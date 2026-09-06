from pathlib import Path
import re

synthesis_path = Path("docs/SYNTHESIS_14_DISTRIBUTED_ACK_VISIBILITY_DURABILITY.md")
if synthesis_path.exists():
    raise SystemExit("Synthesis 14 already exists; refusing duplicate integration")

synthesis = r'''# Synthesis 14 — Distributed Acknowledgement, Visibility, Replication, and Durable Commitment

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
'''
synthesis_path.write_text(synthesis, encoding="utf-8")

readme_path = Path("README.md")
readme = readme_path.read_text(encoding="utf-8")
if "SYNTHESIS_14_DISTRIBUTED_ACK_VISIBILITY_DURABILITY.md" in readme:
    raise SystemExit("README already links Synthesis 14")
anchor = "A bounded durability-handoff comparison is now available in [`docs/SYNTHESIS_13_DURABILITY_HANDOFF_PERSISTENCE_DOMAIN.md`](docs/SYNTHESIS_13_DURABILITY_HANDOFF_PERSISTENCE_DOMAIN.md)."
pos = readme.find(anchor)
if pos < 0:
    raise SystemExit("README Synthesis 13 anchor not found")
para_end = readme.find("\n\n", pos)
if para_end < 0:
    raise SystemExit("README Synthesis 13 paragraph end not found")
s14_para = (
    "A bounded distributed-acknowledgement/visibility comparison is now available in "
    "[`docs/SYNTHESIS_14_DISTRIBUTED_ACK_VISIBILITY_DURABILITY.md`]"
    "(docs/SYNTHESIS_14_DISTRIBUTED_ACK_VISIBILITY_DURABILITY.md). "
    "Across grounded RADOS, Kafka, and Chain Replication cases it separates local application, qualified replica membership, replication progress, protocol completion/currentness, acknowledgement/notification, reader-specific visibility, persistence-boundary arrival, failure-model qualification, and client knowledge. "
    "It fixes the counterexamples `acknowledged ≠ durable`, `replicated ≠ READ_COMMITTED-visible`, `service completed ≠ client knows`, and `same word committed ≠ same durability contract`."
)
readme = readme[:para_end] + "\n\n" + s14_para + readme[para_end:]
readme_path.write_text(readme, encoding="utf-8")

roadmap_path = Path("ROADMAP.md")
roadmap = roadmap_path.read_text(encoding="utf-8")
pattern = re.compile(r"^- \[ \] How should acknowledged, visible, replicated, and durably committed be separated across systems\?$", re.M)
replacement = (
    "- [x] How should acknowledged, visible, replicated, and durably committed be separated across systems? "
    "— bounded cross-case closure in [`docs/SYNTHESIS_14_DISTRIBUTED_ACK_VISIBILITY_DURABILITY.md`]"
    "(docs/SYNTHESIS_14_DISTRIBUTED_ACK_VISIBILITY_DURABILITY.md): grounded RADOS, Kafka, and Chain Replication cases now separate observer-specific acknowledgement, reader-specific visibility, qualified replica membership/progress, protocol completion/currentness, local persistence boundary, failure model, and client knowledge. Historical commit/ack genealogy, Paxos/Raft, Byzantine finality, geo-durability tiers, end-to-end filesystem/database composition, and empirical fault injection remain open."
)
roadmap, count = pattern.subn(replacement, roadmap)
if count != 1:
    raise SystemExit(f"ROADMAP distributed durability checkbox replacement count={count}")
roadmap_path.write_text(roadmap, encoding="utf-8")

case_index_path = Path("CASE_INDEX.md")
case_index = case_index_path.read_text(encoding="utf-8")
if "## Synthesis 14 — distributed acknowledgement / visibility / durability findings" in case_index:
    raise SystemExit("CASE_INDEX already contains Synthesis 14 findings")
if re.search(r"^1592\.", case_index, re.M):
    raise SystemExit("CASE_INDEX finding 1592 already allocated")
additions = r'''

## Synthesis 14 — distributed acknowledgement / visibility / durability findings

1592. **acknowledgement ≠ one universal retention threshold** — RADOS client acknowledgement, RADOS final commit notification, Chain Replication internal `ack(r)`, and client reply carry different observers and contracts; the message type must be identified before inferring retention strength.
1593. **acknowledged ≠ durably committed** — bounded 2006 RADOS can acknowledge after all replicating OSDs apply the update to volatile buffer caches and issue a later final notification only after safe disk commit.
1594. **replica multiplicity ≠ qualified replica set** — Kafka assigned replicas and current ISR membership are separate relations; intended replication factor does not by itself state how many replicas presently participate in the committed-prefix guarantee.
1595. **local append/application ≠ replication-qualified frontier** — a Kafka leader or Chain Replication upstream server can contain the update before the stronger high-watermark/tail-qualified service boundary has advanced.
1596. **replicated ≠ one binary predicate** — a defensible replication claim needs both the set of replicas that currently count and progress evidence showing how far that set has incorporated the update.
1597. **protocol commitment/currentness vocabulary ≠ local physical-media durability vocabulary** — Kafka 0.8.2 `committed` is grounded as an ISR/high-watermark relation; this synthesis does not silently reinterpret that historical term as synchronous physical-media flush on every broker.
1598. **replication commitment ≠ transactional `READ_COMMITTED` visibility** — Kafka 0.11 can place records below the replication high watermark while an open transaction keeps the last stable offset behind them.
1599. **physical record survival ≠ application-visible history** — aborted Kafka transactional records can remain in the replicated log while retained ABORT/index evidence causes `READ_COMMITTED` consumers to suppress them.
1600. **upstream replica application ≠ tail-qualified service completion** — Chain Replication permits an update to change upstream replicas while remaining pending until the tail processes it.
1601. **service-side completion ≠ client knowledge** — Chain Replication explicitly permits an update to have executed although the client did not receive the reply, so timeout/acknowledgement state cannot be substituted for the service event itself.
1602. **completion evidence can authorize forgetting temporary recovery state** — backward Chain Replication acknowledgements allow predecessors to retire `Sent_i` forwarding obligations without erasing the completed object update.
1603. **visibility ≠ one global property of retained bytes** — RADOS bounded visibility/synchronization, Kafka ordinary high-watermark reads, Kafka transactional LSO filtering, and Chain Replication tail queries expose different reader-admission rules over retained state.
1604. **replicated volatile state ≠ failure-qualified durable state** — RADOS demonstrates that redundancy across volatile OSD caches can still remain vulnerable to the simultaneous power-loss model that motivates its later disk-commit boundary.
1605. **distributed protocol guarantee + local persistence guarantee + failure-domain assumption must compose** — Synthesis 14 operates above Synthesis 13: multiplying replicas does not manufacture a stronger local persistence contract, while locally durable replicas still require distributed authority/currentness and read-admission rules.
1606. **same word `committed` across systems ≠ same contract or genealogy** — RADOS final disk `commit`, Kafka replicated-prefix `committed`, and transactional `READ_COMMITTED` visibility must remain source-bounded historical terms rather than flattened into one modern definition.
1607. **acknowledged / visible / replicated / durable ≠ universal temporal ladder** — the four relations can branch, couple, or lag differently by protocol; comparison must type observer, reader, replica qualification/progress, persistence boundary, and covered failure model.
'''
case_index = case_index.rstrip() + additions + "\n"
case_index_path.write_text(case_index, encoding="utf-8")

# Lightweight invariants before the workflow stages/commits.
for p in [synthesis_path, readme_path, roadmap_path, case_index_path]:
    data = p.read_text(encoding="utf-8")
    if "\r" in data:
        raise SystemExit(f"CRLF introduced in {p}")
    if data and not data.endswith("\n"):
        raise SystemExit(f"missing EOF newline: {p}")
if "SYNTHESIS_14_DISTRIBUTED_ACK_VISIBILITY_DURABILITY.md" not in readme_path.read_text(encoding="utf-8"):
    raise SystemExit("README navigation missing Synthesis 14")
if re.search(r"^- \[ \] How should acknowledged, visible, replicated, and durably committed be separated across systems\?$", roadmap_path.read_text(encoding="utf-8"), re.M):
    raise SystemExit("ROADMAP question remained unchecked")
if "1607. **acknowledged / visible / replicated / durable ≠ universal temporal ladder**" not in case_index_path.read_text(encoding="utf-8"):
    raise SystemExit("CASE_INDEX findings missing")
