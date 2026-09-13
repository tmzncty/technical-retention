from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"anchor missing in {path}: {old[:220]!r}")
    if text.count(old) != 1:
        raise SystemExit(f"anchor not unique in {path}: {old[:220]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


def insert_before_once(path: str, anchor: str, addition: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if anchor not in text:
        raise SystemExit(f"anchor missing in {path}: {anchor[:220]!r}")
    if text.count(anchor) != 1:
        raise SystemExit(f"anchor not unique in {path}: {anchor[:220]!r}")
    p.write_text(text.replace(anchor, addition + anchor, 1), encoding="utf-8")


def insert_after_line_prefix(path: str, prefix: str, addition: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    hits = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    if len(hits) != 1:
        raise SystemExit(f"expected one line prefix in {path}, got {len(hits)}: {prefix!r}")
    i = hits[0]
    lines.insert(i + 1, addition)
    p.write_text("".join(lines), encoding="utf-8")


repo = Path(".")
evidence_path = repo / "evidence/153-ceph-2016-pg-activation-trim-obligation-reconstruction-deepening.md"
case_path = "cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md"
roadmap_path = "ROADMAP.md"
index_path = "CASE_INDEX.md"
synthesis_path = "docs/SYNTHESIS_28_RECLAMATION_AUTHORITY_AFTER_RETIREMENT.md"

if evidence_path.exists():
    raise SystemExit(f"evidence already exists: {evidence_path}")

EVIDENCE = r'''# Case 153 Deepening — Ceph Snap-Trim Obligation Reconstruction Across PG Activation (2016–2026)

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
'''

evidence_path.write_text(EVIDENCE, encoding="utf-8")

CASE_DEEPENING = r'''## PG-activation reconstruction deepening: the obligation can survive without the old queue object

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

'''

insert_before_once(case_path, "## Prior art and genealogy boundary\n", CASE_DEEPENING)

# Add the new evidence record to the case-index table row without rewriting the case's established status.
replace_once(
    index_path,
    "[2013 source-tree + maintained Ceph grounding](evidence/153-ceph-2013-snaptrim-asynchronous-reclamation-grounding.md); first-introduction genealogy, internal representation transitions, lower-layer allocator timing, and fault injection remain open",
    "[2013 source-tree + maintained Ceph grounding](evidence/153-ceph-2013-snaptrim-asynchronous-reclamation-grounding.md) + [2016 PG-activation reconstruction deepening](evidence/153-ceph-2016-pg-activation-trim-obligation-reconstruction-deepening.md); activation-time queue reconstruction is now grounded, while first-introduction genealogy, internal representation transitions, exact per-object crash windows, lower-layer allocator timing, and fault injection remain open"
)

ROADMAP_ADDITION = r'''- [x] **Case 153 PG-activation / snap-trim obligation reconstruction deepening** — [`evidence/153-ceph-2016-pg-activation-trim-obligation-reconstruction-deepening.md`](evidence/153-ceph-2016-pg-activation-trim-obligation-reconstruction-deepening.md) closes a bounded restart-state seam left by the initial snaptrim case. Ceph's 15-Dec-2016 `pgpool.rst` plus matching `PG.cc` explicitly reconstruct `snap_trimq` at PG activation as removed snapshots minus `info.purged_snaps`; the inspected 12-Sep-2026 mainline source preserves the relation while moving it into `PeeringState`/OSDMap `removed_snaps_queue` and an activation `to_trim` handoff. This fixes `retained cleanup obligation != retained exact worker-queue object`, `queue reconstruction != exact cursor resume`, and `lost completion evidence can cause retrim != retired snapshot becomes live again`. Exact first-introduction genealogy, the representation-transition commit chain, per-object crash/fault injection, and lower-layer allocator timing remain open; fresh `computing-archaeology` search again found no dedicated snaptrim study to reuse.
'''
insert_after_line_prefix(
    roadmap_path,
    "- [x] **Case 153 Ceph RADOS snap-trimming / asynchronous snapshot-reclamation slice**",
    ROADMAP_ADDITION,
)

SYNTHESIS_ADDITION = r'''### A retained obligation need not be the worker queue itself

Case 153 now supplies a useful refinement to the phrase **retained cleanup obligation**. A 2016 Ceph implementation/documentation slice reconstructs `snap_trimq` at PG activation from the removed-snapshot relation minus `purged_snaps`; current source preserves the subtraction relation through different data structures. The obligation can therefore survive because the inputs needed to *derive pending work* remain available, even if the old in-memory queue object and exact worker cursor do not.

This gives a third shape between a literally durable work list and pure re-observation:

```text
authoritative retirement state
        +
retained completion state
        ↓
reconstructed pending-work set
```

For Synthesis 28, the rule is therefore:

> **retained cleanup obligation != necessarily a durably serialized scheduler queue.**

The comparison with ext3/ext4's explicit orphan tracking and GFS's reconciliation from current authority/inventory is functional only. It does not imply shared algorithms or genealogy.

'''
insert_before_once(synthesis_path, "## 8. E — forgetting stale state can require active preservation of live state\n", SYNTHESIS_ADDITION)

# Append a bounded findings block. 3859 is the current tail at the preflight HEAD.
p = Path(index_path)
text = p.read_text(encoding="utf-8")
if "### Findings 3860–3875" in text or "**3860 —" in text:
    raise SystemExit("Case 153 reconstruction findings already present")
if "**3859 —" not in text:
    raise SystemExit("expected current CASE_INDEX tail finding 3859")

FINDINGS = r'''

### Findings 3860–3875 — Case 153 Ceph snaptrim PG-activation obligation reconstruction

- **3860 — H/P** — Ceph commit `0f6be4c98cf26b0237cbfbe505c54eaedfe96351`, committed 15-Dec-2016, added a first-party `pgpool.rst` document describing how removed-snapshot state feeds snap trimming; this is a documented-by floor, not an invention date.
- **3861 — H/P** — The 2016 PGPool document distinguishes `cached_removed_snaps` from `newly_removed_snaps` and says OSDMap state recovered during PG loading initializes pool state before later map updates extend the removed-snapshot set.
- **3862 — H/P/E** — The same document explicitly says PG activation initializes the snap-trim queue from `cached_removed_snaps` and subtracts already completed `purged_snaps`, leaving snapshots that still need trimming.
- **3863 — H/P** — Frozen `PG.cc` at the same commit independently implements the documented relation: `snap_trimq = pool.cached_removed_snaps`, followed by intersection/subtraction against `info.purged_snaps`.
- **3864 — E** — In that implementation, pending reclamation work is therefore derivable from retained retirement state plus retained completion state; the exact old in-memory queue object is not the sole carrier of the obligation.
- **3865 — E** — `unfinished maintenance obligation persists != exact scheduler queue persists`: PG activation can materialize a new queue from authoritative/recovery state.
- **3866 — E/X** — `queue reconstructed != exact worker cursor restored`; the inspected sources do not establish persistence of thread state, scheduling order, or exact object-by-object iterator position across restart.
- **3867 — P-current** — Inspected Ceph main source at `a2c71ca9...` (12-Sep-2026) builds a primary-activation `to_trim` set from the OSDMap `removed_snaps_queue`, subtracts the intersection with `info.purged_snaps`, and passes the result into the PG activation callback.
- **3868 — P-current/E** — Current Crimson PG code assigns the activation-provided snapshot set into `snap_trimq`, making the queue-materialization step explicit in a present implementation path.
- **3869 — E/X** — The 2016 `cached_removed_snaps` representation and current `removed_snaps_queue`/`PeeringState` representation support a stable subtraction relation but are not claimed to be the same data structure or an uninterrupted byte-level implementation lineage.
- **3870 — P-current** — Maintained `snaps.rst` says the primary shares PG info with replicas and replicas persist the new `purged_snaps` set along with the rest of the info; completion state is therefore stronger than a transient worker-local flag in the documented design.
- **3871 — P-current/E** — Maintained recovery documentation says losing a `purged_snaps` update can cause Ceph to retrim a now-empty snapshot, providing a bounded example where missing completion evidence yields redundant work rather than renewed snapshot authority.
- **3872 — E/X** — The documented empty-retrim case does not establish universal exactly-once, universal idempotence, or transaction-level crash atomicity for every snaptrim sub-operation/backend.
- **3873 — FA** — ext3/ext4 orphan tracking, Ceph activation-time queue reconstruction, and GFS re-observation represent different functional ways to preserve or recover cleanup obligations; the comparison does not imply shared algorithms or genealogy.
- **3874 — E/I** — A technical obligation can remain persistent through reconstructibility of `work still owed` even when the executor's temporary queue identity is not retained; this is project interpretation, not historical Ceph vocabulary.
- **3875 — X** — Reconstructing snaptrim work does not prove BlueStore allocator reuse timing, SSD physical erase, cryptographic erasure, sanitization, forensic irrecoverability, or the 2016 mechanism's first-introduction date.
'''

p.write_text(text.rstrip() + FINDINGS + "\n", encoding="utf-8")
