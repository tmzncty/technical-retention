# Apache Kafka 0.11 Leader-Epoch Recovery: Log Lineage, Safe Truncation, and Retained Recovery Metadata

## Scope

- **Bounded system:** Apache Kafka 0.11.0.0, released 28 June 2017, with KIP-101 and the exact `0.11.0.0` source tag as the principal historical/implementation artifacts.
- **Bounded mechanism:** leader-epoch identifiers stamped into the replicated log, per-replica epoch→start-offset recovery metadata, the `OffsetsForLeaderEpoch` exchange, follower truncation before normal fetching, and reconciliation of epoch metadata with the local log.
- **Research question:** when a follower and leader both retain plausible physical suffixes after failure, what retained relation lets the follower distinguish a common history from a divergent one without using its possibly stale high watermark as the sole truncation boundary?

This is **not** a general history of Kafka replication, ISR membership, producer acknowledgements, log compaction, transactions, or consensus. [Case 56](56-apache-kafka-replicated-log-high-watermark.md) already grounds Kafka 0.8.2 high-watermark/ISR currentness and the older failover-truncation regime. This case begins precisely where Case 56 stops: KIP-101's later lineage-aware recovery mechanism.

The bounded retention claim is:

> **Kafka 0.11 can retain a compact history of leadership boundaries alongside the replicated records and use that history to decide which physically surviving suffix still belongs to the leader's lineage. A follower first enters a truncation phase, asks the leader for the end of a leader epoch it has observed, reconciles its epoch checkpoint, truncates only beyond the resulting common boundary, and only then resumes ordinary fetching. The epoch checkpoint is therefore retained recovery lineage rather than user payload or a complete event history; successful convergence may require deliberate forgetting of a surviving divergent suffix.**

`retained recovery lineage`, `lineage-qualified truncation`, `authoritative common prefix`, and `lineage metadata` below are **project engineering terms**, not historical Kafka vocabulary.

---

## Historical vocabulary

KIP-101 and the 0.11.0.0 source use:

- `Leader Epoch`;
- `Leader Epoch Start Offset`;
- `Leader Epoch Sequence File` in the KIP design text;
- `leader-epoch-checkpoint` in the released implementation;
- `OffsetsForLeaderEpoch` / `OffsetForLeaderEpoch`;
- `LeaderEpochFileCache`;
- `truncate` / `truncateTo`;
- `high watermark`;
- `log end offset`;
- `unclean leader election`.

Do not silently rename these as a Raft term, a generic consensus epoch, a filesystem journal, or a complete operation log.

---

## Historical record

### H/P — KIP-101 was accepted for the Kafka 0.11 line as a replication-fault-tolerance change

Apache's KIP record identifies KIP-101, “Alter Replication Protocol to use Leader Epoch rather than High Watermark for Truncation,” as accepted work associated with KAFKA-1211 and the 0.11.0.0 development line. Apache's 0.11 release material dates 0.11.0.0 to 28 June 2017 and describes the new message format as supporting improved replication fault tolerance through KIP-101.

The historical claim here is consequently bounded: **by Kafka 0.11, leader-epoch information was deliberately made part of follower log-recovery/truncation semantics.** This does not claim that Kafka invented epochs, replicated logs, or truncation.

**Primary anchors:** Apache KIP-101; Apache Kafka 0.11.0.0 release/upgrade documentation.

### H/P — KIP-101 identifies a failure of high-watermark-only truncation

KIP-101's motivation gives a concrete hard-failure case in which a leader has already committed a message and a follower has fetched it, but the follower has not yet learned the newly advanced high watermark. If that follower crashes and later initializes by truncating to its older locally retained high watermark, it can delete a message that had in fact become committed.

The KIP also discusses repeated hard failures that can leave logs divergent. The problem is therefore not merely “some bytes disappeared.” It is that **a compact currentness boundary can be insufficient to reconstruct which suffix belongs to which period of leadership**.

This directly sharpens Case 56:

```text
high watermark
    = consumer/commit-prefix currentness relation
    ≠ sufficient lineage witness for every follower-recovery truncation
```

**Primary anchor:** KIP-101, Motivation.

### H/P — Leader Epoch records periods of leadership and their first offsets

KIP-101 defines a `Leader Epoch` as a monotonically increasing identifier for a continuous period of leadership of a partition and a `Leader Epoch Start Offset` as the first offset belonging to that epoch. The proposed `Leader Epoch Sequence File` records mappings from epoch to start offset.

The 0.11.0.0 source realizes the same relation in `LeaderEpochFileCache`: its documentation says it represents `(LeaderEpoch => Offset)` mappings for a particular replica and that the offset is the first message in each epoch. `LeaderEpochCheckpointFile` persists those entries in a file named `leader-epoch-checkpoint`, with each line containing `epoch startOffset`.

Thus the retained object is deliberately small compared with the user log: it marks **leadership boundaries**, not every record or fetch event.

**Primary anchors:** KIP-101; `LeaderEpochFileCache.scala`; `LeaderEpochCheckpointFile.scala`, tag `0.11.0.0`.

### H/P — the released cache is reconstructed from the checkpoint and flushed as epochs change

`LeaderEpochFileCache` initializes its in-memory epoch list from `checkpoint.read()`. On a valid new epoch assignment it adds `EpochEntry(epoch, offset)` and calls `flush()`. `endOffsetFor(epoch)` returns the next epoch's start offset as the requested epoch's end, or the current log-end offset when the requested epoch is the latest epoch.

This is direct implementation evidence for a compact retained recovery structure:

```text
(epoch 7 -> offset 100)
(epoch 8 -> offset 145)
(epoch 9 -> offset 211)
```

Such a file does not store the contents of offsets 100–210; it stores the boundaries needed to reason about which leadership interval those records belong to.

**Primary anchor:** `core/src/main/scala/kafka/server/epoch/LeaderEpochFileCache.scala`, tag `0.11.0.0`.

### H/P — follower recovery has an explicit truncation phase before ordinary fetching

`AbstractFetcherThread` in 0.11.0.0 models a partition fetch state that can be `truncatingLog`. Its `maybeTruncate()` path builds leader-epoch requests for partitions in that phase, fetches epoch end offsets from the leader, computes truncation points, performs truncation, and only then marks truncation complete. Normal fetch construction excludes a partition while it is still in the truncation phase.

The source comment states the purpose plainly: retrieve the latest offset for each partition's leader epoch, which is the offset the follower should truncate to “ensure accurate log replication.”

This supplies a temporal ordering relation:

```text
leadership/follower transition
    -> lineage query
    -> truncation decision
    -> local log convergence
    -> ordinary replication fetch
```

**Primary anchor:** `core/src/main/scala/kafka/server/AbstractFetcherThread.scala`, tag `0.11.0.0`.

### H/P — the follower asks with its retained latest epoch and truncates to the leader-qualified boundary

In `ReplicaFetcherThread`, 0.11-era brokers enable the leader-epoch request path. `buildLeaderEpochRequest` sends each truncating follower partition's latest locally known epoch. The leader returns an `EpochEndOffset`. `maybeTruncate` then chooses a truncation point:

- an undefined epoch offset falls back to the follower high watermark;
- if the leader's returned end is at or beyond the follower's current log end, the follower keeps its current end;
- otherwise it truncates to the returned leader epoch end.

The implementation then calls `logManager.truncateTo(truncationPoints)`.

So **local length is not the authority criterion**. A follower may retain more records yet deliberately delete them because the leader's epoch lineage qualifies a shorter boundary as common.

**Primary anchor:** `core/src/main/scala/kafka/server/ReplicaFetcherThread.scala`, tag `0.11.0.0`.

### H/P — epoch metadata itself must be reconciled with truncation and log lifetime

KIP-101 does not treat the sequence file as an immutable oracle. It requires the epoch information to track log deletion/compaction and says that after an unclean shutdown, if the sequence file contains entries beyond the log end, those entries must be removed. The released `LeaderEpochFileCache` likewise has `clearAndFlushLatest(offset)` to remove epoch entries whose start offsets are at or beyond a truncation point, and `clearAndFlushEarliest(offset)` to retire older entries when the log's retained prefix advances.

This is an important retention boundary: **recovery metadata is useful only while it remains consistent with the payload/log embodiment it qualifies.** Keeping more obsolete epoch entries is not automatically safer.

**Primary anchors:** KIP-101; `LeaderEpochFileCache.scala`, tag `0.11.0.0`.

### H/P — KIP-101 does not eliminate the high watermark

KIP-101 changes how follower truncation can be decided. It does not redefine the high watermark out of Kafka. The 0.11 source explicitly falls back to high-watermark truncation when a leader-epoch end offset is unavailable, including compatibility with older message/protocol regimes that lack the new epoch information.

Case 56's high watermark therefore remains a committed/visible-prefix relation; Case 90 shows that **a second retained relation was added because that boundary alone was not always enough for safe lineage recovery**.

**Primary anchors:** KIP-101 compatibility discussion; `ReplicaFetcherThread.scala`, tag `0.11.0.0`.

### H/P — the KIP explicitly preserves an unclean-election limit

KIP-101 states that the mechanism does not fully protect the `unclean.leader.election.enable=true` regime. Its appendix demonstrates how an out-of-sync replica can still become leader and create divergence that the normal clean lineage assumptions do not prevent.

Accordingly, this case must not be summarized as “leader epochs make divergent histories impossible.” The bounded claim is narrower: they improve follower truncation under the clean recovery assumptions implemented by the protocol.

**Primary anchor:** KIP-101, limitations / unclean leader election appendix.

---

## Retained state

### 1. User records / partition log

The replicated records remain the payload-bearing state.

### 2. Leader-epoch identifier carried with log data

Records/message sets acquire a relation to the leadership interval in which they were produced.

### 3. Epoch → start-offset sequence

This compact mapping records where each observed leadership interval begins. It is lineage/recovery metadata, not application payload.

### 4. `leader-epoch-checkpoint`

The released implementation gives the mapping a durable per-replica embodiment across restart.

### 5. Log end and high watermark

These remain separate currentness/progress boundaries. They are inputs/fallbacks, not synonyms for the leader-epoch history.

### 6. Fetcher truncation state

A follower can be temporarily classified as still needing truncation before ordinary replication resumes. This is transient control state, distinct from the durable epoch checkpoint.

---

## Retention mechanism

A simplified divergent-follower path is:

```text
follower retains log through offset 230
follower latest epoch = 8
current leader has epoch sequence:
    epoch 8 starts at 180
    epoch 9 starts at 214

follower becomes follower of current leader
    -> partition enters truncating phase
    -> follower asks leader for end of epoch 8
    -> leader replies 214
    -> follower truncates local suffix at 214
    -> local epoch cache is reconciled/flushed
    -> ordinary fetching resumes from the current leader
```

The exact offsets are illustrative. The sourced mechanism is the relation: **a surviving suffix is qualified by shared leadership lineage before it is admitted as the continuing log.**

---

## Engineering reconstruction

### E — physical suffix survival ≠ authoritative suffix

Bytes can remain perfectly readable on a follower and still be discarded if they lie beyond the leader-qualified common epoch boundary.

### E — log-end offset ≠ lineage equivalence

Two replicas can have equal or different lengths without that fact alone proving that their suffixes were produced under the same leadership sequence.

### E — high watermark ≠ complete recovery lineage

A high watermark compresses a committed-prefix boundary. KIP-101's motivating failure shows that the locally retained value can lag facts that became committed elsewhere before failure. The epoch sequence retains a different kind of evidence.

### E — leader epoch ≠ wall-clock timestamp

The number orders leadership periods for one partition. It should not be interpreted as elapsed physical time or as a universal cluster generation number.

### E — epoch checkpoint ≠ user payload

Losing the epoch checkpoint need not mean all partition records disappeared; it means a compact recovery relation may be unavailable and the implementation may need fallback/reconstruction behavior.

### E — epoch sequence ≠ complete operation history

The mapping preserves leadership boundaries, not every produce, fetch, acknowledgement, ISR transition, or truncation event. It is intentionally selective historical state used for future recovery.

### E — retained recovery metadata can itself become stale or impossible

Entries beyond the surviving log end after an unclean shutdown cannot truthfully qualify nonexistent records. Truncation and prefix deletion can also require epoch entries to be removed or rewritten.

### E — correct recovery can require correct forgetting

The follower may need to delete a physically surviving divergent suffix before it can safely resume replication. More retained material is not automatically more continuity.

### E — recovery ordering is part of retention semantics

`query lineage -> decide boundary -> truncate -> fetch` matters. Fetching first and deciding lineage later would mix histories before the recovery relation was established.

### E — compatibility fallback ≠ semantic identity

Falling back to the high watermark when leader-epoch data is unavailable preserves compatibility; it does not mean the two mechanisms encode the same information.

---

## Functional analogies and limits

### A — Case 56 high watermark / ISR

This is the direct internal predecessor in the repository. Case 56 grounds Kafka 0.8.2's committed-prefix/currentness boundary and older truncation behavior. Case 90 grounds the later KIP-101 response to a specific recovery weakness. The cases are historically related inside Kafka but not interchangeable.

### A — Chain Replication Case 81

Both systems retain compact protocol state that helps decide how a replica may rejoin after failure. Chain Replication uses ordered chain roles plus `Sent` suffix state; Kafka 0.11 uses leadership epochs and offset boundaries. This is functional comparison, not genealogy.

### A — HDFS QJM epoch fencing Case 50

Both use the word `epoch`, but for different authority problems. HDFS QJM epochs fence writers to journal nodes; Kafka leader epochs classify periods of partition leadership and support log truncation. Shared vocabulary is not mechanism identity.

### A — Linux RAID5 PPL Case 88

Both show that recovery can depend on retaining state much smaller than a full duplicate of the payload. PPL preserves partial-parity recovery evidence for a non-atomic stripe update; Kafka preserves leadership-boundary lineage for replicated-log convergence. No historical descent is claimed.

---

## Prior-art and genealogy boundary

Do **not** claim:

- Kafka invented replicated logs, epochs/generations, log truncation, or primary/backup recovery;
- KIP-101 invented Kafka's leader epoch concept from nothing — the KIP itself describes an existing leader epoch that is extended/stamped and used for truncation;
- the term `Leader Epoch Sequence File` necessarily remained the exact released filename — the 0.11 implementation uses `leader-epoch-checkpoint`;
- a Kafka leader epoch is equivalent to a Raft term, HDFS QJM epoch, database LSN, or wall-clock timestamp;
- KIP-101 makes unclean leader election safe from divergence;
- logical log truncation proves secure physical erasure of storage media.

The broader genealogy of epoch-based replicated-log recovery belongs in distributed-systems history / `computing-archaeology` if developed later. This case needs only enough prior-art discipline to avoid turning a 2017 Kafka implementation change into an origin myth.

---

## Philosophical interpretation — bounded

### I — continuity can depend on retaining a history of authority boundaries rather than retaining every historical event

The follower needs enough past structure to answer a future question: *where does my history stop being the same history as the current leader's?* The answer is not supplied by physical survival alone and does not require preserving a complete chronology. A sparse sequence of leadership boundaries is sufficient for this bounded protocol.

### I — forgetting can be constitutive of continuity

A divergent suffix may be materially intact yet incompatible with the current authoritative lineage. Truncating it is destructive at the byte/logical-record level but preservative at the protocol level: it re-establishes one continuing replicated history.

These are project interpretations, not claims that Apache authors used this philosophical vocabulary.

---

## What would falsify or narrow this case

- evidence that the 0.11.0.0 released path never used the epoch checkpoint for follower truncation would invalidate the central implementation claim;
- evidence that KIP-101's shipped semantics differed materially from the exact tag would require splitting proposal and implementation more sharply;
- evidence that a named fallback path preserves exactly the same lineage information as the epoch sequence would narrow the `high watermark ≠ lineage` reconstruction;
- a claim about secure erasure, physical disk overwrite, or SSD sanitization would require entirely different evidence.

---

## Sources

### Primary / official

1. Apache Kafka, **KIP-101: Alter Replication Protocol to use Leader Epoch rather than High Watermark for Truncation** — definitions, motivation, sequence-file design, request/reply recovery, compatibility, and unclean-election limit.
   - <https://cwiki.apache.org/confluence/display/KAFKA/KIP-101%3A+Alter+Replication+Protocol+to+use+Leader+Epoch+rather+than+High+Watermark+for+Truncation>
2. Apache Kafka **0.11.0.0** release / upgrade documentation — release date and KIP-101 replication-fault-tolerance context.
   - <https://kafka.apache.org/downloads>
3. Apache Kafka `0.11.0.0`, `LeaderEpochFileCache.scala`.
   - <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/server/epoch/LeaderEpochFileCache.scala>
4. Apache Kafka `0.11.0.0`, `LeaderEpochCheckpointFile.scala`.
   - <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/server/checkpoints/LeaderEpochCheckpointFile.scala>
5. Apache Kafka `0.11.0.0`, `AbstractFetcherThread.scala`.
   - <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/server/AbstractFetcherThread.scala>
6. Apache Kafka `0.11.0.0`, `ReplicaFetcherThread.scala`.
   - <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/server/ReplicaFetcherThread.scala>

See the source-by-source claim ledger in [`../evidence/90-kafka-2016-2017-leader-epoch-truncation-grounding.md`](../evidence/90-kafka-2016-2017-leader-epoch-truncation-grounding.md).

---

## Status

**`grounded`**

The bounded mechanism is supported by Apache's accepted KIP, release documentation, and exact-tag implementation source. Remaining work is historical breadth, not a blocker for this case: pre-Kafka epoch/generation genealogy, later KIP-279/KIP-320 refinements, modern KRaft behavior, production incident studies, and empirical fault injection should remain separate slices.