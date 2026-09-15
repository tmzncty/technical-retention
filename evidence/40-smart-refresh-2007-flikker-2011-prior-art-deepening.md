# Case 40 evidence deepening — Smart Refresh (2007) and Flikker (2011) before RAIDR

**Status:** `bounded deepening complete`

## Question and boundary

Case 40 already grounds RAIDR (ISCA 2012) as a retention-profile-mediated DRAM refresh design and uses the 2013 commodity-DRAM retention study to bound the validity of saved retention profiles. The remaining historical problem is narrower:

> Before RAIDR, what substantially different reasons had already been used to justify skipping or weakening DRAM refresh, and which state had to be retained to make those policies work?

This record inspects two peer-reviewed pre-RAIDR systems papers:

1. Mrinmoy Ghosh and Hsien-Hsin S. Lee, **“Smart Refresh: An Enhanced Memory Controller Design for Reducing Energy in Conventional and 3D Die-Stacked DRAMs,”** MICRO 2007.
2. Song Liu, Karthik Pattabiraman, Thomas Moscibroda, and Benjamin G. Zorn, **“Flikker: Saving DRAM Refresh-power through Critical Data Partitioning,”** ASPLOS 2011.

They are used as **prior-art mechanism records**, not as evidence that RAIDR copied either implementation and not as proof of shipped commercial deployment.

The bounded result is that at least three distinct refresh-reduction relations were public before/at RAIDR:

```text
Smart Refresh (2007)
    recent ordinary access refreshed the row
    -> remember access recency
    -> skip redundant periodic refresh

Flikker (2011)
    software marks data as non-critical
    -> allocate by semantic criticality
    -> deliberately use lower refresh for the non-critical region
    -> accept some corruption

RAIDR (2012)
    profile physical retention heterogeneity
    -> retain row/bin classification
    -> choose row-specific cadence intended to preserve all rows
```

Therefore, `fewer refresh operations` is not a sufficient mechanism description.

---

## Source ladder

### P1 — IEEE / MICRO 2007: Smart Refresh

IEEE Xplore’s record and abstract for Ghosh and Lee’s MICRO 2007 paper directly describe the mechanism: a timeout counter is associated with each DRAM row; a row recently read or written by the processor or another device does not need an additional periodic refresh because the access has already restored the row. The paper evaluates the design in simulation and reports refresh-operation and energy reductions.

Primary record:

- DOI: <https://doi.org/10.1109/MICRO.2007.13>
- IEEE Xplore title: **Smart Refresh: An Enhanced Memory Controller Design for Reducing Energy in Conventional and 3D Die-Stacked DRAMs**
- conference: 40th Annual IEEE/ACM International Symposium on Microarchitecture, 1–5 December 2007.

This evidence is sufficient for the bounded historical claim `per-row access-recency / timeout state was already proposed as a refresh-elision input in 2007`. It is not used here to infer an undocumented commercial implementation.

### P2 — ACM / author-hosted full paper: Flikker

The ASPLOS 2011 paper is available from Microsoft Research as the authors’ full PDF:

- Microsoft Research publication page: <https://www.microsoft.com/en-us/research/publication/flikker-saving-dram-refresh-power-through-critical-data-partitioning/>
- author-hosted PDF: <https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ASPLOS_2011.pdf>
- DOI: <https://doi.org/10.1145/1950365.1950391>

The paper explicitly says that programmers distinguish critical and non-critical data, the runtime allocates them to separate memory pages/regions, critical data receives the normal refresh rate, and non-critical data receives a substantially lower rate at the deliberate cost of some data corruption. It describes Flikker as mainly software plus modest hardware support and discusses extending Partial-Array Self-Refresh (PASR)-style controls so different regions can use different rates.

### P3 — RAIDR comparison anchor

The original RAIDR paper remains the mechanism anchor for Case 40:

- CMU/PDL record: <https://pdl.cmu.edu/PDL-FTP/NVM/raidr-isca12_abs.shtml>
- DOI: <https://doi.org/10.1109/ISCA.2012.6237001>

RAIDR groups rows by measured retention time, represents short-retention bins with Bloom filters, and chooses different refresh frequencies by those bins. Its stated objective is to eliminate unnecessary refresh while preserving data integrity under its profiling/model assumptions.

---

## Historical record

### H/P — 2007 Smart Refresh uses access recency, not retention-time profiling

Ghosh and Lee’s abstract states that Smart Refresh maintains a timeout counter for each memory row. If a row has recently been read or written, the design treats the ordinary access as having refreshed the cells and skips the otherwise scheduled periodic refresh.

The policy input is therefore **elapsed time since a restorative access**, not a measured estimate of how long that row’s weakest cell can retain charge.

Bounded relation:

```text
recent ordinary row access
    -> row already restored recently
    -> scheduled refresh can be redundant
```

This is materially different from:

```text
measured weak/strong row classification
    -> row assigned to a retention-time bin
    -> cadence selected from the bin
```

The two designs may both reduce refresh count, but they retain different controller knowledge and rely on different safety arguments.

### H/P — Smart Refresh retains per-row scheduling history

A timeout counter per row is control state about **when that row was last refreshed by an ordinary access or equivalent restoration event**. Losing or corrupting that history has a different meaning from losing payload bits.

The paper’s public mechanism therefore provides an earlier instance of second-order state governing maintenance, but the state is **activity history**, not a physical retention profile.

Historical vocabulary used here stays close to the paper: `time-out counter`, `memory row`, recent `read`/`write`, and periodic `refresh`. `Maintenance-history metadata` is this repository’s engineering reconstruction.

### H/P — 2011 Flikker changes the retention obligation by software-declared criticality

Flikker deliberately makes a different trade. Its abstract and introduction state that:

- programmers mark critical versus non-critical data;
- runtime/OS support separates them into different memory pages/regions;
- critical data stays at the regular refresh rate;
- non-critical data is refreshed at a substantially lower rate;
- the lower rate knowingly increases corruption in non-critical data.

The design therefore does **not** claim that every skipped refresh is redundant under a physical-retention model. Instead, it accepts weaker hardware correctness for data the application is expected to tolerate losing or corrupting.

Bounded relation:

```text
application semantic classification
    -> placement in a refresh region
    -> different refresh policy
    -> intentionally different error exposure
```

That is not RAIDR’s relation.

### H/P — Flikker ties software semantics to refresh geometry

The paper says Flikker builds on mobile-DRAM partial-refresh ideas and proposes hardware support that allows different portions of memory to receive different refresh rates. The software side adds a construct for marking non-critical data plus OS/runtime support to allocate such data to the corresponding region.

This creates a chain across layers:

```text
programmer/application semantic judgment
    -> runtime/OS allocation
    -> physical memory region
    -> region refresh cadence
```

The retained classification is therefore not a measurement of cell leakage. It is a policy decision about which payload is permitted to face a higher corruption probability.

### H/P — Flikker’s own novelty claim is scoped to software-controlled intentional error exposure

Flikker states a bounded `to the best of our knowledge` claim: it presents itself as the first software technique to intentionally introduce hardware errors for memory power savings based on application characteristics. This record preserves that scope. It does not rewrite the claim into `Flikker invented reduced-refresh DRAM`, which Smart Refresh and earlier device/power-management work would already contradict.

### H/P — RAIDR’s historical novelty boundary is consequently narrower than “first selective refresh”

RAIDR itself cites Smart Refresh as prior work and frames its contribution around exploiting **retention-time variation** with a low-cost memory-controller modification. The pre-2012 record therefore blocks several retrospective shortcuts:

```text
selective refresh existed before RAIDR
    != retention-profile binning existed in the same form

software-semantic reduced refresh existed before RAIDR
    != RAIDR accepted intentional corruption

per-row recency tracking existed before RAIDR
    != per-row retention-time profiling
```

---

## Engineering reconstruction

### E — the same actuator can be driven by different evidence

All three schemes ultimately modify refresh work, but the decision inputs differ:

| Mechanism | Decision evidence | Retained control state | Intended consequence |
| --- | --- | --- | --- |
| Smart Refresh | recent access/restoration | per-row timeout/recency state | skip a refresh argued to be redundant |
| Flikker | application-declared criticality | semantic class + placement relation | save power while accepting errors in selected data |
| RAIDR | measured row retention behavior | retention-time bins / Bloom filters + schedule state | lower cadence for stronger rows while intending full preservation |

This is a useful anti-flattening rule:

> **same maintenance actuator != same maintenance authority or justification.**

### E — “weakening maintenance” and “proving maintenance redundant” are different operations

Smart Refresh’s safety argument is temporal: an ordinary access has already performed the restorative work recently enough that another scheduled refresh is redundant.

Flikker’s argument is semantic: some data may tolerate more corruption, so the system intentionally weakens maintenance for that class.

RAIDR’s argument is physical/model-based: measured retention heterogeneity indicates that many rows can safely wait longer.

Therefore:

```text
redundant refresh elimination
    != accepted-loss maintenance reduction
    != retention-profile-aware cadence reduction
```

### E — the retained metadata can describe history, meaning, or substrate behavior

The comparison adds three kinds of non-payload state:

1. **history metadata** — when a row was last restored/accessed;
2. **semantic/policy metadata** — whether software treats data as critical;
3. **substrate-profile metadata** — how long a row is believed to retain data.

All can affect whether refresh work occurs, yet their validity conditions differ.

A Smart Refresh counter becomes unsafe if restoration history is wrong or stale. A Flikker classification becomes unsafe relative to application expectations if criticality/placement is wrong. A RAIDR profile becomes unsafe if physical behavior was mismeasured or changes through DPD/VRT.

### E — conservative-error direction differs across the three schemes

Case 40 already notes that RAIDR’s Bloom-filter false positive can safely cause **extra** refresh if the weak-row population was correctly identified.

The prior art highlights different error directions:

- Smart Refresh falsely believing a row was recently restored could cause under-maintenance; forgetting recency generally tends toward extra refresh rather than less refresh.
- Flikker misclassifying critical data as non-critical can expose semantically important payload to a deliberately weaker refresh regime.
- RAIDR misclassifying a weak row as strong can under-refresh it; representing a strong row as weak tends toward extra work.

Thus `metadata error` is too coarse. What matters is **which direction an error moves maintenance authority**.

### E — persistence horizon depends on the policy state

These mechanisms also resist one universal answer to “must the metadata persist?”

- recent-access timeout state only needs to cover the live scheduling horizon; after a conservative reset, a controller can resume by treating rows as needing normal refresh;
- Flikker’s critical/non-critical relation must survive or be reconstructed as long as the associated data remains allocated under that semantic policy;
- RAIDR explicitly proposes saving its profiled bins for reuse across boots, creating a longer persistence horizon and therefore a staleness problem.

The last clause is an engineering comparison, not a claim that the Smart Refresh or Flikker papers specify a particular crash-recovery protocol.

---

## Cross-case comparison

### Case 35 — PASR is a coverage primitive; Flikker adds semantic policy

Case 35 treats Partial-Array Self-Refresh as a selective-retention mechanism in commercial mobile DRAM: some regions can be excluded from refresh. Flikker discusses extending PASR-like hardware so different regions can use different rates, but the application-level contribution is the criticality classification and allocation policy above that hardware primitive.

Therefore:

> **PASR capability != Flikker’s application-semantic policy.**

No genealogy beyond the paper’s stated dependency is inferred.

### Case 93 — profile staleness is specific to a substrate model

Case 93 and Case 40 stress that a retained physical profile can become stale because of VRT/DPD. Smart Refresh’s recency counter and Flikker’s semantic class can also become wrong, but for different reasons. They should not be relabeled as VRT/profile-staleness mechanisms.

### Case 34/133 — environmental evidence is another independent policy input

Temperature-conditioned refresh uses environmental state. The present comparison adds access history and semantic criticality as two other inputs. A single system could, in principle, combine several such inputs, but this evidence does not claim that any of the three historical systems did so.

---

## Functional analogy — bounded

A useful functional analogy is that all three designs keep **control state about why a future maintenance action may be skipped or weakened**.

The analogy stops at that abstraction. A timeout counter is not a retention profile; a programmer annotation is not a sensor; a Bloom-filter bin is not an application-value judgment. Similar effects on refresh traffic do not establish shared implementation, shared genealogy, or shared failure semantics.

---

## Philosophical interpretation — bounded

The historical record supports a narrow conceptual distinction:

> Technical retention can be reduced because maintenance is known to have happened recently, because the substrate is modeled as needing less maintenance, or because the system elects to tolerate more forgetting for selected content.

These are three different relations among memory, maintenance, and value. The final clause is a repository interpretation of Flikker’s explicit correctness/energy trade, not language attributed to the paper’s authors beyond their documented `critical/non-critical` and reliability vocabulary.

---

## Explicit non-claims

This evidence does **not** claim that:

- Smart Refresh, Flikker, or RAIDR were deployed in a named commercial memory controller;
- Smart Refresh measured row retention time;
- Flikker inferred physical row weakness;
- Flikker preserved every non-critical bit despite lower refresh;
- RAIDR intentionally accepted application-visible corruption as part of its normal objective;
- PASR and Flikker are identical mechanisms;
- a Smart Refresh timeout counter must persist across reboot;
- Flikker’s semantic metadata has a particular crash-consistency protocol;
- the listed works are the complete pre-2012 prior-art genealogy;
- MICRO 2007 or ASPLOS 2011 publication establishes invention priority over all patents, internal industry work, or earlier publications;
- similar refresh reduction proves a direct technical genealogy among the three designs.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Smart Refresh was published at MICRO 2007 | H/P | IEEE conference record |
| Smart Refresh uses a timeout counter per memory row | H/P | IEEE abstract/mechanism description |
| Smart Refresh skips periodic refresh for rows recently read/written | H/P | IEEE abstract/mechanism description |
| Smart Refresh therefore uses access-recency state rather than a measured retention-time bin | E | direct mechanism comparison with RAIDR |
| Flikker was published at ASPLOS 2011 | H/P | ACM/Microsoft Research full paper |
| Flikker separates critical and non-critical data through programmer/runtime support | H/P | full paper abstract/introduction/design overview |
| Flikker keeps critical data at regular refresh and lowers refresh for non-critical data | H/P | full paper abstract/introduction |
| Flikker explicitly accepts some data corruption in the lower-refresh class | H/P | full paper abstract/introduction |
| Flikker discusses extending PASR-style hardware so regions can use different rates | H/P | full paper introduction/design overview |
| Flikker’s semantic classification is equivalent to measuring cell retention time | X | contradicted by mechanism |
| Smart Refresh’s recency counter is equivalent to RAIDR’s retention profile | X | contradicted by mechanism |
| RAIDR was the first system to reduce DRAM refresh selectively | X | pre-2012 prior art contradicts the broad claim |
| The pre-RAIDR papers prove a direct genealogy into RAIDR | X | no such lineage established by this evidence |
| Reduced refresh always means the same retention contract | X | comparison shows distinct redundancy, accepted-error, and physical-profile regimes |

---

## Related repositories

Fresh repository searches found no dedicated `Smart Refresh` or `Flikker` case in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). A full chronology of DRAM-controller refresh-reduction research, PASR standard evolution, or commercial adoption belongs there if developed. This evidence keeps only the retention-specific distinctions needed by Case 40.

The anti-anachronism rule from [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) remains important: `time-out counter`, `critical/non-critical data`, `PASR`, `retention time bins`, and `Bloom filters` are historical technical vocabulary; `history metadata`, `semantic policy metadata`, and `substrate-profile metadata` are repository reconstruction terms.

---

## Sources

1. Mrinmoy Ghosh and Hsien-Hsin S. Lee, **“Smart Refresh: An Enhanced Memory Controller Design for Reducing Energy in Conventional and 3D Die-Stacked DRAMs,”** 40th Annual IEEE/ACM International Symposium on Microarchitecture (MICRO 2007), Chicago, 1–5 December 2007. DOI: <https://doi.org/10.1109/MICRO.2007.13>. Inspected publisher record/abstract for per-row timeout state, recent-read/write refresh elision, evaluation scope, and date.
2. Song Liu, Karthik Pattabiraman, Thomas Moscibroda, Benjamin G. Zorn, **“Flikker: Saving DRAM Refresh-power through Critical Data Partitioning,”** ASPLOS XVI, 5–11 March 2011, pp. 213–224. DOI: <https://doi.org/10.1145/1950365.1950391>. Author-hosted full PDF: <https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ASPLOS_2011.pdf>. Inspected abstract, Introduction, Design Overview, and opening hardware discussion for critical/non-critical classification, deliberate corruption trade, allocation, PASR relation, and differing refresh rates.
3. Jamie Liu, Ben Jaiyen, Richard Veras, Onur Mutlu, **“RAIDR: Retention-Aware Intelligent DRAM Refresh,”** ISCA 2012. DOI: <https://doi.org/10.1109/ISCA.2012.6237001>. CMU PDL record: <https://pdl.cmu.edu/PDL-FTP/NVM/raidr-isca12_abs.shtml>. Used only as the comparison anchor already grounded by Case 40.

## Bounded conclusion

The historical floor for selective DRAM refresh cannot be summarized as `RAIDR introduced skipping refresh`. By 2007, Smart Refresh had already proposed per-row access-recency state to suppress refreshes made redundant by recent reads/writes. By 2011, Flikker had already connected software-declared data criticality to heterogeneous refresh rates and explicitly accepted a bounded increase in corruption for the non-critical class. RAIDR’s 2012 contribution occupies a different point: it uses measured physical retention heterogeneity to assign cadence while intending to preserve all data under its profiling assumptions.

For `technical-retention`, the durable lesson is not a priority slogan but a decomposition:

```text
maintenance reduction because restoration happened recently
    !=
maintenance reduction because forgetting is acceptable for selected payload
    !=
maintenance reduction because measured substrate margin is larger
```

Each relation needs different retained control state, has different unsafe error directions, and creates a different contract with the payload it is trying to retain.