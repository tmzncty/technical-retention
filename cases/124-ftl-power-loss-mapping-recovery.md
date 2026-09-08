# Case 124 — FTL Power-Loss Mapping Recovery: Persistent Payload, Volatile Resolution State, and Reconstruction

## Status

**`grounded`** — bounded to the 1993–2014 mapped-Flash / FTL recovery path needed to establish one relation: nonvolatile payload can survive a power interruption while volatile or stale logical-to-physical resolution state must be reconstructed before the surviving payload is again reliably legible through the logical interface.

Grounding record: [`../evidence/124-ftl-1995-2014-mapping-recovery-grounding.md`](../evidence/124-ftl-1995-2014-mapping-recovery-grounding.md).

## Scope

Case 04 established that mapped Flash can keep one logical identity while its physical embodiment moves, and that mapping/allocation state is constitutive retention state. Case 124 asks the failure-side follow-on question:

> What survives when the Flash payload remains nonvolatile but the working mapping table, address cache, or other relation used to resolve current logical addresses is lost at power failure?

This case is **not**:

- a complete history of Flash Translation Layers;
- a claim that every SSD uses the same mapping-table architecture;
- a claim that a 2009 academic proposal or a 2011 patent was the first power-fail recovery design;
- a claim that mapping recovery reconstructs lost NAND payload bits;
- a claim that every physically surviving page remains logically current;
- a claim that startup scanning, map-block reconstruction, log replay, and deterministic replay are one implementation lineage;
- a filesystem `fsync` or host-interface durability case;
- a secure erase, sanitization, or forensic-recovery case.

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `FTL`, `flash translation layer`, and power-failure mapping recovery found no dedicated case to reuse. Broader FTL/controller genealogy belongs there if developed; this case retains only the mapping-relation lifetime and recovery boundary.

---

## Historical vocabulary

The bounded sources use vocabulary including:

- `virtual map`;
- `Virtual Block Map (VBM)`;
- `Block Allocation Map (BAM)`;
- `page address cache`;
- `map block`;
- `block map table (BMT)`;
- `super map`;
- `dedicated map`;
- `update log`;
- `checkpoint`;
- `crash recovery`;
- `FTL metadata consistency`.

The following are **project engineering terms**, not historical actor vocabulary:

- `resolution-state lifetime`;
- `logical legibility`;
- `recovery substrate`;
- `relation reconstruction`;
- `payload-survival / mapping-survival split`.

---

## Historical record

### H/P — 1993-filed mapped Flash already made the relation reconstructible

Case 04's inspected Amir Ban / M-Systems patent, US 5,404,485, filed **8 March 1993**, describes a virtual mapping system in which the logical/virtual identity can remain stable while current data moves to a new physical Flash location.

The same source places a major portion of mapping state in nonvolatile Flash, keeps a smaller secondary map in RAM, and describes rebuilding volatile secondary state at startup from retained block-usage information.

This is already enough to reject:

> `volatile working map lost` = `all mapped payload necessarily lost`.

It is also enough to reject a novelty claim that later SSD research invented the broad idea of rebuilding volatile lookup state from Flash-resident mapping/allocation evidence.

### H/P — Intel AP-619 documents FTL mapping and rebuildable RAM state by August 1995

Intel Application Note AP-619, *FTL Logger: Exchanging Data with FTL Systems* (**August 1995**), documents the `Flash Translation Layer (FTL)` name no later than that date and describes BAM/VBM metadata for a virtual block storage device.

The application note says VBM state can reside on media or can be rebuilt in RAM from retained allocation information when media are reinserted.

The historical claim is deliberately narrow:

> By 1995, a vendor document for the PCMCIA FTL format already treated logical-to-physical lookup state as something that could be reconstructed from nonvolatile Flash-resident metadata.

This is a terminology and mechanism floor, not an invention date for FTL or crash recovery.

### H/P/S — a 2009 peer-reviewed FTL paper makes power-failure cache loss explicit

Jung-Wook Park, Seung-Ho Park, Gi-Ho Park, and Shin-Dug Kim, *An integrated mapping table for hybrid FTL with fault-tolerant address cache*, was received **26 December 2008**, accepted **3 March 2009**, and published **10 April 2009** in *IEICE Electronics Express*.

The paper describes later FTLs that keep physical page addresses in Flash spare areas while using an address cache to reduce lookup cost. It explicitly identifies power failure as a risk: losing only a few cached page-table entries can create substantial inconsistency for data information.

Its proposed scheme integrates metadata into a Flash-resident `hybrid map block`. On startup, a partial scan of that map block rebuilds block and bitmap tables; page-table entries are then fetched on demand into the cache.

For this paper's own proposal:

> **volatile page-address cache ≠ sole retained mapping authority**.

The nonvolatile map block is intended to preserve enough relation state to regenerate volatile working metadata.

The paper is an academic proposed design with simulation results. It is not evidence that all 2009 commercial SSDs used this structure.

### H/P — a 2011 ITRI filing separates cached BMT from nonvolatile recovery records

US 9,164,887 B2, *Power-failure recovery device and method for flash memory*, has a **5 December 2011** filing/priority date and names Industrial Technology Research Institute (ITRI) as assignee.

The disclosure describes:

- a `block map table (BMT)` recording logical-block → physical-block mappings;
- the BMT temporarily stored in cache;
- a `super map` and `dedicated map` stored in Flash;
- an `update log`;
- an abnormal-shutdown recovery path that loads the Flash-resident BMT to cache and replays update-log labels to recover the mapping relation.

Its own description explicitly states that the recovery mechanism can recover a BMT lost because of power failure using information registered in the update log.

This is strong primary evidence for a split among:

```text
working translation state in volatile cache
        !=
nonvolatile map/checkpoint/log evidence
        !=
user payload pages
```

The patent proves a disclosed design, not a shipping-product implementation or first invention.

### H/P/S — DAC 2014 treats FTL crash recovery as metadata-consistency recovery

Chi Zhang, Yi Wang, Tianzheng Wang, Renhai Chen, Duo Liu, and Zili Shao, *Deterministic crash recovery for NAND flash based storage systems*, appeared at DAC 2014.

The paper defines the FTL crash-recovery problem as maintaining and recovering **FTL metadata consistency** after system crash. Its DCR design replays deterministic operations between the last checkpoint and the crash point and checks a bounded number of blocks rather than scanning the entire Flash chip.

For this bounded case, the important point is not that DCR is the canonical recovery algorithm. It is that a later independent research path again treats crash recovery as recovery of the metadata relation that makes the Flash contents usable as the intended logical store.

---

## Retained state

The bounded case separates at least six state classes.

### 1. User payload pages

Nonvolatile Flash data pages containing user or higher-layer data.

Physical survival of these pages is a substrate fact. It does not by itself identify which page is the current embodiment of a logical address.

### 2. Flash-resident mapping/allocation evidence

Examples in the bounded sources include BAM/VBM information, map blocks, logical-address information in spare areas, BMT copies, super/dedicated maps, and update logs.

These are not the user payload, but they can be constitutive of later logical access.

### 3. Volatile working mapping/cache state

RAM/SRAM/DRAM structures used to make normal logical-to-physical lookup fast.

They may disappear at power loss even though Flash-resident payload and recovery evidence survive.

### 4. Currentness / supersession relation

Out-of-place Flash can leave several physical embodiments with the same broad logical lineage. The system still needs evidence that determines which embodiment is current and which is obsolete/deleted.

The mapping relation therefore carries more than geometric location; it can participate in currentness.

### 5. Recovery frontier / checkpoint-log state

Later designs can preserve a checkpoint and enough subsequent history or deterministic reconstruction evidence to advance from that checkpoint to a crash-consistent mapping state.

This is not a complete user-operation history.

### 6. Reconstructed runtime map

After startup scan or replay, the controller again has a working relation suitable for ordinary lookup.

The reconstructed table is a service-enabling representation of retained relations, not a newly reconstructed copy of every payload byte.

---

## Retention mechanism

The bounded recovery pattern can be represented as:

```text
normal operation
    logical address
        |
        v
volatile working lookup/cache
        |
        +------ resolves ------> current physical Flash page
        |
        +------ updates -------> Flash-resident mapping/log evidence

power failure
    |
    +--> volatile working lookup may disappear
    |
    +--> nonvolatile payload may survive
    |
    +--> nonvolatile relation evidence may survive

restart
    |
    +--> scan / load checkpoint / replay log / bounded reconstruction
    |
    v
reconstructed working mapping
    |
    v
ordinary logical service resumes
```

The reusable point is:

> **The thing reconstructed after power failure can be the address/currentness relation, not the payload.**

That distinguishes relation recovery from data reconstruction.

---

## Failure semantics

### Payload survives, working map does not

This is the central counterexample.

A NAND page can remain physically readable after power failure while the RAM-resident lookup entry that tells the controller which LBA/LPN should resolve to that page has vanished.

Therefore:

> **payload persistence ≠ logical legibility**.

### Recovery evidence survives, but service is not yet ready

A map block, BMT, or update log can remain intact while the controller is still rebuilding runtime structures.

Therefore:

> **recoverability of the mapping relation ≠ immediate post-reset availability**.

Recovery time is part of service restoration even when no payload rewrite is required.

### Some metadata survives, but it is insufficient or stale

A durable checkpoint without enough information about later mapping updates may not identify the intended current mapping at the crash boundary.

Therefore:

> **some retained mapping metadata ≠ sufficient crash-consistent currentness evidence**.

The bounded sources motivate recovery protocols precisely because retaining arbitrary metadata bytes is weaker than recovering a consistent relation.

### Mapping reconstruction succeeds, payload can still be bad

A valid logical-to-physical relation cannot manufacture payload bits lost to program failure, media corruption, unreadable pages, or a write that never became durable.

Therefore:

> **mapping recovered ≠ payload recovered or validated**.

### Payload can outlive its normal name

If relation evidence is lost beyond reconstruction, physical pages can survive while ordinary logical lookup can no longer reliably name them.

That is a technical-forgetting mode in which what disappears is not necessarily the physical state first, but the relation needed to interpret it as current logical storage.

---

## Engineering reconstruction

### E1 — mapping metadata is constitutive retention infrastructure

Assumptions:

1. a logical address can move among physical Flash pages;
2. several old/new physical embodiments can coexist before reclamation;
3. ordinary reads require a logical-to-physical decision.

Then preserving the user payload alone is insufficient for the mapped service. The system must preserve or reconstruct a relation that selects the admissible physical embodiment.

This is already grounded historically by Case 04; Case 124 adds the power-loss/recovery side.

### E2 — volatile cache loss does not imply relation loss if a recovery substrate survives

The 2009 map-block design and 2011 ITRI disclosure both keep normal-operation translation state in faster volatile memory while retaining enough nonvolatile metadata to regenerate it.

Thus:

> **working-state volatility ≠ service-state ephemerality**.

A volatile representation can be disposable if a lower-level retained relation is sufficient for reconstruction.

### E3 — mapping reconstruction is different from payload reconstruction

Scanning metadata, rebuilding tables, or replaying a mapping log changes the controller's knowledge/lookup state. It need not rewrite all surviving user pages.

Thus:

> **relation reconstruction ≠ content reconstruction**.

This is functionally different from RAID/EC reconstruction, where missing payload contribution is mathematically regenerated.

### E4 — restart cost depends on retained summary structure

Whole-media scan, partial map-block scan, checkpoint plus replay, and deterministic bounded reconstruction make different time/space trade-offs.

This supports a retention-design question:

> How much relation state is retained during normal operation in order to reduce later recovery work?

The comparison is functional only. The sources do not establish one direct genealogy across all four techniques.

### E5 — currentness can be lost without immediate physical erasure

Out-of-place updates can leave old pages physically present. If the metadata deciding the current embodiment is lost or inconsistent, byte survival alone does not establish which version should answer the logical address.

This is the Flash-side counterpart to Synthesis 16's broader relation-loss warning, but it is **not** a replicated-system mechanism and should not be relabeled as replica currentness.

---

## Cross-case comparison

### Case 04 — mapping as constitutive state

Case 04 establishes the positive relation:

> logical identity can survive physical relocation because mapping/allocation state preserves the resolution relation.

Case 124 supplies the negative/failure relation:

> physically surviving embodiments can become logically illegible or ambiguous if the resolution/currentness relation is not itself recoverable.

### Synthesis 15 — relation loss is the failure-side complement

Synthesis 15 separates designation, payload value, resolution relation, and physical embodiment.

Case 124 provides a concrete Flash failure mode in which:

- physical embodiment may survive;
- payload bits may survive;
- designation vocabulary may still exist;
- but the operational resolution relation must be rebuilt before the designation can reliably reach the intended embodiment.

### Case 15 — SSD power-loss durability is a different problem

Case 15 asks whether volatile staged data/controller state reaches nonvolatile media during flush/orderly shutdown/unexpected power loss.

Case 124 asks whether already surviving nonvolatile Flash can be **resolved correctly after loss of volatile mapping state**.

Therefore:

> **payload durability handoff failure ≠ mapping-recovery failure**.

They may coexist in one SSD, but the retained objects and failure predicates differ.

### Case 16 / Synthesis 16 — relation dependence without genealogy

BSD FFS allocation/dependency state and distributed currentness evidence also show that surviving bytes can become unusable or inadmissible when constitutive relations are lost.

That is a functional analogy only. No FTL → filesystem → distributed-replication genealogy is claimed.

---

## Prior-art and novelty boundary

The repository should not say:

> `Power-fail-safe FTL mapping was invented in 2009 / 2011 / 2014.`

Case 04 already has stronger earlier evidence:

- Ban's 1993-filed patent stores major mapping state in Flash and rebuilds volatile secondary state at startup;
- Intel AP-619 documents FTL BAM/VBM relation state and rebuildable RAM lookup by August 1995.

The later sources strengthen a different claim: **power failure and crash recovery make the lifetime split between volatile working translation state and nonvolatile relation evidence explicit, and they expose several engineering strategies for reconstructing consistency.**

No direct genealogy is asserted among Ban, PCMCIA FTL, Park et al., ITRI, and DCR.

---

## Rejected claims

The bounded evidence does **not** support:

- `all physically surviving NAND pages are recoverable as files/blocks`;
- `mapping-table loss always destroys payload`;
- `rebuilding a map reconstructs lost user data`;
- `any retained checkpoint is sufficient to identify the crash-consistent current mapping`;
- `all SSDs persist their L2P/BMT in the same way`;
- `map-block scan, update-log replay, and deterministic replay are one technology lineage`;
- `a published recovery paper is evidence of universal commercial adoption`;
- `mapping recovery implies secure deletion of obsolete pages`;
- `mapping recovery implies integrity validation of the selected payload`.

---

## Claim ledger

| Claim | Label | Confidence |
| --- | --- | --- |
| 1993-filed Ban Flash mapping already supports startup reconstruction of volatile secondary mapping state from retained Flash metadata | `H/P` | high |
| Intel AP-619 documents FTL BAM/VBM mapping and rebuildable RAM state by August 1995 | `H/P` | high |
| Park et al. 2009 explicitly frames cached mapping loss under power failure as an inconsistency problem and proposes Flash-resident map-block recovery | `H/P/S` | high for the paper's proposed mechanism |
| ITRI's 2011 filing separates cache-resident BMT from Flash-resident map/log evidence and discloses abnormal-shutdown replay | `H/P` | high |
| DCR 2014 independently frames FTL crash recovery as metadata-consistency recovery | `H/P/S` | high for the published system |
| physical payload survival does not by itself recover logical resolution/currentness | `E` | high within mapped-Flash assumptions |
| volatile working map loss does not imply permanent relation loss if a sufficient nonvolatile recovery substrate survives | `E` | high |
| mapping reconstruction and payload reconstruction are distinct operations | `E` | high |
| recovery strategy changes startup/recovery work without changing NAND nonvolatility itself | `E` | high |
| these sources form one direct implementation genealogy | `X` | rejected |
| a mapping recovery success proves payload integrity | `X` | rejected |

---

## Open evidence debt

- direct facsimile comparison of earlier PCMCIA FTL specifications around power-fail/reinsertion recovery;
- named commercial SSD/controller firmware evidence tying a specific mapping checkpoint/log design to shipping hardware;
- independent fault-injection measurements that separate payload survival, mapping loss, recovery time, and post-recovery correctness;
- exact crash-ordering requirements between data-page programming and mapping/log persistence for named controllers;
- broader FTL crash-recovery genealogy, to be developed in `computing-archaeology` rather than duplicated here;
- forensic recovery after complete mapping loss, which is a separate question from ordinary service reconstruction.
