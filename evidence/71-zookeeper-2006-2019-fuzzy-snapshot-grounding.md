# Case 71 Grounding Record — ZooKeeper Fuzzy Snapshot / Replay Recovery, 2006–2019

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
