# Apache Cassandra Incremental Repair State: `repairedAt`, Anti-Compaction, and Pending-Repair Handoff

## Scope

- **Bounded system:** Apache Cassandra incremental anti-entropy repair from the feature rationale recorded in CASSANDRA-5351 (fixed for 2.1 beta1), through the legacy repaired/unrepaired implementation visible on the `cassandra-3.11` branch, with the 4.0 pending-repair redesign from CASSANDRA-9143 used as a later correction/qualification.
- **Bounded mechanism:** remembered repair eligibility, `repairedAt` SSTable metadata, repaired/unrepaired SSTable segregation, anti-compaction, operator-triggered incremental/full repair, and the later `pendingRepair` intermediate state used to keep an in-progress incremental repair from being mistaken for completed repair.
- **Primary source base:** Apache Cassandra issue tracker, versioned 3.11 documentation, `cassandra-3.11` source, and `cassandra-4.0` repair source.
- **Research question:** what happens when the history of maintenance itself becomes retained control state that determines whether data will be checked again in the future?

This is **not** a general history of Cassandra, Merkle trees, Dynamo-style anti-entropy, LSM trees, or distributed consistency. Case 41 already covers Cassandra tombstone retention, `gc_grace_seconds`, and resurrection. This case isolates a different relation: **repair-history state as a future-maintenance selector**.

The bounded retention claim is:

> **Incremental repair saves work by remembering which SSTable data has already been successfully repaired and excluding that class from later incremental passes. That remembered classification is therefore not merely an operator log: it changes future maintenance eligibility, shapes compaction topology, and can itself become a consistency problem. Cassandra 4.0's pending-repair design makes the intermediate status of repair explicit so that data is not promoted to repaired until the repair session reaches a coordinated completion state.**

`maintenance-history state`, `future-maintenance eligibility`, `maintenance-state currentness`, and `repair-state handoff` below are project terms. Apache historical vocabulary includes `incremental repair`, `full repair`, `repaired`, `unrepaired`, `repairedAt`, `anticompaction`, `pending repair`, and the named repair-session states in later source.

---

## Historical vocabulary

### Direct Apache vocabulary

The bounded sources use:

- `repair`;
- `anti-entropy repair`;
- `incremental repair`;
- `full repair`;
- `Merkle tree`;
- `repaired` / `unrepaired` data and SSTables;
- `repairedAt`;
- `anticompaction` / `anti-compaction`;
- `pending repair` / `pendingRepair` in the 4.0 redesign;
- `repair session`;
- `PREPARING`, `FINALIZED`, and `FAILED` session states in the later consistent-repair implementation.

### Project reconstruction vocabulary

The following terms are analytical conveniences, not claims about Apache developers' historical wording:

- **maintenance-history state** — retained metadata whose meaning includes whether a previous maintenance operation has successfully covered some data;
- **future-maintenance eligibility** — whether a future incremental repair considers a retained embodiment part of its repair input set;
- **maintenance-state currentness** — whether the repair classification still truthfully represents the maintenance relation it is meant to encode;
- **repair-state handoff** — the transition from unrepaired, through an in-progress isolated state, to repaired or back to unrepaired.

---

## Historical record

### H/P — incremental repair was explicitly proposed as remembered successful repair

CASSANDRA-5351, **“Avoid repairing already-repaired data by default,”** records the feature rationale that became a Cassandra 2.1 repair mechanism. The issue says repair had historically built its Merkle tree from all data in a column family and describes that as correct but inefficient. The proposed optimization is explicit:

- remember which SSTables have already been successfully repaired;
- repair only SSTables new since the previous repair;
- teach compaction not to mix repaired and unrepaired data again.

The issue is marked fixed for **2.1 beta1**.

This is unusually strong historical evidence because the actors themselves formulate the control-state dependency: remembering past successful maintenance is introduced precisely so future maintenance can omit that state.

**Primary anchor:** Apache JIRA CASSANDRA-5351.

### H/P — Cassandra 3.11 documentation makes repaired marking change future repair scope

The versioned 3.11 repair documentation distinguishes:

- **full repair:** operates over all data in the token range being repaired;
- **incremental repair:** repairs only data written since the previous incremental repair.

The documentation then states that once incremental repair **marks data as repaired, it will not try to repair it again**. Apache also gives the reason this is only a bounded optimization: skipping repaired data is suitable for missed-write synchronization but does not protect against later disk corruption, operator-caused loss, or Cassandra bugs. The documentation therefore recommends occasional full repair.

The same page says repair in 3.11 is not automatically scheduled by Cassandra because it can create substantial disk and network I/O; it is invoked by an operator through `nodetool`.

**Primary anchor:** Apache Cassandra 3.11, `Operating > Repair`, especially `Incremental and Full Repairs` and `Usage and Best Practices`.

### H/P — `repairedAt` is literal retained SSTable metadata in the 3.11 source

`StatsMetadata.java` on the `cassandra-3.11` branch declares `public final long repairedAt` as part of the SSTable metadata component.

This matters because “repaired” is not merely reconstructed from an external operator diary at the next run. It is represented in the storage engine's retained metadata and can be reloaded with the SSTable.

**Primary anchor:** `src/java/org/apache/cassandra/io/sstable/metadata/StatsMetadata.java`, branch `cassandra-3.11`.

### H/P — anti-compaction materializes repaired and unrepaired classes

The 3.11 compaction documentation states that with incremental repair Cassandra must keep track of repaired and unrepaired data. It says anti-compaction splits repaired data into **repaired and unrepaired SSTables**, and separate compaction-strategy instances are maintained for the two sets to avoid mixing them again.

The 3.11 source makes the mechanism concrete. `CompactionManager.doAntiCompaction()` documents that repaired ranges are tracked through `StatsMetadata.repairedAt`. Its anti-compaction writer creates one output with the repair timestamp and another with `UNREPAIRED_SSTABLE`; the original SSTable is then obsoleted after the split is prepared.

`CompactionStrategyManager.java` is even more explicit in its class comment: it maintains two actual compaction-strategy instances per data directory, one for repaired data and one for unrepaired data, “to be able to totally separate the different sets of sstables.”

**Primary anchors:** Apache Cassandra 3.11 compaction documentation; `CompactionManager.java`; `CompactionStrategyManager.java`, branch `cassandra-3.11`.

### H/P — an entirely covered SSTable can be reclassified without physical splitting

The 3.11 `performAnticompaction()` path distinguishes the logical repair classification from the physical split operation. If an SSTable is fully contained in the repaired ranges, the code logs that it is **mutating `repairedAt` instead of anticompacting**, reloads the metadata, and notifies the tracker that repair status changed.

So:

```text
repair-state transition
    != necessarily physical SSTable split
```

Anti-compaction is needed where repaired and unrepaired ranges share one SSTable; a fully covered SSTable can cross the repair-state boundary by metadata mutation alone.

**Primary anchor:** `CompactionManager.performAnticompaction()`, `cassandra-3.11`.

### H/P — repaired/unrepaired segregation also changes compaction behavior

The 3.11 compaction documentation warns that once repaired and unrepaired data are separated, the separation affects more than repair input selection. If incremental repair is run once and then abandoned, very old repaired SSTables can block compaction from dropping tombstones in newer unrepaired SSTables.

This gives the remembered maintenance state a second operational consequence:

- it filters future incremental repair;
- it partitions future compaction work.

Case 41 already analyzes tombstone correctness and reclamation. Here the point is narrower: **maintenance-history classification changes the topology within which later reclamation is allowed to operate.**

**Primary anchor:** Apache Cassandra 3.11, `Compaction > Repaired/unrepaired data`.

### H/P — “repaired once” is not a statement of present integrity

Apache 3.11 explicitly says incremental repair will not revisit marked-repaired data, while full repair operates over all data and should still run occasionally because later disk corruption, operator error, or Cassandra bugs are outside what remembered incremental coverage protects against.

This is a direct counterexample to reading `repaired` as a timeless health claim. In this bounded mechanism it is principally maintenance-history/eligibility state.

The same page provides `--validate` to compare repaired data using Merkle trees without streaming and says that if repaired data is found out of sync, a full repair should be run.

**Primary anchor:** Apache Cassandra 3.11 repair documentation.

### H/P — the legacy repair-history state itself could become inconsistent across replicas

CASSANDRA-9143, **“Fix consistency of incrementally repaired data across replicas,”** documents the defect pressure that led to the Cassandra 4.0 redesign. The issue explains that the legacy mechanism sent anti-compaction requests to replicas and marked appropriate SSTables repaired, but failures could leave replica nodes with inconsistent `repairedAt` classification. The discussion also identifies normal compaction during a repair as another way data could be classified inconsistently, creating unnecessary future streaming and unpredictable incremental-repair behavior.

The important evidence boundary is:

> the Jira establishes a problem in **the consistency of the repair classification itself**.

This case does not infer from that statement that every such divergence necessarily produces payload corruption or data loss. It establishes that a control relation used to optimize future repair could itself become distributed and inconsistent.

**Primary anchor:** Apache JIRA CASSANDRA-9143.

### H/P — Cassandra 4.0 adds a pending-repair state before promotion to repaired

CASSANDRA-9143 describes the redesigned incremental-repair sequence that was ultimately fixed for Cassandra 4.0:

1. persist the session locally on each participant;
2. anti-compact overlapping unrepaired SSTables into a **pending repair bucket**;
3. validate/synchronize that isolated data;
4. use a coordinated finalization step to promote pending data to repaired;
5. if validation/synchronization/finalization fails, move the state back to unrepaired rather than treating the attempt as completed repair.

The `cassandra-4.0` source gives the corresponding implementation boundary. `PendingAntiCompaction` describes its role as isolating unrepaired SSTables for a token range into a pending-repair group so they cannot be compacted with other SSTables while being repaired. Its acquisition predicate:

- excludes already repaired SSTables;
- rejects legacy SSTables that do not support pending repair;
- excludes SSTables already pending another non-finalized repair session.

`LocalSessions.java` persists local repair-session state, including `repaired_at`, session `state`, coordinator, participants, ranges, and table IDs. Its state-transition path saves the state and treats completed session transitions separately; prepare handling says data is isolated before a success response is sent to the coordinator.

**Primary anchors:** CASSANDRA-9143; `PendingAntiCompaction.java`; `LocalSessions.java`, branch `cassandra-4.0`.

---

## Retained state

The bounded case contains several different state classes.

### 1. User payload and ordinary Cassandra version/timestamp state

This remains the data whose replica divergence repair is intended to reconcile.

### 2. SSTable repair classification

In 3.11, `repairedAt` distinguishes repaired from unrepaired SSTable state for incremental-repair and compaction purposes.

### 3. Physical repaired/unrepaired SSTable embodiments

Anti-compaction can rewrite one mixed physical SSTable into separate repaired and unrepaired outputs.

### 4. Compaction-strategy membership

The repair classification participates in selecting which compaction strategy instance owns an SSTable, keeping the sets separated.

### 5. Repair-session state in the later design

Cassandra 4.0 adds a distinct `pendingRepair`/session relation so “selected for this in-progress repair” is not collapsed into “already repaired.”

### 6. Operator/scheduler state

In 3.11, recurring repair remains an operational obligation outside the automatic core maintenance loop: someone or some external system must invoke it often enough for the cluster's failure/tombstone assumptions.

The case therefore distinguishes **payload state**, **currentness/version state**, **maintenance-history state**, **in-progress maintenance state**, and **operational scheduling state**.

---

## Physical / logical substrate

The relevant substrate is layered:

```text
replicated Cassandra partitions
    -> immutable SSTable files
    -> SSTable metadata including repairedAt
    -> repaired/unrepaired compaction buckets
    -> later pendingRepair/session state
    -> operator-issued repair schedule
```

The key retained distinction is not a new physical bit-cell mechanism. It is a storage-engine/protocol classification that survives long enough to alter future maintenance behavior.

---

## Retention mechanism

### Legacy 3.11-style bounded sequence

```text
new writes -> unrepaired SSTables
        |
        v
operator starts incremental repair
        |
        v
Merkle-tree validation / streaming of differences
        |
        v
anti-compaction or repairedAt mutation
        |
        +---- repaired range -> repaired SSTable/class
        |
        +---- remainder ------> unrepaired SSTable/class
        |
        v
future incremental repair excludes repaired class
```

The system saves future work by preserving a result of past maintenance.

### Later 4.0 correction boundary

```text
unrepaired
   |
   v
prepare + isolate
   |
   v
pending repair
   |
   +---- session succeeds/finalizes -> repaired
   |
   +---- session fails -------------> unrepaired
```

The later state machine makes a previously fragile transition explicit: **being processed by a repair is not yet equivalent to having successfully completed repair.**

---

## Addressing and access geometry

The user-facing object remains addressed through Cassandra's normal partition/table model. Repair does not create a second application namespace for “repaired data.”

Internally, however, maintenance accesses a filtered population:

- token ranges define the repair domain;
- SSTable membership and repair metadata qualify which physical files/ranges participate;
- incremental repair excludes already repaired state;
- full repair intentionally widens the domain back to all data in the chosen token range;
- the later pending-repair design isolates a repair session's population before synchronization.

So maintenance has an **access geometry of its own**. The same user data can be addressable to the application while excluded from one maintenance pass because of retained repair-history state.

---

## Read semantics

Ordinary application reads are not defined by `repairedAt` in the way incremental-repair selection is. A repaired SSTable is not a special historical version returned to clients.

This is important because it blocks a misleading analogy:

```text
repairedAt
    != application version timestamp
    != proof that this read is correct forever
```

The 3.11 `--validate` option further shows that repaired data can later be rechecked for cross-node equality even while it remains classified as repaired.

---

## Write and erasure semantics

`repairedAt` is not an application write or delete. The repair pipeline can change maintenance metadata and physical SSTable organization without changing the logical user value.

Anti-compaction may:

- rewrite an SSTable into repaired and unrepaired outputs;
- mark one output with a repair timestamp;
- leave the other `UNREPAIRED_SSTABLE`;
- obsolete the original mixed SSTable.

If the whole SSTable lies inside the repaired range, 3.11 can instead mutate repair metadata without performing the split.

Physical rewriting, logical payload change, and maintenance-state change are therefore separate axes.

---

## Time

Relevant timescales include:

- the interval between incremental repairs;
- the interval between occasional full repairs;
- duration of one repair session;
- anti-compaction duration and compaction backlog;
- the lifetime of a `repairedAt` classification;
- time between a later corruption/loss event and the next full validation/repair;
- `gc_grace_seconds`, which Case 41 shows is a separate deletion-evidence deadline;
- in later designs, the lifetime of a pending repair session before finalization/failure cleanup.

This case therefore adds another form of technical time:

> **past maintenance can leave a retained classification whose future validity depends on what happens after the maintenance event.**

---

## Maintenance and labor

### 3.11 operator responsibility

Apache explicitly says repair is not automatically run because it can produce substantial disk/network I/O. The operator invokes `nodetool repair`, chooses incremental/full mode, scopes ranges/keyspaces/tables, and establishes a cadence.

Incremental repair reduces repeated work but introduces:

- repair-state bookkeeping;
- anti-compaction I/O;
- separate repaired/unrepaired compaction populations;
- the need to remember that full repair remains necessary for failure classes incremental skipping does not revisit.

### 4.0 internalization of session coordination

The pending-repair redesign moves more correctness work into the database protocol:

- persist local session state;
- isolate the repair population;
- prevent conflicting reuse/compaction;
- coordinate promotion/failure.

That does not mean repair becomes maintenance-free or operator-free. It changes which part of the repair-state transition is internally enforced.

---

## Failure / forgetting modes

Keep these distinct:

- missed writes between replicas;
- repair not being scheduled often enough;
- a repaired SSTable later suffering disk corruption;
- operator-caused loss after a prior successful repair;
- software defect after prior successful repair;
- a repair session failing before all participants agree on completed repair state;
- repaired/unrepaired classification diverging across replicas;
- repaired and unrepaired data being mixed by compaction;
- an in-progress repair being mistaken for completed repair;
- stale pending-repair session state blocking later maintenance;
- one-off incremental repair creating long-lived compaction separation that impedes tombstone reclamation;
- loss/corruption of the repair metadata itself.

These are not one generic “repair failed” condition.

---

## Engineering reconstruction

### E — past repair completion can become future-maintenance eligibility state

The point of incremental repair is not only that repair happened. Its result is retained so a future incremental repair can omit data already classified as repaired.

### E — maintenance-history metadata ≠ payload, while it can be constitutive of future maintenance

`repairedAt` does not contain the user's value, but it changes whether the storage engine will revisit the SSTable in a later incremental repair.

### E — repaired status ≠ present integrity or replica equality forever

Apache's own documentation requires this distinction: later corruption, operator loss, or bugs can invalidate present state while `repaired` remains a record of previous maintenance coverage. Full repair and `--validate` exist precisely because past repair is not a perpetual health certificate.

### E — repair completion ≠ disposal of repair history

A successful incremental repair produces retained classification state. Maintenance is not merely an event that vanishes after completion; its result changes later system behavior.

### E — anti-compaction ≠ ordinary compaction

The bounded anti-compaction operation is specifically tied to repaired-range separation and repair metadata. Similar physical rewriting does not make it the same operation as routine size/level/time-window compaction.

### E — maintenance-state transition ≠ necessarily payload rewrite

A fully covered SSTable can change `repairedAt` without being physically split. Conversely, a partially covered SSTable can be rewritten into two embodiments while preserving the user-level data relation.

### E — maintenance-state consistency can become a distributed correctness problem of its own

CASSANDRA-9143 shows that participants could disagree about which data had been marked repaired. Once that classification determines future maintenance eligibility, consistency of maintenance metadata is no longer merely cosmetic.

This does **not** mean `repairedAt` becomes application consensus state. It means the repair subsystem has a distributed control-state consistency obligation.

### E — pending repair ≠ repaired

The 4.0 design creates an intermediate state for data isolated for an in-progress repair. This blocks the shortcut:

```text
repair started
    -> data already counts as repaired
```

A session must complete the later state transition.

### E — failed maintenance attempt ≠ safe successful-maintenance evidence

The CASSANDRA-9143 design returns failed pending data to unrepaired status rather than preserving a false successful-repair classification.

### E — repair optimization can create a verification blind spot

Skipping data that was previously repaired saves I/O. The same optimization intentionally stops revisiting that data for incremental missed-write synchronization, so later fault classes require a different pass. Optimization and coverage are not monotonic synonyms.

### E — lower repair I/O ≠ lower total maintenance complexity

Incremental repair replaces repeated full-range checking with retained repair metadata, anti-compaction, separate compaction populations, cadence management, and—later—session-state coordination. Work is redistributed rather than abolished.

### E — maintenance classification can shape forgetting/reclamation without being deletion state

The 3.11 compaction documentation's repaired/unrepaired separation can impede tombstone dropping if incremental repair is abandoned. Case 41's negative deletion evidence and Case 48's repair-history evidence are distinct, but they compose: **how the system remembers maintenance can constrain when it can forget obsolete data.**

---

## Philosophical / media-theoretical interpretation

This case sharpens a narrower proposition than “systems remember their own history.”

The technically precise point is:

> **A system can retain a result of previous maintenance because that result determines what future maintenance is allowed to ignore. Once that happens, the truth and currentness of the maintenance-history state matter operationally.**

This produces a second-order retention relation:

```text
payload is retained
    because repair can restore replica agreement

repair effort is reduced
    because the system retains evidence of past repair

that retained evidence must itself remain sufficiently trustworthy
    or future repair scope becomes wrong/inefficient
```

The 4.0 pending-repair redesign adds a temporal boundary between **being under maintenance** and **having completed maintenance**. The system must retain that distinction long enough to decide whether the attempt becomes accepted repair history or is rolled back to an unrepaired obligation.

This is relevant to philosophical questions about memory of maintenance, institutionalized care, and second-order technical memory, but it does not by itself establish Stieglerian tertiary retention or a human-memory analogy. `repairedAt` is storage-engine control state.

---

## Functional analogies

### A — Cassandra `repairedAt` and SSD protection-health metadata

Case 38's Intel PLI SMART state and this case both retain information about maintenance/protection history rather than user payload. But:

- Intel AFh/AEh describes a device protection path and test/event history;
- Cassandra `repairedAt` changes incremental anti-entropy selection and compaction grouping;
- no historical relation or common implementation lineage is claimed.

### A — Cassandra repair-state handoff and representation handoff in Windows Azure LRC

Case 24 retains coding progress/completion before old replicas are retired. Cassandra 4.0 retains a pending-repair session before data is promoted into the repaired class. Both illustrate that **in-progress representation/work state need not be admissible as completed state**.

The mechanisms are otherwise different: one converts immutable extent redundancy representation; the other coordinates anti-entropy maintenance eligibility.

### A — Cassandra repaired/unrepaired state and AVATAR/RAIDR maintenance classifications

Cases 40 and 43 attach retained classifications to DRAM rows to choose later refresh policy. Cassandra attaches repair-history classification to SSTables/ranges to choose later repair scope. The shared relation is only second-order maintenance selection; physical substrate, failure model, timing, and historical genealogy differ completely.

---

## Prior art and novelty boundary

This case must not claim Cassandra invented anti-entropy, Merkle-tree comparison, repair bookkeeping, or the general idea of remembering maintenance history.

Cassandra's own CASSANDRA-5351 supplies a narrower historical claim: **within Cassandra**, the 2.1 feature explicitly introduced remembering successfully repaired SSTables so default repair could avoid reprocessing them and required repaired/unrepaired segregation during compaction.

Case 23 already anchors Dynamo's 2007 Merkle-tree anti-entropy as an earlier distributed-store comparison. The present contribution is therefore not a generic anti-entropy genealogy; it is the retention-specific analysis of **repair history becoming future repair eligibility state**, plus the later Cassandra evidence that this control state itself needed stronger consistency semantics.

---

## Counterexamples and limits

- `repairedAt` is not a proof that every replica is currently identical forever.
- A repaired SSTable can later be affected by corruption, operator loss, or software bugs; Apache explicitly keeps full repair as a separate tool.
- The 3.11 repair documentation describes intended/default incremental-repair semantics, while CASSANDRA-9143 and later Apache operational writing qualify the safety of legacy 3.x incremental repair. This case therefore does not advertise Cassandra 3.11 incremental repair as universally reliable.
- CASSANDRA-9143 documents repair-state inconsistency and the 4.0 redesign; it does not license unsourced claims that every metadata inconsistency necessarily caused payload loss.
- `pendingRepair` is a later Cassandra mechanism and must not be projected backward into 2.1/3.11 historical vocabulary.
- Full repair, incremental repair, validation, anti-compaction, ordinary compaction, hints, tombstone reclamation, and secure erasure remain different mechanisms.
- The case does not provide a general LSM-tree compaction history.
- The case does not establish that modern Cassandra's newest auto-repair implementation has the same operator boundary as 3.11; that is later work.

---

## Related repositories

A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for Cassandra incremental repair, `repairedAt`, anti-compaction, and Merkle repair found no dedicated overlapping technical-history case during this slice. The material therefore stays here as a retention-specific distributed-maintenance study rather than duplicating an existing mechanism history.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) supplies the methodological guard: the strongest historical language comes from CASSANDRA-5351 itself—**“remembering which sstables have already been successfully repaired”**—while `maintenance-history state` and `future-maintenance eligibility` remain modern project reconstruction terms.

---

## Sources

### Primary Apache sources

1. Apache Cassandra JIRA, **CASSANDRA-5351 — Avoid repairing already-repaired data by default**, fixed in 2.1 beta1: <https://issues.apache.org/jira/browse/CASSANDRA-5351>
2. Apache Cassandra 3.11 documentation, **Repair**: <https://cassandra.apache.org/doc/3.11/cassandra/operating/repair.html>
3. Apache Cassandra 3.11 documentation, **Compaction**, especially `Repaired/unrepaired data`: <https://cassandra.apache.org/doc/3.11/cassandra/operating/compaction/index.html>
4. Apache Cassandra source, branch `cassandra-3.11`, `StatsMetadata.java`: <https://github.com/apache/cassandra/blob/cassandra-3.11/src/java/org/apache/cassandra/io/sstable/metadata/StatsMetadata.java>
5. Apache Cassandra source, branch `cassandra-3.11`, `CompactionManager.java`: <https://github.com/apache/cassandra/blob/cassandra-3.11/src/java/org/apache/cassandra/db/compaction/CompactionManager.java>
6. Apache Cassandra source, branch `cassandra-3.11`, `CompactionStrategyManager.java`: <https://github.com/apache/cassandra/blob/cassandra-3.11/src/java/org/apache/cassandra/db/compaction/CompactionStrategyManager.java>
7. Apache Cassandra JIRA, **CASSANDRA-9143 — Fix consistency of incrementally repaired data across replicas**, fixed in 4.0: <https://issues.apache.org/jira/browse/CASSANDRA-9143>
8. Apache Cassandra source, branch `cassandra-4.0`, `PendingAntiCompaction.java`: <https://github.com/apache/cassandra/blob/cassandra-4.0/src/java/org/apache/cassandra/db/repair/PendingAntiCompaction.java>
9. Apache Cassandra source, branch `cassandra-4.0`, `LocalSessions.java`: <https://github.com/apache/cassandra/blob/cassandra-4.0/src/java/org/apache/cassandra/repair/consistent/LocalSessions.java>

### Context / prior-art controls

10. Apache Cassandra project blog, Alexander Dejanovski, **“Reaper: Anti-entropy Repair Made Easy”**, 28 September 2021: <https://cassandra.apache.org/_/blog/Reaper-Anti-entropy-Repair-Made-Easy.html>. Useful as a later operational qualification; not used to back-project Reaper or 4.0 behavior into Cassandra 3.11.
11. [`Case 23 — Amazon Dynamo`](23-amazon-dynamo-divergent-version-anti-entropy.md), for the already-grounded 2007 Merkle-tree/anti-entropy comparison.
12. [`Case 41 — Cassandra GC Grace`](41-apache-cassandra-tombstone-gc-grace-resurrection.md), for tombstone retention and deletion-resurrection semantics deliberately kept separate from this repair-history slice.

---

## Status

**Grounded.**

The bounded claim is supported by Apache's own feature issue, versioned 3.11 operator documentation, 3.11 implementation state (`repairedAt`, anti-compaction, repaired/unrepaired compaction separation), the defect record that exposes inconsistency in the maintenance-state relation, and the 4.0 source that introduces an explicit pending-repair/session handoff. The case deliberately leaves modern auto-repair scheduling, post-4.0 repair evolution, independent fault injection, and broader anti-entropy genealogy for separate work.