# Apache Kafka 0.8.2 Replicated Log: High Watermark, ISR Currentness, and Failover Truncation

## Scope

- **Bounded system:** Apache Kafka 0.8.2.0, released 2 February 2015, with the versioned 0.8.2 design/configuration documentation and the exact `0.8.2.0` source tag as the principal artifacts.
- **Bounded mechanism:** partition leadership, assigned replicas versus the in-sync replica set (ISR), leader and follower log-end offsets, the high watermark, consumer exposure of committed data, periodic high-watermark checkpointing, ISR shrink/expansion, and follower truncation after an unclean election.
- **Research question:** when several physical logs survive, what retained control state determines which prefix counts as committed/current, and why can recovery deliberately discard a longer surviving suffix instead of treating it as more authoritative?

This is **not** a general history of Kafka replication, consensus, ZooKeeper, message durability, Raft/Paxos, producer semantics, or later leader-epoch recovery. Kafka replication first arrived in 0.8.0; this case uses 0.8.2.0 because its versioned documentation and source make the high-watermark/ISR mechanism and recovery behavior inspectable together.

This case also does not duplicate [Case 42](42-apache-kafka-log-compaction-delete-marker-retention.md). Case 42 asks how a committed keyed log can deliberately forget superseded history while keeping stable offsets and current-state reconstructability. Case 56 asks how replication decides which part of a physically surviving log is sufficiently replicated/current to be exposed and retained through failover.

The bounded retention claim is:

> **Kafka 0.8.2.0 does not equate physical record presence, a replica's log-end offset, or assigned replica membership with committed retained state. The leader advances a high watermark from the minimum log-end position of the current ISR; ordinary consumer reads are bounded by that watermark; ISR membership is itself retained coordination state; and a follower whose longer suffix conflicts with an uncleanly elected leader may be truncated to the leader's end offset. Persistence therefore depends on a protocol-defined committed prefix and current replica qualification, not on preserving every physically surviving suffix.**

`committed-prefix retention`, `replica currentness`, `admissible recovery suffix`, and `retained recovery boundary` below are **project engineering terms**, not historical Kafka vocabulary.

---

## Historical vocabulary

The inspected 0.8.2 artifacts use:

- `leader` and `follower`;
- `replication factor`;
- `replicas` / assigned replicas;
- `in sync` and `ISR`;
- `committed`;
- `high watermark` / `highwatermark`;
- `log end offset`;
- `leader epoch`;
- `unclean leader election`;
- `truncate` / `truncateTo`;
- `replication-offset-checkpoint`;
- `request.required.acks`;
- `min.insync.replicas`;
- `replica.high.watermark.checkpoint.interval.ms`.

Do not retroactively replace these bounded 0.8.2 terms with later Kafka concepts such as leader-epoch checkpoint recovery, transactional last-stable offset, KRaft metadata epochs, or modern follower-fetch semantics.

---

## Historical record

### H/P — replication is partition-scoped and leadership is temporary protocol authority

Kafka 0.8.2's design documentation says the unit of replication is a topic partition. Under non-failure conditions, a partition has one leader and zero or more followers; all reads and writes go through the leader in this bounded version. The leader tracks which followers remain `in sync`.

This establishes a distinction between **replica multiplicity** and **temporary command/read authority**. Several physical replicas may exist, but they are not symmetric answerers at one moment.

**Primary anchor:** Apache Kafka 0.8.2, `Design` → `Replication`.

### H/P — commitment is defined relative to the current ISR

The 0.8.2 design states that a message is considered `committed` when all in-sync replicas for the partition have applied it to their log. Only committed messages are given to ordinary consumers. It separately states that an ISR member is an assigned replica sufficiently alive/caught up to remain in the in-sync set.

Thus the bounded historical semantics already separate:

```text
record appended on leader
    ≠ record replicated to every assigned replica
    ≠ record committed relative to the current ISR
    ≠ record exposed to ordinary consumer read
```

**Primary anchor:** Apache Kafka 0.8.2 `Design` → `Replication`; 0.8.2 broker/topic configuration for lag and ISR controls.

### H/P — the leader computes the high watermark from ISR log-end positions

In tag `0.8.2.0`, `Partition.scala` maintains `inSyncReplicas`. Its `maybeIncrementLeaderHW` obtains all log-end offsets in the ISR and chooses their minimum as the candidate high watermark. The watermark only moves forward in that path.

When a follower fetch advances, `updateLeaderHWAndMaybeExpandIsr` can add it back to ISR only if it is assigned, not already in ISR, and its log end is at least the leader's high watermark. ISR changes are written to ZooKeeper by `updateIsr`.

This is direct implementation evidence that **the slowest/current ISR frontier, not the leader's own longest suffix, defines the committed boundary** in the bounded mechanism.

**Primary anchor:** `core/src/main/scala/kafka/cluster/Partition.scala`, tag `0.8.2.0`, especially `updateLeaderHWAndMaybeExpandIsr`, `maybeIncrementLeaderHW`, `maybeShrinkIsr`.

### H/P — ordinary consumer reads are bounded by the high watermark

In `ReplicaManager.scala`, `readMessageSet` distinguishes follower-replication fetches from ordinary consumer/debugging fetches. A broker follower can fetch beyond the leader high watermark so it can catch up. Ordinary clients instead receive a `maxOffset` equal to the local leader replica's high watermark, and `log.read` is bounded by it.

This implementation directly supports the design claim that uncommitted tail records can physically exist in a leader log without being exposed as committed consumer data.

**Primary anchor:** `core/src/main/scala/kafka/server/ReplicaManager.scala`, tag `0.8.2.0`, `readMessageSet`.

### H/P — follower high watermark is separately constrained by its own log end and the leader's watermark

`ReplicaFetcherThread.scala` appends records fetched from the leader and then sets the follower high watermark to:

```text
min(follower log end offset, leader-reported high watermark)
```

The follower can therefore have a physical log tail that is longer than the prefix it currently treats as committed.

**Primary anchor:** `core/src/main/scala/kafka/server/ReplicaFetcherThread.scala`, tag `0.8.2.0`, `processPartitionData`.

### H/P — the high watermark is periodically persisted for recovery

The official 0.8.2 broker configuration documents `replica.high.watermark.checkpoint.interval.ms` (default 5000 ms) as the frequency with which each replica saves its high watermark to disk `to handle recovery`.

The source makes the embodiment explicit. `ReplicaManager` names the file `replication-offset-checkpoint`, creates one `OffsetCheckpoint` per log directory, and schedules `checkpointHighWatermarks` at the configured interval. `Partition.getOrCreateReplica` reads the checkpoint at startup and clamps a recovered checkpoint value to the local log end.

The checkpoint is therefore **retained recovery/control state**, not user payload and not a complete history of replication events.

**Primary anchors:** Apache Kafka 0.8.2 `Broker Configs`; `ReplicaManager.scala`; `Partition.scala`, tag `0.8.2.0`.

### H/P — assigned replicas, ISR membership, and producer acknowledgement policy are distinct controls

The 0.8.2 configuration documents `min.insync.replicas`. With `request.required.acks=-1`, a produce request succeeds only under the documented minimum-ISR condition. The source's `checkEnoughReplicasReachOffset` checks the required offset against the high watermark for the `requiredAcks < 0` path and separately checks current ISR size against the configured minimum.

Consequently, a topic may have a replication factor of three while only two replicas are currently in ISR, and the configured minimum can decide whether the system continues accepting writes. `replication factor`, `ISR size`, `acks`, and `committed frontier` are related but non-identical state/policy relations.

**Primary anchors:** Apache Kafka 0.8.2 `Broker Configs`; `Partition.scala` tag `0.8.2.0`.

### H/P — 0.8.2 allows unclean election and documents the durability trade-off

The 0.8.2 broker configuration has `unclean.leader.election.enable=true` by default and describes it as permitting a non-ISR replica to become leader as a last resort even though this may cause data loss. The versioned design explains the underlying trade-off: waiting for an ISR member preserves the normal committed-message guarantee but can sacrifice availability; choosing an out-of-sync replica restores availability by making a potentially incomplete log the new source of truth.

Later Kafka changed this default, so the 0.8.2 default must not be projected onto modern deployments.

**Primary anchors:** Apache Kafka 0.8.2 `Broker Configs`; 0.8.2 `Design` → `Unclean leader election`.

### H/P — recovery can deliberately truncate a longer surviving log

`ReplicaFetcherThread.handleOffsetOutOfRange` documents an unclean-election scenario in code comments: an old leader can return after an out-of-sync follower was elected and began accepting new writes. If the current leader's end offset is behind the returning follower's end offset, the returning replica truncates its local log to the current leader's end offset and continues fetching.

The source also contains a safety check: if unclean leader election is no longer allowed for that topic, the broker halts instead of unexpectedly performing this data-losing truncation.

This is direct period implementation evidence for the counterintuitive relation:

> **a physically longer surviving log is not automatically the more authoritative retained state.**

**Primary anchor:** `core/src/main/scala/kafka/server/ReplicaFetcherThread.scala`, tag `0.8.2.0`, `handleOffsetOutOfRange`.

---

## Retained state

The bounded replicated-log mechanism retains several different things.

### 1. Partition payload/log records

Each replica physically retains a local ordered log with offsets.

### 2. Assigned-replica relation

The replication factor / assignment says which brokers are supposed to host the partition. This does not prove that every assigned replica is currently caught up.

### 3. ISR membership

The ISR is a changing currentness/admissibility set. It tells the replication protocol which replicas are sufficiently caught up to participate in the bounded commitment/election guarantee.

### 4. Per-replica log-end offsets

The leader tracks remote replica progress. These progress positions are inputs to the high-watermark calculation.

### 5. High watermark

The high watermark is a prefix boundary: ordinary consumer exposure stops there even if more bytes/records exist in the local log tail.

### 6. High-watermark checkpoint

`replication-offset-checkpoint` stores recovery/control state across broker restart. It is a compact retained boundary, not a record-by-record replication history.

### 7. Leader / controller / leader-epoch state

The implementation stores leadership and epoch relations used to reject stale leadership/controller actions. These are adjacent authority state, not the same state as the payload high watermark.

---

## Retention mechanism

A simplified healthy path is:

```text
leader LEO = 105
follower A LEO = 105
follower B LEO = 101
ISR = {leader, A, B}

minimum ISR LEO = 101
    -> leader high watermark can advance to 101
    -> ordinary consumers can read only through committed prefix
    -> records 101..104 may physically exist on leader/A
       while remaining outside consumer-visible committed state

B catches up
    -> B LEO advances
    -> minimum ISR frontier advances
    -> high watermark advances
```

A bounded unclean-recovery path is:

```text
old leader has a longer tail
    -> old ISR becomes unavailable
    -> non-ISR replica is uncleanly elected
    -> its shorter log becomes current leader log
    -> old leader later rejoins as follower
    -> old leader end offset > current leader end offset
    -> returning follower truncates its longer local suffix
    -> replication resumes from current leader
```

The second path is intentional protocol convergence under an explicitly weaker durability regime, not ordinary bit-corruption repair.

---

## Read, write, and recovery semantics

### Write/append

A leader can append a record before every in-sync follower has reached it. Physical append therefore precedes the stronger committed-prefix relation.

### Replication read

Follower fetch is allowed to retrieve the leader's uncommitted tail because copying that tail is precisely how the follower helps advance the high watermark.

### Ordinary consumer read

In the bounded 0.8.2 source, ordinary reads are capped at the high watermark. Successful bytes on disk beyond the boundary are not ordinary committed output.

### ISR transition

Slow/stuck followers can be removed from ISR. A follower can rejoin only after its log end has reached at least the leader high watermark and it satisfies the other assignment/membership conditions.

### Failover / truncation

A longer but no-longer-authoritative follower suffix can be discarded so that its log converges to the currently elected leader. Under unclean election this may sacrifice data that physically survived on the returning replica.

---

## Engineering reconstruction

### E — physical record presence ≠ committed retention

A record can physically exist in one or more local logs while lying above the high watermark. In this bounded protocol it has not yet acquired the same retention guarantee as the committed prefix.

### E — leader log end ≠ committed frontier

The leader can be ahead of followers. Its longest current suffix is an append frontier, not automatically the consumer-visible retention frontier.

### E — replication factor ≠ current redundancy margin

Assignment describes intended replica multiplicity. ISR membership describes the currently qualified set. A three-replica partition with one ISR member has a very different current failure margin from a three-replica partition with all three in sync.

### E — replica membership ≠ replica currentness

An assigned replica may still hold substantial data yet be outside ISR because it is too far behind/stuck. Physical participation in the replica set does not by itself grant currentness/election qualification under the normal guarantee.

### E — retained protocol metadata can define which surviving bytes count

ISR state, per-replica progress, high watermark, and leadership state are not application records, but losing or misinterpreting them changes which physical log suffix may be exposed, elected, or discarded. They are retention infrastructure.

### E — high-watermark persistence ≠ complete replication-history retention

The checkpoint stores a compact recovery boundary. It does not preserve a historical event log of every follower lag transition, every ISR calculation, or every replication fetch that produced that boundary.

### E — longer surviving suffix ≠ greater authority

The unclean-election recovery code provides a particularly strong counterexample to naive material maximalism. More surviving bytes can be deliberately discarded when protocol authority has moved to a shorter log.

### E — failover convergence can require forgetting

Recovery is not always `find the copy with the most data and keep it`. Under the bounded unclean path, convergence requires erasing/truncating a physically extant suffix so replicas again share one current history.

### E — committed-prefix continuity ≠ preservation of every acknowledged-looking local append

An append can be locally successful before it is part of the high-watermark prefix. The protocol therefore distinguishes the event `this broker stored these bytes` from the stronger relation `this replicated partition now treats them as committed`.

### E — availability policy can change the retention guarantee

With unclean election enabled, the system can choose a currently available out-of-sync copy and thereby trade the normal committed-message guarantee for service restoration. Availability is not simply orthogonal to retention; policy can authorize a new history boundary that abandons some formerly surviving state.

---

## Functional analogies and limits

### A — Kafka high watermark versus GFS master checkpoint (Case 46)

Both retain compact recovery-related state, but they solve different problems. GFS checkpoint + operation log reconstructs master namespace/mapping state; Kafka high watermark qualifies a replicated log prefix for consumer exposure/recovery. `checkpoint` similarity is not mechanism identity.

### A — Kafka ISR/currentness versus RADOS peering/currentness (Case 05)

Both demonstrate that replica multiplicity is weaker than replica admissibility/currentness. RADOS uses PG/version/peering relations in an object store; Kafka 0.8.2 uses leader/ISR/progress/high-watermark relations in a partition log. This is a functional comparison only.

### A — Kafka truncation versus HDFS generation-stamp recovery (Case 49)

Both reject `more surviving bytes = more authoritative state`. HDFS lease recovery can converge replicas to a common block length under generation-stamp rules; Kafka can truncate a follower suffix to the current leader log. Their authority, write, and recovery protocols are historically and technically distinct.

### A — Kafka replication forgetting versus Kafka compaction forgetting (Case 42)

These two Kafka mechanisms should not be collapsed merely because both remove records:

- Case 42 compaction forgets **superseded committed keyed history** while preserving latest keyed state and stable logical offsets.
- Case 56 failover truncation can forget a **non-authoritative/divergent suffix** to restore replica convergence.

`history no longer retained` therefore has different preconditions and purposes even inside one software family.

---

## Prior-art boundary

Kafka did not invent replicated logs, primary/backup replication, quorums, commit frontiers, or failure recovery.

The 0.8.2 design itself explicitly situates Kafka among replicated-log/state-machine work and names ZooKeeper's Zab, Raft, Viewstamped Replication, and Microsoft Research's PacificA as related work. It says the most similar academic publication known to the Kafka authors was **PacificA: Replication in Log-Based Distributed Storage Systems** (Microsoft Research technical report MSR-TR-2008-25, February 2008).

The bounded historical claim is therefore narrower:

> **By Kafka 0.8.2.0, Apache had an inspectable production design in which ISR membership, per-replica log-end progress, a high-watermark committed prefix, checkpointed recovery state, and optional unclean-election truncation jointly determined what a surviving replicated partition treated as current/committed.**

No novelty claim is made for the underlying class of replication algorithm.

---

## Philosophical interpretation — bounded

### I — retention is not maximization of surviving traces

Case 47 already showed that old Flash traces can survive after logical deletion. Case 56 adds the converse distributed problem: **survival can be too much**. A physically longer log may be the wrong future because its suffix no longer belongs to the protocol-authorized history.

This makes `retention` inseparable from a rule of admissibility when several embodiments diverge. The system does not merely ask what survived; it asks what survived **within the currently authorized continuity relation**.

### I — technical forgetting can constitute continuity

Truncation sounds like loss, yet in this recovery path it is the operation that lets a returning replica become part of one current log again. Forgetting a divergent suffix can therefore be constitutive of continued logical identity.

Do not generalize this into a metaphysical claim that all identity requires erasure. The point is bounded: Kafka's replicated-log identity can require selective protocol-authorized forgetting during recovery.

---

## Counterexamples and limits

This case does **not** establish that:

- any Kafka version uses exactly the 0.8.2 ISR/high-watermark implementation;
- the high watermark is identical to the later transactional `last stable offset`;
- high-watermark checkpointing preserves the latest in-memory watermark at every instant;
- `request.required.acks=-1` means every assigned replica rather than all current ISR members;
- replication factor alone expresses current durability;
- unclean election is always enabled (it was default-true in the bounded 0.8.2 documentation; later defaults differ);
- a longer log is always wrong after failover;
- normal clean leader election requires the same data-losing truncation scenario described in `handleOffsetOutOfRange`;
- 0.8.2's offset-based recovery solves all divergent-log cases. Later Kafka introduced stronger leader-epoch-based recovery machinery; that deserves a separate case.

---

## Claim ledger

| Claim | Type | Status |
| --- | --- | --- |
| Kafka 0.8.2 partition replication has one leader and an ISR | H/P | established |
| commit is defined against the current ISR | H/P | established |
| leader high watermark advances from the minimum ISR log-end frontier | H/P/E | established in 0.8.2.0 source |
| ordinary consumer reads are capped at the high watermark | H/P | established in 0.8.2.0 source |
| follower high watermark is bounded by both follower LEO and leader HW | H/P | established in 0.8.2.0 source |
| high watermark is periodically checkpointed to `replication-offset-checkpoint` | H/P | established |
| ISR membership can shrink/expand with follower progress | H/P | established |
| replication factor ≠ ISR size/current redundancy margin | E | supported |
| physical record presence ≠ committed retention | E | supported |
| leader LEO ≠ committed frontier | E | supported |
| longer surviving suffix ≠ automatically authoritative suffix | H/P/E | established by bounded unclean-recovery path |
| recovery convergence can require truncating extant records | H/P/E | established in bounded path |
| high-watermark checkpoint ≠ complete replication history | E | supported |
| Kafka invented replicated logs/quorums | X | rejected |
| 0.8.2 semantics can be projected onto current Kafka | X | rejected |

---

## Sources

### Primary / period Apache material

1. Apache Kafka, **0.8.2 Design — Replication**: <https://kafka.apache.org/082/design/design/>.
2. Apache Kafka, **0.8.2 Broker Configs**: <https://kafka.apache.org/082/configuration/broker-configs/>.
3. Apache Kafka, **0.8.2 Downloads / release record**, 0.8.2.0 released 2 February 2015: <https://kafka.apache.org/community/downloads/>.
4. Apache Kafka source tag `0.8.2.0`, `Partition.scala`: <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/cluster/Partition.scala>.
5. Apache Kafka source tag `0.8.2.0`, `ReplicaManager.scala`: <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/server/ReplicaManager.scala>.
6. Apache Kafka source tag `0.8.2.0`, `ReplicaFetcherThread.scala`: <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/server/ReplicaFetcherThread.scala>.
7. Apache Kafka 0.8.0 release notes, including KAFKA-50 intra-cluster replication: <https://archive.apache.org/dist/kafka/0.8.0/RELEASE_NOTES.html>.

### Prior art / qualification

8. Wei Lin, Mao Yang, Lintao Zhang, Lidong Zhou, **PacificA: Replication in Log-Based Distributed Storage Systems**, Microsoft Research, MSR-TR-2008-25, February 2008: <https://www.microsoft.com/en-us/research/publication/pacifica-replication-in-log-based-distributed-storage-systems/>.

---

## Related repositories

Searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated Kafka replication/high-watermark case at the time of this slice. No generic Kafka history is duplicated here. If that repository later develops a log-replication engineering history, this case should link to it and keep only the retention-specific comparison.

Methodological anti-anachronism follows [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history): later words such as `committed-prefix retention` are project reconstructions, not claims about Apache's own 2015 conceptual vocabulary.

---

## Status

**`grounded`** for the bounded Apache Kafka 0.8.2.0 ISR/high-watermark/consumer-visibility/checkpoint/unclean-truncation mechanism.

Open follow-ups remain intentionally separate:

- Kafka 0.11+ leader-epoch checkpoint recovery and divergent-log truncation;
- later change of the unclean-election default and durability policy history;
- modern KRaft leader/metadata recovery;
- transactional `last stable offset` versus replication high watermark;
- independent fault-injection against a named Kafka release;
- filesystem/device durability composition below Kafka's log.
