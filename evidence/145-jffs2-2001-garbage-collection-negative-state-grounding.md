# Evidence 145 — JFFS2 2001 garbage collection, negative-state retention, and erase-admission grounding

## Scope

This evidence record grounds the bounded Case 145 claim that 2001 JFFS2 separates:

1. logical node supersession from physical stale-node survival;
2. current-node relocation from application-visible mutation;
3. obsolete-node accumulation from erase-block reclamation;
4. truncation/hole semantics from a mere absence of information;
5. apparent all-ones erase state from evidence that an erase completed successfully;
6. filesystem reclamation from secure sanitization.

It does not establish JFFS2 invention priority, a complete Linux-MTD CVS genealogy, current JFFS2 semantics, every Flash chip's power-fail behavior, or forensic erasure.

---

## Source classification

### P1 — Woodhouse 2001 Sourceware technical paper — `H/P`

David Woodhouse, Red Hat, **“JFFS: The Journalling Flash File System”**, dated **10 October 2001**:
<https://sourceware.org/jffs2/jffs2-html/>

JFFS2 section:
<https://sourceware.org/jffs2/jffs2-html/node3.html>

Why it is strong: developer-authored, period technical description, directly inspectable HTML, and unusually explicit about design tradeoffs and failure observations.

Limits: it is not an independent laboratory validation and not a formal proof of GC correctness; Woodhouse explicitly says a formal proof of the garbage-collection algorithm was desired and that the then-current approach was empirical.

### P2 — Linux 2.4.10 release message archival reproduction — `H/P*`

Linus Torvalds release message dated **23 September 2001**, reproduced by Linux Today:
<https://www.linuxtoday.com/developer/linus-torvalds-linux-2-4-10/>

It says Linux 2.4.10 includes major filesystem updates including `jffs2`. This is used only to establish a September-2001 mainline public floor. The mirror status is retained explicitly.

### P3 — Linux 2.4.10 patch mirror, `fs/jffs2/read.c` — `H/P*`

FUNET archival kernel patch mirror:
<https://ftp.funet.fi/pub/linux/kernel/v2.4/patch-html/patch-2.4.10/linux_fs_jffs2_read.c.html>

Direct code anchor: the read path checks `JFFS2_COMPR_ZERO` and zero-fills the output range. This confirms that the explicit hole/zero node can carry range semantics without storing ordinary zero payload bytes.

### P4 — Linux 2.4.10 patch mirror, `fs/jffs2/readinode.c` — `H/P*`

FUNET archival kernel patch mirror:
<https://ftp.funet.fi/pub/linux/kernel/v2.4/patch-html/patch-2.4.10/linux_fs_jffs2_readinode.c.html>

Used as period implementation continuity for node-fragment/version/obsolescence logic. The mirror is not used to claim exact source ancestry.

---

## Precise inspected anchors from P1

### A1 — reimplementation/public context

The JFFS2 section says a January-2001 compression requirement and mailing-list discussion led to a complete reimplementation, and that the current code at the time of writing ran on Linux 2.4. This supports a 2001 design/public-implementation context, not an invention date.

### A2 — erase-block lists and delayed reclamation

The paper says JFFS2 treats erase blocks individually. `clean_list` represents blocks full of valid nodes; `dirty_list` represents blocks containing at least one obsoleted node; `free_list` supplies writable erased blocks. GC normally selects dirty blocks but occasionally clean blocks to distribute wear.

Safe conclusion:

`obsolete physical node exists -> erase block may still contain current nodes -> block is not yet directly reusable`.

### A3 — logical unlink through a newer negative dirent

The `JFFS2_NODETYPE_DIRENT` description says a link is removed by writing a dirent with the same name, target inode zero, and a higher `version`.

Safe conclusion:

`namespace deletion currentness != immediate disappearance of all older physical dirent/inode/data nodes`.

### A4 — clean marker after successful erase

The paper says `JFFS2_NODETYPE_CLEANMARKER` is written to a newly erased block to show erase completed successfully and the block may safely be used. It contrasts this with original JFFS's assumption that an all-`0xFF` scan implied free space.

The historical failure observation is specifically bounded: power loss during erase on many Flash types could leave unstable bits that happened to read as ones; repeated readback was reported insufficiently reliable; JFFS2 therefore wrote a marker after successful erase.

Safe conclusions:

- `apparent 0xFF != JFFS2-qualified successful erase`;
- `physical-looking blankness != reuse authority`;
- `CLEANMARKER != file payload`.

Do not infer cryptographic proof, universal device physics, or secure sanitization.

### A5 — mount reconstruction and obsolete-node detection

The mount section says JFFS2 scans physical media, validates CRCs, caches `version` and data-range information, and then builds complete inode maps so obsoleted nodes can be detected.

Safe conclusion:

`physical node presence != current/admissible inode contribution`.

### A6 — GC rewrite / exact-copy behavior

The GC section says a replacement node can be written to obsolete the original. When recompression/merging would require too much expansion, an original node may be copied intact while preserving its original `version`.

Safe conclusions:

- `new physical embodiment != new logical payload value`;
- `physical relocation != necessarily new version`;
- `GC completion != application write history`.

### A7 — original JFFS truncation relation

For original JFFS, truncation writes a new node with the shortened length and marks older beyond-end nodes obsolete in memory. Sequential GC ensures old data for future holes are collected before the truncation node. The paper explicitly states that correctness depended on **evidence of truncation remaining until the old data were erased**.

Safe conclusion:

`negative/currentness evidence may need to outlive stale positive payload`.

### A8 — JFFS2 out-of-order GC invalidates the absence-only hole assumption

Because JFFS2 can collect blocks out of order, the predecessor's collection-order invariant cannot guarantee that old data will be gone before truncation evidence disappears. The paper says old data must never `show through` holes and rejects a proper hole as complete absence of information.

Safe conclusion:

`absence of current payload description != sufficient proof that stale positive data must not contribute`.

### A9 — explicit zero-range node

On write past EOF or truncate-to-larger-size, JFFS2 inserts a node using `JFFS2_COMPR_ZERO`: no actual data are contained in the node, but the represented byte range reads as zero. A large hole can be represented by one such physical node.

P3 independently supplies a period source-code witness that the read path zero-fills when it encounters this compression type.

Safe conclusion:

`explicit zero-state relation != stored zero-filled payload`.

---

## Evidence matrix

| Claim | Evidence | Classification | Safe strength |
|---|---|---|---|
| JFFS2 was publicly documented/shipped in Linux-2.4 context by Sep–Oct 2001 | P1 + P2 | `H/P`, `H/P*` | public floor, not invention date |
| erase blocks can contain valid and obsolete nodes | P1 A2 | `H/P` | direct period mechanism |
| GC moves current nodes before erasing an older block | P1 A2/A6 | `H/P` | direct period mechanism |
| GC may preserve the same version on an exact copy | P1 A6 | `H/P` | bounded implementation/design behavior |
| unlink uses higher-version zero-target dirent | P1 A3 | `H/P` | direct period format behavior |
| mount detects obsolete nodes using validated physical scan + version/range maps | P1 A5 | `H/P` | direct period recovery/currentness behavior |
| predecessor truncation evidence had to remain until old data erased | P1 A7 | `H/P` | direct developer historical explanation |
| JFFS2 uses explicit zero nodes to prevent stale data show-through | P1 A8/A9 + P3 | `H/P`, `H/P*` | strong bounded mechanism |
| apparent all-ones state was not accepted as safe erase evidence | P1 A4 | `H/P` | direct design rationale and reported tests |
| CLEANMARKER qualifies successful erase/reuse | P1 A4 | `H/P` | direct format/operation behavior |
| JFFS2 GC securely sanitizes media | unsupported | — | explicitly rejected |
| JFFS2 invented Flash GC / negative state | unsupported | — | explicitly rejected |

---

## Historical record vs engineering reconstruction

### Historical record

The period sources directly establish:

- node/version/range based reconstruction;
- dirty blocks containing obsoleted nodes;
- copying/recompressing live nodes during GC;
- block erase after live content is moved;
- higher-version zero-target dirent unlink;
- predecessor truncation evidence lifetime;
- `JFFS2_COMPR_ZERO` for file gaps;
- `CLEANMARKER` after successful erase;
- reported failure of apparent-all-ones/readback as sufficient erase evidence under interrupted erase in tested Flash behavior.

### Engineering reconstruction

The project derives, but does not attribute as historical terminology:

- `logical supersession != physical erasure`;
- `negative evidence lifetime can be coupled to stale-positive lifetime`;
- `absence != authoritative zero`;
- `erase appearance != reuse authority`;
- `physical relocation != logical mutation`;
- `reclamation != sanitization`.

### Functional analogy

Only at relation level:

- Case 04 mapped Flash: designation/currentness survives physical relocation;
- Case 41 Cassandra tombstone: negative evidence must survive long enough to suppress stale positive state;
- Case 74 JBD revoke: negative recovery evidence suppresses older positive replay;
- Case 73 GFS GC: logical retirement and physical reclamation are staged;
- Case 44 NVMe sanitize: demonstrates why reclamation erase must not be promoted into a security-erasure contract.

None of these comparisons establishes genealogy or mechanism identity.

### Philosophical interpretation

The bounded interpretive statement is only that technical forgetting can itself require retained relations indicating what no longer counts as current or what is safely reusable. The source does not warrant a general theory of absence, memory, or archival erasure.

---

## Prior-art boundary

P1 explicitly presents JFFS2 as a reimplementation following the original JFFS and describes JFFS as a Flash-specific log-structured filesystem. Therefore the conservative claim is:

> **JFFS2 provides a directly documented 2001 instance of the bounded mechanisms studied here; it is not treated as their point of invention.**

A fresh code/document search of `tmzncty/technical-retention` and `tmzncty/computing-archaeology` found no dedicated JFFS2 case. If a broad JFFS/JFFS2/LFS/YAFFS/UBIFS genealogy is later built, it belongs primarily in `computing-archaeology`; this file should remain the retention-specific evidence record.

---

## Stop conditions / unsupported extensions

Do not upgrade this evidence into any of the following without new sources:

- all stale JFFS2 bytes remain for a predictable time;
- block erase guarantees forensic irrecoverability;
- `CLEANMARKER` is proof of every physical cell's state;
- every Flash chip exhibits the exact interrupted-erase behavior reported in 2001;
- all modern JFFS2 versions use precisely the same algorithms;
- JFFS2 GC is equivalent to managed-SSD FTL GC;
- JFFS2 introduced tombstones, holes, log compaction, or garbage collection;
- source-version ordering is a complete user-operation history;
- a zero-range node is a stored payload full of zero bytes.

---

## Remaining evidence debt

1. Recover exact Linux-MTD CVS commits for JFFS2's early-2001 implementation and clean-marker introduction.
2. Obtain origin-hosted or cryptographically matched historical Linux source artifacts if possible.
3. Trace later JFFS2 on-flash-format and GC evolution separately from this 2001 floor.
4. Reproduce interrupted-erase/cleanmarker behavior on named raw-Flash parts if hardware/fault-injection work becomes worthwhile.
5. Test truncation/GC interruption and mount reconstruction under controlled faults.
6. Keep managed-SSD FTL garbage collection and secure-sanitization claims in their own cases.
7. Route broad Flash-filesystem genealogy to `computing-archaeology`.

The bounded Case 145 mechanism is sufficiently grounded without closing these broader questions.
