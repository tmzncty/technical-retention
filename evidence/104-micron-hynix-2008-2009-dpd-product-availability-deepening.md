# Evidence 104B — Mobile DDR Deep-Power-Down Product Availability and Optionality (2008–2009)

## Scope

This note deepens [`../cases/104-micron-lpddr-selective-adaptive-self-refresh.md`](../cases/104-micron-lpddr-selective-adaptive-self-refresh.md) around one narrow chronology/contract question left open by the 2014 Micron low-power-state deepening:

> How early can this repository directly document Deep Power-Down (DPD) in named Mobile DDR product documentation, and does the existence of DPD vocabulary in a product document imply that every listed ordering/configuration necessarily implements it?

Two vendor-authored product documents preserved by distributors/archives give a bounded answer:

1. Micron's `MT46H16M16LF` / `MT46H8M32LF/LG` Mobile DDR datasheet, Rev. H, June 2008, lists Deep Power-Down and describes it as eliminating memory-array power, not retaining data, and requiring a full initialization sequence after exit.
2. Hynix's `H5MS2G22MFR` / `H5MS2G32MFR` 2-Gbit Mobile DDR datasheet, Rev. 1.2, May 2009, describes Deep Power Down as an **optional feature**, says internal voltage generators stop, states that array data plus Mode Register and Extended Mode Register information are lost, and requires complete reinitialization after exit.

This closes only a bounded **named-product public-document floor**. It does not establish when JEDEC first standardized DPD, when either vendor first shipped DPD-capable silicon, whether every ordering code listed in either document implemented the feature, or who invented the mechanism.

Because both surviving copies are vendor-authored documents hosted by third parties rather than current vendor origin pages, historical claims are tagged `H/P*` under repository policy.

---

## Source identity and provenance

### P1 — Micron Mobile DDR, Rev. H 6/08 — `H/P*`

- **Manufacturer:** Micron Technology, Inc.
- **Product family:** `MT46H16M16LF` and `MT46H8M32LF/LG` Mobile DDR SDRAM.
- **Document revision/date:** Rev. H, June 2008.
- **Relevant public mirror:** AllDatasheet HTML rendering of the Micron datasheet.
- **Feature-level evidence:** the front matter lists Deep Power-Down together with Mobile-DDR low-power features such as PASR/TCSR.
- **Operation-level evidence:** the Deep Power-Down section states that DPD achieves maximum power reduction by eliminating power to the memory array; data are not retained; after exit the device requires 200 µs of valid clocks followed by PRECHARGE ALL and the full DRAM initialization sequence.

Accessible pages:

- <https://www.alldatasheet.com/html-pdf/75876/MICRON/MT46H16M16LF/185/1/MT46H16M16LF.html>
- <https://www.alldatasheet.com/html-pdf/75876/MICRON/MT46H16M16LF/9123/49/MT46H16M16LF.html>

The dates in this note are document dates. They are not first-shipment dates or invention dates.

### P2 — Hynix 2-Gbit Mobile DDR, Rev. 1.2 May 2009 — `H/P*`

- **Manufacturer:** Hynix Semiconductor.
- **Product family:** `H5MS2G22MFR` / `H5MS2G32MFR` 2-Gbit Mobile DDR SDRAM.
- **Document revision/date:** Rev. 1.2, May 2009.
- **Preserved vendor document:** distributor-hosted Hynix PDF.
- **Feature-level evidence:** the feature list marks `Deep Power Down` as an **optional** feature and tells the reader to contact the Hynix office for availability.
- **Operation-level evidence:** the DPD section states that internal voltage generators are stopped; all memory data are lost; Mode Register and Extended Mode Register information are lost; exit requires 200 µs before complete device reinitialization; the documented flow includes PRECHARGE ALL, two AUTO REFRESH commands, and mode-register loading.

Accessible copy:

- <https://www.farnell.com/datasheets/1750885.pdf>

The optionality language is part of the product contract and is important evidence against treating feature vocabulary as proof of universal implementation across every ordering/configuration.

---

## Historical record

### H/P* — Micron publicly documented DPD in a named Mobile DDR product family by June 2008

Micron's June-2008 Rev. H datasheet lists `Deep Power-Down` and describes the command/state behavior for a named Mobile DDR family. The DPD section says that the mode reduces power by eliminating power to the memory array and that data are not retained.

The exit path is not described as resuming old array state. After leaving DPD, Micron requires a 200 µs interval with valid clocks, then PRECHARGE ALL and the complete initialization sequence.

The bounded historical floor is therefore:

```text
by June 2008
named Micron Mobile DDR product documentation
    exposes DPD as a non-retentive low-power mode
```

This is earlier than the January/February-2014 Micron documents previously used by Case 104, but it is not a claim that DPD first appeared in 2008.

### H/P* — Hynix documented the same broad mode class in May 2009, but marked it optional

Hynix's May-2009 product document describes Deep Power Down as an optional feature. In the DPD section it states that internal voltage generators are stopped and that **all memory data are lost**. It separately says that Mode Register and Extended Mode Register information are also lost.

On exit, the host must wait 200 µs and completely reinitialize the device. The illustrated sequence includes PRECHARGE ALL, two AUTO REFRESH commands, and loading the mode register.

This adds a second product-level boundary:

```text
feature appears in a product-family document
    !=
feature is guaranteed on every product/configuration named by that document
```

The document itself makes availability conditional.

### H/P* — DPD may discard both payload and configuration/control state

The Hynix source is more explicit than the Micron source about which non-payload state crosses the DPD boundary: Mode Register and Extended Mode Register information are lost alongside array data.

That supports a historical statement about this named Hynix contract, not a universal LPDDR rule:

```text
DPD transition
    can invalidate payload state
    and also invalidate retained device-configuration state
```

The later requirement to reload configuration is therefore not merely ceremonial startup work; at least in this documented product it follows from specified loss of those register values.

---

## Engineering reconstruction

### E — low-power state names do not define one persistence horizon

Case 104 already separates ordinary Power-Down, SELF REFRESH, and DPD. The 2008–2009 product evidence strengthens the historical floor for that distinction while adding an availability dimension:

```text
same product family / interface vocabulary
    !=
same guaranteed capability set for every ordering/configuration
```

A capability can be documented while still being optional.

### E — payload continuity and configuration continuity are separate retention relations

Hynix's explicit loss of array data plus Mode Register / Extended Mode Register information makes the decomposition concrete:

```text
payload state
configuration state
mode / initialization state
```

can cross a power-management boundary differently from ordinary self-refresh operation. The fact that all three need reconstruction after DPD is evidence about the exit contract, not evidence that they share one physical substrate.

### E — complete reinitialization is service restoration, not data restoration

Both vendor documents require a startup/reinitialization path after DPD. Reinitialization restores the device to a state in which normal commands may again be issued; it does not reconstruct the pre-DPD user payload.

Therefore:

```text
operational readiness restored
    !=
old payload restored
```

### E — product-document chronology is not standards genealogy

The two dated documents establish public product-level lower bounds only. They cannot safely answer:

- when JEDEC first standardized DPD;
- whether one vendor copied another;
- whether an earlier vendor product already implemented equivalent behavior;
- whether the 2008/2009 parts were the first shipping devices with DPD.

Those are different historical questions requiring standards/revision and product-line archaeology.

---

## Functional comparison — explicitly non-genealogical

### Micron 2008 versus Hynix 2009

The safe functional comparison is narrow:

- both documents describe a deepest low-power mode in which user payload is outside the retention contract;
- both require substantial reinitialization before normal service resumes;
- Hynix additionally makes feature optionality and loss of MR/EMR state explicit.

What is **not** established:

- identical internal power gating;
- identical voltage domains;
- identical command-state implementation;
- identical die revisions;
- direct vendor-to-vendor genealogy;
- identical availability across every ordering code.

### Case 02 magnetic core

Case 02 supplies an intentionally different functional counterexample: a core array may preserve payload magnetization across controlled loss of power even though surrounding control state is reset and power transitions require protection. Mobile-DDR DPD instead withdraws the documented payload-retention condition and then requires initialization.

This is a functional comparison of **power-boundary retention relations**, not a claim of shared mechanism or historical continuity.

---

## Rejected upgrades / limits

### X — no JEDEC introduction date

Neither vendor datasheet by itself establishes when Deep Power-Down entered a JEDEC Mobile DDR / LPDDR standard or became normative/optional there.

### X — no invention or first-product claim

June 2008 Micron and May 2009 Hynix are public-document floors for named products. Earlier implementations or publications may exist.

### X — no universal feature-availability claim

Hynix explicitly labels DPD optional. The existence of a command description therefore cannot be promoted into `every listed H5MS2G22MFR/H5MS2G32MFR configuration necessarily supports DPD` without ordering-code or availability evidence.

### X — no sanitization claim

`All memory data is lost` / `data will not be retained` are product retention contracts. They do not specify forensic remanence, exact capacitor-decay time, a verification pass, or an assurance level for sanitization.

### X — no exact cell-state trajectory

Neither document exposes the analog charge trajectory of every cell after DPD entry. The interface-level contract is non-retention, not a measured physical-erasure curve.

---

## What this closes and what remains open

This slice closes a bounded part of Case 104's earlier open work:

1. named Mobile DDR product documentation with DPD is directly visible by **June 2008** in Micron's Rev. H family document;
2. a separate **May 2009** Hynix family document independently describes DPD and makes optionality explicit;
3. Hynix documents that DPD can lose both user payload and MR/EMR configuration state;
4. both vendors require reinitialization rather than payload resume after DPD.

Still open:

- pre-2008 DPD product/document genealogy;
- JEDEC normative introduction and revision history;
- exact ordering-code / commercial-option availability for the Hynix optional feature;
- controller policy deciding when DPD is selected;
- cross-vendor supply-domain and entry/exit timing differences beyond these documents;
- hardware decay/remanence measurements after DPD;
- broader mobile-memory power-management genealogy.

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated Deep Power-Down / Mobile-DDR module to reuse. Broader standards, product-line, and circuit genealogy belongs there rather than being rebuilt here.
