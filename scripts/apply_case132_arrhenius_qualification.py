from pathlib import Path

CASE = Path('cases/132-cryogenic-serial-flash-retention-operability.md')
ROADMAP = Path('ROADMAP.md')
INDEX = Path('CASE_INDEX.md')
EVIDENCE = Path('evidence/132-2005-2013-arrhenius-qualification-boundary-deepening.md')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly one match, found {count}')
    return text.replace(old, new, 1)


EVIDENCE_TEXT = r'''# Case 132 deepening — accelerated retention qualification and Arrhenius model boundaries, 2005–2013

This evidence addendum deepens [`../cases/132-cryogenic-serial-flash-retention-operability.md`](../cases/132-cryogenic-serial-flash-retention-operability.md).

**Bounded question:** the 2015 cryogenic experiment directly observed a finite cold-store -> warm-verify retention result, and the earlier Case-132 addendum separately grounded temperature-conditioned product retention contracts. What can manufacturer-primary reliability documentation establish about a different evidentiary operation — using high-temperature accelerated stress plus an Arrhenius model to estimate retention at a stated use temperature — and where must that model stop?

This addendum does **not** identify the anonymous 2015 serial-Flash samples with Freescale/NXP products. It does not derive a microscopic charge-loss law for those samples, does not validate an Arrhenius relation down to liquid-nitrogen temperature, and does not claim that one activation energy applies across Flash technologies.

---

## Source A — Freescale EB618/D Rev. 4, April 2005

**Document:** Martin Niset and Peter Kuhn, NVM Reliability, Freescale Semiconductor, *Typical Data Retention for Nonvolatile Memory*, EB618/D, Rev. 4, April 2005.

**First-party preserved PDF:** <https://www.nxp.com/docs/en/engineering-bulletin/EB618.pdf>

**First-party product-page provenance:** NXP continues to list `EB618`, Rev. 4, dated 2 April 2005, as a technical note for legacy Freescale MCU families.

**Evidence class:** `H/P` — manufacturer engineering bulletin preserved by the successor manufacturer.

### A1. Minimum specification and typical modeled retention are different claims

EB618 explicitly separates a product's **minimum data-retention life** from a longer **typical** value. It defines the latter by de-rating what it calls a technology's intrinsic retention capability to a normalized use condition.

That distinction matters because a model-derived typical value is not silently promoted into a guaranteed minimum:

```text
minimum product retention specification
    !=
typical model-derived retention estimate
```

The bulletin therefore blocks a common historical shortcut: a long extrapolated number in a reliability note is not automatically the product's guaranteed archival lifetime.

### A2. The bulletin makes accelerated stress and the Arrhenius model explicit

EB618 describes intrinsic data retention as an **estimate** based on accelerated-stress data and the Arrhenius model. For floating-gate technologies it gives the temperature acceleration factor as:

```text
AF = exp[(Ea / k) * (1/TUse - 1/TStress)]
```

where `Ea` is intrinsic activation energy, `TUse` the use temperature, and `TStress` the stress temperature.

The historical record is therefore stronger than a vague statement that hotter tests are merely `faster`. Freescale documents an explicit stress-to-use transformation whose result depends on both the temperatures and a model parameter.

### A3. Activation energy can be measured or explicitly defaulted

EB618 says Freescale determines intrinsic activation energy for a technology empirically by evaluating **time-to-failure under high-temperature stress**. It then says typical retention at the nominal use condition is calculated from the measured activation energy together with accelerated-stress data from technology certification, product qualification, or wafer bake.

The same bulletin separately labels `0.8 eV` as a **default** activation energy used when empirical data are unavailable. Its table shows different technology rows using `0.92 eV` and `1.2 eV` measured values as well as `0.8 eV` default values.

That directly grounds:

```text
empirically determined Ea
    !=
default Ea used for estimation
    !=
universal Flash activation energy
```

### A4. “Equivalent years” are model outputs, not years directly observed

With the stated default `0.8 eV`, EB618 gives examples such as `1008 h at 150 °C` being equivalent under the model to `1150 years at 25 °C` or `60 years at 55 °C`, and `24 h at 250 °C` being equivalent to `1800 years at 25 °C` or `100 years at 55 °C`.

These examples are valuable precisely because their evidence status can be typed. The high-temperature hours are an accelerated-stress exposure; the much longer use-condition intervals are **derived model-equivalent times**. They are not direct observations of a device operating for centuries.

Therefore:

> **accelerated-stress duration != directly observed use-life duration.**

---

## Source B — Freescale K30 Sub-Family Data Sheet, Rev. 7, February 2013

**Document:** Freescale Semiconductor, *K30 Sub-Family Data Sheet*, K30P81M100SF2, Rev. 7, February 2013.

**First-party preserved PDF:** <https://www.nxp.com/assets/documents/data/en/data-sheets/K30P81M100SF2.pdf>

**Evidence class:** `H/P` — manufacturer product datasheet.

The NVM reliability table says its **typical data-retention values are based on measured response accelerated at high temperature and de-rated to a constant 25 °C use profile**. In the same note it explicitly says:

> `Engineering Bulletin EB618 does not apply to this technology.`

That one sentence is an unusually strong anti-portability boundary. It shows that the broad *method family* — accelerated high-temperature response followed by de-rating to a use profile — can continue while the older bulletin's technology-specific treatment is explicitly declared inapplicable to a newer product technology.

The safe relation is:

```text
continuity of accelerated-retention methodology
    !=
portability of one technology's parameters / bulletin coverage
```

The K30 datasheet does not explain every revised model parameter or reproduce the full qualification dataset. Its contribution here is the explicit manufacturer warning against reusing EB618 as if it were technology-independent.

---

## Historical record

The two manufacturer records support a bounded 2005–2013 chronology:

1. by April 2005, Freescale publicly described typical NVM retention as a model-mediated estimate from accelerated stress, with an explicit Arrhenius acceleration factor and technology-specific empirical/default activation energies;
2. by February 2013, a Freescale product datasheet still described typical retention as based on measured high-temperature accelerated response and de-rating to a 25 °C use profile, while explicitly stating that **EB618 did not apply to that technology**.

This is not an invention chronology for Arrhenius reliability modeling. It is a public manufacturer-documentation floor for the bounded retention-qualification relation.

---

## Engineering reconstruction

### E — accelerated qualification compresses evidence time, not physical calendar history

An accelerated stress can make a retention claim testable within laboratory time only by introducing a model connecting stress and use conditions. The result is therefore relational:

```text
observed stress response
    + stress temperature
    + use temperature
    + activation-energy assumption / measurement
    + model
    -> model-equivalent use-condition estimate
```

The derived use interval is not itself an observed history of the tested sample.

### E — the acceleration factor is parameterized, not universal

Because `AF` depends on `Ea`, `TUse`, and `TStress`, changing the assumed/measured activation energy changes the mapping between stress time and use time. EB618's own technology table and the K30 exclusion make parameter portability an evidence question rather than a default assumption.

### E — method continuity != parameter portability

The K30 datasheet is a direct counterexample to treating an older reliability bulletin as a timeless physical law. A vendor can continue to use high-temperature acceleration/de-rating while refusing to apply an older technology-specific document to a newer process.

### E — model-equivalent time != deterministic failure instant

A retention estimate or qualification relation describes what a population/model/product contract supports under stated assumptions and criteria. It does not imply that every bit in every individual device fails when a derived clock reaches one exact instant.

### E — a temperature/use model can matter without being stored by the memory

The retention calculation can depend on stress/use temperatures and a normalized use profile even when the Flash payload contains no log of those temperatures. A condition on the retention relation is not automatically a retained telemetry record.

---

## Functional analogy — bounded

### Case 76 — JESD218 SSD endurance / retention qualification

Case 76 also separates direct stress execution from a later service/retention claim and treats temperature, workload, endurance state, error criteria, and controller recovery as parts of a qualification relation.

The safe analogy is only:

> **both cases make a retention lifetime claim depend on an evidence-producing stress/model/qualification procedure rather than on waiting for the full advertised use interval.**

The mechanisms and layers remain different. EB618 concerns manufacturer NVM technology/product retention estimation; JESD218 is an SSD-level standardized endurance/retention service contract. No genealogy or parameter identity is asserted.

### Case 132 cryogenic experiment

The 2015 cryogenic experiment is almost the inverse evidentiary shape: it reports a finite **direct observation** under very low-temperature storage with periodic warm verification, rather than using an Arrhenius acceleration factor to translate a high-temperature stress into a much longer modeled use interval.

That contrast is useful, but it does **not** authorize taking EB618's formula/activation energies and extrapolating them down to the experiment's approximately `-130 °C` to `-195 °C` storage regime.

---

## Philosophical interpretation — bounded

### I — a technical “lifetime” can be a model-mediated evidence relation

A published retention lifetime can name more than elapsed time on a specimen. In accelerated qualification it can summarize a relation among observed stress, a transformation model, technology-specific parameters, a target use condition, and an acceptance criterion.

This sharpens the repository's general distinction between **retained state** and **evidence that licenses a future-retention claim**. It does not mean that the device somehow `stores future time`, and it does not convert reliability engineering into a philosophical theory of memory.

---

## Rejected claims / stop boundaries

- `EB618 is the origin of Arrhenius reliability modeling` — **rejected**; the bulletin calls the method an industry standard and makes no invention-priority claim.
- `0.8 eV is the activation energy of Flash` — **rejected**; EB618 distinguishes measured technology-specific values from a default value used when empirical data are unavailable.
- `EB618 parameters apply to every later Freescale/NXP Flash technology` — **rejected**; the 2013 K30 datasheet explicitly says EB618 does not apply to that technology.
- `1008 h at 150 °C is literally the same physical history as 1150 years at 25 °C` — **rejected**; equivalence is produced by the stated model and assumptions.
- `the 2015 cryogenic no-error result validates the inverse of EB618's high-temperature Arrhenius relation` — **rejected**; there is no product/process identity or validated common activation-energy regime across those temperatures.
- `typical extrapolated retention is the guaranteed minimum product lifetime` — **rejected**; EB618 explicitly separates the two.
- `accelerated qualification proves continuous field reliability under every workload, environment, and device state` — **rejected**; the evidence is bounded by technology, stress procedure, use condition, model, and acceptance criteria.

---

## Related repositories

### `tmzncty/computing-archaeology`

A fresh search for `data retention Arrhenius flash` found no dedicated overlapping case. A broader history of Arrhenius semiconductor reliability engineering, activation-energy measurement, JEDEC/AEC accelerated-life methodology, and process-generation changes belongs there if developed. This repository keeps only the retention-specific distinction among direct observation, accelerated stress, model transformation, product guarantee, and cross-technology parameter portability.

### `tmzncty/problem-history`

The historical actor problem in EB618 is how a manufacturer defines and supports `typical data retention` from accelerated evidence, not a general philosophical question about whether memory `travels through time`. The latter remains a later project interpretation.

---

## Readiness assessment

This slice closes the bounded Case-132 roadmap gap at the **manufacturer-primary accelerated-stress / Arrhenius-method boundary**:

- explicit 2005 stress-to-use formula and evidence chain;
- explicit separation of minimum specification from typical model-derived retention;
- explicit distinction between measured and default activation energy;
- technology-specific activation-energy examples;
- an explicit 2013 product-level warning that EB618 does not apply to a newer technology even while accelerated high-temperature response/de-rating remains the stated methodology.

It does **not** close direct raw-cell charge-loss kinetics for the anonymous 2015 serial-Flash devices, validate one Arrhenius model into the cryogenic range, provide independent long-duration replication, or supply controlled fault injection.
'''

EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
if EVIDENCE.exists() and EVIDENCE.read_text(encoding='utf-8') != EVIDENCE_TEXT:
    raise RuntimeError('evidence path already exists with different content')
EVIDENCE.write_text(EVIDENCE_TEXT, encoding='utf-8')

# --- Case 132 ---
case = CASE.read_text(encoding='utf-8')
link_path = '../evidence/132-2005-2013-arrhenius-qualification-boundary-deepening.md'
if link_path not in case:
    anchor = "Temperature-conditioned qualification deepening: [`../evidence/132-2014-2018-temperature-conditioned-retention-contract-deepening.md`](../evidence/132-2014-2018-temperature-conditioned-retention-contract-deepening.md). This later/deeper evidence is a bounded comparison, not an identification of the anonymous cryogenic-test ICs with Cypress products.\n"
    addition = anchor + "\nAccelerated-retention qualification deepening: [`../evidence/132-2005-2013-arrhenius-qualification-boundary-deepening.md`](../evidence/132-2005-2013-arrhenius-qualification-boundary-deepening.md). This 2005–2013 manufacturer-primary slice grounds accelerated-stress / Arrhenius evidence semantics and technology-specific parameter portability; it does not convert the 2015 cryogenic observation into an inverse acceleration law.\n"
    case = replace_once(case, anchor, addition, 'case evidence-link insertion')

hist_anchor = "Detailed evidence and provenance are kept in the temperature-conditioned addendum.\n\n---\n\n## Retained state and substrate"
if '### H/P — accelerated retention qualification is model-mediated and technology-qualified' not in case:
    hist_insert = """Detailed evidence and provenance are kept in the temperature-conditioned addendum.\n\n### H/P — accelerated retention qualification is model-mediated and technology-qualified\n\nFreescale's April-2005 EB618 engineering bulletin describes `typical data retention` as an estimate derived from accelerated stress plus an Arrhenius stress-to-use transformation. It explicitly separates product minimum retention from the longer typical estimate, says activation energy can be determined empirically from high-temperature time-to-failure data, and separately labels `0.8 eV` as a default when empirical activation-energy data are unavailable. Its technology table also contains different measured/default `Ea` values rather than one universal Flash constant.\n\nA February-2013 Freescale K30 datasheet supplies a particularly strong boundary: it still says typical retention is based on measured high-temperature accelerated response de-rated to a constant 25 °C use profile, yet explicitly states that **EB618 does not apply to this technology**. Thus the method family can persist while one older technology-specific treatment becomes inapplicable.\n\nThese records are separate from the anonymous commercial parts in the 2015 cryogenic study. They establish a manufacturer-primary accelerated-qualification method boundary, not product identity or a cold-to-hot conversion for the cryogenic samples. Detailed evidence is in the 2005–2013 accelerated-retention addendum.\n\n---\n\n## Retained state and substrate"""
    case = replace_once(case, hist_anchor, hist_insert, 'case historical deepening insertion')

if '5. **accelerated-stress exposure time**' not in case:
    time_old = """At least four different times must stay separate:\n\n1. **storage interval** — the duration for which an already-written pattern remains recoverable under the tested cryogenic-storage procedure;\n2. **verification interval** — roughly six months between warm checks in the retention group;\n3. **command latency** — program/erase time, which increased substantially at lower temperature;\n4. **environmental transition time** — the warm/cold mode change needed to perform the periodic verification procedure.\n\nNone of these intervals is interchangeable with a JEDEC SSD retention class, a NAND raw-cell retention constant, or a DRAM refresh interval."""
    time_new = """At least six different times must stay separate:\n\n1. **storage interval** — the duration for which an already-written pattern remains recoverable under the tested cryogenic-storage procedure;\n2. **verification interval** — roughly six months between warm checks in the retention group;\n3. **command latency** — program/erase time, which increased substantially at lower temperature;\n4. **environmental transition time** — the warm/cold mode change needed to perform the periodic verification procedure;\n5. **accelerated-stress exposure time** — laboratory bake/stress duration actually elapsed in an accelerated-retention test;\n6. **model-equivalent use time** — a longer use-condition interval derived from stress temperature, use temperature, activation energy, and a model rather than directly observed on the specimen.\n\nNone of these intervals is interchangeable with a JEDEC SSD retention class, a NAND raw-cell retention constant, or a DRAM refresh interval. In particular, accelerated-stress time and model-equivalent use time are related by assumptions rather than being the same observed history."""
    case = replace_once(case, time_old, time_new, 'case time decomposition')

if '### E — accelerated-test time != directly observed use-life time' not in case:
    eng_anchor = "### X — cold result != inverse high-temperature acceleration law\n"
    eng_insert = """### E — accelerated-test time != directly observed use-life time\n\nEB618's high-temperature bake examples compress an evidence-producing test by using an Arrhenius stress-to-use transformation. The stress hours are observed; the much longer nominal-use interval is a model result. `equivalent years` therefore must not be paraphrased as a specimen having literally survived those years.\n\n### E — one activation energy != one universal Flash temperature law\n\nThe acceleration factor depends on `Ea`, stress temperature, and use temperature. EB618 itself distinguishes measured technology-specific activation energies from a default value, while the 2013 K30 datasheet explicitly says EB618 does not apply to its technology. Model choice and parameter applicability are therefore evidence questions.\n\n### E — method continuity != parameter portability\n\nA later product can retain the broad practice `measured high-temperature response -> de-rate to use profile` while rejecting the applicability of an older engineering bulletin. Shared reliability methodology does not establish shared process parameters, retention kinetics, or product guarantee.\n\n### X — cold result != inverse high-temperature acceleration law\n"""
    case = replace_once(case, eng_anchor, eng_insert, 'case engineering deepening')

if 'The new 2005–2013 slice adds a second boundary' not in case:
    a76_anchor = "> **component cryogenic experiment ≠ SSD retention contract.**\n"
    a76_add = a76_anchor + "\nThe new 2005–2013 slice adds a second boundary: accelerated high-temperature stress plus model de-rating can support a use-condition retention estimate without becoming the same evidence class as Case 132's directly observed finite cryogenic storage experiment. The analogy to Case 76 is only at the qualification/evidence-relation level; SSD workload/controller/error criteria remain separate.\n"
    case = replace_once(case, a76_anchor, a76_add, 'case cross-case qualification boundary')

if '### I — a retention lifetime can be a model-mediated evidence relation' not in case:
    phil_anchor = "This is a project interpretation. The 2015 authors do not present the experiment as a theory of memory, archive, or tertiary retention.\n\n---\n\n## Counterexamples and limits"
    phil_insert = """This is a project interpretation. The 2015 authors do not present the experiment as a theory of memory, archive, or tertiary retention.\n\n### I — a retention lifetime can be a model-mediated evidence relation\n\nThe Freescale accelerated-retention documents add a narrow epistemic distinction: a technical lifetime may summarize observed stress plus a transformation model, technology-specific parameters, and a target use condition rather than one directly elapsed specimen history. That helps separate **the retained state** from **the evidence that licenses a retention claim**. It does not mean the device stores future time or that model-based reliability is identical to memory itself.\n\n---\n\n## Counterexamples and limits"""
    case = replace_once(case, phil_anchor, phil_insert, 'case philosophical deepening')

if '- EB618 is manufacturer-primary evidence for one accelerated-retention methodology' not in case:
    counter_anchor = "- Elevated-temperature product contracts do not identify the anonymous 2015 samples, prove raw-cell charge-loss kinetics, or provide a universal Flash activation energy.\n"
    counter_add = counter_anchor + "- EB618 is manufacturer-primary evidence for one accelerated-retention methodology, not an invention-priority claim for the Arrhenius model and not a universal parameter table for later Flash processes.\n- The 2013 K30 datasheet explicitly says EB618 does not apply to its technology, so same-vendor method continuity cannot be used to carry older parameters forward automatically.\n- No inspected source validates EB618's high-temperature model parameters across the 2015 experiment's liquid-nitrogen-scale storage temperatures.\n"
    case = replace_once(case, counter_anchor, counter_add, 'case counterexample additions')

if '| Freescale EB618 defines typical retention as an accelerated-stress / Arrhenius estimate' not in case:
    ledger_anchor = "| cryogenic zero-error observation determines a quantitative high-temperature acceleration law | `X` | no common activation-energy/kinetics measurement |\n"
    ledger_add = ledger_anchor + "| Freescale EB618 defines typical retention as an accelerated-stress / Arrhenius estimate rather than the product minimum guarantee | `H/P` | 2005 manufacturer engineering bulletin |\n| EB618 distinguishes measured technology-specific activation energy from a `0.8 eV` default used when empirical data are unavailable | `H/P` | direct manufacturer methodology statement |\n| the 2013 K30 datasheet still uses high-temperature acceleration/de-rating but explicitly says EB618 does not apply to that technology | `H/P` | direct product datasheet boundary |\n| accelerated-stress duration is the same directly observed history as the model-equivalent use interval | `X` | equivalence is model- and parameter-mediated |\n| EB618 parameters can be extrapolated to the 2015 anonymous cryogenic parts / liquid-nitrogen regime | `X` | no product/process identity or validated cryogenic-range model |\n"
    case = replace_once(case, ledger_anchor, ledger_add, 'case claim-ledger additions')

if 'Fresh searches for `cryogenic`, `serial flash`, and `data retention Arrhenius flash`' not in case:
    old_related = "Fresh searches for `cryogenic` and `serial flash` found no dedicated case to reuse. A broader history of low-temperature electronics, serial-Flash product evolution, device packaging, and cryogenic instrumentation belongs there if developed. This case retains only the retention-specific relation among environmental storage, operation availability, verification, and reversibility."
    new_related = "Fresh searches for `cryogenic`, `serial flash`, and `data retention Arrhenius flash` found no dedicated case to reuse. A broader history of low-temperature electronics, serial-Flash product evolution, semiconductor reliability/Arrhenius methodology, activation-energy measurement, and cryogenic instrumentation belongs there if developed. This case retains only the retention-specific relation among environmental storage, operation availability, verification, accelerated evidence, model transformation, and reversibility."
    case = replace_once(case, old_related, new_related, 'case related-repo update')

if '6. Martin Niset and Peter Kuhn' not in case:
    sources_anchor = "5. Cypress Semiconductor, *S25FL116K/S25FL132K/S25FL164K* SPI Flash datasheet, Document 002-00497, current legacy Rev. *I (4 July 2018), with revision history recording Data Retention section addition in 2016: <https://www.infineon.com/assets/row/public/documents/10/49/infineon-s25fl116k-s25fl132k-s25fl164k-16-mbit-2-mbyte-32-mbit-4-mbyte-64-mbit-8-mbyte-3.0-v-spi-flash-memory-datasheet-en.pdf?fileId=8ac78c8c7d0d8da4017d0ed4ebee537f>.\n"
    sources_add = sources_anchor + "6. Martin Niset and Peter Kuhn, Freescale Semiconductor NVM Reliability, *Typical Data Retention for Nonvolatile Memory*, EB618/D Rev. 4, April 2005; first-party successor-hosted PDF: <https://www.nxp.com/docs/en/engineering-bulletin/EB618.pdf>.\n7. Freescale Semiconductor, *K30 Sub-Family Data Sheet*, K30P81M100SF2, Rev. 7, February 2013; first-party successor-hosted PDF: <https://www.nxp.com/assets/documents/data/en/data-sheets/K30P81M100SF2.pdf>.\n"
    case = replace_once(case, sources_anchor, sources_add, 'case source additions')

CASE.write_text(case, encoding='utf-8')

# --- ROADMAP ---
roadmap = ROADMAP.read_text(encoding='utf-8')
if 'Case 132 accelerated-retention / Arrhenius qualification boundary deepening' not in roadmap:
    roadmap_anchor = "- [ ] DRAM evolution and refresh machinery beyond the bounded case"
    pos = roadmap.find(roadmap_anchor)
    if pos < 0:
        raise RuntimeError('ROADMAP phase-2 insertion anchor unavailable')
    bullet = "- [x] Case 132 accelerated-retention / Arrhenius qualification boundary deepening — [`cases/132-cryogenic-serial-flash-retention-operability.md`](cases/132-cryogenic-serial-flash-retention-operability.md), deepened by [`evidence/132-2005-2013-arrhenius-qualification-boundary-deepening.md`](evidence/132-2005-2013-arrhenius-qualification-boundary-deepening.md): Freescale EB618 Rev. 4 (04/2005) makes `typical data retention` a model-mediated estimate from accelerated stress plus an Arrhenius stress-to-use transformation, separates the product minimum guarantee from the typical estimate, and distinguishes measured technology-specific activation energies from a `0.8 eV` default. Freescale's K30 Rev. 7 datasheet (02/2013) still describes measured high-temperature response de-rated to a 25 °C use profile while explicitly saying EB618 does not apply to that technology. This closes `accelerated-stress time != directly observed use-life time` and `method continuity != parameter portability`; raw-cell kinetics for the anonymous 2015 parts, cryogenic-range model validation, independent replication, and fault injection remain open. Broad reliability-method genealogy belongs primarily in `computing-archaeology`.\n\n"
    roadmap = roadmap[:pos] + bullet + roadmap[pos:]

old_debt = "raw Flash/EEPROM charge-loss kinetics and quantitative acceleration beyond the now-grounded vendor temperature-conditioned qualification/derating boundary, longer independent replication, and controlled fault injection remain open;"
new_debt = "manufacturer-primary accelerated-stress/Arrhenius methodology and technology-specific parameter portability are now further bounded by the 2005–2013 Case 132 deepening; direct raw Flash/EEPROM charge-loss kinetics for the anonymous cryogenic-test parts, cryogenic-range validation of any acceleration model, longer independent replication, and controlled fault injection remain open;"
if old_debt in roadmap:
    roadmap = replace_once(roadmap, old_debt, new_debt, 'ROADMAP Case 132 Phase-4 debt update')
elif new_debt not in roadmap:
    raise RuntimeError('ROADMAP Case 132 Phase-4 debt marker unavailable')
ROADMAP.write_text(roadmap, encoding='utf-8')

# --- CASE_INDEX ---
index = INDEX.read_text(encoding='utf-8')
case_row_lines = [line for line in index.splitlines(keepends=True) if '[Cryogenic Serial Flash: Retention Without Full Cryogenic Operability]' in line]
if len(case_row_lines) != 1:
    raise RuntimeError(f'Case 132 index row count unexpected: {len(case_row_lines)}')
case_row = case_row_lines[0]
if '132-2005-2013-arrhenius-qualification-boundary-deepening.md' not in case_row:
    body = case_row.rstrip('\n')
    if not body.endswith(' |'):
        raise RuntimeError('Case 132 index row does not end with expected table delimiter')
    body = body[:-2] + " + [2005–2013 accelerated-stress / Arrhenius model-boundary deepening](evidence/132-2005-2013-arrhenius-qualification-boundary-deepening.md); direct anonymous-device kinetics, cryogenic-range model validation, independent replication/fault injection remain open |"
    index = index.replace(case_row, body + '\n', 1)

new_section_heading = '## Case 132 deepening — accelerated-stress / Arrhenius qualification findings\n'
if new_section_heading not in index:
    existing_heading = '## Case 132 deepening — elevated-temperature Flash retention-contract findings\n'
    start = index.find(existing_heading)
    if start < 0:
        raise RuntimeError('existing Case 132 deepening findings heading unavailable')
    next_heading = index.find('\n## ', start + len(existing_heading))
    if next_heading < 0:
        raise RuntimeError('next findings heading after Case 132 unavailable')
    findings = r'''

## Case 132 deepening — accelerated-stress / Arrhenius qualification findings

Evidence: [`evidence/132-2005-2013-arrhenius-qualification-boundary-deepening.md`](evidence/132-2005-2013-arrhenius-qualification-boundary-deepening.md).

- **2695 — EB618's April-2005 public manufacturer record != invention of Arrhenius reliability modeling.** Freescale calls the Arrhenius model an industry standard; the bounded date is a documentation floor for this vendor retention-method description, not an origin claim. (`H/P`, `X`)
- **2696 — minimum product retention specification != typical model-derived retention estimate.** EB618 explicitly separates a generally 10–20-year guaranteed minimum from longer typical values de-rated from intrinsic capability to a normalized use condition. (`H/P`, `E`)
- **2697 — accelerated-stress duration != directly observed nominal-use lifetime.** High-temperature hours are observed stress exposure; century-scale examples at lower use temperatures are Arrhenius-model outputs, not elapsed specimen histories. (`H/P`, `E`)
- **2698 — temperature acceleration factor != universal clock conversion.** EB618's `AF` depends on activation energy, stress temperature, and use temperature, so equivalence is parameterized by a stated model relation. (`H/P`, `E`)
- **2699 — empirically determined activation energy != default activation energy.** Freescale says technology `Ea` can be determined from high-temperature time-to-failure data while `0.8 eV` is used as a conservative default when empirical data are unavailable. (`H/P`)
- **2700 — one activation energy != universal Flash activation energy.** EB618's own table shows measured `0.92 eV` and `1.2 eV` rows alongside `0.8 eV` default rows, blocking one-value portability across technologies. (`H/P`, `X`)
- **2701 — continuity of accelerated-retention methodology != applicability of EB618.** The 2013 K30 datasheet still bases typical retention on measured high-temperature accelerated response de-rated to 25 °C while explicitly saying EB618 does not apply to that technology. (`H/P`, `E`)
- **2702 — same vendor lineage != same retention parameter set.** A successor product/process can require a different technology-specific qualification treatment even when the broad stress/de-rating method persists. (`H/P`, `E`, `X`)
- **2703 — high-temperature acceleration evidence != cryogenic-range model validation.** Nothing in EB618 or the K30 note validates the same `Ea`/Arrhenius relation across the 2015 serial-Flash experiment's approximately -130 °C to -195 °C storage regime. (`H/P`, `E`, `X`)
- **2704 — cryogenic no-error observation != inverse Arrhenius coefficient.** The 24-month direct cold-store/warm-verify result does not identify product/process parameters needed to convert it into a quantitative high-temperature lifetime law. (`H/P`, `E`, `X`)
- **2705 — model-equivalent retention time != deterministic individual-device failure instant.** An extrapolated population/use-condition estimate does not imply every bit fails when one derived timer expires. (`E`, `X`)
- **2706 — long typical intrinsic estimate != guaranteed minimum product lifetime.** EB618's explicit two-level specification blocks promotion of a modeled typical value into an archival guarantee. (`H/P`, `X`)
- **2707 — retention-qualification model != active-operation envelope.** Accelerated retention estimation answers a stored-state survival question; Case 132's cryogenic program/erase pass-rate and latency measurements answer an operation-availability question. (`E`, `X`)
- **2708 — Case 132 accelerated modeling ~= Case 76 SSD qualification only as a bounded evidence-relation analogy.** Both translate bounded stress/test evidence into a use-condition retention claim, but NVM technology parameters and SSD workload/controller/error contracts remain different layers and mechanisms. (`A`, `X`)
- **2709 — related-repository boundary:** a fresh `tmzncty/computing-archaeology` search for `data retention Arrhenius flash` found no dedicated case to reuse; broad semiconductor-reliability, activation-energy, and JEDEC/AEC accelerated-test genealogy belongs there if developed, while Case 132 keeps the retention-specific direct-observation/model/guarantee boundary. (`H/P` project-state record)
'''
    index = index[:next_heading] + findings + index[next_heading:]

INDEX.write_text(index, encoding='utf-8')

# --- final bounded assertions ---
case = CASE.read_text(encoding='utf-8')
roadmap = ROADMAP.read_text(encoding='utf-8')
index = INDEX.read_text(encoding='utf-8')
ev = EVIDENCE.read_text(encoding='utf-8')

assert case.count('132-2005-2013-arrhenius-qualification-boundary-deepening.md') >= 2
assert case.count('### H/P — accelerated retention qualification is model-mediated and technology-qualified') == 1
assert case.count('### E — accelerated-test time != directly observed use-life time') == 1
assert roadmap.count('Case 132 accelerated-retention / Arrhenius qualification boundary deepening') == 1
assert roadmap.count('132-2005-2013-arrhenius-qualification-boundary-deepening.md') == 2
assert index.count(new_section_heading.strip()) == 1
assert index.count('132-2005-2013-arrhenius-qualification-boundary-deepening.md') >= 2
for n in range(2695, 2710):
    marker = f'**{n} —'
    assert index.count(marker) == 1, (n, index.count(marker))
assert '## Historical record' in ev
assert '## Engineering reconstruction' in ev
assert '## Functional analogy — bounded' in ev
assert '## Philosophical interpretation — bounded' in ev
assert 'EB618 does not apply to this technology' in ev
