# Case 04 deepening — Linux FTL erase completion, preparation, and transfer-unit reuse admission (2005 released source)

## Status

**Case 04 remains `grounded`.**

This packet closes one previously explicit Case-04 evidence debt at a bounded implementation level:

> find a named FTL implementation in which successful erase qualification is not merely inferred from raw-Flash status, but is connected in source code to the state that makes erased capacity eligible for subsequent relocation/reuse.

The bounded witness is the Linux `ftl.c` Flash Translation Layer driver in the **v2.6.12** release tag, whose tagged commit is `9ee1c939d1cb936b1f98e8d81aeffab57bae46ab`.

The central source-level result is stronger than the earlier generic reconstruction:

```text
erase request accepted
    != erase completed successfully
    != transfer unit prepared successfully
    != transfer unit admitted as relocation destination
```

In this implementation the allocator/reclaimer does not choose a transfer unit merely because an erase request returned successfully. The MTD erase callback must report `MTD_ERASE_DONE`, after which the transfer unit enters `XFER_ERASED`; `prepare_xfer()` must then successfully write the FTL transfer-unit header and BAM stub before setting `XFER_PREPARED`; and `reclaim_block()` chooses only `XFER_PREPARED` units as relocation destinations.

This is a **named software FTL implementation** and a source-level control path. It is not a claim about every M-Systems product, every PCMCIA card, NAND SSD firmware, or modern managed SSD.

---

## Why this slice is separate from the Micron raw-NAND packet

The preceding Case-04 Micron packet established a lower device-level boundary:

```text
ERASE no longer busy
    != ERASE passed
```

That packet deliberately stopped before allocator admission. It did **not** establish that a higher-level FTL waits for successful erase qualification before returning erased capacity to a reusable pool.

Linux `ftl.c` supplies the missing implementation-level seam. It exposes an explicit state machine whose reuse candidate must progress through:

```text
XFER_UNKNOWN
    -> XFER_ERASING
    -> XFER_ERASED
    -> XFER_PREPARED
    -> selected as relocation destination
```

with a failure branch:

```text
erase callback != MTD_ERASE_DONE
    -> XFER_FAILED
    -> not selected as a prepared transfer unit
```

The two packets therefore fit together functionally without asserting that Linux `ftl.c` drove the Micron NAND family used in the earlier packet.

---

## Source baseline and chronology discipline

### Historical record — the released source

The Linux v2.6.12 tag resolves to commit:

```text
9ee1c939d1cb936b1f98e8d81aeffab57bae46ab
```

The tag object describes it as the final 2.6.12 release. Linus Torvalds' release announcement is dated **17 June 2005**.

The source file identifies itself as:

> `A Flash Translation Layer memory card driver`

and says that it implements a disk-like block device with an apparent 512-byte block size for Flash memory cards.

The same source header records:

- a Linux-MTD port by David Woodhouse;
- an earlier source marker `ftl_cs.c 1.62 2000/02/01 00:59:04`;
- David A. Hinds as the initial developer of the original code;
- a legal note that the FTL format is patented by M-Systems and that M-Systems granted a royalty-free license for FTL-compatible drivers, file systems, and utilities using the PCMCIA FTL data formats for PCMCIA devices.

### Chronology limit

The 2005 release source is direct evidence for the behavior present in Linux v2.6.12.

The embedded `ftl_cs.c 1.62 2000/02/01` provenance line is evidence that this released driver derives from an older PCMCIA FTL code line. It is **not**, by itself, proof that every relevant state transition in the 2005 file was already identical in the 2000 revision.

Accordingly this packet uses **2005 released-source behavior** as the historical implementation baseline and treats the 2000 line only as provenance metadata.

---

## Historical / source record

## H1 — the implementation has explicit transfer-unit states

The v2.6.12 driver defines:

```c
#define XFER_UNKNOWN   0x00
#define XFER_ERASING   0x01
#define XFER_ERASED    0x02
#define XFER_PREPARED  0x03
#define XFER_FAILED    0x04
```

This is already enough to reject a one-bit model such as `free / not-free` for transfer-unit lifecycle.

The implementation distinguishes at least:

- a unit whose usable state is not yet established;
- an erase in progress;
- erase completion recognized as successful;
- successful post-erase FTL preparation;
- failure.

The repository terms `qualification`, `reuse admission`, and `maintenance authority` below are analytical labels. The historical source terms are the state names above.

---

## H2 — erase request acceptance is not erase completion

`erase_xfer()` first sets:

```c
xfer->state = XFER_ERASING;
```

It then allocates an `erase_info`, installs `ftl_erase_callback`, and submits the erase through the MTD device's `erase` method.

A return value of zero from that submission does **not** set `XFER_ERASED`. In this v2.6.12 implementation it increments the transfer unit's `EraseCount`, while the state remains governed by the asynchronous erase lifecycle.

This matters because the MTD interface itself defines separate erase states:

```c
MTD_ERASE_PENDING
MTD_ERASING
MTD_ERASE_SUSPEND
MTD_ERASE_DONE
MTD_ERASE_FAILED
```

So the source supports a direct anti-collapse rule:

```text
erase submission returned success
    != erase operation reached DONE
```

A secondary implementation detail follows:

```text
EraseCount increment in erase_xfer()
    != completion certificate
```

The counter mutation occurs on successful request submission, before the callback determines whether the asynchronous operation finished in `MTD_ERASE_DONE` or a failure state. This packet does not reinterpret `EraseCount` as a physical wear meter with perfect device-level truth; it is the driver's accounting variable.

---

## H3 — the callback turns MTD completion evidence into FTL state

`ftl_erase_callback()` locates the matching transfer unit and then branches on the MTD erase result:

```c
if (erase->state == MTD_ERASE_DONE)
    xfer->state = XFER_ERASED;
else {
    xfer->state = XFER_FAILED;
    ...
}
```

Thus the source-level state transition is explicit:

```text
MTD_ERASE_DONE
    -> XFER_ERASED

anything else reaching this failure branch
    -> XFER_FAILED
```

This is the named-implementation bridge that the raw-NAND packet did not supply: a lower-layer erase result is consumed by the FTL and changes higher-level reuse-control state.

But `XFER_ERASED` is still **not** the state that `reclaim_block()` selects for reuse.

---

## H4 — successful erase is followed by an FTL-specific preparation stage

`prepare_xfer()` is documented in the source as taking a `freshly erased transfer unit` and giving it an appropriate header.

The function first pessimistically sets:

```c
xfer->state = XFER_FAILED;
```

It then writes:

1. an FTL erase-unit header whose `LogicalEUN` is `0xffff` and whose erase count is recorded;
2. a BAM stub containing `BLOCK_CONTROL` entries.

Any write error returns before admission.

Only after those writes succeed does the function execute:

```c
xfer->state = XFER_PREPARED;
```

Therefore:

```text
erase completed successfully
    -> XFER_ERASED
    -> metadata preparation attempted
        -> preparation success -> XFER_PREPARED
        -> preparation failure -> XFER_FAILED / no admission
```

This closes an important ambiguity left by a simple `erase PASS -> free` story. Even an erased medium embodiment is not yet a usable transfer unit in this FTL until the control metadata needed by the format has been established.

---

## H5 — the reclaimer selects only `XFER_PREPARED` units

`reclaim_block()` loops over the configured transfer units.

Its state handling is ordered:

```text
XFER_UNKNOWN
    -> call erase_xfer()

XFER_ERASING
    -> mark that erase work is still queued

XFER_ERASED
    -> call prepare_xfer()

XFER_PREPARED
    -> eligible for the transfer-unit selection comparison
```

The candidate `xfer` is assigned only inside the `XFER_PREPARED` branch, where the code chooses among prepared units using erase count.

If no prepared unit exists but an erase is still queued, the code synchronizes/waits and loops. If there is neither a usable candidate nor queued work that can make progress, reclaim fails.

The named implementation therefore directly supports:

```text
XFER_ERASED
    != allocation/admission state

XFER_PREPARED
    -> eligible relocation destination
```

This is a bounded form of the Case-04 debt previously described as a `free-pool transition`: the pool here is specifically the driver's set of **prepared transfer units available for relocation**, not a universal SSD free-block pool.

---

## H6 — reclamation returns the expired embodiment to the transfer-unit lifecycle

After a prepared transfer unit is chosen, `copy_erase_unit()` copies the still-live blocks from a selected data erase unit into that transfer unit and swaps the relevant block pointers/accounting.

If that copy operation returns successfully, `reclaim_block()` then calls:

```c
erase_xfer(part, xfer);
```

where `xfer` now refers, after the swap, to the expired physical erase unit that must be recycled through the erase/preparation lifecycle.

This makes the reuse loop source-visible:

```text
prepared transfer unit
    -> receives still-live data
    -> logical/data-unit role changes through pointer swap
    -> old embodiment becomes transfer-unit candidate
    -> erase lifecycle begins
    -> successful erase
    -> FTL preparation
    -> prepared transfer unit again
```

The stable logical block interface is therefore sustained by repeated movement plus requalification of physical erase-unit capacity.

---

## H7 — ordinary free data blocks and transfer-unit readiness are different allocator layers

The same driver separately tracks:

```c
part->EUNInfo[i].Free
part->FreeTotal
```

and `find_free()` searches the BAM of current data erase units for a `BLOCK_FREE` entry.

This must not be collapsed with the transfer-unit state machine.

At least two allocation/reuse notions coexist in the implementation:

1. **free 512-byte data blocks inside current data erase units**, tracked through BAM/free counters;
2. **prepared transfer erase units** that can receive live data during reclamation.

Therefore even inside one historical FTL implementation:

```text
`free block`
    != `prepared transfer unit`
```

and the repository should not use `free pool` as though it were one universal historical data structure.

---

## H8 — restart rebuild treats a persistent transfer-unit header as preparation evidence

`build_maps()` scans erase-unit headers at initialization.

For a header that passes the FTL format check and has:

```c
LogicalEUN == 0xffff
```

it reconstructs the transfer unit in RAM as:

```c
XFER_PREPARED
```

Otherwise that transfer-unit slot is reconstructed as `XFER_UNKNOWN` and must pass through the erase/preparation path before it can later be selected.

This adds a persistence-horizon distinction:

```text
volatile XFER_PREPARED enum instance
    != sole evidence of preparedness

on-media FTL header state
    -> can reconstruct prepared eligibility after restart
```

### Important cut-point limit

`prepare_xfer()` writes the header before writing the BAM stub, whereas `build_maps()` visibly uses the header / `LogicalEUN == 0xffff` condition to classify a transfer unit as prepared.

That source ordering creates a **fault-injection question** at the cut between header write and completion of BAM-stub writes.

This packet does **not** claim that a power failure at that point necessarily produces a falsely admitted transfer unit. Establishing that would require the exact Flash programming semantics, lower-layer error behavior, and a restart/fault trace. The source ordering merely identifies the cut point that deserves testing.

---

## Engineering reconstruction

The historical source supports a more precise Case-04 transition model:

```text
old embodiment selected for reclamation
    -> live contents copied to prepared transfer unit
    -> role/pointer swap publishes new working placement in this implementation
    -> expired physical erase unit enters transfer lifecycle

XFER_UNKNOWN
    -> erase request submitted
    -> XFER_ERASING
    -> callback verdict
        -> failure: XFER_FAILED
        -> MTD_ERASE_DONE: XFER_ERASED
    -> FTL header + BAM preparation
        -> failure: no prepared admission
        -> success: XFER_PREPARED
    -> eligible as next relocation destination
```

From that implementation we can safely reconstruct:

```text
reclaim eligibility
    != erase request acceptance
    != erase completion evidence
    != post-erase format preparation
    != reuse admission
```

### A named implementation now closes the earlier generic gap

Before this packet Case 04 had:

```text
erase PASS
    != allocator free-pool insertion
```

as a conservative **unclosed boundary**.

Linux v2.6.12 FTL now shows one real implementation in which that boundary is explicit and has an additional stage:

```text
lower-layer erase DONE
    -> XFER_ERASED
    -> FTL metadata preparation
    -> XFER_PREPARED
    -> allocator/reclaimer may choose it
```

So the revised statement is not that `erase PASS always inserts into a free pool`. It is:

> **at least one named historical FTL makes successful erase completion a prerequisite for a separate FTL preparation step, and only the successfully prepared state is admitted as a reusable relocation resource.**

That is the bounded evidence claim.

---

## Historical record vs engineering reconstruction vs functional analogy vs philosophical interpretation

### Historical record

Directly source-supported claims in this packet are:

- Linux v2.6.12 contains a PCMCIA-style Flash Translation Layer memory-card driver;
- the source identifies David A. Hinds as original developer and records an older `ftl_cs.c` provenance line;
- the source's legal note ties the data format to M-Systems' PCMCIA FTL licensing statement;
- the driver has `UNKNOWN`, `ERASING`, `ERASED`, `PREPARED`, and `FAILED` transfer-unit states;
- asynchronous MTD erase completion is delivered through a callback;
- only `MTD_ERASE_DONE` converts a transfer unit to `XFER_ERASED` in that callback;
- `prepare_xfer()` writes FTL metadata after erase and sets `XFER_PREPARED` only after its writes succeed;
- `reclaim_block()` selects only `XFER_PREPARED` units as relocation destinations;
- initialization can reconstruct a transfer unit as prepared from an on-media FTL header whose `LogicalEUN` is `0xffff`.

### Engineering reconstruction

Repository-level terms include:

- `erase qualification`;
- `reuse admission`;
- `reuse authority`;
- `relocation capacity`;
- `control-state persistence horizon`.

These describe relations visible in the implementation but are not attributed as Linux/MTD/M-Systems actor vocabulary.

### Functional analogy

The state progression can be compared functionally to:

- raw-NAND ERASE ready/pass qualification in the Micron Case-04 packet;
- bad-block admissibility/currentness in Case 78;
- background reclamation opportunity/execution/completion in managed-SSD Case 150;
- repair/admission state machines in distributed-storage cases.

Those comparisons do not imply common lineage, common physical mechanism, or interchangeable failure semantics.

### Philosophical interpretation

The implementation sharpens one retention claim:

> reclaimed capacity is not simply `empty space`; it is space whose destructive transition and control metadata have been qualified enough for the current mechanism to trust it again.

That is an interpretation of the source-controlled engineering sequence. It is not historical vocabulary from Hinds, Linux MTD, PCMCIA, or M-Systems.

---

## Cross-case comparisons — functional only

### Case 04 chain 10 — Micron raw-NAND erase status

Micron supplies the lower-level distinction:

```text
not busy
    != erase success
```

Linux FTL supplies a higher software-level distinction:

```text
MTD_ERASE_DONE
    != XFER_PREPARED
    != selected relocation destination
```

Together they show why `erase complete` and `capacity reusable` should remain separate claims.

No claim is made that this Linux driver used the specific Micron NAND family from chain 10.

### Case 78 — NAND bad-block-management currentness

Case 78 shows that physical-media admissibility and persistent bad-block knowledge can themselves require retained metadata and reconstruction.

Linux FTL here shows another, narrower admission relation for a transfer unit after erase/preparation.

```text
media defect retirement
    != FTL transfer-unit preparation
```

They can both constrain reuse, but they are different control relations.

### Case 150 — managed-SSD garbage collection

Case 150 concerns background maintenance inside managed SSDs. Linux `ftl.c` is a host/software FTL for Flash memory cards and exposes its control state directly in source.

The comparison is only:

```text
maintenance opportunity/execution
    != maintenance qualification
    != reusable-capacity admission
```

It is not evidence that commercial SSD firmware copied this Linux state machine.

---

## Counterexamples and explicit non-claims

This packet does **not** claim that:

1. Linux v2.6.12 `ftl.c` is a NAND-SSD FTL;
2. the driver applies to every Flash medium or every MTD driver;
3. M-Systems wrote the Linux driver;
4. the v2.6.12 source is byte-for-byte identical to Hinds' 2000 `ftl_cs.c` revision;
5. the 2000 provenance line proves the full 2005 state machine already existed unchanged in 2000;
6. `MTD_ERASE_DONE` is a universal physical proof under every device/power-failure model;
7. incrementing `EraseCount` proves an erase physically completed;
8. `XFER_ERASED` is already reusable by the FTL reclaimer;
9. `XFER_PREPARED` means every byte in an erase unit is user-data free space;
10. `XFER_PREPARED` is the same thing as a free 512-byte data block;
11. the driver's transfer-unit pool is identical to a modern SSD over-provisioned free-block pool;
12. erase completion proves sanitization or secure deletion;
13. successful preparation proves user payload correctness under arbitrary faults;
14. the pointer/accounting swap is crash-atomic under arbitrary power loss;
15. source-code ordering proves lower-layer persistence ordering;
16. a header write reaching Flash proves the later BAM-stub writes also reached Flash;
17. `build_maps()` is proven safe under a power cut at every instruction of `prepare_xfer()`;
18. an interrupted preparation necessarily causes false reuse after restart;
19. the driver demonstrates a specific shipping M-Systems card's firmware behavior;
20. the driver demonstrates a modern SSD controller's internal policy;
21. the PCMCIA FTL specification and later SSD FTLs are one unchanged implementation lineage;
22. `free pool`, `transfer unit`, `free block`, `reserve block`, and `over-provisioning` are interchangeable historical terms;
23. successful erase alone is sufficient for FTL reuse in this implementation;
24. reuse admission means obsolete previous payload has been independently forensically verified as unrecoverable.

---

## Evidence-strength assessment

### Strong

- explicit released source-state names and transitions;
- callback branch on `MTD_ERASE_DONE`;
- post-erase `prepare_xfer()` writes before `XFER_PREPARED`;
- selection of only `XFER_PREPARED` transfer units in `reclaim_block()`;
- MTD's distinct pending/erasing/done/failed states;
- restart reconstruction of `XFER_PREPARED` from the on-media FTL header condition.

### Moderate / bounded

- interpreting `XFER_PREPARED` as **reuse/admission authority** for relocation capacity. This is a faithful engineering reconstruction of how `reclaim_block()` selects candidates, but `reuse authority` is repository vocabulary.
- using the source header's 2000 revision marker as code-line provenance rather than as proof of identical 2000 behavior.

### Still open

- physical-power-failure testing across the erase callback boundary;
- fault injection between FTL header write and BAM-stub completion;
- exact persistence guarantees of the lower MTD driver/media for those writes;
- named shipping-card behavior under the same cut points;
- modern NAND/SSD allocator equivalents.

---

## Effect on Case 04 evidence debt

The earlier highest-priority debt was:

> **Named FTL free-pool transition** — source-level firmware/patent/implementation evidence that a block joins a reusable/free pool only after successful erase qualification.

This packet closes that debt in a bounded historical implementation form:

```text
Linux v2.6.12 PCMCIA-style FTL

lower erase completion evidence
    -> XFER_ERASED
    -> FTL metadata preparation
    -> XFER_PREPARED
    -> eligible transfer-unit selection
```

The debt should therefore be replaced by narrower questions:

1. **fault trace across erase DONE -> preparation -> reuse** — interrupt the implementation at each cut point and observe restart classification;
2. **preparation cut-point durability** — test the header-before-BAM ordering and `build_maps()` reconstruction path;
3. **named shipping Flash card** — connect the source-level state machine to one identified physical product and lower Flash command/status behavior;
4. **modern NAND/SSD comparison** — find a firmware/open-controller implementation with a block-level free/reserve-pool transition after NAND ERASE qualification;
5. **retirement interaction** — show how erase failure and developed bad-block retirement intersect with this FTL's transfer-unit capacity accounting.

Case 04 remains `grounded`; this source-level closure does not justify a maturity promotion by itself.

---

## Related-repository routing

A fresh search of `tmzncty/computing-archaeology` for `ftl.c`, `Flash Translation Layer David Hinds`, and the Linux FTL driver found no dedicated packet to reuse.

Accordingly this file keeps only the retention-specific seam:

```text
erase result
    -> FTL preparation state
    -> reuse admission
```

Broader Linux-MTD history, PCMCIA FTL standardization, Hinds/Card Services history, M-Systems licensing/patent history, Flash-card product genealogy, and later SSD-controller evolution belong primarily in `computing-archaeology`.

---

## Sources

1. Linux kernel v2.6.12, `drivers/mtd/ftl.c`, released source at tag `v2.6.12`; tag resolves to commit `9ee1c939d1cb936b1f98e8d81aeffab57bae46ab`: <https://github.com/torvalds/linux/blob/v2.6.12/drivers/mtd/ftl.c>.
2. Linux kernel v2.6.12, `include/linux/mtd/mtd.h`, MTD erase-state definitions and `erase_info`: <https://github.com/torvalds/linux/blob/v2.6.12/include/linux/mtd/mtd.h>.
3. Git tag metadata for Linux `v2.6.12`, annotated as the final 2.6.12 release: <https://api.github.com/repos/torvalds/linux/git/ref/tags/v2.6.12>.
4. Linus Torvalds, `Linux 2.6.12`, linux-kernel release announcement, 17 June 2005, archived by LWN: <https://lwn.net/Articles/140441/>.
5. kernel.org Linux 2.6 source archive, preserving the 2.6.12 release family: <https://www.kernel.org/pub/linux/kernel/v2.6/>.

### Existing Case-04 packets used only for bounded comparison

- [`04-micron-2011-2014-raw-nand-erase-status-reuse-authority-deepening.md`](04-micron-2011-2014-raw-nand-erase-status-reuse-authority-deepening.md)
- [`04-m-systems-2001-2003-interrupted-erase-recovery-deepening.md`](04-m-systems-2001-2003-interrupted-erase-recovery-deepening.md)
- [`04-trueffs-2003-2004-mapping-power-failure-reconstruction-deepening.md`](04-trueffs-2003-2004-mapping-power-failure-reconstruction-deepening.md)

No genealogy among those implementations is inferred merely from the functional comparison.