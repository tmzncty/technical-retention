#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

git pull --ff-only origin main

case_path="cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md"
evidence_path="evidence/153-ceph-2013-snaptrim-asynchronous-reclamation-grounding.md"
workflow_path=".github/workflows/integrate-case153.yml"
script_path="scripts/integration_153.sh"

if [[ -e "$case_path" || -e "$evidence_path" ]]; then
  echo "Case 153 canonical files already exist; refusing to duplicate." >&2
  exit 1
fi

python3 - <<'PY'
from pathlib import Path
idx = Path('CASE_INDEX.md').read_text(encoding='utf-8')
if '3292.' not in idx:
    raise SystemExit('Expected Case 152 finding 3292 is absent; CASE_INDEX baseline changed.')
if '3293.' in idx or 'Case 153 — Ceph RADOS Snap Trimming' in idx:
    raise SystemExit('Finding 3293 or Case 153 already exists; refusing to collide.')
road = Path('ROADMAP.md').read_text(encoding='utf-8')
if 'Case 152' not in road:
    raise SystemExit('Expected Case 152 roadmap entry is absent; ROADMAP baseline changed.')
PY

cat > "$case_path" <<'EOF'
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
   - <https://docs.ceph.com/en/nautilus/rados/operations/pg-states/>

### Prior-art guardrail / repository comparison

5. Dave Hitz, James Lau, Michael Malcolm, **“File System Design for an NFS File Server Appliance,”** USENIX Winter 1994 — earlier WAFL copy-on-write snapshot witness:
   - <https://www.usenix.org/conference/usenix-winter-1994-technical-conference/file-system-design-nfs-file-server-appliance>
6. Case 99 — ZFS Snapshots: [`99-zfs-snapshot-reference-pinned-retention.md`](99-zfs-snapshot-reference-pinned-retention.md)
7. Case 73 — GFS lazy garbage collection: [`73-gfs-lazy-garbage-collection.md`](73-gfs-lazy-garbage-collection.md)
8. Case 147 — S3 multipart pre-object retention: [`147-s3-multipart-upload-preobject-retention.md`](147-s3-multipart-upload-preobject-retention.md)
9. Case 05 — RADOS replicated object repair: [`05-rados-replicated-object-repair.md`](05-rados-replicated-object-repair.md)
EOF

cat > "$evidence_path" <<'EOF'
# Evidence 153 — Ceph RADOS Snapshot Trimming, Clone Liveness, and Asynchronous Reclamation

**Status:** grounded evidence record

## Research question

What first-party evidence is sufficient to show that RADOS snapshot retirement can precede object-clone reclamation, that clone reclamation is reference-conditioned and asynchronous, and that the trim transition is maintained as distributed PG state rather than a one-shot local delete?

## Repository preflight

- `tmzncty/technical-retention` search for `snaptrim`: no existing dedicated case before this slice.
- `tmzncty/computing-archaeology` search for `snaptrim`: no dedicated study found before this slice.
- Nearby cases reviewed for overlap: Case 05 RADOS replica repair, Case 73 GFS lazy GC, Case 98 Ceph lost/unfound authority, Case 99 ZFS snapshots, Case 142 Ceph recovery headroom, Case 147 S3 multipart cleanup.

Decision: create a bounded RADOS snap-trimming case; keep broad Ceph snapshot genealogy and general distributed-GC history out of this repository.

## Evidence classification

### E153.1 — Frozen 2013 Ceph commit adding snapshot-trimming documentation

- **Source:** Ceph commit `ba449ce031058fbd05b5f44dbc0c9550e7ca11f5`.
- **Commit message:** `osd_internals/snaps.rst: add a description of snaps and trimming`.
- **Committed:** 2013-03-14 01:48:24 UTC.
- **Class:** first-party source-control historical record (`P/H`).
- **Claims supported:**
  - a public Ceph source-tree document explicitly described RADOS snapshot and trimming internals by this date;
  - the document was added as a dedicated snaps/trimming description, not reconstructed from a later manual alone.
- **Strength:** high for a documented-by chronology floor.
- **Stop condition:** commit date is not an invention date and does not prove this is the first implementation commit.

### E153.2 — Frozen 2013 `snaps.rst`: snapshot / clone representation

- **Source:** `doc/dev/osd_internals/snaps.rst` at commit `ba449ce...`.
- **Class:** frozen first-party technical documentation (`P/H/E`).
- **Claims supported:**
  - RADOS exposes pool snaps and self-managed snaps;
  - `SnapContext` carries snapshot-set / sequence information relevant to writes;
  - objects have a writable head and possible clone objects;
  - `SnapSet` tracks snapshots, clones, overlap, and clone size;
  - a clone's `object_info_t` records the snapshots for which that clone is defined.
- **Strength:** high for the documented 2013 model.
- **Stop condition:** not a complete source-level proof of every OSD storage backend or later release.

### E153.3 — Frozen 2013 `snaps.rst`: retirement → queue → async trim

- **Source:** same frozen document, `Snap Removal` section.
- **Class:** frozen first-party technical documentation (`P/H/E`).
- **Claims supported:**
  - removing a snapshot updates monitor/pool-snapshot state and causes the PG to add it to a trim queue;
  - a clone can be removed only after all of its snapshot memberships are removed;
  - snapshot trimming is asynchronous via `snap_trim_wq` while the PG is clean and not scrubbing;
  - trim scans affected objects and revises snapshot membership before removing no-longer-needed clone state.
- **Strength:** very high for the bounded relation `snapshot retirement != immediate clone reclamation`.
- **Stop condition:** does not establish secure erase, lower-layer allocator timing, or universal user-facing semantics for RBD/CephFS/RGW.

### E153.4 — Frozen 2013 `snaps.rst`: replicated trim / recovery

- **Source:** same frozen document, trim sequence and `Recovery` section.
- **Class:** frozen first-party technical documentation (`P/H/E`).
- **Claims supported:**
  - per-object trim creates a log entry and replicated operation (`repop`);
  - replicas receive the new snapshot set / membership update;
  - normal PG peering and recovery maintain snap-trimmer operations, with a documented caveat around empty snap-collection cleanup in that implementation.
- **Strength:** high for showing reclamation is distributed state transition rather than merely local deletion.
- **Stop condition:** does not prove exactly-once semantics or every lower-layer write is crash-atomic.

### E153.5 — Maintained Ceph snapshot internals

- **Source:** current `ceph/ceph` `doc/dev/osd_internals/snaps.rst` and rendered Reef documentation.
- **Class:** maintained first-party technical documentation (`P-current`).
- **Claims supported:**
  - the high-level remove → `snap_trimq` → asynchronous trim relation remains documented;
  - clone removal still depends on no remaining live snapshot membership;
  - `SnapMapper` maps objects to snaps and snaps to objects;
  - log/replica updates and `purged_snaps` remain part of the trim/recovery description;
  - if a `purged_snaps` update is lost, the documented consequence can be retrimming a now-empty snapshot.
- **Strength:** high for maintained continuity and bounded recovery semantics.
- **Stop condition:** current implementation details are not projected backward unchanged into 2013.

### E153.6 — Frozen/current divergence as anti-anachronism evidence

- **Sources:** 2013 frozen `snaps.rst` vs maintained mainline `snaps.rst`.
- **Class:** comparative primary-source evidence (`P/H/X`).
- **Observed difference:**
  - 2013 document: if head is deleted while clones survive, create `snapdir`; reverse lookup described with snap collections / hard links;
  - maintained document: head with surviving clones is represented as a whiteout holding the `SnapSet`; reverse lookup is documented through `SnapMapper`.
- **Claim supported:** stable high-level retention semantics can survive changes in internal representation.
- **Stop condition:** exact transition date / commits and all intermediate versions are not reconstructed here.

### E153.7 — Maintained PG-state vocabulary

- **Source:** Ceph Placement Group States documentation.
- **Class:** maintained first-party operations documentation (`P-current`).
- **Claims supported:**
  - `snaptrim`: trimming snapshots;
  - `snaptrim_wait`: queued to trim snapshots;
  - `snaptrim_error`: error stopped trimming snapshots.
- **Strength:** high for current operator-visible distinction between queue, execution, and error.
- **Stop condition:** no claim that these exact externally visible state names were already present in March 2013.

### E153.8 — WAFL 1994 prior-art guardrail

- **Source:** Hitz, Lau, Malcolm, USENIX Winter 1994, *File System Design for an NFS File Server Appliance*; already grounded in Case 99.
- **Class:** high-quality period scholarly/engineering source (`S/H`).
- **Claim supported:** copy-on-write snapshots and read-only historical clones are publicly documented well before the 2013 Ceph snapshot-trimming record.
- **Strength:** high for blocking a broad snapshot/COW novelty claim.
- **Stop condition:** does not establish direct WAFL → Ceph ancestry or that WAFL used Ceph's snap-trimming algorithm.

## Mechanism reconstruction

The evidence supports this bounded sequence:

```text
live snapshot relation
      |
      | administrative / monitor retirement
      v
retired snapshot + retained trim obligation
      |
      | asynchronous PG work
      v
per-object snapshot membership revision
      |
      +-- some live snapshot still references clone --> keep clone
      |
      +-- no live snapshot references clone ----------> remove clone
      |
      v
replicated trim state converges / recovery maintains work
```

This is an engineering reconstruction, not historical source wording.

## Strong distinctions grounded by the sources

1. `snapshot removal request != asynchronous trim completion`.
2. `snapshot identity retired != all clone embodiments already gone`.
3. `one snapshot removed != shared clone reclaimable`.
4. `clone physical presence != current snapshot authority`.
5. `trim queue membership != active trim execution`.
6. `active trim != successful trim completion`.
7. `reclamation update != uncoordinated local deletion`.
8. `control/mapping state != payload replica`.
9. `stable high-level relation != frozen internal representation`.
10. `clone removal != media sanitization`.

## Counterevidence / stop conditions

### S153.1 — Do not back-project maintained internals into 2013

The 2013 document and current document differ on `snapdir` vs whiteout and snap collections vs `SnapMapper`. Current terms can illuminate continuity, but cannot silently rewrite the frozen historical implementation.

### S153.2 — Do not equate RADOS internals with every Ceph snapshot product surface

RBD snapshot protection/clone dependencies, CephFS snapshots, and RGW object-versioning/lifecycle semantics are distinct layers with their own contracts.

### S153.3 — Do not infer one clone per snapshot

The source explicitly permits clone membership across multiple snapshots. This shared membership is the reason one snapshot retirement need not authorize clone deletion.

### S153.4 — Do not infer exactly-once trim

Maintained documentation says a lost `purged_snaps` update can lead to retrimming an empty snapshot. The safe inference is that this documented replay/retrim situation is tolerated, not that every sub-operation is exactly-once or universally idempotent.

### S153.5 — Do not infer sanitization

Neither frozen nor maintained snap-trimming documentation proves physical overwrite, Flash erase, crypto erase, replica-media synchronization at a forensic boundary, or irrecoverability after clone removal.

### S153.6 — Do not turn prior art into genealogy

WAFL 1994 is sufficient to block a broad novelty claim around COW snapshots. It is not evidence for direct implementation descent into Ceph snaptrim.

## Cross-case evidence use

- **Case 99 (ZFS snapshots):** earlier repository-grounded witness that a historical version can pin old storage while references survive. Used only as a functional comparison and prior-art guardrail.
- **Case 73 (GFS lazy GC):** distributed delayed reclamation after logical retirement, but via different namespace/chunk-reference machinery.
- **Case 147 (S3 multipart):** another staged cleanup relation in which authority transition precedes confirmed storage cleanup, but applied to prospective parts rather than historical clones.
- **Case 05 (RADOS repair):** same broad storage family, opposite retention task: repair current replicated state versus prune historical clone state.

## Related-repository decision

A fresh `tmzncty/computing-archaeology` search for `snaptrim` returned no dedicated study. This case therefore keeps only the mechanism-centered retention slice here. Future work on:

- first introduction of RADOS snapshotting;
- exact snap-collection → `SnapMapper` transition;
- `snapdir` → whiteout transition;
- evolution of `snaptrim` PG states;
- broader distributed snapshot-GC genealogy;

should primarily move to `computing-archaeology`.

## Evidence-quality summary

| Item | Quality | Why |
| --- | --- | --- |
| 2013 Ceph commit / frozen file | **primary / high** | dated first-party source-tree record with mechanism text |
| maintained Ceph snap internals | **primary current / high** | first-party continuity and implementation-evolution witness |
| maintained PG states | **primary current / high** | first-party operator-visible state vocabulary |
| WAFL 1994 USENIX paper | **scholarly period / high** | explicit earlier snapshot/COW witness |
| cross-case comparisons | **analytical** | functional comparison only, not genealogy |

## Sources

1. Ceph commit `ba449ce031058fbd05b5f44dbc0c9550e7ca11f5`, 2013-03-14:
   <https://github.com/ceph/ceph/commit/ba449ce031058fbd05b5f44dbc0c9550e7ca11f5>
2. Ceph frozen `doc/dev/osd_internals/snaps.rst` at that commit:
   <https://github.com/ceph/ceph/blob/ba449ce031058fbd05b5f44dbc0c9550e7ca11f5/doc/dev/osd_internals/snaps.rst>
3. Ceph maintained `doc/dev/osd_internals/snaps.rst`:
   <https://github.com/ceph/ceph/blob/main/doc/dev/osd_internals/snaps.rst>
4. Ceph Reef rendered snapshot-internals documentation:
   <https://docs.ceph.com/en/reef/dev/osd_internals/snaps/>
5. Ceph Placement Group States:
   <https://docs.ceph.com/en/nautilus/rados/operations/pg-states/>
6. Hitz, Lau, Malcolm, USENIX Winter 1994, *File System Design for an NFS File Server Appliance*:
   <https://www.usenix.org/conference/usenix-winter-1994-technical-conference/file-system-design-nfs-file-server-appliance>
EOF

cat >> CASE_INDEX.md <<'EOF'

### Case 153 — Ceph RADOS Snap Trimming: Snapshot Retirement, Clone Liveness, and Asynchronous Reclamation
3293. **[H]** Ceph commit `ba449ce031058fbd05b5f44dbc0c9550e7ca11f5`, committed 2013-03-14, added a first-party developer document explicitly describing RADOS snapshots and trimming; this is a conservative documented-by boundary, not an invention date.
3294. **[H/E]** The frozen 2013 document distinguishes pool snaps and self-managed snaps, uses `SnapContext` sequencing, and describes writable heads plus snapshot-serving clone objects tracked by `SnapSet` / clone membership metadata.
3295. **[E]** Snapshot removal changes monitor/pool-snapshot state and feeds a per-PG trim queue; retirement of snapshot authority therefore creates a retained cleanup obligation rather than proving cleanup is already complete.
3296. **[E]** `snapshot removal request != trim execution != trim completion`: the 2013 document explicitly describes snapshot trimming as asynchronous `snap_trim_wq` work.
3297. **[E]** A clone can be removed only after all of its snapshot memberships are removed, so `one snapshot retired != shared clone reclaimable`.
3298. **[E]** Snapshot identity and clone embodiment are not one-to-one: one clone may remain authoritative for another live snapshot even after one snapshot is retired.
3299. **[E]** The frozen 2013 document conditions asynchronous trimming on the PG being clean and not scrubbing, so foreground retirement can create maintenance debt whose execution depends on other PG state.
3300. **[E]** Per-object trim uses log entries and replicated operations to update object/snapshot metadata on replicas; `reclamation work != uncoordinated local deletion`.
3301. **[E]** The 2013 document says ordinary PG peering/recovery maintains snap-trimmer operations, making unfinished trim a recoverable distributed-state obligation rather than best-effort local housekeeping.
3302. **[E]** Maintained Ceph documentation uses `SnapMapper` mappings and persisted `purged_snaps` state to drive/record trimming; these are control/index state, not payload replicas.
3303. **[E]** Maintained PG-state vocabulary distinguishes `snaptrim_wait`, `snaptrim`, and `snaptrim_error`, grounding `queued cleanup != executing cleanup != successful cleanup` without back-projecting those exact state names into 2013.
3304. **[E]** Maintained documentation says loss of a `purged_snaps` update can cause retrimming of an already-empty snapshot; this supports bounded retry/re-execution tolerance, not a universal exactly-once claim.
3305. **[H/E]** The 2013 document describes surviving-clone metadata through `snapdir` plus snap collections/hard links, whereas maintained documentation uses a whiteout head plus `SnapMapper`; the high-level retention relation survived internal-representation change.
3306. **[X]** `current whiteout/SnapMapper model != frozen 2013 implementation`: maintained internals must not be silently projected backward, and exact transition genealogy remains open.
3307. **[E]** `snapshot retirement != clone trim completion != media sanitization`: neither snapshot-state retirement nor clone-object removal proves secure overwrite/erase of all lower-layer embodiments.
3308. **[H/A]** WAFL's 1994 USENIX snapshot/COW record is an earlier prior-art floor for copy-on-write historical views, blocking a broad Ceph novelty claim while establishing no direct WAFL→Ceph snaptrim genealogy.
3309. **[C]** Case 99 ZFS and Case 153 Ceph both condition historical-state reclamation on surviving references, but ZFS block-tree/reference accounting and RADOS per-PG clone trimming are functionally analogous rather than genealogically interchangeable.
3310. **[C]** Case 73 GFS lazy GC and Case 153 both delay physical/distributed cleanup after logical retirement, but GFS namespace/chunk-reference cleanup and Ceph snapshot-clone trimming use different retained relations and state machines.
3311. **[C]** Case 147 S3 multipart abort and Case 153 both show authority retirement can precede confirmed storage cleanup; the retained payload directions differ because S3 parts are prospective pre-object state while Ceph clones are historical versions.
3312. **[P]** Interpretation only: distributed forgetting can require additional retained control state—queues, mappings, logs, and recovery obligations—to complete forgetting safely; this is not historical Ceph vocabulary.
3313. **[E]** Related-repository boundary: broad Ceph snapshot chronology, snap-collection→`SnapMapper` and `snapdir`→whiteout transitions, PG-state genealogy, and cross-system snapshot-GC history belong primarily in `computing-archaeology`; Case 153 keeps only the bounded retention/reclamation relation.
EOF

cat >> ROADMAP.md <<'EOF'
- [x] **Case 153 Ceph RADOS snap-trimming / asynchronous snapshot-reclamation slice** — [`cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md`](cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md) + [`evidence/153-ceph-2013-snaptrim-asynchronous-reclamation-grounding.md`](evidence/153-ceph-2013-snaptrim-asynchronous-reclamation-grounding.md): Samuel Just's 14-Mar-2013 first-party source-tree document already separates snapshot retirement, per-PG trim queueing, reference-conditioned clone removal, asynchronous `snap_trim_wq` execution, replica/log updates, and recovery. Maintained Ceph documentation adds current `SnapMapper`/`purged_snaps` and `snaptrim_wait`/`snaptrim`/`snaptrim_error` continuity while also exposing an anti-anachronism boundary: the 2013 `snapdir`/snap-collection representation is not the maintained whiteout/`SnapMapper` representation. This closes the bounded `snapshot retired != clone reclaimed`, `one snap removed != shared clone disposable`, `queued != executing != completed reclamation`, and `logical trim != sanitization` seams. Exact first-introduction genealogy, internal representation transitions, PG-state history, lower-layer allocator timing, and fault injection remain open; broad snapshot-GC genealogy belongs primarily in `computing-archaeology`.
EOF

python3 - <<'PY'
from pathlib import Path
p = Path('ROADMAP.md')
s = p.read_text(encoding='utf-8')
s2 = s.replace(
    'garbage collection / reclamation — **partially advanced by grounded Cases 73, 125, and 145**',
    'garbage collection / reclamation — **partially advanced by grounded Cases 73, 125, 145, 150, and 153**'
)
s2 = s2.replace(
    'Database GC, managed-SSD/FTL-controller GC, distributed/object-store reclamation beyond the bounded cases, damaged-recovery-metadata cases, media-sanitization closure, and broader reclamation genealogies remain open',
    'Database GC, deeper managed-SSD/FTL-controller GC beyond Case 150, distributed/object-store reclamation beyond the bounded GFS/Ceph slices, damaged-recovery-metadata cases, media-sanitization closure, and broader reclamation genealogies remain open'
)
if s2 == s:
    raise SystemExit('Expected garbage-collection roadmap wording was not updated; refusing silent no-op.')
p.write_text(s2, encoding='utf-8')
PY

rm -f "$workflow_path" "$script_path"

git add -A

git diff --cached --check

python3 - <<'PY'
from pathlib import Path
idx = Path('CASE_INDEX.md').read_text(encoding='utf-8')
for n in range(3293, 3314):
    token = f'{n}.'
    if idx.count(token) != 1:
        raise SystemExit(f'Expected exactly one finding {token}; saw {idx.count(token)}')
case = Path('cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md').read_text(encoding='utf-8')
ev = Path('evidence/153-ceph-2013-snaptrim-asynchronous-reclamation-grounding.md').read_text(encoding='utf-8')
road = Path('ROADMAP.md').read_text(encoding='utf-8')
checks = [
    ('case status', '**Status:** `grounded`' in case),
    ('historical commit', 'ba449ce031058fbd05b5f44dbc0c9550e7ca11f5' in case and 'ba449ce031058fbd05b5f44dbc0c9550e7ca11f5' in ev),
    ('anti-anachronism', 'snapdir' in case and 'SnapMapper' in case and 'whiteout' in case),
    ('case index heading', 'Case 153 — Ceph RADOS Snap Trimming' in idx),
    ('roadmap item', 'Case 153 Ceph RADOS snap-trimming' in road),
    ('roadmap GC status', 'Cases 73, 125, 145, 150, and 153' in road),
]
for label, ok in checks:
    if not ok:
        raise SystemExit(f'Validation failed: {label}')
PY

git commit -m "case153: ground Ceph RADOS snaptrim reclamation"
git push origin HEAD:main
