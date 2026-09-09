# Case 78 Deepening — Linux MTD BBT Currentness Arithmetic and Candidate Admissibility (2004–2021)

## Scope

This addendum deepens [`Case 78`](../cases/78-micron-nand-bad-block-marker-management.md) at a narrow seam left open by the earlier mirrored/versioned-BBT study: **when two retained BBT representations disagree, what makes one representation authoritative enough to reconstruct the working exclusion map?**

The bounded historical witnesses are all from the Linux MTD lineage:

- the 28 May 2004 MTD CVS change that introduced/refactored per-chip mirrored BBT reconciliation;
- the released Linux 2.6.12 source of 17 June 2005;
- Brian Norris's September 2011 `wait to set BBT version` patch, merged with the MTD tree in November 2011;
- Stefan Riedmueller's March 2021 upstream patch that makes BBT search skip blocks already marked bad.

This is **not** a general Linux-MTD genealogy, not proof that Linux invented BBT versioning, not a claim about proprietary SSD controllers, and not a controlled power-cut experiment. The purpose is narrower: to separate four relations that the convenient phrase `take the newer BBT` can hide — **candidate discovery, media admissibility/readability, version ordering, and content validity**.

---

## Historical record

### H/P — 28 May 2004: the archived MTD code used ordinary numeric ordering for a 32-bit-stored BBT version

The archived Linux MTD CVS diff dated 28 May 2004 adds/refactors `check_create()` for per-chip BBTs. When primary and mirror both exist but their versions differ, the new code compares them with an ordinary numeric relation:

```c
if (td->version[i] > md->version[i])
```

and chooses the numerically larger table before scheduling the other representation for rewrite. In the same archived source, BBT search reads the version as a little-endian `int` from the OOB area and `write_bbt()` stores it with `cpu_to_le32`; `nand_update_bbt()` increments the per-chip version before writing primary and mirror.

The historically safe statement is therefore only:

> In the inspected May-2004 implementation, BBT currentness was discriminated by an ordinary numeric comparison over the then-stored version representation.

It does not follow that this was the final Linux rule, that the version was an audit sequence with unlimited range, or that a larger number independently proved the selected table's contents were usable.

**Primary contemporary source:** Linux MTD CVS archive, 28 May 2004, `nand_bbt.c` 1.9 -> 1.10: <https://lists.infradead.org/pipermail/linux-mtd-cvs/2004-May/003683.html>.

### H/P — Linux 2.6.12: the persisted version became one byte and comparison used a signed modular difference

The final Linux 2.6.12 release commit is dated 17 June 2005. Its `nand_bbt.c` writes `td->version[chip]` into a single OOB byte and logs it as a two-digit hexadecimal value. `nand_update_bbt()` increments the in-memory version on each update.

The same released source no longer decides currentness with a plain `>` comparison. If versions differ it evaluates:

```c
((int8_t)(td->version[i] - md->version[i])) > 0
```

and selects/re-writes primary or mirror according to the sign of that truncated difference.

This gives a directly inspectable historical floor for a **cyclic / wrap-aware comparison rule** in released Linux code. The code itself does not use the later project phrase `serial-number arithmetic`, so that phrase is an engineering description rather than historical vocabulary.

A bounded reconstruction shows why the distinction matters. If one update advances a one-byte version from `0xff` to `0x00` while its peer remains at `0xff`, then the raw numeric relation `0x00 > 0xff` is false, whereas the inspected signed-difference expression evaluates `(int8_t)(0 - 255)` as `+1` and can treat `0x00` as the newer nearby version.

**Primary released source:** Linux v2.6.12, `drivers/mtd/nand/nand_bbt.c`: <https://github.com/torvalds/linux/blob/v2.6.12/drivers/mtd/nand/nand_bbt.c>.

**Release anchor:** Linux 2.6.12 final commit `9ee1c939d1cb936b1f98e8d81aeffab57bae46ab`, 17 June 2005: <https://github.com/torvalds/linux/commit/9ee1c939d1cb936b1f98e8d81aeffab57bae46ab>.

### E — signed one-byte difference supplies local cyclic order, not unlimited chronology

The signed-difference rule has an important mathematical limit. With an 8-bit cyclic counter, it can order **nearby** versions across wrap, but it does not encode an unbounded total history. A modular separation of exactly `0x80` has no unique before/after interpretation under an 8-bit signed-difference rule, and sufficiently large unobserved divergence can reverse the apparent order.

This is an **engineering reconstruction from the expression**, not an explicit Linux 2.6.12 guarantee that peers can diverge by any specific maximum. In the ordinary mirrored-update path the intended divergence is small because both copies are rewritten toward the same version. The important retention conclusion is narrower:

> `finite currentness token` != `unbounded chronological sequence`.

The comparison rule and the bounded-divergence assumptions around it are part of what gives the token meaning.

### H/P — September 2011: a numerically newer BBT could still be an invalid candidate

Brian Norris's 20 September 2011 patch, titled `mtd: nand: wait to set BBT version`, documents a concrete failure mode in the reconciliation sequence. Its example is:

```text
primary version 0x02
mirror  version 0x01
primary has uncorrectable ECC errors
```

Before the fix, the code could first choose the primary because its version was newer, copy `0x02` into the mirror's in-memory version state, then discover the primary was unreadable due to ECC, retry from the clean mirror, and finally write the old mirror contents back while labeling them version `0x02`. The patch removes the early version propagation, clears the version of an ECC-invalid candidate, and postpones equalizing versions until after a valid readable table has been selected.

The patch is unusually useful for this project because it states the boundary in an implementation-level counterexample:

> **newer version metadata was not sufficient to establish a usable current BBT.**

The MTD merge commit of 7 November 2011 explicitly lists `mtd: nand: wait to set BBT version` among the merged changes.

**Primary development record:** Brian Norris, `[PATCH v2 11/14] mtd: nand: wait to set BBT version`, linux-mtd, 20 September 2011: <https://lists.infradead.org/pipermail/linux-mtd/2011-September/037965.html>.

**Upstream merge anchor:** Linux commit `e0d65113a70f1dc514e625cc4e7a7485a4bf72df`, 7 November 2011: <https://github.com/torvalds/linux/commit/e0d65113a70f1dc514e625cc4e7a7485a4bf72df>.

### H/P — March 2021: the BBT's own storage block can become inadmissible, making candidate placement part of currentness

On 28 March 2021, upstream commit `bd9c9fe2ad04546940f4a9979d679e62cae6aa51` changed BBT search so blocks already marked bad are skipped before their BBT signature/version is considered. The commit message explains the reason: blocks containing the BBT can themselves become bad; in a rare case where two BBT blocks wear out, failing to skip bad candidates could cause an obsolete BBT to be used instead of a newer available version.

The code change is small but conceptually decisive. A BBT-looking record is not an admissible candidate merely because its signature and version bytes can be found at a reserved location. The media holding the control state participates in the authority relation.

Therefore:

> `candidate has recognizable BBT metadata` != `candidate is admissible as the current BBT`.

**Primary upstream source:** Linux commit `bd9c9fe2ad04546940f4a9979d679e62cae6aa51`, `mtd: rawnand: bbt: Skip bad blocks when searching for the BBT in NAND`, 28 March 2021: <https://github.com/torvalds/linux/commit/bd9c9fe2ad04546940f4a9979d679e62cae6aa51>.

---

## Engineering reconstruction

### E — BBT authority is a pipeline, not one scalar comparison

Across the inspected sources, reconstruction of the operational BBT can be decomposed as:

```text
candidate placement / signature discovery
    -> candidate-media admissibility
    -> version comparison
    -> payload read / ECC validity
    -> choose working table
    -> rewrite stale or missing peer
```

This decomposition prevents `version` from silently absorbing responsibilities it does not perform.

### E — currentness metadata needs an interpretation rule

Retaining the version byte is not enough. A consumer must know how two values are compared, including what happens near numeric wrap. Linux's shift from the May-2004 ordinary numeric comparison to the released 2.6.12 signed-difference rule is direct historical evidence that **representation plus comparison semantics** jointly determine currentness.

Therefore:

> `retained currentness token` != `retained currentness meaning by itself`.

### E — higher/newer metadata is subordinate to candidate validity

The 2011 patch establishes a sharp ordering of checks. A table selected provisionally by version can later fail ECC validation, at which point its version must not be allowed to upgrade the surviving copy's authority label.

Therefore:

- `higher version` != `valid payload`;
- `version selected first` != `authority irrevocably established`;
- `version agreement after repair` != `proof that the rejected candidate had valid contents`.

### E — currentness and media qualification are recursive but distinct

Case 78 already showed that a BBT carries negative qualification state about ordinary NAND blocks. The 2021 patch adds the inverse dependency: the blocks that carry the BBT are themselves subject to media qualification before their retained control state should be trusted.

This does not create an infinite regress. The bounded implementation uses the NAND bad-block marker / scan path to reject an inadmissible BBT-host block, then uses the surviving BBT to reconstruct the broader block-qualification map.

Therefore:

> `BBT describes admissibility` does not imply `every BBT embodiment is automatically admissible`.

### E — version convergence is not history recovery

When a stale or missing peer is rewritten, the pair can converge again on one version and one current BBT image. Nothing in these sources implies recovery of every earlier BBT version, each bad-block discovery event, or the sequence of failed reconciliation attempts.

Therefore:

> `replica currentness repaired` != `event history reconstructed`.

---

## Functional comparisons — not genealogy

### A — Case 128, ZFS labels / uberblocks

Both regimes require a consumer to distinguish among multiple retained control-state candidates rather than assuming all surviving copies are equally current. The mechanisms remain different. ZFS uses its own checksum / transaction-generation / label structure; Linux MTD's bounded BBT path uses NAND placement, BBT signature/version state, ECC-read results, and bad-block qualification.

The comparison is limited to the function `choose an admissible current control-state representation`. It is not implementation genealogy.

### A — Synthesis 26, maintenance-control-state persistence horizons

The BBT version is long-lived maintenance-control state, but its persistence horizon alone does not create authority. Authority is conditional on the interpretation rule and on the candidate surviving the relevant validity checks. This adds a concrete Flash counterexample to any equation:

> `state survived restart` = `state remains authoritative`.

### A — distributed epochs / sequence numbers

It is tempting to call the BBT version an `epoch`, `term`, or distributed logical clock. Those labels are rejected here. The signed-difference expression is functionally comparable to finite sequence-number ordering, but the Linux MTD pair is not a consensus protocol and the sources do not establish descent from distributed-system sequence-number designs.

---

## Philosophical interpretation — bounded

### I — persistence of a sign does not guarantee persistence of its authority relation

The modest interpretive result is that a retained control mark can physically survive while losing, or failing to establish, the relation that makes it authoritative. A version byte only says `newer` inside a comparison regime; a BBT image only supplies exclusion authority if its carrier and contents remain admissible enough to be used.

This is not a claim that technical systems `remember how to remember`, and it is not a general theory of archival authority. It is a mechanism-specific observation:

> **continuity can depend on retaining both state and the bounded rules by which surviving representations are compared, rejected, and repaired.**

---

## Counterexamples and limits

- The 28-May-2004 CVS record is a public implementation floor, not an invention claim for BBT versioning or mirrored recovery.
- This slice does not identify the exact commit/date between May 2004 and Linux 2.6.12 at which the one-byte representation and signed-difference comparison first appeared; it establishes only a bounded chronology: ordinary numeric comparison in the inspected 2004 CVS diff, signed-difference comparison in the final 2.6.12 source by 17 June 2005.
- The `0xff -> 0x00` and half-range examples are engineering consequences of the inspected one-byte/signed-difference code, not quoted Linux design promises.
- The signed-difference rule does not by itself prove safety under arbitrarily large primary/mirror divergence.
- The 2011 patch demonstrates a source-level failure mode and repair; it is not a controlled power-cut or NAND fault-injection result.
- The 2021 patch establishes that bad BBT-host blocks can cause stale selection in the described rare case; it does not quantify field incidence.
- Version state is not treated as a cryptographic authenticator, checksum, transaction log, or complete failure history.
- None of these Linux sources prove behavior inside a managed SSD controller.
- No claim is made that Linux MTD invented cyclic sequence-number comparison; broader sequence-number, bootloader, DiskOnChip, NAND-controller, and BBT genealogy belongs primarily in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). A fresh repository search for `bad block table NAND BBT version` found no dedicated companion case to reuse in this round.

---

## Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| 28-May-2004 MTD CVS used ordinary numeric comparison between differing primary/mirror versions | H/P | grounded in archived CVS diff |
| the inspected 2004 code read/wrote the BBT version as little-endian integer state | H/P | grounded in archived CVS diff |
| Linux 2.6.12 stored the BBT version in one byte and used signed 8-bit difference for currentness selection | H/P | grounded in released source |
| one-byte signed-difference ordering can carry nearby currentness across `0xff -> 0x00` wrap | E | bounded reconstruction from released code |
| finite modular version != unlimited chronological sequence | E | bounded mathematical reconstruction |
| September-2011 patch deferred version propagation until a valid clean BBT copy was selected | H/P | grounded in linux-mtd patch; merge anchored in upstream commit |
| higher BBT version != valid BBT payload | E/H | directly motivated by 2011 counterexample |
| March-2021 upstream source skips bad BBT-host blocks to avoid selecting an obsolete table in a documented rare case | H/P | grounded in upstream commit |
| recognizable BBT candidate != admissible current BBT | E | bounded reconstruction |
| repairing version agreement != reconstructing bad-block event history | E | bounded reconstruction |
| this lineage proves managed-SSD BBT internals | X | unsupported |
| Linux invented BBT versioning or finite sequence arithmetic | X | not established |

---

## Sources

### Primary / contemporary

1. Linux MTD CVS archive, 28 May 2004, `nand_bbt.c` 1.9 -> 1.10: <https://lists.infradead.org/pipermail/linux-mtd-cvs/2004-May/003683.html>.
2. Linux v2.6.12 source, `drivers/mtd/nand/nand_bbt.c`, final release anchored at 17 June 2005: <https://github.com/torvalds/linux/blob/v2.6.12/drivers/mtd/nand/nand_bbt.c>.
3. Brian Norris, `[PATCH v2 11/14] mtd: nand: wait to set BBT version`, linux-mtd, 20 September 2011: <https://lists.infradead.org/pipermail/linux-mtd/2011-September/037965.html>.
4. Linux upstream merge `e0d65113a70f1dc514e625cc4e7a7485a4bf72df`, 7 November 2011, listing the BBT-version patch in the merged MTD series: <https://github.com/torvalds/linux/commit/e0d65113a70f1dc514e625cc4e7a7485a4bf72df>.
5. Linux upstream commit `bd9c9fe2ad04546940f4a9979d679e62cae6aa51`, 28 March 2021, `mtd: rawnand: bbt: Skip bad blocks when searching for the BBT in NAND`: <https://github.com/torvalds/linux/commit/bd9c9fe2ad04546940f4a9979d679e62cae6aa51>.

### Related repository

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — broad BBT / DiskOnChip / bootloader / controller genealogy and general finite-sequence-number history belong there; this addendum keeps only the retention-specific currentness/admissibility boundary.
