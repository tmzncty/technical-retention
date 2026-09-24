# Evidence 116 Deepening — Hadoop 3.0.1 HA Maintenance Intent and Per-NameNode Refresh Boundaries

## Purpose

This packet deepens Case 116 by isolating one control-plane question that is easy to blur when discussing HDFS DataNode maintenance in an HA deployment:

> if maintenance intent and its expiration are present in the external host configuration, does one NameNode's refresh automatically prove that every NameNode has materialized the same current maintenance state?

For the inspected Hadoop 3.0.1 source, the bounded answer is **no**. The external host configuration is read into a `HostConfigManager` owned by a NameNode-side `DatanodeManager`; `refreshNodes()` then reevaluates that NameNode's own DataNode descriptors. The HA-capable test infrastructure likewise exposes refresh as an operation directed at a specific NameNode index.

This packet therefore separates:

- durable or shared **maintenance intent** from a NameNode's current in-memory interpretation of that intent;
- external policy bytes from a controller-local parsed policy snapshot;
- policy reload from DataNode admin-state materialization;
- one NameNode's materialization from demonstrated propagation into a peer NameNode;
- source-level control topology from a behavioral HA failover experiment.

It does **not** claim that a correctly operated HDFS HA deployment necessarily loses maintenance state on failover, that active-only refresh is the recommended workflow, or that maintenance itself is unsafe. The result is narrower: a single NameNode refresh is not source evidence of a replicated runtime maintenance-state transition at every NameNode.

---

## Exact implementation baseline

All implementation claims in this packet are pinned to Apache Hadoop commit:

- `496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0`
- Hadoop 3.0.1 source generation

The relevant files are:

1. `CombinedHostFileManager.java`
2. `DatanodeManager.java`
3. `FSNamesystem.java`
4. `NameNodeRpcServer.java`
5. `AdminStatesBaseTest.java`
6. `TestDecommission.java`
7. `TestMaintenanceState.java`

Pinning the commit matters because later Hadoop releases may alter command routing, host-provider behavior, HA tooling, or tests.

---

## Historical / source record

### 1. Maintenance intent lives in the host-provider input

`CombinedHostFileManager` implements a combined JSON host-file provider. In the inspected source, `refresh()` obtains the configured `dfs.hosts` path and passes it to a private refresh routine. That routine:

1. creates a new `HostProperties` object;
2. reads `DatanodeAdminProperties[]` from the configured file;
3. parses each entry;
4. adds each entry's administrative properties to the new object;
5. replaces the manager instance's previous `hostProperties` with the newly constructed object.

The same manager exposes maintenance expiration through:

```text
getMaintenanceExpirationTimeInMS(DatanodeID dn)
    -> hostProperties.getMaintenanceExpireTimeInMS(...)
```

The key source-level fact is therefore not merely that the file exists. A particular manager instance has a particular parsed `HostProperties` snapshot, and refresh replaces that snapshot.

**Historical/source statement:** Hadoop 3.0.1's combined host provider materializes the configured external policy into manager-local parsed state.

**Boundary:** this source does not require that the configured path reside on local storage; multiple NameNodes could refer to identical or shared bytes. The point is about *loading/materialization*, not about storage location.

### 2. `DatanodeManager.refreshNodes()` performs local policy reload and local descriptor reevaluation

The inspected `DatanodeManager.refreshNodes(Configuration conf)` does two relevant things:

```text
refreshHostsReader(conf)
    -> hostConfigManager.refresh()

refreshDatanodes()
    -> iterate a copy of this DatanodeManager's datanodeMap
```

For each `DatanodeDescriptor`, `refreshDatanodes()` queries the local `hostConfigManager` and then chooses among operations including:

- disallowing a node that is not included;
- `startMaintenance(node, maintenanceExpireTimeInMS)` when maintenance is requested and not expired;
- `startDecommission(node)` when excluded;
- `stopMaintenance(node)` / `stopDecommission(node)` otherwise;
- updating the node's upgrade domain.

This is direct source evidence for a two-stage control path:

```text
external host-policy representation
    -> HostConfigManager refresh
    -> local parsed policy snapshot
    -> local DatanodeDescriptor reevaluation
    -> local admin-state operation
```

It is not a source path of the form:

```text
refresh one NameNode
    -> serialize current host-policy snapshot into a replicated transaction
    -> peer NameNodes automatically materialize the same admin transition
```

### 3. The inspected RPC path targets the receiving NameNode's namesystem

The NameNode-side refresh RPC calls `namesystem.refreshNodes()`. The inspected `FSNamesystem.refreshNodes()` path delegates to that NameNode's block-management/DataNode-management layer, which in turn reloads the host provider as above.

For this packet, the important negative boundary is deliberately narrow:

> the inspected `refreshNodes` call path reloads and reevaluates the receiving NameNode's external host configuration; this path is not itself an edit-log publication of the external host-policy snapshot to peer NameNodes.

This is **not** a claim that no related effect can ever appear in an edit log elsewhere in HDFS. It is only a characterization of the inspected refresh path.

### 4. HA-capable test infrastructure makes the per-NameNode boundary explicit

`AdminStatesBaseTest` can create a simple HA topology using:

```text
MiniDFSNNTopology.simpleHATopology()
```

and explicitly transitions NameNode index `0` to active.

More importantly, the test helper is indexed by NameNode:

```text
refreshNodes(final int nnIndex)
    -> cluster.getNamesystem(nnIndex)
    -> getBlockManager()
    -> getDatanodeManager()
    -> refreshNodes(conf)
```

The common `takeNodeOutofService(...)` helper writes the requested decommission/maintenance entries to the JSON host file and then calls:

```text
refreshNodes(nnIndex)
```

The helper therefore treats the external policy write and a particular NameNode's policy refresh as distinct operations. Even in a test base capable of constructing an HA topology, refresh is addressed to a specific NameNode runtime.

This is strong source/test-topology evidence for:

```text
host file changed
    != every NameNode has necessarily reloaded it
```

It does **not** by itself prove the externally observable state of a standby after a particular production failover sequence; that requires a behavioral test.

### 5. Decommission tests corroborate separate standby-side admin processing, but are not maintenance proof

Hadoop 3.0.1 includes decommission coverage involving a standby NameNode. This is useful only as a bounded corroboration that administrative processing can be discussed per NameNode in the HA test environment.

It is not acceptable to turn that into:

```text
decommission test
    == maintenance failover test
```

Decommission and maintenance have different admission, replica-accounting, and expiry semantics in Case 116. This packet therefore does not use the decommission test as the primary proof of maintenance behavior.

### 6. The inspected maintenance test does not close the HA failover seam

The existing `TestMaintenanceState` suite grounds many maintenance semantics, but in the inspected Hadoop 3.0.1 version no dedicated maintenance regression was identified that performs the exact sequence needed here:

```text
write maintenance intent
    -> refresh only active NameNode
    -> observe active vs standby
    -> fail over
    -> observe maintenance admin state before peer refresh
```

That absence is stated narrowly as a result of this inspection. It is not a claim that no later Hadoop release, downstream distribution, or external test suite contains such coverage.

---

## Engineering reconstruction

The following vocabulary is repository analysis, not historical Hadoop terminology.

### A. Per-controller policy snapshot

A **per-controller policy snapshot** is the parsed host-provider state currently held by one NameNode's host configuration manager.

The source supports the distinction:

```text
external maintenance intent exists
    != NameNode A has loaded current intent
    != NameNode B has loaded current intent
```

Even if both NameNodes are configured to read the same pathname or byte-identical file, each controller still performs its own read/parse/replace operation before its local manager snapshot is known to be current.

### B. Controller-local materialization

**Controller-local materialization** is the act of taking a loaded policy snapshot and applying it to that controller's current `DatanodeDescriptor` state via `refreshDatanodes()`.

That gives a longer chain:

```text
operator intent
    -> external host-file representation
    -> controller-local host-provider snapshot
    -> local DataNode descriptor reevaluation
    -> start/stop maintenance operation
    -> local maintenance-state progression
```

Each arrow is a separate relation. The existence of an earlier representation does not prove every later representation is already current.

### C. Independently materialized maintenance intent

For an HA pair, the source topology is consistent with:

```text
                 external host policy
                        |
              +---------+---------+
              |                   |
              v                   v
      NameNode A refresh   NameNode B refresh
              |                   |
              v                   v
       snapshot A            snapshot B
              |                   |
              v                   v
     admin state A         admin state B
```

The two branches can converge because they read equivalent policy and observe equivalent cluster state. But convergence should not be confused with proof of synchronous propagation from A's refresh into B's in-memory state.

Repository shorthand:

```text
same external policy source
    + independent refresh/re-observation
    -> potentially convergent controller state
```

not:

```text
refresh A
    -> by itself proves current materialization at B
```

### D. Maintenance obligation can outlive one controller representation

The existing Case 116 restart packet already establishes that maintenance admin state is reconstructible from durable external host configuration plus live cluster observations after NameNode restart.

This HA slice adds another axis:

```text
maintenance obligation persists in external policy
    != every controller replica currently carries an up-to-date in-memory representation
```

This is a control-state continuity result, not a payload-retention result.

### E. Policy persistence and replicated namespace history are different authorities

The host-provider file is an external administrative input. The namespace edit log is a different persistence mechanism. The inspected refresh path does not justify collapsing them into one thing.

Therefore:

```text
namespace history replicated
    != external maintenance policy snapshot replicated
```

and:

```text
HA namespace failover capability
    != proof that every external-control input was refreshed identically
```

This distinction is particularly important for timeout-bearing maintenance intent, because an expiration timestamp can remain durable in an external representation while a controller's current local interpretation depends on whether that representation has been loaded and reevaluated.

---

## State matrix for the unresolved HA seam

The source permits the following analytical matrix. The rows are not claimed as measured runtime results; they identify states a behavioral test should distinguish.

| External host policy | NN A refreshed | NN B refreshed | What source evidence proves | What remains experimental |
| --- | --- | --- | --- | --- |
| old | no | no | both may retain earlier local snapshots | exact observable admin states |
| new maintenance intent | yes | no | A executes its refresh/re-evaluation path; B has not been proven refreshed by A's call | B's exact current admin state; failover outcome |
| new maintenance intent | yes | yes | both independently execute refresh/re-evaluation | convergence timing and any race |
| maintenance removed | yes | no | A can stop maintenance from current policy; B is not proven refreshed by A | behavior after immediate failover |
| expiration crossed | one side re-evaluates | other side not re-evaluated | maintenance expiration is a policy/control boundary in existing Case 116 evidence | exact HA transition timing across failover |

The crucial methodological point is:

> source topology identifies a seam; it does not replace a fault/failover trace through that seam.

---

## What this packet closes

### Closed at source level

1. `CombinedHostFileManager` loads the external host file into a manager-local replacement `HostProperties` snapshot.
2. maintenance expiration is queried from that local snapshot.
3. `DatanodeManager.refreshNodes()` invokes that local host-provider refresh and reevaluates that manager's local DataNode map.
4. the HA-capable `AdminStatesBaseTest` exposes refresh as an operation directed to a specific NameNode index.
5. external policy mutation and NameNode refresh are therefore distinct control operations in the inspected implementation/test infrastructure.
6. refreshing one NameNode is not, by the inspected call path alone, evidence that a peer NameNode has loaded the same current host-policy snapshot.

### Still open

1. actual standby state after active-only maintenance refresh;
2. actual failover behavior before standby refresh;
3. whether particular operational tooling or distributions deliberately refresh both NameNodes;
4. behavior when maintenance expiration crosses during active/standby transition;
5. differences between controlled failover, standby restart, active restart, and full HA restart;
6. later-version changes that may add stronger synchronization or tests.

---

## Functional comparison only

These comparisons are structural, not genealogical.

### Case 25 — Swift reconstructive retry

Case 25 shows a different setting where maintenance work need not preserve one volatile continuation object: surviving local/remote state can be re-observed and a later run can reconstruct work authority.

The bounded functional analogy is:

```text
surviving external evidence
    + later re-observation
    -> reconstruct current maintenance work/state
```

HDFS host-policy refresh is not Swift SSYNC, and no lineage is asserted.

### Case 142 — Ceph capacity-gated repair

Case 142 distinguishes a maintenance obligation from a current execution/admission authority. Case 116 similarly shows that a maintenance intention outside a controller is not identical to that controller's current local materialization.

Again, this is a vocabulary-level comparison only.

---

## Philosophical interpretation

Separated deliberately from the historical and engineering record:

> A durable obligation may persist outside a controller while one controller's present in-memory representation of that obligation is stale, absent, or not yet re-materialized.

For technical-retention purposes this is useful because it prevents a common category error: treating persistence of a *rule or obligation* as identical to persistence of every runtime structure that currently enforces it.

No philosophical interpretation is used as evidence for Hadoop behavior.

---

## Explicit non-claims

This packet does **not** establish any of the following:

1. HDFS HA necessarily loses DataNode maintenance state on failover.
2. Refreshing only the active NameNode is the documented or recommended operator procedure.
3. The standby can never learn equivalent state through some other observation or later refresh.
4. Maintenance state is stored only in the JSON host file in every Hadoop version or provider implementation.
5. The inspected refresh path proves that no related state is ever recorded in the edit log anywhere else.
6. Shared host-file bytes imply shared in-memory `HostProperties` objects.
7. A local host-file path and a shared-filesystem path have identical failure properties.
8. Decommission behavior is identical to maintenance behavior.
9. A decommission standby test proves the maintenance failover seam.
10. The absence of a dedicated regression in the inspected maintenance test file proves that no such test exists in later Hadoop releases.
11. A maintenance request has completed merely because the host file contains the request.
12. A loaded maintenance request has completed admission merely because `refreshNodes()` returned.
13. Both NameNodes will necessarily diverge if only one is refreshed.
14. Both NameNodes will necessarily converge at the same instant if both are refreshed.
15. DataNode heartbeats alone recreate the external maintenance expiration if the receiving NameNode has not loaded that policy.
16. Namespace HA replication and host-policy refresh are the same mechanism.
17. Policy staleness implies payload loss.
18. Administrative-state divergence implies block corruption.
19. Maintenance expiration is a physical-media retention deadline.
20. Controlled failover and crash failover exercise identical timing.
21. Standby restart and active failover exercise identical reconstruction paths.
22. This source inspection is a replacement for a two-NameNode behavioral trace.
23. Hadoop originated the general idea of independently materialized external maintenance policy.
24. Any cross-case comparison in this packet establishes historical influence.

---

## Highest-value next experiment

A focused HA regression/fault trace should make the source-level seam observable:

```text
1. start two NameNodes in simple HA with CombinedHostFileManager
2. place a DataNode under maintenance with a bounded expiration
3. write the shared/external host-policy representation
4. refresh active NameNode only
5. inspect active and standby DataNode admin states independently
6. fail over before explicitly refreshing the former standby
7. observe the new active's immediate interpretation
8. explicitly refresh and observe convergence
9. repeat after refreshing both NameNodes before failover
10. repeat with the expiration boundary crossed during the sequence
11. distinguish controlled failover from standby restart
```

The strongest output would record, at each cut point:

- host-file contents and timestamp/version surrogate;
- active/standby identity;
- each NameNode's observed DataNode admin state;
- stored maintenance expiration in each descriptor;
- reconstruction/replication actions;
- state before and after explicit refresh;
- state before and after failover.

That would convert the current result from **source-topology evidence** into a direct behavioral HA retention trace.

---

## Evidence classification

| Layer | Result |
| --- | --- |
| Historical / source record | Hadoop 3.0.1 external host policy is parsed by a NameNode-local host manager and applied through that NameNode's `DatanodeManager.refreshNodes()` |
| Engineering reconstruction | maintenance intent can be durably represented outside a controller while controller-local materialization remains a separate step |
| Functional analogy | later re-observation/reconstruction can preserve an obligation without preserving one volatile controller representation |
| Philosophical interpretation | persistence of an obligation is not identical to simultaneous persistence of all runtime representations of it |

Case 116 should remain **`grounded`**. This packet closes a source-level boundary but does not supply the HA failover experiment needed for a stronger maturity claim.

---

## Primary sources

All source links below are pinned to Apache Hadoop commit `496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0`.

- `CombinedHostFileManager.java`  
  <https://github.com/apache/hadoop/blob/496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/CombinedHostFileManager.java>

- `DatanodeManager.java`  
  <https://github.com/apache/hadoop/blob/496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/DatanodeManager.java>

- `FSNamesystem.java`  
  <https://github.com/apache/hadoop/blob/496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.java>

- `NameNodeRpcServer.java`  
  <https://github.com/apache/hadoop/blob/496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/NameNodeRpcServer.java>

- `AdminStatesBaseTest.java`  
  <https://github.com/apache/hadoop/blob/496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0/hadoop-hdfs-project/hadoop-hdfs/src/test/java/org/apache/hadoop/hdfs/AdminStatesBaseTest.java>

- `TestDecommission.java`  
  <https://github.com/apache/hadoop/blob/496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0/hadoop-hdfs-project/hadoop-hdfs/src/test/java/org/apache/hadoop/hdfs/TestDecommission.java>

- `TestMaintenanceState.java`  
  <https://github.com/apache/hadoop/blob/496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0/hadoop-hdfs-project/hadoop-hdfs/src/test/java/org/apache/hadoop/hdfs/TestMaintenanceState.java>

### Related Case 116 packets

- [`116-hadoop-2014-2018-datanode-maintenance-grounding.md`](116-hadoop-2014-2018-datanode-maintenance-grounding.md)
- [`116-hadoop-2014-2017-maintenance-expiry-clock-persistence-genealogy-deepening.md`](116-hadoop-2014-2017-maintenance-expiry-clock-persistence-genealogy-deepening.md)
- [`116-hadoop-301-maintenance-restart-reconstitution-deepening.md`](116-hadoop-301-maintenance-restart-reconstitution-deepening.md)
- [`116-hadoop-335-336-ec-maintenance-sufficiency-deepening.md`](116-hadoop-335-336-ec-maintenance-sufficiency-deepening.md)

---

## Reuse check

A fresh repository search of `tmzncty/computing-archaeology` for HDFS maintenance / standby / failover material did not identify a dedicated packet that could be reused directly for this seam. This is a search result for this run, not an exhaustive proof that the archaeology repository contains no related sentence. The present packet therefore stays narrowly focused on retention/control semantics instead of constructing a broader HDFS HA history.
