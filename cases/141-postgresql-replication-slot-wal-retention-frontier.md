# Case 141 — PostgreSQL Replication Slots: WAL Retention Frontier and Continuation Admission

**Status:** grounded  
**Claim layer:** historical record + engineering reconstruction + bounded functional analogy + bounded philosophical interpretation  
**Primary regime:** PostgreSQL pre-slot archive-backed standby operation (9.1, 2011), public logical-slot / replication-slot development (2012–2014), PostgreSQL 9.4 replication-slot release (2014), PostgreSQL 13 resource-bound evolution (2020), and PostgreSQL 17 logical failover-slot synchronization (2024)  
**Evidence records:**

- [`../evidence/141-postgresql-2014-2020-replication-slot-wal-retention-grounding.md`](../evidence/141-postgresql-2014-2020-replication-slot-wal-retention-grounding.md)
- [`../evidence/141-postgresql-2012-2014-replication-slot-public-genealogy-deepening.md`](../evidence/141-postgresql-2012-2014-replication-slot-public-genealogy-deepening.md)
- [`../evidence/141-postgresql-2024-failover-slot-synchronization-deepening.md`](../evidence/141-postgresql-2024-failover-slot-synchronization-deepening.md)
- [`../evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md`](../evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md)
- [`../evidence/141-postgresql-2018-2020-physical-slot-advance-persistence-deepening.md`](../evidence/141-postgresql-2018-2020-physical-slot-advance-persistence-deepening.md)
- [`../evidence/141-postgresql-2011-2020-wal-archive-alternate-continuation-deepening.md`](../evidence/141-postgresql-2011-2020-wal-archive-alternate-continuation-deepening.md)

## Summary

This case asks a narrow distributed-log retention question:

> **Can history that is no longer needed for the primary's immediate current state remain non-reclaimable because a lagging or disconnected future consumer still needs it, and what happens when the primary later gains authority to sacrifice that continuation relation to bound local storage use?**

PostgreSQL 9.4 supplies a clean mechanism. A **replication slot** is persistent control state. Its `restart_lsn` records the oldest WAL position that might still be required by the slot's consumer. PostgreSQL aggregates slot requirements into the WAL-removal horizon, so old WAL remains available even while the consumer is not currently connected.

But Case 141 now also records an important pre-slot and cross-carrier boundary: PostgreSQL 9.1 already documented physical standby catch-up through an independently accessible WAL archive. Consequently, a primary-local slot protection failure and global disappearance of the corresponding history are not the same proposition.

The retained objects and paths are therefore not one thing:

```text
primary current database state
        != replication-slot control state
        != consumer-need frontier (`restart_lsn`)
        != primary-local WAL history governed by that frontier
        != archived WAL copies retained elsewhere
        != base-backup materialized state
        != current connection/activity state
```

The released 9.4 documentation exposes a cost: replication slots retain only history known to be needed, but the original design had no built-in way to bound the disk space that slot-retained `pg_xlog` could consume.

PostgreSQL 13 makes that conflict explicit. `max_slot_wal_keep_size` can cap how much WAL a slot is allowed to protect. The later `wal_status` state machine distinguishes `reserved`, `extended`, `unreserved`, and `lost`. In particular, `unreserved` means required WAL is no longer protected although some segments may still physically exist until checkpoint removal; `lost` means required WAL for that slot has been removed and the slot is no longer usable.

The archive deepening prevents a stronger but unsupported inference:

```text
slot is `lost`
    != every copy of the required WAL is globally absent
```

For a physical standby, an accessible archive can independently supply the replay interval if it retained enough segments. If no usable replay path remains, PostgreSQL documents reinitialization from a new base backup.

The case's central decomposition is now:

```text
history still needed by consumer
    != history currently protected on the primary
    != history physically present on the primary
    != equivalent history present in another carrier
    != slot usable for continuation
    != standby recoverable through some alternate path
```

The 2020 policy is later history and must not be projected back into 2014 vocabulary or semantics; likewise, physical-standby archive recovery must not be projected onto logical decoding without direct evidence.

## Research questions

1. What exactly is retained by a PostgreSQL replication slot?
2. How does a small `restart_lsn` frontier govern the lifetime of a much larger WAL corpus?
3. Does a disconnected consumer stop constraining retention? No — under the 9.4 slot relation, disconnection and retention obligation are separate.
4. Does crash-safe slot state imply all required WAL necessarily survives forever? No — PostgreSQL 13 provides a direct counterexample.
5. What is the difference among `reserved`, `unreserved`, physically present, and `lost` WAL?
6. Can WAL needed by a physical standby survive outside the primary's slot-governed local corpus? Yes — the documented WAL archive is an independent carrier, provided it retains a sufficient replay interval.
7. Is slot invalidation or local WAL removal technical erasure? No — both are weaker than media sanitization and weaker than global absence of all copies.
8. How does this differ from Raft snapshot transfer, Bigtable redo-point recovery, and LevelDB file liveness?
9. What belongs here versus broader PostgreSQL/WAL history in `computing-archaeology`?

## Source ladder

| Evidence | Date | Strength | Use here |
|---|---:|---|---|
| PostgreSQL 9.1 warm-standby docs | 2011 release series | `H/P` | pre-slot archive/local/stream fallback, base-backup reinitialization, archive cleanup |
| PostgreSQL pgsql-hackers, `logical changeset generation v3` | 2012-11-15 | `H/P` | public `max_logical_slots` / logical-slot floor |
| PostgreSQL pgsql-hackers v3 review reply | 2012-12-13 | `H/P` | slot-id reused across separate walsender sessions; explicit restart-persistence gap |
| PostgreSQL pgsql-hackers, `logical changeset generation v4` | 2013-01-15 | `H/P` | crash/restart persistence work and permanent slot lifecycle |
| PostgreSQL pgsql-hackers, `logical changeset generation v5` | 2013-06-14 | `H/P` | explicit plan to generalize `logical slot` into replication slots usable by streaming replication |
| PostgreSQL `858ec118...`, “Introduce replication slots” | 2014-02-01 | `H/P` | crash-safe slot purpose and initial WAL-retention relation |
| PostgreSQL 9.4 release/docs | 2014-12-18 release | `H/P` | released slot contract plus archive as an alternate physical-standby continuation carrier |
| PostgreSQL 9.4 `REL9_4_0` `slot.c` / `slot.h` | 2014 | `H/P` | persistent slot fields, save/checkpoint/startup reconstitution, minimum required LSN |
| PostgreSQL `c6550776...` | 2020-04-07 | `H/P` | `max_slot_wal_keep_size`, checkpoint invalidation, disk-exhaustion motivation |
| PostgreSQL `b8fd4e02...` | 2020-06-24 | `H/P` | `reserved` / `extended` / `unreserved` / `lost` state refinement |
| PostgreSQL 13 release/docs | 2020-09-24 release | `H/P` | released resource-bound contract and continued archive/local retention separation |
| PostgreSQL 17 failover-slot commits/docs | 2024 | `H/P` | cross-node persistence/admission of logical slot state |

The complete source and claim ledgers are in the evidence files.

## Historical record

### 0. 2011 pre-slot boundary: archive-backed standby catch-up already exists

PostgreSQL 9.1, released **12 September 2011**, documents physical standby operation as able to recover WAL from an archive via `restore_command`, from WAL already present on the standby, or by streaming from the primary.

The 9.1 streaming-replication section states that without file-based continuous archiving, `wal_keep_segments` must be large enough to stop the primary recycling WAL too early; otherwise an excessively lagging standby must be reinitialized from a new base backup. If an archive accessible to the standby exists, the standby can instead use that archive to catch up.

This is earlier than PostgreSQL replication slots and establishes a strict novelty boundary:

```text
archive-backed physical-standby continuation
    predates
replication-slot WAL-retention control
```

The archive is also documented as operationally separate from the live primary: PostgreSQL recommends placing it where the standby can still reach it even when the primary is down.

This does not claim PostgreSQL invented log shipping or archive-based recovery in 2011.

### 1. 2012–2014 public genealogy: a logical-decoding slot is made persistent and then generalized

The bounded pre-2014 genealogy is source-controlled in [`../evidence/141-postgresql-2012-2014-replication-slot-public-genealogy-deepening.md`](../evidence/141-postgresql-2012-2014-replication-slot-public-genealogy-deepening.md).

The public sequence matters because the February-2014 mainline commit was not the first public appearance of slot vocabulary or of the problem that a replication consumer's continuation state must outlive one connection:

- **15 November 2012:** the `logical changeset generation v3` patch series already exposes `max_logical_slots`.
- **13 December 2012:** the author describes one-time slot setup followed by later use in another walsender and after restart, while explicitly admitting that the then-current patch **did not yet persist enough between restarts**.
- **15 January 2013:** v4 explicitly lists crash/restart persistence work and exposes a permanent replication-slot lifecycle.
- **14 June 2013:** v5 explicitly plans to move from a `logical slot` interface to generic `replication slots` usable by streaming replication.
- **1 February 2014:** mainline `858ec118...` introduces crash-safe replication slots, calls the initially landed form `physical`, and anticipates logical slots with somewhat different properties.

That gives a bounded chronology without turning it into a priority claim:

```text
public logical-slot prototype/design
    != genericization proposal
    != mainline physical-slot integration
    != released PostgreSQL 9.4 contract
    != invention date
```

The December-2012 persistence admission is especially useful:

```text
object is intended to survive restart
    != implementation already persists enough state to do so
```

Likewise:

```text
generic slot identity/lifecycle machinery
    != identical physical-slot and logical-slot retained state
```

Earlier/private precursors, exact patch-by-patch ancestry into mainline, and the later 9.4 logical-slot landing sequence remain open.

### 2. Replication slots enter PostgreSQL as crash-safe continuation state

PostgreSQL commit `858ec11858a914d4c380971985709b6d6b7dd6fc`, committed on **1 February 2014**, explicitly introduces replication slots as a **crash-safe data structure** that can prevent premature removal of WAL needed by a standby. The final PostgreSQL 9.4 release followed on **18 December 2014**.

`mainline implementation date != release date != first proposal/invention date`

### 3. Slot state is not the WAL corpus

In PostgreSQL 9.4 source, a slot has persistent state on disk under `pg_replslot` and an in-memory cache while the server is running. `ReplicationSlotPersistentData` includes `restart_lsn`, described as the oldest LSN that might still be required by the slot.

The slot therefore does not preserve downstream continuity by storing another copy of all WAL inside the slot object. It preserves a **control relation** that tells WAL reclamation how far back history may still be needed.

`slot metadata != protected WAL history`

### 4. One retained frontier can extend the lifetime of many WAL segments

The 9.4 `pg_replication_slots` documentation describes `restart_lsn` as the oldest WAL position that might still be required by the consumer and therefore will not be automatically removed during checkpoints.

The 9.4 implementation computes the oldest valid `restart_lsn` across slots and publishes that requirement to the WAL subsystem. A single sufficiently lagging slot can therefore hold the effective retention floor farther in the past than newer slots.

`small retained frontier != small retention consequence`

### 5. Current inactivity does not erase a future continuation claim

PostgreSQL 9.4 explicitly motivates slots as retaining required WAL even when a standby is disconnected. The user-visible slot view separately reports whether a slot is currently `active`.

`active connection lifetime != slot lifetime != retained-history obligation lifetime`

### 6. The slot's own retention relation has a crash boundary

The 9.4 implementation distinguishes in-memory dirty state from saved state. `ReplicationSlotSave()` serializes slot state to disk; checkpoints save slots; startup restores on-disk slots and recomputes retention constraints. Slot creation uses a temporary path plus synchronization and rename steps.

`PostgreSQL performs persistence operations != every filesystem/controller/device empirically satisfies them under every fault`

### 7. The original precise retention relation could grow without a built-in slot-space bound

The PostgreSQL 9.4 warm-standby documentation contrasts slots with fixed WAL-keeping and archive strategies. Slots can retain only what is known to be needed, but the original design had no built-in slot-space limit.

`retention precision != retention cheapness`

### 8. PostgreSQL 13 makes resource survival capable of defeating continuation preservation

On **7 April 2020**, commit `c6550776394e25c1620bc8258427c8f1d448080d` added `max_slot_wal_keep_size`. Its commit message states the operational motive: excessive slot-retained WAL could make the primary fail by exhausting space. Over-limit slots can be invalidated at checkpoint, allowing old WAL storage to be released.

PostgreSQL 13, released **24 September 2020**, includes this behavior.

```text
consumer says: this history is still needed for continuation
primary policy says: only up to this resource budget remains protected
```

The system resolves the conflict by allowing protection to end and downstream continuation to fail.

### 9. `unreserved` proves physical presence and retention authority can diverge

Commit `b8fd4e02c6d01183bf6def5897ad6cf7766bfff4` refined WAL availability into `reserved`, `extended`, `unreserved`, and `lost`.

For this case, `unreserved` is crucial. Required WAL is no longer protected under the configured slot-retention rules, yet some segments may still exist until checkpoint removal and the consumer can sometimes catch up. `lost` is stronger: some required WAL has been removed and the slot is no longer usable.

```text
needed + protected
    -> needed + no longer protected + still present locally
    -> needed + removed from the slot's required local path
    -> old slot continuation inadmissible
```

Thus:

`physical survival != current retention protection`

and:

`protection withdrawal != completed physical disappearance`

## 2014–2015 deepening — logical consumer acknowledgement and WAL restart are distinct frontiers

The released PostgreSQL 9.4 logical-slot implementation persists both `confirmed_flush`, tied to client acknowledgement, and `restart_lsn`, the oldest WAL position the slot may still require. The same source retains candidate restart working state.

`LogicalConfirmReceivedLocation()` makes the distinction operational: consumer confirmation directly advances `confirmed_flush`; `restart_lsn` moves only when a prepared restart candidate exists and its validity position has been reached by confirmed progress.

```text
consumer acknowledgement frontier (`confirmed_flush`)
    != WAL restart/reclamation frontier (`restart_lsn`)
```

PostgreSQL's 10-August-2015 commit `3f811c2d6f51b13b71adff99e82894dd48cee055`, exposing `confirmed_flush_lsn` in `pg_replication_slots`, explicitly says the two positions have distinct meanings and that `restart_lsn` will commonly be older than the confirmed position.

There is also an observability chronology: 9.4 source already persists `confirmed_flush`, while the separate view column arrives in 2015.

`persistent internal control state != operator-visible telemetry surface`

`2015 view-column introduction != 2015 invention of the underlying persisted state`

Consumer acknowledgement can make a candidate restart position admissible, but acknowledgement is not itself WAL deletion.

Full source/claim separation is recorded in [`../evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md`](../evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md).

## 2018–2020 deepening — physical-slot advancement exposes the retention frontier's own persistence horizon

PostgreSQL added `pg_replication_slot_advance()` on **17 January 2018** for both physical and logical slots. A **24 December 2019** pgsql-hackers report then showed that a physical slot's newly advanced `restart_lsn` could be visible before restart and revert afterward because the physical path had changed only in-memory state without marking persistent slot data dirty.

The **30 January 2020** fix (`b0afdcad21fde1470e6502a376bfaf0e10d384fa`, backpatched through 11) made physical advancement participate in checkpoint-driven slot persistence. PostgreSQL 11.7 and 12.2, released **13 February 2020**, carry the fix. Released PostgreSQL 12 documentation nevertheless keeps the checkpoint boundary explicit: updated slot information is written at the follow-up checkpoint, and a crash can still return the slot to an earlier position.

```text
new restart_lsn returned / visible in memory
    != updated slot frontier already written for restart recovery
    != older WAL physically reclaimed
```

A physical slot's `restart_lsn` is a compact claimant on history. Advancing it can narrow the WAL prefix the slot still requires, but the claimant itself first crosses an in-memory-to-checkpoint persistence boundary. Only separately can WAL-removal machinery later reclaim files.

This closes `function returned != checkpoint-durable slot frontier`, `clean-restart persistence != arbitrary-crash persistence immediately after return`, and `restart_lsn advanced != old WAL already removed`.

Full source/claim separation is recorded in [`../evidence/141-postgresql-2018-2020-physical-slot-advance-persistence-deepening.md`](../evidence/141-postgresql-2018-2020-physical-slot-advance-persistence-deepening.md).

## 2011–2020 deepening — archive retention is an alternate physical-standby continuation carrier

PostgreSQL 9.1 already documents a physical standby trying WAL from an archive, then standby-local WAL, then streaming from the primary. Without an archive, a standby that falls behind beyond `wal_keep_segments` can require a new base backup; with an accessible archive retaining enough segments, it can instead catch up from that archive.

PostgreSQL 9.4 keeps this architecture when replication slots arrive. Its documentation says that `wal_keep_segments` or a replication slot can keep primary-local WAL from recycling too early, but those local retention solutions are not required for catch-up when an accessible archive retains the necessary WAL.

PostgreSQL 13 preserves the same structure using `wal_keep_size`, while separately exposing bounded slot states including `lost`.

This yields a crucial carrier separation:

```text
slot-local protection of primary WAL
    != archive retention of copied WAL
    != standby-local WAL already received
    != slot usability
```

Therefore:

```text
slot is `lost`
    -> the slot is no longer usable

slot is `lost`
    != no equivalent WAL exists in an archive or backup
```

The reverse inference is also blocked:

```text
archive still contains required WAL
    != the old lost slot is automatically resurrected
```

The inspected docs establish an alternate physical-standby replay path, not a procedure for repairing a lost slot in place.

### Base-backup reinitialization is a change of recovery starting point

If required WAL is no longer available through the usable replay path, PostgreSQL documents reinitializing the standby from a new base backup.

```text
old base image + missing WAL interval
    -> old continuation path fails

newer base image
    -> new materialized starting point
    -> only later WAL must be replayed
```

This substitutes newer materialized state for an unavailable historical replay interval. It does **not** reconstruct the missing WAL bytes.

### Archive cleanup is a separate retirement authority

PostgreSQL documents `archive_cleanup_command` / `pg_archivecleanup` for removing archive files no longer required by a standby, while warning that an archive used for backup must still retain files needed to recover from at least the latest base backup.

```text
not needed by one standby
    != not needed by backup recovery
    != safe to retire for every consumer
```

And PostgreSQL 13 WAL-configuration documentation states that when archiving is enabled, a WAL segment must be archived before local recycling/removal.

```text
checkpoint crash-recovery need ended
    != archive handoff obligation already satisfied
    != archive copy retained forever
```

This section is intentionally scoped to physical warm-standby continuation. No logical-slot archive/rebootstrap equivalence is claimed.

Full source/claim separation is recorded in [`../evidence/141-postgresql-2011-2020-wal-archive-alternate-continuation-deepening.md`](../evidence/141-postgresql-2011-2020-wal-archive-alternate-continuation-deepening.md).

## 2024 deepening — failover-slot synchronization makes the retention frontier itself cross-node state

PostgreSQL 17, released **26 September 2024**, adds an explicit logical-slot failover regime. The implementation history separates several steps that the final feature can otherwise make look like one operation.

On **25 January 2024**, commit `c393308b69d229b664391ac583b9e07418d411b6` added the logical-slot `failover` property and explicitly stated that synchronization capability was not yet present. Commit `93db6cbda037f1be9544932bd9a785dabf3ff712` on **22 February 2024** then added the periodic slot sync worker and `sync_replication_slots` on the standby. A separate **8 March 2024** commit, `bf279ddd1c28ce0251446ee90043a4cb96e5db0f`, added the wait relation for selected physical failover candidates; its development name `standby_slot_names` was renamed `synchronized_standby_slots` on **1 July 2024** by `0f934b0739ad28e8e20d8ad22ca80538544ce28a`.

Released documentation adds an admission boundary. A standby can persist a synchronized logical slot only if the WAL and system-catalog rows required by the primary slot are still available there. At failover time, resumability depends on a **persistent** synchronized slot whose `pg_replication_slots.synced` value reached true before promotion.

```text
slot exists on primary
    != `failover = true`
    != standby synchronization enabled
    != synchronized slot admitted/persisted on standby
    != required WAL/catalog substrate available there
    != subscriber state/currentness
    != successful post-promotion continuation
```

The original 9.4 case showed a compact retained claimant constraining reclamation of a much larger WAL corpus. PostgreSQL 17 adds a second-order requirement: if another node may inherit publisher authority, the **claimant itself must survive and remain admissibly current on that future primary**.

`replicated retention frontier != replicated replay substrate`

`failover = true != synced = true != guaranteed subscriber currentness`

When `synchronized_standby_slots` is configured, future failover readiness can also constrain present logical-sender progress. This is a configured relation, not a claim that all PostgreSQL logical replication is synchronous.

EDB's open-source `pg_failover_slots` extension was publicly announced on **18 April 2023** and provides earlier PostgreSQL-ecosystem functional prior art for slot-copy/synchronization behavior. No extension→core code ancestry is asserted.

Full source/claim separation is recorded in [`../evidence/141-postgresql-2024-failover-slot-synchronization-deepening.md`](../evidence/141-postgresql-2024-failover-slot-synchronization-deepening.md).

## Retained state and mechanism

The bounded regime contains at least nine distinct relations:

1. **primary current database state** — what the primary currently serves;
2. **WAL history on the primary** — older change records supporting downstream continuation;
3. **slot identity and persistent control state** — the retained replication-stream object;
4. **consumer-need frontier** — especially `restart_lsn`;
5. **current activity state** — whether a consumer is presently using the slot;
6. **WAL retention/admissibility state** — whether required local history is protected, merely present, or lost under the later bounded policy;
7. **archived WAL copies** — another carrier with separate placement and cleanup authority;
8. **standby-local WAL already received** — another possible replay source;
9. **base-backup materialized state** — the bootstrap point that can be replaced when an old replay path is irreparable.

The central lifecycle is:

```text
consumer falls behind or disconnects
    -> persistent slot may remain
    -> restart_lsn stays behind primary progress
    -> primary-local WAL remains protected
    -> retained-history volume grows

PostgreSQL 13, if a finite cap is configured:
    -> retention budget can be exceeded
    -> WAL may become unreserved
    -> checkpoint can remove required local WAL
    -> slot becomes lost / unusable

independently, for a physical standby:
    -> archive may still contain required replay history
    -> standby may catch up from archive if the interval is sufficient
    -> otherwise standby must be reinitialized from a new base backup
```

## Engineering reconstruction

### A. Current-state sufficiency and continuation-history sufficiency are different

The primary may have everything required to serve its own current database state while an older WAL segment is still indispensable to a lagging downstream consumer.

`primary can continue serving != old WAL is reclaimable`

### B. A frontier can retain history without being history

A `restart_lsn` is compact second-order state. It says which earlier history remains possibly necessary. Its semantic weight is larger than its storage size because it governs reclamation of a potentially large log prefix.

`small metadata footprint != small retention consequence`

### C. Downstream absence can remain operationally present as an obligation

A disconnected consumer is not currently executing on the primary, yet the slot makes its future need operationally effective in the present by withholding WAL reclamation.

### D. Retention obligation and retention capacity can conflict

PostgreSQL 9.4 privileges continuation strongly enough that slot-held WAL lacks a built-in space cap. PostgreSQL 13 adds a policy that can withdraw protection rather than let that relation consume unlimited primary storage.

`history still useful != infrastructure will preserve it without limit`

### E. Slot persistence does not imply continuation persistence

The 2020 regime gives a direct counterexample. The slot can still exist while its required WAL is `lost` and the slot unusable.

`slot presence != replay-substrate presence != continuation admissibility`

### F. `unreserved` separates eligibility for reclamation from completed reclamation

When WAL becomes `unreserved`, it has crossed a policy boundary before it has necessarily crossed a physical removal boundary.

`retirement authority != completed retirement`

### G. One continuation need can be served by multiple carriers

For the physical standby path, a needed WAL range can be available on the primary, in standby-local WAL, or in an accessible archive. The logical replay dependency is therefore distinct from any single physical carrier.

`local carrier loss != global history loss`

But:

`history survives somewhere != current slot/configuration can consume it`

### H. Rebootstrap substitutes materialized state for unavailable history

A new base backup can establish a later materialized starting point after the old replay interval has become unavailable. This is a new continuation basis, not a reconstruction of the missing history.

`new materialized state != recovered missing WAL`

## Cross-case comparison

### Case 58 — Raft snapshotting

Raft permits committed log history to become dispensable after equivalent stable state plus boundary/membership metadata exists; a follower that needs compacted history can receive `InstallSnapshot`.

PostgreSQL slots normally preserve replay history for a lagging consumer, but the newly grounded base-backup path shows a bounded functional analogue when that history is unavailable: a newer materialized state can replace the old replay starting point.

```text
Raft:
old log unavailable/compacted -> transfer snapshot -> resume from snapshot boundary

PostgreSQL physical standby:
required WAL unavailable -> obtain newer base backup -> resume with later WAL
```

This is not a genealogy and does not imply the protocols solve the same consistency problem.

### Case 57 — Bigtable redo/materialization

Case 57's redo points delimit history needed to reconstruct a tablet's volatile/current materialization. PostgreSQL `restart_lsn` can delimit history needed by another replication consumer, while base backup plus later WAL gives a separate materialization-plus-redo decomposition.

`local recovery frontier != remote-consumer continuation frontier`

### Case 137 — LevelDB obsolete-file liveness

LevelDB can keep a superseded SSTable because a still-live `Version`/iterator references it. PostgreSQL can keep otherwise old WAL because a persistent slot still claims a downstream need.

`locally superseded/old != reclaimable while another live relation still depends on it`

### Case 41 / distributed deletion cases

Cassandra tombstones and similar negative evidence can remain because a disconnected/stale replica may later reappear. PostgreSQL slots likewise show future distributed continuation needs extending the life of otherwise old state.

The analogy stops at **future participant need constraining reclamation**.

### Case 130 — LTO access-path survival

Case 130 distinguishes surviving media from an actually usable reader path. The archive deepening supplies a distributed counterpart:

`history survives in some carrier != the current continuation path is usable`

The media, software, and protocol mechanisms are otherwise unrelated.

## Terminology and anti-anachronism

### PostgreSQL 9.1 vocabulary

Relevant pre-slot terms include:

- WAL archive;
- `restore_command`;
- `wal_keep_segments`;
- streaming replication;
- base backup;
- `archive_cleanup_command`.

Do not rewrite this 2011 behavior in later replication-slot vocabulary.

### PostgreSQL 2012–2013 public development vocabulary

The bounded development terms include `logical slot`, `max_logical_slots`, `slot-id` / `slotname`, `permanent replication slot`, and evolving logical-replication commands. These terms document a development series and must not be silently rewritten as the final 9.4 API.

### PostgreSQL 9.4 vocabulary

Relevant released terms include `replication slot`, physical/logical slot, `restart_lsn`, `active`, `pg_replslot`, WAL segments, checkpoints, archive, and base backup.

### PostgreSQL 13 additions

Relevant later terms include `max_slot_wal_keep_size`, `wal_status`, `reserved`, `extended`, `unreserved`, and `lost`.

Do not rewrite the 2014 design as though it already had the 2020 cap or four-state availability model.

Likewise, project terms such as `continuation admission`, `retention frontier`, `history-liveness claimant`, `alternate carrier`, and `retirement authority` are **engineering reconstruction vocabulary**, not PostgreSQL historical vocabulary.

## Philosophical interpretation — bounded

The case contributes two modest temporal observations.

First, a WAL segment's technical future can depend on a participant that is currently absent. The slot makes that future-oriented claim on the past durable across disconnection and restart.

Second, the archive deepening shows that “forgotten here” and “forgotten everywhere” are different propositions. One retained past can have several carriers with different custodians and retirement rules. A system can also abandon one continuity path and establish another by choosing a newer materialized starting point, without reconstructing the missing past.

PostgreSQL 13 supplies the counterweight: any one retention relation can still be bounded by resource policy.

These are project interpretations, not PostgreSQL historical vocabulary and not equations with human memory, archival promises, or tertiary retention.

## Failure and forgetting

- **Consumer lag grows:** more historical WAL can remain live because the frontier stays old.
- **Consumer disconnects:** the slot can continue retaining history; connection loss is not automatically continuation loss.
- **Primary crashes/restarts:** persistent slot state can restore the retention relation.
- **Changed slot state not yet saved:** in-memory and crash-surviving control state are distinct.
- **9.4 slot retained indefinitely:** local WAL space can become the failure resource.
- **v13 configured cap exceeded:** protection can be withdrawn to protect primary capacity.
- **`unreserved`:** required local WAL may still exist but is no longer protected from checkpoint removal.
- **`lost`:** the slot's required WAL has been removed from the relevant local path and the slot is no longer usable.
- **Archive survives:** a physical standby may still have an alternate catch-up carrier if the needed interval is complete and accessible.
- **Archive gap / cleanup removes needed WAL:** that alternate replay path can fail independently of slot state.
- **All usable replay paths missing:** physical standby reinitialization from a new base backup is required by the documented warm-standby path.
- **Slot dropped/invalidated or local WAL removed:** this changes continuation/replay authority; it does not prove secure media erasure or global absence of all copies.
- **Underlying storage violates persistence assumptions:** slot/archive guarantees are then outside the contract directly established by PostgreSQL source/docs alone.

## Counterexamples and stop conditions

- **Public prototype != released contract.** The 2012–2013 patch series is historical-development evidence, not a substitute for PostgreSQL 9.4 documentation.
- **Persistence intent != implemented crash safety.** The December-2012 author reply explicitly says the patch did not yet persist enough across restart.
- **Generic slot abstraction != identical slot types.** Physical and logical slots have different retained-state and recovery semantics.
- **Public chronology != invention priority.** The dates establish bounded PostgreSQL floors only.
- **Replication slot != replica.** The slot is control state about a stream, not another full database copy.
- **Replication slot != WAL corpus.** It governs retention of WAL stored elsewhere.
- **Replication slot != WAL archive.** The archive is a separate copy carrier with separate cleanup policy.
- **`restart_lsn` != full replay history.** It is a frontier, not the retained records themselves.
- **`confirmed_flush_lsn` != `restart_lsn`.** Logical consumer acknowledgement and oldest-needed WAL are distinct frontiers.
- **Consumer acknowledgement != completed WAL reclamation.** Confirmation can permit frontier movement; it is not deletion.
- **Current primary state != sufficient downstream replay history.** A remote consumer can still need old WAL.
- **Inactive != no retention obligation.** Disconnected consumers are a core slot use case.
- **Crash-safe slot != immortal slot.** Administrative drop and resource-bounded invalidation remain possible.
- **Precise retention != bounded storage cost.** PostgreSQL 9.4 demonstrates the contrary.
- **WAL present != WAL protected.** PostgreSQL 13 `unreserved` is a direct counterexample.
- **WAL unprotected != WAL already removed.** The consumer may still catch up before removal.
- **Slot exists != slot usable.** A `lost` slot can remain observable while its required replay history is gone from the protected local path.
- **Slot `lost` != WAL globally nonexistent.** An independent archive/backup may still contain equivalent history.
- **Archived WAL exists != lost slot automatically usable again.** No such repair procedure is established here.
- **Physical-standby archive recovery != logical-slot archive recovery.** Do not generalize across slot types without evidence.
- **Archive handoff != indefinite archive retention.** Cleanup and external lifecycle policy remain separate.
- **Safe to clean for one standby != safe for backup recovery.** PostgreSQL explicitly distinguishes the claims.
- **New base backup != reconstruction of missing WAL.** It establishes a later materialized starting point.
- **WAL removal != secure deletion.** No media sanitization claim follows.
- **PostgreSQL replication retention != Raft snapshotting.** The comparison is functional only.
- **2020 resource-bound semantics != 2014 design vocabulary.** Later evolution remains later.

## Prior art and novelty boundary

This case does not claim PostgreSQL invented log retention, replication progress, replay positions, log shipping, WAL archiving, base-backup recovery, or keeping history for lagging replicas.

The 2011 archive deepening strengthens the local anti-novelty boundary: archive-backed physical-standby catch-up and base-backup reinitialization were already released PostgreSQL behavior before replication slots existed.

The 2012–2014 public genealogy then shows an evolving logical-slot mechanism, an explicit persistence shortfall, crash/restart-persistence work, genericization intent, and the mainline physical-slot landing. It does **not** establish first invention, private origins, or non-PostgreSQL ancestry.

The source-controlled contribution is therefore narrower:

> **PostgreSQL 9.4 gives a particularly explicit crash-safe mechanism in which a retained consumer-need frontier constrains primary-local WAL reclamation even across disconnection; PostgreSQL 13 gives an explicit later counterexample in which resource protection can withdraw that guarantee, while the older WAL-archive path demonstrates that loss of primary-local protection or even loss of slot usability is not equivalent to global disappearance of every possible replay carrier.**

A complete genealogy belongs in `tmzncty/computing-archaeology`, not here.

## Uncertainty and next evidence

The bounded case is grounded, while these remain open:

1. pre-November-2012 private/public slot precursors plus exact patch-by-patch ancestry from the 2012–2013 logical-slot work into the February-2014 generic/physical implementation and later 9.4 logical-slot landing;
2. physical-slot advancement and release-by-release semantics beyond the grounded logical `confirmed_flush` / `restart_lsn` split and 2018–2020 persistence fix;
3. **narrowed archive/rebootstrap debt:** exact supported behavior if a physical slot is `lost` while an independent archive still holds the nominally required WAL, whether any supported sequence can reuse that archive without dropping/recreating the slot, logical-slot-specific archive/rebootstrap semantics, and archive-gap fault injection;
4. post-17 failover-slot fixes, multi-standby/cascading evolution, promotion fault injection, and production failover traces;
5. named production incidents or measurements of WAL accumulation and primary disk-pressure failure;
6. controlled checkpoint/slot-loss/archive-gap fault injection;
7. lower-layer filesystem/device/archive persistence testing for slot save, WAL removal, archive handoff, and external retention;
8. full replication/log-retention/archive genealogy, coordinated with `computing-archaeology`.

## Related repository boundary

`tmzncty/computing-archaeology` was freshly searched for `PostgreSQL replication slot`, `restart_lsn`, `WAL archive`, and `restore_command`; no dedicated overlapping study was found.

If the broad history of PostgreSQL WAL, log shipping, streaming replication, backup tooling, logical decoding, replication slots, failover slots, or archive implementations is developed there later, this case should link to it rather than reproduce it.

`technical-retention` keeps the narrower question:

> **Which retained relation makes otherwise old history continue to count as live, which carrier currently embodies that history, what event or policy ends each carrier's protection, and does loss of one continuation path coincide with physical disappearance everywhere?**

## Evidence links

- [Evidence 141 — PostgreSQL 2014–2020 replication-slot WAL-retention grounding](../evidence/141-postgresql-2014-2020-replication-slot-wal-retention-grounding.md)
- [Evidence 141 deepening — PostgreSQL 2012–2014 replication-slot public genealogy](../evidence/141-postgresql-2012-2014-replication-slot-public-genealogy-deepening.md)
- [Evidence 141 deepening — PostgreSQL 17 failover-slot synchronization](../evidence/141-postgresql-2024-failover-slot-synchronization-deepening.md)
- [Evidence 141B — logical-slot `confirmed_flush` vs `restart_lsn` dual frontier](../evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md)
- [Evidence 141 deepening — physical-slot manual-advance persistence](../evidence/141-postgresql-2018-2020-physical-slot-advance-persistence-deepening.md)
- [Evidence 141 deepening — 2011–2020 WAL archive alternate continuation](../evidence/141-postgresql-2011-2020-wal-archive-alternate-continuation-deepening.md)
- [Case 58 — Raft snapshot/log compaction](58-raft-snapshot-log-compaction.md)
- [Case 57 — Bigtable tablet log/memtable recovery](57-google-bigtable-tablet-log-memtable-recovery.md)
- [Case 137 — LevelDB MANIFEST/CURRENT](137-leveldb-v17-manifest-current-recovery.md)
- [PostgreSQL 9.1 warm-standby documentation](https://www.postgresql.org/docs/9.1/warm-standby.html)
- [PostgreSQL commit `858ec118...`](https://github.com/postgres/postgres/commit/858ec11858a914d4c380971985709b6d6b7dd6fc)
- [PostgreSQL 9.4 warm-standby / replication-slot documentation](https://www.postgresql.org/docs/9.4/warm-standby.html)
- [PostgreSQL commit `c6550776...`](https://github.com/postgres/postgres/commit/c6550776394e25c1620bc8258427c8f1d448080d)
- [PostgreSQL commit `b8fd4e02...`](https://github.com/postgres/postgres/commit/b8fd4e02c6d01183bf6def5897ad6cf7766bfff4)
- [PostgreSQL 13 replication-slot view](https://www.postgresql.org/docs/13/view-pg-replication-slots.html)
- [PostgreSQL 13 WAL configuration](https://www.postgresql.org/docs/13/wal-configuration.html)