# Case 76 deepening — Intel 2012 Arrhenius retention acceleration is mechanism-specific

## Status

**`grounded` evidence deepening** for Case 76. This packet narrows one question inside SSD endurance/retention qualification:

> When a high-temperature retention bake is converted into an equivalent lower-temperature dwell, what exactly is being treated as equivalent, and what happens when more than one physical retention mechanism has a different temperature dependence?

This is not a replacement for the directly inspected JESD218 material in the base case. The principal source here is Intel's June 2012 application note, which explains how Intel interpreted and applied JESD218A retention qualification to NAND SSDs.

The bounded result is:

```text
retention qualification condition
    = prior wear state
    + storage temperature
    + storage time
    + acceptance / error criterion

Arrhenius-equivalent dwell for mechanism M
    != universal physical age for every retention mechanism
```

The reason is source-level, not philosophical: Intel distinguishes intrinsic charge loss (ICL) from stress-induced leakage current (SILC), assigns them materially different temperature behavior, and explicitly warns that a high-temperature bake that accelerates ICL does not simply accelerate SILC in the same way.

---

## Sources

### Primary manufacturer source

Intel Corporation, **_Data Retention in Intel Solid-State Drives_**, Application Note, order number **325999-002US**, revision 002, **June 2012**.

Current public mirror retained by Solidigm community infrastructure:

- <https://community.solidigm.com/hzhwu46669/attachments/hzhwu46669/Solid_State_Drives/3096/1/App_note_SSD_Data_retention.pdf>

The document revision history records an initial December 2011 release and the June 2012 revision used here.

### Repository context

- Base case: [`../cases/76-jedec-ssd-endurance-retention-qualification.md`](../cases/76-jedec-ssd-endurance-retention-qualification.md)
- Datacenter product-profile continuation: [`76-ocp-2021-2026-datacenter-nvme-retention-profile-deepening.md`](76-ocp-2021-2026-datacenter-nvme-retention-profile-deepening.md)
- Operational powered-maintenance continuation: [`../cases/111-enterprise-ssd-extended-shutdown-maintenance.md`](../cases/111-enterprise-ssd-extended-shutdown-maintenance.md)

No focused `JESD218A retention SSD` packet was found in `tmzncty/computing-archaeology` during this pass. The wider technology history therefore remains routed there rather than being recreated here.

---

# 1. Historical record

## 1.1 Intel names more than one NAND retention-loss mechanism

Intel's application note describes two distinct NAND retention mechanisms associated with program/erase-induced tunnel-oxide degradation.

For **intrinsic charge loss (ICL)**, the note describes charge trapped at metastable defects during programming and later detrapping over time. It says this mechanism is **strongly thermally activated**: increasing storage temperature increases the charge-loss rate.

For **stress-induced leakage current (SILC)**, the note describes a leakage path created by defects in the tunnel oxide. It says SILC is **not highly dependent on temperature** in the way ICL is and may anneal at temperatures as low as roughly 55 °C.

The document also distinguishes the resulting threshold-voltage failure tendencies in its MLC example: ICL and SILC are not merely two names for one mathematical process.

Therefore the period manufacturer record itself blocks:

```text
"NAND retention loss"
    != one homogeneous temperature-acceleration mechanism
```

## 1.2 ICL is the mechanism used for Intel's Arrhenius worked example

Intel says that ICL retention behavior can be accelerated by raising storage temperature and uses the Arrhenius relation to map between a use temperature and a stress-bake temperature.

The note gives:

```text
AF = acceleration factor between two storage temperatures
k  = 8.617 × 10^-5 eV/K
Ea = activation energy, typically 1.1 eV for the worked ICL relation
```

It then gives an enterprise-class worked example:

```text
retention use condition: 40 °C for 3 months = 2,190 h
stress-bake condition:    66 °C
Ea used:                  1.1 eV
calculated AF:            22.76
calculated bake time:     2,190 / 22.76 ≈ 96 h
```

Intel states that 66 °C / 96 h is one retention stress-bake condition specified in the JESD218A table it is discussing.

This is a strong historical record for a **particular acceleration model and qualification mapping**. It is not evidence that every physical process in an SSD becomes 22.76 times older during that bake.

## 1.3 Intel explicitly gives SILC a different temperature boundary

Immediately after the ICL worked example, Intel states that SILC has a fairly low activation energy of about **0.2 eV** and, more importantly, can sometimes anneal at relatively low temperatures, including around 55 °C.

The note therefore says that a high-temperature bake generally cannot be used to accelerate SILC so as to emulate a use condition in the same simple manner.

This is the key evidence boundary for this packet:

```text
ICL high-temperature acceleration
    != SILC high-temperature acceleration
```

and more strongly:

```text
higher temperature
    can accelerate one retention-loss mechanism
while
higher temperature
    can promote recovery / annealing relevant to another mechanism
```

That is why the meaning of an accelerated dwell is conditional on the mechanism being modeled.

## 1.4 Intel says JESD218A accounts for the low-activation-energy case separately

In its standards discussion, Intel says the main endurance/retention stress conditions are designed around a **high activation energy mechanism such as ICL**.

For **low activation energy mechanisms such as SILC**, the note says the standard suggests an optional room-temperature retention verification after the low-temperature endurance verification, or obtaining the corresponding data during NAND-component qualification. Intel notes that mathematical extrapolation is still needed because such mechanisms are difficult to accelerate using a high-temperature bake or other stress.

The historical point is therefore not merely that Intel knew two mechanisms existed. The qualification discussion itself keeps their evidence paths distinct.

## 1.5 Prior wear is part of the retention condition

Intel also states that both ICL and SILC arise from tunnel-oxide degradation caused by program/erase cycling and that retention capability is better at lower P/E-cycle counts than at greater wear.

The same note warns that **how** P/E cycling is performed matters: cycling time and cycling temperature affect recovery between cycles. Faster qualification cycling and field cycling need not leave exactly the same trap population even at a nominally similar cycle count.

Thus the historical source supports a condition richer than:

```text
retention = f(storage time)
```

It instead supports at least:

```text
retention behavior
    = f(prior P/E stress,
        P/E stress history,
        storage temperature,
        storage time,
        physical mechanism,
        device/controller error margin)
```

The final line is an engineering decomposition; Intel does not present it in this notation.

---

# 2. Engineering reconstruction

## 2.1 Acceleration factor is indexed by an assumed mechanism

For a thermally activated process modeled by an Arrhenius relation, a common time-acceleration expression is:

```text
AF_M = exp[(Ea_M / k) × (1/T_use - 1/T_stress)]

t_equiv,M = t_stress × AF_M
```

The subscript `M` matters.

The Intel example uses an activation energy of 1.1 eV and obtains an acceleration factor of 22.76 from 40 °C to 66 °C. That reproduces the 96-hour stress-bake mapping to 2,190 hours at 40 °C for the high-activation-energy mechanism being modeled.

But if a second mechanism has another effective activation energy or changes direction because of recovery/annealing, the same stress dwell does **not** acquire the same equivalent-time interpretation.

Therefore:

```text
96 h at 66 °C
    == about 2,190 h at 40 °C
```

is incomplete unless the mechanism/model assumptions are carried with the statement.

A safer representation is:

```text
96 h at 66 °C
    --under the 1.1 eV high-Ea Arrhenius model used by Intel-->
about 2,190 h at 40 °C
```

## 2.2 Qualification equivalence is not universal thermodynamic age

A qualification procedure can legitimately use an accelerated condition to obtain evidence for a specified service requirement without asserting that every microscopic state variable follows one universal clock.

The useful distinction is:

```text
qualification-equivalent exposure
    != microscopic-state equivalence
    != universal "SSD age"
```

The first is a test-contract concept. The second would require evidence that all material state relevant to future correctness is the same. Intel's ICL/SILC discussion explicitly prevents treating those two propositions as interchangeable.

## 2.3 A retention qualification point is a tuple, not a scalar duration

Case 76 already grounds the JESD218 relation between workload-qualified endurance and later power-off retention. This packet makes the temperature/model part explicit.

A useful engineering tuple is:

```text
Q = (
    prior endurance / wear state,
    wear-generation history,
    retention power state,
    retention temperature,
    retention duration,
    physical mechanism model,
    UBER / functional acceptance criteria
)
```

Changing one member does not preserve the same claim automatically.

Thus:

```text
3 months
```

without temperature and wear boundary is not the same qualification claim, and:

```text
96 hours
```

without its stress temperature and mechanism model is not the same accelerated evidence.

## 2.4 Stress temperature can have opposite directional effects on different state variables

Intel's note gives a particularly useful counterexample to monotonic thinking.

During storage:

```text
higher T
    -> faster ICL
    -> worse ICL-driven retention margin
```

But for some damage/trap populations associated with SILC and P/E cycling:

```text
higher T
    -> stronger recovery / annealing
    -> potentially less of that damage population
```

Therefore the shortcut:

```text
hotter always means strictly more retention aging in every relevant sense
```

is not supported by this source.

This does not imply that heating an SSD is beneficial. It means only that a multi-mechanism reliability state cannot be reduced to a single monotonic temperature-age coordinate without evidence.

## 2.5 Test acceleration and field prediction are different inference steps

The Intel note uses acceleration to build a qualification method. A field-life prediction adds further assumptions:

```text
qualification stress result
    + field temperature distribution
    + field write / P-E history
    + controller behavior
    + mechanism mixture
    + population statistics
    -> field prediction
```

A qualification pass alone therefore does not yield a context-free statement such as:

```text
this SSD will retain arbitrary data for exactly N months in every deployment
```

Case 76 should retain the distinction between a standardized service boundary and a universal physical lifetime claim.

---

# 3. Functional analogy

These analogies describe **relations**, not common implementation genealogy.

## 3.1 Case 111 — powered maintenance duration is not accelerated passive dwell

Case 111 documents SSD cases in which powered background maintenance can refresh media over a nontrivial duration.

That mechanism has a different causal structure from the Case 76 accelerated bake:

```text
Case 76 accelerated retention dwell
    -> passive physical evolution under a qualification condition

Case 111 powered maintenance
    -> controller/device executes maintenance while powered
```

A period of powered refresh opportunity must not be converted into an Arrhenius-equivalent unpowered storage age merely because both use units of hours or days.

## 3.2 OCP/datacenter product profiles are requirement surfaces, not physics models

The existing Case 76 OCP deepening records later datacenter/NVMe retention requirement profiles and named product-contract evidence.

That evidence belongs to a different layer:

```text
service / qualification requirement
    != mechanism-specific acceleration model
```

The recurrence of a three-month / 40 °C product-level retention statement does not by itself establish that every underlying NAND generation has the same ICL/SILC balance, activation energies, or controller margin.

## 3.3 Cross-case lesson: equal elapsed time need not mean equal retained state

Across the repository, several cases already distinguish wall-clock duration from the state transitions occurring during that duration. Case 76 contributes a physical qualification form of the same structural lesson:

```text
same elapsed time
    + different temperature / wear / mechanism
    != same retention evidence
```

This is a functional comparison only.

---

# 4. Philosophical interpretation

The narrow philosophical interpretation is that **retention time is indexed**.

A statement such as “the data lasts three months” appears scalar, but engineering meaning depends on a relation among a medium state, a temperature history, a power state, a prior-wear history, a failure criterion, and a model connecting test conditions to use conditions.

The retained object is therefore not adequately described by duration alone.

This is a project-level interpretation, not terminology attributed to Intel or JEDEC.

---

# 5. Evidence-strength table

| Claim | Evidence strength | Boundary |
| --- | --- | --- |
| Intel's 2012 note distinguishes ICL and SILC | strong primary manufacturer source | does not establish invention priority |
| ICL is described as strongly thermally activated | strong primary manufacturer source | specific quantitative behavior still depends on device/process |
| Intel's Arrhenius example uses `Ea = 1.1 eV` | strong primary manufacturer source | model parameter is not universal for all mechanisms |
| 40 °C / 2,190 h maps to 66 °C / 96 h in Intel's high-Ea example | strong primary manufacturer source | equivalence is model-conditioned |
| Intel describes SILC as about `0.2 eV` and capable of annealing around 55 °C | strong primary manufacturer source | not a universal threshold for all NAND generations |
| High-T bake generally cannot emulate SILC use conditions by the same simple acceleration | strong primary manufacturer source | does not mean SILC is absent from high-T tests |
| A qualification exposure is not universal physical age | engineering reconstruction directly constrained by source | not a quoted Intel/JEDEC phrase |
| Retention qualification should be represented as a tuple of wear, temperature, time and criterion | engineering reconstruction | conceptual model, not historical vocabulary |

---

# 6. Explicit non-claims

This evidence packet does **not** claim:

1. that JESD218/JESD218A is invalid because more than one physical mechanism exists;
2. that every NAND retention mechanism follows `Ea = 1.1 eV`;
3. that 66 °C for 96 hours is universally equivalent to three months at 40 °C for every mechanism or every SSD;
4. that SILC always anneals away completely at 55 °C;
5. that elevated temperature is generally beneficial for SSD retention;
6. that the Intel 2012 note establishes the invention priority of ICL, SILC, accelerated retention testing, or the Arrhenius method;
7. that a standardized retention qualification point is the same as a product's exact field lifetime;
8. that two products publishing the same retention service interval necessarily use the same NAND, controller margin, or physical model;
9. that later OCP/NVMe product requirements descend technically from this Intel note;
10. that a passive high-temperature dwell is functionally identical to powered media refresh or scrubbing.

---

# 7. What this closes

This packet closes a previously loose shortcut inside Case 76:

```text
accelerated retention time
    -> one universal equivalent-age number
```

The better bounded statement is:

```text
specified stress temperature + dwell
    -> evidence under a stated acceleration model
    -> for the mechanism / criterion that model is intended to cover
```

Intel's own 2012 discussion is unusually useful because it places the counterexample next to the worked acceleration calculation: ICL is used for the high-Ea Arrhenius mapping, while SILC is treated separately because its temperature dependence and annealing behavior differ.

---

# 8. Remaining debt

The highest-value follow-up work is now narrower:

- directly compare retained normative wording across public/archived JESD218 revisions instead of relying on Intel's paraphrase for the A-revision details;
- find multi-temperature, post-cycling experimental datasets that separately quantify ICL and SILC contribution over time;
- identify how later TLC and QLC qualification methods partition high-Ea and low-Ea failure mechanisms;
- distinguish NAND-component-level retention qualification from SSD-level controller-inclusive qualification in later generations;
- find product or qualification reports that expose the actual acceptance telemetry around accelerated retention, rather than only the final service contract;
- compare field temperature/write-history distributions with qualification assumptions without treating qualification as a literal lifetime simulator.

No maturity promotion is justified by this packet alone. Case 76 remains **`grounded`**.