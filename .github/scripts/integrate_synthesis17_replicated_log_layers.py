from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"anchor missing in {path}: {old[:120]!r}")
    if text.count(old) != 1:
        raise SystemExit(f"anchor not unique in {path}: {old[:120]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


def append_once(path: str, marker: str, block: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8").rstrip() + "\n"
    if marker in text:
        raise SystemExit(f"marker already present in {path}: {marker}")
    p.write_text(text + "\n" + block.strip() + "\n", encoding="utf-8")


def normalize(path: str) -> None:
    p = Path(path)
    p.write_text(p.read_text(encoding="utf-8").rstrip() + "\n", encoding="utf-8")


doc_path = Path("docs/SYNTHESIS_17_REPLICATED_LOG_SUFFIX_CURRENTNESS_VISIBILITY.md")
if doc_path.exists():
    raise SystemExit(f"refusing to overwrite existing {doc_path}")

doc = r'''# Synthesis 17 — Replicated-Log Suffix Survival, Currentness, Visibility, and Truncation Authority

## Status and scope

**Bounded engineering synthesis over already-grounded Apache Kafka cases.** This document closes one explicit ROADMAP question:

> In a replicated log, how should physical suffix survival, replica currentness, committed-prefix/high-watermark state, consumer visibility, and failover truncation authority be separated?

The bounded answer is:

> **A replicated log does not have one single frontier called “the retained state.” Physical bytes, replica qualification, replicated commitment, reader visibility, and recovery/truncation authority can advance or retreat under different rules. A longer surviving suffix can be non-current; a committed prefix can be broader than one reader's visible history; and correct failover can require deleting physically intact records after lineage qualification.**

The comparison is deliberately narrow and uses three already-grounded Kafka slices:

- [Case 56 — Kafka 0.8.2 ISR/high-watermark currentness and failover truncation](../cases/56-apache-kafka-replicated-log-high-watermark.md);
- [Case 90 — Kafka 0.11 leader-epoch lineage and safe truncation](../cases/90-apache-kafka-leader-epoch-safe-truncation.md);
- [Case 63 — Kafka 0.11 transactional `READ_COMMITTED` visibility](../cases/63-apache-kafka-transactional-read-visibility.md).

Historical facts remain in those canonical case/evidence records. The decomposition below is an **engineering reconstruction** across them. Comparisons to other systems are **functional analogies only**. This document does not claim that Kafka invented replicated logs, high-watermark commitment, epochs, transactional visibility, or truncation, and it does not turn later Kafka vocabulary into a timeless distributed-systems taxonomy.

---

## 1. One local log can carry several different boundaries

The simplest mistaken model is:

```text
bytes exist on disk
    -> replica has them
    -> they are committed
    -> consumers may see them
    -> they must survive failover
```

The grounded Kafka cases break every arrow in that chain.

Case 56 shows a leader or follower may physically retain records beyond the high watermark. Those records are part of a local log embodiment but are not yet in the ordinary committed/consumer-visible prefix. The same case also shows an assigned replica can fall outside the ISR while retaining substantial payload.

Case 90 shows that even a suffix which once looked plausible relative to local offset state can fail a later lineage test. KIP-101 added leader-epoch history because a locally retained high watermark was not by itself a complete witness for safe follower truncation. The 2018–2019 follow-up evidence then shows that the epoch cache itself must be complete and format-admissible before it is trusted.

Case 63 adds a further split inside the already replicated prefix. Kafka 0.11 can retain records below the high watermark while a `READ_COMMITTED` consumer still stops at the last stable offset (LSO), and aborted transaction records can remain physically present while retained decision/index state causes that reader to suppress them.

Thus a single ordered partition can simultaneously have several relevant frontiers or qualifications:

```text
local physical log end
    >= replicated/committed high watermark
    >= transaction-stable visibility frontier for READ_COMMITTED
```

The inequalities are schematic rather than a universal formula for every Kafka state, but they expose the key point: **different relations answer different questions over the same bytes.**

---

## 2. Six relations that must remain distinct

### 2.1 Physical suffix survival

Question:

> Which records still exist in this replica's local log embodiment?

This is the weakest layer in the synthesis. It establishes byte/record presence at one replica, not protocol authority.

A follower may retain a longer suffix than the current leader. A leader may retain an appended tail above the high watermark. Aborted transactional records may remain in ordinary log segments.

Therefore:

```text
record physically present
    != record current
    != record visible
    != record guaranteed to survive recovery
```

### 2.2 Replica currentness / qualification

Question:

> Which replica is sufficiently caught up and protocol-qualified to participate in the current replication guarantee?

In Case 56, assigned-replica membership and ISR membership are separate. A replica can still possess data while being outside ISR because it is lagging or otherwise no longer qualified as in-sync.

This relation is about the replica as a participant, not just about a record offset.

Therefore:

```text
assigned replica
    != in-sync replica

payload survives on replica
    != replica retains current replication qualification
```

### 2.3 Committed-prefix / high-watermark state

Question:

> Up to which offset does the bounded replication protocol treat the log prefix as committed/current enough for ordinary consumption?

Case 56 grounds the high watermark as a retained frontier derived from ISR progress and periodically checkpointed for recovery. It is weaker than “all assigned replicas have these records” and stronger than “the leader appended these bytes.”

The high-watermark checkpoint is itself retained control state, not payload and not a complete replication history.

Therefore:

```text
leader log end
    != high watermark

replication factor
    != current committed frontier

high-watermark checkpoint
    != complete history of replication events
```

### 2.4 Reader visibility / admissible history

Question:

> Which records may this reader receive under this read contract?

In Kafka 0.8.2 ordinary consumer reads are bounded by the high watermark. Case 63 shows that this stops being the whole visibility story once transactional isolation is introduced. A `READ_COMMITTED` consumer can be bounded by an LSO below the high watermark, and aborted records can be filtered even though their bytes remain in the replicated log.

So “consumer visibility” is not merely another spelling of “replicated commitment.” It is observer/protocol qualified.

Therefore:

```text
below high watermark
    != necessarily READ_COMMITTED-visible

physically retained aborted record
    != application-visible committed history

one partition log
    != one universal reader-visible history
```

### 2.5 Failover truncation authority

Question:

> When histories diverge, what authorizes deletion of a surviving suffix so a follower can rejoin the current log lineage?

Case 56's bounded unclean-election path can make a shorter current leader authoritative and cause a returning follower to truncate a longer local suffix. Case 90 then introduces leader-epoch lineage so follower recovery can locate a common history boundary more safely than by relying on a possibly stale local high watermark alone.

Truncation authority is therefore not inferred from physical length. It is a recovery relation established by current leadership plus the admissible protocol evidence for common history.

Therefore:

```text
longer surviving suffix
    != stronger recovery authority

local high watermark
    != complete lineage witness

leader-epoch metadata exists
    != metadata is automatically admissible
```

### 2.6 Convergence after authority has been decided

Question:

> Have the replicas actually been brought back into one admissible history after the decision?

A truncation decision, an ISR transition, or a transaction decision can establish what should count before every physical replica/segment representation has converged. Follower fetching, cache reconciliation, index rebuilding, segment cleanup, or later compaction can continue after an authoritative boundary is known.

Thus:

```text
boundary decided
    != convergence work complete

currentness established
    != all old embodiments removed
```

---

## 3. The high watermark answers one question, not every question

### Historical record inherited from Case 56

Kafka 0.8.2 computes a leader high watermark from the minimum log-end position of the current ISR. Ordinary consumer reads are bounded by that watermark, while follower replication fetches may continue beyond it so followers can catch up. The high watermark is periodically checkpointed to disk for recovery.

### Engineering reconstruction

The high watermark is best treated here as a **committed-prefix/currentness frontier**. It summarizes enough replication progress to answer a bounded service question, but it does not encode every fact that can later matter to recovery.

That becomes explicit in Case 90. KIP-101's motivating failure is precisely a situation in which a follower's locally retained high watermark can lag a record that had in fact become committed elsewhere before failure. If the follower simply truncates to its stale checkpoint, it can delete a record the protocol had already committed.

Therefore the repository should retain this guardrail:

> **A compact frontier can be authoritative for one operation and insufficient evidence for another.**

The high watermark can qualify the committed prefix while still being an incomplete lineage witness for follower recovery.

---

## 4. Leader epochs add lineage qualification, not another payload copy

### Historical record inherited from Case 90

Kafka 0.11 retains leader-epoch boundaries and uses an `OffsetsForLeaderEpoch` exchange before a follower resumes ordinary fetching. A follower can ask the current leader for the end of a locally observed epoch, truncate beyond the returned common boundary, reconcile epoch metadata, and then fetch forward again.

Post-release Kafka fixes from 2018–2019 sharpen the lifetime of that evidence:

- KAFKA-7415 shows an epoch cache can exist yet be incomplete after successive elections;
- KAFKA-7897 shows cache presence is not sufficient when the record format cannot support the lineage history being inferred;
- KAFKA-7959 deliberately clears/deletes sparse epoch-cache state so a later format upgrade cannot misuse it;
- KAFKA-7984 records cache rebuildability from eligible record batches while also exposing format-qualified reconstruction limits.

### Engineering reconstruction

Leader-epoch state is neither a second user log nor a universal replacement for the high watermark. It preserves a different relation: **where leadership intervals begin, so a surviving suffix can be tested for common lineage during recovery.**

This yields two independent failure classes:

```text
payload suffix missing
    != lineage evidence missing

lineage evidence present
    != lineage evidence truthful/admissible
```

It also yields an important retention counterexample:

> **Deleting stale recovery metadata can preserve higher-level continuity better than keeping it.**

That is deliberate forgetting of a derived relation, not deletion of the partition payload.

---

## 5. Transactional visibility can be narrower than replicated commitment

### Historical record inherited from Case 63

Kafka 0.11 `READ_COMMITTED` semantics introduce a last stable offset constrained by the earliest open transaction. The fetch path therefore carries both high watermark and LSO. COMMIT/ABORT control records, transaction indexes, and producer/transaction state help determine which transactional records become deliverable. Aborted records can stay physically present while the consumer suppresses them.

### Engineering reconstruction

This is a decisive counterexample to the shortcut:

```text
committed by replication
    = visible application history
```

Replication commitment and transactional decision answer different questions:

- the high watermark asks whether the prefix satisfies the bounded replication-currentness condition;
- the LSO asks how far a `READ_COMMITTED` reader may advance without crossing an unresolved transaction;
- abort decision/index evidence can exclude particular transactional records even after the stability frontier advances.

Thus **visibility is observer- and contract-relative even over one committed replicated log**.

This also shows why negative retained state matters. An ABORT marker/index entry is not ordinary user payload, yet its continued availability helps ensure that physically retained transactional bytes continue to count as absent from the `READ_COMMITTED` application history.

---

## 6. A bounded state-machine view

The following is a project reconstruction, not Kafka's own diagram:

```text
append record locally
    |
    v
physical suffix exists on one replica
    |
    +--> follower copies record
    |       |
    |       v
    |   replica progress changes
    |       |
    |       v
    |   ISR-qualified replication can advance HW
    |       |
    |       v
    |   replicated/committed prefix expands
    |       |
    |       +--> ordinary non-transactional visibility may expand
    |       |
    |       +--> READ_COMMITTED may still wait on LSO/transaction decision
    |
    +--> leadership/failure change
            |
            v
        lineage qualification
            |
            v
        keep common suffix or truncate divergent tail
            |
            v
        resume follower fetch / convergence
```

This diagram deliberately has branches because there is no single scalar “retention level” that monotonically increases from append to forever-safe history.

---

## 7. Why “more retained” is not monotonic

The three cases jointly reject a material-maximalist rule:

> Preserve the most bytes and the most metadata, and recovery will necessarily be safer.

Counterexamples:

1. **Longer payload can be less authoritative.** A returning Kafka replica can have more tail records yet be required to truncate them.
2. **More currentness metadata can be harmful.** A stale or format-inadmissible leader-epoch cache can drive unnecessary truncation; clearing it can be safer.
3. **More visible records can violate the read contract.** `READ_COMMITTED` intentionally withholds or filters bytes that exist in the replicated log.
4. **More replicas does not mean more current replicas.** Assigned replicas outside ISR do not count the same way as in-sync replicas for the bounded commitment rule.

The safer engineering principle is:

> **Retention quality depends on preserving the right payload and the right qualifying relations under the right authority and observer contract, not on maximizing surviving material indiscriminately.**

---

## 8. Relation to adjacent syntheses

This document is intentionally narrower than existing syntheses.

- [Synthesis 14](SYNTHESIS_14_DISTRIBUTED_ACK_VISIBILITY_DURABILITY.md) compares acknowledgement, replication, visibility, and durability across RADOS, Kafka, and Chain Replication. Synthesis 17 stays inside the ordered replicated-log problem and adds suffix/truncation/lineage detail.
- [Synthesis 16](SYNTHESIS_16_REPLICA_CURRENTNESS_RETAINED_RELATION.md) defines `currentness/admissibility relation` across Dynamo, Swift, Cassandra, and Kafka. Synthesis 17 specializes that category into ordered-log layers and adds transactional visibility as a counterexample to `committed prefix = one universal visible history`.
- [Synthesis 13](SYNTHESIS_13_DURABILITY_HANDOFF_PERSISTENCE_DOMAIN.md) concerns cache/device persistence boundaries. Synthesis 17 does **not** infer device-level power-fail durability merely from Kafka replication/commit language.
- [Case 42](../cases/42-apache-kafka-log-compaction-delete-marker-retention.md) concerns keyed log compaction and history retirement. Failover truncation here removes a divergent/non-admissible suffix for convergence; compaction forgets superseded keyed history under a different rule.
- [Case 64](../cases/64-apache-kafka-transaction-coordinator-state-recovery.md) covers coordinator recovery. Synthesis 17 uses only the partition-log visibility relation grounded in Case 63 and does not reclassify coordinator state as a log-suffix frontier.

---

## 9. Historical and prior-art boundary

This synthesis is **not** an invention-priority document. It reuses primary evidence already grounded in the canonical cases and keeps their dates/vocabulary separate:

- Apache Kafka 0.8.2.0 source and versioned design/configuration material for ISR, high watermark, consumer read bounds, checkpointing, and unclean-election truncation;
- Apache KIP-101 plus Kafka 0.11.0.0 source for leader-epoch recovery and lineage-qualified truncation;
- Apache KIP-98 plus Kafka 0.11.0.0 source for transactional `READ_COMMITTED`, LSO, control records, and aborted-transaction indexes;
- Apache 2018–2019 KAFKA-7415, KAFKA-7897, KAFKA-7959, and KAFKA-7984 only as later validation/evolution of leader-epoch-cache completeness and admissibility.

Useful primary anchors already preserved by the cases include:

- Kafka `0.8.2.0` source: <https://github.com/apache/kafka/tree/0.8.2.0>;
- Kafka `0.11.0.0` source: <https://github.com/apache/kafka/tree/0.11.0.0>;
- KIP-101: <https://cwiki.apache.org/confluence/display/KAFKA/KIP-101%3A+Alter+Replication+Protocol+to+use+Leader+Epoch+rather+than+High+Watermark+for+Truncation>;
- KIP-98: <https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging>.

Current searches of `tmzncty/computing-archaeology` found no dedicated Kafka high-watermark / leader-epoch / transactional-visibility synthesis to reuse. Broad replicated-log, commit-index, epoch/term, transaction-log, and recovery genealogy belongs there if developed. `technical-retention` keeps only this bounded retention-layer decomposition.

---

## 10. Bounded conclusion

For this replicated-log slice, retain six separate questions:

1. **Presence:** which bytes physically survive on which replica?
2. **Replica qualification:** which replicas are currently in the protocol's qualified set?
3. **Commit frontier:** which prefix satisfies the bounded replication-currentness rule?
4. **Visibility:** which part of that retained/committed material may this reader observe under its isolation contract?
5. **Recovery authority:** which retained lineage/currentness evidence authorizes keeping or truncating a suffix after failover?
6. **Convergence:** has the physical replica set actually been brought back into the newly qualified history?

The strongest reusable guardrails are:

> **physical suffix survival != replica currentness != committed-prefix state != reader visibility != failover truncation authority**

and:

> **a longer surviving log can be less authoritative, while a narrower visible history can be more correct for a particular read contract.**
'''
doc_path.write_text(doc.rstrip() + "\n", encoding="utf-8")

readme_insert = r'''A bounded replicated-log layer comparison is now available in [`docs/SYNTHESIS_17_REPLICATED_LOG_SUFFIX_CURRENTNESS_VISIBILITY.md`](docs/SYNTHESIS_17_REPLICATED_LOG_SUFFIX_CURRENTNESS_VISIBILITY.md). Centered on grounded Kafka Cases 56, 90, and 63, it separates physical suffix survival, replica qualification, committed-prefix/high-watermark state, reader-specific visibility, lineage-qualified failover truncation authority, and later convergence. It fixes the counterexamples `longer surviving suffix ≠ stronger authority`, `below high watermark ≠ automatically READ_COMMITTED-visible`, `checkpoint exists ≠ lineage evidence admissible`, and `boundary decided ≠ convergence complete`.

'''
replace_once(
    "README.md",
    "This chain is a **research heuristic**, not a claim that all of these mechanisms are historically or philosophically identical.\n",
    readme_insert + "This chain is a **research heuristic**, not a claim that all of these mechanisms are historically or philosophically identical.\n",
)

roadmap_old = "- [ ] In a replicated log, how should physical suffix survival, replica currentness, committed-prefix/high-watermark state, consumer visibility, and failover truncation authority be separated?"
roadmap_new = "- [x] In a replicated log, separate `physical suffix survival`, `replica currentness/qualification`, `committed-prefix/high-watermark state`, `reader-specific visibility`, `failover truncation authority`, and later `convergence` — bounded by [`docs/SYNTHESIS_17_REPLICATED_LOG_SUFFIX_CURRENTNESS_VISIBILITY.md`](docs/SYNTHESIS_17_REPLICATED_LOG_SUFFIX_CURRENTNESS_VISIBILITY.md), using grounded Kafka Cases 56, 90, and 63. The synthesis preserves `high watermark ≠ complete lineage witness`, adds the transactional counterexample `below high watermark ≠ automatically READ_COMMITTED-visible`, and keeps lineage evidence, truncation authority, and post-decision convergence distinct. Broader replicated-log/epoch/transaction genealogy, other systems, end-to-end device durability, and production fault injection remain separate work."
replace_once("ROADMAP.md", roadmap_old, roadmap_new)

case_index_block = r'''## Synthesis 17 — replicated-log suffix/currentness/visibility findings

- **2077 — physical suffix survival ≠ replica currentness:** a Kafka replica can retain readable records while falling outside ISR or while its suffix no longer belongs to the current recovery lineage. (`H/P` inherited, `E`)
- **2078 — assigned replica ≠ in-sync replica:** replica placement/membership and present replication qualification are separate relations; retained bytes do not by themselves restore ISR status. (`H/P` inherited, `E`)
- **2079 — leader log end ≠ committed-prefix frontier:** Case 56 grounds local append progress beyond the high watermark, so the longest local suffix is not automatically the protocol's committed state. (`H/P` inherited, `E`)
- **2080 — high-watermark checkpoint ≠ complete replication history:** the checkpoint retains a compact recovery/currentness frontier rather than every follower fetch, ISR transition, or acknowledgement event that produced it. (`H/P` inherited, `E`)
- **2081 — high watermark ≠ complete recovery-lineage witness:** KIP-101 exists because a stale locally retained high watermark can be insufficient for safe follower truncation after failure. (`H/P` inherited, `E`)
- **2082 — leader-epoch lineage ≠ another payload copy:** epoch→offset state qualifies leadership boundaries for recovery; it does not duplicate the application records it helps interpret. (`H/P` inherited, `E`)
- **2083 — lineage metadata presence ≠ lineage metadata admissibility:** the 2018–2019 Case-90 deepening shows completeness and record-format support are part of whether retained epoch state may safely authorize truncation. (`H/P` inherited, `E`)
- **2084 — longer surviving suffix ≠ stronger truncation authority:** a returning follower may be required to delete physically intact tail records so it converges to the currently qualified leader lineage. (`H/P` inherited, `E`)
- **2085 — below high watermark ≠ automatically `READ_COMMITTED`-visible:** Case 63's LSO can lag the replication high watermark while a transaction remains unresolved. (`H/P` inherited, `E`)
- **2086 — replication commitment ≠ transaction decision:** records can satisfy the replication frontier before COMMIT/ABORT state makes their application-level outcome known. (`H/P` inherited, `E`)
- **2087 — aborted payload presence ≠ application-visible committed history:** Kafka can retain aborted transactional records in log segments while decision/index evidence causes `READ_COMMITTED` consumers to suppress them. (`H/P` inherited, `E`)
- **2088 — one physical replicated log ≠ one universal visible history:** read isolation can select different admissible histories over the same retained bytes and replication state. (`H/P` inherited, `E`)
- **2089 — truncation decision ≠ convergence complete:** deciding the authoritative common boundary is distinct from follower fetch, epoch-cache reconciliation, index rebuilding, cleanup, or other later work that brings embodiments back into agreement. (`E`)
- **2090 — more retained material ≠ monotonically safer retention:** longer divergent payload, stale lineage metadata, and broader reader visibility can each be less correct than a smaller protocol-qualified state. (`E`, `A`)
- **2091 — Synthesis 16 currentness ≠ Synthesis 17 ordered-log closure:** Synthesis 16 provides the broad cross-system currentness/admissibility category; Synthesis 17 specializes it into ordered-log presence, qualification, commit, visibility, truncation, and convergence layers without asserting a new historical mechanism. (`A`, `X`)
- **2092 — related-repository boundary:** current `tmzncty/computing-archaeology` searches found no dedicated Kafka high-watermark/leader-epoch/transactional-visibility synthesis; broad replicated-log, epoch/term, commit-index, transaction-log, and recovery genealogy belongs there if developed. (`H/P` project-state record)
'''
append_once("CASE_INDEX.md", "## Synthesis 17 — replicated-log suffix/currentness/visibility findings", case_index_block)

for changed in [
    str(doc_path),
    "README.md",
    "ROADMAP.md",
    "CASE_INDEX.md",
]:
    normalize(changed)
