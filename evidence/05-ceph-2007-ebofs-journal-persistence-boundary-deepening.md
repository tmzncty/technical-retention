# Case 05 evidence deepening — Ceph 2007 EBOFS journal / persistence-boundary semantics

**Status:** bounded deepening complete

**Case:** [`cases/05-rados-replicated-object-repair.md`](../cases/05-rados-replicated-object-repair.md)

**Follow-on to:** [`05-ceph-2007-osdmap-restart-persistence-deepening.md`](05-ceph-2007-osdmap-restart-persistence-deepening.md)

**Bounded question:** In the September 2007 Ceph implementation used by the preceding OSDMap-restart slice, what did the local EBOFS layer distinguish between an update being applied, a journal record being queued, a journal record becoming replayable / `onsafe`, an EBOFS epoch being checkpointed, and a later restart replaying the update? What does that let us say — and not say — about the separately written OSDMap blobs and the later OSD superblock / PG-state transaction?

This is **not** a general history of EBOFS, filesystem journaling, Ceph crash consistency, or block-device durability. It closes only the local persistence-boundary debt exposed by the September-2007 OSDMap source inspection.

---

## 1. Why this slice exists

The preceding Case 05 deepening established a useful representation-level distinction:

```text
OSDMap object exists locally
    !=
superblock.current_epoch selects / admits that map as processed state
```

The source also exposed a suspiciously important ordering fact. `OSD::handle_osd_map()` stores incoming full and incremental map objects with direct `store->write(...)` calls **outside** the later `ObjectStore::Transaction`; only afterward does it update PG state, write the OSD superblock into that transaction, and call `store->apply_transaction(t)`.

That earlier note deliberately refused to infer an exact crash outcome because it had not yet inspected the contemporaneous EBOFS lower layer.

This slice asks only enough of EBOFS to sharpen that boundary.

The result is not a universal crash-consistency theorem. It is a source-level staging model:

```text
runtime / cache application
    != journal submission
    != complete journal record / safe callback
    != EBOFS epoch checkpoint
    != higher-layer distributed commit
```

For the map-update path specifically, the code also supports:

```text
map-object write call
    != later OSD superblock + PG-state transaction
```

Those two calls can be ordered without being one atomic ObjectStore transaction.

---

## 2. Source custody and chronology

### 2.1 Architectural source — OSDI 2006

Sage A. Weil et al., **“Ceph: A Scalable, High-Performance Distributed File System,”** OSDI '06, November 2006.

USENIX publication record:

<https://www.usenix.org/conference/osdi-06/ceph-scalable-high-performance-distributed-file-system>

Full HTML:

<https://www.usenix.org/legacy/events/osdi06/tech/full_papers/weil/weil_html/>

Section 5.3 explicitly separates early acknowledgement after updates reach the OSDs' in-memory buffer caches from a later final `commit` after the update is safely committed to disk.

Section 5.6 says EBOFS was designed with update semantics that separate **update serialization (for synchronization)** from **on-disk commits (for safety)**.

This paper is an architectural / historical vocabulary witness. It is **not** used as proof of the exact June–September 2007 source implementation below.

### 2.2 EBOFS journaling implementation introduction — June 2007

Ceph public Git history preserves the earlier SourceForge SVN history.

Two useful implementation landmarks are:

- `3a020592356ef9ded943fffdabfb0ecde5666db5`
  - 1 June 2007
  - mirrored SVN revision `@1386`
  - commit message: `* beginnings of ebofs journaling`
- `da3a11dd833ba756b7e9ca6e7bc8e04be91eacc2`
  - 20 June 2007
  - mirrored SVN revision `@1432`
  - commit message: `* simple ebofs journaling, yay!`

The second commit already contains the essential shape later present in September: journal replay on mount, transaction encoding into journal entries, commit-epoch coordination, and `onsafe` callbacks.

Commit:

<https://github.com/ceph/ceph/commit/da3a11dd833ba756b7e9ca6e7bc8e04be91eacc2>

### 2.3 Main implementation snapshot — 5 September 2007

This note uses the same snapshot as the OSDMap-restart deepening:

- `c93efe01c518c2e90ba62245352baaac5fa675f2`
- 5 September 2007
- mirrored SVN revision `@1787`
- commit message: `stupid hack to pull osdmaps out of an osd store`

Commit:

<https://github.com/ceph/ceph/commit/c93efe01c518c2e90ba62245352baaac5fa675f2>

Relevant files at that revision:

- `trunk/ceph/osd/OSD.cc`
  - <https://github.com/ceph/ceph/blob/c93efe01c518c2e90ba62245352baaac5fa675f2/trunk/ceph/osd/OSD.cc>
- `trunk/ceph/ebofs/Ebofs.cc`
  - <https://github.com/ceph/ceph/blob/c93efe01c518c2e90ba62245352baaac5fa675f2/trunk/ceph/ebofs/Ebofs.cc>
- `trunk/ceph/ebofs/FileJournal.cc`
  - <https://github.com/ceph/ceph/blob/c93efe01c518c2e90ba62245352baaac5fa675f2/trunk/ceph/ebofs/FileJournal.cc>
- `trunk/ceph/ebofs/FileJournal.h`
  - <https://github.com/ceph/ceph/blob/c93efe01c518c2e90ba62245352baaac5fa675f2/trunk/ceph/ebofs/FileJournal.h>

### Chronological caution

The OSDI paper predates the inspected journaling commits. The paper establishes the design distinction between synchronization and safety; the 2007 source establishes one implementation of local persistence staging.

Nothing here proves that the exact September code existed in the November-2006 prototype, and nothing here is a statement about modern Ceph / BlueStore.

---

## 3. Historical record — the OSD map path really is split into separate ObjectStore calls

At `c93efe01...`, `OSD::handle_osd_map()` first loops over incoming full maps and incremental maps.

For a previously unseen full map it executes:

```cpp
store->write(oid, 0, p->second.length(), p->second, 0);
```

The source comment is unusually explicit:

```text
store _outside_ transaction; activate_map reads it.
```

The incremental-map path does the same thing.

Only after those direct writes does the OSD:

1. advance `superblock.current_epoch` while applying available epochs;
2. update PG state;
3. add per-PG `info` attributes to an `ObjectStore::Transaction`;
4. add the OSD superblock through `write_superblock(t)`;
5. call `store->apply_transaction(t)`.

Both direct map writes pass a null completion context (`0`). The final transaction is also submitted without an `onsafe` context in this path.

### Historical claim

**The September-2007 map path intentionally separated incoming map-object writes from the later superblock / PG-state transaction.**

The source therefore does not justify this model:

```text
map bytes
+ processed epoch marker
+ updated PG info
    = one ObjectStore atomic transaction
```

They are not submitted as one ObjectStore transaction.

### Important limit

Separate submission does not by itself tell us the exact physical media state after a power failure. That requires the EBOFS journal/checkpoint semantics inspected below and, below that, the block-device / hardware persistence behavior that remains outside this slice.

---

## 4. Historical record — `apply_transaction()` applies first and journals afterward

At the September snapshot, `Ebofs::apply_transaction(Transaction& t, Context *onsafe)` does the following under the EBOFS lock:

1. calls `_apply_transaction(t)`;
2. if a journal exists, encodes the transaction;
3. calls `journal->submit_entry(bl, onsafe)`;
4. otherwise, if `onsafe` exists, places it in the current epoch's `commit_waiters`;
5. unlocks and returns.

The crucial order is therefore:

```text
_apply_transaction(t)
    ↓
submit journal entry / register later commit waiter
    ↓
return to caller
```

### Historical claim

**At this revision, `apply_transaction()` returning is not itself the source-level safe-completion event.**

The function can return after the transaction has been applied to EBOFS's working state and queued to the journal, while the journal writer thread is still responsible for writing the queued record.

That distinction is already consistent with the OSDI paper's architectural separation of update serialization / visibility from on-disk safety.

### Null `onsafe` matters

The inspected `handle_osd_map()` path does not pass an `onsafe` callback for either the direct map writes or the final transaction.

Therefore the higher-level function is **not synchronously waiting on the local safe-notification mechanism visible in this API**.

This does not mean the updates are never made durable. It means that the return from those calls cannot be equated with the `onsafe` milestone merely by reading the call site.

---

## 5. Historical record — `submit_entry()` queues; it does not synchronously write the entry

`FileJournal::submit_entry()` holds the journal write lock, checks space/wrap conditions, then appends:

```text
(current super_epoch, encoded transaction)
```

to `writeq`, appends the corresponding callback to `commitq`, advances `queue_pos`, signals the writer thread, and returns `true`.

The actual file writes happen in `FileJournal::write_thread_entry()`.

### Historical claim

There are at least two distinct local states:

```text
journal entry accepted into write queue
    !=
journal entry completely written by writer thread
```

The code's `queue_pos` and `write_pos` are separate precisely because queued progress and completed writer progress are not identical.

This gives a stronger boundary than the generic word `journaled` often suggests. A transaction can be **designated for journaling** before its journal record is fully materialized.

---

## 6. Historical record — a journal entry is framed as header + body + footer

The September `FileJournal` writes each record as:

```text
entry header
encoded transaction body
entry footer (same header fields / magic relation)
```

The header includes:

- epoch;
- length;
- two magic values derived from position, filesystem id, epoch, and length.

On replay, `read_entry()`:

1. reads the leading header;
2. validates its magic;
3. reads the body;
4. reads the trailing footer;
5. validates footer magic and checks epoch/length agreement with the header.

If the header is invalid, or if the footer does not validate / match, `read_entry()` returns `false` and replay stops at that point.

### Historical claim

**The journal contains an explicit record-completeness test. A partially framed tail record is not treated as a valid transaction to replay.**

This is stronger than merely saying “EBOFS has a log.” The format itself distinguishes a complete replay candidate from an incomplete tail.

### Bounded consequence

At the journal-format level, restart replay is naturally **prefix-like**:

```text
complete validated entry 1
complete validated entry 2
...
first incomplete / invalid tail
    -> stop replay here
```

This is a property of the inspected journal reader. It is not yet a universal statement about all hardware failure modes.

---

## 7. Historical record — the journal file is opened with `O_SYNC`

`FileJournal::create()` and `FileJournal::open()` use:

```cpp
::open(fn.c_str(), O_RDWR|O_SYNC)
```

After the writer thread finishes the header/body/footer writes for one queued entry, it queues the corresponding `oncommit` callback through EBOFS's finisher machinery.

### Historical claim

The implementation **intends** the completed journal write to be a local persistence / safe-notification boundary stronger than mere queue admission.

That intention is reinforced by the naming of the callback path (`oncommit`) and by the 2006 architectural distinction between synchronization and safety.

### Required limit

`O_SYNC` is an operating-system interface request. This slice does **not** independently validate:

- drive write-cache honesty;
- power-loss behavior of a specific disk/controller;
- barrier/flush implementation in the underlying kernel/device stack;
- whether every 2007 deployed system provided the same persistence guarantee.

Therefore the defensible wording is:

> **complete `O_SYNC` journal write / queued `oncommit` callback is the implementation's local safe milestone, not independently verified proof of nonvolatile hardware persistence under every failure model.**

---

## 8. Historical record — EBOFS also has a later full epoch checkpoint

The EBOFS commit thread maintains `super_epoch`.

For a dirty epoch it:

1. increments `super_epoch`;
2. calls `journal->commit_epoch_start()` when a journal exists;
3. starts flushing inode/object-table/B-tree related state;
4. uses the block-device barrier path;
5. waits for dirty buffer-cache, inode, and node-pool work;
6. prepares and writes the EBOFS filesystem superblock for the epoch;
7. calls `journal->commit_epoch_finish()`;
8. releases the earlier epoch's `commit_waiters` and signals sync waiters.

`write_super()` alternates the EBOFS superblock between block 0 and block 1 according to `epoch & 1`.

On mount, EBOFS reads both superblocks and chooses the one with the larger epoch.

### Historical claim

EBOFS represents another persistence stage beyond an individual journal entry:

```text
individual operation recoverable from journal
    !=
operation absorbed into a completed EBOFS epoch checkpoint
```

The checkpoint permits old journal epochs to be retired because the filesystem's main structures have advanced to a newer durable checkpoint state.

### Do not confuse the two superblocks

This note discusses two differently scoped things named `superblock`:

1. **EBOFS filesystem superblocks** at raw blocks 0/1, carrying EBOFS epoch/table roots;
2. **Ceph OSD `OSDSuperblock`**, stored as an ObjectStore object and carrying `whoami`, `current_epoch`, `oldest_map`, `newest_map`, etc.

They are not the same structure and must not be collapsed.

---

## 9. Historical record — mount checkpoint selection and journal replay are distinct phases

During `Ebofs::mount()` the code:

1. reads EBOFS superblocks 0 and 1;
2. selects the newer EBOFS `super_epoch`;
3. opens the object/index tables from that checkpoint;
4. opens the journal;
5. reads journal entries starting at a header-selected position;
6. skips records older than the selected checkpoint epoch;
7. advances one epoch when the next journal epoch is encountered;
8. decodes each accepted transaction and calls `_apply_transaction(t)`;
9. stops at the end / invalid tail;
10. makes the journal writable again.

### Historical claim

**Restart is not “load one final image.” It is checkpoint selection plus qualified replay of later retained transactions.**

For this local layer:

```text
checkpoint state
+ replayable journal suffix
    -> reconstructed EBOFS working state
```

The relation is operationally similar to other log/checkpoint systems in the repository, but the exact authority and commit semantics remain EBOFS-specific.

---

## 10. Engineering reconstruction — five local stages should remain separate

The source supports the following project-level decomposition:

```text
1. working-state application
   _apply_transaction() changes EBOFS in-memory/cached structures

2. journal admission
   encoded transaction is accepted into FileJournal writeq

3. replayable / safe journal materialization
   complete framed record is written; oncommit may be released

4. epoch checkpoint absorption
   dirty data/metadata structures are flushed and newer EBOFS superblock is written

5. restart reconstruction
   newest EBOFS checkpoint is selected and complete later journal entries are replayed
```

These are engineering-reconstruction labels, not period Ceph terminology.

The crucial rule is:

> **progress through one stage must not be silently promoted into completion of a later stage.**

So:

```text
transaction applied
    != safe callback reached

journal entry queued
    != complete replayable journal record

complete journal record
    != absorbed into EBOFS checkpoint

EBOFS locally recoverable
    != RADOS distributed commit complete
```

---

## 11. Engineering reconstruction — a prefix between map write and OSD-state transaction is representable

The map path submits the map-object write first and the OSD superblock / PG-state transaction later.

The FileJournal writer processes queued entries in list order. The replay reader accepts complete framed entries and stops at an invalid/partial tail.

That combination supports a bounded statement about the **state space represented by the implementation**:

```text
entry A: map-object write
entry B: later OSD superblock + PG-info transaction

possible replayable journal prefix shape:
    A complete
    B not complete / not replayable
```

This is exactly the kind of shape that makes the earlier representation distinction operationally meaningful:

```text
map bytes can be present/replayable
    while
processed/current epoch marker is not yet replayable from the later transaction
```

### Why the wording is deliberately cautious

This note says **representable by the journal protocol**, not “guaranteed physical crash outcome at source line X.”

A stronger claim would require independently establishing:

- exact lower-level persistence of each synchronous file write under the specific storage stack;
- device-cache flush semantics;
- exact timing of crash relative to writer thread and EBOFS epoch checkpoint;
- whether the separate journal file and raw EBOFS device have any additional ordering/failure coupling.

Still, this source inspection closes the earlier debt enough to reject the opposite overclaim:

```text
because handle_osd_map() called map write and superblock transaction sequentially,
those states must always become crash-persistent atomically
```

The implementation does not provide that cross-call atomicity at the ObjectStore transaction level.

---

## 12. Engineering reconstruction — call order, transaction scope, and persistence scope are different relations

The inspected source makes three forms of ordering visible:

### 12.1 Program-order submission

The OSD submits direct map writes before the final transaction.

### 12.2 ObjectStore transaction grouping

PG `info`, newly encoded full maps generated during incremental advancement, and the OSD superblock can be grouped in `t` and passed to one `apply_transaction()` call.

The earlier received-map writes are not in that transaction.

### 12.3 Local persistence progression

Journal records are asynchronously written and later absorbed into EBOFS epoch checkpoints.

These are not interchangeable:

```text
called earlier
    != same transaction

same transaction
    != caller waited for onsafe

caller returned
    != epoch checkpoint complete
```

This is a useful general retention lesson: **program order is not itself a persistence contract**.

---

## 13. Engineering reconstruction — `onsafe` is evidence about completion, not merely a callback convenience

The EBOFS interface makes a semantic distinction visible by accepting a `Context *onsafe`.

With the journal active, that callback is associated with the queued journal record and released by the journal writer after the record's writes complete. Without the journal, the callback is retained until the relevant EBOFS commit epoch completes.

Therefore `onsafe` belongs to the repository's growing family of **completion evidence** mechanisms:

```text
operation requested
    != operation applied
    != completion evidence produced
```

But the map-processing call site deliberately passes `0`, so no higher-level local safe acknowledgement is awaited there.

This distinction should not be inflated into an end-to-end RADOS statement. Other request paths can and do use completion machinery differently.

---

## 14. Engineering reconstruction — local recoverability is only one layer of distributed retention

Even after this deepening, Case 05 retains several different layers:

```text
local EBOFS operation state
    ↓
local journal / checkpoint recoverability
    ↓
OSD restart-selected map / PG history state
    ↓
live monitor map reconciliation
    ↓
PG peering / content-currentness reconstruction
    ↓
replica repair / desired redundancy restoration
```

A lower layer can succeed without a higher layer being complete.

Examples:

- the map object may survive locally while the cluster has already advanced to a newer epoch;
- a locally selected map may be restart-legible but still stale globally;
- local PG logs may survive while peering is unfinished;
- a PG may become serviceable while full replica repair remains outstanding.

So:

> **local crash recoverability is constitutive of distributed retention, but it is not identical to distributed currentness or redundancy restoration.**

---

## 15. Functional analogy — SQLite WAL, explicitly bounded

Case 152's SQLite WAL evidence provides a useful **functional analogy** only.

Both systems can be decomposed into:

```text
working-state mutation
    != retained log/journal evidence
    != checkpoint absorption
    != restart reconstruction
```

But the analogy stops quickly.

SQLite WAL has its own commit-marker, reader-snapshot, checkpoint, and database-file authority semantics. EBOFS in this 2007 Ceph source is a local object-store implementation beneath a distributed OSD protocol, with separate Ceph OSD superblock / PG state layered above it.

This note does **not** claim:

- shared implementation;
- direct historical influence;
- equivalent transaction semantics;
- equivalent crash guarantees.

The comparison is useful only because it prevents the project from treating the word `journal` as one universal mechanism.

---

## 16. Philosophical interpretation — persistence has staged predicates

The exact technical fact creating the conceptual problem is simple:

> one update can successively be applied, queued for retention, made replayable, checkpointed, reconstructed after restart, and later admitted as current in a distributed protocol.

The conceptual lesson is not that persistence is “illusory.”

It is that **`the state remains` is incomplete unless the persistence boundary and failure model are named**.

For this bounded case, `having happened` can refer to several technically real but non-equivalent predicates:

```text
happened in working state
happened in replayable local evidence
happened in checkpointed local state
happened in restart-reconstructed state
happened in distributed current state
```

The interpretation stops at that decomposition. It does not turn EBOFS into a universal metaphysics of memory.

---

## 17. Explicit non-claims

This note does **not** claim any of the following:

1. that `apply_transaction()` return proves physical nonvolatile persistence;
2. that `store->write()` return proves physical nonvolatile persistence;
3. that `O_SYNC` defeats every disk/controller volatile cache or dishonest flush implementation;
4. that every 2007 Ceph deployment used identical hardware / kernel persistence semantics;
5. that map-object write and OSD superblock transaction are one ObjectStore atomic transaction;
6. that source-level call order proves a precise hardware crash state for every interruption point;
7. that the map blob must survive whenever the later superblock does;
8. that the later superblock must be lost whenever a map blob survives;
9. that an EBOFS journal entry is identical to an EBOFS epoch checkpoint;
10. that a complete journal record proves the transaction has already been absorbed into the main EBOFS structures on disk;
11. that an EBOFS filesystem superblock is the same object as Ceph's `OSDSuperblock`;
12. that locally recovered OSDMap state is globally current cluster state;
13. that local EBOFS recoverability proves PG peering completion;
14. that local EBOFS recoverability proves desired replica count restored;
15. that this source describes modern Ceph, BlueStore, FileStore, or current messenger/OSD semantics;
16. that the June 2007 journaling implementation was present unchanged in the November-2006 OSDI prototype;
17. that this is a general history of write-ahead logging or journaling;
18. that EBOFS and SQLite WAL share a historical genealogy;
19. that a null `onsafe` means an operation will never become durable;
20. that a non-null `onsafe` is independent end-to-end proof against every hardware failure model.

---

## 18. Claim ledger

| Claim | Type | Evidence | Strength |
|---|---|---|---|
| OSDI 2006 explicitly separates synchronization/visibility from on-disk safety | Historical record | OSDI 2006 §§5.3, 5.6 | strong |
| EBOFS journaling appears in public source by June 2007 | Historical record | commits `3a020592...`, `da3a11dd...` | strong |
| September-2007 `handle_osd_map()` writes received maps outside the later transaction | Historical record | `OSD.cc` @ `c93efe01...` | strong |
| direct map writes and final map-state transaction use null `onsafe` in this path | Historical record | `OSD.cc` @ `c93efe01...` | strong |
| `apply_transaction()` applies working state before journal submission | Historical record | `Ebofs.cc` @ `c93efe01...` | strong |
| `submit_entry()` queues work; writer thread performs later file writes | Historical record | `FileJournal.cc` @ `c93efe01...` | strong |
| journal entry uses validated header/body/footer framing | Historical record | `FileJournal.h/.cc` @ `c93efe01...` | strong |
| replay stops at an invalid / partial record tail | Historical record | `FileJournal::read_entry()` | strong |
| journal is opened with `O_SYNC` | Historical record | `FileJournal::create/open()` | strong |
| EBOFS later flushes main structures, writes an epoch superblock, then retires committed journal epochs | Historical record | `Ebofs::commit_thread_entry()` | strong |
| mount selects newest EBOFS checkpoint then replays eligible journal entries | Historical record | `Ebofs::mount()` | strong |
| map presence and OSD processed-epoch state can occupy different local retention stages | Engineering reconstruction | ordered separate calls + journal framing/replay | strong, bounded |
| program-order submission is not cross-call transaction atomicity | Engineering reconstruction | OSD call structure + ObjectStore transaction scope | strong |
| a replayable prefix ending after map write but before later OSD-state transaction is representable by journal semantics | Engineering reconstruction | FIFO writer + validated prefix replay + call order | strong as representation/state-space claim; not hardware outcome proof |
| EBOFS local safe/checkpoint state is not RADOS distributed commit/currentness | Engineering reconstruction | EBOFS source + OSDI protocol layers | strong |
| EBOFS and SQLite WAL share only a staged-retention functional pattern | Functional analogy | Cases 05 / 152 | bounded |
| persistence requires naming the relevant boundary/failure model | Philosophical interpretation | mechanism decomposition above | bounded |

---

## 19. What this closes from the previous OSDMap note

The previous OSDMap-restart evidence left open the statement:

> exact power-failure outcomes require contemporaneous ObjectStore/EBOFS durability, writeback, ordering, and transaction semantics.

This slice **partly closes that debt at the source-model level**.

We can now say directly that:

```text
map writes are separate earlier ObjectStore calls
final OSD superblock/PG update is a later transaction
EBOFS applies before it journals
journal admission precedes writer completion
complete records are independently replay-qualified
checkpoint absorption is later still
```

That is enough to reject cross-call atomicity and to explain why `map blob present != processed/current epoch persisted` is more than a purely structural distinction.

It does **not** close device-level crash validation.

---

## 20. Remaining evidence debt

The remaining work is narrower and should not expand this case into a general EBOFS history.

### 20.1 Block-device / hardware persistence validation

Inspect the contemporaneous `BlockDevice` implementation only if a future claim needs exact semantics for:

- `dev.barrier()`;
- raw-device write completion;
- cache flush / ordering;
- kernel and disk write-cache behavior.

Source inspection alone still cannot validate real hardware honesty under sudden power loss.

### 20.2 Fault-injection / reconstruction experiment

A historically pinned build, if practical, could test selected crash points around:

```text
map write
journal writer completion
final OSD-state transaction
EBOFS epoch checkpoint
```

Such an experiment would be an **Experiment** claim, not historical evidence of deployed failures.

### 20.3 Broader EBOFS genealogy

The full history of EBOFS journaling, later FileStore, production deployment, bug fixes, and replacement by later local stores belongs primarily in `computing-archaeology`.

A fresh companion-repository search for `EBOFS` did not reveal a dedicated reusable packet in this run.

---

## 21. Bounded result

The result can be summarized without pretending to have solved every crash case:

```text
OSD map message arrives
    ↓
received map object written through separate ObjectStore call
    ↓
EBOFS working state changes
    ↓
encoded operation queued to journal
    ↓
complete framed journal record may become replayable / safe
    ↓
later OSD map advancement updates PG info + OSDSuperblock in another transaction
    ↓
that transaction traverses the same local journal/checkpoint machinery
    ↓
EBOFS epoch checkpoint can later absorb journaled work
    ↓
restart selects checkpoint + replays complete later entries
```

Therefore:

> **map-object presence, processed-map admission, local replayability, local checkpoint completion, distributed currentness, and repaired redundancy are different retention predicates.**

And more narrowly:

> **the September-2007 implementation does not make the earlier map-object write and the later OSD superblock/PG-state update one atomic ObjectStore transaction; its journal/replay machinery can represent a complete-prefix state in which earlier retained work exists without a later transaction being replayable.**

The final sentence remains a source-level statement about the represented local state machine. Hardware-specific power-loss outcomes remain outside the claim.

---

## Sources

- Sage A. Weil, Scott A. Brandt, Ethan L. Miller, Darrell D. E. Long, Carlos Maltzahn, “Ceph: A Scalable, High-Performance Distributed File System,” OSDI '06, November 2006, especially §§5.3 and 5.6. USENIX: <https://www.usenix.org/conference/osdi-06/ceph-scalable-high-performance-distributed-file-system>; HTML: <https://www.usenix.org/legacy/events/osdi06/tech/full_papers/weil/weil_html/>.
- Ceph commit `3a020592356ef9ded943fffdabfb0ecde5666db5`, 1 June 2007, `beginnings of ebofs journaling`: <https://github.com/ceph/ceph/commit/3a020592356ef9ded943fffdabfb0ecde5666db5>.
- Ceph commit `da3a11dd833ba756b7e9ca6e7bc8e04be91eacc2`, 20 June 2007, `simple ebofs journaling, yay!`: <https://github.com/ceph/ceph/commit/da3a11dd833ba756b7e9ca6e7bc8e04be91eacc2>.
- Ceph commit `c93efe01c518c2e90ba62245352baaac5fa675f2`, 5 September 2007 / SVN r1787: <https://github.com/ceph/ceph/commit/c93efe01c518c2e90ba62245352baaac5fa675f2>.
- `OSD.cc` at `c93efe01...`, especially `handle_osd_map()`: <https://github.com/ceph/ceph/blob/c93efe01c518c2e90ba62245352baaac5fa675f2/trunk/ceph/osd/OSD.cc>.
- `Ebofs.cc` at `c93efe01...`, especially `mount()`, `write_super()`, `commit_thread_entry()`, and `apply_transaction()`: <https://github.com/ceph/ceph/blob/c93efe01c518c2e90ba62245352baaac5fa675f2/trunk/ceph/ebofs/Ebofs.cc>.
- `FileJournal.h` at `c93efe01...`: <https://github.com/ceph/ceph/blob/c93efe01c518c2e90ba62245352baaac5fa675f2/trunk/ceph/ebofs/FileJournal.h>.
- `FileJournal.cc` at `c93efe01...`, especially `open()`, `write_thread_entry()`, `submit_entry()`, `commit_epoch_finish()`, and `read_entry()`: <https://github.com/ceph/ceph/blob/c93efe01c518c2e90ba62245352baaac5fa675f2/trunk/ceph/ebofs/FileJournal.cc>.
