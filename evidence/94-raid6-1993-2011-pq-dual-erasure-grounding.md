# Grounding record — RAID-6 P+Q dual-erasure reconstructability and corruption-location boundary, 1993–2011

**Case:** [`cases/94-raid6-pq-dual-erasure-corruption-boundary.md`](../cases/94-raid6-pq-dual-erasure-corruption-boundary.md)  
**Status:** `grounded`  
**Scope:** period P+Q/RAID-6 taxonomy and mechanism; Linux mathematical/implementation witness; explicit boundary between known missing positions and unknown corruption locations.

## Research question

What exactly does the second RAID syndrome add to recoverability, and what additional retained relations are still needed before that algebra can authorize a correct recovery?

The evidence is intentionally selected to distinguish four layers:

1. **historical record** — period P+Q / RAID Level 6 / double-disk-failure vocabulary;
2. **engineering reconstruction** — two independent equations solve two missing values only when the relevant positions/currentness relation is known;
3. **functional comparison** — comparison to RAID5, scrub, distributed erasure coding, and PPL;
4. **interpretation** — the repository-level claim that redundancy is failure-model-relative information.

No philosophical interpretation is used to raise evidence maturity.

---

## Source A — Chen et al., UCB/CSD-93-778 (1993)

**Type:** `P/H` — contemporary academic technical report; later published in *ACM Computing Surveys* 26(2), 1994.  
**Record:** <https://www2.eecs.berkeley.edu/Pubs/TechRpts/1993/6306.html>  
**PDF:** <https://www2.eecs.berkeley.edu/Pubs/TechRpts/1993/Archive/CSD-93-778.pdf>

### Locator

- §3.2.7 — **“P+Q Redundancy (RAID Level 6)”**.
- The Berkeley record dates UCB/CSD-93-778 to **1993** and describes the report as covering RAID levels 0–6.

### Claims supported

- the source explicitly names a `P+Q` RAID Level 6 organization;
- the section contrasts ordinary parity's ability to correct a **single self-identifying failure** with stronger coding needed as multiple failures become plausible;
- P+Q uses a Reed–Solomon-style redundancy relation to protect against up to two disk failures with two redundant disks;
- a small write has to update both redundancy components and carries higher access cost (the survey's bounded small-write accounting is six disk accesses).

### What the source does not prove here

- that Chen et al. invented every double-parity/two-failure disk-array scheme;
- that all later RAID-6 uses the same P+Q implementation;
- that two parity symbols automatically locate arbitrary silent corruption;
- any one controller's power-fail atomicity.

The phrase `single self-identifying failure` is retained because it is historically useful: the source itself distinguishes a failure whose location is identified from a generic unknown-error problem.

---

## Source B — H. Peter Anvin, *The mathematics of RAID-6* (2004/2011)

**Type:** `P/H` — Linux technical note by the RAID-6 implementation author.  
**PDF:** <https://www.kernel.org/pub/linux/kernel/people/hpa/raid6.pdf>  
**Version line:** first version **20 January 2004**, last updated **20 December 2011**.

The PDF was directly inspected, not merely cited from a search-result snippet.

### Locator B1 — printed p. 1

The introduction states the bounded requirement: RAID-6 should survive loss of any two drives and therefore computes two syndromes, `P` and `Q`.

**Supports:**

- the dual-drive-loss target;
- P/Q as two separately named syndromes.

### Locator B2 — §2, printed p. 3

The note defines:

- `P` as the ordinary XOR syndrome;
- `Q` as a Reed–Solomon finite-field syndrome with powers/coefficients tied to data position.

**Supports:**

- `P ≠ Q`;
- the second redundancy relation is algebraically independent rather than a second full replica or a duplicate P block;
- disk/stripe position participates in the Q interpretation.

### Locator B3 — printed p. 4, “Recovering from a two-data-drive failure”

The derivation names missing positions `x` and `y`, and states that `x`, `y`, the surviving syndrome values, and the surviving data relation are known before solving for the two missing data contributions.

**Supports:**

- the **known-position prerequisite**;
- `erasure-location knowledge can be constitutive recovery state`;
- two independent equations can recover two missing data values under that prerequisite.

The word `erasure` is project engineering vocabulary. The historical note speaks in terms of failed/lost drives and known indexes.

### Locator B4 — diagnostic discussion, printed p. 8

The note explicitly warns that RAID-6 by itself cannot in general detect, much less recover from, dual-disk corruption. It further warns that ambiguous corruption in corresponding byte positions can lead an automated implementation to damage another drive if it attempts an unjustified correction.

**Supports:**

- `two known drive losses ≠ arbitrary two-drive corruption recovery`;
- `successful algebraic reconstruction ≠ fault diagnosis`;
- recovery authority depends on evidence about which embodiment is bad, not merely on the number of surviving syndrome bytes.

### Boundary

This note explains one Linux P+Q formulation. It is not used as a universal definition of every technology sold as “RAID-6”.

---

## Source C — Linux `lib/raid/raid6/recov.c`

**Type:** `P` — current source-code implementation witness, **not** a period source for 1993/2004 history.  
**Pinned snapshot:** <https://github.com/torvalds/linux/blob/4d7d9486c04d917265f64c55bd23b2cc4fe7749c/lib/raid/raid6/recov.c>

### Direct implementation witness

The file's header describes `RAID-6 data recovery in dual failure mode`.

The scalar dual-data recovery routine is:

`raid6_2data_recov_intx1(int disks, size_t bytes, int faila, int failb, void **ptrs)`

The implementation:

- receives `faila` and `failb` explicitly;
- temporarily substitutes zero pages for the missing data positions while generating syndromes;
- chooses finite-field multiplier tables using the failed indexes / their positional difference;
- reconstructs the two missing blocks.

### Claims supported

- Linux operationalizes the same known-position recovery distinction;
- positional identity is an input to reconstruction rather than incidental explanatory prose.

### Boundary

This current source is not evidence that the exact same code existed in 2004, nor that every Linux RAID-6 SIMD implementation uses the identical scalar routine internally.

---

## Source D — EVENODD, IBM Research / ISCA 1994

**Type:** `P/H` — contemporary conference-publication record.  
**Record:** <https://research.ibm.com/publications/evenodd-an-optimal-scheme-for-tolerating-double-disk-failures-in-raid-architectures>  
**Date:** **18 April 1994**.

IBM's abstract describes EVENODD as tolerating up to two disk failures with only two redundant disks and simple XOR computation, while contrasting it with the existing optimal-storage Reed–Solomon approach requiring finite-field computation.

### Claims supported

- by 1994, a two-redundant-disk/two-failure scheme existed that was not the same Reed–Solomon P+Q mechanism;
- therefore `two-disk-failure RAID ≠ necessarily P+Q Reed–Solomon`;
- the Chen/Anvin mechanism must not be promoted into a universal algorithm definition or invention-priority claim.

### Boundary

This record is used only as a prior-art/algorithm-plurality witness. The detailed EVENODD layout, proof, implementation history, and genealogy remain outside this case.

---

## Source E — Linux MD “dirty + degraded” operational boundary

**Type:** `P/S` — current Linux kernel institutional documentation, used only as a later operational witness.  
**URL:** <https://www.kernel.org/doc/html/next/admin-guide/md.html>  
**Section:** “Boot time assembly of degraded/dirty arrays”.

The documentation says a RAID5 or RAID6 array that is both dirty and degraded can have undetectable data corruption: dirty state means parity cannot be trusted, while degraded state means data blocks are missing and cannot reliably be reconstructed from that parity. Linux therefore normally refuses startup without explicit override.

### Claims supported

- stronger coding does not abolish parity/syndrome **currentness** as a prerequisite;
- physical survival of parity bytes does not imply those bytes are admissible reconstruction evidence;
- coding strength and crash/update consistency are distinct relations.

### Boundary

This is not back-projected into Chen et al. 1993 as historical vocabulary, and it does not replace the separate write-hole evidence in Cases 17 and 88.

---

## Related-repository audit

Searched `tmzncty/computing-archaeology` for RAID / RAID-6 / P+Q / parity-disk material before opening this case. No existing bounded RAID-6/P+Q technical-history case was found.

Routing decision:

- **this repository:** the retention-specific distinction between known-erasure reconstructability, syndrome/currentness state, and corruption-location uncertainty;
- **computing-archaeology:** full RAID-6 genealogy, coding-family development, controller/product history, disk-array architecture chronology, and implementation lineage.

This avoids manufacturing a broad storage-history chapter inside `technical-retention`.

---

## Evidence-backed reconstruction

### R1 — P+Q retains two independent coded constraints

`E`, grounded in Sources A/B.

The user data are not copied twice. P and Q retain two different equations over the current stripe. This increases the number of missing contributions that can be solved under the assumed failure model.

### R2 — failure location is part of the recovery relation

`E`, grounded in Sources B/C.

The two-data recovery problem is parameterized by `x/y` or `faila/failb`. The source set therefore permits the project statement:

> a code can retain enough payload redundancy while still depending on separate retained/re-observed information about **where** the loss occurred.

This is not application payload or complete event history.

### R3 — known erasures and unknown corruptions are different unknown sets

`E`, grounded in Source B.

For two missing drives, locations are known and the unknowns are the missing values. With arbitrary silent corruption, both the bad locations and bad values may be unknown. The same two syndromes therefore do not imply the same recoverability.

### R4 — syndrome currentness is prior to trustworthy reconstruction

`E/A`, grounded in Source E and Cases 17/88.

The algebra assumes P/Q belong to the same current stripe relation as the surviving data. If the array is dirty/inconsistent, retaining the syndrome bytes is insufficient.

### R5 — full failure margin returns after repair, not merely after successful degraded I/O

`E/A`, grounded in Case 17 plus the two-failure margin in Sources A/B.

One known failure consumes one of the bounded code's tolerable missing contributions even when current reads can still be served or reconstructed.

---

## Explicit rejected / unsupported claims

| Rejected claim | Reason |
| --- | --- |
| `RAID-6 always means Reed–Solomon P+Q` | EVENODD supplies a contemporary alternative double-failure code |
| `Chen et al. invented all double-parity RAID` | bounded sources do not establish universal invention priority |
| `two parity disks are two replicas` | P/Q are coded relations over stripe data, not full duplicates |
| `RAID-6 automatically fixes the RAID write hole` | coding strength and cross-member update/currentness semantics are separate; Linux dirty+degraded boundary and Case 88 prevent this inference |
| `two parity syndromes detect and repair any two corrupt disks` | Anvin explicitly rejects the general dual-corruption claim |
| `the largest surviving set is automatically authoritative` | currentness/fault-location evidence can disqualify physically present state |
| `successful reconstruction proves the chosen failure diagnosis was correct` | Anvin's diagnostic warning supplies a direct counterexample |
| `erasure` is Chen et al.'s universal historical term for this case | retained as project engineering shorthand; period sources use failed/self-identifying failure vocabulary |
| `current Linux recov.c is the exact 2004 code` | used only as a present implementation witness |
| `two-failure tolerance implies three-failure tolerance` | outside the two-syndrome bounded model and unsupported |

---

## Cross-case boundaries

### Case 17 — RAID parity reconstruction

Case 17 remains the canonical single-parity / one-known-failure reconstruction case and already grounds:

- parity currentness;
- demand reconstruction;
- degraded service versus completed repair;
- reconstruction progress.

Case 94 should not duplicate that history. It adds only the second independent syndrome and the known-erasure / unknown-corruption distinction.

### Case 18 — proactive scrub

Scrub can help discover latent corruption while redundancy still exists. That is **functional comparison**, not a substitute for P+Q algebra. A code can be able to reconstruct a *known* missing member without being able to diagnose arbitrary hidden corrupt members.

### Cases 19 / 24 / 27 — distributed erasure coding

They are comparative evidence that coded recoverability composes with placement, locality, integrity qualification, and repair authority. They do not establish direct genealogy into or out of Linux RAID-6.

### Case 88 — Linux MD PPL

PPL addresses crash-time parity-currentness/write-hole evidence in RAID5. It is a useful boundary precisely because Case 94's extra syndrome does not make multi-device updates atomic.

---

## Maturity decision

`grounded` is justified for this bounded slice because it has:

- a contemporary 1993 Berkeley RAID Level 6/P+Q source;
- a directly inspected Linux RAID-6 mathematics note with exact P/Q, two-data, and dual-corruption boundary locators;
- a source-code implementation witness with explicit failed-position inputs;
- a contemporary alternative-code witness preventing algorithm/invention overclaim;
- a current institutional parity-currentness counterexample;
- an explicit related-repository duplication audit;
- typed historical / engineering / analogy / interpretation boundaries.

The case is **not** mature enough to support a universal RAID-6 history or a claim about every commercial controller.

---

## Remaining open work

1. Full RAID-6 / Reed–Solomon / EVENODD / later coding genealogy.
2. Production-controller crash semantics and write-cache behavior.
3. RAID-Z/dRAID and checksummed multi-parity source-selection semantics.
4. Rebuild throttling, URE-aware policy, and large-drive reliability evolution.
5. Independent double-failure / silent-corruption fault injection on named systems.
6. Exact historical transition from research RAID Level 6 terminology to standardized/product naming.

These are separate future slices, not blockers for the present claim.
