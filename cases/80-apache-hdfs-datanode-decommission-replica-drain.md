# Apache HDFS DataNode Decommissioning: Administrative Retirement, Replication Drain, and Recommission

## Scope

- **Bounded historical/technical regime:** HDFS administrative decommissioning as documented in Hadoop 0.18-era architecture material, Hadoop 1.0.4 administration documentation, the Hadoop 2.7.0 decommission-manager refactor record, and exact Hadoop 2.7.3 source; the rack-placement deepening additionally inspects Hadoop 0.18 replica-placement documentation, Hadoop 2.7.3 `BlockPlacementPolicyDefault`, and GFS 2003 as an earlier prior-art floor.
- **Primary question:** what must remain, be copied, be topologically qualified, and be re-checked before an otherwise surviving storage node may stop counting as an ordinary in-service embodiment of replicated HDFS blocks?
- **Retention-specific focus:** administrative exclusion, `DECOMMISSION_INPROGRESS`, replication work before retirement, replica-count versus rack-placement sufficiency, final full-map verification, health qualification, and recommission cleanup.
- **Excluded from this case:** a general HDFS history; generic cluster expansion; balancing; HDFS erasure coding; storage-media sanitization; node hardware replacement procedure; or invention priority for graceful node draining/rack-aware storage.

Grounding records:

- [`../evidence/80-hadoop-2008-2016-datanode-decommission-grounding.md`](../evidence/80-hadoop-2008-2016-datanode-decommission-grounding.md)
- [`../evidence/80-hadoop-2003-2016-rack-placement-decommission-deepening.md`](../evidence/80-hadoop-2003-2016-rack-placement-decommission-deepening.md)

This case is deliberately adjacent to Case 79 but asks the inverse operational question. Case 79 studies how a restarted NameNode **re-observes surviving replicas before acting on an incomplete inventory**. Case 80 studies how HDFS **intentionally withdraws one still-existing DataNode from service only after enough other embodiments satisfy a bounded replication and placement condition**.

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
- `refreshNodes`;
- `rack-aware replica placement policy`;
- `BlockPlacementPolicyDefault`;
- `verifyBlockPlacement`;
- `network location` / rack location.

The following are **project engineering terms**, not historical quotations from the sources:

- `administrative retirement`;
- `replication drain`;
- `withdrawal authority`;
- `retirement admissibility`;
- `planned embodiment withdrawal`;
- `failure-domain diversity`;
- `topological qualification`.

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

`isSufficientlyReplicated` first accepts blocks whose live-replica count meets the expected replication factor **and** whose placement policy is satisfied. But Hadoop 2.7.3 also has bounded exceptions: for the last block of an under-construction file, the code can permit decommission when at least `minReplication` live copies remain; for a non-under-construction block whose expected replication exceeds live replicas, the code can still regard it as sufficient for decommission once `defaultReplication` is met.

The correct historical claim is therefore release-specific:

> `under-replicated` does not mechanically imply `must block decommission` under every 2.7.3 code path.

This is not generalized into a timeless HDFS policy.

### H/P — HDFS 0.18 explicitly separates replica count from rack distribution

The 0.18 architecture document calls replica placement critical to reliability and performance and says rack-aware placement aims to improve reliability, availability, and network bandwidth utilization.

It first describes putting replicas on unique racks as a `simple but non-optimal` policy: that protects against an entire rack failure and distributes read bandwidth, but increases cross-rack write traffic.

For the common replication-factor-three case, the same document instead places two replicas on different nodes of the local rack and the third on a different rack. It explicitly notes that only two unique racks are used.

Therefore, already in this bounded HDFS record:

> **replication factor ≠ rack diversity**

and:

> **maximal rack spread ≠ automatically preferred placement**.

**Primary source:** Apache Hadoop release-0.18.0 HDFS architecture, `Replica Placement: The First Baby Steps`: <https://github.com/apache/hadoop/blob/release-0.18.0/docs/hdfs_design.html>.

### H/P — Hadoop 2.7.3 keeps placement qualification separate from replica count

The exact `BlockPlacementPolicyDefault` source describes a factor-three target order that differs from the 0.18 documentation: first local when possible, second on a different rack, third on another node of the second replica's rack.

More importantly for Case 80, `verifyBlockPlacement` counts distinct rack network locations and, once the cluster has been multi-rack, uses:

```text
minRacks = min(2, numberOfReplicas)
```

as the bounded default minimum. Thus three replicas do not imply a three-rack requirement.

The same implementation constrains targets through a per-rack maximum and constructs rack-aware candidate groups when selecting excess replicas for deletion.

**Primary source:** Apache Hadoop 2.7.3 source, `BlockPlacementPolicyDefault.java`: <https://github.com/apache/hadoop/blob/branch-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/BlockPlacementPolicyDefault.java>.

This gives three separate relations:

> **live-replica count ≠ placement-policy satisfaction**;

> **placement-policy satisfaction ≠ maximal rack spread**;

> **over-replica deletion ≠ arbitrary copy deletion**.

### H/P — the exact factor-three target order changed between the inspected 0.18 and 2.7.3 records

The 0.18 architecture text describes `local rack + local rack + remote rack`; the 2.7.3 class comment/source describes `local + remote + same remote rack`.

Both yield a two-rack factor-three placement, but they are not the same target sequence. This is a useful historiographic guardrail:

> **same two-rack diversity objective ≠ same per-replica target order across releases**.

The project therefore keeps the two release records distinct rather than merging their mechanics into a timeless “HDFS policy.”

### H/P — decommission-in-progress death is treated differently from starting decommission on an already-dead node

The class-level comment states that a decommission-in-progress DataNode that becomes dead does **not** advance to decommissioned until it becomes live again, specifically to avoid potential durability loss for singly replicated blocks (HDFS-6791).

This apparently awkward distinction is important. `Administrative retirement complete` is not merely a synonym for `the source node is no longer reachable`; disappearance during a planned drain can reduce the evidence available to prove that the handoff is safe.

### H/P — recommission reverses administrative retirement and can create cleanup work

`stopDecommission` returns the node toward service through `HeartbeatManager`. If the node is alive, `processOverReplicatedBlocksOnReCommission(node)` is invoked. The manager also removes the node from pending/tracked decommission state.

This means recommission is not `restore payload from backup`. The old DataNode may still possess its replicas. In fact, replicas created elsewhere during decommission can make the recommissioned cluster **over-replicated**, creating a separate cleanup obligation whose candidate selection is itself topology-aware in the bounded placement-policy implementation.

---

## Retained state

At least seven state classes should remain distinct.

### 1. User payload blocks

The bytes that HDFS must continue serving despite changes in which DataNodes embody them.

### 2. Replica-location and replica-count relation

The NameNode's working block map identifies where replicas are observed and how many live/decommissioning/decommissioned copies exist for a block. This relation is not the payload itself.

### 3. Rack / network-topology relation

The placement policy uses DataNode network locations/racks to classify the topology of the surviving replicas. This failure-domain model is control state, not a second payload copy.

### 4. Placement-policy satisfaction

A block can have a live-replica count and separately have a placement result. The ordinary full-strength decommission success branch in 2.7.3 requires both enough live replicas and placement-policy satisfaction.

### 5. DataNode administrative state

`In Service`, `Decommission In Progress`, and `Decommissioned` qualify what the system is allowed to conclude or do about a node independently of simple liveness.

### 6. Administrative configuration / intent

The include/exclude configuration and `refreshNodes` path express operator-selected membership intent. They are distinct from heartbeat-derived reachability.

### 7. Decommission progress state

The monitor's current list/counters of insufficiently replicated blocks are working control state. They help schedule and bound maintenance but are explicitly revalidated before final retirement.

---

## Maintenance and transition

The bounded live-node path can be reconstructed as:

```text
in-service DataNode
    -> administrator marks node for decommission
    -> DECOMMISSION_INPROGRESS
    -> scan blocks on the node
    -> inspect live replicas + placement policy
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
    -> choose excess cleanup with topology-aware placement logic
```

The first sequence is **not** claimed to describe every HDFS release or every modern maintenance mode. It is the documented 2.7.3 decommission path.

---

## Read, write, retirement, and forgetting

### Read/write service

This case does not attempt a complete client read-selection or write-placement audit for decommissioning nodes. The source-level claim is narrower: decommission state is a first-class administrative qualification consulted by HDFS block-management logic, and the node's blocks participate in sufficiency calculations during the transition.

### Placement

A live-copy count is not the complete ordinary full-strength preservation predicate in the bounded 2.7.3 path. Placement policy evaluates the topological spread of replicas separately. Conversely, placement satisfaction does not require each replica to inhabit a unique rack.

### Retirement

`DECOMMISSIONED` is an administrative outcome, not evidence that the machine, disks, or block files have been physically destroyed. The inspected decommission manager reaches completion by state transition after replication/placement/health checks; it does not establish secure media erasure.

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

### E — replica multiplicity and failure-domain diversity are separate dimensions

Three replicas can satisfy a factor-three copy count while inhabiting only two racks in the bounded default policies. The number of embodiments and their distribution across correlated-failure domains are distinct retained relations.

### E — placement sufficiency is not maximal dispersion

The bounded 2.7.3 default verifier requires at least two racks once that topology exists; it does not require every replica to occupy a unique rack. More dispersion is therefore not synonymous with the exact admission predicate.

### E — successful retirement is not the same as restored maximal redundancy under every intermediate predicate

The release-specific `sufficiently replicated` test is not a single equation with file replication factor in all cases. Administrative progress can depend on bounded safety thresholds distinct from the simple label `under-replicated`.

### E — topology-aware cleanup is a second retention decision

When recommission or other events create excess copies, choosing which embodiment to retire can itself depend on rack distribution. Restoring the desired copy count and preserving an acceptable failure-domain geometry are separate but coupled tasks.

---

## Functional comparisons — not genealogy

### A — Case 79, HDFS startup SafeMode

Both cases delay potentially dangerous action while replica knowledge is incomplete or a preservation condition is not yet satisfied.

The direction differs:

- Case 79 **re-observes surviving embodiments after NameNode startup** before ordinary repair/mutation proceeds;
- Case 80 **intentionally withdraws one embodiment** while ensuring other replicas are sufficient before retirement completes.

`startup inventory confidence ≠ planned replica drain`.

### A — Case 05, RADOS repair

Both can create replacement replicas and restore a desired distributed retention relation, and both make physical placement relevant to survival. Case 05's CRUSH/PG mechanism and failure/membership-triggered repair remain historically distinct from HDFS rack-aware placement and operator-driven decommission. This is a functional comparison, not a genealogy claim.

### A — Cases 19 and 24, f4 / Windows Azure LRC

The coded-storage cases already separate algebraic fragment count/reconstructability from failure-domain placement. Case 80 supplies the replicated-storage counterpart:

> **copy count ≠ failure-domain placement**, just as **coded reconstructability ≠ failure-domain placement**.

No coding genealogy is implied.

### A — Case 83, HDFS block scanner

Rack placement says where replica embodiments are distributed. It does not establish that those embodiments have recently passed checksum verification.

`placement qualification ≠ integrity qualification`.

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

> **a system can make withdrawal from service conditional on prior preservation work and current evidence about both the number and placement of the remaining embodiments.**

That may inform later analysis of availability, replaceability, or technical forgetting. It does not by itself establish a Heideggerian `Bestand` claim, and `decommissioned` is not a philosophical synonym for forgotten.

---

## Counterexamples and limits

- The sources do not establish that HDFS invented graceful storage-node decommissioning.
- GFS 2003 is an earlier rack-placement mechanism floor, but chronology/function do not prove direct GFS→HDFS implementation genealogy.
- The Hadoop 0.18 command proves an early named operation, not the exact later 2.7.3 state machine.
- The Hadoop 0.18 factor-three rack order must not be projected onto 2.7.3; the inspected target sequences differ.
- The 1.0.4 include/exclude semantics should not be projected unchanged onto every later release.
- The 2.7.3 `sufficiently replicated` exceptions are release-specific and should not be normalized into a universal HDFS retirement rule.
- Replication factor does not by itself state rack diversity; conversely, the bounded default placement verifier does not require one unique rack per replica.
- Rack/network-location classification is an operational failure-domain model, not proof that every physical failure mode is independent across racks.
- Placement qualification does not prove checksum integrity, replica currentness, or writer/NameNode authority.
- The inspected code does not establish that decommission completion securely erases local block data.
- Decommission is not equated with dead-node failure recovery, rack rebalancing, storage-volume removal, or modern HDFS maintenance state.
- The blocker list is explicitly allowed to become stale; it is not treated as a durable audit history.
- The case does not prove crash-persistence semantics for every transient `DecommissionManager` data structure.
- Recommission processing of over-replication establishes cleanup behavior in this source path, not an invariant that every recommission always deletes a replica.
- The topology-aware excess-copy source path is not claimed to be globally optimal under every workload/failure model.
- No claim is made about exact throughput, completion time, network volume, or operator labor for a named production cluster.

---

## Prior-art boundary

This case makes **no invention-priority claim** for planned storage-node retirement, graceful draining, replication before maintenance, cluster membership administration, or rack-aware replica placement.

For decommissioning, the defensible historical statement remains:

> Hadoop 0.18-era documentation already exposed an explicit DataNode decommission operation; Hadoop 1.0.4 documentation tied later decommission/recommission intent to administrator-controlled host configuration; and Hadoop 2.7.3 source makes the retention relation inspectable as a monitored transition in which a live node remains `DECOMMISSION_INPROGRESS` while insufficient replicas are scheduled/checked, followed by a full-map and health revalidation before `DECOMMISSIONED`.

For rack-placement prior art, Ghemawat, Gobioff, and Leung's GFS 2003 paper explicitly says machine-level spreading is insufficient for its goal and that chunk replicas must also be spread across racks. This is an earlier distributed-filesystem mechanism floor than the bounded HDFS 0.18 record.

That permits the negative priority statement:

> **HDFS 0.18 rack-aware placement ≠ invention priority for cross-rack replica placement.**

But it does **not** establish:

> GFS implementation → HDFS implementation.

A real genealogy would require direct design/citation/code-history evidence rather than chronology plus functional similarity.

The `computing-archaeology` repository was searched for dedicated `HDFS rack replica placement` / `rack awareness` material before this deepening; no directly reusable treatment was found. A broader history of cluster placement, failure-domain modeling, draining, and membership protocols belongs there if developed later.

---

## Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| HDFS documented an explicit DataNode decommission operation by release 0.18 | H/P | grounded in Apache release documentation |
| Hadoop 1.0.4 `refreshNodes` re-read include/exclude configuration to drive decommission/recommission decisions | H/P | grounded in Apache user guide |
| Hadoop 2.7.3 exposes `In Service`, `Decommission In Progress`, and `Decommissioned` administrative states | H/P | grounded in exact release source |
| live-node decommission schedules/checks replication before final retirement | H/P | grounded in `DecommissionManager` |
| ordinary full-strength `isSufficientlyReplicated` checks both live count and placement-policy satisfaction | H/P | grounded in exact 2.7.3 source |
| Hadoop 0.18 factor-three placement intentionally uses two racks rather than three | H/P | grounded in release documentation |
| Hadoop 2.7.3 default placement verification separately counts racks and requires at least two in the bounded multi-rack path | H/P | grounded in exact source |
| HDFS 0.18 and 2.7.3 inspected factor-three target orders differ | H/P | grounded by release-bounded comparison |
| 2.7.3 target admission and excess-replica cleanup consult rack topology | H/P | grounded in exact `BlockPlacementPolicyDefault` source |
| the tracked blocker list may be stale and is rechecked against the actual block map before completion | H/P | grounded in source comment/control flow |
| final completion also checks node health | H/P | grounded in source |
| a decommission-in-progress node that becomes dead does not automatically finish retirement in the bounded source | H/P | grounded in class documentation |
| recommission can trigger over-replication processing | H/P | grounded in `stopDecommission` |
| GFS 2003 provides an earlier rack-aware distributed-filesystem placement floor | H/P | grounded in original SOSP paper |
| replica multiplicity ≠ failure-domain diversity | E | bounded reconstruction |
| live-replica count ≠ placement-policy satisfaction | E | bounded reconstruction |
| placement sufficiency ≠ maximal rack spread | E | bounded reconstruction |
| physical DataNode survival ≠ continued in-service authority | E | bounded reconstruction |
| decommission request ≠ completed retirement | E | bounded reconstruction |
| planned embodiment withdrawal can require proactive preservation work | E | bounded reconstruction |
| progress summary ≠ final retirement authority | E | bounded reconstruction |
| over-replica deletion ≠ arbitrary copy deletion | E | bounded reconstruction |
| placement qualification ≠ integrity/currentness qualification | E/A | cross-case boundary only |
| decommission ≠ secure sanitization | E | bounded negative claim |
| GFS rack placement ≠ demonstrated GFS→HDFS implementation genealogy | X | chronology/function insufficient for descent |
| HDFS decommission ≈ failure repair / media reassignment only functionally | A | explicitly non-genealogical comparison |

---

## Summary

HDFS DataNode decommissioning adds a retention regime in which the object being removed is not necessarily the payload but **one embodiment's right/obligation to remain part of the serving redundancy set**.

The bounded 2.7.3 implementation is especially revealing because it refuses a one-step equation `administrator excludes node -> node is gone`. A live DataNode first becomes `DECOMMISSION_INPROGRESS`; its blocks are scanned, replication work may be scheduled, a bounded blocker set is maintained, and even a zero blocker set is revalidated against the current full block map and node health before the node becomes `DECOMMISSIONED`.

The rack-placement deepening sharpens what “enough elsewhere” means. In the ordinary full-strength path, enough live replicas and acceptable placement are separate predicates. Three copies need not mean three racks; placement satisfaction need not mean maximal dispersion; and later excess-copy cleanup can itself be topology-aware. The 0.18/2.7.3 comparison also shows why the repository must keep release mechanics dated rather than silently fusing them into one timeless HDFS algorithm.

Therefore:

> **planned embodiment withdrawal can itself be retention work: the system preserves enough, in an admissible topology, before it authorizes itself to stop depending on here.**
