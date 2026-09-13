# Evidence 56C — Kafka 2.0 KIP-279 Largest-Common-Epoch Recovery

## Target case

[`cases/56-apache-kafka-replicated-log-high-watermark.md`](../cases/56-apache-kafka-replicated-log-high-watermark.md)

Parent grounding record: [`56-kafka-082-replication-high-watermark-grounding.md`](56-kafka-082-replication-high-watermark-grounding.md).

Earlier leader-epoch deepening: [`56-kafka-0110-leader-epoch-lineage-truncation-deepening.md`](56-kafka-0110-leader-epoch-lineage-truncation-deepening.md).

## Status

**`bounded deepening complete`.**

This slice closes one explicit follow-up left by the Kafka 0.11 leader-epoch evidence:

> What exactly changed when KIP-279 corrected the first KIP-101 truncation protocol, and what retained relation does Kafka 2.0 use when one epoch lookup is not enough to identify a safe convergence point?

The bounded answer is:

> **Kafka 2.0 makes the epoch identity of an `OffsetsForLeaderEpoch` end offset explicit, lets a follower walk backward through its retained leader-epoch history when the leader returns an epoch the follower does not know, and can perform intermediate truncations until both replicas reach an epoch they actually share. Recovery therefore converges on a lineage-qualified common prefix rather than comparing an untyped offset from one epoch with a local offset from another.**

This is a recovery-semantics and retained-control-state deepening. It is not a claim that Kafka 2.0 preserves a complete event history, that KIP-279 makes unclean election lossless, that every compaction history preserves all lineage evidence, or that Kafka leader epochs are equivalent to consensus terms in another protocol.

---

## Bounded artifacts and dates

- **KAFKA-6361 — `Fast leader fail over can lead to log divergence between leader and follower`**: created **14 December 2017**, resolved **10 May 2018**, fixed in Kafka **2.0.0**.
- **KIP-279 — `Fix log divergence between leader and follower after fast leader fail over`**: accepted Apache Kafka design proposal by Anna Povzner.
- **Apache Kafka pull request #4882**: implementation of KIP-279; merged with merge commit `9679c44d2b521b5c627e7bde375c0883f5857e0c`.
- **Apache Kafka 2.0.0**: released **30 July 2018**.
- **Exact implementation slice**: source tag `2.0.0`, especially `AbstractFetcherThread.scala`, `ReplicaFetcherThread.scala`, `LeaderEpochFileCache.scala`, `OffsetsForLeaderEpochResponse.java`, and `EpochDrivenReplicationProtocolAcceptanceTest.scala`.

Primary records:

- KIP-279: <https://cwiki.apache.org/confluence/display/KAFKA/KIP-279%3A+Fix+log+divergence+between+leader+and+follower+after+fast+leader+fail+over>
- KAFKA-6361: <https://issues.apache.org/jira/browse/KAFKA-6361>
- implementation PR #4882: <https://github.com/apache/kafka/pull/4882>
- Kafka release archive / downloads record: <https://kafka.apache.org/community/downloads/>

---

## Historical record

### H — KAFKA-6361 records an observed failure after KIP-101, not only a hypothetical protocol puzzle

KAFKA-6361 explicitly says the Kafka team had **observed** an edge case in which replication failover could leave a replica permanently out of sync with the leader, despite KIP-101's improved leader-epoch truncation logic.

The issue constructs the failure with two brokers. A leader in epoch 1 has one batch that replicated and a second batch that did not. The other broker becomes leader in epoch 2 and writes a different suffix. Before the old leader has truncated, leadership changes again and the old leader becomes epoch-3 leader with its earlier epoch-1 suffix still present.

When the epoch-2 follower later asks the new leader for the end of epoch 2, the pre-KIP-279 protocol can return offset `21` even though the new leader never had epoch 2. The issue identifies three outcomes depending on the follower's epoch-2 batch end. The observed case was the one where the follower did not truncate and subsequently hit out-of-order offsets; the operational workaround was to delete the active segment on that replica so it could replicate consistently again.

This source therefore supports a stronger historical claim than `someone imagined an edge case`:

```text
KIP-101 lineage lookup
    -> still had an ambiguity in at least one deployed recovery history
    -> observed replica non-convergence
    -> protocol correction tracked as KAFKA-6361
```

It does **not** establish the population frequency of the bug, the exact affected production deployment, or a general claim that Kafka 0.11 replication was unreliable.

### H — KIP-279 identifies the semantic defect as an offset whose epoch provenance is ambiguous

KIP-279 states the problem directly: the follower can receive an offset for an epoch it does not know about and then compare that offset against offsets from a different epoch.

That matters because the same numerical offset range can belong to different leadership histories. The proposal therefore sets a more precise target than `find a smaller offset`:

> truncate the follower to the **largest common log prefix, where both offsets and epochs match**.

The historical correction is consequently not just `add more retries`. It changes what the response means.

### H — response version 1 carries the actual leader epoch associated with the returned end offset

KIP-279 proposes adding `leader_epoch` to each partition result in `OffsetsForLeaderEpochResponse`.

Kafka 2.0.0 implements that distinction in `OffsetsForLeaderEpochResponse.java`:

- response partition schema V0 contains error, partition, and `end_offset`;
- response partition schema V1 adds `LEADER_EPOCH`;
- the implementation comment says that this field specifies **which leader epoch the end offset belongs to**;
- when parsing an older response that lacks the field, the object uses the no-partition-leader-epoch sentinel rather than inventing provenance that was not transmitted.

Primary source:

- <https://github.com/apache/kafka/blob/2.0.0/clients/src/main/java/org/apache/kafka/common/requests/OffsetsForLeaderEpochResponse.java>

This is the core protocol-level repair:

```text
end offset
    -> end offset + actual epoch identity
```

The extra field does not make the response a complete replica history. It supplies only the provenance needed for the bounded truncation decision.

### H — the leader answers with the largest retained epoch less than or equal to the requested epoch

Kafka 2.0.0 `LeaderEpochFileCache.endOffsetFor` now returns a pair `(epoch, end offset)`, not only an offset.

Its source documentation says:

- the returned epoch is the largest epoch less than or equal to the requested epoch;
- that epoch's end is the start offset of the first larger epoch, or current log end if the requested/latest epoch is the latest known epoch;
- if the request precedes the first tracked epoch, the implementation returns an undefined result so recovery can fall back to the high-watermark path during upgrade/history gaps.

Primary source:

- <https://github.com/apache/kafka/blob/2.0.0/core/src/main/scala/kafka/server/epoch/LeaderEpochFileCache.scala>

This is an important difference from interpreting `end_offset` alone. The leader can say, in effect:

```text
"I do not have your requested epoch 2;
 the closest earlier epoch I actually have is epoch 1,
 and its end is offset X."
```

instead of returning `X` without exposing which lineage produced it.

### H — Kafka 2.0 can perform an intermediate truncation and then ask again

`AbstractFetcherThread.getOffsetTruncationState` in the 2.0.0 source implements the iterative part of KIP-279.

When the leader replies with a valid `(leader epoch, end offset)` but the follower's epoch cache does not contain that exact returned epoch, the follower:

1. asks its own epoch cache for the largest local epoch less than the leader-returned epoch;
2. computes that local epoch's end offset;
3. truncates to that intermediate boundary;
4. records `truncationCompleted = false`.

The fetcher state machine then remains in the truncating phase, so another `OffsetsForLeaderEpoch` exchange can be issued using the follower's now-earlier latest epoch.

If the returned epoch is also known locally, final truncation is bounded by the follower's end for that epoch, the leader's returned end offset, and the follower's current log end.

Primary source:

- <https://github.com/apache/kafka/blob/2.0.0/core/src/main/scala/kafka/server/AbstractFetcherThread.scala>

The exact shipping implementation therefore supports:

```text
one lookup failed to establish common lineage
    -> intermediate rollback of later local lineage
    -> another lookup
    -> repeat until common lineage or fallback boundary
```

`truncationCompleted = false` is significant retained/run-time control state for this process, but it is not a durable cross-crash event history and should not be described as one.

### H — KIP-279 does not eliminate high-watermark fallback

Kafka 2.0.0 retains several compatibility/history-gap branches.

`AbstractFetcherThread` says an undefined epoch offset can occur when:

- the leader is still using message format older than the leader-epoch regime; or
- the follower asks for an epoch older than the first one retained by the leader.

That branch uses the follower's initial truncation offset, which for the ordinary follower path is its high-watermark-based recovery reference.

A second compatibility branch handles a valid end offset whose response has no epoch identity. The source says this can happen when leader or follower uses the pre-`KAFKA_2_0_IV0` inter-broker protocol response format; in that case the leader's offset is used without the iterative epoch comparison available in response V1.

`ReplicaFetcherThread` makes the rollout boundary explicit:

- `OffsetsForLeaderEpoch` request/response version `1` is used when inter-broker protocol is at least `KAFKA_2_0_IV0`;
- older inter-broker protocol uses version `0`;
- if the cluster cannot send the leader-epoch request at all, the fetcher synthesizes an undefined epoch/offset result so the truncation path falls back to the older high-watermark behavior.

Primary sources:

- <https://github.com/apache/kafka/blob/2.0.0/core/src/main/scala/kafka/server/AbstractFetcherThread.scala>
- <https://github.com/apache/kafka/blob/2.0.0/core/src/main/scala/kafka/server/ReplicaFetcherThread.scala>

Thus:

```text
software upgraded to 2.0
    !=
KIP-279 response semantics active for every replication exchange
```

The inter-broker protocol state is part of the effective recovery regime.

### H — the high watermark still answers a different question after KIP-279

Kafka 2.0.0 `ReplicaFetcherThread.processPartitionData` still advances the follower high watermark as:

```text
min(follower log end offset, leader-reported high watermark)
```

KIP-279 therefore does not replace the high watermark as the replicated/committed-prefix frontier. It refines the **lineage comparison used to decide divergent-log truncation**.

This preserves the layered result from Evidence 56B:

```text
high watermark
    !=
leader-epoch lineage
```

and adds:

```text
leader-epoch lineage
    !=
one scalar epoch lookup
```

because some histories require walking backward across multiple retained epoch relations.

### H — Apache added a release-level test for repeated unclean leader changes

Kafka 2.0.0's `EpochDrivenReplicationProtocolAcceptanceTest` contains `logsShouldNotDivergeOnUncleanLeaderElections`.

The test:

- creates two brokers with unclean leader election enabled;
- uses replication factor 2 and `min.insync.replicas = 1`;
- repeatedly shuts down one broker, brings up the other, and writes under successive leadership histories;
- restarts the second broker and waits for logs to converge;
- compares the active-segment batch checksum sequence between both brokers.

The implementation PR says this test failed before the KIP-279 fix was applied.

Primary sources:

- <https://github.com/apache/kafka/blob/2.0.0/core/src/test/scala/unit/kafka/server/epoch/EpochDrivenReplicationProtocolAcceptanceTest.scala>
- <https://github.com/apache/kafka/pull/4882>

This is implementation-era validation of the targeted failure history. It is not exhaustive proof over all partitions, filesystems, crashes, protocol mixes, or future Kafka versions.

### H — KIP-279 explicitly exposes a compaction/reconstruction boundary for lineage retention

The KIP's `Impact of topic compaction` section says the proposed solution requires preserving history in the leader-epoch sequence file. It notes a narrower failure path:

1. the epoch file itself is lost;
2. the broker must rebuild epoch history from the retained log;
3. log compaction may already have removed every offset belonging to a particular epoch;
4. reconstruction can therefore miss that epoch entry.

The KIP lists possible compaction changes—such as leaving a tombstone for an otherwise-removed epoch or not compacting beyond persistent high watermark—but explicitly says those changes are **not** made by KIP-279.

Primary source:

- KIP-279, `Impact of topic compaction`.

The safe historical claim is therefore:

```text
KIP-279's convergence algorithm depends on retained epoch history
    !=
every possible loss-and-rebuild path preserves complete epoch history
```

Do not turn this into `Kafka compaction is unsafe` or `the epoch checkpoint is always sufficient`. The source identifies a conditional reconstruction gap, not a universal failure.

---

## Engineering reconstruction

The following formulations are project-level reconstructions, not Apache's historical vocabulary.

### E — an offset is not self-authenticating recovery evidence

A numerical log position says **where** a boundary lies. KAFKA-6361 demonstrates that it does not, by itself, say **which leadership lineage** that boundary belongs to.

Therefore:

```text
same / comparable offset
    !=
same lineage-qualified history
```

KIP-279 strengthens recovery by returning the epoch identity that gives the end offset its interpretation.

### E — recovery metadata can need provenance about its own value

The end offset in a protocol response is already control metadata. KIP-279 adds metadata about that metadata: the epoch under which the returned boundary is meaningful.

That supports a recursive relation:

```text
recovery boundary value
    + provenance of that boundary
    -> stronger recovery authority
```

This does not imply an infinite regress. The bounded protocol has a concrete stopping rule: find an epoch both replicas know, then compare the end offset within that epoch.

### E — convergence can be a negotiated walk over two retained histories

KIP-101 made a follower ask the leader about one retained epoch. KIP-279 makes the response itself capable of redirecting the comparison to an older epoch.

Thus a safe truncation boundary may be discovered through repeated comparison rather than already existing as one scalar stored identically on both replicas:

```text
follower lineage
      +
leader lineage
      +
iterative comparison
      -> largest common epoch
      -> common offset boundary within that epoch
```

The retained state is local and asymmetric; convergence is computed from the relation between those local histories.

### E — intermediate truncation is not yet convergence

Kafka 2.0 records whether a truncation step is final. When the follower backs up to an earlier locally known epoch because it does not recognize the leader-returned epoch, `truncationCompleted = false` keeps the recovery procedure active.

Therefore:

```text
some divergent suffix removed
    !=
common lineage established
    !=
ordinary replication resumed
```

This is a useful counterexample to treating `truncate` as one atomic semantic event.

### E — stronger lineage evidence can extend below the current high watermark in exceptional histories

KIP-279 explicitly says unclean-election recovery may have to look further back than the high watermark to find the largest epoch known to both brokers.

This does **not** mean that high watermark is normally irrelevant or that committed data may always be freely discarded. It means that under the policy/failure histories being repaired, the current scalar frontier may be insufficient to identify where histories last agreed.

The important relation is:

```text
commit/visibility frontier
    !=
complete lineage-comparison search space
```

### E — payload compaction and lineage retention have different sufficiency conditions

A compacted log may remain perfectly adequate for serving current keyed state while no longer containing at least one record from every historical leader epoch. If the separate epoch history survives, recovery can still use it. If that history is lost and must be reconstructed from the compacted payload, some lineage distinctions may be unavailable.

Thus:

```text
payload sufficient for current service
    !=
payload sufficient to reconstruct all recovery metadata
```

This is one of the clearest retention-specific results in the slice. It is grounded in KIP-279's own compaction discussion, not projected from a generic archival metaphor.

### E — compatibility fallback is a reduction in recovery evidence, not proof of immediate data loss

Kafka 2.0 can deliberately fall back to older truncation evidence when protocol/history support is absent.

So:

```text
lineage evidence unavailable
    -> weaker bounded recovery rule
    !=
automatic proof of corrupted payload
```

Whether loss or divergence occurs still depends on the concrete leadership/failure history and policy configuration.

---

## Functional analogies — bounded

### A — Raft Case 58: term/index matching

Raft and Kafka both show that log position alone is not enough to establish a safe continuation after leadership changes. Raft couples an index with a term inside a consensus protocol; Kafka KIP-279 compares retained partition leader epochs and offsets to select a truncation boundary.

The analogy stops there. Kafka's ISR/high-watermark replication design, ZooKeeper-era leadership, election policies, and follower recovery are not Raft's consensus protocol, and no genealogy is inferred from the shared use of epoch/term-like lineage markers.

### A — RADOS Case 05: peering/currentness

RADOS peering and Kafka KIP-279 both reject `the longest surviving copy wins`. Each uses retained protocol evidence to determine which surviving state is admissible before repair/convergence.

The evidence structures and repair algorithms are different. This is functional comparison only.

### A — HDFS generation/recovery stamps

HDFS generation/recovery stamps and Kafka leader epochs both qualify surviving bytes with version/authority information. KIP-279 adds an especially explicit counterexample: a numerically plausible boundary can still be wrong if its version/epoch provenance is misinterpreted.

No common implementation or historical influence is claimed.

---

## Philosophical / media-theoretical interpretation — bounded

### I — persistence of an ordered history is persistence of discriminations, not only records

The exact technical fact is that both brokers can retain bytes at overlapping offsets while disagreeing about which leadership history those bytes belong to. KIP-279 therefore needs a retained distinction—epoch lineage—to decide which continuation counts as common.

A narrow project interpretation is:

> **for an ordered replicated history, retention can require preserving not only records but also enough distinctions to judge whether two surviving sequences belong to the same continuation.**

This is not Apache's philosophical vocabulary and does not imply that every archive or memory has a Kafka-like lineage relation.

### I — forgetting can be constitutive of restored continuity

KIP-279 may repeatedly truncate a follower before ordinary fetching resumes. The procedure is retention-preserving only relative to a protocol-qualified continuation: some physically surviving suffixes must be forgotten so the replica can rejoin the accepted history.

This does not make deletion intrinsically preservative. The claim is bounded to a recovery protocol whose evidence and authority rules have already selected another continuation.

---

## Explicit non-claims

1. **KIP-279 did not invent Kafka leader epochs.** KIP-101 already introduced the earlier leader-epoch truncation protocol.
2. **KIP-279 is not evidence that every Kafka divergence bug ended in 2.0.** This slice grounds one correction and its exact source path.
3. **`leader_epoch` in response V1 is not a complete provenance record.** It identifies the epoch associated with one returned end boundary.
4. **Largest-common-epoch recovery is not the same thing as consensus.** No Kafka↔Raft equivalence is claimed.
5. **High watermark did not become obsolete.** Kafka 2.0 still uses it for replicated/committed-prefix state and as a fallback in specified recovery gaps.
6. **A fallback to high watermark does not prove data loss occurred.** It means the stronger lineage comparison is unavailable in that branch.
7. **A persistent leader-epoch checkpoint is not an infallible correctness certificate.** It can be truncated/pruned with log history and the KIP itself discusses loss/rebuild limits.
8. **Topic compaction is not claimed to break KIP-279 under normal operation.** The bounded risk is loss of the epoch file followed by reconstruction from a log that no longer contains evidence of every epoch.
9. **The proposed compaction fixes in KIP-279 are not treated as implemented by this KIP.** The document explicitly leaves them for possible future work.
10. **The integration test is not an exhaustive proof.** It validates a concrete repeated-leadership failure history.
11. **The observed KAFKA-6361 incident is not used to estimate bug frequency.** No deployment population is available here.
12. **Kafka 2.0 protocol behavior is not silently projected onto 0.11.0.0.** Evidence 56B remains the bounded record for KIP-101-era semantics.
13. **No claim is made that current KRaft-era Kafka uses exactly this ZooKeeper-era recovery machinery unchanged.**
14. **No direct historical genealogy is inferred from functional similarities to RADOS, HDFS, Raft, or other replicated-log systems.**

---

## Claim ledger

| Claim | Layer | Evidence strength |
| --- | --- | --- |
| KAFKA-6361 documents an observed post-KIP-101 non-convergence edge case | historical record | strong Apache JIRA record |
| KIP-279 targets largest common prefix where offset and epoch both match | historical record | strong accepted KIP |
| response V1 adds the actual `leader_epoch` associated with returned `end_offset` | historical record | exact Kafka 2.0 source |
| leader returns largest retained epoch `<= requested` plus its end offset | historical record | exact Kafka 2.0 source |
| follower can intermediate-truncate and issue another epoch request | historical record | exact Kafka 2.0 source |
| `truncationCompleted = false` distinguishes an intermediate from final recovery step | historical record / engineering consequence | exact source |
| Kafka 2.0 keeps HW semantics distinct and preserves compatibility fallbacks | historical record | exact source |
| release test exercises repeated unclean-leader histories and compares final batch checksums | historical record | exact 2.0 test + implementation PR |
| lost epoch checkpoint + compacted-away epoch can make lineage reconstruction incomplete | historical record | accepted KIP boundary |
| same offset does not establish same lineage-qualified history | engineering reconstruction | strongly entailed by bug/fix |
| payload service sufficiency does not imply full recovery-metadata reconstructability | engineering reconstruction | bounded KIP compaction consequence |
| Raft/RADOS/HDFS comparisons are functional only | functional analogy | explicitly bounded |
| persistence of ordered history can require retention of discriminating lineage state | philosophical interpretation | bounded project reading |

---

## Related-repository duplication check

A fresh search of `tmzncty/computing-archaeology` for `Kafka leader epoch` returned no dedicated Kafka replication/leader-epoch technical-history module. This record therefore contains the bounded retention-specific source analysis needed here rather than duplicating an existing companion-repository account.

If `computing-archaeology` later grows a Kafka protocol-history case, move broad chronology there and keep only the retention-specific lineage/currentness comparison here.

---

## Remaining evidence debt

This slice closes the explicit `KIP-279/post-0.11 leader-epoch correction chronology and exact largest-common-epoch convergence semantics` item from the Case 56 grounding record.

Still open:

- independent fault injection against an unmodified Kafka 2.0.0 deployment, including checkpoint-loss plus compacted-log reconstruction;
- exact later changes to `OffsetsForLeaderEpoch` and leader-epoch cache behavior after 2.0;
- KRaft metadata/leader-epoch semantics as a separate modern regime;
- transactional high watermark versus Last Stable Offset;
- exact filesystem/device durability below epoch checkpoint and payload-log writes;
- ZooKeeper ISR/leader-state crash behavior if a later synthesis needs it;
- policy history of `unclean.leader.election.enable` defaults and deployment practice.

None of those gaps blocks this bounded deepening.