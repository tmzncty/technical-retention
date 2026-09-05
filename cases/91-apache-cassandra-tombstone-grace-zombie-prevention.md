# Apache Cassandra Tombstone Grace: Retaining Deletion Evidence to Prevent Zombie Resurrection

## Scope

- **Bounded system:** Apache Cassandra's 1.2-era deletion/compaction semantics, checked against the `cassandra-1.2.19` source tag; later Apache documentation is used only as an institutional clarification of the distributed tombstone model, not as proof that every modern option existed in 1.2.
- **Bounded mechanism:** timestamped deletion markers (`DeletedColumn` / tombstones), `gc_grace_seconds`, compaction-time purge eligibility, overlap checks against older SSTables, and the risk that a stale surviving replica can reintroduce a pre-delete value after deletion evidence has been forgotten.
- **Research question:** why can a distributed store need to retain evidence that a value was deleted, and what must become true before that negative evidence can itself be safely forgotten?

This is **not** a general history of Cassandra, Dynamo-style replication, SSTables, anti-entropy repair, hinted handoff, compaction strategies, TTL, or secure deletion. The case isolates one retention paradox: **logical forgetting can require temporarily retaining a deletion record.**

The bounded retention claim is:

> **Cassandra does not make a distributed deletion durable merely by making an old value locally absent. It records a timestamped deletion marker, keeps that negative/currentness evidence through a grace interval, and lets compaction purge it only under additional local shadowing constraints. If the deletion evidence disappears while an older replica or SSTable version can still become authoritative again, deleted data can reappear. Correct forgetting therefore depends on retaining, propagating, and only later retiring a record of forgetting.**

`negative currentness evidence`, `distributed forgetting witness`, `purge admissibility`, and `absence is not self-authenticating` below are **project engineering terms**, not historical Cassandra vocabulary.

---

## Historical vocabulary

The bounded sources use:

- `tombstone`;
- `DeletedColumn`;
- `markedForDeleteAt` / deletion timestamp;
- `localDeletionTime`;
- `gc_grace_seconds`;
- `gcBefore`;
- `compaction`;
- `purge` / `drop tombstones`;
- `SSTable`;
- `repair`;
- later Apache documentation uses `zombie` for deleted data that reappears from a stale replica.

Do not silently rename the marker as a transaction rollback record, secure-erase certificate, consensus tombstone, or filesystem journal revoke record.

---

## Historical record

### H/P — deletion is represented by a retained marker rather than immediate absence

Apache's Cassandra documentation describes a delete as the insertion of a timestamped deletion marker called a tombstone. The marker goes through the write path and can be written to SSTables; reads suppress values with timestamps older than the tombstone.

The exact `cassandra-1.2.19` source gives this negative state a concrete implementation embodiment. `DeletedColumn` is a `Column` subclass whose `isMarkedForDelete()` returns true, whose deletion timestamp is returned by `getMarkedForDeleteAt()`, whose local deletion time is retained in its value bytes, and whose serialization carries a deletion flag.

So the bounded historical fact is stronger than “deleted data is gone”:

```text
old value may still exist in an immutable SSTable
        +
newer retained deletion marker
        -> old value is no longer current for reads
```

**Primary anchors:** Apache Cassandra tombstone documentation; `DeletedColumn.java`, tag `cassandra-1.2.19`.

### H/P — Cassandra 1.2.19 gives user tables a ten-day default grace interval

`CFMetaData.java` in the `cassandra-1.2.19` tag defines `DEFAULT_GC_GRACE_SECONDS = 864000`, i.e. ten days. Modern Apache documentation preserves the same default and explains the grace interval as time during which tombstones remain available so lagging/unavailable replicas have an opportunity to learn the deletion before the marker becomes purge-eligible.

This supports a narrow statement: **the deletion marker has its own retention policy and lifetime distinct from the deleted user value.**

**Primary anchors:** `CFMetaData.java`, tag `cassandra-1.2.19`; Apache Cassandra tombstone documentation.

### H/P — elapsed grace is not the same thing as immediate physical removal

Apache documentation states that after `gc_grace_seconds` expires a tombstone *may* be removed, but it is not removed merely because the clock crossed the threshold: removal occurs during compaction. It also explains the shadowing constraint: if the tombstone is in one SSTable while an older value for the same partition can survive in another, compaction must include the relevant older data before the tombstone can be dropped safely.

The 1.2.19 implementation exposes the same local admissibility idea in `CompactionController.shouldPurge`. Its comment defines the condition as knowing that all versions of the row are included in the compaction set, and the method refuses purge when an overlapping SSTable may contain a version with a timestamp at or before the deletion timestamp.

Thus:

```text
grace threshold crossed
    != tombstone physically gone
    != safe purge by time alone
```

**Primary anchors:** `CompactionController.java`, tag `cassandra-1.2.19`; Apache Cassandra tombstone documentation.

### H/P — stale replicas can make physical survival conflict with logical deletion

Apache's documentation gives the distributed failure mode explicitly. If one replica misses a delete, it can retain the pre-delete value while other replicas retain the tombstone. If the tombstone disappears from the rest of the cluster before that stale replica is reconciled, the surviving old value can be propagated back and reappear; the documentation calls this a `zombie`.

The retention problem is therefore not lack of physical persistence. The dangerous object is often **too persistent**: an old value survives perfectly well, but the negative/currentness evidence that disqualifies it no longer does.

**Institutional anchor:** Apache Cassandra tombstone documentation.

### H/P — CASSANDRA-7810 shows that purge ordering matters even without a remote stale replica

Apache issue CASSANDRA-7810, fixed for 1.2.19, 2.0.11, and 2.1.0, reports a single-node reproduction with `gc_grace_seconds = 0`: insert a row, delete it, flush and compact, and the deleted row reappears. The issue diagnosis is that tombstones were considered obsolete and discarded before being locally applied correctly during compaction.

`CHANGES.txt` for 1.2.19 records the corresponding change as `Track expired tombstones (CASSANDRA-7810)`.

This is an important counterexample to an overly simple distributed story. **Even when no replica is missing, “tombstone is old enough to collect” is not sufficient if the compaction operation forgets the deletion witness before it has finished using that witness to suppress older local data.**

**Primary/institutional anchors:** ASF JIRA CASSANDRA-7810; Cassandra `CHANGES.txt`, tag `cassandra-1.2.19`.

### H/P — deletion-marker compaction is older than Cassandra

Google's 2006 Bigtable paper describes non-major-compaction SSTables containing `special deletion entries` that suppress deleted data in older live SSTables; a major compaction can then produce an SSTable containing neither deletion information nor the deleted data. This is direct prior art for deletion markers whose retention is temporarily necessary because older immutable representations remain live.

Accordingly, this case does **not** claim that Cassandra invented tombstones, deletion markers, immutable-SSTable delete suppression, or compaction-mediated reclamation.

**Primary anchor:** Chang et al., “Bigtable: A Distributed Storage System for Structured Data,” OSDI 2006, §5.4.

---

## Retained state

### 1. Older user-value embodiments

A pre-delete value can remain in an immutable SSTable or on a lagging replica after the application has issued a delete.

### 2. Tombstone / `DeletedColumn`

The deletion marker carries a deletion timestamp/currentness relation and local deletion time. It is a retained state in its own right.

### 3. Grace / purge-threshold state

`gc_grace_seconds` supplies a time policy for when a tombstone can become eligible for collection. It is not a proof that all stale replicas are repaired.

### 4. Compaction overlap knowledge

The local engine must know whether older versions can remain outside the compaction set. That knowledge contributes to whether dropping the marker is locally admissible.

### 5. Replica/reconciliation state

At cluster level, safe operational deletion depends on whether replicas that could later return old data have learned or otherwise ceased to be able to reintroduce the pre-delete value. This case does not reconstruct the entire repair protocol.

---

## Retention mechanism

A simplified three-replica path is:

```text
before delete:
    R1: A@10
    R2: A@10
    R3: A@10

R3 becomes unavailable

delete A at timestamp 20:
    R1: A@10 + tombstone@20
    R2: A@10 + tombstone@20
    R3: A@10

while deletion evidence is retained:
    reads on R1/R2 suppress A@10
    compaction must not discard tombstone@20 while relevant older A can survive
    repair/reconciliation can propagate the deletion relation to R3

after the stale value can no longer legitimately win:
    old A embodiments and then obsolete deletion evidence can be reclaimed
```

Unsafe early retirement instead yields:

```text
R1/R2 forget tombstone@20
R3 still retains A@10
    -> A@10 is no longer opposed by retained deletion evidence
    -> reconciliation can make A visible again
```

The exact topology is illustrative. The sourced mechanism is that **negative state must survive long enough to dominate older positive state across the system's reconciliation and compaction boundaries.**

---

## Engineering reconstruction

### E — logical deletion ≠ physical disappearance

A newer tombstone can make an older value non-current while the older bytes still exist in another SSTable or replica.

### E — tombstone ≠ deleted payload

The marker is not a second copy of the deleted value. It is compact negative/currentness evidence saying that older value versions are no longer admissible.

### E — local deletion ≠ cluster-wide forgetting

One node can correctly suppress a value while another unavailable node still holds a pre-delete version.

### E — physical survival ≠ currentness

A stale replica's old value can remain perfectly readable while being logically superseded by a deletion timestamp.

### E — grace expiry ≠ immediate purge

Crossing the grace threshold creates eligibility. Compaction is a later operation.

### E — grace expiry ≠ sufficient local purge authority

The 1.2.19 compaction controller still checks whether older shadowed versions may remain outside the compaction set.

### E — time policy ≠ proof of distributed convergence

A ten-day grace interval is an operational assumption/window, not cryptographic or consensus proof that every possible stale replica has learned the deletion.

### E — forgetting can require retained negative evidence

To make a value stay forgotten in a replicated system, Cassandra temporarily preserves a record whose purpose is to say that an older surviving value must not count.

### E — forgetting the forgetting record too early can restore the old value

The zombie failure is not a paradox once currentness metadata is separated from payload survival: old positive state survives, negative authority disappears, and the old state becomes admissible again.

### E — safe purge is a closure relation, not just an age test

At minimum in the local compaction path, the deletion marker must remain until relevant older versions are included/suppressed. At cluster level, replica reconciliation adds a further operational boundary.

### E — CASSANDRA-7810 proves purge sequencing is semantically significant

Even a single-node compaction can resurrect data if expired deletion markers are discarded before their suppressive effect is applied to older local representations.

### E — tombstone collection ≠ secure sanitization

Dropping a Cassandra deletion marker and old logical rows during compaction says nothing by itself about forensic erasure of underlying disk/SSD media, remapped sectors, snapshots, or backups.

---

## Functional analogies and limits

### A — Case 74 JBD revoke

Both cases retain **negative evidence** that suppresses older surviving state. JBD revoke is transaction-relative recovery metadata that prevents an older journal record from being replayed onto a reused block. Cassandra tombstones are timestamped database deletion/currentness state that must coexist with immutable SSTables and distributed replicas. This is a functional comparison, not genealogy.

### A — Case 73 GFS deferred deletion

Both systems separate a user-visible delete from later reclamation. GFS uses namespace renaming/reference retirement and later chunk cleanup; Cassandra writes a timestamped negative record that beats older value versions. Similar temporal shape does not make the mechanisms identical.

### A — Case 90 Kafka lineage-qualified truncation

Both show that a physically surviving older state need not remain authoritative. Kafka rejects a divergent suffix by leader-epoch lineage; Cassandra rejects an older value by timestamped deletion state. No historical descent is claimed.

### A — Case 44 deallocation / sanitization

Both reinforce that logical unavailability is weaker than secure physical erasure. A Cassandra tombstone is a database-currentness mechanism, not a sanitize primitive.

---

## Prior-art and genealogy boundary

Do **not** claim:

- Cassandra invented tombstones or deletion-marker compaction;
- Bigtable's `special deletion entries` and Cassandra `DeletedColumn` are implementation-identical merely because they serve a comparable function;
- `gc_grace_seconds` proves all replicas have converged when it expires;
- every modern Cassandra tombstone option existed in 1.2.19 — in particular, later `only_purge_repaired_tombstones` behavior must not be projected backward;
- tombstone purge securely erases old data from physical media, backups, snapshots, or forensic remnants;
- the 1.2.19 source inspected here establishes the complete historical genealogy of Cassandra repair/hinted-handoff deletion propagation.

The broader Bigtable/LSM/Cassandra storage-engine genealogy belongs in `computing-archaeology` if developed later. This case uses Bigtable only as an earlier primary prior-art witness and keeps the retention-specific argument here.

---

## Philosophical interpretation — bounded

### I — absence is not self-authenticating in a distributed store

A future operation cannot infer from one node's absence of a value that the system as a whole has forgotten it. Another embodiment can still exist and later become visible. Cassandra therefore materializes deletion as a positive technical trace: a retained marker that authorizes the interpretation of older surviving data as no longer current.

### I — forgetting can have a memory phase

In this bounded mechanism, forgetting is not the instant conversion of `something` into `nothing`. It has a period in which the system remembers **that the thing must count as forgotten**. Only after the relevant older representations have lost their ability to reassert themselves can that negative memory itself become disposable.

These are project interpretations, not claims that Cassandra developers used this philosophical vocabulary.

---

## What would falsify or narrow this case

- evidence that `cassandra-1.2.19` did not represent column deletion with the inspected `DeletedColumn` timestamp/local-deletion state would require rewriting the implementation claim;
- evidence that `CompactionController.shouldPurge` was not on the relevant 1.2.19 tombstone-removal path would narrow the local purge-admissibility argument;
- a version-specific repair regime that permits safe zero-grace deletion under additional guarantees would not falsify this case, but it would require naming those stronger guarantees explicitly;
- evidence that the modern Apache `zombie` explanation does not accurately describe the historical 1.2 distributed failure envelope would require separating the modern explanatory vocabulary more sharply from the 1.2 implementation record.

---

## Remaining work deliberately left open

- exact pre-1.2 Cassandra tombstone implementation genealogy;
- direct source reconstruction of repair/hinted-handoff deletion propagation for one exact early release;
- later `only_purge_repaired_tombstones`, repair-aware tombstone GC, and modern compaction evolution;
- range tombstones, partition tombstones, TTL-expiry variants, and newer storage-engine encodings;
- named production incidents beyond CASSANDRA-7810;
- secure deletion / SSD forensic behavior after Cassandra-level compaction;
- a full Bigtable → Cassandra / LSM deletion genealogy in `computing-archaeology`.

---

## Sources

See [`../evidence/91-cassandra-2006-2014-tombstone-grace-grounding.md`](../evidence/91-cassandra-2006-2014-tombstone-grace-grounding.md).
