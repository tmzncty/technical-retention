from pathlib import Path

EVIDENCE_PATH = Path('evidence/142-ceph-reef-projected-backfill-admission-accounting-deepening.md')
CASE_PATH = Path('cases/142-ceph-reef-capacity-gated-recovery.md')
ROADMAP_PATH = Path('ROADMAP.md')
INDEX_PATH = Path('CASE_INDEX.md')

if EVIDENCE_PATH.exists():
    raise SystemExit(f'{EVIDENCE_PATH} already exists; refusing duplicate integration')

EVIDENCE_PATH.write_text(r'''# Evidence 142C — Ceph Reef projected backfill admission accounting

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
''', encoding='utf-8')

# Update Case 142 evidence navigation and add the bounded mechanism deepening.
case = CASE_PATH.read_text(encoding='utf-8')
old_link = "A source-level Reef `v18.2.0` deepening is [`../evidence/142-ceph-reef-source-retry-state-horizon-deepening.md`](../evidence/142-ceph-reef-source-retry-state-horizon-deepening.md).\n"
new_link = old_link + "\nA source-level projected-capacity accounting deepening is [`../evidence/142-ceph-reef-projected-backfill-admission-accounting-deepening.md`](../evidence/142-ceph-reef-projected-backfill-admission-accounting-deepening.md).\n"
if old_link not in case:
    raise SystemExit('Case 142 evidence-link marker not found')
case = case.replace(old_link, new_link, 1)
section_marker = "---\n\n## OSDMap fullness state: policy itself must remain current\n"
if section_marker not in case:
    raise SystemExit('Case 142 OSDMap section marker not found')
section = r'''### Reef source deepening: projected backfill bytes are admission state, not exact preallocation

The released Reef `v18.2.0` source makes the health-check wording about projected occupancy concrete. `MBackfillReserve` carries `primary_num_bytes` and `shard_num_bytes` into the remote reservation path. For an ordinary replicated PG, `pending_backfill()` treats the extra capacity claim as `max(0, primary_bytes - local_bytes)` rather than charging the target for the entire source PG again.

For erasure-coded pools, the source explicitly says it **overestimates by a full stripe per object** because exact per-object stripe rounding is not known at that point. Nearby comments also state that compression information, metadata overhead, and omap overhead are not fully available to the calculation.

The target passes the resulting `pending_adjustment` into `tentative_backfill_full()`. `OSDService::compute_adjusted_ratio()` applies the proposed increment and also folds in pending backfill state from other PGs before comparing the adjusted ratio with the ordinary fullness thresholds. At the same time, Reef keeps a separate raw `physical_ratio`; the failsafe-full branch uses that raw ratio while `FULL` / `BACKFILLFULL` / `NEARFULL` are evaluated against the adjusted quantity.

This closes a more precise relation than the documentation alone:

```text
current raw physical utilization
    != utilization adjusted for already-promised + proposed backfill bytes
    != exact future backend allocation
```

Engineering reconstruction: physically empty bytes can already be partly **spoken for** by admitted maintenance work before those bytes are materially occupied. But this is retained accounting/control state, not an exact disk-extent reservation and not another payload copy. Reservation acceptance therefore does not guarantee eventual completion, while rejection does not prove loss; it changes the present admissibility of a still-owed repair.

Full source and approximation boundaries: [`../evidence/142-ceph-reef-projected-backfill-admission-accounting-deepening.md`](../evidence/142-ceph-reef-projected-backfill-admission-accounting-deepening.md).

---

## OSDMap fullness state: policy itself must remain current
'''
case = case.replace(section_marker, section, 1)
source_line = "- Source-level retry-state deepening: [`../evidence/142-ceph-reef-source-retry-state-horizon-deepening.md`](../evidence/142-ceph-reef-source-retry-state-horizon-deepening.md)."
if source_line not in case:
    raise SystemExit('Case 142 Sources marker not found')
case = case.replace(source_line, source_line + "\n- Projected-backfill admission accounting: [`../evidence/142-ceph-reef-projected-backfill-admission-accounting-deepening.md`](../evidence/142-ceph-reef-projected-backfill-admission-accounting-deepening.md).", 1)
CASE_PATH.write_text(case, encoding='utf-8')

# Add a concise Phase-2 completion/status entry.
roadmap = ROADMAP_PATH.read_text(encoding='utf-8')
phase2 = "## Phase 2 — Build missing technical bridges\n\n"
if phase2 not in roadmap:
    raise SystemExit('ROADMAP Phase 2 marker not found')
roadmap_entry = "- [x] **Case 142 Ceph Reef projected-backfill admission accounting deepening:** [`cases/142-ceph-reef-capacity-gated-recovery.md`](cases/142-ceph-reef-capacity-gated-recovery.md) + [`evidence/142-ceph-reef-projected-backfill-admission-accounting-deepening.md`](evidence/142-ceph-reef-projected-backfill-admission-accounting-deepening.md) use the released `v18.2.0` `MBackfillReserve` / `PG` / `OSDService` path to separate raw physical occupancy, already-pending repair claims, a proposed incremental backfill claim, and the adjusted fullness quantity used for admission. The replicated path uses positive source-minus-local bytes; the EC path explicitly overestimates by a stripe-per-object term because exact rounding is unavailable, while source comments retain compression/metadata/omap limits. This closes `current physical free space != uncommitted repair headroom` and `admission estimate != exact future physical allocation` without treating byte counters as extent preallocation, promising completion, or claiming first-introduction genealogy. Production traces, backend-specific estimate error, mClock interaction, and release genealogy remain open; broad mechanism history stays with `computing-archaeology`.\n\n"
if roadmap_entry in roadmap:
    raise SystemExit('ROADMAP entry already present')
roadmap = roadmap.replace(phase2, phase2 + roadmap_entry, 1)
ROADMAP_PATH.write_text(roadmap, encoding='utf-8')

# Append findings after the current authoritative tail. Refuse to guess numbering.
index = INDEX_PATH.read_text(encoding='utf-8').rstrip() + "\n"
if "**3667 — X**" not in index:
    raise SystemExit('CASE_INDEX does not end in expected 3667-era ledger; refusing to renumber blindly')
if "Findings 3668–3683 — Case 142 Reef projected backfill admission accounting" in index:
    raise SystemExit('CASE_INDEX findings already present')
appendix = r'''

### Findings 3668–3683 — Case 142 Reef projected backfill admission accounting

- **3668 — H/P** — Reef `MBackfillReserve` version 5 carries `primary_num_bytes` and `shard_num_bytes` with a remote backfill reservation request, so admission can reason about expected byte volume before the target receives all backfill payload.
- **3669 — H/P** — For the ordinary replicated path, Reef computes pending additional backfill as `max(0, primary_bytes - local_bytes)`, separating source PG size from the incremental destination-capacity claim.
- **3670 — H/P** — Reef's erasure-coded path explicitly overestimates by a full stripe per object because exact per-object stripe rounding is unavailable from the aggregate information at that point.
- **3671 — H/P** — The same source records unresolved/approximate dimensions for metadata overhead, compression adjustment, and omap overhead; the admission calculation is not a complete backend-allocation model.
- **3672 — H/P** — The remote PG passes the proposed pending increment into `tentative_backfill_full()` before granting the reservation, allowing a not-yet-physically-full target to reject work whose expected addition crosses `BACKFILLFULL`.
- **3673 — H/P** — `OSDService::compute_adjusted_ratio()` also incorporates pending backfill state from PGs already holding reservations, so later decisions can account for multiple promised-but-not-yet-materialized repair populations.
- **3674 — H/P** — Reef keeps raw `physical_ratio` distinct from adjusted `cur_ratio`; the released fullness state machine uses raw physical usage for failsafe-full while ordinary `FULL` / `BACKFILLFULL` / `NEARFULL` evaluate the adjusted ratio.
- **3675 — H/P** — Accepted remote backfill accounting is retained in PG byte counters and cleared by `unreserve_recovery_space()`, making the capacity claim maintenance-control state with its own lifetime rather than payload data.
- **3676 — E** — `current physical free space != uncommitted repair headroom`: bytes can remain physically unused while already contributing to admission pressure because pending maintenance has claimed them in the accounting relation.
- **3677 — E** — `admission-effective occupancy != exact future physical allocation`: the former is a policy-facing estimate assembled before all backend allocation details are known.
- **3678 — E** — `fullness threshold authority != quantity evaluated against the threshold`: OSDMap policy supplies the ratios, while pending-byte accounting constructs the adjusted utilization compared with them.
- **3679 — E** — `reservation accepted != backfill completion guaranteed`; admission establishes present headroom under the current estimate, not immunity from later writes, failures, revocation, or changed cluster state.
- **3680 — E/A** — Repair urgency, source reconstructability, and destination-capacity admission are independent axes: Case 136's priority/readability distinctions and Case 142's projected-capacity gate are functionally comparable but not one mechanism.
- **3681 — A/E** — Small retained control state can govern much larger retained populations in both Case 141 and Case 142, but WAL-retention frontiers and Ceph pending-backfill byte claims have unrelated protocols and histories.
- **3682 — X** — Pending-backfill counters do not prove exact disk-extent preallocation, exact EC/storage overhead, complete compression/omap accounting, or a universal future-capacity guarantee.
- **3683 — X** — Capacity admission/rejection neither proves payload loss nor sanitization, and the cited 2018 implementation-intent commits do not establish invention priority or unchanged behavior across all Ceph releases.
'''
INDEX_PATH.write_text(index + appendix.lstrip('\n'), encoding='utf-8')

# Local consistency guards.
for p in (EVIDENCE_PATH, CASE_PATH, ROADMAP_PATH, INDEX_PATH):
    text = p.read_text(encoding='utf-8')
    if '\r' in text:
        raise SystemExit(f'CR character found in {p}')
    if not text.endswith('\n'):
        p.write_text(text + '\n', encoding='utf-8')

print('Case 142 projected-backfill integration prepared')
