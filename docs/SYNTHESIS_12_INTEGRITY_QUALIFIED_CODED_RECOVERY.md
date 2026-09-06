# Synthesis 12 — Integrity-Qualified Coded Recovery: Authority, Diagnosis, Decode, and Revalidation

## Scope

This is a **bounded cross-case engineering synthesis**, not a new historical case and not a genealogy of RAID, erasure coding, checksums, scrubbing, Swift, Ceph, or ZFS.

It closes one relation-decomposition question already present in the roadmap:

> In integrity-qualified coded storage, how should `coded recoverability`, `local checksum validity`, `checksum-metadata authority`, `scrub coverage`, `diagnostic mismatch`, and `restored repair confidence` be separated?

The comparison is built from already-grounded repository cases:

- [Case 25 — Swift mutable EC overwrite / durability-currentness](../cases/25-openstack-swift-ec-overwrite-durability-currentness.md);
- [Case 27 — Ceph Luminous EC / BlueStore checksum authority](../cases/27-ceph-luminous-ec-deep-scrub-checksum-authority.md);
- [Case 29 — Ceph Luminous scrub-authoritative EC repair](../cases/29-ceph-luminous-ec-scrub-authoritative-repair.md);
- [Case 94 — RAID-6 P+Q dual-erasure / corruption-location boundary](../cases/94-raid6-pq-dual-erasure-corruption-boundary.md);
- [Case 96 — OpenZFS dRAID distributed-spare / sequential reconstruction](../cases/96-openzfs-draid-distributed-spare-sequential-resilver.md).

Historical claims remain owned by those case/evidence records. The terms introduced below are **project engineering vocabulary (`E`)** unless explicitly identified as period/product vocabulary. Functional comparison does not establish common descent.

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for scrub/checksum/erasure-coding/RAID-integrity combinations found no dedicated overlapping case in the current search surface. A broader history of RAID integrity, controller patrol read, checksum design, scrubbing, erasure-code families, or storage-controller products should therefore remain routed there if later developed; this document keeps only the retention-specific relation decomposition.

---

## Why this synthesis is not already Synthesis 07 or 08

[Synthesis 07](SYNTHESIS_07_CODED_RECOVERABILITY_REPAIR_MARGIN.md) separates **known failure/exposure, code reconstructability, degraded service, repair scope, reconstruction geometry, restored redundancy, and later verification**.

[Synthesis 08](SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md) separates **presence, integrity evidence, proactive verification, defect discovery, diagnosis, repairability, repair, and revalidation** across replicated and coded systems.

The remaining gap is the seam between them:

> **When recovery is coded rather than simple replica copy, which surviving contributions are allowed to enter the equations, what evidence can disqualify them, and what does successful reconstruction still fail to prove?**

This synthesis therefore does not repeat either earlier document. It composes their boundaries around one narrower object: **integrity-qualified coded inputs and outputs**.

---

## Historical records kept separate

### RAID-6 P+Q — stronger code does not solve arbitrary corruption diagnosis

Case 94 grounds the P+Q / RAID-6 relation in Chen et al. and H. Peter Anvin's mathematics note. Two independent syndromes can solve for two **known missing positions** under the bounded model. The coefficients depend on those positions.

The same source set supplies the counterexample needed here: RAID-6 does not, in general, locate and repair arbitrary dual silent corruption merely because two redundant equations exist. A stronger code relation is not automatically a stronger diagnosis relation.

So the coded-storage integrity problem begins before decode:

```text
more parity information
    !=
knowledge of which apparently present contribution should be distrusted
```

### Swift EC — currentness qualification can precede any integrity claim

Case 25 shows a different axis. A set of physically present Swift fragments must satisfy release-bounded timestamp/version, distinct-index, and durability/currentness rules before it forms an admissible object cohort. Enough bytes or enough indexes are not sufficient if they belong to the wrong overwrite generation or have not crossed the commit/durability gate.

That axis is deliberately kept separate from checksum authority. A fragment can be **current but corrupt**; another can be **locally valid but stale**. Version/currentness and integrity qualification must compose rather than substitute for one another.

### Ceph Luminous — checksums are retained state whose authority can fail

Case 27 supplies the strongest integrity-metadata counterexample. Luminous EC overwrites on BlueStore were tied to checksumming and deep scrub, so the algebraic fact that `K` sufficiently many fragments exist was not the whole recovery relation.

The 12.2.6 checksum-maintenance regression then reverses the ordinary direction of suspicion: stored digest metadata could itself become stale/inconsistent. Ceph 12.2.7 introduced a bounded `osd distrust data digest` workaround, and 12.2.8 required upgrade plus full deep-scrub/reconciliation before normal trust could be restored.

Therefore:

```text
checksum stored
    !=
checksum currently authoritative
```

and:

```text
checksum mismatch
    !=
proof that payload bytes are the defective side
```

### Ceph Luminous repair — diagnosis and code sufficiency are separate layers

Case 29 follows the 12.2.8 source path after scrub disagreement. The scrub backend excludes shards with read/stat/hash/size/info errors, selects an operational `auth` / `authoritative` candidate relation, records missing/inconsistent peers, and only later hands ordinary recovery a candidate source set.

The EC backend then independently filters available shard indexes and asks `minimum_to_decode(...)` which subset is mathematically sufficient. New read failures can cause the planned source set to be revised and the decode requirement recalculated.

This establishes the central seam:

```text
repair-source admissibility
    !=
algebraic decode sufficiency
```

The source comment that an auth shard may reach the path without the implementation knowing that it has the objectively "correct" data also prevents a stronger epistemic claim. `Authoritative` is an operational role under available evidence, not a universal proof of truth.

### OpenZFS dRAID — restored coded margin can precede restored integrity confidence

Case 96 supplies the completion-side counterexample. Sequential dRAID reconstruction can restore the configured redundancy relation first. Because that pass does not itself perform the ordinary block-pointer checksum verification of a scrub, a scrub follows by default.

So even after bytes have been reconstructed and the coded failure margin is back:

```text
restored coded redundancy
    !=
completed integrity revalidation
```

---

## Engineering reconstruction: eleven typed relations

The following decomposition is analytical. It is not asserted as one implementation pipeline used by every coded storage system.

### 1. Coded contribution presence

Does a parity block, data fragment, coding fragment, or shard physically exist at the expected logical/code position?

Presence is necessary in many repair paths but is the weakest state in this synthesis. A present contribution can still be stale, unreadable, corrupt, or otherwise inadmissible.

### 2. Version / currentness qualification

Does the contribution belong to the coded logical state that is allowed to count now?

Swift's timestamp/durability rules make this axis explicit. RAID parity-currentness and other coded systems can expose analogous but historically distinct currentness relations.

### 3. Local integrity evidence

What retained relation is available to test whether a contribution's bytes/structure match an expected integrity condition?

Examples include checksums, digests, hash-info, read-status, size/metadata consistency, or lower-layer read/ECC status. These relations are not themselves another complete user-payload copy.

### 4. Integrity-metadata authority

May the verifier itself currently be trusted?

Case 27 shows why this needs its own type. A stored digest can be present and syntactically usable while a release bug has made its maintenance relation unreliable. Systems may therefore need version/repair knowledge about the **integrity metadata itself**.

### 5. Verification coverage / recency

Has the relevant contribution and integrity relation actually been exercised under the chosen verification policy, and how recently?

A configured scrub interval or a completed pass is evidence about work performed. It is not a permanent guarantee that every coded contribution remains sound.

### 6. Diagnostic mismatch / fault-location evidence

What evidence says one contribution or relation should stop counting?

A read error can self-identify a missing/unusable position. A checksum mismatch may only prove disagreement. RAID-6's arbitrary-corruption limit shows that extra equations do not automatically convert ambiguity into known erasure locations.

### 7. Repair-source admissibility

After currentness/integrity/diagnostic filtering, which surviving contributions may be used as repair inputs?

Case 29's `auth_list`, error exclusions, missing maps, and candidate locations are a release-specific implementation of this more general analytical role.

### 8. Algebraic decode sufficiency

Given the currently admissible coded indexes, does the code provide enough independent information to reconstruct the requested missing contribution(s)?

This is where `minimum_to_decode`, P/Q equations, or another codec relation matters. It answers a mathematical sufficiency question after the source-admissibility question has already constrained the input set.

### 9. Repair execution / materialized replacement

Has reconstruction actually produced and installed the missing contribution in an admissible embodiment?

A candidate set or successful decode plan is not yet a repaired disk/shard. Reads, decode, writes, metadata updates, and installation still have to complete.

### 10. Restored coded margin

Has the system regained the intended ordinary tolerance against the next failure under its configured code/placement relation?

This is stronger than one foreground read succeeding, and weaker than every integrity confidence condition being renewed.

### 11. Integrity revalidation / returned confidence

Has later verification exercised the reconstructed/current coded state strongly enough to restore the system's chosen integrity claim?

OpenZFS dRAID gives the direct ordering counterexample: coded redundancy can be restored before the follow-up scrub.

---

## Compact relation map

```text
coded contribution physically present
        ↓
version/currentness qualified
        ↓
local integrity evidence available
        ↓
integrity metadata itself currently authoritative
        ↓
verification actually exercises the relation
        ↓
diagnostic mismatch / known-unusable-position evidence
        ↓
repair-source admissibility
        ↓
mathematical decode sufficiency
        ↓
reconstruction / replacement installed
        ↓
configured coded margin restored
        ↓
(optional/separate) integrity revalidation
```

This map is a diagnostic checklist, not a universal causal sequence. Some systems discover faults on demand rather than by scrub; some fold integrity checks into ordinary reads; some have no mutable-version axis; some revalidate during reconstruction rather than afterward.

Its purpose is to prevent the single word `recoverable` from silently meaning five different things.

---

## Cross-case matrix

| Relation | Swift Case 25 | Ceph Case 27 | Ceph Case 29 | RAID-6 Case 94 | dRAID Case 96 |
| --- | --- | --- | --- | --- | --- |
| physical coded contribution | fragment archive | EC chunk / BlueStore extent | per-shard object state | data/P/Q contribution | surviving/rebuilt dRAID contribution |
| currentness/version gate | timestamp + durability cohort | PG/object/version context | ObjectInfo/version participates in selection | parity/data coded-currentness | current allocated/layout relation |
| integrity evidence | outside the case's main slice | BlueStore/data digests + deep scrub | read/hash/size/info error state | syndrome consistency is not full payload checksum diagnosis | later block-pointer checksum scrub |
| integrity-metadata authority | not the main slice | explicit 12.2.6–12.2.8 distrust/requalification boundary | candidate logic consumes bounded scrub evidence | parity can be current or untrustworthy after dirty/degraded state | scrub provides stronger later qualification |
| diagnosis/source filtering | version mismatch makes fragment inadmissible | mismatch/inconsistency discovered | bad shards excluded; `auth_list`/ok peers retained | known failed positions vs ambiguous silent corruption | failed/reconstructed device relation |
| code sufficiency | distinct-index / release-specific EC sufficiency | `K/M` geometry exists but case centers integrity qualification | `minimum_to_decode` over filtered indexes | two-known-erasure P+Q equations | inherited RAID-Z/dRAID code relation |
| repair milestone | reconstructor convergence after committed version | incident-specific digest/trust repair plus ordinary data repair | missing-state injection → reads/decode/install | re-materialize missing contribution | sequential reconstruction restores redundancy |
| later confidence | future verification still separate | full deep-scrub can be return-to-trust work | later errors can revise source set | extra diagnosis/checking remains independent | follow-up scrub explicitly separate |

The matrix is `A/E`: functional comparison across separately grounded systems, not evidence of direct lineage or shared terminology.

---

## Findings

### E — coded contribution presence ≠ integrity-qualified contribution

A coded system can retain the right number of physical objects while some of them should not enter reconstruction. Presence says where bytes exist; integrity/currentness qualification says which bytes may count.

### E — version/currentness qualification ≠ integrity qualification

A Swift fragment can be from the wrong overwrite generation even if its local bytes are intact. A Ceph shard can belong to the current object state yet fail a read/hash/size/info check. These are independent axes.

### E — checksum presence ≠ checksum-metadata authority

Ceph's Luminous regression is the concrete counterexample. Verification metadata is maintained state, and the mechanism maintaining it can fail. The verifier therefore cannot be treated as an external oracle.

### E — checksum mismatch ≠ fault localization

A mismatch establishes disagreement. It does not, by itself, identify whether payload, digest metadata, or another compared contribution is wrong. Repair needs additional evidence/policy to turn disagreement into a known-unusable source relation.

### E — more parity equations ≠ stronger corruption diagnosis

RAID-6 P+Q expands the erasure patterns that can be reconstructed once failed positions are known. It does not generally identify arbitrary pairs of silent corruptions. Code strength and diagnosis strength are different resources.

### E — fault-location evidence ≠ algebraic decode sufficiency

Knowing which shard is bad still leaves the code question: are enough other qualified indexes available? Conversely, having enough nominal indexes is useless if integrity/currentness evidence excludes too many of them.

### E — operational repair authority ≠ objective correctness

Ceph's `authoritative` candidate relation is procedural and bounded by available checks. This is exactly why the code comment preserving uncertainty matters: systems often need an operational source of truth before they possess philosophical or cryptographic certainty.

### E — nominal coded margin ≠ integrity-qualified repair margin

A nominal `M`-parity or `K+M` configuration describes a code/failure model. Hidden corruption, stale fragments, or distrusted integrity metadata can reduce the set of safe repair inputs before the system has lost the nominal number of physical members.

The useful repair-margin question is therefore not only:

> how many devices/fragments remain?

but:

> how many **current and integrity-qualified independent coded contributions** remain for the next required reconstruction?

### E — verification coverage is retained operational evidence, not timeless truth

A deep scrub can renew confidence over an exercised population. Later corruption or an unvisited fault class can still invalidate future assumptions. Coverage and recency belong to the confidence claim.

### E — repair-source admissibility can change during recovery

Case 29 can discover new read failures, add those indexes to error state, and recompute a decode set. The source set is therefore not necessarily fixed at the moment repair is scheduled.

### E — reconstructed bytes ≠ restored integrity confidence

OpenZFS dRAID provides the completion-side counterexample: reconstruction can restore coded redundancy before later checksum verification. `repaired` must therefore name which completion axis has actually closed.

### E — mutable-currentness gate ≠ integrity-authority gate

Synthesis 10's mutable EC currentness relation remains orthogonal. A version can be committed/current and still fail integrity checks; another version can be perfectly checksum-valid and still be inadmissible because it is stale. Coded retention composes both gates.

---

## Relationship to nearby syntheses

### Synthesis 07 — coded recoverability / repair margin

Synthesis 07 asks what a known failure does to algebraic recoverability, degraded service, repair scope, geometry, and restored redundancy. Synthesis 12 inserts the **qualification seam before the equations** and the **confidence seam after reconstruction**.

### Synthesis 08 — proactive integrity

Synthesis 08 asks how hidden defects are discovered and repaired across replicated and coded storage. Synthesis 12 narrows that result to cases where repair inputs are **coded contributions** rather than interchangeable full replicas, making source qualification and mathematical sufficiency separately necessary.

### Synthesis 10 — mutable EC currentness

Synthesis 10 asks which fragment cohort is committed/current. Synthesis 12 adds the orthogonal integrity question: even the right version must still be a trustworthy decode input.

Together, the three documents prevent three different gates from being collapsed:

```text
current version?
    !=
trustworthy contribution?
    !=
enough independent contributions to decode?
```

---

## What must not be inferred

This synthesis does **not** establish:

- one historical lineage from RAID-6 to Swift, Ceph, or OpenZFS;
- that every coded system uses checksums, scrub, or Ceph-like authority selection;
- that a checksum proves authenticity or identifies the faulty side of a disagreement;
- that RAID-6 can generally diagnose any two silent corruptions;
- that a fragment from the current version is therefore integrity-valid;
- that an integrity-valid fragment from another version is therefore current;
- that an operational `authoritative` source is objectively correct;
- that enough physical fragments imply enough qualified independent fragments;
- that a successful foreground decode means durable repair has completed;
- that restored coded redundancy means later scrub/revalidation is complete;
- that one scalar `health`, `parity`, or `repairable` value can replace the typed relations above.

---

## Philosophical boundary

`I` — Coded systems make a narrow epistemic feature of technical retention unusually visible: persistence can depend not only on surviving material and reconstruction equations, but on retained **rules for which survivors are allowed to count as evidence for one another**.

`I` — That does not make truth, authority, or verification the essence of all technical retention. Magnetic-core remanence, positional state, and other cases elsewhere in the repository remain counterexamples to a universal claim that persistence requires continual proof. The present statement is bounded to systems whose continued recoverability is mediated by coded relations and integrity qualification.

No philosophical vocabulary is attributed to RAID, Swift, Ceph, or OpenZFS engineers.

---

## Source ownership and next work

Historical source locations and evidence grades remain in the case/evidence records linked above. This synthesis intentionally does not duplicate their bibliographies.

Still-open work includes:

- adversarial authenticity and cryptographic integrity rather than accidental-corruption checksums;
- correlated/cross-shard corruption where several contributions fail under a shared cause;
- cross-node scrub coordination and partially completed verification populations;
- production fault injection where integrity metadata, currentness metadata, or repair progress is stale after crash;
- controller patrol-read / RAID verification genealogy and named-product behavior;
- URE-aware rebuild policy and quantitative exposure models;
- wider coded-storage families where reconstruction and verification are fused rather than staged;
- broader checksum / erasure-coding / RAID history in `computing-archaeology` if that project develops the track.

Those are additional research slices, not blockers for the bounded relation decomposition closed here.
