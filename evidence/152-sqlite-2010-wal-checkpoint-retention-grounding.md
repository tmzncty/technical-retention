# Evidence 152 — SQLite 3.7.0 WAL Checkpoint, Reader Marks, and Reuse Authority

Status: grounded evidence record

## Research Question

What evidence is sufficient to show that SQLite WAL can retain already-committed revised pages outside the main database file, that active readers can constrain checkpoint/reuse, and that the wal-index has a different durability horizon from the WAL itself?

## Evidence Classification

### E152.1 — SQLite 3.7.0 release boundary

- **Source:** SQLite first-party release record, `3.7.0`, dated 2010-07-21.
- **Class:** primary historical (`P/H`).
- **Claim supported:** SQLite 3.7.0 publicly added write-ahead logging.
- **Strength:** high for release chronology.
- **Stop condition:** not an invention date for WAL generally; not a complete implementation genealogy.

### E152.2 — Frozen 3.7.0 WAL format and reader comments

- **Source:** SQLite official GitHub mirror, tag `version-3.7.0`, `src/wal.c`.
- **Class:** frozen first-party source (`P`).
- **Claims supported:**
  - WAL frames hold revised page contents;
  - a transaction commits when a frame with a commit marker is written;
  - checkpoint transfers WAL content back to the database;
  - the WAL can later be reused;
  - frame salts/checksums/counters distinguish current frames from leftovers;
  - a reader fixes an `mxFrame` boundary and ignores later frames for a consistent snapshot;
  - wal-index is transient and reconstructible from the WAL.
- **Strength:** very high for the bounded 3.7.0 implementation semantics documented in source.
- **Stop condition:** comments are implementation documentation, not proof of every filesystem/device durability promise or every later SQLite version.

### E152.3 — Frozen 3.7.0 checkpoint coordination structure

- **Source:** same frozen `src/wal.c`, `WalCkptInfo` comments.
- **Class:** frozen first-party source (`P`).
- **Claims supported:**
  - `nBackfill` counts WAL frames copied back to the database;
  - reader marks bound safe checkpoint progress;
  - `nBackfill == mxFrame` means all current frames are backfilled;
  - the writer resets/reuses the WAL only when all content is backfilled and no readers are using the WAL.
- **Strength:** very high for 3.7.0 source-level relation.
- **Stop condition:** does not establish physical secure erasure, controller-level overwrite, or later checkpoint API chronology.

### E152.4 — Maintained SQLite WAL design documentation

- **Source:** SQLite first-party `wal.html`.
- **Class:** maintained primary technical (`P-current`).
- **Claims supported:**
  - rollback-journal and WAL directions differ;
  - commit can occur before main-database writeback;
  - readers use an end mark;
  - checkpoint may stop at a reader boundary and resume later;
  - the WAL file is part of persistent database state and must remain paired with the database while relevant.
- **Strength:** high for maintained design semantics and operational guidance.
- **Stop condition:** not a frozen facsimile of all 2010 details; later defaults/APIs must not be projected backward without separate chronology.

### E152.5 — ARIES prior-art guardrail

- **Source:** IBM Research publication page for Mohan et al., ARIES, ACM TODS, 1992.
- **Class:** high-quality primary scholarly historical (`S/H`).
- **Claim supported:** write-ahead logging was an established published transaction-recovery term/technique before SQLite 3.7.0.
- **Strength:** high for the anti-novelty guardrail.
- **Stop condition:** no direct ARIES -> SQLite genealogy established here; ARIES semantics are not equated with SQLite's WAL state machine.

## Claim Matrix

| Claim | Classification | Evidence | Confidence |
|---|---|---|---|
| SQLite 3.7.0 added WAL on 2010-07-21 | historical record | E152.1 | high |
| WAL frames in 3.7.0 store revised database-page contents | historical/technical record | E152.2 | high |
| a commit record can establish commit before checkpoint copies pages into the main database | technical record | E152.2, E152.4 | high |
| reader `mxFrame` / end mark stays fixed during a read transaction | technical record | E152.2, E152.4 | high |
| a live reader can constrain checkpoint progress | technical record | E152.3, E152.4 | high |
| `nBackfill == mxFrame` alone is insufficient for WAL reset if readers still use the WAL | technical record | E152.3 | high |
| wal-index is transient and reconstructible from WAL in 3.7.0 | technical record | E152.2 | high |
| WAL reset/reuse securely sanitizes earlier physical embodiments | rejected claim | no supporting evidence | high confidence rejection |
| SQLite invented write-ahead logging in 2010 | rejected historical claim | E152.5 | high confidence rejection |
| ARIES directly caused SQLite's implementation | genealogy claim | not established | unsupported |
| current SQLite checkpoint defaults existed unchanged in 3.7.0 | anachronistic implementation claim | not established | unsupported |

## Engineering Reconstruction Boundary

The strongest safe reconstruction is:

```text
base database contains older page
    -> writer appends revised page frame(s) to WAL
    -> commit marker makes transaction committed
    -> new reader records a current end mark / mxFrame
    -> old reader may retain an earlier cut
    -> checkpoint backfills frames that are safe relative to reader marks
    -> nBackfill eventually reaches mxFrame
    -> after no reader still uses the WAL, writer may reset/reuse it
```

This reconstruction does **not** say:

- that every committed page immediately exists in the base database;
- that every reader sees the latest commit;
- that wal-index state is a durable payload copy;
- that WAL reset physically sanitizes storage media;
- that all later SQLite WAL APIs/defaults existed in the initial 3.7.0 release.

## Retention Relations Extracted

1. **Commit relation:** valid frame sequence + commit marker establish a transaction boundary.
2. **Snapshot relation:** reader cut (`mxFrame` / end mark) determines which WAL prefix is visible.
3. **Backfill relation:** `nBackfill` records how much eligible WAL content has been copied to the database.
4. **Reuse relation:** full backfill plus absence of WAL-using readers permits reset/reuse.
5. **Generation-validity relation:** salts/checksums/counters distinguish current WAL frames from leftovers.
6. **Derived coordination relation:** wal-index accelerates reads and coordinates checkpoint/readers but is reconstructible from the persistent WAL.

These relations have different lifetimes and must not be collapsed into a single “journal exists” bit.

## Prior-Art and Anti-Anachronism Notes

1. **2010 is the SQLite WAL release boundary, not the invention date of WAL.**
2. **ARIES 1992 is only a prior-art guardrail here, not a genealogy claim.**
3. **Frozen 3.7.0 source has priority for 2010 implementation claims.**
4. **Current `wal.html` is maintained design documentation, not a frozen 2010 artifact.**
5. Modern automatic-checkpoint thresholds, later checkpoint modes, read-only changes, and other later behavior require their own chronology before being attributed to 3.7.0.
6. WAL reset/reuse is a logical/protocol transition, not evidence of secure physical erasure.

## Cross-Case Limits

- **Case 143:** direct same-project contrast. Rollback journal retains old page images for undo; WAL retains revised pages and later backfills them. Same atomicity/recovery domain does not make the mechanisms identical.
- **Case 73:** functional reclamation analogy only. A location becomes reusable after the relation keeping old material needed has retired; no genealogy.
- **Case 145:** JFFS2 may relocate live nodes before block erase. This illuminates `preserve live state before reuse`, but raw-Flash FS GC is not a SQLite checkpoint.
- **Case 124:** both show that authoritative durable state may span multiple related artifacts. Failure models and transition protocols differ.

## Related-Repository Check

A search of `tmzncty/computing-archaeology` for `SQLite WAL checkpoint` / `WAL` found no dedicated SQLite WAL treatment before this slice was opened. Broad database-log genealogy and SQLite pager history should be developed there if needed.

## Open Evidence Debt

- recover exact SQLite Fossil check-ins leading to 3.7.0 WAL publication;
- establish exact introduction dates for later checkpoint modes/default changes before using them historically;
- find named fault-injection studies or run controlled experiments around commit/checkpoint/reset boundaries;
- trace broader WAL/ARIES/System R history in `computing-archaeology` rather than expanding this case sideways;
- keep lower-layer durability/sanitization questions attached to their storage/filesystem evidence, not inferred from SQLite logical protocol.

## Sources

- SQLite 3.7.0 release: https://sqlite.org/releaselog/3_7_0.html
- SQLite WAL documentation: https://sqlite.org/wal.html
- SQLite 3.7.0 `src/wal.c`: https://github.com/sqlite/sqlite/blob/version-3.7.0/src/wal.c
- IBM Research ARIES publication page: https://research.ibm.com/publications/aries-a-transaction-recovery-method-supporting-fine-granularity-locking-and-partial-rollbacks-using-write-ahead-logging
