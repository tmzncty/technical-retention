# ZFS Feature Flags: Retained Format Requirements and Software Admissibility

**Status:** `grounded`

## Scope

This case asks one bounded retention question:

> If ZFS pool bytes, labels, and restart roots survive, how can retained on-disk feature state still make the pool unreadable or read-write-inadmissible to software that does not implement the required format semantics?

The historical core is the **21 May 2012 illumos** integration `ad135b5d644628e791c3188a6ecbd9c257961ef8`, whose commit message includes `2747 SPA versioning with zfs feature flags`, plus FreeBSD's **11 June 2012** adoption. Current OpenZFS documentation is later continuity only; a 2016 FreeBSD loader change is a later interpreter-boundary witness.

This is not a generic ZFS history, a second Case 128, a complete release matrix, a send-stream study, or a claim that ZFS invented filesystem feature flags.

A fresh `tmzncty/computing-archaeology` search found no dedicated ZFS/ext2 feature-flag case in the current search surface. Broad compatibility-bit genealogy, software preservation, migration, and format history belong there if developed.

## Evidence navigation

- [Evidence 129B — `async_destroy` reclamation lifetime and compatibility state](../evidence/129-zfs-async-destroy-reclamation-compatibility-deepening.md) — grounds one feature-specific case where outstanding reclamation keeps a read-write compatibility obligation active after logical destroy returns.
- [Evidence 129C — ext2 1997–2001 compatibility-mask prior art](../evidence/129-ext2-1997-2001-compat-rocompat-incompat-prior-art-deepening.md) — grounds the earlier `COMPAT` / `RO_COMPAT` / `INCOMPAT` topology and the stricter e2fsck tool-role boundary, blocking a broad novelty claim without asserting ext2→ZFS genealogy.

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

No invention claim is made. A 2013 porting/integration commit (`c1cdd9900b7b676fd1d1952125a5acd3435db5d7`) itself describes ZFS feature flags as conceptually similar to Linux `ext[234]`-style feature flags. Evidence 129C now grounds the older side of that comparison with period Linux material rather than leaving it as a retrospective analogy alone.

Linux's April-2001 ext2 documentation explicitly distinguishes `COMPAT`, `RO_COMPAT`, and `INCOMPAT` feature classes. In the documented contract, unknown `COMPAT` features can remain read/write-safe to an older kernel; unknown `RO_COMPAT` features can preserve reading while preventing unsafe writes; and unknown `INCOMPAT` features can make mounting/reading unsafe. The same document says e2fsck is stricter and refuses to check a filesystem when it encounters any unknown feature in those classes. An April-1998 kernel patch additionally shows `s_feature_compat`, `s_feature_incompat`, and `s_feature_ro_compat` already present in the inspected v2.1.92 source preimage.

This blocks the broad claim that ZFS 2012 was the first public filesystem mechanism to retain feature metadata that conditions read/write admissibility for older software. It also adds another retention boundary:

```text
safe to read
    != safe to write
    != safe to validate / repair with the same software generation
```

The comparison is functional. ext2 uses categorical superblock masks; ZFS uses feature identifiers and separate required-for-read / required-for-write relations plus `disabled` / `enabled` / `active` lifecycle state. Neither the earlier ext2 record nor the 2013 participant-side analogy establishes direct ext→ZFS genealogy.

A proper history of filesystem compatibility masks, format revisioning, and influence belongs in `computing-archaeology`.

## Cross-case boundaries

- **Case 128:** restart-root/topology admissibility makes the pool graph legible; Case 129 asks whether the interpreter understands the retained format. `restart-root admissibility ≠ format admissibility`.
- **Case 90 / Kafka:** both reject `metadata presence = admissibility`, but leader-epoch lineage and filesystem format support are unrelated mechanisms.
- **Case 123 / ATA DCO:** both retain small control state that changes a future access surface; DCO is drive capability configuration, not filesystem format interpretation.
- **Case 130 / LTO:** both show that surviving data can lose requested operations when the compatible interpreter/reader chain is unavailable. Filesystem feature masks and tape-drive generations are only functionally analogous.

These are functional comparisons (`A`), not genealogy.

## Philosophical interpretation

`I` — Case 129 makes technical legibility depend on more than material inscription. State can survive physically yet become operationally unavailable when the compatible interpreter chain disappears.

`I` — Obsolescence can therefore be relational rather than destructive: changing the interpreter can restore access to unchanged media.

`I` — Evidence 129C sharpens the relation further: preservation of observational access does not automatically preserve authority to mutate, validate, or repair the retained format.

These are project interpretations, not claims about ext2/e2fsprogs, illumos/OpenZFS, or FreeBSD authors' intent.


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

## Evidence deepening 129C — ext2 access-mode and tool-role prior art

[`Evidence 129C`](../evidence/129-ext2-1997-2001-compat-rocompat-incompat-prior-art-deepening.md) adds primary historical grounding for the ext-family comparison already present in the case.

The April-2001 Linux ext2 documentation explicitly defines three compatibility classes and ties them to different behavior by an older interpreter. `COMPAT` may remain read/write-safe, `RO_COMPAT` can preserve reads while refusing unsafe writes, and `INCOMPAT` can require refusing the mount. The same document then gives e2fsck a stricter rule: unknown features in **any** class block the filesystem check because the tool cannot verify the newer feature's invariants.

This produces a broader operation-conditioned admissibility model:

```text
surviving filesystem bytes
    + retained feature class
    + interpreter capability
    + requested operation / tool role
    -> admissible read / write / check / repair path
```

The resulting distinctions are useful beyond the prior-art chronology:

```text
readable by old software
    != writable by old software
    != safely checkable / repairable by old tooling
```

The ZFS comparison remains guarded. The ext2 masks are not ZFS feature objects, and the ext2 record does not supply ZFS's enabled/active lifecycle. The evidence is sufficient to block a broad novelty claim about read/write compatibility gating; it is insufficient to establish design descent.

## Limits

This case does not establish that:

- an unsupported pool is corrupt;
- read-only fallback is always available;
- `enabled` means format state is already in use;
- `active` is universally irreversible;
- pool import compatibility equals boot compatibility;
- preserving one binary guarantees future executability;
- current OpenZFS semantics may be projected backward onto every 2012 feature;
- ZFS invented compatibility metadata;
- ext2 and ZFS feature mechanisms share one encoding or lifecycle;
- an old reader that can mount a filesystem can necessarily validate or repair all active feature semantics.

## Sources

- illumos/illumos-gate, `ad135b5d644628e791c3188a6ecbd9c257961ef8`, 21 May 2012: <https://github.com/illumos/illumos-gate/commit/ad135b5d644628e791c3188a6ecbd9c257961ef8>
- FreeBSD, `2d9cf57e18654edda53bcb460ca66641ba69ed75`, 11 June 2012: <https://github.com/freebsd/freebsd-src/commit/2d9cf57e18654edda53bcb460ca66641ba69ed75>
- OpenZFS, `zpool-features(7)`: <https://openzfs.github.io/openzfs-docs/man/master/7/zpool-features.7.html>
- OpenZFS, **Feature Flags**: <https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Pool%20Structure/Feature%20Flags.html>
- FreeBSD, `4deb8929ea01a581258a31cc027c0d4177daaff8`, 1 August 2016: <https://github.com/freebsd/freebsd-src/commit/4deb8929ea01a581258a31cc027c0d4177daaff8>
- FreeBSD, `c1cdd9900b7b676fd1d1952125a5acd3435db5d7`, 8 January 2013: <https://github.com/freebsd/freebsd-src/commit/c1cdd9900b7b676fd1d1952125a5acd3435db5d7>
- Linux kernel patch archive, `patch-2.4.4`, `Documentation/filesystems/ext2.txt`, 20 April 2001: <https://ftp.funet.fi/pub/Linux/kernel/v2.4/patch-html/patch-2.4.4/linux_Documentation_filesystems_ext2.txt.html>
- Linux kernel patch archive, `patch-2.1.93`, `fs/ext2/super.c`, 4 April 1998: <https://ftp.csc.fi/pub/Linux/kernel/v2.1/patch-html/patch-2.1.93/linux_fs_ext2_super.c.html>
