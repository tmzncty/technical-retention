# Case 48 deepening — 2017–2018 Cassandra repair-session durability, referential integrity, and overlap isolation

## Status

**`bounded deepening complete`**

This addendum deepens one narrow part of Case 48: after Cassandra's consistent incremental-repair redesign introduced a persisted local repair session and `pendingRepair` SSTable state, **what had to remain true about the relationship between the session record, the messages published to other participants, and the SSTables that still referred to the session?**

The bounded answer is unusually concrete because three Apache Cassandra bug fixes from 2017–2018 expose three different correctness obligations:

1. **CASSANDRA-13660 (2017):** a participant must durably persist `FINALIZE_PROMISED` before it publishes a successful finalize promise to the coordinator;
2. **CASSANDRA-13758 (2017):** cleanup must not delete a local repair-session record while SSTables still remain associated with that pending-repair session;
3. **CASSANDRA-14763 (2018):** a new incremental-repair prepare must not silently step around intersecting SSTables owned by a different non-finalized repair session, because that older session may later fail and return its data to the unrepaired set.

Together they show that the new intermediate repair state was not just an extra enum. It created a retained **control relation** whose durability, lifetime, and scope had to stay aligned with the physical SSTables and with externally visible protocol progress.

The bounded retention claim is:

> **For Cassandra's consistent incremental-repair handoff, a session state can become authoritative only after the relevant local state is durable enough to survive the failure model assumed by the protocol; that session record cannot safely be discarded while storage objects still refer to it; and a later maintenance pass cannot treat an overlapping non-finalized session as irrelevant merely because the newer pass itself completes.**

`publication frontier`, `durability-before-promise`, `repair-session referential integrity`, `maintenance-epoch overlap`, and `control-state authority` are project reconstruction terms. Apache's direct vocabulary includes `system.repairs`, `FINALIZE_PROMISED`, `FinalizePromise`, `pending repair`, `LocalSession`, `pendingRepair`, `repairedAt`, `FINALIZED`, `FAILED`, and `unrepaired`.

---

## Research question

Case 48 already grounds the broad 2.1 → 3.11 → 4.0 story:

```text
remember successful repair
    -> repairedAt / repaired-vs-unrepaired classes
    -> legacy classification inconsistency
    -> pending-repair/session handoff before promotion to repaired
```

That leaves a narrower question:

> Once an in-progress repair session itself becomes retained state, what evidence shows how long that state must survive and when it is allowed to become externally authoritative or disposable?

This addendum does **not** attempt a complete history of Cassandra 4.0 repair development. It isolates three source-level corrections that directly expose the lifetime rules of the retained control state.

---

## Source ladder and provenance

### A. CASSANDRA-13660 and commit `7df240e74f0bda9a15eff3c9de02eb0cd8771b20`

Primary Apache sources:

- Apache JIRA, **CASSANDRA-13660 — Correctly timed kill -9 can put incremental repair sessions in an illegal state**: <https://issues.apache.org/jira/browse/CASSANDRA-13660>
- Apache Cassandra commit, **“Flush system.repair table before IR finalize promise”**, 6 July 2017: <https://github.com/apache/cassandra/commit/7df240e74f0bda9a15eff3c9de02eb0cd8771b20>

The Jira gives the failure sequence. The commit gives the implementation correction in `LocalSessions.java`.

### B. CASSANDRA-13758 and commit `e1a1b80d424e31eeb5805c710ce010953160e3a4`

Primary Apache sources:

- Apache JIRA, **CASSANDRA-13758 — Incremental repair sessions shouldn't be deleted if they still have sstables**: <https://issues.apache.org/jira/browse/CASSANDRA-13758>
- Apache Cassandra commit, **“Don't delete incremental repair sessions if they still have sstables”**, 18 August 2017: <https://github.com/apache/cassandra/commit/e1a1b80d424e31eeb5805c710ce010953160e3a4>

The Jira states the semantic failure caused by premature session deletion. The commit shows cleanup consulting pending-repair SSTable membership before deleting the session.

### C. CASSANDRA-14763 and commit `167ebbcf4304512fa538e9cfc18da4295511d16c`

Primary Apache sources:

- Apache JIRA, **CASSANDRA-14763 — Fail incremental repair prepare phase if it encounters sstables from un-finalized sessions**: <https://issues.apache.org/jira/browse/CASSANDRA-14763>
- Apache Cassandra commit, **“Fail incremental repair prepare phase if it encounters sstables from un-finalized sessions”**, 21 September 2018: <https://github.com/apache/cassandra/commit/167ebbcf4304512fa538e9cfc18da4295511d16c>

The Jira explains why an overlapping pending session invalidates a tempting “latest successful repair = high-water mark” assumption. The commit makes that overlap a prepare-phase failure rather than silently excluding the other session's SSTables.

### D. Context only: CASSANDRA-9143

Case 48 already uses CASSANDRA-9143 as the main redesign anchor. It remains context here, not a newly researched novelty claim:

- <https://issues.apache.org/jira/browse/CASSANDRA-9143>

---

## Historical record

### 1. CASSANDRA-13660 exposes a crash window between local state transition and published protocol promise

Apache's Jira describes a precisely timed failure:

1. a participant has reached the point where it sends a finalize promise to the incremental-repair coordinator;
2. the local `FINALIZE_PROMISED` mutation has not yet been synced durably;
3. the process is killed;
4. after restart, the local session can reappear in an earlier state;
5. later recovery encounters an illegal transition such as `PREPARED -> FINALIZED`.

The issue is explicit that the problem is **not** simply “a repair message was lost.” The problematic state is the opposite: the coordinator may have observed a successful promise that the participant's durable local state cannot reproduce after restart.

Safe historical statement:

> by July 2017, Apache developers had identified that the consistent-repair protocol could publish a finalize promise before the participant's corresponding local session state was durably recoverable.

### 2. The CASSANDRA-13660 fix orders durable local state before external promise

Commit `7df240e...` adds `syncTable()` in `LocalSessions.java` and calls it after `setStateAndSave(session, FINALIZE_PROMISED)` but **before** sending `FinalizePromise` to the coordinator.

The code comment gives the rationale directly: without the blocking flush, a failure after responding but before the commit-log mutation had reached stable storage could make the session revert on startup and prevent failure recovery from promoting it correctly.

The critical order becomes:

```text
set local session = FINALIZE_PROMISED
    -> forceBlockingFlush(system.repairs)
    -> send successful FinalizePromise
```

not:

```text
set state in a not-yet-stable form
    -> publish promise
    -> maybe become durable later
```

This is direct source evidence for **durability-before-promise** in this bounded protocol transition.

It does **not** establish that every Cassandra repair-session mutation is synchronously flushed before every message. The commit is about this particular finalize-promise boundary.

### 3. A protocol message being observable is not equivalent to its causal state being restart-safe

The 2017 bug separates three events that are easy to collapse:

```text
state transition executed in process
    != state transition durable across restart
    != successful promise observed by coordinator
```

The fix specifically constrains their ordering at one point:

```text
restart-surviving local promise state
    must precede
externally visible successful promise
```

The commit comment connects violation of that order to possible inconsistency in repaired-data sets across nodes. That is stronger than a cosmetic observability bug, while still not proving a specific user-payload corruption trace for every crash in the window.

### 4. CASSANDRA-13758 exposes a second lifetime: completed/old session metadata can still be referenced by SSTables

A month later, CASSANDRA-13758 records a different failure mode. Local incremental-repair session cleanup could decide a session was old enough to delete without first checking whether SSTables were still marked as belonging to that repair.

The Jira states the consequence directly:

> deleting a successful repair session while outstanding SSTables still belong to it can cause those SSTables to be demoted to unrepaired, creating an inconsistency.

Normally the associated SSTables were expected to have been promoted or demoted already. The issue was raised because bugs such as reference leaks could leave them behind, and the cleanup path needed to be robust against those exceptional states.

This gives a direct historical boundary:

```text
session is logically old/completed enough for normal cleanup
    !=
session record is necessarily unreferenced and disposable
```

### 5. The CASSANDRA-13758 fix makes deletion depend on whether pending-repair data still exists

Commit `e1a1b80...` adds an explicit reference check across the compaction state:

- `CompactionStrategyManager.hasDataForPendingRepair(sessionID)`;
- `PendingRepairManager.hasDataForSession(sessionID)`;
- `LocalSessions.sessionHasData(session)`.

The cleanup path changes from unconditional age/state-driven deletion to:

```text
if session is eligible for cleanup:
    if no pending-repair SSTable data remains:
        delete session
    else:
        retain session and warn
```

The tests added by the same commit cover both cases: sessions with no remaining SSTables can be deleted; sessions with remaining pending-repair data remain present in memory and in the persisted session table.

This is strong source-level evidence for a **referential-lifetime rule** between control metadata and storage objects.

### 6. Session metadata is therefore not merely an operator audit record

If deleting the session record can change the treatment of SSTables that still carry the session identifier, the record participates in the interpretation of those SSTables.

Bounded engineering consequence:

```text
pendingRepair UUID on SSTable
    + local session record
    -> meaningful in-progress/completed repair relation
```

Removing one side while the other survives can change later classification behavior.

This does not mean the relation is implemented as a general-purpose database foreign key. `repair-session referential integrity` is project language for the narrower invariant exposed by the fix.

### 7. CASSANDRA-14763 exposes a third lifetime: one unfinished maintenance epoch can constrain the next

In September 2018, CASSANDRA-14763 addressed an overlap problem during incremental-repair prepare.

The Jira explains that a pending repair session can remain isolated for a period and may later fail, at which point its SSTables move back to the unrepaired set. Before the fix, a newer repair prepare could ignore SSTables already pending another session for the same range and proceed with the remaining data.

That is unsafe for a particular operational expectation. If the newer repair succeeds while the older pending session is still excluded, and the older session later fails and returns its data to unrepaired, then the newer successful repair cannot safely be treated as a high-water mark proving that all older received data has been repaired.

The Jira states this explicitly:

> you can't use the most recent successful incremental repair as the high water mark for fully repaired data.

### 8. The CASSANDRA-14763 fix turns overlapping non-finalized pending state into a prepare failure

Commit `167ebbcf...` changes `PendingAntiCompaction.AcquisitionCallable` so it:

- scans intersecting live SSTables;
- excludes already repaired SSTables;
- notices SSTables carrying another `pendingRepair` session;
- checks whether that other session is finalized;
- records conflicting non-finalized session IDs;
- fails the new acquisition if such conflicts exist.

The implementation comment gives the reasoning: if the other session later fails and returns its data to unrepaired, silently proceeding would violate the normal expectation that data received before the successful repair is covered by that repair.

The same commit also adds a post-acquisition check to abort if an acquired SSTable raced into repaired or pending-repair state.

Therefore:

```text
new repair can ignore a currently isolated overlapping epoch
    !=
new repair can later claim an unqualified high-water mark
```

### 9. Finished session and finalized session are not interchangeable with “no longer relevant”

Across these fixes, several distinct notions appear:

- state has advanced in memory;
- state is restart-surviving;
- coordinator has observed a promise;
- session is finalized or failed;
- SSTables still reference the session;
- a later repair overlaps the same range;
- cleanup considers the session old enough to delete.

No inspected source licenses collapsing these into one Boolean `done` bit.

---

## Retained-state decomposition

This slice sharpens Case 48's state model into at least these separable relations.

### 1. User payload and ordinary Cassandra timestamps

The replicated data whose cross-replica agreement repair ultimately protects.

### 2. `repairedAt`

Legacy/completed repair-history classification that changes later repair selection and compaction grouping.

### 3. SSTable `pendingRepair` identifier

A storage-object-level relation linking SSTable data to an in-progress consistent repair session.

### 4. Persisted local repair-session row

The `system.repairs` / `LocalSession` state used by the consistent-repair protocol, including session identity and state.

### 5. In-memory session state

The currently loaded runtime representation. CASSANDRA-13660 demonstrates that mutation of runtime/logged state is not identical to the stronger durability needed before a finalize promise is exposed.

### 6. External protocol observation

The coordinator's observation of a successful `FinalizePromise`.

### 7. Compaction/pending-repair membership

Whether live SSTables still exist in the pending-repair group for a session.

### 8. Cleanup eligibility

A policy judgment that a session is old/completed enough that deletion would normally be considered.

### 9. Overlap/conflict relation

Whether another non-finalized repair session owns intersecting SSTables for the range a new repair wants to isolate.

These are not interchangeable:

```text
runtime state advanced
    != durable state advanced
    != peer observed promise

session old enough for cleanup
    != no SSTable still refers to session

new repair completed
    != all older overlapping pending data is thereby covered
```

---

## Engineering reconstruction

### E — protocol authority may require a durability threshold, not merely a local write

CASSANDRA-13660 supports a bounded reconstruction:

> At the finalize-promise boundary, the participant's promise becomes safe to publish only after the local session state needed to honor/recover that promise has crossed the required durability boundary.

The exact storage mechanism in this 2017 fix is a blocking flush of the repairs table. The broader phrase `durability threshold` is analytical shorthand, not Apache vocabulary.

### E — “published” and “durable” are two different orderings

A distributed protocol can have a state that is visible to another node but not yet recoverable after local restart. That combination matters because after failure the peer and restarted participant can remember different protocol histories.

For this transition:

```text
publish success before durable state
    -> possible history disagreement after restart
```

The fix makes the stronger state precede publication.

### E — completed workflow state can remain constitutive after the workflow itself has stopped

CASSANDRA-13758 shows that a session record can continue to matter after the normal protocol work is expected to be finished because SSTables may still carry the session identifier.

Therefore:

```text
workflow no longer actively running
    != control record no longer semantically referenced
```

### E — cleanup is a correctness operation when metadata has dependents

Deleting a control record is not always “just freeing metadata.” If surviving storage objects require that record to interpret their maintenance status, cleanup changes the effective system state.

This is why the 2017 fix makes cleanup consult live pending-repair membership.

### E — maintenance epochs can overlap in address space without being independent in truth conditions

CASSANDRA-14763 shows that two repair sessions over intersecting data cannot always be reasoned about as separate jobs. One session's future failure can reclassify SSTables after the newer session has completed.

Thus the newer session's meaning depends on the unresolved older epoch:

```text
successful newer session
    + excluded older pending data
    + older session later fails
    -> some pre-existing data returns to unrepaired
```

The fix avoids granting the newer repair that ambiguous completion by failing prepare when an intersecting non-finalized pending session is found.

### E — high-water marks require closure over deferred state, not just a recent success timestamp

A “latest successful repair” can function as a high-water mark only if the relevant older data cannot later re-enter the not-yet-repaired population outside that success.

This is a reconstruction of the Jira's explicit high-water-mark warning. It is not a claim that Cassandra stores one universal high-water-mark variable.

---

## Functional comparisons

### A — Case 61 HDFS Observer state publication

Case 61's HDFS deepening distinguishes an RPC business result becoming visible from the corresponding freshness metadata being published first. Cassandra's CASSANDRA-13660 has a related ordering shape:

```text
Cassandra:
durable protocol state before successful promise publication

HDFS:
freshness metadata publication before caller can act on returned result
```

The functional analogy is **authority/publication ordering**. The mechanisms differ: Cassandra is protecting crash-recoverable repair-session state; HDFS is propagating a read-freshness frontier.

No historical lineage is claimed.

### A — Case 141 PostgreSQL replication-slot lifetime

Case 141 also contains retained control metadata whose deletion can release a protection relation over other state. Cassandra's local repair-session record similarly cannot always be removed merely because the active operation looks finished.

The analogy stops at **control metadata lifetime constrained by dependent state**. PostgreSQL replication slots retain WAL/history for consumers; Cassandra repair sessions qualify pending SSTable repair membership.

### A — Case 24 Windows Azure LRC representation handoff

Case 24 already supplies the stronger handoff analogy used in the canonical Case 48: intermediate work must not be admitted as completed representation too early. The present addendum sharpens the Cassandra side by showing that even after adding an intermediate state, the implementation still had to define:

- when state is durable enough to promise;
- when metadata is old enough to delete;
- when a newer handoff is blocked by an unresolved older one.

---

## Historical record / reconstruction / analogy / interpretation ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| a kill after finalize promise but before durable local state could restart the session in an earlier state | `H/P` | CASSANDRA-13660 Jira |
| commit `7df240e...` flushes `system.repairs` after `FINALIZE_PROMISED` and before sending `FinalizePromise` | `H/P` | Apache commit |
| a successful promise therefore has a durability-before-publication ordering requirement at this boundary | `E` | direct reconstruction from the fix and code comment |
| deleting an old session while SSTables still belong to it can demote those SSTables and create inconsistency | `H/P` | CASSANDRA-13758 Jira |
| commit `e1a1b80...` makes cleanup retain sessions while pending-repair data remains | `H/P` | Apache commit |
| this is a referential-lifetime relation between control metadata and storage objects | `E` | project term; no claim of general foreign-key mechanism |
| an intersecting non-finalized repair session can invalidate “latest successful repair = high-water mark” | `H/P` | CASSANDRA-14763 Jira |
| commit `167ebbcf...` fails prepare on such conflicting sessions | `H/P` | Apache commit |
| maintenance epochs are not independent when unresolved data can later return to unrepaired | `E` | bounded reconstruction |
| these mechanisms resemble authority/publication and dependent-metadata lifetime patterns in other cases | `A` | functional analogy only |
| maintenance memory has its own conditions for becoming authoritative and for being forgotten | `I` | bounded project interpretation |

---

## Bounded philosophical interpretation

The narrow conceptual point is not simply that “the system remembers repair.” Case 48 already establishes that.

This slice adds two stricter propositions:

> **technical maintenance memory has an admission rule for becoming authoritative, and it can also have a disposal rule for when it is safe to forget that memory.**

In this Cassandra sequence:

```text
control state is produced
    -> must become durable enough before promise publication
    -> may remain referenced by pending SSTables
    -> must survive until those dependents no longer need it
    -> unresolved older state can constrain whether newer maintenance may claim completion
```

That is a useful retention pattern because “remembering” and “forgetting” are both conditional operations on control state.

The sources do not describe this philosophically. They describe repair sessions, SSTables, flushes, cleanup, and prepare failures. `maintenance memory`, `authority`, and `disposal rule` are interpretive vocabulary layered on top of the engineering record.

---

## Explicit non-claims

This addendum does **not** claim:

1. Cassandra invented write-ahead durability, two-phase commit, promises, referential integrity, or distributed repair epochs.
2. `system.repairs` is itself a general consensus log.
3. `forceBlockingFlush()` makes the entire repair protocol crash-atomic under every storage failure.
4. receiving a `FinalizePromise` proves user payload is durably identical on every replica.
5. every deletion of a completed repair session causes inconsistency; CASSANDRA-13758 concerns the case where SSTables still remain associated with it.
6. every overlapping repair is invalid; CASSANDRA-14763 specifically concerns intersecting SSTables owned by other **non-finalized** sessions.
7. a pending session's eventual failure necessarily causes user-visible data loss; the direct evidence is repair-classification/high-water-mark correctness.
8. the 24-hour auto-fail behavior described in CASSANDRA-14763 is a universal value across all later Cassandra versions.
9. `repair-session referential integrity` was Apache's term.
10. the HDFS, PostgreSQL, Azure, and Cassandra mechanisms share a historical genealogy.
11. these 2017–2018 development fixes prove the behavior of every released Cassandra 4.x point release.
12. the evidence here replaces the broader CASSANDRA-9143 redesign history already bounded in Case 48.

---

## What this closes

This addendum boundedly closes a specific evidence debt inside Case 48:

- source-level evidence for **restart durability at the finalize-promise publication boundary**;
- source-level evidence for **session-record lifetime while pending-repair SSTables still refer to it**;
- source-level evidence for **overlap isolation between unresolved and newer repair sessions**.

It does **not** close:

- the full 4.0 → 5.x consistent-repair bug/fix history;
- later zombie/stuck-session operational behavior;
- CASSANDRA-19399 or other post-release repair-session liveness issues;
- modern automatic-repair scheduling;
- independent crash/fault-injection experiments;
- performance costs of blocking flush at the finalize-promise boundary;
- a general theory of distributed transaction protocols.

---

## Related repositories

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for Cassandra incremental repair, `repairedAt`, `pendingRepair`, and consistent repair found no dedicated overlapping technical-history module during this slice.

Accordingly this file keeps only the retention-specific question: **when repair control state becomes authoritative, how long it must remain, and what future maintenance it gates.** A complete Cassandra repair-protocol genealogy, Merkle-tree history, compaction architecture history, or Dynamo→Cassandra lineage still belongs in `computing-archaeology` if pursued.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) remains the methodological guard against turning these bug fixes into anachronistic general theory: the historical actors describe concrete repair-state races and cleanup/overlap failures; the cross-case terminology here is reconstruction.

---

## Sources

### Primary Apache sources

1. Apache JIRA, **CASSANDRA-13660 — Correctly timed kill -9 can put incremental repair sessions in an illegal state**, created 3 July 2017, resolved 6 July 2017: <https://issues.apache.org/jira/browse/CASSANDRA-13660>
2. Apache Cassandra commit `7df240e74f0bda9a15eff3c9de02eb0cd8771b20`, **Flush system.repair table before IR finalize promise**, 6 July 2017: <https://github.com/apache/cassandra/commit/7df240e74f0bda9a15eff3c9de02eb0cd8771b20>
3. Apache JIRA, **CASSANDRA-13758 — Incremental repair sessions shouldn't be deleted if they still have sstables**, created 11 August 2017, resolved 18 August 2017: <https://issues.apache.org/jira/browse/CASSANDRA-13758>
4. Apache Cassandra commit `e1a1b80d424e31eeb5805c710ce010953160e3a4`, **Don't delete incremental repair sessions if they still have sstables**, 18 August 2017: <https://github.com/apache/cassandra/commit/e1a1b80d424e31eeb5805c710ce010953160e3a4>
5. Apache JIRA, **CASSANDRA-14763 — Fail incremental repair prepare phase if it encounters sstables from un-finalized sessions**, created 18 September 2018, resolved 21 September 2018: <https://issues.apache.org/jira/browse/CASSANDRA-14763>
6. Apache Cassandra commit `167ebbcf4304512fa538e9cfc18da4295511d16c`, **Fail incremental repair prepare phase if it encounters sstables from un-finalized sessions**, 21 September 2018: <https://github.com/apache/cassandra/commit/167ebbcf4304512fa538e9cfc18da4295511d16c>
7. Apache JIRA, **CASSANDRA-9143 — Fix consistency of incrementally repaired data across replicas**: <https://issues.apache.org/jira/browse/CASSANDRA-9143>

### Internal comparison anchors

8. [`Case 48 — Apache Cassandra Incremental Repair State`](../cases/48-apache-cassandra-incremental-repair-state.md).
9. [`Case 61 — Apache HDFS Observer State-ID Read Freshness`](../cases/61-apache-hdfs-observer-stateid-read-freshness.md), for a functional comparison around state-publication ordering.
10. [`Case 141 — PostgreSQL Replication Slot WAL Retention Frontier`](../cases/141-postgresql-replication-slot-wal-retention-frontier.md), for a functional comparison around retained control metadata whose lifetime is constrained by dependent historical state.
11. [`Case 24 — Windows Azure LRC Lazy Redundancy Transition`](../cases/24-windows-azure-lrc-lazy-redundancy-transition.md), for the existing bounded handoff comparison.

---

## Result

**`bounded deepening complete`**

The evidence is strong enough to add three narrow claims to Case 48 without changing its maturity:

```text
promise observed by coordinator
    != local promise state necessarily restart-safe

session old/completed enough for normal cleanup
    != safe to delete while SSTables still reference it

newer repair succeeds
    != universal high-water mark if excluded older pending data can later return unrepaired
```

These are source-grounded limits on when maintenance-history state becomes authoritative and when it may safely be forgotten. They do not turn Cassandra repair sessions into a general distributed-transaction theory, and they do not establish user-payload loss for every violated invariant.