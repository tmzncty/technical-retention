# Host-Driven SCSI VERIFY: Medium Qualification, Byte Comparison, and Maintenance-Locus Boundary

## Scope

- **Object / system:** the SCSI `VERIFY (10)` command as evidenced by a September 1990 Toshiba SCSI-2 CD-ROM interface specification, T10's SCSI-2 publication record, a 1997 Seagate SCSI-2/SCSI-3 interface manual, a September 2005 SBC-3 working draft continuity witness, and a June 2022 Seagate command-reference negative control for VERIFY versus reassignment.
- **Retention question:** what changes when media qualification is explicitly requested by an initiator for a named logical-block range rather than being scheduled autonomously inside a drive (Case 101) or by a RAID controller's patrol policy (Case 102), and what repair authority does that qualification request *not* carry?
- **Status:** `grounded`.

This is **not** a complete genealogy of SCSI VERIFY, WRITE AND VERIFY, host scrub utilities, T10 Background Medium Scan, RAID Patrol Read, parity checking, filesystem checksums, bad-sector reassignment, or media-error recovery. The bounded question is narrower:

> **What does a host-issued VERIFY request qualify, what does it not qualify, where does scheduling/coverage responsibility remain, and how is verification evidence separated from remediation authority?**

The project terms `host-driven verification`, `coverage policy`, `medium-readability qualification`, `verification-currentness precondition`, and `remediation authority` below are **engineering reconstructions**, not historical SCSI vocabulary.

## Evidence navigation

- [SCSI VERIFY vs reassignment authority, 2001–2022](../evidence/103-scsi-2001-2022-verification-vs-remediation-authority-deepening.md) — adds a same-manual 2022 negative control: verify-medium operations do not trigger automatic read reassignment, while read operations may gain automatic-reallocation authority through `ARRE` and `REASSIGN BLOCKS` remains a separate remediation command; also brackets changing `REASSIGN BLOCKS` payload semantics in T10 records from 2001 to 2005.
- [T10 REASSIGN BLOCKS payload-protection transition, 2001–2004](../evidence/103-t10-2001-2004-reassign-payload-protection-transition-deepening.md) — tightens the direct standards-text transition from the older `listed-block data may be altered` rule in SBC-2 Revision 9 (May 2003) to the conditional recover-and-carry-forward rule in the final T10 SBC-2 Revision 16 (13 November 2004), while separately tracing the 03-176 → 03-365 end-to-end-protection proposal lineage and preserving proposal-versus-incorporated-text boundaries.

---

## Historical vocabulary

The inspected/indexed primary sources use terms including:

- `VERIFY (10)`;
- operation code `2Fh`;
- `medium (quality) verification` / `medium verification`;
- `BytChk` / `BYTCHK`;
- `byte-by-byte compare`;
- `MISCOMPARE`;
- `Logical Block Address`;
- `Verification Length`;
- `Verify Error Recovery` / read-recovery parameters;
- `CRC`, `ECC`, retry, and later protection information;
- `ARRE` / `Automatic Read Reallocation Enabled`;
- `REASSIGN BLOCKS`;
- `GLIST` / `PLIST`.

Do not silently rename one VERIFY request as `scrub`, `Patrol Read`, `Background Medium Scan`, or `Consistency Check`. A host program can build a sweep out of repeated VERIFY commands, but that scheduling layer is not identical to the command semantics.

Likewise, `verification evidence` and `remediation authority` are project terms. They are used to keep historically distinct SCSI operations from being collapsed into one generic notion of `disk checking`.

---

## Historical record

### H/P — a September 1990 Toshiba product interface already exposed optional VERIFY (10)

Toshiba's **CD-ROM SCSI Interface Specifications, Version 5.0**, dated September 1990, lists `VERIFY (10)` (`2Fh`) among commands newly added from Version 4.0. Section 5-3.19 says the command requests the CD-ROM to verify data on the installed medium. For this CD-ROM implementation, `BlkVfy` and `BytChk` are to be zero and the device supports **medium (quality) verification with no data comparison**.

The same section says verification performs the same operation as READ except that no data is transferred and only status is returned after verification. The device may execute ECC/retry error recovery when necessary and allowed, and the read-recovery parameters are also used as verification criteria.

This gives a conservative historical floor:

> **By September 1990, a vendor SCSI-2 interface document already implemented optional host-issued VERIFY semantics.**

It does **not** prove that Toshiba invented VERIFY, nor does it establish the date at which every SCSI-2 draft first acquired the command.

### H/P — T10's publication record separates working implementation chronology from final SCSI-2 publication

T10's SCSI-2 archive identifies final committee draft Revision 10L as dated **7 September 1993**, with status `Published`, and points to the approved standard as **X3.131:1994**.

The Toshiba 1990 witness therefore matters methodologically: a final 1994 standards designation must not be treated as the invention or first-implementation date of every command contained in that standard family.

> **final standard publication ≠ first implementation or first proposal.**

### H/P — Seagate 1997 separates medium verification from initiator-supplied byte comparison

Seagate's **Product Manual — Disc Drive SCSI-2/SCSI-3 Interface (Vol. 2; Ver. 2), Rev. H**, publication 77738479, August 1997, describes VERIFY using an explicit starting logical block and verification length.

Its `BytChk=0` path is a medium verification using mechanisms such as CRC/ECC **without data comparison**. Its `BytChk=1` path instead performs a byte-by-byte comparison between data on the medium and data transferred from the initiator; mismatch terminates with CHECK CONDITION / `MISCOMPARE`.

That is a crucial boundary:

> **media readability / codeword qualification ≠ equality to an initiator-retained expected value.**

The same command family can ask either question, but the evidence source and failure interpretation differ.

### H/P — one VERIFY command names an explicit range; it does not define a recurring coverage policy

Both the Toshiba and Seagate descriptions expose a start address and a verification length. The historical command is therefore request-scoped.

Nothing in these bounded command descriptions establishes:

- an automatic interval;
- an idle-time scheduler;
- a persistent whole-medium scan cursor;
- a promise that every block will eventually be visited;
- a RAID parity-consistency pass.

A host can issue commands over successive ranges, but that is a higher-level policy built from the primitive:

> **range-scoped verification capability ≠ autonomous whole-medium maintenance coverage.**

### H/P — the September 2005 SBC-3 draft makes a later cache/currentness precondition explicit

T10 document `05-344r0`, carrying the 9 September 2005 SBC-3 Revision 0 text, says VERIFY (10) requests verification of specified logical blocks on the medium. It also requires logical units containing cache to write the referenced cached blocks to the medium before the verification, analogously to a range-scoped SYNCHRONIZE CACHE with `SYNC_NV=0`.

The same text states that Verify Error Recovery settings define the verification criteria where implemented, preserves `BYTCHK=0` medium verification without data comparison, and defines `BYTCHK=1` byte-by-byte comparison against data transferred from the application client while also checking protection information.

This later text makes another retention boundary visible:

> **the logical block selected for verification may have a newer cached embodiment than the medium embodiment that is about to be qualified.**

So in this 2005 bounded interface, the device first closes a currentness/persistence relation for the referenced range and then verifies the medium representation. This does **not** mean every earlier VERIFY implementation had identical cache semantics; the claim is explicitly revision-bounded.

### H/P — Seagate 2022 explicitly separates verify error recovery from automatic read reassignment

Seagate's **_Serial Attached SCSI (SAS) SCSI Commands Reference Manual_, Rev. M**, dated June 2022, defines the `Verify Error Recovery` mode page for verify-medium operations, including `VERIFY` and the verify part of `WRITE AND VERIFY`. The page provides retry/recovery controls, but explicitly states that **verify-medium operations do not trigger automatic read reassignment**.

The same manual separately gives ordinary read operations an `ARRE` (`Automatic Read Reallocation Enabled`) control. With `ARRE=1`, automatic reallocation of defective logical blocks during read operations is enabled; the documented path performs reallocation only after successful data recovery and places the recovered data in the reallocated logical block.

This supplies a same-vendor, same-manual negative control:

```text
VERIFY error recovery
    !=
automatic read reassignment

ordinary READ + ARRE authority
    may perform automatic reallocation after successful recovery
```

The difference is not merely foreground versus background scheduling. It is a difference in the **repair authority attached to the operation class**.

### H/P — explicit REASSIGN BLOCKS remains a separate remediation path in the same 2022 manual

The June 2022 Seagate command reference separately documents `REASSIGN BLOCKS`: the application supplies defective LBAs, the device reassigns the medium used for those logical blocks, and recoverable user/protection data are carried to the reassigned block. If recovery fails, the command uses vendor-specific user data rather than pretending the prior value was recovered.

Therefore the current command reference exposes three separable roles:

```text
VERIFY
    -> bounded qualification / error evidence

READ with ARRE enabled
    -> read-path recovery may gain automatic-reallocation authority

REASSIGN BLOCKS
    -> explicit defect-remediation command
```

This does not prove undocumented firmware never performs other maintenance. It establishes the public interface contract documented by Seagate.

### H/P — T10 records show that the REASSIGN payload contract itself must be dated

A T10 proposal from **11 July 2001**, `01-210r0`, says data in logical blocks listed for reassignment **may be altered**, while all other blocks are preserved. By the **9 September 2005** SBC-3 Revision 0 draft, the text instead says that if the device can recover user data and protection information from the original logical block, it shall carry that recovered information to the reassigned logical block; if recovery is impossible, vendor-specific user data are used.

The exact accepted proposal or revision at which this wording changed has not yet been identified. The safe conclusion is narrower:

> **same command name across standards-development eras ≠ identical payload-preservation contract.**

This matters to Case 103 because a transition from `verification evidence` to `repair` cannot be analyzed merely by seeing the word `REASSIGN`; the dated command semantics still matter.

Detailed record: [`../evidence/103-scsi-2001-2022-verification-vs-remediation-authority-deepening.md`](../evidence/103-scsi-2001-2022-verification-vs-remediation-authority-deepening.md). The newer [`../evidence/103-t10-2001-2004-reassign-payload-protection-transition-deepening.md`](../evidence/103-t10-2001-2004-reassign-payload-protection-transition-deepening.md) tightens the directly observed standards-text bracket to **SBC-2 Revision 9 (May 2003) → Revision 16 (13 November 2004)** and separately traces the proposal-stage protection-information work without claiming an exact first incorporated revision.

---

## Retained state and maintenance relations

Case 103 exposes at least seven separate relations.

### 1. Current logical payload

The initiator names logical blocks whose current value is the retention target.

### 2. Medium embodiment

VERIFY asks the device to exercise the medium representation rather than merely return cached user data.

### 3. Device-local verification evidence

ECC/CRC, retry behavior, and later protection-information checks can qualify whether the medium representation satisfies the device's verification criteria.

### 4. Optional external expected value

With byte checking enabled in the bounded Seagate/later SBC text, initiator-supplied bytes add a separate equality witness. That witness is not created by the medium itself.

### 5. Request scope

LBA plus verification length define which logical blocks this command attempts to qualify.

### 6. Higher-level coverage policy

Whether an operator/tool repeats VERIFY across a whole device, how often, with what throttling, and how it persists progress belongs above the command in this case.

### 7. Remediation authority

A verification path can have retry/correction policy without having relocation authority. The 2022 Seagate manual makes that boundary explicit by denying automatic read reassignment to verify-medium operations while separately exposing `ARRE` for reads and `REASSIGN BLOCKS` as an explicit remediation command.

---

## Cross-case comparison

### Case 101 — SCSI Background Medium Scan

Case 101's BMS is device-side background maintenance. It can retain progress/results and continue scanning without a host issuing one VERIFY request per range.

Case 103 is initiator-driven and range-scoped:

> **host-issued VERIFY ≠ drive-internal Background Medium Scan.**

The November 2005 BMS proposal is useful because its `REASSIGN STATUS` distinguishes pending remediation, successful device action, rewrite-in-place, application-client reassignment, and failed paths. That is proposal-bounded standards-development evidence, not proof every final product implemented every status.

Functional overlap in medium exercising does not establish BMS descent from VERIFY or vice versa.

### Case 14 — SCSI defect reassignment

Case 14 owns the logical-identity / physical-replacement problem. Case 103 now supplies the upstream negative control:

```text
qualify an embodiment
    !=
replace an embodiment
    !=
preserve the prior value across replacement
```

The 2022 Seagate manual directly separates VERIFY from automatic read reassignment; the T10 transition is now directly bracketed more tightly by **SBC-2 Revision 9 (May 2003)** and the final committee **Revision 16 (13 November 2004)**, warning that even `REASSIGN BLOCKS` cannot be treated as one timeless payload-preservation contract.

> **verification evidence ≠ reassignment ≠ guaranteed payload recovery.**

### Case 102 — PERC / MegaRAID Patrol Read

Case 102 moves proactive checking into a RAID controller with an automatic/manual patrol policy and separately defined Consistency Check.

Case 103 stays at the block-command boundary:

> **VERIFY capability ≠ Patrol Read scheduling policy.**

and:

> **medium verification ≠ RAID parity consistency.**

A controller may use lower-layer reads or verify-like operations internally, but this case does not infer the implementation of Dell/LSI Patrol Read from the shared function.

### Case 87 — SCSI cache durability

Case 87 owns WRITE BACK / FUA / SYNCHRONIZE CACHE durability semantics. The 2005 SBC-3 VERIFY rule adds a narrow composition point: referenced dirty cached blocks are pushed to medium before that range is verified.

Therefore:

> **VERIFY's range precondition ≠ a general replacement for SYNCHRONIZE CACHE or FUA.**

It explains what medium image the verification is about; it does not establish unrelated writes as durable.

### Cases 18 / 27 / Synthesis 08

ZFS/Ceph-style scrub can qualify higher-layer checksums, versions, placement, and repair sources. SCSI VERIFY can qualify medium readability and, with byte checking, equality to supplied bytes for the selected range.

> **device-medium qualification ≠ end-to-end object/current-version integrity authority.**

The shared pattern `check before ordinary demand exposes a fault` is a functional analogy, not a genealogy.

---

## Prior-art and genealogy boundary

This case makes no priority claim for:

- media verification generally;
- SCSI VERIFY before September 1990;
- host disk scrubbing;
- disk surface scans;
- SCSI WRITE AND VERIFY;
- T10 Background Medium Scan;
- RAID Patrol Read / Media Patrol;
- filesystem/data-integrity scrub;
- bad-sector reassignment or automatic reallocation.

The 1990 Toshiba source is an implementation/documentation floor, not an invention certificate. T10's 1993/1994 publication record is a standards-history node, not a universal origin. The 1997 Seagate and 2005 SBC-3 documents are continuity/semantic-deepening witnesses. The 2022 Seagate manual is later interface-contract evidence, not evidence of what every earlier drive did.

A fresh repository search again found no dedicated SCSI VERIFY / REASSIGN BLOCKS / Background Medium Scan history in `tmzncty/computing-archaeology`; a broader command and HDD defect-management genealogy should be coordinated there rather than expanded opportunistically here.

---

## Engineering reconstruction

Case 103 now supports these bounded relations:

1. `host-issued verification ≠ autonomous background scan`;
2. `verification command ≠ maintenance schedule`;
3. `specified LBA range ≠ whole-medium coverage`;
4. `medium verification ≠ initiator-supplied byte comparison`;
5. `successful medium verification ≠ RAID redundancy consistency`;
6. `successful medium verification ≠ end-to-end current-version/checksum authority`;
7. `verification result ≠ repair completion`;
8. `verification criteria ≠ universal payload-correctness oracle`;
9. `no payload transfer to initiator ≠ no medium read / no physical work`;
10. `verification capability ≠ Patrol Read implementation genealogy`;
11. `SCSI-2 final publication ≠ invention of VERIFY`;
12. `verification target selection ≠ pre-existing medium currentness` in the explicitly bounded 2005 cached-unit rule;
13. `VERIFY range synchronization ≠ general write-durability closure`;
14. `verify error recovery ≠ automatic read reassignment` in the bounded 2022 Seagate contract;
15. `same LBA + different command path ≠ same remediation authority`;
16. `successful recovery during VERIFY ≠ evidence of physical relocation`;
17. `same command name across revisions ≠ identical payload-preservation contract`;
18. `proposal-stage protection intent ≠ incorporated command text`;
19. `logical-address continuity ≠ unconditional old-payload recovery even after the stronger Revision 16 contract`.

These are project analytical statements, not T10/Toshiba/Seagate historical terminology.

---

## Philosophical interpretation — bounded

Case 103 is useful because the same material medium can be **present, serviceable, and yet deliberately re-qualified** through a command that does not create a new user value. Verification produces evidence about continuation; it is not identical to continuation itself.

The 2022 negative control makes the distinction sharper: the same system can grant one operation error-recovery work without granting it automatic relocation authority. A retained object can therefore be **tested** without the test itself becoming the operation that changes its physical embodiment.

The stronger philosophical claim that verification somehow constitutes memory by observation is not supported. Technically, the narrower point is enough:

> **retention can depend on renewing confidence in an embodiment, while the authority to schedule that test and the authority to replace the embodiment remain separate relations.**

---

## Evidence limits / future work

Still open:

- direct revision-by-revision archaeology of SCSI-2 drafts before Revision 10L to locate VERIFY's exact standardization introduction;
- direct page-image inspection of the Toshiba 1990 facsimile if the archive becomes renderable; current claims use the indexed primary text and exact section/page locator;
- full SCSI-1 / CCS / vendor-pre-SCSI-2 verification genealogy;
- WRITE AND VERIFY versus separate WRITE + VERIFY history;
- named host utilities that build persistent whole-device sweeps from VERIFY;
- cross-vendor disk/controller use of VERIFY internally;
- empirical fault injection for recovered, medium-error, and MISCOMPARE outcomes;
- direct inspection of SBC-2 Revisions 10–15b to identify the **first exact revision** that changed `REASSIGN BLOCKS` from the older `data may be altered` wording to the conditional recover-and-carry-forward rule; the current direct-text bracket is Revision 9 → Revision 16;
- identification of the exact T10 motion / incorporated proposal that changed the `REASSIGN BLOCKS` command text, rather than inferring it from the broader 03-176/03-365 protection proposal family;
- a named-drive trace that captures VERIFY failure followed by host-selected `REASSIGN BLOCKS`, write-driven relocation, or another remediation path;
- cross-vendor product evidence on whether verify-medium operations can trigger relocation.

The former broad debt `interaction with grown-defect reassignment` is therefore **partly closed at the public interface-contract level** by the 2022 Seagate negative control. The standards-transition debt is also narrowed from a 2001→2005 bracket to **SBC-2 Revision 9 (May 2003) → Revision 16 (November 2004)**, with proposal-stage lineage recovered. Product traces and the exact first incorporated revision remain open.

---

## Source and inspection notes

Primary sources used by the reassignment deepening now include:

1. T10 `01-210r0`, **_Reassign Blocks 2 TBytes Support_**, 11 July 2001.  
   <https://www.t10.org/ftp/t10/document.01/01-210r0.pdf>
2. T10 SBC-2 project page, Project 1417-D / INCITS 405.  
   <https://www.t10.org/members/w_sbc2.htm>
3. T10 `03-176r0`, **_End-to-End Data Protection_**, 1 May 2003.  
   <https://www.t10.org/ftp/t10/document.03/03-176r0.pdf>
4. T10 `03-371r0`, **_SCSI Commands, Architecture, & Protocol Working Group Meeting -- November 4-5, 2003_**, 6 November 2003.  
   <https://www.t10.org/ftp/t10/document.03/03-371r0.pdf>
5. T10 `04-114r0`, **_SBC-2 Option to Check Only the Logical Block Guard_**, 18 April 2004.  
   <https://www.t10.org/ftp/t10/document.04/04-114r0.pdf>
6. T10 `05-344r0`, **_Working Draft SCSI Block Commands - 3 (SBC-3), Revision 0_**, 9 September 2005.  
   <https://t10.org/ftp/t10/document.05/05-344r0.pdf>
7. T10 `05-340r2`, **_SBC-3 SPC-4 Background scan additions_**, 11 November 2005.  
   <https://www.t10.org/ftp/t10/document.05/05-340r2.pdf>
8. Seagate Technology LLC, **_Serial Attached SCSI (SAS) SCSI Commands Reference Manual_**, Publication 100293068, Rev. M, June 2022.  
   <https://www.seagate.com/content/dam/seagate/migrated-assets/staticfiles/support/docs/manual/Interface%20manuals/100293068m.pdf>

The 2001, May-2003, November-2003, and April-2004 T10 PDFs were inspected with page-preserving text and rendered page images during the new pass. The Revision 9 and Revision 16 command texts are taken from indexed surviving copies; official T10 project/working-draft pages independently establish the revision sequence, date metadata, final-draft status, and INCITS 405-2005 mapping. Revision 9 preserves a cover-date/project-list-date discrepancy (25 May versus 31 May 2003) rather than silently normalizing it.

---

## Result

**Grounded.**

The 1990 Toshiba source establishes an early product-level SCSI-2-style host-issued VERIFY implementation; T10 anchors the later final SCSI-2 publication node; Seagate 1997 cleanly separates medium verification from expected-data comparison; and the 2005 SBC-3 draft exposes later cache-to-medium currentness closure before verification.

The 2022 Seagate evidence closes a further boundary at the command-contract level: **verify-medium operations can perform real error-recovery work without gaining automatic read-reassignment authority**. Ordinary reads may receive that authority through `ARRE`, while explicit `REASSIGN BLOCKS` remains a separate remediation command. The new standards-history deepening further shows that `REASSIGN BLOCKS` itself did not have one timeless payload-preservation contract: the older wording is still present in SBC-2 Revision 9 in May 2003, proposal work in 2003 explicitly brings valid protection information into reassignment semantics, and final T10 SBC-2 Revision 16 of 13 November 2004 requires recoverable user data and protection information to be carried into the reassigned logical block. The exact first incorporated revision remains deliberately open.