# Evidence 115 — HDFS Snapshot Shared Blocks and Replication Obligation, 2012–2014

## Purpose

This record grounds the bounded claims in [`../cases/115-apache-hdfs-snapshot-shared-block-replication.md`](../cases/115-apache-hdfs-snapshot-shared-block-replication.md).

The source question is narrow:

> Did early HDFS snapshot design and implementation preserve historical file state by sharing DataNode blocks, and could snapshot-retained metadata continue to affect the replication requirement of those shared blocks after the current file changed or disappeared?

The answer is **yes** for the inspected 2012 design record and Hadoop 2.4.1 implementation. This record does not establish snapshot invention priority, every later Hadoop release, actual cluster convergence timing, lower-layer sanitization, or direct WAFL/ZFS→HDFS genealogy.

---

## Source ledger

| Source | Date / revision | Type | Exact use | Limit |
| --- | --- | --- | --- | --- |
| Apache JIRA, [HDFS-2802](https://issues.apache.org/jira/browse/HDFS-2802) | created 17 Jan 2012; fixed for 2.1.0-beta | primary project record | establishes explicit HDFS snapshot project, point-in-time vocabulary, target release, design/implementation work | issue history is not invention priority |
| Apache JIRA, [HDFS-4078](https://issues.apache.org/jira/browse/HDFS-4078) | created 19 Oct 2012; resolved 22 Oct 2012 | primary design/implementation record | explicitly states current/snapshot file replication may differ while blocks are shared and block replication is their maximum | concise issue statement; inspected release source supplies implementation corroboration |
| Apache Hadoop, [Release 2.1.0-beta](https://hadoop.apache.org/release/2.1.0-beta.html) | 25 Aug 2013 | official release record | public release floor; HDFS Snapshots listed as significant highlight | not first conception/invention evidence |
| Apache Hadoop 2.4.1, [HDFS Snapshots](https://hadoop.apache.org/docs/r2.4.1/hadoop-project-dist/hadoop-hdfs/HdfsSnapshots.html) | last published 21 Jun 2014 | official versioned documentation | O(1) creation, modification-proportional metadata, no DataNode block copy, snapshot block-list/file-size retention, reverse-chronological diffs, `.snapshot` path | user-facing mechanism description, not complete NameNode source |
| Apache Hadoop `release-2.4.1`, [`INodeFile.java`](https://github.com/apache/hadoop/blob/release-2.4.1/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/INodeFile.java) | release-2.4.1 source | primary source code | `getBlockReplication()`, current-file-deleted branch, `cleanSubtree(...)` deletion/block-collection boundary | one release line; does not prove all later versions |

---

## Evidence A — project/release chronology

### A1. HDFS-2802

HDFS-2802 was created **17 January 2012** as `Support for RW/RO snapshots in HDFS`. Its description defines snapshots as point-in-time images of parts of the filesystem or the entire filesystem. The issue's fix/target version is `2.1.0-beta`, and its attachments/subtasks show active design and implementation work through 2012–2013.

### A2. Public release

Apache's **25 August 2013** Hadoop 2.1.0-beta release page lists `HDFS Snapshots` among the significant highlights.

### Supported historical floor

```text
HDFS snapshot development is explicit by January 2012,
and the feature is publicly highlighted in Hadoop 2.1.0-beta on 25 August 2013.
```

### Not supported

```text
2012 = invention date of filesystem snapshots
Hadoop 2.1.0-beta = first snapshot implementation anywhere
HDFS-2802 = first conception of the mechanism
```

Case 99 already records older WAFL/ZFS snapshot prior art and blocks those stronger novelty claims.

---

## Evidence B — no eager DataNode block copy

The versioned Hadoop 2.4.1 HDFS snapshot documentation gives four implementation properties that matter here:

1. snapshot creation is O(1) excluding inode lookup;
2. extra memory is proportional to files/directories modified relative to snapshots;
3. **blocks in DataNodes are not copied** — snapshot files record the block list and file size;
4. modifications are recorded in reverse chronological order, so current data remains directly accessible and snapshot data is computed by removing later modifications from current state.

### Supported boundaries

```text
snapshot creation != full payload duplication
```

```text
separate .snapshot namespace != separate DataNode block population
```

```text
logical historical coverage != physical copy created at snapshot time
```

This is a reference/diff-based historical view over shared distributed blocks.

---

## Evidence C — 2012 replication semantics across temporal versions

HDFS-4078 gives unusually direct contemporary language for the cross-version replication relation.

It distinguishes:

- file replication of the original/current file;
- file replication of a snapshot file;
- block replication of blocks shared between them.

The issue states that current and snapshot file replication values can differ. Because the underlying blocks are shared, block replication is the **maximum** of the original/current and snapshot-file replication values. With multiple snapshots, the maximum is taken across the current file and all snapshot files.

### Supported relation

For one block shared across temporal versions:

```text
R_block = max(R_current, R_snapshot_1, R_snapshot_2, ...)
```

### Explicitly rejected models

```text
R_block = R_current only
```

and

```text
R_block = R_current + R_snapshot_1 + R_snapshot_2 + ...
```

The snapshot does not acquire an independent replica set merely because it represents a separate temporal version.

### Methodological consequence

```text
snapshot count != physical replica count
```

and

```text
historical version metadata can affect current distributed redundancy policy
```

The second statement is an engineering reconstruction grounded in the explicit max rule; it is not Apache's philosophical vocabulary.

---

## Evidence D — release-source corroboration of the max rule

### D1. `getFileReplication(snapshot)`

In `release-2.4.1`, `INodeFile.getFileReplication(int snapshot)` returns the historical snapshot inode's file-replication value when the requested state is not `CURRENT_STATE_ID`; otherwise it reads the current inode header.

This preserves a distinction between a temporal file attribute and the effective replication of the shared block collection.

### D2. `getBlockReplication()`

The same source then computes block replication by:

1. taking current file replication;
2. obtaining `getMaxBlockRepInDiffs()` from `FileWithSnapshotFeature`;
3. returning the larger current/snapshot value;
4. if `isCurrentFileDeleted()` is true, returning the snapshot maximum directly.

### Supported boundaries

```text
file replication attribute != effective block replication
```

```text
current file deleted != snapshot replication obligation absent
```

```text
historical metadata can remain operational after current namespace state disappears
```

### Important limit

The code establishes the expected/effective replication value used by the block collection. It does not, by itself, measure how quickly a real cluster creates/deletes replicas to converge on that value after a metadata transition.

---

## Evidence E — deletion and block collection are snapshot-sensitive

### E1. `cleanSubtree(...)` branch without a snapshot

For a current file with `priorSnapshotId == NO_SNAPSHOT_ID`, the source comments that this occurs when deleting the current file and the file is not in any snapshot. It computes quota usage and calls `destroyAndCollectBlocks(...)`.

### E2. `cleanSubtree(...)` branch with a prior snapshot

When deleting the current file with a prior snapshot, the implementation does **not** run the same general destroy-and-collect path. It performs only a special cleanup for a zero-sized under-construction block when relevant.

### Supported boundary

```text
current file deletion != block collection when a snapshot still retains the file
```

This is a namespace/reference-liveness result. It does not prove immediate physical persistence forever: later snapshot deletion and block-management cleanup can retire the remaining relation.

---

## Evidence F — access relation

The 2.4.1 documentation exposes snapshots through the reserved `.snapshot` path. A path such as:

```text
/foo/.snapshot/s0/bar
```

addresses the snapshot version of `/foo/bar`, and ordinary filesystem API/CLI operations can read it.

This supplies a useful layer distinction:

```text
historical pathname != block ID != DataNode location
```

A snapshot's temporal namespace identity is resolved through NameNode metadata to shared block identities and then to distributed replicas.

---

## Evidence G — cross-case constraints

### G1. ZFS Case 99

Case 99 and HDFS Case 115 both show a complete historical view surviving through shared references rather than eager full-payload copying. But their implementation state differs: ZFS uses filesystem COW trees/accounting/holds, while HDFS uses snapshot diffs/inode state over distributed HDFS blocks and a max-replication rule.

Supported comparison:

```text
shared-reference historical retention = bounded functional analogy
```

Rejected claim:

```text
ZFS snapshot mechanism = HDFS snapshot mechanism
```

No genealogy is established.

### G2. HDFS Case 80

Case 80 establishes that live replica count and rack/failure-domain placement qualification are separate. Case 115 therefore must not turn the max replication factor into proof of adequate placement.

```text
replication factor != placement-policy satisfaction
```

### G3. HDFS Case 83

Case 83 establishes that positive replica presence and checksum/integrity qualification are separate.

```text
replica multiplicity != replica integrity
```

---

## Evidence H — forgetting boundary

The inspected sources support the retirement of namespace/reference relations and collection of blocks under specified conditions. They do **not** support a stronger forensic statement that snapshot deletion immediately overwrites every physical DataNode sector or device-internal embodiment.

Therefore retain the chain:

```text
snapshot delete
    != block-management collection/invalidation completion
    != filesystem/device reuse
    != physical sanitization
```

Lower-layer forgetting must be demonstrated separately.

---

## Claim ledger

| ID | Claim | Evidence | Strength | Limit |
| --- | --- | --- | --- | --- |
| 115-A | explicit HDFS snapshot project exists by Jan 2012 | HDFS-2802 | strong primary project record | not invention priority |
| 115-B | HDFS Snapshots publicly highlighted in 2.1.0-beta on 25 Aug 2013 | Apache release record | strong institutional primary | release floor only |
| 115-C | snapshot creation does not copy DataNode blocks | Hadoop 2.4.1 docs | strong versioned primary docs | one release family |
| 115-D | snapshot files retain block list/file size and use reverse-chronological modifications | Hadoop 2.4.1 docs | strong versioned primary docs | not complete source-level model |
| 115-E | current/snapshot file replication values may differ | HDFS-4078 | strong contemporary design record | bounded to snapshot design family |
| 115-F | shared-block replication is max across current/snapshot file replication | HDFS-4078 + 2.4.1 source | strong primary corroboration | not a measurement of convergence timing |
| 115-G | current-file deletion can leave snapshot maximum as effective block replication | `INodeFile.getBlockReplication()` | strong source-level evidence | release-bounded |
| 115-H | current file retained by snapshot avoids ordinary destroy-and-collect branch | `INodeFile.cleanSubtree()` | strong source-level evidence | lower-layer deletion/sanitization not covered |
| 115-I | snapshot is an independent backup | no source | rejected | shared blocks/cluster infrastructure contradict that shortcut |
| 115-J | HDFS snapshots descend directly from WAFL/ZFS | no genealogy source | rejected | functional/prior-art comparison only |

## Open evidence debt

- exact HDFS snapshot design attachments and branch history beyond the issue-level records;
- earliest pre-HDFS snapshot genealogy (belongs primarily in `computing-archaeology`);
- precise NameNode FSImage/edit-log crash persistence for snapshot diff/reference state;
- current Hadoop source continuity or semantic changes after 2.4.1;
- measured cluster behavior when snapshot/current replication factors diverge;
- fault injection across current-file deletion, snapshot deletion, under-replication, and NameNode restart;
- lower-layer DataNode deletion/reuse/sanitization timing.
