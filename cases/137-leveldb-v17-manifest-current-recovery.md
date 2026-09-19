# LevelDB v1.7 MANIFEST/CURRENT: Current-State Reconstruction, Version Liveness, and Obsolete-File Retirement

## Status

**`grounded`** — bounded primarily to Google LevelDB tag `v1.7` (`40768657bc8ec3ded60712eeeab7c25b1b07deca`, 16 October 2012 UTC) and its checked-in source/documentation, with an earlier **January 2012 `CURRENT` file-content sync fix** and a later 2013 namespace-durability report used as bounded historical deepenings. The case keeps file-content persistence, namespace publication, and old-root retirement ordering separate rather than treating them as one durability event.

Evidence navigation:

- baseline grounding: [`../evidence/137-leveldb-v17-manifest-current-grounding.md`](../evidence/137-leveldb-v17-manifest-current-grounding.md);
- January-2012 `CURRENT` content-sync fix: [`../evidence/137-leveldb-2012-current-content-sync-fix-deepening.md`](../evidence/137-leveldb-2012-current-content-sync-fix-deepening.md);
- CURRENT/rename namespace-durability deepening: [`../evidence/137-leveldb-v17-2013-current-rename-namespace-durability-deepening.md`](../evidence/137-leveldb-v17-2013-current-rename-namespace-durability-deepening.md).

This case does not claim that LevelDB invented LSM trees, manifests, write-ahead logging, tombstones, compaction, atomic rename, or crash-consistent metadata protocols.

## Scope

Case 57 establishes the Bigtable relation among commit log, volatile memtable, immutable SSTables, live-file metadata, redo points, and later compaction. Case 137 asks a narrower question in a bounded LevelDB release:

> When database state is represented by many immutable table files, what retained metadata makes a particular subset count as current after restart, how is that metadata itself selected, and when may physically surviving but superseded files finally be retired?

LevelDB v1.7 exposes three distinct retained histories/relations:

1. **user-update log files** (`*.log`) retain recent payload mutations for recovery;
2. **MANIFEST** is a metadata log whose `VersionEdit` records describe changes to the serving file set and recovery metadata;
3. **CURRENT** is a small indirection file naming which MANIFEST ordinary recovery should interpret.

Compaction creates new SSTables, records additions/deletions in MANIFEST, installs a new in-memory `Version`, and later permits obsolete physical files to be removed when they are no longer referenced by live Versions or pending output state.

The durability deepenings add a fourth boundary:

> a MANIFEST may be durably embodied as a file before the `CURRENT -> MANIFEST` designation has independently crossed its own crash-persistence frontier; within that designation path, selector-file **content synchronization** and final **namespace publication durability** are themselves different obligations.

This case is **not**:

- a general LevelDB/RocksDB history;
- a claim that `CURRENT` contains the current key/value database;
- a claim that MANIFEST is the user-data WAL;
- a proof that v1.7's `SetCurrentFile()` sequence is durably atomic on every filesystem/storage stack;
- a claim that the 2012 issue-68 failure reproduces on every OS/filesystem or that the 2013 rename/fsync issue reproduces on ext3/ext4 or every POSIX filesystem;
- a proof that an unreferenced/deleted SSTable is securely erased from underlying media;
- a claim that Bigtable, LevelDB, etcd, or PostgreSQL have identical recovery metadata or code lineage.

## Historical vocabulary

The inspected LevelDB v1.7 sources use:

- `log file` for recent user updates;
- `memtable`;
- `sorted table` / `sstable`;
- `level` / `level-0`;
- `MANIFEST` / `descriptor`;
- `CURRENT`;
- `Version` / `VersionSet`;
- `VersionEdit`;
- `current` version;
- `live files`;
- `pending_outputs_`;
- `compaction`;
- `deletion marker`;
- `DeleteObsoleteFiles()`;
- `Recover()`.

`current-state relation`, `membership authority`, `recovery graph`, `metadata-history compaction`, `root-pointer publication frontier`, `file-content persistence frontier`, and `namespace-persistence frontier` below are project engineering terms, not period LevelDB vocabulary.

---

## Historical / implementation record

### H/P — v1.7 separates user-update logs from the MANIFEST metadata log

The checked-in `doc/impl.html` says each `*.log` stores recent updates. It separately describes MANIFEST as a log of sorted-table membership, key ranges, and other metadata, with serving-state changes appended as files are added or removed. `CURRENT` is described as a small text file naming the latest MANIFEST.

Therefore:

```text
user-update log
    != MANIFEST serving-state log
    != CURRENT selector
```

### H/P — recovery begins at CURRENT and reconstructs file membership from the named MANIFEST

`VersionSet::Recover()` reads `CURRENT`, requires its terminating newline, opens the named MANIFEST, and replays checksummed `VersionEdit` records into a `Builder`. Required metadata such as log number, next-file number, and last sequence is recovered before the reconstructed Version is installed.

Thus:

> **CURRENT names the metadata history to interpret; it is not the database payload or a complete materialized membership table.**

The restart path is relational:

```text
CURRENT
    -> selected MANIFEST history
    -> reconstructed VersionSet
```

### H/P — candidate metadata is synced before a new MANIFEST is published through CURRENT

In v1.7 `VersionSet::LogAndApply()`, a proposed edit is applied to a candidate `Version`. The encoded edit is appended to the descriptor/MANIFEST log and `descriptor_file_->Sync()` is called. If a new descriptor was created, only then does LevelDB call `SetCurrentFile()`.

After these I/O steps succeed, `AppendVersion(v)` installs the candidate as the current in-memory Version.

Bounded ordering:

```text
candidate VersionEdit
    -> append metadata record to MANIFEST
    -> Sync MANIFEST
    -> if new descriptor, SetCurrentFile(...)
    -> AppendVersion(candidate) in memory
```

This directly separates **metadata embodiment persistence** from **metadata designation/publication**.

### H/P — January 2012 issue 68 identifies a separate missing sync on CURRENT contents

Original Google Code issue 68, preserved as GitHub issue #74, was created **16 January 2012**. In one Ubuntu Server 10.10 / Riak 1.0.2 environment, the reporter described a forced-power-off window in which `CURRENT` could reopen as sixteen zero bytes and the database could not be opened. The report says changing the ordinary LevelDB write `sync` option did not alter the reproduced problem and identifies the lack of an explicit `CURRENT` sync as the suspected cause.

On **18 January 2012**, Sanjay Ghemawat replied that the diagnosis was correct and that a fix was in progress. His recovery advice was to reconstruct `CURRENT` cautiously from a plausible nonempty MANIFEST name, preferably on a copy of the database directory. That advice is evidence that selector failure can coexist with surviving recovery metadata; it is not a universal automatic recovery algorithm.

On **25 January 2012**, upstream commit `3c8be108bfb5fbd7d51f824199627e757279f79e` explicitly names issue 68 as **“no sync of CURRENT file.”** Its `CURRENT`-specific diff changes `SetCurrentFile()` from `WriteStringToFile(...)` to `WriteStringToFileSync(...)`. The new helper calls the file object's `Sync()` before close when the sync path is requested.

The pre-fix parent `c8c5866...` therefore has:

```text
append temp CURRENT contents
    -> close
    -> rename to CURRENT
```

while the fixed path has:

```text
append temp CURRENT contents
    -> file Sync()
    -> close
    -> rename to CURRENT
```

The full chronology and stop conditions are in [`../evidence/137-leveldb-2012-current-content-sync-fix-deepening.md`](../evidence/137-leveldb-2012-current-content-sync-fix-deepening.md).

This is a bounded field report plus source-level fix, not a claim that the pre-fix path lost `CURRENT` on every filesystem or that `3c8be108...` introduced MANIFEST/CURRENT itself.

### H/P — SetCurrentFile syncs a temporary pointer file and then renames it to CURRENT

In v1.7 `db/filename.cc`, `SetCurrentFile()` writes `MANIFEST-N\n` to a temporary `*.dbtmp` through `WriteStringToFileSync()` and then calls:

```cpp
env->RenameFile(tmp, CurrentFileName(dbname));
```

`WriteStringToFileSync()` in `util/env.cc` creates the file, appends its bytes, calls the file object's `Sync()`, and closes it.

The sequence is therefore:

```text
MANIFEST contents synced
    -> temporary CURRENT contents synced
    -> rename temporary name to CURRENT
```

It does not follow that all three are one persistence event. The January 2012 history now shows that the middle step was an explicit corrective addition before the v1.7 baseline.

### H/P — the v1.7 POSIX RenameFile path is a direct rename wrapper without a parent-directory sync in that function

`PosixEnv::RenameFile()` in v1.7 `util/env_posix.cc` directly calls `rename(src, target)` and returns an error on failure. `DeleteFile()` directly calls `unlink()`.

The `RenameFile()` function contains no explicit subsequent `fsync()` of the database directory.

This is a source-level statement about the inspected POSIX Env. It is **not** a universal claim about every `Env`, OS, filesystem, controller, or power-failure model.

### H/P — payload recovery may require WAL files newer than the MANIFEST's registered log frontier

After `VersionSet::Recover()`, `DBImpl::Recover()` scans the database directory for log files at or above the MANIFEST-derived log frontier, plus the legacy previous-log number. A source comment explicitly notes that a prior incarnation may have created a new log without registering it in the descriptor.

Those logs are replayed in generation order and may be materialized as new level-0 tables.

Therefore:

> **recovered membership metadata != complete recent payload recovery history.**

### H/P — compaction output is made usable before metadata makes it current

For ordinary compaction, v1.7 finishes new output tables, syncs/closes them, and checks non-empty outputs through the table cache. `InstallCompactionResults()` records input deletions and output additions in a `VersionEdit`, which is persisted through `LogAndApply()`.

Only after the file-set transition is installed does the background-compaction path call `DeleteObsoleteFiles()`.

Bounded handoff:

```text
old live input tables
    -> build/sync new output tables
    -> persist file-set edit in MANIFEST
    -> install new current Version
    -> identify/delete obsolete files
```

### H/P — losing newest-version membership does not immediately make an SSTable reclaimable

`version_set.h` says the newest Version is `current`, while older Versions may stay live to provide a consistent view to active readers. `VersionSet::AddLiveFiles()` traverses every live Version and marks referenced table numbers live.

`DBImpl::DeleteObsoleteFiles()` begins from `pending_outputs_`, adds every file referenced by live Versions, and deletes a table only if it is absent from this live set.

Therefore:

> **not referenced by newest current Version != immediately reclaimable physical file.**

### H/P — obsolete descriptor/log names can be unlinked after the newer recovery state is accepted

`DeleteObsoleteFiles()` also applies liveness rules to descriptor and log files. Older MANIFEST names and no-longer-needed logs may be deleted once the current `VersionSet` and log-number relations no longer require them.

This creates a directionally important relation:

```text
publish/accept new recovery root
    -> old recovery-root components become eligible for retirement
```

### H/P — 2013 upstream issue 189/#195 explicitly raised rename-vs-unlink crash-order portability

Original LevelDB issue 189, created 17 July 2013 and preserved as GitHub issue #195, is titled “Possible bug: fsync() required after calling rename()”. The report describes the open/recovery path as producing new state, updating CURRENT with atomic rename, and then deleting old log/MANIFEST files.

Its concern is specifically that LevelDB did not explicitly ensure the `CURRENT` rename became persistent before later `unlink()` operations became persistent. If the old recovery files disappeared while the old CURRENT relation survived a crash, restart could lack files required by that old root.

The report also preserves a crucial negative boundary: the reporter says the behavior was **not reproduced on the ext3/ext4 filesystems they normally used**. The issue is therefore evidence of a recognized portability/persistence-order seam, not proof of a universal LevelDB corruption bug.

The 2013 concern is deliberately not merged with issue 68. The 2012 fix strengthens **selector-file content persistence**; the 2013 report asks about **final namespace publication and its ordering against later retirement**.

Detailed chronology and source boundaries are in [`../evidence/137-leveldb-v17-2013-current-rename-namespace-durability-deepening.md`](../evidence/137-leveldb-v17-2013-current-rename-namespace-durability-deepening.md).

### H/P — current upstream preserves the same local SetCurrentFile source shape

Current upstream `db/filename.cc`, inspected during the deepening, still writes/syncs a temporary pointer and then calls `RenameFile()` to replace CURRENT; the function itself contains no explicit parent-directory sync afterward.

This is only source-shape continuity. It does not prove identical behavior for every modern Env/filesystem, prove issue #195 remains exploitable, or establish that no durability work occurs elsewhere.

### H/P — LevelDB's implementation note draws a bounded Bigtable comparison

`doc/impl.html` describes LevelDB as “similar in spirit” to the representation of a single Bigtable tablet while immediately noting organization differences.

That is historical evidence for an author-drawn functional comparison, not evidence of identical recovery contracts or one-to-one metadata lineage.

---

## Retained state

At least nine state classes must remain distinct.

### 1. User key/value and deletion records

Application-level logical contents represented across current memtable, recent user-update log, and live SSTables.

### 2. User-update log history

`*.log` records retain recent mutations that can be replayed after process loss.

### 3. Immutable SSTable embodiments

Individual table files retain sorted key/value/deletion entries. Physical existence alone does not decide whether a table belongs to the current serving state.

### 4. MANIFEST / VersionEdit history

MANIFEST retains changes to serving-file membership and required recovery metadata. It is metadata history, not a second copy of all user payload.

### 5. CURRENT contents

CURRENT retains the textual MANIFEST name that recovery should interpret. The January 2012 fix is specifically about requesting persistence for those selector contents before publication.

### 6. CURRENT namespace binding / publication state

The final pathname `dbname/CURRENT` is itself a retained namespace relation. In the POSIX path, making the temporary file durable and renaming it are distinct operations; crash persistence of the final directory entry is a separate lower-layer question.

### 7. In-memory Version / VersionSet state

The current Version is reconstructed and then evolves in memory. Older Versions can remain live for readers.

### 8. Pending-output state

`pending_outputs_` protects newly allocated output files that are in flight but not yet safely classifiable as ordinary current table files.

### 9. File-liveness / reclamation relation

A file is reclaimable only when relevant Version, pending-output, log-number, and file-type rules no longer keep it live.

---

## Engineering reconstruction

### File existence != current membership

An SSTable can survive physically while no longer belonging to the newest Version. Conversely, intact SSTables are insufficient to reconstruct the intended current view if the selecting metadata relation is missing or corrupt.

```text
physical embodiment survival
    != current serving membership
```

### CURRENT != current database state

CURRENT is indirection to a MANIFEST name. Recovery must replay the selected MANIFEST to reconstruct VersionSet.

```text
pointer-to-currentness evidence
    != materialized current payload
```

### MANIFEST persistence != payload completeness

Recovery deliberately searches for newer user logs that may not yet be registered in the descriptor.

```text
metadata checkpoint/frontier
    != complete recent mutation history
```

### New embodiment created != new embodiment authoritative

Compaction can finish and sync a new SSTable before metadata admits it into the serving file set.

```text
durable candidate file
    != current member
```

### Durable MANIFEST != durably published MANIFEST selection

The deepenings make the layered boundary explicit:

```text
MANIFEST contents synced
    != temp CURRENT contents appended/closed
    != temp CURRENT contents explicitly synced
    != CURRENT rename performed
    != containing namespace independently proven crash-durable
```

The January 2012 fix closes a source-level gap between the second and third milestones. The later rename/directory issue concerns a subsequent milestone.

### User-write sync != CURRENT metadata sync

Issue 68 reports that ordinary write `sync` selection did not alter the reproduced `CURRENT` failure, while the actual patch changes the selector-publication helper. At project level:

```text
user mutation durability policy
    != recovery-selector durability path
```

Making client payload acknowledgements stricter does not automatically strengthen every independent metadata publication path.

### Fixing file-content durability != proving end-to-end root publication durability

The January 2012 history and July 2013 report form a useful counterexample to treating `sync` as one global Boolean:

```text
selector bytes explicitly synced
    -> one persistence obligation strengthened

but

final pathname publication
    + ordering against old-root unlink
    -> still a separate question
```

Thus:

> **one persistence frontier closed != all later persistence frontiers closed.**

### Atomic rename visibility != crash-persistent publication

Calling `rename()` atomic describes the ordinary namespace replacement relation. It does not, by itself, settle which directory update survives a sudden failure on every backend.

```text
atomic observer-visible replacement
    != universal post-crash namespace guarantee
```

### Restart-root publication != old-root retirement

The LevelDB control flow publishes/accepts new recovery metadata before old names become reclaimable. The 2013 issue exposes why the same **program order** may still need a persistence-order guarantee:

```text
new root accepted by running process
    != new root proven durable before every later unlink
```

The concern is cross-object retirement ordering, not merely whether one file received `Sync()`.

### Selector corruption != payload disappearance

The 2012 maintainer recovery advice demonstrates a narrower failure shape: ordinary opening can be stranded by a corrupt selector even when candidate MANIFEST material remains. Therefore:

```text
recovery metadata survives
    + selector relation unusable
    -> ordinary restart may fail
```

Re-establishing the selector may restore interpretive reach to surviving metadata; it does not manufacture payload bytes absent from logs/SSTables, nor prove that an arbitrarily chosen MANIFEST is current.

### Superseded from current != safe to delete

Live readers can hold old Versions, and `AddLiveFiles()` preserves their tables.

```text
loss of newest-version authority
    != immediate physical reclamation
```

### File deletion != sanitization

`DeleteObsoleteFiles()` performs filesystem-level deletion. It does not establish overwrite, NAND block erase, controller secure erase, crypto erase, or forensic disappearance.

```text
LevelDB obsolete-file deletion
    != media sanitization
```

Cases 44/47 remain the appropriate repository layer for stronger forgetting claims.

---

## Relation to neighboring cases

### Case 57 — Bigtable tablet recovery

Both systems compose recent redo history, volatile memtable state, immutable tables, and metadata defining a current/recoverable file set.

But the metadata forms remain distinct:

- Bigtable 2006: tablet `METADATA` includes SSTable lists and redo points;
- LevelDB v1.7: `CURRENT` names a MANIFEST whose `VersionEdit` history reconstructs VersionSet.

LevelDB's own “similar in spirit” statement supports comparison, not identity.

### Case 42 — Kafka log compaction

Kafka Case 42 compacts a user-visible keyed log while preserving logical offsets/current-per-key semantics. LevelDB's MANIFEST is metadata history; user updates live separately in `*.log` files and SSTables.

```text
log-structured current-state metadata
    != keyed user-log compaction
```

### Case 124 — Linux ext4 rename/fsync durability closure

Case 124 supplies the filesystem-level vocabulary needed to avoid conflation:

```text
rename visibility atomicity
    != file durability
    != containing-directory entry durability
```

LevelDB adds a recovery-specific consequence: `CURRENT` is not merely a filename but the restart selector that chooses a MANIFEST history. The January 2012 fix and the later 2013 issue make the file-content-versus-directory-publication split historically visible within one application.

The comparison is functional, not a claim that ext4 semantics define every LevelDB `Env`.

### Case 58 — etcd snapshot directory-fsync correction

Case 58's 2026 received-snapshot deepening records a later etcd implementation that explicitly adds a containing-directory fsync after renaming the final snapshot DB before higher-level snapshot processing proceeds.

The common relation is:

```text
file content persistence
    != namespace mutation
    != namespace persistence closure
    != higher-level publication
```

The retained objects and protocols differ: etcd is publishing a received snapshot DB in a Raft path; LevelDB's `CURRENT` selects a MANIFEST history.

### PostgreSQL durable-rename deepening under Case 124

The PostgreSQL evidence in Case 124 gives another application-level counterexample in which durable file contents under the wrong filename are insufficient for correct WAL recovery.

It provides a design comparison, not a requirement that LevelDB copy PostgreSQL's exact syscall sequence.

---

## Prior art and anti-anachronism

The safe historical floor is now more precise:

- **16 January 2012:** original issue 68 reports a named-environment forced-power-loss `CURRENT` corruption and identifies missing explicit sync as the suspected path;
- **18 January 2012:** a LevelDB maintainer accepts the diagnosis and says a fix is in progress;
- **25 January 2012:** commit `3c8be108...` changes `SetCurrentFile()` to use `WriteStringToFileSync()`, whose sync path calls `file->Sync()` before close;
- **16 October 2012:** the v1.7 baseline contains the synced-temp-file publication path analyzed here;
- **17 July 2013:** upstream issue 189 separately records the rename-vs-unlink power-failure/portability concern later migrated as GitHub #195;
- current upstream source inspected in 2026 retains the same local temp-sync-then-rename shape in `SetCurrentFile()`.

Do **not** turn those facts into claims that LevelDB invented manifests, root selectors, atomic pointer replacement, file/directory sync practice, WAL recovery, immutable-file reclamation, or the general LSM design. The January 2012 commit is a bounded **corrective chronology for one selector-content persistence frontier**, not an invention-priority result.

Earlier and descendant genealogy belongs primarily in `computing-archaeology` if developed.

---

## Philosophical interpretation — bounded

A technically surviving file is not necessarily a surviving **current object**. Currentness can depend on retained relations that select, order, and authorize material embodiments.

The MANIFEST/CURRENT chain makes that relation unusually visible:

```text
MANIFEST bytes survive
    + CURRENT does not durably designate them
    -> ordinary restart need not treat that MANIFEST as current
```

The same bytes can move from candidate, to current, to superseded-but-reader-live, to reclaimable without their payload changing at each logical boundary.

The paired durability deepenings add one narrow proposition:

> **retention of an embodiment, retention of the selector's own bytes, and retention of the namespace designation relation required to find/interpret that selector can be separate technical obligations.**

This is an engineering-derived interpretation, not historical LevelDB vocabulary. It does not imply that metadata is metaphysically more real than payload or that every filename is a philosophical form of memory.

---

## Related-repository check

Fresh searches of `tmzncty/computing-archaeology` for `LevelDB`, including `LevelDB CURRENT MANIFEST`, returned no dedicated overlapping study during this round.

Division of labor:

- `technical-retention`: current-file-set relation, MANIFEST embodiment vs CURRENT designation, selector file-content persistence, namespace-persistence frontier, metadata/payload-history separation, old-Version liveness, retirement boundary, and bounded cross-case comparison;
- `computing-archaeology`: broader LSM genealogy, Bigtable→LevelDB/RocksDB history, exact first commits introducing the design, Google Code / LevelDB platform evolution, Riak/eleveldb integration history, database/filesystem genealogy, and later descendants.

No duplicate technical-history packet was created here.

---

## Open evidence debt

The 2013 deepening closes the **source-level v1.7 CURRENT rename / namespace-persistence seam** as a documented bounded concern, while the January 2012 deepening now closes the narrower **pre-v1.7 CURRENT file-content Sync chronology**. Remaining debt is narrower:

- exact first-introduction commits for MANIFEST/CURRENT/VersionSet semantics before the January 2012 fix;
- exact downstream Riak/eleveldb revision used by the original issue-68 reporter;
- controlled fault injection across pre-fix/post-fix selector content sync, MANIFEST sync, CURRENT replacement, directory persistence, and old-file unlink on selected historical filesystems;
- exact post-2013 issue/commit genealogy, including whether platform implementations or descendants added durability closure elsewhere;
- Windows/non-POSIX `Env` behavior;
- initial-database creation durability, whose `NewDB()` path deserves separate treatment rather than being silently equated with later MANIFEST rollover;
- later LevelDB/RocksDB MANIFEST rollover and atomicity evolution;
- corruption/truncation behavior beyond the bounded checked recovery path;
- exact old-Version lifetime under snapshots/iterators across releases;
- lower device/controller persistence beneath requested file/directory synchronization;
- filesystem/device-layer proof for physical reclamation or sanitization after obsolete-file deletion.

None of these require a maturity change: Case 137 remains **`grounded`**.