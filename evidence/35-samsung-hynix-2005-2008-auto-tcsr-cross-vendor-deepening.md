# Case 35 Deepening — Samsung / Hynix 2005–2008 Automatic TCSR as Cross-Vendor Product Semantics

## Status

**`bounded deepening complete`** for one narrow question left open by Case 35:

> Was Micron's documented combination of automatic on-device temperature-conditioned self refresh and separately programmable partial-array retention merely a Micron-local product idiom, or can closely related semantics be grounded in contemporary product documents from other DRAM vendors?

This record adds a bounded **cross-vendor product-document comparison** using Samsung Mobile-DDR material from 2005–2006 and Hynix Mobile DDR material from 2008.

It does **not** establish:

- a complete JEDEC revision-by-revision genealogy of TCSR or PASR;
- invention priority for Samsung, Hynix, Micron, or any other vendor;
- identical internal sensor, oscillator, controller, or array circuitry across vendors;
- that a preliminary product specification proves volume shipment;
- that similar interface semantics prove direct technology transfer;
- that every Mobile DDR / LPDDR generation behaves this way;
- that `AUTO TCSR`, `Internal TCSR`, and Micron's product-specific TCSR wording are perfectly interchangeable historical terms.

Case: [`../cases/35-micron-mobile-ddr-automatic-tcsr.md`](../cases/35-micron-mobile-ddr-automatic-tcsr.md)

Primary grounding record for the original Micron case: [`35-micron-2005-2008-mobile-ddr-tcsr-grounding.md`](35-micron-2005-2008-mobile-ddr-tcsr-grounding.md)

---

## 1. Why this slice matters

The original Case 35 already established a strong Micron product-level counterexample to a common interface assumption:

```text
TCSR-labelled register field exists
    !=
software actually controls refresh cadence
```

Micron's 512Mb Mobile SDRAM Rev. J 2/08 says an on-die temperature sensor is used instead of effective host TCSR programming; programming the displayed TCSR bits has no effect, while PASR remains separately controller-selectable.

A remaining historical question was whether this should be treated as a Micron-specific implementation choice or as part of a broader contemporary Mobile-DDR design pattern.

Samsung and Hynix product documents provide a useful bounded answer. They show that, by the mid-2000s, other vendors also documented:

- automatic temperature-conditioned self-refresh behavior inside the DRAM;
- on-device temperature sensing or control logic;
- no need for an external TCSR programming action for the automatic path;
- separately selectable PASR coverage.

The conclusion is intentionally limited to **cross-vendor product semantics**. It is not upgraded into a normative standards claim.

---

## 2. Samsung K4X51323PC, Rev. 0.6, October 2005

### 2.1 Document identity and revision boundary

Samsung's manufacturer document is titled:

- `16M x32 Mobile-DDR SDRAM`;
- device family `K4X51323PC-7(8)E/G`;
- `Revision 0.6`;
- `October 2005`;
- status marked `Preliminary`.

The preserved revision-history page records:

- Rev. 0.0 — first target specification, draft date **October 27, 2004**;
- Rev. 0.2 — preliminary datasheet, **December 20, 2004**;
- Rev. 0.6 — among other changes, defines maximum burst refresh cycle, **October 18, 2005**.

**Evidence boundary:** the currently inspected Rev. 0.6 document contains the TCSR semantics described below. The revision table alone does **not** prove that the same TCSR wording was already present in Rev. 0.0 in October 2004. The earlier revision date is therefore document lineage, not an earlier TCSR-publication date.

Public archival HTML transcription of the Samsung-branded revision-history page:

- <https://www.alldatasheet.com/html-pdf/168597/SAMSUNG/K4X51323PC-7E/606/2/K4X51323PC-7E.html>

The feature page identifies the device as Mobile-DDR SDRAM and explicitly lists:

- `Partial Self Refresh Type ( Full, 1/2, 1/4 Array )`;
- `Internal Temperature Compensated Self Refresh`;
- `Deep Power Down Mode`;
- an ordinary auto-refresh duty-cycle statement for the product's specified temperature range.

Archival HTML transcription of the feature page:

- <https://www.alldatasheet.com/html-pdf/168597/SAMSUNG/K4X51323PC-7E/912/3/K4X51323PC-7E.html>

The source chain is a **manufacturer document preserved by a public datasheet mirror**, not a current samsung.com download. Claims in this record are tied to identifiable Samsung document text, revision markers, device names, and page content rather than distributor prose.

### 2.2 Internal TCSR is automatic

The Rev. 0.6 TCSR section is unusually explicit. Under `Internal Temperature Compensated Self Refresh (TCSR)`, Samsung states that Mobile DDR SDRAM includes:

- an **internal temperature sensor**;
- control units;
- automatic control of the self-refresh cycle according to temperature ranges around 45 °C and 85 °C;
- a stated sensor tolerance of ±5 °C.

Public archival transcription of the TCSR/PASR page:

- <https://datasheet4u.com/pdf-down/K/4/X/K4X51323PC-7E_Samsungsemiconductor.pdf> — mirrored Samsung document, page 11 in Rev. 0.6 text as indexed by the archive.

The important retention relation is not the precise threshold number. It is the locus of authority:

```text
device temperature observation
    -> on-device control logic
    -> self-refresh-cycle selection
```

This is direct historical product-document evidence. It does not require reconstructing an undocumented host algorithm.

### 2.3 External TCSR programming is explicitly ignored

The same Samsung section says that if the controller issues the EMRS code for **external TCSR**, that TCSR code is **ignored**.

This creates a strong product-interface boundary independently of the Micron document:

```text
interface vocabulary can name an external TCSR path
    !=
that path has effective cadence authority on this device
```

And more specifically:

```text
external TCSR command issued
    !=
automatic TCSR authority transferred to the controller
```

The direct historical statement is Samsung's `ignored` behavior. The phrase `cadence authority` is project reconstruction vocabulary.

### 2.4 PASR remains a separate coverage mechanism

On the same page, Samsung documents PASR as a separate feature with three self-refresh coverage choices:

- full array;
- half array;
- quarter array.

The accompanying diagrams identify which bank-address regions remain inside the `Partial Self Refresh Area`.

That co-location is analytically useful because the device can simultaneously expose:

```text
AUTO TCSR
    -> decide how self-refresh cadence changes with temperature

PASR
    -> decide how much of the array receives self-refresh maintenance
```

Therefore:

> **temperature-conditioned cadence control != retained-array coverage control**.

The two controls occur in one manufacturer product specification but answer different retention questions.

### 2.5 Preliminary product specification is not shipment proof

The Rev. 0.6 document is explicitly `Preliminary`.

Safe historical wording is:

> In an October 2005 preliminary specification for the K4X51323PC family, Samsung documented Internal TCSR using an internal sensor/control path, ignored external-TCSR EMRS semantics, and separately selectable PASR coverage.

Unsafe wording would be:

> Samsung was definitely shipping this exact Rev. 0.6 implementation at volume in October 2005.

This record does not make the latter claim.

---

## 3. Samsung K4X51163PC, February 2006: same semantic pattern in another named family

A February 2006 Samsung datasheet for the `K4X51163PC-L(F)E/G`, a `32M x16 Mobile-DDR SDRAM`, independently preserves the same product-level pattern.

Its feature list includes:

- Internal Temperature Compensated Self Refresh;
- PASR with full / half / quarter-array choices;
- Deep Power Down Mode.

The TCSR page states that:

- the device contains an internal temperature sensor and control units;
- the self-refresh cycle is controlled automatically according to temperature ranges;
- an external TCSR EMRS code issued by the controller is ignored;
- PASR remains separately selectable.

Archival HTML/text sources:

- overview / feature metadata: <https://www.alldatasheet.com/datasheet-pdf/pdf/146538/SAMSUNG/K4X51163PC.html>
- page-9 HTML transcription containing the TCSR/PASR text: <https://www.alldatasheet.co.kr/html-pdf/146538/SAMSUNG/K4X51163PC/2721/9/K4X51163PC.html>

This second family matters because it reduces the risk of treating the Rev. 0.6 K4X51323PC wording as a one-document anomaly.

The safe bounded conclusion is still only:

> Samsung documented the same broad automatic-TCSR / separate-PASR semantics in more than one named Mobile-DDR family across late 2005 and early 2006 documentation.

It does not prove identical die implementation or identical sensor calibration between the two families.

---

## 4. Hynix H5MS5122DFR / H5MS5132DFR, Rev. 1.2, July 2008

### 4.1 Product-level low-power feature vocabulary

Hynix's Rev. 1.2 July 2008 Mobile DDR SDRAM documentation for the `H5MS5122DFR Series / H5MS5132DFR Series` lists:

- `PASR (Partial Array Self Refresh)`;
- `AUTO TCSR (Temperature Compensated Self Refresh)`;
- optional `DPD (Deep Power Down)`.

The same document describes the Mobile DDR as providing programmable self-refresh options including PASR and TCSR.

Public archival transcription of the Hynix document:

- <https://dtsheet.com/doc/642277/hynix-h5ms5132dfr>

### 4.2 Internal sensor; no external EMRS required

Hynix states that the series has `Auto TCSR` to reduce self-refresh current consumption and explains that, because an **internal temperature sensor** is implemented, the device can automatically adjust refresh rate according to temperature **without external EMRS command**.

This is not textually identical to Samsung's stronger `external TCSR code is ignored` statement.

The distinction matters:

```text
Samsung 2005/2006 bounded wording
    external TCSR EMRS code is ignored

Hynix 2008 bounded wording
    Auto TCSR adjusts refresh rate without external EMRS command
```

Both support an automatic on-device path. Only the Samsung source set directly supports the stronger claim about an issued external TCSR code being ignored.

### 4.3 Self-refresh authority and PASR remain separately described

The Hynix document separately explains that:

- SELF REFRESH retains data without external clocking and schedules refresh internally;
- Auto TCSR lets the Mobile DDR control refresh rate according to temperature;
- PASR selects the memory array to be refreshed;
- both mechanisms can reduce self-refresh current for different reasons.

This is a particularly clean manufacturer statement of the distinction already reconstructed in Case 35:

```text
self-refresh authority
    !=
temperature-conditioned cadence
    !=
retained-array coverage
```

Hynix does not need to use those project terms for the distinction to be visible in the product behavior it documents.

---

## 5. Cross-vendor historical result

The bounded chronology now looks like this:

```text
Samsung K4X51323PC Rev. 0.6 — October 2005
    Internal TCSR
    internal temperature sensor + control units
    automatic self-refresh-cycle control
    external TCSR EMRS code ignored
    PASR separately selects full / 1/2 / 1/4 array

Samsung K4X51163PC — February 2006
    same broad automatic-TCSR / ignored-external-TCSR pattern
    PASR separately selects full / 1/2 / 1/4 array

Micron 512Mb Mobile SDRAM Rev. J — February 2008
    on-die temperature sensor automatically controls self-refresh oscillator
    displayed TCSR bits have no effect on that product version
    PASR remains separately programmable

Hynix H5MS5122DFR / H5MS5132DFR Rev. 1.2 — July 2008
    Auto TCSR with internal temperature sensor
    automatic refresh-rate adjustment without external EMRS command
    PASR separately selects retained array coverage
```

This supports a cross-vendor product-level conclusion:

> By 2005–2008, multiple Mobile-DDR vendors documented designs in which temperature-conditioned self-refresh cadence could be internalized in the DRAM while PASR remained a separate mechanism for choosing retained array scope.

A second bounded conclusion is also supported:

> Host-visible or historically inherited TCSR interface vocabulary did not necessarily mean that the host retained effective cadence authority on a particular product version.

For Samsung, the external TCSR code is explicitly ignored. For Micron, the displayed/programmed TCSR bits are explicitly documented as having no effect on the bounded product version. Hynix independently documents automatic operation without an external EMRS command.

---

## 6. What the cross-vendor convergence does *not* prove

### 6.1 Similar product semantics do not establish standards genealogy

Samsung, Micron, and Hynix all operated in the same Mobile-DDR ecosystem and their documents use overlapping historical vocabulary.

That is not enough to infer:

```text
same broad behavior
    -> same normative clause
    -> same revision date
    -> same implementation requirement
```

A complete standards-history claim still requires direct inspection of the relevant JEDEC documents and, ideally, revision/change history.

### 6.2 Similar semantics do not establish direct technical lineage

The evidence does not show that:

- Samsung copied Micron;
- Micron copied Samsung;
- Hynix copied either;
- one vendor licensed a specific TCSR circuit from another;
- all three used the same sensor topology or oscillator control law.

The safe statement is **contemporary cross-vendor semantic convergence**, not a technology-transfer genealogy.

### 6.3 Internal temperature sensing is still only a proxy for retention need

The product documents describe temperature-conditioned refresh-rate control. They do not say that each row's exact remaining retention margin is measured.

Therefore:

```text
on-die temperature sensor
    !=
per-row retention-time measurement
```

And:

```text
automatic refresh-rate adjustment
    !=
modern retention-time profiling
```

### 6.4 Automatic cadence does not determine retention scope

Samsung, Micron, and Hynix all separately discuss PASR.

That separation blocks another flattening:

```text
correct automatic cadence
    !=
whole-array preservation
```

If policy excludes part of the array from PASR coverage, a correctly functioning automatic temperature path does not restore an entitlement that the coverage policy deliberately withdrew.

---

## 7. Retained-state decomposition

The expanded cross-vendor record supports the following project reconstruction:

```text
charge-dependent array payload
    !=
self-refresh mode / recurring-maintenance authority
    !=
temperature observation
    !=
temperature-to-cadence policy
    !=
effective cadence-control locus
    !=
PASR coverage selection
    !=
external interface fields or commands
```

The last distinction is especially important.

A product can preserve a field name or command vocabulary while assigning actual cadence authority elsewhere:

```text
external TCSR vocabulary survives
    + internal automatic sensor path exists
    -> external field/command can become ineffective or unnecessary
```

This is an **engineering reconstruction** of the documented interface relation, not a historical term used by the vendors.

---

## 8. Failure and interpretation boundaries

The source set supports several bounded failure/interpretation distinctions:

1. **Host software can mis-model authority.** If software assumes every TCSR-labelled field or EMRS code controls cadence, it can be wrong for Samsung's and Micron's bounded products.
2. **Cadence and coverage can fail independently.** Correct automatic TCSR does not compensate for a PASR policy that excludes needed data.
3. **Temperature is not a complete retention oracle.** The source documents do not cover every sensor fault, thermal gradient, calibration error, or per-cell variation.
4. **A preliminary document is not shipment evidence.** Samsung Rev. 0.6 is useful historical product-specification evidence without being promoted into a volume-shipment claim.
5. **A mirrored primary document has a chain-of-custody limit.** The preserved files identify Samsung/Hynix document families, revisions, and manufacturer text, but the current retrieval path is an archival datasheet mirror rather than the vendors' present support sites.

---

## 9. Historical record vs engineering reconstruction vs analogy vs interpretation

### Historical record

Directly documented manufacturer-level facts include:

- Samsung Rev. 0.6 October 2005 product-specification identity and revision history;
- Samsung's Internal TCSR wording, internal temperature sensor/control units, ignored external TCSR EMRS code, and separate PASR modes;
- the February 2006 K4X51163PC repetition of the same broad TCSR/PASR pattern;
- Hynix Rev. 1.2 July 2008 Auto TCSR, internal sensor, automatic refresh-rate adjustment without external EMRS, PASR, and self-refresh behavior;
- the Micron facts already grounded by the original Case 35 record.

### Engineering reconstruction

Project terms introduced to compare these records include:

- `cadence authority`;
- `coverage authority`;
- `effective control locus`;
- `interface vocabulary != effective authority`;
- `temperature observation != per-row retention margin`.

These are analytical labels, not quotations from Samsung, Micron, Hynix, or JEDEC.

### Functional analogy

A bounded analogy may compare this interface pattern with other systems where a legacy-visible control surface remains present while an automatic internal policy has become authoritative.

The analogy is only about **control-locus mismatch**. It does not imply architectural lineage between DRAM and unrelated systems.

### Philosophical interpretation

A narrow conceptual pressure follows:

> A system may preserve the visible language of external control even after the operative responsibility for maintaining state has moved inward.

That is a philosophical/interpretive statement prompted by the engineering record. It is not a claim about vendor intent or historical self-understanding.

---

## 10. Cross-case comparison

This deepening strengthens, but does not merge, several existing cases:

```text
Case 21
    AUTO REFRESH / SELF REFRESH
    -> recurring-maintenance responsibility can cross the package boundary

Case 34
    temperature-dependent DRAM refresh
    -> measured environment can influence maintenance cadence

Case 35
    commercial Mobile DDR Auto TCSR + PASR
    -> cadence can be internally temperature-conditioned
    -> coverage can remain separately policy-selected
    -> interface field presence does not guarantee host authority

Case 104 / 105 / 139
    LPDDR selective/per-bank refresh cases
    -> maintenance target scope and accounting remain distinct questions
```

The new Samsung/Hynix evidence does not convert these into one historical lineage. It only sharpens the common retention decomposition.

---

## 11. Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Samsung K4X51323PC Rev. 0.6 is an October 2005 preliminary Mobile-DDR specification | H/P | direct Samsung document identity/revision page via archival mirror |
| Rev. 0.0 of that document family is dated October 27, 2004 | H/P | direct revision-history table |
| The inspected Rev. 0.6 proves TCSR wording was already present in Rev. 0.0 | X | not established; earlier revision content not inspected |
| Samsung Rev. 0.6 documents Internal TCSR with internal temperature sensor/control units | H/P | direct Samsung TCSR section via archival mirror |
| Samsung says external TCSR EMRS code is ignored | H/P | direct negative interface statement |
| Samsung separately documents full / half / quarter-array PASR | H/P | direct PASR section |
| Samsung's February 2006 K4X51163PC document repeats the same broad automatic-TCSR / PASR pattern | H/P | direct named-family datasheet text via archival mirror |
| Hynix Rev. 1.2 July 2008 documents Auto TCSR using an internal temperature sensor | H/P | direct Hynix manufacturer-document text via archival mirror |
| Hynix says Auto TCSR can adjust refresh rate without external EMRS command | H/P | direct mechanism/interface statement |
| Hynix's wording proves an issued external TCSR EMRS command is ignored exactly as in Samsung | X | not established; Hynix wording is weaker/different |
| Similar Samsung/Micron/Hynix behavior proves a specific JEDEC revision mandated identical implementation | X | standard text not inspected in this slice |
| Similar behavior proves direct inter-vendor technical transfer | X | no genealogy evidence |
| Internal temperature sensing is equivalent to per-row retention profiling | X | not the documented mechanism |
| Cross-vendor product documents support separating cadence authority from PASR coverage authority | I | engineering reconstruction grounded in independent manufacturer records |

---

## 12. Related-repository check

Current GitHub code search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `temperature compensated self refresh` returned no dedicated technical-history case to reuse.

A comprehensive Mobile-DDR / LPDDR standards and vendor genealogy should therefore still be routed to that companion repository if developed broadly. This evidence file intentionally keeps only the retention-specific comparison:

- where temperature-conditioned cadence control resides;
- whether external controls remain effective;
- how PASR coverage remains separate from cadence.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) remains relevant methodologically: historical vocabulary (`Internal TCSR`, `AUTO TCSR`, `PASR`) is preserved, while `cadence authority` and `coverage authority` remain clearly marked modern reconstruction terms.

---

## 13. Remaining gaps

This bounded slice does not close:

- direct JEDEC revision-by-revision TCSR/PASR clause history;
- ballot/proposal genealogy for internal versus external TCSR;
- vendor-to-vendor implementation or licensing genealogy;
- direct shipment evidence for Samsung's October 2005 preliminary Rev. 0.6 part;
- sensor topology, calibration circuit, oscillator law, and thermal-gradient qualification;
- exact DPD control-state survival semantics across these vendors;
- later LPDDR MR4 thermal-update / refresh-rate handoff history;
- per-row retention-time profiling or RowHammer-oriented refresh policy.

Those remain separate slices.

---

## Sources

1. Samsung Electronics, `K4X51323PC-7(8)E/G`, **16M x32 Mobile-DDR SDRAM**, Rev. 0.6, October 2005, preliminary. Archival HTML transcription of revision history: <https://www.alldatasheet.com/html-pdf/168597/SAMSUNG/K4X51323PC-7E/606/2/K4X51323PC-7E.html>.
2. Samsung Electronics, same Rev. 0.6 document, feature page: <https://www.alldatasheet.com/html-pdf/168597/SAMSUNG/K4X51323PC-7E/912/3/K4X51323PC-7E.html>.
3. Samsung Electronics, same Rev. 0.6 document, TCSR/PASR content preserved in the mirrored document indexed here: <https://datasheet4u.com/pdf-down/K/4/X/K4X51323PC-7E_Samsungsemiconductor.pdf>.
4. Samsung Electronics, `K4X51163PC-L(F)E/G`, **32M x16 Mobile-DDR SDRAM**, February 2006; archival product-document overview: <https://www.alldatasheet.com/datasheet-pdf/pdf/146538/SAMSUNG/K4X51163PC.html>.
5. Samsung Electronics, same K4X51163PC document, page-9 archival HTML transcription containing Internal TCSR and PASR semantics: <https://www.alldatasheet.co.kr/html-pdf/146538/SAMSUNG/K4X51163PC/2721/9/K4X51163PC.html>.
6. Hynix Semiconductor, `H5MS5122DFR Series / H5MS5132DFR Series`, **Mobile DDR SDRAM 512Mbit (16M x 32bit)**, Rev. 1.2, July 2008; public archival transcription: <https://dtsheet.com/doc/642277/hynix-h5ms5132dfr>.
7. Micron comparison source: [`35-micron-2005-2008-mobile-ddr-tcsr-grounding.md`](35-micron-2005-2008-mobile-ddr-tcsr-grounding.md).
