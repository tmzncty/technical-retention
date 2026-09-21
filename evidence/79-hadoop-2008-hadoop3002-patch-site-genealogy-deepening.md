# Evidence 79D — HADOOP-3002 Patch-Site Genealogy, Deferred Invalidation, and SafeMode Execution Authority (2008)

## Status

**`bounded deepening complete`**. Canonical Case 79 remains **`grounded`**; this source-genealogy slice does not justify a maturity promotion.

This record closes a narrow debt left by the earlier SafeMode destructive-command deepening:

> What exact source change carried HADOOP-3002, how did the first implementation differ from the final one, and what does the released code say about the lifetime of a deletion obligation versus permission to execute deletion now?

The answer is unusually concrete because the archived Apache Git/SVN history preserves both a failed first attempt and the final branch merges.

The final HADOOP-3002 source revision was **SVN r675012**. It was merged into:

- `branch-0.18` as Git commit `5b3f857124b8e962d3a4fce00df622fb926c2bbc`, branch SVN r675015, on 2008-07-08;
- `branch-0.17` as Git commit `c32d1180b0755c6659131c7a60ffac104f6233e5`, branch SVN r675055, also on 2008-07-08.

In the released 0.17 line the source transformation is direct:

```text
0.17.1
block report discovers blocks that do not belong to a file
    -> processReport returns an array of obsolete blocks
    -> NameNode.blockReport may immediately return DNA_INVALIDATE

0.17.2 / HADOOP-3002
block report discovers blocks that do not belong to a file
    -> reportDiff classifies them into toInvalidate
    -> processReport calls addToInvalidates(...)
    -> processReport returns no deletion command
    -> ordinary invalidation scheduling emits work later
```

The retention-specific result is therefore:

```text
recognize a deletion obligation
    !=
emit a deletion command now
```

and more strongly:

```text
retain pending invalidation work
    + withhold execution authority during SafeMode
    -> defer destructive maintenance without forgetting it
```

`pending invalidation work`, `execution authority`, and `deletion obligation` are project engineering terms. Apache's historical vocabulary is `safe mode`, `block report`, `invalidate`, `block removal`, `recentInvalidateSets`, `heartbeat`, and related code identifiers.

---

## Scope

This slice is intentionally limited to:

1. the July 2008 HADOOP-3002 patch sequence;
2. the first branch-0.18 merge and its subsequent revert;
3. the final trunk source revision and the exact branch-0.18 / branch-0.17 merges;
4. the released 0.17.1 -> 0.17.2 source delta at the block-report, invalidation, and scheduler seams;
5. the distinction among identifying stale/invalid work, retaining that work, and authorizing destructive execution.

It does **not** attempt to reconstruct:

- every HDFS invalidation path in 2008;
- every lock in the NameNode or a formal deadlock proof;
- HADOOP-4810's later startup-loss root cause;
- the exact persistence behavior of `recentInvalidateSets` across NameNode process restart;
- all branch differences outside HADOOP-3002;
- an invention-priority genealogy for deferred deletion queues;
- modern HDFS invalidation behavior from this 2008 code;
- the complete history of SafeMode.

---

## Source custody and chronology

### Primary source A — HADOOP-3002 issue record

ASF JIRA HADOOP-3002 is titled **“HDFS should not remove blocks while in safemode.”** The issue was created on 2008-03-12, marked Blocker, affected 0.16.0, resolved on 2008-07-08, and lists 0.17.2 as its fix version.

The discussion records the implementation seam directly. Heartbeat processing already had SafeMode-aware command suppression, while block-report processing could independently return commands that caused removal. The issue therefore targeted more than a documentation statement: it targeted an execution path that bypassed the intended policy.

Source:

- https://issues.apache.org/jira/browse/HADOOP-3002

### Primary source B — first branch-0.18 merge, 2008-07-07

The archived `apache/hadoop-common` history preserves an early HADOOP-3002 merge:

- Git SHA: `9fc0ca9d4610b43a18df4987d01e194cacefc2f1`
- message: `HADOOP-3002. Merge -r 674644:674645 from trunk to branch 0.18.`
- branch SVN revision: `674648`

Source:

- https://github.com/apache/hadoop-common/commit/9fc0ca9d4610b43a18df4987d01e194cacefc2f1

This first attempt already removed direct delete-command return from block-report processing and added a broader SafeMode-aware rewrite of heartbeat command handling. It also moved the SafeMode check upward from replication-only scheduling into broader DataNode work computation.

### Primary source C — explicit revert, 2008-07-07

The archived history then records an explicit HADOOP-3002 revert:

- Git SHA: `6afd12e39cf9d9251632c9aa9e01eab7fea12869`
- message: `Revert changes for revision 674657-674658 related to HADOOP-3002.`
- branch SVN revision: `674675`

Source:

- https://github.com/apache/hadoop-common/commit/6afd12e39cf9d9251632c9aa9e01eab7fea12869

The JIRA discussion explains why the first version was abandoned: reviewers identified a possible lock-order / deadlock problem in the broader heartbeat-path change. Shvachko reported reverting the committed change and then posted a revised patch that no longer changed heartbeat processing directly.

This chronology matters because it prevents a false narrative in which one obvious `if (safeMode)` check was simply missing and then trivially added.

### Primary source D — final trunk source revision and branch-0.18 merge

The final branch-0.18 merge is exact:

- Git SHA: `5b3f857124b8e962d3a4fce00df622fb926c2bbc`
- message: `HADOOP-3002. Merge -r 675011:675012 from trunk to branch 0.18.`
- source revision: trunk SVN **r675012**
- branch SVN revision: `675015`
- date: 2008-07-08

Source:

- https://github.com/apache/hadoop-common/commit/5b3f857124b8e962d3a4fce00df622fb926c2bbc

The branch commit contains the full patch, so an inaccessible historical trunk Git SHA is not required to reconstruct the actual code delta. The source identity is preserved as SVN r675012 and by the exact merged branch diff.

### Primary source E — final branch-0.17 merge

The same final trunk change was merged into branch 0.17:

- Git SHA: `c32d1180b0755c6659131c7a60ffac104f6233e5`
- message: `HADOOP-3002. Merge -r 675011:675012 from trunk to branch 0.17.`
- source revision: trunk SVN **r675012**
- branch SVN revision: `675055`
- date: 2008-07-08

Source:

- https://github.com/apache/hadoop-common/commit/c32d1180b0755c6659131c7a60ffac104f6233e5

This gives a direct branch-lineage relation:

```text
trunk r675012
    -> branch-0.18 r675015 / Git 5b3f8571...
    -> branch-0.17 r675055 / Git c32d1180...
```

It does not imply the two branches were otherwise source-identical.

### Primary source F — released 0.17.1 and 0.17.2 source

The archived Apache repository exposes both release tags. In 0.17.1, `FSNamesystem.processReport(...)` returns `Block[]`. Invalid blocks can be placed into a local `obsolete` list and returned; `NameNode.blockReport(...)` turns a nonempty returned array into a deletion command.

In 0.17.2, `processReport(...)` returns `void`. `DatanodeDescriptor.reportDiff(...)` receives a new `toInvalidate` collection. Blocks absent from `blocksMap` are classified into `toInvalidate`; `processReport(...)` passes those blocks to `addToInvalidates(...)`; and `NameNode.blockReport(...)` no longer constructs a deletion command from the report response.

Sources:

- 0.17.1 source tree: https://github.com/apache/hadoop-common/tree/release-0.17.1
- 0.17.2 source tree: https://github.com/apache/hadoop-common/tree/release-0.17.2
- branch-0.17 final HADOOP-3002 diff: https://github.com/apache/hadoop-common/commit/c32d1180b0755c6659131c7a60ffac104f6233e5

---

## Historical record

### H/P — the pre-fix block-report path could combine observation and immediate deletion command emission

In the 0.17.1 source, `processReport(...)` does two conceptually different jobs in one request path:

1. update the NameNode's block-location working relation from the DataNode report;
2. build a bounded list of blocks considered obsolete and return that list to the RPC caller.

`NameNode.blockReport(...)` can then immediately translate the returned list into a block-invalidation command.

The source even documents the split behavior for larger obsolete sets: once the direct-return list exceeds the configured chunk boundary, additional invalidations are placed into `recentInvalidateSets` to be sent later through heartbeat responses.

Thus the old implementation already had **two invalidation-delivery routes**:

```text
block-report direct return
    OR
queued invalidation -> later heartbeat response
```

HADOOP-3002 removes the direct-return route from the block-report path.

### H/P — the final patch makes `toInvalidate` a first-class report-difference result

The final diff changes `DatanodeDescriptor.reportDiff(...)` from four relevant parameters to five by adding a `toInvalidate` collection.

A reported block not found in `blocksMap` is no longer inserted into `toAdd`; it is inserted into `toInvalidate`.

That distinction matters historically: the final patch does not merely suppress a command after classification. It changes the report-difference representation so that “reported but does not belong to a file” is carried as a separate invalidation result.

### H/P — `processReport` stops returning deletion work to the block-report RPC

The final patch changes:

```text
Block[] processReport(...)
```

to:

```text
void processReport(...)
```

and removes the local `obsolete` array returned to the caller.

`NameNode.blockReport(...)` correspondingly stops converting that returned array into a `DNA_INVALIDATE` / block-removal command.

This is an exact code-level closure of the seam described in HADOOP-3002: block-report processing can still identify blocks that should eventually be invalidated, but it no longer emits their deletion in the block-report response.

### H/P — invalidation work is retained through the ordinary invalidation machinery

For each `toInvalidate` block, the final patch calls:

```text
addToInvalidates(b, node)
```

The 0.17 source comments describe `recentInvalidateSets` as per-storage collections of blocks recently invalidated and believed to live on that machine. Later DataNode work/heartbeat processing can draw invalidation work from those structures.

The bounded historical statement is therefore:

> HADOOP-3002 changed the block-report path from immediate deletion-command return to registering invalidation work for deferred scheduling.

This does **not** establish that the invalidation queue was crash-persistent. In this source family it is a NameNode working-state structure; this slice makes no durability claim across NameNode restart.

### H/P — the scheduler-level SafeMode check is broadened

The final patch also moves the SafeMode check.

Before the change, the check sat inside `computeReplicationWork(...)`, so it prevented replication scheduling but did not cover invalidation work computed by the sibling path.

After the change, `computeDatanodeWork(...)` checks `isInSafeMode()` before computing either replication or invalidation work and returns immediately when SafeMode is active.

Therefore the final structure is not merely:

```text
blockReport no longer returns delete command
```

It is also:

```text
SafeMode active
    -> computeDatanodeWork returns before
       replication work or invalidation work is scheduled
```

That is a broader execution-authority gate.

### H/P — the first patch pursued a broader heartbeat-path rewrite and was reverted

The first branch-0.18 merge (`9fc0ca9d...`) changed `handleHeartbeat(...)` directly so that SafeMode returned only the distributed-upgrade command while other ordinary commands were suppressed. It also contained the block-report deferral and scheduler-level changes.

The explicit revert (`6afd12e3...`) undid those changes. JIRA discussion ties the retreat to concern about lock ordering / possible deadlock. The revised final patch then achieved the SafeMode removal goal **without** the same direct heartbeat-processing rewrite.

This produces an unusually useful historical negative result:

> a safety property can be desirable while a particular implementation of that property is rejected because it threatens another correctness property, here liveness/concurrency safety.

The sources do not justify a formal proof that deadlock definitely occurred; the historical record supports “potential deadlock / lock-order concern” and an actual revert.

### H/P — both 0.17 and 0.18 receive the same final trunk source revision

The branch commit messages explicitly name the same trunk interval, `675011:675012`, for both branches.

That is stronger chronology evidence than merely observing similar released behavior later. It establishes shared source lineage for this particular HADOOP-3002 change.

It does **not** establish that every surrounding class or branch state was identical; the actual diffs show branch-specific source-layout and nearby-code differences.

---

## Engineering reconstruction

### E — deletion obligation and deletion execution have different lifetimes

The most useful retention decomposition is:

```text
block report supplies evidence
    -> controller classifies a block for invalidation
    -> invalidation obligation is represented in working state
    -> scheduler waits until ordinary execution is admitted
    -> later heartbeat can carry deletion work
    -> DataNode may then remove the block
```

Therefore:

> **deletion obligation exists != deletion authority is active now**.

And:

> **deferring destructive maintenance != forgetting that maintenance is owed**.

This is a technical-retention relation because retaining the *obligation* is what allows the system to postpone destruction safely without permanently abandoning reclamation.

### E — control-state retention can be about future destruction, not only future preservation

Many retention mechanisms preserve state because a future operation needs it to keep data alive. Here, a queue/working relation preserves state because a future operation may eventually destroy stale data.

That gives a complementary pattern:

```text
retain enough control state now
    so that destructive work can be executed later
    under a safer authority condition
```

The retained item is not the user payload. It is a future maintenance obligation.

### E — immediate observation should not automatically carry immediate destructive authority

A block report is fresh positive input from a DataNode. The pre-fix path could use the same RPC interaction both to update the inventory relation and to return delete commands for blocks that did not fit the NameNode's current namespace/block map.

The final patch separates those stages.

Thus:

> **fresh observation event != permission to complete all consequences of that observation in the same response**.

This is especially important during startup SafeMode, when the NameNode is deliberately reconstructing distributed placement knowledge.

### E — moving a guard upward changes its authority surface

The SafeMode check moved from `computeReplicationWork(...)` to `computeDatanodeWork(...)`.

Engineering reconstruction:

```text
lower-level guard
    -> protects replication scheduling only

higher-level guard
    -> protects the combined DataNode-work scheduling surface
       before replication and invalidation are split
```

The source therefore supplies a concrete example of **guard placement** being part of the retention contract. A policy statement is not enough; the guard must dominate every relevant destructive-work path.

### E — a correct policy can have an unsafe first synchronization strategy

The first patch's revert prevents a simplistic lesson such as “put the SafeMode test earlier and the bug is solved.” The first implementation mixed the desired command restriction with a broader heartbeat control-flow change and triggered lock-order concerns.

The bounded engineering result is:

> **correct safety policy != concurrency-safe first implementation**.

And:

```text
one hazard reduced
    !=
no new hazard introduced by the guard itself
```

This should remain an engineering reconstruction, not a claim that HADOOP-3002's authors used this exact abstraction.

### E — queueing is not durability

`addToInvalidates(...)` is enough to decouple discovery from immediate command emission within the running NameNode, but the inspected source does not turn `recentInvalidateSets` into a durable journal in this slice.

Therefore:

> **deferred work represented in memory != crash-persistent work obligation**.

If later restart behavior matters, it must be established separately from source or fault injection. The system may be able to rediscover invalidation work from subsequent reports; that is a different claim from persisting the exact queue.

### E — release-bearing source matters more than an abandoned patch

The first patch is historically useful because it exposes the design search and the concurrency tradeoff. It is not the final contract.

For the bounded released claim, the evidence hierarchy is:

```text
JIRA proposal / early patch
    < committed-then-reverted branch state
    < final trunk revision merged to release branches
    < released/tagged source carrying the final structure
```

This prevents an abandoned implementation detail from being projected into Hadoop 0.17.2 behavior.

---

## Controlled functional comparisons

### A — Case 153, Ceph snap-trim obligation reconstruction

Case 153 has a functionally similar split:

```text
cleanup debt exists
    !=
a particular actor is currently authorized to execute cleanup
```

HADOOP-3002 supplies a different implementation and history:

```text
invalidation obligation exists
    !=
SafeMode permits deletion command emission now
```

The analogy is **functional only**. There is no claim that HDFS derived this design from Ceph, or vice versa.

### A — Case 46, GFS runtime-location reconstruction

Case 46 shows storage-location state being reconstructed after master restart. Case 79 adds a separate admission question: whether destructive maintenance should run while distributed inventory is being re-established.

Functional relation only:

```text
reconstructed location knowledge
    !=
destructive action automatically admitted
```

No GFS-to-HDFS source genealogy is claimed here.

### A — Case 51, HDFS command fencing

Case 51 asks which NameNode is entitled to issue block-changing commands after HA transitions. HADOOP-3002 asks whether an otherwise legitimate NameNode should emit a class of destructive command while SafeMode is active.

Therefore:

> **command-source authority != command-class admission under current recovery state**.

### A — Case 83, maintenance-history control state

Case 83 shows that retaining recent verification history affects whether future maintenance is due. HADOOP-3002 shows a different control-state role: pending invalidation work can remain due while execution is intentionally withheld.

Thus:

> **maintenance eligibility history != pending destructive-work obligation**.

---

## Philosophical interpretation — bounded

A narrow project-level formulation is useful:

> **Remembering that something should eventually be forgotten is not the same as being permitted to forget it now.**

In this case, the NameNode can preserve a pending invalidation relation while SafeMode withholds destructive execution. The retained control state therefore mediates a future act of forgetting/reclamation.

A second bounded formulation is:

> Technical preservation can depend on the controlled postponement of destruction, not only on active duplication or repair.

These are repository interpretations. Apache's developers discussed SafeMode, invalidation, block reports, heartbeat processing, lock ordering, and block removal—not a philosophical theory of memory or forgetting.

---

## Explicit non-claims

This evidence record does **not** claim that:

1. HADOOP-3002 invented deferred invalidation queues.
2. SVN r675012 is the invention date for SafeMode or destructive-command gating.
3. The historical trunk commit has been assigned a Git SHA here; the exact source identity available in the archive is SVN r675012 plus exact branch merge commits.
4. `branch-0.17` and `branch-0.18` were otherwise identical.
5. The Git annotated-tag timestamp for `release-0.17.2` is the original 2008 release timestamp; mirror/tag migration metadata must not replace historical release records.
6. `recentInvalidateSets` is durable across NameNode restart.
7. Queued invalidation work survives every crash without rediscovery.
8. A block in `toInvalidate` was physically deleted immediately.
9. A block absent from `blocksMap` is proof that its bytes are physically corrupt.
10. Every HDFS deletion path in 2008 passed through HADOOP-3002's exact code sites.
11. HADOOP-3002 fixed every later startup deletion bug.
12. HADOOP-4810 has the same root cause as HADOOP-3002.
13. SafeMode establishes complete global replica knowledge.
14. The 0.999 threshold means every block or every DataNode has reported.
15. A block report is a cryptographic proof.
16. A block report is itself a repair operation.
17. `addToInvalidates(...)` means the DataNode has acknowledged deletion.
18. Invalidation queued means invalidation completed.
19. SafeMode means all reads are universally available.
20. Manual SafeMode and automatic startup SafeMode have identical lifecycle semantics.
21. The first patch's lock concern proves a deadlock actually occurred in production.
22. The first patch's revert means the SafeMode removal policy was rejected.
23. Moving the guard to `computeDatanodeWork(...)` proves no other command path existed.
24. Every heartbeat command is destructive.
25. Every invalidation obligation originated from negative/missing evidence.
26. Apache developers used the project terms `execution authority`, `deletion obligation`, or `action-relative evidence`.
27. HDFS derived its invalidation design from Ceph or GFS.
28. A retained deletion obligation is user payload.
29. Deferring deletion is equivalent to never reclaiming stale blocks.
30. Released 0.17.2 source can be projected unchanged onto modern HDFS.

---

## Evidence ledger

| Claim | Layer | Evidence | Strength / boundary |
| --- | --- | --- | --- |
| HADOOP-3002 targets block removal while SafeMode is active | H/P | ASF JIRA HADOOP-3002 | strong, issue-level |
| first branch-0.18 HADOOP-3002 merge was `9fc0ca9d...` from trunk r674645 | H/P | archived Apache Git commit | strong |
| an explicit HADOOP-3002 revert followed as `6afd12e3...` | H/P | archived Apache Git commit | strong |
| JIRA discussion ties the revised patch to lock/deadlock concern | H/P | ASF JIRA comments | strong for concern/revert rationale; not proof of production deadlock |
| final source revision was trunk r675012 | H/P | branch merge commit messages | strong |
| branch-0.18 final merge is `5b3f8571...` / r675015 | H/P | archived Apache Git commit | strong |
| branch-0.17 final merge is `c32d1180...` / r675055 | H/P | archived Apache Git commit | strong |
| final patch changes reportDiff to produce `toInvalidate` | H/P | exact commit diff | strong |
| final patch changes `processReport` from `Block[]` to `void` | H/P | exact commit diff | strong |
| final patch removes direct invalidate command from `NameNode.blockReport` | H/P | exact commit diff | strong |
| final patch sends invalid blocks through `addToInvalidates` | H/P | exact commit diff | strong |
| final patch moves SafeMode check from replication-only work to combined DataNode work | H/P | exact commit diff | strong |
| invalidation obligation can exist while execution is withheld | E | reconstruction from queue + SafeMode gate | strong, bounded to running-state semantics |
| deferred invalidation queue is crash-persistent | X | not established | rejected |
| correct safety policy != concurrency-safe first implementation | E | first merge + revert + JIRA lock concern | strong as bounded reconstruction |
| Ceph snap-trim is genealogically related | X | no evidence | rejected; functional analogy only |

---

## Related-repository boundary

A fresh search of `tmzncty/computing-archaeology` for `HADOOP-3002`, `recentInvalidateSets`, and SafeMode/block-removal material found no dedicated reusable packet in this pass.

A broad history of Hadoop's SVN-to-Git migration, NameNode locking, RPC command evolution, or the complete invalidation subsystem belongs more naturally in `computing-archaeology` if developed later. This file keeps only the retention-specific seam: **classification of destructive work, retention of pending obligation, and delayed execution authority during startup SafeMode**.

---

## Remaining work after this slice

This slice closes the local debts for:

- exact final HADOOP-3002 source revision;
- exact branch-0.17 and branch-0.18 merge commits;
- released 0.17.1 -> 0.17.2 block-report/invalidation patch site;
- the first-attempt -> revert -> revised-final chronology.

Still open:

1. locate a canonical Git object for the historical trunk r675012 itself, if a faithful pre-split mirror exposes one; this is a provenance refinement, not required to establish the final code delta;
2. period-correct fault injection with partial/delayed block reports and invalidation-command tracing;
3. separate reconstruction of HADOOP-4810 corrupt/excess-replica classification and deletion ordering;
4. determine, in a separate persistence slice, how invalidation obligations are rediscovered or reconstructed across NameNode restart rather than assuming the exact in-memory queue survives;
5. repository-wide `CASE_INDEX.md` repair as an independent navigation task.

Case 79 remains **`grounded`**.