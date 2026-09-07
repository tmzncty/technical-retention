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
