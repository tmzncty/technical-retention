# Apache HDFS DataNode Decommissioning: Administrative Retirement, Replication Drain, and Recommission

## Scope

- **Bounded historical/technical regime:** HDFS administrative decommissioning as documented in Hadoop 0.18-era architecture material, Hadoop 1.0.4 administration documentation, the Hadoop 2.7.0 decommission-manager refactor record, and exact Hadoop 2.7.3 source.
- **Primary question:** what must remain, be copied, and be re-checked before an otherwise surviving storage node may stop counting as an ordinary in-service embodiment of replicated HDFS blocks?
- **Retention-specific focus:** administrative exclusion, `DECOMMISSION_INPROGRESS`, replication work before retirement, final full-map verification, health qualification, and recommission cleanup.
- **Excluded from this case:** a general HDFS history; generic cluster expansion; balancing; HDFS erasure coding; storage-media sanitization; node hardware replacement procedure; or invention priority for graceful node draining.

This case is deliberately adjacent to Case 79 but asks the inverse operational question. Case 79 studies how a restarted NameNode **re-observes surviving replicas before acting on an incomplete inventory**. Case 80 studies how HDFS **intentionally withdraws one still-existing DataNode from service only after enough other embodiments satisfy a bounded replication condition**.

---

## Historical vocabulary

The primary HDFS sources use terms including:

- `Decommission DataNode`;
- `Recommission or decommission DataNode(s)`;
- `dfs.hosts` / `dfs.hosts.exclude`;
- `DECOMMISSION_INPROGRESS` / `Decommission In Progress`;
- `DECOMMISSIONED` / `Decommissioned`;
- `In Service`;
- `sufficiently replicated`;
- `under-replicated` / `insufficiently replicated`;
- `decommissioning`;
- `replication`;
- `Blockreport`;
- `Heartbeat`;
- `refreshNodes`.

The following are **project engineering terms**, not historical quotations from the sources:

- `administrative retirement`;
- `replication drain`;
- `withdrawal authority`;
- `retirement admissibility`;
- `planned embodiment withdrawal`.

They are used only to expose retention relations across cases.

---

## Historical record

### H/P — HDFS exposed explicit DataNode decommissioning by the 0.18 documentation

The Hadoop 0.18 HDFS architecture document lists a DFSAdmin operation named `Decommission DataNode datanodename`, invoked as:

```text
bin/hadoop dfsadmin -decommission datanodename
```

This is useful as an early bounded witness because it shows that planned administrative withdrawal was already a named HDFS operation before the later `DecommissionManager` refactor studied below. It does **not** by itself establish the full internal state machine or invention priority.

**Primary source:** Apache Hadoop, release-0.18.0, *The Hadoop Distributed File System: Architecture and Design*, `DFSAdmin`: <https://github.com/apache/hadoop/blob/release-0.18.0/docs/hdfs_design.html>.

### H/P — later administrator intent is carried through include/exclude configuration plus `refreshNodes`

The Hadoop 1.0.4 HDFS Users Guide describes `dfsadmin -refreshNodes` as re-reading `dfs.hosts` and `dfs.hosts.exclude`. The resulting configured membership determines which hosts should be decommissioned and which already-marked hosts should have decommissioning stopped.

The exact wording in that historical guide has some awkward edge-case phrasing, so this case does not generalize every list-combination rule beyond the documented version. The important retention relation is narrower: **planned retirement is an explicit administrative/configuration state, not merely an inference that a machine stopped answering Heartbeats.**

**Primary source:** Apache Hadoop 1.0.4, *HDFS Users Guide*, `DFSAdmin Command`: <https://hadoop.apache.org/docs/r1.0.4/hdfs_user_guide.html>.

### H/P — Hadoop 2.7.3 separates liveness from a three-state administrative lifecycle

The exact Hadoop 2.7.3 `DatanodeInfo` source defines:

```text
NORMAL                  -> "In Service"
DECOMMISSION_INPROGRESS -> "Decommission In Progress"
DECOMMISSIONED          -> "Decommissioned"
```

That is a source-level reason not to collapse `node is alive`, `node is being retired`, and `node has completed retirement` into one binary predicate. A DataNode can remain a material/networked machine while its administrative relation to the storage service changes.

**Primary source:** Apache Hadoop 2.7.3 source, `DatanodeInfo.java`: <https://github.com/apache/hadoop/blob/branch-2.7.3/hadoop-hdfs-project/hadoop-hdfs-client/src/main/java/org/apache/hadoop/hdfs/protocol/DatanodeInfo.java>.

### H/P — 2.7.0 refactored an existing decommissioning mechanism rather than introducing the concept

The Apache 2.7.0 release notes record HDFS-7411 as `Refactor and improve decommissioning logic into DecommissionManager`, adding a blocks-per-interval throttle intended to make scan pauses more predictable.

This matters for historical restraint. The 2.7.3 class is an especially inspectable implementation witness, but the release note itself says **refactor and improve**; combined with the 0.18 documentation, it blocks any claim that Hadoop 2.7.x invented DataNode decommissioning.

**Primary/institutional source:** Apache Hadoop 2.7.0 release notes, HDFS-7411: <https://github.com/apache/hadoop/blob/trunk/hadoop-common-project/hadoop-common/src/site/markdown/release/2.7.0/RELEASENOTES.2.7.0.md>.

### H/P — live-node decommission completes only after block-sufficiency work and monitoring

The Hadoop 2.7.3 `DecommissionManager` class documentation explicitly separates two situations:

- a node that is already dead when decommission starts can be marked decommissioned immediately;
- a live node enters a decommission-in-progress state and is monitored until its blocks are `sufficiently replicated`.

The monitor retains a working set of block references that currently prevent completion. On an initial full scan it also schedules replication for under-replicated blocks when the replication queues are active. As those blocks become sufficiently replicated, the working set is pruned.

Thus planned retirement can create **proactive preservation work before withdrawal completes**. The old embodiment is not first discarded and then repaired merely as an accident of failure; the system can keep it present while arranging other acceptable replicas.

**Primary source:** Apache Hadoop 2.7.3 source, `DecommissionManager.java`: <https://github.com/apache/hadoop/blob/branch-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/DecommissionManager.java>.

### H/P — the progress list is not trusted as the final authority

The same source warns that the `decomNodeBlocks` map can become out of date because it is not updated by every block report or other event. Consequently, when the tracked blocker list reaches zero, the monitor performs another scan against the **actual block map** before finally marking the DataNode decommissioned.

Completion also requires `isNodeHealthyForDecommission(dn)`.

This gives a strong retention distinction:

> a convenient retained summary of outstanding work is not automatically authoritative proof that the preservation condition is satisfied now.

The summary accelerates progress checking; final retirement authority is gated by revalidation against a more current relation.

### H/P — `under-replicated` and `blocks decommission` are not identical predicates in this bounded release

`isSufficientlyReplicated` first accepts blocks whose live-replica count meets the expected replication factor and placement policy. But Hadoop 2.7.3 also has bounded exceptions: for the last block of an under-construction file, the code can permit decommission when at least `minReplication` live copies remain; for a non-under-construction block whose expected replication exceeds live replicas, the code can still regard it as sufficient for decommission once `defaultReplication` is met.

The correct historical claim is therefore release-specific:

> `under-replicated` does not mechanically imply `must block decommission` under every 2.7.3 code path.

This is not generalized into a timeless HDFS policy.

### H/P — decommission-in-progress death is treated differently from starting decommission on an already-dead node

The class-level comment states that a decommission-in-progress DataNode that becomes dead does **not** advance to decommissioned until it becomes live again, specifically to avoid potential durability loss for singly replicated blocks (HDFS-6791).

This apparently awkward distinction is important. `Administrative retirement complete` is not merely a synonym for `the source node is no longer reachable`; disappearance during a planned drain can reduce the evidence available to prove that the handoff is safe.

### H/P — recommission reverses administrative retirement and can create cleanup work

`stopDecommission` returns the node toward service through `HeartbeatManager`. If the node is alive, `processOverReplicatedBlocksOnReCommission(node)` is invoked. The manager also removes the node from pending/tracked decommission state.

This means recommission is not `restore payload from backup`. The old DataNode may still possess its replicas. In fact, replicas created elsewhere during decommission can make the recommissioned cluster **over-replicated**, creating a separate cleanup obligation.

---

## Retained state

At least five state classes should remain distinct.

### 1. User payload blocks

The bytes that HDFS must continue serving despite changes in which DataNodes embody them.

### 2. Replica-location and replica-count relation

The NameNode's working block map identifies where replicas are observed and how many live/decommissioning/decommissioned copies exist for a block. This relation is not the payload itself.

### 3. DataNode administrative state

`In Service`, `Decommission In Progress`, and `Decommissioned` qualify what the system is allowed to conclude or do about a node independently of simple liveness.

### 4. Administrative configuration / intent

The include/exclude configuration and `refreshNodes` path express operator-selected membership intent. They are distinct from heartbeat-derived reachability.

### 5. Decommission progress state

The monitor's current list/counters of insufficiently replicated blocks are working control state. They help schedule and bound maintenance but are explicitly revalidated before final retirement.

---

## Maintenance and transition

The bounded live-node path can be reconstructed as:

```text
in-service DataNode
    -> administrator marks node for decommission
    -> DECOMMISSION_INPROGRESS
    -> scan blocks on the node
    -> schedule replication where required
    -> retain/refresh a bounded blocker set
    -> blocker set reaches zero
    -> full block-map re-check + node-health check
    -> DECOMMISSIONED
```

A later policy change can instead produce:

```text
DECOMMISSION_INPROGRESS / DECOMMISSIONED
    -> stop decommission
    -> return node toward service
    -> detect/process any resulting over-replication
```

The first sequence is **not** claimed to describe every HDFS release or every modern maintenance mode. It is the documented 2.7.3 decommission path.

---

## Read, write, retirement, and forgetting

### Read/write service

This case does not attempt a complete client read-selection or write-placement audit for decommissioning nodes. The source-level claim is narrower: decommission state is a first-class administrative qualification consulted by HDFS block-management logic, and the node's blocks participate in sufficiency calculations during the transition.

### Retirement

`DECOMMISSIONED` is an administrative outcome, not evidence that the machine, disks, or block files have been physically destroyed. The inspected decommission manager reaches completion by state transition after replication/health checks; it does not establish secure media erasure.

### Forgetting

The safe objective is to forget **dependence on this node as an in-service embodiment**, not necessarily to erase every byte on that node at the moment decommission completes.

This gives a useful inversion of many deletion cases:

> preservation elsewhere can be the precondition for forgetting one embodiment's service role.

### Recommission

Stopping decommission can restore the node's administrative participation while leaving separately created replicas elsewhere. Any excess-replica cleanup is subsequent convergence work, not proof that the decommission process was mistaken.

---

## Engineering reconstruction

### E — physical survival does not guarantee continued service authority

A live DataNode and its local block files can persist while the administrative state moves through decommissioning. Material presence and membership/admissibility are separate relations.

### E — planned forgetting of one embodiment can require preservation work first

The system can replicate blocks away from a retiring live node before allowing retirement to complete. Forgetting dependence is therefore produced by maintenance, not merely by loss.

### E — progress metadata can be useful without being final authority

The tracked blocker list reduces repeated work, but its documented staleness requires a final full-block-map check. A retained summary can support maintenance while remaining epistemically subordinate to re-observation.

### E — retirement admissibility is relational

Whether a DataNode may finish decommissioning depends on the other replicas and placement/health conditions, not on an intrinsic property of the node alone.

### E — successful retirement is not the same as restored maximal redundancy under every intermediate predicate

The release-specific `sufficiently replicated` test is not a single equation with file replication factor in all cases. Administrative progress can depend on bounded safety thresholds distinct from the simple label `under-replicated`.

---

## Functional comparisons — not genealogy

### A — Case 79, HDFS startup SafeMode

Both cases delay potentially dangerous action while replica knowledge is incomplete or a preservation condition is not yet satisfied.

The direction differs:

- Case 79 **re-observes surviving embodiments after NameNode startup** before ordinary repair/mutation proceeds;
- Case 80 **intentionally withdraws one embodiment** while ensuring other replicas are sufficient before retirement completes.

`startup inventory confidence ≠ planned replica drain`.

### A — Case 05, RADOS repair

Both can create replacement replicas and restore a desired distributed retention relation. Case 05's bounded trigger is failure/membership-driven repair; Case 80's bounded trigger is an administrator's planned retirement of an HDFS DataNode. This is a functional comparison, not a genealogy claim.

### A — Case 73, GFS garbage collection

GFS lazy GC retires namespace/chunk references and eventually deletes orphaned/stale physical replicas. HDFS decommission instead preserves live blocks elsewhere so one node can leave service. `node-role retirement ≠ object deletion / garbage collection`.

### A — Case 51, HDFS DataNode command fencing

Case 51 asks which NameNode may issue block-changing commands after HA transitions. Case 80 asks whether a storage node has completed an administrator-driven withdrawal while sufficient block embodiments remain. `command-source authority ≠ storage-node administrative membership`.

### A — Case 14 / Case 78, defect-driven replacement

Disk/NAND defect management can preserve a logical address while retiring a failed physical sector/block. HDFS decommission also preserves higher-level block identity across embodiment changes, but its trigger is planned cluster administration rather than a local media defect. Again, similarity of continuity relation is not descent.

---

## Philosophical interpretation — bounded

### I — persistence can include an orderly right to withdraw support

This case complicates a picture in which retention is only the positive act of keeping copies. A distributed service also needs rules for when one supporting embodiment may cease to matter.

The technically grounded point is modest:

> **a system can make withdrawal from service conditional on prior preservation work and current evidence about the remaining embodiments.**

That may inform later analysis of availability, replaceability, or technical forgetting. It does not by itself establish a Heideggerian `Bestand` claim, and `decommissioned` is not a philosophical synonym for forgotten.

---

## Counterexamples and limits

- The sources do not establish that HDFS invented graceful storage-node decommissioning.
- The Hadoop 0.18 command proves an early named operation, not the exact later 2.7.3 state machine.
- The 1.0.4 include/exclude semantics should not be projected unchanged onto every later release.
- The 2.7.3 `sufficiently replicated` exceptions are release-specific and should not be normalized into a universal HDFS retirement rule.
- The inspected code does not establish that decommission completion securely erases local block data.
- Decommission is not equated with dead-node failure recovery, rack rebalancing, storage-volume removal, or modern HDFS maintenance state.
- The blocker list is explicitly allowed to become stale; it is not treated as a durable audit history.
- The case does not prove crash-persistence semantics for every transient `DecommissionManager` data structure.
- Recommission processing of over-replication establishes cleanup behavior in this source path, not an invariant that every recommission always deletes a replica.
- No claim is made about exact throughput, completion time, network volume, or operator labor for a named production cluster.

---

## Prior-art boundary

This case makes **no invention-priority claim** for planned storage-node retirement, graceful draining, replication before maintenance, or cluster membership administration.

The defensible historical statement is narrower:

> Hadoop 0.18-era documentation already exposed an explicit DataNode decommission operation; Hadoop 1.0.4 documentation tied later decommission/recommission intent to administrator-controlled host configuration; and Hadoop 2.7.3 source makes the retention relation inspectable as a monitored transition in which a live node remains `DECOMMISSION_INPROGRESS` while insufficient replicas are scheduled/checked, followed by a full-map and health revalidation before `DECOMMISSIONED`.

The `computing-archaeology` repository was searched for a dedicated HDFS DataNode-decommission slice before writing this case; no directly reusable treatment was found. A broader history of cluster draining, storage-node maintenance, and membership protocols belongs there if developed later.

---

## Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| HDFS documented an explicit DataNode decommission operation by release 0.18 | H/P | grounded in Apache release documentation |
| Hadoop 1.0.4 `refreshNodes` re-read include/exclude configuration to drive decommission/recommission decisions | H/P | grounded in Apache user guide |
| Hadoop 2.7.3 exposes `In Service`, `Decommission In Progress`, and `Decommissioned` administrative states | H/P | grounded in exact release source |
| live-node decommission schedules/checks replication before final retirement | H/P | grounded in `DecommissionManager` |
| the tracked blocker list may be stale and is rechecked against the actual block map before completion | H/P | grounded in source comment/control flow |
| final completion also checks node health | H/P | grounded in source |
| a decommission-in-progress node that becomes dead does not automatically finish retirement in the bounded source | H/P | grounded in class documentation |
| recommission can trigger over-replication processing | H/P | grounded in `stopDecommission` |
| physical DataNode survival ≠ continued in-service authority | E | bounded reconstruction |
| decommission request ≠ completed retirement | E | bounded reconstruction |
| planned embodiment withdrawal can require proactive preservation work | E | bounded reconstruction |
| progress summary ≠ final retirement authority | E | bounded reconstruction |
| decommission ≠ secure sanitization | E | bounded negative claim |
| HDFS decommission ≈ failure repair / media reassignment only functionally | A | explicitly non-genealogical comparison |

---

## Summary

HDFS DataNode decommissioning adds a retention regime in which the object being removed is not necessarily the payload but **one embodiment's right/obligation to remain part of the serving redundancy set**.

The bounded 2.7.3 implementation is especially revealing because it refuses a one-step equation `administrator excludes node -> node is gone`. A live DataNode first becomes `DECOMMISSION_INPROGRESS`; its blocks are scanned, replication work may be scheduled, a bounded blocker set is maintained, and even a zero blocker set is revalidated against the current full block map and node health before the node becomes `DECOMMISSIONED`.

Therefore:

> **planned embodiment withdrawal can itself be retention work: the system preserves enough elsewhere before it authorizes itself to stop depending on here.**
