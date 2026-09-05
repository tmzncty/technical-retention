# Case 91 Grounding Record — Cassandra 2006–2014 Deletion-Marker Retention

## Purpose

This record grounds [`cases/91-apache-cassandra-tombstone-grace-zombie-prevention.md`](../cases/91-apache-cassandra-tombstone-grace-zombie-prevention.md) without turning Cassandra deletion into a generic history of LSM trees, distributed databases, repair, or secure erasure.

**Question:** what evidence supports the claim that a Cassandra deletion can depend on retaining a timestamped negative marker until older local/distributed representations can no longer legitimately reassert the deleted value?

**Evidence boundary:** exact `cassandra-1.2.19` source and ASF issue/change records are the principal historical/implementation evidence. Current Apache Cassandra documentation is used as an institutional explanation of the tombstone/zombie model where it is consistent with the inspected historical implementation; modern options are not projected backward. Bigtable 2006 is used only as earlier primary prior art for deletion entries in immutable-SSTable compaction.

---

## Source ledger

### P1 — Apache Cassandra `DeletedColumn.java`, tag `cassandra-1.2.19`

**Artifact:** Apache Cassandra source.

**URL:** <https://github.com/apache/cassandra/blob/cassandra-1.2.19/src/java/org/apache/cassandra/db/DeletedColumn.java>

**Type:** primary implementation artifact.

**Observed implementation facts:**

- `DeletedColumn` extends `Column`;
- `isMarkedForDelete()` always returns true;
- `getMarkedForDeleteAt()` returns the column timestamp;
- `getLocalDeletionTime()` decodes a retained local deletion time;
- serialization uses `ColumnSerializer.DELETION_MASK`;
- validation requires a four-byte tombstone value and nonnegative local deletion time.

**Supports:** a deletion marker is a retained first-class database representation, not mere absence.

**Does not support:** a complete account of every Cassandra delete type or repair propagation path.

### P2 — Apache Cassandra `CFMetaData.java`, tag `cassandra-1.2.19`

**Artifact:** Apache Cassandra source.

**URL:** <https://github.com/apache/cassandra/blob/cassandra-1.2.19/src/java/org/apache/cassandra/config/CFMetaData.java>

**Type:** primary implementation artifact.

**Observed implementation fact:**

- `DEFAULT_GC_GRACE_SECONDS = 864000` for ordinary user tables, i.e. ten days.

**Supports:** the tombstone has a configurable retention-policy timescale distinct from the lifetime of the deleted value.

**Boundary:** special system tables can have different grace values; the constant is not a universal physical-retention guarantee.

### P3 — Apache Cassandra `CompactionController.java`, tag `cassandra-1.2.19`

**Artifact:** Apache Cassandra source.

**URL:** <https://github.com/apache/cassandra/blob/cassandra-1.2.19/src/java/org/apache/cassandra/db/compaction/CompactionController.java>

**Type:** primary implementation artifact.

**Observed implementation facts:**

- the controller retains `gcBefore` as compaction state;
- `shouldPurge(key, maxDeletionTimestamp)` is documented to return true only when it is safe to drop tombstones because all versions of the row are known to be in the compaction set;
- it searches overlapping SSTables;
- if an overlapping SSTable may contain the key and its minimum timestamp is at/before the deletion timestamp, purge is refused.

**Supports:** elapsed age is not the entire local purge condition; the engine also protects against older shadowed representations surviving outside the compaction set.

**Does not support:** proof that every distributed replica has repaired.

### P4 — Apache Cassandra `CHANGES.txt`, tag `cassandra-1.2.19`

**Artifact:** Apache Cassandra release change record.

**URL:** <https://github.com/apache/cassandra/blob/cassandra-1.2.19/CHANGES.txt>

**Type:** primary project change record.

**Observed historical facts:**

- 1.2.19 lists `Track expired tombstones (CASSANDRA-7810)`;
- the same release list contains additional tombstone-related fixes, reinforcing that tombstone lifecycle correctness was active implementation work rather than a purely conceptual rule.

**Supports:** CASSANDRA-7810 belongs to the exact bounded release line.

### P5 — ASF JIRA CASSANDRA-7810, “tombstones gc'd before being locally applied”

**Artifact:** Apache Cassandra issue record, created 21 August 2014, resolved 27 August 2014.

**URL:** <https://issues.apache.org/jira/browse/CASSANDRA-7810>

**Type:** primary/institutional defect record.

**Observed failure:**

- reproduction uses a one-node cluster and `gc_grace_seconds = 0`;
- a row is inserted, deleted, flushed, and compacted;
- after compaction the row reappears;
- the issue diagnosis says the tombstone appears to have been considered obsolete and discarded before being locally applied;
- fix versions include 1.2.19, 2.0.11, and 2.1.0.

**Supports:** tombstone age/expiry cannot be treated as permission to discard the deletion relation before it has performed its suppressive work; purge sequencing matters even without a missing remote replica.

**Does not support:** a claim that all Cassandra resurrection bugs have the same cause.

### S1 — Apache Cassandra documentation, `Tombstones`

**Artifact:** current Apache Cassandra institutional documentation.

**URL:** <https://cassandra.apache.org/doc/latest/cassandra/managing/operating/compaction/tombstones.html>

**Type:** official later documentation / institutional secondary-to-historical-implementation evidence.

**Supports:**

- Cassandra treats delete as insertion of a timestamped tombstone;
- values timestamped before the tombstone are ignored;
- unavailable replicas can miss the tombstone and retain pre-delete data;
- if the deletion marker disappears before the stale replica is reconciled, deleted data can reappear as a `zombie`;
- `gc_grace_seconds` defaults to 864000 seconds in the documented default;
- grace expiry makes tombstones removable during compaction rather than immediately removing them at the deadline;
- safe compaction also depends on including older data that the tombstone shadows;
- later versions can add further repair-aware purge policy.

**Version boundary:** this page documents modern Cassandra. Its newer `only_purge_repaired_tombstones` option is **not** used as evidence for 1.2.19 behavior. `zombie` is treated as later official explanatory vocabulary unless separately found in the 1.2 sources.

### P6 — Chang et al., Bigtable, OSDI 2006, §5.4

**Artifact:** Fay Chang et al., “Bigtable: A Distributed Storage System for Structured Data,” OSDI 2006.

**URL:** <https://storage.googleapis.com/gweb-research2023-media/pubtools/4443.pdf>

**Type:** primary/contemporary technical paper; prior-art witness.

**Exact anchor:** §5.4 `Compactions`, printed paper page 6 / PDF page 5 in the inspected copy.

**Observed historical facts:**

- SSTables from non-major compactions can contain `special deletion entries` that suppress deleted data in older live SSTables;
- a major compaction can rewrite all SSTables into one containing neither deletion information nor deleted data;
- major compactions reclaim resources used by deleted data and make deleted data disappear on a later timescale.

**Supports:** deletion-marker retention across immutable representations and later compaction-mediated retirement predate Cassandra.

**Does not support:** implementation identity or a directly proven code genealogy from Bigtable to Cassandra.

---

## Claim ledger

| Claim | Layer | Evidence | Strength |
|---|---|---|---|
| Cassandra 1.2.19 represents a column deletion with a `DeletedColumn` carrying delete/local-time state | historical / implementation record | P1 | strong |
| the 1.2.19 ordinary user-table default `gc_grace_seconds` is 864000 seconds | historical / implementation record | P2 | strong |
| local purge can be refused when an overlapping SSTable may retain an older version | implementation record | P3 | strong |
| grace expiry is not the same event as tombstone removal | institutional explanation + implementation structure | S1, P3 | strong |
| a stale replica that missed a deletion can reintroduce old data after deletion evidence disappears | institutional distributed-system explanation | S1 | strong, later official explanation |
| CASSANDRA-7810 could resurrect a deleted row on one node when an expired tombstone was discarded too early in compaction | historical defect record | P5, P4 | strong |
| Bigtable 2006 already used special deletion entries and later major-compaction retirement | prior art | P6 | strong |
| logical deletion ≠ physical disappearance | engineering reconstruction | P1, P3, S1 | strong |
| tombstone ≠ deleted payload | engineering reconstruction | P1 | strong |
| grace expiry ≠ sufficient local purge authority | engineering reconstruction | P2, P3 | strong |
| local deletion ≠ cluster-wide forgetting | engineering reconstruction | S1 | strong within documented model |
| correct forgetting can require retaining negative evidence | engineering reconstruction | P1, P3, S1, P5 | strong |
| tombstone purge ≠ secure media sanitization | negative boundary | no sanitization claim in P1–P6 | strong as claim-control boundary |
| Cassandra invented tombstone/deletion-entry compaction | rejected origin claim | contradicted by P6 prior art | rejected |

---

## Historical record / engineering reconstruction / analogy separation

### Historical record

Safe to state as sourced facts:

- exact `DeletedColumn` fields/methods and deletion serialization in 1.2.19;
- the exact 1.2.19 default grace constant;
- the exact compaction controller's overlap-aware `shouldPurge` logic;
- CASSANDRA-7810's single-node resurrection reproduction and fix-version record;
- modern Apache's documented tombstone/zombie explanation, with its later date made explicit;
- Bigtable 2006 `special deletion entries` and major-compaction semantics.

### Engineering reconstruction

Project terms and conclusions derived from those facts:

- `negative currentness evidence`;
- `distributed forgetting witness`;
- `purge admissibility`;
- `absence is not self-authenticating`;
- `logical deletion ≠ physical disappearance`;
- `grace expiry ≠ sufficient local purge authority`;
- `forgetting the forgetting record too early can restore an older state`.

### Functional analogy only

- JBD revoke Case 74: both keep negative evidence, but one governs journal replay after block reuse and one governs database versions/replicas;
- GFS deletion Case 73: both defer reclamation after logical deletion, with different authority and cleanup mechanisms;
- Kafka Case 90: both can reject physically surviving state as no longer authoritative, with unrelated lineage/currentness machinery;
- deallocation/sanitize Case 44: both demonstrate logical forgetting does not prove physical erasure.

### Philosophical interpretation only

The repository may say that forgetting has a temporary memory phase or that absence is not self-authenticating. Cassandra's developers and Bigtable's authors need not have formulated the mechanism in those philosophical terms.

---

## Prior-art controls

### Reject: “Cassandra invented tombstones”

Bigtable 2006 directly documents `special deletion entries` in SSTables and later compaction that retires both deletion information and deleted data. A broader database/LSM genealogy would likely extend further back and has not been completed here.

### Reject: “Bigtable deletion entries = Cassandra tombstones”

The comparison establishes prior function, not implementation identity. Cassandra adds its own distributed-replica/grace/repair context and historical vocabulary.

### Reject: “ten days means deletion is guaranteed safe after ten days”

`gc_grace_seconds` is a policy interval. The 1.2.19 local compaction path still checks overlapping old versions, and the later Apache distributed explanation explicitly frames stale-node recovery/repair timing as the reason early tombstone disappearance can be unsafe.

### Reject: “expired = already purged”

Apache documentation distinguishes expiry/eligibility from actual compaction removal.

### Reject: “purged = securely erased”

No inspected source establishes media sanitization, forensic irrecoverability, backup deletion, snapshot deletion, or controller-level erase.

### Reject: “modern repair-aware purge controls existed in 1.2.19”

Later options such as `only_purge_repaired_tombstones` must remain later unless exact historical source says otherwise.

---

## Cross-case comparison notes

### Case 74 — retained negative recovery evidence

JBD revoke records a transaction-relative prohibition: older journal data must not be replayed onto a block whose later use supersedes it. Cassandra tombstones record database deletion/currentness: older value timestamps must not become visible, including across stale replicas. Both make the technically important state a negative relation rather than a payload copy, but their trigger, scope, and history are different.

### Case 73 — deferred deletion and reclamation

GFS separates user deletion, hidden-name grace, namespace/chunk reference retirement, and later replica cleanup. Cassandra separates delete-marker insertion, grace, local compaction shadowing checks, distributed reconciliation risk, and eventual marker/data reclamation. Both refute `DELETE call = instant physical erasure`, but their mechanisms should not be merged.

### Case 90 — survival versus authority

Kafka can discard a longer physical suffix when leader-epoch lineage says it is divergent. Cassandra can suppress a physically surviving older value when a newer tombstone says it is deleted. This supports the cross-case proposition `physical survival ≠ authoritative current state` without implying genealogy.

### Case 44 — logical deletion versus sanitization

Cassandra tombstone retirement belongs to database logical/currentness semantics. It supplies no secure-erase certificate for the underlying medium.

---

## Remaining work deliberately left open

- exact pre-1.2 historical origin of Cassandra `DeletedColumn` / tombstone vocabulary;
- one exact early-release reconstruction of hinted handoff + anti-entropy repair for deletions;
- later repair-aware tombstone purging and `only_purge_repaired_tombstones` genealogy;
- range/partition tombstones and TTL expiration;
- production fault-injection reproductions beyond the archived CASSANDRA-7810 defect;
- complete Bigtable / LSM / Cassandra deletion-marker genealogy in `computing-archaeology`;
- secure deletion of the physical medium after Cassandra compaction.

---

## Promotion decision

**Status: `grounded`.**

Reason:

- exact tagged Cassandra source establishes the deletion-marker embodiment, default grace timescale, and overlap-aware purge condition;
- an ASF defect record supplies a concrete falsifying failure mode for premature local forgetting;
- official Apache documentation supplies the distributed stale-replica/zombie explanation while remaining explicitly later than the bounded implementation;
- Bigtable 2006 provides primary prior art that blocks an origin myth;
- the case's engineering/analogy/philosophy layers are labeled and its modern-version boundaries are explicit.
