from pathlib import Path
import subprocess


def append_once(path: str, marker: str, block: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if marker in text:
        return
    if not text.endswith("\n"):
        text += "\n"
    text += "\n" + block.strip() + "\n"
    p.write_text(text, encoding="utf-8")


evidence_path = Path("evidence/153-ceph-2017-2019-removed-snaps-representation-transition-deepening.md")
evidence_path.write_text(r'''# Evidence 153C — Ceph 2017–2019 Removed-Snapshot Obligation Representation Transition

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
''', encoding="utf-8")

append_once(
    "cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md",
    "## 2017–2019 representation transition deepening",
    r'''
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
''')

append_once(
    "evidence/153-ceph-2016-pg-activation-trim-obligation-reconstruction-deepening.md",
    "## Follow-on closure: 2017–2019 representation transition",
    r'''
## Follow-on closure: 2017–2019 representation transition

The representation-transition debt intentionally left open by this record is now closed by [`153-ceph-2017-2019-removed-snaps-representation-transition-deepening.md`](153-ceph-2017-2019-removed-snaps-representation-transition-deepening.md). That follow-on traces the December-2017 Mimic OSDMap cutover, the May-2019 `PeeringState` `to_trim` separation, and the July-2019 removal of the pre-Mimic PGPool cache path. Exact first-introduction genealogy, per-object crash/fault injection, and lower-layer allocator timing remain open.
''')

roadmap = Path("ROADMAP.md")
rt = roadmap.read_text(encoding="utf-8")
old_open = "Exact first-introduction genealogy, the representation-transition commit chain, per-object crash/fault injection, and lower-layer allocator timing remain open;"
new_open = "Exact first-introduction genealogy, per-object crash/fault injection, and lower-layer allocator timing remain open;"
if old_open in rt:
    rt = rt.replace(old_open, new_open, 1)
marker = "**Case 153 2017–2019 removed-snapshot representation transition deepening:**"
if marker not in rt:
    anchor = "- [x] **Cross-case reclamation-authority synthesis**"
    if anchor not in rt:
        raise RuntimeError("ROADMAP insertion anchor missing")
    bullet = "- [x] **Case 153 2017–2019 removed-snapshot representation transition deepening:** [`cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md`](cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md) + [`evidence/153-ceph-2017-2019-removed-snaps-representation-transition-deepening.md`](evidence/153-ceph-2017-2019-removed-snaps-representation-transition-deepening.md) close the commit-chain debt left by the activation-reconstruction slice. Ceph `553048fb` (1-Dec-2017) moves the current removed-but-not-purged obligation into OSDMap `removed_snaps_queue` with per-epoch `new_removed_snaps` / `new_purged_snaps`; `6e1b7c4` makes that path Mimic-gated while retaining the PGPool cache only for <= Luminous; `8885b0e` (1-May-2019) derives an activation-local `to_trim` in `PeeringState` before materializing `snap_trimq`; and the 2–3 Jul 2019 Octopus-targeting cleanup removes the legacy branch. This closes `same cleanup obligation relation != same container/ownership layer/transient worker queue` without claiming first invention, production deployment dates, exact cursor resume, universal idempotence, or lower-layer physical reclamation. Exact pre-2016 introduction genealogy, per-object crash/fault injection, allocator timing, and broad distributed snapshot-GC genealogy remain open; fresh `computing-archaeology` search found no dedicated snaptrim study to reuse.\n"
    rt = rt.replace(anchor, bullet + "\n" + anchor, 1)
roadmap.write_text(rt, encoding="utf-8")

idx = Path("CASE_INDEX.md")
it = idx.read_text(encoding="utf-8")
idx_marker = "## Findings 3892–3907 — Case 153 Ceph removed-snapshot representation transition deepening"
if idx_marker not in it:
    findings = r'''

## Findings 3892–3907 — Case 153 Ceph removed-snapshot representation transition deepening

- **Finding 3892 (H/P)** — Ceph commit `553048fb` on 1-Dec-2017 explicitly replaces the idea of maintaining removed snapshot IDs over all time with per-epoch newly removed/newly purged deltas plus an OSDMap interval of snapshots removed but not yet purged.
- **Finding 3893 (H/P)** — The introducing `removed_snaps_queue` commit describes its steady-state scope as snapshots currently being removed and exposes it as the cluster's trimming-snapshot set; it is therefore not safely characterized as a complete historical archive of removals.
- **Finding 3894 (E)** — `new_removed_snaps` union and `new_purged_snaps` subtraction make the OSDMap queue a current unresolved-reclamation relation rather than merely a renamed copy of the earlier all-time set.
- **Finding 3895 (H/P)** — Same-day commit `6e1b7c4` gates the new path on `require_osd_release >= MIMIC` and explicitly says OSDMap tracks `removed_snaps_queue` while `pg_info_t` tracks `purged_snaps` with map deltas.
- **Finding 3896 (H/P)** — The `<= luminous` branch in `6e1b7c4` continues maintaining `PGPool.cached_removed_snaps` / `newly_removed_snaps`; the representation transition is therefore compatibility-gated, not an instantaneous global rename.
- **Finding 3897 (H/P)** — On the Mimic path, PG activation initializes trim candidates from OSDMap `removed_snaps_queue` rather than the PGPool cache.
- **Finding 3898 (E)** — Activation intersects candidate trim work with `info.purged_snaps`, subtracts completion evidence from the candidates, and reconciles local purge knowledge; this supports the compact reconstruction `pending work = retained removal obligation - recorded completion` without making it historical Ceph vocabulary.
- **Finding 3899 (H/P)** — While active, the Mimic path consumes OSDMap `new_removed_snaps` and `new_purged_snaps`, showing that the cutover changes both the retained source representation and how obligation/completion changes are propagated.
- **Finding 3900 (H/P)** — Commit `8885b0e` on 1-May-2019 explicitly restructures activation to avoid manipulating `snap_trimq` while reconciling `info.purged_snaps`, deriving a local `to_trim` set in `PeeringState` instead.
- **Finding 3901 (H/P)** — In `8885b0e`, `PeeringState` passes the derived `to_trim` through `on_activate`, and the PG listener then assigns it to `snap_trimq`; derivation and execution-queue materialization are source-visible separate steps.
- **Finding 3902 (E)** — The 2019 refactor supports `retained reclamation authority != activation-time derived handoff != in-memory worker queue`; preserving the obligation does not require preserving one exact scheduler object.
- **Finding 3903 (H/P)** — The 2-Jul-2019 Octopus-targeting cleanup (`b59a25d`, `e963ee6`) removes the pre-Mimic snap-trim/cache path, leaving OSDMap `removed_snaps_queue` as the ordinary activation source rather than inventing the obligation relation at that date.
- **Finding 3904 (H/P)** — Commit `cabc48c` switches a `PrimaryLogPG` snap-trim membership check to OSDMap `removed_snaps_queue`, further consolidating the OSDMap representation in the same cleanup series.
- **Finding 3905 (X)** — The 2017 implementation commits, 2019 refactor/cleanup commits, and 3-Jul-2019 merge are source-history boundaries; they do not by themselves establish first invention, first production deployment, or first user-visible release dates.
- **Finding 3906 (X)** — This representation genealogy does not establish exact per-object cursor resume, universal exactly-once/idempotent trim behavior, BlueStore allocator reuse timing, Flash erase, sanitization, or forensic irrecoverability.
- **Finding 3907 (FA/E)** — Cases 125, 153, and 73 support a bounded functional comparison among explicit durable cleanup-target tracking, reconstruction from retirement/completion state, and re-observation/reconciliation; the comparison does not establish shared algorithms or genealogy.
'''
    if not it.endswith("\n"):
        it += "\n"
    it += findings
    idx.write_text(it, encoding="utf-8")

# Remove temporary integration scaffolding before the canonical commit.
Path(".github/workflows/tmp-case153-cutover.yml").unlink(missing_ok=True)
Path("tools/tmp_case153_integrate.py").unlink(missing_ok=True)

subprocess.run(["git", "config", "user.name", "Tmzncty"], check=True)
subprocess.run(["git", "config", "user.email", "72063145+tmzncty@users.noreply.github.com"], check=True)
subprocess.run(["git", "add", "-A"], check=True)
subprocess.run(["git", "diff", "--cached", "--check"], check=True)
subprocess.run(["git", "commit", "-m", "case153: trace removed-snap representation cutover [skip ci]"], check=True)
subprocess.run(["git", "push", "origin", "HEAD:main"], check=True)
