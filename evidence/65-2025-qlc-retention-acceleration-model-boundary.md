# Case 65 Deepening — 2025 QLC Retention Acceleration-Model Boundary

## Status

**`bounded deepening complete`** for one narrow question that remained under-specified after the 2019–2024 QLC evidence packet:

> When high-temperature testing is used to stand in for longer low-temperature QLC retention time, is the resulting time mapping itself a fixed physical fact, or is it a model-dependent relation whose parameters can vary with device condition?

The 2025 IEEE TCAD paper by Shaoqi Yang et al., **“Retention Accelerated Testing for 3-D QLC NAND Flash Memory: Characterization, Analysis, and Modeling,”** supplies a direct QLC-generation witness that the conventional fixed-parameter Arrhenius treatment can be inaccurate for the tested 3D charge-trap QLC regime. Its published abstract reports an empirical model with a changing **apparent activation energy (`Ea`)**, a temperature- and cycle-related `Ea` parameter table, a measured mapping between 40 °C retention time and other temperatures, and a maximum error reduction of approximately 70% relative to the classic Arrhenius model in the authors' evaluation.

This packet is intentionally **abstract-bounded**. The publisher full text was not available through an inspectable public path in this research pass. It therefore does not invent the tested vendor, layer count, exact P/E points, exact temperature set, detailed fitting equations, per-state curves, sample count, confidence intervals, or the meaning of every error metric beyond what the published abstract exposes.

The result is still useful for `technical-retention`, because it separates the **retention phenomenon** from the **clock-conversion model used to infer one retention interval from another**.

## Navigation

- canonical case: [`../cases/65-3d-nand-early-retention-loss-age-aware-reading.md`](../cases/65-3d-nand-early-retention-loss-age-aware-reading.md)
- prior direct-QCL generation packet: [`65-2019-2024-qlc-retention-read-threshold-deepening.md`](65-2019-2024-qlc-retention-read-threshold-deepening.md)
- direct TLC packet: [`65-2022-2024-tlc-retention-read-voltage-deepening.md`](65-2022-2024-tlc-retention-read-voltage-deepening.md)
- early-retention / ReMAR grounding: [`65-3d-nand-2010-2018-early-retention-grounding.md`](65-3d-nand-2010-2018-early-retention-grounding.md)

## Scope

This slice asks only about **accelerated-retention inference**:

```text
high-temperature observation interval
    -> model / parameterization
    -> inferred lower-temperature retention interval
```

It does **not** ask whether:

- one particular commercial SSD meets a warranty or JEDEC retention requirement;
- the tested QLC device is representative of every QLC generation;
- a controller ships the authors' empirical model;
- the 2025 model is ReMAR;
- changing `Ea` is itself a physical refresh mechanism;
- an accelerated-test conversion is the same thing as elapsed wall-clock age stored by a controller;
- a better lifetime model restores charge or repairs a page;
- the conventional Arrhenius equation is generally invalid for all nonvolatile memories.

The bounded object is the **validity and state-dependence of the conversion relation used by a retention-acceleration experiment**.

## Source roles and custody

### Source A — Yang et al., IEEE TCAD 2025

Shaoqi Yang, Meng Zhang, Xuepeng Zhan, Peng Guo, Xiaohuan Zhao, Guangkuo Yang, Xinyi Guo, Jixuan Wu, Fei Wu, Jiezhi Chen, **“Retention Accelerated Testing for 3-D QLC NAND Flash Memory: Characterization, Analysis, and Modeling,”** *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems* 44(7), 2025, pp. 2779–2788, DOI `10.1109/TCAD.2025.3526055`.

The DOI-indexed publication record identifies a peer-reviewed IEEE journal article. Accessible copies of the published abstract report that:

- the study analyzes data-retention properties of **3-D QLC NAND flash memory**;
- the conventional Arrhenius model is inaccurate in the bounded analyzed regime;
- an empirical model varies **apparent activation energy (`Ea`)** according to other parameters;
- the model supplies a **temperature- and cycle-related `Ea` parameter table** for high-temperature accelerated testing;
- the authors observe a linear connection between **40 °C data-retention-time mapping** and other temperatures; and
- in their evaluation, the modified model reduces error by **approximately 70% at maximum** relative to the classic Arrhenius model.

**Evidence role:** peer-reviewed publication/abstract-level historical and engineering evidence.

**Custody limit:** the IEEE full text was not inspectable in this pass. Claims are therefore limited to the published abstract and bibliographic record. A third-party article that supplies additional experiment details was found but is **not** used here as authority for layer count, tester identity, exact temperature points, detailed curves, or parameter values.

### Source B — Sciacca, Kosuru, Papandreou, IEEE EDTM 2024

M. Dean Sciacca, Trinadhachari Kosuru, Nikolaos Papandreou, **“Cycling Condition Impacts on 3D QLC NAND Reliability,”** *EDTM 2024*, DOI `10.1109/EDTM58488.2024.10511536`.

IBM Research's institutional record says that this work evaluates data retention in state-of-the-art 3D charge-trap QLC and characterizes RBER and optimal-read-voltage offsets under different P/E counts, dwell times, and cycling temperatures.

**Evidence role here:** controlled comparison only. It establishes that QLC retention behavior is conditioned by more than nominal elapsed retention time, but this packet does not claim that Sciacca et al. and Yang et al. use the same model, device, or test protocol.

### Source C — Wang et al., IEEE IMW 2019

Kunliang Wang, Gang Du, Zhiyuan Lun, Xiaoyan Liu, **“The Method of Predicting Retention Threshold Voltage Distribution for NAND Flash Memory Based on Back-Propagation Neural Network,”** *IEEE IMW 2019*, DOI `10.1109/IMW.2019.8739277`.

The Peking University institutional record covers 3-D TLC and QLC measured retention-conditioned threshold-voltage distributions and read-voltage optimization.

**Evidence role here:** controlled comparison only. A model that predicts the **distribution/read boundary** is not the same object as a model that converts **accelerated test time across temperatures**.

## Historical record

### H-65A.1 — accelerated-retention modeling remains an active QLC problem in 2025

The 2025 paper's title and abstract explicitly place **retention accelerated testing** itself at the center of a modern 3D QLC study.

That matters historically because high-temperature testing is not merely an invisible laboratory convenience in this record. The validity of the time-conversion model is itself treated as an engineering problem.

Minimum safe historical claim:

> **By 2025, peer-reviewed 3D QLC work explicitly reported that a conventional Arrhenius retention-acceleration model could be inaccurate for the tested regime and proposed a condition-dependent apparent-activation-energy model instead.**

This is not a claim that Arrhenius acceleration was first questioned in 2025. Earlier charge-trap and nonvolatile-memory literature already discusses non-Arrhenius or multiple-activation-energy behavior. That broader genealogy belongs in `computing-archaeology` if developed.

### H-65A.2 — the paper does not treat `Ea` as one context-free constant

The abstract describes a **temperature- and cycle-related parameter table for `Ea`**.

Therefore, at the source-vocabulary layer:

```text
one fixed apparent activation energy
    !=
conditioned apparent activation energy used by the proposed model
```

The exact table entries and functional form are outside this packet because the full text was not inspected.

### H-65A.3 — the reported object includes an explicit time-mapping relation

The abstract reports a linear connection between **40 °C data-retention-time mapping** and the other tested temperatures.

The source therefore directly supports a distinction between:

```text
observed test time at temperature T
    !=
modeled equivalent retention time at 40 °C
```

The right side is an inferred relation produced by a model/empirical mapping, not simply another label for the left side.

## Engineering reconstruction

### E-65A.1 — retention time and accelerated-test equivalent time are different state variables

A physical cell experiences an actual temperature history for an actual duration. An accelerated test then uses a model to infer what that observation means for another temperature/time regime.

Therefore:

```text
actual bake / observation interval
    !=
model-derived equivalent retention interval
```

This seems obvious mathematically, but it is technically important for retention claims. If the conversion relation is wrong, the measured physical behavior may be real while the **inferred long-horizon lifetime** is wrong.

That yields a useful retention chain:

```text
physical QLC state under test
    -> measured retention observable
    -> acceleration model + calibrated parameters
    -> equivalent-time estimate
    -> lifetime / qualification interpretation
```

Each arrow can fail independently.

### E-65A.2 — calibration state can be retention evidence without being payload

The 2025 abstract's temperature- and cycle-related `Ea` table is not user data stored in the NAND page. It is **model/calibration state** used to interpret accelerated-retention evidence.

Thus:

```text
retained user payload
    !=
physical degradation state
    !=
experimental observation
    !=
acceleration-model parameterization
    !=
inferred service-age equivalent
```

This extends Case 65's existing distinction between physical state and read-interpretation metadata into a different layer: **the apparatus used to make claims about retention can itself require stateful calibration.**

Nothing in the abstract establishes that a shipping SSD stores the `Ea` table.

### E-65A.3 — wear condition can enter the time-conversion rule, not only the raw-error curve

Case 65 already contains direct QLC evidence that P/E cycle count, dwell, and cycling temperature condition observed retention/read behavior.

The 2025 paper adds a different relation: its proposed `Ea` parameterization is described as **temperature- and cycle-related**.

Therefore the bounded reconstruction is:

```text
P/E condition
    -> physical retention behavior

and, in the proposed accelerated-test model,

P/E condition + temperature
    -> chosen / inferred apparent-Ea parameterization
    -> equivalent-time mapping
```

The second chain is not the same as the first. The model attempts to describe the first.

### E-65A.4 — model error is not medium corruption

The paper reports that the modified model can reduce error relative to a classic Arrhenius model.

That error is an error of **prediction / mapping / model fit in the tested analysis**, not evidence that the NAND page itself suffered 70% fewer raw bit errors, 70% longer guaranteed retention, or 70% lower UBER.

Therefore:

```text
model-prediction error reduction
    !=
RBER reduction
    !=
ECC-margin restoration
    !=
retention-lifetime extension
```

This distinction is mandatory because all four numbers could colloquially be called an “improvement,” while only the first is supported by the accessible abstract.

### E-65A.5 — an accelerated test is an epistemic shortcut, not a physical fast-forward command

High-temperature acceleration exposes a medium to a different physical condition and uses a model to infer another time regime.

It does not literally cause the device to experience the same complete history it would have experienced during years at a lower temperature.

Therefore:

> **equivalent modeled age ≠ identical physical history.**

This packet does not claim that the authors make this philosophical formulation; it is an engineering stop condition against treating accelerated-equivalent time as a preserved chronological trace.

### E-65A.6 — better acceleration modeling does not close controller-deployment questions

The 2025 paper can improve the evidence base for laboratory lifetime inference while leaving all of these questions open:

- does a shipping controller track data age?
- does it use `Ea` or a temperature/cycle table online?
- does it alter read voltage from that model?
- does it rewrite cold data?
- does it persist model state across firmware update or power loss?

Thus:

```text
laboratory retention model
    !=
firmware retention policy
```

A future source may connect the two, but this paper's accessible record does not.

## Controlled functional comparison

### With Case 65 ReMAR

ReMAR uses retained/estimated data age plus P/E information to improve **read-reference selection** for an existing aged embodiment.

The 2025 accelerated-testing work uses temperature/cycle-conditioned model state to improve **time/lifetime inference** across test conditions.

Safe comparison:

```text
context-conditioned model
    -> stronger interpretation of retention-related evidence
```

Stop condition:

```text
read-reference model
    !=
accelerated-test time-conversion model
```

No genealogy is asserted.

### With the 2019 QLC threshold-distribution model

Wang et al. use a BpNN to predict retention-conditioned threshold-voltage distributions and support read-voltage optimization.

Yang et al. 2025 address the accuracy of retention-acceleration/lifetime mapping.

Therefore:

```text
predict Vth distribution / read boundary
    !=
predict equivalent retention time / lifetime mapping
```

Both are model-mediated interpretations of retention evidence, but the dependent variable and operational role differ.

### With the 2024 IBM QLC cycling-condition evidence

Sciacca et al. show that P/E count, dwell, and cycling temperature matter to measured QLC retention/RBER/read-voltage behavior.

Yang et al. show that temperature and cycle condition also matter to the proposed accelerated-test `Ea` parameterization.

Safe functional synthesis:

> **nominal elapsed retention time alone is not a complete descriptor of either the measured QLC state or the model used to extrapolate that state across test conditions.**

Stop condition: the studies are not assumed to use the same device generation, vendor, sample population, temperature schedule, or calibration equation.

### With JEDEC-style qualification concepts

A qualification standard may specify a retention objective and an acceleration procedure. This packet does **not** import any particular JEDEC activation energy, temperature, or pass/fail criterion into the 2025 experiment unless a directly inspected standard/source says so.

Therefore:

```text
research-model fit
    !=
standards compliance
    !=
product warranty
```

## Failure and forgetting boundaries

This deepening adds a failure mode at the **evidence/model layer** rather than at the cell layer.

Distinct failures now include:

- physical charge/threshold evolution makes data harder to read;
- ECC/read-reference policy can become mismatched to the current distribution;
- retained timing/context metadata can be missing or stale;
- a neighbor-conditioned or age-conditioned recovery model can be wrong;
- an accelerated-retention model can map a high-temperature observation to the wrong lower-temperature equivalent interval;
- a parameter table can be valid only for a bounded wear/temperature/device regime;
- model fit can improve while payload margin continues to degrade physically;
- a model can be historically superseded without any NAND payload bit changing.

Therefore:

```text
failure of retention evidence interpretation
    !=
failure of retained payload
```

But the former can still matter materially: an over-optimistic lifetime inference can lead an engineer to claim a retention margin that the medium does not actually have.

## Historical / engineering / analogy / interpretation ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| a 2025 IEEE TCAD paper directly studies accelerated retention testing in 3D QLC NAND | `H/P` | DOI-indexed peer-reviewed publication record |
| the accessible abstract reports conventional Arrhenius inaccuracy in the bounded analyzed regime | `H/P` | abstract-level only |
| the proposed model varies apparent `Ea` using other parameters | `H/P` | abstract-level only |
| the model exposes a temperature- and cycle-related `Ea` parameter table | `H/P` | abstract-level only; exact table not inspected |
| the abstract reports a linear 40 °C retention-time mapping to other temperatures | `H/P` | abstract-level only; exact tested temperatures not asserted here |
| modified-model error falls by approximately 70% at maximum relative to classic Arrhenius in the authors' evaluation | `H/P` | abstract-level result; metric details require full text |
| equivalent retention time is a model output distinct from actual observation time | `E` | engineering reconstruction from accelerated-testing relation |
| calibration/model state can affect the strength of a retention claim without being user payload | `E` | bounded reconstruction |
| reported 70% model-error reduction means 70% lower RBER or 70% longer retention | `X` | not supported |
| the proposed model physically restores lost charge | `X` | modeling is not rewrite/refresh |
| the paper proves one activation energy is invalid for all NAND or NVM | `X` | source is bounded to analyzed 3D QLC regime |
| the paper proves a named retail SSD ships the model | `X` | deployment not established |
| the paper closes full-text QLC quantitative-debt in Case 65 | `X` | full text was not inspected in this pass |
| accelerated-equivalent age is identical to the medium's complete low-temperature physical history | `X/E` | equivalence is model-bounded, not identity of histories |
| ReMAR, BpNN threshold prediction, and accelerated-time mapping are the same algorithm | `X/A` | only high-level functional comparison is allowed |
| improved model calibration can strengthen retention evidence without altering the retained payload | `I` | bounded philosophical pressure derived from engineering distinction |

## Explicit non-claims

This packet does **not** claim:

1. that the 2025 paper invented Arrhenius testing;
2. that it first discovered non-Arrhenius behavior in charge-trap memory;
3. that one fixed `Ea` is wrong for every NAND device;
4. that `Ea` is a controller counter or user-visible SMART field;
5. that the proposed table is stored on the tested NAND;
6. that the paper identifies a retail SSD model;
7. that the paper identifies every fabrication/process detail in the accessible abstract;
8. that the test population is quantitatively representative of all QLC NAND;
9. that the full article was inspected in this pass;
10. that details from third-party summaries are upgraded into primary evidence;
11. that a linear mapping reported for the tested regime is universally linear;
12. that the reported maximum error reduction applies to every condition;
13. that prediction-error reduction equals bit-error reduction;
14. that prediction-error reduction equals lifetime extension;
15. that accelerated test time equals wall-clock service age;
16. that thermal acceleration reproduces every aspect of low-temperature history;
17. that a better model is a refresh operation;
18. that a better model is an ECC operation;
19. that a better model changes FTL currentness;
20. that model validity proves standards compliance;
21. that model validity proves warranty compliance;
22. that the paper demonstrates ReMAR in a product;
23. that the paper demonstrates ReNAC in a product;
24. that it shares a genealogy with the 2019 BpNN model;
25. that it shares a genealogy with Toshiba's age-aware tracking patents;
26. that the IBM 2024 and Yang 2025 studies use identical QLC generations or protocols;
27. that the source closes the open named-controller deployment question;
28. that it closes sudden-power-loss consistency of retention metadata;
29. that it closes long-horizon raw full-text QLC characterization debt; or
30. that changing an inference model means the older physical measurements were unreal.

## Philosophical interpretation — bounded

The engineering result creates one narrow conceptual pressure:

> **What is retained as evidence of future retention is not exhausted by the state of the medium; it can also depend on the validity of the model that converts present observations into claims about another time regime.**

That is different from saying the model “stores the data.” It does not. The NAND payload and the acceleration model occupy different technical roles.

A second bounded distinction follows:

> **A technical age can be inferred rather than remembered.**

An “equivalent retention time” produced by accelerated testing is not necessarily a timestamp retained by the device. It is a modeled relation between observed conditions and another temporal regime.

This matters to a philosophy of technical retention because it prevents a collapse of:

```text
chronological duration
    ==
physical aging trajectory
    ==
accelerated-test equivalent age
    ==
controller-retained age metadata
```

Those can interact, but they are not one object.

## Bounded conclusion

The 2025 QLC record adds a distinct layer to Case 65:

```text
physical QLC retention evolution
    -> measured high-temperature behavior
    -> temperature / wear-conditioned acceleration model
    -> inferred equivalent retention interval
    -> lifetime / qualification claim
```

The important boundary is:

> **retention phenomenon ≠ retention-acceleration model ≠ inferred retention lifetime.**

Case 65 already shows that the same surviving NAND embodiment can require context-sensitive read interpretation. This packet shows a related but different fact: the **evidence used to characterize retention across time/temperature can also require context-sensitive interpretation**.

The packet does not close the existing full-text QLC debt. Instead it sharpens that debt: future work should inspect the complete Yang et al. paper for the exact device/test population, acceleration temperatures, cycle bins, apparent-`Ea` parameterization, error definition, validation procedure, per-state behavior, and long-horizon extrapolation limits.

## Sources

1. Shaoqi Yang, Meng Zhang, Xuepeng Zhan, Peng Guo, Xiaohuan Zhao, Guangkuo Yang, Xinyi Guo, Jixuan Wu, Fei Wu, Jiezhi Chen, **“Retention Accelerated Testing for 3-D QLC NAND Flash Memory: Characterization, Analysis, and Modeling,”** *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems* 44(7), 2025, pp. 2779–2788, DOI `10.1109/TCAD.2025.3526055`; IEEE record: <https://ieeexplore.ieee.org/document/10824831/>.
2. DOI/bibliographic and abstract cross-check: <https://colab.ws/articles/10.1109%2Ftcad.2025.3526055>. Used only to expose the published abstract where IEEE Xplore's public page was script-gated in this pass.
3. M. Dean Sciacca, Trinadhachari Kosuru, Nikolaos Papandreou, **“Cycling Condition Impacts on 3D QLC NAND Reliability,”** *2024 8th IEEE Electron Devices Technology & Manufacturing Conference (EDTM)*, DOI `10.1109/EDTM58488.2024.10511536`; IBM Research institutional record: <https://research.ibm.com/publications/cycling-condition-impacts-on-3d-qlc-nand-reliability>.
4. Kunliang Wang, Gang Du, Zhiyuan Lun, Xiaoyan Liu, **“The Method of Predicting Retention Threshold Voltage Distribution for NAND Flash Memory Based on Back-Propagation Neural Network,”** *2019 IEEE 11th International Memory Workshop (IMW)*, DOI `10.1109/IMW.2019.8739277`; Peking University institutional record: <https://ir.pku.edu.cn/handle/20.500.11897/544481>.

## Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for the 2025 title, `QLC retention`, and `activation energy` found no dedicated reusable packet.

If a broader genealogy of Arrhenius testing, multiple/non-constant activation-energy models, charge-trap retention acceleration, JEDEC qualification practice, or NAND reliability test equipment is developed, it belongs there. This repository keeps only the retention-specific distinction among physical aging, measured evidence, acceleration-model state, and inferred temporal claim.