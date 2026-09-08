from pathlib import Path
import re

CASE_PATH = Path('cases/124-linux-ext4-rename-fsync-durability-closure.md')
EVIDENCE_PATH = Path('evidence/124-linux-ext4-2009-2026-rename-fsync-grounding.md')

case = r'''# Linux ext4 Replace-by-Rename: Atomic Visibility, `auto_da_alloc`, and `fsync` Durability Closure

## Scope

- **Bounded period:** the 2009 ext4 delayed-allocation intervention, checked against the current Linux interface/documentation contract through Linux man-pages 6.18 (2026).
- **Primary historical witnesses:** Linux commits `8750c6d5fcbd3342b3d908d157f81d345c5325a7` (24 February 2009) and `afd4672dc7610b7feef5190168aa917cc2e417e4` (17 March 2009), plus their June 2009 stable-review postings.
- **Current interface witnesses:** Linux `rename(2)` and `fsync(2)` man-pages 6.18, and current Linux ext4 documentation.
- **Research question:** when an application writes a replacement file and renames it over an existing pathname, which relation is made atomic, which state is merely ordered for later commit, and which durability obligations still require explicit synchronization?

This is not a general history of ext4, POSIX filesystems, journaling, or atomic file replacement. Case 16 already grounds BSD FFS soft updates and Case 74 grounds JBD revoke replay suppression. This case isolates a different boundary:

> **atomic pathname visibility, data-before-metadata ordering, file durability, and directory-entry durability are different retention relations.**

The 2009 ext4 workaround is treated as a historically specific compatibility/safety intervention, not as a portable durability theorem.

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
'''

evidence = r'''# Evidence 124 — Linux ext4 Replace-by-Rename / `fsync` Grounding, 2009–2026

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
'''

CASE_PATH.parent.mkdir(parents=True, exist_ok=True)
EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
if CASE_PATH.exists() or EVIDENCE_PATH.exists():
    raise SystemExit('Case 124 canonical path already exists; refusing duplicate integration')
CASE_PATH.write_text(case.strip() + '\n', encoding='utf-8')
EVIDENCE_PATH.write_text(evidence.strip() + '\n', encoding='utf-8')

roadmap_path = Path('ROADMAP.md')
roadmap = roadmap_path.read_text(encoding='utf-8')
roadmap_lines = roadmap.splitlines()
needle = '- [ ] file-system crash consistency —'
matching = [i for i, line in enumerate(roadmap_lines) if line.startswith(needle)]
if len(matching) != 1:
    raise SystemExit(f'Expected one filesystem crash-consistency roadmap row, found {len(matching)}')
i = matching[0]
roadmap_lines[i] = "- [ ] file-system crash consistency — **partially advanced by grounded Cases 16, 74, and 124**: [`cases/16-bsd-ffs-soft-updates-crash-admissibility.md`](cases/16-bsd-ffs-soft-updates-crash-admissibility.md) separates volatile application-visible metadata, dependency-safe stable writeback, immediate crash-admissible mount state, explicit `fsync` durability closure, and later reclamation. [`cases/74-linux-jbd-revoke-stale-replay-suppression.md`](cases/74-linux-jbd-revoke-stale-replay-suppression.md) adds negative recovery evidence that can suppress an older committed journal image after block reuse. [`cases/124-linux-ext4-rename-fsync-durability-closure.md`](cases/124-linux-ext4-rename-fsync-durability-closure.md), grounded by [`evidence/124-linux-ext4-2009-2026-rename-fsync-grounding.md`](evidence/124-linux-ext4-2009-2026-rename-fsync-grounding.md), now closes the bounded modern-Linux replace-by-rename relation: 2009 ext4 primary commits show a delayed-allocation compatibility heuristic (`auto_da_alloc`) intended to avoid the zero-length crash window under `data=ordered`, while current Linux interface documentation separately types atomic pathname visibility, file `fsync`, and containing-directory `fsync`. The broad item stays unchecked because copy-on-write/checkpoint consistency, transactional filesystems, complete WAL/journaling genealogy, cross-filesystem rename durability, ext4 fast-commit evolution, fault-injected replay/replacement validation, and lower-layer device-persistence composition remain distinct regimes;"
roadmap_path.write_text('\n'.join(roadmap_lines).rstrip() + '\n', encoding='utf-8')

index_path = Path('CASE_INDEX.md')
index = index_path.read_text(encoding='utf-8')
if 'cases/124-linux-ext4-rename-fsync-durability-closure.md' in index:
    raise SystemExit('Case 124 already indexed; refusing duplicate')
rows = index.splitlines()
anchors = [i for i, line in enumerate(rows) if 'cases/123-ata6-device-configuration-overlay-capability-retention.md' in line]
if len(anchors) != 1:
    raise SystemExit(f'Expected one Case 123 table row, found {len(anchors)}')
row = "| [Linux ext4 Replace-by-Rename: Atomic Visibility, `auto_da_alloc`, and `fsync` Durability Closure](cases/124-linux-ext4-rename-fsync-durability-closure.md) | **grounded** | replacement-file payload + inode/file metadata + destination directory-entry binding + delayed-allocation/journal ordering state + lower persistence contract | separate atomic live namespace visibility, relative data-before-metadata ordering, file durability, directory-entry durability, and lower-layer persistence; show compatibility heuristic ≠ explicit durability closure | [2009–2026 ext4 rename/fsync grounding](evidence/124-linux-ext4-2009-2026-rename-fsync-grounding.md); exact documentation/man-page genealogy, cross-directory rename, fast-commit evolution, named-device composition, cross-filesystem comparison, and fault injection remain open |"
rows.insert(anchors[0] + 1, row)
index = '\n'.join(rows).rstrip()
nums = [int(x) for x in re.findall(r'^- \*\*(\d+) —', index, flags=re.M)]
if not nums:
    raise SystemExit('Could not determine CASE_INDEX finding number')
n = max(nums) + 1
findings = [
    ('rename atomic visibility ≠ crash durability', 'current Linux `rename(2)` protects ordinary pathname observers from an intermediate missing destination; it does not itself certify that the replacement binding survives power loss. (`H/P`, `E`)'),
    ('file `fsync` ≠ directory-entry `fsync`', 'Linux `fsync(2)` explicitly requires separate synchronization of the containing directory when that directory entry must reach disk. (`H/P`)'),
    ('payload durability ≠ namespace durability', 'replacement-file bytes/inode state and the `target → replacement object` directory relation are separately synchronized retention targets. (`H/P`, `E`)'),
    ('data-before-rename ordering ≠ rename-durable-by-return', 'ext4 `auto_da_alloc` under documented `data=ordered` constrains order at journal commit; relative ordering does not prove that either persistence event already occurred when `rename()` returns. (`H/P`, `E`, `X`)'),
    ('compatibility heuristic ≠ explicit durability closure', 'the 2009 ext4 patches protect common unsynchronized application patterns but also make the behavior configurable; this is not a substitute for explicit file/directory synchronization. (`H/P`, `E`, `X`)'),
    ('`auto_da_alloc` policy ≠ intrinsic syscall semantics', 'the March 2009 mount option can disable the automatic allocation safety path, so the behavior belongs to ext4 policy/configuration rather than the definition of `rename()`. (`H/P`)'),
    ('one ext4 data mode ≠ one universal crash relation', '`data=ordered` preserves a data-before-metadata relation that `data=writeback` does not; mount-mode scope must remain explicit. (`H/P`, `X`)'),
    ('directory durability work ≠ payload rewrite', 'synchronizing the parent directory closes a namespace-metadata obligation and need not mean rewriting the entire already-synchronized replacement payload. (`H/P`, `E`)'),
    ('successful file synchronization ≠ durable expected pathname', 'the file can satisfy its own `fsync` scope while the desired containing-directory entry remains outside that completed scope. (`H/P`, `E`)'),
    ('stable pathname identity ≠ stable inode embodiment', 'replace-by-rename can keep the application-facing target name while changing which file object/inode the name designates; designation continuity does not require embodiment continuity. (`E`, `A`)'),
    ('2009 implementation fix ≠ invention of atomic replacement or `fsync`', 'current Linux histories place `rename` and `fsync` in older C/BSD/POSIX lineages; the ext4 evidence establishes a delayed-allocation-specific intervention, not origin priority. (`H/P`, `X`)'),
    ('current Linux contract ≠ verbatim 2009 contract', '2026 man-pages and current kernel docs are continuity/interface evidence and must not be projected backward as the exact historical wording of the 2009 patches. (`H/P`, `X`)'),
    ('filesystem ordering ≠ lower-device persistence compliance', 'a correct file/namespace synchronization protocol still depends on the cache/Flush/FUA/persistence-domain contract provided below it; Cases 15/20/87 and Synthesis 13 remain separate layers. (`A`, `E`)'),
    ('Case 16 `fsync` closure ≠ Case 124 namespace closure', 'soft updates already shows stronger explicit durability than ordinary writeback; Case 124 adds the counterexample that file synchronization still does not necessarily close the containing directory-entry relation. (`A`)'),
    ('journal adjacency ≠ one journaling mechanism', 'Case 74 revoke state qualifies stale redo after block reuse, while Case 124 concerns replacement payload/name durability; sharing JBD/ext-family context does not make their retained state or failure question identical. (`A`, `X`)'),
    ('related-repository boundary', 'current `tmzncty/computing-archaeology` search found no dedicated ext4 replace-by-rename durability case; broad ext4/JBD2/delayed-allocation genealogy belongs there if developed. (`H/P` project-state record)'),
]
section = ['','## Case 124 — Linux ext4 rename / `fsync` durability findings','']
for title, body in findings:
    section.append(f'- **{n} — {title}:** {body}')
    n += 1
index_path.write_text(index + '\n' + '\n'.join(section).rstrip() + '\n', encoding='utf-8')
