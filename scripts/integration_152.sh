#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

case_path="cases/152-sqlite-wal-checkpoint-backfill-reader-retention.md"
evidence_path="evidence/152-sqlite-2010-wal-checkpoint-retention-grounding.md"
case143_path="cases/143-sqlite3-rollback-journal-hot-recovery-authority.md"
workflow_path=".github/workflows/integrate-case152.yml"
script_path="scripts/integration_152.sh"

if [[ -e "$case_path" || -e "$evidence_path" ]]; then
  echo "Case 152 canonical files already exist; refusing to duplicate." >&2
  exit 1
fi

python3 - <<'PY'
from pathlib import Path
idx = Path('CASE_INDEX.md').read_text(encoding='utf-8')
if '3272.' not in idx:
    raise SystemExit('Expected Case 151 finding 3272 is absent; CASE_INDEX baseline changed.')
if '3273.' in idx or 'Case 152 — SQLite WAL Checkpoint' in idx:
    raise SystemExit('Finding 3273 or Case 152 already exists; refusing to collide.')
road = Path('ROADMAP.md').read_text(encoding='utf-8')
if 'Case 151' not in road:
    raise SystemExit('Expected Case 151 roadmap entry is absent; ROADMAP baseline changed.')
PY

cat > "$case_path" <<'EOF'
# Case 152 — SQLite WAL Checkpoint: Committed-but-Unbackfilled State, Reader End Marks, and Reuse Authority

Status: grounded

## 0. Research Status Snapshot

- **Historical record:** grounded at a conservative public boundary. SQLite 3.7.0 was released on **2010-07-21** and its release record says it added write-ahead logging. The frozen `version-3.7.0` `src/wal.c` implementation comments directly document frames, commit markers, reader snapshot marks, checkpoint/backfill state, WAL reset conditions, and the transient wal-index.
- **Engineering reconstruction:** grounded at the public format/protocol level. A transaction can be committed in the WAL before its revised pages are copied back into the main database. Checkpoint completion, reader retirement, and WAL reuse are separate transitions.
- **Prior art:** bounded. IBM's 1992 ARIES publication explicitly uses write-ahead logging, so SQLite 3.7.0 is not treated as the invention of WAL. No ARIES -> SQLite genealogy is asserted.
- **Functional analogy:** bounded. Case 143 is a documented SQLite-internal contrast between rollback journaling and WAL; reclamation analogies to garbage collection are functional only.
- **Philosophical interpretation:** interpretation only. A committed/current database state can be distributed across a base image, a retained delta log, and reader-specific cut points rather than being identical to the bytes currently resident in one canonical file.

## 1. Problem Statement

Case 143 showed that SQLite rollback journaling temporarily retains **older page images** so an interrupted overwrite can be undone. SQLite WAL mode, introduced in 3.7.0, reverses the direction: the original database file remains in place while **revised page images** are appended to a WAL. A commit record can make those revisions transactionally current before checkpoint has copied them back into the main database.

That yields a precise retention problem:

> After a transaction is already committed, what retained WAL state must continue to exist, what reader relations can prevent it from being overwritten, and what transition finally gives the writer authority to reuse the WAL region?

This case is deliberately about **committed-but-not-yet-backfilled state and WAL reuse authority**. It is not a general history of write-ahead logging, not a benchmark of SQLite WAL performance, and not a claim about secure deletion.

The detailed source ledger is [`../evidence/152-sqlite-2010-wal-checkpoint-retention-grounding.md`](../evidence/152-sqlite-2010-wal-checkpoint-retention-grounding.md).

## 2. Boundary and Stop Conditions

### In scope

- SQLite 3.7.0 as the public WAL introduction boundary;
- WAL frames and commit markers;
- reader `mxFrame` / end-mark snapshot boundaries;
- checkpoint/backfill progress;
- the conditions under which the WAL may be reset and reused;
- the distinction between persistent WAL state and transient wal-index coordination state;
- direct comparison with Case 143 rollback journaling;
- prior-art guardrail against calling SQLite the inventor of WAL.

### Out of scope

- full ARIES/System R/database-recovery genealogy;
- later SQLite checkpoint modes as if they were all frozen in 3.7.0;
- exact filesystem/device durability below SQLite's VFS contract;
- WAL2, begin-concurrent, or experimental branches;
- performance benchmarking;
- low-level flash remanence or secure sanitization;
- claims that `mxFrame` or `nBackfill` are user payload replicas.

## 3. Evidence Matrix

| ID | Evidence | Type | Supports | Does not support |
|---|---|---|---|---|
| E152.1 | SQLite 3.7.0 release record, 2010-07-21 | first-party historical | public release boundary; WAL added in 3.7.0 | invention of WAL generally |
| E152.2 | SQLite `version-3.7.0/src/wal.c` header/comments | frozen first-party source | frames contain revised pages; commit marker; checkpoint; reader snapshot; transient wal-index | all later SQLite behavior |
| E152.3 | SQLite 3.7.0 `WalCkptInfo` comments | frozen first-party source | `nBackfill`, reader marks, checkpoint limits, reset/reuse preconditions | exact physical-media erasure or secure deletion |
| E152.4 | current SQLite WAL design document | maintained first-party technical | explicit rollback-vs-WAL contrast; current end-mark/checkpoint explanation; WAL is persistent database state | verbatim 2010 implementation for every later feature |
| E152.5 | IBM Research ARIES, 1992 | high-quality primary scholarly | write-ahead logging existed publicly before SQLite WAL | direct genealogy into SQLite |

## 4. Historical Record

### 4.1 Public SQLite boundary: 2010-07-21

SQLite's first-party 3.7.0 release page is dated **2010-07-21** and lists “Added support for write-ahead logging.” The maintained SQLite WAL documentation gives the same version/date boundary.

This is a release/public-availability statement, not an invention claim. WAL terminology and recovery methods predate SQLite by decades; IBM Research's ARIES publication in **1992** explicitly describes a transaction recovery method using write-ahead logging.

Therefore:

> **SQLite 3.7.0 WAL introduction != invention of write-ahead logging.**

And chronology alone does not establish ARIES -> SQLite implementation genealogy.

### 4.2 Frozen 3.7.0 source already contains the retention relation

The `version-3.7.0` `src/wal.c` comments define a WAL as a header followed by frames. Each frame records the revised contents of one database page. A transaction commits when a frame containing a commit marker is written. Periodically, WAL content is transferred back into the database file by a **checkpoint**.

The same source explicitly allows a WAL file to be used multiple times: after frames have been checkpointed, new frames can later overwrite older ones. Checksums/counters/salts distinguish valid frames from leftovers from prior checkpoint generations.

That directly establishes:

- `commit != checkpoint`;
- `frame physically present != frame valid in the current WAL generation`;
- `old WAL bytes reusable != old WAL bytes securely erased`.

## 5. Mechanism 1 — Commit can precede main-file incorporation

The maintained SQLite documentation makes the contrast especially clear. In rollback-journal mode, old content is copied aside and the main database is changed. In WAL mode, original database content remains in the database file while changes are appended to the WAL; a transaction commits when a commit record is appended.

So a committed transaction does **not** require its revised pages to have already been copied into the main database file.

At that moment the logical database may be embodied by a composition:

```text
main database file
    +
valid committed WAL frames
    =
current state for a newly starting reader
```

This is not merely a performance optimization. It is a currentness relation: the newest committed state can be authoritative even while some of its page embodiments remain outside the base database file.

Therefore:

> **transaction commit != main-file backfill completion.**

And:

> **main database file alone != necessarily the complete latest committed database state while live WAL frames remain relevant.**

The current SQLite WAL documentation reinforces the operational consequence: the WAL file is part of persistent database state and separating it from the database can lose committed transactions or corrupt the usable database image. That current maintenance statement is a later operational witness; it is not silently projected into every 2010 syscall detail.

## 6. Mechanism 2 — Reader end marks retain an older current cut

The frozen 3.7.0 source says that when a read transaction starts, it records the index of the last valid WAL frame (`mxFrame`) and uses that same boundary for subsequent reads. Later transactions may append frames beyond that point, but the earlier reader ignores them and therefore sees a consistent snapshot.

The maintained WAL documentation calls the corresponding boundary the reader's **end mark**.

This yields a useful distinction:

> **globally later committed frame != visible frame for every already-running reader.**

A reader's snapshot is not another full copy of the database. It is a retained **cut relation** that tells the reader which WAL generation prefix counts for that read transaction.

Thus:

```text
payload pages
    !=
reader snapshot boundary
    !=
global newest commit boundary
```

Multiple readers can legitimately use different cut points over the same database/WAL material.

## 7. Mechanism 3 — Checkpoint progress is constrained by live readers

The 3.7.0 source's `WalCkptInfo` explicitly records:

- `nBackfill`: how many WAL frames have been copied back into the database;
- reader marks: boundaries associated with active reader locks.

The source comment says the checkpointer may transfer frames only up to limits that are safe for all reader marks in use. The maintained WAL documentation gives the same higher-level behavior: a checkpoint can run concurrently with readers but must stop before it would overwrite database-file state still needed by an older reader snapshot, and it can resume later.

Therefore:

> **checkpoint started != checkpoint completed.**

And more importantly:

> **committed data eligible for eventual backfill != data immediately safe to overwrite in the base image for every live reader.**

An already-committed transaction can coexist with an older reader that still imposes retention pressure on the WAL/base relationship. The transaction's commit status and the reader's snapshot lifetime are separate clocks.

## 8. Mechanism 4 — Full backfill alone does not grant WAL reuse authority

The 3.7.0 `WalCkptInfo` comments make the reuse gate explicit. `nBackfill == mxFrame` means all current WAL content has been copied into the database. But a writer resets the WAL back to its beginning only when **both** conditions hold:

1. all WAL content has been backfilled; and
2. no readers are using the WAL.

This is the central retention result of the case:

```text
all frames backfilled
    +
no reader still depends on WAL
    -> WAL reset/reuse authority
```

So:

> **backfill completion != immediate WAL reuse authority.**

The remaining reader relation can keep old WAL generations operationally relevant even after their page contents have been copied to the main database.

Once the conditions are satisfied, the writer can restart at frame 1 and later overwrite old frame locations. The source's generation salts/checksums help distinguish current frames from leftovers.

But this transition is protocol-level reclamation, not secure deletion:

> **WAL reset/reuse != media sanitization.**

Nothing in the cited SQLite protocol proves that prior magnetic/flash embodiments have become forensically irrecoverable.

## 9. Mechanism 5 — Durable WAL state and transient wal-index state are different

The frozen 3.7.0 source is unusually explicit: the **wal-index is transient** and after a crash “can (and should) be reconstructed from the original WAL file.” It may live in shared memory or an mmapped backing file and can use an architecture-specific representation because it is not the durable cross-platform record.

This prevents a common collapse:

> **coordination metadata needed for efficient live access != durable recovery source of truth.**

The WAL contains the page frames and validity/commit information from which the wal-index can be rebuilt. The wal-index accelerates lookup and holds live checkpoint/reader coordination such as `nBackfill` and reader marks.

So:

```text
persistent WAL evidence
    !=
reconstructible wal-index acceleration/coordination state
```

That does not mean the wal-index is unimportant while the database is running. It means its required lifetime and reconstruction obligations differ from those of the WAL payload/commit record.

## 10. Direct Contrast with Case 143

Case 143 and Case 152 are not two names for the same journal protocol. SQLite's own documentation describes their directionality differently.

### Rollback journal — Case 143

```text
retain old page image
    -> overwrite main-file page
    -> if failure, restore older state
    -> on commit, retire rollback authority
```

The retained journal is predominantly **pre-change recovery state**.

### WAL — Case 152

```text
keep old main-file page in place
    -> append revised page to WAL
    -> commit by appending commit marker
    -> readers compose base + eligible WAL frames
    -> checkpoint later copies revised pages back
    -> after backfill and reader retirement, permit WAL reuse
```

The retained WAL contains **newer committed state** that may need to remain authoritative until it is safely incorporated and no reader still requires the older cut relation.

Thus:

> **rollback-journal old-state retention != WAL new-state retention.**

Both solve atomicity/recovery problems inside SQLite, but they do so with different direction of retained payload and different retirement transitions.

## 11. Prior Art and Anti-Anachronism

IBM's ARIES paper, published in 1992, is sufficient to block any claim that SQLite introduced write-ahead logging as a general technique. This case does not attempt to recover the earlier System R / database-log genealogy or prove that SQLite derived a particular state machine from ARIES.

Likewise, current SQLite WAL documentation contains later features and wording. The frozen 3.7.0 source is used for claims about the initial public implementation wherever possible; current documentation is used for maintained public semantics and current operational warnings.

Therefore:

- `2010 SQLite WAL != first WAL`;
- `earlier WAL literature != proven direct SQLite genealogy`;
- `current SQLite WAL docs != frozen 2010 implementation in every detail`.

## 12. Cross-Case Comparison

| Case | Retained relation | Safe comparison | Stop condition |
|---|---|---|---|
| Case 143 — SQLite rollback journal | older page images + hotness/commit relation | same project, directly documented alternate journal direction | do not collapse undo-oriented rollback into WAL backfill |
| Case 73 — GC / reclamation | retained reachability/reclamation relation | reuse waits for a relation that says old material is no longer needed | functional analogy only; no storage-engine genealogy |
| Case 145 — JFFS2 GC | live-node relocation before erase | old physical space becomes reclaimable only after live state is preserved elsewhere | raw-Flash FS mechanics are not SQLite checkpoint mechanics |
| Case 124 — durable rename boundary | persistence depends on more than one object/namespace relation | a single file's bytes may be insufficient to describe authoritative durable state | different failure model and mechanism |

The strongest comparison is Case 143 because SQLite itself explicitly contrasts rollback and WAL. The GC comparisons are strictly functional: they illuminate the difference between **material copied elsewhere** and **authority to reuse the old location** without asserting shared ancestry.

## 13. Related Repository Boundary

`tmzncty/computing-archaeology` was searched for a dedicated SQLite WAL/checkpoint case before this slice was opened; none was found.

A broad history of write-ahead logging, ARIES/System R lineage, SQLite pager evolution, wal-index implementation history, VFS portability, and later checkpoint-mode evolution belongs primarily in `computing-archaeology`.

`technical-retention` keeps the narrower question:

> **how committed revised pages, reader cut points, backfill progress, and reuse authority acquire different lifetimes inside one recovery protocol.**

## 14. Philosophical Interpretation

**Interpretation only:** “current” need not name one fully materialized file image. In WAL mode, a current committed database can be a relation among an older base image, newer retained frames, and a reader-specific admissibility boundary.

That supports a narrow repository-level observation:

> **technical currentness can be compositional, while retirement of old storage depends on both incorporation and the disappearance of observers that still need an older cut.**

This is not SQLite's historical vocabulary and must not be treated as evidence for human memory, social memory, or a universal philosophy of persistence.

## 15. Open Questions

- recover exact SQLite Fossil check-ins/technical notes leading from pre-3.7.0 WAL development to the 2010 release without treating source-file copyright dates as release dates;
- trace the broader WAL/ARIES/System R genealogy in `computing-archaeology` before making any lineage claim;
- separately ground later SQLite checkpoint modes and WAL-growth controls if their exact introduction chronology matters;
- perform VFS/fault-injection experiments that crash between commit, partial checkpoint, reader retirement, and WAL reset;
- test copy/move/separation failure modes for database/WAL pairs in an isolated experiment;
- keep physical-device persistence and sanitization routed through lower-layer cases rather than inferring them from SQLite's logical reuse protocol.

## Sources

1. SQLite, **Release 3.7.0 On 2010-07-21**: https://sqlite.org/releaselog/3_7_0.html
2. SQLite, **Write-Ahead Logging**: https://sqlite.org/wal.html
3. SQLite source, frozen `version-3.7.0`, `src/wal.c`: https://github.com/sqlite/sqlite/blob/version-3.7.0/src/wal.c
4. C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh, Peter Schwarz, IBM Research, **ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging**, ACM TODS, 1992: https://research.ibm.com/publications/aries-a-transaction-recovery-method-supporting-fine-granularity-locking-and-partial-rollbacks-using-write-ahead-logging
5. Case 143 — SQLite 3 Rollback Journals: [`143-sqlite3-rollback-journal-hot-recovery-authority.md`](143-sqlite3-rollback-journal-hot-recovery-authority.md)
EOF

cat > "$evidence_path" <<'EOF'
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
EOF

python3 - <<'PY'
from pathlib import Path

idx_path = Path('CASE_INDEX.md')
idx = idx_path.read_text(encoding='utf-8').rstrip() + '\n'
section = r'''

### Case 152 — SQLite WAL Checkpoint: Committed-but-Unbackfilled State, Reader End Marks, and Reuse Authority
3273. **[H]** SQLite 3.7.0 was released on 2010-07-21 and its first-party release record says it added write-ahead logging; this is a SQLite public-release boundary, not a general WAL invention date.
3274. **[H/E]** Frozen `version-3.7.0/src/wal.c` documents WAL frames containing revised database-page contents and transaction commit when a frame carrying a commit marker is written.
3275. **[E]** `transaction commit != checkpoint`: SQLite can establish a committed transaction in the WAL before revised pages are copied into the main database file.
3276. **[E]** `committed current state != main-database-file-only state`: while relevant WAL frames remain, a reader may need the base database plus eligible committed WAL frames to reconstruct current content.
3277. **[E]** A 3.7.0 reader fixes an `mxFrame` boundary (maintained docs call the analogous boundary an end mark) and uses it for the read transaction, so snapshot identity is a retained cut relation rather than another payload replica.
3278. **[E]** `later global commit != visibility to every existing reader`: frames appended after an older reader's cut are deliberately ignored by that reader.
3279. **[E]** Active reader marks constrain checkpoint progress; a checkpointer cannot freely overwrite base-database state that an older reader still relies on.
3280. **[E]** `nBackfill` in the 3.7.0 wal-index records how many WAL frames have been copied into the database, making checkpoint progress distinct from commit state and from checkpoint completion.
3281. **[E]** `all frames backfilled != immediate WAL reuse authority`: 3.7.0 resets/reuses the WAL only when `nBackfill == mxFrame` and no readers are using the WAL.
3282. **[E]** WAL frame validity is generational: salts/checksums/counters distinguish current frames from leftovers after checkpoint/reset, so physical survival of an old frame does not make it current.
3283. **[E]** `WAL reset/reuse != media sanitization`: logical invalidation/overwrite eligibility does not prove old magnetic/flash embodiments are forensically irrecoverable.
3284. **[E]** The 3.7.0 source explicitly calls the wal-index transient and reconstructible from the original WAL after crash.
3285. **[E]** `persistent WAL evidence != reconstructible wal-index coordination state`: payload/commit records and lookup/checkpoint/read-mark metadata have different required lifetimes.
3286. **[H]** IBM Research's 1992 ARIES publication explicitly uses write-ahead logging, providing a conservative prior-art floor well before SQLite 3.7.0.
3287. **[A]** `earlier WAL literature != direct SQLite genealogy`: chronology blocks a novelty overclaim but does not establish ARIES -> SQLite implementation descent.
3288. **[E]** Case 143 and Case 152 form a documented SQLite-internal contrast: rollback journaling retains older page images before overwrite, while WAL retains revised page images outside the base file until later checkpoint/backfill.
3289. **[E]** `rollback authority retirement != WAL reuse authority`: the two SQLite journal directions retire different retained state under different transition conditions.
3290. **[A]** GC/reclamation cases are only functional analogies: both may delay reuse until a retained relation retires, but SQLite checkpoint, JFFS2 erase-block GC, and other reclamation state machines are not genealogically interchangeable.
3291. **[E]** Current SQLite documentation treats the WAL file as part of persistent database state while relevant; separating it from the database can lose committed transactions or corrupt the usable pair. This is a maintained operational witness, not a frozen 2010 syscall trace.
3292. **[P]** Interpretation only: technical currentness can be compositional across a base image, retained deltas, and observer-specific cut relations; this is not SQLite historical vocabulary or a universal model of memory.
'''
idx_path.write_text(idx + section.lstrip('\n'), encoding='utf-8')

road_path = Path('ROADMAP.md')
road = road_path.read_text(encoding='utf-8')
entry = '- [x] Ground SQLite WAL checkpoint retention as a bounded case: 3.7.0 public boundary, commit-before-backfill, reader end-mark/mxFrame snapshot retention, `nBackfill` progress, full-backfill-plus-reader-retirement reuse gate, transient wal-index vs persistent WAL, ARIES prior-art guardrail, and direct contrast with Case 143 rollback journaling (Case 152).'
if 'Case 152' not in road:
    lines = road.splitlines()
    inserted = False
    for i, line in enumerate(lines):
        if 'Case 151' in line and line.lstrip().startswith('- [x]'):
            lines.insert(i + 1, entry)
            inserted = True
            break
    if not inserted:
        raise SystemExit('Could not locate checked Case 151 ROADMAP entry for insertion.')
    road_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

p = Path('cases/143-sqlite3-rollback-journal-hot-recovery-authority.md')
s = p.read_text(encoding='utf-8')
old = '- compare rollback-journal and WAL-mode currentness only in a separate bounded case;'
new = '- rollback-journal versus WAL-mode currentness is now addressed separately in [`Case 152`](152-sqlite-wal-checkpoint-backfill-reader-retention.md); keep further WAL genealogy and experiments out of this rollback-journal case;'
if old not in s:
    raise SystemExit('Expected Case 143 open-work line not found; refusing to patch stale text.')
p.write_text(s.replace(old, new, 1), encoding='utf-8')
PY

git diff --check

grep -q '^Status: grounded' "$case_path"
grep -q 'commit != checkpoint' "$case_path"
grep -q 'wal-index is transient' "$case_path"
grep -q '3273\.' CASE_INDEX.md
grep -q '3292\.' CASE_INDEX.md
grep -q 'Case 152' ROADMAP.md
grep -q 'Case 152' "$case143_path"

git add CASE_INDEX.md ROADMAP.md "$case_path" "$evidence_path" "$case143_path"
git rm -f "$script_path" "$workflow_path"

git diff --cached --check

git commit -m "case152: ground SQLite WAL checkpoint retention"
git push origin HEAD:main
