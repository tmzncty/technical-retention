# Case 140 — IBM Double-Disk-Failure Array Codes: Retaining a Second Failure Margin

**Status:** grounded  
**Claim layer:** historical record + engineering reconstruction + bounded functional analogy  
**Primary regime:** 1991–1995 IBM disk/DASD-array coding for up to two unavailable members and the adjacent error-vs-erasure recovery boundary  
**Evidence:** [`../evidence/140-ibm-1991-1994-double-disk-array-codes-grounding.md`](../evidence/140-ibm-1991-1994-double-disk-array-codes-grounding.md) · [`../evidence/140-ibm-1991-1995-erasure-error-budget-deepening.md`](../evidence/140-ibm-1991-1995-erasure-error-budget-deepening.md)

## Summary

Case 17 established the repository's bounded single-parity RAID relation: after one member fails, the logical data may still be reconstructable while the array has entered a degraded state and has largely spent the failure margin that single parity provided.

This case asks the next narrow question:

> **What changes when the coding relation is explicitly designed to survive up to two unavailable disks rather than one?**

The inspected early-1990s IBM record gives three useful anchors:

1. an IBM patent family with a **1991-02-11 priority** and **1992-08-19 EP publication** for encoding and rebuilding up to two unavailable DASDs;
2. Mario Blaum's **IEEE ICC 1992** paper describing protection against two disk failures with two redundant disks and XOR-only coding;
3. the **ISCA 1994 / journal 1995 EVENODD** line, explicitly framed for RAID architectures, again tolerating up to two disk failures with two redundant disks and XOR operations.

The retention-specific result is not merely "more parity." It is a different temporal margin:

`healthy coded array → one member unavailable → payload still reconstructable AND one additional member-failure margin remains → repair/rebuild → full designed margin restored`

That remaining margin exists in the **relation among surviving fragments and parity constraints**, not in a second full copy of the payload.

The later deepening adds a second distinction. IBM US5351246A explicitly gives a different recovery budget for **known unavailable DASDs / erasures** than for **one DASD in error**. In the cited construction, one erroneous DASD consumes redundancy equivalent to two parity DASDs because the errant unit must be identified and corrected. Therefore:

`same physical parity bytes != same usable recovery margin under different fault-location uncertainty`

The case deliberately does **not** call every 1991–1995 disclosure `RAID-6`. Later RAID-6 terminology is used only for functional comparison. Source-era wording and later category names remain separate.

## Research questions

1. What did early IBM disk-array sources actually claim about surviving two unavailable members?
2. How does two-failure reconstructability differ from Case 17's single-parity degraded mode?
3. Does "two redundant disks" mean two replicas? No — what relation is actually retained?
4. Is mathematical reconstructability the same thing as completed repair? No — what margin remains while degraded?
5. How does a located unavailable member differ from a still-present but erroneous DASD?
6. Does a two-disk-failure scheme automatically detect arbitrary silent corruption? No — where is the error/erasure boundary?
7. Can the later term `RAID-6` be projected backward into 1991–1995? Not without source-era evidence.
8. What belongs here versus broader coding/RAID genealogy in `computing-archaeology`?

## Source ladder

| Evidence | Date | Strength | Use here |
|---|---:|---|---|
| IBM patent family EP0499365A2 / US07/653,596 | priority 1991-02-11; EP publication 1992-08-19 | `H/P*` | up-to-two unavailable DASDs, row/diagonal simple parity, spare rebuild, degraded/reconstruction vocabulary |
| Mario Blaum, IEEE ICC 1992, IBM Research record | 1992-06-14 | `H/P` | explicit two-disk-failure protection, two redundant disks, XOR-only coding |
| IBM US5351246A | 1991 lineage; publication 1994-09-27 | `H/P*` | explicit distinction between unavailable DASDs / erasures and one DASD in error; different parity-redundancy budget |
| Blaum et al., EVENODD, ISCA 1994 / IEEE TC 1995 institutional records | 1994–1995 | `H/P` | named two-failure RAID-architecture scheme; two redundant disks; XOR implementation; abstract-level one-column-in-error decoder |
| Plank, FAST 2008 / USENIX | 2008 | later scholarly context | explicit later RAID-6 `k+2` / any-two-device functional category only |

`H/P*` means the patent is a primary public record inspected through a public mirror rather than an origin-host facsimile.

## Historical record

### 1. The 1991 date is a priority floor, not a public-disclosure claim

EP0499365A2 records a **1991-02-11 priority date** and an **EP publication date of 1992-08-19**. Its family points to U.S. application 07/653,596 / later US5271012A.

The document describes an `(M-1) × M` logical data array encoded with paired simple parity relations along row/diagonal paths so that data can be rebuilt when **up to two DASDs fail**. Reconstructed data may be written back onto spare DASD capacity.

This chronology must be stated carefully:

- `1991 priority/family record != demonstrated public availability in 1991`;
- the inspected EP publication is public in 1992;
- the separately published ICC paper below is dated June 1992.

No product shipment follows merely from a patent-family record.

### 2. ICC 1992 explicitly states the two-failure / two-redundancy relation

IBM Research's record for Mario Blaum's *A coding technique for recovery against double disk failures in disk arrays* dates the IEEE ICC paper to **1992-06-14**.

Its abstract states that the array is protected against **two disk failures**, requires **two redundant disks**, and uses exclusive-OR operations for encoding and decoding, contrasted with finite-field approaches such as Reed–Solomon.

The source therefore directly establishes a two-member-failure target and redundancy quantity. It does **not** establish two complete replicas, a named shipping implementation, or contemporary use of the term `RAID-6`.

### 3. EVENODD in 1994–1995 is explicitly a RAID-architecture scheme

IBM Research dates the ISCA 1994 paper *EVENODD: An optimal scheme for tolerating double disk failures in RAID architectures* to **1994-04-18**. The 1995 IEEE Transactions on Computers article, *EVENODD: An Efficient Scheme for Tolerating Double Disk Failures in RAID Architectures*, provides the fuller journal publication record.

The institutional abstracts say EVENODD:

- tolerates up to two disk failures;
- adds only two redundant disks;
- uses simple XOR computations;
- can reuse parity hardware of the kind typically present in RAID-5 controllers;
- is compared against Reed–Solomon approaches that also use two extra disks but require finite-field operations.

The 1995 journal abstract additionally states that the paper presents a decoding algorithm for **one column (track) in error**.

Two historical cautions are mandatory.

First, source-era `first known` / optimality wording remains an **authors' scoped claim**, not an independently proven universal invention priority. The abstract itself acknowledges prior Reed–Solomon-based optimal-storage approaches.

Second, "can be implemented" with RAID-5 parity hardware is not evidence that any named RAID-5 controller shipped EVENODD support. Hardware primitive compatibility and deployed controller semantics are different claims.

### 4. US5351246A makes the error/erasure budget explicit

US5351246A, assigned to IBM and published **1994-09-27**, distinguishes two fault models.

For unavailable DASDs / erasures, it states that up to `R` unavailable DASDs can be rebuilt where `R <= P`, with `P` parity DASDs.

For **one DASD in error**, it states that the erroneous DASD can be corrected in the presence of up to `R-2` unavailable DASDs, again with `R <= P`. The patent explicitly explains that the DASD-in-error case requires redundancy equivalent to **two parity DASDs to identify and correct the errant unit**.

The patent also distinguishes `data error` from `erasure` in its definitions. That makes the distinction source-grounded rather than a later repository invention.

This document is historically adjacent to the IBM array-code record used by Case 140, but this case does **not** assert:

`US5351246A == EVENODD`

The bounded claim is only that contemporaneous IBM coded-array work explicitly treated unknown-error correction as a different redundancy budget from known unavailable-member recovery.

## Engineering reconstruction

### A. One parity relation and two missing members are different equations

For the single-parity relation in Case 17, a stripe with one missing member has one unknown and one independent parity relation. Reconstruction is possible from the surviving members.

With two arbitrary missing members, ordinary single parity leaves two unknown member values constrained by only one parity relation. The missing values are not uniquely determined in general.

The early IBM two-failure schemes add additional independent coding structure so that the stated pair of unavailable members remains reconstructable under the code's assumptions.

Therefore:

`one-failure parity relation != two-failure coding relation`

This is an engineering reconstruction of the cited mechanism, not a historical claim that all implementations use the same equations.

### B. Two redundant disks are not two copies

A particularly important stop condition is:

`two redundant disks != two complete replicas`

The redundant members store coding relations derived from multiple data members. The protected state is distributed across data and coded fragments. The future ability to reconstruct exists because the surviving set still satisfies enough independent relations, not because two whole copies of each object exist somewhere.

### C. After the first failure, some future-failure margin can remain

If a code is specified to tolerate **up to two located unavailable members**, then after the first member becomes unavailable, one additional member can disappear while the current logical payload remains reconstructable within that stated model.

That gives a useful contrast with Case 17:

- **single-parity Case 17:** first failure can leave data reconstructable but consumes the protection relation's ordinary same-domain one-member failure margin;
- **Case 140 two-failure code:** first failure can leave data reconstructable **and** retain one additional member-failure margin.

This does not make the degraded state equivalent to healthy state. After the first failure the system has less margin than its designed maximum. Repair still matters because rebuilding onto a spare returns the coded object toward its full physical redundancy embodiment.

Hence:

`recoverable now != full designed failure margin != repair complete`

### D. Coding capability and rebuild policy remain separate

The patent-family text discusses spare substitution and rebuilding, including scheduled or opportunistic reconstruction. But nothing about a two-failure code by itself determines:

- rebuild rate;
- foreground I/O share;
- wall-clock exposure;
- controller retry policy;
- exact progress checkpoint persistence;
- what happens under every crash during rebuild.

Those are separate maintenance-policy questions. Case 136 is the repository's clearer controller-policy example.

`can reconstruct two failures != has a particular rebuild scheduler`

### E. Erasure-location knowledge changes the usable recovery budget

The deeper IBM patent record makes the earlier error boundary more precise.

Let:

- `P` be the number of parity DASDs;
- `U` be known unavailable DASDs present in the recovery problem.

At the level stated by US5351246A:

```text
known unavailable / erasure case:
    U <= P

one DASD in error + known unavailable case:
    U <= P - 2
```

The engineering interpretation is straightforward but important.

For a known unavailable member, the decoder already knows **which coordinate is missing** and solves for its value.

For a still-present but erroneous DASD, the recovery relation must also establish **which coordinate is the errant source**. In the patent's construction, that identification-plus-correction problem consumes redundancy equivalent to two parity DASDs.

Therefore:

`same stored parity budget + different fault-location knowledge != same recoverability`

This is not merely an abstract coding-theory distinction. It changes the future recovery margin of the stored array without changing how many parity devices physically exist.

### F. The `P = 2` boundary

With two parity DASDs, the patent's stated bounds imply:

```text
P = 2

up to two known unavailable DASDs
    OR
one DASD in error with no additional unavailable DASD under the cited bound
```

The cited evidence therefore does **not** authorize the stronger statement:

`P = 2 -> one unknown error + one erasure is recoverable`

That combination is outside the patent's stated `U <= P - 2` mixed bound.

This sharpens the canonical rule:

`double-disk-failure tolerance != arbitrary silent-corruption correction`

into:

`known-erasure margin != unknown-error margin`

### G. Error correction still is not arbitrary silent-corruption handling

The new evidence narrows one previous stop condition but does not remove it.

US5351246A establishes a specific **one-DASD-in-error** model. The 1995 EVENODD abstract advertises a **one-column (track) in error** decoder.

It still does not follow that these schemes automatically:

- discover every silently corrupted sector inside an otherwise responsive drive;
- correct arbitrary multiple unknown errors;
- distinguish every stale-but-checksum-consistent state from current state;
- replace scrub, end-to-end checksums, or controller/media ECC;
- solve parity currentness after an interrupted update.

Thus:

`one coded-column error model != arbitrary corruption model`

### H. Physical redundancy and recovery authority are not identical

The deepened case needs four distinct predicates:

```text
P1: coded parity bytes physically survive
P2: those relations correspond to the current protected data state
P3: failed / errant coordinates are known or locatable under the code model
P4: enough independent redundancy remains to solve the requested recovery problem
```

Physical survival of parity can satisfy `P1` while the system still lacks `P3` or `P4` for a harder fault model.

Therefore:

`parity physically present != parity sufficient for this recovery problem`

## Terminology and prior-art boundary

### Source-era language

The inspected sources use:

- `double disk failures`;
- `up to two unavailable DASDs`;
- `data error` and `erasure` in US5351246A;
- `one DASD in error`;
- `one column (track) in error` in the 1995 EVENODD abstract;
- `RAID architectures` in the EVENODD title/abstract.

They do not, in the inspected material, establish that the exact label `RAID-6` was their own term for the 1991–1995 schemes.

### Later RAID-6 comparison

Plank's FAST 2008 USENIX paper explicitly describes RAID-6 as a `k+2` storage arrangement designed to tolerate any two device failures and discusses two coding devices conventionally called `P` and `Q`.

That supplies a later functional category:

`early two-failure array code ~ later RAID-6 any-two-device reconstructability`

But `~` here means **functional analogy**, not direct genealogy or retroactive nomenclature.

The broader history of Reed–Solomon array use, EVENODD, RDP, controller adoption, the `RAID-6` name, and standards belongs in `tmzncty/computing-archaeology` if pursued. A fresh companion-repository search found no dedicated EVENODD study to reuse during this deepening.

## Cross-case comparison

### Case 17 — one-failure parity reconstruction

Both cases separate **service continuity** from **repair completion**. The difference is the residual margin after the first member loss.

| Relation | Case 17 single parity | Case 140 two-failure code |
|---|---|---|
| Healthy protection target | one unavailable member | up to two unavailable members |
| After first member loss | payload can remain reconstructable | payload can remain reconstructable |
| Same-domain additional member-loss margin | ordinarily exhausted | one additional member remains within stated code target |
| Need to rebuild/repair | yes | yes |
| Rebuild means secure erase | no | no |

This is a functional contrast, not a claim that every two-failure implementation is literally "RAID-5 plus another parity disk."

### Case 94 — RAID-6 P/Q corruption boundary

Case 94 provides a later functional comparison: redundant equations that are sufficient for **known erasures** do not automatically grant safe repair authority for arbitrary unknown corruption.

Case 140 now contributes earlier source-level evidence that the distinction can be expressed directly as a recovery-budget difference:

`known unavailable member -> one redundancy unit in the cited budget`

versus

`one unknown DASD error -> two-parity equivalent for identification + correction in US5351246A`

This is a functional comparison across cases, not a genealogy from the IBM patent to Linux md, OpenZFS, Ceph, or any later P/Q implementation.

### Case 101 — detection/localization versus repair authority

Case 101's scrub material is useful only at a higher functional level. Discovering an unreadable or inconsistent region can change what the system knows about which source is trustworthy; that knowledge can in turn change whether a coded reconstruction is admissible.

The shared abstraction is:

`detection / localization evidence -> repair admissibility -> usable reconstruction margin`

No direct technical lineage between ServeRAID scrubbing and Case 140 is claimed.

### Case 136 — rebuild-rate policy

Case 136 asks how much execution priority a controller gives an owed rebuild. Case 140 asks what redundancy relation makes missing or erroneous content reconstructable in the first place.

`reconstructability relation != repair scheduling policy`

### Distributed erasure-coded storage

Later distributed erasure-coded systems share the broad pattern:

`surviving fragments + coding relation → reconstruct missing fragment(s)`

But distributed placement, membership/currentness, failure domains, network repair traffic, fault localization, and protocol authority are additional layers. Functional similarity does not establish descent from the IBM schemes.

## Retention relevance

The first conceptual contribution remains that **future tolerance can itself be a retained technical state**.

After one disk disappears, a two-failure code may retain two things at once:

1. enough information to reconstruct the **current payload**;
2. enough independent redundancy relation to absorb **one further located member loss** before reconstruction becomes impossible under the code model.

The second property is not a stored historical log and not another object copy. It is a remaining relation among surviving coded fragments.

The new evidence adds a second retention result: **the usable amount of that margin depends on what is known about the fault**.

```text
retained coded state
    + currentness of that coded relation
    + failure / erasure location knowledge or locator capability
    -> operational recoverability under a stated fault model
```

Thus the same physical parity embodiment can support different future outcomes depending on whether the system is solving for values at known missing coordinates or must also identify an errant source.

The philosophical interpretation should stop there. `Knowledge` here means machine-usable failure-location/admissibility information or information derivable under the decoder's code model, not a metaphysical property of storage.

## Counterexamples and stop conditions

- **Double-disk tolerance != mirroring.** Two redundant disks do not imply two full payload copies.
- **Two erasures != one error plus one erasure.** With `P=2`, US5351246A's stated mixed bound does not establish the latter combination.
- **One-DASD-in-error correction != arbitrary corruption correction.** The source model is narrower than arbitrary sector/byte/bit corruption.
- **One-column-in-error abstract claim != full inspected decoder proof.** The journal abstract establishes scope, not every algorithmic detail.
- **US5351246A != EVENODD.** Historical adjacency and shared IBM array-code context do not make the constructions identical.
- **Double-disk-failure scheme != source-era `RAID-6` terminology.** Later terminology is comparison only.
- **Patent priority != public disclosure date.** Priority/family dates and publication dates support different historical claims.
- **Patent/paper disclosure != commercial deployment.** No named controller shipment is established here.
- **XOR-only != RAID-5-equivalent protection.** Shared computational primitives do not imply identical reconstructability.
- **Parity-hardware reuse != controller support.** Implementability is not a firmware/product record.
- **Authors' optimality wording != global systems optimum.** No inference to rebuild latency, IOPS, risk, or operational cost.
- **Recoverability != repair completion.** A degraded array can remain reconstructable while carrying less future-failure margin.
- **Parity readable != parity current.** This case does not solve write-hole or stale-parity currentness.
- **Rebuild != scrub.** Reconstruction does not by itself locate arbitrary unknown silent corruption.
- **Rebuild != sanitization.** Writing reconstructed state to a spare says nothing about secure erasure of a failed/removed member.

## Uncertainty and next evidence

The bounded case remains grounded, while these debts remain open:

1. direct origin-host facsimiles for the early patent family and full conference texts rather than institutional abstracts/public mirrors;
2. page-level inspection of the 1995 EVENODD journal paper's one-column-error decoder if exact mixed-fault semantics are needed;
3. full Reed–Solomon / diagonal-parity / EVENODD / RDP genealogy;
4. earliest and standards-level history of the term `RAID-6`;
5. named production hardware/firmware implementing the cited schemes;
6. second-failure-during-rebuild fault behavior;
7. sector-level URE/ECC/CRC interaction and failure-location semantics;
8. parity-currentness / write-hole handling during interrupted multi-parity updates;
9. real rebuild throughput, latency, write amplification, and operational-risk measurements.

## Related repository boundary

Fresh searches of `tmzncty/computing-archaeology` for `EVENODD` and the IBM error/erasure array-code line found no dedicated overlapping packet.

`technical-retention` keeps the narrower seam:

**coded recoverability budget → known erasure location versus unknown errant source → different redundancy consumption → repair admissibility / remaining failure margin.**

Broader IBM Almaden array-code history, Reed–Solomon / EVENODD / RDP genealogy, controller adoption, product implementation, and the history of the `RAID-6` category belong in `computing-archaeology` if pursued.

## Evidence links

- [Evidence 140 — IBM 1991–1994 double-disk-failure array codes](../evidence/140-ibm-1991-1994-double-disk-array-codes-grounding.md)
- [Evidence 140D — IBM 1991–1995 error-vs-erasure recovery budget](../evidence/140-ibm-1991-1995-erasure-error-budget-deepening.md)
- [Case 17 — RAID parity reconstruction](17-raid-parity-reconstruction-degraded-repair.md)
- [Case 94 — RAID-6 P/Q dual-erasure / corruption boundary](94-raid6-pq-dual-erasure-corruption-boundary.md)
- [Case 101 — scrub / repair-authority boundary](101-scsi-background-medium-scan-proactive-defect-discovery.md)
- [Case 136 — MegaRAID/PERC rebuild rate](136-megaraid-perc-rebuild-rate-repair-priority.md)
- [IBM Research — ICC 1992 double disk failures](https://research.ibm.com/publications/a-coding-technique-for-recovery-against-double-disk-failures-in-disk-arrays)
- [IBM Research — EVENODD journal record](https://research.ibm.com/publications/evenodd-an-efficient-scheme-for-tolerating-double-disk-failures-in-raid-architectures)
- [CaltechAUTHORS — EVENODD journal record](https://authors.library.caltech.edu/records/4azcy-f4q81)
- [US5351246A public patent record](https://patents.google.com/patent/US5351246A/en)
- [EP0499365A2 public patent record](https://patents.google.com/patent/EP0499365A2/en)
- [USENIX FAST 2008 — RAID-6 Liberation Codes](https://www.usenix.org/conference/fast-08/raid-6-liberation-codes)
