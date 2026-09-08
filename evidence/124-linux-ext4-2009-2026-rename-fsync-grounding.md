# Evidence 124 — Linux ext4 Replace-by-Rename / `fsync` Grounding, 2009–2026

## Purpose

Ground the narrow Case 124 claim that **rename visibility atomicity, ext4's delayed-allocation compatibility heuristic, file durability, and containing-directory durability are separate relations**.

This record deliberately mixes a 2009 historical implementation slice with current Linux interface documentation only where the dates are kept explicit. Current documentation is continuity/contract evidence; it is not projected backward as verbatim 2009 semantics.

---

## Source inventory

| ID | Date | Type | Source | Use |
| --- | --- | --- | --- | --- |
| P1 | 2009-02-24 | primary source code/commit | Linux commit [`8750c6d5...`](https://github.com/torvalds/linux/commit/8750c6d5fcbd3342b3d908d157f81d345c5325a7), Theodore Ts'o, `ext4: Automatically allocate delay allocated blocks on rename` | exact rename-overwrite delayed-allocation intervention and zero-length crash rationale |
| P2 | 2009-03-17 | primary source code/commit | Linux commit [`afd4672d...`](https://github.com/torvalds/linux/commit/afd4672dc7610b7feef5190168aa917cc2e417e4), `ext4: Add auto_da_alloc mount option` | makes the safety behavior administratively disableable; bounds it as policy, not syscall semantics |
| P3 | 2009-06-09 | primary stable-review archive | [`[patch 78/87] ext4: Add auto_da_alloc mount option`](https://lkml.iu.edu/hypermail/linux/kernel/0906.1/00889.html) | independently accessible period archive reproducing P2 and its `NO_AUTO_DA_ALLOC` gating |
| P4 | current, inspected 2026-09 | official kernel documentation | [`Documentation/admin-guide/ext4.rst`](https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/ext4.rst) / [rendered kernel docs](https://cdn.kernel.org/doc/html/latest/admin-guide/ext4.html) | current `auto_da_alloc`, `data=ordered`, `data=writeback`, journal-commit semantics |
| P5 | 2026-02-08 | Linux interface documentation | [`rename(2)`, man-pages 6.18](https://man7.org/linux/man-pages/man2/rename.2.html) | atomic replacement as concurrent pathname-visibility relation |
| P6 | 2026-02-08 | Linux interface documentation | [`fsync(2)`, man-pages 6.18](https://man7.org/linux/man-pages/man2/fsync.2.html) | file data/metadata synchronization and explicit separate directory-entry synchronization |
| P7 | 2022-09-01 | primary developer discussion | Jan Kara, [`Re: [PATCH -next] ext4: ensure data forced to disk when rename`](https://lkml.iu.edu/hypermail/linux/kernel/2209.0/00366.html) | continuity guardrail: ext4 does not promise data securely on disk before rename; userspace must request the guarantee |

P1 and P2 are the main historical implementation anchors. P3 is a stable-review reproduction rather than an independent invention witness. P4–P7 are later continuity/interface evidence and are dated accordingly.

---

## Direct source checks

### P1 — 24 February 2009 rename allocation change

GitHub's canonical Linux commit record gives author/committer Theodore Ts'o and timestamp `2009-02-24T04:05:27Z`. The commit message says the overwrite-by-rename path should force delayed-allocation blocks to allocation so that, with `data=ordered`, data can be pushed out together with journal commit; the stated failure symptom is a zero-length file after unexpected crash.

The patch adds `force_da_alloc` to `ext4_rename()` and calls `ext4_alloc_da_blocks(old_inode)` after the journal operation succeeds when the overwritten destination path triggers the condition.

**Supported:** a specific ext4 implementation mitigation and its stated crash rationale.

**Not supported:** `rename()` as a durability barrier, directory durability by syscall return, or universal behavior outside the documented mode/implementation.

### P2/P3 — `auto_da_alloc` is a policy switch

The canonical commit record dates `afd4672dc7610b7feef5190168aa917cc2e417e4` to 17 March 2009. The commit introduces `EXT4_MOUNT_NO_AUTO_DA_ALLOC` and gates the rename/truncate safety path on that option. The June stable-review post reproduces the patch and states that disabling the feature may be desirable when unexpected crashes are considered low risk because the safety behavior reduces delayed-allocation effectiveness.

**Supported:** the mitigation is configurable policy, not an intrinsic property of the rename syscall.

### P4 — current ext4 documentation keeps the guarantee mode- and commit-qualified

The current kernel docs describe `auto_da_alloc(*)` as detecting replace-via-rename / truncate patterns and allocating delayed blocks so that, at the **next journal commit** under default `data=ordered`, new-file data are forced out before rename commit. The docs separately state that `data=writeback` does not preserve data-before-metadata ordering.

**Supported:** relative ordering in a named configuration.

**Not supported:** immediate persistence at `rename()` return or one behavior shared by every data mode.

### P5 — `rename` atomicity is a pathname-observer property

Linux man-pages 6.18 says replacement of an existing `newpath` is atomic in the sense that another process does not see a point where `newpath` is missing.

**Supported:** live namespace visibility atomicity.

**Not supported:** failure-surviving persistence of the new binding or payload.

### P6 — file and directory durability have explicitly distinct scopes

Linux man-pages 6.18 says successful `fsync(fd)` flushes modified file data and associated file metadata to storage and waits for completion. It explicitly adds that this does not necessarily ensure the containing directory entry has reached disk; a separate `fsync()` on a directory fd is needed.

**Supported:** `file fsync ≠ directory-entry fsync` as an interface-level distinction.

### P7 — later ext4 maintainer clarification preserves the boundary

In September 2022 Jan Kara rejected a proposal to wait for all file data before rename as an unnecessary performance cost. He states that ext4 does not guarantee data are securely on disk before rename and that userspace is responsible if it needs that guarantee; the existing behavior is intended to make the vulnerable window smaller for careless applications.

**Supported:** later maintainer-level continuity of the heuristic-versus-guarantee distinction.

**Not supported:** proof that this exact wording or every implementation detail already held in 2009.

---

## Claim ledger

| Claim | Type | Evidence | Status / limit |
| --- | --- | --- | --- |
| ext4 added an overwrite-by-rename delayed-allocation intervention on 24 Feb 2009 | H/P | P1 | grounded exact commit/date |
| the stated purpose included avoiding zero-length replacement files after unexpected crash in `data=ordered` | H/P | P1 | grounded, configuration-bounded |
| `auto_da_alloc` became a switch for that safety behavior in March 2009 | H/P | P2/P3 | grounded exact canonical commit plus stable archive |
| the mitigation can be disabled | H/P | P2/P3 | grounded; therefore not intrinsic rename semantics |
| current ext4 docs tie the behavior to next journal commit and default ordered mode | H/P | P4 | grounded current contract only |
| `data=ordered` and `data=writeback` have different data/metadata ordering | H/P | P4 | grounded current docs |
| existing-target rename is atomically replaced for ordinary pathname observers | H/P | P5 | grounded current Linux syscall docs |
| rename visibility atomicity implies crash durability | X | P5/P6/P7 | rejected |
| file `fsync` includes file data and associated file metadata | H/P | P6 | grounded current Linux docs |
| file `fsync` necessarily persists containing directory entry | X | P6 | explicitly rejected by source |
| directory `fsync` is a separate namespace durability obligation | H/P/E | P6 | grounded interface fact + engineering framing |
| `auto_da_alloc` is equivalent to explicit `fsync` | X | P4/P7 | rejected |
| data-before-rename order means rename is durable at syscall return | E/X | P1/P4/P7 | rejected |
| current man-page wording is verbatim 2009 semantics | X | source dating | rejected |
| a correct filesystem protocol proves lower device power-loss compliance | X | Cases 15/20/87, Synthesis 13 | rejected; cross-layer composition remains separate |

---

## Engineering decomposition

The bounded state graph is:

```text
replacement payload
      +
replacement inode/file metadata
      +
current destination-name binding
      +
writeback/journal ordering state
      +
lower storage persistence contract
```

The relevant operations do not collapse this graph into one Boolean:

```text
write()        → modifies file state, often still cached
fsync(file)    → closes file data/file-metadata durability scope
rename()       → atomically changes live namespace visibility
fsync(dir)     → closes containing-directory-entry durability scope
auto_da_alloc  → implementation heuristic/order aid for a common omitted-sync pattern
```

This is an **engineering reconstruction** from the typed interface contracts. Linux does not name one universal `durability closure` object.

---

## Prior-art / anti-anachronism controls

1. `rename()` predates ext4; the current man-page history lists C89 / 4.3BSD / POSIX lineage. P1 therefore cannot establish atomic rename invention.
2. `fsync()` predates ext4; the current man-page history lists 4.2BSD and later standardization. Case 124 does not claim ext4 invented file synchronization.
3. P1/P2 establish a 2009 ext4 implementation response to delayed-allocation crash behavior, not the origin of safe file replacement as a general problem.
4. P4–P7 are later evidence. They may confirm a distinction still present in current Linux, but they do not rewrite historical actors' exact 2009 contract.
5. Similar `write → sync → rename → sync-dir` patterns on other filesystems are future comparison, not implied genealogy.

---

## Cross-case boundary

- **Case 16:** dependency-preserving FFS writeback and explicit file durability closure; useful functional predecessor/comparator, not claimed ext4 genealogy.
- **Case 74:** JBD revoke records qualify replay after block reuse; different retained state and failure question despite journal adjacency.
- **Cases 15/20/87 + Synthesis 13:** lower device/interface persistence. A filesystem's correct ordering only composes with the durability actually supplied underneath.

---

## Related-repository check

A current `tmzncty/computing-archaeology` search for `soft updates fsync journaling crash consistency` returned no dedicated ext4 replace-by-rename case. If a broad ext4/JBD2/delayed-allocation genealogy is developed later, it belongs primarily there. Case 124 keeps only the retention-specific decomposition.

---

## Remaining evidence debt

- inspect the exact first documentation commit that introduced the modern prose around `auto_da_alloc`;
- trace directory-`fsync` wording across Linux man-pages revisions rather than using only the current contract;
- fault-inject 2009-era and current ext4 under `data=ordered`, `data=writeback`, `auto_da_alloc`, and `noauto_da_alloc`;
- test cross-directory rename and both parent-directory durability scopes;
- inspect ext4 fast-commit interaction;
- compare other filesystems without assuming Linux/ext4 semantics;
- validate lower-layer Flush/FUA/barrier behavior on named devices.
