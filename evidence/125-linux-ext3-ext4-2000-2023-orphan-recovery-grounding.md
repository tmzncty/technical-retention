# Evidence 125 — Linux ext3/ext4 Orphan Recovery Grounding, 2000–2023

## Purpose

Ground the narrow Case 125 claim that **filesystem namespace retirement can precede allocation reclamation, and ext3/ext4 retain explicit crash-recovery metadata identifying inodes whose delete/truncate cleanup still needs to be completed**.

The evidence is deliberately bounded. A July 2000 ext3 release announcement establishes a public implementation floor; Linux v2.6.12 source establishes operational recovery ordering; later ext4 source/documentation shows a representation change rather than a new recovery concept; a 2023 power-cut fix supplies a concrete failure witness for inconsistent recovery metadata.

---

## Source inventory

| ID | Date | Type | Source | Use |
| --- | --- | --- | --- | --- |
| P1 | 2000-07-05 | primary period developer/release announcement | Stephen C. Tweedie, [`ext3-0.0.2e released`](https://lkml.rescloud.iu.edu/0007.0/0582.html) | public floor for ext3 `orphan-list` code; credits Andreas Dilger implementation; unlinked-open crash-cleanup purpose |
| P2 | 2000-07-06 | primary period developer/release announcement | Stephen C. Tweedie, [`PATCH: ext3-0.0.2f released`](https://lkml.rescloud.iu.edu/0007.0/0718.html) and follow-up changelog | states on-disk list of inodes needing recovery cleanup; covers unlinked-open deletion and truncate completion across transaction boundaries |
| P3 | Linux v2.6.12 source snapshot | primary source code | [`fs/ext3/super.c`](https://github.com/torvalds/linux/blob/v2.6.12/fs/ext3/super.c) | `ext3_orphan_cleanup()` traversal, link-count-qualified truncate/delete behavior, restartable cleanup |
| P4 | Linux v2.6.12 source snapshot | primary source code | [`fs/ext3/inode.c`](https://github.com/torvalds/linux/blob/v2.6.12/fs/ext3/inode.c) | `ext3_truncate()` restartability; journal replay explicitly precedes orphan-list truncate restart |
| P5 | 2021-08-16 author date / 2021-08-31 UTC committer date | primary source commit | Linux [`02f310fcf47f...`](https://github.com/torvalds/linux/commit/02f310fcf47fa9311d6ba2946a8d19e7d7d11f37), Jan Kara, `ext4: Speedup ext4 orphan inode handling` | linked-list scalability limit; orphan-file representation; compatibility and `RO_COMPAT_ORPHAN_PRESENT` state |
| P6 | current, inspected 2026-09 | official kernel documentation | Linux [`Documentation/filesystems/ext4/orphan.rst`](https://github.com/torvalds/linux/blob/master/Documentation/filesystems/ext4/orphan.rst) / [rendered kernel docs](https://www.kernel.org/doc/html/latest/filesystems/ext4/orphan.html) | current explanation of unlinked-open leakage, multi-transaction truncate tracking, list/orphan-file representations, mount/unmount feature semantics |
| P7 | 2023-06-28 author date / 2023-08-27 upstream committer date | primary source commit + power-cut test record | Linux [`1524773425ae...`](https://github.com/torvalds/linux/commit/1524773425ae8113b0b782886366e68656b34e53), Zhihao Cheng, `ext4: fix unttached inode after power cut with orphan file feature enabled` | demonstrates orphan-file membership alone can fail if inode state used by cleanup was not durably updated |

P1/P2 are mailing-list archive mirrors of period developer messages, so they are treated as primary historical content but not as canonical Git commit objects. P3/P4 are a later source snapshot used to expose implementation semantics already descended from the bounded ext3 regime; they are not proof that every line was present in July 2000. P5–P7 are explicitly later ext4 evolution/validation and are not projected backward.

---

## Direct source checks

### P1 — 5 July 2000 public orphan-list floor

Tweedie's `ext3-0.0.2e released` message says the release includes `orphan-list` code based on an implementation by Andreas Dilger. The purpose is to clean inodes that have been unlinked but are still held open by a process because such inodes need to be deleted properly after a crash.

**Supported:** ext3 publicly shipped/announced an orphan-list implementation by this date and explicitly linked it to post-crash cleanup of unlinked-open inodes.

**Not supported:** invention priority, first-ever filesystem orphan tracking, or sole authorship by Tweedie.

### P2 — 6 July 2000 expands the target class to interrupted truncates

The 0.0.2f release message says orphan handling was also extended to `rmdir` cases, while its change list for 0.0.2e describes Andreas Dilger's orphan-list implementation as an **on-disk list of inodes needing cleaned up on recovery**. The listed uses are deletion after reboot of unlinked-but-still-open files and completion after recovery of truncates that were in progress but split across a transaction boundary.

**Supported:** on-disk target identity can retain unfinished cleanup across crash for both final deletion and truncate continuation.

**Not supported:** one universal orphan semantic for all later ext3/ext4 states.

### P3 — v2.6.12 `ext3_orphan_cleanup()` walks and interprets retained targets

The source comment says the function walks a singly linked list starting from the superblock for inodes deleted from directories but held open at crash time. The implementation repeatedly obtains `s_last_orphan`, loads the inode, and then:

- calls `ext3_truncate(inode)` when `i_nlink` is nonzero;
- otherwise follows the unreferenced-inode deletion path through `iput()`.

The comment also says each recovered inode is linked into the in-memory orphan list and handled through ordinary journaled deletion behavior so the chain remains consistent even if another crash occurs during recovery.

**Supported:** orphan membership selects a recovery target, but surviving inode state helps select the recovery operation; cleanup itself remains restartable/journaled.

### P4 — v2.6.12 `ext3_truncate()` separates replay from cleanup restart

The source says the truncate algorithm must keep filesystem+journal state restartable at every committed transaction boundary. It explicitly states that journal replay occurs **before** restart of truncate against the orphan inode list. The committed inode contains the desired size; if a crash leaves blocks beyond the truncation point, `ext3_orphan_cleanup()` calls truncate again and releases them.

**Supported:** `journal replay ≠ orphan restart ≠ completed reclamation` as separate phases in one recovery chain.

**Not supported:** a general rule that every filesystem must order recovery this way.

### P5/P6 — ext4 changes representation while preserving the recovery function

The 2021 commit describes the old on-disk orphan linked list as a scalability bottleneck under heavy truncate/unlink load. The new design stores inode numbers in a special `orphan file`; when it is full, code can fall back to the traditional list. The commit adds `s_orphan_file_inum`, `EXT4_FEATURE_COMPAT_ORPHAN_FILE`, and `EXT4_FEATURE_RO_COMPAT_ORPHAN_PRESENT`.

Current kernel documentation explains the same two representations and states that writable mount sets `RO_COMPAT_ORPHAN_PRESENT` to indicate possible valid orphan entries; mount with the feature reads/processes the orphan file; clean unmount clears the feature to avoid unnecessary scan and maintain compatibility with older kernels.

**Supported:** same bounded cleanup function can survive a change in metadata layout; scan-admission state is distinct from the cleanup-target population.

**Not supported:** 2021 invention of orphan recovery or exact identity between ext3's July-2000 implementation and all modern ext4 internals.

### P7 — 2023 power-cut failure validates a consistency dependency

The upstream commit records an xfstests `generic/475` power-cut case. In several error paths, the in-memory link count was reduced and the inode was added to the orphan file, but the inode was not marked dirty first. The journal could commit the orphan entry, then power could fail. At recovery the inode table still contained `nlink=1`, so `ext4_orphan_cleanup()` / `ext4_process_orphan()` did not delete it. The result was an allocated inode with no directory entries, reported by `e2fsck` as unattached. The fix marks the inode dirty before orphan insertion in the affected paths.

**Supported:** retained cleanup-target identity can be physically present yet semantically insufficient when target-state evidence is stale; recovery correctness depends on a relation among several metadata objects.

**Not supported:** all orphan-file failures, all ext4 power-cut behavior, or a statement that the orphan file itself was lost/corrupt.

---

## Claim ledger

| Claim | Type | Evidence | Status / limit |
| --- | --- | --- | --- |
| ext3 publicly announced orphan-list code on 5 Jul 2000 | H/P | P1 | grounded public implementation floor |
| the announcement credits an Andreas Dilger implementation basis | H/P | P1/P2 | grounded; blocks sole-inventor wording |
| orphan tracking covered unlinked-open crash cleanup | H/P | P1/P2/P3 | grounded across release message and later source witness |
| the July-2000 description included an on-disk list | H/P | P2 | grounded period developer statement |
| orphan tracking also retained interrupted multi-transaction truncate work | H/P | P2/P4/P6 | grounded; later source/docs supply operational continuity |
| orphan membership alone determines every recovery action | X | P3/P7 | rejected; inode state participates |
| journal replay and orphan cleanup are the same phase | X | P4 | explicitly rejected by source |
| namespace detachment implies immediate block/inode reclamation | E/X | P1/P2/P6 | rejected |
| retained orphan metadata is user payload | X | P1–P6 | rejected |
| current orphan-file representation is the original 2000 data structure | X | P2/P5/P6 | rejected |
| `RO_COMPAT_ORPHAN_PRESENT` and the orphan entries are one state object | E/X | P5/P6 | rejected; summary/scan state versus population |
| clean-unmount feature clearing is equivalent to erasing file payload | X | P6 | rejected |
| 2021 orphan-file commit invented orphan recovery | X | P1/P2/P5 | rejected by two-decade-earlier floor |
| retained target identity is sufficient even when target inode fields are stale | X | P7 | rejected by power-cut bug |
| the 2023 bug proves payload loss | X | P7 | rejected; documented result is unattached allocated inode/reclamation inconsistency |
| orphan cleanup proves lower-media sanitization | X | scope + Case 44 | rejected |
| Case 16 soft-updates reclamation and ext orphan tracking are historically identical | A/X | Case 16 + P1–P6 | functional analogy only |

---

## Engineering decomposition

The bounded crash-recovery state graph is:

```text
namespace/link relation
        +
inode size / block tree / allocation ownership
        +
orphan target enumeration
        +
journal replay state
        +
scan-admission / representation metadata
        ↓
post-crash interpretation and cleanup
        ↓
reclamation closure
```

The key transitions are not one Boolean `deleted` state:

```text
unlink visible             → name relation may end
open reference remains     → inode lifetime can continue
orphan entry durable       → cleanup target survives crash
journal replay complete    → committed metadata becomes recovery base
orphan processing complete → delete/truncate obligation is discharged
allocation update complete → blocks/inode become reusable
sanitize/erase complete    → separate lower-layer forgetting relation, if requested
```

This is an **engineering reconstruction** from the documented implementation. Linux does not name one universal `reclamation closure` object.

---

## Prior-art / anti-anachronism controls

1. Unix unlink-open semantics predate the bounded ext3 evidence. The release messages themselves describe that pre-existing semantic condition rather than claiming to invent it.
2. P1/P2 credit Andreas Dilger's implementation, so the July 2000 date is a public ext3 implementation floor, not an invention date and not a sole-Tweedie origin claim.
3. Case 16 already grounds a 1999–2000 BSD FFS soft-updates regime in which crash-safe operation can leave reclamation work for later repair. That is prior functional evidence that `crash consistency ≠ all resources already reclaimed`; it is not proof of direct lineage into ext3's orphan list.
4. The 2021 orphan-file commit explicitly begins from an existing linked-list mechanism and changes scalability/representation. It cannot safely serve as orphan-recovery origin evidence.
5. The 2023 fix is validation/evolution evidence. It must not be projected backward as a defect or semantic detail known in the 2000 release.

---

## Cross-case boundary

- **Case 16 — BSD FFS soft updates:** can preserve a structurally admissible disk image while deferred resource/accounting repair remains. Case 125 instead retains explicit inode identities for post-crash delete/truncate continuation. Similar recovery/reclamation function, different mechanism and no asserted genealogy.
- **Case 74 — Linux JBD revoke:** retained negative replay evidence suppresses a stale journal image after block reuse. Case 125 retains positive cleanup-target evidence that causes/resumes work after replay. `revoke record ≠ orphan entry`.
- **Case 124 — ext4 rename/`fsync`:** establishes namespace visibility/durability boundaries. Case 125 establishes that even ended pathname reachability does not itself prove allocation reclamation.
- **Case 73 — GFS lazy GC:** distributed logical deletion can precede later replica cleanup. This is a functional analogy to deferred reclamation, not a shared metadata representation or historical lineage.
- **Case 44 — NVMe Deallocate/Sanitize:** reclamation/reuse inside a filesystem does not establish physical-media sanitization or crypto erase.

---

## Related-repository check

Fresh searches of `tmzncty/computing-archaeology` for `orphan`, `ext3 orphan`, and `ext4 orphan` returned no dedicated case to reuse. Broad Unix inode lifetime, ext2/ext3/ext4 evolution, JBD/JBD2, e2fsck, and filesystem crash-consistency genealogy remain better suited to the companion repository if developed. Evidence 125 stays with the retention-specific recovery/reclamation relation.

---

## Remaining evidence debt

- locate and inspect the pre-0.0.2e Andreas Dilger patch or archived tarball source;
- pin the earliest exact field/layout behavior of the July-2000 implementation rather than relying on later v2.6.12 source for operational detail;
- trace ext3→ext4 linked-list continuity release by release;
- inspect e2fsprogs handling of corrupt/partial orphan structures;
- reproduce xfstests power-cut behavior for the 2023 bug and fix;
- fault-inject lost/stale orphan-list head, individual entries, orphan-file blocks, `RO_COMPAT_ORPHAN_PRESENT`, and inode state independently;
- compare filesystem families and database free-space recovery without assuming one universal orphan mechanism;
- validate lower-layer discard/erase/sanitize separately where physical forgetting matters.
