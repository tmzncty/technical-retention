# Case 115 deepening — Hadoop 2.4.1 snapshot checkpoint/restart and block-retirement path

## Scope

This record deepens **Case 115 — Apache HDFS Snapshots** with one bounded question in the exact Apache Hadoop **`release-2.4.1`** source tree:

> After a snapshot is the remaining namespace relation that keeps an old file state reachable, what does the released implementation/test suite establish about surviving a NameNode checkpoint/restart, and what staged path begins when the final snapshot/reference relation is retired and blocks become collectable?

This slice is intentionally narrower than a general HDFS restart, deletion, garbage-collection, or media-sanitization history. It establishes one explicit `saveNamespace` + NameNode restart regression path and one NameNode-to-DataNode invalidation path. It does **not** establish arbitrary crash timing, every edit-log replay edge case, HA failover semantics, local-filesystem block reuse, device remapping, physical overwrite, or secure sanitization.

## Source pin

Apache's annotated Git tag `release-2.4.1` points to tag object `a5ffd153f61c68ae6f62a2f30fac59687c9b0dbd`, created **30 June 2014**, which in turn points to commit:

`1b5c6b3a3b90c6e396e00e991b49d170eb2dac55`

All source-code claims below are bounded to that tagged commit unless otherwise stated.

## Primary sources

### P1 — Apache Hadoop 2.4.1 snapshot documentation

- Apache Hadoop 2.4.1, **HDFS Snapshots**, last published **21 June 2014**.
- <https://hadoop.apache.org/docs/r2.4.1/hadoop-project-dist/hadoop-hdfs/HdfsSnapshots.html>

Relevant statements: snapshots are read-only point-in-time copies; creation is O(1) apart from inode lookup; **DataNode blocks are not copied**; snapshot files retain block lists and file sizes while modifications are recorded relative to current state.

### P2 — `TestSnapshotBlocksMap.java` at the 2.4.1 tagged commit

- <https://github.com/apache/hadoop/blob/1b5c6b3a3b90c6e396e00e991b49d170eb2dac55/hadoop-hdfs-project/hadoop-hdfs/src/test/java/org/apache/hadoop/hdfs/server/namenode/snapshot/TestSnapshotBlocksMap.java>

Relevant regression paths:

- `testDeletionWithSnapshots` checks that deleting the current file does not remove its blocks from the block map while a snapshot still retains that file, and that deleting a newer snapshot still leaves blocks when an older snapshot retains the file.
- `testReadSnapshotFileWithCheckpoint` creates a snapshot, deletes the current file, explicitly enters safe mode, calls `saveNamespace`, leaves safe mode, restarts the NameNode, and then reads the snapshot path. The source comment says the restart is intended to load snapshot files from fsimage.
- `testReadRenamedSnapshotFileWithCheckpoint` exercises the same checkpoint/restart pattern after rename/snapshot operations and reads historical snapshot paths after restart.

These tests are especially valuable because they establish an executable project regression boundary rather than merely documenting intended snapshot semantics.

### P3 — `FSNamesystem.java`

- <https://github.com/apache/hadoop/blob/1b5c6b3a3b90c6e396e00e991b49d170eb2dac55/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.java>

In the snapshot-delete path, `snapshotManager.deleteSnapshot(...)` receives `collectedBlocks`. After edit-log synchronization, `FSNamesystem` invokes `removeBlocks(collectedBlocks)` and clears the collection. `removeBlocks(...)` incrementally delegates each collected block to `blockManager.removeBlock(...)`.

### P4 — `BlockManager.java`

- <https://github.com/apache/hadoop/blob/1b5c6b3a3b90c6e396e00e991b49d170eb2dac55/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/BlockManager.java>

`removeBlock(Block block)` marks the block with `BlockCommand.NO_ACK`, calls `addToInvalidates(block)`, removes corrupt-replica bookkeeping, removes the block from `blocksMap`, and removes it from pending/needed replication structures. The internal invalidation step enumerates storages/DataNodes that hold the block and queues invalidation work.

### P5 — `InvalidateBlocks.java`

- <https://github.com/apache/hadoop/blob/1b5c6b3a3b90c6e396e00e991b49d170eb2dac55/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/InvalidateBlocks.java>

The invalidation structure keeps blocks associated with DataNodes and `invalidateWork(...)` moves a bounded batch onto the `DatanodeDescriptor` with `dn.addBlocksToBeInvalidated(...)`. This is queued/scheduled work rather than evidence that media has already been erased.

### P6 — `DatanodeManager.java`

- <https://github.com/apache/hadoop/blob/1b5c6b3a3b90c6e396e00e991b49d170eb2dac55/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/DatanodeManager.java>

The heartbeat-response path retrieves `nodeinfo.getInvalidateBlocks(blockInvalidateLimit)` and, when blocks are available, sends a `BlockCommand` with `DatanodeProtocol.DNA_INVALIDATE` for that block pool and bounded block list.

### P7 — `BPOfferService.java`

- <https://github.com/apache/hadoop/blob/1b5c6b3a3b90c6e396e00e991b49d170eb2dac55/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/BPOfferService.java>

When the DataNode receives `DNA_INVALIDATE`, the source describes the local blocks as obsolete and safe to garbage-collect, removes them from block-scanner tracking when applicable, and calls `dn.getFSDataset().invalidate(blockPoolId, toDelete)`, then increments the blocks-removed metric.

## Historical record

### H/P — a snapshot-only historical file is exercised across explicit `saveNamespace` checkpoint + NameNode restart

The `release-2.4.1` regression suite does not merely create/read a snapshot in one NameNode process. `testReadSnapshotFileWithCheckpoint` performs this bounded sequence:

```text
create current file
  -> create snapshot
  -> delete current file
  -> enter safe mode
  -> saveNamespace
  -> leave safe mode
  -> restart NameNode
  -> read the file through the snapshot path
```

The test comment states that the restart loads snapshot files from fsimage. A sibling test covers historical snapshot paths after rename/snapshot operations through the same checkpoint/restart pattern.

Therefore this release supplies direct project evidence for:

> **snapshot-retained namespace/reference state can survive an explicit namespace checkpoint and NameNode restart while continuing to make the historical file readable.**

This is stronger than a source-only reconstruction of snapshot metadata classes, but narrower than a claim about every restart/failure path.

### H/P — retained snapshot references delay block collection

`testDeletionWithSnapshots` directly checks that blocks remain in the NameNode block map after the current file is deleted while snapshot state still retains the file. Deleting one snapshot also does not collect blocks when another snapshot remains authoritative for that historical file.

The historical implementation therefore distinguishes:

```text
current pathname gone
        !=
all historical references gone
        !=
block collectable
```

### H/P — when snapshot deletion yields collectable blocks, retirement proceeds through NameNode block management and queued DataNode invalidation

The source chain is explicit in the same release:

```text
snapshotManager.deleteSnapshot(..., collectedBlocks, ...)
        ->
FSNamesystem.removeBlocks(collectedBlocks)
        ->
BlockManager.removeBlock(block)
        ->
addToInvalidates(block)
        ->
InvalidateBlocks / DatanodeDescriptor queue
        ->
heartbeat response: DNA_INVALIDATE
        ->
DataNode BPOfferService
        ->
FSDataset.invalidate(...)
```

This chain supplies a released implementation record for staged block retirement once namespace/snapshot reclamation identifies blocks that no longer need to be retained.

## Engineering reconstruction

### E — checkpoint survival and physical block duplication are different relations

The snapshot regression proves that the historical namespace/reference structure remains usable across the explicit checkpoint/restart path. P1 independently says DataNode blocks are not copied for snapshots.

Therefore:

> **checkpoint-surviving snapshot authority != newly copied snapshot payload embodiment.**

The historical view can survive because retained namespace/diff/block-reference state is serialized/reconstituted while the same distributed block identities continue to provide payload.

### E — NameNode retirement and DataNode deletion are separate stages

Once the final retaining relation disappears, the NameNode can retire the block from its authoritative management structures and enqueue invalidations. That is not the same instant as the DataNode receiving and executing `DNA_INVALIDATE`.

Therefore:

> **last-reference retirement != immediate DataNode invalidation completion.**

and:

> **NameNode block-map retirement != DataNode local deletion completion.**

The invalidation queue and heartbeat-carried command make the asynchronous boundary concrete.

### E — command dispatch is still not media sanitization

`BPOfferService` ultimately calls the DataNode dataset's `invalidate(...)`. This establishes a local HDFS storage-management operation, not a proof that every underlying sector has been overwritten or cryptographically/media-sanitized.

The remaining lower layers are deliberately outside this slice:

```text
FSDataset.invalidate
  -> local filesystem unlink/free-space behavior
  -> later allocation/reuse
  -> block-device translation/remapping/cache behavior
  -> magnetic/flash physical remanence or sanitize operation
```

Thus:

> **`DNA_INVALIDATE` dispatch != demonstrated physical overwrite/sanitization.**

and:

> **namespace/block-management invisibility != physical erasure.**

### E — persistence and reclamation can have different temporal shapes

The bounded checkpoint test demonstrates a retained reference relation surviving a NameNode restart. The retirement path, by contrast, explicitly uses queued and heartbeat-mediated work.

This supports a useful cross-layer distinction:

> **retention authority can survive restart while later physical reclamation remains staged and asynchronous.**

The statement is about the inspected 2.4.1 mechanism, not a universal property of distributed storage.

## Explicit stop conditions

This evidence does **not** establish:

1. arbitrary power-loss/crash persistence at every point between snapshot edits and checkpoint;
2. every edit-log replay ordering or corruption case;
3. NameNode HA active/standby failover semantics;
4. that `saveNamespace` is required for all normal HDFS restart recovery;
5. that snapshot creation makes a second DataNode block copy;
6. that removing one current pathname makes a still-snapshotted block collectable;
7. that `BlockManager.removeBlock` means the DataNode has already deleted the block;
8. that `DNA_INVALIDATE` delivery/execution is synchronous with namespace deletion;
9. that `FSDataset.invalidate` proves filesystem overwrite, device erase, TRIM/Sanitize, or forensic irrecoverability;
10. that this exact 2.4.1 path is unchanged in later Hadoop releases.

In particular:

> **`saveNamespace + restart` regression != arbitrary crash/edit-log-replay proof.**

and:

> **logical retirement != secure physical sanitization.**

## Cross-case comparison

### Case 04 — mapped Flash

At a bounded functional level, Case 04 and this HDFS slice both separate **loss of logical/current authority** from **later reclamation of an old physical embodiment**. But their mechanisms are not the same:

- HDFS snapshot/current namespace references and NameNode block management determine whether distributed block identities remain live;
- mapped Flash uses logical-to-physical mapping/currentness plus erase-block reclamation inside a different storage stack.

So:

> **deferred reclamation is a functional analogy, not evidence of HDFS↔FTL genealogy or implementation identity.**

### Case 02 — magnetic-core sanitization

Case 02's security-erasure deepening supplies another bounded boundary: changing ordinary system authority/current value is not by itself proof of stronger reconstruction-resistant purging. Case 115 now supplies a distributed-storage instance in which namespace/reference retirement, DataNode invalidation, and physical sanitization are visibly different stages.

No physical mechanism identity is implied.

## Philosophical / media-theoretical interpretation

`I` — A retained past can outlive present namespace reachability because a separate historical reference relation continues to authorize shared embodiments. When the final legitimating relation is withdrawn, loss of authority and destruction/reuse of embodiment still need not be one event.

This is a project interpretation of the bounded mechanism. HDFS is not being anthropomorphized as human remembering/forgetting, and the source record is not rewritten into philosophical vocabulary.

## Related-repository boundary

A fresh search of `tmzncty/computing-archaeology` found no dedicated HDFS snapshot/checkpoint/block-invalidation study to reuse. The wider history of HDFS namespace persistence, edit-log/checkpoint evolution, DataNode storage layout, deletion implementation across releases, and distributed-filesystem snapshot genealogy belongs there if pursued. This repository keeps only the retention-specific relation established above.
