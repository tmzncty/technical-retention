# Case 83 grounding — HDFS DataNode block scanning, checksum verification, and retained scan progress (2003–2016)

## Purpose

Ground the bounded Case 83 claim that HDFS can know a replica is present while still requiring later integrity verification before that embodiment continues to count as a trustworthy replica, and that the background verification process itself retains scheduling/progress state.

This record separates:

- **historical record** — what Apache / GFS sources actually say or implement;
- **engineering reconstruction** — the retention relations inferred from those mechanisms;
- **functional analogy** — comparisons to ZFS and other cases;
- **philosophical interpretation** — what the mechanism contributes to the project's retention vocabulary.

It does **not** establish invention priority for checksums, scrubbing, replicated repair, or HDFS background scanning.

---

## Source set and evidence grade

| Source | Date / version | Type | Use here | Grade |
| --- | --- | --- | --- | --- |
| Ghemawat, Gobioff, Leung, *The Google File System*, SOSP | 2003 | original systems paper | prior-art boundary for checksum verification on reads plus idle scanning of inactive chunks and replica replacement | **P** |
| Apache JIRA HADOOP-3635, `Uncaught exception in DataBlockScanner` | 2008; affects 0.17.0, fixed 0.18.0 | project issue / contemporary operational witness | proves an HDFS `DataBlockScanner` was already responsible for verifying local blocks by 2008 | **H/P** |
| Apache JIRA HDFS-3194, `DataNode block scanner is running too frequently` | 2012 | project issue | historical 21-day / three-week scan-period expectation | **H/P** |
| Apache JIRA HDFS-7548, `Corrupt block reporting delayed until datablock scanner thread detects it` | 2014–2015 | project issue | confirms scanner-mediated corruption discovery/reporting remained operationally consequential | **H/P** |
| Apache JIRA HDFS-7430, `Rewrite the BlockScanner to use O(1) memory and use multiple threads` | 2014–2015 | project design / implementation issue | grounds compact last-scanned-position design and per-volume rewrite | **H/P** |
| Apache JIRA HDFS-12209, `VolumeScanner scan cursor not save periodic` | later project bug, linked from HDFS-7430 | project defect witness | corrects the assumption that the configured in-pass cursor-save interval was effective | **H/P** |
| Apache Hadoop 2.7.3 HDFS Architecture | 2016 release docs | official system documentation | Blockreport presence, checksums, corruption, alternate replicas, re-replication | **H/P** |
| Hadoop `rel/release-2.7.3`, `BlockScanner.java` | 2.7.3 | tag-matched source | scan-period semantics, rate enablement, suspect-block scheduling | **H/P** |
| Hadoop `rel/release-2.7.3`, `VolumeScanner.java` | 2.7.3 | tag-matched source | per-volume threads, verification path, race handling, bad-block reporting, cursor persistence, coverage scheduling | **H/P** |
| Apache JIRA HDFS-11160 + Hadoop commit `aebb9127...` | 2016 | project issue + matching source commit | concurrent append can mix new checksum with old data; fix captures last partial checksum under dataset lock | **H/P** |
| Apache JIRA HDFS-12136 | 2017 | project follow-up | lock-based HDFS-11160 fix had a documented BlockSender contention/performance cost | **H/P** |
| `technical-retention` Case 18 | current repo | grounded internal case | bounded functional comparison to ZFS proactive scrub | **A** |
| `technical-retention` Case 79 | current repo | grounded internal case | distinguish Blockreport inventory re-observation from integrity qualification | **E/A** |

`P` here means primary/contemporary evidence under repository conventions; it does not imply every source is a peer-reviewed paper.

---

## Source anchors

### A. Apache Hadoop 2.7.3 HDFS Architecture

URL:
<https://hadoop.apache.org/docs/r2.7.3/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html>

Relevant headings:

- `Data Replication`;
- `Data Disk Failure, Heartbeats and Re-Replication`;
- `Data Integrity`.

Grounded observations:

1. A DataNode periodically sends Heartbeats and Blockreports.
2. A Blockreport contains a list of blocks on the DataNode.
3. Replica corruption is one reason re-replication may become necessary.
4. HDFS checks retrieved file contents against checksum information.
5. On mismatch another replica can be used.

Evidence consequence:

> The official architecture separates **inventory evidence** (`this DataNode reports block B`) from **integrity evidence** (`the bytes accepted for B satisfy the checksum relation`).

Do not strengthen this into `Blockreport proves nothing`: a Blockreport is useful positive location/inventory evidence. The bounded claim is only that it is not a full content-integrity qualification.

---

### B. Hadoop `rel/release-2.7.3` — `BlockScanner.java`

URL:
<https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/BlockScanner.java>

Relevant implementation anchors:

#### Scanner configuration

The source imports:

- `DFS_DATANODE_SCAN_PERIOD_HOURS_KEY`;
- `DFS_DATANODE_SCAN_PERIOD_HOURS_DEFAULT`;
- `DFS_BLOCK_SCANNER_VOLUME_BYTES_PER_SECOND`;
- `DFS_BLOCK_SCANNER_VOLUME_BYTES_PER_SECOND_DEFAULT`.

`getConfiguredScanPeriodMs` documents two boundary cases:

- zero is converted to the historical three-week default for compatibility;
- a negative value disables the scanner.

`isEnabled()` requires both a positive scan period and a positive target byte rate.

Supported claim:

> Background verification is policy- and resource-bounded work, not continuous omniscience over every stored block.

#### Suspect-block path

`markSuspectBlock` says a suspect block should be rescanned soon and notes that `VolumeScanner` avoids rescanning the same suspicious block repeatedly in a short interval.

Supported claim:

> HDFS 2.7.3 composes broad scheduled coverage with an event/suspicion-driven priority path.

Unsupported strengthening:

> Every corruption is immediately marked suspect.

The source only grounds what happens **after** this method is called.

---

### C. Hadoop `rel/release-2.7.3` — `VolumeScanner.java`

URL:
<https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/VolumeScanner.java>

This is the strongest source for Case 83.

#### Per-volume scanner and bounded progress state

The class comment states that one `VolumeScanner` scans a single volume and that the DataNode's `BlockScanner` manages these scanner threads.

Its state includes:

- block iterators by block pool;
- `suspectBlocks`;
- a cache of recently scanned suspect blocks;
- a current iterator;
- per-hour scanned-byte accounting;
- statistics including blocks scanned, scan errors, last block, and end-of-pass state.

Supported claim:

> The maintenance process has explicit state apart from the payload it verifies.

#### Verification path

`scanBlock` resolves the currently stored block/genstamp, builds a `BlockSender` with checksum verification enabled, throttles the read, streams it to a null output, and passes success/failure to the result handler.

Supported claim:

> The background operation can exercise the read/check path without an application consuming the returned payload.

This is not evidence that scanner traffic is literally identical to every client read path or to every historical Hadoop release.

#### Failure classification and bad-block reporting

`ScanResultHandler.handle`:

- returns normally after successful verification;
- ignores an error if the block is no longer in the dataset;
- treats `FileNotFoundException` specially because it can be a race with a write / replica transition;
- for other failures on a still-present block, logs `Reporting bad` and calls `datanode.reportBadBlocks(block)`.

Supported claims:

- `verification failure ≠ unconditional corruption verdict`;
- concurrency state can matter to interpretation of a failed read;
- a qualifying local failure becomes distributed control information through bad-block reporting.

Do **not** infer from this method alone the complete NameNode state transition or exact later physical deletion timing.

#### Retained iterator / cursor

The scanner calls `iter.save()` through `saveBlockIterator`. `findNextUsableBlockIter` explicitly explains that the persisted cursor uses wall-clock time because monotonic time commonly resets when the machine reboots.

The source-level mechanism is now deepened in [`83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md`](83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md): `FsVolumeImpl` serializes directory/subdirectory/entry/EOF position plus wall-clock save/start timestamps to a temporary file and requests `ATOMIC_MOVE` to the live `.cursor`; `VolumeScanner` falls back to a fresh iterator if loading fails.

However, the earlier phrase `saved periodically` is too strong for effective 2.7.3 behavior. The in-pass interval branch subtracts the wall-clock `lastSavedMs` from `Time.monotonicNow()`, and Apache HDFS-12209 is explicitly titled `VolumeScanner scan cursor not save periodic`. EOF and orderly-exit saves are separate code paths and remain grounded.

Supported claims:

> The implementation has an explicit restart-persistent scanner traversal checkpoint mechanism.

> Configured periodic-save intent does not establish effective periodic checkpoint cadence.

> Missing/unreadable checkpoint state can fall back to replay from a fresh iterator.

Evidence limits:

- requested `ATOMIC_MOVE` does not by itself establish file/directory durability under sudden power loss;
- a cursor position is not a complete per-block success history;
- this slice does not provide filesystem fault injection or downstream-vendor patch genealogy.

The safe reconstruction is `retained maintenance-traversal checkpoint`, not `perfect durable proof of verification history`.

#### Rate limiting and coverage

The loop calculates effective bytes per second and delays further scanning when the target would be exceeded. It chooses usable block iterators, rewinds a completed block-pool iterator only after the configured scan period, and can prioritize a suspect block over the next regularly scheduled block.

Supported claims:

- broad verification has a coverage schedule;
- coverage consumes bounded storage I/O;
- the time between successful checks is an operational variable;
- suspect priority and ordinary periodic traversal are distinct triggers.

---

### D. HADOOP-3635 — 2008 historical witness

URL:
<https://issues.apache.org/jira/browse/HADOOP-3635>

Issue title:
`Uncaught exception in DataBlockScanner`

Issue metadata:

- affects `0.17.0`;
- fixed in `0.18.0`;
- description reports DataNodes that stopped **verifying local blocks** when the scanner thread failed.

Supported historical boundary:

> An HDFS `DataBlockScanner` whose operational purpose included local-block verification existed no later than the Hadoop 0.17/0.18 period in 2008.

Do not use this issue to project the 2.7.3 `VolumeScanner` class structure backward into 2008.

---

### E. HDFS-3194 — 2012 scan-period witness

URL:
<https://issues.apache.org/jira/browse/HDFS-3194>

The issue says the default block-scanning interval should be 21 days / three weeks and each block should be scanned once in that interval; the reported bug was continuous rescanning.

Supported claim:

> By 2012 the HDFS scanner had an explicit broad-coverage cadence whose intended default was measured in weeks, not a demand-only checking model.

Boundary:

> `three weeks` is release/configuration history, not a physical law or universal HDFS guarantee.

---

### F. HDFS-7548 — detection/reporting interaction

URL:
<https://issues.apache.org/jira/browse/HDFS-7548>

The issue reports a case where a corrupt block could remain unreported as corrupt until the DataNode block scanner picked it up, while replication attempts failed with checksum errors.

Use:

- corroborates that corruption discovery/reporting and replication are separate control paths;
- demonstrates why detection latency can matter operationally.

Do not generalize the bug into normal behavior of all HDFS versions; it was filed precisely because the interaction was undesirable and was fixed.

---

### G. GFS 2003 prior-art boundary

Citation:

Sanjay Ghemawat, Howard Gobioff, and Shun-Tak Leung, **“The Google File System,”** *Proceedings of the 19th ACM Symposium on Operating Systems Principles*, 2003, §5.2 `Data Integrity`.

Publication page:
<https://research.google/pubs/the-google-file-system/>

Relevant historical record:

- chunkservers maintain checksums for their own chunk copies;
- reads verify the affected checksum blocks before data is returned;
- a checksum mismatch is reported and another replica can serve as the recovery source;
- during idle periods, chunkservers can scan inactive chunks to detect corruption in rarely read data;
- after detection the master can create a new uncorrupted replica and retire the corrupt embodiment.

Prior-art consequence:

> The broad function `proactive checksum scan of dormant distributed-storage replicas + replacement from another replica` is documented in GFS in 2003, before the 2008 HDFS `DataBlockScanner` witness used here.

This does **not** establish direct code lineage or prove that HDFS copied a particular implementation. Genealogy remains open.

---

## 2016 addendum — verification evidence must be coherent with the payload state

Detailed record: [`83-hdfs-2016-volume-scanner-concurrent-append-coherence-deepening.md`](83-hdfs-2016-volume-scanner-concurrent-append-coherence-deepening.md).

HDFS-11160 records a concrete counterexample to the shortcut `checksum mismatch = corrupt bytes`: during concurrent append, `VolumeScanner` could compare a new checksum against old data and report a good replica as corrupt. Apache's matching commit captures the finalized replica's last partial checksum while holding the dataset lock and adds a concurrent append/scan regression test.

This later evidence deepens, rather than contradicts, the 2.7.3 `ScanResultHandler` boundary above. The earlier handler already recognized that some race-related failures should not automatically become bad-block reports; HDFS-11160 shows another race that escaped that classification logic because the read/check path itself could construct an incoherent checksum/data observation.

The safe engineering relations are:

- `checksum mismatch != necessarily physical payload corruption`;
- `checksum algorithm correctness != observation coherence`;
- `integrity metadata presence != currentness for the judged payload version`;
- `corrupt-replica report != ground truth`;
- `verification-coherence fix != payload repair`.

HDFS-12136 is retained as a separate 2017 cost boundary: the issue attributes severe serialization under some load to the HDFS-11160 lock/read strategy. It does not prove that every coherent verifier requires that locking design.

---

## Cursor checkpoint addendum — retained maintenance state can have a defective retention cadence

Detailed record: [`83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md`](83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md).

HDFS-7430 makes the O(1) design goal explicit: retain last-scanned traversal position instead of per-block scan status. The 2.7.3 source serializes that compact cursor and requests a temp-file-to-live-file atomic move. But the periodic checkpoint condition mixes monotonic and wall-clock time domains, and HDFS-12209 records the resulting failure to save the cursor periodically.

The safe engineering relations are:

- `cursor position != per-block verification history`;
- `configured cursor-save interval != effective periodic checkpoint cadence`;
- `ATOMIC_MOVE request != demonstrated power-loss durability`;
- `cursor load failure != scanner disablement`;
- `checkpoint replay != payload rollback`;
- `restart continuity != exactly-once scan execution`.

This narrows an earlier Case 83 overstatement without changing the broader conclusion that scan progress is a real retained control-state class.

---

## Claim ledger

| Claim | Label | Evidence | Boundary |
| --- | --- | --- | --- |
| HDFS had a DataNode background block verifier by 2008 | H/P | HADOOP-3635 | no first-invention claim; no projection of 2.7.3 class structure backward |
| HDFS Blockreport records block presence/inventory, not full content qualification | H/P + E | HDFS 2.7.3 Architecture | Blockreport remains useful positive inventory evidence |
| 2.7.3 background scanner has configurable periodic and bandwidth limits | H/P | `BlockScanner.java`, `VolumeScanner.java` | exact defaults/configuration are version-specific |
| suspect blocks can be prioritized | H/P | `BlockScanner.markSuspectBlock`, `VolumeScanner` queue/cache | source does not prove every error triggers suspicion immediately |
| scanner verifies by exercising a checksummed block-read path | H/P | `VolumeScanner.scanBlock` | not a claim that every Hadoop read path is identical |
| qualifying scan failures are reported as bad blocks | H/P | `ScanResultHandler` | exact downstream NameNode transition is outside this method |
| some transient/racy failures are intentionally not reported as corruption | H/P | `ScanResultHandler` FileNotFound handling | specific to inspected implementation/path |
| scanner traversal/cursor state has explicit save/load paths | H/P | `FsVolumeImpl.BlockIteratorImpl`, `VolumeScanner` | EOF/orderly-exit saves are grounded; in-pass periodic save is affected by the HDFS-12209 clock-domain defect |
| scan-progress state is retention infrastructure rather than payload | E | source structure | project terminology |
| successful verification has temporal scope, not permanent validity | E | recurring scan regime + failure model | not an Apache historical phrase |
| verification and repair are separate | H/P + E | local scanner vs architecture re-replication responsibility | later repair details outside bounded scanner |
| corrupt-replica reporting is not physical sanitization | E/X | reporting semantics | no secure-erasure claim supported |
| GFS had the broad proactive distributed integrity-scan function by 2003 | H/P | GFS §5.2 | no direct HDFS genealogy claim |
| HDFS scanner and ZFS scrub are functionally comparable but historically distinct | A | Case 18 + HDFS evidence | analogy only |
| concurrent append can make checksum/data observations incoherent | H/P | HDFS-11160 | bounded to documented race; not every mismatch |
| the 2016 fix captures last partial checksum under dataset lock | H/P | commit `aebb9127...` | does not establish global snapshot atomicity |
| checksum mismatch can be a false corruption verdict | H/P + E | HDFS-11160, HDFS-6804 | does not deny genuine corruption mismatches |
| coherence correction can have service cost | H/P + E | HDFS-12136 | product/code-path witness, not universal law |
| HDFS-7430 intentionally replaces per-block scan-status memory with last-scanned traversal position | H/P | HDFS-7430 | rewrite witness, not checkpoint invention priority |
| 2.7.3 cursor save uses temp serialization plus requested `ATOMIC_MOVE` | H/P | `FsVolumeImpl.java` | does not establish sudden-power-loss durability |
| missing/unreadable cursor load falls back to a fresh iterator | H/P | `VolumeScanner.enableBlockPoolId` | replay can still consume bounded scan budget |
| 2.7.3 periodic cursor-save check mixes monotonic and wall-clock timestamps | H/P | `VolumeScanner.java` + `FsVolumeImpl.java` | exact elapsed-time comparison is invalid across those domains |
| Apache records a bug titled `VolumeScanner scan cursor not save periodic` | H/P | HDFS-12209 | supports defect boundary, not every downstream deployment |
| cursor progress is not a successful-verification ledger | E | iterator advance + separate scan-error path | project reconstruction |

---

## Engineering reconstruction

The evidence supports these project-level distinctions:

1. `replica presence ≠ integrity qualification`;
2. `Blockreport ≠ checksum verification`;
3. `periodic verification ≠ demand read verification`;
4. `checksum verification ≠ payload repair`;
5. `corrupt-replica report ≠ physical deletion`;
6. `repair from another replica ≠ scanner-local rewrite`;
7. `scanner exception ≠ unconditional corruption verdict`;
8. `suspect priority ≠ ordinary periodic cadence`;
9. `scan progress/cursor state ≠ user payload`;
10. `retained scanner cursor ≠ complete verification history`;
11. `successful verification at one time ≠ permanent future integrity`;
12. `inventory re-observation ≠ content-integrity qualification`;
13. `repair capacity ≠ corruption discovery`;
14. `background verification ≠ historical identity with ZFS scrub`;
15. `corruption deauthorization ≠ secure sanitization`;
16. `checksum mismatch ≠ necessarily physical payload corruption`;
17. `checksum algorithm correctness ≠ checksum/data observation coherence`;
18. `integrity metadata presence ≠ currentness for the judged payload state`;
19. `corrupt-replica report ≠ ground truth about media damage`;
20. `verification-coherence fix ≠ payload repair`;
21. `coherent verification ≠ free verification`;
22. `cursor position ≠ per-block verification history`;
23. `configured checkpoint interval ≠ effective checkpoint cadence`;
24. `ATOMIC_MOVE request ≠ demonstrated power-loss durability`;
25. `cursor load failure ≠ scanner disablement`;
26. `checkpoint replay ≠ payload rollback`;
27. `restart continuity ≠ exactly-once scan traversal`.

The strongest contribution to the repository's maintenance taxonomy is #9–11: **the mechanism that verifies retained data has its own state, schedule, and temporal continuity.**

---

## Cross-case boundary

### Case 79 — startup SafeMode / Blockreport

Case 79: `is a replica currently reported/present?`

Case 83: `does a present local replica still pass the integrity path when checked?`

The second question does not make the first redundant, and the first does not answer the second.

### Case 18 — ZFS scrub

Shared function:

- proactive reading/checking before ordinary demand;
- latent-defect discovery while another repair source may still exist.

Different mechanism:

- ZFS scrub is a pool/filesystem traversal with ZFS checksum/self-healing semantics;
- HDFS scanner is per-DataNode/per-volume local verification feeding bad-replica information into distributed replication control.

No genealogy claim.

### Case 77 — DRAM sniff / corrective writeback

Case 77 can correct a codeword and write it back within the memory system. Case 83 can instead disqualify/report an entire distributed replica and depend on a different replica for restoration. `integrity renewal` therefore has different embodiment and authority structures across the two cases.

---

## Related-repository check

Searches of `tmzncty/computing-archaeology` for `HDFS`, `HDFS block scanner checksum`, and the specific scanner mechanism returned no dedicated case at the time of the original slice. Fresh checks during the HDFS-11160 deepening and this cursor-checkpoint deepening likewise found no dedicated `HDFS-11160`, `HDFS-7430`, `HDFS-12209`, `VolumeScanner`, or `BlockScanner` case to reuse.

Therefore this record does **not** duplicate an existing companion-repository history. It intentionally leaves the following to future `computing-archaeology` work if pursued:

- Nutch/HDFS origin chronology;
- GFS→HDFS influence/genealogy;
- scanner rewrite history across 0.x, 1.x, 2.x, and 3.x;
- storage-stack implementation constraints outside the retention question.

---

## Rejected / unsupported claims

Do **not** claim:

- HDFS invented background storage scrubbing;
- the 2.7.3 BlockScanner was the first HDFS scanner;
- a Blockreport proves content integrity;
- every scanner exception proves corruption;
- every successfully reported block is currently checksum-clean;
- the scanner itself repairs a corrupt replica;
- a bad-replica report immediately erases local media;
- physical deletion is secure sanitization;
- saved scan progress is a complete durable history of every verification event;
- the configured ten-minute cursor-save interval proves the 2.7.3 implementation checkpointed effectively every ten minutes;
- requested `ATOMIC_MOVE` alone proves power-loss durability of the cursor;
- the configured scan period guarantees a strict per-block upper bound under every workload/failure/configuration;
- HDFS BlockScanner and ZFS scrub are the same historical mechanism;
- GFS 2003 proves a direct code or organizational genealogy into HDFS.

---

## Promotion judgment

**Status: `grounded`.**

Reason:

- mechanism-level behavior is anchored in tag-matched Apache source;
- the official HDFS architecture supplies the inventory/integrity/re-replication boundary;
- 2008 and 2012 Apache issue history gives earlier scanner/cadence witnesses;
- GFS 2003 prevents an invention-priority overclaim;
- related-repository duplication was checked;
- uncertainty about exact scanner genealogy, filesystem/power-loss cursor durability, HDFS-12209 release/downstream handling, and later product behavior is explicitly retained rather than hidden.
