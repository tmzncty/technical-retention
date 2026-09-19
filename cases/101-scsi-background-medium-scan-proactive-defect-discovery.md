# SCSI Background Medium Scan: Proactive Readability Verification, Defect Logging, and Conditional Reassignment

## Scope

- **Object / system:** T10 SCSI Background Medium Scan (BMS) and related Background Pre-Scan controls, now bounded backward by an IBM 2001-filed / 2002-published controller-level media-scanner disclosure and a Seagate December-2003 drive-side BGMS/pre-scan filing, then through the March 2005 T10 approval, January 2006 clarification work, an April 2005 Dell PERC controller-level `Patrol Read` witness, February/March 2006 generic LSI MegaRAID documentation, a February 2007 Seagate Cheetah 15K.5 FC product witness, and later bounded vendor/controller comparisons.
- **Retention question:** what work is required when a disk sector may still physically exist and remain addressable, yet its future readability has become uncertain before any application happens to request it?
- **Status:** `grounded`.

This is **not** a general history of disk scrubbing, SCSI VERIFY, SMART, RAID-controller patrol read, RAID consistency checking, bad-sector remapping, filesystem scrubbing, or secure erasure. Case 14 already grounds SCSI defect reassignment and logical-block continuity across physical replacement. Case 101 follows an upstream question:

> **How can a storage device proactively discover that a still-present block has become difficult or impossible to read, retain evidence of that discovery, and condition later repair without confusing detection with repair?**

The project terms `readability qualification`, `coverage age`, `repair admissibility`, and `maintenance evidence` below are **engineering reconstructions**, not T10, Seagate, Dell, LSI, or IBM historical vocabulary.

Bounded deepenings:

- [`../evidence/101-ibm-2001-seagate-2003-background-media-scan-prior-art-deepening.md`](../evidence/101-ibm-2001-seagate-2003-background-media-scan-prior-art-deepening.md) — direct pre-2005 primary prior-art floor: IBM controller/RAID-controller background scanner publicly disclosed by December 2002, plus a December-2003 Seagate drive-side BGMS/pre-scan design record; filing/publication/standardization and functional-similarity/genealogy boundaries are kept separate;
- [`../evidence/101-dell-2005-2006-perc-patrol-read-controller-deepening.md`](../evidence/101-dell-2005-2006-perc-patrol-read-controller-deepening.md) — Dell PERC controller-level maintenance locus, RAID-state-dependent repair, and NVRAM maintenance-state horizons;
- [`../evidence/101-lsi-dell-2003-2006-patrol-read-documentation-lineage-deepening.md`](../evidence/101-lsi-dell-2003-2006-patrol-read-documentation-lineage-deepening.md) — 2003–2006 documentation chronology, April-2005 public-floor tightening, generic LSI witness, and Dell/LSI source-lineage weighting.

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

The earlier IBM patent uses `background media surface scanner`, `predictive media failure analysis`, `proactive media defect management`, and written-region indicators. The December-2003 Seagate filing explicitly uses `background media scan (BGMS)`, `pre-scan`, `LOG SENSE`, `LOG SELECT`, and `WRITE AND VERIFY`. These terms are historical vocabulary in those particular records; similarity to later T10 vocabulary does not by itself prove textual or implementation genealogy.

The bounded Dell/LSI controller witnesses add period vendor terms including `Background Patrol Read`, `Patrol Read`, `Patrol Read Mode`, `Patrol Read Status`, `Patrol Read Control`, `Auto`, `Manual`, `Manual Halt`, `Disable`, `Consistency Check`, `SMART alerts`, and the `MegaPR` utility. Later Dell support documentation additionally exposes `PR completed Bitmap`, `Last complete Bitmap`, scheduling state, and NVRAM-held error information for the legacy implementation family.

Do not silently normalize IBM `media surface scanner`, Seagate `BGMS`, T10 `Background Medium Scan`, Dell/LSI `Patrol Read`, later vendor-specific patrol terminology, filesystem `scrub`, or distributed `scanner` vocabulary into one historical term. Those terms can be compared functionally but do not establish one lineage.

---

## Historical record

### H/P — T10 standardized an already-existing function rather than claiming to invent background scanning

T10 document `04-198r5`, dated 9 March 2005 and submitted by Gerry Houlder of Seagate, opens by proposing a **standard method to control and retrieve status from background medium scan operations**. The proposal explicitly says that several drive vendors, including Seagate, already had proprietary methods and that customers had requested a standard method. It also says many systems performed background medium scanning in the operating system.

That statement is an important prior-art guardrail. The defensible historical claim is not `T10 invented disk scrubbing in 2005`. It is narrower:

> **By March 2005 T10 was standardizing a device-side control/status interface for a function that the proposal itself says already existed in proprietary drives and host software.**

The T10 plenary minutes for 10 March 2005 record that `04-198r5` had been recommended for SPC-4 and SBC-3 and that the motion to approve it for inclusion passed `20:0:13:13=46`.

### H/P — direct earlier primary evidence now grounds that prior-art statement

IBM filed US09/872,386 on **1 June 2001**; the application was publicly published as US20020184580A1 on **5 December 2002**. It explicitly describes a background storage-media surface scanner for predictive failure analysis and proactive defect management. The scanner can execute in an internal/external controller, a RAID array controller, or a host processor; can run when workload falls below a threshold; can cover all or selected regions; can track errors/reallocations; and can reconstruct unreadable data from RAID redundancy before replacement in one embodiment.

Seagate filed US10/740,886 on **18 December 2003**. That design record explicitly describes drive-side `BGMS`, a power-up `pre-scan`, idle/interval gating, recovered/unrecovered error logging, host control, and conversion of a WRITE to WRITE AND VERIFY when its target range has not yet been pre-scanned. The application was not publicly published until **25 August 2005**, so the filing proves a pre-standardization Seagate design record, not public availability of that patent text in 2003.

The bounded prior-art relation is therefore:

```text
pre-existing host/controller/drive proactive-scan mechanisms
    !=
March 2005 T10 interoperable control/status standardization
```

and:

```text
functional similarity
    !=
demonstrated patent -> standard genealogy
```

Detailed record: [`../evidence/101-ibm-2001-seagate-2003-background-media-scan-prior-art-deepening.md`](../evidence/101-ibm-2001-seagate-2003-background-media-scan-prior-art-deepening.md).

### H/P — maintenance locus was already plural before T10 BMS

The IBM disclosure explicitly permits controller/RAID-controller/host-side scanning, while the 2003 Seagate filing describes self-initiated drive-side BGMS. These are direct early counterexamples to the assumption that `background media scanning` names one fixed system locus.

```text
host / software maintenance
    != controller / RAID-controller maintenance
    != drive-internal maintenance
```

The shared function does not imply identical traffic, redundancy knowledge, repair authority, state persistence, or scheduling.

### H/P — early records already separate traversal progress, maintenance metadata, and repair

IBM describes written-region indicators, scan selection, error/reallocation tracking, and optional RAID reconstruction; Seagate separately exposes current scan progress plus finite error-log state through `LOG SENSE` / `LOG SELECT`.

Thus before the 2005 T10 interface, primary records already support:

```text
user payload
    != coverage / traversal state
    != maintenance metadata / error evidence
    != repair authority
    != repair completion
```

Seagate's finite log may wrap, so retained maintenance evidence is not automatically a complete lifetime history. Clearing that log is not physical sanitization.

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

The December-2003 Seagate filing is now an earlier design witness for the same broad `pre-scan coverage -> conditional WRITE AND VERIFY` function, but it is not treated as proof of one-to-one T10 clause descent.

### H/P — January 2006 clarification separates “medium error detected” from “scan failed”

T10 `05-340r3`, dated 18 January 2006, describes itself as changes and clarifications to the background scan operation recently added to SBC-3. One explicit correction is terminological: warnings that had been read as `PRE-SCAN FAILED` or `SCAN FAILED` were renamed to say the scan **detected a medium error**.

This is unusually useful historical negative evidence. A successful maintenance operation may terminate with evidence that the medium contains a problem.

> **maintenance detected a fault ≠ maintenance operation itself failed.**

The same proposal adds clearer foreground-preemption constraints, including minimum idle time before scanning and a maximum time to suspend background scanning when new commands arrive.

### H/P — logical coverage does not require one fixed LBA-linear physical traversal

The March 2005 text described BMS starting at LBA zero and ending at the last LBA. The January 2006 clarification explicitly calls that implication too restrictive and says the device server should be allowed to scan logical blocks in any order, for example according to physical block layout rather than logical block layout.

This prevents a false engineering inference from the earlier proposal text:

> **whole-medium logical coverage ≠ one mandatory LBA-order physical traversal.**

The earlier IBM disclosure independently allowed all-sector, selected-region, skipped-region, and differential-frequency scanning. That is a functional earlier counterexample to a universal fixed-traversal assumption, not proof of direct influence on the 2006 wording.

### H/P* — Dell PERC supplies a named controller-level `Patrol Read` witness by April 2005

A surviving copy of Dell's **PowerEdge Expandable RAID Controller 4/Di/Si and 4e/Di/Si User's Guide**, released **April 2005**, exposes `Patrol Read Mode`, `Patrol Read Status`, and `Patrol Read Control`, with `Manual`, `Auto`, `Manual Halt`, and `Disabled` modes. The same manual separately documents `Consistency Check` and identifies `MegaRAID` as an LSI Logic trademark.

Dell's still-live record for **MegaPR for Linux v.1.03, A02**, released **7 June 2005**, then says the utility can start, stop, and display the status of `Patrol Read` on specified PERC 3, PERC 4, and PERC 4e controllers. The page labels the package `Initial Release of MegaPR for Linux`, but also requires a minimum supporting controller firmware level and pre-existing Auto/Manual Patrol Read mode.

Therefore:

```text
April 2005 named-controller Patrol Read documentation
    !=
7 June 2005 initial Linux utility release
    !=
first firmware implementation
```

The April manual is a surviving mirror rather than a current Dell-hosted artifact, so the tightened date is a strong bounded documentation witness, not an invention/firmware-origin claim.

The IBM 2001/2002 patent now provides an earlier generic controller/RAID-controller proactive-scan mechanism floor; it does **not** back-date the exact `Patrol Read` product terminology.

### H/P — generic LSI MegaRAID documentation exposes Patrol Read by the February/March 2006 Version 2.0 edition

LSI Logic's **MegaRAID Configuration Software User's Guide**, DB15-000269-01, Version 2.0, survives in the current Broadcom archive. Its revision table gives `Version 2.0 — February 2006`, while the title/front matter identifies the surviving Second Edition as **March 2006**. The repository therefore preserves both date signals instead of silently flattening them.

The manual contains a dedicated §2.4.7 `Patrol Read`. It describes preventive review for possible physical-drive errors, exposes Manual/Auto/Manual Halt/Disable modes, and reports completed iterations, active/stopped state, and the schedule for the next execution. Elsewhere it says Auto mode schedules a new Patrol Read within four hours after the last iteration completes.

The same manual separately defines `Consistency Check` as verification of RAID redundancy correctness for supported RAID levels. Hence, generic LSI documentation independently confirms the interface distinction:

> **Patrol Read ≠ Consistency Check.**

This closes the narrow debt `obtain period LSI/MegaRAID material independent of a Dell-authored manual`. It does **not** make Dell and LSI independent engineering lineages.

### H/P* — the inspected February 2003 LSI Version 1.0 manual documents Consistency Check but not Patrol Read

LSI's revision history identifies DB15-000269-00 as Version 1.0 / February 2003. A surviving searchable copy of that First Edition contains explicit `Check Consistency` controls and semantics but returns no full-text match for `Patrol Read`.

That negative evidence is deliberately bounded to documentation:

> **the inspected 2003 Version 1.0 manual does not expose Patrol Read**

is supported; the stronger statement

> **no MegaRAID firmware or product had an equivalent capability in 2003**

is not.

The IBM 2002 public disclosure is another reason not to infer absence of controller-level proactive scan mechanisms from this one LSI manual's terminology absence.

This also blocks a date error: the Version 2.0 manual's repeated `Copyright © 2003–2006` cannot be used to back-date its Patrol Read section to 2003.

### H/P — Dell/LSI Patrol Read evidence is lineage-related rather than two clean independent vendor witnesses

The April 2005 Dell manual identifies `MegaRAID` as an LSI Logic trademark, and Dell's official June 2005 support page titles the supported PERC family as `LSI Logic PERC3/... PERC 4/...`. LSI's own documentation describes MegaRAID controllers integrated into systems by other manufacturers.

The defensible provenance conclusion is therefore:

> **Dell PERC and LSI MegaRAID documents can corroborate Patrol Read semantics, but their corporate mastheads should not be counted mechanically as two independent implementation lineages.**

This does not prove bit-for-bit firmware identity, identical behavior across every PERC/MegaRAID model, or invention priority.

Detailed chronology/source-lineage record: [`../evidence/101-lsi-dell-2003-2006-patrol-read-documentation-lineage-deepening.md`](../evidence/101-lsi-dell-2003-2006-patrol-read-documentation-lineage-deepening.md).

### H/P — Dell's 2006 article places Patrol Read at the RAID-controller maintenance locus

A February 2006 *Dell Power Solutions* article by Drew Habas and John Sieber describes `Background Patrol Read` as a PERC feature that issues commands across configured array drives, detects media defects, and, where redundancy permits, reconstructs data from peer drives before the affected drive writes to a reassigned sector. The same article explicitly separates Background Patrol Read from parity/mirror `Consistency Check` and predictive `SMART alerts`.

This gives a controller-level maintenance locus that must not be silently collapsed into the drive-side T10 BMS relation:

```text
device-side BMS
    != controller-orchestrated PERC Patrol Read
```

Chronological proximity in 2005–2006 is not proof that one implementation descended from the other or that PERC invoked the standardized T10 BMS operation internally.

Detailed controller-state record: [`../evidence/101-dell-2005-2006-perc-patrol-read-controller-deepening.md`](../evidence/101-dell-2005-2006-perc-patrol-read-controller-deepening.md).

### H/P — a 2007 Seagate product manual documents BMS as shipped drive behavior

Seagate's **Cheetah 15K.5 FC Product Manual, Rev. C**, February 2007, describes `Background Media Scan` as a self-initiated scan defined in the T10 SPC-4 work. The manual says the drive performs reads across the medium while idle, can use BMS on RAID hot spares before they enter service, exposes a BMS log so a host can avoid suspect locations, and logs or reallocates unreadable/recovered-error sites according to `ARRE/AWRE` settings.

The same product manual separately describes factory defects in a `P-list` and post-shipment grown defects in a `G-list`.

This is a **named-product implementation witness**. It does not license the claim that every SCSI drive implemented BMS, that Seagate invented the function, or that all hardware RAID patrol-read implementations are the same mechanism.

### H/S — latent sector errors make proactive discovery a real field reliability problem

Bairavasundaram et al., SIGMETRICS 2007, analyze production data over 32 months across 1.53 million nearline and enterprise disks and define latent sector errors as errors that remain undetected until the corresponding sectors are accessed.

This independent study is useful context for why proactive reading can matter. It is **not** evidence that the T10 BMS proposal caused, implemented, or uniquely solved the observed field behavior, and it is not used as an origin claim for scrubbing.

---

## Retained state and maintenance relations

The bounded case contains at least six distinct state classes.

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

The earlier Seagate filing strengthens this boundary by showing a finite log that can wrap and be cleared separately from traversal progress. The IBM disclosure additionally shows written-region metadata that can determine which regions contain payload requiring preservation during testing.

### 5. Repair authority and spare resources

`ARRE/AWRE` determine whether certain automatic relocation paths are permitted. The actual availability of replacement capacity, the ability to recover the old payload, and successful completion of reassignment remain distinct from those permission bits.

The earlier IBM RAID-controller embodiment further shows that redundancy-assisted reconstruction can be a separate repair authority from drive-local read recovery.

### 6. Controller-level maintenance summary and recurrence state

The Dell PERC deepening adds a higher-layer variant. Later Dell support documentation for the legacy PERC family says Patrol Read data are stored in controller NVRAM for physical-drive progress/completion summaries, scheduling, and error logging. It exposes PR-completion bitmaps, a prior-completion bitmap, bitmap-clear time, next desired start time, and recovered/unrecovered error information.

The same documentation says an interrupted **Auto** Patrol Read restarts from the beginning after server reboot, while **Manual** mode does not automatically restart. Therefore:

> **persistent maintenance policy / summary / error evidence ≠ persistent exact execution checkpoint.**

The completion bitmap is also a recent per-drive summary, not a per-LBA timeless certificate.

Generic LSI Version 2.0 adds a period controller-side recurrence witness: completed-iteration count, active/stopped state, and next-execution schedule are exposed, while Auto mode schedules another pass relative to prior completion. Those fields still do not prove a per-LBA persistent verification ledger or power-loss-persistent exact frontier.

---

## Trigger and timing structure

BMS and the bounded prior-art/controller comparisons make several clocks visible:

1. time since the prior scan cycle;
2. idle time before a background pass may resume;
3. foreground-command latency allowed before maintenance suspends;
4. time since a sector last happened to be read by ordinary workload;
5. physical defect creation time, which may be unknown;
6. defect discovery time during a scan or foreground access;
7. delay between discovery and any repair/reassignment;
8. power-on pre-scan coverage progress;
9. controller-level recurrence scheduling time;
10. recent completion-summary window;
11. one interrupted pass's execution frontier;
12. patent filing time;
13. patent/public-document publication time;
14. standards approval time;
15. controller documentation / utility-release time, which is not the same clock as feature conception or firmware introduction.

These times must not be collapsed.

A medium error discovered at time `t2` may have been created at some unknown earlier `t1`. A successful scan at `t0` is evidence about the blocks exercised then, not a guarantee about `t3`.

> **scan completion ≠ timeless readability certificate.**

Likewise, a retained schedule or recent completion bitmap does not necessarily retain the exact LBA/frontier required to continue an interrupted controller scan without repeating work. A patent filing date does not by itself establish public availability or shipment, and a host utility published at one date does not date the underlying controller capability to that same day.

---

## Failure and forgetting boundaries

Keep these separate:

- sector remains physically present but becomes harder to read;
- a recovered error is observed;
- a sector becomes unreadable;
- BMS is disabled, delayed, or repeatedly preempted;
- scan-result logging fills or is unavailable;
- a finite earlier error log wraps and overwrites older maintenance evidence;
- a defect is logged but automatic repair is not permitted;
- repair is permitted but no successful relocation occurs;
- a controller detects a defect but the present RAID state cannot reconstruct the payload;
- reassignment occurs but the old payload could not be recovered;
- a logical block is remapped while the old physical sector remains on the medium;
- a log entry is cleared after handling;
- a controller retains recurring-maintenance policy but loses the exact in-flight execution frontier;
- a patent/design record exists before public publication;
- documentation survives while exact first implementation chronology is lost;
- secure sanitization of old media embodiments.

Calling all of these `disk failure` or `feature history` would lose the relation under study.

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

The IBM and Dell controller witnesses add controller-level branches in which redundancy may supply the old payload before a drive reassignment/rewrite. That yields:

> **defect discovery ≠ payload reconstructability ≠ reassignment ≠ completed payload preservation.**

### Case 18 — ZFS scrub

BMS/PERC Patrol Read and ZFS scrub proactively read state before ordinary demand exposes a fault, but they qualify different relations.

- BMS is device-local medium readability/recovery work under a SCSI drive interface.
- PERC/MegaRAID Patrol Read is controller-orchestrated media verification with RAID-aware repair context.
- ZFS scrub is filesystem/pool-level checksum and redundancy verification with end-to-end block identity and repair semantics.

A disk sector can be readable while the filesystem block is semantically/checksum wrong; a filesystem checksum can also identify bad content without explaining the physical-sector defect mechanism.

> **medium readability qualification ≠ controller redundancy qualification ≠ higher-layer checksum integrity qualification.**

The comparison is functional, not genealogical.

### Case 55 — NVMe health telemetry

Case 55 exposes counters, warnings, spare margin, and endurance estimates. BMS performs active coverage reads and records concrete scan findings. The 2006 Dell article supplies a period vendor version of the same distinction by putting SMART alerts and active Background Patrol Read into different Fault Management Suite roles.

> **health telemetry / prediction ≠ proactive verification coverage.**

A warning/counter may indicate risk without proving which particular block is unreadable; a scan can find a bad block without supplying a complete life/endurance model.

### Case 83 / Synthesis 08 — HDFS and distributed integrity maintenance

HDFS BlockScanner and GFS idle checking show proactive integrity discovery at the distributed replica layer. BMS shows a device-local function; PERC/MegaRAID Patrol Read adds a controller-level array function between that layer and a filesystem/distributed checker.

The shared functional pattern is `background verification before demand`. It does not establish an IBM/T10/PERC/MegaRAID→HDFS/GFS genealogy, identical integrity semantics, or identical repair authority.

### Case 111 — evidence/source-lineage weighting

Case 111's IBM/Lenovo documentation deepening already showed that a second corporate masthead can represent closely related operational guidance rather than a cleanly independent engineering witness. Case 101 adds a different hardware-controller example: Dell records themselves expose LSI Logic / MegaRAID provenance around the relevant PERC family.

The comparison is methodological only:

> **source multiplicity ≠ engineering-lineage multiplicity.**

It does not assert a historical relationship between IBM/Lenovo SSD guidance and Dell/LSI controller development.

### Synthesis 26 — maintenance-control-state persistence horizons

The Dell PERC evidence provides a bounded controller example in which NVRAM-held schedule/completion/error metadata can outlive one maintenance execution while an interrupted Auto scan still restarts from the beginning.

> **maintenance-control persistence horizon ≠ maintenance-execution persistence horizon.**

The earlier IBM disclosure shows nonvolatile placement as an architectural option for scanner program/metadata, while the Seagate filing shows traversal and finite log state as distinct objects. Neither earlier patent proves the Dell PERC exact restart behavior, and the comparison remains functional rather than genealogical.

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

`04-198r5` itself says proprietary drive methods and operating-system scanning already existed. That statement is now backed by direct earlier primary evidence: IBM's controller/host-capable media scanner was publicly disclosed in December 2002, and Seagate had filed a drive-side BGMS/pre-scan design by December 2003. The latter filing became public only in August 2005, so it is a pre-standardization design record rather than a pre-vote public-document floor.

These records close the bounded debt `obtain direct pre-2005 primary evidence for proactive media scanning`, but they do not identify the first-ever implementation, first shipment, or one proven genealogy into T10.

The March 2005 plenary evidence establishes a standards-inclusion decision, not invention. The April 2005 Dell manual moves the named PERC public-document floor earlier than the June MegaPR utility release, but neither artifact establishes first firmware implementation or invention. IBM's 2002 disclosure provides an earlier generic controller-level mechanism floor without back-dating the specific term `Patrol Read`. The 2007 Seagate manual establishes one drive-side product witness, not universal adoption.

The broader ROADMAP phrase `controller patrol-read history` therefore remains partly open, but three bounded gaps are now closed:

- **generic controller/RAID-controller proactive media scanning is directly public in the IBM record by December 2002**;
- **named Dell PERC 4/Di/Si-family Patrol Read documentation exists by April 2005**;
- **generic LSI MegaRAID Patrol Read documentation exists in the February/March 2006 Version 2.0 manual**, while the inspected February 2003 Version 1.0 manual documents Consistency Check but contains no Patrol Read text match.

The second and third statements are documentation chronologies, not implementation chronologies. Dell and LSI should also not be counted naively as independent vendor lineages because period Dell records explicitly expose LSI Logic / MegaRAID provenance around the relevant controller family.

A full history still needs earlier SCSI VERIFY/host sweep evidence, named IBM product/firmware evidence practicing the 2001 patent family, Seagate product/release evidence between the December 2003 filing and T10 work, pre-April-2005 Dell/LSI firmware/release-note chronology, model-specific OEM/retail controller lineage, IBM ServeRAID and genuinely independent controller vendors, cross-vendor parity consistency-check distinctions, and evidence about how `patrol read` terminology moved across vendors.

A fresh repository search found no dedicated `US6922801` / SCSI BMS / patrol-read history in `tmzncty/computing-archaeology`. If that broader engineering genealogy is built later, it should live there and Case 101 should remain the retention-specific prior-art/BMS/controller boundary.

---

## 2024 Western Digital cross-vendor product deepening

A later named-product witness sharpens the control-state and repair-authority boundary without changing the 2005 standardization claim above. Western Digital's *Ultrastar DC HC590 SAS Hard Disk Drive Specification*, Rev. 1.0 (31 October 2024), exposes current BMS status and `Medium Scan Progress` separately from counts of background scans and background-medium scans performed **over the life of the drive**. This gives a directly documented distinction between a current traversal state and a cumulative maintenance-history summary; the lifetime counter still is not a per-LBA ledger of successful verification.

The same specification says that clearing `EN_BMS` during an active scan suspends the scan and that re-enabling it resumes from the suspended location. The bounded claim is therefore `maintenance execution lifetime != maintenance-control/progress lifetime`. The inspected text does **not** say where that suspended location is stored or that it survives arbitrary reset, power loss, firmware replacement, format, or sanitize, so `resume after disable/re-enable != demonstrated power-loss-persistent checkpoint`.

Most importantly, the HC590 states that **reassignment during the background scan is not supported**. Its result states instead include cases where a defect is pending an application-client `REASSIGN` or write, where a rewrite succeeded, and where the application client successfully reassigned the block. Compared with the existing 2007 Seagate witness, which makes logging/reallocation depend on ARRE/AWRE policy, this blocks a universal `BMS = automatic in-scan relocation` reading:

> **BMS support != automatic in-scan reassignment support.**

and:

> **standardized BMS control/reporting semantics != identical vendor repair policy.**

The 2024 product document is later continuity/counterexample evidence, not evidence of T10's 2005 historical intent or a Seagate-to-Western-Digital implementation genealogy.

Detailed record: [`../evidence/101-wd-2024-bms-progress-repair-policy-deepening.md`](../evidence/101-wd-2024-bms-progress-repair-policy-deepening.md).

---

## 2003–2006 LSI/Dell documentation chronology and source-lineage deepening

The bounded chronology adds a layer that the earlier Dell controller deepening did not attempt.

The inspected LSI **Version 1.0 / February 2003** manual documents `Check Consistency` but yields no `Patrol Read` text match. This is treated only as documentation absence. Dell's **April 2005** PERC 4/Di/Si / 4e/Di/Si guide then exposes Patrol Read mode/status/control and Auto/Manual/Manual Halt/Disabled behavior. Dell's **7 June 2005** MegaPR Linux package is explicitly an initial utility release, but it requires a pre-existing supported firmware level and Patrol Read mode. LSI's generic **Version 2.0 / February–March 2006** manual then exposes a dedicated Patrol Read section and the same broad control vocabulary.

This closes the narrow sequence:

```text
February 2003 inspected LSI manual
    -> Consistency Check documented
    -> no Patrol Read text match

April 2005 Dell PERC guide
    -> named-controller Patrol Read documented

7 June 2005 Dell MegaPR Linux
    -> host utility release
    -> requires supporting firmware

February/March 2006 LSI Version 2.0
    -> generic MegaRAID Patrol Read documented
```

It does **not** close conception, first firmware, first shipment, or invention dates. The IBM December-2002 public disclosure now provides an earlier generic controller proactive-scan mechanism, which makes the LSI 2003 terminology absence even less suitable as evidence for absence of broader practice.

The same evidence also changes how cross-vendor corroboration is counted. Dell's guide names MegaRAID as an LSI Logic trademark; Dell's official MegaPR page titles the supported PERC list with `LSI Logic`; LSI documentation explicitly contemplates MegaRAID controllers installed in systems made by other manufacturers. Therefore:

> **different corporate masthead != independently evolved engineering lineage.**

The Dell and LSI documents still provide useful separate artifacts and chronology, but they should be weighted as an overlapping controller ecosystem until model/firmware genealogy proves more.

The LSI Version 2.0 manual's `Copyright © 2003–2006` also supplies a source-control warning: its revision table and the inspected 2003 First Edition must govern feature dating. A copyright range is not evidence that every later clause existed at the start of the range.

Detailed source/claim ledger: [`../evidence/101-lsi-dell-2003-2006-patrol-read-documentation-lineage-deepening.md`](../evidence/101-lsi-dell-2003-2006-patrol-read-documentation-lineage-deepening.md).

---

## 2005–2006 Dell PERC controller deepening

The Dell slice closes a different layer than the Western Digital drive witness, the early-patent prior-art floor, and the source-lineage chronology above. Dell's April 2005 user guide supplies the earliest inspected named-controller `Patrol Read` documentation; the 7 June 2005 MegaPR release proves a public host-side `Patrol Read` control/status utility on named PERC families. The February 2006 Dell Power Solutions article then describes controller-orchestrated media testing, redundancy-assisted reconstruction, drive reassignment/rewrite, Auto/Manual recurrence, and workload-sensitive command issue.

The same period article explicitly separates three maintenance/health relations:

```text
Patrol Read
    -> proactive media-defect coverage/recovery

Consistency Check
    -> parity/mirror data-consistency qualification/correction

SMART alerts
    -> predictive drive-health warning
```

A later Dell support record for the legacy PERC family adds NVRAM-held scheduling, recent completion summaries, and error information. Crucially, it also states that an interrupted Auto Patrol Read starts again from the beginning after reboot, while Manual mode does not automatically restart. Therefore the retained controller state cannot be treated as one undifferentiated checkpoint:

> **retained maintenance policy / summary / error evidence != retained exact execution frontier.**

The record also describes RAID-state-dependent repair, so a controller can discover a medium defect in a state where redundant reconstruction is not admissible. Hence:

> **coverage != reconstructability != remediation.**

Detailed source and claim ledger: [`../evidence/101-dell-2005-2006-perc-patrol-read-controller-deepening.md`](../evidence/101-dell-2005-2006-perc-patrol-read-controller-deepening.md).

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
14. `BMS standardization ≠ invention of background scanning or proof of a patrol-read genealogy`;
15. `device-local proactive scan ≠ controller-level redundancy-aware proactive scan`;
16. `Patrol Read ≠ parity/mirror Consistency Check ≠ SMART prediction`;
17. `defect discovery ≠ payload reconstructability ≠ completed controller repair`;
18. `persistent maintenance policy/summary/error evidence ≠ persistent exact scan-position checkpoint`;
19. `recent per-drive completion bitmap ≠ per-LBA verification ledger`;
20. `restarted maintenance from the beginning ≠ loss of all retained maintenance policy/history`;
21. `public documentation date ≠ firmware implementation date ≠ invention date`;
22. `initial host-utility release ≠ initial controller-feature release`;
23. `copyright range ≠ clause introduction date`;
24. `second corporate masthead ≠ independent engineering lineage`;
25. `completion-relative recurrence schedule ≠ fixed wall-clock period`;
26. `patent filing date ≠ patent publication date ≠ standards approval date ≠ product shipment date`;
27. `generic controller-level scan mechanism ≠ named-product Patrol Read terminology`;
28. `finite maintenance log ≠ complete lifetime maintenance history`;
29. `maintenance locus ≠ maintenance function` — host, controller, and drive can perform functionally similar pre-demand verification without sharing implementation or authority.

These are project analytical statements unless a distinction is explicitly marked above as historical vocabulary. They are not assertions that IBM, T10, Dell, LSI, Seagate, or Western Digital engineers used this ontology.

---

## Philosophical interpretation — bounded

Case 101 strengthens a narrow theme already visible in Synthesis 08: some retention work is **epistemic maintenance**. A physical embodiment can remain present while the system's justified confidence in its future readability decays because no recent operation has exercised it. A background scan creates new evidence by deliberately reading before application demand forces the question.

The IBM/Seagate prior-art deepening shows that this epistemic relation was already coupled to concrete control structures before T10 standardization: workload gates, selected coverage, traversal position, written-region metadata, finite error logs, redundancy-aware reconstruction, and pre-scan-dependent write semantics. That does not make the patents a single genealogy; it shows that `verification` was already an engineered state machine rather than an abstract idea.

The Dell controller comparison adds another bounded point: a system can retain evidence that maintenance is due, recently completed, or encountered errors without retaining an exact continuation point for the interrupted act itself. The `obligation/history` relation and the `execution frontier` are different retained objects.

The source-lineage deepening adds a historiographic guardrail rather than a new ontology of storage: retained documentation does not become independent evidence merely because it survives under multiple mastheads. Provenance conditions the weight of apparently repeated testimony.

The stronger universal claim must be rejected. Storage does not become persistent merely because it is repeatedly observed, and not every medium needs proactive reading to remain physically stable. Here the scan does not cause magnetic retention in the ordinary sense; it changes what the system knows about the embodiment and can trigger later repair before redundancy or recoverability margin is lost.

---

## Evidence limits / future work

Still open:

- full archival reconstruction of `04-198r0` through `r4` and every CAP change;
- exact final SBC-3/SPC-4 publication wording and later revision genealogy;
- host-initiated SCSI VERIFY scrub history before device-side BMS;
- pre-2001 controller/vendor proactive-scan implementation evidence;
- named IBM product/firmware evidence tying US09/872,386 to a shipped controller;
- Seagate product/release evidence between the December 2003 filing and the 2005 T10 process;
- direct T10 contribution/prosecution evidence for or against patent-to-standard clause genealogy;
- pre-April-2005 Dell/LSI Patrol Read firmware-development, release-note, and shipment chronology;
- exact model/firmware lineage between individual Dell PERC 3/4 controllers and retail/generic LSI MegaRAID families;
- IBM ServeRAID and genuinely independent controller vendors' period `Patrol Read` genealogy and terminology;
- cross-vendor distinction between patrol read and parity `Consistency Check` beyond the related Dell/LSI ecosystem;
- direct evidence for or against a T10-BMS-to-controller-Patrol-Read genealogy;
- field fault injection on BMS- or period-PERC/MegaRAID-capable hardware;
- quantitative BMS/controller scheduling, bandwidth, and detection-latency behavior in deployed arrays;
- interaction with drive-internal ECC, SMART predictive attributes, and error-recovery firmware;
- correlated/multi-sector defects and URE-aware RAID rebuild policy;
- exact persistence of legacy PERC NVRAM Patrol Read fields across controller replacement, NVRAM loss/corruption, and firmware transition;
- lower-layer forensic persistence after reassignment or logical retirement.

The direct pre-2005 mechanism floor is now partially closed by IBM 2001/2002 and Seagate 2003 evidence; earliest-ever practice, shipping implementations, and detailed genealogy remain open.

These limits do not block the bounded result.

---

## Related repositories

### `tmzncty/computing-archaeology`

Repository search found no dedicated `US6922801`, SCSI BMS, or patrol-read case at the time of this slice. Case 101 therefore keeps only the retention-specific historical boundary, maintenance-state decomposition, and source-provenance warning. A broader history of IBM/Seagate controller and drive development, host scrubbing, SCSI VERIFY, LSI/MegaRAID/PERC/ServeRAID genealogy, patent lineage, and consistency checking should be developed there and linked back rather than duplicated here.

### `tmzncty/problem-history`

Useful anti-anachronism guardrail: `readability qualification`, `coverage age`, `maintenance evidence`, `maintenance-control persistence horizon`, `documentation floor`, and `source-lineage independence` are project reconstructions. Historical actors in the bounded sources spoke of background media surface scanner, proactive media defect management, BGMS, pre-scan, BMS, Patrol Read, Patrol Read Mode/Status/Control, Auto/Manual/Manual Halt/Disable, Consistency Check, SMART, recovered/unreadable errors, ARRE/AWRE, log pages, reassignment status, NVRAM, and completion bitmaps.

---

## Sources

### Primary / contemporary

- IBM / John Edward Archibald, Jr. and Brian Dennis McKean, **_Storage media scanner apparatus and method providing media predictive failure analysis and proactive media surface defect management_**, US09/872,386, filed 1 June 2001; published as US20020184580A1 on 5 December 2002; later US6922801B2: <https://patents.google.com/patent/US6922801B2/en>
- LSI Logic, **_MegaRAID Configuration Software User's Guide_**, DB15-000269-00, Version 1.0 / First Edition, February 2003. Surviving searchable PDF mirror: <https://www.manuallib.com/download/pdf0/LSILOGIC-MEGARAID-CONFIGURATION-SOFTWARE-USER-GUIDE.PDF>
- Seagate / Mark Gaertner, Xiaoying Li, David A. Anderson, **_Background media scan for recovery of data errors_**, US10/740,886, filed 18 December 2003; published as US20050188238A1 on 25 August 2005; later US7490261B2: <https://patents.google.com/patent/US7490261B2/en>
- T10, Gerry Houlder (Seagate), **`04-198r5 — Background Medium Scan`**, 9 March 2005: <https://www.t10.org/ftp/t10/document.04/04-198r5.pdf>
- T10, Weber & Lohmeyer, **Minutes of T10 Plenary Meeting #66 — March 10, 2005**, `05-097r0`, especially §10.5 recording approval of `04-198r5`: <https://www.t10.org/ftp/t10/document.05/05-097r0.htm>
- Dell, **_PowerEdge Expandable RAID Controller 4/Di/Si and 4e/Di/Si User's Guide_**, Release April 2005, Rev. A07. Surviving page-preserving copy: <https://dell.manymanuals.com/computer-hardware/perc-4-si/user-manual-31973>
- Dell, **MegaPR for Linux, v.1.03, A02**, release date 7 June 2005: <https://www.dell.com/support/home/en-us/drivers/driversdetails?driverid=nfpxp>
- T10, Rob Elliott (HP), **`05-340r3 — SBC-3 SPC-4 Background scan additions`**, 18 January 2006: <https://www.t10.org/ftp/t10/document.05/05-340r3.pdf>
- T10, **2005 document register**, identifying CAP minutes `05-096r0`, plenary minutes `05-097r0`, and the `05-340` proposal family: <https://www.t10.org/doc05.htm>
- Drew Habas and John Sieber, **“Background Patrol Read for Dell PowerEdge RAID Controllers,”** *Dell Power Solutions*, February 2006, pp. 73–75. Historical Dell URL: <http://www.dell.com/downloads/global/power/ps1q06-20050212-Habas.pdf>. Inspected surviving page-preserving PDF: <https://device.report/m/6f19713c57627fcded037f379ce7f40935f82e64231047790be0b44ae2498823.pdf>
- LSI Logic, **_MegaRAID Configuration Software User's Guide_**, DB15-000269-01, Version 2.0 / Second Edition, February/March 2006. Current Broadcom archive: <https://docs.broadcom.com/doc/12353347>
- Seagate, **_Cheetah 15K.5 FC Product Manual_, Publication 100384772 Rev. C**, February 2007, §7.4 `Background Media Scan`: <https://www.seagate.com/staticfiles/support/disc/manuals/fc/100384772c.pdf>

### Later vendor continuity / implementation detail

- Dell, **Patrol ReadによるRAIDアレイのメンテナンス**, document `000129145`, version 7, last updated 24 February 2026: <https://www.dell.com/support/kbdoc/ja-jp/000129145/patrol-read%E3%81%AB%E3%82%88%E3%82%8Braid%E3%82%A2%E3%83%AC%E3%82%A4%E3%81%AE%E3%83%A1%E3%83%B3%E3%83%86%E3%83%8A%E3%83%B3%E3%82%B9>

### Independent scholarly context

- Lakshmi N. Bairavasundaram, Garth R. Goodson, Shankar Pasupathy, Jiri Schindler, **“An Analysis of Latent Sector Errors in Disk Drives,”** SIGMETRICS 2007, pp. 289–300, DOI `10.1145/1254882.1254917`: <https://research.cs.wisc.edu/adsl/Publications/latent-sigmetrics07.html>

### Internal comparisons

- [`cases/14-scsi-disk-defect-reassignment-logical-identity.md`](14-scsi-disk-defect-reassignment-logical-identity.md)
- [`cases/18-zfs-scrub-latent-error-detection.md`](18-zfs-scrub-latent-error-detection.md)
- [`cases/55-nvme-smart-health-endurance-telemetry.md`](55-nvme-smart-health-endurance-telemetry.md)
- [`cases/83-apache-hdfs-block-scanner-checksum-verification.md`](83-apache-hdfs-block-scanner-checksum-verification.md)
- [`cases/111-enterprise-ssd-extended-shutdown-maintenance.md`](111-enterprise-ssd-extended-shutdown-maintenance.md)
- [`docs/SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md`](../docs/SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md)
- [`docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md`](../docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md)

---

## Status

**Grounded bounded case.**

The core drive-side mechanism and historical boundary remain supported by T10 proposal/committee records plus a named Seagate product manual; the SIGMETRICS field study is used only as independent latent-error context. The prior-art floor is now materially stronger: IBM's controller/RAID-controller/host-capable media scanner was publicly disclosed by 5 December 2002, and Seagate's December-2003 filing already records drive-side BGMS, power-up pre-scan, idle/interval gating, error logs, and conditional WRITE AND VERIFY before the March 2005 T10 approval, while publication of that Seagate application occurred only in August 2005. This closes a bounded `direct pre-2005 mechanism evidence` gap without making an earliest-invention or patent-to-standard genealogy claim.

The controller branch still has a tighter named-product documentation chronology: the inspected LSI 2003 First Edition documents Consistency Check but not Patrol Read; Dell PERC 4/Di/Si-family documentation exposes Patrol Read by April 2005; Dell's MegaPR Linux utility follows on 7 June 2005 and presupposes supporting firmware; and generic LSI MegaRAID Version 2.0 documentation exposes Patrol Read by its February/March 2006 edition. The Dell deepening still supplies the stronger controller-state counterexample in which maintenance schedule/completion/error evidence can persist while an interrupted Auto pass does not retain an exact restart frontier.

Case 101 still does not claim invention of scrubbing, a direct IBM/Seagate-patent→T10 genealogy, a direct T10→PERC/MegaRAID genealogy, complete cross-vendor patrol-read history, or equivalence with higher-layer integrity verification; Dell/LSI documents remain explicitly weighted as overlapping source/engineering lineage rather than naively independent vendor witnesses.