from pathlib import Path
import re

ROOT = Path('.')
CASE = ROOT / 'cases/115-apache-hdfs-snapshot-shared-block-replication.md'
EVIDENCE = ROOT / 'evidence/115-hadoop-241-snapshot-restart-retirement-deepening.md'
ROADMAP = ROOT / 'ROADMAP.md'
INDEX = ROOT / 'CASE_INDEX.md'

EVIDENCE_TEXT = r'''# Case 115 deepening — Hadoop 2.4.1 snapshot checkpoint/restart and block-retirement path

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
'''

CASE_SECTION = r'''## Checkpoint/restart and block-retirement deepening — Hadoop 2.4.1

The companion evidence record [`evidence/115-hadoop-241-snapshot-restart-retirement-deepening.md`](../evidence/115-hadoop-241-snapshot-restart-retirement-deepening.md) closes two bounded implementation seams without turning this case into a generic HDFS lifecycle study.

### H/P — explicit checkpoint/restart regression

`release-2.4.1` `TestSnapshotBlocksMap.testReadSnapshotFileWithCheckpoint` creates a file and snapshot, deletes the current file, enters safe mode, calls `saveNamespace`, leaves safe mode, restarts the NameNode, and then reads the file through the snapshot path. The neighboring renamed-snapshot regression repeats the checkpoint/restart boundary across historical aliases.

This establishes only the inspected path:

> **snapshot-retained historical reachability can survive an explicit namespace checkpoint and NameNode restart.**

It does not establish every crash/edit-log replay ordering, HA failover, or later-release behavior. In particular:

> **`saveNamespace + restart` regression != arbitrary crash/edit-log-replay proof.**

Since the 2.4.1 snapshot documentation independently states that DataNode blocks are not copied, checkpoint survival also does not imply a new snapshot payload embodiment:

> **checkpoint-surviving snapshot authority != newly copied block embodiment.**

### H/P + E — final-reference retirement is a staged control path

The same release exposes a lower-layer sequence after snapshot deletion makes blocks collectable. `FSNamesystem` passes `collectedBlocks` to `removeBlocks(...)`; `BlockManager.removeBlock(...)` retires NameNode block-management state and queues invalidation; `InvalidateBlocks` moves bounded work to a DataNode descriptor; the heartbeat path sends `DNA_INVALIDATE`; and DataNode `BPOfferService` calls `FSDataset.invalidate(...)`.

The important separation is temporal and authoritative:

```text
last retaining namespace/snapshot relation disappears
        ->
block becomes collectable at NameNode layer
        ->
NameNode block-management retirement + invalidation queue
        ->
heartbeat-carried DNA_INVALIDATE
        ->
DataNode dataset invalidate
        ->
(lower filesystem/device reuse or sanitization not established here)
```

Therefore:

> **last-reference retirement != immediate DataNode invalidation completion.**

> **NameNode block-map retirement != DataNode local deletion completion.**

> **`DNA_INVALIDATE` / `FSDataset.invalidate` != demonstrated physical overwrite or secure sanitization.**

This refines the earlier `snapshot delete != block collection completion != physical sanitization` boundary with a released implementation path rather than collapsing the stages.

### Functional comparison only

Mapped Flash Case 04 also separates authority/currentness retirement from later reclamation, but HDFS namespace/block-management references are not an FTL mapping table and no genealogy is implied. Magnetic-core Case 02 separately shows why ordinary logical clearing/retirement should not be promoted into a stronger sanitization claim.

### Remaining bounded debt

Still open: arbitrary crash/edit-log replay and HA-failover semantics for snapshots; lower `FSDataset`/filesystem reuse behavior; block-device remapping/discard/sanitize composition; fault-injected timing between retirement, invalidation dispatch, DataNode execution, and restart; and evolution of this path across later Hadoop releases. Broader HDFS persistence/deletion history remains a `computing-archaeology` task.
'''

FINDINGS = r'''

## Case 115 deepening — HDFS snapshot checkpoint/restart and block-retirement findings

- **2770 — snapshot-only historical reachability can survive an explicit `saveNamespace` checkpoint + NameNode restart in Hadoop 2.4.1:** the released regression creates a snapshot, deletes the current file, checkpoints, restarts the NameNode, and reads the historical path. (`H/P`)
- **2771 — checkpoint-surviving snapshot authority != newly copied block embodiment:** Hadoop 2.4.1 documents that DataNode blocks are not copied for snapshots, so restart survival does not imply snapshot payload duplication. (`H/P`, `E`)
- **2772 — `saveNamespace + restart` regression != arbitrary crash/edit-log-replay proof:** the inspected test is an explicit orderly checkpoint/restart path and cannot certify every failure instant or journal edge case. (`H/P`, `X`)
- **2773 — current pathname deletion != last retaining reference deletion:** released snapshot block-map tests retain blocks after current-file deletion while a snapshot still references the historical file. (`H/P`)
- **2774 — deleting one snapshot != collectability when another snapshot still retains the file:** `testDeletionWithSnapshots` exercises multiple retained snapshot relations before block retirement. (`H/P`)
- **2775 — collectable-block discovery != DataNode deletion completion:** snapshot deletion can produce `collectedBlocks`, but `FSNamesystem` and `BlockManager` still perform later retirement/invalidation work. (`H/P`, `E`)
- **2776 — NameNode block-map retirement != DataNode local deletion completion:** `BlockManager.removeBlock` removes NameNode-side management state while separately queuing invalidation for holders. (`H/P`, `E`)
- **2777 — invalidation queue != invalidation execution:** `InvalidateBlocks` moves bounded work to a DataNode descriptor for later command delivery. (`H/P`, `E`)
- **2778 — heartbeat-carried `DNA_INVALIDATE` makes reclamation asynchronous at the inspected control boundary:** `DatanodeManager` attaches bounded invalidate commands to heartbeat responses rather than making namespace deletion itself the local erase operation. (`H/P`, `E`)
- **2779 — DataNode `FSDataset.invalidate` != demonstrated media overwrite/sanitization:** the released DataNode path establishes local HDFS dataset invalidation, not underlying filesystem/device erasure or forensic irrecoverability. (`H/P`, `E`, `X`)
- **2780 — namespace/block-management invisibility != physical erasure:** after authority is retired at upper layers, lower physical embodiments may pass through additional filesystem/device reclamation stages not established by this case. (`E`, `X`)
- **2781 — retention authority can survive restart while later reclamation remains staged:** the explicit checkpoint regression and queued invalidation path exhibit different temporal shapes inside the same bounded release. (`E`)
- **2782 — HDFS deferred reclamation ≈ mapped-Flash invalidation only functionally:** both separate current/reference authority from later reclamation, but HDFS snapshot references are not FTL mappings and no genealogy is implied. (`A`, `X`)
- **2783 — HDFS block retirement != security purge:** Case 02's clearing/purging boundary applies only as a relational warning; `DNA_INVALIDATE` cannot be promoted into a secure-sanitization claim without lower-layer evidence. (`A`, `X`)
- **2784 — broader HDFS checkpoint/deletion genealogy remains a related-repository task:** a fresh `computing-archaeology` search found no dedicated HDFS snapshot/checkpoint/invalidation study; edit-log evolution, filesystem/device deletion, and cross-release genealogy belong there if pursued. (`H/P` project-state record)
'''


def must_once(text: str, needle: str, label: str) -> None:
    n = text.count(needle)
    if n != 1:
        raise RuntimeError(f'{label}: expected exactly one occurrence, got {n}')

# Evidence file: fail rather than overwrite an independently-created record.
if EVIDENCE.exists():
    if EVIDENCE.read_text() != EVIDENCE_TEXT:
        raise RuntimeError(f'{EVIDENCE} already exists with different content')
else:
    EVIDENCE.write_text(EVIDENCE_TEXT)

# Deepen Case 115 in-place using stable semantic anchors.
case = CASE.read_text()
if '## Checkpoint/restart and block-retirement deepening — Hadoop 2.4.1' not in case:
    old_scope = '- a full account of NameNode FSImage/edit-log persistence for snapshots;'
    if old_scope in case:
        case = case.replace(
            old_scope,
            '- a full account of NameNode FSImage/edit-log persistence for snapshots beyond the bounded `saveNamespace` checkpoint + restart regression established below;',
            1,
        )
    old_lower = 'The exact post-snapshot-deletion sequence through block invalidation, DataNode deletion, filesystem free-space reuse, device remapping, and media overwrite is outside this bounded slice.'
    if old_lower in case:
        case = case.replace(
            old_lower,
            'The deepening below now establishes the Hadoop 2.4.1 NameNode block-retirement → queued invalidation → heartbeat `DNA_INVALIDATE` → DataNode `FSDataset.invalidate(...)` path. Filesystem free-space reuse, device remapping, media overwrite, and secure sanitization remain outside this bounded slice.',
            1,
        )
    anchor = '## Prior art and genealogy boundary'
    must_once(case, anchor, 'case insertion anchor')
    case = case.replace(anchor, CASE_SECTION + '\n\n' + anchor, 1)
CASE.write_text(case)

# Record completion in Phase 2 without depending on an exact neighboring case order.
road = ROADMAP.read_text()
road_entry = "- [x] Case 115 HDFS snapshot checkpoint/restart + block-retirement/invalidation deepening — [`cases/115-apache-hdfs-snapshot-shared-block-replication.md`](cases/115-apache-hdfs-snapshot-shared-block-replication.md), deepened by [`evidence/115-hadoop-241-snapshot-restart-retirement-deepening.md`](evidence/115-hadoop-241-snapshot-restart-retirement-deepening.md): Hadoop 2.4.1 regression tests ground snapshot-only historical reachability through an explicit `saveNamespace` checkpoint + NameNode restart, while the released source grounds the staged `collectedBlocks` → `BlockManager.removeBlock` → queued invalidation → heartbeat `DNA_INVALIDATE` → DataNode `FSDataset.invalidate(...)` path. This closes the bounded `checkpoint-surviving authority != copied embodiment`, `last-reference retirement != immediate DataNode deletion`, and `invalidation != media sanitization` seams without claiming arbitrary crash/edit-log replay, HA failover, filesystem/device overwrite, or later-release identity. Broader HDFS checkpoint/deletion genealogy belongs primarily in `computing-archaeology`."
if 'evidence/115-hadoop-241-snapshot-restart-retirement-deepening.md' not in road:
    phase2 = '## Phase 2 — Build missing technical bridges'
    must_once(road, phase2, 'Phase 2 heading')
    start = road.index(phase2)
    m = re.search(r'\n## Phase 3\b', road[start:])
    if not m:
        raise RuntimeError('Could not locate Phase 3 after Phase 2')
    end = start + m.start()
    before = road[:end].rstrip()
    after = road[end:]
    road = before + '\n\n' + road_entry + '\n' + after
ROADMAP.write_text(road)

# Update Case Index table row and append chronological findings.
idx = INDEX.read_text()
nums = [int(x) for x in re.findall(r'(?m)^-? ?\*\*(\d+)\s+—', idx)]
if not nums:
    raise RuntimeError('No numbered findings found in CASE_INDEX')
if max(nums) != 2769 and '## Case 115 deepening — HDFS snapshot checkpoint/restart and block-retirement findings' not in idx:
    raise RuntimeError(f'Expected pre-slice max finding 2769, found {max(nums)}')

if 'evidence/115-hadoop-241-snapshot-restart-retirement-deepening.md' not in idx:
    lines = idx.splitlines()
    hits = [i for i, line in enumerate(lines) if '(cases/115-apache-hdfs-snapshot-shared-block-replication.md)' in line]
    if len(hits) != 1:
        raise RuntimeError(f'Expected one Case115 index row, got {len(hits)}')
    i = hits[0]
    row = lines[i]
    if not row.rstrip().endswith('|'):
        raise RuntimeError('Case115 index row is not a markdown table row')
    row = row.rstrip()[:-1].rstrip() + ' + [2.4.1 checkpoint/restart + block-retirement deepening](evidence/115-hadoop-241-snapshot-restart-retirement-deepening.md) |'
    lines[i] = row
    idx = '\n'.join(lines)

if '## Case 115 deepening — HDFS snapshot checkpoint/restart and block-retirement findings' not in idx:
    idx = idx.rstrip() + FINDINGS + '\n'
INDEX.write_text(idx)

# Bounded assertions after mutation.
for path in (CASE, EVIDENCE, ROADMAP, INDEX):
    if not path.read_text().endswith('\n'):
        path.write_text(path.read_text() + '\n')

idx2 = INDEX.read_text()
for n in range(2770, 2785):
    if len(re.findall(rf'(?m)^- \*\*{n} —', idx2)) != 1:
        raise RuntimeError(f'Finding {n} missing or duplicated')

assert 'saveNamespace + restart` regression != arbitrary crash/edit-log-replay proof' in CASE.read_text()
assert 'DNA_INVALIDATE' in CASE.read_text()
assert 'FSDataset.invalidate' in EVIDENCE.read_text()
assert road_entry in ROADMAP.read_text()
print('Case 115 bounded deepening staged successfully.')
