# RAIDR Retention-Aware DRAM Refresh: Row Binning, Profiling Metadata, and Variable-Retention Limits

## Status

**`grounded`** — bounded to the 2012 RAIDR research design and its 2013 experimental retention-profiling stress test. The case uses the original ISCA 2012 RAIDR paper as the mechanism record and the original ISCA 2013 study of 248 commodity DDR3 chips as later empirical evidence that complicates a static retention-profile assumption.

Grounding record: [`../evidence/40-raidr-2012-2013-retention-profile-grounding.md`](../evidence/40-raidr-2012-2013-retention-profile-grounding.md).

## Scope

This case asks a narrow question left open by the existing DRAM cases:

> What changes when refresh cadence is selected from a retained profile of **which rows are weak**, rather than applying one device-wide cadence or only scaling cadence from a global environmental condition?

RAIDR (`Retention-Aware Intelligent DRAM Refresh`) proposed three linked steps:

1. profile DRAM retention behavior;
2. classify rows into `retention time bins` stored at the memory controller;
3. refresh weak-row bins more frequently and let other rows wait longer.

The 2013 follow-up study then asks whether the profiling relation can actually be treated as stable and conservative enough for this kind of policy. Its measurements expose `data pattern dependence` (DPD) and `variable retention time` (VRT) as obstacles to that assumption.

This is **not**:

- a full history of retention-aware DRAM refresh;
- a claim that RAIDR was deployed in a shipped memory controller;
- a JEDEC refresh-standard genealogy;
- a claim that every DRAM row has one immutable retention time;
- a RowHammer mitigation case;
- a claim that temperature-compensated refresh and row-retention profiling are the same mechanism;
- a claim that the 2013 findings were already known in their later empirical form when the 2012 RAIDR paper was written.

The case therefore grounds a **profile-mediated maintenance-policy regime** and, crucially, the limits of treating the profile as a timeless description of the substrate.

## Relation to the earlier DRAM cases

The existing cases already separate several relations hidden by the word `refresh`:

```text
Case 03
    why decaying dynamic-cell charge requires repeated restoration

Case 09
    where refresh-row enumeration comes from

Case 10
    how a leakage-related proxy can internalize a maintenance trigger

Case 21
    how AUTO REFRESH and SELF REFRESH move recurring maintenance authority
    across the package boundary

Case 33
    which bank/bank-group resources are blocked by a refresh operation

Case 34
    how a measured environmental condition can change a selected cadence

Case 35
    how commercial Mobile DDR can combine automatic TCSR,
    internal self-refresh authority, and separately selectable PASR coverage

Case 40
    how measured row-retention heterogeneity can become retained controller metadata
    that decides which rows receive which cadence,
    and how DPD/VRT challenge the future validity of that metadata
```

Case 40 is therefore not another generic `DRAM needs refresh` case. Its changed relation is:

> **the system retains second-order state about the expected retention behavior of the state it is trying to retain.**

## Historical vocabulary and record

### RAIDR, 2012

Jamie Liu, Ben Jaiyen, Richard Veras, and Onur Mutlu presented **RAIDR: Retention-Aware Intelligent DRAM Refresh** at ISCA 2012.

The paper's own vocabulary includes:

- `RAIDR` / `Retention-Aware Intelligent DRAM Refresh`;
- `retention time`;
- `retention time bins`;
- `retention time profiling`;
- `Bloom filters`;
- `refresh candidate row`;
- `row counter`;
- `period counter`;
- `refresh rate scaler`.

The paper defines a row's retention time as the **minimum retention time across all cells in that row**. Rows whose retention times fall below a new default interval are represented in shorter-retention bins at the memory controller. During operation, the controller periodically selects each row as a refresh candidate and consults the bins to decide whether that row must be refreshed in the current period.

The authors evaluate a two-bin design in a modeled 32 GB, 8-core system and report a 74.6% reduction in refresh operations, 16.1% average DRAM power reduction, 8.6% average performance improvement in the extended-temperature evaluation, and 1.25 KB of memory-controller storage overhead.

Those figures are **paper evaluation results**, not measurements from a commercially shipped RAIDR controller.

### Retention-time profiling stress test, 2013

Jamie Liu, Ben Jaiyen, Yoongu Kim, Chris Wilkerson, and Onur Mutlu then published **An Experimental Study of Data Retention Behavior in Modern DRAM Devices: Implications for Retention Time Profiling Mechanisms** at ISCA 2013.

Using a temperature-controlled FPGA-based platform, they collected retention information from **248 commodity DDR3 DRAM chips from five major vendors**. The paper uses the terms:

- `retention time profiling`;
- `data pattern dependence` (`DPD`);
- `variable retention time` (`VRT`);
- `weak cells`;
- `retention time states`.

The study explicitly frames accurate profiling as a precondition for prior retention-aware mechanisms to guarantee data integrity. It then shows why that condition is difficult: in some devices, testing only all-1 and all-0 patterns found **less than 15% of all weak cells**, while VRT can move a cell to a much shorter retention state after it has already been measured. The authors state that even a `2x` safety margin may not suffice in the presence of VRT.

The 2013 paper is used here as a **later empirical qualification** of a class of profiling assumptions. It does not retroactively rewrite the 2012 paper's historical vocabulary.

## Retained payload and retained policy state

The primary payload remains ordinary dynamic-cell charge. RAIDR adds another retained layer above it:

1. **payload state** — values represented by cell charge;
2. **measured retention information** — observed time-to-failure behavior under the profiling procedure;
3. **row classification** — membership in a retention-time bin, using the row minimum across its cells;
4. **compact bin representation** — Bloom-filter state in the memory controller;
5. **scheduling phase** — row counter, period counter, and rate-scaler state;
6. **temperature policy state** — a multiplicative scaler that globally adjusts refresh frequency;
7. **optionally persisted profile** — the 2012 paper proposes saving profiling results in an operating-system file for later boots.

`Second-order retention state`, `maintenance-policy metadata`, and `profile validity` are project reconstruction terms, not phrases attributed to the historical authors.

## Engineering reconstruction

### One refresh obligation does not imply one device-wide cadence

Conventional refresh in the bounded papers is described as refreshing every row at the rate required by the weakest cells. RAIDR instead uses measured heterogeneity to place rows in different cadence classes.

Therefore:

> **refresh obligation ≠ one device-wide maintenance cadence**.

Every row still has a restoration obligation. The proposed optimization changes **how often each row is entitled to consume maintenance work**.

This differs from PASR in Case 35. PASR can deliberately exclude regions from retention work and accept their loss. RAIDR's policy is intended to preserve all data while reducing unnecessary work for rows believed to have longer margins.

### Row-retention heterogeneity and global temperature scaling are separate axes

RAIDR does not use temperature as a substitute for row profiling. Section 3.5 adds a separate `refresh rate scaler` that changes the rate for **all rows** by a multiplicative factor as device temperature changes.

Therefore:

> **row-retention heterogeneity ≠ temperature-conditioned global scaling**.

Case 34 changes cadence from an environmental proxy. Case 40 changes cadence from a spatial classification of rows, then separately scales that policy with temperature.

A system can therefore have both:

```text
which row is weak?
    → profile / bin relation

how does current temperature change every row's safe interval?
    → global rate-scaling relation
```

The two relations should not be collapsed into one `adaptive refresh` category when mechanism matters.

### The maintenance profile is itself retained state

The 2012 paper proposes that profiling results can be saved to a file by the operating system and restored into the controller at later boot-ups.

That makes the profile more than transient diagnostic output. It can become part of the machinery that determines future refresh decisions.

Therefore:

> **profile metadata ≠ payload, while profile metadata can be retention infrastructure**.

The payload survives only if the future scheduler classifies its row conservatively enough. A retained description of the substrate can thus become causally constitutive of retaining the substrate's payload.

### Approximation direction matters when metadata controls maintenance

RAIDR uses Bloom filters because they can have false positives but not false negatives for inserted elements. In the paper's mapping:

- a false positive can make a row appear in a **shorter-retention / more-frequent-refresh** class than necessary;
- a false negative would be dangerous because a genuinely weak row could be refreshed too slowly.

The paper explicitly treats the first error direction as safe: extra refresh work is wasted, but data integrity is not endangered under the model.

Therefore:

> **metadata approximation direction matters**.

And more specifically:

> **safe over-maintenance ≠ unsafe under-maintenance**.

This is a useful retention relation beyond Bloom filters themselves. Approximate metadata is not simply `less accurate`; its error direction can determine whether the cost is extra work or payload loss.

### Row-level retention policy is not exact per-cell policy

Although the physical variation exists at cell level, RAIDR defines a row's retention time as the **minimum** retention time of all cells in that row and schedules refresh at row granularity.

Therefore:

> **row-level retention class ≠ exact per-cell retention policy**.

One weak cell can pull an entire row into a shorter-retention class. RAIDR exploits more heterogeneity than a device-wide interval, but it does not expose a unique maintenance deadline for every cell.

### A measured retention time is not automatically a future guarantee

The 2012 paper says profiling results can be reused at later boots because retention time was assumed not to change significantly over a cell's lifetime, while handling temperature separately. Yet the same section already notes that nearby data values can affect measured retention time and leaves deeper analysis of that problem to future work.

The 2013 study then directly attacks the broader assumption that a measured profile remains a conservative future profile. It finds two independent complications:

- **DPD**: the observed retention time depends on surrounding data patterns, so a profiler can miss weak states if its patterns do not expose the worst case;
- **VRT**: some cells transition unpredictably between multiple retention states, so a later state can be substantially weaker than the state observed during profiling.

Therefore:

> **measured retention time ≠ guaranteed future minimum retention time**.

And:

> **retention profile ≠ immutable physical truth**.

The profile is an empirical claim about expected future behavior, not a direct reading of an eternal cell constant.

### Saved-across-boots does not mean valid-across-boots

The proposed OS file makes a profile persist longer. The 2013 evidence shows why persistence of the profile is not sufficient:

> **saved profile across boots ≠ perpetual validity of that profile**.

Indeed, retaining stale control knowledge can be more dangerous than forgetting it if the stale profile causes a weak row to be under-refreshed.

This is a different failure mode from ordinary metadata loss. Here the metadata can survive **too successfully** while the relation it describes has changed or was incompletely measured.

### Model-level integrity closure is conditional on profile quality

RAIDR's Bloom-filter argument legitimately shows that false positives do not create under-refresh **given correct insertion/classification of weak rows**. The 2013 paper shows that this condition cannot be treated as trivial.

Therefore:

> **Bloom-filter no-false-negative property ≠ no profiling false negatives**.

The set representation can be conservative even while the measurement procedure used to populate the set misses a weak cell or later VRT changes the relevant minimum.

Likewise:

> **model-level integrity guarantee ≠ empirical immunity to DPD/VRT**.

The two papers do not contradict at the same layer. One establishes a scheduler/representation property under an input model; the other challenges whether the required input can be measured and kept conservative.

### More selective maintenance still requires profiling and controller work

RAIDR removes many refreshes by adding:

- profiling work;
- retained bin metadata;
- Bloom-filter lookups;
- row/period counters;
- temperature scaling;
- row-specific refresh commands.

Therefore:

> **more selective maintenance ≠ zero maintenance-management cost**.

The system performs less substrate restoration by doing more work to know **which restoration is necessary**.

### Retention-aware refresh is not self-refresh authority

The 2012 paper explicitly evaluates normal self refresh as a different mechanism in idle periods, where the DRAM manages refresh internally. RAIDR instead keeps row-specific refresh decisions in the memory-controller side and wakes DRAM for selected row refreshes.

Therefore:

> **retention-aware refresh policy ≠ self-refresh authority**.

Case 21/35 ask where recurring maintenance authority resides. Case 40 asks how a controller that owns the schedule differentiates rows by an estimated retention requirement.

## Failure and forgetting boundaries

This case adds failure modes that do not fit a simple `refresh stopped` story:

- **profile omission** — a weak cell/row is never classified conservatively;
- **pattern incompleteness** — the profiling data pattern does not expose a weaker physical state;
- **VRT transition** — a cell later moves into a shorter-retention state;
- **stale persisted profile** — old classification survives even when it is no longer conservative;
- **temperature error** — a global rate scaler is based on an insufficient environmental assumption;
- **representation false positive** — safe but costly over-refresh in RAIDR's Bloom-filter design;
- **representation overflow/underclassification risk** — a naive bounded table can fail to hold all weak rows, which the paper uses as an argument for the Bloom representation;
- **service cost** — selective row refresh still consumes command/bandwidth/energy resources and can interfere with demand accesses.

The important methodological result is that **retention failure can come from a wrong model of the retention mechanism, not only from physical leakage itself**.

## Prior art and anti-anachronism

The RAIDR paper itself reviews multiple earlier refresh-reduction proposals. In particular, it discusses Ghosh and Lee's **Smart Refresh** (MICRO-40, 2007), which keeps per-row timeout state and skips refreshes when recent accesses have already restored a row. It also cites earlier DRAM-device modifications and ECC/software approaches.

RAIDR's own conclusion makes a narrower novelty claim: to the authors' knowledge, it was the first low-cost **memory-controller modification** to reduce refreshes by exploiting variability in DRAM cell retention times.

This repository preserves that scope instead of rewriting it as:

> `RAIDR invented retention-aware refresh.`

The 2013 DPD/VRT study likewise did not invent the phenomena it names; it cites earlier physical/device literature and contributes a broad quantitative study on commodity DDR3 chips. Historical priority and retention-specific methodological use remain distinct.

## Functional analogy and philosophical limit

A bounded functional analogy can compare RAIDR's retained profile to predictive-maintenance state in other systems: the system stores knowledge about a component's expected degradation so that future maintenance can be scheduled selectively.

The analogy stops there. A DRAM row bin is not an SSD wear table, a filesystem scrub schedule, a medical risk score, or an archival appraisal policy.

A narrow conceptual pressure does follow:

> A technical system may have to remember **how its own substrate tends to forget** in order to decide how much work is required to keep another state available.

The 2013 results sharpen the pressure:

> retained knowledge about forgetting can itself become stale, incomplete, or probabilistic.

Those are engineering/philosophical interpretations of the documented mechanisms and measurements. They are not historical claims that the authors formulated a philosophy of memory.

## Cross-case result

The DRAM decomposition can now distinguish:

```text
dynamic-cell payload / leakage
    !=
row-local retention heterogeneity
    !=
profiling experiment
    !=
profile validity over future time
    !=
row-level retention classification
    !=
compact controller representation
    !=
global temperature scaling
    !=
refresh-candidate scheduling
    !=
recurring maintenance authority
    !=
refresh target/interference geometry
    !=
restoration execution
```

Case 40's central addition is the middle of that chain: **measurement and retained policy metadata mediate the relation between physical degradation and later maintenance**.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| RAIDR groups rows into retention-time bins and assigns different refresh rates | H/P | direct ISCA 2012 mechanism description |
| RAIDR stores the bins at the memory-controller side using Bloom filters | H/P | direct 2012 paper |
| The paper defines row retention time as the minimum across cells in the row | H/P | direct §3.1 definition |
| RAIDR's Bloom representation allows false positives but not false negatives for inserted elements | H/P | direct §3.3 mechanism |
| Under the paper's mapping, false positives can cause extra refreshes without causing under-refresh | H/P/E | direct paper argument; conditional on correct profiling/classification |
| RAIDR separately applies global temperature-based rate scaling | H/P | direct §3.5 mechanism |
| The 2012 paper proposes saving profiling results in an OS file and restoring them on later boots | H/P | direct §3.2 mechanism |
| The 2013 study tested 248 commodity DDR3 chips from five vendors | H/P | direct peer-reviewed experimental report |
| DPD can make simple all-1/all-0 profiles miss most weak cells in some tested devices | H/P | direct 2013 empirical result |
| VRT can move a cell to a much shorter retention state after measurement; a 2x margin may be insufficient | H/P | direct 2013 empirical conclusion |
| A Bloom filter's representation guarantee solves DPD/VRT profiling accuracy | X | unsupported; these are different layers |
| RAIDR was a shipped commercial controller feature | X | not established by this source set |
| RAIDR is identical to Mobile-DDR TCSR/self refresh | X | mechanism/authority boundary contradicts the equation |
| The 2013 study proves every DRAM cell has unstable retention time | X | it reports VRT in a subset and broad prevalence, not universal per-cell instability |

## Related repositories

Current searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `RAIDR`, `retention-aware refresh`, `DRAM refresh retention time`, and `Variable Retention Time` returned no dedicated case to reuse.

A comprehensive DRAM-controller/history treatment should be routed there if developed. This repository keeps the retention-specific distinction among **physical margin, measurement, retained profile, scheduling policy, and profile validity**.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) remains the anti-anachronism guardrail: `retention time bin`, `Bloom filter`, DPD, and VRT are sourced historical/technical vocabulary, while `second-order retention state` and `remembering how the substrate forgets` are later reconstructions.

## Sources

1. Jamie Liu, Ben Jaiyen, Richard Veras, Onur Mutlu, **“RAIDR: Retention-Aware Intelligent DRAM Refresh,”** *Proceedings of the 39th International Symposium on Computer Architecture (ISCA)*, Portland, Oregon, 9–13 June 2012. Relevant locations: abstract and Introduction pp. 1–2; retention distribution and RAIDR overview pp. 3–4; profiling/Bloom filters pp. 4–5; temperature scaling and controller state pp. 5–6; prior work pp. 6–7; evaluation pp. 8–10; conclusion p. 11. Author-hosted PDF: <https://people.inf.ethz.ch/omutlu/pub/raidr-dram-refresh_isca12.pdf>. CMU PDL record: <https://pdl.cmu.edu/PDL-FTP/NVM/raidr-isca12_abs.shtml>.
2. Jamie Liu, Ben Jaiyen, Yoongu Kim, Chris Wilkerson, Onur Mutlu, **“An Experimental Study of Data Retention Behavior in Modern DRAM Devices: Implications for Retention Time Profiling Mechanisms,”** *Proceedings of the 40th International Symposium on Computer Architecture (ISCA)*, Tel Aviv, Israel, 23–27 June 2013. Relevant locations: abstract/Introduction pp. 1–2; retention profiling and DPD/VRT pp. 2–3; methodology pp. 3–5; empirical analysis and profiling implications later in the paper. CMU PDL PDF: <https://www.pdl.cmu.edu/PDL-FTP/NVM/dram-retention_isca13.pdf>. PDL record: <https://www.pdl.cmu.edu/PDL-FTP/NVM/dram-retention_isca13_abs.shtml>.
3. Internal comparison only: [`03-dram-refresh-as-scheduled-restoration.md`](03-dram-refresh-as-scheduled-restoration.md), [`21-micron-sdram-refresh-mode-handoff.md`](21-micron-sdram-refresh-mode-handoff.md), [`34-micron-temperature-dependent-dram-refresh.md`](34-micron-temperature-dependent-dram-refresh.md), and [`35-micron-mobile-ddr-automatic-tcsr.md`](35-micron-mobile-ddr-automatic-tcsr.md).
