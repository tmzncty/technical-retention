from pathlib import Path
import subprocess

CASE_PATH = "cases/80-apache-hdfs-datanode-decommission-replica-drain.md"
EVIDENCE_PATH = "evidence/80-hadoop-2008-2016-datanode-decommission-grounding.md"
WORKFLOW_PATH = ".github/workflows/case80-integration.yml"
SCRIPT_PATH = "tools/integrate_case80.py"

case_text = r'''# Apache HDFS DataNode Decommissioning: Administrative Retirement, Replication Drain, and Recommission

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
'''

evidence_text = r'''# Case 80 grounding record — Apache HDFS DataNode decommissioning, 2008–2016

## Purpose

Ground Case 80's narrow retention claim: HDFS planned DataNode retirement is not merely node disappearance. In the bounded historical/source chain, administrative intent initiates a distinct decommissioning state, a live node can remain present while replication work is scheduled and checked, final retirement is revalidated against current block state and node health, and recommission can reverse the administrative transition without reconstructing payload from scratch.

This record separates:

- **historical record / primary evidence** from Apache documentation and exact source;
- **engineering reconstruction** about embodiment withdrawal and retention obligations;
- **functional analogy** to other repair/replacement cases;
- **prior-art limits** that block an HDFS-first claim.

---

## Source A — Hadoop release-0.18.0 HDFS architecture document

**Type:** Apache period/release documentation; primary institutional source.

**Artifact:** `docs/hdfs_design.html`, tag/ref `release-0.18.0`.

**URL:** <https://github.com/apache/hadoop/blob/release-0.18.0/docs/hdfs_design.html>

### Directly inspected evidence

In the `DFSAdmin` table, the document lists:

```text
Decommission DataNode datanodename
bin/hadoop dfsadmin -decommission datanodename
```

### Supports

- explicit HDFS administrative decommissioning existed as a named operation by the 0.18 documentation;
- later 2.7.x `DecommissionManager` is not the first evidence of the concept in HDFS.

### Does not support

- the exact 2.7.3 state machine;
- first invention of graceful node drain;
- a claim that the 0.18 implementation had every later safety condition.

---

## Source B — Hadoop 1.0.4 HDFS Users Guide

**Type:** Apache release documentation; primary institutional source.

**URL:** <https://hadoop.apache.org/docs/r1.0.4/hdfs_user_guide.html>

### Directly inspected evidence

The `DFSAdmin Command` section says `-refreshNodes`:

- updates hosts allowed to connect to the NameNode;
- re-reads `dfs.hosts` and `dfs.hosts.exclude`;
- uses the list state to cause decommissioning or to stop decommissioning for already-marked hosts.

### Supports

- administrative intent/configuration is distinct from heartbeat liveness;
- decommission can be reversible at the administrative-control layer;
- node-role change is not simply inferred from machine failure.

### Boundary

The guide's exact list-combination wording is version-specific and somewhat awkward. Case 80 uses it only for the existence of explicit configuration-driven decommission/recommission control, not as a universal modern HDFS truth table.

---

## Source C — Hadoop 2.7.0 release notes, HDFS-7411

**Type:** Apache release record; primary institutional source.

**URL:** <https://github.com/apache/hadoop/blob/trunk/hadoop-common-project/hadoop-common/src/site/markdown/release/2.7.0/RELEASENOTES.2.7.0.md>

### Directly inspected evidence

HDFS-7411 is titled:

```text
Refactor and improve decommissioning logic into DecommissionManager
```

The release note says the change introduced `dfs.namenode.decommission.blocks.per.interval`, replacing/deprecating the node-count throttle for more predictable scanning pauses.

### Supports

- `DecommissionManager` is a refactoring/improvement witness, not proof that the feature originated in 2.7;
- background scan work itself had operational cost significant enough to receive an explicit work-throttling control.

### Boundary

This case does not turn one performance-oriented release note into a full chronology of decommission internals.

---

## Source D — Hadoop 2.7.3 `DatanodeInfo.java`

**Type:** exact release source; primary implementation evidence.

**Path:** `hadoop-hdfs-project/hadoop-hdfs-client/src/main/java/org/apache/hadoop/hdfs/protocol/DatanodeInfo.java`

**URL:** <https://github.com/apache/hadoop/blob/branch-2.7.3/hadoop-hdfs-project/hadoop-hdfs-client/src/main/java/org/apache/hadoop/hdfs/protocol/DatanodeInfo.java>

### Directly inspected evidence

The `AdminStates` enum defines:

```text
NORMAL("In Service")
DECOMMISSION_INPROGRESS("Decommission In Progress")
DECOMMISSIONED("Decommissioned")
```

### Supports

- decommission is a multi-stage administrative state relation;
- liveness and administrative service state must not be collapsed conceptually.

### Does not support by itself

- the conditions under which the state transitions occur;
- client read-selection behavior from each state;
- persistence of the enum value across every crash/restart path.

---

## Source E — Hadoop 2.7.3 `DecommissionManager.java`

**Type:** exact release source; primary implementation evidence.

**Path:** `hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/DecommissionManager.java`

**URL:** <https://github.com/apache/hadoop/blob/branch-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/DecommissionManager.java>

### Directly inspected evidence — class contract

The class comment says:

- dead DataNodes can be decommissioned immediately when decommission starts;
- live DataNodes are decommissioned after their blocks are `sufficiently replicated`;
- they transition through a decommission-in-progress state monitored by a background thread;
- merely under-replicated blocks need not always block completion if the bounded threshold rule is met;
- a node already in decommission progress that becomes dead does not advance to decommissioned until it becomes live again, to prevent potential durability loss for singly replicated blocks.

### Directly inspected evidence — progress representation

`decomNodeBlocks` tracks references to blocks that currently prevent completion. The source comment explicitly warns the map can become out of date because block reports and other events do not update it directly. Before final retirement, the implementation rechecks the actual block map.

### Directly inspected evidence — start/stop transition

`startDecommission` calls `HeartbeatManager`, records start time for a live node, and queues it for monitor work.

`stopDecommission` reverses the state through `HeartbeatManager`, removes pending/tracked state, and for an alive node calls `processOverReplicatedBlocksOnReCommission(node)`.

### Directly inspected evidence — monitor and replication scheduling

For a newly tracked node, the monitor performs a full scan through its block list, schedules under-replicated blocks for replication when appropriate, and keeps the subset that is insufficiently replicated for decommission completion.

When the tracked list reaches zero on a later pass, the monitor performs another full block-map scan. It marks the node decommissioned only if that full scan is clean **and** `isNodeHealthyForDecommission(dn)` returns true.

### Directly inspected evidence — sufficiency is not a one-predicate synonym

`isSufficientlyReplicated` distinguishes:

- expected replication + placement-policy satisfaction;
- the last block of an under-construction file, where `minReplication` can be enough in the bounded path;
- non-under-construction blocks where `defaultReplication` can be enough even when expected replication is larger than the live count.

This grounds only a release-specific result:

> `under-replicated` and `blocks decommission` are not identical predicates in Hadoop 2.7.3.

---

## Source F — Hadoop 2.7.3 HDFS Architecture

**Type:** Apache release documentation; primary institutional source.

**URL:** <https://hadoop.apache.org/docs/r2.7.3/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html>

### Directly inspected evidence

The architecture document states that:

- the NameNode makes block-replication decisions;
- DataNodes send Heartbeats and Blockreports;
- absence of Heartbeats can cause a node to be marked dead and can trigger re-replication;
- `dfsadmin -refreshNodes` is the administrator action for recommissioning/decommissioning DataNodes.

### Supports

- planned administrative retirement and heartbeat-detected failure are different triggers even though both can affect replica maintenance;
- replication work sits under NameNode block-management authority.

### Boundary

The architecture page is used to contrast planned admin action with failure-triggered re-replication, not to claim every decommission implementation detail is documented there.

---

## Related-repository check

Before creating Case 80, `tmzncty/computing-archaeology` was searched for dedicated HDFS/DataNode/decommission material. No directly reusable treatment was found.

Therefore Case 80 keeps only the retention-specific decomposition here. A future broad history of cluster drain/maintenance should be built in `computing-archaeology` and linked back rather than duplicated.

---

## Grounded historical statements

The source chain supports these historical statements:

1. HDFS exposed an explicit DataNode decommission administrator operation by the 0.18 documentation.
2. Hadoop 1.0.4 documentation made decommission/recommission configuration-driven through host include/exclude state plus `refreshNodes`.
3. Hadoop 2.7.0 explicitly described its new `DecommissionManager` work as a refactor/improvement of existing decommissioning logic.
4. Hadoop 2.7.3 source distinguished `In Service`, `Decommission In Progress`, and `Decommissioned` administrative states.
5. For a live node, 2.7.3 decommissioning scanned blocks, scheduled replication where required, tracked insufficient blocks, and rechecked the full block map before final completion.
6. Final completion in the bounded source also required a node-health predicate.
7. A node dying *during* decommission-in-progress did not automatically count as successfully decommissioned.
8. Recommission could trigger over-replication processing.

---

## Engineering reconstruction supported by those statements

The following are project reconstructions, not Apache historical vocabulary:

- **physical DataNode survival ≠ continued in-service authority**;
- **decommission request ≠ completed retirement**;
- **planned retirement ≠ failure detection**;
- **replication drain ≠ payload deletion**;
- **replica creation before retirement ≠ only post-failure repair**;
- **progress summary ≠ final authoritative proof**;
- **planned embodiment withdrawal can require preservation work before role forgetting**;
- **recommission ≠ restoration from backup**;
- **administrative retirement ≠ secure sanitization**.

---

## Functional analogies — explicitly not genealogy

- **Case 79 HDFS SafeMode:** both delay action around uncertain/insufficient replica state, but Case 79 rebuilds startup knowledge while Case 80 withdraws one known embodiment after preservation checks.
- **Case 05 RADOS:** both can add replicas to preserve logical state, but failure/membership-triggered repair is not the same historical mechanism as HDFS operator-driven decommission.
- **Case 73 GFS GC:** both can end the operational role of a physical replica, but object/chunk reclamation is not node decommissioning.
- **Case 14 / Case 78:** defect-driven sector/block replacement preserves identity across embodiment change, but does not establish lineage to administrative cluster drain.

---

## Rejected or unsupported claims

| Claim | Status | Reason |
| --- | --- | --- |
| HDFS invented graceful node decommissioning | rejected | no priority study; earlier distributed/cluster-management genealogy not audited |
| Hadoop 2.7 introduced DataNode decommission | rejected | 0.18 documentation already names the operation; 2.7.0 calls its change a refactor/improvement |
| decommissioned means local bytes securely erased | rejected | inspected path establishes administrative completion, not sanitization |
| dead DataNode = decommissioned DataNode | rejected | liveness and admin states differ; decommission-in-progress death can explicitly block completion |
| under-replicated block always blocks decommission in 2.7.3 | rejected | `isSufficientlyReplicated` contains bounded release-specific exceptions |
| zero entries in the monitor blocker list proves completion | rejected | source says list can be stale and performs a full-map recheck |
| recommission restores payload from backup | rejected | source can process over-replication precisely because old and newly created replicas may coexist |
| Case 80 proves current HDFS maintenance-mode semantics | rejected | bounded to historical decommission path; later maintenance state is separate |

---

## Evidence status

**`grounded`** for the bounded Case 80 relation.

The case is grounded by multiple Apache primary/release artifacts spanning an early administrator-visible command, later configuration semantics, a release-level refactor record, and exact 2.7.3 state/control flow. Remaining work is broader genealogy, release-to-release evolution, production performance/fault traces, and secure-media behavior—not a blocker for the retention-specific claim.
'''

readme_case_line = "- [`Case 80 — Apache HDFS DataNode Decommissioning: Administrative Retirement, Replication Drain, and Recommission`](cases/80-apache-hdfs-datanode-decommission-replica-drain.md) — `grounded`; Apache 0.18/1.0.4 documentation and Hadoop 2.7.3 source separate planned administrative exclusion from node failure: a live DataNode can remain `DECOMMISSION_INPROGRESS` while block replication is scheduled/checked, then pass a full block-map and health revalidation before `DECOMMISSIONED`; recommission can reverse the role transition and expose over-replication cleanup. Grounding: [`evidence/80-hadoop-2008-2016-datanode-decommission-grounding.md`](evidence/80-hadoop-2008-2016-datanode-decommission-grounding.md)."
readme_evidence_line = "- [`evidence/80-hadoop-2008-2016-datanode-decommission-grounding.md`](evidence/80-hadoop-2008-2016-datanode-decommission-grounding.md) — Case-80 grounding record: Apache 0.18/1.0.4 administrator documentation, the Hadoop 2.7.0 decommission-manager refactor record, and exact 2.7.3 `DatanodeInfo`/`DecommissionManager` source separate administrative intent, liveness, replication drain, progress summaries, final revalidation, recommission, and secure-erasure boundaries."

roadmap_line = "- [x] HDFS DataNode decommission / planned replica drain — [`cases/80-apache-hdfs-datanode-decommission-replica-drain.md`](cases/80-apache-hdfs-datanode-decommission-replica-drain.md), grounded by [`evidence/80-hadoop-2008-2016-datanode-decommission-grounding.md`](evidence/80-hadoop-2008-2016-datanode-decommission-grounding.md), adds planned embodiment withdrawal as a retention regime: administrative exclusion first creates `DECOMMISSION_INPROGRESS`; a live node's insufficient blocks are scanned and replication may be scheduled; a stale-prone progress list is not trusted as final authority, so completion rechecks the actual block map and node health before `DECOMMISSIONED`; recommission can create over-replication cleanup. This remains distinct from startup SafeMode re-observation (Case 79), HA command fencing (Case 51), failure repair, garbage collection, and secure sanitization."

ledger_line = "| [Apache HDFS DataNode Decommissioning: Administrative Retirement, Replication Drain, and Recommission](cases/80-apache-hdfs-datanode-decommission-replica-drain.md) | **grounded** | replicated HDFS blocks + DataNode admin state + administrator include/exclude intent + tracked insufficient-block/progress state + NameNode block-map/health revalidation | separate planned administrative withdrawal from liveness failure; decommission request from completed retirement; proactive replication drain from post-failure repair; progress summary from final authority; and role retirement from media sanitization | [2008–2016 HDFS DataNode-decommission grounding](evidence/80-hadoop-2008-2016-datanode-decommission-grounding.md); broader cluster-drain genealogy, later maintenance-state semantics, named-cluster performance/fault traces, and lower-layer sanitization remain separate work |"

matrix_line = "| HDFS DataNode decommission / 2008–2016 bounded regime | DataNode-resident block replicas + admin-state relation + host include/exclude intent + NameNode block map + transient blocker/progress set | administrator-triggered drain; scan source-node blocks; schedule needed replication; prune blockers; full-map and health recheck; optional recommission/over-replication cleanup | ordinary payload reads are outside the bounded audit; retirement semantics are qualified by admin/replica state rather than byte destruction | file/path -> block identity -> current replica locations, plus a separate node administrative-membership relation | logical block identity survives creation of replicas elsewhere while one still-existing DataNode loses in-service status | no complete history; current admin/progress/replica relations are enough for the bounded transition, and the monitor summary is explicitly not authoritative history |"

findings = r'''## Case 80 — HDFS DataNode decommission findings

957. **administrative exclusion intent ≠ completed DataNode retirement** — operator/configuration action can start decommissioning while the node remains in an explicit intermediate state;
958. **`DECOMMISSION_INPROGRESS` ≠ `DECOMMISSIONED`** — Hadoop 2.7.3 represents these as distinct administrative states with different completion conditions;
959. **planned retirement ≠ failure detection** — include/exclude administration and `refreshNodes` are explicit role decisions, while Heartbeat loss is a liveness/failure signal;
960. **replication drain before retirement ≠ repair only after abrupt node failure** — a live source node can remain present while the NameNode schedules preservation work elsewhere before withdrawal completes;
961. **physical DataNode survival ≠ continued in-service authority** — a machine and its local replicas can materially survive while its administrative relation to the cluster changes;
962. **replica survival on the retiring node ≠ sufficient future redundancy** — retirement is gated by the state of other replicas/placement, not by the mere fact that source bytes still exist;
963. **decommission progress list ≠ authoritative final block map** — the 2.7.3 source explicitly allows the tracked blocker set to become stale;
964. **zero tracked blockers ≠ final completion without revalidation** — the manager performs a full block-map scan before finally marking the node decommissioned;
965. **replica count ≠ placement/retirement sufficiency** — the bounded completion logic can also consult placement policy and node health;
966. **under-replicated ≠ always decommission-blocking in the bounded 2.7.3 rules** — `isSufficientlyReplicated` contains release-specific minimum/default-replication exceptions, so the predicates must not be treated as synonyms;
967. **node liveness/health ≠ administrative service state** — the source separately represents reachability/health and `In Service`/decommission states, and a decommission-in-progress node dying can block successful completion;
968. **recommission ≠ payload restoration from backup** — stopping decommission can return a still-present node to service without recreating its local block contents;
969. **recommission can create over-replication cleanup work** — replicas produced elsewhere during the drain may coexist with the returning node, so convergence can continue after administrative reversal;
970. **administrative retirement ≠ secure data erasure** — the inspected completion path changes cluster role after preservation checks and supplies no media-sanitization guarantee;
971. **planned embodiment withdrawal can require proactive preservation work before role forgetting** — retention may consist not only in repairing after loss but in making dependence safely removable before a known support is withdrawn;
972. **HDFS decommission ≈ RADOS/GFS/defect repair only as functional comparison** — all can preserve higher-level identity while embodiments change, but trigger, authority, object, lifecycle, and historical mechanism differ.
'''


def run(*args):
    subprocess.run(args, check=True)


def insert_after(lines, predicate, new_line, start=0):
    if any(new_line == line for line in lines):
        return lines
    for i in range(start, len(lines)):
        if predicate(lines[i]):
            lines.insert(i + 1, new_line)
            return lines
    raise RuntimeError(f"insertion anchor not found for: {new_line[:80]}")


def write_lines(path, lines):
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


# Create the bounded case and its independent evidence record.
Path(CASE_PATH).parent.mkdir(parents=True, exist_ok=True)
Path(EVIDENCE_PATH).parent.mkdir(parents=True, exist_ok=True)
Path(CASE_PATH).write_text(case_text, encoding="utf-8")
Path(EVIDENCE_PATH).write_text(evidence_text, encoding="utf-8")

# README navigation: add one case entry and one evidence entry.
readme = Path("README.md").read_text(encoding="utf-8").splitlines()
insert_after(
    readme,
    lambda line: "cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md" in line,
    readme_case_line,
)
insert_after(
    readme,
    lambda line: line.startswith("- [`evidence/79-hadoop-2010-2016-startup-safemode-grounding.md`"),
    readme_evidence_line,
)
write_lines("README.md", readme)

# ROADMAP: close only this bounded bridge, before the still-open broader DRAM line.
roadmap = Path("ROADMAP.md").read_text(encoding="utf-8").splitlines()
if roadmap_line not in roadmap:
    for i, line in enumerate(roadmap):
        if line.startswith("- [ ] DRAM evolution and refresh machinery beyond the bounded case"):
            roadmap.insert(i, roadmap_line)
            break
    else:
        raise RuntimeError("ROADMAP insertion anchor not found")
write_lines("ROADMAP.md", roadmap)

# CASE_INDEX main ledger.
index = Path("CASE_INDEX.md").read_text(encoding="utf-8")
lines = index.splitlines()
comparison_heading = lines.index("## Comparison matrix — provisional")
if ledger_line not in lines:
    for i in range(comparison_heading):
        if "cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md" in lines[i]:
            lines.insert(i + 1, ledger_line)
            break
    else:
        raise RuntimeError("CASE_INDEX case79 ledger anchor not found")

# Aggregate status and comparison matrix.
index_text = "\n".join(lines) + "\n"
old_aggregate = "After eighty bounded cases, **all eighty cases are now `grounded`.**"
new_aggregate = "After eighty-one bounded cases, **all eighty-one cases are now `grounded`.**"
if old_aggregate in index_text:
    index_text = index_text.replace(old_aggregate, new_aggregate, 1)
elif new_aggregate not in index_text:
    raise RuntimeError("CASE_INDEX aggregate-status anchor not found")
lines = index_text.splitlines()
comparison_heading = lines.index("## Comparison matrix — provisional")
if matrix_line not in lines:
    for i in range(comparison_heading + 1, len(lines)):
        if lines[i].startswith("| HDFS startup SafeMode / 2010–2016 bounded regime |"):
            lines.insert(i + 1, matrix_line)
            break
    else:
        raise RuntimeError("CASE_INDEX comparison Case79 anchor not found")
index_text = "\n".join(lines).rstrip() + "\n"

if "## Case 80 — HDFS DataNode decommission findings" not in index_text:
    if "956. **HDFS bounded SafeMode evidence ≠ invention-priority proof**" not in index_text:
        raise RuntimeError("CASE_INDEX finding 956 anchor not found")
    index_text = index_text.rstrip() + "\n\n" + findings.rstrip() + "\n"
Path("CASE_INDEX.md").write_text(index_text, encoding="utf-8")

# Validation: avoid brittle exact Markdown-link counts; assert semantic anchors instead.
for p in ["README.md", "ROADMAP.md", "CASE_INDEX.md", CASE_PATH, EVIDENCE_PATH]:
    if not Path(p).exists() or Path(p).stat().st_size == 0:
        raise RuntimeError(f"missing/empty required file: {p}")

assert CASE_PATH in Path("README.md").read_text(encoding="utf-8")
assert EVIDENCE_PATH in Path("README.md").read_text(encoding="utf-8")
assert CASE_PATH in Path("ROADMAP.md").read_text(encoding="utf-8")
idx = Path("CASE_INDEX.md").read_text(encoding="utf-8")
assert CASE_PATH in idx and EVIDENCE_PATH in idx
assert "After eighty-one bounded cases, **all eighty-one cases are now `grounded`.**" in idx
assert "957. **administrative exclusion intent ≠ completed DataNode retirement**" in idx
assert "972. **HDFS decommission ≈ RADOS/GFS/defect repair only as functional comparison**" in idx
assert "## Historical record" in case_text and "## Engineering reconstruction" in case_text
assert "## Functional comparisons — not genealogy" in case_text
assert "## Philosophical interpretation — bounded" in case_text
assert "## Rejected or unsupported claims" in evidence_text

run("git", "diff", "--check")
run("git", "config", "user.name", "github-actions[bot]")
run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
run("git", "add", "README.md", "ROADMAP.md", "CASE_INDEX.md", CASE_PATH, EVIDENCE_PATH)
run("git", "rm", "-f", SCRIPT_PATH, WORKFLOW_PATH)
run("git", "commit", "-m", "case80: ground HDFS datanode decommission drain")
run("git", "push", "origin", "HEAD:main")
