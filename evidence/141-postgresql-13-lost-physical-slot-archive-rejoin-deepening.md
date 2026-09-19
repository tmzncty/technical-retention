# Case 141 Evidence Deepening: PostgreSQL 13 `lost` Physical Slot, Archive Catch-Up, and Re-established WAL Protection

## Status

**`bounded deepening complete`** for one narrow PostgreSQL 13 physical-replication question: what survives when `max_slot_wal_keep_size` invalidates a physical replication slot, how a standby can bridge the missing interval through an independent WAL archive, and under what source-level conditions the same physical slot object can acquire a new `restart_lsn` protection frontier afterward.

This slice corrects an overly strong reading of the public `wal_status = lost` wording. PostgreSQL 13 documentation says a `lost` slot is no longer usable because some required WAL has been removed. The 13.x physical-streaming source exposes a more precise state machine: invalidation persists the failed old frontier by copying it to `invalidated_at` and clearing `restart_lsn`, but does **not** drop the slot object; `START_REPLICATION` with a physical slot deliberately does not validate that slot's `restart_lsn`; and a later standby flush acknowledgement can install a new valid `restart_lsn`. A PostgreSQL 13.3 field report independently records the corresponding operational pattern: streaming failed after the slot fell behind, archive recovery took over, and streaming resumed after archive catch-up.

The bounded result is therefore:

```text
old slot-protected continuation frontier is lost
    != slot object is deleted
    != every copy of the missing WAL is gone
    != physical slot name can never participate in streaming again
```

and, more carefully:

```text
archive bridges the missing replay interval on the standby
    -> standby reaches a later start point still available from the primary
    -> physical START_REPLICATION may use the existing slot name
    -> standby flush feedback may install a later restart_lsn
    -> slot-based protection is re-established from that later frontier
```

This is **not** evidence that archived WAL is copied into the slot, that the old missing range becomes protected again, that every `lost` physical slot automatically recovers, or that logical slots have the same requalification path.

---

## Research question

The preceding archive deepening established that primary-local slot protection and an independently retained WAL archive are separate carriers. It deliberately left this debt open:

> **If a physical slot reaches `lost` while the standby can still recover the missing WAL from an archive, must the operator discard/recreate that slot, or can the existing physical slot object regain a valid protection frontier once the standby has bridged the gap?**

The PostgreSQL 13.3 source supports the second possibility for physical streaming, with important limits.

---

## Sources inspected

### PostgreSQL project documentation and source

1. PostgreSQL 13 documentation, **26.2 Log-Shipping Standby Servers**: <https://www.postgresql.org/docs/13/warm-standby.html>.
2. PostgreSQL 13 documentation, **51.80 `pg_replication_slots`**: <https://www.postgresql.org/docs/13/view-pg-replication-slots.html>.
3. PostgreSQL 13 documentation, **19.6 Replication**: <https://www.postgresql.org/docs/13/runtime-config-replication.html>.
4. PostgreSQL commit `c6550776394e25c1620bc8258427c8f1d448080d`, **7 April 2020**, `Allow users to limit storage reserved by replication slots`: <https://github.com/postgres/postgres/commit/c6550776394e25c1620bc8258427c8f1d448080d>.
5. PostgreSQL `REL_13_3`, `src/backend/replication/slot.c`: <https://github.com/postgres/postgres/blob/REL_13_3/src/backend/replication/slot.c>.
6. PostgreSQL `REL_13_3`, `src/backend/replication/walsender.c`: <https://github.com/postgres/postgres/blob/REL_13_3/src/backend/replication/walsender.c>.
7. PostgreSQL `REL_13_3`, `src/backend/replication/slotfuncs.c`: <https://github.com/postgres/postgres/blob/REL_13_3/src/backend/replication/slotfuncs.c>.
8. PostgreSQL `REL_13_0`, `src/include/replication/slot.h`: <https://github.com/postgres/postgres/blob/REL_13_0/src/include/replication/slot.h>.

### Contemporary operator/developer record

9. PostgreSQL bug report **#17103**, **13 July 2021**, PostgreSQL 13.3 deployment with `max_slot_wal_keep_size`, archive catch-up, and later streaming recovery: <https://www.postgresql.org/message-id/17103-004130e8f27782c9%40postgresql.org>.
10. Kyotaro Horiguchi response, **14 July 2021**: <https://www.postgresql.org/message-id/20210714.111214.590009579344145004.horikyota.ntt%40gmail.com>.
11. Jeff Janes response, **14 July 2021**, identifying a separate WAL-removal bug while discussing the same lost-slot case: <https://www.postgresql.org/message-id/CAMkU%3D1wfXqQ9yhD%2BvZ6%2BkSV%3DMiP2B%3Du%3DwMGEgqFGUVFT3pT73w%40mail.gmail.com>.

A fresh search of `tmzncty/computing-archaeology` for `PostgreSQL replication slot restart_lsn WAL archive restore_command` found no dedicated packet to reuse. Broad PostgreSQL WAL/streaming/archive history remains companion-repository work.

---

## Historical / source record

### H/P — PostgreSQL 13 documents `lost` as removal of WAL required by a slot

The PostgreSQL 13 `pg_replication_slots` view defines four WAL-availability states: `reserved`, `extended`, `unreserved`, and `lost`.

The public documentation says:

- `unreserved` means the slot no longer retains the required WAL and some files are candidates for removal at the next checkpoint; this state can return to `reserved` or `extended`;
- `lost` means some required WAL files have been removed and the slot is no longer usable;
- `safe_wal_size` is `NULL` for lost slots.

The configuration documentation separately says that when `max_slot_wal_keep_size` is nonnegative and a slot's `restart_lsn` falls too far behind, the standby using that slot may no longer be able to continue because required WAL can be removed.

This is the public contract surface. It correctly warns that the old required range is no longer safely available through that slot's protection claim.

### H/P — checkpoint invalidation preserves the fact of the failed old frontier but clears its protection frontier

In PostgreSQL 13.3 `InvalidateObsoleteReplicationSlots()`, a slot whose `restart_lsn` falls behind the removal boundary is invalidated at checkpoint time.

The source does three especially important things:

```text
invalidated_at = old restart_lsn
restart_lsn = InvalidXLogRecPtr
ReplicationSlotSave()
```

It also terminates an active process using the too-far-behind slot before persisting this invalidated state.

This is not a slot drop. The slot remains `in_use` as a named object, while the old protection frontier is removed.

Therefore:

```text
old retention claim invalidated
    != slot object deleted
```

### H/P — `invalidated_at` and `restart_lsn` are both persistent slot state

`ReplicationSlotPersistentData` in the PostgreSQL 13 source contains:

- `restart_lsn`: oldest LSN that might still be required by the slot;
- `invalidated_at`: the old `restart_lsn` copied when the slot is invalidated.

Both belong to `data surviving shutdowns and crashes`.

The invalidation event therefore leaves persistent evidence of a failed old protection relation rather than merely changing a transient status string.

### H/P — the system view derives `lost` from the relation between those fields and WAL availability

The PostgreSQL 13.3 implementation of `pg_replication_slots` first checks the pair:

```text
restart_lsn is invalid
AND invalidated_at is valid
```

and treats that as definite `WALAVAIL_REMOVED` / `lost`.

If `restart_lsn` is valid, however, the view instead evaluates availability from the current `restart_lsn` through `GetWALAvailability()`.

That source shape matters. `lost` is not represented by a separate immutable tombstone bit whose presence permanently forbids the slot from ever having another valid frontier. It is an observable state derived from the current protection frontier plus retained invalidation evidence and WAL availability.

### H/P — physical `START_REPLICATION` deliberately does not validate the slot's `restart_lsn`

PostgreSQL 13.3 `StartReplication()` acquires the named slot and rejects it if it is logical when physical replication was requested.

For a physical slot it then contains an explicit comment:

```text
we don't need to verify the slot's restart_lsn here;
instead we rely on the caller requesting the starting point to use;
if the WAL segment doesn't exist, we'll fail later
```

This supplies a crucial source-level qualification to the coarse `lost` wording:

```text
physical slot object acquired
    != server automatically resumes from slot.restart_lsn
```

The requested streaming start point is supplied by the replication client/standby. If that requested WAL still exists on the sender, the physical stream can proceed even though the slot's old `restart_lsn` had previously been invalidated.

### H/P — physical standby flush feedback can install a new `restart_lsn`

In PostgreSQL 13.3, standby status replies carry write, flush, and apply positions. If a physical replication slot is active and the standby reports a valid flush position, `ProcessStandbyReplyMessage()` calls `PhysicalConfirmReceivedLocation(flushPtr)`.

That function does not require the previous `restart_lsn` to be valid. If the reported LSN differs from the current slot value, it writes:

```text
slot->data.restart_lsn = lsn
```

then marks the slot dirty and recomputes the required-WAL horizon.

Consequently, a previously invalidated physical slot can acquire a later in-memory `restart_lsn` after successful physical streaming resumes.

### H/P — the new physical frontier is not synchronously persisted at each acknowledgement

The same `PhysicalConfirmReceivedLocation()` function explicitly does **not** call `ReplicationSlotSave()` on each update. It marks the slot dirty and relies on later persistence.

For this bounded case:

```text
new protection frontier installed in memory
    != that newly advanced frontier already fsynced as slot state
```

This is the same broader distinction already present elsewhere in Case 141: runtime authority and crash-surviving authority can have different horizons.

### H/P — SQL `pg_replication_slot_advance()` cannot be used to repair an invalidated slot

PostgreSQL 13.3 makes a different choice in the SQL advance path. After acquiring a slot, `pg_replication_slot_advance()` checks whether `restart_lsn` is invalid and errors with detail stating that the slot either never reserved WAL **or has been invalidated**.

Thus:

```text
physical streaming feedback may install a new restart_lsn
    != SQL slot-advance is an in-place invalidated-slot repair API
```

This is a useful authority boundary. Not every mechanism that can normally move a slot frontier forward is allowed to re-establish an invalidated one.

### H/P — standby operation already alternates archive recovery and streaming

PostgreSQL 13 warm-standby documentation specifies a retry loop:

1. restore WAL from the archive with `restore_command`;
2. use WAL available in the standby's local `pg_wal`;
3. if those sources are exhausted and streaming is configured, connect to the primary and request streaming from the last valid record found;
4. if streaming fails or disconnects, return to archive recovery and repeat.

The same documentation says that with a sufficiently complete accessible WAL archive, `wal_keep_size` or a replication slot is not required merely to let a physical standby catch up.

This supplies the missing bridge between the source-level slot behavior and the alternate carrier established by the earlier evidence record.

### H/P — `primary_slot_name` binds the standby's streaming phase to a named physical slot

PostgreSQL 13's replication-slot configuration example instructs a standby to set `primary_slot_name` to the physical slot it should use for streaming.

Archive replay and slot-backed streaming therefore remain separate phases of standby recovery even when they belong to one operator configuration:

```text
restore_command -> archive replay
primary_slot_name -> named slot used when streaming is attempted
```

The archive is not imported into the slot. The standby simply advances through the archive until it can request a streaming start point that the primary can serve.

### H/P — PostgreSQL 13.3 field evidence records archive catch-up followed by restored streaming

Bug #17103 reports a PostgreSQL 13.3 deployment with one replica, streaming replication using a slot, archiving enabled, and `max_slot_wal_keep_size = 600GB`.

The operator reports this sequence:

- replication lag grew;
- `safe_wal_size` became negative;
- streaming stopped working;
- the replica began recovery from the WAL archive;
- after hours, the replica caught up from the archive;
- replication was restored with no delay.

The report's primary purpose was a different PG13 WAL-removal problem, later discussed as a bug. It is therefore not a controlled experiment proving every internal state transition. But it is a named contemporary production witness that the documented archive-to-streaming fallback was not merely hypothetical in this exact `max_slot_wal_keep_size` regime.

It does **not** by itself prove the exact `wal_status` value at every moment, nor does it replace the source inspection above.

---

## Engineering reconstruction

### E — `lost` destroys the old protection relation, not necessarily the slot's identity

The source supports a three-part distinction:

```text
slot name / object identity
    != old failed restart frontier
    != later re-established restart frontier
```

Invalidation preserves the named object while replacing the old `restart_lsn` with an invalid value. If later physical streaming becomes possible, feedback can place a new, later `restart_lsn` in that same object.

Therefore it is too strong to model physical-slot invalidation as irreversible object death.

### E — the continuity gap can be crossed by a carrier the slot does not control

Suppose the old slot protected WAL through frontier `R0`, but required local WAL behind `R0` is removed and the slot becomes `lost`.

If an independent archive still contains the missing interval, the standby can replay it without making the slot protect or contain that interval.

A bounded reconstruction is:

```text
primary slot loses R0 protection
    -> streaming from old standby point fails
    -> standby replays missing WAL from archive
    -> standby reaches R1
    -> R1 is still available on primary
    -> standby requests streaming from R1 using the configured slot name
    -> first valid flush feedback installs a later restart_lsn
```

The old interval was supplied by the archive, not resurrected on the primary.

### E — same slot object does not imply uninterrupted retention obligation

If the slot name persists across the episode, one could casually say “the slot recovered.” That phrase hides the most important retention fact.

The protection relation is discontinuous:

```text
slot protects old range
    -> protection withdrawn / old range lost locally
    -> no valid restart_lsn protection frontier
    -> later physical stream establishes a new frontier
```

The same control object can therefore outlive one failed continuation claim and later carry another.

`control-object continuity != uninterrupted history-protection continuity`

### E — archive catch-up can re-establish eligibility for streaming without restoring the missing primary-local bytes

The standby's archive replay changes **what start point it needs next**. It does not make the primary regain WAL that was already removed.

Thus:

```text
archive replay advances standby state
    -> later requested start point may lie inside current primary WAL
```

not:

```text
archive replay
    -> old removed primary WAL reappears
```

### E — a requested start point is a separate continuation authority from the old slot frontier

Physical `START_REPLICATION` trusts the client's requested start position and checks actual WAL availability later. The old `restart_lsn` is not used as an automatic resume pointer for physical streaming.

This yields another Case-141 distinction:

```text
slot retention frontier
    != client's requested streaming start point
    != actual WAL segment availability at that point
```

A valid new stream requires the latter two to align even after the old slot frontier is gone.

### E — re-established runtime protection and crash-surviving re-established protection are different states

Because `PhysicalConfirmReceivedLocation()` marks the slot dirty rather than synchronously saving it, a new acknowledged frontier can matter immediately to `ReplicationSlotsComputeRequiredLSN()` while still awaiting ordinary slot persistence.

Therefore:

```text
new restart_lsn affects runtime WAL retention
    != new restart_lsn necessarily survives an immediate crash
```

The exact crash outcome depends on when the dirty slot is next saved. This slice does not claim a stronger crash guarantee than the source gives.

### E — `pg_replication_slot_advance()` and streaming feedback have different requalification authority

The SQL advance function explicitly refuses an invalid `restart_lsn`; physical streaming acknowledgement can replace an invalid value.

This is not merely an API convenience difference. It means the system distinguishes:

```text
operator asks metadata frontier to jump forward
    != live physical consumer proves receipt/flush of a later stream position
```

The second path can supply new evidence for a future retention obligation that the first path is not allowed to manufacture after invalidation.

### E — public `lost` wording should be read as a current continuation failure, not an eternal tombstone for a physical slot name

The documentation's operational warning remains valid: once required WAL is removed, the old continuation path protected by that slot has failed.

The source-level qualification is narrower:

> **For a PostgreSQL 13 physical slot, `lost` need not mean that the named slot object can never again hold a useful `restart_lsn`. If an external carrier lets the standby bridge the missing range and the primary can serve a later requested start point, normal physical streaming feedback can establish a new frontier in the same slot object.**

This statement is intentionally limited to the inspected physical-slot path.

---

## Functional comparison

### A — Case 58 Raft snapshot catch-up: external state substitution can change the next log frontier

A bounded functional analogy exists with Case 58. A lagging Raft follower can install a newer materialized snapshot and then require only later log entries. PostgreSQL archive catch-up similarly advances the standby through history by another carrier until a later streaming frontier becomes usable.

The mechanisms differ sharply:

- PostgreSQL archive catch-up replays WAL rather than installing a consensus snapshot;
- a physical replication slot is not a Raft match index;
- no protocol genealogy is asserted.

The shared abstract form is only:

```text
old incremental path unavailable
    -> alternate retained state/history advances consumer
    -> later incremental frontier becomes admissible
```

### A — Case 137 LevelDB and Case 145 JFFS2: reconstructed authority after retained evidence changes

Cases 137 and 145 both separate surviving physical state from the control evidence needed to make future operations admissible. Here the corresponding split is distributed:

- the archive preserves replayable history;
- the standby's replay progress changes its next request;
- a later physical acknowledgement establishes a new slot retention frontier.

This is functional comparison only. PostgreSQL replication slots are not filesystem selectors or erase-block clean markers.

---

## Philosophical interpretation — bounded

Project interpretation only:

This slice gives a precise example of **identity surviving a broken obligation**.

The named physical slot can persist while the retention promise associated with its old frontier fails. Later, the same object can carry a new promise beginning at a later point, provided another carrier has already bridged the missing past for the consumer.

So technical continuity can split into at least three different continuities:

```text
continuity of object identity
continuity of retained historical coverage
continuity of future operating relation
```

They can fail and recover independently.

This is a repository-level interpretation, not PostgreSQL project vocabulary and not a claim about human memory, archival identity, or metaphysical persistence.

---

## Explicit non-claims / stop conditions

1. **X — every PostgreSQL 13 `lost` physical slot automatically recovers.** Rejected; a later stream start point must actually be available.
2. **X — archive presence by itself changes the slot's `restart_lsn`.** Rejected; the archive is consumed by the standby, while physical streaming feedback updates the slot.
3. **X — the old removed primary-local WAL is restored by archive catch-up.** Rejected.
4. **X — the old failed retention interval becomes protected again.** Rejected; the new frontier is later.
5. **X — a `lost` slot object is dropped.** Rejected by the inspected invalidation source.
6. **X — `invalidated_at` is merely transient telemetry.** Rejected; it is persistent slot data.
7. **X — `lost` is an immutable tombstone bit in PostgreSQL 13.3.** Rejected by the inspected view/source representation.
8. **X — `pg_replication_slot_advance()` can repair an invalidated slot.** Rejected by its explicit invalidated-slot error path.
9. **X — a client may request any arbitrary LSN and force it to become protected.** Rejected; physical streaming still requires the requested WAL to exist and normal feedback to occur.
10. **X — runtime `restart_lsn` advancement is synchronously persisted on every standby reply.** Rejected by `PhysicalConfirmReceivedLocation()`.
11. **X — same slot name means uninterrupted protection of all intervening WAL.** Rejected.
12. **X — PostgreSQL documentation is simply wrong when it calls `lost` unusable.** Rejected; the old continuation relation is unusable, while source inspection adds a later requalification path for physical streaming.
13. **X — the production bug report alone proves internal slot state.** Rejected; it is an operational witness corroborating a source-grounded mechanism.
14. **X — bug #17103 proves the same behavior for every PostgreSQL 13 minor release.** Not claimed.
15. **X — this physical-slot rejoin path applies to logical decoding.** Rejected as unsupported.
16. **X — an archive is part of a replication slot.** Rejected.
17. **X — archive catch-up means archival retention is indefinite.** Rejected; archive cleanup remains separate.
18. **X — local WAL removal is secure erasure.** Rejected; no sanitization claim follows.
19. **X — preserving slot identity preserves the identity of every downstream recovery relation.** Not established.
20. **X — functional comparison with Raft, LevelDB, or JFFS2 establishes genealogy.** Rejected.

---

## Claim ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| PostgreSQL 13 docs define `lost` as required WAL removed and the slot no longer usable | `H/P` | official `pg_replication_slots` docs |
| checkpoint invalidation copies old `restart_lsn` to `invalidated_at`, clears `restart_lsn`, saves the slot, and does not drop it | `H/P` | REL_13_3 `InvalidateObsoleteReplicationSlots()` |
| `restart_lsn` and `invalidated_at` are persistent slot data | `H/P` | REL_13_0/13.x `slot.h` |
| `pg_replication_slots` derives definite lost state when `restart_lsn` is invalid while `invalidated_at` is valid | `H/P` | REL_13_3 `slotfuncs.c` |
| physical `START_REPLICATION` intentionally does not validate the slot's `restart_lsn` | `H/P` | REL_13_3 `walsender.c` |
| a standby flush reply can assign a later `restart_lsn` to a physical slot even when the previous value was invalid | `H/P` | REL_13_3 `PhysicalConfirmReceivedLocation()` |
| that physical acknowledgement update is marked dirty but not synchronously saved on each reply | `H/P` | same source function |
| SQL `pg_replication_slot_advance()` refuses a slot whose `restart_lsn` is invalid / invalidated | `H/P` | REL_13_3 `slotfuncs.c` |
| standby recovery loops archive -> local `pg_wal` -> streaming and returns to archive after streaming failure | `H/P` | official PostgreSQL 13 warm-standby docs |
| a 13.3 operator reported streaming failure, archive recovery, then restored replication after archive catch-up | `H/P*` | bug #17103; production witness, not controlled experiment |
| same physical slot object can outlive failure of an old protection frontier | `E` | invalidation does not drop object + later feedback can set new frontier |
| archive catch-up can change the standby's next required streaming point without restoring removed primary-local WAL | `E` | docs + source reconstruction |
| same slot identity does not imply uninterrupted WAL-retention coverage | `E` | bounded state-machine reconstruction |
| physical streaming feedback and SQL slot advancement have different requalification authority after invalidation | `E` | direct source comparison |
| any of the above applies unchanged to logical slots | `X` | not established |

---

## Prior-art / chronology boundary

This slice makes no novelty claim for log shipping, replay fallback, consumer progress, or retention frontiers.

Its historical result is narrowly PostgreSQL-specific:

```text
2011-era released standby model:
archive/local-WAL/stream retry already exists

2014:
replication slots add persistent primary-local WAL protection

2020 PostgreSQL 13:
max_slot_wal_keep_size can invalidate that protection

2020 source / 2021 13.3 field witness:
physical slot object may later acquire a new frontier after the consumer
bridges the missing interval through another carrier
```

The source-level requalification path is an implementation/behavior result, not a claim that PostgreSQL invented this pattern.

---

## What this slice closes

This closes the **physical-slot** part of the earlier Case 141 archive/rebootstrap debt more precisely than the prior evidence could:

- a physical slot invalidated by `max_slot_wal_keep_size` is not dropped;
- its old `restart_lsn` protection is explicitly cleared and persisted as invalidated state;
- archive catch-up can independently advance the standby through the missing interval;
- the same physical slot name can participate in a later streaming attempt from a start point that still exists on the primary;
- physical flush feedback can then establish a later `restart_lsn` in that slot;
- SQL `pg_replication_slot_advance()` is **not** the repair path;
- the newly re-established runtime frontier has its own persistence horizon because acknowledgement updates are not synchronously saved each time.

Remaining debt is narrower:

1. controlled fault injection reproducing `lost -> archive catch-up -> same-slot streaming -> new restart_lsn -> checkpoint -> crash/restart`;
2. exact release-by-release changes to this physical-slot behavior after PostgreSQL 13, including fixes associated with the 2021 WAL-retention bug thread;
3. logical-slot-specific invalidation and rebootstrap semantics, which must remain separate;
4. production traces that include `pg_replication_slots` before/after states rather than only operator narrative;
5. lower-layer archive and storage durability validation;
6. broader PostgreSQL WAL/archive/replication genealogy in `computing-archaeology`.

## Related repository routing

A fresh companion search found no dedicated PostgreSQL replication-slot/archive study in `tmzncty/computing-archaeology`.

`technical-retention` therefore keeps only this bounded seam:

```text
old physical continuation claim fails
    -> slot identity survives
    -> another carrier may bridge the missing history
    -> later live-consumer evidence can establish a new protection frontier
    -> runtime requalification and crash-surviving requalification remain distinct
```

Broader PostgreSQL streaming-replication history, WAL archival genealogy, deployment practice, and bug-by-bug release history remain companion-repository work.