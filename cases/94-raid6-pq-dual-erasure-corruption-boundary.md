# RAID-6 P+Q: Dual-Erasure Reconstructability and the Corruption-Location Boundary

**Status:** `grounded`

## Scope

This case asks one bounded question:

> What additional retention relation is created by a second independent RAID syndrome, and what does that relation still fail to establish?

The historical/mechanism window is deliberately narrow:

- Chen et al.'s 1993 Berkeley RAID survey / 1994 ACM survey formulation of **P+Q redundancy (RAID Level 6)**;
- H. Peter Anvin's 2004–2011 Linux RAID-6 mathematics note;
- current Linux `raid6` recovery code as an implementation witness for recovery parameterized by known failed positions;
- the 1994 EVENODD publication as a prior-art/alternative-code boundary;
- current Linux MD documentation only as a later operational witness for parity-currentness limits.

This is **not** a general history of RAID-6, Reed–Solomon coding, EVENODD, RAID-Z, declustering, storage-controller products, rebuild policy, or modern erasure coding. Those broader histories belong in `computing-archaeology`; a repository search found no existing RAID-6/P+Q case there to reuse.

Case 17 already grounds single-missing-member parity reconstruction, degraded operation, parity currentness, and the difference between current service and restored redundancy. Case 94 adds the narrower **two-known-erasure** boundary and asks what extra information P+Q actually retains.

## Evidence labels and vocabulary

Historical vocabulary used by the sources:

- `P+Q redundancy`;
- `RAID Level 6`;
- `P` and `Q`;
- `Reed-Solomon`;
- disk failure / failed drive;
- Chen et al.'s `single self-identifying failure`.

Project engineering vocabulary used here:

- **known erasure** / **erasure-location knowledge** — a modern compact description for recovery when the missing positions are already known;
- **dual-erasure margin** — the ability of the bounded P+Q relation to reconstruct two known missing drive contributions;
- **fault-location prerequisite** — the distinction between knowing which positions are unavailable and diagnosing which apparently present positions are corrupt;
- **coded-currentness** — whether the retained data and syndromes still belong to one mutually consistent stripe state.

These project terms are engineering reconstructions (`E`). They are not attributed retroactively to every period source.

## Historical record

### H/P — Chen et al. 1993: P+Q as RAID Level 6

The Berkeley technical report *RAID: High-Performance, Reliable Secondary Storage* (UCB/CSD-93-778, November 1993), later published in *ACM Computing Surveys* in 1994, explicitly includes §3.2.7, **“P+Q Redundancy (RAID Level 6)”**.

The section begins from a useful historical boundary: ordinary parity corrects a **single self-identifying failure**. For larger arrays, the survey introduces a stronger P+Q redundancy code based on Reed–Solomon coding and describes protection against up to two disk failures with two redundant disks.

That wording matters. It does not establish that the array can infer the location of any arbitrary pair of silent corruptions merely because two redundant equations exist.

Chen et al. also make the maintenance cost visible: a small data update in P+Q must update both redundancy contributions, so the bounded survey counts six disk accesses for the small-write case. Extra reconstructability therefore adds update work; the second syndrome is not a passive duplicate that can be ignored until failure.

### H/P — Anvin 2004/2011: independent P and Q syndromes

H. Peter Anvin's Linux note *The mathematics of RAID-6* states the bounded design goal directly: RAID-6 supports loss of any two drives by computing two syndromes, **P** and **Q**.

In §2:

- **P** is the ordinary XOR syndrome familiar from RAID-5;
- **Q** is an independent Reed–Solomon / finite-field syndrome with position-dependent coefficients.

The point of retaining both is not “two copies of parity.” The two independent relations provide enough equations to solve for two missing data contributions **when their positions are known**.

### H/P — the two-data recovery equations explicitly assume the failed positions

Anvin's two-data-drive derivation writes the missing positions as `x` and `y` and treats them as known inputs to the recovery equations. The coefficients used to solve for the two unknown data blocks depend on those positions.

This supplies a concrete retention boundary:

> retaining P and Q is not sufficient by itself; recovery also depends on retaining or re-establishing the stripe/member-position relation and knowing which contributions are missing.

The physical disk identities can change during replacement, but the code-position relation cannot simply become ambiguous without changing the recovery problem.

### P — current Linux source preserves the same known-position interface

Current Linux source provides a useful implementation witness without being used as 2004 historical evidence. In `lib/raid/raid6/recov.c`, the dual-data recovery function receives explicit `faila` and `failb` positions. The recovery tables are selected from the positional difference and the individual failed indexes before both missing blocks are reconstructed.

This is not proof that all RAID-6 implementations share Linux internals. It is a source-level witness that the mathematical distinction is operational rather than merely expository.

### H/P — RAID-6 is not, in general, a dual-corruption locator

Anvin's diagnostic discussion provides the crucial counterexample. With one corrupt drive, recomputed syndromes can sometimes be used to identify a likely bad position. But the note explicitly warns that RAID-6 **cannot in general detect, much less recover from, arbitrary dual-disk corruption** when corruption locations are not already known. In an ambiguous same-byte-position case, automated “repair” can even damage a third drive if it guesses the wrong source of truth.

This is the strongest boundary in the case:

**two-known-erasure reconstructability ≠ arbitrary two-corruption diagnosis/recovery**.

The code carries additional algebraic information. It does not automatically carry all the epistemic information required to decide *which* surviving-looking embodiment should be distrusted.

### P — current Linux MD keeps parity currentness separate from coding strength

Linux MD documentation separately refuses normal startup of a RAID5/RAID6 array that is both **dirty and degraded**, because dirty state means parity cannot be trusted while degraded state means some data blocks are missing and therefore cannot be reliably reconstructed from untrusted parity.

This later operational witness prevents another overclaim:

**two syndromes ≠ crash-atomic/current parity**.

Case 88 already treats the write-hole/recovery-evidence problem. Case 94 does not re-open it; it uses the MD rule only to show that adding Q does not abolish the need to know whether the coded relation is current.

## What has to remain

For the bounded P+Q recovery relation, later reconstruction can depend on more than “some bytes survived”:

1. the surviving current data contributions;
2. the current P syndrome;
3. the current Q syndrome;
4. the stripe/member ordering that gives Q its position-dependent coefficient relation;
5. the identity/positions of contributions known to be unavailable for the recovery operation;
6. enough currentness/array state to reject stale or inconsistent redundancy;
7. repair progress / replacement state if the system is to know whether the full dual-failure margin has been restored.

Items 4–7 are not user payload. They are constitutive control/admissibility relations around the coded payload.

## Mechanism reconstruction

A compact engineering reconstruction is sufficient here.

For data contributions \(D_i\):

- `P` behaves as the XOR of the data contributions;
- `Q` is a distinct weighted finite-field sum whose coefficient depends on position `i`.

If one data contribution is missing and ordinary parity is available, P alone can reconstruct it. If two data contributions at known positions `x` and `y` are missing, the remaining P/Q relations provide two independent equations for the two unknown values.

The independence of P and Q is therefore the retained technical resource. The fact that the coefficients are position-dependent is why the code-position relation is also constitutive.

This reconstruction deliberately stops before a general tutorial on Galois-field arithmetic.

## Maintenance and failure boundaries

### Updating one value creates two redundancy obligations

A current logical write changes the data contribution and, in the P+Q regime, both syndrome relations. Chen et al.'s small-write accounting makes that cost explicit.

**more reconstruction margin ≠ free redundancy**.

### Known loss and unknown corruption are different fault models

A missing drive normally supplies its own location as part of the failure condition: the system knows which member is absent. Silent corruption can leave every drive present while making the location of the bad information uncertain.

The same two equations face different unknowns in those two regimes.

**number of parity equations ≠ number of arbitrary faults that can always be diagnosed**.

### A first failure consumes margin even when service continues

After one known member loss, a bounded P+Q array can still possess enough independent information to reconstruct another known missing contribution. But it no longer has the same future-failure margin as the fully repaired array.

So Case 17's distinction survives at a stronger code distance:

**degraded service continuity ≠ restored redundancy margin**.

### Stale parity can defeat algebra that is otherwise correct

If P/Q no longer describe the same current stripe state as the surviving data, solving the equations faithfully can produce the wrong answer.

**algebraic solvability ≠ coded-currentness**.

### Dual parity does not close the write hole

P+Q increases the number of independent coded constraints. It does not make several member writes atomic across sudden power loss.

That is why Case 88 remains a separate recovery-order/durability case.

## Prior art and genealogy boundary

### Chen et al. do not establish universal invention priority

The 1993 Berkeley survey is a strong period anchor for the explicit **P+Q / RAID Level 6** formulation used here. This case does not promote that publication date into a universal “invention of double-parity arrays” claim.

### EVENODD demonstrates algorithm plurality

Blaum, Brady, Bruck, and Menon's 1994 EVENODD paper describes another scheme that tolerates up to two disk failures with two redundant disks using XOR computations, contrasting it with the then-known Reed–Solomon approach.

For this repository, EVENODD establishes only a prior-art boundary:

**RAID-6 / two-disk-failure protection ≠ necessarily P+Q Reed–Solomon implementation**.

A full coding genealogy belongs in `computing-archaeology`.

## Cross-case comparison

| Comparison | Status | What carries across | What must not be collapsed |
| --- | --- | --- | --- |
| Case 17 RAID parity reconstruction | `A/E` | coded reconstruction, degraded service, repair margin, parity currentness | one-known-failure XOR parity is not the two-syndrome P+Q regime |
| Case 18 ZFS scrub | `A` | integrity evidence can be required before repair authority | proactive corruption detection is not the same operation as solving known erasures |
| Case 19 Facebook f4 | `A` | Reed–Solomon-coded recoverability without full replicas | distributed failure-domain placement and object reconstruction differ from local RAID-6 P+Q |
| Case 24 Azure LRC | `A` | recovery cost depends on code dependency structure | LRC locality and cloud extent handoff are different code/system semantics |
| Case 27 Ceph EC scrub | `A` | coded surviving fragments still need integrity/currentness qualification | Ceph's scrub-authority protocol is not Linux/Chen RAID-6 |
| Case 88 Linux MD PPL | `A` | coded redundancy still depends on crash-safe currentness/order evidence | PPL write-hole closure is not an additional parity equation |

No direct historical genealogy is inferred among these systems.

## Philosophical interpretation

`I` — The case is useful because it makes “more retained information” visibly **typed**. A second syndrome expands the class of missing-state relations that can be reconstructed, but only inside a fault model in which missing positions and currentness are sufficiently known.

`I` — This supports the repository's target-relative notion of retention: later continuation depends not only on the quantity of surviving material but on which relations remain admissible for the future recovery operation.

These are project interpretations, not claims made by Chen, Anvin, or Linux developers as philosophical theses.

## Claim ledger

| Claim | Label | Support | Limit |
| --- | --- | --- | --- |
| Chen et al. present P+Q as RAID Level 6 and protection against up to two disk failures | `H/P` | Berkeley report §3.2.7 | not universal invention priority |
| P and Q are independent syndromes, with Q using Reed–Solomon finite-field arithmetic | `H/P` | Anvin §2 | bounded Linux P+Q formulation |
| two missing data contributions are solved using known failed positions | `H/P/E` | Anvin two-data derivation | does not prove all controllers expose the same API |
| Linux dual-data recovery takes explicit failed indexes | `P` | current `lib/raid/raid6/recov.c` | current implementation witness, not 2004 source identity |
| arbitrary dual-disk corruption is not generally detectable/recoverable by RAID-6 alone | `H/P` | Anvin diagnostic section | does not deny additional checksums/scrub/metadata can help |
| dirty+degraded RAID5/6 can have untrustworthy parity and unreconstructable missing data | `P/E` | Linux MD admin guide | current Linux operational boundary, not 1993 history |
| P+Q is not two replicas | `E` | source mechanism comparison | project reconstruction |
| failure-location knowledge can be constitutive recovery state | `E` | positional equations + Linux `faila/failb` | project vocabulary |
| dual parity does not itself close the write hole | `E/A` | Cases 17/88 + Linux currentness boundary | no claim about every controller implementation |
| EVENODD is an alternative two-redundant-disk scheme | `H/P` | IBM Research 1994 record | used only to block one-algorithm/invention story |

## Sources

### Primary / contemporary

1. Peter M. Chen, Edward K. Lee, Garth A. Gibson, Randy H. Katz, and David A. Patterson, **“RAID: High-Performance, Reliable Secondary Storage,”** UCB/CSD-93-778, November 1993; especially §3.2.7 “P+Q Redundancy (RAID Level 6)”.
   - Berkeley record: <https://www2.eecs.berkeley.edu/Pubs/TechRpts/1993/6306.html>
   - archived report PDF: <https://www2.eecs.berkeley.edu/Pubs/TechRpts/1993/Archive/CSD-93-778.pdf>

2. H. Peter Anvin, **“The mathematics of RAID-6,”** first version 20 January 2004, last updated 20 December 2011.
   - <https://www.kernel.org/pub/linux/kernel/people/hpa/raid6.pdf>
   - especially printed pp. 3–4 for P/Q and two-data recovery; printed p. 8 for the dual-corruption diagnostic limit.

3. Linux kernel, **`lib/raid/raid6/recov.c`**, current source snapshot used only as an implementation witness.
   - <https://github.com/torvalds/linux/blob/4d7d9486c04d917265f64c55bd23b2cc4fe7749c/lib/raid/raid6/recov.c>

4. Mario Blaum, Jim Brady, Jehoshua Bruck, and Jai Menon, **“EVENODD: An optimal scheme for tolerating double disk failures in RAID architectures,”** ISCA 1994, 18 April 1994.
   - IBM Research record: <https://research.ibm.com/publications/evenodd-an-optimal-scheme-for-tolerating-double-disk-failures-in-raid-architectures>

### Later institutional / operational witness

5. Linux kernel documentation, **“RAID arrays”**, section “Boot time assembly of degraded/dirty arrays”.
   - <https://www.kernel.org/doc/html/next/admin-guide/md.html>

## Open work kept outside this case

- full RAID-6 / P+Q / EVENODD / Reed–Solomon invention genealogy;
- exact production-controller implementations and crash semantics;
- RAID-Z, dRAID, declustered parity, and modern array layouts;
- rebuild throttling and URE-aware rebuild policy;
- checksummed RAID-6 fault-location/repair protocols;
- independent hardware fault injection;
- performance comparison among modern RAID-6 implementations;
- secure deletion / forensic behavior of reconstructed or retired members.

Those are separate research slices rather than blockers for this case's bounded mechanism claim.
