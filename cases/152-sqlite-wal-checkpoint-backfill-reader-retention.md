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
