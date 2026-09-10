# LevelDB v1.7 MANIFEST/CURRENT: Current-State Reconstruction, Version Liveness, and Obsolete-File Retirement

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
