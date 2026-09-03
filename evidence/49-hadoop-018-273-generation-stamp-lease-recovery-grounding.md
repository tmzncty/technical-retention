# Case 49 grounding — HDFS generation stamps, lease recovery, and last-block convergence

## Promotion target

Ground [`cases/49-apache-hdfs-generation-stamp-lease-recovery.md`](../cases/49-apache-hdfs-generation-stamp-lease-recovery.md) as a bounded distributed-retention case without turning one Hadoop release into a complete HDFS history.

**Result:** `grounded`.

The central relation is directly supported by Apache primary sources:

> a surviving HDFS block replica is not automatically current merely because its bytes still exist; lease recovery qualifies replicas through generation, length, state, recovery authority, and a NameNode metadata transition.

---

## Bounded evidence set

### A. Apache JIRA HADOOP-3283 — generation-stamp mechanism for append

- **Issue:** `Need a mechanism for data nodes to update generation stamps.`
- **Created:** 18 April 2008.
- **Resolved:** 25 April 2008.
- **Fix version:** Hadoop 0.18.0.
- **Direct historical statement:** for the HDFS append work, a generation stamp is added to each block and DataNodes need a mechanism to update generation stamps for lease recovery.
- **Use here:** establishes that generation stamps and their recovery update path predate Hadoop 2.7.3 and were explicitly connected to append/lease recovery by historical actors.
- **URL:** <https://issues.apache.org/jira/browse/HADOOP-3283>

### B. Apache JIRA HADOOP-3310 — lease recovery for append

- **Issue:** `Lease recovery for append`.
- **Created:** 24 April 2008.
- **Resolved:** 2 June 2008.
- **Fix version:** Hadoop 0.18.0.
- **Release-note statement:** lease recovery was implemented to synchronize the last block of a file; protocol support was added for triggering block recovery, block synchronization, and block update.
- **Direct historical statement:** lease recovery is performed when replicas of a block in a lease may have different generation-stamp values.
- **Use here:** strongest early primary source for the problem historical actors were explicitly solving.
- **URL:** <https://issues.apache.org/jira/browse/HADOOP-3310>

### C. Apache JIRA HADOOP-1700 — append umbrella

- **Issue:** `Append to files in HDFS`.
- **Fixed:** Hadoop 0.19.0.
- **Use here:** places HADOOP-3283 and HADOOP-3310 inside the append feature lineage and prevents a false claim that 2.7.3 originated the mechanism.
- **URL:** <https://issues.apache.org/jira/browse/HADOOP-1700>

### D. Hadoop 2.7.3 release/tag

- **Release tag:** `rel/release-2.7.3`.
- **Annotated tag date:** 25 August 2016.
- **Release commit:** `baa91f7c6bc9cb92be5982de4719c1c8af91ccff`.
- **Use here:** gives a reproducible implementation snapshot rather than relying on current `trunk` semantics.
- **Release page:** <https://hadoop.apache.org/docs/r2.7.3/>
- **Commit:** <https://github.com/apache/hadoop/commit/baa91f7c6bc9cb92be5982de4719c1c8af91ccff>

### E. Hadoop 2.7.3 `LeaseManager.java`

- **Path:** `hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/LeaseManager.java`
- **Version:** release commit above.
- **Direct source evidence:** class comment says `LeaseManager` performs lease housekeeping and provides lease-recovery methods.
- **Direct source evidence:** its explicit recovery algorithm says:
  1. NameNode retrieves lease information;
  2. considers the last block of each file;
  3. identifies DataNodes containing that block and selects a primary;
  4. the primary obtains a new generation stamp from the NameNode;
  5. gathers block information from each DataNode;
  6. computes the minimum block length;
  7. updates DataNodes with a valid generation stamp to the new stamp and minimum length;
  8. acknowledges results;
  9. NameNode updates `BlockInfo`, removes the file/lease relation, and commits changes to the edit log.
- **Use here:** directly grounds the bounded recovery sequence and the `minimum recovered length != maximum surviving bytes` reconstruction.
- **URL:** <https://github.com/apache/hadoop/blob/baa91f7c6bc9cb92be5982de4719c1c8af91ccff/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/LeaseManager.java>

### F. Hadoop 2.7.3 `BlockInfoContiguousUnderConstruction.java`

- **Path:** `hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/BlockInfoContiguousUnderConstruction.java`
- **Version:** same release commit.
- **Direct source evidence:** the class represents a block currently being constructed, usually the last block of a file open for write or append.
- **Direct source evidence:** each under-construction replica records generation stamp, length, and state reported by its DataNode.
- **Direct source evidence:** an expected storage location is *not guaranteed* actually to contain the corresponding replica.
- **Direct source evidence:** `blockRecoveryId` is the new generation stamp after successful recovery and is also used to identify the correct recovery if abandoned recoveries reappear.
- **Direct source evidence:** `initializeBlockRecovery()` moves the block to `UNDER_RECOVERY`, records the recovery ID, and chooses an alive primary.
- **Direct source evidence:** `setGenerationStampAndVerifyReplicas()` removes replicas with a generation stamp different from the final stamp and logs them as stale.
- **Direct source evidence:** conversion to a complete block is conditioned on committed generation/length state and sufficient reported replicas.
- **Use here:** grounds replica admissibility, recovery fencing, expected-location/observed-existence separation, and the distinction between bytes and block control state.
- **URL:** <https://github.com/apache/hadoop/blob/baa91f7c6bc9cb92be5982de4719c1c8af91ccff/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/BlockInfoContiguousUnderConstruction.java>

### G. Hadoop 2.7.3 HDFS Architecture

- **Document:** `HDFS Architecture`.
- **Last published for this version:** 18 August 2016.
- **Direct source evidence:** a file is split into replicated blocks on DataNodes; NameNode controls namespace and block mapping/replication; files have strictly one writer at any time in this bounded model.
- **Direct source evidence:** NameNode metadata changes are persisted in the EditLog; checksum verification is described separately as a data-integrity mechanism.
- **Use here:** establishes architectural context, keeps generation/currentness separate from checksum integrity, and supports the final metadata/edit-log recovery boundary.
- **URL:** <https://hadoop.apache.org/docs/r2.7.3/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html>

### H. Apache JIRA HDFS-1149 — negative evidence for crash-persistent recovery authority

- **Issue:** `Lease reassignment is not persisted to edit log`.
- **Fixed:** Hadoop 0.23.0.
- **Direct problem statement:** during lease recovery the lease was reassigned to a special NameNode holder but the reassignment was not persisted; after a NameNode restart the original leaseholder could again allocate blocks or complete a file whose recovery had already begun.
- **Use here:** demonstrates that recovery authority/control state can be correct in volatile NameNode state yet fail its purpose across restart unless the transition is durably represented.
- **URL:** <https://issues.apache.org/jira/browse/HDFS-1149>

---

## Claim ledger

| Claim | Label | Evidence | Strength / boundary |
| --- | --- | --- | --- |
| generation stamps were introduced in the append work before 2.7.3 | `H/P` | HADOOP-3283; HADOOP-1700 | strong; blocks a 2.7.3 invention claim |
| lease recovery was explicitly designed to synchronize a last block whose replicas could have different generation stamps | `H/P` | HADOOP-3310 | strong historical problem statement |
| 2.7.3 recovery selects a primary, obtains a new generation stamp, gathers replica state, computes minimum length, updates valid-stamp replicas, then updates NameNode metadata/edit log | `H/P` | 2.7.3 `LeaseManager.java` | strong implementation-level source comment |
| under-construction replica state includes reported generation, length, and state | `H/P` | `BlockInfoContiguousUnderConstruction.java` | strong |
| an expected replica location is not proof that a replica physically exists there | `H/P` | same source | strong |
| a mismatching generation stamp can make a replica stale and removed from current block membership | `H/P` | same source | strong |
| recovery ID/new generation is used to identify the right recovery if abandoned recoveries reappear | `H/P` | same source | strong |
| physical replica presence is insufficient for currentness | `E` | generation-stamp verification + stale-replica removal | strong reconstruction |
| maximum surviving length is not necessarily the recovered length | `E` | `LeaseManager` minimum-length rule | strong for this bounded algorithm; not universalized to all releases/recovery paths |
| the minimum-length rule preserves a common admissible prefix rather than the longest observed suffix | `E` | minimum-length rule | bounded reconstruction; “common prefix” is project wording |
| generation stamp is not a checksum | `H/E` | separate generation/currentness source + HDFS Architecture checksum section | strong separation |
| generation stamp is not a Dynamo vector clock or consensus term | `A/X` | source semantics + Cases 23/26/46 | functional comparison only; no genealogy claimed |
| recovery authority must itself survive relevant failures | `H/E` | HDFS-1149 | unusually strong negative historical evidence |
| lease recovery alone restores the configured replication factor | `X` | not established by bounded source set | explicitly rejected |
| truncating a disputed suffix securely erases its physical traces | `X` | not established | explicitly rejected |

---

## Exact mechanism boundary

The evidence supports this bounded chain:

```text
single writer / lease
        |
        v
last block under construction
        |
        +---- replica A: generation g, length LA
        +---- replica B: generation g, length LB
        +---- replica C: stale/other generation
        |
        v
lease recovery
        |
        +---- new generation / recovery ID
        +---- primary gathers replica states
        +---- common minimum length chosen
        +---- valid replicas updated
        |
        v
NameNode BlockInfo + lease state
        |
        v
edit-log commit
```

The diagram is an **engineering reconstruction** of relationships explicitly named in the source; it is not Apache's own published diagram.

---

## Counterexample value

This case is valuable because it breaks several tempting equations.

### `replica presence = current state`

Rejected. The source explicitly removes stale-generation replicas.

### `more surviving bytes = more recoverable truth`

Rejected for the bounded recovery rule. Recovery computes a minimum block length rather than automatically preferring the longest replica.

### `one block ID = one fully specified retained state`

Rejected. Generation stamp, length, under-construction state, lease/recovery authority, and replica reports all qualify what the block currently means.

### `successful in-memory recovery transition = crash-persistent authority transition`

Rejected by HDFS-1149.

### `version evidence = integrity evidence`

Rejected. HDFS architecture describes checksums separately from the generation/recovery mechanism.

---

## Cross-case controls

### Case 26 / GFS inactive-chunk integrity

Functional bridge: both GFS and HDFS can have physically surviving replicated data that is rejected as current because version/currentness metadata says otherwise.

Boundary: GFS chunk-version/checksum/replication semantics and HDFS generation-stamp/lease-recovery semantics are not identical mechanisms and no genealogy is inferred here.

### Case 23 / Dynamo

Functional bridge: retained version metadata changes which surviving values count.

Boundary: Dynamo vector clocks encode causal ancestry and may retain concurrent versions; an HDFS generation stamp in this case identifies block generation/recovery currentness. `generation stamp != vector clock`.

### Case 48 / Cassandra incremental repair state

Functional bridge: maintenance/recovery transitions have their own retained identity/state.

Boundary: Cassandra `pendingRepair` prevents an in-progress anti-entropy repair from being mistaken for completed maintenance; HDFS recovery ID/new generation fences the current block recovery against abandoned attempts. The objects and correctness conditions differ.

### Case 46 / GFS master recovery

Functional bridge: payload survival and metadata/authority recovery are distinct.

Boundary: Case 46 is master restart reconstruction through log/checkpoint/re-observation; Case 49 is last-block convergence after writer/lease failure.

---

## `computing-archaeology` reuse check

Searched `tmzncty/computing-archaeology` for HDFS, generation-stamp, lease-recovery, and block-recovery coverage before writing. No dedicated case was found.

Therefore this slice does not duplicate a pre-existing companion-repository history. If a broader HDFS historical genealogy is later developed there, this case should link to it and retain only the currentness/recovery comparison.

---

## Maturity decision

**Promote to `grounded`.**

Why:

- early Apache issue records establish the historical problem and prior-art date boundary;
- the exact Hadoop 2.7.3 release commit gives reproducible implementation evidence;
- the release source explicitly states the recovery algorithm and currentness/fencing fields;
- versioned Apache architecture documentation supplies system/edit-log/integrity context;
- HDFS-1149 supplies a concrete historical failure showing that volatile recovery authority is insufficient across NameNode restart;
- counterexamples and non-claims are explicit;
- the related repository was checked for duplicate treatment.

Remaining work is intentionally separate: later HDFS recovery evolution, pipeline-recovery variants, NameNode HA/fencing, modern erasure-coded HDFS, and fault-injection validation should not be silently folded into this bounded case.
