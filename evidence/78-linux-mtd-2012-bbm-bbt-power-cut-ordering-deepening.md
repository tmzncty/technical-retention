# Case 78 deepening — Linux MTD 2012 BBM / flash-BBT publication ordering under power cuts

**Status:** `bounded deepening complete`

## Scope

This evidence slice deepens [`../cases/78-micron-nand-bad-block-marker-management.md`](../cases/78-micron-nand-bad-block-marker-management.md) at one narrow seam:

> When Linux MTD represents a grown bad NAND block both by a per-block OOB bad-block marker (BBM) and by a centralized flash-resident bad-block table (BBT), what ordering did maintainers choose between those representations, and what did they claim about sudden power loss between the writes?

The bounded historical window is **Linux v3.3 → the January 2012 linux-mtd patch discussion → released Linux v3.4**, with a small later-source continuity check only where needed.

This is not a general NAND crash-consistency study. It does not attempt to prove NAND-page program atomicity, controller power-loss behavior, bootloader interoperability, managed-SSD FTL behavior, or universal BBT safety.

The contribution is narrower: it shows that a bad-block exclusion relation may be deliberately published into **multiple non-atomically-updated representations**, that maintainers explicitly reasoned about the order of those writes under power cuts, and that the chosen released path still admitted a bounded temporary-divergence window.

---

## Claim-type boundary

### Historical record

What the January 2012 linux-mtd patch/thread and released v3.3/v3.4 source actually say or implement.

### Engineering reconstruction

What follows from having an in-memory BBT, a per-block OOB marker, and a flash-resident BBT whose updates are ordered but not transactionally committed as one object.

### Functional analogy

A limited comparison with other repository cases in which currentness or exclusion survives through redundant control representations. No shared implementation or historical genealogy is claimed.

### Philosophical interpretation

Only the restrained observation that technical retention can preserve a **negative rule of non-use** by maintaining multiple representations whose agreement may lag. No claim is made that Linux MTD engineers used philosophical vocabulary.

---

## Sources and evidence classes

### P1 — January 2012 linux-mtd patch v4

Brian Norris, `[PATCH v4 2/2] mtd: nand: write BBM to OOB even with flash-based BBT`, 20 January 2012:

<https://lists.infradead.org/pipermail/linux-mtd/2012-January/039391.html>

This is a contemporaneous primary engineering source. It contains both the proposed code and the author’s explicit power-cut rationale.

### P2 — contemporaneous review discussion

Shmulik Ladkani reply, 21 January 2012:

<https://lists.infradead.org/pipermail/linux-mtd/2012-January/039392.html>

Follow-up identifying the erase-before-rewrite hazard after a previous interrupted BBM/BBT update:

<https://lists.infradead.org/pipermail/linux-mtd/2012-January/039393.html>

Brian Norris reply, 23 January 2012:

<https://lists.infradead.org/pipermail/linux-mtd/2012-January/039406.html>

These messages matter because they preserve uncertainty and failure-window reasoning that the released code alone does not narrate.

### P3 — released Linux v3.3 source

`drivers/mtd/nand/nand_base.c` at tag `v3.3`:

<https://github.com/torvalds/linux/blob/v3.3/drivers/mtd/nand/nand_base.c>

The inspected `nand_default_block_markbad()` path updates the RAM BBT and then chooses **either** the flash-based BBT path **or** the OOB-marker path. When `NAND_BBT_USE_FLASH` is set, `nand_update_bbt()` is called instead of writing the grown-bad-block marker into the per-block OOB location.

### P4 — released Linux v3.4 source

`drivers/mtd/nand/nand_base.c` at tag `v3.4`:

<https://github.com/torvalds/linux/blob/v3.4/drivers/mtd/nand/nand_base.c>

The released source contains the changed default sequence and the new `NAND_BBT_NO_OOB_BBM` opt-out. This establishes that the January design was not merely an unmerged mailing-list proposal: the behavior is present in a released kernel tag.

### Later continuity witness

Later Linux source retains the same broad rule in `nand_block_markbad_lowlevel()`: attempt erase, write the per-block bad-block marker unless disabled, then update the BBT. This is used only to show continuity of the relation, not to project later driver architecture back into 2012.

---

## Historical record

### H/P — Linux v3.3 could let the flash BBT become the sole current record of grown bad blocks

In the released v3.3 `nand_default_block_markbad()` path, Linux first updates its in-memory `chip->bbt`. It then branches:

```text
if NAND_BBT_USE_FLASH:
    nand_update_bbt(...)
else:
    write bad-block marker into OOB
```

For the flash-BBT configuration, newly grown bad blocks therefore did not also receive the ordinary per-block OOB marker through this default path.

The January 2012 patch describes the retention consequence directly: over time, OOB bad-block markers become stale and the flash-resident BBT becomes the only source of current grown-bad-block information.

This is already a useful distinction:

```text
physical block has become bad
    != every representation of badness is current
```

The defect state and the metadata representations that encode exclusion are not the same object.

---

### H/P — the patch argues for two representations because they serve different recovery/interoperability paths

The patch does not justify writing the OOB BBM merely as duplicate bookkeeping. It gives two concrete cases:

1. a bootloader may not understand the Linux flash-BBT format;
2. a flash BBT may be corrupted, forcing the medium to be rescanned for bad blocks.

The author also characterizes the OOB location as the standard location for bad-block information and notes that its distributed placement can tolerate some corruption differently from one centralized table.

For Case 78, the important historical point is therefore not `more copies are always safer`. It is:

> **different representations can preserve the same exclusion relation for different readers and recovery paths.**

A centralized flash BBT can be efficient/current for Linux while a per-block marker can remain legible to a simpler scanner or bootloader.

---

### H/P — v4 deliberately orders BBM before flash-BBT publication for power-cut reasons

The January 2012 v4 patch describes the new default marking sequence as:

```text
1. erase affected block so the OOB marker can be written cleanly
2. update the in-memory BBT
3. write the bad-block marker to the affected block's OOB area
4. update the flash-based BBT
```

Its revision note explicitly says v4 reordered the operations so the BBM is written before the BBT because this “should help with power cuts.”

The released Linux v3.4 source contains the same four-stage ordering in the function comment and implementation.

This is a period engineering decision about **publication order among exclusion-state embodiments**.

It is not proof of a transaction.

---

### H/P — maintainers explicitly accepted a window in which OOB BBM and flash BBT can disagree

The patch says a power cut between stages (3) and (4) can leave the OOB marker and flash BBT “out of sync.” It then expresses an expectation that later I/O after reboot will rediscover that the block should be marked bad and thereby bring the representations back into agreement.

The important historical vocabulary here is not `atomic commit`; it is the much weaker claim that the sequence should handle power cuts “gracefully enough.”

Therefore the source itself blocks this stronger statement:

```text
ordered BBM + BBT writes
    != atomic bad-block-state commit
```

and also blocks:

```text
BBM/BBT temporary disagreement
    == loss of all exclusion evidence
```

The proposed recovery relies on one representation remaining discoverable and later work repairing the other representation.

---

### H/P — the review thread exposes an additional erase-before-rewrite interruption seam

Shmulik Ladkani immediately noticed a second-order problem. Suppose a prior power cut happened after the OOB BBM was written but before the flash BBT was updated. On a later attempt to mark the block again, the new default path begins by erasing the affected block before rewriting the OOB marker.

That means the recovery attempt itself can create another interval in which the surviving OOB marker has just been erased and has not yet been rewritten.

Brian Norris replied that this matters in cases including:

- a power cut after erase but before re-writing OOB;
- a write error while re-writing OOB.

He suggested checking the existing marker could be useful, but the released v3.4 function inspected here still performs the erase-first sequence.

This matters because it prevents an over-clean reconstruction such as:

```text
BBM-first ordering
    -> every power cut leaves a conservative durable marker
```

That universal claim is not supported.

The narrower result is:

> **the 2012 change improves the representation structure and intentionally places OOB publication before flash-BBT publication, while contemporaneous reviewers still identify interruption windows that the simple ordering alone does not close.**

---

### H/P — released v3.4 preserves an opt-out because OOB marking is not universally writable

The patch adds `NAND_BBT_NO_OOB_BBM` for systems that use a flash BBT but cannot support writing new OOB bad-block markers, with ECC use of the spare area given as an example.

This is important negative evidence:

```text
flash BBT support
    != universal ability to maintain per-block OOB BBMs
```

The dual-representation strategy is therefore conditional on the device/controller/OOB layout exposing a writable marker path.

It must not be generalized to every raw-NAND controller, much less to managed SSD internals.

---

## Retained-state decomposition

This slice requires at least seven distinct states.

### 1. Physical block condition

The block may have suffered a program/erase failure or other condition that causes software to classify it as bad.

This is not itself a metadata representation.

### 2. In-memory bad-block state

The running kernel keeps a RAM BBT used for immediate allocation/admission decisions.

It has process/boot lifetime unless reconstructed from persistent evidence.

### 3. Per-block OOB bad-block marker

A marker attached to the affected eraseblock supplies distributed negative evidence that a scanner or other software can inspect.

It is a physical embodiment of the exclusion relation, not the defect itself.

### 4. Flash-resident bad-block table

The flash BBT centralizes current bad-block state and, in the broader Case 78 implementation, may itself be mirrored and version-qualified.

Its currentness does not imply the OOB marker is current unless the implementation maintains both.

### 5. BBT version / currentness metadata

Version state helps choose between primary/mirror BBT candidates. It does not encode every individual block-retirement event.

### 6. Reader / interpreter capability

A bootloader or recovery scanner may understand OOB BBMs while not understanding a particular flash-BBT format.

Thus metadata survival and metadata interpretability remain distinct.

### 7. Resynchronization obligation

After an interrupted update, one representation can indicate that the other should eventually be repaired.

This is not a user payload and not a separately serialized transaction log in the inspected path. It is a maintenance consequence reconstructed from the surviving negative evidence plus later block-check/mark behavior.

---

## Engineering reconstruction

### E — one exclusion relation can have several non-equivalent embodiments

The same operational rule — `do not use this physical block` — can be represented by:

```text
RAM BBT entry
per-block OOB BBM
flash-resident BBT entry
```

These are not interchangeable in every circumstance because they differ in persistence, locality, corruption domain, and reader compatibility.

Therefore:

```text
same exclusion meaning
    != same embodiment
    != same persistence horizon
    != same interpreter population
```

---

### E — representation agreement is a maintained property, not a prerequisite for every instant of safety

The 2012 source accepts that BBM and flash BBT can temporarily disagree after a power cut.

That means `all representations agree` is not the only state from which continued recovery may be possible.

A more precise reconstruction is:

```text
persistent negative evidence survives somewhere
    + later software can discover it
    + later software is permitted to update stale peers
        -> exclusion relation may converge again
```

This is deliberately conditional. If the surviving representation cannot be read, is itself corrupted, or is erased before it is propagated, convergence is not guaranteed.

---

### E — publication order can bias the failure mode without making the update atomic

Writing the distributed OOB marker before the centralized flash BBT means one interruption window can leave:

```text
OOB says BAD
flash BBT still says GOOD/old
```

rather than first publishing only the centralized update while the per-block marker remains stale.

In a recovery environment that trusts/scans OOB markers, the former can be a conservative asymmetry: an extra `bad` indication tends to exclude a block rather than silently re-admit it.

But this statement requires assumptions about marker write completion and later marker inspection. The contemporaneous erase-before-rewrite discussion shows why it cannot be promoted into a universal crash-safety theorem.

Hence:

```text
safety-oriented write order
    != atomic update
    != durable transaction
    != power-cut proof
```

---

### E — rediscovery/republication is different from rollback

The patch’s proposed post-reboot behavior is not transactional rollback to a pre-update state. It is closer to:

```text
surviving per-block negative evidence
    -> later observation
    -> recreate / update centralized negative state
```

The system may therefore regain consistency by **re-observing a surviving fact** rather than by replaying a durable transaction record.

This is an important persistence-horizon distinction:

```text
reconstructable control state
    != checkpointed control state
```

---

### E — a defect marker is not a complete defect history

Even when the OOB BBM survives and repairs a stale flash BBT, it does not tell the system:

- exactly when the failure occurred;
- which command first exposed it;
- how many prior correctable errors occurred;
- whether another metadata write was interrupted;
- the complete provenance of the retirement decision.

It preserves a current negative qualification, not an audit history.

---

## Functional comparisons — not genealogy

### A — Case 78’s 2004 mirrored/versioned BBT deepening

The earlier deepening concerns **currentness among centralized BBT copies**:

```text
primary BBT
mirror BBT
version ordering / candidate validity
```

This 2012 slice concerns **cross-representation publication**:

```text
per-block OOB BBM
flash-resident BBT
```

The two problems interact but are not the same.

A power cut between OOB publication and `nand_update_bbt()` is not equivalent to a power cut between primary- and mirror-BBT writes.

### A — Case 115 / other replay-based systems

Some software cases preserve an explicit log that can replay incomplete state changes. The inspected 2012 NAND path does not provide evidence for such a transaction log. Its bounded recovery idea instead relies on persistent per-block negative evidence being rediscovered and used to repair a stale summary.

The functional similarity is only that a later process can reconstruct current control state from retained evidence.

### A — tombstones and negative metadata

As in Cases 41/42/74, a negative record can make a still-physically-present positive candidate inadmissible. Here the object is a physical NAND block, and the negative state is distributed across BBM/BBT representations. No data-model or historical genealogy is implied.

---

## Philosophical interpretation — bounded

Case 78 already shows that persistence can require preserving a prohibition: `this block must not count as usable`.

The 2012 Linux path sharpens that idea without requiring a larger philosophy. A prohibition can survive through several material inscriptions whose agreement is itself maintained over time. What must remain is not necessarily one immutable record; it can be enough that a future operation can still reconstruct the exclusion relation from an admissible surviving witness.

That is an engineering fact about negative-state retention and reconstruction. It does not make BBMs `memory` in a psychological sense, and it does not establish a universal theory of distributed truth.

---

## Explicit non-claims

This slice does **not** claim any of the following:

1. Linux invented bad-block markers or flash bad-block tables.
2. Linux v3.4 makes bad-block updates transactionally atomic.
3. The OOB marker write is itself atomic under sudden power failure.
4. A completed `nand_do_write_oob()` proves media-level durability against every failure model.
5. A power cut between OOB and flash-BBT update is always harmless.
6. A later boot necessarily scans every OOB marker before the affected block could be used.
7. Every bootloader understands Linux flash-BBT format.
8. Every bootloader scans OOB BBMs correctly.
9. Every raw-NAND controller permits writable OOB BBMs.
10. `NAND_BBT_NO_OOB_BBM` is unsafe in every system; it explicitly exists for systems whose layout/constraints require it.
11. Mirrored/versioned flash BBTs are atomic merely because the per-block BBM is written first.
12. A bad-block marker records the complete error or retirement history.
13. Reconstructability after reboot is equivalent to retaining an exact execution checkpoint.
14. The v3.4 default path proves safety across controller reset, kernel panic, DMA failure, torn NAND program, ECC failure, or simultaneous metadata corruption.
15. The raw-NAND Linux mechanism describes proprietary managed-SSD FTL internals.
16. Chronological precedence establishes a genealogy to later bootloaders, controllers, or SSD firmware.

---

## Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| v3.3 flash-BBT marking path could update the flash BBT without also writing the grown-bad-block OOB marker | H/P | directly grounded in released v3.3 source |
| January 2012 patch identifies stale OOB markers / flash BBT as sole current source as the prior behavior | H/P | explicit patch rationale |
| patch cites bootloader incompatibility and BBT-corruption rescan as reasons to keep OOB BBMs current | H/P | explicit patch rationale |
| v4 orders OOB BBM publication before flash-BBT update because that should help with power cuts | H/P | explicit revision note + code |
| released v3.4 contains the four-stage erase → RAM BBT → OOB BBM → flash BBT path | H/P | released source |
| power loss between OOB BBM and flash-BBT update can leave them out of sync | H/P | explicit patch statement |
| patch author expected later I/O to rediscover and re-sync that state | H/P | explicit patch statement; expectation, not fault-injection proof |
| contemporaneous reviewer identified erase-before-rewrite as another interruption hazard after a prior partial update | H/P | explicit review discussion |
| Brian Norris acknowledged power-cut-after-erase-before-OOB-rewrite and OOB rewrite failure as relevant cases | H/P | explicit reply |
| `NAND_BBT_NO_OOB_BBM` permits systems to opt out of new OOB marking | H/P | patch + released code |
| BBM-first publication can bias one failure window toward a conservative exclusion witness | E | bounded reconstruction with stated assumptions |
| BBM-first publication makes update atomic | X | explicitly rejected |
| temporary representation disagreement necessarily means the exclusion relation is lost | X | rejected; source describes rediscovery/re-sync path |
| reconstructable BBT state = checkpointed BBT state | X | rejected |
| per-block BBM = complete bad-block history | X | rejected |

---

## What this changes in Case 78

Before this slice, Case 78 already established:

- factory marks can be erasable;
- operational BBT state can be persisted and rebuilt;
- Linux flash BBTs can be mirrored/versioned;
- BBT currentness requires candidate validity, not just version magnitude;
- the BBT’s own physical carrier can later be retired and replaced.

This deepening adds a missing **cross-representation interruption boundary**:

```text
physical retirement decision
    -> RAM exclusion state
    -> distributed OOB exclusion evidence
    -> centralized flash-BBT exclusion state
```

and shows that the latter two persistent representations were intentionally ordered but could temporarily diverge.

The resulting Case-78 relation is now more precise:

```text
negative media-qualification state
    != one marker
    != one table
    != one atomic publication event
```

---

## Remaining evidence debt

The following remain useful but are outside this bounded slice:

- identify the exact upstream commit object that carried the January patch into mainline, rather than relying only on the mailing-list series plus v3.3/v3.4 released-source delta;
- power-cut fault injection at each stage of the released v3.4 marking sequence;
- NAND-specific evidence about partial/torn OOB marker programming under power failure;
- exact boot-time and first-use paths by which a stale flash BBT plus newer OOB BBM is rediscovered on representative drivers;
- whether and how specific bootloaders (U-Boot, Barebox, vendor ROMs) interoperate with Linux-generated grown-bad-block markers and flash BBT formats;
- crash windows inside `nand_update_bbt()` across primary/mirror publication;
- controller families that require `NAND_BBT_NO_OOB_BBM`, and the alternative persistence/recovery contract they rely on;
- dual corruption of OOB BBM and flash-BBT state;
- empirical recovery when BBT carrier failure and a newly grown bad block occur in the same interruption interval;
- broader Linux-MTD / bootloader bad-block-management genealogy, which belongs primarily in `tmzncty/computing-archaeology`.

None of these gaps blocks the bounded conclusion that Linux v3.4 deliberately maintained both per-block and centralized exclusion representations and that the implementation’s power-cut reasoning was **ordering + later reconstruction**, not demonstrated transactional atomicity.

---

## Related repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `NAND BBT bad block marker` found no dedicated case to reuse.

If the broader history is pursued, `computing-archaeology` should own:

- Linux-MTD BBT genealogy before and after 2012;
- U-Boot/Barebox/controller interoperability history;
- NAND-controller OOB/ECC layout constraints;
- managed-flash implementation genealogy.

`technical-retention` should retain only the bounded argument about the persistence, divergence, reconstruction, and authority of negative media-qualification state.

---

## Sources

### Primary / contemporary

- Brian Norris, **`[PATCH v4 2/2] mtd: nand: write BBM to OOB even with flash-based BBT`**, linux-mtd, 20 January 2012: <https://lists.infradead.org/pipermail/linux-mtd/2012-January/039391.html>.
- Shmulik Ladkani, review reply, 21 January 2012: <https://lists.infradead.org/pipermail/linux-mtd/2012-January/039392.html>.
- Shmulik Ladkani, erase-before-rewrite follow-up, 21 January 2012: <https://lists.infradead.org/pipermail/linux-mtd/2012-January/039393.html>.
- Brian Norris, response on the additional interruption cases, 23 January 2012: <https://lists.infradead.org/pipermail/linux-mtd/2012-January/039406.html>.
- Linux `v3.3`, `drivers/mtd/nand/nand_base.c`: <https://github.com/torvalds/linux/blob/v3.3/drivers/mtd/nand/nand_base.c>.
- Linux `v3.4`, `drivers/mtd/nand/nand_base.c`: <https://github.com/torvalds/linux/blob/v3.4/drivers/mtd/nand/nand_base.c>.

### Later continuity / documentation

- Linux kernel MTD NAND documentation, `Bad block table support`: <https://www.kernel.org/doc/html/v4.20/driver-api/mtdnand.html>.
- Later Linux source retaining BBM-before-BBT ordering in `nand_block_markbad_lowlevel()`: <https://github.com/torvalds/linux/tree/master/drivers/mtd/nand/raw>.

### Internal comparisons

- [`78-linux-mtd-2004-mirrored-versioned-bbt-deepening.md`](78-linux-mtd-2004-mirrored-versioned-bbt-deepening.md)
- [`78-linux-mtd-2004-2021-bbt-currentness-admissibility-deepening.md`](78-linux-mtd-2004-2021-bbt-currentness-admissibility-deepening.md)
- [`78-linux-mtd-2016-bbt-carrier-failure-relocation-deepening.md`](78-linux-mtd-2016-bbt-carrier-failure-relocation-deepening.md)
- [`../cases/78-micron-nand-bad-block-marker-management.md`](../cases/78-micron-nand-bad-block-marker-management.md)

---

## Bounded conclusion

Released Linux v3.4 changed the default flash-BBT bad-block-marking path so that a grown bad block could be represented both by its per-block OOB marker and by the flash-resident BBT, with the OOB marker written before the centralized BBT update. The contemporaneous patch explicitly framed that order as helpful under power cuts while also acknowledging that an interruption could leave the representations out of sync and require later rediscovery/resynchronization. Reviewers immediately identified a further erase-before-rewrite interruption window, preventing the ordering from being mistaken for transaction-level atomicity.

For technical retention, the useful result is therefore not `Linux solved bad-block crash consistency in 2012`. It is the narrower relation:

```text
retained exclusion relation
    may have multiple persistent embodiments
    whose publication is ordered but non-atomic,
    whose disagreement can itself become maintenance debt,
    and whose recoverability depends on a surviving witness
    plus a future interpreter able to reconstruct current exclusion state.
```
