# Case 153 Deepening — Ceph Snap-Trim Obligation Reconstruction Across PG Activation (2016–2026)

**Status:** evidence deepening for grounded Case 153

## Research question

Case 153 already establishes that retiring a RADOS snapshot can create asynchronous per-PG trim work and that `purged_snaps`, `SnapMapper`, PG log entries, replicas, peering, and recovery participate in maintaining that work. This slice asks a narrower failure/restart question:

> **Does unfinished snap trimming require the exact in-memory `snap_trimq` object to survive, or can the work queue be reconstructed from retained snapshot-retirement and completion state when a PG activates again?**

The bounded answer is that Ceph has documented and implemented queue **reconstruction**. A 2016 first-party PGPool document and source snapshot explicitly derive `snap_trimq` from the set of removed snapshots minus `info.purged_snaps`; current source has evolved the representation but preserves the same relation by deriving `to_trim` from the OSDMap's removed-snapshot queue minus the PG's `purged_snaps` before activation.

This supports a stronger retention distinction than the original Case 153 wording:

```text
retained reclamation obligation
!=
retention of the exact scheduler queue object
```

It does **not** establish exact per-object cursor persistence, exactly-once trimming, transaction-level crash atomicity for every storage backend, or secure media sanitization.

## Repository preflight

Before this slice:

- Case 153 was `grounded` from the 14-Mar-2013 `snaps.rst` record plus maintained Ceph documentation;
- its open debt explicitly included PG-state/recovery history and fault behavior;
- the latest Case-153 repository commits were `d881424e...` (`case153: ground Ceph RADOS snaptrim reclamation`) and `7e4d6f67...` (`case153: use current Ceph PG-state source`), both from 11-Sep-2026;
- fresh searches of `tmzncty/computing-archaeology` for `snaptrim`, `purged_snaps`, and `SnapMapper` found no dedicated study to reuse.

Decision: deepen only the restart/activation reconstruction seam here. Broader Ceph OSD/PG genealogy remains companion-repository work.

## Evidence classification

### E153R.1 — 15-Dec-2016 first-party `pgpool.rst` documents reconstruction inputs

- **Source:** Ceph commit `0f6be4c98cf26b0237cbfbe505c54eaedfe96351`, Brad Hubbard, committed 15-Dec-2016, message `doc/dev/osd_internals: add pgpool.rst`.
- **Frozen file:** `doc/dev/osd_internals/pgpool.rst` at that commit.
- **Class:** first-party source-control historical record (`H/P`).

The document says `PGPool` maintains:

- `cached_removed_snaps` — the current removed-snapshot set;
- `newly_removed_snaps` — snapshots newly removed in the latest epoch.

It further states that during `OSD::load_pgs` the OSD map is recovered from the PG's file store and used to initialize the pool state; later OSDMap updates merge newly removed snapshots into the cached removed set.

Most importantly, it says that when a PG activates, Ceph initializes the snap-trim queue from `cached_removed_snaps` and subtracts snapshots already represented in `purged_snaps`, leaving the snapshots that still need trimming. Asynchronous `snap_trim_wq` execution follows later.

This is direct historical evidence for:

```text
removed-snapshot authority set
-
already-purged completion set
=
pending snap-trim work set
```

The equation is an engineering restatement of the documented operation, not Ceph's own notation.

### E153R.2 — frozen 2016 `PG.cc` implements the documented subtraction

- **Source:** `src/osd/PG.cc` at commit `0f6be4c...`.
- **Class:** frozen first-party implementation evidence (`H/P/E`).

The source's `PGPool::update()` builds `newly_removed_snaps`, merges them into `cached_removed_snaps`, and tracks map epochs. In the PG activation path the source then:

1. copies `pool.cached_removed_snaps` into `snap_trimq`;
2. intersects that queue with `info.purged_snaps`;
3. subtracts the already-purged intersection from the queue.

The source therefore confirms that the queue is a **derived activation-time structure** rather than evidence that the exact prior in-memory work-queue object itself must be serialized unchanged.

The same code also contains a defensive branch for `info.purged_snaps` not being a subset of `pool.cached_removed_snaps`; this is useful as a reminder that reconstruction is a reconciliation operation, not a metaphysical identity between two containers.

### E153R.3 — maintained/current source preserves the relation while changing representation

- **Source snapshot:** Ceph `main` at `a2c71ca92826a08801d9e5e7668c5a14e94cce91` (12-Sep-2026).
- **Files:** `src/osd/PeeringState.cc`, `src/crimson/osd/pg.cc`, and maintained `doc/dev/osd_internals/snaps.rst`.
- **Class:** current first-party implementation/continuity evidence (`P-current/E`).

Current `PeeringState` no longer reconstructs from a field literally named `PGPool::cached_removed_snaps`. On primary activation it:

1. obtains the OSDMap `removed_snaps_queue` for the pool;
2. builds a local `to_trim` interval set from that retirement state;
3. computes the intersection with `info.purged_snaps`;
4. subtracts the purged portion;
5. passes the result to the PG activation callback as `to_trim`.

The current Crimson PG implementation makes the handoff especially explicit: `PG::on_activate(interval_set<snapid_t> snaps)` assigns the supplied set into `snap_trimq`.

Therefore the high-level relation survives a representation/refactoring change:

```text
2016: cached_removed_snaps - info.purged_snaps -> snap_trimq
2026: OSDMap removed_snaps_queue - info.purged_snaps -> to_trim -> snap_trimq
```

This is continuity of a retention relation, not evidence that the data structures are frozen across releases.

### E153R.4 — `purged_snaps` is completion evidence, not merely a transient worker flag

Maintained `snaps.rst` states that the primary shares PG info with replicas and that replicas persist the new set of `purged_snaps` along with the rest of the info. The same document says normal PG peering/recovery maintain snap-trimmer operations; if a `purged_snaps` update is lost, the consequence is that Ceph may retrim a now-empty snapshot.

For the bounded question, this supports two points:

- `purged_snaps` participates in persistent/replicated completion state used to suppress already-completed trim work during later reconstruction;
- loss of that completion evidence can cause **redundant re-execution** rather than proving that retirement authority or old clones silently become current again.

It does not prove universal exactly-once or transaction-level atomicity.

### E153R.5 — `SnapMapper` supplies membership state, not an exact worker cursor

Maintained snapshot internals describe `SnapMapper` as a backing-store-supported mapping in both directions:

- object -> set of snapshots;
- snapshot -> affected objects.

The trim worker uses that mapping to select objects for a snapshot and updates the mapping as object membership changes. This is sufficient to explain why reconstruction at the **snapshot-ID obligation level** need not imply replaying an identical volatile cursor object.

The inspected sources do not establish that the exact object-by-object iterator position or scheduling microstate survives a crash. Do not upgrade queue reconstruction into `resume at the exact instruction/object boundary`.

## Historical record versus engineering reconstruction

### Historical / primary record (H/P)

By 15-Dec-2016 Ceph's own developer documentation and matching source explicitly showed activation-time `snap_trimq` construction from removed snapshots minus already-purged snapshots. By the inspected 12-Sep-2026 mainline source, the concrete containers had changed but primary activation still computes pending snapshot IDs from current removal state minus `info.purged_snaps` and hands that derived set to the PG.

### Engineering reconstruction (E)

The retained relation can be expressed as:

```text
retirement knowledge R
completion knowledge P
pending obligation Q = R - P
```

`Q` may be materialized as a worker queue when the PG becomes active. Correctness therefore does not require `Q` to be the same in-memory object that existed before a process restart, provided the retained relations used to reconstruct it remain authoritative enough for the implementation's recovery rules.

This gives several bounded distinctions:

- `unfinished maintenance obligation persists != exact scheduler object persists`;
- `queue reconstructed != exact worker cursor restored`;
- `snapshot retirement remembered != trim completion remembered`;
- `completion evidence lost != retired snapshot becomes live again`;
- `re-execution tolerated in a documented case != universal exactly-once semantics`.

### Functional analogy (A)

Case 125 ext3/ext4 retains an explicit crash-persistent orphan target set. Case 153 demonstrates a different shape: the worker queue can be reconstructed from retirement state and completion state during PG activation. Case 73 GFS goes further toward reconciliation from current authority plus re-observed inventory.

The useful comparison is only:

> **a cleanup obligation can survive either as an explicit durable work structure or as a relation that allows pending work to be reconstructed.**

These systems do not share an algorithm or genealogy.

Synthesis 28 now records this narrower distinction so that `retained cleanup obligation` is not silently equated with `durably serialized worker queue`.

### Philosophical interpretation — bounded (I)

A technical obligation can persist through **reconstructibility** rather than through identity of the executor's temporary data structure. What must remain is enough authoritative relation to recover what work is still owed, not necessarily the exact queue object or instruction position that previously represented that work.

This is a project-level interpretation, not historical Ceph vocabulary.

## Counterevidence / stop conditions

### S153R.1 — 2016 is a documented-by floor, not first introduction

Commit `0f6be4c...` adds the PGPool document in 2016, but the corresponding mechanism can predate that documentation. This slice does not claim 2016 as the invention or first implementation of queue reconstruction.

### S153R.2 — do not freeze 2016 names into current Ceph

The 2016 document/source uses `cached_removed_snaps`; inspected current source builds `to_trim` from the OSDMap `removed_snaps_queue`. The relation is comparable, but the representation changed.

### S153R.3 — queue reconstruction is not exact cursor persistence

The evidence does not establish persistence of the exact `snap_trim_wq` scheduling order, a per-object iterator position, CPU/thread state, or byte-identical in-memory queue representation across restart.

### S153R.4 — retrim tolerance is not a universal exactly-once theorem

The maintained document's specific statement about losing a `purged_snaps` update and retrimming an empty snapshot is bounded. It does not prove all snaptrim sub-operations are idempotent under every crash point or backend failure.

### S153R.5 — no lower-layer erase/sanitize conclusion

Reconstructing pending clone cleanup says nothing by itself about BlueStore allocator reuse timing, SSD FTL erase, cryptographic erasure, or forensic irrecoverability.

## What this slice closes

This closes one bounded Case-153 recovery debt:

> **unfinished snapshot-reclamation work can be reconstructed at PG activation from retained removal/completion relations; retention of the exact old in-memory trim queue is not required by the documented mechanism.**

Still open:

- exact first-introduction genealogy of this reconstruction mechanism;
- commit-by-commit transition from 2016 `cached_removed_snaps` to current `removed_snaps_queue` / `PeeringState` representation;
- exact per-object crash windows and backend transaction atomicity;
- deliberate OSD-kill/fault-injection validation during snaptrim;
- lower-layer allocator/free-space timing after clone removal;
- broader distributed snapshot-GC genealogy.

The broader engineering/history belongs primarily in `tmzncty/computing-archaeology`; a fresh search found no dedicated snaptrim study there to reuse in this pass.

## Sources

1. Ceph commit `0f6be4c98cf26b0237cbfbe505c54eaedfe96351`, **`doc/dev/osd_internals: add pgpool.rst`**, 2016-12-15:
   <https://github.com/ceph/ceph/commit/0f6be4c98cf26b0237cbfbe505c54eaedfe96351>
2. Frozen `pgpool.rst` at that commit:
   <https://github.com/ceph/ceph/blob/0f6be4c98cf26b0237cbfbe505c54eaedfe96351/doc/dev/osd_internals/pgpool.rst>
3. Frozen `src/osd/PG.cc` at that commit:
   <https://github.com/ceph/ceph/blob/0f6be4c98cf26b0237cbfbe505c54eaedfe96351/src/osd/PG.cc>
4. Ceph main snapshot `a2c71ca92826a08801d9e5e7668c5a14e94cce91`, 2026-09-12:
   <https://github.com/ceph/ceph/commit/a2c71ca92826a08801d9e5e7668c5a14e94cce91>
5. Current `PeeringState.cc` at that snapshot:
   <https://github.com/ceph/ceph/blob/a2c71ca92826a08801d9e5e7668c5a14e94cce91/src/osd/PeeringState.cc>
6. Current Crimson PG activation implementation at that snapshot:
   <https://github.com/ceph/ceph/blob/a2c71ca92826a08801d9e5e7668c5a14e94cce91/src/crimson/osd/pg.cc>
7. Maintained snapshot internals at that snapshot:
   <https://github.com/ceph/ceph/blob/a2c71ca92826a08801d9e5e7668c5a14e94cce91/doc/dev/osd_internals/snaps.rst>
8. Rendered Mimic PGPool documentation (continuity witness, not first-introduction evidence):
   <https://docs.ceph.com/en/mimic/dev/osd_internals/pgpool/>
