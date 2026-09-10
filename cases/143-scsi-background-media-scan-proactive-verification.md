# SCSI Background Media Scan: Idle-Time Verification, Retained Scan Progress, and Repair-Authority Separation

**Status:** `grounded`

## Scope

- **Object / system:** SCSI Background Medium/Media Scan (BMS), bounded to 2005 T10 standardization proposals plus named Seagate 2007 and Western Digital 2024 SAS-drive implementations.
- **Date range:** **2005–2024**, with explicit evidence inside the 2005 proposal that proprietary drive and operating-system background scanning already existed earlier.
- **Retention question:** how can a disk keep proactive integrity-inspection work alive across foreground service interruptions, and how do scan coverage, defect evidence, and defect repair remain separate states?

This is not a generic history of disk scrubbing, SMART, SCSI error recovery, RAID, filesystem checksums, or hard-disk failure physics. Case 18 already grounds ZFS pool scrubbing; Case 83 grounds the HDFS DataNode block scanner; Case 14 grounds SCSI logical-block identity across defect reassignment. This case stays below those layers and asks a narrower question:

> **Can a medium remain ordinarily readable while the device still owes proactive inspection, and can that inspection be suspended, resumed, and reported without equating verification with repair?**

The answer in the bounded record is yes.

Detailed source ledger: [`../evidence/143-t10-2005-seagate-wd-background-media-scan-grounding.md`](../evidence/143-t10-2005-seagate-wd-background-media-scan-grounding.md).

---

## Historical vocabulary

The inspected primary sources directly use:

- `Background Medium Scan` / `Background Media Scan`;
- `BMS` / `BGMS`;
- `background pre-scan` / `Media Pre-Scan`;
- `Background Scan Results log page`;
- `BMS status` / `background scanning status`;
- `Medium Scan Progress`;
- `Number of Background Scans Performed`;
- `EN_BMS`;
- `BMS Interval Time` / `Background Medium Scan Interval Time`;
- `IDLE TIME` / `Minimum Idle Time Before Background Scan`;
- `REASSIGN STATUS`;
- `ARRE` / `AWRE`;
- `REASSIGN BLOCKS`;
- `re-write` / `reallocation` / `reassignment`;
- `suspected bad logical blocks` / `medium error`.

Project phrases such as **inspection obligation**, **verification coverage**, **maintenance continuation point**, **repair-authority separation**, and **second-order maintenance evidence** are engineering reconstructions. They are not source-era SCSI terminology.

The spelling varies: T10 proposals commonly say `Background Medium Scan`, while the Seagate manual says `Background Media Scan`. The case preserves source wording rather than inventing a historical distinction between the two forms.

---

## Prior-art / chronology boundary

T10/04-198 revision 5 is dated 9 March 2005, but its first page explicitly says:

- several drive vendors, including Seagate, already had proprietary methods for controlling background scan operations;
- many systems already implemented background medium scanning in their operating systems;
- customers wanted a standard method so host processes could control and retrieve status consistently.

The same document's revision notes refer to changes requested at the November 2004 CAP meeting.

Therefore this case uses 2005 as a **public standardization witness**, not an invention date.

Safe historical formulation:

> **By 2005, T10 was standardizing control and reporting for drive-side background medium scanning against a field that the proposal itself describes as already containing proprietary drive and operating-system implementations.**

This case does not establish first invention, first commercial deployment, first use of the word `scrub`, or a direct genealogy from any earlier operating-system scan to SCSI BMS.

---

## Retained state

BMS exposes several different kinds of state that must not be collapsed.

### 1. User payload on the medium

The disk's ordinary logical blocks remain the data whose continued readability is being tested.

BMS does not create a second authoritative payload copy merely by reading those blocks.

### 2. Current scan execution / traversal state

The device can be:

- waiting for the BMS interval;
- waiting for enough idle time;
- actively scanning;
- temporarily preempted by foreground commands;
- explicitly suspended;
- halted by a condition such as a vendor-specific cause or temperature limit;
- at some progress point between first and final LBA.

This is maintenance-control state, not payload.

### 3. Scan progress and cumulative scan counters

The standardized/logged interface exposes current scan progress and a number-of-scans field. The 2024 Western Digital HC590 further labels scan counts as totals over the **life of the drive**.

Thus:

`current traversal point != cumulative maintenance count`

Neither is a complete record of every LBA's full verification history.

### 4. Defect/error evidence

The Background Scan Results log can contain medium-error entries with defect location, sense information, time information, and reassignment status.

These entries are evidence produced by maintenance. They are neither the payload nor a guarantee that the defect has already been fixed.

### 5. Repair/reassignment state

A detected problematic LBA may be:

- judged not to need reassignment;
- awaiting a host REASSIGN or write action;
- successfully reassigned by the device;
- unsuccessfully reassigned;
- recovered by rewrite;
- handled by a product-specific path.

The result therefore carries **repair-state typing** after discovery.

---

## Physical / logical substrate

At the payload layer this case concerns magnetic-disk logical blocks implemented on a drive's physical recording medium and accessed through the drive controller.

BMS adds controller-side machinery:

- an LBA traversal;
- an interval/idle scheduler;
- read/error-recovery logic;
- scan status/progress;
- a result log;
- optional rewrite/reassignment policy;
- a host-visible SCSI control/reporting interface.

The logical block remains the interface designation even if later defect management replaces its physical sector, as separately studied in Case 14.

Do not infer the exact servo, ECC, head, sector-remapping, NVRAM, or firmware implementation from the BMS interface alone.

---

## Retention mechanism

### Ordinary retention is not BMS itself

The magnetic recording medium and drive electronics retain/read the ordinary payload independently of whether BMS is currently running.

BMS is a **proactive integrity-maintenance path** layered on that retained medium. Its purpose is not to rewrite every healthy sector periodically. It reads the medium to discover difficult/unreadable locations before ordinary demand necessarily encounters them.

Thus:

`medium retention mechanism != proactive verification mechanism`

### Recurring inspection

In the 2005 T10 model, after the configured interval and idle condition the device begins scanning from LBA zero through the final LBA. After a complete pass, the interval relation starts again and another cycle may later begin.

This is recurring inspection, but it is not DRAM refresh:

- BMS need not rewrite healthy blocks;
- its interval is a maintenance scheduling parameter rather than a demonstrated physical bit-retention deadline;
- ordinary host service can preempt the scan.

### Opportunistic execution

The work is deliberately pushed into idle opportunity. T10/05-340r0 adds an explicit idle-time condition. Seagate's 2007 Cheetah implementation says BMS performs sequential reads while idle and immediately yields to host commands, aside from finishing a BMS error-recovery action already in progress.

Therefore:

`maintenance recurrence != continuous execution`

and

`maintenance enabled != maintenance currently running`

---

## Foreground preemption and maintenance continuation

This is the central retention relation in the case.

The 2005 T10 proposals say that foreground commands suspend an active background scan, and that scanning later resumes from the point where it stopped. The 2024 Western Digital HC590 additionally says an in-progress scan disabled with `EN_BMS=0` is suspended and, when re-enabled, resumes from the suspended location.

That gives the bounded state transition:

```text
inspection still owed
        ↓
scan starts
        ↓
progress advances
        ↓
foreground command or explicit disable
        ↓
scan execution suspended
        ↓
foreground service / disabled interval
        ↓
resume condition satisfied
        ↓
scan continues from retained working position
```

So:

> **an individual execution interval can end while the maintenance continuation relation survives.**

This is not yet proof of **power-loss-persistent** scan progress. The inspected sources establish resume across foreground preemption and, for the HC590, disable/re-enable. They do not establish where that position is stored or whether it survives arbitrary reset/power cycle.

---

## Read semantics

### Demand read

An application-client read exists to satisfy an ordinary request.

### BMS read

A BMS read exists to test the medium proactively. T10/04-198r5 defines scanning in terms of identifying difficult/unreadable blocks, logging problems, and optionally taking corrective action. It also says scanned blocks are not retained in cache merely because BMS read them.

Thus:

`read operation != one universal semantic role`

The same broad physical read machinery may participate in foreground retrieval, proactive verification, pre-scan, error recovery, and maintenance without those operations having the same authority or temporal purpose.

---

## Detection is not repair

The T10 result model makes this separation unusually explicit.

A medium-scan entry can say that:

- no reassignment is needed;
- reassignment is pending host action;
- the drive successfully reassigned the LBA;
- reassignment failed;
- the LBA recovered via rewrite.

T10 also says the host may need to take action after examining the result log.

Therefore:

> **defect discovery != repair completion.**

and:

> **verification coverage != restored physical repair margin.**

This blocks a common shortcut in descriptions of `scrubbing`, where scan, diagnosis, repair, and later revalidation are compressed into one verb.

---

## Vendor policy is not implied by the generic feature name

The named-product evidence deliberately includes a counterexample.

Seagate Cheetah 15K.5 (2007) says unreadable and recovered error sites are logged or reallocated according to ARRE/AWRE settings.

Western Digital Ultrastar DC HC590 (2024) exposes the same broad BMS family of status/result semantics but states explicitly that **reassignment during the background scan is not supported**. Its result states include pending application-client action, successful rewrite, and successful application-client reassignment.

Thus:

`BMS supported != automatic in-scan reassignment supported`

and

`standardized control/reporting semantics != identical vendor repair implementation`

The later HC590 is a product-level counterexample, not historical evidence about what every 2005 proposer or 2007 Seagate drive did.

---

## Coverage and time

At least six different timescales appear:

1. ordinary foreground command latency;
2. idle time before background work is admitted;
3. one burst of background execution;
4. time required to traverse the medium;
5. configured interval between BMS cycles;
6. much longer lifetime accumulation of scan counts and defect evidence.

These should not be normalized into one `refresh interval`.

A complete scan means the configured traversal reached its end under the drive's detection semantics at that time. It does not mean:

- every future read will succeed;
- every analog degradation process was measured;
- every latent corruption above the drive layer was detected;
- the drive can never develop a later defect.

The fact that BMS recurs is itself evidence against treating one pass as a timeless certificate.

---

## Maintenance evidence can have a different lifetime from maintenance execution

The source set exposes several forms of second-order evidence:

- current BMS status;
- current scan progress;
- cumulative scan counts;
- defect/error log entries;
- reassignment/repair status.

A scan may no longer be executing while some of those results remain available to the host. Conversely, T10/04-198r5 allows medium-scan log entries to be deleted or overwritten without implying that the user payload itself has been deleted.

Therefore:

`maintenance execution lifetime != maintenance-evidence lifetime != payload lifetime`

The HC590's lifetime scan counts add another horizon, but they still do not constitute a full per-sector history.

---

## Maintenance and labor

### Device-side work

The drive may perform:

- interval and idle-time scheduling;
- sequential LBA traversal;
- read retries/correction through its normal error-recovery machinery;
- progress accounting;
- defect/error logging;
- optional rewrite/reassignment depending on product/policy;
- foreground preemption and later continuation.

### Host/operator work

The host can participate by:

- enabling/disabling BMS;
- configuring timing/control fields;
- polling status/results;
- receiving asynchronous error indications where configured;
- issuing REASSIGN or later write operations for defects not fully handled by the device;
- choosing error-recovery/reallocation policy.

The maintenance regime therefore is not accurately described as either purely `automatic` or purely `host-driven`.

A better decomposition is:

`device executes inspection + host/device share policy/repair authority`

---

## Failure / forgetting modes

Keep these separate.

### 1. Physical medium defect exists but has not yet been discovered

The block may remain apparently present until a demand read or proactive scan exposes difficulty.

### 2. BMS has not yet covered the block in the current cycle

Lack of recent verification is not itself proof of corruption.

### 3. Scan is temporarily preempted

Foreground service interrupts the maintenance execution, but the scan can later resume.

### 4. Scan is explicitly disabled or halted

This is a control/scheduling state, not payload erasure.

### 5. Defect is detected but repair is pending

Evidence exists, but host/device repair action has not yet completed.

### 6. Repair/reassignment fails

The existence of a scan and a detected LBA does not guarantee successful re-embodiment.

### 7. Result evidence is overwritten/cleared

The defect-log history can be reduced without proving that the underlying block was repaired or securely erased.

### 8. Higher-layer corruption survives a clean drive-level scan

BMS does not establish filesystem checksum validity, application-object currentness, RAID parity currentness, or distributed-replica authority.

---

## Historical record

The bounded primary record supports these claims:

1. **T10/04-198r5 (9 March 2005)** proposed a standard control/status model for BMS and explicitly acknowledged pre-existing proprietary drive and OS scanning;
2. the T10 model defined medium scanning as proactive reads to identify difficult/unreadable blocks, log them, and optionally make them readable again;
3. T10 background scan is distinct from foreground application traffic and may be suspended by foreground commands;
4. T10 exposes status, scan count, progress, medium-error location, and reassignment status;
5. repair can be complete, pending host action, failed, or achieved through rewrite/reassignment rather than being implied by scan completion;
6. **T10/05-340r0 (9 September 2005)** further exposes interval + idle admission and resume-from-position behavior;
7. **Seagate Cheetah 15K.5 Rev. E (August 2007)** implements a named self-initiated idle-time BMS and documents host-command preemption plus ARRE/AWRE-dependent logging/reallocation;
8. **Western Digital Ultrastar DC HC590 Rev. 1.0 (31 October 2024)** exposes BMS progress/lifetime counts and resume-after-disable semantics while explicitly declining in-scan reassignment.

Primary sources:

- T10/04-198r5, *Background Medium Scan*: <https://www.t10.org/ftp/t10/document.04/04-198r5.pdf>
- T10/05-340r0, *SBC-3 SPC-4 Background scan additions*: <https://www.t10.org/ftp/t10/document.05/05-340r0.pdf>
- Seagate, *Cheetah 15K.5 SAS Product Manual*, Rev. E, August 2007: <https://www.seagate.com/content/dam/seagate/migrated-assets/staticfiles/support/disc/manuals/enterprise/cheetah/15K.5/SAS/100384784e.pdf>
- Western Digital, *Ultrastar DC HC590 SAS Hard Disk Drive Specification*, Rev. 1.0, 31 October 2024: <https://documents.westerndigital.com/content/dam/doc-library/en_us/assets/public/western-digital/product/data-center-drives/ultrastar-dc-hc500-series/product-manual-ultrastar-dc-hc590-sas.pdf>

---

## Engineering reconstruction

The source record supports the following project-level distinctions:

1. **payload presence != recent proactive verification**;
2. **ordinary read service != BMS verification read**;
3. **BMS enabled != BMS executing**;
4. **foreground preemption != maintenance cancellation**;
5. **scan progress != defect-event history**;
6. **cumulative scan count != per-LBA verification history**;
7. **scan completed != every defect repaired**;
8. **defect detected != repair completed**;
9. **device-side inspection != device-side automatic reassignment**;
10. **one completed pass != future integrity guarantee**;
11. **BMS interval != physical retention deadline**;
12. **maintenance continuation point != demonstrated power-loss-persistent checkpoint**;
13. **maintenance evidence can outlive one execution burst without being payload**;
14. **cleared scan-result evidence != media sanitization**;
15. **drive-level media verification != end-to-end logical integrity**.

---

## Functional analogies

### Case 18 — ZFS scrub

Both mechanisms can discover a problem before ordinary application demand reaches it.

But:

- BMS is inside the drive and qualifies readability under drive error-recovery semantics;
- ZFS scrub traverses pool/filesystem state, checks ZFS checksums, and can use ZFS redundancy for self-healing.

So:

`proactive verification functionally similar != same verifier authority or repair layer`

No genealogy is claimed.

### Case 83 — HDFS block scanner

HDFS also retains traversal/progress state for proactive verification, but its object is an HDFS replica plus checksum relation, and failed verification is reported into distributed replica management.

BMS does not know HDFS replica currentness or NameNode authority.

Thus:

`maintenance progress can recur at several layers != one universal scan state`

### Case 14 — SCSI defect reassignment

Case 14 focuses on preserving logical-block identity while physical placement changes. Case 143 adds the earlier **discovery/qualification** step that may lead to reassignment.

`discovery != relocation`

### Case 136 — RAID rebuild rate

Case 136 concerns how much controller resource an admitted repair receives after a member failure. BMS instead spends idle opportunity proactively testing the medium before a member-level failure necessarily occurs.

`proactive inspection scheduling != failed-member rebuild scheduling`

---

## Philosophical / media-theoretical interpretation

The mechanism supports one narrow interpretive point.

A retained object can remain materially present and ordinarily readable while the system nevertheless treats its **continued trustworthiness as unfinished work**. Retention in this case therefore includes not only holding a state but maintaining a recurring opportunity to inspect the material support and preserve enough control/evidence to continue that inspection after foreground work interrupts it.

This does not make verification state another copy of the object. It does not imply that all persistence is operational or continuously active. It only sharpens one bounded form of technical availability:

> **some retained embodiments remain dependable partly because inspection can recur, be preempted, resume, produce evidence, and hand discovered defects to a separate repair authority.**

No claim is made that BMS is `tertiary retention`, that media scans instantiate Heideggerian `Bestand`, or that SCSI designers were theorizing memory philosophically.

---

## Counterexamples and limits

- **Standardization != invention.** T10's own 2005 proposal reports pre-existing proprietary and OS implementations.
- **BMS != periodic refresh.** Healthy sectors need not be rewritten every interval and no cell-level decay deadline is established.
- **BMS != SMART as a whole.** A product can integrate reporting with other health machinery, but this case does not equate the categories.
- **BMS != ZFS/HDFS scrub.** They operate at different layers with different integrity evidence and repair authority.
- **Successful scan != timeless integrity certificate.** Later defects remain possible.
- **Detected defect != automatic repair.** The HC590 explicitly supplies a counterexample to universal in-scan reassignment.
- **Resume from suspended location != proven crash-durable checkpoint.** Power-cycle/reset persistence is not established here.
- **Reassignment != secure erasure.** An old physical sector's forensic state is not established by logical reallocation.
- **Current scan progress != complete maintenance history.** The result log is finite and can be cleared/overwritten.
- **Drive-level readability != application correctness.** BMS does not certify higher-layer checksums, parity, version currentness, or semantic integrity.
- **2007 Seagate behavior != 2024 Western Digital behavior.** Same feature family does not erase implementation chronology.

---

## Related repositories

A fresh `tmzncty/computing-archaeology` repository search for `background media scan SCSI` returned no dedicated study during this slice.

Broader work on:

- pre-2005 disk scrubbing and proprietary vendor scan implementations;
- SMART/offline testing genealogy;
- SCSI SPC/SBC revision history;
- disk ECC/servo/media defect physics;
- product firmware and NVRAM implementation;
- empirical latent-sector-error distributions;

belongs primarily in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) if developed. This repository should retain the cross-mechanism relation among **proactive inspection, foreground preemption, maintenance continuation/evidence, and separate repair authority**.

---

## Next evidence work

The bounded case is grounded. Further work should be targeted rather than another generic disk-health survey:

- recover exact T10/04-198 first-revision chronology and final SPC/SBC integration/ballot history;
- identify earlier proprietary implementations named by primary vendor manuals;
- compare exact BMS and SMART offline/self-test semantics;
- test power-cycle/reset persistence of progress/results on named drives;
- collect cross-vendor product differences in automatic rewrite/reassignment;
- add fault-injected/field evidence for latent errors, thermal halt, sustained foreground load, result-log saturation, and power interruption.