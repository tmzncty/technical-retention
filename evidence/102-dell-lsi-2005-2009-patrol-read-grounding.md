# Evidence Record 102 — Dell / LSI 2005–2009 Patrol Read Grounding

## Purpose

Ground [`cases/102-perc-megaraid-patrol-read-consistency-boundary.md`](../cases/102-perc-megaraid-patrol-read-consistency-boundary.md) with two 2005 Dell PERC maintenance documents and a later LSI MegaRAID manual-family continuity witness.

The record is intentionally bounded. It establishes a controller-level distinction between **physical-media Patrol Read** and **RAID redundancy Consistency Check**. It does not claim a complete patrol-read genealogy or prove that Dell PERC, LSI MegaRAID, T10 BMS, and other vendors share one implementation lineage.

---

## Claim matrix

| ID | Claim | Type | Evidence | Strength |
|---|---|---|---|---|
| 102-A | Dell's July 2005 maintenance guide says June/July 2005 PERC 3/4/4e firmware/driver updates introduced `Background Patrol Read` for the specified supported families. | historical record | Dell, *Maintenance Best Practices for Direct-Attached SCSI Solutions*, Rev. 1.1, 20 July 2005 | **direct / manufacturer primary text via mirror** |
| 102-B | Dell describes Background Patrol Read as a physical-disk read-verify/media-level operation for finding bad blocks, with automatic and manual modes. | historical record | same Dell guide | **direct / manufacturer primary text via mirror** |
| 102-C | Dell separately describes Consistency Check as a data-level operation that validates data/parity and can also encounter/remediate bad blocks. | historical record | same Dell guide | **direct / manufacturer primary text via mirror** |
| 102-D | Dell's November 2005 SCSI reference guide explicitly says Patrol Read and Consistency Check are not the same operation and contrasts physical-media defects with parity validation. | historical record | Dell SCSI Storage Solution Team, 17 Nov. 2005, p. 33 | **direct / manufacturer primary text via mirror** |
| 102-E | The inspected LSI manual-family revision table records versions from Dec. 2005 through Rev. F in Mar. 2009, including v2.0 Rev. B in June 2007. | historical record | LSI MegaRAID SAS Software User Guide revision table | **direct / manufacturer manual text via mirror** |
| 102-F | The inspected later MegaRAID text treats Patrol Read as controller-scoped drive-error checking with auto/manual/disabled settings and Consistency Check as redundant-virtual-drive data/parity verification. | historical record | LSI `80-00156-01` Rev. F text | **direct / later manufacturer-manual continuity witness via mirror** |
| 102-G | MegaRAID event vocabulary distinguishes corrected medium errors, uncorrectable medium errors, bad-block puncturing, and inconsistent parity. | historical record | LSI Rev. F event table | **direct / later manufacturer-manual continuity witness via mirror** |
| 102-H | `physical-media verification ≠ redundancy-consistency verification` is an analytical relation supported by Dell's explicit task distinction. | engineering reconstruction | synthesis across 102-B/C/D | **strong bounded reconstruction** |
| 102-I | `drive-internal BMS ≠ RAID-controller Patrol Read` is a layer distinction; functional similarity does not establish genealogy. | engineering reconstruction / analogy | Case 101 + Dell 2005 | **bounded reconstruction** |
| 102-J | PERC/MegaRAID terminology similarity does not by itself prove one controller lineage. | anti-anachronism / genealogy boundary | source limitations | **explicitly bounded** |

---

## Source 1 — Dell, *Maintenance Best Practices for Direct-Attached SCSI Solutions*, Rev. 1.1

**Date:** 20 July 2005.

**Current inspected text mirror:** <https://manualzilla.com/doc/7358644/dell-dc--3-user-guide>

### Directly supports

The document states that June/July 2005 firmware and driver updates to supported PERC 3, PERC 4, and PERC 4e controllers introduced `Background Patrol Read`. It describes the feature as a background read-verify across the physical disk for bad blocks, explicitly calls it a **media level** feature, and says it does not verify data inside the block or stripe.

It describes automatic and manual run modes. The automatic mode is intended for continual checking and remapping of discovered media errors; the manual mode is a faster one-run scan using different throttling parameters.

Immediately afterward the guide describes `Consistency Check` as a **data level** check that verifies data inside the block/stripe and checks bad blocks. It says the operation can find and repair data/parity mismatches. It also describes bad-block handling through grown-defect recording, parity reconstruction where possible, and writing recovered data to a new location.

### Does not support

- invention of background disk scanning;
- all PERC generations or all firmware versions;
- a claim that Patrol Read validates parity;
- a claim that Consistency Check is only a media scan;
- guaranteed reconstruction for every media error;
- a direct genealogy from T10 BMS;
- secure erasure of a remapped sector.

### Transport limitation

The currently accessible copy is a text mirror of a document whose title/date/body identify it as Dell material. Until a stable Dell-hosted facsimile is reacquired, cite it as **manufacturer-primary content via third-party mirror**, not as an independently preserved Dell archive endpoint.

---

## Source 2 — Dell SCSI Storage Solution Team, *A Reference Guide for Optimizing Dell SCSI Solutions*, Rev. A02

**Date:** 17 November 2005.

**Inspected page mirror:** <https://www.manualowl.com/m/Dell/341-7044/Manual/370091?page=33>

**Alternate whole-document mirror:** <https://www.manualowl.com/m/Dell/PowerVault-220S/Manual/189886>

### Directly supports

Page 33 describes Patrol Read as a preventative-maintenance background operation on supported PERC 3/4/4e controller families. It says Patrol Read examines each block in a configured physical disk for media errors, can attempt repair through bad-block reallocation, and provides Manual and Automatic modes.

Most importantly, the page states that Patrol Read and Consistency Check **are not the same operations**: the former examines the physical disk for media defects, while the latter validates data through parity.

This is the strongest concise primary wording for the case's bounded distinction.

### Boundary

The guide is PERC-specific operational guidance, not a general RAID standard and not an origin history of proactive verification.

---

## Source 3 — LSI, *MegaRAID SAS Software User Guide*, document family `80-00156-01`

**Inspected text mirror:** <https://manualzz.com/doc/7972547/lsi-megaraid-sas-raid-controllers--megaraid-storage-manag...>

**Additional text mirror:** <https://manualzilla.com/doc/6892884/megaraid-sas-software-user-s-guide>

### Revision-history evidence

The inspected LSI manual-family revision table records:

- `DB15-000339-00`, December 2005 — Version 1.0;
- `80-00156-01 Rev. A`, August 2006 — Version 1.1;
- `80-00156-01 Rev. B`, June 2007 — Version 2.0;
- `80-00156-01 Rev. C`, July 2007 — Version 2.1;
- later Rev. D/E/F updates through March 2009.

This supports chronology of the **manual family**. It does not prove that every sentence in the inspected Rev. F text was present in the earlier revisions.

### Directly supports in the inspected later text

The later text describes Patrol Read as reviewing the system for drive errors that could lead to failure and taking corrective action depending on configuration/error type. It exposes automatic/manual/disabled modes, rate, delay, and status.

It says a Patrol Read can verify sectors of drives connected to the controller, including system-reserved areas of RAID-configured drives, and can operate across all RAID levels and hot spares.

Separately, Consistency Check verifies correctness of data in redundant virtual drives; for parity systems it computes data and compares the result with parity. The later event table distinguishes Patrol Read corrected/uncorrectable medium errors and bad-block puncturing from Consistency Check events including inconsistent parity and uncorrectable double medium errors.

### Boundary

Use the detailed behavior as a **later continuity witness**. Do not back-project Rev. F wording into December 2005 or June 2007 without direct version-specific facsimile inspection.

---

## Source 4 — Dell Power Solutions article, bibliographic lead only

**Citation lead:** Drew Habas and John Sieber, “Background Patrol Read for Dell PowerEdge RAID Controllers,” *Dell Power Solutions*, February 2006, pp. 73–75.

A historical Dell URL is widely cited as:

<http://www.dell.com/downloads/global/power/ps1q06-20050212-Habas.pdf>

### Current use

This article is a strong **future primary-source target**, but it was not directly inspected as a stable primary facsimile in this slice. Secondary bibliographic records and later patent literature confirm that such an article was cited, but Case 102's central claims do not depend on it.

Do not promote claims from this bibliographic lead until the actual article is directly inspected.

---

## Cross-case evidence boundary

### Case 101 — T10 BMS

Case 101 directly shows that T10's 2005 BMS standardization effort acknowledged earlier proprietary drive methods and host/OS scanning. Reuse that fact only as a prior-art guardrail against a Dell invention claim.

The maintenance locus differs: Case 101 is device-side BMS; Case 102 is RAID-controller-level Patrol Read. Similar proactive-read function is a functional analogy, not a proven implementation lineage.

### Case 14 — SCSI reassignment

Reuse Case 14 for the distinction between logical-block continuity, physical-sector replacement, and payload preservation. Case 102 adds controller-driven discovery and possible parity-based reconstruction; it does not rewrite reassignment history.

### Case 17 — RAID reconstruction

Reuse Case 17 for parity algebra and degraded-repair margin. Case 102 only shows that a maintenance process may discover a defect while redundancy is still available to participate in correction.

### Case 18 / Synthesis 08

Use only as higher-layer comparison. ZFS checksum authority and distributed integrity maintenance are not equivalent to media-level Patrol Read or RAID parity Consistency Check.

---

## Evidence classification

### Historical record (`H`)

Safe to state:

- Dell's July 2005 guide documents the June/July 2005 introduction of named `Background Patrol Read` support for bounded PERC controller families;
- Dell describes Background Patrol Read as media-level physical-disk read verification and Consistency Check as a data/parity-level task;
- Dell's November 2005 guide explicitly says the two are not the same operation;
- both tasks can encounter media defects, so the distinction is not a claim of disjoint physical I/O;
- the inspected LSI manual-family revision table records a document lineage from December 2005 through 2009;
- the inspected later LSI text retains distinct Patrol Read and Consistency Check scopes and event classes.

### Engineering reconstruction (`E`)

Safe only as project analysis:

- `physical-media verification ≠ redundancy-consistency verification`;
- `physical-drive coverage ≠ virtual-drive redundancy coverage`;
- `task identity ≠ error severity ≠ repair outcome`;
- `automatic maintenance scheduling ≠ permanent health certificate`;
- `event-log evidence ≠ repaired payload`.

### Functional analogy (`A`)

Allowed with labels:

- T10 BMS, PERC Patrol Read, ZFS scrub, and distributed background scanners can all be compared as proactive verification before demand;
- this does not establish identical maintenance locus, integrity authority, or genealogy.

### Philosophical interpretation (`I`)

Bounded inference only:

- RAID makes technical confidence layered: physical readability and relational redundancy consistency can require distinct maintenance operations;
- this does not imply that verification itself creates physical persistence.

---

## Claims explicitly not established

Do **not** use this record to claim:

- Dell or LSI invented disk scrubbing;
- T10 BMS and PERC Patrol Read are historically synonymous;
- PERC and MegaRAID share a directly demonstrated firmware lineage;
- the 2009 LSI wording was already identical in the 2005/2007 revisions;
- Patrol Read validates parity or end-to-end application checksums;
- Consistency Check guarantees all physical sectors have been recently exercised;
- every discovered bad block can be reconstructed successfully;
- controller remapping securely erases the old physical embodiment.

---

## Related-repository check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `patrol read` found no dedicated overlapping case in the current search surface. A later broad controller genealogy should therefore be coordinated there; Case 102 should remain a retention-specific bounded controller example.

---

## Result

**Grounded.**

The two 2005 Dell texts are sufficient to establish the bounded PERC historical vocabulary and the central media-level versus data/parity-level distinction. The later LSI manual is used conservatively as a continuity and event-model witness rather than as proof of exact 2005/2007 wording. Together the evidence supports a precise retention relation without inventing a universal scrub history: proactive physical-media qualification, redundancy-consistency qualification, defect handling, reconstruction, and later verification are separate operations and state transitions.
