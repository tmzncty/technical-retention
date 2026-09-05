# Grounding record — DRAM variable retention time and profile staleness, 1987–2013

## Purpose

This record grounds [`../cases/93-dram-variable-retention-time-profile-staleness.md`](../cases/93-dram-variable-retention-time-profile-staleness.md).

The bounded question is not `what is the whole history of DRAM retention testing?` It is:

> **When refresh policy is chosen from a retained measurement/profile of row retention time, what primary evidence shows that the represented retention behavior can later change or depend on measurement context, so that a perfectly preserved profile can become unsafe?**

The source set deliberately combines:

1. a 2012 architecture paper that makes stored retention-time classification an explicit controller input;
2. a 2013 large commodity-DDR3 characterization that directly tests the accuracy assumptions of retention-time profiling;
3. earlier VRT device evidence from IBM Research and a Micron manufacturer patent;
4. the 2013 paper's conservative bibliography for the 1987 `variable hold time` chronology.

The broader history of DRAM manufacturing test, JEDEC refresh standards, transistor-level VRT physics, online profiling, and later DDR generations is outside this record.

---

## Source A — RAIDR, ISCA 2012

**Jamie Liu, Ben Jaiyen, Richard Veras, Onur Mutlu, “RAIDR: Retention-Aware Intelligent DRAM Refresh,” Proceedings of the 39th International Symposium on Computer Architecture (ISCA), Portland, Oregon, 9–13 June 2012.**

CMU Parallel Data Laboratory abstract:

- <https://pdl.cmu.edu/PDL-FTP/NVM/raidr-isca12_abs.shtml>

Full paper:

- <https://pdl.cmu.edu/PDL-FTP/NVM/raidr-isca12.pdf>

### Evidence role

`P/S` — original peer-reviewed architecture research. It is used here as an explicit example of a retention-aware control design whose correctness depends on stored profiling state. This case does **not** claim RAIDR was deployed in commodity systems.

### Exact anchors used

#### Abstract / §1 — retention-time bins become controller state

- printed p. 1: RAIDR groups DRAM rows into retention-time bins and applies different refresh rates to the bins;
- the paper stores those bins in the memory controller, implemented with Bloom filters;
- the abstract reports the specific evaluated storage overhead and refresh/power/performance effects, but those performance numbers are not central to Case 93.

Use this to support:

- `retention-aware refresh can replace some recurring maintenance work with retained classification knowledge`;
- `retention profile/bin state ≠ user payload`.

Do not use it to claim all retention-aware mechanisms use Bloom filters.

#### §3.1, printed p. 4 — profile → bin → refresh decision

The operational path is explicit:

1. profile each row's retention time;
2. if needed, insert it into the corresponding bin;
3. during operation, consult bins when the row becomes a refresh candidate;
4. refresh according to the bin interval or default interval.

The paper states that because rows are refreshed at an interval equal to or shorter than their **measured** retention time, data integrity is guaranteed in the model.

Use this to support the bounded dependency:

```text
profile measurement
    -> retained classification
    -> maintenance deadline
    -> payload integrity
```

The word `measured` is crucial. Case 93 tests whether the measured value remains conservative.

#### §3.2, printed pp. 4–5 — profile persistence across boots

The straightforward profile procedure writes static patterns, disables refresh, and observes the first bit change. After measurement, the paper says results can be saved by the operating system and restored into the memory controller on later boots without further profiling, based on the cited assumption that retention time does not change significantly over a cell's lifetime.

A footnote on the same page already notes that circuit-level crosstalk makes retention depend on nearby stored values and that the worst-case pattern depends on array architecture; further analysis is left to future work.

Use this to support:

- `profile persistence across boot is an explicit architectural proposal`;
- `RAIDR itself acknowledged a data-pattern qualification problem`;
- the later 2013 study is a direct stress test of an assumption, not an unrelated modern analogy.

Do **not** write `RAIDR is incorrect`; the paper describes an evaluated proposal under its model and leaves some profiling questions open.

#### §3.7, printed p. 7 — permanently stored profiles in attached systems

For 3D-stacked DRAM/eDRAM where controller logic is permanently attached to the memory, the paper discusses profiling once and permanently storing results in controller fuses/ROM.

Use this only to show that profile longevity was a deliberate design possibility. Do not infer actual shipped fused RAIDR profiles.

---

## Source B — Liu et al., ISCA 2013

**Jamie Liu, Ben Jaiyen, Yoongu Kim, Chris Wilkerson, Onur Mutlu, “An Experimental Study of Data Retention Behavior in Modern DRAM Devices: Implications for Retention Time Profiling Mechanisms,” ISCA 2013, Tel Aviv, Israel, June 2013.**

Institutional landing page:

- <https://istc-cc.cmu.edu/publications/papers/2013/dram-retention-time-characterization_isca13_abs.shtml>

Full paper:

- <https://istc-cc.cmu.edu/publications/papers/2013/dram-retention-time-characterization_isca13.pdf>

### Evidence role

`P/S` — original peer-reviewed experimental research and the main evidence that static retention profiles are challenged by DPD and VRT in the tested commodity DDR3 population.

### Exact anchors used

#### Abstract / §1 — sample and the two profiling problems

- printed p. 1: the authors tested **248 commodity DDR3 chips from five major vendors** using a temperature-controlled FPGA platform;
- they identify `data pattern dependence`, where retention time is affected by data stored in other cells;
- they identify `variable retention time`, where retention time of some cells changes unpredictably over time;
- the introduction explicitly says prior profile-based mechanisms depend on profile accuracy.

Use this to support:

- `profile correctness is an independent requirement from profile storage`;
- `retention time is not always a context-free fixed scalar`.

The sample is large and multi-vendor but still historical and bounded. Do not universalize every numeric result to all DRAM.

#### §1 — simple patterns can miss weak cells

The introduction reports that in some tested devices, using only all-1/all-0 patterns identifies **less than 15%** of weak cells found with broader pattern exploration. The exact effect varies across device design/process.

Use this to support:

- `profiling data pattern ≠ neutral context`;
- `address coverage ≠ worst-case state/context coverage`.

Do not claim all-1/all-0 always miss 85% of weak cells; the paper explicitly says `in some devices`.

#### §1 and §6.1 — VRT can invalidate small fixed margins

The introduction says VRT can lower a cell's retention time significantly below the measured value and that even a **2× safety margin may not suffice**. In §6.1, the measured minimum/maximum behavior includes cells changing by more than a factor of four; the authors say guardband-only handling in that observed population would require a large guard band, greater than four.

Use this to support:

- `guard band ≠ proof against unbounded/unobserved state change`;
- `measured deadline ≠ permanently safe deadline`.

Do not turn these into universal DDR guard-band requirements.

#### §2.3 — profile assumption and physical/context factors

The paper summarizes prior proposals as mechanisms that measure/store retention time and then adjust refresh rate. It explicitly says such works assume the profile stays the same and remains conservative enough for data integrity. It then names DPD and VRT as time/context-dependent effects that violate the simple assumption.

For DPD it discusses data-dependent bitline/wordline coupling and noise. For VRT it states that many cells transition between multiple leakage-current and retention-time states, and summarizes the charge-trap / TA-GIDL explanation from prior device literature.

Use the physical explanation cautiously: Case 93 needs the measured profile-instability fact, not a claim that every microscopic pathway is settled.

#### §6.1 — VRT prevalence in the tested population

The paper reports VRT in all tested device families and says that among cells with low minimum retention times — those most relevant to refresh reduction — cells exhibiting VRT are more common than cells without it. It reports changes exceeding 4× in some cells and concludes profile-based mechanisms must adapt to changes in the retention profile.

Use this to support:

- `profile revalidation/adaptation can be a maintenance obligation`;
- `more durable profile storage does not solve profile staleness`.

#### §6.2 — observation window can miss the low-retention state

The paper reports substantial populations remaining in a high-retention state for about **15,000 s (~4 h)** and some staying high for nearly the full **~1-day** experiment. It concludes profiling may need to continue on the order of days to reliably observe lowest states.

Use this to support:

- `profiling duration ≠ proof of observing the worst state`;
- `complete address sweep ≠ complete temporal-state characterization`.

Do not claim every DRAM requires days of profiling.

#### §6.3 — architectural unpredictability and lifecycle boundary

The paper says that at the architectural level there appears to be no way to determine whether a cell exhibits VRT without observing it transition, and discusses online profiling/ECC as future directions. It also says high-temperature exposure such as soldering can induce VRT in previously unsusceptible cells according to cited device literature, so a pre-assembly manufacturer profile may not match the final assembled module.

Use this to support:

- `manufacturing profile ≠ final-system profile` as a lifecycle-bounded risk;
- `profile reuse across lifecycle transitions needs evidence`.

Do not claim all soldering creates VRT.

#### §7.3 — VRT chronology

The paper states that VRT was first observed by Yaney et al. and later confirmed/investigated by Restle et al., with the earlier works establishing multiple retention states and exponentially distributed state residence times.

Use this as a scholarly bridge for chronology. The 1987 full text was not directly inspected in this slice, so Case 93 does not rely on it for a detailed mechanism claim.

---

## Source C — Restle, Park, Lloyd, IBM / IEDM 1992

**P.J. Restle, J.W. Park, B.F. Lloyd, “DRAM variable retention time,” International Electron Devices Meeting (IEDM), 13 December 1992.**

IBM Research publication record:

- <https://research.ibm.com/publications/dram-variable-retention-time>

DOI landing page is linked from the IBM record.

### Evidence role

`H/P` — contemporary device-research witness, with an institutional abstract retained by IBM Research.

### Exact anchor used

The IBM abstract defines VRT as varying cell leakage that changes how long the cell retains information. It reports study of 4 Mbit and 16 Mbit DRAM chips from multiple manufacturers and both trench- and stacked-capacitor technologies, says VRT cells were found on all examined chips, and distinguishes two-state and multi-state VRT.

Use this to support:

- VRT was established as a DRAM device phenomenon by 1992;
- multiple retention states are not a term invented by the 2013 profile study.

Do not use the institutional abstract to reconstruct details that require the uninspected full paper.

---

## Source D — Yaney et al., IEDM 1987

**D.S. Yaney et al., “A meta-stable leakage phenomenon in DRAM charge storage — Variable hold time,” IEDM 1987, pp. 336–339, DOI `10.1109/IEDM.1987.191425`.**

### Evidence role

`H` chronology anchor, indirectly checked through the 2013 peer-reviewed related-work section and bibliographic records. The exact full text was not directly inspected in this slice.

Use only for the narrow statement:

> Liu et al. 2013 identify Yaney et al. 1987 as the first observation of the phenomenon later discussed as VRT, under the vocabulary `variable hold time`.

Do not derive transistor physics, numeric transition rates, or invention priority solely from this uninspected source.

---

## Source E — Micron VRT patent, filed 2002

**Russell L. Meyer and Ray Beffa, “Method of reducing variable retention characteristics in DRAM cells,” US10/230,594, filed 29 August 2002; application US20040042306A1; patent US6898138B2; original assignee Micron Technology, Inc.**

Public patent record:

- <https://patents.google.com/patent/US6898138B2/en>

### Evidence role

`H/P` — manufacturer-primary witness that time-varying retention was an explicit DRAM qualification/manufacturing problem before the 2012–2013 controller-profile papers.

### Exact anchors used

#### Background — variability at constant temperature

The patent says retention time may change as time passes even at constant temperature, making it difficult to specify a guaranteed minimum refresh rate if some cells vary unpredictably.

Use this to support:

- `ordinary temperature dependence ≠ VRT`; both can exist, but time-varying retention cannot be reduced to ambient temperature alone.

#### Fig. 2 example — early qualification can miss later lower-retention state

The detailed description gives an illustrative cell around 120 ms for an initial period, later changing to about 48 ms. It explicitly explains that such a cell could pass a 64 ms-oriented test early and then require faster refresh later, potentially losing data if the system waits too long.

Use this to support:

- `test pass at t1 ≠ guaranteed future retention requirement`;
- `profile staleness can be dangerous even when profile bits are intact`.

The exact values are **illustrative patent examples**, not population statistics.

#### Patent process — VRT mitigation is distinct from controller profiling

The claimed process uses temperature/reverse-bias stress to reduce variable-retention behavior. This case does not evaluate whether that process became a production practice. Its relevance is historical: manufacturers treated unstable retention as a real enough device problem to motivate process-level mitigation.

---

## Claim ledger

| Claim | Label | Source basis | Boundary |
| --- | --- | --- | --- |
| retention-aware refresh can store row classifications and choose refresh rate from them | `H/P` | RAIDR 2012 §§3.1–3.3 | architecture proposal, not generic commodity deployment |
| RAIDR proposed saving a measured profile and reusing it on later boots | `H/P` | RAIDR §3.2 | historical design assumption; not proof profile is immutable |
| permanently attached controller/DRAM designs were proposed as candidates for one-time permanent profile storage | `H/P` | RAIDR §3.7 | proposal only; no shipped-product claim |
| VRT existed in device research by 1992 | `H/P` | IBM Restle et al. IEDM 1992 record | institutional abstract; full-paper details not extrapolated |
| 2013 characterization tested 248 commodity DDR3 chips from five vendors | `H/P` | Liu et al. Abstract / methodology | sample-bounded |
| DPD makes measured retention dependent on stored values elsewhere | `H/P` | Liu et al. §§1–2.3, 5 | mechanism/context finding in tested DDR3 population |
| in some devices all-0/all-1 profiling found less than 15% of weak cells exposed by broader patterns | `H/P` | Liu et al. §1 | `some devices`, not universal |
| VRT can move a cell among multiple retention states | `H/P` | Restle 1992; Liu et al. §§2.3, 6 | broader transistor-physics genealogy remains open |
| 2× guardband was not sufficient as a universal guarantee in the 2013 observations | `H/P` | Liu et al. §1 / §6.1 | not a universal required factor |
| some observed cells changed by more than 4× | `H/P` | Liu et al. §6.1 | tested cells only |
| some VRT cells stayed high-retention for ~4 h and some nearly ~1 day | `H/P` | Liu et al. §6.2 | observation/sample bounded |
| short profiling can miss a future low-retention state | `E` | Liu et al. §6.2–6.3 | engineering consequence of observed residence times |
| high-temperature assembly exposure can invalidate a pre-assembly profile | `H/S` | Liu et al. §6.3 citing prior device work | possibility/evidence boundary, not every assembly |
| Micron described time-varying retention at constant temperature and a test-escape example | `H/P` | US6898138B2 | patent description, exact numbers illustrative |
| measured retention time ≠ immutable cell property | `E` | synthesis of Sources B, C, E | project formulation |
| profile persistence ≠ profile correctness | `E` | RAIDR profile persistence + VRT/DPD evidence | project formulation |
| retention metadata ≠ payload | `E` | RAIDR controller bins versus DRAM data | project formulation |
| maintenance policy may require revalidation/online profiling/error tolerance | `E` | Liu et al. §6.3 + architecture dependency | not a claim one historical standard mandated this |
| VRT ≠ RowHammer | `A/X` | comparison to Case 53 | different causal mechanisms; no genealogy |

---

## Rejected / unsupported claims

### X — `RAIDR invented retention-aware refresh`

Rejected. RAIDR's own related-work section discusses earlier device/controller proposals. This case uses RAIDR because its profile/bin dependency is explicit and well documented.

### X — `the 2013 paper discovered VRT`

Rejected. Its own related-work section identifies Yaney et al. 1987 and Restle et al. 1992 as earlier VRT/VHT work.

### X — `IBM invented VRT in 1992`

Unsupported. The 1992 IBM paper is a strong earlier primary/institutional witness, while the 2013 literature review points to 1987 work before it.

### X — `retention time is always one fixed intrinsic number per cell`

Rejected for the bounded tested population by VRT and DPD evidence.

### X — `a stored profile is safe as long as its bits are preserved`

Rejected as an engineering inference. A bit-perfect profile can cease to be conservative if the represented cell enters a lower-retention state or the measurement context changes.

### X — `2× guardband is always unsafe` or `4× is always required`

Rejected. These are observations/implications from the 2013 tested devices, not universal constants.

### X — `all DRAM requires days of profiling`

Rejected. The paper says some observed VRT state residence times imply profiling may need to run on the order of days to reliably expose lowest states; this is not a universal timing rule.

### X — `all soldering induces VRT`

Rejected. The 2013 paper says high-temperature exposure can induce VRT according to earlier work, which creates a lifecycle boundary; it does not make a universal assembly claim.

### X — `DPD is RowHammer`

Rejected. DPD concerns data-value-dependent retention/sensing context; RowHammer concerns repeated access/activation disturbance. They can both make retention relational without being the same physical mechanism.

### X — `VRT is merely temperature dependence`

Rejected. Temperature strongly influences DRAM retention, but VRT includes time-varying state changes that can occur even at constant temperature in the manufacturer evidence.

### X — `retention profile = complete retention history`

Rejected. A profile/bin is a compressed control classification. It need not preserve the sequence of leakage states, test observations, data patterns, or refresh events that produced it.

---

## Related-repository check

A GitHub code search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `variable retention time`, `DRAM VRT`, and related terms returned no dedicated existing case during this slice. The broader device-physics/history work should go there if undertaken later. `technical-retention` keeps the narrower question of **when retained maintenance knowledge remains authoritative**.

---

## Promotion decision

**Status: `grounded`.**

Reason:

- the control architecture is directly anchored in a contemporary peer-reviewed paper;
- the profile-instability counterexample is directly anchored in a large peer-reviewed multi-vendor device study;
- VRT prior art is independently anchored by IBM Research's 1992 institutional primary record and a Micron manufacturer patent;
- source roles and uninspected 1987 full text are explicitly bounded;
- the case distinguishes historical terminology, engineering reconstruction, functional analogy, and philosophical interpretation;
- remaining gaps are genealogy/deployment/standards work rather than blockers for the bounded retention claim.
