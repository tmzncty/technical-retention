from pathlib import Path

CASE_PATH = Path('cases/103-scsi-verify-host-driven-medium-qualification.md')
EVIDENCE_PATH = Path('evidence/103-scsi-1990-2005-verify-grounding.md')
ROADMAP_PATH = Path('ROADMAP.md')
INDEX_PATH = Path('CASE_INDEX.md')

case_text = r'''# Host-Driven SCSI VERIFY: Medium Qualification, Byte Comparison, and Maintenance-Locus Boundary

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
'''

evidence_text = r'''# Evidence Record 103 — SCSI 1990–2005 VERIFY Grounding

## Purpose

Ground [`cases/103-scsi-verify-host-driven-medium-qualification.md`](../cases/103-scsi-verify-host-driven-medium-qualification.md) with period/primary documentation for host-issued SCSI VERIFY semantics and a conservative standardization timeline.

The record supports only a bounded claim set: explicit range-scoped verification, medium verification without data comparison, optional expected-data comparison, device-defined recovery criteria, and a later cache-to-medium precondition. It does **not** establish invention priority or a full VERIFY/BMS/Patrol-Read genealogy.

---

## Source 1 — Toshiba, September 1990

**Document:** *TOSHIBA CD-ROM SCSI Interface Specifications, Ver. 5.0*  
**Date:** September 1990  
**Archive:** Bitsavers  
**URL:** <https://www.bitsavers.org/pdf/toshiba/cdrom/Toshiba_CD-ROM_SCSI-2_Interface_Specifications_Version_5.0_Sep90.pdf>  
**Locator:** Appendix A (`VERIFY (10)` listed among commands newly added from Ver. 4.0); §5-3.19, printed p. 67.

### Directly supported

- `VERIFY (10)` operation code is `2Fh`.
- The command requests verification of data on the installed CD-ROM medium.
- This product directs `BlkVfy` and `BytChk` to zero.
- It supports medium-quality verification without data comparison.
- Verification executes the same operation as READ except that data are not transferred to the initiator; status is returned after verification.
- ECC/retry recovery may be used where necessary/allowed.
- Read-recovery parameters also serve as verification criteria.
- LBA/address and verification length scope the requested work.

### Evidence handling note

The archive was text-indexed and the exact §5-3.19 / p. 67 content was recoverable through search, but the PDF endpoint did not render successfully in the current browser path. Therefore this record makes **text/locator claims only** and no visual-layout/facsimile claim.

### Does not support

- Toshiba invention priority;
- first appearance of VERIFY in a SCSI committee draft;
- magnetic-disk behavior;
- autonomous background scheduling;
- byte-comparison behavior for this specific CD-ROM implementation (the bits are explicitly constrained to zero).

---

## Source 2 — T10 SCSI-2 archive / publication record

**Page:** T10 X3T9.2 documents / SCSI-2 archive  
**URL:** <https://www.t10.org/x3t9_2.htm>  
**Locator:** `SCSI-2 Small Computer System Interface - 2 (SCSI-2)` entry.

### Directly supported

- final committee draft Revision `10L` is dated **1993-09-07**;
- status is `Published`;
- T10 identifies the approved SCSI-2 standard as **X3.131:1994** (later reaffirmed).

### Methodological use

This is a standards-publication anchor only. Combined with the Toshiba September 1990 product witness, it blocks any inference that a 1994 final-standard date is automatically the invention or first product-use date of VERIFY.

---

## Source 3 — Seagate, August 1997

**Document:** *Product Manual — Disc Drive SCSI-2/SCSI-3 Interface (Vol. 2; Ver. 2), Rev. H*  
**Publication:** 77738479 Rev H  
**Date:** August 1997  
**Archive:** Bitsavers mirror  
**URL:** <https://bitsavers.trailing-edge.com/pdf/seagate/scsi/77738479H_SCSI-2_SCSI-3_Interface_Product_Manual_Volume_2_Version_2.pdf_199708.pdf>  
**Locators:** printed pp. 190–191 / PDF pp. 199–200 around VERIFY notes.

### Directly supported

- `BytChk=0` performs medium verification using CRC/ECC-style checking with no data comparison.
- `BytChk=1` performs a byte-by-byte comparison of medium data with data transferred from the initiator.
- mismatch returns CHECK CONDITION with sense key `MISCOMPARE`.
- the logical block address identifies where VERIFY begins and verification length identifies a contiguous range.
- Verify Error Recovery parameters govern verification criteria where supported.

### Evidence boundary

The accessible PDF text was directly indexed; the page-image fetch from the Seagate host was unreliable, so the record relies on the archived text and precise page locators rather than visual reconstruction.

---

## Source 4 — T10 `05-344r0`, September 2005

**Document:** Proposed SBC-3 Revision 00 / embedded *Working Draft SCSI Block Commands - 3 (SBC-3), Revision 0*  
**Date:** proposal 12 September 2005; embedded draft dated 9 September 2005  
**URL:** <https://t10.org/ftp/t10/document.05/05-344r0.pdf>  
**Locator:** §5.20 `VERIFY (10) command`, printed p. 65 / PDF p. 80.

### Directly inspected

The rendered page directly shows:

- VERIFY requests the device server to verify specified logical blocks on the medium;
- cached referenced logical blocks are written to the medium first, analogous to range-scoped SYNCHRONIZE CACHE with `SYNC_NV=0`;
- Verify Error Recovery settings define verification criteria when implemented, otherwise criteria are vendor-specific;
- `BYTCHK=0` performs medium verification with no data comparison and checks applicable protection information;
- `BYTCHK=1` compares user data read from the medium with data transferred from the data-out buffer and also checks/compares protection information.

### Evidence boundary

This is a **2005 working-draft continuity witness**, not evidence that every 1990/1994 implementation had identical cache or protection-information rules. Do not project its later semantics backward.

---

## Cross-source claim ledger

| Claim | Label | Support | Boundary |
| --- | --- | --- | --- |
| September 1990 Toshiba documentation implements optional VERIFY (10) | `H/P` | Source 1 | product/document floor, not invention priority |
| final SCSI-2 committee draft 10L dates to 1993-09-07; approved designation X3.131:1994 | `H/P` | Source 2 | publication history only |
| medium verification can occur without initiator-data comparison | `H/P` | Sources 1, 3, 4 | criteria remain device/revision scoped |
| later VERIFY can optionally compare medium data with initiator-supplied expected data | `H/P` | Sources 3, 4 | Toshiba CD-ROM source explicitly does not use this mode |
| one VERIFY names an LBA/range rather than an autonomous schedule | `H/P` | Sources 1, 3, 4 | host tooling may build a sweep above it |
| 2005 cached units synchronize referenced blocks to medium before verify | `H/P` | Source 4 | do not project backward |
| VERIFY is not BMS, Patrol Read, parity Consistency Check, or end-to-end scrub | `E/A` | cross-case comparison | functional/layer distinction, not historical vocabulary |
| SCSI-2 final publication invented VERIFY | `X` | contradicted by Source 1 chronology | rejected |
| VERIFY capability proves whole-medium recent coverage | `X` | request-scoped command semantics | rejected |

---

## Related-repository check

A fresh default-branch search of `tmzncty/computing-archaeology` for `SCSI VERIFY` found no dedicated case to reuse. The broad SCSI-command genealogy remains a good candidate for that repository; this evidence record retains only the technical-retention slice.

---

## Result

The evidence supports `grounded` status for the bounded host-driven VERIFY relation. Strongest claims are source-local and period-specific; the engineering synthesis is explicitly separated from genealogy and from later autonomous maintenance mechanisms.
'''

findings = r'''## Case 103 — Host-Driven SCSI VERIFY findings

1532. **host-issued verification ≠ autonomous background scan** — VERIFY performs work because an initiator requests a named range; Case 101 BMS retains an internal background-scan regime and Case 102 Patrol Read adds a controller maintenance policy.
1533. **verification command ≠ maintenance schedule** — possession of VERIFY semantics does not itself establish cadence, idle-time scheduling, persistent scan progress, or automatic recurrence.
1534. **specified LBA range ≠ whole-medium coverage** — a successful command qualifies only its requested scope; whole-device coverage requires a higher-level sweep policy and completion evidence.
1535. **medium verification ≠ initiator-supplied byte comparison** — Seagate/T10 preserve a no-data-comparison medium check and a distinct BYTCHK path that compares against bytes retained/provided by the initiator.
1536. **successful medium verification ≠ RAID redundancy consistency** — exercising one medium representation does not establish agreement between mirrored/parity members; Case 102 Consistency Check owns that separate relation.
1537. **successful medium verification ≠ end-to-end current-version/checksum authority** — device-local CRC/ECC/recovery criteria do not establish that a higher-layer object version, mapping, checksum, or replica cohort is the authoritative current state.
1538. **verification result ≠ repair completion** — detecting or recovering through a read path does not by itself establish reassignment, rewrite, redundancy restoration, or future-margin renewal.
1539. **verification criteria ≠ universal payload-correctness oracle** — recovery mode parameters and vendor/revision-specific criteria define what the device tests; a pass is relative to that contract and scope.
1540. **no payload transfer to initiator ≠ no medium read / no physical work** — Toshiba explicitly describes VERIFY as READ-like device work with data transfer suppressed, so interface silence is not maintenance absence.
1541. **VERIFY capability ≠ Patrol Read implementation genealogy** — a RAID controller may expose a functionally similar proactive media test, but shared purpose does not prove that Dell/LSI Patrol Read is implemented as host-visible SCSI VERIFY or descends from it.
1542. **SCSI-2 final publication ≠ invention of VERIFY** — T10 dates final draft 10L to 1993 and X3.131 to 1994, while Toshiba already documents a SCSI-2-style VERIFY implementation in September 1990.
1543. **verification target selection ≠ pre-existing medium currentness** — the 2005 SBC-3 draft requires referenced dirty cached blocks to reach the medium before that range is verified, exposing currentness closure as a precondition to medium qualification in that revision.
1544. **VERIFY range synchronization ≠ general write-durability closure** — the 2005 precondition applies to referenced blocks for the verification operation and does not replace the broader FUA/SYNCHRONIZE CACHE contracts grounded in Case 87.
1545. **SCSI VERIFY comparison ≠ historical genealogy among BMS, Patrol Read, scrub, or Consistency Check** — Cases 101–103 support a maintenance-locus comparison only; device, host, controller, and higher-layer verification regimes retain different vocabularies, authorities, and scopes.'''

# New research files.
for path, text in ((CASE_PATH, case_text), (EVIDENCE_PATH, evidence_text)):
    if path.exists():
        raise SystemExit(f'{path} already exists')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + '\n', encoding='utf-8')

# ROADMAP: close the bounded host-command slice and remove stale “host SCSI VERIFY” blockers from 101/102.
roadmap = ROADMAP_PATH.read_text(encoding='utf-8')
if 'Host-driven SCSI VERIFY / explicit-range medium-qualification boundary' in roadmap:
    raise SystemExit('ROADMAP already contains Case 103 bullet')
lines = roadmap.splitlines()
case101_idxs = [i for i, line in enumerate(lines) if line.startswith('- [x] SCSI Background Medium Scan / proactive medium-readability boundary —')]
case102_idxs = [i for i, line in enumerate(lines) if line.startswith('- [x] Dell PERC / LSI MegaRAID Patrol Read versus Consistency Check boundary —')]
if len(case101_idxs) != 1 or len(case102_idxs) != 1:
    raise SystemExit(f'Unexpected roadmap anchors: Case101={len(case101_idxs)} Case102={len(case102_idxs)}')
lines[case101_idxs[0]] = lines[case101_idxs[0]].replace(
    'host SCSI VERIFY history, broader cross-vendor Patrol Read/Consistency Check genealogy beyond Case 102, field fault injection, and URE-aware policy remain open and should be coordinated with `computing-archaeology`.',
    'host sweep/application tooling above the bounded Case 103 VERIFY command, broader cross-vendor Patrol Read/Consistency Check genealogy beyond Case 102, field fault injection, and URE-aware policy remain open and should be coordinated with `computing-archaeology`.'
)
lines[case102_idxs[0]] = lines[case102_idxs[0]].replace(
    'host SCSI VERIFY, other controller families/cross-vendor terminology history, field fault injection, and URE-aware policy remain open.',
    'host sweep/application tooling above bounded Case 103 VERIFY semantics, other controller families/cross-vendor terminology history, field fault injection, and URE-aware policy remain open.'
)
case103_bullet = '- [x] Host-driven SCSI VERIFY / explicit-range medium-qualification boundary — [`cases/103-scsi-verify-host-driven-medium-qualification.md`](cases/103-scsi-verify-host-driven-medium-qualification.md), grounded by [`evidence/103-scsi-1990-2005-verify-grounding.md`](evidence/103-scsi-1990-2005-verify-grounding.md), uses a September 1990 Toshiba SCSI-2 CD-ROM interface, T10\'s SCSI-2 publication record, Seagate\'s August 1997 SCSI-2/SCSI-3 interface manual, and a directly rendered September 2005 SBC-3 draft to separate initiator-issued range qualification, medium verification without data comparison, optional expected-data byte comparison, recovery criteria, and the later cache-to-medium currentness precondition. This closes the bounded host-command maintenance-locus slice without turning one VERIFY request into an autonomous scrub policy or claiming SCSI-2 invention priority; pre-SCSI-2 command genealogy, named host whole-device sweep tooling, cross-vendor controller history, and fault injection remain open.'
# Recompute Case102 index after edits and insert after it.
case102_i = [i for i, line in enumerate(lines) if line.startswith('- [x] Dell PERC / LSI MegaRAID Patrol Read versus Consistency Check boundary —')][0]
lines.insert(case102_i + 1, case103_bullet)
ROADMAP_PATH.write_text('\n'.join(lines).rstrip('\n') + '\n', encoding='utf-8')

# CASE_INDEX: insert status/navigation row after Case 102 and append numbered findings.
index = INDEX_PATH.read_text(encoding='utf-8')
if '## Case 103 — Host-Driven SCSI VERIFY findings' in index:
    raise SystemExit('CASE_INDEX already contains Case 103 findings')
idx_lines = index.splitlines()
row_idxs = [i for i, line in enumerate(idx_lines) if 'cases/102-perc-megaraid-patrol-read-consistency-boundary.md' in line and line.startswith('| [')]
if len(row_idxs) != 1:
    raise SystemExit(f'Expected one Case 102 navigation row, got {len(row_idxs)}')
row = '| [Host-Driven SCSI VERIFY: Medium Qualification, Byte Comparison, and Maintenance-Locus Boundary](cases/103-scsi-verify-host-driven-medium-qualification.md) | **grounded** | initiator-issued range-scoped medium verification + optional expected-data comparison + device recovery criteria | separate host-command verification from autonomous BMS/controller patrol, medium qualification from expected-data comparison, and command scope from maintenance coverage policy | [1990–2005 Toshiba/Seagate/T10 grounding](evidence/103-scsi-1990-2005-verify-grounding.md); pre-SCSI-2 genealogy, named host sweep tooling, controller lineage, and fault injection remain open |'
idx_lines.insert(row_idxs[0] + 1, row)
index = '\n'.join(idx_lines).rstrip('\n')
last = index.splitlines()[-1]
if not last.startswith('1531. **media readability ≠ parity consistency ≠ end-to-end checksum integrity**'):
    raise SystemExit(f'Unexpected CASE_INDEX tail before Case 103: {last[:180]}')
INDEX_PATH.write_text(index + '\n\n' + findings.rstrip() + '\n', encoding='utf-8')
