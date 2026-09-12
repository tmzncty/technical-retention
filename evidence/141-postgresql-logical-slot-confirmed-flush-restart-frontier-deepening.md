# Evidence 141B — PostgreSQL logical-slot confirmed-flush vs WAL-restart frontier

**Status:** grounded
**Case:** [`../cases/141-postgresql-replication-slot-wal-retention-frontier.md`](../cases/141-postgresql-replication-slot-wal-retention-frontier.md)
**Bounded question:** in the PostgreSQL 9.4 logical-slot implementation, does a consumer's acknowledged logical-decoding position coincide with the oldest WAL position the server may reclaim, or are these distinct retained frontiers with different advancement rules?

## Evidence boundary

This record narrows one open item in Case 141: **logical-slot advancement semantics**. It does not attempt a general history of logical decoding, physical replication, feedback protocols, WAL recycling, output plugins, or PostgreSQL replication slots.

The bounded claim uses PostgreSQL project-primary sources: released `REL9_4_0` source, PostgreSQL 9.4/9.5 documentation, and the 10-August-2015 commit that exposed `confirmed_flush_lsn` in `pg_replication_slots`.

The result is:

```text
consumer-confirmed logical position (`confirmed_flush` / later `confirmed_flush_lsn`)
    != oldest WAL still required for decoding (`restart_lsn`)
    != completed WAL removal
    != media sanitization
```

## Source ladder

| Source | Date / version | Evidence class | Use here |
|---|---:|---|---|
| PostgreSQL `REL9_4_0` `src/include/replication/slot.h` | PostgreSQL 9.4.0 release tree, 2014 | `H/P` | persistent `restart_lsn` and `confirmed_flush`; candidate restart state |
| PostgreSQL `REL9_4_0` `src/backend/replication/logical/logical.c` | PostgreSQL 9.4.0 release tree, 2014 | `H/P` | consumer-confirmation update path; candidate-gated `restart_lsn` advancement |
| PostgreSQL 9.4 `pg_replication_slots` documentation | 9.4 release series | `H/P` | user-visible view exposes `restart_lsn` but not `confirmed_flush_lsn` |
| PostgreSQL commit `3f811c2d6f51b13b71adff99e82894dd48cee055` | 2015-08-10 | `H/P` | explicitly distinguishes the two positions and exposes `confirmed_flush_lsn` |
| PostgreSQL 9.5 `pg_replication_slots` documentation | 9.5 release series | `H/P` | released definitions of both fields; `confirmed_flush_lsn` is logical-slot-only |

These sources ground implementation and interface semantics. They do not independently measure production lag, disk pressure, crash behavior, or lower-storage persistence compliance.

## Historical record

### 1. PostgreSQL 9.4 already persists two different logical-slot positions

In `REL9_4_0`, `ReplicationSlotPersistentData` is explicitly the on-disk data of a replication slot preserved across restarts. It contains both:

- `restart_lsn`, described as the oldest LSN that might be required by the slot;
- `confirmed_flush`, tied to client acknowledgement of receipt.

The same header keeps `candidate_restart_valid` and `candidate_restart_lsn` as logical-slot working state, and explains that `restart_lsn` can be increased only after the corresponding candidate is valid relative to client-confirmed progress.

**Anchor:** <https://github.com/postgres/postgres/blob/REL9_4_0/src/include/replication/slot.h>

This is direct historical evidence that the released 9.4 implementation did not model logical consumer progress and WAL restart need as one scalar state.

### 2. Consumer confirmation directly advances `confirmed_flush`

The released 9.4 `LogicalConfirmReceivedLocation()` path handles a consumer's confirmation that it has received changes through an LSN. The function assigns that LSN to `slot->data.confirmed_flush`.

**Anchor:** <https://github.com/postgres/postgres/blob/REL9_4_0/src/backend/replication/logical/logical.c>

Therefore:

`consumer confirmation event -> confirmed_flush advancement`

This does not imply an equal `restart_lsn` update.

### 3. `restart_lsn` advancement is candidate-gated

In the same function, `restart_lsn` advances only when `candidate_restart_valid` exists and that validity position has been reached by the newly confirmed LSN. The code then installs `candidate_restart_lsn` and clears the candidate fields.

The neighboring source comment describes the restart candidate as the minimal LSN needed to replay transactions that had not yet committed at the candidate's `current_lsn`, and says that the change takes effect only once the client confirms receipt through that point.

The released implementation therefore has this bounded relation:

```text
consumer acknowledges farther progress
    -> `confirmed_flush` advances
    -> if a prepared restart candidate is now valid
         `restart_lsn` may advance to that candidate
       else
         `restart_lsn` need not move yet
```

The different update conditions are stronger evidence than the mere presence of two differently named fields.

### 4. Logical progress can be ahead of the WAL-restart frontier

The mechanism explains why a logical slot can retain a `restart_lsn` older than its consumer-confirmed position. The decoder can still require WAL from before the consumer's acknowledged frontier to reconstruct or resume decoding correctly.

The bounded engineering reconstruction is:

`consumer no longer needs logical output before X != decoder no longer needs any WAL before X`

This concerns logical decoding, not every PostgreSQL recovery or archival use of WAL.

### 5. PostgreSQL 9.4 persisted the second frontier before exposing it in the system view

PostgreSQL 9.4's documented `pg_replication_slots` view lists `restart_lsn` but no `confirmed_flush_lsn` column, even though the 9.4 release source already persists `confirmed_flush`.

**Anchor:** <https://www.postgresql.org/docs/9.4/catalog-pg-replication-slots.html>

Thus:

`persistent internal control state != operator-visible system-view telemetry`

The absence of a view column is not evidence that the underlying state did not exist.

### 6. The 2015 PostgreSQL commit explicitly names the distinction

Commit `3f811c2d6f51b13b71adff99e82894dd48cee055`, committed **10 August 2015**, adds `confirmed_flush_lsn` to `pg_replication_slots`.

Its project commit message says `restart_lsn` and `confirmed_flush` have **rather distinct meanings**. It characterizes `restart_lsn` as the oldest WAL still required, valid for physical and logical slots, while `confirmed_flush` is the location through which a logical slot's consumer has confirmed receiving data. It also notes that a slot commonly requires older WAL at `restart_lsn` than the confirmed position.

**Project archive:** <https://www.postgresql.org/message-id/E1ZOlGa-0001pQ-JL%40gemulon.postgresql.org>

This is direct project-history evidence for the distinction rather than later repository terminology.

### 7. PostgreSQL 9.5 makes both positions operator-visible

The PostgreSQL 9.5 `pg_replication_slots` documentation exposes both:

- `restart_lsn`: oldest WAL still possibly required by the consumer and therefore protected from ordinary checkpoint removal;
- `confirmed_flush_lsn`: the position through which a logical slot's consumer has confirmed receiving data; it is `NULL` for physical slots.

**Anchor:** <https://www.postgresql.org/docs/9.5/view-pg-replication-slots.html>

The released interface therefore gives operators two separate progress/retention coordinates rather than one generic replication offset.

## Engineering reconstruction

### A. Consumer acknowledgement is an input to reclamation eligibility, not identical to it

The 9.4 update path allows acknowledged progress to make a prepared restart candidate eligible. It does not calculate WAL reclaimability by simply assigning `restart_lsn = confirmed_flush`.

Therefore:

`acknowledgement frontier != WAL-restart/reclamation frontier`

and:

`confirmed_flush advanced != all earlier WAL immediately reclaimable`

### B. One retained history can have multiple permission frontiers

For logical decoding, one retained position records what the consumer has confirmed receiving while another records how far back decoding may still need raw WAL:

```text
confirmed_flush:
  how far has consumer receipt been acknowledged?

restart_lsn:
  how far back can WAL still be needed to resume decoding correctly?
```

`acknowledgement frontier` and `reclamation frontier` are project reconstruction terms. PostgreSQL's historical vocabulary remains `confirmed_flush` / `confirmed_flush_lsn` and `restart_lsn`.

### C. Interface visibility has its own chronology

The underlying `confirmed_flush` state exists in 9.4 release source while the system-view column arrives in 2015 for the next release line.

So:

`state introduction != telemetry exposure date`

The 2015 commit must not be misread as the invention or first implementation of the underlying state.

## Functional comparison — bounded

Other repository log cases also separate progress evidence from a history-liveness boundary. That is only a structural analogy. PostgreSQL logical decoding is not Kafka high-watermark semantics, Raft snapshot compaction, LevelDB obsolete-file liveness, or any other log-maintenance mechanism, and no code lineage is claimed.

## Philosophical interpretation — bounded

Project interpretation only: a system can know that a consumer has already received a later point while still being unable to forget all earlier physical history. Receipt/acknowledgement and permission to discard are different relations.

This is not PostgreSQL historical vocabulary and does not equate database log retention with human memory, testimony, or archival ethics.

## Counterexamples and stop conditions

- **`confirmed_flush_lsn != restart_lsn`.** Project source and documentation give them different meanings and advancement conditions.
- **Consumer acknowledgement != WAL deletion.** Confirmation can enable a restart candidate; it is not itself a checkpoint/removal event.
- **Logical output no longer needed before the confirmed position != raw WAL physically absent.** The slot can still require older WAL through `restart_lsn`.
- **`confirmed_flush_lsn` != universal physical-slot progress metric.** The documented column is `NULL` for physical slots.
- **View exposure in 2015 != underlying-state invention in 2015.** `confirmed_flush` is already persisted in the 9.4 release source.
- **Frontier advancement != sanitization.** Neither position proves byte erasure from filesystem, device, archive, backup, or forensic embodiments.
- **9.4 source semantics != all later-version implementation details.** Later evolution must be checked before importing exact candidate/update behavior.
- **Project analogy != protocol identity.** No Kafka/Raft/LSM mechanism identity or genealogy follows.

## Related repository boundary

`tmzncty/computing-archaeology` was rechecked during this slice for `PostgreSQL replication slot`, `confirmed_flush_lsn`, and `restart_lsn`; no dedicated overlapping module was found.

Broader logical-decoding / replication-slot proposal history, physical-slot protocol genealogy, and release-by-release source archaeology belong there if developed. This record keeps only the retention-specific distinction needed by `technical-retention`.

## Remaining uncertainty

This slice closes the broad **logical-slot dual-frontier** question for the 9.4/9.5 baseline. It does not close:

1. exact physical-slot advancement and feedback semantics across releases;
2. pre-9.4 proposal/review genealogy for `confirmed_flush` and candidate restart logic;
3. later changes to candidate-restart generation/advancement and long-transaction behavior;
4. interaction with archiving, base backups, slot copy/migration, and reinitialization;
5. production measurements of `confirmed_flush_lsn - restart_lsn` divergence;
6. controlled fault injection around slot-state persistence, WAL recycling, and restart.

## Claim ledger

| Claim | Type | Strength |
|---|---|---|
| `REL9_4_0` persistent slot data contains separate `restart_lsn` and `confirmed_flush` fields | `H/P` | strong |
| 9.4 `LogicalConfirmReceivedLocation()` directly advances `confirmed_flush` | `H/P` | strong |
| 9.4 `restart_lsn` advances only when a valid candidate is crossed by confirmed progress | `H/P` | strong |
| consumer acknowledgement frontier is not identical to WAL-restart/reclamation frontier | `E` | strong, source-grounded |
| 9.4 system view exposes `restart_lsn` while the internal persistent `confirmed_flush` is not yet exposed there | `H/P, E` | strong |
| 2015 commit explicitly states that the two fields have distinct meanings and normally can differ | `H/P` | strong |
| 9.5 exposes `confirmed_flush_lsn` for logical slots and retains separate `restart_lsn` | `H/P` | strong |
| persistent internal state can predate its operator-visible telemetry surface | `E` | strong for this bounded instance |
| analogous progress/history-liveness splits in other systems imply shared mechanism or genealogy | `A, X` | rejected upgrade |
| either frontier proves secure erasure of older bytes | `X` | rejected |

## Source links

- PostgreSQL `REL9_4_0` `slot.h`: <https://github.com/postgres/postgres/blob/REL9_4_0/src/include/replication/slot.h>
- PostgreSQL `REL9_4_0` `logical.c`: <https://github.com/postgres/postgres/blob/REL9_4_0/src/backend/replication/logical/logical.c>
- PostgreSQL 9.4 `pg_replication_slots`: <https://www.postgresql.org/docs/9.4/catalog-pg-replication-slots.html>
- PostgreSQL 2015 commit archive: <https://www.postgresql.org/message-id/E1ZOlGa-0001pQ-JL%40gemulon.postgresql.org>
- PostgreSQL commit `3f811c2d...`: <https://git.postgresql.org/gitweb/?p=postgresql.git;a=commit;h=3f811c2d6f51b13b71adff99e82894dd48cee055>
- PostgreSQL 9.5 `pg_replication_slots`: <https://www.postgresql.org/docs/9.5/view-pg-replication-slots.html>
