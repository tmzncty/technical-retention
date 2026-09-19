# Evidence 137C — LevelDB 2012 `CURRENT` Content-Sync Fix: File-Content Durability Before Namespace Publication

**Status:** bounded deepening complete  
**Case:** [`../cases/137-leveldb-v17-manifest-current-recovery.md`](../cases/137-leveldb-v17-manifest-current-recovery.md)  
**Primary slice:** original LevelDB issue 68 (16 January 2012), maintainer response, and upstream fix `3c8be108bfb5fbd7d51f824199627e757279f79e` (25 January 2012)  
**Claim layers:** historical record + engineering reconstruction + bounded functional comparison + bounded philosophical interpretation

## Research question

Case 137 already establishes, for LevelDB v1.7 and later source witnesses, that `CURRENT` is a small restart selector naming the MANIFEST ordinary recovery should interpret, and that the selector has at least two lower-level persistence problems:

1. are the bytes naming the MANIFEST durably written to the temporary file before publication?;
2. is the final pathname relation created by `rename()` itself crash-persistent before old recovery material is retired?

The previous deepening concentrated on the second question through the 2013 rename/fsync report. This slice asks the earlier and narrower question:

> **When did the inspected LevelDB line acquire an explicit file-content `Sync()` for the temporary `CURRENT` contents, and what does that fix establish — and not establish — about the larger restart-root publication protocol?**

The bounded answer is unusually clean because an original issue report, a maintainer acknowledgement, and the exact fixing diff survive.

## Source ladder

| Source | Date | Role | Strength / limit |
| --- | --- | --- | --- |
| LevelDB original issue 68, migrated as GitHub issue #74 | 2012-01-16 | field report of corrupted `CURRENT` after forced power-off | primary participant report; one environment/report, not a universal filesystem law |
| Sanjay Ghemawat comment on original issue 68 | 2012-01-18 | maintainer acknowledgement and recovery advice | primary project response |
| LevelDB commit `3c8be108...` | 2012-01-25 | exact source change adding explicit sync to the temporary `CURRENT` content path | strongest mechanism witness for this slice |
| parent `c8c5866...`, `db/filename.cc` and `util/env.cc` | immediately pre-fix | direct preimage of the affected path | source-level negative witness: append/close path contains no explicit `Sync()` |
| LevelDB v1.7, `40768657...` | 2012-10-16 | later release baseline used by canonical Case 137 | establishes the fix is already present by the canonical baseline |
| original 2013 issue 189 / migrated #195 | 2013-07-17 | later namespace-publication / rename-vs-unlink concern | distinct later persistence frontier; must not be collapsed into issue 68 |

## Historical record

### H/P — original issue 68 reports a `CURRENT` corruption window on forced power-off

The migrated GitHub issue #74 preserves original Google Code issue 68 with an original creation timestamp of **16 January 2012**.

The reporter describes this bounded sequence:

1. open an existing database;
2. forcibly power off the computer within roughly 30 seconds;
3. reboot;
4. observe that `CURRENT` can no longer be used to open the database.

In the reported instance, the file contained sixteen zero bytes instead of the expected MANIFEST name. The report identifies Ubuntu Server 10.10 and the LevelDB copy bundled with Riak 1.0.2 / `eleveldb` as the environment under test.

The reporter further states that the application-level write `sync` option did not change the outcome and that their testing indicated `CURRENT` was not explicitly synchronized; waiting substantially longer before power-off avoided the reproduced corruption in that environment.

This is **field evidence**, not a universal proof about every filesystem, storage stack, LevelDB build, crash timing, or Riak deployment.

Primary record: <https://github.com/google/leveldb/issues/74>

### H/P — the maintainer accepted the diagnosis rather than treating it as only user speculation

A migrated comment preserves Sanjay Ghemawat's **18 January 2012** response. He says the report is correct and that a fix is being prepared. He also gives a bounded recovery suggestion: replace the corrupt `CURRENT` with a line naming the newest MANIFEST that appears nonempty, and first try that procedure on a copy of the database directory.

The recovery suggestion is useful evidence of the role of `CURRENT`: corruption of the selector can make ordinary opening fail even while candidate MANIFEST material still survives.

It is **not** an algorithmic proof that the highest-numbered or newest nonempty MANIFEST is always the semantically correct recovery root under every crash history. The maintainer's own caution to work on a copy should be preserved as part of the historical record.

Comments: <https://github.com/google/leveldb/issues/74#issuecomment-55005500>

### H/P — the 25 January 2012 upstream commit names issue 68 as “no sync of CURRENT file”

Upstream commit `3c8be108bfb5fbd7d51f824199627e757279f79e`, authored/committed by Sanjay Ghemawat on **25 January 2012**, has the message:

> `fixed issues 66 (leaking files on disk error) and 68 (no sync of CURRENT file)`

The migrated issue thread separately records the maintainer marking issue 68 fixed by that change.

This commit also contains changes for issue 66. The Case 137 claim here is restricted to the `CURRENT`-related hunks in `db/filename.cc` and `util/env.cc`; unrelated compaction/no-space changes must not be attributed to the durability fix.

Commit: <https://github.com/google/leveldb/commit/3c8be108bfb5fbd7d51f824199627e757279f79e>

Issue closure comment: <https://github.com/google/leveldb/issues/74#issuecomment-55005505>

### H/P — the pre-fix `SetCurrentFile()` path writes the temporary selector through the non-sync helper

In the parent commit `c8c5866a86c8d4a3e80d8708d14a06776fb683d1`, `SetCurrentFile()` constructs the MANIFEST basename, writes that text plus a newline to a temporary file using:

```cpp
WriteStringToFile(env, contents.ToString() + "\n", tmp)
```

and, if that succeeds, renames the temporary path to `CURRENT`.

The contemporaneous pre-fix `WriteStringToFile()` implementation:

1. creates a writable file;
2. appends the bytes;
3. closes the file;
4. deletes it on failure.

There is no explicit `file->Sync()` in that helper.

Pre-fix sources:

- <https://github.com/google/leveldb/blob/c8c5866a86c8d4a3e80d8708d14a06776fb683d1/db/filename.cc>
- <https://github.com/google/leveldb/blob/c8c5866a86c8d4a3e80d8708d14a06776fb683d1/util/env.cc>

This is a source-level statement about the inspected path. It does not assert what a particular filesystem, kernel, drive cache, or power-loss sequence may happen to persist despite the missing explicit call.

### H/P — the fix changes that exact path to `WriteStringToFileSync()`

The fixing diff changes the `SetCurrentFile()` call from `WriteStringToFile(...)` to `WriteStringToFileSync(...)` while retaining the subsequent rename to `CURRENT`.

The same commit refactors the helper into `DoWriteStringToFile(..., bool should_sync)` and, when `should_sync` is true, executes:

```cpp
file->Sync();
```

before closing the file.

Thus the bounded source transition is:

```text
pre-fix:
    create temp selector
    -> append MANIFEST name
    -> close
    -> rename temp to CURRENT

post-fix:
    create temp selector
    -> append MANIFEST name
    -> file Sync()
    -> close
    -> rename temp to CURRENT
```

Post-fix sources:

- <https://github.com/google/leveldb/blob/3c8be108bfb5fbd7d51f824199627e757279f79e/db/filename.cc>
- <https://github.com/google/leveldb/blob/3c8be108bfb5fbd7d51f824199627e757279f79e/util/env.cc>

### H/P — the v1.7 canonical baseline already contains the content-sync fix

Case 137's main frozen baseline is LevelDB v1.7, commit `40768657bc8ec3ded60712eeeab7c25b1b07deca`, dated 16 October 2012.

That source uses `WriteStringToFileSync()` for the temporary selector and then renames it to `CURRENT`. Therefore the January 2012 fix is part of the implementation inherited by the canonical v1.7 analysis.

This deepening changes the chronology from merely:

```text
by v1.7 (October 2012): temp CURRENT content is explicitly synced
```

to the stronger but still bounded sequence:

```text
16 Jan 2012: field report identifies missing explicit CURRENT sync
18 Jan 2012: maintainer accepts diagnosis
25 Jan 2012: upstream source adds explicit temp-CURRENT file Sync()
16 Oct 2012: v1.7 baseline contains that path
17 Jul 2013: separate rename/directory persistence-order concern is raised
```

The January fix date is **not** the invention date of `CURRENT`, MANIFEST selection, atomic rename, database metadata persistence, or crash-safe root publication.

### H/P — issue 68 and the 2013 rename/fsync issue concern different persistence frontiers

The 2012 patch makes the temporary `CURRENT` file's **contents** pass through the Env's file `Sync()` before rename.

The later 2013 report preserved as issue #195 asks a different question: after rename publishes the new `CURRENT` pathname, can a filesystem crash preserve later old-file `unlink()` operations while failing to preserve the rename itself? The concern is therefore about **namespace persistence / cross-object retirement ordering**, not whether the temporary file's contents were explicitly synced.

The historical sequence itself demonstrates why these should be kept separate:

```text
2012 fix:
    selector bytes / file-content persistence

2013 concern:
    selector pathname publication
    + ordering against retirement of old recovery files
```

A fix to the first does not logically or historically entail closure of the second.

## Engineering reconstruction

### E — restart-root retention has at least a content layer and a designation layer

For the bounded `CURRENT` protocol, a useful decomposition is:

```text
C1 = bytes containing "MANIFEST-N\n" exist in a file
C2 = those bytes have crossed the file Sync() boundary requested by LevelDB
C3 = pathname CURRENT designates that file after rename
C4 = that pathname update has crossed the relevant namespace crash-persistence boundary
C5 = old recovery-root material may be retired without stranding restart
```

The January 2012 change directly strengthens the transition from `C1` toward `C2`. It does not itself prove `C4` or `C5`.

Therefore:

> **selector content synchronized != selector namespace publication durably closed.**

### E — application write sync policy and recovery-selector sync are different controls

The issue reporter specifically says changing LevelDB's ordinary write `sync` option did not alter the reproduced problem. The source change is correspondingly in the helper used to publish `CURRENT`, not in the user-write WAL option path.

At the bounded interface level:

```text
user mutation WriteOptions.sync
    !=
CURRENT metadata file Sync()
```

This is an important maintenance/durability-state distinction: making payload-update acknowledgements stricter does not automatically strengthen every independent recovery-metadata publication path.

The field report alone does not prove every possible `sync=true` workload has the same failure behavior; the safe conclusion is that the repaired path was independently missing its own explicit synchronization.

### E — append/close is not interchangeable with an explicit durability request

The pre-fix helper appended and closed the temporary file. The project should not rewrite that as “nothing was ever persisted.” Filesystems may persist data asynchronously, and a close can be followed by later writeback.

The narrower relation is:

> **file was successfully appended/closed != application explicitly requested the Env's file `Sync()` before publication.**

The 2012 patch is evidence that the LevelDB maintainers considered that distinction operationally relevant for `CURRENT`.

### E — one persistence fix can expose the next unclosed frontier

The later 2013 issue is not evidence that the 2012 fix was useless. It demonstrates a layered protocol:

```text
selector payload bytes
    -> selector file-content persistence request
    -> selector namespace replacement
    -> namespace persistence ordering
    -> old-root retirement
```

Closing an earlier frontier can still leave a later one vulnerable under a different failure model.

> **fixing file-content durability != proving end-to-end restart-root durability.**

### E — selector corruption can be logically catastrophic while payload embodiments survive

The maintainer's recovery advice presupposes that a corrupt `CURRENT` can coexist with usable MANIFEST material. That yields a precise retention boundary:

```text
MANIFEST material survives
    + selector unusable
    -> ordinary restart can fail
```

and, conversely:

```text
re-established selector
    -> may restore interpretive reach to surviving recovery metadata
```

This is not equivalent to reconstructing lost user payload, and manual selection of a candidate MANIFEST requires care.

### E — a root pointer is small but can carry large recovery authority

`CURRENT` contains little data compared with SSTables and logs, yet it decides which MANIFEST history ordinary recovery starts from.

The engineering importance of a retained state is therefore not proportional to its byte size:

> **small control state can have large currentness/recovery authority.**

This is a project reconstruction, not LevelDB's historical terminology.

## Functional comparisons

### A — Case 124: ext4 rename/fsync durability closure

Case 124 separates file contents, rename visibility, and directory-entry durability. Case 137 provides an application-level historical sequence in which those distinctions become visible as **two separate bug/concern generations**:

- 2012: explicit content sync for the temporary selector is added;
- 2013: rename/directory persistence ordering is separately questioned.

The comparison is functional only. ext4 does not define every LevelDB `Env`, and LevelDB's bug history is not an ext4 genealogy.

### A — Case 58: etcd snapshot publication

The etcd received-snapshot deepening records a later implementation explicitly syncing a containing directory after final rename. The common functional shape is:

```text
content persistence
    != namespace publication
    != higher-level recovery admission
```

The objects and protocols differ: LevelDB publishes a MANIFEST selector; etcd publishes received snapshot material in a Raft recovery path.

### A — Case 137 baseline: candidate MANIFEST versus CURRENT designation

The January 2012 fix is not a new state class separate from the canonical case. It deepens one transition inside the existing relation:

```text
synced MANIFEST candidate
    -> synchronized selector-file contents
    -> renamed CURRENT designation
```

It therefore belongs in Case 137 rather than becoming a duplicate new case.

## Philosophical interpretation — bounded

One narrow interpretation survives the mechanism:

> **Technical persistence can depend on preserving not only an embodiment but the small designation relation that tells a later system which embodiment to treat as current.**

The January 2012 record sharpens that idea further. Even the designation relation has layers: its text can be present, its file contents can be explicitly synchronized, and its namespace binding can still have a separate crash-persistence problem.

This is an engineering-derived interpretation. It does not make filenames “memory” in a human sense, establish a metaphysics of reference, or imply that metadata is ontologically prior to payload.

## Explicit non-claims

This slice does **not** claim:

1. LevelDB invented MANIFEST files, root pointers, atomic rename, WAL, LSM trees, or crash-safe metadata publication.
2. 16 January 2012 is the first date anyone noticed this class of persistence bug.
3. `3c8be108...` is the first commit introducing `CURRENT` or MANIFEST semantics.
4. The issue-68 report reproduces on every operating system, filesystem, storage controller, or LevelDB embedding.
5. Sixteen zero bytes are the only possible manifestation of pre-fix `CURRENT` loss.
6. `close()` means data is never persisted; the distinction is the absence of an explicit LevelDB file `Sync()` request in the inspected helper.
7. `file->Sync()` proves platter/NAND persistence under every hardware failure model.
8. The January 2012 change fsyncs the containing directory after `rename()`.
9. The January 2012 change closes the later 2013 rename-vs-unlink persistence-order concern.
10. Atomic `rename()` visibility is identical to post-crash directory-entry durability.
11. `WriteOptions.sync=true` and `CURRENT` publication are the same durability path.
12. A surviving MANIFEST is necessarily the correct one to select manually after every crash.
13. The maintainer's recovery suggestion is a universally safe automated recovery algorithm.
14. Rewriting `CURRENT` reconstructs user data that is actually absent from all logs/SSTables.
15. A corrupt `CURRENT` proves its referenced MANIFEST is corrupt.
16. A valid `CURRENT` proves every referenced SSTable/log is present and semantically valid.
17. The source diff establishes exact device-cache flush commands below the LevelDB `Env` abstraction.
18. The 2012 and 2013 reports share one identical root cause merely because both concern `CURRENT`.
19. The later v1.7 implementation is bit-for-bit identical to every January 2012 build or downstream Riak copy.
20. The bounded persistence relation proves any philosophical claim by itself.

## Claim ledger

| Claim | Layer | Evidence | Status / limit |
| --- | --- | --- | --- |
| Original issue 68 was created 16-Jan-2012 and reports `CURRENT` corruption after forced power-off in a named Ubuntu/Riak environment | H/P | migrated issue #74 | strong field report; bounded environment |
| Reporter says ordinary write `sync` setting did not alter the reproduced problem | H/P | migrated issue #74 | reporter observation; not universalized |
| Maintainer accepted the diagnosis on 18-Jan-2012 | H/P | migrated maintainer comment | strong project-participant evidence |
| Pre-fix `SetCurrentFile()` used non-sync `WriteStringToFile()` | H/P | parent source `c8c5866...` | direct source witness |
| Pre-fix helper has append + close but no explicit `file->Sync()` | H/P | parent `util/env.cc` | direct source witness |
| Commit `3c8be108...` dated 25-Jan-2012 names issue 68 as “no sync of CURRENT file” | H/P | upstream commit | direct primary evidence |
| Fix changes `SetCurrentFile()` to `WriteStringToFileSync()` | H/P | commit diff | direct source witness |
| Sync helper calls `file->Sync()` before close when requested | H/P | post-fix `util/env.cc` | direct source witness |
| v1.7 later contains this synced-temp-file path | H/P | frozen v1.7 source | strong bounded continuity |
| The 2012 content-sync fix and 2013 namespace-persistence concern are different frontiers | E/H | source chronology + two issue records | strong bounded decomposition |
| File-content Sync proves final `CURRENT` directory entry is crash-durable | X | not supported | rejected |
| User WAL sync automatically fixes CURRENT publication | X | issue/source paths separate | rejected |
| Corrupt selector can coexist with surviving candidate recovery metadata | E/H | maintainer recovery advice + architecture | strong bounded conclusion |
| Manual newest-MANIFEST selection is always correct | X | not established | rejected |

## Related-repository check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `LevelDB CURRENT MANIFEST` found no dedicated packet to reuse in this round.

Division of labor remains:

- `technical-retention`: selector content durability, designation/currentness relation, namespace-publication frontier, old-root retirement ordering, and consequences for restart legibility;
- `computing-archaeology`: broader LSM genealogy, pre-LevelDB metadata-root designs, Google Code / LevelDB implementation evolution, filesystem portability history, Riak/eleveldb integration history, and later RocksDB descendants.

The January 2012 patch is retained here only because it directly sharpens Case 137's persistence boundary.

## Remaining evidence debt

This slice closes only the narrow **pre-v1.7 `CURRENT` file-content Sync chronology**. Remaining work includes:

- exact first introduction of `CURRENT`, MANIFEST, and VersionSet before the January 2012 fix;
- direct reconstruction of the precise downstream Riak/eleveldb revision used by the original reporter;
- controlled fault injection across pre-fix and post-fix LevelDB on period filesystems;
- exact relationship between each historical `Env::Sync()` implementation and OS/device flush primitives;
- the full 2013 issue/commit/platform genealogy for namespace-persistence closure;
- Windows and other non-POSIX `Env` behavior;
- initial-database `NewDB()` publication semantics;
- later LevelDB/RocksDB recovery-root protocol evolution;
- lower-layer media persistence and sanitization, which remain separate concerns.

None of these require a maturity change. Case 137 remains **`grounded`**.

## Sources

1. LevelDB migrated issue #74, **CURRENT file is not synced**, preserving original Google Code issue 68 and original 16-Jan-2012 report: <https://github.com/google/leveldb/issues/74>.
2. Migrated maintainer comments on issue #74, preserving 18-Jan-2012 acknowledgement and 25-Jan-2012 fix note: <https://github.com/google/leveldb/issues/74#issuecomment-55005500> and <https://github.com/google/leveldb/issues/74#issuecomment-55005505>.
3. Google LevelDB commit `3c8be108bfb5fbd7d51f824199627e757279f79e`, 25-Jan-2012, **fixed issues 66 ... and 68 (no sync of CURRENT file)**: <https://github.com/google/leveldb/commit/3c8be108bfb5fbd7d51f824199627e757279f79e>.
4. Pre-fix `db/filename.cc` at parent `c8c5866...`: <https://github.com/google/leveldb/blob/c8c5866a86c8d4a3e80d8708d14a06776fb683d1/db/filename.cc>.
5. Pre-fix `util/env.cc` at parent `c8c5866...`: <https://github.com/google/leveldb/blob/c8c5866a86c8d4a3e80d8708d14a06776fb683d1/util/env.cc>.
6. Post-fix `db/filename.cc` at `3c8be108...`: <https://github.com/google/leveldb/blob/3c8be108bfb5fbd7d51f824199627e757279f79e/db/filename.cc>.
7. Post-fix `util/env.cc` at `3c8be108...`: <https://github.com/google/leveldb/blob/3c8be108bfb5fbd7d51f824199627e757279f79e/util/env.cc>.
8. Frozen LevelDB v1.7 `db/filename.cc`, commit `40768657bc8ec3ded60712eeeab7c25b1b07deca`: <https://github.com/google/leveldb/blob/40768657bc8ec3ded60712eeeab7c25b1b07deca/db/filename.cc>.
9. Existing Case 137 namespace-persistence deepening: [`137-leveldb-v17-2013-current-rename-namespace-durability-deepening.md`](137-leveldb-v17-2013-current-rename-namespace-durability-deepening.md).
