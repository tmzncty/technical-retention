# Evidence Record 101 — T10 2004–2007 Background Medium Scan Grounding

## Purpose

Ground [`cases/101-scsi-background-medium-scan-proactive-defect-discovery.md`](../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md) with primary T10 standardization records, a named Seagate product manual, and one independent field-study context source.

This record is intentionally bounded. It establishes a 2004–2007 **SCSI device-side Background Medium Scan** regime and its relation to defect logging and conditional reassignment. It does not claim a complete history of disk scrubbing, RAID-controller patrol read, SCSI VERIFY, or defect management.

---

## Claim matrix

| ID | Claim | Type | Evidence | Strength |
|---|---|---|---|---|
| 101-A | By March 2005 T10 was standardizing control/status for BMS, while the proposal itself said proprietary drive methods and OS implementations already existed. | historical record | T10 `04-198r5`, p. 1 | **direct / primary** |
| 101-B | Device-side BMS reads medium blocks during background/idle operation to identify difficult/unreadable blocks, log problems, and optionally take vendor-specific recovery action. | historical record | `04-198r5`, Background scanning overview | **direct / primary** |
| 101-C | Background scanning is separated from ordinary SCSI-interface data transfer and scanned blocks are not retained in cache. | historical record | `04-198r5`, Background scanning overview | **direct / primary** |
| 101-D | Recoverable read errors and unreadable blocks have different paths; `ARRE` and `AWRE` separately govern automatic repair/relocation permissions. | historical record | `04-198r5`; reaffirmed/clarified in `05-340r3` | **direct / primary** |
| 101-E | BMS result state includes activity/suspension, count/progress, suspect locations, and `REASSIGN STATUS` indicating whether host action may remain. | historical record | `04-198r5`, interpreting logged results | **direct / primary** |
| 101-F | Pre-scan is a power-on regime that can convert writes to unscanned regions into write-and-verify until coverage advances. | historical record | `04-198r5`, Background pre-scan feature | **direct / primary** |
| 101-G | T10 plenary approved `04-198r5` for inclusion in SPC-4 and SBC-3 on 10 March 2005. | historical record | T10 `05-097r0`, §10.5 | **direct / committee record** |
| 101-H | January 2006 clarification renamed “scan failed” style warnings to “background scan detected medium error,” separating maintenance success from medium health. | historical record | T10 `05-340r3`, overview items 1–3 | **direct / primary** |
| 101-I | January 2006 work permits device-chosen scan order, e.g. based on physical layout rather than LBA order. | historical record | `05-340r3`, overview item 6 and revised model | **direct / primary** |
| 101-J | Seagate Cheetah 15K.5 FC Rev. C documents BMS as a self-initiated product feature and ties logged/reallocated sites to ARRE/AWRE policy. | historical record | Seagate 100384772 Rev. C, §7.4 | **direct / manufacturer primary** |
| 101-K | Latent sector errors can remain undetected until sector access and were measured at scale in production drives. | historical/scholarly context | Bairavasundaram et al., SIGMETRICS 2007 | **strong independent context** |
| 101-L | `physical sector presence ≠ readability qualification` and `defect discovery ≠ completed repair` are analytical relations supported by the above source separation. | engineering reconstruction | synthesis across 101-B/D/E + Case 14 | **bounded reconstruction** |
| 101-M | BMS is functionally comparable to ZFS/HDFS proactive verification but is not thereby the same mechanism or a proven ancestor. | functional analogy | Cases 18/83 + source boundary | **bounded analogy** |

---

## Source 1 — T10 `04-198r5`, Background Medium Scan

**Document:** T10/04-198 revision 5, Gerry Houlder, Seagate Technology, dated 9 March 2005.

**URL:** <https://www.t10.org/ftp/t10/document.04/04-198r5.pdf>

### Directly supports

The opening page says the proposal supplies a standard control/status method for BMS; several drive vendors already had proprietary controls; many systems implemented scanning in the operating system; device-side scanning could reduce host overhead and interface bandwidth. It then describes idle-period reads, logging, and customer-permitted rewrite/relocation.

The proposed model states that medium scanning identifies blocks that are difficult to read or unreadable, logs read problems, and may take vendor-specific action to restore readability. It distinguishes recoverable read errors governed by `ARRE` from unreadable blocks that may be marked bad and later relocated on write under `AWRE`.

The result-log description exposes scan status/count/progress plus suspect block locations and a `REASSIGN STATUS` field that says whether the device handled the defect or host action may remain.

The pre-scan text separately describes power-on coverage and write-and-verify for a write into an as-yet-unscanned region.

### Does not support

- invention of background disk scanning;
- an origin date for disk scrubbing generally;
- a claim that every SCSI device implements BMS;
- a complete physical defect model;
- a claim that all recovered errors are relocated;
- secure erasure of replaced sectors.

The document itself blocks the first two overclaims by naming existing proprietary/vendor and OS implementations.

---

## Source 2 — T10 Plenary Meeting #66, `05-097r0`

**Document:** Ralph Weber / John Lohmeyer, Minutes of T10 Plenary Meeting #66, meeting 10 March 2005; minutes dated 14 March 2005.

**URL:** <https://www.t10.org/ftp/t10/document.05/05-097r0.htm>

### Directly supports

Section 10.5 records that Gerry Houlder reviewed `04-198r5 (Background Media Scan)` as recommended for SPC-4 and SBC-3, moved its approval for inclusion, and that the motion passed `20:0:13:13=46`.

This is evidence for **committee disposition**, not invention or universal implementation.

---

## Source 3 — T10 `05-340r3`, SBC-3 SPC-4 Background scan additions

**Document:** Rob Elliott, HP, 18 January 2006.

**URL:** <https://www.t10.org/ftp/t10/document.05/05-340r3.pdf>

### Directly supports

The revision history identifies r0 on 9 September 2005 and r3 on 18 January 2006. The overview calls the work changes and clarifications to background scanning recently added to SBC-3.

Important bounded corrections include:

- warning language changed from `SCAN FAILED` to `BACKGROUND SCAN DETECTED MEDIUM ERROR` because the old wording falsely suggested the maintenance operation itself failed;
- proposal of a minimum idle interval before maintenance resumes;
- a bound on how long the device should keep foreground work waiting while it stops scanning/reallocation activity;
- permission for device-chosen scan order, including physical-layout-oriented order rather than mandatory LBA order;
- clearer log-full/suspend behavior;
- continued separation of recoverable reads/`ARRE`, unreadable blocks, and write-time `AWRE` relocation.

### Why it matters

This source prevents two accidental frozen-spec readings of `04-198r5`: that whole-medium coverage necessarily means one LBA-linear physical sweep, and that a warning about a discovered medium error means the scan mechanism itself failed.

---

## Source 4 — T10 2005 document register

**URL:** <https://www.t10.org/doc05.htm>

The register independently anchors:

- `05-096r0` as March 8–9 CAP Working Group minutes;
- `05-097r0` as March 10 plenary minutes;
- `05-313r0` as a change to BMS;
- `05-340r0` through `r3` as the background-scan-additions proposal family.

Use this as chronology/document-control evidence, not as a substitute for the contents of the proposals themselves.

---

## Source 5 — Seagate Cheetah 15K.5 FC Product Manual, Rev. C

**Document:** Seagate Publication 100384772, Rev. C, February 2007.

**URL:** <https://www.seagate.com/staticfiles/support/disc/manuals/fc/100384772c.pdf>

### Directly supports

Section 7.4 describes BMS as a self-initiated media scan and points to T10 SPC-4 work. It says the drive reads across the medium while idle; notes use on RAID hot spares before host service; describes BMS Log Page use for suspect locations; and says unreadable/recovered-error sites are logged or reallocated according to `ARRE/AWRE` settings.

Nearby product text distinguishes factory `P-list` defects from post-shipment `G-list` grown defects.

### Boundary

This is one named Seagate product family. It is not evidence for every SCSI drive, every firmware revision, or the origin of BMS.

---

## Source 6 — Bairavasundaram et al., SIGMETRICS 2007

**Citation:** Lakshmi N. Bairavasundaram, Garth R. Goodson, Shankar Pasupathy, Jiri Schindler, “An Analysis of Latent Sector Errors in Disk Drives,” SIGMETRICS 2007, pp. 289–300, DOI `10.1145/1254882.1254917`.

**Institutional abstract:** <https://research.cs.wisc.edu/adsl/Publications/latent-sigmetrics07.html>

### Directly supports

The study analyzes 32 months of production data across 1.53 million nearline and enterprise disks and describes latent sector errors as errors that go undetected until the corresponding sector is accessed.

### Boundary

The study supplies **field context for the latent-discovery problem**, not evidence that T10 BMS was used on those drives, not a product validation of Cheetah BMS, and not proof that one scanning policy is optimal.

---

## Cross-case evidence boundary

### Case 14 — reassignment

Case 14's Seagate/SCSI evidence is deliberately reused rather than rewritten. It establishes that `REASSIGN BLOCKS` changes the physical medium serving the same LBA and that the command does not itself preserve the affected old payload. Case 101 only supplies an upstream discovery/logging path.

### Case 18 — ZFS scrub

Use only as functional comparison. ZFS checksum/redundancy semantics are a higher-layer integrity relation; device readability is not equivalent to end-to-end filesystem correctness.

### Case 55 — NVMe health telemetry

Use only to separate active verification coverage from health/endurance/spare telemetry.

### Case 83 / Synthesis 08 — distributed integrity maintenance

Use only as cross-layer functional comparison: proactive read/check before demand can occur at device, filesystem, or distributed-replica layers without implying identical algorithms or historical descent.

---

## Evidence classification

### Historical record (`H`)

Safe to state:

- T10 `04-198r5` is dated 9 March 2005 and proposes standard BMS control/status semantics;
- the proposal itself acknowledges earlier proprietary drive methods and host/OS scanning;
- the 10 March 2005 plenary approved `04-198r5` for inclusion in SPC-4/SBC-3;
- the proposal separates recoverable/unreadable conditions and ARRE/AWRE permissions;
- it exposes scan status/progress and defect/result logging;
- 2006 T10 work clarifies warning semantics, foreground preemption, and non-LBA-order scan freedom;
- a February 2007 Cheetah 15K.5 FC manual documents BMS as a product feature;
- SIGMETRICS 2007 measured latent sector errors at scale.

### Engineering reconstruction (`E`)

Safe only as project analysis:

- `physical presence ≠ readability qualification`;
- `coverage progress ≠ permanent integrity certificate`;
- `defect discovery ≠ completed repair`;
- `repair permission ≠ repair completion`;
- `maintenance detection time ≠ defect creation time`;
- `device-local readability ≠ higher-layer checksum integrity`.

### Functional analogy (`F`)

Allowed with labels:

- BMS, ZFS scrub, HDFS BlockScanner, GFS idle checking, and RAID patrol read can all be compared as proactive verification functions;
- this does not establish common implementation, semantics, or genealogy.

### Philosophical interpretation (`P`)

Bounded inference only:

- proactive scan work can preserve or withdraw the system's justified confidence in a material embodiment before ordinary demand tests it;
- this does not imply that observation itself physically causes persistence or that all storage requires scanning.

---

## Claims explicitly not established

Do **not** use this evidence record to claim:

- T10, Seagate, or Gerry Houlder invented disk scrubbing;
- `Background Medium Scan` and vendor `Patrol Read` are historically synonymous;
- a BMS pass proves every block will remain readable later;
- a logged error has already been repaired;
- ARRE/AWRE guarantee successful relocation or spare availability;
- BMS verifies filesystem checksums, application semantics, parity consistency, or replica currentness;
- Seagate's BMS implementation represents all SCSI products;
- clearing BMS logs erases the underlying sector or any forensic trace.

---

## Related-repository check

A repository search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `patrol read` and `background medium scan` found no dedicated overlapping case in the current search surface. The broader disk/controller engineering genealogy therefore remains an appropriate future companion-repository task rather than something Case 101 should invent from functional similarity.

---

## Result

**Grounded.**

The primary record is strong enough to establish the bounded historical mechanism, its standardization boundary, and a named-product witness. The evidence also supports a precise retention decomposition: proactive readability discovery can precede application demand; discovery, logging, repair permission, reassignment, and payload preservation are different events; and scan coverage is time-bounded maintenance evidence rather than a permanent integrity property.
