# Case 83 deepening — HDFS-11187, reconstructible last-partial-checksum cache, and the cost boundary of coherent verification (2016–2018)

## Purpose

Deepen Case 83 at a boundary left open by the HDFS-11160 analysis: **after Apache fixed a concurrent append/scan false-corruption race by reading the last partial checksum of a finalized replica while holding the dataset lock, how did HDFS later reduce the resulting lock/I/O cost without giving up the need for checksum/data currentness?**

The bounded answer is HDFS-11187 and Apache Hadoop commit `2021f4bdce3b27c46edaad198f0007a26a8a1391` from 3 February 2018. The change adds an in-memory `lastPartialChunkChecksum` to `FinalizedReplica`, carries that checksum through relevant replica-state transitions when available, and otherwise reconstructs it lazily from the ordinary on-disk metadata file. The Hadoop 2.7.6 release source confirms that this design shipped in a named release.

This slice is useful for `technical-retention` because it exposes **two different kinds of retained integrity state**:

1. the ordinary on-disk checksum metadata needed to verify a replica;
2. a volatile, reconstructible in-memory checksum cache used to avoid repeated disk I/O and lock contention while preserving the last-partial-chunk relation needed by concurrent readers/scanners.

The cache is not another user-data copy and is not evidence that HDFS persists every verification-relevant relation across process restart. Its loss is recoverable from the durable metadata path; its **currentness while present**, however, matters for whether a later verifier uses the right checksum for the visible payload state.

This addendum separates:

- **historical record (`H/P`)** — Apache JIRA, Apache Hadoop commit history, and release-tag source;
- **engineering reconstruction (`E`)** — controlled retention relations inferred from the implementation;
- **functional analogy (`A`)** — comparison to other retained auxiliary state in this repository;
- **rejected strengthening (`X`)** — claims not supported by the bounded evidence.

It does not establish invention priority for checksum caching, lazy loading, replica-state metadata propagation, copy-on-write integrity state, or lock-free verification.

---

## Source set and evidence grade

| Source | Date | Type | Use here | Grade |
| --- | --- | --- | --- | --- |
| Apache JIRA HDFS-11160 | resolved 2016-12-16 | contemporary Apache bug record | correctness predecessor: false corruption classification during concurrent append/scan | **H/P** |
| Apache JIRA HDFS-11187 | created 2016-11-29; resolved 2018-02-21 | contemporary Apache improvement record | primary statement that the HDFS-11160 implementation repeatedly read the last partial checksum from disk while holding `FsDatasetImpl` lock and proposed keeping an up-to-date in-memory value | **H/P** |
| Apache JIRA HDFS-12136 | created 2017-07-13; later resolved `Won't Fix` | contemporary Apache performance issue | operational witness for lock/I/O contention caused by the HDFS-11160 strategy and for the demand to remove disk I/O from the dataset lock | **H/P** |
| Apache Hadoop commit `2021f4bd...` | 2018-02-03 UTC | Apache source commit | implementation witness for `FinalizedReplica.lastPartialChunkChecksum`, lazy reconstruction, and checksum propagation across replica transitions | **H/P** |
| Apache Hadoop `rel/release-2.7.6` `BlockSender.java` / `FinalizedReplica.java` | released 2018-04-16 | tag-matched release source | confirms the lazy cached-checksum mechanism in a named released branch | **H/P** |
| Hadoop 2.7.6 release notes | 2018-04-16 | Apache release documentation | confirms HDFS-11187 is included as a major DataNode improvement | **H/P** |
| Existing Case 83 HDFS-11160 deepening | repository evidence | grounded internal evidence | establishes the preceding checksum/data observation-coherence problem and lock-based fix | **H/P + E** |

`H/P` means historical/primary project evidence under this repository's conventions; it does not imply peer-reviewed publication.

---

## Historical record

### H/P — HDFS-11160 fixed a currentness race by doing metadata I/O while the dataset lock was held

The preceding Case 83 deepening already grounds HDFS-11160: `VolumeScanner` could compare a checksum from one concurrent state with data from another and report a good replica as corrupt. Apache's December 2016 fix obtained the last partial checksum for a `FinalizedReplica` while the dataset lock was held.

That gives the starting point for this slice:

```text
need a checksum corresponding to the visible payload boundary
        -> read last partial checksum while dataset relation is locked
        -> avoid one false-mismatch race
```

The fix improved observation coherence, but the mechanism coupled **disk metadata I/O** to a broadly contended DataNode lock.

This predecessor matters because HDFS-11187 is not an independent feature story. It is explicitly an optimization of the state relation introduced/strengthened by HDFS-11160.

---

### H/P — HDFS-11187 explicitly proposes an up-to-date in-memory checksum relation

Apache JIRA HDFS-11187 states that HDFS-11160 ensures `BlockSender` reads the correct version of the metadata file when concurrent writers exist, but calls the implementation non-optimal because it must read the last partial chunk checksum from disk while holding the `FsDatasetImpl` lock for every reader.

The issue then states the intended optimization directly: keep an **up-to-date version of the last partial checksum in memory** and reduce disk access.

That wording supports a narrow historical claim:

> By late 2016 Apache developers were treating the last-partial-chunk checksum not only as durable metadata on disk, but also as a candidate piece of in-memory state whose currentness had to track replica transitions closely enough to serve concurrent reads/scans without repeated lock-held metadata I/O.

Do not strengthen this into `the in-memory checksum becomes the sole authority`. The patch retains the on-disk metadata path and reconstructs the in-memory value from it when necessary.

---

### H/P — HDFS-12136 records the service cost of performing metadata I/O inside the dataset lock

HDFS-12136, opened in July 2017, says the HDFS-11160 implementation reads the last partial chunk checksum from disk while holding the exclusive dataset lock for `BlockSender` construction. The issue reports severe serialization under high I/O / xceiver activity and describes DataXceiver threads, replication, decommissioning, heartbeat processing, and client pipelines contending around that lock.

The issue was ultimately resolved `Won't Fix`, so its proposed patch should not be silently treated as the released solution. Its historical value here is different: it documents that the correctness fix had become an operational contention problem and records an explicit engineering preference to eliminate disk I/O from that lock.

Controlled boundary:

> **a correctness-preserving observation boundary can itself become a liveness/service hazard when expensive I/O is placed inside a highly contended lock.**

This is an implementation-specific historical tradeoff, not a universal theorem that locks and I/O can never be combined safely.

---

### H/P — 2018 commit `2021f4bd...` adds `lastPartialChunkChecksum` to `FinalizedReplica`

Apache Hadoop commit `2021f4bdce3b27c46edaad198f0007a26a8a1391`, committed 3 February 2018 under HDFS-11187, makes the proposed auxiliary state concrete.

In `FinalizedReplica` the commit adds:

```text
private byte[] lastPartialChunkChecksum;
```

plus getters/setters, constructors that can receive the checksum, copy-constructor propagation, and `loadLastPartialChunkChecksum()` for reconstructing it from the replica's block/meta files.

This is a direct source-level witness for a new retained state class:

```text
on-disk block + checksum metadata
        !=
in-memory last-partial-checksum cache attached to FinalizedReplica
```

The second state exists to make later access cheaper and more coherent under the implementation's concurrency model; it is not another durable payload representation.

---

### H/P — loading the cache is intentionally lazy because eager reconstruction would increase DataNode startup latency

The new `BlockSender.getPartialChunkChecksumForFinalized()` contains an unusually explicit design comment. It says there are many places where a finalized replica object is created and that loading the last partial checksum whenever such an object is created would increase DataNode initialization latency; therefore the checksum is loaded **lazily**.

For a finalized replica whose visible length ends in a partial checksum chunk and whose cached checksum is `null`, `BlockSender` calls `loadLastPartialChunkChecksum()` and stores the reconstructed value. If the metadata file is missing, the code logs the condition and returns `null`, preserving the pre-existing fallback behavior rather than claiming successful reconstruction.

The released Hadoop 2.7.6 `BlockSender.java` contains the same lazy-loading explanation and path.

This is strong negative evidence against treating every useful integrity relation as something that must itself be persisted or eagerly restored at boot:

> **restart-surviving integrity metadata != eager reconstruction of every performance/currentness cache derived from it.**

The implementation explicitly chooses `reconstruct on first relevant use` for this auxiliary state.

---

### H/P — the optimization moves disk checksum loading out of the dataset-lock critical section

In the HDFS-11187 commit, `BlockSender` still obtains the replica and visible length while holding the dataset lock, but the old call that loaded the finalized replica's last checksum inside that critical section is removed.

After the lock-scoped lookup, the code separately obtains the last checksum for `ReplicaBeingWritten` / `FinalizedReplica`. For finalized replicas, `getPartialChunkChecksumForFinalized()` either uses the already retained in-memory checksum or lazily reconstructs it from disk.

The bounded historical result is therefore:

```text
HDFS-11160 regime:
lock-scoped replica observation
    + disk read of last partial checksum inside the lock

HDFS-11187 regime:
lock-scoped replica / visible-length observation
    + retained in-memory checksum when available
    + lazy disk reconstruction when absent
```

Do not convert this into `HDFS-11187 eliminates all locking from BlockSender` or `all checksum I/O is now lock-free`. The commit changes one specific last-partial-checksum path.

---

### H/P — the checksum is propagated across relevant replica-state transitions instead of being treated as a disposable local variable

The HDFS-11187 commit does more than add a cache field.

Its diff shows the checksum relation being carried through several object/state transitions:

- a `FinalizedReplica` copy constructor copies the last partial checksum;
- replica builders can receive the checksum when creating a finalized replica;
- when a block becomes finalized, the implementation can copy the last checksum from a prior finalized or RBW representation into the new finalized replica;
- when a finalized replica is opened for append and converted to RBW, the new RBW receives `finalized.getLastPartialChunkChecksum()` rather than unconditionally rereading the metadata file in that transition;
- one recovery/finalization path explicitly reloads the last partial checksum when reusing the original finalized replica.

This supports a narrow but important statement:

> **the optimization depends on maintaining checksum currentness across replica-state changes, not merely memoizing one disk read forever.**

The exact state machine is HDFS-specific. This evidence does not justify a generic rule that every storage system must propagate integrity metadata through the same transitions.

---

### H/P — Hadoop 2.7.6 confirms the cache/lazy-load design shipped in a named release

HDFS-11187 lists several fixed versions, including 2.7.6, 2.8.4, 2.9.1, 3.0.3, 3.1.0, and 2.10.0. Hadoop 2.7.6 release notes list HDFS-11187 as a DataNode improvement.

Tag-matched `rel/release-2.7.6` source contains:

- `FinalizedReplica.lastPartialChunkChecksum`;
- constructors and copy behavior for that field;
- `loadLastPartialChunkChecksum()` from the ordinary metadata file;
- the `BlockSender` lazy-load path with the explicit startup-latency comment.

This turns the mainline commit into a named-release implementation witness rather than leaving it as an unshipped patch proposal.

---

## Retained-state decomposition

The 2018 implementation makes a finer decomposition useful.

### 1. User payload

The block data remains the payload embodiment being protected/qualified.

### 2. Durable checksum metadata

The metadata file contains the checksum information from which verification is performed and from which the last partial checksum can be reconstructed.

This is not the payload itself.

### 3. Volatile `FinalizedReplica.lastPartialChunkChecksum`

This is a process-memory copy of the integrity relation for the final partial chunk.

It is:

- not the full checksum file;
- not a full-block verification result;
- not a persisted scanner certificate;
- reconstructible from the metadata file when absent;
- operationally useful because its current value can be reused without repeated disk I/O.

### 4. Visible-length / replica-state relation

The checksum has meaning only relative to the payload length/state for which it was produced. A byte array without the associated visible data boundary is not sufficient evidence that the cache applies to the bytes now being judged.

### 5. Scanner traversal state

Case 83's cursor is a different auxiliary state. It records where broad maintenance traversal had progressed and is deliberately persisted to a cursor file.

This contrast is useful:

```text
scanner cursor
    = persisted/restart-oriented maintenance-progress checkpoint

lastPartialChunkChecksum cache
    = volatile/reconstructible integrity-currentness optimization
```

Both are auxiliary to the user payload, but they have different required persistence horizons.

---

## Engineering reconstruction

### E1 — durable source state and reconstructible cache are different retention obligations

The 2018 path supports:

> **durable checksum metadata != volatile checksum cache.**

If the cache disappears, the implementation can reconstruct it from the metadata file. Therefore cache loss alone is not equivalent to checksum-metadata loss or payload loss.

Conversely, a warm in-memory cache does not replace the need for durable metadata across restart.

---

### E2 — cache persistence horizon can be shorter than the object's logical persistence horizon

A finalized HDFS replica can survive DataNode process lifetime boundaries on disk while the Java object and its in-memory checksum cache do not.

The release source deliberately avoids rebuilding all such cache state at DataNode initialization and instead restores it on demand.

Therefore:

> **logical replica persistence != persistence of every auxiliary state used to serve that replica efficiently.**

This is one concrete example of a system choosing **reconstructibility** rather than persistence for an auxiliary relation.

---

### E3 — reconstructible does not mean semantically irrelevant

The cache can be rebuilt, but while it exists it participates in a correctness-sensitive relation: the last partial checksum must correspond to the visible payload boundary relevant to the reader/scanner.

Therefore:

> **reconstructible state != semantically disposable state.**

Losing the cache can be safe if reconstruction is correct. Retaining a stale or incorrectly propagated cache could be worse than losing it, because a verifier may act on the wrong integrity evidence.

This is an engineering reconstruction from the bug/fix sequence; the evidence does not document every possible stale-cache failure mode experimentally.

---

### E4 — retaining derived state can trade repeated I/O for invalidation/propagation complexity

HDFS-11160 paid repeated disk-I/O and locking cost to obtain a current checksum relation. HDFS-11187 retains a derived value in memory and propagates it across state transitions.

That changes where complexity lives:

```text
re-read authoritative metadata on each relevant access
        vs
retain derived state + keep it current + reconstruct when absent
```

The second regime can reduce repeated I/O, but it introduces a new obligation: the derived state must either be correctly propagated/updated or intentionally discarded so it can be reconstructed.

This is a bounded engineering comparison, not evidence that caching always improves performance or correctness.

---

### E5 — eager startup reconstruction is not required merely because later access may need the state

The source comment gives a direct design reason for lazy loading: eager loading across all finalized replicas would increase DataNode initialization latency.

Therefore:

> **state needed eventually != state that must be reconstructed before service startup completes.**

A system can defer reconstruction until the first operation whose semantics require that relation, provided the durable source remains available and the access path handles absence correctly.

---

### E6 — integrity-currentness state and maintenance-progress state have different failure consequences

Within Case 83 itself:

- losing the persisted scanner cursor can replay already-covered traversal and consume future scan budget;
- losing the in-memory partial-checksum cache causes a later lazy reconstruction from disk;
- losing/corrupting the durable checksum metadata is a different and more serious integrity-evidence failure;
- retaining a stale checksum relation risks a false verification judgment.

Therefore:

> **auxiliary state loss has mechanism-specific consequences; `metadata lost` is too coarse a category.**

---

## Functional comparisons

### A — Case 83 cursor checkpoint versus last-partial-checksum cache

This is an intra-case functional comparison, not a claim that the two structures share a common implementation.

The block-iterator cursor is persisted because restart continuity of broad maintenance traversal is useful. The last-partial checksum cache is deliberately allowed to begin absent and is reconstructed lazily because eager restoration would increase startup cost.

Thus Case 83 now contains two opposite retention policies for auxiliary state:

```text
persist progress because replay is costly
        vs
reconstruct checksum cache because eager restoration is costly
```

The difference is not `important state` versus `unimportant state`; it is a difference in **reconstruction cost, source availability, and required persistence horizon**.

### A — Case 79 startup block-report re-observation

Case 79 shows that the NameNode can rebuild current replica-location knowledge after restart from DataNode reports rather than requiring every location relation to be represented as one monolithic durable image.

HDFS-11187 is a much smaller local mechanism, but the bounded functional analogy is:

> **some operational state can be reconstructed from surviving lower-layer evidence instead of being independently persisted.**

Do not infer shared code, common ancestry, or equivalent authority. Replica-location reconstruction and partial-checksum cache reconstruction operate at different layers with different consequences.

---

## Philosophical interpretation — bounded

The useful philosophical point is not that `memory is cache`.

The technical case supports a narrower statement:

> A persistent technical object can depend on auxiliary relations whose own required lifetime is shorter than the object's lifetime, provided those relations can be re-established from surviving evidence when they become necessary again.

This complicates a simple equation of `what must persist` with `everything the running system currently knows`. Some state is worth retaining durably; some is worth retaining only while current; some is intentionally forgotten and reconstructed because preserving it across every boundary would cost more than recomputing it.

That is a bounded interpretation of this implementation. It is not Apache historical vocabulary and should not be generalized to human memory or archives without separate argument.

---

## Rejected / unsupported claims

Do **not** claim:

- HDFS-11187 invented checksum caching;
- HDFS-11187 is the first storage system to retain integrity metadata in memory;
- HDFS-12136's unmerged proposal is the implementation that shipped;
- the in-memory `lastPartialChunkChecksum` is the sole authoritative checksum for the replica;
- the cache is persisted across DataNode process or machine restart;
- cache loss is payload loss;
- cache loss is checksum-file loss;
- lazy loading proves every startup/restart path is correct under arbitrary failure;
- HDFS-11187 eliminates all dataset locking or all metadata I/O from `BlockSender`;
- the 2018 commit makes all concurrent HDFS reads snapshot-atomic;
- a non-null cached checksum is a durable per-block proof that the block is good;
- one cached partial checksum proves the rest of the block verified successfully;
- copying the cache across replica objects proves arbitrary crash consistency;
- the ordinary metadata file itself is proven power-loss-safe by this source set;
- the tag-matched 2.7.6 code proves every downstream Hadoop distribution used identical locking/currentness semantics;
- the HDFS cache is historically or technically identical to CPU caches, database buffer pools, ZFS metadata caches, or SSD controller RAM.

---

## Prior-art boundary

This slice makes no priority claim for:

- keeping checksums or hashes in volatile memory;
- lazy loading;
- memoization/caching;
- propagating derived integrity state through object transitions;
- separating durable authoritative state from reconstructible runtime state;
- moving I/O out of a contended lock.

The safe historical claim is only:

> **Apache HDFS-11187 documents a 2016–2018 design transition in which the last partial checksum of a finalized replica becomes explicit reconstructible in-memory state, lazily loaded from on-disk metadata when absent and propagated across selected replica transitions, in order to reduce the disk-I/O/locking cost exposed after HDFS-11160.**

---

## Related-repository check

A fresh search of `tmzncty/computing-archaeology` for `HDFS-11187` and `BlockSender` found no dedicated treatment to reuse during this slice.

Accordingly this addendum keeps only the retention-specific distinction among durable checksum metadata, volatile/current auxiliary checksum state, and persisted scanner-progress state. A broader history of HDFS append semantics, checksum-file formats, `BlockSender`, DataNode lock evolution, or GFS→HDFS integrity scanning still belongs primarily in `computing-archaeology` if developed.

---

## Sources

### Primary / contemporary

- Apache JIRA HDFS-11160, **VolumeScanner reports write-in-progress replicas as corrupt incorrectly**, resolved 16 December 2016: <https://issues.apache.org/jira/browse/HDFS-11160>
- Apache JIRA HDFS-11187, **Optimize disk access for last partial chunk checksum of Finalized replica**, created 29 November 2016; resolved 21 February 2018: <https://issues.apache.org/jira/browse/HDFS-11187>
- Apache JIRA HDFS-12136, **BlockSender performance regression due to volume scanner edge case**, created 13 July 2017: <https://issues.apache.org/jira/browse/HDFS-12136>
- Apache Hadoop commit `2021f4bdce3b27c46edaad198f0007a26a8a1391`, **HDFS-11187. Optimize disk access for last partial chunk checksum of Finalized replica**, 3 February 2018 UTC: <https://github.com/apache/hadoop/commit/2021f4bdce3b27c46edaad198f0007a26a8a1391>
- Apache Hadoop 2.7.6 release source, `BlockSender.java`: <https://github.com/apache/hadoop/blob/rel/release-2.7.6/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/BlockSender.java>
- Apache Hadoop 2.7.6 release source, `FinalizedReplica.java`: <https://github.com/apache/hadoop/blob/rel/release-2.7.6/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/FinalizedReplica.java>
- Apache Hadoop 2.7.6 release notes, including HDFS-11187: <https://hadoop.apache.org/docs/r2.7.6/hadoop-project-dist/hadoop-common/releasenotes.html>

### Internal

- [`../cases/83-apache-hdfs-block-scanner-checksum-verification.md`](../cases/83-apache-hdfs-block-scanner-checksum-verification.md)
- [`83-hdfs-2016-volume-scanner-concurrent-append-coherence-deepening.md`](83-hdfs-2016-volume-scanner-concurrent-append-coherence-deepening.md)
- [`83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md`](83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md)
- [`../cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md`](../cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md)

---

## Promotion judgment

**Status: `bounded deepening complete`.**

The slice closes the previously open question of a later alternative to HDFS-11160's lock-held checksum I/O at the level needed by Case 83. HDFS-11187 and tag-matched 2.7.6 source show a shipped regime that retains the final partial checksum as reconstructible in-memory state, lazily rebuilds it from durable metadata when absent, and propagates it across selected replica transitions. The evidence does not prove arbitrary crash consistency, full post-2018 scanner evolution, or a universal architecture for checksum caching.