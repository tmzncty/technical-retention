# Evidence 153C — Ceph 2017–2019 Removed-Snapshot Obligation Representation Transition

## Status

Grounded bounded deepening for Case 153. This record closes the roadmap's narrow representation-transition debt between the 2016 `cached_removed_snaps` activation model and the later OSDMap / `PeeringState` path. It does **not** claim to identify the invention of snap trimming, the first production deployment of these changes, or the complete genealogy of distributed snapshot garbage collection.

## Research question

The 2016 source inspected in Evidence 153B reconstructs pending snapshot-trim work from a PG-local cache of removed snapshots minus `info.purged_snaps`. Maintained Ceph instead derives work from OSDMap `removed_snaps_queue` in `PeeringState` and hands an activation-local `to_trim` set to the PG. When, and in what source-visible steps, did that representation and ownership boundary change?

The narrow question is therefore:

> Did Ceph merely rename one durable queue, or did it move the retained reclamation obligation across representations while preserving the relation needed to reconstruct pending work?

## Primary-source chain

### 1. 2017-12-01 — OSDMap acquires current removed-but-not-purged state and epoch deltas

Ceph commit [`553048fbf97af999783deb7e992c8ecfa5e55500`](https://github.com/ceph/ceph/commit/553048fbf97af999783deb7e992c8ecfa5e55500), `osd/OSDMap: track newly removed and purged snaps in each epoch`, explicitly says that instead of maintaining a set of snapshot IDs removed "over all time", each OSDMap epoch should record newly removed and newly purged snapshots. It also adds an interval of snapshots removed but not yet purged, described as the set currently being removed and as visibility into the cluster's "trimming snaps" set.

The diff adds three distinct structures:

- `new_removed_snaps` — removals introduced by the current epoch;
- `new_purged_snaps` — purges introduced by the current epoch;
- `removed_snaps_queue` — the accumulated interval of removed snapshots still awaiting purge, updated by unioning new removals and subtracting new purges.

This is not safely described as a simple field rename. The commit message explicitly changes the intended temporal scope from an all-time removed set toward current unresolved reclamation obligation plus per-epoch deltas.

### 2. 2017-12-01 — Mimic compatibility cutover changes where PG activation gets the obligation

Ceph commit [`6e1b7c4c14be575a554ffe1d6e71c0d6189486af`](https://github.com/ceph/ceph/commit/6e1b7c4c14be575a554ffe1d6e71c0d6189486af), `osd/PG: use new mimic osdmap structures for removed, pruned snaps`, makes the transition compatibility-aware rather than instantaneous.

For `require_osd_release >= CEPH_RELEASE_MIMIC`, `PGPool::update` comments that Mimic tracks `removed_snaps_queue` in the OSDMap and `purged_snaps` in `pg_info_t`, with deltas for both in each OSDMap, and therefore the PGPool cache no longer needs to track the same state. The code clears `cached_removed_snaps` / `newly_removed_snaps` on that path. The legacy `<= luminous` branch continues maintaining those caches.

Activation is correspondingly split:

```text
pre-Mimic:
    PGPool.cached_removed_snaps
              |
              v
          snap_trimq

Mimic+:
    OSDMap.removed_snaps_queue
              |
              +---- reconcile with pg_info_t.purged_snaps
              |
              v
          snap_trimq
```

The same change also consumes `new_removed_snaps` and `new_purged_snaps` from advancing OSDMaps while a PG is active. This is direct evidence that the transition changes both the retained source representation and how changes are propagated, while preserving the logical task of determining which retired snapshots still require trim work.

### 3. 2019-05-01 — `PeeringState` separates derivation from the PG execution queue

Ceph commit [`8885b0e54c99af7bf167e45bc1550ff7a0da4d46`](https://github.com/ceph/ceph/commit/8885b0e54c99af7bf167e45bc1550ff7a0da4d46), `PeeringState: restructure activate to avoid snap_trimq`, states its purpose directly: do not use `snap_trimq` while manipulating `info.purged_snaps`; instead pass the resulting `to_trim` set into `on_activate`.

The diff moves activation-time reconciliation into a local `interval_set<snapid_t> to_trim`. `PeeringState::activate` fills that set from the legacy cache or, on Mimic+, from OSDMap `removed_snaps_queue`; intersects it with `info.purged_snaps`; subtracts already-purged work; and passes the result through `on_activate(std::move(to_trim))`. The PG listener then assigns the received set to `snap_trimq`.

That source split supports a stronger representation boundary:

```text
retained reclamation authority
        != activation-time derived handoff
        != worker/execution queue object
```

The relation is preserved while the transient container used by the executor is deliberately kept out of the reconciliation step.

### 4. 2019-07-02/03 — Octopus-targeting cleanup retires the pre-Mimic representation branch

The July 2019 cleanup series removes the compatibility path rather than introducing the obligation relation for the first time:

- [`b59a25d9c985e414e3015c76f3fd84a1525afe3c`](https://github.com/ceph/ceph/commit/b59a25d9c985e414e3015c76f3fd84a1525afe3c), `osd/PG: drop pre-mimic snap_trimq code`;
- [`e963ee6039a29def026d90100e2ca5454b658649`](https://github.com/ceph/ceph/commit/e963ee6039a29def026d90100e2ca5454b658649), `osd/PeeringState: removed pre-mimic removed snap tracking`, which deletes `PGPool.cached_removed_snaps` / `newly_removed_snaps` and makes activation read OSDMap `removed_snaps_queue` unconditionally;
- [`cabc48c40332875e8827f4f0e6dbde9ab7e9fd7a`](https://github.com/ceph/ceph/commit/cabc48c40332875e8827f4f0e6dbde9ab7e9fd7a), `osd/PrimaryLogPG: use osdmap removed_snaps_queue for snap trimming`, which switches a trim-related removed-snapshot membership test to the OSDMap queue;
- merge [`1cc7617c8af0792ce0659d7855a2284cb680dc2c`](https://github.com/ceph/ceph/commit/1cc7617c8af0792ce0659d7855a2284cb680dc2c), 2019-07-03, integrates the wider pre-Octopus snapshot compatibility cleanup series.

The safe historical statement is therefore that the OSDMap representation was introduced and compatibility-gated in late 2017, `PeeringState` later took explicit ownership of activation-time derivation in May 2019, and the pre-Mimic branch was removed in the July 2019 Octopus-targeting cleanup. The merge date is an integration boundary, not an invention or production-rollout date.

## Engineering reconstruction

Across the inspected commits, the source-visible representation changes approximately as follows:

```text
2016 / legacy path
    PGPool.cached_removed_snaps
      - pg_info_t.purged_snaps
        -> pending snap_trimq

2017 Mimic path
    OSDMap.removed_snaps_queue
      + OSDMap epoch deltas
      reconciled with pg_info_t.purged_snaps
        -> pending snap_trimq

2019 PeeringState refactor
    OSDMap.removed_snaps_queue
      reconciled with pg_info_t.purged_snaps
        -> activation-local to_trim
          -> PG snap_trimq

2019 Octopus-targeting cleanup
    remove the pre-Mimic PGPool cache branch;
    OSDMap queue becomes the ordinary source for this obligation path.
```

The durable/reconstructible relation that matters is not byte identity of a particular queue object. It is enough to preserve the authority needed to distinguish retired-but-not-yet-accounted-as-purged work from completed work and to reconstruct the pending set at activation.

A compact project-level formulation is:

```text
same cleanup obligation relation
    != same container
    != same ownership layer
    != same transient scheduler object
```

## Claim-layer separation

### Historical record

The commit dates, messages, compatibility gates, field names, and source diffs above are public Ceph implementation records. They directly support the stated source-level transitions.

### Engineering reconstruction

`pending trim = retained removal obligation - completion evidence` is a compact reconstruction of the relation expressed by the inspected interval-set intersection/subtraction logic. It is useful for comparison, but it is not a quoted Ceph equation.

### Functional analogy

Case 125 ext3/ext4 orphan recovery retains an explicit cleanup target relation, while Case 153 can reconstruct pending snaptrim work from retirement and completion state; Case 73 GFS instead supplies an inventory/reconciliation contrast. These are functional strategies for carrying cleanup obligation across interruption. No common algorithm, implementation lineage, or influence claim follows.

### Philosophical interpretation

No new philosophical claim is required for this slice. The source work is sufficient to establish a narrower technical point: an obligation can remain recoverable while the software representation that carries or derives it changes.

## Negative claims / boundaries

This evidence does **not** establish that:

- `553048fb` is the invention of Ceph snap trimming, snapshot GC, or `purged_snaps`;
- the commit dates equal production deployment dates;
- `removed_snaps_queue` is a complete historical archive of every removed snapshot — its introducing commit explicitly narrows it toward current removed-but-not-purged work;
- `PeeringState::to_trim` is itself durable authority — it is an activation-time derived handoff;
- a reconstructed snapshot ID proves an exact per-object cursor, iterator, thread, or transaction resumed after crash;
- retrimming is universally idempotent or exactly-once;
- logical snaptrim completion proves BlueStore allocator reuse, Flash erase, sanitize, cryptographic erasure, or forensic irrecoverability;
- the 2017–2019 commits prove a genealogy to unrelated snapshot-GC systems.

## Related-repository check

A fresh search of `tmzncty/computing-archaeology` for `snaptrim` and `purged_snaps` found no dedicated treatment to reuse. This file therefore stays limited to the Ceph representation cutover. A broader history of distributed snapshot reclamation, GC terminology, or storage-engine allocator evolution belongs in the companion technical-history repository rather than being rebuilt here.

## Closure

This slice closes the roadmap item for the **commit-by-commit 2016-cache → 2017 OSDMap → 2019 PeeringState representation transition**. Still open are exact first-introduction genealogy before the 2016 documentary floor, per-object crash/fault-injection behavior, lower-layer allocator timing, and broader distributed snapshot-GC genealogy.
