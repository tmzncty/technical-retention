# Case 78 Deepening — Linux MTD v3.3 Dual-BBT Serial Publication and Cut-Point Asymmetry

Canonical case: [`../cases/78-micron-nand-bad-block-marker-management.md`](../cases/78-micron-nand-bad-block-marker-management.md)

**Evidence maturity contribution:** `grounded` source-level deepening; no case maturity promotion.

## Research question

Case 78 already establishes that Linux MTD can retain a flash bad-block table (BBT) as a mirrored, versioned control structure, and that later Linux work deliberately orders a grown-bad-block OOB marker before the flash-BBT update to improve the power-cut boundary.

This packet asks a narrower question left open by those results:

> When a mirrored flash BBT is updated, are the two persistent copies published as one atomic event, or are they rewritten serially such that a crash/failure can leave a newer primary beside an older, missing, erased, or otherwise incomplete mirror?

The bounded source snapshot is Linux `v3.3`, `drivers/mtd/nand/nand_bbt.c`.

The answer in this implementation is clear at source level: **the two copies are updated serially, primary first and mirror second, and each individual copy is itself rewritten through an erase-then-write sequence.** The recovery path explicitly understands missing and unequal-version copies and can schedule repair from the usable/current peer.

That is not a physical power-cut experiment. It is a source-level cut-point analysis of the software publication order and the recovery states the implementation admits.

---

## Claim discipline

This packet keeps four layers separate.

### Historical / source record

Statements directly established by the inspected Linux source:

- `nand_update_bbt()` increments primary and mirror version state in memory;
- the primary BBT is passed to `write_bbt()` first;
- a primary-write error returns before the mirror rewrite is attempted;
- the mirror rewrite is attempted only after the primary write succeeds;
- `write_bbt()` erases the selected BBT eraseblock and then writes the new table image;
- `check_create()` has explicit cases for one missing copy and for unequal versions, selecting a surviving/current table and scheduling the peer for rewrite.

### Engineering reconstruction

Derived control relations such as:

- `two retained copies != atomic two-copy publication`;
- `same version assigned in RAM != same version durably published to both copies`;
- `new primary present != mirror convergence complete`;
- `replica disagreement != maintenance obligation completed`.

The phrase **serially replicated maintenance metadata** is project vocabulary, not Linux historical terminology.

### Functional analogy

Comparison to other cases is limited to control shape: staged publication, surviving representation, and later repair. It is not a claim of implementation ancestry.

### Philosophical interpretation

Any interpretive language about continuity or retained authority is kept downstream of the implementation facts and is not attributed to Linux developers.

---

## Historical / source record

### H/P — `nand_update_bbt()` advances both in-memory versions before either persistent copy is rewritten

In Linux `v3.3`, `nand_update_bbt()` obtains the primary descriptor `td` and optional mirror descriptor `md`, then advances the per-chip version state:

```c
td->version[chip]++;
if (md)
        md->version[chip]++;
```

Only after that does it begin persistent publication.

This gives an immediate boundary:

```text
primary.version == mirror.version in RAM
    !=
primary and mirror already contain that version on NAND
```

The equalized in-memory version is an intended target for this update episode, not proof that both persistent embodiments have reached it.

**Primary source:** Linux `v3.3`, `drivers/mtd/nand/nand_bbt.c`, `nand_update_bbt()`: <https://github.com/torvalds/linux/blob/v3.3/drivers/mtd/nand/nand_bbt.c>.

### H/P — persistent publication is ordered: primary first, mirror second

The same function then writes the primary descriptor first:

```c
if (td->options & NAND_BBT_WRITE) {
        res = write_bbt(mtd, buf, td, md, chipsel);
        if (res < 0)
                goto out;
}
```

Only after a successful primary call does it attempt the mirror:

```c
if (md && (md->options & NAND_BBT_WRITE))
        res = write_bbt(mtd, buf, md, td, chipsel);
```

The early exit on primary failure matters. An update attempt can fail while leaving the mirror deliberately untouched by that attempt.

The implementation therefore does not present the two BBT copies as a single atomic write primitive.

### H/P — one BBT-copy rewrite is itself an erase-then-write sequence

Inside `write_bbt()`, after choosing a BBT-host block and constructing the serialized table image, Linux issues an erase of the target eraseblock:

```c
res = nand_erase_nand(mtd, &einfo, 1);
if (res < 0)
        goto outerr;
```

and only after a successful erase calls the BBT write path:

```c
res = scan_write_bbt(mtd, to, len, buf,
        td->options & NAND_BBT_NO_OOB ? NULL : &buf[len]);
if (res < 0)
        goto outerr;
```

It then reports the BBT location/version and records the page used by that descriptor.

So even before considering two replicas, a single-copy refresh has at least this source-visible structure:

```text
old BBT embodiment
    -> erase selected BBT carrier
    -> program serialized new BBT image
    -> record successful placement in runtime descriptor
```

Nothing in this sequence is a software-level atomic replacement of the entire eraseblock.

**Primary source:** Linux `v3.3`, `drivers/mtd/nand/nand_bbt.c`, `write_bbt()`: <https://github.com/torvalds/linux/blob/v3.3/drivers/mtd/nand/nand_bbt.c>.

### H/P — startup/reconciliation explicitly admits missing and unequal copies

The `check_create()` path documents its own purpose as creating or updating BBTs when one is missing or one version is less than the other.

For mirrored tables it distinguishes, among other cases:

```text
primary missing + mirror missing
    -> create and write both

primary missing + mirror present
    -> read mirror
    -> schedule primary rewrite

primary present + mirror missing
    -> read primary
    -> schedule mirror rewrite

both present + equal versions
    -> use primary

both present + unequal versions
    -> choose the newer one under the implementation's version rule
    -> schedule the other copy for rewrite
```

The writeback is again ordered primary-side operation before mirror-side operation where both are requested, with errors returned immediately.

This is direct evidence that **asymmetric replica state is an expected recovery condition**, not an impossible state excluded by the design.

**Primary source:** Linux `v3.3`, `drivers/mtd/nand/nand_bbt.c`, `check_create()`: <https://github.com/torvalds/linux/blob/v3.3/drivers/mtd/nand/nand_bbt.c>.

### H/P — currentness selection is not version magnitude alone

Case 78 already has a separate packet for the details omitted here: version-wrap ordering, ECC-invalid newer candidates, and bad BBT-host blocks all constrain which surviving table is actually admissible as authority.

See [`78-linux-mtd-2004-2021-bbt-currentness-admissibility-deepening.md`](78-linux-mtd-2004-2021-bbt-currentness-admissibility-deepening.md).

This packet therefore uses `newer` only as shorthand for **the copy selected by the implementation's admissibility/currentness rules**, not simply the numerically larger byte.

---

## Cut-point reconstruction

The following matrix is a bounded engineering reconstruction from the source ordering. It does **not** claim that each row has been reproduced with a physical power-cut rig.

| Cut point | Primary BBT | Mirror BBT | Bounded consequence |
| --- | --- | --- | --- |
| before persistent rewrite begins | old | old | no new flash-BBT publication yet |
| primary erase has begun / primary new image not successfully written | erased, incomplete, old, or otherwise not proven current depending on physical outcome | old | mirror remains the untouched older persistent peer for this attempt |
| primary write succeeds, before mirror erase | new | old | versions/payloads may legitimately diverge |
| mirror erase has begun, mirror new image not successfully written | new | erased, incomplete, old, or otherwise not proven current | primary can remain the current surviving peer |
| mirror write succeeds | new | new | intended replica convergence reached |

The table deliberately says `may` around physical media outcomes. Source order establishes which operation was requested and when the second replica is touched; it does not establish exact NAND charge state after arbitrary power removal.

### E — two persistent copies do not imply a two-copy atomic transaction

The strongest bounded statement is:

```text
mirrored metadata
    != atomic replicated commit
```

Linux obtains resilience by allowing one copy to survive and by retaining enough currentness/admissibility information to choose and repair a peer. It does not make the two erase/program sequences one indivisible persistence event.

### E — same target version is not the same thing as synchronized persistence

Because primary and mirror versions are advanced in memory before the first persistent write, the relation is:

```text
same intended version
    != same published version
    != same durable payload
```

The version field helps interpret surviving copies after divergence; it does not prevent divergence from occurring.

### E — convergence is a maintenance outcome, not a prerequisite for every usable state

The recovery path can use one table while arranging to rewrite the missing/stale peer. Therefore:

```text
one admissible current BBT survives
    + repair rule survives
    -> mirrored state can be reconstructed
```

without requiring the previous update episode itself to resume from a saved program counter.

This is a form of **reconstructive maintenance** in project terminology: the next operating interval can infer remaining replica-repair work from surviving persistent state.

---

## Relation to grown-bad-block markers

The separate 2012 Case-78 packet establishes another ordering layer: later Linux work deliberately put the per-block OOB bad-block marker before the flash-BBT update in the grown-bad-block path.

See [`78-linux-mtd-2012-bbm-bbt-power-cut-ordering-deepening.md`](78-linux-mtd-2012-bbm-bbt-power-cut-ordering-deepening.md).

Taken together, the source-level control chain can be represented as:

```text
new bad block recognized
    -> lower-level bad-block marker attempted/published
    -> RAM BBT state changed
    -> flash-BBT update requested
        -> primary BBT erase/write
        -> mirror BBT erase/write
```

This reveals multiple persistence horizons for one exclusion relation.

### E — lower-level exclusion evidence can outlive an incomplete summary update

Where the OOB marker write has actually succeeded before flash-BBT publication, a later interruption can leave the higher-level BBT copies stale or asymmetric while a lower-level per-block exclusion witness already exists.

That supports the bounded relation:

```text
summary metadata not converged
    != all exclusion evidence absent
```

But this is not a universal guarantee. It depends on the marker write having succeeded and on the later scan/recovery policy actually consulting the relevant representation.

### E — retained evidence and retained summary are different obligations

The per-block marker and flash BBT serve related but different roles:

```text
per-block marker
    = local negative media-qualification evidence

flash BBT
    = operational summary/control representation
```

Losing or delaying one representation therefore does not automatically have the same consequence as losing the other.

---

## Relation to BBT-carrier failure

Case 78 also has a later Linux packet showing that a block carrying the BBT can itself fail and, in later code, trigger relocation to another eligible BBT carrier.

See [`78-linux-mtd-2016-bbt-carrier-failure-relocation-deepening.md`](78-linux-mtd-2016-bbt-carrier-failure-relocation-deepening.md).

The present packet adds a different dimension:

```text
carrier replacement policy
    != replica publication atomicity
```

A system may know how to abandon a failed BBT-host block and still publish primary/mirror updates serially.

---

## Functional comparisons — not genealogy

### A — Case 04: Flash mapping/currentness publication

Case 04 repeatedly distinguishes establishment of a replacement/current representation from retirement of an older embodiment. Case 78 has a comparable control shape when a newer BBT copy exists while an older peer still remains.

The mechanisms are not the same. A Linux MTD BBT is negative media-qualification metadata, not an FTL logical-to-physical mapping transaction.

### A — Case 25: reconstructive retry

Case 25 shows a different system in which surviving state can allow a later maintenance pass to rediscover remaining work rather than preserving a volatile continuation object.

Case 78 is functionally comparable only at that abstraction level:

```text
volatile update episode lost
    != maintenance obligation lost
```

There is no claim of shared implementation lineage.

---

## Philosophical interpretation — bounded

The modest interpretive result is that redundancy can preserve continuity without preserving simultaneity.

A mirrored control structure can remain useful even though its copies do not cross every transition together. Continuity instead depends on enough surviving evidence to answer two questions later:

1. which surviving representation is admissible/current enough to use; and
2. which missing/stale representation still requires maintenance.

That is a statement about this mechanism's control structure, not a general theory that every redundant system behaves this way.

---

## Explicit non-claims

This packet does **not** establish that:

1. Linux MTD invented mirrored or versioned NAND BBTs.
2. Linux `v3.3` is the first version with this exact primary-then-mirror update order.
3. Every NAND platform enables flash-based mirrored BBTs.
4. Every BBT descriptor has a mirror.
5. Primary and mirror are always placed on physically independent failure domains.
6. A source-level return from `scan_write_bbt()` is equivalent to survival of arbitrary sudden power loss.
7. The NAND device, controller, power supply, cache, or board guarantees persistence at every cut point listed above.
8. A primary erase interrupted by power loss necessarily produces one particular physical bit pattern.
9. A mirror erase interrupted by power loss necessarily leaves the primary readable.
10. Both BBT copies can never be lost together.
11. The BBT version byte is a transaction log, audit history, checksum, or cryptographic authority token.
12. Equal in-memory versions prove equal persistent payloads.
13. Equal persistent versions prove identical valid payloads under every corruption pattern.
14. The numerically greater raw version byte is always newer; the separate currentness packet documents the bounded comparison rule and its validity constraints.
15. A surviving newer copy is automatically usable before ECC/media-admissibility checks.
16. A successful OOB bad-block-marker write is guaranteed in every grown-bad-block event.
17. A later boot always consults every possible lower-level marker under every board/configuration policy.
18. Marker-before-BBT ordering makes the whole bad-block-management update atomic.
19. Reconciliation reconstructs the exact sequence of interrupted historical updates.
20. BBT carrier relocation and BBT replica convergence are the same maintenance operation.
21. This raw-NAND implementation proves anything about proprietary SSD-controller metadata protocols.
22. The cut-point matrix is a physical fault-injection result.
23. Process reset, SoC reset, brownout, and abrupt battery removal are equivalent failure stimuli.
24. `reconstructive maintenance` or `serially replicated maintenance metadata` are upstream Linux terms.

---

## What this closes

This packet closes a specific source-level debt for Case 78:

> **Does mirrored/versioned Linux MTD BBT state imply atomic publication of both copies?**

For the inspected Linux `v3.3` implementation: **no**. The copies are updated serially; primary failure aborts before mirror rewrite; each copy is erased then written; and the recovery path explicitly handles missing/unequal copies.

It does **not** close the stronger physical-fault question.

---

## Highest-value remaining debts

1. **Exact fault injection across the serial update path.** Exercise cuts during primary erase/write, between copies, and during mirror erase/write, then record boot-time selection/healing.
2. **Marker + dual-BBT combined fault trace.** Demonstrate the full grown-bad sequence where the OOB marker succeeds but flash-BBT publication is interrupted at each replica boundary.
3. **Marker-write failure path.** Distinguish failure to publish the lower-level exclusion witness from failure to converge the summary BBT.
4. **BBT-carrier failure during replica update.** Combine the 2016 relocation mechanism with the serial-publication cut points.
5. **Configuration boundary.** Document which real boards/devices enable mirrored flash BBT, use OOB markers, suppress them, or rely on alternate bootloader/firmware policies.
6. **Physical persistence boundary.** Separate software return semantics from NAND-device power-loss guarantees using platform/device evidence or controlled tests.

---

## Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| `nand_update_bbt()` increments primary and mirror versions before persistent writes | H/P | grounded in Linux v3.3 source |
| primary BBT is written before mirror BBT | H/P | grounded in Linux v3.3 source |
| primary write error exits before mirror rewrite | H/P | grounded in Linux v3.3 source |
| each inspected BBT-copy rewrite performs erase before table write | H/P | grounded in `write_bbt()` |
| `check_create()` handles missing and unequal-version mirrored copies | H/P | grounded in Linux v3.3 source |
| mirrored BBT != atomic two-copy publication | E | direct bounded reconstruction from call order |
| equal in-memory target versions != equal durable publication | E | direct bounded reconstruction |
| asymmetric replica state can carry repair debt | E | grounded by reconciliation/writeback logic |
| successful OOB marker can preserve lower-level exclusion evidence while flash BBT is stale/asymmetric | E | bounded synthesis with existing 2012 marker-order packet |
| arbitrary power cut leaves a known exact NAND state at every listed cut point | X | not established |
| this mechanism proves managed-SSD metadata behavior | X | unsupported |

---

## Sources

### Primary source inspected in this packet

1. Linux `v3.3`, `drivers/mtd/nand/nand_bbt.c`, especially `write_bbt()`, `check_create()`, and `nand_update_bbt()`: <https://github.com/torvalds/linux/blob/v3.3/drivers/mtd/nand/nand_bbt.c>.

### Existing Case-78 evidence reused rather than duplicated

2. [`78-linux-mtd-2004-mirrored-versioned-bbt-deepening.md`](78-linux-mtd-2004-mirrored-versioned-bbt-deepening.md) — mirrored/versioned BBT grounding and bounded recovery semantics.
3. [`78-linux-mtd-2004-2021-bbt-currentness-admissibility-deepening.md`](78-linux-mtd-2004-2021-bbt-currentness-admissibility-deepening.md) — cyclic version ordering, ECC-invalid candidates, and BBT-carrier admissibility.
4. [`78-linux-mtd-2012-bbm-bbt-power-cut-ordering-deepening.md`](78-linux-mtd-2012-bbm-bbt-power-cut-ordering-deepening.md) — grown-bad OOB marker before flash-BBT update and the remaining power-cut caveats.
5. [`78-linux-mtd-2016-bbt-carrier-failure-relocation-deepening.md`](78-linux-mtd-2016-bbt-carrier-failure-relocation-deepening.md) — relocation when the BBT's own storage carrier fails.

### Related repository boundary

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `nand_update_bbt` and NAND bad-block-table material did not identify a dedicated reusable packet for this exact serial-publication cut point in this round. Broader NAND/BBT genealogy therefore remains outside this Case-78 deepening rather than being rebuilt here.

---

## Status

- Case: **78**
- Canonical case: [`../cases/78-micron-nand-bad-block-marker-management.md`](../cases/78-micron-nand-bad-block-marker-management.md)
- Repository maturity: **`grounded`**
- Maturity promotion: **none**
- Source layer added: **Linux v3.3 source-level dual-copy publication ordering and reconciliation cut points**
- Last updated: **2026-09-24**
