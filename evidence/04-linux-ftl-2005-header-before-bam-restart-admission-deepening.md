# Case 04 deepening — Linux v2.6.12 header-before-BAM restart admission

**Status:** Case 04 remains `grounded`.

This slice closes the source-level question left open by the earlier Linux FTL reuse-admission packet: `prepare_xfer()` writes the transfer-unit header before it finishes writing the BAM control stub, while restart `build_maps()` classifies a valid `LogicalEUN == 0xffff` header as `XFER_PREPARED`. The question is whether that source ordering, by itself, shows that restart can expose an incompletely prepared transfer unit to ordinary data allocation or unsafe relocation.

The bounded answer from Linux v2.6.12 plus the PCMCIA/JEIDA Release 7.0 format is narrower: **the header is a restart admission marker for the transfer-unit role, but a prepared transfer unit is not an ordinary data-unit free-space source; before promotion, `copy_erase_unit()` reconstructs the destination contents and writes a complete BAM derived from the source.** This closes the software/control-path seam while leaving lower-media torn-write and program-order behavior open.

## Historical / source record

### Linux v2.6.12 writes the header before the BAM stub

In `drivers/mtd/ftl.c`, `prepare_xfer()` begins by setting the volatile transfer-unit state pessimistically to `XFER_FAILED`.

It then writes a fresh FTL erase-unit header:

```text
LogicalEUN = FFFFh
EraseCount = current transfer-unit count
```

Only after that header write succeeds does the function write `BLOCK_CONTROL` (`00000030h`) entries into the BAM positions that correspond to FTL control structures. Only after the loop succeeds does the volatile state become `XFER_PREPARED`.

So the uninterrupted runtime path is:

```text
freshly erased unit
    -> write EUH with LogicalEUN = FFFFh
    -> write BAM control stub
    -> XFER_PREPARED
```

### Restart classifies the header before inspecting a transfer-unit BAM

`build_maps()` scans erase-unit headers first.

For a header that passes the `FTL100` format test:

- a unique in-range `LogicalEUN` becomes a data erase unit;
- `LogicalEUN == FFFFh` becomes an `XFER_PREPARED` transfer unit;
- other non-data / duplicate cases become `XFER_UNKNOWN`.

The later BAM-reading loop iterates over `part->DataUnits` / `EUNInfo[]`, not over `XferInfo[]`. A transfer unit admitted from `LogicalEUN == FFFFh` therefore does **not** have its BAM consumed to build the live Virtual Block Map at startup.

This establishes a real asymmetry:

```text
restart admission of transfer-unit role
    is header-derived

restart reconstruction of live data mapping
    is data-unit BAM-derived
```

### Prepared transfer units are not ordinary free data blocks

`find_free()` searches `EUNInfo[]` data erase units and their BAMs for ordinary free 512-byte blocks. It does not allocate host data directly from `XferInfo[]`.

`XFER_PREPARED` units are instead selected by `reclaim_block()` as relocation destinations.

Therefore:

```text
XFER_PREPARED
    != ordinary BLOCK_FREE entry
    != direct host-write allocation source
```

### Relocation overwrites the destination BAM before promotion

`copy_erase_unit()` does not trust a prepared transfer unit's pre-existing BAM as the authority for the relocated data.

Its sequence is:

```text
source BAM read
    -> destination LogicalEUN = 7FFFh
    -> source live data copied to corresponding destination blocks
    -> source-derived BAM written to destination
    -> destination LogicalEUN changed to source LogicalEUN
    -> runtime source/transfer roles swapped
```

The source BAM's `BLOCK_CONTROL` entries are preserved in that copied BAM. The PCMCIA/JEIDA format defines `00000030h` as the allocation-information value for blocks that contain FTL control structures, including the Erase Unit Header and BAM.

The standard's Unit Recovery description also says that a properly prepared Transfer Unit has erased data/map areas plus initialized global EUH fields, and that its BAM contains only Control entries for the FTL structures for that Transfer Unit. Before data copy it moves to `7FFFh`; after successful transfer it receives the source `LogicalEUN`.

## Engineering reconstruction

### The earlier apparent seam

The earlier packet conservatively left this question open:

```text
header write succeeds
    -> power loss before BAM-stub loop completes
    -> restart sees FFFFh
    -> build_maps() reconstructs XFER_PREPARED
    -> ?
```

Source inspection now shows that the `?` should not be filled with “therefore ordinary data allocation consumes a partially prepared BAM.”

Instead, within this implementation:

```text
header-derived XFER_PREPARED
    -> eligible only as a transfer-unit relocation destination
    -> destination BAM is rebuilt from source before LogicalEUN promotion
```

That gives a bounded software-level closure:

```text
restart admission from FFFFh header
    != proof BAM stub had completed before the crash

but also

missing/partial pre-relocation BAM stub
    != evidence that live data mapping will be built from that partial BAM
```

### Why the BAM stub can be regenerated in the observed path

The PCMCIA format reserves `30h` allocation entries for blocks containing FTL control structures.

Linux's `prepare_xfer()` writes those control entries to a freshly erased transfer unit. If restart happens after the header but before all of those entries have been written, the unit may still be classified as prepared from its header. But the next successful `copy_erase_unit()`:

1. derives the destination block-state map from the source unit's BAM;
2. copies live payload blocks according to that source BAM;
3. writes the complete source-derived BAM to the destination;
4. only then promotes the destination from `7FFFh` to the source logical identity.

At the software-state level, the pre-copy BAM stub is therefore **not the final publication record for the relocated data**.

### Retention relation exposed by the implementation

The sharper Case-04 relation is:

```text
persistent role marker
    != complete final relocation metadata

restart role admission
    != logical-data publication

preparation metadata
    can be provisional
    if later promotion is gated by reconstruction of authoritative metadata
```

For repository terminology, **role admission marker**, **provisional preparation metadata**, and **promotion-gated reconstruction** are engineering-reconstruction terms. They are not historical Linux/PCMCIA vocabulary.

## Functional analogy

A narrow structural analogy exists with distributed or journaled systems:

```text
early durable marker
    != final current-state publication
```

and:

```text
restart can admit an object into an intermediate role
    without treating its intermediate metadata
    as the final authority for client-visible state
```

The analogy stops there. This does not make PCMCIA FTL a consensus protocol, journal, WAL, or modern SSD firmware lineage.

## Philosophical interpretation

The mechanism sharpens a retention point already visible elsewhere in Case 04: persistence can depend on retaining **enough state to recover a role**, rather than retaining every transient working representation exactly.

Here the durable `FFFFh` header can be sufficient to re-establish “this erase unit is available as a transfer unit” even when the exact pre-crash preparation sequence did not reach its final volatile state. The later relocation path reconstructs the metadata that matters before promotion to a logical data identity.

That interpretation remains downstream of the source record.

## Explicit non-claims

This packet does **not** claim that:

1. arbitrary torn EUH writes are accepted safely;
2. a successful MTD `write()` call is a hardware persistence barrier;
3. the underlying Flash guarantees atomic 16-bit, 32-bit, header-sized, or page-sized programming;
4. a power loss cannot leave partially programmed `LogicalEUN` or BAM entries;
5. reprogramming a partially written BAM entry is always electrically legal on every medium;
6. the source-level order implies exact lower-media persistence order;
7. the PCMCIA specification guarantees Linux's implementation-level crash behavior;
8. every FTL may reconstruct transfer-unit eligibility from a header alone;
9. `XFER_PREPARED` is equivalent to an SSD free-block-pool member;
10. the pre-copy BAM stub is irrelevant under every fault model;
11. the path is safe if the source BAM itself is corrupt;
12. the path is safe if destination data/program operations partially fail;
13. the driver validates byte-for-byte equivalence before duplicate-`LogicalEUN` collapse;
14. this proves behavior of any named shipping M-Systems card;
15. this proves behavior of modern NAND SSD firmware.

## What is closed and what remains open

Closed at **source/control-path level**:

- restart may reconstruct `XFER_PREPARED` from the `FFFFh` header without reading the transfer-unit BAM;
- that state does not feed ordinary `find_free()` host-data allocation;
- the relocation path writes a source-derived complete BAM before destination logical-identity promotion;
- therefore “header-before-BAM” is not, by itself, evidence that a partial BAM becomes the live logical mapping.

Still open at **lower-media / experiment level**:

1. torn or partially programmed EUH field behavior;
2. persistence ordering between the EUH write and later BAM writes;
3. whether a partially programmed `30h` control entry can always be safely completed on the actual medium;
4. reset/power-loss traces at each write boundary;
5. a named physical PC Card / MTD driver witness.

The next highest-value trace is therefore no longer a generic `header -> BAM -> restart` question. It is a lower-layer fault matrix that distinguishes:

```text
clean durable FFFFh header + incomplete control stub
    from
partially programmed / unreadable header
    from
program failure while rebuilding the destination BAM
    from
failure after BAM reconstruction but before LogicalEUN promotion
```

## Related-repository routing

A fresh search of `tmzncty/computing-archaeology` for `prepare_xfer build_maps`, `LogicalEUN 7FFF FFFF`, and `PCMCIA FTL BAM transfer unit` found no dedicated packet to reuse.

Broader PC Card, MTD, Flash-programming, and FTL genealogy remains routed there. This packet keeps only the retention/control seam.

## Sources

1. Linux kernel v2.6.12, `drivers/mtd/ftl.c`, especially `build_maps()`, `prepare_xfer()`, `copy_erase_unit()`, `reclaim_block()`, and `find_free()`: <https://github.com/torvalds/linux/blob/v2.6.12/drivers/mtd/ftl.c>.
2. Linux kernel v2.6.12, `include/linux/mtd/ftl.h`, especially `erase_unit_header_t` and `BLOCK_CONTROL`: <https://github.com/torvalds/linux/blob/v2.6.12/include/linux/mtd/ftl.h>.
3. PCMCIA/JEIDA, *PC Card Standard Release 7.0, Volume 7: Media Storage Formats Specification*, first printing February 1999, §§5.1.2.5, 5.1.5, 5.1.6.3: <https://0x04.net/~mwk/doc/pcmcia/volumes/07-ms-70.pdf>.
4. Existing Case-04 implementation packet: [04-linux-ftl-2005-transfer-unit-reuse-admission-deepening.md](04-linux-ftl-2005-transfer-unit-reuse-admission-deepening.md).
5. Existing duplicate-identity packet: [04-pcmcia-1999-linux-2005-duplicate-logicaleun-recovery-boundary-deepening.md](04-pcmcia-1999-linux-2005-duplicate-logicaleun-recovery-boundary-deepening.md).
