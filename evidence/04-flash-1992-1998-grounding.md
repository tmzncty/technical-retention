# Evidence Record — Mapped Flash, 1992–1998

## Purpose

This record deepens [`cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md) enough to evaluate it against the repository's `grounded` gate.

The bounded claim is not a general history of NAND, SSDs, or every Flash Translation Layer. It is narrower:

> A rewritable Flash storage service can preserve one logical identity while deliberately replacing its physical embodiment, and that continuity depends on retained mapping/allocation state plus maintenance procedures whose purposes must be distinguished.

The evidence below separates four things that are easy to collapse:

1. **out-of-place remapping** — preserve logical identity while changing physical placement;
2. **reclamation / clean-up** — recover erase-unit capacity while copying still-current data elsewhere;
3. **wear leveling** — distribute switching/erase burden to reduce premature failure;
4. **FTL** — a historically attested translation-layer format/abstraction, not a label to project automatically onto every earlier Flash manager.

---

## Source A — Amir Ban / M-Systems, US 5,404,485

**Type:** H/P — patent, primary technical evidence.

**Title:** `Flash file system`

**Inventor:** Amir Ban

**Original assignee:** M-Systems Flash Disk Pioneers Ltd.

**Filed:** 8 March 1993

**Issued:** 4 April 1995

**Patent:** US 5,404,485

**Stable text / PDF:**

- https://patents.google.com/patent/US5404485A/en
- official patent-image PDF linked from that record

### Direct scan anchors

The patent-image scan has now been visually inspected rather than relying only on HTML transcription.

#### Printed pp. 1–2 — erase-before-write and virtual mapping

The background describes Flash as nonvolatile but not practically rewritable at a previously written area without a preceding block erase. The summary then introduces a virtual mapping system that allows new writes to go to **unwritten physical address locations** while preserving the computer-visible address.

On printed p. 2 the mechanism is explicit:

- each byte/block can be described in physical and virtual address spaces;
- a virtual map converts the virtual address to the current physical address;
- if the currently mapped physical block is already written, the controller finds an unwritten block;
- new data are written there;
- the map is changed so the **original virtual address** resolves to the new physical block;
- the former physical block becomes unusable until the containing unit is later erased.

This directly grounds:

> **identity persistence does not require location persistence.**

It also grounds the temporal distinction between an old embodiment ceasing to count as current and its later physical erasure.

#### Printed pp. 2–4 — logical unit identity survives transfer

The scan states that each unit has a logical unit address/number which remains unchanged as the unit is rewritten into a new physical address location.

Printed p. 4 is especially useful because the unit header and allocation map are described together. The patent states, in substance, that data must move physically during transfer while the logical unit number preferably remains unchanged. The block-allocation statuses include:

- `block free and writable`;
- `block deleted and not writable`;
- `block allocated and contains user data`.

The source therefore supplies its own period vocabulary for the distinction this case is studying. `Deleted` is an allocation/currentness state; it is not the same event as erasing the containing unit.

#### Printed pp. 5–6; FIGS. 4–8 — two-stage translation, rewrite, and reclamation

The patent uses two-stage translation from virtual address to logical-unit-relative address and then to physical unit/location. This lets a logical unit move without requiring its external identity to change.

The write flow in FIG. 6 and accompanying text performs an out-of-place update:

1. examine the allocation map;
2. if the target is already occupied, locate a free address;
3. write the replacement there;
4. mark the original block `deleted and not writable`;
5. update the virtual/logical mapping to the new embodiment.

The transfer flow in FIGS. 7–8 is a separate maintenance procedure:

1. choose a unit for transfer;
2. read its still-current active blocks;
3. write those blocks into the reserved transfer unit;
4. erase the original unit;
5. change the logical-to-physical unit map so the logical unit identity continues at the replacement physical unit.

This grounds a precise definition of reclamation for the bounded case:

> **copy current state → erase the old erase unit → update/rebind identity metadata.**

#### Printed p. 6 onward; FIG. 9 — mapping state is itself retained state

The patent places the major portion of the virtual map in nonvolatile Flash while keeping a smaller secondary map in RAM. It also explains how the volatile secondary state can be rebuilt at startup from retained block-usage information.

The user data alone therefore do not constitute the whole retained object-service state. The system must also preserve or reconstruct relations that answer:

> Which physical embodiment currently counts for this virtual identity?

That is direct primary support for treating mapping/allocation metadata as **constitutive retention state**, not merely performance bookkeeping.

### Claim boundary

This patent should not be silently renamed a modern SSD FTL. Its own vocabulary is `virtual map`, `logical unit`, `physical address`, `transfer unit`, allocation state, and unit transfer. Later FTL terminology is grounded separately below.

---

## Source B — Steven E. Wells / Intel, US 5,341,339

**Type:** H/P — patent, primary technical evidence.

**Title:** `Method for wear leveling in a flash EEPROM memory`

**Inventor:** Steven E. Wells

**Assignee:** Intel Corporation

**Continuation lineage:** application Ser. No. 07/969,467 filed 30 October 1992

**Patent issued:** 23 August 1994

**Stable text / PDF:**

- https://patents.google.com/patent/US5341339A/en
- patent-image PDF linked from that record

### Printed pp. 1–4 — mapping and clean-up are already distinct from wear equalization

The patent describes an array in which data are written to available empty locations without requiring the physical sector position to match the logical sector number. A lookup table records the relationship.

When a logical sector changes:

- the new version is written at a new physical position;
- the lookup table is updated;
- the previous physical position is marked `dirty`.

After dirty sectors accumulate, `cleaning up a block` copies valid information elsewhere and erases the block to recover capacity.

This is useful independent corroboration of the same broad architectural fact found in Ban: logical sectors survive physical relocation through mapping, while old embodiments can become invalid before block erasure.

### Printed pp. 3–4 — finite switching life creates another maintenance objective

The patent then introduces a **different problem**. It states that Flash has a limited life under repeated switching and gives contemporary engineering estimates: switching may begin to slow after roughly ten thousand operations, while roughly one hundred thousand may be required before system operation is affected in the described context.

The source observes that normal workload and clean-up selection can make some blocks switch much more often than others. It therefore seeks to equalize switching across the array.

The abstract and summary are explicit: selection of a block for clean-up considers both:

- how many invalid sectors the block contains; and
- how many switching operations the block has already undergone.

### Why this matters methodologically

The source prevents an important category error:

> **reclamation is not automatically wear leveling.**

Reclamation asks which obsolete physical state should be destroyed to recover writable capacity while retaining still-current data.

Wear leveling adds another objective: how to distribute destructive/program/erase work across the medium so that heavily rewritten regions do not consume their usable switching life disproportionately.

The operations can be coupled in one controller, but their retention problems are not identical.

---

## Source C — Intel AP-619, August 1995

**Type:** H/P — contemporary manufacturer application note; primary vendor evidence reporting a PCMCIA-approved format.

**Title:** `FTL Logger: Exchanging Data with FTL Systems`

**Authors:** Kirk Blum and Peter Lam

**Document:** Intel Application Note AP-619, order no. 292174-001

**Date:** August 1995

**Preserved scan:** https://intel-vintage-developer.eu5.org/DESIGN/FLCARD/APPLNOTS/292174_1.PDF

### Printed p. 1 — a defensible terminology/standardization anchor

Intel reports that several companies worked with Intel and PCMCIA to standardize the Flash-media format used for sector-based disk emulation, and states that the format had recently been approved by PCMCIA as the **Flash Translation Layer (FTL)** format, with the FTL specification available from PCMCIA.

This establishes a conservative historical result:

> **By August 1995, `Flash Translation Layer (FTL)` was documented by Intel as the name of a PCMCIA-approved Flash-media format/translation architecture.**

It does **not** establish that August 1995 was the first coinage of `FTL`. Until an earlier directly inspected source is found, the repository should say `documented no later than 1995`, not `invented in 1995`.

The same page also says allocated Flash space cannot immediately be reused after deletion until a reclamation process called `clean-up` is run.

### Printed p. 3 — FTL fundamentals

The application note gives an unusually concise period account of the abstraction:

- Flash erase units are much larger than host-style writable blocks;
- a translation layer is needed between conventional OS/block semantics and Flash erase semantics;
- FTL redirects writes to unallocated/free areas;
- it invalidates the area that previously contained the block's data;
- it records where the remapped block is physically placed so later reads return the current data;
- to higher software it presents a **virtual block storage device** and manages logical-to-physical mapping.

This is exactly the historical bridge that should be used instead of retroactively calling every 1980s/early-1990s Flash-management technique an `FTL`.

### Printed pp. 3–4 and glossary — metadata/currentness

The document describes Block Allocation Maps (BAM), a Virtual Block Map (VBM), erase-unit headers, deleted/free/bad states, and a transfer unit reserved for reclamation. It also notes that VBM state can reside on media or be rebuilt in RAM from retained allocation information when media are reinserted.

This independently reinforces the case's central point:

> Physical Flash state is not enough to recover the current logical namespace; retained mapping/allocation relations matter.

---

## Source D — Toshiba TC5816BFT NAND Flash E2PROM datasheet, 1998

**Type:** H/P — manufacturer datasheet, primary device evidence.

**Device:** Toshiba TC5816BFT, `16 MBIT (2M × 8 bits) CMOS NAND FLASH E2PROM`

**Document date:** 1 July 1998

**Preserved scan used in this pass:** https://datasheet.octopart.com/TC5816BFT-Toshiba-datasheet-181393403.pdf

### Device geometry and operation

The manufacturer sheet identifies the part as NAND Flash and organizes it as pages within blocks, with erase performed at block granularity and separate automatic page-program / block-erase operations.

This is a device-level anchor for the physical asymmetry that controller mapping must manage: program and erase are distinct operations at different structural granularities.

### Printed p. 34/36 — bad blocks, operation failure, ECC, and replacement

The datasheet explicitly warns that some blocks can be unusable and supplies a valid-good-block count rather than promising that every physical block is usable.

For program and erase failures it prescribes status checking followed by **block replacement**. Its illustrated program-failure recovery says that when an error occurs in Block A, data should be reprogrammed into another Block B from an external buffer, and future access to Block A should be prevented by maintaining a bad-block table or equivalent scheme. The same section names ECC as a countermeasure for a single-bit program failure.

This is later than Ban/Wells and should not be projected backward into their exact designs. It nevertheless provides manufacturer-level evidence that by the late 1990s NAND persistence already depended on more than cell nonvolatility:

- physical blocks may be unusable or fail;
- controllers/systems must retain bad-block identity;
- successful retained data can require re-creation on a replacement block;
- ECC and replacement policy participate in usable retention.

The document does not provide the endurance-count evidence used in this case. Finite switching-life evidence is instead grounded in the contemporary Wells patent and later standards evidence remains separately bounded in the main case.

---

## Masuoka 1987 status — deliberately not overclaimed

Fujio Masuoka, Momodomi, Iwata, and Shirota's IEDM 1987 paper, `New ultra high density EPROM and Flash EEPROM with NAND structure cell`, remains an important earlier device-history boundary (IEDM Technical Digest 1987, pp. 552–555, DOI `10.1109/IEDM.1987.191485`).

During this grounding pass, bibliographic metadata and abstract-level records were recoverable, but a directly inspectable full text was not obtained. Therefore:

- the paper is **not** used as a unique source for any central mapping, FTL, reclamation, or wear-leveling claim;
- the roadmap item to inspect the full paper remains open;
- the grounded status of Case 04 rests on directly inspected 1992–1998 mapping/controller/vendor sources instead.

---

## Claim ledger

| Claim | Label | Evidence | Status |
| --- | --- | --- | --- |
| Flash erase-before-write creates a mismatch with disk-like arbitrary rewrite semantics | H/P | Ban 1993-filed patent, printed pp. 1–2; Wells 1992 lineage | grounded |
| A stable virtual/logical identity can resolve to a new physical location after rewrite | H/P | Ban, printed pp. 2–6; Wells, printed pp. 3–4 | grounded |
| Logical invalidation can precede physical erase | H/P | Ban allocation statuses + later transfer; Wells dirty-sector + later clean-up | grounded |
| Reclamation preserves current blocks by copying them before erasing an old unit/block | H/P | Ban FIGS. 7–8; Wells clean-up description | grounded |
| Mapping/allocation metadata is part of the state needed to recover current identity | H/P + E | Ban map-in-Flash / reconstructible secondary map; Intel AP-619 VBM/BAM | grounded |
| `Flash Translation Layer (FTL)` is historically attested by August 1995 as a PCMCIA-approved format according to Intel | H/P | Intel AP-619, printed p. 1 | grounded, `no later than 1995`; not claimed as first coinage |
| FTL remaps writes to free areas, invalidates old areas, records physical placement, and presents virtual block semantics | H/P | Intel AP-619, printed p. 3 | grounded |
| Reclamation and wear leveling are distinct maintenance objectives | H/P + E | Wells patent separates dirty-space clean-up from switching-count equalization | grounded |
| Flash physical nonvolatility does not imply unlimited rewriting | H/P | Wells finite switching-life discussion; bounded later ONFI evidence in main case | grounded for distinction, not universal numeric lifetime |
| NAND usable retention can require bad-block metadata, ECC, and block replacement | H/P | Toshiba TC5816BFT, printed p. 34/36 | grounded as 1998 boundary |
| The 1987 Masuoka paper itself establishes later FTL semantics | X | no such claim supported | rejected |
| Every reclamation algorithm is wear leveling | X | Wells explicitly gives separate objective | rejected |
| `deleted` universally means physically recoverable data | X | architecture only establishes invalidation ≠ erase operation | rejected |

---

## Engineering reconstruction

The grounded source chain supports a layered model of Flash retention:

```text
physical nonvolatile cell state
        ↓
program / erase geometry
        ↓
out-of-place replacement of changed state
        ↓
logical→physical mapping says which embodiment is current
        ↓
old embodiment becomes invalid / dirty
        ↓
reclamation copies still-current state before erase
        ↓
wear policy may additionally choose work to distribute finite switching burden
        ↓
bad-block / ECC / replacement state can preserve service despite physical failure
```

The important result is not that Flash is less persistent than it appears. It is that **different kinds of persistence are being combined**:

- cell-level nonvolatility;
- identity continuity across relocation;
- metadata continuity;
- capacity continuity through reclamation;
- lifetime continuity through wear management;
- service continuity through bad-block replacement and error handling.

Calling all of these simply `nonvolatile storage` loses the mechanism.

---

## Counterexamples and limits

1. **Not every Flash controller is Ban's system.** The patent is a bounded architecture, not a universal specification of later SSDs.
2. **FTL is not retroactive vocabulary.** Intel AP-619 gives a defensible 1995 terminology/standardization anchor, not permission to rename every earlier Flash manager an FTL.
3. **Reclamation is not wear leveling.** A controller can reclaim capacity without equalizing erase/switch counts; Wells makes the additional lifetime objective explicit.
4. **Logical invalidation does not prove forensic recoverability.** The case proves semantic separation from physical erase, not a universal recovery technique or retention duration.
5. **A surviving data cell without its mapping may be unusable as the intended logical object.** Conversely, a logical identity can survive replacement of the cells that once embodied it.
6. **The Toshiba 1998 device is boundary evidence.** It must not be used to claim that Ban's 1993 implementation had the same NAND bad-block/ECC behavior.
7. **Masuoka 1987 full text remains uninspected in this pass.** It is not a central dependency of the grounded mapping argument.

---

## Related-repository boundary

A code/document search in `tmzncty/computing-archaeology` during this pass did not surface an existing dedicated Flash/FTL article. Its roadmap nevertheless already identifies ROM → PROM → EPROM → EEPROM → Flash and SSD/FTL as a technical-history bridge.

Accordingly:

- this case owns the **retention-specific argument** about identity, mapping, invalidation, reclamation, and maintenance categories;
- a broad semiconductor/SSD history still belongs in `computing-archaeology` and should be linked here when built;
- this record should not expand into a survey of NAND generations, controller architectures, modern NVMe, TRIM, secure erase, or contemporary SSD reliability.

---

## Grounding decision

Case 04 now satisfies the repository's `grounded` requirements for its bounded claim:

- primary historical vocabulary recovered;
- multiple independent contemporary primary sources;
- exact printed-page / figure anchors for central mechanisms;
- mechanism described below the disk-like interface;
- maintenance triggers and failure modes separated;
- modern FTL vocabulary historically bounded;
- counterexamples/limits recorded;
- related-repository duplication checked.

The remaining Masuoka 1987 full-text inspection is worthwhile archival cleanup, but the core mapped-retention argument no longer depends on it.
