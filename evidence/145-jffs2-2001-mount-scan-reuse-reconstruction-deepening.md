# Evidence 145D — JFFS2 2001 Mount Scan: Reconstructed Reuse Authority and Conservative Erase Admission

## Status

**`bounded deepening complete`**

This packet deepens one narrow open seam in Case 145: how a JFFS2 restart/mount reconstructs enough state from Flash to distinguish a block that may be used immediately from a block that merely *looks* erased or contains no currently admissible payload.

It does **not** attempt a general JFFS2 mount-history survey, a complete Linux-MTD genealogy, or a modern JFFS2 implementation study.

---

## Research slice

Existing Case 145 evidence already grounds the live erase path:

```text
GC retirement
    -> erase_pending
    -> active erase
    -> MTD_ERASE_DONE
    -> erase_complete
    -> optional readback qualification
    -> CLEANMARKER write
    -> free_list admission
```

The remaining question is the restart side of the same relation:

> after the volatile list state is gone, what retained evidence lets JFFS2 reconstruct whether an erase block is already reusable, still contains current/dirty state, or should be erased again?

The answer is intentionally bounded. The strongest 2001 source is David Woodhouse's developer-authored technical paper, which explicitly describes mount scanning, block lists, the `CLEANMARKER`, and the reason an apparently all-`0xFF` block is not trustworthy reuse evidence. Linux 2.4.10 archival source supplies the period data structures and scan/erase entry points. A later kernel patch preserves a near-release `scan.c` lineage identifier (`v1.51`, 2001-09-19) and the whole-medium erase-safety guard in unchanged context. That later diff is treated as a source-lineage witness, **not** silently upgraded into an exact Linux 2.4.10 `scan.c` facsimile.

---

## Source set and provenance

### P1 — David Woodhouse, JFFS/JFFS2 technical paper, 10 October 2001 — `H/P`

David Woodhouse, **“JFFS: The Journalling Flash File System”**, Red Hat, 10 October 2001:

- <https://sourceware.org/jffs2/jffs2-html/>
- JFFS2 section: <https://sourceware.org/jffs2/jffs2-html/node3.html>

Directly inspected statements used here:

- JFFS2 mount first scans the physical medium, validates node CRCs, allocates raw-node references, and caches version/range information;
- erase blocks are represented by in-core list membership including `clean_list`, `dirty_list`, and `free_list`;
- a free block in the described design contains a valid marker showing the block was properly and completely erased;
- `JFFS2_NODETYPE_CLEANMARKER` is written after successful erase completion and signifies that the block may safely be used;
- simply seeing `0xFF` in every byte was found unsafe under interrupted-erase testing;
- blocks that do not appear to contain valid nodes are erased and then receive the marker.

This is period developer-authored documentation, not an independent field-failure survey.

### P2 — Linux 2.4.10 release announcement and kernel archive — `H/P*`

Linus Torvalds's 23 September 2001 release message is preserved by the Indiana University LKML archive:

<https://lkml.iu.edu/0109.2/1616.html>

The message identifies Linux 2.4.10 and lists JFFS2 among the major filesystem updates. Kernel.org's v2.4 archive independently lists `linux-2.4.10` with the same 23 September 2001 release date:

<https://www.kernel.org/pub/linux/kernel/v2.4/>

These establish release/publication context only.

### P3 — Linux 2.4.10 archival `nodelist.h` patch — `H/P*`

FUNET archival patch mirror:

<https://www.nic.funet.fi/index/Linux/kernel/v2.4/patch-html/patch-2.4.10/linux_fs_jffs2_nodelist.h.html>

The patch introduces the JFFS2 source into the Linux 2.4.10 tree relative to 2.4.9 and exposes the period in-core structures. Relevant items include:

- `struct jffs2_raw_node_ref`, whose low flag bit records obsolescence;
- `struct jffs2_inode_cache` and temporary scan structures;
- `struct jffs2_eraseblock` with list membership plus `used_size`, `dirty_size`, and `free_size` accounting;
- the `jffs2_scan_medium()` declaration;
- the erase-side declarations `jffs2_erase_pending_blocks()`, `jffs2_mark_erased_blocks()`, and `jffs2_erase_pending_trigger()`.

This file does not by itself prove every branch in `scan.c`; it anchors the exact release-era state vocabulary and scan/erase composition.

### P4 — Linux 2.4.19 patch preserving the 2.4.18 `scan.c` preimage — `H/P*`

FUNET archival patch mirror:

<https://ftp.funet.fi/pub/linux/kernel/v2.4/patch-html/patch-2.4.19/linux-2.4.19_fs_jffs2_scan.c.html>

The diff identifies the Linux 2.4.18 preimage as:

```text
$Id: scan.c,v 1.51 2001/09/19 00:06:35 dwmw2 Exp $
```

The patch then changes that identifier to a 2002 branch revision. In unchanged-context lines immediately after the per-block classification loop, the preimage already contains the safety check that refuses to proceed with pending erases when there is no reconstructed used state and the medium is not simply the all-empty case, emitting the message that it is “refusing to erase blocks on filesystem with no valid JFFS2 nodes.”

This is important but provenance-limited: it is a 2.4.18 preimage shown by a 2.4.19 patch, not a directly rendered 2.4.10 `scan.c` artifact. Its RCS identifier predates 2.4.10's 23 September 2001 release, so it is retained here as **near-release source-lineage evidence**. It is not used to claim that every byte of the 2.4.18 preimage is proven identical to 2.4.10.

### C1 — later JFFS2 `scan.c` continuity — `C`, not the historical anchor

Later Linux JFFS2 source continues to make the list reconstruction explicit: an all-`0xFF`/`BLK_STATE_ALLFF` block is queued for erase rather than admitted directly to `free_list`, while a cleanmarker-qualified block can be admitted as free when otherwise clean. Modern source also retains the whole-medium “no valid JFFS2 nodes” safety guard.

This later source is used only as a continuity/cross-check. The historical claim below rests on P1 plus the period/near-period source lineage, not on projecting modern implementation details backward.

---

## Historical record

### H-145.31 — mount reconstructs operational state from the physical medium

Woodhouse describes JFFS2 mounting as a staged reconstruction. The first stage scans the physical medium, checks CRCs, allocates raw node references, creates inode-cache structures for inodes with valid nodes, and caches information such as version and covered data range. Subsequent passes build inode maps, identify obsolete nodes, account links, and remove unlinked inodes.

Therefore the in-core mount state is not assumed to survive a restart. It is rebuilt from retained Flash contents and relations.

This is a historical statement about the documented 2001 design.

### H-145.32 — `free_list` membership is associated with a retained marker, not naked emptiness

The 2001 paper says that blocks on the `free_list` in a new filesystem contain only one valid node: a marker showing the block was properly and completely erased.

The same paper defines `JFFS2_NODETYPE_CLEANMARKER` as a node written to a newly erased block after successful erase completion to show that the block can safely be used for storage.

The marker is therefore part of the period design's restart-visible evidence for reuse admission.

### H-145.33 — all-ones appearance was explicitly rejected as sufficient reuse evidence

Woodhouse contrasts JFFS2 with the original JFFS behavior of treating a block that appeared to contain `0xFF` throughout as free. Power-fail testing showed this could be unsafe because an interrupted erase could leave unstable bits that happened to read as ones. Re-reading the block repeatedly was reported as insufficiently reliable to rule the condition out.

The accepted design response was to write the marker after a successful erase.

The historical claim is deliberately narrow:

```text
observed all-ones appearance
    !=
trusted evidence that the preceding erase completed successfully
```

This is not generalized to every Flash technology or every later MTD driver.

### H-145.34 — blocks without valid nodes are sent through erase/marker establishment

The 2001 paper states that when JFFS2 encounters Flash blocks that do not appear to contain valid nodes, it triggers an erase operation and subsequently writes the appropriate marker node.

Thus “contains no valid node” is not equivalent to “already allocator-free.” The design can require another transition before the block becomes trusted reusable space.

### H-145.35 — the release-era implementation separates persisted Flash state from volatile scan structures

The Linux 2.4.10 archival `nodelist.h` exposes `struct jffs2_eraseblock`, list membership, block accounting, raw-node references, inode caches, and `jffs2_scan_medium()`. Those are in-core reconstruction structures. The same release-era source family contains the erase operations that later establish reusable blocks.

Nothing in this evidence says those linked-list heads themselves are persisted on Flash. Their semantics are reconstructed from what is found on the medium.

### H-145.36 — a near-release `scan.c` lineage contains an erase-safety refusal

The Linux 2.4.18 preimage shown in the 2.4.19 archival diff carries RCS revision `1.51` dated 19 September 2001. In unchanged context after scan classification, it refuses pending erase activity when no used state was reconstructed and the medium does not satisfy its allowed all-empty condition.

The code therefore preserves a second conservative boundary beyond per-block cleanmarker semantics:

```text
no reconstructed valid payload/current state
    !=
authority to erase every uncertain block automatically
```

Because P4 is a 2.4.18 preimage, this claim is about the near-release source lineage, not an assertion of byte-for-byte 2.4.10 identity.

---

## Engineering reconstruction

### E-145.31 — mount is an authority reconstruction, not merely a payload index rebuild

The 2001 mount scan does more than locate file bytes. It reconstructs relations that determine what the running filesystem is allowed to treat as current, dirty, obsolete, or reusable.

A bounded model is:

```text
retained Flash observations
    + node validity / CRC
    + version and range relations
    + CLEANMARKER evidence
        -> reconstructed in-core classifications
        -> later read / GC / allocation authority
```

The term **authority reconstruction** is project vocabulary. Woodhouse does not use that phrase.

### E-145.32 — volatile workflow state and retained restart evidence are different carriers

Existing Evidence 145B showed live in-memory transitions through `erase_pending`, active erase, `erase_complete`, qualification, marker write, and `free_list` admission.

This packet adds the restart side:

```text
volatile list membership lost at restart
    !=
loss of all evidence about block reuse status

retained node/marker contents
    -> mount scan
    -> new volatile classification
```

The on-Flash marker is therefore not the same state as `free_list` membership. It is evidence from which a new running instance may reconstruct an admissible free classification.

### E-145.33 — apparent emptiness is a candidate physical condition, not reuse authority

The cleanmarker rationale yields a three-way distinction:

```text
looks erased / all ones
    !=
erase known to have completed
    !=
block admitted as reusable by the filesystem
```

The first is an observation. The second is a transition-history claim. The third is a filesystem policy/state decision.

### E-145.34 — absence of valid payload can create a maintenance obligation rather than free space

A block with no valid JFFS2 nodes can still require erasure and marker establishment. In this bounded design, negative payload evidence may therefore imply **work to do**, not immediate allocation permission.

```text
no valid nodes found
    -> possible erase/requalification obligation
    != immediate free-list authority
```

This is distinct from the truncation seam elsewhere in Case 145, where explicit zero-state evidence suppresses stale payload. Here the retained/reconstructed relation concerns block reuse.

### E-145.35 — the safety guard is a fail-closed boundary at whole-medium scale

The near-release scan lineage's refusal to erase when it reconstructed no valid JFFS2 state but the medium was not an allowed empty case can be read as a conservative admission rule:

```text
scan cannot establish a coherent ordinary filesystem state
    -> do not convert uncertainty into destructive erase progress
```

This does not prove a formal crash-consistency theorem, and it does not mean every corruption path fails closed. It establishes one explicit refusal path.

### E-145.36 — runtime completion and restart recognition are separate checkpoints

Combining Evidence 145B with this packet gives a more complete seam:

```text
live erase completion
    -> marker establishment
    -> live free-list admission

restart
    -> volatile list state disappears
    -> retained marker/node evidence remains
    -> scan reconstructs new list/accounting state
```

Thus:

> **completion during one boot != persistence of that boot's list membership**

and

> **persistent reuse witness != permanently stored allocator data structure**.

---

## Functional comparisons — explicitly non-genealogical

### Case 137 — LevelDB `CURRENT`

Both cases show a small retained object controlling interpretation of a larger retained substrate. LevelDB `CURRENT` selects a manifest/recovery root; JFFS2's cleanmarker qualifies erase-block reuse. The mechanisms, failure models, layers, and histories are unrelated.

The functional comparison is only:

```text
small retained control evidence
    can determine
whether larger surviving state is admissible for a role
```

### Case 78 — NAND bad-block retirement

A cleanmarker and bad-block metadata can both influence allocator behavior, but their polarity differs: cleanmarker evidence can admit a block for reuse, while bad-block evidence excludes a carrier. Co-location in spare/OOB regions in later JFFS2/NAND implementations does not make them one metadata type.

### Case 150 — managed-SSD garbage collection

JFFS2 exposes the scan/requalification boundary at filesystem/MTD level. A managed SSD can hide comparable physical reclamation details behind firmware. This is a layer comparison only, not a controller genealogy claim.

---

## Philosophical interpretation — bounded

The mechanism supports one modest interpretation:

> an apparently empty substrate may still require retained evidence of **how it became empty** before the system is willing to treat it as available again.

That is not a claim that JFFS2 encodes a general philosophy of provenance. It is an engineering consequence of the reported interrupted-erase hazard and of the choice to retain a marker whose meaning survives the volatile execution that created it.

A second bounded point follows from mount reconstruction: operational classifications can disappear with a process and still be recoverable because the system retains enough lower-level evidence to recreate them. The retained thing need not be the same representation as the state later used in memory.

---

## Explicit non-claims

This packet does **not** claim:

1. that JFFS2 invented clean markers, mount scanning, Flash garbage collection, or conservative reuse admission;
2. that the 23 September 2001 Linux release date is the invention date of these mechanisms;
3. that the 2.4.18 `scan.c` preimage is a cryptographically proven byte-identical copy of Linux 2.4.10 `scan.c`;
4. that every branch of the later `BLK_STATE_*` switch is proven here to have identical 2.4.10 semantics;
5. that every all-`0xFF` Flash block is physically unstable;
6. that repeated readback can never detect interrupted erase on any Flash device;
7. that a cleanmarker proves every cell has reached an ideal erased state;
8. that cleanmarker recognition is a security or sanitization certificate;
9. that `free_list` membership is persisted directly on Flash;
10. that a block with no valid nodes is always erased successfully;
11. that every scan failure path is fail-closed;
12. that the whole-medium refusal guard is a complete corruption-recovery policy;
13. that mount reconstruction preserves all transient progress of an interrupted erase;
14. that the 2001 NOR-oriented semantics are identical to later NAND/OOB handling;
15. that later `MTD_OOB_AUTO` placement behavior existed in 2001;
16. that runtime `bad_list` membership means a persistent NAND bad-block marker was written;
17. that filesystem reclamation establishes forensic disappearance;
18. that the paper's reported power-fail observations provide a statistical failure-rate estimate;
19. that a modern JFFS2 source tree may be projected wholesale back to 2001;
20. that the functional comparisons above establish genealogy or design influence.

---

## Claim ledger

| ID | Type | Claim | Evidence | Strength |
| --- | --- | --- | --- | --- |
| H-145.31 | H | 2001 JFFS2 mount begins by scanning physical Flash, validating nodes and rebuilding in-core references/caches | P1 | strong |
| H-145.32 | H | 2001 `free_list` blocks are described as carrying a valid erase-completion marker | P1 | strong |
| H-145.33 | H | all-`0xFF` appearance was rejected as sufficient reuse evidence after power-fail testing | P1 | strong |
| H-145.34 | H | blocks without valid nodes are erased and then marked rather than simply assumed reusable | P1 | strong |
| H-145.35 | H | Linux 2.4.10 exposes scan/in-core block-accounting structures and erase-side entry points | P3 | strong, archival mirror |
| H-145.36 | H | near-release `scan.c` lineage contains the no-valid-JFFS2-nodes destructive-erase refusal | P4 | moderate/strong, release-lineage rather than exact 2.4.10 facsimile |
| E-145.31 | E | mount reconstructs operational authority from retained Flash evidence | H-145.31/32/34 | strong reconstruction |
| E-145.32 | E | persistent marker evidence is a different carrier from volatile `free_list` membership | H-145.31/32 + Evidence 145B | strong reconstruction |
| E-145.33 | E | erased-looking appearance, erase completion, and allocator admission are distinct states | H-145.33/34 | strong reconstruction |
| E-145.34 | E | no-valid-node state can imply maintenance/requalification rather than immediate free space | H-145.34 | strong reconstruction |
| E-145.35 | E | the whole-medium guard is one explicit fail-closed admission boundary | H-145.36 | bounded reconstruction |
| C-145.31 | C | later JFFS2 source retains the same broad all-FF-versus-marker admission topology | later source continuity only | corroborative, not historical anchor |
| I-145.31 | I | retained evidence can encode the provenance of an apparently empty state | E-145.33 | bounded interpretation |

---

## What this closes

This closes the **mechanism-level restart seam** left open by Case 145:

```text
runtime reuse state
    != persistent list membership

retained marker/node evidence
    -> mount reconstruction
    -> allocator / GC classification
```

It also makes explicit that JFFS2's 2001 design does not infer free-space authority from erased appearance alone. The paper's mount and cleanmarker descriptions are sufficient to establish that conceptual/reconstruction boundary without pretending that a later kernel source dump is a 2001 facsimile.

---

## Remaining evidence debt

Still open after this bounded deepening:

- obtain and directly inspect an origin-hosted or cryptographically matched **Linux 2.4.10 `fs/jffs2/scan.c`** artifact, so each exact `BLK_STATE_*` transition can be release-pinned rather than inferred from the period paper plus near-release lineage;
- reconstruct pre-mainline Linux-MTD CVS history and the exact cleanmarker introduction change;
- fault-inject power loss between erase completion, marker write, and later mount reconstruction;
- test malformed/missing marker paths against a period-compatible implementation;
- separate exact 2001 NOR behavior from later NAND/OOB scan/requalification semantics at commit granularity;
- reproduce the reported interrupted-erase instability on named Flash devices, if suitable hardware/archival data become available;
- examine how later summary nodes change scan cost without silently changing the underlying reuse-authority relation.

Broader JFFS/JFFS2/LFS/YAFFS/UBIFS genealogy remains better placed in `tmzncty/computing-archaeology`. A fresh repository search for `JFFS2` found no existing dedicated companion packet to reuse in this run.

---

## Bottom line

The 2001 record supports a precise retention boundary:

```text
apparently empty Flash
    != trusted erased history
    != allocator reuse authority

successful erase
    -> retained CLEANMARKER evidence
    -> later mount can reconstruct reuse status
```

The running kernel's lists are transient. What survives is lower-level Flash evidence from which those lists can be rebuilt. That is the new contribution of this slice; it does not alter Case 145's `grounded` maturity.