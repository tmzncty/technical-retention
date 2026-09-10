# Case 124 deepening — PostgreSQL 2016 `durable_rename`: file contents, namespace durability, and WAL recovery identity

## Scope

This evidence slice deepens Case 124 with one bounded application-level witness: PostgreSQL's March 2016 introduction and deployment of `durable_rename()` / `durable_link_or_rename()`.

The question is deliberately narrow:

> When an application uses rename to install or recycle a file, what additional retention relation must survive a crash beyond the file's bytes themselves?

The primary record is PostgreSQL commits `606e0f9841b820d826f837bf741a3e5e9cc62fa1` and `1d4a0ab19a7e45aa8b94d7f720d1d9cefb81ec40`, both committed 9 March 2016 (mailing-list publication 10 March UTC). Current PostgreSQL source is used only to check that the helper's same-directory durability structure remains recognizable; it is not projected backward as independent 2016 wording.

This slice is not a general PostgreSQL WAL history, a proof of ext4/XFS crash behavior for every version/mount mode, or a portable theorem that one syscall sequence closes every storage stack. Broader filesystem and database durability genealogy belongs in `tmzncty/computing-archaeology` if developed.

---

## Historical vocabulary

The 2016 PostgreSQL sources themselves use:

- `rename(2)`;
- `durable` / `durability`;
- `fsync` / `fdatasync`;
- `containing directory`;
- `checkpoint`;
- `WAL files`;
- `recycled`;
- `WAL replay`;
- `data loss`.

The following are project engineering terms:

- **namespace durability**;
- **name/content binding**;
- **durability closure**;
- **recovery identity**;
- **pre-rename payload closure**.

They summarize relations visible in the source record; they are not attributed to PostgreSQL developers as period terminology.

---

## Historical record

### H/P — PostgreSQL introduced an explicit durable-rename wrapper in March 2016

PostgreSQL commit [`606e0f9841b820d826f837bf741a3e5e9cc62fa1`](https://github.com/postgres/postgres/commit/606e0f9841b820d826f837bf741a3e5e9cc62fa1), `Introduce durable_rename() and durable_link_or_rename()`, states that `rename(2)` is not guaranteed to be durable across crashes and calls out XFS and ext4 with `data=writeback` as important examples.

The commit describes the wrapper sequence for its bounded replace-in-place use case as:

```text
fsync old/source file
    -> fsync existing target if present
    -> rename
    -> fsync file under the new name
    -> fsync containing directory
```

The implementation comment says the routine is intended to make the effect of the rename survive a crash and to leave either the pre-existing or moved file rather than a mixed/truncated replacement.

This is application source history, not an ext4 specification. PostgreSQL is documenting the durability assumptions it needs from the filesystem interface.

### H/P — the existing-target pre-sync was explicitly conservative

The same commit says syncing an already-existing target before replacement is **not strictly necessary**, but makes crash reasoning easier by ensuring that either the source or target file has persisted contents.

Therefore:

```text
implemented conservative fsync step
    !=
proof that every durable-rename protocol requires exactly that step
```

### H/P — the helper deliberately excludes arbitrary cross-directory rename

The 2016 source comment explicitly says `durable_rename()` does not support renaming across arbitrary directories, noting that such paths may reside on different filesystems.

The bounded evidence therefore supports a containing-directory closure for the helper's intended same-directory uses. It does **not** establish that syncing one parent directory is sufficient for every cross-directory rename pattern.

### H/P — the follow-up commit tied missing directory durability to a concrete WAL recovery failure

The immediately following commit [`1d4a0ab19a7e45aa8b94d7f720d1d9cefb81ec40`](https://github.com/postgres/postgres/commit/1d4a0ab19a7e45aa8b94d7f720d1d9cefb81ec40), `Avoid unlikely data-loss scenarios due to rename() without fsync`, replaced ordinary rename/link sequences at multiple PostgreSQL call sites with the new durable wrappers.

Its strongest concrete example occurs at checkpoint/WAL recycling. The commit explains that recycled old WAL files had their new **contents** `fdatasync`ed, but their containing directory was not fsynced. After an OS/hardware crash, a file could therefore retain its **old WAL filename while containing new WAL content**. Recovery would then fail to replay the content under the name by which it should have been discovered.

This is stronger than a generic statement that `rename` may be lost. It shows a real application invariant whose two components can diverge:

```text
persisted file bytes
    + stale persisted filename
    -> recovery-visible identity mismatch
```

### H/P — the 2016 change was intentionally backpatched

The commit messages state `Backpatch: All supported branches`; PostgreSQL's commit mail archive records corresponding branch-specific hashes. This shows the developers treated the durability issue as applicable to supported released branches, not merely as a feature for one future release.

That backpatch policy does not rewrite earlier historical behavior: deployments before the fix may still have used ordinary rename sequences.

---

## Engineering reconstruction

### E — file-content durability != name/content-binding durability

The WAL example directly demonstrates that the bytes of a recycled file can have crossed a durability boundary while the namespace binding that gives those bytes their recovery meaning has not.

For this bounded application, the retained object is therefore not adequately modeled as `byte string survived`. Recovery depends on a relation:

```text
WAL segment identity / filename
        -> intended segment contents
        -> recovery traversal/replay
```

A stale first edge can make durable bytes operationally absent from the recovery sequence.

### E — pre-rename payload closure and post-rename namespace closure answer different failure windows

Syncing the source before rename protects against a crash after the in-memory rename has taken effect but before later flushes complete: the newly installed name should not expose an embodiment whose contents were never made durable.

Syncing the post-rename file and containing directory answers a later question: whether the new file state and directory entry survive the crash as the intended replacement relation.

Therefore:

> **pre-rename payload durability != post-rename namespace durability.**

### E — `fdatasync` of WAL contents != checkpoint/recovery closure

The follow-up commit's failure scenario is especially useful because the new WAL contents had already been `fdatasync`ed. A checkpoint-related durability protocol can still be incomplete if the naming relation that recovery uses is not also durable.

So:

> **durable component payload != durable recovery graph.**

### E — syscall success and filesystem ordering heuristics remain different evidence classes

Case 124's ext4 `auto_da_alloc` evidence shows a filesystem heuristic that narrows a common replace-by-rename crash window. PostgreSQL's 2016 wrapper is an application-level explicit durability protocol. Neither should be silently substituted for the other:

```text
filesystem compatibility heuristic
    != application-issued durability closure
```

### E — lower-layer compliance remains an external premise

PostgreSQL can issue `fsync`/`fdatasync` and structure ordering around their interface contract. This source set does not independently prove that every controller, cache, drive, virtualized stack, or power-loss path honors those requests correctly.

Cases 15, 20, 31, and 87 remain the lower persistence-domain / device-contract comparisons.

---

## Functional comparisons and limits

### A — Case 16 soft updates

Both cases show that a filesystem-visible current relation can outrun the crash-surviving relation and that explicit synchronization closes a stronger target. PostgreSQL adds an application witness in which the desired target is specifically a **name/content pairing used by recovery**.

No genealogy from BSD soft updates to PostgreSQL is asserted.

### A — Case 25 mutable EC currentness

Swift's fragment timestamp / `.durable` relation and PostgreSQL's WAL filename/content relation both demonstrate that materially present bytes need enough control/currentness evidence to be admitted as the intended version. Their protocols and failure domains are otherwise different.

### A — Cases 15/20/31/87

These cases show why the application-level protocol still composes with lower persistence semantics. A successful `fsync` request is evidence at the filesystem interface boundary, not transistor-level proof of NAND/platter persistence.

---

## Philosophical interpretation

### I — technical persistence can depend on a durable identity edge

The narrow interpretive result is that later recovery may require a durable relation between **what survived** and **under which name/position it is to be retrieved**. The WAL example makes this unusually concrete: new bytes under an old segment name can survive materially while failing the intended recovery identity.

This does not imply that every filename is intrinsically part of every object's identity, nor that namespace metadata should be redescribed as human memory. It is a system-specific continuation rule.

---

## Claim ledger

| Claim | Label | Support | Limit |
| --- | --- | --- | --- |
| PostgreSQL introduced `durable_rename()` in March 2016 because ordinary rename was not assumed crash-durable | `H/P` | commit `606e0f9841...` | application implementation record, not a universal filesystem theorem |
| bounded wrapper syncs source, optionally existing target, performs rename, then syncs new file and containing directory | `H/P` | commit diff/comment | same-directory helper; not arbitrary cross-directory closure |
| existing-target pre-sync was described as conservative rather than strictly necessary | `H/P` | commit comment | does not identify the unique minimal portable sequence |
| missing directory fsync could leave an old WAL name attached to new fdatasynced content | `H/P` | commit `1d4a0ab19...` | concrete PostgreSQL failure scenario, not every rename workload |
| durable bytes can still be unusable for intended recovery when naming/currentness metadata is stale | `E` | WAL scenario | project reconstruction |
| application durability protocol != ext4 `auto_da_alloc` heuristic | `E/A` | Case 124 + PostgreSQL evidence | no genealogy claimed |
| helper semantics != lower-layer device compliance | `E/A` | interface layering | requires separate device/fault evidence |

---

## Sources

1. PostgreSQL commit `606e0f9841b820d826f837bf741a3e5e9cc62fa1`, **“Introduce durable_rename() and durable_link_or_rename().”**, 9 March 2016.
   - <https://github.com/postgres/postgres/commit/606e0f9841b820d826f837bf741a3e5e9cc62fa1>
   - official commit-mail record: <https://www.postgresql.org/message-id/E1adrE0-0001Or-CA%40gemulon.postgresql.org>

2. PostgreSQL commit `1d4a0ab19a7e45aa8b94d7f720d1d9cefb81ec40`, **“Avoid unlikely data-loss scenarios due to rename() without fsync.”**, 9 March 2016.
   - <https://github.com/postgres/postgres/commit/1d4a0ab19a7e45aa8b94d7f720d1d9cefb81ec40>
   - official commit-mail record: <https://www.postgresql.org/message-id/E1adrE1-0001PP-Vx%40gemulon.postgresql.org>

3. PostgreSQL current source, `src/backend/storage/file/fd.c`, `durable_rename()`; later implementation witness only.
   - <https://github.com/postgres/postgres/blob/master/src/backend/storage/file/fd.c>

## Open work kept outside this slice

- crash/fault-injection reproduction across named ext4/XFS versions and mount modes;
- cross-directory rename and explicit source/destination-directory durability obligations;
- complete PostgreSQL rename/fsync genealogy before 2016 and later changes to the helper;
- comparison with SQLite, RocksDB, LMDB, XFS, btrfs, ZFS, APFS, and NTFS durable replacement protocols;
- lower-layer controller/device compliance with flush/fsync persistence contracts;
- general WAL/checkpoint history.
