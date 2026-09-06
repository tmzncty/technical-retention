# Dell PERC / LSI MegaRAID Patrol Read: Media Verification Versus RAID Consistency Checking

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
