from pathlib import Path

ROOT = Path('.')


def replace_once(path, old, new):
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected marker once, found {count}: {old[:120]!r}')
    p.write_text(text.replace(old, new, 1).rstrip() + '\n', encoding='utf-8')


def append_once(path, marker, block):
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    if marker in text:
        raise SystemExit(f'{path}: marker already present: {marker}')
    p.write_text(text.rstrip() + '\n\n' + block.strip() + '\n', encoding='utf-8')


addendum = r'''# Case 132 deepening — Cypress/Infineon temperature-conditioned Flash retention contracts, 2014–2018

This evidence addendum deepens [`../cases/132-cryogenic-serial-flash-retention-operability.md`](../cases/132-cryogenic-serial-flash-retention-operability.md).

**Bounded question:** the 2015 cryogenic experiment shows that an already-written serial-Flash pattern can remain recoverable through a cold-store -> warm-verify procedure while very-low-temperature program/erase operation becomes slow or unavailable. What public manufacturer evidence, available around the same period, shows about the *other* side of the environmental relation: elevated temperature and prior cycling as conditions on retention lifetime?

This addendum does **not** identify the anonymous commercial ICs in the 2015 experiment with any Cypress product. It also does not derive a raw-cell Arrhenius law from product specifications. Its contribution is narrower: it grounds a temperature-conditioned **retention contract / qualification** boundary that prevents `operating temperature`, `storage temperature`, and `retention lifetime` from being collapsed into one number.

---

## Source A — Cypress PSoC 3 CY8C34 Automotive Family Datasheet, Rev. *G, 14 February 2014

**Document:** Cypress Semiconductor, *PSoC 3: CY8C34 Automotive Family Datasheet*, Document 001-57331 Rev. *G, revised 14 February 2014.

**Preserved first-party hosting:** <https://www.infineon.com/dgdl/Infineon-PSoC_3_CY8C34_Automotive_Family_Datasheet_Programmable_System-on-Chip_%28PSoC%29_Datasheet-AdditionalTechnicalInformation-v08_00-EN.pdf?fileId=8ac78c8c7d0d8da4017d0ecabcb643c4>

**Evidence class:** `H/P` — manufacturer datasheet, preserved on Infineon's current site after the Cypress acquisition.

### A1. Active-operation envelope and retention qualification are stated separately

Section 11.7 says the memory specifications are generally valid over `-40 °C <= TA <= 125 °C` unless otherwise noted. The Flash timing table separately gives block write, erase, and program timing over temperature ranges extending to `TA <= 125 °C` / `TJ <= 140 °C`.

The same table then gives **retention-specific exceptions** rather than one lifetime valid everywhere:

- after **100 K erase/program cycles**, minimum Flash retention is **20 years** at average ambient `TA <= 55 °C`;
- after the same **100 K erase/program cycles**, the listed minimum is **10 years** at average ambient `TA <= 85 °C`;
- note 53 says Cypress provides a retention calculator based on an application's individual temperature profile across the broader `-40 °C` to `+125 °C` ambient range.

This is unusually useful for the repository because cycle count can be held fixed while the published retention interval changes with average temperature.

**Grounded boundary:** `active-operation temperature range != one temperature-independent retention lifetime`.

### A2. Retention is dated from a state-changing event, not from manufacture

The table defines the Flash retention period as measured from the **last erase cycle**. That is a service-history relation, not device age from fabrication and not powered uptime.

**Grounded boundary:** `retention clock origin != device manufacturing date != controller power-on time`.

### A3. A temperature profile is stronger than a single maximum-temperature label

The datasheet's retention-calculator note refers to customers' individual temperature profiles. The historical product contract therefore already treats environmental exposure as a time-varying history rather than reducing retention to a single product-grade label.

**Engineering reconstruction:** a retention guarantee can depend on an accumulated environmental/use history even when the logical payload and address remain unchanged.

---

## Source B — Cypress KBA203737, 15 October 2015

**Document:** Cypress/Infineon Knowledge Base, “How long will data be retained in Cypress Flash memory devices if only a few erase cycles are planned?”, KBA203737, dated 15 October 2015.

**Current institutional record:** <https://community.infineon.com/t5/Knowledge-Base-Articles/How-long-will-data-be-retained-in-Cypress-Flash-memory-devices-if-only-a-few/ta-p/249710>

**Evidence class:** `H/P*` — manufacturer institutional guidance contemporaneous with Case 132's publication year, but not a product-specific datasheet or standards text. It cites Cypress application note AN98549.

The KBA says that with very few erase cycles, typical retention can be expected around the long end of the product guidance, but it immediately qualifies that answer by storage temperature: below about `55 °C` may not create the same issue, whereas higher temperatures over extended periods require calculation to ensure the desired longevity.

The safe use here is not the wording `20 years for all Cypress Flash`. It is the relationship the vendor explicitly foregrounds:

> low cycling burden does not make retention independent of temperature history.

**Grounded boundary:** `few P/E cycles != temperature-independent shelf life`.

---

## Source C — S25FL1-K serial Flash datasheet continuity

**Document:** Cypress Semiconductor, *S25FL116K/S25FL132K/S25FL164K, 3.0 V SPI Flash Memory*, Document 002-00497. The current Infineon-hosted legacy PDF is Rev. *I, revised 4 July 2018; its revision history records that the Data Retention section was added in Rev. *E on 29 June 2016.

**First-party preserved PDF:** <https://www.infineon.com/assets/row/public/documents/10/49/infineon-s25fl116k-s25fl132k-s25fl164k-16-mbit-2-mbyte-32-mbit-4-mbyte-64-mbit-8-mbyte-3.0-v-spi-flash-memory-datasheet-en.pdf?fileId=8ac78c8c7d0d8da4017d0ed4ebee537f>

**Evidence class:** `H/P` for the named product specification and revision history; later than the 2015 cryogenic paper and therefore used only as same-vendor serial-Flash continuity, not as evidence about the anonymous tested batches.

The Data Integrity table lists:

- `10K Program/Erase Cycles -> 20 Years` minimum retention;
- `100K Program/Erase Cycles -> 2 Years` minimum retention.

The same product family separately exposes Industrial / Industrial Plus operating grades up to `+85 °C` / `+105 °C`. The retention table itself does **not** print a temperature qualifier next to those two rows. Therefore this document alone must **not** be paraphrased as `20 years at +105 °C`.

A later Infineon NOR-Flash FAQ makes the vendor's interpretation explicit: the 10K/100K retention examples assume about **55 °C average field temperature**, and retention after cycling depends on field temperature, P/E count, and cycling interval.

**Later institutional continuity:** <https://community.infineon.com/t5/Knowledge-Base-Articles/NOR-Flash-FAQs/ta-p/255345>

**Grounded boundary:** `product operating-grade ceiling != implied retention-test temperature`.

---

## Evidence decomposition

The sources require at least four separate environmental/use variables:

```text
current operating temperature
    -> can the device execute read/program/erase within its active specification?

average / time-profiled retention temperature
    -> how long is the post-write/post-erase state qualified to remain recoverable?

prior P/E cycling
    -> how much endurance history precedes the retention interval?

cycling interval / annealing history
    -> what temporal pattern produced that wear state?
```

Only the first variable is an instantaneous command-environment question. The others can encode a history that matters after active writes stop.

---

## Engineering reconstruction

### E1. Operating-temperature admissibility != retention-duration qualification

A device can be specified to operate at a temperature at which the guaranteed retention interval, after a given cycling history, is shorter than at a lower average temperature. `The command is supported here` is therefore weaker than `the written state is guaranteed for N years here`.

### E2. Retention lifetime is history-conditioned

For the bounded Cypress evidence, retention cannot be reconstructed from `nonvolatile` alone. At minimum it is conditioned by temperature history and P/E history, and vendor guidance also calls out cycling interval.

### E3. Case 132's cryogenic result is not an acceleration model

The 2015 cryogenic paper reports zero observed bit errors at four warm verification points over 24 months for one finite experiment. The Cypress high-temperature qualification evidence independently shows temperature-conditioned retention contracts, but the two do not supply a measured common activation energy or a quantitative cold-vs-hot lifetime ratio.

Therefore:

`cryogenic no-error observation != measured Arrhenius acceleration coefficient`.

### E4. `Colder` is not one monotonic system-level quality axis

Case 132 already shows very low temperature worsening program/erase service. The elevated-temperature product evidence shows that hotter average exposure can shorten qualified retention. These can coexist because **operation margin** and **retention lifetime** are different relations.

This does not justify a universal optimum temperature or a claim that every Flash mechanism has the same temperature dependence.

---

## Historical / mechanism boundaries

- PSoC 3 embedded Flash is **not** the same product/process as the anonymous serial-Flash batches in Ihmig et al. 2015.
- Cypress's 2015 KBA is manufacturer guidance, not a JEDEC normative standard or direct raw-cell experiment.
- The later S25FL1-K / Infineon FAQ continuity does not retroactively prove that the anonymous 2015 samples used the same retention model.
- Product qualification numbers do not expose a complete trap/charge-loss distribution or a universal activation energy.
- The sequence `2014 datasheet -> 2015 cryogenic paper -> 2016/2018 serial-Flash datasheet` is a source chronology, **not a proven engineering genealogy** among products or authors.

---

## Cross-case controls

### Case 76 — JESD218 SSD qualification

Case 76 already shows that SSD endurance and power-off retention are application-class/workload/temperature-qualified service contracts. This addendum remains below that level: it shows a manufacturer Flash/embedded-memory contract in which environmental history and cycling condition the retained state.

Safe comparison: `retention lifetime is qualified by use/environment history`.

Rejected identity: `PSoC/serial-NOR product table == JESD218 SSD contract`.

### Cases 03 / 127 — DRAM

DRAM cooling and Flash temperature-conditioned retention can be compared only as environment-sensitive recoverability. DRAM's volatile charge restoration/remanence regime is not Flash's nonvolatile post-cycling retention regime.

### Cases 36 / 52 / 59 / 67 — Flash maintenance/disturbance

Those cases show retention debt from age, reads, programming interference, and controller policy. This addendum adds **environmental/use-history qualification**, not a new refresh/reclaim mechanism.

---

## Readiness assessment

This slice closes the bounded roadmap item **“elevated-temperature comparison” at the vendor qualification/contract layer**:

- direct 2014 manufacturer datasheet with fixed-cycle-count, temperature-conditioned retention numbers;
- a contemporaneous 2015 manufacturer KBA explicitly warning that higher-temperature exposure requires longevity calculation;
- later named serial-Flash product continuity with explicit P/E-conditioned retention and a separate operating-temperature range;
- explicit anti-overclaim boundaries against product identity, raw-cell kinetics, and genealogy.

It does **not** close direct Flash/EEPROM charge-loss kinetics, activation-energy measurement, accelerated bake methodology, independent replication, or controlled fault injection. Those remain open.
'''

add_path = ROOT / 'evidence/132-2014-2018-temperature-conditioned-retention-contract-deepening.md'
if add_path.exists():
    raise SystemExit(f'{add_path} already exists')
add_path.write_text(addendum.rstrip() + '\n', encoding='utf-8')

# Case 132: add navigation, historical section, engineering boundaries, claim-ledger rows, and sources.
replace_once(
    'cases/132-cryogenic-serial-flash-retention-operability.md',
    'Grounding record: [`../evidence/132-2015-cryogenic-serial-flash-grounding.md`](../evidence/132-2015-cryogenic-serial-flash-grounding.md).',
    'Grounding record: [`../evidence/132-2015-cryogenic-serial-flash-grounding.md`](../evidence/132-2015-cryogenic-serial-flash-grounding.md).\n\nTemperature-conditioned qualification deepening: [`../evidence/132-2014-2018-temperature-conditioned-retention-contract-deepening.md`](../evidence/132-2014-2018-temperature-conditioned-retention-contract-deepening.md). This later/deeper evidence is a bounded comparison, not an identification of the anonymous cryogenic-test ICs with Cypress products.'
)

case_hist_marker = 'A historical product family can preserve its ordinary interface identity while the physical margin underneath that interface changes across production revisions.\n\n---\n\n## Retained state and substrate'
case_hist_block = '''A historical product family can preserve its ordinary interface identity while the physical margin underneath that interface changes across production revisions.

### H/P — elevated-temperature qualification is a separate retention relation

A 14-February-2014 Cypress PSoC 3 CY8C34 Automotive datasheet provides a useful pre-publication counterweight to the cryogenic experiment. Its Flash write/erase/program timing is specified over an active range extending to `TA <= 125 °C`, while retention is separately qualified by **average ambient temperature and prior cycling**: after 100 K erase/program cycles the table gives 20 years at `TA <= 55 °C` but 10 years at `TA <= 85 °C`. The same datasheet says the retention period is measured from the last erase cycle and offers a calculator based on an application's temperature profile.

Cypress KBA203737, dated 15 October 2015, independently tells users that low erase counts do not remove temperature dependence: extended higher-temperature storage requires a longevity calculation. Later S25FL1-K serial-Flash documentation preserves the same separation between P/E-conditioned retention and a broader active operating-temperature grade.

These are not evidence about the identity or process of the 2015 paper's anonymous samples. They establish a **vendor qualification boundary**:

> **operating-temperature support != a uniform retention guarantee over that entire operating range.**

Detailed evidence and provenance are kept in the temperature-conditioned addendum.

---

## Retained state and substrate'''
replace_once('cases/132-cryogenic-serial-flash-retention-operability.md', case_hist_marker, case_hist_block)

eng_marker = '### E — environment can preserve one relation while degrading another\n\n`colder` is not one scalar measure of `better memory`. In this case the environment can support long storage of an already-written pattern while worsening active-operation timing and pass rate.\n\n---\n\n## Functional analogies and limits'
eng_new = '''### E — environment can preserve one relation while degrading another

`colder` is not one scalar measure of `better memory`. In this case the environment can support long storage of an already-written pattern while worsening active-operation timing and pass rate.

### E — active operating range != retention qualification range

The 2014 Cypress product evidence makes the converse boundary explicit: Flash operations may remain specified across a broad high-temperature range while the qualified retention interval is separately conditioned by average temperature and prior cycling. A product's operating-grade ceiling is therefore not a hidden promise that its headline retention number applies unchanged at that ceiling.

### E — temperature history can be retained as a condition even when no temperature log is stored in the memory

The Cypress retention-calculator note makes the guarantee depend on an application's temperature profile. The Flash payload does not need to store a temperature log for environmental history to matter physically and contractually. `retention depends on history` therefore does not imply `the device archives that history`.

### X — cold result != inverse high-temperature acceleration law

The cryogenic paper and Cypress qualification tables constrain the environmental problem from different sides, but they do not establish one measured activation energy or a quantitative conversion from `24 months with zero observed errors while cold` to a predicted room/high-temperature lifetime.

---

## Functional analogies and limits'''
replace_once('cases/132-cryogenic-serial-flash-retention-operability.md', eng_marker, eng_new)

replace_once(
    'cases/132-cryogenic-serial-flash-retention-operability.md',
    '- Very-low-temperature program/erase degradation does not imply the same behavior at elevated storage temperatures.\n- The experiment does not replace JESD218/JESD219 SSD qualification or named SSD/controller validation.',
    '- Very-low-temperature program/erase degradation does not imply the same behavior at elevated storage temperatures. The Cypress addendum supplies only a separate vendor qualification/derating boundary, not a common microscopic model.\n- Elevated-temperature product contracts do not identify the anonymous 2015 samples, prove raw-cell charge-loss kinetics, or provide a universal Flash activation energy.\n- The experiment does not replace JESD218/JESD219 SSD qualification or named SSD/controller validation.'
)

replace_once(
    'cases/132-cryogenic-serial-flash-retention-operability.md',
    '| retention-valid environment can differ from operation-valid environment | `E` | bounded reconstruction from split test results |',
    '| retention-valid environment can differ from operation-valid environment | `E` | bounded reconstruction from split test results |\n| at fixed 100 K P/E history, Cypress PSoC Flash qualified 20 years at average `TA <= 55 °C` but 10 years at `TA <= 85 °C` | `H/P` | 2014 manufacturer datasheet |\n| active operating-temperature range implies the same retention lifetime at every supported temperature | `X` | manufacturer retention conditions reject this shortcut |\n| cryogenic zero-error observation determines a quantitative high-temperature acceleration law | `X` | no common activation-energy/kinetics measurement |'
)

replace_once(
    'cases/132-cryogenic-serial-flash-retention-operability.md',
    '2. Author-uploaded accepted manuscript for the same article, PII `S0011-2275(15)00064-8`, Manuscript ID `CRYOGENICS-D-15-00007`, received 7 January 2015, revised 7 May 2015, accepted 14 May 2015. ResearchGate record: <https://www.researchgate.net/publication/277338221_Batch_screening_of_commercial_serial_flash-memory_integrated_circuits_for_low-temperature_applications>.\n\nThe accepted manuscript, not a publisher-typeset facsimile, is the directly text-inspected experimental source in this slice. Exact claims are therefore anchored to its section/figure/table structure in the accompanying evidence record rather than to unverified final-pagination quotations.',
    '2. Author-uploaded accepted manuscript for the same article, PII `S0011-2275(15)00064-8`, Manuscript ID `CRYOGENICS-D-15-00007`, received 7 January 2015, revised 7 May 2015, accepted 14 May 2015. ResearchGate record: <https://www.researchgate.net/publication/277338221_Batch_screening_of_commercial_serial_flash-memory_integrated_circuits_for_low-temperature_applications>.\n3. Cypress Semiconductor, *PSoC 3: CY8C34 Automotive Family Datasheet*, Document 001-57331 Rev. *G, revised 14 February 2014; first-party legacy copy preserved by Infineon: <https://www.infineon.com/dgdl/Infineon-PSoC_3_CY8C34_Automotive_Family_Datasheet_Programmable_System-on-Chip_%28PSoC%29_Datasheet-AdditionalTechnicalInformation-v08_00-EN.pdf?fileId=8ac78c8c7d0d8da4017d0ecabcb643c4>.\n4. Cypress/Infineon, KBA203737, **“How long will data be retained in Cypress Flash memory devices if only a few erase cycles are planned?”**, 15 October 2015: <https://community.infineon.com/t5/Knowledge-Base-Articles/How-long-will-data-be-retained-in-Cypress-Flash-memory-devices-if-only-a-few/ta-p/249710>.\n5. Cypress Semiconductor, *S25FL116K/S25FL132K/S25FL164K* SPI Flash datasheet, Document 002-00497, current legacy Rev. *I (4 July 2018), with revision history recording Data Retention section addition in 2016: <https://www.infineon.com/assets/row/public/documents/10/49/infineon-s25fl116k-s25fl132k-s25fl164k-16-mbit-2-mbyte-32-mbit-4-mbyte-64-mbit-8-mbyte-3.0-v-spi-flash-memory-datasheet-en.pdf?fileId=8ac78c8c7d0d8da4017d0ed4ebee537f>.\n\nThe accepted manuscript, not a publisher-typeset facsimile, is the directly text-inspected cryogenic experimental source. The Cypress documents are separate product/vendor qualification witnesses used to bound elevated-temperature claims; they are not evidence that the anonymous cryogenic-test parts were Cypress devices.'
)

# Existing grounding record: route the now-closed elevated-temperature comparison item to the addendum.
replace_once(
    'evidence/132-2015-cryogenic-serial-flash-grounding.md',
    'This evidence record grounds [`cases/132-cryogenic-serial-flash-retention-operability.md`](../cases/132-cryogenic-serial-flash-retention-operability.md).',
    'This evidence record grounds [`cases/132-cryogenic-serial-flash-retention-operability.md`](../cases/132-cryogenic-serial-flash-retention-operability.md). Elevated-temperature product qualification/derating is deepened separately in [`132-2014-2018-temperature-conditioned-retention-contract-deepening.md`](132-2014-2018-temperature-conditioned-retention-contract-deepening.md).'
)
replace_once(
    'evidence/132-2015-cryogenic-serial-flash-grounding.md',
    'Future work should be narrow rather than generic: longer-duration replication, elevated-temperature comparison, direct raw-cell threshold/charge-loss studies, named modern serial-Flash products, independent laboratories, or controlled thermal-cycling fault experiments.',
    'Future work should be narrow rather than generic: longer-duration replication, direct raw-cell threshold/charge-loss and quantitative acceleration studies, named modern serial-Flash products, independent laboratories, or controlled thermal-cycling fault experiments. The bounded elevated-temperature **qualification/contract** comparison is now handled by the linked Case-132 addendum; raw-cell kinetics remain open.'
)

# ROADMAP: add a completed bounded slice and refine the remaining gap rather than closing kinetics.
roadmap_insert = '''## Phase 2 — Build missing technical bridges

- [x] Case 132 elevated-temperature Flash retention-contract deepening — [`cases/132-cryogenic-serial-flash-retention-operability.md`](cases/132-cryogenic-serial-flash-retention-operability.md), deepened by [`evidence/132-2014-2018-temperature-conditioned-retention-contract-deepening.md`](evidence/132-2014-2018-temperature-conditioned-retention-contract-deepening.md): Cypress's 2014 PSoC 3 datasheet holds 100 K P/E history constant while qualifying 20 years at average `TA <= 55 °C` and 10 years at `TA <= 85 °C`, and its retention calculator is explicitly temperature-profile dependent; a 15-Oct-2015 Cypress KBA independently warns that extended higher-temperature storage requires longevity calculation. This closes the bounded `operating-temperature support != uniform retention lifetime` / elevated-temperature **vendor qualification** comparison without identifying the anonymous 2015 cryogenic samples, deriving a raw-cell activation energy, or claiming one Flash-wide acceleration law. Direct charge-loss kinetics, bake/acceleration methodology, independent replication, and controlled fault injection remain open.'''
replace_once('ROADMAP.md', '## Phase 2 — Build missing technical bridges', roadmap_insert)
replace_once(
    'ROADMAP.md',
    'Flash/EEPROM charge-loss kinetics beyond this device-level cryogenic result, elevated-temperature acceleration, longer independent replication, and controlled fault injection remain open;',
    'raw Flash/EEPROM charge-loss kinetics and quantitative acceleration beyond the now-grounded vendor temperature-conditioned qualification/derating boundary, longer independent replication, and controlled fault injection remain open;'
)

# CASE_INDEX: update the Case-132 navigation row and append new findings.
replace_once(
    'CASE_INDEX.md',
    '[2015 cryogenic serial-Flash grounding](evidence/132-2015-cryogenic-serial-flash-grounding.md); longer-duration replication, elevated-temperature comparison, raw-cell charge-loss kinetics, named modern products, and independent fault testing remain open',
    '[2015 cryogenic serial-Flash grounding](evidence/132-2015-cryogenic-serial-flash-grounding.md) + [2014–2018 temperature-conditioned retention-contract deepening](evidence/132-2014-2018-temperature-conditioned-retention-contract-deepening.md); elevated-temperature vendor qualification/derating is now bounded, while longer-duration replication, direct raw-cell charge-loss/acceleration kinetics, named modern products, and independent fault testing remain open'
)

findings = r'''## Case 132 deepening — elevated-temperature Flash retention-contract findings

- **2439 — active operating-temperature range != one uniform retention lifetime.** Cypress PSoC 3 specifies Flash operations across a broad temperature range while giving separately conditioned retention intervals; command admissibility and long-term state survival are different product relations. (`H/P`, `E`)
- **2440 — fixed P/E history != temperature-independent retention.** In the 2014 CY8C34 table, the same 100 K erase/program history is paired with 20 years minimum retention at average `TA <= 55 °C` but 10 years at `TA <= 85 °C`. (`H/P`)
- **2441 — product temperature grade != retention-test temperature.** A device can carry an operating grade extending above the temperature used to qualify a headline retention interval; the broader grade must not be silently substituted for the retention condition. (`H/P`, `X`)
- **2442 — retention clock origin != manufacturing age or power-on time.** The bounded Cypress datasheet measures Flash retention from the last erase cycle, making state-change history rather than fabrication date the stated origin of the retention interval. (`H/P`, `E`)
- **2443 — environmental retention condition can be a time profile, not one instantaneous maximum.** Cypress's note offers a calculator based on customer temperature profiles across the operating range, so retention qualification can depend on exposure history. (`H/P`, `E`)
- **2444 — temperature history and cycling history are jointly relevant.** Holding only one variable fixed is insufficient: the historical product evidence conditions retention by both prior P/E count and average/profiled temperature. (`H/P`, `E`)
- **2445 — low cycling burden != temperature-independent shelf life.** Cypress KBA203737 (15-Oct-2015) says few erase cycles can support long retention while still warning that extended higher-temperature exposure requires longevity calculation. (`H/P*`, `X`)
- **2446 — serial-Flash retention table != proof that the same lifetime holds at every supported operating temperature.** S25FL1-K documentation separately states P/E-conditioned retention and active temperature grades; later Infineon guidance identifies about 55 °C average field temperature as the assumption behind the 10K/100K examples. (`H/P`, `X`)
- **2447 — cryogenic zero-error observation != measured acceleration law.** Ihmig et al.'s 24-month finite test and Cypress's elevated-temperature qualification numbers do not provide one common activation energy or a quantitative cold-to-hot lifetime conversion. (`H/P`, `E`, `X`)
- **2448 — elevated-temperature qualification witness != identity of the cryogenic-test device.** The 2015 experiment anonymizes its commercial serial-Flash parts; the Cypress PSoC/KBA/S25FL records are bounded comparative witnesses, not product identification. (`H/P`, `X`)
- **2449 — colder storage benefit and colder operation penalty can coexist without contradiction.** Case 132's cryogenic program/erase slowdown and the vendor's elevated-temperature retention derating concern different operation-typed relations; neither supports a scalar rule that `colder is always better`. (`E`)
- **2450 — vendor retention contract != raw-cell charge-loss kinetics.** This deepening closes the roadmap's elevated-temperature comparison only at the qualification/derating layer; activation-energy measurement, bake acceleration, threshold-distribution evolution, and independent fault experiments remain open. (`H/P`, `X`)
'''
append_once('CASE_INDEX.md', '## Case 132 deepening — elevated-temperature Flash retention-contract findings', findings)

# Validate canonical state before self-cleanup.
index = (ROOT / 'CASE_INDEX.md').read_text(encoding='utf-8')
for n in range(2439, 2451):
    token = f'**{n} —'
    if index.count(token) != 1:
        raise SystemExit(f'finding {n} count != 1')

for path in [
    'cases/132-cryogenic-serial-flash-retention-operability.md',
    'evidence/132-2015-cryogenic-serial-flash-grounding.md',
    'evidence/132-2014-2018-temperature-conditioned-retention-contract-deepening.md',
    'ROADMAP.md',
    'CASE_INDEX.md',
]:
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    p.write_text(text.rstrip() + '\n', encoding='utf-8')

# Remove one-shot integration scaffolding in the same research commit.
for temp in [ROOT / '.github/workflows/tmp-case132-temperature-contract.yml', ROOT / 'tools/tmp_case132_temperature_contract.py']:
    if temp.exists():
        temp.unlink()
