# Case 78 Deepening — Linux MTD Mirrored and Versioned Flash Bad-Block Tables (2004)

## Scope

This addendum deepens [`Case 78`](../cases/78-micron-nand-bad-block-marker-management.md) at one narrow boundary left open by the original ONFI/Micron case: **once bad-block exclusion knowledge has itself been copied into NAND, how can that control metadata be updated without treating one on-flash table as an infallible single point of truth?**

The bounded historical witness is the Linux MTD NAND bad-block-table implementation and its developer documentation in 2004. This is not a general Linux-MTD history, not a claim that Linux invented bad-block tables, and not evidence about a proprietary SSD controller. It is useful because the source exposes the persistence structure of the BBT itself: flash-resident primary/mirror copies, per-copy version state, reserved BBT blocks, update/reconciliation paths, and explicit limits on what mirroring guarantees.

---

## Historical record

### H/P — 2004 Linux MTD documentation treats a flash BBT as retained control state with its own redundancy

Thomas Gleixner's Linux MTD NAND driver documentation, copyright 2004, distinguishes the ordinary RAM BBT from an optional/required BBT stored in Flash. For the default Flash-BBT path it documents:

- per-chip BBT storage;
- two bits per block;
- automatic placement at the end of the chip;
- **mirrored tables with version numbers**;
- four blocks reserved at the end of the chip for automatic BBT placement.

The same documentation says the mirrored copy exists to allow BBT updates without losing the table, and recommends write support only with mirrored tables plus version control. It describes the version field as the device-side currentness discriminator and says this arrangement reduces the risk of losing bad-block information during update.

**Primary project documentation:** Linux MTD, *MTD NAND Driver Programming Interface*, `Bad block table support`, Thomas Gleixner, copyright 2004: <https://www.kernel.org/doc./htmldocs/mtdnand/Bad_Block_table_support.html>.

### H/P — the 28 May 2004 MTD CVS record exposes the reconciliation algorithm

The archived MTD CVS change of 28 May 2004 (`nand_bbt.c` 1.9 → 1.10) is a direct contemporary implementation witness. It changed the default Flash BBT to per-chip state and introduced/refactored `check_create()` so each chip's primary and mirror are examined separately.

For the mirrored path, the source distinguishes four conditions:

1. neither table is found — create a BBT and, when write support is enabled, write both;
2. only one table is found — read that surviving table and schedule creation of the missing peer;
3. both are found at equal version — use the primary without repair work;
4. both are found at different versions — read the higher-version table and schedule rewrite of the lower-version peer.

This is not merely “two copies exist.” The copies carry retained **currentness metadata** that determines which representation may reconstitute the operational BBT after restart.

**Primary contemporary source:** Linux MTD CVS archive, 28 May 2004, `nand_base.c 1.92→1.93`, `nand_bbt.c 1.9→1.10`: <https://lists.infradead.org/pipermail/linux-mtd-cvs/2004-May/003683.html>.

### H/P — BBT update changes version state before writing primary and mirror

In the same 28 May source, `nand_update_bbt()` selects the affected chip for a per-chip table, increments the in-memory version for the primary and mirror, writes the primary table first, and then writes the mirror if configured. The scan/reconciliation path can therefore encounter readable copies at different versions after an incomplete two-copy update and has an explicit path to recover from the newer surviving copy.

The safe historical statement is conditional: **if one readable copy with the newer version survives while its peer is older or missing, the bounded implementation knows how to choose the newer representation and rewrite the lagging peer.** The source does not prove that every sudden-power-loss point leaves one complete readable copy.

### H/P — BBT storage blocks are protected by allocation-state classification

The same change adds a `mark_bbt_region()` path whose comment says the BBT regions are marked to prevent accidental erases/writes. The main NAND erase/check path receives an `allowbbt` distinction so ordinary operations cannot casually erase the blocks holding the exclusion table, while BBT-management code can deliberately access them.

This is a useful historical detail because the control metadata has its own **placement protection**. A block used to preserve the table of unusable/reserved blocks is itself excluded from ordinary allocation.

However, `reserved-for-BBT` must not be normalized into `physically defective`. In this implementation a BBT-region classification can be an intentional control reservation rather than a claim about material failure.

---

## Engineering reconstruction

### E — exclusion metadata can require a retention mechanism of its own

Case 78 already established that bad-block evidence can migrate from factory marker to an operational BBT. The Linux MTD implementation adds a second layer:

```text
bad-block / reserved-block relation
    -> in-memory working BBT
    -> flash primary BBT + version
    -> flash mirror BBT + version
    -> restart comparison / repair
    -> reconstructed working BBT
```

The payload is not duplicated by this mechanism. What is duplicated is **allocation authority about which physical blocks must not be used normally**.

### E — redundancy without currentness is insufficient

Two readable tables can disagree. The version field supplies a bounded rule for deciding which table is treated as newer before the stale/missing peer is repaired.

Therefore:

> `two BBT copies` ≠ `two equally authoritative BBT copies`.

### E — BBT version is currentness metadata, not retained history

The per-chip version tells the implementation which readable table is newer for this reconciliation rule. It does not preserve the sequence of bad-block discoveries, the reason each block was retired, factory test conditions, timestamps, or a complete update log.

Therefore:

> `BBT version` ≠ `bad-block event history`.

### E — mirrored/versioned update narrows a failure window; it does not prove transactional atomicity

The Linux documentation itself frames versioned mirroring as risk reduction, not absolute failure immunity. The inspected 2004 code writes the two representations through distinct erase/write operations. This evidence does **not** establish:

- power-fail atomicity of one table rewrite;
- filesystem/database-style transactions;
- checksum protection against every corruption pattern;
- survival when both reserved BBT regions are damaged;
- correct handling of every version-wrap or corrupt-version case;
- equivalence to a quorum protocol.

So the original Case-78 limit remains, but is now sharper:

> `mirrored + versioned BBT` ≠ `universally crash-atomic BBT update`.

### E — control-state reservation ≠ physical defect

Marking BBT regions as unavailable to ordinary operations reuses negative allocation semantics to protect the metadata that carries negative allocation semantics. That does not imply the reserved BBT blocks are physically bad.

This yields a useful distinction:

> `inadmissible for ordinary payload allocation` ≠ `materially defective`.

---

## Functional comparisons — not genealogy

### A — Case 39, Flash mapping recovery

Case 39 and this deepening both show that non-payload Flash metadata can be required before ordinary logical service is safe. But their retained relations differ:

- GeckoFTL-style mapping/recovery state answers which physical embodiment currently realizes a logical address;
- the Case-78 BBT answers which physical blocks are excluded/reserved from ordinary use.

`positive logical resolution metadata` ≠ `negative media-qualification metadata`.

### A — Case 128, ZFS labels and uberblocks

Both cases duplicate compact control state and include a currentness-selection relation. The comparison stops there. ZFS vdev labels/uberblocks carry pool topology and restart roots with checksums/transaction generations; Linux MTD's bounded BBT carries block-qualification state and a simple per-table version relation. No implementation or historical descent is claimed.

### A — distributed replication terminology is unsafe here

A primary/mirror BBT pair is not evidence of consensus, quorum replication, leader election, or distributed agreement. “Replica” can be a broad functional description of duplicate state, but distributed-storage protocol vocabulary would overstate the mechanism.

---

## Philosophical interpretation — bounded

### I — the rule of non-use can itself need protected continuation

The modest philosophical consequence is recursive only in an engineering sense: retaining payload safely may require retaining exclusion metadata, and retaining that exclusion metadata may in turn require duplication, currentness discrimination, and protected placement.

This does **not** license a general “memory of memory” thesis. It establishes only that technical retention can compose multiple layers of retained control state whose persistence horizons and authority rules differ from the user payload they protect.

---

## Counterexamples and limits

- The 2004 Linux MTD sources do not establish invention priority for flash BBT mirroring, versioning, or bad-block management.
- They are a host/raw-NAND software implementation witness, not proof of the internals of a managed SSD.
- The documentation's “without data loss” motivation for mirroring is treated as a project design claim; the inspected source is not an independent power-cut qualification report.
- A higher readable BBT version is only a bounded currentness rule; this addendum does not establish behavior for every corrupt, wrapped, or adversarial version value.
- Reserved BBT blocks are not necessarily physically defective blocks.
- Surviving BBT state does not by itself prove the user payload is correct, ECC-qualified, current, or securely retained.
- No controlled power-cut or dual-copy corruption experiment is performed in this slice.

---

## Prior-art boundary

This slice deliberately makes no first/invention claim. Its defensible historical floor is narrower:

> By May 2004, the Linux MTD NAND implementation publicly contained a flash-resident BBT regime with primary/mirror representations, version-based currentness selection and stale/missing-copy rewrite logic, plus protected BBT placement; contemporary MTD documentation describes mirrored versioned tables as the recommended writable Flash-BBT arrangement.

This predates the ONFI 1.0 / Micron documents used in the original Case 78 but does not prove Linux originated the mechanism. A broader BBT/DiskOnChip/bootloader/controller genealogy belongs in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) if developed. A fresh repository search for `NAND bad block table` found no dedicated companion case to reuse in this round.

---

## Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| Linux MTD documented flash-resident mirrored BBTs with version numbers in 2004 | H/P | grounded in MTD developer documentation |
| 28-May-2004 source chooses the higher readable BBT version and can rewrite an older/missing peer | H/P | grounded in archived CVS diff |
| 28-May-2004 `nand_update_bbt()` increments per-chip version state and writes primary then mirror | H/P | grounded in archived CVS diff |
| BBT storage regions are protected from ordinary erase/write paths | H/P | grounded in archived CVS diff |
| two BBT copies ≠ two equally authoritative copies | E | bounded reconstruction from version comparison |
| BBT version ≠ bad-block event history | E | bounded reconstruction |
| mirrored/versioned BBT ≠ universal power-fail atomicity | E/X | explicit limit; documentation promises risk reduction, not exhaustive fault proof |
| reserved-for-BBT ≠ physically defective | E/X | bounded implementation distinction |
| Linux MTD flash BBT ≈ GeckoFTL/ZFS only at non-payload control-state continuity level | A | functional analogy only |
| Linux MTD invented BBT mirroring/versioning | X | unsupported / not investigated |
| mirrored BBT proves managed-SSD controller behavior | X | unsupported |

---

## Sources

### Primary / contemporary

1. Linux MTD, Thomas Gleixner, *MTD NAND Driver Programming Interface*, `Bad block table support`, copyright 2004: <https://www.kernel.org/doc./htmldocs/mtdnand/Bad_Block_table_support.html>.
2. Linux MTD CVS archive, 28 May 2004, `nand_base.c` 1.92→1.93 and `nand_bbt.c` 1.9→1.10, log message `Make bad block table per chip default. Fake bad blocks in the bbt region.`: <https://lists.infradead.org/pipermail/linux-mtd-cvs/2004-May/003683.html>.

### Later continuity reference — not used to back-project new 2004 claims

3. Linux kernel documentation, current `MTD NAND Driver Programming Interface`, flash BBT creation/write/version-control descriptions: <https://www.kernel.org/doc/html/latest/driver-api/mtdnand.html>.

### Related repository

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — broad NAND/MTD/bootloader/BBT genealogy belongs there; this addendum keeps only the retention-specific control-metadata persistence/currentness boundary.
