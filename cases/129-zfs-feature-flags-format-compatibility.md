# ZFS Feature Flags: Retained Format Requirements and Software Admissibility

**Status:** `grounded`

## Scope

This case asks one bounded retention question:

> If ZFS pool bytes, labels, and restart roots survive, how can retained on-disk feature state still make the pool unreadable or read-write-inadmissible to software that does not implement the required format semantics?

The historical core is the **21 May 2012 illumos** integration `ad135b5d644628e791c3188a6ecbd9c257961ef8`, whose commit message includes `2747 SPA versioning with zfs feature flags`, plus FreeBSD's **11 June 2012** adoption. Current OpenZFS documentation is later continuity only; a 2016 FreeBSD loader change is a later interpreter-boundary witness.

This is not a generic ZFS history, a second Case 128, a complete release matrix, a send-stream study, or a claim that ZFS invented filesystem feature flags.

A fresh `tmzncty/computing-archaeology` search found no dedicated ZFS feature-flag case in the current search surface. Broad compatibility-bit genealogy, software preservation, migration, and format history belong there if developed.

## Vocabulary and claim boundary

Historical/source vocabulary:

- `feature flags`, `SPA versioning`, pool version `5000`;
- `feature@...`;
- `disabled`, `enabled`, `active`;
- `features_for_read`, `features_for_write`, `feature_descriptions`;
- `read-only compatible`.

Project engineering vocabulary (`E`):

- **format admissibility** — whether one surviving on-disk state may be opened by a particular implementation under a requested access mode;
- **interpreter capability** — the software-side semantics needed to understand that format;
- **compatibility obligation** — retained control state that makes future software support a condition of continued access.

These project terms are not attributed to historical actors.

## Historical record

### H/P — the 2012 feature-mode boundary

The illumos change replaces the old endpoint at version 28 with:

```text
SPA_VERSION_BEFORE_FEATURES = 28
SPA_VERSION = 5000
SPA_VERSION_FEATURES = 5000
```

This establishes the feature-flags transition in this code line. It does **not** make `5000` one monolithic post-28 format version.

### H/P — read and write requirements are retained separately

The same integration adds MOS names:

```text
features_for_read
features_for_write
feature_descriptions
```

and pool fields documented as feature objects required to read or write the pool. This is control metadata, not user payload.

### H/P — `disabled`, `enabled`, and `active` are different states

The 2012 userland code exposes `feature@...` as:

```text
disabled | enabled | active
```

and its property path distinguishes absence, zero reference count, and nonzero reference count. Current OpenZFS `zpool-features(7)` keeps the conceptual boundary explicit: `enabled` means the capability is allowed but its format change has not yet been made; `active` means the on-disk change is in effect. Later features can have feature-specific transitions, so this case does not universalize one activation lifetime.

### H/P — unsupported-for-write can be weaker than unreadable

The 2012 source adds separate statuses for unsupported features required for **read** and for **write**. Its load path can determine that a pool is unavailable read-write while still available read-only when the missing feature does not prevent reading.

Thus:

> **unsupported for write ≠ unreadable.**

The GRUB-side code sharpens the same point: it checks `features_for_read` and comments that it need not check `features_for_write` because GRUB opens pools read-only.

### H/P — enabled capability is not yet feature use

The same change adds `zpool create -d` to avoid automatically enabling supported features, while individual `feature@...=enabled` properties may be set. Current OpenZFS documentation confirms that software lacking an enabled-but-not-active feature can still import the pool until feature-dependent format changes actually occur.

Thus:

> **feature enabled ≠ feature active.**

### H/P — contemporary portability witness

FreeBSD commit `2d9cf57e18654edda53bcb460ca66641ba69ed75` (11 June 2012) explicitly says it introduces ZFS pool feature flags, bumps SPA version to 5000, adds `com.delphix:async_destroy`, implements boot support, and merges the illumos 2619/2747 work.

This is a portability/continuity witness, not a second invention.

### H/P — later boot-path witness

FreeBSD commit `4deb8929ea01a581258a31cc027c0d4177daaff8` (1 August 2016) makes boot code compare MOS features against loader support. Its commit message says unsupported **active** features disqualify a pool from booting, while merely enabled-but-unused features do not.

So:

> **pool survival/importability ≠ boot-path admissibility.**

A boot loader is another interpreter with its own supported-feature set.

## Retained relation

The bounded mechanism is:

```text
surviving pool bytes / restart root
        +
retained active feature requirements
        +
software-supported feature semantics
        +
requested access mode
        ->
format-admissible open/import
```

For read-write service, the required interpreter capability can be stronger than for read-only service.

This relation is an engineering reconstruction, not a source quotation.

## Retention, access, and failure

Case 128 already shows that restart depends on surviving labels/topology and an admissible uberblock root. Case 129 adds a separate gate: software must understand the format requirements attached to the surviving pool.

A physically readable pool can therefore fail in several distinct ways:

- a software release lacks a feature required for writing;
- it lacks a feature required even for reading;
- a boot environment supports fewer features than the full OS;
- compatible software is no longer runnable or obtainable;
- feature metadata is itself corrupt;
- operators activate a feature and thereby narrow compatibility with older recovery environments.

These are not generic `bit loss`.

The relevant timescales are also different: media lifetime, root-generation lifetime, enabled-but-unused feature lifetime, active feature lifetime, software-support lifetime, and institutional ability to run an interpreter.

## Engineering findings

The primary sources support these guarded distinctions:

> **payload survival ≠ software interpretability.**

> **restart-root survival ≠ format admissibility.**

> **feature supported by software ≠ feature used by this pool.**

> **required-for-read ≠ required-for-write.**

> **read-only importability ≠ read-write compatibility.**

> **software obsolescence ≠ physical erasure.**

> **format compatibility ≠ media integrity.**

Installing compatible software may restore access to unchanged surviving bytes. Conversely, activating a feature may remove an older interpreter's access without destroying payload.

## Prior art boundary

No invention claim is made. A 2013 porting commit (`c1cdd9900b7b676fd1d1952125a5acd3435db5d7`) itself describes ZFS feature flags as conceptually similar to Linux `ext[234]`-style feature flags. That is a useful participant-side anti-novelty warning, but it is not enough to establish a direct ext→ZFS genealogy.

A proper history of filesystem compatibility masks and format migration belongs in `computing-archaeology`.

## Cross-case boundaries

- **Case 128:** restart-root/topology admissibility makes the pool graph legible; Case 129 asks whether the interpreter understands the retained format. `restart-root admissibility ≠ format admissibility`.
- **Case 90 / Kafka:** both reject `metadata presence = admissibility`, but leader-epoch lineage and filesystem format support are unrelated mechanisms.
- **Case 123 / ATA DCO:** both retain small control state that changes a future access surface; DCO is drive capability configuration, not filesystem format interpretation.

These are functional comparisons (`A`), not genealogy.

## Philosophical interpretation

`I` — Case 129 makes technical legibility depend on more than material inscription. State can survive physically yet become operationally unavailable when the compatible interpreter chain disappears.

`I` — Obsolescence can therefore be relational rather than destructive: changing the interpreter can restore access to unchanged media.

These are project interpretations, not claims about illumos/OpenZFS authors' intent.

## Limits

This case does not establish that:

- an unsupported pool is corrupt;
- read-only fallback is always available;
- `enabled` means format state is already in use;
- `active` is universally irreversible;
- pool import compatibility equals boot compatibility;
- preserving one binary guarantees future executability;
- current OpenZFS semantics may be projected backward onto every 2012 feature;
- ZFS invented compatibility metadata.

## Sources

- illumos/illumos-gate, `ad135b5d644628e791c3188a6ecbd9c257961ef8`, 21 May 2012: <https://github.com/illumos/illumos-gate/commit/ad135b5d644628e791c3188a6ecbd9c257961ef8>
- FreeBSD, `2d9cf57e18654edda53bcb460ca66641ba69ed75`, 11 June 2012: <https://github.com/freebsd/freebsd-src/commit/2d9cf57e18654edda53bcb460ca66641ba69ed75>
- OpenZFS, `zpool-features(7)`: <https://openzfs.github.io/openzfs-docs/man/master/7/zpool-features.7.html>
- OpenZFS, **Feature Flags**: <https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Pool%20Structure/Feature%20Flags.html>
- FreeBSD, `4deb8929ea01a581258a31cc027c0d4177daaff8`, 1 August 2016: <https://github.com/freebsd/freebsd-src/commit/4deb8929ea01a581258a31cc027c0d4177daaff8>
- FreeBSD, `c1cdd9900b7b676fd1d1952125a5acd3435db5d7`, 8 January 2013: <https://github.com/freebsd/freebsd-src/commit/c1cdd9900b7b676fd1d1952125a5acd3435db5d7>
