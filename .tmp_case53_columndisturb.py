from pathlib import Path
import re

EVIDENCE_PATH = Path('evidence/53-columndisturb-2025-nonlocal-read-disturb-deepening.md')
CASE_PATH = Path('cases/53-dram-rowhammer-targeted-refresh-policy.md')
ROADMAP_PATH = Path('ROADMAP.md')
INDEX_PATH = Path('CASE_INDEX.md')

EVIDENCE = r'''# Case 53 Deepening — ColumnDisturb: column-coupled DRAM read disturbance beyond RowHammer adjacency (2025)

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
'''

CASE_APPEND = r'''

## 2025 ColumnDisturb deepening: disturbance topology is not always row adjacency

Follow-up evidence: [`../evidence/53-columndisturb-2025-nonlocal-read-disturb-deepening.md`](../evidence/53-columndisturb-2025-nonlocal-read-disturb-deepening.md).

Yüksel et al. (arXiv:2510.14750v2, 17 October 2025) experimentally report **ColumnDisturb**, a later DRAM read-disturbance phenomenon whose measured victim relation follows shared physical columns / bitlines across multiple subarrays rather than only the few row-neighbor victims associated with RowHammer / RowPress. Their tested population comprises 216 DDR4 and 4 HBM2 chips; the reported blast radius reaches as many as three subarrays / 3072 rows in tested DDR4 chips, and some tested devices exhibit bitflips within a nominal refresh window.

This does **not** extend the historical scope of the original 2012–2020 RowHammer case by silently calling ColumnDisturb "RowHammer." It supplies a bounded later counterexample to one possible overgeneralization of Case 53's engineering model:

> **physical row adjacency is one disturbance topology, not a universal definition of access-induced DRAM retention risk**.

The safer reconstruction is `access history + hidden physical coupling relation -> disturbance-conditioned victim set`. RowHammer instantiates that relation with row-neighbor coupling; ColumnDisturb's published experiments instead implicate shared columns / bitlines across subarray boundaries.

The deepening also sharpens the link to Cases 40/43. The 2025 paper compares ordinary retention failures with ColumnDisturb victims and reports a substantially wider disturbance-weak population, then shows that this expanded weak-row set can sharply reduce the simulated benefit of RAIDR-style heterogeneous refresh. Therefore **retention-profile classification != mechanism-independent robustness classification**. A row that is "strong" under a no-disturbance retention test is not thereby proven safe under every access-conditioned coupling mechanism.

Historical record, engineering reconstruction, analogy, and interpretation remain separate: the authors' claim of a first experimental ColumnDisturb demonstration is recorded as an author claim rather than independently verified invention priority; ColumnDisturb is only functionally analogous to RowHammer at the access-induced-retention level; and the project phrase "mechanism-relative retention neighborhood" is not attributed to the paper's actors.
'''

ROADMAP_APPEND = r'''

## Completed bounded deepening — Case 53 ColumnDisturb topology counterexample (2026-09-12)

- Added [`evidence/53-columndisturb-2025-nonlocal-read-disturb-deepening.md`](evidence/53-columndisturb-2025-nonlocal-read-disturb-deepening.md), grounded in Yüksel et al., arXiv:2510.14750v2 (17 October 2025).
- Extended Case 53 without merging mechanisms: RowHammer's row-neighbor victim relation is now explicitly bounded against ColumnDisturb's experimentally reported column/bitline-coupled victims across multiple subarrays.
- Added the engineering distinction `aggressor-history evidence != complete victim-coverage policy` and the cross-case result `retention-profile classification != mechanism-independent robustness classification`.
- Recorded the paper's 216-DDR4 + 4-HBM2 test population, within-refresh-window failures in some tested devices, and its retention-aware-refresh/RAIDR implications while keeping all numeric outcomes sample/model bounded.
- Preserved chronology discipline: the 2025 paper's "first" language is stored as an author claim, not independently established invention priority; broader bitline/read-disturb genealogy remains a `computing-archaeology` task.
- Fresh `tmzncty/computing-archaeology` searches for `ColumnDisturb` and `RowPress` found no reusable dedicated module, so no duplicate historical genealogy was created here.
'''

FINDINGS = [
    ("2025 ColumnDisturb publication record", "Yüksel et al. arXiv:2510.14750v2 (17 Oct 2025) experimentally report a column/bitline-based read-disturbance phenomenon in commodity DRAM; this is a later deepening witness, not vocabulary projected into the 2012–2020 RowHammer record.", "H/P"),
    ("broad tested population != universal device claim", "the study covers 216 DDR4 and 4 HBM2 chips, with DDR4 devices from three major manufacturers, but those samples do not prove identical behavior for every DRAM device or generation.", "H/P, X"),
    ("RowHammer victim geometry != ColumnDisturb victim geometry", "the paper contrasts RowHammer/RowPress's few neighboring-row victims in one subarray with ColumnDisturb cells sharing physical columns/bitlines across multiple subarrays.", "H/P, A, X"),
    ("single aggressor episode can have nonlocal victim scope", "in tested DDR4 chips the reported ColumnDisturb blast radius reaches as many as three subarrays / 3072 rows; the number is a bounded experimental maximum rather than a universal architectural constant.", "H/P, X"),
    ("ordinary refresh-window compliance != access-disturbance immunity", "some tested devices exhibit ColumnDisturb bitflips within a nominal DDR4 refresh window, so scheduled refresh timing alone does not establish immunity to this access-induced failure mode.", "H/P, E"),
    ("ordinary retention-weak set != ColumnDisturb-weak set", "the paper filters retention failures and reports ColumnDisturb affecting many more rows, up to 198x in the tested population, preventing ordinary retention profiling from being treated as a complete disturbance-victim oracle.", "H/P, E"),
    ("retention-profile classification != mechanism-independent robustness classification", "a row classified strong under no-disturbance retention testing may still participate in an access-conditioned physical coupling relation that creates a different failure route.", "E"),
    ("aggressor-history evidence != complete victim-coverage policy", "correctly remembering/counting aggressor activity does not by itself reveal every victim if the maintenance policy assumes the wrong physical coupling topology.", "E"),
    ("row-neighbor topology != universal DRAM disturbance topology", "Case 53's RowHammer adjacency relation is one mechanism-specific instance; the safer project model uses a hidden physical coupling relation whose shape must be established separately.", "E, X"),
    ("retention-aware refresh savings depend on failure-model completeness", "the 2025 RAIDR analysis expands the weak-row population with ColumnDisturb victims and shows substantially reduced simulated refresh savings; selective maintenance efficiency is conditional on the classification model's coverage.", "H/P, E"),
    ("global faster refresh != targeted ColumnDisturb maintenance", "the paper separately evaluates globally shorter refresh periods and proactive victim refresh, preserving the distinction between blanket maintenance cadence and topology/risk-targeted work.", "H/P, E"),
    ("ColumnDisturb ~ RowHammer only at access-induced-retention level", "both can make another retained state unsafe through workload activity, but their reported victim geometries and proposed physical pathways are not interchangeable.", "A, X"),
    ("ColumnDisturb ~ NAND read disturb / core half-select only functionally", "Cases 52 and 70 likewise show operations imposing retention cost elsewhere, but media physics, topology, timescales, and maintenance mechanisms remain distinct.", "A, X"),
    ("mechanism-relative retention neighborhood is project interpretation", "the idea that a retained state's relevant neighborhood depends on the operative coupling mechanism is a repository-level interpretation, not terminology attributed to the 2025 authors.", "I, X"),
    ("2025 first-work statement != independently proven invention priority", "the authors' first experimental demonstration claim is recorded as their claim; older DRAM read-disturb, bitline-architecture, RowHammer, RowPress, and retention literature prevent a broader invention claim without a dedicated genealogy.", "H/P, X"),
    ("related-repository boundary", "fresh computing-archaeology searches for ColumnDisturb and RowPress found no dedicated reusable module; broader bitline/open-bitline disturbance genealogy belongs there if developed, while Case 53 keeps the retention-policy counterexample.", "H/P project-state record"),
]

# Create / verify evidence.
if EVIDENCE_PATH.exists():
    existing = EVIDENCE_PATH.read_text()
    if existing != EVIDENCE:
        raise SystemExit(f'{EVIDENCE_PATH} exists with unexpected content')
else:
    EVIDENCE_PATH.write_text(EVIDENCE)

# Append the bounded deepening to Case 53.
case = CASE_PATH.read_text()
marker = '## 2025 ColumnDisturb deepening: disturbance topology is not always row adjacency'
if marker not in case:
    CASE_PATH.write_text(case.rstrip() + CASE_APPEND + '\n')

# Add a completed roadmap record.
roadmap = ROADMAP_PATH.read_text()
roadmap_marker = '## Completed bounded deepening — Case 53 ColumnDisturb topology counterexample (2026-09-12)'
if roadmap_marker not in roadmap:
    ROADMAP_PATH.write_text(roadmap.rstrip() + ROADMAP_APPEND + '\n')

# Update the Case 53 catalog row and append sequential findings without assuming the current max ID.
index = INDEX_PATH.read_text()
old_row_tail = '[2012–2020 RowHammer/targeted-refresh grounding](evidence/53-rowhammer-2012-2020-targeted-refresh-grounding.md); later DDR5 RFM, exact JEDEC chronology, post-2020 defenses, and independent named-product validation remain separate work |'
new_row_tail = '[2012–2020 RowHammer/targeted-refresh grounding](evidence/53-rowhammer-2012-2020-targeted-refresh-grounding.md) + [2025 ColumnDisturb topology deepening](evidence/53-columndisturb-2025-nonlocal-read-disturb-deepening.md); later DDR5 RFM/ColumnDisturb interaction, exact JEDEC chronology, independent reproduction, and device-level causal validation remain separate work |'
if old_row_tail in index:
    index = index.replace(old_row_tail, new_row_tail, 1)
elif new_row_tail not in index:
    raise SystemExit('Case 53 catalog-row anchor not found')

section_marker = '## Case 53 — 2025 ColumnDisturb topology deepening findings'
if section_marker not in index:
    ids = [int(x) for x in re.findall(r'\*\*(\d+)\s+—', index)]
    start = (max(ids) + 1) if ids else 1
    lines = ["", "", section_marker, "", "Deepening record: [`evidence/53-columndisturb-2025-nonlocal-read-disturb-deepening.md`](evidence/53-columndisturb-2025-nonlocal-read-disturb-deepening.md).", ""]
    for off, (title, body, tags) in enumerate(FINDINGS):
        lines.append(f'- **{start + off} — {title}:** {body} (`{tags}`)')
    index = index.rstrip() + '\n'.join(lines) + '\n'
INDEX_PATH.write_text(index)

# Basic consistency checks.
for p in (EVIDENCE_PATH, CASE_PATH, ROADMAP_PATH, INDEX_PATH):
    if not p.exists() or not p.read_text().strip():
        raise SystemExit(f'missing/empty expected output: {p}')
assert '53-columndisturb-2025-nonlocal-read-disturb-deepening.md' in CASE_PATH.read_text()
assert '53-columndisturb-2025-nonlocal-read-disturb-deepening.md' in INDEX_PATH.read_text()
assert roadmap_marker in ROADMAP_PATH.read_text()
print('Case 53 ColumnDisturb integration prepared')
