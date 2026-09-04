# Case 80 grounding record — Apache HDFS DataNode decommissioning, 2008–2016

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
