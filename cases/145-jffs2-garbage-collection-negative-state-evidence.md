# JFFS2 Garbage Collection: Obsolete-Node Reclamation, Truncation Evidence, and Explicit Zero-State Retention

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

### Evidence navigation

- [`evidence/145-jffs2-2001-garbage-collection-negative-state-grounding.md`](../evidence/145-jffs2-2001-garbage-collection-negative-state-grounding.md) — canonical 2001 mechanism grounding.
- [`evidence/145-jffs2-2001-erase-pipeline-reuse-admission-deepening.md`](../evidence/145-jffs2-2001-erase-pipeline-reuse-admission-deepening.md) — Linux 2.4.10 source deepening: `erase_pending` → active erase → `MTD_ERASE_DONE` → `erase_complete` → qualification/cleanmarker → `free_list`, with retry and bad-list exits.
- [`evidence/145-jffs2-2004-2007-nand-oob-cleanmarker-placement-deepening.md`](../evidence/145-jffs2-2004-2007-nand-oob-cleanmarker-placement-deepening.md) — later NAND/OOB deepening: reuse-admission semantics versus physical marker placement, `MTD_OOB_AUTO`, conservative requalification, and bad-block-marker separation.
- [`evidence/145-jffs2-2001-mount-scan-reuse-reconstruction-deepening.md`](../evidence/145-jffs2-2001-mount-scan-reuse-reconstruction-deepening.md) — mount/restart deepening: volatile list state is rebuilt from retained Flash evidence; erased-looking blocks are not automatically reuse-authoritative; near-release `scan.c` lineage also preserves a whole-medium destructive-erase refusal when no valid JFFS2 state is reconstructed.

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

The archival Linux 2.4.10 `gc.c` source strengthens the ordering boundary. In inspected relocation paths it writes a replacement node before marking the prior node obsolete, and only when the selected GC block's `used_size` reaches zero does it move that block onto `erase_pending_list`.

### Engineering reconstruction

A new physical embodiment created by GC is not necessarily a new application-visible value. In the exact-copy path even the logical version may remain the same.

So:

> **physical relocation != logical mutation**

and:

> **wear-distribution movement != forgetting**.

The 2.4.10 source also lets the reclamation chain be made more explicit:

```text
some nodes obsolete
    !=
all current nodes safely relocated/retired
    !=
whole block erase-eligible
```

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

### Linux 2.4.10 erase-state pipeline deepening

The September-2001 archival source now makes the reuse boundary more granular than the paper alone.

`gc.c` moves a selected block to `erase_pending_list` only after the GC block has no `used_size` left. `erase.c` then moves pending work into an active erase state and submits an MTD erase. Immediate `-ENOMEM` or `-EAGAIN` failures requeue the block; other immediate failures exclude it through `bad_list`.

The asynchronous callback treats `MTD_ERASE_DONE` as a distinct stage: success moves the block to `erase_complete_list`, **not** directly to `free_list`. `jffs2_mark_erased_blocks()` then attempts a readback pass when it can allocate a verification buffer; read failure, short read, or a non-`0xFF` word rejects the block. The source also explicitly shows that this verification is not unconditional: if the temporary buffer allocation fails, the code proceeds while logging that it is assuming the erase worked.

Finally, JFFS2 writes the cleanmarker. A marker write failure or short write prevents free-list admission. Only after successful marker writing/accounting does the block enter `free_list`.

The bounded state relation is therefore:

```text
logical obsolescence
    != whole-block erase eligibility
    != erase queued
    != erase active
    != MTD_ERASE_DONE
    != successful readback qualification
    != cleanmarker write
    != free-list admission
```

The readback stage is conditional in this exact source snapshot, so it must not be rewritten as an invariant that every admitted block passed full readback verification.

A second retention distinction follows from carrier lifetime. `erase_pending_list`, `erasing_list`, and `erase_complete_list` are in-core workflow classifications. The cleanmarker is an on-Flash witness intended to survive restart. Thus:

```text
runtime maintenance phase
    != retained restart/reuse witness
```

The full state machine, retry paths, source classification, and non-claim ledger are in [`evidence/145-jffs2-2001-erase-pipeline-reuse-admission-deepening.md`](../evidence/145-jffs2-2001-erase-pipeline-reuse-admission-deepening.md).

### Mount-time reuse-authority reconstruction deepening

The restart side of that state machine is now grounded separately in [`evidence/145-jffs2-2001-mount-scan-reuse-reconstruction-deepening.md`](../evidence/145-jffs2-2001-mount-scan-reuse-reconstruction-deepening.md).

Woodhouse's 2001 paper explicitly describes mount as a reconstruction from the physical medium: the first pass scans Flash, checks node CRCs, allocates raw-node references and inode caches, and caches version/range information for later passes. The same period description says a `free_list` block contains the marker showing that it was properly and completely erased, while a block that merely appears all `0xFF` is not trusted because interrupted erase can leave unstable bits. Blocks lacking valid nodes are sent through erase and subsequent marker establishment rather than simply being declared free.

Linux 2.4.10's archival `nodelist.h` independently exposes the release-era in-core erase-block accounting, scan structures, `jffs2_scan_medium()`, and erase-side entry points. A later 2.4.19 patch identifies its 2.4.18 `scan.c` preimage as RCS revision `1.51` dated **19 September 2001** and preserves in unchanged context the scan-time refusal to proceed with destructive pending erases when no valid JFFS2 state has been reconstructed except in the allowed empty-medium case. Because that is a 2.4.18 preimage, it is retained as near-release source-lineage evidence rather than claimed as a byte-identical 2.4.10 facsimile.

The bounded restart relation is now:

```text
runtime free / erase workflow lists
    -> lost with the running kernel

retained node + CLEANMARKER evidence
    -> mount scan
    -> reconstructed in-core classification
    -> allocation / GC authority
```

and, separately:

```text
all-0xFF / no-valid-node appearance
    != successful-erase history
    != immediate free-list authority
```

This closes the mechanism-level `retained restart witness -> reconstructed reuse authority` seam while keeping one source-provenance debt explicit: exact branch-by-branch `BLK_STATE_*` release pinning still awaits a directly inspected origin-hosted or cryptographically matched Linux 2.4.10 `scan.c` artifact.

### NAND/OOB placement deepening, 2004–2007

Later Linux-MTD records add an important boundary to the 2001 mechanism. By 2004 JFFS2's NAND cleanmarker could reside in OOB rather than the ordinary data area. A 2007 JFFS2 patch moved NAND cleanmarker access from fixed OOB placement to `MTD_OOB_AUTO`, under which MTD can present free OOB bytes as a contiguous buffer even when their physical positions are discontinuous.

The same patch explicitly notes that the cleanmarker may move on some flashes; JFFS2 can handle this conservatively by re-erasing otherwise empty erase blocks and writing a marker in the currently recognized layout. It also checks NAND bad-block state separately from cleanmarker recognition.

The bounded relations are therefore:

- `reuse-admission semantics != fixed physical marker coordinates`;
- `ordinary data-area emptiness != absence of retained control evidence`;
- `physically surviving old marker != currently recognized reuse authority`;
- `missing cleanmarker != NAND bad-block identity`;
- `OOB co-location != common metadata meaning`.

The full source/provenance and non-claim ledger is in [`evidence/145-jffs2-2004-2007-nand-oob-cleanmarker-placement-deepening.md`](../evidence/145-jffs2-2004-2007-nand-oob-cleanmarker-placement-deepening.md). This is a later implementation deepening, not a claim that the 2007 code path was already present in 2001.

---

## Forgetting and failure modes

Keep the following separate:

- **logical supersession** — a newer version/range relation makes an older node obsolete;
- **unlink** — a higher-version zero-target dirent retires one namespace link;
- **truncation / explicit zero relation** — a byte range is qualified to read as zero despite possibly surviving older data nodes;
- **garbage collection** — still-current nodes may be copied and an old erase block later made erase-eligible;
- **erase obligation** — an erase-eligible block may be queued or retried without yet being active or complete;
- **lower-layer erase completion** — the MTD callback may report `MTD_ERASE_DONE` without the block yet being on `free_list`;
- **reuse admission** — cleanmarker success plus accounting moves the block to allocator-visible free space in the inspected 2001 path;
- **mount reconstruction** — restart loses volatile list membership and rebuilds it from retained Flash/node/marker evidence rather than treating erased appearance as self-authenticating;
- **Flash erase** — physically changes the erase block for reuse at this layer;
- **secure sanitization** — not established by these mechanisms.

JFFS2 garbage collection is a space-reclamation process. The sources inspected here do not establish forensic irrecoverability, device-wide purge, key destruction, or compliance with a sanitize specification. Case 44 remains the stronger command/policy forgetting boundary, and Case 47 remains the empirical raw-flash/remanence comparison.

---

## Cross-case comparison

### Case 04 — mapped Flash

Both cases separate logical identity/currentness from physical embodiment and require erase-block reclamation. Case 04 is an FTL/logical-address mapping case; Case 145 is a filesystem-on-raw-Flash node/version case. Similar relation, different layer and historical mechanism.

The later NAND deepening adds one narrower functional analogy: `MTD_OOB_AUTO` lets JFFS2 rely on a higher-level free-OOB view while MTD owns exact physical free-byte positions. This is **not** an FTL genealogy claim and does not make OOB autoplacement a block-mapping layer.

### Case 150 — managed-SSD garbage collection

Both Case 145 and Case 150 separate logical invalidation from later physical reclamation. The 2001 JFFS2 source exposes intermediate filesystem/MTD states — erase eligibility, pending work, active erase, lower-layer completion, marker qualification, allocator admission — that a managed SSD may hide behind controller firmware and a block interface. This is a functional layer comparison, not a claim of shared GC design or genealogy.

### Case 74 — JBD revoke

Both cases show that retained negative/control evidence can prevent older positive data from becoming authoritative. JBD revoke suppresses replay of stale committed block images after reuse; JFFS2's explicit zero-range node prevents stale old file data from showing through a hole. This is a functional analogy, not a shared implementation or genealogy.

### Case 41 — Cassandra tombstones

A Cassandra tombstone can remain necessary while a stale positive replica still exists. JFFS2's truncation evidence and zero-range node provide a local raw-Flash/filesystem counterpart in the abstract sense that **negative currentness evidence may need to outlive stale positive state**. Their consistency models, scales, and mechanisms are unrelated.

### Case 73 — GFS garbage collection

Both use delayed reclamation, but GFS separates namespace retirement and distributed replica cleanup, whereas JFFS2 reclaims mixed raw-Flash erase blocks after preserving current nodes. Shared `garbage collection` vocabulary does not imply one state machine.

### Case 78 — NAND bad-block retirement

Both JFFS2 cleanmarkers and NAND bad-block metadata can involve spare/OOB state, but their authority is different: a bad-block relation excludes a carrier from ordinary use, while a JFFS2 cleanmarker admits an otherwise usable erase block after successful erase. Physical neighborhood does not imply semantic identity.

The 2001 source adds another caution: JFFS2's runtime `bad_list` path for erase/qualification failure must not be promoted into a claim that a persistent NAND bad-block marker or device bad-block table has been written.

### Case 137 — LevelDB recovery-root selection

The new mount deepening permits one narrow functional comparison. Both LevelDB `CURRENT` and JFFS2's cleanmarker are small retained control evidence whose interpretation affects whether a much larger surviving substrate is admissible for a role. `CURRENT` selects a manifest/recovery root; a JFFS2 cleanmarker qualifies an erase block for reuse after restart. This is not a genealogy claim and the layers, failure models, and encodings are unrelated.

### Case 44 — sanitization

JFFS2 block erase is performed for filesystem reuse and wear/space management. It is not evidence for an interface-level or security-level sanitize guarantee. Likewise, `free_list` admission is not a sanitize-completion certificate.

---

## Prior-art and genealogy boundary

The 2001 paper itself makes JFFS2's predecessor relation to Axis Communications' JFFS explicit, and its bibliography/context places the work in a wider log-structured/Flash-filesystem tradition. Accordingly:

- this case does not claim JFFS2 invented log-structured Flash storage;
- it does not claim first use of garbage collection or tombstone-like negative state;
- Linux 2.4.10 / October 2001 provides a **public implementation/documentation floor**, not an invention-priority date;
- exact pre-mainline Linux-MTD CVS history and broader JFFS/LFS/YAFFS/UBIFS genealogy belong primarily in `tmzncty/computing-archaeology` if pursued.

A fresh repository search again found no existing dedicated JFFS2 study in `tmzncty/computing-archaeology`, so the retention-specific erase-pipeline, mount-reconstruction, and NAND/OOB deepenings added here do not duplicate known companion-repository work.

---

## Philosophical interpretation — bounded

The engineering evidence supports one modest philosophical observation: **forgetting can require retained evidence of what must no longer count**.

In the truncation example, physical persistence of older bytes is not enough to make them current, while mere absence of new payload is not enough to guarantee zero semantics. An explicit relation can preserve the fact that a range should count as empty/zero until stale positive embodiments cease to threaten reconstruction.

Likewise, the `CLEANMARKER` shows that an apparently blank substrate need not count as reusable until the system retains evidence of a successful transition into that state. The 2.4.10 erase pipeline adds a narrower point: a block may be logically erasable, queued, physically under erase, or even reported complete by the lower layer without yet being admitted by the filesystem allocator. The mount deepening adds that volatile admission state need not itself persist: lower-level retained evidence can be scanned to reconstruct a new running classification after restart. The later NAND evidence adds another: the meaning of such a witness can outlive one physical placement convention if the system retains a safe way to recognize or re-establish the qualifying relation.

This does not make JFFS2 a theory of memory, archival absence, or human forgetting. It is a mechanism-level counterexample useful for the project's larger distinction among physical survival, logical currentness, maintenance progress, reclamation, admissibility, and interpretability.

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

It explicitly lists `jffs2` among major filesystem updates. Because the surviving page used here is an archival reproduction rather than an origin-hosted kernel mailing-list artifact, it is used only as a release-date/public-availability witness, not for detailed mechanism claims. The new mount evidence additionally records the Indiana University LKML archive copy and kernel.org archive index.

### P3 — Linux 2.4.10 archival implementation, `fs/jffs2/read.c` — `H/P*`

FUNET archival kernel patch mirror:
<https://ftp.funet.fi/pub/linux/kernel/v2.4/patch-html/patch-2.4.10/linux_fs_jffs2_read.c.html>

The period patch implementation checks `ri->compr == JFFS2_COMPR_ZERO` and returns a zero-filled range, grounding the distinction between an explicit zero-state node and a stored zero-byte payload body.

### P4 — Linux 2.4.10 archival implementation, `fs/jffs2/readinode.c` — `H/P*`

FUNET archival patch mirror:
<https://ftp.funet.fi/pub/linux/kernel/v2.4/patch-html/patch-2.4.10/linux_fs_jffs2_readinode.c.html>

Used only as a source-level continuity witness for the period node/version/obsolescence machinery. Exact Linux-MTD CVS ancestry remains open.

### P5 — Linux-MTD CVS / mailing-list NAND cleanmarker records, 2004–2007 — `H/P`

The detailed source ledger is maintained in [`evidence/145-jffs2-2004-2007-nand-oob-cleanmarker-placement-deepening.md`](../evidence/145-jffs2-2004-2007-nand-oob-cleanmarker-placement-deepening.md). Its strongest primary anchor is Artem Bityutskiy's 2007 `MTD_OOB_AUTO` JFFS2 patch:

<https://lists.infradead.org/pipermail/linux-mtd/2007-February/017323.html>

It is used only for later NAND placement/recognition behavior and is not projected backward into the 2001 mechanism.

### P6 — Linux 2.4.10 archival `gc.c` / `erase.c` / `nodelist.h` — `H/P*`

FUNET archival patch mirrors:

- <https://www.nic.funet.fi/index/Linux/kernel/v2.4/patch-html/patch-2.4.10/linux_fs_jffs2_gc.c.html>
- <https://ftp.funet.fi/index/Linux/kernel/v2.4/patch-html/patch-2.4.10/linux_fs_jffs2_erase.c.html>
- <https://www.nic.funet.fi/index/Linux/kernel/v2.4/patch-html/patch-2.4.10/linux_fs_jffs2_nodelist.h.html>

These period source witnesses ground the finer erase-state pipeline: GC only queues a block after no used bytes remain; erase work can be retried or fail; `MTD_ERASE_DONE` moves to `erase_complete_list`; verification can reject the block but may be skipped if the verification buffer cannot be allocated; cleanmarker write precedes `free_list` admission. The mirror status is retained, and these files are not used to claim exact pre-mainline CVS introduction dates.

### P7 — near-release `scan.c` lineage and release archive — `H/P*`

- Linux 2.4.19 patch exposing the Linux 2.4.18 `scan.c` preimage and its RCS identifier: <https://ftp.funet.fi/pub/linux/kernel/v2.4/patch-html/patch-2.4.19/linux-2.4.19_fs_jffs2_scan.c.html>
- Linux 2.4.10 release message, IU LKML archive: <https://lkml.iu.edu/0109.2/1616.html>
- kernel.org v2.4 release archive: <https://www.kernel.org/pub/linux/kernel/v2.4/>

The preimage is identified as `scan.c,v 1.51 2001/09/19 00:06:35`; unchanged diff context retains the whole-medium refusal to erase pending blocks when no valid JFFS2 state is reconstructed outside the accepted empty case. This is near-release source-lineage evidence, not a directly rendered 2.4.10 `scan.c` facsimile. The detailed provenance and non-claim ledger are in Evidence 145D.

---

## Evidence-strength note

The central 2001 mechanism claims depend on P1, a directly inspectable developer-authored period source. P2–P4, P6, and P7 provide archival release/source witnesses but are mirrors or near-release source lineage; they are therefore not upgraded into origin-hosted primary facsimiles. P6 materially strengthens the live state-machine boundary because it exposes implementation transitions that the prose paper compresses into “erase” and “free” operations. P7 strengthens the restart side by tying the mount-scan safety guard to a `scan.c` RCS revision dated immediately before the 2.4.10 release, while preserving the explicit limitation that the rendered artifact is a 2.4.18 preimage. P5 is a later primary implementation record used to deepen NAND placement semantics. No claim in this case depends on a current JFFS2 manual being projected backward onto 2001.

---

## Open debt

Still open:

- exact Linux-MTD CVS / pre-2.4.10 JFFS2 introduction genealogy;
- exact history of the original clean-marker change beyond Woodhouse's retrospective statement that it followed real-application use;
- direct origin-hosted historical 2.4.10 source snapshots or cryptographically matched artifacts if recoverable;
- directly inspect an exact Linux 2.4.10 `fs/jffs2/scan.c` artifact so each release-specific `BLK_STATE_*` classification branch can be pinned without relying on the period prose plus near-release `scan.c` lineage;
- exact introduction commit for NAND OOB cleanmarkers and exact upstream merge/released-kernel floor for the 2007 `MTD_OOB_AUTO` change;
- later `MTD_OPS_AUTO_OOB`, large-OOB/ECC-layout, and mtd-utils compatibility evolution;
- device-specific replication of interrupted-erase / unstable-bit behavior;
- fault injection across GC copy, `erase_pending`, active erase, `MTD_ERASE_DONE`, readback, cleanmarker write, free-list transition, truncation, mount recovery, missing markers, and OOB-layout changes;
- interaction with modern raw-NAND bad-block/ECC layers beyond the bounded Case 78 comparison;
- managed-SSD/FTL garbage collection composition;
- broader JFFS/LFS/Flash-filesystem genealogy.

The source-level erase-pipeline debt is now partially closed: the 2.4.10 transition from GC eligibility through marker-qualified `free_list` admission is directly inspected. The mount-time reconstruction debt is also partially closed at mechanism level: the 2001 paper directly grounds scan/reconstruction and marker-qualified reuse, while near-release `scan.c` lineage grounds the conservative no-valid-state erase refusal. Exact 2.4.10 branch-level `scan.c` archaeology, crash-window experiments, device physics, and exact source genealogy remain open.

None is required to support the bounded 2001 relation or the 2004–2007 NAND/OOB placement deepening established here.

---

## Maturity note

This case remains `grounded`. The central claims — mixed valid/obsolete erase blocks, relocation-before-reclamation, version/range-based obsolescence, explicit zero-range state after truncation, staged erase/reuse admission, restart reconstruction from retained marker/node evidence, and post-erase clean-marker qualification — are directly anchored in a period developer-authored technical record plus archival 2.4.10 implementation witnesses and carefully bounded near-release source lineage. The erase-pipeline deepening strengthens the distinction among logical retirement, maintenance progress, lower-layer completion, verification, retained witness, and allocator admission; the mount deepening strengthens the distinction between transient runtime classification and restart-reconstructible reuse authority; the later NAND/OOB deepening strengthens the distinction between reuse-admission semantics and physical witness placement. None alone justifies promoting the entire case to `mature`.