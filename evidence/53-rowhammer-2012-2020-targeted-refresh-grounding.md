# Case 53 Grounding Record — RowHammer, Targeted Refresh, and Mitigation Limits (2012–2020)

## Scope and status

This record grounds [`../cases/53-dram-rowhammer-targeted-refresh-policy.md`](../cases/53-dram-rowhammer-targeted-refresh-policy.md).

**Status: `grounded`.** The bounded claim is not that this file reconstructs the entire RowHammer/security/JEDEC history. It establishes a narrower retention relation with complementary evidence:

1. a **2012-priority Intel primary patent record** for row-hammer detection, victim-row adjacency, and targeted refresh;
2. a **2014 peer-reviewed experimental primary research record** for widespread disturbance errors in tested commodity DRAM and for the proposed PARA mitigation;
3. a **2015 Micron manufacturer product-family document** for `Target Row Refresh Mode` / `MAC` / `tMAW` vocabulary and an automatic-background-TRR claim;
4. a **2020 peer-reviewed black-box empirical qualification** showing that opaque in-DRAM TRR implementations in a bounded sample were not equivalent to immunity against all tested hammering patterns.

The evidence is strong enough to distinguish **physical disturbance**, **ordinary refresh**, **access-history/topology-conditioned extra refresh**, **residual error correction**, and **implementation-level guarantee** without treating any one mitigation label as a universal contract.

---

## Source matrix

| Source | Date / status | Evidence role | What it can establish here | What it cannot establish here |
| --- | --- | --- | --- | --- |
| Kuljit S. Bains et al., US20140006703A1, **“Row hammer refresh command”** | priority 2012-06-30; published 2014-01-02 | period primary patent record | `row hammer event/condition`, thresholded accesses within a time window, target/aggressor vs physically adjacent victim rows, targeted-refresh command architecture, controller/device division of adjacency knowledge | product deployment, every vendor implementation, JEDEC-wide normative semantics |
| Yoongu Kim et al., **“Flipping Bits in Memory Without Accessing Them”**, ISCA 2014 | peer-reviewed experimental paper | primary research / direct experiment | 129-module/972-chip test population, 110 affected modules/836 chips, observed disturbance threshold, nearby-row charge-loss mechanism, mitigation taxonomy, PARA design and modeled tradeoffs | invention priority for the whole phenomenon, PARA commercial deployment, universal thresholds for later DRAM |
| Micron Technology, **4Gb x4/x8/x16 DDR4 SDRAM**, doc. `09005aef84af6dd0`, Rev. E 11/15 | manufacturer datasheet, accessed via archive/distributor mirror | manufacturer product-family primary documentation | `Target Row Refresh Mode`, `maximum activate count (MAC)`, `maximum activate window (tMAW)`, `TRn`, victim-row vocabulary, bounded claim that Micron devices covered by the document automatically perform TRR in the background | independently verified fault immunity, all Micron DDR4 revisions, all DDR4 vendors, exact internal algorithm beyond the document |
| Pietro Frigo et al., **“TRRespass: Exploiting the Many Sides of Target Row Refresh,”** IEEE S&P 2020 | peer-reviewed empirical security/reliability evaluation | later independent qualification | black-box evidence that implementation-specific TRR could be bypassed in 13 of 42 tested DDR4 modules using TRR-aware/many-sided patterns; mitigation class is not a universal implementation guarantee | all TRR implementations fail; the precise internal design of every tested device; post-2020/DDR5 behavior |

---

## A. Intel 2012-priority targeted-refresh record

### Bibliographic anchor

- Kuljit S. Bains, John B. Halbert, Christopher P. Mozak, Theodore Z. Schoenborn, Zvika Greenfield, **“Row hammer refresh command,”** US20140006703A1.
- Priority: **30 June 2012**.
- Publication: **2 January 2014**.
- Source: Google Patents full text: <https://patents.google.com/patent/US20140006703A1/en>.

### Claims grounded

The filing explicitly treats repeated accesses to one row within a bounded time window as a `row hammer event` / `row hammer condition`. It describes the heavily accessed row separately from a **physically adjacent** row whose stored data may become corrupted. It also describes a `targeted refresh command` path in which a memory controller can identify the hammered row and a memory device can refresh one or more victim rows.

This directly grounds the following historical statements before the 2014 ISCA paper:

- `row hammer` vocabulary existed in Intel work with 2012 priority;
- a threshold number of accesses in a time window could be treated as a mitigation trigger;
- the vulnerable state may reside in an adjacent row rather than in the row being directly accessed;
- a controller can identify an aggressor/target row while the DRAM device resolves the physical victim neighbor(s);
- logical row numbering need not expose manufacturer-specific physical adjacency/remapping.

### Why this matters for prior art

The safe chronology is:

> **2014 open experimental characterization ≠ invention of RowHammer-aware targeted refresh.**

The 2014 paper can still be historically important for broad open empirical characterization, real-system demonstration, mitigation comparison, and PARA. The patent prevents the repository from assigning a false invention priority to it.

### Limits

A patent application is evidence that the concepts and vocabulary were formulated and disclosed. It is **not** evidence that a particular Intel memory controller or DRAM product shipped the exact disclosed mechanism, and it is not a JEDEC specification.

---

## B. Kim et al. ISCA 2014 — measured disturbance and PARA

### Bibliographic anchor

- Yoongu Kim, Ross Daly, Jeremie Kim, Chris Fallin, Ji Hye Lee, Donghyuk Lee, Chris Wilkerson, Konrad Lai, Onur Mutlu, **“Flipping Bits in Memory Without Accessing Them: An Experimental Study of DRAM Disturbance Errors,”** *Proceedings of ISCA*, 2014.
- CMU/ISTC paper PDF: <https://istc-cc.cmu.edu/publications/papers/2014/kim-isca14.pdf>.
- Companion experimental repository: <https://github.com/CMU-SAFARI/rowhammer>.

### Exact empirical anchors used

The abstract/introduction reports:

- **129 DRAM modules** tested;
- **972 DRAM chips** represented;
- disturbance errors in **110 modules / 836 chips**;
- a minimum observed disturbance threshold of approximately **139K row activations** in the tested population;
- the physical account that repeatedly toggling a row's wordline can accelerate charge leakage in nearby rows and eventually induce bit flips.

These numbers are retained as **bounded experimental results for the sampled contemporary DRAM**, not as universal thresholds for all DRAM technologies.

### Section 8 mitigation anchors

The paper compares multiple mitigation families rather than treating `refresh` as one undifferentiated action:

- stronger ECC;
- globally increasing refresh frequency;
- retiring/remapping vulnerable cells;
- tracking frequently activated rows and refreshing their neighbors;
- the proposed **Probabilistic Adjacent Row Activation (`PARA`)** mechanism.

PARA is important because it is explicitly designed to avoid per-row hotness counters. On a row close, the controller probabilistically activates an adjacent row, so more aggressor accesses create more opportunities for a victim refresh **without storing a full per-row activation-history table**.

The paper also explicitly treats PARA as probabilistic. The failure probability can be driven very low under chosen assumptions/parameters, but it is not an absolute deterministic prevention theorem for every implementation and workload.

### Engineering conclusions supported

From the measured mechanism and mitigation comparison, the repository can safely reconstruct:

> **meeting the ordinary refresh schedule ≠ immunity to access-induced retention loss**.

The ordinary DRAM refresh deadline can be met while repeated activity on another row accelerates the victim's loss of charge margin.

It can also reconstruct:

> **periodic refresh deadline ≠ disturbance-conditioned refresh urgency**.

And PARA supplies the counterexample:

> **workload-conditioned maintenance ≠ necessarily explicit per-row history retention**.

### Deployment limit

The paper evaluates PARA as a research proposal. Its reported performance/reliability tradeoffs are characterization/simulation results, **not named commercial-controller deployment evidence**.

---

## B.1 Additional exact ISCA 2014 anchors retained after duplicate-case consolidation

A later research pass accidentally created a second RowHammer case around the same 2012 Intel patent and 2014 Kim et al. paper. That duplicate case has been removed; the useful non-duplicative source anchors are retained here.

### §2.2–§2.4 — aggressor restoration can coexist with victim degradation

Kim et al. describe ordinary row activation as sensing through the row buffer followed by restoration of the opened row's cell charge. Combined with the measured aggressor/victim disturbance relation, this supports the bounded engineering reconstruction:

> repeated aggressor activation can repeatedly restore the aggressor row while contributing to accelerated leakage in physically nearby victim rows.

This is not a claim that the paper used the phrase `aggressor restoration`; it is a mechanism-level inference from the documented access/restore path and disturbance measurements.

### §7 — victim cells are not merely ordinary weak-retention cells

The paper's `Victim Cells ≠ Weak Cells` subsection compares disturbance victims with cells identified by a long no-access/no-refresh retention test and reports little overlap in the characterized modules. The authors state cautiously that the disturbance coupling pathway may be independent of the process variation responsible for ordinary weak cells.

Use this to block:

- `RowHammer victim = shortest ordinary retention-time cell`;
- `RowHammer is only ordinary passive leakage with a uniformly faster clock`.

The conclusion remains sample-bounded to the measured devices.

### §8.1 — quantitative global-refresh cost witness

Kim et al. report that globally shortening the refresh interval can eliminate disturbance errors under the tested conditions, but at substantial performance/energy cost. Their illustrative 8.2 ms interval is associated with estimated refresh-time overhead of roughly 11–35%, compared with the cited baseline range of roughly 1.4–4.5%.

Use this to support:

- `global faster refresh ≠ targeted refresh`;
- the choice of mitigation changes trigger, scope, retained control state, and maintenance cost even when the underlying restoration operation is still refresh.

Do not universalize these percentages beyond the paper's assumptions and devices.

## C. Micron DDR4 `Target Row Refresh Mode` record

### Document anchor

- Micron Technology, **4Gb: x4, x8, x16 DDR4 SDRAM**.
- Document identifier: `09005aef84af6dd0`.
- Revision: **Rev. E 11/15**.
- Section: **`Target Row Refresh Mode`**.
- Archived/distributor mirror used for direct inspection: <https://tz.yic-electronics.com/datasheet/cf/MT40A256M16GE-083E-B.pdf>.

### Vocabulary and bounded claim

The document defines or uses:

- `Target Row Refresh Mode` / `TRR`;
- `maximum activate count (MAC)`;
- `maximum activate window (tMAW)`;
- a target row (`TRn`) activated excessively within that window;
- adjacent `victim rows` that require refresh.

The document states that Micron DDR4 devices covered by the document automatically perform TRR mode in the background.

This is enough to establish a **manufacturer/product-family record** that targeted disturbance refresh was not only an academic thought experiment by late 2015.

### Provenance qualification

The accessible PDF in this run is a distributor/archive mirror, not a current Micron-hosted URL. The file itself carries Micron's title, identifier, revision, and copyright. Therefore the evidence is recorded as **manufacturer documentation reached through a mirror** rather than silently represented as current official web hosting.

### What is deliberately not inferred

The document does not justify:

- `all DDR4 has the same TRR`;
- `TRR is one standardized internal algorithm`;
- `background TRR guarantees immunity to every possible activation pattern`;
- `the exact tracking capacity/topology algorithm is publicly specified`;
- `a passed datasheet statement equals independent adversarial fault validation`.

---

## D. TRRespass 2020 — empirical qualification of opaque TRR

### Bibliographic anchor

- Pietro Frigo et al., **“TRRespass: Exploiting the Many Sides of Target Row Refresh,”** *2020 IEEE Symposium on Security and Privacy*.
- DOI: <https://doi.org/10.1109/SP40000.2020.00090>.
- Author/arXiv record: <https://arxiv.org/abs/2004.01807>.
- Project/source repository: <https://github.com/vusec/trrespass>.

### Bounded empirical result

The authors use a black-box RowHammer fuzzer to explore TRR-protected DDR4 modules. They report finding TRR-aware access patterns capable of inducing bit flips in **13 of 42** tested modules across the three major DRAM vendors. Many of the useful patterns are **many-sided**, spreading activation across multiple aggressor rows rather than using only one or two obvious aggressors.

### What this qualifies

The result supports:

> **TRR presence ≠ universal RowHammer immunity**.

and:

> **mitigation-class label ≠ complete implementation contract**.

If the internal tracker/sampler/topology policy is opaque, knowing only that a device “has TRR” does not reveal the full set of activation patterns it can reliably contain.

### What this does not prove

The study does **not** prove:

- every TRR implementation is vulnerable;
- every Micron DDR4 device is vulnerable;
- every access pattern bypasses TRR;
- DDR5/Post-2020 refresh-management mechanisms have the same behavior;
- the internal implementation of every tested part is exactly known.

The correct evidence level is bounded empirical qualification, not universal defeat.

---

## Cross-case separations established

### Ordinary refresh vs disturbance-conditioned refresh

Case 03 grounds scheduled DRAM restoration under ordinary leakage. Case 53 adds another trigger:

```text
ordinary time/retention deadline
    -> periodic refresh

aggressor activation history + physical adjacency
    -> extra victim-row refresh urgency
```

These can coexist. RowHammer does not replace the ordinary refresh obligation.

### Temperature/profile feedback vs access-induced victimhood

Cases 34/35 condition refresh on environmental temperature. Cases 40/43 condition policy on measured row-retention behavior and runtime error feedback. Case 53 instead adds **another row's activation history and physical coupling** as inputs.

Therefore:

> **intrinsic retention weakness ≠ access-induced victimhood**.

A row can be an ordinary-retention row yet become vulnerable under a pathological neighboring access pattern.

### Same Bank Refresh vs targeted victim refresh

Case 33's Same Bank Refresh localizes scheduled maintenance by bank/bank-group service geometry. RowHammer targeted refresh localizes **extra restoration** around a disturbance relation.

Therefore:

> **refresh localization for service concurrency ≠ refresh targeting for disturbance containment**.

### Preventive refresh vs ECC/ECS correction

Case 45 grounds on-die ECC/ECS as error correction/scrub/writeback. Case 53's targeted refresh is a preventive/restorative action intended to preserve victim charge before a disturbance becomes an error.

Therefore:

> **disturbance prevention/restoration ≠ residual error correction**.

They can be composed, but they act at different points in the error trajectory.

---

## Rejected overclaims

The following statements are **not** supported and should remain rejected:

- `RowHammer is just ordinary DRAM retention leakage.`
- `The 2014 ISCA paper invented RowHammer-aware refresh.`
- `PARA is a shipped commercial feature in the sources inspected here.`
- `PARA is a deterministic guarantee.`
- `TRR is one transparent standardized algorithm.`
- `A device advertising/implementing TRR is immune to all hammering patterns.`
- `Logical row numbering exposes physical victim adjacency.`
- `Micron's bounded 2015 product-family statement applies to every DDR4 device/vendor/revision.`
- `TRRespass proves all TRR is ineffective.`
- `A 2020 DDR4 result can be projected unchanged onto DDR5/RFM.`

---

## Related-repository duplication check

A current GitHub code search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `RowHammer` and `DRAM disturbance` returned no dedicated case. No technical history was therefore duplicated in this slice.

If later work expands into DRAM scaling, coupling mechanisms, historical security exploitation, full JEDEC DDR4→DDR5 mitigation evolution, or manufacturer-specific controller/device archaeology, that broader engineering history should primarily live in `computing-archaeology` and be linked back here.

---

## Maturity judgment

`grounded` is justified because the central bounded claims no longer depend on one source type:

- **prior-art chronology and architecture** are independently anchored by the 2012-priority Intel patent;
- **physical disturbance and mitigation tradeoffs** are directly measured and analyzed in the 2014 ISCA study;
- **commercial manufacturer vocabulary/product-family claim** is anchored by Micron's 2015 datasheet;
- **implementation-level limitation** is independently tested by TRRespass 2020.

The case is **not `mature`**. A future promotion would benefit from direct official JEDEC text for exact DDR4/LPDDR4 TRR semantics (if normative/publicly available), DDR5 Refresh Management (`RFM`) chronology and behavior, named-product/controller fault-injection with exact revisions, and post-2020 mitigation evolution.

## Sources

1. Bains, Kuljit S., John B. Halbert, Christopher P. Mozak, Theodore Z. Schoenborn, Zvika Greenfield. **“Row hammer refresh command.”** US20140006703A1. Priority 30 June 2012. <https://patents.google.com/patent/US20140006703A1/en>.
2. Kim, Yoongu, Ross Daly, Jeremie Kim, Chris Fallin, Ji Hye Lee, Donghyuk Lee, Chris Wilkerson, Konrad Lai, Onur Mutlu. **“Flipping Bits in Memory Without Accessing Them: An Experimental Study of DRAM Disturbance Errors.”** ISCA 2014. <https://istc-cc.cmu.edu/publications/papers/2014/kim-isca14.pdf>.
3. CMU-SAFARI. **rowhammer** experimental repository. <https://github.com/CMU-SAFARI/rowhammer>.
4. Micron Technology. **4Gb: x4, x8, x16 DDR4 SDRAM**, `09005aef84af6dd0`, Rev. E 11/15, `Target Row Refresh Mode`. Archived/distributor mirror: <https://tz.yic-electronics.com/datasheet/cf/MT40A256M16GE-083E-B.pdf>.
5. Frigo, Pietro et al. **“TRRespass: Exploiting the Many Sides of Target Row Refresh.”** 2020 IEEE Symposium on Security and Privacy. DOI <https://doi.org/10.1109/SP40000.2020.00090>; <https://arxiv.org/abs/2004.01807>.
6. VUSec. **TRRespass** project repository. <https://github.com/vusec/trrespass>.
