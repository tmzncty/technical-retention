# Case 65 Grounding — 3D NAND Early Retention Loss and Age-Aware Reading (2010–2018)

## Status

**Grounded for the bounded case.**

The central mechanism and numerical/operational claims are grounded in the directly inspected 2018 Luo et al. full paper. The 2010 and 2016 papers are used to constrain priority and vocabulary through stable bibliographic/abstract records and the 2018 paper's own discussion of prior work. This record does **not** claim a complete invention genealogy or named-product deployment.

## Bounded research question

> When charge-trap 3D NAND exhibits strongly front-loaded post-program retention loss, what state must remain besides the payload if a controller wants to adapt later reads to the age of the current physical embodiment?

## Source hierarchy

| Source | Type / date | What was inspected | What it supports | What it does not support |
| --- | --- | --- | --- | --- |
| Luo et al., *Improving 3D NAND Flash Memory Lifetime by Tolerating Early Retention Loss and Process Variation*, POMACS 2018, DOI `10.1145/3224432`, arXiv `1807.05140v2` | peer-reviewed primary experimental systems paper | author-accessible full text, especially §§1, 3, 4.3–4.5, 5.2, 6.3 and evaluation | real 3D NAND MLC characterization; 24-day early-retention curve; changing optimal Vref; ReMAR model/metadata/read policy; explicit limitations and comparison to planar techniques | named chip vendor/product; universal 3D/TLC/QLC behavior; commercial ReMAR deployment |
| Choi et al., *Comprehensive evaluation of early retention ... tube-type 3-D NAND Flash Memory*, VLSI Technology 2016, DOI `10.1109/VLSIT.2016.7573385` | primary device paper | bibliographic record + abstract; chronology cross-checked by 2018 paper and 2017 review | source-period `early retention`; fast charge loss within seconds; tube-type 3D NAND; lateral-loss/shared-charge-trap explanation in bounded abstract | 24-day system-level behavior; ReMAR; all later 3D NAND |
| Chen et al., *Study of fast initial charge loss ... charge-trapping NAND flash*, IEDM 2010, DOI `10.1109/IEDM.2010.5703304` | primary device paper | stable bibliographic record/abstract + later review citation | `fast initial charge loss` in charge-trapping NAND by 2010; priority boundary against a 2018 origin claim | a complete 3D-NAND mechanism genealogy; ReMAR or 2018 chip behavior |
| *Reliability of NAND Flash Memories: Planar Cells and Emerging Issues in 3D Devices*, *Computers* 6(2):16, 2017, DOI `10.3390/computers6020016` | scholarly review | references/discussion around 3D retention | independent chronology linking 2010 charge-trap fast loss and 2016 3D early retention | substitute for primary evidence where exact mechanism/claim is decisive |

## Primary-source locations

### Luo et al. 2018

Author-accessible text: <https://arxiv.org/abs/1807.05140>  
Published DOI: <https://doi.org/10.1145/3224432>

The directly inspected full paper supplies the central evidence:

- **Introduction / contribution statement** — distinguishes planar floating-gate NAND from 3D charge-trap NAND; identifies early retention loss as rapid post-program error growth and states that the work extends prior short-duration observation to 24 days.
- **§4.3 Early Retention Loss** — experiment uses multiple blocks across P/E-cycle points, observes retention from minutes out to 24 days, and shows RBER rising approximately one order of magnitude within ~3 hours and much more slowly thereafter; the paper describes the rate as steep initially and flattening with age.
- **§4.3 read-reference discussion** — optimal read-reference voltages move rapidly for young data and more slowly for older data, tying later read interpretation to retention age.
- **§4.4 Retention Interference** — neighboring stored state can alter victim leakage rate; retained only as a boundary/context claim here.
- **§4.5 comparison with planar error sources** — reports lower program-interference/read-disturb sensitivity for the particular characterized generation; this record treats that as generation-bounded and does not generalize it to all later 3D NAND.
- **§6.3 ReMAR** — tracks retention age, uses a retention model plus P/E-cycle/program-time information, and adapts read reference voltage on reads; discusses small controller metadata and a time-source/RTC/host-sync relation.
- **Evaluation** — reports ReMAR reducing RBER in the evaluated population/model; combined techniques yield the paper's larger lifetime/ECC-overhead figures. These are evaluation results, not a field-deployment certificate.

## Chronology / prior-art control

### 2010: charge-trapping NAND fast initial charge loss

Chen et al. publish the phrase **`fast initial charge loss`** in an IEDM paper on charge-trapping NAND. Stable record: DOI `10.1109/IEDM.2010.5703304`.

Safe conclusion:

> fast initial charge loss in charge-trapping NAND predates the 2018 3D-NAND systems characterization.

Unsafe conclusion rejected:

> Chen 2010 already established every later tube-type 3D NAND retention mechanism and controller policy.

### 2016: tube-type 3D NAND `early retention`

Choi et al., DOI `10.1109/VLSIT.2016.7573385`, explicitly describe fast charge loss within seconds as **`early retention`** in tube-type 3D NAND. The abstract attributes the bounded result mainly to lateral charge loss through shared charge-trap layers and studies microsecond-to-second behavior.

Safe conclusion:

> 3D-NAND early-retention observation predates Luo et al. 2018.

The 2018 paper itself says its novelty is **extended-duration observation**, contrasting its 24-day measurements with a prior study confined to roughly the first minutes after program.

### 2018: extended real-chip characterization + age-aware reading

The defensible novelty boundary is not “first early retention.” It is:

> a broad real-chip 3D NAND characterization that extends early-retention observation across a workload-relevant multi-day interval, models the age-dependent distributions/read references, and evaluates a controller mechanism (ReMAR) that tracks age to adapt later reads.

## Claim ledger

| Claim | Label | Evidence | Confidence / limit |
| --- | --- | --- | --- |
| fast initial charge loss in charge-trapping NAND is documented by 2010 | `H/P` | Chen IEDM 2010 record | high for chronology/vocabulary; no broader mechanism priority claim |
| `early retention` in tube-type 3D NAND is documented by 2016 | `H/P` | Choi VLSI 2016 abstract/DOI | high for bounded source claim; full paper not used for unsupported detail |
| Luo et al. experimentally study real 3D NAND MLC chips to 24 days | `H/P` | 2018 full paper §§1, 4.3 | high |
| tested RBER rises about an order of magnitude within ~3 hours, then much more slowly | `H/P` | 2018 §4.3 / plotted data | high, but population-specific |
| optimal read-reference voltage changes with retention age | `H/P` | 2018 §4.3, model | high for tested population |
| ReMAR uses age/P-E/program-time state to adapt Vref | `H/P` | 2018 §6.3 | high as proposal/evaluation |
| controller time state can be retention infrastructure | `E` | reconstruction from ReMAR's timestamp/time-source dependency | strong bounded reconstruction |
| ReMAR physically restores leaked charge | `X` | contradicted by mechanism: it adapts the read boundary | rejected |
| one fixed periodic refresh policy is always sufficient/optimal for 3D NAND | `X` | early-retention curve + FCR transfer evaluation | rejected as universal claim |
| all 3D NAND generations have the paper's same 3-hour/11-day behavior | `X` | device/process dependence | rejected |
| ReMAR shipped in a named product | `X` | no named deployment evidence in source set | rejected |
| early retention loss = read disturb = program interference | `X/A` | mechanisms/triggers differ | rejected except bounded comparison of shared ECC-margin pressure |

## Engineering reconstruction checks

### `nonvolatile` boundary

The paper never requires the page to be continually powered merely to retain its programmed state. The project therefore does **not** call the medium DRAM-like volatile. The narrower reconstruction is:

```text
power-independent charge survival
    !=
time-invariant threshold distribution
    !=
time-invariant optimal read reference
    !=
time-invariant raw-error margin
```

### Controller metadata boundary

ReMAR's program time/P-E information is constitutive only to the **age-aware optimization path**. Losing that metadata does not prove the NAND payload instantly vanishes. Other reading/ECC/recovery paths may remain possible.

Therefore:

> metadata dependence ≠ payload identity.

### Physical renewal boundary

Changing Vref changes interpretation, not the cell's stored charge. Accordingly:

> age-aware reading ≠ FCR rewrite/remap ≠ secure erase.

## Cross-case stop conditions

| Compared case | Safe relation | Stop condition |
| --- | --- | --- |
| Case 36 FCR | both make NAND reliability policy retention-age aware | FCR renews physical embodiment/margin; ReMAR adapts read interpretation; planar/3D evidence regimes differ |
| Case 52 read disturb | both consume finite raw-error/ECC margin | read disturb is caused by repeated access/Vpass stress; early retention loss progresses after program with time |
| Case 59 program interference | both can make cell recoverability relational to nearby physical state/activity | program interference is neighbor-program induced capacitive shift; 3D retention interference is neighbor-conditioned leakage in a charge-trap structure |
| Case 03 / DRAM refresh | both expose time-sensitive reliability policy | DRAM periodic regeneration is constitutive volatile-state restoration; ReMAR is nonvolatile-age-aware read interpretation |
| Case 55 NVMe health telemetry | both retain controller/history-derived metadata | lifetime SMART aggregates device history; a program timestamp estimates age of one current physical embodiment for read policy |

## Related-repository duplication check

Searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for:

- `3D NAND`;
- `early retention loss`;
- `read reclaim`;
- `ReMAR`;

returned no dedicated case at the time of this grounding pass. A general history of charge-trap cells, vertical-stack manufacturing, BiCS/V-NAND, layer scaling, or product genealogy should be built there rather than duplicated here.

## What remains open after this case

This case intentionally leaves several roadmap gaps open:

- modern **3D-NAND read reclaim / device-specific read-disturb management** in named or source-verifiable controllers;
- TLC/QLC and later-generation quantitative early-retention behavior;
- named commercial deployment of age-aware read-reference management;
- HeatWatch/self-recovery + temperature as a distinct 3D-NAND retention policy slice;
- retention-interference/ReNAC as a full independent slice;
- controller metadata loss/corruption experiments for age-aware read policy;
- composition with filesystem/database persistence semantics.

## Sources

1. Yixin Luo, Saugata Ghose, Yu Cai, Erich F. Haratsch, Onur Mutlu, **“Improving 3D NAND Flash Memory Lifetime by Tolerating Early Retention Loss and Process Variation,”** *Proc. ACM Meas. Anal. Comput. Syst.* 2(3), Article 37, 2018, DOI `10.1145/3224432`, arXiv `1807.05140v2`: <https://arxiv.org/abs/1807.05140>.
2. Bongsik Choi et al., **“Comprehensive evaluation of early retention (fast charge loss within a few seconds) characteristics in tube-type 3-D NAND Flash Memory,”** VLSI Technology 2016, DOI `10.1109/VLSIT.2016.7573385`.
3. C.-P. Chen et al., **“Study of fast initial charge loss and its impact on the programmed states Vt distribution of charge-trapping NAND flash,”** IEDM 2010, DOI `10.1109/IEDM.2010.5703304`.
4. **“Reliability of NAND Flash Memories: Planar Cells and Emerging Issues in 3D Devices,”** *Computers* 6(2):16, 2017, DOI `10.3390/computers6020016`, used for secondary chronology/cross-check only.
