# Synthesis 14 — Distributed Acknowledgement, Visibility, Replication, and Durable Commitment

## Scope

This is a **bounded cross-case engineering synthesis**, not a new historical case and not a genealogy of distributed storage, replication, consensus, acknowledgements, or transaction processing.

It closes one relation-decomposition question already present in the roadmap:

> How should `acknowledged`, `visible`, `replicated`, and `durably committed` be separated across systems?

The comparison is built only from already-grounded repository cases:

- [Case 05 — 2006 RADOS replicated objects](../cases/05-rados-replicated-object-repair.md);
- [Case 56 — Kafka 0.8.2 replicated-log high watermark](../cases/56-apache-kafka-replicated-log-high-watermark.md);
- [Case 63 — Kafka 0.11 transactional read visibility](../cases/63-apache-kafka-transactional-read-visibility.md);
- [Case 81 — OSDI 2004 Chain Replication](../cases/81-chain-replication-tail-currentness-reconfiguration.md).

Historical claims remain owned by those case/evidence records. The relation names introduced here are **project engineering vocabulary (`E`)** unless explicitly identified as historical vocabulary. Similarity is functional comparison, not evidence of protocol descent.

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for acknowledgement/replication/commit/visibility combinations and for Chain Replication found no dedicated overlapping case in the current search surface. A broader history of replicated storage or distributed commit vocabulary belongs there if later developed; this document keeps only the retention-specific decomposition.

---

## Why the four words cannot form one universal ladder

Distributed-storage prose often compresses several different questions into a sentence such as `the write was acknowledged and replicated, so it is committed and visible`. The grounded cases show that this is unsafe.

The predicates can refer to different actors and different boundaries:

- **acknowledged to whom?** A downstream replica, an upstream server, a client, or an application?
- **visible through which read rule?** A primary read, a tail read, an ordinary Kafka consumer, or a `READ_COMMITTED` consumer?
- **replicated across which qualified set?** Every assigned replica, the current ISR, every chain member reached so far, or volatile caches on all current RADOS OSDs?
- **committed under which historical vocabulary?** Kafka's replicated-prefix `committed` relation is not automatically the same contract as RADOS's later disk `commit` notification.
- **durable against which failure?** One server failure, process restart, simultaneous power loss, controller loss, or something stronger?

The synthesis therefore does **not** propose the universal pipeline:

```text
acknowledged -> visible -> replicated -> durable
```

Instead it treats each word as a typed relation whose subject, observer, replica qualification rule, persistence boundary, and failure model must be stated.

---

## Historical records kept separate

### RADOS 2006 — client acknowledgement can precede final disk commit

Case 05 grounds an unusually explicit separation. In the 2006 Ceph/RADOS design, the primary forwards an update to the OSDs replicating the object. The paper describes an acknowledgement after the update has been applied to the in-memory buffer caches of the replicating OSDs, while a later final `commit` notification is sent only after the data has safely reached disk.

The authors separately identify two client concerns: making the update visible quickly for synchronization and knowing that it is safely replicated on disk. The prototype client therefore retains writes locally until final commit so acknowledged updates can be replayed after a simultaneous power loss affecting all OSDs in the placement group.

For this bounded historical regime:

```text
ordered / replicated into OSD volatile caches
    -> client acknowledgement and visibility milestone
    -> later disk commit notification
```

This is direct counterevidence to `acknowledged = durable on final media`.

It must not be projected onto modern Ceph releases.

### Kafka 0.8.2 — physical append, assigned replicas, ISR qualification, high watermark, and consumer exposure are different relations

Case 56 grounds a different architecture and vocabulary. A record can exist in the leader log before every in-sync follower has reached it. The leader computes the high watermark from progress of the current ISR, and ordinary consumer reads are bounded by that watermark.

The case therefore separates:

```text
record exists on leader
    !=
record exists on every assigned replica
    !=
current ISR has reached the prefix
    !=
ordinary consumer is admitted through the high-watermark boundary
```

Kafka 0.8.2 itself calls messages `committed` when all in-sync replicas have applied them to their logs. That historical word must stay attached to Kafka's own replication/currentness contract. This synthesis does **not** silently upgrade it into a claim that every participating disk has synchronously completed a physical-media flush.

The same case also shows that intended replication factor is weaker than current replication qualification: assigned replica membership and ISR membership are not synonyms.

### Kafka 0.11 — replication commitment can still be weaker than transactional visibility

Case 63 supplies a direct counterexample to `committed prefix = every committed-mode reader may now see the bytes`.

Kafka 0.11 retains both the replication high watermark and a transaction-sensitive last stable offset (LSO). A transactional batch can lie below the high watermark while an earlier/open transaction still constrains the LSO. `READ_COMMITTED` consumers stop at the LSO and also suppress aborted transactional ranges using retained transaction-decision evidence.

Thus:

```text
physically appended
    -> replication-qualified below high watermark
    -> transaction decision / stability qualification
    -> READ_COMMITTED admissibility
```

An ABORT can leave the record bytes physically present while making them intentionally invisible to `READ_COMMITTED` application history. Visibility is therefore not a monotonic synonym for physical survival or replication.

### Chain Replication 2004 — upstream application, tail-qualified completion, acknowledgement propagation, and client knowledge can separate

Case 81 uses another strong-consistency design. Updates enter at the head and can already have changed upstream replicas while remaining in `Pending` relative to the tail. The paper's client-view completed history is tied to tail processing; queries go to the tail.

After the tail processes an update, `ack(r)` travels backward. Each predecessor can then remove the request from its retained `Sent_i` forwarding-obligation state. The paper also explicitly allows the case where an update has executed even though the client did not receive its reply and therefore retries after timeout.

The bounded relations are therefore distinct:

```text
upstream replica has applied update
    !=
tail-qualified service completion
    !=
upstream receipt of backward completion acknowledgement
    !=
client knowledge that completion occurred
```

Case 81 deliberately does not claim that tail completion or `ack(r)` is a stable-media `fsync` guarantee below each server. The protocol's consistency/completion boundary and each server's local persistence medium remain separate questions.

---

## Engineering reconstruction: nine typed relations

The following types are analytical. A given protocol may merge some of them, omit others, or expose a different order.

### 1. Local application / embodiment

Has some server or replica incorporated the update into its local state?

This is the weakest relation in these examples. Chain Replication upstream servers and a Kafka leader can contain new state before the stronger service frontier has advanced.

### 2. Replica-set membership

Which physical/logical replicas are intended to participate?

Kafka assigned replicas, Kafka ISR, RADOS current PG membership, and Chain Replication chain roles are not interchangeable membership predicates. A multiplicity count without qualification can overstate the current retention margin.

### 3. Replication progress / coverage

How far has the selected qualified replica set actually incorporated the update?

This can be represented by follower log-end offsets, serial propagation toward a tail, or completion at multiple replica caches. `replicated` therefore needs both a **set** and a **progress boundary**.

### 4. Service-side completion frontier

At what protocol event does the service itself treat the operation as completed/current for the relevant semantics?

Examples include Chain Replication tail processing and Kafka's high-watermark advancement. These are different mechanisms and historical vocabularies.

### 5. Acknowledgement / notification relation

What observer has received evidence of which event?

RADOS client acknowledgement, RADOS final commit notification, Chain Replication's internal backward `ack(r)`, and a client reply are different messages with different meanings. The noun `ack` is not a durability type by itself.

### 6. Read-admission / visibility relation

Which reader is allowed to observe the update now?

RADOS's bounded 2006 design couples its early acknowledgement with one visibility/synchronization milestone. Kafka 0.8.2 ordinary consumers are bounded by the high watermark. Kafka 0.11 `READ_COMMITTED` adds the LSO and abort filtering. Chain Replication sends queries to the tail.

`visible` must therefore name an interface and admission rule.

### 7. Persistence-boundary / durable-commit relation

Has the update crossed a boundary that the historical system explicitly treats as persistent for a stated failure model?

RADOS 2006 supplies a clear example with its later safe-on-disk commit notification. The Kafka and Chain Replication cases in this synthesis are **not** promoted to an equivalent physical-media durability claim unless their own bounded evidence establishes one.

This preserves the important rule:

> **protocol commitment/currentness vocabulary is not automatically storage-media durability vocabulary.**

### 8. Failure-model qualification

What failure can the stronger relation survive?

RADOS's distinction is motivated partly by simultaneous power loss across the replicating OSDs. Kafka ISR/high-watermark semantics concern qualified replicated history and failover rules. Chain Replication assumes fail-stop storage servers and explicitly leaves the local storage-media durability layer outside the case.

A guarantee cannot be compared without carrying its failure envelope.

### 9. Client/application knowledge

Does the caller know that the relevant service/durability event occurred?

Chain Replication's lost-reply warning proves that service-side execution and client knowledge can diverge. A timeout therefore does not prove non-execution, just as a successful early acknowledgement in RADOS does not prove later disk commit.

---

## Counterexample matrix

| Shortcut | Counterexample from grounded cases | Correct boundary |
| --- | --- | --- |
| `acknowledged = durable` | RADOS early ack precedes final disk commit | acknowledgement type must name its persistence boundary |
| `replica count = current replicated state` | Kafka assigned replicas can differ from ISR | intended membership != current qualified set |
| `local append = committed prefix` | Kafka leader can be ahead of ISR high watermark | local embodiment != replication-qualified frontier |
| `replication committed = READ_COMMITTED visible` | Kafka 0.11 LSO can lag HW | replication frontier != transaction/read-admission frontier |
| `physically retained = application visible` | aborted Kafka records remain in log but are filtered | payload survival != admissible application history |
| `applied on several replicas = service completed` | Chain Replication update can remain pending before tail processing | partial propagation != tail-qualified completion |
| `service completed = client knows` | Chain Replication permits lost reply after execution | completion event != observer knowledge |
| `committed means the same thing everywhere` | Kafka `committed` and RADOS final `commit` name different contracts | preserve system-specific historical vocabulary |
| `replicated = durable against power loss` | RADOS can replicate in volatile OSD caches before disk commit | redundancy location/class and failure model matter |

---

## A diagnostic relation map

A safer cross-system checklist is:

```text
new logical update
    ↓
local embodiment/application on one or more members
    ↓
qualified replica membership + progress evidence
    ↓
protocol-specific completion/currentness frontier
    ├── acknowledgement / notification to some observer
    ├── read-admission / visibility rule for some reader
    └── possibly a stronger persistence-boundary transition
            ↓
       failure-model-qualified durability

separately:
client/application knowledge of any of the above
```

The branches matter. Acknowledgement, visibility, and persistence need not occur in one fixed order, need not be emitted by one component, and need not carry the same failure guarantee.

---

## Cross-case comparison with Synthesis 13

[Synthesis 13](SYNTHESIS_13_DURABILITY_HANDOFF_PERSISTENCE_DOMAIN.md) decomposes durability **inside storage interfaces and persistence domains**: command/store completion, cache/buffer residence, explicit persistence control, ordering, failure-triggered transfer, atomicity, recovery, and higher-layer closure.

This synthesis operates one layer outward. It asks how a **distributed protocol** qualifies replica participation, progress, completion, acknowledgement, and reader visibility before or alongside any local persistence boundary.

The two syntheses should compose, not replace one another:

```text
distributed protocol relation
    +
per-member/local persistence relation
    +
failure-domain assumptions
    =
actual end-to-end durability claim
```

A distributed replication protocol cannot manufacture a stronger local media guarantee merely by multiplying copies; conversely, locally persistent replicas still require authority/currentness and read-admission rules to define one distributed retained object.

---

## Historical, analogy, and philosophical boundaries

### Historical record

No new historical event is asserted here. Dates, mechanisms, and historical vocabulary remain sourced by Cases 05, 56, 63, and 81 and their evidence records.

### Engineering reconstruction

The nine typed relations and diagnostic maps are project-level decompositions derived from those grounded mechanisms. They are not claimed as terminology used by Ceph, Kafka, or the Chain Replication authors.

### Functional analogy

The cases are compared only where they solve a shared function: deciding when an update has progressed far enough, which replicas count, who may observe it, what evidence can retire temporary obligations, and what stronger failure guarantee has actually been earned.

### Philosophical interpretation

No new Stieglerian, Heideggerian, Ernstian, or Kirschenbaum-style thesis is asserted. At most, the cases discipline a later philosophical question: technical `having occurred` is often relation-specific rather than one timeless property. That observation remains downstream of the engineering distinctions.

---

## What this synthesis does not close

The following remain open:

- a historical genealogy of `commit`, `ack`, quorum, primary/backup, and replicated-log vocabulary;
- Paxos/Raft quorum-commit semantics as a separate bounded comparison;
- Byzantine/fork-aware acknowledgement and finality;
- geo-replication latency and durability tiers;
- end-to-end composition with filesystem/database `fsync`, WAL, or transaction commit;
- protocol behavior under network partitions beyond the bounded source models;
- empirical fault-injection showing exactly which acknowledged states survive which real power/controller/node failures;
- probabilistic durability claims for independent versus correlated failure domains.

These are deliberately not inferred from four grounded cases.

---

## Bounded result

The roadmap question can be closed only at this level:

> **`acknowledged`, `visible`, `replicated`, and `durably committed` are not four labels for one event and do not form one universal temporal ladder. A defensible retention claim must type at least the observer receiving acknowledgement, the reader/interface receiving visibility, the qualified replica set and progress frontier supplying replication, the persistence boundary supplying durability, and the failure model under which that boundary is meant to hold.**

The strongest counterexamples are deliberately asymmetric:

- RADOS: replicated volatile-cache acknowledgement can precede safe-on-disk commit;
- Kafka 0.8.2: a local/assigned replica state can exist beyond the ISR-qualified consumer-visible high-watermark prefix;
- Kafka 0.11: replication commitment can precede transactional `READ_COMMITTED` visibility;
- Chain Replication: upstream application can precede tail-qualified completion, and service execution can precede successful client knowledge.

That is a bounded engineering synthesis, not a universal theory of distributed durability.
