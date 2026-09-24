# Evidence 142F — Ceph Reef backfill rejection versus revocation authority

**Status:** `bounded deepening complete`  
**Case:** [`../cases/142-ceph-reef-capacity-gated-recovery.md`](../cases/142-ceph-reef-capacity-gated-recovery.md)  
**Baseline:** Ceph `v18.2.0` / Reef; the Case-142 source baseline remains the released tag resolving to commit `5dd24139a1eada541a3bc16b6941c5dde975e26d`.  
**Bounded question:** after a remote OSD has accepted a backfill reservation and the primary has begun backfilling, does the earlier capacity admission remain irrevocably valid until the backfill finishes?

## Evidence boundary

Earlier Case-142 evidence establishes:

- a repair/backfill obligation can survive a capacity rejection;
- a rejected reservation attempt is unwound and retried later;
- projected backfill bytes can participate in capacity admission;
- live `_TOOFULL` episode bits are not themselves the restart authority for the repair obligation;
- mClock scheduling/resource allocation is a layer separate from capacity admission.

One boundary remained under-described: **what if capacity ceases to be acceptable after the remote reservation has already been granted and backfill is in progress?**

Reef source distinguishes two different too-full messages and state-machine paths:

```text
REJECT_TOOFULL
    = refuse the reservation request before the backfill has authority to run

REVOKE_TOOFULL
    = withdraw an already-granted backfill reservation because the target is now too full
```

The second path matters for technical retention because it shows that successful maintenance admission is not necessarily a permanent entitlement to finish the current embodiment of the repair.

Project reconstruction:

```text
repair obligation
    != one reservation attempt
    != initial admission success
    != continuing execution authority
    != repair completion
```

The phrase **continuing execution authority** is project vocabulary. Ceph's source vocabulary is `REQUEST`, `GRANT`, `REJECT_TOOFULL`, `REVOKE_TOOFULL`, reservation, backfill, and the associated peering events/states.

This slice is intentionally narrow. It is not a history of Ceph recovery reservations, not a full account of partial-backfill cleanup, not a crash-consistency experiment, and not a claim about Crimson OSD.

---

## Primary source ladder

| Source | Version | Evidence class | Use here |
| --- | --- | --- | --- |
| Ceph `src/messages/MBackfillReserve.h` | `v18.2.0` | `H/P` | protocol-level distinction among request, grant, rejection, release, too-full revocation, and generic revocation; compatibility encoding boundary |
| Ceph `src/osd/PeeringState.cc` | `v18.2.0` | `H/P` | initial reservation refusal, in-flight too-full revocation, primary-side cancellation, `_TOOFULL` state, and delayed retry |
| Ceph `qa/tasks/backfill_toofull.py` | `v18.2.0` | `H/P` test artifact | project-maintained end-to-end exercise of capacity-blocked, later-admitted, interrupted, and eventually-clean backfill; not a direct `REVOKE_TOOFULL` injection |
| Existing Case-142 evidence | repository-grounded | `H/P + E` | prior capacity, retry, projected-accounting, restart, and scheduler boundaries that this slice must not duplicate |

Primary anchors:

- `MBackfillReserve.h`: <https://github.com/ceph/ceph/blob/v18.2.0/src/messages/MBackfillReserve.h>
- `PeeringState.cc`: <https://github.com/ceph/ceph/blob/v18.2.0/src/osd/PeeringState.cc>
- `qa/tasks/backfill_toofull.py`: <https://github.com/ceph/ceph/blob/v18.2.0/qa/tasks/backfill_toofull.py>
- retry-state deepening: [`142-ceph-reef-source-retry-state-horizon-deepening.md`](142-ceph-reef-source-retry-state-horizon-deepening.md)
- projected-capacity deepening: [`142-ceph-reef-projected-backfill-admission-accounting-deepening.md`](142-ceph-reef-projected-backfill-admission-accounting-deepening.md)
- restart-state deepening: [`142-ceph-reef-restart-reporting-vs-operative-state-deepening.md`](142-ceph-reef-restart-reporting-vs-operative-state-deepening.md)
- mClock scheduling deepening: [`142-ceph-reef-mclock-maintenance-scheduling-boundary-deepening.md`](142-ceph-reef-mclock-maintenance-scheduling-boundary-deepening.md)

A fresh companion-repository search for `backfill_toofull` in `tmzncty/computing-archaeology` found no dedicated reusable packet. The broad reservation/scheduler genealogy remains routed there rather than being recreated here.

---

## Historical / implementation record

### H/P — the wire/message model explicitly distinguishes refusal from revocation

`MBackfillReserve` in Reef defines six message types:

```text
REQUEST
GRANT
REJECT_TOOFULL
RELEASE
REVOKE_TOOFULL
REVOKE
```

The source comments distinguish their direction and meaning.

For `REJECT_TOOFULL`, the remote side tells the primary, in effect, that it is too full and the primary should try later.

For `REVOKE_TOOFULL`, the remote side tells the primary that it is too full and that the already-running backfill must stop.

This is direct implementation evidence that Reef models at least two capacity-failure moments:

```text
capacity unacceptable before execution authority is granted
    !=
capacity becomes unacceptable after execution authority was granted
```

The distinction is not invented by this repository; it is encoded in the message type itself.

### H/P — initial too-full rejection occurs before a remote backfill reservation is granted

On the replica/target path, `RepNotRecovering::react(const RequestBackfillPrio&)` first calls `try_reserve_recovery_space(...)`.

If that reservation-space check fails, the code posts `RejectTooFullRemoteReservation()` instead of establishing the remote reservation.

The target-side state machine then converts that failure into the corresponding rejection path and returns to `RepNotRecovering` after releasing/canceling reservation state.

On the primary side, `WaitRemoteBackfillReserved::react(const RemoteReservationRejectedTooFull&)`:

- sets `PG_STATE_BACKFILL_TOOFULL`;
- invokes `retry()`;
- leaves the current remote-reservation attempt.

`retry()`:

- cancels the local background-I/O reservation;
- sends `RELEASE` to remotes whose reservations had already been acquired earlier in the sequence;
- clears `PG_STATE_BACKFILL_WAIT`;
- publishes updated PG stats;
- schedules a new `RequestBackfill()` after `osd_backfill_retry_interval`.

Thus a pre-start capacity refusal is not represented as a half-open reservation left waiting indefinitely. The current attempt is deliberately unwound and a future attempt is scheduled.

### H/P — an already-granted backfill can later be revoked for capacity

The more important new boundary is visible after the replica has already entered the recovering/backfill-serving state.

`RepRecovering::react(const BackfillTooFull&)`:

1. calls `unreserve_recovery_space()`;
2. sends the primary `MBackfillReserve::REVOKE_TOOFULL`.

The message therefore originates from a target that had already progressed beyond the initial `REQUEST`/`GRANT` decision.

On the primary, `Backfilling::react(const RemoteReservationRevokedTooFull&)`:

1. sets `PG_STATE_BACKFILL_TOOFULL`;
2. clears `PG_STATE_BACKFILLING`;
3. calls `cancel_backfill()`;
4. schedules a future `RequestBackfill()` after `osd_backfill_retry_interval`;
5. transitions to `NotBackfilling`.

The source-level relation is therefore:

```text
remote reservation granted
    -> backfill running
    -> target reports BackfillTooFull
    -> target withdraws reservation
    -> primary stops current backfill episode
    -> PG reports backfill_toofull
    -> later RequestBackfill is scheduled
```

This is stronger than the earlier Case-142 result that “a denied reservation can be retried.” It establishes that **capacity admission can be revoked after maintenance has already begun**.

### H/P — initial rejection and in-flight revocation converge on retry, but they are not the same event

Both paths can lead to `PG_STATE_BACKFILL_TOOFULL` plus a delayed `RequestBackfill()`, but their histories are different:

```text
path A — initial rejection
REQUEST
    -> capacity/reservation check fails
    -> REJECT_TOOFULL
    -> no Backfilling state for this grant
    -> unwind attempt
    -> retry later

path B — in-flight revocation
REQUEST
    -> GRANT
    -> Backfilling
    -> later target-side BackfillTooFull
    -> REVOKE_TOOFULL
    -> cancel current backfill
    -> retry later
```

Therefore a later monitor-visible `backfill_toofull` state does not, by itself, encode whether the current episode failed **before** execution started or **after** execution had already begun.

That is a source-derived observability boundary, not a claim that the two paths are operationally indistinguishable in logs or traces.

### H/P — successful admission is conditionally valid, not a one-time permanent certificate

The existence of `REVOKE_TOOFULL` in the same protocol family as `GRANT` establishes a limited but important contract:

```text
GRANT at time t0
    != proof that the target remains admissible at every later time t1
```

The source supports continuing capacity enforcement strongly enough to terminate an active backfill.

Do not strengthen this into a claim that every occupancy change is continuously rechecked at every byte transfer. This evidence establishes the **revocation path**, not its exact checking cadence or all triggers.

### H/P — current semantics can collapse across the older-peer compatibility boundary

`MBackfillReserve::encode_payload()` contains a compatibility path for peers without `RECOVERY_RESERVATION_2`.

In that path, current message types `RELEASE`, `REVOKE_TOOFULL`, and `REVOKE` are encoded as the older `REJECT_TOOFULL` value.

This yields a separate protocol-version boundary:

```text
current local semantic distinction
    != distinction necessarily preserved on the wire to an older peer
```

The safe conclusion is only that Reef retains a compatibility encoding that can collapse several newer meanings into the older rejection representation.

This file does **not** use that code to reconstruct the full historical introduction date of each message type, Luminous-era behavior, or the complete negotiation genealogy. Those belong in implementation archaeology if later needed.

### H/P — upstream QA shows capacity-blocked backfill is treated as a nonterminal maintenance condition

The Reef tree's `qa/tasks/backfill_toofull.py` constructs an erasure-coded pool, creates a capacity condition that should force `backfill_toofull`, revives the target, and waits for the PG to enter that state.

The task then changes the fullness ratios so that the target should be able to backfill, waits for `backfilling`, deliberately marks the target down to interrupt that backfill, clears the maintenance-pause flags, and finally waits for the cluster to become clean.

This is useful project-maintained test evidence for a broader state relation:

```text
blocked maintenance episode
    -> later admitted maintenance
    -> interruption
    -> later convergence to clean
```

It also reinforces that `backfill_toofull` is not treated as an absorbing data-loss verdict.

But this QA task does **not** directly inject the exact in-flight `REVOKE_TOOFULL` event because of a capacity rise while the target stays up. It therefore cannot substitute for an explicit revocation-path fault/trace experiment.

---

## Engineering reconstruction

### E — maintenance admission is revocable

The strongest bounded reconstruction from the source is:

> **A successful backfill reservation grants present execution authority, not an irrevocable right to complete the whole repair under arbitrary later capacity conditions.**

In project notation:

```text
repair debt
    -> attempt admitted
    -> execution begins
    -> admission condition later fails
    -> execution authority withdrawn
    -> repair debt survives
    -> new attempt may be made later
```

Call this **revocable maintenance admission** if a compact project term is needed.

That phrase is not Ceph vocabulary and must not be presented as a historical term.

### E — repair obligation can outlive both refusal and withdrawal

Case 142 previously showed:

```text
reservation rejected
    != repair obligation discharged
```

The new source path extends that statement:

```text
reservation granted
    != repair obligation discharged

backfill started
    != repair obligation discharged

backfill canceled after revocation
    != repair obligation discharged
```

Only successful restoration of the required redundancy relation can close the maintenance debt relevant to this case.

The exact object-level criterion for “successfully restored” remains governed by Ceph's normal recovery/backfill/currentness machinery and is not re-derived in this file.

### E — “work began” is not a completion certificate

A monitor/operator trace that proves the PG entered `backfilling` proves that a backfill episode ran. It does not prove:

- the destination remained admissible throughout the run;
- the backfill reached its completion transition;
- configured redundancy was restored;
- the PG became `clean`.

Thus:

```text
maintenance activity observed
    != maintenance completion authority
```

This complements other repository cases in which progress/activity telemetry is weaker than a terminal completion relation.

### E — a capacity threshold participates in both admission and continuing execution authority

Earlier evidence already treated fullness policy as an admission gate.

The revocation path shows a second role:

```text
capacity policy / state
    -> initial admission decision
    + continuing authority to keep the backfill reservation
```

The same broad resource condition can therefore constrain maintenance at more than one temporal boundary.

This does not mean the exact same function or threshold calculation is called at every boundary; the source slice establishes the control relation, not every lower-level predicate implementation.

### E — retry reconstructs another attempt rather than preserving one continuous transaction

Both initial rejection and in-flight revocation terminate current reservation/execution state and arrange a later `RequestBackfill()`.

The project reconstruction is:

```text
one attempt dies
    while
repair obligation remains
    -> later attempt is re-entered
```

That is different from freezing one transaction object in place until resources improve.

This distinction matters for retention analysis because the continuity lies in the larger repair relation, not necessarily in continuity of the same reservation instance.

### E — compatibility can preserve the obligation while losing diagnostic resolution

When newer message distinctions collapse to `REJECT_TOOFULL` for older peers, the protocol can retain enough semantics to stop/refuse work while sacrificing some of the newer distinction between release/revoke causes.

A bounded reconstruction is:

```text
maintenance-control compatibility
    may preserve a safe coarse action
    while reducing causal / phase resolution
```

This is not a claim about all mixed-version Ceph correctness. It is only the semantic consequence visible in this one encoding branch.

---

## Functional analogy

### A — Case 142 mClock scheduling

The existing mClock slice establishes:

```text
capacity admission
    != scheduler class / resource share
```

The present slice adds another independent distinction:

```text
initial admission success
    != continuing permission to execute until completion
```

Together, a repair can be:

- not admitted at all;
- admitted but scheduled slowly;
- admitted and running, then revoked;
- completed.

These are different control relations even though all concern the same high-level repair obligation.

### A — Case 136 rebuild-rate policy

Case 136 separates a RAID-controller rebuild obligation from how aggressively rebuild competes for resources.

Case 142 now adds a distributed counterexample to any simple “once rebuild/repair starts, it owns its resource until done” model: Ceph can explicitly revoke the current backfill reservation for capacity.

This is a functional analogy only. No controller-to-Ceph genealogy or implementation equivalence is claimed.

### A — Case 111 managed-Flash maintenance interruption

Case 111's eMMC BKOPS/HPI evidence shows a different reason why background maintenance execution need not be continuous: higher-priority foreground activity can interrupt generic background work.

The bounded comparison is:

```text
maintenance obligation
    != one uninterrupted execution episode
```

The causes differ:

- eMMC HPI is foreground-priority interruption;
- Ceph `REVOKE_TOOFULL` is capacity/reservation withdrawal.

No protocol, product, or historical genealogy is asserted.

---

## Philosophical interpretation

The exact technical fact that creates the conceptual problem is narrow:

> The repair relation can remain normatively/operationally owed even when the currently authorized execution episode is refused, revoked, canceled, and later reconstructed.

This sharpens one aspect of technical retention without turning scheduler or reservation state into “memory” in the same sense as object payload.

The useful interpretation is that persistence may rely on **continuity of an obligation relation across discontinuous embodiments of maintenance work**.

What survives is not necessarily:

- one continuously running repair action;
- one persistent reservation object;
- one uninterrupted transfer.

What must remain recoverable is enough current state, policy, placement, and repair relation to make a later valid attempt possible.

The interpretation stops there. It does not establish a general philosophy of obligation, and it does not imply that all interrupted processes are forms of retention.

---

## Explicitly rejected / unsupported claims

- **Not established:** `REVOKE_TOOFULL` is the only way an active backfill can be canceled.
- **Not established:** every increase in target occupancy immediately triggers `BackfillTooFull`.
- **Not established:** the exact interval or predicate with which an active target rechecks capacity.
- **Not established:** partial object transfers are atomically rolled back when backfill is revoked.
- **Not established:** partially copied object state is physically erased after cancellation.
- **Not established:** retry is idempotent under every object/version race; this slice does not inspect the full backfill object protocol.
- **Not established:** the scheduled retry event itself survives an OSD process crash.
- **Not established:** `PG_STATE_BACKFILL_TOOFULL` itself is restored as live state across restart; Evidence 142E shows the opposite boundary for the classic OSD state bit.
- **Not established:** a later retry succeeds if capacity remains unacceptable.
- **Not established:** the QA task directly exercises an in-flight capacity-triggered `REVOKE_TOOFULL` message.
- **Not established:** upstream QA is a production incident trace.
- **Not established:** the current classic-OSD path can be generalized unchanged to Crimson OSD.
- **Not established:** mixed-version compatibility preserves all newer diagnostic distinctions.
- **Not established:** the compatibility branch proves the first release in which rejection/revocation semantics changed.
- **Not established:** capacity admission, mClock scheduling, and reservation ownership are one policy layer.
- **Not established:** `backfill_toofull` proves existing payload is lost or unreadable.
- **Not established:** a completed backfill alone proves every later integrity/scrub obligation is satisfied.

---

## Related-repository routing

Fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `backfill_toofull` found no dedicated reusable packet.

The division of labor remains:

- **technical-retention:** repair-obligation continuity, admission/revocation authority, retry/reconstruction, and the distinction between present execution permission and restored redundancy;
- **computing-archaeology:** first-introduction history of reservation message types, Luminous compatibility evolution, release/backport matrices, broader recovery scheduler genealogy, and performance history.

Do not turn this file into a release-by-release Ceph reservation history.

---

## Remaining bounded evidence debt

The next useful slices are now more precise.

### 1. In-flight `REVOKE_TOOFULL` trace

Create or locate a classic-OSD Reef test where:

1. a target grants backfill;
2. the PG is observed in `backfilling`;
3. target capacity crosses the relevant condition while the target remains alive;
4. `REVOKE_TOOFULL` is observed;
5. the primary leaves `backfilling`, reports `backfill_toofull`, and later retries.

This would close:

```text
source path exists
    != measured path/timing under induced capacity change
```

### 2. Partial-backfill residue semantics

Inspect exactly what `cancel_backfill()` and the lower backfill backend retain, discard, or rediscover after revocation.

Target boundary:

```text
execution canceled
    != partial transferred state rolled back
    != partial state reusable on retry
```

### 3. Restart during the revoked episode

Combine this slice with Evidence 142E's restart result: crash the primary or target after revocation but before the delayed retry and identify which durable/current relations cause the next attempt.

### 4. Crimson comparison

Inspect Crimson independently before generalizing the classic OSD reject/revoke transition structure.

### 5. Production evidence

Find a named public operational trace where an already-running backfill is stopped for capacity rather than merely refused before starting.

Broader message-history genealogy remains routed to `computing-archaeology`.
