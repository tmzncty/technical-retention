# Micron NAND Bad Blocks: Erasable Factory Defect Marks, Retained Bad-Block Tables, and Replacement

## Scope

- **Bounded historical/technical regime:** Linux MTD flash-resident BBT implementation/documentation from 2004; the Linux v3.3→v3.4 (2012) transition that began maintaining grown-bad-block OOB markers alongside flash BBT state with explicit power-cut ordering; ONFI 1.0 factory-defect mapping (ratified in late 2006); a Micron 8Gb NAND product datasheet dated February 2009; Micron Technical Note TN-29-59 Rev. H (April 2011); a Linux-MTD BBT-carrier relocation change released in Linux v4.9 (2016); and a KIOXIA TH58NYG3S0HBAI6 Rev. 2.00 product witness whose reliability-management wording is conservatively bounded to 2018–2019.
- **Primary question:** what must remain when NAND contains physical blocks that must *not* be treated as usable even though those blocks remain electrically addressable and their defect marker can itself be erased?
- **Retention-specific focus:** factory bad-block evidence, construction and persistence of a bad-block table (BBT), multiple representations of grown-bad-block exclusion state, lifetime-developed bad-block replacement, reserved replacement capacity, BBT-carrier replacement, and the distinction between correctable/maintainable error evidence and block-retirement authority.
- **Excluded from this case:** a general history of NAND, all FTL algorithms, garbage collection, wear leveling, read disturb, program interference, SSD sanitization, or invention priority for bad-block management.

This slice is deliberately adjacent to, but not a repetition of, Case 04. Case 04 asks how a logical identity survives ordinary Flash relocation and reclamation. Case 78 asks how **negative media-qualification state** survives long enough to prevent a physically present block from being accepted as an admissible storage target, and how that exclusion relation is renewed when new blocks fail during service.

KIOXIA soft-error / retirement-classification deepening: [`../evidence/78-kioxia-2018-2019-soft-error-vs-bad-block-retirement-deepening.md`](../evidence/78-kioxia-2018-2019-soft-error-vs-bad-block-retirement-deepening.md).

Linux MTD BBM / flash-BBT power-cut ordering deepening: [`../evidence/78-linux-mtd-2012-bbm-bbt-power-cut-ordering-deepening.md`](../evidence/78-linux-mtd-2012-bbm-bbt-power-cut-ordering-deepening.md).

Linux MTD BBT carrier-failure relocation deepening: [`../evidence/78-linux-mtd-2016-bbt-carrier-failure-relocation-deepening.md`](../evidence/78-linux-mtd-2016-bbt-carrier-failure-relocation-deepening.md).

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
- `Flash Translation Layer (FTL)`;
- Linux `bad block marker`, `flash-based BBT`, and `NAND_BBT_NO_OOB_BBM`.

The following are **project engineering terms**, not historical quotations from those documents:

- `negative media-qualification state`;
- `defect-knowledge retention`;
- `exclusion authority`;
- `defect-evidence migration`;
- `control-metadata carrier`;
- `continuation reserve`;
- `cross-representation convergence`;
- `representation-divergence debt`.

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

### H/P — Linux v3.4 publishes grown-bad-block OOB evidence before the flash BBT, while accepting temporary divergence

Released Linux v3.3's default `nand_default_block_markbad()` path updated the RAM BBT and then chose **either** `nand_update_bbt()` for `NAND_BBT_USE_FLASH` or an OOB bad-block-marker write. Brian Norris's January 2012 linux-mtd patch identifies the consequence explicitly: as grown bad blocks accumulated, OOB markers could become stale and the flash BBT could become the only current source of bad-block information.

The patch changes the default so a grown bad block can be represented in both places. Its v4 ordering is:

```text
erase affected block
    -> update RAM BBT
    -> write per-block OOB bad-block marker
    -> update flash-resident BBT
```

The revision note says the OOB BBM was deliberately moved before the BBT update because this should help with power cuts. Released Linux v3.4 contains that sequence and the `NAND_BBT_NO_OOB_BBM` opt-out.

The patch does **not** claim atomicity. It explicitly says a power cut between the OOB write and flash-BBT update can leave the two representations “out of sync” and expects later I/O to rediscover the bad block and restore agreement. Contemporaneous review then identifies a further boundary: after such a partial update, a later retry begins with erase-before-OOB-rewrite, creating another possible interruption interval. Brian Norris acknowledges power loss after that erase but before rewriting OOB, and OOB rewrite failure, as relevant cases.

Therefore the bounded relations are:

- `one bad-block exclusion relation != one persistent representation`;
- `ordered BBM -> BBT publication != atomic bad-block-state commit`;
- `temporary BBM/BBT disagreement != automatically loss of all exclusion evidence`;
- `reconstructable exclusion state != exact checkpointed update state`;
- `BBM-first ordering != universal power-cut proof`.

See [`evidence/78-linux-mtd-2012-bbm-bbt-power-cut-ordering-deepening.md`](../evidence/78-linux-mtd-2012-bbm-bbt-power-cut-ordering-deepening.md).

### H/P — BBT currentness depends on ordering and candidate admissibility, not version magnitude alone

A second Linux-MTD deepening makes the earlier `higher readable version` shorthand more precise. The 28-May-2004 CVS change used an ordinary numeric `>` comparison between differing primary/mirror versions and stored the then-version field as a little-endian integer. By the final Linux 2.6.12 source (17 June 2005), the persisted BBT version occupies one byte and currentness is chosen with a signed 8-bit difference, `((int8_t)(td->version[i] - md->version[i])) > 0`, allowing nearby versions to be ordered across numeric wrap such as `0xff -> 0x00`.

That comparison rule still does not make the version byte a self-sufficient authority token. A September-2011 MTD patch documents a case where a primary BBT at version `0x02` has uncorrectable ECC errors while a mirror at `0x01` remains clean. The fix delays propagating the nominally newer version until a valid readable copy has actually been selected, preventing the old mirror payload from being falsely relabeled as version `0x02` after the newer candidate fails validation.

A March-2021 upstream change adds another boundary: blocks holding the BBT can themselves become bad, and BBT search must skip such blocks or an obsolete table may be selected instead of a newer available version. Currentness therefore depends on **candidate discovery + carrier admissibility + version ordering + content validity**, not simply on retaining two copies and comparing one scalar.

The bounded relations are:

- `finite version token != unbounded chronology`;
- `numerically larger != unconditionally newer after cyclic reuse`;
- `higher/newer version != valid BBT payload`;
- `recognizable BBT signature/version != admissible BBT embodiment`;
- `version convergence != bad-block event-history recovery`.

See [`evidence/78-linux-mtd-2004-2021-bbt-currentness-admissibility-deepening.md`](../evidence/78-linux-mtd-2004-2021-bbt-currentness-admissibility-deepening.md).

### H/P — Linux 2016 makes the BBT's own failed carrier replaceable during update

Released Linux v4.8 aborted the inspected `write_bbt()` path when the selected BBT eraseblock could not be erased or written. Upstream commit `10ffd570f11701972aff2a6f91f3d253d6f0e7ee` (23 September 2016) changed that behavior: the failing BBT block is marked worn/bad, the descriptor's page pointer is invalidated, and the write loop searches for another eligible BBT block. Released Linux v4.9 contains this retrying implementation.

The generic v4.9 BBT descriptors use a bounded candidate search (`NAND_BBT_SCAN_MAXBLOCKS`, defined there as four), so this is failure-tolerant relocation while replacement carriers remain, not an infinite self-healing guarantee. The patch discussion also explicitly considered the interruption window between retiring a failed carrier and successfully materializing its replacement, so this deepening does not upgrade BBT relocation into a crash-atomic transaction.

Bounded relations:

- `BBT exclusion relation != one physical BBT carrier`;
- `failed BBT carrier -> retirement + alternate-carrier search`;
- `old carrier retired != replacement BBT already durable`;
- `carrier retry != transactional crash atomicity`;
- `replacement-carrier reserve exhausted -> continuation boundary`.

See [`evidence/78-linux-mtd-2016-bbt-carrier-failure-relocation-deepening.md`](../evidence/78-linux-mtd-2016-bbt-carrier-failure-relocation-deepening.md).

### H/P — KIOXIA 2018–2019 separates soft/read-error maintenance from block-retirement authority

KIOXIA's TH58NYG3S0HBAI6 Rev. 2.00 product datasheet supplies a later manufacturer control that sharpens what `bad block` means operationally. Its revision history says `Reliability Guidance` was renewed and `NAND Management` was added on **14 December 2018**; the 1 October 2019 revision rebrands the document as KIOXIA. The exact reliability-management wording inspected here is therefore bounded conservatively to 2018–2019 rather than silently back-projected to the 2013 preliminary revision.

The product's failure table distinguishes three responses: erase failure → block replacement; page-program failure → block replacement; read-bit error → inspect host ECC status and take measures such as rewrite before errors become uncorrectable. The following reliability section says explicitly that a random bit error does **not necessarily** mean a block is bad and says that, generally, program/erase status failure is the event for marking a block bad. It separately explains that retention-loss and read-disturb errors may leave a block usable again after erase/reprogram.

At the same time, the bad-block section repeats the Case-78 negative-retention rule: detected bad blocks must be managed as unusable and should not be erased because the bad-block information may become impossible to recover.

This creates a sharp product-level boundary:

```text
read / random bit error
    -> ECC observation and possible rewrite
    != automatic permanent block retirement

program / erase status failure
    -> block replacement + future-access prevention

retention/read-disturb maintenance-eligible block
    -> erase/reprogram may restore usability

detected bad block
    -> erase can destroy exclusion evidence and is prohibited
```

Thus `error detected != block retired`, and the same erase/reprogram primitive can be restorative in one classification while evidence-destroying in another. This does not mean every soft error is always recoverable or every controller retires blocks only on the two documented status failures.

See [`evidence/78-kioxia-2018-2019-soft-error-vs-bad-block-retirement-deepening.md`](../evidence/78-kioxia-2018-2019-soft-error-vs-bad-block-retirement-deepening.md).

---

## Retained state

At least six different retained states must remain separate.

### 1. User payload

The values the host actually intends to keep.

### 2. Physical cell condition

A block can physically remain present while being marginal, failed, or otherwise excluded from reliable use.

### 3. Factory defect evidence

The spare-area bad-block mark is manufacturer-created negative evidence about a physical block. It is not user payload.

### 4. Operational bad-block / replacement state

The BBT and, for lifetime-developed failures, the retained correspondence from bad block to replacement block determine which physical embodiments may be used and where the logical identity should resolve instead.

### 5. BBT embodiment / carrier location

The exclusion relation itself is materialized in one or more NAND blocks. Linux's 2016 carrier-failure path shows that the current BBT carrier is not identical to the BBT relation: a failed carrier can be retired and the table attempted on another eligible block.

### 6. Cross-representation agreement / convergence state

The Linux v3.4 deepening adds another distinction. A per-block OOB BBM and a flash-resident BBT can encode the same grown-bad-block exclusion relation yet temporarily disagree after interruption. Their agreement is therefore a maintained property, not a timeless identity. A surviving marker may support later reconstruction of a stale table, but that does not amount to a separately persisted transaction log or exact update checkpoint.

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

For Linux v3.4's default flash-BBT marking path, the newly created exclusion relation can be published first to the block's OOB marker and then to the flash BBT. A power cut between those writes can leave representation-convergence work for a later boot/operation. The contemporaneous review shows that this is **reconstructive maintenance under an interruption window**, not an atomic transaction guarantee.

For the Linux v4.9 BBT path, failure of the physical block carrying a BBT update can itself create new bad-block state: the BBT carrier is retired, its recorded page is invalidated, and another eligible carrier is sought. The rule of non-use therefore has a maintenance path for replacing one of its own embodiments.

Thus the object being preserved is not only a payload. The system also preserves and updates a **rule of non-use**, can reconcile multiple persistent representations of that rule, and, in the bounded Linux implementation, can relocate the material embodiment that carries the centralized table.

---

## Read, write, erase, and forgetting

### Read

Reading the marker is an evidence-gathering operation used to construct the exclusion map. Ordinary payload reads are a different relation and remain subject to ECC/read-management regimes covered elsewhere.

### Write

A successful write to a logical address need not imply use of the originally calculated physical block. Bad-block management can redirect the target to a known-good replacement while keeping the higher-level designation stable.

The Linux-MTD deepening adds two control-state levels. First, marking a grown bad block can write a distributed OOB witness and a centralized flash-BBT entry in separate steps. Second, writing the BBT itself need not remain bound to the previously selected BBT block: a carrier erase/write failure can retire that block and cause the same BBT update to be attempted elsewhere.

### Erase

Erase has two very different consequences depending on the target:

- ordinary erase prepares a usable Flash block for future programming;
- erasing the original factory marker can destroy defect evidence while leaving the underlying reason for exclusion unresolved.

KIOXIA's product-level negative control now sharpens that distinction further: erase/reprogram can be a recovery action for a retention/read-disturb-degraded but still maintenance-eligible block, while erase remains prohibited for a block already classified bad because the action may destroy its exclusion evidence.

The Linux v3.4 grown-bad-block path introduces a separate implementation-specific caution: it may deliberately erase the affected block before writing a new OOB BBM. The January 2012 review points out that, after an earlier interruption left only the OOB marker current, another power cut between this erase and marker rewrite is a distinct failure window. That source-level path must not be confused with permission to erase a manufacturer-marked factory-bad block under Micron/KIOXIA product rules.

Therefore:

> **marker erasure ≠ defect repair.**

and:

> **maintenance erase/reprogram ≠ permission to recycle a retired bad block.**

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

The Linux 2012 change adds a second representation relation for grown bad blocks: per-block OOB evidence and the centralized flash BBT can both carry the same exclusion rule for different recovery/interpreter paths.

The Linux 2016 change adds another migration boundary: even the good NAND block chosen to carry the BBT can later fail, so the persisted table can require re-embodiment on another BBT-eligible block.

### E — ordered cross-representation publication is not transaction atomicity

Linux v3.4 writes the grown-bad-block OOB marker before updating the flash BBT and the patch author explicitly connects that ordering to power-cut behavior. But the same source accepts an interval in which the OOB BBM and flash BBT disagree, and review identifies an additional erase-before-rewrite interruption seam.

Therefore:

- `OOB BBM current != flash BBT current`;
- `flash BBT current != OOB BBM current` in configurations/history that do not maintain both;
- `BBM-first publication != atomic commit`;
- `temporary disagreement != necessarily loss of exclusion authority` if a surviving witness can be rediscovered;
- `reconstructable control state != exact checkpointed control state`.

This is a bounded engineering reconstruction. It does not prove that the OOB write itself is media-atomic or durable across every power-failure model.

### E — replacement capacity is a continuation resource

Reserved good blocks become useful precisely when an existing physical embodiment must be retired. The available reserve therefore sets one hidden boundary on continued logical storage service.

The same principle now applies recursively but finitely to BBT placement: alternate eligible BBT carriers are continuation capacity for the exclusion metadata itself. Exhausting that candidate set remains a hard boundary for the inspected relocation path.

### E — BBT-carrier retirement is not the same event as replacement durability

The Linux retry sequence distinguishes `classify old carrier bad`, `invalidate its descriptor location`, `choose another candidate`, and `successfully write the table there`. The 2016 review discussion explicitly considered interruption between retirement and replacement.

Therefore:

- `old BBT carrier retired != replacement BBT durable`;
- `carrier-failure retry != crash-atomic BBT transaction`;
- `BBT relation survives a relocation path != every interruption point is harmless`.

### E — current exclusion state is not a complete failure history

A BBT can answer `which blocks must not be used now?` without retaining every test condition, timestamp, raw error count, or sequence by which each entry became bad. A per-block BBM likewise preserves a negative qualification without preserving the complete chronology. These are current operational control states, not automatically audit logs.

### E — error evidence and retirement authority must remain separate

The KIOXIA product witness shows a read-bit-error path that remains within ECC/rewrite maintenance and a program/erase-failure path that leads to replacement and future-access prevention. The system can therefore retain error evidence sufficient to schedule maintenance without yet creating the stronger future-use rule represented by permanent block exclusion.

Bounded relations:

- `correctable/read error != permanent bad-block classification`;
- `rewrite opportunity != replacement obligation`;
- `payload recoverability != carrier admissibility`;
- `carrier retirement != proof that every page is unreadable`.

---

## Functional comparisons — not genealogy

### A — Case 14, SCSI grown-defect reassignment

Both cases show stable logical designation surviving a physical-target change, and both make defect/replacement metadata constitutive of later address resolution.

The difference matters. Case 14's bounded SCSI regime focuses on a disk logical block whose physical sector is reassigned after a grown defect. Case 78 foregrounds NAND's **manufacturer-supplied factory defect marks, host pre-use scan, erasable negative evidence, and lifetime bad-block table**. This is a functional comparison, not evidence that one mechanism descends from the other.

### A — Case 04, mapped Flash

Ordinary Flash relocation/reclamation and bad-block replacement can both change physical embodiment while preserving higher-level identity, but they have different triggers and goals:

- Case 04 relocation is driven by erase-before-rewrite / reclamation geometry;
- Case 78 replacement is driven by physical-block qualification/failure;
- the 2016 Linux-MTD BBT deepening relocates **control metadata** after failure of the block carrying that metadata.

Therefore `bad-block replacement ≠ garbage collection ≠ wear leveling`, and `BBT carrier relocation` is only functionally analogous to payload relocation at the level of replacing a physical embodiment while preserving a higher-level relation.

### A — Cases 36 and 52, correct/refresh and read-disturb maintenance

Case 36 treats ECC-bounded retention maintenance and Case 52 treats read-disturb-induced decay/recovery. KIOXIA's product guidance supplies a manufacturer-side bridge without collapsing the mechanisms: read/random bit errors can justify ECC observation and rewrite, while program/erase status failures can justify replacement and exclusion.

Thus:

- `error-margin maintenance != bad-block retirement`;
- `read-disturb damage != automatically a lifetime bad block`;
- shared use of relocation/erase/reprogram does not establish one algorithm or historical genealogy.

### A — Cases 41/42/74, negative control evidence

A tombstone, delete marker, journal revoke, and bad-block entry all can make a still-physically-present positive candidate inadmissible. The similarity stops at that abstract control relation. Their objects, propagation rules, persistence windows, and failure semantics are different.

The Linux 2012 BBM/BBT path adds a further bounded comparison point: one negative relation can have more than one persistent representation, and representation agreement may itself require later maintenance. This does not make a NAND BBM a distributed-database tombstone.

### A — Case 55, health telemetry

SMART/health counters summarize device condition and history. A BBT instead directly participates in choosing which physical blocks may receive payload. `health evidence ≠ allocation authority`.

---

## Philosophical interpretation — bounded

### I — retention can preserve a prohibition

This case is useful because the retained technical state is not only a positive `what is stored where?` relation. The system also has to preserve `this material location must not count as usable`.

The Linux 2012 deepening adds a restrained point: one prohibition may be carried by several inscriptions with different persistence and interpreter properties, and their agreement can itself become maintenance work after interruption. The 2016 carrier-relocation deepening adds a second point: the prohibition itself has a material carrier, and preserving the relation may require abandoning that carrier when it becomes inadmissible. These are engineering facts about representation and re-embodiment, not claims that the machine literally `remembers how to remember`.

The KIOXIA classification control adds another restrained point: **retention can depend on preserving distinctions among kinds of failure evidence, because correction, rewrite, replacement, and exclusion do not authorize the same future actions.**

The philosophical point should remain modest: **technical availability is partly produced by retained exclusions**. A medium does not become operationally available merely because matter and addresses survive. No stronger Heideggerian claim follows from this engineering fact, and `bad block = Bestand` would be a category mistake.

---

## Counterexamples and limits

- The sources do not establish who first invented NAND bad-block marking or bad-block tables.
- The Micron marker locations are device/family specific; they are not a universal NAND geometry.
- The KIOXIA whole-page marker/test procedure is likewise product-specific and is not substituted for ONFI/Micron geometry.
- The factory mark is not asserted to encode the complete failure mechanism or test history.
- `Bad` does not mean every bit/page in the block is unreadable. The bounded definition is a reliability/admissibility classification.
- A random/read bit error does not automatically imply a bad block in the KIOXIA witness, but that does not prove every such error is always recoverable or that every controller uses identical retirement thresholds.
- KIOXIA's statement that retention/read-disturb-degraded blocks may become usable again after erase/reprogram does not authorize erasing a block already classified bad; the same document explicitly warns against doing so.
- The documented PAGE PROGRAM failure boundary should not be generalized to every failure mode or every NAND generation.
- The 2% reserve statement is limited to the Micron devices covered by TN-29-59 and is not a universal NAND requirement.
- The sources specify operational exclusion/replacement, not secure sanitization of retired blocks.
- A saved BBT is necessary in the documented software design. Linux MTD 2004 adds mirrored/versioned Flash-BBT recovery, but this narrows rather than eliminates update-loss risk and does not prove transactional crash atomicity, dual-copy survival, or universal power-cut safety.
- Linux v3.4's BBM-before-flash-BBT order was explicitly chosen with power cuts in mind, but the patch itself accepts BBM/BBT divergence and contemporaneous review identifies an erase-before-marker-rewrite window. The ordering therefore does not prove atomic update, OOB-program atomicity, or universal reboot recovery.
- `NAND_BBT_NO_OOB_BBM` means the dual-representation scheme is not universal even within Linux raw-NAND configurations.
- Linux v4.9's BBT-carrier retry deepens media-failure tolerance but still does not prove crash atomicity: the failed carrier can be retired before a replacement table is durably materialized, and the bounded candidate reserve can be exhausted.
- The generic Linux v4.9 `NAND_BBT_SCAN_MAXBLOCKS = 4` setting is an implementation default, not a universal NAND requirement and not a statement about every custom descriptor.
- Modern managed SSD controllers may hide this machinery from the host and may use different internal representations.

---

## Prior-art boundary

This case makes **no invention-priority claim** for factory bad-block marking, bad-block tables, block replacement, ECC rewrite, read-disturb/retention maintenance, cross-representation bad-block publication, or BBT-carrier relocation.

The defensible historical statement is narrower:

> By ONFI 1.0 (late 2006), factory-defect mapping and a host-created initial bad-block table were standardized chip-interface obligations; Micron's 2009 product documentation and 2011 technical note make the retention consequence explicit by requiring pre-erase capture of erasable factory defect evidence, durable BBT storage, reboot reconstruction, and runtime replacement of newly bad blocks. KIOXIA's surviving 2018–2019 reliability-management wording later makes a complementary classification boundary explicit: a random/read bit error is not automatically a bad-block verdict, while program/erase status failure can move the carrier onto a replacement/exclusion path.

A separate bounded pre-ONFI witness reaches back to Linux MTD in May 2004: its flash-resident BBT code/documentation already exposes mirrored tables, version-based currentness selection, missing/stale-peer rewrite, and protected BBT regions. Between released Linux v3.3 and v3.4, the default flash-BBT marking path then changed so a grown bad block could also receive a per-block OOB marker, with the BBM deliberately published before the flash-BBT update for bounded power-cut reasons while temporary divergence remained acknowledged. A later bounded implementation change, upstream commit `10ffd570` and released Linux v4.9 in 2016, makes the BBT's **own failed carrier** replaceable during an update by retiring it and searching another eligible BBT block. These are historical floors for the inspected implementations, **not** invention-priority claims.

The `computing-archaeology` repository was searched again for `NAND BBT bad block marker`; no directly reusable case was found. Broader NAND/MTD/bootloader/SSD engineering genealogy still belongs there rather than being recreated here.

---

## Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| NAND may ship with defective blocks and acquire additional bad blocks | H/P | grounded by ONFI/Micron primary documentation |
| manufacturer defect evidence is recorded in spare/defect area | H/P | grounded |
| host should create an initial BBT before erase/program | H/P | grounded |
| original bad-block information can be erased and then become unrecoverable | H/P | grounded in Micron TN and product documentation; independently corroborated by KIOXIA product guidance |
| BBT can be saved in a good NAND block and loaded into RAM at reboot | H/P | grounded in Micron TN |
| PROGRAM/ERASE failure can create lifetime bad-block retirement/replacement work | H/P | grounded in Micron TN and KIOXIA product guidance |
| reserve blocks can carry replacement payload and BBT state | H/P | grounded in Micron TN |
| random/read bit error necessarily means the block is bad | X | explicitly rejected by KIOXIA product guidance |
| read-bit error can remain on an ECC/rewrite path while program/erase failure moves to replacement/exclusion | H/P/E | grounded in KIOXIA failure table; relation is bounded reconstruction |
| retention/read-disturb degradation may become usable again after erase/reprogram | H/P | explicit KIOXIA product statement, not generalized to already-retired bad blocks |
| exact KIOXIA reliability-management wording is conservatively dated to 2018–2019 | H/P/E | grounded by Rev. 2.00 revision history |
| physical addressability ≠ admissible allocation | E | reconstruction from documented exclusion semantics |
| marker erasure ≠ defect repair | E | reconstruction bounded by explicit erasability warning |
| negative defect metadata can preserve positive payload reliability | E | reconstruction |
| bad-block replacement ≠ garbage collection / wear leveling | E/A | bounded comparison; Micron itself lists them separately |
| NAND bad-block replacement ≈ SCSI defect reassignment | A | functional analogy only; no genealogy claimed |
| bad-block mark ≈ tombstone/revoke as negative evidence | A | abstract analogy only |
| Linux MTD flash BBT can retain primary/mirror copies with version currentness | H/P | grounded by 2004 MTD documentation/source |
| higher readable BBT version can seed stale/missing-peer rewrite | H/P | grounded by 28-May-2004 archived source |
| released Linux v3.3 flash-BBT path could leave grown-bad-block OOB markers stale | H/P | grounded by v3.3 source + January 2012 patch rationale |
| Linux v3.4 writes grown-bad-block OOB evidence before flash-BBT update by default unless OOB BBM writing is disabled | H/P | grounded by January 2012 patch + released v3.4 source |
| power cut between OOB BBM and flash-BBT update can leave the representations out of sync | H/P | explicit January 2012 source statement |
| BBM-before-BBT ordering = atomic crash-safe transaction | X | explicitly rejected; divergence and further interruption windows remain |
| Linux v4.9 can retire a BBT carrier that fails erase/write and retry another eligible carrier | H/P | grounded by upstream `10ffd570` and released v4.9 source |
| BBT exclusion relation != one physical BBT carrier | E | bounded reconstruction from 2016 implementation |
| BBT carrier retry != crash-atomic BBT update | E/X | bounded by source ordering and contemporaneous review discussion |
| mirrored/versioned BBT ≠ universal crash-atomic update | E/X | bounded reconstruction and explicit limit |
| reserved-for-BBT ≠ physically defective | E/X | bounded implementation distinction |
| `bad block` proves every page unreadable | X | rejected |
| Micron/ONFI/KIOXIA/Linux invented bad-block management | X | unsupported / not investigated |
| retired bad block is securely erased | X | unsupported |

---

## Sources

### Primary / contemporary

1. Open NAND Flash Interface Working Group, *Open NAND Flash Interface Specification*, Rev. 1.0, §3.2 `Factory Defect Mapping`, official PDF: <https://onfi.org/files/onfi_1_0_gold.pdf>.
2. Micron Technology, *8Gb Asynchronous/Synchronous NAND Flash Memory*, MT29F8G08ABABA / MT29F8G08ABCBB family, Draft 27 February 2009, `Error Management`: <https://www.tme.com/Document/f0626004806cbebd352e6f64f6830d11/MT29F8G08ABABAWPIT.pdf>.
3. Micron Technology, TN-29-59, *Bad Block Management in NAND Flash Memory*, Rev. H, April 2011: <https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/791/tn2959_5F00_bbm_5F00_in_5F00_nand_5F00_flash.pdf>.
4. Linux MTD, Thomas Gleixner, *MTD NAND Driver Programming Interface*, `Bad block table support`, copyright 2004: <https://www.kernel.org/doc./htmldocs/mtdnand/Bad_Block_table_support.html>.
5. Linux MTD CVS archive, 28 May 2004, `nand_bbt.c` 1.9→1.10 and related NAND changes: <https://lists.infradead.org/pipermail/linux-mtd-cvs/2004-May/003683.html>.
6. Linux `v3.3`, `drivers/mtd/nand/nand_base.c`, old flash-BBT-vs-OOB marking branch: <https://github.com/torvalds/linux/blob/v3.3/drivers/mtd/nand/nand_base.c>.
7. Brian Norris, `[PATCH v4 2/2] mtd: nand: write BBM to OOB even with flash-based BBT`, 20 January 2012: <https://lists.infradead.org/pipermail/linux-mtd/2012-January/039391.html>.
8. Shmulik Ladkani / Brian Norris, contemporaneous review of BBM/BBT divergence and erase-before-rewrite interruption windows, 21–23 January 2012: <https://lists.infradead.org/pipermail/linux-mtd/2012-January/039393.html> and <https://lists.infradead.org/pipermail/linux-mtd/2012-January/039406.html>.
9. Linux `v3.4`, `drivers/mtd/nand/nand_base.c`, released BBM-before-flash-BBT path: <https://github.com/torvalds/linux/blob/v3.4/drivers/mtd/nand/nand_base.c>.
10. Linux upstream commit `10ffd570f11701972aff2a6f91f3d253d6f0e7ee`, `mtd: nand_bbt: scan for next free bbt block if writing bbt fails`, 23 September 2016: <https://github.com/torvalds/linux/commit/10ffd570f11701972aff2a6f91f3d253d6f0e7ee>.
11. Linux v4.9, `drivers/mtd/nand/nand_bbt.c` and `include/linux/mtd/bbm.h`: <https://github.com/torvalds/linux/blob/v4.9/drivers/mtd/nand/nand_bbt.c>.
12. KIOXIA Corporation, *TH58NYG3S0HBAI6, 8 Gbit (1G × 8 bit) CMOS NAND E2PROM*, Rev. 2.00, `2019-10-01C`, especially pp. 4 and 61–64 plus revision history p. 66: <https://americas.kioxia.com/content/dam/kioxia/newidr/productinfo/datasheet/201910/DST_TH58NYG3S0HBAI6-TDE_EN_31567.pdf>.

### Related cases

- [`04-flash-virtual-mapping-logical-identity.md`](04-flash-virtual-mapping-logical-identity.md)
- [`14-scsi-disk-defect-reassignment-logical-identity.md`](14-scsi-disk-defect-reassignment-logical-identity.md)
- [`36-nand-flash-correct-and-refresh-maintenance.md`](36-nand-flash-correct-and-refresh-maintenance.md)
- [`47-fast11-ssd-sanitization-verification.md`](47-fast11-ssd-sanitization-verification.md)
- [`52-nand-flash-read-disturb-access-induced-decay.md`](52-nand-flash-read-disturb-access-induced-decay.md)
- [`55-nvme-smart-health-endurance-telemetry.md`](55-nvme-smart-health-endurance-telemetry.md)

### Related repository

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — broad NAND/SSD technical history belongs there; this case keeps only the retention-specific negative-metadata/replacement/error-classification/cross-representation-publication/carrier-relocation argument.

---

## Status

**Grounded bounded case.**

The 2012 deepening closes one bounded power-cut/representation-ordering seam without upgrading the Linux raw-NAND BBT design into a transactionally crash-atomic system. Case 78 now distinguishes the physical defect, RAM exclusion state, per-block OOB exclusion witness, centralized flash-BBT state, version/candidate currentness, and BBT-carrier placement. Remaining work is empirical power-cut fault injection and broader bootloader/controller genealogy, not another generic bad-block-management overview.
