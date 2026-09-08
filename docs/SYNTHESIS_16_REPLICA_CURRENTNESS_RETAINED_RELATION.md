# Synthesis 16 — Replica Currentness as a Retained Relation

## Status and scope

**Bounded cross-case engineering synthesis.** This document closes one explicit ROADMAP question:

> When replicas disagree, is `currentness` itself retained metadata/protocol state?

The answer supported by the grounded cases is deliberately qualified:

> **Currentness is not one universal field or one additional copy of the payload. It is a relation that determines which surviving values, versions, fragments, prefixes, or negative records are admissible as the present state under a particular protocol. That relation is often made recoverable by retained metadata or protocol state, but its representation and lifetime vary by system.**

The comparison uses five already-grounded slices:

- [Case 23 — Amazon Dynamo divergent-version retention](../cases/23-amazon-dynamo-divergent-version-anti-entropy.md);
- [Case 25 — OpenStack Swift EC overwrite/durable currentness](../cases/25-openstack-swift-ec-overwrite-durable-currentness.md);
- [Case 41 — Apache Cassandra tombstone/GC-grace resurrection](../cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md);
- [Case 56 — Apache Kafka 0.8.2 high-watermark/ISR currentness](../cases/56-apache-kafka-replicated-log-high-watermark.md);
- [Case 90 — Apache Kafka 0.11 leader-epoch recovery](../cases/90-apache-kafka-leader-epoch-safe-truncation.md).

Historical claims remain in those case/evidence records. The decomposition below is an **engineering reconstruction** across them. Cross-system similarities are **functional analogies only**; this document does not claim a Dynamo→Swift→Cassandra→Kafka genealogy, nor does it claim that their historical actors shared one concept called `currentness`.

---

## 1. Why physical survival is not enough

All five cases provide a counterexample to the shortcut:

```text
surviving bytes / surviving replica
    = current state
```

That equation fails in different ways.

- Dynamo can intentionally retain several causally unrelated versions of one key because no retained causal relation yet establishes that one supersedes the others.
- Swift can have fragment archives physically present while a timestamped coded version is not yet qualified by the same-timestamp/distinct-index/durability relation required for service.
- Cassandra can retain an old positive value on one replica while a newer tombstone on another replica is the state that must win; if the tombstone is forgotten too early, the stale positive value can become admissible again.
- Kafka 0.8.2 can retain a longer local log suffix beyond the high watermark; that suffix is physically present without belonging to the ordinary committed/consumer-visible prefix.
- Kafka 0.11 can retain a longer follower suffix that is nevertheless outside the current leader lineage and must be truncated after an epoch-qualified recovery exchange.

The common engineering lesson is therefore not that all these systems store the same kind of metadata. It is narrower:

> **When several embodiments can answer for one logical object, retention requires a rule for deciding which surviving state still counts.**

---

## 2. Seven relations that must not be collapsed

A useful audit separates at least seven things.

### 2.1 Payload / embodiment presence

Does a node, disk, log, SSTable, or fragment file physically retain bytes?

Presence is necessary for some forms of recovery, but it does not by itself establish that those bytes are current.

### 2.2 Version or lineage designation

What identifier lets the protocol distinguish candidate histories or versions?

Examples in the bounded cases include Dynamo vector-clock entries, Swift timestamps/fragment indexes, Cassandra mutation/tombstone timestamps, Kafka offsets and leader epochs.

An identifier alone does not always decide supersession.

### 2.3 Currentness / admissibility relation

Which candidate state may count as the present answer under the protocol?

This relation can be:

- **set-valued** — Dynamo can retain several concurrent leaves;
- **cohort-qualified** — Swift requires a same-timestamp coded cohort plus durability evidence;
- **negative** — Cassandra tombstones make an older positive value inadmissible;
- **frontier-shaped** — Kafka's high watermark qualifies a committed prefix;
- **lineage-qualified** — Kafka leader epochs identify a common history boundary for recovery.

These forms are functionally comparable only at the level of deciding admissibility.

### 2.4 Authority relation

Who may create, extend, or select the current state now?

Leader/coordinator/writer authority is adjacent to currentness but not identical to it. A process can be authorized to act while inherited payload candidates still need qualification, and surviving payload can remain after its former authority expires.

### 2.5 Visibility relation

Which qualified state may a particular reader observe?

Kafka ordinary consumer visibility is bounded by the high watermark. Dynamo may return several admissible sibling versions. Swift GET requires a usable coded cohort. These are not one universal read rule.

### 2.6 Convergence / repair relation

Have all intended replicas, fragments, or placements caught up?

Dynamo read repair and anti-entropy can continue after a request completes. Swift reconstruction can restore missing fragments or durability markers after the service-level version is already usable. Cassandra repair can propagate deletion evidence after the delete is already logically current on available replicas.

Thus:

> **currentness qualification ≠ full convergence.**

### 2.7 Retirement / forgetting authority

When may an older candidate or its currentness evidence be discarded?

Dynamo causal ancestry can authorize forgetting an ancestor; Swift newer-version commit authorizes retirement of older timestamp files; Cassandra tombstone reclamation is dangerous while stale positive replicas can still return; Kafka recovery can deliberately truncate a physically surviving divergent suffix.

Retirement therefore depends on a relation, not merely on age or physical redundancy.

---

## 3. Currentness evidence has several shapes

### Dynamo — causal currentness can be set-valued

**Historical record inherited from Case 23:** Dynamo attaches vector clocks to object versions. A causally dominated ancestor can be forgotten, while causally unrelated leaves must remain for reconciliation.

**Engineering reconstruction:** currentness here is not a scalar `latest version`. The admissible current state can be a set of unresolved leaves. Retained causal summary supports the distinction between `superseded` and `concurrent`, but the vector clock is not a complete operation history and Dynamo can truncate that metadata at a precision cost.

Therefore:

```text
version exists
    ≠ version is uniquely current

newer arrival
    ≠ causal supersession

retained causal summary
    ≠ complete history
```

### Swift EC — coded currentness needs a version-qualified cohort

**Historical record inherited from Case 25:** Swift EC stores timestamped fragment archives with fragment indexes and uses durability evidence for the timestamp. In the bounded 2.10.1 semantics, a successful GET requires enough distinct fragment indexes at one timestamp plus same-timestamp durability indication.

**Engineering reconstruction:** algebraic reconstructability and physical fragment presence are not enough. The protocol must establish that the fragments belong to one admissible version cohort and that the version crossed the relevant durability/commit boundary.

Therefore:

```text
k fragments survive
    ≠ current coded object

same erasure code
    ≠ same version

physical fragment presence
    ≠ commit/currentness qualification
```

### Cassandra — negative currentness can outrank positive payload

**Historical record inherited from Case 41:** Cassandra retains tombstones so an older positive value on an unavailable replica does not reappear during later repair. `gc_grace_seconds` bounds retention policy but does not prove that repair or propagation completed.

**Engineering reconstruction:** a record whose operational meaning is `this older value must not count` can be more current than surviving positive payload. Losing the negative evidence can change admissibility without changing the old bytes at all.

Therefore:

```text
positive payload survives
    ≠ positive payload remains admissible

negative marker retained
    = positive obligation to suppress stale state

negative marker reclaimed too early
    -> old positive embodiment may become admissible again
```

### Kafka 0.8.2 — currentness can be a committed-prefix frontier

**Historical record inherited from Case 56:** Kafka tracks ISR membership and computes a high watermark from ISR progress. Ordinary consumers are bounded by that watermark, while records can physically exist beyond it. A returning replica can also lose a longer suffix under an unclean-recovery path.

**Engineering reconstruction:** currentness is partly represented as a frontier over an ordered log. A longer physical suffix is not automatically stronger evidence of retained service state.

Therefore:

```text
longer log
    ≠ more authoritative log

assigned replica
    ≠ in-sync replica

local log end
    ≠ committed-prefix frontier
```

### Kafka 0.11 — a frontier can be insufficient without lineage

**Historical record inherited from Case 90:** KIP-101 adds leader-epoch boundary information because a stale locally retained high watermark can be insufficient for safe follower truncation. The released implementation persists epoch→start-offset information and uses an epoch exchange before ordinary fetch resumes.

**Engineering reconstruction:** one compact currentness summary may answer one question yet be insufficient for another. The high watermark qualifies the committed/readable prefix; leader-epoch history qualifies which surviving suffix belongs to the current lineage during recovery.

Therefore:

```text
commit frontier
    ≠ complete recovery-lineage witness

surviving suffix
    ≠ lineage-admissible suffix

more retained metadata
    ≠ automatically safer metadata
```

The last point matters because epoch metadata itself must be reconciled with log truncation and prefix retirement.

---

## 4. Currentness is retained relation, not necessarily retained object

The roadmap question can now be answered more precisely.

### Supported claim

In these distributed cases, currentness is often made operationally recoverable by retained protocol state such as:

- causal/version summaries;
- timestamps and durability witnesses;
- tombstones;
- replica-set qualification and progress frontiers;
- epoch/lineage checkpoints.

That retained state is constitutive because losing or misreading it can change which surviving payload is admitted, returned, repaired, or retired.

### Rejected stronger claim

Do **not** normalize all of those artifacts into a universal `currentness metadata` object.

Why not?

1. some currentness is set-valued rather than singular;
2. some evidence is negative rather than positive;
3. some is a frontier, some a lineage summary, some a cohort witness;
4. some is durable across restart, some is reconstructed or reconciled from participants;
5. one system can require several distinct relations at once;
6. protocol authority, integrity qualification, visibility, and convergence remain separate even when they consume some of the same state.

The safest project vocabulary is therefore:

> **currentness/admissibility relation** — the protocol-qualified relation that determines which surviving state may count as present/current for a specified operation and observer.

When discussing its embodiment, name the actual historical artifact instead of inventing a generic component.

---

## 5. Failure modes exposed by the comparison

The synthesis adds a failure class that is easy to miss when attention stays on payload durability:

> **payload survival can coexist with loss, staleness, or inconsistency of the relation that tells the system which payload counts.**

Examples already grounded include:

- causal-summary truncation reducing ancestry precision in Dynamo;
- stale/pre-commit fragments surviving without a qualifying Swift version relation;
- Cassandra tombstone loss allowing stale positive-state resurrection;
- Kafka high-watermark recovery state being insufficient for a later lineage decision;
- Kafka divergent suffix bytes surviving until epoch-qualified truncation removes them.

This motivates a technical-forgetting distinction:

```text
payload loss
    ≠ currentness-evidence loss
    ≠ authority loss
    ≠ convergence failure
```

Currentness-evidence loss can cause logical forgetting, resurrection, withdrawal, or deliberate truncation even while substantial payload bytes survive.

---

## 6. Relation to existing syntheses

This document does not duplicate the existing synthesis set.

- [Synthesis 10](SYNTHESIS_10_MUTABLE_EC_CURRENTNESS_RETIREMENT_REPAIR.md) is Swift-centered and closes mutable-EC currentness specifically.
- [Synthesis 14](SYNTHESIS_14_DISTRIBUTED_ACK_VISIBILITY_DURABILITY.md) separates acknowledgement, visibility, replication, and durability/completion contracts.
- [Synthesis 15](SYNTHESIS_15_LOGICAL_IDENTITY_EMBODIMENT_REPLACEMENT.md) separates logical designation, payload value, resolution relation, and physical embodiment during replacement/remapping.

Synthesis 16 adds a different axis: **when several candidate embodiments or histories coexist, what retained relation makes one, several, or a prefix admissible as current, and what happens if that qualifying relation is lost or becomes stale?**

---

## 7. Historical and prior-art boundary

This is not an invention-priority document. The canonical cases already preserve their own earlier causal-clock, replication, tombstone, commit, epoch, and log-recovery prior art.

The inspected `tmzncty/computing-archaeology` repository currently has no dedicated cross-system synthesis for Dynamo/Swift/Cassandra/Kafka currentness to reuse. Broader histories of version vectors, anti-entropy, quorum replication, tombstones, epochs, and replicated-log recovery belong there if developed. `technical-retention` retains only this cross-case relation decomposition.

Useful primary anchors already grounded in the cases include:

- DeCandia et al., **“Dynamo: Amazon's Highly Available Key-value Store”** (SOSP 2007), Amazon Science: <https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store>;
- OpenStack Swift signed/released 2.3.0 and 2.10.1 documentation/source, especially the EC multi-phase, GET, and reconstruction paths: <https://github.com/openstack/swift/tree/2.10.1>;
- Apache Cassandra exact GC-grace and repaired-tombstone commits: <https://github.com/apache/cassandra/commit/fa1f80f40da0bb629c40bf09791c6c90f2608774> and <https://github.com/apache/cassandra/commit/6f0c12f3a4668a5dcae162969843f02498ee7e6d>;
- Apache Kafka source tags `0.8.2.0` and `0.11.0.0`: <https://github.com/apache/kafka/tree/0.8.2.0> and <https://github.com/apache/kafka/tree/0.11.0.0>;
- Apache KIP-101, linked and source-anchored in Case 90.

---

## 8. Bounded conclusion

The cross-case answer is:

> **Yes, replica currentness can depend on retained metadata/protocol state, but `currentness` should be modeled as a qualified relation rather than one universal metadata object.**

That relation can decide whether a candidate is:

- superseded or concurrent;
- committed or merely present;
- current positive state or suppressed by newer negative evidence;
- inside or beyond an admissible prefix;
- part of the current lineage or a surviving divergent suffix;
- safe to retire or still needed to prevent resurrection/loss.

The strongest reusable guardrail is therefore:

> **physical survival ≠ currentness; currentness evidence ≠ payload; and losing currentness evidence can change logical survival without immediately changing the surviving bytes.**
