# Case 56 deepening — Kafka 0.8.2 high-watermark checkpoint coverage, restart state, and KAFKA-1647

**Status:** `bounded deepening complete`

## Research slice

This packet deepens one narrow question left implicit in Case 56:

> When Kafka 0.8.2 periodically persists a replica high watermark, what exactly has to survive for that checkpoint to remain usable after restart, and can a checkpoint file be successfully rewritten while silently losing a still-relevant partition boundary?

The answer is yes. Apache's 2014 KAFKA-1647 bug report and fix expose a failure mode that is more specific than generic file corruption or generic crash consistency: a broker could build the next checkpoint from an incomplete set of runtime replica objects, replace the previous checkpoint with that incomplete map, and thereby lose a partition's previously retained high-watermark boundary even though the checkpoint write path itself completed.

This slice therefore separates:

```text
live high watermark
    != periodically persisted high-watermark checkpoint
    != checkpoint-file integrity
    != checkpoint coverage/completeness
    != post-restart reconstructed runtime high watermark
```

The terms `checkpoint coverage`, `checkpoint completeness`, `runtime enumeration source`, and `recovery-boundary evidence` are project engineering terms. Apache's period vocabulary remains `high watermark`, `replication-offset-checkpoint`, `replica`, `partition`, `leader`, `follower`, and `ISR`.

This is not a general Kafka crash-consistency history, not a filesystem durability analysis, and not a study of later leader-epoch checkpoints.

---

## Why this slice is not duplicate work

The existing Case 56 grounding already establishes that Kafka 0.8.2:

- advances the leader high watermark from the current ISR frontier;
- caps ordinary consumer visibility at the high watermark;
- periodically writes high-watermark state to `replication-offset-checkpoint`;
- reads the checkpoint when creating a local replica after restart;
- can truncate a physically longer suffix during bounded recovery paths.

What it did not yet isolate is the **retention dependency of the checkpoint itself**. KAFKA-1647 provides unusually direct evidence that a durable recovery boundary is not preserved merely because a checkpoint file exists or because the writer follows a write-temp/fsync/replace discipline. The set of partition entries selected for the next checkpoint is itself part of correctness.

Searches of `tmzncty/computing-archaeology` for `Kafka high watermark` and `replication-offset-checkpoint` found no dedicated packet to reuse at the time of this slice. Broader Kafka replication genealogy remains routed there if such a track is later created.

---

## Source boundary and evidence classes

The principal sources are all Apache/Kafka primary artifacts:

1. the exact `0.8.2.0` source tag;
2. KAFKA-1647, created 23 September 2014 and resolved 30 October 2014, marked `Critical`, affecting and fixed in 0.8.2.0;
3. the fixing commit `1ed9cf6d03603518d950f7e9a5f122c4ed5d7cee`, committed 30 October 2014;
4. the 0.8.2 broker configuration/source default for `replica.high.watermark.checkpoint.interval.ms`.

The JIRA issue is especially valuable because it reports a production-observed failure scenario and distinguishes symptoms the reporters actually saw from additional possible consequences. It is still an engineering issue report, not an independent controlled fault-injection paper.

---

# Historical record

## H/P — 0.8.2 periodically checkpoints the high watermark rather than persisting every transition synchronously

`KafkaConfig.scala` in tag `0.8.2.0` defines:

```text
replica.high.watermark.checkpoint.interval.ms = 5000 ms by default
```

and describes it as the frequency with which the high watermark is saved to disk.

`ReplicaManager.startHighWaterMarksCheckPointThread()` schedules `checkpointHighWatermarks` at that configured period.

This directly establishes a distinction between the **live runtime high watermark** and the **most recently persisted checkpoint image**. The code does not synchronously persist every high-watermark advancement.

Primary anchors:

- <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/server/KafkaConfig.scala>
- <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/server/ReplicaManager.scala>

## H/P — the checkpoint is a map assembled from runtime local-replica objects

`ReplicaManager.checkpointHighWatermarks()` does not scan log directories and independently rediscover every partition that might need a boundary. It:

1. iterates the broker's current partition objects;
2. asks each for the local replica;
3. keeps replicas with local logs;
4. groups them by log directory;
5. writes a topic/partition → high-watermark map for each directory.

The persistence path therefore depends on the runtime object graph containing every local partition whose high watermark must remain represented.

That is a historical implementation fact, not merely a reconstruction inferred from the later bug report.

Primary anchor:

- `ReplicaManager.scala`, tag `0.8.2.0`, `checkpointHighWatermarks`.

## H/P — clean shutdown explicitly checkpoints high watermarks

In tag `0.8.2.0`, `ReplicaManager.shutdown()` stops the replica fetcher manager and then calls `checkpointHighWatermarks()` before declaring shutdown complete.

This is evidence for a distinct **clean-shutdown handoff path** in addition to the periodic scheduler.

It does not prove that every process termination reaches this path, nor that the resulting file is guaranteed against all lower-layer power-loss behaviors.

Primary anchor:

- `ReplicaManager.scala`, tag `0.8.2.0`, `shutdown`.

## H/P — the checkpoint writer uses a temporary file, file-data sync, and replacement

`OffsetCheckpoint.scala` writes the map to `<checkpoint>.tmp`, flushes the buffered writer, calls `FileDescriptor.sync()` on the temporary file, closes it, and then replaces the previous checkpoint using `renameTo`, with a delete-and-retry fallback for platforms where replacing an existing destination fails.

The reader stores a format version and expected entry count and rejects malformed records or a count mismatch.

This provides evidence for **file-level replacement discipline and internal format validation**.

It does **not** by itself prove:

- parent-directory fsync;
- identical rename/power-failure semantics on every supported filesystem/OS;
- atomicity across all crash points;
- semantic completeness of the set of entries written.

Primary anchor:

- <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/server/OffsetCheckpoint.scala>

## H/P — restart initializes a local replica from the checkpoint but clamps it to the current log end

`Partition.getOrCreateReplica()` in tag `0.8.2.0`:

1. opens/creates the local partition log;
2. reads the high-watermark checkpoint for that log directory;
3. warns if the topic/partition entry is absent;
4. uses `0` when no checkpoint entry exists;
5. otherwise takes the minimum of the checkpoint value and the local log end;
6. initializes the local `Replica` with that value.

Thus the persisted boundary is **recovery input**, not an unconstrained authority that may point beyond the physically available local log.

The source also makes an absent entry materially different from a present positive checkpoint: absence falls back to zero.

Primary anchor:

- <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/cluster/Partition.scala>

## H/P — KAFKA-1647 reports loss of checkpoint entries after hard kills/restarts

Apache KAFKA-1647 is titled **“Replication offset checkpoints (high water marks) can be lost on hard kills and restarts.”** It was filed 23 September 2014, classified `Critical`, and resolved 30 October 2014 for 0.8.2.0.

The report describes a production-discovered multi-broker scenario in which all replicas for a partition can be down during restart sequencing. A broker receives a `LeaderAndIsrRequest`, but for one partition the designated leader is still unavailable. In the pre-fix path, the broker aborts the become-follower transition before creating the local replica object for that partition.

The checkpoint thread later enumerates only the local replica objects that exist. The affected partition is therefore omitted from the newly written checkpoint map, and its previously stored high-watermark entry can disappear when the checkpoint file is replaced.

Primary anchor:

- <https://issues.apache.org/jira/browse/KAFKA-1647>

## H/P — the reported defect is an enumeration/coverage defect, not simply a failed disk write

The critical causal step in KAFKA-1647 is not “checkpoint write returned an I/O error.” The issue instead explains that only partitions with local replica objects are included, so a partition whose replica object was not created is absent from the successful checkpoint rewrite.

This yields a strong bounded distinction:

```text
checkpoint write success
    != complete representation of all still-relevant partition boundaries
```

The old checkpoint can therefore be logically weakened by a successful replacement operation.

This is the central new evidence of the slice.

## H/P — Apache reported concrete downstream consequences of missing checkpoint coverage

KAFKA-1647 lists several possible symptoms. The issue says the reporters observed the latter two of the three listed classes:

- a broker whose high watermark is lost may later truncate a log to zero and refetch from the beginning, causing high I/O;
- if the offsets topic is affected, offsets can reset because offset loading does not read beyond the high watermark;
- the issue additionally warns of a data-loss path under the described hard-kill/re-election sequence.

The evidence boundary matters:

- the issue directly says high I/O and offset reset were observed by the reporters;
- data loss is presented as a possible symptom of the defect scenario, not as one of the two symptoms they say they observed.

Primary anchor:

- KAFKA-1647 description and symptom list.

## H/P — the fix preserves checkpoint coverage by creating the local replica even when the leader is unavailable

Commit `1ed9cf6d03603518d950f7e9a5f122c4ed5d7cee` is explicitly titled:

> KAFKA-1647; Create replicas on follower transition even if leader is unavailable ...

The diff changes the unavailable-leader branch so that it still creates the local replica. The accompanying source comment states that this is required so the partition's high watermark is included in the checkpoint file.

The fix therefore preserves a runtime object needed for future checkpoint enumeration even though the broker still cannot complete the ordinary become-follower state transition at that moment.

Primary anchor:

- <https://github.com/apache/kafka/commit/1ed9cf6d03603518d950f7e9a5f122c4ed5d7cee>

## H/P — the released 0.8.2.0 source retains the fix rationale

The `0.8.2.0` tag contains the same unavailable-leader branch with the explicit KAFKA-1647 comment and `partition.getOrCreateReplica()` call.

This matters because the JIRA lists 0.8.2.0 as both affected and fixed: the issue occurred during the 0.8.2.0 development line, and the released tag contains the corrective logic. It should not be narrated as a post-release 0.8.2.1 fix.

Primary anchor:

- `ReplicaManager.scala`, tag `0.8.2.0`.

---

# Engineering reconstruction

## E — persisted checkpoint bytes ≠ preserved checkpoint meaning

A checkpoint file can remain parseable and successfully replaced while losing a still-needed topic/partition entry.

The retained object is therefore not just “the file.” It includes the relation:

```text
(topic, partition)
    -> retained high-watermark boundary
```

Preserving file existence without preserving the relevant mapping is insufficient.

## E — file integrity ≠ semantic completeness

`OffsetCheckpoint` can validate version, line structure, and declared entry count. Those checks answer questions such as:

- Is this file structurally parseable?
- Did the file contain the number of entries it declared?

They do not answer:

- Did the runtime enumerator include every partition that still required a checkpoint entry?

KAFKA-1647 is therefore a direct counterexample to treating structural consistency as semantic completeness.

## E — checkpoint replacement discipline ≠ checkpoint coverage correctness

Writing a new image to a temporary file, syncing it, and replacing the old file can reduce torn-file exposure while still committing the wrong set of entries.

A useful bounded relation is:

```text
safe-ish replacement mechanics
    != correct snapshot membership
```

This is not an argument that the 0.8.2 replacement path is universally crash-atomic. It is a narrower point: **even perfect file replacement would not cure the KAFKA-1647 omission bug.**

## E — runtime reachability can be retention infrastructure

The local `Replica` object looks like volatile runtime state, but in this implementation it is also the enumeration source from which a durable checkpoint image is produced.

Therefore:

```text
runtime object existence
    -> future checkpoint inclusion
    -> restart boundary survival
```

A volatile object can thus participate in preserving a durable relation without itself surviving the restart.

This is a reconstruction of the implementation dependency, not Apache's historical terminology.

## E — high-watermark persistence is periodic evidence, not persistence of every high-watermark transition

With a 5000 ms default checkpoint interval, the live high watermark can move after the latest durable checkpoint and before a crash.

That ordinary staleness window is distinct from KAFKA-1647:

- **ordinary periodic lag:** the entry exists but may be older than the most recent live high watermark;
- **KAFKA-1647 coverage loss:** the partition entry can disappear from a rewritten checkpoint entirely.

These failure classes should not be collapsed.

## E — clean shutdown closure ≠ hard-kill closure

The explicit shutdown path checkpoints high watermarks. KAFKA-1647 concerns hard-kill/restart sequencing where that closure cannot be assumed.

Thus:

```text
clean lifecycle handoff
    != abrupt-failure retained state
```

The presence of a clean shutdown hook is not evidence that abrupt process or machine loss preserves the same most-recent runtime boundary.

## E — missing checkpoint entry ≠ no payload bytes

On restart, an absent entry falls back to high watermark zero even when the local log can contain data.

This is an unusually sharp demonstration that:

```text
payload embodiment survives
    != recovery boundary survives
```

The local bytes alone do not reconstruct the lost high-watermark commitment relation in this 0.8.2 path.

## E — missing boundary can change what future recovery is allowed to keep

Because the high watermark participates in follower truncation/recovery, losing the checkpoint boundary can cause a broker to treat a much smaller prefix as the known committed frontier. KAFKA-1647's symptom description makes the practical effect explicit: logs may be truncated to zero and refetched.

Retained metadata is therefore not merely diagnostic history. It can govern future destructive recovery action.

## E — retention of currentness metadata can require retaining an otherwise transitional object

The fix is conceptually revealing: even when the designated leader is unavailable and the ordinary follower transition cannot proceed, Apache creates the local replica object anyway so the high watermark remains represented in the checkpoint.

The local object is retained in runtime not because the follower is already operationally current, but because it is needed to preserve recovery metadata across a later checkpoint rewrite.

This separates:

```text
replica object exists for checkpoint coverage
    != follower transition completed
    != leader is reachable
```

## E — a checkpoint is a selected statement about current state, not a passive dump of everything on disk

Kafka 0.8.2's high-watermark file does not infer commitment by scanning records. It serializes selected protocol state from live objects.

A checkpoint therefore has an **epistemic source**: the in-memory structures that are considered eligible to contribute entries. Bugs in that selection relation can destroy recovery knowledge even when the underlying log files remain intact.

---

# Controlled functional comparisons

## A — Case 46 GFS checkpoint: snapshot completeness is a semantic property

Case 46's GFS master checkpoint and Kafka's high-watermark checkpoint are historically and mechanically different:

- GFS uses a checkpoint plus operation-log suffix to reconstruct master metadata;
- Kafka 0.8.2 stores compact per-partition high-watermark boundaries and later rebuilds live replica state around them.

The bounded functional comparison is only this:

> A checkpoint's usefulness depends on whether it contains the state classes that the recovery procedure expects, not merely on whether a checkpoint file survived.

No genealogy or implementation identity is claimed.

## A — Case 04 FTL crash recovery: last durable recovery evidence need not equal final pre-crash runtime state

Case 04's DCR/FTL material and Kafka 0.8.2 both distinguish live runtime state from a durable recovery boundary. But their mechanisms differ sharply:

- the FTL case may reconstruct mapping from a checkpoint plus post-checkpoint media evidence;
- Kafka 0.8.2's high-watermark checkpoint is a replicated-log currentness boundary, not an FTL map and not a replay log of every high-watermark transition.

The shared engineering lesson is bounded:

```text
last durable recovery evidence
    != complete state immediately before crash
```

## A — Case 90 leader-epoch recovery must remain separate

Kafka 0.11's leader-epoch checkpoint retains sparse leadership-lineage boundaries used to qualify divergent-log truncation. It is not the same object as the 0.8.2 `replication-offset-checkpoint` high-watermark file.

Do not use later leader-epoch semantics to explain the KAFKA-1647 defect. This packet remains strictly inside the 0.8.2 high-watermark mechanism.

---

# Philosophical interpretation — bounded and downstream

## I — persistence of a container is not persistence of every relation it once represented

KAFKA-1647 gives a precise technical counterexample to a naive notion of digital persistence. The checkpoint file can continue to exist, be structurally valid, and have been freshly synced, while one partition's recovery boundary has disappeared from it.

The philosophically useful distinction is therefore:

```text
artifact survives
    != represented relation survives
```

This is downstream interpretation. Apache did not formulate the bug in these terms.

## I — forgetting can occur through omission during successful rewriting

The lost high-watermark entry need not be erased by media decay, corruption, or an explicit delete command. It can disappear because the next complete-file rewrite is constructed from an incomplete enumeration.

That yields a bounded form of technical forgetting:

> **a relation may be forgotten by omission from the next authoritative representation.**

This should not be generalized into a claim about all checkpoints or all distributed systems.

## I — durable state may depend on transient state that does not itself need to endure

The fix makes a volatile runtime object part of a durability chain: keeping the local replica object reachable allows the next durable checkpoint to retain the partition boundary. The object itself may vanish at restart, but the durable relation it helps serialize can survive.

This complicates any simple opposition between “volatile” and “persistent” state. The two can form a production relation in which transient state is necessary to refresh or reproduce persistent state.

---

# Explicit non-claims

This packet does **not** establish that:

1. every Kafka 0.8.2 high-watermark advancement was synchronously durable;
2. the default five-second interval is a durability SLA;
3. a five-second-old checkpoint implies exactly five seconds of possible message loss;
4. the checkpoint alone proves payload bytes were durably flushed through every lower storage layer;
5. Java `renameTo` is crash-atomic on every filesystem/platform;
6. `FileDescriptor.sync()` of the temp file fsyncs the parent directory;
7. the 0.8.2 checkpoint writer is immune to torn writes, media faults, or filesystem bugs;
8. KAFKA-1647 was caused by a failed `fsync` or failed `rename`;
9. KAFKA-1647 means the checkpoint file itself necessarily disappeared;
10. every hard kill reproduces KAFKA-1647;
11. every restart loses the high watermark;
12. every missing high watermark causes application payload loss;
13. the issue reporters directly observed the listed data-loss outcome; their issue text says they observed the other two listed symptoms;
14. a missing checkpoint means the corresponding local log contains no records;
15. the local log can reconstruct the old high watermark without additional protocol state;
16. the checkpoint is a complete history of ISR membership or replication events;
17. high-watermark checkpointing is the same mechanism as log-segment flushing;
18. high-watermark checkpointing is the same mechanism as consumer-offset commits;
19. high-watermark checkpointing is the same mechanism as Kafka 0.11 leader-epoch checkpointing;
20. high watermark is the same as the transactional last stable offset;
21. creating a local replica object means the broker successfully became a follower;
22. creating a local replica object means the designated leader was reachable;
23. every structurally valid checkpoint is semantically complete;
24. write-temp/fsync/replace mechanics can compensate for an incomplete source enumeration;
25. Kafka invented checkpoint/restart recovery, replicated logs, or commit frontiers;
26. the KAFKA-1647 fix proves all later Kafka checkpoint/restart bugs were eliminated;
27. the 0.8.2 source semantics can be projected unchanged onto modern Kafka/KRaft;
28. this issue establishes filesystem/device power-loss guarantees below Kafka;
29. this issue is an independent academic fault-injection experiment;
30. the bounded engineering comparison to GFS or FTL implies direct technical genealogy.

---

# Claim ledger

| Claim | Type | Status | Primary basis |
| --- | --- | --- | --- |
| 0.8.2 checkpoints high watermarks periodically | H/P | established | `KafkaConfig.scala`, `ReplicaManager.scala` |
| default checkpoint interval is 5000 ms | H/P | established | `KafkaConfig.scala` tag `0.8.2.0` |
| clean shutdown explicitly checkpoints high watermarks | H/P | established | `ReplicaManager.shutdown()` |
| checkpoint map is assembled from current local replica objects | H/P | established | `ReplicaManager.checkpointHighWatermarks()` |
| checkpoint writer uses temp file + flush + file sync + replacement | H/P | established | `OffsetCheckpoint.scala` |
| checkpoint reader checks format version and entry count | H/P | established | `OffsetCheckpoint.scala` |
| local replica initialization reads checkpoint and clamps to local LEO | H/P | established | `Partition.getOrCreateReplica()` |
| missing checkpoint entry falls back to zero | H/P | established | `Partition.getOrCreateReplica()` |
| KAFKA-1647 reports checkpoint entry loss after hard-kill/restart sequencing | H/P | established | Apache JIRA |
| defect can arise because an unavailable leader prevents creation of a local replica object | H/P | established | JIRA + fixing commit |
| next checkpoint can omit that partition and lose its previous boundary | H/P/E | established in bounded defect | JIRA + writer enumeration path |
| fix creates local replica even when leader unavailable so HW remains checkpointed | H/P | established | commit `1ed9cf6...` + released source |
| file integrity ≠ checkpoint semantic completeness | E | strongly supported | KAFKA-1647 mechanism |
| periodic checkpoint staleness ≠ partition-entry omission | E | supported | config + KAFKA-1647 |
| runtime reachability can be part of a durable-state production chain | E | supported | fix dependency |
| artifact survival ≠ represented-relation survival | I | bounded interpretation | downstream synthesis |
| `renameTo` proves universal crash atomicity | X | rejected | not established by source |
| every missing HW implies payload loss | X | rejected | not established |
| later leader-epoch checkpoint semantics explain this bug | X | rejected | different mechanism/version |

---

# Sources

## Apache primary sources

1. Apache Kafka source tag `0.8.2.0`, `KafkaConfig.scala` — `replica.high.watermark.checkpoint.interval.ms` default and description:  
   <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/server/KafkaConfig.scala>

2. Apache Kafka source tag `0.8.2.0`, `ReplicaManager.scala` — periodic scheduling, checkpoint enumeration, clean-shutdown checkpoint, and released KAFKA-1647 fix:  
   <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/server/ReplicaManager.scala>

3. Apache Kafka source tag `0.8.2.0`, `OffsetCheckpoint.scala` — file format, temp-file write, `sync()`, replacement, and read validation:  
   <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/server/OffsetCheckpoint.scala>

4. Apache Kafka source tag `0.8.2.0`, `Partition.scala` — checkpoint read, missing-entry fallback, and clamp to local log end:  
   <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/cluster/Partition.scala>

5. Apache JIRA **KAFKA-1647 — Replication offset checkpoints (high water marks) can be lost on hard kills and restarts**, created 23 September 2014, resolved 30 October 2014:  
   <https://issues.apache.org/jira/browse/KAFKA-1647>

6. Apache Kafka commit `1ed9cf6d03603518d950f7e9a5f122c4ed5d7cee`, **KAFKA-1647; Create replicas on follower transition even if leader is unavailable...**, 30 October 2014:  
   <https://github.com/apache/kafka/commit/1ed9cf6d03603518d950f7e9a5f122c4ed5d7cee>

## Repository-local comparison anchors

7. [`cases/56-apache-kafka-replicated-log-high-watermark.md`](../cases/56-apache-kafka-replicated-log-high-watermark.md)
8. [`cases/46-google-gfs-master-log-checkpoint-recovery.md`](../cases/46-google-gfs-master-log-checkpoint-recovery.md)
9. [`cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md)
10. [`cases/90-apache-kafka-leader-epoch-safe-truncation.md`](../cases/90-apache-kafka-leader-epoch-safe-truncation.md)

---

# Remaining evidence debt

This slice closes the bounded **checkpoint coverage / runtime-enumeration** debt for Case 56. It does not close:

- exact lower-filesystem crash behavior of the 0.8.2 temp-file/rename path;
- fault injection at each checkpoint write/rename crash point;
- an independently reproduced KAFKA-1647 scenario on a preserved 0.8.2 build;
- exact interactions with log flush/recovery-point checkpointing below the high watermark;
- full chronology of later changes to high-watermark checkpoint formats/ownership;
- later leader-epoch recovery, which remains Case 90;
- KRaft-era metadata/recovery semantics;
- device-level persistence below Kafka.

A particularly useful future experiment would run a preserved 0.8.2 build with controlled process kills at three different layers: after a live HW advance but before the next scheduled checkpoint, during checkpoint-file replacement, and during the unavailable-leader restart sequence represented by KAFKA-1647. Those are three different retention failures and should not be reported as one generic “crash consistency” result.
