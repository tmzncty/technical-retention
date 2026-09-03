# Grounding Record — RAIDR 2012–2013 Retention-Aware Refresh and Profiling Limits

## Status

**`grounded`** for the bounded retention claim in Case 40: RAIDR moves part of DRAM refresh scheduling into a memory-controller policy keyed by retained row-retention profiles, while the 2013 commodity-DDR3 study demonstrates that data-pattern dependence and variable retention time make profile accuracy and future conservatism independent obligations rather than trivial inputs.

Case: [`../cases/40-raidr-retention-aware-dram-refresh.md`](../cases/40-raidr-retention-aware-dram-refresh.md).

This record deliberately separates three evidence layers:

1. **2012 research mechanism** — the original RAIDR paper defines row bins, profiling, Bloom-filter storage, candidate scheduling, and temperature scaling;
2. **2013 empirical stress test** — the original follow-up study measures commodity DDR3 behavior and shows why a profile may be incomplete or become non-conservative;
3. **cross-case reconstruction** — earlier DRAM cases supply refresh/authority/temperature contrasts, but they do not overwrite the vocabulary of the two papers.

## Primary source A — RAIDR, ISCA 2012

### Identity

- **Title:** `RAIDR: Retention-Aware Intelligent DRAM Refresh`
- **Authors:** Jamie Liu, Ben Jaiyen, Richard Veras, Onur Mutlu
- **Venue:** 39th International Symposium on Computer Architecture (ISCA)
- **Place/date:** Portland, Oregon, 9–13 June 2012
- **Author-hosted PDF:** <https://people.inf.ethz.ch/omutlu/pub/raidr-dram-refresh_isca12.pdf>
- **CMU PDL record:** <https://pdl.cmu.edu/PDL-FTP/NVM/raidr-isca12_abs.shtml>

### Abstract / Introduction — printed p. 1

The paper directly states that conventional DRAM refreshes all cells at a rate determined by the leakiest cell, although most cells retain data longer. RAIDR's key idea is to:

- group rows into `retention time bins`;
- apply a different refresh rate to each bin;
- keep rows containing leaky cells at the normal/high rate;
- refresh other rows less frequently;
- use Bloom filters to represent the bins;
- require no DRAM modification and only a small memory-controller modification.

The paper reports, for its evaluated 32 GB 8-core setup, 74.6% fewer refreshes, 16.1% average DRAM power reduction, 8.6% average system-performance improvement in the extended-temperature presentation, and 1.25 KB controller storage overhead.

**Evidence boundary:** these are the paper's modeled/simulated evaluation results. They are not a measurement of a named commercial controller implementing RAIDR.

### Retention distribution and row definition — printed p. 4 / §2.3–3.1

The paper says individual cells have different characteristic retention times and defines a **row's retention time as the minimum retention time across all cells in the row**.

In the two-bin example:

- one bin covers rows in the 64–128 ms interval and is serviced at 64 ms;
- one bin covers rows in the 128–256 ms interval and is serviced at 128 ms;
- rows outside those bins use a 256 ms default interval.

The memory controller chooses each row as a refresh candidate on the base schedule and consults the bins plus elapsed-period state to decide whether a refresh is necessary.

This directly grounds:

> device-wide refresh obligation can be decomposed into row-level cadence classes without eliminating the physical restoration obligation.

### Retention Time Profiling — printed pp. 4–5 / §3.2

The paper's straightforward profiling method is:

- write a small number of static data patterns, such as all-1 or all-0;
- turn refresh off;
- observe when the first bit changes;
- derive row retention from the cells in that row.

It proposes that, after measurements are collected, the operating system can save the results in a file and restore them into the controller on future boots rather than re-profile every boot.

A footnote on the same page already records an important limitation: circuit-level crosstalk can make retention depend on values in nearby bits, and the worst-case pattern depends on the bit-array architecture. The authors leave deeper analysis of that issue to future work.

The next page says the profile can be reused because retention time was treated as not changing significantly over a cell's lifetime, with temperature handled separately.

This is the exact 2012 assumption later placed under pressure by the 2013 study; it should not be silently rewritten as if the 2012 paper had already solved VRT.

### Bloom-filter bin representation — printed p. 5 / §3.3

The paper rejects naive fixed-capacity tables partly because an undersized table could omit weak rows and therefore lose correctness.

For Bloom filters it states:

- false positives can occur;
- false negatives for inserted elements cannot occur;
- in RAIDR, a false positive may refresh a row **more often** than required;
- a row should therefore never be refreshed **less often** than required because of Bloom-filter membership error alone.

This directly supports the bounded relation:

> **safe over-maintenance ≠ unsafe under-maintenance**.

It does **not** prove that the profiling stage inserts every actually weak row. The set-representation property and measurement completeness are separate evidence layers.

### Candidate scheduling and row-specific refresh — printed pp. 5–6 / §3.4

RAIDR uses:

- a row counter that cycles through row addresses;
- a period counter to track base 64 ms periods;
- row-address striping across banks to avoid starvation;
- row activation / RAS-only-style refresh for a selected row.

The paper explicitly accounts for the additional row-address energy cost in its evaluation.

This grounds the distinction between **less restoration work** and **zero maintenance-management work**.

### Temperature variation — printed p. 6 / §3.5

The paper treats temperature as a separate relation from row retention bins.

It says higher temperature decreases retention time and proposes a `refresh rate scaler` whose programmable period changes the refresh rate for **all rows by a multiplicative factor**. It compares this function to temperature-compensated self refresh in some mobile DRAMs while keeping the RAIDR design applicable at the memory-controller level.

This grounds:

> **row-retention heterogeneity ≠ temperature-conditioned global scaling**.

### Self-refresh boundary — printed p. 10 / energy evaluation

For long idle periods, the paper separately models:

- DRAM `self-refresh`, where the DRAM manages refresh internally without memory-controller input;
- RAIDR, where DRAM can be in a lower-power state but is woken for RAIDR's controller-selected row refreshes.

Thus the source itself prevents a silent equation:

> `RAIDR retention-aware policy = self-refresh authority`.

### Prior-art boundary — printed pp. 6–7 and conclusion p. 11

The paper reviews prior proposals including Ghosh and Lee's 2007 `Smart Refresh`, which keeps timeout state per row and can skip a refresh if a recent access has already restored the row. It also cites DRAM-device, ECC, and hardware/software approaches.

Its conclusion makes a narrower claim: **to the authors' knowledge**, RAIDR was the first low-cost **memory-controller modification** to reduce refresh operations by exploiting variability in DRAM cell retention times.

Safe wording retains that scope. Unsafe wording would be:

> `RAIDR invented retention-aware refresh.`

## Primary source B — Commodity DDR3 retention study, ISCA 2013

### Identity

- **Title:** `An Experimental Study of Data Retention Behavior in Modern DRAM Devices: Implications for Retention Time Profiling Mechanisms`
- **Authors:** Jamie Liu, Ben Jaiyen, Yoongu Kim, Chris Wilkerson, Onur Mutlu
- **Venue:** 40th International Symposium on Computer Architecture (ISCA)
- **Place/date:** Tel Aviv, Israel, 23–27 June 2013
- **CMU PDL PDF:** <https://www.pdl.cmu.edu/PDL-FTP/NVM/dram-retention_isca13.pdf>
- **PDL record:** <https://www.pdl.cmu.edu/PDL-FTP/NVM/dram-retention_isca13_abs.shtml>

### Experimental population — abstract / Introduction pp. 1–2

The authors use a temperature-controlled FPGA-based testing platform and report retention behavior from **248 commodity DDR3 DRAM chips from five major vendors**. Manufacturer names are anonymized in the paper.

This is direct peer-reviewed experimental evidence, but not a named-vendor product-compliance test.

### Profile accuracy as a precondition — Introduction p. 1 / §2.3 p. 3

The 2013 paper states that prior retention-aware mechanisms depend on accurate and reliable retention-time profiling. It describes the common assumption that, once a profile has been created, it remains stable and conservative enough to protect data integrity.

It then identifies factors that are not fixed at one point in time and therefore can violate that assumption.

### Data Pattern Dependence — pp. 1–3 and later analysis

The study uses the term `data pattern dependence` (`DPD`) for the effect by which a cell's measured retention behavior depends on data in that cell and nearby cells through circuit-level coupling/noise.

A particularly strong bounded result appears in the Introduction: **in some tested devices, all-1 and all-0 patterns identified less than 15% of all weak cells**.

This directly qualifies a simple static-pattern profiling method. It does not imply that every device has the same coverage ratio.

### Variable Retention Time — pp. 1–3 and later analysis

The study uses `variable retention time` (`VRT`) for cells that transition between multiple leakage/retention-time states.

The Introduction states that VRT can cause a cell's retention time to fall **significantly below its measured value**, and that even a `2x` safety margin may not suffice. The authors report VRT as ubiquitous across the tested modern DRAM population while discussing its manifestation at the cell level and the timescale problem for profiling.

This supports:

> **measured retention time ≠ guaranteed future minimum retention time**.

It does not support:

> `every DRAM cell changes retention state unpredictably`.

### Methodology boundary — pp. 3–5

The study uses a Xilinx ML605 FPGA platform, commodity SO-DIMMs, an insulated temperature-controlled enclosure, and repeated write / refresh / refresh-disabled wait / read-back tests.

The paper deliberately anonymizes manufacturer names, so this evidence should not be transformed into named-vendor claims.

## Claim-to-source matrix

| Claim | Source | Strength / limit |
| --- | --- | --- |
| RAIDR groups rows into retention-time bins and gives bins different refresh rates | 2012 abstract, §3.1 | direct research-mechanism record |
| A row's retention time is the minimum across its cells | 2012 §3.1 | direct definition |
| RAIDR stores bin membership in Bloom filters at the memory controller | 2012 §3.3 | direct mechanism |
| Bloom-filter false positives cause possible extra refresh while false negatives for inserted elements do not occur | 2012 §3.3 | direct representation property |
| RAIDR can save the measured profile in an OS file and restore it on future boots | 2012 §3.2 | direct proposed mechanism |
| RAIDR separately scales all-row cadence with temperature | 2012 §3.5 | direct mechanism; distinct from row bins |
| RAIDR and DRAM self refresh are treated as distinct mechanisms | 2012 idle-energy evaluation | direct comparison |
| 74.6% / 16.1% / 8.6% / 1.25 KB describe a deployed controller | none | **rejected**; they are paper evaluation figures |
| 2013 study tested 248 commodity DDR3 chips from five major vendors | 2013 abstract/Introduction | direct empirical scope |
| Simple all-1/all-0 testing can miss most weak cells in some devices | 2013 Introduction | direct bounded empirical result; not universal ratio |
| VRT can move retention below a prior measured value; 2x margin may be insufficient | 2013 Introduction and VRT analysis | direct empirical conclusion |
| Bloom-filter conservatism solves profiling incompleteness/VRT | none | **rejected**; representation and profile validity are separate |
| A saved profile remains permanently valid because its bytes survive | none | **rejected** by the later profile-validity evidence |
| RAIDR was commercially deployed | none | **unsupported** |

## Engineering reconstruction enabled by the evidence

### 1. Refresh obligation versus refresh cadence

The DRAM restoration obligation remains. RAIDR changes the mapping from **row classification → cadence**, showing that `must refresh` and `must refresh every row at one interval` are different claims.

### 2. Spatial heterogeneity versus environmental scaling

RAIDR has both row bins and a global temperature scaler. This is unusually useful cross-case evidence because one mechanism documents the independence of those two axes instead of forcing us to infer it from unrelated systems.

### 3. Retention metadata as retention infrastructure

The profile can be stored beyond the profiling event and reloaded to control later maintenance. The system therefore retains not only payload but a description of **how much maintenance it believes each row needs**.

### 4. Conservative approximate representation versus conservative measurement

A Bloom filter can conservatively encode an already-known weak-row set. That does not make the weak-row discovery procedure conservative.

This yields the exact two-layer distinction:

```text
profile / measurement completeness
    !=
set-representation false-negative property
```

### 5. Historical model versus later empirical qualification

The 2012 paper's boot-to-boot reuse argument and the 2013 VRT/DPD results belong to different dates and evidence states. The later paper may show that a prior simplifying assumption is difficult to satisfy; it must not be written as though the 2012 authors already had the later quantitative finding.

### 6. Persistent control metadata can be stale

The OS-profile-file proposal exposes a retention failure that is not `metadata disappeared`. The file may remain intact while its represented relationship is no longer conservative.

Thus:

> **control-state survival ≠ control-state validity**.

## Prior art and anti-anachronism

The 2012 paper itself supplies a prior-art map and cites Smart Refresh (MICRO-40, 2007) plus multiple device/controller/ECC/software approaches. This record therefore makes no broad invention claim.

The 2013 paper cites earlier VRT and physical-retention literature. Its contribution is a broad commodity-DDR3 experimental characterization and analysis of profiling implications, not invention of the physical phenomena.

Historical vocabulary preserved here includes `RAIDR`, `retention time bins`, `Retention Time Profiling`, `Bloom filters`, `refresh rate scaler`, `data pattern dependence`, and `variable retention time`.

Project reconstruction terms include `second-order retention state`, `profile validity`, `maintenance-policy metadata`, and `safe over-maintenance versus unsafe under-maintenance`.

## Related-repository check

Current GitHub code searches of `tmzncty/computing-archaeology` for `RAIDR`, `retention-aware refresh`, `DRAM refresh retention time`, and `Variable Retention Time` returned no dedicated case to reuse.

A broad history of refresh-reduction research, DDR controller evolution, or retention characterization should be routed there. This record remains bounded to the retention-specific chain:

```text
physical retention margin
    → measurement
    → profile
    → retained policy metadata
    → selective refresh decision
    → later profile revalidation problem
```

## Remaining gaps

This record does **not** close:

- commercial deployment of retention-aware refresh policies;
- a JEDEC-standardized per-row retention-time interface;
- later online profiling mechanisms designed explicitly around VRT/DPD;
- ECC-assisted profiling and failure tolerance;
- modern DDR5/LPDDR controller implementations;
- RowHammer/TRR refresh semantics;
- named-vendor retention distributions, because the 2013 study anonymizes vendors;
- a complete device-physics history of DPD or VRT;
- whether later production memory controllers retain similar profiling metadata across boots.

Those are separate bounded slices rather than reasons to enlarge Case 40.
