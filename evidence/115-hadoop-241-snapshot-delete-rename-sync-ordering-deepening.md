# Evidence 115D — Hadoop 2.4.1 Snapshot Delete/Rename Completion and Retirement Ordering

**Status:** `bounded deepening complete`

## Scope

This note closes one deliberately narrow debt left by Evidence 115C and the canonical Case 115:

> In Apache Hadoop `release-2.4.1`, what exactly happens between a successful snapshot **rename** or **delete** namespace mutation, its edit-log record, the HDFS `logSync()` boundary, and—only for deletion—the later block-retirement path?

The answer is useful because `snapshot operation succeeded`, `namespace edit was logged`, `the caller's edit crossed the NameNode edit-log sync boundary`, `NameNode block-retirement work ran`, `DataNode invalidation completed`, and `physical media was overwritten` are not the same event.

This record is intentionally version-bounded to Hadoop `release-2.4.1`. It does not claim arbitrary-crash safety at every instruction boundary, JournalNode/HA semantics, lower-device durability, secure erasure, or historical priority for edit logging or snapshots.

The slice also does not reopen the broader HDFS snapshot history. Existing Case 115 evidence already grounds shared-block snapshot semantics, replication obligations, ordinary edit-log replay, checkpoint/restart behavior, and the later NameNode→DataNode invalidation pipeline. Here the question is only **completion ordering for two snapshot namespace operations**.

---

## Source and repository checks

Before this slice, the current Case 115 canon and Evidence 115C already established:

- dedicated `CreateSnapshotOp`, `DeleteSnapshotOp`, and `RenameSnapshotOp` edit-log representations;
- matching `FSEditLogLoader` replay branches;
- normal non-format restart reconstruction through edit-log application;
- `createSnapshot(...) -> logCreateSnapshot(...) -> logSync() -> successful return`;
- a separate staged block-retirement/invalidation path after a final retaining relation disappears.

Evidence 115C explicitly left **the exact delete/rename API completion-sync boundaries** open. This slice checks those paths directly rather than assuming they match create.

A fresh search of `tmzncty/computing-archaeology` for `HDFS snapshot deleteSnapshot renameSnapshot` found no dedicated packet to reuse. Broader Hadoop journaling, NameNode implementation history, snapshot genealogy, and HA evolution remain work for that companion repository.

---

## Primary sources

### P1 — Apache Hadoop `release-2.4.1` `FSNamesystem.java` — `H/P`

<https://github.com/apache/hadoop/blob/release-2.4.1/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.java>

The released source contains the operation paths inspected here.

For `renameSnapshot(...)`, the successful non-retry path performs, in order:

1. permission/name checks;
2. `snapshotManager.renameSnapshot(...)`;
3. `getEditLog().logRenameSnapshot(...)`;
4. leaves the NameNode write-lock block and records retry-cache state;
5. calls `getEditLog().logSync()`;
6. performs audit logging and returns.

For `deleteSnapshot(...)`, the successful non-retry path performs, in order:

1. permission and safe-mode checks;
2. allocates `BlocksMapUpdateInfo collectedBlocks` and an inode-removal collection;
3. `snapshotManager.deleteSnapshot(...)`, which may populate the retirement collections;
4. removes collected inodes from the inode map;
5. `getEditLog().logDeleteSnapshot(...)`;
6. leaves the write-lock block and records retry-cache state;
7. calls `getEditLog().logSync()`;
8. calls `removeBlocks(collectedBlocks)` and clears that collection;
9. performs audit logging and returns.

The important evidence is the ordering. The source does not say that `logSync()` by itself proves secure lower-media durability, nor that `removeBlocks(...)` means a DataNode has already erased local bytes.

### P2 — Apache Hadoop `release-2.4.1` `FSEditLog.java` — `H/P`

<https://github.com/apache/hadoop/blob/release-2.4.1/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSEditLog.java>

`logDeleteSnapshot(...)` and `logRenameSnapshot(...)` construct their specific edit operations, optionally attach RPC IDs, and call `logEdit(op)`.

The same file documents `FSEditLog` as maintaining a log of namespace modifications. Its `logSync()` implementation obtains the calling thread's current transaction ID (`mytxid`), waits if another sync is running and has not yet covered that transaction, treats `mytxid <= synctxid` as already flushed, and otherwise performs the sync path. The file explicitly tracks a monotonically increasing `txid` and a `synctxid` described as the last synced transaction ID.

This lets the retention claim remain exact:

> `logSync()` is a transaction-oriented NameNode edit-log synchronization boundary for the caller's logged operation; it is not an unlimited theorem about every layer below the journal implementation.

### P3 — Evidence 115B / existing Case 115 retirement path — `H/P + E`

The already-grounded 2.4.1 retirement path is:

```text
collected block
    -> FSNamesystem.removeBlocks(...)
    -> BlockManager.removeBlock(...)
    -> invalidation work retained for the DataNode
    -> heartbeat DNA_INVALIDATE
    -> DataNode FSDataset.invalidate(...)
```

This slice does not re-prove that path. It uses it only to interpret what follows `deleteSnapshot(...)->logSync()`.

### P4 — Evidence 115C / existing replay path — `H/P + E`

Evidence 115C already establishes that `DeleteSnapshotOp` and `RenameSnapshotOp` have replay handlers in `FSEditLogLoader`, and that the released snapshot test suite explicitly exercises ordinary edit-log application across NameNode restart.

This matters because the edit record is not only a contemporaneous completion marker. It participates in later reconstruction of namespace state.

---

## Historical record

### H/P — rename has an explicit mutation → edit → sync → return path

The inspected `renameSnapshot(...)` implementation does not merely mutate `SnapshotManager` state and return.

The successful path is:

```text
rename snapshot namespace relation
    -> logRenameSnapshot(...)
    -> release NameNode write lock
    -> logSync()
    -> audit / return
```

Therefore, for this release and this path:

> **successful rename return != merely unsynchronized in-process rename state.**

The rename has crossed the NameNode edit-log sync boundary before the API method completes.

This statement is deliberately software-layered. It does not say that every possible device cache, RAID controller, SSD FTL, or power-loss mode has independently been proven durable.

### H/P — delete also crosses `logSync()` before the API method completes

The corresponding delete path likewise records `DeleteSnapshotOp` and then calls `logSync()` before returning.

This closes the exact debt left by Evidence 115C:

```text
snapshot deletion mutation
    -> logDeleteSnapshot(...)
    -> logSync()
    -> successful deleteSnapshot completion path
```

The delete path therefore has an explicit sync boundary just as the already-grounded create path does, but the source had to be inspected directly; it was not safe to infer symmetry from create alone.

### H/P — delete orders edit-log synchronization before NameNode block retirement

The strongest new ordering fact is more specific than `delete also syncs`.

In `deleteSnapshot(...)`, the source performs:

```text
snapshotManager.deleteSnapshot(..., collectedBlocks, removedINodes)
    -> remove collected inodes from inode map
    -> logDeleteSnapshot(...)
    -> unlock
    -> logSync()
    -> removeBlocks(collectedBlocks)
    -> return
```

Thus the operation first establishes and synchronizes the namespace deletion edit, and only afterward invokes the NameNode block-removal path for blocks that became collectable.

The safe statement is:

> **the inspected delete path orders the snapshot-deletion edit-log sync boundary before its post-delete `removeBlocks(collectedBlocks)` call.**

This is not yet a proof of every crash point between those calls. It is a directly observed program-order relation in the released source.

### H/P — the returned delete call is later than NameNode `removeBlocks(...)`, but not later than DataNode deletion completion

The method invokes `removeBlocks(collectedBlocks)` before its normal return. Existing Evidence 115B shows that this NameNode-side operation leads into a queued invalidation pipeline rather than synchronously proving that every DataNode has already removed its local replica.

So two boundaries coexist:

```text
successful delete API return
    -> NameNode removeBlocks path has been invoked

successful delete API return
    -/-> every DataNode invalidation has completed
```

The second arrow is intentionally rejected.

### H/P — rename and delete share sync-before-return but not the same retirement consequences

Both operations cross `logSync()` before normal return, but only deletion may create collected blocks/inodes and enter the retirement pipeline.

Therefore:

> **same completion-sync pattern != same state-retirement effect.**

A rename changes how retained historical state is named. A deletion can retire a historical namespace relation and, if it was the last retaining relation for some blocks, expose those blocks to later invalidation/reuse work.

---

## Engineering reconstruction

### E — completion must be decomposed by layer

The source supports at least these distinct completion points:

```text
namespace mutation applied in live NameNode state
        !=
edit operation appended to current edit stream
        !=
caller's transaction covered by HDFS logSync boundary
        !=
NameNode post-delete retirement work invoked
        !=
DataNode invalidation command delivered
        !=
DataNode local dataset invalidation completed
        !=
filesystem extent reused
        !=
physical medium overwritten / sanitized
```

Only some of these are traversed by snapshot rename. Snapshot delete can traverse more of them, but not synchronously all the way to physical erasure.

This decomposition prevents the word `delete` from smuggling in stronger forgetting semantics than the code establishes.

### E — the delete edit is retained before the asynchronous lower retention obligation is discharged

Once the last snapshot relation disappears, some block-retention obligations may end. The inspected ordering shows that the NameNode first synchronizes the namespace transition that withdraws that authority, then starts the post-delete block-removal path.

A useful reconstruction is:

```text
retained authority says block is still historically live
        ->
namespace deletion retires that authority
        ->
edit-log sync retains/reconstructs the authority change
        ->
NameNode may retire block-management state / queue invalidation
        ->
DataNode work can later discharge the physical replica obligation
```

The edit log therefore retains not payload bytes but a **change in retention authority**.

### E — durable-enough namespace knowledge and completed reclamation are different obligations

The delete path exposes two state machines:

1. a namespace-history state machine whose transition is represented in the edit log;
2. a block-retirement state machine that can continue after that transition is synchronized.

Hence:

> **retained knowledge that a snapshot was deleted != completed reclamation of every block formerly protected by that snapshot.**

This is the distributed-filesystem counterpart of several other repository cases in which logical retirement precedes physical reuse, but the analogy remains functional rather than genealogical.

### E — `logSync()` can be satisfied by another sync that already covered the caller's txid

`FSEditLog.logSync()` checks the calling thread's transaction ID against `synctxid`. If another concurrent sync has already advanced the synced frontier beyond the caller's transaction, the method can treat that transaction as already flushed instead of forcing an additional dedicated physical flush for that one API call.

Thus:

> **one successful snapshot API call != one unique dedicated journal flush operation.**

The relevant retained fact is coverage of the caller's transaction by the synced edit-log frontier, not a one-to-one mapping between API calls and flush syscalls/devices.

This is an engineering reading of the source's transaction/sync batching behavior, not a claim about a particular disk cache implementation.

---

## Functional comparison only

### A/E — Case 152 SQLite WAL checkpoint progress

Case 152 also separates authoritative logged history from later maintenance progress. The useful comparison is that a durable/replayable logical transition can coexist with later work that is not itself the authoritative history.

The mechanisms are not genealogically or technically identical: HDFS edit-log namespace operations and SQLite WAL frames/checkpoint backfill use different data structures, failure models, and interfaces.

### A/E — Case 145 JFFS2 reuse admission

Case 145 separates logical obsolescence, erase execution, qualification, and later free-list admission. HDFS snapshot deletion similarly demonstrates that **retirement authority and physical reuse are staged**, but an HDFS block invalidation is not a Flash erase pipeline and no implementation lineage is implied.

### A/E — Case 04 mapped Flash / TRIM

Mapped Flash and host deallocation cases also distinguish logical invalidation from later physical reclamation. Here the relevant relation is a distributed namespace/reference withdrawal followed by NameNode/DataNode cleanup, not FTL mapping retirement.

---

## Philosophical interpretation

`I` — The case gives a precise technical example of why forgetting is not one event. A historical relation can stop counting as authoritative at the namespace layer while the physical embodiments that it formerly protected continue to exist through several later maintenance stages.

`I` — Conversely, the system can retain a record of **having withdrawn a retention obligation**. The edit log is not just a repository of positive persistence claims; it can carry a transition whose operational meaning is that some prior historical reachability no longer has to be maintained.

These interpretations follow the technical decomposition above. They are not Apache actors' vocabulary and do not turn HDFS into a general philosophical model of forgetting.

---

## Explicit non-claims

This record does **not** establish:

1. that Hadoop/HDFS invented snapshot edit logging;
2. that Hadoop/HDFS invented write-ahead or operation logging;
3. that HDFS snapshots are independent backups;
4. that rename duplicates DataNode blocks;
5. that delete immediately erases DataNode storage;
6. that `logSync()` proves every lower storage layer is power-fail durable;
7. that one API call causes one unique journal flush;
8. that a `logSync()` return proves DataNode invalidation completion;
9. that `removeBlocks(...)` proves local filesystem extent reuse;
10. that DataNode invalidation proves physical overwrite;
11. that DataNode invalidation proves secure sanitization;
12. that the source ordering proves every arbitrary crash point is recovered correctly;
13. that a crash between `logSync()` and `removeBlocks(...)` is harmless without separate recovery evidence;
14. that active/standby JournalNode failover has been tested here;
15. that retry-cache state and edit-log state have identical persistence horizons;
16. that create, rename, and delete are implementation-identical merely because all can cross `logSync()`;
17. that a snapshot deletion necessarily frees any particular block—other references can still retain it;
18. that snapshot deletion removes a stronger-replication obligation if another snapshot/current file still imposes it;
19. that Hadoop 2.4.1 behavior is unchanged in modern releases;
20. that functional similarities to WAL, FTL invalidation, or JFFS2 establish genealogy.

---

## What this closes

Closed for the inspected `release-2.4.1` source:

- exact successful `renameSnapshot(...)` namespace-mutation → `logRenameSnapshot(...)` → `logSync()` → return boundary;
- exact successful `deleteSnapshot(...)` namespace-mutation → `logDeleteSnapshot(...)` → `logSync()` → return boundary;
- program-order fact that delete calls `logSync()` **before** the post-delete `removeBlocks(collectedBlocks)` path;
- program-order fact that normal delete return occurs only after the NameNode `removeBlocks(...)` call has run;
- distinction between sync coverage of an edit-log transaction and one dedicated per-call flush;
- distinction between synchronized namespace retirement and later DataNode/local-media reclamation.

Still open:

- fault injection at the window between namespace mutation, edit append, `logSync()`, and `removeBlocks(...)`;
- torn/truncated/corrupt edit-log behavior;
- exact recovery if a NameNode dies after the deletion edit is synced but before all collected blocks enter or finish invalidation processing;
- HA active/standby + shared-edits/JournalNode failover semantics;
- later Hadoop evolution of these operation paths;
- lower filesystem reuse, device remapping/discard, overwrite, and sanitize composition;
- named production incidents or fault-injection studies validating these exact boundaries.

---

## Claim ledger

| Claim | Label | Evidence | Limit |
| --- | --- | --- | --- |
| successful 2.4.1 snapshot rename logs `RenameSnapshotOp` and crosses `logSync()` before normal return | `H/P` | `FSNamesystem.renameSnapshot`; `FSEditLog.logRenameSnapshot` | version/path bounded; lower-media durability not proved |
| successful 2.4.1 snapshot delete logs `DeleteSnapshotOp` and crosses `logSync()` before normal return | `H/P` | `FSNamesystem.deleteSnapshot`; `FSEditLog.logDeleteSnapshot` | version/path bounded; arbitrary crash injection not proved |
| delete orders edit-log sync before `removeBlocks(collectedBlocks)` | `H/P` | `FSNamesystem.deleteSnapshot` | source program order, not exhaustive crash proof |
| normal delete return occurs after NameNode `removeBlocks(...)` is invoked | `H/P` | `FSNamesystem.deleteSnapshot` | does not mean DataNode deletion completed |
| `logSync()` covers the caller's transaction and may be satisfied by an already-advanced synced frontier | `H/P + E` | `FSEditLog.logSync`, `txid`, `synctxid` | does not identify lower physical flush implementation |
| synchronized snapshot deletion equals completed physical reclamation | `X` | no supporting source | explicitly rejected |
| one API call requires one unique physical/journal flush | `X` | `FSEditLog.logSync` batching/frontier behavior | explicitly rejected |
| the ordering proves arbitrary crash recovery | `X` | no fault-injection source | explicitly rejected |

---

## Related repositories

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — fresh search found no dedicated HDFS snapshot delete/rename completion packet. Broad NameNode edit-log history, HA journal evolution, filesystem snapshot genealogy, and Hadoop release-to-release engineering history belong there.
- [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) — useful if later work asks how `delete`, `sync`, `durable`, `snapshot`, `invalidate`, or `recovery` became distinct actor categories rather than importing present-day terminology.

---

## Sources

1. Apache Hadoop `release-2.4.1`, `FSNamesystem.java`.
   - <https://github.com/apache/hadoop/blob/release-2.4.1/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.java>
   - inspected paths: `renameSnapshot(...)`, `deleteSnapshot(...)`.

2. Apache Hadoop `release-2.4.1`, `FSEditLog.java`.
   - <https://github.com/apache/hadoop/blob/release-2.4.1/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSEditLog.java>
   - inspected paths: `logDeleteSnapshot(...)`, `logRenameSnapshot(...)`, `logEdit(...)`, `logSync()` and the `txid`/`synctxid` state.

3. Existing Case 115 restart/retirement deepening.
   - [`115-hadoop-241-snapshot-restart-retirement-deepening.md`](115-hadoop-241-snapshot-restart-retirement-deepening.md)

4. Existing Case 115 edit-log replay deepening.
   - [`115-hadoop-241-snapshot-editlog-replay-deepening.md`](115-hadoop-241-snapshot-editlog-replay-deepening.md)

5. Canonical Case 115.
   - [`../cases/115-apache-hdfs-snapshot-shared-block-replication.md`](../cases/115-apache-hdfs-snapshot-shared-block-replication.md)
