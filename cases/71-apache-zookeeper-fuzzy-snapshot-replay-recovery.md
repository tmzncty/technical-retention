# Apache ZooKeeper Fuzzy Snapshots: Non-Point-in-Time Materialization, Ordered Replay, and Recovery-Set Retention

## Status

**`grounded`** — bounded to the fuzzy-snapshot / transaction-log recovery relation documented by Apache ZooKeeper's 2009–2019 administrator documentation and the 2010 USENIX ATC ZooKeeper paper.

Grounding record: [`../evidence/71-zookeeper-2006-2019-fuzzy-snapshot-grounding.md`](../evidence/71-zookeeper-2006-2019-fuzzy-snapshot-grounding.md).

## Scope

This case asks one narrow distributed-retention question:

> **Can a durable snapshot remain a valid recovery representation even when it does not correspond to any single historical state that ever existed, and what log history must remain so that recovery still converges to the authoritative end-of-log state?**

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

recovery
    -> load latest complete fuzzy snapshot
    -> retain/find log coverage from snapshot start
    -> replay idempotent transactions in order
    -> duplicate application of some already-embodied changes is tolerated
    -> reconstructed tree reaches the state at the end of the retained log
```

This is **not** a general ZooKeeper, Zab, consensus, checkpointing, write-ahead-logging, or distributed-coordination history. It also does not claim that ZooKeeper invented snapshots, WAL, fuzzy checkpoints, idempotent replay, or state-machine recovery. The 2010 paper explicitly compares its replay-log-plus-snapshot approach to Chubby, and Chubby's 2006 paper in turn describes a write-ahead-log-and-snapshot database related to still earlier work.

The retention-specific claim is narrower:

> **ZooKeeper supplies a particularly explicit production-oriented case in which a retained recovery image need not be a faithful picture of one historical instant. Recoverability instead depends on a relation among the fuzzy snapshot, its replay boundary, ordered idempotent transactions, and enough retained log files to close the gap to the end of the log.**

`recovery-set retention`, `representation closure`, and `historical-instant fidelity` below are project engineering terms, not ZooKeeper vocabulary.

## Historical vocabulary

The sources directly use `replicated database`, `in-memory database`, `replay log`, `write-ahead log`, `committed operations`, `snapshot`, `fuzzy snapshot`, `transaction`, `idempotent`, `zxid`, `transaction log`, `non-volatile storage`, `PurgeTxnLog`, and `autopurge.snapRetainCount`.

Do not silently normalize these into Raft `lastIncludedIndex/Term`, GFS checkpoint positions, database LSNs, Kafka high watermarks, HDFS epochs, or a generic `snapshot ID`.

## Historical record

### H/P — current serving state is in memory while recovery state is separately logged

The 2010 USENIX ATC paper states that the replicated ZooKeeper database is an in-memory data tree. For recoverability, updates are logged to disk, and writes are forced to disk media before they are applied to the in-memory database. The same section calls the retained history a replay log / write-ahead log of committed operations and says ZooKeeper periodically snapshots the in-memory database.

This prevents the shortcut:

> `current in-memory tree = one already-complete durable image`.

**Primary anchor:** Hunt et al. 2010, §4 and lines corresponding to the paper's pp. 7–8.

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

## Retained state and mechanism

The bounded recovery regime contains several different state classes:

1. **current in-memory data tree** — the serving embodiment;
2. **transaction log** — committed update history used for replay;
3. **fuzzy snapshot payload** — a durable materialization that may mix points from the snapshot interval;
4. **snapshot-start zxid / naming boundary** — a replay locator, not a proof of point-in-time image fidelity;
5. **ordered transaction semantics** — the condition under which duplicate replay remains admissible;
6. **recovery-set file coverage** — enough log files around and after the snapshot start to reach the desired end state;
7. **purge policy** — an administrative rule that can retire older recovery representations while preserving a configured recent set.

The key relation is therefore not:

```text
snapshot = exact old state
```

but:

```text
fuzzy durable materialization
    + replay boundary
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

The snapshot is not self-authenticating as a complete current state. Its adequacy depends on the associated log semantics and retained log coverage. Losing the needed replay history can turn a physically intact snapshot into an insufficient recovery representation.

### E — current payload retention can require history retention only up to a moving recovery frontier

ZooKeeper does not need every transaction forever to recover current state. Once newer complete recovery sets exist, older snapshots/logs can be purged according to policy. Current-state retention therefore depends on **bounded** history, not necessarily an indefinite audit log.

### E — file-age ordering ≠ recovery-dependency ordering

The last log file whose starting zxid precedes the snapshot can still contain post-start transactions needed for recovery. A file that looks `older` by its starting identifier can therefore remain part of the newer snapshot's recovery closure.

### E — serving-state durability and archival history are different objectives

The 3.4.14 guide permits retention management of old files while the service can continue to retain enough state for restart. Conversely, an operator may keep more old snapshots/logs for troubleshooting or rollback. Those extra files are historical retention beyond the minimum current-serving recovery contract.

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

## Failure and forgetting

- **Missing required log coverage:** a physically readable fuzzy snapshot can become insufficient to reconstruct the end-of-log state.
- **Replay out of order:** the cited idempotence argument no longer establishes convergence.
- **Incomplete snapshot mistaken for complete:** the bounded documentation explicitly requires a latest complete fuzzy snapshot; mere file existence is not enough.
- **Naive filename-based cleanup:** deleting the last preceding log can remove post-snapshot-start transactions still required by the recovery set.
- **Over-retention:** keeping every historical snapshot/log consumes storage and is not required by the bounded current-recovery semantics.
- **Over-aggressive purge:** deleting outside the documented recovery closure can destroy restart history even while some snapshot bytes survive.
- **Lower-layer storage failure:** `non-volatile storage` / forcing to disk in the cited source is a system assumption/operation, not independent proof of every filesystem, drive-cache, RAID, or power-fail implementation below it.

Purging ZooKeeper files is **logical/operational history retirement**, not proof of secure media sanitization or forensic erasure.

## Prior art and novelty boundary

No invention-priority claim is made.

The ZooKeeper paper itself says that, **as Chubby**, ZooKeeper keeps a replay/WAL of committed operations and periodic snapshots. Mike Burrows's 2006 Chubby paper says Chubby's rewritten database used write-ahead logging and snapshotting similar to earlier work by Birrell et al. This is enough to block any claim that ZooKeeper originated the generic log-plus-snapshot recovery pattern.

The defensible project contribution is narrower:

> **ZooKeeper 2009–2019 documentation plus the 2010 implementation paper provide an unusually explicit case where recovery correctness is compatible with a durable snapshot that never existed as one live historical state, because ordered idempotent replay and recovery-set retention supply the missing temporal closure.**

## Philosophical interpretation

### I — a retained technical `image` need not be a preserved past moment

This case can discipline philosophical language about technical memory: one durable representation may support faithful continuation without being an exact frozen picture of any single prior instant.

That does **not** license an analogy to human memory, narrative memory, or phenomenological retention. It is an engineering fact about one recovery construction. The philosophical usefulness lies precisely in refusing the shortcut `snapshot = preserved past present`.

## Source ledger

1. Patrick Hunt, Mahadev Konar, Flavio P. Junqueira, and Benjamin Reed, **“ZooKeeper: Wait-free coordination for Internet-scale systems,”** USENIX Annual Technical Conference 2010, official USENIX PDF: <https://www.usenix.org/legacy/events/atc10/tech/full_papers/Hunt.pdf>.
   - §§4.1–4.3: in-memory replicated database, disk/WAL before apply, idempotent transactions, ordered redelivery, fuzzy snapshots, worked recovery example.
2. Apache ZooKeeper **3.1.2 Administrator's Guide** (release announced 14 December 2009): <https://zookeeper.apache.org/doc/r3.1.2/zookeeperAdmin.html>.
   - `Data File Management`: period documentation of fuzzy snapshot naming and replay semantics.
3. Apache ZooKeeper **3.4.14 Administrator's Guide** (release announced 2 April 2019): <https://zookeeper.apache.org/doc/r3.4.14/zookeeperAdmin.html>.
   - `Data File Management` / `File Management`: snapshot-start zxid, non-volatile transaction log, recovery file set, preceding-log requirement.
   - `Ongoing Data Directory Cleanup` / advanced configuration: `PurgeTxnLog`, automatic purge, `autopurge.snapRetainCount`, `autopurge.purgeInterval`.
4. Mike Burrows, **“The Chubby lock service for loosely-coupled distributed systems,”** OSDI 2006, §2.10: <https://www.usenix.org/legacy/event/osdi06/tech/full_papers/burrows/burrows_html/>.
   - prior-art boundary: Chubby's rewritten database used write-ahead logging and snapshotting and explicitly pointed to earlier related work.

A search of `tmzncty/computing-archaeology` for ZooKeeper snapshot / transaction-log / zxid terms found no dedicated case before drafting. This case therefore adds retention-specific analysis rather than duplicating an existing engineering history.

## Claim ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| ZooKeeper serving state is an in-memory replicated tree with a separate durable replay log | H/P | Hunt et al. §4 | supported |
| transactions are forced to disk before application in the bounded 2010 implementation description | H/P | Hunt et al. §4 | supported |
| internal state-changing transactions are idempotent and duplicate replay is allowed in order | H/P | Hunt et al. §§4.1–4.3 | supported |
| fuzzy snapshot may correspond to no actual point-in-time tree | H/P | Hunt et al. §4.3; Apache admin docs | supported |
| replay from the snapshot-start boundary reconstructs end-of-log state | H/P | Hunt et al. §4.3; Apache admin docs | supported |
| last log preceding a snapshot may still contain newer needed transactions | H/P | Apache 3.4.14 admin guide | supported |
| configured purge can retire older snapshots/logs while preserving recent recovery sets | H/P | Apache 3.4.14 admin guide | supported |
| fuzzy snapshot alone is sufficient regardless of retained transaction history | X | sources above | rejected |
| idempotence makes transaction order irrelevant | X | Hunt et al. §4.2 | rejected |
| snapshot filename zxid is the maximum zxid embodied anywhere in the file | X | Apache admin docs | rejected |
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

## Next evidence

Future work should remain separate: exact release-tag source archaeology for snapshot creation/atomic rename and restore crash windows; Zab persistence/epoch history beyond the bounded paper; corruption handling; dynamic reconfiguration; independent fault injection; container/filesystem durability composition; and later snapshot/restore APIs. None is required to support this case's central fuzzy-snapshot/replay distinction.
