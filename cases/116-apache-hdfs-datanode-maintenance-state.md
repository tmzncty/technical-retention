# Apache HDFS DataNode Maintenance State: Temporary Withdrawal, Relaxed Redundancy, and Expiry

## Status

**`grounded`** — bounded to the HDFS DataNode maintenance-state design recorded in 2014–2017 ASF issue/design material and the released Hadoop 2.9.0 / 3.0.1 documentation and source. This case does not claim that HDFS invented maintenance modes, temporary node withdrawal, relaxed redundancy, or failure-domain-aware operations.

Grounding record: [`../evidence/116-hadoop-2014-2018-datanode-maintenance-grounding.md`](../evidence/116-hadoop-2014-2018-datanode-maintenance-grounding.md).

Restart-reconstitution deepening: [`../evidence/116-hadoop-301-maintenance-restart-reconstitution-deepening.md`](../evidence/116-hadoop-301-maintenance-restart-reconstitution-deepening.md).

## Scope

Case 80 established the older HDFS decommission path: a live DataNode selected for planned retirement remains `DECOMMISSION_INPROGRESS` until enough other replicas satisfy the bounded decommission condition, after which the node can become `DECOMMISSIONED`.

Case 116 asks the deliberately different question introduced by later HDFS maintenance state:

> **If an operator expects a DataNode to disappear only temporarily, can the storage system preserve the node's replica role without paying the full replication cost of permanent withdrawal, and what state limits that temporary relaxation?**

The bounded regime includes:

- `ENTERING_MAINTENANCE` and `IN_MAINTENANCE` administrative states;
- a maintenance-specific minimum-redundancy condition;
- continued accounting of replicas on the maintenance node;
- exclusion of an `IN_MAINTENANCE` node from ordinary read placement in the inspected design/release family;
- suppression of ordinary block invalidation / unnecessary re-replication while maintenance is valid;
- a retained maintenance-expiry time;
- automatic return from the maintenance regime when that time expires;
- re-replication or cleanup work when the temporary assumption no longer holds.

This is **not** a general Hadoop rolling-upgrade history, a DataNode hardware-maintenance manual, an HDFS erasure-coding case, or a claim about every later Hadoop release. It also does not replace Case 80's older decommission/rack-placement analysis.

---

## Historical vocabulary

The inspected ASF/Hadoop sources directly use:

- `maintenance mode` / `maintenance state`;
- `ENTERING_MAINTENANCE`;
- `IN_MAINTENANCE`;
- `DECOMMISSION_INPROGRESS` / `DECOMMISSIONED`;
- `admin state`;
- `liveness` / `live` / `dead`;
- `minimally replicated` / `sufficiently replicated`;
- `dfs.namenode.maintenance.replication.min` in released documentation/source;
- `maintenanceExpireTimeInMS`;
- `maintenance expires` / maintenance expiration;
- `refreshNodes`;
- `BlockMap` / block maps;
- replication / reconstruction;
- over-replicated / extra redundancy.

The following are **project engineering terms**, not period quotations:

- `temporary withdrawal contract`;
- `relaxed redundancy envelope`;
- `retained return expectation`;
- `expiry-bounded dependency`;
- `temporary embodiment credit`;
- `withdrawal horizon`.

---

## Historical record

### H/P — a short-outage maintenance-mode requirement was public before HDFS-7877

ASF issue HDFS-6729, active publicly in July–August 2014, describes a DataNode maintenance mode for short interventions such as upgrading RAM or adding disks. Its motivating contrast is explicit: for a short outage, operators did not want to incur the behavior associated with normal failure/decommission when they expected the same DataNode to return soon.

The issue was later marked duplicate of HDFS-7877. Therefore:

> **HDFS-7877 in 2015 is not an invention-priority date for the HDFS maintenance-state idea.**

The 2014 issue is only an earlier public HDFS project floor. It does not establish broader distributed-storage priority.

### H/P — the 2015 design separates liveness from administrative maintenance state

The April 2015 HDFS-7877 design document says only the NameNode needs to know that a DataNode is in maintenance; the DataNode itself need not contain the authoritative maintenance-state decision. It adds `ENTERING_MAINTENANCE` and `IN_MAINTENANCE` alongside the older in-service/decommission states.

This produces a direct historical separation:

```text
DataNode liveness
    !=
DataNode administrative maintenance state
```

A machine can be administratively in maintenance while alive or dead. The state machine explicitly includes both liveness conditions.

### H/P — maintenance admission uses a different preservation threshold from decommission

The HDFS-7877 design document gives the central distinction. If the only replica of a block is on a DataNode about to enter maintenance, another replica should first be created for availability. The node therefore passes through `ENTERING_MAINTENANCE` until its blocks meet a maintenance-specific minimum.

The design directly contrasts the two transitions:

- `ENTERING_MAINTENANCE -> IN_MAINTENANCE` uses a maintenance minimum;
- `DECOMMISSION_INPROGRESS -> DECOMMISSIONED` uses the ordinary file-replication requirement in the design's bounded wording.

Released Hadoop 3.0.1 `DatanodeAdminManager` keeps the same structural distinction: maintenance does **not always** require re-replication to the normal factor; the block replication factor is relaxed while the maintenance interval remains valid.

So:

> **planned temporary withdrawal ≠ planned permanent retirement**

and:

> **maintenance admissibility ≠ decommission admissibility**.

### H/P — the maintenance replica can remain part of retained block state while ordinary service avoids the node

The 2015 design says replicas on a maintenance node remain in the NameNode block maps and are still treated as valid from the bounded block-replication point of view; putting the node in maintenance is specifically intended not to trigger ordinary replication merely because that node later becomes dead during the planned interval.

At the same time, the design differentiates read/write eligibility. It says an `IN_MAINTENANCE` node is excluded from returned read locations and is not selected for future writes, while a live `ENTERING_MAINTENANCE` node may still appear for reads until the transition completes.

That yields three different relations:

```text
replica is physically present / known
    !=
replica is credited in maintenance redundancy accounting
    !=
replica is eligible for ordinary client service now
```

The project should not collapse them into one Boolean `replica valid`.

### H/P — released 3.0.1 code retains expiration as control state

Hadoop 3.0.1 `DatanodeAdminManager.startMaintenance()` stores `maintenanceExpireTimeInMS` on the DataNode descriptor and tracks the node even after it reaches `IN_MAINTENANCE`, specifically so the monitor can later observe maintenance expiration.

The monitor checks `maintenanceExpired()`. If the condition becomes true it calls `stopMaintenance()` and removes the node from the maintenance tracking relation.

Thus:

> **maintenance state is not only a node label; it includes a retained time boundary that can revoke the relaxed-redundancy regime.**

The expiry time is control-plane retention state, not user payload and not a media-retention lifetime.

### H/P — expiration changes the preservation policy rather than erasing the node's replicas

The class documentation states that the replication factor is relaxed only up to the maintenance expiry time. If the DataNode has not returned appropriately by expiry, blocks are re-replicated as in the ordinary decommission/failure-oriented path to avoid prolonged service degradation.

`stopMaintenance()` makes the concrete cleanup distinction:

- if the node is dead, replicas that had remained represented in block maps while maintenance was active are removed from that accounting, which can trigger necessary replication;
- if the node is alive, the system processes extra redundancy because returning to ordinary service may make some replicas over-redundant.

Therefore:

> **expiry ≠ payload deletion**;

> **expiry = withdrawal of permission to keep relying on the temporary maintenance relation** in the bounded design.

The resulting work depends on whether the node actually returned.

### H/P — maintenance completion is still a monitored transition, not merely operator intent

The 3.0.1 manager tracks `ENTERING_MAINTENANCE` nodes, scans blocks that require reconstruction, prunes the blocker list as sufficient redundancy becomes available, and performs a full block-map recheck before marking the node `IN_MAINTENANCE`. It also requires the node to satisfy the relevant health qualification.

This closely resembles the revalidation pattern already grounded for decommissioning in Case 80, but with a different target sufficiency rule.

So:

> **operator requests maintenance ≠ node is already admissible to disappear**.

The retained administrative intent must be followed by evidence that the bounded minimum condition is satisfied.

### H/P — the feature became a released HDFS interface by the 2.9.0 / 3.0 generation

HDFS-7877 is recorded as resolved on 20 September 2017 with fix versions including Hadoop 2.9.0, 3.0.0-beta1, and 3.1.0. Apache's Hadoop 2.9.0 documentation, published 18 November 2017, exposes `-enteringmaintenance` and `-inmaintenance` filters in `hdfs dfsadmin -report`. Hadoop 3.0.0 documentation published 8 December 2017 includes a dedicated DataNode Admin guide, and the 3.0.1 release source inspected here contains the maintenance/decommission manager implementation.

These dates establish an open project/release floor. They do not establish first production deployment in the world or even first private HDFS deployment: the HDFS-7877 discussion itself notes production-cluster interest before the ASF release completion.

---

## Restart reconstitution deepening — Hadoop 3.0.1

A later source-level deepening now separates two restart contracts that the broad maintenance-state case previously left together. In the exact Hadoop 3.0.1 tag, the combined JSON hosts file can retain `adminState: IN_MAINTENANCE` together with `maintenanceExpireTimeInMS`; `CombinedHostFileManager.refresh()` reloads those host properties, and `DatanodeManager` consults them when DataNodes register. Thus a fresh NameNode process can reconstitute maintenance intent and its expiry from retained external configuration.

The same released test suite provides an important counterexample to the shortcut “maintenance policy survived, therefore every replica credit survived.” In a bounded restart scenario where the maintenance DataNode is down, the restarted NameNode restores the normal live-replica count because it does not yet know that the absent maintenance node still carries the replica. When that DataNode later returns, its maintenance replica relation becomes visible again.

So the bounded release now supports:

> **persisted maintenance intent / expiry != persisted runtime knowledge of a particular replica embodiment**

and:

> **policy survival != service-side reliance survival**.

A maintenance replica's bytes may physically survive the NameNode restart while the restarted control plane declines to rely on that unobserved location. This is not payload loss; it is a difference in the restart lifetime of **embodiment evidence**.

The deepening also fixes an important negative boundary. The inspected configuration-reload path does not by itself establish whether every maintenance-related field is or is not serialized through FSImage/edit logs, and a NameNode process restart is not the same event as a DataNode return/re-registration or every HA failover path.

Deepening record: [`../evidence/116-hadoop-301-maintenance-restart-reconstitution-deepening.md`](../evidence/116-hadoop-301-maintenance-restart-reconstitution-deepening.md).

---

## Retained state

At least eight state classes should remain distinct.

### 1. User payload blocks

The actual HDFS block bytes on DataNodes.

### 2. Replica-location relation

The NameNode's block map records which DataNodes are known to embody each block. Under maintenance, a replica can remain represented even while the node becomes temporarily unavailable.

### 3. Normal expected replication factor

The ordinary file/block redundancy objective remains a policy state even when maintenance temporarily relaxes what must be live elsewhere.

### 4. Maintenance minimum

`dfs.namenode.maintenance.replication.min` is a separate threshold governing how much non-maintenance redundancy is required before the temporary withdrawal is admitted.

### 5. Administrative state

`ENTERING_MAINTENANCE` and `IN_MAINTENANCE` distinguish requested-but-not-yet-admissible withdrawal from accepted temporary withdrawal.

### 6. Liveness state

Live/dead/stale observations remain distinct from administrative maintenance state.

### 7. Maintenance expiration

`maintenanceExpireTimeInMS` retains the temporal bound on how long the relaxed relation may remain authoritative.

### 8. Transition / reconstruction progress

The manager retains a working set of insufficiently stored blocks and revalidates before completing the transition. This is maintenance progress state, not payload.

---

## Engineering reconstruction

### Temporary absence can preserve role identity while relaxing immediate embodiment requirements

Decommissioning prepares the system to stop depending on a node as an ordinary replica holder. Maintenance instead says, approximately:

```text
this node is expected to return
    +
its replicas still matter to the retained topology relation
    +
ordinary service should avoid depending on it during the outage
    +
only a smaller live-replica floor must be restored elsewhere
    +
that relaxation is time-bounded
```

This is a different preservation strategy from copying every embodiment away before shutdown.

### Retention policy can depend on expected future return

The maintenance state encodes an operational expectation about the future: the same DataNode is expected back soon enough that full decommission replication would be wasteful.

That expectation is not merely prose in an operator runbook. It becomes machine-visible state through the admin state and expiration time, and it changes block-management actions.

> **future-return expectation can be constitutive retention-control state.**

### Reduced redundancy is not the same as lost redundancy policy

During maintenance the ordinary expected replication factor has not been redefined as a smaller permanent factor. Instead the system temporarily admits a different live-replica condition while remembering that one embodiment belongs to an out-of-service node expected to return.

Therefore:

> **temporary redundancy relaxation ≠ permanent replication-factor change**.

When maintenance ends, ordinary redundancy accounting resumes and may require either reconstruction or deletion of excess copies.

### A replica can be retained but temporarily denied service authority

The bounded design makes a maintenance replica useful to the preservation relation without making it an ordinary read/write target.

That is a strong repository-wide distinction:

> **retained embodiment ≠ current service eligibility**.

This is analogous at a high functional level to other cases where physically surviving state is not currently admissible, but the mechanism here is distributed administrative policy rather than version staleness, checksum failure, or access protection.

### Expiry is revocation of a temporary assumption

The most useful cross-case abstraction is not `timer deletes data`. It is:

```text
retained policy assumption
    -> remains authoritative until bounded time
    -> expiry revokes the relaxed preservation rule
    -> system must recompute / repair under ordinary rules
```

The timer governs **which retention policy is admissible**, not how long disk magnetic state or Flash charge physically survives.

---

## Cross-case boundaries

### Versus Case 80 — HDFS DataNode decommissioning

Case 80 studies planned withdrawal where HDFS seeks enough alternative replicas/placement before the old node can stop counting as an in-service embodiment. Case 116 studies a later temporary-withdrawal regime that deliberately avoids full decommission replication when a bounded minimum is available and the node is expected back.

The key comparison is:

> **same physical outage plan ≠ same retention obligation when administrative horizon differs.**

A short-term maintenance contract can retain dependency on the returning embodiment; decommissioning is designed to retire that dependency.

This is a direct historical/engineering comparison within HDFS, not a claim that one mechanism universally supersedes the other.

### Versus Case 68 — Dynamo membership and temporary failure

Dynamo 2007 separates transient reachability suspicion from explicit persistent membership change; HDFS maintenance state also separates temporary absence from permanent administrative withdrawal.

**Functional analogy only.** Dynamo uses local failure suspicion, sloppy quorum/hinted handoff, and explicit ring membership history. HDFS uses NameNode-administered node state, replica thresholds, block maps, and an expiry-bounded maintenance contract. No genealogy is asserted.

### Versus Case 115 — HDFS snapshot replication obligation

Case 115 shows historical namespace metadata imposing a present replication requirement on shared blocks. Case 116 shows administrative/time metadata temporarily relaxing the number of live non-maintenance embodiments required for a planned outage.

Both show that payload-copy policy depends on retained metadata, but the controlling relations are different:

- temporal namespace/version authority in Case 115;
- node administrative horizon and expiry in Case 116.

### Versus media-level retention cases

Maintenance expiry is not DRAM refresh deadline, SSD retention rating, NAND charge-loss time, or magnetic decay. It is a distributed control-policy deadline.

> **policy expiry ≠ physical retention expiry**.

---

## Failure and forgetting boundaries

Keep these failure modes separate:

- administrator requests maintenance but minimum replica conditions are not yet satisfied;
- a node enters maintenance and does not return before expiry;
- maintenance-expiration state is incorrect or lost;
- a dead maintenance node continues to be counted after the temporary contract should have ended;
- a returning node creates over-redundancy that is not cleaned up;
- ordinary clients are accidentally directed to an unavailable `IN_MAINTENANCE` node;
- insufficient non-maintenance replicas make temporary withdrawal unsafe;
- liveness state is mistaken for administrative intent;
- `IN_MAINTENANCE` is mistaken for physical erasure, decommissioning, or permanent membership removal.

The bounded sources do not establish secure erasure, disk sanitization, or physical destruction of any replica.

---

## Prior-art and genealogy boundary

The repository must not say that HDFS-7877 invented temporary storage-node maintenance semantics.

- HDFS-6729 supplies an earlier public HDFS project record in 2014.
- HDFS-7877 begins in March 2015 and absorbs/coordinates the feature work.
- HDFS-7877's 2015 design document is a design record, not a release record.
- HDFS-7877's September 2017 resolution/fix versions and Apache 2.9.0/3.0.x documentation/source supply the bounded released-interface floor used here.
- The earlier existence of decommissioning (Case 80) does not make maintenance state identical to decommissioning.
- This case does not attempt the broader history of planned temporary replica withdrawal in distributed storage. That belongs in `computing-archaeology` if developed.

A repository search found no dedicated HDFS DataNode-maintenance-state case in `tmzncty/computing-archaeology` during this round.

---

## What is established

### Historical record

- short-duration DataNode maintenance was an explicit ASF problem by 2014;
- the 2015 HDFS-7877 design added distinct entering/in-maintenance states and a maintenance-specific minimum-replication concept;
- HDFS-7877 resolved in 2017 with 2.9.0 / 3.0.0-beta1 / 3.1.0 fix versions;
- released 2.9.0 documentation exposes maintenance admin-state reporting;
- released 3.0.1 source retains expiration, tracks maintenance transitions, and applies different reconstruction/cleanup behavior from ordinary decommissioning.

### Engineering reconstruction

- `liveness != admin state`;
- `physical replica presence != ordinary service eligibility`;
- `maintenance minimum != ordinary replication factor`;
- `maintenance admission != decommission completion`;
- `temporary redundancy relaxation != permanent factor reduction`;
- `expiry != data deletion`;
- `expiry = loss of authority for the bounded relaxed-dependency assumption`;
- `expected return can be retained control state that changes present replication work`.

### Functional analogy only

- Dynamo temporary failure vs membership change;
- other cases in which a surviving embodiment is retained but not currently service-authoritative.

### Not established

- invention priority for maintenance mode;
- first production deployment;
- universal semantics across every Hadoop 3.x release;
- exact behavior for every erasure-coded block layout;
- fault-injection validation of expiry/restart races;
- physical media sanitization after maintenance/decommission;
- broad distributed-storage maintenance-mode genealogy.

---

## Follow-up debt

Useful later work is deliberately narrower than another generic HDFS overview:

1. inspect the exact commit series/subtasks that moved HDFS-7877 from the 2015 design to the final 2017 implementation;
2. audit NameNode restart/failover persistence of maintenance expiration across the relevant 2.9/3.0 transition;
3. test maintenance expiry with dead/live returning nodes and observe reconstruction/over-replication convergence;
4. separately analyze erasure-coded HDFS maintenance semantics if they differ materially;
5. move a broader history of temporary-node-maintenance mechanisms across distributed stores to `computing-archaeology`.

The bounded Case 116 itself is grounded.