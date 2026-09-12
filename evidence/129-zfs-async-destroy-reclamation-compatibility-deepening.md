# Evidence 129B — OpenZFS `async_destroy`: reclamation lifetime and feature-state compatibility

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
