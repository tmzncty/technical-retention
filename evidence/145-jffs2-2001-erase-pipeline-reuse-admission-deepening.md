# Evidence 145 — JFFS2 2001 erase pipeline, completion, and reuse-admission deepening

## Status

**`bounded deepening complete`**

## Scope

This evidence record deepens Case 145 at one narrow implementation seam in the Linux 2.4.10-era JFFS2 code:

> **After garbage collection has made an erase block logically disposable, what distinct runtime stages remain before JFFS2 admits that block to `free_list` for reuse?**

The bounded answer is not simply “GC erases the block.” The inspected September-2001 source exposes a staged pipeline:

```text
all live/current content removed or relocated
    -> gcblock has no used bytes
    -> erase_pending_list
    -> erasing_list / MTD erase request
    -> MTD_ERASE_DONE callback state
    -> erase_complete_list
    -> optional all-0xFF verification pass
    -> CLEANMARKER write
    -> free_list admission
```

The implementation also has separate retry and quarantine paths. This makes Case 145 a stronger example of the distinction among **logical retirement**, **physical maintenance request**, **device-reported completion**, **verification**, **retained reuse evidence**, and **allocator admission**.

This record does **not** establish a hardware-level power-fail guarantee, forensic sanitization, universal MTD semantics, or a complete proof of JFFS2 GC correctness.

---

## Source classification

### P1 — Linux 2.4.10 archival implementation, `fs/jffs2/gc.c` — `H/P*`

FUNET archival Linux kernel patch mirror for Linux 2.4.10, patch dated **14 September 2001**:

<https://www.nic.funet.fi/index/Linux/kernel/v2.4/patch-html/patch-2.4.10/linux_fs_jffs2_gc.c.html>

The file identifies itself as JFFS2 code created by David Woodhouse / Red Hat, with CVS id `gc.c,v 1.51 2001/05/24`.

Direct anchors used here:

- a GC block is moved to `erase_pending_list` only when `c->gcblock` exists and `c->gcblock->used_size` is zero;
- the source log message describes that block as “completely obsoleted by GC” before the transition;
- the transition increments `nr_erasing_blocks` and triggers erase work;
- replacement-node paths write the replacement before marking the prior node obsolete.

Mirror status is retained explicitly. This source is used as a period implementation witness, not as proof of exact pre-mainline CVS ancestry.

### P2 — Linux 2.4.10 archival implementation, `fs/jffs2/erase.c` — `H/P*`

FUNET archival Linux kernel patch mirror, also dated **14 September 2001**:

<https://ftp.funet.fi/index/Linux/kernel/v2.4/patch-html/patch-2.4.10/linux_fs_jffs2_erase.c.html>

The file identifies itself as JFFS2 code created by David Woodhouse / Red Hat, with CVS id `erase.c,v 1.19 2001/03/25`.

Direct anchors used here:

- `jffs2_erase_pending_blocks()` moves a block from `erase_pending_list` into `erasing_list`, clears its used/dirty/free accounting, drops in-core node references for the block, and calls the MTD erase path;
- immediate `-ENOMEM` / `-EAGAIN` erase-start failures refile the block to `erase_pending_list` rather than admitting it for use;
- other immediate failures put the block on `bad_list`;
- the asynchronous erase callback distinguishes `MTD_ERASE_DONE` from non-done completion state;
- a successful callback moves the block to `erase_complete_list`, not directly to `free_list`;
- `jffs2_mark_erased_blocks()` can read the newly erased block back and reject read errors, short reads, or non-`0xFF` words;
- failure to allocate the temporary verification buffer causes the code to log that it is **assuming** the erase worked, so a readback pass is not an unconditional prerequisite in this version;
- JFFS2 then writes the clean marker;
- marker write errors or short writes route the block to `bad_list`;
- only after the marker write does the implementation account the marker, assign remaining free space, and append the block to `free_list`.

### P3 — Linux 2.4.10 archival implementation, `fs/jffs2/nodelist.h` — `H/P*`

FUNET archival Linux kernel patch mirror:

<https://www.nic.funet.fi/index/Linux/kernel/v2.4/patch-html/patch-2.4.10/linux_fs_jffs2_nodelist.h.html>

This provides the period in-core eraseblock accounting vocabulary and an especially relevant design comment: deletion-related negative nodes may need to remain non-obsolete until the older node they suppress has actually been removed from Flash. The corresponding `deletia` field is commented as prospective (`MAYBE`), so it is used only as a design-intent witness, not as evidence that a complete persisted deletion-retention structure shipped in this exact code snapshot.

### P4 — David Woodhouse, JFFS/JFFS2 technical paper, 10 October 2001 — `H/P`

<https://sourceware.org/jffs2/jffs2-html/node3.html>

The developer-authored period paper explains the higher-level reason for `CLEANMARKER`: apparent all-ones state after an interrupted erase was not accepted as sufficient evidence that the block was safely erased, so JFFS2 writes a marker following successful erase completion.

P4 supplies the design rationale; P1–P3 supply the finer-grained implementation state machine.

---

## Historical record

### H1 — GC eligibility precedes erase submission

The inspected `gc.c` does not enqueue a still-used GC block for erase. Near the end of a GC pass it checks whether `c->gcblock` exists and whether `used_size` has fallen to zero. Only then does it move the block to `erase_pending_list`, clear `c->gcblock`, increment `nr_erasing_blocks`, and trigger erase work.

This gives a direct implementation boundary:

```text
some nodes obsolete
    !=
whole block erase-eligible
```

and more specifically:

```text
dirty / partially obsolete block
    -> preserve or relocate remaining current nodes
    -> used_size == 0
    -> erase_pending
```

The code does not warrant the stronger claim that every logical node-retirement operation immediately schedules a hardware erase.

### H2 — replacement can be established before old-node retirement

Period `gc.c` paths for metadata and hole/data rewriting first write a replacement node. Only after a successful replacement write does the code mark the old node obsolete in the inspected paths.

That implementation ordering strengthens the existing Case 145 relation:

```text
new physical embodiment established
    -> old embodiment retired logically
    -> containing block may eventually become erase-eligible
```

It remains possible for application-visible meaning to stay unchanged across this movement. This is GC relocation, not necessarily a user mutation.

### H3 — `erase_pending` is not `erasing`

`jffs2_erase_pending_blocks()` takes a block from `erase_pending_list`, moves its space accounting into `erasing_size`, frees its in-core raw-node references, puts it on `erasing_list`, and then invokes `c->mtd->erase()`.

The distinction is operationally real because an erase request can fail immediately. In the inspected code:

- `-ENOMEM` and `-EAGAIN` refile the block on `erase_pending_list` for later work;
- other immediate failures move the block to `bad_list`.

Therefore:

```text
erase obligation retained
    !=
erase request successfully admitted by lower layer
```

A transient inability to start erase does not convert the block into free capacity.

### H4 — MTD-reported erase completion is not free-list admission

The asynchronous callback examines `instr->state`.

If the state is not `MTD_ERASE_DONE`, the code removes the block from the active erase path, accounts it as bad, and places it on `bad_list`.

If the state is `MTD_ERASE_DONE`, the code moves the block to `erase_complete_list`.

Crucially, the successful callback does **not** add the block directly to `free_list`.

This produces another directly observed boundary:

```text
lower-layer completion report
    !=
JFFS2 reuse admission
```

The name `erase_complete_list` therefore denotes a completed lower-layer step inside a larger filesystem state machine; it is not equivalent to allocator-visible reusable space.

### H5 — readback verification is a separate stage, but not an unconditional one

`jffs2_mark_erased_blocks()` processes `erase_complete_list`. In the ordinary path it allocates a page-sized buffer and scans the newly erased block. Read failure, short read, or a word not equal to all ones routes the block to the bad path.

However, if allocation of the temporary verification page fails, the code explicitly logs that it is **assuming the erase worked** and proceeds.

That detail is important because it prevents an overclaim such as:

> “Linux 2.4.10 JFFS2 always performed a successful full readback verification before every cleanmarker.”

It did not, according to this source snapshot.

The safe relation is instead:

```text
MTD_ERASE_DONE
    -> verification attempted when buffer allocation succeeds
    -> verification may reject the block
    -> verification may be skipped on allocation failure
```

Thus `all-0xFF readback verified` is neither identical to `MTD_ERASE_DONE` nor an unconditional historical prerequisite for all free-list transitions in this exact implementation.

### H6 — cleanmarker write remains a distinct admission step

After the successful/assumed erase state reaches the marker-writing path, JFFS2 writes the `JFFS2_NODETYPE_CLEANMARKER` to the start of the block in this NOR-era implementation.

A marker write error or short write routes to the bad path. Only after the marker is successfully written does the code:

- create the marker's raw-node reference;
- account marker bytes as used;
- account the rest of the erase block as free;
- move the block to `free_list`;
- increment `nr_free_blocks`.

Therefore the strongest code-level sequence supported here is:

```text
logically erasable
    -> erase pending
    -> erase request active
    -> MTD reports erase done
    -> erase complete staging
    -> optional readback qualification
    -> cleanmarker write succeeds
    -> free-list admission
```

The sequence has failure/retry exits at multiple stages.

---

## Engineering reconstruction

The repository can now distinguish at least six meanings of “the block is gone/empty/free” in this bounded implementation:

1. **no longer logically current** — one or more old nodes are obsolete;
2. **whole-block GC retirement complete** — no `used_size` remains, so the block becomes erase-eligible;
3. **maintenance queued** — the block is on `erase_pending_list`;
4. **erase active / lower-layer operation accepted** — it has moved through `erasing_list` and an MTD erase is in flight;
5. **lower-layer completion reported** — `MTD_ERASE_DONE` moved it to `erase_complete_list`;
6. **filesystem reuse admitted** — marker write/accounting complete and the block is on `free_list`.

The bounded relation is:

```text
logical obsolescence
    != block erase eligibility
    != erase queued
    != erase active
    != lower-layer erase completion
    != successful readback qualification
    != cleanmarker persistence attempt
    != free-list admission
```

Some adjacent stages may collapse on a particular execution path, and readback can be skipped on verification-buffer allocation failure. The point is not that every stage is always independently durable; the point is that the 2001 implementation does not treat them as one semantic event.

### Runtime workflow state versus retained restart evidence

`erase_pending_list`, `erasing_list`, and `erase_complete_list` are in-core workflow classifications. The `CLEANMARKER` is on-flash evidence intended to survive restart and qualify an erased block.

So:

```text
runtime maintenance phase
    !=
retained on-flash reuse witness
```

This is exactly why the case should not use a generic word such as “state” without naming the carrier and failure horizon.

### Retry obligation versus reusable capacity

The transient immediate-failure path gives another useful distinction:

```text
still needs erase
    + temporary inability to start erase
    -> erase_pending retained
    != free space
```

The system preserves the maintenance obligation rather than treating a failed attempt as evidence of completion.

### Failure quarantine versus successful retirement

Harder failure paths move the erase block to `bad_list`. In this source snapshot that is runtime filesystem bookkeeping. It should not be promoted into a claim about a NAND factory bad-block marker, persistent bad-block table, or universal MTD bad-block semantics.

Safe formulation:

```text
failed reclamation path
    -> capacity excluded from ordinary free-list reuse in the running instance
```

not:

```text
failed reclamation path
    -> universally persisted physical bad-block identity
```

---

## Functional comparison

### Case 150 — managed-SSD garbage collection

Both Case 145 and Case 150 separate logical invalidation from later physical reclamation. The difference is locus and observability:

- JFFS2's 2001 raw-Flash path exposes filesystem-level eraseblock lists, MTD completion, marker writing, and allocator admission in software;
- a managed SSD can hide relocation/reclamation behind controller firmware and the block interface.

This is a relation-level comparison only. It does not claim JFFS2 and SSD FTL garbage collectors share code, genealogy, or failure semantics.

### Case 78 — NAND bad-block retirement

Both cases can exclude physical capacity from reuse, but the authority differs. Case 145's 2001 `bad_list` path is runtime JFFS2 handling for failed erase/qualification in the inspected code. Case 78 concerns device/media bad-block identity and management. They must not be collapsed merely because both involve unusable erase blocks.

### Case 44 — sanitize

The JFFS2 pipeline is a reclamation-and-reuse pipeline. It provides no interface-level promise that retired user data are forensically unrecoverable, no purge taxonomy, and no sanitize completion contract.

Therefore:

```text
free_list admission
    != secure erase certification
    != sanitize completion
```

### Case 136 — repair-priority policy

There is a narrow formal analogy only: a maintenance obligation can remain pending while the substrate is not yet back in normal service. Case 136 is about repair scheduling and redundancy restoration; Case 145 is about raw-Flash reclamation. No genealogy or common scheduler is implied.

---

## Philosophical interpretation — bounded

This implementation supports one modest interpretive claim:

> **A transition can be physically underway, lower-layer complete, or even apparently successful without yet counting as admitted for reuse at the layer that owns currentness.**

The important object is therefore not just the substrate's apparent bit pattern. It is the relation among:

- what the filesystem has retired;
- which maintenance obligation remains;
- what the lower layer reports;
- what qualification was performed or skipped;
- what retained witness was written;
- what the allocator is now allowed to reuse.

This is not a general theory of trust, absence, or memory. It is a bounded interpretation of an explicit 2001 filesystem state machine.

---

## Explicit non-claims

This evidence does **not** establish that:

1. JFFS2 invented Flash garbage collection.
2. Linux 2.4.10 is the first implementation containing this pipeline.
3. the FUNET mirror is an origin-hosted kernel source artifact.
4. `used_size == 0` proves the underlying cells are erased.
5. `erase_pending_list` is durable across reset.
6. `erasing_list` is durable across reset.
7. `erase_complete_list` is durable across reset.
8. every MTD driver gave identical physical meaning to `MTD_ERASE_DONE`.
9. `MTD_ERASE_DONE` is a hardware power-fail durability certificate.
10. JFFS2 always performs full readback verification after erase.
11. an all-`0xFF` verification pass proves every cell is stable under every later condition.
12. a `CLEANMARKER` cryptographically proves the physical state of the whole block.
13. successful `CLEANMARKER` write is equivalent to secure sanitization.
14. a block placed on `bad_list` has a persistent NAND bad-block marker.
15. the 2001 NOR-oriented marker placement is identical to later NAND/OOB placement.
16. freeing in-core raw-node references erases physical stale node bytes.
17. `free_list` admission means no remanent physical information exists.
18. the inspected code is a formal proof of crash consistency.
19. every interruption point in the pipeline has been fault-injection tested here.
20. later JFFS2 releases preserve every detail of this exact state machine.

---

## Claim ledger

| Claim | Evidence | Class | Safe strength |
|---|---|---|---|
| GC queues a block for erase after `used_size` reaches zero | P1 | Historical record | direct period source witness |
| erase-pending and active erase are distinct runtime states | P2 | Historical record | direct period source witness |
| transient erase-start failure can requeue work | P2 | Historical record | direct period source witness |
| non-transient/improper completion can route capacity to `bad_list` | P2 | Historical record | direct period source witness |
| `MTD_ERASE_DONE` leads to `erase_complete_list`, not immediately `free_list` | P2 | Historical record | direct period source witness |
| readback can reject a supposedly erased block | P2 | Historical record | direct period source witness |
| readback is skipped when its temporary buffer allocation fails | P2 | Historical record | direct period source witness; prevents stronger universal claim |
| cleanmarker write failure prevents free-list admission | P2 | Historical record | direct period source witness |
| successful marker path precedes `free_list` insertion | P2 | Historical record | direct period source witness |
| runtime erase-list state is not the same carrier as the on-flash cleanmarker | P2 + P4 | Engineering reconstruction | strongly supported bounded distinction |
| reuse admission is not sanitization | P1–P4 plus absence of sanitize contract | Engineering reconstruction | strong negative boundary |
| every stage survives power loss exactly as listed | unsupported | — | explicitly rejected |

---

## Prior-art and genealogy boundary

This deepening does not change Case 145's priority posture. JFFS2 is treated as a directly inspectable 2001 implementation instance, not as the invention point for log-structured reclamation, Flash garbage collection, erase verification, negative state, or tombstone-like semantics.

A fresh search of `tmzncty/computing-archaeology` found no dedicated JFFS2 packet. The broader JFFS/JFFS2/LFS/YAFFS/UBIFS genealogy, MTD subsystem history, vendor Flash behavior, and exact CVS ancestry should remain companion-repository work. This file keeps only the retention-specific seam:

```text
logical retirement
    -> maintenance eligibility
    -> maintenance execution
    -> lower-layer completion
    -> qualification / retained witness
    -> reuse admission
```

---

## Remaining evidence debt

1. Recover origin-hosted Linux-MTD CVS commits or cryptographically matched source artifacts for the exact introduction of this erase state machine.
2. Recover the exact 2001 `scan.c` path that reconstructs clean/free/erase-pending classification on mount and bind it directly to crash-window analysis.
3. Fault-inject power loss at `erase_pending`, active erase, `MTD_ERASE_DONE`, readback, cleanmarker write, and free-list transition boundaries.
4. Test named raw-Flash devices to distinguish filesystem policy from device-specific interrupted-erase physics.
5. Trace later NAND/OOB changes separately; do not project the 2001 NOR-era marker path into 2004–2007 NAND behavior.
6. Keep managed-SSD/FTL GC and sanitize guarantees in their dedicated cases.

The bounded source-level claim is complete without closing those larger questions.
