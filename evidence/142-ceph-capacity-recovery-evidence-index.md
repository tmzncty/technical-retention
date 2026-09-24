# Case 142 evidence index — Ceph capacity-gated recovery and reconstructed maintenance state

**Case:** [`142 — Ceph Reef capacity-gated recovery`](../cases/142-ceph-reef-capacity-gated-recovery.md)  
**Current maturity:** `grounded`  
**Purpose:** evidence navigation, authority-layer separation, and bounded-debt tracking

## Why this index exists

Case 142 now contains several evidence slices that all mention recovery, backfill, fullness, reservation, scheduling, retry, and restart, but they answer different questions.

They should not be collapsed into a single claim that “Ceph stops recovery when disks are full.”

The current package separates:

```text
repair / redundancy obligation
    != current capacity policy
    != projected-capacity accounting
    != initial maintenance admission
    != continuing reservation / execution authority
    != scheduler class / resource share
    != live PG episode state
    != retry scheduling state
    != persisted PG reporting snapshot
    != operative state reconstructed after restart
```

This index keeps those layers navigable and records which debts are closed.

---

## Canonical case

### C142 — Ceph Reef capacity-gated recovery

[`../cases/142-ceph-reef-capacity-gated-recovery.md`](../cases/142-ceph-reef-capacity-gated-recovery.md)

The canonical case establishes the broad bounded result:

```text
payload still serviceable
    != configured redundancy restored
    != repair currently executable
```

It also separates:

- `active` from `clean`;
- recovery/backfill need from repair admission;
- `nearfull`, `backfillfull`, `full`, and failsafe-full roles;
- destination eligibility from mere CRUSH placement suitability;
- automatic fullness gating from operator `nobackfill` / `norecover` / `norebalance` pauses;
- current occupancy from projected occupancy after already-mapped backfill.

Use the canonical case for the overall mechanism and maturity claim. Use the evidence layers below for exact source, chronology, accounting, scheduling, revocation, and restart boundaries.

---

## Evidence chain A — Reef documentation grounding

### E142-A — capacity-gated recovery / repair headroom grounding

[`142-ceph-reef-capacity-gated-recovery-grounding.md`](142-ceph-reef-capacity-gated-recovery-grounding.md)

**Question:** can a PG remain serviceable while recovery/backfill is blocked because a destination is too full?

**Bounded result:** Reef documentation explicitly distinguishes `active`, `clean`, `degraded`, `recovery_toofull`, and `backfill_toofull`, and documents fullness thresholds plus delayed retry.

This grounds the first-order relation:

```text
current serviceability
    != restored redundancy

repair is needed
    != repair is presently admitted
```

**Do not infer:** data loss from `_toofull`, universal read availability while degraded, or a physical-media failure threshold from `backfillfull`.

---

## Evidence chain B — source-level retry and episode horizons

### E142-B — Reef retry state / maintenance-control horizons

[`142-ceph-reef-source-retry-state-horizon-deepening.md`](142-ceph-reef-source-retry-state-horizon-deepening.md)

**Question:** after a capacity rejection, what live source-level state records the blocked episode and how does Ceph try again?

**Pinned baseline:** Ceph `v18.2.0`, commit `5dd24139a1eada541a3bc16b6941c5dde975e26d`.

The source distinguishes:

```text
policy horizon
    -> fullness ratios / cluster-map authority

episode horizon
    -> PG_STATE_RECOVERY_TOOFULL / PG_STATE_BACKFILL_TOOFULL

retry horizon
    -> scheduled DoRecovery() / RequestBackfill() event
```

A capacity rejection can unwind the current reservation attempt while leaving the maintenance obligation live and scheduling a later attempt.

Important distinction:

```text
reservation attempt ended
    != redundancy debt discharged
```

Evidence E142-E below separately closes the former restart question for the live `_TOOFULL` bitset.

---

## Evidence chain C — projected capacity and promised backfill bytes

### E142-C — projected-backfill admission accounting

[`142-ceph-reef-projected-backfill-admission-accounting-deepening.md`](142-ceph-reef-projected-backfill-admission-accounting-deepening.md)

**Question:** does Reef fullness admission consider only bytes already present on the destination, or can already-promised/proposed maintenance bytes affect present admission?

**Bounded result:** the source carries byte-count information into remote backfill reservation and computes an adjusted utilization that includes pending/proposed backfill state before comparing ordinary fullness thresholds.

For replicated PGs, the extra claim is based on the missing difference rather than charging the whole source PG again; for EC, the source intentionally overestimates by a full stripe per object because exact per-object rounding is not available at that point.

This supports:

```text
raw physical utilization
    != utilization adjusted for promised/proposed backfill
    != exact eventual backend allocation
```

The accounting is an admission/control relation. It is not disk-extent preallocation and not another payload copy.

---

## Evidence chain D — scheduler/execution authority after admission

### E142-D — Reef mClock maintenance-scheduling boundary

[`142-ceph-reef-mclock-maintenance-scheduling-boundary-deepening.md`](142-ceph-reef-mclock-maintenance-scheduling-boundary-deepening.md)

**Question:** once maintenance is known to be needed and has passed the relevant capacity/reservation gates, what separately governs its access to OSD execution resources?

**Bounded result:** Reef exposes another control layer through mClock service classes, profiles, reservation/weight/limit policy, and separate recovery/backfill concurrency controls.

The evidence fixes:

```text
repair obligation
    != capacity admission
    != scheduler service class
    != scheduler resource share / dequeue opportunity
    != maintenance completion
```

It also blocks the shortcut that all maintenance or all redundancy-restoration traffic belongs to one immutable scheduler class. Documentation-level classes and source-level priority-derived queue classification must be kept distinct.

This file is a scheduling slice, not dmClock/mClock genealogy. Broad scheduler history remains a `computing-archaeology` concern.

---

## Evidence chain E — restart boundary: reporting snapshot versus operative PG state

### E142-E — Reef restart reconstruction of `_TOOFULL` state

[`142-ceph-reef-restart-reporting-vs-operative-state-deepening.md`](142-ceph-reef-restart-reporting-vs-operative-state-deepening.md)

**Question:** when an OSD restarts, is a prior `_TOOFULL` PG state restored as live state-machine authority from disk?

**Pinned baseline:** classic OSD path in Ceph `v18.2.0`.

The source exposes two different “state” representations:

```text
PeeringState::state
    = live PG_STATE_* control bitset

pg_info_t.stats.state
    = statistics/reporting field retained inside pg_info_t
```

The live `PeeringState::state` member is initialized independently. Disk initialization restores PG info/history/log relations without assigning the persisted `info.stats.state` report back into the live state bitset.

During normal operation, the reporting direction is instead:

```text
live PeeringState::state
    -> info.stats.state
```

This closes the restart boundary:

```text
persisted PG-state report
    != restored live state-machine authority
```

A restarted PG can later produce a new `_TOOFULL` episode if the durable/current PG relations still require repair and current capacity policy rejects the new attempt.

Therefore:

```text
episode-state continuity
    != maintenance-obligation continuity
```

and:

```text
maintenance obligation may survive by re-derivation
    rather than checkpointing every transient episode bit
```

**Do not infer:** exact monitor stale-state timing, persistence of the pre-crash timer object, identical Crimson semantics, or measured production restart timing.

---

## Evidence chain F — initial rejection versus in-flight revocation

### E142-F — revocable backfill admission

[`142-ceph-reef-backfill-rejection-vs-revocation-authority-deepening.md`](142-ceph-reef-backfill-rejection-vs-revocation-authority-deepening.md)

**Question:** after a target has granted a backfill reservation and the PG is already backfilling, does that earlier capacity admission remain valid until completion?

**Pinned baseline:** classic Reef OSD path in Ceph `v18.2.0`.

`MBackfillReserve` explicitly distinguishes:

```text
REJECT_TOOFULL
    -> refuse a reservation request because the target is too full

REVOKE_TOOFULL
    -> withdraw an already-granted reservation because the target is too full
```

The primary-side paths are correspondingly different:

```text
initial rejection:
REQUEST
    -> REJECT_TOOFULL
    -> unwind current reservation attempt
    -> backfill_toofull
    -> delayed RequestBackfill

in-flight revocation:
REQUEST
    -> GRANT
    -> Backfilling
    -> REVOKE_TOOFULL
    -> cancel current backfill
    -> backfill_toofull
    -> delayed RequestBackfill
```

This closes a new source-level boundary:

```text
initial admission success
    != continuing authority to execute until completion
```

Project term: **revocable maintenance admission**. This is engineering reconstruction, not Ceph historical vocabulary.

The same message header also exposes a compatibility boundary: without `RECOVERY_RESERVATION_2`, `RELEASE`, `REVOKE_TOOFULL`, and `REVOKE` can be encoded as the older `REJECT_TOOFULL` value. Therefore:

```text
current local semantic distinction
    != distinction necessarily preserved on the wire to an older peer
```

This does not establish a full release genealogy.

Upstream `qa/tasks/backfill_toofull.py` further shows a nonterminal lifecycle spanning `backfill_toofull`, later `backfilling`, interruption, and eventual `clean`, but it does not directly inject the exact in-flight capacity-triggered `REVOKE_TOOFULL` path. That measured trace remains open.

---

## Supplemental chronology — pre-Reef semantics evolution

### E142-HIST — 2012–2019 `backfill_toofull` evolution

[`142-ceph-2012-2019-backfill-toofull-semantics-evolution-deepening.md`](142-ceph-2012-2019-backfill-toofull-semantics-evolution-deepening.md)

**Question:** how far before Reef can the relevant state vocabulary and capacity-gated behavior be directly anchored without turning Case 142 into a full Ceph history?

**Bounded result:** upstream source/documentation establishes a conservative chronology including:

- 2012 implementation with backfill-full threshold, `PG_STATE_BACKFILL_TOOFULL`, rejection, and delayed retry;
- 2014 documentation naming `backfill_toofull`;
- later differentiation of too-full rejection/revocation causes;
- 2018 projected-byte admission;
- 2019 health/state cleanup separating capacity causation from generic reservation retry.

The methodological result is:

```text
same visible state name across releases
    != unchanged trigger / transport / diagnostic semantics
```

The broader reservation/scheduler genealogy remains a `computing-archaeology` concern.

---

## Combined technical picture

The evidence chain now supports this layered model:

```text
surviving object / replica state
    + PG info / log / missing relations
    + configured replica target
        |
        v
repair obligation
        |
        +------------------------------+
        |                              |
        v                              v
current OSDMap policy           candidate destination
        |                              |
        +--------------+---------------+
                       v
        projected-capacity / reservation admission
                       |
           +-----------+-----------+
           |                       |
           v                       v
       admitted                rejected too full
           |                       |
           v                       v
  scheduler / concurrency      live *_TOOFULL
       execution policy             |
           |                        v
           v                 delayed retry
     backfill running
           |
           +-------------------------------+
           |                               |
           v                               v
   completes normally          reservation revoked too full
           |                               |
           v                               v
 recovered / clean path       cancel current backfill episode
                                           |
                                           v
                                  live backfill_toofull
                                           |
                                           v
                                      delayed retry
```

A process restart adds a different boundary:

```text
durable PG info/log + cluster-map relations survive/reappear
    while
live PeeringState::state is newly initialized
    and
persisted info.stats.state is not restored as live authority

therefore:
maintenance need and capacity diagnosis can be re-derived
```

This yields at least eight distinct continuity questions:

1. **payload continuity** — do usable object embodiments remain?
2. **redundancy-obligation continuity** — does the system still know the configured replica target is not satisfied?
3. **policy continuity** — what fullness thresholds and placement rules currently govern admission?
4. **accounting continuity** — what pending/promised capacity is counted against new work?
5. **execution-authority continuity** — does an accepted backfill still have permission/reservation to continue?
6. **scheduler-policy continuity** — what service class/resource share governs admitted work?
7. **episode continuity** — is this live peering machine currently marked `_TOOFULL` / `BACKFILLING` / waiting?
8. **reporting continuity** — what state snapshot is retained/published about the PG?

They compose, but they are not synonyms.

---

## Cross-case comparison

### Case 05 — RADOS replicated-object repair

[`../cases/05-rados-replicated-object-repair.md`](../cases/05-rados-replicated-object-repair.md)

Case 05 supplies the ordinary RADOS repair/currentness substrate. Case 142 asks what happens when resource policy refuses or later withdraws the next repair embodiment needed to restore the ordinary replica target.

### Case 98 — unfound recovery exhaustion

[`../cases/98-ceph-unfound-recovery-exhaustion-administrative-loss.md`](../cases/98-ceph-unfound-recovery-exhaustion-administrative-loss.md)

```text
source/current state cannot be found
    != destination capacity rejects or revokes repair
```

`unfound` is a source/currentness problem; `_toofull` is an admission/headroom problem.

### Case 25 — Swift EC durable/currentness evidence

[`../cases/25-openstack-swift-ec-overwrite-durable-currentness.md`](../cases/25-openstack-swift-ec-overwrite-durable-currentness.md)

Functional contrast only. Swift has filesystem representations that themselves participate in durable/current qualification. E142-E shows a different authority relation: a persisted `pg_stat_t.state` snapshot is not the restart checkpoint for Ceph's live peering-state bitset.

```text
metadata is serialized
    != metadata is restart authority
```

No genealogy is claimed.

### Case 136 — rebuild-rate repair priority

[`../cases/136-megaraid-perc-rebuild-rate-repair-priority.md`](../cases/136-megaraid-perc-rebuild-rate-repair-priority.md)

Functional analogy only:

```text
repair priority
    != repair admission
    != continuing repair authority
```

Case 136 varies how strongly admitted repair competes for resources. Case 142 additionally shows a gate that can refuse admission and a reservation that can later be revoked.

### Case 111 — managed-Flash background maintenance interruption

[`../cases/111-enterprise-ssd-extended-shutdown-maintenance.md`](../cases/111-enterprise-ssd-extended-shutdown-maintenance.md)

Functional analogy only. eMMC BKOPS/HPI supplies another counterexample to the assumption that one maintenance obligation must execute in one uninterrupted episode. The cause differs: HPI is priority interruption; Ceph `REVOKE_TOOFULL` is capacity/reservation withdrawal. No genealogy is asserted.

---

## What is closed

The Case-142 package now has direct documentation/source support for:

- current serviceability being distinct from configured redundancy restoration;
- `recovery_toofull` / `backfill_toofull` as capacity-blocked maintenance states rather than proof of data loss;
- capacity rejection leaving a retryable maintenance obligation;
- fullness policy, live episode state, and retry cadence being distinct control layers;
- current raw utilization being distinct from projected utilization after promised/proposed backfill bytes;
- projected-byte accounting having explicit approximation limits, especially for EC and unavailable backend-overhead information;
- scheduling/resource-share policy being distinct from capacity admission and from repair completion;
- a pre-Reef implementation floor for `backfill_toofull` semantics and later refinement of causation/health reporting;
- classic Reef OSD live `PeeringState::state` being initialized independently of the persisted `pg_info_t.stats.state` report;
- disk initialization restoring PG info/history/log relations without restoring the reporting state field into the live state bitset;
- `_TOOFULL` continuity across restart therefore being reconstructive/re-entered rather than direct live-bit checkpoint restoration;
- Reef distinguishing initial `REJECT_TOOFULL` from in-flight `REVOKE_TOOFULL` in the backfill reservation protocol;
- an active backfill being cancelable for a later too-full condition while the repair obligation remains retryable;
- mixed/older-peer compatibility being able to collapse several newer reservation/revocation meanings into the older rejection encoding.

The former explicit debt “do `_TOOFULL` PG flags themselves survive an OSD daemon restart?” remains **closed at the classic Reef source-initialization level** with a negative/qualified answer: a state report may persist, but it is not loaded back as operative peering-state authority.

The new source-level question “does one successful backfill reservation remain irrevocably valid until completion?” is also **closed for the classic Reef source baseline** with a negative answer: `REVOKE_TOOFULL` can withdraw an already-granted backfill reservation and return the PG to a retryable `backfill_toofull` episode.

Case 142 remains `grounded`. These deepenings improve mechanism resolution; they do not independently justify maturity promotion.

---

## Remaining bounded debt

Priority order for future one-round slices:

### 1. In-flight capacity-revocation trace

Run or locate a Reef classic-OSD trace where a target:

- first grants the reservation;
- reaches `backfilling`;
- crosses the capacity condition while remaining alive;
- emits/causes `REVOKE_TOOFULL`;
- makes the primary leave `backfilling` and publish `backfill_toofull`;
- later admits a retry.

Target boundary:

```text
source path exists
    != measured revocation path / timing
```

### 2. Partial-backfill residue semantics

Inspect exactly what `cancel_backfill()` and the lower backfill backend retain, discard, or rediscover after revocation.

```text
backfill canceled
    != partial transfer rolled back
    != partial transfer reused on retry
```

### 3. Real restart/fault trace

With a known `backfill_toofull` PG, terminate/restart the relevant OSD and capture monitor-visible state, startup/peering intermediate states, first new capacity rejection, and time until `_TOOFULL` is republished.

### 4. Monitor stale-report window

Measure whether a monitor retains/presents the pre-restart state snapshot while the new OSD instance has not yet republished its operative state.

### 5. Retry-event restart semantics

Instrument which event causes the first post-restart repair attempt. Do not assume the pre-crash delayed event survived merely because repair resumes.

### 6. Crimson OSD comparison

Independently inspect Crimson's initialization/load/reporting and backfill-revocation paths before generalizing the classic OSD results.

### 7. Production evidence

Find a named public incident/operations trace showing capacity-gated recovery, preferably including an already-running backfill that is revoked for capacity.

### 8. Broader history

First-introduction genealogy, release/backport matrices, scheduler evolution, reservation-message compatibility history, and wider PG-state serialization history should remain in `tmzncty/computing-archaeology` unless a specific retention claim requires them.

---

## Related-repository status

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `backfill_toofull` found no dedicated reusable module.

Current division of labor:

- **technical-retention:** authority layers, repair debt, capacity admission, projected headroom, revocable execution authority, scheduler/resource separation, retry/restart reconstruction;
- **computing-archaeology:** broad implementation genealogy, reservation/message evolution, scheduler history, release-by-release semantics, compatibility archaeology, historical benchmarks.

Do not duplicate the general RADOS history already grounded in Case 05.