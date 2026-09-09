# Evidence 116 — Hadoop 3.0.1 Maintenance Restart Reconstitution

## Scope

This deepening closes one bounded follow-up question from Case 116:

> **In the released Hadoop 3.0.1 implementation, what survives a NameNode restart as durable maintenance intent, and what runtime replica relation must instead be reconstructed or re-observed?**

The inspected boundary is the exact Apache Hadoop `rel/release-3.0.1` tag, whose annotated tag points to commit `496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0` and is dated 23 March 2018. The claim is therefore release-specific. It is not a general statement about all later HDFS HA/failover implementations, and it does not claim that every maintenance-related field is or is not serialized in FSImage/edit logs.

This slice is intentionally about **restart reconstitution of retention-control relations**, not generic Hadoop restart history.

## Source custody and exact locations

Primary Apache sources, all inspected at commit `496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0`:

1. Apache Hadoop annotated tag `rel/release-3.0.1` — tag object `f8f37e90115ef5de75643fa980aa3ff5fd1ffc18`, pointing to commit `496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0`.
   - <https://github.com/apache/hadoop/tree/496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0>
2. `HdfsDataNodeAdminGuide.md` — section describing the combined JSON hosts file, `adminState: IN_MAINTENANCE`, `maintenanceExpireTimeInMS`, and the `-refreshNodes` workflow.
   - <https://github.com/apache/hadoop/blob/496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0/hadoop-hdfs-project/hadoop-hdfs/src/site/markdown/HdfsDataNodeAdminGuide.md>
3. `CombinedHostFileManager.java` — `refresh()` and `getMaintenanceExpirationTimeInMS(...)`.
   - <https://github.com/apache/hadoop/blob/496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/CombinedHostFileManager.java>
4. `DatanodeManager.java` — constructor host-configuration refresh and `startAdminOperationIfNecessary(...)` on DataNode registration.
   - <https://github.com/apache/hadoop/blob/496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/DatanodeManager.java>
5. `TestMaintenanceState.java` — project regression tests covering NameNode restart while maintenance nodes/replicas are present, including the dead-maintenance-node case in which the restarted NameNode initially restores ordinary live replicas because it does not yet know that the maintenance node still carries a replica.
   - <https://github.com/apache/hadoop/blob/496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0/hadoop-hdfs-project/hadoop-hdfs/src/test/java/org/apache/hadoop/hdfs/TestMaintenanceState.java>

A fresh repository search in `tmzncty/computing-archaeology` for HDFS maintenance/restart material found no dedicated overlapping study to reuse. Broader NameNode/HA history remains a companion-repository task if pursued.

---

## Historical record

### H/P — released 3.0.1 makes maintenance intent and expiry external host-configuration properties

The released DataNode Administration guide requires the combined JSON host-file format for maintenance mode. Its host records can carry an administrative state of `IN_MAINTENANCE` and a `maintenanceExpireTimeInMS` epoch value; operators change host-level state in the hosts file and ask the NameNode to refresh nodes.

This gives the bounded release an externally retained configuration representation for two relations that Case 116 already treats as retention-control state:

```text
wanted maintenance administrative state
+
maintenance expiry horizon
```

The guide's configuration representation should not be confused with the current in-memory `DatanodeDescriptor` or with a block-replica location report.

### H/P — released source reloads that host configuration into a fresh NameNode process

`DatanodeManager` constructs the configured host-file manager and calls its `refresh()` path. In the combined-host implementation, `CombinedHostFileManager.refresh()` reads the configured hosts file and replaces the manager's in-memory host properties.

`CombinedHostFileManager.getMaintenanceExpirationTimeInMS(...)` returns the configured expiry for entries whose administrative state is `IN_MAINTENANCE`. `DatanodeManager.startAdminOperationIfNecessary(...)` consults that value when a DataNode registers and calls `startMaintenance(...)` when the configured maintenance condition is applicable.

Therefore, within this exact release path:

> **maintenance intent and its expiry can be reconstituted from retained host configuration rather than requiring the old Java object graph to survive process restart.**

This is a source-of-truth statement about the inspected code path, not a claim that no related state is ever stored elsewhere.

### H/P — the released test suite distinguishes restart-surviving policy from runtime knowledge of a dead maintenance replica

`TestMaintenanceState` contains a NameNode-restart scenario in which a maintenance DataNode carrying a replica is down. After NameNode restart, the test expects HDFS to restore the ordinary number of live replicas because the restarted NameNode does not yet know that the absent maintenance DataNode has that replica. When the DataNode returns, the maintenance replica relation is again visible and the test can observe both the live replicas and the maintenance replica.

The same test class also checks that out-of-service nodes represented in the block map remain appropriately represented across a NameNode restart in the bounded scenarios it exercises.

These are Apache project regression tests, not independent production validation. Their value here is narrower: they expose which relations the implementation deliberately treats differently at restart.

---

## Engineering reconstruction

### E — persisted admin intent != persisted runtime replica-location knowledge

The restart path exposes at least two retention contracts:

```text
host JSON
    -> retained desired admin relation + expiry
    -> reloaded by fresh NameNode process

runtime block / DataNode observations
    -> knowledge that a particular DataNode currently embodies a replica
    -> may require post-restart re-observation / DataNode return
```

The first relation can survive by configuration replay. The bounded dead-maintenance-node test demonstrates that the second relation is not simply assumed to have identical restart persistence semantics: the NameNode can compensate with ordinary live replicas while the maintenance holder is absent and unknown.

### E — policy survival != service-side reliance survival

It is possible for the system to retain the operator's statement “this host is in maintenance until time T” while declining, after restart, to rely on an unobserved dead host as though its replica were presently available evidence.

Thus:

> **surviving policy authority does not imply surviving operational credit for every embodiment named by that policy.**

This is particularly important because Case 116's maintenance optimization relies on expected return. After restart, the expectation can remain configured while runtime topology evidence is rebuilt more conservatively.

### E — temporary dependency credit before restart != guaranteed durable restart credit

Before restart, a known maintenance replica may be counted within the maintenance regime while ordinary live-replica obligations are relaxed. In the bounded regression scenario, a restarted NameNode that does not know the dead maintenance node's replica restores ordinary live replicas instead of treating the old credit as unquestioned durable knowledge.

That yields a useful stop condition:

> **an optimization based on presently known embodiment does not automatically become a durable restart promise.**

This does not mean the replica bytes vanished. It means the authority to rely on their known location is a different retained relation from the bytes themselves.

### E — NameNode restart != DataNode restart / re-registration

A NameNode process restart reconstructs control state from configuration and runtime discovery paths. A DataNode's later return/re-registration is a separate event that can supply fresh evidence about embodiment and bring the maintenance relation back into active block accounting.

Do not collapse these into one generic “restart persistence” claim.

### E/X — host-config-derived reconstruction != proven FSImage/edit-log serialization

The inspected materials are sufficient to show a configuration-derived reconstruction path. They are **not** sufficient to prove a repository-wide negative such as “maintenance state is never serialized in FSImage/edit logs,” nor a positive such as “all maintenance runtime state is checkpointed there.”

That question remains outside this bounded slice unless separately traced through image/edit-log serialization code and failover tests.

---

## Functional comparison

### A/X — Case 79 HDFS startup re-observation is a bounded same-system analogy, not mechanism identity

Case 79 grounds the older HDFS startup distinction between durable namespace/block metadata and block-to-DataNode location knowledge rebuilt by DataNode reports. Case 116's 3.0.1 maintenance path presents a related shape:

- desired maintenance state and expiry have an external configuration source of truth;
- runtime knowledge that an absent DataNode currently embodies a usable replica can require re-observation.

The analogy is useful because both cases separate **retained policy/metadata** from **runtime evidence reconstructed from participants**. But the mechanisms are not interchangeable: startup SafeMode thresholds and BlockReports are not the same state machine as maintenance admission, expiry, or `CombinedHostFileManager`.

No genealogy claim is made.

### A/X — this is not a generic distributed consensus or lease case

`maintenanceExpireTimeInMS` is an operator-supplied maintenance horizon in the inspected HDFS design. Nothing here establishes quorum lease semantics, consensus-log replication of the relation, or a universal distributed “maintenance lease” abstraction.

---

## Philosophical interpretation

### I — persistence can be split across state classes with different restart contracts

A narrow interpretation is now defensible:

> **A technical preservation relation can survive restart through one retained representation while the evidence needed to rely on a particular physical embodiment must be re-observed.**

Here the operator's maintenance intention and expiry can persist as configuration, while runtime replica-location knowledge has a different restart contract. The resulting continuity is therefore neither “everything persisted” nor “everything was reconstructed from scratch.”

Do not inflate this into “memory of memory,” a universal theory of distributed storage, or a claim that configuration is intrinsically more authoritative than runtime evidence. The authority ordering is specific to the bounded HDFS paths inspected here.

---

## Explicit non-equivalences fixed by this deepening

- `persisted host-admin intent != in-memory DatanodeDescriptor continuity`;
- `persisted maintenance expiry != persisted runtime replica-location knowledge`;
- `known replica before restart != automatically credited replica after restart`;
- `replica bytes may physically survive != NameNode presently knows/credits that embodiment`;
- `maintenance policy survives != relaxed-redundancy reliance necessarily survives unchanged`;
- `NameNode restart != DataNode return/re-registration`;
- `configuration replay != proof of FSImage/edit-log serialization`;
- `Apache regression test != independent production validation`;
- `same-system functional analogy != mechanism identity or genealogy`.

---

## What remains open

This slice does **not** close:

1. exact HDFS-7877 subtask/commit genealogy before the released 3.0.1 state;
2. full HA active/standby failover semantics and whether every path behaves identically to the bounded process-restart tests;
3. exact FSImage/edit-log serialization status for every maintenance-related field;
4. erasure-coded block-group maintenance semantics;
5. expiry/dead-node convergence under injected failures;
6. broad maintenance-mode history across distributed storage systems.

Those are separate research slices. The broader implementation/history items should primarily be routed to `computing-archaeology` if developed.
