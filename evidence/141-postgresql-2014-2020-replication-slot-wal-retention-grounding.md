# Evidence 141 — PostgreSQL 2014–2020 replication-slot WAL-retention grounding

**Status:** grounded  
**Case:** [`../cases/141-postgresql-replication-slot-wal-retention-frontier.md`](../cases/141-postgresql-replication-slot-wal-retention-frontier.md)  
**Bounded question:** how can a retained consumer-progress/need frontier keep otherwise reclaimable WAL history alive, and what changes when the primary is later allowed to sacrifice that continuation guarantee to bound local storage consumption?

## Evidence boundary

This record is deliberately narrow. It does **not** attempt a general history of PostgreSQL streaming replication, logical decoding, WAL, hot standby, checkpoints, base backups, or database recovery.

It uses two source-bounded moments:

1. **PostgreSQL 9.4 development/release (2014):** replication slots become a crash-safe retained control state that prevents premature WAL removal for a consumer, including while a standby is disconnected. The released 9.4 documentation explicitly notes that replication-slot WAL retention had no built-in space bound.
2. **PostgreSQL 13 development/release (2020):** `max_slot_wal_keep_size` introduces an explicit resource cap. A slot can cease to protect its required WAL and eventually become unusable once needed segments are removed. The final 13-era `wal_status` vocabulary distinguishes `reserved`, `extended`, `unreserved`, and `lost`.

The 2020 terms are **not** projected backward into PostgreSQL 9.4. They are later implementation/history evidence showing that the original retention relation was subsequently made resource-bounded.

## Source ladder

| Source | Date | Evidence class | Use here |
|---|---:|---|---|
| PostgreSQL commit `858ec11858a914d4c380971985709b6d6b7dd6fc`, “Introduce replication slots” | 2014-02-01 | `H/P` | explicit crash-safe slot purpose; prevent premature removal of WAL needed by a standby; initial physical-slot implementation |
| PostgreSQL 9.4 release notes | 2014-12-18 | `H/P` | released-feature chronology and project description of replication slots |
| PostgreSQL 9.4 `REL9_4_0` `slot.c` / `slot.h` | 2014 release tree | `H/P` | on-disk persistent slot state, `restart_lsn`, dirty/save/checkpoint/startup behavior, minimum required LSN aggregation |
| PostgreSQL 9.4 replication-slot / warm-standby documentation | 9.4 release series | `H/P` | `restart_lsn` meaning, disconnected-standby protection, retention-versus-space tradeoff, explicit absence of a slot-space bound |
| PostgreSQL commit `c6550776394e25c1620bc8258427c8f1d448080d` | 2020-04-07 | `H/P` | adds `max_slot_wal_keep_size`; records operational motive; invalidates over-limit slots at checkpoint so storage can be released |
| PostgreSQL commit `b8fd4e02c6d01183bf6def5897ad6cf7766bfff4` | 2020-06-24 | `H/P` | finalizes `reserved` / `extended` / `unreserved` / `lost` availability-state distinction before v13 release |
| PostgreSQL 13 release notes and docs | 2020-09-24 release | `H/P` | released cap and user-visible WAL-availability contract |

All central sources are PostgreSQL project primary materials: source code, commit records, and official documentation. This is sufficient for the bounded implementation/contract claim; it is not independent empirical validation of disk-pressure or crash behavior on a particular production deployment.

## Historical record

### 1. The February 2014 introduction explicitly calls replication slots crash-safe

Commit [`858ec11858a914d4c380971985709b6d6b7dd6fc`](https://github.com/postgres/postgres/commit/858ec11858a914d4c380971985709b6d6b7dd6fc), committed 1 February 2014, is titled **“Introduce replication slots.”** Its commit message states that replication slots are a **crash-safe data structure** intended to prevent premature removal of write-ahead-log segments needed by a standby. It also notes that the initial patch calls this form a `physical` slot because logical-decoding slots were forthcoming.

This gives a precise historical floor for the implementation entering the PostgreSQL tree. It does not by itself prove earlier proposal priority, production deployment on that date, or the complete logical-slot semantics that existed by the final 9.4 release.

PostgreSQL 9.4 was released on **18 December 2014**. The official release notes list replication slots as a 9.4 replication feature and describe them as coordinating streaming standbys by preserving WAL until it is no longer needed.

**Anchors:**

- commit: <https://github.com/postgres/postgres/commit/858ec11858a914d4c380971985709b6d6b7dd6fc>
- PostgreSQL 9.4 release notes: <https://www.postgresql.org/docs/9.4/release-9-4.html>

### 2. The retained slot object and the WAL it protects are different state

The released `REL9_4_0` source is unusually explicit about this distinction.

`src/backend/replication/slot.c` says replication slots keep state about replication streams and that their primary purpose is to prevent premature removal of WAL or old tuple versions. It states that slots need to be **permanent (to allow restarts)** and **crash-safe**. Each slot has its own directory under `$PGDATA/pg_replslot`; an on-disk state file holds its data, while a copy is cached in memory while the server runs.

`src/include/replication/slot.h` defines persistent slot data separately from shared-memory working fields. Among the persistent fields is:

- `restart_lsn` — “oldest LSN that might be required by this replication slot”.

The same header marks the persistent data as surviving shutdowns and crashes. Persistent and ephemeral slot lifetimes are explicitly distinct: persistent slots remain across release/restart, whereas ephemeral slots are dropped on release or restart.

This supports:

`retained slot metadata != retained WAL payload/history`

The slot is a small control object that can force a much larger population of WAL segments to remain available.

**Anchors:**

- `REL9_4_0` `slot.c`: <https://github.com/postgres/postgres/blob/REL9_4_0/src/backend/replication/slot.c>
- `REL9_4_0` `slot.h`: <https://github.com/postgres/postgres/blob/REL9_4_0/src/include/replication/slot.h>

### 3. `restart_lsn` is a retention frontier, not a copy of the retained history

The PostgreSQL 9.4 `pg_replication_slots` documentation defines `restart_lsn` as the address of the **oldest WAL that still might be required by the consumer of the slot** and therefore is not automatically removed during checkpoints.

In `REL9_4_0` source, `ReplicationSlotsComputeRequiredLSN()` scans all defined slots, takes the oldest valid `restart_lsn`, and passes that minimum requirement into the WAL subsystem via `XLogSetReplicationSlotMinimumLSN()`.

The engineering relation is therefore:

```text
small retained frontier metadata
    -> oldest still-required WAL position
    -> WAL-removal lower bound
    -> older log segments remain physically available for future consumer catch-up
```

The frontier summarizes a **need relation**. It does not encode the intervening WAL records themselves and is not a complete history of what the standby has done.

**Anchors:**

- PostgreSQL 9.4 `pg_replication_slots`: <https://www.postgresql.org/docs/9.4/catalog-pg-replication-slots.html>
- `REL9_4_0` `slot.c`: <https://github.com/postgres/postgres/blob/REL9_4_0/src/backend/replication/slot.c>

### 4. Consumer disconnection does not automatically terminate the retention obligation

The PostgreSQL 9.4 warm-standby documentation states that replication slots prevent required WAL removal and can protect required rows **even when the standby is disconnected**. This is exactly the retention distinction needed here:

`consumer currently active != consumer still has a future continuation claim`

The `active` state visible in `pg_replication_slots` is therefore not equivalent to the lifetime of the retained WAL obligation. An inactive/disconnected consumer may still be the reason old WAL remains.

This does **not** imply that a permanently abandoned slot should be kept forever. It establishes only the released mechanism: slot existence/current frontier can outlive the current connection and continue to constrain reclamation.

**Anchor:**

- PostgreSQL 9.4 warm standby / replication slots: <https://www.postgresql.org/docs/9.4/warm-standby.html#STREAMING-REPLICATION-SLOTS>

### 5. Crash-safe control state is actively serialized and reconstituted

In `REL9_4_0`:

- `ReplicationSlotSave()` serializes the acquired slot state from memory to disk and comments that this guarantees current slot state will survive a crash;
- marking a slot dirty does **not** mean it has already been flushed; the comment explicitly says actual flush may be delayed and code requiring correctness should call `ReplicationSlotSave()`;
- checkpoint processing saves all replication slots;
- startup scans `pg_replslot`, cleans incomplete `.tmp` directories, restores slots from disk, and recomputes required `xmin`/LSN constraints before normal operation proceeds;
- slot creation uses a temporary directory, writes/syncs state, renames it into place, and synchronizes the relevant paths.

This supports a second separation:

`in-memory slot update != crash-surviving slot update`

and, at the repository's lower-layer boundary:

`documented fsync/rename protocol != empirical proof that every storage stack honors the intended persistence contract`

The latter is a stop condition inherited from Cases 124 and 13-style durability analysis, not a defect claim against PostgreSQL.

**Anchor:**

- `REL9_4_0` `slot.c`: <https://github.com/postgres/postgres/blob/REL9_4_0/src/backend/replication/slot.c>

### 6. PostgreSQL 9.4 explicitly exposes the cost of exact consumer-driven history retention

The 9.4 warm-standby documentation contrasts replication slots with fixed `wal_keep_segments` and WAL archiving. It says slots avoid retaining more WAL than is known to be needed, but notes an important disadvantage of the original design: the alternatives can bound `pg_xlog` space while **there was then no way to do so using replication slots**.

This blocks an easy but false inference:

`more precise retention scope != bounded retention cost`

A slot can know precisely that an old prefix is still needed and, because that need remains valid, force the primary to keep accumulating history as the consumer falls farther behind.

**Anchor:**

- PostgreSQL 9.4 warm standby / replication slots: <https://www.postgresql.org/docs/9.4/warm-standby.html#STREAMING-REPLICATION-SLOTS>

### 7. PostgreSQL 13 deliberately makes the continuation guarantee resource-bounded

Commit [`c6550776394e25c1620bc8258427c8f1d448080d`](https://github.com/postgres/postgres/commit/c6550776394e25c1620bc8258427c8f1d448080d), committed 7 April 2020, is unusually useful because its rationale states the operational tradeoff directly. It says experience showed that allowing replication slots to retain excessive data could make the primary fail by running out of space. The change adds `max_slot_wal_keep_size`; slots that exceed the configured allowance are invalidated at checkpoint time so storage can be released.

PostgreSQL 13 release notes later record the feature: WAL storage retained for replication slots can be limited, and slots requiring more are marked invalid.

This is not merely a smaller cache size. It changes which retained relation wins under resource pressure:

```text
2014 default relation:
consumer still needs WAL -> keep WAL

2020 bounded relation when configured:
consumer still needs WAL
    + slot exceeds permitted retention budget
    -> retention protection may be withdrawn at checkpoint
    -> required WAL may be removed
    -> slot continuation can become impossible
```

**Anchors:**

- implementation commit: <https://github.com/postgres/postgres/commit/c6550776394e25c1620bc8258427c8f1d448080d>
- PostgreSQL 13 release notes: <https://www.postgresql.org/docs/13/release-13.html>
- PostgreSQL 13 replication settings: <https://www.postgresql.org/docs/13/runtime-config-replication.html>

### 8. `unreserved` and `lost` separate withdrawal of protection from completed history loss

A follow-up PostgreSQL 13 commit, [`b8fd4e02c6d01183bf6def5897ad6cf7766bfff4`](https://github.com/postgres/postgres/commit/b8fd4e02c6d01183bf6def5897ad6cf7766bfff4), committed 24 June 2020 and backpatched to the v13 line before release, refines the user-visible state machine to:

- `reserved` — needed WAL lies within ordinary WAL-size constraints;
- `extended` — needed WAL remains available because extra history is still being retained;
- `unreserved` — the slot no longer protects all required WAL, but the threatened files have not necessarily been removed yet; the slot may still catch up and return to a safer state;
- `lost` — required WAL has actually been removed and the slot is no longer usable.

The released PostgreSQL 13 `pg_replication_slots` documentation preserves this distinction.

This yields a particularly clean retention counterexample:

`physical presence now != protected future availability`

During `unreserved`, bytes may still physically exist in `pg_wal`, yet the slot's authority to keep them is already withdrawn. Conversely:

`protection withdrawn != loss already completed`

The consumer can sometimes catch up before checkpoint removal converts danger into `lost`.

**Anchors:**

- status-refinement commit: <https://github.com/postgres/postgres/commit/b8fd4e02c6d01183bf6def5897ad6cf7766bfff4>
- PostgreSQL 13 `pg_replication_slots`: <https://www.postgresql.org/docs/13/view-pg-replication-slots.html>

## Engineering reconstruction

### A. History liveness can be externally claimed

A WAL segment can be obsolete for the primary's immediate serving state yet still be live for a lagging downstream consumer. The consumer does not keep the segment alive by holding a direct filesystem reference; the slot retains a frontier that causes the WAL subsystem to withhold reclamation.

Thus:

`locally old != globally reclaimable under the configured replication relation`

### B. The retained frontier is second-order state

`restart_lsn` is not user payload and is not a copy of WAL. It is retained **about** which earlier WAL may still be needed. A few bytes of control metadata can therefore govern the liveness of a much larger historical population.

`retained maintenance/recovery metadata can dominate payload-history lifetime`

### C. Slot persistence and downstream continuation are separable

In the 2014 design, crash-safe slot state exists specifically so the retention obligation survives server restart. In the 2020 bounded design, however, the slot object can continue to exist while required WAL has become `lost` and the slot is unusable.

Therefore:

`slot metadata survives != replay substrate survives != downstream continuation remains admissible`

### D. Resource protection can become forgetting authority

`max_slot_wal_keep_size` turns local storage pressure into a policy capable of ending an older continuation relation. The mechanism does not decide that the historical WAL was semantically false or that the consumer no longer wanted it. It decides that retaining it is no longer permitted under the configured primary-space budget.

This is a bounded engineering statement about PostgreSQL's retention policy, not a general theorem that resource pressure always implies forgetting.

### E. `unreserved` is a revocable grace state, not completed loss

The 2020 state machine is important because it avoids collapsing three different facts:

1. WAL is still physically present;
2. WAL is still protected from reclamation;
3. WAL is still sufficient for future slot continuation.

Those relations can diverge temporarily.

## Cross-case comparison

### Case 58 — Raft snapshotting

Raft 2014 allows a leader to retire a committed log prefix after stable state plus continuation metadata has replaced it; a follower that falls behind the retained prefix can receive `InstallSnapshot` rather than the missing entries.

PostgreSQL 9.4 replication slots take a different bounded path: the primary can keep the required WAL history itself because a lagging consumer still needs it. PostgreSQL 13 then adds a configured point at which this history-retention promise may be withdrawn to protect primary storage.

Functional comparison only:

`Raft history retirement + state-transfer substitute != PostgreSQL slot-pinned WAL replay history`

No genealogy is claimed.

### Case 57 — Bigtable log/materialization recovery

Bigtable redo points decide what history a tablet needs to rebuild local current state after failure. PostgreSQL replication-slot `restart_lsn` can instead represent history needed by a **different consumer** to continue from the primary.

`local recovery frontier != downstream-consumer retention frontier`

### Case 137 — LevelDB file liveness

LevelDB shows an obsolete SSTable can remain physically live because an older in-process `Version`/iterator still references it. PostgreSQL slots provide a distributed analogue only at the functional level: a log segment that the primary would otherwise recycle can remain live because a remote consumer's retained frontier still claims it.

`reference-pinned local file liveness ~ consumer-frontier-pinned WAL liveness`

The mechanism, failure model, and history are different.

## Philosophical interpretation — bounded

The useful conceptual point is small:

> A past log segment can remain present not because the current primary state still needs it, but because a **future continuation relation** with another participant has not yet been discharged.

The 2020 cap then shows that such a future claim is not metaphysically absolute. Infrastructure can retain a separate authority to withdraw the preservation obligation when the local resource envelope is exceeded.

This is an interpretation of a documented engineering relation. It is **not** evidence that PostgreSQL developers were formulating a philosophy of memory, nor that all archives or memories are future-consumer claims.

## Counterexamples and stop conditions

- **Replication slot != WAL archive.** A slot retains a replay requirement/frontier; it is not itself the retained WAL corpus.
- **`restart_lsn` != complete consumer history.** It is a lower frontier for possibly required WAL.
- **Inactive/disconnected != abandoned.** Slot-backed retention can outlive the current connection.
- **Crash-safe slot != proof of lower-device crash safety.** The source documents the filesystem persistence protocol, not empirical compliance of every storage stack.
- **Exact needed-history retention != bounded disk consumption.** PostgreSQL 9.4 explicitly documents the original unbounded-space problem.
- **Configured WAL cap != graceful replication catch-up guarantee.** PostgreSQL 13 can invalidate the slot and sacrifice continuation.
- **`unreserved` != `lost`.** Protection can be withdrawn before the files are actually removed.
- **WAL physical presence != protected future availability.** An unreserved segment may still exist while being eligible for removal.
- **Slot invalidation / WAL recycling != secure erase.** No overwrite, block erase, crypto erase, or forensic disappearance is established.
- **PostgreSQL 13 vocabulary != PostgreSQL 9.4 vocabulary.** `max_slot_wal_keep_size` and the four-state `wal_status` model are later history.
- **Replication-slot WAL retention != consensus commitment.** Keeping replay history says nothing by itself about how a transaction became committed.
- **Replication-slot retention != snapshot state transfer.** A lagging consumer needing removed WAL may require reinitialization or another recovery source; this case does not claim a Raft-like substitute protocol.

## Open evidence debt

1. exact pre-2014 proposal/review genealogy and any precursor implementation outside the main tree;
2. detailed physical-slot versus logical-slot advancement rules beyond the common retention-frontier relation used here;
3. WAL-archive fallback and base-backup/reinitialization behavior under each slot-loss scenario;
4. later failover-slot synchronization and cross-primary continuity semantics;
5. production traces quantifying disk-pressure growth and time-to-loss under a named workload;
6. fault injection around slot-state persistence, checkpoint invalidation, and WAL removal;
7. lower-layer filesystem/device persistence validation for the `pg_replslot` save protocol.

## Related-repository check

A fresh search of `tmzncty/computing-archaeology` for `PostgreSQL replication slot`, `restart_lsn`, and replication-slot WAL retention found no dedicated overlapping study in this pass.

If a broader PostgreSQL WAL/replication genealogy is later developed, it belongs primarily in that companion repository. `technical-retention` keeps the narrower relation:

> **a retained frontier can keep history alive for a lagging future consumer; a later resource policy can withdraw that guarantee before the bytes have yet disappeared, and eventual history removal can invalidate continuation without constituting secure erasure.**

## Claim ledger

| Claim | Type | Evidence | Status |
|---|---|---|---|
| replication slots entered PostgreSQL mainline as a crash-safe WAL-retention mechanism in February 2014 | `H/P` | `858ec118...` | supported |
| PostgreSQL 9.4 was released 18 December 2014 with replication slots | `H/P` | 9.4 release notes | supported |
| persistent slot state includes `restart_lsn` and survives restart/crash by an explicit on-disk save/restore path | `H/P` | `REL9_4_0` `slot.h`, `slot.c` | supported |
| `restart_lsn` marks the oldest WAL that might still be required and constrains automatic removal | `H/P` | 9.4 docs + source | supported |
| a disconnected standby can remain protected by its slot | `H/P` | 9.4 warm-standby docs | supported |
| 9.4 replication-slot WAL retention lacked a built-in `pg_xlog` space bound | `H/P` | 9.4 warm-standby docs | supported |
| PostgreSQL 13 added `max_slot_wal_keep_size` to prevent excessive slot-retained WAL from exhausting primary storage | `H/P` | `c6550776...` + v13 release/docs | supported |
| over-limit slot invalidation can release WAL at checkpoint at the cost of replication continuation | `H/P` | `c6550776...` + v13 docs | supported |
| `unreserved` means protection is gone before required files are necessarily removed; `lost` means required WAL has been removed and slot is unusable | `H/P` | `b8fd4e02...` + v13 docs | supported |
| a small retained frontier can govern a much larger historical corpus | `E` | source mechanism | bounded inference |
| local current-state sufficiency does not imply downstream replay-history dispensability | `E` | mechanism + docs | bounded inference |
| `slot survives != required WAL survives != consumer can continue` under the v13 cap | `E` | v13 state machine | supported reconstruction |
| slot invalidation/WAL removal is not secure sanitization | `E/X` | interface/filesystem scope | explicit stop condition |
| Raft/Bigtable/LevelDB comparisons are functional only | `A/X` | grounded Cases 58/57/137 | bounded comparison |
