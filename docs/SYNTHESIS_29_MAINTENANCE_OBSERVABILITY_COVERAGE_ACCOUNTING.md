# Synthesis 29 — Maintenance Observability: Schedule, Admission, Coverage, Accounting, and Closure

> **Question:** when a retention-maintenance mechanism exposes configuration, status, progress, counters, or completion events, what is an observer actually entitled to infer about the work that was due, admitted, executed, covered, completed, repaired, or revalidated?

**Status:** bounded cross-case engineering synthesis over already-grounded cases. It adds no invention-priority claim and no historical genealogy among DRAM refresh, HDFS block scanning, RAID-controller Patrol Read, NAND/SSD refresh accounting, or e.MMC background maintenance. Historical claims remain in the individual case and evidence records.

Grounded anchors used here:

- [`Case 09 — DRAM CBR refresh-address internalization`](../cases/09-dram-cbr-refresh-address-internalization.md), especially [`09-ti-cbr-refresh-address-grounding`](../evidence/09-ti-cbr-refresh-address-grounding.md) and [`09-dram-refresh-counter-initialization-test-deepening`](../evidence/09-dram-refresh-counter-initialization-test-deepening.md) — a refresh deadline/coverage contract can remain external while row enumeration becomes chip-local; counter phase and refresh-command cadence are different state;
- [`Case 83 — HDFS BlockScanner`](../cases/83-apache-hdfs-block-scanner-checksum-verification.md), especially [`83-hadoop-270-271-blockscanner-default-enable-regression-deepening`](../evidence/83-hadoop-270-271-blockscanner-default-enable-regression-deepening.md) and [`83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening`](../evidence/83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md) — implementation availability, effective configuration, traversal progress, successful verification, and distributed repair are not one state;
- [`Case 102 — Dell PERC / LSI MegaRAID Patrol Read`](../cases/102-perc-megaraid-patrol-read-consistency-boundary.md), especially [`102-lsi-2007-patrol-read-scheduling-observability-deepening`](../evidence/102-lsi-2007-patrol-read-scheduling-observability-deepening.md) — schedule, start admission, continued execution, event-log progress, media-error outcome, and parity-consistency checking remain distinct;
- [`Case 67 — SK hynix / Samsung / OCP read-reclaim and refresh telemetry`](../cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md), especially [`67-2020-2025-ocp-refresh-count-semantics-deepening`](../evidence/67-2020-2025-ocp-refresh-count-semantics-deepening.md) — standardized integrity-maintenance reallocation accounting does not thereby become whole-device background-refresh coverage state;
- [`Case 135 — Micron automotive eMMC self refresh / BKOPS`](../cases/135-micron-emmc-self-refresh-time-trigger-maintenance.md), especially [`135-micron-emmc-2021-2023-self-refresh-grounding`](../evidence/135-micron-emmc-2021-2023-self-refresh-grounding.md) and [`135-jedec-emmc51-bkops-maintenance-opportunity-deepening`](../evidence/135-jedec-emmc51-bkops-maintenance-opportunity-deepening.md) — elapsed-time eligibility, idle opportunity, current progress, outstanding work, completion/history telemetry, and standardized background-operation urgency are different relations.

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Patrol Read`, `BlockScanner`, `Refresh Counts`, and `BKOPS` found no dedicated cross-mechanism packet to reuse. Broader histories of RAID-controller patrol scanning, HDFS scanner evolution, OCP SSD telemetry, eMMC background operations, and DRAM refresh-control genealogy remain appropriate work for that repository. The present document keeps only the cross-case retention-specific distinction among **maintenance observables and the claims they can support**.

---

## 1. Verdict

The grounded cases reject a single maintenance state called `enabled`, `running`, `healthy`, `refreshed`, or `complete`.

A useful cross-case decomposition is:

```text
maintenance obligation / due condition
    !=
policy or configured cadence
    !=
admission / execution opportunity
    !=
execution now occurring
    !=
coverage / progress over the intended target set
    !=
maintenance-event accounting
    !=
operation-completion claim
    !=
repair / redundancy-restoration outcome
    !=
later revalidation / renewed confidence
```

Not every mechanism exposes every layer, and the sequence is not universally chronological. A counter can increase while a whole-device coverage obligation is still behind; an operation can be scheduled but never admitted; progress can be known without proving repair; a pass can complete without creating a timeless health certificate; and a maintenance implementation can exist in source while effective configuration disables it.

The central rule is therefore:

> **A maintenance-facing observable is evidence for a bounded proposition, not a generic certificate that “maintenance happened correctly.”**

For every status bit, counter, progress record, event, or completion message, ask:

1. **what proposition does it assert or summarize?**
2. **what target set and time interval does that proposition cover?**
3. **what mechanism produced it?**
4. **what reset/persistence semantics does it have?**
5. **what stronger conclusion is still not justified?**

---

## 2. Claim discipline

This synthesis follows [`METHOD.md`](METHOD.md) and [`../AGENTS.md`](../AGENTS.md).

- **H/P — historical / primary:** release-specific defaults, command semantics, product fields, event names, timing values, and standards wording remain sourced in the individual cases/evidence packets.
- **E — engineering reconstruction:** `maintenance observability`, `coverage evidence`, `accounting summary`, `closure claim`, and the decomposition below are project analytical terms.
- **A — functional analogy:** two mechanisms can expose similar progress or counters without sharing implementation, physical mechanism, or genealogy.
- **I — philosophical interpretation:** the final interpretation is limited to what technical evidence about preservation work can and cannot establish.

This document does **not** use the existence of a telemetry field to infer undisclosed firmware state machines, nor does it turn one vendor's `Refresh`, `Patrol`, `Scan`, or `BKOPS` vocabulary into universal historical categories.

---

## 3. Why this is not Synthesis 24, 26, 27, or Audit 06 again

[`Synthesis 24`](SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md) asks **what makes maintenance due** and already establishes the important chain `trigger != opportunity != progress != execution != completion`.

The present synthesis asks a narrower observer-facing question:

> **When one of those stages is exposed through configuration, status, telemetry, logs, or counters, what claim does the exposed state actually warrant?**

[`Synthesis 26`](SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md) asks **how long maintenance-control state must survive**, and distinguishes reinitialize, persist-and-resume, persist-and-validate, and discard-and-replay policies. The present synthesis instead asks **what the retained or visible state means as evidence about maintenance**.

[`Synthesis 27`](SYNTHESIS_27_RETENTION_POLICY_EVIDENCE_VALIDITY.md) asks whether an **input** to maintenance policy — a sensor, profile, proxy, or error observation — is sufficiently representative and current to trust. The present synthesis mainly concerns the **observable state around and after scheduling/execution**: enabled state, admission, progress, coverage, accounting, completion, repair outcome, and revalidation.

[`SYNTHESIS_AUDIT_06_MAINTENANCE_VISIBILITY.md`](SYNTHESIS_AUDIT_06_MAINTENANCE_VISIBILITY.md) asks **to whom maintenance is visible** and rejects a monotonic law that greater reliability means more hidden work. The present synthesis is orthogonal: even after an observer can see a maintenance surface, the semantics of that surface remain bounded.

Thus:

```text
visibility to an observer
    !=
semantic strength of the observable
```

and:

```text
control-state persistence horizon
    !=
evidentiary meaning of the control/telemetry state
```

---

## 4. Comparison axes for a maintenance observable

Before using a maintenance field or status as evidence, audit at least these dimensions:

| Axis | Question |
| --- | --- |
| **producer** | Controller, device, host daemon, distributed coordinator, operator configuration, event logger? |
| **object** | What work or target relation is being described? |
| **scope** | One row, block, volume, device, virtual drive, pass, queue, or lifetime? |
| **stage** | Policy, admission, execution, progress, accounting, completion, repair, revalidation? |
| **target-set semantics** | Does the state encode which objects were or remain to be covered? |
| **time semantics** | Current state, since-last-observation, one-pass state, cumulative count, lifetime-style summary? |
| **reset / persistence** | Volatile, restart-persistent, power-cycle-persistent, resettable, unspecified? |
| **granularity** | Scalar, cursor, per-target map, event log, range, queue length, completion timestamp? |
| **causal specificity** | Does the state identify why maintenance occurred, or only that some event was counted? |
| **closure strength** | Does it prove admission, execution, coverage, repair, or only a weaker predecessor? |
| **revalidation** | What later observation could invalidate or supersede the earlier result? |

A maintenance observable can be perfectly accurate for its own field semantics while still being insufficient for a stronger operational claim.

---

## 5. Case 09 — coverage contract is not the same thing as scheduling or row-enumeration state

The DRAM refresh-control case is a useful baseline because it starts from a physically simple obligation but already refuses a single `refresh state`.

The period product contract can require a specified number of row restorations inside a bounded interval. Later CAS-before-RAS designs can generate the refresh row internally while the external processor or memory controller still supplies recurring command cadence.

The bounded relation is:

```text
refresh deadline / coverage requirement
    !=
external recurrence schedule
    !=
on-chip next-row counter phase
    !=
one refresh command executed
    !=
all required rows serviced inside the interval
```

This matters for observability because seeing one part does not reveal all the others. An internal row counter can advance correctly while external cadence is insufficient; a controller can issue commands without proving full target coverage if row-selection/currentness state is wrong; and the existence of a nominal refresh period is not a historical log of which rows were actually serviced.

The case therefore supplies the first rule:

> **maintenance command count != maintenance target coverage unless the mechanism establishes that mapping.**

It also blocks a common telemetry shortcut:

> **scheduler configured != deadline satisfied.**

This is an engineering comparison. The historical sources do not present a modern generalized `coverage certificate` abstraction.

---

## 6. Case 83 — implementation, effective configuration, cursor progress, verification, and repair are different claims

HDFS gives the strongest software counterexample to `feature exists = maintenance is active`.

HDFS-8681 records that the 2.7.0 BlockScanner implementation could be present while the shipped interaction between a zero default and the `> 0` enable predicate left the scanner disabled by default. The 2.7.1 repair changed the default and compatibility semantics.

Therefore:

```text
scanner implementation present
    !=
effective configuration admits scanning
```

Even after admission, a configured three-week scan period is policy, not a proof that every block was actually verified inside that interval under arbitrary load and failures.

The saved block-iterator cursor adds a different observable. It can retain traversal progress across restart, but it is not an integrity verdict for blocks that have not yet been reached, and its own periodic-save path had a clock-domain defect in the bounded release history.

Thus:

```text
cursor exists
    !=
all intended blocks covered
    !=
all covered blocks currently good
```

A successful individual checksum scan provides stronger local evidence, while a qualifying failure can be reported to the NameNode for distributed repair. Yet even there:

```text
verification failure reported
    !=
replacement replica already created
```

and:

```text
successful earlier verification
    !=
timeless integrity certificate
```

Case 83 therefore supplies a software-specific warning that both **configured policy** and **retained progress** can be real states without being completion evidence.

---

## 7. Case 102 — schedule, start admission, continued execution, event status, and repair outcome are separable

The 2007 MegaRAID Version 2.0 evidence makes several maintenance stages visible at one controller interface.

Patrol Read exposes `Auto`, `Manual`, and `Disabled` modes, a nominal 7-day / 168-hour default, a continuous option, a task rate, and a delay between iterations. The manual also says Patrol Read starts only after an idle interval when no other background task is active, but may continue after admission while foreground I/O becomes heavy.

Therefore:

```text
configured schedule
    !=
start-admission condition
    !=
continued execution condition
```

and the nominal seven-day cadence is not a seven-day physical defect law.

The same interface exposes progress/status through event logging and command status, including separate event classes for corrected medium error, uncorrectable medium error, and bad-block puncture. This makes observability richer without collapsing the states:

```text
progress/status event
    !=
coverage complete
    !=
error corrected
    !=
redundancy restored
```

The separate Consistency Check path further shows that a complete Patrol Read of physical-drive sectors does not automatically establish parity/data consistency for a redundant virtual disk.

Thus:

> **coverage is always coverage of a specified target relation, not generic “health.”**

A physical-drive maintenance pass and a redundancy-consistency pass can both be complete while proving different propositions.

---

## 8. Case 67 — accounting counter is not coverage-control state or maintenance history

The OCP/Samsung material is the strongest counterexample to reading a cumulative counter as a maintenance-completion certificate.

OCP defines SMART-10 `Refresh Counts` as counting blocks reallocated to maintain data integrity, while excluding ordinary garbage-collection movement and, in later wording, wear-leveling relocation. That gives the field meaningful standardized accounting semantics.

But OCP separately requires background data refresh for powered-on retention, including whole-device coverage expectations. The inspected standard does not state that each background-refresh operation maps one-to-one to SMART-10, nor that SMART-10 itself is the state used to schedule or prove whole-device coverage.

Therefore:

```text
integrity-maintenance reallocation counted
    !=
background-refresh trigger state
    !=
whole-device coverage-control state
    !=
one complete background-refresh pass
```

Samsung's later product schema strengthens the warning by exposing distinct fields for:

- `Lifetime read Reclaim count`;
- `Patrol Read Reclaim Count`;
- OCP `Refresh Counts`.

Separate names and byte locations justify keeping the accounting categories distinct, but do not prove that their event sets are mutually exclusive.

The general rule is:

> **a cumulative maintenance counter can be semantically well-defined while still omitting target identity, trigger cause, event ordering, coverage gaps, repair margin, and current outstanding work.**

Accordingly:

```text
counter increased
    !=
maintenance debt is zero
```

and:

```text
counter did not increase
    !=
no maintenance-related work occurred
```

unless the specific interface contract establishes those stronger implications.

---

## 9. Case 135 — outstanding work, eligibility, opportunity, progress, and historical counters coexist

The bounded Micron/Armadillo eMMC path supplies a particularly useful multi-stage interface.

The documented sequence separates:

```text
reset opens control window
    -> host supplies time
    -> elapsed-time eligibility is evaluated
    -> bus idle supplies execution opportunity
    -> post-idle delay elapses
    -> self-refresh work may execute
    -> current progress / queue state can be observed
    -> completion/history statistics can remain afterward
```

The shipped integration also uses ECC-related selection, so work can be selective rather than a proof of unconditional whole-media rewrite.

The exposed telemetry includes current `Self Refresh progress of scan`, queue-related state, completion-related information, `Self Refresh Loop Count`, `Refresh Count`, and `Power Loss Counter`. These fields are not interchangeable:

```text
current progress
    !=
outstanding queue depth
    !=
completed-loop count
    !=
power-loss history
```

The standardized e.MMC BKOPS surface adds another orthogonal relation. `BKOPS_STATUS` reports background-work urgency; manual and automatic control fields govern when host/device authority can provide execution opportunity. An urgency/status value is not the completed work itself.

Therefore:

```text
work is needed
    !=
work is currently admissible
    !=
work is executing
    !=
work is complete
```

Case 135 is especially important because it demonstrates that a single managed device can expose several maintenance observables at once without any one field becoming a total state of retention health.

---

## 10. Cross-case observability matrix

| Observable class | Case 09 DRAM | Case 83 HDFS | Case 102 MegaRAID | Case 67 NAND/SSD | Case 135 eMMC | What it does **not** prove by itself |
| --- | --- | --- | --- | --- | --- | --- |
| **policy / configured cadence** | refresh-period/command responsibility | scan period / enable semantics | Auto/Manual/Disabled; delay; 7-day default | adaptive thresholds / background-refresh policy exist at different layers | RTC policy, Delay 1/2; BKOPS enable modes | that work was admitted or completed |
| **admission / opportunity** | controller/device arbitration | scanner thread/rate/load conditions | idle/no-other-background-task start condition | powered background-maintenance opportunity | bus idle; BKOPS service window | target coverage |
| **execution state** | refresh command / restore action | current scanner work | running Patrol Read | reclaim/refresh event may occur | current self-refresh/BKOPS work | full pass completion |
| **progress / coverage state** | row-counter phase only partially represents coverage | block iterator / cursor | logged task progress | exact whole-device coverage state not exposed by SMART-10 | scan progress / queue state | correctness of every target or repair closure |
| **event / outcome evidence** | bounded test/control behavior | success/failure report for a block | corrected/uncorrectable/puncture event classes | reclaim/refresh category counted | completion-related / power-loss state | timeless future health |
| **cumulative accounting** | not a full historical ledger | cursor is not event count | event log is not one scalar lifetime certificate | Lifetime reclaim / patrol reclaim / OCP Refresh Counts | Loop Count / Refresh Count | target identity, ordering, remaining debt |
| **repair / closure evidence** | deadline satisfaction requires bounded coverage relation | bad report precedes distributed repair | error discovery/correction and parity consistency separate | reallocation preserves data but does not prove background coverage closure | loop completion can coexist with later new work | later degradation cannot occur |

The matrix is functional comparison only. It does not assert shared implementation or vocabulary.

---

## 11. Six recurring inference errors

The cases support six reusable negative rules.

### 11.1 Configured does not mean effective

HDFS 2.7.0 is the direct counterexample: implementation and configuration schema existed while the default interaction disabled the scanner.

> **configuration surface != effective maintenance behavior**.

### 11.2 Scheduled does not mean admitted

MegaRAID can have a nominal Patrol Read schedule while start still waits for idle/no-other-background-task conditions. eMMC self refresh can be elapsed-time eligible while waiting for bus idleness.

> **due/scheduled != admitted**.

### 11.3 Running does not mean target coverage complete

Progress or current execution says that maintenance is in flight, not that the full target set has been covered.

> **execution != coverage closure**.

### 11.4 Coverage complete does not mean every stronger integrity relation is proven

Physical-drive Patrol Read does not prove RAID parity consistency. An HDFS scanner pass does not itself prove the distributed replication goal has already been restored after discovering corruption.

> **coverage of relation A != qualification of relation B**.

### 11.5 Counter increased does not mean debt cleared

OCP `Refresh Counts` records a bounded class of integrity-maintenance reallocations but is not specified as the whole-device background-refresh coverage state. eMMC loop/count telemetry similarly summarizes work without becoming a future-retention guarantee.

> **accounting != closure**.

### 11.6 Completion does not mean timeless health

A completed scan/pass/refresh establishes, at most, a bounded result under a target set, time, mechanism, and failure model. New defects, new writes, new disturbance, or later degradation can create fresh obligations.

> **maintenance completion != permanent correctness certificate**.

---

## 12. Accounting, progress, and history must remain distinct

Several cases make it tempting to call every retained maintenance record `history`. That is too strong.

A cursor can retain where a traversal should resume without recording each target already checked. A cumulative count can report how many qualifying events occurred without preserving their addresses or order. An event log can retain richer event classes while still being finite, resettable, incomplete, or scoped to one controller. A current progress field can disappear at completion while a lifetime-style count remains.

A useful decomposition is:

```text
current phase / status
    !=
progress coordinate
    !=
target-coverage map
    !=
event log
    !=
cumulative accounting summary
    !=
complete provenance/history
```

This extends Synthesis 26 without duplicating it. Synthesis 26 asks how long such state must survive; this synthesis asks what proposition each representation can support while it exists.

---

## 13. Closure is relation-specific

The strongest cross-case result is that `complete` must always be qualified by **what relation has closed**.

Examples:

```text
DRAM:
refresh-cycle completion
    != full deadline-window coverage unless all required rows are serviced

HDFS:
block verification completion
    != distributed replacement-replica completion

MegaRAID:
Patrol Read completion
    != Consistency Check completion

OCP SSD:
integrity reallocation event completed
    != whole-device background-refresh coverage proved complete

eMMC:
one self-refresh loop completed
    != no future retention-maintenance obligation remains
```

Therefore repository prose should prefer explicit forms such as:

- `scan pass complete over X target set`;
- `repair complete under Y redundancy relation`;
- `counter records Z event class`;
- `current progress reached end of this traversal`;

rather than an unqualified `maintenance complete` or `device refreshed`.

---

## 14. Controlled comparison with maintenance-policy evidence

Synthesis 27 concerns **evidence consumed to decide maintenance**. The present synthesis concerns **evidence exposed about maintenance state or outcome**. Some artifacts can participate in both directions, so the distinction is functional rather than ontological.

For example:

```text
ECC/error evidence
    -> may be consumed as an input that selects renewal

renewal counter / completion status
    -> may be exposed later as evidence that bounded work occurred
```

A controller can also feed an output back into future policy. That does not erase the analytical distinction:

> **evidence used to choose work != evidence used to report work**, even if one retained field later participates in both roles.

The audit questions differ:

- for policy evidence: **is the observation representative/current enough to trust?**
- for maintenance observability: **what completed/ongoing proposition does the status actually establish?**

---

## 15. Counterexample ledger

| Candidate claim | Result | Why |
| --- | --- | --- |
| If a maintenance feature exists, it is active. | **rejected** | HDFS 2.7.0 default-disable regression |
| If maintenance is scheduled every N time units, every target is necessarily covered every N time units. | **rejected** | scheduling/admission/load/coverage are separate; MegaRAID and HDFS give direct boundaries |
| A progress indicator is a completion certificate. | **rejected** | progress is an intermediate observable; target-set closure remains separate |
| A cumulative maintenance count proves whole-device coverage. | **rejected** | OCP SMART-10 accounting and background-refresh coverage are separately specified |
| A completed media scan proves RAID parity consistency. | **rejected** | MegaRAID Patrol Read and Consistency Check are distinct tasks/scopes |
| A bad-block/corruption report proves repair already succeeded. | **rejected** | HDFS reporting precedes distributed repair; MegaRAID event classes distinguish outcomes |
| A prior successful maintenance pass proves future health. | **rejected** | later degradation/work can create a new obligation |
| Different telemetry labels prove disjoint event sets. | **rejected** | Samsung/OCP schema distinguishes fields but does not establish event-set exclusivity |
| Maintenance observability is useless unless it is a complete history. | **rejected** | cursors, counters, status, and queue state can be operationally useful under bounded semantics |
| One universal `maintenance health` bit can replace the distinctions above. | **rejected** | the grounded cases require policy, admission, coverage, accounting, repair, and revalidation to remain separable |

---

## 16. Engineering reconstruction: an observability contract

For future cases, a maintenance-facing interface should be reconstructed as an **observability contract** rather than treated as self-explanatory telemetry.

A compact template is:

```text
observable O
    produced by P
    about target relation R
    over scope S
    during / after interval T
    with reset/persistence horizon H
    and update semantics U

O supports claim C
O does not establish stronger claim C+
revalidation path = V
```

For example, the OCP field can be represented without inventing firmware details:

```text
O = SMART-10 Refresh Counts
P = device implementation under OCP reporting contract
R = counted integrity-maintenance block reallocations
S = cumulative field scope defined by the standard/product schema
C = qualifying reallocations were accounted
C+ = whole-device refresh coverage is currently complete   [not established]
```

This template forces a source-bounded claim and makes missing semantics explicit rather than filling them from intuition.

---

## 17. Philosophical / media-theoretical limit

A narrow interpretation is defensible:

> **Technical persistence can depend not only on preservation work, but on retained and exposed claims about that work — claims whose scope is always narrower than the total history or future of the retained object.**

This matters because a system often acts on compressed evidence: a cursor, a counter, a status code, a completion event, or a queue depth. Such evidence can be sufficient for coordination without becoming a complete representation of everything that physically happened.

The interpretation must stop there. These controller and software observables are not automatically human memory, testimony, archival provenance, or epistemology. The project gains precision by first asking exactly what technical proposition a field supports and where that proposition ends.

---

## 18. Result for repository vocabulary

The repository should preserve the following distinctions in future case writing:

```text
maintenance policy / cadence
maintenance admission / opportunity
maintenance execution state
maintenance progress
maintenance target coverage
maintenance event/outcome evidence
maintenance accounting summary
maintenance completion / closure
repair / redundancy restoration
revalidation
```

Use `maintenance observability` only as an umbrella for interfaces or retained states that expose one or more of these relations. Do not use it as a synonym for monitoring, health, telemetry, or maintenance-control state in general.

The strongest portable rule is:

> **Name the proposition, target set, time scope, and closure level before treating maintenance telemetry as evidence.**

---

## 19. Remaining bounded work

This synthesis is complete for the current cross-case question, but several evidence-bearing follow-ons remain open:

1. **power-loss/reset semantics of cumulative maintenance counters** — especially named SSD/eMMC devices where `Lifetime`, `Refresh`, or reclaim counters are exposed but atomicity/reset behavior is undocumented;
2. **coverage certificates versus scalar counters** — find primary examples where a device explicitly reports a completed target-set pass rather than only progress or cumulative work;
3. **telemetry loss / wrap / reset counterexamples** — source or fault-injection evidence showing how operator inference fails when accounting state is reset, lost, or saturated;
4. **repair closure after proactive discovery** — deepen named systems where scan completion, repair completion, and later revalidation have separately inspectable states;
5. **standards vocabulary genealogy** — if pursued, route the history of `scrub`, `patrol`, `background scan`, `refresh`, `reclaim`, and health/accounting vocabulary primarily through `computing-archaeology`, while keeping the relation-level comparison here.

None of those are required to retain the present bounded result.
