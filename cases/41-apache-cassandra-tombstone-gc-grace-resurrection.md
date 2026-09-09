# Apache Cassandra GC Grace: Tombstone Retention, Repair Windows, and Data Resurrection

## Scope

- **Bounded system:** Apache Cassandra 3.x operational semantics remain the principal behavior layer, with bounded historical floors from Apache Incubator Cassandra in 2009 and Cassandra 1.2.19 in 2014, plus a narrowly bounded Cassandra 4.1.0–4.1.6 Paxos-v2 defect/fix deepening; the older and later artifacts are used only where they directly change deletion-evidence retention, reclamation, or resurrection boundaries.
- **Bounded mechanism:** deletion tombstones, `gc_grace_seconds`, compaction-time tombstone purging, repair, hinted handoff, and the `only_purge_repaired_tombstones` safety option.
- **Primary source base:** Apache Cassandra 3.11 official documentation; Apache Cassandra source/tests and release records; exact Apache git history for the 17 April 2009 GC-grace configurability change and the 11 August 2015 repaired-tombstone purge option; plus bounded 1.2.19 implementation evidence.
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


## Historical deepening — Apache Incubator Cassandra 2009 grace-policy floor

This earlier slice sharpens the chronology of a mechanism already present in the canonical case. It does **not** identify the invention date of Cassandra tombstones or grace-period reclamation.

### H/P — by 17 April 2009, GC grace was an explicit configurable propagation/failure budget

Apache Incubator Cassandra commit [`fa1f80f40da0bb629c40bf09791c6c90f2608774`](https://github.com/apache/cassandra/commit/fa1f80f40da0bb629c40bf09791c6c90f2608774), committed on **17 April 2009**, changed a fixed `GC_GRACE_IN_SECONDS` into a configuration value. The added `storage-conf.xml` comment says the interval is the time to wait before garbage-collecting deletion markers and instructs operators to choose a value large enough that they are confident the deletion marker will have propagated to all replicas by then, even in the face of hardware failures. The shipped example/default is `864000` seconds, ten days.

That wording is direct historical implementation evidence for the intended operational relation:

```text
retained deletion marker
    + chosen failure/propagation interval
    -> later eligibility for garbage collection
```

It is **not** evidence that the timer itself performs propagation or proves convergence.

### H/P — the 2009 configurability commit is not the origin of GC grace

The same diff removes an already-existing fixed constant:

```text
GC_GRACE_IN_SECONDS = 10 * 24 * 3600
```

and its unchanged context already says deleted columns, supercolumns, and column families must be preserved until they have been deleted for at least that grace interval. Therefore the inspected trunk already had a ten-day preservation rule before this customization commit.

The safe historical claim is only:

> **17 April 2009 is a public implementation floor for configurable Cassandra GC grace and its explicit propagation/hardware-failure rationale; the grace mechanism itself is older than that change.**

This blocks the novelty error `configuration introduction date = mechanism invention date`.

### E — `gc_grace` is a coordination budget, not a convergence certificate

The source comment delegates a judgment to the operator: choose enough time to be confident the deletion marker will propagate through expected failures. That makes the interval a **retention policy budget** around a distributed maintenance process, not evidence that the maintenance process has actually completed.

Project reconstruction:

```text
elapsed grace
    != proof all replicas received the delete

configured failure envelope
    != observed repair completion
```

The distinction explains why a ten-day default cannot be universalized into a timeless safe-forgetting theorem. Outage duration, repair practice, topology, operational failures, and later implementation controls can all change whether the retained negative evidence has actually completed its job.

### H/P — 2015 adds an optional repair-qualified retirement rule

Apache Cassandra commit [`6f0c12f3a4668a5dcae162969843f02498ee7e6d`](https://github.com/apache/cassandra/commit/6f0c12f3a4668a5dcae162969843f02498ee7e6d), committed on **11 August 2015** for **CASSANDRA-6434**, adds `only_purge_repaired_tombstones`. Its release-note text explicitly says the option exists to avoid resurrection if repair has not run within `gc_grace_seconds`, while warning that long periods without repair can retain tombstones and create other problems.

This is a later strengthening of the reclamation predicate:

```text
age-qualified tombstone
    + optional repaired-state qualification
    -> narrower purge authority
```

It must not be projected backward into the 2009 implementation or Cassandra 1.2.19. Conversely, the later option makes visible a distinction that the project should keep explicit: **age eligibility and repair evidence are different kinds of state**.

### E/A — relation to Case 48 without mechanism collapse

Case 48 tracks Cassandra incremental-repair state as its own retained control relation. Case 41 consumes repaired/unrepaired status only insofar as the 2015 option can use it to qualify tombstone reclamation. Thus:

```text
tombstone age
    != repairedness state
    != proof of cluster-wide convergence
```

This is a bounded cross-case engineering relation, not a claim that all repair metadata and tombstone metadata are one mechanism.

---

## Historical deepening — Cassandra 1.2.19, local purge ordering, and pre-Cassandra prior art

The canonical case is centered on Cassandra 3.x because that release family exposes the later repair-aware purge option especially clearly. A separate later-added duplicate case repeated most of the same tombstone / grace / resurrection mechanism while adding useful older evidence. That older evidence is retained here rather than maintained as a duplicate case.

### H/P — Cassandra 1.2.19 makes the deletion marker an explicit retained object

The `cassandra-1.2.19` source contains `DeletedColumn`, a `Column` subclass whose deletion state is represented explicitly: `isMarkedForDelete()` returns true, `getMarkedForDeleteAt()` returns the column timestamp, `getLocalDeletionTime()` retains the local deletion time, and serialization uses the deletion mask.

**Primary anchor:** Apache Cassandra `DeletedColumn.java`, tag `cassandra-1.2.19`: <https://github.com/apache/cassandra/blob/cassandra-1.2.19/src/java/org/apache/cassandra/db/DeletedColumn.java>.

This is direct implementation evidence for a narrow point already used by the case: deletion is not represented merely by absence; negative/currentness state has an embodiment of its own.

### H/P — the 1.2.19 grace interval is policy state, while overlap still constrains local purge

`CFMetaData.java` in the same tag defines `DEFAULT_GC_GRACE_SECONDS = 864000` for ordinary user tables. More importantly, `CompactionController.shouldPurge(key, maxDeletionTimestamp)` is documented around the condition that all versions of the row be present in the compaction set; it checks overlapping SSTables and refuses purge when an overlapping SSTable can still contain a version at or before the deletion timestamp.

**Primary anchors:**

- <https://github.com/apache/cassandra/blob/cassandra-1.2.19/src/java/org/apache/cassandra/config/CFMetaData.java>
- <https://github.com/apache/cassandra/blob/cassandra-1.2.19/src/java/org/apache/cassandra/db/compaction/CompactionController.java>

The historical/engineering boundary is therefore sharper than `ten days makes deletion safe`:

```text
grace age
    -> purge eligibility input

but

overlapping older representations
    -> can still block local purge
```

`safe-forgetting closure` remains a project reconstruction, not Cassandra vocabulary.

### H/P — CASSANDRA-7810 is a one-node counterexample to “this is only a stale-replica problem”

ASF issue **CASSANDRA-7810**, resolved in August 2014 with fix versions including 1.2.19, 2.0.11, and 2.1.0, reproduces resurrection in a single-node cluster with `gc_grace_seconds = 0`: insert, delete, flush, compact, and the deleted row reappears. The issue diagnosis is that expired tombstones were discarded before their suppressive effect had been correctly applied during compaction. Cassandra 1.2.19 `CHANGES.txt` records `Track expired tombstones (CASSANDRA-7810)`.

**Primary/institutional anchors:**

- <https://issues.apache.org/jira/browse/CASSANDRA-7810>
- <https://github.com/apache/cassandra/blob/cassandra-1.2.19/CHANGES.txt>

This adds a distinct failure boundary to the distributed zombie example: even with no remote stale replica, **retiring negative evidence in the wrong local operation order can restore older positive state**.

### H/P prior art — deletion entries that must survive non-major compaction predate Cassandra

Chang et al.'s **Bigtable** paper (OSDI 2006), §5.4, states that SSTables produced by non-major compactions can contain `special deletion entries` that suppress deleted data in older live SSTables; a major compaction can later produce an SSTable containing neither deletion information nor deleted data.

**Primary anchor:** Fay Chang et al., “Bigtable: A Distributed Storage System for Structured Data,” OSDI 2006, §5.4, HTML proceedings: <https://static.usenix.org/event/osdi06/tech/chang/chang_html/>.

This is earlier primary prior art for the **function** `retain deletion evidence while older immutable representations remain live, then retire both when compaction closes the relation`. It does **not** establish implementation identity, direct Bigtable → Cassandra code descent, or invention priority for the wider tombstone concept.

### Version boundary preserved

Do not project the later Cassandra 3.x `only_purge_repaired_tombstones` option backward into 1.2.19. Conversely, do not use the older `DeletedColumn` embodiment as if it were the exact encoding of every later tombstone type. The canonical case now intentionally uses two bounded historical layers:

- 1.2.19 / 2014 for explicit deletion-marker embodiment, overlap-aware purge, and the CASSANDRA-7810 local sequencing failure;
- 3.x / 3.11 for the later documented hints/repair/grace model and repair-qualified purge option.

---

## Historical deepening — Cassandra 4.1.0–4.1.6 Paxos v2 stale-commit redistribution

This later slice is grounded separately in [`evidence/41-cassandra-2024-paxos-v2-stale-commit-resurrection-deepening.md`](../evidence/41-cassandra-2024-paxos-v2-stale-commit-resurrection-deepening.md). It does **not** replace the 1.2/3.x mechanism above. It adds one post-4.0 counterexample to an overly narrow safe-forgetting model.

### H/P — Cassandra 4.1 adds Paxos v2, Paxos Repair, and non-legacy Paxos-state purge modes

The Cassandra 4.1 release `NEWS.txt` introduces Paxos v2 and a Paxos Repair mechanism. After regular repairs include Paxos repair, the release record encourages operators to move to `paxos_state_purging: repaired`. Tagged 4.1.6 source defines `legacy`, `gc_grace`, and `repaired` purging modes and documents `legacy` as the default.

These are separate from the ordinary table tombstone / `gc_grace_seconds` mechanism already established by the case, even though the later modes deliberately relate Paxos-state retirement to GC grace or repair evidence.

### H/P — CASSANDRA-19617 shows a stale Paxos commit can reapply an insert after tombstone collection

Apache issue CASSANDRA-19617, created **3 May 2024** and resolved **11 June 2024**, is recorded as a critical correctness bug since Cassandra 4.1.0 and fixed beginning with 4.1.6. The issue explicitly limits the defect to `paxos_state_purging: gc_grace` and `repaired`.

Apache identifies two failures: old Paxos state could be purged on compaction but not filtered on load, and `PaxosPrepare` did not filter commits against the Paxos repair low bound. Under the described compaction pattern, some replicas could discard newer Paxos commits while an older commit survived elsewhere. A coordinator could then redistribute that old commit, allowing an **insert to be reapplied after GC grace elapsed and the user-data tombstone had been collected**.

**Primary anchor:** <https://issues.apache.org/jira/browse/CASSANDRA-19617>

### H/P — the 4.1.6 fix makes stale-state admissibility explicit at load and prepare time

Apache commit [`53b06453b7dea147ef6369765e0b7ac7fb0990fd`](https://github.com/apache/cassandra/commit/53b06453b7dea147ef6369765e0b7ac7fb0990fd), `Refresh stale paxos commit`, filters loaded promises/accepted/committed Paxos state using the applicable purge boundary and makes `PaxosPrepare` discard committed state below the maximum repair low bound returned by participants. Its distributed regression test constructs stale `system.paxos` state and requires the deleted row to remain absent after the later Paxos operation.

This fix is not tombstone restoration. It changes which surviving Paxos state is allowed to count.

### E — safe forgetting must close auxiliary re-authorization paths

The earlier case already established:

```text
stale positive replica
    + lost deletion evidence
    -> possible resurrection
```

The 2024 defect adds:

```text
stale positive Paxos commit
    + asymmetric retirement of newer Paxos state
    + later tombstone collection
    + obsolete commit wrongly treated as admissible
    -> possible reapplication of old insert
```

Therefore `replicas repaired enough for ordinary tombstone retirement` and `every auxiliary mechanism can no longer re-authorize older positive state` are not the same proposition.

This is a bounded engineering reconstruction from one Apache defect class, not a universal theorem about Paxos or distributed deletion.

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

### 7. Paxos coordination state and repair lower bound in the bounded 4.1 deepening

For Paxos-v2/LWT operations, `system.paxos` can retain older accepted/committed coordination state separately from the user-table tombstone. CASSANDRA-19617 shows that this auxiliary positive state also needs an admissibility boundary: a physically surviving old commit below the applicable GC-grace/repair floor must not regain redistribution authority.

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
- in the bounded Cassandra 4.1 Paxos-v2 defect, stale auxiliary Paxos commit state surviving newer coordination state and later being treated as redistributable after the user-data tombstone is collected;
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


### E — auxiliary positive state can defeat otherwise-completed negative-state retirement

CASSANDRA-19617 narrows the earlier phrase `safe-forgetting condition`. Tombstone age, local overlap closure, and ordinary repair evidence can be insufficient if a separate retained coordination substrate can still re-authorize a superseded positive mutation.

So, in the bounded 4.1 Paxos-v2 configuration:

```text
user-data tombstone reclaimed
    != proof every older positive state is non-authoritative
```

The fix does not preserve the tombstone longer. It filters old Paxos state so physical survival does not automatically become protocol authority.

### E — purge-on-compaction != purge-on-observation

A retained record can be physically eligible for cleanup yet still reappear between compaction events unless read/load/prepare paths apply the same semantic boundary. CASSANDRA-19617 is therefore also a currentness-check placement failure: applying retirement only during one maintenance path did not guarantee that every later observer would treat the old state as retired.

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
- CASSANDRA-19617 is bounded to Cassandra 4.1 Paxos-v2 `paxos_state_purging: gc_grace` / `repaired`; the issue explicitly says the legacy/default TTL purging mode is not affected by this defect.
- The 4.1.6 fix is an old-Paxos-state admissibility correction, not proof that all later Paxos/tombstone interactions are closed.
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


### Cassandra 4.1 Paxos-v2 stale-commit deepening

6. Apache Cassandra 4.1.6 `NEWS.txt`, Paxos v2 / Paxos Repair release record: <https://github.com/apache/cassandra/blob/cassandra-4.1.6/NEWS.txt>
7. Apache Cassandra 4.1.6 `Config.java`, `PaxosStatePurging` modes/default: <https://github.com/apache/cassandra/blob/cassandra-4.1.6/src/java/org/apache/cassandra/config/Config.java>
8. Apache JIRA CASSANDRA-19617, **Paxos may re-distribute stale commits that predate a collectable tombstone**: <https://issues.apache.org/jira/browse/CASSANDRA-19617>
9. Apache Cassandra commit `53b06453b7dea147ef6369765e0b7ac7fb0990fd`, **Refresh stale paxos commit**: <https://github.com/apache/cassandra/commit/53b06453b7dea147ef6369765e0b7ac7fb0990fd>
10. Regression test `CasWriteTest.testStaleCommitInSystemPaxos` at the fix commit: <https://github.com/apache/cassandra/blob/53b06453b7dea147ef6369765e0b7ac7fb0990fd/test/distributed/org/apache/cassandra/distributed/test/CasWriteTest.java>

### Later terminology / continuity check

11. Apache Cassandra current documentation, **Tombstones**: <https://cassandra.apache.org/doc/latest/cassandra/managing/operating/compaction/tombstones.html>

---

## Status

**`grounded`**

The central mechanism is supported by Apache's release-family documentation, source, tests, and release notes. The 4.1.0–4.1.6 Paxos-v2 deepening additionally grounds one auxiliary-state resurrection path after tombstone collection. Remaining work includes post-4.1.6 Paxos/tombstone semantics, broader range/TTL-tombstone evolution, independent fault injection, and genealogy; none blocks the bounded case.
