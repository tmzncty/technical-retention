from pathlib import Path

EVIDENCE_PATH = Path("evidence/129-zfs-async-destroy-reclamation-compatibility-deepening.md")
CASE_PATH = Path("cases/129-zfs-feature-flags-format-compatibility.md")
ROADMAP_PATH = Path("ROADMAP.md")
INDEX_PATH = Path("CASE_INDEX.md")
WORKFLOW_PATH = Path(".github/workflows/integrate-case129-async-destroy.yml")
SELF_PATH = Path(".github/scripts/integrate-case129.py")

if EVIDENCE_PATH.exists():
    raise SystemExit("evidence file already exists; refusing duplicate integration")

evidence = r'''# Evidence 129B — OpenZFS `async_destroy`: reclamation lifetime and feature-state compatibility

**Status:** `grounded`  
**Case:** [`../cases/129-zfs-feature-flags-format-compatibility.md`](../cases/129-zfs-feature-flags-format-compatibility.md)  
**Bounded question:** when `async_destroy` allows logical destroy to return before all space has been reclaimed, can the unfinished reclamation relation itself keep the pool feature active and therefore retain a software-compatibility requirement?

## Evidence boundary

Case 129 already establishes the general ZFS feature-flag relation between retained format requirements and software admissibility. This slice asks one narrower, feature-specific question about `com.delphix:async_destroy`:

```text
logical destroy completion
    != background space-reclamation completion
    != relaxation of this feature's active-state compatibility obligation
```

The historical/project record below uses released OpenZFS documentation plus a pinned released source tree. It does not reconstruct invention priority, a complete illumos/OpenZFS genealogy, or a generic rule for every ZFS feature.

## Primary technical sources

- OpenZFS v0.6, `zpool-features(5)`: <https://openzfs.github.io/openzfs-docs/man/v0.6/5/zpool-features.5.html>
- OpenZFS v0.6, `zpool(8)`: <https://openzfs.github.io/openzfs-docs/man/v0.6/8/zpool.8.html>
- OpenZFS current `zpool-features(7)`: <https://openzfs.github.io/openzfs-docs/man/master/7/zpool-features.7.html>
- OpenZFS current Feature Flags concept documentation: <https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Pool%20Structure/Feature%20Flags.html>
- OpenZFS `zfs-2.2.8`, `module/zcommon/zfeature_common.c`: <https://github.com/openzfs/zfs/blob/zfs-2.2.8/module/zcommon/zfeature_common.c>
- Historical feature-flags integration already grounded in the parent case: illumos `ad135b5d644628e791c3188a6ecbd9c257961ef8`, 21 May 2012: <https://github.com/illumos/illumos-gate/commit/ad135b5d644628e791c3188a6ecbd9c257961ef8>

Current documentation and the 2.2.8 source are continuity witnesses. They are not projected backward as proof that every historical release had identical code paths.

---

## Historical / project record

### H/P — `async_destroy` separates destroy completion from completion of space reclamation

The OpenZFS v0.6 feature documentation explains that, without `async_destroy`, destroying a filesystem requires traversing its data so used space can be returned to the pool before the filesystem is fully removed. With `async_destroy` enabled, used-space reclamation is instead performed by a background process, allowing the destroy operation to complete without traversing the entire filesystem first.

The same documentation says an interrupted asynchronous destroy can resume after the pool has been opened.

Therefore the released project documentation directly establishes:

> **destroy operation can complete != all corresponding space has already been reclaimed.**

### H/P — `freeing` exposes remaining asynchronous reclamation work

The feature page says the amount of space still to be reclaimed by the background process is exposed through the `freeing` property. The contemporaneous `zpool(8)` documentation likewise describes `freeing` as space from destroyed filesystems or snapshots that is still being returned asynchronously; as reclamation proceeds, that quantity decreases while ordinary free space increases.

`freeing` is therefore operator-visible evidence about outstanding reclamation. It is not a second copy of the destroyed payload.

### H/P — `async_destroy` is active only while `freeing` is non-zero

The released feature documentation states explicitly that `async_destroy` is active only while `freeing` is non-zero. Current `zpool-features(7)` retains the same feature-specific rule.

This matters because generic feature-state semantics distinguish:

- **enabled** — the feature is permitted but the on-disk change is not currently in effect;
- **active** — the feature's on-disk change is in effect and supporting software is required for read-write import.

Thus the outstanding reclamation quantity and this feature's compatibility state are directly coupled by project documentation.

### H/P — the feature is read-only compatible, not universally import-blocking

OpenZFS documents `com.delphix:async_destroy` as **READ-ONLY COMPATIBLE: yes** and with no dependencies. The pinned OpenZFS 2.2.8 source registers `SPA_FEATURE_ASYNC_DESTROY` with `ZFEATURE_FLAG_READONLY_COMPAT`.

This is a useful boundary: if unsupported active features are all read-only compatible, lack of support can forbid read-write import without necessarily forbidding read-only access.

Therefore:

> **active unsupported feature != every form of import impossible.**

### H/P — enablement is one-way even though this feature's activity can be episodic

The generic feature-state documentation says that once a feature is enabled it cannot be disabled. It also says some features may later return from `active` to `enabled`; `async_destroy` supplies a concrete case because its active state is tied to non-zero `freeing`.

For this feature, the relevant state path is therefore bounded as:

```text
disabled
  -> enabled / inactive
  -> active while `freeing > 0`
  -> enabled / inactive after `freeing == 0`
```

The final state is **not** a return to `disabled`.

---

## Engineering reconstruction

### E — outstanding reclamation can retain a read-write interpreter obligation

Combining the feature-specific and generic project documentation gives this bounded reconstruction:

```text
destroy returns
    ↓
background reclamation remains (`freeing > 0`)
    ↓
`com.delphix:async_destroy` remains active
    ↓
feature support remains required for read-write import
    ↓
background reclamation drains (`freeing == 0`)
    ↓
this feature returns to enabled / inactive
```

Calling the outstanding work a **reclamation debt** or **compatibility obligation** is project vocabulary, not OpenZFS wording. The source-supported facts are the background reclaim process, the `freeing` quantity, the active-while-nonzero rule, and the generic import contract.

This gives a concrete retention relation in which unfinished maintenance/reclamation state can prolong a software requirement after the user-visible deletion operation has already completed.

### E — compatibility-state relaxation is not rollback to the pre-feature pool

When `freeing` reaches zero, this feature ceases to be active, but the feature remains enabled. Therefore:

> **active -> enabled/inactive != enabled -> disabled rollback.**

Likewise, `freeing == 0` does not establish byte identity with the pool state before the destroy, before feature enablement, or before background reclamation began.

### E — `freeing` is relation/accounting evidence, not an embodiment map

The property reports the amount of space still being reclaimed. It does not identify exact device sectors, prove that every unreclaimed logical block remains physically readable, or establish how a particular storage device internally remapped data.

Therefore:

> **`freeing > 0` != exact physical block map.**

and:

> **`freeing == 0` != sanitization or forensic non-recoverability proof.**

---

## Functional comparison

### A — Case 153 Ceph asynchronous SnapTrim

Case 153 and this slice share one bounded functional pattern:

> **logical deletion accepted/completed != asynchronous reclamation obligation completed.**

The mechanisms are not treated as equivalent. Ceph's SnapTrim state machine and ZFS `async_destroy` have different implementations and histories. The additional fact established here is specifically ZFS's documented coupling between outstanding reclamation and the pool feature's active compatibility state.

No Ceph -> ZFS or ZFS -> Ceph genealogy is asserted.

---

## Rejected / unsupported claims

- **X — destroy return proves all old blocks are already free.** Released OpenZFS documentation explicitly separates operation completion from background reclamation.
- **X — `async_destroy` being enabled means it is always active.** Its documented active condition is non-zero `freeing`.
- **X — after `freeing` drains, the feature becomes disabled again.** Generic feature semantics say enabled features cannot be disabled; this feature can instead return to enabled/inactive.
- **X — an active `async_destroy` feature makes every unsupported import impossible.** It is documented and source-registered as read-only compatible.
- **X — `freeing` identifies exact unreclaimed physical sectors.** It is an aggregate reclamation quantity, not an embodiment map.
- **X — `freeing == 0` proves secure deletion, sanitization, exact physical erasure, or forensic non-recoverability.** No source in this slice supports that escalation.
- **X — every ZFS feature has the same active/inactive lifetime.** Activation/deactivation rules are feature-specific.
- **X — the 2012 feature-flags date establishes invention priority for asynchronous deletion or feature-controlled compatibility.** It is an implementation chronology anchor only.
- **X — ZFS `async_destroy` and Ceph SnapTrim are the same mechanism or share a proven genealogy.** The comparison is functional only.

## Claim ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| `async_destroy` lets destroy complete before all space reclamation finishes | `H/P` | released OpenZFS feature documentation |
| interrupted background destroy work can resume after pool open | `H/P` | released OpenZFS feature documentation |
| `freeing` exposes remaining asynchronous reclamation quantity | `H/P` | OpenZFS `zpool-features` + `zpool` docs |
| `async_destroy` is active only while `freeing != 0` | `H/P` | explicit feature-specific documentation |
| `async_destroy` is read-only compatible | `H/P` | docs + pinned 2.2.8 registration source |
| feature enablement cannot be reversed to disabled | `H/P` | generic feature-state documentation |
| outstanding reclamation can preserve this feature's read-write interpreter obligation | `E` | reconstruction from documented rules |
| drained reclamation can relax activity without undoing enablement | `E` | generic + feature-specific state boundaries |
| Ceph SnapTrim is a functional asynchronous-reclamation analogy only | `A` | cross-case comparison |
| zero `freeing` proves sanitization | `X` | unsupported by source scope |

## Related-repository check and remaining debt

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for ZFS feature flags and `async_destroy` found no dedicated module to reuse in this round.

Still open after this slice:

- source-level refcount transitions and crash/fault matrices for `async_destroy`;
- release-by-release compatibility matrices across illumos/OpenZFS/FreeBSD/other descendants;
- ext-family and other filesystem feature-bit prior art;
- bootloader, send-stream, dataset-feature, migration, emulation, and corruption-test matrices;
- broader asynchronous-delete and feature-bit genealogy, which should primarily live in `computing-archaeology` rather than be rebuilt here.
'''
EVIDENCE_PATH.write_text(evidence, encoding="utf-8")

case = CASE_PATH.read_text(encoding="utf-8")
marker = "## Evidence deepening 129B — `async_destroy` reclamation lifetime and compatibility state"
if marker in case:
    raise SystemExit("case129 deepening already integrated")
case_add = r'''
## Evidence deepening 129B — `async_destroy` reclamation lifetime and compatibility state

New [`Evidence 129B`](../evidence/129-zfs-async-destroy-reclamation-compatibility-deepening.md) grounds one feature-specific lifetime that the baseline feature-flags case previously left implicit.

Released OpenZFS documentation says `async_destroy` lets a destroy operation complete while used space is still being returned by a background process; interrupted work can resume after the pool opens, and remaining work is exposed as `freeing`. The feature-specific rule is unusually direct: **`com.delphix:async_destroy` is active only while `freeing` is non-zero**. OpenZFS also documents and source-registers it as read-only compatible.

Historical/project record:

```text
destroy operation completed
    != background reclaim completed

`freeing > 0`
    -> `async_destroy` active
    -> feature support required for read-write import
```

The generic feature contract adds a second boundary: once enabled, a feature cannot be disabled, even though some features can return from `active` to `enabled`. For `async_destroy`, draining `freeing` can therefore relax the active compatibility requirement without returning the pool to a pre-feature state.

Engineering reconstruction, not project wording:

> **an outstanding asynchronous reclamation relation can prolong a read-write software-compatibility obligation after logical deletion has completed; completion of that reclamation can relax activity without undoing feature enablement.**

This conclusion is feature-specific. `freeing == 0` is neither byte-identical rollback nor a physical-sector erasure/sanitization witness. The bounded functional analogy to [Case 153](153-ceph-rados-snaptrim-asynchronous-reclamation.md) is only `logical deletion != asynchronous reclamation completion`; Ceph SnapTrim and ZFS `async_destroy` are not treated as one mechanism or genealogy.

'''
anchor = "\n## Limits\n"
if anchor not in case:
    raise SystemExit("Case 129 Limits anchor not found")
CASE_PATH.write_text(case.replace(anchor, "\n" + case_add + "## Limits\n", 1), encoding="utf-8")

roadmap = ROADMAP_PATH.read_text(encoding="utf-8")
roadmap_marker = "Case 129 async_destroy reclamation / compatibility deepening"
if roadmap_marker in roadmap:
    raise SystemExit("roadmap deepening already integrated")
roadmap_anchor = "- [x] Case 129 ZFS/OpenZFS feature-flags / format-software compatibility boundary"
lines = roadmap.splitlines()
idx = next((i for i, line in enumerate(lines) if line.startswith(roadmap_anchor)), None)
if idx is None:
    raise SystemExit("Case 129 roadmap anchor not found")
roadmap_line = (
    "- [x] Case 129 async_destroy reclamation / compatibility deepening — "
    "[`cases/129-zfs-feature-flags-format-compatibility.md`](cases/129-zfs-feature-flags-format-compatibility.md), "
    "with [`evidence/129-zfs-async-destroy-reclamation-compatibility-deepening.md`](evidence/129-zfs-async-destroy-reclamation-compatibility-deepening.md): "
    "released OpenZFS documentation separates destroy completion from background space return, exposes remaining work as `freeing`, and states that `com.delphix:async_destroy` is active only while `freeing` is non-zero. The pinned 2.2.8 source independently registers it as read-only compatible. Combined with generic feature-state rules, this grounds `outstanding reclamation -> active read-write compatibility requirement`, while also showing `activity can drain -> enabled/inactive` without reversing feature enablement. `freeing == 0` is not rollback or sanitization evidence. Exact refcount/crash matrices, release genealogy, and broad feature-bit/asynchronous-delete history remain open and should primarily route to `computing-archaeology`."
)
lines.insert(idx + 1, roadmap_line)
ROADMAP_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

index = INDEX_PATH.read_text(encoding="utf-8").rstrip()
heading = "### Findings 3684–3699 — Case 129 async_destroy reclamation / compatibility lifetime"
if heading in index:
    raise SystemExit("CASE_INDEX findings already integrated")
if index.count("**3683 —") != 1:
    raise SystemExit(f"expected exactly one finding 3683, saw {index.count('**3683 —')}")
findings = r'''

### Findings 3684–3699 — Case 129 async_destroy reclamation / compatibility lifetime

- **3684 — H/P** — Released OpenZFS documentation says `async_destroy` allows a filesystem destroy operation to complete while used space is reclaimed later by a background process.
- **3685 — H/P** — The same documentation says interrupted asynchronous destroy work can resume after the pool is opened, so the reclamation obligation can survive an interruption/open boundary.
- **3686 — H/P** — OpenZFS exposes the amount still to be reclaimed by the background destroy process through the pool `freeing` property.
- **3687 — H/P** — The `async_destroy` feature documentation explicitly states that the feature is active only while `freeing` is non-zero.
- **3688 — H/P** — `com.delphix:async_destroy` is documented as read-only compatible and without dependencies; OpenZFS 2.2.8 source registers it with `ZFEATURE_FLAG_READONLY_COMPAT`.
- **3689 — H/P** — Generic ZFS feature-state semantics define `active` as an on-disk format change in effect for which supporting software is required for read-write import.
- **3690 — H/P** — Generic semantics distinguish `enabled` but inactive features, and state that once a feature is enabled it cannot be disabled even though some features may later return from active to enabled.
- **3691 — E** — For `async_destroy`, outstanding reclamation (`freeing > 0`) is therefore also a persistence condition for this feature's read-write software-support obligation.
- **3692 — E** — Logical destroy completion can precede both space-reclamation completion and relaxation of this feature's active-state compatibility requirement.
- **3693 — E** — Draining `freeing` to zero can relax this feature's activity without returning the pool to the pre-enable state; `active -> enabled/inactive != enabled -> disabled`.
- **3694 — E** — `freeing` is reclamation/accounting evidence concerning outstanding work, not a second payload copy and not an exact physical-sector map.
- **3695 — A/E** — Case 153 Ceph SnapTrim is a bounded functional analogy for `logical deletion != asynchronous reclamation completion`; only the ZFS evidence here directly couples outstanding reclamation to pool-feature activity/import compatibility.
- **3696 — X** — ZFS `async_destroy` and Ceph SnapTrim are not thereby the same protocol, implementation, or proven genealogy.
- **3697 — X** — An active read-only-compatible `async_destroy` feature does not imply that every unsupported import is impossible; read-only compatibility is a distinct access-mode boundary.
- **3698 — X** — `freeing == 0` or `async_destroy` becoming inactive does not prove byte-identical rollback, secure deletion, sanitization, exact physical erasure, or forensic non-recoverability.
- **3699 — X** — The 2012 feature-flags integration and later released documentation/source establish implementation/documentation chronology, not invention priority for asynchronous deletion or feature-controlled format compatibility.
'''
INDEX_PATH.write_text(index + findings + "\n", encoding="utf-8")

# Validate the canonical edits before removing the one-shot integration machinery.
idx_text = INDEX_PATH.read_text(encoding="utf-8")
for n in range(3684, 3700):
    token = f"**{n} —"
    assert idx_text.count(token) == 1, (n, idx_text.count(token))
assert ROADMAP_PATH.read_text(encoding="utf-8").count(roadmap_marker) == 1
assert CASE_PATH.read_text(encoding="utf-8").count(marker) == 1
assert EVIDENCE_PATH.exists()

# Leave only canonical research files in the final tree.
if WORKFLOW_PATH.exists():
    WORKFLOW_PATH.unlink()
if SELF_PATH.exists():
    SELF_PATH.unlink()
