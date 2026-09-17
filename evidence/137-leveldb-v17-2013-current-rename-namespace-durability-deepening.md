# Case 137 deepening — LevelDB v1.7/2013 `CURRENT`: rename publication, namespace durability, and obsolete-file retirement

## Status

**`bounded deepening complete`**

This packet deepens [`../cases/137-leveldb-v17-manifest-current-recovery.md`](../cases/137-leveldb-v17-manifest-current-recovery.md) at one narrow boundary left explicit by the canonical case:

> In LevelDB v1.7, a new MANIFEST is synced before `CURRENT` is replaced through a synced temporary file plus `rename()`. What exactly has crossed a persistence boundary at each step, and what may still depend on filesystem namespace-durability ordering before old metadata/log files are retired?

The bounded historical/implementation witnesses are:

- Google LevelDB tag **v1.7**, commit `40768657bc8ec3ded60712eeeab7c25b1b07deca` (16 October 2012 UTC), especially `db/version_set.cc`, `db/filename.cc`, `db/db_impl.cc`, and `util/env*.cc`;
- original LevelDB issue **189**, created **2013-07-17**, preserved as GitHub issue **#195**, “Possible bug: fsync() required after calling rename()”;
- current upstream `db/filename.cc`, inspected only as a later source-continuity witness, not as a statement that every current platform has the same crash behavior.

This packet does **not** establish a reproduced corruption on ext3/ext4, does not establish a universal POSIX crash model, and does not claim that LevelDB's `rename()` lacks atomic namespace visibility. The concern is narrower: **durability/order of the pathname relation across sudden failure and later namespace deletion**.

## Evidence classes

- **H/P — historical / implementation record:** exact LevelDB v1.7 source and the dated 2013 upstream issue record.
- **E — engineering reconstruction:** separation among MANIFEST contents, `CURRENT` contents, rename visibility, directory-entry persistence, restart authority, and retirement of old files.
- **A — functional analogy:** bounded comparison with Case 124's rename/fsync closure and Case 58's etcd snapshot-directory fsync correction.
- **P — philosophical interpretation:** a narrow statement that retained bytes can remain unusable as the intended restart object if the retained designation relation is lost or ambiguous.

## Research question

Case 137 already establishes that LevelDB recovery is relational:

```text
CURRENT
    -> names one MANIFEST
    -> MANIFEST replay reconstructs VersionSet/current file membership
    -> newer WAL/log files may still contribute recent payload history
```

The missing lower-layer question is whether these two propositions are equivalent:

```text
A. the new MANIFEST file contents were synced
B. the new MANIFEST became the crash-durable MANIFEST selected by CURRENT
```

They are not the same proposition in the v1.7 source path.

The packet therefore isolates a **root-pointer publication frontier**:

```text
new metadata embodiment exists
    != new metadata embodiment is selected by CURRENT
    != CURRENT rename is durably retained in the containing namespace
    != old recovery roots are safe to retire under every crash model
```

`root-pointer publication frontier` is a project engineering term, not LevelDB vocabulary.

---

## Historical / implementation record

### H/P — v1.7 syncs the MANIFEST record before installing a newly created MANIFEST through `CURRENT`

In `VersionSet::LogAndApply()`, v1.7 first creates a new descriptor/MANIFEST if needed, writes a snapshot, appends the encoded `VersionEdit`, and calls:

```cpp
s = descriptor_file_->Sync();
```

Only after that succeeds, when the path is using a newly created descriptor file, the code executes:

```cpp
s = SetCurrentFile(env_, dbname_, manifest_file_number_);
```

Only after the I/O block succeeds does `AppendVersion(v)` make the candidate Version current in memory.

Primary source:

- LevelDB v1.7 `db/version_set.cc`: <https://github.com/google/leveldb/blob/v1.7/db/version_set.cc>

Bounded ordering:

```text
new MANIFEST embodiment
    -> append VersionEdit
    -> Sync MANIFEST file
    -> SetCurrentFile(...)
    -> AppendVersion(...) in memory
```

This is already enough to reject one collapse:

> **MANIFEST file durability != `CURRENT` publication.**

The metadata artifact can cross its own file-sync boundary before the selector naming it is replaced.

### H/P — `SetCurrentFile()` separately syncs a temporary pointer file and then renames it to `CURRENT`

In v1.7 `db/filename.cc`, `SetCurrentFile()` forms the target `MANIFEST-%06llu` name, writes that name plus newline to a temporary `*.dbtmp` file through `WriteStringToFileSync()`, and only then calls:

```cpp
env->RenameFile(tmp, CurrentFileName(dbname));
```

If the operation fails, the temporary file is deleted.

Primary source:

- LevelDB v1.7 `db/filename.cc`: <https://github.com/google/leveldb/blob/v1.7/db/filename.cc>

This creates a second decomposition:

```text
MANIFEST contents synced
    != temporary CURRENT contents synced
    != temporary name renamed to CURRENT
```

The purpose of the temporary file is not disputed here. The narrower question is what the subsequent `RenameFile()` means for crash persistence on the active `Env`/filesystem.

### H/P — `WriteStringToFileSync()` asks the file object to `Sync()`; it does not itself synchronize the containing directory

In v1.7 `util/env.cc`, `WriteStringToFileSync()` delegates to `DoWriteStringToFile(..., should_sync=true)`. That helper:

1. creates a writable file;
2. appends the data;
3. calls `file->Sync()` when `should_sync` is true;
4. closes the file.

It does not contain an operation that synchronizes the parent directory after a later rename.

Primary source:

- LevelDB v1.7 `util/env.cc`: <https://github.com/google/leveldb/blob/v1.7/util/env.cc>

Therefore the source-level claim is limited to the file object passed through `WritableFile::Sync()`:

> **synced temporary-file contents != independently demonstrated containing-directory durability.**

The exact lower-layer semantics still depend on the `Env` implementation and filesystem/storage contract.

### H/P — the v1.7 POSIX `RenameFile()` implementation is a direct `rename(2)` wrapper

In `util/env_posix.cc`, v1.7 implements `PosixEnv::RenameFile()` by calling:

```cpp
rename(src.c_str(), target.c_str())
```

and returning an I/O error on failure. The function contains no subsequent `fsync()` of the database directory.

The same `PosixEnv` implements `DeleteFile()` as a direct `unlink()` call.

Primary source:

- LevelDB v1.7 `util/env_posix.cc`: <https://github.com/google/leveldb/blob/v1.7/util/env_posix.cc>

This is a source-level fact about this implementation. It is not by itself a universal claim about what every Unix filesystem will preserve after power failure.

### H/P — recovery treats `CURRENT` as the restart root that chooses which MANIFEST is interpreted

`VersionSet::Recover()` in v1.7 explicitly begins by reading `CURRENT`, checks that it ends in a newline, strips the newline, constructs the named descriptor path, and opens that MANIFEST. It then replays its checksummed records into a `Builder` before installing the recovered Version.

Primary source:

- LevelDB v1.7 `db/version_set.cc`: <https://github.com/google/leveldb/blob/v1.7/db/version_set.cc>

Thus the pathname/content relation of `CURRENT` is not decorative metadata:

```text
CURRENT bytes/name relation
    -> choose MANIFEST history
    -> reconstruct VersionSet
```

If a particular MANIFEST's contents survive but the restart path no longer selects it, artifact survival and restart authority have diverged.

### H/P — obsolete descriptors/logs are actively deleted after the new state has been accepted by LevelDB's higher-level control flow

`DBImpl::DeleteObsoleteFiles()` enumerates database-directory files and applies type-specific liveness rules. For descriptor files, v1.7 keeps the current MANIFEST number and newer incarnations and deletes older descriptors. Obsolete log files and obsolete tables are likewise unlinked according to their own liveness conditions.

At open/recovery, after `VersionSet::LogAndApply()` succeeds, `DB::Open()` calls `DeleteObsoleteFiles()`. Compaction paths likewise install the resulting Version edit and subsequently invoke obsolete-file deletion.

Primary source:

- LevelDB v1.7 `db/db_impl.cc`: <https://github.com/google/leveldb/blob/v1.7/db/db_impl.cc>

This matters because restart publication and retirement form a directional relationship:

```text
new restart root accepted
    -> old metadata/log names may become eligible for unlink
```

The code does not preserve all historical recovery roots indefinitely.

### H/P — the 2013 upstream issue identified exactly the rename-vs-unlink persistence-order concern

Original LevelDB issue 189 was created on **2013-07-17** and later migrated to GitHub as issue **#195**, titled “Possible bug: fsync() required after calling rename()”. The report describes the open/recovery sequence as:

```text
compact current logs to SST
    -> create new MANIFEST
    -> update CURRENT via rename
    -> delete old logs and old MANIFEST
```

The reporter's concern was that LevelDB did not explicitly ensure the `CURRENT` rename had become persistent before the later unlink operations became persistent. The report says that if the unlink operations were to survive while the rename did not, restart could encounter a missing old MANIFEST or deleted log needed by the old root.

Primary issue record:

- LevelDB issue #195: <https://github.com/google/leveldb/issues/195>

The issue preserves two critical limits that must travel with the claim:

1. the reporter explicitly said the problem was **not reproduced on the ext3/ext4 filesystems they normally used**;
2. the motivation was portability / unspecified ordering across other operating systems and filesystems, not a demonstrated universal Linux corruption.

As inspected in this round, the migrated GitHub issue remains open. Open issue status is not proof that the report is correct in every detail, nor is it a maintained specification.

### H/P — the current upstream `SetCurrentFile()` source still exhibits the same local temp-sync-then-rename shape

Current upstream `db/filename.cc`, inspected in this round, still writes the temporary pointer through `WriteStringToFileSync()` and then calls `env->RenameFile(tmp, CurrentFileName(dbname))`; the function itself does not add an explicit parent-directory sync after the rename.

Current source:

- LevelDB `main`, `db/filename.cc`: <https://github.com/google/leveldb/blob/main/db/filename.cc>

This is only a **source-shape continuity witness**. It does not prove:

- that every current `Env` implementation maps to the same syscalls;
- that every filesystem/storage stack needs the same explicit operation;
- that issue #195 remains exploitable;
- that no durability work happens elsewhere in a caller/platform layer.

---

## Engineering reconstruction

### E — durable metadata embodiment != durable metadata designation

The new MANIFEST contains the metadata history LevelDB intends to use. `CURRENT` separately names which MANIFEST recovery should interpret.

Therefore:

```text
MANIFEST contents survive
    != recovery is guaranteed to select that MANIFEST
```

The content object and the designation relation have different persistence paths.

### E — synced temporary `CURRENT` file != durable final `CURRENT` pathname

`WriteStringToFileSync()` closes one obligation for the temporary file object. The later `rename()` changes the namespace relation.

Under the Linux interface boundary documented in Case 124, these are not automatically the same persistence target:

```text
file object durability
    != containing-directory entry durability
```

This packet does not import Linux behavior into every LevelDB `Env`; it uses the distinction to prevent an unjustified source-level inference.

### E — atomic rename visibility != crash-persistent publication

An atomic replacement operation can make `CURRENT` change from old to new without exposing an intermediate ordinary namespace state to concurrent observers. That says something different from which directory state survives a sudden crash.

Therefore:

```text
atomic observer-visible replacement
    != explicit post-crash namespace-durability closure
```

Calling the latter question a “rename atomicity bug” would blur two different contracts.

### E — restart-root publication and old-root retirement form a safety ordering

A generic safe handoff has the shape:

```text
prepare new recovery metadata
    -> make new recovery root durable/authoritative
    -> only then retire data needed solely by the old recovery root
```

LevelDB v1.7 clearly performs the higher-level operations in that program order. The 2013 issue asks whether the persistence layer is guaranteed to preserve the same order across crash for `rename(CURRENT)` and later `unlink()` operations.

The issue is therefore not simply “a file was unsynced.” It is a **cross-object retirement-order question**.

### E — API success != filesystem-independent power-fail theorem

At the LevelDB layer, successful `RenameFile()` is enough for `SetCurrentFile()` to return success, and successful higher-level application may make older files eligible for deletion.

The source does not, in this path, encode a separate explicit parent-directory durability acknowledgement.

Hence:

```text
RenameFile() success at Env/API layer
    != independently proven namespace persistence on every backend
```

This is an evidence boundary, not a declaration that the API contract is defective on all platforms.

### E — orphan-new metadata and missing-old authority are asymmetric failure shapes

Before the new `CURRENT` publication is durable, a newly created MANIFEST can exist without being selected after restart. Such an unselected new MANIFEST is conceptually an **orphan candidate** rather than automatically a corrupt current state.

The more dangerous theoretical direction described by issue #195 is different:

```text
old CURRENT relation survives crash
    + old MANIFEST/log already retired
    -> restart root may refer to state whose required objects no longer exist
```

This is why retirement ordering matters independently of the durability of the new artifact itself.

### E — currentness is a retained graph edge, not an intrinsic property of MANIFEST bytes

The same MANIFEST file bytes do not intrinsically announce “I am current.” Currentness arises from a relation:

```text
CURRENT -> MANIFEST-N
```

and from the recovery procedure that interprets this relation.

This reinforces the canonical Case 137 proposition:

> **physical survival != current membership.**

The deepening adds:

> **durable candidate metadata != durably published currentness.**

---

## Crash-window matrix — bounded reconstruction

The following matrix is deliberately qualitative. It does not pretend that one ordering is guaranteed on every filesystem.

| Point reached in program order | New MANIFEST file | Temp pointer file | Live namespace | Old recovery files | Bounded interpretation |
| --- | --- | --- | --- | --- | --- |
| before MANIFEST sync | created/dirty or partial | absent | old CURRENT | retained | new metadata not yet at its explicit file-sync frontier |
| after MANIFEST sync | sync requested/completed at file layer | absent | old CURRENT | retained | new metadata embodiment is ahead of publication |
| after temp pointer sync | new MANIFEST synced | temp pointer synced | old CURRENT | retained | intended pointer contents exist but final designation has not changed |
| after `rename(temp, CURRENT)` returns | new MANIFEST synced | consumed/replaced by rename | process observes new CURRENT | normally retained until later cleanup | publication visible at API/namespace level; crash persistence remains backend-qualified |
| after obsolete-file deletion calls | new MANIFEST intended current | — | process uses new CURRENT | old names may be removed | correctness now depends on publication/retirement ordering supplied by the persistence stack |

The matrix does not claim that ext3/ext4 reorder these operations harmfully; the 2013 reporter explicitly said they had not reproduced the problem there.

---

## Functional comparisons

### A — Case 124: Linux ext4 rename/fsync durability closure

Case 124 establishes a general Linux distinction:

```text
rename visibility atomicity
    != file durability
    != containing-directory entry durability
```

Case 137 supplies an application-level instance in which the directory relation is also a **recovery-selection relation**: `CURRENT` decides which MANIFEST recovery interprets.

The comparison is functional, not genealogical. The 2009 ext4 interventions did not create LevelDB's MANIFEST design, and LevelDB's `Env` abstraction is not identical to ext4.

See:

- [`../cases/124-linux-ext4-rename-fsync-durability-closure.md`](../cases/124-linux-ext4-rename-fsync-durability-closure.md)

### A — Case 58: etcd received-snapshot directory fsync correction

Case 58's 2026 etcd deepening provides a useful contrast. There, upstream later changed the received snapshot DB path so that, after the final rename, the containing snapshot directory is explicitly synced before save success is returned and the Raft message is processed.

That yields a similar shape:

```text
file content durability
    -> namespace mutation
    -> namespace durability closure
    -> higher-level publication
```

But the retained objects differ:

- etcd: a received snapshot DB pathname participating in a Raft snapshot receive path;
- LevelDB: the `CURRENT` root pointer selecting a MANIFEST history.

The comparison supports a persistence-boundary vocabulary, not a claim that the systems share implementation lineage or identical failure semantics.

See:

- [`58-etcd-2026-received-snapshot-db-directory-fsync-deepening.md`](58-etcd-2026-received-snapshot-db-directory-fsync-deepening.md)

### A — PostgreSQL durable rename evidence under Case 124

Case 124's PostgreSQL deepening records a production implementation that explicitly synchronizes namespace state around durable rename and a WAL-recycling failure in which durable file contents under the wrong filename were insufficient for correct recovery.

That supplies a design contrast:

```text
bytes durable
    != name/content identity durable
    != recovery closure
```

Again, this is not evidence that LevelDB must copy PostgreSQL's exact syscall sequence or that their metadata protocols are the same.

---

## Prior-art and chronology boundary

The chronology established by this packet is intentionally narrow:

- **2012-10-16:** LevelDB v1.7 is a released/tagged source witness for the MANIFEST sync → temporary pointer sync → `CURRENT` rename path and for later obsolete-file deletion.
- **2013-07-17:** original issue 189 records an explicit power-failure/portability concern about whether `CURRENT` rename persistence is ordered before old-file unlink persistence.
- **current upstream inspected in 2026:** `SetCurrentFile()` still has the same local temp-sync-then-rename shape in `db/filename.cc`.

This does not establish:

- the first invention of manifest-pointer replacement;
- the first database to notice directory fsync;
- the first report of rename/unlink crash ordering;
- a complete LevelDB issue-resolution genealogy;
- a RocksDB lineage claim.

Broader database/filesystem genealogy belongs in `computing-archaeology` if developed.

---

## Philosophical interpretation — bounded

### P — retained access can depend on retaining the designation relation

This case gives a precise technical example of why “the bytes still exist” is not always equivalent to “the intended object survives.”

A MANIFEST may be present and internally readable, yet LevelDB restart normally reaches a MANIFEST through `CURRENT`. The retained relation:

```text
CURRENT -> selected MANIFEST
```

is therefore constitutive of ordinary restart accessibility/currentness.

The philosophical inference is limited to:

> **retention of an embodiment and retention of the relation that designates it for future interpretation can be separate technical obligations.**

This is not a claim that filenames are inherently semantic, that metadata is metaphysically prior to data, or that every pointer file is a philosophical “memory.”

---

## Explicit non-claims

This packet does **not** claim:

1. that LevelDB v1.7 corrupts on every power failure;
2. that issue #195 was reproduced on ext3 or ext4;
3. that `rename()` is non-atomic for ordinary namespace observers;
4. that POSIX promises one universal sudden-power-loss persistence ordering for all filesystems;
5. that LevelDB's generic `Env::RenameFile` always maps to the v1.7 POSIX implementation;
6. that a directory `fsync()` is necessarily the correct primitive on every non-POSIX backend;
7. that the v1.7 source proves what a drive controller physically persisted after cache/power failure;
8. that `descriptor_file_->Sync()` is equivalent to durable `CURRENT` publication;
9. that syncing the temporary CURRENT file automatically syncs the later rename;
10. that the 2013 issue reporter's proposed concern is an upstream-maintainer specification;
11. that open issue status proves present-day exploitability;
12. that current `db/filename.cc` alone proves no durability work occurs elsewhere;
13. that all old MANIFEST/log files are deleted immediately after every CURRENT replacement;
14. that an orphan new MANIFEST is necessarily harmful;
15. that losing a new MANIFEST while retaining the old complete recovery root necessarily corrupts the database;
16. that LevelDB and etcd have the same recovery architecture;
17. that LevelDB and PostgreSQL require identical durable-rename sequences;
18. that `CURRENT` contains user payload;
19. that MANIFEST is the user-update WAL;
20. that this packet closes lower-layer media persistence or secure-erasure questions.

---

## Claim ledger

| Claim | Evidence class | Strength | Stop condition |
| --- | --- | --- | --- |
| v1.7 syncs MANIFEST records before `SetCurrentFile()` when installing a new descriptor | H/P | strong primary source | bounded to inspected v1.7 path |
| `SetCurrentFile()` syncs a temp pointer file then calls `RenameFile()` to replace CURRENT | H/P | strong primary source | does not itself define crash durability |
| v1.7 POSIX `RenameFile()` directly wraps `rename()` without parent-directory fsync in that function | H/P | strong primary source | POSIX Env only |
| recovery reads CURRENT first and opens the named MANIFEST | H/P | strong primary source | ordinary inspected recovery path |
| v1.7 obsolete-file cleanup can unlink older descriptor/log/table names after state installation | H/P | strong primary source | type/liveness rules still apply |
| 2013 issue 189/#195 explicitly raised rename-vs-unlink crash-order portability | H/P | dated upstream issue record | contributor report, not universal proof |
| issue reporter did not reproduce the bug on ext3/ext4 | H/P | explicit negative boundary | says nothing about all versions/modes |
| durable MANIFEST contents and durable CURRENT designation are separate engineering obligations | E | strong reconstruction from source decomposition | lower-layer exact contract remains backend-specific |
| restart-root publication should precede retirement of state required by the old root | E | bounded safety reconstruction | not claimed as LevelDB's period terminology |
| retained objecthood can depend on retained designation relation | P | bounded interpretation | not historical vocabulary |

---

## Related-repository check

Fresh searches of `tmzncty/computing-archaeology` for `LevelDB` returned no dedicated overlapping packet during this round.

Division of labor remains:

- `technical-retention`: MANIFEST embodiment vs `CURRENT` designation, restart-authority publication, obsolete-root retirement, and cross-case durability boundaries;
- `computing-archaeology`: broader LSM/database genealogy, exact first-introduction commits, LevelDB→RocksDB evolution, filesystem history, and platform-specific durability evolution.

No parallel technical history was created here.

---

## Remaining evidence debt

This packet closes the **source-level v1.7 CURRENT rename / namespace-persistence seam** as a bounded documented concern, not as a universal reproduced defect. Remaining useful slices are narrower:

- controlled fault injection on selected historical LevelDB + filesystem combinations across MANIFEST sync, CURRENT rename, and old-file unlink;
- exact issue/commit genealogy after 2013: whether particular platforms or descendants added directory-durability closure elsewhere;
- Windows/non-POSIX `Env` behavior and its restart guarantees;
- precise initial-DB creation durability (`NewDB()` has a different MANIFEST close/sync shape and deserves its own bounded analysis if pursued);
- later LevelDB/RocksDB MANIFEST rollover implementations and explicit durability documentation;
- lower storage-stack validation beneath file/directory synchronization requests.

None of these are blockers for the narrower conclusion established here:

> **LevelDB v1.7 separately persists MANIFEST contents and publishes a MANIFEST choice through `CURRENT`; the POSIX `SetCurrentFile()` path syncs the temporary pointer file and then performs a plain rename, while a 2013 upstream issue explicitly recognized that crash-persistent ordering between that rename and later old-file unlink operations is a distinct filesystem-dependent question.**
