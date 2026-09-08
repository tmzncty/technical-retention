# Linux ext3/ext4 Orphan Tracking: Crash-Persistent Cleanup Obligations and Deferred Reclamation

## Status

**`grounded`** — bounded to the ext3 orphan-list implementation publicly described in July 2000, a Linux v2.6.12 source witness for mount-time orphan/truncate recovery, and the later ext4 orphan-file representation and 2023 power-cut correction.

Grounding record: [`../evidence/125-linux-ext3-ext4-2000-2023-orphan-recovery-grounding.md`](../evidence/125-linux-ext3-ext4-2000-2023-orphan-recovery-grounding.md).

## Scope

This case addresses one unchecked Phase-4 forgetting/reclamation problem:

> **What retained state lets a filesystem remember that an object which is no longer normally named still has unfinished inode/block cleanup after a crash?**

The bounded relation is:

```text
unlink or multi-transaction truncate begins
        ↓
ordinary namespace/current-size state advances
        ↓
an inode can still carry blocks or require final deletion/truncation
        ↓
filesystem retains an on-disk orphan relation
        ↓
crash destroys volatile continuation state
        ↓
journal recovery re-establishes a crash-admissible filesystem
        ↓
orphan processing resumes delete/truncate work
        ↓
allocation resources become reclaimable
```

This is not a general history of Unix unlink semantics, ext2/ext3/ext4, journaling, `fsck`, orphan files, crash consistency, delayed allocation, or secure deletion. Case 16 already grounds BSD FFS soft-updates crash admissibility and post-crash reclamation; Case 74 grounds JBD revoke as stale-redo suppression; Case 124 grounds ext4 rename/`fsync` durability closure. Case 125 isolates a different retained object:

> **an explicit crash-surviving cleanup obligation whose target can already be detached from ordinary namespace reachability.**

`cleanup obligation`, `cleanup-target relation`, `reclamation closure`, and `scan-admission summary` below are project engineering terms. They are not attributed to ext3/ext4 developers as period vocabulary.

---

## Historical vocabulary

The inspected sources directly use:

- `orphan-list` / `orphan list`;
- `orphan inode`;
- `unlinked but ... held open`;
- `recovery`;
- `truncate` / `truncates`;
- `delete` / `deleting unreferenced inode`;
- `s_last_orphan`;
- `i_dtime`;
- `orphan file`;
- `COMPAT_ORPHAN_FILE`;
- `RO_COMPAT_ORPHAN_PRESENT`;
- `power cut`;
- `unattached inode`.

The project vocabulary is deliberately separated from those terms.

---

## Historical record

### H/P — July 2000 gives a public implementation floor, not an invention date

Stephen C. Tweedie's 5 July 2000 `ext3-0.0.2e released` announcement says that release included `orphan-list` code based on an implementation by Andreas Dilger. The stated purpose was to clean up inodes that had been unlinked but remained open by a process and therefore needed proper deletion after a crash.

The 6 July 2000 `ext3-0.0.2f` announcement is even more explicit. Its change list describes Andreas Dilger's implementation as an **on-disk list of inodes needing cleanup on recovery**, including both:

- deletion after reboot of unlinked-but-still-open files; and
- completion after recovery of truncates that had been split across a transaction boundary.

This establishes a dated public implementation/release floor. It does **not** establish that ext3 invented Unix unlink-open semantics, orphan tracking, deferred reclamation, or crash cleanup; the announcement itself attributes the implementation basis to Dilger rather than supporting a single-inventor claim.

### H/P — Linux v2.6.12 source makes the retained cleanup relation operationally explicit

In `fs/ext3/super.c` from Linux v2.6.12, `ext3_orphan_cleanup()` is documented as walking a singly linked list beginning in the superblock. The comment says these are inodes deleted from all directories but held open by a process at crash time. Recovery traverses the list and attempts to delete them.

The function does not treat every orphan identically. It reads the surviving inode and branches on link count:

- if `inode->i_nlink` is nonzero, it calls `ext3_truncate(inode)` and counts a recovered truncate;
- otherwise it performs the unreferenced-inode deletion path through `iput()`.

This is evidence that **orphan membership alone is a target-selection relation, not the whole recovery semantics**. The surviving inode state still helps decide what cleanup operation is appropriate.

### H/P — journal replay and orphan cleanup are ordered but distinct recovery phases

The v2.6.12 `ext3_truncate()` source says its guiding rule is that the file tree plus journal must remain restartable at transaction boundaries. It explicitly states that at recovery time **journal replay occurs before restart of truncate against the orphan inode list**. The committed inode already carries the desired new `i_size`; if a crash left blocks to the right of that truncation point, later `ext3_orphan_cleanup()` calls `ext3_truncate()` again to release them.

Therefore:

```text
journal replay
        ≠
orphan cleanup
        ≠
resource reclamation already complete
```

The phases compose, but one cannot be substituted for another.

### H/P — current ext4 documentation preserves the same recovery function while changing its representation

Current Linux ext4 documentation says that an inode can be removed from the directory hierarchy while remaining alive because it is open; after a crash the filesystem must clean it up or the inode and referenced blocks leak. It also says truncate/extend may require multiple journal transactions, so an inode is tracked as orphan to allow post-crash removal of excess blocks.

The documentation distinguishes two on-disk representations:

1. the traditional global singly linked list, with `s_last_orphan` in the superblock and `i_dtime` overloaded to point to the previous/next orphan in the chain; and
2. the newer `COMPAT_ORPHAN_FILE` representation, where a special file stores inode numbers in orphan-file blocks.

The retention function therefore survives a layout change:

```text
cleanup obligation function
        ≠
one immutable metadata representation
```

### H/P — `RO_COMPAT_ORPHAN_PRESENT` is a retained scan-admission summary, not the orphan population itself

The current ext4 documentation says a writable mount sets `RO_COMPAT_ORPHAN_PRESENT` to indicate that valid orphan entries may exist. If the feature is seen at mount, ext4 reads the orphan file and processes its entries. A clean unmount removes the feature so later mounts need not scan the orphan file and older kernels remain compatible.

This supplies another explicit state split:

```text
orphan-file contents
        ≠
feature bit saying a scan may be required
        ≠
cleanup work already completed
```

The feature bit is a summary/control relation for recovery admission. It is not a duplicate list of cleanup targets.

### H/P — the 2021 orphan-file change was a scaling/representation change, not a new orphan-recovery invention

Linux commit [`02f310fcf47fa9311d6ba2946a8d19e7d7d11f37`](https://github.com/torvalds/linux/commit/02f310fcf47fa9311d6ba2946a8d19e7d7d11f37), authored 16 August 2021 and committed upstream 31 August 2021 (UTC), calls the existing on-disk linked list a scalability bottleneck for heavy truncate/unlink workloads. It introduces the special orphan file, falls back to the old list when the file has no free slot, and adds the compatibility/RO-compat feature-state relation described above.

This is later evolution of how cleanup obligations are retained. It must not be projected backward into ext3-0.0.2e or treated as the origin of the orphan mechanism.

### H/P — a 2023 power-cut bug shows retained orphan membership can be insufficient if target inode state is inconsistent

Linux commit [`1524773425ae8113b0b782886366e68656b34e53`](https://github.com/torvalds/linux/commit/1524773425ae8113b0b782886366e68656b34e53), authored 28 June 2023 and committed upstream 27 August 2023, fixes a power-cut failure with the orphan-file feature. The commit records an xfstests `generic/475` scenario in which an inode was added to orphan-file tracking after its in-memory link count dropped, but the changed inode was not first marked dirty. After the journal commit and power cut, recovery loaded an on-disk inode whose link count was still one; orphan cleanup therefore did not delete it, leaving an allocated unattached inode reported by `e2fsck`.

This is a particularly strong retention counterexample:

```text
cleanup-target membership retained
        +
target state stale/inconsistent
        =
cleanup obligation not correctly discharged
```

The fix adds `ext4_mark_inode_dirty()` before orphan insertion in the affected error paths.

---

## Retained state

At least five different state classes participate in the bounded case.

### 1. File/inode payload and block ownership

The inode can still reference blocks even after its ordinary directory name has disappeared or while a truncate is only partially completed.

### 2. Namespace/reference state

Directory reachability and link count describe whether ordinary names still retain the inode. This relation can advance before physical resources are finally released.

### 3. Orphan cleanup-target state

The traditional list or orphan file identifies inodes for which recovery-time work remains outstanding. This is not application payload; it is retained maintenance/recovery metadata.

### 4. Journal/recovery state

Committed journal records restore a crash-admissible metadata state before orphan cleanup is restarted. Case 74's revoke evidence belongs to this replay layer, not to orphan-target enumeration.

### 5. Allocation/reclamation state

Blocks and inode allocation cannot be treated as safely reusable merely because a pathname disappeared. Reclamation closes only after the relevant delete/truncate work updates ownership/allocation relations.

---

## Retention mechanism

### Unlinked-open inode

Unix permits a file to lose its directory entry while an open reference keeps the inode alive. The filesystem cannot reclaim the inode immediately merely because pathname reachability ended.

When the last in-memory reference would normally trigger final deletion, a crash can remove that volatile continuation path. The orphan relation carries enough target identity into the next mount to restart the work.

### Multi-transaction truncate

A large truncate can cross journal transaction boundaries. The desired smaller size can already be committed while some old blocks remain linked/reachable from the inode tree. The orphan relation keeps the inode eligible for recovery-time completion.

### Mount-time recovery

The bounded v2.6.12 sequence is:

```text
journal replay
        ↓
walk s_last_orphan chain
        ↓
read target inode
        ↓
link-count / inode-state qualification
        ↓
resume truncate OR delete unreferenced inode
        ↓
release blocks/inode through ordinary journaled paths
```

The cleanup work itself is journaled so a second crash during recovery can remain restartable.

### Modern orphan file

The 2021 redesign changes target enumeration from a single linked list to indexed inode-number entries in a special file, plus a `RO_COMPAT_ORPHAN_PRESENT` mount-time scan indicator. This changes contention and representation without changing the bounded recovery question: **which inodes still carry unfinished cleanup work?**

---

## Engineering reconstruction

### E — namespace detachment ≠ storage reclamation

A directory entry can disappear while the inode and blocks remain intentionally allocated because the file is still open or because cleanup spans transactions.

Logical disappearance from normal path lookup is therefore weaker than completed resource retirement.

### E — cleanup obligation ≠ cleanup completion

An orphan-list/orphan-file entry says work remains. It is evidence for future maintenance, not proof that deletion/truncation has already finished.

### E — retained cleanup metadata ≠ retained user payload

The orphan relation identifies what needs post-crash work. It need not reproduce the file data it helps retire.

### E — journal replay ≠ orphan restart

The v2.6.12 source explicitly orders journal replay before orphan-truncate restart. Replaying committed metadata closes one recovery relation; walking the orphan population discharges another.

### E — target identity ≠ sufficient target semantics

The 2023 bug shows that retaining the inode number in the orphan file can still be insufficient if the on-disk inode fields used to interpret that target are stale. A recovery index and the state it indexes form a consistency relation.

### E — scan-admission metadata ≠ scan population

`RO_COMPAT_ORPHAN_PRESENT` summarizes whether the orphan file may need processing; the actual inode-number entries identify targets. Losing or misinterpreting either kind of state can affect recovery differently.

### E — representation evolution ≠ functional novelty

The traditional linked list and the 2021 orphan file implement different data structures for the same bounded future-cleanup function. The newer representation's performance motivation does not make orphan cleanup a 2021 invention.

### E — physical survival ≠ safely reusable capacity

Blocks can physically survive, and even remain reachable from an inode tree, while their final ownership/reclamation status is unresolved. Capacity becomes reusable only after filesystem metadata authorizes reuse.

---

## Failure and forgetting modes

- crash after unlink while the inode is still held open;
- crash during a truncate split across transactions;
- loss/corruption of the orphan target relation;
- stale target inode state that makes retained orphan membership semantically misleading;
- damaged/inadmissible journal state before orphan processing;
- second crash during cleanup;
- orphan-file/list corruption that prevents complete target enumeration;
- cleanup completing logically while lower-layer media sanitization remains entirely unaddressed.

These must not be collapsed into one phrase such as `file deletion failed`.

---

## Cross-case functional comparisons

### A — Case 16 BSD FFS soft updates

Case 16 already shows that a filesystem can resume from a structurally admissible stable image while some resource/accounting cleanup remains for later `fsck`-style reclamation. Case 125 supplies a different mechanism: ext3/ext4 deliberately retain a named set of inodes whose delete/truncate work must be resumed.

The functional similarity is `safe crash recovery can preserve unfinished reclamation work`. The mechanism is not the same, and no BSD FFS → ext3 genealogy is asserted.

### A — Case 74 Linux JBD revoke

A revoke record says an older committed journal image must **not** be replayed after block reuse. An orphan entry says a particular inode **must** receive recovery-time cleanup. Both are recovery-control metadata, but their polarity and authority differ:

```text
revoke: suppress stale recovery action
orphan: require/resume cleanup action
```

Shared ext/JBD context does not make them one mechanism.

### A — Case 124 ext4 rename / `fsync`

Case 124 separates pathname visibility and namespace durability from payload durability. Case 125 adds a later lifecycle boundary: even a successfully removed name does not imply that the inode and blocks have already been reclaimed.

Thus:

```text
namespace state
    ≠ durability closure
    ≠ allocation reclamation
```

### A — Case 73 GFS lazy garbage collection

GFS also lets logical deletion/reference retirement precede later physical replica cleanup. That is a useful functional analogy at the level of deferred reclamation. GFS's distributed hidden-name grace, master/chunkserver inventory, and HeartBeat-driven cleanup are not ext orphan-list mechanisms and no genealogy is implied.

---

## Philosophical interpretation

### I — forgetting can leave a retained obligation to finish forgetting

A pathname can cease to name an object while the system deliberately preserves metadata saying that further cleanup remains necessary. In this bounded sense, technical forgetting is not always one state transition from `present` to `absent`; it can have an intermediate maintenance phase in which **the object is no longer ordinarily current/named, yet the system must remember enough about it to complete reclamation safely**.

This is a philosophical interpretation built on the mechanism, not historical ext3/ext4 vocabulary and not a claim that every deletion process has the same temporal structure.

---

## Prior-art / novelty boundary

Do not claim:

- ext3 invented Unix unlink-open semantics;
- Stephen Tweedie alone invented the orphan list — the July 2000 release record explicitly credits an Andreas Dilger implementation;
- July 2000 is the first-ever orphan/recovery mechanism in filesystem history;
- the 2021 ext4 orphan file invented orphan recovery;
- an orphan-list entry is a complete recovery log or complete filesystem history;
- successful orphan cleanup proves secure media erasure;
- Case 16 soft-updates reclamation is historically identical to ext3 orphan cleanup;
- a physically present inode/block is necessarily current, named, or safely reusable.

The safe claim is narrower:

> **By July 2000 ext3 publicly used an on-disk orphan list to retain the identity of inodes needing deletion or truncate completion after crash; later source makes journal replay and orphan restart separate phases, modern ext4 changes the representation to a scalable orphan file, and a 2023 power-cut fix demonstrates that retained cleanup-target identity must remain consistent with the target inode state for reclamation to succeed.**

---

## Related repositories

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `orphan`, `ext3 orphan`, and `ext4 orphan` found no dedicated case to reuse during this slice. A broad Unix unlink/inode, ext2→ext3→ext4, JBD/JBD2, `fsck`, or orphan-file genealogy belongs there if developed. This case keeps only the retention-specific split among namespace retirement, retained cleanup obligation, replay, target-state qualification, and resource reclamation.

---

## Evidence gaps

- recover the exact pre-0.0.2e Andreas Dilger patch/source history rather than using the release announcement as the first bounded public floor;
- inspect the ext3-0.0.2e/0.0.2f tarball itself to pin the earliest on-disk field layout and transaction ordering;
- trace the old linked-list implementation across ext3/ext4 releases before the 2021 orphan-file change;
- inspect the exact e2fsprogs recovery/checking behavior for damaged orphan metadata;
- run power-cut/fault-injection tests across traditional-list and orphan-file modes;
- test corrupt/missing `s_last_orphan`, orphan-file entries, and `RO_COMPAT_ORPHAN_PRESENT` independently;
- compare XFS, UFS/FFS, btrfs, ZFS, and database free-space reclamation without assuming one common mechanism;
- separate ordinary reclamation from lower-layer discard/sanitize/crypto-erase in named deployments.

These are future slices, not blockers for the bounded relation established here.
