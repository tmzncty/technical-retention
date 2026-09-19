# Case 48 evidence deepening — Cassandra repair-administration visibility, cleanup authority, and zombie-session residue (2018–2024)

## Status

**Bounded deepening complete.**

This note deepens [`../cases/48-apache-cassandra-incremental-repair-state.md`](../cases/48-apache-cassandra-incremental-repair-state.md) at one narrow boundary:

> once incremental repair has its own retained session and pending-SSTable state, how can an operator tell whether that maintenance state still exists, distinguish completed session state from unreleased pending data, and force the promotion/demotion cleanup that retires a completed repair obligation?

The principal historical slice is **CASSANDRA-14939**, opened 17 December 2018 and resolved for Cassandra 4.0 on 25 August 2020. A later **CASSANDRA-19399** field defect report from Cassandra 4.1.3 is used only as a counterexample showing that a session record being `FAILED` or absent from the default active-session listing does not by itself prove that every SSTable-side pending relation has been retired.

This is not a general history of Cassandra repair, `nodetool`, Reaper, or Cassandra 4.x operations.

---

## Research question

Case 48 already grounds this repair-state sequence:

```text
unrepaired
    -> pending repair
    -> finalized repaired
       or failed -> unrepaired
```

It also grounds earlier fixes requiring:

- local durability before a successful finalize promise is published;
- repair-session records to outlive SSTables that still reference them;
- newer repair sessions not to silently pass unresolved older pending data.

The next bounded question is different:

> **What retained evidence must be observable, and what cleanup authority must exist, when the protocol-level repair session has completed or failed but SSTables are still physically classified as pending repair?**

---

## Source set

### Primary Apache issue records

1. Apache Cassandra **CASSANDRA-14939 — “fix some operational holes in incremental repair”**
   - created: 17 December 2018;
   - resolved: 25 August 2020;
   - fixed for Cassandra 4.0;
   - source-control link: commit `c34317526fc6dbe559beb36cf44e24278656bdf2`.
   - <https://issues.apache.org/jira/browse/CASSANDRA-14939>

2. Apache Cassandra **CASSANDRA-19399 — “Zombie repair session blocks further incremental repairs due to SSTable lock”**
   - created: 14 February 2024;
   - user report against Cassandra 4.1.3;
   - still open/unresolved in the inspected issue record;
   - <https://issues.apache.org/jira/browse/CASSANDRA-19399>

### Primary Apache source / documentation

3. Apache Cassandra commit **`c34317526fc6dbe559beb36cf44e24278656bdf2`**, committed 25 August 2020, “Add addition incremental repair visibility to nodetool repair_admin”, reviewed for CASSANDRA-14939:
   - <https://github.com/apache/cassandra/commit/c34317526fc6dbe559beb36cf44e24278656bdf2>

4. `RepairAdmin.java` at that commit:
   - <https://github.com/apache/cassandra/blob/c34317526fc6dbe559beb36cf44e24278656bdf2/src/java/org/apache/cassandra/tools/nodetool/RepairAdmin.java>

5. Cassandra 4.1 generated `nodetool repair_admin` documentation:
   - <https://cassandra.apache.org/doc/4.1/cassandra/tools/nodetool/repair_admin.html>

The 2024 Jira is a project-hosted defect report rather than a resolved implementation proof. It is therefore used only for the exact observed failure boundary stated in the issue, not as a frequency estimate or a universal property of all Cassandra 4.1 deployments.

---

# Historical record

## H/P — CASSANDRA-14939 identifies observability and cleanup as missing operational state

CASSANDRA-14939 does not describe a new anti-entropy algorithm. Its own wording identifies three “operational rough spots” in incremental repair that made the mechanism harder to automate and operate at scale:

1. visibility into whether **pending repair data exists for a token range**;
2. the ability to **force promotion/demotion of data for completed sessions** rather than waiting for compaction;
3. the ability to retrieve the **most recent `repairedAt` state** for a token range.

This is direct historical evidence that the project developers treated repair-session state, pending-data residue, and repaired-history state as operationally distinct things worth exposing.

The issue was opened on 17 December 2018 and resolved on 25 August 2020 for Cassandra 4.0.

### Bounded historical claim

By the 4.0 development cycle, Apache Cassandra explicitly recognized that successful automation required more than knowing that a repair command had been issued or that a session object existed. Operators needed visibility into retained **data-side maintenance classification** and an administrative path to retire completed repair state.

---

## H/P — the 2020 commit adds separate views for session state, pending data, and repaired history

Commit `c34317526f...` adds two new `repair_admin` summaries while retaining the existing session list/cancel operations:

```text
repair_admin list
repair_admin summarize-pending
repair_admin summarize-repaired
repair_admin cleanup
repair_admin cancel
```

The command split itself is evidence against collapsing these into one “repair status” bit.

### `list`

`RepairAdmin.ListCmd` prints session-level fields including:

- session id;
- state;
- last activity;
- coordinator;
- participants.

### `summarize-pending`

`RepairAdmin.SummarizePendingCmd` asks the repair service for pending statistics and reports per keyspace/table:

- total data marked pending repair;
- and, in verbose mode, separate `pending`, `finalized`, and `failed` quantities.

The command can also be restricted by token range and schema arguments.

### `summarize-repaired`

`RepairAdmin.SummarizeRepairedCmd` reports repaired-history information for the selected scope. The implementation prints `min_repaired` and `max_repaired`, and verbose output can include finer sections.

This matters because operator-visible repaired history is not reduced to one cluster-global timestamp.

---

## H/P — pending classification is read from live SSTables, not merely inferred from an active-session list

The same commit adds `ColumnFamilyStore.getPendingRepairStats()`.

That implementation iterates live SSTables and reads each SSTable's `pendingRepair` session identifier. SSTables with no pending-repair id are skipped; SSTables that carry one are grouped by session and accumulated into pending statistics.

The narrow historical point is important:

> **pending repair is observable as a relation embodied on SSTables, not only as a row in a session-status display.**

This does not mean every internal repair state is stored in the SSTable itself. It means this particular operator-visible pending-data summary is grounded in SSTable-side pending-repair metadata.

---

## H/P — the 2020 tests distinguish pending, finalized, and failed session affiliations

The commit's unit-test additions exercise a sequence in which SSTables are first marked pending under repair-session IDs, then one session becomes `FAILED` and another `FINALIZED`.

The expected statistics change from:

```text
pending = all marked SSTables
failed = 0
finalized = 0
```

to a distribution in which failed-session SSTables and finalized-session SSTables remain separately countable until their pending affiliations are removed.

The test then mutates those SSTables out of the pending sets and expects the total pending-session set to become empty.

That is direct implementation evidence for a distinction between:

```text
session reaches terminal state
    !=
all SSTables have already left pending-repair classification
```

---

## H/P — `cleanup` is an explicit transition from terminal session to released data state

The 2020 `repair_admin cleanup` command is described as cleaning up pending data from completed sessions. The documentation says this normally happens automatically, but the command exists when it needs to be expedited.

The source routes cleanup through `cleanupPending(...)` and reports, per table, successful and unsuccessful session cleanups.

The lower-level commit adds `releaseRepairData(...)`. For pending-repair managers, cleanup obtains the final repair outcome and constructs a `RepairFinishedCompactionTask` for SSTables belonging to the terminal session. The cleanup result distinguishes sessions whose data were successfully released from those that could not be released.

Thus terminal session state is not itself the last state transition. A data-side release operation still has to materialize the terminal outcome.

---

## H/P — `--force` changes cleanup admission around conflicting compactions, not the historical outcome of the repair

The command documentation states that `cleanup --force` can cancel compactions that are preventing promotion.

The 2020 source implements the force path by running repair-data release while compactions touching the relevant pending SSTables are disabled/cancelled.

The safe historical statement is therefore:

> `--force` strengthens the operator's ability to obtain the resources needed for cleanup.

It is **not** evidence that an unresolved or failed repair is magically converted into a successful repair. Promotion versus demotion still derives from repair-session outcome.

---

## H/P — Cassandra 4.1 continues to expose the same distinct administrative surfaces

The inspected Cassandra 4.1 `repair_admin` documentation retains:

- `list`, with `--all` to include completed and failed sessions;
- `cancel` for an incremental repair session;
- `cleanup` for pending data from completed sessions;
- `summarize-pending`, reporting the amount of data marked pending repair for a token range;
- `summarize-repaired`, returning repaired-history information for a token range.

The documentation explicitly says cleanup normally happens automatically but can be expedited, and that `--force` may be used when compactions prevent promotion.

This is a continuity witness for the operator-visible state decomposition. It is not proof that every later repair-state defect was eliminated.

---

## H/P — CASSANDRA-19399 supplies a later counterexample: `FAILED` session state can coexist with SSTable-side residue that blocks a new repair

CASSANDRA-19399 is a 14 February 2024 user report against Cassandra 4.1.3. The reporter observed future incremental repairs failing because intersecting SSTables still belonged to an older incremental-repair session.

The issue records three especially useful observations:

1. ordinary `nodetool repair_admin list` reported **no active sessions**;
2. `nodetool repair_admin list --all` showed the offending older session as **`FAILED`**;
3. cancelling the failed session did not clear the condition; the reporter states that affected-node restarts cleared the observed blockage.

The issue remains open/unresolved in the inspected ASF record. It must therefore be treated as a bounded defect report, not a settled mechanism description or an estimate of how often Cassandra 4.1 behaves this way.

Even with that limitation, it is a strong counterexample to two invalid equivalences:

```text
no active session listed
    !=
no SSTable-side pending repair residue

session state == FAILED
    !=
pending data affiliation necessarily retired
```

---

# Engineering reconstruction

## E — repair has at least three separately current relations

The 2020 administrative interface makes a useful decomposition explicit:

```text
A. repair-session relation
   session id / state / coordinator / participants

B. data-to-session relation
   SSTables still marked pending for a session

C. repaired-history relation
   repairedAt state that affects future maintenance eligibility
```

A fourth relation is the cleanup transition that reconciles B with the terminal outcome of A.

None of these should be substituted for another.

---

## E — terminal protocol state is not identical to materialized storage classification

A repair session can become finalized or failed before every pending SSTable has been promoted or demoted out of its pending bucket.

The safe reconstruction is:

```text
repair outcome determined
    -> terminal session state retained
    -> SSTable pending affiliation may still exist
    -> cleanup/compaction materializes promotion or demotion
    -> pending affiliation retired
```

This is a handoff, not one atomic conceptual instant.

---

## E — observability is part of maintainability but not proof of closure

`summarize-pending` makes a hidden maintenance relation observable. `summarize-repaired` makes maintenance-history coverage more observable. `cleanup` gives an explicit administrative action.

But:

```text
observable pending state
    !=
maintenance complete

operator can request cleanup
    !=
cleanup succeeded

cleanup reports success
    !=
independent proof of payload correctness
```

The command output is operational evidence about Cassandra's repair-control state, not a substitute for an independent end-to-end integrity proof.

---

## E — “repair complete” can require retiring an obligation, not merely producing a result

Case 48 originally emphasizes retaining maintenance history so future incremental repair can avoid already-repaired data. The 2020 slice exposes the inverse obligation: when a repair session ends, data must also cease being classified as **pending that session**.

So a repair lifecycle contains both retention and retirement work:

```text
retain pending relation while outcome unresolved
    -> determine terminal outcome
    -> retain enough outcome state to drive release
    -> promote or demote data
    -> retire pending relation
```

Forgetting too early can misclassify unfinished work; retaining too long can block later maintenance.

---

## E — stale maintenance state can become a liveness/resource constraint even when user payload still exists

CASSANDRA-19399 reports a later repair being rejected because SSTables remained associated with an older session.

The bounded engineering lesson is:

```text
payload survives
    + stale/unreleased maintenance classification survives
    -> future maintenance may be inadmissible
```

That is different from data loss. It is a failure of **maintenance-state retirement/currentness** that can reduce the system's ability to perform future repair.

---

## E — session listing and pending-data enumeration answer different questions

The 2024 report makes this distinction especially sharp:

```text
“is there an active repair session?”
    !=
“does any live SSTable still carry a pending-repair relation?”
```

This is why the 2020 addition of `summarize-pending` is conceptually important even though it did not alter the anti-entropy algorithm itself.

---

# Functional comparisons

## A — Case 41 tombstones: negative-state retirement versus repair-state retirement

Case 41 retains tombstones because forgetting deletion evidence too early can let stale positive data become current again.

Case 48 retains pending/session state because forgetting or failing to retire the right maintenance relation can misclassify repair progress or block later repair.

The functional analogy is only:

```text
retained control evidence has a safe lifetime
```

The underlying states, failure models, and algorithms are different.

---

## A — Case 145 JFFS2: completion state versus reuse admission

Case 145 separates erase completion from later qualification/CLEANMARKER/reuse admission. This Cassandra slice similarly separates terminal repair outcome from pending-data release.

Functional shape:

```text
operation outcome established
    !=
downstream state transition fully materialized
```

There is no historical or implementation genealogy between JFFS2 erase management and Cassandra repair.

---

## A — Case 141 / other retained-control-state lifetime cases

The general comparison is to any system in which an object references a control record and the control record must not disappear before dependent state is reconciled.

Case 48's earlier CASSANDRA-13758 already established this referential-lifetime rule for repair sessions. CASSANDRA-14939 adds the operator-facing side: administrators need to inspect and release the dependent pending state rather than treating session completion as enough.

---

# Philosophical interpretation

The technical fact that creates the conceptual problem is precise:

> a system can finish the logical decision about a maintenance operation while still carrying materialized classifications that say some data belongs to that maintenance episode.

The useful concept here is not “memory” in the abstract but **retained obligation**.

Pending-repair state is not valuable because the system wants a historical archive of the repair. It is valuable while the repair outcome is unresolved or has not yet been materialized into repaired/unrepaired classification. After that, the same surviving relation can become an obstacle.

This yields a bounded retention/forgetting relation:

```text
retain while needed to preserve maintenance correctness
    -> expose enough state to judge what remains
    -> retire when terminal outcome has been safely materialized
```

The interpretation stops there. It does not establish a human-memory analogy, a universal theory of institutional memory, or a claim that all stale metadata are philosophically equivalent.

---

# Explicit non-claims

This evidence does **not** claim that:

1. Cassandra invented operator-visible repair state;
2. CASSANDRA-14939 invented incremental repair;
3. `repair_admin` output is an independent integrity audit;
4. a `FINALIZED` session means every replica is forever correct;
5. a `FAILED` session means every SSTable has already been demoted;
6. `cleanup --force` converts a failed repair into a successful repair;
7. cancelling compactions is itself payload repair;
8. `summarize-repaired` is a universal cluster-wide high-water mark;
9. `repairedAt` is an application version timestamp;
10. pending-repair metadata and payload currentness are the same state;
11. terminal session state and SSTable classification change atomically in one indivisible step;
12. CASSANDRA-19399 affects every Cassandra 4.1 deployment;
13. the CASSANDRA-19399 reporter's restart workaround proves the exact root cause;
14. an unresolved Jira report is equivalent to a merged fix;
15. “no active session” means there are no retained repair-control obligations;
16. successful cleanup proves absence of later disk corruption;
17. the 2020 operator tooling eliminates all later zombie/stuck-session failure modes;
18. Reaper caused CASSANDRA-19399—the issue only says this was a possibility considered by the reporter;
19. this slice supplies a general Cassandra operations guide;
20. similar cleanup/retirement shapes in other systems establish genealogy.

---

# Claim ledger

| ID | Type | Claim | Evidence strength |
|---|---|---|---|
| `H-48.30` | Historical record | CASSANDRA-14939 explicitly requested visibility into pending repair data, forced promotion/demotion for completed sessions, and repairedAt visibility. | High — ASF Jira |
| `H-48.31` | Historical record | Commit `c34317526f...` added `summarize-pending`, `summarize-repaired`, and cleanup support to `repair_admin`. | High — Apache source commit |
| `H-48.32` | Historical record | Pending statistics are built from live SSTables carrying `pendingRepair` session IDs. | High — Apache source |
| `H-48.33` | Historical record | Tests distinguish still-pending SSTables attached to active, failed, and finalized sessions before those affiliations are removed. | High — Apache tests in the commit |
| `H-48.34` | Historical record | Cassandra 4.1 documentation retains separate list/cancel/cleanup/pending-summary/repaired-summary operations. | High — Apache versioned docs |
| `H-48.35` | Historical record | CASSANDRA-19399 reports a 4.1.3 case where no active session was listed but a failed older session still had SSTable-side effects blocking a later incremental repair. | Medium-high — ASF unresolved user defect report |
| `E-48.36` | Engineering reconstruction | Repair-session state, SSTable pending affiliation, repaired-history state, and cleanup completion are distinct relations. | Strongly grounded in source interface and tests |
| `E-48.37` | Engineering reconstruction | Terminal repair outcome can precede complete materialization of promotion/demotion. | Strongly grounded in cleanup design |
| `E-48.38` | Engineering reconstruction | Retained maintenance state can become a future-maintenance liveness/admission problem if not retired. | Grounded in CASSANDRA-19399; bounded to reported behavior |
| `A-48.39` | Functional analogy | Case 48 and Case 145 both separate operation outcome from later admission/release state. | Functional only; no genealogy |

---

# Prior-art / novelty boundary

This slice makes no broad novelty claim for repair observability, maintenance cleanup, or administrative state machines.

The historically defensible claim is narrower:

> **Within Cassandra's 4.0 incremental-repair redesign, CASSANDRA-14939 explicitly promoted pending-data residue and repaired-history coverage into operator-visible state and added an administrative cleanup path for completed sessions.**

The later CASSANDRA-19399 report is important precisely because it prevents a triumphalist reading of that change: exposing and administering a retained relation does not prove that every path retires it correctly.

Broader histories of distributed repair administration, anti-entropy tooling, Cassandra Reaper, and operator observability belong primarily in `computing-archaeology` rather than here.

---

# Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `CASSANDRA-14939`, `repair_admin`, incremental-repair pending state, and the relevant command vocabulary found no dedicated overlapping packet during this slice.

Accordingly this file retains only the retention-specific seam:

```text
repair session outcome
    -> retained terminal state
    -> pending SSTable affiliation
    -> operator visibility / cleanup authority
    -> promotion or demotion materialized
    -> pending obligation retired
```

A broader Cassandra 4.x repair-tooling history, Reaper history, operational incident survey, and command-interface genealogy should be built in `computing-archaeology` if needed.

---

# Remaining evidence debt

This bounded slice closes the specific Case-48 debt around **post-4.0 operator visibility and manual cleanup of pending repair state**, but leaves several questions open:

- the exact root cause and eventual resolution, if any, of CASSANDRA-19399;
- CASSANDRA-17172 and other stuck-session reports as a separate fault taxonomy rather than anecdotal accumulation;
- crash/fault-injection validation around cleanup and pending-state retirement;
- version-by-version behavior of cleanup after 4.1;
- interaction with modern Cassandra auto-repair scheduling;
- whether later releases provide stronger invariants or independent reconciliation of orphaned pending SSTable affiliations;
- broader anti-entropy administration/tooling genealogy.

These are follow-on slices, not assumptions licensed by the present evidence.
