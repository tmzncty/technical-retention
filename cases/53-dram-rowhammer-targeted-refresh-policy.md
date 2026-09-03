# DRAM RowHammer: Access-Induced Retention Loss, Targeted Refresh, and Mitigation Limits

## Status

**`grounded`** — bounded to the 2012–2020 RowHammer / targeted-refresh record needed for a retention-specific comparison: Intel's 2012-priority row-hammer refresh-command work, Kim et al.'s 2014 experimental characterization and PARA proposal, a Micron DDR4 manufacturer datasheet revision from 2015, and the 2020 TRRespass black-box evaluation of in-DRAM TRR. The case distinguishes measured disturbance physics, proposed policy, manufacturer interface/product claims, and later empirical bypass evidence.

Grounding record: [`../evidence/53-rowhammer-2012-2020-targeted-refresh-grounding.md`](../evidence/53-rowhammer-2012-2020-targeted-refresh-grounding.md).

## Scope

This case asks a narrow question left open by Cases 03, 33, 34, 40, 43, and 45:

> What changes when DRAM retention failure is driven not only by elapsed time, temperature, or a row's intrinsic retention profile, but by repeated activation of a physically nearby row — so the maintenance policy must respond to access history and physical adjacency?

The bounded regime is **RowHammer / DRAM disturbance mitigation through extra refresh work**. It is not a general history of RowHammer attacks, exploitation, memory security, or every post-2020 mitigation.

This is **not**:

- a claim that RowHammer and ordinary retention leakage are the same physical process;
- a claim that every DDR4/LPDDR4 part implements the same Target Row Refresh (`TRR`) algorithm;
- evidence that PARA shipped in a named commercial memory controller;
- evidence that `TRR` is one standardized implementation with one deterministic guarantee;
- a complete JEDEC DDR4/LPDDR4/DDR5 chronology;
- a claim that the 2014 paper invented the broader row-hammer problem or targeted refresh;
- a security-exploitation case except where attack-oriented experiments qualify the retention mechanism.

## Historical vocabulary and record

### Row-hammer refresh-command work before the 2014 paper

Intel patent application US20140006703A1 has a priority date of **30 June 2012**. Its vocabulary includes `row hammer event`, `row hammer condition`, `targeted refresh command`, `victim row`, a threshold number of accesses within a time window, and a distinction between the row being excessively accessed and the physically adjacent row whose data may be corrupted.

The filing matters for chronology. It also exposes an architectural boundary: the memory controller can identify the hammered row, while the DRAM device can determine which physical row or rows are actually adjacent and therefore require targeted refresh. The patent explicitly notes that logical row labels and physical adjacency can differ across manufacturers and that controllers do not necessarily know the internal physical layout.

Therefore the 2014 academic paper must not be described as the invention of row-hammer-aware targeted refresh.

### 2014 experimental characterization and PARA

Yoongu Kim et al., **“Flipping Bits in Memory Without Accessing Them: An Experimental Study of DRAM Disturbance Errors,”** ISCA 2014, experimentally tested 129 DRAM modules comprising 972 chips and reported disturbance errors in 110 modules / 836 chips. The paper reports a minimum observed disturbance threshold of about 139K row activations in the tested population and identifies the mechanism as repeated wordline toggling that accelerates charge leakage in nearby rows.

The paper then evaluates several mitigation classes, including stronger ECC, increasing the global refresh rate, retiring/remapping vulnerable cells, explicitly tracking hot rows and refreshing neighbors, and a proposed **Probabilistic Adjacent Row Activation (`PARA`)** mechanism.

PARA is intentionally stateless: whenever a row is opened and closed, the memory controller probabilistically opens one of its adjacent rows. Repeated aggressor activity therefore increases the probability that a vulnerable neighbor is refreshed before disturbance accumulates to an error. The paper is explicit that PARA is probabilistic rather than absolutely deterministic, and its reported overhead is a simulation/evaluation result rather than deployment evidence.

### 2015 Micron DDR4 manufacturer record

A mirrored Micron **4Gb x4/x8/x16 DDR4 SDRAM** datasheet, document identifier `09005aef84af6dd0`, Rev. E (11/2015), contains a section titled `Target Row Refresh Mode`. It defines a `maximum activate count (MAC)` within a `maximum activate window (tMAW)`, calls the excessively activated row the target row (`TRn`), and calls the adjacent rows requiring refresh the victim rows. The same manufacturer document states that Micron DDR4 devices automatically perform TRR mode in the background.

This is product-family manufacturer documentation, not an independently verified universal DDR4 guarantee. The copy used here is a distributor/archive mirror; the document itself carries Micron's title, document identifier, revision, and copyright.

### 2020 TRRespass qualification

Pietro Frigo et al., **“TRRespass: Exploiting the Many Sides of Target Row Refresh,”** IEEE S&P 2020, treats `TRR` not as one transparent algorithm but as a family of opaque in-DRAM mitigation mechanisms. Their black-box fuzzer found TRR-aware hammering patterns that induced bit flips in **13 of 42** tested DDR4 modules from the three major DRAM vendors, including many-sided patterns using multiple aggressor rows.

This later evidence does not show that every TRR implementation fails. It does show that a manufacturer/device's possession of a mitigation class cannot be equated with a complete retention guarantee against all access patterns.

## Retained state and constitutive control relations

The bounded regime contains several separable states and relations:

1. **victim-row payload charge** — the data that must remain distinguishable until ordinary or targeted restoration;
2. **aggressor activation history** — repeated row open/close activity within a relevant time window;
3. **aggressor/victim physical-adjacency relation** — which rows are physically close enough for disturbance coupling;
4. **ordinary refresh schedule** — periodic restoration required even without hammering;
5. **disturbance threshold / policy bound** — e.g. a maximum activation count or a research-model `Nth` threshold;
6. **mitigation policy state** — counters, detector state, TRR implementation state, or alternatively PARA's probability parameter without per-row counters;
7. **targeted refresh action** — extra restoration directed to a row at elevated disturbance risk;
8. **error-detection/correction state** — ECC or other mechanisms that may detect/correct some residual failures without eliminating the disturbance process;
9. **topology/remapping knowledge** — enough information to translate a hammered logical row into the physical neighbors whose state is at risk.

These are not all payload. Some are **retention infrastructure about the circumstances under which payload should be restored**.

## Engineering reconstruction

### Scheduled refresh can be correct and still be insufficient under adversarial access

Case 03 established periodic DRAM refresh as a deadline-driven obligation. RowHammer adds a different route to the same failure surface: repeated activation of an aggressor row can accelerate charge loss in nearby victim rows so that the victim crosses its safe margin **before the ordinary refresh schedule would have restored it**.

Therefore:

> **meeting the ordinary refresh schedule ≠ immunity to access-induced retention loss**.

The extra refresh is not replacing ordinary DRAM refresh. It is compensating for a workload-induced acceleration of the victim's effective retention deadline.

This creates a distinct policy axis:

> **periodic refresh deadline ≠ disturbance-conditioned refresh urgency**.

### Access history can become part of retention policy without becoming payload

The 2012 Intel filing describes threshold-based detection of excessive accesses, while Kim et al. analyze per-row counters and related hot-row tracking as one mitigation family. In those designs, recent activation history becomes control evidence for future maintenance.

Therefore:

> **recent access history can become constitutive retention-policy state**.

But PARA provides an important counterexample to a simplistic conclusion that RowHammer defense always requires storing a per-row history. PARA deliberately uses a probability parameter and a random event at row close, avoiding per-row activation counters.

Hence:

> **workload-conditioned maintenance ≠ necessarily explicit per-row history retention**.

The system can make future maintenance statistically dependent on access without preserving a full explicit record of that access.

### Targeted refresh separates disturbance detection from physical-neighbor resolution

The Intel patent's targeted-refresh architecture is especially useful for this repository. The controller can detect or be told that a logical row has crossed a hammer threshold, yet the DRAM device may be the component that knows which physical victim rows are adjacent after manufacturer-specific layout and internal remapping.

Therefore:

> **aggressor identification ≠ victim-row physical resolution**.

and:

> **logical row adjacency ≠ physical disturbance adjacency**.

A mitigation can therefore depend on retained or computable topology relations that are not visible in the host's ordinary address model.

This also sharpens Case 33. Same Bank Refresh concerns **which bank geometry is occupied by scheduled maintenance**; RowHammer-targeted refresh concerns **which physical neighbors need extra restoration because of access-induced coupling**. Both localize refresh work, but for different reasons and using different geometry.

### Global refresh and targeted refresh trade coverage for selective work

Kim et al. show that simply refreshing all rows more frequently can suppress disturbance errors, but at substantial energy/performance cost. Targeted methods instead try to spend extra refresh work only where access behavior indicates elevated risk.

Therefore:

> **more frequent global refresh ≠ targeted disturbance mitigation**.

The first raises maintenance work for every row regardless of recent access. The second requires some combination of detection, topology knowledge, or probabilistic policy to choose additional restoration work.

This is another example of the repository's recurring distinction:

> **retention obligation ≠ maintenance scheduling policy**.

The obligation is to prevent state from crossing an unrecoverable margin; the policy decides when and where to spend restoration work.

### PARA is stateless with respect to row counters, not maintenance-free

Kim et al. call PARA stateless because it does not maintain expensive per-row activation counters or aggressor/victim address tables. Yet every row close still creates a probabilistic decision and may create an additional adjacent-row activation/refresh.

Therefore:

> **counter-free policy state ≠ zero retention work**.

and:

> **stateless mitigation ≠ deterministic guarantee**.

The scheme's guarantee is probabilistic. The 2014 paper explicitly states that PARA cannot prevent disturbance errors with absolute certainty, although the probability can be made extremely small for chosen assumptions and parameters.

The repository therefore records the analytical boundary:

> **modeled low failure probability ≠ measured deployed-system immunity**.

### A named mitigation class does not by itself establish the retention guarantee

The 2015 Micron datasheet establishes a manufacturer claim that its DDR4 devices automatically perform a type of TRR in the background. TRRespass 2020 later shows that opaque in-DRAM TRR implementations can have finite tracking/sampling capacities or other behavior that sophisticated access patterns exploit.

Therefore:

> **TRR presence ≠ universal RowHammer immunity**.

and more generally:

> **mitigation-class label ≠ complete implementation contract**.

This is not an accusation that every implementation is defective. It is a methodological warning: without an exact mechanism, threshold, tracking capacity, topology rule, and fault model, `has TRR` is not enough evidence to infer the set of access patterns under which victim retention is protected.

### Residual error correction is not the same as preventing disturbance

Kim et al. discuss ECC as one possible defense and show that common single-error-correcting server ECC is not sufficient for every observed multi-bit disturbance pattern. Intel's later/current guidance likewise treats prevention/containment and residual error correction as separate mitigation layers.

For this bounded historical case the safe conclusion is:

> **disturbance prevention/restoration ≠ residual error correction**.

A targeted refresh tries to restore the vulnerable victim before corruption manifests. ECC acts after raw errors exist, within a correction envelope. The two mechanisms may compose but are not interchangeable.

## Relation to other DRAM cases

### Case 03 — ordinary scheduled refresh

Case 03 asks why a DRAM cell must be periodically restored even without unusual access. Case 53 adds the possibility that **access to another row changes the effective urgency of restoration**.

```text
ordinary retention deadline
    -> periodic refresh

aggressor activation history + physical coupling
    -> extra victim-row restoration / mitigation
```

### Cases 34/35 — temperature-conditioned cadence

Temperature-conditioned refresh changes cadence because the environment alters charge-retention margin. RowHammer-targeted refresh changes extra restoration because **workload activity on neighboring rows** alters the victim's margin. Environmental condition and access history are therefore different policy inputs.

### Cases 40/43 — retention-profile and runtime feedback

RAIDR/AVATAR use measured row-retention behavior and error feedback to classify refresh cadence. RowHammer mitigation instead reacts to **disturbance risk induced by other rows' activation history**. A victim row can be intrinsically ordinary in retention time yet become unsafe under a pathological aggressor pattern.

Therefore:

> **intrinsic retention weakness ≠ access-induced victimhood**.

### Case 45 — ECC/ECS composition

ECS scrubbing detects/corrects/writes back existing correctable errors. Targeted RowHammer refresh aims to restore a victim before the disturbance creates an error. Both are integrity-maintenance work, but their trigger and timing relation differ.

## Failure and forgetting boundaries

Within this bounded regime, loss can arise when:

- an aggressor row is activated often enough to accelerate victim-cell charge leakage;
- ordinary refresh arrives too late for the disturbance-amplified victim margin;
- hot-row tracking misses or undercounts the effective aggressor set;
- a bounded tracker/sampler is overwhelmed by a many-sided pattern;
- logical-to-physical adjacency or internal remapping is misunderstood;
- a targeted refresh policy chooses the wrong neighbors, too low a probability, or too high a threshold;
- ECC encounters a multi-bit pattern outside its correction capability;
- a product-specific mitigation behaves differently from the abstract `TRR` label assumed by software or a researcher.

Forgetting here is not simply `DRAM leaked over time`. It is failure to restore the current victim state before **access-amplified physical coupling** pushes that state beyond recoverability.

## Prior art and anti-anachronism

The 2014 paper itself notes industry awareness and Intel patent applications dating to 2012. The 2012-priority Intel filing directly uses `row hammer`, thresholded access, `victim row`, and `targeted refresh command`. Therefore:

> **2014 experimental characterization ≠ invention of RowHammer-aware targeted refresh**.

The defensible historical claim is narrower: Kim et al. 2014 provided a broad open experimental characterization of disturbance errors in contemporary commodity DRAM, demonstrated a user-level access pattern on real systems, systematically compared mitigation classes, and proposed PARA.

Likewise, this case uses `access-induced retention loss`, `disturbance-conditioned refresh urgency`, and `retention-policy state` as project analytical vocabulary. Those phrases must not be attributed to 2012–2020 actors unless a source actually uses them.

## Philosophical interpretation — bounded

The case adds one narrow pressure to the repository's idea of retention:

> a retained state's maintenance need can be relational and workload-produced. The victim row's future does not depend only on its own age, temperature, or intrinsic weakness; it can depend on what another address is repeatedly asked to do.

That makes technical persistence less like an isolated object's private endurance and more like a managed relation among neighboring physical states, access patterns, and maintenance policy. This is an engineering-derived conceptual observation, not a philosophical claim made by Intel, Micron, or the RowHammer researchers.

## Cross-case result

Case 53 adds a new refresh-policy relation:

```text
ordinary DRAM refresh obligation
    !=
aggressor activation history
    !=
physical aggressor/victim adjacency
    !=
row-hammer threshold / detector / probability policy
    !=
targeted victim refresh
    !=
residual ECC correction
    !=
empirical guarantee against arbitrary access patterns
```

The strongest new comparison rule is:

> **maintenance urgency can be induced by the activity of a different retained state.**

That is stronger than saying merely that DRAM needs refresh.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| `row hammer event`, victim-row, and targeted-refresh-command vocabulary existed in Intel work with 2012 priority | H/P | US20140006703A1 |
| Repeated activation of one DRAM row can accelerate charge loss and induce errors in nearby rows | H/P | Kim et al., ISCA 2014 experimental characterization |
| 110 of 129 tested modules showed disturbance errors in the 2014 study | H/P | ISCA 2014 abstract/introduction |
| Ordinary scheduled refresh can be insufficient when neighboring activation accelerates charge loss | E/P | mechanism and mitigation analysis in ISCA 2014 |
| Increasing global refresh rate and targeted adjacent-row refresh are distinct mitigation policies | H/P/E | ISCA 2014 §8 |
| PARA uses low-probability adjacent-row activations without per-row counters | H/P | ISCA 2014 §8.2 |
| PARA provides an absolute deterministic guarantee | X | the paper explicitly describes a probabilistic residual failure probability |
| PARA was deployed in a named commercial controller | X | the bounded sources do not establish deployment |
| Controller-visible logical row identity always reveals physical victim adjacency | X | Intel patent and ISCA 2014 both identify physical-adjacency/remapping knowledge as a problem |
| Micron's 2015 DDR4 manufacturer datasheet documents automatic background TRR for the bounded product family | H/P | Micron document `09005aef84af6dd0`, Rev. E 11/15, accessed through an archive/distributor mirror |
| `TRR` is one transparent implementation with one universal guarantee | X | TRRespass 2020 documents implementation diversity/opacity and bypass patterns |
| 13 of 42 tested TRR-protected DDR4 modules were vulnerable to TRRespass's TRR-aware patterns | H/S/P-like experimental publication | IEEE S&P 2020 / author arXiv record |
| Every TRR-equipped DDR4 module is vulnerable | X | the 2020 result is bounded to its tested modules/patterns |
| RowHammer disturbance and ordinary retention leakage are the same mechanism | X | the safe comparison is that disturbance accelerates charge loss and creates extra restoration urgency |

## Related repositories

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `RowHammer` and `DRAM disturbance` found no dedicated case. A broader history of DRAM scaling, device coupling, security exploitation, JEDEC mitigation evolution, and DDR5 Refresh Management (`RFM`) belongs there or in later bounded work. This repository keeps the narrower retention question: how access to one physical row can create an extra restoration obligation for another, and what control state/policy is required to make that obligation actionable.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) supplies the anti-anachronism discipline. `row hammer`, `victim row`, `targeted refresh`, `TRR`, and `PARA` are source vocabulary where cited; `disturbance-conditioned refresh urgency` and `maintenance urgency induced by another retained state` are project reconstructions.

## Sources

1. Kuljit S. Bains, John B. Halbert, Christopher P. Mozak, Theodore Z. Schoenborn, Zvika Greenfield, **“Row hammer refresh command,”** US20140006703A1, priority 30 June 2012, published 2 January 2014: <https://patents.google.com/patent/US20140006703A1/en>.
2. Yoongu Kim, Ross Daly, Jeremie Kim, Chris Fallin, Ji Hye Lee, Donghyuk Lee, Chris Wilkerson, Konrad Lai, Onur Mutlu, **“Flipping Bits in Memory Without Accessing Them: An Experimental Study of DRAM Disturbance Errors,”** ISCA 2014: <https://istc-cc.cmu.edu/publications/papers/2014/kim-isca14.pdf>.
3. CMU-SAFARI, **rowhammer** experimental source repository accompanying the ISCA 2014 work: <https://github.com/CMU-SAFARI/rowhammer>.
4. Micron Technology, **4Gb: x4, x8, x16 DDR4 SDRAM**, document `09005aef84af6dd0`, Rev. E 11/15, `Target Row Refresh Mode`; archived distributor mirror: <https://tz.yic-electronics.com/datasheet/cf/MT40A256M16GE-083E-B.pdf>.
5. Pietro Frigo et al., **“TRRespass: Exploiting the Many Sides of Target Row Refresh,”** IEEE Symposium on Security and Privacy, 2020, DOI 10.1109/SP40000.2020.00090: <https://doi.org/10.1109/SP40000.2020.00090>; author/arXiv record: <https://arxiv.org/abs/2004.01807>.
