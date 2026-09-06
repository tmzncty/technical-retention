# Host-Driven SCSI VERIFY: Medium Qualification, Byte Comparison, and Maintenance-Locus Boundary

## Scope

- **Object / system:** the SCSI `VERIFY (10)` command as evidenced by a September 1990 Toshiba SCSI-2 CD-ROM interface specification, T10's SCSI-2 publication record, a 1997 Seagate SCSI-2/SCSI-3 interface manual, and a September 2005 SBC-3 working draft continuity witness.
- **Retention question:** what changes when media qualification is explicitly requested by an initiator for a named logical-block range rather than being scheduled autonomously inside a drive (Case 101) or by a RAID controller's patrol policy (Case 102)?
- **Status:** `grounded`.

This is **not** a complete genealogy of SCSI VERIFY, WRITE AND VERIFY, host scrub utilities, T10 Background Medium Scan, RAID Patrol Read, parity checking, filesystem checksums, or media-error recovery. The bounded question is narrower:

> **What does a host-issued VERIFY request qualify, what does it not qualify, and where does scheduling/coverage responsibility remain?**

The project terms `host-driven verification`, `coverage policy`, `medium-readability qualification`, and `verification-currentness precondition` below are **engineering reconstructions**, not historical SCSI vocabulary.

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
- `CRC`, `ECC`, retry, and later protection information.

Do not silently rename one VERIFY request as `scrub`, `Patrol Read`, `Background Medium Scan`, or `Consistency Check`. A host program can build a sweep out of repeated VERIFY commands, but that scheduling layer is not identical to the command semantics.

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

T10 proposal `05-344r0`, carrying the 9 September 2005 SBC-3 Revision 0 text, says VERIFY (10) requests verification of specified logical blocks on the medium. It also requires logical units containing cache to write the referenced cached blocks to the medium before the verification, analogously to a range-scoped SYNCHRONIZE CACHE with `SYNC_NV=0`.

The same text states that Verify Error Recovery settings define the verification criteria where implemented, preserves `BYTCHK=0` medium verification without data comparison, and defines `BYTCHK=1` byte-by-byte comparison against data transferred from the application client while also checking protection information.

This later text makes another retention boundary visible:

> **the logical block selected for verification may have a newer cached embodiment than the medium embodiment that is about to be qualified.**

So in this 2005 bounded interface, the device first closes a currentness/persistence relation for the referenced range and then verifies the medium representation. This does **not** mean every earlier VERIFY implementation had identical cache semantics; the claim is explicitly revision-bounded.

---

## Retained state and maintenance relations

Case 103 exposes at least six separate relations.

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

---

## Cross-case comparison

### Case 101 — SCSI Background Medium Scan

Case 101's BMS is device-side background maintenance. It can retain progress/results and continue scanning without a host issuing one VERIFY request per range.

Case 103 is initiator-driven and range-scoped:

> **host-issued VERIFY ≠ drive-internal Background Medium Scan.**

Functional overlap in medium exercising does not establish BMS descent from VERIFY or vice versa.

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
- filesystem/data-integrity scrub.

The 1990 Toshiba source is an implementation/documentation floor, not an invention certificate. T10's 1993/1994 publication record is a standards-history node, not a universal origin. The 1997 Seagate and 2005 SBC-3 documents are continuity/semantic-deepening witnesses.

A fresh repository search found no dedicated SCSI VERIFY history in `tmzncty/computing-archaeology`; a broader command genealogy should be coordinated there rather than expanded opportunistically here.

---

## Engineering reconstruction

Case 103 adds these bounded relations:

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
13. `VERIFY range synchronization ≠ general write-durability closure`.

These are project analytical statements, not T10/Toshiba/Seagate historical terminology.

---

## Philosophical interpretation — bounded

Case 103 is useful because the same material medium can be **present, serviceable, and yet deliberately re-qualified** through a command that does not create a new user value. Verification produces evidence about continuation; it is not identical to continuation itself.

The stronger philosophical claim that verification somehow constitutes memory by observation is not supported. Technically, the narrower point is enough: **retention can depend on periodically or deliberately renewing confidence in an embodiment, while the scheduling authority for that confidence may sit at a different layer from the device that performs the check.**

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
- interaction with grown-defect reassignment and URE-aware array policy.

---

## Result

**Grounded.**

The 1990 Toshiba source establishes an early product-level SCSI-2-style host-issued VERIFY implementation; T10 anchors the later final SCSI-2 publication node; Seagate 1997 cleanly separates medium verification from expected-data comparison; and the 2005 SBC-3 draft exposes later cache-to-medium currentness closure before verification. Together they close the bounded **host-command maintenance-locus** slice without converting a command primitive into an autonomous scrub policy or a historical genealogy.
