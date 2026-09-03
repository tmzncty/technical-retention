# Apache HDFS Generation-Stamp Lease Recovery: Replica Currentness, Common-Length Convergence, and Recovery Fencing

## Scope

- **Bounded system:** Apache Hadoop HDFS append/lease-recovery lineage introduced around Hadoop 0.18–0.19, examined through the released Hadoop **2.7.3** source snapshot tagged on 25 August 2016.
- **Bounded mechanism:** a file open for write/append, its last under-construction block, the file lease, per-block generation stamp, replica-reported length/state, recovery ID, primary-DataNode block synchronization, and final NameNode metadata/edit-log transition.
- **Primary source base:** Apache JIRA HADOOP-3283, HADOOP-3310, and HADOOP-1700; Apache Hadoop 2.7.3 `LeaseManager` and `BlockInfoContiguousUnderConstruction` source; the versioned HDFS Architecture document; HDFS-1149 as an earlier failure/correction record for crash-persistent recovery authority.
- **Research question:** when several physical replicas of the last block survive a failed writer but disagree about generation or length, what retained relations decide which bytes still count as the file and how a new recovery attempt supersedes abandoned ones?

This is **not** a general HDFS history. It does not cover NameNode HA, snapshots, erasure coding, general pipeline replacement, safemode, or every later lease-recovery change. Case 46 already covers GFS master-log/checkpoint recovery; Cases 41 and 48 cover Cassandra deletion/repair state. This case isolates **HDFS last-block currentness and writer-failure convergence**.

The bounded retention claim is:

> **HDFS can retain several physical embodiments of an under-construction block while refusing to treat their mere survival as sufficient currentness. Lease recovery gathers replica state, advances the generation/recovery epoch, chooses a length that the participating valid replicas can share, updates those replicas, then commits the resulting block/file state at the NameNode. Persistence therefore depends on retained authority and version/length relations as well as bytes. In the bounded algorithm, recovery may deliberately discard a longer surviving suffix so the file converges on a common admissible prefix.**

`replica admissibility`, `common-length convergence`, `recovery epoch`, and `authority retention` below are project terms. Apache historical vocabulary includes `lease`, `lease recovery`, `generation stamp`, `block recovery`, `UNDER_CONSTRUCTION`, `UNDER_RECOVERY`, `COMMITTED`, `primary datanode`, and `edit log`.

---

## Historical vocabulary and prior-art boundary

### Direct Apache vocabulary

The bounded sources use:

- `append`;
- `lease` and `lease recovery`;
- `generation stamp`;
- `block` and `replica`;
- `primary datanode` during recovery;
- `block recovery ID`;
- `UNDER_CONSTRUCTION`, `UNDER_RECOVERY`, and `COMMITTED`;
- `minimum block length`;
- `stale replica`;
- `BlockInfo`;
- `edit log`.

### Origin boundary

Hadoop 2.7.3 is a **snapshot of an already mature mechanism**, not an invention-priority date.

HADOOP-3283, created in April 2008 and fixed for Hadoop 0.18.0, says that a generation stamp was being added to each block for file append and that DataNodes needed a mechanism to update generation stamps for lease recovery. HADOOP-3310, also fixed for 0.18.0, says lease recovery was implemented to synchronize the last block of a file and explicitly states that recovery is needed when replicas may have different generation-stamp values. HADOOP-1700 records append itself as a feature fixed for 0.19.0 and links those recovery/generation-stamp tasks.

Therefore this case does **not** claim that Hadoop 2.7.3 introduced generation stamps, append, or lease recovery.

**Primary anchors:**

- Apache JIRA HADOOP-3283, “Need a mechanism for data nodes to update generation stamps.”
- Apache JIRA HADOOP-3310, “Lease recovery for append.”
- Apache JIRA HADOOP-1700, “Append to files in HDFS.”

---

## Historical record

### H/P — HDFS exposes one logical file while block copies are distributed

The versioned Hadoop 2.7.3 HDFS Architecture document describes files as sequences of blocks stored on DataNodes, with replication controlled by the NameNode. It also says files have **strictly one writer at any time** in the bounded model and that the NameNode is the repository/arbitrator for HDFS metadata.

This matters for lease recovery because the failure problem is not simply “find any surviving copy.” The system must recover a single current continuation/closure for a file whose last block may have been in flight when the writer disappeared.

**Primary anchor:** Apache Hadoop 2.7.3, `HDFS Architecture`, sections `NameNode and DataNodes`, `Data Replication`, and `Simple Coherency Model`.

### H/P — the released 2.7.3 source states the lease-recovery algorithm explicitly

`LeaseManager.java` at the Hadoop 2.7.3 release commit contains an explicit `Lease Recovery Algorithm` comment. For each affected file, the NameNode considers the last block, finds the DataNodes containing it, chooses a primary DataNode, gives that primary a new generation stamp, and has it gather block information from the replicas. The primary then computes the **minimum block length** and updates DataNodes that have a valid generation stamp with the **new generation stamp and minimum block length**. After acknowledgement, the NameNode updates `BlockInfo`, removes the file from the lease, and commits the changes to the edit log.

This is direct implementation-level evidence that:

```text
surviving replica bytes
    -> replica generation/length evidence
    -> recovery-selected generation + common length
    -> updated replica state
    -> NameNode BlockInfo / lease transition
    -> edit-log commit
```

are distinct stages.

**Primary anchor:** Hadoop 2.7.3 release commit `baa91f7c6bc9cb92be5982de4719c1c8af91ccff`, `LeaseManager.java`.

### H/P — under-construction block state retains more than bytes

`BlockInfoContiguousUnderConstruction.java` in the same release says it represents a block currently being constructed, usually the last block of a file open for write or append. Its replica records retain the generation stamp, length, and replica state as reported by each DataNode.

The class comment also warns that an **expected location is not guaranteed to have a corresponding replica**. Assignment history and observed surviving embodiment are therefore distinct state.

The same class refuses to collapse under-construction state directly into complete state: completion requires the block state — including generation stamp and length — to have been committed and sufficient replicas to have reported.

**Primary anchor:** Hadoop 2.7.3 `BlockInfoContiguousUnderConstruction.java`.

### H/P — the recovery ID is also the new generation stamp

The 2.7.3 under-construction block object stores `blockRecoveryId`. Its source comment says this value is the **new generation stamp that the block will have after recovery succeeds** and is also used as a recovery ID “to identify the right recovery if any of the abandoned recoveries re-appear.”

`initializeBlockRecovery()` moves the block into `UNDER_RECOVERY`, records the recovery ID, and selects an alive recovery primary. This turns version/currentness metadata into a fencing relation among recovery attempts: an old recovery process can physically reappear without automatically regaining authority over the current block state.

**Primary anchor:** Hadoop 2.7.3 `BlockInfoContiguousUnderConstruction.java`.

### H/P — a wrong generation stamp can make a physically present replica stale

`setGenerationStampAndVerifyReplicas()` sets the final generation stamp and explicitly removes replicas whose reported generation stamp does not match, logging them as **stale replicas**.

This is a direct counterexample to:

```text
replica physically exists -> replica counts as current
```

The currentness relation is qualified by retained generation/version state.

**Primary anchor:** Hadoop 2.7.3 `BlockInfoContiguousUnderConstruction.java`.

### H/P — final recovery state is a metadata transition, not only DataNode mutation

The `LeaseManager` algorithm ends by updating NameNode `BlockInfo`, removing the file/lease relation, and committing the change to the edit log. The 2.7.3 Architecture document separately describes the EditLog as the persistent transaction log for file-system metadata changes.

The relevant distinction is not that “the edit log stores the file bytes” — it does not. Rather, replica synchronization and durable metadata authority are two different pieces of making the recovered file state survive the recovery event.

### H/P — Apache's own history shows why recovery authority must survive NameNode restart

HDFS-1149, “Lease reassignment is not persisted to edit log,” documented an earlier bug in which lease recovery reassigned a lease to a special NameNode holder but failed to persist that reassignment. After a NameNode restart, the **original leaseholder could again allocate blocks or complete a file even though recovery had already started**. The issue was fixed for 0.23.0.

This is unusually strong negative evidence: recovery authority can be logically correct in memory and still be unsafe if the fact of reassignment is not part of crash-recoverable metadata.

**Primary anchor:** Apache JIRA HDFS-1149.

---

## Retained state

The bounded mechanism contains at least six state classes.

### 1. User payload bytes

Block replica contents on DataNodes.

### 2. Block identity and generation stamp

A block ID alone does not describe the current recovery generation. The generation stamp distinguishes current from stale embodiments/attempts.

### 3. Replica length and replica state

During recovery the primary gathers per-replica block information. The bounded algorithm explicitly chooses a common minimum length before synchronizing replicas.

### 4. File lease / writer authority

The lease represents the active writer relation. Recovery is not merely byte copying; it is also transition away from an abandoned writer's authority.

### 5. Under-construction / recovery / committed control state

The NameNode represents whether the block is still being built, being recovered, or committed.

### 6. Recovery ID and persistent metadata transition

The new generation stamp/recovery ID identifies the currently valid recovery attempt; NameNode metadata and edit-log transitions make the recovered relation survive beyond the in-memory recovery exchange.

---

## Physical / logical substrate

```text
file pathname / inode relation
        |
        v
logical HDFS block ID
        |
        +---- generation stamp / UC state / length
        |
        +---- lease / writer authority
        |
        v
replica embodiments on DataNodes
        |
        v
lease/block recovery coordination
        |
        v
recovered BlockInfo + edit-log state
```

The payload is physically distributed, while currentness and writer/recovery authority are control relations coordinated by the NameNode and recovery protocol.

---

## Retention mechanism

### Normal write/append boundary

HDFS 2.7.3 allows one writer for the file. The last block may be under construction and replicated while the client is alive.

### Writer failure / lease-recovery boundary

When recovery is required, the bounded source describes:

```text
recover lease
    -> select last block
    -> select recovery primary
    -> allocate new generation/recovery stamp
    -> query replica state
    -> choose minimum common length
    -> update admissible replicas to new generation/length
    -> update NameNode BlockInfo
    -> remove lease relation
    -> commit metadata transition to EditLog
```

The file's persistence through writer failure therefore includes both **replica reconciliation** and **authority/currentness transition**.

---

## Read / write / erase semantics

### Read

Ordinary HDFS reads are not the central mechanism here. The important qualification is that a physically surviving replica can be excluded from current block state when its generation stamp is stale.

### Write / append

The bounded architecture provides a single writer. Append made recovery of a partially written final block materially important because a later writer must not simply continue from whichever surviving replica happens to be longest.

### Recovery rewrite / truncation

The 2.7.3 algorithm updates participating valid-generation replicas to the new generation stamp **and minimum block length**.

**Engineering reconstruction:** when replicas disagree in length after interruption, selecting the minimum length preserves only a prefix represented across the chosen valid replicas. Extra suffix bytes that physically survive on a longer replica are not automatically promoted to recovered file state.

This is intentional forgetting by convergence, not secure erasure.

---

## Maintenance and labor

Maintenance is distributed across several actors:

- the NameNode retains lease/block metadata and issues the recovery generation;
- one DataNode becomes recovery primary and gathers peer replica state;
- DataNodes update replica generation/length;
- the edit log retains the resulting metadata transition;
- client/NameNode lease management supplies the failure/recovery trigger.

Automation does not eliminate maintenance authority. It redistributes it into NameNode timers/state, recovery RPCs, DataNode coordination, and durable metadata bookkeeping.

---

## Failure and forgetting

### Failure mode 1 — writer disappears while the last block is under construction

Replica bytes may survive but disagree in length or generation.

### Failure mode 2 — stale replica survives

A replica can physically remain while a mismatching generation stamp makes it ineligible as current state.

### Failure mode 3 — abandoned recovery reappears

The recovery ID/new generation stamp exists partly to identify the right recovery when abandoned attempts reappear.

### Failure mode 4 — recovery authority is not crash-persistent

HDFS-1149 shows that a lease can be reassigned in memory while a NameNode restart revives the old writer's apparent authority if reassignment was not persisted.

### Failure mode 5 — common recovered state is shorter than a surviving embodiment

The bounded algorithm can choose a minimum length, deliberately declining to retain a longer unshared suffix as current file state.

### What is *not* established

This case does not claim:

- every HDFS recovery always loses the longest suffix;
- the minimum-length rule is the only HDFS pipeline-recovery rule across all releases;
- generation stamps are checksums;
- generation stamps are vector clocks, Raft terms, or consensus-log indexes;
- lease recovery restores the configured replication factor by itself;
- HDFS 2.7.3 invented append/lease recovery;
- physically discarded suffix bytes are securely erased from media.

---

## Historical record vs engineering reconstruction

### Historical record

Direct Apache sources establish:

- generation stamps were added in the append work by 2008;
- lease recovery exists to synchronize the final block when replicas may have different generation stamps;
- the 2.7.3 algorithm gathers replica state, computes minimum length, advances generation, updates replicas, then updates NameNode metadata and the edit log;
- under-construction replicas carry reported generation/length/state;
- a mismatched generation makes a replica stale;
- the recovery ID/new generation distinguishes the valid recovery if abandoned attempts return;
- an earlier missing edit-log record for lease reassignment could allow the original writer to regain effective authority after NameNode restart.

### Engineering reconstruction

From those mechanisms, this repository infers:

- **replica presence ≠ replica admissibility/currentness**;
- **replica multiplicity ≠ agreement**;
- **same block ID ≠ same current block state** when generation/length/state differ;
- **maximum surviving bytes ≠ recovered committed length**;
- **longer surviving replica ≠ automatically more authoritative replica**;
- **writer failure recovery can preserve a common prefix by refusing a disputed suffix**;
- **recovery authority itself is retained state and must survive the failure modes against which it is meant to arbitrate**.

These are project reconstructions, not quotations from Apache engineers.

---

## Functional comparisons

### HDFS generation stamp vs GFS chunk version — functional analogy only

Cases 26 and 46 show GFS using chunk-version/currentness metadata alongside checksum and master recovery relations. HDFS generation stamps likewise qualify whether a surviving block embodiment is current.

The shared function is **version-qualified admissibility of replicated data**. This does not establish historical borrowing, identical version semantics, or identical recovery algorithms.

### HDFS generation stamp vs Dynamo vector clock — functional analogy only

Case 23's vector clocks preserve causal ancestry and can retain concurrent branches. HDFS generation stamps in this bounded case are NameNode-assigned block generations/recovery IDs used to identify current versus stale recovery state.

Therefore:

```text
generation stamp != vector clock
```

### HDFS recovery ID vs Cassandra pending repair — functional analogy only

Case 48 retains a repair-session state so data selected for maintenance is not mistaken for successfully repaired data. HDFS retains a block recovery ID/new generation to distinguish the current recovery from abandoned attempts. Both make **maintenance transition identity** explicit, but they govern different objects and protocols.

### HDFS checksum vs generation stamp

The 2.7.3 Architecture document separately describes file checksums for corruption detection. A checksum answers an integrity question; a generation stamp answers a currentness/recovery-generation question. A replica can be byte-integral yet stale.

---

## Philosophical interpretation

**Interpretive claim, not historical vocabulary:** this case complicates any equation of persistence with “whatever bytes lasted longest.” After interruption, HDFS persistence can require an act of exclusion: surviving copies are compared, authority is advanced, and a disputed longer suffix can cease to count as the file even while some physical embodiment survived.

The retained object is therefore not the maximal sum of surviving traces. It is the state that remains **admissible under the recovery relation**.

That observation is useful for the repository's broader philosophy of technical retention, but it does **not** turn HDFS generation stamps into a theory of human memory, historical truth, or archival authority.

---

## Counterexamples and limits

1. A healthy closed HDFS block does not require lease recovery merely because it is replicated.
2. Physical replica count can be high while the last-block replicas disagree; multiplicity does not settle currentness.
3. A longer replica may contain bytes that are physically real yet not survive the recovery decision as current file state.
4. A valid generation stamp does not prove payload integrity; checksum/integrity is a separate relation.
5. An in-memory lease-recovery transition can be semantically correct yet fail across NameNode restart if the authority change is not persisted, as HDFS-1149 demonstrated historically.
6. The 2.7.3 source is a release-bounded implementation witness, not a complete history of later HDFS recovery semantics.

---

## Source anchors

### Primary / contemporary

- Apache Hadoop 2.7.3 release page: <https://hadoop.apache.org/docs/r2.7.3/>
- Apache Hadoop 2.7.3 HDFS Architecture: <https://hadoop.apache.org/docs/r2.7.3/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html>
- Hadoop 2.7.3 release commit (`baa91f7c6bc9cb92be5982de4719c1c8af91ccff`), `LeaseManager.java`: <https://github.com/apache/hadoop/blob/baa91f7c6bc9cb92be5982de4719c1c8af91ccff/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/LeaseManager.java>
- Same release commit, `BlockInfoContiguousUnderConstruction.java`: <https://github.com/apache/hadoop/blob/baa91f7c6bc9cb92be5982de4719c1c8af91ccff/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/BlockInfoContiguousUnderConstruction.java>
- Apache JIRA HADOOP-3283: <https://issues.apache.org/jira/browse/HADOOP-3283>
- Apache JIRA HADOOP-3310: <https://issues.apache.org/jira/browse/HADOOP-3310>
- Apache JIRA HADOOP-1700: <https://issues.apache.org/jira/browse/HADOOP-1700>
- Apache JIRA HDFS-1149: <https://issues.apache.org/jira/browse/HDFS-1149>

### Related repository check

`tmzncty/computing-archaeology` was searched for HDFS generation-stamp / lease-recovery / block-recovery coverage before this slice. No dedicated case was found, so this file keeps the treatment narrow and retention-specific rather than duplicating a general HDFS history.

---

## Provisional finding

> **A distributed copy can survive yet cease to count. In HDFS lease recovery, currentness is not exhausted by physical presence: generation, length, recovery identity, writer authority, and durable NameNode metadata jointly decide which surviving block state becomes the file after interruption.**
