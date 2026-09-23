# Evidence 142E — Ceph Reef restart boundary: persisted PG reporting state versus operative `_TOOFULL` state

**Status:** grounded  
**Case:** [`../cases/142-ceph-reef-capacity-gated-recovery.md`](../cases/142-ceph-reef-capacity-gated-recovery.md)  
**Baseline:** Ceph `v18.2.0` / tag object `1b139c136c6c691cc0201a42662d40f0da782d61`, resolving to commit `5dd24139a1eada541a3bc16b6941c5dde975e26d`  
**Bounded question:** if an OSD process stops while a PG is reported as `recovery_toofull` or `backfill_toofull`, does Reef restore that `_TOOFULL` condition as live peering-state authority from disk, or does the live state have to be reconstructed/re-entered after restart?

## Why this slice exists

Evidence 142B established three different maintenance-control horizons in the Reef source:

1. OSDMap/configuration fullness policy;
2. a PG's current `_TOOFULL` episode state;
3. a scheduled retry event.

It deliberately left one claim open:

> whether `PG_STATE_RECOVERY_TOOFULL` or `PG_STATE_BACKFILL_TOOFULL` themselves survive an OSD daemon crash/restart as operative state.

This slice closes that question at the **source-level initialization boundary** for the classic OSD path in released Reef `v18.2.0`.

The answer requires a distinction that is easy to miss because Ceph has two different fields both called, in effect, PG “state”:

```text
PeeringState::state
    = live state-machine/control state

pg_info_t.stats.state
    = PG statistics/reporting field
```

A serialized statistics snapshot can therefore contain PG-state bits without those bits being the mechanism that restores the live peering machine.

---

## Source ladder

| Source | Version | Evidence class | Use here |
|---|---|---|---|
| Ceph tag object for `v18.2.0` | 2023 | `H/P` | pins the release source to commit `5dd24139...` |
| `src/osd/PeeringState.h` | `v18.2.0` | `H/P` | live `state` initialization; `init_from_disk_state()` load boundary |
| `src/osd/PeeringState.cc` | `v18.2.0` | `H/P` | state-machine construction, dirty-state persistence call, `_TOOFULL` reactions, stats publication |
| `src/osd/PG.cc` | `v18.2.0` | `H/P` | PG disk-load path (`read_state`) and persisted PG metadata handoff |
| `src/osd/osd_types.h` | `v18.2.0` | `H/P` | `pg_info_t`, `pg_stat_t`, and the separate statistics `state` field |
| Evidence 142B | repository | prior bounded synthesis | retry/episode/policy horizons already grounded |

Primary anchors:

- tag ref: <https://api.github.com/repos/ceph/ceph/git/ref/tags/v18.2.0>
- `PeeringState.h`: <https://github.com/ceph/ceph/blob/v18.2.0/src/osd/PeeringState.h>
- `PeeringState.cc`: <https://github.com/ceph/ceph/blob/v18.2.0/src/osd/PeeringState.cc>
- `PG.cc`: <https://github.com/ceph/ceph/blob/v18.2.0/src/osd/PG.cc>
- `osd_types.h`: <https://github.com/ceph/ceph/blob/v18.2.0/src/osd/osd_types.h>
- prior source-level retry deepening: [`142-ceph-reef-source-retry-state-horizon-deepening.md`](142-ceph-reef-source-retry-state-horizon-deepening.md)

---

# Historical / source-level record

## 1. The live peering-state bitset is initialized independently

In `PeeringState.h`, the operative peering-state fields are explicitly declared as:

```cpp
int role = -1;
uint64_t state = 0;        // PG_STATE_*
```

The constructor in `PeeringState.cc` builds a fresh `info(spgid)`, constructs the state machine, and calls:

```cpp
machine.initiate();
```

This matters because the live `state` member starts from zero as part of a newly constructed peering-state object. It is not declared as an alias or reference into `pg_info_t.stats.state`.

Bounded result:

```text
new PeeringState instance
    -> live PG_STATE_* bitset starts at 0
```

This alone would not prove what the disk-load path later does, so the next step is essential.

---

## 2. The disk-load path restores PG information, past intervals, and the PG log — not the live state bitset

`PG::read_state()` reads persistent PG metadata into local values including:

- `pg_info_t info_from_disk`;
- `PastIntervals past_intervals_from_disk`;
- the PG log/missing state through the callback passed to `init_from_disk_state()`.

It then calls:

```cpp
recovery_state.init_from_disk_state(
    std::move(info_from_disk),
    std::move(past_intervals_from_disk),
    ...pg_log_init...);
```

The corresponding `PeeringState::init_from_disk_state()` implementation is narrow and explicit:

```cpp
info = std::move(info_from_disk);
last_written_info = info;
past_intervals = std::move(past_intervals_from_disk);
auto ret = pg_log_init(pg_log);
log_weirdness();
return ret;
```

There is no assignment in this initialization routine of the form:

```text
PeeringState::state <- info.stats.state
```

or another disk-loaded state-bit source into the live `state` member.

This closes the core source-level question:

> **Reef's inspected classic-OSD initialization path does not restore the live `PeeringState::state` bitset from the persisted PG statistics field.**

That is narrower than saying “Ceph persists no PG state,” which would be wrong.

---

## 3. `pg_info_t` can itself contain a serialized PG-state reporting snapshot

`osd_types.h` makes the trap explicit.

`pg_info_t` includes:

```cpp
pg_stat_t stats;
```

and `pg_stat_t` includes:

```cpp
uint64_t state;
```

with its own constructor initializing that statistics field to zero.

Therefore the correct boundary is **not**:

```text
PG_STATE bits are never serialized anywhere
```

Instead it is:

```text
serialized/reporting pg_info_t.stats.state
    != live PeeringState::state authority
```

A previous state report can be part of persisted `pg_info_t`, while the newly constructed control machine still begins with its own separate live state bitset.

This distinction is especially important for technical-retention language: a retained description of a prior control state is not automatically a retained executable continuation of that control state.

---

## 4. Runtime publication copies live state into the reporting field, not vice versa

The Reef peering code updates the statistics/reporting representation from the current live state. In the stats update path, after recording state-change timing, it performs:

```cpp
info.stats.state = state;
```

The direction is significant:

```text
live PeeringState::state
    -> pg_info_t.stats.state report/snapshot
```

The inspected restart initialization path does not reverse that arrow.

This supports a stronger, still bounded distinction:

```text
persisted state report
    != restored state-machine control authority
```

The word **report** here is a repository description of the role played by `pg_stat_t`; Ceph itself names the structure `pg_stat_t` and uses it for PG statistics/state reporting.

---

## 5. `_TOOFULL` is re-entered by the live state machine when the capacity condition is encountered again

Evidence 142B already grounded the relevant Reef transitions:

- `RecoveryTooFull` sets `PG_STATE_RECOVERY_TOOFULL` and schedules a later `DoRecovery()`;
- `RemoteReservationRejectedTooFull` sets `PG_STATE_BACKFILL_TOOFULL`, unwinds the current reservation attempt, and schedules a later `RequestBackfill()`;
- successful entry into the corresponding maintenance path clears the relevant wait/too-full bits.

Combined with the restart initialization boundary above, the source-level relationship is:

```text
before restart:
    live PG episode may carry *_TOOFULL

process reconstruction:
    new PeeringState::state starts from 0
    persisted pg_info/history/log are loaded
    state machine is initiated / peering proceeds

if capacity policy still rejects required maintenance:
    live state machine can set *_TOOFULL again
```

Thus the meaningful continuity is not “the exact `_TOOFULL` bit remained continuously live in process memory.”

The stronger continuity is distributed across other retained relations:

- PG/object/log information that still implies repair/backfill work;
- current placement/pool relations;
- OSDMap fullness policy;
- the newly executing peering/recovery logic that can test the condition again.

---

# Engineering reconstruction

## A. Five different state classes should not be collapsed

For this case, the restart boundary is clearest if five things are named separately.

### 1. Payload / replica state

The object embodiments and PG contents whose redundancy is incomplete.

### 2. Persistent PG recovery information

`pg_info_t`, past intervals, log/missing information, and related durable metadata used to reconstruct PG knowledge.

### 3. Persisted reporting snapshot

`pg_info_t.stats.state`, which can record PG state bits as statistics/reporting state.

### 4. Operative peering state

`PeeringState::state`, the live bitset manipulated by the peering state machine.

### 5. Cluster policy authority

OSDMap fullness ratios and related current map/configuration state that decide whether recovery/backfill is admissible.

These relations can coexist without sharing one persistence mechanism.

---

## B. Crash/restart does not have to retain the episode flag to retain the maintenance obligation

The useful reconstruction is:

```text
repair debt exists
    + persisted PG/log/placement evidence
    + fullness policy still active

OSD process dies
    ↓
old live *_TOOFULL episode bit disappears with old process state
    ↓
PG state is reconstructed from durable metadata + current cluster map
    ↓
maintenance admission is attempted again
    ↓
if target remains too full
    -> a new *_TOOFULL episode is produced
```

So:

```text
episode-state continuity
    != maintenance-obligation continuity
```

and:

```text
same human-readable PG state before and after restart
    != proof that one in-memory state instance survived the restart
```

This is a useful negative result. A maintenance obligation can survive by being **re-derivable** rather than by preserving every transient control bit.

---

## C. Persisted observability is weaker than operative resumption

Because `pg_info_t.stats.state` can be retained while `PeeringState::state` is newly initialized, the case also supports:

```text
retained observation / report
    != retained executable continuation
```

A stored report may help describe what the PG looked like, but this source path does not use that report as a checkpoint from which to resume the exact state-machine node.

This avoids an easy category error in distributed-system archaeology: seeing a state enum serialized inside a metadata structure does not by itself prove that the software restarts by restoring that enum into its live controller.

---

## D. Retry timers and retry obligation should remain separate

Evidence 142B showed that a capacity rejection schedules a future peering event after the configured retry interval.

This slice does **not** claim the timer/event object itself is durably checkpointed across process restart. The inspected initialization path instead supports a safer statement:

```text
pre-crash scheduled retry event
    != proven durable timer checkpoint

repair still needed after restart
    != dependent on preserving that exact timer object
```

Normal startup/peering can rediscover the need for work and encounter the same capacity gate again.

The exact wall-clock delay from restart to re-evaluation remains an empirical/runtime scheduling question, not established here.

---

# Functional analogy

A bounded analogy exists with systems that retain enough **authoritative substrate** to reconstruct a transient index or controller state after restart.

The functional pattern is:

```text
transient control representation disappears
    + lower-level durable facts survive
    -> control representation can be rebuilt/re-entered
```

This is only a functional analogy. It does not imply that Ceph PG peering is genealogically related to database index recovery, flash FTL reconstruction, or any other case in this repository.

A particularly useful contrast is Case 25 (Swift EC): some Swift filesystem markers are themselves part of the protocol's durable/current qualification. In Case 142 here, the inspected `pg_stat_t.state` report is **not** the restart authority for `PeeringState::state`. Similar-looking metadata can therefore occupy different authority roles.

---

# Philosophical / media-theoretical interpretation

The narrow interpretive lesson is not that “state is ephemeral.”

It is that continuity can be carried at a different layer from the visible symptom of continuity.

For a capacity-blocked Ceph PG, the human-visible label `backfill_toofull` may disappear with one process episode and later reappear, while the deeper reason for repair remains in the surviving object/PG/log/map relations.

That supports a bounded formulation:

> **technical continuity can be reconstructive: a transient description need not persist continuously if the relations required to regenerate the obligation and its current diagnosis remain available.**

This remains an engineering-grounded interpretation. It is not a claim that every recomputable state is equivalent to retained payload or that all distributed control metadata forms one ontological class.

---

# Explicit non-claims / limits

This evidence does **not** establish any of the following:

1. that no PG-state bits are ever serialized — `pg_info_t.stats.state` exists and may be serialized with `pg_info_t`;
2. that every value in `pg_info_t.stats.state` is necessarily stale after restart;
3. that monitor-visible PG state has a particular stale-report interval during OSD startup;
4. that a restarted PG immediately returns to `backfill_toofull` or `recovery_toofull` with no intermediate states;
5. that the same OSD remains primary or the same target remains selected after restart;
6. that OSDMap fullness policy itself is reconstructed from `pg_info_t` — it is separate cluster-map authority;
7. that the pre-crash scheduled retry event/timer is durably checkpointed;
8. that re-peering or re-evaluation completes within the configured retry interval after a process restart;
9. that all Ceph releases before/after Reef use the identical load/state representation;
10. that Crimson OSD has been independently proven identical here; this slice is bounded to the classic OSD path inspected in Reef `v18.2.0`;
11. that a capacity gate is the only reason recovery/backfill can remain blocked after restart;
12. that source-level reconstruction semantics are equivalent to a real crash/fault-injection trace.

---

# What is now closed

For the classic OSD path in Ceph Reef `v18.2.0`, the prior open question can now be narrowed from:

> do `_TOOFULL` flags themselves survive OSD daemon restart?

to the source-grounded answer:

> **the live `PeeringState::state` bitset is newly initialized, and `init_from_disk_state()` restores `pg_info_t`, past intervals, and PG-log state without loading `pg_info_t.stats.state` back into the live bitset. A persisted PG-state statistics snapshot therefore does not constitute restored operative `_TOOFULL` authority.**

If the same capacity constraint still applies, the live state machine can produce a new `_TOOFULL` episode when recovery/backfill admission is attempted again.

Case 142 should remain `grounded`; this closes one control-state persistence debt but is not a reason for maturity promotion.

---

# Remaining bounded debt

The next useful one-round slices are now more empirical and narrower:

1. **restart fault trace:** run Reef with a PG held in `backfill_toofull`, kill/restart the primary OSD, and capture the exact state sequence and elapsed time until capacity gating is re-established;
2. **monitor-report boundary:** measure whether/how long a monitor can display pre-restart PG statistics while the restarted OSD is still peering;
3. **scheduled-event boundary:** instrument whether the first post-restart retry is driven by startup/peering discovery, a newly scheduled timer, or another map/event trigger in the tested scenario;
4. **Crimson comparison:** independently inspect Crimson OSD initialization and reporting authority before generalizing the classic-path result;
5. **mixed-version behavior:** keep release evolution in `computing-archaeology` unless it is needed to resolve a retention-specific compatibility claim.

---

# Related-repository check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `backfill_toofull` again found no dedicated reusable module.

The division remains:

- `technical-retention`: what must remain authoritative across a blocked-repair episode and restart, and which transient state can be reconstructed;
- `computing-archaeology`: broader release genealogy of PG-state serialization, reservation machinery, schedulers, and OSD implementation changes.

No general Ceph history is duplicated here.