# Case 90 Grounding Record — Kafka 2016–2017 Leader-Epoch Truncation

## Purpose

This record grounds [`cases/90-apache-kafka-leader-epoch-safe-truncation.md`](../cases/90-apache-kafka-leader-epoch-safe-truncation.md) without turning KIP-101 into a generic history of replicated logs.

**Question:** what evidence supports the claim that Kafka 0.11 retained a compact leader-epoch→offset lineage and used it to qualify follower truncation before ordinary replication resumed?

**Evidence boundary:** accepted Apache design material + exact `0.11.0.0` source are primary. Later Kafka documents are useful only to clarify compatibility/evolution, not to back-project modern semantics into 2017.

---

## Source ledger

### P1 — Apache KIP-101

**Artifact:** Apache Kafka, `KIP-101: Alter Replication Protocol to use Leader Epoch rather than High Watermark for Truncation`.

**URL:** <https://cwiki.apache.org/confluence/display/KAFKA/KIP-101%3A+Alter+Replication+Protocol+to+use+Leader+Epoch+rather+than+High+Watermark+for+Truncation>

**Type:** primary / contemporaneous standards-design record.

**Supports:**

- KIP status / issue linkage;
- historical definitions of `Leader Epoch`, `Leader Epoch Start Offset`, and `Leader Epoch Sequence File`;
- the committed-message-loss failure possible when follower initialization truncates to a stale local high watermark;
- repeated-hard-failure divergent-log motivation;
- the epoch→start-offset vector as a lineage witness;
- follower request to the leader for an epoch end and subsequent truncation;
- per-log-directory sequence-file persistence/caching proposal;
- compatibility fallback when epoch information is unavailable;
- reconciliation of sequence data with log deletion/compaction and unclean-shutdown log end;
- explicit limitation under unclean leader election.

**Does not support:**

- a claim that Kafka invented epochs, replicated logs, or truncation;
- a claim that KIP-101 makes all leader elections divergence-free;
- physical-medium erasure semantics.

### P2 — Apache Kafka 0.11.0.0 release documentation

**Artifact:** Apache Kafka downloads / 0.11 upgrade material.

**URLs:**

- <https://kafka.apache.org/downloads>
- <https://kafka.apache.org/0110/documentation.html#upgrade_11_message_format>

**Type:** primary / official product documentation.

**Supports:**

- release date: **28 June 2017** for 0.11.0.0;
- 0.11 message-format change context;
- official attribution of improved replication fault tolerance to KIP-101.

**Does not support:**

- detailed source-level truncation behavior by itself.

### P3 — `LeaderEpochFileCache.scala`, tag `0.11.0.0`

**Artifact:** Apache Kafka source.

**URL:** <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/server/epoch/LeaderEpochFileCache.scala>

**Type:** primary implementation artifact.

**Observed implementation facts:**

- `LeaderEpochCache` exposes assignment, latest-epoch query, epoch end-offset lookup, and clearing/flushing operations;
- `LeaderEpochFileCache` says it represents `(LeaderEpoch => Offset)` mappings for one replica;
- offset is the first message in each epoch;
- startup populates the in-memory list from `checkpoint.read()`;
- accepted epoch assignments append an `EpochEntry(epoch, offset)` and flush;
- `endOffsetFor` resolves an epoch end using the first start offset of the next epoch, or LEO for the latest epoch;
- `clearAndFlushLatest` removes entries whose starts are at/after a truncation boundary;
- `clearAndFlushEarliest` retires/adjusts older epoch boundaries as the retained log prefix advances;
- `flush()` writes the epoch list to the checkpoint.

**Inference allowed:** this is compact recovery/lineage metadata rather than application payload or complete record history.

**Inference not allowed:** its on-disk persistence is equivalent to transactional durability of every application record.

### P4 — `LeaderEpochCheckpointFile.scala`, tag `0.11.0.0`

**Artifact:** Apache Kafka source.

**URL:** <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/server/checkpoints/LeaderEpochCheckpointFile.scala>

**Type:** primary implementation artifact.

**Observed implementation facts:**

- filename constant is `leader-epoch-checkpoint`;
- source says the class persists a map of `(LeaderEpoch => Offsets)` for a particular replica;
- line formatter serializes `epoch startOffset`;
- checkpoint read/write provides the durable embodiment used by the cache.

**Boundary:** KIP-101's design phrase `Leader Epoch Sequence File` and the implementation filename are related but not identical strings; the case preserves both rather than normalizing one into the other.

### P5 — `AbstractFetcherThread.scala`, tag `0.11.0.0`

**Artifact:** Apache Kafka source.

**URL:** <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/server/AbstractFetcherThread.scala>

**Type:** primary implementation artifact.

**Observed implementation facts:**

- fetch state has a `truncatingLog` phase;
- `doWork()` calls `maybeTruncate()` before building the normal fetch request;
- `maybeTruncate()` builds epoch requests for truncating partitions, fetches leader epoch ends, computes truncation, then marks truncation complete;
- source comments state the leader epoch result identifies the offset a follower should truncate to for accurate log replication;
- partitions are not treated as ordinary ready-for-fetch partitions until truncation completes.

**Supports:** recovery ordering is itself a control relation: **qualify lineage before normal replication resumes**.

### P6 — `ReplicaFetcherThread.scala`, tag `0.11.0.0`

**Artifact:** Apache Kafka source.

**URL:** <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/server/ReplicaFetcherThread.scala>

**Type:** primary implementation artifact.

**Observed implementation facts:**

- leader-epoch requests are enabled for the appropriate 0.11 inter-broker protocol level;
- request construction uses the follower's latest epoch from its local epoch cache;
- `maybeTruncate` consumes `EpochEndOffset` replies;
- undefined epoch end falls back to high watermark;
- leader epoch end at/beyond follower LEO keeps the follower LEO;
- a leader epoch end behind follower LEO becomes the truncation point;
- the resulting map is passed to `logManager.truncateTo`;
- older offset-out-of-range / unclean-election handling remains separately present.

**Supports:** surviving follower length is not the sole recovery authority and KIP-101 coexists with fallback/legacy paths.

---

## Claim ledger

| Claim | Layer | Evidence | Strength |
|---|---|---|---|
| Kafka 0.11.0.0 shipped 28 June 2017 | historical record | P2 | strong |
| KIP-101 was accepted to alter replication truncation from HW-only toward leader-epoch recovery | historical record | P1, P2 | strong |
| stale follower HW can delete a message already committed on the leader in the motivating hard-failure case | historical record | P1 | strong |
| Leader Epoch denotes a leadership period and maps to its first offset | historical record | P1, P3 | strong |
| released code persists epoch/start-offset entries in `leader-epoch-checkpoint` | historical/implementation record | P3, P4 | strong |
| follower recovery has a truncating phase before ordinary fetch | implementation record | P5 | strong |
| follower queries leader for its latest local epoch and can truncate to returned epoch end | implementation record | P5, P6 | strong |
| undefined epoch data falls back to high-watermark-based recovery | implementation record | P6; P1 compatibility discussion | strong |
| epoch metadata can itself be pruned/reconciled after truncation/log-prefix movement | historical/implementation record | P1, P3 | strong |
| KIP-101 does not fully solve unclean-election divergence | historical record | P1 | strong |
| high watermark ≠ complete recovery lineage | engineering reconstruction | P1 + Case 56 comparison | strong |
| physical suffix survival ≠ authoritative suffix | engineering reconstruction | P5, P6 | strong |
| epoch checkpoint ≠ complete operation history | engineering reconstruction | P3, P4 | strong |
| correct convergence can require forgetting a surviving divergent suffix | engineering reconstruction | P5, P6 | strong |
| Kafka leader epoch ≠ HDFS QJM epoch / Raft term | comparison boundary | source-specific meanings; Cases 50/90 | strong as a non-equivalence rule |
| truncation ≠ secure sanitization | negative boundary | no physical erase claim in P1–P6 | strong as claim-control boundary |

---

## Historical record / engineering reconstruction / analogy separation

### Historical record

Safe to state as period facts:

- KIP-101's own definitions and motivating failure cases;
- the accepted 0.11 design intent to use leader epochs for safer follower truncation;
- exact-tag source objects, filenames, APIs, fetcher state transitions, and truncation branches;
- compatibility fallback and explicit unclean-election limitation.

### Engineering reconstruction

Project terms that summarize those facts but are not Kafka period vocabulary:

- `retained recovery lineage`;
- `lineage-qualified truncation`;
- `authoritative common prefix`;
- `lineage metadata`;
- `physical suffix survival ≠ authoritative suffix`;
- `high watermark ≠ complete recovery lineage`.

### Functional analogy only

- Chain Replication Case 81: both coordinate replica re-entry, different mechanisms/history;
- HDFS QJM Case 50: both use the word epoch, but one fences journal writers and one marks partition leadership lineage;
- RAID5 PPL Case 88: both preserve bounded recovery evidence smaller than payload, but one is parity/write-hole recovery and one replicated-log genealogy;
- Raft Case 58: replicated logs and truncation are comparable at a high level, but no direct lineage is asserted here.

### Philosophical interpretation only

The repository may interpret the mechanism as evidence that continuity can depend on selective historical retention and selective forgetting. That is **not** an Apache historical claim.

---

## Prior-art controls

### Reject: “KIP-101 invented Kafka leader epochs”

KIP-101 itself describes an **existing Leader Epoch** and proposes using/stamping it for truncation semantics. The bounded novelty claim is a change in replication recovery use, not origin of the concept.

### Reject: “KIP-101 invented epoch-based replicated-log recovery”

No such priority search has been performed. Replicated-log generation/term/epoch techniques predate this bounded implementation in distributed-systems literature. A genealogy claim belongs in separate historical research.

### Reject: “leader epoch = Raft term”

The systems can be functionally compared, but their source vocabularies, state machines, and historical lineages must remain separate unless direct evidence establishes a relation.

### Reject: “leader-epoch-checkpoint replaces the log”

The file stores boundary entries. Payload remains in the partition log.

### Reject: “leader epochs replace high watermark everywhere”

The exact 0.11 source retains high-watermark semantics and a fallback truncation path.

### Reject: “truncation securely erases the abandoned records”

Logical log truncation does not establish a forensic/media sanitization guarantee.

---

## Cross-case comparison notes

### Case 56 — direct Kafka predecessor

Case 56 established that in Kafka 0.8.2:

- assigned replicas ≠ ISR-qualified replicas;
- leader LEO ≠ committed high watermark;
- ordinary reads are bounded by HW;
- recovery could truncate a longer returning follower after unclean election.

Case 90 should not repeat those as new discoveries. Its contribution is narrower and later: **why high-watermark state can be insufficient for safe follower truncation and how leader-epoch lineage adds a different retained relation.**

### Case 50 — same word, different epoch

HDFS QJM `epoch` grants/fences writer authority at journal nodes. Kafka `Leader Epoch` labels periods of partition leadership so a replica can locate a lineage boundary. This is a useful anti-anachronism/anti-equivalence test.

### Case 81 — state needed until reconfiguration completes

Chain Replication's `Sent` state retains in-flight updates until acknowledgements/repair close. Kafka's epoch checkpoint persists across steady operation and restart as a sparse lineage structure. Both show protocol metadata can be constitutive of retention without being payload.

### Case 88 — recovery-sufficient evidence can be smaller than payload

Linux MD PPL stores partial parity and stripe metadata rather than a second complete copy of every in-flight write. Kafka stores leadership boundary points rather than a second complete event history. The mathematical/operational mechanisms are unrelated.

---

## Remaining work deliberately left open

- pre-Kafka genealogy of leader epochs/generations/terms in replicated logs;
- KIP-279/KIP-320 and later truncation refinements;
- KRaft-era metadata/leadership semantics;
- exact historical rollout behavior in mixed-version production clusters;
- fault-injection reproduction of KIP-101 motivating cases;
- forensic behavior of truncated records on HDD/SSD media;
- broader Kafka replication history in `computing-archaeology` if that repository later chooses it.

These are not blockers for the bounded `grounded` status of Case 90.