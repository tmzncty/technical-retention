# Evidence 118 — Micron DDR5 Directed Refresh Management, 2012–2024 grounding

## Purpose

This evidence record grounds [`../cases/118-micron-ddr5-directed-refresh-management.md`](../cases/118-micron-ddr5-directed-refresh-management.md).

The bounded question is not whether RowHammer exists or whether DDR5 has generic Refresh Management. Those are already handled in Cases 53 and 54. The narrower question is:

> What primary/manufacturer evidence establishes a DDR5 product contract in which a sampled row address directs refresh toward a bounded set of **physically adjacent neighboring rows**, and what prior art prevents that contract from being misdescribed as the invention of address-directed targeted refresh?

The inspected evidence supports a strong product-contract result and a conservative prior-art floor. It does **not** establish a full JEDEC DRFM genealogy or independent fault immunity.

## Evidence classification

- **H/P** — historical / primary or manufacturer technical record.
- **E** — engineering reconstruction constrained by those records.
- **A** — bounded functional analogy across repository cases.
- **X** — explicitly unsupported or rejected stronger inference.

---

## Source A — Micron 16Gb DDR5 SDRAM Die Rev D, Rev. E, January 2024

### Identity and provenance

Manufacturer: **Micron Technology, Inc.**

Document:

- **16Gb DDR5 SDRAM Die Rev D**;
- document identifier `CCM005-1684161373-39`;
- Rev. E, `01/2024`;
- example part number in the document: `MT60B2G8RZ-64B:D`;
- product organizations shown include 4Gx4, 2Gx8, and 1Gx16.

Publicly inspectable HTML extraction of the manufacturer-authored document:

<https://device.report/m/79c9b0cad85e0bf0b889e0e3b5f5704f52b7b91c61a05a0b158e47c64f7ae743>

The source is therefore **manufacturer-primary in authorship but accessed through a public mirror/extraction**, not through a current Micron-hosted archive. That provenance is retained explicitly.

### Product-specific DRFM section

The addendum contains a section titled:

> `Directed Refresh Management (DRFM) Variance`

It says that this section describes the product's DRFM support and its variance from the core design data sheet. It then replaces the core `Bounded Refresh Configuration (BRC)` / `tDRFM` subsections with product-specific values.

The central contract states that the DRFM command refreshes **physically adjacent neighboring rows** to a **DRFM sampled address**, up to a distance selected by BRC in `MR59:OP[2:1]`.

This sentence is the decisive evidence for Case 118. It separates:

```text
sampled address
    !=
physically adjacent rows actually refreshed
```

The source also assigns responsibility for outer-row refresh ratios to the DRAM itself.

### BRC2 / BRC3 / BRC4 behavior

The product-specific table establishes three supported BRC options:

- **BRC2** — ±1 rows are always refreshed; ±2 rows are ratio-controlled;
- **BRC3** — ±1 always; ±2 and ±3 ratio-controlled;
- **BRC4** — ±1 always; ±2, ±3, and ±4 ratio-controlled.

The prose makes the asymmetry especially explicit for BRC4: ±1 is always refreshed while the farther rows are refreshed according to a device-determined ratio.

Therefore the record directly blocks:

> `inside BRC radius = refreshed on every DRFM command`.

BRC is a bounded **coverage/configuration relation**, while the actual refresh frequency within that bounded neighborhood is nonuniform.

### BRC support state

The addendum says `MR59:OP[3]` is read/write for this device and that the device supports all BRC options (`BRC2`, `BRC3`, `BRC4`) for either value of that support-level bit.

This is a product-specific feature/capability fact. It does not prove identical options in every DDR5 die revision or vendor.

### DRFM duration

The product gives:

```text
tDRFM = (2 * tRRF) * BRC
```

and separates all-bank and same-bank per-row refresh durations. The resulting table is:

| BRC | `tDRFMab` | `tDRFMsb` |
| --- | ---: | ---: |
| 2 | 280 ns | 240 ns |
| 3 | 420 ns | 360 ns |
| 4 | 560 ns | 480 ns |

For this product, broader bounded neighbor coverage therefore reserves more maintenance time.

Safe inference:

> **wider BRC scope != zero additional service exclusion time.**

Unsafe inference:

> `DDR5 universally has these exact tDRFM values`.

The values belong to the inspected Micron product contract.

### Relation to ordinary RFM fields

The same function-matrix region records Refresh Management and Adaptive RFM support and notes that `RAAMMT`, `RAAIMT`, and RAA decrement apply when the RFM requirement bit is set or when ARFM is set to qualifying levels.

That context is useful but Case 118 does not attempt to reconstruct the complete ARFM/DRFM state machine. Case 54 remains the canonical broad RFM/RAA split-authority case.

---

## Source B — Intel row-hammer targeted-refresh patent, 2012 priority / 2014 publication

### Identity

- Intel Corporation, **“Row hammer refresh command”**;
- U.S. application `13/539,415`;
- priority and filing date: **2012-06-30**;
- application publication US20140006703A1: **2014-01-02**;
- later grant US9236110B2.

Public patent record:

<https://patents.google.com/patent/US20140006703A1/en>

Filing/priority date and public publication date are kept separate. The 2012 date is useful for family chronology; the public A1 document dates to January 2014.

### Address-directed targeted refresh

The patent describes a controller-side mechanism that receives a row-hammer indication, identifies an address associated with the hammered row, and sends command/address information so the memory device performs targeted refresh on victim row(s).

The most useful architecture boundary is explicit:

- the controller can supply a row address associated with the target/hammered row;
- the memory device can compute the specific victim-row address or addresses;
- the memory device performs targeted refresh on adjacent victim row(s).

The patent further says that controller-visible adjacent addresses do not necessarily map to physically adjacent internal rows, because device-specific address mapping may intervene.

Therefore this record already establishes, before the Micron 2024 product document, the general relation:

```text
controller-visible / supplied row address
    -> device-specific physical-neighbor resolution
    -> targeted adjacent-row refresh
```

### Off-cycle maintenance

The patent describes targeted refresh as an **off-cycle** refresh relative to regular scheduled refresh. This helps preserve the boundary:

> **disturbance-directed refresh != ordinary periodic refresh progress.**

The patent is not used to determine Micron's exact DDR5 accounting rules. It supplies only an earlier functional mechanism floor.

### Novelty and genealogy limit

This source blocks an overbroad claim that DDR5 DRFM invented the idea of sending address information so a DRAM can refresh physically adjacent victim rows.

It does **not** establish:

- that Intel's design was commercially deployed in the exact disclosed form;
- that the later DDR5 DRFM command descends directly from this patent;
- that Micron used this patent's detector, command sequence, mode-register state, or threshold logic;
- that the patent is the earliest targeted-refresh concept in all prior art.

Thus:

> **chronological/functionally similar prior art != demonstrated genealogy.**

---

## Source C — repository controls

### Case 53 — RowHammer targeted-refresh policy

[`../cases/53-dram-rowhammer-targeted-refresh-policy.md`](../cases/53-dram-rowhammer-targeted-refresh-policy.md) already owns the 2012–2020 disturbance/targeted-refresh history and later mitigation limits. Case 118 reuses that boundary rather than recreating a RowHammer history.

Key reuse:

- target/aggressor row and victim row are different relations;
- logical row adjacency need not equal physical adjacency;
- targeted restoration and ordinary periodic refresh have different triggers;
- mitigation label/support is not itself universal empirical immunity.

### Case 54 — DDR5 RFM split maintenance authority

[`../cases/54-ddr5-rfm-split-maintenance-authority.md`](../cases/54-ddr5-rfm-split-maintenance-authority.md) already owns:

- device-advertised RFM requirement;
- controller-side RAA-like activation pressure;
- RFM scheduling/issuance;
- hidden in-DRAM management;
- platform support vs enablement vs observed command behavior.

Case 118 therefore does **not** duplicate generic RFM. Its new axis is:

> **sampled row anchor + bounded physical-neighbor scope + nonuniform distance-dependent refresh frequency + BRC-dependent timing.**

### Case 112 — HBM3 RFMpb

[`../cases/112-hbm3-rfm-bonus-maintenance-vs-periodic-refresh.md`](../cases/112-hbm3-rfm-bonus-maintenance-vs-periodic-refresh.md) grounds a different activity-conditioned localization: HBM3 `RFMpb` can target one bank without advancing ordinary `REFpb` rolling coverage.

That comparison gives a strong negative control:

> **per-bank RFM target != DRFM sampled-row / physical-neighbor target.**

Shared `RFM` vocabulary does not establish identical geometry.

---

## Historical record / reconstruction / analogy / philosophy separation

### Historical record

The Micron addendum records:

- product/revision identity;
- DRFM support/variance;
- sampled-address wording;
- physical-neighbor refresh wording;
- BRC2/3/4 behavior;
- nonuniform outer-row ratio responsibility;
- BRC support level;
- product-specific `tDRFMab` / `tDRFMsb` timings.

The Intel patent records:

- 2012 priority / 2014 public publication dates;
- row-hammer / targeted-refresh vocabulary;
- command/address-directed refresh;
- controller-visible address vs device-resolved physical victim relation;
- off-cycle targeted refresh.

### Engineering reconstruction

The evidence supports separating:

1. trigger/sample production;
2. sampled row designation;
3. device-internal physical-neighbor resolution;
4. bounded neighbor radius;
5. per-distance refresh-frequency policy;
6. bank-level command scope;
7. maintenance duration;
8. ordinary periodic-refresh progress.

Those eight relations are not one state merely because all participate in `refresh management`.

### Functional analogy

Intel targeted refresh, DDR5 RFM, Micron DRFM, HBM3 RFM, and even magnetic-core half-select disturbance may be compared at selected relational axes. No historical or material identity follows.

### Philosophical limit

The technical result is enough: future availability of one row's data can depend on restoration work directed by another row's access relation and by hidden physical adjacency. No stronger philosophical claim is required. In particular, this does not convert a device-internal neighbor map into `tertiary retention` or make DRAM a privileged model of technical memory in general.

---

## Related-repository audit

`tmzncty/computing-archaeology` was searched in this round for:

- `Directed Refresh Management`;
- `DRFM`.

No dedicated matching case/document was found in the current searchable repository state.

Therefore:

- Case 118 keeps only the retention-specific decomposition and prior-art guardrail;
- a complete JEDEC DDR5 DRFM/ARFM/PRAC chronology, vendor comparison, circuit/layout history, or controller implementation history should primarily live in `computing-archaeology` if developed;
- no technical-history duplication is intentionally introduced here.

---

## Claim ledger

| Claim | Type | Strength | Evidence / limit |
| --- | --- | --- | --- |
| Micron Rev. E 01/2024 product addendum contains a DRFM variance section | H/P | strong | manufacturer-authored mirrored document |
| DRFM uses a sampled address as the anchor for refreshing physically adjacent neighboring rows | H/P | strong | Micron DRFM variance prose |
| BRC is selected through MR59 and bounds neighbor distance | H/P | strong | Micron product contract |
| Product supports BRC2, BRC3, BRC4 | H/P | strong | BRC Support Level text |
| ±1 always refreshed while farther rows may use a ratio | H/P | strong | product-specific BRC table/prose |
| broader BRC increases documented tDRFM | H/P/E | strong in bounded product | table + equation; not universalized |
| sampled row != refreshed-row set | E | strong | direct consequence of wording |
| bank command scope != BRC row radius | E | strong | independent command/timing and BRC axes |
| 2012-priority Intel record already describes address-directed adjacent-victim refresh | H/P | strong bounded prior art | US20140006703A1 family |
| 2012 priority date = public disclosure date | X | rejected | publication was 2014-01-02 |
| Intel targeted refresh = direct DDR5 DRFM ancestor | X | unproven | no influence chain established |
| BRC = complete physical vulnerability map | X | unsupported | configuration/contract only |
| all rows inside BRC refreshed each command | X | contradicted | outer rows are ratio-controlled |
| DRFM command success = empirical arbitrary-pattern immunity | X | unsupported | independent fault validation absent |
| January 2024 = invention date of DRFM/targeted refresh | X | rejected | earlier targeted-refresh record exists; DRFM genealogy unexamined |

---

## Evidence debt

A future maturation pass should seek, in priority order:

1. a directly accessible normative JEDEC revision/technical proposal establishing exact DRFM/BRC adoption chronology;
2. standards text for sampled-address generation/command semantics and interaction with ARFM/PRAC;
3. a named platform/controller trace showing actual DRFM command issuance and sampled addresses;
4. manufacturer documentation for how PPR/remapping affects physical-neighbor targeting;
5. independent fault injection across BRC settings;
6. cross-vendor DDR5 DRFM product contracts;
7. exact outer-row ratio behavior if ever publicly disclosed;
8. earlier pre-2012 targeted-refresh/disturbance-maintenance genealogy.

Until then, the safe project claim is deliberately narrow:

> **By January 2024, a named Micron 16Gb DDR5 die revision publicly documented DRFM as sampled-address-directed refresh of a configurable bounded physical neighborhood, with always-refreshed ±1 rows, ratio-controlled farther rows, and BRC-dependent service time; address-directed adjacent-victim refresh has explicit earlier public technical prior art, so the product record is not an invention-priority proof.**
