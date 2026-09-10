# SQLite 3 Rollback Journals: Hot Recovery Evidence, Commit Invalidation, and Paired-State Identity

**Status:** `grounded`

## Scope

- **Object / system:** SQLite 3 rollback-journal mode, with the single-database rollback journal as the core mechanism and the multi-database super-journal as a bounded extension.
- **Historical anchor:** SQLite 3.0.0, released **18 June 2004**; SQLite's maintained locking document says it was originally created in early 2004 to explain the new Version-3 locking and journaling design.
- **Later bounded extensions:** `PERSIST` journal mode, introduced experimentally in SQLite 3.5.9 on **14 May 2008**, and `TRUNCATE`, added in SQLite 3.6.4 on **15 October 2008**.
- **Retention question:** when an interrupted transaction leaves both a partially changed database file and rollback information on disk, what retained relation makes the old pages recovery-authoritative, and what transition makes those same rollback bytes cease to count as a live recovery obligation?

This case is deliberately about **rollback-mode recovery currentness**, not a general SQLite history. SQLite WAL mode (3.7.0, 2010) is a different protocol and is outside the bounded mechanism except as a stop condition.

The detailed source ledger is [`../evidence/143-sqlite3-rollback-journal-hotness-grounding.md`](../evidence/143-sqlite3-rollback-journal-hotness-grounding.md).

---

## Historical vocabulary and chronology

The inspected SQLite project documents directly use:

- `rollback journal`;
- `hot journal`;
- `super-journal`;
- `SHARED`, `RESERVED`, `PENDING`, and `EXCLUSIVE` locks;
- `journal_mode=DELETE`;
- `journal_mode=PERSIST`;
- `journal_mode=TRUNCATE`;
- `commit`;
- `rollback`;
- `pager`.

The maintained **File Locking And Concurrency In SQLite Version 3** document says it was originally created in early 2004 and that Version 3.0.0 introduced a new locking and journaling mechanism. The SQLite 3.0.0 release record, dated **2004-06-18**, separately lists improved concurrency and atomic commits for `ATTACH`ed databases.

That chronology is sufficient to anchor the Version-3 rollback-journal design family in 2004. It is **not** sufficient to claim that every sentence in today's maintained documentation, every later optimization, or every current journal mode already existed unchanged in 3.0.0.

The later release records are explicit:

- SQLite 3.5.9 (2008-05-14) added experimental `journal_mode` support and persistent journals;
- SQLite 3.6.4 (2008-10-15) added the `TRUNCATE` option;
- SQLite 3.7.0 (2010-07-21) later added WAL mode, which is not the mechanism studied here.

Therefore:

> **maintained Version-3 documentation != frozen 2004 source snapshot**

and:

> **2008 PERSIST/TRUNCATE semantics != vocabulary to project back into the 2004 release without qualification.**

---

## Retained state

A rollback-mode transaction can involve several different retained state classes:

1. the **main database file**, which may contain some new pages and some old pages after an interrupted write;
2. a **rollback journal**, containing original page images and the original database size;
3. a **journal header**, whose validity participates in whether the journal is rollback-eligible;
4. process / operating-system **lock state**, which participates in determining whether a journal is `hot`;
5. for multi-database transactions, a **super-journal** containing the names of participating rollback journals, while each rollback journal contains the super-journal name.

These are not interchangeable copies of the database. The rollback journal is selective old-state recovery evidence; the super-journal is a relation among journals, not another store of page payload.

The central decomposition is:

```text
main-file bytes
    !=
rollback page images
    !=
journal validity
    !=
hot-journal recovery authority
    !=
transaction commit state
```

---

## Mechanism 1 — Before overwriting current pages, retain enough old state to undo

SQLite's atomic-commit documentation says that before changing database pages in the main database file, SQLite writes the original content of pages that will be modified into a rollback journal. The journal also records the original database size so a database that grew during an interrupted transaction can be truncated back to its prior size.

SQLite then flushes the rollback journal to nonvolatile storage before changing the main database file. The project documentation treats this ordering as critical to surviving power loss.

The mechanism is therefore **undo-oriented**:

```text
old current page
    -> copy old page into rollback journal
    -> make rollback evidence durable enough for the promised model
    -> allow main-file page to be overwritten
```

This differs from a write-ahead redo log that primarily retains operations or new values for later replay.

Engineering reconstruction:

> **the ability to overwrite current state safely is purchased by temporarily retaining an older recoverable state.**

That older state is not an archive. Its liveness is bounded by the transaction/recovery protocol.

---

## Mechanism 2 — A journal file is not recovery-authoritative merely because bytes exist

SQLite defines a **hot journal** relationally. In the maintained Version-3 locking documentation, a rollback journal is hot only when conditions such as the following hold:

- the journal exists;
- it is large enough to contain meaningful content;
- its header is non-zero and well formed;
- its super-journal exists, or the journal names no super-journal;
- there is no `RESERVED` lock on the corresponding database file.

The exact list matters. It means:

> **rollback-journal physical presence != hot-journal status.**

A valid-looking sequence of old page images is not sufficient by itself. Recovery authority depends on retained metadata and on the journal's relationship to the corresponding database / transaction state.

This becomes even clearer in `PERSIST` mode: the journal file may deliberately remain present after commit, but zeroing its header prevents later rollback. Old page-image bytes may therefore remain in the file while the protocol has withdrawn their status as live recovery evidence.

So:

> **physical survival of prior-state bytes != current admissibility as rollback state.**

That is a direct storage-system example of why forensic survivability and authoritative currentness must remain separate.

---

## Mechanism 3 — A hot journal can make the main file temporarily non-authoritative for reads

After a crash or power loss, the main database file may be internally inconsistent because only part of a transaction reached it. SQLite's locking document says that before reading, a connection checks for a hot journal. If one is present, SQLite acquires stronger locks, copies original pages from the journal back into the database, flushes the restored database state, and only then retires the hot journal.

Thus:

> **main database file exists != main database file is immediately safe to interpret as the current logical database.**

The retained rollback relation can temporarily outrank the apparent newest bytes in the main file. Recovery reconstructs the pre-transaction state rather than treating whichever sectors happen to be newest as authoritative.

The future operation that matters is not merely "read these bytes." It is:

```text
detect recovery obligation
    -> establish exclusive recovery authority
    -> restore prior page state
    -> persist restored state
    -> retire rollback authority
    -> admit ordinary reads
```

This is recovery-mediated currentness.

---

## Mechanism 4 — Commit can be a withdrawal of rollback authority

SQLite's atomic-commit documentation makes a particularly useful retention distinction. In the default `DELETE` rollback mode, once database changes have been flushed, deleting the rollback journal is the event SQLite treats as the commit point.

The project documentation is careful: file deletion is not physically instantaneous in some absolute sense; it is used because from the user-process interface the journal's existence can be observed as yes/no under SQLite's assumptions.

The later `PERSIST` and `TRUNCATE` modes show that **journal-file deletion itself is not the essence of the logical transition**:

- `DELETE`: remove the journal file;
- `TRUNCATE`: reduce it to zero length;
- `PERSIST`: keep the file but invalidate the journal header, normally by overwriting it with zeros.

All three can establish the same higher-level result: the prior rollback material no longer qualifies as a live journal capable of undoing the transaction.

Therefore:

> **commit != one universal physical deletion operation.**

More precisely:

> **commit currentness can be established by making prior recovery evidence inadmissible.**

This is an engineering reconstruction of the documented protocol, not SQLite's own philosophical vocabulary.

It also creates a strong anti-forensics boundary:

> **rollback authority retired != old page bytes securely erased.**

`PERSIST` is the explicit counterexample: the file may remain, yet its header invalidation changes its operational status.

---

## Mechanism 5 — Multi-database atomicity depends on a retained reference graph

For a transaction spanning multiple `ATTACH`ed databases, SQLite gives each database its own rollback journal and adds a **super-journal**. The super-journal stores the names of the individual journals; each individual journal stores the name of the super-journal.

The super-journal contains no original database page images. Its role is relational.

Before commit:

```text
super-journal exists
    <-> individual journals name it
    -> those journals remain hot if other hotness conditions hold
```

The SQLite documentation identifies deletion of the super-journal as the multi-file commit point. Crucially, after the super-journal is deleted, the individual rollback-journal files can still physically exist for cleanup, yet they are no longer considered hot because the super-journal they name no longer exists.

This yields one of the cleanest relations in the repository:

> **rollback bytes can survive while the reference that grants them cross-database recovery authority disappears.**

And:

> **multi-object commit state can depend on a small retained graph of names, not on duplicating all payload into one master record.**

The super-journal is therefore neither a payload replica nor a complete history. It is commit/recovery coordination state.

---

## Mechanism 6 — Stale metadata can survive after its operational liveness ends

SQLite's locking documentation describes **stale super-journals**. A super-journal is stale when no individual rollback journal still points to it; deleting such a stale super-journal is optional cleanup used to reclaim disk space.

This separates:

`metadata physical presence != metadata operational liveness != reclamation completion`

The system does not have to erase an obsolete coordination object at the instant it ceases to matter. A later liveness check can prove that no current rollback relation depends on it and only then reclaim it.

That is functionally comparable to other repository cases in which currentness is retired before physical reclamation, but the SQLite mechanism is namespace/reference based rather than Flash-translation or distributed-replica based.

---

## Mechanism 7 — Recovery evidence must remain paired with the database it qualifies

SQLite's current **How To Corrupt An SQLite Database File** documentation gives a blunt operational warning: after a failed write transaction, a hot rollback journal must be kept with its database; moving, deleting, renaming, mismatching, or copying the database without its hot journal can defeat automatic recovery and lead to corruption.

This gives a relational identity boundary:

> **database bytes + unrelated journal bytes != recoverable database state.**

and:

> **recovery evidence survival != recovery relation survival.**

The journal must remain paired with the database whose earlier pages it records. Retaining both byte sequences somewhere is not enough if the naming/location relation needed to associate them is broken.

This complements Case 124's directory-durability finding. Case 124 shows that durable file contents may still lack a durable namespace binding after rename; Case 143 shows that a recovery protocol may depend on retaining the **correct binding between main state and recovery evidence**.

---

## Failure model and stop conditions

This case does not universalize SQLite's durability assumptions.

The project documentation itself says the pager depends on operating-system locking and flush primitives behaving as advertised. It discusses failure modes involving broken locking, incomplete flushes, volatile device caches, filesystem behavior, and deletion/separation of hot journals.

Therefore:

> **documented rollback protocol != empirical proof for every filesystem/controller/power-loss combination.**

Likewise:

- journal deletion/truncation/header invalidation is **not secure sanitization**;
- rollback is **not backup**;
- a hot journal is **not a long-term version history**;
- the super-journal is **not a payload replica**;
- rollback mode is **not WAL mode**;
- the case does not prove that every current SQLite build follows one identical syscall trace on every VFS;
- the maintained project docs are authoritative design references but not frozen facsimiles of every 2004 implementation detail.

Power-cut / fault-injection reproduction remains separate experimental work.

---

## Cross-case comparison

### Case 124 — ext4 / PostgreSQL durable rename boundary

[`Case 124`](124-linux-ext4-rename-fsync-durability-closure.md) shows that file-content durability and namespace durability can diverge and that a recovery identity relation may require directory persistence.

Case 143 adds:

> **correct recovery bytes != correct recovery pairing/admissibility.**

SQLite can have both main-file and journal bytes physically present while their name/header/super-journal/lock relations determine whether rollback is required.

This is functional comparison, not genealogy.

### Case 137 — LevelDB MANIFEST/CURRENT

[`Case 137`](137-leveldb-v17-manifest-current-recovery.md) uses `CURRENT` and MANIFEST replay to determine the current serving version, while old SSTables can remain physically present.

SQLite rollback mode uses a different direction of authority: it retains old page images so that an interrupted overwrite can be undone, then commits by withdrawing rollback eligibility.

Functional contrast:

`select current reconstructed metadata state` (LevelDB)

versus

`retain prior page state until rollback authority is withdrawn` (SQLite).

### Case 74 — JBD/JBD2 revoke

[`Case 74`](74-linux-jbd-revoke-suppress-stale-replay.md) shows recovery metadata suppressing stale journal replay for blocks whose later use changes replay admissibility.

SQLite hot-journal logic also separates stored recovery material from admissibility, but the historical mechanisms differ. No JBD -> SQLite genealogy is claimed.

### Case 44 — sanitization

[`Case 44`](44-nvme13-deallocate-sanitize-forgetting.md) is a useful stop condition. SQLite `PERSIST` can invalidate rollback authority while prior page bytes remain physically present. That is almost the inverse of a sanitize claim:

`no longer rollback-authoritative != media data made inaccessible`.

A transaction commit is not a sanitization operation.

---

## Controlled conceptual interpretation

### Engineering reconstruction

The bounded mechanism supports three project-level statements:

1. **safe destructive update can require temporary retention of an earlier recoverable state;**
2. **recovery authority is relational, not reducible to the physical presence of journal bytes;**
3. **commit can be implemented as a change in which retained state remains admissible for future recovery.**

### Functional analogy

A hot journal is functionally similar to other retained recovery evidence only in the narrow sense that later operations inspect small state to decide how to reconstruct or qualify a larger state.

It is not historically identical to:

- a database WAL;
- a filesystem journal;
- a Flash translation map;
- a replica tombstone;
- a snapshot;
- a sanitize status log.

### Philosophical interpretation

The most defensible philosophical observation is limited:

> **technical persistence can depend not only on which traces survive, but on retained relations that say which trace is still entitled to count in a future operation.**

SQLite's `PERSIST` mode is especially useful because physical journal survival and rollback authority visibly diverge.

This does not make the journal a model of human memory, does not make commit equivalent to forgetting in the psychological sense, and does not turn every transaction protocol into tertiary retention.

---

## Related-repository boundary

A fresh recursive-tree search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated SQLite / rollback-journal case.

If developed later, the following belong primarily there:

- SQLite 2 -> SQLite 3 pager/locking genealogy;
- exact 2004 source-level pager evolution;
- VFS and filesystem-portability history;
- PERSIST/TRUNCATE implementation genealogy;
- WAL-mode evolution after 2010;
- named platform/device crash behavior.

`technical-retention` keeps the narrower cross-mechanism question: **how old page images, journal validity, reference relationships, and commit transitions determine which surviving state remains admissible for recovery.**

---

## Open work

- recover a frozen early-2004/3.0.x source/document snapshot for exact line-level comparison against maintained documentation;
- identify the exact introduction genealogy of the super-journal implementation rather than relying only on the Version-3 maintained design record and 3.0.0 release note;
- deepen the PERSIST introduction from release note into source/check-in history if a later argument depends on exact implementation chronology;
- compare rollback-journal and WAL-mode currentness only in a separate bounded case;
- run controlled power-cut / VFS fault experiments for DELETE/PERSIST/TRUNCATE;
- test database+journal rename/copy/mispairing failure modes in an isolated experiment;
- keep filesystem and device durability claims routed through Cases 124/15/31 rather than silently assuming `fsync` closes every lower layer.

## Sources

Primary SQLite project sources:

- SQLite, **File Locking And Concurrency In SQLite Version 3**: <https://www.sqlite.org/lockingv3.html>
- SQLite, **Atomic Commit In SQLite**: <https://www.sqlite.org/atomiccommit.html>
- SQLite, **Database File Format — rollback journal**: <https://www.sqlite.org/fileformat.html>
- SQLite, **PRAGMA journal_mode**: <https://www.sqlite.org/pragma.html#pragma_journal_mode>
- SQLite, **How To Corrupt An SQLite Database File**: <https://www.sqlite.org/howtocorrupt.html>
- SQLite, **Release 3.0.0 — 2004-06-18**: <https://www.sqlite.org/releaselog/3_0_0.html>
- SQLite, **Release 3.5.9 — 2008-05-14**: <https://www.sqlite.org/releaselog/3_5_9.html>
- SQLite, **Release 3.6.4 — 2008-10-15**: <https://www.sqlite.org/releaselog/3_6_4.html>
- SQLite, **Write-Ahead Logging**, used only to bound WAL's 3.7.0 introduction and difference from rollback mode: <https://www.sqlite.org/wal.html>
