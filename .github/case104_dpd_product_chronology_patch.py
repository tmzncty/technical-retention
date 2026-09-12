from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"anchor missing in {path}: {old[:160]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


def append_once(path: str, required_marker: str, addition: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if required_marker not in text:
        raise SystemExit(f"required marker missing in {path}: {required_marker!r}")
    if addition.strip() in text:
        raise SystemExit(f"addition already present in {path}")
    p.write_text(text.rstrip() + "\n\n" + addition.strip() + "\n", encoding="utf-8")


baseline = "496f2ff0ea7eef83eda7779badb9674662bbf227"
evidence_path = Path("evidence/104-micron-hynix-2008-2009-dpd-product-availability-deepening.md")
case_path = Path("cases/104-micron-lpddr-selective-adaptive-self-refresh.md")
roadmap_path = Path("ROADMAP.md")
index_path = Path("CASE_INDEX.md")

if evidence_path.exists():
    raise SystemExit("Case 104 DPD chronology evidence already exists")
if "### Findings 3796–3811" in index_path.read_text(encoding="utf-8"):
    raise SystemExit("CASE_INDEX findings already present")
if "Case 104 Mobile DDR DPD earlier-product / optional-capability deepening" in roadmap_path.read_text(encoding="utf-8"):
    raise SystemExit("ROADMAP item already present")


evidence_path.write_text(r'''# Evidence 104B — Mobile DDR Deep-Power-Down Product Availability and Optionality (2008–2009)

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
''', encoding="utf-8")

# Add the evidence link immediately after the existing low-power deepening navigation.
nav_anchor = "Low-power-state retention-boundary deepening: [`../evidence/104-micron-2014-lpddr-low-power-retention-boundary-deepening.md`](../evidence/104-micron-2014-lpddr-low-power-retention-boundary-deepening.md). This product-level slice separates ordinary Power-Down, SELF REFRESH, and DPD without turning DPD content loss into a sanitization claim."
nav_repl = nav_anchor + "\n\nEarlier DPD product-availability / optionality deepening: [`../evidence/104-micron-hynix-2008-2009-dpd-product-availability-deepening.md`](../evidence/104-micron-hynix-2008-2009-dpd-product-availability-deepening.md). This earlier named-product slice moves the bounded public-document floor to June 2008 and adds Hynix May-2009 optional-feature plus MR/EMR-loss evidence without turning product chronology into JEDEC or invention genealogy."
replace_once(str(case_path), nav_anchor, nav_repl)

# Add the historical result after the existing DPD power-boundary section.
hist_anchor = "The content-loss statement is still not a sanitization guarantee. The datasheet does not establish the cell-level remanence horizon, laboratory recoverability, or verified physical erasure after DPD.\n\n## Retained state and control state"
hist_repl = """The content-loss statement is still not a sanitization guarantee. The datasheet does not establish the cell-level remanence horizon, laboratory recoverability, or verified physical erasure after DPD.

### H/P* — named Mobile-DDR DPD product documents are visible by 2008–2009, with optionality still explicit

Micron's earlier Mobile DDR Rev. H document (June 2008) already lists Deep Power-Down for the `MT46H16M16LF` / `MT46H8M32LF/LG` family and gives the same broad non-retentive boundary: memory-array power is eliminated, payload is not retained, and exit is followed by 200 microseconds of valid clocks plus PRECHARGE ALL and the full initialization sequence.

Hynix's `H5MS2G22MFR` / `H5MS2G32MFR` Rev. 1.2 document (May 2009) independently describes Deep Power Down, but marks it as an **optional feature**. Its DPD section says internal voltage generators stop, all memory data are lost, and Mode Register plus Extended Mode Register information are also lost; exit requires a 200-microsecond wait and complete device reinitialization.

These dated documents are product-document lower bounds, not invention or JEDEC-standardization dates. They add two bounded distinctions:

```text
product-family documentation includes DPD
    !=
every ordering/configuration necessarily implements DPD

DPD payload loss
    can coexist with
configuration/control-state loss
```

The Hynix optionality statement is especially important: presence of interface vocabulary and a command description is not by itself proof of universal feature availability.

Detailed source treatment: [`../evidence/104-micron-hynix-2008-2009-dpd-product-availability-deepening.md`](../evidence/104-micron-hynix-2008-2009-dpd-product-availability-deepening.md).

## Retained state and control state"""
replace_once(str(case_path), hist_anchor, hist_repl)

# Expand the retained-state decomposition with the newly explicit Hynix configuration-state witness.
state_anchor = "4. **power/mode state** — whether the device is in ordinary operation, self refresh, or DPD.\n\nThe project terms `retention-scope policy` and `maintenance-rate control` are engineering reconstructions, not Micron's historical vocabulary."
state_repl = """4. **power/mode state** — whether the device is in ordinary operation, self refresh, or DPD;
5. **device-configuration state** — mode-register settings that may need to be reconstructed after a deep-power transition; the May-2009 Hynix product document explicitly says MR/EMR information is lost in DPD.

The project terms `retention-scope policy` and `maintenance-rate control` are engineering reconstructions, not Micron's or Hynix's historical vocabulary. The Hynix MR/EMR statement is a named-product witness and must not be universalized to every LPDDR generation."""
replace_once(str(case_path), state_anchor, state_repl)

# Add compact claim-ledger rows before the existing negative sanitization row.
ledger_anchor = "| DPD content loss is equivalent to verified sanitization | X | not established; no remanence / recovery / erase-assurance evidence |"
ledger_repl = """| Micron Rev. H 6/08 publicly documents DPD for a named Mobile DDR product family, with non-retention and full-init exit semantics | H/P* | Micron vendor document preserved by archival mirror |
| Hynix Rev. 1.2 05/09 documents DPD as optional and states that payload plus MR/EMR state are lost | H/P* | Hynix vendor datasheet preserved by distributor |
| appearance of DPD in a product-family document proves universal availability across every listed configuration | X | contradicted by Hynix's explicit optional-feature language |
| DPD content loss is equivalent to verified sanitization | X | not established; no remanence / recovery / erase-assurance evidence |"""
replace_once(str(case_path), ledger_anchor, ledger_repl)

# Add the two earlier product documents to the source list after the existing 2014 source.
source_anchor = "4. Micron Technology, Inc., _512Mb: x16, x32 Mobile LPDDR SDRAM_, `t67m_512mb_mobile_lpddr.pdf`, Rev. I, January 2014, especially pp. 90–94; vendor-origin datasheet preserved via Texas Instruments: <https://e2e.ti.com/cfs-file/__key/telligent-evolution-components-attachments/00-791-00-00-00-38-27-14/T67M_5F00_512Mb_5F00_mobile_5F00_lpddr_5F00_sdram.pdf>."
source_repl = source_anchor + "\n5. Micron Technology, Inc., Mobile DDR SDRAM `MT46H16M16LF` / `MT46H8M32LF/LG`, Rev. H, June 2008, especially feature list and Deep Power-Down operation; vendor-origin text preserved by AllDatasheet: <https://www.alldatasheet.com/html-pdf/75876/MICRON/MT46H16M16LF/185/1/MT46H16M16LF.html> and <https://www.alldatasheet.com/html-pdf/75876/MICRON/MT46H16M16LF/9123/49/MT46H16M16LF.html>.\n6. Hynix Semiconductor, _2Gbit Mobile DDR SDRAM_, `H5MS2G22MFR` / `H5MS2G32MFR`, Rev. 1.2, May 2009, especially feature list and Deep Power Down operation; vendor datasheet preserved by Farnell: <https://www.farnell.com/datasheets/1750885.pdf>."
replace_once(str(case_path), source_anchor, source_repl)

# ROADMAP: record the bounded closure while leaving standards genealogy open.
roadmap_anchor = "## Phase 2 — Build missing technical bridges\n\n"
roadmap_item = """- [x] **Case 104 Mobile DDR DPD earlier-product / optional-capability deepening:** [`cases/104-micron-lpddr-selective-adaptive-self-refresh.md`](cases/104-micron-lpddr-selective-adaptive-self-refresh.md) + [`evidence/104-micron-hynix-2008-2009-dpd-product-availability-deepening.md`](evidence/104-micron-hynix-2008-2009-dpd-product-availability-deepening.md) move the bounded named-product public-document floor earlier than the existing 2014 witness: Micron Rev. H (June 2008) already documents DPD as eliminating array power, not retaining data, and requiring full initialization after exit; Hynix Rev. 1.2 (May 2009) independently documents DPD but explicitly marks it optional, and states that memory data plus MR/EMR configuration state are lost. This closes only the bounded earlier-product gap and fixes `product-family vocabulary != universal feature availability`, `payload loss can coexist with configuration-state loss`, and `reinitialization != payload restoration`. JEDEC introduction/revision chronology, pre-2008 product genealogy, exact optional-ordering availability, controller policy, remanence tests, and wider mobile-memory power-management history remain open; broader genealogy belongs primarily in `computing-archaeology`.\n\n"""
replace_once(str(roadmap_path), roadmap_anchor, roadmap_anchor + roadmap_item)

# CASE_INDEX: continue from the verified previous tail (3795).
findings = r'''### Findings 3796–3811 — Case 104 Mobile DDR DPD earlier-product / optional-capability boundary

- **3796 — H/P*** — Micron's Mobile DDR Rev. H document is dated June 2008 and names the `MT46H16M16LF` / `MT46H8M32LF/LG` product family while listing Deep Power-Down among its low-power capabilities.
- **3797 — H/P*** — Micron's June-2008 DPD section says the mode obtains maximum power reduction by eliminating power to the memory array and that data are not retained.
- **3798 — H/P*** — The same Micron document requires a 200-microsecond exit interval with valid clocks followed by PRECHARGE ALL and the full DRAM initialization sequence before ordinary service resumes.
- **3799 — H/P*** — Hynix's `H5MS2G22MFR` / `H5MS2G32MFR` 2-Gbit Mobile DDR Rev. 1.2 document is dated May 2009 and lists Deep Power Down as an optional feature whose availability requires vendor confirmation.
- **3800 — H/P*** — Hynix says DPD stops internal voltage generators and loses all memory data in the bounded product contract.
- **3801 — H/P*** — Hynix separately states that Mode Register and Extended Mode Register information are lost in DPD, making non-payload configuration-state loss explicit.
- **3802 — H/P*** — Hynix requires a 200-microsecond delay and complete device reinitialization after DPD; the documented sequence includes PRECHARGE ALL, two AUTO REFRESH commands, and mode-register loading.
- **3803 — E** — `product-family documentation includes DPD != every ordering/configuration necessarily implements DPD`; Hynix's explicit optionality blocks universal feature-availability inference.
- **3804 — E** — `payload continuity != configuration continuity`: the Hynix witness shows one power-management transition can invalidate both user data and device-configuration state while those remain analytically distinct state classes.
- **3805 — E** — `complete reinitialization != payload restoration`; the exit sequence restores command/service admissibility rather than reconstructing pre-DPD user data.
- **3806 — E** — The June-2008 and May-2009 dates are public product-document lower bounds, not first-shipment, invention, or JEDEC-standardization dates.
- **3807 — A/E** — Micron 2008 and Hynix 2009 share the bounded functional relation `DPD -> payload outside retention contract -> reinitialization`, but the sources do not establish identical internal voltage domains, circuitry, or command-state implementations.
- **3808 — A/E** — Case 02 magnetic core remains a functional counterexample: controlled power removal can preserve core payload while surrounding control state resets, whereas Mobile-DDR DPD explicitly withdraws the payload-retention contract; no shared genealogy is inferred.
- **3809 — X** — These vendor documents do not establish when DPD entered a JEDEC Mobile DDR/LPDDR standard or whether the feature was normative, optional, or revised there at any particular date.
- **3810 — X** — `data not retained` / `all memory data is lost` do not establish secure sanitization, an exact capacitor-decay horizon, or forensic non-recoverability.
- **3811 — X** — No claim is made that Micron or Hynix invented DPD, that June 2008 is the first product deployment, or that every configuration in either family has identical entry/exit or retention behavior.'''
append_once(str(index_path), "**3795 — X**", findings)

for p in [case_path, evidence_path, roadmap_path, index_path]:
    text = p.read_text(encoding="utf-8")
    if "\t" in text:
        raise SystemExit(f"tab found in {p}")

print(f"Case 104 DPD product chronology patch applied on expected baseline {baseline}")
