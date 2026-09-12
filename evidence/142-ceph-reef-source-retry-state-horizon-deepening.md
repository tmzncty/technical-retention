# Evidence 142B — Ceph Reef source-level capacity-gated retry state and retention horizons

**Status:** grounded  
**Case:** [`../cases/142-ceph-reef-capacity-gated-recovery.md`](../cases/142-ceph-reef-capacity-gated-recovery.md)  
**Baseline:** Ceph `v18.2.0` tag, released August 2023; annotated tag resolves to commit `5dd24139a1eada541a3bc16b6941c5dde975e26d`.  
**Bounded question:** once capacity policy blocks recovery or backfill, what source-level state survives the failed admission attempt, what is deliberately cleared, and what causes the system to try again?

## Evidence boundary

This deepening does **not** attempt a release-by-release history of Ceph recovery reservations. It freezes one released Reef implementation and asks how three different kinds of maintenance-control state coexist:

1. cluster policy that determines whether a destination is too full;
2. placement-group state that reports the current capacity-blocked episode;
3. a shorter retry obligation represented by a scheduled future peering event.

The slice also checks upstream standalone QA because it is useful evidence that the named states were intentionally exercised by the project. Those tests are not production traces and do not establish real-cluster failure rates or latency.

No claim is made here that `recovery_toofull` or `backfill_toofull` first appeared in Reef, that their in-memory flags survive an OSD daemon restart, or that the same transition graph applies unchanged before or after Reef.

## Source ladder

| Source | Version / date | Evidence class | Use here |
|---|---|---|---|
| Ceph `src/osd/PeeringState.cc` | `v18.2.0` / commit `5dd24139...` | `H/P` | exact too-full reactions, state-bit changes, retry-event scheduling, reservation release, and transition boundaries |
| Ceph `src/common/options/osd.yaml.in` | `v18.2.0` | `H/P` | `osd_recovery_retry_interval` and `osd_backfill_retry_interval` defaults and descriptions |
| Ceph `qa/standalone/osd/osd-recovery-space.sh` | `v18.2.0` | `H/P` | project test deliberately drives and asserts `recovery_toofull` |
| Ceph `qa/standalone/osd-backfill/osd-backfill-space.sh` | `v18.2.0` | `H/P` | project test deliberately drives and checks capacity-blocked backfill behavior |
| Reef Recovery Reservation / PG State / Health documentation | Reef docs | `H/P` | user/developer-facing semantics already grounded in Evidence 142A |

Primary anchors:

- tag: <https://github.com/ceph/ceph/releases/tag/v18.2.0>
- `PeeringState.cc`: <https://github.com/ceph/ceph/blob/v18.2.0/src/osd/PeeringState.cc>
- OSD options: <https://github.com/ceph/ceph/blob/v18.2.0/src/common/options/osd.yaml.in>
- recovery-space QA: <https://github.com/ceph/ceph/blob/v18.2.0/qa/standalone/osd/osd-recovery-space.sh>
- backfill-space QA: <https://github.com/ceph/ceph/blob/v18.2.0/qa/standalone/osd-backfill/osd-backfill-space.sh>
- prior documentation grounding: [`142-ceph-reef-capacity-gated-recovery-grounding.md`](142-ceph-reef-capacity-gated-recovery-grounding.md)

## Historical / source-level record

### 1. Recovery too-full is a retryable state, not an absorbing failure

In the Reef source, the recovery path checks fullness before acquiring the local recovery reservation. When the check produces `RecoveryTooFull`, `WaitLocalRecoveryReserved::react(const RecoveryTooFull&)`:

- sets `PG_STATE_RECOVERY_TOOFULL`;
- schedules a future `DoRecovery()` peering event after `osd_recovery_retry_interval`;
- leaves the current recovery-reservation state rather than entering `Recovering`.

The successful `Recovering` entry path clears both `PG_STATE_RECOVERY_WAIT` and `PG_STATE_RECOVERY_TOOFULL` before setting `PG_STATE_RECOVERING`.

This is source-level support for:

`recovery gate active now != recovery obligation abandoned`

It is **not** proof that a retry eventually succeeds. If capacity remains unacceptable, a later attempt can be gated again.

### 2. Backfill rejection records the episode and reconstructs the retry path

`WaitRemoteBackfillReserved::react(const RemoteReservationRejectedTooFull&)` sets `PG_STATE_BACKFILL_TOOFULL`, invokes `retry()`, and transitions out of the remote-reservation wait state.

The `retry()` path first cancels the local background-I/O reservation, cancels previously acquired remote reservations, and schedules a future `RequestBackfill()` event after `osd_backfill_retry_interval`.

The important state-machine boundary is therefore not merely “sleep and continue the same transaction.” The current reservation attempt is unwound and a later event asks the peering machine to enter the backfill path again.

Hence:

`reservation rejection != suspended reservation transaction != forgotten repair need`

### 3. Capacity-blocked PG flags are episode state, not the fullness policy itself

The source explicitly clears `PG_STATE_RECOVERY_TOOFULL` and `PG_STATE_BACKFILL_TOOFULL` on relevant lifecycle/reset paths. Successful entry into active recovery/backfill paths also clears the waiting/too-full reporting state appropriate to that path.

That means a PG state bit can disappear because the peering/recovery episode changed even though the cluster's OSD fullness ratios have not changed.

This strengthens a distinction already visible in the documentation:

`current PG state flag != cluster fullness-policy authority`

The latter lives in OSDMap/configuration state; the former is current control/reporting state for a PG.

This evidence does not establish the exact crash-persistence representation of every PG state bit and therefore does not claim that `_TOOFULL` flags themselves are durable across daemon restart.

### 4. Retry cadence is separately configurable state

In the Reef `osd.yaml.in` baseline:

- `osd_recovery_retry_interval` is the interval between recovery attempts after a replica denies recovery because it is full;
- `osd_backfill_retry_interval` is the analogous interval for backfill;
- both have a documented default of `30.0` seconds in this release baseline.

The interval is not the fullness threshold and is not a deadline by which recovery must succeed.

Thus:

`capacity-admission policy != retry cadence`

and:

`retry interval != repair deadline`

### 5. Upstream QA intentionally drives the named states

The Reef tree contains standalone tests for capacity-blocked recovery/backfill.

`qa/standalone/osd/osd-recovery-space.sh` manipulates available space/fullness conditions, waits for `recovery_toofull`, asserts that one PG enters that state, and checks the corresponding health report.

`qa/standalone/osd-backfill/osd-backfill-space.sh` similarly constructs an insufficient-headroom condition and checks capacity-blocked backfill behavior.

These tests are important because they show the states were not merely unused enum names in the inspected release. They are still **test harness evidence**, not observations from a named production deployment.

## Engineering reconstruction

The source supports three different retention horizons for maintenance-control information.

### A. Policy horizon

The OSDMap fullness ratios and related configuration define when a destination is admissible. That policy can persist across many individual PG attempts and many retry events until map/configuration/operator state changes.

### B. Episode horizon

`PG_STATE_RECOVERY_TOOFULL` and `PG_STATE_BACKFILL_TOOFULL` summarize the current PG recovery/backfill episode. They are set and cleared as the state machine moves between blocked, waiting, recovering/backfilling, and reset paths.

### C. Retry horizon

A scheduled `DoRecovery()` or `RequestBackfill()` event carries a shorter-lived obligation: try the maintenance path again after the configured delay. The event is neither the repair payload nor the fullness policy.

The resulting project reconstruction is:

```text
longer-lived capacity policy
        ↓ evaluates
current PG maintenance episode
        ↓ may produce
short-lived retry obligation
        ↓ re-enters
future admission attempt
```

These horizons can overlap without being identical.

Consequently:

- `gate active != work abandoned`;
- `PG too-full flag cleared != fullness policy changed`;
- `retry scheduled != progress guaranteed`;
- `reservation released != redundancy debt discharged`;
- `current state report != durable cluster policy`.

This is an engineering reconstruction. Ceph does not name these three categories “retention horizons.”

## Functional analogy

A bounded analogy can be made to other cases in this repository that separate a maintenance obligation from the opportunity to execute it.

- Case 136 separates rebuild obligation from controller resource-priority policy.
- Case 141 shows small retained control state governing the lifetime of much larger WAL history.
- Case 142 here adds a different relation: destination-capacity policy can reject the current repair embodiment while a later retry obligation remains live.

The analogy is functional only. No shared implementation, genealogy, or common storage mechanism is claimed.

## Project interpretation

For this repository, the useful point is not simply that “Ceph retries.” The source shows that the system retains **different kinds of knowledge for different lengths of time**:

- policy answering whether maintenance is admissible;
- episode state answering why this PG is not progressing now;
- retry state answering what should be attempted later.

A maintenance system therefore need not retain every control fact with the same lifetime as the payload or even with the same lifetime as the maintenance obligation itself.

That is a narrow technical-retention claim, not a philosophical claim that all scheduling state is memory in the same sense as object replicas.

## Explicitly rejected / unsupported claims

- **Not established:** Reef introduced capacity-gated recovery/backfill or these state names.
- **Not established:** the `_TOOFULL` PG flags themselves survive an OSD daemon crash/restart.
- **Not established:** a scheduled retry guarantees eventual repair progress.
- **Not established:** releasing a reservation frees enough physical capacity to admit the next attempt.
- **Not established:** `recovery_toofull` and `backfill_toofull` are the same state or use the same threshold.
- **Not established:** mClock/work-class scheduling semantics can be inferred from this retry path.
- **Not established:** upstream standalone QA is a production operational trace.
- **Not established:** a successful retry implies sanitization or physical erasure of obsolete object embodiments.

## Related-repository check

A fresh repository search of `tmzncty/computing-archaeology` for `recovery_toofull` found no existing dedicated module to reuse.

The stable Reef source-state baseline belongs here because it closes a retention-mechanism question already opened by Case 142. Earlier first-introduction history, release-to-release state-machine evolution, scheduler genealogy, and broader implementation archaeology should still be routed to `computing-archaeology` rather than duplicated here.

## Remaining evidence debt

After this deepening, the next useful Case 142 work is narrower:

1. trace commit/release evolution of `_TOOFULL` transitions only if a historical claim needs it;
2. inspect mClock/work-class interaction as a **separate** scheduling slice;
3. obtain named public cluster traces or incident reports showing capacity-gated recovery in operation;
4. run controlled capacity/fault experiments if empirical transition timing matters.

The broad source-level question “does a too-full rejection leave a retryable obligation, and how is that control state represented in Reef?” is now paid for the `v18.2.0` baseline.
