# Evidence 79B — Hadoop Manual SafeMode Process Lifetime vs Startup Reinitialization (2008–2016)

## Status

**`bounded deepening complete`**.

This record deepens [`../cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md`](../cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md) around one narrow retention question:

> When an operator manually places a running HDFS NameNode into SafeMode, is that manual admission state itself the same kind of retained state as the namespace image/edit history that survives a NameNode restart?

For the bounded released implementations inspected here, the answer is **no**. Hadoop 0.18.0 and 2.7.3 both distinguish:

- a fresh **startup SafeMode** control object constructed during NameNode process initialization from configuration and startup state; and
- a **manual SafeMode** control object/state created or marked in a running process when the operator enters SafeMode.

The source therefore supports a narrow lifecycle boundary:

```text
durable namespace state
    !=
process-resident manual SafeMode state
    !=
fresh startup SafeMode state after restart
```

A restart does **not** imply unrestricted service. It substitutes the ordinary startup SafeMode/re-observation path for the prior process's manual SafeMode state. This is a control-state lifetime distinction, not a claim that operator intent is philosophically unimportant or that every Hadoop release has identical implementation details.

---

## Scope

This slice is intentionally small. It asks only:

1. how released Hadoop 0.18.0 represents startup versus manual SafeMode;
2. how released Hadoop 2.7.3 represents the same distinction;
3. what the exact process-start paths imply about the persistence horizon of manual SafeMode state;
4. why edit-log synchronization performed around manual entry must not be misread as proof that the manual SafeMode flag itself is a durable namespace edit.

It does **not** attempt to reconstruct:

- every SafeMode implementation before 0.18.0 or after 2.7.3;
- HA active/standby propagation of operator SafeMode intent;
- every `hdfs dfsadmin -safemode` CLI variation;
- later force-exit semantics;
- NameNode recovery mode in general;
- the complete edit-log opcode history;
- distributed-filesystem safe-startup genealogy;
- operational policy for production clusters.

Those are separate slices.

---

## Source custody and inspection boundary

### Primary source A — Apache Hadoop `release-0.18.0`

Directly inspected released source:

- Apache Hadoop, `release-0.18.0`, `src/hdfs/org/apache/hadoop/dfs/FSNamesystem.java`:
  <https://github.com/apache/hadoop/blob/release-0.18.0/src/hdfs/org/apache/hadoop/dfs/FSNamesystem.java>

Apache's release record dates Hadoop 0.18.0 to **22 August 2008**:

- <https://hadoop.apache.org/release/0.18.0.html>

Relevant inspected implementation anchors:

- startup `initialize(...)` loads the namespace image and then assigns `this.safeMode = new SafeModeInfo(conf)`;
- the configuration-taking `SafeModeInfo(Configuration)` constructor is the automatic/startup form;
- `SAFEMODE_ENTER` calls `enterSafeMode()`;
- `enterSafeMode()` is explicitly documented as manual entry and assigns `safeMode = new SafeModeInfo()` if SafeMode is not already on;
- the no-argument constructor is explicitly documented as the manual SafeMode form and uses unreachable automatic-exit values, including a threshold of `1.5` and negative block counters to distinguish the mode.

### Primary source B — Apache Hadoop `rel/release-2.7.3`

Directly inspected released source:

- Apache Hadoop, `rel/release-2.7.3`, `hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.java`:
  <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.java>

Relevant inspected implementation anchors:

- `SafeModeInfo(Configuration conf)` is documented as creating automatic SafeMode at NameNode startup;
- NameNode/FSNamesystem initialization creates a new `SafeModeInfo(conf)`;
- `SafeModeInfo(boolean resourcesLow)` is the manual-or-low-resource form and uses values that cannot satisfy the automatic startup exit condition;
- `enterSafeMode(boolean resourcesLow)` creates a new `SafeModeInfo(resourcesLow)` when SafeMode is not already active, or marks the existing object manual/low-resource when appropriate;
- before/around manual entry, when the edit log is open for write, `logSyncAll()` is used to ensure concurrent namespace operations are synced.

This record uses those exact released-source paths as positive evidence. It does **not** infer undocumented on-disk state from class names alone.

---

## Historical record

### H/P — Hadoop 0.18.0 reconstructs startup SafeMode instead of deserializing a prior manual SafeMode object

The 0.18.0 `FSNamesystem.initialize(...)` path has an important ordering. It loads the namespace image and then creates:

```java
this.safeMode = new SafeModeInfo(conf);
setBlockTotal();
```

The same file distinguishes this configuration-taking constructor from a separate no-argument constructor used for manual SafeMode.

The bounded historical statement is therefore:

> **In released Hadoop 0.18.0, a new NameNode process creates a new startup `SafeModeInfo` from configuration/startup state; the process does not resume by restoring the prior process's manual `SafeModeInfo` object.**

This does not prove a general law about all HDFS control state. It is one exact released implementation path.

### H/P — manual SafeMode in 0.18.0 is separately instantiated in the running process

The same source makes manual entry explicit. `SAFEMODE_ENTER` calls `enterSafeMode()`, whose source comment says `Enter safe mode manually`. If SafeMode is not already active, the method assigns:

```java
safeMode = new SafeModeInfo();
```

The no-argument constructor is likewise explicitly documented as creating `SafeModeInfo` when SafeMode is entered manually. Its deliberately unreachable automatic threshold and sentinel block counts distinguish it from startup progress accounting.

Thus, by 0.18.0, `SafeMode` is already one public/service-state name covering at least two control-state provenances:

```text
startup
    -> SafeModeInfo(Configuration)

manual operator entry
    -> SafeModeInfo()
```

The source itself, not later reconstruction, establishes that implementation split.

### H/P — 2.7.3 preserves the startup/manual lifecycle distinction

Released Hadoop 2.7.3 retains the same broad separation with a somewhat evolved implementation.

Its `SafeModeInfo(Configuration conf)` constructor is explicitly the startup automatic form. The class documentation says startup SafeMode counts safe blocks and uses threshold/extension conditions to decide when automatic exit becomes possible.

Manual/low-resource SafeMode is represented through `SafeModeInfo(boolean resourcesLow)`. That constructor deliberately chooses values that cannot satisfy the automatic startup condition: the threshold is set above one, the DataNode and extension thresholds are made unreachable, and the safe-replication value is set beyond normal replication limits.

The public control path remains separate from startup construction. `enterSafeMode(boolean resourcesLow)` creates the manual/low-resource form if no SafeMode is currently active, or marks an already-active SafeMode as manual/low-resource.

Therefore:

> **The startup/manual distinction is not an artifact of one 2008 snapshot; it remains explicit in the bounded 2.7.3 source.**

This is continuity evidence only. It is not a claim that every intermediate release has identical fields, defaults, or state transitions.

### H/P — 2.7.3 syncs namespace edits around manual entry

The 2.7.3 `enterSafeMode(boolean resourcesLow)` method performs `logSyncAll()` when the edit log is open for writing. The source comment explains the reason: concurrent operations should be fully synced so the FSImage/namespace state is stable on disk as SafeMode is entered.

This is important positive evidence for a different relation:

```text
manual admission boundary
    -> synchronize prior/concurrent namespace edit state
```

It is **not**, by itself, evidence for:

```text
manual SafeMode flag
    -> durable SafeMode edit record
```

The inspected path shows the SafeMode state being created/marked in `FSNamesystem` memory and the namespace edit stream being synchronized. Those are two different effects.

A stronger claim that no other part of every supported Hadoop release ever persisted SafeMode intent would require a broader opcode/image-schema audit and is not made here.

---

## Engineering reconstruction

### E — admission policy can have a shorter lifetime than the namespace it constrains

The bounded source family exposes at least three state classes with different lifetimes:

1. **durable namespace state** — checkpoint/image plus edit history used to reconstruct namespace state;
2. **startup SafeMode control/progress state** — freshly created for a NameNode startup and advanced by re-observation/progress conditions;
3. **manual SafeMode state** — operator-imposed process control state used to keep mutation/service restrictions in place independent of the automatic startup threshold.

A useful retention decomposition is therefore:

```text
namespace survives restart
    !=
manual admission policy survives restart as the same control state
```

and:

```text
old process in manual SafeMode
    -> process ends
    -> new NameNode constructs startup SafeMode
    -> startup evidence/threshold logic applies
```

The second chain is an engineering reconstruction from the directly inspected construction paths. It does not claim anything about administrator intent outside the process or about external automation that might re-enter manual SafeMode after restart.

### E — restart reinitialization is not equivalent to “SafeMode forgotten and service opened”

A simplistic description would say that manual SafeMode is “lost on restart.” That is incomplete because a newly starting NameNode itself enters startup SafeMode.

The more precise relation is:

> **manual SafeMode continuity is broken, but admission restriction is re-established under a different startup provenance and exit condition.**

Thus:

```text
manual SafeMode not restored
    !=
NameNode immediately writable after restart
```

The user-visible name can remain `SafeMode` while the underlying reason for being in that state has changed.

### E — same state label does not imply same state history

Both modes can cause the NameNode to report itself as being in SafeMode, but the state was produced differently:

```text
startup SafeMode
    provenance = process startup + configured threshold/progress logic

manual SafeMode
    provenance = operator control action in a running process
```

Therefore:

> **same service-state label ≠ same provenance ≠ same exit rule ≠ same persistence horizon.**

This is directly relevant to technical retention because a stable label can hide a replacement of the control state that justifies the label.

### E — syncing durable state at a control boundary is not the same as persisting the boundary condition

The 2.7.3 `logSyncAll()` calls show that a control transition can deliberately strengthen durability of one state class without making the control transition itself part of that same persistent state class.

Bounded reconstruction:

```text
enter manual SafeMode
    -> ensure preceding namespace edits are synced
    -> establish/mark in-process admission state
```

So:

> **durability barrier for namespace edits ≠ durable encoding of manual SafeMode intent.**

This distinction prevents a common category error in which every operation that causes a flush is treated as if the operation's own control state were thereby journaled.

### E — re-observed inventory and manual admission policy are different restart problems

Case 79 already establishes that block-location state can be reconstructed from DataNode reports after restart. The present deepening adds a counterpoint: manual SafeMode is not reconstructed by those reports.

```text
block-location relation
    -> re-derived from distributed inventory evidence

manual SafeMode intent
    -> not re-derived from block reports
```

The same restart can therefore contain both:

- **reconstruction of an operational relation**, and
- **replacement of a previous process-local policy state with a fresh startup state**.

Not every volatile state needs the same recovery mechanism.

---

## Functional comparison — bounded

### A — relation to Case 05 RADOS restart map context

Case 05 shows a different retention choice: persisted map/superblock/PG evidence is used after restart to re-establish placement/history context, followed by reconciliation with newer map state.

Case 79's manual SafeMode state is a useful counterexample. It is not treated as another durable restart context. A new startup SafeMode is constructed instead.

The bounded comparison is:

> **some control state is worth retaining as restart evidence; other control state can be safely reinitialized when the system has an independent startup gate.**

This is a functional comparison only. HDFS SafeMode is not historically derived from Ceph OSDMap persistence, and the mechanisms solve different problems.

### A — relation to Case 116 maintenance mode

Case 116 separately treats temporary DataNode maintenance state and expiry. Case 79's manual SafeMode is NameNode-wide operator admission control. Sharing the broad idea of an operator-imposed restricted mode does not make their scope, lifetime, or persistence semantics identical.

Therefore:

> **operator-imposed restriction ≠ one universal persistence contract.**

---

## Philosophical interpretation — bounded

The exact technical pressure is narrow:

> A durable object can outlive a policy state that temporarily restricted what could be done to that object, while a later process reinstates a different restriction for a different reason.

This clarifies one limit of object-centered talk about persistence. What survives is not necessarily every contemporaneous authority relation or operator decision that surrounded the object.

The conceptual contribution stops there. It does **not** justify describing a process restart as institutional forgetting, treating SafeMode as human memory, or inferring a general philosophy in which policies are less real than data. In this bounded implementation, their **persistence contracts differ**; that is the technical fact.

---

## Explicit non-claims

This evidence does **not** establish that:

1. manual SafeMode was first introduced in Hadoop 0.18.0;
2. every Hadoop release uses exactly the same constructor or sentinel values;
3. every later HDFS deployment loses all operator SafeMode intent at every restart boundary;
4. no wrapper, service manager, automation system, or administrator can re-enter manual SafeMode after restart;
5. the NameNode becomes writable immediately after a restart from manual SafeMode;
6. startup SafeMode and manual SafeMode have identical exit conditions;
7. `logSyncAll()` journals the manual SafeMode flag;
8. `logSyncAll()` proves lower-device stable-media durability under every hardware failure;
9. manual SafeMode is a transaction commit protocol;
10. SafeMode is itself payload retention;
11. block reports reconstruct manual policy state;
12. restart destroys the HDFS namespace merely because manual SafeMode state is reinitialized;
13. SafeMode protects against every form of corruption or Byzantine report;
14. an HA standby necessarily shares an active node's manual SafeMode state in the same way;
15. this bounded lifecycle proves invention priority for safe startup/read-only recovery modes;
16. HDFS and Ceph have one common historical control-state lineage.

---

## Claim ledger

| Claim | Layer | Support / boundary |
| --- | --- | --- |
| Hadoop 0.18.0 startup loads namespace state and then creates `SafeModeInfo(conf)` | `H/P` | exact `release-0.18.0` `FSNamesystem.java` |
| Hadoop 0.18.0 manual `SAFEMODE_ENTER` uses a separate manual `SafeModeInfo()` path | `H/P` | exact `release-0.18.0` `FSNamesystem.java` |
| Hadoop 2.7.3 still distinguishes automatic-startup `SafeModeInfo(conf)` from manual/low-resource `SafeModeInfo(boolean)` | `H/P` | exact `rel/release-2.7.3` `FSNamesystem.java` |
| 2.7.3 syncs the edit log around manual entry when it is open for writing | `H/P` | exact `enterSafeMode(boolean)` implementation |
| a fresh bounded NameNode process does not resume the previous process's manual `SafeModeInfo`; it creates startup SafeMode state | `E` grounded in released source | positive startup-construction and manual-entry paths in 0.18.0 and 2.7.3 |
| manual SafeMode persistence horizon differs from durable namespace persistence horizon | `E` | lifecycle decomposition from the same paths |
| restart from manual SafeMode means immediate unrestricted service | `X` | contradicted by fresh startup SafeMode construction |
| edit-log synchronization proves manual SafeMode intent itself is journaled | `X` | the inspected path shows synchronization plus in-memory SafeMode mutation; it does not show a SafeMode edit record |
| block reports reconstruct manual SafeMode intent | `X` | block reports feed inventory/safe-block progress, not the manual-entry provenance |
| HDFS and Ceph share one historical control-state lineage | `X` | only bounded functional comparison is made |

---

## Remaining evidence debt

The following remain open and should not be smuggled into this slice:

- a release-by-release audit of manual SafeMode persistence semantics after 2.7.3;
- HA active/standby transitions while manual SafeMode is set;
- later force-exit and maintenance-related SafeMode changes;
- an exhaustive edit-log/fsimage schema audit for SafeMode-related state;
- empirical restart/fault-injection tests against named Hadoop releases;
- external cluster-management systems that may reapply operator policy after restart;
- the broader historical genealogy of startup/recovery restriction modes across distributed filesystems.

The last item belongs primarily in `tmzncty/computing-archaeology` if developed beyond this retention-specific seam. Fresh repository searches for `safemode` and `HDFS` did not surface a dedicated reusable packet there during this pass; the search API reported incomplete-result status, so this is recorded only as a routing check, not proof that no adjacent material can ever exist.

---

## Sources

### Primary released source

1. Apache Hadoop, **release 0.18.0 available**, 22 August 2008: <https://hadoop.apache.org/release/0.18.0.html>.
2. Apache Hadoop `release-0.18.0`, **`src/hdfs/org/apache/hadoop/dfs/FSNamesystem.java`**: <https://github.com/apache/hadoop/blob/release-0.18.0/src/hdfs/org/apache/hadoop/dfs/FSNamesystem.java>.
3. Apache Hadoop `rel/release-2.7.3`, **`hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.java`**: <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.java>.

### In-repository context

- [`../cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md`](../cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md) — canonical startup re-observation case.
- [`../cases/05-rados-replicated-object-repair.md`](../cases/05-rados-replicated-object-repair.md) — restart placement/map evidence as a bounded functional counterexample.
- [`../cases/116-apache-hdfs-datanode-maintenance-expiry.md`](../cases/116-apache-hdfs-datanode-maintenance-expiry.md) — separate per-DataNode maintenance-state scope/lifetime.

---

## Bounded result

For released Hadoop 0.18.0 and 2.7.3, the source supports this retention-specific conclusion:

```text
durable namespace / edit history
    survives process replacement through its own persistence path

manual SafeMode control state
    belongs to the running FSNamesystem control lifecycle

new NameNode process
    constructs fresh startup SafeMode state
    and re-establishes startup admission from configuration + observed progress
```

Therefore:

> **Retaining HDFS namespace identity does not require retaining every process-local admission policy with the same lifetime. A restart can replace manual control state with a newly constructed startup control regime while the durable namespace and DataNode payload embodiments continue through their separate retention paths.**
