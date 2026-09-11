# Micron NAND OTP Data Protect: Programmable-Then-Irreversible Authority, No-Erase Payload, and Readable Permanence

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
