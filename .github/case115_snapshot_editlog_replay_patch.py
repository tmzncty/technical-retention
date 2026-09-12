from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"anchor missing in {path}: {old[:180]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


def append_once(path: str, required_marker: str, addition: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if required_marker not in text:
        raise SystemExit(f"required marker missing in {path}: {required_marker!r}")
    if addition.strip() in text:
        raise SystemExit(f"addition already present in {path}")
    p.write_text(text.rstrip() + "\n\n" + addition.strip() + "\n", encoding="utf-8")


baseline = "a3057d5f3798fc48eefd0b648c95c76542d178c9"
evidence_path = Path("evidence/115-hadoop-241-snapshot-editlog-replay-deepening.md")
case_path = Path("cases/115-apache-hdfs-snapshot-shared-block-replication.md")
roadmap_path = Path("ROADMAP.md")
index_path = Path("CASE_INDEX.md")

if evidence_path.exists():
    raise SystemExit("Case 115 edit-log replay evidence already exists")
if "### Findings 3812–3827" in index_path.read_text(encoding="utf-8"):
    raise SystemExit("CASE_INDEX findings already present")
if "Case 115 HDFS snapshot normal edit-log replay deepening" in roadmap_path.read_text(encoding="utf-8"):
    raise SystemExit("ROADMAP item already present")


evidence_path.write_text(r'''# Evidence 115C — Hadoop 2.4.1 Snapshot Edit-Log Replay and NameNode-Restart Reconstruction

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
''', encoding="utf-8")

old_debt = "Still open: arbitrary crash/edit-log replay and HA-failover semantics for snapshots; lower `FSDataset`/filesystem reuse behavior; block-device remapping/discard/sanitize composition; fault-injected timing between retirement, invalidation dispatch, DataNode execution, and restart; and evolution of this path across later Hadoop releases. Broader HDFS persistence/deletion history remains a `computing-archaeology` task."
new_debt = "Still open: arbitrary-crash / torn-or-corrupt-edit-log recovery and HA-failover semantics for snapshots; lower `FSDataset`/filesystem reuse behavior; block-device remapping/discard/sanitize composition; fault-injected timing between retirement, invalidation dispatch, DataNode execution, and restart; and evolution of this path across later Hadoop releases. Normal non-format NameNode restart with snapshot edit-log application is now grounded separately below. Broader HDFS persistence/deletion history remains a `computing-archaeology` task."
replace_once(str(case_path), old_debt, new_debt)

case_anchor = "\n\n## Prior art and genealogy boundary"
case_section = r'''

## Normal edit-log replay deepening — Hadoop 2.4.1

The companion evidence record [`evidence/115-hadoop-241-snapshot-editlog-replay-deepening.md`](../evidence/115-hadoop-241-snapshot-editlog-replay-deepening.md) closes the **normal NameNode-restart replay** part of the earlier persistence debt without turning the case into a general crash-consistency claim.

### H/P — snapshot lifecycle operations are explicit edit-log operations with explicit replay handlers

In `release-2.4.1`, `FSEditLog` serializes `CreateSnapshotOp`, `DeleteSnapshotOp`, and `RenameSnapshotOp`; `FSEditLogLoader` contains matching `OP_CREATE_SNAPSHOT`, `OP_DELETE_SNAPSHOT`, and `OP_RENAME_SNAPSHOT` branches that apply the operations through `SnapshotManager`.

This supplies a released implementation path:

```text
snapshot namespace transition
    -> snapshot-specific edit-log operation
    -> later loader replay
    -> reconstructed snapshot namespace relation
```

The edit record is control/history state. It is not another copy of the DataNode block payload.

### H/P — the released regression separates edit-log replay from later fsimage loading

`TestSnapshot.checkFSImage()` says it restarts the cluster to check **edit log applying and fsimage saving/loading**. It first shuts down and restarts `MiniDFSCluster` with `format(false)`, dumps a middle namespace tree specifically to check that the edit log is applied correctly, and compares that tree with the pre-restart tree. Only afterward does it call `saveNamespace()` and perform a second non-format restart to check the fsimage-loaded tree.

Therefore the bounded release test supports:

> **snapshot namespace authority can survive ordinary NameNode process restart through edit-log application, not only through a prior explicit `saveNamespace` checkpoint.**

### H/P + E — successful createSnapshot crosses an HDFS edit-log sync boundary before return

The inspected `FSNamesystem.createSnapshot(...)` path mutates the snapshot manager, calls `logCreateSnapshot(...)`, leaves the write-lock block, then calls `getEditLog().logSync()` before the method returns the snapshot path.

The safe conclusion is exact and software-layered:

> **successful create return != merely unsynchronized in-process snapshot state.**

But:

> **HDFS `logSync()` boundary != universal proof of lower-media durability under every hardware fault.**

### Engineering reconstruction

Together with the existing 2.4.1 documentation that DataNode blocks are not copied for snapshots, the replay path demonstrates a useful control/payload decomposition:

```text
retained namespace/edit history
    + shared block identities
    + surviving DataNode replicas
    -> reconstructed historical snapshot view after NameNode restart
```

Hence:

> **NameNode process-memory loss != snapshot-relation loss.**

> **snapshot edit-log replay != snapshot payload duplication.**

> **reconstructed namespace relation != proof that every DataNode replica is healthy.**

### Remaining boundary

The released test uses orderly shutdown and ordinary restart. It does not inject failures at every edit-log write/sync instruction, prove torn/corrupt-log recovery, or exercise active/standby shared-edits failover. The new evidence therefore narrows the old debt rather than erasing it:

> **normal restart replay != arbitrary crash/torn-log recovery != HA failover.**
'''
replace_once(str(case_path), case_anchor, case_section + case_anchor)

roadmap_anchor = "## Phase 2 — Build missing technical bridges\n\n"
roadmap_item = """- [x] **Case 115 HDFS snapshot normal edit-log replay deepening:** [`cases/115-apache-hdfs-snapshot-shared-block-replication.md`](cases/115-apache-hdfs-snapshot-shared-block-replication.md) + [`evidence/115-hadoop-241-snapshot-editlog-replay-deepening.md`](evidence/115-hadoop-241-snapshot-editlog-replay-deepening.md) ground the ordinary NameNode-restart path that Evidence 115B intentionally left open. Hadoop `release-2.4.1` has explicit create/delete/rename snapshot edit-log operations, matching loader replay branches, and a `TestSnapshot.checkFSImage()` sequence whose first `format(false)` restart is explicitly used to check that the edit log is applied correctly before a later `saveNamespace` + fsimage restart. The exact successful `createSnapshot` path also calls `logCreateSnapshot` then `logSync` before returning. This closes `NameNode process-memory loss != snapshot-relation loss` for normal replay and fixes `snapshot edit-log replay != payload duplication`; arbitrary crash/torn-log recovery, HA/shared-edits failover, delete/rename completion-sync details, lease/open-file interactions, and lower-media durability remain open. Broader journaling/replay genealogy belongs primarily in `computing-archaeology`.\n\n"""
replace_once(str(roadmap_path), roadmap_anchor, roadmap_anchor + roadmap_item)

findings = r'''### Findings 3812–3827 — Case 115 HDFS snapshot normal edit-log replay boundary

- **3812 — H/P** — Apache Hadoop `release-2.4.1` `FSEditLog.logCreateSnapshot(...)` constructs `CreateSnapshotOp` and submits it through `logEdit(op)`, making snapshot creation an explicit edit-log state transition.
- **3813 — H/P** — The same release has `logDeleteSnapshot(...)` backed by `DeleteSnapshotOp` plus `logEdit(op)`, rather than treating snapshot deletion as an unlogged in-memory-only change.
- **3814 — H/P** — The same release has `logRenameSnapshot(...)` backed by `RenameSnapshotOp` plus `logEdit(op)`, making historical-name change explicit in the edit stream.
- **3815 — H/P** — `FSEditLogLoader` handles `OP_CREATE_SNAPSHOT` by invoking `SnapshotManager.createSnapshot(...)`, so the create opcode participates in namespace reconstruction.
- **3816 — H/P** — `FSEditLogLoader` handles `OP_DELETE_SNAPSHOT` by invoking `SnapshotManager.deleteSnapshot(...)` and then processing collected blocks / removed inodes, preserving the distinction between replayed namespace retirement and later lower-media erasure.
- **3817 — H/P** — `FSEditLogLoader` handles `OP_RENAME_SNAPSHOT` by invoking `SnapshotManager.renameSnapshot(...)`, pairing the serialized rename with an explicit replay path.
- **3818 — H/P** — `TestSnapshot.checkFSImage()` explicitly says it restarts the cluster to check edit-log application and fsimage saving/loading; its first `format(false)` restart occurs before `saveNamespace()` and its middle tree is later compared to verify that edit-log application preserved the snapshot-bearing namespace tree.
- **3819 — E** — `NameNode process-memory loss != snapshot-relation loss`: persisted namespace/edit history can be replayed to reconstruct the relation that keeps shared HDFS blocks historically reachable.
- **3820 — E** — `snapshot edit-log replay != snapshot payload duplication`; the replayed state is namespace/control history, while released HDFS snapshot documentation separately says DataNode blocks are not copied for snapshots.
- **3821 — H/P** — In the inspected `release-2.4.1` successful `FSNamesystem.createSnapshot(...)` path, the NameNode logs the create operation and calls `getEditLog().logSync()` before returning the snapshot path.
- **3822 — E/X** — Crossing that exact HDFS `logSync()` boundary is stronger than merely retaining unsynchronized Java-object state but is not promoted into a universal physical-media durability guarantee across every filesystem, controller, device cache, power fault, or correlated failure.
- **3823 — X** — The released non-format restart regression uses orderly shutdown; `normal restart + edit-log application != arbitrary crash / torn-or-corrupt-log recovery proof`.
- **3824 — X** — The inspected restart does not establish active/standby, JournalNode quorum, shared-edits fencing, or other HA failover behavior; `single-NameNode restart replay != HA semantics`.
- **3825 — E** — Reconstructed snapshot namespace authority still depends on surviving DataNode block replicas for payload; edit replay can restore naming/currentness relations without proving every replica healthy or correctly placed.
- **3826 — E/X** — Replayed snapshot deletion can retire namespace/reference state and trigger block-collection logic, but it does not prove immediate filesystem reuse, media overwrite, discard completion, sanitization, or forensic non-recoverability.
- **3827 — X** — Hadoop 2.4.1 supplies a bounded released implementation/replay witness only; no claim is made that HDFS invented snapshots, edit logging, replay, copy-on-write retention, or namespace checkpointing.'''
append_once(str(index_path), "**3811 — X**", findings)

for p in [case_path, evidence_path, roadmap_path, index_path]:
    text = p.read_text(encoding="utf-8")
    if "\t" in text:
        raise SystemExit(f"tab found in {p}")

print(f"Case 115 snapshot edit-log replay patch applied on expected baseline {baseline}")
