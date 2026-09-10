from pathlib import Path

CASE = Path("cases/137-leveldb-v17-manifest-current-recovery.md")
EVID = Path("evidence/137-leveldb-v17-manifest-current-grounding.md")
ROADMAP = Path("ROADMAP.md")
INDEX = Path("CASE_INDEX.md")

CASE.write_text(r'''# LevelDB v1.7 MANIFEST/CURRENT: Current-State Reconstruction, Version Liveness, and Obsolete-File Retirement

## Status

**`grounded`** — bounded to Google LevelDB tag `v1.7` (`40768657bc8ec3ded60712eeeab7c25b1b07deca`, 16 October 2012 UTC) and its checked-in implementation documentation/source. This case does not claim that LevelDB invented LSM trees, manifests, write-ahead logging, tombstones, compaction, or crash-consistent metadata protocols.

Grounding record: [`../evidence/137-leveldb-v17-manifest-current-grounding.md`](../evidence/137-leveldb-v17-manifest-current-grounding.md).

## Scope

Case 57 already establishes the Bigtable relation among commit log, volatile memtable, immutable SSTables, live-file metadata, redo points, and later compaction. Case 137 asks a narrower question in a bounded LevelDB release:

> When current database state is represented by many immutable table files, what retained metadata makes a particular subset count as the current serving state after restart, and when may physically surviving but superseded files finally be deleted?

LevelDB v1.7 is useful because its own implementation documentation and source expose three separate histories/relations:

1. **user-update log files** (`*.log`) retain recent payload mutations for recovery;
2. **MANIFEST** is itself a log whose `VersionEdit` records describe changes to the serving file set and associated metadata;
3. **CURRENT** is a small indirection file naming which MANIFEST should be used at open.

Compaction then creates new SSTables, records file additions/deletions in the MANIFEST, installs a new in-memory `Version`, and only later lets obsolete physical files be removed when they are no longer referenced by any live version or pending output.

This case is **not**:

- a general LevelDB/RocksDB history;
- a claim that `CURRENT` contains the current key/value database;
- a claim that MANIFEST is the user-data write-ahead log;
- a proof that v1.7's `SetCurrentFile()` sequence is durably atomic on every filesystem and storage stack;
- a proof that an unreferenced/deleted SSTable is securely erased from underlying media;
- a claim that every surviving old SSTable remains readable or semantically useful;
- a claim that Bigtable and LevelDB have identical recovery metadata or direct code lineage.

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

`current-state relation`, `membership authority`, `recovery graph`, and `metadata-history compaction` below are project engineering terms, not period LevelDB vocabulary.

## Historical record

### H/P — v1.7 explicitly separates user-update logs from the MANIFEST metadata log

The checked-in `doc/impl.html` says each `*.log` file stores a sequence of recent updates, with each update appended to the current log. It separately says a MANIFEST lists the sorted tables comprising each level, their key ranges, and other metadata; the MANIFEST is formatted as a log, and changes to the **serving state** as files are added or removed are appended to it.

This is a direct terminology boundary inside one implementation:

> **user-update log != MANIFEST serving-state log.**

The same source says `CURRENT` is a simple text file containing the name of the latest MANIFEST.

### H/P — recovery begins with a small pointer, then reconstructs current file membership by replaying metadata edits

`VersionSet::Recover()` first reads `CURRENT`, requires its final newline, opens the named MANIFEST, and reads it through LevelDB's log reader with checksums enabled. Each decoded `VersionEdit` is applied to a `Builder`; required meta fields such as log number, next-file number, and last sequence are recovered; only after this replay succeeds does LevelDB create and append the recovered `Version` as current.

Thus:

> **CURRENT names the metadata history to interpret; it is not the database payload or a complete materialized file-membership table by itself.**

### H/P — a candidate serving-state change is logged and synced before it becomes the current in-memory Version

In v1.7 `VersionSet::LogAndApply()` first applies the proposed edit to a candidate `Version`. It then appends the encoded edit to the descriptor/MANIFEST log and calls `descriptor_file_->Sync()`. If this is a newly created MANIFEST, it calls `SetCurrentFile()` to install the corresponding CURRENT pointer. Only after those steps succeed does `AppendVersion(v)` make the candidate the current in-memory Version.

This directly supports the bounded ordering:

```text
candidate VersionEdit
    -> append metadata record to MANIFEST
    -> Sync MANIFEST
    -> if needed, install CURRENT pointer
    -> AppendVersion(candidate) as in-memory current
```

The source does **not** prove end-to-end crash atomicity for every filesystem/controller combination. `SetCurrentFile()` writes and syncs a temporary file and then renames it to CURRENT, but v1.7 does not itself establish the stronger universal proposition that the containing-directory rename is durable under every crash model.

### H/P — payload recovery can require WAL files newer than the MANIFEST's registered log number

`DBImpl::Recover()` first recovers the `VersionSet`, then scans database-directory files for log files whose numbers are at or above the MANIFEST-derived log frontier (plus the legacy previous-log number). The source comment explicitly says a previous incarnation may have added a new log file without registering it in the descriptor.

Those logs are replayed in generation order into memtables and can be materialized as new level-0 tables during recovery.

Therefore:

> **recovered file-membership metadata != complete recent payload recovery history.**

The MANIFEST and user-update log have different retained roles.

### H/P — compaction output is made usable before metadata makes it current

For ordinary compaction, v1.7 builds new output tables, finishes them, calls `Sync()` and `Close()` on output files, and opens each non-empty output through the table cache as a usability check. `InstallCompactionResults()` then places input deletions and output additions into a `VersionEdit` and sends that edit through `LogAndApply()`.

Only after the file-set transition is installed does `BackgroundCompaction()` call `DeleteObsoleteFiles()`.

This supplies a bounded handoff:

```text
old live input tables
    -> build new output tables
    -> sync/close/check outputs
    -> persist file-set edit in MANIFEST
    -> install new current Version
    -> identify/delete now-obsolete files
```

### H/P — losing current membership does not immediately make a physical SSTable deletable

`version_set.h` says the newest Version is called `current`, while older Versions may remain to provide a consistent view to live iterators. `VersionSet::AddLiveFiles()` traverses **every live Version** in the linked list and inserts every referenced table-file number into the live set.

`DBImpl::DeleteObsoleteFiles()` begins from `pending_outputs_`, adds all files referenced by live Versions, and only deletes a table file if its number is absent from this live set.

Therefore:

> **not referenced by the newest current Version != immediately reclaimable physical file.**

A superseded Version retained for a live iterator can prolong the file's liveness after current serving authority has moved on.

### H/P — LevelDB's own implementation note makes an explicit but bounded Bigtable comparison

`doc/impl.html` states that LevelDB's implementation is “similar in spirit” to the representation of a single Bigtable tablet while immediately noting that the file organization is somewhat different.

That statement is historical evidence that LevelDB's authors themselves drew a functional/design comparison. It is **not** sufficient evidence of source-code descent, identical recovery contracts, or a one-to-one mapping from Bigtable `METADATA`/redo points to LevelDB `CURRENT`/MANIFEST.

## Retained state

At least eight state classes must remain distinct in this bounded release.

### 1. User key/value and deletion records

These are the application-level logical contents represented across the current memtable, recent log, and live SSTables.

### 2. User-update log history

`*.log` records retain recent mutations that can be replayed after process loss.

### 3. Immutable SSTable embodiments

Individual table files retain sorted key/value/deletion entries. Physical existence alone does not decide whether a table belongs to the current serving state.

### 4. MANIFEST / VersionEdit history

The MANIFEST retains changes to the serving-state file set and required recovery metadata. It is metadata history, not a second copy of all user payload.

### 5. CURRENT indirection

CURRENT retains the name of the MANIFEST that recovery should interpret.

### 6. In-memory Version / VersionSet state

The current Version is a reconstructed and then evolving in-memory file-membership relation. Older Versions can remain live for iterators.

### 7. Pending-output state

`pending_outputs_` protects newly allocated output files that are being produced but are not yet safely classified as ordinary current table files.

### 8. File-liveness / reclamation relation

A table file is reclaimable only when it is absent from the live set formed from all retained Versions and pending outputs, subject to the file-type rules in `DeleteObsoleteFiles()`.

## Engineering reconstruction

### File existence != current membership

An SSTable can physically survive in the database directory while no longer belonging to the newest Version. Conversely, a set of individually intact SSTables is insufficient to reconstruct the intended current database view if the metadata relation selecting and ordering them is unavailable or corrupt.

> **physical embodiment survival != current serving membership.**

### CURRENT != current database state

CURRENT is only an indirection to a MANIFEST name. Recovery must then parse the MANIFEST's edit history to reconstruct the VersionSet.

> **pointer-to-currentness evidence != materialized current payload.**

The small file is important because it qualifies which larger retained history should be interpreted.

### MANIFEST persistence != payload completeness

The v1.7 recovery path deliberately searches for newer user logs that may not yet have been registered in the descriptor.

> **metadata checkpoint/frontier != complete recent mutation history.**

This is a concrete counterexample to treating one “manifest” as a universal recovery image.

### New embodiment created != new embodiment authoritative

Compaction can finish and sync a new SSTable before the MANIFEST/current Version admits it into the serving file set.

> **durable candidate file != current member.**

`pending_outputs_` further shows that physically created output needs a separate liveness classification while construction is in flight.

### Superseded from current != safe to delete

Live iterators can hold old Versions, and `AddLiveFiles()` treats files referenced by those Versions as live.

> **loss of newest-version authority != immediate physical reclamation.**

This is an in-process reader-liveness boundary, not a historical archive promise. Once the old Version references disappear and no other rule keeps the file, `DeleteObsoleteFiles()` may remove it.

### File deletion != sanitization

`DeleteObsoleteFiles()` invokes filesystem deletion on obsolete names. This is a logical/filesystem reclamation action. It does not establish overwrite, NAND block erase, controller secure erase, crypto erase, or forensic disappearance.

> **LevelDB obsolete-file deletion != media sanitization.**

Cases 44/47 remain the appropriate repository layer for stronger forgetting claims.

## Relation to neighboring cases

### Case 57 — Bigtable tablet recovery

The closest internal comparison is Case 57. Both systems compose recent redo history, volatile memtable state, immutable SSTables, and retained metadata that defines a current/recoverable file set.

But the metadata shapes are deliberately kept distinct:

- Bigtable 2006: tablet `METADATA` contains SSTable lists and redo points;
- LevelDB v1.7: `CURRENT` names a MANIFEST, whose `VersionEdit` log reconstructs the `VersionSet`.

LevelDB's own “similar in spirit” statement allows a historically grounded comparison, but not an identity claim.

### Case 42 — Kafka log compaction

Kafka Case 42 compacts a user-visible keyed log while preserving logical offsets and current-per-key semantics. LevelDB's MANIFEST is a metadata log of serving-file-set changes, while its user updates live in separate `*.log` files and SSTables.

> **log-structured current-state metadata != keyed user-log compaction.**

The common word `log` is not evidence of the same retained object or compaction contract.

### Case 124 — rename / namespace durability closure

LevelDB v1.7's `SetCurrentFile()` uses a sync-temp-then-rename pattern to replace CURRENT. Case 124 shows why visibility/rename and crash durability must remain separate claims.

The present case therefore records the exact LevelDB code sequence but does **not** promote it into a universal filesystem durability theorem.

## Prior art and anti-anachronism

The safe historical floor in this case is deliberately modest:

- by the `v1.7` tag commit of 16 October 2012, LevelDB publicly shipped/checks in the MANIFEST/CURRENT/VersionSet/recovery behavior analyzed here;
- the source headers and implementation notes reach back to 2011, but this case does not claim the exact first commit for each mechanism;
- LevelDB's own implementation note explicitly compares the design “in spirit” with a single Bigtable tablet while preserving organizational differences.

This does **not** establish invention priority for LSM metadata, manifest logs, WAL recovery, immutable-file reclamation, snapshot pinning, or atomic-current-pointer replacement. Earlier database and filesystem genealogy belongs primarily in `computing-archaeology` if developed.

## Philosophical interpretation — bounded

This case sharpens one narrow retention proposition:

> a technically surviving file is not necessarily a surviving **current object**; currentness can depend on a retained relation that selects, orders, and authorizes material embodiments.

The MANIFEST/CURRENT chain makes that relation unusually visible. The same bytes can move from current membership to superseded-but-reader-live status and finally to reclaimable status without the file's material contents changing at the moment each logical boundary is crossed.

This is an engineering-derived interpretation, not historical LevelDB vocabulary. It does not imply that metadata is metaphysically more real than payload, and it does not generalize every database manifest into the same philosophical structure.

## Related-repository check

Fresh searches of `tmzncty/computing-archaeology` for `LevelDB`, `MANIFEST`, `CURRENT`, `VersionSet`, and `LSM` returned no dedicated overlapping study during this round.

Division of labor:

- `technical-retention`: current-file-set relation, metadata/payload-history separation, old-Version liveness, reclamation boundary, and cross-case comparison;
- `computing-archaeology`: broader LSM-tree genealogy, Bigtable→LevelDB/RocksDB engineering history, exact first commits, filesystem interaction, and implementation evolution.

## Open evidence debt

- exact first-introduction commits for MANIFEST/CURRENT/VersionSet semantics before v1.7;
- later LevelDB/RocksDB MANIFEST rollover and atomicity evolution;
- fault injection across MANIFEST sync, CURRENT replacement, directory persistence, and power loss;
- behavior under corrupted/truncated MANIFEST or CURRENT beyond the bounded checked code path;
- exact lifetime of old Versions under snapshots versus iterators across releases;
- filesystem/device-layer proof for when deleted obsolete files are physically reclaimed;
- broader LSM/WAL/manifest genealogy and descendant-system comparison.
''', encoding="utf-8")

EVID.write_text(r'''# Evidence 137 — Google LevelDB v1.7 MANIFEST/CURRENT, Recovery, and File-Liveness Grounding

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
''', encoding="utf-8")

roadmap = ROADMAP.read_text(encoding="utf-8")
case136_prefix = "- [x] Case 136 MegaRAID/PERC rebuild-rate / repair-priority policy slice"
if "Case 137 LevelDB v1.7 MANIFEST/CURRENT" not in roadmap:
    lines = roadmap.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(case136_prefix):
            lines.insert(i + 1, "- [x] Case 137 LevelDB v1.7 MANIFEST/CURRENT current-state reconstruction / file-liveness slice — [`cases/137-leveldb-v17-manifest-current-recovery.md`](cases/137-leveldb-v17-manifest-current-recovery.md) + [`evidence/137-leveldb-v17-manifest-current-grounding.md`](evidence/137-leveldb-v17-manifest-current-grounding.md): the 16-October-2012 `v1.7` tree separates recent user-update logs from the MANIFEST serving-state log and the CURRENT indirection, grounds recovery by metadata-edit replay plus separately discovered WAL replay, and shows compaction handoff as output sync/check -> MANIFEST/current-Version admission -> later obsolete-file deletion. Older live Versions retained for iterators and `pending_outputs_` broaden physical file liveness beyond newest-Version membership. This closes the bounded `file presence != current membership`, `MANIFEST != user WAL`, and `superseded != immediately reclaimable` seams without claiming universal filesystem crash atomicity or media sanitization. Exact pre-v1.7 genealogy, later LevelDB/RocksDB evolution, and fault injection remain open; broader LSM history belongs primarily in `computing-archaeology`.")
            break
    else:
        raise RuntimeError("Case 136 roadmap anchor not found")
    roadmap = "\n".join(lines) + "\n"

bridge_old = "The broad item stays unchecked because Databus mechanism genealogy, pre/post-0.8.1 Kafka compaction chronology, replication/ISR interaction, later Streams changelog/processing semantics and post-0.11 transaction/coordinator evolution, compaction correctness under failure, and operational/commercial evolution remain separate regimes."
bridge_new = "Case 137 adds a separate embedded-LSM metadata-currentness witness: LevelDB v1.7 uses CURRENT -> MANIFEST VersionEdit replay to reconstruct the current table-file set while separately replaying newer user-update logs, and delays table-file reclamation while older live Versions or pending outputs still retain liveness. This is not Kafka keyed user-log compaction or Bigtable's distributed METADATA/redo-point contract. The broad item stays unchecked because Databus mechanism genealogy, pre/post-0.8.1 Kafka compaction chronology, replication/ISR interaction, later Streams changelog/processing semantics and post-0.11 transaction/coordinator evolution, broader LevelDB/RocksDB evolution, compaction correctness under failure, and operational/commercial evolution remain separate regimes."
if bridge_old in roadmap:
    roadmap = roadmap.replace(bridge_old, bridge_new, 1)
elif bridge_new not in roadmap:
    raise RuntimeError("append-log roadmap bridge anchor not found")
ROADMAP.write_text(roadmap, encoding="utf-8")

index = INDEX.read_text(encoding="utf-8")
row = "| [LevelDB v1.7 MANIFEST/CURRENT: Current-State Reconstruction, Version Liveness, and Obsolete-File Retirement](cases/137-leveldb-v17-manifest-current-recovery.md) | **grounded** | append-only user WAL + MANIFEST metadata log + CURRENT indirection + immutable SSTables + live-Version reference protection + staged file reclamation | separate physical file survival, current file-set authority, metadata-history replay, user-log replay, candidate output, reader-pinned old Version, and later reclamation; show `log` names different retained objects inside one system | [2012 v1.7 grounding](evidence/137-leveldb-v17-manifest-current-grounding.md); pre-v1.7 first-introduction history, later LevelDB/RocksDB evolution, cross-filesystem fault injection, and lower-layer reclamation remain open |"
if "cases/137-leveldb-v17-manifest-current-recovery.md" not in index:
    lines = index.splitlines()
    for i, line in enumerate(lines):
        if "cases/136-megaraid-perc-rebuild-rate-repair-priority.md" in line:
            lines.insert(i + 1, row)
            break
    else:
        raise RuntimeError("Case 136 table row anchor not found")
    index = "\n".join(lines) + "\n"

findings = r'''

## Case 137 — LevelDB v1.7 MANIFEST/CURRENT current-state reconstruction findings

Grounding record: [`evidence/137-leveldb-v17-manifest-current-grounding.md`](evidence/137-leveldb-v17-manifest-current-grounding.md).

- **2911 — user-update log != MANIFEST serving-state log:** LevelDB v1.7 uses `*.log` for recent user mutations while MANIFEST is a log of table-file-set/serving metadata changes. (`H/P`)
- **2912 — CURRENT != current database payload:** CURRENT contains the name of the latest MANIFEST; it is an indirection selecting metadata history, not a materialized key/value database. (`H/P`, `E`)
- **2913 — CURRENT pointer survival != successful current-state reconstruction:** recovery must still open, checksum/read, decode, and apply the named MANIFEST records before installing a recovered Version. (`H/P`, `E`)
- **2914 — directory SSTable presence != current membership:** current serving state is reconstructed from Version metadata; merely finding an SSTable in the directory does not make it a member of the recovered current Version. (`H/P`, `E`)
- **2915 — MANIFEST replay != user-WAL replay:** `VersionSet::Recover()` reconstructs file-set metadata, while `DBImpl::Recover()` separately discovers/replays qualifying log files for recent payload mutations. (`H/P`, `E`)
- **2916 — MANIFEST log frontier != complete recent payload history:** v1.7 explicitly anticipates a newer log file created by a previous incarnation without registration in the descriptor. (`H/P`, `E`)
- **2917 — candidate Version != installed current Version:** `LogAndApply()` builds a candidate, appends/syncs its VersionEdit in MANIFEST, performs CURRENT installation when needed, and only then calls `AppendVersion()` on success. (`H/P`, `E`)
- **2918 — synced compaction output != current serving member:** an output SSTable is finished, synced/closed, and checked before `InstallCompactionResults()` persists/adds it to the file-set relation. (`H/P`, `E`)
- **2919 — pending output != current serving membership:** `pending_outputs_` protects in-construction/new files from obsolete-file deletion even before ordinary Version membership is established. (`H/P`, `E`)
- **2920 — newest-Version supersession != immediate file reclamation:** `AddLiveFiles()` retains files referenced by every live Version, not only the newest current Version. (`H/P`, `E`)
- **2921 — reader-liveness can prolong physical file liveness:** `version_set.h` states older Versions may survive for live iterators, so a reader can indirectly keep superseded SSTables non-obsolete. (`H/P`, `E`)
- **2922 — current-Version transition != reclamation completion:** compaction installs its file-set edit before `DeleteObsoleteFiles()` removes files that no remaining liveness rule protects. (`H/P`, `E`)
- **2923 — metadata-log snapshot/rollover != complete-history retention:** a new MANIFEST can begin with `WriteSnapshot()` of current Version metadata and then receive later edits; preserving current reconstructability does not require one eternal metadata event stream. (`H/P`, `E`)
- **2924 — sync-temp + rename CURRENT != universal crash-durability theorem:** v1.7 `SetCurrentFile()` documents the application sequence, but Case 124's filesystem boundary prevents inferring durable directory replacement across every filesystem/device stack. (`H/P`, `A`, `X`)
- **2925 — obsolete-file deletion != media sanitization:** LevelDB filesystem deletion/reclamation does not establish overwrite, Flash erase, crypto erase, or forensic disappearance. (`E`, `X`)
- **2926 — LevelDB's “similar in spirit” Bigtable comparison != identical recovery contract:** the project-primary note supports a historical functional comparison while explicitly preserving different file organization; Case 57's `METADATA`/redo-point scheme is not silently renamed MANIFEST/CURRENT. (`H/P`, `A`, `X`)
- **2927 — `log` vocabulary != one retention role:** Kafka keyed logs, Bigtable commit logs, LevelDB user-update logs, and LevelDB MANIFEST logs retain different objects/relations despite shared append-log language. (`A`, `X`)
- **2928 — related-repository boundary:** fresh `computing-archaeology` searches for `LevelDB`, `MANIFEST`, `CURRENT`, `VersionSet`, and `LSM` found no dedicated overlapping case; broad LSM/LevelDB/RocksDB genealogy belongs there if developed, while Case 137 keeps the currentness/recovery/reclamation relation. (`H/P` project-state record)
'''
if "## Case 137 — LevelDB v1.7 MANIFEST/CURRENT current-state reconstruction findings" not in index:
    index = index.rstrip() + findings + "\n"
INDEX.write_text(index, encoding="utf-8")
