from pathlib import Path

CASE_PATH = Path("cases/71-apache-zookeeper-fuzzy-snapshot-replay-recovery.md")
EVIDENCE_PATH = Path("evidence/71-zookeeper-2006-2019-fuzzy-snapshot-grounding.md")
WORKFLOW_PATH = Path(".github/workflows/case71-integrate.yml")
SELF_PATH = Path(".github/case71_integrate.py")

case_text = r'''# Apache ZooKeeper Fuzzy Snapshots: Non-Point-in-Time Materialization, Ordered Replay, and Recovery-Set Retention

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
'''

evidence_text = r'''# Case 71 Grounding Record — ZooKeeper Fuzzy Snapshot / Replay Recovery, 2006–2019

## Purpose

This record grounds [`../cases/71-apache-zookeeper-fuzzy-snapshot-replay-recovery.md`](../cases/71-apache-zookeeper-fuzzy-snapshot-replay-recovery.md).

The bounded question is not `how does ZooKeeper work?` and not `what is a consensus snapshot?` Case 58 already covers Raft snapshot/log compaction, while Cases 46 and 57 cover GFS checkpoint recovery and Bigtable log/materialization recovery.

The narrower question is:

> **What primary evidence shows that ZooKeeper deliberately permits a durable snapshot that may correspond to no actual instantaneous tree, and what retained ordered log relation makes that fuzzy image a valid recovery base?**

The case is promoted directly to `grounded` because the central mechanism is stated explicitly by the 2010 system paper and independently restated in period/release documentation, while the 2006 Chubby paper provides an explicit prior-art boundary against an origin claim.

---

## Source A — Hunt et al., USENIX ATC 2010

- **Title:** `ZooKeeper: Wait-free coordination for Internet-scale systems`
- **Authors:** Patrick Hunt, Mahadev Konar, Flavio P. Junqueira, Benjamin Reed
- **Venue:** USENIX Annual Technical Conference 2010
- **Primary source:** https://www.usenix.org/legacy/events/atc10/tech/full_papers/Hunt.pdf
- **Evidence role:** implementation-era recovery mechanism, transaction idempotence/order, fuzzy snapshot semantics, worked recovery example.

### What §4 establishes

The paper states that the fully replicated ZooKeeper database is held in memory. For recoverability, updates are logged to disk; the implementation description says the writes are forced to disk media before they are applied to the in-memory database. It explicitly calls the retained history a replay log / write-ahead log of committed operations and says periodic snapshots are generated.

This supports:

> `serving embodiment ≠ durable recovery representation`.

### What §§4.1–4.2 establish

ZooKeeper transforms client write requests into state-changing transactions that capture the new state/version/timestamps. The paper distinguishes those internal transactions from the incoming request and describes them as idempotent.

It further says recovery may redeliver messages; multiple delivery is acceptable if the transactions are applied **in order**. ZooKeeper therefore requires redelivery at least from the start of the last snapshot.

This supports both:

> `duplicate replay tolerance ≠ duplicate client-request tolerance`

and:

> `idempotence ≠ order irrelevance`.

### What §4.3 establishes

The snapshot is called `fuzzy` because ZooKeeper does not globally lock the data tree. It scans the tree and writes znodes while updates can continue. The result may contain some but not all updates from the snapshot interval and may correspond to no tree state that existed at a single instant.

The paper's `/foo` and `/goo` example is decisive. A fuzzy image may contain a version combination that was never live; replaying the ordered transactions nevertheless reconstructs the pre-crash service state.

This directly grounds:

> `recovery-equivalent representation ≠ historically existing instantaneous representation`.

### Evidence boundary

The paper does **not** establish:

- that every client operation is idempotent;
- that transaction replay order is irrelevant;
- that any arbitrary mixed snapshot is recoverable;
- that ZooKeeper invented fuzzy checkpoints or WAL;
- exact lower-layer power-failure semantics of every disk/controller/filesystem used in deployment.

---

## Source B — Apache ZooKeeper 3.1.2 Administrator's Guide

- **Release announced:** 2009-12-14
- **Primary source:** https://zookeeper.apache.org/doc/r3.1.2/zookeeperAdmin.html
- **Evidence role:** period-release administrator description of `snapshot.<zxid>`, fuzzy state, and transaction-log replay.

The guide says:

- `snapshot.<zxid>` holds a fuzzy data-tree snapshot;
- the suffix is the last committed zxid at snapshot **start**;
- the file can contain a subset of updates that happen during the scan;
- the resulting image may correspond to no actual data-tree state;
- replay against the fuzzy snapshot recovers the state at the end of the log;
- transactions are written to non-volatile storage before updates take place.

This documentation predates the 2010 paper's publication and therefore also blocks treating the paper as the first public appearance of the mechanism.

It does **not** by itself establish invention priority before ZooKeeper 3.1.2.

---

## Source C — Apache ZooKeeper 3.4.14 Administrator's Guide

- **Release announced:** 2019-04-02
- **Primary source:** https://zookeeper.apache.org/doc/r3.4.14/zookeeperAdmin.html
- **Evidence role:** mature 3.4-series recovery-set and cleanup semantics.

### Fuzzy snapshot and log boundary

The guide repeats the core fuzzy-snapshot explanation and defines snapshot suffix semantics from the start boundary.

### Recovery-set file coverage

The strongest retention-specific statement is in `File Management`:

- current restart needs the latest complete fuzzy snapshot;
- all following transaction logs are needed;
- the **last log file preceding** the snapshot is also needed;
- that earlier-starting file can contain transactions newer than the snapshot because snapshotting and log rollover can proceed independently.

This directly supports:

> `older-starting log file ≠ obsolete recovery evidence`.

It also shows that the retention unit is a **set/relation of files**, not simply whichever single snapshot has the largest filename suffix.

### Purging and bounded history

The same guide documents `PurgeTxnLog` and says automatic purge was introduced in 3.4.0. `autopurge.snapRetainCount` keeps the configured number of recent snapshots and corresponding transaction logs, while `autopurge.purgeInterval` controls execution; the bounded release documents default/minimum retention of three snapshots.

This supports:

> `current recoverability ≠ indefinite preservation of every recovery artifact`.

### Evidence boundary

The guide does not prove:

- physical secure erasure after purge;
- exact storage blocks overwritten by cleanup;
- that keeping only the minimum count survives every conceivable corruption pattern;
- the behavior of later ZooKeeper 3.5+/3.6+/3.9 snapshot APIs.

---

## Source D — Burrows, Chubby, OSDI 2006

- **Title:** `The Chubby lock service for loosely-coupled distributed systems`
- **Author:** Mike Burrows
- **Venue:** OSDI 2006
- **Primary source:** https://www.usenix.org/legacy/event/osdi06/tech/full_papers/burrows/burrows_html/
- **Evidence role:** prior-art boundary.

Section 2.10 says Chubby replaced Berkeley DB replication with a simpler database using **write-ahead logging and snapshotting** similar to an earlier Birrell et al. design. Chubby's log itself was consensus-replicated.

The ZooKeeper 2010 paper in turn explicitly says it keeps a replay/WAL and snapshots `as Chubby`.

Therefore this case must not say:

- ZooKeeper invented WAL;
- ZooKeeper invented periodic snapshots;
- ZooKeeper first combined them for replicated coordination state.

A full genealogy of fuzzy/nonblocking checkpoint algorithms is outside this slice.

---

## Related-repository duplication check

A search of `tmzncty/computing-archaeology` for `ZooKeeper`, `fuzzy snapshot`, `transaction log`, and `zxid` did not find a dedicated case before drafting.

The present case therefore does not duplicate an existing engineering history there. If future work expands into ZooKeeper/Zab protocol history, that broader technical-history material should be routed to `computing-archaeology` and only the retention-specific comparison retained here.

---

## Claim-source matrix

| Claim | Hunt et al. 2010 | ZK 3.1.2 guide | ZK 3.4.14 guide | Chubby 2006 | Status |
| --- | --- | --- | --- | --- | --- |
| current serving data tree is in memory while updates are durably logged for recovery | direct | compatible | direct | analogous | **grounded** |
| snapshot can contain a subset of concurrent updates and match no actual instantaneous state | direct | direct | direct | — | **grounded** |
| ordered idempotent replay makes such a fuzzy image recoverable | direct | direct | direct | — | **grounded** |
| snapshot suffix zxid marks snapshot-start boundary rather than maximum embedded update | compatible | direct | direct | — | **grounded** |
| last log preceding snapshot may contain newer required transactions | compatible | version-specific layout differs | direct | — | **grounded** for 3.4.14 |
| old recovery history may be policy-pruned while retaining recent recovery sets | — | external/manual cleanup era | direct | backups discussed | **grounded** for 3.4.14 |
| ZooKeeper invented WAL+snapshot recovery | no | no | no | directly contradictory prior art | **rejected** |
| idempotence makes ordering unnecessary | directly contradicted | no | no | — | **rejected** |
| purge means secure erasure | no | no | no | no | **rejected / unsupported** |

---

## Cross-case comparison boundary

### Case 58 — Raft snapshotting

Functional analogy:

> materialized state can reduce dependence on an indefinitely growing ordered log.

Critical difference:

- Raft's bounded snapshot is tied to an included committed log prefix plus `lastIncludedIndex`/`lastIncludedTerm` and configuration;
- ZooKeeper's fuzzy snapshot can embody a mixed subset of concurrent changes and relies on ordered idempotent replay from the snapshot-start boundary.

No identity of consensus or snapshot semantics is claimed.

### Case 46 — GFS master checkpoint

Both use durable materialization plus later log history to bound restart work. GFS's checkpoint path and ZooKeeper's deliberately fuzzy scan have different point-in-time and recovery-set semantics.

### Case 57 — Bigtable tablet recovery

Both use retained mutation history plus materialized state. Bigtable's memtable/SSTable/redo-point machinery is neither a ZooKeeper fuzzy snapshot nor a Zab replay log.

---

## Findings suitable for synthesis

1. **A technically valid recovery image need not preserve one actual historical instant.**
2. **Snapshot naming metadata can define a conservative replay boundary without describing every update already embodied in the snapshot.**
3. **Idempotence can permit duplicate replay while order remains constitutive.**
4. **A physically intact snapshot can be insufficient if the required replay history is lost.**
5. **Recovery can depend on retaining a closure of related files rather than one privileged artifact.**
6. **An apparently older log can remain part of a newer recovery set.**
7. **Current-state retention may require bounded history without requiring complete indefinite history.**
8. **Cleanup policy can deliberately forget old recovery representations without logically deleting the current ZooKeeper tree.**

---

## Evidence status

**`grounded`**

Promotion rationale:

- **primary evidence:** directly inspected 2010 USENIX implementation paper plus Apache release documentation;
- **period vocabulary:** `replay log`, `write-ahead log`, `committed operations`, `fuzzy snapshot`, `idempotent`, `zxid`;
- **mechanism:** nonlocking tree scan + snapshot-start boundary + ordered idempotent replay + retained transaction-log coverage;
- **operational deepening:** 3.4.14 file-management and autopurge semantics expose which history may remain necessary and which may be policy-retired;
- **prior art:** Chubby 2006 blocks a generic WAL/snapshot-origin claim;
- **related-repository duplication checked:** yes.

### Remaining work

Not blockers for this bounded case:

- exact tag-matched source audit of snapshot file creation/rename and restore atomicity;
- deeper Zab transaction-log and epoch lineage;
- direct fault injection for incomplete/corrupt snapshots and missing log segments;
- lower-layer filesystem/device persistence composition;
- broader checkpoint/fuzzy-checkpoint genealogy;
- later ZooKeeper snapshot/restore APIs.
'''

readme_case_line = "- [`cases/71-apache-zookeeper-fuzzy-snapshot-replay-recovery.md`](cases/71-apache-zookeeper-fuzzy-snapshot-replay-recovery.md) — grounded ZooKeeper fuzzy-snapshot recovery bridge: a durable tree image may correspond to no actual instantaneous state, yet ordered idempotent transaction replay from the snapshot-start boundary reconstructs the end-of-log state; recovery depends on a closure of snapshot plus surrounding log files rather than one privileged point-in-time artifact."
readme_evidence_line = "- [`evidence/71-zookeeper-2006-2019-fuzzy-snapshot-grounding.md`](evidence/71-zookeeper-2006-2019-fuzzy-snapshot-grounding.md) — Case-71 grounding record: Hunt et al. 2010 plus Apache 3.1.2/3.4.14 documentation ground non-point-in-time fuzzy materialization, ordered idempotent replay, preceding-log recovery-set retention, and bounded purge semantics; Chubby 2006 blocks a WAL/snapshot invention claim."
roadmap_line = "- [x] ZooKeeper fuzzy snapshot / replay recovery — [`cases/71-apache-zookeeper-fuzzy-snapshot-replay-recovery.md`](cases/71-apache-zookeeper-fuzzy-snapshot-replay-recovery.md), grounded by [`evidence/71-zookeeper-2006-2019-fuzzy-snapshot-grounding.md`](evidence/71-zookeeper-2006-2019-fuzzy-snapshot-grounding.md), adds a deliberately non-point-in-time recovery regime: the durable snapshot may correspond to no actual live tree, while ordered idempotent replay from the snapshot-start boundary reconstructs end-of-log state. Apache 3.4.14 further makes recovery-set retention explicit: the latest complete fuzzy snapshot, following logs, and the last preceding log can all be required, while purge policy may retire older complete recovery sets. This remains distinct from Raft Case 58's stable committed-prefix snapshot semantics and does not claim ZooKeeper invented WAL/snapshot recovery."

case_index_row = "| [Apache ZooKeeper Fuzzy Snapshots: Non-Point-in-Time Materialization, Ordered Replay, and Recovery-Set Retention](cases/71-apache-zookeeper-fuzzy-snapshot-replay-recovery.md) | **grounded** | replicated in-memory coordination state + non-volatile transaction log + nonlocking fuzzy snapshot + snapshot-start zxid + ordered idempotent replay + bounded recovery-file-set retention | separate recovery-equivalent materialization from point-in-time historical fidelity; snapshot boundary from maximum embodied update; duplicate replay tolerance from order irrelevance; and current-state recoverability from indefinite log history | [2006–2019 ZooKeeper/Chubby grounding](evidence/71-zookeeper-2006-2019-fuzzy-snapshot-grounding.md); exact tag-matched snapshot/restore crash windows, Zab persistence genealogy, corruption fault injection, and later snapshot APIs remain separate work |"

matrix_row = "| Apache ZooKeeper fuzzy snapshot / 2009–2019 bounded regime | in-memory data tree + non-volatile ordered transaction log + fuzzy snapshot + snapshot-start zxid + recovery-set file coverage | committed transactions are logged before application; snapshot scans without globally freezing the tree; recovery replays idempotent transactions in order; old recovery sets may later be purged by policy | serving reads use the in-memory replica; restart first reconstructs the tree from fuzzy materialization plus replay history | znode paths name logical state while zxid/log-file boundaries locate recovery progress rather than physical payload placement | snapshot payload can be temporally mixed; current logical tree survives process loss if the required snapshot/log closure remains | retains bounded replay history and optional older recovery sets rather than a mandatory complete indefinite operation history |"

findings = r'''

## Case 71 — ZooKeeper fuzzy-snapshot / replay-recovery findings

813. **recovery-equivalent representation ≠ historically existing instantaneous representation** — a ZooKeeper fuzzy snapshot may correspond to no live tree state that ever existed, yet still be a valid base for reconstruction;
814. **fuzzy snapshot ≠ arbitrary inconsistent bytes** — the bounded image comes from atomic per-znode reads during an ordered update stream and is paired with a defined replay discipline;
815. **snapshot-start zxid ≠ maximum update embodied in the snapshot** — the filename boundary marks the last committed transaction at snapshot start while the file may already include effects of later transactions;
816. **snapshot payload ≠ sufficient recovery closure** — recoverability depends on the retained transaction history needed to replay from the snapshot-start boundary to the desired end state;
817. **duplicate replay tolerance ≠ order irrelevance** — ZooKeeper's internal transactions are idempotent, but the 2010 paper explicitly requires redelivery/application in order;
818. **client request ≠ idempotent recovery transaction** — the implementation transforms requests into state-changing transactions that capture resulting versions/state; the replay argument does not make arbitrary duplicate client operations harmless;
819. **current in-memory state ≠ one independently durable image** — the serving database lives in memory while durable log and snapshot representations separately support reconstruction;
820. **durable transaction history ≠ complete indefinite history** — enough ordered history must survive for recovery, but older complete recovery sets can later become dispensable;
821. **last log preceding snapshot ≠ necessarily obsolete log** — Apache 3.4.14 warns that the earlier-starting log may contain transactions newer than snapshot start and therefore remain required;
822. **file-age ordering ≠ recovery-dependency ordering** — a file that appears older by starting zxid can still belong to the closure of a newer fuzzy snapshot;
823. **recovery-set retention can matter more than retention of one privileged file** — restart depends on a compatible snapshot/log set rather than on the physical survival of one artifact considered in isolation;
824. **newer recovery closure can authorize forgetting of older recovery artifacts** — purge can delete older snapshots and corresponding logs after newer retained sets exist, without deleting the current logical tree;
825. **purge policy ≠ secure erasure policy** — removing ZooKeeper's live recovery artifacts does not prove lower-layer physical sanitization or forensic absence;
826. **operator-retained rollback/troubleshooting history ≠ minimum restart history** — administrators may preserve older files beyond what the server needs for current restart, making archival depth a separate policy dimension;
827. **ZooKeeper fuzzy snapshot ≠ Raft stable-snapshot semantics** — both bound replay history, but Case 71 relies on non-point-in-time materialization plus ordered idempotent replay while Case 58 carries committed-prefix boundary/term/configuration semantics;
828. **ZooKeeper 2010 fuzzy recovery ≠ invention of WAL/snapshot recovery** — the paper explicitly points to Chubby, whose 2006 paper already describes write-ahead logging plus snapshotting and itself cites earlier related work.
'''


def insert_after_line(path, needle, new_line):
    text = Path(path).read_text(encoding="utf-8")
    if new_line in text:
        return
    lines = text.splitlines()
    matches = [i for i, line in enumerate(lines) if needle in line]
    if len(matches) != 1:
        raise RuntimeError(f"anchor {needle!r} matched {len(matches)} times in {path}")
    lines.insert(matches[0] + 1, new_line)
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")

if CASE_PATH.exists() or EVIDENCE_PATH.exists():
    raise RuntimeError("Case 71 research files already exist")
CASE_PATH.write_text(case_text.rstrip() + "\n", encoding="utf-8")
EVIDENCE_PATH.write_text(evidence_text.rstrip() + "\n", encoding="utf-8")

insert_after_line("README.md", "cases/70-magnetic-core-half-select-disturbance.md", readme_case_line)
insert_after_line("README.md", "evidence/70-core-1951-1959-half-select-grounding.md", readme_evidence_line)
insert_after_line("ROADMAP.md", "magnetic-core half-select disturbance / selection-margin deepening", roadmap_line)
insert_after_line("CASE_INDEX.md", "cases/70-magnetic-core-half-select-disturbance.md", case_index_row)
insert_after_line("CASE_INDEX.md", "| Coincident-current magnetic-core half-select / 1951–1959 bounded regime", matrix_row)

ci_path = Path("CASE_INDEX.md")
ci = ci_path.read_text(encoding="utf-8")
if "## Case 71 — ZooKeeper fuzzy-snapshot / replay-recovery findings" not in ci:
    if "812. **Case-70 deepening ≠ new core-memory invention claim**" not in ci:
        raise RuntimeError("Case 70 findings tail not found")
    ci_path.write_text(ci.rstrip() + findings + "\n", encoding="utf-8")

assert "cases/71-apache-zookeeper-fuzzy-snapshot-replay-recovery.md" in Path("README.md").read_text(encoding="utf-8")
assert "ZooKeeper fuzzy snapshot / replay recovery" in Path("ROADMAP.md").read_text(encoding="utf-8")
assert "828. **ZooKeeper 2010 fuzzy recovery" in Path("CASE_INDEX.md").read_text(encoding="utf-8")

nums = sorted(int(p.name[:2]) for p in Path("cases").glob("[0-9][0-9]-*.md"))
if nums != list(range(72)):
    raise RuntimeError(f"case ledger is not continuous 00–71: {nums}")

if WORKFLOW_PATH.exists():
    WORKFLOW_PATH.unlink()
if SELF_PATH.exists():
    SELF_PATH.unlink()
