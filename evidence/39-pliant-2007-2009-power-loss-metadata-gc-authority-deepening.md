# Case 39 Deepening — Pliant 2007–2009 Power-Loss Metadata Rebuild and Garbage-Collection Authority

## Purpose

This evidence record deepens [`cases/39-geckoftl-power-failure-metadata-recovery.md`](../cases/39-geckoftl-power-failure-metadata-recovery.md) with an earlier controller-architecture disclosure that directly connects post-power-loss metadata reconstruction to the validity and free-space relations later used by garbage collection.

The bounded question is:

> By the late 2000s, did a flash-controller design explicitly distinguish volatile working translation/validity tables from Flash-resident recovery evidence, and reconstruct enough free/valid/currentness state after power loss for ordinary allocation and later garbage collection to have trustworthy authority again?

**Result: yes, for the disclosed Pliant architecture.** A Pliant Technology patent family with a **27 December 2007 priority date**, filed **8 April 2008** and published as U.S. applications on **2 July 2009**, describes volatile Forward/Reverse Tables in controller DRAM, Flash-resident SuperBlock/SuperPage metadata, power-loss reconstruction of mapping/currentness/validity state, reconstruction of the SuperBlock Freelist, and a paired garbage-collection mechanism that consumes the Reverse Table's invalid-page counts and Freelist state.

**Status:** `bounded deepening complete`.

This is evidence of a disclosed controller architecture. It is **not** evidence that a named Pliant SSD shipped with exactly this firmware, that every commercial SSD uses this recovery path, or that GeckoFTL, Crucial/Micron M550 firmware, or any later controller descended from this design.

---

## Source set and evidence classes

### Source A — Pliant, `US20090172262A1`, metadata rebuild after power loss

**Document:** Aaron K. Olbrich and Douglas A. Prins, _Metadata rebuild in a flash memory controller following a loss of power_, U.S. application `US20090172262A1`, later patent family including `US8621137B2`.

**Priority:** 27 December 2007.

**Filed:** 8 April 2008.

**Published:** 2 July 2009.

**Contemporaneous assignee record:** Pliant Technology, Inc.; the family later passed into the SanDisk enterprise patent portfolio.

**Primary record:** <https://patents.google.com/patent/US20090172262A1/en> ; grant-family transcription: <https://patents.google.com/patent/US8621137B2/en>.

**Evidence class:** `H/P` for the disclosed mechanism and chronology.

### Source B — Pliant, `US20090172258A1`, paired garbage-collection controller design

**Document:** Aaron K. Olbrich and Douglas A. Prins, _Flash memory controller garbage collection operations performed independently in multiple flash memory groups_, U.S. application `US20090172258A1`, later `US8533384B2`.

**Priority:** 27 December 2007.

**Filed:** 8 April 2008.

**Published:** 2 July 2009.

**Original assignee record:** Pliant Technology LLC / assignment to Pliant Technology, Inc. on filing; later SanDisk assignments belong to the subsequent legal history.

**Primary record:** <https://patents.google.com/patent/US20090172258A1/en>.

**Evidence class:** `H/P` for the disclosed garbage-collection and controller-state mechanism.

### Why the two documents may be compared here

The applications share inventors, the same 27 December 2007 provisional-priority family, the same controller terminology/figures, and explicit cross-references to the companion applications. The safe use is therefore to reconstruct the **documented architecture family**.

This does **not** license a stronger claim that every claim in one patent is necessarily implemented together with every claim in the other in a shipped product.

---

## Historical record

### H/P — the controller keeps important translation and validity working state in volatile DRAM

The power-loss section states that `Data Path DRAM 107` stores the `Forward` and `Reverse Tables` because DRAM access is faster than Flash access. It then states the consequence directly: because that DRAM is volatile, unexpected power loss requires those tables to be rebuilt, along with the SuperBlock Metadata Table for the currently open SuperBlock.

This is a direct late-2000s controller-design witness for:

```text
nonvolatile NAND payload
    !=
volatile controller translation / validity working state
```

The source does not merely infer this from generic DRAM volatility; it supplies a named recovery procedure for the tables.

### H/P — Flash-resident metadata is the reconstruction substrate

The disclosed recovery path rebuilds:

- open-SuperBlock metadata from per-SuperPage metadata stored in Flash;
- Forward and Reverse Tables from Flash-resident SuperBlock Metadata Tables plus the rebuilt open-SuperBlock table;
- free-space state by classifying SuperBlocks from Flash-resident open/closed flags.

Thus the normal DRAM representation and the retained recovery substrate are explicitly different objects.

A bounded representation is:

```text
volatile Forward / Reverse Tables lost
        +
Flash-resident SuperBlock / SuperPage metadata survives
        ↓
scan + classify + compare timestamps
        ↓
reconstituted mapping / validity / free-space working state
```

### H/P — open, closed, and erased blocks carry different recovery semantics

The SuperBlock Metadata Table includes a SuperBlock timestamp, erase count, `Open Flag`, and `Closed Flag`.

The paired controller description says the table is written to Flash at three transitions:

1. when a SuperBlock is erased and placed on the Freelist;
2. when it is opened, with `Open Flag` set so the open block can be identified after unexpected power loss;
3. when it is closed, with `Closed Flag` set and the filled table copied back to Flash.

The two flags therefore encode three documented states:

```text
both clear         -> free / erased
open=1, closed=0   -> open
open=1, closed=1   -> closed
```

This matters because restart reconstruction does not treat all surviving Flash blocks alike.

### H/P — an erased-state witness can reconstruct free-space admission

During recovery, the controller checks the Open/Closed flags. If both are clear, the source interprets the SuperBlock as erased and places its identifier on the `SuperBlock Freelist`.

The Freelist is separately defined as containing identifiers of SuperBlocks that are free and therefore available to be written; the garbage-collection document defines free SuperBlocks as erased and available for future writes.

The retention relation is therefore narrower than `Flash bytes survived`:

```text
retained block-state metadata
        ↓
restart classification as erased/free
        ↓
re-admission to volatile Freelist
        ↓
allocation authority restored
```

The recovery operation is reconstructing **reuse authority**, not physically erasing the block at that moment.

### H/P — timestamps reconstruct currentness when more than one physical embodiment names the same LBA

For closed SuperBlocks, recovery walks Flash-resident metadata and uses LBAs as Forward-Table lookup keys. If the same LBA is encountered more than once, the controller compares SuperBlock timestamps. The older physical embodiment is marked invalid in the Reverse Table, while the Forward Table is pointed at the newer SuperPage and that new location is marked valid.

If competing writes occur in the same SuperBlock, the procedure descends to SuperPage timestamps.

This is a direct historical example of:

```text
multiple surviving physical embodiments
        !=
one self-evident current logical value
```

Currentness is reconstructed from retained ordering evidence.

### H/P — open blocks require finer-grained recovery because the closed-block summary is incomplete

The source explicitly says that if a SuperBlock was still open at power loss, the Flash-resident SuperBlock Metadata Table is not sufficient to determine the LBAs assigned to its SuperPages because the complete table is written only when the SuperBlock is closed.

The recovery procedure therefore examines per-SuperPage metadata to repopulate the open block's table. The rebuilt open block is assigned a current timestamp so its written pages can be compared conservatively against older closed-block versions.

This gives a useful relation:

```text
physical pages in an open block survived
        !=
closed-block summary metadata was complete
```

and therefore:

```text
coarse retained summary
        may require
finer-grained retained witnesses during restart
```

### H/P — the Reverse Table is both a recovered validity relation and an input to garbage collection

The paired garbage-collection application describes a Reverse Table with:

- a Valid bit for each SuperPage;
- a Count field giving the number of invalid SuperPages in each SuperBlock;
- a timestamp used by the rebuild process;
- an erase count that may be used for wear-leveling / selection policy.

The Count is explicitly used for garbage collection. When GC begins, the controller checks Reverse-Table Count fields while searching for candidate SuperBlocks.

Thus the same broad controller architecture does not treat validity metadata as a restart-only artifact. It is ordinary maintenance state.

### H/P — free-space state also drives garbage-collection urgency

The paired GC application defines a `SuperBlock Freelist Counter` and compares it with critical and non-critical thresholds. Low free-block count can initiate non-critical GC or move the controller into critical GC, with different scheduling priority relative to host operations.

After a chosen block's live data have been consolidated and the block erased, the described GC path writes a fresh metadata table containing retained erase/defect information and only then places the SuperBlock back on the Freelist and increments the Freelist Counter.

Accordingly:

```text
physical block exists
    !=
block is on Freelist
    !=
GC has completed reuse admission for that block
```

### H/P — power-loss recovery reconstructs authority that later maintenance consumes

The two companion disclosures together support a bounded controller-state dependency:

```text
Flash-resident open/closed/erased flags
    + timestamps
    + per-page LBA metadata
        ↓ restart reconstruction
Forward Table currentness
    + Reverse Table valid/invalid state
    + Freelist membership
        ↓ ordinary controller operation
allocation decisions
    + GC urgency
    + GC victim selection
```

This is stronger than merely saying “the mapping table comes back.” The recovered state includes relations governing **which embodiment counts, which pages are obsolete, and which blocks may be reused**.

It is still weaker than saying that an interrupted garbage-collection transaction is resumed exactly where it stopped.

---

## Chronology and prior-art boundary

The date vocabulary must stay explicit.

```text
27 Dec 2007   Pliant provisional priority
08 Apr 2008   Pliant U.S. nonprovisional filings
10 Apr 2009   Park et al. paper released publicly
02 Jul 2009   Pliant applications published publicly
05 Dec 2011   ITRI filing used elsewhere in Case 39
Jun 2014      DCR publication
2015–2017     Logarithmic Gecko / GeckoFTL / patent publication sequence
```

Therefore:

- **Pliant has an earlier design/priority date than Park's 2009 publication**;
- **Park is the earlier inspected public publication**, because the Pliant applications were not published until July 2009;
- patent priority/filling chronology must not be silently rewritten as public availability;
- none of these dates establishes direct genealogy into GeckoFTL.

The safe prior-art consequence is:

> By a 2007-priority / 2009-public controller disclosure, volatile Forward/Reverse mapping-validity tables, Flash-resident reconstruction metadata, restart-time currentness selection, and Freelist reconstruction were explicit parts of a flash-controller design. GeckoFTL therefore cannot be treated as the origin of the generic idea that controller mapping/validity/free-space authority may need reconstruction after power loss.

GeckoFTL's distinct bounded contribution remains its later metadata-scaling problem, PVB/Logarithmic-Gecko organization, completion/admissibility witnesses, and pinned-run recovery dependencies.

---

## Engineering reconstruction

The grounded historical mechanism supports these project-level distinctions.

### `payload survival ≠ translation-state survival`

The controller can retain NAND data while losing Forward/Reverse Tables in volatile DRAM.

### `translation-state loss ≠ permanent relation loss`

Flash-resident block/page metadata and ordering evidence can regenerate the working relation.

### `readable physical embodiment ≠ current logical embodiment`

When the same LBA appears in multiple surviving locations, timestamps and reconstructed validity state decide which one becomes current in the Forward Table.

### `erased physical state ≠ reconstructed free-list membership`

The source separately reconstructs volatile Freelist membership from retained state flags.

### `free-list membership ≠ erase operation`

At recovery, a block is admitted to the reconstructed Freelist because retained metadata identifies it as already erased; the recovery step is not itself the physical erase.

### `recovered validity state ≠ payload integrity validation`

Rebuilding Forward/Reverse tables determines which location should count. It does not by itself prove that the selected NAND cells are error-free or that every interrupted host write had reached a durable commitment point.

### `reconstructed GC authority ≠ resumed interrupted GC workflow`

The paired disclosures show reconstructed validity/free-space relations that later GC consumes. They do not, in the inspected passages, preserve a GC program counter or prove exact continuation of an interrupted relocation/erase sequence.

### `retained recovery substrate ≠ zero restart work`

The design scans block/page metadata, compares timestamps, reconstructs tables, and re-admits free blocks before volatile working state is restored.

---

## Functional comparison

### A — Case 39 GeckoFTL

Both the Pliant controller disclosure and GeckoFTL separate volatile working metadata from retained Flash evidence used after interruption.

The bounded similarity is:

```text
volatile interpretation / validity state disappears
        ↓
retained Flash metadata is examined
        ↓
working currentness / validity relations are reconstructed
```

The mechanisms differ. Pliant uses Forward/Reverse Tables, SuperBlock/SuperPage metadata, flags, timestamps, and a Freelist. GeckoFTL uses page-associative mapping structures, PVB/Logarithmic Gecko, run directories, preamble/postamble qualification, checkpoints, and pinned-run dependencies.

**No genealogy is claimed.**

### A — Case 150 managed-SSD garbage collection

Case 150 separates host-visible allocation from controller-internal validity, over-provisioning, relocation, erase, and reclamation authority. The Pliant evidence sharpens one prerequisite: after a volatile-state loss, controller maintenance cannot safely rely on an imagined in-memory validity/free-space state; that authority may have to be reconstructed first.

Functional bridge only:

```text
reconstructed current/valid/free relation
        -> can support later GC decisions
```

This does **not** show that Crucial/Micron M550 used Pliant firmware, Pliant table formats, or the same GC scheduler.

### A — Case 145 JFFS2 reuse admission

JFFS2 and the Pliant controller both distinguish physical medium state from a later admission relation saying space may be reused. The layer, evidence carrier, and state machine are different: JFFS2 is a filesystem over MTD with CLEANMARKER/reuse-list semantics; Pliant's disclosure is controller-internal Flash metadata and DRAM-table reconstruction.

---

## Philosophical interpretation

The bounded conceptual point is not that “memory reconstructs itself” in a general sense.

The exact technical fact is narrower:

> the Flash may retain both payload and traces about prior controller state while the volatile relations that made those traces operationally legible have disappeared; restart work reconstitutes a currentness/validity/reuse authority from those retained traces.

This supports a project-level distinction between **material survival** and **renewed operational authority**. It does not prove a theory of human memory, tertiary retention, or archive.

---

## Explicit non-claims

1. `US20090172262A1` is a patent/application disclosure, not proof of a named shipping SSD's firmware behavior.
2. The 27 December 2007 priority date is not a 2007 public-publication date.
3. Pliant's earlier priority does not make the later July 2009 publication publicly prior to Park's April 2009 paper.
4. Similarity to Park, ITRI, DCR, or GeckoFTL does not establish transmission or code genealogy.
5. Forward/Reverse Tables are not asserted to be universal FTL structures.
6. SuperBlock/SuperPage terminology is architecture-specific, not generic NAND vocabulary.
7. Rebuilt Forward Table state does not prove payload ECC integrity.
8. A timestamp comparison does not prove host-level transaction durability.
9. Reconstructed validity is not secure deletion or sanitization evidence.
10. Reconstructed Freelist membership is not evidence that recovery itself erased the block.
11. A free block is not the same thing as an arbitrary host-visible free LBA.
12. Reverse-Table invalidity is not equivalent to T13 TRIM semantics.
13. The paired patent documents do not prove that every claimed submechanism shipped together.
14. The documents do not prove exact power-fail behavior of a specific Pliant/SanDisk product revision.
15. The documents do not establish independent fault-injection compliance.
16. The inspected passages do not prove exact resumption of an interrupted GC program step.
17. The Pliant design is not evidence that Crucial M550 used the same FTL or GC architecture.
18. The Pliant design is not evidence that GeckoFTL copied Pliant.
19. Patent grant/publication is not the same event as product introduction or deployment.
20. Later assignment into a SanDisk portfolio must not be back-projected into the 2007–2009 design as “SanDisk's 2007 controller.”

---

## Claims strengthened by this slice

### G-39.23 — `volatile Forward/Reverse Tables ≠ nonvolatile recovery substrate`

**Evidence:** the disclosure stores working Forward/Reverse Tables in volatile DRAM but rebuilds them from Flash-resident SuperBlock/SuperPage metadata after unexpected power loss.

**Status:** grounded for the disclosed Pliant architecture.

### G-39.24 — `surviving duplicate embodiments ≠ self-evident currentness`

**Evidence:** recovery compares block/page timestamps and marks older duplicate LBA embodiments invalid while repopulating the Forward Table with the newer location.

**Status:** grounded.

### G-39.25 — `erased-state evidence -> reconstructed Freelist authority`

**Evidence:** open/closed flags identify a SuperBlock that was erased at failure; recovery places that block on the SuperBlock Freelist.

**Status:** grounded architecture-specific relation.

### G-39.26 — `recovered validity/free-space authority -> later GC input`

**Evidence:** the companion GC disclosure uses Reverse-Table invalid counts to select GC victims and Freelist count to trigger/priority-control GC; after GC erase, Freelist admission is an explicit completion step.

**Status:** grounded functional dependency within the disclosed architecture family.

### G-39.27 — `open block != closed-summary recoverability`

**Evidence:** the disclosure says a still-open block's Flash-resident SuperBlock summary is insufficient, so recovery reconstructs it from per-SuperPage metadata.

**Status:** grounded.

### G-39.28 — `priority date ≠ public availability`

**Evidence:** the Pliant family claims 27 December 2007 priority but the U.S. applications were published 2 July 2009, after Park et al.'s 10 April 2009 publication.

**Status:** grounded chronology guardrail.

### G-39.29 — `controller metadata rebuild ≠ interrupted-GC transaction replay`

**Evidence:** the inspected documents reconstruct currentness/validity/Freelist state and describe ordinary GC consumption of those structures, but do not preserve an exact GC execution cursor across power loss.

**Status:** explicit limit.

---

## Related-repository duplication check

Fresh searches of `tmzncty/computing-archaeology` for `US8621137` and `metadata rebuild power loss flash controller` returned no dedicated reusable packet.

**Routing consequence:** this repository keeps only the retention-specific seam:

```text
Flash-resident state witnesses
    -> restart currentness/validity/free-space reconstruction
    -> renewed allocation / GC authority
```

A broader history of Pliant Technology, enterprise SSD controller architectures, the full 2007 provisional family, Pliant-to-SanDisk corporate/product genealogy, controller microarchitecture, and shipping-product adoption belongs in `computing-archaeology` if developed.

---

## Remaining debt after this deepening

Higher-value follow-ups remain:

- a **named shipping controller/product** with public documentation or source showing its actual restart metadata-recovery contract;
- independent power-cut / fault-injection evidence distinguishing mapping recovery, payload durability, and GC/reclamation correctness;
- exact controller behavior if power fails during a GC relocation or erase, rather than merely before later GC consumes reconstructed state;
- cross-vendor evidence showing which recovery relations recur and which are Pliant-specific;
- standards-visible or host-visible reporting of controller metadata-recovery failure, if any.

Case 39 should remain `grounded`; this slice sharpens its prior-art and controller-maintenance boundary rather than changing maturity.

---

## Sources

### Primary / period technical sources

- Aaron K. Olbrich and Douglas A. Prins, _Metadata rebuild in a flash memory controller following a loss of power_, `US20090172262A1`, priority 27 December 2007, filed 8 April 2008, published 2 July 2009: <https://patents.google.com/patent/US20090172262A1/en>. Grant-family transcription: <https://patents.google.com/patent/US8621137B2/en>.
- Aaron K. Olbrich and Douglas A. Prins, _Flash memory controller garbage collection operations performed independently in multiple flash memory groups_, `US20090172258A1`, priority 27 December 2007, filed 8 April 2008, published 2 July 2009: <https://patents.google.com/patent/US20090172258A1/en>.

### Existing Case 39 chronology anchors

- Jung-Wook Park, Seung-Ho Park, Gi-Ho Park, Shin-Dug Kim, _An integrated mapping table for hybrid FTL with fault-tolerant address cache_, IEICE Electronics Express 6(7), released 10 April 2009, DOI `10.1587/elex.6.368`: <https://doi.org/10.1587/elex.6.368>.
- Chi Zhang et al., _Deterministic Crash Recovery for NAND Flash Based Storage Systems_, DAC 2014, DOI `10.1109/DAC.2014.6881475` / `10.1145/2593069.2593124`.
- Niv Dayan, Philippe Bonnet, and Stratos Idreos, _GeckoFTL: Scalable Flash Translation Techniques For Very Large Flash Devices_, SIGMOD 2016, DOI `10.1145/2882903.2915219`.
