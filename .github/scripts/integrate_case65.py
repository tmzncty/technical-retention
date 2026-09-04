from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
CASE_PATH = "cases/65-3d-nand-early-retention-loss-age-aware-reading.md"
EVIDENCE_PATH = "evidence/65-3d-nand-2010-2018-early-retention-grounding.md"

case = r'''# 3D NAND Early Retention Loss: Front-Loaded Charge Loss, Retention Age, and Read-Reference Adaptation

## Status

**`grounded`** — bounded to the retention-specific transition from earlier charge-trapping NAND fast-initial-charge-loss evidence (2010), through a 2016 tube-type 3D NAND early-retention study, to Luo et al.'s extended 2018 experimental characterization of real 3D NAND MLC chips and their **Retention Model Aware Reading (ReMAR)** proposal.

Grounding record: [`../evidence/65-3d-nand-2010-2018-early-retention-grounding.md`](../evidence/65-3d-nand-2010-2018-early-retention-grounding.md).

## Scope

This case asks a narrow question left open by Cases 36, 52, and 59:

> What changes when a nonvolatile 3D charge-trap NAND cell loses a disproportionate amount of retention margin soon after programming, so that the age of the data can become an input to the later read interpretation itself?

The bounded object is **early retention loss / fast initial charge loss** in charge-trapping NAND, with special attention to the 2018 extended-duration characterization of real 3D NAND MLC chips and its age-aware read-reference proposal.

This is **not**:

- a complete history of 3D NAND or charge-trap Flash;
- evidence that every 3D NAND generation, TLC/QLC product, or vendor has the same early-retention curve;
- a claim that 2018 invented fast initial charge loss or first observed early retention in 3D NAND;
- evidence that ReMAR shipped in a named commercial SSD/controller;
- a modern device-specific `read reclaim` case;
- the same mechanism as Case 36's planar-NAND Flash Correct-and-Refresh (FCR), Case 52's read disturb, or Case 59's program interference;
- a claim that retention interference, layer-to-layer process variation, early retention loss, and read disturb are one phenomenon.

The 2018 authors characterize chips from a major vendor but do not identify the vendor/product. Numerical results therefore remain bounded to their test population and model assumptions.

## Historical vocabulary and chronology

### `fast initial charge loss` before the 2018 3D-NAND characterization

C.-P. Chen and colleagues' IEDM 2010 paper is titled **“Study of fast initial charge loss and its impact on the programmed states Vt distribution of charge-trapping NAND flash.”** Its published record places `fast initial charge loss` explicitly in charge-trapping NAND well before the 2018 ReMAR work.

This matters for priority:

> **2018 extended 3D-NAND characterization ≠ invention of fast initial charge loss in charge-trapping NAND.**

The 2010 result is used as prior art only. This repository does not project the later 3D device organization, ReMAR policy, or 24-day experimental curve backward onto that paper.

### `early retention` in tube-type 3D NAND by 2016

Bongsik Choi and colleagues' 2016 VLSI Technology paper uses **`early retention`** for fast charge loss within seconds in tube-type, word-line-stacked 3D NAND. Its abstract reports measurements from microseconds to seconds and attributes the bounded behavior mainly to lateral charge loss through shared charge-trap layers, with sensitivity to program/erase levels.

The authors frame this as the first observation of early retention in their tube-type 3D NAND regime. The present repository keeps that claim source-bounded rather than upgrading it into a universal invention claim.

This establishes a second priority boundary:

> **2018 24-day study ≠ first 3D-NAND early-retention observation.**

### Extended-duration characterization in 2018

Yixin Luo, Saugata Ghose, Yu Cai, Erich F. Haratsch, and Onur Mutlu experimentally characterize real, then-state-of-the-art 3D NAND MLC chips in 2018. Their paper explicitly distinguishes its contribution from the 2016 study: the earlier work observed the first minutes after program, while Luo et al. follow retention behavior out to **24 days**.

In the tested population, the raw bit error rate (`RBER`) rises by about an order of magnitude within roughly **three hours** after programming and then increases much more slowly; another approximately order-of-magnitude increase takes on the order of **eleven days**. The important retention result is the *shape* of this curve, not the universalization of those exact numbers.

The paper uses historical/technical vocabulary including:

- `early retention loss`;
- `retention time` / `retention age`;
- `charge trap`;
- `threshold voltage (Vth)`;
- `raw bit error rate (RBER)`;
- `read reference voltage` / `optimal read reference voltage`;
- `Retention Model Aware Reading (ReMAR)`;
- `retention interference`;
- `layer-to-layer process variation`.

`front-loaded retention hazard`, `read-interpretation state`, and `controller time continuity` below are project analytical terms, not period vocabulary.

## Retained state and constitutive control state

The bounded regime contains several separable relations:

1. **cell charge / threshold-voltage state** — charge retained in a 3D charge-trap transistor and expressed through its threshold voltage;
2. **logical MLC value** — the bit value inferred from which voltage interval the cell is classified into;
3. **retention age** — elapsed time since the current data embodiment was programmed;
4. **P/E-cycle history** — wear state that changes the error behavior/model parameters;
5. **read-reference policy** — the voltage boundaries used to interpret the current threshold distribution;
6. **ECC margin** — remaining raw-error budget before logical recovery fails;
7. **program-time metadata** — in ReMAR, controller-retained timing state used to estimate current retention age;
8. **time source / reboot continuity** — ReMAR's proposed mechanism requires a meaningful clock relation across reads and controller restarts so that retained program timestamps can still be interpreted.

The program timestamp is not user payload. It is retained controller evidence about *when the current physical embodiment began aging*.

## Engineering reconstruction

### Nonvolatile does not mean temporally stationary

The cell does not require continuous operating power merely to keep its programmed charge distinction. Yet the 2018 measurements show that the physical distribution changes rapidly soon after programming.

Therefore:

> **nonvolatile retention ≠ time-invariant read margin**.

And, more specifically:

> **equal elapsed-time increments ≠ equal marginal retention loss**.

A one-hour interval immediately after program can matter differently from an equal interval much later. The retention curve is strongly front-loaded in the bounded experiment.

This is not a redefinition of Flash as volatile. It is a distinction between **power-independent survival** and **the time evolution of the error/read margin of that surviving state**.

### Retention age is not one linear maintenance clock

Case 36 already showed that NAND retention can motivate proactive controller work. Early retention loss adds a different temporal shape: the risk/margin change is concentrated near the beginning of the embodiment's life rather than progressing at one constant rate.

Thus:

> **retention age ≠ one linear maintenance clock**.

A policy that assumes one fixed periodic interval can be a poor match to a mechanism whose error growth is steep immediately after program and flatter later.

Luo et al. explicitly evaluate the earlier planar-oriented FCR policy and report that, under their 3D NAND model/measurements, its lifetime benefit is much smaller than the large planar result cited from the earlier work. This is an evaluation of transfer mismatch, not proof that all physical rewriting policies are wrong for 3D NAND.

### The same surviving cell state can require a different later read criterion

As charge leaks and threshold-voltage distributions shift, the read-reference voltage that minimizes raw errors also changes. The 2018 study observes that the optimal reference changes quickly when data is young and much more slowly after the early-retention period.

Therefore:

> **surviving cell charge ≠ fixed read-reference interpretation**.

And:

> **retained logical identity can depend on an age-sensitive interpretation rule.**

The bits need not be rewritten merely for a reader to change how the existing physical state is classified.

### ReMAR makes retained age metadata part of reading

ReMAR proposes to model retention loss and choose read-reference voltages using estimated data age. The controller keeps block program time together with P/E-cycle state, computes retention age on reads, and applies the model to select a better reference voltage.

This produces a particularly clear retention relation:

> **program-time metadata can become read-interpretation state.**

The timestamp does not carry the user's payload, and it does not preserve every program/read event. It is a compact control relation that helps decide how the payload should later be recovered.

Therefore:

> **retained program timestamp ≠ retained payload ≠ complete access history.**

The 2018 evaluation reports an average RBER reduction for ReMAR relative to its baseline. That is research-system/model evidence, not evidence of a shipped commercial controller.

### Clock continuity can become retention infrastructure

A timestamp helps only if its later interpretation remains meaningful. Luo et al. discuss using a real-time clock and, where necessary, synchronizing time with the host after boot.

This means that a retention regime over NAND charge can depend on another state that is not stored in the NAND page itself:

> **controller time continuity can become retention infrastructure.**

Yet:

> **controller time continuity ≠ medium charge continuity.**

Losing a clock relation and losing the charge state are different failures. The former can disable an age-aware optimization even while the payload remains physically present and perhaps still recoverable by other read/ECC paths.

### Read-reference adaptation is not physical refresh

ReMAR changes the voltage boundary used to interpret an aged distribution. It does not claim to put leaked charge back into the cell.

Therefore:

> **read-reference adaptation ≠ physical refresh/restoration.**

This is the central boundary against Case 36. FCR may reprogram or remap corrected payload to renew physical margin. ReMAR can instead extract a lower-error logical interpretation from the existing aged embodiment by using a better read boundary.

A later system could compose both kinds of techniques, but functional composability does not make them one operation.

### Logical recoverability can outlast pristine physical margin

As in Cases 36, 52, and 59, raw error growth can occur while ECC and read-retry/reference adaptation still recover the intended page.

Therefore:

> **correct logical read ≠ unchanged physical retention margin.**

And:

> **RBER growth ≠ immediate logical forgetting.**

Forgetting occurs only when available interpretation/correction/recovery resources can no longer recover an admissible logical value under the relevant service contract.

## Neighbor effects: a bounded context, not a merged case

The 2018 paper also describes `retention interference`: the leakage rate of a victim cell can depend on the charge state of a vertically adjacent cell, plausibly through the shared charge-trap structure. This is important context because it makes retention behavior relational.

But it must not be confused with Case 59:

> **retention interference ≠ program interference.**

Case 59 concerns a threshold shift caused by a neighboring **program operation** through capacitive coupling in a bounded planar floating-gate MLC regime. The 2018 retention-interference result concerns the **subsequent leakage rate** of charge-trap 3D cells as conditioned by neighboring stored state.

The present case does not attempt a full ReNAC or retention-interference history. Those remain separable slices if later evidence warrants them.

## Cross-case boundaries

### Versus Case 36 — Flash Correct-and-Refresh

Case 36:

```text
elapsed retention age / wear
    -> accumulating raw errors
    -> ECC correction
    -> in-place reprogram OR remap/rewrite
    -> renewed physical margin
```

Case 65:

```text
program time + P/E state
    -> strongly front-loaded 3D retention aging
    -> model estimated current distribution
    -> age-aware read-reference selection
    -> lower-error interpretation of existing embodiment
```

Safe functional analogy: both let controller policy depend on retention age.

Stop condition: **physical renewal is not the same as read-boundary adaptation**, and the evaluated planar/3D regimes differ.

### Versus Case 52 — NAND read disturb

Case 52 is **access-induced**: repeated reads apply pass-through stress to other cells, so read count can become a maintenance clock.

Case 65 is **post-program time dependent**: the steep early charge-loss period occurs as the programmed state ages, without requiring repeated reads as the trigger.

Therefore:

> **early retention loss ≠ read disturb.**

### Versus Case 59 — NAND program interference

Case 59 is **write-event-induced neighbor coupling**. Case 65 is **retention-time evolution** in charge-trap 3D NAND, with a separately identified neighbor-conditioned leakage phenomenon.

Therefore:

> **early retention loss ≠ program interference**.

### Versus DRAM refresh

A narrow analogy is allowed: both DRAM and NAND cases can make later readability depend on time-sensitive policy.

The analogy stops there. DRAM refresh is constitutive periodic restoration of volatile dynamic-cell state; early-retention-aware 3D NAND reading concerns a nonvolatile medium whose aged physical distribution may be interpreted with a changed reference voltage.

## Failure and forgetting boundaries

Distinct failure modes include:

- fast post-program charge loss shifts threshold distributions;
- P/E wear changes the applicable error behavior;
- a fixed read-reference voltage becomes increasingly mismatched to the aged distribution;
- ECC margin can be consumed even while reads still succeed;
- program-time metadata can be missing, stale, or associated with the wrong current physical embodiment;
- clock continuity/time synchronization can be unavailable after restart;
- the analytical model can be inaccurate for a different chip generation or vendor;
- age-aware reading can reduce errors without physically renewing the cell, leaving later physical aging still active;
- a controller can eventually exhaust ECC/read-retry/recovery options even though some physical charge remains.

Forgetting here is therefore neither “power was removed” nor “a certain wall-clock duration elapsed.” It is loss of a sufficiently distinguishable and recoverable logical state under the available read-reference, ECC, metadata, and policy resources.

## Historical record / engineering reconstruction / interpretation ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| fast initial charge loss is documented in charge-trapping NAND by 2010 | `H/P` | IEDM 2010 bibliographic/abstract record; used only for prior art |
| tube-type 3D NAND `early retention` within seconds is documented by 2016 | `H/P` | VLSI Technology 2016 paper metadata/abstract |
| Luo et al. extend observation of real 3D NAND early retention to 24 days and report strongly front-loaded RBER growth | `H/P` | directly inspected 2018 full paper, especially §4.3 |
| optimal read-reference voltage changes with data age in the bounded 3D NAND population | `H/P` | 2018 §4.3 and modeling sections |
| ReMAR tracks data age and adapts the read reference using program time/P-E information | `H/P` | 2018 §6.3 |
| a retained timestamp can become constitutive read-interpretation state | `E` | engineering reconstruction from ReMAR mechanism |
| time continuity can be retention infrastructure without being payload | `E` | reconstruction from RTC/host-time requirement |
| age-aware reference selection physically restores lost charge | `X` | ReMAR changes read interpretation; it is not a charge-rewrite mechanism |
| ReMAR is proven deployed in a named commercial controller | `X` | 2018 is a research proposal/evaluation; tested chip vendor is anonymized |
| every later 3D NAND/TLC/QLC generation has the same three-hour curve | `X` | outside bounded MLC device population |
| early retention loss is identical to read disturb or program interference | `X/A` | only higher-level margin/maintenance comparisons are allowed |
| nonvolatile media can require time-sensitive interpretation policy | `I` | bounded philosophical pressure; not historical actor vocabulary |

## Philosophical interpretation — bounded

This case supplies one narrow conceptual correction:

> **A retained state can remain materially present while the rule for making it reliably available to a future operation changes with the age of that state.**

That is useful to a philosophy of technical retention because it separates `remaining` from `remaining equally legible under one fixed interpretation`. It does not imply that the 2010–2018 engineers were making a philosophical claim about memory, nor does it make every controller timestamp a form of cultural or tertiary retention.

The engineering result comes first: a nonvolatile charge-trap state can age nonlinearly, and a controller can use retained age evidence to adapt how it reads the state.

## Cross-case result

Case 65 adds this chain:

```text
3D charge-trap programmed state
    !=
retention age
    !=
front-loaded threshold/RBER evolution
    !=
optimal read-reference voltage
    !=
ECC-correctable logical payload
    !=
program-time / P-E metadata
    !=
age-aware controller interpretation
    !=
physical refresh or rewrite
```

The strongest new result is that **retention policy can move from “renew the physical state on a schedule” toward “retain enough temporal metadata to reinterpret the same aged physical state more accurately.”** This is a functional comparison, not a claim of historical replacement or universal SSD practice.

## Related repositories

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `3D NAND`, `early retention loss`, `read reclaim`, and `ReMAR` found no dedicated case to reuse. A broader history of BiCS/V-NAND/charge-trap process architecture belongs there. This repository keeps only the retention-specific relation among front-loaded aging, read-reference adaptation, controller age metadata, ECC margin, and physical renewal.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) supplies the anti-anachronism discipline. `fast initial charge loss`, `early retention`, and `ReMAR` are source vocabulary where cited; `front-loaded retention hazard` and `read-interpretation state` are modern analytical terms.

## Sources

1. Yixin Luo, Saugata Ghose, Yu Cai, Erich F. Haratsch, Onur Mutlu, **“Improving 3D NAND Flash Memory Lifetime by Tolerating Early Retention Loss and Process Variation,”** *Proceedings of the ACM on Measurement and Analysis of Computing Systems* 2(3), Article 37, December 2018, DOI `10.1145/3224432`; presented at SIGMETRICS 2018. Author-accessible full text: <https://arxiv.org/abs/1807.05140>.
2. Bongsik Choi et al., **“Comprehensive evaluation of early retention (fast charge loss within a few seconds) characteristics in tube-type 3-D NAND Flash Memory,”** *2016 IEEE Symposium on VLSI Technology*, Honolulu, 14–16 June 2016, DOI `10.1109/VLSIT.2016.7573385`.
3. C.-P. Chen, H.-T. Lue, C.-C. Hsieh, K.-P. Chang, K.-Y. Hsieh, C.-Y. Lu, **“Study of fast initial charge loss and its impact on the programmed states Vt distribution of charge-trapping NAND flash,”** *2010 IEEE International Electron Devices Meeting (IEDM)*, San Francisco, 6–8 December 2010, pp. 5.6.1–5.6.4 / 118–121, DOI `10.1109/IEDM.2010.5703304`.
4. Christian Monzio Compagnoni, Alessandro Goda, Andrea S. Spinelli, Paolo Feeley, Alberto L. Lacaita, and Akira Visconti, **“Reviewing the Evolution of the NAND Flash Technology,”** and related 3D-NAND reliability literature are useful background but are not used to establish the central bounded claims here.
5. Rino Micheloni et al. / 2017 review context: **“Reliability of NAND Flash Memories: Planar Cells and Emerging Issues in 3D Devices,”** *Computers* 6(2):16, 2017, DOI `10.3390/computers6020016`, used as scholarly chronology/cross-check rather than as a substitute for the primary papers.
'''

evidence = r'''# Case 65 Grounding — 3D NAND Early Retention Loss and Age-Aware Reading (2010–2018)

## Status

**Grounded for the bounded case.**

The central mechanism and numerical/operational claims are grounded in the directly inspected 2018 Luo et al. full paper. The 2010 and 2016 papers are used to constrain priority and vocabulary through stable bibliographic/abstract records and the 2018 paper's own discussion of prior work. This record does **not** claim a complete invention genealogy or named-product deployment.

## Bounded research question

> When charge-trap 3D NAND exhibits strongly front-loaded post-program retention loss, what state must remain besides the payload if a controller wants to adapt later reads to the age of the current physical embodiment?

## Source hierarchy

| Source | Type / date | What was inspected | What it supports | What it does not support |
| --- | --- | --- | --- | --- |
| Luo et al., *Improving 3D NAND Flash Memory Lifetime by Tolerating Early Retention Loss and Process Variation*, POMACS 2018, DOI `10.1145/3224432`, arXiv `1807.05140v2` | peer-reviewed primary experimental systems paper | author-accessible full text, especially §§1, 3, 4.3–4.5, 5.2, 6.3 and evaluation | real 3D NAND MLC characterization; 24-day early-retention curve; changing optimal Vref; ReMAR model/metadata/read policy; explicit limitations and comparison to planar techniques | named chip vendor/product; universal 3D/TLC/QLC behavior; commercial ReMAR deployment |
| Choi et al., *Comprehensive evaluation of early retention ... tube-type 3-D NAND Flash Memory*, VLSI Technology 2016, DOI `10.1109/VLSIT.2016.7573385` | primary device paper | bibliographic record + abstract; chronology cross-checked by 2018 paper and 2017 review | source-period `early retention`; fast charge loss within seconds; tube-type 3D NAND; lateral-loss/shared-charge-trap explanation in bounded abstract | 24-day system-level behavior; ReMAR; all later 3D NAND |
| Chen et al., *Study of fast initial charge loss ... charge-trapping NAND flash*, IEDM 2010, DOI `10.1109/IEDM.2010.5703304` | primary device paper | stable bibliographic record/abstract + later review citation | `fast initial charge loss` in charge-trapping NAND by 2010; priority boundary against a 2018 origin claim | a complete 3D-NAND mechanism genealogy; ReMAR or 2018 chip behavior |
| *Reliability of NAND Flash Memories: Planar Cells and Emerging Issues in 3D Devices*, *Computers* 6(2):16, 2017, DOI `10.3390/computers6020016` | scholarly review | references/discussion around 3D retention | independent chronology linking 2010 charge-trap fast loss and 2016 3D early retention | substitute for primary evidence where exact mechanism/claim is decisive |

## Primary-source locations

### Luo et al. 2018

Author-accessible text: <https://arxiv.org/abs/1807.05140>  
Published DOI: <https://doi.org/10.1145/3224432>

The directly inspected full paper supplies the central evidence:

- **Introduction / contribution statement** — distinguishes planar floating-gate NAND from 3D charge-trap NAND; identifies early retention loss as rapid post-program error growth and states that the work extends prior short-duration observation to 24 days.
- **§4.3 Early Retention Loss** — experiment uses multiple blocks across P/E-cycle points, observes retention from minutes out to 24 days, and shows RBER rising approximately one order of magnitude within ~3 hours and much more slowly thereafter; the paper describes the rate as steep initially and flattening with age.
- **§4.3 read-reference discussion** — optimal read-reference voltages move rapidly for young data and more slowly for older data, tying later read interpretation to retention age.
- **§4.4 Retention Interference** — neighboring stored state can alter victim leakage rate; retained only as a boundary/context claim here.
- **§4.5 comparison with planar error sources** — reports lower program-interference/read-disturb sensitivity for the particular characterized generation; this record treats that as generation-bounded and does not generalize it to all later 3D NAND.
- **§6.3 ReMAR** — tracks retention age, uses a retention model plus P/E-cycle/program-time information, and adapts read reference voltage on reads; discusses small controller metadata and a time-source/RTC/host-sync relation.
- **Evaluation** — reports ReMAR reducing RBER in the evaluated population/model; combined techniques yield the paper's larger lifetime/ECC-overhead figures. These are evaluation results, not a field-deployment certificate.

## Chronology / prior-art control

### 2010: charge-trapping NAND fast initial charge loss

Chen et al. publish the phrase **`fast initial charge loss`** in an IEDM paper on charge-trapping NAND. Stable record: DOI `10.1109/IEDM.2010.5703304`.

Safe conclusion:

> fast initial charge loss in charge-trapping NAND predates the 2018 3D-NAND systems characterization.

Unsafe conclusion rejected:

> Chen 2010 already established every later tube-type 3D NAND retention mechanism and controller policy.

### 2016: tube-type 3D NAND `early retention`

Choi et al., DOI `10.1109/VLSIT.2016.7573385`, explicitly describe fast charge loss within seconds as **`early retention`** in tube-type 3D NAND. The abstract attributes the bounded result mainly to lateral charge loss through shared charge-trap layers and studies microsecond-to-second behavior.

Safe conclusion:

> 3D-NAND early-retention observation predates Luo et al. 2018.

The 2018 paper itself says its novelty is **extended-duration observation**, contrasting its 24-day measurements with a prior study confined to roughly the first minutes after program.

### 2018: extended real-chip characterization + age-aware reading

The defensible novelty boundary is not “first early retention.” It is:

> a broad real-chip 3D NAND characterization that extends early-retention observation across a workload-relevant multi-day interval, models the age-dependent distributions/read references, and evaluates a controller mechanism (ReMAR) that tracks age to adapt later reads.

## Claim ledger

| Claim | Label | Evidence | Confidence / limit |
| --- | --- | --- | --- |
| fast initial charge loss in charge-trapping NAND is documented by 2010 | `H/P` | Chen IEDM 2010 record | high for chronology/vocabulary; no broader mechanism priority claim |
| `early retention` in tube-type 3D NAND is documented by 2016 | `H/P` | Choi VLSI 2016 abstract/DOI | high for bounded source claim; full paper not used for unsupported detail |
| Luo et al. experimentally study real 3D NAND MLC chips to 24 days | `H/P` | 2018 full paper §§1, 4.3 | high |
| tested RBER rises about an order of magnitude within ~3 hours, then much more slowly | `H/P` | 2018 §4.3 / plotted data | high, but population-specific |
| optimal read-reference voltage changes with retention age | `H/P` | 2018 §4.3, model | high for tested population |
| ReMAR uses age/P-E/program-time state to adapt Vref | `H/P` | 2018 §6.3 | high as proposal/evaluation |
| controller time state can be retention infrastructure | `E` | reconstruction from ReMAR's timestamp/time-source dependency | strong bounded reconstruction |
| ReMAR physically restores leaked charge | `X` | contradicted by mechanism: it adapts the read boundary | rejected |
| one fixed periodic refresh policy is always sufficient/optimal for 3D NAND | `X` | early-retention curve + FCR transfer evaluation | rejected as universal claim |
| all 3D NAND generations have the paper's same 3-hour/11-day behavior | `X` | device/process dependence | rejected |
| ReMAR shipped in a named product | `X` | no named deployment evidence in source set | rejected |
| early retention loss = read disturb = program interference | `X/A` | mechanisms/triggers differ | rejected except bounded comparison of shared ECC-margin pressure |

## Engineering reconstruction checks

### `nonvolatile` boundary

The paper never requires the page to be continually powered merely to retain its programmed state. The project therefore does **not** call the medium DRAM-like volatile. The narrower reconstruction is:

```text
power-independent charge survival
    !=
time-invariant threshold distribution
    !=
time-invariant optimal read reference
    !=
time-invariant raw-error margin
```

### Controller metadata boundary

ReMAR's program time/P-E information is constitutive only to the **age-aware optimization path**. Losing that metadata does not prove the NAND payload instantly vanishes. Other reading/ECC/recovery paths may remain possible.

Therefore:

> metadata dependence ≠ payload identity.

### Physical renewal boundary

Changing Vref changes interpretation, not the cell's stored charge. Accordingly:

> age-aware reading ≠ FCR rewrite/remap ≠ secure erase.

## Cross-case stop conditions

| Compared case | Safe relation | Stop condition |
| --- | --- | --- |
| Case 36 FCR | both make NAND reliability policy retention-age aware | FCR renews physical embodiment/margin; ReMAR adapts read interpretation; planar/3D evidence regimes differ |
| Case 52 read disturb | both consume finite raw-error/ECC margin | read disturb is caused by repeated access/Vpass stress; early retention loss progresses after program with time |
| Case 59 program interference | both can make cell recoverability relational to nearby physical state/activity | program interference is neighbor-program induced capacitive shift; 3D retention interference is neighbor-conditioned leakage in a charge-trap structure |
| Case 03 / DRAM refresh | both expose time-sensitive reliability policy | DRAM periodic regeneration is constitutive volatile-state restoration; ReMAR is nonvolatile-age-aware read interpretation |
| Case 55 NVMe health telemetry | both retain controller/history-derived metadata | lifetime SMART aggregates device history; a program timestamp estimates age of one current physical embodiment for read policy |

## Related-repository duplication check

Searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for:

- `3D NAND`;
- `early retention loss`;
- `read reclaim`;
- `ReMAR`;

returned no dedicated case at the time of this grounding pass. A general history of charge-trap cells, vertical-stack manufacturing, BiCS/V-NAND, layer scaling, or product genealogy should be built there rather than duplicated here.

## What remains open after this case

This case intentionally leaves several roadmap gaps open:

- modern **3D-NAND read reclaim / device-specific read-disturb management** in named or source-verifiable controllers;
- TLC/QLC and later-generation quantitative early-retention behavior;
- named commercial deployment of age-aware read-reference management;
- HeatWatch/self-recovery + temperature as a distinct 3D-NAND retention policy slice;
- retention-interference/ReNAC as a full independent slice;
- controller metadata loss/corruption experiments for age-aware read policy;
- composition with filesystem/database persistence semantics.

## Sources

1. Yixin Luo, Saugata Ghose, Yu Cai, Erich F. Haratsch, Onur Mutlu, **“Improving 3D NAND Flash Memory Lifetime by Tolerating Early Retention Loss and Process Variation,”** *Proc. ACM Meas. Anal. Comput. Syst.* 2(3), Article 37, 2018, DOI `10.1145/3224432`, arXiv `1807.05140v2`: <https://arxiv.org/abs/1807.05140>.
2. Bongsik Choi et al., **“Comprehensive evaluation of early retention (fast charge loss within a few seconds) characteristics in tube-type 3-D NAND Flash Memory,”** VLSI Technology 2016, DOI `10.1109/VLSIT.2016.7573385`.
3. C.-P. Chen et al., **“Study of fast initial charge loss and its impact on the programmed states Vt distribution of charge-trapping NAND flash,”** IEDM 2010, DOI `10.1109/IEDM.2010.5703304`.
4. **“Reliability of NAND Flash Memories: Planar Cells and Emerging Issues in 3D Devices,”** *Computers* 6(2):16, 2017, DOI `10.3390/computers6020016`, used for secondary chronology/cross-check only.
'''

readme_case_line = "- [`cases/65-3d-nand-early-retention-loss-age-aware-reading.md`](cases/65-3d-nand-early-retention-loss-age-aware-reading.md) — grounded 3D-NAND retention bridge: 2010/2016 prior art bounds fast-initial-charge-loss and early-retention chronology, while Luo et al. 2018 ground strongly front-loaded real-chip retention aging and ReMAR's use of program-time/P-E metadata to adapt later read-reference voltage without physically refreshing the cell."
readme_evidence_line = "- [`evidence/65-3d-nand-2010-2018-early-retention-grounding.md`](evidence/65-3d-nand-2010-2018-early-retention-grounding.md) — Case-65 grounding record: 2010 charge-trap fast-loss and 2016 tube-type 3D early-retention prior art constrain novelty; directly inspected 2018 full text grounds the 24-day front-loaded error curve, age-dependent optimal Vref, ReMAR metadata/time-source requirements, and proposal-versus-deployment boundary."

case_index_row = "| [3D NAND Early Retention Loss: Front-Loaded Charge Loss, Retention Age, and Read-Reference Adaptation](cases/65-3d-nand-early-retention-loss-age-aware-reading.md) | **grounded** | 3D charge-trap NAND + strongly front-loaded post-program retention loss + age/P-E metadata + age-aware read-reference policy + ECC margin | separate nonvolatility from time-invariant margin; retention age from a linear clock; physical renewal from read interpretation; and program-time metadata from payload/history | [2010–2018 early-retention grounding](evidence/65-3d-nand-2010-2018-early-retention-grounding.md); modern named-device read reclaim/read-disturb policy, later TLC/QLC generations, commercial ReMAR-like deployment, HeatWatch, and controller-metadata fault validation remain separate work |"

matrix_row = "| 3D NAND early retention / 2010–2018 bounded regime | charge-trap cell threshold distribution + program-age/P-E metadata + controller read-reference model | no DRAM-like periodic restoration merely to hold charge; bounded ReMAR proposal retains age evidence and adapts later Vref, while ECC handles residual raw errors | logically nondestructive read whose reference voltage may be selected according to estimated data age | ordinary page/block mapping plus controller metadata tying the current embodiment to program time/P-E state | current physical embodiment can remain in place under ReMAR; other policies may later rewrite/remap but are separate mechanisms | no payload history by default; compact program-time/P-E state preserves age evidence, not the sequence of writes/reads |"

findings = r'''## Case 65 — 3D NAND early-retention findings

717. **nonvolatile retention ≠ time-invariant read margin** — the bounded 3D charge-trap cells retain programmed state without continuous power while their threshold distributions and raw-error margin can change rapidly after programming;
718. **equal elapsed-time increments ≠ equal marginal retention loss** — Luo et al.'s tested population shows strongly front-loaded RBER growth, with much faster change in the first hours than over equal later intervals;
719. **retention age ≠ one linear maintenance clock** — a fixed-period policy can mismatch a mechanism whose error growth rate changes sharply with age;
720. **surviving cell charge ≠ fixed read-reference interpretation** — the optimal discrimination voltage changes as the retained threshold distribution ages;
721. **program-time metadata can become read-interpretation state** — ReMAR proposes retaining program time together with P/E-cycle information so later reads can choose an age-appropriate reference voltage;
722. **retained program timestamp ≠ retained payload ≠ complete access history** — the timestamp is compact controller evidence about the current embodiment's age, not the user's data and not a record of every event;
723. **read-reference adaptation ≠ physical refresh** — ReMAR changes how an aged cell is interpreted rather than restoring its leaked charge, unlike Case 36's rewrite/reprogram/remap paths;
724. **correct logical read ≠ unchanged physical retention margin** — raw errors and threshold drift can grow while reference adaptation/ECC still recover the intended value;
725. **2018 3D-NAND characterization ≠ invention of fast initial charge loss** — Chen et al. document `fast initial charge loss` in charge-trapping NAND at IEDM 2010;
726. **2018 extended-duration study ≠ first 3D-NAND early-retention observation** — Choi et al. use `early retention` for fast loss in tube-type 3D NAND in 2016; Luo et al.'s defensible novelty is the longer real-chip characterization/modeling and resulting controller proposal;
727. **one periodic refresh interval ≠ universally matched NAND retention policy** — the 2018 evaluation shows an earlier planar-oriented FCR policy transfers poorly to the front-loaded behavior of its tested 3D NAND regime, without proving all physical-renewal policies invalid;
728. **controller clock/time continuity can become retention infrastructure** — an age-aware read policy needs a meaningful later relation between retained program time and current time, including across reboot;
729. **controller time continuity ≠ medium charge continuity** — losing/scrambling age evidence can disable an optimization while the NAND charge and logical payload may still physically survive;
730. **early retention loss ≠ read disturb ≠ program interference** — elapsed post-program aging, repeated-read Vpass stress, and neighbor-program coupling are distinct triggers/mechanisms even when they consume one ECC budget;
731. **retention interference ≠ program interference** — the 2018 3D result conditions charge-leakage rate on neighboring stored state, whereas Case 59's bounded planar result is a threshold shift caused by a neighboring program transition;
732. **ReMAR proposal/evaluation ≠ shipped-controller deployment** — the paper tests real chips and evaluates a controller technique but does not identify a commercial SSD that implements ReMAR as specified.
'''


def insert_after_line_with(text, needle, new_line):
    if new_line in text:
        return text
    lines = text.splitlines()
    matches = [i for i, line in enumerate(lines) if needle in line]
    if not matches:
        raise RuntimeError(f"anchor not found: {needle}")
    lines.insert(matches[-1] + 1, new_line)
    return "\n".join(lines).rstrip() + "\n"


def patch_readme(text):
    text = insert_after_line_with(text, "cases/64-apache-kafka-transaction-coordinator-state-recovery.md", readme_case_line)
    text = insert_after_line_with(text, "evidence/64-kafka-0110-transaction-state-recovery-grounding.md", readme_evidence_line)
    return text


def patch_roadmap(text):
    if CASE_PATH in text:
        return text
    lines = text.splitlines()
    idx = next((i for i, line in enumerate(lines) if "SSD FTL/controller-mediated persistence" in line), None)
    if idx is None:
        raise RuntimeError("SSD roadmap anchor not found")
    line = lines[idx]
    line2, n = re.subn(r"55, and 59\*\*", "55, 59, and 65**", line, count=1)
    if n == 0:
        line2, n = re.subn(r"and 59\*\*", "59, and 65**", line, count=1)
    if n == 0:
        raise RuntimeError("could not update SSD case list")
    desc = " [`cases/65-3d-nand-early-retention-loss-age-aware-reading.md`](cases/65-3d-nand-early-retention-loss-age-aware-reading.md), grounded by [`evidence/65-3d-nand-2010-2018-early-retention-grounding.md`](evidence/65-3d-nand-2010-2018-early-retention-grounding.md), adds a 3D charge-trap early-retention regime: 2010/2016 prior art prevents a false 2018 origin claim, while the extended 2018 real-chip study shows strongly front-loaded post-program error growth and evaluates ReMAR, where retained program-time/P-E state selects an age-aware read reference without physically renewing the cell. This narrows the 3D-NAND roadmap gap but leaves modern named-device read reclaim/read-disturb management open."
    marker = " The broad item stays unchecked because"
    if marker not in line2:
        raise RuntimeError("SSD broad-item marker not found")
    line2 = line2.replace(marker, desc + marker, 1)
    lines[idx] = line2
    return "\n".join(lines).rstrip() + "\n"


def patch_case_index(text):
    if CASE_PATH not in text:
        text = insert_after_line_with(text, "cases/64-apache-kafka-transaction-coordinator-state-recovery.md", case_index_row)
    if matrix_row not in text:
        lines = text.splitlines()
        h = next((i for i, line in enumerate(lines) if line.strip() == "## Comparison matrix — provisional"), None)
        if h is None:
            raise RuntimeError("comparison matrix heading not found")
        start = next((i for i in range(h + 1, len(lines)) if lines[i].startswith("| Case |")), None)
        if start is None:
            raise RuntimeError("comparison matrix table not found")
        end = start + 2
        while end < len(lines) and lines[end].startswith("|"):
            end += 1
        lines.insert(end, matrix_row)
        text = "\n".join(lines).rstrip() + "\n"
    if "## Case 65 — 3D NAND early-retention findings" not in text:
        text = text.rstrip() + "\n\n" + findings.rstrip() + "\n"
    return text


def run(*args):
    return subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)


def main():
    # Bring the triggering checkout to the latest main before making the bounded integration.
    subprocess.run(["git", "pull", "--ff-only", "origin", "main"], cwd=ROOT, check=True)

    (ROOT / CASE_PATH).write_text(case.rstrip() + "\n", encoding="utf-8")
    (ROOT / EVIDENCE_PATH).write_text(evidence.rstrip() + "\n", encoding="utf-8")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
    index = (ROOT / "CASE_INDEX.md").read_text(encoding="utf-8")

    (ROOT / "README.md").write_text(patch_readme(readme), encoding="utf-8")
    (ROOT / "ROADMAP.md").write_text(patch_roadmap(roadmap), encoding="utf-8")
    (ROOT / "CASE_INDEX.md").write_text(patch_case_index(index), encoding="utf-8")

    # Validate the permanent tree before committing.
    nums = sorted(int(p.name[:2]) for p in (ROOT / "cases").glob("[0-9][0-9]-*.md"))
    if nums != list(range(66)):
        raise RuntimeError(f"case-number ledger mismatch: {nums[:3]} ... {nums[-5:]}")
    for p in [CASE_PATH, EVIDENCE_PATH]:
        if not (ROOT / p).exists():
            raise RuntimeError(f"missing {p}")
    for nav in ["README.md", "ROADMAP.md", "CASE_INDEX.md"]:
        t = (ROOT / nav).read_text(encoding="utf-8")
        if CASE_PATH not in t:
            raise RuntimeError(f"{nav} missing case 65 path")
    idx_text = (ROOT / "CASE_INDEX.md").read_text(encoding="utf-8")
    if "717. **nonvolatile retention" not in idx_text or "732. **ReMAR proposal/evaluation" not in idx_text:
        raise RuntimeError("case 65 findings missing")
    if idx_text.count(CASE_PATH) < 1:
        raise RuntimeError("case 65 index row missing")
    run("git", "diff", "--check")

    subprocess.run(["git", "config", "user.name", "github-actions[bot]"], cwd=ROOT, check=True)
    subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], cwd=ROOT, check=True)
    subprocess.run(["git", "add", "README.md", "ROADMAP.md", "CASE_INDEX.md", CASE_PATH, EVIDENCE_PATH], cwd=ROOT, check=True)
    subprocess.run(["git", "rm", "-f", ".github/scripts/integrate_case65.py", ".github/workflows/integrate-case65.yml"], cwd=ROOT, check=True)
    subprocess.run(["git", "commit", "-m", "case65: ground 3D NAND early retention and age-aware reading"], cwd=ROOT, check=True)
    subprocess.run(["git", "push", "origin", "HEAD:main"], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
