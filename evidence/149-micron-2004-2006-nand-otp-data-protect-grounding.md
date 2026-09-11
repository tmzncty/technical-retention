# Evidence 149 — Micron 2004–2006 NAND OTP data-protect grounding

## Purpose

Ground Case 149 at the raw-NAND product/interface layer and prevent six common shortcuts:

1. treating `one-time programmable` as exactly one program command;
2. treating `unprotected` as equivalent to `erasable`;
3. treating payload programming and irreversible protection as one state transition;
4. treating permanent write protection as confidentiality or sanitization;
5. treating a broad Micron patent embodiment as proof of the exact shipped product implementation;
6. treating Micron's 2006 product witness as invention priority for flash OTP.

This record separates historical primary claims (`H/P`), mirrored-primary product evidence (`H/P*`), engineering reconstruction (`E`), functional analogy (`A`), and stop conditions/counterclaims (`X`).

---

## Source ledger

### S1 — Micron 2Gb, 4Gb, 8Gb x8/x16 NAND Flash Memory, Rev. D 12/06 (`H/P*`)

- Manufacturer: Micron Technology, Inc.
- Document: `2Gb, 4Gb, 8Gb: x8, x16 NAND Flash Memory`.
- Revision: **Rev. D 12/06 EN**; footer carries ©2005 Micron Technology, Inc.
- Preserved HTML transcription/mirror: <https://www.yumpu.com/en/document/view/40037130/nand-flash-datasheet-micron>
- Relevant section: `One-Time Programmable (OTP) Area`, including `OTP DATA PROGRAM A0h-10h`, `OTP DATA PROTECT A5h-10h`, and `OTP DATA READ AFh-30h`.
- Why `H/P*`: the text is a period Micron datasheet, but this run did not recover the exact revision from an origin-hosted Micron URL. The mirror is used as a faithful product-document witness, not promoted to stronger provenance than available.

Relevant statements preserved by S1:

- ten full OTP pages are available and guaranteed good;
- the OTP area leaves the factory unwritten (`1`s);
- programming/partial programming changes only `1` bits toward `0`;
- the OTP area cannot be erased whether protected or not;
- programming and protection are discrete operations so data can be programmed/verified before permanent protection;
- after `OTP DATA PROTECT`, pages are no longer programmable and cannot be unprotected;
- OTP pages remain readable whether protected or not;
- protection is considered established after the protect operation receives good status confirmation.

### S2 — Micron `Non-volatile one time programmable memory` patent family (`H/P`)

- Assignee: Micron Technology, Inc.
- Inventors: Benjamin Louie; Ebrahim Abedifard.
- Original family application: US10/933,205.
- Filing / priority anchor: **2-Sep-2004**.
- First listed publication: `US20060044893A1`, **2-Mar-2006**.
- Grant in that branch: `US7239552B2`, 3-Jul-2007.
- Family/continuation page used: <https://patents.google.com/patent/US7852681B2/en>

Relevant disclosed mechanisms:

- flash memory can contain OTP blocks;
- a verify operation can detect programming and inhibit further programming/erasing;
- alternatively, a block can remain program/erase capable until a predetermined page or lock bit is programmed, after which the block is locked;
- one described embodiment uses NAND flash architecture, while the disclosure says it is not limited to NAND;
- the background explicitly recognizes earlier NOR-type flash OTP areas.

Chronology guardrail:

> `2-Sep-2004 filing/priority != 2-Sep-2004 public disclosure`.

For public-document chronology this record uses the **2-Mar-2006** publication as the safer disclosure anchor.

### S3 — AMD/Fujitsu `US6662262B1`, OTP sector double protection (`H/P`)

- Title: `OTP sector double protection for a simultaneous operation flash memory`.
- Assignees: Advanced Micro Devices, Inc.; Fujitsu Limited.
- Filing: **19-Oct-1999**.
- Patent date/publication: **9-Dec-2003**.
- Google Patents: <https://patents.google.com/patent/US6662262B1/en>
- Additional bibliographic witness: <https://patents.justia.com/patent/6662262>

Relevant mechanism:

- OTP write-protect CAM records write-protection;
- an OTP sector lock CAM can lock that write-protect CAM in its programmed state;
- the resulting OTP sector is designated read-only.

Use: earlier same-medium prior art against a Micron invention-priority claim.

Stop condition: S3 does **not** prove direct genealogy into Micron's NAND OTP feature, nor the same circuit structure.

### S4 — Micron Product Security Center (`H/P`, current continuity witness)

- Organization: Micron Technology, Inc.
- URL: <https://www.micron.com/about/company/product-security-center>
- Current wording: Micron says NAND devices provide an OTP area outside the main flash array where customers can program unique data, and that OTP functionality allows the host to lock programmed data against modification.

Use: shows that Micron still distinguishes ordinary NAND array behavior from an OTP region and describes locking as protection against modification.

Stop condition: current marketing/security documentation cannot establish the exact 2006 command bytes, page count, or implementation.

### S5 — Micron Nonvolatile Memory Security page (`H/P`, current taxonomy witness)

- Organization: Micron Technology, Inc.
- URL: <https://www.micron.com/products/nonvolatile-memory-security>
- Current taxonomy distinguishes one-time programming / OTP space from volatile lock, nonvolatile lock, password protection, sanitize, and secure removal.

Use: later first-party evidence that `OTP`, access locking, and sanitization are distinct security/retention categories in Micron's own vocabulary.

Stop condition: current taxonomy is not back-projected as period-2006 wording.

---

## Claim-by-claim grounding

### C1 — 2006 product-level public floor

**Claim (`H/P*`):** by Rev. D 12/06 Micron documented a NAND OTP area with separate program, protect, and read operations.

**Evidence:** S1.

**Boundary (`X`):** this is a public/product-document floor, not an invention date. S2 and S3 already show earlier OTP-related flash work.

### C2 — Factory state and one-way bit programming

**Claim (`H/P*`):** S1 says the OTP area leaves the factory unwritten with all bits at `1`, and programming can program only `0` bits.

**Conclusion (`E`):** permitted payload evolution is directional even before global protection.

### C3 — Unprotected does not mean erasable

**Claim (`H/P*`):** S1 explicitly says the OTP area cannot be erased whether or not it is protected.

**Conclusion (`E`):** `unprotected != erasable`; erase authority and further-program authority are separate.

### C4 — `OTP` does not mean exactly one program command

**Claim (`H/P*`):** S1 allows an entire OTP page to be programmed or partial-page programming sequences before final protection, and other OTP pages may be programmed similarly.

**Conclusion (`E`):** `one-time programmable != exactly one host program invocation`.

The relevant invariant is the allowed direction/future transition set, not a literal command count of one.

### C5 — Program and protect are distinct transitions

**Claim (`H/P*`):** S1 explicitly describes OTP programming and protection as two discrete operations, with program/verify before permanent protection.

**Conclusions (`E`):**

- `programmed != protected`;
- `payload state != future-mutation authority`.

### C6 — Protect is irreversible in the bounded product interface

**Claim (`H/P*`):** after protection, S1 says OTP pages can no longer be programmed and cannot be unprotected.

**Conclusion (`E`):** protection is a one-way authority transition, not a temporary write-protect bit in the exposed interface.

### C7 — Protect completion is status-qualified

**Claim (`H/P*`):** S1 requires the protect operation to finish and directs the host to read status; its note says data is protected after good status confirmation.

**Conclusion (`E`):** `protect command issue != demonstrated successful protected state`.

### C8 — Read survives protection

**Claim (`H/P*`):** S1 says OTP data can be read whether or not the area is protected.

**Conclusions (`E`):**

- `write authority retired != data inaccessible`;
- `read-only != secret`.

### C9 — OTP protection is not sanitization

**Claim (`H/P*`):** S1 preserves read access after protection rather than destroying data.

**Later taxonomy (`H/P`):** S5 separately describes OTP and sanitize/secure-removal categories.

**Conclusion (`E/X`):** `permanent retention against mutation != secure forgetting`.

### C10 — OTP protection is not confidentiality

**Claim (`H/P*`):** post-protection read remains part of the documented interface.

**Conclusion (`E/X`):** write prohibition alone does not provide secrecy or encryption.

### C11 — Patent-family mechanism is broader than the product state machine

**Claim (`H/P`):** S2 includes embodiments where a block may be program/erase capable until a lock page/bit is programmed, after which both are inhibited.

**Counterpoint (`H/P*`):** S1 says the 2006 product OTP area cannot be erased even while unprotected.

**Conclusion (`E/X`):** use S2 to show a mechanism family in which retained lock state controls future operation authority, but do not identify that broad embodiment as the exact S1 implementation.

### C12 — Filing/priority and public disclosure chronology must remain separate

**Claim (`H/P`):** S2 family metadata gives 2-Sep-2004 filing/priority and `US20060044893A1` publication on 2-Mar-2006.

**Conclusion (`E`):** `2004 priority != 2004 public disclosure`.

### C13 — Earlier flash OTP prior art exists

**Claim (`H/P`):** S3 was filed in 1999 and published/granted in 2003 and describes persistent OTP-sector write-protect/lock state in flash.

**Conclusion (`E/X`):** Micron's 2006 NAND witness is not invention priority for flash OTP/read-only locking. Chronology alone does not establish direct design lineage.

### C14 — Current Micron wording preserves the payload/authority distinction

**Claim (`H/P`):** S4 describes NAND OTP storage as a distinct area and says OTP functionality lets the host lock programmed data from modification.

**Conclusion (`E`):** the distinction between `data programmed` and `data locked against modification` remains meaningful in Micron's current first-party vocabulary.

**Boundary (`X`):** do not use S4 to infer that every present NAND part uses S1's `A0h/A5h/AFh` command contract.

---

## Cross-case controls

### Case 11 — floating-gate EPROM (`A`)

Case 11 retains charge nonvolatilely but provides a deliberate radiation erasure route in the bounded Intel/Frohman disclosure. S1's NAND OTP area has no erase operation even before protection.

Safe comparison:

> `state durable under ordinary power loss != same forgetting authority`.

### Case 13 — early Flash coarse erase (`A`)

Case 13's central relation is electrically programmable storage coupled to coarse erase/reuse. Case 149 demonstrates that a bounded area on a flash device can intentionally exclude erase/reuse and then separately retire further program authority.

Safe comparison:

> `same broad flash family != same admissible operation set`.

### Case 78 — NAND bad-block marker (`A`)

Both involve small retained control relations that change future treatment of NAND regions, but the predicates differ: bad-block marking means avoid a defective region; OTP protection means retain content and reject future mutation.

### Case 110 — WORM/Object Lock (`A`)

Both can functionally restrict future modification while retaining read access. Cloud/object/file WORM, however, has version, policy, time, legal-hold, and administrative state unlike a raw NAND OTP area. No genealogy or state-machine identity is asserted.

### Case 114 — NVMe namespace write protection (`A`)

NVMe namespace write protection is a host/controller access-policy layer. Micron OTP is a raw-device sub-area with a documented irreversible protection transition and no erase operation in the bounded product interface.

### Case 44 — NVMe sanitize (`A`)

Case 44 concerns forgetting/removal of recoverable user data. Case 149 concerns preserving data while retiring write authority. They point in opposite directions.

---

## Counterclaim ledger

| Shortcut | Status | Reason |
| --- | --- | --- |
| “OTP means exactly one program command” | rejected | S1 allows whole/partial page programming before final protect |
| “Unprotected OTP is ordinary erasable NAND” | rejected | S1 says OTP area cannot be erased even when unprotected |
| “Once any data is programmed, the whole area is protected” | rejected | S1 separates program/verify and protect operations |
| “Protect just means data happens to be nonvolatile” | rejected | protection changes future program authority; payload was already nonvolatile |
| “Protect command byte means protection certainly succeeded” | rejected | S1 qualifies protected state by operation completion/good status |
| “Protected means unreadable/secret” | rejected | S1 preserves read access after protect |
| “Protected means securely erased” | rejected | data is intentionally retained and readable |
| “The patent proves the exact 2006 product circuit” | rejected | S2 is broader than S1 and includes erasable-before-lock embodiments |
| “Micron invented flash OTP in 2004/2006” | rejected | S3 provides earlier 1999-filed / 2003-published flash OTP-sector prior art |
| “2004 filing date is a 2004 public disclosure date” | rejected | public patent publication in the cited family is 2006 |
| “Current Micron OTP wording proves the exact old command set” | rejected | S4/S5 are later continuity/taxonomy witnesses only |
| “OTP permanence proves invasive physical tamper resistance” | ungrounded | inspected sources define interface behavior, not full physical adversary resistance |

---

## Related-repository boundary

Fresh searches of `tmzncty/computing-archaeology` for `Micron NAND OTP`, `OTP DATA PROTECT`, and related terms returned no dedicated study to reuse. This record therefore retains the bounded persistence/authority mechanism here.

A broader technical history of PROM/EPROM/EEPROM/Flash OTP vocabulary, vendor secure-sector lineages, ONFI standardization, eFuse/antifuse alternatives, and physical attack practice should be developed in `computing-archaeology` and linked back rather than duplicated.

---

## Open debt

- recover an origin-hosted or archival-origin copy of the exact Micron Rev. D 12/06 datasheet;
- identify exact part numbers/die generations covered by the historical document and whether protection representation differs across revisions;
- trace ONFI OTP command standardization and later Micron command migrations;
- locate period Micron application notes describing intended serial-number/security provisioning workflows;
- perform hardware validation of protect, post-protect program rejection, reset, and power-cycle behavior on a compatible device;
- deepen AMD/Fujitsu/Micron flash-OTP genealogy in `computing-archaeology` without rewriting chronology as causation.
