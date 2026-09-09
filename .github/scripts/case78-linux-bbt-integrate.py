from pathlib import Path
import re

EVIDENCE_PATH = Path("evidence/78-linux-mtd-2004-mirrored-versioned-bbt-deepening.md")
if EVIDENCE_PATH.exists():
    raise SystemExit("evidence file already exists")

EVIDENCE = r'''# Case 78 Deepening — Linux MTD Mirrored and Versioned Flash Bad-Block Tables (2004)

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
'''
EVIDENCE_PATH.write_text(EVIDENCE, encoding="utf-8")

case = Path("cases/78-micron-nand-bad-block-marker-management.md")
text = case.read_text(encoding="utf-8")
old_scope = "- **Bounded historical/technical regime:** ONFI 1.0 factory-defect mapping (ratified in late 2006), a Micron 8Gb NAND product datasheet dated February 2009, and Micron Technical Note TN-29-59 Rev. H (April 2011)."
new_scope = "- **Bounded historical/technical regime:** Linux MTD flash-resident BBT implementation/documentation from 2004, ONFI 1.0 factory-defect mapping (ratified in late 2006), a Micron 8Gb NAND product datasheet dated February 2009, and Micron Technical Note TN-29-59 Rev. H (April 2011)."
if text.count(old_scope) != 1:
    raise SystemExit("Case 78 scope anchor mismatch")
text = text.replace(old_scope, new_scope)

retained_anchor = "\n---\n\n## Retained state\n"
deepening = r'''

### H/P — Linux MTD 2004 makes the persisted BBT itself mirrored and version-qualified

A separate pre-ONFI software witness sharpens the original Micron statement that a BBT may be saved in good NAND. Linux MTD's 2004 NAND documentation describes a Flash-BBT regime whose default arrangement uses **mirrored tables with version numbers** and reserves blocks for BBT placement. The archived 28-May-2004 `nand_bbt.c` change exposes the corresponding currentness logic: if one table is missing, the surviving peer can seed its rewrite; if both are present but have different versions, the higher readable version is selected and the older peer is scheduled for update.

The same source increments per-chip BBT version state during `nand_update_bbt()` and writes primary and mirror through separate operations. It also marks BBT regions so normal erase/write paths do not accidentally consume the blocks that hold this control metadata.

This deepens, rather than reverses, the original limit on crash atomicity. The Linux documentation presents mirroring/version control as risk reduction, and the source supplies a recovery path when a newer readable copy survives. Neither source proves that every sudden-power-loss point leaves one complete readable copy, that both copies cannot be corrupted together, or that a simple version field is an audit history.

Therefore the bounded relations are:

- `saved BBT ≠ single infallible BBT embodiment`;
- `two BBT copies ≠ two equally authoritative copies`;
- `BBT version ≠ bad-block event history`;
- `mirrored + versioned BBT ≠ universal crash-atomic update`;
- `reserved-for-BBT block ≠ physically defective block`.

See [`evidence/78-linux-mtd-2004-mirrored-versioned-bbt-deepening.md`](../evidence/78-linux-mtd-2004-mirrored-versioned-bbt-deepening.md).
'''
if text.count(retained_anchor) != 1:
    raise SystemExit("Case 78 retained-state anchor mismatch")
text = text.replace(retained_anchor, deepening + retained_anchor)

old_limit = "- A saved BBT is necessary in the documented software design but does not by itself prove crash-atomic implementation of every table update."
new_limit = "- A saved BBT is necessary in the documented software design. Linux MTD 2004 adds mirrored/versioned Flash-BBT recovery, but this narrows rather than eliminates update-loss risk and does not prove transactional crash atomicity, dual-copy survival, or universal power-cut safety."
if text.count(old_limit) != 1:
    raise SystemExit("Case 78 limit anchor mismatch")
text = text.replace(old_limit, new_limit)

prior_anchor = "The `computing-archaeology` repository was searched for a dedicated NAND bad-block-management slice before writing this case; no directly reusable case was found. Broader NAND/SSD engineering genealogy still belongs there rather than being recreated here."
prior_new = "A separate bounded pre-ONFI witness now reaches back to Linux MTD in May 2004: its flash-resident BBT code/documentation already exposes mirrored tables, version-based currentness selection, missing/stale-peer rewrite, and protected BBT regions. This is a historical floor for the inspected implementation, **not** an invention-priority claim.\n\nThe `computing-archaeology` repository was searched again for `NAND bad block table`; no directly reusable case was found. Broader NAND/MTD/bootloader/SSD engineering genealogy still belongs there rather than being recreated here."
if text.count(prior_anchor) != 1:
    raise SystemExit("Case 78 prior-art anchor mismatch")
text = text.replace(prior_anchor, prior_new)

ledger_anchor = "| `bad block` proves every page unreadable | X | rejected |"
ledger_rows = "| Linux MTD flash BBT can retain primary/mirror copies with version currentness | H/P | grounded by 2004 MTD documentation/source |\n| higher readable BBT version can seed stale/missing-peer rewrite | H/P | grounded by 28-May-2004 archived source |\n| mirrored/versioned BBT ≠ universal crash-atomic update | E/X | bounded reconstruction and explicit limit |\n| reserved-for-BBT ≠ physically defective | E/X | bounded implementation distinction |\n"
if text.count(ledger_anchor) != 1:
    raise SystemExit("Case 78 ledger anchor mismatch")
text = text.replace(ledger_anchor, ledger_rows + ledger_anchor)

sources_anchor = "3. Micron Technology, TN-29-59, *Bad Block Management in NAND Flash Memory*, Rev. H, April 2011: <https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/791/tn2959_5F00_bbm_5F00_in_5F00_nand_5F00_flash.pdf>."
sources_new = sources_anchor + "\n4. Linux MTD, Thomas Gleixner, *MTD NAND Driver Programming Interface*, `Bad block table support`, copyright 2004: <https://www.kernel.org/doc./htmldocs/mtdnand/Bad_Block_table_support.html>.\n5. Linux MTD CVS archive, 28 May 2004, `nand_bbt.c` 1.9→1.10 and related NAND changes: <https://lists.infradead.org/pipermail/linux-mtd-cvs/2004-May/003683.html>."
if text.count(sources_anchor) != 1:
    raise SystemExit("Case 78 sources anchor mismatch")
text = text.replace(sources_anchor, sources_new)
case.write_text(text, encoding="utf-8")

roadmap = Path("ROADMAP.md")
r = roadmap.read_text(encoding="utf-8")
case83_anchor = "- [x] Case 83 HDFS BlockScanner cursor checkpoint / clock-domain deepening"
if r.count(case83_anchor) != 1:
    raise SystemExit("ROADMAP Case 83 anchor mismatch")
roadmap_entry = "- [x] Case 78 Linux MTD mirrored/versioned Flash-BBT deepening — [`cases/78-micron-nand-bad-block-marker-management.md`](cases/78-micron-nand-bad-block-marker-management.md), deepened by [`evidence/78-linux-mtd-2004-mirrored-versioned-bbt-deepening.md`](evidence/78-linux-mtd-2004-mirrored-versioned-bbt-deepening.md): 2004 Linux MTD project documentation and the 28-May-2004 archived `nand_bbt.c` update ground primary/mirror Flash BBTs, per-table version currentness, stale/missing-peer rewrite, and BBT-region protection. This advances the open Case-78 `crash-atomic BBT update` seam without falsely closing it: `mirrored + versioned = universally crash-atomic`, `BBT version = failure history`, and `reserved-for-BBT = physically defective` are explicitly rejected. Exact pre-2004 genealogy, version-wrap/corrupt-version behavior, dual-copy/power-cut fault injection, later bootloader/controller implementations, and managed-SSD internals remain open; broad BBT genealogy belongs primarily in `computing-archaeology`.\n\n"
r = r.replace(case83_anchor, roadmap_entry + case83_anchor)
roadmap.write_text(r, encoding="utf-8")

index = Path("CASE_INDEX.md")
idx = index.read_text(encoding="utf-8")
old_row_fragment = "[2006–2011 ONFI/Micron bad-block grounding](evidence/78-micron-2006-2011-nand-bad-block-grounding.md); invention genealogy, exact managed-SSD implementations, crash-atomic BBT update behavior, and independent product validation remain separate work"
new_row_fragment = "[2006–2011 ONFI/Micron bad-block grounding](evidence/78-micron-2006-2011-nand-bad-block-grounding.md) + [2004 Linux MTD mirrored/versioned BBT deepening](evidence/78-linux-mtd-2004-mirrored-versioned-bbt-deepening.md); Flash-resident BBT redundancy/currentness is now grounded at source level, while invention genealogy, exact pre-2004 lineage, dual-copy/power-cut fault behavior, managed-SSD implementations, and independent product validation remain separate work"
if idx.count(old_row_fragment) != 1:
    raise SystemExit("CASE_INDEX Case 78 row anchor mismatch")
idx = idx.replace(old_row_fragment, new_row_fragment)
if "**2619 —" not in idx or "**2620 —" in idx:
    raise SystemExit("CASE_INDEX finding boundary mismatch")
findings = r'''

## Case 78 deepening — Linux MTD mirrored/versioned Flash-BBT findings

Evidence: [`evidence/78-linux-mtd-2004-mirrored-versioned-bbt-deepening.md`](evidence/78-linux-mtd-2004-mirrored-versioned-bbt-deepening.md)

- **2620 — by May 2004 Linux MTD publicly implements flash-resident BBT primary/mirror state with version-based currentness logic.** This is a bounded implementation floor, not an invention-priority claim for BBTs, mirroring, or versioning. (`H/P`, `X`)
- **2621 — flash-resident BBT != ordinary RAM working BBT.** The MTD documentation distinguishes a RAM table built for fast runtime lookup from optional/required table state retained on NAND across restart. (`H/P`, `E`)
- **2622 — two BBT copies != two equally authoritative copies.** When readable primary and mirror versions differ, the 28-May-2004 code selects the higher version as the source and schedules the lower-version peer for rewrite. (`H/P`, `E`)
- **2623 — missing mirror != automatic loss of exclusion knowledge.** If one readable table survives and write support is enabled, `check_create()` can read that copy and recreate the missing peer. (`H/P`)
- **2624 — mirrored/versioned BBT != universal crash-atomic update.** The documentation frames the arrangement as risk reduction, while the implementation performs distinct erase/write operations; no inspected source proves one complete readable copy survives every power-cut point. (`H/P`, `E`, `X`)
- **2625 — BBT version != bad-block event history.** The version relation selects a newer table but does not retain retirement causes, factory test conditions, timestamps, or a complete sequence of previous BBT states. (`E`, `X`)
- **2626 — newer readable version != proof of payload correctness.** BBT currentness qualifies allocation/exclusion metadata; it does not checksum, ECC-qualify, or establish currentness of user data stored elsewhere. (`E`)
- **2627 — BBT storage itself consumes protected NAND capacity.** The 2004 documentation reserves blocks for automatic Flash-BBT placement, turning physically usable space into retention infrastructure for control metadata. (`H/P`, `E`)
- **2628 — reserved-for-BBT != physically defective.** The May-2004 code marks BBT regions so ordinary erase/write paths avoid them; this control classification must not be read as evidence of material block failure. (`H/P`, `E`, `X`)
- **2629 — control metadata can require its own placement protection.** Case 78's rule of non-use is not only stored; the physical embodiments carrying that rule are themselves withheld from ordinary allocation. (`E`)
- **2630 — BBT repair != payload relocation.** Rewriting a stale/missing BBT peer restores exclusion-metadata redundancy/currentness; moving user data away from a newly failed block remains a different operation. (`E`)
- **2631 — BBT mirroring != distributed consensus/quorum.** Primary/mirror selection is local raw-NAND control metadata with a version comparison; distributed-replication vocabulary would overstate the bounded mechanism. (`A`, `X`)
- **2632 — Case 39 FTL mapping ~= Case 78 BBT only as non-payload control-state continuity.** Mapping metadata positively resolves logical identities to embodiments; BBT metadata negatively excludes/reserves physical blocks. (`A`, `X`)
- **2633 — Case 128 ZFS control-metadata redundancy ~= Case 78 only at duplicate/currentness structure.** ZFS label/uberblock topology, checksums, transaction generations, and restart-root semantics are not the Linux MTD BBT mechanism or genealogy. (`A`, `X`)
- **2634 — related-repository boundary:** a fresh `tmzncty/computing-archaeology` search for `NAND bad block table` found no dedicated case to reuse; broad DiskOnChip/MTD/bootloader/controller BBT genealogy belongs there if developed, while Case 78 keeps the retention-specific exclusion-metadata persistence/currentness boundary. (`H/P` project-state record)
'''
idx = idx.rstrip() + findings + "\n"
index.write_text(idx, encoding="utf-8")

for n in range(2620, 2635):
    count = len(re.findall(rf"\*\*{n} —", idx))
    if count != 1:
        raise SystemExit(f"finding {n} count={count}")
for required in [
    "## Historical record",
    "## Engineering reconstruction",
    "## Functional comparisons — not genealogy",
    "## Philosophical interpretation — bounded",
    "## Counterexamples and limits",
    "## Prior-art boundary",
]:
    if required not in EVIDENCE:
        raise SystemExit(f"missing evidence section {required}")
