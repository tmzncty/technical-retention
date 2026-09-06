from pathlib import Path

CASE_PATH = Path('cases/102-perc-megaraid-patrol-read-consistency-boundary.md')
EVIDENCE_PATH = Path('evidence/102-dell-lsi-2005-2009-patrol-read-grounding.md')
ROADMAP_PATH = Path('ROADMAP.md')
INDEX_PATH = Path('CASE_INDEX.md')

case_text = r'''# Dell PERC / LSI MegaRAID Patrol Read: Media Verification Versus RAID Consistency Checking

## Scope

- **Object / system:** Dell PowerEdge RAID Controller (PERC) Background Patrol Read in 2005 documentation, with later LSI MegaRAID patrol-read / consistency-check continuity bounded by the 2009 revision of the MegaRAID SAS Software User Guide.
- **Retention question:** what changes when proactive maintenance is moved above an individual disk into a RAID controller that can both exercise physical media and use redundant array state, while still keeping media verification distinct from redundancy-consistency verification?
- **Status:** `grounded`.

This is **not** a complete history of RAID scrubbing, SCSI VERIFY, T10 Background Medium Scan, parity checking, SMART, PERC firmware, LSI/MegaRAID genealogy, or latent-sector-error mitigation. Case 101 already grounds the 2004–2007 device-side SCSI Background Medium Scan (BMS) boundary. Case 102 takes the next bounded controller-level slice:

> **How did period PERC documentation distinguish Background Patrol Read from Consistency Check, and what retention relations become visible when a controller can discover media defects before demand while separately validating RAID redundancy?**

The project terms `media-readability qualification`, `redundancy-consistency qualification`, `maintenance locus`, and `coverage certificate` below are **engineering reconstructions**, not Dell or LSI historical vocabulary.

---

## Historical vocabulary

The inspected sources directly use terms including:

- `Background Patrol Read` / `Patrol Read`;
- `Consistency Check`;
- `read verify`;
- `media level feature`;
- `data level check`;
- `media errors` / `bad blocks`;
- `grown defects list`;
- `reallocate` / `remap`;
- `data parity`;
- `Automatic` / `Manual` patrol-read modes;
- `Patrol Read Rate`;
- `Consistency Check rate`;
- `hot spare`;
- `virtual drive` in later MegaRAID documentation.

Do not silently normalize these terms into T10 `Background Medium Scan`, ZFS `scrub`, HDFS `BlockScanner`, or a universal `scrubbing` state machine. They can be compared functionally while their implementation layers and historical vocabularies remain distinct.

---

## Historical record

### H/P — Dell documented Background Patrol Read as a PERC firmware feature in mid-2005

Dell's **Maintenance Best Practices for Direct-Attached SCSI Solutions**, Revision 1.1, dated 20 July 2005, says that the June/July 2005 firmware and driver updates for PERC 3, PERC 4, and PERC 4e controllers, excluding PERC 3/Di and PERC 4/im, introduced a feature called `Background Patrol Read`.

The document describes it as a background `read verify` across the physical disk for finding bad blocks. It calls the feature **media level** and explicitly says it does not verify data inside the block or stripe. Its automatic mode is described as continual checking so that media errors can be detected and data remapped during product life; a manual mode provides a one-run scan with different throttling behavior.

This is a bounded product-family introduction claim:

> **Dell documented Background Patrol Read as newly introduced for these PERC firmware/driver families in June/July 2005.**

It is **not** evidence that Dell invented proactive disk verification in 2005. Case 101's T10 proposal, dated March 2005, already says proprietary drive and host/OS background-scan methods existed.

### H/P — Dell separated media-level Patrol Read from data/parity-level Consistency Check

The same July 2005 maintenance guide immediately distinguishes `Consistency Check` from Background Patrol Read. Consistency Check is described as a data-level check that verifies data inside the block or stripe as well as checking for bad blocks. For redundant arrays it can find stripes where data and parity do not match and repair the inconsistency.

The guide also says that medium defects found during Consistency Check can be entered in the drive's grown-defect list; damaged-block data may be reconstructed through parity and written to a new location.

Therefore the historical record itself gives two maintenance relations that overlap in physical I/O but are not identical:

```text
Patrol Read
    -> exercise physical-disk sectors
    -> discover / sometimes remediate media defects

Consistency Check
    -> exercise RAID logical/redundancy state
    -> compare data with redundant/parity relation
    -> can also encounter and remediate media defects
```

This blocks two symmetric overclaims:

> **Patrol Read ≠ Consistency Check.**

and:

> **task distinction ≠ disjoint error coverage.**

### H/P — Dell's November 2005 reference guide repeats the boundary as operational guidance

Dell's **A Reference Guide for Optimizing Dell SCSI Solutions**, authored by the Dell SCSI Storage Solution Team and dated 17 November 2005, describes Patrol Read as a preventative-maintenance background operation on supported PERC 3/4/4e controllers. It says Patrol Read examines each block of a configured physical disk for media errors and attempts to repair them through bad-block reallocation.

The guide then states explicitly that Patrol Read and Consistency Check are not the same operation: Patrol Read examines the physical disk for media defects, while Consistency Check validates data using data parity.

This second Dell document is important because the distinction is not merely inferred from command names. It is spelled out as the product's maintenance model.

### H/P — controller-level proactive verification adds array redundancy to the remediation path

The July 2005 Dell guide's surrounding defect discussion says that when a bad block is encountered on a normal read in a redundant array, the controller may reconstruct missing data from parity, remap the bad location, and write the reconstructed data to the replacement location. Its Consistency Check description similarly ties discovered bad blocks to grown-defect handling and parity reconstruction.

This differs from a bare statement that the disk itself can relocate a sector. A RAID controller has access to an additional relation: other members can sometimes supply a reconstruction source.

But that capability must not be converted into a guarantee:

> **redundancy available in principle ≠ successful reconstruction for every discovered defect.**

Double faults, degraded arrays, absent redundancy, or additional unreadable sectors can remove that path. Case 17 remains the canonical parity-reconstructability case; Case 14 remains the canonical logical-block / physical-reassignment case.

### H/P — later LSI MegaRAID documentation retains Patrol Read and Consistency Check as distinct controller tasks

The LSI **MegaRAID SAS Software User Guide**, document family `80-00156-01`, has a revision table showing Version 1.0 in December 2005, Version 1.1 in August 2006, Version 2.0 / Rev. B in June 2007, Version 2.1 / Rev. C in July 2007, and later revisions through Rev. F in March 2009.

The inspected Rev. F text describes Patrol Read as reviewing the system for drive errors that could lead to failure and taking corrective action depending on drive-group configuration and error type. It exposes controller-level automatic/manual/disabled modes, patrol-read rates, execution delay, and status. Elsewhere, it defines Consistency Check as verifying correctness of data in redundant virtual drives; in parity layouts, that means computing data and comparing it with parity.

The same guide says Patrol Read can verify sectors of drives connected to the controller, including system-reserved areas on configured drives, and can cover all RAID levels and hot spares. Consistency Check, by contrast, is scoped to redundant virtual drives.

This is a **later continuity witness**, not proof that every sentence in the 2009 Rev. F text was already present in the December 2005 or June 2007 editions. The revision table anchors the document family chronology; exact wording is attributed only to the inspected later revision.

### H/P — later MegaRAID event vocabulary preserves distinct maintenance outcomes

The inspected MegaRAID guide's event table contains separate patrol-read events for a corrected medium error, an uncorrectable medium error, and bad-block puncturing. Consistency Check has its own events for corrected medium errors, completion with corrections, uncorrectable double medium errors, and inconsistent parity.

These event classes are especially useful retention evidence because they prevent one generic `scan found a problem` state:

```text
maintenance task identity
    !=
medium-error severity
    !=
parity-consistency verdict
    !=
repair outcome
```

An event log records controller knowledge and task progress; it is not the user payload and is not by itself proof that redundancy or physical readability has been fully restored.

---

## Retained state and maintenance relations

Case 102 contains at least six distinct state classes.

### 1. Physical sector embodiments

Patrol Read exercises physical-drive sectors to discover medium defects before ordinary demand necessarily reaches them.

### 2. Logical / virtual-drive payload

The controller presents RAID virtual drives whose logical state can remain serviceable while particular physical sectors are remapped or reconstructed.

### 3. Redundancy relation

Mirrored or parity information is retained separately from the mere readability of each sector. Consistency Check asks whether those redundant representations still agree according to the RAID relation.

### 4. Defect / reassignment state

Drive grown-defect lists, remapped locations, and controller knowledge of bad blocks condition whether a physical location remains eligible for future service.

### 5. Maintenance scheduling / rate state

Automatic versus manual Patrol Read, execution delay, task rate, and idle/background scheduling determine when proactive verification gets maintenance opportunity.

This control state is neither payload nor proof of media health.

### 6. Maintenance evidence / event state

Task status, discovered medium errors, inconsistent parity events, corrections, and failed/uncorrectable outcomes retain evidence about what the controller observed and attempted.

This evidence can guide later action without being equivalent to the repaired state itself.

---

## Trigger and coverage structure

The controller-level case exposes several non-identical clocks and scopes:

1. time since the last Patrol Read pass;
2. automatic/manual maintenance schedule;
3. foreground-I/O load and controller maintenance opportunity;
4. Patrol Read physical-drive coverage;
5. Consistency Check virtual-drive/redundancy coverage;
6. defect creation time, usually unknown;
7. defect discovery time;
8. correction/reallocation/reconstruction time;
9. later verification time after repair.

Thus:

> **maintenance schedule ≠ physical hazard clock.**

and:

> **completed Patrol Read coverage ≠ timeless media certificate.**

and:

> **completed Patrol Read ≠ completed redundancy-consistency qualification.**

---

## Cross-case comparison

### Case 101 — SCSI Background Medium Scan

Case 101 is device-side. Its T10 proposal intentionally moves scanning into the SCSI device server and emphasizes that ordinary SCSI-interface bandwidth need not be consumed by the background operation.

Case 102 is controller-level. Dell describes PERC Background Patrol Read as a controller maintenance feature operating across configured physical disks, while RAID redundancy can participate in remediation.

The functional similarity is real: both proactively exercise medium readability before application demand. The historical identity is not established:

> **drive-internal BMS ≠ RAID-controller Patrol Read.**

No `BMS -> PERC Patrol Read` genealogy is asserted here.

### Case 14 — SCSI defect reassignment

Case 14 owns the distinction between one LBA and the physical sector currently serving it. Case 102 adds a controller that can discover a problem proactively and, in redundant arrays, may possess another source from which to reconstruct the logical payload before or while remapping.

Therefore:

> **bad-block reallocation ≠ payload reconstruction.**

and:

> **payload reconstruction ≠ proof that all redundant relations are consistent.**

### Case 17 — RAID parity reconstruction

Parity can provide a recovery source after a known missing/unreadable contribution, but Patrol Read is not itself the parity algebra and Consistency Check is not identical to rebuild.

> **media-defect discovery ≠ algebraic reconstructability ≠ repair completion.**

### Case 18 / Synthesis 08 — proactive integrity

ZFS scrub validates checksummed end-to-end block identity and can repair from redundancy. Dell/LSI Patrol Read is lower-layer media verification; Consistency Check validates RAID redundancy/parity. The shared `proactive verification` function does not make their integrity authorities identical.

> **media readability ≠ parity consistency ≠ end-to-end checksum integrity.**

---

## Prior-art and genealogy boundary

This case makes **no invention-priority claim** for:

- disk scrubbing;
- background read verification;
- SCSI VERIFY sweeps;
- T10 Background Medium Scan;
- bad-sector remapping;
- RAID consistency checking;
- parity scrubbing;
- the term `Patrol Read` outside the bounded Dell/LSI material.

The July 2005 Dell document supports a narrow statement that a feature named `Background Patrol Read` was introduced in specified PERC firmware/driver updates. It does not establish first invention of the function.

Likewise, the later LSI manual demonstrates the persistence of a controller-level `Patrol Read` / `Consistency Check` distinction in a MegaRAID document family. This case does **not** infer a direct PERC-to-MegaRAID implementation lineage merely from shared terminology or known industry relationships. A proper genealogy would require controller silicon/firmware lineage, release notes, OEM mappings, and earlier vendor documentation.

A fresh repository search found no dedicated Patrol Read history in `tmzncty/computing-archaeology`. Broader controller genealogy should be coordinated there rather than grown opportunistically inside this retention case.

---

## Engineering reconstruction

Case 102 adds these controlled relations:

1. `physical-media verification ≠ redundancy-consistency verification`;
2. `RAID-controller Patrol Read ≠ drive-internal Background Medium Scan`;
3. `physical-drive maintenance scope ≠ redundant virtual-drive consistency scope`;
4. `task distinction ≠ disjoint error coverage`;
5. `correctable medium error ≠ uncorrectable medium error`;
6. `bad-block handling / puncture ≠ successful payload restoration`;
7. `Patrol Read completion ≠ parity-consistency certification`;
8. `Consistency Check completion ≠ controller-wide physical-media coverage certification`;
9. `automatic patrol scheduling ≠ maintenance-free persistence`;
10. `maintenance event/progress state ≠ user payload state`;
11. `named PERC feature introduction ≠ invention of background disk verification`;
12. `shared Patrol Read terminology/function ≠ proven controller genealogy`;
13. `media readability ≠ parity consistency ≠ end-to-end checksum integrity`.

These are project analytical statements, not a claim that Dell or LSI engineers used this ontology.

---

## Philosophical interpretation — bounded

Case 102 gives a precise example of **layered technical confidence**. A RAID controller may need evidence that physical sectors remain readable and separate evidence that redundant representations remain mutually consistent. The logical object can therefore depend on several maintenance judgments that are produced by different operations at different scopes.

This does not mean that redundancy is a philosophical form of memory or that verification creates persistence by observation. The technical point is narrower: **continued availability can depend on maintaining both embodiments and the relations that authorize reconstruction among them.**

---

## Evidence limits / future work

Still open after this case:

- direct archived facsimiles from Dell rather than text mirrors for the July and November 2005 documents;
- the February 2006 Dell Power Solutions article as a directly inspected primary facsimile;
- exact PERC firmware release-note chronology and controller/OEM hardware lineage;
- exact text comparison across MegaRAID document versions 1.0, 1.1, 2.0, 2.1, and later revisions;
- host-driven SCSI VERIFY scrub history;
- IBM ServeRAID, Adaptec, HP Smart Array, and other controller terminology/history;
- cross-vendor `Patrol Read` / `Media Patrol` / `Consistency Check` genealogy;
- empirical fault injection demonstrating correctable versus uncorrectable medium-error paths;
- URE-aware rebuild and scrub scheduling policy;
- secure-erasure implications of remapped/punctured sectors.

---

## Result

**Grounded.**

The 2005 Dell material directly establishes a named PERC Background Patrol Read regime and, crucially, explicitly separates physical-media verification from Consistency Check's data/parity verification. Later LSI MegaRAID documentation supplies a bounded continuity witness for controller-level scheduling, scope, task-specific events, and the continued separation of Patrol Read from redundant-virtual-drive consistency checking. The case therefore closes one named-controller slice without converting functional similarity into a universal scrub model or a historical genealogy.
'''

evidence_text = r'''# Evidence Record 102 — Dell / LSI 2005–2009 Patrol Read Grounding

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
'''

if CASE_PATH.exists() or EVIDENCE_PATH.exists():
    raise SystemExit('Case/evidence 102 path already exists; refusing to overwrite')
CASE_PATH.write_text(case_text.rstrip('\n') + '\n', encoding='utf-8')
EVIDENCE_PATH.write_text(evidence_text.rstrip('\n') + '\n', encoding='utf-8')

# ROADMAP: update the open frontier coherently and add one bounded completion bullet.
roadmap = ROADMAP_PATH.read_text(encoding='utf-8')
if 'cases/102-perc-megaraid-patrol-read-consistency-boundary.md' in roadmap:
    raise SystemExit('ROADMAP already contains Case 102')
lines = roadmap.splitlines()
case101_idxs = [i for i, line in enumerate(lines) if line.startswith('- [x] SCSI Background Medium Scan / proactive medium-readability boundary —')]
if len(case101_idxs) != 1:
    raise SystemExit(f'Expected exactly one Case 101 roadmap bullet, got {len(case101_idxs)}')
i = case101_idxs[0]
lines[i] = lines[i].replace(
    'host SCSI VERIFY history, named RAID-controller Patrol Read/Consistency Check genealogy, field fault injection, and URE-aware policy remain open and should be coordinated with `computing-archaeology`.',
    'host SCSI VERIFY history, broader cross-vendor Patrol Read/Consistency Check genealogy beyond Case 102, field fault injection, and URE-aware policy remain open and should be coordinated with `computing-archaeology`.'
)
case102_bullet = '- [x] Dell PERC / LSI MegaRAID Patrol Read versus Consistency Check boundary — [`cases/102-perc-megaraid-patrol-read-consistency-boundary.md`](cases/102-perc-megaraid-patrol-read-consistency-boundary.md), grounded by [`evidence/102-dell-lsi-2005-2009-patrol-read-grounding.md`](evidence/102-dell-lsi-2005-2009-patrol-read-grounding.md), uses two July/November 2005 Dell PERC maintenance documents plus a conservatively bounded later LSI MegaRAID continuity witness to separate controller-driven physical-media verification, redundant-virtual-drive parity consistency, maintenance scheduling/coverage, medium-error outcomes, bad-block handling, and reconstruction authority. This closes one named-controller slice without asserting Dell invention, T10 BMS→PERC descent, or PERC→MegaRAID firmware genealogy; host SCSI VERIFY, other controller families/cross-vendor terminology history, field fault injection, and URE-aware policy remain open.'
lines.insert(i + 1, case102_bullet)

syn_idxs = [j for j, line in enumerate(lines) if line.startswith('- [x] Proactive-integrity / defect-discovery / repair-margin synthesis —')]
if len(syn_idxs) == 1:
    j = syn_idxs[0]
    lines[j] = lines[j].replace(
        'the broader RAID-controller patrol-read genealogy beyond Case 101,',
        'the broader cross-vendor RAID-controller patrol-read genealogy beyond Cases 101–102,'
    )
ROADMAP_PATH.write_text('\n'.join(lines).rstrip('\n') + '\n', encoding='utf-8')

# CASE_INDEX: insert navigation/status row after Case 101 and append numbered findings.
index = INDEX_PATH.read_text(encoding='utf-8')
if '## Case 102 — Dell PERC / LSI MegaRAID Patrol Read findings' in index:
    raise SystemExit('CASE_INDEX already contains Case 102 findings')
idx_lines = index.splitlines()
row_idxs = [i for i, line in enumerate(idx_lines) if 'cases/101-scsi-background-medium-scan-proactive-defect-discovery.md' in line and line.startswith('| [')]
if len(row_idxs) != 1:
    raise SystemExit(f'Expected one Case 101 table row, got {len(row_idxs)}')
row = '| [Dell PERC / LSI MegaRAID Patrol Read: Media Verification Versus RAID Consistency Checking](cases/102-perc-megaraid-patrol-read-consistency-boundary.md) | **grounded** | controller-driven proactive physical-media verification + separate RAID redundancy consistency checking + bad-block remediation / optional reconstruction | separate media readability from parity consistency, maintenance scheduling from coverage proof, and repair capability from repair outcome without inventing a BMS/Patrol-Read genealogy | [2005–2009 Dell/LSI grounding record](evidence/102-dell-lsi-2005-2009-patrol-read-grounding.md); host SCSI VERIFY, cross-vendor controller genealogy, exact firmware lineage, and fault injection remain open |'
idx_lines.insert(row_idxs[0] + 1, row)
index = '\n'.join(idx_lines).rstrip('\n')
last = index.splitlines()[-1]
if not last.startswith('1518. **BMS standardization ≠ invention of background scanning'):
    raise SystemExit(f'Unexpected CASE_INDEX tail before Case 102: {last[:160]}')
findings = r'''

## Case 102 — Dell PERC / LSI MegaRAID Patrol Read findings

1519. **physical-media verification ≠ redundancy-consistency verification** — Dell explicitly separates Patrol Read's physical-disk/media-defect role from Consistency Check's data/parity validation role;
1520. **RAID-controller Patrol Read ≠ drive-internal Background Medium Scan** — both can proactively exercise media before demand, but Case 101 locates BMS inside the SCSI device server while Case 102 locates Patrol Read at the RAID-controller maintenance layer;
1521. **physical-drive maintenance scope ≠ redundant virtual-drive consistency scope** — later MegaRAID documentation allows Patrol Read across drives/hot spares and all RAID levels, while Consistency Check is defined for redundant virtual drives;
1522. **task distinction ≠ disjoint error coverage** — Dell Consistency Check can also encounter bad blocks, and later MegaRAID events show medium-error outcomes under both task families;
1523. **correctable medium error ≠ uncorrectable medium error** — later controller event vocabulary preserves separate outcomes rather than one generic bad-sector state;
1524. **bad-block handling / puncture ≠ successful payload restoration** — a controller can record or isolate a defective location without thereby proving that the logical data was reconstructed and restored;
1525. **Patrol Read completion ≠ parity-consistency certification** — completing a physical-media scan does not establish that redundant data/parity relations have been checked by Consistency Check;
1526. **Consistency Check completion ≠ controller-wide media-coverage certification** — validating redundant virtual-drive relations does not establish recent Patrol Read coverage of every physical scope such as hot spares or system-reserved areas;
1527. **automatic patrol schedule ≠ maintenance-free persistence** — automatic mode retains recurring maintenance policy, but continued verification still consumes controller time and competes with foreground/background work;
1528. **maintenance event/progress state ≠ user payload state** — controller logs/status retain evidence about scans, errors, and corrections without being the data whose retention is at issue;
1529. **named PERC feature introduction ≠ invention of background disk verification** — Dell can date introduction of `Background Patrol Read` to bounded PERC firmware/driver families without establishing priority over earlier proprietary, host, or device-side scanning;
1530. **shared `Patrol Read` terminology/function ≠ proven controller genealogy** — Dell PERC and later LSI MegaRAID material can be compared historically and functionally, but shared naming does not by itself prove firmware descent or OEM implementation identity;
1531. **media readability ≠ parity consistency ≠ end-to-end checksum integrity** — PERC/MegaRAID media checks, RAID consistency checks, and higher-layer ZFS-style checksum authority qualify different relations even when each is called proactive integrity maintenance.
'''
INDEX_PATH.write_text(index + findings.rstrip('\n') + '\n', encoding='utf-8')

# Lightweight structural validation before workflow commit.
for p in (CASE_PATH, EVIDENCE_PATH, ROADMAP_PATH, INDEX_PATH):
    text = p.read_text(encoding='utf-8')
    if not text.endswith('\n'):
        raise SystemExit(f'{p} missing final newline')
if case102_bullet not in ROADMAP_PATH.read_text(encoding='utf-8'):
    raise SystemExit('Case 102 roadmap bullet missing')
if '1531. **media readability ≠ parity consistency ≠ end-to-end checksum integrity**' not in INDEX_PATH.read_text(encoding='utf-8'):
    raise SystemExit('Case 102 findings missing')
if 'cases/102-perc-megaraid-patrol-read-consistency-boundary.md' not in INDEX_PATH.read_text(encoding='utf-8'):
    raise SystemExit('Case 102 case-table navigation row missing')
print('case102 integration patch prepared')
