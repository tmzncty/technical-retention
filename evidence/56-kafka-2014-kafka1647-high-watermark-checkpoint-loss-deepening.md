# Deepening Record — Kafka 2014 KAFKA-1647 High-Watermark Checkpoint Loss

## Target case

[`cases/56-apache-kafka-replicated-log-high-watermark.md`](../cases/56-apache-kafka-replicated-log-high-watermark.md)

## Status

**`bounded deepening complete`**

This record deepens one narrow question left implicit by the original Kafka 0.8.2 grounding:

> If `replication-offset-checkpoint` is the retained high-watermark recovery boundary, what happens when the broker accidentally omits a partition from the in-memory replica set used to rewrite that checkpoint?

The answer is unusually well documented because Apache fixed exactly such a bug as **KAFKA-1647** in 2014. The bug report describes a production-observed hard-kill/restart scenario; the pre-fix source shows why a local log could exist without a local `Replica` object; the fix explicitly creates that object so the partition's high watermark remains present when the checkpoint file is rewritten; and the final `0.8.2.0` tag contains the repair.

This is not a general Kafka crash-consistency study. It does not establish filesystem-level atomicity of the checkpoint file, exact behavior under every power-loss point, ZooKeeper durability, or modern Kafka semantics.

---

## Why this slice matters

The base case already established:

```text
payload log bytes
    != high watermark
    != checkpointed high-watermark recovery state
```

KAFKA-1647 adds a stronger and more concrete retention boundary:

```text
old checkpoint entry exists on disk
    != partition is represented in the next checkpoint rewrite

partition log still exists
    != local Replica object exists
    != its high watermark will be emitted into the next checkpoint map
```

The issue therefore gives a direct historical counterexample to treating recovery metadata as a passive derivative that can always be reconstructed from surviving payload bytes without consequence.

---

## Historical record

### H/P — the 0.8.2 checkpoint writer rewrites a complete per-directory map

In the exact `0.8.2.0` source, `ReplicaManager.checkpointHighWatermarks()`:

1. enumerates local `Replica` objects from `allPartitions`;
2. keeps replicas that have local logs;
3. groups them by log directory;
4. builds a fresh `TopicAndPartition -> highWatermark` map for each directory;
5. passes that map to the directory's `OffsetCheckpoint.write()`.

The writer is therefore not an append-only journal of changed partitions. A partition omitted from the newly constructed map is omitted from the newly materialized checkpoint contents.

**Primary anchor:** Apache Kafka tag `0.8.2.0`, `core/src/main/scala/kafka/server/ReplicaManager.scala`, `checkpointHighWatermarks()`.

URL: <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/server/ReplicaManager.scala>

### H/P — `OffsetCheckpoint.write()` replaces the checkpoint file from a temporary file

The exact `0.8.2.0` `OffsetCheckpoint` implementation writes:

- version `0`;
- the number of entries;
- one `topic partition offset` line per supplied map entry.

It writes those contents to `<checkpoint>.tmp`, flushes the buffered writer, calls `FileDescriptor.sync()` on the temporary file, then attempts to rename the temporary file over the previous checkpoint. On platforms where `renameTo()` does not replace an existing target, the implementation deletes the destination first and retries the rename.

At object construction it also deletes a leftover `.tmp` file and creates the checkpoint file if necessary.

**Primary anchor:** Apache Kafka tag `0.8.2.0`, `core/src/main/scala/kafka/server/OffsetCheckpoint.scala`.

URL: <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/server/OffsetCheckpoint.scala>

### H/P — checkpoint read validates the serialized map, but absence of one partition is not file corruption

`OffsetCheckpoint.read()` checks the version, parses each line, and verifies that the parsed entry count matches the serialized expected count. But a syntactically valid checkpoint can simply lack a particular partition.

`Partition.getOrCreateReplica()` then:

1. reads the checkpoint map for the log directory;
2. warns if the current partition has no entry;
3. uses `0L` when the entry is absent;
4. otherwise uses the checkpoint value, clamped to the local log end offset.

Thus:

```text
well-formed checkpoint file
    != complete checkpoint membership for every extant local log
```

and, in this bounded implementation:

```text
missing partition checkpoint entry
    -> recovered local high watermark = 0
```

**Primary anchors:** `OffsetCheckpoint.scala`; `Partition.scala`, tag `0.8.2.0`.

URL: <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/cluster/Partition.scala>

### H/P — before KAFKA-1647, an unavailable new leader could leave the local replica object uncreated

The parent of the fixing commit is `89831204c092f3a417bf41945925a2e9a0ec828e`.

In that pre-fix `ReplicaManager.makeFollowers()` path, when a `LeaderAndIsrRequest` named a new leader that was unavailable, the broker logged an error and aborted that partition's become-follower transition. The branch did **not** call `partition.getOrCreateReplica()`.

This matters because checkpoint generation enumerated `Replica` objects, not merely directories containing partition logs.

So the pre-fix state relation could be:

```text
local partition log exists
    + no local Replica object was created for this transition
    -> partition absent from checkpointHighWatermarks() input set
```

**Primary anchor:** Apache Kafka commit parent `89831204c092f3a417bf41945925a2e9a0ec828e`, `ReplicaManager.scala`.

URL: <https://github.com/apache/kafka/blob/89831204c092f3a417bf41945925a2e9a0ec828e/core/src/main/scala/kafka/server/ReplicaManager.scala>

### H/P — KAFKA-1647 was reported as a production-observed hard-kill/restart bug

ASF JIRA KAFKA-1647 is titled **“Replication offset checkpoints (high water marks) can be lost on hard kills and restarts.”** It is recorded as a resolved critical bug affecting and fixed in `0.8.2.0`.

The report says the scenario had been encountered in a production environment and gives a concrete multi-broker example. After a parallel hard kill and restart, a partition could retain its local log but lack a local replica object when its new leader was unavailable. When the high-watermark checkpoint thread subsequently rewrote the checkpoint file, only partitions represented by local replica objects were included; an older checkpoint entry for the omitted partition could therefore disappear.

The report lists possible symptoms including:

- data loss in a later sequence of follower truncation and leadership change;
- high I/O when a broker with a lost high watermark later truncates its log to zero and refetches from the beginning;
- offset resets if the offsets topic is affected, because offset loading does not read beyond the high watermark.

These are historical issue-report claims for the bounded bug, not a general statement that every hard kill causes these outcomes.

**Primary project record:** ASF JIRA KAFKA-1647.

URL: <https://issues.apache.org/jira/browse/KAFKA-1647>

### H/P — the 30 October 2014 fix makes checkpoint membership explicit

Apache commit `1ed9cf6d03603518d950f7e9a5f122c4ed5d7cee`, committed on **30 October 2014**, has the message:

> `KAFKA-1647; Create replicas on follower transition even if leader is unavailable, otherwise replication offset checkpoints (high water marks) can be lost on hard kills and restarts`

The functional change is small and unusually revealing. In the branch where the new leader is unavailable, the code now calls:

```scala
partition.getOrCreateReplica()
```

with an adjacent comment saying this is required so the partition's high watermark is included in the checkpoint file.

The historical point is therefore not inferred from a modern architecture description: the fix itself states that **existence of the local replica object was a prerequisite for preserving that partition's high-watermark entry across a checkpoint rewrite**.

**Primary anchor:** Apache Kafka commit `1ed9cf6d03603518d950f7e9a5f122c4ed5d7cee`.

URL: <https://github.com/apache/kafka/commit/1ed9cf6d03603518d950f7e9a5f122c4ed5d7cee>

### H/P — released 0.8.2.0 contains the fix

The final `0.8.2.0` source retains the KAFKA-1647 branch comment and `partition.getOrCreateReplica()` call when the new leader is unavailable.

Therefore this case should distinguish:

```text
pre-fix 2014 source behavior
    != released 0.8.2.0 behavior
```

The bug is useful historical evidence for why the retained checkpoint membership matters; it must not be described as an unfixed defect of the final 0.8.2.0 tag.

**Primary anchor:** tag `0.8.2.0`, `ReplicaManager.scala`.

---

## High-watermark checkpoint versus recovery-point checkpoint

Kafka 0.8.2.0 also has a separate file named `recovery-point-offset-checkpoint` managed by `LogManager`.

The two checkpoint families should not be collapsed merely because both serialize `TopicAndPartition -> offset` maps with `OffsetCheckpoint`.

### H/P — `replication-offset-checkpoint`

Owned by `ReplicaManager` and populated from each local replica's **high watermark**.

Its bounded role is replication/consumer recovery state: `Partition.getOrCreateReplica()` uses it to initialize the local replica high watermark after startup.

### H/P — `recovery-point-offset-checkpoint`

Owned by `LogManager` and populated from each log's **recovery point**.

`LogManager.loadLogs()` reads this file and passes the recovered point into `new Log(...)`. The source describes the recovery-point checkpoint as avoiding recovery of the whole log on startup.

`LogManager.truncateTo()` also calls `checkpointRecoveryPointOffsets()` after truncation.

### Engineering distinction

```text
replication high watermark
    != local log recovery point

replication-offset-checkpoint
    != recovery-point-offset-checkpoint
```

The shared serializer does not make the two offsets interchangeable.

This distinction is particularly important for KAFKA-1647: loss of a high-watermark entry can cause the reconstructed **replication boundary** to fall to zero; a later follower transition can then use that high watermark as the truncation target, after which local log recovery metadata is checkpointed for the now-truncated log.

That propagation is stronger than “one metadata file became stale.” A lost control frontier can authorize subsequent payload forgetting.

**Primary anchors:** `ReplicaManager.scala`, `Partition.scala`, `LogManager.scala`, tag `0.8.2.0`.

---

## Retained-state decomposition

This deepening adds several distinct objects to the Case 56 decomposition.

### 1. Payload log

The topic-partition log directory and its record bytes.

### 2. Runtime local `Replica` object

The in-process object through which `ReplicaManager` discovers the local partition's high watermark for checkpoint emission.

It is not itself durable retained state.

### 3. Runtime high watermark

The current replication/visibility prefix boundary held by the local replica.

### 4. Durable high-watermark entry

A `topic partition offset` tuple in `replication-offset-checkpoint`.

### 5. Checkpoint membership

The fact that the partition is present at all in the newly materialized checkpoint map.

This is distinct from the numerical offset value.

### 6. Local-log recovery point

The offset used by the log subsystem to bound local startup recovery work.

### 7. Durable recovery-point entry

The corresponding entry in `recovery-point-offset-checkpoint`.

The useful chain is therefore:

```text
payload bytes on disk
    != runtime replica object
    != runtime high watermark
    != durable HW value
    != membership of partition in HW checkpoint
    != log recovery point
```

KAFKA-1647 specifically demonstrates that losing **membership of the partition in the checkpoint rewrite** can matter even when the payload directory survives.

---

## Engineering reconstruction

### E — durable value retention depends on durable membership retention

A map-like checkpoint has two independent questions:

```text
what value is stored for key K?
which keys K survive the next materialization?
```

KAFKA-1647 failed at the second question. The old value was not merely updated to a bad offset; the partition could disappear from the rewritten map because no runtime `Replica` object caused it to be emitted.

### E — payload survival does not reconstruct protocol qualification automatically

The log bytes can remain physically present while the high-watermark checkpoint entry disappears. In the bounded startup code, absence is interpreted as high watermark zero rather than “scan payload and infer the previous committed frontier.”

So:

```text
surviving payload
    != surviving knowledge of committed prefix
```

### E — default-on-missing is a recovery policy, not evidence of historical truth

`0L` is a conservative software fallback for an absent checkpoint entry. It is not evidence that the partition historically had committed nothing.

### E — metadata loss can amplify into payload rewrite/truncation work

The JIRA report's high-I/O symptom makes the amplification explicit: a lost watermark can lead to truncation to zero and refetch from the beginning.

Thus:

```text
small control-state loss
    -> potentially large physical rewrite / network recovery work
```

The relation is scenario-dependent, not universal.

### E — checkpoint freshness and checkpoint membership are different failure axes

Periodic checkpointing already implies the durable offset may lag the latest in-memory high watermark. KAFKA-1647 is a different failure:

```text
stale but present checkpoint entry
    != omitted checkpoint entry
```

The latter can trigger the zero fallback.

### E — serializer reuse does not imply semantic identity

Both high-watermark and recovery-point files use `OffsetCheckpoint`, yet they encode different frontiers maintained by different subsystems.

```text
same file format
    != same retained meaning
```

---

## Functional comparison

### F — Case 100 ZFS DTL persistence

Case 100 shows that compact non-payload control metadata can preserve outstanding repair obligations across reload. Case 56 KAFKA-1647 shows a different failure shape: compact non-payload metadata preserves a committed-prefix recovery boundary, and omission of one key can cause excessive rollback/re-replication.

Functional commonality:

```text
payload survives
    != maintenance / recovery control state survives
```

No shared implementation or historical lineage is claimed.

### F — Case 49 HDFS generation-stamp recovery

Case 49 and this Kafka slice both show that a recovery controller may deliberately shorten physically surviving data according to retained authority metadata. HDFS generation stamps/lease recovery and Kafka high watermarks/ISR are different protocols.

### F — Case 25 Swift durability witnesses

Both systems separate a payload embodiment from metadata that determines whether/how that payload participates in recovery. Swift EC durable markers and Kafka high-watermark checkpoints are not analogous file formats and have no claimed genealogy.

---

## Philosophical interpretation — bounded

### P — retained history includes rules for where history is allowed to end

KAFKA-1647 is a concrete reminder that “the data survived” and “the system remembers how much of that data belonged to the committed past” are different propositions.

The second proposition can be embodied in a tiny checkpoint map whose loss changes future recovery behavior.

This is a project-level interpretation. Apache's historical issue and source discuss high watermarks, checkpoints, replicas, truncation, and recovery, not a philosophy of technical memory.

---

## Explicit non-claims

This deepening does **not** claim that:

1. every Kafka 0.8.2 hard kill loses high-watermark state;
2. the final `0.8.2.0` tag still contains the pre-fix KAFKA-1647 omission bug;
3. every absent checkpoint entry causes user-visible data loss;
4. a high-watermark checkpoint is the only source of Kafka recovery information;
5. a high watermark and a log recovery point mean the same thing;
6. `OffsetCheckpoint.write()` provides a proven crash-atomic transaction on every filesystem/platform;
7. `FileDescriptor.sync()` on the temporary file proves parent-directory durability;
8. Java `renameTo()` has identical replacement/crash semantics on every supported platform;
9. the `.tmp` cleanup behavior proves recovery from every interrupted rename sequence;
10. a syntactically valid checkpoint is semantically complete for every local log;
11. a missing checkpoint key proves historical high watermark zero;
12. the production incident quantified how frequently this defect occurred;
13. KAFKA-1647 independently proves ZooKeeper state loss or corruption;
14. later leader-epoch checkpoint machinery is identical to this 0.8.2 high-watermark checkpoint;
15. current Kafka retains the same files, defaults, or restart semantics.

---

## Claim ledger

| Claim | Type | Status |
| --- | --- | --- |
| 0.8.2 checkpointing enumerates local `Replica` objects and rewrites a fresh map | H/P | established in exact-tag source |
| `OffsetCheckpoint.write()` serializes supplied entries to a temp file, fsyncs that file, then renames | H/P | established in exact-tag source |
| missing partition entry falls back to high watermark `0L` | H/P | established in exact-tag `Partition.scala` |
| pre-fix unavailable-leader branch did not create the local replica object | H/P | established in parent source |
| KAFKA-1647 describes production-observed checkpoint loss after hard-kill/restart sequencing | H/P | established in ASF issue record |
| 30 Oct 2014 fix explicitly creates local replica to preserve checkpoint inclusion | H/P | established in Apache commit |
| released `0.8.2.0` contains that fix | H/P | established in exact tag |
| high-watermark checkpoint and recovery-point checkpoint are distinct semantics | H/P/E | established by source ownership/use |
| old checkpoint value retention depends on key inclusion in the next full-map rewrite | E | strongly supported |
| surviving payload does not by itself reconstruct the prior committed frontier in this startup path | E | supported |
| small control-state loss can amplify into large re-replication/truncation work | H/P/E | scenario established by JIRA; generalized only narrowly |
| checkpoint temp-file swap is crash-atomic on all filesystems | X | not established |
| final 0.8.2.0 still has the omission defect | X | rejected |
| high watermark = log recovery point | X | rejected |

---

## Sources

### Apache primary / period sources

1. ASF JIRA **KAFKA-1647 — Replication offset checkpoints (high water marks) can be lost on hard kills and restarts**: <https://issues.apache.org/jira/browse/KAFKA-1647>.
2. Apache Kafka commit `1ed9cf6d03603518d950f7e9a5f122c4ed5d7cee`, 30 October 2014, KAFKA-1647 fix: <https://github.com/apache/kafka/commit/1ed9cf6d03603518d950f7e9a5f122c4ed5d7cee>.
3. Pre-fix parent `89831204c092f3a417bf41945925a2e9a0ec828e`, `ReplicaManager.scala`: <https://github.com/apache/kafka/blob/89831204c092f3a417bf41945925a2e9a0ec828e/core/src/main/scala/kafka/server/ReplicaManager.scala>.
4. Kafka `0.8.2.0`, `ReplicaManager.scala`: <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/server/ReplicaManager.scala>.
5. Kafka `0.8.2.0`, `OffsetCheckpoint.scala`: <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/server/OffsetCheckpoint.scala>.
6. Kafka `0.8.2.0`, `Partition.scala`: <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/cluster/Partition.scala>.
7. Kafka `0.8.2.0`, `LogManager.scala`: <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/log/LogManager.scala>.

---

## Related-repository duplication check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `KAFKA-1647` found no dedicated treatment. This record therefore keeps only the retention-specific failure chain and does not attempt a general Kafka checkpoint/restart history.

If `computing-archaeology` later grows a Kafka broker-recovery chronology, this file should link to it and retain only the checkpoint-membership/control-state argument.

---

## Remaining debt after this slice

This deepening closes the **historical KAFKA-1647 checkpoint-membership failure** gap, but intentionally leaves open:

- independent fault injection reproducing the defect on a pre-fix revision and demonstrating the fixed revision;
- exact filesystem/device crash durability of the temp-file + `FileDescriptor.sync()` + `renameTo()` sequence;
- malformed high-watermark checkpoint startup behavior traced through the complete broker exception path;
- ZooKeeper ISR/leader-state crash composition with local checkpoint loss;
- modern Kafka's successor checkpoint/state machinery;
- quantitative frequency or fleet impact of KAFKA-1647 beyond the reported production incident.

None of these open items changes the bounded conclusion:

> **In the 2014 KAFKA-1647 failure, a partition could keep its local log while disappearing from the runtime set used to rewrite `replication-offset-checkpoint`; the missing durable high-watermark entry then reconstructed as zero and could drive later truncation/re-replication. The fix explicitly restored checkpoint membership by ensuring the local replica object existed even when the new leader was unavailable.**
