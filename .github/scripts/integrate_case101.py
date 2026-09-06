from pathlib import Path

CASE_PATH = Path('cases/101-scsi-background-medium-scan-proactive-defect-discovery.md')
EVIDENCE_PATH = Path('evidence/101-t10-2004-2007-background-medium-scan-grounding.md')
ROADMAP_PATH = Path('ROADMAP.md')
INDEX_PATH = Path('CASE_INDEX.md')

case_text = r'''# SCSI Background Medium Scan: Proactive Readability Verification, Defect Logging, and Conditional Reassignment

## Scope

- **Object / system:** T10 SCSI Background Medium Scan (BMS) and related Background Pre-Scan controls, bounded from the archived 2004 proposal family through the March 2005 T10 approval, January 2006 clarification work, and a February 2007 Seagate Cheetah 15K.5 FC product witness.
- **Retention question:** what work is required when a disk sector may still physically exist and remain addressable, yet its future readability has become uncertain before any application happens to request it?
- **Status:** `grounded`.

This is **not** a general history of disk scrubbing, SCSI VERIFY, SMART, RAID-controller patrol read, RAID consistency checking, bad-sector remapping, filesystem scrubbing, or secure erasure. Case 14 already grounds SCSI defect reassignment and logical-block continuity across physical replacement. Case 101 follows an upstream question:

> **How can a storage device proactively discover that a still-present block has become difficult or impossible to read, retain evidence of that discovery, and condition later repair without confusing detection with repair?**

The project terms `readability qualification`, `coverage age`, `repair admissibility`, and `maintenance evidence` below are **engineering reconstructions**, not T10 or Seagate historical vocabulary.

---

## Historical vocabulary

The inspected T10 and Seagate sources directly use terms including:

- `Background Medium Scan` / `BMS`;
- `Background Pre-Scan` / `pre-scan`;
- `Background Control mode page`;
- `Background Scan Results log page`;
- `EN_BMS`;
- `EN_PS`;
- `BMS interval` / `Background Medium Scan Interval Time`;
- `Minimum Idle Time Before Background Scan`;
- `Maximum Time To Suspend Background Scan`;
- `ARRE` / `Automatic Read Reallocation Enabled`;
- `AWRE` / `Automatic Write Reallocation Enabled`;
- `REASSIGN STATUS`;
- `recovered error`;
- `unreadable` / `medium error`;
- `P-list` / `G-list` in the Seagate product manual.

Do not silently normalize these into later vendor-specific `patrol read`, filesystem `scrub`, or distributed `scanner` vocabulary. Those terms can be compared functionally but do not establish one lineage.

---

## Historical record

### H/P — T10 standardized an already-existing function rather than claiming to invent background scanning

T10 document `04-198r5`, dated 9 March 2005 and submitted by Gerry Houlder of Seagate, opens by proposing a **standard method to control and retrieve status from background medium scan operations**. The proposal explicitly says that several drive vendors, including Seagate, already had proprietary methods and that customers had requested a standard method. It also says many systems performed background medium scanning in the operating system.

That statement is an important prior-art guardrail. The defensible historical claim is not `T10 invented disk scrubbing in 2005`. It is narrower:

> **By March 2005 T10 was standardizing a device-side control/status interface for a function that the proposal itself says already existed in proprietary drives and host software.**

The T10 plenary minutes for 10 March 2005 record that `04-198r5` had been recommended for SPC-4 and SBC-3 and that the motion to approve it for inclusion passed `20:0:13:13=46`.

### H/P — device-side BMS relocates maintenance work without consuming ordinary SCSI-interface bandwidth

`04-198r5` describes ordinary background medium scanning as the device server reading logical blocks from the medium to:

1. identify blocks that are difficult to read or unreadable;
2. log read problems; and
3. when permitted, take vendor-specific action to make a block readable again.

The same text defines background scanning so that it does not use SCSI-interface bandwidth and says blocks read by the scan are not to be retained in cache afterward. The proposal's introduction contrasts this with host/OS-driven scanning and says moving the scan into the drive reduces system overhead and otherwise unproductive interface traffic.

This is a change in **maintenance locus and interface traffic**, not a change in the physical fact that the medium must still be read.

### H/P — readability difficulty, unrecoverability, and repair permission are separate states

The 2005 proposal distinguishes a block that can be read only after extra actions such as retries or correction from a block that is unreadable.

For a recoverable read error, the device may use vendor-specific recovery, but automatic repair or relocation is controlled by `ARRE`. For an unreadable block, the device may mark the block bad so that it can later be relocated; `AWRE` separately controls relocation during a future write. If AWRE permits it, a block previously noted as unrecoverable can be reassigned at the start of the next write to that LBA.

Therefore the historical interface itself blocks several shortcuts:

```text
read difficulty
    !=
unrecoverable read
    !=
automatic relocation permission
    !=
completed reassignment
```

Case 14 remains the canonical repository case for what SCSI reassignment does to the physical medium behind an LBA and why reassignment alone does not necessarily preserve the old payload.

### H/P — scan state and defect evidence are exposed separately from the payload

`04-198r5` adds a Background Scan Results log page. It exposes whether background pre-scan or BMS is active or suspended, scan count, scan progress, suspected-bad-block location information, and a `REASSIGN STATUS` field indicating whether the device handled a defect or the application client may still need to act, for example by reassigning or rewriting an LBA.

After the application has interpreted the entries and completed any required action, it may clear the entries using `LOG SELECT` with the specified control bit.

Thus a scan can produce retained **maintenance evidence** that is neither the user payload nor the repair itself.

> **logged defect evidence ≠ completed remediation.**

Clearing that log is likewise not evidence of secure media erasure.

### H/P — pre-scan is a distinct power-on coverage regime, not merely another periodic BMS pass

The 2005 proposal defines a related Background Pre-Scan option that starts after power-on. If the host writes to a region not yet covered by pre-scan, the device converts that write into write-and-verify; a write to an already scanned region proceeds normally.

The proposal also notes the performance cost of this behavior before the first scan completes. Pre-scan therefore links **coverage state** to temporary write semantics.

This is distinct from ordinary periodic BMS:

> **power-on pre-scan coverage ≠ recurring idle BMS coverage.**

and:

> **write-and-verify while coverage is incomplete ≠ the ordinary write path after that region has already been covered.**

### H/P — January 2006 clarification separates “medium error detected” from “scan failed”

T10 `05-340r3`, dated 18 January 2006, describes itself as changes and clarifications to the background scan operation recently added to SBC-3. One explicit correction is terminological: warnings that had been read as `PRE-SCAN FAILED` or `SCAN FAILED` were renamed to say the scan **detected a medium error**.

This is unusually useful historical negative evidence. A successful maintenance operation may terminate with evidence that the medium contains a problem.

> **maintenance detected a fault ≠ maintenance operation itself failed.**

The same proposal adds clearer foreground-preemption constraints, including minimum idle time before scanning and a maximum time to suspend background scanning when new commands arrive.

### H/P — logical coverage does not require one fixed LBA-linear physical traversal

The March 2005 text described BMS starting at LBA zero and ending at the last LBA. The January 2006 clarification explicitly calls that implication too restrictive and says the device server should be allowed to scan logical blocks in any order, for example according to physical block layout rather than logical block layout.

This prevents a false engineering inference from the earlier proposal text:

> **whole-medium logical coverage ≠ one mandatory LBA-order physical traversal.**

The retained scan/control relation can specify that coverage is due and report progress without exposing the complete internal physical scheduling algorithm.

### H/P — a 2007 Seagate product manual documents BMS as shipped drive behavior

Seagate's **Cheetah 15K.5 FC Product Manual, Rev. C**, February 2007, describes `Background Media Scan` as a self-initiated scan defined in the T10 SPC-4 work. The manual says the drive performs reads across the medium while idle, can use BMS on RAID hot spares before they enter service, exposes a BMS log so a host can avoid suspect locations, and logs or reallocates unreadable/recovered-error sites according to `ARRE/AWRE` settings.

The same product manual separately describes factory defects in a `P-list` and post-shipment grown defects in a `G-list`.

This is a **named-product implementation witness**. It does not license the claim that every SCSI drive implemented BMS, that Seagate invented the function, or that all hardware RAID patrol-read implementations are the same mechanism.

### H/S — latent sector errors make proactive discovery a real field reliability problem

Bairavasundaram et al., SIGMETRICS 2007, analyze production data over 32 months across 1.53 million nearline and enterprise disks and define latent sector errors as errors that remain undetected until the corresponding sectors are accessed.

This independent study is useful context for why proactive reading can matter. It is **not** evidence that the T10 BMS proposal caused, implemented, or uniquely solved the observed field behavior, and it is not used as an origin claim for scrubbing.

---

## Retained state and maintenance relations

The bounded case contains at least five distinct state classes.

### 1. User payload on the medium

The magnetic sector state is the object whose future readability matters.

### 2. Logical designation

The scan and logs can name suspect locations by logical block address even if later defect management changes the physical sector embodying that LBA. Case 14 owns that replacement relation.

### 3. Scan-control and schedule state

Enable bits, interval, idle-time policy, pre-scan controls, suspend/resume state, and progress govern when proactive reads occur.

This state is not user payload.

### 4. Readability / defect evidence

Recovered errors, unreadable blocks, suspected-bad-block entries, and reassignment status record what a scan learned and whether additional action may be required.

This is neither a complete failure history nor a permanent integrity certificate.

### 5. Repair authority and spare resources

`ARRE/AWRE` determine whether certain automatic relocation paths are permitted. The actual availability of replacement capacity, the ability to recover the old payload, and successful completion of reassignment remain distinct from those permission bits.

---

## Trigger and timing structure

BMS makes several clocks visible:

1. time since the prior scan cycle;
2. idle time before a background pass may resume;
3. foreground-command latency allowed before maintenance suspends;
4. time since a sector last happened to be read by ordinary workload;
5. physical defect creation time, which may be unknown;
6. defect discovery time during a scan or foreground access;
7. delay between discovery and any repair/reassignment;
8. power-on pre-scan coverage progress.

These times must not be collapsed.

A medium error discovered at time `t2` may have been created at some unknown earlier `t1`. A successful scan at `t0` is evidence about the blocks exercised then, not a guarantee about `t3`.

> **scan completion ≠ timeless readability certificate.**

---

## Failure and forgetting boundaries

Keep these separate:

- sector remains physically present but becomes harder to read;
- a recovered error is observed;
- a sector becomes unreadable;
- BMS is disabled, delayed, or repeatedly preempted;
- scan-result logging fills or is unavailable;
- a defect is logged but automatic repair is not permitted;
- repair is permitted but no successful relocation occurs;
- reassignment occurs but the old payload could not be recovered;
- a logical block is remapped while the old physical sector remains on the medium;
- a log entry is cleared after handling;
- secure sanitization of old media embodiments.

Calling all of these `disk failure` would lose the relation under study.

---

## Cross-case comparison

### Case 14 — SCSI defect reassignment

Case 101 is upstream of Case 14 in one possible maintenance path:

```text
proactive read
    -> difficult/unreadable evidence
    -> logged / qualified defect
    -> optional repair or later write-time relocation
    -> reassignment / replacement embodiment
```

This diagram is an **engineering reconstruction**, not a claim that every drive follows one universal sequence. Case 14 directly proves that reassignment can change the physical medium behind the same LBA and that the reassignment command itself does not guarantee preservation of the affected old data.

Therefore:

> **defect discovery ≠ reassignment ≠ payload preservation.**

### Case 18 — ZFS scrub

Both BMS and ZFS scrub proactively read state before ordinary demand exposes a fault, but they qualify different relations.

- BMS is device-local medium readability/recovery work under a SCSI drive interface.
- ZFS scrub is filesystem/pool-level checksum and redundancy verification with end-to-end block identity and repair semantics.

A disk sector can be readable while the filesystem block is semantically/checksum wrong; a filesystem checksum can also identify bad content without explaining the physical-sector defect mechanism.

> **medium readability qualification ≠ higher-layer checksum integrity qualification.**

The comparison is functional, not genealogical.

### Case 55 — NVMe health telemetry

Case 55 exposes counters, warnings, spare margin, and endurance estimates. BMS performs active coverage reads and records concrete scan findings.

> **health telemetry ≠ proactive verification coverage.**

A warning/counter may indicate risk without proving which particular block is unreadable; a scan can find a bad block without supplying a complete life/endurance model.

### Case 83 / Synthesis 08 — HDFS and distributed integrity maintenance

HDFS BlockScanner and GFS idle checking show proactive integrity discovery at the distributed replica layer. BMS shows a device-local predecessor/contemporary function at a lower storage layer.

The shared functional pattern is `background verification before demand`. It does not establish a T10→HDFS/GFS genealogy, identical integrity semantics, or identical repair authority.

---

## Prior-art and terminology boundary

This case makes **no invention-priority claim** for:

- background disk scanning;
- disk scrubbing;
- host-initiated SCSI VERIFY sweeps;
- bad-sector remapping;
- RAID patrol read;
- filesystem scrub;
- distributed checksum scanning.

`04-198r5` itself says proprietary drive methods and operating-system scanning already existed. The March 2005 plenary evidence establishes a standards-inclusion decision, not invention. The 2007 Seagate manual establishes one product witness, not universal adoption.

The broader ROADMAP phrase `controller patrol-read history` therefore remains partly open. This case closes only a bounded **device-side SCSI Background Medium Scan** slice. A full history would need named RAID controllers, period LSI/ServeRAID/other manuals, SCSI VERIFY-based host/controller implementations, parity consistency checks, and evidence about how `patrol read` terminology moved across vendors.

A fresh repository search found no dedicated `patrol read` / `background medium scan` history in `tmzncty/computing-archaeology`. If that broader engineering genealogy is built later, it should live there and Case 101 should remain the retention-specific BMS boundary.

---

## Engineering reconstruction

Case 101 adds these controlled relations:

1. `physical sector presence ≠ readability qualification`;
2. `background scan access ≠ application demand read`;
3. `scan discovery time ≠ defect creation time`;
4. `recoverable read difficulty ≠ unrecoverable medium error`;
5. `defect detection ≠ completed repair/reallocation`;
6. `ARRE repair permission ≠ AWRE write-time reallocation permission`;
7. `suspected-bad-block log entry ≠ device-completed remediation`;
8. `scan progress/count ≠ permanent integrity certificate`;
9. `background maintenance suspension ≠ maintenance abandonment`;
10. `power-on pre-scan ≠ periodic BMS`;
11. `pre-scan write-and-verify ≠ ordinary post-coverage write semantics`;
12. `logical coverage ≠ fixed LBA-order physical traversal`;
13. `device-local readability verification ≠ filesystem/distributed checksum integrity`;
14. `BMS standardization ≠ invention of background scanning or proof of a patrol-read genealogy`.

These are project analytical statements. They are not assertions that T10 participants used this ontology.

---

## Philosophical interpretation — bounded

Case 101 strengthens a narrow theme already visible in Synthesis 08: some retention work is **epistemic maintenance**. A physical embodiment can remain present while the system's justified confidence in its future readability decays because no recent operation has exercised it. A background scan creates new evidence by deliberately reading before application demand forces the question.

The stronger universal claim must be rejected. Storage does not become persistent merely because it is repeatedly observed, and not every medium needs proactive reading to remain physically stable. Here the scan does not cause magnetic retention in the ordinary sense; it changes what the system knows about the embodiment and can trigger later repair before redundancy or recoverability margin is lost.

---

## Evidence limits / future work

Still open:

- full archival reconstruction of `04-198r0` through `r4` and every CAP change;
- exact final SBC-3/SPC-4 publication wording and later revision genealogy;
- host-initiated SCSI VERIFY scrub history before device-side BMS;
- named hardware RAID-controller `Patrol Read` genealogy and vendor terminology;
- distinction between patrol read and parity `Consistency Check` across products;
- field fault injection on BMS-capable drives;
- quantitative BMS scheduling, bandwidth, and detection-latency behavior in deployed arrays;
- interaction with drive-internal ECC, SMART predictive attributes, and error-recovery firmware;
- correlated/multi-sector defects and URE-aware RAID rebuild policy;
- lower-layer forensic persistence after reassignment or logical retirement.

These limits do not block the bounded result.

---

## Related repositories

### `tmzncty/computing-archaeology`

Repository search found no dedicated SCSI BMS / patrol-read case at the time of this slice. Case 101 therefore keeps only the retention-specific historical boundary and relation decomposition. A broader history of host scrubbing, SCSI VERIFY, drive firmware, RAID patrol read, and consistency checking should be developed there and linked back rather than duplicated here.

### `tmzncty/problem-history`

Useful anti-anachronism guardrail: `readability qualification`, `coverage age`, and `maintenance evidence` are project reconstructions. Historical actors in the bounded sources spoke of medium scan, pre-scan, recovered/unreadable errors, ARRE/AWRE, log pages, and reassignment status.

---

## Sources

### Primary / contemporary

- T10, Gerry Houlder (Seagate), **`04-198r5 — Background Medium Scan`**, 9 March 2005: <https://www.t10.org/ftp/t10/document.04/04-198r5.pdf>
- T10, Weber & Lohmeyer, **Minutes of T10 Plenary Meeting #66 — March 10, 2005**, `05-097r0`, especially §10.5 recording approval of `04-198r5`: <https://www.t10.org/ftp/t10/document.05/05-097r0.htm>
- T10, Rob Elliott (HP), **`05-340r3 — SBC-3 SPC-4 Background scan additions`**, 18 January 2006: <https://www.t10.org/ftp/t10/document.05/05-340r3.pdf>
- T10, **2005 document register**, identifying CAP minutes `05-096r0`, plenary minutes `05-097r0`, and the `05-340` proposal family: <https://www.t10.org/doc05.htm>
- Seagate, **_Cheetah 15K.5 FC Product Manual_, Publication 100384772 Rev. C**, February 2007, §7.4 `Background Media Scan`: <https://www.seagate.com/staticfiles/support/disc/manuals/fc/100384772c.pdf>

### Independent scholarly context

- Lakshmi N. Bairavasundaram, Garth R. Goodson, Shankar Pasupathy, Jiri Schindler, **“An Analysis of Latent Sector Errors in Disk Drives,”** SIGMETRICS 2007, pp. 289–300, DOI `10.1145/1254882.1254917`: <https://research.cs.wisc.edu/adsl/Publications/latent-sigmetrics07.html>

### Internal comparisons

- [`cases/14-scsi-disk-defect-reassignment-logical-identity.md`](14-scsi-disk-defect-reassignment-logical-identity.md)
- [`cases/18-zfs-scrub-latent-error-detection.md`](18-zfs-scrub-latent-error-detection.md)
- [`cases/55-nvme-smart-health-endurance-telemetry.md`](55-nvme-smart-health-endurance-telemetry.md)
- [`cases/83-apache-hdfs-block-scanner-checksum-verification.md`](83-apache-hdfs-block-scanner-checksum-verification.md)
- [`docs/SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md`](../docs/SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md)

---

## Status

**Grounded bounded case.**

The core mechanism and historical boundary are supported by T10 proposal/committee records plus a named Seagate product manual; the SIGMETRICS field study is used only as independent latent-error context. The case closes a device-side SCSI BMS relation slice without claiming invention of scrubbing, complete patrol-read history, or equivalence with higher-layer integrity verification.
'''

evidence_text = r'''# Evidence Record 101 — T10 2004–2007 Background Medium Scan Grounding

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
'''

if CASE_PATH.exists() or EVIDENCE_PATH.exists():
    raise SystemExit('Case/evidence 101 path already exists; refusing to overwrite')
CASE_PATH.write_text(case_text, encoding='utf-8')
EVIDENCE_PATH.write_text(evidence_text, encoding='utf-8')

roadmap = ROADMAP_PATH.read_text(encoding='utf-8')
if 'cases/101-scsi-background-medium-scan-proactive-defect-discovery.md' in roadmap:
    raise SystemExit('ROADMAP already contains Case 101')
lines = roadmap.splitlines()
needle = '- [x] Proactive-integrity / defect-discovery / repair-margin synthesis —'
idxs = [i for i, line in enumerate(lines) if line.startswith(needle)]
if len(idxs) != 1:
    raise SystemExit(f'Expected exactly one proactive-integrity roadmap line, got {len(idxs)}')
i = idxs[0]
old = lines[i]
old = old.replace('controller patrol-read history, adversarial integrity, correlated failures, cross-node scan coordination, and field fault injection remain open.', 'the broader RAID-controller patrol-read genealogy beyond Case 101, adversarial integrity, correlated failures, cross-node scan coordination, and field fault injection remain open.')
lines[i] = old
case_bullet = '- [x] SCSI Background Medium Scan / proactive medium-readability boundary — [`cases/101-scsi-background-medium-scan-proactive-defect-discovery.md`](cases/101-scsi-background-medium-scan-proactive-defect-discovery.md), grounded by [`evidence/101-t10-2004-2007-background-medium-scan-grounding.md`](evidence/101-t10-2004-2007-background-medium-scan-grounding.md), uses T10 `04-198r5`, the March 2005 plenary approval record, January 2006 clarification work, and a February 2007 Seagate Cheetah 15K.5 FC manual to separate proactive readability discovery, recovered versus unreadable conditions, ARRE/AWRE repair permission, result logging/progress, power-on pre-scan, and later reassignment. This closes a bounded device-side SCSI BMS slice of the broader patrol-read frontier without claiming invention of disk scrubbing or a BMS→RAID-controller genealogy; host SCSI VERIFY history, named RAID-controller Patrol Read/Consistency Check genealogy, field fault injection, and URE-aware policy remain open and should be coordinated with `computing-archaeology`.'
lines.insert(i + 1, case_bullet)
ROADMAP_PATH.write_text('\n'.join(lines) + '\n', encoding='utf-8')

index = INDEX_PATH.read_text(encoding='utf-8')
if '## Case 101 — SCSI Background Medium Scan findings' in index:
    raise SystemExit('CASE_INDEX already contains Case 101')
stripped = index.rstrip('\n')
last = stripped.splitlines()[-1]
if not last.startswith('1504. **distributed replica-integrity lifecycle synthesis'):
    raise SystemExit(f'Unexpected CASE_INDEX tail: {last[:120]}')
findings = r'''

## Case 101 — SCSI Background Medium Scan findings

1505. **physical sector presence ≠ readability qualification** — a logical/physical block can remain present while a later proactive read discovers that the embodiment is difficult or impossible to read;
1506. **background scan access ≠ application demand read** — BMS deliberately exercises medium state during maintenance/idle time so latent readability problems can be found before ordinary workload happens to touch the block;
1507. **scan discovery time ≠ defect creation time** — the scan dates the observation of a problem, not necessarily the earlier physical event that produced it;
1508. **recoverable read difficulty ≠ unrecoverable medium error** — T10 separates blocks that require retries/correction from blocks that cannot be read, so one generic `bad sector` state is too coarse;
1509. **defect detection ≠ completed repair/reallocation** — identifying or logging a problematic block can create a repair obligation without establishing that a replacement embodiment now exists;
1510. **ARRE repair permission ≠ AWRE write-time reallocation permission** — the T10 model exposes different controls for automatic action on recoverable read errors and relocation during later writes;
1511. **suspected-bad-block log entry ≠ device-completed remediation** — `REASSIGN STATUS` exists precisely because a logged result can still require host/application action;
1512. **scan progress/count ≠ permanent integrity certificate** — coverage state reports maintenance work performed or in progress, not timeless future readability of every sector;
1513. **background maintenance suspension ≠ maintenance abandonment** — foreground commands can suspend BMS and later allow it to resume, so service priority and eventual coverage are separate scheduling relations;
1514. **power-on pre-scan ≠ periodic BMS** — pre-scan is a distinct startup coverage regime with its own enable/timeout and interaction with writes;
1515. **pre-scan write-and-verify ≠ ordinary post-coverage write semantics** — a write to an unscanned region may carry an extra verification obligation that disappears once that region has been covered;
1516. **whole-medium logical coverage ≠ fixed LBA-order physical traversal** — 2006 T10 clarification explicitly permits device-chosen scan order, including physical-layout-oriented scheduling;
1517. **device-local readability verification ≠ filesystem/distributed checksum integrity** — BMS, ZFS scrub, and HDFS/GFS background checking share a proactive-verification function but qualify different layers and failure relations;
1518. **BMS standardization ≠ invention of background scanning or proof of a patrol-read genealogy** — `04-198r5` itself acknowledges earlier proprietary drive and OS methods; the bounded case establishes T10 interface standardization and one Seagate product witness, not the complete history of disk scrubbing or RAID-controller Patrol Read.
'''
INDEX_PATH.write_text(stripped + findings + '\n', encoding='utf-8')

# Lightweight structural validation before the workflow commits anything.
for p in (CASE_PATH, EVIDENCE_PATH, ROADMAP_PATH, INDEX_PATH):
    text = p.read_text(encoding='utf-8')
    if not text.endswith('\n'):
        raise SystemExit(f'{p} missing final newline')
if '1505. **physical sector presence ≠ readability qualification**' not in INDEX_PATH.read_text(encoding='utf-8'):
    raise SystemExit('Case 101 findings missing')
if case_bullet not in ROADMAP_PATH.read_text(encoding='utf-8'):
    raise SystemExit('Case 101 roadmap bullet missing')
print('case101 integration patch prepared')
