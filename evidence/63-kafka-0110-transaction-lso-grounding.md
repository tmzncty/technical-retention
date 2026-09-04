# Case 63 Grounding Record — Apache Kafka 0.11 Transactional Read Visibility, 2017

## Status

**`grounded`** for the bounded claim that Kafka `0.11.0.0` separates the replicated high watermark from a transaction-sensitive last stable offset (LSO), retains COMMIT/ABORT decision evidence and aborted-transaction index state, and uses those relations to decide what a `READ_COMMITTED` consumer may observe even while excluded transactional records remain physically present in the log.

This record does **not** claim that Kafka invented transactions, atomic commit, isolation, transaction logs, commit/abort markers as a general concept, or exactly-once processing.

---

## Research question

Once transactional records have been appended and replicated, what additional retained state is required to determine whether they belong to the application-visible committed history?

The bounded answer is:

```text
physical log record
    + replication currentness / high watermark
    + transaction decision state
    + first-open-transaction frontier / LSO
    + aborted-transaction lookup evidence
    + consumer isolation rule
        ↓
READ_COMMITTED admissibility
```

The central result is therefore not `Kafka stores transactions`. It is:

> **a replicated record can survive materially and still fail to count as part of the retained history presented to a particular reader.**

---

## Repository-state and duplication check

Before this slice, the repository already had two Kafka cases:

- Case 42 — log compaction/delete-marker retention;
- Case 56 — `0.8.2` ISR/high-watermark replicated-prefix currentness and failover truncation.

Case 56 explicitly left `transactions/last-stable-offset` as later work rather than importing post-0.8 semantics. Case 63 closes that specific later boundary without modifying the older case's historical vocabulary.

A repository search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for Kafka transaction/LSO-specific material returned no dedicated case during this slice. Broader Kafka/database transaction history therefore remains appropriate future work there; this repository keeps only the retention-specific comparison.

---

## Source ledger

| Source | Type | Exact use | What it does not prove |
| --- | --- | --- | --- |
| Apache Kafka, KIP-98, `Exactly Once Delivery and Transactional Messaging` | `H/P`, project design record | transaction coordinator/log concepts; transactional ID and producer epoch; COMMIT/ABORT control messages; fetch isolation; LSO and aborted-transaction response fields; abort as downstream non-delivery; limitations | not final normative specification for every implementation detail; current wiki rendering may include later edits; exact release source is used for implementation claims |
| Apache Kafka tag `0.11.0.0`, annotated 2017-06-28 | `H/P`, exact release tag | bounded implementation/version identity | tag date alone does not prove feature correctness or deployment prevalence |
| `ConsumerConfig.java`, tag `0.11.0.0`, `ISOLATION_LEVEL_DOC` | `H/P`, exact source | `READ_COMMITTED`/`READ_UNCOMMITTED`; LSO as one less than first open transaction; offset-order withholding; LSO may lag HW; `seekToEnd` behavior | consumer documentation does not by itself explain index persistence/recovery |
| `ReplicaManager.scala`, tag `0.11.0.0` | `H/P`, exact broker source | simultaneous HW and LSO state; LSO used as maximum offset under `READ_COMMITTED`; fetch response transports LSO and aborted transaction data | does not alone prove coordinator durability or raw disk layout |
| `Log.scala`, tag `0.11.0.0` | `H/P`, exact storage source | `firstUnstableOffset`; completed transaction processing; transaction-index update; aborted-transaction collection; source comment tying visible offset to LSO and HW | does not make transaction index the sole authority for transaction outcome |
| `TransactionIndex.scala`, tag `0.11.0.0` | `H/P`, exact storage source | per-segment aborted transaction metadata; first/last offsets; LSO-at-abort; READ_COMMITTED lookup; cross-segment recovery note | index is derived protocol metadata, not the full transaction log or transaction coordinator state |
| `ProducerStateManager.scala`, tag `0.11.0.0` | `H/P`, exact source | producer epochs/sequences; current transaction first offset; producer-state snapshot schema; recovery/replay support | not evidence that every in-memory transition is synchronously durable at every instant |
| Apache commit `e71dce89c0da50f3eccc47d0fc050c92d5a99b88`, KAFKA-5121, 2017-05-06 | `H/P`, implementation-history artifact | explicit KIP-98 transaction-index implementation; Fetch protocol isolation/LSO/aborted transaction data; consumer filtering/control-batch changes | one commit does not represent every final 0.11 transaction change |
| Jim Gray et al., `The Recovery Manager of the System R Database Manager`, *ACM Computing Surveys* 13(2), 1981 | `H/S-P`, contemporary database prior-art anchor via IBM Research | transaction concept; application commit/abort; transaction-log undo/redo; blocks Kafka-first transaction/recovery claim | does not imply direct implementation lineage into Kafka |

---

## Primary-source anchors

### 1. Exact `0.11.0.0` release boundary

Apache's annotated tag `0.11.0.0` points to commit `e18335dd953107a61d89451932de33d33c0fd207` and is dated **28 June 2017**.

This date is used only to bound the source tree. It is safer than treating current Kafka documentation as if every modern statement described the first transaction implementation.

---

### 2. Consumer configuration — LSO is not the high watermark

`ConsumerConfig.ISOLATION_LEVEL_DOC` in the exact tag provides the strongest concise semantic anchor.

It establishes that:

- `READ_COMMITTED` returns transactional records only when committed;
- `READ_UNCOMMITTED` is the default and may return records from aborted transactions;
- records are returned in offset order;
- LSO is one less than the offset of the first open transaction;
- records after an ongoing transaction are withheld until the relevant transaction completes;
- a `READ_COMMITTED` consumer therefore may not read all the way to the high watermark;
- `seekToEnd` uses LSO in this isolation mode.

The critical distinction is not just numerical:

```text
high watermark
    asks: how far is the replicated committed prefix?

last stable offset
    asks: how far is the ordered prefix transactionally decided for READ_COMMITTED?
```

This directly closes the later-transaction gap intentionally left by Case 56.

---

### 3. ReplicaManager — the broker carries both frontiers at once

`ReplicaManager.scala` does not collapse the two frontiers into one variable. `LogReadResult` / `FetchPartitionData` carry `highWatermark` and `lastStableOffset` separately.

In the read path, the broker takes the local replica high watermark, computes LSO when isolation is `READ_COMMITTED`, and uses LSO as the maximum offset for a committed read when available.

This is direct implementation evidence for:

> **replication commitment ≠ transactional read admissibility.**

It also means the same partition can have several meaningful `end` positions depending on the operational question.

---

### 4. Log — first unstable offset is retained uncertainty

`Log.scala` describes `firstUnstableOffset` as the earliest offset of an incomplete transaction and says it is used to compute LSO.

The field is interesting for this repository because it is **not application payload** and is not merely a performance counter. It represents retained unresolvedness: a prior transaction has not yet acquired a final decision, so later offset-ordered reading cannot yet treat the prefix beyond it as stable.

This produces the bounded relation:

```text
uncertainty retained about earlier transaction
        -> later bytes can exist
        -> later bytes can be replicated
        -> later bytes can still be withheld from READ_COMMITTED
```

No philosophical language is needed to establish that engineering relation.

---

### 5. Completed transaction processing — decision changes interpretation of earlier bytes

The bounded `Log.scala` defines a `CompletedTxn` with producer ID, transaction first offset, completion-marker offset, and aborted/committed classification.

When a completed transaction is appended, the implementation calls `ProducerStateManager.completeTxn`, gets the resulting LSO, and updates the segment transaction index. The source comment says the last offset visible under `READ_COMMITTED` is limited by the LSO and HW.

This is evidence that transaction completion changes the **admissibility relation** of data that was already appended earlier.

The completion operation does not need to rewrite the original payload bytes in order to change whether those bytes count as committed application history.

---

### 6. Transaction index — retained negative-decision evidence

The opening comment of `TransactionIndex.scala` explicitly says that the index retains metadata about aborted transactions for each segment, including transaction start/end offsets and the LSO at abort time, and that it is used for `READ_COMMITTED` fetches.

`collectAbortedTxns` finds aborted transactions overlapping a requested offset range. The serialized logical entry fields are:

```text
producerId
firstOffset
lastOffset
lastStableOffset
```

The index can be truncated, flushed, deleted with its segment, and rebuilt. The same source notes that because a transaction may span segments, recovery can require scanning earlier segments to rediscover its beginning.

This yields two separate conclusions:

1. **transaction index ≠ complete transaction history** — it is a bounded derived lookup structure;
2. **rebuildable metadata ≠ dispensable metadata** — the system still needs equivalent decision/range knowledge for correct `READ_COMMITTED` filtering.

---

### 7. Fetch path — application-level forgetting while bytes survive

For `READ_COMMITTED`, the broker gathers aborted transaction ranges from the transaction index and attaches them to fetch data. KIP-98's Fetch response adds both `LastStableOffset` and `AbortedTransactions` next to `HighwaterMarkOffset`.

The consumer-side KIP-98 implementation uses those ranges to skip aborted batches; control batches are not returned as ordinary records.

Therefore an ABORT is not modeled as:

```text
erase original bytes -> reader cannot find them
```

but rather:

```text
retain original bytes
+ retain transaction decision/range evidence
+ apply isolation filter
-> application does not receive them
```

That mechanism is the strongest reason to include this case in `technical-retention` rather than in a generic Kafka history.

---

### 8. Producer-state snapshot — recovery state is not payload state

`ProducerStateManager.scala` retains recent producer state including producer ID, epoch, last sequence, last offset, coordinator epoch, and `current_txn_first_offset` in a snapshot format. Recovery can combine snapshots with log scanning.

This is used only to support the bounded distinction:

> **correct future interpretation of the log depends on retained/reconstructible protocol state not reducible to user payload bytes.**

No claim is made that the producer-state snapshot alone is the transaction coordinator's authoritative durable state.

---

## Prior-art guardrail

### Database transactions and log-based recovery predate Kafka 0.11

The IBM Research record for Gray et al.'s 1981 System R recovery-manager paper describes a transaction concept in which applications can commit or abort effects and recovery uses records in a transaction log for undo/redo.

The safe historical boundary is therefore:

```text
transactions / commit / abort / transaction-log recovery
    existed decades before Kafka 0.11

Kafka 0.11 bounded contribution here
    = transaction semantics composed with an ordered replicated log,
      hidden control records,
      LSO read frontier,
      aborted-range index,
      and consumer-selectable isolation
```

No direct System R → Kafka genealogy is claimed.

---

## Mechanism reconstruction

### Open transaction

```text
append transactional records
        ↓
replicate them
        ↓
HW may pass their offsets
        ↓
transaction still open
        ↓
first unstable offset remains
        ↓
LSO stays behind
        ↓
READ_COMMITTED consumer waits at frontier
```

### Commit

```text
transaction coordinator decides COMMIT
        ↓
COMMIT markers written to participant logs
        ↓
local transaction state completes
        ↓
LSO may advance
        ↓
records become eligible for READ_COMMITTED delivery
```

### Abort

```text
transaction coordinator decides ABORT
        ↓
ABORT markers written
        ↓
index records aborted transaction range
        ↓
LSO may advance
        ↓
READ_COMMITTED fetch carries aborted-range evidence
        ↓
consumer discards those batches
```

The abort path is an example where **retention of a decision is required to preserve forgetting of retained data**.

---

## Claim classification

### Historical record (`H/P`)

Established from Apache sources:

- Kafka `0.11.0.0` supports transactional producer/consumer semantics;
- `READ_COMMITTED` and `READ_UNCOMMITTED` are distinct consumer modes;
- LSO is bounded by the first open transaction and may lag HW;
- COMMIT/ABORT are control records rather than ordinary application output;
- aborted-transaction metadata is indexed by log segment and returned for committed reads;
- producer/open-transaction metadata has explicit snapshot/replay support.

### Engineering reconstruction (`E`)

Supported:

- physical log presence is weaker than transactional read admissibility;
- HW and LSO represent different retained protocol boundaries;
- negative transaction decisions can be constitutive retention state;
- logical forgetting can require retaining evidence rather than deleting payload;
- one unresolved transaction can constrain later offset visibility;
- derived/rebuildable indexes remain semantically necessary as a relation even if their physical representation can be regenerated.

### Functional analogy (`A`)

Allowed with explicit limits:

- Case 56 HW: comparable as a frontier, not same criterion;
- Case 42 delete marker: comparable as negative evidence, not same semantics;
- Swift/Cassandra tombstones: comparable only in `negative evidence suppresses positive state` relation;
- Raft snapshot metadata: comparable only in `derived/materialized control state can replace/reconstruct another representation` relation.

### Philosophical interpretation (`I`)

Bounded interpretation:

- one physical inscription can participate in multiple operationally admissible histories depending on retained decision state and read rule;
- `forgotten for this interface` need not mean `physically absent`.

Rejected:

- Kafka isolation is literally historiography or human memory;
- abort is archival destruction;
- application invisibility entails forensic disappearance.

---

## Counterexamples and limits

### `committed transaction = delivered atomically to one consumer` — reject

KIP-98 itself discusses limitations: cross-partition transactions, seeks, topic retention/compaction, and consumer subscription geometry mean a transaction should not be imagined as one indivisible `poll()` result.

### `ABORT = erase` — reject

The implementation filters aborted records while the log can retain the original record batches. Secure erase/sanitization is a different layer handled elsewhere in the repository.

### `transaction index = transaction log` — reject

The segment-local transaction index is a derived lookup structure for aborted ranges. The KIP transaction log is a coordinator state store. They are distinct retained state classes.

### `LSO = HW` — reject

They can coincide when no earlier open transaction constrains visibility, but equality in one state does not make the concepts identical.

### `all Kafka 0.11 transaction behavior was final/correct` — reject

Later releases contain transaction fixes and defensive KIPs. This case intentionally stops at the exact `0.11.0.0` mechanism and does not backport later guarantees.

---

## Cross-case consequences

### Case 56 — replicated log

```text
Case 56:
    surviving/replicated suffix
        -> ISR progress
        -> high watermark
        -> replication-committed prefix

Case 63:
    replicated prefix
        + open/decided transaction state
        -> last stable offset
        + abort index/filter
        -> READ_COMMITTED history
```

Finding:

> **replication currentness and transaction decision are compositional retention layers, not interchangeable synonyms for `committed`.**

### Case 42 — log compaction

```text
Case 42 delete marker:
    newest keyed negative state
    -> old keyed versions cease to represent current state
    -> marker itself can later be removed after its retention horizon

Case 63 ABORT marker:
    transaction decision
    -> transaction's produced records never become READ_COMMITTED application history
```

Finding:

> **Kafka has more than one technical form of forgetting, even within an append-log family.**

### Cases 28/41 — distributed tombstones

The shared functional relation is:

```text
retain negative evidence
    so surviving positive data does not regain authority
```

But Swift/Cassandra solve replica-consistency/reconciliation problems, whereas Kafka 0.11 solves transaction-isolation visibility in an ordered log. No genealogy is implied.

---

## Findings promoted to CASE_INDEX

Numbered globally as findings **685–700**:

685. **high watermark ≠ last stable offset**;
686. **replication commitment ≠ transaction decision**;
687. **physically retained aborted record ≠ `READ_COMMITTED`-visible record**;
688. **transaction abort ≠ physical erasure**;
689. **negative decision evidence can sustain logical forgetting**;
690. **control-record invisibility ≠ control-state irrelevance**;
691. **first open transaction can constrain visibility of later offsets**;
692. **offset-order preservation can turn one open transaction into a partition-wide read frontier**;
693. **transaction index ≠ user payload**;
694. **transaction index ≠ complete transaction history**;
695. **rebuildable metadata ≠ dispensable metadata**;
696. **`READ_UNCOMMITTED` and `READ_COMMITTED` can expose different admissible histories from the same physical log**;
697. **replication-currentness state ≠ transaction-decision state**;
698. **transactional commit ≠ atomic consumer delivery as one indivisible read batch**;
699. **Kafka abort marker ≠ Kafka compaction tombstone**;
700. **Kafka 0.11 transactional isolation ≠ invention of transactions/atomic commit**.

---

## Sources

### Apache primary sources

- KIP-98: <https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging>
- Kafka `0.11.0.0` tag: <https://github.com/apache/kafka/tree/0.11.0.0>
- `ConsumerConfig.java`: <https://github.com/apache/kafka/blob/0.11.0.0/clients/src/main/java/org/apache/kafka/clients/consumer/ConsumerConfig.java>
- `ReplicaManager.scala`: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/server/ReplicaManager.scala>
- `Log.scala`: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/log/Log.scala>
- `TransactionIndex.scala`: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/log/TransactionIndex.scala>
- `ProducerStateManager.scala`: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/log/ProducerStateManager.scala>
- KAFKA-5121 transaction-index implementation commit: <https://github.com/apache/kafka/commit/e71dce89c0da50f3eccc47d0fc050c92d5a99b88>

### Prior art

- Jim Gray, Paul McJones, Mike Blasgen, Bruce Lindsay, Raymond Lorie, Tom Price, Franco Putzolu, Irving Traiger, `The Recovery Manager of the System R Database Manager`, *ACM Computing Surveys* 13(2), June 1981; IBM Research record: <https://research.ibm.com/publications/the-recovery-manager-of-the-system-r-database-manager>

---

## Maturity decision

Promote directly to **`grounded`** because the central mechanism does not depend on one fragile or retrospective source:

- exact Apache release-tag consumer semantics establish LSO/HW separation;
- exact broker/log source establishes LSO use and first-unstable transaction state;
- exact transaction-index source establishes retained aborted-range evidence;
- KIP-98 and its implementation commit establish the intended control-marker/fetch-isolation composition;
- System R literature blocks a false transaction-invention claim;
- existing Cases 42 and 56 provide bounded same-project counterexamples that prevent `Kafka committed`, `delete marker`, and `transaction abort` from being collapsed into one relation.

Future work should remain narrow: Kafka transaction-coordinator state-log recovery, later transaction correctness/defense evolution, Streams changelog/processing semantics, compaction interaction, independent fault injection, and cross-layer durability remain separate cases rather than hidden requirements for this one.
