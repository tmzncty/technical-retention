from pathlib import Path

CASE = r'''# Micron NAND Bad Blocks: Erasable Factory Defect Marks, Retained Bad-Block Tables, and Replacement

## Scope

- **Bounded historical/technical regime:** ONFI 1.0 factory-defect mapping (ratified in late 2006), a Micron 8Gb NAND product datasheet dated February 2009, and Micron Technical Note TN-29-59 Rev. H (April 2011).
- **Primary question:** what must remain when NAND contains physical blocks that must *not* be treated as usable even though those blocks remain electrically addressable and their defect marker can itself be erased?
- **Retention-specific focus:** factory bad-block evidence, construction and persistence of a bad-block table (BBT), lifetime-developed bad-block replacement, and reserved replacement capacity.
- **Excluded from this case:** a general history of NAND, all FTL algorithms, garbage collection, wear leveling, read disturb, program interference, SSD sanitization, or invention priority for bad-block management.

This slice is deliberately adjacent to, but not a repetition of, Case 04. Case 04 asks how a logical identity survives ordinary Flash relocation and reclamation. Case 78 asks how **negative media-qualification state** survives long enough to prevent a physically present block from being accepted as an admissible storage target, and how that exclusion relation is renewed when new blocks fail during service.

---

## Historical vocabulary

The primary sources use terms including:

- `factory defect mapping` (ONFI);
- `defective block` / `invalid block`;
- `bad-block mark` / `bad block information`;
- `bad block table`;
- `bad block management`;
- `block replacement`;
- `skip block`;
- `reserve block`;
- `user addressable block area`;
- `reserved block area`;
- `PROGRAM` / `ERASE` status failure;
- `Flash Translation Layer (FTL)`.

The following are **project engineering terms**, not historical quotations from those documents:

- `negative media-qualification state`;
- `defect-knowledge retention`;
- `exclusion authority`;
- `defect-evidence migration`.

They are used only to compare the documented mechanism with other retention regimes.

---

## Historical record

### H/P — ONFI 1.0 does not presume a pristine NAND array

ONFI 1.0 §3.2 states that the Flash array is not presumed pristine and that some defects can render blocks unusable. Factory defects are represented at **block granularity**. For an 8-bit device the manufacturer marks a defective block by placing `00h` in the designated defect area of the first or last page; the host is instructed not to erase or program manufacturer-marked defective blocks.

The same section requires the host-side factory-defect scan that creates an initial bad-block table before normal erase/program use. It also warns that the manufacturer defect marking can change over device lifetime and is expected to be read by the host and incorporated into a BBT during initial use.

This is already enough to reject a simple equation:

> electrically selectable physical block = admissible storage block.

A negative qualification relation sits between physical addressability and permitted use.

**Primary source:** Open NAND Flash Interface Working Group, *Open NAND Flash Interface Specification*, Revision 1.0, §3.2 `Factory Defect Mapping`, official archival PDF: <https://onfi.org/files/onfi_1_0_gold.pdf>.

### H/P — a Micron 2009 product explicitly requires pre-erase scanning

Micron's February 2009 8Gb asynchronous/synchronous NAND datasheet says a LUN may contain factory-invalid blocks and may develop additional invalid blocks with use. It defines an invalid block as one containing at least one page with more bad bits than the minimum ECC can correct.

Before shipping, Micron attempts to program the bad-block mark in invalid blocks and guarantees the first spare-area location contains the mark. The product documentation instructs system software to inspect that spare location **before any PROGRAM or ERASE operation**, build a BBT, and map around those blocks. It explains why chronology matters: the factory may have detected marginal blocks under worst-case conditions, and after an erase the marking may not be recoverable.

The product therefore supplies a concrete, named-device witness for the standards-level relation:

```text
factory test result
    -> physical bad-block mark
    -> host scan before erase/program
    -> operational BBT
    -> exclusion/remapping during service
```

**Primary source:** Micron, *8Gb Asynchronous/Synchronous NAND Flash Memory*, MT29F8G08ABABA / MT29F8G08ABCBB family, Draft 27 February 2009, `Error Management`, p. 88 in the document pagination: <https://www.tme.com/Document/f0626004806cbebd352e6f64f6830d11/MT29F8G08ABABAWPIT.pdf>.

### H/P — Micron 2011 makes the erasability of defect evidence explicit

TN-29-59 states that bad-block information is written before shipping and gives device-family-specific locations in the spare area. It then gives the crucial retention warning:

- the bad-block information must be read before erase;
- the bad-block information is itself erasable;
- once erased, the original information cannot simply be recovered;
- recreating bad-block knowledge without the factory information is not equally effective because the factory used environmental, program/erase, and proprietary test conditions unavailable to the ordinary system.

The material defect and the marker describing it therefore have different persistence semantics. Erasing the marker does **not** repair the marginal block; it can instead destroy the evidence that tells software not to use the block.

**Primary source:** Micron, TN-29-59 Rev. H, April 2011, pp. 1–2, especially `Recognizing Bad Blocks`: <https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/791/tn2959_5F00_bbm_5F00_in_5F00_nand_5F00_flash.pdf>.

### H/P — factory marks are materialized into a second retained representation

TN-29-59 says the BBT is constructed by reading the relevant spare areas across NAND. Once created, the BBT is **saved to a good block**, and on reboot it is loaded into RAM. Blocks represented in that table are treated as non-addressable by the bad-block-management layer; if the FTL resolves a request to one, management software redirects the operation to a good block.

Thus the operational defect relation deliberately changes embodiment:

```text
factory marker in a bad block's spare area
    -> scan-derived table
    -> table saved in a good NAND block
    -> RAM-resident working table after reboot
```

The system does not need every representation to be equally durable at every moment. It needs a durable-enough path by which the exclusion relation can be reconstructed for the next operating interval.

### H/P — lifetime failures create new exclusion state and replacement work

The same technical note distinguishes bad blocks present at shipment from additional bad blocks that develop later. PROGRAM or ERASE failure in the NAND status register can identify a new bad block. For the bounded PAGE PROGRAM failure described by Micron, data in other pages of the block are not thereby destroyed, so the block can be replaced by reprogramming the current page data and copying the remaining current data to a valid block.

Micron documents two broad management strategies:

- **skip block** — bypass bad physical blocks, retaining enough correspondence information for lifetime-developed failures;
- **reserve block** — redirect to known-good blocks in a reserved area, which also stores the BBT and tracks remapped developed bad blocks.

The reserve-block account says the bad-block-management layer can be transparent to the FTL: from the FTL's perspective the data appear to be written to the same address even though the physical target has changed.

This is not merely failure detection. It is failure-triggered **identity-preserving re-embodiment** plus retention of the relation that makes future accesses resolve away from the retired block.

**Primary source:** Micron TN-29-59 Rev. H, April 2011, p. 3, `Block Replacement`, `Skip Block Method`, and `Reserve Block Method`.

### H/P — replacement reserve is retention infrastructure, not simply unused capacity

TN-29-59 separates `user addressable block area` from `reserved block area`. The latter is used for replacement blocks and BBT storage. For the Micron devices covered by the note, the document states a maximum lifetime bad-block allowance of 2% of total blocks and says the same number is commonly reserved.

This 2% figure is **not generalized into a universal NAND constant**. The stronger retention point is architectural: some physically good capacity can be withheld from ordinary user addressing precisely so the logical service can survive later physical-block retirement.

---

## Retained state

At least four different retained states must remain separate.

### 1. User payload

The values the host actually intends to keep.

### 2. Physical cell condition

A block can physically remain present while being marginal, failed, or otherwise excluded from reliable use.

### 3. Factory defect evidence

The spare-area bad-block mark is manufacturer-created negative evidence about a physical block. It is not user payload.

### 4. Operational bad-block / replacement state

The BBT and, for lifetime-developed failures, the retained correspondence from bad block to replacement block determine which physical embodiments may be used and where the logical identity should resolve instead.

A surviving payload bitstream is therefore not by itself a complete storage service. The system also requires enough retained qualification and mapping state to reject embodiments that no longer count as safe storage targets.

---

## Maintenance and migration of defect knowledge

This case adds a form of maintenance that is easy to miss because it concerns metadata rather than charge refresh.

### At initialization

Factory bad-block evidence is scanned before destructive erase/program use and condensed into a BBT.

### Across restart

A durable copy of the BBT in a good NAND block permits a RAM working copy to be rebuilt.

### During service

PROGRAM/ERASE status can create new bad-block state. The current payload is moved when necessary, a replacement is allocated, and the table/correspondence is updated.

Thus the object being preserved is not only a payload. The system also preserves and updates a **rule of non-use**.

---

## Read, write, erase, and forgetting

### Read

Reading the marker is an evidence-gathering operation used to construct the exclusion map. Ordinary payload reads are a different relation and remain subject to ECC/read-management regimes covered elsewhere.

### Write

A successful write to a logical address need not imply use of the originally calculated physical block. Bad-block management can redirect the target to a known-good replacement while keeping the higher-level designation stable.

### Erase

Erase has two very different consequences depending on the target:

- ordinary erase prepares a usable Flash block for future programming;
- erasing the original factory marker can destroy defect evidence while leaving the underlying reason for exclusion unresolved.

Therefore:

> **marker erasure ≠ defect repair.**

### Forgetting

Forgetting a bad-block relation is potentially harmful. If the negative qualification state disappears while the physical block still exists, later software can mistake surviving addressability for admissibility.

That is the reverse of a secure-deletion objective. Here the dangerous failure is not that obsolete data survive; it is that **exclusion evidence fails to survive**.

---

## Engineering reconstruction

The primary documents support the following bounded reconstruction.

### E — physical presence does not establish allocation authority

A block may answer electrical commands yet be excluded because retained defect state says its reliability is not guaranteed.

### E — negative metadata can be constitutive of positive payload retention

The BBT does not contain the user's intended payload, but preserving it helps prevent the controller from placing that payload on known-unreliable blocks.

### E — defect evidence can require migration between embodiments

The original factory mark can be erasable or drift; the operational system therefore materializes the same exclusion relation as a table in a good block and later as a RAM working structure.

### E — replacement capacity is a continuation resource

Reserved good blocks become useful precisely when an existing physical embodiment must be retired. The available reserve therefore sets one hidden boundary on continued logical storage service.

### E — current exclusion state is not a complete failure history

A BBT can answer `which blocks must not be used now?` without retaining every test condition, timestamp, raw error count, or sequence by which each entry became bad. It is current operational control state, not automatically an audit log.

---

## Functional comparisons — not genealogy

### A — Case 14, SCSI grown-defect reassignment

Both cases show stable logical designation surviving a physical-target change, and both make defect/replacement metadata constitutive of later address resolution.

The difference matters. Case 14's bounded SCSI regime focuses on a disk logical block whose physical sector is reassigned after a grown defect. Case 78 foregrounds NAND's **manufacturer-supplied factory defect marks, host pre-use scan, erasable negative evidence, and lifetime bad-block table**. This is a functional comparison, not evidence that one mechanism descends from the other.

### A — Case 04, mapped Flash

Ordinary Flash relocation/reclamation and bad-block replacement can both change physical embodiment while preserving higher-level identity, but they have different triggers and goals:

- Case 04 relocation is driven by erase-before-rewrite / reclamation geometry;
- Case 78 replacement is driven by physical-block qualification/failure.

Therefore `bad-block replacement ≠ garbage collection ≠ wear leveling`.

### A — Cases 41/42/74, negative control evidence

A tombstone, delete marker, journal revoke, and bad-block entry all can make a still-physically-present positive candidate inadmissible. The similarity stops at that abstract control relation. Their objects, propagation rules, persistence windows, and failure semantics are different.

### A — Case 55, health telemetry

SMART/health counters summarize device condition and history. A BBT instead directly participates in choosing which physical blocks may receive payload. `health evidence ≠ allocation authority`.

---

## Philosophical interpretation — bounded

### I — retention can preserve a prohibition

This case is useful because the retained technical state is not only a positive `what is stored where?` relation. The system also has to preserve `this material location must not count as usable`.

The philosophical point should remain modest: **technical availability is partly produced by retained exclusions**. A medium does not become operationally available merely because matter and addresses survive. No stronger Heideggerian claim follows from this engineering fact, and `bad block = Bestand` would be a category mistake.

---

## Counterexamples and limits

- The sources do not establish who first invented NAND bad-block marking or bad-block tables.
- The Micron marker locations are device/family specific; they are not a universal NAND geometry.
- The factory mark is not asserted to encode the complete failure mechanism or test history.
- `Bad` does not mean every bit/page in the block is unreadable. The bounded definition is a reliability/admissibility classification.
- The documented PAGE PROGRAM failure boundary should not be generalized to every failure mode or every NAND generation.
- The 2% reserve statement is limited to the Micron devices covered by TN-29-59 and is not a universal NAND requirement.
- The sources specify operational exclusion/replacement, not secure sanitization of retired blocks.
- A saved BBT is necessary in the documented software design but does not by itself prove crash-atomic implementation of every table update.
- Modern managed SSD controllers may hide this machinery from the host and may use different internal representations.

---

## Prior-art boundary

This case makes **no invention-priority claim** for factory bad-block marking, bad-block tables, or block replacement.

The defensible historical statement is narrower:

> By ONFI 1.0 (late 2006), factory-defect mapping and a host-created initial bad-block table were standardized chip-interface obligations; Micron's 2009 product documentation and 2011 technical note make the retention consequence explicit by requiring pre-erase capture of erasable factory defect evidence, durable BBT storage, reboot reconstruction, and runtime replacement of newly bad blocks.

The `computing-archaeology` repository was searched for a dedicated NAND bad-block-management slice before writing this case; no directly reusable case was found. Broader NAND/SSD engineering genealogy still belongs there rather than being recreated here.

---

## Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| NAND may ship with defective blocks and acquire additional bad blocks | H/P | grounded by ONFI/Micron primary documentation |
| manufacturer defect evidence is recorded in spare/defect area | H/P | grounded |
| host should create an initial BBT before erase/program | H/P | grounded |
| original bad-block information can be erased and then become unrecoverable | H/P | grounded in Micron TN and product documentation |
| BBT can be saved in a good NAND block and loaded into RAM at reboot | H/P | grounded in Micron TN |
| PROGRAM/ERASE failure can create lifetime bad-block retirement/replacement work | H/P | grounded in Micron TN |
| reserve blocks can carry replacement payload and BBT state | H/P | grounded in Micron TN |
| physical addressability ≠ admissible allocation | E | reconstruction from documented exclusion semantics |
| marker erasure ≠ defect repair | E | reconstruction bounded by explicit erasability warning |
| negative defect metadata can preserve positive payload reliability | E | reconstruction |
| bad-block replacement ≠ garbage collection / wear leveling | E/A | bounded comparison; Micron itself lists them separately |
| NAND bad-block replacement ≈ SCSI defect reassignment | A | functional analogy only; no genealogy claimed |
| bad-block mark ≈ tombstone/revoke as negative evidence | A | abstract analogy only |
| `bad block` proves every page unreadable | X | rejected |
| Micron/ONFI invented bad-block management | X | unsupported / not investigated |
| retired bad block is securely erased | X | unsupported |

---

## Sources

### Primary / contemporary

1. Open NAND Flash Interface Working Group, *Open NAND Flash Interface Specification*, Rev. 1.0, §3.2 `Factory Defect Mapping`, official PDF: <https://onfi.org/files/onfi_1_0_gold.pdf>.
2. Micron Technology, *8Gb Asynchronous/Synchronous NAND Flash Memory*, MT29F8G08ABABA / MT29F8G08ABCBB family, Draft 27 February 2009, `Error Management`: <https://www.tme.com/Document/f0626004806cbebd352e6f64f6830d11/MT29F8G08ABABAWPIT.pdf>.
3. Micron Technology, TN-29-59, *Bad Block Management in NAND Flash Memory*, Rev. H, April 2011: <https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/791/tn2959_5F00_bbm_5F00_in_5F00_nand_5F00_flash.pdf>.

### Related cases

- [`04-flash-virtual-mapping-logical-identity.md`](04-flash-virtual-mapping-logical-identity.md)
- [`14-scsi-disk-defect-reassignment-logical-identity.md`](14-scsi-disk-defect-reassignment-logical-identity.md)
- [`47-fast11-ssd-sanitization-verification.md`](47-fast11-ssd-sanitization-verification.md)
- [`55-nvme-smart-health-endurance-telemetry.md`](55-nvme-smart-health-endurance-telemetry.md)

### Related repository

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — broad NAND/SSD technical history belongs there; this case keeps only the retention-specific negative-metadata/replacement argument.
'''

EVIDENCE = r'''# Case 78 Grounding — ONFI/Micron NAND Bad-Block Evidence, 2006–2011

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
'''

README_LINE = "- [`Case 77 — Data General Dynamic-RAM “Sniffing”: Refresh-Coupled ECC Scrub and Corrective Writeback`](cases/77-data-general-dram-sniff-refresh-ecc-scrub.md) — `grounded`; Data General's 1980-filed design uses dynamic-RAM refresh opportunities to advance a distinct full-word `sniff`/ECC check and conditionally rewrite corrected state. Earlier IBM 1971 cycle-stealing systematic correction blocks a first-invention claim, while the design itself separates charge-refresh coverage, integrity-scan coverage, demand correction, stored repair, and maintenance retry/currentness. Grounding: [`evidence/77-ibm-data-general-1971-1988-ecc-scrub-grounding.md`](evidence/77-ibm-data-general-1971-1988-ecc-scrub-grounding.md)."
README_ADD = README_LINE + "\n- [`Case 78 — Micron NAND Bad Blocks: Erasable Factory Defect Marks, Retained Bad-Block Tables, and Replacement`](cases/78-micron-nand-bad-block-marker-management.md) — `grounded`; ONFI 1.0 plus Micron 2009/2011 primary documentation show that factory defect evidence must be captured before destructive erase/program use because the marker itself may be lost, then materialized as a durable bad-block table that is reloaded at reboot and extended when lifetime PROGRAM/ERASE failures force physical replacement. Grounding: [`evidence/78-micron-2006-2011-nand-bad-block-grounding.md`](evidence/78-micron-2006-2011-nand-bad-block-grounding.md)."

CASE77_ROW = "| [Data General Dynamic-RAM “Sniffing”: Refresh-Coupled ECC Scrub and Corrective Writeback](cases/77-data-general-dram-sniff-refresh-ecc-scrub.md) | **grounded** | dynamic-RAM charge + row refresh + ECC/check bits + full-word sniff address/coverage + conditional corrected writeback + foreground-aware retry | separate charge restoration from codeword-integrity renewal even when one schedule composes them; demand correction from stored repair; row-refresh coverage from word-scrub coverage; and correction algebra from writeback currentness | [1971–1988 IBM/Data General grounding](evidence/77-ibm-data-general-1971-1988-ecc-scrub-grounding.md); named Data General deployment, full scrub-terminology genealogy, controller-placement history, hard-error sparing, and independent fault validation remain separate work |"
CASE78_ROW = "| [Micron NAND Bad Blocks: Erasable Factory Defect Marks, Retained Bad-Block Tables, and Replacement](cases/78-micron-nand-bad-block-marker-management.md) | **grounded** | factory defect marks + scan-derived persistent BBT + RAM working table + status-detected lifetime bad blocks + reserved replacement capacity/remap state | separate physical block survival from admissible allocation; defect from erasable defect evidence; factory mark from operational table; bad-block replacement from GC/wear leveling; and payload continuity from exclusion-metadata continuity | [2006–2011 ONFI/Micron bad-block grounding](evidence/78-micron-2006-2011-nand-bad-block-grounding.md); invention genealogy, exact managed-SSD implementations, crash-atomic BBT update behavior, and independent product validation remain separate work |"

MATRIX77 = "| Data General DRAM sniffing / 1980–1983 bounded design | dynamic-cell charge + ECC-protected word/check bits + row-refresh schedule + full-word sniff position + correction/writeback control | ordinary row refresh remains millisecond-scale in the illustrative design; one full word is additionally sniffed per refresh opportunity; correctable errors can trigger re-read/correct/writeback and foreground traffic can force retry | a demand read may return corrected data without immediately repairing the stored word; the later sniff path repairs the embodiment | refresh needs row coverage while sniffing advances a fuller row/column/module address relation | no payload relocation is required; the same logical location is renewed in place, but a stale maintenance image must not overwrite a newer foreground value | no application history by default; bounded scan-position/error/diagnostic state supports coverage and repair rather than a complete access history |"
MATRIX78 = "| ONFI/Micron NAND bad-block management / 2006–2011 bounded regime | user payload + physical block condition + factory spare-area defect mark + persistent BBT/replacement mapping + reserved good blocks | capture factory marks before erase/program; persist BBT in a good block; reload working table at boot; status-detected lifetime failure triggers exclusion, copy, and replacement | bad-block marker/BBT reads qualify a physical target for use; ordinary payload read/ECC remains separate | FTL/logical target is checked against bad-block state and can be redirected to a reserved good physical block | factory and runtime bad blocks remain physically present while losing allocation authority; current payload can migrate to a replacement | current exclusion/replacement state is retained, not complete factory-test or failure chronology |"

F924 = "924. **Data General 1980 refresh-coupled correction ≠ invention of systematic memory correction** — IBM's 1971-filed cycle-stealing memory-correcting design already systematically revisits and rewrites corrected monolithic-memory state, so the bounded novelty claim is the Data General dynamic-RAM refresh/sniff composition rather than first invention."
NEW_FINDINGS = F924 + r'''
925. **physical block survival ≠ admissible allocation** — Case 78's factory-marked NAND blocks remain material/addressable objects while retained defect state requires the system to exclude them from normal use;
926. **factory defect mark ≠ physical defect** — the marker is evidence created by manufacturing test, not the defect mechanism itself;
927. **marker erasure ≠ defect repair** — Micron explicitly warns that bad-block information is erasable and may become unrecoverable after erase, while the reason the block was classified bad need not disappear;
928. **defect-evidence retention can require representation change** — the original spare-area mark is scanned into a BBT saved in a good block and then reconstructed as a RAM working table after reboot;
929. **durable BBT ≠ RAM working BBT** — one embodiment crosses power loss while the other supports ordinary runtime lookup; loss/recreation boundaries differ even when they represent the same exclusion relation;
930. **bad-block table ≠ complete defect history** — the table answers which targets must be excluded/remapped now without preserving all factory test conditions, raw errors, timestamps, or failure chronology;
931. **factory bad block ≠ lifetime-developed bad block** — the first arrives with manufacturer-supplied defect evidence; the second can be created by later PROGRAM/ERASE failure status and requires runtime update/replacement;
932. **PROGRAM failure ≠ automatic loss of every other page in the block** — Micron's bounded procedure explicitly allows current data from the affected block to be recopied to a replacement;
933. **bad-block detection ≠ completed replacement** — identifying a failed physical target creates a new preservation obligation; current payload/correspondence must still be transferred and the exclusion/remap state retained;
934. **bad-block replacement ≠ garbage collection** — both can move Flash payload, but Case 78 is triggered by media qualification/failure while Case 04 reclamation is driven by erase/reuse geometry;
935. **bad-block replacement ≠ wear leveling** — failure exclusion preserves reliable service; wear leveling distributes physical cycling burden. Micron lists the functions separately;
936. **reserved good blocks ≠ simply unused capacity** — withheld physical capacity can be retention infrastructure that permits logical identity to continue after physical-block retirement;
937. **logical-address continuity can depend on negative metadata** — a positive map is insufficient when another retained relation must veto known-bad physical targets and redirect access;
938. **bad-block retirement ≠ secure sanitization** — exclusion from future allocation does not establish erasure of payload remnants in the retired block;
939. **NAND bad-block exclusion ≈ tombstone/revoke only as functional analogy** — each can make a physically surviving candidate inadmissible, but object, scope, lifetime, replication, and mechanism differ;
940. **NAND bad-block replacement ≈ SCSI grown-defect reassignment only at the continuity relation** — both can preserve higher-level designation while replacing a physical target, but NAND factory markers/pre-use BBT capture and Flash-specific replacement semantics are not a disk genealogy claim.'''

ROAD_HEADER_OLD = "SSD FTL/controller-mediated persistence beyond the bounded Ban/1990s case — **partially advanced by grounded Cases 15, 20, 30, 31, 32, 36, 37, 38, 39, 44, 47, 52, 55, 59, 65, 66, 67, and 76**."
ROAD_HEADER_NEW = "SSD FTL/controller-mediated persistence beyond the bounded Ban/1990s case — **partially advanced by grounded Cases 15, 20, 30, 31, 32, 36, 37, 38, 39, 44, 47, 52, 55, 59, 65, 66, 67, 76, and 78**."
ROAD_ANCHOR = "This keeps standardized endurance rating, physical P/E wear, powered refresh, health telemetry, and actual post-rating data survival distinct. The broad item stays unchecked"
ROAD_INSERT = "This keeps standardized endurance rating, physical P/E wear, powered refresh, health telemetry, and actual post-rating data survival distinct. [`cases/78-micron-nand-bad-block-marker-management.md`](cases/78-micron-nand-bad-block-marker-management.md), grounded by [`evidence/78-micron-2006-2011-nand-bad-block-grounding.md`](evidence/78-micron-2006-2011-nand-bad-block-grounding.md), adds the factory/runtime bad-block qualification layer: ONFI 1.0 and Micron primary documentation require factory defect marks to be captured before destructive erase/program use, materialized into a BBT that can survive in a good block and be reloaded at reboot, and extended when later PROGRAM/ERASE failures trigger remap/copy into reserved good blocks. This separates physical block survival, defect evidence, allocation authority, logical-address continuity, replacement reserve, garbage collection, wear leveling, and sanitization. The broad item stays unchecked"


def replace_once(path, old, new):
    p = Path(path)
    s = p.read_text()
    if s.count(old) != 1:
        raise SystemExit(f"expected exactly one anchor in {path}: {old[:80]!r}, found {s.count(old)}")
    p.write_text(s.replace(old, new, 1))


if Path('cases/78-micron-nand-bad-block-marker-management.md').exists():
    raise SystemExit('Case 78 already exists; refusing duplicate integration')

Path('cases/78-micron-nand-bad-block-marker-management.md').write_text(CASE)
Path('evidence/78-micron-2006-2011-nand-bad-block-grounding.md').write_text(EVIDENCE)

replace_once('README.md', README_LINE, README_ADD)
replace_once('CASE_INDEX.md', CASE77_ROW, CASE77_ROW + '\n' + CASE78_ROW)
replace_once('CASE_INDEX.md', MATRIX77, MATRIX77 + '\n' + MATRIX78)
replace_once('CASE_INDEX.md', 'After seventy-eight bounded cases, **all seventy-eight cases are now `grounded`.**', 'After seventy-nine bounded cases, **all seventy-nine cases are now `grounded`.**')
replace_once('CASE_INDEX.md', F924, NEW_FINDINGS)
replace_once('ROADMAP.md', ROAD_HEADER_OLD, ROAD_HEADER_NEW)
replace_once('ROADMAP.md', ROAD_ANCHOR, ROAD_INSERT)

# Validation: navigation, status, numbering and accidental label collisions.
readme = Path('README.md').read_text()
roadmap = Path('ROADMAP.md').read_text()
index = Path('CASE_INDEX.md').read_text()
assert readme.count('cases/78-micron-nand-bad-block-marker-management.md') == 1
assert roadmap.count('cases/78-micron-nand-bad-block-marker-management.md') == 1
assert index.count('cases/78-micron-nand-bad-block-marker-management.md') == 1
assert 'After seventy-nine bounded cases, **all seventy-nine cases are now `grounded`.**' in index
for n in range(925, 941):
    assert f'{n}. **' in index
assert '941. **' not in index
assert 'bad-block replacement ≠ garbage collection' in index
assert Path('cases/78-micron-nand-bad-block-marker-management.md').read_text().count('## Historical record') == 1
assert Path('evidence/78-micron-2006-2011-nand-bad-block-grounding.md').exists()

# Temporary integration machinery must not survive the substantive commit.
Path('.github/workflows/case78-integration.yml').unlink(missing_ok=True)
Path('.github/case78_integrate.py').unlink(missing_ok=True)
