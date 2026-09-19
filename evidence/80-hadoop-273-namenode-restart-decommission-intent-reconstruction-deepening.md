# Case 80 deepening — Hadoop 2.7.3 NameNode restart, decommission-intent re-import, and disposable progress state

**Status:** `bounded deepening complete` for the NameNode-restart / decommission-intent reconstruction seam.

Canonical case: [`../cases/80-apache-hdfs-datanode-decommission-replica-drain.md`](../cases/80-apache-hdfs-datanode-decommission-replica-drain.md).

## Scope

Case 80 already establishes the ordinary Hadoop 2.7.3 decommission relation:

```text
operator exclusion
    -> DECOMMISSION_INPROGRESS
    -> inspect replica sufficiency / placement
    -> schedule preservation work as needed
    -> revalidate against the actual block map
    -> DECOMMISSIONED
```

This addendum asks one narrower question:

> **If the NameNode process is restarted while decommission intent exists, what actually has to survive the process boundary for the retirement obligation to continue?**

The bounded answer is not `the whole DecommissionManager state machine is durably checkpointed`.

The inspected Hadoop 2.7.3 source and regression test instead expose three different persistence horizons:

1. **administrator-selected include/exclude configuration** survives outside the NameNode process and is re-read when a new `DatanodeManager` is constructed;
2. **`pendingNodes` / `decomNodeBlocks` decommission-progress structures** are ordinary in-memory collections newly allocated with each `DecommissionManager` instance;
3. **current replica/block relations** are re-observed through DataNode registration/reporting and are consulted again before final retirement authority is granted.

A release-bounded regression test makes the restart seam concrete: it writes a DataNode into the exclude file, adds another DataNode, restarts the NameNode, waits for the originally excluded node to reach `DECOMMISSIONED`, and verifies that the block has been replicated while both DataNodes remain alive.

This is a retention-specific control-state study, not a general HDFS startup history, not a filesystem/configuration-file durability study, and not a claim that every Hadoop release reconstructs decommission state in exactly this way.

---

## Source custody and inspected baseline

The source-level baseline is Apache Hadoop **`branch-2.7.3`**, inspected at branch-head commit:

- `baa91f7c6bc9cb92be5982de4719c1c8af91ccff` — `Set the release date for 2.7.3-RC2`, 18 August 2016.

Pinned source paths:

- `DatanodeManager.java`:
  <https://github.com/apache/hadoop/blob/baa91f7c6bc9cb92be5982de4719c1c8af91ccff/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/DatanodeManager.java>
- `DecommissionManager.java`:
  <https://github.com/apache/hadoop/blob/baa91f7c6bc9cb92be5982de4719c1c8af91ccff/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/DecommissionManager.java>
- `TestDecommission.java`:
  <https://github.com/apache/hadoop/blob/baa91f7c6bc9cb92be5982de4719c1c8af91ccff/hadoop-hdfs-project/hadoop-hdfs/src/test/java/org/apache/hadoop/hdfs/TestDecommission.java>

The repository's broader Case-80 grounding continues to supply the older 0.18/1.0.4 documentation history and the 2.7.x decommission/placement context. This packet does not repeat that history.

Fresh searches of `tmzncty/computing-archaeology` for `HDFS decommission restart` and `dfs.hosts.exclude` found no dedicated packet to reuse. Broader Hadoop administration/configuration and HA evolution remain companion-repository territory if developed later.

---

## Historical record

### H/P — the NameNode process reads host membership/exclusion configuration into a fresh manager

In the Hadoop 2.7.3 `DatanodeManager` constructor, a new `HostFileManager` is created as an ordinary field of the newly constructed manager. During construction, the code calls `hostFileManager.refresh(...)` using the configured `DFS_HOSTS` and `DFS_HOSTS_EXCLUDE` paths.

The bounded historical relation is therefore:

```text
new NameNode-side manager instance
    -> read configured include/exclude files
    -> construct current in-process host-policy view
```

This is stronger than saying only that an already-running NameNode can react to `dfsadmin -refreshNodes`. The constructor itself imports the host-file relation when the manager is created.

It is also weaker than saying `dfs.hosts.exclude is part of fsimage/edit-log state`. The inspected source shows external configuration being read; it does not convert that file into a NameNode namespace-journal object.

### H/P — explicit `refreshNodes` and process construction are two different import opportunities

`DatanodeManager.refreshNodes(conf)` calls `refreshHostsReader(conf)`, obtains the namesystem write lock, and then invokes `refreshDatanodes()`.

`refreshDatanodes()` maps current host configuration onto already known DataNodes:

```text
not included
    -> mark disallowed

included + excluded
    -> start decommission

included + not excluded
    -> stop decommission
```

This is the ordinary running-process path already broadly represented in Case 80.

The constructor path above matters because it shows that restart continuity does not require the old process to execute a final `refreshNodes()` before dying. A new manager has its own configuration-import path.

### H/P — DataNode registration re-applies exclude policy

Hadoop 2.7.3 also checks exclusion when a DataNode registers.

`DatanodeManager.startDecommissioningIfExcluded(DatanodeDescriptor nodeReg)` does exactly the bounded policy handoff its name suggests:

```text
if hostFileManager says this DataNode is excluded
    -> decomManager.startDecommission(nodeReg)
```

`registerDatanode(...)` calls this helper after registering the descriptor with the heartbeat/topology structures for both replacement/restart and new-registration paths inspected here.

This gives a restart-relevant relation:

```text
exclude intent survives outside old NameNode process
    + DataNode later registers with new NameNode process
        -> exclusion is evaluated again
        -> decommission transition can be re-established
```

The old in-memory `AdminState` object does not have to be treated as the sole carrier of the obligation.

### H/P — `DecommissionManager` progress containers are newly allocated process-local structures

The Hadoop 2.7.3 `DecommissionManager` constructor creates:

- `decomNodeBlocks = new TreeMap<>()`;
- `pendingNodes = new LinkedList<>()`.

The class documentation says `decomNodeBlocks` contains decommission-in-progress nodes plus references to blocks that currently prevent completion. It also explicitly warns that the map can become out of date because block reports and other events do not update it continuously.

`startDecommission(node)` then places a newly decommissioning live node into this runtime machinery:

- `hbManager.startDecommission(node)` changes the administrative relation;
- if the node is in progress, the implementation records a monotonic start time in `node.decommissioningStatus`;
- the node is appended to `pendingNodes` for later scanning/tracking.

Nothing in the inspected constructor serializes the prior Java `TreeMap`, `LinkedList`, iterator position, or monotonic start time and reloads the same process objects after restart.

Safe historical statement:

> **The inspected decommission progress collections are process-local working state and are constructed anew with a new `DecommissionManager`.**

Unsafe stronger statement:

> **No decommission-related information survives anywhere across NameNode restart.**

The latter is contradicted by the externally retained host exclusion and the restart regression test below.

### H/P — the progress map is not authoritative even before considering restart

The source itself says `decomNodeBlocks` may become stale and that, before a DataNode is finally marked decommissioned, the implementation checks the actual block map again.

This is important for the restart interpretation. The system already treats its progress summary as subordinate to a more current replica relation during ordinary execution.

Therefore restart-time loss/reconstruction of progress bookkeeping is not equivalent to loss of the authoritative preservation condition.

The bounded distinction is:

```text
working list of blockers
    != current actual block relation
    != final retirement authority
```

### H/P — a release regression test writes exclude intent, restarts the NameNode, and still completes decommission

`TestDecommission.testDecommissionWithNamenodeRestart()` supplies a direct release-level witness.

The test performs the following bounded sequence:

1. starts one NameNode and one DataNode;
2. writes a file at replication factor 1;
3. records the first DataNode's identity/address;
4. writes that DataNode address into the configured exclude file;
5. starts a second DataNode;
6. restarts the NameNode;
7. obtains the original DataNode descriptor from the restarted NameNode;
8. waits until it reaches `AdminStates.DECOMMISSIONED`;
9. asserts that both DataNodes remain alive;
10. checks that the file has the expected replica relation after decommission.

The sequence is especially useful because the test writes the exclude file and then relies on **NameNode restart**, rather than first calling the test helper's ordinary `refreshNodes()` path on the old NameNode.

The test therefore supports this bounded product/source-level claim:

> **In Hadoop 2.7.3's tested path, an exclusion written before NameNode restart can be imported by the restarted NameNode and drive decommission to completion after restart.**

The test does not prove arbitrary crash/torn-write behavior for the exclude file itself, and it does not prove that every intermediate progress datum survives.

### H/P — decommission completion after restart still depends on post-restart storage evidence

The same regression test starts a second DataNode before the restart so that the original single-replica file can gain another embodiment while the first node is retired.

The ordinary `DecommissionManager` path remains responsible for evaluating sufficiency, and its final completion logic rechecks the actual block map rather than trusting the working blocker summary.

Thus the restart test is not evidence of a magical policy-only state transition:

```text
exclude file says retire node
    != enough replicas already exist
    != retirement can skip preservation checks
```

The configuration preserves the **obligation/intent**. Current block state still supplies the evidence needed to discharge that obligation safely.

---

## Engineering reconstruction

### E — a maintenance obligation can outlive the process that was executing it

The release-bounded mechanism supports the following reconstruction:

```text
operator writes exclude intent
    -> external host-policy representation survives

old NameNode process stops
    -> old Java progress collections disappear with it

new NameNode process starts
    -> host files are read into a fresh HostFileManager

DataNode registers / storage state is re-observed
    -> exclusion is evaluated again
    -> decommission transition is re-established

fresh DecommissionManager working state
    -> pending/tracked blockers are reconstructed by scanning
    -> preservation work proceeds

current block-map + health revalidation
    -> DECOMMISSIONED
```

The identity that crosses restart is therefore not the identity of a Java collection or monitor iteration. It is a relation reconstructed from more durable policy plus newly observed storage state.

### E — persistence horizon and authority are different axes

This case now exposes at least four control-state horizons:

| State/relation | Persistence horizon in this bounded path | Authority role |
| --- | --- | --- |
| include/exclude administrator intent | external to NameNode process; re-read by new manager | selects whether decommission should be in force |
| `pendingNodes` / `decomNodeBlocks` | process-local runtime state | accelerates/tracks maintenance work |
| DataNode/replica/block relation | re-observed/reconstructed after startup | supplies current preservation evidence |
| final decommission predicate | recomputed from current relation | authorizes retirement completion |

The table blocks a common shortcut:

> **more durable control state != more authoritative control state**.

The external exclude file survives the process and carries policy, but it does not prove replication sufficiency. The ephemeral progress map can help execute the policy, but it does not have final authority even while it exists.

### E — reconstructed progress is not a rollback of user payload

Losing a monitor queue or blocker cache on NameNode restart does not imply that DataNode block payloads have been reverted to an earlier version.

The relevant distinction is:

```text
maintenance-control progress representation lost/rebuilt
    != payload lost
    != payload rolled back
    != replica relation unchanged
```

Reconstruction can cost time and repeated scanning while still preserving correctness if the authoritative policy and current storage evidence remain available.

### E — continuity can reside in a rule plus re-observation rather than a checkpoint

The bounded restart path is not best described as `resume from exact maintenance checkpoint`.

It is closer to:

```text
retain the rule that work is required
    + re-observe enough of the world
    -> regenerate working state
    -> continue toward the same admissibility condition
```

This gives a useful project distinction:

> **maintenance obligation continuity != exact maintenance-progress continuity**.

### E — the restart boundary separates intent from proof

The exclude file answers roughly:

> Which node should cease ordinary service membership?

The block/placement/health relation answers:

> Is it safe to declare that withdrawal complete now?

Those are different technical questions, carried by different state.

Therefore:

```text
retained intent
    != retained proof of completion
```

and:

```text
policy re-import
    != retirement completion
```

### E — re-execution can be a valid retention strategy for derived control state

If a state is derivable from surviving authoritative inputs and current observations, preserving that state byte-for-byte across restart may be unnecessary.

Case 80 provides a bounded example:

- the old progress map can disappear;
- exclusion intent can be re-imported;
- DataNode/block state can be re-observed;
- a new progress map can be built;
- final authority can be recomputed.

This does not mean rebuilding is free. It can repeat scans, lose monotonic progress accounting, or delay completion. The claim is about correctness/continuity of the maintenance relation, not zero restart cost.

---

## Functional comparisons — explicitly not genealogy

### A — Case 79 HDFS startup SafeMode

Case 79 and this addendum both make startup/restart a re-observation problem, but the retained obligations differ.

Case 79 asks when the restarted NameNode has observed enough replicas to leave startup SafeMode and resume ordinary cluster action.

This Case-80 deepening asks how a separately retained **operator withdrawal intent** can be re-imported and then discharged against newly reconstructed replica knowledge.

So:

```text
startup inventory confidence
    != decommission policy persistence
    != decommission completion
```

The comparison stays inside HDFS but does not claim the same state machine.

### A — Case 145 JFFS2 mount-time classification reconstruction

Case 145 shows volatile allocator/block classifications reconstructed after restart from more persistent on-flash evidence.

Case 80 similarly shows a runtime maintenance classification/progress structure that need not be preserved as the same in-memory object if surviving policy and re-observable system state can regenerate the operational relation.

The common function is only:

```text
volatile derived state disappears
    + stronger surviving evidence remains
    -> derived operational state can be rebuilt
```

There is no filesystem-to-HDFS genealogy claim, and the evidence carriers are radically different.

### A — Case 152 SQLite WAL checkpoint progress

Case 152 distinguishes authoritative committed WAL evidence from restart-reconstructible checkpoint-progress state.

Case 80 supplies a distributed-maintenance analogue at the relation level:

```text
maintenance progress checkpoint/cache
    != authoritative reason the obligation exists
    != authoritative current condition for declaring it complete
```

This is a functional analogy only. Hadoop decommission is not a database WAL protocol.

---

## Philosophical interpretation — bounded

### I — continuity of an obligation need not be continuity of an executor state

The technical fact is precise: a NameNode process can disappear together with its runtime progress collections while an externally represented exclusion policy remains, after which a new process can re-import the policy, re-observe the storage relation, and recreate the work needed to finish retirement.

A bounded conceptual reading is:

> **what persists can be an obligation-producing relation rather than an uninterrupted internal process state.**

That makes retention here less like preserving one frozen control image and more like preserving enough normative/technical relation for a later executor to reproduce the required action.

This interpretation stops at the mechanism. It does not turn `dfs.hosts.exclude` into a philosophical archive, does not identify administrator intent with human memory, and does not claim that every resilient system should prefer reconstruction over checkpoints.

### I — forgetting dependence can itself require remembered policy

Case 80 already frames decommission as forgetting dependence on one embodiment only after sufficient preservation elsewhere.

The restart boundary adds a further condition: the system may need to remember **that it intended to stop depending on that embodiment** even when the process performing the withdrawal is replaced.

Thus the technical act of retiring one relation can depend on retaining another relation long enough for the retirement to be safely completed.

---

## Explicit non-claims

1. This addendum does **not** claim Hadoop 2.7.3 invented restart-safe decommissioning.
2. It does **not** claim `dfs.hosts.exclude` is stored in HDFS namespace fsimage or edit logs.
3. It does **not** claim the exclude file is automatically replicated, journaled, atomically replaced, or power-fail safe by HDFS.
4. It does **not** claim every `DatanodeInfo.AdminState` value is durably serialized and restored as the same object across NameNode restart.
5. It does **not** claim `pendingNodes` survives restart.
6. It does **not** claim `decomNodeBlocks` survives restart.
7. It does **not** claim the decommission monitor's iterator/cursor survives restart.
8. It does **not** claim the old monotonic decommission start time survives with identical semantics.
9. It does **not** claim losing process-local progress bookkeeping is consequence-free; re-scanning can cost time/work.
10. It does **not** claim the externally retained policy is sufficient evidence that replication/placement is safe.
11. It does **not** claim a node can be marked decommissioned after restart without current block/health evaluation.
12. It does **not** claim DataNode payload blocks are recreated from the exclude file.
13. It does **not** claim NameNode restart rolls back or rewrites DataNode payload.
14. It does **not** claim the regression test covers an exclude-file torn write or filesystem corruption.
15. It does **not** claim the regression test simulates arbitrary machine power loss during every decommission interleaving.
16. It does **not** claim the tested single-NameNode path defines HA Standby/Active restart semantics.
17. It does **not** claim federation shares one automatically durable exclusion representation across all NameNodes.
18. It does **not** claim later HDFS maintenance mode (Case 116) uses the same persistence/reconstruction rules.
19. It does **not** claim decommission completion erases bytes from the retired DataNode.
20. It does **not** claim `DECOMMISSIONED` is equivalent to secure deletion or sanitization.
21. It does **not** claim an exclude entry proves the target DataNode is alive, healthy, or reachable.
22. It does **not** claim re-registration alone proves the full block inventory is current.
23. It does **not** claim the working blocker map and actual block map are interchangeable.
24. It does **not** claim the Case 145 or Case 152 comparisons establish genealogy or shared implementation.
25. It does **not** generalize the exact 2.7.3 constructor/registration path to all Hadoop releases.

---

## Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| Hadoop 2.7.3 constructs a fresh `HostFileManager` and refreshes it from configured include/exclude files during `DatanodeManager` construction | H/P | direct exact-release source |
| running `refreshNodes` re-reads host configuration and maps exclusion to decommission / removal from exclusion to stop-decommission | H/P | direct exact-release source |
| DataNode registration calls `startDecommissioningIfExcluded` | H/P | direct exact-release source |
| an excluded registering DataNode can have decommission re-applied by the new NameNode-side manager | H/P | direct exact-release source/control-flow reconstruction |
| `DecommissionManager` allocates fresh `decomNodeBlocks` and `pendingNodes` collections in its constructor | H/P | direct exact-release source |
| `startDecommission` records runtime start/progress state and adds an in-progress node to `pendingNodes` | H/P | direct exact-release source |
| `decomNodeBlocks` is documented as potentially stale and final retirement rechecks the actual block map | H/P | direct exact-release source |
| `testDecommissionWithNamenodeRestart` writes an exclude entry before NameNode restart and expects the excluded node to become decommissioned afterward | H/P | direct exact-release regression test |
| the same regression test adds another DataNode and verifies the file replica relation after decommission | H/P | direct exact-release regression test |
| decommission intent can survive process restart without preserving the same progress collections | E | bounded reconstruction from constructor/registration/test relation |
| maintenance-obligation continuity != exact maintenance-progress continuity | E | bounded reconstruction |
| externally retained policy != proof of retirement safety | E | bounded reconstruction |
| process-local progress cache != final retirement authority | E | bounded reconstruction |
| derived maintenance state can be rebuilt from retained policy plus current observations | E | bounded reconstruction |
| loss/rebuild of maintenance progress != payload rollback | E | bounded negative reconstruction |
| restart may repeat work without invalidating the preservation relation | E | bounded reconstruction; performance magnitude unmeasured |
| Case 145 / Case 152 comparisons are functional only | A | explicitly non-genealogical |
| continuity of obligation can survive discontinuity of executor state | I | bounded philosophical interpretation from exact mechanism |

---

## Remaining evidence debt

This slice closes only the bounded 2.7.3 restart/reconstruction seam. Useful future work remains:

1. **HA Active/Standby restart and failover:** inspect exactly how host-exclusion configuration is distributed/reloaded and how decommission work is re-established on role changes, without merging that with the single-NameNode test here.
2. **Federation:** determine the operational/durability assumptions for keeping exclusion files consistent across independent NameNodes.
3. **Configuration-file durability:** if historically important, inspect how operators/distributions wrote and distributed `dfs.hosts.exclude`; that is an administration/filesystem question, not established by this source alone.
4. **Precise restart phase ordering:** trace registration, initial block reports, replication queues, and decommission scans under controlled delayed-report interleavings.
5. **Progress-cost validation:** measure how much decommission scan work is repeated after restart under large blocker sets; correctness and restart cost are separate claims.
6. **Later-version evolution:** compare newer HDFS decommission and maintenance-state restart handling only as explicitly versioned slices.
7. **Production evidence:** named-cluster incident/operations evidence could test whether configuration drift or delayed inventory ever caused practical decommission-reconstruction problems.

None of these is required to retain Case 80's current `grounded` maturity. The new result is narrower: **the 2.7.3 release source and its regression test directly separate externally retained decommission intent, reconstructible runtime progress, and revalidated current storage evidence across a NameNode restart.**

---

## Summary

The restart boundary turns Case 80 into a sharper maintenance-control-state example.

Hadoop 2.7.3 does not need the old NameNode process to preserve its `DecommissionManager` Java collections byte-for-byte in order for the decommission obligation to continue. The new `DatanodeManager` reloads host include/exclude configuration; DataNode registration re-evaluates exclusion; a fresh `DecommissionManager` constructs new runtime progress structures; and final retirement remains tied to current block/health evidence rather than to the old progress cache.

The bounded relation is:

```text
retained administrator intent
    + re-observable storage state
    -> reconstructed maintenance work
    -> current proof of preservation
    -> renewed retirement authority
```

Therefore:

> **a maintenance obligation can survive a process restart even when its transient progress representation does not; what must persist is enough authoritative policy and recoverable world-state to reconstruct the obligation and re-prove its completion condition.**
