# NAND Flash Correct-and-Refresh: ECC-Bounded Retention Through Controller Maintenance

## Status

**`grounded`** — bounded to Yu Cai et al.'s peer-reviewed 2012 ICCD proposal and evaluation of **Flash Correct-and-Refresh (FCR)** for 3x-nm MLC NAND Flash, with later 2015 retention-characterization work used only as a boundary check on retention-age/read-recovery semantics.

Grounding record: [`../evidence/36-cai-2012-flash-correct-refresh-grounding.md`](../evidence/36-cai-2012-flash-correct-refresh-grounding.md).

## Scope

This case asks a narrow question left open by Cases 04, 13, and 15:

> What changes when a physically nonvolatile Flash medium is treated as requiring periodic controller/software maintenance in order to keep accumulated retention errors inside an ECC-qualified reliability margin?

The 2012 FCR paper proposes three related controller/software policies:

- **remapping-based FCR** — read a valid block, correct accumulated errors with ECC, program corrected data to a free block, and remap the logical address;
- **hybrid reprogramming/remapping FCR** — usually restore charge in place, but remap when accumulated right-shift/program errors become too large;
- **adaptive-rate FCR** — change refresh cadence as block wear / P/E-cycle count changes rather than assuming one fixed interval for the entire device lifetime.

This is **not**:

- evidence that all NAND Flash or all SSDs require the same refresh policy;
- evidence that the proposed FCR algorithms were commercially deployed exactly as simulated;
- a claim that Flash is physically volatile in the DRAM sense;
- a claim that Flash `refresh` and DRAM refresh are the same historical mechanism;
- a general history of NAND reliability, ECC, read-retry, LDPC, 3D NAND, or SSD firmware;
- an invention-priority claim for Flash refresh.

The bounded object is the **2012 FCR proposal/evaluation as an explicit retention-maintenance regime**.

## Historical vocabulary and record

The primary paper is Yu Cai, Gulay Yalcin, Onur Mutlu, Erich F. Haratsch, Adrian Cristal, Osman S. Unsal, and Ken Mai, **“Flash Correct-and-Refresh: Retention-Aware Error Management for Increased Flash Memory Lifetime,”** presented at the 30th IEEE International Conference on Computer Design (ICCD), Montreal, September 2012, pp. 94–101, DOI `10.1109/ICCD.2012.6378623`.

Its own vocabulary includes:

- `retention errors`;
- `Flash Correct-and-Refresh (FCR)`;
- `remapping-based FCR`;
- `in-place reprogramming`;
- `hybrid FCR`;
- `adaptive-rate FCR`;
- `program/erase (P/E) cycles`;
- `raw BER (RBER)` / `uncorrectable BER (UBER)`;
- `error correcting codes (ECC)`;
- `flash translation layer (FTL)`;
- `wear leveling` and `garbage collection`.

The authors characterize retention errors as errors caused when an already-programmed floating-gate cell gradually loses charge and its threshold-voltage state can cross a read-reference boundary. In their measured 3x-nm MLC population, retention error rate increases with retention time and P/E wear, and the paper treats retention errors as the dominant error class in that bounded experimental regime.

The central proposal is explicit: periodically **read, correct, and refresh** stored data before accumulated retention errors exceed the correction capability of the selected ECC. `Refresh` in this paper means either reprogramming or remapping, not a DRAM row-restore command.

## Retained state and constitutive control state

The bounded FCR regime contains several separable states:

1. **cell state** — threshold-voltage / charge distributions encoding MLC values;
2. **logical payload** — the error-corrected page/block value presented by the SSD;
3. **ECC margin** — how many raw errors can still be corrected before UBER violates the target;
4. **mapping / validity state** — which physical block currently embodies the logical address and which blocks contain valid data;
5. **wear state** — per-block P/E-cycle counts used by adaptive-rate FCR and already maintained for wear leveling;
6. **maintenance policy state** — which blocks need refresh and at what rate.

`ECC margin`, `maintenance policy state`, and `retention qualification` are project reconstruction terms. They are not presented as period vocabulary.

## Engineering reconstruction

### Nonvolatility does not guarantee maintenance-free reliable retention

The Flash cell remains physically nonvolatile: power is not required merely to prevent immediate disappearance of the programmed state. Yet the paper's mechanism begins from a different requirement — keeping raw retention errors below an ECC-bounded reliability threshold over a desired service interval.

Therefore:

> **nonvolatile medium ≠ maintenance-free reliable retention at a specified error target**.

This does not redefine Flash as volatile. It separates **unpowered physical persistence** from **continued system-level recoverability with a bounded error budget**.

### Raw-state degradation can precede logical data loss

The paper explicitly places ECC between raw Flash reads and host-visible corrected data. Retention errors can accumulate in the physical readout while the controller still reconstructs the correct logical page.

Therefore:

> **raw physical error accumulation ≠ immediate logical payload loss**.

But the same relation creates a deadline of another kind: once accumulated errors outrun ECC capability, the page may no longer be recoverable by that path.

Thus:

> **ECC-correctability margin ≠ indefinite retention margin**.

FCR acts before that margin is exhausted.

### Long logical retention can be composed from shorter physical-retention intervals

The paper gives a deliberately concrete model result: with its examined 3x-nm MLC data and a fixed 512-bit BCH code, a much shorter guaranteed storage interval permits many more P/E cycles than a three-year interval. It uses the example of refreshing every three days to synthesize a much longer logical storage requirement.

The numerical values are **experiment/model specific**, not universal NAND laws. The retention relation is more general:

> **long logical retention interval ≠ one uninterrupted physical-embodiment interval**.

Repeated correction and rewriting can make the later logical state depend on a sequence of shorter, renewed physical embodiments.

### Flash refresh can preserve identity by changing location

In remapping-based FCR the controller:

1. selects valid data needing refresh;
2. reads it page by page;
3. corrects accumulated errors with ECC;
4. programs the corrected data into a new free block;
5. remaps the logical address.

Therefore:

> **retention maintenance ≠ location stability**.

This directly extends Case 04. Case 04 grounds relocation under rewrite/reclamation pressure; Case 36 adds a different trigger — **retention-error margin** — for deliberately replacing the physical embodiment while preserving logical identity.

### `Refresh` is not one physical operation

The paper itself contrasts NAND with DRAM. Its remapping path rewrites corrected payload into another erased block. Its in-place path instead uses ISPP to add charge back to cells whose retention error came from charge loss.

Therefore:

> **Flash FCR `refresh` ≠ DRAM refresh**.

The shared word names a functional goal — restore usable state before loss — while the substrate constraints, granularity, controller role, rewrite geometry, and side effects differ.

### Maintenance can consume the lifetime it is trying to extend

Periodic remapping creates additional erase cycles because old blocks eventually become reclaimable. The paper explicitly observes an inflection point for some workloads where increasing remap frequency can reduce lifetime.

Therefore:

> **more maintenance ≠ more lifetime**.

A retention operation can spend endurance in order to preserve error margin.

The in-place path exposes a second counterexample. Reprogramming can correct left-shift retention errors by adding charge, but it can also create program-interference errors and cannot repair right-shift errors requiring charge removal. Hybrid FCR therefore monitors right-shift error count and falls back to remapping when the threshold is exceeded.

Hence:

> **maintenance operation ≠ error-neutral repair**.

Retention work can create a different failure mechanism while suppressing the original one.

### Refresh cadence can depend on retained wear history

Adaptive-rate FCR starts with no refresh while retention errors remain inside the selected ECC margin, then increases refresh frequency as P/E cycles accumulate. The paper notes that per-block P/E-cycle information is already maintained for wear leveling.

Therefore:

> **refresh cadence ≠ one fixed medium constant**.

And:

> **payload retention can depend on retained maintenance metadata**.

The system needs a remembered wear relation in order to decide how much future retention work to perform.

### Maintenance competes with ordinary service and requires power

The paper says FCR requires powered Flash, can run with lower priority or during idle periods, and can be interrupted to reduce response-time impact.

Thus the proposed persistence is not a free background property. It consumes controller time, Flash operations, energy, and a service window.

## Failure and forgetting boundaries

Within this bounded regime, loss can occur through several distinct paths:

- charge leakage and threshold-voltage drift increase raw retention errors;
- ECC can mask/correct those errors until its capability is exceeded;
- remap-based refresh can consume additional erase/endurance budget;
- in-place reprogramming can introduce program-interference errors;
- a refresh policy that is too slow can allow correctability margin to expire;
- a refresh policy that is too aggressive can spend endurance or create new errors;
- powered-controller maintenance cannot execute while the device remains unpowered;
- losing mapping/validity/wear metadata would undermine the policy even if payload charge still exists.

Forgetting is therefore not one event. In this case it can be **physical drift beyond a recoverable threshold**, **loss of the logical-currentness relation**, or **failure of the maintenance regime to renew error margin in time**.

## Prior art and anti-anachronism

The 2012 paper includes a bounded authorial priority statement (“to our knowledge”) about its combination of retention-error characteristics. This repository does **not** promote that into an invention-priority claim without a broader historical search.

Nor does it project the FCR term backward onto earlier Flash. Cases 11–13 and 04 preserve their own period vocabulary and mechanisms. `FCR` is used historically only for the 2012 proposal and its later descendants/citations where explicitly sourced.

A 2015 follow-up by Cai et al. characterizes retention age in real 2y-nm MLC NAND and shows that optimal read-reference voltage changes with retention age. That later evidence deepens the general point that retained charge, readable interpretation, and controller recovery parameters can diverge over time. It is not used to rewrite the 2012 FCR mechanism or claim deployment.

## Functional analogy and philosophical limit

A bounded analogy to DRAM is useful only at this level:

> both systems can make later recoverability depend on maintenance before an error/decay boundary is crossed.

The analogy stops immediately after that functional relation. DRAM refresh is constitutive periodic restoration of volatile dynamic-cell state; FCR is a proposed controller/software reliability policy over a nonvolatile, erase/endurance-constrained medium with ECC and remapping.

The case creates one narrow conceptual pressure:

> A substrate may be called nonvolatile while a particular **reliability-qualified continuation relation** over that substrate becomes operational and maintenance-dependent.

That is an engineering/philosophical interpretation. It is not evidence that the 2012 authors were making a philosophical claim about persistence.

## Cross-case result

Case 36 extends the Flash/SSD comparison as follows:

```text
floating-gate charge state
    !=
raw readout / retention-error population
    !=
ECC-correctable logical payload
    !=
remaining correction margin
    !=
refresh-cadence decision
    !=
read + correction
    !=
in-place charge restoration OR remap to new embodiment
    !=
updated mapping / wear state
    !=
restored future correction margin
```

It also separates proactive retention renewal from integrity scrubbing. ZFS/GFS cases use verification to discover whether retained copies are already inconsistent/corrupt; FCR is triggered by a model/policy aimed at **preventing time/wear-dependent raw error accumulation from outrunning ECC**. The operations can both be background scans, but their failure models and repair semantics are not identical.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Cai et al. presented FCR at ICCD 2012 | H/P | peer-reviewed primary paper + institutional bibliographic records |
| FCR periodically reads, ECC-corrects, then reprograms in place or remaps before retention errors exceed ECC capability | H/P | abstract + §§I, IV |
| Remapping FCR programs corrected data to a new free block and changes the logical mapping | H/P | §IV.A / Fig. 3 |
| In-place reprogramming restores charge without erase for the bounded retention-error direction | H/P | §IV.B / Fig. 4 |
| In-place reprogramming can create program-interference errors and cannot repair the opposite/right-shift error direction | H/P | §IV.B / Fig. 5 |
| Hybrid FCR uses error evidence to decide when to remap instead of continuing in-place reprogramming | H/P | §IV.B / Fig. 6 |
| Adaptive-rate FCR changes refresh frequency with P/E cycles and reuses per-block wear information | H/P | §IV.C–D |
| More frequent remapping can reduce lifetime because it adds erase cycles | H/P/E | §IV.A + evaluation discussion |
| FCR requires power and can be scheduled as background/idle work | H/P | §IV.D |
| The reported 46× average lifetime improvement proves a production SSD achieved 46× measured field life | X | the paper reports simulation driven by measured characterization/workload data, not a multi-year production deployment |
| FCR proves all NAND Flash requires periodic refresh | X | outside the bounded 3x-nm MLC proposal/evaluation |
| NAND FCR refresh is historically or physically identical to DRAM refresh | X | paper itself distinguishes the mechanisms |

## Related repositories

Current inspection of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) finds broad Flash/controller history still listed as an area to deepen, not a dedicated FCR retention case to reuse. A general NAND-controller reliability history belongs there; this repository keeps the retention-specific comparison among nonvolatility, ECC margin, refresh trigger, remapping, and endurance.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) supplies the anti-anachronism rule: the 2012 authors' `Flash Correct-and-Refresh` vocabulary is historical; `reliability-qualified continuation` and `maintenance metadata` remain modern analytical terms.

## Sources

1. Yu Cai, Gulay Yalcin, Onur Mutlu, Erich F. Haratsch, Adrian Cristal, Osman S. Unsal, Ken Mai, **“Flash Correct-and-Refresh: Retention-Aware Error Management for Increased Flash Memory Lifetime,”** *30th IEEE International Conference on Computer Design (ICCD)*, Montreal, September 2012, pp. 94–101, DOI `10.1109/ICCD.2012.6378623`. Author-hosted paper: <https://users.ece.cmu.edu/~omutlu/pub/flash-correct-and-refresh_iccd12.pdf>.
2. ETH Zurich Systems Group publication record for the same ICCD 2012 paper: <https://publications.systems.ethz.ch/publication/791>.
3. Carnegie Mellon KiltHub record, posted 1 October 2012, preserving the abstract and evaluation boundary: <https://kilthub.cmu.edu/articles/journal_contribution/Flash_Correct-and-Refresh_Retention-Aware_Error_Management_for_Increased_Flash_Memory_Lifetime/6468821>.
4. Yu Cai, Yixin Luo, Erich F. Haratsch, Ken Mai, Onur Mutlu, **“Data Retention in MLC NAND Flash Memory: Characterization, Optimization, and Recovery,”** *HPCA 2015*, pp. 551–563, DOI `10.1109/HPCA.2015.7056062`; used only as later retention-age/read-recovery boundary evidence: <https://www.istc-cc.cmu.edu/publications/papers/2015/flash-memory-data-retention_hpca15_abs.shtml>.
