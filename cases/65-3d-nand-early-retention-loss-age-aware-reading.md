# 3D NAND Early Retention Loss: Front-Loaded Charge Loss, Retention Age, and Read-Reference Adaptation

## Status

**`grounded`** — bounded to the retention-specific transition from earlier charge-trapping NAND fast-initial-charge-loss evidence (2010), through a 2016 tube-type 3D NAND early-retention study, to Luo et al.'s extended 2018 experimental characterization of real 3D NAND MLC chips and their **Retention Model Aware Reading (ReMAR)** proposal. A follow-on deepening now also isolates the same 2018 paper's **retention interference** measurements and **Retention Interference Aware Neighbor-Cell Assisted Correction (ReNAC)** proposal without upgrading either proposal into product deployment.

Evidence navigation:

- grounding: [`../evidence/65-3d-nand-2010-2018-early-retention-grounding.md`](../evidence/65-3d-nand-2010-2018-early-retention-grounding.md)
- retention-interference / ReNAC deepening: [`../evidence/65-luo-2018-retention-interference-renac-deepening.md`](../evidence/65-luo-2018-retention-interference-renac-deepening.md)

## Scope

This case asks a narrow question left open by Cases 36, 52, and 59:

> What changes when a nonvolatile 3D charge-trap NAND cell loses a disproportionate amount of retention margin soon after programming, so that the age of the data can become an input to later read interpretation — and when the retained state of a vertically adjacent cell can further condition that aging trajectory?

The bounded object is **early retention loss / fast initial charge loss** in charge-trapping NAND, with special attention to the 2018 extended-duration characterization of real 3D NAND MLC chips, its age-aware ReMAR proposal, and its separately measured neighbor-conditioned **retention interference** phenomenon.

This is **not**:

- a complete history of 3D NAND or charge-trap Flash;
- evidence that every 3D NAND generation, TLC/QLC product, or vendor has the same early-retention curve or retention-interference magnitude;
- a claim that 2018 invented fast initial charge loss or first observed early retention in 3D NAND;
- evidence that ReMAR or ReNAC shipped in a named commercial SSD/controller;
- a modern device-specific `read reclaim` case;
- the same mechanism as Case 36's planar-NAND Flash Correct-and-Refresh (FCR), Case 52's read disturb, or Case 59's program interference;
- a claim that retention interference, layer-to-layer process variation, early retention loss, and read disturb are one phenomenon;
- a claim that the 2018 paper demonstrated a meaningful ReNAC lifetime improvement on its tested generation; the paper explicitly says it did not.

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

Yixin Luo, Saugata Ghose, Yu Cai, Erich F. Haratsch, and Onur Mutlu experimentally characterize real, then-state-of-the-art 3D NAND MLC chips in 2018. Their paper explicitly distinguishes its contribution from earlier short-duration work and follows retention behavior out to **24 days**.

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
- `Retention Interference Aware Neighbor-Cell Assisted Correction (ReNAC)`;
- `layer-to-layer process variation`.

`front-loaded retention hazard`, `read-interpretation state`, `controller time continuity`, and `relational retention trajectory` below are project analytical terms, not period vocabulary.

## Retained state and constitutive control state

The bounded regime contains several separable relations:

1. **cell charge / threshold-voltage state** — charge retained in a 3D charge-trap transistor and expressed through its threshold voltage;
2. **logical MLC value** — the bit value inferred from which voltage interval the cell is classified into;
3. **retention age** — elapsed time since the current data embodiment was programmed;
4. **P/E-cycle history** — wear state that changes the error behavior/model parameters;
5. **read-reference policy** — the voltage boundaries used to interpret the current threshold distribution;
6. **ECC margin** — remaining raw-error budget before logical recovery fails;
7. **program-time metadata** — in ReMAR, controller-retained timing state used to estimate current retention age;
8. **time source / reboot continuity** — ReMAR's proposed mechanism requires a meaningful clock relation across reads and controller restarts so that retained program timestamps can still be interpreted;
9. **vertically adjacent neighbor state** — in the measured retention-interference relation, a conditioning variable for the victim's threshold-voltage evolution;
10. **neighbor-aware recovery policy** — in ReNAC, an additional read-offset selection relation used after the ordinary read path fails.

The program timestamp is not user payload. Likewise, the neighbor's value does not become part of the victim application's payload merely because it can be used as recovery side information.

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

> **correct logical read ≠ unchanged physical retention margin**.

And:

> **RBER growth ≠ immediate logical forgetting**.

Forgetting occurs only when available interpretation/correction/recovery resources can no longer recover an admissible logical value under the relevant service contract.

## Retention interference deepening: age plus neighbor state

The 2018 paper does more than report front-loaded aging. In §4.4 it measures **retention interference**: the speed of victim-cell retention loss depends on the threshold-voltage state of a vertically adjacent neighbor that shares the charge-trap structure along the bitline.

The authors describe charge moving between higher- and lower-threshold-voltage neighbors through the shared charge-trap layer. They then deliberately control for **program interference** by using neighbors programmed before the victims and excluding an erased-state victim regime that has separate interference sensitivity. Grouping cells by victim state and neighbor state over a 24-day interval, they observe smaller victim threshold shifts when the neighboring cell is in a higher-voltage state.

That gives Case 65 a stronger relation than age-aware reading alone:

```text
retention age
    !=
complete measured retention trajectory

retention age + neighbor stored state
    ->
more specific estimate of victim threshold-voltage evolution
```

Therefore:

> **same retention age ≠ necessarily the same physical retention trajectory.**

And:

> **victim logical identity ≠ physically self-contained victim state.**

The neighbor does not become part of the victim payload. It becomes part of the physical context that can help explain and recover the victim.

### ReNAC adapts a recovery form without merging the failure mechanisms

Luo et al. explicitly compare the data dependency of retention interference with the earlier data dependency of **program interference**. They adapt the 2014 Neighbor-Cell Assisted Correction (`NAC`) recovery pattern to retention interference and name the result **ReNAC**.

The bounded mechanism is:

```text
retention time + vertically adjacent neighbor state
    -> online retention-interference model
    -> neighbor-dependent read offset
    -> reread after ordinary read/ECC failure
```

This is a read-path recovery proposal, not a physical rewrite.

Therefore:

> **neighbor-assisted logical recovery ≠ physical restoration of the victim cell.**

And the genealogy must stop before a mechanism identity claim:

> **reuse of NAC's recovery form ≠ program interference and retention interference are the same physics.**

### The negative result is part of the evidence

The paper states that ReNAC does **not** show meaningful flash-lifetime improvement for the current generation of 3D NAND it tested. The measured retention-interference shift is less than two normalized voltage steps and is smaller than the voltage movement from process variation and early retention loss in that population.

The authors expect retention interference to matter more as geometries shrink and in TLC/QLC devices with narrower state margins, but leave quantitative future-device evaluation open.

Therefore:

> **ReNAC proposed ≠ demonstrated current-generation lifetime benefit.**

And:

> **projected future TLC/QLC importance ≠ measured TLC/QLC result.**

The dedicated deepening record keeps this negative result and the full non-claim list: [`../evidence/65-luo-2018-retention-interference-renac-deepening.md`](../evidence/65-luo-2018-retention-interference-renac-deepening.md).

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

Case 65 ReMAR:

```text
program time + P/E state
    -> strongly front-loaded 3D retention aging
    -> model estimated current distribution
    -> age-aware read-reference selection
    -> lower-error interpretation of existing embodiment
```

Case 65 ReNAC deepening:

```text
retention time + neighbor state
    -> neighbor-conditioned retention estimate
    -> failure-path read-offset selection
    -> reread of the existing embodiment
```

Safe functional analogy: all can preserve logical availability against retention-related error growth.

Stop condition: **physical renewal is not the same as read-boundary adaptation**, and the evaluated planar/3D regimes differ.

### Versus Case 52 — NAND read disturb

Case 52 is **access-induced**: repeated reads apply pass-through stress to other cells, so read count can become a maintenance clock.

Case 65 is **post-program time dependent**: the steep early charge-loss period and retention-interference relation evolve with retention time; repeated reads are not the trigger of the underlying phenomenon.

Therefore:

> **early retention loss / retention interference ≠ read disturb.**

### Versus Case 59 — NAND program interference / NAC

Case 59 is **write-event-induced neighbor coupling**. A neighboring program event shifts a previously programmed victim, and program order matters.

Case 65 retention interference is **retention-time evolution conditioned by neighbor stored state** in a 3D charge-trap structure. Luo et al. reuse the neighbor-aware recovery *form* of NAC as ReNAC but experimentally control for program interference when characterizing the retention phenomenon.

Therefore:

> **retention interference ≠ program interference.**

But a safe functional analogy remains:

> **in both cases, neighbor state can become decoding side information after the ordinary read path fails.**

### Versus DRAM refresh

A narrow analogy is allowed: both DRAM and NAND cases can make later readability depend on time-sensitive policy.

The analogy stops there. DRAM refresh is constitutive periodic restoration of volatile dynamic-cell state; early-retention-aware 3D NAND reading concerns a nonvolatile medium whose aged physical distribution may be interpreted with a changed reference voltage, optionally informed by neighbor state.

## Failure and forgetting boundaries

Distinct failure modes include:

- fast post-program charge loss shifts threshold distributions;
- P/E wear changes the applicable error behavior;
- a fixed read-reference voltage becomes increasingly mismatched to the aged distribution;
- ECC margin can be consumed even while reads still succeed;
- program-time metadata can be missing, stale, or associated with the wrong current physical embodiment;
- clock continuity/time synchronization can be unavailable after restart;
- the analytical model can be inaccurate for a different chip generation or vendor;
- a victim's threshold evolution can differ because a vertically adjacent neighbor occupies a different state;
- neighbor-state metadata/reads can be unavailable or the neighbor-conditioned model can be wrong;
- age-aware or neighbor-aware reading can reduce errors without physically renewing the cell, leaving later physical aging still active;
- a controller can eventually exhaust ECC/read-retry/recovery options even though some physical charge remains.

Forgetting here is therefore neither “power was removed” nor “a certain wall-clock duration elapsed.” It is loss of a sufficiently distinguishable and recoverable logical state under the available read-reference, ECC, metadata, neighbor information, and policy resources.

## Historical record / engineering reconstruction / interpretation ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| fast initial charge loss is documented in charge-trapping NAND by 2010 | `H/P` | IEDM 2010 bibliographic/abstract record; used only for prior art |
| tube-type 3D NAND `early retention` within seconds is documented by 2016 | `H/P` | VLSI Technology 2016 paper metadata/abstract |
| Luo et al. extend observation of real 3D NAND early retention to 24 days and report strongly front-loaded RBER growth | `H/P` | directly inspected 2018 full paper, especially §4.3 |
| optimal read-reference voltage changes with retention age in the bounded 3D NAND population | `H/P` | 2018 §4.3 and modeling sections |
| ReMAR tracks data age and adapts the read reference using program time/P-E information | `H/P` | 2018 §6.3 |
| Luo et al. measure victim retention shift correlated with vertically adjacent neighbor state | `H/P` | 2018 §4.4 |
| the authors control the retention-interference experiment against program-interference contamination | `H/P` | 2018 §4.4 |
| ReNAC models retention interference using retention time and neighbor state | `H/P` | 2018 §6.4 |
| ReNAC adapts earlier NAC's recovery form | `H/P` | 2018 §6.4 + Cai et al. SIGMETRICS 2014 |
| ReNAC shows meaningful lifetime improvement on the tested current generation | `X` | 2018 explicitly reports that it does not |
| a retained timestamp can become constitutive read-interpretation state | `E` | engineering reconstruction from ReMAR mechanism |
| time continuity can be retention infrastructure without being payload | `E` | reconstruction from RTC/host-time requirement |
| neighbor state can become recovery side information without becoming victim payload | `E` | reconstruction from retention-interference/ReNAC mechanism |
| age-aware or neighbor-aware reference selection physically restores lost charge | `X` | read-boundary adaptation is not charge rewrite |
| ReMAR or ReNAC is proven deployed in a named commercial controller | `X` | 2018 mechanisms are research proposals/evaluations; tested chip vendor is anonymized |
| every later 3D NAND/TLC/QLC generation has the same three-hour curve or same interference magnitude | `X` | outside bounded MLC device population |
| early retention loss / retention interference is identical to read disturb or program interference | `X/A` | only higher-level margin/maintenance comparisons are allowed |
| nonvolatile media can require time-sensitive and relational interpretation policy | `I` | bounded philosophical pressure; not historical actor vocabulary |

## Philosophical interpretation — bounded

This case supplies two narrow conceptual corrections:

> **A retained state can remain materially present while the rule for making it reliably available to a future operation changes with the age of that state.**

And, after the retention-interference deepening:

> **A retained state can remain materially local while its future legibility is partly relational to another retained state.**

These are useful to a philosophy of technical retention because they separate `remaining` from `remaining equally legible under one fixed interpretation`, and they show that recovery context can include both temporal and spatially adjacent evidence. They do not imply that the engineers were making a philosophical claim about memory, nor do they make every controller timestamp or neighbor read a form of cultural or tertiary retention.

The engineering result comes first: a nonvolatile charge-trap state can age nonlinearly, and the controller can use retained age evidence — and, in the bounded ReNAC proposal, neighbor-state evidence — to adapt how it reads the state.

## Cross-case result

Case 65 now adds this chain:

```text
3D charge-trap programmed state
    !=
retention age
    !=
front-loaded threshold/RBER evolution
    !=
vertically adjacent neighbor state
    !=
neighbor-conditioned retention trajectory
    !=
optimal / recovery read-reference voltage
    !=
ECC-correctable logical payload
    !=
program-time / P-E metadata
    !=
age-aware / neighbor-aware controller interpretation
    !=
physical refresh or rewrite
```

The strongest result remains that **retention policy can move from “renew the physical state on a schedule” toward “retain enough temporal and contextual evidence to reinterpret the same aged physical state more accurately.”** This is a functional comparison, not a claim of historical replacement or universal SSD practice.

## Related repositories

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `3D NAND`, `retention interference`, and `ReNAC` found no dedicated case to reuse. A broader history of BiCS/V-NAND/charge-trap process architecture belongs there. This repository keeps only the retention-specific relation among front-loaded aging, neighbor-conditioned drift, read-reference adaptation, controller age metadata, ECC margin, and physical renewal.

Case 59 remains the local home for the earlier program-interference/NAC genealogy; this case links that work instead of duplicating it.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) supplies the anti-anachronism discipline. `fast initial charge loss`, `early retention`, `ReMAR`, `retention interference`, and `ReNAC` are source vocabulary where cited; `front-loaded retention hazard`, `read-interpretation state`, and `relational retention trajectory` are modern analytical terms.

## Remaining work

The early-retention/ReMAR case and the 2018 retention-interference/ReNAC slice are grounded, but stronger evidence remains open:

- independent replication of retention interference in later **named** 3D NAND generations/vendors;
- direct TLC/QLC measurements rather than carrying forward the 2018 projection;
- named-controller/product evidence for ReMAR- or ReNAC-like policies;
- firmware/command traces showing when a real controller reads neighbor state after ECC failure;
- interaction with modern LDPC soft decoding, multi-step read retry, and read reclaim;
- fault-injection experiments separating neighbor-aware benefit from generic read-retry heuristics;
- later architecture evidence showing whether shared-charge-trap leakage geometry changes materially;
- broader BiCS/V-NAND/process genealogy in `computing-archaeology`, linked back here rather than duplicated.

## Sources

1. Yixin Luo, Saugata Ghose, Yu Cai, Erich F. Haratsch, Onur Mutlu, **“Improving 3D NAND Flash Memory Lifetime by Tolerating Early Retention Loss and Process Variation,”** *Proceedings of the ACM on Measurement and Analysis of Computing Systems* 2(3), Article 37, 2018, DOI `10.1145/3224432`; author-accessible full text: <https://arxiv.org/abs/1807.05140>.
2. Bongsik Choi et al., **“Comprehensive evaluation of early retention (fast charge loss within a few seconds) characteristics in tube-type 3-D NAND Flash Memory,”** *2016 IEEE Symposium on VLSI Technology*, Honolulu, 14–16 June 2016, DOI `10.1109/VLSIT.2016.7573385`.
3. C.-P. Chen, H.-T. Lue, C.-C. Hsieh, K.-P. Chang, K.-Y. Hsieh, C.-Y. Lu, **“Study of fast initial charge loss and its impact on the programmed states Vt distribution of charge-trapping NAND flash,”** *2010 IEEE International Electron Devices Meeting (IEDM)*, San Francisco, 6–8 December 2010, pp. 5.6.1–5.6.4 / 118–121, DOI `10.1109/IEDM.2010.5703304`.
4. Yu Cai, Gulay Yalcin, Onur Mutlu, Erich F. Haratsch, Osman Unsal, Adrian Cristal, Ken Mai, **“Neighbor-Cell Assisted Error Correction for MLC NAND Flash Memories,”** *ACM SIGMETRICS*, June 2014, pp. 491–504; institutional abstract: <https://istc-cc.cmu.edu/publications/papers/2014/neighbor-assisted-error-correction-in-flash_sigmetrics14_abs.shtml>.
5. **“Reliability of NAND Flash Memories: Planar Cells and Emerging Issues in 3D Devices,”** *Computers* 6(2):16, 2017, DOI `10.3390/computers6020016`, used as scholarly chronology/cross-check rather than as a substitute for primary evidence where mechanism claims are decisive.
