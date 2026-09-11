# Case 41 deepening evidence — Cassandra 4.1 persistent hint windows and the 4.1.5 stale-window correction

## Scope

This record deepens Case 41's existing Cassandra hinted-handoff boundary with one narrow question:

> **What exactly is the lifetime of the hint-generation window when the failed replica repeatedly restarts or briefly returns, and what state must Cassandra remember so that a configured retention window does not silently restart forever?**

The bounded historical slice is:

- the Cassandra 4.1 feature integrated by ASF commit `b2ccd0f3f588a34cd68222bdacd1914478914ac9` on **22 October 2021** for **CASSANDRA-14309**;
- Apache Cassandra **4.1 GA on 13 December 2022**, where the feature shipped;
- the later **CASSANDRA-19495** correction committed on **5 April 2024** as `5fb562d7efbad7bf9c2297a62991d36da90589e9`, fixed for 4.1.5.

Case 41 remains principally a tombstone / GC-grace / resurrection case. This evidence record does **not** turn it into a general history of hinted handoff. Case 23 already grounds Amazon Dynamo's 2007 hinted-handoff design and therefore supplies an explicit prior-art boundary for the generic technique.

The project phrases `persistent hint-window admission state`, `retention-window scope`, and `maintenance-state currentness` below are **engineering reconstructions**. They are not Apache Cassandra historical vocabulary.

---

## Evidence ledger

| Source | Date / status | What it grounds | What it does not ground |
| --- | --- | --- | --- |
| Apache Cassandra commit [`b2ccd0f3...`](https://github.com/apache/cassandra/commit/b2ccd0f3f588a34cd68222bdacd1914478914ac9), CASSANDRA-14309 | committed 2021-10-22; targeted 4.1 | feature rationale, `hint_window_persistent_enabled`, earliest-hint tracking, NEWS/CHANGES wording | invention of hinted handoff; 3.x semantics |
| Apache Cassandra 4.1.0 [`StorageProxy.java`](https://github.com/apache/cassandra/blob/cassandra-4.1.0/src/java/org/apache/cassandra/service/StorageProxy.java) | released in 4.1 GA 2022-12-13 | admission rule combines endpoint downtime with oldest outstanding hint age when persistent windows are enabled | guaranteed delivery; cluster convergence |
| Apache Cassandra 4.1.0 [`HintsService.java`](https://github.com/apache/cassandra/blob/cassandra-4.1.0/src/java/org/apache/cassandra/hints/HintsService.java) | 4.1.0 implementation | earliest pending hint is derived from the first on-disk descriptor and in-memory hint buffers | application payload currentness by itself |
| Apache Cassandra 4.1 NEWS / configuration text | 4.1 | repeated node restart could previously reopen hint eligibility indefinitely and consume growing disk; persistent window defaults on | a universal safe outage duration |
| ASF issue [CASSANDRA-19495](https://issues.apache.org/jira/browse/CASSANDRA-19495) | created 2024-03-26; resolved 2024-04-05; since 4.1.0; fixed in 4.1.5 | regression where stale earliest-hint state could suppress hints on a later outage | every 4.1 deployment necessarily suffered data loss |
| Apache Cassandra commit [`5fb562d7...`](https://github.com/apache/cassandra/commit/5fb562d7efbad7bf9c2297a62991d36da90589e9) | committed 2024-04-05 | fix clears earliest-hint buffer state as hint dispatch / host excision advances | general proof that hinted handoff is exactly-once |
| Apache Cassandra 4.1 GA announcement | 2022-12-13 | release date for the bounded shipping version | feature invention date |

Primary release announcement: <https://cassandra.apache.org/_/blog/Cassandra-4.1-is-here.html>.

---

## Historical record

### H/P — pre-4.1 hint-window admission was tied to observed downtime and could be reopened by restart

The Cassandra 4.1 NEWS entry added by CASSANDRA-14309 states the failure mode directly. Before the change, the hint system used `max_hint_window_in_ms`, but the window was **not persistent across restarts**. A node that restarted could again appear to have been down for less than the configured window. If it repeatedly restarted without outstanding hint delivery completing, Cassandra could continue accepting new hints indefinitely, with correspondingly growing disk use.

This is a historical actor statement from the feature's own release note, not a project inference about every older Cassandra deployment.

The narrow historical relation is:

```text
configured max hint window
    + downtime counter that can restart
    !=
a window that necessarily bounds hint creation across repeated restart episodes
```

### H/P — CASSANDRA-14309 adds a default-on persistent-window policy

Commit `b2ccd0f3...`, committed to Apache Cassandra on **22 October 2021**, is titled **“ensure hint window is persistent across restarts of a node”** and records CASSANDRA-14309 in CHANGES for Cassandra 4.1.

The same commit adds `hint_window_persistent_enabled`, defaulting to `true`. Its configuration documentation says that when enabled Cassandra should not keep saving hints indefinitely merely because a destination keeps restarting before delivery finishes.

The commit's NEWS entry is especially useful because it states the policy in operational terms: when endpoint downtime alone has not exceeded the configured window, Cassandra additionally checks whether there is already a hint older than that window. If so, another hint is not persisted.

### H/P — the 4.1.0 implementation compares two different clocks/relations

In tag `cassandra-4.1.0`, `StorageProxy.shouldHint()` first computes whether the destination's current observed downtime exceeds `maxHintWindow`. If persistent windows are enabled and that downtime check has not already rejected hinting, it then asks `HintsService` for the earliest hint associated with the destination host ID and compares that timestamp with the same window.

So the implementation does **not** merely rename the downtime timer. It combines:

1. current endpoint-down duration; and
2. age of the oldest still-outstanding hint relation.

`HintsService.getEarliestHintForHost()` in 4.1.0 derives the oldest timestamp from both the first persisted hint descriptor and in-memory buffers. That makes the admission predicate depend on retained maintenance state, not only on current gossip liveness.

### H/P — Apache Cassandra 4.1 GA is a release boundary, not an origin boundary

The Apache Cassandra community announced general availability of 4.1 on **13 December 2022**. This record therefore uses 4.1 as the bounded shipping version for the persistent-window behavior.

The feature commit predates that release, and generic hinted handoff predates Cassandra 4.1 by far. Case 23 already grounds Amazon Dynamo's published 2007 hinted-handoff mechanism. Nothing here claims that Cassandra invented hinted handoff, bounded repair windows, or deferred replica delivery.

### H/P — CASSANDRA-19495 exposes a later currentness bug in the retained window state

ASF issue CASSANDRA-19495, filed on **26 March 2024**, reports a 4.1.5-era scenario in which a node goes down, receives replayed hints after recovery, and later goes down a second time. If enough time has elapsed since the first outage, the second outage may receive **no new hints** because the earliest-hint timestamp used by the persistent-window check was not cleared when the previous obligation had completed.

The issue marks the problem as **since 4.1.0** and lists **4.1.5** among the fix versions. The important historical point is not that all 4.1.0–4.1.4 clusters necessarily lost writes. It is that the control state introduced to keep one retention window from reopening indefinitely could itself outlive the maintenance relation it was supposed to describe.

### H/P — the 2024 fix retires stale earliest-hint state when the obligation advances

Commit `5fb562d7...`, committed **5 April 2024**, is titled **“Fix hints delivery for a node going down repeatedly.”** Among its changes it adds methods for clearing earliest-hint timestamps from buffers and invokes that clearing as hint dispatch advances; it also clears the buffer-side state when a host's hints are excised.

That patch is direct implementation evidence for the needed lifecycle rule:

```text
oldest-outstanding-hint state
    must not survive indefinitely after
its corresponding outstanding-hint relation has been discharged/retired
```

The fix should not be inflated into an exactly-once-delivery guarantee. Cassandra's own hints documentation continues to describe hints as best effort and not a substitute for anti-entropy repair.

---

## Engineering reconstruction

### E — retention-window scope is part of the mechanism

A timer is not fully specified by its numeric duration. One must also know **what event starts it, what event can reset it, and what retained state carries its age across process / liveness transitions**.

For this bounded mechanism:

```text
3 hours as a number
    !=
3 hours of one continuous gossip-down episode
    !=
3 hours from the oldest still-outstanding hint obligation
```

CASSANDRA-14309 changes the effective scope of the hint-generation window by making prior outstanding hint age participate in future admission.

### E — hint generation admission and hint delivery completion are different states

`shouldHint()` answers whether another deferred mutation should be retained for a target. It does not prove that older hints have been replayed, that the target is current, or that anti-entropy repair has converged the replica set.

Therefore:

```text
new hint rejected because window expired
    !=
old hint delivery completed
    !=
replica convergence proven
```

This preserves the existing Case 41 boundary: hints are a bounded best-effort missed-write path, while repair remains a separate convergence mechanism.

### E — bounding retention can require retaining control history

The 4.1 design is a compact witness for a recurring repository pattern: bounding the lifetime of one state class may require keeping another state class long enough to remember that the budget has already been consumed.

Here, an oldest-hint timestamp / descriptor relation participates in preventing repeated restarts from reopening the generation budget. The timestamp is not the user mutation, but it helps decide whether another mutation may be retained as a hint.

### E — retained control state has its own currentness problem

CASSANDRA-19495 supplies the counterexample. If the oldest-hint marker persists after the corresponding hints have been delivered or otherwise retired, the same protective predicate can become too strong and reject legitimate hints in a later, distinct outage.

Thus:

```text
control metadata retained long enough to enforce a bound
    !=
control metadata may be retained forever
```

Maintenance metadata needs a retirement condition of its own.

---

## Functional analogy

### A — Case 48: Cassandra incremental-repair state

Case 48 shows `repairedAt` / pending-repair metadata changing future maintenance eligibility and later needing its own currentness discipline. The persistent hint window is functionally analogous only at that level: **retained maintenance metadata changes which future maintenance work is admitted**.

The mechanisms are different. Repair classification governs which SSTable state enters incremental repair; the hint-window state governs whether a coordinator admits another deferred mutation for an unavailable replica.

### A — Case 23: Amazon Dynamo hinted handoff

Case 23 is the correct prior-art and mechanism-family boundary for generic hinted handoff. Dynamo 2007 already retains a temporary replica plus a hint naming its intended destination and later hands it back. Cassandra's 4.1 persistent-window change is not evidence that Cassandra invented that family of behavior; it is a later operational refinement of **how long new deferred-delivery obligations remain admissible across repeated liveness transitions**.

---

## Philosophical interpretation

### I — remembering that a retention budget was already consumed

**Interpretive, not Apache terminology:** a system may need to remember the age of an unresolved memory obligation so that a temporary retention promise does not silently become permanent whenever a process or peer changes state.

CASSANDRA-19495 adds the symmetric warning: that remembered age must itself be forgettable when the obligation it summarized is gone. In project terms, the system must retain enough history to enforce forgetting, but must also know when that history has ceased to be authoritative.

---

## Boundaries and anti-overclaim

- `max_hint_window != guaranteed replica convergence deadline`.
- `endpoint downtime != age of oldest outstanding hint`.
- `restart / brief liveness != proof outstanding hints were delivered`.
- `hint admission rejected != repair complete`.
- `hint delivery != anti-entropy repair`.
- `earliest-hint timestamp != application version timestamp`.
- `persistent hint-window state != permanent hint retention`.
- `CASSANDRA-19495 bug report != proof every affected-version deployment lost data`.
- `4.1 persistent-window feature != invention of hinted handoff`.
- hint expiration, delivery, or deletion from the coordinator does not establish media sanitization anywhere in the cluster.

---

## Prior art and related-repository boundary

- Case 23 already grounds **Amazon Dynamo (2007)** as earlier primary evidence for hinted handoff, temporary placement, and later delivery. That is sufficient to block a generic Cassandra-origin claim here.
- A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Cassandra hint window` / persistent hinted handoff found no dedicated existing treatment at the time of this slice.
- A full genealogy of hinted handoff across Dynamo, Cassandra, Riak, Voldemort, and later systems belongs in `computing-archaeology` if pursued. This repository only retains the bounded state-lifetime relation needed for Case 41.

---

## Open evidence debt

- inspect the original CASSANDRA-14309 issue discussion / review thread if a stable archival export becomes available, especially for rejected alternative policies;
- test 4.1.0 and 4.1.5+ under controlled repeated down/up cycles with paused hint dispatch and a shortened window to reproduce both the pre-fix stale-window failure and the corrected lifecycle;
- compare on-disk descriptor timestamps with in-buffer earliest-hint state during restart, dispatch, and excision;
- trace whether later releases alter the admission predicate or persistence scope again, without projecting trunk behavior backward into 4.1.0.

---

## Status

**`grounded`** as a bounded Case 41 evidence deepening for persistent hint-window scope, retained maintenance-state currentness, and the 4.1.5 correction.
