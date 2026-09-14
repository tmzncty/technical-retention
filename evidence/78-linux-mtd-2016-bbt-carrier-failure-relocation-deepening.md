# Case 78 Deepening — Linux MTD BBT Carrier-Failure Relocation (2016)

## Status

**bounded deepening complete**

## Scope

This addendum deepens [`Case 78`](../cases/78-micron-nand-bad-block-marker-management.md) at a narrow boundary left open by the earlier mirrored/versioned-BBT studies: **what happens when the NAND eraseblock that is supposed to carry the bad-block table itself fails during a BBT update?**

The bounded historical witnesses are:

- released Linux v4.8, where an erase/write failure while writing a BBT carrier aborts the BBT write path;
- Kyle Roeschley's 2015–2016 linux-mtd patch series and the associated maintainer discussion;
- upstream commit `10ffd570f11701972aff2a6f91f3d253d6f0e7ee`, committed 23 September 2016;
- released Linux v4.9, whose source contains the resulting carrier-retirement-and-retry mechanism.

This is not a general history of Linux MTD, not evidence about a proprietary SSD controller, not an invention-priority claim for metadata relocation, and not a power-cut fault-injection experiment. The retention-specific question is smaller:

> When the retained control state that says which NAND blocks may be used is itself stored on a block that becomes unusable, can the control state change physical embodiment without abandoning the update?

---

## Historical vocabulary

The inspected Linux sources use terms including:

- `bad block table` / `BBT`;
- `BBT block`;
- `bad block marker`;
- `worn` / `factory marked bad`;
- `mirror bad block table`;
- `version`;
- `No space left to write bad block table`.

The following are project engineering terms, not quotations from the Linux sources:

- `control-metadata carrier`;
- `carrier retirement`;
- `control-state re-embodiment`;
- `continuation reserve`;
- `metadata-carrier exhaustion`.

---

## Historical record

### H/P — Linux v4.8 aborted a BBT write when the chosen BBT block could not be erased or written

Released Linux v4.8 selects either the previously recorded BBT page or an automatically placed candidate in the configured BBT search region. Once that target is chosen, `write_bbt()` erases the target eraseblock and writes the table image.

In the v4.8 source, both of these failures terminate the operation:

```c
res = nand_erase_nand(mtd, &einfo, 1);
if (res < 0)
        goto outerr;

res = scan_write_bbt(...);
if (res < 0)
        goto outerr;
```

The common error path reports `error while writing bad block table` and returns the error. The function does not, in this released version, retire that failed BBT carrier and continue searching another candidate for the same update.

This does **not** mean Linux v4.8 lacked ordinary NAND bad-block handling. The bounded claim concerns only this BBT-write failure path: a failure of the block selected to carry the BBT ended this attempt instead of automatically relocating the BBT write to another reserved candidate.

**Primary released source:** Linux v4.8, `drivers/mtd/nand/nand_bbt.c`: <https://github.com/torvalds/linux/blob/v4.8/drivers/mtd/nand/nand_bbt.c>.

### H/P — the 2016 upstream change states the new policy explicitly

Upstream commit `10ffd570f11701972aff2a6f91f3d253d6f0e7ee`, authored by Kyle Roeschley and committed by Boris Brezillon on 23 September 2016, is titled:

> `mtd: nand_bbt: scan for next free bbt block if writing bbt fails`

Its commit message states the intended behavior directly: if erasing or writing the BBT fails, the current BBT block should be marked bad and the BBT descriptor should be used to find the next unused block; failure should be returned only when no space remains for that retry path.

The patch adds `mark_bbt_block_bad()`. For the failed BBT carrier it:

1. records the block as `BBT_BLOCK_WORN` in the in-memory BBT;
2. invokes the NAND bad-block-marking operation for that physical block;
3. invalidates `td->pages[chip]` by setting it to `-1` so the descriptor no longer points at the failed carrier.

The write loop is changed from a simple per-chip `for` progression to a retry-capable `while`. An erase failure or a BBT write failure now calls `mark_bbt_block_bad(...)` and `continue`s, causing target selection to run again rather than immediately returning the first media error.

**Primary upstream source:** Linux commit `10ffd570f11701972aff2a6f91f3d253d6f0e7ee`: <https://github.com/torvalds/linux/commit/10ffd570f11701972aff2a6f91f3d253d6f0e7ee>.

### H/P — Linux v4.9 contains the carrier-retirement-and-retry behavior in a released tree

Linux v4.9, released 11 December 2016, contains the new implementation. Its `get_bbt_block()` walks the bounded BBT placement range and skips blocks already classified `BBT_BLOCK_WORN` or `BBT_BLOCK_FACTORY_BAD`; it also avoids selecting the page occupied by the mirror BBT.

In `write_bbt()`:

```text
select BBT carrier
    -> erase carrier
       -> failure: mark carrier bad, invalidate descriptor page, retry
    -> write BBT image
       -> failure: mark carrier bad, invalidate descriptor page, retry
    -> success: record td->pages[chip] = new page
```

If candidate selection cannot find another acceptable block, `get_bbt_block()` returns `-ENOSPC` and the write path reports `No space left to write bad block table`.

This is a concrete released implementation of **control-state relocation after failure of the control state's own physical carrier**.

**Primary released source:** Linux v4.9, `drivers/mtd/nand/nand_bbt.c`: <https://github.com/torvalds/linux/blob/v4.9/drivers/mtd/nand/nand_bbt.c>.

**Release anchor:** kernel.org v4.x archive, `linux-4.9.tar.*`, 11 December 2016: <https://www.kernel.org/pub/linux/kernel/v4.x/>.

### H/P — the default BBT placement reserve is finite

In Linux v4.9, the generic primary and mirror descriptors use:

```c
.maxblocks = NAND_BBT_SCAN_MAXBLOCKS
```

and the corresponding header defines:

```c
#define NAND_BBT_SCAN_MAXBLOCKS 4
```

This does not mean every custom BBT descriptor has exactly four possible carrier blocks. It does establish a concrete default implementation in which the space searched for BBT placement is deliberately bounded.

The retention consequence is therefore conditional and finite:

> failed BBT carrier -> try another eligible carrier **while the configured candidate reserve still contains one**.

**Primary released sources:** Linux v4.9, `drivers/mtd/nand/nand_bbt.c` and `include/linux/mtd/bbm.h`.

### H/P — the patch discussion explicitly noticed an interruption boundary

The linux-mtd review thread is useful because it records a concern that the final source alone does not narrate. During review, Boris Brezillon questioned the ordering in which the failing BBT carrier is marked bad before a new BBT has successfully been written. He noted that if the replacement BBT write is then interrupted, the next recovery can fall back to a full bad-block-marker scan; he also cautioned that this is not harmless for every platform, especially where bad-block-marker area usage differs.

The safe use of this discussion is narrow:

- the developers themselves recognized that `retire old carrier -> successfully materialize replacement BBT` was not being presented as one indivisible transactional step;
- a recovery path may have to reconstruct exclusion knowledge from lower-level bad-block markers if the replacement write does not complete;
- platform-specific bad-block-marker conventions matter.

This is **not** evidence that a particular production system lost its BBT during a power failure, and the review discussion is not a substitute for fault-injection data.

**Primary development discussion:** linux-mtd, `[PATCH v3] mtd: nand_bbt: scan for next free bbt block if writing bbt fails`, April 2016: <https://lists.infradead.org/pipermail/linux-mtd/2016-April/067340.html>.

---

## Engineering reconstruction

### E — the BBT carrier is replaceable even though the exclusion relation must persist

Case 78 already established that the BBT is retained control state: it determines which physical NAND blocks are excluded from ordinary use. The 2016 change adds a second level of indirection:

```text
bad-block exclusion relation
    -> BBT image + version
    -> one physical BBT carrier block
    -> carrier erase/write failure
    -> carrier becomes excluded too
    -> BBT image is attempted on another eligible carrier
```

Therefore:

> `persistence of exclusion authority` != `persistence of one BBT eraseblock`.

The physical block holding the rule of non-use can itself become a target of the rule of non-use.

### E — BBT metadata is subject to the same broad media-failure problem it manages

The BBT exists because NAND blocks can become unreliable. The 2016 code makes explicit that a BBT-reserved block is not exempt from that failure regime.

This is recursive only in a bounded engineering sense:

```text
BBT classifies blocks
    AND
BBT carrier is itself a block that may become bad
```

The implementation breaks the recursion operationally by using lower-level bad-block marking plus a finite reserved placement search to find a new carrier.

It does **not** imply an infinite hierarchy of BBTs describing BBTs.

### E — retirement of the failed carrier is different from successful preservation of the replacement

The retry logic performs several distinct state transitions:

1. detect erase/write failure;
2. classify the current BBT carrier as worn/bad;
3. invalidate the descriptor's old page pointer;
4. search another candidate;
5. erase/write the BBT image there;
6. only on success record the new page as the current BBT location.

Therefore:

> `old BBT carrier retired` != `replacement BBT durable`.

The review discussion makes this distinction historically visible by considering interruption between these stages.

### E — metadata-carrier reserve is retention infrastructure

The bounded search region is not merely `unused space`. It provides alternative physical embodiments for the BBT when a previous carrier becomes unusable.

For the generic v4.9 descriptors, `NAND_BBT_SCAN_MAXBLOCKS = 4` supplies a concrete default bound on that search. Custom descriptors can differ, so the number is not generalized into a NAND law.

The stronger cross-case relation is:

> `available replacement carriers` are a continuation resource for retained control state.

This is closely related to the reserved replacement capacity already documented for ordinary bad-block replacement in Case 78, but the object being re-embodied here is the **qualification map itself**, not user payload.

### E — relocation is not the same thing as crash atomicity

The 2016 retry mechanism improves tolerance of a carrier that fails during the BBT write operation. It does not establish a transaction that makes every interruption point equivalent to either the old complete state or the new complete state.

The sources do not prove:

- power-cut atomicity between bad-marking the failed carrier and writing its replacement;
- survival if every eligible BBT carrier is bad;
- survival if both mirrored table paths become unusable together;
- correct recovery on platforms whose bad-block markers cannot be reconstructed by the assumed scan;
- that marking a carrier bad always succeeds after the original erase/write failure;
- that a successful `write_bbt()` return is an end-to-end power-loss qualification.

Thus:

> `carrier-failure retry` != `transactional BBT update`.

### E — the new failure boundary is exhaustion, not immortality

The change converts one class of immediate media error into a relocation attempt. It does not eliminate the physical failure boundary; it moves it.

A simplified bounded chain is:

```text
one carrier fails
    -> retire it
    -> try another candidate

candidate reserve exhausted
    -> -ENOSPC / BBT update cannot continue through this mechanism
```

So the 2016 change is best described as **failure-tolerant continuation while admissible replacement capacity remains**, not as indefinite self-healing.

---

## Functional comparisons — not genealogy

### A — Case 04, mapped Flash payload relocation

Both mechanisms let a logical relation survive a physical-location change, but the retained objects differ:

- Case 04 relocates current payload embodiments under Flash rewrite/reclamation geometry;
- this Case-78 deepening relocates the BBT representation that carries **negative media-qualification authority**.

Therefore:

> `payload relocation` ≈ `control-metadata relocation` only at the function `preserve a relation while replacing its physical carrier`.

No common algorithm or genealogy is claimed.

### A — Case 39, mapping-metadata recovery

Both cases make non-payload Flash metadata constitutive of later safe service. Case 39 asks how positive logical-to-physical resolution state is reconstructed; Case 78 asks how negative block-admissibility state survives and how its own carrier may be replaced.

`mapping authority` != `exclusion authority`.

### A — Case 100, ZFS DTL persistence

Case 100 shows a different control-state regime in which a durable repair-debt basis is persisted and runtime views can be reconstructed from it. The Linux BBT here instead moves a durable control image away from a failed NAND carrier.

The only intended analogy is:

> non-payload maintenance/control state can have its own persistence mechanism and its own failure boundary.

This is not implementation genealogy.

---

## Philosophical interpretation — bounded

### I — preservation can require replacement of the thing that carries the rule of preservation

The modest interpretive point is not that the system literally `remembers how to remember`. The technical statement is narrower: the rule that excludes unreliable carriers is itself materially embodied, and that embodiment can fail.

Continuation therefore depends on preserving the **relation** while permitting replacement of its carrier.

The case also blocks a simple equation between durability and immobility:

> a retained control relation can become more durable precisely because its implementation permits the physical location that carries it to be abandoned.

No stronger philosophical claim follows from the source record.

---

## Explicit non-claims

This slice does **not** claim that:

1. Linux invented bad-block tables;
2. Linux invented metadata relocation;
3. Linux v4.8 could never recover from a BBT write failure by any higher-level intervention;
4. every NAND implementation uses the Linux generic BBT descriptors;
5. every BBT has exactly four candidate blocks;
6. every erase/write error proves permanent physical wear;
7. the 2016 change is a database-style transaction;
8. primary and mirror writes become atomic with each other;
9. a successful carrier retry proves power-cut safety;
10. a failed BBT carrier implies user payload corruption;
11. the BBT contains complete bad-block event history;
12. a managed SSD exposes or internally copies this Linux design;
13. BBT relocation is the same mechanism as FTL garbage collection;
14. bad-block-marker reconstruction works identically on every platform;
15. the mailing-list interruption discussion is a production incident report.

---

## Prior-art boundary

No invention-priority claim is made.

The defensible chronology is narrower:

> Released Linux v4.8 still aborted the inspected BBT write path when the selected BBT eraseblock could not be erased or written. Upstream commit `10ffd570` in September 2016 changed that path so a failed BBT carrier is marked bad and another eligible BBT block is sought; released Linux v4.9 contains that behavior. The associated review discussion also records that the carrier-retirement/replacement sequence should not be confused with an indivisible crash-atomic handoff.

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `NAND bad block table`, `BBT`, and `nand_bbt` found no dedicated companion history to reuse. Broader NAND/MTD/bootloader/controller genealogy still belongs there rather than being recreated here.

---

## Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| Linux v4.8 returned from the BBT write path when target erase or write failed | H/P | grounded in released v4.8 source |
| 2016 upstream commit `10ffd570` changes erase/write failure into bad-mark + next-candidate retry | H/P | grounded in upstream commit and diff |
| failed BBT carrier is marked `BBT_BLOCK_WORN`, physically bad-marked, and its descriptor page invalidated | H/P | grounded in upstream commit |
| Linux v4.9 contains the retrying implementation | H/P | grounded in released v4.9 source |
| generic v4.9 BBT descriptors use a four-block maximum scan range | H/P | grounded in released source/header; not generalized to custom descriptors |
| BBT control state can change physical carrier after carrier failure | E | bounded reconstruction from released implementation |
| BBT carrier retirement != successful replacement durability | E | bounded reconstruction; interruption concern appears in review discussion |
| replacement-carrier capacity is continuation infrastructure | E | bounded reconstruction |
| carrier retry != crash-atomic BBT update | E/X | explicit boundary; no power-cut experiment supplied |
| same relocation function implies same mechanism as FTL payload relocation | X/A | rejected; analogy only |
| this proves proprietary SSD-controller BBT internals | X | unsupported |

---

## Sources

### Primary / contemporary

1. Linux v4.8, `drivers/mtd/nand/nand_bbt.c`: <https://github.com/torvalds/linux/blob/v4.8/drivers/mtd/nand/nand_bbt.c>.
2. Kyle Roeschley / Boris Brezillon, Linux upstream commit `10ffd570f11701972aff2a6f91f3d253d6f0e7ee`, `mtd: nand_bbt: scan for next free bbt block if writing bbt fails`, 23 September 2016: <https://github.com/torvalds/linux/commit/10ffd570f11701972aff2a6f91f3d253d6f0e7ee>.
3. linux-mtd discussion, `[PATCH v3] mtd: nand_bbt: scan for next free bbt block if writing bbt fails`, April 2016: <https://lists.infradead.org/pipermail/linux-mtd/2016-April/067340.html>.
4. Linux v4.9, `drivers/mtd/nand/nand_bbt.c`: <https://github.com/torvalds/linux/blob/v4.9/drivers/mtd/nand/nand_bbt.c>.
5. Linux v4.9, `include/linux/mtd/bbm.h`, `NAND_BBT_SCAN_MAXBLOCKS`: <https://github.com/torvalds/linux/blob/v4.9/include/linux/mtd/bbm.h>.
6. kernel.org v4.x release archive, Linux 4.9 dated 11 December 2016: <https://www.kernel.org/pub/linux/kernel/v4.x/>.

### Related Case-78 evidence

- [`78-linux-mtd-2004-mirrored-versioned-bbt-deepening.md`](78-linux-mtd-2004-mirrored-versioned-bbt-deepening.md) — primary/mirror BBT persistence and version reconciliation.
- [`78-linux-mtd-2004-2021-bbt-currentness-admissibility-deepening.md`](78-linux-mtd-2004-2021-bbt-currentness-admissibility-deepening.md) — cyclic currentness arithmetic, ECC-invalid newer candidates, and bad BBT-host admissibility.
- [`78-kioxia-2018-2019-soft-error-vs-bad-block-retirement-deepening.md`](78-kioxia-2018-2019-soft-error-vs-bad-block-retirement-deepening.md) — maintenance-eligible errors versus permanent block retirement.

### Related repository

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — broad NAND/MTD/bootloader/controller history belongs there; this addendum keeps only the retention-specific carrier-failure relocation boundary.
