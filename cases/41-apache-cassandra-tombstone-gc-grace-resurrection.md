# Apache Cassandra GC Grace: Tombstone Retention, Repair Windows, and Data Resurrection

## Scope

- **Bounded system:** Apache Cassandra 3.x operational semantics, using the Cassandra 3.11 documentation/branch as the principal inspected artifact and the 3.x `NEWS.txt` record for the repaired-tombstone option.
- **Bounded mechanism:** deletion tombstones, `gc_grace_seconds`, compaction-time tombstone purging, repair, hinted handoff, and the `only_purge_repaired_tombstones` safety option.
- **Primary source base:** Apache Cassandra 3.11 official documentation, Apache Cassandra source/tests on the `cassandra-3.11` branch, and Apache Cassandra `NEWS.txt`.
- **Research question:** why can a distributed system need to retain evidence of deletion, and why can forgetting that evidence too early cause older positive data to become current again?

This is **not** a general history of Cassandra, LSM trees, eventual consistency, anti-entropy, or distributed deletion. It does not claim Cassandra invented tombstones, hinted handoff, repair, or grace-period reclamation.

The bounded retention claim is:

> **In Cassandra 3.x, a delete is represented by retained tombstone state because replicas may temporarily disagree. Tombstone reclamation is therefore constrained not only by age but by compaction overlap and, optionally, repair evidence; if deletion evidence disappears while an isolated replica still retains an older value, later repair can make that older value reappear.**

That sentence is an **engineering reconstruction** from Apache's documented and implemented behavior. `negative-state retention`, `anti-resurrection evidence`, `safe-forgetting condition`, and `repair-qualified forgetting` below are project terms, not Cassandra historical vocabulary.

---

## Historical vocabulary

The bounded Apache sources directly use:

- `tombstone`;
- `gc_grace_seconds`;
- `compaction`;
- `repair` / `anti-entropy repair`;
- `hint` / `hinted handoff`;
- `max_hint_window_in_ms`;
- `repaired` / `unrepaired` SSTables;
- `only_purge_repaired_tombstones`;
- `resurrected` / `resurrected data` in the 3.x documentation and release notes.

Later/current Apache documentation also uses the convenient term `zombie` for this failure mode, but this case does not require that later label to explain the 3.x mechanism.

The following are **project terms only**:

- `negative-state retention` — retaining a state whose operational meaning is that an older positive value must not be admitted as current;
- `anti-resurrection evidence` — retained delete/currentness evidence required to stop an isolated stale replica from restoring older data;
- `safe-forgetting condition` — the conditions under which the tombstone may be reclaimed without violating the bounded distributed-currentness objective;
- `repair-qualified forgetting` — tying reclamation eligibility to evidence that repair has occurred.

---

## Historical record

### H/P — DELETE writes a tombstone instead of immediately removing the underlying value

Apache Cassandra 3.11 documentation states that when Cassandra receives a delete request it **does not actually remove the data from the underlying store**. It writes a special piece of data called a tombstone. The tombstone represents the delete and prevents values older than that tombstone from appearing in queries.

Apache explicitly explains this design through Cassandra's distributed nature.

**Primary anchor:** Apache Cassandra 3.11, `Operating > Compaction > Tombstones and Garbage Collection (GC) Grace`, `Why Tombstones`.

### H/P — without retained deletion evidence, repair can resurrect an older value

The same documentation gives a three-replica example. If one replica is unavailable during deletion and deletion were represented only by removing local values, the cluster could become:

```text
[], [], [A]
```

A later repair would then copy `A` back to the two empty replicas, yielding:

```text
[A], [A], [A]
```

Apache explicitly calls this data being **resurrected even though it had been deleted**.

With tombstones, the available replicas instead retain deletion evidence and later repair propagates the tombstone to the stale replica.

**Primary anchor:** Apache Cassandra 3.11 compaction documentation, `Deletes without tombstones` and `Deletes with Tombstones`.

### H/P — `gc_grace_seconds` is a retention window, not an immediate-delete timer

The 3.11 documentation says table-level `gc_grace_seconds` controls how long Cassandra retains tombstones through compaction events before removing them. It says the duration should directly reflect how long a user expects to allow before recovering a failed node. The documented default is `864000` seconds, or ten days.

The same source explicitly warns that a node down or disconnected longer than `gc_grace_seconds` can allow deleted data to be repaired back into the cluster.

**Primary anchor:** Apache Cassandra 3.11 compaction documentation, `The gc_grace_seconds parameter and Tombstone Removal`.

### H/P — expiry alone does not remove a tombstone

Apache 3.11 documents additional compaction conditions. A tombstone must be older than `gc_grace_seconds`, and compaction must include the SSTable containing the tombstone together with older overlapping data that it shadows. The documentation also says explicitly that tombstones are not removed merely because the grace interval elapsed; a compaction event is required.

This blocks a simplistic model:

```text
gc_grace_seconds expires
    -> tombstone physically disappears immediately
```

**Primary anchor:** Apache Cassandra 3.11 compaction documentation, lines/section on tombstone removal conditions.

### H/P — repaired/unrepaired state can become part of reclamation eligibility

Apache's 3.x `NEWS.txt` records an option to **not purge unrepaired tombstones**. Its rationale is explicit: avoid data resurrection if repair has not run within `gc_grace_seconds`. The option is named `only_purge_repaired_tombstones`.

The release note also gives the other side of the tradeoff: if repair is not run for a long time, tombstones can accumulate and cause other problems.

The `cassandra-3.11` source defines `ONLY_PURGE_REPAIRED_TOMBSTONES`, and branch unit tests construct tables with `gc_grace_seconds=0` plus `only_purge_repaired_tombstones=true`; repaired tombstones are allowed to purge while unrepaired tombstones remain.

**Primary anchors:** Apache Cassandra `NEWS.txt`; `src/java/org/apache/cassandra/db/compaction/AbstractCompactionStrategy.java`; `test/unit/org/apache/cassandra/db/RepairedDataTombstonesTest.java`, branch `cassandra-3.11`.

### H/P — hinted handoff is temporary assistance, not a replacement for repair

The Cassandra 3.11 hints documentation says coordinators can retain temporary hints for unavailable replicas and replay them after those replicas return. It also explicitly calls hints **best effort** and says they do not guarantee eventual consistency the way anti-entropy repair does.

The documented `max_hint_window_in_ms` default is three hours. If a node remains unavailable beyond that window, it can remain out of sync until read repair or full/incremental anti-entropy repair propagates the mutation.

This gives two different retention windows with different meanings:

- hint retention supports a missed mutation delivery path;
- tombstone grace constrains when deletion evidence may be forgotten.

They must not be treated as one timer or one guarantee.

**Primary anchor:** Apache Cassandra 3.11, `Operating > Hints`.

---

## Retained state

The bounded regime retains several different kinds of state.

### 1. Positive value embodiments

An unavailable replica may continue to retain an older value after other replicas have accepted a deletion.

### 2. Tombstone / deletion state

The tombstone carries timestamped negative currentness: values older than it should no longer count as current query results.

### 3. Repair relation

Replica agreement is not instantaneous. The system needs maintenance paths that can propagate missing mutations or reconcile inconsistent replicas.

### 4. Repaired/unrepaired status

Incremental repair and anticompaction distinguish repaired from unrepaired SSTables. With `only_purge_repaired_tombstones`, that state directly affects whether expired tombstones are eligible to disappear.

### 5. Compaction/overlap relation

A tombstone cannot safely be dropped merely because it is old if older shadowed data remains outside the compaction set.

### 6. Hint state

Hints are temporary retained mutations for unavailable replicas. They can shorten inconsistency duration but do not substitute for the stronger repair relation.

The client-visible result `not found` is therefore supported by several hidden states that can outlive the DELETE request itself.

---

## Retention mechanism

A simplified bounded sequence is:

```text
positive value replicated
    -> one replica becomes unavailable
    -> DELETE reaches available replicas
    -> available replicas retain tombstone state
    -> unavailable replica may still retain older value
    -> hints may deliver the missed deletion if outage is short
    -> anti-entropy/read repair can reconcile replicas later
    -> tombstone becomes age-eligible after gc_grace_seconds
    -> compaction/overlap checks decide whether it can actually be purged
    -> optional repaired-state rule can postpone purge until repair evidence exists
```

The important point is that **time, repair, and physical reclamation are separate relations**.

---

## Addressing and read semantics

The logical key remains stable while replicas can temporarily disagree about which timestamped state is admissible. Reads and repair therefore depend on currentness ordering, not merely on whether some physical bytes exist.

A stale positive value can be physically readable and still be noncurrent while a newer tombstone exists. If the tombstone has been reclaimed everywhere that could defeat the stale value, the same positive bytes can become dangerous again during repair.

So:

```text
physical presence
    != current admissibility

and

absence of a tombstone
    != proof that no stale positive embodiment survives elsewhere
```

---

## Write, deletion, and reclamation semantics

A DELETE in this regime must be separated into at least four events:

1. create/propagate negative currentness state;
2. suppress older positive state in queries and reconciliation;
3. converge replicas through hints/read repair/anti-entropy repair;
4. later reclaim tombstone storage through compaction when the applicable safety conditions allow it.

The fourth event is **not secure erasure** of all historical bytes. This case does not address media sanitization.

---

## Time

Relevant timescales include:

- client DELETE latency;
- replica outage duration;
- `max_hint_window_in_ms`;
- read-repair / anti-entropy-repair cadence;
- `gc_grace_seconds`;
- compaction scheduling;
- the age/overlap relation of SSTables;
- the longer operational lifetime of stale positive copies on unavailable media.

This is a protocol/maintenance time structure, not a physical-decay deadline like DRAM refresh.

---

## Failure / forgetting modes

Keep these distinct:

- deletion mutation not reaching one replica;
- hints expiring or failing to deliver the mutation;
- repair not occurring before the grace relation becomes unsafe;
- tombstone reclamation while a stale replica can still re-enter;
- compaction failing to include all older shadowed data;
- loss of repair/currentness evidence;
- operator configuration of a grace window shorter than the real outage/repair envelope;
- indefinitely retaining tombstones and incurring storage/read/compaction costs;
- physical remnants after logical deletion;
- secure-erasure failure, which is outside this case.

---

## Engineering reconstruction

### E — logical deletion ≠ immediate physical removal

Cassandra's own documentation makes the distinction literal: DELETE creates a tombstone instead of removing the underlying value immediately.

### E — negative-state retention ≠ payload retention

The tombstone is not the payload being preserved. It is retained evidence that an older payload must no longer count.

### E — tombstone presence ≠ replica convergence

A local tombstone can coexist with a stale positive replica. The system still requires mutation delivery or repair to make the deletion relation sufficiently distributed.

### E — grace expiry ≠ actual reclamation

Age creates eligibility, not physical completion. Compaction and overlap conditions still govern actual removal.

### E — retention window ≠ repair guarantee

`gc_grace_seconds` describes a time envelope in which deletion evidence is retained; it does not itself perform repair. Likewise hints are best-effort assistance, not proof that every replica received the deletion.

### E — forgetting control state can resurrect payload

This case provides a particularly sharp forgetting failure:

> the system can correctly stop treating old payload as current, then later forget the negative evidence that enforced that state, and thereby allow the old payload to become current again during repair.

The lost thing is not initially the user payload; it is the relation that says the payload has been superseded by deletion.

### E — repair can preserve forgetting or defeat it

When tombstone evidence survives, repair propagates deletion. When only the stale positive value survives as admissible evidence, repair can propagate that value instead. `repair` therefore is not intrinsically a preservation-of-newest-state operation independent of the state available to it.

### E — repair-qualified forgetting trades safety against retained-state cost

`only_purge_repaired_tombstones` can postpone forgetting until repair evidence exists. Apache's own release note simultaneously warns that long-running lack of repair can retain tombstones indefinitely enough to cause other problems. Safer negative-state retention consumes storage and maintenance resources.

---

## Functional analogies

### A — Cassandra tombstones and Swift tombstones

Case 28 and Case 41 both show deletion requiring retained negative state across asynchronous replicas.

The analogy stops at the relation level:

- Swift 2.10.1 uses timestamped `.ts` files, `reclaim_age`, replication/reconstruction, and its own consistency-window language;
- Cassandra uses tombstones inside its LSM/SSTable model, `gc_grace_seconds`, compaction overlap, hints, repair, and optional repaired-state gating;
- neither case proves historical derivation from the other.

### A — Cassandra repair and Dynamo anti-entropy

Case 23 and Cassandra both distinguish temporary mutation-delivery help from later convergence work. But Dynamo's vector-clock divergent-version model and Cassandra's tombstone/last-write-style deletion relation are not the same currentness mechanism.

### A — tombstone reclamation and Flash invalidation

Both can leave old physical embodiments after a logical state has changed. Cassandra's stale replicas and distributed repair are not Flash erase units or FTL garbage collection. This is a functional comparison only.

---

## Philosophical / media-theoretical interpretation

The exact technical pressure is stronger than the generic statement that deletion may leave traces:

> **A system may have to remember that something was deleted, because forgetting the deletion can make the deleted thing return.**

The case therefore separates three forms of forgetting:

1. the payload is made noncurrent;
2. replicas converge on that negative state;
3. the evidence of deletion is itself reclaimed.

These are not one event.

This can discipline philosophical discussion of forgetting, trace, and technical memory, but no direct equivalence to human forgetting, archival erasure, or Stiegler's tertiary retention follows automatically. The tombstone is operational distributed-control state unless a separate argument establishes a broader cultural or mnemonic role.

---

## Counterexamples and limits

- The case is release-family bounded; later Cassandra versions add/change repair and tombstone tooling.
- `gc_grace_seconds` is not proof of global convergence.
- Hints are explicitly best effort.
- Tombstone age does not imply immediate physical deletion.
- `only_purge_repaired_tombstones` strengthens one reclamation condition but does not prove absence of every possible stale/corrupt copy.
- The case does not establish secure erasure.
- The case does not claim Cassandra invented tombstones or anti-entropy repair.
- The case does not generalize one Cassandra setting into a universal distributed-store deletion rule.

---

## Related repositories

A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for Cassandra tombstone / `gc_grace_seconds` / zombie-deletion material found no dedicated overlapping case during this research slice. This case therefore remains here as retention-specific distributed-currentness analysis rather than duplicating an existing technical history.

`problem-history` remains the methodological guard: project terms such as `negative-state retention` and `safe-forgetting condition` are modern reconstructions, not claims about Cassandra developers' historical vocabulary.

---

## Sources

### Primary / project sources

1. Apache Cassandra 3.11 documentation, **Compaction — Tombstones and Garbage Collection (GC) Grace**: <https://cassandra.apache.org/doc/3.11/cassandra/operating/compaction/index.html>
2. Apache Cassandra 3.11 documentation, **Hints**: <https://cassandra.apache.org/doc/3.11/cassandra/operating/hints.html>
3. Apache Cassandra repository, `cassandra-3.11`, **NEWS.txt**: <https://github.com/apache/cassandra/blob/cassandra-3.11/NEWS.txt>
4. Apache Cassandra repository, `cassandra-3.11`, `AbstractCompactionStrategy.java`: <https://github.com/apache/cassandra/blob/cassandra-3.11/src/java/org/apache/cassandra/db/compaction/AbstractCompactionStrategy.java>
5. Apache Cassandra repository, `cassandra-3.11`, `RepairedDataTombstonesTest.java`: <https://github.com/apache/cassandra/blob/cassandra-3.11/test/unit/org/apache/cassandra/db/RepairedDataTombstonesTest.java>

### Later terminology / continuity check

6. Apache Cassandra current documentation, **Tombstones**: <https://cassandra.apache.org/doc/latest/cassandra/managing/operating/compaction/tombstones.html>

---

## Status

**`grounded`**

The central mechanism is supported by Apache's release-family documentation, source, tests, and release notes. Remaining work is later-version semantic archaeology or broader genealogy, not a blocker for this bounded case.
