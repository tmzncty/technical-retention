# Case 78 Grounding — ONFI/Micron NAND Bad-Block Evidence, 2006–2011

## Purpose

This record grounds [`../cases/78-micron-nand-bad-block-marker-management.md`](../cases/78-micron-nand-bad-block-marker-management.md).

The narrow research question is:

> How can reliable NAND retention depend on preserving **negative defect evidence** whose original physical marker may itself be erased, and how is that evidence transformed into an operational table that survives restart and later physical-block replacement?

The record keeps four layers separate:

1. manufacturer-created factory defect marks;
2. host/system bad-block table state;
3. lifetime-developed failure/replacement relations;
4. user payload.

It does not claim invention priority for bad-block management.

---

## Source A — ONFI 1.0 factory defect mapping

**Document:** Open NAND Flash Interface Working Group, *Open NAND Flash Interface Specification*, Revision 1.0.

**Locator:** §3.2 `Factory Defect Mapping`, especially §3.2.1–3.2.2 and the factory-defect scanning algorithm.

**Official URL:** <https://onfi.org/files/onfi_1_0_gold.pdf>

### Directly established

- The NAND array is not presumed pristine; defects may make blocks unusable.
- Factory defects are represented at block granularity.
- For x8 access a defective block is factory marked with `00h` in the designated defect area of the first or last page; x16 uses `0000h`.
- The host shall not erase/program manufacturer-marked defective blocks.
- The host is expected to scan factory defect areas and create the initial BBT before erase/program use.
- The specification warns that manufacturer defect marking values can change over device lifetime and expects the host to capture them in a BBT during initial use.

### Evidence role

This is the standards-level anchor for `physical block exists ≠ block is admissible for storage` and for the transition from factory mark to host-retained table.

### Limit

ONFI 1.0 is not used as evidence that ONFI invented bad-block marking. No first-use claim is made.

---

## Source B — Micron 8Gb asynchronous/synchronous NAND, February 2009

**Document:** Micron Technology, *8Gb Asynchronous/Synchronous NAND Flash Memory*, MT29F8G08ABABA / MT29F8G08ABCBB family, Draft 27 February 2009.

**Locator:** `Error Management`, document p. 88 (PDF parse around pp. 87–88); Table 15 `Error Management Details`.

**URL:** <https://www.tme.com/Document/f0626004806cbebd352e6f64f6830d11/MT29F8G08ABABAWPIT.pdf>

### Directly established

- A LUN can contain factory-invalid blocks and can develop additional invalid blocks with use.
- Invalidity is defined relative to the minimum required ECC: at least one page has more bad bits than that ECC can correct.
- Micron attempts to program the factory bad-block mark in invalid blocks and guarantees the first spare-area location contains it.
- The method is stated to comply with ONFI Factory Defect Mapping requirements.
- System software should check the spare location on the first page of every block before PROGRAM or ERASE, then create a BBT and map around bad areas.
- Factory testing occurs under worst-case conditions; after erase the bad-block marking may not be recoverable.
- Runtime reliability requires status checking after PROGRAM/ERASE plus ECC, bad-block management, and wear leveling.
- The table gives a minimum valid-block count of 2,008 out of 2,048 blocks per LUN for this bounded product and a `00h` bad-block mark.

### Evidence role

This is a named-product witness connecting the ONFI relation to a concrete Micron part family and explicitly grounding the dangerous ordering `scan before destructive erase/program`.

### Limits

- The numeric NVB/ECC/marker details are product-specific.
- The document does not specify one universal managed-SSD controller implementation.

---

## Source C — Micron TN-29-59 Rev. H, April 2011

**Document:** Micron Technology, TN-29-59, *Bad Block Management in NAND Flash Memory*, Rev. H, April 2011.

**URL used for inspection:** <https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/791/tn2959_5F00_bbm_5F00_in_5F00_nand_5F00_flash.pdf>

### p. 1 — scope and bad-block category

The note states that bad blocks may be present at shipment or develop during device lifetime, and that bad-block management, block replacement, and ECC software are needed.

**Evidence role:** separates factory qualification from lifetime failure.

### p. 2 — `Recognizing Bad Blocks`

Directly established:

- factory bad-block information is written before shipping;
- marker locations differ by SLC/MLC and page/device organization;
- the information must be read before erase because it is erasable and cannot be recovered once erased;
- Micron strongly recommends preserving the original information;
- substitute recognition methods are not equally effective because factory detection used severe environmental conditions, PROGRAM/ERASE cycles, and proprietary test modes;
- the BBT is created by scanning spare areas;
- the BBT is saved to a good block;
- on reboot it is loaded into RAM;
- blocks listed in the BBT are excluded and bad-block management redirects an FTL target to a good block.

**Evidence role:** core proof that the underlying badness and its marker have different retention semantics, and that the operational exclusion relation migrates from marker → durable table → RAM working state.

### p. 3 — `Block Replacement`

Directly established:

- additional bad blocks are identified by PROGRAM/ERASE failure status;
- for the described PAGE PROGRAM failure, other pages in the same block are not affected, so current data can be copied into a replacement block;
- both skip-block and reserve-block methods are documented;
- a lifetime-developed mapping relation must itself be stored in NAND for the skip method;
- the reserve area holds replacement blocks and the BBT, which also tracks remapped developed bad blocks;
- before a physical write, management checks the calculated target, redirects bad targets, and when a block becomes bad remaps it and copies its data;
- Micron describes this management as transparent to the FTL: from the FTL's perspective the data are written to the same address.

**Evidence role:** grounds failure-triggered relocation plus retained correspondence state.

### p. 4 — separation from neighboring maintenance

The conclusion separately recommends bad-block management, garbage collection, and wear leveling, while making ECC mandatory.

**Evidence role:** blocks the shortcut `bad-block replacement = garbage collection = wear leveling` even within one vendor's own software-tool taxonomy.

---

## Corroborating implementation boundary — Linux NAND MTD

A later Linux NAND bad-block implementation contains manufacturer/device-dependent marker-placement handling rather than treating the marker as one universal byte location. This is useful only as a later implementation witness for geometry variability; it is not needed for the core historical claim and is not used to rewrite Micron's period vocabulary.

Repository/code family checked through the public Linux/Android kernel mirror during research.

---

## Related-repository duplication check

Before opening Case 78, `tmzncty/computing-archaeology` code search was run for `bad block NAND` / NAND bad-block management. No dedicated case directly reusable for this retention-specific slice was returned.

Boundary retained:

- general NAND evolution, controller architecture, manufacturing yields, and complete bad-block-management genealogy belong in `computing-archaeology`;
- this repository keeps the specific relation `erasable defect evidence -> retained exclusion table -> failure-triggered replacement`.

---

## Historical / reconstruction boundary

### Historical record

The sources directly document:

- factory and lifetime bad blocks;
- defect marks in spare/defect areas;
- pre-erase scanning;
- BBT creation;
- BBT persistence in a good block and loading into RAM;
- status-triggered lifetime retirement;
- skip/reserve replacement methods;
- reserved replacement area;
- transparent remapping from the FTL's perspective.

### Engineering reconstruction

The repository infers, and labels as inference:

- `factory defect mark ≠ defect itself`;
- `marker erasure ≠ defect repair`;
- `physical presence/addressability ≠ admissible allocation`;
- `negative media-qualification state can be constitutive of positive payload retention`;
- `defect evidence can migrate between embodiments`;
- `BBT current state ≠ complete failure/test history`;
- `reserved capacity can be retention infrastructure`.

### Functional analogy

Only at the bounded functional level:

- SCSI grown-defect reassignment also preserves higher-level designation across physical replacement;
- tombstones/revokes also show negative state suppressing an otherwise physically surviving candidate;
- health telemetry also retains non-payload device state.

No genealogy among those mechanisms is claimed.

### Philosophical interpretation

The only philosophical extension retained is the modest proposition that operational availability can depend on retained **exclusions** as well as retained positive mappings. This does not redefine Heideggerian `Bestand` or convert the BBT into a philosophical category.

---

## Prior-art / novelty boundary

### Claims rejected

- `ONFI invented bad-block management` — not established.
- `Micron invented bad-block tables` — not established.
- `bad-block mark is permanent ROM-like defect metadata` — contradicted by Micron's erasability warning.
- `bad block means every page is already unreadable` — contradicted by the bounded definition and replacement procedure.
- `retiring a bad block securely erases it` — not established.
- `bad-block replacement is just wear leveling or garbage collection` — sources keep these functions distinct.

### Narrow defensible claim

By late 2006 ONFI had standardized factory-defect mapping plus host creation of an initial BBT. Micron's 2009/2011 primary documents expose a retention-specific consequence unusually clearly: **the physical evidence that a block is unsafe can itself be destroyed or drift, so a reliable system must capture, preserve, reconstruct, and extend the exclusion relation while moving payload away from newly failed embodiments.**

That is the contribution of Case 78.
