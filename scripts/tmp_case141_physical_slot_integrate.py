from pathlib import Path

EVIDENCE_PATH = Path('evidence/141-postgresql-2018-2020-physical-slot-advance-persistence-deepening.md')
CASE_PATH = Path('cases/141-postgresql-replication-slot-wal-retention-frontier.md')
ROADMAP_PATH = Path('ROADMAP.md')
INDEX_PATH = Path('CASE_INDEX.md')

if EVIDENCE_PATH.exists():
    raise SystemExit(f'{EVIDENCE_PATH} already exists; refusing duplicate integration')

EVIDENCE_PATH.write_text(r'''# Case 141 Evidence Deepening: PostgreSQL 2018–2020 Physical Replication-Slot Advance Persistence

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
''', encoding='utf-8')

case = CASE_PATH.read_text(encoding='utf-8')
bullet = "- [`../evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md`](../evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md)\n"
if bullet not in case:
    raise SystemExit('Case 141 evidence-list marker not found')
case = case.replace(bullet, bullet + "- [`../evidence/141-postgresql-2018-2020-physical-slot-advance-persistence-deepening.md`](../evidence/141-postgresql-2018-2020-physical-slot-advance-persistence-deepening.md)\n", 1)
section_marker = "## 2024 deepening — failover-slot synchronization makes the retention frontier itself cross-node state\n"
if section_marker not in case:
    raise SystemExit('Case 141 section insertion marker not found')
section = r'''## 2018–2020 deepening — physical-slot advancement exposes the retention frontier's own persistence horizon

PostgreSQL added `pg_replication_slot_advance()` on **17 January 2018** for both physical and logical slots. A **24 December 2019** pgsql-hackers report then showed that a physical slot's newly advanced `restart_lsn` could be visible before restart and revert afterward because the physical path had changed only in-memory state without marking persistent slot data dirty.

The **30 January 2020** fix (`b0afdcad21fde1470e6502a376bfaf0e10d384fa`, backpatched through 11) made physical advancement participate in checkpoint-driven slot persistence. PostgreSQL 11.7 and 12.2, released **13 February 2020**, carry the fix. Released PostgreSQL 12 documentation nevertheless keeps the checkpoint boundary explicit: updated slot information is written at the follow-up checkpoint, and a crash can still return the slot to an earlier position.

```text
new restart_lsn returned / visible in memory
    != updated slot frontier already written for restart recovery
    != older WAL physically reclaimed
```

### Engineering reconstruction — the claimant on WAL has a delayed persistence boundary

A physical slot's `restart_lsn` is a compact claimant on history. Advancing it can narrow the WAL prefix that the slot still requires, but the claimant itself first crosses an in-memory-to-checkpoint persistence boundary. Only separately can WAL-removal machinery use the newer frontier and later reclaim files.

This closes `function returned != checkpoint-durable slot frontier`, `clean-restart persistence != arbitrary-crash persistence immediately after return`, and `restart_lsn advanced != old WAL already removed`. The physical/logical discrepancy also supplies a direct counterexample to assuming that one SQL interface means one internal persistence path.

### Functional analogy and stop condition

The bounded analogy is to other checkpointed control-state cases; it is not mechanism identity with Kafka, HDFS, or DRAM maintenance state. Slot advancement is also not sanitization: it changes a replay-history retention relation without proving secure erasure of local WAL remnants, archives, backups, or lower-layer embodiments.

Full source/claim separation is recorded in [`../evidence/141-postgresql-2018-2020-physical-slot-advance-persistence-deepening.md`](../evidence/141-postgresql-2018-2020-physical-slot-advance-persistence-deepening.md).

'''
case = case.replace(section_marker, section + section_marker, 1)
CASE_PATH.write_text(case, encoding='utf-8')

roadmap = ROADMAP_PATH.read_text(encoding='utf-8')
roadmap = roadmap.replace(
    "This closes only the bounded retention-frontier/resource-authority relation; pre-2014 genealogy, detailed physical/logical-slot evolution, archive/reinitialization paths, failover-slot semantics, production disk-pressure traces, and fault injection remain open.",
    "This closes only the bounded retention-frontier/resource-authority relation; pre-2014 genealogy, remaining physical/logical-slot evolution, archive/reinitialization paths, failover-slot semantics, production disk-pressure traces, and fault injection remain open.",
    1,
)
old_recent = "Physical-slot advancement, pre-9.4 proposal genealogy, later long-transaction/candidate evolution, archive/base-backup/slot-copy interaction, production divergence traces, and fault injection remain open; broader genealogy remains for `computing-archaeology`."
if old_recent not in roadmap:
    raise SystemExit('Roadmap Case 141 recent open-work marker not found')
roadmap = roadmap.replace(old_recent, "Pre-9.4 proposal genealogy, later long-transaction/candidate evolution, archive/base-backup/slot-copy interaction, production divergence traces, and fault injection remain open; broader genealogy remains for `computing-archaeology`.", 1)
heading = "### Recent bounded evidence deepening\n\n"
pos = roadmap.find(heading)
if pos < 0:
    raise SystemExit('Roadmap recent-deepening heading not found')
insert_at = pos + len(heading)
item = "- [x] **Case 141 deepening — PostgreSQL physical-slot advance persistence horizon (2018–2020)** — [`cases/141-postgresql-replication-slot-wal-retention-frontier.md`](cases/141-postgresql-replication-slot-wal-retention-frontier.md), deepened by [`evidence/141-postgresql-2018-2020-physical-slot-advance-persistence-deepening.md`](evidence/141-postgresql-2018-2020-physical-slot-advance-persistence-deepening.md): PostgreSQL's 17-Jan-2018 `pg_replication_slot_advance()` feature, a 24-Dec-2019 reproducible physical-slot restart regression, and the 30-Jan-2020 backpatched fix ground a distinct persistence horizon for the retention frontier itself. The fix marks physical advancement for checkpoint persistence, while released docs preserve the crash rule that the slot may return to an earlier position before that persistence boundary. This closes `SQL return != checkpoint-durable frontier`, `in-memory restart_lsn != persisted slot state`, `clean-restart persistence != arbitrary-crash persistence`, and `frontier advanced != WAL physically removed`, without treating physical/logical slot paths as identical or slot advancement as sanitization. Later required-LSN/checkpoint evolution, production traces, and fault injection remain open; broader PostgreSQL replication genealogy belongs primarily in `computing-archaeology`.\n\n"
roadmap = roadmap[:insert_at] + item + roadmap[insert_at:]
ROADMAP_PATH.write_text(roadmap, encoding='utf-8')

index = INDEX_PATH.read_text(encoding='utf-8')
old_tail = "[2014–2020 grounding](evidence/141-postgresql-2014-2020-replication-slot-wal-retention-grounding.md) + [9.4/9.5 logical dual-frontier deepening](evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md) + [2024 failover-slot deepening](evidence/141-postgresql-2024-failover-slot-synchronization-deepening.md); physical-slot advancement, pre-9.4 genealogy, archive/reinitialization, post-17 evolution, production traces, and fault injection remain open |"
if old_tail not in index:
    raise SystemExit('CASE_INDEX Case 141 row marker not found')
new_tail = "[2014–2020 grounding](evidence/141-postgresql-2014-2020-replication-slot-wal-retention-grounding.md) + [9.4/9.5 logical dual-frontier deepening](evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md) + [2018–2020 physical-slot advance persistence deepening](evidence/141-postgresql-2018-2020-physical-slot-advance-persistence-deepening.md) + [2024 failover-slot deepening](evidence/141-postgresql-2024-failover-slot-synchronization-deepening.md); pre-9.4 genealogy, archive/reinitialization, later required-LSN/checkpoint evolution, post-17 evolution, production traces, and fault injection remain open |"
index = index.replace(old_tail, new_tail, 1)
if '### Findings 3652–3667 — Case 141 physical-slot advance persistence horizon' in index:
    raise SystemExit('CASE_INDEX findings already present')
findings = r'''

### Findings 3652–3667 — Case 141 physical-slot advance persistence horizon

- **3652 — H/P** — PostgreSQL commit `9c7d06d60680c7f00d931233873dee81fdb311c6` added `pg_replication_slot_advance()` for both physical and logical replication slots on 17 January 2018.
- **3653 — H/P** — The physical-slot path can expose a newly advanced `restart_lsn`, making the administrative operation directly relevant to the WAL-retention frontier rather than merely to connection activity.
- **3654 — H/P** — A 24 December 2019 PostgreSQL project bug report reproduced an advanced physical `restart_lsn` reverting to its older value after server restart.
- **3655 — H/P** — The reported defect was a persistence-path difference: physical advancement changed in-memory slot state without marking the slot dirty, while logical advancement already dirtied its slot state through its own path.
- **3656 — H/P** — PostgreSQL's 30 January 2020 fix `b0afdcad21fde1470e6502a376bfaf0e10d384fa` marked physical advancement for persistence, added clean-restart tests, and was explicitly backpatched through version 11.
- **3657 — H/P** — PostgreSQL 11.7 and 12.2, both released 13 February 2020, explicitly record the physical-slot advancement persistence fix.
- **3658 — H/P** — Released PostgreSQL 12 documentation states that updated slot-position information is written at the follow-up checkpoint when advancement occurs.
- **3659 — H/P** — The same documentation preserves a crash boundary: after a crash, the slot may return to an earlier position.
- **3660 — E** — A successful `pg_replication_slot_advance()` return is therefore not a synchronous durability acknowledgement for the new slot frontier.
- **3661 — E** — Current in-memory `restart_lsn` and restart-recovered on-disk slot state are distinct persistence horizons even though they describe the same logical frontier.
- **3662 — E** — Repairing clean-restart persistence does not establish arbitrary-crash persistence at every instant after SQL completion; the checkpoint boundary remains operative.
- **3663 — E** — Advancing `restart_lsn` changes or narrows the slot's claim on old WAL but is not itself proof that the corresponding WAL files have already been reclaimed.
- **3664 — E/A** — One SQL function serving physical and logical slots does not imply identical internal persistence paths; the 2019–2020 discrepancy is a direct counterexample to interface-level normalization.
- **3665 — A** — The bounded cross-case analogy is checkpointed control-state persistence, not a shared protocol or genealogy with Kafka, HDFS, DRAM maintenance telemetry, or other repository cases.
- **3666 — X** — The 2020 fix does not prove immediate fsync/atomic durability at function return, and the project documentation explicitly retains possible backward movement after crash.
- **3667 — X** — Slot-frontier advancement is neither completed WAL deletion nor sanitization, and the 2018/2020 PostgreSQL dates do not establish invention priority for replication-progress advancement or checkpointed metadata.
'''
INDEX_PATH.write_text(index.rstrip() + findings + '\n', encoding='utf-8')
