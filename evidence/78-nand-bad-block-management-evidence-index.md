# Case 78 Evidence Index — NAND Bad-Block Knowledge, BBT Currentness, and Repair

Canonical case: [`../cases/78-micron-nand-bad-block-marker-management.md`](../cases/78-micron-nand-bad-block-marker-management.md)

**Current maturity:** `grounded`

This file is a navigation and evidence-boundary aid. `CASE_INDEX.md` remains the repository-wide maturity ledger.

Case 78 is about retention of **negative media-qualification state**: a physically addressable NAND block may have to remain excluded from ordinary storage even after the original defect mark could be erased, and that exclusion relation may move through multiple representations over device life.

The current evidence package deliberately separates:

```text
physical defect / failure observation
    != local bad-block evidence
    != RAM working exclusion state
    != persisted BBT summary
    != BBT replica currentness
    != BBT-carrier admissibility
    != BBT replica convergence
    != replacement-block availability
```

---

## 1. Canonical manufacturer / standards grounding

[`../cases/78-micron-nand-bad-block-marker-management.md`](../cases/78-micron-nand-bad-block-marker-management.md)

**Role:** canonical historical and mechanism synthesis.

The case combines ONFI factory-defect mapping, Micron product/technical-note evidence, Linux flash-BBT mechanisms, and later named-device retirement/replacement evidence.

Core relation:

```text
physically selectable block
    != admissible storage block
```

and:

```text
material defect
    != retained evidence describing that defect
```

A factory or grown-bad exclusion relation can therefore require its own retained control state.

---

## 2. Linux MTD 2004 — mirrored and versioned flash BBT

[`78-linux-mtd-2004-mirrored-versioned-bbt-deepening.md`](78-linux-mtd-2004-mirrored-versioned-bbt-deepening.md)

**Role:** persistent-summary redundancy grounding.

Establishes a public Linux-MTD implementation in which flash-resident BBT state can be mirrored, version-qualified, placed in reserved blocks, selected from surviving peers, and rewritten when a peer is absent or stale.

Core boundaries:

```text
saved BBT
    != single infallible embodiment

two copies
    != two equally current authorities

version field
    != complete bad-block event history
```

This packet establishes the redundancy/currentness mechanism but deliberately does not treat it as a universal crash-atomic transaction.

---

## 3. Linux MTD 2004–2021 — currentness arithmetic and candidate admissibility

[`78-linux-mtd-2004-2021-bbt-currentness-admissibility-deepening.md`](78-linux-mtd-2004-2021-bbt-currentness-admissibility-deepening.md)

**Role:** authority-selection deepening.

Separates four relations that `use the newer BBT` can otherwise hide:

```text
candidate discovery
    -> carrier admissibility
    -> version ordering
    -> payload readability / validity
    -> authority selection
```

The packet shows that nearby cyclic version ordering, ECC validity, and the qualification of the block carrying the BBT all participate in currentness.

Therefore:

```text
higher-looking version
    != automatically usable current state
```

and:

```text
retained currentness token
    != retained currentness meaning by itself
```

---

## 4. Linux MTD 2012 — grown-bad marker before flash-BBT update

[`78-linux-mtd-2012-bbm-bbt-power-cut-ordering-deepening.md`](78-linux-mtd-2012-bbm-bbt-power-cut-ordering-deepening.md)

**Role:** cross-representation publication ordering.

The v3.3→v3.4-era change deliberately moves the per-block OOB bad-block marker ahead of the flash-BBT update for the grown-bad path, with power-cut behavior explicitly discussed in development review.

Bounded chain:

```text
new grown-bad block
    -> RAM BBT state
    -> OOB bad-block marker
    -> flash BBT update
```

The packet is important precisely because it does **not** claim atomicity. A power cut can leave marker and BBT temporarily divergent, and later recovery/retry is part of the design discussion.

```text
ordered publication
    != atomic representation convergence
```

---

## 5. Linux MTD v3.3 — serial primary/mirror publication and cut-point asymmetry

[`78-linux-mtd-2012-dual-bbt-update-cutpoint-asymmetry-deepening.md`](78-linux-mtd-2012-dual-bbt-update-cutpoint-asymmetry-deepening.md)

**Role:** replica-publication cut-point deepening.

The inspected source makes the mirrored update sequence explicit:

```text
advance intended version state
    -> rewrite primary BBT
    -> if primary succeeded, rewrite mirror BBT
```

and each copy is itself rewritten as:

```text
erase BBT carrier
    -> write new serialized BBT image
```

The recovery path explicitly handles missing and unequal-version peers.

Therefore:

```text
two persistent BBT copies
    != atomic two-copy commit

same target version in RAM
    != both copies durably published

one current copy survives
    != replica-repair debt has disappeared
```

The cut-point matrix in the packet is a source-level reconstruction, not a physical power-cut experiment.

---

## 6. Linux MTD 2016 — failed BBT carrier relocation

[`78-linux-mtd-2016-bbt-carrier-failure-relocation-deepening.md`](78-linux-mtd-2016-bbt-carrier-failure-relocation-deepening.md)

**Role:** control-metadata-carrier replacement.

A block that stores the BBT can itself become bad. The later Linux path can retire a failing BBT-host block and search for another eligible location within the bounded BBT placement region.

Core boundary:

```text
BBT contents remain logically required
    != current physical BBT carrier remains admissible
```

This is distinct from replica convergence. Carrier relocation answers `where may this control state live?`; mirrored update ordering answers `which copies have reached the intended current image?`.

---

## 7. KIOXIA 2018–2019 — correctable error evidence versus retirement authority

[`78-kioxia-2018-2019-soft-error-vs-bad-block-retirement-deepening.md`](78-kioxia-2018-2019-soft-error-vs-bad-block-retirement-deepening.md)

**Role:** named-product media-state classification boundary.

This packet prevents every correctable or maintainable error indication from being silently upgraded into block-retirement authority.

Core relation:

```text
error observed / corrected
    != block declared permanently inadmissible
```

The exact evidence and replacement policy remain product-specific; this chain is not used to infer Linux-MTD implementation internals.

---

## Unified control-state chain

The evidence package now supports the following bounded synthesis:

```text
physical defect / grown failure
    -> local defect evidence or failure result
    -> working bad-block exclusion state
    -> persistent BBT summary
        -> primary replica publication
        -> mirror replica publication
    -> restart-time candidate discovery
    -> carrier / payload admissibility checks
    -> currentness selection
    -> stale / missing peer repair
    -> continued exclusion or replacement mapping
```

Several non-equivalences are central:

```text
one logical exclusion relation
    != one physical representation

redundancy
    != atomic publication

current copy available
    != all copies converged

control state retained
    != its carrier automatically remains admissible

repairable divergence
    != exact update history retained
```

---

## Cross-case links — functional comparison only

### Case 04 — Flash mapping / reclamation

[`../cases/04-flash-memory-virtual-mapping.md`](../cases/04-flash-memory-virtual-mapping.md)

Both cases separate logical/current authority from physical embodiment, but the control state differs:

- Case 04: positive logical-to-physical identity/currentness and reclaim/reuse boundaries;
- Case 78: negative media qualification, exclusion, BBT persistence, and replacement capacity.

No common historical genealogy is claimed.

### Case 25 — OpenStack Swift EC

[`../cases/25-openstack-swift-ec-reconstruction.md`](../cases/25-openstack-swift-ec-reconstruction.md)

The narrow functional comparison is reconstructive maintenance:

```text
volatile maintenance episode disappears
    != maintenance obligation disappears
```

Swift and Linux MTD implement this in radically different media and control structures. The comparison is conceptual only.

---

## Evidence-strength map

| Question | Best current evidence | Status |
| --- | --- | --- |
| Can NAND contain blocks that remain addressable but must be excluded? | ONFI + Micron canonical case | grounded |
| Can bad-block evidence itself be erasable? | Micron TN-29-59 canonical case | grounded |
| Can a BBT be persisted outside the bad block and reloaded? | Micron + Linux canonical case | grounded |
| Can the flash BBT be mirrored/versioned? | 2004 Linux packet | grounded |
| Is currentness just `larger version wins`? | 2004–2021 currentness packet | grounded negative boundary |
| Can grown-bad OOB evidence be published before BBT summary update? | 2012 ordering packet | grounded |
| Are primary and mirror BBT updates atomic together? | v3.3 serial-publication packet | grounded negative boundary at source level |
| Can the BBT's own carrier fail and be replaced? | 2016 relocation packet | grounded |
| Does every correctable media error authorize retirement? | KIOXIA packet | grounded negative boundary |
| What exact state survives abrupt power loss at every dual-copy cut point? | no controlled trace yet | open |

---

## Open debts, prioritized

### P1 — exact dual-BBT fault injection

Exercise abrupt interruption at source-visible boundaries:

```text
before primary erase
inside / after primary erase
inside / after primary write
between primary and mirror
inside / after mirror erase
inside / after mirror write
```

Then inspect which copies are discovered, which candidate is selected, what version is reported, and whether reconciliation repairs the peer.

This would move the latest source-level cut-point reconstruction toward directly observed failure behavior.

### P1 — combined OOB-marker + primary/mirror interruption trace

The strongest Case-78 fault experiment would span both representation layers:

```text
OOB marker succeeds
    -> primary BBT publication interrupted / succeeds
    -> mirror BBT publication interrupted / succeeds
    -> reboot
    -> scan / authority selection / healing
```

This would test the proposition that lower-level exclusion evidence can preserve enough information for later summary repair in the actual configured path.

### P1 — marker-write failure

The existing ordering result is strongest when the lower-level OOB marker really reaches the device. The failure case where marker publication itself fails needs separate treatment; it must not be silently folded into `BBT update failed`.

### P2 — carrier relocation combined with mirrored update

Combine the 2016 BBT-host failure/relocation path with the primary/mirror publication sequence. The interesting question is not merely whether another carrier is found, but how replica currentness is maintained when the carrier fails during a replica refresh.

### P2 — real configuration witnesses

Identify named boards/SoCs/products that actually select:

- mirrored flash BBT;
- per-block OOB markers plus flash BBT;
- `NAND_BBT_NO_OOB_BBM` or equivalent suppression;
- bootloader-managed or firmware-managed alternatives.

This would prevent generic kernel capability from being mistaken for universal deployed policy.

### P2 — related history in `computing-archaeology`

A fresh search in this round did not surface a dedicated `nand_update_bbt` / dual-BBT publication packet in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). If broader BBT genealogy becomes useful, it should be developed there and linked back rather than duplicated here.

---

## Terminology guardrail

Historical/source terms in the current packet include:

- bad block / bad-block marker;
- bad block table / BBT;
- primary / mirror descriptors;
- version;
- erase / write;
- reserved BBT blocks;
- block replacement.

Project analytical terms include:

- negative media-qualification state;
- exclusion authority;
- representation-divergence debt;
- serially replicated maintenance metadata;
- staged redundant publication;
- reconstructive maintenance;
- control-metadata carrier.

The latter group must not be back-projected into Linux, Micron, ONFI, or KIOXIA historical vocabulary.

---

## Status

- Case: **78**
- Current maturity: **`grounded`**
- Maturity change this round: **none**
- New evidence chain this round: **Linux v3.3 serial primary/mirror BBT publication and cut-point asymmetry**
- `CASE_INDEX.md`: remains the authoritative repository-wide ledger; this focused index does not replace it.
- Last updated: **2026-09-24**
