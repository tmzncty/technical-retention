# Apache ZooKeeper Fuzzy Snapshots: Non-Point-in-Time Materialization, Ordered Replay, and Recovery-Set Retention

## Status

**`grounded`** — bounded to the fuzzy-snapshot / transaction-log recovery relation documented by Apache ZooKeeper's 2009–2019 administrator documentation, the 2010 USENIX ATC ZooKeeper paper, and exact-release source inspection of ZooKeeper 3.4.14.

Evidence navigation:

- grounding record: [`../evidence/71-zookeeper-2006-2019-fuzzy-snapshot-grounding.md`](../evidence/71-zookeeper-2006-2019-fuzzy-snapshot-grounding.md)
- 3.4.14 source deepening: [`../evidence/71-zookeeper-3414-snapshot-admission-replay-source-deepening.md`](../evidence/71-zookeeper-3414-snapshot-admission-replay-source-deepening.md)

The new source deepening does **not** change maturity. It closes the bounded implementation debt around snapshot creation/admission/replay without turning one release's source into a universal ZooKeeper history.

## Scope

This case asks one narrow distributed-retention question:

> **Can a durable snapshot remain a valid recovery representation even when it does not correspond to any single historical state that ever existed, and what log history plus admission evidence must remain so that recovery still converges to the authoritative end-of-log state?**

The bounded mechanism is:

```text
committed ZooKeeper update
    -> transaction written to non-volatile log
    -> update applied to in-memory data tree

periodic snapshot begins at zxid S
    -> no global lock freezes the whole tree
    -> depth-first snapshot reads znodes while later updates continue
    -> snapshot may embody only a subset of updates after S
    -> resulting file may describe no state that ever existed at one instant

3.4.14 snapshot materialization
    -> final snapshot.<S> pathname is chosen before serialization finishes
    -> payload + checksum + trailing completion marker are written
    -> restart filters structurally incomplete candidates
    -> full deserialize/checksum admits or rejects remaining candidates
    -> a newer rejected candidate can yield to an older retained snapshot

recovery
    -> load a checksum-admissible fuzzy snapshot
    -> derive replay boundary from selected snapshot filename
    -> retain/find log coverage from that boundary
    -> replay idempotent transactions in order
    -> duplicate application of some already-embodied changes is tolerated
    -> reconstructed tree reaches the state at the end of the retained log
```

This is **not** a general ZooKeeper, Zab, consensus, checkpointing, write-ahead-logging, or distributed-coordination history. It also does not claim that ZooKeeper invented snapshots, WAL, fuzzy checkpoints, idempotent replay, completion markers, checksums, or state-machine recovery. The 2010 paper explicitly compares its replay-log-plus-snapshot approach to Chubby, and Chubby's 2006 paper in turn describes a write-ahead-log-and-snapshot database related to still earlier work.

The retention-specific claim is narrower:

> **ZooKeeper supplies a particularly explicit production-oriented case in which a retained recovery image need not be a faithful picture of one historical instant. Recoverability instead depends on a relation among fuzzy snapshot bytes, evidence that those bytes are admissible, a replay boundary, ordered idempotent transactions, and enough retained log files to close the gap to the end of the log.**

`recovery-set retention`, `representation closure`, `snapshot admission`, and `historical-instant fidelity` below are project engineering terms, not ZooKeeper vocabulary.

## Historical vocabulary

The sources directly use `replicated database`, `in-memory database`, `replay log`, `write-ahead log`, `committed operations`, `snapshot`, `fuzzy snapshot`, `transaction`, `idempotent`, `zxid`, `transaction log`, `non-volatile storage`, `PurgeTxnLog`, and `autopurge.snapRetainCount`.

The 3.4.14 source additionally exposes concrete implementation terms such as `snapshot.<zxid>`, `lastProcessedZxid`, `isValidSnapshot`, `Adler32`, and the trailing `/` marker.

Do not silently normalize these into Raft `lastIncludedIndex/Term`, GFS checkpoint positions, database LSNs, Kafka high watermarks, HDFS epochs, or a generic `snapshot ID`.

## Historical record

### H/P — current serving state is in memory while recovery state is separately logged

The 2010 USENIX ATC paper states that the replicated ZooKeeper database is an in-memory data tree. For recoverability, updates are logged to disk, and writes are forced to disk media before they are applied to the in-memory database. The same section calls the retained history a replay log / write-ahead log of committed operations and says ZooKeeper periodically snapshots the in-memory database.

This prevents the shortcut:

> `current in-memory tree = one already-complete durable image`.

**Primary anchor:** Hunt et al. 2010, §4 and pp. 7–8.

### H/P — ZooKeeper transactions are designed to tolerate replay

The paper says that Zab can redeliver messages during recovery and that ZooKeeper transactions are idempotent. Multiple delivery is acceptable **as long as transactions are delivered in order**. ZooKeeper therefore requires redelivery of at least the messages delivered after the start of the last snapshot.

**Primary anchor:** Hunt et al. 2010, §§4.1–4.3.

### H/P — a fuzzy snapshot may correspond to no actual historical tree state

Section 4.3 says ZooKeeper does not lock the whole state while snapshotting. It performs a depth-first scan, atomically reading each znode's data and metadata while normal updates continue. The resulting snapshot may include only a subset of changes that occurred while the scan was in progress and may therefore correspond to **no ZooKeeper state that existed at any one point in time**.

The paper gives a concrete `/foo` and `/goo` example in which the snapshot contains a combination of versions that was never simultaneously the live tree.

**Primary anchor:** Hunt et al. 2010, §4.3.

### H/P — ordered replay converts the fuzzy image into the end-of-log state

The same section explains why the fuzzy image remains usable: because the state-changing transactions are idempotent, replaying them in order can reapply changes already present in part of the fuzzy snapshot without changing the final result. The worked example recovers the pre-crash service state after replay.

This is not a claim that arbitrary duplicate client requests are harmless. The paper distinguishes client requests from the internal idempotent transactions generated for execution.

**Primary anchor:** Hunt et al. 2010, §§4.1 and 4.3.

### H/P — the snapshot filename zxid marks a boundary, not a complete description of every version embodied in the file

Apache's 3.1.2 and 3.4.14 administrator guides say that the snapshot suffix is the zxid of the last committed transaction **at the start of the snapshot**. They also say the resulting file can contain a subset of updates that happened while snapshotting was in progress.

Therefore the suffix must not be read as `maximum transaction represented anywhere inside the file`.

**Primary anchors:** ZooKeeper 3.1.2 and 3.4.14 Administrator's Guide, `Data File Management`.

### H/P — recovery needs a set of files, not merely the newest-looking snapshot filename

The 3.4.14 guide states that the server needs the latest complete fuzzy snapshot, all log files following it, **and the last log file preceding it**. The reason is explicit: snapshotting and log rolling proceed somewhat independently, so the preceding log file can contain transactions newer than the snapshot start.

This is a direct source-level counterexample to naive cleanup by filename order alone.

**Primary anchor:** ZooKeeper 3.4.14 Administrator's Guide, `File Management`.

### H/P — retention policy can deliberately prune old recovery history

The 3.4.14 guide documents `PurgeTxnLog` and says automatic purge was introduced in 3.4.0. `autopurge.snapRetainCount` retains a configured number of recent snapshots and their corresponding transaction logs and deletes older ones; the default and minimum in that release are three.

The maintenance policy therefore distinguishes:

- what is needed for current restart recoverability;
- what older historical recovery sets an operator elects to preserve;
- what files can be intentionally retired.

**Primary anchor:** ZooKeeper 3.4.14 Administrator's Guide, `Ongoing Data Directory Cleanup` and advanced configuration.

### H/P — exact 3.4.14 source writes directly to the final snapshot pathname

Apache's `release-3.4.14` tag resolves to release commit `4c25d480e66aadd371de8bd2fd8da255ac140bcf`.

At that commit, `FileTxnSnapLog.save()` captures `dataTree.lastProcessedZxid`, constructs `snapshot.<zxid>`, and passes that final file to `FileSnap.serialize()`. `FileSnap.serialize()` opens a `FileOutputStream` on that pathname and writes the snapshot body, Adler32 checksum value, and trailing `/` marker before flushing and closing.

There is no temp-snapshot pathname or rename in this bounded method chain. There is also no explicit `FileDescriptor.sync()` / `FileChannel.force()` in `FileSnap.serialize()`.

Therefore the exact 3.4.14 result is:

```text
final pathname existence
    != atomic publication by rename
```

This says nothing universal about later releases or every lower storage layer.

### H/P — exact 3.4.14 source has two snapshot-admission layers

`Util.isValidSnapshot()` explicitly says a snapshot may be invalid because the server died while storing it. It rejects malformed names, files shorter than ten bytes, and files whose final five bytes do not encode the one-byte string `/`.

`FileSnap.findNValidSnapshots()` warns that this is only a lightweight/high-probability validity check. `FileSnap.deserialize()` then performs the stronger step: header parsing plus full Adler32 verification.

Therefore:

```text
snapshot file exists
    != end marker present
    != full deserialize/checksum succeeds
```

### H/P — exact 3.4.14 source can fall back from a newer unusable snapshot

`FileSnap.deserialize()` considers up to 100 recent structurally plausible candidates, newest first. If a candidate raises an `IOException` during deserialize/checksum verification, it logs the problem and tries the next candidate. Only after a candidate succeeds does it set `DataTree.lastProcessedZxid` from the selected snapshot filename.

Thus:

```text
newest snapshot pathname
    != newest admissible recovery snapshot
```

Retaining an older snapshot can preserve a recovery option when a newer artifact is incomplete or corrupt.

### H/P — exact 3.4.14 restore starts replay from the selected snapshot boundary

`FileTxnSnapLog.restore()` calls `snapLog.deserialize(...)` and then `fastForwardFromEdits(...)`. The latter opens transaction-log iteration at:

```text
dt.lastProcessedZxid + 1
```

`processTransaction()` also contains the implementation explanation that snapshots are lazily created, so later transactions can already have made it into the snapshot. During replay, `NONODE` / `NODEEXISTS` conditions caused by those duplicate effects are treated as tolerable in this recovery path.

This is direct source-level confirmation of the fuzzy-snapshot/replay relationship already grounded by the paper and administrator guide.

## Retained state and mechanism

The bounded recovery regime contains several different state classes:

1. **current in-memory data tree** — the serving embodiment;
2. **transaction log** — committed update history used for replay;
3. **fuzzy snapshot payload** — a durable materialization that may mix points from the snapshot interval;
4. **snapshot-start zxid / naming boundary** — a replay locator, not a proof of point-in-time image fidelity;
5. **snapshot completion marker** — in 3.4.14, lightweight structural evidence that serialization reached the end of the bounded format;
6. **snapshot checksum/header validity** — stronger admission evidence checked during full deserialize;
7. **snapshot candidate ordering/fallback** — newest-first recovery selection with older retained candidates still potentially useful;
8. **selected snapshot boundary** — the zxid recovered from the candidate actually admitted;
9. **ordered transaction semantics** — the condition under which duplicate replay remains admissible;
10. **recovery-set file coverage** — enough log files around and after the selected snapshot boundary to reach the desired end state;
11. **purge policy** — an administrative rule that can retire older recovery representations while preserving a configured recent set;
12. **lower-layer persistence behavior** — assumed below the bounded Java implementation and not established merely by file existence, flush, close, or source-level `force()` calls.

The key relation is therefore not:

```text
snapshot = exact old state
```

and not:

```text
snapshot file exists = recoverable snapshot
```

but:

```text
admissible fuzzy materialization
    + selected replay boundary
    + ordered idempotent transactions
    + sufficient retained log coverage
    = recoverable current state
```

## Engineering reconstruction

### E — recovery-equivalent representation ≠ historically existing instantaneous representation

ZooKeeper is a strong counterexample to the assumption that a useful snapshot must itself have been the live state at some instant. The durable image can be internally temporally mixed and still be a valid recovery base because the replay semantics repair that mismatch.

### E — snapshot boundary metadata ≠ maximum embodied update

A snapshot named with start zxid `S` can contain effects of transactions after `S`. The boundary identifies where conservative replay begins; it does not enumerate or cap every update already visible in the snapshot payload.

### E — duplicate replay tolerance ≠ order irrelevance

Idempotence makes reapplying a transaction acceptable, but the paper explicitly retains ordering as a condition. A system that remembers `these operations are individually idempotent` but forgets the required sequence does not inherit ZooKeeper's recovery argument.

### E — fuzzy snapshot validity is relational

A checksum-valid snapshot is not independently sufficient current state. Its adequacy depends on the associated log semantics and retained log coverage. Losing needed replay history can turn physically intact and internally valid snapshot bytes into an insufficient recovery representation.

### E — final pathname existence ≠ snapshot admission

In 3.4.14 the final-named snapshot can exist while serialization is still in progress. Reader-side structural and checksum checks determine whether the artifact is eligible to become a recovery base.

This yields a useful control distinction:

```text
payload embodiment
    != evidence authorizing that embodiment for recovery
```

### E — reader-side fallback ≠ crash-atomic snapshot publication

The inspected 3.4.14 path is not `temp -> fsync -> rename`. It is instead bounded by:

```text
direct final-name write
    + trailing completion marker
    + checksum verification
    + newest-to-older candidate fallback
```

Those mechanisms can tolerate some interrupted/corrupt latest snapshots without making publication an indivisible storage transaction.

### E — retaining older snapshot candidates can preserve recovery-option redundancy

An older candidate can remain useful even when a newer snapshot pathname exists. This is representation-level fallback, not ZooKeeper ensemble replication and not a claim that old snapshots are always needed.

### E — snapshot admission ≠ recovery-set completeness

Passing the completion and checksum tests establishes that the candidate can be deserialized. It does not establish that the transaction logs required to advance from its replay boundary are all still present.

### E — current payload retention can require history retention only up to a moving recovery frontier

ZooKeeper does not need every transaction forever to recover current state. Once newer complete recovery sets exist, older snapshots/logs can be purged according to policy. Current-state retention therefore depends on **bounded** history, not necessarily an indefinite audit log.

### E — file-age ordering ≠ recovery-dependency ordering

The last log file whose starting zxid precedes the snapshot can still contain post-snapshot-start transactions needed for recovery. A file that looks `older` by its starting identifier can therefore remain part of the newer snapshot's recovery closure.

### E — serving-state durability and archival history are different objectives

The 3.4.14 guide permits retention management of old files while the service can continue to retain enough state for restart. Conversely, an operator may keep more old snapshots/logs for troubleshooting or rollback. Those extra files are historical retention beyond the minimum current-serving recovery contract.

### E — transaction-log force path ≠ snapshot-file write path

At the same 3.4.14 release commit, `FileTxnLog.commit()` conditionally calls `FileChannel.force(false)` when `forceSync` is enabled, whereas the inspected `FileSnap.serialize()` path has no corresponding explicit force call.

This is an implementation distinction, **not** a complete proof of power-failure behavior for either artifact. Filesystem, kernel, controller, device-cache, and hardware semantics remain outside this source-only slice.

## Functional analogies and boundaries

### A — ZooKeeper fuzzy snapshot vs Raft stable snapshot (Case 58)

Both substitute materialized state for unbounded replay history and retain a boundary linking the materialized state to later history.

The analogy stops there. Raft Case 58 grounds a snapshot of committed applied state with explicit `last included index/term` and cluster configuration, after which the covered prefix is discarded and lagging followers may receive `InstallSnapshot`. ZooKeeper's bounded fuzzy image may correspond to no actual instantaneous tree state and relies on ordered idempotent replay from the snapshot-start boundary.

Therefore:

> `ZooKeeper fuzzy snapshot ≠ Raft snapshot semantics`.

### A — ZooKeeper vs GFS master checkpoint (Case 46)

Both bound replay with a durable materialization plus later log history. GFS's bounded case treats a complete checkpoint and operation-log suffix, while ZooKeeper explicitly tolerates a non-point-in-time fuzzy scan whose replay can duplicate some already embodied updates.

### A — ZooKeeper vs Bigtable tablet recovery (Case 57)

Both combine a materialized state with replayable history and later maintenance that can make older representations dispensable. Bigtable's memtable/SSTable/redo-point composition is not ZooKeeper's replicated in-memory data tree plus fuzzy snapshot and idempotent transaction replay.

### A — ZooKeeper vs Kafka checkpoint membership (Case 56)

Both show that small recovery-control state can change how surviving payload is interpreted after restart. Kafka Case 56 concerns high-watermark checkpoint membership and follower recovery; ZooKeeper Case 71 concerns snapshot admission and replay-boundary selection. No common implementation or genealogy is claimed.

### A — ZooKeeper vs OpenZFS scrub completion (Case 18)

Both distinguish work/artifact existence from evidence that an operation reached a safe software-visible completion boundary. The analogy is limited to completion/admission evidence: a ZooKeeper snapshot is not a scrub checkpoint, and OpenZFS scan state is not a fuzzy database materialization.

## Failure and forgetting

- **Missing required log coverage:** a physically readable and checksum-valid fuzzy snapshot can still be insufficient to reconstruct the end-of-log state.
- **Replay out of order:** the cited idempotence argument no longer establishes convergence.
- **Interrupted snapshot write:** a final `snapshot.<zxid>` pathname can exist without the trailing completion marker; 3.4.14 is designed to reject that condition.
- **Structurally complete but corrupt snapshot:** the trailing marker alone does not authorize use; full deserialize/checksum can reject the candidate and try an older one.
- **Newest candidate rejected:** older retained snapshots can still be live recovery options rather than automatically obsolete history.
- **Naive filename-based cleanup:** deleting the last preceding log can remove post-snapshot-start transactions still required by the recovery set.
- **Over-retention:** keeping every historical snapshot/log consumes storage and is not required by the bounded current-recovery semantics.
- **Over-aggressive purge:** deleting outside the documented recovery closure can destroy restart history even while some snapshot bytes survive.
- **Lower-layer storage failure:** `non-volatile storage`, Java flush/close, and source-level `force(false)` calls are system operations/assumptions, not independent proof of every filesystem, drive-cache, RAID, or power-fail implementation below them.

Purging ZooKeeper files is **logical/operational history retirement**, not proof of secure media sanitization or forensic erasure.

## Prior art and novelty boundary

No invention-priority claim is made.

The ZooKeeper paper itself says that, **as Chubby**, ZooKeeper keeps a replay/WAL of committed operations and periodic snapshots. Mike Burrows's 2006 Chubby paper says Chubby's rewritten database used write-ahead logging and snapshotting similar to earlier work by Birrell et al. This is enough to block any claim that ZooKeeper originated the generic log-plus-snapshot recovery pattern.

The 3.4.14 source deepening is also not evidence that ZooKeeper invented end markers, checksums, fallback recovery, or direct-final-name snapshot writing.

The defensible project contribution is narrower:

> **ZooKeeper's period documentation, 2010 implementation paper, and exact 3.4.14 source together expose a recovery chain in which a durable image can be temporally fuzzy, a final-named artifact can remain inadmissible, and current-state recovery depends on both validation evidence and ordered retained history rather than on one privileged snapshot file.**

## Philosophical interpretation

### I — a retained technical `image` need not be a preserved past moment

This case can discipline philosophical language about technical memory: one durable representation may support faithful continuation without being an exact frozen picture of any single prior instant.

### I — persisted bytes ≠ admitted memory representation

The 3.4.14 source adds a second disciplined distinction. A snapshot file can physically exist while the implementation refuses to treat it as a legitimate recovery base because it lacks structural completion evidence or fails checksum/deserialization.

That does **not** license an analogy to human memory, narrative memory, archival authenticity, or phenomenological retention. These are engineering facts about one recovery construction. Their philosophical usefulness lies precisely in refusing shortcuts such as `snapshot = preserved past present` or `bytes remain = system accepts them as memory`.

## Source ledger

1. Patrick Hunt, Mahadev Konar, Flavio P. Junqueira, and Benjamin Reed, **“ZooKeeper: Wait-free coordination for Internet-scale systems,”** USENIX Annual Technical Conference 2010, official USENIX PDF: <https://www.usenix.org/legacy/events/atc10/tech/full_papers/Hunt.pdf>.
   - §§4.1–4.3: in-memory replicated database, disk/WAL before apply, idempotent transactions, ordered redelivery, fuzzy snapshots, worked recovery example.
2. Apache ZooKeeper **3.1.2 Administrator's Guide** (release announced 14 December 2009): <https://zookeeper.apache.org/doc/r3.1.2/zookeeperAdmin.html>.
   - `Data File Management`: period documentation of fuzzy snapshot naming and replay semantics.
3. Apache ZooKeeper **3.4.14 Administrator's Guide** (release announced 2 April 2019): <https://zookeeper.apache.org/doc/r3.4.14/zookeeperAdmin.html>.
   - `Data File Management` / `File Management`: snapshot-start zxid, non-volatile transaction log, recovery file set, preceding-log requirement.
   - `Ongoing Data Directory Cleanup` / advanced configuration: `PurgeTxnLog`, automatic purge, `autopurge.snapRetainCount`, `autopurge.purgeInterval`.
4. Apache ZooKeeper **3.4.14 release source**, tag `release-3.4.14`, commit `4c25d480e66aadd371de8bd2fd8da255ac140bcf`: <https://github.com/apache/zookeeper/tree/4c25d480e66aadd371de8bd2fd8da255ac140bcf>.
   - `SyncRequestProcessor.java`: asynchronous snapshot launch after log roll.
   - `ZooKeeperServer.java` / `FileTxnSnapLog.java`: snapshot save and restore composition.
   - `FileSnap.java`: direct final-path write, completion marker, checksum verification, newest-to-older fallback.
   - `Util.java`: incomplete-snapshot end-marker validity check.
   - `FileTxnLog.java`: transaction-log iterator/commit path and conditional `force(false)` comparison.
5. Mike Burrows, **“The Chubby lock service for loosely-coupled distributed systems,”** OSDI 2006, §2.10: <https://www.usenix.org/legacy/event/osdi06/tech/full_papers/burrows/burrows_html/>.
   - prior-art boundary: Chubby's rewritten database used write-ahead logging and snapshotting and explicitly pointed to earlier related work.

A fresh search of `tmzncty/computing-archaeology` for `ZooKeeper snapshot transaction log zxid` found no dedicated case. This case therefore adds retention-specific source analysis rather than duplicating an existing engineering history there.

## Claim ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| ZooKeeper serving state is an in-memory replicated tree with a separate durable replay log | H/P | Hunt et al. §4 | supported |
| transactions are forced to disk before application in the bounded 2010 implementation description | H/P | Hunt et al. §4 | supported |
| internal state-changing transactions are idempotent and duplicate replay is allowed in order | H/P | Hunt et al. §§4.1–4.3 | supported |
| fuzzy snapshot may correspond to no actual point-in-time tree | H/P | Hunt et al. §4.3; Apache admin docs; 3.4.14 replay comments | supported |
| replay from the snapshot-start boundary reconstructs end-of-log state | H/P | Hunt et al.; Apache admin docs; `FileTxnSnapLog` | supported |
| last log preceding a snapshot may still contain newer needed transactions | H/P | Apache 3.4.14 admin guide | supported |
| configured purge can retire older snapshots/logs while preserving recent recovery sets | H/P | Apache 3.4.14 admin guide | supported |
| 3.4.14 writes snapshot payload directly to the supplied final `snapshot.<zxid>` path | H/P | `FileTxnSnapLog.save()`; `FileSnap.serialize()` | supported |
| 3.4.14 bounded snapshot path publishes by temp-file atomic rename | X | inspected release source | rejected for this path |
| trailing `/` is lightweight structural completion evidence | H/P | `Util.isValidSnapshot()`; `FileSnap.serialize()` | supported |
| trailing marker alone proves full snapshot validity | X | `FileSnap.findNValidSnapshots()` comment + full checksum path | rejected |
| full deserialize validates header and Adler32 checksum | H/P | `FileSnap.deserialize()` | supported |
| newest final-named snapshot must be the recovery base | X | newest-to-older fallback path | rejected |
| older retained snapshot may be selected if newer candidate is unusable | H/P | `FileSnap.deserialize()` | supported |
| successful candidate filename determines replay start state | H/P | `FileSnap.deserialize()`; `fastForwardFromEdits()` | supported |
| checksum-valid snapshot alone is sufficient regardless of retained transaction history | X | docs + restore composition | rejected |
| idempotence makes transaction order irrelevant | X | Hunt et al. §4.2 | rejected |
| snapshot filename zxid is the maximum zxid embodied anywhere in the file | X | Apache admin docs | rejected |
| source-level flush/force proves universal lower-layer power-loss durability | X | lower-layer evidence absent | rejected |
| purging ZooKeeper files proves secure physical erasure | X | no lower-layer evidence | rejected |
| ZooKeeper invented WAL+snapshot recovery | X | Hunt et al.; Burrows 2006 | rejected |

## Case findings

1. **Recovery-equivalent representation ≠ historically existing instantaneous representation.**
2. **Fuzzy snapshot ≠ arbitrary inconsistent bytes.**
3. **Snapshot-start zxid ≠ maximum update embodied in the snapshot.**
4. **Snapshot payload ≠ sufficient recovery closure.**
5. **Duplicate replay tolerance ≠ order irrelevance.**
6. **Current in-memory state ≠ one independently durable image.**
7. **Durable transaction history ≠ complete indefinite history.**
8. **Last log preceding snapshot ≠ necessarily obsolete log.**
9. **File-age ordering ≠ recovery-dependency ordering.**
10. **Recovery-set retention can be more important than retention of one privileged file.**
11. **Newer complete recovery set can authorize retirement of older recovery history.**
12. **Purge policy ≠ secure erasure policy.**
13. **Operator-retained rollback/troubleshooting history ≠ minimum restart-recovery history.**
14. **ZooKeeper fuzzy snapshot ≠ Raft stable-snapshot semantics.**
15. **Fuzzy materialization can reduce snapshot locking work by shifting correctness burden into replay semantics.**
16. **ZooKeeper 2010 fuzzy recovery ≠ invention of WAL/snapshot recovery.**
17. **Final snapshot pathname existence ≠ completed snapshot materialization.**
18. **Completion marker ≠ full checksum/content admission.**
19. **Newest snapshot pathname ≠ necessarily selected recovery base.**
20. **Reader-side validation/fallback ≠ crash-atomic publication.**
21. **Admissible snapshot ≠ complete recovery set.**
22. **Payload bytes ≠ evidence authorizing those bytes for recovery.**
23. **Transaction-log force path ≠ snapshot-file write path.**

## Next evidence

The exact 3.4.14 release-tag source archaeology for snapshot creation/admission/replay is now closed by the linked deepening.

Future work should remain separate: controlled kill/power-cut fault injection at multiple points in `FileSnap.serialize()`; deliberate end-marker/body/checksum corruption; missing transaction-log segments after a valid snapshot; filesystem/device persistence composition for snapshot close/flush versus log `force(false)`; source genealogy before 3.4.14 and later snapshot-format changes; Zab persistence/epoch history; dynamic reconfiguration; and later snapshot/restore APIs. None is required to support this case's central fuzzy-snapshot/admission/replay distinction.