# Evidence 150 — IBM 2009–2012 SSD GC Validity / Mapping / Erase Prior-Art Deepening

## Status

**`bounded deepening complete`**

This evidence slice deepens Case 150's managed-SSD garbage-collection mechanism without attributing undocumented internals to the Crucial M550. It adds a manufacturer-authored SSD-controller design with a **2009-12-17 priority date** that explicitly separates invalidity metadata, victim selection, recovery/re-storage of still-valid data, address-map update, later block erase, and a bounded power-interruption metadata-preservation path.

The historical artifact is IBM's patent family represented by:

- Roy D. Cideciyan, Evangelos S. Eleftheriou, Robert Haas, Xiao-Yu Hu, Ilias Iliadis, **“Data management in solid state storage devices,”** US20120266050A1 / US8904261B2;
- priority: **17 December 2009**;
- filing: **16 December 2010**;
- U.S. application publication: **18 October 2012**;
- assignee: **International Business Machines Corporation**.

Primary inspection source:

<https://patents.google.com/patent/US8904261B2/en>

The patent is used as **manufacturer-primary design evidence** and **prior-art / mechanism evidence**. It is not treated as proof of commercial deployment, not treated as a Micron/Crucial source, and not used to infer the proprietary M550 state machine.

---

## Research question

Case 150 already grounds two facts that should remain separate:

1. the 2014 Crucial M550 publicly listed **Active Garbage Collection** and **TRIM support** as distinct features;
2. generic SSD GC requires preservation/relocation of still-valid data before a mixed erase block can be reclaimed.

The open mechanism question was narrower:

> Can a manufacturer-authored SSD-controller record expose an actual internal GC control sequence strongly enough to separate **invalidity evidence**, **victim choice**, **live-data preservation**, **mapping/currentness update**, **erase eligibility**, and **physical erase** — without pretending that sequence is the M550 algorithm?

IBM's 2009-priority patent is useful because it does exactly that for its own described SSD controller.

---

## Source role and claim classes

### Historical / primary (`H/P`)

The patent directly documents a proposed IBM SSD-controller architecture and its terminology, including:

- write-out-of-place;
- `LBA/PBA address map`;
- `page-invalid (PI) flag`;
- PI counts;
- garbage collection;
- recovery of still-valid data;
- re-storage into new locations;
- address-map update;
- later block erase;
- controller metadata held in memory;
- a bounded pre-shutdown copy of transient parity and current address-map metadata into Flash after power interruption is detected.

### Engineering reconstruction (`E`)

This evidence reconstructs the state/authority transitions implied by that sequence. Terms such as **reclaim authority**, **reclamation debt**, **currentness publication**, and **erase eligibility** are project terms, not IBM's patent vocabulary.

### Functional analogy (`FA`)

The IBM design is compared with Case 150's Crucial/M550 product evidence only at the level of functional structure: both concern controller-managed Flash reclamation. No implementation identity or genealogy is asserted.

### Philosophical interpretation (`A`, bounded)

The evidence supports only the restrained observation that selective forgetting can depend on retained control state about what is still valid and where it moved. It does not establish a general philosophy of forgetting.

---

## Historical record

### H/P — the patent explicitly places GC after out-of-place invalidation

The IBM record describes Flash pages as writable units inside larger erasable blocks and notes that data can only be written to a block after erase. It then describes write-out-of-place updates as producing invalid old pages and states that a follow-up internal process is required to eliminate invalid data and release locations for new input. It names this process `garbage collection`.

This is already enough to reject a synchronous-collapse model:

```text
new logical write / overwrite
    != old physical page erased immediately
```

The old embodiment first becomes **invalid from the controller's point of view**; reclamation is a later internal-management operation.

### H/P — invalidity is represented as controller state

In the described embodiment, the controller sets a **page-invalid (`PI`) flag** for a page superseded by an LBA overwrite. It likewise sets PI for pages containing data deleted by a host.

The controller also maintains a **PI count** for each stride group, recording how many invalid pages that group contains. Those counts are explicitly used in later internal management.

So the source exposes at least two layers of negative/currentness state:

```text
page PI flag
    -> this physical page no longer counts as valid/current input

stride-group PI count
    -> aggregate evidence used to prioritize reclamation work
```

Neither field is user payload and neither field, by itself, is a physical erase.

### H/P — mapping state and validity state are distinct

The controller separately maintains an **LBA/PBA address map** recording the location of input data in the Flash storage.

That produces a useful decomposition:

```text
logical designation / LBA
    != physical location / PBA
    != validity state of an old physical page
```

A page can remain physically present after it ceases to be the current embodiment of an LBA. The controller therefore needs both positive resolution state — where the current data are — and negative validity state — which older locations no longer count.

### H/P — victim selection uses invalidity evidence

The patent's Figure 6 GC description says the controller first selects blocks for erasure. In the described embodiment, selection is based on the PI counts of stride groups; groups with higher invalid-page counts can be selected first.

This directly separates:

```text
an invalid page exists
    != its containing block is selected now
```

The controller may accumulate invalid pages and their counts before deciding that a particular group should be recycled.

### H/P — block selection still does not authorize immediate erase of all contents

After selecting a stride group, the controller recovers the **still-valid** data from pages whose PI flags are not set. Error-correction processing may be applied during this recovery.

The source therefore makes the selective nature of GC explicit:

```text
victim chosen for recycling
    != all bytes inside it are disposable
```

The controller must discriminate still-valid from invalid embodiments before the old erase container can safely disappear.

### H/P — still-valid data are re-stored before the address map is updated

The patent then sends the recovered valid data back as input and re-stores them in **new strides**. Only after that does the Figure 6 sequence update the controller's address map to reflect the new locations.

For the described state machine, the historical order is therefore:

```text
select recycle target
    -> recover still-valid data
    -> re-store recovered data in new physical locations
    -> update address map to those new locations
```

This is much sharper evidence than the generic slogan “GC copies valid pages.” It exposes a distinct mapping/currentness publication step after new embodiments have been created.

### H/P — old-block erase is later than the map update, and can be delayed further

After the address map is updated, the old recycled stride group's blocks **can then be erased**. The patent adds that the erasures may be performed **immediately or at any subsequent time** to release those blocks for new data.

That wording fixes an especially useful boundary:

```text
new physical copy exists
    != address map already points to it
    != old block already erased
    != old block already reusable
```

and:

```text
mapping/currentness transition complete enough to proceed
    != physical reclamation completed at that instant
```

This gives Case 150 direct manufacturer-primary support for **reclamation debt after logical/currentness transition** without claiming anything about the M550's exact implementation.

### H/P — the patent's generic background explanation says the same thing in simpler form

Outside the specific stride/C2-code embodiment, the patent's background also describes ordinary Flash garbage collection as selecting an occupied block, recovering all still-valid data, copying those valid pages elsewhere, and then erasing the old block. Blocks are typically selected according to the amount of invalid data.

The specific Figure 6 embodiment therefore does not create the whole conceptual structure from nothing; it instantiates a controller design within an already recognized SSD-management problem.

That supports the anti-priority boundary:

> **2009 priority is an evidence floor for this IBM design, not an invention date for Flash garbage collection.**

Case 150 already carries an earlier 2005 academic guardrail through Gal & Toledo.

---

## Retained-state decomposition

The IBM artifact lets the case separate at least seven state classes.

### 1. Current user payload

The logical data the host still expects to retrieve.

### 2. Current physical embodiment

The Flash page/stride currently carrying that payload.

### 3. Old physical embodiment

A superseded or host-deleted page may remain physically present until later recycling.

### 4. Positive location/currentness metadata

The LBA/PBA address map determines where current logical data resolve.

### 5. Negative validity metadata

PI flags identify pages that no longer count as valid; PI counts summarize invalidity pressure for victim selection.

### 6. Reclamation state

A group can move from merely containing invalid pages, to selected victim, to copied/re-mapped, to erase-eligible, to actually erased/reusable.

### 7. Transient protection/control metadata

The patent's specific C2-coded design also retains transient parity and other controller metadata in memory during operation and describes copying transient parity plus the current address map into Flash after a power interruption is detected and before shutdown.

The last class is deliberately not generalized into a universal SSD GC crash protocol.

---

## Engineering reconstruction

### E — invalidity is authority, not destruction

A PI flag changes how a physical page counts in controller state. It does not itself remove charge from the NAND cells.

```text
page marked invalid
    != page physically erased
```

This is the controller-local analogue of the broader Case 150 distinction between logical retirement and later physical reclamation.

### E — victim selection is a scheduling decision, not an erase completion event

PI counts influence which groups are recycled first. Therefore a controller can retain **reclamation pressure / debt** as metadata before spending bandwidth and erase cycles to discharge that debt.

```text
high invalid-page count
    -> stronger candidate for GC
    != block already reclaimed
```

### E — preservation of current data is a precondition of selective forgetting

The described controller cannot erase a mixed group merely because some pages are stale. It first recovers still-valid data and creates new embodiments.

This makes the central Case 150 thesis concrete:

> **forgetting stale embodiments requires preserving current embodiments across the transition.**

### E — embodiment creation, currentness publication, and physical retirement are three transitions

The Figure 6 order supplies a useful three-way split:

1. recovered current data are re-stored at new physical locations;
2. the address map is updated to those new locations;
3. the old block is erased now or later.

Accordingly:

```text
new embodiment exists
    != new embodiment is the controller's published/current resolution

published/current resolution moved
    != old embodiment physically gone
```

This is a later manufacturer-authored control-architecture witness for Case 04's broader logical/physical distinction.

### E — reclamation completion has a separate temporal horizon

Because old-block erasure may occur “immediately or at any subsequent time,” the system can have a state in which logical/currentness migration is already complete enough for the map to point elsewhere but physical free-space recovery is still pending.

Project term:

> **reclamation debt** = old physical capacity that is no longer required for current logical resolution but has not yet completed the erase/reuse transition.

The term is reconstructive; IBM is not claimed to use it.

### E — a pre-shutdown metadata copy is not proof of GC crash atomicity

The IBM embodiment says that, after the controller detects a power-supply interruption, transient parity together with metadata including the current address map can be copied to Flash before shutdown.

This shows that **controller metadata preservation across a detected shutdown** was an explicit design concern in the same manufacturer artifact.

But it does not establish:

- that every interruption leaves enough energy/time to complete that copy;
- that PI flags/counts are persisted with one atomic transaction;
- that the Figure 6 GC sequence is crash-atomic at every step;
- that old/new map publication survives an arbitrary torn metadata write;
- that M550 uses this design;
- that a commercial IBM product shipped this exact embodiment.

Therefore:

```text
bounded pre-shutdown metadata preservation path
    != arbitrary-power-cut GC transaction proof
```

Case 39 remains the stronger repository case for explicitly studied FTL restart reconstitution after volatile controller state disappears.

---

## Historical / engineering boundary

The following are **historical facts from the IBM artifact**:

- priority/publication/assignee identity;
- out-of-place updates can create invalid pages;
- PI flags mark overwritten/deleted pages invalid in the described design;
- PI counts influence GC selection;
- still-valid data are recovered and re-stored;
- the address map is then updated;
- old blocks can then be erased;
- erase may happen immediately or later;
- detected power interruption can trigger a pre-shutdown copy of transient parity and current-map metadata in the described embodiment.

The following are **project engineering reconstructions**:

- `negative validity authority`;
- `reclaim authority`;
- `currentness publication`;
- `reclamation debt`;
- `erase eligibility` as a distinct analytical state;
- the claim that these transitions form a useful cross-case retention decomposition.

Keeping this separation matters because the source is an engineering patent, not a theory paper using the repository's vocabulary.

---

## Functional comparison with Case 150 / Crucial M550

The comparison is deliberately bounded.

### What can safely be said

- IBM's 2009-priority manufacturer record predates the M550's 2014 productization anchor.
- IBM exposes one SSD-controller design in which invalidity state, victim selection, live-data re-storage, map update, and later erase are distinct.
- Crucial later advertises a named product with both `Active Garbage Collection` and `TRIM support`.
- The two records jointly make a linear `delete -> instant erase` model untenable for managed-SSD reasoning.

### What cannot safely be said

- M550 used IBM's stride/C2 design;
- M550 used PI flags or PI counts in this form;
- M550 inherited IBM's controller code or patent architecture;
- the M550 map-update/erase ordering is exactly Figure 6's ordering;
- IBM's patent establishes the first commercial SSD GC implementation;
- the 2009 priority date establishes first invention of garbage collection.

Thus:

```text
historically earlier manufacturer GC state-machine witness
    != direct M550 implementation evidence
    != genealogy
```

---

## Cross-case comparison

### Case 04 — mapped Flash / FTL identity

Case 04 establishes that logical identity can survive physical relocation. The IBM artifact provides a later, explicit managed-SSD sequence in which new physical embodiments are written and then the LBA/PBA address map is updated before the old group is erased.

Functional result:

```text
physical relocation
    + mapping/currentness update
    + later old-block erase
```

No claim is made that Case 04's early mapped-Flash designs descended into this IBM embodiment.

### Case 39 — GeckoFTL power-failure metadata recovery

Case 39 asks how mapping/validity metadata can be reconstructed after volatile controller state disappears in a research FTL.

The IBM patent is useful as a contrast: it contains a pre-shutdown metadata-copy path, but this slice does not demonstrate an arbitrary-crash reconstruction protocol for GC. Therefore:

```text
pre-shutdown preservation attempt
    != post-crash reconstruction proof
```

### Case 44 — deallocation / Trim

Case 44 shows that host deallocation semantics do not by themselves establish physical erase or sanitization. The IBM embodiment says a host deletion can result in a PI invalidity flag, after which later internal GC may recycle the page's containing group.

This is a functional bridge only. The patent passage does not justify asserting one exact ATA TRIM command path for every host deletion.

### Case 47 — sanitization / remanence

Ordinary GC may erase particular recycled blocks, but the IBM controller description is a capacity-management mechanism. It does not claim complete security purge of every embodiment, spare/remapped area, cache, or key-bearing structure.

Therefore:

```text
GC block erase
    != sanitize completion
```

### Case 150 — Crucial M550

Case 150's named-product claim remains product-specific: M550 publicly lists Active Garbage Collection and TRIM, while Crucial's maintained support material documents powered-idle maintenance opportunity.

This IBM evidence should be linked as **prior-art/control-architecture deepening**, not merged into the M550 historical record.

---

## Related-repository check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for combinations of `garbage collection`, `SSD`, `FTL`, `IBM`, and `Cideciyan` returned no dedicated matching case to reuse in this pass.

Accordingly, this evidence keeps only the retention-specific controller-state ordering. A complete history of SSD GC algorithms, commercial controller lineages, victim heuristics, write amplification, over-provisioning, and firmware families belongs primarily in `computing-archaeology` if pursued.

---

## Explicit non-claims

This evidence does **not** claim that:

1. IBM invented Flash garbage collection in 2009.
2. US8904261B2 was the first SSD patent to describe garbage collection.
3. Every embodiment in a patent was commercially shipped.
4. Crucial or Micron licensed or implemented this IBM design.
5. M550 uses IBM's C2 coding, strides, PI flags, or PI-count heuristic.
6. A host deletion is identical to ATA TRIM in every path described by the patent.
7. Setting a PI flag physically erases NAND.
8. Selecting a victim means erase has already begun.
9. Re-storing valid data automatically makes the new mapping durable.
10. Updating an in-memory address map proves sudden-power-loss durability.
11. The patent's pre-shutdown metadata copy is a transactionally atomic GC journal.
12. Old-block erase occurs synchronously with map update; the source explicitly permits later erase.
13. A block erased by ordinary GC proves whole-device sanitization.
14. The IBM artifact discloses M550 Device Sleep / idle GC eligibility.
15. Chronological precedence establishes technical influence or genealogy.
16. The patent's specific ECC/stride architecture is universal SSD practice.

---

## Claim ledger

| Claim | Type | Strength | Boundary |
| --- | --- | --- | --- |
| IBM patent family has 2009-12-17 priority and IBM assignee | H/P | strong | document-family chronology, not invention priority |
| IBM describes out-of-place invalidation followed by GC | H/P | strong | described controller design / background |
| PI flags mark overwritten/deleted pages invalid in the embodiment | H/P | strong | not universal SSD metadata format |
| PI counts can guide victim selection | H/P | strong | described stride-group heuristic only |
| still-valid data are recovered and re-stored before map update | H/P | strong | Figure 6 embodiment |
| address map update precedes old-block erase in Figure 6 | H/P | strong | described sequence, not M550 evidence |
| old block erasure may be immediate or later | H/P | strong | directly stated in patent |
| invalidity evidence != physical erase | E | strong | follows directly from separated states |
| new embodiment != published/current mapping != old embodiment erased | E | strong | bounded reconstruction from Figure 6 ordering |
| GC can leave reclamation debt after map/currentness transition | E | strong | project term; supported by deferred erase wording |
| detected power interruption triggers bounded metadata-preservation path | H/P | strong | patent embodiment only |
| that path proves arbitrary-power-cut GC atomicity | X | rejected | source does not establish it |
| IBM mechanism is the M550 algorithm | X | rejected | no evidence of identity/genealogy |
| ordinary GC proves sanitization | X | rejected | different completeness/authority contract |

---

## Remaining evidence debt

This slice closes only the generic **“find a first-party managed-SSD controller state-machine witness”** portion of Case 150's earlier debt. It does **not** close the product-specific M550 questions.

Remaining high-value work is now narrower:

1. obtain a Micron/Crucial or Marvell artifact that exposes the M550's actual victim-selection / map-publication / erase / crash-recovery behavior;
2. determine M550 GC eligibility across Active, Partial, Slumber, and DevSleep with product-specific evidence or instrumentation;
3. perform controlled power-cut testing at distinct migration phases to separate `new copy written`, `mapping made authoritative`, and `old block erased`;
4. trace the broader commercial-SSD GC genealogy in `computing-archaeology` rather than turning Case 150 into a general FTL history;
5. keep security sanitization validation separate from ordinary capacity-reclamation erase.

---

## Source

### P1 — IBM manufacturer-primary patent family

Roy D. Cideciyan, Evangelos S. Eleftheriou, Robert Haas, Xiao-Yu Hu, Ilias Iliadis, **“Data management in solid state storage devices,”** US20120266050A1 / US8904261B2, International Business Machines Corporation; priority 17 December 2009; U.S. filing 16 December 2010; application publication 18 October 2012.

Google Patents inspection copy:
<https://patents.google.com/patent/US8904261B2/en>

Relevant inspected portions:

- bibliographic record — priority, filing, publication, inventors, IBM assignee;
- background — page-write/block-erase asymmetry; write-out-of-place invalidation; generic garbage-collection sequence;
- controller embodiment — LBA/PBA map; PI flags; PI counts;
- Figure 6 description — victim selection; still-valid-data recovery; re-storage; address-map update; old-block erase; immediate-or-later erase timing;
- power-interruption passage — bounded pre-shutdown preservation of transient parity and current-map metadata.

The patent remains a design disclosure. Commercial deployment and M550 identity are not inferred.

### Prior-art guardrail already carried by canonical Case 150

Eran Gal and Sivan Toledo, **“Algorithms and Data Structures for Flash Memories,”** _ACM Computing Surveys_ 37(2), June 2005. Case 150 uses it only to establish that erase-unit management, not-in-place update, reclamation, and wear-management problem families predate the IBM/M550 records; no direct genealogy is asserted.
