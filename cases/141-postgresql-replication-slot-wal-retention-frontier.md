# Case 141 — PostgreSQL Replication Slots: WAL Retention Frontier and Continuation Admission

**Status:** grounded  
**Claim layer:** historical record + engineering reconstruction + bounded functional analogy + bounded philosophical interpretation  
**Primary regime:** PostgreSQL pre-slot archive-backed standby operation (9.1, 2011), public logical-slot / replication-slot development (2012–2014), PostgreSQL 9.4 replication-slot release (2014), physical-slot frontier persistence work (2018–2020), PostgreSQL 13 resource-bound invalidation and physical-slot rejoin behavior (2020–2021), and PostgreSQL 17 logical failover-slot synchronization (2024)  
**Evidence records:**

- [`../evidence/141-postgresql-2014-2020-replication-slot-wal-retention-grounding.md`](../evidence/141-postgresql-2014-2020-replication-slot-wal-retention-grounding.md)
- [`../evidence/141-postgresql-2012-2014-replication-slot-public-genealogy-deepening.md`](../evidence/141-postgresql-2012-2014-replication-slot-public-genealogy-deepening.md)
- [`../evidence/141-postgresql-2024-failover-slot-synchronization-deepening.md`](../evidence/141-postgresql-2024-failover-slot-synchronization-deepening.md)
- [`../evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md`](../evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md)
- [`../evidence/141-postgresql-2018-2020-physical-slot-advance-persistence-deepening.md`](../evidence/141-postgresql-2018-2020-physical-slot-advance-persistence-deepening.md)
- [`../evidence/141-postgresql-2011-2020-wal-archive-alternate-continuation-deepening.md`](../evidence/141-postgresql-2011-2020-wal-archive-alternate-continuation-deepening.md)
- [`../evidence/141-postgresql-13-lost-physical-slot-archive-rejoin-deepening.md`](../evidence/141-postgresql-13-lost-physical-slot-archive-rejoin-deepening.md)

## Summary

This case asks a narrow distributed-log retention question:

> **Can history that is no longer needed for the primary's immediate current state remain non-reclaimable because a lagging or disconnected future consumer still needs it, and what happens when the primary later gains authority to sacrifice that continuation relation to bound local storage use?**

PostgreSQL 9.4 supplies a clean mechanism. A **replication slot** is persistent control state. Its `restart_lsn` records the oldest WAL position that might still be required by the slot's consumer. PostgreSQL aggregates slot requirements into the WAL-removal horizon, so old WAL remains available even while the consumer is not currently connected.

But the retained objects and continuation paths are not one thing:

```text
primary current database state
        != replication-slot control object
        != consumer-need frontier (`restart_lsn`)
        != primary-local WAL history governed by that frontier
        != archived WAL copies retained elsewhere
        != standby-local WAL already received
        != base-backup materialized state
        != current connection/activity state
```

PostgreSQL 9.1 already documented physical standby catch-up through an independently accessible WAL archive before replication slots existed. Therefore a primary-local slot protection failure and global disappearance of the corresponding history are not the same proposition.

PostgreSQL 13 makes a second conflict explicit. `max_slot_wal_keep_size` can cap how much WAL a slot is allowed to protect. The later `wal_status` state machine distinguishes `reserved`, `extended`, `unreserved`, and `lost`. `unreserved` separates withdrawal of retention protection from completed local removal. `lost` means some WAL required by the old slot frontier has been removed.

The newest source-level deepening adds an important qualification to the public phrase “the slot is no longer usable.” In PostgreSQL 13 physical replication, invalidation clears and persists the old `restart_lsn` but does **not** drop the named slot object. Physical `START_REPLICATION` deliberately does not validate that old slot frontier; it trusts the client's requested start point and later fails only if the requested WAL is unavailable. If an independent archive lets the standby replay the missing interval until it reaches a start point still available on the primary, a later physical stream can use the same slot name, and standby flush feedback can install a new, later `restart_lsn`.

The precise decomposition is therefore:

```text
old slot-protected continuation frontier lost
    != slot object deleted
    != every equivalent WAL copy globally absent
    != same physical slot name permanently unusable

archive bridges missing history for standby
    -> later start point becomes streamable
    -> physical feedback establishes new restart_lsn
    -> slot-based protection resumes from a later frontier
```

This does **not** restore the old missing primary-local WAL or make the old retention obligation continuous. The same control object can outlive one failed continuation claim and later carry another.

The case's central retention distinction is now:

```text
history still needed by consumer
    != history currently protected on primary
    != history physically present on primary
    != equivalent history present in another carrier
    != old continuation relation still valid
    != slot object identity still present
    != a later continuation relation can be established
```

The 2020 policy is later history and must not be projected back into 2014 vocabulary or semantics. Likewise, physical archive/rejoin behavior must not be projected onto logical decoding without direct evidence.

## Research questions

1. What exactly is retained by a PostgreSQL replication slot?
2. How does a small `restart_lsn` frontier govern the lifetime of a much larger WAL corpus?
3. Does a disconnected consumer stop constraining retention? No — under the 9.4 slot relation, disconnection and retention obligation are separate.
4. Does crash-safe slot state imply all required WAL necessarily survives forever? No — PostgreSQL 13 provides a direct counterexample.
5. What is the difference among `reserved`, `unreserved`, physically present, and `lost` WAL?
6. Can WAL needed by a physical standby survive outside the primary's slot-governed local corpus? Yes — an accessible archive is a separate carrier if it retains a sufficient replay interval.
7. Does `wal_status = lost` mean the physical slot object has been destroyed forever? No — inspected PostgreSQL 13 source separates invalidated old frontier from persistent slot identity and permits later physical feedback to install a new frontier.
8. Can SQL `pg_replication_slot_advance()` repair that invalidated frontier? No — PostgreSQL 13 explicitly rejects advance when `restart_lsn` is invalidated.
9. Is slot invalidation or local WAL removal technical erasure? No — both are weaker than media sanitization and weaker than global absence of all copies.
10. How does this differ from Raft snapshot transfer, Bigtable redo-point recovery, LevelDB file liveness, and other retention cases?
11. What belongs here versus broader PostgreSQL/WAL history in `computing-archaeology`?

## Source ladder

| Evidence | Date | Strength | Use here |
|---|---:|---|---|
| PostgreSQL 9.1 warm-standby docs | 2011 release series | `H/P` | pre-slot archive/local/stream fallback, base-backup reinitialization, archive cleanup |
| PostgreSQL pgsql-hackers `logical changeset generation` v3–v5 | 2012–2013 | `H/P` | public logical-slot vocabulary, restart persistence gap, genericization intent |
| PostgreSQL `858ec118...`, “Introduce replication slots” | 2014-02-01 | `H/P` | crash-safe slot purpose and mainline physical-slot retention relation |
| PostgreSQL 9.4 release/docs/source | 2014-12-18 release | `H/P` | released slot contract; persistent slot fields; archive remains alternate physical carrier |
| PostgreSQL `pg_replication_slot_advance()` introduction/fix evidence | 2018–2020 | `H/P` | physical frontier movement and checkpoint persistence boundary |
| PostgreSQL `c6550776...` | 2020-04-07 | `H/P` | `max_slot_wal_keep_size`, checkpoint invalidation, disk-exhaustion motivation |
| PostgreSQL `b8fd4e02...` | 2020-06-24 | `H/P` | `reserved` / `extended` / `unreserved` / `lost` refinement |
| PostgreSQL 13 docs and `REL_13_0` / `REL_13_3` source | 2020–2021 regime | `H/P` | invalidation fields, physical `START_REPLICATION`, feedback-driven new frontier, SQL advance rejection |
| PostgreSQL bug #17103 | 2021-07-13 | `H/P*` | contemporary 13.3 operator witness: slot lag -> archive catch-up -> streaming restored |
| PostgreSQL 17 failover-slot commits/docs | 2024 | `H/P` | cross-node persistence/admission of logical slot state |

`H/P*` marks a primary historical operator report rather than a controlled project test. It corroborates the source-grounded mechanism but does not replace it.

## Historical record

### 0. 2011 pre-slot boundary: archive-backed standby catch-up already exists

PostgreSQL 9.1, released **12 September 2011**, documents physical standby operation as able to recover WAL from an archive via `restore_command`, from WAL already present on the standby, or by streaming from the primary.

The standby retry model is already multi-carrier:

```text
archive
    -> standby-local WAL
    -> streaming from primary
    -> on stream failure, retry archive again
```

Without file-based continuous archiving, a standby that falls behind beyond available primary WAL may need a new base backup. With an accessible archive retaining enough segments, the standby can catch up without depending on the primary's old local WAL.

This predates replication slots:

```text
archive-backed physical-standby continuation
    predates
replication-slot WAL-retention control
```

The archive is operationally distinct from the live primary; PostgreSQL recommends putting it somewhere the standby can reach even when the primary is down.

This does not claim PostgreSQL invented log shipping or archive-based recovery in 2011.

### 1. 2012–2014 public genealogy: logical-slot work becomes persistent, then generic

The bounded pre-2014 genealogy is source-controlled in [`../evidence/141-postgresql-2012-2014-replication-slot-public-genealogy-deepening.md`](../evidence/141-postgresql-2012-2014-replication-slot-public-genealogy-deepening.md).

The public sequence matters:

- **15 November 2012:** `logical changeset generation v3` exposes `max_logical_slots`.
- **13 December 2012:** the author describes one-time slot setup followed by later use in another walsender and after restart, while explicitly admitting that the current patch does not yet persist enough between restarts.
- **15 January 2013:** v4 adds explicit crash/restart persistence work and permanent slot lifecycle.
- **14 June 2013:** v5 plans to move from a `logical slot` interface to generic `replication slots` usable by streaming replication.
- **1 February 2014:** mainline `858ec118...` introduces crash-safe replication slots, initially in physical form, while anticipating logical slots with different properties.

Thus:

```text
public logical-slot prototype/design
    != genericization proposal
    != mainline physical-slot integration
    != released PostgreSQL 9.4 contract
    != invention date
```

### 2. 2014: replication slots enter mainline as crash-safe continuation state

Commit `858ec11858a914d4c380971985709b6d6b7dd6fc`, committed on **1 February 2014**, explicitly introduces replication slots as a crash-safe data structure able to prevent premature removal of WAL needed by a standby. PostgreSQL 9.4 was released on **18 December 2014**.

`mainline implementation date != release date != first proposal/invention date`

### 3. Slot state is not the WAL corpus

In PostgreSQL 9.4, a slot has persistent state under `pg_replslot` and in-memory state while the server is running. `ReplicationSlotPersistentData` includes `restart_lsn`, the oldest LSN that might still be required.

The slot therefore preserves continuity by retaining a **control relation** that constrains WAL reclamation. It does not contain another copy of all protected WAL.

`slot metadata != protected WAL history`

### 4. One retained frontier can extend the lifetime of many WAL segments

The implementation computes the oldest valid `restart_lsn` across slots and publishes that requirement to the WAL subsystem. A single lagging slot can therefore hold the effective retention floor far in the past.

`small retained frontier != small retention consequence`

### 5. Current inactivity does not erase a future continuation claim

PostgreSQL explicitly motivates slots as retaining required WAL even when a standby is disconnected. The view separately reports whether a slot is currently `active`.

`active connection lifetime != slot lifetime != retained-history obligation lifetime`

### 6. The slot's own retention relation has a persistence boundary

The implementation distinguishes in-memory dirty state from saved state. `ReplicationSlotSave()` serializes slot data; checkpoints save slots; startup restores on-disk slots and recomputes retention constraints.

`PostgreSQL performs persistence operations != every lower layer empirically satisfies them under every fault`

### 7. The original precise relation could consume unbounded local WAL space

PostgreSQL 9.4 can retain exactly the history a slot is known to need, but the original design does not provide a built-in per-slot WAL-space cap.

`retention precision != retention cheapness`

### 8. 2014–2015: logical acknowledgement and WAL restart are distinct frontiers

Logical slots persist both `confirmed_flush` and `restart_lsn`.

`LogicalConfirmReceivedLocation()` makes the distinction operational: consumer confirmation advances `confirmed_flush`; `restart_lsn` moves only when a prepared restart candidate has become valid.

```text
consumer acknowledgement frontier (`confirmed_flush`)
    != WAL restart/reclamation frontier (`restart_lsn`)
```

PostgreSQL's **10 August 2015** commit `3f811c2d6f51b13b71adff99e82894dd48cee055`, exposing `confirmed_flush_lsn` in `pg_replication_slots`, explicitly says the positions have different meanings and that `restart_lsn` will commonly be older.

`persistent internal control state != operator-visible telemetry surface`

### 9. 2018–2020: physical-slot advancement exposes the frontier's own persistence horizon

PostgreSQL added `pg_replication_slot_advance()` on **17 January 2018**. A **24 December 2019** report showed that a physical slot's newly advanced `restart_lsn` could be visible before restart and revert afterward because the physical path changed only in-memory state without marking persistent slot data dirty.

The **30 January 2020** fix `b0afdcad21fde1470e6502a376bfaf0e10d384fa`, backpatched through PostgreSQL 11, made physical advancement participate in checkpoint-driven slot persistence.

```text
new restart_lsn returned / visible in memory
    != updated slot frontier already written for restart recovery
    != older WAL physically reclaimed
```

### 10. 2020: resource survival can defeat continuation preservation

On **7 April 2020**, commit `c6550776394e25c1620bc8258427c8f1d448080d` added `max_slot_wal_keep_size`. Its commit message gives the operational motive: excessive slot-retained WAL can make the primary fail by exhausting storage. Over-limit slots are invalidated at checkpoint so storage can be released.

PostgreSQL 13, released **24 September 2020**, includes this behavior.

```text
consumer says: history is still needed for continuation
primary policy says: only this much local history may remain protected
```

The system can choose primary resource survival over preserving the old continuation relation.

### 11. `unreserved` separates protection authority from physical presence

Commit `b8fd4e02c6d01183bf6def5897ad6cf7766bfff4` refined WAL availability into `reserved`, `extended`, `unreserved`, and `lost`.

`unreserved` means required WAL is no longer protected under the configured slot-retention rule, while some segments may still exist until removal. The consumer can sometimes catch up before those bytes disappear.

```text
needed + protected
    -> needed + unprotected + still present
    -> needed + removed from the old local continuation path
```

`physical survival != current retention protection`

`protection withdrawal != completed physical disappearance`

### 12. Archive retention remains an alternate physical-standby continuation carrier

PostgreSQL 9.4 and 13 retain the same architecture as 9.1: an accessible archive can carry a replay interval independently of slot-governed local WAL.

```text
slot-local protection of primary WAL
    != archive retention of copied WAL
    != standby-local WAL already received
    != slot object state
```

If no usable replay path remains, PostgreSQL documents reinitializing the physical standby from a new base backup.

`new base backup != reconstruction of missing WAL`

Archive cleanup is also a separate retirement authority. PostgreSQL warns that files unnecessary for one standby may still be needed for backup recovery.

### 13. PostgreSQL 13 invalidation clears an old physical frontier without dropping the slot object

The PostgreSQL 13.3 source makes the `lost` transition concrete. `InvalidateObsoleteReplicationSlots()`:

1. identifies a slot whose `restart_lsn` lies behind the removal boundary;
2. terminates an active process using that too-far-behind slot;
3. copies the old frontier into `invalidated_at`;
4. clears `restart_lsn` to `InvalidXLogRecPtr`;
5. marks and saves the slot.

The source does **not** drop the slot object.

```text
old restart frontier invalidated
    != named slot object deleted
```

`ReplicationSlotPersistentData` explicitly keeps both `restart_lsn` and `invalidated_at` in state that survives shutdown and crash.

### 14. `lost` is derived from current frontier/availability state, not an immutable tombstone bit

In PostgreSQL 13.3 `pg_replication_slots`, an invalid `restart_lsn` together with a valid `invalidated_at` is treated as definite removed/lost state. If `restart_lsn` is valid, however, the view evaluates current WAL availability from that frontier.

This means `lost` is an observable state of the current continuation relation, not a separate immutable bit that permanently destroys slot identity.

### 15. Physical `START_REPLICATION` deliberately does not trust the old slot frontier as its start point

When PostgreSQL 13.3 starts physical replication with a named slot, `StartReplication()` acquires that slot and rejects logical slots in this path. It then explicitly states that it does **not** need to verify the slot's `restart_lsn`; instead it relies on the caller's requested start point and will fail later if the needed WAL segment does not exist.

Therefore:

```text
slot retention frontier
    != client-requested physical stream start point
    != actual WAL availability at that requested point
```

This is the source-level opening through which a physical slot whose old frontier was invalidated can later participate in streaming from a later still-present point.

### 16. Physical standby feedback can establish a new frontier in the same slot object

Standby status replies contain write, flush, and apply positions. If a physical slot is active and a valid flush position is reported, PostgreSQL 13.3 calls `PhysicalConfirmReceivedLocation(flushPtr)`.

That function does not require the previous `restart_lsn` to be valid. It can assign the reported flush LSN to `slot->data.restart_lsn`, mark the slot dirty, and recompute required WAL.

So:

```text
old frontier invalidated
    + later physical stream succeeds
    + standby confirms later flush position
    -> same slot object can acquire later restart_lsn
```

This is a **new retention relation beginning at a later frontier**, not restoration of the old missing range.

### 17. Re-established runtime protection has its own persistence horizon

`PhysicalConfirmReceivedLocation()` marks the new position dirty but does not synchronously call `ReplicationSlotSave()` for every acknowledgement.

```text
later restart_lsn active for runtime retention
    != later restart_lsn already persisted for immediate-crash recovery
```

This extends the earlier physical-slot persistence lesson: even requalification of a failed relation has a volatile-to-persistent boundary.

### 18. SQL `pg_replication_slot_advance()` is not the invalidated-slot repair path

PostgreSQL 13.3 explicitly rejects `pg_replication_slot_advance()` when the slot's `restart_lsn` is invalid, with detail saying the slot has never reserved WAL or has been invalidated.

Thus:

```text
operator metadata advance
    != live physical-consumer feedback
```

Only the latter inspected path can establish the new physical frontier after invalidation.

### 19. Archive catch-up can bridge the missing interval before same-slot physical streaming resumes

The PostgreSQL 13 standby retry loop tries archive recovery, then local `pg_wal`, then streaming from the last valid record found. If streaming fails, it returns to the archive and retries.

With `primary_slot_name` configured, the streaming phase uses the named physical slot. This creates the bounded rejoin sequence:

```text
old slot frontier lost
    -> old streaming request cannot be served
    -> restore_command supplies missing archived WAL
    -> standby replay reaches later R1
    -> R1 remains available on primary
    -> standby requests physical stream from R1 using same slot name
    -> flush feedback installs later restart_lsn
    -> slot protection resumes from R1 or later
```

The archive is not copied into the slot and need not repopulate removed primary-local WAL.

### 20. A PostgreSQL 13.3 field report records this archive-to-streaming recovery pattern

Bug #17103, reported **13 July 2021**, describes a PostgreSQL 13.3 deployment using one physical streaming replica, a slot, `max_slot_wal_keep_size`, and working archiving.

The operator reports that when `safe_wal_size` went negative, streaming stopped; the replica switched to archive recovery; after catching up from the archive, replication was restored with no delay.

The thread's main subject was a separate WAL-removal problem, so this is not a controlled slot-state experiment. It is nevertheless a contemporary named-version witness matching the source-grounded archive/rejoin path.

`production witness != complete protocol trace`

### 21. 2024: failover-slot synchronization makes the frontier itself cross-node state

PostgreSQL 17, released **26 September 2024**, adds an explicit logical-slot failover regime.

The development sequence is itself layered:

- **25 January 2024**, `c393308b...`: logical-slot `failover` property, without synchronization capability yet;
- **22 February 2024**, `93db6cbd...`: periodic slot sync worker and `sync_replication_slots`;
- **8 March 2024**, `bf279ddd...`: wait relation for selected physical failover candidates;
- **1 July 2024**, `0f934b07...`: rename to `synchronized_standby_slots`.

Released documentation adds an admission boundary: a standby can persist a synchronized logical slot only if required WAL and catalog rows are still available there. Post-promotion resumability depends on a persistent synchronized slot that reached `synced = true` before promotion.

```text
slot exists on primary
    != `failover = true`
    != synchronization enabled
    != synchronized slot admitted/persisted on standby
    != required replay substrate available there
    != subscriber currentness
    != successful post-promotion continuation
```

The 9.4 case begins with a compact claimant that constrains a larger WAL corpus. PostgreSQL 17 adds a second-order retention requirement: when another node may inherit publisher authority, the claimant itself must become admissible persistent state there.

## Retained state and mechanism

The bounded regime contains at least twelve distinct relations:

1. **primary current database state** — what the primary currently serves;
2. **primary-local WAL corpus** — older change records supporting replay;
3. **slot object identity** — the named retained replication control object;
4. **old consumer-need frontier** — especially the old `restart_lsn`;
5. **invalidation evidence** — `invalidated_at` retaining the failed old frontier;
6. **current activity state** — whether a consumer is presently using the slot;
7. **WAL retention/admissibility state** — protected, unreserved, removed/lost;
8. **archived WAL copies** — another carrier with separate placement and cleanup authority;
9. **standby-local WAL** — another possible replay source;
10. **base-backup materialized state** — a replaceable bootstrap point;
11. **client-requested streaming start point** — a physical protocol input distinct from slot retention frontier;
12. **later re-established `restart_lsn`** — a new protection relation after successful physical rejoin.

A compact lifecycle is:

```text
consumer falls behind or disconnects
    -> slot persists
    -> restart_lsn stays old
    -> primary-local WAL stays protected
    -> retained-history volume grows

finite PostgreSQL 13 cap exceeded
    -> WAL may become unreserved
    -> checkpoint may remove old required WAL
    -> invalidation preserves old frontier in invalidated_at
    -> restart_lsn cleared
    -> old continuation relation becomes lost

independently for physical standby
    -> archive may still carry missing interval
    -> standby may replay archive until later overlap with primary
    -> same named physical slot may be acquired for later stream
    -> standby flush feedback may install later restart_lsn
    -> new protection relation begins
```

## Engineering reconstruction

### A. Current-state sufficiency and continuation-history sufficiency differ

The primary can have everything required to serve its own current database state while old WAL remains indispensable to a lagging downstream consumer.

`primary can continue serving != old WAL is reclaimable`

### B. A frontier can retain history without being history

A `restart_lsn` is compact second-order state. It says which earlier history remains possibly necessary and can therefore govern reclamation of a much larger log prefix.

`small metadata footprint != small retention consequence`

### C. Downstream absence can remain operationally present as an obligation

A disconnected consumer is not currently executing, yet its persistent slot can make future need effective in the present by withholding reclamation.

### D. Retention obligation and retention capacity can conflict

PostgreSQL 13 can withdraw protection rather than allow one continuation relation to exhaust primary storage.

`history still useful != infrastructure will preserve it without limit`

### E. Slot identity, old continuation claim, and later continuation claim are separable

The new source deepening replaces an overly simple model:

```text
slot lost -> slot dead forever
```

with:

```text
slot object survives
old protection relation fails
later physical protection relation may be established from a later point
```

`control-object continuity != uninterrupted retained-history continuity`

### F. `unreserved` separates retirement authority from completed retirement

When WAL becomes `unreserved`, it has crossed a policy boundary before it has necessarily crossed a physical removal boundary.

`retirement authority != completed retirement`

### G. One continuation need can be served by multiple carriers

For physical standby replay, needed WAL can be on the primary, already local to the standby, or in an archive.

`local carrier loss != global history loss`

But:

`history survives somewhere != current streaming start point is immediately admissible`

### H. Archive replay can change what future history is needed without restoring removed local bytes

Archive catch-up advances the standby through the gap. It does not recreate the deleted primary-local WAL.

```text
archive replay advances consumer state
    -> later requested streaming point may become available
```

### I. Physical stream start point and slot retention frontier are different authorities

PostgreSQL 13 physical `START_REPLICATION` relies on the caller's requested start position rather than treating `restart_lsn` as the automatic resume pointer.

`client request != slot retention claim != segment availability`

### J. Live-consumer evidence and operator frontier editing have different requalification power

`pg_replication_slot_advance()` rejects an invalidated frontier. Physical flush feedback can establish a new frontier.

```text
operator says “move metadata”
    != live standby demonstrates receipt/flush at later LSN
```

This is a direct authority boundary rather than a cosmetic API difference.

### K. Runtime requalification and crash-surviving requalification are separate

The new physical `restart_lsn` can affect runtime retention before it has been saved at a later checkpoint.

`new runtime frontier != new crash-surviving frontier already persisted`

### L. Rebootstrap substitutes materialized state for unavailable history

If every usable replay path has a gap, a new base backup establishes a later materialized starting point.

`new materialized state != recovered missing WAL`

## Cross-case comparison

### Case 58 — Raft snapshot/log compaction

Raft can replace unavailable compacted log history for a lagging follower by transferring a newer snapshot plus protocol boundary metadata.

PostgreSQL has two bounded functional analogies:

```text
archive path:
missing primary-local WAL -> replay retained archive -> later streaming frontier becomes usable

base-backup path:
missing replay interval -> install newer materialized state -> continue with later WAL
```

The mechanisms, consistency protocols, and histories are different. No genealogy is asserted.

### Case 57 — Bigtable redo/materialization

Case 57 distinguishes materialized tablet state from subsequent redo history. PostgreSQL base backup plus WAL has a comparable materialization-plus-history decomposition, while `restart_lsn` additionally expresses a remote consumer's retention claim.

`local recovery frontier != remote-consumer continuation frontier`

### Case 137 — LevelDB obsolete-file liveness

LevelDB can retain a superseded SSTable because a still-live `Version`/iterator references it. PostgreSQL can keep otherwise old WAL because a persistent slot claims future need.

`locally superseded/old != reclaimable while another live relation depends on it`

### Case 145 — JFFS2 mount reconstruction

Case 145 distinguishes volatile runtime classification from authority rebuilt from retained evidence after restart. PostgreSQL's physical-slot rejoin adds a distributed variant: an old frontier can fail, another carrier can advance the consumer, and later live feedback can establish new retention authority.

`functional similarity != shared implementation or genealogy`

### Case 130 — LTO access-path survival

Case 130 distinguishes surviving media from a usable reader path. PostgreSQL supplies a distributed analogue:

`history survives in some carrier != the currently attempted continuation path is usable`

## Terminology and anti-anachronism

### PostgreSQL 9.1 vocabulary

Relevant pre-slot terms include WAL archive, `restore_command`, `wal_keep_segments`, streaming replication, base backup, and `archive_cleanup_command`.

Do not rewrite this 2011 behavior in later replication-slot vocabulary.

### PostgreSQL 2012–2013 development vocabulary

Relevant terms include `logical slot`, `max_logical_slots`, `slot-id` / `slotname`, `permanent replication slot`, and evolving logical-replication commands.

These document a development series, not the final 9.4 API.

### PostgreSQL 9.4 vocabulary

Relevant released terms include replication slot, physical/logical slot, `restart_lsn`, `active`, `pg_replslot`, WAL segments, checkpoints, archive, and base backup.

### PostgreSQL 13 additions

Relevant later terms include `max_slot_wal_keep_size`, `wal_status`, `reserved`, `extended`, `unreserved`, `lost`, and persistent `invalidated_at` in the implementation.

The project terms `continuation admission`, `retention frontier`, `history-liveness claimant`, `alternate carrier`, `requalification`, and `retirement authority` are **engineering reconstruction vocabulary**, not PostgreSQL historical vocabulary.

Do not rewrite the 2014 design as though it already had the 2020 cap or four-state availability model. Do not rewrite the public phrase `lost` as an immutable tombstone once the source-level physical rejoin path has been inspected.

## Philosophical interpretation — bounded

This case now contributes three modest temporal observations.

First, a WAL segment's technical future can depend on a participant that is currently absent. A slot makes that future-oriented claim on the past durable across disconnection and restart.

Second, “forgotten here” and “forgotten everywhere” are different propositions. One past can have several carriers with different custodians and retirement rules.

Third, **object identity can survive a broken obligation**. A physical slot name/object can remain after its old continuation frontier fails; later, after another carrier has bridged the missing past for the consumer, the same object can carry a new future retention claim from a later point.

Thus three continuities must remain distinct:

```text
continuity of control-object identity
continuity of retained historical coverage
continuity of future operating relation
```

These are project interpretations, not PostgreSQL project vocabulary and not equations with human memory, archival promises, or metaphysical identity.

## Failure and forgetting

- **Consumer lag grows:** more historical WAL can remain live because the frontier stays old.
- **Consumer disconnects:** the slot can continue retaining history; connection loss is not automatically continuation loss.
- **Primary crashes/restarts:** saved slot state can restore the retention relation.
- **Changed slot state not yet saved:** in-memory and crash-surviving control state differ.
- **9.4 slot retained indefinitely:** local WAL space can become the failure resource.
- **PostgreSQL 13 cap exceeded:** protection can be withdrawn to protect primary capacity.
- **`unreserved`:** required local WAL can still exist while no longer protected from later removal.
- **checkpoint invalidation:** old `restart_lsn` moves to `invalidated_at`, active use can be terminated, and the protection frontier is cleared.
- **`lost`:** the old slot continuation relation has lost required local WAL; this is not global erasure and not necessarily permanent object death for a physical slot.
- **Archive survives:** a physical standby may replay the missing interval independently.
- **Archive catches standby up to available primary WAL:** same physical slot identity can participate in a later stream; flush feedback can establish a new `restart_lsn`.
- **New frontier only dirty in memory:** runtime protection can precede checkpoint persistence of that requalified frontier.
- **Archive gap / cleanup removes needed WAL:** alternate replay can fail independently of slot state.
- **Every usable replay path missing:** reinitialize physical standby from a new base backup.
- **Slot drop/local WAL removal:** changes continuation/replay authority; does not prove secure media erasure.
- **Underlying storage violates persistence assumptions:** guarantees exceed the contract directly established by PostgreSQL source/docs.

## Counterexamples and stop conditions

- **Public prototype != released contract.** 2012–2013 patch history is not a substitute for 9.4 docs.
- **Persistence intent != implemented crash safety.** The December-2012 author reply admits a then-current restart persistence gap.
- **Generic slot abstraction != identical slot types.** Physical and logical retained state/recovery semantics differ.
- **Public chronology != invention priority.** Dates establish bounded PostgreSQL floors only.
- **Replication slot != replica.** Slot is control state, not another database copy.
- **Replication slot != WAL corpus.** It governs history stored elsewhere.
- **Replication slot != WAL archive.** Archive is a separate carrier with separate cleanup policy.
- **`restart_lsn` != full replay history.** It is a frontier.
- **`confirmed_flush_lsn` != `restart_lsn`.** Logical acknowledgement and oldest-needed WAL differ.
- **Consumer acknowledgement != completed WAL reclamation.** Confirmation can permit frontier movement; it is not deletion.
- **Current primary state != sufficient downstream replay history.** Remote consumer can need older WAL.
- **Inactive != no retention obligation.** Disconnection is a core slot use case.
- **Crash-safe slot != immortal slot.** Administrative drop and resource invalidation remain possible.
- **Precise retention != bounded storage cost.** PostgreSQL 9.4 demonstrates the contrary.
- **WAL present != WAL protected.** `unreserved` is a direct counterexample.
- **WAL unprotected != WAL already removed.** Consumer may still catch up first.
- **Old slot continuation lost != slot object deleted.** PostgreSQL 13 invalidation preserves the named object.
- **Slot `lost` != WAL globally nonexistent.** Archive/backup may contain equivalent history.
- **Archive present != old frontier repaired.** Archive bridges the consumer's gap; it does not restore removed primary-local WAL.
- **`lost` != immutable tombstone for a physical slot name.** Inspected 13.x source allows a later stream to establish a new frontier.
- **Same slot name != uninterrupted history protection.** The old and new retention relations can be discontinuous.
- **`pg_replication_slot_advance()` != invalidated-slot repair API.** PostgreSQL 13 explicitly rejects that case.
- **New runtime restart frontier != new crash-surviving frontier already persisted.** Physical feedback marks dirty rather than synchronously saving every acknowledgement.
- **Physical archive/rejoin != logical-slot archive/rejoin.** Do not generalize across slot types.
- **Archive handoff != indefinite archive retention.** Cleanup remains separate.
- **Safe cleanup for one standby != safe cleanup for backup recovery.** PostgreSQL explicitly distinguishes claims.
- **New base backup != reconstruction of missing WAL.** It establishes a later materialized starting point.
- **WAL removal != secure deletion.** No sanitization claim follows.
- **PostgreSQL replication retention != Raft snapshotting.** Comparison is functional only.
- **2020 resource-bound semantics != 2014 design vocabulary.** Later evolution remains later.

## Prior art and novelty boundary

This case does not claim PostgreSQL invented log retention, replication progress, replay positions, log shipping, WAL archiving, base-backup recovery, consumer acknowledgements, or keeping history for lagging replicas.

The chronology instead establishes boundaries:

```text
2011:
archive-backed physical standby catch-up + base-backup reinitialization already released

2012–2013:
public logical-slot prototype, restart-persistence gap, persistence work, genericization intent

2014:
mainline/released crash-safe replication slots constrain primary-local WAL reclamation

2018–2020:
manual physical frontier movement exposes its own checkpoint persistence horizon

2020 PostgreSQL 13:
resource cap can invalidate old slot protection

2020 source / 2021 field witness:
physical slot object may later carry a new frontier after another carrier bridges the gap

2024 PostgreSQL 17:
logical failover slot itself becomes cross-node retained/admitted state
```

The source-controlled contribution is therefore narrow:

> **PostgreSQL provides unusually explicit examples of retained consumer-need metadata constraining history reclamation, later resource policy withdrawing that protection, alternate carriers preserving replayability outside the primary, and a physical control object surviving failure of one continuation frontier long enough to acquire another.**

A complete genealogy belongs in `tmzncty/computing-archaeology`.

## Uncertainty and next evidence

The bounded case remains **grounded**. This round closes the previous physical-slot question “must a lost physical slot necessarily be dropped/recreated after archive catch-up?” at source level: **no; PostgreSQL 13 physical streaming contains an in-place later-frontier re-establishment path using the existing slot object once the client can request still-available WAL.**

Remaining debt is narrower:

1. controlled fault injection reproducing `lost -> archive catch-up -> same-slot stream -> new restart_lsn -> checkpoint -> crash/restart` with captured `pg_replication_slots` states;
2. release-by-release physical-slot behavior after PostgreSQL 13, including fixes associated with the 2021 `max_slot_wal_keep_size` WAL-removal bug thread;
3. logical-slot-specific invalidation/archive/rebootstrap semantics, which must not be inferred from this physical path;
4. pre-November-2012 private/public slot precursors and exact patch ancestry into the 2014/9.4 implementations;
5. post-17 failover-slot fixes, cascading/multi-standby evolution, promotion fault injection, and production failover traces;
6. lower-layer filesystem/device/archive persistence testing for slot save, WAL removal, archive handoff, and external retention;
7. broader replication/log-retention/archive genealogy coordinated with `computing-archaeology`.

## Related repository boundary

`tmzncty/computing-archaeology` was freshly searched for `PostgreSQL replication slot restart_lsn WAL archive restore_command`; no dedicated overlapping study was found.

If broad PostgreSQL WAL, log-shipping, streaming-replication, backup-tooling, archive-implementation, logical-decoding, or slot history is developed there later, this case should link to it rather than reproduce it.

`technical-retention` keeps the narrower question:

> **Which retained relation makes otherwise old history count as live, which carrier currently embodies that history, what ends each carrier's protection, and can a surviving control object acquire a new continuation relation after its old one fails?**

## Evidence links

- [Evidence 141 — PostgreSQL 2014–2020 replication-slot WAL-retention grounding](../evidence/141-postgresql-2014-2020-replication-slot-wal-retention-grounding.md)
- [Evidence 141 deepening — PostgreSQL 2012–2014 replication-slot public genealogy](../evidence/141-postgresql-2012-2014-replication-slot-public-genealogy-deepening.md)
- [Evidence 141 deepening — PostgreSQL 17 failover-slot synchronization](../evidence/141-postgresql-2024-failover-slot-synchronization-deepening.md)
- [Evidence 141B — logical-slot `confirmed_flush` vs `restart_lsn` dual frontier](../evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md)
- [Evidence 141 deepening — physical-slot manual-advance persistence](../evidence/141-postgresql-2018-2020-physical-slot-advance-persistence-deepening.md)
- [Evidence 141 deepening — 2011–2020 WAL archive alternate continuation](../evidence/141-postgresql-2011-2020-wal-archive-alternate-continuation-deepening.md)
- [Evidence 141 deepening — PostgreSQL 13 lost physical slot, archive catch-up, and later-frontier rejoin](../evidence/141-postgresql-13-lost-physical-slot-archive-rejoin-deepening.md)
- [Case 58 — Raft snapshot/log compaction](58-raft-snapshot-log-compaction.md)
- [Case 57 — Bigtable tablet log/memtable recovery](57-google-bigtable-tablet-log-memtable-recovery.md)
- [Case 137 — LevelDB MANIFEST/CURRENT](137-leveldb-v17-manifest-current-recovery.md)
- [Case 145 — JFFS2 negative-state evidence](145-jffs2-garbage-collection-negative-state-evidence.md)
- [PostgreSQL 9.1 warm-standby documentation](https://www.postgresql.org/docs/9.1/warm-standby.html)
- [PostgreSQL commit `858ec118...`](https://github.com/postgres/postgres/commit/858ec11858a914d4c380971985709b6d6b7dd6fc)
- [PostgreSQL 9.4 warm-standby / replication-slot documentation](https://www.postgresql.org/docs/9.4/warm-standby.html)
- [PostgreSQL commit `c6550776...`](https://github.com/postgres/postgres/commit/c6550776394e25c1620bc8258427c8f1d448080d)
- [PostgreSQL commit `b8fd4e02...`](https://github.com/postgres/postgres/commit/b8fd4e02c6d01183bf6def5897ad6cf7766bfff4)
- [PostgreSQL 13 replication-slot view](https://www.postgresql.org/docs/13/view-pg-replication-slots.html)
- [PostgreSQL 13 warm-standby documentation](https://www.postgresql.org/docs/13/warm-standby.html)
- [PostgreSQL 13.3 `slot.c`](https://github.com/postgres/postgres/blob/REL_13_3/src/backend/replication/slot.c)
- [PostgreSQL 13.3 `walsender.c`](https://github.com/postgres/postgres/blob/REL_13_3/src/backend/replication/walsender.c)
- [PostgreSQL 13.3 `slotfuncs.c`](https://github.com/postgres/postgres/blob/REL_13_3/src/backend/replication/slotfuncs.c)
- [PostgreSQL bug #17103](https://www.postgresql.org/message-id/17103-004130e8f27782c9%40postgresql.org)