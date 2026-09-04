# Apache Kafka 0.11 Transaction Coordinator State Recovery: Compacted Current State, Failover Reload, and Resumed Completion

## Scope

- **Bounded system:** Apache Kafka `0.11.0.0`, released 28 June 2017.
- **Bounded mechanism:** the transaction coordinator's internal transaction-state topic, its keyed transaction metadata, compacted current-state representation, in-memory coordinator cache, coordinator-partition leadership handoff, durable transition-before-cache-update rule, recovery of `PrepareCommit` / `PrepareAbort`, producer-epoch fencing, coordinator-epoch checks, and expiration tombstones for inactive transactional IDs.
- **Research question:** what must survive a transaction coordinator process or role change so that a transaction can continue to count as the same transaction, with the same already-chosen completion direction, without treating one broker's RAM as the authority?

This is **not** a general history of database transactions, two-phase commit, Kafka exactly-once semantics, Kafka Streams, idempotent sequence-number recovery, later transaction protocol hardening, KRaft, or post-0.11 coordinator redesign.

It is intentionally adjacent to, but distinct from:

- [Case 56](56-apache-kafka-replicated-log-high-watermark.md), which studies replication currentness and high-watermark visibility in Kafka 0.8.2;
- [Case 63](63-apache-kafka-transactional-read-visibility.md), which studies the user-log side of Kafka 0.11 transactions: LSO, COMMIT/ABORT control batches, aborted-range indexing, and `READ_COMMITTED` filtering.

Case 64 asks about the **coordinator's own retained control state**. Its bounded retention claim is:

> **Kafka 0.11.0.0 does not make one transaction coordinator process's memory the sole carrier of transaction identity or progress. Transaction metadata is written as keyed state into a replicated internal Kafka topic configured for compaction; a broker taking leadership for a transaction-state partition reconstructs its cache from that log, and a recovered `PrepareCommit` or `PrepareAbort` causes completion markers to be resumed. The same implementation updates its in-memory transaction state only after the corresponding state-log append succeeds and guards later work with coordinator and producer epochs. Thus process-local cache state, durable transaction state, completion work, and current authority are distinct retention relations.**

`retained coordination state`, `completion-direction retention`, and `recovery-obligation state` below are **project engineering terms**, not historical Kafka vocabulary.

---

## Historical vocabulary

The inspected Apache artifacts use:

- `Transaction Coordinator`;
- `Transaction Log` / transaction state topic;
- `transactionalId` / `TransactionalId`;
- `producerId` / PID;
- `producerEpoch`;
- `coordinatorEpoch`;
- transaction states `Empty`, `Ongoing`, `PrepareCommit`, `PrepareAbort`, `CompleteCommit`, `CompleteAbort`, `Dead`;
- `transaction metadata cache`;
- `cleanup.policy=compact`;
- `transaction.state.log.replication.factor`;
- `transaction.state.log.min.isr`;
- `required acks = -1` in the implementation;
- transaction-log tombstones represented by a keyed record with a null value.

Do not replace these with generic database terms such as `WAL`, `2PC coordinator log`, or `redo log` unless explicitly labeled as analogy. Kafka's design belongs in a much older family of transaction-recovery ideas, but the exact state machine and storage composition are Kafka-specific.

---

## Historical record

### H/P — Kafka 0.11.0.0 shipped on 28 June 2017

Apache's release archive dates `0.11.0.0` to 28 June 2017. The exact source tag is therefore the implementation boundary used below rather than current Kafka source.

**Primary/institutional anchor:** Apache Kafka downloads archive, `0.11.0.0` release entry.

### H/P — KIP-98 defines the Transaction Log as the coordinator's persistent replicated state store

KIP-98 introduces an internal Kafka `Transaction Log` and describes it as a persistent, replicated record whose latest-version snapshot encapsulates the current state of each active transaction. It also makes `TransactionalId` persistent across producer instances and says the mapping is logged so a later producer instance can recover or abort an incomplete transaction.

This is already enough to reject a process-local interpretation of transaction identity: a broker process can disappear while the transaction's coordination state remains reconstructible elsewhere.

**Primary anchor:** Apache Kafka KIP-98, `Key Concepts` and `Getting a producer Id`.

### H/P — the exact 0.11.0.0 transaction-log value is current transaction metadata, not user payload

`TransactionLog.scala` defines the key as `transactional_id`. Its value schema includes:

- producer ID;
- producer epoch;
- transaction timeout;
- transaction status;
- the set of topic partitions participating in the transaction;
- transaction-entry timestamp;
- transaction-start timestamp.

The same file configures the internal transaction topic with compaction, no compression, disabled unclean leader election, and required acknowledgements of `-1`; defaults include 50 partitions, replication factor 3, and minimum ISR 2.

These records are coordination state. They are not the application's produced records and they are not the COMMIT/ABORT control batches written to the participating user-topic partitions.

**Primary anchor:** `core/src/main/scala/kafka/coordinator/transaction/TransactionLog.scala`, tag `0.11.0.0`.

### H/P — durable state transition precedes the corresponding in-memory transition

`TransactionMetadata.scala` explicitly says the transaction metadata should be updated only after the corresponding transaction-log entry has been successfully written and replicated. `TransactionStateManager.appendTransactionToLog` implements this ordering: it serializes the proposed metadata, appends it to the internal transaction topic with the enforced acknowledgement setting, and only in the successful callback calls `completeTransitionTo` on the cached metadata.

The cache can therefore hold a **pending** transition while the system waits for the durable transition record. A prepared in-memory intention is not yet equivalent to a completed coordinator-state transition.

**Primary anchors:** `TransactionMetadata.scala`, `completeTransitionTo`; `TransactionStateManager.scala`, `appendTransactionToLog`, tag `0.11.0.0`.

### H/P — a broker that gains transaction-partition leadership reconstructs the coordinator cache from the log

`TransactionStateManager.loadTransactionMetadata` reads the transaction-state log partition and rebuilds a map indexed by `transactionalId`. A null value removes an ID; otherwise the decoded metadata replaces the prior value for that key in the loaded map. `loadTransactionsForTxnTopicPartition` installs that reconstructed map as the transaction metadata cache for the newly owned partition.

Conversely, when the broker becomes a follower for a transaction-state partition, `removeTransactionsForTxnTopicPartition` removes the corresponding cached transaction metadata.

The bounded implementation therefore treats the in-memory cache as **role-local materialization**, not as the only enduring representation of transaction state.

**Primary anchor:** `TransactionStateManager.scala`, `loadTransactionMetadata`, `loadTransactionsForTxnTopicPartition`, and `removeTransactionsForTxnTopicPartition`, tag `0.11.0.0`.

### H/P — recovered PREPARE state resumes completion instead of choosing again

After loading a transaction-state partition, the implementation inspects reconstructed transactions. If one is in `PrepareAbort`, it schedules ABORT markers; if one is in `PrepareCommit`, it schedules COMMIT markers. The code removes the partition from the `loading` set before sending those markers so the follow-up final transaction-log append is not blocked by coordinator-load state.

This makes the retained PREPARE state operationally consequential after coordinator handoff:

```text
recovered PrepareCommit
    -> resume COMMIT-marker propagation

recovered PrepareAbort
    -> resume ABORT-marker propagation
```

The recovery path is not documented as asking a new coordinator to re-evaluate application intent. The direction chosen before the failure survives as coordinator state and determines the remaining work.

**Primary anchor:** `TransactionStateManager.scala`, `loadTransactionsForTxnTopicPartition`, tag `0.11.0.0`.

### H/P — EndTxn persists PREPARE before marker propagation and final completion

The exact `TransactionCoordinator.handleEndTransaction` implementation transforms `Ongoing` to `PrepareCommit` or `PrepareAbort`, appends that new metadata through `appendTransactionToLog`, and sends transaction markers only after that append succeeds. It then prepares the final completion state while marker delivery proceeds.

KIP-98 describes the same high-level sequence: write PREPARE to the transaction log, write COMMIT/ABORT markers to participant logs, then write final COMMITTED/ABORTED state to the transaction log.

This ordering explains why PREPARE is a recovery boundary rather than a transient label.

**Primary anchors:** `TransactionCoordinator.scala`, `handleEndTransaction`, tag `0.11.0.0`; KIP-98 §5.1–5.3.

### H/P — coordinator epoch and producer epoch protect different authorities

`TransactionStateManager` tracks a coordinator epoch with the transaction-state partition's loaded cache entry. `appendTransactionToLog` checks that the coordinator epoch still matches before appending and again before committing the cache transition. Its source comment explicitly describes the danger of an old coordinator epoch appending after transaction-partition emigration/immigration.

Separately, `TransactionMetadata` stores a producer epoch. KIP-98 says a new producer instance with the same `TransactionalId` bumps that epoch to fence a previous zombie producer.

The two epochs must not be collapsed:

- **producer epoch** qualifies which producer generation may act for a `TransactionalId`;
- **coordinator epoch** qualifies which coordinator-partition ownership generation may continue coordinator work in the bounded implementation.

**Primary anchors:** `TransactionStateManager.scala`, `appendTransactionToLog`; `TransactionMetadata.scala`, producer-epoch transitions; KIP-98 `InitPidRequest`.

### H/P — transaction-state history is intentionally compactable

`TransactionStateManager.transactionTopicConfigs` forces `cleanup.policy=compact`. `loadTransactionMetadata` reconstructs current per-`TransactionalId` metadata by repeatedly replacing the loaded value for a key, which matches a latest-value state-store use rather than a requirement to keep every historical transition forever.

KIP-98 is explicit that after all participant markers are written and the final COMMITTED/ABORTED state is recorded, most messages for the transaction can be removed; only the completed transaction's PID plus timestamp need remain until the `TransactionalId`→PID mapping itself expires.

Thus the transaction coordinator needs durable **current coordination state**, but not an indefinitely complete transition history.

**Primary anchors:** `TransactionStateManager.scala`, `transactionTopicConfigs` and load path; KIP-98 §5.3.

### H/P — expiration uses a state-log tombstone and removes cache state only after the append succeeds

The 0.11.0.0 state manager periodically considers inactive transactional IDs in `Empty`, `CompleteCommit`, or `CompleteAbort`. For an eligible ID it prepares `Dead`, writes a keyed record with a null value to the internal transaction-state topic, and removes the ID from the in-memory cache only after the append callback reports success and the cached epoch/pending state still match.

This tombstone is a **different record and forgetting mechanism** from Case 63's ABORT control marker in a user-topic log:

- transaction-state tombstone: forget an expired coordinator mapping from the compacted internal state store;
- ABORT control marker: preserve the negative decision that a particular transaction's user records must not appear in `READ_COMMITTED` history.

**Primary anchor:** `TransactionStateManager.scala`, `enableTransactionalIdExpiration`, tag `0.11.0.0`.

---

## Retained state

The bounded mechanism contains several different retained objects and authority relations.

### 1. Transactional ID identity

`TransactionalId` is a user-stable identity intended to span producer sessions. It is the lookup key for coordinator metadata.

### 2. Transaction metadata record

The internal topic retains producer identity/epoch, transaction status, participant set, timeout, and timestamps. This record is coordinator control state rather than user payload.

### 3. Transaction-state topic replication

The coordinator state itself is stored through Kafka replication. A single coordinator process is replaceable because the state store has its own replicated durability regime.

### 4. In-memory metadata cache

The active coordinator keeps a fast materialized cache for the transaction-state partition it currently owns. It can be destroyed and reconstructed.

### 5. Completion-direction state

`PrepareCommit` and `PrepareAbort` preserve the direction of a transaction already entering completion. They determine which marker must be resumed after recovery.

### 6. Producer epoch

This qualifies which producer instance remains legitimate for the persistent `TransactionalId`.

### 7. Coordinator epoch / ownership generation

This guards current coordinator authority across transaction-state partition movement.

### 8. Expiration tombstone

A null-valued state-log record retires an inactive `TransactionalId` from the compacted current-state map after the configured inactivity horizon.

---

## Retention mechanism

A simplified normal completion path is:

```text
Ongoing transaction in coordinator cache
    -> prepare in-memory transition to PrepareCommit / PrepareAbort
    -> append proposed metadata to replicated __transaction_state log
    -> append succeeds
    -> complete cached transition
    -> send COMMIT / ABORT markers to participant logs
    -> write final CompleteCommit / CompleteAbort coordinator state
```

A simplified coordinator-handoff path is:

```text
broker A loses transaction-state partition leadership
    -> broker-A cache for that partition is discarded
    -> broker B gains leadership
    -> broker B scans/reconstructs current metadata from transaction-state log
    -> recovered current states populate broker-B cache
    -> recovered PrepareCommit / PrepareAbort state resumes matching marker work
    -> final completion can proceed without broker A's RAM
```

A simplified expiration path is:

```text
completed/empty transactionalId becomes inactive long enough
    -> prepare Dead transition
    -> append keyed null-value tombstone to transaction-state log
    -> append succeeds under current coordinator ownership
    -> remove transactionalId metadata from cache
    -> compaction may later remove superseded physical state-log records
```

---

## Engineering reconstruction

### E — coordinator RAM ≠ authoritative transaction-state persistence

The cache is necessary for current operation but reconstructible from the retained internal log. A process-local object can disappear without erasing the transaction's coordination identity or current state.

### E — process lifetime ≠ transaction lifetime

A transaction can cross broker/coordinator role changes because its current coordination state has a replicated representation independent of one process lifetime.

### E — pending state transition ≠ durable coordinator-state transition

The implementation can mark an intended transition as pending before the append; only the successful replicated-log append permits the cached metadata to complete that transition.

### E — PREPARE retention can preserve a future obligation

`PrepareCommit` or `PrepareAbort` does more than describe the past. On reload it tells the new coordinator what work remains: send the corresponding participant markers and drive the transaction to completion.

### E — resumed completion ≠ re-deciding the transaction

Recovery acts from the retained PREPARE direction. The source path does not turn a recovered `PrepareCommit` into a new vote between commit and abort.

### E — current transaction state ≠ complete transaction history

The compacted state log can preserve the latest state needed for continuation while discarding superseded transitions. Recoverability does not require an audit-complete history of every coordinator step.

### E — reconstructible cache ≠ optional durable state store

The fact that RAM can be rebuilt from the log makes the RAM representation disposable. It does not make the underlying current transaction metadata dispensable.

### E — producer epoch ≠ coordinator epoch

Both are fencing/currentness metadata, but they qualify different actors. One prevents an old producer generation from continuing; the other prevents stale coordinator ownership from safely mutating the transaction-state log/cache.

### E — durable state may preserve a decision while physical work remains incomplete

A transaction can durably be in `PrepareCommit` while COMMIT markers have not yet reached every participant. Decision-direction retention and completion-work completion are therefore separate.

### E — state-log compaction can be retention infrastructure rather than mere storage optimization

Because the coordinator's restart model wants the latest current state per `TransactionalId`, key compaction aligns the physical log with the logical state-store abstraction. It permits superseded transition records to disappear while preserving the currently authoritative value.

### E — transaction-state tombstone ≠ transaction ABORT marker

Both are negative-looking records, but one retires an inactive coordinator identity from an internal compacted state store while the other preserves a transaction outcome so user records remain excluded from committed reads.

### E — successful final transaction outcome ≠ permanent retention of all coordinator metadata

After completion, KIP-98 explicitly reduces what must remain; later inactivity permits the stable transactional-ID mapping itself to expire. Retention obligations change with transaction lifecycle state.

---

## Failure and recovery boundaries

### Coordinator process crash / role movement

The bounded mechanism addresses loss of the coordinator's in-memory cache by reconstructing from the internal transaction-state topic on partition leadership. This is not evidence that every arbitrary storage corruption of `__transaction_state` is recoverable.

### PREPARE-state interruption

`PrepareCommit` / `PrepareAbort` are specifically recoverable intermediate states in the inspected source. This is stronger than saying “Kafka retries transactions”: the source preserves which completion direction was already chosen.

### Stale coordinator

Coordinator epoch checks prevent a cache transition from blindly continuing after ownership has changed. This is an authority-currentness rule, not payload integrity checking.

### Zombie producer

Producer epoch fencing prevents a previous producer generation sharing the same `TransactionalId` from remaining equally authoritative. This is separate from coordinator failover.

### State-store loss

Neither KIP-98 nor the inspected code makes `TransactionalId` identity independent of the transaction-state store itself. Replication is part of the retention mechanism; loss beyond that failure envelope is not solved by the in-memory cache abstraction.

### Compaction

Compaction is safe only relative to the state-store semantics that retain the current keyed value/tombstone as required. This case does not claim that arbitrary deletion of transaction-state records is safe.

---

## Functional analogies and limits

### A — Bigtable current-state recovery (Case 57)

Both systems can reconstruct volatile serving/control state from durable records and can make older history less necessary once a current materialization is established. But Bigtable's memtable/SSTable/redo composition and Kafka's compacted `TransactionalId` state store are different mechanisms and historical lineages.

### A — Raft snapshotting (Case 58)

Both can discard older authoritative history while preserving enough current state to continue. Kafka 0.11 transaction-state compaction is keyed latest-value log cleaning; Raft snapshotting replaces a committed consensus prefix with a state-machine snapshot plus boundary metadata. Do not collapse them.

### A — Kafka user-log compaction (Case 42)

Both use Kafka log compaction, but the retained objects differ. Case 42 studies application/key current-state reconstruction and delete-marker retention in ordinary compacted topics. Case 64 studies Kafka's internal transaction-coordinator state store and its role in transaction recovery.

### A — Kafka ABORT visibility (Case 63)

Case 63's ABORT marker is participant-log evidence needed to exclude user payload from `READ_COMMITTED` history. Case 64's transaction-state record is coordinator state needed to recover and continue the transaction protocol. They are linked by one transaction but are not the same retained record.

### A — database recovery logs

There is a broad functional analogy to older transaction managers that retain log state so commit/abort and recovery survive process failure. This is **not** a novelty claim for Kafka. System R and later distributed database systems predate Kafka by decades.

---

## Prior art and novelty boundary

The historical novelty claim must remain narrow.

Jim Gray and colleagues' 1981 System R recovery-manager paper already describes transactions that commit or abort, transaction-log records, and undo/redo recovery. Distributed atomic-commit and coordinator recovery also long predate Kafka. Therefore:

> **Kafka 0.11 did not invent transaction logs, commit/abort recovery, persistent transaction identifiers, or distributed atomic commitment.**

The bounded historical contribution documented here is the **Kafka-specific 0.11 composition**:

- `TransactionalId`-keyed coordinator state;
- a replicated internal Kafka topic used as that state store;
- compacted latest-value semantics;
- transaction state including participant partitions and producer epoch;
- durable PREPARE before marker fan-out;
- reload of the current state on transaction-partition leadership;
- resumption of COMMIT/ABORT marker work from recovered PREPARE state;
- separate producer and coordinator fencing/currentness mechanisms;
- tombstone retirement of inactive transaction identities.

That is enough for a retention case without an invention-priority claim.

---

## Philosophical interpretation

### I — retention can preserve an unfinished obligation, not only a finished fact

The interesting retained object here is sometimes neither a user payload nor a completed outcome. `PrepareCommit` and `PrepareAbort` preserve a **protocol obligation still owed to the future**. A later coordinator reads a state produced in the past and is constrained to continue the already-selected completion path.

This supports a narrow project-level observation:

> technical retention can make an unfinished obligation available to a future operator/process as an admissible continuation.

The mechanism does not require calling Kafka's transaction state “memory” in a human or philosophical sense.

### I — identity can survive replacement of the active interpreter

The coordinator process is replaceable, but `TransactionalId` plus retained protocol state let a successor process treat the reconstructed transaction as the same ongoing coordination object. The identity relation is therefore not process identity.

Again, this is an engineering-philosophical interpretation of the documented mechanism, not Kafka's own conceptual vocabulary.

---

## Rejected or unsupported claims

### X — “the coordinator cache is the durable transaction record”

Rejected. The exact source reconstructs the cache from the internal transaction-state log on ownership.

### X — “PREPARE is merely an in-memory transient state”

Rejected for the bounded path. PREPARE metadata is appended to the transaction-state log before marker fan-out and is explicitly resumed on reload.

### X — “coordinator epoch and producer epoch are the same fence”

Rejected. They qualify different roles/generations.

### X — “Kafka compaction preserves a complete transaction audit trail”

Rejected. The design explicitly allows superseded transaction-log records to be removed after current completion state is established.

### X — “transaction-state tombstone physically erases all traces of the transaction”

Rejected. It retires the keyed mapping from the internal compacted state store; physical log cleaning is later, and participant/user logs have distinct retention rules.

### X — “Case 64 proves transaction recovery under every Kafka failure mode”

Rejected. This case is bounded to the `0.11.0.0` state-store/cache/leadership recovery path and its documented failure envelope.

---

## Source map

### Primary / contemporary implementation and design

1. Apache Kafka, tag `0.11.0.0`, `TransactionStateManager.scala`: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/coordinator/transaction/TransactionStateManager.scala>
2. Apache Kafka, tag `0.11.0.0`, `TransactionLog.scala`: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/coordinator/transaction/TransactionLog.scala>
3. Apache Kafka, tag `0.11.0.0`, `TransactionMetadata.scala`: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/coordinator/transaction/TransactionMetadata.scala>
4. Apache Kafka, tag `0.11.0.0`, `TransactionCoordinator.scala`: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/coordinator/transaction/TransactionCoordinator.scala>
5. Apache Kafka, KIP-98, _Exactly Once Delivery and Transactional Messaging_: <https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging>
6. Apache Kafka downloads archive, release date for `0.11.0.0`: <https://kafka.apache.org/community/downloads/>

### Prior art / novelty boundary

7. Jim Gray et al., _The Recovery Manager of the System R Database Manager_, **ACM Computing Surveys** 13(2), June 1981: <https://research.ibm.com/publications/the-recovery-manager-of-the-system-r-database-manager>

### Related repository check

`tmzncty/computing-archaeology` was searched before writing this case for Kafka transaction-coordinator / `__transaction_state` coverage. No dedicated case was found, so this file keeps the discussion retention-specific rather than duplicating a pre-existing technical history.

---

## Status

**grounded**

The central mechanism is supported by exact Apache `0.11.0.0` release-tag source plus KIP-98, with System R used only to block an invention-priority claim. Future work should treat post-0.11 transaction-protocol evolution, KRaft coordinator redesign, independent failure injection, Streams exactly-once processing state, and transaction-state-store corruption/compliance as separate slices.
