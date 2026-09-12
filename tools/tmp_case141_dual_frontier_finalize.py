from pathlib import Path
import re

case = Path('cases/141-postgresql-replication-slot-wal-retention-frontier.md')
text = case.read_text()
ev = '- [`../evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md`](../evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md)'
if ev not in text:
    anchor = '- [`../evidence/141-postgresql-2024-failover-slot-synchronization-deepening.md`](../evidence/141-postgresql-2024-failover-slot-synchronization-deepening.md)'
    if anchor not in text:
        raise SystemExit('case top evidence anchor missing')
    text = text.replace(anchor, anchor + '\n' + ev, 1)

heading = '## 2014–2015 deepening — logical consumer acknowledgement and WAL restart are distinct frontiers'
if heading not in text:
    insert_before = '## 2024 deepening — failover-slot synchronization makes the retention frontier itself cross-node state'
    if insert_before not in text:
        raise SystemExit('2024 heading missing')
    section = '''## 2014–2015 deepening — logical consumer acknowledgement and WAL restart are distinct frontiers

The released PostgreSQL 9.4 logical-slot implementation already persists **two different positions**. `ReplicationSlotPersistentData` contains both `confirmed_flush`, tied to client acknowledgement, and `restart_lsn`, the oldest WAL position that the slot may still require. The same 9.4 header retains `candidate_restart_valid` / `candidate_restart_lsn` as logical-slot working state.

`LogicalConfirmReceivedLocation()` makes the distinction operational rather than nominal. Consumer confirmation directly advances `confirmed_flush`; `restart_lsn` moves only when a prepared restart candidate exists and its validity position has been reached by confirmed progress. The neighboring source comment describes the restart candidate as the minimal LSN needed to replay transactions that had not yet committed at the candidate's point.

Thus:

```text
consumer acknowledgement frontier (`confirmed_flush`)
    != WAL restart/reclamation frontier (`restart_lsn`)
```

and, more specifically:

`confirmed progress advanced != every older WAL record immediately reclaimable`

PostgreSQL's own 10-August-2015 commit `3f811c2d6f51b13b71adff99e82894dd48cee055`, which exposes `confirmed_flush_lsn` in `pg_replication_slots`, states that the two positions have “rather distinct meanings” and notes that `restart_lsn` will commonly be older than the confirmed position. PostgreSQL 9.5 then documents `confirmed_flush_lsn` as logical-slot consumer receipt progress while `restart_lsn` remains the oldest possibly required WAL.

There is also an observability chronology. PostgreSQL 9.4 source already persists `confirmed_flush`, but the documented 9.4 `pg_replication_slots` view exposes only `restart_lsn`; the separate `confirmed_flush_lsn` view column arrives with the 2015 commit. Therefore:

`persistent internal control state != operator-visible telemetry surface`

and:

`2015 view-column introduction != 2015 invention of the underlying persisted state`.

### Engineering reconstruction — acknowledgement is permission input, not completed reclamation

Consumer acknowledgement can make a candidate restart position admissible, but acknowledgement is not itself WAL deletion and the two positions need not coincide. “Consumer has seen through X” and “server may forget every WAL byte before X” are different propositions.

### Functional analogy and stop condition

Other repository log cases also separate progress evidence from history liveness, but this is only a functional analogy. PostgreSQL's candidate restart logic is not Kafka high-watermark logic, Raft snapshot compaction, or LSM obsolete-file reclamation, and no genealogy is claimed.

Neither frontier is a sanitization witness. Moving either value says nothing by itself about filesystem remnants, archived WAL, backups, device overprovisioning, or forensic recoverability.

Full source/claim separation is recorded in [`../evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md`](../evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md).

'''
    text = text.replace(insert_before, section + insert_before, 1)

cex_anchor = '- **`restart_lsn` != full replay history.** It is a frontier, not the retained records themselves.'
if '- **`confirmed_flush_lsn` != `restart_lsn`.**' not in text:
    if cex_anchor not in text:
        raise SystemExit('counterexample anchor missing')
    text = text.replace(cex_anchor, cex_anchor + '\n- **`confirmed_flush_lsn` != `restart_lsn`.** Logical consumer acknowledgement and the oldest WAL still needed for decoding are distinct frontiers.\n- **Consumer acknowledgement != completed WAL reclamation.** Confirmation can permit a restart candidate to advance; it is not itself a checkpoint/removal event.', 1)

text = text.replace('2. physical-slot versus logical-slot advancement semantics in release-by-release detail;', '2. physical-slot advancement and release-by-release semantics beyond the now-grounded logical `confirmed_flush` / `restart_lsn` split;', 1)
bottom = '- [Evidence 141 deepening — PostgreSQL 17 failover-slot synchronization](../evidence/141-postgresql-2024-failover-slot-synchronization-deepening.md)'
bottom_new = '- [Evidence 141B — logical-slot `confirmed_flush` vs `restart_lsn` dual frontier](../evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md)'
if bottom_new not in text:
    if bottom not in text:
        raise SystemExit('bottom evidence anchor missing')
    text = text.replace(bottom, bottom + '\n' + bottom_new, 1)
case.write_text(text)

roadmap = Path('ROADMAP.md')
r = roadmap.read_text()
marker = '**Case 141 deepening — PostgreSQL logical-slot acknowledgement vs WAL-restart dual frontier**'
if marker not in r:
    anchor = '### Recent bounded evidence deepening\n\n'
    if anchor not in r:
        raise SystemExit('roadmap recent section missing')
    item = '- [x] **Case 141 deepening — PostgreSQL logical-slot acknowledgement vs WAL-restart dual frontier** — [`cases/141-postgresql-replication-slot-wal-retention-frontier.md`](cases/141-postgresql-replication-slot-wal-retention-frontier.md), deepened by [`evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md`](evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md): PostgreSQL `REL9_4_0` source shows `confirmed_flush` and `restart_lsn` already persisted as different logical-slot positions, with consumer confirmation advancing the former while the latter moves only through a validity-gated restart candidate. The 10-August-2015 `3f811c2d` commit then exposes `confirmed_flush_lsn` and explicitly says the two positions have distinct meanings, closing the bounded `consumer acknowledgement != WAL reclaimability frontier` and `persistent internal state != operator-visible telemetry` seams. Physical-slot advancement, pre-9.4 proposal genealogy, later long-transaction/candidate evolution, archive/base-backup/slot-copy interaction, production divergence traces, and fault injection remain open; broader genealogy remains for `computing-archaeology`.\n\n'
    r = r.replace(anchor, anchor + item, 1)
roadmap.write_text(r)

index = Path('CASE_INDEX.md')
i = index.read_text()
row_pattern = re.compile(r'^\| \[PostgreSQL Replication Slots: WAL Retention Frontier and Continuation Admission\].*$', re.M)
new_row = '| [PostgreSQL Replication Slots: WAL Retention Frontier and Continuation Admission](cases/141-postgresql-replication-slot-wal-retention-frontier.md) | **grounded** | persistent replication-slot metadata + logical `confirmed_flush` acknowledgement frontier + `restart_lsn` WAL-need frontier + retained WAL history + downstream continuation eligibility | separate consumer-confirmed logical progress from raw-WAL restart need, primary current state, slot persistence, activity, WAL protection/physical availability, resource-bounded reclamation, and slot usability | [2014–2020 grounding](evidence/141-postgresql-2014-2020-replication-slot-wal-retention-grounding.md) + [9.4/9.5 logical dual-frontier deepening](evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md) + [2024 failover-slot deepening](evidence/141-postgresql-2024-failover-slot-synchronization-deepening.md); physical-slot advancement, pre-9.4 genealogy, archive/reinitialization, post-17 evolution, production traces, and fault injection remain open |'
matches = row_pattern.findall(i)
if len(matches) != 1:
    raise SystemExit(f'expected one Case 141 row, found {len(matches)}')
i = row_pattern.sub(new_row, i, count=1)

if '**3588 —' not in i:
    findings = '''

## Case 141 — PostgreSQL logical-slot confirmed-flush / restart-frontier deepening findings

Deepening record: [`evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md`](evidence/141-postgresql-logical-slot-confirmed-flush-restart-frontier-deepening.md).

- **3588 — PostgreSQL 9.4 persists two logical-slot positions:** `REL9_4_0` `ReplicationSlotPersistentData` contains both `restart_lsn` and `confirmed_flush`, so WAL restart need and client acknowledgement are not modeled as one field. (`H/P`)
- **3589 — the fields have different historical meanings:** 9.4 source ties `restart_lsn` to the oldest LSN possibly required by the slot and `confirmed_flush` to client-acknowledged receipt. (`H/P`)
- **3590 — consumer confirmation directly advances `confirmed_flush`:** `LogicalConfirmReceivedLocation()` writes the confirmed LSN into persistent slot data. (`H/P`)
- **3591 — `restart_lsn` advancement is candidate-gated:** the same 9.4 path updates `restart_lsn` only when `candidate_restart_valid` exists and has been reached by confirmed progress. (`H/P`)
- **3592 — a restart candidate represents older replay need:** adjacent source describes the candidate as the minimal LSN needed to replay transactions not yet committed at the candidate point. (`H/P`)
- **3593 — consumer acknowledgement frontier != WAL restart/reclamation frontier:** acknowledged logical progress can advance while the older WAL-need frontier remains behind. (`E`)
- **3594 — confirmation is permission input, not a deletion event:** crossing a candidate-validity point can authorize `restart_lsn` movement but does not itself remove a WAL segment. (`E, X`)
- **3595 — logical output availability != raw-WAL physical absence:** older logical changes can be unavailable to the slot consumer while older WAL remains needed through `restart_lsn`. (`E, X`)
- **3596 — PostgreSQL 9.4 internal persistence predates view exposure:** released 9.4 source persists `confirmed_flush`, while the documented 9.4 `pg_replication_slots` view exposes `restart_lsn` but not `confirmed_flush_lsn`. (`H/P`)
- **3597 — telemetry exposure != state introduction:** the 2015 system-view addition cannot be treated as invention of the already-present 9.4 persisted `confirmed_flush` state. (`E, X`)
- **3598 — PostgreSQL itself says the positions have distinct meanings:** commit `3f811c2d` of 10-August-2015 exposes `confirmed_flush_lsn` and states that it differs from `restart_lsn`, which is commonly older. (`H/P`)
- **3599 — `confirmed_flush_lsn` is logical-slot-specific telemetry:** PostgreSQL 9.5 documents it as consumer-confirmed receipt progress and `NULL` for physical slots. (`H/P`)
- **3600 — one retained history can have multiple permission frontiers:** this case supports a bounded reconstruction separating “consumer has acknowledged through here” from “server may no longer need WAL before here”. (`E`)
- **3601 — cross-log similarity remains functional only:** progress/history-liveness splits in Kafka, Raft, or LSM cases do not establish mechanism identity or PostgreSQL lineage. (`A, X`)
- **3602 — neither frontier is a sanitization boundary:** advancement does not prove deletion from filesystem, archive, backup, device, or forensic embodiments. (`X`, rejected upgrade)
- **3603 — scope remains version-bounded:** this slice grounds the PostgreSQL 9.4/9.5 logical dual-frontier baseline, not all later candidate-restart behavior, physical-slot semantics, production lag distributions, or fault behavior. (`X`, scope boundary)
'''
    i = i.rstrip() + findings + '\n'
index.write_text(i)
