# Ceph Reef Capacity-Gated Recovery: Repair Headroom, Admission, and Redundancy Debt

**Status:** `grounded`

## Scope

- **Object / system:** Ceph/RADOS recovery and backfill under OSD fullness controls.
- **Date range:** bounded to the **Ceph Reef 18.2.x documentation line (2023–2025)**; Reef v18.2.0 was released 7 August 2023.
- **Institution / project:** Ceph open-source project.
- **Retention question:** what happens when the cluster still knows that replica repair is required, but destination-capacity policy refuses the operation that would restore the configured redundancy level?

This is not a second generic Ceph replication case. [`Case 05`](05-rados-replicated-object-repair.md) already grounds 2006 RADOS placement, peering, currentness, and ordinary repair when enough state and resources survive. [`Case 98`](98-ceph-unfound-recovery-exhaustion-administrative-loss.md) handles the different boundary where the required newer object state is known but no recoverable embodiment has been found.

The bounded question here is narrower:

> **Can a retained object remain serviceable while the system is unable or unwilling to spend the free capacity required to restore its designed redundancy?**

Reef documentation says yes. That makes free capacity and repair admission part of the operational conditions of distributed retention without turning “empty disk space” into another kind of payload memory.

The detailed source ledger is [`../evidence/142-ceph-reef-capacity-gated-recovery-grounding.md`](../evidence/142-ceph-reef-capacity-gated-recovery-grounding.md).

---

## Historical vocabulary

The inspected Reef documentation directly uses:

- `placement group` / `PG`;
- `active`;
- `clean`;
- `degraded`;
- `undersized`;
- `recovering`;
- `backfilling`;
- `recovery_wait`;
- `backfill_wait`;
- `recovery_toofull`;
- `backfill_toofull`;
- `nearfull`;
- `backfillfull`;
- `full`;
- `failsafe_full`;
- `recovery reservation`;
- local and remote reservations;
- `OSDMap`;
- `nobackfill`, `norecover`, and `norebalance`.

Project phrases such as **repair headroom**, **redundancy debt**, **maintenance admissibility**, and **future capacity claim** are engineering reconstructions. They are not historical Ceph vocabulary.

No claim is made that Reef introduced these terms or mechanisms. The case uses the Reef branch as a stable, bounded documentation witness.

---

## Retained state

At the payload level, Ceph retains replicated RADOS objects.

For this case, however, several additional relations matter:

1. the placement group's current object/replica state;
2. the configured replica target represented by pool/placement policy;
3. whether the PG is currently serviceable (`active`);
4. whether it has the intended number of replicas (`clean`, `degraded`, `undersized` distinctions);
5. whether recovery or backfill is known to be needed;
6. whether a destination OSD is admitted to receive that maintenance traffic;
7. the OSDMap fullness ratios that participate in that admission decision.

The important separation is:

```text
payload still serviceable
    !=
configured redundancy restored
    !=
repair currently executable
```

A system can preserve enough current state to answer requests while still lacking the infrastructure margin needed to return to its normal redundancy target.

---

## Physical / logical substrate

The physical embodiments remain objects on OSD storage devices.

The repair relation additionally depends on:

- surviving source OSDs;
- a destination OSD;
- network and daemon availability;
- sufficient destination free capacity;
- retained fullness-policy values in the OSDMap;
- reservation/scheduling state that admits or delays recovery work.

So this case does not redefine the object's substrate as “free space.” It shows instead that **future replacement embodiments require a place into which they can be created**.

That creates a capacity relation absent from a naive `N copies = durable` account:

```text
surviving current replicas
    + repair knowledge
    + admissible destination capacity
    + maintenance execution
    -> restored replica set
```

---

## Retention mechanism

### Ordinary replicated survival

Case 05 already establishes that RADOS can preserve one logical object across failure and replacement of particular OSDs, provided enough authoritative current state survives.

### Repair/backfill

In Reef vocabulary, `recovering` means migrating/synchronizing objects and replicas. `backfilling` is a special recovery path that scans and synchronizes the full contents of a PG instead of inferring only needed changes from recent-operation logs.

### Capacity admission

The new boundary is that a destination can be considered too full to receive that repair work.

Reef exposes:

- `recovery_toofull` when a recovery operation waits because the destination OSD is over its full ratio;
- `backfill_toofull` when backfill waits because the destination OSD is over its backfillfull ratio.

The retention mechanism therefore has a policy gate between **repair need** and **repair execution**.

---

## Addressing and access geometry

Object location remains governed by the RADOS/CRUSH placement machinery already discussed in Case 05. This case does not reconstruct CRUSH again.

The relevant geometry is instead **destination eligibility**.

A candidate OSD can be topologically appropriate for a PG and still be operationally inadmissible because accepting the backfill would violate fullness policy.

Thus:

`placement target != admitted repair destination at this moment`

This is a later operational complication of the broader RADOS principle that logical identity can survive physical relocation.

---

## Read semantics

The Reef PG-state documentation separates `active` from `clean`:

- an `active` PG processes requests;
- a `clean` PG has all objects replicated the correct number of times;
- a `degraded` PG has some objects not yet replicated the correct number of times.

The monitor documentation likewise says cluster operation can continue in `active+degraded` after failures, even though operators should return the cluster to `active+clean`.

This yields the bounded conclusion:

> **current serviceability does not prove restored redundancy.**

Do not strengthen this into “all reads always work while degraded.” Availability depends on whether the surviving acting set, `min_size`, peering state, and requested object allow service.

---

## Write semantics and foreground availability

Reef health documentation distinguishes the `full` threshold from `backfillfull`:

- `backfillfull` prevents rebalancing/backfill to an affected OSD;
- `full` prevents the cluster from servicing writes through that full condition.

The thresholds are deliberately ordered, with `backfillfull` below `full` in the normal configuration.

That creates a useful admission sequence:

```text
capacity pressure rises
    ↓
nearfull warning
    ↓
backfillfull: stop admitting some repair/rebalance writes
    ↓
full: foreground write availability is sacrificed
```

The point is not that the percentages are metaphysical boundaries. They are policy thresholds intended to keep the cluster from consuming the last margin needed for safe operation.

The Reef monitor overview contains broader wording about reads near `full`, while the health-check entry specifically identifies writes. This case therefore uses the narrower supported claim and does not universalize read behavior.

---

## Repair admission: blocked work is still owed work

The Reef recovery-reservation developer documentation supplies the strongest bounded evidence.

For backfill, the primary obtains a local reservation and then requests a remote reservation from the target OSD. The target can reject that reservation if it is too full under the `backfillfull_ratio` setting. On rejection, the primary drops the local reservation, waits for `osd_backfill_retry_interval`, and retries; the document says the retry is indefinite.

This produces a retention state with no analogue in a simple “repair happened / repair failed” binary:

```text
PG remains in need of repair
    + destination rejected for capacity
    + repair transaction not running
    + retry relation remains live
```

Therefore:

> **maintenance admission denied now ≠ maintenance obligation discharged.**

This is the core contribution of the case.

---

## Prospective capacity: already-mapped work can reserve the future

The Reef `OSD_BACKFILLFULL` health-check text says the condition can apply not only when an OSD has already crossed the threshold, but also when it **would** exceed the threshold if currently mapped backfills finished.

So repair admission is not purely reactive to current bytes-on-disk occupancy.

The control path can account for work that is already promised/in flight and deny further placement before those bytes have arrived.

Engineering reconstruction:

> **projected maintenance occupancy can constrain present maintenance admission.**

That is a future-capacity relation, not a forecast of hardware failure.

---

## OSDMap fullness state: policy itself must remain current

The Reef monitor configuration reference states that the `mon_osd_nearfull_ratio`, `mon_osd_backfillfull_ratio`, and `mon_osd_full_ratio` configuration values are used when the cluster is created, but after creation the values used by OSDs are stored in the **OSDMap**, not read from the ordinary configuration file or central config store.

Later changes are made by OSD-map commands.

This means a few small control values can govern a much larger physical movement relation:

`configuration source text != current cluster repair-admission authority`

and:

`small retained policy state -> large replica-movement consequences`

The project does not infer the exact on-disk serialization or all crash semantics of those OSDMap fields from this documentation alone.

---

## Time

This case has several different clocks:

- the immediate foreground request interval;
- time spent `active+degraded` before redundancy is restored;
- reservation queue waiting;
- `osd_backfill_retry_interval` between rejected backfill attempts;
- operator time to add capacity, rebalance, or change policy;
- the longer period during which a cluster may remain serviceable with less than configured redundancy.

No fixed physical decay deadline is established here.

The main temporal conclusion is:

> **repair obligation lifetime can exceed any one repair-execution attempt.**

A failed admission attempt can end while the reason to attempt repair survives.

---

## Maintenance and labor

Automatic maintenance includes:

- detecting PG degradation/undersizing;
- selecting recovery or backfill paths;
- acquiring local and remote recovery reservations;
- checking capacity policy;
- retrying rejected backfill reservations;
- moving/synchronizing object replicas;
- reporting PG and health state.

Human/operator work includes:

- capacity planning for expected failure domains;
- adding OSDs or otherwise freeing space;
- choosing fullness ratios;
- diagnosing skewed utilization/CRUSH weighting;
- deciding whether to set or clear `nobackfill`, `norecover`, or `norebalance`;
- deciding whether a threshold change is safer than adding capacity.

The Reef monitor documentation explicitly treats spare capacity planning as part of keeping the cluster able to recover to `active+clean` after failures.

So:

`automated repair != maintenance without capacity planning`

---

## Failure / forgetting modes

Keep these separate.

### 1. Replica loss / degradation

One or more intended replicas are absent or stale enough that the configured replica count has not been restored.

### 2. Destination-capacity rejection

A target exists, but recovery/backfill cannot currently proceed because fullness policy rejects it.

### 3. Reservation/queue waiting

Work may be waiting for reservation resources without being blocked specifically by fullness.

### 4. Explicit maintenance suspension

`nobackfill`, `norecover`, or `norebalance` can suspend work by administrator policy. This is distinct from capacity-triggered `*_toofull`.

### 5. Unfound current state

Case 98 covers the different condition in which the required current payload cannot be found among candidate sources.

`unfound != toofull`

### 6. Foreground write refusal at `full`

Capacity policy may begin refusing foreground writes. This is an availability failure boundary, not proof that retained existing payload has been erased.

### 7. Permanent media loss

Actual loss of sufficient authoritative copies is a different failure from a temporary capacity gate.

---

## Historical record

The bounded first-party record supports these statements for the Reef documentation line:

1. `active`, `clean`, and `degraded` are distinct PG states;
2. a cluster can operate `active+degraded` while aiming to return to `active+clean`;
3. `recovery_toofull` and `backfill_toofull` identify maintenance waiting caused by destination capacity thresholds;
4. remote backfill reservation can be rejected for `backfillfull` and retried later;
5. `OSD_BACKFILLFULL` can account for projected occupancy after currently mapped backfills complete;
6. `nearfull`, `backfillfull`, and `full` have different operational roles;
7. current fullness ratios are cluster-map state in the OSDMap after creation;
8. explicit `nobackfill`/`norecover`/`norebalance` flags are a different way to suspend maintenance.

Primary documentation:

- Ceph Reef release page: <https://docs.ceph.com/en/latest/releases/reef/#v18-2-0-reef>
- Reef Monitor Config Reference: <https://docs.ceph.com/en/reef/rados/configuration/mon-config-ref/#storage-capacity>
- Reef Placement Group States: <https://docs.ceph.com/en/reef/rados/operations/pg-states/>
- Reef Recovery Reservation: <https://docs.ceph.com/en/reef/dev/osd_internals/recovery_reservation/>
- Reef Health Checks: <https://docs.ceph.com/en/reef/rados/operations/health-checks/>

---

## Engineering reconstruction

The source record supports the following project-level conclusions:

1. **serviceable now != clean**;
2. **clean != merely enough copies to answer the current request**;
3. **repair required != repair admitted**;
4. **repair admitted != repair completed**;
5. **destination exists != destination has admissible repair headroom**;
6. **backfillfull != full**;
7. **warning threshold != maintenance-admission threshold != foreground-write stop threshold**;
8. **capacity rejection != repair obligation discharged**;
9. **current occupancy != projected post-backfill occupancy**;
10. **configuration-file value != current OSDMap policy authority after cluster creation**;
11. **automatic capacity gate != explicit operator pause**;
12. **source recoverability != destination admissibility**;
13. **current availability != restored designed failure margin**;
14. **repair headroom is retention infrastructure, not retained payload**.

These are engineering reconstructions. Ceph does not present them as a general theory of retention.

---

## Philosophical / media-theoretical interpretation

A narrow interpretation follows from the mechanism.

Distributed persistence is often described through what **exists**: copies, disks, nodes, objects. Case 142 adds a negative but operationally decisive condition: some capacity must remain **unoccupied enough** to receive a future replacement copy.

That does not make emptiness itself a memory object. Rather, it shows that availability over time can depend on maintaining a margin for re-embodiment.

The useful bounded formulation is:

> **a system can retain current state while owing a future restoration, and that restoration is possible only if infrastructure preserves admissible room for another embodiment.**

This sharpens the repository's maintenance theme without turning `free space` into Stieglerian tertiary retention or Heideggerian `Bestand` by word association.

---

## Functional analogies

### Case 136 — rebuild-rate repair priority

MegaRAID/PERC rebuild-rate controls how strongly admitted repair competes with foreground work.

Ceph `*_toofull` adds a different boundary:

`repair priority != repair admission`

A throttled rebuild is still scheduled work; a rejected backfill reservation is work not currently admitted to the destination.

### Case 140 — retained failure margin

The IBM double-disk array-code case separates `recoverable now` from `full designed failure margin`.

Ceph adds the distributed maintenance path by which lost replica margin may remain unrepaired because there is insufficient admissible destination capacity.

Functional analogy only; no historical continuity is claimed.

### Case 141 — small control state governing large retained populations

PostgreSQL's `restart_lsn` can keep large WAL populations live; Ceph's OSDMap fullness ratios can govern whether large replica populations may move into a destination.

The common function is only this:

`small retained policy/frontier state can determine the lifetime or movement of much larger retained state`

The mechanisms, histories, and failure models are unrelated.

---

## Counterexamples and limits

- This case does **not** claim Reef invented fullness-aware recovery.
- It does not prove every `active+degraded` PG can serve every operation.
- `backfill_toofull` is not evidence that data are lost; the documented reservation path retries.
- `recovery_toofull` is not the same as `unfound` or `incomplete`.
- `backfillfull` is not a physical disk/NAND failure threshold.
- raising a ratio does not create capacity and may reduce the safety margin that motivated the gate.
- completing recovery/backfill does not imply old physical copies were securely erased.
- OSDMap persistence here is a documented control-state boundary, not a fault-injection proof of storage-stack atomicity.
- the Reef documentation does not establish exact behavior for every mClock or scheduler configuration.
- no throughput, latency, or data-loss probability is inferred without measurement.

---

## Related repositories

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Ceph backfillfull` found no dedicated case to reuse.

The division of labor is therefore:

- `technical-retention`: capacity as a repair-admission relation; `active != clean`; repair obligation versus repair execution; retained OSDMap policy; spare headroom as maintenance infrastructure;
- `computing-archaeology`: first-introduction genealogy of fullness ratios/reservations, source-code state-machine evolution, scheduler history, release-by-release behavior, and implementation benchmarks if developed later.

Do not duplicate the general 2006 RADOS history already grounded in Case 05.

---

## Sources

- Ceph Project, **Reef release notes**, v18.2.0, released 7 August 2023: <https://docs.ceph.com/en/latest/releases/reef/#v18-2-0-reef>.
- Ceph Project, **Monitor Config Reference — Storage Capacity**, Reef documentation: <https://docs.ceph.com/en/reef/rados/configuration/mon-config-ref/#storage-capacity>.
- Ceph Project, **Placement Group States**, Reef documentation: <https://docs.ceph.com/en/reef/rados/operations/pg-states/>.
- Ceph Project, **Recovery Reservation**, Reef developer documentation: <https://docs.ceph.com/en/reef/dev/osd_internals/recovery_reservation/>.
- Ceph Project, **Health Checks**, Reef documentation: <https://docs.ceph.com/en/reef/rados/operations/health-checks/>.
- Related evidence ledger: [`../evidence/142-ceph-reef-capacity-gated-recovery-grounding.md`](../evidence/142-ceph-reef-capacity-gated-recovery-grounding.md).
