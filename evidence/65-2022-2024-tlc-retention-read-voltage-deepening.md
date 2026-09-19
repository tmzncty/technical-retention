# Case 65 Deepening — Direct 3D-TLC Retention / Read-Voltage Evidence (2022–2024)

## Status

**`bounded deepening complete`** for the narrow question addressed here: direct TLC-generation evidence that retention-after-cycling changes the read-voltage problem, and that later retention results can depend on prior P/E history, temperature, and operation timing.

This record deepens [`../cases/65-3d-nand-early-retention-loss-age-aware-reading.md`](../cases/65-3d-nand-early-retention-loss-age-aware-reading.md).

It closes only part of the canonical case's former debt for **direct TLC/QLC measurements rather than carrying forward a 2018 MLC projection**. The TLC half is now directly witnessed by peer-reviewed 2022 and 2024 records. QLC remains open.

---

## Purpose

Case 65 was originally grounded around Luo et al.'s 2018 characterization of real 3D NAND MLC chips, their Retention Model Aware Reading (`ReMAR`) proposal, and the same paper's retention-interference / `ReNAC` work. That record deliberately refused to project the measured MLC behavior quantitatively into later TLC or QLC devices.

The remaining question for this slice is narrower:

> do later peer-reviewed measurements directly show that 3D **TLC** retention/cycling state changes the read-reference problem, without assuming that the 2018 MLC curves simply carry forward?

Two sources answer that bounded question from different directions:

1. a 2022 IEEE Silicon Nanoelectronics Workshop paper directly characterizes threshold distributions and optimal read voltages under retention-after-cycling in TLC 3D NAND and proposes a model for predicting optimal-read-voltage shift;
2. a 2024 peer-reviewed Micromachines paper directly tests raw 64-layer 3D charge-trap TLC NAND and includes a 24-hour data-retention experiment after heavy cycling under controlled prior program/erase timing and temperature histories.

Neither source is used to prove QLC behavior, named commercial-controller deployment, ReMAR ancestry, or one universal 3D-NAND retention law.

---

## Related-repository check

Fresh searches of `tmzncty/computing-archaeology` for `TLC 3D NAND` and for the exact 2022 title exposed no dedicated reusable packet.

Accordingly this file keeps only the retention-specific seam:

```text
TLC physical / wear / temperature history
    -> threshold-distribution / error evolution
    -> changing read-reference problem
    -> bounded model / policy implications
```

Broader 3D-NAND architecture, BiCS/V-NAND genealogy, TLC product generations, process integration, controller history, and commercial adoption remain `computing-archaeology` work if later developed.

---

## Sources inspected

### Source A — 2022 IEEE SNW: TLC retention-after-cycling and optimal read voltage

**Type:** `H/P` — primary peer-reviewed conference paper record, inspected through IEEE Xplore's publication metadata and abstract.

Hongzhe Lin, Yifan Guo, Yifang Xi, Yachen Kong, Xuepeng Zhan, Jiezhi Chen, **“Optimal Read Voltages of Retention-after-Cycling in Triple-level-cell (TLC) 3D NAND Flash Memory and its High-precision Modeling Method,”** 2022 IEEE Silicon Nanoelectronics Workshop (SNW), 11–12 June 2022, DOI `10.1109/SNW56633.2022.9889070`.

Primary publisher record:

- https://ieeexplore.ieee.org/document/9889070/

The abstract directly states that the work characterizes threshold-voltage distributions of multiple programmed states and optimal read voltages in **TLC 3D NAND** under retention-after-cycling. It then distinguishes its proposed low-latency mathematical prediction of optimal-read-voltage shift (`ORVS`) from a traditional search-based read-retry strategy.

The authors report evaluation across multiple cycling and retention conditions. One explicit abstract-level result is a reported **96.6% prediction accuracy** for blocks at **8k P/E cycles** after **335 hours at 55 °C** retention.

Evidence boundary: the public abstract is enough to establish direct TLC retention/cycling characterization plus a model-predicted read-voltage-shift result. It is **not** enough to reconstruct every state-by-state curve, controller implementation detail, model coefficient, or full experimental protocol. Those are not invented here.

### Source B — 2024 Micromachines: raw 64-layer 3D CT TLC, operation history, and 24-hour retention

**Type:** `H/P` — primary peer-reviewed article with openly inspectable methods/results text.

Xuesong Zheng, Yifan Wu, Haitao Dong, Yizhi Liu, Pengpeng Sang, Liyi Xiao, Xuepeng Zhan, **“Impact of Program–Erase Operation Intervals at Different Temperatures on 3D Charge-Trapping Triple-Level-Cell NAND Flash Memory Reliability,”** *Micromachines* 15(9), 1060, published 23 August 2024, DOI `10.3390/mi15091060`.

Primary / institutional-access records:

- https://www.mdpi.com/2072-666X/15/9/1060
- https://pubmed.ncbi.nlm.nih.gov/39337720/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC11434188/

The methods identify an FPGA-based raw-NAND tester and a **128 Gbit charge-trap 3D TLC NAND** device with **64 stacked layers**, 5,912 valid blocks, 768 logical pages per block, and 18,336 bytes per page. The tester supports operation from 25 °C to 85 °C.

The experiment varies two timing intervals while keeping the total operation period at 0.1 s:

- `Ters`: Erase -> next Program interval;
- `Tpgm`: Program -> next Erase interval;
- the two compared pairs are `0.01 s / 0.09 s` and `0.09 s / 0.01 s`.

The study examines fresh state through **10k P/E cycles**, separates program-disturb, read-disturb, and data-retention processes, and records the eight TLC threshold states (`H, A, B, C, D, E, F, G`).

For the retention path specifically, the authors perform repeated reads immediately after the preceding program-disturb process and continue the data-retention observation to **24 hours**. Figure 9 reports 24-hour retention results after **10k P/E cycles** under the different prior operation intervals and at 25 °C / 85 °C.

The text reports that the resulting fail-bit counts (`FBCs`) differ according to the prior program-disturb temperature/history. In the room-temperature prior-history case, the longer `Tpgm` condition shows lower FBC than the longer `Ters` condition; the authors discuss charge redistribution/loss through lateral or vertical charge migration as the bounded physical explanation for that result. For the high-temperature prior-history case, the two operation-interval conditions are reported as similar during the 24-hour retention experiment, with charge loss dominant in the retention process.

The paper's own conclusion is broader than retention alone: operation interval, operating temperature, and P/E cycling jointly affect the observed TLC reliability/error regime. This record uses that result only to constrain the retention/history relation, not to turn program disturb, read disturb, and retention into one failure mechanism.

---

## Historical record

### H/P — direct TLC retention/read-reference evidence exists by 2022

The 2022 IEEE paper removes the need to infer the existence of a retention-dependent read-reference problem in TLC solely from Luo et al.'s 2018 MLC population.

The historically safe statement is now:

```text
2018
real 3D NAND MLC characterization
    -> early retention / changing optimal read reference
    -> ReMAR research proposal

2022
peer-reviewed TLC 3D NAND characterization
    -> retention-after-cycling threshold distributions
    -> optimal read voltages
    -> ORVS prediction model
```

This is a chronology of inspected publications, not a genealogy claim.

### H/P — the 2022 paper directly couples wear and retention in the read-voltage problem

The source is not merely a generic TLC paper. Its title and abstract both make `retention-after-cycling` the condition under which threshold distributions and optimal read voltages are studied.

The bounded relation is therefore:

```text
P/E-cycling state
    + retention exposure
    -> threshold-distribution condition
    -> optimal read-voltage condition
```

The paper's reported 8k-P/E / 335 h at 55 °C result is evidence that the proposed model was evaluated in a heavily cycled, retained TLC regime.

It is not a claim that every 8k-cycle TLC device has the same distribution, that 335 hours is a retention specification, or that 55 °C is a universal acceleration condition.

### H/P — a later raw-TLC experiment makes prior operation history part of the observed retention result

The 2024 paper tests a concrete raw 64-layer charge-trap TLC device and intentionally varies earlier program/erase timing and temperature before the 24-hour retention measurement.

This directly demonstrates a history-conditioned experiment:

```text
same broad TLC medium class
    + different prior P/E timing / temperature condition
    -> different later measured error population
```

The source therefore blocks a shortcut in which `retention time` is treated as the only relevant descriptor of the retained cell population.

### H/P — TLC multi-state error direction is itself structured

The 2024 study represents TLC using eight threshold states and separates observed errors into threshold-voltage **downshift** and **upshift** directions. It reports that the dominant direction differs between room-temperature and high-temperature program-disturb regimes.

For this repository, the important retention-side consequence is limited:

> `raw error count` is not necessarily one homogeneous physical event class.

A controller or reliability model may need to distinguish how a distribution moved rather than merely know that the aggregate count increased.

This does not authorize the repository to assign every upshift/downshift bit to one microscopic mechanism in an arbitrary product.

---

## Engineering reconstruction

### E — TLC closes a former generation-transfer gap, but does not erase generation specificity

Before this deepening, Case 65 could safely say that the 2018 MLC work projected greater future importance for narrower-margin TLC/QLC, but it could not substitute that projection for measured later-generation evidence.

The 2022 and 2024 records now support:

> **direct TLC evidence exists for retention-conditioned threshold/read-voltage behavior.**

They do **not** support:

> **the exact 2018 MLC early-retention curve is quantitatively portable to TLC.**

The distinction is important:

```text
mechanism class recurs
    !=
curve shape / coefficient / threshold recurs unchanged
```

### E — retained state age is not a sufficient state descriptor

Case 65 already separates retention age from P/E history, word-line/process context, neighbor state, and controller metadata.

The 2024 experiment strengthens that separation with a direct TLC history witness. A later 24-hour retention result can depend on conditions established before the 24-hour clock begins.

Thus:

```text
elapsed retention time
    !=
complete physical-history state
```

and:

```text
current read time
    - current program time
    !=
all context relevant to present read margin
```

For a bounded TLC population, prior P/E cycling, operation timing, and temperature history can condition the later error distribution.

### E — a model can replace some online search without becoming the retained payload

The 2022 paper contrasts model-based ORVS prediction with traditional search-based read retry.

That yields a useful controller-layer distinction:

```text
aged TLC physical distribution
    !=
optimal read boundary
    !=
method used to discover / predict that boundary
```

A model that predicts a read-voltage shift is interpretation/control machinery. It is not the user payload, and it does not physically restore leaked charge.

Therefore:

> **read-voltage prediction != physical refresh.**

And:

> **model accuracy != payload-retention guarantee.**

The reported 96.6% figure is prediction accuracy under one reported experimental condition, not an end-to-end uncorrectable-bit-error probability or a commercial SSD reliability guarantee.

### E — prior operation history can change later maintenance/read policy without being stored as a literal event log

The 2024 paper controls history experimentally. It does not demonstrate that a commercial controller retains a complete log of every erase/program interval and temperature.

The engineering lesson must therefore be phrased carefully:

> a variable can be physically history-dependent even when the device does not preserve a literal metadata record of that history.

This mirrors the broader repository distinction between **state depends on history** and **system archives history**.

### E — direct TLC measurement does not close the deployment question

Both sources are device/research evidence. Neither proves that a named shipping SSD implements ReMAR, the 2022 ORVS model, or a controller policy derived from the 2024 experiment.

So:

```text
measured TLC behavior
    -> supports a policy problem

!=
measured commercial-controller policy
```

The canonical deployment debt remains open.

---

## Functional comparison

### A — versus Luo et al. 2018 ReMAR

The safe common structure is:

```text
retained NAND distribution evolves
    -> default/fixed read boundary becomes less optimal
    -> read interpretation can be adapted
```

The differences matter:

- 2018 ReMAR is grounded in a specific real-3D-NAND MLC characterization and uses estimated data age plus P/E state;
- 2022 directly studies TLC retention-after-cycling and proposes a mathematical ORVS predictor;
- 2024 directly studies raw 64-layer TLC and shows that prior operation timing / temperature can condition later error outcomes.

Therefore:

> **similar read-adaptation problem != same algorithm.**

> **later TLC evidence != proof of ReMAR descent or deployment.**

### A — versus Case 36 physical refresh

Case 36 can renew physical NAND margin by rewrite/remap.

This Case-65 slice instead concerns better characterization or interpretation of the current TLC embodiment.

```text
choose / predict a better read voltage
    !=
rewrite charge state
```

The two can be composed in a real controller, but composition is not identity.

### A — versus Case 52 read disturb and Case 59 program interference

The 2024 paper studies program-disturb, read-disturb, and data-retention processes within one experimental program, but that does not collapse them into one mechanism.

A retained population may carry physical consequences of earlier operations into a later retention experiment while the causal categories remain distinct.

Thus:

> **one device history can compose multiple stress mechanisms without making those mechanisms synonymous.**

### A — versus Case 132 temperature-conditioned serial-Flash retention

Case 132 separates storage temperature, active operability, and retention qualification. This Case-65 TLC slice adds a different boundary: temperature can be part of the **preceding operating history** that changes the later error distribution.

The shared functional lesson is only:

> environmental history can condition future recoverability.

The device populations, temperature ranges, retention procedures, and physical mechanisms are different.

---

## Philosophical interpretation — bounded

### I — the age of an object is not always the same as its technical history

The technical record supports a narrow interpretive point:

> two retained objects with the same elapsed retention age need not have the same present recovery margin if their prior wear, temperature, operation timing, spatial context, or neighbor context differs.

This is useful for the repository because it prevents `time since write` from becoming a universal scalar theory of retention.

The historical actors are not attributed a philosophy of memory. The claim is an engineering-disciplined project interpretation.

### I — evidence for persistence can itself be model-mediated

The 2022 result also reinforces a distinction already visible elsewhere in the repository:

```text
physical state
    !=
model of that state
    !=
decision made from the model
```

A more accurate prediction of an optimal read boundary can improve recoverability without making the physical payload younger or less worn.

---

## Explicit non-claims

This deepening does **not** claim:

1. that the 2022 paper invented adaptive read voltage, read retry, retention modeling, or TLC NAND;
2. that the 2024 paper invented operation-history-aware NAND reliability analysis;
3. that the 2018 MLC measurements and 2022/2024 TLC measurements are quantitatively interchangeable;
4. that the 2022 `96.6%` model-prediction figure is a data-retention success probability;
5. that `335 h @ 55 °C` is a product retention specification or a universal acceleration equivalent;
6. that an 8k-P/E research block corresponds to every shipping TLC product's rated life;
7. that the 2024 `10k P/E` condition is a recommended commercial operating point;
8. that 24-hour laboratory retention proves long-term archival retention;
9. that high-temperature prior history universally improves later TLC retention;
10. that every upshift or downshift error in arbitrary TLC products has the same microscopic cause;
11. that program disturb, read disturb, and retention are the same mechanism;
12. that prior-history dependence implies a controller stores a complete event history;
13. that either source demonstrates QLC behavior;
14. that either source demonstrates a named retail SSD/controller running ReMAR;
15. that the 2022 ORVS predictor is ReMAR;
16. that the 2022 work descends from or influenced the 2018 work beyond ordinary citation/field context without separate genealogy evidence;
17. that the 2024 work proves sudden-power-loss consistency of age/tracking metadata;
18. that read-voltage adaptation restores leaked physical charge;
19. that lower FBC under one laboratory path proves more residual physical charge in every cell;
20. that a model reducing read search latency necessarily improves total SSD lifetime;
21. that a raw-chip tester reproduces every controller/ECC/FTL behavior of an SSD;
22. that findings from one 64-layer 128-Gbit TLC device are universal across later layer counts, vendors, floating-gate designs, or QLC;
23. that QLC's narrower state spacing can be treated as measured here merely because the papers discuss multi-bit NAND context;
24. that the canonical Case 65 named-product deployment debt is closed;
25. that this slice replaces broader TLC/3D-NAND technical history in `computing-archaeology`.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| 2022 IEEE SNW directly characterizes retention-after-cycling threshold distributions and optimal read voltages in TLC 3D NAND | `H/P` | primary peer-reviewed abstract / publisher record |
| the 2022 work proposes mathematical prediction of optimal read-voltage shift rather than only search-based retry | `H/P` | primary abstract |
| 96.6% prediction accuracy is reported for 8k-P/E blocks after 335 h at 55 °C | `H/P` | primary abstract; bounded condition |
| 2024 work uses a raw 128-Gbit, 64-layer charge-trap TLC NAND device and FPGA tester | `H/P` | directly inspectable methods text |
| 2024 work examines fresh through 10k P/E states at 25 °C and 85 °C | `H/P` | directly inspectable methods/results |
| 2024 work performs a data-retention path out to 24 h after the preceding stress history | `H/P` | directly inspectable methods + Figure 9 description |
| after 10k P/E, the 24 h retention FBCs differ across some prior timing/temperature histories | `H/P` | directly inspectable results; source-bounded |
| direct TLC evidence now exists, so TLC need not be represented only as a projection from the 2018 MLC paper | `E` | bounded synthesis of 2022/2024 primary records |
| same elapsed retention time can correspond to different recovery margin when prior history differs | `E` | bounded reconstruction from the controlled 2024 histories |
| read-voltage prediction is physical charge restoration | `X` | explicitly unsupported |
| the 2022 96.6% value is an end-to-end retention probability | `X` | wrong metric |
| QLC is directly measured by these two sources | `X` | not established |
| either source proves ReMAR/ReNAC commercial deployment | `X` | not established |
| recurrence of age-/history-conditioned read adaptation proves genealogy | `X/A` | functional similarity only |
| technical age can be multidimensional rather than one scalar elapsed-time variable | `I` | bounded project interpretation after H/E record |

---

## Resulting bounded distinctions

```text
MLC early-retention evidence
    !=
TLC direct measurement
    !=
QLC direct measurement

retention time
    !=
P/E wear state
    !=
prior operation interval
    !=
prior temperature history

threshold distribution
    !=
optimal read boundary
    !=
method used to find/predict that boundary

model prediction accuracy
    !=
logical read success probability
    !=
retention guarantee

read-voltage adaptation
    !=
physical rewrite / refresh

history-dependent physics
    !=
persisted literal history log

research-device result
    !=
named commercial-controller deployment
```

---

## What this closes in Case 65

The canonical remaining-work item:

> `direct TLC/QLC measurements rather than carrying forward the 2018 projection`

can now be narrowed to:

> **direct QLC measurements remain open; direct TLC retention/read-voltage evidence is now grounded by 2022/2024 peer-reviewed measurements.**

This is evidence deepening, not a maturity promotion. Case 65 should remain `grounded`.

---

## Remaining work after this slice

- direct **QLC** measurements of retention-age/read-reference evolution;
- direct TLC/QLC measurements that specifically reproduce or reject the 2018 front-loaded early-retention curve shape across named generations;
- named shipped controller/product evidence for ReMAR-like age-aware read tracking;
- named shipped controller/product evidence for ReNAC-like neighbor-aware recovery;
- firmware/command traces showing controller selection of retention-conditioned read offsets after ECC stress;
- interaction with LDPC soft decoding, multi-step read retry, and read reclaim in a named product;
- sudden-power-loss consistency of persisted age/tracking metadata;
- evidence for how age/reference state follows FTL relocation, refresh, or garbage collection;
- broader TLC/QLC generation/process/controller history in `computing-archaeology` rather than duplicated here.

---

## Source-custody note

The 2022 claims in this record are intentionally limited to what is exposed by the IEEE publisher record/abstract. No unavailable full-text figure or model coefficient is reconstructed from secondary summaries.

The 2024 claims are taken from the openly inspectable article methods/results and PubMed/PMC bibliographic record. It is used as a raw-device research witness, not as a commercial SSD product specification.
