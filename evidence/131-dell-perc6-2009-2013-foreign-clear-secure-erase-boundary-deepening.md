# Evidence 131B — Dell PERC 6 (2009) Foreign-Clear and Configuration-Retirement Boundary

**Status:** `bounded deepening complete`

## Purpose

This evidence note deepens Case 131 at one narrow retention boundary:

> what exactly is retired when a Dell PERC operator chooses **Clear** rather than **Import** for a foreign configuration, and why must that transition not be conflated with media formatting, virtual-disk initialization, RAID rebuild, consistency verification, or secure sanitization?

The source slice is intentionally small. It uses a Dell-authored PERC 6/i, PERC 6/E and CERC 6/i User's Guide whose surviving searchable text identifies the working document as `Dell_PERC6.2_UG.book`, dated **24 June 2009**, plus a later Dell-hosted PERC H310/H710/H710P/H810 User's Guide, Rev. A02, **March 2013**, as a direct vendor continuity witness.

This note does **not** attempt to identify the binary on-disk metadata format, prove a DDF implementation, establish invention priority, or generalize the semantics to arbitrary RAID controllers.

---

## Source classification

### Source A — Dell PERC 6/i, PERC 6/E and CERC 6/i User's Guide

**Type:** `H/P*` — Dell-authored product manual; surviving searchable copy is mirrored rather than currently fetched from Dell's support front end.

**Document marker:** `Dell_PERC6.2_UG.book`

**Document working date visible in page footers:** **24 June 2009**

**Copyright line:** Dell, 2007–2009.

**Searchable surviving copy inspected:**

https://manualzilla.com/doc/7425219/dell-poweredge-expandable-raid-controller-3-user-s-guide

The product identity, page numbering, section titles, and dated footer are internally consistent across the inspected pages. Because the currently convenient searchable copy is a mirror, claims below are labelled `H/P*`, not silently upgraded to a currently Dell-hosted PDF.

### Source B — Dell PowerEdge RAID Controller H310, H710, H710P, and H810 User's Guide

**Type:** `H/P` — Dell-hosted vendor primary.

**Revision:** Rev. A02

**Date:** **March 2013**

**Dell-hosted PDF:**

https://dl.dell.com/manuals/common/poweredge-rc-h710_user%27s%20guide_en-us.pdf

Page 44 independently repeats the import / clear split and the ability to inspect a foreign configuration before importing it.

---

# I. Historical record

## H/P* — the 2009 manual names the retained object `foreign metadata`

In the troubleshooting table, the PERC 6 manual explains the POST warning `Foreign configuration(s) found on adapter` by saying that controller firmware detects a physical disk with existing **foreign metadata**, flags that disk as foreign, and raises an alert.

This is stronger than reconstructing the object only from later management vocabulary. For this product/manual line, Dell itself directly names retained disk-side evidence as `foreign metadata`.

Bounded historical claim:

> By the inspected June-2009 PERC 6 manual, Dell documented controller detection of **existing foreign metadata on a physical disk** as the cause of the disk entering the `foreign` state.

The wording does not reveal the complete metadata layout, serialization format, sequence-number rules, checksum scheme, or standard provenance.

## H/P* — foreign configuration can be previewed without importing it

The `Foreign Configuration View` section says that the utility can display the disk groups, virtual disks, physical disks, space allocation, and hot spares represented by the foreign configuration before the operator chooses what to do.

The manual explicitly separates:

```text
foreign configuration exists
    -> view / preview
    -> import OR clear
```

Therefore:

> **configuration visibility != configuration admission.**

The controller can expose a retained configuration relation to the operator without yet making that relation its active virtual-disk configuration.

## H/P* — `Import` and `Clear` are opposite authority transitions

The 2009 manual repeatedly presents the two actions as alternatives.

For reinserted disks, it says:

- `Import` imports the foreign configuration to the controller;
- `Clear` deletes the foreign configuration from the reinserted disks.

For the case where disks from a virtual disk were removed at different times, it says:

- `Import` merges the foreign configurations with the existing controller configuration;
- `Clear` deletes those foreign configurations from the reinserted disks.

For a non-redundant virtual disk, it again says:

- `Import` imports the foreign configuration;
- `Clear` deletes it from the reinserted disks.

The manual therefore supports a direct authority split:

```text
Import
    -> retain / adopt the old disk-carried configuration relation

Clear
    -> retire that foreign configuration relation from the reinserted disks
```

This is a configuration-state transition. It is not merely a display preference.

## H/P* — clearing changes the disk's controller-visible state to `Ready` and can cause data loss

The PERC 6 troubleshooting table states that after the operator clears a foreign configuration, the physical disk goes to the `Ready` state and warns that this may lead to data loss.

This supplies a concrete postcondition:

```text
foreign metadata admitted as foreign
    -> Clear
    -> disk becomes Ready
```

The important retention consequence is not that all payload sectors have necessarily disappeared. It is that the controller has retired the retained relation by which those sectors participated in the former foreign virtual-disk configuration.

The warning blocks any attempt to describe `Clear` as harmless metadata housekeeping.

## H/P* — `Clear` is not the manual's `Format`

The glossary places `Foreign Configuration` and `Format` next to one another but defines them differently.

For foreign configuration, the guide says an existing RAID configuration can be imported or cleared so a new one can be created.

For `Format`, the guide describes **writing a specific value to all data fields on a physical disk**.

These definitions establish a direct terminology boundary inside the same manual:

> **Clear Foreign Configuration != Format.**

The guide does not describe foreign clear as a pass over all user-data fields.

That distinction matters because a configuration-retirement operation can destroy ordinary controller access to data without proving that every data field was overwritten.

## H/P* — `Clear` is also not virtual-disk `Initialization`

The same glossary separately defines `Initialization` as writing zeros to virtual-disk data fields and generating parity; it explicitly says initialization erases previous data.

So the inspected manual distinguishes at least three destructive or potentially destructive operations:

```text
Clear Foreign Configuration
    -> delete retained foreign configuration relation
    -> disk becomes Ready
    -> may lead to data loss

Format
    -> write a specific value to all physical-disk data fields

Initialization
    -> write zeros to virtual-disk data fields
    -> generate parity
    -> erase previous data
```

This is unusually useful primary-source support for the project's rule:

> **loss of recoverability / authority != physical payload erasure.**

No claim is made here that old payload is forensically recoverable after every clear. The point is only that Dell's own operation definitions are not equivalent.

## H/P* — import can be followed by rebuild, and Dell then calls for consistency checking

The PERC 6 manual describes cases in which an imported configuration causes pulled drives to be automatically rebuilt. It then recommends starting a consistency check after rebuild completion to ensure virtual-disk data integrity.

This yields a direct ordered decomposition:

```text
configuration import
    -> possible rebuild
    -> consistency check
```

Accordingly:

> **Import != Rebuild != Consistency Check.**

A successful import re-establishes configuration authority. It is not, by itself, proof that redundancy has been repaired or that data/parity consistency has been checked.

## H/P* — importability is evaluated against current drive state

The 2009 manual also says that drive state may change between a foreign-configuration scan and the actual import. It limits import to qualifying drive states and excludes failed/offline drives.

Therefore:

> **previewed foreign configuration != guaranteed later importability.**

Retained evidence can remain visible while the admissible operation changes underneath it.

This makes the operation relation explicitly time-sensitive:

```text
retained foreign metadata
    + current member state
    + current controller rules
    -> import admissibility
```

The retained metadata alone is not sufficient.

## H/P* — clearing foreign configuration and discarding preserved dirty cache are separate forgetting operations

Immediately after the foreign-configuration section, the PERC 6 manual describes `pinned cache`: dirty cache retained when a virtual disk goes offline or is deleted because physical disks are missing.

The manual says the pinned cache remains until the virtual disk is imported or the cache is discarded, and warns the operator to import the foreign configuration before discarding preserved cache because otherwise data belonging to that foreign configuration may be lost.

This directly exposes two different retained objects and two different retirement actions:

```text
disk side
    foreign configuration / foreign metadata
        -> Import or Clear

controller side
    preserved dirty / pinned cache
        -> later flush after recovery or Discard
```

The same recovery episode may contain both.

> **Clear foreign configuration != discard preserved cache.**

and:

> **configuration retirement != pending-payload retirement.**

The manual additionally warns that clearing the controller configuration while preserved cache exists can discard the cache and lose virtual-disk data. That stronger controller-wide operation must not be silently equated with the narrower foreign-config `Clear`.

## H/P — 2013 Dell-hosted guide independently preserves the preview / import / clear split

The Dell-hosted March-2013 PERC H310/H710/H710P/H810 guide states that a foreign configuration appears in the management screen; the operator can inspect it in `Foreign View` without importing it; and the available actions are `Import` and `Clear`.

It tells the operator to verify that expected physical disks are present before import and says that `Clear` deletes the foreign configuration. In the same flow, Dell again distinguishes later rebuild and consistency checking: an imported member may enter `Rebuild`, and Dell recommends a consistency check after rebuild completion.

This later primary source is used as a continuity witness:

> the `visible foreign configuration -> preview -> import/clear -> possible rebuild -> consistency check` control topology remained explicit in a later PERC product family.

It is not used to project H710/H810 internals backward into PERC 6.

## H/P — the 2013 secured-foreign path supplies an explicit secure-erase exception

The same Dell-hosted guide has a separate section for **secured foreign configurations**. There, Dell says:

- `Import` and `Clear` remain the high-level choices;
- but to **Clear** a foreign configuration secured with a different security key, the operator must use **Instant Secure Erase**;
- Dell defines Instant Secure Erase as permanently erasing all data on an encryption-capable physical disk and resetting the security attributes;
- a secured foreign disk whose passphrase is unavailable remains inaccessible until the correct passphrase is supplied or the disk is instant-secure-erased.

This prevents a different overgeneralization.

The evidence does **not** support:

> `Clear never erases payload.`

Instead, the bounded relation is:

```text
ordinary foreign-config Clear semantics
    -> delete the foreign configuration relation

but

secured foreign configuration + different/unavailable key
    -> Clear path requires Instant Secure Erase
    -> permanent data erasure + security-attribute reset
```

Therefore:

> **the label `Clear` alone does not determine the physical-erasure semantics; security context and the concrete execution path matter.**

This is stronger and more precise than either `Clear = sanitization` or `Clear never touches payload`.

---

# II. Engineering reconstruction

The following relations are **project-level reconstructions**, not Dell quotations.

## 1. Configuration evidence and payload are different retained classes

The PERC 6 manual's own operation vocabulary requires at least:

```text
payload/parity embodiments
    !=
foreign metadata / array-topology relation
```

Clearing the second can make the first inaccessible through the controller's old virtual-disk relation without proving that all of the first has been physically rewritten.

## 2. Detection, visibility, admission, repair, and verification are separate phases

The 2009 sequence supports:

```text
foreign metadata survives
    -> controller detects foreign state
    -> operator can preview
    -> import admissibility evaluated
    -> configuration imported
    -> rebuild may occur
    -> consistency check can follow
```

Each arrow represents a different obligation.

Collapsing them into a single statement such as `array recovered` loses information about which authority and which evidence have actually been established.

## 3. Clear is an authority-retirement transition

For this evidence slice, a useful formalization is:

```text
foreign relation R(disk set, virtual disk)
    -> Clear
    -> controller no longer retains/adopts R as foreign configuration
    -> disks can enter Ready/new-allocation path
```

That is stronger than `ignore the warning`, but weaker than `overwrite every payload field`.

## 4. Logical forgetting can precede physical forgetting — but not in every clear path

For the ordinary PERC 6 foreign-clear path, the source-supported distinction between `Clear` and `Format` yields:

```text
configuration relation forgotten / deleted
    !=
evidence that all data fields were overwritten
```

This is a central retention boundary.

It demonstrates a system in which the ability to *reconstruct the interpretation* of surviving payload can be deliberately retired before the physical payload medium is **proven** erased.

The March-2013 secured-foreign path adds a crucial exception:

```text
secured foreign relation
    + incompatible / unavailable security key
    + requested Clear
        -> Instant Secure Erase required
        -> permanent data erase
```

So the correct project rule is contextual:

> **configuration retirement does not, by itself, prove physical erasure; some security-gated clear paths explicitly require physical/cryptographic secure-erasure machinery.**

## 5. Reuse admission follows state retirement, while the erasure path depends on context

The 2009 manual's Ready-state warning supports this bounded reconstruction:

```text
foreign state
    -> Clear
    -> Ready
    -> eligible for a different allocation/configuration path
```

The later secure path shows that a protected drive may have an extra gate before that transition can be completed.

Do **not** strengthen either source into a universal statement about every PERC generation or every drive type.

## 6. Two retained-state carriers require two recovery decisions

When foreign disk metadata and pinned cache coexist, recovery is not one Boolean.

A more accurate representation is:

```text
disk-resident configuration retained?
controller-side pending writes retained?
member set sufficient?
configuration imported?
pending writes flushed?
rebuild complete?
consistency verified?
```

One `yes` does not entail the others.

---

# III. Functional comparison

## Case 102 — PERC Patrol Read / Consistency Check

Case 102 operates after an array is admitted and focuses on verification/maintenance.

This evidence deepening shows directly from the PERC 6 manual that foreign configuration import may precede rebuild and a subsequent consistency check.

Functional relation only:

```text
admission
    != repair
    != integrity verification
```

No new genealogy claim is made.

## Case 128 — ZFS retained member metadata

Case 128 and Case 131 both show that member-media metadata can preserve the ability to reconstruct a higher-level storage relation after control state changes.

But `PERC Clear Foreign Configuration` must not be rewritten as `zpool labelclear`, nor vice versa. Encodings, selection rules, repair semantics, and software/controller architecture differ.

The comparison is limited to:

```text
retained interpretive metadata
    -> can preserve future re-admission capability

retirement of interpretive metadata
    -> can remove that capability before physical media is sanitized
```

## Case 44 — cryptographic erasure / key authority

The 2013 PERC secured-foreign path makes this comparison more concrete but still bounded.

A secured foreign virtual disk can remain inaccessible because the current controller lacks the necessary key/passphrase authority. Dell then distinguishes two very different routes:

```text
recover key/passphrase authority
    -> import remains possible

or

Instant Secure Erase
    -> permanently erase all data
    -> reset security attributes
```

This is functionally adjacent to Case 44's key-authority questions, but the evidence here does not establish NIST sanitization compliance, forensic resistance, or a universal cryptographic-erasure implementation.

The important separation is:

> **configuration authority != key authority != payload-erasure authority.**

## Case 145 — reuse admission

Case 145 separates JFFS2 erase completion / cleanmarker qualification from later free-list admission.

Case 131 provides a different functional pattern:

```text
retire old configuration relation
    -> disk reaches Ready / new-configuration path
```

The commonality is only that **reuse authority is mediated by retained state**.

No filesystem/RAID implementation lineage is asserted.

---

# IV. Philosophical interpretation

**I — optional interpretation.**

This evidence makes a useful distinction between **bits that survive** and **the relation that tells a system what those bits are allowed to mean**.

A disk can still physically contain old payload while the controller has forgotten or deleted the foreign array relation needed to expose that payload as the former virtual disk. In that bounded sense, `forgetting` can occur at an authority/interpretation layer before it occurs at the material layer.

The inverse also holds: retaining the metadata does not automatically make the data current, reconstructable, or trustworthy.

This interpretation is secondary. Dell's manual documents operations and warnings; it does not present a philosophy of memory or identity.

---

# V. Explicit non-claims

This evidence does **not** establish any of the following:

1. Dell invented foreign configuration.
2. PERC 6 was the first RAID controller to store topology state on member disks.
3. The PERC 6 on-disk format is SNIA DDF.
4. The exact byte offsets or field layout of PERC foreign metadata.
5. The exact atomicity guarantees of `Clear`.
6. That `Clear` leaves every former payload sector untouched.
7. That payload is forensically recoverable after every `Clear`.
8. That an ordinary foreign-configuration `Clear` is automatically secure sanitization.
9. That every `Clear` path avoids payload erasure; the 2013 secured-foreign path explicitly requires Instant Secure Erase under the documented key condition.
10. That `Clear` is the same operation as `Format`.
11. That `Clear` is the same operation as virtual-disk `Initialization`.
12. That successful `Import` proves payload integrity.
13. That successful `Import` proves parity consistency.
14. That successful `Import` means no rebuild is required.
15. That `Ready` means the physical disk is blank.
16. That `Ready` by itself proves old data cannot be recovered.
17. That every PERC generation implements foreign state identically.
18. That the 2013 H710/H810 guide proves 2009 PERC 6 field-level internals.
19. That discarding pinned cache and clearing foreign metadata are equivalent.
20. That configuration deletion alone satisfies any regulatory sanitization requirement.
21. That an operator should experiment with `Clear` on a production array.
22. That this document provides recovery advice for a currently damaged array.

---

# VI. Claim ledger additions

| ID | Claim | Label | Evidence | Strength / limit |
| --- | --- | --- | --- | --- |
| G-131.27 | The June-2009 PERC 6 manual says controller firmware detects a physical disk with existing `foreign metadata` and flags it foreign. | `H/P*` | A | direct Dell-authored terminology; mirror provenance caveat |
| G-131.28 | The PERC 6 Foreign Configuration View can expose configuration detail before import. | `H/P*` | A | direct |
| G-131.29 | PERC 6 `Import` adopts/merges foreign configuration, while `Clear` deletes foreign configuration from reinserted disks. | `H/P*` | A | direct repeated operation semantics |
| G-131.30 | After clearing foreign configuration, PERC 6 documents the physical disk entering `Ready` state and warns of possible data loss. | `H/P*` | A | direct troubleshooting-table statement |
| G-131.31 | In the same PERC 6 glossary, `Format` is defined as writing a value to all physical-disk data fields. | `H/P*` | A | direct terminology contrast |
| G-131.32 | The same glossary defines virtual-disk initialization as zeroing data fields / generating parity and says it erases prior data. | `H/P*` | A | direct terminology contrast |
| G-131.33 | Therefore `Clear Foreign Configuration` is not evidenced as either `Format` or virtual-disk `Initialization`. | `E`, `X` | A | strong same-manual contrast; does not prove sector-level aftermath |
| G-131.34 | In documented PERC 6 cases, import may be followed by automatic rebuild and Dell recommends consistency checking after rebuild. | `H/P*` | A | direct ordered sequence |
| G-131.35 | Foreign-config visibility does not guarantee later importability because current drive state is re-evaluated and failed/offline drives cannot be imported. | `H/P*`, `E` | A | direct constraint + bounded reconstruction |
| G-131.36 | Preserved/pinned dirty cache is a separate retained object with a separate discard path from disk-side foreign configuration. | `H/P*`, `E` | A | direct neighboring manual sections |
| G-131.37 | Configuration retirement can remove ordinary PERC recoverability without evidence of whole-medium overwrite. | `E` | A | supported by clear-vs-format definitions; no forensic claim |
| G-131.38 | The Dell-hosted March-2013 PERC guide independently preserves the preview / Import / Clear / possible rebuild / consistency-check separation. | `H/P` | B | later product continuity; direct Dell-hosted source |
| G-131.39 | Ordinary foreign-clear semantics alone do not prove whole-medium sanitization. | `X`, `E` | A, B | operation-boundary claim; not a forensic recoverability claim |
| G-131.40 | Import, rebuild, and consistency checking are distinct PERC operations/phases. | `H/P*`, `H/P`, `E` | A, B | direct sequence in both generations |
| G-131.41 | 24-Jun-2009 is a directly inspected manual-documentation point, not invention priority for foreign-clear semantics. | `X` | A | chronology guardrail |
| G-131.42 | In the March-2013 secured-foreign path, clearing a foreign configuration secured with a different key requires Instant Secure Erase. | `H/P` | B | direct Dell-hosted exception |
| G-131.43 | Dell defines Instant Secure Erase as permanently erasing all data on the encryption-capable physical disk and resetting security attributes. | `H/P` | B | direct |
| G-131.44 | Therefore the high-level label `Clear` does not uniquely determine physical-erasure semantics without the security context and concrete execution path. | `E` | A, B | contextual reconstruction |

---

# VII. Prior-art / terminology boundary

The 2009 manual is useful here for **terminology and operation semantics**, not invention chronology.

The currently inspected Case 131 floor remains Dell's November-2007 firmware documentation. This deepening does not move that floor earlier.

It does, however, strengthen the vocabulary record by directly pairing all of these terms in one product manual:

```text
foreign metadata
foreign configuration
Import
Clear
Ready
Format
Initialization
rebuild
Consistency Check
pinned cache
discard cache
```

That co-location lets the project distinguish several operations without importing meanings from later RAID tooling.

A broader prior-art investigation of earlier PERC/MegaRAID foreign-metadata behavior belongs in `tmzncty/computing-archaeology`. A fresh repository search found no existing dedicated PERC foreign-configuration packet to reuse.

---

# VIII. Remaining evidence debt

This bounded deepening closes the narrow `Clear semantics / whole-medium overwrite ambiguity` at the **vendor terminology** level, but leaves several questions open:

- exact PERC 6 on-disk metadata layout and update atomicity;
- whether and how foreign-metadata clear is journaled or made crash-safe;
- failure during `Clear` itself;
- controller-NVRAM corruption rather than replacement;
- cross-generation PERC metadata compatibility;
- failed/corrupt/nontransportable cache modules;
- encrypted virtual-disk key loss;
- independent laboratory fault injection;
- forensic measurement of sectors before/after `Clear`;
- earlier RAID-controller prior art.

These should not be inferred from the present documentation.

---

# IX. Source pointers

1. Dell, _PERC 6/i, PERC 6/E and CERC 6/i User's Guide_, `Dell_PERC6.2_UG.book`, page footer dated 24 Jun 2009. Surviving searchable Dell-authored copy:
   https://manualzilla.com/doc/7425219/dell-poweredge-expandable-raid-controller-3-user-s-guide

   Key inspected locations:
   - pp. 89–92: import/clear, preview, member-state constraints, rebuild follow-up;
   - p. 93: preserved/pinned cache and discard warnings;
   - p. 116: firmware detection of `foreign metadata`; Clear -> `Ready`; data-loss warning;
   - pp. 142–143 glossary: `Foreign Configuration`, `Format`, `Initialization`.

2. Dell, _PowerEdge RAID Controller (PERC) H310, H710, H710P, and H810 User's Guide_, Rev. A02, March 2013, Dell-hosted PDF:
   https://dl.dell.com/manuals/common/poweredge-rc-h710_user%27s%20guide_en-us.pdf

   Key inspected locations:
   - pp. 44–46: Foreign View preview, Import / Clear alternatives, rebuild follow-up, consistency check, preserved-cache discard;
   - pp. 68–69: secured foreign import/clear, Instant Secure Erase requirement under a different security key, and Dell's permanent-erasure definition;
   - p. 14: full initialization overwrites all blocks; fast initialization overwrites only the first and last 8 MB.

---

# X. Integration target

Canonical case:

[Case 131 — Dell PERC Foreign Configuration: Retained Array Topology Across Controller Replacement](../cases/131-dell-perc-foreign-configuration-controller-replacement.md)

Recommended canonical additions from this evidence are deliberately compact:

```text
foreign metadata detected
    != configuration imported

Clear foreign configuration
    -> configuration relation retired
    -> disk can become Ready
    != evidence of Format / Initialization / whole-medium erase

secured foreign config + different key
    -> Clear requires Instant Secure Erase
    -> permanent erase

Import
    != Rebuild
    != Consistency Check

foreign-configuration Clear
    != pinned-cache Discard
```

This evidence should deepen Case 131 without changing its `grounded` maturity.
