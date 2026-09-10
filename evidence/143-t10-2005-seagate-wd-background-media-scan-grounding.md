# Evidence 143 — T10 / Seagate / Western Digital Background Media Scan grounding

**Case:** [`../cases/143-scsi-background-media-scan-proactive-verification.md`](../cases/143-scsi-background-media-scan-proactive-verification.md)

**Bounded question:** how does a disk keep an integrity-inspection obligation alive across ordinary foreground service, and how are scan coverage, defect evidence, and repair authority kept distinct?

**Status:** `grounded` for the bounded 2005 standardization / 2007 named-product / 2024 named-product relation. This record does **not** establish invention priority for disk scrubbing, universal BMS implementation behavior, power-loss persistence of scan position, or physical erasure of defective sectors.

---

## Source ledger

### S1 — T10/04-198 revision 5, *Background Medium Scan*

- **Author:** Gerry Houlder, Seagate Technology.
- **Date on document:** 9 March 2005.
- **Institution:** T10 Technical Committee.
- **Document:** T10/04-198 revision 5.
- **URL:** <https://www.t10.org/ftp/t10/document.04/04-198r5.pdf>
- **Evidence class:** `H/P` — primary standards-development proposal, not a final published ANSI standard.
- **Central locations:** p. 1 overview and revision history; pp. 2–4 model/control text; pp. 5–7 status/result-log fields.

Important anti-priority evidence appears on p. 1. The proposal says several drive vendors, including Seagate, already had proprietary background-scan methods and that many systems implemented background scanning in their operating systems. The proposal's stated purpose is to define a **standard method to control and retrieve status**, not to claim invention of scanning itself. Revision notes also record changes requested at the November 2004 CAP meeting, so work on the proposal predates the revision-5 date; this evidence still does not establish the first proposal, first implementation, or first public use.

### S2 — T10/05-340 revision 0, *SBC-3 SPC-4 Background scan additions*

- **Author:** Rob Elliott.
- **Date on document:** 9 September 2005.
- **Institution:** T10 Technical Committee.
- **Document:** T10/05-340 revision 0.
- **URL:** <https://www.t10.org/ftp/t10/document.05/05-340r0.pdf>
- **Evidence class:** `H/P` — primary standards-development proposal/draft-change text.
- **Central locations:** pp. 2–3 background-medium-scan behavior and result interpretation; pp. 4–6 status/reassignment/control fields.

This later proposal is useful because it states the idle-time and suspension behavior particularly clearly: after the interval and configured idle time, the device scans from LBA zero to the last LBA; foreground application-client commands suspend the scan; the scan resumes where it left off after the foreground work and another idle period. The result log exposes active/suspended status, number of scans, progress, defect locations, and a typed reassignment status.

### S3 — Seagate, *Cheetah 15K.5 SAS Product Manual*, publication 100384784, Rev. E

- **Date:** August 2007.
- **Models:** ST3300655SS, ST3146855SS, ST373455SS.
- **Manufacturer:** Seagate Technology LLC.
- **URL:** <https://www.seagate.com/content/dam/seagate/migrated-assets/staticfiles/support/disc/manuals/enterprise/cheetah/15K.5/SAS/100384784e.pdf>
- **Evidence class:** `H/P` — first-party named-product manual.
- **Central location:** printed §7.4, p. 39 of the manual (PDF p. 44), plus §7 defect/error-management context.

The manual calls BMS a **self-initiated media scan**, says it performs sequential reads across the entire medium while the drive is idle, and explicitly links the feature to T10 SPC-4. It says unreadable/recovered error locations are logged or reallocated according to ARRE/AWRE policy. It also documents foreground preemption: BMS reads are interrupted immediately to service host commands, although an already-started BMS error-recovery action completes before service returns. The product implementation uses bursts of background work and brief suspension windows so other idle functions can run.

### S4 — Western Digital, *Ultrastar DC HC590 SAS Hard Disk Drive Specification*, Rev. 1.0

- **Date:** 31 October 2024.
- **Example models:** WUH722626AL5201 / AL5204 and WUH722624AL5201 / AL5204.
- **Manufacturer:** Western Digital.
- **URL:** <https://documents.westerndigital.com/content/dam/doc-library/en_us/assets/public/western-digital/product/data-center-drives/ultrastar-dc-hc500-series/product-manual-ultrastar-dc-hc590-sas.pdf>
- **Evidence class:** `H/P` — first-party named-product specification used as later continuity and counterexample evidence, not as evidence of 2005 historical intent.
- **Central locations:** §8.8.12, printed pp. 126–127, Background Medium Scan log; §8.11.15.1, printed p. 181, Background Control subpage.

The HC590 exposes BMS status, progress, the total number of background scans and background-medium scans performed **over the life of the drive**, error-time power-on minutes, defect location, and reassignment status. Its Background Control page says disabling EN_BMS during a scan suspends the scan and re-enabling it resumes from the suspended location. Crucially, the same product specification says **reassignment during the background scan is not supported**: detected defects may instead be pending host REASSIGN/write action, successfully rewritten, or recorded as having been reassigned by the application client. This is a useful product-level counterexample to any universal reading of BMS as automatic relocation.

---

## Historical findings

### H1 — the 2005 proposal is standardization evidence, not an invention claim

T10/04-198r5 p. 1 says that multiple drive vendors already had proprietary controls for background medium scan and that many operating systems performed background scanning. Customers wanted a standard method for controlling and retrieving status from drive-side operations.

Therefore the safe historical statement is:

> **By March 2005 T10 had a concrete proposal to standardize drive-side BMS control and reporting; the proposal itself records pre-existing proprietary drive and operating-system scanning and therefore blocks a T10/2005 invention claim.**

Do not rewrite this as `BMS was invented in 2005`.

### H2 — BMS is proactive media read/verification work, not ordinary demand service

T10/04-198r5 pp. 1–2 defines medium scanning as device-server reads intended to identify difficult/unreadable logical blocks, log read problems, and optionally take vendor-specific action to make a block readable again. It says background scanning is performed without using SCSI-interface bandwidth for the scanned data, and that scanned blocks are not retained in cache merely because BMS read them.

Seagate 2007 §7.4 implements the same overall relation as a named product: sequential medium reads during idle time, with the host able to inspect results rather than issuing its own scan traffic.

This grounds:

`ordinary application demand read != proactive BMS verification read`

It does **not** mean BMS observes analog media state directly; it uses the drive's ordinary internal read/recovery machinery.

### H3 — foreground commands can preempt scan execution without cancelling the scan relation

T10/05-340r0 pp. 2–3 says application-client commands suspend an active BMS while the device processes those commands, after which the scan resumes where it left off once commands complete and the configured idle period is satisfied. Seagate 2007 §7.4 gives a named implementation in which BMS is immediately interrupted for host commands, subject to completion of already-started BMS error recovery.

This grounds:

`scan execution interrupted != scan obligation discharged`

and

`foreground service priority != background-maintenance cancellation`

The inspected text does not prove that the resume position survives arbitrary power loss.

### H4 — the standardization work retains explicit progress/status separate from defect results

T10/04-198r5 pp. 5–7 and T10/05-340r0 expose a background scanning status parameter including status, number of scans performed, and medium-scan progress. Separate medium-scan parameters record encountered defect locations and error/reassignment status. T10/04-198r5 also states that clearing medium-scan result parameters need not affect the background-scanning status parameter.

Therefore:

`maintenance progress/status != defect-event ledger`

and

`defect-event ledger != payload`

The proposal's finite log can overwrite older entries when full. It is consequently not a complete history of every defect ever observed.

### H5 — scan completion is verification coverage, not a timeless integrity certificate

The T10 model scans from LBA zero through the final LBA, then waits for the BMS interval and starts another cycle. The recurrence itself is evidence against interpreting one completed pass as permanent proof that no later defect can arise.

Safe reconstruction:

`one completed media pass != future media integrity guarantee`

The BMS interval is a maintenance scheduling interval, not a demonstrated physical data-retention deadline.

### H6 — detection and repair are separate, typed outcomes

T10/04-198r5 says correctable read problems may be rewritten or relocated subject to policy and exposes REASSIGN STATUS values for no reassignment, pending host action, successful device reassignment, failed reassignment, and recovery via rewrite. T10/05-340r0 likewise states that the result field tells the host whether the device handled the defect or the application client may need to reassign/rewrite the LBA.

Thus:

`defect detected != defect repaired`

and

`verification coverage != restored media margin`

This is directly relevant to retention: maintenance can successfully discover a weakening embodiment while the actual re-embodiment/repair step remains separate.

### H7 — automatic repair is not guaranteed by the generic feature name

Seagate 2007 says unreadable/recovered sites are logged or reallocated according to ARRE/AWRE settings. Western Digital HC590 2024, by contrast, explicitly says reassignment **during** background scan is not supported and exposes pending host reassign/write, rewrite success, and application-client reassignment states.

Therefore:

`BMS support != automatic device-side reassignment guarantee`

and

`same standards vocabulary != identical vendor repair policy`

The HC590 is later implementation evidence, not evidence about the Cheetah firmware or the 2005 proposers' exact implementation.

### H8 — later products can retain second-order maintenance evidence over a much longer horizon than one scan

Western Digital HC590 §8.8.12 defines the number of background scans and number of background medium scans as counts performed **over the life of the drive**, while separately reporting current scan progress and BMS status.

This gives a useful state-horizon distinction:

`current scan position/progress != cumulative lifetime scan count`

Neither quantity is equivalent to a per-LBA history of all successful verifications.

### H9 — disable/suspend semantics preserve a maintenance continuation point in the named HC590 contract

HC590 §8.11.15.1 says that changing EN_BMS from one to zero during an active scan suspends the scan; when EN_BMS is set back to one, the scan resumes from the suspended location.

This grounds a bounded continuation relation across **feature disable/re-enable**. It does not establish the nonvolatile storage mechanism for that position, nor survival across a power cycle, controller replacement, firmware update, format, or sanitize event.

---

## Engineering reconstruction

The source record supports the following relation chain:

```text
medium remains ordinarily serviceable
        ↓
BMS interval / idle opportunity arrives
        ↓
device performs proactive sequential reads
        ↓
foreground command may temporarily preempt the scan
        ↓
scan resumes from retained working position
        ↓
read difficulty / unreadability may be discovered
        ↓
result/status evidence is exposed
        ↓
optional device-side rewrite/reassignment
        or
host-side repair action may still be required
        ↓
a later scan can re-check the medium
```

Important decompositions:

1. **payload presence != recent verification**;
2. **ordinary readability now != complete proactive coverage**;
3. **scan enabled != scan currently executing**;
4. **scan interrupted != scan cancelled**;
5. **scan progress != scan history**;
6. **scan history count != per-LBA integrity history**;
7. **defect discovery != repair completion**;
8. **repair completion != permanent future integrity**;
9. **BMS interval != physical retention deadline**;
10. **device-internal scan != filesystem/distributed checksum scrub**;
11. **background-maintenance control state != user payload**;
12. **same BMS interface != one universal reallocation policy**.

---

## Cross-case boundaries

### Case 18 — ZFS scrub

Functional analogy only. Both move integrity discovery before foreground demand, but the evidence authority differs:

- BMS is inside a SCSI disk and checks the medium through the device's own read/error-recovery machinery;
- ZFS scrub traverses filesystem/pool state, verifies ZFS checksums, and may repair from ZFS redundancy.

Therefore:

`drive BMS != filesystem checksum scrub`

and a clean BMS result does not certify ZFS logical checksums, current block-pointer authority, mirrors, RAID-Z parity, or end-to-end application semantics.

### Case 83 — HDFS DataNode block scanner

Again functional analogy only. HDFS deliberately checks stored replicas and can report corrupt replicas to a distributed authority; BMS is below that layer and need not know HDFS block identity, checksum metadata, or replica currentness.

A useful comparison is:

`proactive integrity work can have retained traversal/progress state at multiple layers, but the state being qualified and the repair authority differ.`

Do not infer genealogy between SCSI BMS and HDFS scanning.

### Cases 14 and 136 — reassignment and repair scheduling

Case 14 grounds logical-block identity across SCSI defect reassignment. Case 143 adds a proactive **discovery** route that may feed reassignment/rewrite but does not guarantee it. Case 136 concerns resource priority of RAID rebuild after member failure. These should not be collapsed:

`media verification != defect reassignment != array rebuild scheduling`

---

## Philosophical limit

The narrow conceptual use is that technical retention can include an **inspection obligation**: the bytes need not change for the system to spend time periodically asking whether their physical embodiment still supports reliable recovery.

This is not evidence that every retained object must be continuously inspected. It is not an instance of `tertiary retention` merely because scan state or defect logs persist. The mechanism supports only the bounded claim that **availability over time may depend on preserving and resuming maintenance work whose object is the trustworthiness of an existing embodiment rather than creation of a new payload state.**

---

## Stop conditions / unsupported claims

Do **not** infer from this evidence that:

- T10 or Seagate invented disk scrubbing/background media verification in 2005;
- `Background Media Scan`, `scrub`, HDFS block scan, SMART self-test, and RAID rebuild are synonyms;
- a successful BMS pass proves future correctness or detects every possible corruption mode;
- every BMS-capable drive automatically reassigns every weak block;
- scan position is proven crash-durable or power-loss persistent;
- BMS result-log entries form a complete immutable lifetime history;
- a reassigned LBA means its previous physical sector has been securely erased;
- a drive-level BMS pass proves filesystem/application end-to-end integrity;
- the BMS interval is a magnetic-retention or bit-decay deadline;
- Western Digital 2024 behavior can be projected backward into Seagate 2007 or T10 2005 implementation history.

---

## Related-repository check

A fresh repository search for `background media scan SCSI` in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) returned no dedicated study during this slice.

If developed later, the broader history of disk read scrubbing, SMART/offline tests, SCSI standards revision genealogy, servo/media defect physics, and vendor firmware implementation belongs primarily in `computing-archaeology`. `technical-retention` should keep the bounded relation among **proactive inspection, foreground preemption, retained maintenance progress/evidence, and repair authority**.

---

## Remaining debt

- establish the exact first revision/date and ballot/integration path of T10/04-198 and 05-340 into final SPC/SBC standards;
- locate pre-2004 proprietary vendor and operating-system implementations named by primary sources;
- compare BMS with SMART offline collection/self-test using exact standards vocabulary;
- determine power-cycle/reset persistence of BMS progress and logs for named devices rather than infer it;
- inspect modern cross-vendor SAS products for repair-policy differences;
- obtain field/fault-injection evidence showing how BMS behaves under latent-sector errors, repeated foreground load, thermal halt, log-full conditions, and power loss;
- keep physical-sector remanence and secure sanitization as separate work.