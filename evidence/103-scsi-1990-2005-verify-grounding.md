# Evidence Record 103 — SCSI 1990–2005 VERIFY Grounding

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
