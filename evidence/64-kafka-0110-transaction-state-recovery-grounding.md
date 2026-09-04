# Grounding Record — Kafka 0.11 Transaction Coordinator State Recovery

## Case

[`cases/64-apache-kafka-transaction-coordinator-state-recovery.md`](../cases/64-apache-kafka-transaction-coordinator-state-recovery.md)

## Promotion decision

**Status: `grounded`.**

The bounded claims are grounded by exact Apache Kafka `0.11.0.0` release-tag source for the transaction coordinator, transaction-state manager, transaction metadata, and transaction-log schema/configuration. KIP-98 supplies the period design vocabulary and intended cross-session recovery contract. Earlier System R recovery literature is used as prior art so Kafka is not credited with inventing transaction logging or commit/abort recovery.

The evidence is strong enough to establish the case without claiming later Kafka semantics or independent fault-injection validation.

---

## Source ledger

### P1 — Apache Kafka `0.11.0.0` `TransactionStateManager.scala`

URL: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/coordinator/transaction/TransactionStateManager.scala>

**Directly supports:**

- the state manager owns a special internal transaction log, transaction metadata, and expiration logic;
- transaction-state topic configs force `cleanup.policy=compact`, no compression, disabled unclean leader election, and use the configured minimum ISR;
- `transactionalId` hashes to a transaction-state topic partition;
- a newly owned transaction-state partition is read to reconstruct a per-`transactionalId` metadata map;
- null values remove IDs during reconstruction;
- `PrepareAbort` and `PrepareCommit` loaded from the log cause ABORT/COMMIT completion markers to be resumed;
- a broker losing transaction-state partition ownership removes the corresponding cached metadata;
- state-log append success is checked before the cache transition completes;
- coordinator epoch is checked around append/cache update;
- expiration writes null-valued transaction-log records and removes cache state only after successful append.

**Does not by itself support:**

- that every possible `__transaction_state` corruption is recoverable;
- later KRaft transaction coordinator behavior;
- independent production fault-injection success rates.

### P2 — Apache Kafka `0.11.0.0` `TransactionLog.scala`

URL: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/coordinator/transaction/TransactionLog.scala>

**Directly supports:**

- key = `transactional_id`;
- value fields for producer ID, producer epoch, timeout, transaction status, participant partitions, and timestamps;
- defaults of 50 transaction-log partitions, replication factor 3, minimum ISR 2;
- enforced `acks=-1`, compaction, no compression, and disabled unclean leader election in the bounded implementation;
- null value as transaction-log tombstone on decode.

**Boundary:** these are coordinator metadata records, not application transaction payload records or participant COMMIT/ABORT control batches.

### P3 — Apache Kafka `0.11.0.0` `TransactionMetadata.scala`

URL: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/coordinator/transaction/TransactionMetadata.scala>

**Directly supports:**

- transaction states `Empty`, `Ongoing`, `PrepareCommit`, `PrepareAbort`, `CompleteCommit`, `CompleteAbort`, `Dead`;
- producer ID and producer epoch as retained metadata;
- pending transition state;
- the implementation comment that metadata transition should be applied only after the corresponding log entry is successfully written and replicated;
- producer-epoch increment/fencing behavior in the bounded state machine.

**Boundary:** producer epoch is not the same thing as coordinator epoch.

### P4 — Apache Kafka `0.11.0.0` `TransactionCoordinator.scala`

URL: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/coordinator/transaction/TransactionCoordinator.scala>

**Directly supports:**

- `EndTxn` turns `Ongoing` into `PrepareCommit` or `PrepareAbort` according to the requested result;
- that PREPARE transition is appended through the state manager before marker work begins;
- marker fan-out follows successful state-log append;
- the coordinator can respond after the prepared transition has been durably appended and continue marker work asynchronously;
- coordinator epoch is checked again before continuing under the cached ownership generation;
- timed-out ongoing transactions are driven toward ABORT by the coordinator's background task.

**Boundary:** this case does not generalize timeout behavior to later versions.

### P5 — Apache Kafka KIP-98, _Exactly Once Delivery and Transactional Messaging_

URL: <https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging>

Relevant anchors:

- `Key Concepts`: Transaction Coordinator; persistent replicated Transaction Log; current-state snapshot of active transactions; persistent `TransactionalId`; producer epoch;
- `Getting a producer Id`: log the TransactionalId→PID mapping; bump epoch; recover or abort incomplete prior transaction;
- `AddPartitionsToTxnRequest`: participant set is logged so completion markers can later be written;
- `EndTxnRequest`: PREPARE state is written before COMMIT/ABORT marker fan-out;
- `Writing the final Commit or Abort Message`: final state written after participant markers; most transaction-log messages may then be removed.

**Provenance caution:** the Apache wiki page has received later editorial updates. Exact 2017 implementation claims therefore rely primarily on the `0.11.0.0` tag source; KIP-98 is used for design vocabulary and the documented proposal/guarantee boundary.

### P6 — Apache Kafka downloads archive

URL: <https://kafka.apache.org/community/downloads/>

**Directly supports:** `0.11.0.0` release date = **28 June 2017**.

### S/Prior-art — Gray et al., System R recovery manager, 1981

IBM Research record: <https://research.ibm.com/publications/the-recovery-manager-of-the-system-r-database-manager>

The IBM/ACM record describes transactions that commit, abort, or partially undo effects and states that transaction undo/redo are based on records kept in a transaction log.

**Use here:** novelty boundary only. It blocks claims such as `Kafka invented transaction logs`, `Kafka invented commit/abort recovery`, or `Kafka first made transaction state survive process failure`.

---

## Claim-to-evidence matrix

| Claim | Type | Evidence | Strength / limit |
| --- | --- | --- | --- |
| transaction coordinator current state is retained in an internal Kafka transaction log rather than only process RAM | H/P | P1, P2, P5 | direct design + exact source |
| transaction metadata is keyed by `transactionalId` and contains producer/status/participant/timing state | H/P | P2 | exact schema |
| transaction-state topic uses compaction and replication-oriented settings | H/P | P1, P2, P5 | exact source; not a claim of invulnerability |
| cache is reconstructed when a broker gains transaction-state partition leadership | H/P | P1 | exact load path |
| cached state is removed when ownership is lost | H/P | P1 | exact follower transition path |
| cache transition completes only after successful state-log append | H/P | P1, P3 | explicit implementation ordering |
| recovered `PrepareCommit` / `PrepareAbort` resumes matching marker work | H/P | P1 | exact reload path |
| PREPARE precedes marker fan-out in normal EndTxn flow | H/P | P4, P5 | implementation + KIP agreement |
| producer epoch and coordinator epoch protect different authority relations | H/P + E | P1, P3, P5 | exact separate fields/uses; project comparison is reconstruction |
| current coordinator state does not require retention of all past transition records | H/P + E | P1, P5 | compaction + KIP explicit removal after completion |
| expired transaction-state mapping is removed using an internal-log tombstone | H/P | P1 | exact source |
| transaction-state tombstone ≠ participant ABORT marker | E/A | P1, P4, P5 + Case 63 | direct mechanisms differ; comparison is project analysis |
| coordinator process lifetime ≠ transaction lifetime | E | P1, P5 | follows from reload and cross-session contract |
| PREPARE retention can preserve a future completion obligation | E/I | P1, P4 | mechanism grounded; terminology is project-level |
| Kafka 0.11 did not invent transaction-log recovery | X/prior art | System R 1981 | strong chronology boundary |

---

## Important negative evidence / non-claims

1. **No claim of exhaustive Kafka transaction history.** The slice is `0.11.0.0` only.
2. **No claim that compaction preserves audit history.** The opposite is important: current state can survive after superseded transition records are discarded.
3. **No claim that a transaction-state tombstone sanitizes physical media.** It is a keyed logical deletion in a compacted Kafka log.
4. **No claim that producer epoch equals coordinator epoch.** They have different objects of authority.
5. **No claim that user-topic ABORT marker equals state-topic tombstone.** Case 63 and Case 64 require these negative states to remain distinct.
6. **No claim of independent fault-injection compliance.** The mechanism is grounded in Apache design/source, not a third-party crash campaign against a named deployment.
7. **No claim of Kafka invention priority for logging, commit/abort, recovery, or distributed atomic commit.**

---

## Cross-case consequences

This case adds the following retention distinctions to the repository:

- **coordinator cache ≠ durable coordinator state**;
- **process lifetime ≠ transaction lifetime**;
- **pending transition ≠ durably admitted transition**;
- **durably retained PREPARE direction ≠ completed participant work**;
- **resumed completion ≠ re-deciding transaction outcome**;
- **current transaction state ≠ full transaction transition history**;
- **producer epoch ≠ coordinator epoch**;
- **transaction-state tombstone ≠ user-topic ABORT marker**;
- **compaction of coordinator state ≠ secure erasure**;
- **retained protocol state can encode unfinished future obligations**.

These relations are compatible with Case 42's keyed log compaction, Case 56's replication frontier, Case 57's durable-state-to-volatile-materialization recovery, Case 58's history-to-snapshot transition, and Case 63's transaction-sensitive user-log visibility, but none of those cases is a substitute for the coordinator recovery mechanism documented here.

---

## Related-repository check

A search of `tmzncty/computing-archaeology` for Kafka transaction coordinator / transaction-state coverage returned no dedicated case. The broader history of database recovery, transaction processing, and message brokers should be routed there if expanded; `technical-retention` keeps only the bounded question of what transaction state must survive coordinator replacement and why.

---

## Remaining work intentionally left open

- post-0.11 transaction coordinator evolution and correctness fixes;
- KRaft-era transaction coordinator/state-store redesign;
- independent crash/failover fault injection against a reproducible Kafka 0.11 cluster;
- interaction with Kafka Streams state/changelog restoration;
- detailed transaction-timeout failure campaigns;
- transaction-state topic corruption/loss beyond normal replication assumptions;
- operational/commercial evidence for exact failure envelopes.

None is required to ground this bounded 2017 mechanism.
