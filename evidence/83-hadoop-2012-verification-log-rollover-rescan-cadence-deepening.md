# Case 83 evidence deepening — HDFS verification-log rollover and rescan cadence (2012)

Status: **bounded deepening complete**. This file deepens Case 83 without changing its canonical maturity (`grounded`).

## Scope

This slice asks a narrow question:

> In the 2012 HDFS `DataBlockScanner` / `BlockPoolSliceScanner`, what retained state prevented a recently verified block from being treated as due again, and what happened when that state was discarded too early?

It does **not** attempt a full history of HDFS block scanning, checksum formats, later `VolumeScanner` cursor semantics, or all release branches. Those remain in the Case 83 grounding and later evidence files.

The key result is historical and engineering-specific: in the HDFS-3828 failure, recently completed verification history was not merely retrospective telemetry. It was consumed by scanner scheduling logic. Premature rolling of the verification logs erased earlier verification times within the same scan period, so an otherwise successful scanner could repeatedly verify the same block every few seconds rather than at the configured long interval.

This produces a bounded retention relation:

```text
successful block verification
    -> verification-time evidence retained long enough for scheduling
    -> block remains recognized as already covered in the current period

successful block verification
    + premature verification-log rollover
    -> scheduler loses earlier completion evidence
    -> block may become eligible again far too soon
```

The historical actors did not use the project's philosophical vocabulary below. Terms such as "maintenance-completion evidence" and "retention horizon" are engineering reconstruction only.

---

## Source custody and inspection boundary

Primary public sources inspected on 2026-09-21:

1. Apache JIRA **HDFS-3194 — "DataNode block scanner is running too frequently"**
   - https://issues.apache.org/jira/browse/HDFS-3194
   - Filed in April 2012; records the observed mismatch between the expected default 21-day block scan interval and repeated scans separated by seconds.
2. Apache JIRA **HDFS-3828 — "Block Scanner rescans blocks too frequently"**
   - https://issues.apache.org/jira/browse/HDFS-3828
   - Filed 2012-08-21; gives the more precise failure mechanism: `BlockPoolSliceScanner#scan` was reached repeatedly, `cleanUp` unconditionally rolled `verificationLogs`, and after two iterations the first iteration's verification times had been lost.
3. Apache JIRA attachment **`hdfs-3828-3.txt`**
   - https://issues.apache.org/jira/secure/attachment/12543965/hdfs-3828-3.txt
   - Final reviewed patch attached 2012-09-06. It adds a current-period work test, renames the cleanup action to `rollVerificationLogs`, introduces a scanner sleep constant, and adds a regression test that repeatedly wakes the scanner while requiring only one block scan.
4. Apache JIRA integration record on HDFS-3828
   - The JIRA activity records integration on 2012-09-06 as Subversion revision **1381472**, including `BlockPoolSliceScanner.java`, `DataBlockScanner.java`, the HDFS changelog, and `TestMultipleNNDataBlockScanner.java`.
   - The same record states that the change was committed to trunk and `branch-2`; `branch-0.23` required additional merges and was deliberately not taken at that time.
5. Apache Hadoop 2.5.0 changelog
   - https://hadoop.apache.org/docs/r3.3.6/hadoop-project-dist/hadoop-common/release/2.5.0/CHANGELOG.2.5.0.html
   - Records **Release 2.5.0 — 2014-08-11** and lists HDFS-3828 among improvements.

The source set is enough to establish the bug, the code-level correction, the test invariant, the 2012 trunk/branch-2 integration, and later 2.5.0 release-record placement.

It is **not** enough to claim that 2.5.0 was the first binary ever shipped with the correction, because the JIRA itself records earlier integration to trunk and `branch-2`, and historical release-branch bookkeeping changed over time. A tag-by-tag binary genealogy remains open.

---

## Historical record

### 1. April 2012: the symptom was already explicit

HDFS-3194 describes the intended default behavior as one block scan per 21 days (three weeks), but reports the same block being verified repeatedly at roughly 15-second intervals.

That record establishes two things without reconstruction:

- the configured or expected scanner interval was much longer than the observed effective cadence;
- successful verification messages did not, by themselves, guarantee that the block would remain excluded from immediate re-verification.

Safe historical statement:

```text
expected default scan interval: ~21 days
observed effective interval in the report: seconds
```

Unsafe historical statement:

```text
HDFS-3194 already proved the final HDFS-3828 root cause in full
```

The later HDFS-3828 discussion explicitly says it branched from HDFS-3194 and supplies the more precise verification-log rollover mechanism.

### 2. August 2012: HDFS-3828 names the lost scheduling history

HDFS-3828's description states that `BlockPoolSliceScanner#scan` called `cleanUp` whenever invoked through `DataBlockScanner#run` / `scanBlockPoolSlice`; `cleanUp` unconditionally rolled the `verificationLogs`; and after two iterations the first iteration's block verification times had been lost.

The JIRA then gives a concrete one-block-cluster symptom: the same block is successfully verified at timestamps approximately ten seconds apart.

The historically grounded causal chain is therefore:

```text
scanner invoked again
    -> cleanup rolls verification logs
    -> prior verification-time entries become unavailable to that scheduling pass
    -> previously verified block can be reconsidered
    -> repeated verification at a seconds-scale interval
```

This is stronger evidence than a generic claim that "the scanner ran too often": the issue identifies which retained record was being discarded and why that mattered.

### 3. Review discussion separates wakeup cadence from work cadence

The HDFS-3828 review discusses the DataBlockScanner thread waking frequently, including a five-second sleep interval, while also trying to enforce a much longer per-block scan period.

Reviewers and the patch author considered whether the scanner should sleep until the next useful time, but the accepted near-term repair retained periodic wakeups and added a short-circuit when no work remained in the current period.

That historical discussion directly supports this distinction:

```text
worker thread wakeup cadence
    !=
block-maintenance due cadence
```

The scheduler may wake every few seconds without being entitled to re-verify the same block every few seconds.

### 4. September 2012: accepted patch restores a period-level eligibility guard

The final `hdfs-3828-3.txt` patch introduces / uses the concept `workRemainingInCurrentPeriod()`.

The relevant behavior is:

- if no bytes remain to scan **and** the current time is still before `currentPeriodStart + scanPeriod`, the method reports no current-period work;
- `scanBlockPoolSlice()` exits rather than rebuilding processing state and running a redundant scan;
- the old `cleanUp` name is replaced with the more semantically specific `rollVerificationLogs`;
- `DataBlockScanner` gets a named `SLEEP_PERIOD_MS` constant;
- the regression test wakes / samples repeatedly but asserts that the block is scanned only once during that interval.

The test is especially important because it guards the intended separation between repeated scheduler opportunities and actual verification execution.

### 5. Integration and release chronology must remain distinct

The HDFS-3828 activity stream records:

```text
2012-09-06:
    final patch accepted
    Subversion revision 1381472 integrated
    trunk + branch-2 explicitly mentioned
    branch-0.23 explicitly held back pending additional merges

2014-04-29:
    issue later marked resolved after branch bookkeeping discussion

2014-08-11:
    Hadoop 2.5.0 release changelog includes HDFS-3828
```

These are different historical events.

Do not collapse them into:

```text
"the fix happened in 2.5.0 in 2014"
```

The public record shows source integration in 2012. Conversely, do not infer from the 2012 integration alone which released binary first carried the behavior without checking the relevant tags / release branches.

---

## Terminology anchored in the 2012 sources

| Term | Historical / code meaning in this slice | Do not silently upgrade it to |
|---|---|---|
| `verificationLogs` | records used to recover / process block verification times | immutable audit log; complete forensic history |
| verification time | time associated with a completed block verification | proof that the underlying media can never fail afterward |
| scan period | interval governing scanner coverage / rescan timing | worker-thread sleep period |
| `rollVerificationLogs` | rotation / rollover operation on verification logs | payload rewrite; checksum regeneration; replica repair |
| `workRemainingInCurrentPeriod()` | guard for whether current-period scanner work remains | proof of global cluster health |
| `SLEEP_PERIOD_MS` | periodic worker sleep / wake interval | desired per-block maintenance interval |
| `totalScans` in the regression path | test-visible count of scans | durable lifetime scan counter |

This terminology table matters because the same word "period" can otherwise blur two different clocks: the short event-loop cadence and the long maintenance-coverage cadence.

---

## Engineering reconstruction

### A. Verification history was active control state

A common but unsafe simplification is:

```text
verification log = diagnostics about what already happened
```

For this code path, the 2012 bug record shows a stronger role. Prior verification times were parsed into `processedBlocks`, and that state helped prevent already covered blocks from being scanned again too soon.

A more accurate engineering classification is:

```text
verification history
    = historical observation record
    + input to future maintenance eligibility
```

Therefore:

```text
retrospective evidence
    can also be prospective control state
```

This does not make every HDFS log correctness-critical. It applies specifically to the verification-time records participating in this scanner algorithm.

### B. Successful maintenance and retained completion evidence are different states

The repeated log messages in HDFS-3828 show that the verification itself succeeded.

Yet the scanner still re-ran because prior verification timing information was lost from the effective scheduling history.

So:

```text
maintenance operation succeeded at t1
    !=
scheduler can still establish at t2 that the object is not yet due
```

The second proposition requires some surviving representation of recent completion, whether as a timestamp, period accounting, cursor, bitmap, journal entry, or another mechanism.

For this HDFS implementation, the relevant historical representation was verification-log-derived block timing state.

### C. Configured period is not self-enforcing

The user-visible / configured scan period did not magically regulate real execution. The period had to be interpreted using state that survived between repeated scanner invocations.

Thus:

```text
configured scan period
    + correct maintenance-history retention
    -> intended effective cadence
```

but:

```text
configured scan period
    + premature loss of completion history
    -> possible severe over-scanning
```

This is an important complement to the more familiar failure mode where lost maintenance state causes work to be skipped. Here, losing maintenance history caused **too much** work.

### D. Over-maintenance is a retention failure mode

Within this bounded case, a retention bug does not mean the user payload became unreadable.

Instead, the system failed to retain enough evidence of recent verification to suppress redundant work.

Consequences can include:

- unnecessary media reads;
- unnecessary CPU / I/O scheduling activity;
- scanner log noise;
- interference with useful work;
- distortion of the effective maintenance cadence.

Therefore the project's failure taxonomy should admit:

```text
maintenance-control state lost
    -> under-maintenance
or
    -> over-maintenance
or
    -> duplicated maintenance
```

Which branch occurs depends on how the lost state was used.

### E. A bounded retention horizon can be enough

The evidence does **not** imply that every verification timestamp must be retained forever.

The scheduling need is bounded: recent completion evidence needs to remain distinguishable for at least the horizon during which it determines whether a block is still covered / not due under the scanner's period logic.

Project-level reconstruction:

```text
required history lifetime
    is determined by the future decision that consumes it
```

For HDFS-3828, premature rollover within the same period was too early.

This is not a claim that the precise minimum safe horizon is universally equal to `scanPeriod`; the on-disk log organization, multiple generations, restart behavior, and period-boundary logic need code-version-specific inspection for that stronger statement.

### F. Wakeup is opportunity, not obligation

The patch's regression strategy makes another contract visible:

```text
thread wakes
    !=
block due
    !=
block scanned
```

This resembles admission-vs-execution distinctions elsewhere in the repository, but the historical source here is specific: the scanner loop can wake at a short fixed interval while `workRemainingInCurrentPeriod()` vetoes redundant current-period work.

### G. Rollover is not payload destruction

The phrase "lost the first iteration of block verification times" in HDFS-3828 refers to the verification-history representation involved in scheduling.

It does not say that:

- HDFS block payload bytes were deleted;
- block checksum files were deleted;
- replicas were removed;
- previously verified data became corrupt at rollover;
- a repair operation failed.

The strongest safe relation is:

```text
verification-history rollover
    -> loss of scheduling evidence about earlier verification
```

not:

```text
verification-history rollover
    -> loss of user data
```

---

## Failure sequence before HDFS-3828

A compact reconstructed sequence, bounded by the JIRA description and patch:

```text
1. Block B is successfully verified.
2. B's verification time is present in verification-log-derived state.
3. DataBlockScanner wakes again shortly afterward.
4. BlockPoolSliceScanner enters the path that invokes cleanup / rollover.
5. verificationLogs are rolled again within the still-current scan period.
6. After repeated rollovers, an earlier verification-time entry is no longer available.
7. The reconstructed processed-block history no longer proves B was already covered recently.
8. B becomes eligible for another scan.
9. The same block is successfully verified again seconds later.
```

Step 7 is an engineering explanation of the scheduling consequence; the historical record explicitly supplies the earlier log loss and repeated rescan symptom.

---

## Repair invariant after HDFS-3828

The accepted patch adds an early eligibility check. In project terms, its bounded invariant is:

```text
if current-period work has already been exhausted
and the current scan period has not expired,
repeated scanner wakeups must not cause another full block scan.
```

The regression test turns that into executable evidence by repeatedly waiting around the short scanner wake interval while asserting one total scan for the block during the observed period.

This is not a full proof of all scanner scheduling semantics, but it is strong evidence for the specific bug contract.

---

## Relation to HDFS-3194

HDFS-3194 and HDFS-3828 should not be collapsed into one issue.

Safe relationship:

```text
HDFS-3194:
    earlier report / attempted correction of pathological over-scanning

HDFS-3828:
    follow-on issue identifying remaining premature verification-log rollover
    and adding a current-period work guard + regression test
```

HDFS-3828's own comments say the patch was significantly inspired by HDFS-3194 while little code remained from the earlier work.

This is enough to establish issue-level continuity, not a broader genealogy claim about every later scanner implementation.

---

## Relation to later Case 83 evidence

### 1. 2012 verification-log history vs later `VolumeScanner` cursor

Both mechanisms help a scanner avoid losing its place in recurring maintenance, but they are not the same retained object.

```text
2012 verification-log-derived state:
    per-block / recent verification history used in eligibility processing

later VolumeScanner cursor:
    traversal-position checkpoint used to resume volume scanning
```

Controlled functional analogy:

```text
both retain maintenance-progress information across time
```

Rejected stronger claim:

```text
verificationLogs == VolumeScanner cursor
```

No such identity is established here.

### 2. 2012 rollover bug vs HDFS 2.7.0 scanner-enable regression

The later 2.7.0 bug shows:

```text
scanner implementation exists
    !=
scanner is effectively enabled
```

The 2012 bug shows a different boundary:

```text
scanner executes successfully
    !=
its effective cadence is correct
```

Together, these are useful but distinct maintenance-control failures.

### 3. 2012 history loss vs 2018 partial checksum cache

The later checksum cache is reconstructible performance state; losing it need not destroy integrity authority.

The 2012 verification-time history is also not user payload, but in this code path it directly affects maintenance scheduling.

Thus:

```text
non-payload state
    !=
optional state
```

and:

```text
reconstructible eventually
    !=
safe to discard at every moment
```

The exact reconstruction semantics differ across these mechanisms.

---

## Controlled cross-case comparison

This section is **functional comparison only**. It does not assert a historical lineage.

### Case 26 — GFS integrity evidence

Case 26 distinguishes correctness-relevant integrity records from optional diagnostic history.

Case 83 adds a complementary example: a record about completed maintenance can be operationally active because the scheduler consumes it.

Safe comparison:

```text
what looks like "history" can have a future operational consumer
```

Rejected comparison:

```text
GFS diagnostic logs and HDFS verificationLogs have the same correctness role
```

They do not.

### Synthesis 29 — maintenance observability

Synthesis 29 distinguishes schedule, execution, coverage, accounting, and closure. HDFS-3828 supplies a useful concrete case where completion/accounting evidence feeds the next scheduling decision.

Safe project-level comparison:

```text
maintenance completion observed once
    !=
completion evidence retained long enough for later scheduling
```

The synthesis terminology postdates the 2012 HDFS sources and must not be attributed to Apache developers as their historical vocabulary.

---

## Philosophical interpretation — explicitly fenced off

A narrow philosophical reading is possible:

> A system can need memory of its own successful maintenance in order not to repeat that maintenance pathologically.

This is a project interpretation, not an HDFS design phrase.

The historical case is concrete enough without the philosophical layer:

- a block was verified;
- verification time was recorded;
- records were rolled too aggressively;
- the scheduler lost earlier verification times;
- the block was scanned again far too soon;
- a patch restored a current-period eligibility guard.

No anthropomorphic claim is required.

---

## Explicit non-claims

This evidence does **not** claim that:

1. HDFS invented periodic background block scrubbing.
2. HDFS-3194 and HDFS-3828 are the same bug report.
3. every HDFS version used the same verification-log format.
4. every block verification timestamp had to survive forever.
5. `verificationLogs` were an immutable audit log.
6. `verificationLogs` preserved a complete forensic history of all scans.
7. rolling a verification log deleted HDFS payload blocks.
8. rolling a verification log deleted block checksum data.
9. a successful scan repaired a block.
10. a successful scan proved the media would remain healthy afterward.
11. the five-second scanner wakeup interval was the intended per-block verification interval.
12. the configured 21-day default alone was enough to enforce actual cadence.
13. repeated scanning necessarily caused data corruption.
14. repeated scanning necessarily caused a user-visible outage.
15. loss of maintenance history always causes under-maintenance.
16. loss of maintenance history always causes over-maintenance.
17. HDFS-3828 fixed every scanner scheduling inefficiency.
18. revision 1381472 was immediately present in every maintained Hadoop branch.
19. branch-0.23 received the 2012 patch; the JIRA explicitly says it was held back at that point.
20. Hadoop 2.5.0 was necessarily the first released binary carrying the behavior.
21. the 2014 changelog date is the same event as the 2012 source integration.
22. `verificationLogs` are identical to later `VolumeScanner` cursor checkpoints.
23. later cursor semantics can be retroactively assigned to 2012 code.
24. the HDFS developers used the phrase "maintenance-completion evidence".
25. the HDFS developers used the phrase "retention horizon" in this issue.
26. a historical timestamp is operationally important merely because it exists.
27. all operational logs should therefore be retained indefinitely.
28. a log record's diagnostic value and scheduling value are the same thing.
29. one-block-cluster behavior alone proves all multi-block / multi-volume edge cases.
30. this slice closes Case 83's remaining restart, clock, release-lineage, and fault-injection debts.

---

## Evidence strength

### Strongly grounded

- HDFS-3194 reported a seconds-scale repeated-scan symptom against a stated 21-day default expectation.
- HDFS-3828 explicitly identifies unconditional verification-log rolling as causing earlier verification times to be lost after repeated iterations.
- The final patch adds a current-period work guard and regression testing against repeated scans.
- The JIRA records 2012-09-06 integration to trunk and branch-2 as revision 1381472 and explicitly says branch-0.23 was held back at that moment.
- Hadoop's 2.5.0 changelog lists HDFS-3828 under the 2014-08-11 release.

### Engineering reconstruction, not historical wording

- verification-time history is classified here as `maintenance-control state` because later eligibility consumes it;
- preservation duration is described as a `retention horizon` determined by the future scheduling decision;
- losing completion history is classified as an `over-maintenance` / duplicated-maintenance failure mode.

### Still open

- exact verification-log on-disk format and generation-retention behavior across each affected version;
- restart / crash semantics for these logs in the precise pre- and post-HDFS-3828 code;
- first released tag carrying revision 1381472 behavior on each supported branch;
- empirical I/O / latency effect of pathological rescanning under realistic multi-block volumes;
- whether every path reading these logs used the same notion of recent verification;
- precise genealogy from `DataBlockScanner` verification logs to later `VolumeScanner` cursor / iterator persistence.

---

## Related-repository reuse check

`tmzncty/computing-archaeology` was searched for `DataBlockScanner` / HDFS block-scanner material before writing this slice. No directly reusable packet was found.

Accordingly, this file keeps only the retention-specific evidence needed by `technical-retention`; it does not create a general Hadoop scanner history merely to duplicate another repository's possible future scope.

---

## Candidate canonical delta

This evidence supports adding the following bounded claims to Case 83 when convenient:

```text
2012 HDFS verification-time logs were not merely retrospective diagnostics;
they participated in suppressing premature block rescans.

Premature rollover could erase recent completion evidence while the configured
scan period was still in force, producing repeated successful scans every few
seconds instead of the intended long cadence.

Therefore scanner loop wakeup, successful scan execution, retained verification
history, and effective rescan cadence are distinct retained-state relations.
```

Canonical maturity should remain **`grounded`**. This slice deepens one scheduling-state failure mode but does not close the broader restart, fault-injection, release genealogy, or later-scanner-transition debts.

---

## Primary references

- Apache JIRA, **HDFS-3194 — DataNode block scanner is running too frequently**: https://issues.apache.org/jira/browse/HDFS-3194
- Apache JIRA, **HDFS-3828 — Block Scanner rescans blocks too frequently**: https://issues.apache.org/jira/browse/HDFS-3828
- Apache JIRA attachment, **hdfs-3828-3.txt**: https://issues.apache.org/jira/secure/attachment/12543965/hdfs-3828-3.txt
- Apache Hadoop changelog, **Release 2.5.0 — 2014-08-11**: https://hadoop.apache.org/docs/r3.3.6/hadoop-project-dist/hadoop-common/release/2.5.0/CHANGELOG.2.5.0.html

Accessed: 2026-09-21.
