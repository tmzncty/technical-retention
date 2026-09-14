# Grounding Record — Apache Kafka 0.8.2 Replication High Watermark

## Target case

[`cases/56-apache-kafka-replicated-log-high-watermark.md`](../cases/56-apache-kafka-replicated-log-high-watermark.md)

## Promotion decision

**Status: `grounded`.**

This record grounds one bounded question:

> In Apache Kafka 0.8.2.0, what protocol and retained control state distinguish a physically present log suffix from the committed/current prefix that ordinary consumers may observe and future leaders are expected to preserve?

It does not claim to ground the full Kafka replication genealogy or current Kafka semantics.

---

## Source set

### A. Apache Kafka 0.8.2 versioned design documentation — primary

URL: <https://kafka.apache.org/082/design/design/>

Relevant section: `Replication`, including `Replicated Logs: Quorums, ISRs, and State Machines`, `Unclean leader election`, and availability/durability discussion.

Directly supports:

- partition as the unit of replication;
- one leader plus followers;
- leader tracking an `in sync` set;
- commitment only after all current ISR members have applied a message;
- ordinary consumer exposure of committed messages;
- committed-message guarantee conditional on at least one ISR replica remaining alive;
- ISR as the normal leader-eligibility set;
- ISR persistence to ZooKeeper when changed;
- explicit contrast between Kafka's ISR approach and majority voting;
- unclean-election availability-versus-consistency trade-off;
- Apache's own acknowledgement of earlier replicated-log/consensus work, including PacificA.

**Evidence strength:** strong period project documentation for intended semantics and historical vocabulary.

### B. Apache Kafka 0.8.2 broker configuration — primary

URL: <https://kafka.apache.org/082/configuration/broker-configs/>

Directly supports:

- `replica.lag.max.messages` as one ISR-removal condition in this release;
- `replica.high.watermark.checkpoint.interval.ms = 5000`, described as the frequency with which each replica saves its high watermark to disk `to handle recovery`;
- `unclean.leader.election.enable = true` in the bounded 0.8.2 documentation, with explicit warning that electing a non-ISR replica may cause data loss;
- topic `min.insync.replicas = 1` default and its composition with `request.required.acks=-1`.

**Evidence strength:** strong release-specific interface/configuration evidence.

### C. Apache Kafka source tag `0.8.2.0`, `Partition.scala` — primary implementation

URL: <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/cluster/Partition.scala>

Key inspected mechanisms:

1. `inSyncReplicas` is explicit partition state.
2. On local replica creation, the broker reads the high-watermark checkpoint and initializes the replica watermark to the checkpointed value clamped by local `logEndOffset`.
3. `updateLeaderHWAndMaybeExpandIsr` admits an assigned follower back into ISR only when its log end has reached at least the leader high watermark (plus assignment/not-already-member conditions).
4. `maybeIncrementLeaderHW` collects log-end offsets of current ISR replicas and selects their minimum as the candidate high watermark.
5. `maybeShrinkIsr` removes out-of-sync followers and then recomputes the high watermark.
6. `checkEnoughReplicasReachOffset` separates `requiredAcks`, high-watermark advancement, ISR size, and `min.insync.replicas`.

**Evidence strength:** direct exact-tag implementation evidence.

### D. Apache Kafka source tag `0.8.2.0`, `ReplicaManager.scala` — primary implementation

URL: <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/server/ReplicaManager.scala>

Key inspected mechanisms:

1. `HighWatermarkFilename = "replication-offset-checkpoint"`.
2. One `OffsetCheckpoint` object is created per log directory.
3. `startHighWaterMarksCheckPointThread` periodically schedules checkpointing at `replicaHighWatermarkCheckpointIntervalMs`.
4. `readMessageSet` uses no high-watermark cap for valid broker follower fetches, but for ordinary client fetches it supplies `Some(localReplica.highWatermark.messageOffset)` as `maxOffsetOpt` to `log.read`.

This is the strongest direct implementation anchor for:

> **follower replication may read/copy a tail that ordinary consumers are not yet allowed to observe.**

**Evidence strength:** direct exact-tag implementation evidence.

### E. Apache Kafka source tag `0.8.2.0`, `ReplicaFetcherThread.scala` — primary implementation

URL: <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/server/ReplicaFetcherThread.scala>

Key inspected mechanisms:

1. After appending fetched messages, follower high watermark is set to `min(follower log end offset, leader-reported HW)`.
2. `handleOffsetOutOfRange` contains an explicit unclean-election recovery scenario in its source comment.
3. If a returning follower has an end offset beyond the current leader's end offset, the follower can truncate to the current leader's end and resume fetching.
4. If topic configuration disallows unclean election, this source path halts rather than unexpectedly perform the data-losing truncation.
5. A separate branch handles a follower so old that its end lies before the leader's retained start, resetting the follower to the leader start offset.

**Evidence strength:** direct exact-tag implementation evidence and especially strong counterexample to `longer surviving log = more authoritative log`.

### F. Apache Kafka release record — primary project record

URL: <https://kafka.apache.org/community/downloads/>

Supports:

- Kafka 0.8.2.0 release date: **2 February 2015**.

The versioned upgrade page also states that replication was introduced with Kafka 0.8.x relative to 0.7.

### G. Kafka 0.8.0 release notes — primary project record

URL: <https://archive.apache.org/dist/kafka/0.8.0/RELEASE_NOTES.html>

Supports:

- KAFKA-50 `kafka intra-cluster replication support` as a 0.8.0 new feature.

This prevents a false claim that 0.8.2 invented Kafka replication.

### H. PacificA — prior-art / scholarly-primary boundary

Wei Lin, Mao Yang, Lintao Zhang, Lidong Zhou, **PacificA: Replication in Log-Based Distributed Storage Systems**, Microsoft Research, MSR-TR-2008-25, February 2008.

Official record: <https://www.microsoft.com/en-us/research/publication/pacifica-replication-in-log-based-distributed-storage-systems/>

Kafka's own 0.8.2 design says PacificA is the most similar academic publication the authors knew to Kafka's implementation. PacificA itself presents a practical replication framework for log-based distributed storage and explicitly situates practical replication on top of established consensus foundations.

**Evidence use:** prior-art/novelty boundary only. It is not used to infer undocumented Kafka details.

### I. KAFKA-1647 checkpoint-loss bug and fix — primary project record + implementation

ASF JIRA: <https://issues.apache.org/jira/browse/KAFKA-1647>

Fix commit: <https://github.com/apache/kafka/commit/1ed9cf6d03603518d950f7e9a5f122c4ed5d7cee>

Pre-fix parent: <https://github.com/apache/kafka/blob/89831204c092f3a417bf41945925a2e9a0ec828e/core/src/main/scala/kafka/server/ReplicaManager.scala>

Exact-tag serializer: <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/server/OffsetCheckpoint.scala>

Exact-tag log recovery-point implementation: <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/log/LogManager.scala>

Directly supports:

- the production-observed 2014 failure in which a partition could retain its local log yet disappear from a rewritten high-watermark checkpoint because no local `Replica` object had been created;
- missing checkpoint membership falling back to high watermark zero when the local replica was later reconstructed;
- the 30 October 2014 fix explicitly creating the local replica even if the new leader is unavailable so its high watermark is included in the checkpoint;
- the distinction between `replication-offset-checkpoint` and `recovery-point-offset-checkpoint` despite their use of the same `OffsetCheckpoint` serializer;
- the exact temp-file, file-fsync, rename replacement sequence used by `OffsetCheckpoint.write()` without establishing universal filesystem crash atomicity.

**Evidence strength:** unusually strong bug/fix genealogy because issue report, pre-fix source, fixing commit, and released exact-tag behavior all align.

Detailed bounded record: [`56-kafka-2014-kafka1647-high-watermark-checkpoint-loss-deepening.md`](56-kafka-2014-kafka1647-high-watermark-checkpoint-loss-deepening.md).

---

## Evidence-to-claim map

| Claim | Evidence | Strength |
| --- | --- | --- |
| partition has leader/followers and leader tracks ISR | A, C | primary + source |
| committed means applied by all current ISR members in bounded design | A | primary design |
| ordinary consumers see only committed prefix | A, D | primary design + source |
| leader HW advances from minimum current ISR LEO | C | exact source |
| follower HW is bounded by follower LEO and leader HW | E | exact source |
| ISR membership can shrink and later expand with catch-up | A, C | design + source |
| ISR state is persisted to ZooKeeper when changed | A, C | design + source |
| HW has persistent checkpoint embodiment | B, C, D | config + source |
| replication factor / assigned set is not identical to ISR | A, B, C | strong |
| `acks=-1` composes with ISR/HW and `min.insync.replicas` | B, C | strong bounded source |
| 0.8.2 unclean election default is true | B | release-specific primary |
| non-ISR leader election may lose data | A, B | primary |
| returning longer follower can be truncated to current leader | E | exact source |
| checkpoint rewrite membership depends on enumerated local `Replica` objects | I | pre-fix/fix/exact-tag source |
| an absent partition checkpoint entry reconstructs local HW as zero | C, I | exact source |
| KAFKA-1647 could preserve payload log while losing the remembered committed frontier | I | production issue + source genealogy |
| `replication-offset-checkpoint` ≠ `recovery-point-offset-checkpoint` | I | exact source ownership/use |
| Kafka replication predates 0.8.2 | F, G | primary release history |
| Kafka did not invent replicated-log replication | A, H | explicit prior-art boundary |

---

## Historical record versus engineering reconstruction

### Historical record

The following are source-grounded historical facts for the bounded 0.8.2.0 regime:

- Apache used `ISR`, `committed`, `high watermark`, `log end offset`, and `unclean leader election` terminology.
- A partition had one leader and follower replicas.
- The high watermark was computed from ISR progress and checkpointed to disk.
- Ordinary reads were capped at the high watermark while follower replication could fetch beyond it.
- ISR could shrink and expand.
- unclean election could admit a non-ISR replica and risk data loss.
- the source contained a recovery path that truncates a returning follower to a shorter current leader.
- KAFKA-1647 recorded a production-observed failure where checkpoint rewrite membership could omit a partition whose local replica object had not been created after an unavailable-leader transition.
- the October 2014 fix explicitly ensured local-replica creation so that partition high-watermark state remained included in checkpoint generation.

### Engineering reconstruction

The project-level formulations below are not Apache's historical vocabulary even when strongly entailed by the mechanism:

- `physical record presence ≠ committed retention`;
- `leader LEO ≠ committed frontier`;
- `replication factor ≠ current redundancy margin`;
- `retained protocol metadata can define which surviving bytes count`;
- `failover convergence can require forgetting`;
- `longer surviving suffix ≠ greater authority`;
- `high-watermark checkpoint ≠ complete replication-history retention`;
- `durable checkpoint value ≠ durable checkpoint membership`;
- `surviving payload ≠ surviving knowledge of committed prefix`;
- `same checkpoint serializer ≠ same retained semantic frontier`.

### Functional analogy

Comparisons to RADOS peering, HDFS generation-stamp recovery, GFS checkpoints, ZFS DTL persistence, and Kafka log compaction are functional only. No common genealogy is inferred from shared words such as `log`, `replica`, `checkpoint`, `current`, or `truncate`.

### Philosophical interpretation

The case permits a narrow interpretation: technical persistence in a replicated system is not maximal physical survival but protocol-qualified continuity. This is an interpretation of the grounded mechanism, not a historical claim about Kafka engineers' philosophical intent.

---

## Counterevidence and qualification

### 1. 0.8.2 unclean election weakens the normal guarantee

This is not hidden as an implementation accident. Apache documented the availability/consistency trade-off and made unclean leader election configurable. Therefore the case must not state `Kafka always preserves all committed data` without the stated failure/policy assumptions.

### 2. `acks=-1` is not “all assigned replicas forever”

The 0.8.2 design/configuration and source tie it to the **current ISR**, subject also to `min.insync.replicas`. A failed assigned replica can be outside ISR while writes continue. The case therefore rejects `replication factor = required acknowledgements`.

### 3. A checkpoint interval implies a distinction between runtime and persisted control state

The config explicitly says the high watermark is saved periodically. The case does **not** infer from this alone that every crash loses committed data or that the checkpoint is the only recovery evidence. It only establishes that high-watermark recovery has a persistent checkpoint representation separate from payload logs.

### 4. Offset-based 0.8.2 recovery is not later leader-epoch recovery

Later Kafka work changed recovery semantics and added stronger leader-epoch mechanisms. Those later mechanisms must not be back-projected into this source slice. The first bounded follow-on is now grounded separately in [`56-kafka-0110-leader-epoch-lineage-truncation-deepening.md`](56-kafka-0110-leader-epoch-lineage-truncation-deepening.md): Kafka 0.11.0.0 retains per-replica leader-epoch/start-offset history and uses it as a lineage-aware truncation relation, while the high watermark remains a distinct committed/visibility frontier.

### 5. Consumer visibility is not the same question as producer completion

This case grounds ordinary consumer exposure against the high watermark. Producer acknowledgement has its own policy/configuration path. They interact but should not be collapsed into one generic `durable` event.

### 6. KAFKA-1647 is pre-fix history, not a defect claim against the released tag

The October 2014 commit fixes the omitted-replica checkpoint-membership path and the final `0.8.2.0` source contains the fix. The bug is used as historical evidence of why checkpoint membership matters, not as a claim that released 0.8.2.0 still loses that entry through the same path.

The same slice also does **not** promote `FileDescriptor.sync()` plus Java `renameTo()` into a universal crash-atomicity theorem. The exact filesystem/device durability boundary remains open.

---

## Cross-case contribution

This slice changes the repository's comparison in five useful ways.

### A. Replication introduces a retained **prefix boundary**

Cases 05/23/25 already show replica currentness/version admissibility. Kafka adds a particularly explicit ordered-log boundary: bytes above the high watermark can be physically present but outside committed consumer-visible history.

### B. More surviving state can be the wrong state

Cases 47 and 44 emphasize traces that survive too long during forgetting. Kafka 0.8.2 provides the converse problem during convergence: an extant longer suffix may have to be truncated because protocol authority selected another continuation.

### C. Retention metadata can be compact rather than historical

`replication-offset-checkpoint` preserves a recovery frontier without storing a full record of the replication events that established it. This strengthens Case 46's distinction between reconstructing/currently qualifying a state and retaining its full history.

### D. One software family can contain different forgetting mechanisms

Case 42 compaction removes superseded committed keyed history. Case 56 failover truncation removes a non-authoritative/divergent suffix. Both are `forgetting` only at a very abstract level; their safety conditions are different.

### E. Map membership can itself be retained recovery state

KAFKA-1647 adds a useful comparison to Case 100's persisted ZFS DTL basis: in both systems small non-payload control metadata changes subsequent recovery work even when payload media still exist. Kafka's specific failure is not a corrupted payload or an incorrect stored number but omission of a partition key from a full-map checkpoint rewrite. The analogy is functional only.

---

## Related-repository duplication check

A fresh repository search of `tmzncty/computing-archaeology` for `KAFKA-1647` returned no dedicated result. Accordingly this record contains only the retention-specific bounded mechanism and does not create a generic Kafka restart/checkpoint history.

If a later `computing-archaeology` case covers Kafka's distributed-log engineering history, link it here and trim any duplicated chronology.

---

## Follow-on deepening

- [`56-kafka-2014-kafka1647-high-watermark-checkpoint-loss-deepening.md`](56-kafka-2014-kafka1647-high-watermark-checkpoint-loss-deepening.md) closes the historical high-watermark checkpoint-membership failure slice. It traces the production-observed KAFKA-1647 scenario, the pre-fix missing local-replica object, the 30 October 2014 fix, the released 0.8.2.0 inclusion behavior, the zero-on-missing fallback, and the semantic distinction between replication and local-log recovery checkpoints.
- [`56-kafka-0110-leader-epoch-lineage-truncation-deepening.md`](56-kafka-0110-leader-epoch-lineage-truncation-deepening.md) closes the initial Kafka 0.11.0.0 leader-epoch follow-up. It separates the high-watermark committed/visibility frontier from retained leader-epoch lineage used for truncation, inspects the exact `leader-epoch-checkpoint` implementation and KIP-101 acceptance tests, preserves mixed-version high-watermark fallback as a distinct regime, and uses KIP-279 as later counterevidence against claiming that the initial KIP-101 protocol solved every divergence history.
- [`56-kafka-2000-kip279-largest-common-epoch-deepening.md`](56-kafka-2000-kip279-largest-common-epoch-deepening.md) closes the explicit post-0.11 KIP-279 follow-up. It grounds the observed KAFKA-6361 failure, Kafka 2.0 response-V1 `leader_epoch` provenance, iterative largest-common-epoch backtracking, compatibility/high-watermark fallbacks, the 2.0 unclean-election acceptance test, and the KIP's explicit compaction/reconstruction boundary for retained epoch history.

---

## Remaining gaps

- later change of `unclean.leader.election.enable` default (0.11.0.0 disabled it by default) as a policy-history case;
- KRaft metadata/leader epoch evolution;
- transactional high watermark versus last stable offset;
- independent failure injection reproducing a pre-fix KAFKA-1647 sequence and confirming fixed behavior;
- exact filesystem/device crash durability of `OffsetCheckpoint` temp-file + file-fsync + rename replacement;
- source-controlled ZooKeeper ISR/leader-state crash behavior if that becomes necessary for a later synthesis claim.

None of these gaps blocks `grounded` status for the bounded 0.8.2.0 mechanism or the separate 0.11 / 2.0 leader-epoch deepenings.
