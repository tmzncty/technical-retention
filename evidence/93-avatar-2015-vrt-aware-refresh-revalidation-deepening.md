# Evidence deepening — AVATAR 2015: runtime requalification of DRAM retention metadata

## Purpose

This addendum deepens [`../cases/93-dram-variable-retention-time-profile-staleness.md`](../cases/93-dram-variable-retention-time-profile-staleness.md) with one bounded later response to the profile-staleness problem already grounded there.

The question is not whether AVATAR is the history of adaptive DRAM refresh, nor whether it was deployed in commodity systems. The narrow question is:

> **Once a retention-time profile can become unsafe at runtime because of variable retention time (VRT), what retained control state and evidence-generating work can be used to revise the maintenance policy while the system is running?**

This record keeps four layers separate:

- **historical record:** what Qureshi et al. proposed and evaluated at DSN 2015;
- **engineering reconstruction:** what follows from the dependency between row classification, error evidence, and refresh rate;
- **functional analogy:** comparisons to scrubbing/currentness mechanisms elsewhere in the repository;
- **deployment boundary:** a peer-reviewed architecture proposal and measured DRAM characterization are not evidence of production deployment or JEDEC adoption.

---

## Primary source

**Moinuddin K. Qureshi, Dae-Hyun Kim, Samira Khan, Prashant J. Nair, Onur Mutlu, “AVATAR: A Variable-Retention-Time (VRT) Aware Refresh for DRAM Systems,” IEEE/IFIP International Conference on Dependable Systems and Networks (DSN), 2015, pp. 427–437, DOI `10.1109/DSN.2015.58`.**

Author/institution-hosted full paper:

- <https://memlab.ece.gatech.edu/papers/DSN_2015_1.pdf>

Bibliographic cross-check:

- <https://dblp.org/rec/conf/dsn/QureshiKKNM15>

### Evidence role

`H/P` — original peer-reviewed systems research. It is a primary source for the proposed architecture, its experimental characterization inputs, and its simulation/reliability evaluation. It is **not** a product manual, standard, or field-deployment report.

---

## Exact anchors and bounded claims

### §II-C–D — refresh-rate classification is retained control state

AVATAR describes multirate refresh as an initial retention test followed by a per-row **Refresh Rate Table (RRT)** that determines whether a row receives Fast or Slow Refresh. For the configuration studied, the paper uses one RRT bit per row.

The paper also explicitly discusses storing the RRT in a reserved DRAM region rather than SRAM and, in that design alternative, triplicating the RRT to tolerate VRT-related errors in the RRT itself.

Use this to support:

```text
payload bits
    ≠ refresh-classification bits
    ≠ evidence that the classification is still safe
```

and:

```text
control metadata can itself require protection
```

Do **not** generalize the one-bit RRT, DRAM placement, or triplication choice to all retention-aware refresh designs.

### §II-D / §III — static multirate classification is challenged by runtime VRT

The paper states the key assumption of ordinary multirate refresh explicitly: the retention-time profile does not change at runtime. VRT violates that assumption because the same cell can move between higher- and lower-retention states unpredictably.

This is consistent with the earlier Case-93 evidence from 1987–2013, but the 2015 paper is useful because it makes the failed assumption part of an explicit maintenance-policy design problem.

Use this to support:

- `profile bits intact ≠ profile semantics still conservative`;
- `row address stable ≠ maintenance class stable`.

### §VI-A — ECC correction becomes a trigger for refresh-class update

AVATAR combines multirate refresh with ECC. When an ECC correction is observed, the proposal **upgrades the containing row to Fast Refresh**. The historical mechanism is therefore not merely “ECC repairs a bit.” Error evidence is also reused to modify future maintenance policy.

The paper notes an important diagnostic limit: an ECC correction can also be caused by a soft error. AVATAR nevertheless conservatively upgrades the row, arguing from the relative error rates in its model/measurements rather than from perfect cause identification.

Use this to support:

```text
error corrected
    ≠ cause uniquely diagnosed
```

and:

```text
repair evidence
    -> policy reclassification
    -> changed future refresh work
```

Do not redescribe every corrected error as proven VRT.

### §VI-A / Figure 13 — proactive scrub supplies observation coverage

The paper points out that ECC is normally checked when data is accessed; cold regions could therefore accumulate VRT-related errors without being observed. AVATAR adds a proactive memory scrub that periodically checks memory and upgrades a row whenever correction exposes an error.

The evaluation uses a 15-minute scrub interval. That number is an evaluated design parameter, **not** a DRAM standard, universal safe interval, or production requirement.

Use this to support:

- `error-detection capability ≠ error-observation coverage`;
- `scrub ≠ refresh`;
- `proactive evidence generation can be part of retention maintenance`.

### §VI-A / §VI-E — classification can move in both directions

Rows migrate conservatively toward Fast Refresh when runtime error evidence appears. The paper also proposes infrequent retention testing — illustrated as approximately yearly in the evaluated policy — so rows no longer exhibiting VRT can be downgraded back to Slow Refresh.

The RRT is therefore not merely a durable profile loaded once. In AVATAR it is a **mutable maintenance classification** whose authority is refreshed by different evidence paths:

```text
initial retention test
    -> Slow/Fast classification

runtime ECC/scrub evidence
    -> upgrade to Fast Refresh

later retention retest
    -> possible downgrade to Slow Refresh
```

Use this to support:

- `reclassification ≠ payload rewrite`;
- `maintenance metadata persistence ≠ maintenance metadata immutability`;
- `conservative upgrade authority ≠ symmetric downgrade authority`.

The asymmetry matters: an observed correction triggers immediate conservative upgrade, while relaxation of the maintenance burden is tied to a separate retest.

### §VI-F — observation frequency is itself a reliability/overhead parameter

The paper explicitly analyzes scrub interval as a trade-off: more frequent scrub reduces the time newly active VRT cells remain undiscovered but consumes read bandwidth and energy. The specific overhead values are evaluation-specific.

Use this to support the engineering relation:

```text
physical VRT transition
    -> latent unsafe classification
    -> observation delay
    -> correction/reclassification
```

The interval between the physical change and its observation is therefore a separate maintenance timescale from the ordinary DRAM refresh interval.

---

## Engineering reconstruction

### E — profile staleness can be repaired without reconstructing payload identity

AVATAR does not need a new row address when a row becomes unsafe at the slow rate. It changes the retained relation:

```text
row identity -> refresh class
```

The physical row and logical designation can remain stable while the maintenance rule changes.

### E — preserved metadata may need a validity-maintenance loop

Case 93 already established that a perfectly preserved retention profile can become stale. AVATAR supplies a concrete research design in which the response is not “store the profile more durably,” but:

- generate new runtime evidence;
- revise the classification;
- conservatively increase maintenance;
- later require separate evidence before reducing maintenance again.

Thus:

```text
metadata durability ≠ metadata validity
```

and:

```text
validity maintenance can require its own observation schedule
```

### E — an error-correcting mechanism can become a policy sensor

ECC has at least two roles in this bounded proposal:

1. correct the immediately observed erroneous word within the assumed code capability;
2. produce an event that causes future refresh policy for the containing row to change.

This does not make ECC a VRT detector in the strict causal-diagnostic sense. The paper itself notes soft-error ambiguity.

### E — proactive scan and refresh have different maintenance semantics

Refresh restores charge before the presumed retention deadline. Scrub reads/checks state in order to expose errors that may revise the deadline classification. They are both maintenance work, but their triggers, evidence roles, and effects differ.

### E — optimization can create second-order state that must survive the same medium it controls

In the paper's DRAM-resident RRT alternative, the refresh policy metadata is stored in DRAM and may be triplicated to protect it. The control state that decides how aggressively DRAM is maintained can itself depend on DRAM retention and error protection.

This is a bounded architecture option, not a universal recursive property of memory controllers.

---

## Functional comparisons and stop conditions

### Case 18 / Synthesis 08 — proactive integrity checking

AVATAR scrub and ZFS/device scrubbing can both be compared as **proactive evidence generation before ordinary demand exposes a problem**.

Stop condition:

- DRAM scrub here discovers correctable retention failures and feeds row refresh classification;
- storage scrub validates blocks/checksums/redundancy and may repair from alternate embodiments.

They do not share a physical mechanism or historical genealogy.

### Case 90 / Synthesis 16 — currentness/admissibility metadata

A refresh class and a leader-epoch/currentness record can both remain physically present while the relation they represent becomes unsafe or inadmissible.

Stop condition: DRAM RRT state is maintenance-policy metadata for one physical memory array; replicated-log lineage is protocol authority/currentness evidence. They are not instances of one historical metadata technology.

---

## Anti-overclaim ledger

Do not claim:

- AVATAR was deployed in commodity DRAM controllers;
- AVATAR is a JEDEC requirement;
- AVATAR invented VRT, retention-aware refresh, ECC scrubbing, or multirate refresh;
- every ECC correction proves VRT;
- a 15-minute scrub interval or yearly retest is universally correct;
- RRT triplication is required by all adaptive refresh schemes;
- a corrected error means the original profile is globally wrong;
- runtime upgrade of a row proves the underlying VRT state will remain permanently low;
- adaptive refresh removes ordinary refresh or eliminates maintenance.

The broader architecture, standards, product, and manufacturing genealogy belongs primarily in `tmzncty/computing-archaeology` if developed. This addendum retains only the relation needed by `technical-retention`: **a retained preservation prescription can be revised by newly generated evidence, and the work required to keep the prescription valid is distinct from the work it schedules.**

---

## Claim ledger

| Claim | Label | Source basis | Boundary |
| --- | --- | --- | --- |
| AVATAR uses a per-row RRT to select Fast/Slow Refresh | `H/P` | DSN 2015 §II-C | proposal/evaluation, not deployment |
| the paper discusses storing RRT in reserved DRAM and triplicating it | `H/P` | DSN 2015 §II-C footnote | design option, not universal implementation |
| runtime VRT invalidates the static-profile assumption | `H/P` | DSN 2015 §II-D / §III | bounded to VRT/multirate-refresh problem |
| AVATAR upgrades a row to Fast Refresh after ECC correction | `H/P` | DSN 2015 §VI-A | correction is not perfect causal diagnosis |
| proactive scrub is added to expose failures in low-activity memory | `H/P` | DSN 2015 §VI-A | 15-minute interval is evaluation-specific |
| separate retention testing can later downgrade rows | `H/P` | DSN 2015 §VI-A / §VI-E | yearly example is proposal/evaluation-specific |
| observation coverage is distinct from having ECC capability | `E` | §VI-A access-vs-scrub distinction | project formulation |
| maintenance classification can be mutable while row identity stays stable | `E` | RRT upgrade/downgrade path | project formulation |
| metadata durability is distinct from metadata validity | `E` | Case 93 + AVATAR response | project formulation |
| ECC can supply both immediate correction and a policy-update event | `E` | §VI-A | does not imply unique VRT diagnosis |
| scrub and refresh are different maintenance operations | `E/A` | §VI-A plus DRAM refresh mechanism | no genealogy claim |

---

## Related-repository check

A fresh search of `tmzncty/computing-archaeology` for `variable retention time`, `VRT`, `RAIDR`, and `AVATAR` found no dedicated treatment to reuse in this pass. If a broader DRAM refresh-optimization genealogy is later written there, this addendum should link to it rather than duplicate the history.