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
