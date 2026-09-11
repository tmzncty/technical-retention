from pathlib import Path

CASE_PATH = Path('cases/149-micron-nand-otp-data-protect-irreversible-authority.md')
EVIDENCE_PATH = Path('evidence/149-micron-2004-2006-nand-otp-data-protect-grounding.md')
INDEX_PATH = Path('CASE_INDEX.md')
ROADMAP_PATH = Path('ROADMAP.md')

for p in [INDEX_PATH, ROADMAP_PATH]:
    if not p.exists():
        raise SystemExit(f'missing required file: {p}')
for p in [CASE_PATH, EVIDENCE_PATH]:
    if p.exists():
        raise SystemExit(f'refusing duplicate existing path: {p}')

CASE = r'''# Micron NAND OTP Data Protect: Programmable-Then-Irreversible Authority, No-Erase Payload, and Readable Permanence

## Status

**`grounded`** — bounded to a Micron 2Gb/4Gb/8Gb x8/x16 NAND Flash product datasheet, Revision D (12/2006), plus Micron's 2004-filed / 2006-published `Non-volatile one time programmable memory` patent family as a mechanism-family witness. An AMD/Fujitsu flash-OTP patent filed in 1999 and granted/published in 2003 is used only as earlier same-medium prior art. Micron's current Product Security Center is a later first-party continuity witness, not evidence that every current product has the exact 2006 command set.

Grounding record: [`../evidence/149-micron-2004-2006-nand-otp-data-protect-grounding.md`](../evidence/149-micron-2004-2006-nand-otp-data-protect-grounding.md).

## Scope

- **Object / system:** Micron raw NAND one-time-programmable (OTP) area and the `OTP DATA PROGRAM`, `OTP DATA PROTECT`, and `OTP DATA READ` relations documented in the 2006 product datasheet.
- **Date anchor:** the historical product document is Rev. D, **12/2006**; the related Micron patent family has a 2-Sep-2004 filing/priority date and a first listed publication `US20060044893A1` dated **2-Mar-2006**.
- **Retention question:** what changes when an already non-erasable NAND OTP area remains incrementally programmable until a separate irreversible protection transition retires future programming authority, while read authority continues?

The bounded product state machine is:

```text
factory OTP area
    -> unwritten / all 1s
    -> no erase operation available
    -> program whole/partial OTP pages (1 -> 0 transitions)
    -> verify/read while still unprotected
    -> optional additional permitted programming
    -> OTP DATA PROTECT
       -> protection operation completes successfully
       -> further OTP programming becomes unavailable
       -> unprotect is not available
       -> OTP data remains readable
```

This case is **not**:

- a claim that Micron invented OTP memory, OTP ROM, flash OTP sectors, or flash write protection;
- a claim that `one-time programmable` means exactly one host-side program command;
- a claim that the 2006 product's OTP pages were ordinary main-array blocks dynamically converted to OTP by the patent mechanism;
- a claim that permanent write protection proves physical anti-tamper resistance against invasive laboratory attacks;
- a claim that read-only permanence implies confidentiality;
- a claim that OTP protection is secure erase, sanitize, or destruction of retained data;
- a general history of PROM, EPROM, EEPROM, NOR Flash security registers, eFuse, antifuse, or managed-NAND RPMB.

---

## Historical vocabulary and chronology

The 2006 Micron datasheet calls the feature a **One-Time Programmable (OTP) Area** and separates three operations:

- `OTP DATA PROGRAM` (`A0h-10h`);
- `OTP DATA PROTECT` (`A5h-10h`);
- `OTP DATA READ` (`AFh-30h`).

The datasheet says the OTP area leaves the factory unwritten, with all bits at `1`. Programming can change selected bits to `0`. Crucially, it also says the OTP area **cannot be erased even when it is not protected**. Protection therefore does not create the no-erase property; protection retires the remaining ability to program the area further.

The same document explicitly presents programming and protection as **two discrete operations** so data can be programmed and verified before permanent protection.

This period vocabulary must be preserved. Later generic labels such as `WORM`, cloud object lock, namespace write protection, or secure storage may be useful for functional comparison, but they are not substitutions for what the Micron product document calls the mechanism.

---

## Historical record

### The OTP area is already non-erasable before protection

The 2006 product datasheet states that the OTP area cannot be erased whether or not it is protected. That yields an important three-way distinction:

> **unprotected != erasable**

and

> **no erase authority != no remaining program authority**.

An unprotected OTP area has already lost one class of future transition — returning programmed `0` bits to the erased `1` state — while still permitting bounded forward programming.

This differs from ordinary rewritable NAND blocks whose normal lifecycle includes block erase as the precondition for reuse.

### `OTP` does not mean one single programming command

The historical datasheet allows an OTP page to be programmed as an entire page or through multiple partial-page programming sequences before final protection. It also describes programming other pages in the OTP area in the same manner.

Therefore:

> **one-time-programmable storage != exactly one program command**.

The `one-time` property is a constraint on the direction and future admissibility of state transitions, not necessarily a count of one API invocation.

A page can accumulate irreversible `1 -> 0` changes before the area enters its final protected state.

### Programmed and protected are separate states

Because program/verify and protect are discrete operations, valid payload can exist in the OTP area while the area remains unprotected and therefore still admits additional permitted programming.

Thus:

> **programmed != protected**

and

> **payload state != future-mutation authority**.

The payload does not by itself tell us whether the interface still admits another OTP program operation.

### Protection is an irreversible authority transition

The datasheet's `OTP DATA PROTECT` operation says that after protection, pages in the OTP area are no longer programmable and **cannot be unprotected**.

So the important retained fact is not another payload copy. It is an enduring control relation that changes which future operations are admissible:

```text
before protect: read + permitted further program; no erase

after protect:  read; no further program; no erase; no unprotect
```

This is a particularly clean example of technical retention in which part of what persists is a **prohibition on future mutation**.

### Read authority survives the retirement of write authority

The datasheet says OTP data can be read whether or not the area is protected.

Therefore:

> **write authority retired != payload inaccessible**

and

> **read-only != secret**.

Protection preserves the data against defined future programming; it is not an encryption or confidentiality mechanism.

### Protection completion is itself status-qualified

The `OTP DATA PROTECT` sequence drives `R/B#` low while protection is in progress and directs the host to inspect status after the device becomes ready. The document states that OTP data is protected following a good status confirmation.

That provides a useful transition boundary:

> **protect command issued != protection successfully established**.

The irreversible relation should be treated as established after the operation's completion/status contract, not merely after the first command byte is placed on the bus.

---

## Micron patent-family mechanism witness

Micron's `Non-volatile one time programmable memory` family has a 2-Sep-2004 filing/priority anchor and a first listed publication `US20060044893A1` dated 2-Mar-2006. The family describes NAND and NOR flash embodiments in which blocks may be designated as OTP blocks.

Two mechanisms are particularly relevant:

1. a verify path can detect prior programming and then inhibit further programming/erasing; or
2. a block can remain program/erase capable until a predetermined page or lock bit is programmed, after which the OTP block is locked against further program/erase.

The family also explicitly recognizes earlier NOR-type flash OTP areas in its background.

This is useful engineering evidence that `OTP` can be realized by **retaining authority/control state over otherwise flash-like cells**, rather than requiring an entirely different physical memory chemistry.

But the product/document boundary matters:

> **patent family embodiment != demonstrated implementation of the 2006 datasheet part**.

The 2006 product datasheet says its OTP area cannot be erased even before protection. The patent family includes broader embodiments where a block may be erasable before lock. Those are not collapsed into one shipped state machine.

---

## Earlier flash-OTP prior art

AMD/Fujitsu's `US6662262B1`, filed 19-Oct-1999 and issued 9-Dec-2003, describes an OTP sector in a simultaneous-operation flash memory using an OTP write-protect CAM plus an OTP sector lock CAM. The lock CAM can hold the write-protect CAM in its programmed state so the OTP sector is treated as read-only.

This is earlier same-medium evidence that flash products/patents could encode persistent read-only authority before Micron's 2004 filing and 2006 product documentation.

Therefore:

> **Micron 2006 NAND OTP != invention of flash OTP or persistent OTP locking**.

But chronology is not genealogy. This case does not claim that the Micron product descends from the AMD/Fujitsu design or uses its double-CAM architecture.

---

## Retained state

At least five different state classes coexist in the bounded Micron product contract:

1. **OTP payload state** — which OTP bits/pages have been programmed from erased `1` toward programmed `0`;
2. **protection authority state** — whether the area remains open to further permitted programming or has been irreversibly protected;
3. **operation-progress/status state** — temporary busy/status state while program/protect commands execute;
4. **read authority** — the continuing ability to retrieve OTP data before and after protection;
5. **main-array state** — ordinary NAND payload outside the OTP area, governed by a different program/erase lifecycle.

These are not interchangeable.

In particular:

> **nonvolatile payload != immutable payload**

because unprotected OTP data can remain nonvolatile while future permitted programming is still possible.

And:

> **immutable-through-defined-interface != physically destroyed or confidential**.

---

## Physical / logical substrate

The historical datasheet grounds observable interface semantics but does not expose every transistor or latch used to remember that OTP protection has occurred.

The related Micron patent family demonstrates plausible flash-level mechanisms — verification of prior programming, programmed lock page/bit, and control logic that inhibits future operations — but it is broader than the exact product contract.

Accordingly, the safe reconstruction is:

```text
retained payload state
    +
retained protection / admissibility state
    +
control logic that checks that state
    ->
future program command rejected / unavailable after protection
```

The repository does **not** infer a specific fuse, latch topology, redundant encoding, or physical attack threshold for the 2006 part from the command behavior alone.

---

## Access and geometry

The 2006 witness describes ten full OTP pages, separate OTP command addressing, and an OTP area distinct from ordinary main-array access. This geometry matters because a retention relation can apply to a bounded sub-area of the same device rather than to every NAND cell on the die.

Thus:

> **device contains OTP storage != entire NAND device is one-time programmable**.

The ordinary main array and OTP area can have different admissible transitions while sharing one package and broad flash technology family.

---

## Time and irreversibility

The important temporal boundary is not a lease or countdown. It is a one-way transition:

```text
unwritten/unprotected
    -> programmed/unprotected
    -> protected
```

There is no documented `protected -> unprotected` transition in the bounded product interface.

That makes the protection state qualitatively different from temporary write-protect modes. It also differs from time-based WORM policies whose mutation authority may change when a retention deadline expires.

The irreversible step creates an operational horizon: after successful protection, later software is expected to inherit the restriction established by an earlier operation.

---

## Cross-case controls

### Case 11 — Intel/Frohman EPROM

Case 11's bounded EPROM state is electrically programmed and deliberately erasable through external radiation. Case 149's 2006 NAND OTP area, by contrast, has no erase operation even before final protection and then separately retires remaining program authority.

Safe comparison:

> `nonvolatile state with an erase route != OTP state whose documented interface excludes erase`.

No teleological progression is claimed.

### Case 13 — early Flash coarse erase

Case 13 focuses on how Flash couples convenient electrical programming with coarse erase/reuse geometry. Case 149 shows a sub-area on a flash device whose contract intentionally withholds that erase/reuse path.

Safe comparison:

> `flash technology family != uniform erase/reuse authority across every region`.

### Case 78 — NAND bad-block markers

Both mechanisms can involve small non-payload state that changes future admissible operations. A bad-block marker tells software/controller logic to avoid a defective region; OTP protection tells the device to preserve programmed content against future programming. These relations are functionally comparable but not equivalent and no genealogy is implied.

### Case 110 — cloud WORM / Object Lock

Both can be described abstractly as restricting future mutation while preserving read access. But S3/Azure/GCS/NetApp WORM cases operate at object/version/file/policy layers with time, legal-hold, version, or administrative semantics. Micron OTP is a device-local NAND-area contract with a one-way protect transition.

Therefore:

> **same high-level WORM analogy != same state machine, authority model, or substrate**.

### Case 114 — NVMe namespace write protection

Namespace write-protection is a controller/namespace access policy over host writes. It should not be back-translated into a raw-NAND OTP mechanism. Case 149's historical product contract has a dedicated OTP area that cannot be erased and becomes permanently non-programmable after protect.

### Case 44 — NVMe sanitize

OTP protection and sanitize point in opposite directions. Protection keeps data readable while retiring future mutation; sanitize aims to make prior user data unrecoverable under a defined sanitization contract.

> **permanently keep != securely forget**.

---

## Functional analogy vs philosophical interpretation

A cautious functional statement is justified:

> Some systems retain not only data, but also a durable rule about which future transformations remain admissible.

Case 149 is a strong low-level example because the rule is one-way and local to a bounded NAND region.

That sentence is **engineering interpretation**, not a claim that Micron engineers described OTP as `retention`, nor that the feature is automatically an instance of Stieglerian tertiary retention, Heideggerian `Bestand`, archival custody, or any other philosophical category.

The philosophy layer remains optional and downstream of the mechanism.

---

## Stop conditions

The current source set does **not** establish:

- that Micron invented OTP memory or flash OTP;
- the exact transistor/control-latch implementation of the 2006 shipped part;
- whether every later Micron NAND family uses the same commands, page count, or protection representation;
- invasive-attack resistance of the protection state;
- cryptographic authenticity, secrecy, monotonic-counter semantics, or anti-rollback guarantees;
- a media-sanitization property;
- a complete AMD/Fujitsu -> Micron genealogy;
- the precise standards history by which OTP commands entered later ONFI-era devices.

---

## Related-repository boundary

Fresh `tmzncty/computing-archaeology` searches found no dedicated Micron NAND OTP / `OTP DATA PROTECT` study to reuse. This case therefore keeps the retention-specific mechanism here.

A wider history of:

- PROM/EPROM/EEPROM one-time and multiple-time programmability vocabulary;
- AMD/Fujitsu secure-sector / OTP-sector product lines;
- Micron NAND generation chronology;
- ONFI OTP command standardization;
- flash security-register, lock-bit, eFuse, and antifuse lineages;
- physical reverse-engineering and attack resistance;

belongs primarily in `computing-archaeology` rather than being duplicated here.

---

## Open debt

- obtain an origin-hosted archived copy of the exact 2006 Micron datasheet rather than relying on a faithful third-party mirror for the period product witness;
- identify the exact shipped part-number family and die/control implementation corresponding to the Rev. D datasheet;
- trace when Micron's OTP command vocabulary entered or aligned with ONFI specifications;
- compare later Micron NAND OTP command revisions without back-projecting them into 2006;
- test a compatible physical device, if obtainable, to observe protect success/failure, reset/power-cycle behavior, and attempted post-protect programming;
- route the broader flash-OTP genealogy to `computing-archaeology`.
'''

EVIDENCE = r'''# Evidence 149 — Micron 2004–2006 NAND OTP data-protect grounding

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
'''

CASE_ROW = r'''| [Micron NAND OTP Data Protect: Programmable-Then-Irreversible Authority, No-Erase Payload, and Readable Permanence](cases/149-micron-nand-otp-data-protect-irreversible-authority.md) | **grounded** | raw-NAND OTP sub-area + one-way 1→0 payload programming + irreversible protect state + continuing read authority | distinguish nonvolatile from protected; unprotected from erasable; OTP from one literal program command; payload from mutation authority; protection from confidentiality/sanitize | [2004–2006 Micron patent/product grounding + 1999/2003 flash-OTP prior-art guardrail](evidence/149-micron-2004-2006-nand-otp-data-protect-grounding.md); exact shipped control embodiment, ONFI genealogy, archival-origin datasheet, and hardware validation remain open |'''

FINDINGS = r'''
## Case 149 — Micron NAND OTP Data Protect findings

Grounding record: [`evidence/149-micron-2004-2006-nand-otp-data-protect-grounding.md`](evidence/149-micron-2004-2006-nand-otp-data-protect-grounding.md).

- **3216 — 2006 product-document floor != invention date:** Micron Rev. D 12/06 documents a raw-NAND OTP area with separate program/protect/read operations; earlier flash OTP prior art rejects an invention-priority reading. (`H/P*`, `X`)
- **3217 — OTP != exactly one program command:** the product allows whole-page or multiple partial-page programming before final protection, so `one-time programmable` describes bounded transition semantics rather than one host invocation. (`H/P*`, `E`)
- **3218 — unprotected != erasable:** the OTP area cannot be erased whether protected or not; erase authority is absent before final protect. (`H/P*`, `E`)
- **3219 — no erase authority != no remaining program authority:** unprotected OTP pages can still accept permitted `1 -> 0` programming even though they cannot be erased. (`H/P*`, `E`)
- **3220 — programmed != protected:** program/verify and protect are discrete operations, so payload can already exist while further permitted programming remains admissible. (`H/P*`, `E`)
- **3221 — protection is an irreversible authority transition:** after successful `OTP DATA PROTECT`, pages are no longer programmable and cannot be unprotected through the documented interface. (`H/P*`, `E`)
- **3222 — protect command issue != protected-state confirmation:** the product reports busy/status and documents protection following good status confirmation. (`H/P*`, `E`)
- **3223 — protected != unreadable:** OTP data remains readable whether or not the area is protected; write-authority retirement does not retire read authority. (`H/P*`, `E`)
- **3224 — payload state != protection-authority state:** identical programmed bits can exist before and after protection while the set of permitted future operations differs. (`E`)
- **3225 — OTP protection != confidentiality:** continued read authority means permanent write prohibition is not, by itself, secrecy or encryption. (`H/P*`, `E`, `X`)
- **3226 — OTP protection != sanitization:** the operation intentionally retains readable data rather than making prior data unrecoverable. (`H/P*`, `E`, `X`)
- **3227 — 2004 filing/priority != 2004 public disclosure:** Micron's patent family is anchored to a 2-Sep-2004 filing/priority date but lists `US20060044893A1` publication on 2-Mar-2006. (`H/P`, `X`)
- **3228 — patent mechanism family != exact shipped-product embodiment:** Micron's patent includes erasable-before-lock flash-block embodiments, while the 2006 product OTP area is non-erasable even before protect; the sources must not be collapsed. (`H/P`, `H/P*`, `E`, `X`)
- **3229 — device-local OTP sub-area != whole-device OTP:** a NAND package can contain ordinary main-array storage and a separately governed OTP area with different admissible transitions. (`H/P*`, `E`)
- **3230 — AMD/Fujitsu 1999-filed/2003-published flash OTP prior art != direct genealogy:** `US6662262B1` predates the Micron filing and uses persistent write-protect/lock CAM state, defeating invention priority without proving design descent. (`H/P`, `A`, `X`)
- **3231 — Case11 EPROM erase route != NAND OTP no-erase contract:** both retain nonvolatile charge state, but their deliberate forgetting authorities differ. Functional comparison only. (`A`, `X`)
- **3232 — Case110/Case114 mutation restrictions != raw-NAND OTP state machine:** cloud WORM and NVMe namespace write protection constrain future mutation at different layers and with different authority/expiry semantics. (`A`, `X`)
- **3233 — related-repository boundary:** fresh `tmzncty/computing-archaeology` searches found no dedicated Micron NAND OTP study; broader flash-OTP/ONFI/security-register genealogy belongs there while Case149 retains the bounded persistence/authority relation. (`H/P` project-state record)
'''

ROADMAP_ENTRY = r'''
- [x] **Case 149 Micron NAND OTP Data Protect irreversible-authority slice** — [`cases/149-micron-nand-otp-data-protect-irreversible-authority.md`](cases/149-micron-nand-otp-data-protect-irreversible-authority.md), grounded by [`evidence/149-micron-2004-2006-nand-otp-data-protect-grounding.md`](evidence/149-micron-2004-2006-nand-otp-data-protect-grounding.md): Micron's Rev. D 12/06 raw-NAND product witness separates an already non-erasable OTP area from its later irreversible `OTP DATA PROTECT` transition, permits bounded whole/partial programming and verification before protect, preserves read after protect, and therefore fixes `OTP != one literal program command`, `unprotected != erasable`, `programmed != protected`, and `payload != future-mutation authority`. A 2004-filed/2006-published Micron patent family is used only as a broader mechanism witness; AMD/Fujitsu `US6662262B1` (1999 filing, 2003 patent) supplies earlier flash-OTP prior art without a genealogy claim. Exact shipped control circuitry, origin-hosted archival datasheet recovery, ONFI genealogy, and hardware fault/power-cycle validation remain open; fresh `computing-archaeology` searches found no dedicated study to reuse.
'''

# Concurrency / numbering guards.
index = INDEX_PATH.read_text(encoding='utf-8')
roadmap = ROADMAP_PATH.read_text(encoding='utf-8')
if 'cases/149-micron-nand-otp-data-protect-irreversible-authority.md' in index or 'Case 149 — Micron NAND OTP Data Protect findings' in index:
    raise SystemExit('Case149 already present in CASE_INDEX; refusing duplicate')
if '3216 —' in index:
    raise SystemExit('finding 3216 already occupied; concurrent index advance requires renumbering')
if '3215 — related-repository boundary' not in index:
    raise SystemExit('expected Case148 terminal finding 3215 not found; concurrent state changed')
if 'cases/148-nvme13-device-self-test-reset-surviving-maintenance.md' not in index:
    raise SystemExit('expected Case148 index row missing')
if 'Case 149 Micron NAND OTP Data Protect irreversible-authority slice' in roadmap:
    raise SystemExit('Case149 already present in ROADMAP; refusing duplicate')
if 'Case 148 NVMe 1.3 Device Self-test reset/power-surviving maintenance slice' not in roadmap:
    raise SystemExit('expected Case148 roadmap state missing')

CASE_PATH.parent.mkdir(parents=True, exist_ok=True)
EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
CASE_PATH.write_text(CASE.rstrip() + '\n', encoding='utf-8')
EVIDENCE_PATH.write_text(EVIDENCE.rstrip() + '\n', encoding='utf-8')

marker = '\n## Comparison matrix — provisional'
if marker not in index:
    raise SystemExit('CASE_INDEX case-table marker not found')
index = index.replace(marker, '\n' + CASE_ROW + marker, 1)
index = index.rstrip() + '\n' + FINDINGS.strip() + '\n'
INDEX_PATH.write_text(index, encoding='utf-8')

roadmap = roadmap.rstrip() + '\n' + ROADMAP_ENTRY.strip() + '\n'
ROADMAP_PATH.write_text(roadmap, encoding='utf-8')
