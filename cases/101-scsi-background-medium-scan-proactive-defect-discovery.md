# SCSI Background Medium Scan: Proactive Readability Verification, Defect Logging, and Conditional Reassignment

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
