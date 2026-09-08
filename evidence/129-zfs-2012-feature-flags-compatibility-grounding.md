# Evidence 129 — ZFS feature-flags / format-compatibility grounding, 2012–2016

**Case:** [`cases/129-zfs-feature-flags-format-compatibility.md`](../cases/129-zfs-feature-flags-format-compatibility.md)

## Question and evidence discipline

What primary evidence supports the bounded claim that physically surviving ZFS pool state can remain unavailable to a particular software implementation because retained feature metadata imposes read/write format requirements?

Labels follow repository convention: `H/P` historical-primary; `H/S` institutional documentation; `E` engineering reconstruction; `A` functional analogy; `I` interpretation; `X` rejected overclaim.

The historical core is May–June 2012 implementation evidence. Current OpenZFS documentation is later continuity; 2016 boot evidence is not back-projected.

## P1 — illumos feature-flags integration, 21 May 2012

Commit: <https://github.com/illumos/illumos-gate/commit/ad135b5d644628e791c3188a6ecbd9c257961ef8>

Commit message includes:

```text
2747 SPA versioning with zfs feature flags
```

GitHub records `2012-05-21 12:11:39 -0700`.

### P1.1 — version-mode boundary

The change defines `SPA_VERSION_BEFORE_FEATURES = 28` and `SPA_VERSION_FEATURES = SPA_VERSION = 5000`.

**Supports:** explicit transition to feature-mode versioning in this code line. (`H/P`)

**Rejects:** `5000 = one monolithic active feature level`. (`X`)

### P1.2 — retained feature objects

The change adds:

```text
features_for_read
features_for_write
feature_descriptions
```

and pool fields commented as objects required to read or write the pool.

**Supports:** format-compatibility state is retained separately from payload, and read/write requirements are distinct. (`H/P`, `E`)

### P1.3 — state vocabulary

Userland adds `disabled`, `enabled`, and `active` feature-property states. The property path distinguishes absence, zero refcount, and nonzero refcount.

**Supports:** administrative capability state and actual format use are separable. (`H/P`)

### P1.4 — read/write incompatibility classes

The change adds `ZPOOL_STATUS_UNSUP_FEAT_READ` and `ZPOOL_STATUS_UNSUP_FEAT_WRITE`. Load logic distinguishes a feature that blocks opening the pool from one that blocks write access but can still permit a read-only path.

**Supports:** `unsupported-for-write ≠ unreadable`. (`H/P`)

### P1.5 — role-specific read checking

GRUB-side source locates `features_for_read` and comments that it does not check `features_for_write` because GRUB opens pools read-only.

**Supports:** requested access mode/interpreter role changes the required feature subset. (`H/P`)

### P1.6 — enablement before use

`zpool create -d` is added so supported pool features need not be enabled automatically; individual `feature@...=enabled` properties can be selected.

**Supports:** capability enablement is distinct from later use. (`H/P`)

## P2 — FreeBSD adoption, 11 June 2012

Commit: <https://github.com/freebsd/freebsd-src/commit/2d9cf57e18654edda53bcb460ca66641ba69ed75>

The commit message explicitly says it introduces ZFS pool feature flags, bumps SPA version to 5000, adds `com.delphix:async_destroy`, implements boot support, and merges illumos issues 2619/2747.

**Supports:** near-contemporary cross-platform adoption of the illumos architecture. (`H/P`)

**Rejects:** independent FreeBSD invention. (`X`)

## P3 — current OpenZFS continuity

Current `zpool-features(7)`:
<https://openzfs.github.io/openzfs-docs/man/master/7/zpool-features.7.html>

It states that:

- `active` means the on-disk format change is in effect and support is needed for read-write import;
- a non-read-only-compatible active feature also requires support for read-only import;
- `enabled` means the feature was allowed but its format changes have not yet been made;
- unsupported enabled/inactive features can remain compatible;
- some features can return from active to enabled.

**Classification:** `H/S` current documentation, not 2012 evidence.

**Use:** continuity and a guardrail against treating activation lifetimes as universal.

## P4 — FreeBSD loader witness, 1 August 2016

Commit: <https://github.com/freebsd/freebsd-src/commit/4deb8929ea01a581258a31cc027c0d4177daaff8>

Its message says boot code and loader compare MOS feature lists with supported features; unsupported **active** features disqualify a boot candidate, while merely enabled-but-unused features do not.

**Supports:** `enabled ≠ active` and `pool survival ≠ boot-path admissibility`. (`H/P` later continuity)

**Boundary:** loader capability is not identical to userspace import capability.

## P5 — anti-novelty warning, 8 January 2013

Commit: <https://github.com/freebsd/freebsd-src/commit/c1cdd9900b7b676fd1d1952125a5acd3435db5d7>

The porting commit describes the design as conceptually similar to Linux `ext[234]`-style feature flags.

**Supports:** do not claim ZFS invented filesystem feature flags. (`H/P` participant-side comparison)

**Does not support:** a direct ext→ZFS genealogy. (`X`)

## Claim matrix

| ID | Claim | Label | Best source |
| --- | --- | --- | --- |
| G-129.1 | illumos integrates feature-flag SPA versioning on 21-May-2012 | `H/P` | P1 |
| G-129.2 | feature mode follows pre-feature version 28 with marker 5000 | `H/P` | P1.1 |
| G-129.3 | read-required and write-required feature state are separate | `H/P` | P1.2/P1.4 |
| G-129.4 | disabled, enabled, active are distinct | `H/P` | P1.3 |
| G-129.5 | unknown read-required feature can prevent open | `H/P` | P1.4/P1.5 |
| G-129.6 | missing write support can preserve a read-only path | `H/P` | P1.4 |
| G-129.7 | FreeBSD adopted the illumos work in June 2012 | `H/P` | P2 |
| G-129.8 | current OpenZFS retains enabled/active/read-only-compatible semantics | `H/S` later | P3 |
| G-129.9 | later loader rejects unsupported active features | `H/P` later | P4 |
| G-129.10 | surviving pool bytes guarantee software interpretability | `X` | mechanism comparison |
| G-129.11 | enabled means feature format is already in use | `X` | P1/P3/P4 |
| G-129.12 | unsupported-for-write means unreadable | `X` | P1/P3 |
| G-129.13 | ZFS invented filesystem feature flags | `X` | P5 + scope |

## Engineering reconstruction

The sources support:

```text
surviving pool state
  + restart-root/topology legibility
  + retained active format requirements
  + compatible interpreter for requested mode
  -> possible service admission
```

Project conclusions (`E`):

- `payload survival ≠ software interpretability`;
- `restart-root survival ≠ format admissibility`;
- `enabled capability ≠ active format use`;
- `required-for-read ≠ required-for-write`;
- `read-only compatibility ≠ read-write compatibility`;
- `software obsolescence ≠ physical erasure`;
- compatible-interpreter restoration can restore service without first rewriting surviving payload.

## Functional comparison boundaries

- **Case 128:** root/topology admissibility and format admissibility compose but are not one gate.
- **Case 90:** both expose `metadata presence ≠ admissibility`; mechanisms/histories differ.
- **Case 123:** control state changes a future access surface, but DCO and ZFS format requirements are unrelated mechanisms.

## Open gaps

Still open:

- exact pre-May-2012 proposal/list genealogy;
- direct ext2/ext3/ext4 primary prior-art archaeology;
- per-feature cross-implementation release matrices;
- feature-ZAP corruption/loss behavior;
- dataset feature and send/receive format compatibility;
- loader matrices beyond the 2016 witness;
- emulation/VM/software-preservation strategies;
- named-release downgrade/import fault matrices;
- broader format/software-obsolescence history.
