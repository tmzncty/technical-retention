from pathlib import Path
import re

CASE_PATH = Path('cases/145-jffs2-garbage-collection-negative-state-evidence.md')
EVIDENCE_PATH = Path('evidence/145-jffs2-2001-garbage-collection-negative-state-grounding.md')
INDEX_PATH = Path('CASE_INDEX.md')
ROADMAP_PATH = Path('ROADMAP.md')

for p in (INDEX_PATH, ROADMAP_PATH):
    if not p.exists():
        raise SystemExit(f'missing required file: {p}')
if CASE_PATH.exists() or EVIDENCE_PATH.exists():
    raise SystemExit('Case 145 path already exists; refusing to overwrite concurrent work')

CASE = r'''# JFFS2 Garbage Collection: Obsolete-Node Reclamation, Truncation Evidence, and Explicit Zero-State Retention

## Status

**`grounded`**

## Scope

- **System:** JFFS2 as publicly documented and shipped in the Linux 2.4 era in 2001.
- **Historical anchor:** David Woodhouse's 10 October 2001 technical paper, plus archival Linux 2.4.10 source/announcement evidence from September 2001.
- **Retention question:** when raw-Flash filesystem nodes are superseded, unlinked, truncated, relocated, or erased, which retained relations distinguish current file state from physically surviving stale nodes, and which evidence is required before an erase block becomes reusable?

This is not a complete history of JFFS/JFFS2, log-structured file systems, Linux MTD, Flash translation layers, wear leveling, or secure erase. It does not claim that JFFS2 invented Flash garbage collection, log-structured storage, tombstones, explicit zero runs, or erase verification.

The bounded question is narrower:

> **How can a raw-Flash filesystem safely forget obsolete physical nodes when stale bytes may outlive logical supersession, and why can the absence of data or the appearance of an erased block be insufficient evidence of the state that should be admitted next?**

The case is useful because it places three retention relations in one 2001 implementation family:

1. a newer logical node can retire an older node before the old bytes are erased;
2. garbage collection can relocate still-current data before reclaiming its old erase block;
3. negative/reuse evidence (`JFFS2_COMPR_ZERO`, `CLEANMARKER`) can remain constitutive even though that evidence is much smaller than the stale data or erased capacity whose interpretation it controls.

---

## Historical vocabulary

The primary 2001 source uses period terms including:

- `JFFS2`;
- `node` and physical node;
- `version`;
- `obsolete` / `obsoleted node`;
- `clean_list`, `dirty_list`, and `free_list`;
- `garbage collection`;
- `erase block`;
- `hole` and `truncation`;
- `JFFS2_COMPR_ZERO`;
- `JFFS2_NODETYPE_CLEANMARKER`;
- `link`, `unlink`, and directory-entry node.

The project phrases **negative currentness evidence**, **reuse admission evidence**, **retirement relation**, and **stale-positive suppression** are engineering reconstructions. They are not asserted as JFFS2 developers' 2001 vocabulary.

---

## Retained state and physical substrate

JFFS2 operates directly on erase-block Flash rather than exposing the filesystem as a conventional overwrite-in-place block filesystem. Nodes are written sequentially; an erase block can contain valid and obsolete nodes; and an erase operation applies at erase-block granularity.

The retention target therefore cannot be reduced to `file payload bytes`. At least the following relations matter in the bounded design:

- inode and directory-entry identity;
- node `version` ordering/currentness;
- byte-range coverage of data nodes;
- whether a physical node has been superseded/obsoleted;
- the erase-block population of valid versus obsolete nodes;
- explicit zero-range nodes used after truncation/extension;
- post-erase `CLEANMARKER` evidence qualifying a block as safely reusable.

A physical node can survive while no longer contributing to current file contents. Conversely, a tiny node containing no ordinary file payload can remain necessary to keep old surviving payload from becoming logically visible again.

---

## Historical record: JFFS2 public in 2001

David Woodhouse's 10 October 2001 paper says that, after discussion beginning around a January 2001 compression requirement, JFFS2 was implemented as a substantial reimplementation of JFFS and at the time was usable with Linux 2.4 kernels. The paper documents its node format, block lists, mount scan, garbage collection, truncation/hole handling, and clean-marker mechanism.

An archived copy of Linus Torvalds's Linux 2.4.10 release announcement, dated 23 September 2001, explicitly lists JFFS2 among the major filesystem updates. Archival 2.4.10 patch mirrors contain the JFFS2 implementation. These provide a conservative **September–October 2001 public floor** for the bounded mechanism.

This is not a first-invention claim. The same paper describes the original Axis Communications JFFS as the predecessor and treats JFFS2 as a reimplementation responding to limitations in that earlier design. Broader JFFS/log-structured/Flash-filesystem genealogy remains outside this case.

---

## Logical supersession can precede physical reclamation

### Historical record

Woodhouse describes JFFS2 erase blocks as belonging to several lists. A `dirty_list` block can contain at least one obsoleted node while still containing valid nodes. When free space falls below a heuristic threshold, garbage collection selects an older block and moves nodes until the older erase block can be erased and its space reclaimed.

During mount, JFFS2 first scans the physical medium and validates node CRCs. It caches version and range information and later constructs per-inode maps so that obsoleted nodes can be detected.

For directory entries, unlinking is represented by writing a higher-version dirent for the same name with target inode number zero.

### Engineering reconstruction

These mechanisms separate several events that are easy to collapse:

```text
new/current logical relation established
        ↓
older physical node becomes obsolete
        ↓
old node may remain as dirty space
        ↓
GC preserves any still-current nodes elsewhere
        ↓
whole old erase block becomes reclaimable
        ↓
erase physically recovers free space
```

Therefore:

- `newer/current node established != older-node physical erasure`;
- `obsolete node != immediately reusable bytes`;
- `logical unlink != physical purge`;
- `physically readable node != current/admissible file state`.

The mount-time scan is especially useful for the repository's currentness vocabulary. Physical presence supplies candidates; version/range relations decide which candidates still contribute to the current inode map.

---

## Garbage collection can relocate current state without a logical update

### Historical record

The 2001 paper says garbage collection can obtain the inode corresponding to a physical node, reconstruct the relevant page, recompress it, and write a replacement node so that the original becomes obsolete. It also notes a space-bounding complication: if recompression would expand a node beyond available slack space, JFFS2 may copy the original node intact while preserving its original `version` number.

The block-selection policy also occasionally takes blocks from `clean_list`, moving still-valid data so that erase cycles are distributed rather than repeatedly consuming only already-dirty blocks.

### Engineering reconstruction

A new physical embodiment created by GC is not necessarily a new application-visible value. In the exact-copy path even the logical version may remain the same.

So:

> **physical relocation != logical mutation**

and:

> **wear-distribution movement != forgetting**.

This is a useful contrast with Case 04 mapped Flash. Both can preserve logical designation/currentness while physical embodiment changes, but JFFS2 performs the relation at a raw-Flash filesystem layer with explicit inode/node/version semantics. The comparison is functional; it is not an FTL genealogy claim.

---

## Truncation: absence is not always sufficient negative state

This is the case's strongest retention boundary.

### JFFS predecessor assumption

The paper explains a problem created by truncating a file and later writing beyond the new end. The intervening range is a hole and must read as zero.

For the original JFFS, truncation wrote a node recording the new length and marked older nodes beyond that point obsolete in memory. Its sequential garbage-collection order ensured that old payload nodes for the truncated range were collected before the truncation node itself. Woodhouse states the key historical dependency explicitly: correct behavior was guaranteed because **evidence of the truncation remained until the old data were erased**.

That is already a retention rule. The negative state did not merely describe what should be forgotten; it had to outlive the stale positive data whose reappearance it prohibited.

### JFFS2 out-of-order collection changes the obligation

JFFS2 allows erase blocks to be collected out of order. The old ordering invariant therefore cannot be reused safely: if a truncation record disappeared while stale older data for the hole still survived elsewhere, those old bytes could `show through` during reconstruction.

The design response was not to represent a proper hole as a total absence of information. When extending past EOF, JFFS2 writes a `JFFS2_COMPR_ZERO` data node covering the gap. The node contains no ordinary data payload, yet its range means that reads return zeros.

The 2.4.10-era `read.c` implementation provides a direct code-level witness: when `ri->compr == JFFS2_COMPR_ZERO`, the read path fills the requested buffer with zero rather than reading stored payload bytes for that range.

### Engineering reconstruction

This yields a particularly clean distinction:

```text
stale positive bytes physically survive
             +
explicit zero-range node survives and remains current
             ↓
current logical read result = zero
```

Therefore:

- `absence of a current data node != authoritative zero`;
- `zero-range currentness evidence != stored zero-byte payload`;
- `negative evidence lifetime can be constrained by stale-positive lifetime`;
- `truncation/currentness evidence != complete deletion history`.

The point is not that every filesystem needs tombstones or explicit holes. It is that JFFS2 provides a concrete counterexample to the assumption that “nothing there” always encodes enough state to prevent older physical information from reacquiring authority.

---

## CLEANMARKER: erase appearance is not reuse authority

### Historical record

JFFS2 writes a `JFFS2_NODETYPE_CLEANMARKER` to a newly erased block to show that the erase operation completed successfully and that the block may safely be used for storage.

Woodhouse contrasts this with original JFFS behavior that treated a block appearing as all `0xFF` during scanning as free. Reported power-fail testing found this unsafe: interrupted erase could leave unstable Flash bits that happened to read as ones, and repeated readback was not sufficiently reliable to exclude later data loss. The accepted JFFS2 solution was to write a marker immediately after successful erase completion.

### Engineering reconstruction

A clean-looking physical pattern and a trusted completed transition are different things:

- `observed 0xFF appearance != demonstrated successful erase`;
- `erase completion != mere erase-looking bit pattern`;
- `successful erase evidence != block payload`;
- `block physically empty-looking != block admitted for reuse`.

`CLEANMARKER` is therefore a small retained **reuse-admission witness**. It does not cryptographically prove every cell's state, and this case does not generalize the reported 2001 power-fail behavior to every Flash technology. It grounds only the JFFS2 design's reason for refusing to infer safe reuse from apparent all-ones state alone.

---

## Forgetting and failure modes

Keep the following separate:

- **logical supersession** — a newer version/range relation makes an older node obsolete;
- **unlink** — a higher-version zero-target dirent retires one namespace link;
- **truncation / explicit zero relation** — a byte range is qualified to read as zero despite possibly surviving older data nodes;
- **garbage collection** — still-current nodes may be copied and an old erase block later reclaimed;
- **Flash erase** — recovers an erase block for reuse at this layer;
- **reuse admission** — `CLEANMARKER` records that JFFS2 regards the erase as successfully completed;
- **secure sanitization** — not established by these mechanisms.

JFFS2 garbage collection is a space-reclamation process. The sources inspected here do not establish forensic irrecoverability, device-wide purge, key destruction, or compliance with a sanitize specification. Case 44 remains the stronger command/policy forgetting boundary, and Case 47 remains the empirical raw-flash/remanence comparison.

---

## Cross-case comparison

### Case 04 — mapped Flash

Both cases separate logical identity/currentness from physical embodiment and require erase-block reclamation. Case 04 is an FTL/logical-address mapping case; Case 145 is a filesystem-on-raw-Flash node/version case. Similar relation, different layer and historical mechanism.

### Case 74 — JBD revoke

Both cases show that retained negative/control evidence can prevent older positive data from becoming authoritative. JBD revoke suppresses replay of stale committed block images after reuse; JFFS2's explicit zero-range node prevents stale old file data from showing through a hole. This is a functional analogy, not a shared implementation or genealogy.

### Case 41 — Cassandra tombstones

A Cassandra tombstone can remain necessary while a stale positive replica still exists. JFFS2's truncation evidence and zero-range node provide a local raw-Flash/filesystem counterpart in the abstract sense that **negative currentness evidence may need to outlive stale positive state**. Their consistency models, scales, and mechanisms are unrelated.

### Case 73 — GFS garbage collection

Both use delayed reclamation, but GFS separates namespace retirement and distributed replica cleanup, whereas JFFS2 reclaims mixed raw-Flash erase blocks after preserving current nodes. Shared `garbage collection` vocabulary does not imply one state machine.

### Case 44 — sanitization

JFFS2 block erase is performed for filesystem reuse and wear/space management. It is not evidence for an interface-level or security-level sanitize guarantee.

---

## Prior-art and genealogy boundary

The 2001 paper itself makes JFFS2's predecessor relation to Axis Communications' JFFS explicit, and its bibliography/context places the work in a wider log-structured/Flash-filesystem tradition. Accordingly:

- this case does not claim JFFS2 invented log-structured Flash storage;
- it does not claim first use of garbage collection or tombstone-like negative state;
- Linux 2.4.10 / October 2001 provides a **public implementation/documentation floor**, not an invention-priority date;
- exact pre-mainline Linux-MTD CVS history and broader JFFS/LFS/YAFFS/UBIFS genealogy belong primarily in `tmzncty/computing-archaeology` if pursued.

A fresh repository search found no existing dedicated JFFS2 study in either repository, so this bounded retention case does not duplicate known companion-repository work.

---

## Philosophical interpretation — bounded

The engineering evidence supports one modest philosophical observation: **forgetting can require retained evidence of what must no longer count**.

In the truncation example, physical persistence of older bytes is not enough to make them current, while mere absence of new payload is not enough to guarantee zero semantics. An explicit relation can preserve the fact that a range should count as empty/zero until stale positive embodiments cease to threaten reconstruction.

Likewise, the `CLEANMARKER` shows that an apparently blank substrate need not count as reusable until the system retains evidence of a successful transition into that state.

This does not make JFFS2 a theory of memory, archival absence, or human forgetting. It is a mechanism-level counterexample useful for the project's larger distinction among physical survival, logical currentness, reclamation, and admissibility.

---

## Source ledger

### P1 — David Woodhouse, JFFS/JFFS2 technical paper, 10 October 2001 — `H/P`

David Woodhouse, **“JFFS: The Journalling Flash File System”**, Red Hat, 10 October 2001, Sourceware HTML:
<https://sourceware.org/jffs2/jffs2-html/>

JFFS2 section:
<https://sourceware.org/jffs2/jffs2-html/node3.html>

Directly inspected anchors:

- JFFS2 reimplementation / Linux-2.4 context;
- erase-block `clean_list` / `dirty_list` / `free_list` and wear-distributing GC;
- higher-version zero-target dirent for unlink;
- `JFFS2_NODETYPE_CLEANMARKER` rationale and power-fail erase evidence;
- mount scanning, version/range caching, and obsolete-node detection;
- GC rewrite/exact-copy version behavior;
- truncation/file-hole discussion and `JFFS2_COMPR_ZERO`.

This is a manufacturer/developer-authored period technical record. It is not a formal proof or an independent failure study.

### P2 — Linux 2.4.10 release announcement, 23 September 2001 — `H/P*`

Archived reproduction of Linus Torvalds's release message:
<https://www.linuxtoday.com/developer/linus-torvalds-linux-2-4-10/>

It explicitly lists `jffs2` among major filesystem updates. Because the surviving page used here is an archival reproduction rather than an origin-hosted kernel mailing-list artifact, it is used only as a release-date/public-availability witness, not for detailed mechanism claims.

### P3 — Linux 2.4.10 archival implementation, `fs/jffs2/read.c` — `H/P*`

FUNET archival patch mirror:
<https://ftp.funet.fi/pub/linux/kernel/v2.4/patch-html/patch-2.4.10/linux_fs_jffs2_read.c.html>

The period patch implementation checks `ri->compr == JFFS2_COMPR_ZERO` and returns a zero-filled range, grounding the distinction between an explicit zero-state node and a stored zero-byte payload body.

### P4 — Linux 2.4.10 archival implementation, `fs/jffs2/readinode.c` — `H/P*`

FUNET archival patch mirror:
<https://ftp.funet.fi/pub/linux/kernel/v2.4/patch-html/patch-2.4.10/linux_fs_jffs2_readinode.c.html>

Used only as a source-level continuity witness for the period node/version/obsolescence machinery. Exact Linux-MTD CVS ancestry remains open.

---

## Evidence-strength note

The central mechanism claims depend on P1, a directly inspectable developer-authored period source. P2–P4 provide archival release/source witnesses but are mirrors; they are therefore not upgraded into origin-hosted primary facsimiles. No claim in this case depends on a current JFFS2 manual being projected backward onto 2001.

---

## Open debt

Still open:

- exact Linux-MTD CVS / pre-2.4.10 JFFS2 introduction genealogy;
- exact history of the clean-marker change beyond Woodhouse's retrospective statement that it followed real-application use;
- direct origin-hosted historical source snapshots if recoverable;
- later JFFS2 implementation evolution and current behavior;
- device-specific replication of interrupted-erase / unstable-bit behavior;
- fault injection across GC copy, truncation, cleanmarker write, mount recovery, and erase interruption;
- interaction with modern raw-NAND bad-block/ECC layers;
- managed-SSD/FTL garbage collection composition;
- broader JFFS/LFS/Flash-filesystem genealogy.

None is required to support the bounded 2001 relation established here.

---

## Maturity note

This case is `grounded` because the central claims — mixed valid/obsolete erase blocks, relocation-before-reclamation, version/range-based obsolescence, explicit zero-range state after truncation, and post-erase clean-marker reuse qualification — are directly anchored in a period developer-authored technical record, with archival 2.4.10 release/source witnesses for the public implementation floor.
'''

EVIDENCE = r'''# Evidence 145 — JFFS2 2001 garbage collection, negative-state retention, and erase-admission grounding

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
'''

CASE_PATH.write_text(CASE, encoding='utf-8')
EVIDENCE_PATH.write_text(EVIDENCE, encoding='utf-8')

index = INDEX_PATH.read_text(encoding='utf-8')
row_anchor = '| [Apache ZooKeeper Ephemeral Znodes: Session-Scoped Liveness, Timeout-Qualified Retirement, and Logical Deletion](cases/144-zookeeper-ephemeral-session-liveness.md) |'
pos = index.find(row_anchor)
if pos < 0:
    raise SystemExit('Case 144 table-row anchor not found')
line_end = index.find('\n', pos)
if line_end < 0:
    raise SystemExit('Case 144 row newline not found')
new_row = '| [JFFS2 Garbage Collection: Obsolete-Node Reclamation, Truncation Evidence, and Explicit Zero-State Retention](cases/145-jffs2-garbage-collection-negative-state-evidence.md) | **grounded** | raw-Flash nodes + node versions/ranges + obsolete/dirty-block state + explicit zero-range nodes + `CLEANMARKER` reuse evidence | separate logical supersession/unlink/truncation, stale physical-node survival, current-node relocation, erase-block reclamation, erase-completion evidence, and reuse admission | [2001 grounding](evidence/145-jffs2-2001-garbage-collection-negative-state-grounding.md); pre-mainline CVS genealogy, later source evolution, device-specific erase-failure behavior, managed-FTL composition, and fault injection remain open |\n'
index = index[:line_end+1] + new_row + index[line_end+1:]

findings = r'''

## Case 145 — JFFS2 garbage-collection / negative-state findings

Grounding record: [`evidence/145-jffs2-2001-garbage-collection-negative-state-grounding.md`](evidence/145-jffs2-2001-garbage-collection-negative-state-grounding.md).

- **3127 — September–October 2001 public floor != invention date:** Linux 2.4.10's 23-Sep-2001 release record names JFFS2 and Woodhouse's 10-Oct-2001 period paper documents the bounded mechanism; neither establishes first implementation, deployment, or invention priority. (`H/P`, `H/P*`, `X`)
- **3128 — logical supersession != physical erasure:** a newer/current node can make an older node obsolete while the older physical node remains in dirty erase-block space until later collection. (`H/P`, `E`)
- **3129 — obsolete node != immediately reusable block:** an erase block may mix obsolete and still-valid nodes, so current content must be preserved before whole-block erase/reuse. (`H/P`, `E`)
- **3130 — garbage-collection relocation != logical update:** JFFS2 can rewrite/recompress current data into a replacement node solely to reclaim an old block, without an application-level payload change. (`H/P`, `E`)
- **3131 — physical relocation need not advance node version:** the bounded exact-copy GC path can preserve the original `version` number when expansion would exceed available slack space. (`H/P`, `E`)
- **3132 — physical node presence != current inode contribution:** mount scans candidate nodes but uses validity, version, and byte-range relations to identify obsoleted nodes and reconstruct the current map. (`H/P`, `E`)
- **3133 — logical unlink != physical purge:** JFFS2 retires a link by writing a higher-version dirent with target inode zero; the namespace transition does not itself establish erasure of older nodes. (`H/P`, `E`)
- **3134 — truncation evidence can outlive discarded payload:** Woodhouse says original JFFS correctness relied on truncation evidence remaining until old data for the affected range had been erased. (`H/P`, `E`)
- **3135 — out-of-order GC changes the negative-state retention obligation:** JFFS2 cannot rely on JFFS's sequential collection order to ensure stale data disappears before truncation evidence. (`H/P`, `E`)
- **3136 — absence of information != authoritative zero:** a proper hole represented by no information could allow surviving older data to `show through`, so absence alone is not a sufficient currentness witness in the bounded reconstruction regime. (`H/P`, `E`, `X`)
- **3137 — explicit zero node is retained negative/currentness evidence:** `JFFS2_COMPR_ZERO` represents a byte range that must read as zero while potentially stale older positive data can still physically exist. (`H/P`, `E`)
- **3138 — zero-range semantics != stored zero-filled payload:** the period 2.4.10 `read.c` path zero-fills the read result for `JFFS2_COMPR_ZERO`; the node can encode the relation without carrying ordinary zero data bytes for the range. (`H/P*`, `E`)
- **3139 — `CLEANMARKER` is post-erase reuse-admission evidence:** JFFS2 writes the marker after successful erase so the block can later be treated as safe storage space. (`H/P`, `E`)
- **3140 — apparent all-`0xFF` != proven reusable erase state:** the 2001 report says interrupted erase could leave unstable bits that happened to read as ones, and repeated readback was not sufficiently reliable in the tested setting. (`H/P`, `E`, `X`)
- **3141 — erase appearance != erase-completion authority:** JFFS2's reuse decision depends on retained successful-transition evidence rather than only the currently observed erased-looking bit pattern. (`H/P`, `E`)
- **3142 — wear-leveling movement != forgetting:** GC occasionally moves clean/current data to distribute erase cycles; physical relocation can therefore occur without logical deletion or supersession. (`H/P`, `E`, `X`)
- **3143 — reclamation erase != secure sanitization:** JFFS2 erase recovers filesystem space; the bounded sources do not establish device-wide purge, forensic irrecoverability, cryptographic erase, or a sanitize contract. (`E`, `A`, `X`)
- **3144 — related-repository boundary:** fresh searches found no dedicated JFFS2 study in this repository or `tmzncty/computing-archaeology`; broad JFFS/LFS/Flash-filesystem genealogy belongs primarily in the companion repository, while Case 145 keeps the retention/reclamation/negative-evidence relation. (`H/P` project-state record)
'''
if '## Case 145 — JFFS2 garbage-collection / negative-state findings' in index:
    raise SystemExit('Case 145 findings unexpectedly already present')
index = index.rstrip() + findings + '\n'
INDEX_PATH.write_text(index, encoding='utf-8')

roadmap = ROADMAP_PATH.read_text(encoding='utf-8')
phase2_anchor = '## Phase 2 — Build missing technical bridges\n\n'
if phase2_anchor not in roadmap:
    raise SystemExit('Phase 2 anchor not found')
phase2_bullet = ('- [x] Case 145 JFFS2 raw-Flash garbage-collection / negative-state-evidence slice — '
                 '[`cases/145-jffs2-garbage-collection-negative-state-evidence.md`](cases/145-jffs2-garbage-collection-negative-state-evidence.md) + '
                 '[`evidence/145-jffs2-2001-garbage-collection-negative-state-grounding.md`](evidence/145-jffs2-2001-garbage-collection-negative-state-grounding.md): '
                 "Woodhouse's 10-Oct-2001 period design record plus archival Linux 2.4.10 source/release evidence separate obsolete logical state from physically surviving nodes, mixed-block reclamation from current-data relocation, and an explicit `JFFS2_COMPR_ZERO` node from mere absence of information. `CLEANMARKER` further makes reuse admission depend on retained evidence of successful erase rather than apparent all-`0xFF` state after an interrupted erase. This closes the bounded `logical supersession != physical erasure`, `absence != authoritative zero`, and `erase appearance != reuse authority` seams without treating JFFS2 GC as secure sanitization or SSD-FTL genealogy. Exact pre-mainline Linux-MTD CVS genealogy, later implementation evolution, raw-device fault injection, and broader JFFS/LFS/Flash-filesystem history remain open and belong primarily in `computing-archaeology`.\n")
roadmap = roadmap.replace(phase2_anchor, phase2_anchor + phase2_bullet, 1)

pattern = re.compile(r'^- \[ \] garbage collection / reclamation — \*\*partially advanced by grounded Cases 73 and 125\*\*:.*$', re.M)
m = pattern.search(roadmap)
if not m:
    raise SystemExit('Phase 4 garbage-collection bullet anchor not found')
replacement = ('- [ ] garbage collection / reclamation — **partially advanced by grounded Cases 73, 125, and 145**: '
               'GFS 2003 separates logged deletion, hidden-name grace, namespace/chunk reference retirement, HeartBeat-driven replica cleanup, and stale-replica deauthorization; Case 125 adds local-filesystem crash-persistent orphan cleanup targets before blocks/inodes become reusable; Case 145 now adds raw-Flash filesystem reclamation in which newer/version-qualified state can make older physical nodes obsolete, GC moves still-current nodes before whole-block erase, explicit `JFFS2_COMPR_ZERO` prevents stale truncated data from reacquiring authority, and `CLEANMARKER` qualifies post-erase reuse rather than trusting an apparent all-ones pattern. Database GC, managed-SSD/FTL-controller GC, distributed/object-store reclamation beyond the bounded cases, damaged-recovery-metadata cases, media-sanitization closure, and broader reclamation genealogies remain open; broad JFFS/LFS/Flash-filesystem history belongs primarily in `computing-archaeology`;')
roadmap = roadmap[:m.start()] + replacement + roadmap[m.end():]
ROADMAP_PATH.write_text(roadmap, encoding='utf-8')
