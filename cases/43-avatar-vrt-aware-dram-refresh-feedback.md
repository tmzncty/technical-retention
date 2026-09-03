# AVATAR VRT-Aware DRAM Refresh: ECC Feedback, Scrubbing, and Runtime Row Reclassification

## Status

**`grounded`** — bounded to Qureshi et al.'s DSN 2015 AVATAR research design and evaluation. The case uses the paper's experimental characterization of variable-retention-time behavior in 24 DRAM chips to motivate a system-level controller design in which ECC-corrected runtime failures and proactive scrubbing can revise a row's refresh class.

Grounding record: [`../evidence/43-avatar-2015-vrt-aware-refresh-grounding.md`](../evidence/43-avatar-2015-vrt-aware-refresh-grounding.md).

## Scope

This case asks the narrow question left open by Case 40:

> What changes when a retained refresh profile is **revised at runtime by observed correctable failures**, rather than being trusted as a static description of row retention behavior?

AVATAR (`A Variable-Retention-Time (VRT) Aware Refresh for DRAM Systems`) combines:

1. initial retention testing that populates a `Row Refresh Table` (`RRT`);
2. multirate refresh with `SlowRefresh` and `Fast Refresh` classes;
3. ECC on ordinary accesses;
4. proactive memory scrubbing to inspect low-activity memory;
5. runtime row upgrades when ECC detects and corrects an error;
6. infrequent retention testing that can later downgrade rows again.

This is **not**:

- a full history of VRT physics or DRAM retention profiling;
- a claim that AVATAR shipped in a commercial controller;
- a JEDEC refresh-standard genealogy;
- a claim that ECC and refresh are one operation;
- a claim that scrubbing and refresh are one operation;
- a complete solution to data-pattern dependence (`DPD`);
- a RowHammer mitigation case;
- evidence that the modeled reliability numbers are field lifetimes of deployed hardware.

The bounded contribution is a **runtime maintenance-policy feedback regime**: observed correctable failures can become evidence that changes how frequently the affected row will be maintained in the future.

## Relation to Case 40

Case 40 establishes two facts that matter here:

```text
retention profile can be retained across time
    !=
retention profile remains conservative across time
```

The 2013 DPD/VRT evidence showed why a profile can survive perfectly while the relation it describes becomes incomplete or non-conservative.

Case 43 does not erase that problem. It changes the response:

```text
initial profile
    -> runtime ECC observation
    -> correction of current error
    -> row-class update
    -> faster future refresh
    -> proactive scrub for cold memory
    -> later retention re-test / possible downgrade
```

The changed relation is therefore:

> **maintenance-policy metadata can itself be maintained through runtime feedback.**

## Historical vocabulary and record

Moinuddin K. Qureshi, Dae-Hyun Kim, Samira Manabi Khan, Prashant J. Nair, and Onur Mutlu presented **“AVATAR: A Variable-Retention-Time (VRT) Aware Refresh for DRAM Systems”** at the 45th Annual IEEE/IFIP International Conference on Dependable Systems and Networks (DSN), 2015, pp. 427–437, DOI `10.1109/DSN.2015.58`.

The paper's own vocabulary includes:

- `AVATAR`;
- `Variable-Retention-Time (VRT) Aware Refresh`;
- `Active-VRT Pool (AVP)`;
- `Active-VRT Injection (AVI)`;
- `Row Refresh Table (RRT)`;
- `SlowRefresh`;
- `Fast Refresh`;
- `Data ECC`;
- `Scrub`;
- `Retention Testing`.

The authors experimentally characterize VRT behavior using **24 DRAM chips**, then use those observations to drive an architecture-level reliability/performance evaluation. The paper reports that new VRT-related failures can continue to appear after long testing, which is the reason it rejects reliance on a one-time static profile alone.

The paper's evaluation numbers are retained as **research-model results**, not commercial deployment measurements.

## Mechanism

### 1. Initial testing creates a row-refresh policy state

AVATAR begins with retention testing and stores the resulting row classification in the `Row Refresh Table`.

A row classified as ordinary can use the slower refresh regime. Rows known or later observed to require stronger protection can be placed in the faster regime.

The RRT is therefore not payload. It is retained **control state about how the payload should be maintained**.

### 2. ECC corrects a manifested error and supplies feedback

During normal accesses, AVATAR uses ECC to detect and correct a correctable data error. When a word in a row produces such an event, AVATAR upgrades the **row** to `Fast Refresh`.

This separates two actions:

```text
correct the value that is wrong now
    !=
change the maintenance policy intended to reduce future errors
```

Therefore:

> **error correction ≠ future protection**.

The first restores the currently observed logical value. The second changes the future refresh cadence for a larger spatial unit.

### 3. Demand accesses do not cover cold memory

ECC on ordinary reads/writes observes only lines that are actually accessed. A row that becomes vulnerable while remaining cold can therefore escape demand-triggered observation.

AVATAR adds periodic **memory scrub** to inspect all memory, correct detected errors, and feed the same row-upgrade path.

Therefore:

> **demand-triggered ECC observation ≠ full-memory coverage**.

And:

> **memory scrub ≠ DRAM refresh**.

Scrub is a verification/detection/correction traversal. Refresh is the charge-restoration operation whose cadence AVATAR changes. They cooperate in one retention policy but remain different work.

### 4. Conservative evidence is not perfectly specific evidence

The paper notes that a correctable ECC event can also be caused by a soft error. AVATAR can therefore conservatively upgrade a row even when the observed error was not caused by VRT.

So:

> **ECC correction event ≠ certain VRT diagnosis**.

In this design, the safe direction is to spend extra refresh work rather than risk leaving a truly weak row under-refreshed.

### 5. Runtime upgrade need not be permanent

If upgrades only accumulate, VRT observations can gradually move more rows into the fast class and erode refresh savings. AVATAR therefore includes infrequent retention testing — evaluated with a yearly interval — that can reclassify rows and move rows back to the slower refresh regime when the test supports doing so.

Thus:

> **conservative runtime upgrade ≠ irreversible classification**.

The maintenance-policy state has its own lifecycle: create, observe, revise, and periodically revalidate.

### 6. Reducing refresh adds other maintenance work

AVATAR reduces unnecessary DRAM refreshes by adding or relying on:

- ECC storage/checking/correction;
- a row-refresh table;
- runtime class updates;
- periodic whole-memory scrubbing;
- infrequent retention testing.

The paper explicitly evaluates scrub-period tradeoffs: scrubbing more frequently improves the modeled reliability margin but consumes more energy and foreground bandwidth.

Therefore:

> **less refresh work ≠ less total maintenance work**.

The policy spends observation, correction, metadata, and revalidation work to avoid some restoration work.

## Reliability and evidence boundary

The paper derives long modeled times to uncorrectable error from its VRT characterization and architectural assumptions. Those values are useful inside the paper's comparison, but they must not be rewritten as years of demonstrated field operation.

Two boundaries are especially important.

First, the design/evaluation assumes that a scrub interval identifies the VRT-related data errors that arise during that interval. That assumption is part of the model closure; it is not direct proof that every real platform scrub catches every possible interval failure.

Second, the paper evaluates AVATAR as a research architecture. It does not identify a shipped commercial processor, controller, DIMM, or JEDEC feature that implements AVATAR.

Therefore:

> **model-level reliability result ≠ deployed hardware lifetime**

and:

> **online VRT adaptation ≠ commercial retention-aware-refresh deployment**.

## Failure and forgetting boundaries

The case adds several failure modes above raw capacitor leakage:

- **missed observation** — a vulnerable cold line is not demand-accessed before an error accumulates;
- **scrub-latency exposure** — vulnerability appears between proactive inspections;
- **uncorrectable coincidence** — multiple relevant errors can exceed the assumed ECC correction envelope before policy catches up;
- **misclassification** — a non-VRT correctable error can cause an unnecessary fast-refresh upgrade;
- **stale policy state** — a row remains in a class no longer justified by its current behavior;
- **retest cost** — stronger revalidation consumes time/energy/bandwidth;
- **model-assumption failure** — actual VRT/error processes can depart from the fitted injection/coverage assumptions.

This extends Case 40's result. Retention failure can arise from a stale model of the substrate, but a feedback mechanism that revises the model is itself only as good as its observation coverage, correction envelope, and revalidation schedule.

## Prior art and anti-anachronism

AVATAR is not treated here as the invention of retention-aware refresh.

Case 40 already grounds RAIDR (2012), which uses profiled row-retention heterogeneity to select refresh cadence, and RAIDR itself cites earlier mechanisms such as Smart Refresh (2007). The 2013 experimental study then establishes DPD/VRT as a challenge to static profiling assumptions.

AVATAR's narrower historical contribution is therefore kept in the authors' own 2015 problem setting: use ECC plus scrub-derived runtime failures to adapt a multirate refresh policy under VRT.

The project term `maintenance-policy feedback` is an engineering reconstruction. It is not substituted for the paper's historical vocabulary.

## Functional analogy and philosophical limit

A bounded functional analogy can compare AVATAR to feedback-based preventive maintenance: a system observes correctable degradation and revises how aggressively it services the affected component.

The analogy stops there. AVATAR is not evidence that DRAM “knows itself,” remembers in a human sense, or performs diagnosis in the philosophical sense.

A narrow conceptual pressure does follow from the mechanism:

> A technical system can preserve payload partly by retaining a fallible description of how the substrate tends to fail, then revising that description when the substrate produces new evidence.

And:

> The state that says **how to remember** may itself require periodic correction and revalidation.

These are engineering/philosophical interpretations of the documented design, not claims about the authors' philosophical intentions.

## Cross-case result

The DRAM decomposition now includes a feedback loop that Case 40 left open:

```text
physical retention behavior
    -> initial profiling
    -> retained row-refresh class
    -> runtime error manifestation
    -> ECC detection/correction
    -> policy update
    -> changed future refresh cadence
    -> proactive scrub coverage
    -> later profile revalidation
```

The key addition is that **second-order retention infrastructure is no longer static**. It can itself be revised as the first-order substrate reveals failures.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| AVATAR is a DSN 2015 research design for VRT-aware multirate DRAM refresh | H/P | original paper + bibliographic record |
| Experimental motivation uses observations from 24 DRAM chips | H/P | original abstract/introduction |
| Initial retention testing populates a Row Refresh Table | H/P | original design section |
| A correctable ECC event upgrades the affected row to Fast Refresh | H/P | original design section |
| Periodic scrub is used to inspect low-activity memory and can trigger the same upgrade path | H/P | original design section |
| The evaluated default scrub interval is 15 minutes | H/P | original design/evaluation; paper-specific parameter, not a DRAM standard |
| Infrequent retention testing can later downgrade rows | H/P | original design section |
| The paper assumes scrub identifies VRT-related errors arising during the scrub interval | H/P | explicit design/evaluation assumption |
| ECC correction and future refresh reclassification are separate operations | E | reconstruction from documented control path |
| Scrub and refresh are separate maintenance operations | E/A | mechanism comparison; paper uses both as distinct paths |
| RRT/classification state is second-order retention infrastructure | E | project reconstruction |
| Reported reliability/refresh-savings results are research evaluation results, not commercial field lifetime | H/E | evidence-scope boundary |
| AVATAR was commercially deployed | X | not established by the bounded sources |
| AVATAR invented retention-aware DRAM refresh | X | contradicted by earlier profiled-refresh prior art |

## Sources

### Primary

- Moinuddin K. Qureshi, Dae-Hyun Kim, Samira Manabi Khan, Prashant J. Nair, and Onur Mutlu, **“AVATAR: A Variable-Retention-Time (VRT) Aware Refresh for DRAM Systems,”** DSN 2015, pp. 427–437, DOI `10.1109/DSN.2015.58`. Author/lab-hosted PDF: <https://memlab.ece.gatech.edu/papers/DSN_2015_1.pdf>.
- Carnegie Mellon ISTC mirror of the same paper: <https://www.istc-cc.cmu.edu/publications/papers/2015/avatar-dram-refresh_dsn15.pdf>.

### Bibliographic / institutional

- Georgia Tech Memory Systems Lab publication listing for the DSN 2015 paper.
- DBLP bibliographic record for DSN 2015, pp. 427–437.

## Related repository check

`tmzncty/computing-archaeology` was searched for `AVATAR`, `VRT`, `RAIDR`, and retention-aware DRAM refresh before this slice. No dedicated AVATAR/RAIDR retention-refresh case was found. The broader semiconductor-memory engineering history still belongs there; this case keeps only the retention-specific feedback comparison.
