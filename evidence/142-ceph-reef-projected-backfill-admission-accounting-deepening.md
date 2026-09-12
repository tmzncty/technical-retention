# Evidence 142C — Ceph Reef projected backfill admission accounting

**Status:** `grounded`  
**Case:** [`../cases/142-ceph-reef-capacity-gated-recovery.md`](../cases/142-ceph-reef-capacity-gated-recovery.md)  
**Baseline:** Ceph `v18.2.0` / Reef source tree.  
**Bounded question:** when a target OSD is not yet physically above `backfillfull`, how does Reef account for bytes that an accepted backfill is expected to add, and what does that accounting prove—or fail to prove—about future physical allocation?

## Evidence boundary

Case 142 already establishes the user-visible relation `current serviceability != restored redundancy != repair currently executable`, and Evidence 142B establishes the retry-state relation after a capacity rejection. This slice asks a different, narrower question:

> **What quantity is tested at admission time: current physical occupancy, an estimate of future occupancy, or an exact preallocation of the space the backfill will consume?**

The inspected Reef source answers: the admission path carries byte-count estimates, converts them into a pending increment, combines that increment with already pending backfills, and evaluates a tentative fullness state. The code also records explicit approximation limits, especially for erasure-coded pools, compression, metadata, and omap overhead.

Therefore this slice distinguishes:

```text
current raw physical utilization
    != admission-effective adjusted utilization
    != exact future physical allocation
```

It does **not** reconstruct the first introduction of this mechanism. Broader release-by-release genealogy remains for `computing-archaeology`.

## Primary source ladder

| Source | Version | Evidence class | Use here |
| --- | --- | --- | --- |
| `src/messages/MBackfillReserve.h` | Ceph `v18.2.0` | `H/P` | reservation request carries `primary_num_bytes` and `shard_num_bytes`; too-full reject/revoke message types |
| `src/osd/PG.cc` | Ceph `v18.2.0` | `H/P` | pending-byte computation, EC estimate, approximation comments, reservation acceptance/rejection and retained byte counters |
| `src/osd/OSD.cc` | Ceph `v18.2.0` | `H/P` | tentative fullness calculation; raw `physical_ratio` versus adjusted ratio; inclusion of already-pending PG backfills |
| Reef Health Checks / Recovery Reservation docs | Reef | `H/P` | public statement that backfill may be refused when a target is or would become too full |

Primary anchors:

- <https://github.com/ceph/ceph/blob/v18.2.0/src/messages/MBackfillReserve.h>
- <https://github.com/ceph/ceph/blob/v18.2.0/src/osd/PG.cc>
- <https://github.com/ceph/ceph/blob/v18.2.0/src/osd/OSD.cc>
- <https://docs.ceph.com/en/reef/rados/operations/health-checks/>
- <https://docs.ceph.com/en/reef/dev/osd_internals/recovery_reservation/>

Supplementary implementation-intent witnesses, not invention-priority claims:

- Ceph commit `834d3c19a774f1cc93903447d91d182776e12d18`, 18 December 2018, replicated-pool expected-backfill-size admission: <https://github.com/ceph/ceph/commit/834d3c19a774f1cc93903447d91d182776e12d18>.
- Ceph commit `0474498684d089559d479f62ae16db53c1604652`, 18 December 2018, erasure-coded-pool adaptation: <https://github.com/ceph/ceph/commit/0474498684d089559d479f62ae16db53c1604652>.

These two commits are used only to corroborate the intent visible in the released Reef path. This evidence file does not claim they are the first industry or Ceph implementation of prospective capacity accounting.

---

## Historical / source-level record

### H/P — a backfill reservation request carries byte-count state, not only a queue slot request

In Reef, `MBackfillReserve` version 5 contains both `primary_num_bytes` and `shard_num_bytes`. A `REQUEST` becomes a `RequestBackfillPrio` event carrying those values into the remote side's peering state.

The message contract therefore permits the destination to reason about expected data volume before accepting the backfill reservation.

This is stronger than:

`remote reservation == concurrency token only`

but weaker than:

`remote reservation == exact physical extent allocation`

No block addresses or exact future extents are conveyed by these two byte counters.

### H/P — Reef computes the additional backfill claim as the positive difference between source and local byte estimates

`PG.cc` defines a `pending_backfill()` helper that returns:

```text
max(0, primary_bytes - local_bytes)
```

For the ordinary replicated case, this means the capacity question is not simply “how large is the PG on the primary?” The local amount already present on the target is subtracted, and only a positive expected increment is treated as pending additional occupancy.

Thus:

`source PG bytes != incremental destination-capacity claim`

### H/P — erasure-coded pools use an explicitly conservative stripe-based estimate

Before calling `pending_backfill()`, the Reef path treats erasure-coded PGs specially. The source comment says it will **overestimate by a full stripe per object** because it does not know exactly how each object rounds to a stripe. It divides the aggregate byte count by the EC data-chunk count and then adds one stripe-chunk contribution per object.

The code therefore documents its own epistemic boundary:

`EC pending-byte estimate != exact future encoded allocation`

This is not merely an external interpretation; the released source labels the calculation as an overestimate caused by missing per-object rounding knowledge.

### H/P — the source records additional accounting blind spots

The same Reef path contains explicit comments about quantities it cannot exactly incorporate at this stage:

- metadata overhead is only estimable;
- compression adjustment would require additional compressed/original-byte information from the primary;
- omap overhead is not available through this calculation and may reside on a different partition that stores the database.

These comments are important negative evidence. The admission calculation is a deliberately useful guard, not a complete physical-space simulator.

### H/P — tentative admission adds the expected increment before evaluating `BACKFILLFULL`

The remote PG passes `pending_adjustment` into `OSDService::tentative_backfill_full()`. `OSD.cc` computes an adjusted utilization by reducing reported available space by the proposed increment and then recalculating the fullness state. If the tentative state reaches `BACKFILLFULL` or a stronger fullness state, the backfill reservation is rejected as too full.

So a target can reject a reservation even when its currently observed bytes alone have not yet crossed the relevant threshold.

`physical occupancy below threshold != new backfill admissible`

### H/P — already accepted backfills are folded into subsequent adjusted utilization

`OSDService::compute_adjusted_ratio()` does more than apply the one proposed `adjust_used` value. It iterates over PGs and calls `pg_stat_adjust()` so pending backfill data already associated with PGs are included in the adjusted statistic.

The regular heartbeat path also calls `compute_adjusted_ratio()` without a new proposed increment. Therefore the OSD's advertised/evaluated fullness state can include already pending backfill claims rather than waiting for all corresponding bytes to become physically resident.

This is the source-level mechanism behind the Reef health documentation's warning that an OSD may be considered backfill-full because currently mapped backfills would take it over the threshold.

### H/P — Reef keeps a raw physical ratio distinct from the adjusted ratio

In `OSD.cc`, `compute_adjusted_ratio()` first computes `pratio` from raw physical used bytes (`get_used_raw() / total`). It then returns a second ratio after pending-backfill adjustments. `check_full_status()` stores both `cur_ratio` and `physical_ratio`.

`recalc_full_state()` uses the raw physical ratio for the failsafe-full boundary while evaluating ordinary `FULL`, `BACKFILLFULL`, and `NEARFULL` against the adjusted ratio.

The released implementation therefore directly distinguishes:

```text
raw physical utilization
    vs
policy/admission utilization after pending-backfill accounting
```

The distinction is operational, not merely terminological.

### H/P — an accepted reservation retains byte-count state until it is released/updated

When the remote reservation passes the fullness check, the PG stores the primary/local byte values used for backfill-space accounting. `unreserve_recovery_space()` clears those counters when that capacity claim no longer applies.

That retained accounting state is small compared with the backfill payload, but it changes how later capacity decisions are evaluated.

It is therefore a maintenance-control relation, not another copy of the object data.

---

## Engineering reconstruction

### E — free bytes can be physically unused yet no longer fully uncommitted for repair admission

A naive capacity model treats free space as a direct observation:

```text
free_now = total - used_now
```

Reef's backfill-admission model is relational:

```text
physical used now
+ already pending backfill claims
+ proposed incremental claim
-> tentative admission-effective utilization
```

The project-level conclusion is:

> **currently unoccupied capacity can already be partially spoken for by maintenance obligations that have been admitted but not yet fully materialized.**

“Spoken for” is an engineering reconstruction. The source implements counters/adjusted statistics; it does not allocate named future disk extents at reservation time.

### E — an admission estimate is neither a prediction oracle nor a durability witness

The target's calculation helps prevent obviously unsafe over-admission, but the source itself records missing information. Future foreground writes, allocation overhead, compression behavior, object-size distribution, metadata/omap behavior, and changing cluster state can all make exact future physical occupancy differ from the estimate.

Therefore:

`reservation accepted != capacity outcome guaranteed`

and:

`reservation rejected != payload lost`

A rejection preserves the retryable redundancy debt already grounded in Evidence 142B.

### E — conservative EC estimation trades precision for safety margin

The EC path's “full stripe per object” overestimate is useful precisely because exact encoded allocation is unavailable from the aggregate information carried at that point.

This supports a bounded general lesson:

> **maintenance admission can depend on deliberately conservative retained estimates when exact future embodiment size is not yet knowable.**

The lesson should not be turned into a claim that Ceph's estimate is always conservative under every backend/compression/metadata condition; the source comments identify omitted dimensions.

### E — capacity policy and capacity accounting are separate layers

The OSDMap supplies the fullness thresholds. The pending-byte machinery supplies the adjusted quantity compared against those thresholds.

Thus:

`threshold authority != measured/estimated quantity evaluated against threshold`

Changing the threshold and changing the pending-byte estimate are different interventions, even though both can change the resulting admission decision.

---

## Functional analogies

### Case 136 — repair priority / reconstructability

Case 136 already separates repair scheduling priority from the readability of surviving RAID sources. Case 142 adds another independent axis: a repair can be known, sources can be available, and priority can be high, yet the destination can remain inadmissible because projected occupancy crosses policy.

Functional analogy only:

`repair urgency != repair source validity != destination-capacity admission`

### Case 141 — small retained control state governing a larger retained population

PostgreSQL replication-slot frontiers can keep a much larger WAL population live. Reef pending-backfill byte counters can constrain movement of a much larger object population. The common point is only that small control state can govern future materialization/reclamation relations.

No protocol, lineage, or implementation identity is claimed.

---

## Rejected / unsupported claims

- **X — pending-backfill accounting is exact physical preallocation.** The inspected source carries byte counts and adjusted statistics, not exact future disk extents.
- **X — the adjusted ratio is identical to current physical utilization.** Reef explicitly keeps a raw `physical_ratio` separate from the adjusted ratio.
- **X — EC pending size is exact.** The source explicitly calls its stripe-per-object treatment an overestimate because exact rounding is unavailable.
- **X — the model fully accounts for compression, metadata, and omap.** The source explicitly records these limits/TODOs.
- **X — reservation acceptance guarantees backfill completion.** Admission can be followed by later capacity change, revocation, failure, or retry-state transitions.
- **X — reservation rejection proves data loss.** It proves current maintenance admission failed; Case 142B shows retry state can remain live.
- **X — pending capacity is retained payload.** It is maintenance-control/accounting state concerning a future embodiment.
- **X — `BACKFILLFULL` is a media-retention threshold.** It is a cluster admission-policy boundary.
- **X — 2018 source commits establish invention priority.** They are implementation-intent witnesses only; broader genealogy remains outside this slice.
- **X — successful backfill or capacity reservation establishes secure deletion of obsolete source embodiments.** No sanitization claim follows.

---

## Claim ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| Reef reservation messages carry source/target byte-count information | `H/P` | `MBackfillReserve.h` v18.2.0 |
| replicated pending claim is the positive source-minus-local byte difference | `H/P` | `PG.cc` `pending_backfill()` |
| EC accounting deliberately overestimates by stripe/object because exact rounding is unavailable | `H/P` | `PG.cc` source comment + EC calculation |
| compression/metadata/omap are not fully known to this calculation | `H/P` | explicit `PG.cc` TODO/XXX comments |
| proposed bytes are added before tentative `BACKFILLFULL` evaluation | `H/P` | `PG.cc` + `OSD.cc` |
| already pending PG backfills are included in adjusted utilization | `H/P` | `OSDService::compute_adjusted_ratio()` |
| raw physical ratio and adjusted admission ratio are separate quantities | `H/P` | `OSD.cc` |
| free physical space can be partly committed to admitted future maintenance | `E` | reconstruction from pending-byte accounting |
| admission-effective occupancy is not exact future physical allocation | `E/X` | source approximation limits |
| threshold policy is distinct from the accounting quantity compared with it | `E` | OSDMap policy + source calculation |
| repair urgency/source availability does not imply destination admission | `A/E` | bounded cross-case comparison |
| capacity reservation proves sanitization or exact physical preallocation | `X` | unsupported by source scope |

## Related-repository check and remaining debt

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `backfill_toofull`, `recovery_toofull`, and Ceph backfill-capacity accounting found no dedicated module to reuse in this round.

This source-level calculation belongs in Case 142 because it changes the retention claim: **repair headroom is not merely current empty space; admitted but not-yet-materialized maintenance work can already consume the policy-visible margin.**

Still open after this slice:

- production traces comparing raw versus adjusted fullness during sustained backfill;
- controlled experiments around reservation acceptance, revocation, capacity pressure, and restart;
- backend-specific compression/metadata/omap effects on estimate quality;
- mClock/work-class interaction as a separate scheduling question;
- release-to-release genealogy and earlier introduction history, which should be routed primarily to `computing-archaeology`.
