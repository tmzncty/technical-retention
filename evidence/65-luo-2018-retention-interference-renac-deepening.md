# Case 65 Deepening — 3D NAND Retention Interference and ReNAC (2018)

## Status

**`bounded deepening complete`** — this record isolates one mechanism that the canonical Case 65 previously kept only as context: **retention interference** in the 2018 Luo et al. 3D NAND study, and the corresponding **Retention Interference Aware Neighbor-Cell Assisted Correction (ReNAC)** research proposal.

This is a bounded extension of the existing early-retention/ReMAR case. It does not replace the broader grounding record, and it does not establish commercial deployment.

## Bounded research question

> What changes when retention loss is not determined by the victim cell's age alone, but is measurably conditioned by the stored state of a vertically adjacent cell, so that later recovery can use both time and neighbor state as interpretation inputs?

The question is deliberately narrower than a history of 3D NAND reliability. It asks what additional retained/control relation appears once **retention age alone is insufficient to describe the measured threshold-voltage shift**.

## Why this slice belongs in Case 65

The existing Case 65 already grounds:

- strongly front-loaded early retention loss in real 3D NAND MLC chips;
- age-dependent optimal read-reference voltage;
- ReMAR's use of block program time and P/E-cycle state;
- the distinction between read-reference adaptation and physical refresh/rewrite.

It previously kept `retention interference` only as a neighboring phenomenon. Luo et al. 2018, however, directly characterize that phenomenon and propose a separate read-recovery mechanism, ReNAC. That is enough evidence for a dedicated deepening without turning the case into a general 3D-NAND error catalogue.

## Source hierarchy

| Source | Type / date | Directly supports | Does not support |
| --- | --- | --- | --- |
| Yixin Luo, Saugata Ghose, Yu Cai, Erich F. Haratsch, Onur Mutlu, **“Improving 3D NAND Flash Memory Lifetime by Tolerating Early Retention Loss and Process Variation,”** POMACS 2018, DOI `10.1145/3224432`, arXiv `1807.05140v2` | peer-reviewed primary experimental systems/device study; 2018 | real-chip retention-interference measurement; shared-charge-trap mechanism as described by the authors; experimental separation from program interference; ReNAC proposal and its explicit current-generation limitation | named chip vendor/product; commercial ReNAC deployment; universal TLC/QLC behavior; proof that all later 3D NAND has identical coupling |
| Yu Cai et al., **“Neighbor-Cell Assisted Error Correction for MLC NAND Flash Memories,”** SIGMETRICS 2014 | peer-reviewed primary experimental/recovery paper | original NAC mechanism for program-interference-conditioned recovery; reread after ECC failure using neighbor-conditioned reference voltages | retention interference in 3D charge-trap NAND; ReNAC deployment |
| [`../cases/59-nand-program-interference-write-induced-neighbor-drift.md`](../cases/59-nand-program-interference-write-induced-neighbor-drift.md) | internal grounded case | existing repository genealogy and stop conditions for planar NAND program interference / NAC | proof that retention interference and program interference are the same physical mechanism |

Primary full text used for the central claims: <https://arxiv.org/pdf/1807.05140>.

## Historical record

### 1. Luo et al. identify a neighbor-conditioned retention effect

In §4.4, Luo et al. define **retention interference** as a change in the *speed of retention loss* that depends on the threshold voltage of a vertically adjacent neighbor cell. In the architecture they study, cells along the same bitline share a charge-trap layer. The authors describe charge moving through that shared charge-trap structure when neighboring cells differ in threshold voltage.

Their bounded physical description matters because it is not merely a statistical statement that two nearby cells fail together. The proposed relation is:

```text
vertically adjacent stored state
    -> shared charge-trap leakage relation
    -> victim threshold-voltage evolution over retention time
```

The authors describe a higher-voltage cell as capable of losing charge toward a lower-voltage neighbor, reducing the former threshold voltage while raising the latter.

This record treats that description as **the 2018 authors' mechanism for their tested 3D NAND architecture**. It does not generalize the exact path or magnitude to every later 3D NAND design.

### 2. The experiment explicitly separates retention interference from program interference

The paper does something methodologically important before interpreting the correlation. To reduce contamination from **program interference**, the authors use neighboring cells that were programmed **before** the victim cells, because those neighbors do not induce the later programming interference that Case 59 studies. They also exclude erased-state victims in this comparison because the paper identifies a separate program-interference sensitivity there.

After that control, the authors group victims by:

- victim threshold-voltage state;
- vertically adjacent neighbor state;
- threshold-voltage shift over a 24-day retention interval.

They report that the threshold-voltage shift is **lower when the neighboring cell is in a higher-voltage state**.

That experimental design supports a strong repository boundary:

> **neighbor-conditioned retention drift ≠ automatically residual program interference.**

The two phenomena can both be neighbor-dependent while occurring through different physical histories.

### 3. Age is necessary for the model, but age alone is not sufficient

ReMAR in the same paper uses retention time and wear state to estimate better read-reference voltages. ReNAC adds another variable: **neighbor-cell state**.

The ReNAC mechanism is described as an online retention-interference model whose output depends on:

```text
retention time + vertically adjacent neighbor state
    -> predicted neighbor-dependent read offset
```

The controller obtains retention time using a mechanism similar to ReMAR, then computes and applies the neighbor-dependent read offset for that time.

Therefore the historical mechanism itself already separates two control inputs:

> **data age ≠ complete retention-interference state estimate.**

A page can have the same retention age while individual cells experience different threshold evolution depending on neighboring stored state.

### 4. ReNAC is explicitly adapted from NAC, not invented as a generic refresh mechanism

Luo et al. compare the new retention-interference dependency with the previously known data dependency of **program interference**. They cite Neighbor-Cell Assisted Correction (`NAC`) as prior work for program-interference recovery and adapt the recovery form to the 3D retention-interference problem.

The 2014 NAC paper characterizes threshold-voltage distributions conditional on immediate-neighbor values and proposes rereading an ECC-failing page using reference voltages selected for those conditional distributions.

Luo et al. call the adapted mechanism **Retention Interference Aware Neighbor-Cell Assisted Correction (`ReNAC`)**.

The genealogy therefore supports:

```text
NAC recovery form
    -> adapted to a different measured dependency
    -> ReNAC
```

It does **not** support:

```text
program interference physical mechanism
    = retention interference physical mechanism
```

Functional reuse of a recovery pattern is not identity of the underlying failure physics.

### 5. The paper explicitly reports no meaningful current-generation lifetime improvement from ReNAC

This negative result is essential and must travel with the mechanism.

Luo et al. state that they are **unable to show meaningful flash-lifetime improvement from ReNAC for the current generation of 3D NAND tested**. Their measured retention-interference shift is less than two normalized voltage steps and is much smaller than the threshold-voltage changes caused by process variation and early retention loss in that device population.

The authors expect the effect to become more important with smaller cells and with TLC/QLC because state margins narrow, but they explicitly leave quantitative evaluation on future devices to future work.

Therefore:

> **ReNAC proposed ≠ ReNAC materially improves the tested current generation.**

And:

> **future TLC/QLC benefit expectation ≠ measured TLC/QLC benefit.**

This boundary prevents a research idea from being silently upgraded into a demonstrated contemporary product requirement.

## Engineering reconstruction

### A. Retention state can be relational rather than cell-local

For the early-retention-only path, a compact control description can start with age and wear:

```text
program time + P/E state
    -> expected retention evolution
```

Retention interference adds a relational variable:

```text
program time + P/E state + neighbor state
    -> more specific estimate of victim evolution
```

The key reconstruction is:

> **victim physical state ≠ physically self-contained retention trajectory.**

This does not make the neighbor part of the victim's logical payload. It means the neighbor can be part of the physical conditions under which that payload remains distinguishable.

### B. Same age does not imply same optimal recovery interpretation

Two cells can be equally old yet differ in neighbor state. If the measured retention-interference relation applies, their threshold-voltage shifts need not be identical.

Therefore:

> **same retention age ≠ same threshold-voltage trajectory ≠ necessarily same best recovery offset.**

This is a stricter result than ReMAR alone. ReMAR makes **time** constitutive read metadata; ReNAC makes **time plus spatially adjacent state** part of the proposed recovery model.

### C. Neighbor data becomes recovery side information without becoming payload ownership

ReNAC uses the adjacent stored value to select a read offset for the failed victim read. That gives the repository another example of **side information**:

> **neighbor value can participate in recovery ≠ neighbor value is part of victim logical identity.**

The neighboring data is an input to the decoding/reinterpretation path because it predicts a physical distortion; it is not copied into the victim's application-visible payload.

### D. ReNAC remains a read-path intervention, not physical renewal

The proposed mechanism changes the read reference and rereads data. It does not claim to restore leaked charge, erase and reprogram the block, or remap the payload to a fresh physical embodiment.

Therefore:

```text
neighbor-aware read offset
    != ECC itself
    != physical refresh
    != rewrite/remap
```

A successful reread can recover logical availability while the aged physical embodiment remains aged.

### E. Recovery can depend on state that is discovered only after an initial failure

The NAC lineage is explicitly a recovery path entered after ordinary ECC cannot correct a page. ReNAC adapts that recovery logic to retention interference and is summarized by Luo et al. as adapting the read reference and rereading after a read operation fails.

That creates another useful distinction:

```text
retained physical relation exists continuously
    != controller must continuously inspect it
    != recovery policy needs to consult it on every successful read
```

A latent physical relation can become operationally relevant only when the normal read path fails.

## Cross-case boundaries

### Versus Case 59 — program interference / NAC

Case 59 is bounded to planar floating-gate MLC **program interference**: a later neighboring program transition capacitively shifts an already-programmed victim. Program order is therefore central.

This deepening concerns 3D charge-trap **retention interference**: over retention time, the victim's leakage/threshold evolution is conditioned by a vertically adjacent stored state in a shared charge-trap structure.

Safe comparison:

```text
Case 59: neighbor program event + coupling
    -> victim threshold shift
    -> NAC can use neighbor value as recovery side information

Case 65 deepening: retention time + neighbor stored state
    -> neighbor-conditioned retention shift
    -> ReNAC adapts the NAC recovery form
```

Stop condition:

> **same neighbor-assisted recovery architecture ≠ same physical disturbance mechanism.**

### Versus Case 36 — Flash Correct-and-Refresh

Case 36 renews physical margin by correcting and then rewriting/remapping data. ReNAC changes interpretation on the existing embodiment.

Therefore:

> **neighbor-aware reread ≠ charge restoration.**

The two techniques could be composed in a controller, but composition does not make them one maintenance action.

### Versus Case 52 — read disturb

Read disturb is **access-induced**: repeated read/pass-voltage exposure perturbs other cells. Retention interference is **retention-time-dependent** and is conditioned by neighbor state without requiring repeated reads as its trigger.

Therefore:

> **retention interference ≠ read disturb.**

### Versus the main ReMAR path in Case 65

ReMAR asks:

```text
how old is this embodiment?
```

ReNAC adds:

```text
what state is the relevant neighbor in at this retention age?
```

The two are complementary interpretations of the same broad retention problem but rely on different sufficient statistics.

## Historical record / engineering reconstruction / functional analogy / interpretation ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| Luo et al. measured retention loss correlated with vertically adjacent neighbor state | `H/P` | directly inspected 2018 §§4.4, 6.4 |
| the authors attribute the bounded effect to charge movement through a shared charge-trap layer | `H/P` | 2018 §4.4; kept source-bounded |
| the experiment controls for program interference by choosing program order and excluding ER victims | `H/P` | 2018 §4.4 |
| ReNAC models retention interference as a function of retention time and neighbor state | `H/P` | 2018 §6.4 |
| ReNAC adapts the recovery form of earlier NAC | `H/P` | 2018 §6.4 plus 2014 NAC primary paper |
| current tested generation showed no meaningful ReNAC lifetime improvement | `H/P` | explicit 2018 §6.4 limitation |
| future TLC/QLC chips will definitely require ReNAC | `X` | authors express expectation, not measured proof |
| age alone is not a complete descriptor of measured retention evolution | `E` | reconstruction from neighbor-conditioned measurements/model |
| neighbor state can become recovery side information | `E` | reconstruction from ReNAC/NAC mechanism |
| ReNAC physically renews NAND charge | `X` | mechanism changes read offset and rereads; no rewrite claimed |
| retention interference is the same as Case 59 program interference | `X/A` | only functional analogy is allowed; trigger/physics/history differ |
| a retained object's future legibility can depend on another retained state | `I` | bounded philosophical interpretation; not historical actor vocabulary |

## Explicit non-claims

This deepening does **not** claim that:

1. Luo et al. identified the vendor or commercial product used in the 2018 experiment;
2. every 3D NAND generation exhibits the same retention-interference magnitude;
3. the paper's less-than-two-voltage-step result is a universal constant;
4. retention interference and program interference are synonyms;
5. the same physical charge-transfer path applies to planar floating-gate NAND;
6. ReNAC shipped in a commercial SSD controller;
7. a named vendor adopted ReNAC after 2018;
8. ReNAC materially improved lifetime in the current-generation devices tested by Luo et al.;
9. the authors experimentally demonstrated the projected TLC/QLC advantage;
10. neighbor-aware rereading restores lost charge;
11. ReNAC is equivalent to proactive NAND refresh/rewrite;
12. a neighbor's logical data becomes part of the victim application's payload;
13. all reads require neighbor inspection;
14. the 2018 paper proves the first-ever appearance of every kind of neighbor-conditioned retention behavior in nonvolatile memory;
15. the broad 3D NAND / charge-trap technology genealogy is complete here.

## Philosophical interpretation — bounded

One narrow conceptual pressure follows from the mechanism:

> **A retained state can remain materially local while its reliable future interpretation is relational.**

The victim page need not contain the neighbor's payload, yet the neighbor's state can help explain how the victim's physical margin evolved and how it should be reread after a failure.

That is an interpretation of the engineering relation, not a vocabulary attributed to Luo et al. or NAND vendors.

## Related-repository duplication check

A fresh repository search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `retention interference`, `ReNAC`, and `3D NAND` returned no dedicated topic to reuse in this pass.

Accordingly:

- the **retention-specific mechanism and policy relation** stays in `technical-retention`;
- any broader history of charge-trap architecture, BiCS/V-NAND product genealogy, layer scaling, or vendor process generations should be built in `computing-archaeology` and linked back later;
- Case 59 remains the repository home for the earlier program-interference/NAC genealogy rather than duplicating it here.

## Remaining evidence debt

This bounded slice closes the question “does the 2018 Case-65 source itself support a distinct neighbor-conditioned retention mechanism and a neighbor-aware recovery proposal?” It does **not** close several stronger questions:

- independent replication of retention interference in later named 3D NAND generations/vendors;
- direct measurement on TLC and QLC devices rather than the 2018 projection;
- commercial controller/firmware evidence for ReNAC-like neighbor-state-aware retention recovery;
- command/firmware traces showing when a real controller reads neighbor state after ECC failure;
- interaction with modern LDPC soft decoding and multi-step read retry;
- spatial extent beyond the directly modeled vertically adjacent relation;
- whether later architectures materially change or suppress the shared-charge-trap leakage relation;
- direct fault-injection evidence separating recovery benefit from ordinary read-retry heuristics in a named product.

## Sources

1. Yixin Luo, Saugata Ghose, Yu Cai, Erich F. Haratsch, Onur Mutlu, **“Improving 3D NAND Flash Memory Lifetime by Tolerating Early Retention Loss and Process Variation,”** *Proceedings of the ACM on Measurement and Analysis of Computing Systems* 2(3), Article 37, 2018, DOI `10.1145/3224432`. Author-accessible full text: <https://arxiv.org/abs/1807.05140>; PDF: <https://arxiv.org/pdf/1807.05140>.
2. Yu Cai, Gulay Yalcin, Onur Mutlu, Erich F. Haratsch, Osman Unsal, Adrian Cristal, Ken Mai, **“Neighbor-Cell Assisted Error Correction for MLC NAND Flash Memories,”** *ACM SIGMETRICS*, June 2014, pp. 491–504. Institutional abstract: <https://istc-cc.cmu.edu/publications/papers/2014/neighbor-assisted-error-correction-in-flash_sigmetrics14_abs.shtml>; author/institution PDF: <https://istc-cc.cmu.edu/publications/papers/2014/neighbor-assisted-error-correction-in-flash_sigmetrics14.pdf>.
3. Internal prior-art boundary: [`../cases/59-nand-program-interference-write-induced-neighbor-drift.md`](../cases/59-nand-program-interference-write-induced-neighbor-drift.md), especially the 2013 program-interference and 2014 NAC sections.
