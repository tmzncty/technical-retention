# Evidence 116 — HDFS DataNode Maintenance-State Grounding (2014–2018)

## Purpose

This record grounds Case 116's bounded claim that later HDFS distinguishes a **temporary, expiry-bounded DataNode maintenance relation** from ordinary decommissioning. The evidence is used to separate:

- DataNode liveness from administrative state;
- normal replication from a maintenance-specific live-replica floor;
- known/retained replicas from ordinary service eligibility;
- an operator maintenance request from completed maintenance admission;
- maintenance expiration from payload deletion or physical-media retention time;
- temporary dependence on an expected-to-return embodiment from permanent retirement of that dependence.

The record does **not** establish invention priority for maintenance modes, first production deployment, universal behavior across every Hadoop version, or physical media sanitization.

---

## Source set and evidence roles

### A. ASF HDFS-6729 — earlier public HDFS maintenance-mode floor (2014)

**Source:** Apache Software Foundation JIRA, `HDFS-6729 — Support maintenance mode for DN`.

- URL: <https://issues.apache.org/jira/browse/HDFS-6729>
- Public issue activity: July–August 2014.
- Later disposition: duplicate of HDFS-7877.

The issue motivates a DataNode maintenance mode for short interventions such as hardware work, where operators expect the same node to return soon and do not want the full behavior/cost associated with decommissioning or ordinary prolonged failure.

**Evidence role:** project-internal chronological prior-art floor. It blocks a claim that the March 2015 creation of HDFS-7877 marks the origin of the HDFS maintenance-state idea.

**Boundary:** a JIRA issue is not proof of first implementation, first production use, or invention priority beyond HDFS.

### B. ASF HDFS-7877 — feature chronology and release boundary (2015–2017)

**Source:** Apache Software Foundation JIRA, `HDFS-7877 — Support maintenance state for datanodes`.

- URL: <https://issues.apache.org/jira/browse/HDFS-7877>
- Created: **3 March 2015**.
- Resolved: **20 September 2017**.
- Resolution: Fixed.
- Fix versions listed by ASF include Hadoop **2.9.0**, **3.0.0-beta1**, and **3.1.0**.
- Design attachments were posted in March/April 2015.

**Evidence role:** authoritative ASF chronology linking proposal/design work to named release families.

**Boundary:** the issue chronology is not a substitute for inspecting the design document and released source. A fix-version list also does not establish exact runtime behavior by itself.

### C. HDFS-7877 April 2015 design document — state separation and maintenance-specific redundancy

**Source:** Apache Software Foundation JIRA attachment, `Support maintenance state for datanodes`, design revision attached 4 April 2015.

- URL: <https://issues.apache.org/jira/secure/attachment/12709388/Supportmaintenancestatefordatanodes-2.pdf>

The document directly records the motivation and proposed semantics:

1. maintenance is for temporary unavailability where the DataNode is expected back soon;
2. the NameNode should avoid sending ordinary read/write requests to an `IN_MAINTENANCE` node;
3. `ENTERING_MAINTENANCE` is distinct from `IN_MAINTENANCE`;
4. if a block would otherwise have too little redundancy, replication should occur before the transition completes;
5. the proposed maintenance threshold is separate from the ordinary file replication requirement used in decommission reasoning;
6. replicas on a maintenance node remain represented in the NameNode's block map rather than being immediately treated as destroyed;
7. an `IN_MAINTENANCE` node is not selected as an ordinary write target and is excluded from ordinary read locations in the bounded design;
8. leaving maintenance can require either replica-accounting removal/re-replication for a dead node or extra-replica cleanup for a live returning node.

The draft uses `dfs.namenode.replication.maintenance.min`; the later released implementation/documentation uses `dfs.namenode.maintenance.replication.min`. These names must not be silently normalized as though the draft and final interface were textually identical.

#### Important version boundary: timeout was still open in the 2015 design

The April 2015 document lists timeout support as an **open issue**. Therefore Case 116 must not project the final released expiration semantics backward into the design document.

This yields a useful historical distinction:

> **2015 design intent for maintenance ≠ complete final released maintenance contract.**

The final expiry mechanism is grounded separately in released code below.

### D. Hadoop 2.9.0 HDFS command documentation — released administrative visibility (2017)

**Source:** Apache Hadoop 2.9.0 documentation.

- Release documentation index: <https://hadoop.apache.org/docs/r2.9.0/>
- HDFS Commands Guide: <https://hadoop.apache.org/docs/r2.9.0/hadoop-project-dist/hadoop-hdfs/HDFSCommands.html>
- Documentation publication date shown by Apache: **18 November 2017**.

The released `hdfs dfsadmin -report` interface includes maintenance-state filters such as `-enteringmaintenance` and `-inmaintenance`.

**Evidence role:** released-user-interface witness showing maintenance state is no longer only design/JIRA vocabulary by the 2.9.0 generation.

**Boundary:** command-reporting visibility does not by itself ground the full block-management mechanism; that role belongs to the released source.

### E. Hadoop 3.0.1 DataNode Administration Guide — released operational contrast

**Source:** Apache Hadoop 3.0.1, *HDFS DataNode Admin Guide*.

- URL: <https://hadoop.apache.org/docs/r3.0.1/hadoop-project-dist/hadoop-hdfs/HdfsDataNodeAdminGuide.html>

The guide explicitly contrasts decommissioning with maintenance:

- decommissioning is the path for removing a DataNode from service while restoring ordinary replication elsewhere;
- maintenance is intended for shorter outages and is lighter weight;
- a maintenance node can enter the maintenance regime when blocks are sufficiently/minimally replicated according to the maintenance condition rather than always restoring the full ordinary replication factor first;
- maintenance has a timeout/expiration relation.

**Evidence role:** released operational documentation for the decommission-versus-maintenance boundary.

**Boundary:** this is service documentation, not evidence about physical media lifetime or secure deletion.

### F. Hadoop 3.0.1 `DatanodeAdminManager.java` — released mechanism witness

**Source:** Apache Hadoop source, tag/ref `rel/release-3.0.1`:

<https://github.com/apache/hadoop/blob/rel/release-3.0.1/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/DatanodeAdminManager.java>

The class-level documentation and implementation directly establish several bounded semantics.

#### F1. Maintenance does not always trigger full re-replication

The class comment says DataNodes can be put under maintenance for short-duration work and that, unlike decommissioning, blocks are not always re-replicated merely to enter maintenance. The transition is governed by `dfs.namenode.maintenance.replication.min`.

This supports:

> `maintenance-specific minimum != ordinary full replication requirement`.

#### F2. The relaxed relation is explicitly time-bounded

The same class comment says the block replication factor is relaxed for a maximum of the maintenance expiry time; if the DataNode does not return appropriately by expiry, blocks are re-replicated in the decommission-like preservation regime.

This supports:

> `policy expiry != media-retention expiry`.

#### F3. `startMaintenance()` retains an expiration time

`startMaintenance(DatanodeDescriptor node, long maintenanceExpireTimeInMS)` writes the expiry value into the DataNode descriptor. The code deliberately tracks the node whether it is still entering maintenance or already `IN_MAINTENANCE`, so expiration can be observed later.

This is direct implementation evidence that the temporal boundary is retained control state rather than merely operator prose.

#### F4. The monitor revokes maintenance when expiration is observed

The monitor checks `dn.isMaintenance() && dn.maintenanceExpired()`. When true, it calls `stopMaintenance(dn)` and removes the node from maintenance tracking.

Expiry therefore changes the administrative/redundancy regime. It does not execute a physical erasure of the DataNode's media.

#### F5. Dead and live exits have different convergence work

`stopMaintenance()` distinguishes:

- **dead node:** remove its associated replicas from block maps so necessary replication can be triggered and the ordinary safety relation restored;
- **live node:** process extra redundancy that may now exist after the node returns to ordinary service.

This supports:

> `maintenance exit != one fixed payload operation`.

#### F6. Admission is monitored and revalidated

The manager tracks `ENTERING_MAINTENANCE` nodes, schedules reconstruction where needed, prunes blocks that have become sufficiently stored, and performs a full block-map recheck before marking a node `IN_MAINTENANCE`. The code also uses a health qualification before completing the transition.

This supports:

> `operator request != completed maintenance admission`.

---

## Chronology reconstruction

A conservative bounded chronology is:

```text
July–August 2014
HDFS-6729 publicly proposes short-duration DataNode maintenance mode
        |
        v
3 March 2015
HDFS-7877 created
        |
        v
March–April 2015
HDFS-7877 design documents define entering/in-maintenance semantics,
maintenance-specific minimum redundancy, service exclusion, and block-map behavior;
timeout is still explicitly open
        |
        v
20 September 2017
HDFS-7877 resolved Fixed with 2.9.0 / 3.0.0-beta1 / 3.1.0 fix versions
        |
        v
18 November 2017
Hadoop 2.9.0 docs expose entering/in-maintenance reporting
        |
        v
Hadoop 3.0.x released documentation/source
expiry-bounded maintenance and concrete stop/reconstruction behavior are inspectable
```

This is an **HDFS project/release chronology**, not a broad history of maintenance-mode ideas across distributed storage.

---

## Claim ledger

| Claim | Layer | Evidence | Boundary |
| --- | --- | --- | --- |
| HDFS had a public short-outage maintenance-mode proposal by 2014 | `H/P` | HDFS-6729 | project floor only; no invention claim |
| HDFS-7877 added explicit maintenance-state work in 2015 and resolved in 2017 | `H/P` | HDFS-7877 | JIRA chronology, not mechanism proof by itself |
| maintenance admin state is distinct from node liveness | `H/P` | 2015 design; released source | bounded HDFS semantics |
| entering maintenance and in maintenance are distinct states | `H/P` | 2015 design; 3.0.1 source | not generalized to other systems |
| maintenance can require less live redundancy elsewhere than permanent decommission | `H/P` | 2015 design; 3.0.1 guide/source | exact threshold is version/configuration dependent |
| replica remains known/retained while service eligibility can be withdrawn | `H/P` | 2015 design | design/release-family boundary only |
| maintenance expiry is retained control state | `H/P` | 3.0.1 `startMaintenance` / monitor | final released behavior; not projected into 2015 draft |
| timeout/expiry was still open in April 2015 | `H/P` | HDFS-7877 design PDF | blocks retroactive final-semantics projection |
| expiry can trigger return to ordinary reconstruction policy | `H/P` | 3.0.1 class comment / `stopMaintenance` | does not imply immediate physical copying at one exact instant |
| expiry deletes payload | `X` | contradicted by source behavior | administrative-policy transition, not erase |
| maintenance minimum permanently changes file replication factor | `X` | contradicted by temporary relaxation semantics | policy relation only |
| retained maintenance replica is necessarily ordinary read/write eligible | `X` | contradicted by design/service-selection rules | presence/accounting and service authority differ |
| maintenance is just decommission with a shorter timer | `X` | different threshold, retained replicas, state/expiry semantics | mechanisms are related but not identical |
| HDFS invented temporary maintenance modes | `X` | evidence only establishes HDFS chronology | broader prior art not audited here |

---

## Mechanism decomposition

The bounded released mechanism can be reconstructed as:

```text
operator marks node for maintenance
        |
        v
retain admin intent + expiry
        |
        v
ENTERING_MAINTENANCE
        |
        +--> inspect blocks and non-maintenance redundancy
        +--> schedule reconstruction only where maintenance sufficiency fails
        |
        v
full re-check / health qualification
        |
        v
IN_MAINTENANCE
        |
        +--> replica can remain represented in retained block relation
        +--> ordinary client service avoids the maintenance node
        +--> full ordinary replication may remain temporarily relaxed
        |
        +---- node returns before/at exit ----> restore ordinary service relation
        |                                     + process possible extra redundancy
        |
        +---- expiry while node unavailable -> stop maintenance relation
                                              + remove dead-node replica credit
                                              + restore ordinary reconstruction obligation
```

The diagram is an engineering reconstruction from the source, not Apache's literal state-machine notation.

---

## Cross-case evidence boundaries

### Case 80 — decommission

Case 80 grounds permanent/planned retirement behavior in older HDFS releases. Case 116 uses later maintenance state to show that expected outage horizon can change the preservation obligation.

Safe comparison:

> **decommission retirement admissibility != temporary-maintenance admissibility**.

Do not project Case 116's later states/expiry backward into the 0.18/2.7.3 decommission record.

### Case 68 — Dynamo membership/failure

Both systems distinguish temporary operational unavailability from durable/topological withdrawal.

**Functional analogy only:** Dynamo's local failure suspicion, explicit membership history, sloppy quorum, and hinted handoff are not HDFS's NameNode-administered maintenance state, minimum-replica rule, and expiry mechanism.

### Case 115 — HDFS snapshots

Case 115 shows retained historical metadata imposing a present replication obligation. Case 116 shows retained administrative/time metadata temporarily modifying how much redundancy must be live outside one planned-outage node.

The common point is only that **control metadata can govern present physical redundancy work**.

### Physical-retention cases

HDFS maintenance expiration is not a DRAM refresh deadline, SSD power-off retention rating, NAND charge-loss interval, magnetic decay time, or sanitization duration.

---

## Evidence-strength assessment

### Strong / directly grounded

- 2014 public HDFS maintenance-mode problem statement;
- 2015 proposed state split and maintenance-specific redundancy concept;
- HDFS-7877's 2017 resolution/fix-version boundary;
- released 2.9.0 maintenance-state reporting;
- released 3.0.1 maintenance/decommission distinction;
- `maintenanceExpireTimeInMS` storage and monitor behavior;
- live-vs-dead exit divergence;
- maintenance-specific reconstruction path.

### Moderate / bounded reconstruction

- `expected future return` as a retained policy assumption;
- `expiry revokes relaxed-dependency authority` as a cross-case retention formulation;
- treating a maintenance replica as an embodiment that remains retained/credited but is not ordinary service-authoritative.

These are faithful engineering abstractions, not Apache's period vocabulary.

### Not established

- broad invention genealogy;
- first production deployment;
- exact persistence of maintenance state/expiry through every NameNode HA/restart path;
- every Hadoop 3.x/modern semantic revision;
- erasure-coded maintenance behavior in all versions;
- real-cluster fault timing and convergence bounds;
- media erasure or sanitization.

---

## Evidence debt / future work

1. Recover the exact HDFS-7877 subtask/commit sequence that introduced each final state, configuration key, expiry field, and admin-guide statement.
2. Inspect NameNode edit-log/FSImage persistence and HA failover behavior for maintenance state and expiration in the first released versions.
3. Reproduce dead-node expiry and live-node return in a small HDFS cluster, recording replication queues, block-map transitions, and cleanup timing.
4. Audit erasure-coded HDFS maintenance separately rather than assuming the replicated-block threshold maps directly to striped redundancy.
5. Extend broad temporary-node-withdrawal / maintenance-mode genealogy in `computing-archaeology`, not in this retention-specific case.

## Related-repository check

A repository search during this round found no dedicated HDFS DataNode maintenance-state case in `tmzncty/computing-archaeology`. Case 116 therefore records only the retention-specific control relation. A broader HDFS/distributed-storage maintenance history should be routed to that companion repository if pursued.