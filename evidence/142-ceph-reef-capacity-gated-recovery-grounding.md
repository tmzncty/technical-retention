# Evidence 142 — Ceph Reef capacity-gated recovery / backfill grounding

**Status:** grounded  
**Case:** [`../cases/142-ceph-reef-capacity-gated-recovery.md`](../cases/142-ceph-reef-capacity-gated-recovery.md)  
**Bounded question:** when a replicated placement group is degraded and Ceph knows repair or backfill work is still required, how can destination-capacity policy delay that work without making the repair obligation disappear?

## Evidence boundary

This record is deliberately bounded to **Ceph Reef (18.2.x) documentation as a 2023–2025 project-documentation line**, with the first stable Reef release dated **7 August 2023**. It does not claim that `backfillfull`, `recovery_toofull`, recovery reservations, or OSDMap fullness ratios were invented in Reef. Earlier Ceph releases already expose much of this vocabulary; establishing first introduction and exact release genealogy belongs in `tmzncty/computing-archaeology` if pursued.

The slice asks only four questions:

1. Can a PG remain serviceable while it has not yet regained the configured replica count?
2. Can repair/backfill be prevented from starting because the destination lacks acceptable free capacity?
3. Is that blocked state equivalent to completed repair, permanent loss, or abandonment of the repair obligation?
4. Where does the active fullness policy live: ordinary configuration text, or retained cluster-map state?

The answer supported by the inspected Reef documentation is: **service, redundancy state, repair need, repair admission, and destination-capacity policy are distinct relations.**

## Source ladder

| Source | Date / release line | Evidence class | Use here |
|---|---|---|---|
| Ceph Reef release page, v18.2.0 | 2023-08-07 | `H/P` | bounds the Reef release line; does not establish invention priority |
| Ceph Reef, **Monitor Config Reference**, `Storage Capacity` | Reef docs | `H/P` | `active+degraded` versus `active+clean`; fullness thresholds; ratios stored in OSDMap after cluster creation |
| Ceph Reef, **Placement Group States** | Reef docs | `H/P` | meanings of `active`, `clean`, `degraded`, `recovering`, `recovery_toofull`, `backfilling`, `backfill_toofull`, `remapped`, `undersized` |
| Ceph Reef, **Recovery Reservation** developer documentation | Reef docs | `H/P` | local/remote reservation sequence; remote backfill reservation can be rejected for fullness; retry behavior; state-chart relation |
| Ceph Reef, **Health Checks** | Reef docs | `H/P` | ordered fullness thresholds; `OSD_FULL`, `OSD_BACKFILLFULL`; projected-fullness condition; operator suspension flags |

These are first-party Ceph project documents. They ground the documented control semantics, not empirical behavior on every Reef deployment, device, scheduler, or fault interleaving.

## Primary-source anchors

- Reef v18.2.0 release: <https://docs.ceph.com/en/latest/releases/reef/#v18-2-0-reef>
- Monitor configuration / storage capacity: <https://docs.ceph.com/en/reef/rados/configuration/mon-config-ref/#storage-capacity>
- Placement-group states: <https://docs.ceph.com/en/reef/rados/operations/pg-states/>
- Recovery reservation: <https://docs.ceph.com/en/reef/dev/osd_internals/recovery_reservation/>
- Health checks: <https://docs.ceph.com/en/reef/rados/operations/health-checks/>

## Historical record

### 1. `active` and `clean` are different PG states

The Reef **Placement Group States** document defines:

- `active`: Ceph processes requests to the placement group;
- `clean`: Ceph has replicated all objects in the PG the correct number of times;
- `degraded`: some objects have not yet been replicated the correct number of times;
- `undersized`: the PG has fewer copies than the configured pool replication level.

The Reef **Monitor Config Reference** is even more explicit operationally: after failures a cluster may continue in `active+degraded`, while the desired recovery target is `active+clean`.

This grounds a necessary separation:

`client-service admission != configured redundancy restored`

A PG can be useful now while still owing repair work.

### 2. Recovery and backfill have explicit capacity-blocked states

The Reef PG-state document defines two separate waiting states:

- `recovery_toofull`: recovery waits because a destination OSD is over its **full** ratio;
- `backfill_toofull`: backfill waits because a destination OSD is over its **backfillfull** ratio.

The same document defines `backfilling` as scanning and synchronizing the full contents of a PG rather than using recent-operation logs to infer only the missing changes; it explicitly calls backfill a special case of recovery.

Thus:

`repair required != repair currently admitted`

and:

`recovery capacity gate != backfill capacity gate`

The names refer to related but non-identical maintenance paths and thresholds.

### 3. A rejected backfill reservation leaves work pending and retryable

The Reef **Recovery Reservation** developer document describes the admission sequence. A primary first acquires a local reservation and then asks the backfill target for a remote reservation. The target may reject that reservation, including because it is too full under the `backfillfull_ratio` setting.

When rejected, the primary drops the local reservation, waits for `osd_backfill_retry_interval`, and retries. The document states that it will retry indefinitely.

This is especially strong evidence for the bounded retention relation:

`maintenance admission denied now != maintenance obligation discharged`

The system can retain the need to restore placement/redundancy while refusing the current physical destination operation.

The same document separates `backfill_wait` from `backfill_toofull`: ordinary queue/reservation waiting is not the same state as rejection for destination-capacity policy.

### 4. `backfillfull` can be prospective, not merely a measurement of current occupancy

The Reef **Health Checks** document says `OSD_BACKFILLFULL` can be raised when an OSD either:

- has already crossed the `backfillfull` threshold; **or**
- would cross it if currently mapped backfills completed.

The consequence is that data will not be allowed to rebalance to that OSD.

This makes the gate prospective:

`current used-space measurement != only input to repair admission`

A future capacity claim made by already-mapped maintenance work can affect whether more repair/backfill work is admitted now.

This is not prediction of physical device failure. It is cluster policy reserving headroom against a projected post-backfill occupancy.

### 5. `nearfull`, `backfillfull`, and `full` are different control thresholds

The Reef monitor reference documents default ratios of:

- `nearfull`: `0.85`;
- `backfillfull`: `0.90`;
- `full`: `0.95`.

The health-check documentation expects the broader threshold ordering:

`nearfull < backfillfull < full < failsafe_full`

and warns if the order is invalid.

The semantics are not interchangeable:

- `nearfull` is an early warning;
- `backfillfull` prevents rebalancing/backfill to the affected OSD;
- `full` prevents servicing writes according to the Reef health-check page.

Therefore:

`warning threshold != repair-admission threshold != foreground-write stop threshold`

This is more precise than saying “Ceph gets full.” Different capacities trigger different authorities.

### 6. The active fullness policy is retained in the OSDMap after cluster creation

The Reef **Monitor Config Reference** states that the `mon_osd_full_ratio`, `mon_osd_backfillfull_ratio`, and `mon_osd_nearfull_ratio` configuration-file settings apply at cluster creation; afterward, the values used by OSDs are those **stored in the OSDMap**, not the ordinary configuration file or central configuration store. Later changes are made through OSD-map commands such as `ceph osd set-full-ratio` and `ceph osd set-backfillfull-ratio`.

This grounds:

`configuration-file text != current cluster fullness authority`

The ratios are small retained control state whose current OSDMap values influence whether large amounts of replica-repair traffic are admissible.

The monitor documentation also says monitors maintain the master cluster map, changes go through monitor consensus, and maps have versioned epochs. This supports treating the OSDMap value as cluster-control state rather than a local daemon preference.

It does **not** by itself justify claims about the exact physical on-disk bytes, atomicity under every storage fault, or the earliest release in which these ratios moved into the OSDMap.

### 7. Capacity-gated maintenance is different from an explicit operator pause

The Reef health-check page separately lists OSDMap flags such as:

- `nobackfill`;
- `norecover`;
- `norebalance`.

Those flags suspend categories of maintenance by explicit cluster control. `backfill_toofull` and `recovery_toofull`, by contrast, arise from destination fullness conditions.

Therefore:

`automatic capacity admission gate != administrator maintenance suspension`

Both can delay return to `clean`, but the cause and authority are different.

### 8. Source wording around `full` and reads is not fully uniform; use the narrower claim

The Reef monitor configuration overview says that approaching the full ratio can cause Ceph to prevent writes **or reads** as a data-loss safety measure, while the Reef health-check entry for `OSD_FULL` says full OSDs prevent the cluster from servicing **writes**.

This evidence record therefore does **not** promote a universal Reef claim that every read is blocked at the full threshold. The bounded finding used here is the narrower one common to the operational story:

`fullness policy can sacrifice foreground availability, at least write admission, to avoid a more dangerous capacity state`

The documentation discrepancy is retained rather than silently normalized.

## Engineering reconstruction

### A. Spare capacity is part of the repair path

Replication may leave enough surviving copies to serve an `active+degraded` PG, yet returning to `clean` requires a destination able and permitted to receive reconstructed state.

So physical free capacity is not merely “unused storage.” In this mechanism it functions as **repair headroom**.

`surviving source replicas + repair algorithm != completed redundancy restoration without admissible destination capacity`

### B. Maintenance need and maintenance executability are separable

A PG can still be degraded and still need repair while the relevant recovery/backfill state is `*_toofull`.

The condition blocks work; it does not make the missing replica unnecessary.

This adds a new relation to the repository:

`repair obligation lifetime != repair-execution interval`

### C. Current service and future failure margin can diverge

If a PG is active but degraded, current requests can succeed while designed redundancy has not yet been restored. A capacity gate can prolong that interval.

This should not be converted into an unmeasured probability statement about imminent data loss. The grounded conclusion is narrower:

`service available now != full configured replica margin restored`

### D. Admission is prospective as well as reactive

Because `OSD_BACKFILLFULL` may consider occupancy after already mapped backfills finish, the system can refuse an additional repair destination based on a retained accounting of work that has not yet completed.

That gives a bounded form of future-oriented control:

`projected maintenance occupancy can constrain present maintenance admission`

This is engineering reconstruction from documented policy, not philosophical evidence that the system literally “anticipates” in a human sense.

### E. Small policy state can govern large retained-state movement

The current OSDMap ratios are tiny compared with the object population they govern. Yet those values can determine whether PG contents are copied to a destination and whether the cluster can return to `clean`.

Thus:

`control-state size != scope of retained-state consequences`

This resembles Case 141's small `restart_lsn` frontier governing large WAL populations only at the level of function; the mechanisms and histories are unrelated.

## Cross-case comparison

### Case 05 — RADOS ordinary repair

[`Case 05`](../cases/05-rados-replicated-object-repair.md) grounds the 2006 mechanism by which membership change and peering lead to replica reconstruction and return toward the desired placement set.

Case 142 adds a later operational boundary:

`repair known to be needed != destination currently admissible`

This is a deepening of the distributed-retention problem, not evidence that the exact Reef reservation/fullness machinery already existed in the 2006 paper.

### Case 98 — Ceph unfound objects

[`Case 98`](../cases/98-ceph-unfound-recovery-exhaustion-administrative-loss.md) studies a different failure boundary: Ceph may know a newer object/version should exist but have no currently found source from which to reconstruct it.

Case 142 instead assumes a repair/backfill path exists but the destination is capacity-blocked.

`source/current-version recoverability != destination-capacity admissibility`

Do not collapse `unfound` into `*_toofull`.

### Case 136 — MegaRAID/PERC rebuild rate

[`Case 136`](../cases/136-megaraid-perc-rebuild-rate-repair-priority.md) grounds a policy that changes repair priority/resource share while rebuild remains admitted.

Case 142 adds a different scheduler boundary:

`maintenance priority/throttling != maintenance admission/rejection`

A lower rebuild rate and a rejected backfill destination can both delay restored redundancy, but they are not the same mechanism.

### Case 140 — two-failure array codes

[`Case 140`](../cases/140-ibm-double-disk-failure-array-codes.md) separates current recoverability from remaining designed failure margin. Case 142 shows a distributed replicated system can likewise remain serviceable while the operation that would restore its configured redundancy is delayed by capacity policy.

This is a functional comparison only. No RAID→Ceph genealogy is claimed.

## Philosophical boundary

A narrow interpretation survives the engineering detail:

> persistence may depend not only on whether a valid copy exists, but on whether infrastructure preserves enough **room to repair** after one embodiment disappears.

The useful conceptual object is not “empty space as memory.” It is the relation by which unused capacity becomes operationally reserved as the possibility of future re-embodiment.

Do **not** infer:

- free disk space is itself stored payload;
- `backfillfull` is a physical retention mechanism like DRAM refresh;
- Ceph's capacity policy proves a general theory of scarcity or memory;
- a blocked repair is already data loss.

The mechanism supports only the more precise statement that **retention of redundancy can require retained capacity headroom and an admission policy governing when that headroom may be consumed.**

## Stop conditions / what this evidence does not prove

- Reef documentation does not establish first invention or first deployment of fullness-gated recovery.
- `active+degraded` does not imply every workload/read/write remains available under every degraded configuration.
- `backfill_toofull` does not mean the object is lost; the documented backfill path retries.
- `recovery_toofull` / `backfill_toofull` do not prove media corruption.
- crossing a threshold is policy state, not a measured NAND/HDD physical failure boundary.
- changing OSDMap ratios is not equivalent to adding physical capacity.
- completing backfill is not a secure deletion claim about stale source copies.
- the docs do not prove exact power-loss/crash atomicity of OSDMap ratio changes.
- the inspected docs do not establish exact behavior under every mClock/recovery scheduler configuration.
- no benchmark or fault-injection result is claimed.

## Related-repository check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Ceph backfillfull` found no dedicated historical treatment to reuse.

Accordingly:

- **this repository** keeps the retention-specific comparison: serviceability, redundancy debt, destination-capacity admission, OSDMap policy state, and repair headroom;
- **`computing-archaeology`** remains the better home for first-introduction genealogy of `backfillfull`/recovery reservations, scheduler evolution, exact source-code state-machine history, and release-by-release implementation change.

## Remaining research debt

- first commit/release introducing `backfillfull` and `recovery_toofull`;
- first implementation of OSDMap-stored fullness ratios;
- source-level Reef state-machine inspection beyond the project developer documentation;
- exact mClock interaction with recovery/backfill admission;
- named-cluster traces showing threshold transitions;
- controlled fault/capacity experiments showing `active+degraded → *_toofull → recovery → active+clean`;
- behavior when threshold policy itself changes while work is queued;
- cross-release comparison from pre-Luminous through Reef/Tentacle.

---

## Follow-up — Reef `v18.2.0` source-level retry-state deepening

The documentation-level question in this ledger has now been followed into the released Reef state machine in [`142-ceph-reef-source-retry-state-horizon-deepening.md`](142-ceph-reef-source-retry-state-horizon-deepening.md).

That bounded source slice confirms that too-full recovery/backfill states are coupled to explicit delayed retry events, while the current reservation attempt and PG reporting flags have shorter lifetimes than the cluster fullness policy. It therefore closes the broad Reef-baseline question `capacity rejection -> retryable maintenance obligation` without claiming `_TOOFULL` flag crash persistence, mClock semantics, invention priority, or production prevalence.

Further work should now be narrower: pre/post-Reef transition genealogy, mClock interaction, named operational traces, or controlled fault/capacity experiments.
