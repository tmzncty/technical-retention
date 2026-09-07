from pathlib import Path
from textwrap import dedent

CASE = dedent(r'''\
# Apache HDFS Snapshots: Shared Blocks, Historical Namespace Reachability, and Retained Replication Obligation

**Status:** `grounded`

## Scope

This case asks a bounded distributed-retention question:

> When an HDFS snapshot preserves an older file state without copying its DataNode blocks, what retained metadata keeps those blocks historically reachable, and can an older snapshot continue to constrain the replication obligation of blocks shared with the current file?

The historical slice is bounded to the Apache HDFS snapshot work tracked in **HDFS-2802 / HDFS-4078 (2012)**, its public appearance in **Hadoop 2.1.0-beta (25 August 2013)**, the **Hadoop 2.4.1 snapshot documentation (21 June 2014)**, and the corresponding `release-2.4.1` NameNode source.

This case is not:

- a generic HDFS snapshot history;
- a claim that HDFS invented snapshots or copy-on-write/persistent-version techniques;
- a backup guide;
- a second HDFS placement/decommission case (Case 80);
- a second HDFS integrity-scanner case (Case 83);
- a claim that deleting a snapshot securely erases DataNode media;
- a full account of NameNode FSImage/edit-log persistence for snapshots;
- evidence that HDFS and ZFS snapshots share one implementation or genealogy.

A repository search found no dedicated HDFS-snapshot case in `tmzncty/computing-archaeology`. Broader snapshot genealogy and HDFS implementation history belong there if developed.

## Historical vocabulary

Primary/project vocabulary kept distinct in this case:

Historical Apache vocabulary:

- `snapshot`;
- `snapshottable directory`;
- `.snapshot` path;
- `file replication`;
- `block replication`;
- `snapshot file`;
- `block list`;
- `FileWithSnapshotFeature`;
- `FileDiffList` / snapshot diffs;
- `current file deleted`;
- blocks `collected` for deletion/cleansing.

Project engineering vocabulary:

- **historical reachability** — a snapshot namespace relation still permits a prior file state to name shared HDFS blocks;
- **retained replication obligation** — historical file metadata can continue to participate in the effective replication requirement of blocks shared across temporal versions;
- **reference-pinned distributed retention** — shared DataNode blocks remain constitutive of an older admissible file state without an eager payload copy at snapshot creation.

The project terms are analytical reconstructions, not Apache historical vocabulary.

## Historical record

### H/P — the HDFS snapshot project was explicit by January 2012 and targeted Hadoop 2.1.0-beta

Apache JIRA **HDFS-2802**, created 17 January 2012, describes snapshots as point-in-time images of parts or all of HDFS. The issue was fixed for `2.1.0-beta` and accumulated snapshot-design attachments and implementation subtasks during 2012–2013.

Apache's release page for **Hadoop 2.1.0-beta, 25 August 2013**, lists `HDFS Snapshots` among the release highlights.

This supplies a public development/release floor only. It does not establish invention priority for filesystem snapshots.

### H/P — snapshot creation does not duplicate DataNode blocks

The Hadoop **2.4.1 HDFS Snapshots** documentation says that snapshot creation is O(1) apart from inode lookup, that extra memory grows with modifications relative to snapshots, and that **DataNode blocks are not copied**. Snapshot files retain the block list and file size; modifications are recorded in reverse chronological order so current data remains directly accessible while snapshot state is derived from retained differences.

This directly blocks a common but misleading model:

> **snapshot file != independently copied physical file.**

A separate temporal pathname can be backed by blocks shared with the current namespace state.

### H/P — the 2012 design explicitly separates file replication from shared-block replication

Apache JIRA **HDFS-4078, `Handle replication in snapshots`**, created 19 October 2012, states the key rule unusually clearly. Without snapshots, file replication and block replication coincide. With snapshots, the replication factor of the current/original file and the replication factor retained for a snapshot file can differ. Since the blocks are shared, the required block replication is the **maximum** of the current-file and snapshot-file replication factors; with multiple snapshots, it is the maximum across the current file and all snapshots.

Therefore:

> **temporal-version count != replica count.**

and

> **replication requirements across shared versions combine by maximum, not addition.**

### H/P — Hadoop 2.4.1 source preserves that rule when the current file disappears

In `release-2.4.1`, `INodeFile.getBlockReplication()` starts with the current file's replication, obtains `getMaxBlockRepInDiffs()` from `FileWithSnapshotFeature`, and returns the larger value. If `isCurrentFileDeleted()` is true, the method returns the snapshot maximum directly.

This is stronger than a generic statement that snapshots retain bytes. In this bounded implementation, historical snapshot metadata can still determine the effective block-replication requirement even after the current file has been deleted.

### H/P — deletion of a current file is not equivalent to block collection when a snapshot still contains it

The same `INodeFile.cleanSubtree(...)` implementation distinguishes two cases:

- deleting the current file when it is **not in any snapshot**: quota is computed and `destroyAndCollectBlocks(...)` is called;
- deleting the current file when a prior snapshot exists: the implementation does not take that general destroy-and-collect path, aside from special cleanup of a zero-sized under-construction block.

The source therefore supports the bounded boundary:

> **current-path deletion != immediate block retirement when a snapshot still retains the file.**

This is a NameNode/reference-liveness statement, not proof about when every physical replica is later overwritten.

## Retained state

For the bounded HDFS snapshot mechanism, later access to an old file state depends on retaining at least:

1. snapshot identity and the snapshottable-directory relation;
2. namespace/inode state sufficient to reconstruct the snapshot path;
3. file snapshot differences/attributes, including historical file size and replication information where relevant;
4. the shared HDFS block list that still constitutes that historical file state;
5. NameNode block-management state sufficient to associate those block identities with live replicas;
6. enough DataNode replicas and lower-layer integrity for the blocks to remain readable.

The snapshot name alone is not the payload. Conversely, residual block replicas alone are not a usable HDFS snapshot if the namespace/diff/reference state that makes them part of an admissible historical file has been lost.

## Physical / logical substrate

The bounded layering is:

```text
snapshot name / .snapshot namespace
        ->
INode + snapshot diff / historical file attributes
        ->
shared HDFS block identities
        ->
block-replication requirement
        ->
DataNode replica locations
        ->
local storage media
```

A snapshot adds a temporal namespace/version relation above the distributed replicas. It does not create a second complete DataNode block population at creation time.

## Retention mechanism

### Shared blocks preserve historical payload without eager copying

The 2.4.1 documentation is explicit that snapshot blocks are not copied. Retention is therefore produced by preserving enough namespace/diff/reference state that the old block list remains part of a readable historical view while current state can diverge.

Engineering reconstruction:

```text
shared block payload remains
    +
snapshot metadata still names the prior file state
    +
block manager continues to treat required blocks as live
    =
historical HDFS file remains recoverable through the snapshot path
```

This resembles reference-pinned retention in ZFS Case 99 at a bounded functional level, but HDFS adds a distributed replication layer and its own metadata structures.

### Historical metadata can constrain present physical multiplicity

HDFS-4078 and `INodeFile.getBlockReplication()` give a particularly important cross-layer relation. Suppose a block is shared by a current file with replication factor `R_current` and one or more snapshot versions with retained replication factors `R_snap_i`. The bounded HDFS rule is:

```text
R_block = max(R_current, R_snap_1, R_snap_2, ...)
```

not:

```text
R_block = R_current + R_snap_1 + R_snap_2 + ...
```

and not simply:

```text
R_block = R_current
```

Thus an older temporal version can preserve an operational requirement affecting how many distributed physical embodiments of a shared block should exist.

This is a retention-of-policy/currentness relation layered over payload retention.

### Current-file deletion can leave snapshot-only authority

When the current file is deleted, `getBlockReplication()` can return the maximum snapshot replication value. The file's current pathname/state is gone, but historical metadata remains sufficient to keep the shared blocks meaningful and to retain a replication requirement for them.

Therefore:

> **current namespace membership != sole authority for distributed block retention.**

## Addressing and access geometry

The snapshot is exposed through a reserved `.snapshot` path below a snapshottable directory. The same filesystem APIs can address paths such as:

```text
/foo/.snapshot/s0/bar
```

This temporal namespace is distinct from DataNode placement. A snapshot pathname names a historical file state; the NameNode and block manager still resolve its blocks to DataNode replicas.

Hence:

> **historical pathname != physical replica location.**

## Read semantics

Snapshots are read-only point-in-time copies at the HDFS namespace interface.

A successful snapshot read demonstrates that the required historical namespace/diff state and block replicas remain usable. It does not by itself prove:

- a separate block copy exists for the snapshot;
- every replica is healthy;
- placement policy is satisfied across racks;
- the snapshot is a backup against whole-cluster loss;
- lower-layer sectors have not been remapped or rewritten.

Case 83 remains the dedicated integrity-verification comparison, and Case 80 keeps replica-count/placement/decommission distinctions separate.

## Write and erasure semantics

The snapshot itself is read-only. Later mutations apply to the current namespace state and are recorded relative to retained snapshots rather than by eagerly rewriting a full snapshot copy.

Deleting the current file does not necessarily make its blocks reclaimable because a snapshot may still retain that file. Conversely, deleting a snapshot retires one historical namespace/reference relation but does not by itself prove immediate DataNode overwrite or media sanitization.

Therefore:

> **snapshot delete != block collection completion != physical sanitization.**

The exact post-snapshot-deletion sequence through block invalidation, DataNode deletion, filesystem free-space reuse, device remapping, and media overwrite is outside this bounded slice.

## Time

Relevant times are relational rather than one media-retention interval:

- snapshot creation time;
- later current-file mutations;
- later current-file deletion;
- duration for which a snapshot remains admissible;
- time during which snapshot attributes continue to constrain shared-block replication;
- later snapshot deletion and any asynchronous lower-layer reclamation/replication convergence.

A point-in-time view can therefore impose a future maintenance obligation long after the captured current state ceased to be current.

## Maintenance and labor

The apparently cheap O(1) snapshot creation does not mean retention is costless. The system must continue to maintain:

- snapshot namespace and diff metadata;
- shared block identities;
- NameNode block/replica knowledge;
- the effective replication requirement across current and historical file attributes;
- DataNode replicas and their placement;
- integrity checking and repair through mechanisms handled in other HDFS cases;
- eventual cleanup after all retaining relations disappear.

A small amount of historical metadata can therefore preserve or raise a much larger physical redundancy obligation.

## Failure / forgetting modes

Keep these distinct:

1. **snapshot namespace/diff loss** — blocks may survive physically while the intended historical view becomes unreconstructable;
2. **block-replica loss** — snapshot metadata survives but one or more shared block embodiments disappear;
3. **under-replication** — the file may remain readable while its expected redundancy margin is reduced;
4. **placement-policy failure** — replica count can be numerically sufficient while failure-domain placement is inadequate (Case 80);
5. **integrity failure** — a present replica can be corrupt even though it still counts as a physical copy until detected/handled (Case 83);
6. **snapshot deletion** — historical reachability is intentionally retired at the namespace layer;
7. **lower-layer media loss/reuse** — eventual physical forgetting can occur later and is not proven merely by namespace deletion.

Do not collapse these into one generic `data loss` event.

## Engineering reconstruction

The bounded mechanism supports four useful conclusions.

First:

> **historical logical coverage != physical duplication at snapshot creation.**

Second:

> **current-file replication != effective shared-block replication when snapshots retain stronger historical requirements.**

Third:

> **current namespace deletion != loss of all retention authority.**

Fourth:

> **retained policy metadata can be constitutive of physical redundancy without itself containing payload bytes.**

That fourth relation is especially important for this repository. Distributed retention is not only a question of how many payload copies happen to exist; it also depends on retained metadata defining how many copies the system still owes.

## Prior art and genealogy boundary

Case 99 already carries a **WAFL 1994** prior-art floor for copy-on-write/read-only filesystem snapshots and a later Solaris ZFS witness. Therefore this case makes no HDFS-first claim for snapshots, copy-on-write, or reference-pinned historical state.

The historical record established here is narrower:

- HDFS snapshot work is explicit in the Apache project by 2012;
- the feature is publicly highlighted in the 25 August 2013 Hadoop 2.1.0-beta release;
- HDFS-4078 explicitly binds shared snapshot/current blocks to a max-replication rule;
- the 2.4.1 source implements that relation and preserves snapshot-only block replication after current-file deletion.

Chronological similarity to WAFL/ZFS is not evidence of direct implementation inheritance. Any broad snapshot genealogy belongs in `computing-archaeology`.

## Cross-case comparison

### Case 99 — ZFS snapshots

Both cases retain an older point-in-time view by keeping old/shared data reachable rather than eagerly copying a complete dataset at snapshot creation.

But the bounded mechanisms differ:

- ZFS Case 99 emphasizes copy-on-write tree references, holds/clones, and allocation/reclamation constraints;
- HDFS Case 115 emphasizes NameNode snapshot diffs over shared distributed blocks and an effective replication factor computed across current and historical file attributes.

Therefore:

> **reference-pinned historical retention != identical redundancy semantics.**

No genealogy is implied.

### Case 80 — HDFS decommissioning and rack placement

Case 115's effective replication number does not establish where replicas are placed. Case 80 shows that replica-count sufficiency and placement-policy satisfaction are separate checks.

Therefore:

> **snapshot-retained replication factor != rack/failure-domain qualification.**

### Case 83 — HDFS block scanner

A snapshot can preserve a block identity and a replication requirement while an individual copy later develops corruption. Block scanning/checksum qualification is a separate integrity relation.

Therefore:

> **replica multiplicity != replica integrity.**

## Functional analogy

A bounded analogy to persistent data structures or copy-on-write snapshots is useful: several temporal views can share one underlying object until divergence makes different state necessary.

The analogy stops before implementation identity. HDFS's NameNode snapshot diffs, HDFS block identities, replication policy, and DataNode placement are not ZFS block-pointer/accounting semantics or a language-runtime garbage collector.

## Philosophical / media-theoretical interpretation

`I` — This case sharpens the distinction between **retaining a past representation** and **retaining an obligation created by that past**. An old snapshot can preserve not only a historical path to payload but also metadata that continues to determine the physical redundancy owed to shared blocks.

`I` — The past is therefore not merely passive residue. In this bounded system it can remain operationally normative: an older file attribute can still constrain present replication work after the current file has changed or disappeared.

These are project interpretations. Apache engineers are not being credited with a philosophy of memory, and no historical source is rewritten into Stieglerian or Heideggerian vocabulary.

## Counterexamples and limits

This case does not establish:

- that HDFS invented snapshots;
- that HDFS snapshot creation duplicates DataNode blocks;
- that `max` replication semantics imply additive copies for every snapshot;
- that a snapshot is an independent backup against cluster/media loss;
- that replication-factor satisfaction implies rack-placement satisfaction;
- that replica presence implies checksum/integrity qualification;
- that snapshot deletion immediately removes every DataNode replica;
- that NameNode metadata loss leaves snapshot blocks interpretable merely because sectors remain;
- that the exact 2.4.1 implementation is unchanged in every later Hadoop release;
- that HDFS and ZFS share a direct snapshot genealogy.

## Related repositories

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — no dedicated HDFS-snapshot case was found during this slice. Broader HDFS snapshot implementation history and cross-filesystem snapshot genealogy should live there rather than being duplicated here.
- [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) — useful if later work asks when `snapshot`, `copy-on-write`, `backup`, `replication`, and `recovery` became actors' own problem categories rather than present-day analytical labels.

## Claim ledger

| Claim | Label | Evidence | Limit |
| --- | --- | --- | --- |
| HDFS snapshot work is explicit by 2012 and shipped as a highlighted 2.1.0-beta feature in August 2013 | `H/P` | HDFS-2802; Apache release page | release floor, not invention priority |
| HDFS snapshot creation does not copy DataNode blocks | `H/P` | Hadoop 2.4.1 snapshot docs | version-bounded public contract |
| current/snapshot file replication factors may differ while blocks are shared | `H/P` | HDFS-4078 | design/implementation family, not all later releases proved |
| effective block replication is max across current and snapshot file factors | `H/P` | HDFS-4078; `INodeFile.getBlockReplication()` | bounded to inspected design/release source |
| after current-file deletion, snapshot replication can remain the effective block replication | `H/P/E` | `INodeFile.getBlockReplication()` | does not prove instant convergence of physical copies |
| deleting a current file that remains in a snapshot does not take the ordinary destroy-and-collect path | `H/P` | `INodeFile.cleanSubtree()` | special UC cleanup exists; lower-layer reclamation not reconstructed |
| snapshot retention is equivalent to independent backup | `X` | no supporting source | explicitly rejected |
| snapshot deletion proves media sanitization | `X` | no supporting source | explicitly rejected |
| HDFS snapshot mechanism is historically identical to ZFS/WAFL | `X/A` | no genealogy source | functional comparison only |

## Sources

### Primary / project records

1. Apache Hadoop JIRA, **HDFS-2802 — Support for RW/RO snapshots in HDFS**, created 17 January 2012; fix version 2.1.0-beta.
   - <https://issues.apache.org/jira/browse/HDFS-2802>

2. Apache Hadoop JIRA, **HDFS-4078 — Handle replication in snapshots**, created 19 October 2012, resolved 22 October 2012.
   - <https://issues.apache.org/jira/browse/HDFS-4078>

3. Apache Hadoop, **Release 2.1.0-beta available**, 25 August 2013.
   - <https://hadoop.apache.org/release/2.1.0-beta.html>

4. Apache Hadoop 2.4.1, **HDFS Snapshots**, last published 21 June 2014.
   - <https://hadoop.apache.org/docs/r2.4.1/hadoop-project-dist/hadoop-hdfs/HdfsSnapshots.html>

5. Apache Hadoop source, `release-2.4.1`, **INodeFile.java**.
   - `getBlockReplication()` preserves the maximum replication requirement across current and snapshot diffs and uses the snapshot maximum when the current file is deleted.
   - `cleanSubtree(...)` distinguishes deleting a current file absent from snapshots from deleting one still retained by a snapshot.
   - <https://github.com/apache/hadoop/blob/release-2.4.1/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/INodeFile.java>
''')

EVIDENCE = dedent(r'''\
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
''')

ROADMAP_BULLET = "- [x] Apache HDFS snapshot shared-block / retained replication-obligation boundary — [`cases/115-apache-hdfs-snapshot-shared-block-replication.md`](cases/115-apache-hdfs-snapshot-shared-block-replication.md), grounded by [`evidence/115-hadoop-2012-2014-snapshot-shared-block-grounding.md`](evidence/115-hadoop-2012-2014-snapshot-shared-block-grounding.md): HDFS-2802/HDFS-4078 plus Hadoop 2.4.1 documentation/source show that snapshot creation does not copy DataNode blocks, current and snapshot file replication attributes can diverge while shared-block replication is their maximum, and deleting the current file can leave snapshot-only replication authority. This closes only the bounded `historical reachability vs shared physical blocks vs retained replication obligation` relation; broad snapshot genealogy, FSImage/edit-log crash semantics, later-version continuity, convergence timing, fault injection, and lower-layer sanitization remain open.\n"

CASE_INDEX_ROW = "| [Apache HDFS Snapshots: Shared Blocks, Historical Namespace Reachability, and Retained Replication Obligation](cases/115-apache-hdfs-snapshot-shared-block-replication.md) | **grounded** | snapshot namespace/diff state + shared HDFS block identities + historical/current file replication attributes + max-derived block replication + DataNode replicas | separate historical pathname from physical replica set; snapshot creation from eager block copying; file replication from effective shared-block replication; current-file deletion from loss of snapshot retention authority | [2012–2014 Apache grounding](evidence/115-hadoop-2012-2014-snapshot-shared-block-grounding.md); broader snapshot genealogy, NameNode crash persistence, later release evolution, convergence/fault validation, and physical sanitization remain separate work |\n"

FINDINGS = dedent('''\
- **1797 — HDFS snapshot development/release floor != snapshot invention priority:** HDFS-2802 is explicit by 17 January 2012 and Hadoop 2.1.0-beta publicly highlights HDFS Snapshots on 25 August 2013, but Case 99 already carries earlier filesystem-snapshot prior art. (`H/P`, `X`)
- **1798 — snapshot creation != DataNode block copy:** Hadoop 2.4.1 documents O(1) snapshot creation and explicitly says snapshot files record block lists/file size while DataNode blocks are not copied. (`H/P`)
- **1799 — separate temporal namespace != separate physical block population:** `.snapshot` exposes an older pathname/view while payload blocks may be shared with current state. (`H/P`, `E`)
- **1800 — file replication != effective block replication with snapshots:** HDFS-4078 and `INodeFile` distinguish per-version file-replication attributes from the replication factor required of shared blocks. (`H/P`)
- **1801 — replication across temporal versions is max, not sum:** for blocks shared by current and snapshot files, HDFS-4078 defines block replication as the maximum of their file-replication factors, extended across multiple snapshots. (`H/P`)
- **1802 — snapshot count != replica count:** adding another temporal view does not imply an independent replica set; shared-block replication follows the max rule rather than additive duplication. (`H/P`, `E`)
- **1803 — current-file deletion != loss of snapshot replication authority:** Hadoop 2.4.1 `getBlockReplication()` returns the maximum snapshot replication value when the current file is deleted. (`H/P`)
- **1804 — current pathname deletion != immediate block collection when a snapshot retains the file:** `INodeFile.cleanSubtree()` takes the ordinary destroy-and-collect path only when the current file is not in a snapshot; a snapshot-retained current deletion follows a different branch. (`H/P`)
- **1805 — historical metadata can impose present physical redundancy work:** snapshot-retained file attributes can continue to determine the effective replication obligation of shared distributed blocks after current state diverges or disappears. (`E`)
- **1806 — snapshot reference survival != independent backup:** shared DataNode blocks and common cluster/NameNode infrastructure mean a snapshot is not evidence of a failure-independent backup copy. (`H/P`, `X`)
- **1807 — residual block replicas != snapshot recoverability:** usable historical state also depends on retained namespace/inode/diff/block-identity relations that make those replicas part of an admissible snapshot. (`E`)
- **1808 — snapshot deletion != physical sanitization:** retiring the snapshot/reference relation and later collecting/invalidation of blocks do not prove immediate overwrite of local or device-internal media embodiments. (`E`, `X`)
- **1809 — retained replication factor != rack/failure-domain qualification:** Case 80 separately shows that live-replica count and placement-policy satisfaction are different checks. (`A`, `X`)
- **1810 — replica multiplicity != integrity qualification:** Case 83 separately shows that a present HDFS replica can require checksum scanning/corrupt-replica handling; snapshot-retained copies are not thereby verified copies. (`A`, `X`)
- **1811 — Case 99 ZFS snapshot sharing ~= Case 115 HDFS snapshot sharing only as a bounded functional analogy:** both preserve older views without eager full duplication, but ZFS COW tree/accounting/hold semantics and HDFS snapshot-diff/distributed-replication semantics are not mechanism identity or proven genealogy. (`A`, `X`)
- **1812 — related-repository boundary:** `tmzncty/computing-archaeology` has no dedicated HDFS-snapshot case to reuse in this round; broad snapshot genealogy and HDFS implementation history should be developed there rather than duplicated here. (`H/P` project-state record)
''')

CASE99_INSERT = dedent('''\
### Case 115 — HDFS snapshots

Both Case 99 and Case 115 retain an older point-in-time view through shared underlying payload rather than eagerly copying a complete dataset at snapshot creation. The bounded implementation relation is nevertheless different: HDFS snapshot diffs can retain historical file-replication attributes, and the shared HDFS block collection uses the maximum replication requirement across current and snapshot versions.

Therefore:

> **shared-reference historical retention != identical physical redundancy semantics.**

This is a functional comparison only. It does not establish WAFL/ZFS→HDFS implementation genealogy.

''')


def write_new(path: str, content: str):
    p = Path(path)
    if p.exists():
        existing = p.read_text()
        if existing != content:
            raise SystemExit(f"refusing to overwrite differing existing file: {path}")
        return
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)


def insert_after_matching_line(text: str, needle: str, addition: str) -> str:
    if addition.strip() in text:
        return text
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if needle in line:
            lines.insert(i + 1, addition)
            return ''.join(lines)
    raise SystemExit(f"anchor not found: {needle}")


write_new('cases/115-apache-hdfs-snapshot-shared-block-replication.md', CASE)
write_new('evidence/115-hadoop-2012-2014-snapshot-shared-block-grounding.md', EVIDENCE)

roadmap = Path('ROADMAP.md').read_text()
if 'cases/115-apache-hdfs-snapshot-shared-block-replication.md' not in roadmap:
    roadmap = insert_after_matching_line(
        roadmap,
        'cases/114-nvme14-namespace-write-protection.md',
        ROADMAP_BULLET,
    )
Path('ROADMAP.md').write_text(roadmap)

index = Path('CASE_INDEX.md').read_text()
if 'cases/115-apache-hdfs-snapshot-shared-block-replication.md' not in index:
    index = insert_after_matching_line(
        index,
        'cases/114-nvme14-namespace-write-protection.md',
        CASE_INDEX_ROW,
    )
if '**1797 —' not in index:
    index = insert_after_matching_line(index, '**1796 —', FINDINGS)
Path('CASE_INDEX.md').write_text(index)

case99 = Path('cases/99-zfs-snapshot-reference-pinned-retention.md').read_text()
if '### Case 115 — HDFS snapshots' not in case99:
    marker = '## Functional analogy\n'
    if marker not in case99:
        raise SystemExit('Case 99 functional-analogy anchor not found')
    case99 = case99.replace(marker, CASE99_INSERT + marker, 1)
Path('cases/99-zfs-snapshot-reference-pinned-retention.md').write_text(case99)
