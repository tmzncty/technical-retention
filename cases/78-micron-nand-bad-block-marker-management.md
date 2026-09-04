# Micron NAND Bad Blocks: Erasable Factory Defect Marks, Retained Bad-Block Tables, and Replacement

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
