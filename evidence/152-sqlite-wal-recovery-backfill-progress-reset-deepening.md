# Evidence 152B — SQLite 3.7.0 WAL Recovery: Reconstructible Index, Disposable Backfill Progress, and Restart-Conservative Replay

Status: bounded deepening complete

Research date: 2026-09-17

Canonical case: [`../cases/152-sqlite-wal-checkpoint-backfill-reader-retention.md`](../cases/152-sqlite-wal-checkpoint-backfill-reader-retention.md)

Prior grounding: [`152-sqlite-2010-wal-checkpoint-retention-grounding.md`](152-sqlite-2010-wal-checkpoint-retention-grounding.md)

## 0. Bounded Research Question

The existing Case 152 already establishes that SQLite 3.7.0 WAL mode separates transaction commit, checkpoint/backfill, reader retirement, and WAL reuse, and that the wal-index is transient.

This slice asks a narrower restart question:

> If a process or machine fails after some WAL frames have already been copied into the main database, does SQLite need to retain the exact checkpoint-progress coordinate across the failure in order to recover correctly?

The 3.7.0 source gives an unusually direct answer. The checkpoint-progress field `nBackfill` lives in the transient wal-index. Recovery reconstructs the wal-index from the WAL, but deliberately initializes `nBackfill` to zero. In other words, recovery reconstructs the committed WAL geometry while declining to preserve or infer how much of an earlier checkpoint had already reached the database.

The bounded retention result is:

```text
retained committed WAL evidence
    != retained checkpoint progress

loss of checkpoint-progress metadata
    != loss of committed transaction history

restart recovery
    can conservatively forget prior backfill progress
    when the retained WAL is sufficient to replay the copying work
```

This is a source-level claim about SQLite 3.7.0's WAL algorithm and its documented recovery contract. It is not a universal database rule.

---

## 1. Source Register

### S152B.1 — SQLite 3.7.0 release record

- **Source:** SQLite, `Release 3.7.0 On 2010-07-21`.
- **URL:** https://sqlite.org/releaselog/3_7_0.html
- **Class:** first-party historical release record.
- **Supports:** public release boundary for WAL mode.
- **Does not support:** invention of write-ahead logging; exact internal recovery behavior by itself.

### S152B.2 — Frozen SQLite 3.7.0 `src/wal.c`: WAL and wal-index design comments

- **Source:** SQLite official GitHub mirror, tag `version-3.7.0`, `src/wal.c`.
- **URL:** https://github.com/sqlite/sqlite/blob/version-3.7.0/src/wal.c
- **Class:** frozen first-party implementation source.
- **Supports:**
  - WAL frames hold revised database pages;
  - commit is represented by a commit frame;
  - checkpoint copies WAL content into the database;
  - WAL is synchronized before checkpoint writes are issued to the database;
  - the database is synchronized before completed WAL content may be retired/reset;
  - wal-index is transient and reconstructible from the WAL.
- **Does not support:** lower-layer guarantees beyond the VFS contract or every later SQLite version.

### S152B.3 — Frozen SQLite 3.7.0 `WalCkptInfo` and `walCheckpoint()`

- **Source:** same frozen `src/wal.c`.
- **Class:** frozen first-party implementation source.
- **Supports:**
  - `nBackfill` records how many WAL frames have been copied into the database;
  - active reader marks can limit `mxSafeFrame`;
  - checkpoint starts from the current `nBackfill` and copies eligible frames after it;
  - `nBackfill` is advanced only after the checkpoint's copying work succeeds;
  - when the entire WAL is copied, the database is synchronized before the progress state is advanced to the complete frontier;
  - a writer may reset/reuse the WAL only when full backfill and reader conditions are satisfied.
- **Does not support:** secure deletion or a claim that `nBackfill` is itself durable.

### S152B.4 — Frozen SQLite 3.7.0 `walIndexRecover()`

- **Source:** same frozen `src/wal.c`.
- **Class:** frozen first-party implementation source.
- **Supports:**
  - recovery scans the WAL and validates frames;
  - `mxFrame` is reconstructed from the last valid commit frame;
  - after rebuilding the wal-index header, recovery sets `pInfo->nBackfill = 0`;
  - recovery also reinitializes reader marks rather than attempting to preserve pre-crash reader ownership.
- **Strength:** very high for the bounded 3.7.0 restart behavior.

### S152B.5 — Maintained SQLite WAL-mode file-format documentation

- **Source:** SQLite, `WAL-mode File Format`.
- **URL:** https://sqlite.org/walformat.html
- **Class:** maintained first-party technical documentation.
- **Supports:**
  - the `-shm` wal-index does not contain database content and is not required for crash recovery;
  - the wal-index is not fsync-ed as durable database state;
  - recovery rebuilds the wal-index from a scan of the WAL;
  - recovery sets `mxFrame` to the last valid commit frame;
  - because recovery cannot know how many WAL frames might already have been copied into the database, it initializes `nBackfill` to zero.
- **Temporal caution:** maintained documentation is a later explanatory witness; frozen 3.7.0 source remains primary for claims about the initial implementation.

### S152B.6 — Maintained SQLite WAL overview

- **Source:** SQLite, `Write-Ahead Logging`.
- **URL:** https://sqlite.org/wal.html
- **Class:** maintained first-party technical documentation.
- **Supports:**
  - checkpoint may stop at reader boundaries and resume later;
  - checkpoint remembers progress in the wal-index during live operation;
  - the WAL is part of persistent database state while relevant;
  - WAL must be synchronized before moving content into the database, and the database must be synchronized before resetting the WAL.
- **Temporal caution:** later checkpoint APIs/defaults are not projected backward into 3.7.0 without separate evidence.

---

## 2. Historical / Implementation Record

### 2.1 WAL mode publicly enters SQLite at 3.7.0

SQLite's release record dates 3.7.0 to **2010-07-21** and states that the release added write-ahead logging.

This is only the SQLite release boundary. The broader write-ahead-logging history predates SQLite, as already bounded in the canonical Case 152 and its ARIES prior-art guardrail.

No novelty claim is made here.

### 2.2 The 3.7.0 wal-index is explicitly transient

The frozen `version-3.7.0/src/wal.c` design comments say that the wal-index is transient and, after a crash, can and should be reconstructed from the original WAL file. The comments also explain why the wal-index may use native byte order rather than a cross-platform on-disk representation: it is not the retained cross-platform database record.

That makes the first separation explicit:

```text
WAL frame/commit evidence
    != wal-index acceleration and coordination state
```

The wal-index is operationally important while SQLite is running, but its required lifetime is shorter than the lifetime of committed WAL content.

### 2.3 `nBackfill` is a live checkpoint-progress coordinate

`WalCkptInfo` stores `nBackfill`, defined in the 3.7.0 source as the number of WAL frames that have been written back into the database.

The same structure stores reader marks that constrain how far a checkpoint may safely proceed while readers retain older snapshots.

Thus, during a live process:

```text
mxFrame
    = committed WAL frontier visible to the current wal-index generation

nBackfill
    = checkpoint-copy frontier

aReadMark[]
    = live reader constraints on safe checkpoint progress
```

These fields answer different questions. None should be collapsed into a generic `WAL progress` scalar.

### 2.4 `walCheckpoint()` treats the WAL as the retained replay source

The frozen 3.7.0 checkpoint implementation first computes a reader-safe maximum frame. If there is work beyond `nBackfill`, it synchronizes the WAL before copying page images from WAL frames into the main database.

The source comment explains the retention rationale directly: the WAL is synchronized first so that the new content remains recoverable following power loss or a hard reset while checkpoint writes are being made to the database.

This yields the relevant ordering:

```text
retain/synchronize WAL evidence
    -> copy eligible page images into main database
    -> if all current WAL content is copied, synchronize database
    -> advance live backfill frontier
    -> only later, under additional reader conditions, permit WAL reset/reuse
```

The checkpoint progress coordinate therefore does not carry the committed data by itself. It records how much copying work the current execution believes has safely advanced.

### 2.5 Recovery reconstructs committed geometry but zeros prior backfill progress

The decisive 3.7.0 evidence is `walIndexRecover()`.

Recovery:

1. obtains the relevant exclusive locks;
2. reads and validates the WAL header;
3. scans WAL frames from the beginning;
4. validates frame checksum/salt relations;
5. rebuilds wal-index page mappings;
6. records `mxFrame` at the last valid commit frame;
7. writes the reconstructed wal-index header;
8. resets the checkpoint-information area;
9. explicitly sets `nBackfill = 0`;
10. resets reader marks to their restart baseline.

The implementation does **not** inspect the main database and attempt to infer an exact pre-crash checkpoint frontier.

That is the bounded historical fact around which this slice is organized.

### 2.6 Maintained documentation states the reason explicitly

The maintained `walformat.html` recovery section explains the same rule in direct prose: recovery has no way to know how many frames might previously have been copied back into the database, so it initializes `nBackfill` to zero.

This later documentation is valuable because it makes explicit the rationale visible in the 2010 source structure.

It should not be used to smuggle later APIs or later implementation details into the 3.7.0 baseline.

---

## 3. Engineering Reconstruction

Everything in this section is a reconstruction of the source-level state machine, not historical SQLite vocabulary unless quoted as an identifier.

### 3.1 Restart-conservative progress reset

A useful repository term for the observed pattern is **restart-conservative progress reset**:

> When recovery cannot prove how much non-authoritative maintenance work was durably completed, it discards the old progress coordinate and restarts from a conservative lower bound while retaining the authoritative source from which the work can be repeated.

For SQLite 3.7.0 WAL checkpointing:

```text
retained authority/source:
    valid committed WAL frames

reconstructible derived state:
    wal-index mapping + mxFrame

discarded live progress:
    prior nBackfill

restart baseline:
    nBackfill = 0

recovery consequence:
    checkpoint work may be repeated
```

This term is an analytical label introduced by this repository. It is not a phrase attributed to SQLite developers.

### 3.2 Checkpoint progress can be less durable than the state it protects

This is the central asymmetry:

```text
committed WAL history must remain recoverable
    while relevant

checkpoint progress may be forgotten
    and safely recomputed/replayed
```

The relation is possible because the copied-to-database page is not the sole remaining embodiment while the WAL remains live. A valid WAL frame still carries the revised page image needed to repeat the copy.

Therefore:

> **maintenance-progress persistence != payload/currentness persistence.**

And:

> **checkpoint-progress loss != transaction rollback.**

### 3.3 A partial checkpoint creates replayable uncertainty, not a new transaction state

Suppose a checkpoint has copied some pages to the database but not all of them.

The main database may then contain a mixture of pages that have and have not been refreshed from the WAL. That mixture does not redefine which transaction committed. Commit validity remains determined by the valid committed WAL sequence.

If a crash destroys the wal-index progress information, recovery reconstructs the committed WAL frontier and sets `nBackfill` to zero. A later checkpoint may therefore rewrite database pages that had already been copied before the crash.

So:

```text
physical copy may already have happened
    +
progress proof is gone
    -> repeat copy conservatively
```

This is different from saying that SQLite rolls the database back to frame zero. The progress coordinate is reset; committed state is not thereby forgotten.

### 3.4 Full copy followed by progress loss is still not equivalent to lost commit history

A second boundary is even more useful.

Imagine that the database pages have all been copied and the database synchronization has completed, but a crash occurs before the WAL is reset/reused. The transient wal-index disappears. On recovery, `nBackfill` is again initialized to zero even though the main database may already contain the complete checkpointed image.

The retained WAL lets a later checkpoint conservatively repeat work.

Thus:

> **bitwise survival of maintenance progress is not required when the system retains enough authoritative evidence to replay the maintenance action safely.**

This is not a claim that replay is free. It can create redundant I/O. It is a claim about correctness/recoverability boundaries, not efficiency.

### 3.5 Reuse authority remains stricter than replayability

Discarding `nBackfill` does not grant permission to reuse the WAL.

In the 3.7.0 state machine, reuse/reset requires the live system to establish the relevant complete-backfill condition and the absence of readers that still depend on the WAL.

So the direction is:

```text
replayable checkpoint work
    != full backfill proven now
    != WAL reuse authority
```

A restart that forgets progress moves the system conservatively away from reuse authority until it proves the needed relation again.

---

## 4. Failure-Window Matrix

The following table is an engineering reconstruction bounded by the 3.7.0 ordering and recovery code.

| Failure window | What may already have happened | What survives as authoritative evidence | Recovery treatment | Safe claim |
|---|---|---|---|---|
| before checkpoint starts copying | committed WAL exists; database still old for some pages | WAL commit/frame sequence | rebuild wal-index; `nBackfill=0` | no checkpoint progress is required |
| after WAL sync, during partial database copying | some database pages may contain copied WAL content | synchronized WAL remains replay source | rebuild wal-index; forget old progress; later checkpoint may recopy | partial copy != durable progress obligation |
| after some copies complete but before live `nBackfill` advances | physical work exceeds recorded progress | WAL | restart from zero | duplicate work is preferable to trusting unproven progress |
| after live `nBackfill` advances, before crash | process knew a later copy frontier | WAL; wal-index progress need not survive | reconstructed `nBackfill=0` | live progress coordinate != restart-persistent state |
| after complete copy + database sync, before WAL reset | main database may already embody all current WAL content; WAL still exists | database + still-valid WAL | rebuild wal-index; `nBackfill=0`; re-establish completion before reuse | completed physical work != retained proof of maintenance progress |
| after legal WAL reset/reuse begins | earlier generation has already crossed stronger reuse conditions | current WAL generation rules/salts determine validity | outside this slice's detailed fault matrix | do not infer secure deletion from logical reuse |

This table intentionally uses `may` for post-crash physical-media outcomes. SQLite's VFS ordering is the level of evidence available here; exact drive/controller persistence is not inferred.

---

## 5. Retention-State Decomposition

Case 152 can now distinguish at least six state classes.

### 5.1 Committed payload evidence

- revised page images in valid WAL frames;
- commit-frame relation;
- required while those WAL transactions remain part of current persistent database state.

### 5.2 WAL-generation validity evidence

- header/frame salts, counters, and checksums;
- distinguishes current valid frames from leftovers of older reuse generations.

### 5.3 Reconstructed committed frontier

- `mxFrame` in the wal-index;
- rebuilt from the last valid commit frame during recovery.

### 5.4 Live checkpoint progress

- `nBackfill`;
- records how far the current wal-index generation believes copying has safely advanced;
- deliberately reset to zero during recovery.

### 5.5 Live reader relations

- reader locks and `aReadMark[]`;
- constrain checkpoint/reuse while those live readers exist;
- not treated as cross-crash reader identities.

### 5.6 Reuse authority

- not a single stored bit;
- derived from current backfill and reader conditions before the writer resets/reuses the WAL.

The decomposition prevents this collapse:

```text
all state relevant to recovery
    == all state that must itself persist
```

That equality is false in this bounded case.

---

## 6. Cross-Case Comparison

### 6.1 Case 42 — Kafka cleaner checkpoint: retained progress can itself become stale

Case 42 records a very different maintenance choice. Kafka's cleaner offset checkpoint externalizes a progress frontier across restart. Later log-geometry changes can make that retained scalar stale or semantically invalid, which requires explicit currentness repair.

SQLite Case 152 provides the opposite bounded pattern:

```text
Kafka cleaner:
    persist maintenance progress
    -> later verify that the retained coordinate still fits current log geometry

SQLite WAL checkpoint:
    do not rely on old backfill progress across crash
    -> reconstruct WAL geometry
    -> reset backfill progress to conservative zero
```

Safe functional conclusion:

> A maintenance system may preserve progress across restart, or may intentionally discard it and replay work, depending on what authoritative source remains and what restart proof is cheaper/safer.

No Kafka -> SQLite or SQLite -> Kafka genealogy is asserted.

### 6.2 Synthesis 29 — persistence of meaning is not the only safe strategy

Synthesis 29 distinguishes bitwise persistence, semantic persistence, exact progress persistence, and restart authority.

Case 152 adds a bounded counterpoint: sometimes the safe restart contract is **not to preserve the progress coordinate at all**. Instead, the system preserves authoritative source evidence and reconstructs a conservative runtime state.

This is a functional extension of the repository comparison framework, not historical evidence that SQLite developers used that vocabulary.

### 6.3 Case 143 — rollback journal remains a direct SQLite-internal contrast

Case 143 retains older page images for rollback-oriented recovery. Case 152 retains newer committed WAL page images and can replay checkpoint copying.

Both demonstrate that a small runtime bookkeeping structure is not necessarily the durable recovery payload, but their direction of recovery is different.

Do not collapse:

```text
rollback undo
    == WAL checkpoint replay
```

---

## 7. Historical Record vs Engineering Reconstruction vs Functional Analogy vs Interpretation

### Historical / implementation record

Directly supported by frozen or maintained SQLite first-party sources:

- SQLite 3.7.0 publicly added WAL on 2010-07-21;
- the 3.7.0 wal-index is transient and reconstructible from the WAL;
- `nBackfill` records checkpoint-copy progress;
- checkpoint synchronizes the WAL before copying from it into the database;
- `walIndexRecover()` reconstructs valid WAL geometry and sets `nBackfill` to zero;
- reader marks are reinitialized during recovery;
- WAL reset/reuse is gated by stronger live conditions than merely having copied one or more pages.

### Engineering reconstruction

Repository-level deductions from the implementation ordering:

- pre-crash checkpoint progress can be safely forgotten because the retained WAL allows conservative replay;
- physical checkpoint work may have happened even when restart no longer retains proof of that progress;
- recovery chooses a conservative lower bound rather than trying to infer exact copied-page history;
- loss of progress can trade extra work for simpler restart correctness.

### Functional analogy

Allowed comparisons:

- Kafka Case 42 for persistent-versus-discardable maintenance progress;
- Synthesis 29 for persistence dimensions;
- Case 143 for the same project's alternate journal direction.

These comparisons do not establish shared lineage.

### Philosophical interpretation

Interpretation only:

> Retention can be selective. A system may preserve the evidence needed to recover a valid state while allowing its record of already-performed maintenance effort to disappear.

That is a conceptual reading of the technical case. It is not SQLite's historical terminology and should not be generalized into claims about memory or society.

---

## 8. Explicit Non-Claims

1. This evidence does **not** claim SQLite invented write-ahead logging.
2. It does **not** claim the wal-index is useless; it is essential live coordination/acceleration state.
3. It does **not** claim `nBackfill=0` means the main database has been physically reverted.
4. It does **not** claim a crash erases database pages that had already been checkpointed.
5. It does **not** claim partial checkpoint rolls back committed transactions.
6. It does **not** claim checkpoint replay is transaction replay.
7. It does **not** claim checkpoint replay has zero performance cost.
8. It does **not** claim all VFS implementations use a disk-backed `-shm` file; SQLite may use shared memory or heap-backed substitutes depending on mode/VFS.
9. It does **not** claim the wal-index is part of the portable persistent database format.
10. It does **not** claim exact filesystem, SSD, controller, or power-failure behavior below SQLite's VFS ordering.
11. It does **not** claim every later SQLite release has byte-for-byte identical recovery code.
12. It does **not** project later checkpoint modes or later auto-checkpoint defaults into 3.7.0.
13. It does **not** claim WAL reset/reuse securely sanitizes older media embodiments.
14. It does **not** claim every frame physically present in a WAL is valid or committed.
15. It does **not** claim a reconstructed `mxFrame` by itself grants WAL reuse authority.
16. It does **not** claim old reader identities survive a process/machine crash and must be reconstructed as the same live locks.
17. It does **not** claim recovery can tolerate arbitrary WAL corruption beyond the validity rules checked by SQLite.
18. It does **not** claim the maintained 2025-era documentation is a frozen copy of the 2010 manual.
19. It does **not** claim Kafka cleaner checkpoints and SQLite `nBackfill` descend from a common maintenance-checkpoint design.
20. It does **not** claim that discarding progress is universally preferable to persisting progress.

---

## 9. Claim Ledger

| Claim | Classification | Evidence | Confidence |
|---|---|---|---|
| SQLite 3.7.0 added WAL on 2010-07-21 | historical record | S152B.1 | high |
| 3.7.0 wal-index is transient/reconstructible from WAL | implementation record | S152B.2 | high |
| `nBackfill` records WAL-to-database copy progress | implementation record | S152B.3 | high |
| live readers may limit the safe backfill frontier | implementation record | S152B.3 | high |
| 3.7.0 checkpoint synchronizes WAL before copying WAL content to DB | implementation record | S152B.2, S152B.3 | high |
| `walIndexRecover()` reconstructs WAL geometry and then sets `nBackfill=0` | implementation record | S152B.4 | high |
| maintained SQLite docs explicitly explain that recovery cannot know prior backfill extent and initializes it to zero | maintained technical record | S152B.5 | high |
| exact checkpoint progress need not persist for this recovery design to preserve committed history | engineering reconstruction | S152B.2-S152B.5 | high within bounded model |
| a restart may repeat previously completed page-copy work | engineering reconstruction | S152B.3-S152B.5 | high |
| progress loss is equivalent to transaction loss | rejected claim | source separation above | high-confidence rejection |
| WAL reset is secure deletion | rejected claim | no supporting evidence | high-confidence rejection |
| SQLite's choice is a universal database principle | philosophical/general claim | not established | rejected |

---

## 10. Why This Deepens Rather Than Repeats the Existing Grounding

The first Case 152 evidence already said:

```text
wal-index is transient
    and
nBackfill records checkpoint progress
```

This slice adds the missing restart consequence by following the actual 3.7.0 recovery and checkpoint functions together:

```text
checkpoint may have copied real pages
    -> crash loses transient wal-index
    -> recovery scans authoritative WAL
    -> recovery reconstructs committed mxFrame
    -> recovery explicitly sets nBackfill = 0
    -> later checkpoint may conservatively repeat copying
```

The new contribution is therefore not another description of WAL mode. It is the evidence-backed distinction between:

- **durable/current transaction evidence**;
- **reconstructed current WAL geometry**;
- **discardable maintenance-progress evidence**;
- **re-established reuse authority**.

---

## 11. Related-Repository Boundary

A fresh search of `tmzncty/computing-archaeology` for `SQLite` found no dedicated SQLite WAL/checkpoint packet to reuse.

`technical-retention` keeps only the retention-specific seam:

> **authoritative WAL survives while exact checkpoint progress may be discarded and conservatively replayed after restart.**

A broader history of database recovery, System R/ARIES, SQLite pager development, the Fossil check-in genealogy of WAL, VFS history, and the evolution of later checkpoint modes belongs in `computing-archaeology` rather than being duplicated here.

---

## 12. Remaining Evidence Debt

1. Recover the pre-release SQLite Fossil check-in genealogy that led to the 3.7.0 recovery rule.
2. Find or construct a frozen-3.7.0 fault-injection harness that crashes at controlled points inside `walCheckpoint()` and confirms the replay matrix experimentally.
3. Separate process crash, OS crash, and sudden-power-loss experiments at the VFS boundary.
4. Trace whether and when later SQLite versions changed recovery/checkpoint bookkeeping while retaining the same high-level transient-wal-index contract.
5. Trace later PASSIVE/FULL/RESTART/TRUNCATE checkpoint-mode chronology separately rather than projecting it backward.
6. Measure redundant checkpoint write cost after progress loss only if performance archaeology becomes useful; it is not needed for the retention claim.
7. Keep lower-layer filesystem/SSD durability and sanitization questions in their own evidence chains.

---

## 13. Sources

1. SQLite, **Release 3.7.0 On 2010-07-21**: https://sqlite.org/releaselog/3_7_0.html
2. SQLite source, frozen `version-3.7.0`, **`src/wal.c`**: https://github.com/sqlite/sqlite/blob/version-3.7.0/src/wal.c
3. SQLite, **WAL-mode File Format**: https://sqlite.org/walformat.html
4. SQLite, **Write-Ahead Logging**: https://sqlite.org/wal.html
5. Existing Case 152 evidence: [`152-sqlite-2010-wal-checkpoint-retention-grounding.md`](152-sqlite-2010-wal-checkpoint-retention-grounding.md)
6. Canonical Case 152: [`../cases/152-sqlite-wal-checkpoint-backfill-reader-retention.md`](../cases/152-sqlite-wal-checkpoint-backfill-reader-retention.md)
7. Case 42 — Kafka cleaner checkpoint: [`../cases/42-kafka-log-compaction-tombstone-window.md`](../cases/42-kafka-log-compaction-tombstone-window.md)
8. Synthesis 29 — Semantic Persistence and Restart Continuation: [`../docs/SYNTHESIS_29_SEMANTIC_PERSISTENCE_AND_RESTART_CONTINUATION.md`](../docs/SYNTHESIS_29_SEMANTIC_PERSISTENCE_AND_RESTART_CONTINUATION.md)
9. Case 143 — SQLite rollback journal: [`../cases/143-sqlite3-rollback-journal-hot-recovery-authority.md`](../cases/143-sqlite3-rollback-journal-hot-recovery-authority.md)
