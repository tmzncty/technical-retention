# Case 132 deepening — accelerated retention qualification and Arrhenius model boundaries, 2005–2013

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
