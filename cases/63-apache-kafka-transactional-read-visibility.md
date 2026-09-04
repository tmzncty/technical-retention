# Apache Kafka 0.11 Transactional Read Visibility: Last Stable Offset, Abort Markers, and Retained Negative Decisions

## Scope

- **Bounded system:** Apache Kafka `0.11.0.0`, tagged 28 June 2017, together with KIP-98 and the exact release-tag source tree.
- **Bounded mechanism:** transactional record batches, `READ_COMMITTED` versus `READ_UNCOMMITTED`, the high watermark, first unstable/open transaction, last stable offset (LSO), COMMIT/ABORT control batches, the per-segment transaction index, and the aborted-transaction list returned with Fetch responses.
- **Research question:** when the same physical replicated log contains committed, aborted, non-transactional, and still-open transactional records, what retained control state determines which records count as an admissible history for a `READ_COMMITTED` consumer?

This is **not** a general history of Kafka exactly-once semantics, database transactions, idempotent production, the transaction coordinator, Kafka Streams, transaction timeouts, later KIP-447/KIP-890 behavior, or post-0.11 bug fixes.

It is also distinct from two earlier Kafka cases:

- [Case 42](42-apache-kafka-log-compaction-delete-marker-retention.md) asks how keyed compaction can forget superseded **committed** history while preserving current-state reconstruction and stable logical offsets.
- [Case 56](56-apache-kafka-replicated-log-high-watermark.md) asks how the `0.8.2` ISR/high-watermark mechanism decides which physically present replicated-log prefix counts as committed and how failover can truncate a non-authoritative suffix.

Case 63 begins only after those distinctions are available. Its bounded retention claim is:

> **Kafka 0.11 introduces another admissibility frontier below or equal to the replication high watermark. A `READ_COMMITTED` consumer is bounded by the last stable offset, which is constrained by the earliest open transaction; aborted transactional records may remain physically present in the replicated log yet are deliberately filtered using retained transaction-decision evidence. Therefore physical log presence, replication commitment, transaction decision, and consumer-visible current history are distinct relations.**

`transaction-decision retention`, `negative decision evidence`, and `consumer-visible history` below are **project engineering terms**, not historical Kafka vocabulary.

---

## Historical vocabulary

The inspected Apache artifacts use:

- `transaction` / `transactional`;
- `transactional.id`;
- producer `PID` / producer ID;
- producer `epoch`;
- `Transaction Coordinator`;
- `Transaction Log`;
- `control message` / `control batch`;
- `COMMIT` and `ABORT` markers;
- `READ_COMMITTED` and `READ_UNCOMMITTED`;
- `high watermark`;
- `last stable offset` / `LSO`;
- `first unstable offset`;
- `aborted transactions`;
- `transaction index`;
- `currentTxnFirstOffset` in the producer-state implementation.

Do not silently project later Kafka transaction-defense, follower-read, tiered-storage, KRaft, or Streams implementation semantics back into the bounded `0.11.0.0` source.

---

## Historical record

### H/P — KIP-98 adds transactional decisions and hidden control records to Kafka

KIP-98 describes transactional production across multiple topic partitions and introduces a transaction coordinator, a persistent replicated transaction log, a persistent `TransactionalId`, producer epochs, and control messages. It says COMMIT/ABORT markers are written to the participating user-topic logs and are processed by the system but not exposed as ordinary application records.

The design therefore adds retained state whose purpose is not to become user payload. A control record can be invisible at the application interface while still being constitutive of how later payload is interpreted.

**Primary anchor:** Apache Kafka, KIP-98, `Key Concepts`, `Committing or Aborting a Transaction`, `Control Messages`.

### H/P — abort means user-level exclusion, not physical record removal

KIP-98 describes `abortTransaction()` as making produced records inaccessible to downstream users: consumers encounter and discard the aborted transactional data rather than treating it as committed output. The design also writes an ABORT marker into each participating user log.

That wording must be handled carefully. `effectively erases` in the design is an **interface/logical** statement. It is not evidence that the record bytes are physically erased from the log segment at abort time.

Thus the historical mechanism itself supports:

```text
transactional record bytes remain in log
        + ABORT decision becomes durable/observable to the protocol
        -> READ_COMMITTED consumer does not deliver those records
```

**Primary anchor:** KIP-98 §5.1–5.3.

### H/P — Kafka 0.11 distinguishes high watermark from last stable offset

The exact `0.11.0.0` `ConsumerConfig` documentation says a `READ_COMMITTED` consumer returns transactional messages only after commit. It defines the LSO as one less than the offset of the first open transaction and explicitly says a `READ_COMMITTED` consumer may be unable to read up to the high watermark while transactions are in flight.

It also states that records are returned in offset order. Consequently, records that occur after an open transaction are withheld until that transaction is completed.

The bounded relation is therefore:

```text
log end offset
    >= high watermark
    >= last stable offset
```

where the two right-hand frontiers answer different questions.

**Primary anchor:** `clients/src/main/java/org/apache/kafka/clients/consumer/ConsumerConfig.java`, tag `0.11.0.0`, `ISOLATION_LEVEL_DOC`.

### H/P — broker read admission uses LSO separately from high watermark

`ReplicaManager.scala` carries both `highWatermark` and `lastStableOffset` in read/fetch result state. For `READ_COMMITTED`, it obtains the local replica LSO and uses it as the maximum readable offset; otherwise the ordinary committed read path can use the high watermark.

This source-level separation prevents a misleading statement such as `high watermark is the Kafka visibility frontier` without qualification. In the transactional regime, replication commitment is necessary but not sufficient for `READ_COMMITTED` visibility.

**Primary anchor:** `core/src/main/scala/kafka/server/ReplicaManager.scala`, tag `0.11.0.0`, local replica read path.

### H/P — the first unstable transaction is retained as a visibility constraint

`Log.scala` keeps `firstUnstableOffset`, described in the source as the earliest offset belonging to an incomplete transaction and used to compute the LSO. The same comment says the purpose is to restrict `READ_COMMITTED` fetching to decided data.

A still-open transaction therefore creates a retained negative constraint on the future read frontier. The transaction's payload may already be in the physical log and may already lie below the replication high watermark, but its decision state has not yet advanced far enough for `READ_COMMITTED` consumers to pass it.

**Primary anchor:** `core/src/main/scala/kafka/log/Log.scala`, tag `0.11.0.0`, `firstUnstableOffset`.

### H/P — transaction completion writes a marker and advances transaction-state bookkeeping

In the bounded source, `CompletedTxn` records producer ID, first transaction offset, the offset of the COMMIT/ABORT control record, and whether the transaction was aborted. After a completed transaction is appended, the log asks `ProducerStateManager.completeTxn` for the true LSO and updates the segment transaction index.

The source comment is explicit that the last offset visible to `READ_COMMITTED` consumers is limited by this LSO together with the high watermark.

**Primary anchor:** `Log.scala`, tag `0.11.0.0`, completed-transaction / transaction-index update path.

### H/P — the transaction index retains aborted-transaction evidence by log segment

`TransactionIndex.scala` says directly that the transaction index maintains metadata about aborted transactions for each segment, including their start/end offsets and the LSO at abort time, and that the index is used for fetches at `READ_COMMITTED` isolation.

The file is organized per segment. Transactions may span segments, so rebuilding/searching the index can require earlier segment context. The index entry itself contains:

```text
producerId
firstOffset
lastOffset
lastStableOffset
```

This is retained control/index state rather than application payload.

**Primary anchor:** `core/src/main/scala/kafka/log/TransactionIndex.scala`, tag `0.11.0.0`.

### H/P — the broker returns aborted ranges so the consumer can suppress payload

For a `READ_COMMITTED` read, `Log.scala` collects aborted transactions overlapping the requested range from the segment transaction indexes and attaches them to fetch data. KIP-98's Fetch response design includes both `HighwaterMarkOffset`, `LastStableOffset`, and an `AbortedTransactions` list.

The consumer then skips record batches belonging to aborted producers/ranges, while control batches themselves are not returned as ordinary user records.

The retained log therefore contains at least three semantically different classes of bytes:

1. ordinary/application records that may be deliverable;
2. transactional records whose eventual deliverability depends on a decision;
3. control/index evidence that participates in deciding or explaining that deliverability but is not itself application payload.

**Primary anchors:** KIP-98 `FetchRequest/Response`; `Log.scala`; transaction-index implementation; the KIP-98 implementation commit for transaction-index/consumer filtering.

### H/P — producer-state snapshots retain enough recent transaction/producer state to aid restart reconstruction

`ProducerStateManager.scala` stores producer epoch/sequence/offset information and `current_txn_first_offset` in its snapshot schema. The source also supports rebuilding producer state by loading snapshots and replaying log records during recovery.

This does **not** mean every in-memory transaction-coordination fact is synchronously persisted in one snapshot. The narrower claim is that the broker maintains explicit recoverable producer/transaction progress metadata in addition to the payload log and transaction index.

**Primary anchor:** `core/src/main/scala/kafka/log/ProducerStateManager.scala`, tag `0.11.0.0`.

---

## Retained state

The bounded mechanism contains several retained relations that should not be collapsed.

### 1. User log records

The physical append-only log contains ordinary records and transactional records. Presence here is weaker than `READ_COMMITTED` admissibility.

### 2. Replication high watermark

As in Case 56, this is the replicated committed-prefix frontier. It says nothing by itself about whether a transaction covering records below that frontier is committed or aborted.

### 3. Earliest open / first unstable transaction offset

This is a current transaction-state frontier used in LSO calculation. An earlier undecided transaction can constrain how far a `READ_COMMITTED` consumer may advance.

### 4. Last stable offset

LSO is a consumer-visible stability boundary. In the bounded 0.11 source it can lag the high watermark.

### 5. COMMIT / ABORT control records

These are log records with protocol meaning but not ordinary application payload. They encode the outcome required to interpret earlier transactional records.

### 6. Transaction index

The index retains bounded metadata about aborted transactions and associated stability boundaries so fetches can identify payload that must be filtered.

### 7. Producer-state / open-transaction recovery metadata

Producer ID, epoch, sequences, current transaction start, and related snapshot/replay state support correct continuation and fencing/recovery. They are adjacent retention infrastructure rather than the application data itself.

---

## Retention mechanism

A simplified committed path is:

```text
producer begins transaction T
    -> transactional batches appended to partition log
    -> batches can become replicated below high watermark
    -> T remains open
    -> first unstable offset constrains LSO
    -> READ_COMMITTED consumer stops before T
    -> COMMIT control marker is appended
    -> transaction becomes decided
    -> LSO may advance, subject to any other earlier open transaction and HW
    -> committed records become deliverable
```

A simplified abort path is:

```text
producer begins transaction T
    -> transactional batches appended and replicated
    -> ABORT decision
    -> ABORT control marker appended
    -> transaction index records aborted range / LSO evidence
    -> LSO can advance past the completed transaction
    -> broker returns aborted-range metadata
    -> READ_COMMITTED consumer skips T's payload
    -> physical log may continue to contain T's records
```

The second path is a particularly clear retention/forgetting paradox:

> **the system may need to retain a negative decision long enough to make some physically retained payload count as forgotten for an application-level history.**

---

## Read, write, and decision semantics

### Transactional append

Appending the bytes is not the same operation as deciding their transaction. The records can exist and replicate before the transaction outcome exists.

### `READ_UNCOMMITTED`

The default isolation mode can return transactional records without applying the `READ_COMMITTED` decision filter, including records that later prove aborted.

### `READ_COMMITTED`

The consumer is constrained by LSO and suppresses aborted transaction data. This changes the admissible history without changing the underlying log bytes.

### COMMIT

A commit marker participates in making the transaction's records admissible to `READ_COMMITTED` consumers once the stability frontier permits progress.

### ABORT

An abort marker makes those transaction records non-deliverable to `READ_COMMITTED` consumers. It is logical/semantic forgetting, not immediate physical erasure.

### Recovery

Transaction/producer metadata can be reconstructed from snapshots, log records, and segment indexes. Rebuildability changes representation and restart work; it does not make this metadata semantically optional.

---

## Engineering reconstruction

### E — high watermark ≠ last stable offset

The high watermark is a replication/currentness frontier. The LSO is a transaction-stability/read-isolation frontier. A record can lie below the HW yet above the LSO.

### E — replication commitment ≠ transaction decision

A transaction's bytes can satisfy the replication condition represented by HW before the transaction is known to be committed or aborted.

### E — physical record presence ≠ `READ_COMMITTED` admissibility

An aborted record can remain in a live log segment and still be deliberately absent from the application history observed through `READ_COMMITTED`.

### E — abort ≠ physical erasure

The bounded mechanism forgets by **retained decision + read filtering**, not by synchronously removing the original record bytes.

### E — negative decision evidence can be retention infrastructure

The ABORT outcome, control marker, and transaction-index range are retained precisely so later readers can continue *not* to treat the payload as valid committed history.

This is retention in the service of forgetting.

### E — control-record invisibility ≠ control-state irrelevance

The control marker is intentionally hidden from ordinary application consumption, yet removing its protocol meaning would change whether earlier records are deliverable.

### E — one open transaction can constrain later offset visibility

Because `READ_COMMITTED` preserves partition offset ordering and stops at the earliest open transaction, a later record may wait even if that later record is otherwise non-transactional or belongs to a transaction already decided.

The blocking relation comes from the ordered log frontier, not from a claim that the later record belongs to the earlier transaction.

### E — transaction index ≠ complete transaction history

The per-segment index stores bounded aborted-transaction metadata and LSO information useful for fetch. It does not preserve every coordinator transition, producer request, retry, or causal step that produced the outcome.

### E — rebuildable metadata ≠ dispensable metadata

If an index or producer-state snapshot can be reconstructed by scanning authoritative records, the system may replace one physical representation of control state. The logical function remains necessary.

### E — consumer isolation can select different admissible histories over the same bytes

`READ_UNCOMMITTED` and `READ_COMMITTED` are not two different physical logs. They are different read-admission rules over one retained log plus transaction decision state.

---

## Functional analogies and limits

### A — Case 56 high watermark versus Case 63 LSO

Both are offset frontiers, but they must not be collapsed:

```text
Case 56 high watermark:
    sufficiently replicated/current prefix

Case 63 last stable offset:
    transactionally decided prefix for READ_COMMITTED exposure
```

LSO cannot safely be treated as a later spelling for HW. Transactional Kafka intentionally carries both.

### A — Case 42 compaction tombstone versus Case 63 abort marker

Both can make physically retained records cease to appear in one logical view, but their semantics differ:

- a compaction delete marker is a keyed negative current-state record whose retention horizon protects compaction/current-state reconstruction;
- a transaction ABORT marker says the transaction's produced records never become `READ_COMMITTED` application history.

A tombstone supersedes a keyed prior state. An abort rejects a transaction outcome.

### A — distributed-delete tombstones (Cases 28 and 41) versus transaction abort

Swift/Cassandra tombstones must suppress stale positive replicas across distributed repair windows. Kafka transaction abort works inside an ordered log/transaction-isolation protocol. The useful analogy is only:

> **negative evidence may itself need retention so an older or physically surviving positive representation does not regain authority.**

The replication/reconciliation mechanisms are different.

### A — Raft snapshotting (Case 58) versus transaction-index rebuild

Both show that retained control state can be materialized/reconstructed in forms other than the entire event history. Raft snapshotting deliberately replaces an authoritative command prefix with state-machine materialization; Kafka transaction indexes are derived lookup structures tied to a still-existing log. They are not the same compaction mechanism.

---

## Failure, recovery, and limits

### Open transaction stall

An unresolved earlier transaction can hold LSO behind HW and therefore withhold later records from `READ_COMMITTED` consumers. That is a service/visibility consequence of retained uncertainty, not evidence that the later bytes disappeared.

### Index/recovery dependence

The transaction index can cross segment boundaries conceptually because a transaction itself can span segments. The source notes that index recovery may require scanning earlier segments to rediscover the transaction start.

### Later fixes are outside the bounded claim

Kafka transactions received substantial fixes and defenses after 0.11.0.0. A later bug fix or KIP may reveal a weakness in the first implementation; it should not be silently used to rewrite the 0.11 mechanism as if the later invariant had always been fully enforced.

### Transactional commit ≠ atomic consumer delivery in one poll

KIP-98 itself limits the intuitive `transaction = one atomic consumer batch` reading. Consumers may seek, subscribe to only some partitions, and encounter retention/compaction boundaries. The guarantee is about transactional visibility/decision, not a promise that every record in one committed cross-partition transaction is delivered to one consumer in one indivisible operation.

### Abort ≠ sanitization

Neither ABORT nor consumer filtering is evidence of secure erase, media sanitization, raw-device disappearance, or forensic non-recoverability. Cases 44 and 47 remain the relevant technical-forgetting boundaries for those questions.

---

## Prior art and novelty boundary

Kafka 0.11 did **not** invent transactions, atomic commit, isolation, transaction logs, commit/abort, or distributed transaction processing.

IBM/System R literature had already used the transaction concept and transaction-log-based commit/abort/recovery decades earlier; for example Jim Gray and colleagues' 1981 System R recovery-manager paper explicitly discusses programs committing/aborting effects and transaction-log-based undo/redo. Earlier database work likewise predates Kafka's use of `transaction` vocabulary.

The defensible bounded claim is narrower:

> **By Kafka 0.11.0.0, Apache combined an ordered replicated log with transactional record batches, hidden commit/abort control records, a first-open-transaction/LSO visibility frontier, per-segment aborted-transaction indexing, and a selectable `READ_COMMITTED` consumer rule.**

That combination is historically interesting for this repository because it makes **retained negative decision state** part of what determines the application-visible history of an otherwise physically surviving log.

Do not convert this into an invention-priority claim for any of the general ingredients.

---

## Philosophical interpretation

### I — a retained log does not contain one self-evident past

The bounded technical mechanism shows that the same byte sequence can support more than one legitimate later view. `READ_UNCOMMITTED` and `READ_COMMITTED` do not differ because one has access to a physically different archive. They differ because retained decision state and a read rule determine what counts as admissible history.

This supports a narrow question for the repository:

> When a technical system retains both an inscription and the later decision that the inscription must not count, which one is the retained past?

The engineering answer is relational: both may survive, while protocol semantics decide which is available to a particular operation.

### Boundary

This does **not** prove that database/Kafka isolation is equivalent to historiography, archival exclusion, repression, or human memory. Those are interpretive analogies requiring independent argument.

---

## Claim ledger

| Claim | Type | Status |
| --- | --- | --- |
| Kafka 0.11 exposes `READ_COMMITTED` / `READ_UNCOMMITTED` transactional read isolation | `H/P` | established from exact tag source |
| LSO can lag HW because of the earliest open transaction | `H/P` | established |
| later offsets can be withheld until an earlier transaction completes | `H/P` | established by consumer config semantics |
| COMMIT/ABORT markers are control records not ordinary user payload | `H/P` | established from KIP/source |
| transaction index stores aborted transaction ranges plus LSO data | `H/P` | established from exact tag source |
| abort removes record bytes immediately | `X` | rejected |
| physically present record is automatically `READ_COMMITTED` history | `X` | rejected |
| HW and LSO are synonyms | `X` | rejected |
| one transaction must be delivered to one consumer as one indivisible batch | `X` | rejected/overbroad |
| Kafka invented transactions or atomic commit | `X` | rejected by prior art |
| negative decision evidence can be retention infrastructure | `E` | supported reconstruction |
| the same physical log can support different admissible histories under different isolation rules | `E/I` | supported, with interpretive boundary |

---

## Source notes

Primary and high-quality anchors used in this bounded case:

1. Apache Kafka, **KIP-98 — Exactly Once Delivery and Transactional Messaging**: <https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging>.
2. Apache Kafka tag **`0.11.0.0`**, tagged 28 June 2017: <https://github.com/apache/kafka/tree/0.11.0.0>.
3. `ConsumerConfig.java`, exact `0.11.0.0` tag: <https://github.com/apache/kafka/blob/0.11.0.0/clients/src/main/java/org/apache/kafka/clients/consumer/ConsumerConfig.java>.
4. `ReplicaManager.scala`, exact tag: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/server/ReplicaManager.scala>.
5. `Log.scala`, exact tag: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/log/Log.scala>.
6. `TransactionIndex.scala`, exact tag: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/log/TransactionIndex.scala>.
7. `ProducerStateManager.scala`, exact tag: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/log/ProducerStateManager.scala>.
8. Apache commit **KAFKA-5121; Implement transaction index for KIP-98**, 6 May 2017: <https://github.com/apache/kafka/commit/e71dce89c0da50f3eccc47d0fc050c92d5a99b88>.
9. Jim Gray et al., **The Recovery Manager of the System R Database Manager**, *ACM Computing Surveys* 13(2), June 1981; IBM Research bibliographic record: <https://research.ibm.com/publications/the-recovery-manager-of-the-system-r-database-manager>.

Related-repository search during this slice found no dedicated Kafka transaction/LSO case in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). Broader database transaction history, log-structured system history, and Kafka architecture history should go there if developed; this file keeps only the retention-specific distinction needed here.

---

## Findings promoted to CASE_INDEX

1. **high watermark ≠ last stable offset**;
2. **replication commitment ≠ transaction decision**;
3. **physically retained aborted record ≠ `READ_COMMITTED`-visible record**;
4. **transaction abort ≠ physical erasure**;
5. **negative decision evidence can sustain logical forgetting**;
6. **control-record invisibility ≠ control-state irrelevance**;
7. **first open transaction can constrain visibility of later offsets**;
8. **offset-order preservation can turn one open transaction into a partition-wide read frontier**;
9. **transaction index ≠ user payload**;
10. **transaction index ≠ complete transaction history**;
11. **rebuildable metadata ≠ dispensable metadata**;
12. **`READ_UNCOMMITTED` and `READ_COMMITTED` can expose different admissible histories from the same physical log**;
13. **replication-currentness state ≠ transaction-decision state**;
14. **transactional commit ≠ atomic consumer delivery as one indivisible read batch**;
15. **Kafka abort marker ≠ Kafka compaction tombstone**;
16. **Kafka 0.11 transactional isolation ≠ invention of transactions/atomic commit**.
