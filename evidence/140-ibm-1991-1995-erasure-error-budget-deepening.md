# Evidence 140D — IBM 1991–1995 error-vs-erasure recovery budget deepening

**Status:** bounded deepening complete  
**Case:** [`../cases/140-ibm-double-disk-failure-array-codes.md`](../cases/140-ibm-double-disk-failure-array-codes.md)  
**Claim layer:** historical record + engineering reconstruction + bounded functional comparison  
**Primary question:** when the same coded array has a fixed parity budget, how does recoverability change when failed locations are already known (`erasures` / unavailable DASDs) versus when one still-addressable DASD is erroneous and the errant source must also be identified?

## Why this slice exists

The baseline Case 140 evidence established a clean early-1990s IBM line for reconstructing **up to two unavailable DASDs** with XOR-based array codes. The canonical case correctly refused to infer from that result that the code therefore corrected arbitrary silent corruption.

That boundary was safe but still too coarse.

An adjacent IBM patent, US5351246A, directly distinguishes:

- an **unavailable DASD / erasure** model, where the failed location is known;
- a **DASD in error** model, where an erroneous source must be identified and corrected;
- the different amount of parity redundancy consumed by those two models.

The 1995 journal abstract for EVENODD independently advertises a decoding algorithm for **one column (track) in error** in addition to the familiar two-disk-failure result.

This evidence packet therefore deepens one narrow relation:

> **fault-location knowledge changes the usable recovery budget even when the physical parity bytes have not changed.**

It does **not** turn Case 140 into a general silent-corruption case.

---

## Source custody

### P1 — IBM patent / public patent record

**US5351246A**, *Method and means for coding and rebuilding that data contents of unavailable DASDs or rebuilding the contents of DASDs in error in the presence of reduced number of unavailable DASDs in a DASD array*.

- Assignee: International Business Machines Corporation.
- Inventors in the public record: Miguel M. Blaum and Ron M. Roth.
- Public record: <https://patents.google.com/patent/US5351246A/en>
- The public record lists a 1991 filing/priority lineage and publication/grant on **1994-09-27**.
- This packet uses the HTML patent text because it exposes the definitions, summary, claims, and family chronology directly. It does not rely on an OCR-only scan.

Relevant patent-text anchors include:

- the invention can rebuild `R` unavailable DASDs where `R <= P` parity DASDs;
- it can instead correct **one DASD in error** in the presence of up to `R-2` unavailable DASDs, again with `R <= P`;
- the text explicitly states that a DASD in error requires redundancy equivalent to **two parity DASDs** to identify and correct the errant unit;
- it distinguishes `data error` from `erasure` in its definitions;
- it discusses rebuilding unavailable DASDs onto spares and distinguishes degraded/rebuild operation from normal fault-tolerant operation.

### P2 — IBM Research / Caltech institutional record for the journal EVENODD article

Mario Blaum, Jim Brady, Jehoshua Bruck, and Jai Menon, *EVENODD: An Efficient Scheme for Tolerating Double Disk Failures in RAID Architectures*, **IEEE Transactions on Computers 44(2), 1995, pp. 192–202**.

Institutional records:

- IBM Research: <https://research.ibm.com/publications/evenodd-an-efficient-scheme-for-tolerating-double-disk-failures-in-raid-architectures>
- CaltechAUTHORS: <https://authors.library.caltech.edu/records/4azcy-f4q81>
- DOI: <https://doi.org/10.1109/12.364531>

The public abstract states both that EVENODD tolerates up to two disk failures with two redundant disks and that the paper also presents a decoding algorithm for **one column (track) in error**.

This packet uses that latter statement only at **abstract level**. It does not reconstruct the journal paper's full error-decoding algorithm from an uninspected PDF.

### Existing Case 140 sources retained

The base evidence remains:

- [`140-ibm-1991-1994-double-disk-array-codes-grounding.md`](140-ibm-1991-1994-double-disk-array-codes-grounding.md)
- IBM Research ICC 1992 record
- IBM Research ISCA 1994 EVENODD record
- EP0499365A2 / related early IBM patent-family material

This deepening supplements rather than replaces that packet.

---

## 1. Historical record: IBM explicitly separates `error` from `erasure`

US5351246A does not use `failure`, `error`, and `erasure` as interchangeable words.

Its text defines a **data error** as a changed stored value caused by noise or burst processes. The storage path remains present, but some returned values are wrong.

It separately defines an **erasure** as removal / absence of a data value in a storage location. In the array-level parts of the patent, unavailable DASDs are treated as failures/erasures whose locations are already part of the recovery problem statement.

That gives a source-era distinction that matters operationally:

```text
unavailable DASD / erasure
    -> the missing location is known to the decoder

DASD in error
    -> a value source remains present
    -> but the decoder must identify which source is errant as part of correction
```

The second problem asks the redundancy relation to do more work than the first.

This is not a modern philosophical gloss imposed on the source. The patent itself distinguishes the categories and gives them different recoverability bounds.

---

## 2. Historical record: the parity budget is explicitly different

Let:

- `P` = number of parity DASDs;
- `R` = the number of failure/erasure positions being handled in the patent's construction, with `R <= P`;
- `U` = known unavailable DASDs present alongside an erroneous DASD.

The patent states two different bounds.

### 2.1 Known unavailable DASDs

For unavailable DASDs, the construction can rebuild up to `R` unavailable DASDs where:

```text
R <= P
```

At the budget level used in this packet:

```text
known erasure / unavailable-member budget:
U <= P
```

### 2.2 One DASD in error

For one DASD in error, the patent states that it can correct that DASD in the presence of up to `R-2` unavailable DASDs, with `R <= P`.

The patent then makes the reason explicit: the DASD in error requires the redundancy equivalent of **two parity DASDs to identify and correct the errant unit**.

At the bounded budget level:

```text
one DASD in error + U unavailable:
U <= P - 2
```

The difference is not a change in the number of physical parity devices. It is a change in how much of the code's redundancy is consumed by the uncertainty about which source is wrong.

---

## 3. The `P = 2` boundary is especially useful

For a two-parity construction, the patent's stated budget yields a simple contrast.

### Known member loss

```text
P = 2
U <= 2
```

So up to two known unavailable DASDs can fit the erasure-style bound.

### One erroneous DASD

```text
P = 2
one error + U unavailable
U <= 0
```

So the same two-parity budget can be consumed by locating and correcting one erroneous DASD.

The safe retention statement is therefore:

```text
same two parity units
    -> can cover two located/unavailable members
       OR
    -> can cover one DASD-in-error problem under the patent model

but the cited bound does not thereby cover:
    one DASD in error + one unavailable DASD
```

This is stronger and more precise than saying only that `double-disk tolerance != arbitrary silent corruption correction`.

---

## 4. Engineering reconstruction: why location knowledge is part of recovery state

The following is an engineering reconstruction of the cited bounds, not quoted source terminology.

If a member is known unavailable, the decoder is told **which coordinate is absent**. The coding equations need to solve for missing values at already identified positions.

If a still-present member is erroneous, the decoder has two linked tasks:

1. determine which coordinate is untrustworthy;
2. determine the correct value for that coordinate.

That is why, in the patent's stated construction, one erroneous DASD consumes redundancy equivalent to two parity DASDs.

The useful abstraction is:

```text
retained parity relation
    + fault-location knowledge
    -> one recovery margin

same retained parity relation
    + unknown errant source
    -> smaller usable failure/erasure margin
```

So recoverability is not a function of surviving bytes alone.

It also depends on what the system knows — or can derive — about **which surviving-looking component is admissible as evidence**.

---

## 5. Historical corroboration: EVENODD's 1995 abstract reaches beyond two erasures

The 1995 IEEE Transactions on Computers abstract for EVENODD repeats the familiar result:

- up to two disk failures;
- two redundant disks;
- simple XOR operations;
- no hardware changes beyond parity primitives claimed necessary for the stated RAID-5-controller implementation argument.

But it also says:

> the paper presents a decoding algorithm for one column (track) in error.

That matters because it independently shows that the authors' published EVENODD presentation was not conceptually limited to the erasure-only statement in its title.

The evidence level must remain bounded, however.

From the abstract alone, this packet does **not** infer:

- every mixed error/erasure bound of the full paper;
- arbitrary per-sector silent corruption correction;
- arbitrary multiple-error correction;
- exact syndrome / locator implementation details;
- deployed-controller behavior.

The full paper remains useful future evidence if a page-level error-decoding analysis is needed.

---

## 6. Do not collapse US5351246A into EVENODD

The two records are historically adjacent and technically relevant to the same repository question, but this packet does not assert that they are the same code.

US5351246A describes a broader slope/parity construction with `P` parity DASDs and explicitly states mixed error/erasure bounds.

The 1995 EVENODD abstract describes the named two-redundant-disk scheme and advertises a one-column-in-error decoder.

Therefore the allowed relation is:

```text
IBM array-code prior art / contemporaneous research context
    -> useful comparison

not:
US5351246A == EVENODD
```

No genealogy stronger than the documents directly support is required for the retention result.

---

## 7. Engineering reconstruction: `physical redundancy` and `usable recovery margin` are different predicates

This case now needs at least four predicates rather than one vague word `redundancy`.

```text
P1: coded parity bytes physically survive
P2: parity relations correspond to the current protected data state
P3: failed / errant coordinates are known or can be located under the code model
P4: enough independent redundancy remains to solve the required recovery problem
```

A system can satisfy `P1` while lacking enough information for `P3`, and therefore fail to satisfy `P4` for a harder error model.

That yields:

```text
parity physically present
    != parity sufficient for this fault model

code can reconstruct known erasures
    != code can locate an unknown erroneous source with the same margin
```

This is the retention-specific reason the source is valuable.

---

## 8. Functional comparison — Case 94, not genealogy

Case 94 already studies a later RAID-6 `P/Q` boundary between dual erasure recovery and corruption/integrity qualification.

The functional comparison is:

```text
Case 140:
IBM early-1990s coded-array evidence
    -> explicitly different budgets for known unavailable DASDs and one DASD in error

Case 94:
later RAID-6 / scrub evidence
    -> redundant equations do not make arbitrary unknown corruption safely repairable without enough detection/location/qualification evidence
```

This is a comparison of **recovery preconditions**.

It is not evidence that Linux md RAID6, OpenZFS, Ceph, or later P/Q implementations descend directly from US5351246A or EVENODD.

---

## 9. Functional comparison — scrub / integrity cases

Cases such as Case 101 are useful only at a higher functional level.

A scrub can discover that a region is unreadable or inconsistent and thereby change the system's knowledge about which source is trustworthy. A code can then use redundancy under a fault model that assumes the location of missing or bad state is known.

That gives a generic relation:

```text
detection / localization evidence
    -> changes repair admissibility
    -> changes how much redundancy remains usable for reconstruction
```

But IBM ServeRAID Data Scrubbing is not claimed as the origin of the Case 140 code, and Case 140's patent is not claimed as the origin of later scrub practice.

---

## 10. Philosophical interpretation — keep it narrow

The philosophical reading is bounded:

> A stored redundancy relation does not by itself determine future recoverability. The system may also need retained or newly reconstructed knowledge about which components are absent, which are suspect, and which can still count as evidence.

That can be summarized as:

```text
retained coded state
    + admissibility / fault-location knowledge
    -> operational recoverability
```

The case does **not** prove that `knowledge` is a metaphysical property of storage systems. Here `knowledge` means concrete machine-usable information or a decoder's established failure-coordinate assumptions.

---

## 11. Failure-window / capability matrix

| Condition | Physical parity present? | Bad/missing coordinate known? | Source-supported capability | Retention reading |
|---|---:|---:|---|---|
| healthy coded array | yes | n/a | normal protected operation | full designed relation available |
| one known DASD unavailable | surviving parity yes | yes | rebuild within `R <= P` bound | payload can remain reconstructable; margin shrinks |
| two known DASDs unavailable with `P=2` | surviving equations as assumed | yes | inside two-erasure-style budget | both redundancy units can be spent on located losses |
| one DASD in error with `P=2` | yes | not given in advance by the error model | patent says error consumes two-parity equivalent for identification + correction | same physical redundancy supports a stricter fault budget |
| one DASD in error + one unavailable DASD with `P=2` | yes | unavailable coordinate known; error source must also be identified | outside cited `U <= P-2` mixed bound | do not infer recoverability |
| arbitrary sector corruption | maybe | not necessarily | not established by this slice | code-family claim must not be generalized |
| stale parity / write-hole state | bytes may exist | irrelevant | not solved by this evidence | currentness/atomicity is a separate problem |

---

## 12. Claim ledger

### Directly supported historical claims

1. US5351246A is an IBM patent published on 1994-09-27 with a 1991 application/priority lineage.
2. The patent distinguishes `data error` from `erasure` / unavailable DASD conditions.
3. Its construction rebuilds up to `R` unavailable DASDs where `R <= P`.
4. It also states correction of one DASD in error in the presence of up to `R-2` unavailable DASDs.
5. The patent explicitly says the DASD-in-error case requires redundancy equivalent to two parity DASDs to identify and correct the errant unit.
6. The 1995 EVENODD journal abstract states that the paper presents a decoding algorithm for one column (track) in error.
7. The EVENODD abstract separately states the two-disk-failure / two-redundant-disk result.

### Engineering reconstruction

8. Known erasure locations reduce the decoding uncertainty relative to an unknown erroneous source.
9. For the patent's stated budget, fault-location uncertainty consumes usable redundancy margin without changing the number of physical parity DASDs.
10. With `P=2`, two known unavailable DASDs and one DASD-in-error problem are different ways of consuming the same nominal two-parity capacity.
11. Recovery capability depends on both surviving coded state and the admissibility/location information available to the decoder.

### Functional analogy only

12. Case 94 exhibits a later version of the broad `erasure recovery != arbitrary corruption repair` boundary.
13. Case 101 illustrates how detection/localization work can change repair admissibility.
14. These comparisons establish no technical genealogy.

### Philosophical interpretation only

15. Retention of redundancy is not equivalent to retention of recoverability if the system cannot establish which surviving-looking evidence is trustworthy.

---

## 13. Explicit non-claims

1. **No claim that US5351246A is identical to EVENODD.**
2. **No claim that the patent's `P`-parity construction is the exact algorithm in the 1995 EVENODD paper.**
3. **No claim that EVENODD invented double-disk-failure coding in general.**
4. **No claim that the patent establishes universal invention priority for error/erasure coding.**
5. **No claim that `one column in error` means arbitrary silent corruption at any sector, byte, or bit cardinality.**
6. **No claim of correction of arbitrary multiple unknown errors.**
7. **No claim that two erasures plus one unknown error are correctable with only two parity DASDs.**
8. **No claim that one error plus one erasure is covered by the cited `P=2` bound.**
9. **No claim that every physical disk failure maps cleanly to one code-column erasure.**
10. **No claim that every still-addressable drive returning bad data matches the patent's one-DASD-in-error model.**
11. **No claim that media-sector ECC, controller retry, or transport CRC semantics are specified by this evidence.**
12. **No claim that the code automatically discovers stale parity.**
13. **No claim that the code solves RAID write-hole / torn-update atomicity.**
14. **No claim that parity bytes are current merely because they are readable.**
15. **No claim that reconstruction has completed merely because reconstruction is mathematically possible.**
16. **No claim that reconstructed output is automatically authoritative without currentness/integrity qualification.**
17. **No claim that any named commercial IBM controller shipped the exact patented algorithm.**
18. **No claim that the 1995 abstract exposes the complete one-column-error decoder.**
19. **No claim that the patent terminology equals later Linux md / ZFS / Ceph terminology.**
20. **No direct genealogy claim from IBM array codes to later RAID-6 implementations.**
21. **No direct genealogy claim from the IBM patent to RDP, Liberation codes, or Reed–Solomon deployments.**
22. **No claim that error localization is always stored metadata; it may be inferred by a decoder under its code model.**
23. **No claim that `fault-location knowledge` is historical source terminology; it is this repository's engineering abstraction.**
24. **No claim that stronger mathematical protection removes the need for scrub, checksums, rebuild policy, or monitoring.**
25. **No claim that two redundant disks are two replicas.**
26. **No claim that RAID-6 is the source-era name of the 1991–1995 IBM schemes.**

---

## 14. Remaining evidence debt

This slice closes only the error-vs-erasure **budget** boundary. Remaining work includes:

1. page-level inspection of the 1995 EVENODD journal paper if the exact one-column-error decoder is needed;
2. origin-host / prosecution-history copies for the IBM patent family where historically useful;
3. precise relation among US5271012A, US5351246A, EVENODD, later IBM slope codes, RDP, and other two-parity constructions;
4. product evidence showing which coded-array constructions actually shipped;
5. controller behavior when the hardware reports ambiguous rather than located failures;
6. sector-level URE/ECC/CRC interaction with disk-column coding;
7. currentness/write-hole handling under multi-parity update interruption;
8. rebuild-throughput and second-failure exposure measurements;
9. standards-era terminology for mixed error/erasure RAID recovery.

Those are separate slices rather than prerequisites for the bounded conclusion here.

---

## 15. Bounded conclusion

The new evidence supports a sharper Case 140 boundary than the generic warning that `double-disk tolerance != silent-error correction`.

Within US5351246A's stated model:

```text
P parity DASDs

known unavailable / erasure case:
    U <= P

one DASD in error + known unavailable case:
    U <= P - 2
```

The patent explicitly explains the difference: identifying and correcting one erroneous DASD consumes redundancy equivalent to two parity DASDs.

Therefore:

```text
same physical coded redundancy
    != same usable recovery margin

known failure location
    != unknown errant-source problem

retained parity bytes
    + fault-location/admissibility evidence
    -> operational recoverability
```

The 1995 EVENODD abstract independently confirms that the named scheme's published scope also included a one-column-in-error decoder, while leaving the full algorithm and mixed-fault limits for future page-level work.

That is the complete claim of this deepening.