# 3D NAND Early Retention Loss: Front-Loaded Charge Loss, Retention Age, and Read-Reference Adaptation

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
