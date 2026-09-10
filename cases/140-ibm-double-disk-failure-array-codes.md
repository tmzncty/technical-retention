# Case 140 — IBM Double-Disk-Failure Array Codes: Retaining a Second Failure Margin

**Status:** grounded  
**Claim layer:** historical record + engineering reconstruction + bounded functional analogy  
**Primary regime:** 1991–1994 IBM disk/DASD-array coding for up to two unavailable members  
**Evidence:** [`../evidence/140-ibm-1991-1994-double-disk-array-codes-grounding.md`](../evidence/140-ibm-1991-1994-double-disk-array-codes-grounding.md)

## Summary

Case 17 established the repository's bounded single-parity RAID relation: after one member fails, the logical data may still be reconstructable while the array has entered a degraded state and has largely spent the failure margin that single parity provided.

This case asks the next narrow question:

> **What changes when the coding relation is explicitly designed to survive up to two unavailable disks rather than one?**

The inspected early-1990s IBM record gives three useful anchors:

1. an IBM patent family with a **1991-02-11 priority** and **1992-08-19 EP publication** for encoding and rebuilding up to two unavailable DASDs;
2. Mario Blaum's **IEEE ICC 1992** paper describing protection against two disk failures with two redundant disks and XOR-only coding;
3. the **ISCA 1994 EVENODD** paper, explicitly framed for "RAID architectures," again tolerating up to two disk failures with two redundant disks and XOR operations.

The retention-specific result is not merely "more parity." It is a different temporal margin:

`healthy coded array → one member unavailable → payload still reconstructable AND one additional member-failure margin remains → repair/rebuild → full designed margin restored`

That remaining margin exists in the **relation among surviving fragments and parity constraints**, not in a second full copy of the payload.

The case deliberately does **not** call every 1991–1994 disclosure `RAID-6`. A 2008 USENIX source supplies later explicit RAID-6 terminology only for functional comparison. Source-era wording and later category names are kept separate.

## Research questions

1. What did early IBM disk-array sources actually claim about surviving two unavailable members?
2. How does two-failure reconstructability differ from Case 17's single-parity degraded mode?
3. Does "two redundant disks" mean two replicas? No — what relation is actually retained?
4. Is mathematical reconstructability the same thing as completed repair? No — what margin remains while degraded?
5. Does a two-disk-failure scheme automatically detect arbitrary silent corruption? No — where is the erasure/error boundary?
6. Can the later term `RAID-6` be projected backward into 1991–1994? Not without source-era evidence.
7. What belongs here versus broader coding/RAID genealogy in `computing-archaeology`?

## Source ladder

| Evidence | Date | Strength | Use here |
|---|---:|---|---|
| IBM patent family EP0499365A2 / US07/653,596 | priority 1991-02-11; EP publication 1992-08-19 | `H/P*` | up-to-two unavailable DASDs, row/diagonal simple parity, spare rebuild, degraded/reconstruction vocabulary |
| Mario Blaum, IEEE ICC 1992, IBM Research record | 1992-06-14 | `H/P` | explicit two-disk-failure protection, two redundant disks, XOR-only coding |
| Blaum et al., EVENODD, ISCA 1994, IBM Research record | 1994-04-18 | `H/P` | named two-failure RAID-architecture scheme, two redundant disks, XOR-only implementation, scoped optimality claim |
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

Its abstract is unusually clean for this repository's purpose: it says the array is protected against **two disk failures**, requires **two redundant disks**, and uses exclusive-OR operations for encoding and decoding, contrasted with finite-field approaches such as Reed–Solomon.

The source therefore directly establishes a two-member-failure target and redundancy quantity. It does **not** establish two complete replicas, a named shipping implementation, or contemporary use of the term `RAID-6`.

### 3. EVENODD in 1994 is explicitly a RAID-architecture scheme

IBM Research dates the ISCA 1994 paper *EVENODD: An optimal scheme for tolerating double disk failures in RAID architectures* to **1994-04-18**.

Its abstract says EVENODD:

- tolerates up to two disk failures;
- adds only two redundant disks;
- uses simple XOR computations;
- can reuse parity hardware of the kind typically present in RAID-5 controllers;
- is, in the authors' wording, the first known double-disk-failure scheme optimal with regard to both storage and performance;
- is compared against prior Reed–Solomon approaches that also use two extra disks but require finite-field operations.

Two historical cautions are mandatory.

First, the `first known` wording remains an **authors' scoped claim**, not an independently proven universal invention priority. The abstract itself acknowledges prior Reed–Solomon-based optimal-storage approaches.

Second, "can be implemented" with RAID-5 parity hardware is not evidence that any named RAID-5 controller shipped EVENODD support. Hardware primitive compatibility and deployed controller semantics are different claims.

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

### E. Failed-member reconstruction is not arbitrary silent-error correction

The inspected patent text itself distinguishes errors, erasures, unavailable DASDs, and parity coding. The bounded Case 140 claim is therefore **located member unavailability / failure reconstructability**.

It does not follow that the same code automatically:

- discovers which still-addressable sector silently returned bad data;
- distinguishes every corruption pattern from valid data;
- corrects an arbitrary mixture of unknown errors and unavailable members;
- replaces scrub or end-to-end checksums.

Thus:

`known failed/unavailable member recovery != arbitrary silent-corruption detection`

This keeps the RAID/rebuild line separate from scrub/integrity-detection cases.

## Terminology and prior-art boundary

### Source-era language

The inspected sources use:

- `double disk failures`;
- `up to two unavailable DASDs`;
- `RAID architectures` in the 1994 EVENODD title/abstract.

They do not, in the inspected material, establish that the exact label `RAID-6` was their own term for the 1991–1994 schemes.

### Later RAID-6 comparison

Plank's FAST 2008 USENIX paper explicitly describes RAID-6 as a `k+2` storage arrangement designed to tolerate any two device failures and discusses two coding devices conventionally called `P` and `Q`.

That supplies a later functional category:

`early two-failure array code ~ later RAID-6 any-two-device reconstructability`

But `~` here means **functional analogy**, not direct genealogy or retroactive nomenclature.

The broader history of Reed–Solomon array use, EVENODD, RDP, controller adoption, the `RAID-6` name, and standards belongs in `tmzncty/computing-archaeology` if pursued. A fresh companion-repository search found no dedicated EVENODD / RAID double-parity study to reuse during this slice.

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

### Case 136 — rebuild-rate policy

Case 136 asks how much execution priority a controller gives an owed rebuild. Case 140 asks what redundancy relation makes the missing content reconstructable in the first place.

`reconstructability relation != repair scheduling policy`

### Distributed erasure-coded storage

Later distributed erasure-coded systems share the broad pattern:

`surviving fragments + coding relation → reconstruct missing fragment(s)`

But distributed placement, membership/currentness, failure domains, network repair traffic, and protocol authority are additional layers. Functional similarity does not establish descent from the IBM schemes.

## Retention relevance

The narrow conceptual contribution is that **future tolerance can itself be a retained technical state**.

After one disk disappears, a two-failure code may retain two things at once:

1. enough information to reconstruct the **current payload**;
2. enough independent redundancy relation to absorb **one further located member loss** before reconstruction becomes impossible under the code model.

The second property is not a stored historical log and not another object copy. It is a remaining relation among surviving coded fragments.

That makes the temporal chain:

`coded healthy state → partial loss → current recoverability survives + future-loss margin shrinks → repair materializes missing relation on spare → full designed margin restored`

The philosophical interpretation should stop there. This case is evidence about engineered redundancy relations, not proof of a universal theory of memory, identity, or resilience.

## Counterexamples and stop conditions

- **Double-disk tolerance != mirroring.** Two redundant disks do not imply two full payload copies.
- **Double-disk tolerance != arbitrary corruption correction.** Located/unavailable-member recovery is narrower than silent-error detection and correction.
- **Double-disk-failure scheme != source-era `RAID-6` terminology.** Later terminology is comparison only.
- **Patent priority != public disclosure date.** The 1991 priority and 1992 publication dates serve different historical claims.
- **Patent/paper disclosure != commercial deployment.** No named controller shipment is established here.
- **XOR-only != RAID-5-equivalent protection.** Shared computational primitives do not imply identical reconstructability.
- **Parity-hardware reuse != controller support.** Implementability is not a firmware/product record.
- **Authors' optimality wording != global systems optimum.** No inference to rebuild latency, IOPS, risk, or operational cost.
- **Recoverability != repair completion.** A degraded array can remain reconstructable while carrying less future-failure margin.
- **Rebuild != scrub.** Reconstruction does not by itself locate unknown silent corruption.
- **Rebuild != sanitization.** Writing reconstructed state to a spare says nothing about secure erasure of a failed/removed member.

## Uncertainty and next evidence

The bounded case is grounded, while these debts remain open:

1. direct origin-host facsimiles for the early patent family and full conference texts rather than institutional abstracts/public mirrors;
2. full Reed–Solomon / diagonal-parity / EVENODD / RDP genealogy;
3. earliest and standards-level history of the term `RAID-6`;
4. named production hardware/firmware implementing the cited schemes;
5. second-failure-during-rebuild fault behavior;
6. URE/silent-sector detection and location semantics;
7. real rebuild throughput, latency, write amplification, and operational-risk measurements.

## Related repository boundary

A fresh search of `tmzncty/computing-archaeology` for `EVENODD`, `RAID double parity`, and related wording found no dedicated overlapping study. If that repository later develops the broad coding/controller genealogy, this case should link to it rather than reproduce it.

`technical-retention` keeps the narrower question: **what reconstructability and future-failure margin remain after partial loss, and what separate repair process restores the designed relation?**

## Evidence links

- [Evidence 140 — IBM 1991–1994 double-disk-failure array codes](../evidence/140-ibm-1991-1994-double-disk-array-codes-grounding.md)
- [Case 17 — RAID parity reconstruction](17-raid-parity-reconstruction-degraded-repair.md)
- [Case 136 — MegaRAID/PERC rebuild rate](136-megaraid-perc-rebuild-rate-repair-priority.md)
- [IBM Research — ICC 1992 double disk failures](https://research.ibm.com/publications/a-coding-technique-for-recovery-against-double-disk-failures-in-disk-arrays)
- [IBM Research — ISCA 1994 EVENODD](https://research.ibm.com/publications/evenodd-an-optimal-scheme-for-tolerating-double-disk-failures-in-raid-architectures)
- [EP0499365A2 public patent record](https://patents.google.com/patent/EP0499365A2/en)
- [USENIX FAST 2008 — RAID-6 Liberation Codes](https://www.usenix.org/conference/fast-08/raid-6-liberation-codes)
