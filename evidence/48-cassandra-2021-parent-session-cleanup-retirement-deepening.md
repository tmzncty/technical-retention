# Evidence 48C — Cassandra 2021 parent-repair-session cleanup and retirement boundary

- **Case:** [`cases/48-apache-cassandra-incremental-repair-state.md`](../cases/48-apache-cassandra-incremental-repair-state.md)
- **Status:** bounded deepening complete
- **Bounded slice:** Apache Cassandra CASSANDRA-16446 and its 24 February 2021 source/dtest changes, with CASSANDRA-17172 used only as a later unresolved counterexample to equating a visible session state with active repair work.
- **Question:** after repair has reached its main success path, what retained coordinator/participant control state still has to be retired, and what happens if that cleanup does not complete?

This file does **not** reopen the whole Cassandra incremental-repair history. Case 48 already covers `repairedAt`, pending repair, session durability/reference lifetime, `repair_admin`, and the later CASSANDRA-19399 SSTable-side zombie-residue report. The narrower purpose here is to isolate a different retained object: the in-memory `ActiveRepairService.parentRepairSessions` registry used during a repair.

---

## Why this slice matters

Case 48 already established that maintenance correctness can fail when required state is forgotten too early. CASSANDRA-16446 exposes the opposite direction:

```text
state needed during repair
    -> repair completes
    -> state is no longer supposed to remain indefinitely
    -> failure to retire it becomes operational debt
```

The relevant state is not user payload and is not the `pendingRepair` relation stored on SSTables. It is a participant-local parent repair session object retained in `ActiveRepairService`.

That distinction matters because a system can be wrong in two opposite ways:

```text
forget required maintenance state too early
    -> correctness / coordination risk

retain obsolete maintenance state too long
    -> leak / pause / admission / liveness risk
```

CASSANDRA-16446 is unusually useful because Apache's issue, implementation, message handler, and dtests all expose the retirement boundary directly.

---

# Source set

## Primary Apache sources

1. Apache Cassandra JIRA, **CASSANDRA-16446 — Parent repair sessions leak may lead to node long pauses**, created 15 February 2021 and resolved 24 February 2021: <https://issues.apache.org/jira/browse/CASSANDRA-16446>
2. Apache Cassandra commit `23512cf3da5e8206d8797841f2238cdd86c13d96`, **Prevent parent repair sessions leak**, 24 February 2021: <https://github.com/apache/cassandra/commit/23512cf3da5e8206d8797841f2238cdd86c13d96>
3. `ActiveRepairService.java` at that commit: <https://github.com/apache/cassandra/blob/23512cf3da5e8206d8797841f2238cdd86c13d96/src/java/org/apache/cassandra/service/ActiveRepairService.java>
4. `RepairMessageVerbHandler.java` at that commit: <https://github.com/apache/cassandra/blob/23512cf3da5e8206d8797841f2238cdd86c13d96/src/java/org/apache/cassandra/repair/RepairMessageVerbHandler.java>
5. `CleanupMessage.java` at that commit: <https://github.com/apache/cassandra/blob/23512cf3da5e8206d8797841f2238cdd86c13d96/src/java/org/apache/cassandra/repair/messages/CleanupMessage.java>
6. Apache `cassandra-dtest` commit `c89dea0e8c38ed35ed40d59c975a07585584a637`, **Add tests for parent repair session cleanup**, 24 February 2021: <https://github.com/apache/cassandra-dtest/commit/c89dea0e8c38ed35ed40d59c975a07585584a637>
7. Apache Cassandra JIRA, **CASSANDRA-17172 — incremental repairs get stuck often**, created 27 November 2021; open/unresolved in the inspected record: <https://issues.apache.org/jira/browse/CASSANDRA-17172>

## Existing Case-48 controls

8. [`Evidence 48A`](48-cassandra-2017-2018-repair-session-durability-referential-integrity-deepening.md), for durable session-state ordering and SSTable/session reference lifetime.
9. [`Evidence 48B`](48-cassandra-2018-2024-repair-admin-zombie-session-deepening.md), for `repair_admin`, pending-SSTable visibility/cleanup, and CASSANDRA-19399.

---

# Historical record

## H — CASSANDRA-16446 identifies `parentRepairSessions` as a leakable retained map

The Jira describes `ActiveRepairService` as keeping a map called `parentRepairSessions`. The reported problem is not that the map fails to exist. It is that completed repair sessions can remain in it, allowing the map to grow.

Apache frames the consequence operationally: when enough leaked sessions accumulate, restart-time cleanup can pause nodes for a long time.

This is direct actor language for a **retirement failure** rather than an absence-of-retention failure.

The issue was created on **15 February 2021** and resolved as fixed on **24 February 2021**. Its source-control links point to the Cassandra implementation commit and the matching dtest commit used below.

---

## H — the 2021 fix wires cleanup into successful repair completion

Commit `23512cf3da5e8206d8797841f2238cdd86c13d96`, dated **24 February 2021**, changes the repair completion path so the set of endpoints that successfully prepared for the parent repair is retained and passed to cleanup.

The resulting success path calls:

```text
ActiveRepairService.cleanUp(parentSession, preparedEndpoints)
```

for ordinary repair completion and for preview-repair completion.

The historical point must be stated narrowly:

> **the 2021 patch makes successful completion actively request retirement of parent-repair-session objects on the prepared participants.**

It does not create the entire cleanup protocol from nothing.

---

## H — `CleanupMessage` predates CASSANDRA-16446

At the 2021 commit, `CleanupMessage.java` describes itself as a message to clean up repair resources on replica nodes and carries:

```text
@since 2.1.6
```

The message contains the `parentRepairSession` UUID.

Therefore:

```text
2021 CASSANDRA-16446 fix
    != invention of CleanupMessage
```

The defensible claim is that the 2021 change **reuses an existing cleanup message to close a completion-path retirement hole**.

---

## H — the receiving CLEANUP handler removes the parent repair session

At the same commit, `RepairMessageVerbHandler` handles `CLEANUP_MSG` by calling:

```text
ActiveRepairService.instance.removeParentRepairSession(cleanup.parentRepairSession)
```

and then replying to the sender.

This is important because the message is not merely advisory telemetry. Its direct handler action is removal of the retained parent-session object.

`removeParentRepairSession(...)` removes the UUID from `parentRepairSessions`; if a matching session exists, it also clears snapshots associated with that parent-session ID before returning the removed object.

So the bounded retirement path is:

```text
CLEANUP_MSG received
    -> remove parent session from participant cache/map
    -> clear matching repair snapshots if present
    -> reply
```

This file does not claim that this one message retires every other piece of repair metadata in Cassandra.

---

## H — the cleanup sender intentionally does not convert cleanup failure into repair failure

`ActiveRepairService.cleanUp(...)` documents that it sends `Verb.CLEANUP_MSG` to the given endpoints and that the method **does not throw an exception in case of a messaging failure**.

For each endpoint considered alive by the failure detector, it sends a cleanup message with a callback. On callback failure, the log says the uncleaned sessions will be removed on a node restart and that the condition should not be a problem unless thousands of such messages occur.

A send exception is likewise caught and logged rather than propagated as repair failure.

That establishes a strong ordering boundary:

```text
main repair success
    -> cleanup requested

cleanup message failure
    != retroactive repair failure
```

The retirement of this cache/control object is therefore deliberately weaker than the success criterion for the main repair operation.

---

## H — restart/failure handling is a fallback retirement path, not proof of bounded lifetime

`ActiveRepairService` is registered for endpoint/failure events when a parent repair session is first registered.

Its `onRestart(...)` path invokes `convict(...)`. `convict(...)` identifies parent repair sessions whose coordinator is the affected endpoint and passes them to `abort(...)`; `abort(...)` removes matching parent sessions through `removeParentRepairSession(...)`.

The source comment also says failed parent-session markers are kept long enough to ensure disagreement about coordinator failure fails the overall repair rather than silently accepting conflicting outcome state.

For this slice, the important distinction is:

```text
restart/failure event can trigger retirement
    != every stale session is guaranteed to retire promptly without the normal cleanup path
```

CASSANDRA-16446 exists precisely because relying on later cleanup allowed enough retained objects to accumulate to produce a restart-time cost.

---

## H — the patch adds direct observability of the retained-map population

The same implementation adds:

```text
parentRepairSessionsCount()
    -> parentRepairSessions.size()
```

through the repair service MBean.

The dtest patch uses this method explicitly. It defines an assertion helper that reads `parentRepairSessionsCount` over JMX and reports that a nonzero count may indicate leaking `ParentRepairSession` objects.

The tests then run:

- incremental repair on a three-node cluster;
- preview repair on a three-node cluster;
- a full/sequential repair path;

and assert that the cached parent repair session count is **0** afterward.

Thus the implementation change is accompanied by a concrete postcondition in Apache's test suite:

```text
repair path completes
    -> participant ParentRepairSession cache population returns to zero
```

That is stronger evidence than treating the issue description alone as intended behavior.

---

## H — the dtests do not prove all message-loss and crash interleavings

The dtest commit verifies cleanup after normal repair paths. The inspected patch does not itself constitute exhaustive fault injection for:

- dropped `CLEANUP_MSG`;
- participant crash between main repair completion and cleanup receipt;
- repeated cleanup callback failure;
- process termination while snapshots are being cleared;
- all later 4.x repair implementations.

Therefore the dtests establish a normal-path retirement postcondition, not universal proof that obsolete parent-session state can never survive.

---

## H — CASSANDRA-17172 is a later unresolved counterexample to equating session label with active work

CASSANDRA-17172, filed **27 November 2021** against Cassandra 4.0.1, reports intermittent incremental repairs remaining in state `REPAIRING` while `nodetool netstats` shows no streaming activity. The reporter quotes `LocalSessions` repeatedly learning a `REPAIRING` outcome and doing nothing because that state is not actionable; manual `repair_admin cancel` followed by rerunning the same repair usually succeeds.

The inspected Jira remains **open / unresolved**.

This report is useful only for one bounded point:

```text
visible session state == REPAIRING
    != positive evidence that data movement is currently progressing
```

This file does **not** claim CASSANDRA-17172 has the same root cause as the CASSANDRA-16446 `parentRepairSessions` leak.

---

# Engineering reconstruction

## E — Case 48 now needs at least three separate retained repair-state layers

The prior evidence already separated terminal session outcome from SSTable-side `pendingRepair` affiliation. CASSANDRA-16446 adds another distinct object:

```text
A. consistent-repair / LocalSession outcome state

B. SSTable -> pendingRepair affiliation and repairedAt classification

C. ActiveRepairService.parentRepairSessions participant registry/cache
```

These layers have different persistence and retirement semantics.

In particular:

```text
terminal repair outcome
    != SSTable classification fully materialized
    != parentRepairSessions cache entry retired
```

CASSANDRA-19399 primarily exposes layer B residue. CASSANDRA-16446 exposes layer C residue. Treating both as one generic “zombie session” would erase the mechanism boundary.

---

## E — completion authority and cleanup completion are separate events

The 2021 success path can be reconstructed as:

```text
repair work reaches successful completion
    -> completion callback / preview completion
    -> cleanUp(parentSession, preparedEndpoints)
    -> CLEANUP_MSG sent
    -> participant handler receives message
    -> removeParentRepairSession(parentSession)
    -> local cache/snapshot retirement
```

There are at least two boundaries here:

```text
repair completion
    != cleanup request delivery

cleanup request delivery
    != cleanup side effects completed
```

The code intentionally tolerates cleanup-message failure without throwing from `cleanUp(...)`, so those distinctions are not merely theoretical.

---

## E — cleanup failure can create bounded obsolete state without invalidating the successful repair result

Because messaging failure is caught/logged, the system can preserve:

```text
successful main repair outcome
    + obsolete parent-session cache residue
```

That combination matters. It prevents a misleading binary model in which every surviving repair-session object means the repair itself is unresolved.

Some retained state can be **post-success residue** rather than evidence that the primary maintenance action failed.

---

## E — restart is a garbage-collection opportunity, not equivalent to normal retirement

The implementation's failure log treats restart as a later route for cleaning unretired sessions. CASSANDRA-16446 simultaneously warns that a sufficiently large backlog can make restart cleanup pause-prone.

Therefore:

```text
fallback cleanup exists
    != stale-state lifetime is harmless

restart eventually removes state
    != accumulating that state has zero operational cost
```

A fallback can preserve eventual hygiene while still allowing an unacceptable transient resource-retention regime.

---

## E — retained maintenance state has both a minimum and a maximum useful lifetime

Earlier Case-48 evidence showed why session state must not be deleted while SSTables still refer to it.

This slice shows the opposite rule for a different object: once the parent-session cache entry no longer serves ongoing repair coordination, retaining it indefinitely is not conservative correctness—it is a leak.

So the engineering problem is not “retain as much state as possible.” It is:

```text
retain while authority / references still require the state
    -> retire after the obligation has ended
    -> retain enough fallback information to handle failure
    -> avoid unbounded obsolete-state accumulation
```

This is a lifetime discipline, not a generic preference for more or less retention.

---

## E — observability is part of retirement assurance

`parentRepairSessionsCount()` does not perform cleanup. It exposes whether participant caches actually return toward the expected post-repair state.

This separates:

```text
retirement mechanism
    != retirement observability
```

The dtest deliberately composes them: run a repair, then observe that no cached parent sessions remain.

---

## E — `REPAIRING` is an authority/state label, not a progress meter

The CASSANDRA-17172 report supplies a useful counterexample to treating control state as proof of ongoing work. A session can be reported as `REPAIRING` while the reporter observes no streaming and the local status-learning path finds no actionable transition.

That does not prove the repair can never make progress. It proves only that:

```text
state machine label
    != measured maintenance throughput
```

This boundary is important for operator tooling and later auto-repair systems that may need independent liveness/progress evidence.

---

# Functional comparisons

## A — CASSANDRA-16446 versus CASSANDRA-19399 inside Case 48

The two defect reports should not be collapsed:

```text
CASSANDRA-16446
    obsolete participant parent-session objects remain in memory
    -> accumulation / restart-pause risk

CASSANDRA-19399
    failed-session-associated SSTable pending state remains
    -> later incremental-repair admission/lock failure
```

Both are retirement problems, but they concern different retained carriers and different consequences.

The common functional form is only:

```text
maintenance episode ends or becomes terminal
    -> some dependent control relation survives longer than intended
    -> future operation is degraded
```

No shared root cause is claimed.

---

## A — Case 145 JFFS2 cleanup/admission boundary

Case 145 separates physical erase completion, qualification/CLEANMARKER state, and later block reuse admission. This Cassandra slice similarly separates repair completion from retirement of auxiliary control state.

The analogy is only:

```text
main operation outcome
    != all control-state cleanup completed
```

JFFS2 erase management and Cassandra distributed repair have no historical or implementation genealogy.

---

## A — Case 125 ext4 orphan cleanup

Case 125's orphan-list/recovery mechanism and this Cassandra cleanup path both show that a primary operation can leave auxiliary state whose later cleanup has its own correctness/lifetime rules.

Again the comparison is structural only. ext4 crash recovery, journal semantics, and Cassandra repair messaging are different systems.

---

# Philosophical interpretation

The technical record supports a narrow proposition:

> **Maintenance memory is useful only while its retained relation still carries valid authority or obligation. After that boundary, the same persistence can change from protection into residue.**

This is stronger than saying “systems need memory.” Case 48 now supplies both directions:

```text
premature forgetting
    -> maintenance relation loses required evidence

late forgetting / failed retirement
    -> obsolete maintenance relation becomes operational residue
```

The concept that follows is **timely retirement of technical memory**, not a moral or psychological theory of forgetting.

The historical sources do not use this philosophical language; it is project interpretation of the engineering lifetime constraints.

---

# Explicit non-claims

This evidence does **not** claim that:

1. Cassandra invented distributed cleanup messages;
2. CASSANDRA-16446 invented `CleanupMessage`;
3. every `ParentRepairSession` object is durable on disk;
4. `parentRepairSessions` is the same data structure as the persistent consistent-repair local-session table;
5. `parentRepairSessions` is the same state as SSTable `pendingRepair` metadata;
6. a surviving parent-session cache entry proves the user payload is corrupt;
7. a surviving parent-session cache entry proves the repair failed;
8. successful `CLEANUP_MSG` delivery proves every repair-related datum has been retired;
9. cleanup callback failure rolls back an already successful repair;
10. restart is the only fallback cleanup path in every Cassandra release;
11. restart cleanup has zero cost;
12. one leaked parent session necessarily creates a visible pause;
13. the Jira's warning about large accumulated maps gives a universal numeric threshold;
14. the normal-path dtests exhaustively test message loss and crash timing;
15. `parentRepairSessionsCount() == 0` proves replica payload equality;
16. `REPAIRING` in CASSANDRA-17172 has the same root cause as CASSANDRA-16446;
17. CASSANDRA-17172 affects every Cassandra 4.0.1 deployment;
18. an unresolved Jira report is equivalent to a merged fix;
19. CASSANDRA-19399 and CASSANDRA-16446 are one defect merely because both can be described colloquially as zombie state;
20. functional similarities to filesystem cleanup establish genealogy.

---

# Claim ledger

| ID | Type | Claim | Evidence strength |
|---|---|---|---|
| `H-48.40` | Historical record | CASSANDRA-16446 reports that `ActiveRepairService.parentRepairSessions` could leak and that a large retained map could make restart cleanup pause-prone. | High — ASF Jira |
| `H-48.41` | Historical record | Commit `23512cf3...` wires successful repair/preview completion to `ActiveRepairService.cleanUp(parentSession, preparedEndpoints)`. | High — Apache source commit |
| `H-48.42` | Historical record | `CleanupMessage` at the 2021 commit is documented `@since 2.1.6`; the 2021 patch therefore reuses rather than invents the cleanup message. | High — Apache source |
| `H-48.43` | Historical record | `CLEANUP_MSG` handling removes the matching parent repair session, while `removeParentRepairSession` also clears matching repair snapshots if present. | High — Apache source |
| `H-48.44` | Historical record | `cleanUp(...)` explicitly does not throw on messaging failure and logs restart as a later cleanup opportunity for uncleaned sessions. | High — Apache source |
| `H-48.45` | Historical record | The patch exposes `parentRepairSessionsCount()` and dtests assert a zero post-repair cache count for incremental, preview, and full/sequential repair paths. | High — Apache source + Apache dtests |
| `H-48.46` | Historical record | CASSANDRA-17172 reports Cassandra 4.0.1 sessions remaining `REPAIRING` while no streaming is observed; the issue is open/unresolved in the inspected record. | Medium-high — ASF unresolved defect report |
| `E-48.47` | Engineering reconstruction | Main repair outcome, SSTable pending-repair affiliation, and participant parent-session cache retirement are distinct state relations. | Strongly grounded in source separation |
| `E-48.48` | Engineering reconstruction | Repair success can precede successful cleanup-message delivery because cleanup messaging failure does not throw from the completion path. | Strongly grounded in source |
| `E-48.49` | Engineering reconstruction | Restart fallback does not make obsolete-state lifetime free: accumulated residue can itself impose later cleanup cost. | Strongly grounded in Jira + source logging |
| `A-48.50` | Functional analogy | Case 48 and filesystem cleanup cases share only the form `main outcome != all auxiliary cleanup complete`. | Functional only; no genealogy |

---

# Prior-art / novelty boundary

This slice makes no claim that Cassandra invented cleanup protocols, distributed garbage collection, or resource-retirement messages.

The historically bounded claim is narrower:

> **Within Cassandra's repair implementation, CASSANDRA-16446 identifies a concrete 2021 completion-path leak in participant `ParentRepairSession` retirement and fixes it by invoking an already-existing `CleanupMessage` mechanism after successful repair paths, with MBean/dtest observability of the resulting cache population.**

The `@since 2.1.6` annotation is specifically retained as an anti-novelty guard: the message protocol existed earlier than the 2021 bug fix.

Broader histories of Cassandra repair resource management, distributed cleanup protocols, and the evolution of the 2.1.6 message belong in `computing-archaeology` if needed.

---

# Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `CASSANDRA-16446`, `parentRepairSessions`, and Cassandra incremental repair found no dedicated overlapping packet during this slice.

Accordingly this evidence keeps only the retention-specific seam:

```text
parent repair session needed during maintenance
    -> repair reaches completion
    -> distributed cleanup request
    -> participant cache retirement
    -> fallback cleanup if normal retirement fails
```

A fuller genealogy of Cassandra's `CleanupMessage`, repair RPCs, JMX/MBean administration, and version-by-version repair-service architecture should live in the companion technical-history repository rather than be reconstructed here.

---

# Remaining evidence debt

This slice closes the specific Case-48 debt around **CASSANDRA-16446 participant parent-session cleanup**. It also sharpens, but does not close, the broader stuck/zombie-session question.

Still open:

- the exact root cause and eventual disposition of CASSANDRA-17172;
- the exact root cause and eventual disposition of CASSANDRA-19399;
- fault-injection around lost/delayed `CLEANUP_MSG` and participant crash between repair completion and cache retirement;
- whether later 4.x/5.x repair code strengthened or replaced this cleanup path;
- interaction between parent-session cache retirement and modern auto-repair scheduling;
- broader history of `CleanupMessage` from its 2.1.6 introduction;
- whether metrics/alerts beyond the MBean count became standard operational practice.

These are follow-on slices, not conclusions licensed by the present evidence.
