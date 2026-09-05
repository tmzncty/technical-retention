# Apache HDFS DataNode Block Scanner: Periodic Checksum Verification, Retained Scan Progress, and Corrupt-Replica Reporting

## Scope

- **Object / system:** Apache Hadoop HDFS DataNode background block scanning, bounded primarily to the `rel/release-2.7.3` `BlockScanner` / `VolumeScanner` implementation and the HDFS architecture documentation for Hadoop 2.7.3.
- **Historical boundary:** Hadoop issue history shows `DataBlockScanner` already in use in the 0.17/0.18 period in 2008; this case does not claim that the 2.7.x rewrite invented background integrity scanning.
- **Retention question:** what must be retained or repeatedly re-established when a replica can remain present on disk yet cease to be trustworthy because its contents or checksum relation have become corrupt?
- **Status:** `grounded`.

This is **not** a general history of HDFS checksums, Hadoop replication, storage-media bit errors, DataNode disk checking, ZFS scrubbing, GFS checksums, or distributed repair. Case 79 already establishes that a `Blockreport` is positive inventory evidence rather than a content-integrity proof. Case 83 follows that distinction one layer deeper:

> **A replica can be known to exist at a DataNode while its continued qualification as a usable replica still depends on later verification work.**

The project terms `integrity qualification`, `verification age`, `coverage state`, and `maintenance-progress retention` below are **engineering reconstructions**, not Apache historical vocabulary.

---

## Historical vocabulary

The inspected Apache sources use these terms directly:

- `BlockScanner`;
- `VolumeScanner`;
- `block scanner`;
- `scan period`;
- `suspect block`;
- `block iterator`;
- `cursor file`;
- `Successfully scanned`;
- `verification failed`;
- `Reporting bad`;
- `reportBadBlocks`;
- `Blockreport`;
- `checksum`;
- `corrupted` / `corrupt replica` in HDFS documentation and issue history;
- `re-replication`.

Do not silently replace these with stronger historical claims such as `proof of integrity`, `cryptographic attestation`, `scrub certificate`, or `durable trust ledger`. HDFS checksum verification is an engineering integrity check under a fail-stop / corruption model, not a Byzantine or cryptographic proof.

---

## Retained state

The bounded scanner path exposes several distinct state classes.

### 1. DataNode-resident block payload

A physical/logical HDFS block replica stored in the DataNode's local storage remains the user-data embodiment being checked.

### 2. Checksum / replica metadata needed to verify the block

The scanner uses the ordinary block-sending path with checksum verification enabled. The relevant integrity metadata is not another user-data replica; it is evidence used to decide whether the bytes read from this embodiment remain acceptable.

### 3. NameNode-side replica qualification / corruption relation

When the DataNode reports a bad block, the distributed system can stop treating that embodiment as an acceptable replica and later create replacement redundancy from another surviving good source.

This relation is distinct from whether the underlying local block file has already been physically deleted.

### 4. Scan scheduling and coverage state

`BlockScanner` / `VolumeScanner` retain working state such as:

- the configured scan period;
- per-volume scanners;
- the current block iterator;
- the current block-pool pass;
- recent throughput accounting;
- suspect-block queues;
- scanner statistics;
- an iterator/cursor that is periodically saved.

This state does not contain the user payload. It exists so that integrity maintenance can cover a large volume over time instead of repeatedly checking only whichever block happens to be convenient.

---

## Historical record

### H/P — a DataNode block scanner predates the bounded 2.7.3 implementation

Apache issue `HADOOP-3635`, created in June 2008 against Hadoop 0.17.0 and fixed for 0.18.0, reports DataNodes that had **stopped verifying local blocks** after an uncaught exception in `DataBlockScanner`.

This gives a conservative historical anchor: HDFS already had a DataNode background verification mechanism by the 0.17/0.18 period. It does not establish the first invention of distributed background integrity scanning, nor does it license projecting the later `VolumeScanner` implementation backward unchanged.

### H/P — Hadoop 2.7.3 separates replica presence from data integrity

The Hadoop 2.7.3 HDFS architecture documentation says a `Blockreport` contains the list of blocks on a DataNode. In a separate `Data Integrity` section, it states that corruption may arise from storage, network, or software faults; HDFS verifies contents with checksums and can retrieve another replica when a checksum comparison fails. In the robustness section, a **corrupted replica** is one reason the NameNode may initiate re-replication.

This supplies a direct boundary for Case 79 and Case 83:

> **Blockreport presence ≠ checksum-qualified integrity.**

A DataNode can positively report that a block exists while later verification work may still reject that particular embodiment.

### H/P — the 2.7.3 scanner is periodic, rate-limited maintenance

Tag-matched `BlockScanner.java` imports `dfs.datanode.scan.period.hours` and a per-volume target byte rate. Its configuration logic treats a negative scan period as disabled; for compatibility, a configured zero is converted to the historical three-week default. `isEnabled()` additionally requires a positive scan rate.

Tag-matched `VolumeScanner.java` runs one scanner thread per volume and rate-limits its work using a target bytes-per-second value. The scanner therefore does not assert that every block is continuously under observation. Verification is **scheduled coverage work** competing with ordinary storage bandwidth.

Apache issue `HDFS-3194` independently records the intended older default policy in 2012: each block should be scanned once in a 21-day / three-week interval. This is a historical configuration/default witness, not a universal guarantee for every Hadoop release or deployment.

### H/P — successful scan and failed verification lead to different control paths

In Hadoop 2.7.3 `VolumeScanner.scanBlock`, the scanner obtains the current stored block metadata, constructs a `BlockSender` with verification enabled, and streams the block to a null output under a throttler. A successful read calls the result handler with no exception.

`ScanResultHandler.handle` is deliberately more careful than `exception = corrupt`:

- successful verification returns normally;
- if the block is no longer in the dataset, the error is ignored for corruption reporting;
- a `FileNotFoundException` that may be caused by a race with an in-progress write is explicitly not reported as a bad block;
- other verification failures for a still-present block are logged as `Reporting bad` and sent through `datanode.reportBadBlocks(block)`.

This is important negative evidence:

> **scanner I/O failure ≠ unconditional corruption verdict.**

The implementation preserves room for concurrency/race interpretation before deauthorizing a replica.

### H/P — suspect blocks can be pulled forward without replacing periodic coverage

`BlockScanner.markSuspectBlock` says a suspect block should be rescanned soon. `VolumeScanner` maintains a `suspectBlocks` collection and a short-lived `recentSuspectBlocks` cache so that suspicious embodiments can be prioritized without endlessly rescanning the same block in a tight loop.

The ordinary block iterator remains separately responsible for broad periodic coverage.

Thus:

> **suspect-triggered priority ≠ ordinary periodic scan cadence.**

### H/P — scan position is itself saved maintenance state

`VolumeScanner` periodically calls `saveBlockIterator`. Its scheduling code explicitly explains why the iterator records **wall-clock** time in a `cursor file`: monotonic time commonly resets on machine reboot, while the persisted cursor must survive that boundary. The iterator is also saved at the end of a block-pool pass and at configured intervals during a pass.

The exact durability/atomicity guarantees of the cursor implementation are outside this case, but the design intent is direct: scanner progress is not merely ephemeral loop-local state.

This yields a retention relation unusual enough to deserve its own name in the project:

> **maintenance progress can itself be retained so that maintenance coverage survives process/machine interruption.**

The cursor is not payload and does not make an unchecked block trustworthy. It preserves where the maintenance process was in its coverage traversal.

---

## Verification is not repair

The DataNode scanner reads and checks a local replica. On a qualifying failure it reports the bad block.

That sequence is not itself the creation of a replacement replica:

```text
local replica remains present
        │
        ▼
periodic or suspect-triggered scan
        │
        ▼
checksum / read verification
        │
   ┌────┴────┐
   │         │
 success   qualifying failure
   │         │
   │         ▼
   │   reportBadBlocks
   │         │
   │         ▼
   │   distributed control learns
   │   this embodiment is corrupt
   │         │
   │         ▼
   │   later re-replication can use
   │   another good replica
   ▼
current embodiment remains qualified
```

The HDFS architecture documentation separately assigns replication decisions to the NameNode and names replica corruption as one reason re-replication becomes necessary.

Therefore:

> **checksum verification ≠ payload repair.**

and:

> **corrupt-replica reporting ≠ the scanner itself copying a good replica.**

This distinction matters because detection can succeed while repair cannot—for example if no other good source remains—or repair may occur only after additional scheduling and transfer work.

---

## Read semantics

HDFS has at least two integrity-checking contexts relevant to this bounded comparison.

### Demand-path verification

The architecture documentation describes client-side checksum checking when retrieving file contents. A mismatch can cause the client to obtain the block from another replica.

### Background DataNode verification

The DataNode scanner deliberately reads blocks even when no application currently requests them. Its purpose is to move some integrity discovery **before ordinary demand**.

These paths can share checksum semantics without being the same event:

> **periodic verification ≠ demand read verification.**

Case 83 does not claim that every code path or Hadoop release uses exactly the same checksum implementation internals.

---

## Time and coverage

The case introduces several different temporal relations:

1. **time since a particular replica was last successfully verified**;
2. **time needed to traverse one volume / block pool under the rate limit**;
3. **configured interval before the next broad rescan**;
4. **delay before a newly suspect block is prioritized**;
5. **time between physical corruption and discovery**;
6. **time between discovery/reporting and restoration of desired replication**;
7. **lifetime of the saved scanner cursor across restart**.

`verification age` is a project comparison term for (1); the inspected implementation does not expose a durable per-block certificate whose mere existence permanently guarantees future correctness.

A successful scan only establishes a bounded observation at a time:

> **successful verification at t₁ ≠ immutable integrity at t₂.**

The medium, software, metadata, or device can fail later. Periodic rescanning exists precisely because trust must be renewed under an ongoing failure model.

---

## Failure and forgetting modes

Keep these distinct:

- **payload corruption** — local data bytes no longer match the expected integrity relation;
- **checksum/metadata corruption** — integrity evidence itself can become unusable or inconsistent;
- **replica missing from the local dataset** — absence is not the same diagnosis as checksum corruption;
- **transient/racy lookup failure** — the 2.7.3 handler explicitly avoids turning every `FileNotFoundException` into a corrupt-replica report;
- **scanner disabled or starved** — surviving replicas can go longer without proactive verification;
- **coverage/progress state loss** — may cause inefficient/repeated coverage or enlarge the interval before some blocks are revisited, depending on implementation recovery;
- **corruption discovered but not reportable** — `reportBadBlocks` itself can fail;
- **bad replica reported but no good source exists** — detection succeeds while repair opportunity is already gone;
- **desired redundancy not yet restored** — NameNode may know an embodiment is bad while the system still has reduced failure margin;
- **physical deletion of the corrupt local file** — a later cleanup action, not synonymous with the integrity verdict;
- **secure sanitization** — not established by reporting, invalidation, replication, or local file removal.

Calling all of these `bit rot` would hide the operative distinctions among defect creation, discovery, qualification, reporting, repair, and physical forgetting.

---

## Cross-case comparison

### Case 79 — HDFS Startup SafeMode

Case 79 asks whether the restarted NameNode has **re-observed enough replica locations** to resume ordinary work. Case 83 asks whether a positively present local replica still passes an integrity check.

Therefore:

> **inventory re-observation ≠ integrity qualification.**

A Blockreport can re-establish `block B is present on DataNode D` without proving that a later full read of that replica will verify successfully.

### Case 18 — ZFS scrub

Both cases expose proactive verification as retention work: a block can remain physically present while a latent defect stays undiscovered until maintenance reads it.

The comparison is functional, not genealogical.

- ZFS Case 18 is pool/filesystem-level scrubbing with checksum-qualified redundant copies and conditional self-healing semantics.
- HDFS Case 83 is a DataNode-local periodic/suspect scanner that reports bad replicas into a distributed replication-control system.

Thus:

> **proactive integrity verification is a shared function, not evidence that HDFS `BlockScanner` and ZFS `zpool scrub` are the same mechanism or one descended from the other.**

### Case 05 / distributed repair cases

RADOS and other distributed cases emphasize replica agreement, placement, and repair after failure or divergence. Case 83 supplies an upstream epistemic step: before repair policy can act on latent local corruption, some operation must discover that one embodiment is no longer trustworthy.

> **repair capacity ≠ corruption discovery.**

### Case 77 — DRAM corrective sniffing

Data General's bounded DRAM design can use ECC to correct and write back a damaged codeword. HDFS background scanning, by contrast, can report a bad replica and rely on another distributed embodiment for later replacement.

Both are integrity-maintenance cases, but the repair substrate, authority, scale, and chronology differ.

---

## Prior-art boundary

This case makes **no invention-priority claim** for:

- checksums;
- background media scanning;
- disk scrubbing;
- replicated repair;
- HDFS-style DataNode scanning as the first distributed implementation of such ideas.

Two boundaries are especially important.

First, the Hadoop 2008 issue history proves the mechanism existed before the bounded 2.7.3 rewrite; therefore the case uses 2.7.3 for inspectable semantics, not as an origin date.

Second, Ghemawat, Gobioff, and Leung's 2003 Google File System paper already describes chunkservers checking checksums on reads and, during idle periods, scanning inactive chunks so corruption in rarely read data can be detected; after detection the master can create an uncorrupted replica and retire the corrupt one. That is direct prior art for the broad distributed-storage function `proactive local integrity verification + replica replacement` before HDFS's 2008 `DataBlockScanner` witness.

The defensible historical claim is narrower:

> **By 2008 HDFS had a DataNode `DataBlockScanner` used to verify local blocks, and the Hadoop 2.7.3 implementation gives an inspectable later regime in which per-volume scanners rate-limit periodic coverage, prioritize suspect blocks, persist iterator/cursor progress, distinguish some transient races from bad-block verdicts, and report qualifying failures into the distributed replica-management path.**

A full GFS→Nutch/HDFS scanner genealogy would require dedicated historical work and belongs primarily in `computing-archaeology` if pursued.

---

## Engineering reconstruction

Case 83 adds these controlled relations:

1. `replica presence ≠ integrity qualification`;
2. `Blockreport ≠ checksum verification`;
3. `periodic verification ≠ demand read verification`;
4. `checksum verification ≠ payload repair`;
5. `corrupt-replica report ≠ physical deletion`;
6. `repair from another replica ≠ scanner-local rewrite`;
7. `scanner exception ≠ unconditional corruption verdict`;
8. `suspect priority ≠ ordinary periodic cadence`;
9. `scan progress/cursor state ≠ user payload`;
10. `retained scan progress ≠ retained complete verification history`;
11. `successful verification now ≠ permanent future validity`;
12. `inventory re-observation ≠ integrity qualification`;
13. `proactive verification ≠ historical identity with ZFS scrub`;
14. `distributed repair capacity ≠ corruption discovery`.

These are project engineering terms. They are not claims that Apache developers used this exact ontology.

---

## Philosophical interpretation — bounded

Case 83 sharpens a recurring project problem: **persistence includes epistemic maintenance as well as material maintenance**.

The block can remain exactly where the system thinks it is and still cease to deserve the status `good replica`. A background scan does not normally preserve the block by rewriting it in place; its first contribution is to renew or withdraw a relation of trust between a surviving embodiment and the logical object it is supposed to realize.

This supports a bounded interpretation:

> **Some retention work preserves not the payload directly but the system's justified ability to count a surviving embodiment as admissible.**

The interpretation stops there. It does not imply that all truth, memory, or archives are checksum relations, nor that `trust` is Apache's historical term for checksum success.

---

## Evidence limits / future work

Still open:

- exact source archaeology of the earliest HDFS `DataBlockScanner` implementation and its Nutch/HDFS transition;
- a full GFS→HDFS or other distributed-scrubbing genealogy;
- exact checksum-file / metadata-format evolution across Hadoop releases;
- fault-injection measurements on named HDFS releases;
- later `BlockScanner` / `VolumeScanner` changes after 2.7.3;
- interaction with storage-device internal ECC, RAID, filesystems, and controller scrubbing;
- quantified detection-latency distributions in production clusters;
- exact durability/atomicity guarantees of the saved block-iterator cursor;
- cases where all replicas share correlated corruption;
- Byzantine/adversarial integrity, which checksum scanning does not solve.

These limits do not block the bounded result.

---

## Related repositories

### `tmzncty/computing-archaeology`

Repository search found no dedicated HDFS BlockScanner / checksum-scanning case at the time of this slice. This case therefore keeps only the retention-specific mechanism and prior-art boundary. If a full history of HDFS data-integrity scanning or GFS→HDFS genealogy is built later, it should live there and be linked back rather than duplicated here.

### `tmzncty/problem-history`

Useful methodological guardrail: `integrity qualification`, `verification age`, and `maintenance-progress retention` are our reconstruction terms. The historical actors' vocabulary remains `DataBlockScanner` / `BlockScanner`, `VolumeScanner`, checksum verification, suspect blocks, bad-block reporting, and re-replication.

---

## Sources

### Primary / contemporary

- Apache Hadoop 2.7.3, **HDFS Architecture**, especially `Data Replication`, `Data Disk Failure, Heartbeats and Re-Replication`, and `Data Integrity`: <https://hadoop.apache.org/docs/r2.7.3/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html>
- Apache Hadoop source, tag `rel/release-2.7.3`, `BlockScanner.java`: <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/BlockScanner.java>
- Apache Hadoop source, tag `rel/release-2.7.3`, `VolumeScanner.java`: <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/VolumeScanner.java>
- Apache JIRA, `HADOOP-3635`, **Uncaught exception in DataBlockScanner**, affects 0.17.0 / fixed 0.18.0 (2008): <https://issues.apache.org/jira/browse/HADOOP-3635>
- Apache JIRA, `HDFS-3194`, **DataNode block scanner is running too frequently** (2012): <https://issues.apache.org/jira/browse/HDFS-3194>
- Apache JIRA, `HDFS-7548`, **Corrupt block reporting delayed until datablock scanner thread detects it** (2014–2015): <https://issues.apache.org/jira/browse/HDFS-7548>
- Sanjay Ghemawat, Howard Gobioff, Shun-Tak Leung, **“The Google File System,”** SOSP 2003, especially §5.2 `Data Integrity`: <https://research.google/pubs/the-google-file-system/>

### Internal comparisons

- [`cases/18-zfs-scrub-latent-error-detection.md`](18-zfs-scrub-latent-error-detection.md)
- [`cases/05-rados-replicated-object-repair.md`](05-rados-replicated-object-repair.md)
- [`cases/77-data-general-dram-sniff-refresh-ecc-scrub.md`](77-data-general-dram-sniff-refresh-ecc-scrub.md)
- [`cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md`](79-apache-hdfs-startup-safemode-block-report-reobservation.md)

---

## Status

**Grounded bounded case.**

The central claims are directly supported by Apache documentation, tag-matched Hadoop 2.7.3 source, and earlier Apache issue history; GFS 2003 supplies a conservative prior-art boundary. The case does not generalize from HDFS to all scrubbing systems and does not equate detection, reporting, repair, deletion, or sanitization.