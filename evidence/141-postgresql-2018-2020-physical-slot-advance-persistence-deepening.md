# Case 141 Evidence Deepening: PostgreSQL 2018–2020 Physical Replication-Slot Advance Persistence

## Status

**`grounded`** for the bounded persistence semantics of manually advancing a physical replication slot in PostgreSQL 11-era code and its February-2020 correction. This slice uses PostgreSQL's own commit announcements, developer discussion, released documentation, and release notes.

It does **not** claim that `pg_replication_slot_advance()` synchronously fsyncs slot state before returning, that moving a slot frontier immediately removes older WAL, or that a slot-position change is a sanitization event. It also does not establish the pre-2018 proposal genealogy of manual slot advancement.

## Research question

Case 141 already establishes that replication-slot metadata can retain a compact frontier whose value keeps a much larger WAL corpus alive. The remaining physical-slot question is narrower:

> **When an administrator manually advances a physical replication slot, when has the new retention frontier merely become visible in memory, when has it become restart-persistent control state, and when—if ever—does that imply older WAL has actually disappeared?**

One SQL operation crosses three different horizons that are easy to collapse:

```text
function completed / new restart_lsn visible
        !=
slot control state written for restart recovery
        !=
older WAL physically reclaimed
```

## Sources inspected

1. PostgreSQL committers archive, **“Ability to advance replication slots”**, 17 January 2018, commit `9c7d06d60680c7f00d931233873dee81fdb311c6`: <https://www.postgresql.org/message-id/E1ebm6p-000761-Hc%40gemulon.postgresql.org>.
2. Alexey Kondratov, pgsql-hackers, **“Physical replication slot advance is not persistent”**, 24 December 2019: <https://www.postgresql.org/message-id/059cc53a-8b14-653a-a24d-5f867503b0ee%40postgrespro.ru>.
3. Michael Paquier, pgsql-hackers follow-up, 28 January 2020, documenting the chosen checkpoint-mediated behavior: <https://www.postgresql.org/message-id/20200128080114.GB145179%40paquier.xyz>.
4. PostgreSQL committers archive, **“Fix slot data persistency when advancing physical replication slots”**, 30 January 2020, master commit `b0afdcad21fde1470e6502a376bfaf0e10d384fa`, backpatched through 11: <https://www.postgresql.org/message-id/E1iwzPK-0002kB-2n%40gemulon.postgresql.org>.
5. PostgreSQL 11.7 release notes, released 13 February 2020: <https://www.postgresql.org/docs/11/release-11-7.html>.
6. PostgreSQL 12.2 release notes, released 13 February 2020: <https://www.postgresql.org/docs/12/release-12-2.html>.
7. PostgreSQL 12 system-administration function documentation for `pg_replication_slot_advance()`: <https://www.postgresql.org/docs/12/functions-admin.html>.

The commit announcement is the preferred implementation-history anchor because it is first-party PostgreSQL project material. Branch-specific backpatch object IDs may differ; the historical claim here is the project-level fix and its explicit `Backpatch-through: 11`, corroborated by the 11.7 and 12.2 release notes.

---

## Historical record

### H/P — manual advancement entered PostgreSQL in January 2018 for both physical and logical slots

The PostgreSQL committers archive records commit `9c7d06d60680c7f00d931233873dee81fdb311c6` on **17 January 2018** as adding `pg_replication_slot_advance()` for both physical and logical replication slots.

This establishes a PostgreSQL implementation/public-source floor, not invention priority for manual replication-progress advancement.

### H/P — a December-2019 report showed physical-slot advancement could be visible yet fail to survive restart

On **24 December 2019**, Alexey Kondratov reported a reproducible physical-slot discrepancy. After creating a physical slot, generating WAL, advancing it, and observing the newer `restart_lsn`, a server restart caused the slot to return to the older value.

The report identifies the key boundary: the physical path changed the **in-memory** slot state but did not arrange for that updated persistent data to be saved. The same discussion distinguished logical-slot behavior because logical advancement already dirtied the slot through its own path.

Thus the affected implementation directly falsifies:

`SQL-visible frontier movement == already restart-persistent frontier movement`

### H/P — the January-2020 fix made physical advancement participate in checkpoint persistence

PostgreSQL's **30 January 2020** commit announcement for `b0afdcad21fde1470e6502a376bfaf0e10d384fa` says physical advancement had failed to mark the slot dirty, preventing the follow-up checkpoint from flushing the slot data to disk. The advance could therefore be lost even on a clean restart, unlike the logical path.

The fix marked the physical slot for persistence and added recovery/TAP tests for both physical and logical slot advancement across clean restarts. It was explicitly **backpatched through version 11**.

### H/P — released 11.7 and 12.2 carry the correction

PostgreSQL **11.7** and **12.2**, both released on **13 February 2020**, explicitly record the physical-slot advancement persistence fix.

`fix commit date != supported release date`

### H/P — persistence remains checkpoint-mediated; a crash can still expose an earlier slot position

PostgreSQL 12 documentation states that updated slot information is written at the **follow-up checkpoint** when advancement occurs and separately warns that a crash can return the slot to an earlier position. The January-2020 design discussion intentionally preserved this behavior instead of requiring an immediate flush inside the SQL function.

The released contract is therefore:

```text
advance returns
    -> updated slot state exists
    -> slot is marked/scheduled for checkpoint persistence
    -> checkpoint writes the updated slot state
```

A crash may interrupt the sequence before the newer frontier becomes the restart-recovered frontier.

---

## Engineering reconstruction

### E — operation completion, control-state persistence, and WAL reclamation are separate transitions

A physical slot's `restart_lsn` is a control relation that helps determine how far back WAL may still be needed. Moving it forward changes the **claim on history**; it does not itself contain WAL and it is not the filesystem operation that removes old segments.

```text
administrator requests slot advance
        -> new restart_lsn becomes current in memory
        -> slot state is marked for checkpoint write
        -> later checkpoint makes that control state restart-recoverable
        -> WAL-removal machinery may later treat older history as reclaimable
        -> old WAL may later be removed
```

Each arrow has a distinct observation and failure boundary.

### E — SQL completion is not synchronous durability of the slot frontier

After the 2020 fix, a successful `pg_replication_slot_advance()` tells the caller the position actually reached. It does not prove that the slot's on-disk state has already crossed the next checkpoint boundary.

> **function completion != checkpoint durability of the retention frontier**

### E — clean-restart persistence and arbitrary-crash persistence are different guarantees

The fix repaired a defect that could lose physical advancement even on clean restart and added clean-restart tests. The retained design still permits a crash before the follow-up checkpoint to recover an earlier position.

> **clean restart after the persistence path has run != arbitrary crash at every point after SQL return**

### E — moving `restart_lsn` changes reclamation authority before proving completed reclamation

An advanced physical slot may cease to require some older WAL. That weakens one protection relation, but the SQL function does not prove that old files were immediately unlinked, overwritten, or made unrecoverable.

This aligns with Case 141's later `unreserved`/`lost` distinction:

> **retention protection withdrawn or narrowed != history already physically absent**

### E/A — one SQL function over physical and logical slots does not imply one persistence path

The 2019–2020 bug is a direct interface-level counterexample. PostgreSQL exposed one administrative function for both slot kinds, yet the paths differed in whether advancement dirtied persistent slot state.

> **same operation name / similar returned progress != identical persistence implementation**

This is a bounded functional comparison, not a deeper genealogy claim.

---

## Functional analogy

The narrow cross-case comparison is **checkpointed control-state persistence**. Kafka high-watermark checkpoints, HDFS retained authority state, DDR5 ECS summaries, and PostgreSQL slot state all make it necessary to ask whether a currently visible control value is also recoverable after restart.

Their protocols, authority models, persistence frequencies, and failure consequences differ. No technical identity or historical continuity is asserted.

---

## Philosophical interpretation — bounded

Project interpretation only: a retained history can depend on a second-order retained relation that says which history still matters, and that relation can itself have a persistence delay. This is not PostgreSQL vocabulary and must not replace the implementation terms `restart_lsn`, dirty slot state, checkpoint, or WAL removal.

---

## Rejected / unsupported claims

- **X — `pg_replication_slot_advance()` return means the slot frontier has already been synchronously flushed to durable storage.** Rejected by the checkpoint-mediated documentation and crash warning.
- **X — the 2020 fix removed all possible backward movement after crash.** Rejected: the project explicitly retained that possibility.
- **X — advancing a physical slot immediately deletes every older WAL segment.** Rejected: frontier change and reclamation are different operations/horizons.
- **X — advancing a slot sanitizes old WAL.** Rejected: slot semantics prove nothing about archive copies, backups, filesystem remnants, device overprovisioning, or forensic unrecoverability.
- **X — identical SQL API means physical and logical slots had identical persistence paths.** Rejected by the bug itself.
- **X — January 2018 or January 2020 establishes invention priority.** Rejected: these dates establish PostgreSQL implementation/fix floors only.

---

## Claim ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| `pg_replication_slot_advance()` was added for physical and logical slots in January 2018 | `H/P` | PostgreSQL committers announcement for `9c7d06d...` |
| a physical slot could show an advanced `restart_lsn` yet revert after restart | `H/P` | 24-Dec-2019 reproducible pgsql-hackers report |
| the defect was missing dirty-state marking on physical advancement | `H/P` | bug discussion + 30-Jan-2020 commit announcement |
| logical advancement already dirtied its slot state | `H/P` | same first-party fix record |
| the fix was backpatched through 11 and released in 11.7/12.2 | `H/P` | commit announcement + official release notes |
| updated slot state is written at the follow-up checkpoint | `H/P` | PostgreSQL 12 official docs |
| a crash can still return the slot to an earlier persisted position | `H/P` | official docs + design discussion |
| SQL completion is not synchronous slot-state durability | `E` | derived from checkpoint/crash contract |
| in-memory frontier movement is not identical to on-disk frontier movement | `E` | direct bug/fix boundary |
| advanced frontier is not completed WAL reclamation | `E` | Case 141 slot/WAL separation + function scope |
| same SQL operation does not prove identical physical/logical persistence paths | `E/A` | bounded cross-slot comparison |
| slot advancement proves secure erasure of old WAL | `X` | no sanitization evidence |

## Open work after this slice

This closes the bounded **physical-slot manual-advance persistence** debt listed in Case 141. Still open:

- pre-2018 proposal/review genealogy for `pg_replication_slot_advance()`;
- later `ReplicationSlotsComputeRequiredLSN()` / checkpoint-ordering and race fixes as a separate implementation-evolution slice;
- archive/base-backup/reinitialization interactions when retained WAL is no longer locally available;
- production traces showing divergence between live and last-checkpointed slot state;
- controlled crash/fault injection around SQL return, checkpoint, restart, and WAL removal;
- lower-layer filesystem/device durability validation.

A fresh search of `tmzncty/computing-archaeology` found no dedicated PostgreSQL replication-slot module to reuse in this round. Broader PostgreSQL WAL/replication genealogy should remain there rather than becoming a general database history in `technical-retention`.
