# Case 153 — Ceph RADOS Snap Trimming: Snapshot Retirement, Clone Liveness, and Asynchronous Reclamation

**Status:** `grounded`

## Scope

This case asks one bounded retention question:

> After a Ceph RADOS snapshot is retired at the snapshot-control layer, why can snapshot-derived object clones remain physically/logically present for additional time, and what retained metadata/work state authorizes their later reclamation?

The historical anchor is Samuel Just's Ceph source-tree commit `ba449ce031058fbd05b5f44dbc0c9550e7ca11f5`, committed **2013-03-14**, which added a developer document explicitly describing RADOS snapshots and asynchronous snapshot trimming. Current Ceph developer documentation and placement-group state documentation are used as continuity and implementation-evolution witnesses, not projected backward unchanged into 2013.

This case is deliberately about **RADOS OSD snapshot trimming**, not:

- a generic Ceph history;
- RBD user-facing snapshot protection / clone-parent dependency rules;
- CephFS snapshot semantics;
- a second copy of Case 05's RADOS replication/repair history;
- a second copy of Case 98's `unfound` / `mark_unfound_lost` authority problem;
- a second copy of Case 142's recovery/backfill capacity gating;
- proof that Ceph invented snapshots, copy-on-write, garbage collection, or asynchronous reclamation;
- evidence that removing a RADOS snapshot securely sanitizes every lower-layer physical embodiment.

Fresh repository searches found no dedicated `snaptrim` case in either `tmzncty/technical-retention` or `tmzncty/computing-archaeology` before this slice.

## Historical vocabulary

Historical / project vocabulary retained from the sources:

- `pool snaps`;
- `self managed snaps`;
- `SnapContext`;
- `seq`;
- `head`;
- `clone`;
- `SnapSet`;
- `purged snaps` / `purged_snaps`;
- `snaptrimq` in the 2013 document and `snap_trimq` in maintained documentation;
- `snap_trim_wq`;
- `repop`;
- `snap collections` in the 2013 document;
- `SnapMapper` in the maintained implementation documentation;
- PG states `snaptrim`, `snaptrim_wait`, and `snaptrim_error` in maintained operations documentation.

Project analytical vocabulary:

- **snapshot-retirement authority** — state saying a snapshot identifier is no longer a live historical view;
- **clone liveness** — whether at least one still-live snapshot requires a clone;
- **trim obligation** — retained work state saying retired snapshot membership still needs to be removed from per-object clone metadata and obsolete clones may need reclamation;
- **reclamation completion** — completion of the object-level trimming work, distinct from the earlier snapshot-retirement request;
- **maintenance observability** — operator-visible state distinguishing queued, active, and failed trimming.

These analytical terms are not presented as historical Ceph vocabulary.

## Retained state

For the bounded mechanism, the system may need to retain several different kinds of state at once:

1. the set / sequencing relation identifying snapshots relevant to an object;
2. the `SnapSet` relation describing clones and snapshot membership;
3. clone payload embodiments that still serve one or more live snapshots;
4. a per-PG trimming queue / purged-snapshot relation for work not yet completed;
5. a mapping from snapshot identifiers to affected clone objects (historically snap collections; later `SnapMapper`);
6. log / replicated-operation state used to make trim updates visible to replicas and recoverable through ordinary PG peering/recovery;
7. lower-layer storage state whose physical reuse or sanitization is outside this case.

The important distinction is:

> **snapshot no longer live != every clone formerly serving it is already reclaimable or gone.**

A clone can belong to more than one snapshot. Retiring one snapshot removes one membership relation; it does not automatically retire all other live references to the same clone.

## Physical / logical substrate

The bounded relation can be represented as:

```text
snapshot identity / SnapContext
        ->
object SnapSet + clone membership
        ->
clone object embodiment(s)
        ->
PG / replicated OSD storage
```

Snapshot retirement adds another control path:

```text
snapshot retired / purged relation
        ->
PG trim queue
        ->
per-object membership update
        ->
remove clone only if no live snapshot still needs it
        ->
ordinary lower-layer reclamation may follow
```

The queue and mappings are not payload replicas. They are control metadata that determines when retained payload embodiments cease to be required by snapshot semantics.

## Retention mechanism

### A clone is retained by remaining snapshot membership

The 2013 Ceph developer document states that an object's `SnapSet` tracks the snapshots and clone objects, while each clone's `object_info_t` records the snapshots for which that clone is defined.

On snapshot removal, the PG does not blindly delete every clone touched by that snapshot. The document states that **a clone can be removed when all of its snaps have been removed**.

Engineering reconstruction:

```text
clone belongs to {snap 10, snap 11}
remove snap 10
        ->
clone still belongs to {snap 11}
        ->
clone remains live
remove snap 11
        ->
no live snapshot membership remains
        ->
clone becomes eligible for removal during trimming
```

Therefore:

> **one snapshot retired != shared clone reclaimable.**

This is a reference-conditioned reclamation rule, but the source's own terms (`SnapSet`, clone `snaps`, snap collections / `SnapMapper`) remain primary in historical and engineering claims.

### Snapshot retirement creates asynchronous work

The 2013 document says removing a snapshot changes monitor/snapshot state and causes the PG to add that snapshot to a trimming queue. It then states that trimming is performed **asynchronously** by `snap_trim_wq` while the PG is clean and not scrubbing.

That fixes a temporal separation:

> **snapshot-removal request != trim execution != trim completion.**

The snapshot-control relation can change before every object-level clone relation has been updated and before every now-unneeded clone has been removed.

### Trim is a replicated state transition, not merely a local unlink loop

The 2013 record says each trimmed object receives a log entry and `repop` update; replicas use the logged snapshot-set change to update their own membership metadata. It also says normal PG peering and recovery maintain the snap-trimmer operations, subject to cleanup caveats in that older implementation.

Maintained Ceph documentation preserves the same broad shape: trim updates object info / `SnapSet`, updates `SnapMapper`, propagates new snapshot membership to replicas through log entries, and persists purged-snapshot information.

Hence:

> **reclamation work != uncoordinated local deletion.**

The transition that makes a clone disposable is itself part of replicated object-system state.

### Queue / execution / failure are different observable states

Maintained Ceph placement-group documentation exposes:

- `snaptrim_wait` — queued to trim snapshots;
- `snaptrim` — trimming snapshots;
- `snaptrim_error` — error stopped trimming snapshots.

These names are current operational evidence, not proof that the exact same externally visible PG-state vocabulary existed in March 2013.

They nevertheless provide a strong maintained counterexample to treating one administrative removal command as one instantaneous erasure event:

> **queued cleanup != executing cleanup != successful cleanup.**

## Addressing and access geometry

RADOS snapshotting is object/version geometry, not a second complete pool copy.

The historical document describes a writable `head` plus zero or more `clone` objects. A `SnapContext` carries the snapshot set / sequence relevant to a write; when a newer snapshot boundary requires an older view to remain readable, the OSD can create a clone before mutating the head.

The same clone can serve more than one snapshot interval. This is precisely why deleting one snapshot cannot be translated into `delete one physical clone`.

Thus:

> **snapshot identifier != one dedicated payload copy.**

## Read semantics

Snapshot reads rely on the clone / membership relations that make an older object version admissible for the requested snapshot.

A surviving clone is not necessarily garbage merely because one snapshot was removed. If another live snapshot still maps to it, that clone remains part of an admissible historical view.

Conversely, physical survival of a clone after its final snapshot membership is retired does not make the clone a live snapshot version. During asynchronous trimming, physical presence and logical authority can diverge temporarily.

> **clone presence != current snapshot membership.**

## Write and snapshot semantics

The 2013 record explains that before mutating a head, the OSD checks whether a snapshot boundary since the most recent clone requires a new clone to preserve older reads. The retention mechanism is therefore not `copy every object at snapshot creation`.

Historical versions are materialized selectively as writes cross snapshot boundaries.

This is compatible with the later reclamation rule: one clone can summarize an interval of snapshot membership and becomes removable only when no live snapshot in that relation still needs it.

## Time

The case contains several distinct times:

- snapshot creation / sequencing time;
- later writes that cause clone creation;
- snapshot retirement time at the monitor / pool-snapshot relation;
- time spent queued for trim;
- asynchronous object-by-object trim execution;
- possible interruption / recovery / retry time;
- eventual clone removal when no live snapshot membership remains;
- later lower-layer block reuse or sanitization time, which is outside this case.

There is no single timestamp at which all meanings of “snapshot deleted” become true.

## Maintenance and labor

Snap trimming is explicit maintenance work.

The system must:

- remember which snapshots have been retired;
- discover the affected clone objects;
- update each clone's membership;
- update `SnapSet` / mapping metadata;
- remove clone objects that no longer serve any live snapshot;
- replicate those transitions;
- survive or reconcile peering/recovery;
- expose queued/running/error maintenance state in maintained Ceph.

The historical document further constrains trim execution to a PG that is clean and not scrubbing. This means foreground snapshot retirement can create maintenance debt whose execution is conditioned on other PG state.

Do not generalize this into a claim that `clean` means all lower-layer media are physically sanitized or free of latent faults. It is a Ceph PG-state prerequisite in this mechanism.

## Failure and forgetting

### Removing the snapshot can precede reclaiming the clones

The central forgetting sequence is staged:

```text
snapshot relation retired
    -> trim obligation retained
    -> object memberships revised
    -> unreferenced clone removed
```

A failure or delay between these stages can leave already-retired historical material physically embodied longer than the logical snapshot namespace would suggest.

### Shared membership can intentionally block deletion

A clone with any surviving snapshot membership must remain. This is not a cleanup failure; it is correct retention.

### Recovery maintains unfinished trim work

The 2013 document explicitly ties trim operations to repops/log entries and says normal PG peering and recovery maintain the snap-trimmer operations, with a caveat around old snap-collection cleanup. Maintained documentation similarly states that peering/recovery maintain snap-trimmer operations and that a lost `purged_snaps` update can result in retrimming an already-empty snapshot.

The latter supports a bounded statement that **re-execution can be tolerated in that documented condition**. It does not justify a universal claim that every snaptrim sub-operation is exactly-once or perfectly idempotent under every fault.

### Logical reclamation is not secure sanitization

Removing a clone object or retiring its snapshot membership does not establish:

- overwrite of every BlueStore / FileStore lower-layer block;
- immediate release from all allocator caches;
- SSD FTL invalidation/erase completion;
- cryptographic erasure;
- forensic irrecoverability.

Therefore:

> **snapshot retirement != clone trim completion != media sanitization.**

Cases 44 and 47 remain the stronger erase/sanitization boundary.

## Historical record

### H/P — March 2013 public source-tree documentation

Commit `ba449ce031058fbd05b5f44dbc0c9550e7ca11f5`, committed on **2013-03-14**, added `doc/dev/osd_internals/snaps.rst` with the message `add a description of snaps and trimming`.

The added document already describes:

- pool and self-managed snapshots;
- `SnapContext`;
- head / clone structure;
- `SnapSet` membership;
- snapshot removal feeding a trim queue;
- clone deletion only after all of its snapshot memberships are removed;
- asynchronous `snap_trim_wq` execution;
- per-object log / replicated-operation updates;
- integration with PG recovery.

This is a conservative **documented-by** boundary for the mechanism. It is not a claim that March 2013 was the invention or first implementation date.

### H/P — the internal representation changed later

The 2013 document says deleting a head while clones remain creates a `snapdir` object to house the `SnapSet`, and it describes snapshot collections / hard links for reverse membership lookup.

Maintained mainline documentation instead says a head with surviving clones is kept as a whiteout to house the `SnapSet`, and it documents `SnapMapper` mappings.

Therefore:

> **stable high-level retention relation != frozen internal representation.**

The exact transition genealogy is outside this case. Current `whiteout` / `SnapMapper` details must not be projected backward as if they were already the March-2013 implementation described by the frozen document.

## Engineering reconstruction

A minimal state machine for this case is:

```text
LIVE SNAPSHOT
  snapshot id authorizes historical reads
  clones may carry one or more snapshot memberships
        |
        | remove snapshot
        v
SNAPSHOT RETIRED / TRIM OWED
  snapshot no longer live at control layer
  PG retains trim work / purged-snapshot relation
        |
        | async per-object trim
        v
MEMBERSHIP REVISED
  remove retired snap from clone metadata
  +------------------------------+
  | another live snap remains?   |
  +------------------------------+
       yes |                 | no
           v                 v
      CLONE RETAINED    CLONE REMOVABLE
                           |
                           | replicated removal/update
                           v
                     TRIM COMPLETED
```

This is project engineering reconstruction from Ceph's documented relations, not a claim that Ceph developers used these exact state names.

## PG-activation reconstruction deepening: the obligation can survive without the old queue object

A second evidence pass now closes one narrower restart/recovery question. Ceph's 15-Dec-2016 `pgpool.rst` and matching `PG.cc` show that primary PG activation **constructs** `snap_trimq` from the pool's removed-snapshot set and subtracts `info.purged_snaps`; the current source has changed the concrete representation but still computes `to_trim` from OSDMap removed-snapshot state minus `info.purged_snaps` before handing the result into PG activation. See [`../evidence/153-ceph-2016-pg-activation-trim-obligation-reconstruction-deepening.md`](../evidence/153-ceph-2016-pg-activation-trim-obligation-reconstruction-deepening.md).

This strengthens the failure/recovery model:

```text
snapshot-retirement relation
+
trim-completion relation (`purged_snaps`)
        ↓ activation / reconciliation
pending snap IDs to trim
        ↓
worker queue / asynchronous execution
```

The critical distinction is:

> **unfinished reclamation obligation can remain reconstructible even when the previous in-memory scheduler queue does not survive.**

In 2016 the documented implementation used `cached_removed_snaps - info.purged_snaps -> snap_trimq`. In the inspected 12-Sep-2026 mainline source, `PeeringState` instead builds `to_trim` from the OSDMap `removed_snaps_queue`, subtracts the intersection with `info.purged_snaps`, and passes the result into `on_activate`; the current Crimson PG then materializes that set as `snap_trimq`. The stable relation therefore outlives a concrete representation change.

Maintained `snaps.rst` adds the completion side of the relation: replicas persist the new `purged_snaps` with PG info, normal peering/recovery maintain trim operations, and loss of a `purged_snaps` update can cause a now-empty snapshot to be trimmed again. That is evidence that **missing completion evidence may cause redundant work**, not evidence that the snapshot becomes live again.

Do not over-read this into exact resume semantics. The inspected sources do not establish persistence of a byte-identical queue, thread state, scheduling order, or exact per-object iterator position. `queue reconstructed != exact worker cursor restored`, and the documented empty-retrim case does not prove universal exactly-once/idempotent behavior for every snaptrim crash window.

## Prior art and genealogy boundary

### WAFL 1994 blocks a broad snapshot/COW novelty claim

Case 99 already grounds an earlier public snapshot/COW witness in Dave Hitz, James Lau, and Michael Malcolm's 1994 USENIX WAFL paper. That is enough to reject a claim that Ceph invented copy-on-write filesystem snapshots or reference-pinned historical versions.

This new case does **not** establish that Ceph snap trimming descends from WAFL, ZFS, language garbage collectors, or any other earlier mechanism.

It also does not claim that WAFL's snapshot deletion algorithm is the same as RADOS `snaptrim`.

> **earlier snapshot prior art != direct snaptrim genealogy.**

A broader genealogy of snapshot GC, reference counting, object-version pruning, and distributed reclamation belongs primarily in `tmzncty/computing-archaeology`.

## Cross-case comparison

### Case 99 — ZFS snapshot reference-pinned retention

Both cases show that historical state remains non-reclaimable while a live reference still reaches it.

- Case 99: ZFS snapshots pin old blocks / trees, with holds and clone dependencies able to defer destruction.
- Case 153: RADOS clone membership can span multiple snapshots; retiring a snapshot creates explicit asynchronous per-PG trim work, and a clone is removed only when no live snapshot still needs it.

Functional relation:

> **reference retirement can be a prerequisite for reclamation.**

The concrete metadata, allocation geometry, replication, and cleanup state machines are different. No genealogy is implied.

### Case 73 — GFS lazy garbage collection

Both systems separate logical retirement from later distributed cleanup.

- GFS Case 73 uses hidden-name grace / namespace and chunk-reference retirement before replica cleanup.
- Ceph Case 153 uses snapshot membership / trim queues and per-object clone pruning.

The shared concept is delayed reclamation, not a shared algorithm.

### Case 147 — S3 multipart abort cleanup

Case 147 shows an abort can retire construction authority while racing `UploadPart` operations and retained part storage still require later verification/cleanup.

Case 153 similarly shows a snapshot-control transition can precede complete object-level reclamation. But S3 multipart parts are prospective pre-object payload; Ceph snapshot clones are historical object versions. The direction of retention differs.

### Case 05 — RADOS replica repair

Case 05 concerns keeping a **current** RADOS object replicated and recoverable across OSD failure/membership change. Case 153 concerns pruning **historical snapshot clones** after snapshot authority retires.

> **current-object repair != historical-version reclamation.**

## Functional analogy

A bounded garbage-collector analogy is useful: a clone remains live while some retained snapshot relation still references it, and reclamation follows only after those relations disappear.

The analogy must stop there. Ceph's historical mechanism is expressed in `SnapContext`, `SnapSet`, clone membership, PG queues, logs, replicas, and recovery. It is not evidence that Ceph used tracing-GC semantics or terminology.

## Philosophical / media-theoretical interpretation

`I` — Case 153 gives another concrete reason to separate **forgetting authority** from **material disappearance**. A snapshot can cease to be a live historical view while the system still remembers that cleanup is owed.

`I` — The maintenance queue is a retained trace of forgetting-in-progress: the old relation has been retired, but the system must preserve enough control state to complete that retirement safely across many objects and replicas.

`I` — Distributed forgetting can therefore require additional memory. To remove historical state correctly, the system temporarily retains purge/trim metadata, mappings, logs, and recovery obligations.

These are project interpretations, not historical Ceph claims.

## Counterexamples and limits

This case does not establish:

- that March 2013 is the first implementation or invention date for Ceph snapshots or trimming;
- that current Ceph `SnapMapper`, whiteout, or PG-state details were already identical in 2013;
- that every Ceph snapshot surface (RBD, CephFS, RGW) uses the same user-visible deletion contract;
- that a snapshot ID corresponds to one dedicated clone object;
- that deleting one snapshot allows deletion of a clone still serving another snapshot;
- that queue admission means trimming has started;
- that trimming started means it will finish without error;
- that retrimming an empty snapshot implies exactly-once semantics for all trim work;
- that clone removal securely erases lower-layer media;
- that ZFS/WAFL/GFS/Ceph share a proven implementation genealogy.

## Related repositories

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — fresh search found no dedicated `snaptrim` study. Broader genealogy of Ceph snapshot internals, snapshot GC/reference-counting terminology, and cross-system reclamation belongs there rather than being duplicated here.
- [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) — a future home for when `snapshot deletion`, `garbage collection`, `purge`, and `trim` became explicit engineering problem vocabularies across systems.

## Claim ledger

| Claim | Label | Evidence | Limit |
| --- | --- | --- | --- |
| Ceph publicly documented asynchronous RADOS snapshot trimming by 2013-03-14 | `H/P` | frozen Ceph commit/document | documented-by boundary, not invention date |
| snapshot removal feeds a PG trim queue | `H/P/E` | 2013 frozen developer document | bounded to documented RADOS mechanism |
| clone removal waits until all of that clone's snapshot memberships are removed | `H/P/E` | 2013 frozen developer document; maintained doc continuity | not a universal snapshot rule |
| trimming is asynchronous and conditioned on PG state | `H/P/E` | 2013 document; maintained docs | exact scheduler policy not reconstructed |
| trim updates are logged/replicated and participate in recovery | `H/P/E` | 2013 and maintained developer docs | not a proof of every crash-atomic lower-layer write |
| queued, active, and failed snap trimming are distinguishable | `H/P-current/E` | maintained PG-state docs | not back-projected as 2013 vocabulary |
| 2013 snapdir/snap-collection representation differs from maintained whiteout/SnapMapper representation | `H/P-current/X` | frozen vs maintained docs | exact transition genealogy remains open |
| logical snapshot retirement equals secure media erase | `X` | no source | explicitly rejected |
| WAFL 1994 proves direct ancestry of Ceph snaptrim | `X` | chronology only | explicitly rejected |

## Sources

### Primary / frozen project records

1. Ceph commit `ba449ce031058fbd05b5f44dbc0c9550e7ca11f5`, Samuel Just, **`osd_internals/snaps.rst: add a description of snaps and trimming`**, committed 2013-03-14:
   - <https://github.com/ceph/ceph/commit/ba449ce031058fbd05b5f44dbc0c9550e7ca11f5>
2. Frozen file at that commit, `doc/dev/osd_internals/snaps.rst`:
   - <https://github.com/ceph/ceph/blob/ba449ce031058fbd05b5f44dbc0c9550e7ca11f5/doc/dev/osd_internals/snaps.rst>

### Maintained / later first-party continuity and implementation-evolution witnesses

3. Ceph, maintained `doc/dev/osd_internals/snaps.rst`:
   - <https://github.com/ceph/ceph/blob/main/doc/dev/osd_internals/snaps.rst>
   - rendered stable-release witness: <https://docs.ceph.com/en/reef/dev/osd_internals/snaps/>
4. Ceph, **Placement Group States**, for current `snaptrim`, `snaptrim_wait`, `snaptrim_error` vocabulary:
   - <https://docs.ceph.com/en/latest/rados/operations/pg-states/>

### Prior-art guardrail / repository comparison

5. Dave Hitz, James Lau, Michael Malcolm, **“File System Design for an NFS File Server Appliance,”** USENIX Winter 1994 — earlier WAFL copy-on-write snapshot witness:
   - <https://www.usenix.org/conference/usenix-winter-1994-technical-conference/file-system-design-nfs-file-server-appliance>
6. Case 99 — ZFS Snapshots: [`99-zfs-snapshot-reference-pinned-retention.md`](99-zfs-snapshot-reference-pinned-retention.md)
7. Case 73 — GFS lazy garbage collection: [`73-gfs-lazy-garbage-collection.md`](73-gfs-lazy-garbage-collection.md)
8. Case 147 — S3 multipart pre-object retention: [`147-s3-multipart-upload-preobject-retention.md`](147-s3-multipart-upload-preobject-retention.md)
9. Case 05 — RADOS replicated object repair: [`05-rados-replicated-object-repair.md`](05-rados-replicated-object-repair.md)

## 2017–2019 representation transition deepening

Evidence 153C traces the source-level transition that Evidence 153B left open. In December 2017, Ceph added OSDMap `new_removed_snaps`, `new_purged_snaps`, and `removed_snaps_queue`, with the introducing commit explicitly distinguishing current removed-but-not-purged work from the older all-time removed-snapshot set. A same-day Mimic-gated PG change then kept the old `PGPool.cached_removed_snaps` path only for `<= luminous`, while Mimic activation derived trim work from the OSDMap queue reconciled with `pg_info_t.purged_snaps`.

In May 2019, `PeeringState` deliberately stopped using `snap_trimq` itself during that reconciliation: it derived a local `to_trim` set and passed the result into the PG, where the worker queue was materialized. The July 2019 Octopus-targeting cleanup then removed the pre-Mimic cache branch. The bounded conclusion is therefore stronger than a field-renaming story: **the retained cleanup relation survives while its container, ownership layer, compatibility path, and transient execution representation change**.

This supports:

```text
retained cleanup obligation != retained exact queue object
retained authority != activation-time handoff != worker queue
same obligation relation != same software representation
```

It does not identify the invention of snap trimming, equate commit dates with production deployment, prove exact cursor resume or universal idempotence, or make lower-layer physical reclamation/sanitization claims.

Evidence: [`evidence/153-ceph-2017-2019-removed-snaps-representation-transition-deepening.md`](../evidence/153-ceph-2017-2019-removed-snaps-representation-transition-deepening.md).
