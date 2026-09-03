# Case 50 grounding — HDFS QJM epoch fencing, persisted promises, and HA write authority

## Promotion target

Ground [`cases/50-apache-hdfs-qjm-epoch-fencing.md`](../cases/50-apache-hdfs-qjm-epoch-fencing.md) as a bounded distributed-retention case without turning HDFS high availability or consensus protocols into one generic history.

**Result:** `grounded`.

The central relation is directly supported by Apache primary sources:

> after a new HDFS QJM writer establishes a higher epoch on a JournalNode quorum, the accepting JournalNodes persist a promise not to accept lower writer epochs; an older NameNode can therefore remain alive without retaining successful shared-edit-log mutation authority.

---

## Bounded evidence set

### A. Apache JIRA HDFS-3077 and `qjournal-design.pdf` — quorum journal design

- **Issue:** `Quorum-based protocol for reading and writing edit logs`.
- **Opened:** March 2012.
- **Fix version:** Hadoop 2.0.3-alpha.
- **Primary attachment:** `qjournal-design.pdf`.
- **Direct design evidence:** a batch of edits is successful after acknowledgement from a quorum rather than all JournalNodes; a slow/dead minority can be excluded while a quorum remains.
- **Direct design evidence:** before mutating the edit log a writer must establish an `epoch`; it sends `newEpoch(N)` and may proceed only after quorum acceptance.
- **Direct design evidence:** a JournalNode accepting the new epoch persists and fsyncs `lastPromisedEpoch`; later mutation RPCs carry their epoch and lower epochs are rejected.
- **Direct design evidence:** quorum overlap is the correctness argument preventing a lower-epoch former writer from later obtaining a successful mutation quorum after a higher epoch has been established.
- **Prior-art boundary:** the design explicitly relates the approach to Paxos/ZAB and says its epoch-generation method borrows from those systems. This blocks an HDFS-invention claim for epoch/quorum fencing.
- **Issue URL:** <https://issues.apache.org/jira/browse/HDFS-3077>
- **Design attachment:** <https://issues.apache.org/jira/secure/attachment/12532989/qjournal-design.pdf>

### B. Hadoop 2.7.3 HA with QJM guide — deployed architecture and fencing boundary

- **Document:** `HDFS High Availability Using the Quorum Journal Manager`.
- **Version:** Hadoop 2.7.3.
- **Direct source evidence:** an HA nameservice has redundant NameNodes with only one intended Active at a time.
- **Direct source evidence:** every namespace modification by the Active is durably logged to a majority of JournalNodes; the Standby tails those edits and catches up before promotion.
- **Direct source evidence:** JournalNodes allow only one NameNode writer at a time, preventing two Active NameNodes from corrupting shared metadata through simultaneous QJM writes.
- **Important negative boundary:** QJM journal fencing does not physically terminate the old Active and does not necessarily stop stale reads immediately; the guide still recommends process/external fencing methods where appropriate.
- **Automatic-failover boundary:** ZooKeeper and ZKFC supply a separate election/liveness/failover layer.
- **URL:** <https://hadoop.apache.org/docs/r2.7.3/hadoop-project-dist/hadoop-hdfs/HDFSHighAvailabilityWithQJM.html>

### C. Hadoop 2.7.3 `Journal.java` — persistent acceptor-side fencing state

- **Path:** `hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/qjournal/server/Journal.java`.
- **Version:** `rel/release-2.7.3`.
- **Direct source evidence:** source comment says a new writer asks the JournalNode to ignore requests from previous writers, identified by epoch, and that this epoch is stored persistently on disk to make the promise.
- **Direct source evidence:** `lastPromisedEpoch` and `lastWriterEpoch` are represented by `PersistentLongFile` backed by `last-promised-epoch` and `last-writer-epoch` files.
- **Direct source evidence:** `newEpoch()` rejects an epoch less than or equal to the existing promise, then calls `updateLastPromisedEpoch()` and aborts the current segment.
- **Direct source evidence:** `checkRequest()` rejects a request below `lastPromisedEpoch`; a higher epoch advances the promise and fences earlier writers.
- **Direct source evidence:** the same method maintains a monotonically increasing per-epoch IPC serial guard against reordering/stale retries, while `checkWriteRequest()` separately requires the request epoch to equal `lastWriterEpoch`.
- **Use here:** grounds the distinction `lastPromisedEpoch != lastWriterEpoch != currentEpochIpcSerial` and demonstrates that writer-authority fencing is intended to survive JournalNode restart.
- **URL:** <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/qjournal/server/Journal.java>

### D. Hadoop 2.7.3 `QuorumJournalManager.java` — epoch establishment through quorum-observed history

- **Path:** `hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/qjournal/client/QuorumJournalManager.java`.
- **Version:** `rel/release-2.7.3`.
- **Direct source evidence:** `createNewUniqueEpoch()` is explicitly documented to `Fence any previous writers, and obtain a unique epoch number for write-access to the journal nodes.`
- **Direct source evidence:** it gathers JournalNode state from a write quorum, selects the maximum observed `lastPromisedEpoch`, proposes `max + 1`, waits for `newEpoch()` quorum acceptance, and only then sets that epoch on the logger set.
- **Use here:** independently grounds the design-document algorithm in release source.
- **URL:** <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/qjournal/client/QuorumJournalManager.java>

### E. Apache JIRA HDFS-2185 — ZooKeeper/ZKFC as a separate failover state machine

- **Issue:** ZooKeeper-based automatic failover controller work.
- **Opened:** 22 July 2011.
- **Resolved:** 3 April 2012.
- **Direct problem/function evidence:** leader election, health monitoring/failure detection, failover, and liveness/heartbeat duties belong to the ZK-based failover-controller layer.
- **Use here:** prevents silently collapsing `who wins automatic failover` into `which QJM writer epoch JournalNodes admit`.
- **URL:** <https://issues.apache.org/jira/browse/HDFS-2185>

### F. Apache JIRA HDFS-1972 — DataNode fencing as an out-of-scope neighboring problem

- **Issue:** DataNode-side fencing work for HA split-brain safety.
- **Use here:** records an important scope boundary: QJM's retained writer promise governs shared edit-log mutation, not every command path in the HDFS system.
- **Decision:** do not fold DataNode command fencing into Case 50; leave it as a later bounded case or evidence deepening.
- **URL:** <https://issues.apache.org/jira/browse/HDFS-1972>

---

## Source cross-check

The design document and release source agree on the core fencing chain:

```text
query JournalNode promises from a quorum
        |
        v
choose epoch > observed promises
        |
        v
newEpoch accepted by quorum
        |
        +---- accepted JNs persist lastPromisedEpoch
        |
        v
later mutation RPC carries writer epoch
        |
        +---- lower epoch rejected
        |
        v
edit batch may commit after quorum acknowledgement
```

The 2.7.3 operational guide adds a boundary not obvious from the protocol pseudocode alone: loss of JournalNode write authority does **not** imply immediate disappearance of the former Active process or elimination of every stale read.

---

## Claim ledger

| Claim | Label | Evidence | Strength / boundary |
| --- | --- | --- | --- |
| HDFS HA intends one Active NameNode for mutation service | `H/P` | 2.7.3 HA/QJM guide | strong release-matched system documentation |
| namespace edits are durably logged to a JournalNode majority | `H/P` | 2.7.3 guide; HDFS-3077 design | strong |
| QJM writer epochs were designed to fence previous edit-log writers | `H/P` | HDFS-3077 design §§2.3–2.4 | strong historical design statement |
| accepting a new epoch durably stores/fsyncs `lastPromisedEpoch` | `H/P` | HDFS-3077 design; 2.7.3 `Journal.java` | strong design + implementation evidence |
| JournalNode rejects lower-epoch mutation requests | `H/P` | design; `Journal.checkRequest()` | strong |
| a new writer derives a higher epoch from quorum-observed prior promises and requires quorum acceptance | `H/P` | design; `QuorumJournalManager.createNewUniqueEpoch()` | strong |
| after successful higher-epoch quorum fencing, an older lower-epoch writer cannot again commit a quorum mutation because future quorums overlap | `H/P/E` | HDFS-3077 correctness argument | strong, bounded to the documented quorum protocol |
| process survival does not imply continuing shared-log mutation authority | `E` | QJM epoch fencing | strong reconstruction |
| a minority JN can lag without making its state committed/current | `H/E` | quorum acknowledgement semantics | strong, while quorum assumptions remain satisfied |
| journal-write fencing does not equal process termination or stale-read elimination | `H/P` | 2.7.3 HA/QJM guide | strong negative source boundary |
| ZooKeeper election and QJM writer fencing are separate retained relations | `H/P/E` | HDFS-2185; 2.7.3 guide; QJM design | strong |
| `lastPromisedEpoch` is non-payload retention infrastructure | `E` | persistent promise + mutation gating | strong project reconstruction |
| `lastPromisedEpoch`, `lastWriterEpoch`, and current-epoch IPC serial are one field/one semantic | `X` | 2.7.3 `Journal.java` separates them | rejected |
| QJM invented epoch/quorum fencing | `X` | HDFS-3077 explicitly cites Paxos/ZAB | rejected |
| higher epoch physically kills the old NameNode | `X` | 2.7.3 guide retains separate process-fencing concern | rejected |
| every JournalNode must acknowledge every successful edit | `X` | quorum-write design | rejected |

---

## Counterexample value

### `old process still alive = old process still authoritative`

Rejected. QJM deliberately lets authority be revoked by a higher persisted epoch even if the earlier process, memory, and network reachability survive.

### `fencing = killing a process`

Rejected. QJM performs protocol-level write fencing; Apache still discusses process/external fencing separately and explicitly warns about stale reads from an old Active.

### `quorum durability = immediate all-replica agreement`

Rejected. Success is majority-based. The protection comes from quorum intersection plus persisted promises, not an all-JournalNode synchronous-copy requirement.

### `leader election = write fencing`

Rejected. ZooKeeper/ZKFC decides/coordinates failover while JournalNode epochs gate shared-edit-log writer admission.

### `one monotonic number = one generic consensus term`

Rejected. Release source itself separates promise floor, writer epoch, and per-epoch IPC serial; Case 49 separately uses a block generation stamp. Functional similarity does not license synonymy.

---

## Cross-case controls

### Case 49 / HDFS generation-stamp lease recovery

Functional bridge: both retain monotonically ordered control state so stale participants/embodiments can continue existing without continuing to count.

Boundary: Case 49 qualifies **block replica/recovery currentness**; Case 50 qualifies **NameNode shared-edit-log mutation authority**. `block generation stamp != QJM writer epoch`.

### Case 48 / Cassandra pending repair

Functional bridge: a retained maintenance/protocol transition state constrains future eligibility.

Boundary: Cassandra classifies SSTables and repair sessions; QJM classifies writer epochs at JournalNode mutation admission.

### Cases 28 and 41 / tombstones

Functional bridge: a small retained negative state can prevent an older positive state from becoming current again.

Boundary: tombstones reject **data versions**; `lastPromisedEpoch` rejects **writer epochs/actors**. The negative constraint is comparable, not historically identical.

### Case 46 / GFS master log/checkpoint recovery

Functional bridge: namespace continuity depends on metadata/recovery relations beyond user payload.

Boundary: GFS Case 46 reconstructs master metadata after restart; QJM Case 50 preserves one-writer edit authority across HA failover.

---

## `computing-archaeology` reuse check

Searched `tmzncty/computing-archaeology` for HDFS, QJM, JournalNode, epoch fencing, generation stamps, and lease recovery before writing. No dedicated HDFS/QJM case was found.

Therefore this slice does not duplicate an existing companion-repository history. A future broader HDFS engineering genealogy should live there and be linked here rather than copied.

---

## Maturity decision

**Promote to `grounded`.**

Why:

- Apache's 2012 design states the correctness problem, quorum semantics, persisted promise, epoch-generation algorithm, and prior-art boundary directly;
- Hadoop 2.7.3 release documentation supplies deployed HA/QJM semantics and an unusually useful explicit stale-read/process-fencing limit;
- release-tag source independently implements persistent `lastPromisedEpoch`, lower-epoch rejection, separate writer/IPC state, and quorum epoch establishment;
- ZooKeeper/ZKFC election is source-separated from QJM shared-log fencing;
- counterexamples and non-claims are explicit;
- companion-repository duplication was checked.

Remaining work is deliberately separate: DataNode command fencing, post-2.7 QJM/HA evolution, Observer/read-freshness semantics, independent split-brain fault injection, and broader Paxos/ZAB/consensus-log genealogy.
