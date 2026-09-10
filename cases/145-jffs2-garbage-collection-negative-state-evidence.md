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
