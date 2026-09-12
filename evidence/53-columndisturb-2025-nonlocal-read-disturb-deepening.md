# Case 53 Deepening — ColumnDisturb: column-coupled DRAM read disturbance beyond RowHammer adjacency (2025)

## Status

**`grounded`** — bounded to the October 2025 ColumnDisturb experimental record and its direct implications for the retention-specific claims already made in Case 53. This evidence does **not** merge ColumnDisturb into RowHammer, does not claim a complete device-level causal model, and does not establish invention priority beyond the paper authors' own first-work statement.

## Why this deepening belongs in Case 53

Case 53 established a narrow RowHammer result: ordinary periodic refresh can be insufficient when access to one physical region accelerates loss in another, and maintenance may therefore need access-conditioned targeting rather than only elapsed-time scheduling. The case's 2012–2020 evidence was deliberately bounded to **row-neighbor disturbance** and RowHammer-targeted refresh.

Yüksel et al., *ColumnDisturb: Understanding Column-based Read Disturbance in Real DRAM Chips and Implications for Future Systems*, arXiv:2510.14750v2 (17 October 2025), supplies a useful later counterexample to any accidental generalization of that geometry. The authors experimentally report a **column/bitline-coupled** disturbance phenomenon in real DDR4 and HBM2 devices whose victim set can span multiple subarrays and thousands of rows.

The retention question for this repository is therefore not "is ColumnDisturb just another name for RowHammer?" It is:

> When access-induced retention loss is not confined to the row-neighbor topology assumed by a RowHammer-oriented policy, which parts of the older retention model survive, and which targeting assumptions must be reopened?

Primary source:

- İsmail Emir Yüksel, Ataberk Olgun, F. Nisa Bostancı, Haocong Luo, A. Giray Yağlıkçı, Onur Mutlu, **ColumnDisturb: Understanding Column-based Read Disturbance in Real DRAM Chips and Implications for Future Systems**, arXiv:2510.14750v2, 17 October 2025: <https://arxiv.org/abs/2510.14750>; HTML full text: <https://arxiv.org/html/2510.14750>.

## Historical / published experimental record (`H/P`)

### 1. The paper reports a different spatial disturbance geometry from RowHammer / RowPress

The authors describe RowHammer and RowPress as disturbing a few physically nearby rows within one subarray. ColumnDisturb instead manifests through DRAM columns / bitlines: repeatedly opening or keeping an aggressor row open perturbs columns, and cells sharing those physical columns can flip across multiple subarrays.

In the tested devices, a single aggressor-row episode could concurrently affect cells across **as many as three subarrays**, corresponding to **up to 3072 rows** in the evaluated DDR4 chips. The paper explicitly presents this as a conceptual and experimental difference from the local row-neighbor victim geometry of RowHammer / RowPress.

This is a measured research result for the tested population, not a universal architectural constant for every DRAM generation or organization.

### 2. The evaluated population is broad but still bounded

The study characterizes **216 DDR4 chips from 28 modules** plus **4 HBM2 chips**, covering three major DDR4 manufacturers; the HBM2 population is Samsung. The paper uses DRAM Bender / FPGA-based command control and reverse-engineers physical row/subarray organization needed for the experiments.

The authors report ColumnDisturb in chips from all three tested DDR4 manufacturers and describe increasing vulnerability with newer/smaller-node die revisions. Their technology-scaling inference is based on available die-revision ordering and experimental trends because exact commercial DRAM process-node information is generally not public.

Therefore:

> **broad multi-vendor experimental coverage != universal proof for every DDR4/HBM2 device**.

### 3. Standard refresh-window compliance does not imply immunity to this disturbance mode

The paper reports ColumnDisturb bitflips in some tested devices **within a nominal DDR4 refresh window**, including a cited minimum-time observation around **63.6 ms** for one module. This is directly relevant to Case 53's earlier distinction between ordinary scheduled refresh and access-conditioned disturbance risk.

The bounded historical conclusion is:

> **ordinary periodic refresh timing can be met while an access-induced disturbance failure still occurs**.

That conclusion is common in shape to RowHammer but the victim geometry and proposed causal path differ.

### 4. ColumnDisturb victims are not reducible to ordinary retention-failure rows

The paper explicitly filters retention failures in its methodology and compares ColumnDisturb failures against ordinary retention failures. Across tested refresh intervals, it reports many more rows experiencing ColumnDisturb bitflips than retention failures; the maximum reported increase in affected-row count is **up to 198x** in the tested population.

This provides a later, independent pressure on a relation already important in Case 53:

> **ordinary retention weakness != access-induced disturbance victimhood**.

It does not mean retention behavior is irrelevant to ColumnDisturb; it means an ordinary retention profile alone does not identify the full disturbance-victim set observed by the paper.

### 5. Retention-aware refresh loses benefit when its "weak-row" set omits disturbance-weak rows

Section 6.2 evaluates retention-aware heterogeneous refresh, including a RAIDR-based simulation. The paper's analysis marks rows that fail under ColumnDisturb as an expanded weak-row population relative to ordinary retention-only profiling.

For a 1024 ms strong-row retention assumption, the paper reports that accommodating ColumnDisturb increases required refresh operations by **3.02x on average and up to 14.43x** relative to the retention-only baseline across its tested modules. In the evaluated RAIDR configurations, the larger weak-row population substantially reduces — and for one space-efficient configuration can nearly eliminate — the simulated performance/energy benefit.

These are paper-specific experiment/simulation results, not a measured production-system SLA and not a universal constant for RAIDR-like designs.

### 6. Global faster refresh and targeted ColumnDisturb mitigation remain different policies

The authors evaluate a straightforward response that increases global refresh frequency and contrast it with proactively refreshing identified ColumnDisturb victims. In their modeled 32 Gb DDR5 configuration, moving the all-bank refresh period from 32 ms to 8 ms produces a **42.1% throughput-loss figure**; their proposed targeted approach reduces the modeled overhead relative to that straightforward solution.

For this repository, the useful historical point is not the exact modeled percentage. It is that the 2025 paper itself preserves the distinction already present in Case 53:

> **global extra refresh != topology-/risk-targeted extra refresh**.

## Engineering reconstruction (`E`)

### A. Disturbance topology is part of the retention contract, not merely a locator detail

Case 53 modeled RowHammer retention as depending on an aggressor/victim **physical-adjacency relation**. ColumnDisturb shows that "adjacency" is too specific to elevate into the general rule. A safer cross-case model is:

```text
access episode
    + hidden physical coupling relation
    + disturbance accumulation
    -> victim set whose maintenance urgency changes
```

For RowHammer, the relevant relation is row-neighbor / wordline-oriented. For ColumnDisturb, the reported relation follows shared physical columns / bitlines across subarray boundaries.

Therefore:

> **access-history detection != complete victim-resolution knowledge**.

and:

> **row-neighbor topology != universal DRAM disturbance topology**.

A controller can correctly identify a frequently opened row yet still lack enough information to infer every physically coupled victim under a different disturbance mechanism.

### B. A policy may retain the right history but apply it to the wrong spatial domain

Many RowHammer defenses count, sample, or probabilistically react to aggressor-row activity. ColumnDisturb does not make such history meaningless: aggressor activation/on-time still matters in the 2025 experiments. What changes is the mapping from that history to the victim set that deserves restoration.

Thus:

> **sufficient aggressor-history evidence != sufficient victim-coverage policy**.

The retention failure can be a policy-resolution error even when the system has correctly remembered that an aggressor was active.

### C. "Strong row" is conditional on the failure model used to classify it

Retention-aware heterogeneous refresh calls a row strong when it survives a chosen no-disturbance retention interval. ColumnDisturb supplies a distinct access-conditioned route to failure. The same row can therefore be "strong" under a retention-only profiler while still lying in a disturbance-vulnerable column relation.

Project reconstruction:

> **retention-profile classification != mechanism-independent robustness classification**.

This does not invalidate retention profiling. It constrains the domain of the inference made from that profile.

### D. Maintenance localization can fail because the failure relation is wider than the optimization relation

RAIDR-like policies save work by classifying most rows as strong and refreshing them less often. The ColumnDisturb paper's expanded disturbance-victim population erodes that optimization because more rows require protective work under the new failure model.

The general retention result is:

> **maintenance savings obtained by narrowing the protected set depend on the completeness of the failure model used to define that set**.

A newly observed coupling mechanism can convert previously "uninteresting" rows into maintenance subjects without changing their ordinary retention-time measurement.

### E. Refresh completion is still not mechanism proof

A refresh restores charge to a targeted row, but observing or scheduling refresh does not establish why the row needed it or whether every relevant victim was included. Therefore:

> **refresh action != proof of disturbance mechanism**;
>
> **refresh of one inferred victim set != proof of complete victim coverage**.

This preserves the repository's separation between an action, its policy trigger, the hidden physical relation, and the resulting integrity state.

## Functional analogy (`A`) — explicitly bounded

ColumnDisturb is **functionally analogous** to RowHammer only at a high level:

- an access pattern directed at one DRAM region can increase another retained state's risk;
- ordinary time-based refresh can be insufficient under that access pattern;
- extra restoration can trade performance/energy for integrity;
- topology knowledge and policy state can determine which additional rows are maintained.

The analogy stops there. The 2025 paper explicitly argues for a different victim geometry and a bitline-voltage-oriented explanation. Therefore:

> **ColumnDisturb ~ RowHammer as access-induced retention disturbance** (`A`)
>
> **ColumnDisturb == RowHammer mechanism** (`X`)

The same boundary applies to Case 52 NAND read disturb and Case 70 magnetic-core half-select disturbance. All show that an operation on one logical target can impose retention cost elsewhere, but their media, coupling physics, state variables, timescales, and maintenance mechanisms are not interchangeable.

## Philosophical interpretation (`I`) — bounded

ColumnDisturb adds one modest refinement to the repository's retention vocabulary:

> the relevant "neighborhood" of retained state is operation- and mechanism-relative, not necessarily the neighborhood exposed by the logical address model or by a previously known failure mechanism.

This is a project interpretation derived from the engineering comparison. It is **not** terminology used by the 2025 authors and must not be projected backward into the 2012–2020 RowHammer record.

## Prior-art / chronology boundary

The authors state that their work is the first experimental demonstration and characterization of a column-based read-disturb phenomenon they call ColumnDisturb in real DRAM chips. This repository records that as an **author claim attached to the 2025 publication**, not as independently proven invention priority.

The existence of much earlier RowHammer, RowPress, ordinary retention, bitline-architecture, and read-disturb literature means the safe historical statement is narrow:

> **2025 ColumnDisturb paper != invention of DRAM read disturbance generally**.

No direct genealogy is asserted from RowHammer/TRR to ColumnDisturb, nor from retention-aware refresh research to the newly characterized physical effect.

A fresh search of `tmzncty/computing-archaeology` for `ColumnDisturb` and `RowPress` found no dedicated technical-history module to reuse. If a broader bitline/open-bitline disturbance genealogy, device-physics prior-art chain, or first-introduction audit is built later, it belongs there; this evidence keeps only the retention-policy counterexample needed by Case 53.

## Stop conditions / rejected claims (`X`)

This evidence does **not** establish that:

- ColumnDisturb is the same mechanism as RowHammer or RowPress;
- every DDR4, HBM2, DDR5, or future DRAM device is vulnerable in the same way;
- three subarrays / 3072 rows is a universal blast radius;
- `63.6 ms`, `198x`, `3.02x`, `14.43x`, or any simulation overhead is a universal hardware threshold;
- a retention-only profile is useless, only that its inference domain does not automatically cover a different access-induced failure mechanism;
- current TRR/RFM mechanisms necessarily do or do not mitigate ColumnDisturb unless separately measured or specified;
- the 2025 paper independently proves invention priority;
- observed refresh success proves complete coverage of hidden physical victims;
- bitflips imply secure deletion, sanitization, or controlled forgetting.

## What remains open

1. **Independent reproduction / named-product validation** — repeat ColumnDisturb characterization outside the originating research group and correlate with exact DIMM/HBM product revisions where disclosure permits.
2. **Device-level causal evidence** — distinguish the paper's empirical evidence from its bitline-voltage hypothesis using direct device/circuit evidence.
3. **DDR5 / RFM interaction** — test whether specific RFM/PRAC/DRFM implementations cover the nonlocal victim geometry rather than assuming RowHammer-oriented mitigation transfers automatically.
4. **2026 ColumnKeeper follow-up** — separately evaluate the later mitigation paper rather than importing proposed-policy results into this physical-effect evidence.
5. **Historical genealogy** — trace pre-2025 column/bitline disturbance observations and open-bitline architecture work in `computing-archaeology` before making any first-introduction claim.

## Evidence-strength summary

- **Direct experimental record:** strong for the tested 216 DDR4 + 4 HBM2 chips and the paper's reported failure distributions (`H/P`).
- **Mechanism identity:** bounded; the paper presents substantial empirical evidence and a bitline-voltage hypothesis, but this repository does not elevate that into universal device-physics proof (`H/P`, `X`).
- **Cross-case retention reconstruction:** strong as a logical consequence of the measured nonlocal victim geometry and retention-aware-refresh evaluation (`E`).
- **Historical priority:** deliberately weak beyond the paper's own first-work claim; broader genealogy remains open (`H/P`, `X`).
