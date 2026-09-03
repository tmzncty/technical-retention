# Case 48 Grounding — Cassandra Incremental Repair State, 2.1–4.0

## Purpose

This record grounds [`cases/48-apache-cassandra-incremental-repair-state.md`](../cases/48-apache-cassandra-incremental-repair-state.md).

The bounded question is not merely whether Cassandra repairs replicas. It is whether Apache's own development record, versioned documentation, and source establish the stronger relation used by the case:

```text
past repair succeeds
    -> repair result is retained as SSTable metadata/classification
    -> future incremental repair excludes that class
    -> compaction keeps repaired and unrepaired populations separate
    -> therefore maintenance history changes future maintenance eligibility
    -> if repair classification itself diverges, repair bookkeeping becomes unreliable
    -> later Cassandra introduces pending-repair/session state before final promotion
```

The intended evidence standard is stronger than “a blog says incremental repair is cheaper.” The record requires direct evidence for:

1. historical feature intent;
2. persisted repair-state representation;
3. the anti-compaction mechanism;
4. future-scope consequences;
5. explicit limits of repaired status;
6. documented inconsistency of repair-history state;
7. the later pending-repair correction.

---

## Source hierarchy

### P1 — CASSANDRA-5351: historical feature intent

**Source:** Apache Cassandra JIRA, CASSANDRA-5351, **“Avoid repairing already-repaired data by default”**.

**URL:** <https://issues.apache.org/jira/browse/CASSANDRA-5351>

**Fix version:** 2.1 beta1.

The issue's description establishes three unusually direct actor-level claims:

- repair had built Merkle trees from all data in a column family;
- that behavior was considered correct but inefficient;
- Cassandra could improve it by **remembering which SSTables had already been successfully repaired** and only repairing SSTables new since the previous repair;
- compaction had to be changed so repaired data would not be mixed back together with unrepaired data.

### Claim control

This source supports:

> within Cassandra, remembered repair history was intentionally introduced to narrow future repair scope.

It does **not** support:

- Cassandra invented incremental maintenance;
- Cassandra invented anti-entropy;
- every later `repairedAt` implementation is identical to the first 2.1 implementation;
- the feature was reliable under every failure mode.

---

### P2 — Cassandra 3.11 Repair documentation: future eligibility and limits

**Source:** Apache Cassandra 3.11 documentation, `Operating > Repair`.

**URL:** <https://cassandra.apache.org/doc/3.11/cassandra/operating/repair.html>

**Directly inspected anchors:**

- section `Incremental and Full Repairs`;
- section `Usage and Best Practices`;
- `--validate` option.

The page states:

- full repair operates over all data in the repaired token range;
- incremental repair repairs only data written since the prior incremental repair;
- incremental repair is the default in this bounded documentation;
- once data is marked repaired, incremental repair will not repair it again;
- this is suitable for missed-write synchronization but does not protect against disk corruption, operator-caused data loss, or Cassandra bugs;
- full repairs should therefore still run occasionally;
- repair is not automatically run by Cassandra in this regime because of disk/network I/O cost and is invoked with `nodetool`;
- `--validate` compares repaired data with Merkle trees without streaming and tells the operator to run a full repair if repaired data is out of sync.

### Claim control

This source directly grounds:

```text
repaired classification -> future incremental exclusion
```

and also blocks:

```text
repaired classification -> timeless integrity guarantee
```

The documentation describes the intended 3.11 operational contract. CASSANDRA-9143 and later Apache writing are retained below as an explicit qualification of legacy incremental-repair reliability rather than hidden contradictory evidence.

---

### P3 — Cassandra 3.11 `StatsMetadata.java`: persisted repair field

**Source:** `src/java/org/apache/cassandra/io/sstable/metadata/StatsMetadata.java`, branch `cassandra-3.11`.

**URL:** <https://github.com/apache/cassandra/blob/cassandra-3.11/src/java/org/apache/cassandra/io/sstable/metadata/StatsMetadata.java>

The class declares:

```java
public final long repairedAt;
```

inside the SSTable metadata component alongside timestamp, TTL, level, tombstone-drop-time, and other stored metadata.

### Claim control

This directly supports the statement that repair classification has a retained implementation embodiment attached to SSTables. It does not by itself tell us the complete repair algorithm; that comes from P2/P4/P5.

---

### P4 — Cassandra 3.11 `CompactionManager.java`: anti-compaction and `repairedAt`

**Source:** `src/java/org/apache/cassandra/db/compaction/CompactionManager.java`, branch `cassandra-3.11`.

**URL:** <https://github.com/apache/cassandra/blob/cassandra-3.11/src/java/org/apache/cassandra/db/compaction/CompactionManager.java>

**Directly inspected implementation anchors:**

1. `doAntiCompaction(...)` documents that repaired ranges are tracked through `StatsMetadata.repairedAt`.
2. `antiCompactGroup(...)` creates two writers:
   - repaired output with the supplied `repairedAt`;
   - unrepaired output with `ActiveRepairService.UNREPAIRED_SSTABLE`.
3. The repaired writer is explicitly given the repair timestamp before commit; the original mixed SSTable is obsoleted as part of the transaction.
4. `performAnticompaction(...)` contains the explicit policy that already repaired SSTables are not anti-compacted again in the bounded legacy path.
5. If an SSTable lies wholly inside the repaired range, the implementation logs that it will mutate `repairedAt` **instead of anticompacting**, then reloads metadata and notifies repair-status change.
6. The source comment says anti-compaction can technically operate on repaired SSTables, but the implementation avoids splitting them merely to make their exact repair timestamps more accurate because it does not use the actual timestamp value for that purpose.

### Claim control

This is strong evidence for a distinction that documentation alone could leave vague:

```text
maintenance-state transition
    != necessarily physical split
```

and for the fact that the important bounded relation is the repaired/unrepaired classification, not a rich chronological history encoded in the exact `repairedAt` value.

---

### P5 — Cassandra 3.11 `CompactionStrategyManager.java`: separate compaction populations

**Source:** `src/java/org/apache/cassandra/db/compaction/CompactionStrategyManager.java`, branch `cassandra-3.11`.

**URL:** <https://github.com/apache/cassandra/blob/cassandra-3.11/src/java/org/apache/cassandra/db/compaction/CompactionStrategyManager.java>

The class comment states that the manager has **two actual compaction-strategy instances per data directory**, one for repaired data and one for unrepaired data, specifically so the sets can be totally separated. The class maintains distinct `repaired` and `unrepaired` strategy collections.

### Claim control

This grounds the statement that repair history is not merely consulted at `nodetool repair` invocation. It changes subsequent ordinary storage-engine maintenance grouping.

---

### P6 — Cassandra 3.11 Compaction documentation: repair-state / reclamation coupling

**Source:** Apache Cassandra 3.11 documentation, `Operating > Compaction`.

**URL:** <https://cassandra.apache.org/doc/3.11/cassandra/operating/compaction/index.html>

**Relevant section:** `Repaired/unrepaired data`.

Apache states that:

- incremental repair requires tracking repaired versus unrepaired data;
- anti-compaction splits repaired data into repaired and unrepaired SSTables;
- separate compaction-strategy instances keep the populations from mixing again;
- if incremental repair is run once and then never again, very old repaired SSTables can block compaction from dropping tombstones in newer unrepaired SSTables.

### Claim control

The final point is used only for the bounded composition claim:

> repair-history partitioning can affect later reclamation topology.

Case 41 remains authoritative for Cassandra tombstone/`gc_grace_seconds` anti-resurrection semantics. Case 48 does not duplicate that mechanism.

---

### P7 — CASSANDRA-9143: repair-history classification became a consistency problem

**Source:** Apache Cassandra JIRA, CASSANDRA-9143, **“Fix consistency of incrementally repaired data across replicas.”**

**URL:** <https://issues.apache.org/jira/browse/CASSANDRA-9143>

**Fix version:** Cassandra 4.0 / 4.0-alpha1.

The issue discussion directly records problems in the legacy model:

- anti-compaction requests could succeed on some replicas and fail on others;
- `repairedAt` could therefore become inconsistent between participants;
- ordinary compaction during repair could also alter which data was regarded as repaired/unrepaired;
- such differences could cause unpredictable incremental-repair behavior and unnecessary future streaming.

The redesigned sequence described in the issue is:

1. persist repair session locally on each participant;
2. anti-compact intersecting **unrepaired** SSTables into a **pending repair bucket**;
3. perform validation/synchronization against that isolated set;
4. use a coordinated finalization step to promote pending data to repaired;
5. on failure, return pending data to unrepaired.

### Claim control

CASSANDRA-9143 supports:

> repair classification itself required stronger cross-participant state-transition discipline.

It does not support the stronger unsourced claim:

> every `repairedAt` inconsistency necessarily corrupted user payload.

The issue explicitly discusses consistency/operational correctness of incremental repair metadata and excess/unpredictable streaming. This record stays within that evidence.

---

### P8 — Cassandra 4.0 `PendingAntiCompaction.java`: in-progress repair is a separate class

**Source:** `src/java/org/apache/cassandra/db/repair/PendingAntiCompaction.java`, branch `cassandra-4.0`.

**URL:** <https://github.com/apache/cassandra/blob/cassandra-4.0/src/java/org/apache/cassandra/db/repair/PendingAntiCompaction.java>

The class-level comment states its purpose directly: isolate unrepaired SSTables for a token range into a **pending repair group** so they cannot be compacted with other SSTables while repair is in progress.

The inspected `AntiCompactionPredicate`:

- excludes already repaired SSTables when `metadata.repairedAt != UNREPAIRED_SSTABLE`;
- requires an SSTable format supporting pending repair;
- excludes/interlocks SSTables already pending another non-finalized incremental repair session;
- surfaces conflicting in-progress repair sessions as an error rather than silently mixing them.

### Claim control

This grounds:

```text
pending repair != repaired
pending repair != freely available unrepaired input for another conflicting session
```

and provides a source-level embodiment for the later repair-state handoff.

---

### P9 — Cassandra 4.0 `LocalSessions.java`: retained repair-session state

**Source:** `src/java/org/apache/cassandra/repair/consistent/LocalSessions.java`, branch `cassandra-4.0`.

**URL:** <https://github.com/apache/cassandra/blob/cassandra-4.0/src/java/org/apache/cassandra/repair/consistent/LocalSessions.java>

Directly inspected source shows local session persistence including:

- parent/session ID;
- `started_at`;
- `last_update`;
- `repaired_at`;
- session `state`;
- coordinator;
- participants;
- token ranges;
- table IDs.

The state-transition path validates allowed transitions, saves the session, and separately detects newly completed sessions. Prepare handling describes isolation of the data before a successful prepare response is sent. Failure handling refuses to convert a finalized session back to failed but explicitly transitions non-finalized sessions to `FAILED`.

### Claim control

This grounds that the 4.0 repair protocol retains more than one SSTable repaired bit: the in-progress maintenance relation has explicit session identity, participants, range/table scope, and state.

It does **not** establish modern Cassandra auto-repair; that is a separate later scheduler.

---

### S1/P-context — later Apache Reaper article as operational qualification

**Source:** Alexander Dejanovski, Apache Cassandra blog, **“Reaper: Anti-entropy Repair Made Easy,”** 28 September 2021.

**URL:** <https://cassandra.apache.org/_/blog/Reaper-Anti-entropy-Repair-Made-Easy.html>

The article describes operational complexity around repair and says incremental repair should be safely usable starting with Cassandra 4.0. It is useful as a later project-level qualification of the 3.x/4.0 boundary.

It is **not** used to redefine 3.11 historical behavior, and Reaper is not claimed as part of the Cassandra core implementation in this case.

---

## Related-repository check

Searches in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for:

- `Cassandra incremental repair`;
- `repairedAt`;
- `anti-compaction`;
- Cassandra Merkle repair;

found no dedicated overlapping technical-history case during this research slice.

Therefore this case stays in `technical-retention` as a bounded comparison of retained maintenance state. A future generic history of Cassandra repair/anti-entropy should live in or coordinate with `computing-archaeology` rather than being duplicated here.

---

## Claim ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| Cassandra 2.1 feature rationale explicitly proposed remembering successfully repaired SSTables so future repair could skip them | H/P | P1 | **grounded** |
| Cassandra 3.11 incremental repair excludes data once marked repaired | H/P | P2 | **grounded** |
| `repairedAt` is retained SSTable metadata | H/P | P3 | **grounded** |
| 3.11 anti-compaction can split one input into repaired and unrepaired outputs | H/P | P4 | **grounded** |
| a wholly repaired SSTable can be reclassified by metadata mutation without physical anti-compaction | H/P | P4 | **grounded** |
| 3.11 keeps repaired and unrepaired SSTables in distinct compaction-strategy populations | H/P | P5/P6 | **grounded** |
| running incremental repair once and abandoning it can make repaired/unrepaired separation impede tombstone reclamation | H/P | P6 | **grounded** |
| repaired status is not a perpetual present-integrity guarantee | H/P + E | P2 | **grounded** |
| legacy incremental-repair classification could become inconsistent across replicas | H/P | P7 | **grounded** |
| Cassandra 4.0 introduces pending-repair isolation before promotion to repaired | H/P | P7/P8 | **grounded** |
| 4.0 retains local repair-session state including repaired time, scope, participants, and state | H/P | P9 | **grounded** |
| past repair completion can be modeled as future-maintenance eligibility state | E | P1–P6 | **grounded reconstruction** |
| maintenance-state consistency can itself become a repair-subsystem correctness obligation | E | P7–P9 | **grounded reconstruction** |
| `repairedAt` is equivalent to current application-version authority | X | contradicted by role/scope in P2–P6 | **rejected** |
| 3.11 incremental repair was universally safe/reliable | X | qualified by P7 and later Apache context | **rejected** |
| Cassandra invented anti-entropy or Merkle repair | X | outside evidence; Case 23 already supplies earlier Dynamo comparator | **rejected** |
| `pendingRepair` existed in the original 2.1/3.11 mechanism | X | P7/P8 are later 4.0 evidence | **rejected** |

---

## Cross-case relations justified by this evidence

### 1. `past repair completion ≠ present health`

A repair classification can remain while later corruption/operator loss/bugs arise. The 3.11 documentation itself requires occasional full repair for these later fault classes.

### 2. `maintenance-history metadata ≠ payload`

The metadata does not carry user value, yet future incremental repair uses it to determine whether user-bearing SSTables are revisited.

### 3. `maintenance-state transition ≠ necessarily physical rewriting`

A completely covered SSTable can have `repairedAt` mutated without anti-compaction; partial coverage can require physical split.

### 4. `repair started ≠ repair successfully completed`

The 4.0 pending-repair model exists precisely to retain this distinction through the repair session.

### 5. `maintenance-history consistency ≠ automatic consequence of payload replication`

CASSANDRA-9143 documents a separate consistency problem in the classification of repaired data across replicas.

### 6. `lower repeated verification cost ≠ less maintenance state`

Incremental repair saves data comparison/streaming work by adding remembered repair state, anti-compaction organization, and later stronger session-state coordination.

### 7. `repair-history partitioning ≠ deletion state, while it can affect deletion reclamation`

The 3.11 compaction warning links repaired/unrepaired separation to tombstone-dropping opportunities. This composes with Case 41 without collapsing the two mechanisms.

---

## Prior-art boundary

The historical contribution claimed here is deliberately narrow.

CASSANDRA-5351 provides direct Apache evidence for a Cassandra-specific change: remembering successfully repaired SSTables to avoid re-repairing them by default, together with repaired/unrepaired compaction segregation.

It does not establish invention priority for:

- anti-entropy;
- Merkle trees;
- incremental verification;
- maintenance logs;
- transactional state machines.

[`Case 23`](../cases/23-amazon-dynamo-divergent-version-anti-entropy.md) already grounds Dynamo's 2007 Merkle-tree anti-entropy as an earlier distributed-store comparator. Similarity is functional, not a claim that CASSANDRA-5351 invented the general problem.

---

## Maturity decision

**Case 48: `grounded`.**

Grounding is justified because the central claim no longer rests on one documentation paragraph:

- feature intent is explicit in CASSANDRA-5351;
- future repair exclusion and its failure-model limits are explicit in versioned 3.11 docs;
- persisted `repairedAt` is directly visible in 3.11 source;
- anti-compaction and repaired/unrepaired physical separation are directly visible in 3.11 source;
- separate compaction populations are directly visible in 3.11 source/docs;
- the inconsistency of repair classification is directly documented in CASSANDRA-9143;
- the 4.0 pending/session repair-state correction is directly visible in Apache issue history and source.

Remaining work is narrower than this case:

- post-4.0 incremental-repair evolution and modern auto-repair;
- independent fault-injection reproducing repair-state failures;
- exact release-by-release transition from legacy `repairedAt` to pending-repair implementation;
- Reaper/external scheduler history;
- broader anti-entropy genealogy;
- empirical interaction between modern repair state and tombstone/compaction policies.
