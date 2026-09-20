# Apache Kafka 0.8.2 Replicated Log: High Watermark, ISR Currentness, and Failover Truncation

## Scope

- **Bounded system:** Apache Kafka 0.8.2.0, released 2 February 2015, with the versioned 0.8.2 design/configuration documentation and the exact `0.8.2.0` source tag as the principal artifacts.
- **Bounded mechanism:** partition leadership, assigned replicas versus the in-sync replica set (ISR), leader and follower log-end offsets, the high watermark, consumer exposure of committed data, periodic high-watermark checkpointing, checkpoint coverage across restart, ISR shrink/expansion, and follower truncation after an unclean election.
- **Research question:** when several physical logs survive, what retained control state determines which prefix counts as committed/current, what has to survive for that boundary to remain recoverable after broker restart, and why can recovery deliberately discard a longer surviving suffix instead of treating it as more authoritative?

This is **not** a general history of Kafka replication, consensus, ZooKeeper, message durability, Raft/Paxos, producer semantics, or later leader-epoch recovery. Kafka replication first arrived in 0.8.0; this case uses 0.8.2.0 because its versioned documentation and source make the high-watermark/ISR mechanism and recovery behavior inspectable together.

This case also does not duplicate [Case 42](42-apache-kafka-log-compaction-delete-marker-retention.md). Case 42 asks how a committed keyed log can deliberately forget superseded history while keeping stable offsets and current-state reconstructability. Case 56 asks how replication decides which part of a physically surviving log is sufficiently replicated/current to be exposed and retained through failover.

The bounded retention claim is:

> **Kafka 0.8.2.0 does not equate physical record presence, a replica's log-end offset, or assigned replica membership with committed retained state. The leader advances a high watermark from the minimum log-end position of the current ISR; ordinary consumer reads are bounded by that watermark; ISR membership is itself retained coordination state; a compact high-watermark checkpoint carries a recovery boundary across restart; and a follower whose longer suffix conflicts with an uncleanly elected leader may be truncated to the leader's end offset. KAFKA-1647 further shows that preserving the checkpoint file is insufficient if a still-relevant partition is omitted from the next checkpoint image. Persistence therefore depends on protocol-defined currentness and complete recovery relations, not on preserving every physically surviving suffix or merely preserving a file container.**

`committed-prefix retention`, `replica currentness`, `admissible recovery suffix`, `retained recovery boundary`, and `checkpoint coverage` below are **project engineering terms**, not historical Kafka vocabulary.

---

## Evidence navigation

- Base grounding: [`evidence/56-kafka-082-replication-high-watermark-grounding.md`](../evidence/56-kafka-082-replication-high-watermark-grounding.md).
- Checkpoint/restart deepening: [`evidence/56-kafka-082-high-watermark-checkpoint-coverage-deepening.md`](../evidence/56-kafka-082-high-watermark-checkpoint-coverage-deepening.md).

The second packet uses the 0.8.2.0 source, Apache KAFKA-1647, and its fixing commit to separate live high watermark, persisted checkpoint, checkpoint-file integrity, checkpoint coverage/completeness, and post-restart runtime initialization.

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

**Primary anchors:** Apache Kafka 0.8.2 `Broker Configs`; `KafkaConfig.scala`; `ReplicaManager.scala`; `Partition.scala`, tag `0.8.2.0`.

### H/P — checkpoint replacement has file-level discipline but depends on runtime enumeration

`OffsetCheckpoint.scala` writes a new map to a temporary file, flushes it, calls `FileDescriptor.sync()`, closes it, and then replaces the previous checkpoint using `renameTo` with a platform fallback. Its reader validates a format version and declared entry count.

But `ReplicaManager.checkpointHighWatermarks()` first constructs that map from the broker's current local `Replica` objects. It does not independently scan every log directory and infer which partitions ought to be represented.

Therefore two different correctness questions exist:

```text
is the checkpoint file structurally writable/readable?
    !=
does the checkpoint map include every still-relevant partition?
```

**Primary anchors:** `OffsetCheckpoint.scala`; `ReplicaManager.scala`, tag `0.8.2.0`.

### H/P — clean shutdown explicitly checkpoints high watermarks

`ReplicaManager.shutdown()` shuts down replica fetching and calls `checkpointHighWatermarks()` before reporting shutdown complete. This is a clean-lifecycle handoff path distinct from the periodic checkpoint scheduler.

It does not prove that abrupt process or machine loss reaches that path, nor does it establish lower-filesystem power-loss guarantees.

**Primary anchor:** `ReplicaManager.scala`, tag `0.8.2.0`, `shutdown`.

### H/P — restart uses the checkpoint as bounded recovery input rather than an unconstrained truth

`Partition.getOrCreateReplica()` reads the per-directory checkpoint when constructing a local replica. If the topic/partition entry is absent it warns and falls back to zero; if present, the restored high watermark is clamped to the local log end.

Thus:

```text
persisted checkpoint value
    != unconstrained authority beyond local LEO

missing checkpoint entry
    != missing local payload bytes
```

**Primary anchor:** `Partition.scala`, tag `0.8.2.0`, `getOrCreateReplica`.

### H/P — KAFKA-1647 exposed checkpoint coverage loss across hard-kill/restart sequencing

Apache KAFKA-1647, created 23 September 2014 and resolved 30 October 2014, is titled **“Replication offset checkpoints (high water marks) can be lost on hard kills and restarts.”** It is marked `Critical`, with both affected and fix version 0.8.2.0.

The production-reported scenario is specific. After enough brokers are hard-killed, a restarting broker can receive a `LeaderAndIsrRequest` for a partition whose designated leader is still unavailable. In the pre-fix path, the broker aborts the become-follower transition before creating the local replica object. The later checkpoint pass enumerates only existing local replica objects, so that partition is omitted from the new checkpoint map and its previously stored high-watermark entry can disappear when the file is rewritten.

This is not merely stale periodic persistence. It is **loss of checkpoint coverage**.

**Primary anchors:** Apache KAFKA-1647; fixing commit `1ed9cf6d03603518d950f7e9a5f122c4ed5d7cee`.

### H/P — the defect could leave payload present while the recovery boundary fell back toward zero

KAFKA-1647 reports that a broker which loses the high-watermark entry can later truncate to zero and refetch from the beginning, producing high I/O. It also reports an offsets-topic consequence because offset loading does not read past the high watermark. The issue says the reporters observed those latter two symptom classes; it additionally describes a possible data-loss path under the hard-kill/re-election sequence.

This directly grounds:

```text
log bytes survive
    != high-watermark recovery evidence survives
```

and shows why the checkpoint is active retention infrastructure rather than passive telemetry.

**Primary anchor:** KAFKA-1647 description and symptom list.

### H/P — the fix preserves checkpoint coverage even when ordinary follower transition cannot complete

Commit `1ed9cf6d03603518d950f7e9a5f122c4ed5d7cee` changes the unavailable-leader branch so that Kafka still calls `partition.getOrCreateReplica()`. The code comment states that creating the local replica is required so the partition's high watermark is included in the checkpoint file.

The released `0.8.2.0` tag contains that rationale and behavior.

This gives a precise bounded distinction:

```text
local replica object exists for checkpoint coverage
    != follower transition completed
    != designated leader reachable
```

**Primary anchors:** fixing commit; released `ReplicaManager.scala` tag `0.8.2.0`.

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

### 7. Checkpoint coverage relation

The durable file must not merely survive; it must contain entries for the local partitions whose recovery boundaries remain relevant. KAFKA-1647 shows that this representation relation can fail independently of ordinary file-format validity.

### 8. Leader / controller / leader-epoch state

The implementation stores leadership and epoch relations used to reject stale leadership/controller actions. These are adjacent authority state, not the same state as the payload high watermark. The later leader-epoch checkpoint introduced in newer Kafka releases is a separate mechanism handled in Case 90.

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
    -> periodic checkpoint later serializes the current HW boundary
```

A bounded checkpoint-coverage failure path is:

```text
partition log + prior HW checkpoint exist
    -> brokers are hard-killed/restarted in KAFKA-1647 sequence
    -> designated leader for one partition is unavailable
    -> pre-fix broker aborts follower transition
       before creating local Replica object
    -> checkpoint enumerator sees no local Replica for that partition
    -> next checkpoint image omits partition entry
    -> previous recovery boundary is replaced by an incomplete map
    -> restart initialization can fall back to HW = 0
       even though partition log bytes remain
```

The 0.8.2.0 fix creates the local replica object even when the leader is unavailable so the partition remains represented in subsequent checkpoint output.

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

The final path is intentional protocol convergence under an explicitly weaker durability regime, not ordinary bit-corruption repair.

---

## Read, write, checkpoint, and recovery semantics

### Write/append

A leader can append a record before every in-sync follower has reached it. Physical append therefore precedes the stronger committed-prefix relation.

### Replication read

Follower fetch is allowed to retrieve the leader's uncommitted tail because copying that tail is precisely how the follower helps advance the high watermark.

### Ordinary consumer read

In the bounded 0.8.2 source, ordinary reads are capped at the high watermark. Successful bytes on disk beyond the boundary are not ordinary committed output.

### ISR transition

Slow/stuck followers can be removed from ISR. A follower can rejoin only after its log end has reached at least the leader high watermark and it satisfies the other assignment/membership conditions.

### Checkpoint

The live watermark is periodically materialized as a compact topic/partition → offset map. Clean shutdown performs an additional checkpoint. The map is built from runtime local replica objects, so **membership in the serialization source** is itself a precondition for preserving the durable boundary.

### Restart initialization

A local replica reads its checkpoint entry and clamps that value to local log end. A missing entry falls back to zero. The durable checkpoint is therefore recovery evidence, not the complete pre-crash runtime state and not independent of the surviving log.

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

### E — live high watermark ≠ most recent durable checkpoint

The default 5000 ms periodic interval means a live high watermark can advance after the latest checkpoint. A clean shutdown explicitly checkpoints again, but an abrupt hard kill cannot be assumed to execute that closure path.

Thus ordinary checkpoint staleness is an expected consequence of periodic materialization and must be distinguished from the separate KAFKA-1647 omission defect.

### E — checkpoint file integrity ≠ checkpoint semantic completeness

`OffsetCheckpoint` can produce a parseable, internally count-consistent file while the runtime enumeration feeding it omits a still-relevant partition. KAFKA-1647 is a direct bounded counterexample to treating structural validity as sufficient recovery correctness.

```text
valid checkpoint syntax
    ≠ complete checkpoint membership
```

### E — replacement discipline ≠ correct snapshot membership

Writing a temporary file, syncing it, and replacing the previous image can reduce some classes of partial-file failure while still committing an incomplete set of entries.

Even an idealized perfectly atomic replace would not cure the KAFKA-1647 bug, because the new logical image itself is missing state.

This does not claim universal crash atomicity for Java `renameTo` or the 0.8.2 filesystem path.

### E — runtime object reachability can be retention infrastructure

The local `Replica` object is volatile runtime state, yet `checkpointHighWatermarks()` uses those objects as the enumeration source for durable recovery metadata. The KAFKA-1647 fix creates the object even when normal follower transition cannot complete precisely to preserve future checkpoint inclusion.

A bounded chain is therefore:

```text
runtime Replica exists
    -> partition included in next checkpoint image
    -> high-watermark boundary survives checkpoint replacement
    -> restart can recover that boundary
```

The runtime object need not itself survive the restart to participate in preserving durable state.

### E — missing checkpoint entry ≠ missing payload

`Partition.getOrCreateReplica()` falls back to high watermark zero when the entry is absent even though the local log may contain records. This is a sharp example of **payload survival without recovery-boundary survival**.

### E — retained recovery metadata can authorize later destructive action

KAFKA-1647's symptom path shows that losing the high-watermark entry can cause later truncation to zero and refetch. The checkpoint is not merely diagnostic history: its presence or absence changes what recovery can treat as safely retained.

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

### A — Kafka high-watermark checkpoint versus GFS master checkpoint (Case 46)

Both retain compact recovery-related state, but they solve different problems. GFS checkpoint + operation log reconstructs master namespace/mapping state; Kafka high watermark qualifies a replicated log prefix for consumer exposure/recovery.

KAFKA-1647 adds one bounded common question without making the mechanisms identical: a checkpoint's usefulness depends on **semantic coverage**, not just file existence. GFS and Kafka encode different state classes and use different recovery procedures.

### A — Kafka checkpoint versus FTL recovery checkpoint (Case 04)

Both distinguish live runtime state from durable recovery evidence. But DCR-style FTL recovery can combine a checkpoint with post-checkpoint physical media evidence to reconstruct mapping, whereas Kafka 0.8.2's high-watermark checkpoint is a compact replicated-log currentness boundary, not an FTL map and not a replay log of every HW transition.

The controlled comparison is only:

```text
last durable recovery evidence
    ≠ complete runtime state immediately before crash
```

### A — Kafka ISR/currentness versus RADOS peering/currentness (Case 05)

Both demonstrate that replica multiplicity is weaker than replica admissibility/currentness. RADOS uses PG/version/peering relations in an object store; Kafka 0.8.2 uses leader/ISR/progress/high-watermark relations in a partition log. This is a functional comparison only.

### A — Kafka truncation versus HDFS generation-stamp recovery (Case 49)

Both reject `more surviving bytes = more authoritative state`. HDFS lease recovery can converge replicas to a common block length under generation-stamp rules; Kafka can truncate a follower suffix to the current leader log. Their authority, write, and recovery protocols are historically and technically distinct.

### A — Kafka replication forgetting versus Kafka compaction forgetting (Case 42)

These two Kafka mechanisms should not be collapsed merely because both remove records:

- Case 42 compaction forgets **superseded committed keyed history** while preserving latest keyed state and stable logical offsets.
- Case 56 failover truncation can forget a **non-authoritative/divergent suffix** to restore replica convergence.
- KAFKA-1647 adds a third, different failure: a **recovery relation can be forgotten by omission from a rewritten checkpoint image**.

`history/state no longer retained` therefore has different preconditions and purposes even inside one software family.

### A — Kafka 0.8.2 high-watermark checkpoint versus Kafka 0.11 leader-epoch checkpoint (Case 90)

Both are retained recovery metadata in a replicated log, but they are not the same state. The 0.8.2 file stores high-watermark boundaries; later leader-epoch checkpoints retain lineage boundaries used to qualify divergent-log recovery. Case 90 must not be projected backward into KAFKA-1647.

---

## Prior-art boundary

Kafka did not invent replicated logs, primary/backup replication, quorums, commit frontiers, checkpointing, or failure recovery.

The 0.8.2 design itself explicitly situates Kafka among replicated-log/state-machine work and names ZooKeeper's Zab, Raft, Viewstamped Replication, and Microsoft Research's PacificA as related work. It says the most similar academic publication known to the Kafka authors was **PacificA: Replication in Log-Based Distributed Storage Systems** (Microsoft Research technical report MSR-TR-2008-25, February 2008).

The bounded historical claim is therefore narrower:

> **By Kafka 0.8.2.0, Apache had an inspectable production design in which ISR membership, per-replica log-end progress, a high-watermark committed prefix, checkpointed recovery state, and optional unclean-election truncation jointly determined what a surviving replicated partition treated as current/committed; KAFKA-1647 additionally documents a production-discovered checkpoint-coverage failure and a source-level fix that preserves the local replica object needed to keep a partition's recovery boundary in the durable checkpoint.**

No novelty claim is made for the underlying class of replication or checkpoint algorithm.

---

## Philosophical interpretation — bounded

### I — retention is not maximization of surviving traces

Case 47 already showed that old Flash traces can survive after logical deletion. Case 56 adds the converse distributed problem: **survival can be too much**. A physically longer log may be the wrong future because its suffix no longer belongs to the protocol-authorized history.

This makes `retention` inseparable from a rule of admissibility when several embodiments diverge. The system does not merely ask what survived; it asks what survived **within the currently authorized continuity relation**.

### I — persistence of a container ≠ persistence of every relation it represented

KAFKA-1647 adds another failure mode. A checkpoint file can exist, be parseable, and have been freshly written while a partition's prior recovery boundary has vanished because the new image omitted it.

The downstream distinction is:

```text
artifact survives
    ≠ represented relation survives
```

Apache did not formulate the bug in these philosophical terms.

### I — forgetting can occur through omission during successful rewriting

The KAFKA-1647 entry loss does not require media decay or an explicit delete of the partition checkpoint. The relation disappears because it is omitted from the next authoritative image.

This supports a bounded project interpretation: **technical forgetting can occur by omission during representation renewal.** It should not be generalized to all checkpoint systems.

### I — technical forgetting can also constitute continuity

Truncation sounds like loss, yet in the unclean-recovery path it is the operation that lets a returning replica become part of one current log again. Forgetting a divergent suffix can therefore be constitutive of continued logical identity.

Do not conflate this intentional convergence with the accidental KAFKA-1647 checkpoint omission. One is protocol-authorized forgetting of a divergent suffix; the other is a bug that loses recovery knowledge.

---

## Counterexamples and limits

This case does **not** establish that:

- any Kafka version uses exactly the 0.8.2 ISR/high-watermark implementation;
- the high watermark is identical to the later transactional `last stable offset`;
- high-watermark checkpointing preserves the latest in-memory watermark at every instant;
- the default 5000 ms checkpoint interval is a durability SLA or a direct bound on message loss;
- a structurally valid checkpoint necessarily contains every semantically required partition entry;
- `FileDescriptor.sync()` of the temporary checkpoint file proves parent-directory durability;
- Java `renameTo` is crash-atomic on every filesystem/platform;
- KAFKA-1647 was a failed `fsync`/rename bug rather than a checkpoint-enumeration bug;
- KAFKA-1647 occurs on every hard kill or every restart;
- every missing high-watermark entry implies application payload loss;
- the issue reporters directly observed the listed data-loss path; the issue says they observed the high-I/O and offsets-reset symptom classes;
- creating a local replica object in the fix means the follower transition has completed or its leader is reachable;
- `request.required.acks=-1` means every assigned replica rather than all current ISR members;
- replication factor alone expresses current durability;
- unclean election is always enabled (it was default-true in the bounded 0.8.2 documentation; later defaults differ);
- a longer log is always wrong after failover;
- normal clean leader election requires the same data-losing truncation scenario described in `handleOffsetOutOfRange`;
- 0.8.2's offset-based recovery solves all divergent-log cases. Later Kafka introduced stronger leader-epoch-based recovery machinery; that is Case 90;
- high-watermark checkpointing proves payload data has been flushed through the filesystem/device stack;
- the KAFKA-1647 fix proves all later Kafka checkpoint/restart defects were eliminated.

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
| default high-watermark checkpoint interval is 5000 ms | H/P | established in 0.8.2.0 source |
| clean shutdown explicitly checkpoints high watermarks | H/P | established in source |
| checkpoint map is assembled from current local replica objects | H/P | established in source |
| checkpoint writer uses temp-file write + flush + file sync + replacement | H/P | established in source |
| local replica initialization reads checkpoint, defaults missing entry to zero, and clamps present value to local LEO | H/P | established in source |
| KAFKA-1647 documents partition checkpoint loss in a hard-kill/restart sequence | H/P | established by Apache issue record |
| KAFKA-1647 fix creates a local replica despite unavailable leader so its HW remains checkpointed | H/P | established by fixing commit and released source |
| file integrity ≠ checkpoint semantic completeness | H/P/E | established by bounded defect mechanism |
| periodic checkpoint staleness ≠ checkpoint-entry omission | E | supported |
| runtime replica-object reachability can participate in durable-state production | E | supported by checkpoint enumeration + fix |
| missing checkpoint entry ≠ missing local payload bytes | H/P/E | established by restart path + issue scenario |
| ISR membership can shrink/expand with follower progress | H/P | established |
| replication factor ≠ ISR size/current redundancy margin | E | supported |
| physical record presence ≠ committed retention | E | supported |
| leader LEO ≠ committed frontier | E | supported |
| longer surviving suffix ≠ automatically authoritative suffix | H/P/E | established by bounded unclean-recovery path |
| recovery convergence can require truncating extant records | H/P/E | established in bounded path |
| high-watermark checkpoint ≠ complete replication history | E | supported |
| checkpoint file existence alone guarantees recovery-boundary preservation | X | rejected by KAFKA-1647 |
| Kafka invented replicated logs/quorums/checkpoint recovery | X | rejected |
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
7. Apache Kafka source tag `0.8.2.0`, `KafkaConfig.scala`: <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/server/KafkaConfig.scala>.
8. Apache Kafka source tag `0.8.2.0`, `OffsetCheckpoint.scala`: <https://github.com/apache/kafka/blob/0.8.2.0/core/src/main/scala/kafka/server/OffsetCheckpoint.scala>.
9. Apache JIRA, **KAFKA-1647 — Replication offset checkpoints (high water marks) can be lost on hard kills and restarts**, created 23 September 2014, resolved 30 October 2014: <https://issues.apache.org/jira/browse/KAFKA-1647>.
10. Apache Kafka commit `1ed9cf6d03603518d950f7e9a5f122c4ed5d7cee`, **KAFKA-1647; Create replicas on follower transition even if leader is unavailable...**, 30 October 2014: <https://github.com/apache/kafka/commit/1ed9cf6d03603518d950f7e9a5f122c4ed5d7cee>.
11. Apache Kafka 0.8.0 release notes, including KAFKA-50 intra-cluster replication: <https://archive.apache.org/dist/kafka/0.8.0/RELEASE_NOTES.html>.

### Prior art / qualification

12. Wei Lin, Mao Yang, Lintao Zhang, Lidong Zhou, **PacificA: Replication in Log-Based Distributed Storage Systems**, Microsoft Research, MSR-TR-2008-25, February 2008: <https://www.microsoft.com/en-us/research/publication/pacifica-replication-in-log-based-distributed-storage-systems/>.

---

## Related repositories

Searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Kafka high watermark` and `replication-offset-checkpoint` found no dedicated Kafka replication/high-watermark packet at the time of this deepening. No generic Kafka history is duplicated here. If that repository later develops a log-replication engineering history, this case should link to it and keep only the retention-specific comparison.

Methodological anti-anachronism follows [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history): later words such as `committed-prefix retention` and `checkpoint coverage` are project reconstructions, not claims about Apache's own 2014–2015 conceptual vocabulary.

---

## Status

**`grounded`** for the bounded Apache Kafka 0.8.2.0 ISR/high-watermark/consumer-visibility/checkpoint-coverage/unclean-truncation mechanism.

The KAFKA-1647 deepening closes the narrow question of whether **a durable checkpoint file can survive/rewrite while losing a still-relevant recovery relation**: yes, if runtime enumeration omits the partition. It also grounds the source-level fix that retains/creates the local replica object so the partition remains represented in the checkpoint.

Open follow-ups remain intentionally separate:

- independent reproduction/fault injection of KAFKA-1647 on a preserved 0.8.2 build;
- crash-point testing of the temp-file/sync/rename checkpoint replacement path and lower-filesystem durability;
- interaction between high-watermark checkpointing and log flush/recovery-point persistence;
- later change of the unclean-election default and durability policy history;
- modern KRaft leader/metadata recovery;
- transactional `last stable offset` versus replication high watermark;
- filesystem/device durability composition below Kafka's log.

Kafka 0.11+ leader-epoch divergent-log recovery is now handled separately by [Case 90](90-apache-kafka-leader-epoch-safe-truncation.md) rather than remaining an undifferentiated Case 56 follow-up.
