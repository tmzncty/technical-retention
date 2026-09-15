# Case 142 deepening — Ceph 2012–2019 `backfill_toofull` semantics, retry, and cause-qualified maintenance state

**Status:** `bounded deepening complete`

## Purpose

Case 142 already grounds Ceph Reef `recovery_toofull` / `backfill_toofull`, remote reservation retry, projected backfill occupancy, and the distinction between serviceability and restored redundancy.

This addendum does **not** restate the Reef mechanism. It closes a narrower historical debt left by the canonical case:

> How far back can the public Ceph record establish capacity-gated backfill, and how did the meaning carried by the relevant state / reservation signals become more explicit before Reef?

The inspected upstream commit history supplies a bounded 2012–2019 chain:

1. **2012:** capacity-based refusal, a dedicated `BACKFILL_TOOFULL` PG state, and timed retry already exist together;
2. **2014:** upstream documentation explicitly names `backfill_toofull` as a waiting state caused by destination fullness;
3. **2017:** a generic reservation `REJECT` path is refined with an explicit `TOOFULL` message/event for a running backfill, while old-peer compatibility can still collapse the newer cause distinction on the wire;
4. **2018:** admission expands from current fullness to expected post-backfill occupancy;
5. **2019:** health reporting separates `backfill_toofull` from `recovery_toofull`, and a bug fix prevents a generic reservation revocation from incorrectly acquiring the `backfill_toofull` label;
6. **2019:** event / message names are tightened again so a reservation reject explicitly carries the `TOOFULL` cause in the source vocabulary.

This is a history of **one bounded control relation**, not a complete Ceph recovery/backfill genealogy.

---

## Claim types used here

### Historical record

Exact Ceph upstream commit messages and diffs establish what code / documentation said at particular dates.

### Engineering reconstruction

Project-level distinctions such as `repair debt`, `cause-qualified maintenance state`, `episode state`, and `state authority` are analytical vocabulary used to compare mechanisms. They are not Ceph historical terms.

### Functional analogy

A narrow comparison is made to other cases where retained control state can exist yet be semantically invalid or insufficiently qualified. No implementation genealogy is claimed.

### Philosophical interpretation

The interpretation is deliberately modest: a retained state label is useful only insofar as the relation authorizing its meaning remains valid.

---

## Source set

| Source | Date | Type | Use | Grade |
| --- | --- | --- | --- | --- |
| Ceph commit `c689556896290ac57804b788e42c71b72b97330c`, `PG, OSD: reject backfills when an OSD is nearly full` | 26 Sep 2012 | upstream implementation commit | conservative public implementation floor for capacity-based backfill refusal, `PG_STATE_BACKFILL_TOOFULL`, and delayed retry | **H/P** |
| Ceph commit `6bee1885a9d04f6c82d1769e845c07e08b53a467`, `Docs: Add backfill_toofull to list of PG states` | 21 Jan 2014 | upstream documentation commit | public documentation floor for named waiting state caused by destination fullness | **H/P** |
| Ceph commit `0e9dac1ae1a529ecbb9305dabcb3f97c0e193f8d`, `osd/PG: explicit TOOFULL verb for backfill cancellation` | 23 Oct 2017 UTC | upstream implementation commit | separates explicit too-full cancellation from generic reservation rejection in newer peers, while preserving old-peer compatibility | **H/P** |
| Ceph commit `834d3c19a774f1cc93903447d91d182776e12d18`, `osd: Deny reservation if expected backfill size would put us over backfill_full_ratio` | 18 Dec 2018 | upstream implementation commit | projected-capacity admission for replicated pools; sends byte-count state with reservation request | **H/P** |
| Ceph commit `fa698e18e1c9b1804ff36a4f069cbcfb974b6f08`, `mon: Improve health status for backfill_toofull and recovery_toofull` | 20 Jun 2019 UTC | upstream implementation + documentation + QA commit | distinguishes backfill capacity gate from recovery-full health consequence and explicitly calls `backfill_toofull` potentially transient | **H/P** |
| Ceph commit `fa569ecfecc43ce685b29e0456f62cb085788f25`, `osd: Don't set backfill_toofull in RemoteReservationRevoked path` | 23 Aug 2019 UTC | upstream defect fix | negative evidence: generic reservation revocation/retry must not automatically acquire too-full semantics | **H/P** |
| Ceph commit `0115595c1d1366cb3633e9dc6730496b9e5cf5c4`, `osd: Rename backfill reservation reject names to reflect too full use` | 23 Aug 2019 UTC | upstream implementation terminology cleanup | source vocabulary becomes explicitly cause-qualified: `REJECT_TOOFULL`, `RemoteReservationRejectedTooFull` | **H/P** |

Primary URLs:

- <https://github.com/ceph/ceph/commit/c689556896290ac57804b788e42c71b72b97330c>
- <https://github.com/ceph/ceph/commit/6bee1885a9d04f6c82d1769e845c07e08b53a467>
- <https://github.com/ceph/ceph/commit/0e9dac1ae1a529ecbb9305dabcb3f97c0e193f8d>
- <https://github.com/ceph/ceph/commit/834d3c19a774f1cc93903447d91d182776e12d18>
- <https://github.com/ceph/ceph/commit/fa698e18e1c9b1804ff36a4f069cbcfb974b6f08>
- <https://github.com/ceph/ceph/commit/fa569ecfecc43ce685b29e0456f62cb085788f25>
- <https://github.com/ceph/ceph/commit/0115595c1d1366cb3633e9dc6730496b9e5cf5c4>

---

## Historical record

### H/P — 2012 already couples capacity refusal, a PG state, and timed retry

Commit `c6895568` is the strongest bounded early anchor found in this pass.

Its commit message states the intended behavior directly:

- reject backfills when an OSD reaches a configurable full ratio;
- retry backfilling periodically in the hope that the OSD becomes less full;
- add fullness and retry-interval configuration;
- add PG Active-state transitions for the condition.

The diff makes the relation concrete.

It adds:

- `osd_backfill_full_ratio`;
- `osd_backfill_retry_interval`;
- `MBackfillReserve::REJECT`;
- `PG_STATE_BACKFILL_TOOFULL` with the comment `backfill can't proceed: too full`;
- monitor reporting of `backfill_toofull`;
- a rejection path that cancels the local reservation, sets `PG_STATE_BACKFILL_TOOFULL`, schedules a future `RequestBackfill`, and leaves the current backfill attempt;
- a success path that clears `PG_STATE_BACKFILL_TOOFULL` when the remote reservation is later obtained.

This is enough to establish a conservative public implementation floor:

```text
backfill still needed
    + destination above capacity threshold
    -> current reservation refused
    -> PG marked backfill_toofull
    -> retry scheduled
```

Two boundaries follow directly from the source structure:

> **capacity refusal != repair obligation discharged.**

and

> **one failed reservation attempt != permanent abandonment of backfill.**

The first statement is historical/mechanical; the phrase `repair obligation` is project reconstruction vocabulary.

#### What this does not prove

The 2012 commit is not by itself proof that Ceph invented fullness-aware repair admission in 2012. It is only a public Ceph implementation floor found in this search.

It also does not establish every later `backfill_toofull` semantic detail. Later source changes are evidence that the representation and causal classification continued to evolve.

---

### H/P — 2014 documentation makes the state externally legible

Commit `6bee1885` adds `Backfill-toofull` to the PG-state documentation and describes it as:

- a backfill operation waiting;
- because the destination OSD is over its full ratio.

The commit is documentation-only. Therefore the safe claim is:

> **the named PG state was publicly documented by January 2014.**

Do not rewrite that as:

> **January 2014 was the first implementation of capacity-gated backfill.**

The 2012 implementation record already blocks such a reading.

This is a useful method example for the repository:

```text
first documentation located
    != first code located
    != invention date
```

---

### H/P — 2017 makes one too-full cancellation cause explicit, but compatibility can collapse it

Commit `0e9dac1a` says the earlier path sent `REJECT` when a replica filled up and the primary then set `BACKFILL_TOOFULL`. The change adds an explicit `MBackfillReserve::TOOFULL` verb and a `RemoteReservationRevokedTooFull` event.

That is a source-level move from a more overloaded signal toward a cause-specific signal:

```text
generic reservation rejection/cancellation vocabulary
    -> explicit too-full cancellation vocabulary
```

However, the same diff contains an important compatibility boundary. When encoding for an older peer, `RELEASE` and `TOOFULL` are mapped back to the older `REJECT` value.

Therefore:

> **newer internal causal distinction != guaranteed wire-visible causal distinction to an older peer.**

This is not evidence that old peers behaved incorrectly. It is evidence that compatibility can intentionally preserve a coarser representation while newer code carries a finer internal distinction.

The source comment also notes that, prior to Luminous, `REJECT` had already been overloaded for another reservation meaning. This addendum does not attempt a complete release-by-release compatibility matrix.

---

### H/P — 2018 moves admission from current occupancy toward prospective occupancy

Commit `834d3c19` changes the reservation protocol for replicated pools so that `MBackfillReserve` carries:

- `primary_num_bytes`;
- `shard_num_bytes`.

It adds a tentative fullness calculation and denies a reservation when **expected backfill size** would push the target over `backfill_full_ratio`.

The diff also separates `physical_ratio` from an adjusted ratio used for ordinary fullness-state calculation and folds pending backfill data into that adjusted accounting.

This is an earlier historical floor for a relation that the Reef source deepening already analyzes in its mature form:

```text
current physical occupancy
    != occupancy after already-promised / proposed backfill
```

The 2018 record therefore prevents a false Reef-era novelty claim for projected backfill admission.

It does **not** prove that the exact Reef `pending_backfill()` implementation, approximation rules, EC handling, or all current fields were already identical in 2018.

---

### H/P — 2019 separates backfill-full from recovery-full in health semantics

Commit `fa698e18` changes both documentation and health reporting.

Before the change, `backfill_toofull` and `recovery_toofull` were grouped under a single degraded/full consequence. The change creates distinct health categories:

- `PG_BACKFILL_FULL` for backfill blocked by `backfillfull`;
- `PG_RECOVERY_FULL` for recovery blocked by `full`.

The source assigns different severity:

- `PG_BACKFILL_FULL` -> `HEALTH_WARN`;
- `PG_RECOVERY_FULL` -> `HEALTH_ERR`.

The documentation added in the same commit says `backfill_toofull` may be transient and can clear as PG movement frees space.

This gives three useful boundaries:

> **backfill capacity gate != recovery-full gate.**

> **health severity != payload-loss verdict.**

> **current blocked maintenance state != proof of permanent deadlock.**

The last statement is bounded to the documented possibility of self-resolution. It is not a guarantee that every blocked backfill will eventually make progress.

---

### H/P — August 2019 bug fix: retry/revocation is not itself evidence of `toofull`

Commit `fa569ecf` is especially important for a repository concerned with retained control-state validity.

The commit message says:

> `We shouldn't set backfill_toofull when a revoke occurs in the non-toofull case.`

The diff removes `PG_STATE_BACKFILL_TOOFULL` from a generic `retry()` path and sets it only in the actual reservation-rejection reaction.

The before/after meaning is precise:

```text
reservation episode unwinds / retries
    != therefore destination was too full
```

A generic control transition had been able to stamp the PG with a more specific causal label than the event justified. The fix narrows the state transition so the `backfill_toofull` label is attached to a qualifying rejection instead of every path through retry.

This yields a strong negative boundary:

> **retaining a state flag != retaining a correct diagnosis.**

and more specifically:

> **retry state != capacity-rejection evidence.**

The first sentence is engineering reconstruction; the second follows tightly from the bug fix.

This is not a payload-corruption bug. It is a control/diagnostic-state validity bug whose operational consequence is that the cluster can report a capacity condition that is not actually present.

---

### H/P — later the same day, names are made explicitly cause-qualified

Commit `0115595c` follows the semantic cleanup by renaming source-level reservation terms:

- `REJECT` -> `REJECT_TOOFULL`;
- `RemoteReservationRejected` -> `RemoteReservationRejectedTooFull`;
- `RejectRemoteReservation` -> `RejectTooFullRemoteReservation`.

Its commit message says the only reason for that reject path is a too-full condition and that the new names are intended to make this clearer now that two forms of revoke exist.

The important point is not cosmetic naming by itself. The name change follows the previous bug fix and makes the **event cause** explicit in the control vocabulary.

Thus the pre-Reef record has a progression from:

```text
capacity condition
    -> overloaded reject signal
    -> explicit too-full cancel/revoke signal
    -> bug fix separating generic revoke from too-full reject
    -> cause-qualified reject naming
```

Do not reinterpret that sequence as a claim that the system moved monotonically from `bad` to `good`, or that each later representation is universally more correct under all compatibility conditions. It is a bounded source-history of semantic discrimination in one maintenance-control path.

---

## Retained/control-state decomposition

The pre-Reef history makes several state classes worth keeping separate.

### 1. Payload / replica state

The RADOS object replicas being repaired or backfilled.

### 2. Desired placement / redundancy relation

The reason the cluster knows additional copy movement is still required.

### 3. Destination physical occupancy

What space is currently physically used on an OSD.

### 4. Fullness policy

Thresholds that decide whether additional maintenance writes are admissible.

### 5. Prospective occupancy estimate

Later code can include expected / pending backfill bytes before deciding whether to grant the reservation.

### 6. Reservation state

Whether a current backfill request has obtained the needed local/remote reservation.

### 7. Cause-qualified rejection/revocation state

Why the reservation or running backfill was denied, canceled, or revoked.

### 8. PG episode flag

`PG_STATE_BACKFILL_TOOFULL` is an externally visible summary of the current blocked episode.

### 9. Retry state

A scheduled future request retains the operational intention to try again after the current attempt terminates.

### 10. Health classification

Monitor-side mapping from PG state to an operator-facing health category and severity.

These are related but not interchangeable:

```text
physical fullness
    != fullness policy
    != projected occupancy
    != reservation rejection
    != PG episode flag
    != retry timer/event
    != monitor health severity
```

---

## Engineering reconstruction

The bounded commit chain supports these project-level relations:

1. `repair need != repair admission`;
2. `repair admission failure != repair obligation discharge`;
3. `current attempt ended != future retry relation ended`;
4. `current physical occupancy != projected post-backfill occupancy`;
5. `reservation rejection != every reservation revocation`;
6. `retry path != evidence that capacity caused the retry`;
7. `PG state flag != infallible causal diagnosis`;
8. `state retained != state semantically valid`;
9. `internal cause distinction != old-peer wire distinction`;
10. `health severity != payload-loss verdict`;
11. `blocked now != permanently deadlocked`;
12. `same state name across releases != identical trigger / transport / health semantics`;
13. `public documentation date != first implementation date`;
14. `historical implementation floor != invention-priority proof`.

The most important new relation for Case 142 is:

> **maintenance-control state has an authority condition: the event that licenses a specific diagnosis must be correctly classified.**

`authority condition` is project vocabulary, not Ceph vocabulary.

---

## Functional comparison

### Reef source baseline already in Case 142

The Reef source deepening separates policy, episode, and retry horizons. The 2012–2019 chain supplies the historical reason not to treat those layers as one timeless state machine.

The functional continuity is bounded:

- early and later code can both retain a blocked-maintenance episode and a retry relation;
- later code carries more explicit cause and prospective-capacity information.

No claim is made that the exact 2012 and Reef classes, messages, scheduler, or persistence semantics are identical.

### Case 61 — HDFS state-ID validity

A narrow functional analogy exists with Case 61's lesson that retaining a value is insufficient when its validity regime changes.

Here the problem is different: a PG flag can exist while the event path that produced it did not justify the `toofull` diagnosis.

The shared abstraction is only:

> **retained control state != automatically authoritative control state.**

There is no HDFS↔Ceph genealogy.

---

## Philosophical limit

The bounded conceptual point is small:

> A technical system does not retain only payload and copies; it also retains classifications about why maintenance can or cannot proceed. Those classifications matter only while the relation that authorized them remains valid.

This does not turn Ceph health flags into `memory` in a broad psychological or cultural sense. It only shows that distributed retention depends on small control states whose semantic accuracy can change the system's next actions and an operator's interpretation of risk.

---

## Rejected / unsupported claims

Do **not** claim:

- Ceph invented capacity-gated repair in 2012;
- `c6895568` is the first implementation in all Ceph history rather than the earliest public implementation located in this bounded search;
- the January 2014 documentation commit introduced the mechanism;
- every `backfill_toofull` episode eventually self-resolves;
- `HEALTH_WARN` means the cluster is safe indefinitely;
- `HEALTH_ERR` means payload is already lost;
- `REJECT`, `TOOFULL`, `REVOKE_TOOFULL`, and `REJECT_TOOFULL` are equivalent in every release / peer combination;
- the 2017 compatibility encoding preserves all newer causal distinctions to older peers;
- the 2018 projected-capacity algorithm is identical to Reef's later implementation;
- projected occupancy is exact backend preallocation;
- `PG_STATE_BACKFILL_TOOFULL` itself is durably persisted across every daemon restart;
- a retry event is a durable cross-crash work queue;
- the 2019 false-flag bug caused payload corruption or data loss;
- a corrected diagnostic flag proves eventual repair success;
- this commit chain is a complete history of Ceph backfill, recovery reservations, schedulers, or OSD fullness policy;
- this source chronology establishes invention priority outside Ceph.

---

## Related repositories

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `backfill_toofull` found no dedicated Ceph history to reuse.

The division of labor remains:

- `technical-retention`: the retention-specific relation among repair debt, capacity admission, cause-qualified control state, retry, currentness of diagnosis, and operator-visible health state;
- `computing-archaeology`: complete Ceph backfill/reservation genealogy, release-by-release scheduler evolution, CRUSH/peering implementation history, and benchmark history if developed later.

This addendum intentionally stops once the pre-Reef semantics needed by Case 142 are grounded.

---

## Remaining work

This slice closes a bounded **2012–2019 pre-Reef semantics chronology** for `backfill_toofull` and projected backfill admission.

Still open:

- earlier-than-September-2012 Ceph archaeology for any precursor capacity gate;
- exact release/tag matrix for each commit and downstream backport;
- complete Luminous-era mixed-version compatibility behavior;
- full history of `nearfull` / `backfillfull` / `full` OSDMap thresholds;
- recovery-reservation versus backfill-reservation genealogy outside this narrow path;
- mClock/work-class interaction;
- named production traces showing real clusters entering, clearing, or misreporting the state;
- controlled capacity/fault experiments;
- persistence/reconstitution of PG episode flags and retry work across daemon restart.

Those are separate slices rather than prerequisites for the bounded conclusion here.
