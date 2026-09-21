# Synthesis 29 deepening — maintenance-history loss, future control, and distinguishability

Status: **bounded cross-case deepening complete**

Parent synthesis: [`../docs/SYNTHESIS_29_MAINTENANCE_OBSERVABILITY_COVERAGE_ACCOUNTING.md`](../docs/SYNTHESIS_29_MAINTENANCE_OBSERVABILITY_COVERAGE_ACCOUNTING.md)

Grounded anchors:

- [`Case 38 — Intel DC S3700 PLI self-test validation`](../cases/38-intel-dc-s3700-pli-self-test-validation.md), especially [`38-2014-2015-pli-smart-counter-saturation-observability-deepening.md`](38-2014-2015-pli-smart-counter-saturation-observability-deepening.md);
- [`Case 83 — Apache HDFS BlockScanner`](../cases/83-apache-hdfs-block-scanner-checksum-verification.md), especially [`83-hadoop-2012-verification-log-rollover-rescan-cadence-deepening.md`](83-hadoop-2012-verification-log-rollover-rescan-cadence-deepening.md).

This note closes a narrow part of Synthesis 29's remaining work on **telemetry/history loss**. It does not replace Synthesis 29, Synthesis 26, or Synthesis 30, and it does not change either case's canonical maturity beyond **`grounded`**.

---

## 1. Bounded question

Maintenance systems often retain some trace of earlier work:

- a cumulative count;
- a recency field;
- a pass/fail result;
- a verification timestamp;
- a cursor;
- an event log;
- a completion record.

A loose account calls all of these `maintenance history` and then asks whether the history is retained.

The two grounded cases here show why that question is too coarse.

The narrower question is:

> When distinctions among past maintenance events disappear, does the loss merely weaken later observation, or does it also change which future maintenance action the system is entitled to perform?

The answer is not uniform.

```text
loss of historical distinguishability
    can weaken observation only

or

loss of historical distinguishability
    can change future maintenance eligibility
```

The difference depends on what consumes the retained record later.

---

## 2. Claim discipline

This packet follows [`../docs/METHOD.md`](../docs/METHOD.md) and [`../AGENTS.md`](../AGENTS.md).

### Historical record

Historical claims below remain source-specific:

- Intel documents the S3700 AFh fields, their saturation behavior, and the exclusion of power-cycle tests from one counter;
- Apache HDFS-3828 documents premature `verificationLogs` rollover, loss of earlier verification times, pathological rescanning, and the accepted period-level guard.

### Engineering reconstruction

The terms below are project vocabulary:

- `historical distinguishability`;
- `representational collapse`;
- `decision-bearing maintenance history`;
- `decision horizon`;
- `observational history` versus `prospective control history`.

They are not attributed to Intel or Apache.

### Functional analogy

Case 38 and Case 83 are compared only because both retain maintenance-derived evidence whose information content can later shrink.

This comparison does **not** imply:

- shared implementation;
- shared storage format;
- common standards ancestry;
- direct technical genealogy;
- identical correctness consequences.

### Philosophical interpretation

A final interpretive section asks what it means for a technical system to retain only the past distinctions it still needs. It is explicitly downstream of the engineering evidence and does not turn controller telemetry into human memory, testimony, or archival history.

---

## 3. Primary-source custody inherited from the cases

### 3.1 Intel DC S3700

The Case 38 packet uses two Intel-origin primary documents:

1. Intel, *Power Loss Imminent (PLI) Technology Brief* (2014), currently hosted by Solidigm:
   - <https://www.solidigm.com/content/dam/solidigm/en/site/products/technology/power-loss-imminent-technology-brief/Power-Loss-Imminent-Technology-Brief.pdf>
2. Intel, *Intel Solid-State Drive DC S3700 Series Product Specification*, January 2015, document 328171-010US:
   - <https://www.intel.com/content/dam/www/public/us/en/documents/product-specifications/ssd-dc-s3700-spec.pdf>

The product specification documents SMART attribute `AFh` / decimal 175 with separate fields for:

- power-loss event count;
- minutes since last test;
- lifetime number of tests;
- pass/fail result.

The minutes-since-last-test and lifetime-test fields are finite and saturating. Intel also states that the lifetime-test counter does not increment for a power-cycle test.

### 3.2 Apache HDFS

The Case 83 packet uses Apache's primary issue and patch record:

1. HDFS-3194, `DataNode block scanner is running too frequently`:
   - <https://issues.apache.org/jira/browse/HDFS-3194>
2. HDFS-3828, `Block Scanner rescans blocks too frequently`:
   - <https://issues.apache.org/jira/browse/HDFS-3828>
3. final reviewed patch `hdfs-3828-3.txt`:
   - <https://issues.apache.org/jira/secure/attachment/12543965/hdfs-3828-3.txt>

HDFS-3828 records that repeated calls rolled `verificationLogs` too aggressively. After two iterations, earlier block verification times had been lost, allowing a recently and successfully verified block to become eligible for another scan on a seconds-scale cadence rather than the intended long scan period.

The accepted patch adds a current-period work guard and a regression test that repeatedly wakes the scanner while requiring the block to be scanned only once during the relevant period.

---

## 4. Historical record A — Case 38 preserves a bounded projection, not an exact event history

Intel's AFh layout already separates several propositions:

```text
power-loss events
    !=
self-test recency
    !=
counted self-test total
    !=
latest represented test result
```

Two fields have explicit finite ceilings.

For the 16-bit recency field:

```text
65,535 minutes since last represented test
70,000 minutes since last represented test
100,000 minutes since last represented test

    -> same saturated field value
```

assuming no intervening update changes the observation.

Likewise, once the lifetime-test count saturates, larger exact counts cease to be distinguishable through that field.

This is a documented interface property. It does not require an inference about hidden firmware internals.

Intel additionally excludes a power-cycle test from the lifetime-test count. Therefore two histories can differ even before saturation while mapping to the same lifetime-test value if their difference lies only in that excluded event class.

Historical result:

```text
AFh retained
    !=
exact maintenance-event history retained
```

and:

```text
field named "lifetime"
    !=
lossless count of every PLI test-like event
```

---

## 5. Historical record B — Case 83 shows that recent verification history can be scheduling state

HDFS-3828 supplies a different kind of loss.

The issue does not merely say that an operator-facing log became less informative. It identifies a scanner path in which prior verification times were used to avoid rescanning blocks that had already been covered recently.

The failure sequence was approximately:

```text
successful verification
    -> verification time recorded
    -> scanner invoked again
    -> verification logs rolled too early
    -> earlier verification time no longer available to scheduling logic
    -> block treated as eligible again
    -> redundant scan occurs
```

The block's payload did not have to become corrupt for this to be a retention bug.

What disappeared was evidence that a maintenance obligation had **already been satisfied recently enough** for scheduling purposes.

Historical result:

```text
verification history
    was not only retrospective evidence
    but also an input to later eligibility
```

and:

```text
successful verification at t1
    !=
scheduler at t2 can still establish "not due"
```

if the completion evidence is discarded prematurely.

---

## 6. Engineering reconstruction — two different loss shapes

The cases support a useful distinction between at least two ways maintenance history can lose information.

### 6.1 Representational collapse

Case 38 is the clean example.

A finite field maps multiple distinct underlying histories to the same visible representation.

```text
H1 != H2 != H3

but

O(H1) = O(H2) = O(H3)
```

This can happen because of:

- numeric saturation;
- event-class omission.

The safe consequence is loss of exact distinguishability through that interface.

It does **not** follow that the underlying maintenance stopped or failed.

### 6.2 Premature deletion / rollover

Case 83 is different.

The relevant evidence was discarded before the later consumer had finished needing it.

```text
record exists
    -> future eligibility decision can suppress redundant work

record removed too early
    -> future eligibility decision changes
```

This is stronger than observational ambiguity because the missing past distinction feeds back into future action.

### 6.3 The categories are functional, not exhaustive

Other loss modes remain possible:

- reset to a default or zero state;
- counter wraparound;
- torn or partially persisted accounting state;
- stale but still present records;
- schema/interpretation loss;
- truncation by bounded event-log capacity.

This packet does not claim to have grounded those modes merely by naming them.

---

## 7. Observational history versus decision-bearing history

The two cases motivate a project-level distinction.

### Observational maintenance history

A retained record can support later statements about what probably or definitely happened, within its documented semantics.

Examples include:

- a cumulative event count;
- a pass/fail result;
- a recency field;
- a bounded event log.

Its loss may reduce diagnosability or historical precision without necessarily changing device behavior.

### Decision-bearing maintenance history

A retained record becomes decision-bearing when later control logic consumes it to determine whether work is due, admissible, suppressible, resumable, or complete.

Case 83 directly grounds one such relation:

```text
recent verification-time evidence
    -> future "not yet due" decision
```

The important warning is therefore:

> A record can look like telemetry or history while also functioning as control state.

The labels `log`, `counter`, `history`, and `telemetry` do not by themselves establish whether the record is merely observational or is consumed by future control.

---

## 8. A decision horizon, not an infinite retention requirement

Case 83 does **not** imply that every verification timestamp must be retained forever.

The scheduling relation needs enough information to survive for the interval during which the prior completion still changes future eligibility.

Call that bounded interval the **decision horizon**.

Project reconstruction:

```text
history distinction D
    must survive
    while future decision F still depends on D
```

After that horizon expires, the same exact distinction may become dispensable for the scheduler even though it might remain useful for audit or diagnosis.

This gives a more precise rule than `keep maintenance history`:

> Retain each distinction at least as long as the strongest future claim or control decision that still consumes it requires.

This is compatible with Synthesis 26's persistence-horizon analysis but is not identical to it. Synthesis 26 asks how maintenance-control state survives interruption; the present note asks **which historical distinctions need to remain available to a later decision at all**.

---

## 9. Information loss does not have one operational direction

A common intuition is:

```text
maintenance state lost
    -> maintenance omitted
```

Case 83 is a direct counterexample.

Loss of recent-completion evidence caused **too much** maintenance rather than too little.

Thus the more general relation is:

```text
maintenance-history/control distinction lost
    -> under-maintenance
    or over-maintenance
    or duplicated maintenance
    or changed observability only
```

Which branch occurs depends on the semantics of the missing distinction.

For a scheduler where a record means `already covered`, losing it can create duplicate work.

For a scheduler where a record means `still outstanding`, losing it could instead suppress work.

The second branch is a logical possibility, not something Case 83 itself demonstrates. The grounded result here is only the over-scan path.

---

## 10. Functional comparison table

| Axis | Case 38 — S3700 AFh | Case 83 — HDFS verification logs |
| --- | --- | --- |
| Historical object | SMART maintenance/event fields | block verification-time records |
| Primary producer | SSD firmware/interface implementation | HDFS DataNode scanner implementation |
| Represented past | PLI event/test count, recency, result | recent block verification completion times |
| Loss shape grounded | saturation + event-class omission | premature log rollover/deletion |
| Does distinct history collapse? | yes | yes, by removing earlier records |
| Directly documented effect | exact larger count/age no longer distinguishable; one event class omitted from count | recently verified block can be rescanned far too soon |
| Future-control role established? | not by the AFh evidence packet | yes, verification history participates in scheduling eligibility |
| Payload loss demonstrated? | no | no |
| Maintenance cessation demonstrated? | no | no |
| Shared implementation/genealogy? | **not claimed** | **not claimed** |

The comparison is deliberately asymmetric. That asymmetry is the result.

The fact that both are `maintenance history` does not imply that losing them has the same consequence.

---

## 11. Relation to Synthesis 29, 26, and 30

### 11.1 Synthesis 29 — observability semantics

Synthesis 29 establishes:

```text
maintenance accounting
    !=
maintenance closure
```

and asks what proposition an observable supports.

This deepening adds:

```text
observable/history representation retained
    !=
all distinctions in the underlying maintenance history retained
```

and, from HDFS:

```text
observable/history record
    can also be
future control input
```

This closes only part of Synthesis 29's open debt on telemetry loss/reset/wrap/saturation counterexamples: **saturation** and **premature rollover** now have grounded examples. Reset and wrap remain open.

### 11.2 Synthesis 26 — persistence horizons

Synthesis 26 distinguishes several maintenance-control-state horizons and reconstitution strategies.

This packet contributes a complementary rule:

```text
persistence horizon
    should be derived from
future decisions that still require the distinction
```

It does not say every history record is a checkpoint.

### 11.3 Synthesis 30 — coverage/completion evidence

Synthesis 30 distinguishes local work, traversal progress, domain completion, and completion evidence.

Case 83 adds a temporal afterlife to completion evidence:

```text
completion evidence produced
    !=
completion evidence retained long enough
for the next eligibility decision
```

A completed maintenance action can be correct, yet the system can still mis-schedule later work if the evidence of that completion expires too early.

---

## 12. Counterexample ledger for this slice

| Candidate claim | Result | Reason |
| --- | --- | --- |
| If maintenance telemetry remains readable, exact maintenance history remains recoverable. | **rejected** | S3700 AFh saturation and event-class omission |
| A `lifetime` counter counts every related event forever. | **rejected** | Intel excludes power-cycle tests and documents saturation |
| Counter saturation means the maintenance mechanism stopped. | **rejected** | only the representation's ceiling is documented |
| A successful maintenance action is enough to prevent immediate repetition. | **rejected** | HDFS-3828 lost recent completion evidence and rescanned |
| Losing maintenance history can only cause missed maintenance. | **rejected** | HDFS-3828 demonstrates redundant over-maintenance |
| A history/log record is necessarily retrospective only. | **rejected** | HDFS verification history feeds future scheduling eligibility |
| Every maintenance history record must be kept forever. | **rejected** | the grounded need is bounded by the future decision horizon |
| A cumulative scalar count is equivalent to an event log. | **rejected** | target identity/order/event inclusion can be lost |
| Case 38 and Case 83 share one implementation model. | **rejected** | functional comparison only |
| Less historical detail always means weaker runtime correctness. | **rejected** | Case 38 establishes bounded observability loss without demonstrating runtime failure |

---

## 13. Explicit non-claims

This packet does **not** claim that:

1. Intel AFh controls the PLI self-test scheduler;
2. an AFh saturated field causes a PLI test to be skipped;
3. AFh is a lossless event log;
4. all PLI test-like events increment the lifetime-test count;
5. a power-cycle test is equivalent to a periodic capacitor test;
6. the S3700 stopped testing after 65,535 counted tests;
7. the S3700 stopped updating pass/fail state after counter saturation;
8. AFh reset/power-cycle persistence semantics are established by this packet;
9. HDFS `verificationLogs` are immutable audit records;
10. HDFS-3828 caused user payload corruption;
11. repeated HDFS scanning is equivalent to missing HDFS scanning;
12. HDFS `verificationLogs` and later `VolumeScanner` cursors are the same state;
13. HDFS must retain every verification timestamp indefinitely;
14. every maintenance counter is consumed by scheduling logic;
15. every maintenance log is correctness-critical;
16. every loss of historical detail changes runtime behavior;
17. every maintenance-control bug can be described as history loss;
18. saturation, wrap, reset, rollover, truncation, and staleness are interchangeable mechanisms;
19. a diagnostic history is useless if it is not operational control state;
20. a decision-bearing history is therefore an archive in the cultural or institutional sense;
21. Intel and Apache share a technical lineage;
22. SMART telemetry and HDFS logs have comparable physical persistence mechanisms;
23. a bounded decision horizon can be inferred without inspecting the specific consumer logic;
24. the absence of exact event history implies the absence of adequate maintenance assurance;
25. successful scheduling implies full target coverage;
26. successful coverage implies timeless health;
27. the word `history` has one stable technical meaning across storage systems;
28. the project terms introduced here were used by the historical actors;
29. the two cases exhaust the possible ways maintenance history can lose information;
30. this cross-case deepening promotes Case 38 or Case 83 beyond `grounded`.

---

## 14. Philosophical interpretation — a selectively operative past

A narrow interpretation survives the mechanism-first comparison:

> A technical system does not need to preserve every distinction in its past. It needs to preserve the distinctions that remain operative for later interpretation, control, recovery, or accountability.

Case 38 shows a past deliberately compressed into finite counters and bounded recency/result fields. Distinct histories can become operationally indistinguishable at the interface.

Case 83 shows the opposite pressure: one apparently mundane historical distinction — *this block was already verified recently* — must remain available long enough because it changes what the system should do next.

The useful conceptual point is therefore not that `the machine remembers` in a generic sense. It is that:

```text
past distinctions
    have different technical afterlives
```

Some are retained only for observation. Some are consumed by future control. Some can safely collapse after a bounded horizon. Others cannot collapse yet without changing behavior.

The interpretation stops there. Nothing in these cases by itself establishes a theory of human memory, historiography, testimony, or archival value.

---

## 15. Related-repository reuse status

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for the combined HDFS `DataBlockScanner` / `verificationLogs` and Intel S3700 AFh / counter-saturation seam found no dedicated packet to reuse.

Broader histories of:

- ATA SMART/SCT telemetry;
- SSD power-loss-protection product evolution;
- Hadoop DataNode scanner evolution;
- maintenance-log and health-telemetry genealogy;

belong primarily in `computing-archaeology` if pursued. This packet keeps only the retention-specific cross-case relation.

---

## 16. Remaining bounded work

High-value follow-ons are deliberately narrower than another generic maintenance synthesis:

1. ground a named **counter wraparound** case where wrap changes operator or controller inference;
2. ground a named **reset/clear** case where maintenance accounting disappears while payload and mechanism remain intact;
3. obtain S3700-specific AFh reset/power-cycle semantics or controlled hardware observations;
4. perform HDFS restart/fault observation to separate process restart, DataNode restart, log rollover, and persisted verification-history lifetime;
5. find a case where loss of outstanding-work evidence produces **under-maintenance**, complementing HDFS-3828's over-maintenance counterexample;
6. distinguish operator-facing diagnostic retention requirements from controller-facing decision horizons when one record serves both roles.

These remain separate tasks. The present bounded result is complete without them.
