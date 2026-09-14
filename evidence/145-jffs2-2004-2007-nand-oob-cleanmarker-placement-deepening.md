# Evidence 145 — JFFS2 2004–2007 NAND OOB cleanmarker placement and conservative requalification

## Status

**`bounded deepening complete`**

## Navigation

- Canonical case: [`cases/145-jffs2-garbage-collection-negative-state-evidence.md`](../cases/145-jffs2-garbage-collection-negative-state-evidence.md)
- 2001 grounding: [`145-jffs2-2001-garbage-collection-negative-state-grounding.md`](145-jffs2-2001-garbage-collection-negative-state-grounding.md)
- Related bad-block retirement boundary: [`../cases/78-micron-nand-bad-block-marker-management.md`](../cases/78-micron-nand-bad-block-marker-management.md)
- Related logical/physical mapping boundary: [`../cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md)

---

## Scope

The 2001 Case 145 grounding establishes the basic `CLEANMARKER` relation: JFFS2 does not infer successful erase and safe block reuse merely from an all-`0xFF` appearance. This follow-on asks a narrower later-source question:

> **When JFFS2 moved onto NAND, where did this reuse-admission evidence live, and what happened when the physical OOB placement policy itself changed?**

The bounded result is useful because the same logical evidence relation survives across different physical placements:

- on NOR, period documentation describes the cleanmarker as an in-band small JFFS2 node at the beginning of the erase block;
- on NAND, the cleanmarker is stored in the spare / out-of-band area of the first page;
- by 2007 JFFS2 could ask MTD for automatically placed free OOB bytes rather than own a fixed physical OOB offset;
- the 2007 patch explicitly says that if this changes the cleanmarker position, JFFS2 can conservatively re-erase an empty block and write a new marker rather than trust an unrecognized old placement.

This deepening therefore concerns **placement, recognition, and conservative requalification of reuse evidence**. It is not a general history of NAND OOB, ECC layout, JFFS2-on-NAND, OneNAND, MLC NAND, bad-block management, or UBIFS.

---

## Historical vocabulary

The inspected period sources use:

- `cleanmarker` / `clean marker`;
- `OOB` / `out of band`;
- `spare area`;
- `MTD_OOB_PLACE`;
- `MTD_OOB_AUTO`;
- `oobavail`;
- `eraseblock`;
- `block_isbad`;
- `cleanmarker_size`;
- `JFFS2_NODETYPE_CLEANMARKER`;
- `re-erase`;
- `NAND`, `NOR`, and `OneNAND`.

The following are project reconstructions rather than period JFFS2 terminology:

- **reuse-admission evidence**;
- **evidence placement**;
- **placement abstraction**;
- **conservative requalification**;
- **carrier-exclusion evidence**;
- **semantic identity of the witness**.

---

## Historical record 1 — by 2004, NAND cleanmarker state could exist outside the ordinary data area

A 12 September 2004 Linux-MTD CVS record for `fs/jffs2/scan.c` says it fixes a formatted-partition corner case on NAND where the cleanmarker was not included in ordinary used-data accounting because it **resides in OOB**.

That small maintenance change is useful evidence because it prevents an easy but false equivalence:

```text
ordinary data area contains no JFFS2 nodes
    !=
erase block contains no retained JFFS2 control evidence
```

In the NAND arrangement, a block can look empty in the ordinary data area while retaining a cleanmarker in OOB that affects how JFFS2 classifies the block.

### Safe historical conclusion

By September 2004, the JFFS2 implementation lineage represented NAND cleanmarker state outside the ordinary node/data region.

### Do not infer

The CVS record does **not** by itself establish:

- the first date on which JFFS2 acquired NAND support;
- the first date of OOB cleanmarkers;
- one universal OOB layout for every NAND device;
- that cleanmarker bytes were protected by the same ECC treatment as payload;
- that OOB contains only JFFS2 metadata.

---

## Historical record 2 — 2005 period explanation distinguishes NOR and NAND placement

A Linux-MTD mailing-list explanation dated 9 June 2005 describes the cleanmarker as a special JFFS2 node written immediately after erase so JFFS2 has evidence that the erase operation completed correctly.

It distinguishes the two placement regimes explicitly:

```text
NOR  -> small JFFS2 node at beginning of block
NAND -> spare area of first page
```

The same message says that if an erase block appears all `0xFF` but lacks a cleanmarker, JFFS2 will re-erase it rather than simply treating the apparent erased pattern as sufficient qualification.

This extends the 2001 reuse-admission rule into a NAND-specific placement context.

### Engineering reconstruction

The relevant relation is therefore not:

```text
specific physical byte offset == reuse authority
```

but rather:

```text
recognized cleanmarker in the placement regime expected by this stack
    -> evidence that the block passed the JFFS2 erase/qualification path
```

The exact physical embodiment of that evidence may differ between NOR and NAND.

---

## Historical record 3 — 2007 `MTD_OOB_AUTO` deliberately weakens JFFS2's dependence on fixed OOB positions

Artem Bityutskiy's JFFS2 patch posted 2 February 2007 (authored 31 January) replaces the old `MTD_OOB_PLACE` handling with `MTD_OOB_AUTO`.

Its rationale is unusually explicit. MTD can expose the free bytes in NAND OOB as a contiguous logical buffer even when those bytes are **physically discontinuous**. The patch says JFFS2 should use that facility so the filesystem no longer needs to care how the free bytes are physically situated; OneNAND is named as one motivation.

The diff removes JFFS2-maintained fields describing a specific `fsdata_pos` / `fsdata_len` placement and instead records the amount of OOB space available to JFFS2 (`oobavail`). Reads and writes use `MTD_OOB_AUTO`.

### Engineering reconstruction

This creates a small but important layer boundary:

```text
JFFS2 cleanmarker bytes
        ↓
MTD logical free-OOB view
        ↓
device-specific physical OOB positions
```

So:

```text
semantic witness identity
    != fixed physical OOB coordinates
```

and:

```text
filesystem-visible contiguous OOB buffer
    != physically contiguous OOB bytes
```

This is not an FTL: MTD OOB autoplacement is an interface/layout abstraction for spare-area bytes, not a general logical-block remapping layer. The comparison to Case 04 is functional only.

---

## The 2007 patch keeps bad-block classification separate from cleanmarker recognition

The same patch moves the NAND bad-block check into the erase-block scan before cleanmarker recognition:

- `block_isbad(...)` can classify the erase block as `BLK_STATE_BADBLOCK`;
- only after that does JFFS2 inspect for the NAND cleanmarker;
- absence of the cleanmarker does not itself mean the block is a NAND bad block.

This is a particularly useful boundary next to Case 78.

### Engineering reconstruction

```text
bad-block evidence
    -> carrier exclusion / do not treat as ordinary usable block

JFFS2 cleanmarker
    -> successful-erase / reuse-admission evidence for an otherwise usable block
```

Therefore:

```text
OOB placement region shared
    != metadata meaning shared
```

and:

```text
cleanmarker missing
    != NAND bad block
```

The two relations can have nearly opposite operational consequences even though both may involve NAND spare-area metadata.

Case 78 should continue to own bad-block retirement semantics; this file only uses the comparison to prevent an OOB-location shortcut.

---

## Historical record 4 — a changed marker position can trigger re-erase rather than unsafe reinterpretation

The strongest retention-specific sentence in the 2007 patch rationale says that `MTD_OOB_AUTO` may change the cleanmarker's position on some flashes, but this is acceptable because JFFS2 will **re-erase the empty eraseblocks and write the new correct cleanmarker**, and the author says this behavior was tested.

This closes a subtle question left open by the 2001 case.

The system does not need to preserve the old marker's exact byte coordinates forever in order to preserve the safety relation. If the current software no longer recognizes the old placement, an otherwise empty block can be put through erase again and receive a marker in the currently recognized layout.

### Engineering reconstruction

```text
old marker physically survives at an old/unrecognized placement
    != current software recognizes reuse-admission evidence
```

If the block is otherwise empty, the recovery path can be:

```text
unrecognized / missing current marker
        +
block scans empty
        ↓
conservative erase qualification again
        ↓
write marker using current placement convention
        ↓
block admitted as reusable
```

Thus:

- `physical survival of old evidence != current interpretability of that evidence`;
- `missing recognized witness != proof of physical failure`;
- `layout migration can be resolved by re-performing the qualifying transition`;
- `requalification != recovery of the old marker's physical location`.

This is a narrow JFFS2 behavior, not a general rule for all storage metadata migrations.

---

## Mount behavior preserves a conservative asymmetry

The 2007 patch comments that even when an OOB cleanmarker is not found, JFFS2 still scans the block to determine whether it is empty so it can decide whether erase is appropriate.

A 2010 Linux-MTD discussion restates the operational result in practical terms: during mount JFFS2 scans NAND OOB for cleanmarkers; if a block appears empty but lacks the marker, it is placed on the erase queue; after that qualification, later mounts can recognize the marker and avoid the extra erase.

The important asymmetry is:

```text
marker present and valid
    -> may support direct reuse classification

marker absent, block empty-looking
    -> do not infer equivalent authority from blankness alone
       re-erase / requalify instead
```

This is exactly the kind of retained-state relation Case 145 is meant to separate from payload persistence.

---

## Evidence placement itself can have a compatibility lifetime

The 2007 source change makes the following distinction explicit enough for the repository:

```text
lifetime of the physical cleanmarker bytes
    != lifetime of the software convention that knows where to find them
```

A marker can be physically present but operationally unavailable to a newer layout convention. Conversely, the reuse state can be reconstructed without recovering the old bytes by repeating the erase transition and writing a new recognized marker.

This is not data migration in the ordinary payload sense. It is migration/reconstitution of **control evidence governing whether capacity may re-enter service**.

The bounded lesson is:

> retaining a control witness requires not only retaining its bits, but either retaining the interpretation/placement convention or retaining a safe procedure that can re-establish the witness.

That sentence is an engineering reconstruction, not period JFFS2 vocabulary.

---

## 2007 MLC/NOP-1 RFC — substrate constraints can make the witness itself costly

A later 27 November 2007 RFC from Samsung is useful as a **design-pressure witness**, not as proof of merged behavior.

The author notes that the then-current NAND JFFS2 arrangement used two program operations on page 0 — one for the OOB cleanmarker and another for data — which conflicts with a one-program-per-page (`NOP 1`) constraint relevant to MLC NAND / OneNAND preparation. The RFC therefore proposes not writing the OOB cleanmarker in that case and explicitly says the final cleanmarker approach remained uncertain.

Safe conclusion:

```text
retaining a reuse-admission witness
    itself consumes device-programming budget / must obey substrate rules
```

Do not convert this RFC into a statement that all MLC JFFS2 deployments omitted cleanmarkers or that the proposed code became the final upstream policy.

This is a useful reminder that control metadata is not physically free merely because it is small.

---

## Cross-case comparison

### Case 78 — NAND bad-block marker / BBT

Both can involve NAND spare/OOB state, but the operational meaning differs sharply:

```text
bad-block retirement evidence -> exclude carrier
JFFS2 cleanmarker            -> admit successfully erased carrier for reuse
```

The common physical neighborhood does not establish common semantics, format, ownership, or genealogy.

### Case 04 — Flash virtual mapping

`MTD_OOB_AUTO` lets JFFS2 use a logical free-OOB view without binding itself to exact physical free-byte coordinates. This resembles Case 04 only at the abstract relation level:

```text
stable higher-layer designation
    != stable lower-level physical location
```

It is not evidence that MTD OOB autoplacement is an FTL or that JFFS2 cleanmarker handling descends from Flash Translation Layer designs.

### Case 145 — 2001 cleanmarker grounding

The 2001 record establishes why all-ones appearance is insufficient. The 2004–2007 evidence deepened here shows that the **location of the qualifying evidence can change independently of its role**, and that JFFS2 can conservatively re-perform erase when the current placement convention cannot recognize old qualification evidence.

### Case 44 — sanitization

Re-erasing an empty block to re-establish a cleanmarker is a filesystem reuse-qualification action. Nothing here upgrades it into a secure-erasure or purge guarantee.

---

## Historical record / reconstruction / analogy / interpretation ledger

### Historical record (`H/P`)

The sources directly establish that:

- by 2004 JFFS2 NAND cleanmarker state resided in OOB;
- a 2005 period explanation distinguishes in-band NOR placement from NAND spare-area placement;
- the 2007 JFFS2 patch moves from explicit OOB positioning to `MTD_OOB_AUTO`;
- MTD can present physically discontinuous free OOB bytes as a contiguous view;
- JFFS2's NAND setup records the cleanmarker as out-of-band (`cleanmarker_size = 0` for inline accounting);
- bad-block detection and cleanmarker checking remain distinct scan operations;
- the author explicitly expected position changes on some flashes and reported testing conservative re-erase plus new-marker creation;
- a late-2007 RFC identifies cleanmarker programming as one contributor to an NOP-1 compatibility problem.

### Engineering reconstruction (`E`)

The project derives:

- `main-data emptiness != absence of control state`;
- `reuse-admission semantics != fixed marker coordinates`;
- `physical survival of witness != current recognizability`;
- `missing recognized cleanmarker != bad-block identity`;
- `placement migration can be repaired by requalification rather than by preserving old coordinates`;
- `control metadata has substrate/programming cost`.

### Functional analogy (`A`)

Only relation-level comparisons are made to:

- Case 04 logical/physical indirection;
- Case 78 carrier exclusion metadata;
- Case 44 secure-sanitization boundaries.

No genealogy is inferred from these comparisons.

### Philosophical interpretation (`I`)

A modest interpretation is that a retained technical state may depend on a **recognition convention** as well as surviving bits. When the convention changes, persistence may be achieved not by recovering the old sign exactly but by safely re-performing the transition that authorizes a new sign.

This is not attributed to JFFS2 developers as a philosophical claim, and it is not generalized to archival or human memory.

---

## Explicit non-claims

This evidence does **not** establish that:

1. JFFS2 invented OOB metadata.
2. JFFS2 invented cleanmarker-like erase qualification.
3. September 2004 is the first appearance of NAND cleanmarkers.
4. The 2005 mailing-list explanation is a formal filesystem specification.
5. Every NAND uses the same spare-area layout.
6. `MTD_OOB_AUTO` is an FTL.
7. A JFFS2 cleanmarker is a NAND factory bad-block marker.
8. Missing cleanmarker means bad block.
9. Valid cleanmarker cryptographically proves every cell is erased.
10. Re-erase provides secure sanitization.
11. All old cleanmarkers become unrecognizable after the 2007 change.
12. Every `MTD_OOB_AUTO` migration physically moves a marker.
13. The 2007 MLC/NOP-1 RFC was necessarily merged as posted.
14. All MLC NAND has the same one-program-per-page rule.
15. OOB cleanmarker bytes are necessarily protected by the same ECC policy as payload.
16. Filesystem-visible OOB contiguity implies physical contiguity.
17. `block_isbad` and JFFS2 cleanmarker checks have the same authority source.
18. A block that is currently reusable must remain reusable across every future software/layout convention without requalification.

---

## Source ledger

### P1 — Linux-MTD CVS, `scan.c` 1.111 -> 1.112, 12 September 2004 — `H/P`

`mtd/fs/jffs2 scan.c,1.111,1.112`

<https://lists.infradead.org/pipermail/linux-mtd-cvs/2004-September/004049.html>

Commit log: fixes the no-valid-node formatted-partition case on NAND where the cleanmarker is not counted with ordinary data because it resides in OOB.

Use: period implementation witness for OOB cleanmarker state and accounting consequences.

### P2 — Linux-MTD mailing list, 9 June 2005 — `H/P*`

`mkfs.jffs2 --cleanmarker=?`

<https://lists.infradead.org/pipermail/linux-mtd/2005-June/012767.html>

Use: period engineering explanation of NOR-vs-NAND cleanmarker placement and conservative re-erase when an all-`0xFF` block lacks a marker.

Strength note: useful contemporary practitioner/developer-list record, but not treated as a normative specification or invention claim.

### P3 — Artem Bityutskiy, `[PATCH] [JFFS2] use MTD_OOB_AUTO`, authored 31 January / posted 2 February 2007 — `H/P`

<https://lists.infradead.org/pipermail/linux-mtd/2007-February/017323.html>

Directly inspected anchors:

- `MTD_OOB_AUTO` exposes free OOB bytes as a contiguous buffer even if physically discontinuous;
- JFFS2 should stop caring about exact free-byte positions;
- possible cleanmarker position change is handled by re-erasing empty eraseblocks and writing a new marker;
- `block_isbad()` is separate from `jffs2_check_nand_cleanmarker()`;
- `cleanmarker_size = 0` because the NAND cleanmarker is out-of-band;
- read/write operations use `MTD_OOB_AUTO` and `oobavail`.

This is the strongest source for the bounded placement-abstraction claim.

### P4 — Kyungmin Park, Samsung, `[RFC][PATCH][JFFS2] JFFS2 support for NOP 1`, 27 November 2007 — `H/P-RFC`

<https://lists.infradead.org/pipermail/linux-mtd/2007-November/020008.html>

Use only as a design-pressure witness: the then-current cleanmarker-plus-data programming pattern could conflict with a one-program constraint in the targeted MLC/OneNAND context. The RFC status is retained explicitly; no shipping/upstream-final behavior is inferred from the proposal.

### P5 — Linux-MTD discussion, 5 January 2010 — `H/P*`

`JFFS2 - speed up while booting`

<https://lists.infradead.org/pipermail/linux-mtd/2010-January/028413.html>

Use: later operational explanation that JFFS2 scans OOB cleanmarkers; apparently empty blocks without markers are queued for erase, while subsequent mounts can recognize the marker and avoid the extra erase.

It is corroborative later-source evidence, not projected backward to prove exact 2004 code behavior not otherwise documented.

---

## Prior-art and repository boundary

A fresh search of `tmzncty/computing-archaeology` found no dedicated JFFS2 cleanmarker / NAND-OOB study to reuse. Broad NAND spare-area history, ECC-layout evolution, JFFS/JFFS2/YAFFS/UBIFS genealogy, and MTD API archaeology remain better candidates for that repository if expanded.

This record stays narrower: it deepens the retention-specific question of how **reuse-admission evidence survives a change in physical metadata placement**.

---

## Remaining evidence debt

After this slice, the most useful remaining Case 145 work is narrower than before:

1. recover the exact introduction commit for JFFS2 NAND OOB cleanmarkers rather than using a 2004 public floor;
2. identify the exact upstream merge commit / released-kernel floor for the 2007 `MTD_OOB_AUTO` change;
3. trace how later `MTD_OPS_AUTO_OOB`, large-OOB NAND, ECC placement, and mtd-utils `flash_erase -j` changed the compatibility boundary;
4. test the requalification path under emulated or physical interrupted erase / missing-marker / layout-change faults;
5. keep MLC paired-page / NOP constraints separate unless a product-specific JFFS2 failure trace is available;
6. keep NAND bad-block/ECC retirement semantics in Case 78 and secure erase in Case 44;
7. route broad filesystem genealogy to `computing-archaeology`.

---

## Bounded result

The deepening supports the following concise relations:

```text
reuse-admission evidence semantics
    != fixed physical marker coordinates

ordinary data-area emptiness
    != absence of retained control evidence

cleanmarker missing / unrecognized
    != NAND bad-block identity

physically surviving old marker
    != currently recognized reuse authority

layout convention changes
    -> safe response may be requalification by erase + new marker
       rather than trusting apparent blankness
```

That is enough to close this one-round slice without turning Case 145 into a general NAND-filesystem history.