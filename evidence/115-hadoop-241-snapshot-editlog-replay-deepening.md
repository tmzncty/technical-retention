# Evidence 115C — Hadoop 2.4.1 Snapshot Edit-Log Replay and NameNode-Restart Reconstruction

## Scope

This note deepens [`../cases/115-apache-hdfs-snapshot-shared-block-replication.md`](../cases/115-apache-hdfs-snapshot-shared-block-replication.md) around one deliberately narrow question left open by Evidence 115B:

> In Apache Hadoop `release-2.4.1`, is snapshot namespace state merely able to survive an explicit `saveNamespace` checkpoint, or is there direct released-source evidence that snapshot create/delete/rename relations are represented in the edit log and reconstructed across an ordinary non-format NameNode restart?

The answer is bounded but strong:

1. `FSEditLog` has dedicated create/delete/rename snapshot edit operations;
2. `FSEditLogLoader` has corresponding replay cases that call the snapshot manager;
3. `TestSnapshot.checkFSImage()` explicitly performs a first `format(false)` restart to check edit-log application before it performs `saveNamespace` and a second restart to check fsimage loading;
4. the exact `FSNamesystem.createSnapshot(...)` path in this release logs the create operation and then calls `logSync()` before the successful call returns.

This closes **normal NameNode-restart edit-log reconstruction** for the inspected release. It does **not** establish arbitrary crash behavior at every instruction point, torn/corrupt edit-log recovery, JournalNode/shared-edits HA failover, lower-device write-cache durability, or a snapshot payload copy.

The annotated `release-2.4.1` tag resolves to Apache Hadoop commit `1b5c6b3a3b90c6e396e00e991b49d170eb2dac55`. All implementation claims below are version-bounded to that tree.

---

## Primary sources

### P1 — Apache Hadoop `release-2.4.1` tag — `H/P`

- tag ref: <https://github.com/apache/hadoop/releases/tag/release-2.4.1>
- tagged tree used here: <https://github.com/apache/hadoop/tree/release-2.4.1>
- resolved commit: `1b5c6b3a3b90c6e396e00e991b49d170eb2dac55`

This is a released-project implementation witness, not an invention-priority claim.

### P2 — `FSEditLog.java` — `H/P`

<https://github.com/apache/hadoop/blob/release-2.4.1/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSEditLog.java>

The released source defines snapshot-specific logging methods:

- `logCreateSnapshot(...)` constructs `CreateSnapshotOp` and calls `logEdit(op)`;
- `logDeleteSnapshot(...)` constructs `DeleteSnapshotOp`, records RPC IDs when requested, and calls `logEdit(op)`;
- `logRenameSnapshot(...)` constructs `RenameSnapshotOp`, records RPC IDs when requested, and calls `logEdit(op)`.

The historical claim is only that these snapshot namespace transitions have explicit edit-log representations in this release.

### P3 — `FSEditLogLoader.java` — `H/P`

<https://github.com/apache/hadoop/blob/release-2.4.1/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSEditLogLoader.java>

The loader contains explicit cases for:

- `OP_CREATE_SNAPSHOT`, which invokes `SnapshotManager.createSnapshot(...)`;
- `OP_DELETE_SNAPSHOT`, which invokes `SnapshotManager.deleteSnapshot(...)`, then handles collected blocks and removed inodes;
- `OP_RENAME_SNAPSHOT`, which invokes `SnapshotManager.renameSnapshot(...)`.

Thus the edit representation is paired with replay logic; this is not merely an opcode vocabulary that is never consumed.

### P4 — `TestSnapshot.java` — `H/P`

<https://github.com/apache/hadoop/blob/release-2.4.1/hadoop-hdfs-project/hadoop-hdfs/src/test/java/org/apache/hadoop/hdfs/server/namenode/snapshot/TestSnapshot.java>

`checkFSImage()` is documented in the test itself as restarting the cluster to check **edit-log applying and fsimage saving/loading**. Its sequence is especially useful because it separates two persistence paths:

1. dump the namespace tree;
2. shut down the cluster;
3. start `MiniDFSCluster` with `format(false)`;
4. dump a middle tree, with the source comment saying it will later check whether the edit log is applied correctly;
5. then enter safe mode, call `saveNamespace()`, leave safe mode;
6. restart with `format(false)` again;
7. dump the fsimage-loaded tree;
8. compare both restarted trees with the pre-restart tree.

This test is stronger than an inference from the loader source alone: the released regression suite deliberately checks both the edit-log-applied restart and the later fsimage-loaded restart.

### P5 — `FSNamesystem.java` create-snapshot completion path — `H/P`

<https://github.com/apache/hadoop/blob/release-2.4.1/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.java>

In the inspected `createSnapshot(...)` path, after `snapshotManager.createSnapshot(...)` the NameNode calls `getEditLog().logCreateSnapshot(...)`; after leaving the write-lock block it calls `getEditLog().logSync()` before the method completes and returns the snapshot path.

The precise historical statement is therefore:

> in this release's successful create-snapshot path, the operation crosses the HDFS edit-log `logSync()` boundary before the API call returns.

That statement is intentionally narrower than `the bits are physically durable against every possible storage/power failure`.

### P6 — Hadoop 2.4.1 snapshot documentation — `H/P`

<https://hadoop.apache.org/docs/r2.4.1/hadoop-project-dist/hadoop-hdfs/HdfsSnapshots.html>

The released documentation independently states that snapshot creation does not copy DataNode blocks. That existing Case-115 fact is essential for interpreting edit-log persistence correctly: the edit log is retaining/reconstructing namespace authority over shared block identities, not serializing another copy of the block payload.

---

## Historical record

### H/P — snapshot create/delete/rename are explicit edit-log state transitions

The three dedicated `FSEditLog` methods show that snapshot lifecycle operations are first-class namespace edits in `release-2.4.1`.

This matters because the retention relation is not confined to transient `SnapshotManager` process memory:

```text
snapshot namespace operation
    -> dedicated edit-log op
    -> persisted namespace-history stream
```

The source does not imply that every internal cache or Java object is serialized. It shows that enough operation-level state exists in the edit stream to reconstruct the corresponding namespace transition.

### H/P — the edit-log loader replays those transitions through SnapshotManager

`FSEditLogLoader` maps the opcodes back into snapshot-manager operations. Create and rename reconstruct the corresponding snapshot namespace relations. Delete also computes block/inode retirement effects and removes collected state through the NameNode's replay path.

Therefore, for the inspected release:

> **snapshot edit-log representation != inert audit record.**

It participates in rebuilding current NameNode namespace state.

### H/P — the released snapshot regression deliberately checks edit-log application before fsimage checkpoint loading

`TestSnapshot.checkFSImage()` first restarts the cluster with `format(false)` *before* calling `saveNamespace()`. The source comment explicitly says the middle dump is later checked to see whether the edit log is applied correctly. Only after that first restart does the test checkpoint the namespace and perform the second restart used to check fsimage loading.

The two comparisons therefore establish two separate bounded released-test witnesses:

```text
pre-restart snapshot namespace tree
    == ordinary non-format restart tree after edit-log application

pre-checkpoint snapshot namespace tree
    == later tree loaded after saveNamespace + restart
```

This sharpens Evidence 115B. Snapshot persistence is not demonstrated only by an explicit namespace checkpoint.

### H/P — successful createSnapshot crosses `logSync()` before returning

The exact 2.4.1 create path logs the snapshot operation and then invokes `logSync()` before returning the created snapshot path.

This matters for completion semantics:

```text
snapshot manager mutation
    -> logCreateSnapshot
    -> logSync
    -> successful createSnapshot return
```

But the scope must remain exact. This note does not claim that delete/rename have identical completion details without separately grounding those call paths, nor that HDFS `logSync()` is equivalent to a verified flush through every controller, device cache, remapping layer, and correlated-failure scenario.

---

## Engineering reconstruction

### E — NameNode process-memory loss need not erase snapshot retention authority

The edit-log representation plus loader replay supports the following bounded reconstruction:

```text
live NameNode objects disappear at process restart
        !=
snapshot relation disappears

because

retained FSImage/edit-log namespace state
        -> replay / load
        -> reconstructed snapshot namespace relation
```

The relation that makes historical block identities admissible can therefore outlive the Java objects that previously embodied it.

This is a control-state persistence claim, not payload duplication.

### E — a small retained control history can re-establish authority over much larger payload state

HDFS snapshot documentation says DataNode blocks are not copied at snapshot creation. Combined with edit-log replay, the bounded mechanism is:

```text
small namespace/history record
    + existing shared block identities
    + surviving DataNode replicas
    -> reconstructed historical snapshot view
```

The edit-log entries do not contain the block payload. They preserve enough namespace transition history for the NameNode to reconstitute which shared payload remains reachable and therefore still subject to HDFS retention/replication obligations.

Hence:

> **snapshot metadata durability != snapshot payload duplication.**

### E — persisted relation and available payload remain separate failure dimensions

Successful edit replay can rebuild a snapshot path while a needed DataNode block is missing, corrupt, or under-replicated. Conversely, residual block replicas can remain on storage while the namespace relation that made them an admissible snapshot has been lost.

So:

```text
namespace relation reconstructed
    !=
every payload replica healthy
```

and:

```text
payload bits still present somewhere
    !=
usable snapshot namespace reconstructed
```

Case 80 and Case 83 remain the dedicated HDFS placement and integrity comparisons.

### E — create completion has a named software durability boundary, not an unlimited physical guarantee

Because the exact create path calls `logSync()` before returning, Case 115 can distinguish:

```text
operation merely present in in-memory SnapshotManager state
    !=
operation has crossed HDFS edit-log sync boundary
```

But the repository should not silently upgrade that software boundary into a hardware-level theorem. Device volatile caches, filesystem/journal semantics, storage faults, corrupted/torn edit segments, and multi-node HA journal behavior require their own evidence.

---

## Functional comparison only

### A/E — ZFS / other reference-retention cases

Case 99 and Case 129 also preserve relatively small metadata/reference relations that keep much larger storage state meaningful across time. The useful analogy is only:

> **retained authority/currentness metadata can be constitutive of payload retention.**

HDFS edit-log opcodes, ZFS on-disk structures, and their crash/replay protocols are not asserted to share an implementation or genealogy.

### A/E — RADOS and repair-control cases

Case 05 shows that distributed payload availability depends on retained control/version/placement state as well as raw replicas. The comparison is functional only. An HDFS snapshot edit op is not a RADOS PG log entry and does not establish shared ancestry.

---

## Explicit exclusions

### X — normal restart replay is not arbitrary-crash proof

The released test performs orderly cluster shutdown and non-format restart. It does not inject power loss between individual edit-log writes, truncate an edit at every byte, corrupt checksums, or exhaustively test recovery at each `logSync()` substep.

Therefore:

> **normal restart + edit-log application != arbitrary crash / torn-log recovery proof.**

### X — the test is not an HA/shared-edits failover proof

The inspected `MiniDFSCluster` restart does not by itself establish active/standby failover, JournalNode quorum behavior, observer lag, shared-edits fencing, or split-brain recovery.

Therefore:

> **single-NameNode restart replay != HA failover semantics.**

### X — `logSync()` is not promoted into universal physical-media durability

The source gives a software synchronization boundary. This note does not claim verified persistence through every filesystem, host cache, RAID controller, SSD volatile cache, FTL remap, power-loss event, or correlated failure.

### X — edit replay does not create another DataNode block population

The 2.4.1 snapshot documentation explicitly says DataNode blocks are not copied for snapshots. Reconstructing snapshot namespace state after restart therefore must not be described as restoring an independent snapshot payload copy.

### X — replayed deletion is not secure erasure

`OP_DELETE_SNAPSHOT` replay may retire namespace relations and make blocks collectable through the already-grounded retirement path. It does not prove that the corresponding lower filesystem extents or device media were immediately overwritten, discarded, sanitized, or rendered forensically irrecoverable.

### X — this is not an HDFS-first or snapshot-first claim

The source establishes a released Hadoop 2.4.1 implementation boundary. Existing Case 115 prior-art notes already keep older filesystem snapshot genealogy separate. Nothing here claims that Apache invented edit logging, snapshots, copy-on-write retention, or replay-based namespace recovery.

---

## What this closes and what remains open

This slice closes one previously explicit Case-115 debt:

- **closed:** ordinary `release-2.4.1` NameNode restart reconstruction through explicit snapshot create/delete/rename edit-log operations plus corresponding loader replay;
- **closed:** a released regression that intentionally checks edit-log application before the later fsimage checkpoint/restart check;
- **closed, exact-operation only:** successful create-snapshot completion crosses `logCreateSnapshot` + `logSync()` before returning.

Still open:

- arbitrary crash / power-loss injection around edit serialization and `logSync()`;
- torn, truncated, corrupt, duplicated, or partially recovered edit-log behavior;
- HA active/standby failover and shared-edits / JournalNode semantics;
- exact delete/rename API completion-sync boundaries if needed;
- snapshotted-open files, lease recovery, and degraded-replica interactions;
- later-version evolution of the snapshot edit/replay path;
- lower filesystem/device persistence, discard, overwrite, and sanitization composition.

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated HDFS snapshot/edit-log module to reuse. Broader journaling, WAL/replay, namespace-checkpoint, and filesystem-snapshot genealogy belongs there rather than being rebuilt in this case.
