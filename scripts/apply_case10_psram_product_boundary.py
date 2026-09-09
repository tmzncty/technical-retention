from pathlib import Path

ROOT = Path('.')
EVIDENCE = ROOT / 'evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md'

EVIDENCE_TEXT = r'''# Toshiba pseudo-SRAM product self-refresh: named-product boundary (1994–2001)

**Canonical case:** [`10 — Toshiba Leakage-Tracked Self-Refresh`](../cases/10-toshiba-leakage-tracked-self-refresh.md)  
**Purpose:** test the open `named-product implementation` boundary without equating a commercial `SELF REFRESH` feature with the specific leakage-monitor trigger disclosed in Toshiba's 1984-priority patent.  
**Evidence range:** a 1994 Toshiba static-RAM data-book artifact for the `TC51832A` pseudo-static-RAM family plus Toshiba's official 18-June-2001 `TC51W3216XB` pseudo-SRAM launch announcement.

This is a retention-specific productization check, not a general history of pseudo-SRAM, not a JEDEC chronology, and not a patent-to-product genealogy.

---

## 1. Why this slice matters

Case 10 already grounds two manufacturer-primary circuit disclosures:

- Hitachi's 1982-filed / 31-March-1984-published leakage-simulation + comparator self-refresh design;
- Toshiba's 1984-priority / 1987-published self-refresh design with an oscillator, refresh-address counter, and a preferred leak-current-monitor threshold path.

Those sources establish that leakage-derived autonomous refresh was proposed. They did **not** establish that a named shipping memory part used the exact preferred circuit.

The present slice asks a narrower product question:

> Can named Toshiba pseudo-SRAM products be grounded as using autonomous self-refresh, and if so, does the product documentation establish the same leakage-tracked trigger as US4682306A?

The answer is asymmetric:

> **yes for named-product self-refresh; no for the exact leakage-tracked trigger.**

---

## 2. Source A — Toshiba 1994 Static RAM data book / `TC51832A` family

A scanned Toshiba **1994 Static RAM** data book is preserved at Bitsavers:

- <https://www.bitsavers.org/components/toshiba/_dataBook/1994_Toshiba_Static_RAM.pdf>

The indexed table of contents places `TC51832A` under **Pseudo Static RAM** and identifies a 256K, 32K×8 family. The underlying Toshiba family datasheet is also preserved through a third-party datasheet mirror:

- <https://www.alldatasheet.com/datasheet-pdf/pdf/1462395/TOSHIBA/TC51832AP.html>

### 2.1 Source-custody note

The Bitsavers artifact is a scanned manufacturer data book, but the raw PDF returned HTTP 403 to this research environment during this pass. Search indexing exposed the Toshiba title/catalog entry, and the `TC51832AP` Toshiba datasheet text was independently recoverable through the mirror. Therefore the mechanism claims below are marked **`H/P*`** rather than pretending this pass completed page-image facsimile inspection.

This is stronger than relying on an unsourced parts database, but weaker than a directly rendered manufacturer page. A future facsimile pass can close the page-anchor debt without changing the bounded conclusion unless the scan contradicts the mirrored text.

### 2.2 What the named family directly says

The preserved Toshiba datasheet identifies the `TC51832A` family as a 256K-bit high-speed CMOS **pseudo static RAM**, organized 32,768×8. Its description says the array uses a **one-transistor dynamic memory cell** with CMOS peripheral circuitry while exposing a static-RAM-like interface.

The same product text separates two refresh paths behind the `RFSH` input:

- `Auto refresh`;
- `Self refresh`.

Its feature list says:

- **Self refresh is supported by an internal timer**;
- **Auto refresh is supported by an internal refresh-address counter**;
- the family requires **256 refresh cycles / 4 ms**.

The retention-specific point is not merely that the word `self refresh` appears. The product documentation separates the recurrence source and the row-enumeration mechanism:

```text
one-transistor dynamic payload
    !=
internal refresh-address counter
    !=
internal self-refresh timer
    !=
SRAM-like external access interface
```

### 2.3 Product-family documentation floor, not first-sale chronology

The safe historical claim is:

> **By Toshiba's 1994 static-RAM data-book record, a named `TC51832A` pseudo-static-RAM family was documented with internal-timer self refresh and internal-counter auto refresh.**

This does not establish:

- first invention of pseudo-SRAM;
- first Toshiba product with self refresh;
- first sale or shipment date of `TC51832A`;
- the exact circuit underneath the phrase `internal timer`;
- compliance with a later SDRAM/JEDEC self-refresh contract.

---

## 3. Source B — Toshiba `TC51W3216XB`, 18 June 2001

Toshiba's still-live corporate press archive gives a second, cleaner manufacturer-primary product witness:

- Toshiba Corporation, **“Toshiba Announces its 32Mb Pseudo SRAM Solution,”** 18 June 2001: <https://www.global.toshiba/ww/news/corporate/2001/06/pr1802.html>

The announcement names the **`TC51W3216XB`** and explicitly describes:

- a **standard SRAM interface**;
- a **1-transistor DRAM-like memory cell**;
- a **self-refresh feature**;
- no requirement for a separate DRAM controller;
- no external glue logic normally associated with standard-DRAM refresh operation.

It also states an availability plan: sample quantities in early Q3 2001 and full production approximately two months later.

This source therefore grounds a genuine manufacturer-announced commercialization boundary:

> **Toshiba publicly marketed a named pseudo-SRAM product whose dynamic-cell payload was presented through an SRAM-like interface while self-refresh work was internalized enough to remove the separate DRAM-controller/glue-logic burden described in the announcement.**

The source still does not expose the internal timer/sensor circuit of `TC51W3216XB`.

---

## 4. Engineering reconstruction — what moved behind the interface

### 4.1 Pseudo-static interface ≠ static retention mechanism

`Pseudo static RAM` is historical product vocabulary here. The bounded `TC51832A` documentation simultaneously says the payload uses a one-transistor dynamic memory cell.

Therefore:

> **SRAM-like interface ≠ SRAM-like physical retention.**

The interface can make ordinary use more static-RAM-like while internal refresh continues to preserve a dynamic substrate.

### 4.2 Internal row enumeration ≠ internal recurrence scheduling

The `TC51832A` feature list separately names an internal refresh-address counter for Auto Refresh and an internal timer for Self Refresh. Even in a product that exposes both capabilities, these are not one state or one responsibility.

This independently reinforces the Case-09 / Case-10 decomposition:

> **where the next refresh row comes from ≠ what causes autonomous refresh work to recur.**

### 4.3 Self refresh ≠ leakage-tracked self refresh

This is the central negative result.

Toshiba US4682306A's preferred embodiment derives the start of a refresh sequence from a leak-current monitor capacitor crossing a threshold. The `TC51832A` product text available in this pass says **internal timer**. It does not mention:

- a leak-current monitor capacitor;
- a leakage-simulation capacitor pair;
- a threshold detector/comparator tied to payload-like leakage;
- refresh interval variation as measured leakage changes.

No inference from the word `timer` can fill that gap.

Therefore:

> **named-product autonomous self refresh ≠ named-product leakage-tracked self refresh.**

And:

> **commercial productization of the broad function ≠ deployment proof for the patent's preferred circuit.**

The internal timer could conceivably be influenced by environmental or process conditions in ways the short product description does not disclose, but that possibility is not evidence.

### 4.4 Hidden maintenance ≠ eliminated maintenance

Toshiba's 2001 announcement emphasizes that a separate DRAM controller and external refresh glue logic are unnecessary for its pseudo-SRAM. That is an interface/system-integration statement.

It does not mean dynamic refresh ceased to exist. The same announcement explicitly identifies self refresh and a one-transistor DRAM-like cell.

Thus:

> **external refresh burden removed ≠ refresh obligation removed.**

A product can make persistence *look* static to the surrounding system by internalizing maintenance work.

### 4.5 Self refresh ≠ nonvolatility

Neither named product source says data persists after device power removal. `Self refresh` is a powered maintenance mode for dynamic state, not evidence of intrinsic nonvolatile storage.

Therefore:

> **autonomous refresh ≠ unpowered retention.**

---

## 5. Historical record, reconstruction, analogy, interpretation

### Historical record (`H/P`, `H/P*`)

- Toshiba's 1994 static-RAM data-book artifact lists the named `TC51832A` pseudo-static-RAM family.
- The preserved Toshiba family text describes a one-transistor dynamic array, SRAM-like interface, Auto Refresh, Self Refresh, an internal self-refresh timer, and an internal auto-refresh address counter.
- Toshiba's official 18-June-2001 announcement names `TC51W3216XB`, a one-transistor DRAM-like pseudo-SRAM with SRAM interface and self refresh, and states planned sampling/full-production timing.

### Engineering reconstruction (`E`)

- SRAM-like service can be achieved while dynamic retention maintenance remains internal.
- Refresh-address enumeration and recurring self-refresh timing are distinct control relations.
- Product documentation for broad self-refresh functionality does not establish the patent's leakage-derived trigger.

### Functional analogy (`A`)

Case 21's 1999 Micron SDRAM also distinguishes externally caused refresh from an internal self-refresh regime. The bounded analogy is maintenance-responsibility internalization. The mechanisms/interfaces remain different:

```text
Toshiba TC51832A pseudo-SRAM
    SRAM-like external interface
    RFSH-selected Auto/Self Refresh
    product text names internal timer + refresh-address counter

Micron 64Mb SDR SDRAM (Case 21)
    synchronous command interface
    AUTO REFRESH is externally repeated
    SELF REFRESH is entered with refresh command encoding + CKE LOW
    exit has explicit tXSR service-recovery timing
```

This does not establish Toshiba→Micron genealogy, JEDEC descent, or identical internal circuits.

### Philosophical interpretation (`I`)

The narrow conceptual lesson is that **maintenance can disappear from the user's operational surface without disappearing from the retained state's conditions of persistence**. Internalization can make a dynamic mechanism present itself as a simpler stable service relation.

The limit is equally important: this is not evidence that all apparently passive storage hides continuous work, and it is not historical evidence that Toshiba engineers formulated a philosophy of invisible maintenance.

---

## 6. What this changes in Case 10

Before this slice, Case 10 could say only:

- leakage-derived self-refresh was disclosed in patents;
- named-product implementation of the exact circuit was open.

After this slice, the boundary is more precise:

1. **named Toshiba pseudo-SRAM product families with self refresh are grounded**;
2. a 1994 product-family document explicitly names an **internal timer** and **internal refresh-address counter**;
3. a 2001 official Toshiba product launch confirms commercial productization of dynamic-cell pseudo-SRAM with self refresh and reduced external refresh-controller burden;
4. **the exact leakage-monitor/comparator mechanism of the 1984-priority patent remains unproven in a named product**.

The old open item is therefore not `named-product self refresh?` anymore. It is:

> **named-product deployment of the specific leakage-derived/adaptive trigger, plus the broader patent→product→standards genealogy.**

---

## 7. Related-repository boundary

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `TC518512`, `TC51832`, and `pseudo SRAM` returned no dedicated treatment to reuse.

A broad history of pseudo-SRAM products, asynchronous DRAM interfaces, controller integration, standards, patents, and product generations belongs there if developed. `technical-retention` keeps only the retention-specific distinction among:

- dynamic payload;
- internal refresh-row enumeration;
- autonomous recurrence timing;
- external interface simplification;
- evidence for a specific adaptive/leakage-derived trigger.

---

## 8. Open limits

This slice does **not** close:

- direct page-image inspection and exact page anchors for the 1994 Toshiba data-book copy;
- `TC51832A` first-sale / first-shipment chronology;
- first Toshiba pseudo-SRAM with self refresh;
- transistor-level implementation of the `TC51832A` internal timer;
- proof that any named Toshiba product implemented US4682306A's preferred leak-monitor threshold circuit;
- Hitachi/Toshiba patent-to-product genealogy;
- JEDEC or pseudo-SRAM standards genealogy;
- temperature/process compensation of named-product self-refresh timing;
- production fault injection or retention testing.

Those are separate slices.

## Sources

1. Toshiba, **1994 Static RAM** data book, preserved scan: <https://www.bitsavers.org/components/toshiba/_dataBook/1994_Toshiba_Static_RAM.pdf>.
2. Toshiba Semiconductor, **TC51832A family / TC51832AP, 32,768 word × 8-bit CMOS Pseudo Static RAM**, preserved manufacturer-datasheet mirror: <https://www.alldatasheet.com/datasheet-pdf/pdf/1462395/TOSHIBA/TC51832AP.html>.
3. Toshiba Corporation, **“Toshiba Announces its 32Mb Pseudo SRAM Solution,”** 18 June 2001: <https://www.global.toshiba/ww/news/corporate/2001/06/pr1802.html>.
4. Toshiba Corp., Takayasu Sakurai and Tetsuya Iizuka, **US4682306A, “Self-refresh control circuit for dynamic semiconductor memory device”**: <https://patents.google.com/patent/US4682306A/en>.
5. Hitachi Ltd., **JPS5956291A, “MOS storage device”**, published 31 March 1984: <https://patents.google.com/patent/JPS5956291A/en>.
'''

if EVIDENCE.exists():
    raise SystemExit(f'{EVIDENCE} already exists')
EVIDENCE.write_text(EVIDENCE_TEXT.rstrip() + '\n', encoding='utf-8')

# ---- Case 10 -------------------------------------------------------------
case = ROOT / 'cases/10-toshiba-leakage-tracked-self-refresh.md'
text = case.read_text(encoding='utf-8')

anchor = "Prior-art deepening: [`../evidence/10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md`](../evidence/10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md).\n"
addition = anchor + "\nNamed-product boundary deepening: [`../evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md`](../evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md).\n"
if addition in text:
    raise SystemExit('Case 10 already contains named-product deepening link')
if anchor not in text:
    raise SystemExit('Case 10 evidence-link anchor not found')
text = text.replace(anchor, addition, 1)

scope_old = "This case asks what changes when DRAM refresh no longer depends on an external controller for refresh cadence and instead uses an on-chip monitor of charge decay to decide when an intermittent refresh pass begins. It is not a general history of DRAM self-refresh and does not identify the patent embodiment with a named Toshiba commercial product."
scope_new = "This case asks what changes when DRAM refresh no longer depends on an external controller for refresh cadence and instead uses an on-chip monitor of charge decay to decide when an intermittent refresh pass begins. It is not a general history of DRAM self-refresh. A later product-boundary deepening now grounds named Toshiba pseudo-SRAM products with autonomous self refresh, but it **still does not identify the patent's leakage-monitor embodiment with any named product**."
if scope_old not in text:
    raise SystemExit('Case 10 scope anchor not found')
text = text.replace(scope_old, scope_new, 1)

insert_anchor = "## Failure boundaries\n"
section = r'''## Named-product boundary deepening — Toshiba pseudo-SRAM, 1994–2001

The patent record leaves a product-identity question open. A later Toshiba product-documentation chain now answers only the broad half of that question.

A preserved Toshiba **1994 Static RAM** data-book artifact lists the `TC51832A` family under `Pseudo Static RAM`. The preserved Toshiba family text describes a 32K×8 pseudo-static RAM using a **one-transistor dynamic memory cell**, while exposing an SRAM-like interface. It says the `RFSH` input supports both `Auto Refresh` and `Self Refresh`; the feature list separately says **Self refresh is supported by an internal timer** and **Auto refresh is supported by an internal refresh-address counter**, with 256 refresh cycles / 4 ms. Because the raw Bitsavers PDF could not be directly rendered in this pass and the detailed text was corroborated through a manufacturer-datasheet mirror, these lines are treated as `H/P*` pending direct facsimile page anchors rather than overstated as fully inspected page evidence. See the [named-product evidence addendum](../evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md).

Toshiba's official **18 June 2001** launch announcement supplies a second manufacturer-primary product witness. It names the `TC51W3216XB`, describes a standard SRAM interface over a one-transistor DRAM-like cell, explicitly advertises self refresh, and says a separate DRAM controller / refresh glue logic is unnecessary. The same announcement gives planned sample and full-production timing.

These sources move the product boundary, but they do not collapse it into the patent mechanism:

> **named-product self refresh != named-product leakage-tracked self refresh**

The `TC51832A` product text says `internal timer`; it does not document the preferred US4682306A leak-current-monitor capacitor, threshold detector, or refresh-frequency dependence on measured leakage. A timer cannot be silently renamed a leakage monitor merely because both can start autonomous maintenance.

The stronger decomposition is now:

```text
one-transistor dynamic payload
    !=
SRAM-like service interface
    !=
refresh-row enumeration
    !=
autonomous refresh timing
    !=
leakage-derived/adaptive refresh trigger
```

This also supplies a bounded comparison to Case 21. Both Toshiba pseudo-SRAM and Micron SDRAM can internalize recurring refresh work, but their external interfaces and documented mode semantics differ. The comparison is functional, not a Toshiba→Micron or patent→JEDEC genealogy.

Finally, Toshiba's 2001 statement that a separate refresh controller/glue logic is unnecessary is an interface-placement result, not evidence that maintenance disappeared:

> **external refresh burden removed != refresh obligation removed**.

The physical payload remains dynamic in the named product descriptions, and `Self Refresh` does not establish unpowered nonvolatility.

'''
if insert_anchor not in text:
    raise SystemExit('Case 10 failure-boundary insertion anchor not found')
text = text.replace(insert_anchor, section + insert_anchor, 1)

ledger_anchor = "| A named Toshiba commercial part is proven to use this exact circuit | X | unsupported product-identity leap |"
ledger_replacement = "| A named Toshiba pseudo-SRAM family is documented with Auto Refresh and Self Refresh | H/P* | Toshiba 1994 data-book artifact + preserved `TC51832A` family text |\n| `TC51832A` Self Refresh is documented as using an internal timer while Auto Refresh uses an internal refresh-address counter | H/P* | preserved Toshiba family text; direct facsimile page anchors remain open |\n| Toshiba publicly announced a named `TC51W3216XB` pseudo-SRAM with a one-transistor DRAM-like cell, SRAM interface, and self refresh in 2001 | H/P | Toshiba corporate release, 18-Jun-2001 |\n| Named-product self refresh proves deployment of the US4682306A leak-monitor threshold path | X | product evidence does not expose the patent's monitor/threshold mechanism |\n| A named Toshiba commercial part is proven to use this exact leakage-tracked circuit | X | still unsupported; broad self-refresh productization is now grounded, exact circuit identity is not |"
if ledger_anchor not in text:
    raise SystemExit('Case 10 claim-ledger anchor not found')
text = text.replace(ledger_anchor, ledger_replacement, 1)

related_old = "A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated treatment of this Toshiba leak-monitor self-refresh mechanism. A broader history of DRAM generations, pseudo-SRAM, oscillator design, process leakage, and later standards belongs there rather than being duplicated here."
related_new = "Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for the Toshiba leak-monitor mechanism, `TC518512`, `TC51832`, and `pseudo SRAM` found no dedicated treatment to reuse. A broader history of DRAM generations, pseudo-SRAM products, oscillator/timer design, process leakage, and later standards belongs there rather than being duplicated here."
if related_old not in text:
    raise SystemExit('Case 10 related-repository anchor not found')
text = text.replace(related_old, related_new, 1)

source_anchor = "3. H. Kawamoto et al., “A 288Kb CMOS Pseudo SRAM,” _ISSCC Digest of Technical Papers_, 1984, pp. 276–277, DOI 10.1109/ISSCC.1984.1156683 — period context cited by the patent, not a central mechanism source in this case."
source_repl = "3. Toshiba, **1994 Static RAM** data book, preserved scan: <https://www.bitsavers.org/components/toshiba/_dataBook/1994_Toshiba_Static_RAM.pdf>.\n4. Toshiba Semiconductor, **TC51832A family / TC51832AP, 32,768 word × 8-bit CMOS Pseudo Static RAM**, preserved manufacturer-datasheet mirror: <https://www.alldatasheet.com/datasheet-pdf/pdf/1462395/TOSHIBA/TC51832AP.html>.\n5. Toshiba Corporation, **“Toshiba Announces its 32Mb Pseudo SRAM Solution,”** 18 June 2001: <https://www.global.toshiba/ww/news/corporate/2001/06/pr1802.html>.\n6. H. Kawamoto et al., “A 288Kb CMOS Pseudo SRAM,” _ISSCC Digest of Technical Papers_, 1984, pp. 276–277, DOI 10.1109/ISSCC.1984.1156683 — period context cited by the patent, not a central mechanism source in this case."
if source_anchor not in text:
    raise SystemExit('Case 10 source-list anchor not found')
text = text.replace(source_anchor, source_repl, 1)
case.write_text(text.rstrip() + '\n', encoding='utf-8')

# ---- ROADMAP -------------------------------------------------------------
roadmap = ROOT / 'ROADMAP.md'
road = roadmap.read_text(encoding='utf-8')
road_anchor = "- [ ] DRAM evolution and refresh machinery beyond the bounded case — **partially advanced by fourteen grounded bounded sub-slices**:"
new_road = "- [x] Case 10 named-product pseudo-SRAM self-refresh boundary deepening — [`cases/10-toshiba-leakage-tracked-self-refresh.md`](cases/10-toshiba-leakage-tracked-self-refresh.md), with new [`evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md`](evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md), now separates broad productization of autonomous self refresh from deployment of the 1984-priority patent's specific leakage-derived trigger. Toshiba's 1994 static-RAM data-book record documents the named `TC51832A` pseudo-static-RAM family as one-transistor dynamic storage with SRAM-like service, internal-counter Auto Refresh, and internal-timer Self Refresh; Toshiba's official 18-Jun-2001 `TC51W3216XB` launch independently grounds a named pseudo-SRAM product with DRAM-like cell, SRAM interface, self refresh, and reduced external refresh-controller/glue-logic burden. This closes only `named Toshiba product self-refresh exists`; exact leak-monitor/comparator product identity, direct 1994 page-image anchors, first-sale chronology, patent→product genealogy, JEDEC evolution, and fault validation remain open.\n"
if '10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md' in road:
    raise SystemExit('ROADMAP already contains Case 10 product deepening')
if road_anchor not in road:
    raise SystemExit('ROADMAP DRAM broad-item anchor not found')
road = road.replace(road_anchor, new_road + "\n" + road_anchor, 1)
roadmap.write_text(road.rstrip() + '\n', encoding='utf-8')

# ---- CASE_INDEX row + findings -----------------------------------------
index = ROOT / 'CASE_INDEX.md'
idx = index.read_text(encoding='utf-8')
rows = idx.splitlines()
matched = [i for i, line in enumerate(rows) if line.startswith('| [Toshiba Leakage-Tracked Self-Refresh:')]
if len(matched) != 1:
    raise SystemExit(f'Expected one Case 10 table row, found {len(matched)}')
i = matched[0]
old_row = rows[i]
if '10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md' in old_row:
    raise SystemExit('CASE_INDEX Case 10 row already updated')
old_tail = "[Toshiba 1984 self-refresh scheduling grounding](evidence/10-toshiba-1984-self-refresh-scheduling-grounding.md) + [Hitachi 1982–1984 prior-art deepening](evidence/10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md); pre-1982 genealogy, named-product implementation, later standards/self-refresh evolution, and modern retention-aware policy remain separate work"
new_tail = "[Toshiba 1984 self-refresh scheduling grounding](evidence/10-toshiba-1984-self-refresh-scheduling-grounding.md) + [Hitachi 1982–1984 prior-art deepening](evidence/10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md) + [1994–2001 named-product self-refresh boundary](evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md); pre-1982 genealogy, exact named-product deployment of the leakage-monitor trigger, later standards/self-refresh evolution, and modern retention-aware policy remain separate work"
if old_tail not in old_row:
    raise SystemExit('CASE_INDEX Case 10 row tail anchor not found')
rows[i] = old_row.replace(old_tail, new_tail, 1)
idx = '\n'.join(rows).rstrip() + '\n'

findings = r'''

## Case 10 deepening — Toshiba pseudo-SRAM named-product self-refresh findings

Evidence: [`evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md`](evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md)

- **2576 — 1994 manufacturer data-book presence != first-sale or invention date.** Toshiba's static-RAM catalog gives a conservative named-product documentation floor for the `TC51832A` family; it does not establish first shipment, first Toshiba pseudo-SRAM, or private conception. (`H/P*`, `X`)
- **2577 — pseudo-static interface != static physical retention.** The `TC51832A` product text combines an SRAM-like interface with a one-transistor dynamic memory cell, so service appearance and payload-retention mechanism must remain distinct. (`H/P*`, `E`)
- **2578 — one RFSH pin != one refresh relation.** The bounded product text exposes both Auto Refresh and Self Refresh through the refresh interface while assigning different internal support mechanisms to them. (`H/P*`, `E`)
- **2579 — internal refresh-address counter != internal self-refresh timer.** Row enumeration and recurring maintenance timing are separately named product functions, independently reinforcing the Case-09/Case-10 control-locus decomposition. (`H/P*`, `E`)
- **2580 — internal timer != demonstrated leakage monitor.** The product description does not identify the timer as US4682306A's leak-current-monitor capacitor/threshold path or as a refresh-frequency sensor of actual leakage. (`H/P*`, `X`)
- **2581 — named-product self refresh != named-product leakage-tracked self refresh.** Broad autonomous-maintenance productization is now grounded, while the specific adaptive/leakage-derived trigger remains an unproven product-identity claim. (`H/P*`, `E`, `X`)
- **2582 — self refresh != nonvolatility.** A dynamic-cell device that autonomously refreshes while powered has not thereby acquired unpowered retention. (`H/P*`, `E`, `X`)
- **2583 — external refresh-controller/glue-logic removal != refresh-obligation removal.** Toshiba's 2001 announcement markets simpler system integration while simultaneously describing a DRAM-like cell and self refresh; maintenance moved behind the interface rather than disappearing. (`H/P`, `E`)
- **2584 — 2001 availability plan != field-deployment validation.** Toshiba's official launch establishes a named commercial offering and stated sample/full-production schedule, not measured retention behavior in deployed systems or the internals of shipped lots. (`H/P`, `X`)
- **2585 — TC51832A and TC51W3216XB sharing Toshiba pseudo-SRAM/self-refresh vocabulary != one proven circuit genealogy.** The two product records are continuity witnesses for the product class, not evidence that they share the same timer, monitor, array, or patent embodiment. (`H/P`, `A`, `X`)
- **2586 — Toshiba pseudo-SRAM self refresh != Micron SDRAM Case-21 mode semantics.** Both internalize recurring preservation work, but SRAM-like RFSH operation and synchronous CKE/command/tXSR handoff are different interfaces and mechanisms. (`A`, `X`)
- **2587 — interface simplification can conceal maintenance without making persistence passive.** The surrounding system can lose an explicit refresh-scheduling burden while the retained dynamic payload still depends on recurring internal work. (`E`, `I`)
- **2588 — mirrored manufacturer text != completed facsimile inspection.** Because the Bitsavers 1994 PDF could not be rendered in this pass, detailed `TC51832A` claims remain marked `H/P*` pending direct page-image/page-number anchors rather than being overstated as fully inspected evidence. (`H/P*`, `X`)
- **2589 — related-repository boundary:** fresh `computing-archaeology` searches for `TC518512`, `TC51832`, and `pseudo SRAM` returned no dedicated case to reuse; broad pseudo-SRAM product/standards history belongs there if developed, while Case 10 keeps the retention-specific productization-versus-trigger-identity distinction. (`H/P` project-state record)
'''
if '**2576 —' in idx or '**2589 —' in idx:
    raise SystemExit('CASE_INDEX already contains new finding range')
idx = idx.rstrip() + findings.rstrip() + '\n'
index.write_text(idx, encoding='utf-8')

# ---- Validation ----------------------------------------------------------
for p in (EVIDENCE, case, roadmap, index):
    if not p.exists():
        raise SystemExit(f'missing expected file {p}')

case2 = case.read_text(encoding='utf-8')
assert 'named-product self refresh != named-product leakage-tracked self refresh' in case2
assert '10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md' in case2
road2 = roadmap.read_text(encoding='utf-8')
assert road2.count('10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md') == 1
idx2 = index.read_text(encoding='utf-8')
for n in range(2576, 2590):
    marker = f'**{n} —'
    if idx2.count(marker) != 1:
        raise SystemExit(f'finding {n} count is {idx2.count(marker)}')
if idx2.count('10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md') < 2:
    raise SystemExit('CASE_INDEX navigation/evidence link missing')

print('Case 10 pseudo-SRAM named-product boundary applied successfully')
