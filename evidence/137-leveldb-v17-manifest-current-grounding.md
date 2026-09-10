# Evidence 137 — Google LevelDB v1.7 MANIFEST/CURRENT, Recovery, and File-Liveness Grounding

## Scope

This record grounds one bounded relation in the public LevelDB `v1.7` tree:

> LevelDB reconstructs current serving-file membership from a retained MANIFEST edit log selected by CURRENT, composes that metadata state with separately retained user-update logs during recovery, and delays physical table-file deletion until files are no longer referenced by any live Version or pending output.

The record does not claim invention priority, universal filesystem crash atomicity, or secure media erasure.

## Release identity

**Primary repository tag:** `google/leveldb` `v1.7`

- tag ref: `refs/tags/v1.7`
- commit: `40768657bc8ec3ded60712eeeab7c25b1b07deca`
- commit author/committer: Sanjay Ghemawat
- commit timestamp: `2012-10-16T23:17:53Z`
- tag ref API: https://api.github.com/repos/google/leveldb/git/ref/tags/v1.7
- commit: https://github.com/google/leveldb/commit/40768657bc8ec3ded60712eeeab7c25b1b07deca

This date is a release-tree evidence floor for the inspected behavior, **not** the first invention/implementation date for every mechanism below.

## Source 1 — LevelDB v1.7 `doc/impl.html`

**Type:** project-primary implementation documentation (`H/P`)

URL: https://github.com/google/leveldb/blob/v1.7/doc/impl.html

### Locator A — `Files` / `Log files`

The document says a `*.log` file stores a sequence of recent updates; each update is appended to the current log. A copy of the current log is represented in the in-memory memtable and consulted by reads.

**Supported relation:** recent user-mutation history is a distinct retained representation used for recovery/current reads.

### Locator B — `Manifest`

The document says a MANIFEST lists the sorted tables making up each level, their key ranges, and other metadata. A MANIFEST is formatted as a log, and serving-state changes as files are added/removed are appended.

**Supported relation:** MANIFEST is an append-log of **file-set/serving-state metadata**, not the same thing as the user-update log.

### Locator C — `Current`

The document defines CURRENT as a simple text file containing the name of the latest MANIFEST.

**Supported relation:** `CURRENT != current payload`; it is an indirection selecting a metadata history.

### Locator D — `Recovery`

The documented recovery sequence begins by reading CURRENT to find the latest committed MANIFEST, then reading the named MANIFEST, cleaning stale files, converting log chunks into new level-0 SSTables, and starting new writes with a recovered sequence number.

**Supported relation:** restart composes metadata-history recovery and user-log replay/materialization.

### Locator E — `Garbage collection of files`

The document says `DeleteObsoleteFiles()` is called after compaction and recovery; it deletes table files not referenced from a level and not the output of an active compaction.

The source code below sharpens this statement by showing that “referenced” includes all live Versions, not just the newest one.

### Locator F — introductory Bigtable comparison

The document says LevelDB is “similar in spirit” to the representation of a single Bigtable tablet while its file organization is somewhat different.

**Supported historical claim:** LevelDB authors explicitly drew this design comparison.

**Not supported:** direct code descent, identical metadata semantics, or a claim that Bigtable invented every LevelDB mechanism.

## Source 2 — LevelDB v1.7 `db/version_set.cc`

**Type:** project-primary released source (`H/P`)

URL: https://github.com/google/leveldb/blob/v1.7/db/version_set.cc

### Locator A — `VersionSet::LogAndApply()`

The function:

1. fills required edit metadata (`log_number`, `next_file`, `last_sequence`, etc.);
2. applies the edit to a candidate `Version` through a `Builder`;
3. if necessary creates a new MANIFEST and writes a snapshot of the current Version;
4. appends the encoded edit to the MANIFEST;
5. calls `descriptor_file_->Sync()`;
6. if a new MANIFEST was created, calls `SetCurrentFile()`;
7. only on success calls `AppendVersion(v)` and updates in-memory metadata.

**Supported relations:**

- candidate file-set state is distinguished from installed current Version;
- MANIFEST persistence is ordered before in-memory current-Version installation in this code path;
- new MANIFEST selection through CURRENT is a separate step from MANIFEST content creation.

**Not supported:** universal crash atomicity of the whole storage stack.

### Locator B — `VersionSet::Recover()`

The function reads CURRENT, checks the newline, opens the named MANIFEST, reads checksummed records, decodes `VersionEdit` objects, applies them to a `Builder`, recovers log/next-file/last-sequence fields, and finally installs a reconstructed `Version`.

**Supported relation:** current file membership is reconstructed from retained metadata history, rather than inferred from mere directory presence of SSTables.

### Locator C — `VersionSet::WriteSnapshot()`

When a new descriptor is created, the snapshot record includes comparator name, compaction pointers, and every file in every level of the current Version.

**Supported relation:** a new MANIFEST can begin from a materialized metadata snapshot and then accumulate later VersionEdits; “MANIFEST is a log” does not imply that every historical metadata edit must remain forever in one file.

### Locator D — `VersionSet::AddLiveFiles()`

The function iterates from `dummy_versions_.next_` through **all live Version objects** and adds every referenced table-file number to the live set.

**Supported relation:** file-reclamation liveness is broader than newest-Version membership.

## Source 3 — LevelDB v1.7 `db/version_set.h`

**Type:** project-primary released source/header commentary (`H/P`)

URL: https://github.com/google/leveldb/blob/v1.7/db/version_set.h

The header states that a `DBImpl` is represented by a set of `Version`s; the newest is called `current`; older Versions may be retained to provide a consistent view to live iterators. Each Version tracks a set of table files per level and all Versions are maintained in a `VersionSet`.

**Supported relations:**

- `current` is one distinguished Version among potentially several live Versions;
- old Version lifetime can be extended by live readers/iterators;
- retaining an old Version can retain physical table-file liveness even after the newest Version no longer selects that file.

## Source 4 — LevelDB v1.7 `db/version_edit.h`

**Type:** project-primary released source (`H/P`)

URL: https://github.com/google/leveldb/blob/v1.7/db/version_edit.h

`VersionEdit` has explicit operations/fields for:

- comparator name;
- current/previous log number;
- next file number;
- last sequence;
- compaction pointers;
- adding a file to a level with key-range/file-size metadata;
- deleting a specified file from a specified level.

**Supported relation:** MANIFEST records describe transitions in the serving metadata relation, including explicit file additions/deletions; they are not opaque “database snapshots” by definition.

## Source 5 — LevelDB v1.7 `db/db_impl.cc`

**Type:** project-primary released source (`H/P`)

URL: https://github.com/google/leveldb/blob/v1.7/db/db_impl.cc

### Locator A — `DBImpl::Recover()`

After `versions_->Recover()`, LevelDB scans for log files whose numbers are at/after the MANIFEST's current log number (plus the previous-log compatibility case). The source comment says the previous incarnation may have created a new log without registering it in the descriptor. Logs are sorted and replayed.

**Supported relation:** MANIFEST state can be complete enough to identify the serving file set while still requiring separately retained user-log history for the newest payload mutations.

### Locator B — `RecoverLogFile()` and `WriteLevel0Table()`

Recovered log records are inserted into a memtable. Once needed, the memtable is written into a new level-0 table and the resulting file metadata is added to the pending `VersionEdit`.

**Supported relation:** recovery can replace retained redo history with a new materialized table embodiment before normal operation resumes.

### Locator C — `FinishCompactionOutputFile()`

Compaction output is finished, `Sync()`ed, `Close()`d, and checked through the table cache before successful return.

### Locator D — `InstallCompactionResults()` / `DoCompactionWork()` / `BackgroundCompaction()`

Compaction input deletions and output additions are collected into a `VersionEdit`; after output generation succeeds, `InstallCompactionResults()` invokes `LogAndApply()`. `BackgroundCompaction()` later calls `DeleteObsoleteFiles()` after compaction work/cleanup.

**Supported relation:** new-file embodiment creation, metadata currentness transition, and physical old-file reclamation are staged operations.

### Locator E — `DBImpl::DeleteObsoleteFiles()`

The function starts its live set from `pending_outputs_`, adds all files referenced by live Versions, and preserves/deletes files according to type. Table files are kept only if their number is in the live set.

**Supported relation:** `not in newest current Version` is insufficient for deletion while older live Versions or pending construction still reference/protect a file.

## Source 6 — LevelDB v1.7 `db/filename.cc`

**Type:** project-primary released source (`H/P`)

URL: https://github.com/google/leveldb/blob/v1.7/db/filename.cc

`SetCurrentFile()`:

1. constructs the MANIFEST filename to be installed;
2. writes that name plus newline to a temporary file using `WriteStringToFileSync()`;
3. renames the temporary file to CURRENT;
4. deletes the temporary file on failure.

**Supported relation:** v1.7 distinguishes persistence of the pointer-file contents from the namespace replacement operation that makes the new pointer visible.

**Important stop condition:** this implementation sequence is not, by itself, proof of universal post-crash directory-entry durability. Case 124 should be used for the repository's broader rename/`fsync` boundary.

## Cross-case comparison — evidence-safe

### Case 57 — Bigtable

LevelDB's own implementation document supplies a historical “similar in spirit” comparison to a single Bigtable tablet. Case 57 already grounds Bigtable's commit-log/memtable/SSTable plus `METADATA`/redo-point recovery relation.

Safe comparison:

- both systems retain recent redo history plus immutable materializations and metadata selecting/recovering the live state;
- LevelDB v1.7 specifically reconstructs a `VersionSet` by replaying a MANIFEST chosen through CURRENT;
- Bigtable 2006 uses a different distributed tablet metadata/recovery contract.

Unsafe leap:

> `similar in spirit` = identical metadata format, identical crash protocol, or direct code genealogy.

### Case 42 — Kafka compaction

Kafka's compacted topic is a user-visible keyed log. LevelDB's MANIFEST is a metadata log of serving-state changes. Shared append/compaction vocabulary does not identify the same retained object or service contract.

### Case 124 — filesystem rename durability

`SetCurrentFile()`'s sync-temp + rename sequence is a concrete application-level witness that currentness can depend on a namespace pointer update. It does not supersede Case 124's warning that rename visibility and crash durability are separate layers.

## Findings supported by this record

1. `*.log user-update history != MANIFEST file-membership history`.
2. `CURRENT != current database payload`.
3. `CURRENT pointer survival != successful MANIFEST interpretation`.
4. `SSTable physical presence != current-Version membership`.
5. `MANIFEST replay != user-WAL replay`.
6. `candidate output synced != candidate admitted into current Version`.
7. `current-Version transition != old-file physical reclamation`.
8. `superseded from newest Version != immediately deletable`.
9. `live iterator/version retention can prolong SSTable liveness`.
10. `pending output existence != current serving membership`.
11. `metadata snapshot/rollover != full user-history preservation`.
12. `filesystem deletion != media sanitization`.
13. `LevelDB “similar in spirit” to Bigtable != identical recovery contract or genealogy`.

## Evidence debt

- pre-v1.7 first-introduction commit history for MANIFEST/CURRENT and exact recovery semantics;
- later release changes to MANIFEST rollover/current-file sync behavior;
- cross-filesystem crash/fault-injection validation;
- direct tests for corrupted/truncated CURRENT/MANIFEST and stale file sets;
- exact release-specific snapshot/iterator pinning edge cases;
- lower-layer physical reclamation/sanitization after filesystem unlink.
