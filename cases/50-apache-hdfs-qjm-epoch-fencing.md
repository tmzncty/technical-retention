# Apache HDFS QJM Epoch Fencing: Persisted Writer Promises, Quorum Overlap, and Split-Brain Containment

## Scope

- **Bounded system:** Apache Hadoop HDFS Quorum Journal Manager (QJM), designed in 2012 and examined through the released Hadoop **2.7.3** documentation and `rel/release-2.7.3` source state.
- **Bounded mechanism:** two HA NameNodes sharing namespace edit history through a quorum of JournalNodes; QJM writer epochs; JournalNode `lastPromisedEpoch` / `lastWriterEpoch`; quorum acknowledgement; stale-writer rejection; and the remaining distinction between journal fencing and whole-process/client-read fencing.
- **Primary source base:** HDFS-3077 and its `qjournal-design.pdf`; Apache Hadoop 2.7.3 `HDFSHighAvailabilityWithQJM`; release-source `QuorumJournalManager.java` and `Journal.java`; HDFS-2185 for the separate ZooKeeper failover-controller/election layer.
- **Research question:** after failover, what retained control state makes the newly active NameNode's edit-log authority survive the continued physical existence, execution, or delayed network traffic of an older NameNode that may still believe itself active?

This is **not** a general HDFS HA history. Case 49 already covers last-block lease recovery and block generation stamps. Case 46 covers GFS master log/checkpoint recovery. This case isolates the shared-edit-log **writer-authority fencing relation** in HDFS QJM.

The bounded retention claim is:

> **HDFS QJM does not rely on an old writer disappearing in order for a new writer to become authoritative. A would-be writer first obtains a higher epoch from a quorum; each accepting JournalNode durably retains a promise not to accept lower epochs; later edit-log mutation RPCs carry the writer epoch and are rejected when stale. Because write quorums overlap, an older writer may remain alive and may even reach some JournalNodes, yet it cannot again obtain a quorum capable of committing namespace edits. The retained promise is therefore not payload, but it is constitutive retention infrastructure for preserving which future mutations may count.**

`authority retention`, `write-admissibility state`, and `split-brain containment` below are project terms. Historical Apache vocabulary includes `epoch`, `lastPromisedEpoch`, `lastWriterEpoch`, `newEpoch`, `JournalNode`, `QuorumJournalManager`, `Active`, `Standby`, `fencing`, `split-brain`, and `failover`.

---

## Historical vocabulary and prior-art boundary

### Direct Apache vocabulary

The bounded sources use:

- `QuorumJournalManager` / `QJM`;
- `JournalNode` / `JN`;
- `epoch number`;
- `newEpoch`;
- `lastPromisedEpoch`;
- `lastWriterEpoch`;
- `writer`;
- `fencing` / `fence any previous writers`;
- `Active` / `Standby` NameNode;
- `split-brain scenario`;
- `quorum` / majority;
- `edit log` and `logSync`;
- `ZKFailoverController` / `ZKFC` and ZooKeeper election in the automatic-failover layer.

### Origin and prior-art boundary

HDFS-3077 was opened in **March 2012** to implement a quorum-based shared edit-log alternative for HDFS HA and was fixed for **2.0.3-alpha**. Its design document explicitly says the epoch solution is similar to distributed-systems literature such as **Paxos** and **ZAB**, and says the epoch-generation algorithm borrows from those systems.

Therefore this case does **not** claim that HDFS or QJM invented:

- epochs / ballot-like writer ordering;
- quorum intersection;
- consensus recovery;
- fencing as a distributed-systems concept;
- leader election;
- replicated logs in general.

The historically defensible claim is narrower: HDFS QJM instantiated these ideas in a specific shared-edit-log protocol and retained a durable `lastPromisedEpoch` on JournalNodes to fence prior NameNode writers.

**Primary anchors:**

- Apache HDFS-3077, `Quorum-based protocol for reading and writing edit logs`;
- attached 2012 `qjournal-design.pdf`, especially §§1.3, 2.2–2.4, and 2.8;
- Hadoop 2.7.3 QJM implementation source.

---

## Historical record

### H/P — HDFS HA requires one mutation authority even when two NameNodes exist

The Hadoop 2.7.3 HA/QJM guide says an HA cluster has two NameNodes but, at any point, exactly one should be Active. The Active handles client operations; the Standby follows namespace edits. It also states the correctness danger directly: if both NameNodes act as Active, namespace state can diverge and risk data loss or incorrect results.

This establishes the historical problem in Apache's own vocabulary: physical redundancy of master processes creates an **authority problem** rather than solving it by itself.

**Primary anchor:** <https://hadoop.apache.org/docs/r2.7.3/hadoop-project-dist/hadoop-hdfs/HDFSHighAvailabilityWithQJM.html>

### H/P — namespace mutation durability is quorum-based, not all-node completion

The same 2.7.3 guide states that every namespace modification by the Active is durably logged to a **majority** of JournalNodes. The Standby tails those edits and, before promotion during failover, ensures it has read the edits from the JournalNodes.

The HDFS-3077 design likewise specifies that a batch of edits is considered successfully written after successful response from a quorum. A slow or failed JournalNode may be excluded from the current segment while the system continues as long as a quorum remains.

Therefore:

```text
commit/durable-log success
    != every JournalNode has acknowledged the edit
```

and a minority can lag without automatically becoming the current authority for future writes.

### H/P — the design introduces writer epochs specifically as software fencing state

Section 2.3 of the HDFS-3077 design states the requirement: after a new writer takes over, a previously active writer must be unable to commit further edits. The design introduces epoch numbers with three explicit properties:

1. a writer receives an epoch when it becomes active;
2. epochs are unique among successful writers;
3. epochs totally order writers, so a higher epoch is later.

Before mutating edit logs, a QJM must establish an epoch. It sends `newEpoch(N)` and may proceed only after a quorum of JournalNodes accepts it.

**Primary anchor:** HDFS-3077 `qjournal-design.pdf`, §§2.3–2.4.

### H/P — each accepting JournalNode durably retains the promise

The design says that when a JournalNode accepts `newEpoch(N)`, it persistently records the value as `lastPromisedEpoch` and fsyncs it to local storage. Mutation RPCs carry the requester's epoch. Before acting, a JournalNode compares that epoch against its retained promise and rejects a lower one.

The Hadoop 2.7.3 source preserves the same relation. `Journal.java` declares `last-promised-epoch` as a `PersistentLongFile`; its source comment says a new writer asks the node to ignore requests from previous writers and that the epoch is stored persistently on disk to make that promise. `newEpoch()` rejects an epoch less than or equal to the existing promise, then calls `updateLastPromisedEpoch()`.

This is direct implementation evidence that the fencing relation is intended to survive JournalNode restart rather than exist only in RAM.

**Primary source:** <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/qjournal/server/Journal.java>

### H/P — a new writer derives a higher epoch from quorum-observed prior promises

`QuorumJournalManager.createNewUniqueEpoch()` in Hadoop 2.7.3:

1. requests JournalNode state and waits for a write quorum;
2. finds the maximum `lastPromisedEpoch` in the replies;
3. proposes `maxPromised + 1`;
4. sends `newEpoch()` and again waits for a write quorum;
5. only then installs the epoch in the logger set.

The 2012 design describes the same algorithm and explains why overlapping quorums prevent two proposers from both successfully establishing the same epoch.

**Primary source:** <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/qjournal/client/QuorumJournalManager.java>

### H/P — stale RPC rejection is checked at the JournalNode

Hadoop 2.7.3 `Journal.checkRequest()` rejects an RPC whose epoch is below `lastPromisedEpoch`. If a request arrives with a higher epoch, the JournalNode advances its promise and thereby fences previous writers. The same function additionally checks a monotonically increasing per-epoch IPC serial number so that reordered or stale retry RPCs from the current epoch do not silently become ordinary new mutations.

`checkWriteRequest()` separately requires the request epoch to equal `lastWriterEpoch` for write operations.

The source therefore distinguishes at least three pieces of control state:

```text
lastPromisedEpoch
    -> lower-bound promise about which writer epochs may still be admitted

lastWriterEpoch
    -> epoch of the writer actually associated with current journal writing

currentEpochIpcSerial
    -> in-memory ordering/retry guard inside the current epoch
```

These should not be collapsed into one generic `leader term` without source-specific qualification.

### H/P — quorum overlap, not total erasure of the old writer, enforces the write boundary

The HDFS-3077 design gives the key argument: after a quorum has accepted `newEpoch(N)`, any future quorum necessarily overlaps that quorum at one or more JournalNodes. Because the overlapping node remembers the higher promise and rejects the earlier writer, a lower-epoch writer cannot again mutate the edit log on a quorum.

The historical claim is therefore **not** “the old NameNode is physically unable to send packets.” It is that its requests cease to satisfy the protocol's write-admissibility condition.

### H/P — QJM journal fencing does not make all stale service impossible

The 2.7.3 HA/QJM guide explicitly preserves another boundary. With QJM, only one NameNode is allowed to write to the JournalNodes, so shared metadata cannot be corrupted by two simultaneous edit-log writers. But the old Active can still temporarily answer **read requests** with stale information until it shuts itself down after failing a write. Apache therefore still recommends configuring external/process fencing methods even with QJM.

This is unusually useful negative evidence:

```text
journal-write fencing
    != process termination
    != stale-read elimination
```

The guide's `dfs.ha.fencing.methods`, `sshfence`, and `shell` mechanisms address a different failure surface from the QJM epoch promise.

### H/P — ZooKeeper election is another distinct authority relation

For automatic failover, the 2.7.3 guide describes a ZooKeeper-backed ZKFailoverController. ZooKeeper session expiration supplies failure detection and an ephemeral lock znode supplies active election; the winning ZKFC then runs failover, including fencing the previous active if necessary.

HDFS-2185, opened in July 2011 and resolved in April 2012, separately describes the ZK-based failover controller as performing leader election, health monitoring, failover, and heartbeat/liveness work.

Therefore:

```text
ZooKeeper election state
    != QJM journal-writer epoch state
```

They can compose in one HA deployment without becoming the same retained state or the same historical mechanism.

---

## Retained state

The bounded mechanism contains at least seven relevant state classes.

### 1. Namespace edit records

The actual logical mutation history replicated on JournalNodes.

### 2. JournalNode `lastPromisedEpoch`

Persistent fencing state: the JournalNode's retained promise not to admit older writers.

### 3. `lastWriterEpoch`

Persistent evidence about which epoch actually wrote the current journal state; the implementation uses it separately from the promise floor.

### 4. Current-epoch IPC serial

An in-memory monotonic guard against RPC reordering/stale retries within one epoch. It is reset when the epoch changes.

### 5. Quorum membership/reachability at the moment of acknowledgement

A mutation or epoch establishment succeeds on a majority, not because every physical JournalNode has identical immediate state.

### 6. NameNode HA state

`Active` or `Standby` role as managed by administrative or automatic failover machinery.

### 7. Optional ZooKeeper election/process-fencing state

Automatic failover and process-level fencing add further authority/liveness state outside the JournalNode epoch mechanism.

---

## Retention mechanism

The bounded write-authority sequence is:

```text
candidate NameNode / QJM
        |
        v
read lastPromisedEpoch from a quorum
        |
        v
propose max + 1
        |
        v
newEpoch(N) accepted by a quorum
        |
        +---- each accepting JN durably stores lastPromisedEpoch=N
        |
        v
writer may begin/recover journal work in epoch N
        |
        v
future mutation RPC carries epoch N
        |
        +---- lower epoch -> reject
        +---- acceptable epoch -> continue protocol checks
        |
        v
edit batch acknowledged by quorum
```

The crucial persistence step is not a user-data write. It is retention of a **future refusal condition**: once the higher promise survives, lower writer epochs remain excluded from successful future quorum mutation.

---

## Read / write / erase semantics

### Read

The QJM fencing contract is primarily about **mutation authority**. Apache explicitly warns that an old Active may still answer stale client reads even after it has lost JournalNode write authority.

Thus a read can remain technically executable while the serving process is no longer the desired current authority.

### Write

Namespace mutations are durably logged to a majority of JournalNodes. A requester's epoch is part of mutation admissibility; payload/edit bytes alone are insufficient.

### Erase / forgetting

The mechanism does not securely erase the old NameNode or erase its local memory. Instead, a successful higher epoch makes the lower epoch **protocol-inadmissible for quorum mutation**.

This is a form of technical forgetting at the authority layer:

```text
old writer may still exist
old writer's local state may still exist
old packets may still arrive
        but
old writer authority no longer counts for future quorum writes
```

The old process can later be terminated or fenced separately.

---

## Maintenance and labor

Retention of one coherent mutation authority requires continuing infrastructure:

- JournalNodes persist edit records and epoch promises;
- NameNodes/QJM obtain quorum responses and roll/recover logs;
- Standby NameNode tails shared edits;
- failover tooling or ZKFC detects role transition;
- ZooKeeper, when automatic failover is used, maintains election/session state;
- operators configure JournalNode topology and, where desired, process fencing methods such as `sshfence` or site-specific scripts.

Automatic HA therefore does not remove retention labor. It redistributes it across durable promises, quorum availability, failure detection, election, process control, and operational configuration.

---

## Failure and forgetting

### Failure mode 1 — old Active remains alive after failover

QJM does not require physical disappearance. A higher epoch retained by a quorum prevents the older writer from obtaining a future quorum of successful edit mutations.

### Failure mode 2 — one JournalNode missed the epoch transition

Because epoch establishment and edits are quorum-based, one JN can lag or be unavailable. The guarantee is not “every node remembers immediately”; it depends on quorum intersection for future successful writes.

### Failure mode 3 — stale/reordered RPC resurfaces

Within an epoch, the implementation checks monotonically increasing IPC serials in addition to epoch state.

### Failure mode 4 — QJM fences writes but old Active serves stale reads

Apache documents this explicitly. External/process fencing still has value even when metadata corruption through dual QJM writers is prevented.

### Failure mode 5 — failover election is unavailable

If automatic failover uses ZooKeeper and ZooKeeper is unavailable, the 2.7.3 guide says automatic failovers are not triggered even though HDFS can continue operating with the currently active node. Election availability and namespace retention are therefore distinct service relations.

### What is *not* established

This case does not claim:

- QJM epochs are a new invention rather than a Hadoop use of earlier quorum/epoch ideas;
- a higher epoch physically stops or powers off an older NameNode;
- QJM write fencing prevents every stale read;
- every JournalNode must store every successful edit before client-visible success;
- `lastPromisedEpoch`, `lastWriterEpoch`, block generation stamps, ZooKeeper zxids, Paxos ballots, and Raft terms are synonyms;
- ZooKeeper election alone replaces QJM writer fencing;
- QJM alone guarantees all DataNode-side command fencing or all client-side failover semantics;
- a minority JournalNode that accepts stale traffic can make that traffic committed/current.

---

## Historical record vs engineering reconstruction

### Historical record

Apache primary sources establish:

- HDFS HA runs redundant NameNodes with an intended single Active;
- QJM replicates edits to a JournalNode quorum;
- HDFS-3077's design uses epochs to fence prior writers;
- an accepting JN fsyncs `lastPromisedEpoch`;
- later lower-epoch mutation RPCs are rejected;
- a new QJM derives a higher epoch from quorum-observed promises and only proceeds after quorum acceptance;
- Hadoop 2.7.3 source implements persistent `lastPromisedEpoch`, lower-epoch rejection, and separate `lastWriterEpoch`/IPC-serial checks;
- QJM write fencing does not by itself eliminate stale reads from the old Active;
- automatic failover has a separate ZooKeeper/ZKFC election/liveness layer.

### Engineering reconstruction

From those mechanisms, this repository infers:

- **process survival ≠ retained mutation authority**;
- **being locally `Active` or believing oneself active ≠ quorum-authorized shared-log mutation**;
- **authority can be preserved as a durable refusal relation on future operations**;
- **quorum acknowledgement ≠ all replicas immediately agree**;
- **minority acceptance/existence ≠ committed namespace history**;
- **writer-authority retention depends on control metadata whose purpose is to constrain future edits rather than reproduce past payload**.

These are project reconstructions, not Apache quotations.

---

## Functional comparisons

### QJM epoch vs HDFS block generation stamp — functional analogy only

Case 49 uses a block generation/recovery stamp to qualify which surviving block replicas and recovery attempts count as current. Case 50 uses a QJM writer epoch to qualify which NameNode writer may mutate the shared edit log.

Both order authority/currentness, but their objects and protocols differ:

```text
block generation stamp != QJM writer epoch
```

No shared genealogy is inferred merely from the word `generation` or from monotonic ordering.

### QJM epoch vs Cassandra pending repair — functional analogy only

Case 48 retains maintenance-session state so in-progress repair is not mistaken for completed repair. QJM retains writer promises so an older writer cannot regain successful mutation authority. Both show control history constraining future admissibility, but they govern different actions and consistency problems.

### QJM `lastPromisedEpoch` vs tombstones — functional analogy only

Cases 28 and 41 retain negative currentness to stop deleted payload from reappearing. QJM retains a promise to stop an earlier **actor/epoch** from making future shared-log mutations. Both are retained negative constraints, but one rejects data versions and the other rejects writer authority.

### QJM epoch vs Paxos/ZAB

This is not merely a modern analogy: the **HDFS-3077 design itself** explicitly cites Paxos and ZAB as precedent and says its epoch generation borrows from them. The safe historical statement is therefore that Apache engineers consciously placed the QJM design in that prior-art family.

That still does not make every QJM field semantically identical to every ballot/epoch/zxid field in those systems.

---

## Philosophical interpretation

**Interpretive claim, not Apache vocabulary:** this case is a strong counterexample to treating persistence as the endurance of a thing alone. The old writer can endure materially — process, memory, sockets, local beliefs — while one constitutive relation is deliberately made not to endure: its authority to define the next shared namespace state.

At the same time, that forgetting of authority requires another state to persist: the higher `lastPromisedEpoch` promise.

A bounded philosophical formulation is therefore:

> **Some technical systems preserve continuity by retaining not only what may be repeated, but also a durable rule about what must no longer be accepted.**

The interpretation stops at the protocol boundary. It does not turn QJM into a theory of political sovereignty, human memory, or archival exclusion, and it does not equate a JournalNode integer with Stieglerian tertiary retention.

---

## Claim ledger

| Claim | Label | Evidence | Strength / boundary |
| --- | --- | --- | --- |
| HDFS HA intends exactly one Active NameNode for client mutation service | `H/P` | Hadoop 2.7.3 HA/QJM guide | strong release-matched system documentation |
| namespace edits are durably logged to a majority of JournalNodes | `H/P` | 2.7.3 guide; HDFS-3077 design | strong |
| QJM epochs were designed to fence previous edit-log writers | `H/P` | HDFS-3077 §§2.3–2.4 | strong historical design statement |
| accepting a new epoch durably records `lastPromisedEpoch` | `H/P` | HDFS-3077; 2.7.3 `Journal.java` | strong design + implementation evidence |
| a lower-epoch mutation request is rejected by the JournalNode | `H/P` | design + `Journal.checkRequest()` | strong |
| a new writer uses quorum-observed max promise + 1 and quorum acceptance | `H/P` | design + `QuorumJournalManager.createNewUniqueEpoch()` | strong |
| quorum overlap means the old lower-epoch writer cannot later commit edits on a quorum after successful fencing | `H/P/E` | design's own argument + implementation | strong bounded protocol relation; not generalized to arbitrary quorum systems |
| process survival does not imply continuing write authority | `E` | QJM fencing semantics | strong reconstruction |
| journal-write fencing does not eliminate stale reads from the old Active | `H/P` | Hadoop 2.7.3 HA/QJM guide | strong negative boundary |
| ZooKeeper election and QJM journal fencing are separate mechanisms | `H/P/E` | 2.7.3 automatic-failover guide; HDFS-2185; QJM design | strong |
| `lastPromisedEpoch` is retention infrastructure but not namespace payload | `E` | persistent promise + mutation gating | strong project reconstruction |
| QJM invented epoch/quorum fencing | `X` | design explicitly cites Paxos/ZAB | rejected |
| higher epoch physically terminates the old NameNode | `X` | 2.7.3 guide explicitly retains separate fencing concern | rejected |
| all JNs must acknowledge for a successful edit | `X` | quorum write design | rejected |

---

## `computing-archaeology` reuse check

Searched `tmzncty/computing-archaeology` for HDFS, QJM, JournalNode, epoch fencing, and lease-recovery-related coverage before writing. No dedicated HDFS/QJM case was found.

Therefore this slice keeps its HDFS-specific retention/currentness analysis here rather than duplicating an existing companion-repository technical history. If `computing-archaeology` later develops a broader HDFS/QJM engineering genealogy, this case should link to it and retain only the authority-retention comparison.

---

## Maturity decision

**Promote to `grounded`.**

Why:

- the 2012 Apache design document states the historical correctness requirements and fencing algorithm explicitly;
- the design acknowledges Paxos/ZAB prior art, preventing a false novelty claim;
- the Hadoop 2.7.3 release guide documents the deployed HA/QJM architecture and its stale-read/process-fencing boundary;
- exact 2.7.3 release source independently exposes persistent promise files, epoch checks, and quorum epoch establishment;
- automatic failover/election is source-separated from shared-log writer fencing;
- the case yields several cross-case counterexamples without requiring speculative implementation inference;
- related-repository duplication was checked.

Remaining work is intentionally separate: DataNode command fencing lineage, later Observer/HA read semantics, post-2.7 QJM changes, independent split-brain/fault-injection experiments, and broader consensus-log genealogy should not be silently folded into this bounded case.
