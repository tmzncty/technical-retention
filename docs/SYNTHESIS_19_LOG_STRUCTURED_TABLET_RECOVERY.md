# Synthesis 19 — Log-Structured Tablet Recovery: Redo, Memtable, Materialization, Membership, and Retirement

## Status and scope

**Bounded engineering synthesis over already-grounded recovery and compaction cases.** This document closes one explicit ROADMAP question:

> In log-structured tablet recovery, how should committed redo history, volatile memtable state, immutable materialized files, live-file membership, redo points, replay cost, and deletion-marker retirement be separated?

The bounded answer is:

> **A recoverable tablet is not identical to one log, one memtable, or one immutable file. In the 2006 Bigtable design, committed mutation history, volatile serving state, immutable SSTable materializations, retained live-file membership, redo boundaries, and negative deletion state have different lifetimes and different jobs. Compaction can move current state into a replacement materialization and reduce future replay work; it can later make older positive and negative embodiments dispensable, but only after the current-view and membership relations no longer need them.**

The synthesis is centered on:

- [Case 57 — Google Bigtable tablet log/memtable/SSTable recovery](../cases/57-google-bigtable-tablet-log-memtable-recovery.md), the canonical tablet-recovery case;
- [Case 42 — Kafka 0.8.1 log compaction](../cases/42-apache-kafka-log-compaction-delete-marker-retention.md), a counterexample to treating all `compaction` as the same identity/retirement contract;
- [Case 41 — Cassandra tombstone GC grace](../cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md), a counterexample to treating all negative-state retention as one grace-window mechanism;
- [Case 58 — Raft snapshot/log compaction](../cases/58-raft-snapshot-log-compaction.md), a counterexample showing that history-to-state materialization can carry consensus-specific continuation and repair semantics absent from Bigtable.

Historical facts remain in those canonical cases and evidence records. The decomposition below is **engineering reconstruction**. Cross-system comparisons are **functional analogies** unless explicitly marked as historical record. This synthesis does not claim that Bigtable invented logging, memtables, SSTables, LSM trees, compaction, tombstones, checkpoints, or current-state reconstruction.

---

## 1. The mistaken model: the log is the database and compaction is only space cleanup

A tempting simplified picture is:

```text
append mutation to log
    -> log is the durable database
    -> copy state into memory for speed
    -> occasionally compact old files to save space
```

The grounded Bigtable case breaks every arrow if it is read too strongly.

The commit log is a redo representation for recent committed mutations, but ordinary reads are assembled from a volatile memtable plus the current immutable SSTable set. The memtable is therefore part of the serving embodiment without being the sole durability witness. Conversely, a perfectly readable SSTable is not automatically part of the current tablet: `METADATA` retains which SSTables belong to the tablet. Redo points say where recovery must look into the commit-log history. Minor compaction does not make an uncommitted mutation committed; it materializes already-committed current state and reduces later replay work. Major compaction can eliminate deletion entries only after it has rewritten the complete current view that made those negative records necessary.

The more useful question is therefore:

> **Which representation currently serves the value, which retained relation makes that representation part of the tablet, and which older history or negative evidence remains necessary for a future recovery?**

---

## 2. Eight relations that must remain distinct

### 2.1 Committed redo history

Question:

> Which recent mutations have already crossed the tablet's commit step and therefore must remain recoverable after RAM loss?

In the bounded 2006 Bigtable path, a valid mutation is written to the commit log and only **after the write has committed** is its content inserted into the memtable.

Therefore:

```text
mutation accepted into a volatile working structure
    != original durability event

committed redo record
    != permanent requirement to retain that exact log record forever
```

The redo record is one recovery embodiment of a committed logical mutation. Later materialization can change which embodiment future recovery needs.

### 2.2 Volatile memtable working embodiment

Question:

> Which committed updates are currently held in the sorted in-memory structure that participates directly in reads?

The memtable is volatile, current, and service-relevant. Losing it in a tablet-server failure is expected to be recoverable by combining retained SSTables, redo points, and committed log entries.

Therefore:

```text
volatile memtable loss
    != committed mutation loss

serving embodiment volatility
    != logical commitment volatility
```

The recovered memtable is a new working embodiment of the same qualified mutations, not resurrection of the lost RAM objects.

### 2.3 Immutable materialized SSTables

Question:

> Which already-current state has been rewritten into persistent immutable sorted maps?

Minor compaction freezes a memtable and writes its contents as a new SSTable. Merging and major compactions can produce a new SSTable from several existing inputs. This is not merely byte relocation: the output can replace several prior embodiments as the materialized form used by future reads and recovery.

Therefore:

```text
mutation committed
    != mutation already materialized in an SSTable

materialized in an SSTable
    != this SSTable is the only current tablet embodiment
```

### 2.4 Live-file membership

Question:

> Which immutable SSTables currently constitute the tablet's materialized state?

Bigtable records the tablet's current SSTable set in `METADATA`. Immutability makes a file self-consistent as an object, but does not make it eternally current.

Therefore:

```text
immutable SSTable survives physically
    != SSTable is current tablet state

live-file membership metadata
    != user payload
```

This is one of the strongest examples in the repository of **presence requiring a separate membership/currentness relation**.

### 2.5 Redo points / replay boundary

Question:

> From where in retained commit-log history must recovery begin applying mutations that are not already covered by current materialized state?

`METADATA` retains redo points alongside the current SSTable set. A redo point is not itself the mutations and it is not a compressed copy of the log. It is a boundary relation connecting materialized state to still-needed history.

Therefore:

```text
redo point
    != redo history

replay boundary retained
    != replay work already performed
```

### 2.6 Replay work and recovery cost

Question:

> How much retained history must be read and reapplied before a replacement tablet server can resume the current volatile working state?

Bigtable explicitly says minor compaction reduces the amount of commit-log data that must be read during recovery. That makes replay cost a consequence of the current representation split, not another stored payload object.

Therefore:

```text
current logical state unchanged
    while
future recovery work changes
```

A retention mechanism can improve **future recoverability cost** without creating a new application-visible value.

### 2.7 Deletion entries / negative currentness

Question:

> Which negative state must remain so a merged read does not revive an older positive value that still survives in an older live SSTable?

Non-major Bigtable compactions may retain deletion entries because older live SSTables can still contain the deleted data. A major compaction rewrites the complete current view and can produce an output containing neither the deletion entry nor the deleted data.

Therefore:

```text
delete becomes current
    != old positive embodiment already absent

deletion entry physically present
    != deletion must remain forever
```

Negative state is retained because of a relation to older still-live positive embodiments.

### 2.8 Obsolete-file reclamation

Question:

> When an immutable SSTable is no longer in the current live-file set, when does its physical file disappear?

Bigtable treats permanently removing obsolete data as garbage collection of immutable SSTables. The master uses the `METADATA` live set as roots and deletes files outside that set.

Therefore:

```text
SSTable removed from current membership
    != file already physically deleted

Bigtable-level file deletion
    != lower-media sanitization
```

Representation retirement and physical reclamation are separate transitions.

---

## 3. Commit, materialization, and replay-horizon movement are different events

The bounded write path is:

```text
mutation
    -> commit-log write commits
    -> mutation enters volatile memtable
    -> reads can merge memtable + SSTables
    -> memtable later freezes
    -> new SSTable is produced
    -> future recovery needs less old log replay
```

This exposes three distinct times:

1. **commit time** — the mutation gains the recoverability relation promised by the bounded implementation;
2. **serving time** — the committed mutation participates through the volatile memtable in ordinary reads;
3. **materialization time** — compaction creates a persistent sorted-table embodiment that can move the future replay horizon.

Hence:

```text
commit completion
    != memtable persistence
    != compaction completion
    != old-log reclamation
```

Minor compaction is retention maintenance because it changes how much historical redo must remain operationally relevant to a future restart. It is not a second user commit.

Planned tablet movement makes this relation especially visible. The source server can minor-compact, stop serving, then perform a second usually-fast minor compaction so the destination can load the tablet without log recovery. Materialization deliberately replaces a replay dependency before handoff.

---

## 4. The current tablet is a composition, not one privileged file

Bigtable reads merge the memtable with the tablet's live SSTables. Thus the phrase `current tablet state` names a relation among several embodiments:

```text
current view
    = volatile current entries
    + current immutable components
    + ordering/version/deletion semantics
    + membership metadata selecting the components
```

There need not be one physical file containing the entire current state at every moment.

Two counterexamples follow:

```text
physically newest file
    != necessarily complete current tablet

physically surviving old file
    != necessarily current tablet member
```

The first blocks a naive `latest file = state` model. The second blocks a naive forensic/presence model in which readable bytes automatically count as current service state.

---

## 5. Replay boundary is not replay history, and neither is replay cost

Recovery composes:

```text
current SSTable membership
    + redo points
    + surviving SSTables
    + committed log suffix
    -> reconstructed memtable/current service state
```

Each item answers a different question:

- the SSTables contain materialized values;
- membership says which materializations are current;
- redo points locate the still-relevant history interval;
- commit-log records carry the mutations to replay;
- replay execution reconstructs a volatile working embodiment.

A smaller replay interval is therefore not itself `more durable`. It can mean that more current state has already crossed the materialization handoff.

Conversely, retaining more old log bytes does not by itself make recovery more correct. If membership or replay-boundary relations are wrong, more surviving history can be irrelevant or can require additional duplicate/currentness interpretation.

Bigtable's shared tablet-server commit log adds another separation. Many tablets share one physical append stream, and after failure the log is sorted by `<table, row name, log sequence number>` to recover tablet-local histories. Physical sequentiality is therefore not the logical object-history boundary. Sequence numbers can also let recovery elide duplicate durable entries introduced by log-writer switching.

Thus:

```text
one physical log
    != one logical tablet history

duplicate durable redo records
    != duplicate logical application
```

---

## 6. Deletion retirement is a relation to surviving older state

The bounded Bigtable deletion sequence is:

```text
old positive value survives in older SSTable
    -> deletion entry becomes current
    -> merged read suppresses old value
    -> non-major compaction may retain negative entry
    -> major compaction rewrites complete current view
    -> new output contains neither deleted value nor delete entry
    -> old input SSTables become obsolete
    -> later file GC can reclaim obsolete physical files
```

This gives four distinct forgetting stages:

1. **logical invalidation** — the old value ceases to be admissible in the current view;
2. **negative-evidence retention** — a deletion entry remains necessary while older positive state is still live;
3. **representation closure** — major compaction produces a current view that needs neither the old positive embodiment nor the negative marker;
4. **physical file reclamation** — obsolete SSTable files are later deleted from the live GFS file population.

None of these, in the 2006 Bigtable paper, establishes lower-device overwrite or secure sanitization.

The key retention rule is:

> **A negative record can become dispensable not merely because time passed, but because the older positive embodiments against which it carried authority have themselves been removed from the current representation.**

---

## 7. Counterexample: Kafka `compaction` has a different identity contract

Case 42 prevents the word `compaction` from becoming a generic mechanism name.

Kafka 0.8.1 keyed log compaction retains at least the latest known value per key while allowing superseded records to disappear. Logical offsets remain permanent positions even after the record that once occupied an offset is removed, and null-payload delete markers have an observer-progress/time-bounded retention contract.

Bigtable's bounded mechanism is different:

- tablet reads merge memtable plus live SSTables;
- minor compaction reduces redo replay work;
- `METADATA` selects current immutable components;
- deletion entries are tied to older live SSTables and can disappear through full current-view rewriting.

Therefore:

```text
Bigtable compaction
    != Kafka keyed-log compaction

immutable-SSTable membership
    != permanent Kafka logical offset

Bigtable deletion-entry retirement
    != Kafka delete.retention.ms observer window
```

The similarity is functional: both deliberately rewrite representations so some older history can disappear while a current result remains reconstructible.

---

## 8. Counterexample: Cassandra tombstone grace has a different safety relation

Case 41 prevents all negative state from being normalized into one tombstone rule.

Cassandra retains tombstones across a bounded age/failure envelope because a disconnected stale replica may otherwise later reintroduce an older positive value through repair. The later optional repaired-state gate further separates age eligibility from repair-qualified retirement authority.

Bigtable 2006, in the bounded source, gives a different reason for retaining deletion entries: older live SSTables can still contain deleted data, and a complete major compaction can rewrite a representation needing neither the positive value nor the deletion entry.

Therefore:

```text
negative-state retention
    != one universal grace clock

Bigtable major-compaction closure
    != Cassandra replica-repair convergence
```

The two systems support a functional comparison about temporary negative currentness evidence, not a shared mechanism or genealogy.

---

## 9. Counterexample: Raft snapshotting carries consensus continuation semantics

Case 58 and Synthesis 18 show another form of history-to-state materialization. A committed Raft log prefix can be replaced by a stable snapshot plus `lastIncludedIndex`, `lastIncludedTerm`, effective configuration, and a remaining suffix; lagging followers may then require `InstallSnapshot` instead of entry replay.

Bigtable's redo points and SSTable membership do not carry Raft's consensus term/configuration semantics. A materialized SSTable is not a consensus snapshot, and Bigtable recovery is not `InstallSnapshot` state transfer.

The bounded functional analogy is only:

```text
detailed recent history
    -> materialized current state
    -> future replay requirement can shrink
```

The continuation metadata, authority model, and repair protocol remain system-specific.

---

## 10. Failure and forgetting taxonomy

This synthesis exposes several distinct failure classes. Only the source-grounded mechanism is asserted historically; the failure decomposition below is engineering reconstruction unless a canonical case records an observed failure.

### 10.1 Memtable embodiment is lost

Expected tablet-server failure can destroy RAM while committed mutations remain reconstructible from retained persistent relations.

```text
memtable lost
    != automatically logical state lost
```

### 10.2 SSTable bytes survive but live-file membership is lost or wrong

Readable immutable files are not enough by themselves to identify the current tablet composition.

```text
payload present
    != current membership recoverable
```

### 10.3 Redo history survives but the replay boundary is unavailable or wrong

A log population without the relation saying where current materialization ends and replay begins is a different failure from missing payload.

A too-old boundary can increase replay/duplicate interpretation work; a wrongly advanced boundary can threaten omission of needed updates. The 2006 paper does not provide a crash-window fault matrix for those metadata transitions, so this remains a reconstruction target rather than an observed Bigtable bug claim.

### 10.4 Compaction output is incomplete while source inputs are retired

Safe representation handoff requires the replacement current representation to become admissible before its sole source embodiments are made dispensable. Exact Bigtable metadata-update atomicity is outside the bounded source, so this is a general handoff invariant to test, not a historical accusation.

### 10.5 Deletion evidence is retired while an older positive embodiment remains current-live

The negative relation would no longer suppress the older value. Bigtable's major-compaction rule is important precisely because it can eliminate both sides in one complete rewritten current view. The repository should not infer a documented Bigtable resurrection incident from this mechanism alone.

### 10.6 Obsolete file survives after membership retirement

This is a reclamation/space/forensic residue state, not proof that the old file remains current tablet state.

### 10.7 Bigtable-level deletion completes but lower media retains traces

The 2006 paper's claim that deleted data disappears from the system is bounded to Bigtable's live representation. Lower GFS/disk/Flash remanence, backups, and secure erasure are outside the case.

---

## 11. Historical record, reconstruction, analogy, interpretation

### Historical record

The canonical Case 57 and Evidence 57 retain the sourced 2006 facts:

- commit-log redo precedes memtable insertion;
- reads merge memtable plus current SSTables;
- recovery uses `METADATA` SSTable lists and redo points plus committed log replay;
- minor compaction materializes memtable state and reduces recovery log work;
- merging/major compaction replace older immutable inputs under different scopes;
- deletion entries can suppress values in older live SSTables and disappear after major compaction;
- live SSTable membership roots later file garbage collection;
- one physical tablet-server log can contain many logical tablet histories.

### Engineering reconstruction

Terms such as `representation handoff`, `replay horizon`, `materialization closure`, `negative-evidence lifetime`, and `recovery-cost retention` are project terms used to separate the relations above.

### Functional analogy

Kafka, Cassandra, and Raft are compared only to show that the same broad words—`compaction`, `delete marker`/negative state, `snapshot`/materialization—can implement different retention contracts.

### Philosophical interpretation

No new philosophical thesis is required to close this roadmap item. A later interpretation may ask how a technical system can preserve an admissible current state while deliberately discarding much of the sequence that produced it, but that question remains downstream of the engineering distinctions.

---

## 12. Prior art and novelty boundary

Bigtable's own 2006 paper explicitly describes its memtable/SSTable organization as analogous to the earlier LSM-tree and cites O'Neil et al. 1996. The same bibliography points to earlier logging/group-commit work. Case 57 therefore already blocks claims that Bigtable invented LSM organization, redo logging, or group commit.

This synthesis makes no invention claim for:

- write-ahead/redo logging;
- memory-to-disk materialization;
- LSM trees;
- compaction;
- deletion markers;
- checkpoints or replay boundaries;
- garbage collection of obsolete files.

The project contribution is narrower:

> **Across grounded cases, current-state reconstruction must separately audit redo commitment, volatile serving embodiment, immutable materialization, live membership, replay boundary, recovery work, negative currentness, and physical reclamation. The same word `compaction` cannot safely stand in for all eight.**

A fresh search of `tmzncty/computing-archaeology` for `Bigtable`, `memtable`, `SSTable`, `commit log`, and `tablet recovery` found no dedicated case to reuse. A broader LSM/WAL/tablet/database-storage genealogy belongs there if later developed; this repository keeps only the retention-specific relation decomposition.

---

## 13. Guardrails carried forward

Use these in later cases:

```text
committed redo history != volatile memtable embodiment
commit completion != materialization completion
volatile serving-state loss != committed mutation loss
current tablet != one physical file
immutable file survival != live-file membership
live-file membership != payload
redo point != redo history
replay boundary != replay work
materialization can reduce future history-retention obligation
deletion currentness != deletion-marker retention
marker retirement != obsolete-file reclamation
obsolete-file reclamation != secure sanitization
one physical append log != one logical object history
duplicate durable redo != duplicate logical replay
Bigtable compaction != Kafka compaction != Raft snapshotting
Bigtable deletion-entry retirement != Cassandra tombstone grace
```

The ROADMAP question is closed only at this bounded relation-decomposition level. Exact Bigtable metadata-update crash windows, code-level implementation archaeology, later Bigtable/Cloud Bigtable evolution, RocksDB/LevelDB/HBase descendants, compaction fault injection, and broader database/WAL/LSM genealogy remain separate work.
