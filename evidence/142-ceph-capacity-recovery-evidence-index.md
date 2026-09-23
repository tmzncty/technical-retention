# Case 142 evidence index — Ceph capacity-gated recovery and reconstructed maintenance state

**Case:** [`142 — Ceph Reef capacity-gated recovery`](../cases/142-ceph-reef-capacity-gated-recovery.md)  
**Current maturity:** `grounded`  
**Purpose:** evidence navigation, authority-layer separation, and bounded-debt tracking

## Why this index exists

Case 142 now contains several evidence slices that all mention `backfill_toofull`, recovery, fullness policy, and retry, but they answer different questions.

They should not be collapsed into a single claim that “Ceph stops recovery when disks are full.”

The current package separates:

```text
repair / redundancy obligation
    != current capacity policy
    != projected-capacity accounting
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

Use the canonical case for the overall mechanism and maturity claim. Use the evidence layers below for exact source, chronology, accounting, and restart boundaries.

---

## Evidence chain 1 — Reef documentation grounding

### E142-1 — capacity-gated recovery / repair headroom grounding

[`142-ceph-reef-capacity-gated-recovery-grounding.md`](142-ceph-reef-capacity-gated-recovery-grounding.md)

**Question:** can a PG remain serviceable while repair/backfill is blocked because a destination is too full?

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

## Evidence chain 2 — source-level retry and episode horizons

### E142-2 — Reef retry state / maintenance-control horizons

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

**Important distinction:**

```text
reservation attempt ended
    != redundancy debt discharged
```

The original slice deliberately did **not** establish restart persistence of the `_TOOFULL` live state bits. Evidence chain 5 below now closes that narrower source-level debt for the classic Reef OSD path.

---

## Evidence chain 3 — projected capacity and promised backfill bytes

### E142-3 — projected-backfill admission accounting

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

## Evidence chain 4 — pre-Reef semantics chronology

### E142-4 — 2012–2019 `backfill_toofull` evolution

[`142-ceph-2012-2019-backfill-toofull-semantics-evolution-deepening.md`](142-ceph-2012-2019-backfill-toofull-semantics-evolution-deepening.md)

**Question:** how far before Reef can the relevant state vocabulary and capacity-gated behavior be directly anchored without turning Case 142 into a full Ceph history?

**Bounded result:** upstream source/documentation establishes a conservative chronology including:

- 2012 implementation with backfill-full threshold, `PG_STATE_BACKFILL_TOOFULL`, rejection, and delayed retry;
- 2014 documentation naming `backfill_toofull`;
- later differentiation of too-full rejection/revocation causes;
- 2018 projected-byte admission;
- 2019 health/state cleanup separating capacity causation from generic reservation retry.

The important methodological result is:

```text
same visible state name across releases
    != unchanged trigger / transport / diagnostic semantics
```

This chronology is intentionally bounded. Wider Ceph reservation/scheduler genealogy remains a `computing-archaeology` concern.

---

## Evidence chain 5 — restart boundary: reporting snapshot versus operative PG state

### E142-5 — Reef restart reconstruction of `_TOOFULL` state

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

The live `PeeringState::state` member is initialized to zero. `PG::read_state()` loads `pg_info_t`, past intervals, and PG-log state, and `PeeringState::init_from_disk_state()` moves those structures into the new instance without assigning `info.stats.state` back into the live bitset.

During normal operation, the reporting direction is instead:

```text
live PeeringState::state
    -> info.stats.state
```

This closes the former restart non-claim at source level:

```text
persisted PG-state report
    != restored live state-machine authority
```

A restarted PG can later produce a new `_TOOFULL` episode if the durable/current PG relations still require repair and the current capacity policy rejects the new admission attempt.

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

**Do not infer:** exact monitor stale-state timing, immediate post-restart state order, persistence of the pre-crash timer object, identical Crimson semantics, or a measured production restart trace.

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
               admission calculation
                       |
           +-----------+-----------+
           |                       |
           v                       v
       admitted                rejected too full
           |                       |
           v                       v
 recovery/backfill      live *_TOOFULL episode bit
                                   |
                                   v
                         delayed retry scheduling

process restart boundary:
    durable PG info/log + cluster map survive/reappear
    live PeeringState::state is newly initialized
    persisted info.stats.state is not restored as live authority
    maintenance need and capacity diagnosis can be re-derived
```

This yields at least six distinct continuity questions:

1. **payload continuity** — do usable object embodiments remain?
2. **redundancy-obligation continuity** — does the system still know the configured replica target is not satisfied?
3. **policy continuity** — what fullness thresholds and placement rules currently govern admission?
4. **accounting continuity** — what pending/promised capacity is counted against new work?
5. **episode continuity** — is this live peering machine currently marked `_TOOFULL`?
6. **reporting continuity** — what state snapshot is retained/published about the PG?

They compose, but they are not synonyms.

---

## Cross-case comparison

### Case 05 — RADOS replicated-object repair

[`../cases/05-rados-replicated-object-repair.md`](../cases/05-rados-replicated-object-repair.md)

Case 05 supplies the ordinary RADOS repair/currentness substrate. Case 142 does not duplicate it; it asks what happens when the destination-capacity policy refuses the next embodiment needed to restore the ordinary replica target.

### Case 98 — unfound recovery exhaustion

[`../cases/98-ceph-unfound-recovery-exhaustion-administrative-loss.md`](../cases/98-ceph-unfound-recovery-exhaustion-administrative-loss.md)

The distinction remains:

```text
source/current state cannot be found
    != destination capacity rejects repair
```

`unfound` is a source/currentness problem; `_toofull` is an admission/headroom problem.

### Case 25 — Swift EC durable/currentness evidence

[`../cases/25-openstack-swift-ec-overwrite-durable-currentness.md`](../cases/25-openstack-swift-ec-overwrite-durable-currentness.md)

Functional contrast only. Swift has filesystem representations that themselves participate in durable/current qualification. Case 142 E142-5 shows a different authority relation: a persisted `pg_stat_t.state` snapshot is not the restart checkpoint for Ceph's live peering-state bitset.

The useful warning is:

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
```

Case 136 varies how strongly admitted repair competes for resources. Case 142 shows a gate that can refuse admission entirely until capacity conditions change.

---

## What is closed

The Case 142 package now has direct documentation/source support for:

- current serviceability being distinct from configured redundancy restoration;
- `recovery_toofull` / `backfill_toofull` as capacity-blocked maintenance states rather than proof of data loss;
- capacity rejection leaving a retryable maintenance obligation;
- fullness policy, live episode state, and retry cadence being distinct control layers;
- current raw utilization being distinct from projected utilization after promised/proposed backfill bytes;
- projected-byte accounting having explicit approximation limits, especially for EC and unavailable backend-overhead information;
- a pre-Reef implementation floor for `backfill_toofull` semantics and later refinement of causation/health reporting;
- classic Reef OSD live `PeeringState::state` being initialized independently of the persisted `pg_info_t.stats.state` report;
- disk initialization restoring PG info/history/log relations without restoring the reporting state field into the live state bitset;
- `_TOOFULL` continuity across restart therefore being reconstructive/re-entered rather than proven as direct live-bit checkpoint restoration.

The former explicit debt “do `_TOOFULL` PG flags themselves survive an OSD daemon restart?” is now **closed at the classic Reef source-initialization level** with a negative/qualified answer: a state report may persist, but it is not loaded back as operative peering-state authority.

Case 142 remains `grounded`. These deepenings improve mechanism resolution; they do not independently justify maturity promotion.

---

## Remaining bounded debt

Priority order for future one-round slices:

### 1. Real restart/fault trace

Run Reef with a known `backfill_toofull` PG, terminate/restart the relevant OSD, and capture:

- monitor-visible state before death;
- startup/peering intermediate states;
- first new capacity-rejection event;
- time until `_TOOFULL` is re-published;
- whether destination/primary changes alter the path.

Target boundary:

```text
source-level reconstruction path
    != measured restart behavior/timing
```

### 2. Monitor stale-report window

Measure whether a monitor retains/presents the pre-restart state snapshot while the new OSD instance has not yet republished its operative state.

### 3. Retry-event restart semantics

Instrument which event causes the first post-restart repair attempt. Do not assume the pre-crash delayed event survived merely because repair resumes.

### 4. Crimson OSD comparison

Independently inspect Crimson's initialization/load/reporting path before generalizing E142-5 beyond classic OSD.

### 5. Production evidence

Find a named public incident/operations trace showing capacity-gated recovery and restart behavior. Keep anecdotal operator reports below first-party source/test evidence unless independently corroborated.

### 6. Broader history

First-introduction genealogy, release/backport matrices, scheduler evolution, and wider PG-state serialization history should remain in `tmzncty/computing-archaeology` unless a specific retention claim requires them.

---

## Related-repository status

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `backfill_toofull` still found no dedicated reusable module.

Current division of labor:

- **technical-retention:** authority layers, repair debt, capacity admission, projected headroom, retry/restart reconstruction;
- **computing-archaeology:** broad implementation genealogy, scheduler/reservation history, release-by-release evolution, historical benchmarks.

Do not duplicate the general RADOS history already grounded in Case 05.