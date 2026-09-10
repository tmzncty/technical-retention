# Linux ext4 Replace-by-Rename: Atomic Visibility, `auto_da_alloc`, and `fsync` Durability Closure

## Scope

- **Bounded period:** the 2009 ext4 delayed-allocation intervention, checked against the current Linux interface/documentation contract through Linux man-pages 6.18 (2026).
- **Primary historical witnesses:** Linux commits `8750c6d5fcbd3342b3d908d157f81d345c5325a7` (24 February 2009) and `afd4672dc7610b7feef5190168aa917cc2e417e4` (17 March 2009), plus their June 2009 stable-review postings.
- **Current interface witnesses:** Linux `rename(2)` and `fsync(2)` man-pages 6.18, and current Linux ext4 documentation.
- **Research question:** when an application writes a replacement file and renames it over an existing pathname, which relation is made atomic, which state is merely ordered for later commit, and which durability obligations still require explicit synchronization?

This is not a general history of ext4, POSIX filesystems, journaling, or atomic file replacement. Case 16 already grounds BSD FFS soft updates and Case 74 grounds JBD revoke replay suppression. This case isolates a different boundary:

> **atomic pathname visibility, data-before-metadata ordering, file durability, and directory-entry durability are different retention relations.**

The 2009 ext4 workaround is treated as a historically specific compatibility/safety intervention, not as a portable durability theorem.

Application-level durability deepening: [2016 PostgreSQL `durable_rename` / WAL name-content deepening](../evidence/124-postgresql-2016-durable-rename-wal-name-content-deepening.md). It supplies a 2016 PostgreSQL production-source witness that durable file contents and durable namespace identity are separate recovery obligations.

---

## Historical vocabulary

Period and current Linux sources use terms including:

- `delayed allocation` / delay allocated blocks;
- `data=ordered`;
- `journal commit`;
- `rename`;
- `auto_da_alloc`;
- `fsync`;
- file data and file metadata;
- directory entry.

The following are project engineering terms:

- `visibility atomicity`;
- `namespace durability`;
- `durability closure`;
- `name→inode binding`;
- `compatibility heuristic`.

They describe relations supported by the sources; they are not projected backward as Theodore Ts'o's or POSIX's own terminology.

---

## Historical record

### H/P — the February 2009 ext4 rename patch targeted a crash window created by delayed allocation

Linux commit [`8750c6d5fcbd3342b3d908d157f81d345c5325a7`](https://github.com/torvalds/linux/commit/8750c6d5fcbd3342b3d908d157f81d345c5325a7), authored and committed by Theodore Ts'o on 24 February 2009, changes `ext4_rename()`. When a rename overwrites another inode, the patch forces delayed-allocation blocks to be allocated. Its commit message ties the behavior specifically to `data=ordered`: the data blocks can then be pushed out with the journal commit, avoiding a zero-length replacement file after an unexpected crash.

This is a dated implementation response to an ext4 failure window. It is not evidence that `rename()` itself had acquired a general crash-durability guarantee.

### H/P — `auto_da_alloc` made that safety behavior optional rather than defining a new rename syscall

Commit [`afd4672dc7610b7feef5190168aa917cc2e417e4`](https://github.com/torvalds/linux/commit/afd4672dc7610b7feef5190168aa917cc2e417e4), 17 March 2009, added an `auto_da_alloc` mount option allowing administrators to disable the automatic allocation behavior for truncate/overwrite-by-rename patterns. The commit describes the feature as protection from applications that relied on older practical behavior, while acknowledging a delayed-allocation performance cost.

The June 2009 stable-review posting preserves the same change and explicitly guards `force_da_alloc` behind `NO_AUTO_DA_ALLOC`.

Therefore:

```text
ext4 compatibility/safety policy
        ≠
portable rename durability contract
```

### H/P — current ext4 documentation still describes `auto_da_alloc` as a bounded ordering aid

Current Linux ext4 documentation describes replace-via-rename and replace-via-truncate as patterns in which applications may omit `fsync()`. With `auto_da_alloc` enabled, ext4 forces delayed-allocation blocks to be allocated so that, under the default `data=ordered` mode, new-file data is forced to disk before the rename operation is committed at the next journal commit.

The same documentation distinguishes data modes:

- `data=ordered`: associated data reaches the main filesystem before metadata commit;
- `data=writeback`: that ordering is not preserved;
- `data=journal`: data and metadata pass through the journal.

So even ext4's mitigation is configuration-qualified. `auto_da_alloc` is not evidence that every ext4 mode has the same crash relation.

### H/P — current Linux `rename(2)` grounds atomic replacement as an observer-visible namespace property

Linux man-pages 6.18 states that when `newpath` already exists, it is atomically replaced: another process does not observe a moment in which `newpath` is absent. This is a strong namespace visibility property.

The page does not say that successful return means the new directory entry and replacement payload have already become failure-surviving storage state.

### H/P — current Linux `fsync(2)` explicitly separates file synchronization from directory-entry synchronization

Linux man-pages 6.18 states that `fsync(fd)` flushes a file's modified in-core data and associated file metadata to the storage device and waits for completion. It then explicitly warns that synchronizing the file does not necessarily ensure that its containing directory entry has reached disk; an explicit `fsync()` on a directory file descriptor is needed for that relation.

This supplies a direct interface-level decomposition:

```text
file data + file metadata durability
        ≠
containing-directory entry durability
```

### H/P — ext4 developers still reject the stronger inference that rename itself secures data on disk

In a 1 September 2022 linux-ext4 discussion of another rename/writeback patch, Jan Kara states that ext4 does not guarantee data are securely on disk before rename; userspace is responsible when it needs that guarantee. He describes the existing behavior as starting writeback / shortening a vulnerable window for careless userspace, not as turning rename into an `fsync` substitute.

This later developer statement must not be projected backward as wording from 2009, but it is strong continuity evidence for the semantic boundary.

---

## Retained state

The replace-by-rename pattern involves at least four different targets.

### 1. Replacement-file payload

Bytes written to the temporary/replacement file may be dirty, allocated, written back, or durable depending on the point reached.

### 2. Replacement-file inode metadata

Length, block mapping, timestamps, and other inode-associated state can have a different writeback path from directory naming state.

### 3. Namespace binding

The destination directory retains a relation of the form:

```text
pathname component → inode / file object
```

After replacement, the desired retained relation is that `newpath` names the new file rather than the prior target.

### 4. Journal / writeback control relation

Delayed-allocation state, ordered-mode writeback, and journal commit sequencing determine which changes can reach stable storage in which order. These are constitutive maintenance/control state, not the user payload itself.

---

## Retention mechanism and durability closure

A conservative Linux replacement protocol can be decomposed as:

```text
create/write temporary file
        ↓
fsync(temp-file fd)
        ↓
rename(temp, target)
        ↓
fsync(parent-directory fd)
```

Each arrow closes a different obligation.

### File `fsync`

Establishes the requested file's data/file-metadata storage relation before proceeding. It does not, by itself, certify the later directory entry.

### `rename`

Changes the live namespace atomically with respect to ordinary concurrent pathname observation. That atomicity is not the same predicate as post-crash durability.

### Directory `fsync`

Closes the containing-directory persistence obligation identified explicitly by `fsync(2)`. It is a metadata durability operation: it need not rewrite the entire file payload merely because the name binding must survive.

### `auto_da_alloc`

Narrows one failure window for a common unsynchronized application pattern by forcing delayed allocation / writeback ordering in the documented configuration. It does not replace the explicit file-and-directory synchronization contract.

---

## Engineering reconstruction

### E — atomic visibility ≠ crash durability

`rename()` can prevent concurrent observers from seeing an intermediate missing destination name while still leaving open the question of what survives sudden failure.

### E — payload durability ≠ namespace durability

A replacement file can be durably stored while the desired `target → replacement inode` binding has not yet been made durable. Conversely, a namespace update is not evidence that the payload it names has crossed all lower persistence boundaries.

### E — file `fsync` ≠ directory `fsync`

The Linux interface documentation expressly gives these operations different scopes. A file object's constitutive payload/inode state and the containing namespace edge are separately synchronized targets.

### E — data-before-rename ordering ≠ rename-durable-by-return

`auto_da_alloc` and `data=ordered` can enforce a relative order at journal commit. A relative order between two future persistence events does not imply either event already happened at syscall return.

### E — heuristic protection ≠ explicit durability closure

A filesystem can reduce damage from a common application mistake without converting the mistake into a portable contract. The 2009 intervention is therefore evidence that practical retention semantics can include compatibility heuristics in addition to formal interfaces.

### E — filesystem durability ≠ lower-layer physical persistence by magic

Cases 15, 20, 87 and Synthesis 13 already show that controller caches, Flush/FUA, persistence domains, and power-loss behavior form a lower layer. This case does not infer platter/NAND persistence merely from a high-level filesystem call; it records the Linux interface promise and leaves device-compliance/fault validation separate.

---

## Functional comparisons

### A — Case 16 soft updates

Case 16 shows that crash-admissible stable filesystem state may lag application-visible state and that `fsync` closes a stronger relation. Case 124 adds a Linux namespace-specific counterexample: even after file synchronization, a containing directory entry remains a separately named durability target.

This is a functional comparison, not a claim that ext4 `auto_da_alloc` descends from BSD soft updates.

### A — Case 74 JBD revoke

Case 74 concerns negative recovery evidence suppressing stale redo after block reuse. Case 124 instead concerns when a replacement payload and name binding cross persistence boundaries. Shared journal context does not make revoke semantics and replace-by-rename durability the same mechanism.

### A — Cases 15/20/87 and Synthesis 13

The filesystem can ask for durability while lower layers implement volatile caches and explicit persistence controls. The relation is compositional: a correct namespace protocol cannot strengthen a lower layer beyond the persistence contract actually supplied.

---

## Philosophical interpretation

### I — retained objecthood can depend on a name relation, not only surviving bytes

A file that physically survives but is not durably bound to the expected pathname exposes a useful limit on substrate-centered accounts of persistence. What the application wanted to retain was often not merely a byte sequence but a callable filesystem object under a stable name.

This does not make every directory entry a Stieglerian tertiary retention or Heideggerian `Bestand`. The technical point is narrower: **later availability of a named object can require retention of a relation whose substrate and synchronization path differ from the object's payload.**

---

## Prior-art / novelty boundary

Do not claim:

- that ext4 invented atomic rename;
- that ext4 invented `fsync`;
- that the February/March 2009 patches invented crash-consistent file replacement generally;
- that `auto_da_alloc` is a transaction committing file data and namespace atomically;
- that current Linux man-page wording was the exact historical contract in 2009;
- that rename success proves physical-media persistence;
- that one ext4 data mode establishes semantics for all modes or filesystems.

The safe claim is narrower:

> **The 2009 ext4 delayed-allocation fixes are a dated, primary-source example of a filesystem adding a compatibility heuristic to preserve a data-before-rename relation for common unsynchronized replacement patterns, while current Linux interface documentation still separates rename visibility atomicity, file synchronization, and directory-entry durability.**

---

## Failure / forgetting modes

- crash after ordinary writes but before file durability closure;
- durable temporary-file payload with lost/not-yet-durable destination name binding;
- namespace state durable without the intended payload having satisfied its lower-layer durability contract;
- `noauto_da_alloc` or `data=writeback` invalidating assumptions imported from the default documented path;
- application treating rename success as `fsync` completion;
- application synchronizing the file but omitting the containing directory synchronization needed for the name relation;
- lower-layer cache/persistence failure outside the filesystem's assumed storage contract.

These failures should not be collapsed into one phrase such as `rename was not atomic`.

---

## 2016 PostgreSQL application-level durability deepening

The 2009 ext4 evidence explains why a filesystem added a compatibility heuristic around common unsynchronized replace-by-rename patterns. PostgreSQL's 2016 `durable_rename()` work supplies the complementary application-level witness: a program that actually requires crash durability can explicitly close both payload and namespace obligations rather than treating rename visibility as persistence.

Commit `606e0f9841b820d826f837bf741a3e5e9cc62fa1` introduces a wrapper that fsyncs the source file, optionally syncs an existing target, performs the rename, then fsyncs the file under its new name and its containing directory. The implementation explicitly calls the pre-sync of an existing target conservative rather than strictly necessary, so the case does not universalize one exact syscall sequence.

The follow-up commit `1d4a0ab19a7e45aa8b94d7f720d1d9cefb81ec40` supplies a stronger failure witness. During WAL recycling, new file contents had been `fdatasync`ed while the containing directory was not. A crash could therefore leave **new WAL contents under an old WAL filename**, causing recovery not to replay the intended segment. This fixes a concrete relation:

```text
file-content durability
    !=
name/content-binding durability
    !=
recovery closure
```

For this bounded workload, a filename is not merely presentation metadata: it participates in the recovery traversal that decides which durable bytes count as which WAL segment. The helper also explicitly excludes arbitrary cross-directory rename, so this evidence does not close the separate two-directory durability problem.

This remains separate from lower-layer device compliance. PostgreSQL can issue `fsync`/`fdatasync`; Cases 15, 20, 31, and 87 remain responsible for whether lower persistence layers actually honor the requested contract.

Detailed provenance and stop conditions are recorded in [2016 PostgreSQL `durable_rename` / WAL name-content deepening](../evidence/124-postgresql-2016-durable-rename-wal-name-content-deepening.md).

---

## Related repositories

A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `soft updates fsync journaling crash consistency` did not find a dedicated ext4 replace-by-rename case during this slice. Broad ext2/ext3/ext4/JBD2 history, delayed-allocation design history, and cross-filesystem crash-consistency genealogy belong there if developed. This repository keeps only the retention-specific relation among visibility, ordering, file durability, namespace durability, and lower-layer persistence.

---

## Evidence gaps

- exact revision-by-revision Linux man-pages history for directory `fsync` wording;
- crash/fault-injection traces across representative ext4 kernel versions and mount modes;
- rename across two directories, where both directory durability obligations deserve explicit testing;
- modern fast-commit interaction and exact persistence/barrier composition;
- comparison with XFS, btrfs, ZFS, APFS, NTFS, and database-style atomic replacement;
- named storage-device validation of the lower-layer flush contract;
- complete historical genealogy of application atomic-save idioms.

These are future slices, not blockers for the bounded relation established here.
