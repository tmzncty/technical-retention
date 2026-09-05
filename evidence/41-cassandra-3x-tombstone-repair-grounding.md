# Case 41 Grounding — Cassandra 3.x Tombstones, GC Grace, and Repair

## Purpose

This record grounds [`cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md`](../cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md).

The bounded question is not whether Cassandra has a delete operation. It is whether Apache's own 3.x documentation and implementation establish the stronger retention relation used by the case:

```text
delete accepted
    -> negative tombstone state retained
    -> stale positive replicas may still exist
    -> delivery/repair can propagate deletion
    -> age alone does not physically purge tombstone
    -> compaction/overlap and optionally repaired-state qualify reclamation
    -> loss of deletion evidence before stale replicas are reconciled can resurrect older data
```

## Source hierarchy

### P1 — Apache Cassandra 3.11 compaction documentation

**URL:** <https://cassandra.apache.org/doc/3.11/cassandra/operating/compaction/index.html>

Directly establishes:

- DELETE does not immediately remove underlying data;
- Cassandra writes a `tombstone` representing the delete;
- older values are suppressed by the tombstone;
- the design is tied to Cassandra's distributed nature;
- the documentation's explicit three-node counterexample shows repair resurrecting `[A]` if no tombstone exists;
- with tombstones, repair propagates the deletion marker instead;
- `gc_grace_seconds` controls how long tombstones are retained through compaction before removal;
- the duration should reflect expected failed-node recovery time;
- default `gc_grace_seconds = 864000` (10 days) in this documentation;
- expiry alone is insufficient: compaction and overlapping older SSTable conditions still govern removal;
- `only_purge_repaired_tombstones` can require repaired status before purge;
- a node disconnected longer than `gc_grace_seconds` can allow deleted data to be repaired back into the cluster;
- tombstones are not removed merely because grace has elapsed; compaction is still required.

**Evidence strength:** primary Apache project documentation for the bounded release family.

### P2 — Apache Cassandra 3.11 hints documentation

**URL:** <https://cassandra.apache.org/doc/3.11/cassandra/operating/hints.html>

Directly establishes:

- coordinators retain temporary hints for unavailable replicas;
- hints are replayed after a replica returns;
- hints are `best effort`;
- hints do not guarantee eventual consistency the way anti-entropy repair does;
- the documented default `max_hint_window_in_ms` is three hours;
- a replica unavailable past the hint window remains out of sync until another repair path propagates the mutation.

**Evidence use:** separates temporary delivery assistance from the tombstone grace window and from anti-entropy repair.

### P3 — Apache Cassandra `NEWS.txt`, 3.x history

**URL:** <https://github.com/apache/cassandra/blob/cassandra-3.11/NEWS.txt>

The release history records:

- an option to not purge unrepaired tombstones;
- its explicit rationale: avoid users having data resurrected if repair has not run within `gc_grace_seconds`;
- the option name `only_purge_repaired_tombstones`;
- the counter-cost: without repair for a long time, retained tombstones can themselves cause problems.

**Evidence use:** strong historical Apache vocabulary for the repair-qualified reclamation relation. This source supports `resurrected` directly; the case does not need to project the later convenient word `zombie` backward.

### P4 — `AbstractCompactionStrategy.java`, branch `cassandra-3.11`

**URL:** <https://github.com/apache/cassandra/blob/cassandra-3.11/src/java/org/apache/cassandra/db/compaction/AbstractCompactionStrategy.java>

Directly inspected implementation evidence includes:

```text
ONLY_PURGE_REPAIRED_TOMBSTONES = "only_purge_repaired_tombstones"
```

alongside tombstone-compaction controls.

**Evidence use:** confirms the release-family option exists in implementation, rather than being merely prose documentation.

### P5 — `RepairedDataTombstonesTest.java`, branch `cassandra-3.11`

**URL:** <https://github.com/apache/cassandra/blob/cassandra-3.11/test/unit/org/apache/cassandra/db/RepairedDataTombstonesTest.java>

Directly inspected tests create tables with:

```text
gc_grace_seconds=0
only_purge_repaired_tombstones=true
```

and distinguish repaired from unrepaired SSTables/tombstones. The test comments explicitly expect expired tombstones to be purged from repaired state while unrepaired tombstones are retained.

**Evidence use:** executable project evidence that `repaired` status is operational reclamation state, not merely an administrator label.

### P6 — current Apache Cassandra tombstone documentation

**URL:** <https://cassandra.apache.org/doc/latest/cassandra/managing/operating/compaction/tombstones.html>

Used only as a later continuity/terminology check. Current Apache documentation uses `zombie` for deleted data that persists on a stale replica and can propagate after the tombstone is gone.

**Boundary:** later terminology is not silently attributed to every earlier Cassandra release.

---


## Historical deepening — exact 1.2.19 artifacts, CASSANDRA-7810, and Bigtable prior art

This section absorbs the unique evidence from the now-consolidated duplicate case. It does not change the canonical Case 41 thesis; it gives that thesis a deeper historical and implementation floor.

### P7 — Apache Cassandra `DeletedColumn.java`, tag `cassandra-1.2.19`

**URL:** <https://github.com/apache/cassandra/blob/cassandra-1.2.19/src/java/org/apache/cassandra/db/DeletedColumn.java>

Directly inspected implementation facts retained from the older evidence slice:

- `DeletedColumn` extends `Column`;
- `isMarkedForDelete()` returns true;
- `getMarkedForDeleteAt()` returns the column timestamp;
- `getLocalDeletionTime()` decodes retained local deletion time;
- serialization uses `ColumnSerializer.DELETION_MASK`.

**Use:** strong primary implementation evidence that a deletion marker is first-class retained database state, not mere absence.

**Boundary:** this does not describe every later Cassandra tombstone kind or encoding.

### P8 — Apache Cassandra `CFMetaData.java`, tag `cassandra-1.2.19`

**URL:** <https://github.com/apache/cassandra/blob/cassandra-1.2.19/src/java/org/apache/cassandra/config/CFMetaData.java>

`DEFAULT_GC_GRACE_SECONDS = 864000` provides an exact 1.2.19 implementation witness for the ordinary user-table ten-day default.

**Use:** grounds a historical retention-policy timescale distinct from deleted-value lifetime.

**Boundary:** a configured time window is not proof of repair or global convergence.

### P9 — Apache Cassandra `CompactionController.java`, tag `cassandra-1.2.19`

**URL:** <https://github.com/apache/cassandra/blob/cassandra-1.2.19/src/java/org/apache/cassandra/db/compaction/CompactionController.java>

`shouldPurge(key, maxDeletionTimestamp)` checks overlapping SSTables and refuses purge when an overlapping SSTable may still contain an older version at or before the deletion timestamp.

**Use:** direct implementation evidence that elapsed grace is not the complete local purge condition; older shadowed representations outside the compaction set remain relevant.

**Boundary:** this is local compaction admissibility, not proof that every distributed replica has converged.

### P10 — CASSANDRA-7810 and Cassandra 1.2.19 `CHANGES.txt`

**Issue:** <https://issues.apache.org/jira/browse/CASSANDRA-7810>

**Release record:** <https://github.com/apache/cassandra/blob/cassandra-1.2.19/CHANGES.txt>

The ASF defect record reproduces a deleted row reappearing on a **single node** with `gc_grace_seconds = 0` after flush/compaction, and records fix versions 1.2.19, 2.0.11, and 2.1.0. The 1.2.19 change record includes `Track expired tombstones (CASSANDRA-7810)`.

**Use:** strong project/institutional evidence that purge sequencing itself is semantically significant: a tombstone can be old enough to collect yet still be needed to suppress an older local representation during the current compaction operation.

**Boundary:** this one defect does not explain every Cassandra resurrection bug.

### P11 — Chang et al., Bigtable, OSDI 2006, §5.4

**HTML proceedings:** <https://static.usenix.org/event/osdi06/tech/chang/chang_html/>

The paper states that SSTables produced by non-major compactions can contain `special deletion entries` that suppress deleted data in older live SSTables; a major compaction can later produce an SSTable with neither deletion information nor deleted data.

**Use:** earlier primary prior art for temporarily retaining deletion evidence across immutable representations and later retiring it through a stronger compaction closure.

**Boundary:** prior function is not implementation identity and does not prove a direct Bigtable → Cassandra genealogy.

### Cross-version claim controls added by the deepening

| Claim | Type | Grounding | Boundary |
| --- | --- | --- | --- |
| Cassandra 1.2.19 represents column deletion with explicit `DeletedColumn` state | `H/P` | P7 | exact tagged implementation, not every later encoding |
| 1.2.19 ordinary user-table default grace is 864000 seconds | `H/P` | P8 | policy default, not convergence proof |
| older overlapping SSTable state can block local tombstone purge | `H/P` | P9 | local compaction relation only |
| CASSANDRA-7810 resurrected a deleted row on one node when expired tombstones were discarded too early | `H/P` | P10 | one historical defect class |
| deletion-marker retention across immutable SSTables predates Cassandra | `H/P` prior art | P11 | functional prior art, not direct genealogy |
| `only_purge_repaired_tombstones` existed in Cassandra 1.2.19 | `X` | contradicted by version boundary used here | rejected |
| Bigtable deletion entries and Cassandra tombstones are implementation-identical | `X` | none | rejected |

---

## Claim ledger

| Claim | Type | Grounding | Boundary |
| --- | --- | --- | --- |
| Cassandra DELETE writes tombstone state rather than immediately removing underlying data | H/P | P1 | release-family scoped |
| Tombstone suppresses older values | H/P | P1 | does not imply physical erasure |
| Repair can resurrect data if deletion evidence is absent | H/P | P1, P3 | bounded documented scenario, not claim every repair does so |
| Tombstone-bearing repair propagates deletion instead of stale positive value | H/P | P1 | depends on currentness evidence present in the bounded scenario |
| `gc_grace_seconds` retains tombstones for a failure/recovery envelope | H/P + E | P1 | timer is not itself repair |
| Grace expiry does not imply immediate physical purge | H/P | P1 | compaction/overlap still matter |
| Repaired/unrepaired status can gate tombstone purge | H/P | P1, P3, P4, P5 | option-specific, not universal default behavior |
| Hints are best effort and distinct from anti-entropy repair | H/P | P2 | hint window is not a convergence proof |
| Negative-state retention can be constitutive of successful forgetting | E | P1–P5 | project formulation |
| Forgetting deletion evidence can restore an older payload to current service | E | P1, P3 | project synthesis of documented resurrection scenario |
| Repair-qualified forgetting trades retained-control-state cost against resurrection risk | E | P3, P5 | no universal optimum implied |
| Cassandra tombstone mechanism is historically identical to Swift tombstones | X | none | functional analogy only |
| Tombstone reclamation is secure media erasure | X | none | explicitly out of scope |
| Cassandra invented tombstones or anti-entropy | X | none | no priority claim |

---

## Cross-case controls

### Case 28 — OpenStack Swift tombstones

Shared functional relation:

```text
negative state must remain long enough to defeat stale positive state
```

Do not collapse mechanisms:

- Swift 2.10.1: `.ts`, timestamp ordering, `reclaim_age`, replication/reconstruction, Swift consistency-window semantics;
- Cassandra 3.x: tombstones in LSM/SSTable state, `gc_grace_seconds`, compaction overlap, hints, repair, optional repaired-state gating.

### Case 23 — Amazon Dynamo

Shared functional relation: temporary write-delivery mechanisms and later anti-entropy/convergence can be distinct.

Boundary: Dynamo's vector-clock concurrent-version model is not Cassandra's tombstone reclamation model.

### Case 04 — mapped Flash

Shared functional relation: logical currentness can change before every old physical embodiment disappears.

Boundary: Flash invalidation/reclamation is an erase/mapping problem within a device; Cassandra resurrection is a distributed replica/currentness problem.

---

## Related-repository check

Search of `tmzncty/computing-archaeology` for Cassandra tombstones, `gc_grace_seconds`, zombie/resurrection deletion, and related repair wording returned no dedicated case during this slice.

Therefore this contribution does not duplicate an existing mechanism history there. If a broader Cassandra architecture history is later added to `computing-archaeology`, this case should retain only the deletion/retention comparison and link outward.

---

## Evidence limits

1. This record is centered on Cassandra 3.x/3.11 documentation and branch implementation; it is not a cross-version Cassandra semantics history.
2. It does not prove every stale-replica scenario produces resurrection; it grounds the failure class and the documented conditions.
3. It does not equate `gc_grace_seconds` with successful repair.
4. It does not equate hint retention with tombstone retention.
5. It does not equate tombstone removal with physical sanitization.
6. It does not treat `only_purge_repaired_tombstones` as a cost-free universal recommendation.
7. It does not make invention-priority claims.

## Status decision

**Case 41: `grounded`.**

Reason: the central retention/reclamation/resurrection relation is directly documented by Apache; source and tests independently confirm the repaired-tombstone gating mechanism; the repair/hint boundary is explicit in official documentation; and cross-case analogy boundaries are controlled.
