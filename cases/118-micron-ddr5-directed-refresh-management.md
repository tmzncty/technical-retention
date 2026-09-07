# Case 118 — Micron DDR5 Directed Refresh Management: Sampled-Row Authority and Bounded Physical-Neighbor Refresh

## Status

**`grounded`** — bounded to Micron's 16Gb DDR5 SDRAM Die Revision D product addendum, Rev. E (January 2024), especially its product-specific Directed Refresh Management (`DRFM`) variance, Bounded Refresh Configuration (`BRC`), and `tDRFM` contract. Earlier Intel row-hammer targeted-refresh patent evidence is used only to establish a pre-DRFM functional/prior-art floor; it is not treated as a direct genealogy into DDR5 DRFM.

Grounding record: [`../evidence/118-micron-2012-2024-ddr5-drfm-grounding.md`](../evidence/118-micron-2012-2024-ddr5-drfm-grounding.md).

## Scope

Cases 53 and 54 already establish two nearby but different relations. Case 53 shows that repeated activation of one DRAM row can endanger physically adjacent victim rows and that targeted restoration predates modern DDR5 RFM. Case 54 shows the broader DDR5 `RFM` split-authority contract: the device can advertise extra-management requirements while controller-side activity accounting schedules an interval in which the DRAM performs internal work.

Case 118 asks a narrower question:

> What changes when extra DRAM maintenance is directed by a **sampled row address**, while the device itself is responsible for refreshing a **bounded set of physically adjacent neighboring rows** around that address?

The bounded object is Micron's January-2024 16Gb DDR5 Die Rev D product contract. It is not a complete history of DDR5, RowHammer, TRR, RFM, ARFM, DRFM, PRAC, or JEDEC committee development.

This case is **not**:

- a claim that Micron or DDR5 invented targeted neighbor refresh;
- a claim that the January-2024 addendum is the first DRFM implementation or first DRFM publication;
- a claim that every DDR5 part supports the same `BRC` options or timings;
- a claim that a sampled row address exposes the device's internal physical row map;
- a claim that every row inside the configured BRC radius is refreshed at the same frequency;
- a claim that `DRFM` replaces ordinary periodic `REF`/`REFsb` work;
- a claim that the manufacturer contract independently proves RowHammer immunity under every access pattern;
- a reverse engineering of the device's internal victim-selection, remapping, or refresh scheduling algorithm.

## Historical record

### Micron 16Gb DDR5 Die Rev D, Rev. E, January 2024

Micron document `CCM005-1684161373-39`, **16Gb DDR5 SDRAM Die Rev D**, Rev. E (`01/2024`), identifies itself as a product-specific addendum whose content supersedes the corresponding core-data-sheet material where the two differ. The document gives an example part number `MT60B2G8RZ-64B:D` and covers x4/x8/x16 organizations in this die revision.

Its DDR5 function matrix marks Refresh Management and Adaptive RFM as supported and directs the reader to a dedicated **Directed Refresh Management (DRFM) Variance** section for product-specific DRFM behavior.

The decisive product language is unusually concrete:

- `DRFM` operates relative to a **DRFM sampled address**;
- the command refreshes **physically adjacent neighboring rows** to that sampled address;
- `MR59:OP[2:1]` selects a **Bounded Refresh Configuration (BRC)**;
- this product supports `BRC2`, `BRC3`, and `BRC4`;
- `BRC2` always refreshes the physically adjacent ±1 rows, while ±2 may be refreshed at a device-selected ratio;
- `BRC3` and `BRC4` extend the bounded neighborhood, while the rows beyond ±1 are ratio-controlled rather than necessarily refreshed on every command;
- `tDRFM` grows with BRC according to `(2 * tRRF) * BRC`;
- the all-bank and same-bank forms have different product timings.

For this 16Gb die revision the table gives `tDRFMab` values of 280/420/560 ns for BRC2/3/4 and `tDRFMsb` values of 240/360/480 ns.

These are **manufacturer product-contract facts**, not universal DDR5 timing laws.

### Earlier targeted-refresh prior art

Intel's `Row hammer refresh command` family has a 30 June 2012 priority date; US20140006703A1 was published on 2 January 2014. The public record already describes a controller identifying an address associated with a hammered row, conveying address information to a memory device, and the memory device determining which physically adjacent victim row or region to refresh. It explicitly notes that host/controller-visible adjacent addresses need not be physically adjacent inside DRAM.

That earlier record matters here only as a novelty guardrail:

> **2024 Micron DRFM documentation ≠ invention of address-directed targeted neighbor refresh.**

The inspected evidence does not establish that the Intel patent family directly caused, supplied, or was implemented as DDR5 DRFM.

## Retained states and constitutive relations

The bounded DRFM regime contains several distinct things that should not be collapsed into one `refresh state`:

1. **payload charge state** — the DRAM data whose integrity is the ultimate retention target;
2. **ordinary periodic-refresh obligation** — baseline restoration work independent of this case's directed-maintenance relation;
3. **sampled row address** — the address around which a DRFM operation is directed;
4. **device-internal physical-neighbor relation** — which physical rows are adjacent to the sampled row after device-specific layout/mapping;
5. **BRC configuration** — the configured maximum neighbor distance considered by the bounded DRFM contract;
6. **outer-row refresh ratio policy** — the device's retained/implemented rule for how often rows beyond ±1 are refreshed;
7. **DRFM command form** — all-bank or same-bank directed-maintenance scope in the bounded product documentation;
8. **`tDRFM` service exclusion / maintenance duration** — time reserved for the directed work;
9. **RowHammer/activity evidence upstream of sampling** — whatever mechanism produces the sample or decides a row deserves directed maintenance, which the inspected product addendum does not fully expose.

Only the first is application payload. The address, BRC, ratio policy, command form, and timing are **second-order retention infrastructure** that determine how future restoration work is targeted.

## Engineering reconstruction

### The sampled row is an anchor, not necessarily the row being restored

The product documentation says DRFM refreshes physically adjacent neighboring rows **to** the sampled address. Therefore the address named to the mechanism and the rows receiving restoration are not identical objects.

> **DRFM sampled address ≠ DRFM refreshed-row set.**

That distinction is retention-significant. The command can be directed by evidence about one row while spending restoration work on other rows whose future state is endangered by the first row's activity.

This sharpens the general access-disturbance relation already established by Case 53:

```text
activity / sampled aggressor relation
    -> sampled row designation
    -> device resolves physical neighborhood
    -> directed restoration of neighboring rows
```

The logical request history that motivated sampling is upstream; the physical restoration target is downstream.

### Address-directed maintenance does not expose physical topology

The earlier Intel patent already warns that controller-visible adjacent addresses need not be physically adjacent in DRAM and allows the memory device to compute the victim-row address from the supplied row address and its own configuration. Micron's later product contract similarly speaks in terms of **physically adjacent neighboring rows** around a sampled address without publishing the complete internal row map.

Therefore:

> **sampled address visibility ≠ physical-neighbor-map visibility.**

and:

> **controller-selected anchor ≠ controller knowledge of every physical victim row.**

A host/controller can participate in directing maintenance while the device retains decisive spatial knowledge.

This is a different kind of split authority from Case 54's RAA accounting. Case 54 centers on **when** extra management becomes due and which bank-level opportunity is issued. Case 118 centers on **where** directed restoration is anchored and how the device translates that anchor into a bounded physical neighborhood.

### BRC is a bounded maintenance radius, not a complete victim proof

For the inspected product, `BRC2`, `BRC3`, and `BRC4` increase the maximum stated adjacent-row distance involved in DRFM. But the addendum does not say that every actually vulnerable cell is always exactly within the chosen radius under every internal remapping or disturbance pattern, nor that BRC is itself an empirical fault map.

Therefore:

> **configured BRC distance ≠ demonstrated physical vulnerability boundary.**

BRC is a **maintenance contract/configuration parameter**. Independent RowHammer testing would be required to turn it into a claim about complete fault coverage for a named module/system.

### Inclusion in the BRC neighborhood does not mean equal refresh frequency

The product-specific variance is especially important because it prevents a common simplification. The ±1 rows are always refreshed, while farther rows can be refreshed according to a DRAM-controlled ratio. For BRC4, for example, the documentation does not promise that ±2, ±3, and ±4 all receive a refresh on every DRFM command.

Therefore:

> **inside configured BRC radius ≠ refreshed on every DRFM command.**

and:

> **maintenance coverage set ≠ uniform maintenance frequency.**

The device can preserve a spatial coverage relation while applying a nonuniform temporal policy inside it.

### Wider BRC spends more maintenance time in the bounded product

Micron gives the product relation:

```text
tDRFM = (2 * tRRF) * BRC
```

and tabulates increasing durations from BRC2 through BRC4. Thus a broader bounded physical-neighbor scope is not free at the interface: the commanded maintenance interval increases with configured breadth.

For the inspected part:

```text
BRC2 -> 280 ns DRFMab / 240 ns DRFMsb
BRC3 -> 420 ns DRFMab / 360 ns DRFMsb
BRC4 -> 560 ns DRFMab / 480 ns DRFMsb
```

This supports a narrow engineering relation:

> **wider directed-maintenance scope ≠ zero additional service cost.**

It does **not** prove a universal linear performance cost for every DDR5 product, workload, or controller. It is a product-contract timing relation.

### Same-bank/all-bank command scope is separate from physical-neighbor distance

The addendum provides different `tDRFMab` and `tDRFMsb` values, while BRC independently selects the bounded adjacent-row distance.

Therefore at least two geometry axes must remain separate:

> **bank-level command scope ≠ row-neighborhood refresh radius.**

This is useful against a recurrent vocabulary trap. `same-bank`, `all-bank`, `per-bank`, `BRC4`, and `±4` all sound spatial, but they describe different layers of the maintenance geometry.

Case 112 provides the corresponding HBM3 counterexample: its `RFMpb` selects one bank as an activity-conditioned management target, but that does not by itself expose a sampled row or a bounded physical-neighbor radius.

### Directed refresh remains distinct from ordinary periodic refresh

The earlier Intel targeted-refresh record explicitly describes targeted refresh as off-cycle relative to regular refresh. Existing Cases 03, 33, 54, 105, 106, and 112 separately ground ordinary periodic-refresh obligations and their scheduling/geometry.

Case 118 therefore preserves:

> **directed disturbance maintenance ≠ ordinary periodic retention refresh.**

A DRFM operation may use the physical act of refreshing rows, but its trigger/anchor/coverage relation is different. It should not be counted as proof that the baseline all-row periodic-retention obligation has disappeared unless an exact standard/product clause establishes such accounting.

### DRFM completion is weaker than a universal integrity certificate

The product document specifies which bounded neighbor relation the device must service and how much command time is reserved. It does not publish every internal detector state, row-remapping table, victim-selection algorithm, or post-operation fault-verification result.

Therefore:

> **DRFM command completion ≠ independent proof of RowHammer immunity.**

and:

> **manufacturer maintenance contract ≠ empirical fault-validation result.**

This is the same evidence discipline used elsewhere in the repository: an interface/manufacturer contract establishes a required behavior in scope; independent testing is a different evidence layer.

## Historical record vs engineering reconstruction

### Historical record

The January-2024 Micron product addendum documents DRFM, sampled-address wording, BRC2/3/4 support, nonuniform outer-row refresh ratios, and product-specific `tDRFM` timings. The 2012-priority / 2014-public Intel patent documents an earlier address-directed targeted-refresh mechanism in which the device can resolve physical victim rows from controller-provided address information.

### Engineering reconstruction

From those records the repository can safely distinguish:

```text
maintenance trigger / sample production
    != sampled row address
    != physical-neighbor relation
    != bounded neighbor radius
    != per-distance refresh ratio
    != bank-level command scope
    != maintenance duration
    != baseline periodic refresh progress
```

The documents do not need to use this exact decomposition for it to be a valid mechanism-first reconstruction.

### Functional analogy

Case 53's RowHammer targeted refresh, Case 54's DDR5 RFM, Case 112's HBM3 RFM, and Case 118's Micron DRFM can be compared functionally because all concern extra maintenance under access/disturbance pressure. They must not be flattened into one implementation or one historical lineage.

### Philosophical interpretation — bounded

The technical pressure point is spatial rather than metaphysical: a state's ability to remain can depend on a relation to **neighboring physical states that are not the named access target**. The system can expose one address as the maintenance anchor while retaining the decisive adjacency relation inside the device.

That makes `availability` or `persistence` relational in a very literal engineering sense, but it does not by itself establish a Heideggerian `Bestand`, a Stieglerian tertiary retention, or one general philosophy of memory. The philosophical gain is only that mechanism-first analysis prevents `addressed state` from being mistaken for `self-contained state`.

## Cross-case controls

### Case 53 — RowHammer / targeted refresh

Case 53 owns the 2012–2020 disturbance and targeted-refresh prior-art boundary. Its Intel patent evidence already has the key split: controller-visible address information can identify a hammered row while the DRAM resolves physical victim adjacency.

Case 118 therefore does **not** claim that DDR5 DRFM originated targeted refresh. Its narrower contribution is a later named product contract exposing a sampled-address DRFM plus configurable bounded physical-neighbor scope and timing.

> **earlier targeted-refresh mechanism ≠ proven direct DRFM genealogy.**

### Case 54 — DDR5 RFM split authority

Case 54 asks who advertises the need for extra management, who retains activation pressure, and who issues/performs RFM. Case 118 adds a directed spatial contract.

> **RAA / bank-pressure accounting ≠ sampled-row directed neighbor scope.**

`RFM` and `DRFM` belong to the same broad DDR5 maintenance family in the inspected Micron documentation, but shared naming does not make their control state or target geometry identical.

### Case 112 — HBM3 RFMpb

HBM3 Case 112 shows that one activity-conditioned RFM command can target one bank without advancing the ordinary rolling `REFpb` all-bank cycle. Case 118 shows a different localization: a row-address anchor with bounded physical-neighbor restoration inside a DDR5 product.

> **per-bank management target ≠ row-address-directed physical-neighbor target.**

### Case 70 — magnetic-core half-select disturbance

A distant functional analogy is possible: both cases show that a logical non-target can experience material effects because of physical selection geometry. But core half-select excitation and DRAM RowHammer/DRFM are different substrates, timescales, physics, and historical lineages.

> **shared non-target disturbance pattern ≠ shared physical mechanism or genealogy.**

## Prior art and anti-anachronism

The repository uses Micron's own 2024 vocabulary — `Directed Refresh Management`, `DRFM sampled address`, `Bounded Refresh Configuration`, `BRC`, `tDRFM` — only for the later DDR5 product record.

The earlier Intel patent uses `row hammer event`, `targeted refresh command`, `target row`, and `victim row`. Those terms are retained as the earlier source's vocabulary rather than silently relabeling the 2012 design as `DRFM`.

Thus:

> **functional prior art ≠ terminological identity.**

The 2012 priority date is also not a universal invention-priority judgment for targeted DRAM maintenance. Earlier disturbance/refresh concepts may exist. This slice only establishes that **one explicit address-directed adjacent-victim refresh record predates the 2024 Micron DRFM product document by more than a decade**.

## Claim ledger

| Claim | Type | Strength / limit |
| --- | --- | --- |
| Micron 16Gb DDR5 Die Rev D Rev. E 01/2024 has a product-specific DRFM variance section | H/P | strong; manufacturer-authored document through public mirror |
| DRFM refreshes physically adjacent neighboring rows around a sampled address | H/P | strong for inspected product |
| MR59 BRC selects bounded neighbor distance | H/P | strong for inspected product |
| This product supports BRC2/3/4 | H/P | strong |
| ±1 rows are always refreshed while farther rows may use a DRAM-selected ratio | H/P | strong; exact ratio is not disclosed |
| `tDRFM` increases with BRC and differs for DRFMab/DRFMsb | H/P | strong for documented timings |
| sampled address and refreshed-row set are different relations | E | strong reconstruction from product wording |
| bank command scope and row-neighbor radius are separate geometry axes | E | strong |
| Intel's 2012-priority record predates this product record with address-directed victim refresh | H/P | strong chronological/functional prior-art floor |
| Intel targeted refresh directly evolved into DDR5 DRFM | X | unproven |
| BRC equals the complete physical vulnerability radius | X | unproven |
| all rows inside BRC are refreshed on every DRFM | X | contradicted by ratio wording |
| DRFM completion proves immunity to arbitrary RowHammer patterns | X | unsupported by manufacturer contract alone |
| January 2024 is DRFM invention date | X | rejected |

## Evidence debt / open work

Still open:

- exact JEDEC revision / task-group / technical-proposal chronology by which DRFM and BRC entered DDR5;
- public draft/final normative command encoding and sampling rules where legally accessible;
- the mechanism that generates or selects the `DRFM sampled address` on a named controller/platform;
- how internal remapping and spare/PPR rows affect physical-neighbor resolution;
- exact outer-row ratio policy for the inspected Micron die;
- independent DDR5 DRFM bus traces;
- named-DIMM RowHammer/fault-injection validation under BRC2/3/4;
- ARFM/DRFM/PRAC interactions in later DDR5 revisions;
- broader pre-2012 targeted-refresh genealogy.

Broader DDR5/RowHammer engineering history should primarily be developed in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) if it becomes a dedicated historical line. Current repository search there found no dedicated `DRFM` / `Directed Refresh Management` case to reuse.

## Sources

1. Micron Technology, **16Gb DDR5 SDRAM Die Rev D**, document `CCM005-1684161373-39`, Rev. E, January 2024, especially the DDR5 Function Matrix and `Directed Refresh Management (DRFM) Variance` / `Bounded Refresh Configuration (BRC) and tDRFM` section. Public HTML extraction of the manufacturer document: <https://device.report/m/79c9b0cad85e0bf0b889e0e3b5f5704f52b7b91c61a05a0b158e47c64f7ae743>.
2. Intel Corporation, **“Row hammer refresh command,”** US20140006703A1 / US9236110B2 family, priority 30 June 2012, application publication 2 January 2014. Public patent record: <https://patents.google.com/patent/US20140006703A1/en>.
3. Internal comparison controls: [`53-dram-rowhammer-targeted-refresh-policy.md`](53-dram-rowhammer-targeted-refresh-policy.md), [`54-ddr5-rfm-split-maintenance-authority.md`](54-ddr5-rfm-split-maintenance-authority.md), and [`112-hbm3-rfm-bonus-maintenance-vs-periodic-refresh.md`](112-hbm3-rfm-bonus-maintenance-vs-periodic-refresh.md).
