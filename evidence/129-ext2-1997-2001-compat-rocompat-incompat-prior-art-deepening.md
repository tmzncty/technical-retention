# Evidence 129C — ext2 compatibility masks before ZFS feature flags: access-mode and tool-role admissibility

**Status:** `bounded deepening complete`

## Research question

Case 129 already records a participant-side anti-novelty warning: a 2013 ZFS-on-Linux / FreeBSD-side integration commit describes ZFS feature flags as conceptually similar to Linux `ext[234]`-style feature flags. That statement is useful, but by itself it leaves the earlier Linux mechanism underspecified.

This slice asks a narrower historical and engineering question:

> Before the 2012 ZFS feature-flags integration, did ext2 already retain explicit compatibility classes that made future access depend on both software capability and requested operation, and did different interpreter roles apply different admissibility rules to the same feature state?

The answer is yes, conservatively grounded no later than the Linux 2.4 documentation update of April 2001, with source-level field evidence reaching back at least to the v2.1.92 code line referenced by an April-1998 patch.

This packet does **not** claim that ext2 invented filesystem compatibility flags, that ZFS copied ext2, or that ext2 and ZFS use the same on-disk encoding or lifecycle.

---

## Sources inspected

### Primary / period Linux source-tree evidence

1. Linux kernel patch archive, `patch-2.4.4`, `Documentation/filesystems/ext2.txt`, dated **20 April 2001**. The patch records the previous file as Linux `v2.4.3` with an original date of **1 October 2000** and expands the filesystem's `Feature Compatibility` documentation.
   - <https://ftp.funet.fi/pub/Linux/kernel/v2.4/patch-html/patch-2.4.4/linux_Documentation_filesystems_ext2.txt.html>

2. Linux kernel patch archive, `patch-2.1.93`, `fs/ext2/super.c`, dated **4 April 1998**. The diff modifies assignments for `s_feature_compat`, `s_feature_incompat`, and `s_feature_ro_compat` that already existed in the `v2.1.92` preimage, changing them to explicit little-endian conversion. The archive labels the original file date **16 July 1997**.
   - <https://ftp.csc.fi/pub/Linux/kernel/v2.1/patch-html/patch-2.1.93/linux_fs_ext2_super.c.html>

### ZFS participant-side continuity witness already used by Case 129

3. FreeBSD commit `c1cdd9900b7b676fd1d1952125a5acd3435db5d7`, **8 January 2013**, whose integration message says ZFS feature flags are “conceptually very similar to Linux's ext[234] style of feature flags.”
   - <https://github.com/freebsd/freebsd-src/commit/c1cdd9900b7b676fd1d1952125a5acd3435db5d7>

The FreeBSD statement is used as a contemporary participant-side comparison, not as proof of design descent.

---

## Historical record

### H/P — ext2 revision 1 retained three distinct compatibility fields

The April-2001 documentation patch is unusually useful because it exposes both the previous text and the expanded replacement.

The removed `v2.4.3` text already says that ext2 revision 1 has three 32-bit fields:

- compatible features;
- read-only-compatible features;
- incompatible features.

The replacement text names the classes `COMPAT`, `RO_COMPAT`, and `INCOMPAT` and says the compatibility mechanism was introduced in ext2 revision 1 rather than original revision 0.

Therefore the conservative historical statement is:

> **By the Linux 2.4.3/2.4.4 documentation boundary, ext2 publicly documented three separate on-disk feature-compatibility classes rather than one monolithic format-version bit.**

This evidence does not date the first implementation of revision 1.

### H/P — source-level field names are visible earlier

The Linux 2.1.93 patch of 4 April 1998 changes three assignments in `fs/ext2/super.c` from direct assignment to `le32_to_cpu(...)` conversion:

```text
s_feature_compat
s_feature_incompat
s_feature_ro_compat
```

Because those assignments are present in the patch's `v2.1.92` preimage, the field relation is visibly present in that older source line. The archive labels that preimage 16 July 1997.

This supports only a bounded implementation floor:

> **The three ext2 compatibility-state fields were already represented in the inspected v2.1.92 source line no later than the source state modified by the April-1998 patch.**

It does **not** establish:

- the original commit that introduced the fields;
- that every ext2 implementation in 1997 enforced the later-documented semantics identically;
- that the July-1997 archive date is an invention date;
- any ext2 → ZFS genealogy.

### H/P — `COMPAT` means unknown support need not block read/write

The April-2001 ext2 documentation says a `COMPAT` flag represents a feature whose on-disk format remains compatible enough that an older kernel unaware of the feature can read and write the filesystem without corrupting or making it inconsistent.

The important historical fact is not merely that a bit exists. The class encodes an intended consequence for an interpreter that does **not** know that bit.

Thus:

```text
unknown COMPAT feature
    -> kernel may still read/write
```

within the documented ext2 contract.

### H/P — `RO_COMPAT` separates read admissibility from write admissibility

The same document says an `RO_COMPAT` feature remains compatible for reading, while an older kernel writing such a filesystem could corrupt it, so writing is prevented.

This gives a direct pre-ZFS example of access-mode-dependent format admissibility:

```text
unknown RO_COMPAT feature
    -> read may remain admissible
    -> write must be refused
```

The `SPARSE_SUPER` example explains why this is not merely a naming convention: an old writer could incorrectly treat locations repurposed by the newer layout as ordinary freeable blocks and create inconsistent metadata.

### H/P — `INCOMPAT` can make even mounting/reading unsafe

The 2001 documentation says an `INCOMPAT` flag marks an on-disk-format change that is unreadable to older kernels or otherwise unsafe for an old kernel to mount.

Its examples include:

- `FILETYPE`, where an old kernel would misinterpret the changed directory-entry representation;
- `COMPRESSION`, where lack of decompression support would return wrong data;
- ext3 `RECOVER`, used to prevent mounting without understanding required journal replay.

This documents a stronger barrier than `RO_COMPAT`:

```text
unknown INCOMPAT feature
    -> access can be rejected entirely
```

Again, this is the ext2 documentation's historical contract, not a claim that every bit or implementation followed one identical failure path forever.

### H/P — the checker can require more semantic knowledge than the mount path

The most useful boundary for `technical-retention` appears immediately after the three class definitions. The April-2001 document says `e2fsck` is deliberately stricter than the kernel: if it does not understand **any** `COMPAT`, `RO_COMPAT`, or `INCOMPAT` flag, it refuses to check the filesystem because it cannot verify whether that feature is valid.

That creates a distinct interpreter-role boundary:

```text
feature state acceptable to kernel for ordinary access
    !=
feature state acceptable to filesystem checker for validation/repair
```

In particular, an unknown `COMPAT` feature can be safe for an old kernel to read/write while still being insufficiently understood by an old checker to certify or repair.

The document explicitly frames refusal as preferable to giving the user a false sense of security.

---

## Engineering reconstruction

The historical records support a general relation without requiring ZFS terminology to be projected backward:

```text
surviving filesystem bytes
    + retained feature-class bits
    + interpreter-supported feature semantics
    + requested operation / interpreter role
    -> admissibility decision
```

The requested operation matters in at least two ways:

1. **read versus write** — `RO_COMPAT` permits a weaker read-only path while disallowing an ignorant writer;
2. **ordinary access versus checking/repair** — `e2fsck` may reject a feature set that the kernel can otherwise access because validation requires knowledge of additional invariants.

This yields several guarded distinctions:

> **format bytes readable != safe to modify.**

> **safe to mount != safe to validate/repair with the same software generation.**

> **unknown feature bit != one universal failure mode.**

> **interpreter capability != one scalar “supports filesystem” property.**

The software dependency is operation-specific.

### Capability is a relation, not a property of the medium alone

A disk image can remain byte-for-byte unchanged while its effective access surface differs across software:

```text
old reader + unknown RO_COMPAT
    -> potentially readable read-only

old writer + same bytes
    -> inadmissible

old fsck + same bytes
    -> may refuse verification

new implementation + same bytes
    -> broader admissibility
```

The medium has not physically degraded in this thought experiment. What changes is whether the interpreter has enough semantics for the requested act.

### Repair authority can require stronger semantic closure than reading

The checker rule is important because recovery environments are often treated as if “can read the filesystem” implies “can safely repair it.” ext2 supplies a period counterexample.

The checker must reason about invariants that ordinary access can sometimes leave opaque. Therefore preservation of a recovery path may require retaining not only a reader but also a checker/version with knowledge of all active feature semantics.

Engineering reconstruction:

```text
payload access path retained
    !=
maintenance / repair authority retained
```

This is not a claim that every repair tool is stricter than every mount implementation. It is the bounded relation documented for ext2/e2fsck in this source.

---

## Functional comparison with ZFS Case 129

The comparison is deliberately structural, not genealogical.

### Similarity that is actually supported

The 2013 FreeBSD integration message itself says ZFS feature flags are conceptually similar to Linux `ext[234]`-style feature flags. The ext2 primary record now makes the older side of that comparison concrete.

Both families preserve a distinction between:

```text
feature state that does not block ordinary access
feature state that blocks writing but can allow reading
feature state that can block reading/opening altogether
```

Case 129's ZFS mechanism expresses this through feature objects / required-for-read and required-for-write relations plus implementation support. ext2 expresses it through superblock compatibility classes.

Therefore:

> **similar compatibility topology != same encoding or same lifecycle.**

### Important differences that must remain visible

Do **not** collapse the mechanisms:

- ext2's `COMPAT` / `RO_COMPAT` / `INCOMPAT` are categorical superblock feature masks;
- ZFS feature flags use feature identifiers and separate metadata such as `features_for_read` and `features_for_write`;
- ZFS additionally distinguishes `disabled`, `enabled`, and `active` feature lifecycle state;
- ext2's inspected 2001 documentation does not establish a ZFS-like per-feature reference-count lifecycle;
- ZFS's `async_destroy` activity relation is feature-specific and should not be projected onto ext2 masks;
- ext2's checker rule does not imply that ZFS `zpool import`, `zdb`, `fsck`, or boot environments have identical policy.

### The new anti-novelty boundary

Case 129 can now reject a broad novelty formulation with primary historical evidence rather than only a 2013 retrospective analogy:

```text
2012 ZFS feature flags
    != first public filesystem mechanism in which
       retained feature metadata distinguishes
       read/write compatibility with older software
```

The inspected ext2 record documents that compatibility topology by April 2001, while a 1998 patch shows the three field names already present in an older source line.

This is **prior art for the broad functional pattern**, not an invention-priority judgment and not a genealogy claim.

---

## Cross-case comparison

### Case 128 — ZFS labels / uberblock import

Case 128 asks whether the pool graph and restart root can be reconstructed and admitted. Case 129 plus this ext2 deepening asks a different question: whether a given software interpreter has the semantics needed to use the retained format under a requested operation.

```text
restart root recovered
    !=
format semantically admissible to this interpreter
```

### Case 130 — LTO generational reader obsolescence

Case 130 shows end-to-end readability can depend on preserving a drive generation, host attachment, driver/OS, and application path. The ext2/ZFS feature relation is a software-format analogue:

```text
media survives
    !=
requested operation remains supported by the available interpreter chain
```

This is a functional comparison only; filesystem feature masks and tape-drive compatibility are unrelated mechanisms.

### Case 125 / filesystem crash maintenance

The e2fsck boundary is especially useful beside crash-recovery cases: a tool that can merely parse some filesystem structures is not automatically authorized to certify or mutate every newer feature's invariants.

This comparison does not claim that ext3/ext4 orphan cleanup uses the same feature-state machine.

---

## Philosophical interpretation

`I` — Retention is not exhausted by preserving bits or even by preserving one program capable of reading them. A retained technical object may expose different admissible operations depending on which semantics the surviving interpreter understands.

`I` — “Compatibility” is therefore better treated as a relation among retained format state, interpreter capability, and requested authority than as a timeless property attached to the medium.

`I` — Maintenance tools expose a stronger version of this relation: preserving observational access does not necessarily preserve authority to validate, repair, or safely rewrite.

These are project interpretations. They are not attributed to ext2, e2fsprogs, FreeBSD, illumos, or OpenZFS authors.

---

## Explicit non-claims

This evidence does **not** establish that:

1. ext2 invented filesystem feature bits;
2. 1997 was the invention date of the three ext2 fields;
3. the 1998 patch introduced those fields;
4. every ext2 revision used exactly the April-2001 semantics;
5. every unknown `COMPAT` feature is semantically irrelevant to every tool;
6. every unknown `RO_COMPAT` feature is readable by every old implementation;
7. every unknown `INCOMPAT` feature is physically unreadable;
8. incompatibility implies corruption;
9. read-only compatibility implies repair compatibility;
10. kernel mount policy and e2fsck policy are interchangeable;
11. ZFS copied ext2;
12. Linux ext2 developers influenced the 2012 ZFS design directly;
13. ZFS `features_for_read` is the same field as ext2 `s_feature_ro_compat`;
14. ZFS `features_for_write` is the same field as ext2 `s_feature_incompat`;
15. ZFS `enabled` / `active` states have an ext2-equivalent lifecycle in the inspected sources;
16. the FreeBSD 2013 analogy proves genealogy;
17. a filesystem that cannot be checked is necessarily unreadable;
18. a filesystem that can be read is necessarily safe to write;
19. software support alone guarantees media integrity;
20. preserving source code alone guarantees future executable recovery tooling.

---

## Claim ledger

### G-129.10 — ext2 had three compatibility classes before ZFS feature flags

- **Type:** H/P
- **Strength:** strong
- **Claim:** Linux ext2 documentation by April 2001 explicitly describes `COMPAT`, `RO_COMPAT`, and `INCOMPAT` feature classes in revision 1, with an older v2.4.3 text already recording the three 32-bit fields.
- **Source:** Linux `patch-2.4.4` ext2 documentation patch.

### G-129.11 — field representation is visible in an older 2.1-era source line

- **Type:** H/P
- **Strength:** moderate-to-strong
- **Claim:** the April-1998 2.1.93 patch modifies pre-existing assignments for `s_feature_compat`, `s_feature_incompat`, and `s_feature_ro_compat` in the v2.1.92 preimage.
- **Source:** Linux `patch-2.1.93`, `fs/ext2/super.c`.
- **Guardrail:** not an introduction-date claim.

### G-129.12 — read and write admissibility were already separable

- **Type:** H/P
- **Strength:** strong
- **Claim:** ext2's documented `RO_COMPAT` semantics allow older software to read while preventing writes that could corrupt newer layout semantics.
- **Source:** Linux `patch-2.4.4` ext2 documentation.

### G-129.13 — checker admissibility can be stricter than mount admissibility

- **Type:** H/P + E
- **Strength:** strong
- **Claim:** the 2001 ext2 document says e2fsck refuses unknown features in all three classes even where kernel access can be allowed, establishing an operation/tool-role-specific capability boundary.
- **Source:** Linux `patch-2.4.4` ext2 documentation.

### G-129.14 — broad read/write compatibility-feature novelty is blocked for ZFS

- **Type:** E / prior-art boundary
- **Strength:** strong for broad functional pattern; none for genealogy
- **Claim:** ZFS 2012 cannot safely be described as the first public filesystem mechanism to retain feature metadata that distinguishes old-software read/write admissibility; ext2 publicly documented such a topology by 2001 and a 2013 ZFS integration participant explicitly compared the designs conceptually.
- **Sources:** Linux ext2 documentation; FreeBSD `c1cdd990...`.

### G-129.15 — functional similarity does not establish lineage

- **Type:** A
- **Strength:** strong methodological boundary
- **Claim:** ext2 and ZFS may be compared at the level of operation-conditioned format admissibility without claiming the same encoding, state lifecycle, implementation, or genealogy.

---

## Related-repository routing

A fresh search of `tmzncty/computing-archaeology` for `ext2 feature flags` and `ZFS feature flags` returned no dedicated packet in the current search surface.

This repository therefore keeps only the retention-specific seam:

```text
retained format feature state
    + interpreter capability
    + requested operation / tool role
    -> access / mutation / repair admissibility
```

A broader history of filesystem format revisioning, ext/ext2/ext3/ext4 compatibility masks, e2fsprogs evolution, cross-platform ext2 readers, and influence/genealogy belongs in `computing-archaeology` if developed.

---

## Remaining evidence debt

This bounded slice intentionally leaves several questions open:

- locate the exact historical change that first introduced ext2 revision-1 feature fields;
- inspect period e2fsprogs source/tags to date the checker policy independently of the kernel documentation;
- reconstruct when each early ext2 feature bit entered production kernels and tools;
- inspect the original ZFS feature-flags proposal/discussion for any explicit design influences beyond the later participant-side ext[234] analogy;
- compare other earlier filesystem compatibility/version mechanisms without turning Case 129 into a general filesystem-history survey.

None of these debts weakens the bounded conclusion that the read/write/tool-role compatibility topology is publicly documented well before the 2012 ZFS feature-flags integration.
