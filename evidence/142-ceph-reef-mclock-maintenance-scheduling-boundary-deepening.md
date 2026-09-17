# Evidence 142D — Ceph Reef mClock maintenance-scheduling boundary

**Status:** `bounded deepening complete`  
**Case:** [`../cases/142-ceph-reef-capacity-gated-recovery.md`](../cases/142-ceph-reef-capacity-gated-recovery.md)  
**Baseline:** Ceph `v18.2.0` / Reef source and documentation line.  
**Bounded question:** once recovery/backfill is known to be needed and has passed the relevant capacity/reservation gates, what separately governs its access to OSD execution resources, and can “repair priority” safely be treated as one scalar across Ceph maintenance work?

## Evidence boundary

Case 142 already establishes three different relations:

1. **redundancy debt** — a PG is not yet at the configured replica state;
2. **capacity admission** — destination fullness policy can refuse recovery/backfill even while the debt remains;
3. **retry state** — a rejected attempt can be unwound while a later retry obligation remains live.

Evidence 142C further shows that backfill admission can use projected rather than merely current occupancy.

This slice begins **after that conceptual boundary** and asks a different question:

> If maintenance is admissible, does it therefore have an undifferentiated right to consume OSD resources until it finishes?

For the Reef baseline, the answer is no. Ceph's mClock configuration and scheduler expose another layer that classifies queued operations and allocates resource share between external client work and different kinds of background work.

The central separation is:

```text
repair obligation
    != capacity admission
    != reservation acquisition
    != scheduler service class
    != scheduler resource share / dequeue opportunity
    != maintenance execution
    != repair completion
```

This is a scheduling slice, not a history of dmClock, Ceph scheduler evolution, BlueStore performance, or recovery implementation in general.

It does **not** infer scheduler semantics from the `_TOOFULL` retry path. That earlier evidence explicitly left mClock open; this file closes only the bounded Reef scheduling relation with direct documentation/source evidence.

---

## Primary source ladder

| Source | Version / date | Evidence class | Use here |
| --- | --- | --- | --- |
| Ceph `doc/rados/configuration/mclock-config-ref.rst` | `v18.2.0` / Reef | `H/P` | mClock service classes; built-in profiles; reservation/weight/limit allocation; recovery/backfill option locking; sleep-option handoff; persistent-config versus ephemeral runtime override interface |
| Ceph `src/osd/scheduler/OpSchedulerItem.h` | `v18.2.0` | `H/P` | scheduler-class enum; priority-to-class mapping; per-queueable classification; recovery/backfill message classification is not reducible to one English maintenance label |
| Ceph `doc/dev/osd_internals/mclock_wpq_cmp_study.rst` | shipped in `v18.2.0`; study records a Quincy-development test baseline | `H/P` with chronology caveat | explains reservation/weight/limit as scheduler resource controls and records controlled comparison methodology; not used as the Reef-profile-default authority |
| Existing Evidence 142A–C | repository-grounded Reef material | `H/P + E` | capacity gate, retry horizon, and projected-capacity layers that this scheduling slice must not collapse |

Primary anchors:

- Reef mClock configuration reference: <https://github.com/ceph/ceph/blob/v18.2.0/doc/rados/configuration/mclock-config-ref.rst>
- Reef scheduler queueable/class source: <https://github.com/ceph/ceph/blob/v18.2.0/src/osd/scheduler/OpSchedulerItem.h>
- mClock/WPQ comparison study shipped in the Reef source tree: <https://github.com/ceph/ceph/blob/v18.2.0/doc/dev/osd_internals/mclock_wpq_cmp_study.rst>
- Case 142 capacity grounding: [`142-ceph-reef-capacity-gated-recovery-grounding.md`](142-ceph-reef-capacity-gated-recovery-grounding.md)
- Case 142 retry-state deepening: [`142-ceph-reef-source-retry-state-horizon-deepening.md`](142-ceph-reef-source-retry-state-horizon-deepening.md)
- Case 142 projected-capacity deepening: [`142-ceph-reef-projected-backfill-admission-accounting-deepening.md`](142-ceph-reef-projected-backfill-admission-accounting-deepening.md)

The source-tree comparison study is deliberately used only for the **meaning and empirical intent of mClock resource controls**. Its test environment is an earlier Quincy-development snapshot and its profile tables must not be silently substituted for the Reef configuration reference. The `v18.2.0` configuration reference is the authority for this slice's Reef profile values and documented client-type classification.

---

## Historical / implementation record

### H/P — Reef exposes a scheduler layer distinct from fullness admission

The Reef mClock configuration reference describes mClock as a queuing scheduler used to tune QoS between client I/O and background operations in an OSD.

Its input model includes measured/configured OSD capacity plus a selected mClock profile. The profile then determines lower-level resource-control parameters.

Nothing in that description makes the scheduler itself a replacement for the fullness gate already grounded by Case 142. The two surfaces answer different questions:

```text
fullness / projected-capacity policy:
    may this destination accept this maintenance work?

mClock scheduling policy:
    once operations are queueable, how do service classes share OSD execution capacity?
```

This distinction is historical/implementation evidence at the interface level, not merely a project analogy: the Reef documentation presents the mechanisms under different controls and different state.

### H/P — the user-facing mClock model has three broad service buckets

The Reef mClock reference classifies requests into:

- **Client** — external client I/O;
- **Background recovery** — internal recovery requests;
- **Background best-effort** — internal backfill, scrub, snap trim, and PG deletion requests.

That is already enough to reject one tempting simplification:

`all redundancy-restoration work == one scheduler class`

At the documentation level, recovery and backfill are not assigned to the same broad mClock bucket.

This does **not** prove that every low-level message emitted during a recovery/backfill workflow has one immutable class. The source-level qualification below matters.

### H/P — built-in profiles change resource allocations without changing the existence of the repair obligation

For Reef's built-in profiles, the mClock reference documents different allocations for the service buckets.

The default **`balanced`** profile gives equal 50% reservations to client and background-recovery work, while background best-effort receives the minimum reservation and a lower limit.

The **`high_client_ops`** profile shifts more reservation toward client operations and explicitly describes the tradeoff as slower recoveries.

The **`high_recovery_ops`** profile shifts more reservation toward background recovery and is described as something an administrator may enable temporarily to speed recovery during non-peak hours.

The retained PG state that says repair is needed is not thereby rewritten into a different object. What changes is the scheduler policy governing access to OSD execution capacity.

Thus, for this bounded baseline:

```text
repair debt exists
    != selected scheduler profile

selected scheduler profile changes
    != repair debt discharged
```

### H/P — `high_recovery_ops` must not be paraphrased as “all maintenance gets faster”

The profile name is easy to over-read. Reef's own client-type table places backfill, scrub, snap trim, and PG deletion in **background best-effort**, while `high_recovery_ops` explicitly raises the allocation of **background recovery**.

Therefore the safe statement is:

> `high_recovery_ops` increases the documented allocation for the background-recovery service class.

The stronger statement:

> “`high_recovery_ops` elevates every kind of maintenance operation equally”

is not supported by this interface.

This is an important terminology boundary because Case 142 contains both recovery and backfill paths, both of which can restore replica state, yet the scheduler vocabulary does not flatten them into one class.

### H/P — reservation, weight, and limit are scheduling controls, not durability levels

The Reef configuration reference identifies **reservation**, **weight**, and **limit** as mClock's lower-level resource-control parameters.

The mClock/WPQ study in the Ceph source tree explains their intended scheduler meaning more directly: service types receive at least their reservation, share excess capacity according to weight, and are bounded by limit, assuming the OSD's capacity is known sufficiently well.

The same study states that mClock factors operation cost into scheduling/dequeue calculations; higher modeled cost can leave an operation in the queue longer.

These fields therefore describe **resource allocation and dequeue behavior**. They do not encode:

- how many valid replicas currently exist;
- whether a PG is `clean`;
- whether the destination passes `backfillfull`;
- whether a required source object is readable;
- whether the maintenance operation has completed.

Hence:

`QoS reservation != replica reservation != retained replica`

The shared word “reservation” across scheduling/resource contexts must not be treated as one historical concept.

### H/P — mClock takes control away from older sleep-based pacing when a profile is active

The Reef mClock reference states that when an mClock profile is active, several recovery/scrub/delete/snap-trim sleep options are set to zero. The stated reason is to let the mClock scheduler determine when the next operation is selected from the operation queue and transferred to the operation sequencer.

This establishes a real control-authority handoff:

```text
legacy sleep pacing
    -> disabled under mClock profile

mClock queue policy
    -> determines dequeue timing relation
```

The conclusion is not that every other recovery/backfill concurrency control disappears. In fact, the same document separately discusses `osd_max_backfills` and `osd_recovery_max_active*`.

### H/P — mClock does not make legacy recovery/backfill concurrency controls vanish

The Reef reference says built-in profiles override several recovery/backfill options to mClock defaults:

- `osd_max_backfills`;
- `osd_recovery_max_active`;
- `osd_recovery_max_active_hdd`;
- `osd_recovery_max_active_ssd`.

Changing those values while mClock is active is gated by `osd_mclock_override_recovery_settings`, which defaults to false.

So the scheduling surface is layered even within the execution domain:

```text
mClock service share / dequeue policy
    != max concurrent recovery/backfill controls
```

and:

`profile selected != operator may freely mutate every subordinate limit`

The built-in profile can retain authority over the effective defaults unless the explicit override gate is enabled.

### H/P — the source exposes explicit scheduler classes

In `v18.2.0` `src/osd/scheduler/OpSchedulerItem.h`, Ceph defines:

```text
background_recovery
background_best_effort
immediate
client
```

as `op_scheduler_class` values.

This source-level representation corresponds to the documentation's broad service-class model, but it also exposes an important qualification: classification of recovery-related queueables can depend on **priority**, not only on an English operation name.

`PGOpQueueable::priority_to_scheduler_class()` maps sufficiently high priority to `immediate`, lower recovery-priority work to `background_recovery`, and lower-priority work to `background_best_effort`.

`PGRecovery` and `PGRecoveryContext` use that mapping. `PGRecoveryMsg` also uses priority-derived classification, and its recognized recovery-message set includes push/pull as well as backfill/backfill-remove/scan messages.

Therefore:

```text
documentation-level maintenance category
    != every constituent message's immutable scheduler class
```

and:

```text
operation type
    + priority / source path
    -> effective queue class
```

The latter is an engineering reconstruction from the source. It is intentionally narrower than a claim that every backfill-related message is always background best-effort.

### H/P — some maintenance queueables are explicitly best-effort

The same `v18.2.0` header gives direct class implementations for several queueable maintenance operations:

- PG scrub queueables use `background_best_effort`;
- PG deletion uses `background_best_effort`;
- snap-trim queueables use `background_best_effort`.

This corroborates the user-facing statement that the best-effort bucket is not merely a documentation fiction.

Again, this is not a claim that all sub-operations generated by those workflows can never be reclassified elsewhere in the implementation.

### H/P — queue policy and runtime override state can have different restart lifetimes

The Reef mClock reference distinguishes central configuration commands from **temporary** runtime overrides.

It documents `ceph config set ...` / central config database operations for ordinary profile configuration. Separately, it documents `injectargs` and daemon-local configuration overrides as **ephemeral** and explicitly says those changes are lost when the OSD restarts.

This gives a bounded maintenance-policy persistence contrast:

```text
configured mClock policy
    != ephemeral daemon-local override

runtime override effective now
    != override survives OSD restart
```

This file does not infer the exact database replication, fsync, or crash-atomicity protocol of the Ceph configuration subsystem. It uses only the documented restart-lifetime distinction.

---

## Engineering reconstruction

### E — repair has both an admission problem and an execution-share problem

Case 142's capacity evidence can now be extended into a longer state pipeline:

```text
redundancy debt exists
    -> source/currentness conditions allow repair
    -> placement identifies a candidate destination
    -> fullness / projected-capacity policy admits the attempt
    -> local / remote reservation path admits the attempt
    -> operations enter scheduler classes
    -> scheduler/concurrency policy allocates execution opportunity
    -> object movement / reconstruction progresses
    -> configured redundancy is restored
    -> PG may become clean
```

No arrow is an identity relation.

The most important new counterexample is:

> **destination capacity admission does not grant unlimited execution authority.**

A repair can be capacity-admissible and still progress slowly because foreground/client work and other background classes compete for scheduler resources.

Conversely, a profile favoring recovery does not override a destination that is rejected by the fullness gate.

Thus:

```text
repair priority / QoS
    != repair admission
```

in both directions.

### E — “repair priority” is multidimensional in Ceph

A single scalar word `priority` hides several relations:

1. whether maintenance is admitted at all;
2. which scheduler class a queueable enters;
3. which mClock profile is active;
4. the reservation/weight/limit for that class;
5. separate recovery/backfill concurrency limits;
6. operation/message priority that can affect class selection;
7. modeled operation cost and queue timing.

For this case, the useful project term is **execution authority**: after the system recognizes and admits a repair obligation, policy still controls when/how strongly its constituent operations may consume resources.

“Execution authority” is project vocabulary, not a Ceph historical term.

### E — redundancy semantics and scheduler semantics are orthogonal enough to require separate evidence

Recovery and backfill can both contribute to restoring replica state, but the Reef interface classifies them differently for QoS purposes and the source can classify constituent operations by priority.

Therefore:

`same retention objective != same execution class`

and:

`same scheduler class != same retention objective`

The latter follows because background best-effort also includes scrub, snap trim, and PG deletion, which do not all represent the same redundancy-restoration operation.

This is exactly why mClock belongs as a **separate** Case 142 evidence slice rather than being inferred from the existing retry/capacity material.

### E — retained policy can shape maintenance without becoming retained payload

The active mClock profile and its effective resource-control parameters can persist long enough to govern many individual operations. Yet they are neither object payload nor replica currentness.

They are control state **about how future maintenance and foreground work may consume execution resources**.

This extends the repository's maintenance-control decomposition:

```text
retained payload/currentness relation
    != retained capacity-admission policy
    != retained scheduler policy
    != per-operation queue state
```

The persistence horizons of these layers are not assumed identical.

### E — a policy can remain semantically valid while its performance effect depends on measured capacity

The Reef reference computes profile allocations from OSD capacity, including automated capacity determination and possible fallback/manual override.

Therefore the same profile name is not itself a fixed IOPS amount:

`profile identity != absolute execution throughput`

The scheduler policy may be the same while the capacity basis differs across OSDs or changes through configuration.

This is a bounded policy/measurement distinction, not a benchmark claim.

---

## Functional analogy

### A — Case 136 MegaRAID/PERC rebuild rate

Case 136 shows a controller-side rebuild priority policy that determines how aggressively admitted rebuild work competes with foreground I/O.

Case 142 now has two separate distributed controls:

```text
fullness / projected-capacity policy
    -> whether repair/backfill is admitted

mClock / scheduler policy
    -> how admitted queueable work competes for OSD execution resources
```

The functional lesson is:

`maintenance obligation != maintenance admission != maintenance execution priority`

No LSI/MegaRAID → Ceph genealogy is claimed, and no equivalence is asserted between one controller's rebuild-rate knob and Ceph's service-class scheduler.

### A — Synthesis 26 / maintenance-control-state horizons

The repository's maintenance-control synthesis distinguishes retained policy, runtime state, and shorter-lived execution/retry state. Reef provides a concrete distributed example in which the fullness policy, mClock profile, episode flags, retry event, queue class, and individual operation do not have one common lifetime.

This is a functional comparison only. The synthesis is not historical evidence for Ceph.

---

## Philosophical interpretation — bounded

The technical fact is narrow: long-term availability of a replicated object can depend not only on having enough surviving source state and free destination capacity, but also on granting maintenance work enough **execution opportunity** to restore redundancy.

A useful project interpretation is therefore:

> **retention infrastructure includes not only places where replacement embodiments may be created, but also time/resource claims through which maintenance is allowed to create them.**

This does not make scheduler tokens, IOPS shares, or empty capacity “memory” in the same sense as object replicas. They are conditions governing the future re-embodiment of retained state.

No Stieglerian, Heideggerian, or media-theoretical vocabulary is attributed to Ceph developers.

---

## Explicitly rejected / unsupported claims

- **X — Reef invented mClock or dmClock.** This slice uses a Reef baseline and makes no invention-priority claim.
- **X — capacity admission and mClock scheduling are the same policy.** They answer different questions and live under different controls.
- **X — passing `backfillfull` guarantees prompt backfill completion.** Scheduler contention, concurrency limits, failures, map changes, and later admission changes remain possible.
- **X — a high recovery profile overrides `*_toofull`.** No such relation is established; capacity admission remains separate.
- **X — `high_recovery_ops` elevates all maintenance equally.** Reef documents backfill/scrub/snap trim/PG deletion as background best-effort rather than background recovery.
- **X — every low-level backfill-related message is permanently classified as background best-effort.** `PGRecoveryMsg` classification is priority-derived and its recovery-message set includes backfill-related message types.
- **X — documentation-level service type uniquely determines every constituent operation's source-level scheduler class.** The source exposes priority-sensitive classification.
- **X — mClock reservation is the same thing as Ceph recovery reservation.** One is scheduler resource allocation; the other is a maintenance admission/concurrency mechanism.
- **X — reservation/weight/limit values are durability probabilities or replica counts.** They are scheduler controls.
- **X — selecting a profile guarantees a particular measured throughput.** Actual performance depends on capacity calibration, operation costs, workload competition, shards, backend throttles, and other implementation conditions.
- **X — the mClock/WPQ study's development-profile table is the Reef profile contract.** This evidence uses the Reef config reference for Reef defaults and treats the study as a separate historical/experimental witness.
- **X — `balanced` means equal completion time for client and recovery work.** Equal documented reservation does not imply equal workload, cost, latency, or completion time.
- **X — mClock disables every recovery/backfill control.** The Reef documentation retains separate max-backfill/recovery-active controls.
- **X — an ephemeral runtime override is persistent policy.** The Reef reference says it is lost on OSD restart.
- **X — central Ceph configuration persistence is proven crash-atomic by this slice.** Only the documented runtime-versus-central configuration lifetime distinction is used.
- **X — scheduler-class state survives OSD restart exactly as queued.** No such queue-state persistence claim is made.
- **X — a maintenance operation that gets scheduler service must eventually complete.** Scheduling opportunity is not a completion guarantee.
- **X — completed repair proves old embodiments were sanitized.** No physical-erasure claim follows from redundancy restoration.
- **X — mClock policy is object payload or object currentness metadata.** It is control state governing resource allocation.
- **X — the broader scheduler genealogy belongs entirely in this case.** Release-by-release evolution and algorithm history remain primarily `computing-archaeology` work.

---

## Claim ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| Reef mClock exposes client, background-recovery, and background-best-effort service buckets | `H/P` | `mclock-config-ref.rst` v18.2.0 |
| Reef documentation places internal recovery in background recovery and backfill/scrub/snap trim/PG deletion in background best effort | `H/P` | same |
| Reef built-in profiles allocate the service buckets differently | `H/P` | same |
| `high_client_ops` trades recovery performance for client allocation; `high_recovery_ops` raises background-recovery allocation | `H/P` | same |
| built-in profiles own/lock low-level mClock parameters and gate overrides of recovery/backfill concurrency settings | `H/P` | same |
| mClock-active mode disables several legacy sleep pacing options so dequeue timing is scheduler-owned | `H/P` | same |
| `op_scheduler_class` contains background recovery, background best effort, immediate, and client classes | `H/P` | `OpSchedulerItem.h` v18.2.0 |
| recovery queueables/messages can be scheduler-classified by priority | `H/P` | same |
| some maintenance queueables are explicitly background best effort | `H/P` | same |
| temporary daemon-local mClock overrides are documented as lost on OSD restart | `H/P` | Reef mClock config reference |
| capacity admission and execution-share scheduling are independent control layers | `E` | composition of Case 142A–C + mClock sources |
| same redundancy-restoration objective does not imply one scheduler class | `E` | documentation + source qualification |
| same scheduler class does not imply one retention objective | `E` | best-effort bucket contains heterogeneous maintenance |
| scheduler profile identity is not an absolute throughput quantity | `E` | profile + capacity-calibration relation |
| mClock selection proves durability, completion, or sanitization | `X` | outside source scope |

---

## Related-repository check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Ceph mClock recovery backfill` found no dedicated module to reuse in this round.

The division of labor is therefore:

- **`technical-retention`** keeps the bounded seam needed by Case 142: repair debt → capacity admission → scheduler class/resource allocation → completion are distinct retention-maintenance relations;
- **`computing-archaeology`** should own the broad dmClock/mClock history, pre-Pacific/Pacific/Quincy/Reef scheduler evolution, benchmark history, and implementation-performance archaeology if those are developed later.

No generic Ceph scheduler history is reproduced here beyond what is needed to establish the retention boundary.

---

## Remaining evidence debt

After this slice, the earlier broad “inspect mClock/work-class interaction” debt is closed for the **Reef `v18.2.0` bounded baseline**.

Still open:

1. release-to-release mClock/service-class genealogy, especially pre-Pacific → Pacific → Quincy → Reef, primarily for `computing-archaeology`;
2. exact classic-OSD versus Crimson-OSD class/queue equivalence and divergence;
3. named production traces showing degraded/backfill workloads under different profiles;
4. controlled experiments combining `backfillfull`/projected-capacity gating with mClock profile changes;
5. OSD restart experiments separating persistent configuration from lost queue/runtime state;
6. workload-specific latency/throughput effects under mixed client/recovery/backfill pressure;
7. later scheduler fixes or starvation-avoidance changes, which must not be projected backward into Reef.

The bounded conclusion now paid for is narrower and defensible:

> **Ceph Reef separates the authority to admit repair/backfill from the authority to allocate execution resources to admitted maintenance, and its scheduler further distinguishes service classes rather than treating all retention maintenance as one undifferentiated priority.**
