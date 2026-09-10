# Evidence 143 — SQLite 3 rollback-journal hotness / recovery-authority grounding

**Status:** grounded  
**Case:** [`../cases/143-sqlite3-rollback-journal-hot-recovery-authority.md`](../cases/143-sqlite3-rollback-journal-hot-recovery-authority.md)  
**Bounded question:** when an interrupted SQLite rollback-mode transaction leaves old page images in a journal and a partly changed main database file, which retained relations make those old bytes recovery-authoritative, and how can commit retire that authority without necessarily erasing the old bytes?

## Evidence boundary

This record is deliberately bounded to the SQLite 3 rollback-journal design family.

The historical anchor is **SQLite 3.0.0, released 18 June 2004**. SQLite's maintained `lockingv3` document says it was originally created in early 2004 to describe the new Version-3 locking and journaling design while SQLite 2 was still common. That lets us date the design family conservatively, but it does **not** turn today's maintained documentation into a frozen facsimile of every 3.0.0 implementation detail.

Two later release anchors are used as explicit counterexamples to the idea that transaction commit must physically delete a rollback-journal file:

- SQLite **3.5.9**, 14 May 2008, introduced experimental `journal_mode` support including persistent journal files;
- SQLite **3.6.4**, 15 October 2008, added `TRUNCATE` journal mode.

SQLite WAL mode, introduced in 3.7.0 in 2010, is outside this case except as a stop condition. It is a different recovery/commit protocol.

The slice asks five questions:

1. What state is retained before SQLite overwrites database pages?
2. Why does the physical existence of a journal file not by itself make it a live recovery obligation?
3. How does a hot journal affect which surviving state is authoritative after an interrupted transaction?
4. Can commit retire rollback authority by deletion, truncation, or header invalidation rather than one universal physical act?
5. In a multi-database transaction, can a small retained reference graph determine whether still-present rollback bytes remain recovery-authoritative?

The inspected first-party documentation supports a clear answer: **page-image survival, journal validity, hotness, database/journal pairing, transaction commit, and physical reclamation are distinct relations.**

## Source ladder

| Source | Date / line | Evidence class | Use here |
|---|---|---|---|
| SQLite, **File Locking And Concurrency In SQLite Version 3** | maintained document; states it was originally created early 2004 | `H/P` | rollback-journal purpose, hot-journal conditions, recovery sequence, super-journal relation, stale-super-journal cleanup |
| SQLite, **Release 3.0.0** | 2004-06-18 | `H/P` | historical release anchor for SQLite 3; notes improved concurrency and atomic commits for attached databases |
| SQLite, **Atomic Commit In SQLite** | maintained project design document | `H/P` | copy-before-overwrite ordering, journal flush before main-file write, commit point, hot-journal recovery, multi-file commit |
| SQLite, **Database File Format** | maintained project reference | `H/P` | rollback-journal structure and header/validity context |
| SQLite, **PRAGMA journal_mode** | maintained project reference | `H/P` | `DELETE`, `PERSIST`, `TRUNCATE` operational distinctions |
| SQLite, **Release 3.5.9** | 2008-05-14 | `H/P` | bounded introduction anchor for experimental `journal_mode` / persistent journal mode |
| SQLite, **Release 3.6.4** | 2008-10-15 | `H/P` | bounded introduction anchor for `TRUNCATE` journal mode |
| SQLite, **How To Corrupt An SQLite Database File** | maintained project documentation | `H/P` | database/hot-journal pairing requirement and corruption boundary |
| SQLite, **Write-Ahead Logging** | maintained project documentation | `H/P` | stop condition: WAL is a later, different protocol introduced with 3.7.0 |

These are first-party SQLite project sources. They establish documented protocol semantics and release chronology, not universal empirical correctness under every VFS, filesystem, controller cache, kernel, or power-loss interleaving.

## Primary-source anchors

- SQLite, **File Locking And Concurrency In SQLite Version 3**: <https://www.sqlite.org/lockingv3.html>
- SQLite, **Atomic Commit In SQLite**: <https://www.sqlite.org/atomiccommit.html>
- SQLite, **Database File Format**: <https://www.sqlite.org/fileformat.html>
- SQLite, **PRAGMA journal_mode**: <https://www.sqlite.org/pragma.html#pragma_journal_mode>
- SQLite, **How To Corrupt An SQLite Database File**: <https://www.sqlite.org/howtocorrupt.html>
- SQLite, **Release 3.0.0 — 2004-06-18**: <https://www.sqlite.org/releaselog/3_0_0.html>
- SQLite, **Release 3.5.9 — 2008-05-14**: <https://www.sqlite.org/releaselog/3_5_9.html>
- SQLite, **Release 3.6.4 — 2008-10-15**: <https://www.sqlite.org/releaselog/3_6_4.html>
- SQLite, **Write-Ahead Logging**: <https://www.sqlite.org/wal.html>

## Historical record

### 1. Version-3 rollback journaling is anchored in the 2004 SQLite 3 transition

SQLite's maintained locking document explicitly says it was originally created in early 2004 and describes the new Version-3 locking/journaling mechanism. The 3.0.0 release record is dated **18 June 2004** and separately advertises improved concurrency and atomic commits for transactions involving attached databases.

This supports the bounded chronology:

`SQLite 3 rollback-journal design family -> public 2004 Version-3 transition`

But the evidence must not be stretched into:

`every sentence in today's maintained locking/atomic-commit pages == frozen 18-June-2004 implementation text`

The maintained documents have continued to serve as SQLite's design references. Exact line-by-line 3.0.x source archaeology remains separate work.

### 2. The rollback journal retains old page images before destructive main-file writes

SQLite's atomic-commit description says that before a database page is changed in the main database file, its original content is written to the rollback journal. The journal also records the original database size, which matters if a failed transaction enlarged the database and rollback must restore the prior length.

The journal is flushed before the corresponding main-database changes are allowed to proceed under the documented durability model.

This grounds an undo-oriented preservation order:

```text
current old page
    -> retain old page image in rollback journal
    -> flush rollback evidence under SQLite's assumed storage contract
    -> permit main-file page replacement
```

The immediate historical mechanism is not a general archive and not a redo log. It preserves enough selected previous state to undo an incomplete transaction.

Thus:

`rollback journal != user-visible version history`

and:

`rollback journal != SQLite WAL mode`

### 3. Journal file existence is weaker than hot-journal status

The locking document defines a **hot journal** through a conjunction of conditions rather than through mere file presence. The listed conditions include that the journal exists, is larger than a minimal size, has a non-zero/well-formed header, has a satisfiable super-journal relation (the named super-journal exists, or no super-journal is named), and that there is no `RESERVED` lock on the database file.

Therefore:

`rollback-journal bytes physically present != journal is hot`

and:

`old page images exist != rollback is currently required`

This is a protocol-currentness relation. The same bytes can have different operational meaning depending on retained header, naming, super-journal, and lock state.

### 4. A hot journal can temporarily outrank the apparent newest main-file bytes

SQLite's recovery sequence says a reader checks for a hot journal before treating the database as ordinarily readable. If a hot journal exists, SQLite obtains the locks needed for recovery, rolls original page images back into the database, flushes the recovered state, and only then retires the rollback journal and continues with ordinary access.

An interrupted transaction can therefore leave a main database file whose physically newest page mixture is **not** the logical state SQLite intends to expose.

Bounded conclusion:

`main database file exists != main database file is immediately authoritative current state`

The recovery relation can make the older journaled page image the authoritative input for reconstruction even though a newer partial page write also physically survives.

This is not a claim that the old journal file by itself has authority; hotness and pairing conditions still matter.

### 5. Default rollback-mode commit retires rollback authority

SQLite's atomic-commit design explains the default rollback-journal commit point in terms of deletion of the journal file after database pages have been written and flushed according to the documented sequence. From SQLite's process-visible model, the journal's existence changes as an atomic yes/no event even though lower layers may implement namespace deletion through more complex internal operations.

Therefore the safe bounded claim is:

`default DELETE-mode journal retirement -> transaction treated as committed`

not:

`all filesystems/media perform one universal physically atomic erasure event`

The distinction matters because later SQLite journal modes deliberately implement the same higher-level rollback-invalidation result in different physical ways.

### 6. `PERSIST` makes physical journal survival and rollback authority diverge

SQLite's `journal_mode=PERSIST` does not delete the rollback-journal file at transaction end. Instead, SQLite invalidates the journal header, normally by overwriting the header with zeros. The documentation explicitly says this prevents other connections from rolling the journal back.

The 3.5.9 release record provides the bounded 2008 introduction anchor for persistent journal mode.

This is unusually strong counterexample evidence:

`journal file survives != journal remains rollback-authoritative`

and:

`old page-image bytes may survive != transaction remains uncommitted`

The file can remain allocated precisely as a performance optimization while its recovery semantics have changed.

Nothing here proves secure erasure of the old page images. In fact `PERSIST` is useful because it demonstrates the opposite: operational invalidation can happen while much of the former journal body remains physically present.

### 7. `TRUNCATE`, `DELETE`, and `PERSIST` separate logical commit from one physical retirement act

SQLite 3.6.4 added `TRUNCATE` mode. Current documentation describes the three rollback-journal end states as:

- `DELETE`: remove the journal file;
- `TRUNCATE`: truncate the journal to zero length;
- `PERSIST`: leave the file but invalidate its header.

The modes differ in physical namespace/content state yet can all establish that the old rollback material is no longer a live recovery obligation.

Therefore:

`same higher-level commit relation != one universal physical invalidation mechanism`

Chronology remains controlled: the 2008 `PERSIST`/`TRUNCATE` modes are later evidence and must not be projected backward as 2004 source vocabulary.

### 8. Multi-database commit adds a retained super-journal reference graph

For transactions spanning multiple attached databases, SQLite gives each database its own rollback journal and creates a **super-journal**. The super-journal stores the names of the participating rollback journals; each rollback journal records the super-journal name.

The super-journal does not contain another copy of all changed database pages. It is coordination/reference state.

This grounds:

`super-journal != payload replica`

and:

`small retained reference graph can govern multi-file rollback authority`

The multi-database commit sequence treats deletion of the super-journal as the critical commit transition. After that deletion, individual rollback journals can still physically exist pending cleanup, but a journal that names a now-nonexistent super-journal fails the hot-journal test.

Thus:

`individual rollback journal physically present != still hot after super-journal commit`

This is the strongest bounded example in the case of a **reference relation** changing the currentness of still-surviving bytes.

### 9. A stale super-journal can survive after its operational liveness ends

The locking documentation describes stale super-journals and a procedure for deciding whether one may be deleted. If no live rollback journal still references a super-journal, it can be stale cleanup residue.

Therefore:

`coordination metadata physically present != coordination metadata operationally live`

and:

`operational retirement != physical reclamation completion`

This resembles other repository cases only functionally. SQLite's relation is based on files, names, and rollback-hotness semantics rather than an FTL map or distributed replica membership.

### 10. Database and hot journal must remain correctly paired

SQLite's **How To Corrupt An SQLite Database File** documentation warns that after a failed transaction a hot rollback journal must remain with the database it belongs to. Moving, deleting, renaming, mismatching, or copying a database without its hot journal can defeat automatic recovery and cause corruption.

The important retention relation is therefore not merely two independent byte populations:

`database bytes somewhere + journal bytes somewhere != recoverable paired state`

Instead:

`main-file identity + matching rollback journal + validity/currentness relation -> recoverable state under the protocol`

This supports a general engineering point while keeping the historical mechanism specific:

`recovery evidence survival != recovery relation survival`

## Engineering reconstruction

### A. Destructive update can require temporary retention of a superseded state

Rollback mode permits an in-place database file to be changed because selected old pages remain available until the transaction either commits or recovery no longer needs them.

The retained old state is therefore neither simply obsolete nor archival during the transaction. It has a temporary **recovery authority**.

Project formulation:

`old state superseded in intent != old state immediately dispensable`

until commit currentness is established.

### B. Recovery authority is relational

Hotness depends on more than page bytes. It also depends on journal validity/header state, lock state, and for multi-database transactions the super-journal reference relation.

Therefore:

`trace survival != recovery admissibility`

This is an engineering reconstruction from SQLite's documented protocol, not historical SQLite terminology.

### C. Commit can be modeled as withdrawing a future recovery option

Before commit, rollback journal state remains eligible to undo the transaction. After DELETE/TRUNCATE/PERSIST commit handling, that same prior-state path is no longer admissible.

The project can therefore use:

`commit currentness -> prior rollback path no longer admitted`

without claiming that commit physically destroys every prior trace.

### D. Multi-object atomicity can depend on retained naming/reference structure

The super-journal example shows that retaining page images separately for each database is not enough to encode the atomic group relation. A small name graph coordinates whether the set of journals must still be treated as one recovery obligation.

This is a particularly clear example of:

`control-state size != scope of retained-state consequence`

Deletion of one small super-journal can change the recovery admissibility of several still-existing larger journal files.

### E. Correct identity pairing is constitutive, not decorative metadata

The corruption guidance shows that correct pairing between main database and hot journal is part of the recovery mechanism. If a journal becomes detached from the database it qualifies, keeping its bytes does not preserve the same operational object.

Thus:

`byte survival != retained recovery identity`

## Cross-case comparison

### Case 124 — ext4 / PostgreSQL durable rename

[`Case 124`](../cases/124-linux-ext4-rename-fsync-durability-closure.md) shows that durable file contents do not automatically imply durable namespace binding, and that recovery identity can depend on directory state.

Case 143 adds a related but distinct boundary:

`correct recovery bytes != correct recovery pairing/admissibility`

The comparison is functional only. It does not establish ext4/PostgreSQL -> SQLite genealogy.

### Case 137 — LevelDB MANIFEST/CURRENT

[`Case 137`](../cases/137-leveldb-v17-manifest-current-recovery.md) reconstructs current serving state through a MANIFEST/CURRENT relation plus WAL recovery, with old files sometimes remaining physically live for readers.

SQLite rollback mode instead retains **prior page images** so an incomplete destructive update can be undone, and commit withdraws that rollback authority.

Functional contrast:

`LevelDB: replay/select reconstructed current metadata state`

versus

`SQLite rollback mode: preserve old state until undo authority is retired`

No genealogy is asserted.

### Case 74 — JBD/JBD2 revoke

[`Case 74`](../cases/74-linux-jbd-revoke-suppress-stale-replay.md) shows that stored journal material can be suppressed from replay when later metadata changes its admissibility.

SQLite likewise separates surviving recovery material from whether the protocol treats it as replay/rollback eligible. The implementations, formats, and histories are different; this is only a cross-mechanism comparison.

### Case 44 — NVMe sanitization

[`Case 44`](../cases/44-nvme13-deallocate-sanitize-forgetting.md) supplies an important stop condition.

SQLite `PERSIST` mode can leave old rollback-page bytes in a journal while invalidating the journal header. Therefore:

`rollback authority retired != prior bytes securely erased`

A database commit is not a sanitize operation, and ordinary journal cleanup proves neither overwrite nor forensic disappearance.

## Philosophical boundary

The engineering record permits one narrow interpretive observation:

> **technical persistence can depend not only on which traces survive, but on retained relations that say which trace is still entitled to count in a future operation.**

SQLite is a useful counterexample to any ontology that equates persistence with mere physical survival: `PERSIST` can preserve the journal file while withdrawing rollback authority, and super-journal deletion can change the admissibility of individual journals that still remain.

That does **not** justify:

- calling a rollback journal a model of human memory;
- equating transaction commit with psychological forgetting;
- treating every journal as Stieglerian tertiary retention;
- interpreting the super-journal as a philosophical archive;
- claiming that operational currentness exhausts forensic materiality.

The philosophical layer remains downstream of the documented engineering relations.

## Failure / lower-layer boundary

SQLite's project documentation explicitly depends on the operating system, VFS, locking implementation, flush primitives, filesystem, and storage device honoring the contracts SQLite expects.

The record therefore does not prove:

- every `fsync`/flush reaches nonvolatile media under every controller configuration;
- every filesystem gives identical rename/delete/truncate crash behavior;
- every VFS implements lock semantics correctly;
- power loss cannot expose implementation-specific failure windows;
- a stale journal is forensically unrecoverable;
- journal invalidation is secure erasure.

Power-cut and VFS fault injection belong to experimental evidence, not to this historical/documentary grounding.

## Related-repository check

A fresh recursive-tree check of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated SQLite / rollback-journal case.

The division of labor is therefore:

- **`technical-retention`:** rollback page images, hotness, recovery authority, commit invalidation, pairing, and cross-case retention semantics;
- **`computing-archaeology`:** if pursued, broader SQLite 2 -> 3 pager/locking genealogy, exact 2004 source evolution, VFS/platform history, PERSIST/TRUNCATE source genealogy, WAL evolution, and named-filesystem/device engineering behavior.

No duplicate technical history is created here.

## Findings proposed for `CASE_INDEX.md`

- **3031 — 2004 SQLite-3 anchor != frozen-current-document chronology:** 3.0.0 is dated 2004-06-18 and the maintained locking document says it was originally created in early 2004, but today's maintained design pages are not proof that every described detail was unchanged in 3.0.0. (`H/P`, `X`)
- **3032 — rollback journal retains pre-update page state before destructive main-file update:** SQLite documents copying original page images and original size into the journal before overwriting corresponding database state. (`H/P`, `E`)
- **3033 — rollback journal != redo/WAL history:** rollback mode retains selected prior page images for undo; SQLite WAL mode is a later distinct protocol. (`H/P`, `E`, `X`)
- **3034 — journal physical presence != hot-journal recovery authority:** hotness also depends on valid header/size, super-journal relation, and lock state. (`H/P`, `E`)
- **3035 — hot journal can suspend ordinary read admissibility until rollback:** SQLite checks and rolls back a hot journal before ordinary reading continues. (`H/P`, `E`)
- **3036 — main database-file presence != authoritative readable current state after interrupted write:** physically newer partial page state can be rejected in favor of the pre-transaction state reconstructed from the hot journal. (`H/P`, `E`)
- **3037 — default DELETE-mode commit != universal physical-delete theorem:** journal removal is SQLite's commit transition under its interface/storage assumptions, not proof of one physically atomic erasure mechanism across every lower layer. (`H/P`, `X`)
- **3038 — PERSIST file survival != rollback-authority survival:** 2008 persistent journal mode can leave the file while zeroing/invalidation of the header prevents rollback. (`H/P`, `E`)
- **3039 — DELETE/TRUNCATE/PERSIST physical difference != different high-level commit objective:** deletion, zero-length truncation, and header invalidation can all retire the old rollback path. (`H/P`, `E`)
- **3040 — 2008 journal modes != 2004 vocabulary:** PERSIST/TRUNCATE chronology must not be back-projected into the SQLite 3.0.0 historical record. (`H/P`, `X`)
- **3041 — super-journal reference state != payload replica:** it coordinates a multi-database transaction by retaining journal names rather than another copy of database pages. (`H/P`, `E`)
- **3042 — super-journal deletion can commit while individual rollback journals still physically remain:** named journals cease to be hot when the super-journal relation required by the hotness test disappears. (`H/P`, `E`)
- **3043 — stale super-journal physical presence != operational liveness:** no-longer-referenced coordination metadata may persist until later cleanup. (`H/P`, `E`)
- **3044 — database+journal byte survival != recovery-pairing survival:** SQLite warns that separating, mismatching, renaming, or copying a database without its hot journal can defeat recovery. (`H/P`, `E`)
- **3045 — commit/journal invalidation != sanitization:** retiring rollback authority does not establish overwrite, block erase, cryptographic erase, or forensic disappearance of prior page bytes. (`E`, `X`)
- **3046 — LevelDB current reconstruction != SQLite rollback undo authority:** both use retained control evidence to govern currentness, but their direction of recovery and historical mechanisms differ. (`A`, `X`)
- **3047 — namespace durability relation ~ recovery pairing only functionally:** Case 124 and Case 143 both show that byte survival can be insufficient when the required naming/identity relation is lost, without implying genealogy. (`A`, `X`)
- **3048 — related-repository boundary:** no dedicated SQLite path was found in the fresh `computing-archaeology` recursive-tree check; broader pager/VFS/source genealogy belongs there if developed, while this case keeps recovery-authority semantics. (`H/P` project-state record)

## Open work

- recover and compare a frozen early-2004 / 3.0.x source snapshot against the maintained design pages;
- identify exact super-journal introduction source/check-in history;
- trace PERSIST/TRUNCATE implementation commits beyond the release-note chronology;
- build a separate bounded WAL-mode case rather than merging rollback and WAL semantics;
- run controlled fault/VFS experiments for journal flush, delete, truncate, header invalidation, and hot-journal recovery;
- test database+journal move/copy/mispairing failure modes in an isolated experiment;
- keep filesystem/device durability claims routed through Cases 124/15/31 instead of treating SQLite's documented contract as lower-layer empirical proof.
