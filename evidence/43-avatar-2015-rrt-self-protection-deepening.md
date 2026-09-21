# Case 43 Deepening — AVATAR RRT Placement, Self-Protection, and Policy-State Lifetime (2012–2015)

## Purpose

This evidence slice deepens [`../cases/43-avatar-vrt-aware-dram-refresh-feedback.md`](../cases/43-avatar-vrt-aware-dram-refresh-feedback.md) around one bounded question:

> What changes when the metadata that decides **how aggressively DRAM should be refreshed** can itself be stored in DRAM and therefore needs protection from the same retention instability it describes?

The existing Case 43 record already establishes AVATAR's feedback loop:

```text
initial retention profile
    -> Row Refresh Table (RRT)
    -> runtime ECC / scrub observation
    -> row upgrade to Fast Refresh
    -> later retention test / possible downgrade
```

This slice does not repeat that mechanism. It isolates the **placement, representation, protection, and lifetime of the RRT itself**.

The main historical source is the original AVATAR paper. RAIDR (ISCA 2012), explicitly cited and compared by AVATAR, is used as a controlled prior-art comparison for policy-metadata placement and representation.

---

## Status

**Evidence maturity: grounded deepening.**

This record supports a narrower claim than “AVATAR protects its metadata perfectly.” The paper explicitly proposes an optional DRAM-resident RRT and triplication against VRT-related errors in that RRT, but it does **not** specify a complete voting, repair, reboot, or crash-recovery protocol for the replicated metadata.

Case 43 therefore remains **`grounded`**. No maturity promotion is warranted from this slice.

---

# Historical record

## 1. AVATAR's multirate-refresh state is a one-bit-per-row RRT

Qureshi et al., **“AVATAR: A Variable-Retention-Time (VRT) Aware Refresh for DRAM Systems”** (DSN 2015), describe a generic multirate-refresh implementation in which retention testing populates a `Refresh Rate Table` / `Row Refresh Table` (`RRT`). At runtime, the table determines whether rows use `SlowRefresh` or `FastRefresh`.

For the paper's 8 GB DIMM / 8 KB row-buffer example, the RRT is **128 KB**. The paper says that for its target refresh-rate distribution, **10% or more of rows** can be classified for Fast Refresh, so a one-bit-per-row RRT is used rather than the Bloom-filter representation employed by RAIDR for a much sparser weak-row set.

The paper's figure encodes:

```text
0 = SlowRefresh
1 = FastRefresh
```

and its AVATAR design later updates that state at runtime when ECC or scrubbing reveals a correctable failure.

### Evidence boundary

The 128 KB value belongs to the paper's stated 8 GB / 8 KB-row organization. It is not a universal RRT size for every DRAM system.

The paper's use of one bit per row is a research-design choice for the studied weak-row fraction, not a JEDEC requirement.

---

## 2. The paper distinguishes decision locus from storage locus

The AVATAR paper says that, for its studies, RRT information is assumed to be **available at the memory controller**, similar to RAIDR.

A footnote then gives an alternative physical placement intended to avoid the SRAM cost of keeping the whole RRT in controller SRAM:

- store the RRT in a **reserved area of DRAM**;
- while refresh decisions for the current RRT line, covering **512 rows**, are being used, prefetch the next RRT line from DRAM;
- use this prefetch to hide RRT lookup latency.

This is historically important because it prevents a common collapse:

```text
policy is consumed by the memory controller
    !=
all policy bits must physically reside in controller SRAM
```

The paper explicitly permits a split arrangement in which the controller is the decision locus while the larger policy table can be backed by the DRAM that the policy governs.

### Arithmetic reconstruction

One RRT bit per row means a 512-row RRT line contains 512 policy bits, i.e. 64 bytes. This 64-byte quantity is a direct arithmetic consequence of the paper's stated 512-row grouping, not an independently named AVATAR object in the paper.

No claim is made here that the paper specifies a particular cache-line protocol, coherence mechanism, or exact controller buffer implementation for this prefetched metadata.

---

## 3. DRAM-resident RRT state is explicitly recognized as vulnerable

The most important sentence for technical-retention purposes is in the same footnote. The authors say that an RRT stored in DRAM **can be replicated three times** to tolerate **VRT-related errors in the RRT**.

They report a total storage overhead of approximately **0.005%** for this replicated RRT arrangement.

This is not an inference that “metadata might also fail.” The primary source explicitly recognizes that the control metadata can suffer the same class of VRT-related retention error that motivates AVATAR for payload data.

The documented structure is therefore:

```text
DRAM payload
    -> needs refresh policy because retention varies

refresh policy
    -> represented by RRT bits

optional RRT backing store
    -> can itself live in DRAM
    -> can itself suffer VRT-related errors
    -> therefore may itself require redundancy
```

This is a direct historical record of a second-order protection problem.

---

## 4. AVATAR does not specify the full replicated-RRT protocol

The paper states that the DRAM-resident RRT **can be replicated three times** for tolerating VRT-related RRT errors. In the bounded text inspected for this slice, it does not specify:

- the exact placement of the three copies;
- whether copies are placed in different banks/ranks/chips;
- the read-selection or voting algorithm;
- whether a majority vote is performed on every RRT lookup;
- when a damaged copy is repaired;
- whether a detected disagreement upgrades the row that stores RRT metadata;
- how the three copies are updated when AVATAR upgrades a row to Fast Refresh;
- ordering/atomicity requirements across those updates;
- behavior if a reset or power loss interrupts an update;
- whether the RRT's own DRAM rows are forced to a conservative refresh class.

Therefore:

```text
triplication proposed
    !=
complete replicated-state protocol specified
```

This slice treats triplication as a documented protection option, not as proof of crash consistency or Byzantine-style replicated-state correctness.

---

## 5. Runtime AVATAR updates make the RRT more than a static manufacturing profile

AVATAR's design section states that initial retention testing populates the RRT. During operation, if any word in a row encounters a correctable ECC error, AVATAR upgrades the row to `Fast Refresh`; scrub-triggered corrections feed the same path.

The paper also proposes infrequent retention testing, evaluated around a yearly interval, so that rows can later be downgraded when testing supports doing so.

Therefore the RRT is not merely a static table loaded once and never changed:

```text
initial profile state
    -> conservative runtime upgrades
    -> later revalidation / possible downgrade
```

That matters for the DRAM-resident placement option. Protecting a static copy and maintaining a mutable replicated table are not the same engineering problem.

The source establishes mutability of the logical RRT and separately proposes DRAM triplication. It does **not** provide the update protocol needed to prove that all three physical copies remain mutually consistent through every runtime transition.

---

# Prior art and controlled comparison: RAIDR (2012)

## 6. RAIDR stores sparse retention bins in the memory controller

Jamie Liu, Ben Jaiyen, Richard Veras, and Onur Mutlu, **“RAIDR: Retention-Aware Intelligent DRAM Refresh”** (ISCA 2012), precedes AVATAR and is explicitly cited by the AVATAR paper.

RAIDR groups rows into retention-time bins and stores those bins in the memory controller using Bloom filters. Its evaluated two-bin configuration reports **1.25 KB** of controller storage for a 32 GB system.

RAIDR's representation is designed for a regime in which only a small number of rows belong to the shorter-retention bins. AVATAR explicitly notes that Bloom filters lose their storage advantage when the fraction of rows needing Fast Refresh grows into the several-percent range; for its target case, AVATAR therefore uses one RRT bit per row.

This gives a historically grounded representation tradeoff:

```text
sparse exceptional set
    -> compact Bloom-filter membership state

larger and dynamically changing FastRefresh set
    -> direct one-bit-per-row RRT
```

The comparison is not a claim that AVATAR simply “replaced RAIDR's data structure.” AVATAR addresses VRT-driven runtime adaptation and has different update requirements.

---

## 7. RAIDR's Bloom-filter false positives are intentionally one-sided at the abstract-set level

RAIDR explains that a Bloom filter may yield a **false positive**, causing a row to appear in a shorter-retention bin even if it was not inserted. In RAIDR's refresh policy this means the row may be refreshed **more frequently than necessary**.

The paper emphasizes the complementary property of the Bloom-filter abstraction: inserted elements do not produce false negatives through the normal set-representation semantics, so a genuinely weak row is not omitted merely because of hash collisions.

For retention policy, the abstract error direction is therefore conservative:

```text
representation false positive
    -> extra refresh work
    -> efficiency loss
    -> not under-refresh
```

This is a useful contrast with AVATAR's explicit one-bit state:

```text
RRT encoding:
    1 = FastRefresh
    0 = SlowRefresh
```

If an **unprotected physical bit corruption** changed a logically required `1` into `0`, the policy-level consequence could be under-refresh. This is an engineering reconstruction from the documented encoding, and it helps explain why the AVATAR paper explicitly raises protection of a DRAM-resident RRT.

### Critical non-claim

Bloom filters have no false negatives **under their algorithmic membership semantics**. That does **not** mean a Bloom-filter bit array is immune to physical bit flips. A hardware error that changes a stored Bloom-filter bit can violate the abstract data structure's assumptions.

Therefore this slice does not claim:

> RAIDR's controller-resident Bloom filter is intrinsically fault-proof.

It compares logical representation error semantics, not arbitrary storage-fault semantics.

---

## 8. RAIDR explicitly separates long-lived profiling results from runtime controller state

RAIDR states that, after row retention times are measured, the results can be saved by the operating system in a file and restored to the memory controller on future boot-ups, avoiding repeated profiling under the paper's assumption that retention time does not significantly change over a DRAM cell's lifetime.

For permanently coupled 3D-stacked DRAM/eDRAM arrangements, RAIDR even discusses storing profile results permanently in controller fuses or ROM because the attached DRAM does not change.

This is a useful historical contrast with AVATAR:

```text
RAIDR 2012 baseline assumption
    measured profile can be retained and reused across boots

AVATAR 2015 problem statement
    some cells' relevant retention behavior changes at runtime via VRT
    runtime errors therefore revise refresh-class state
```

AVATAR's bounded paper does not, in the passages inspected here, specify whether runtime FastRefresh upgrades are persisted across a reboot, discarded with the volatile memory epoch, reconstructed by fresh testing, or combined with a saved baseline profile.

Thus:

```text
logical policy table exists at runtime
    !=
its cross-reboot persistence contract is specified
```

No persistence behavior is invented where the paper is silent.

---

# Engineering reconstruction

## 9. Maintenance metadata can become first-class retention payload

When the RRT is stored in controller SRAM, it is control state external to the DRAM payload substrate.

When the optional placement stores that RRT in reserved DRAM, a relation changes:

```text
metadata describing how DRAM must be retained
    -> is itself represented by DRAM charge
    -> therefore itself requires retention service
```

The distinction is:

```text
payload retention
    !=
retention of the policy that schedules payload retention
```

but both can share the same physical failure substrate.

This is the narrow sense in which the RRT becomes **second-order retention state**.

That phrase is a repository engineering term, not vocabulary attributed to Qureshi et al.

---

## 10. Decision locus, backing-store locus, and protection locus are separate

The source supports at least three distinct questions:

1. **Where is a refresh decision made?** — memory controller.
2. **Where can the larger RRT representation be stored?** — optionally reserved DRAM rather than all-SRAM.
3. **How can that DRAM-resident representation be protected?** — the paper suggests three replicas against VRT-related RRT errors.

These should not be collapsed:

```text
controller decides
    !=
controller physically stores the complete table

metadata in DRAM
    !=
metadata left unprotected

metadata replicated
    !=
replica-consistency protocol proven
```

This decomposition is useful across the repository because many systems consume policy state in one component while backing it in another.

---

## 11. Self-hosting creates a recursive service dependency

A DRAM-resident RRT has a structurally recursive relation:

```text
RRT bit says how often row X must be refreshed
    ↓
RRT bit itself resides in some DRAM row Y
    ↓
row Y also needs adequate refresh
```

The source directly establishes DRAM placement and vulnerability; the recursive dependency is an engineering reconstruction.

The paper does not fully resolve, in the inspected text, questions such as:

- what policy protects row Y before its RRT metadata is available;
- whether RRT-resident rows always use the conservative baseline rate;
- whether RRT storage is excluded from the optimized refresh regime;
- whether a separate bootstrap map exists.

These are therefore retained as open implementation questions rather than silently filled in.

The supported conclusion is only:

> once maintenance metadata is placed on the maintained substrate, its own service conditions become part of the retention design.

---

## 12. Prefetching changes availability requirements without changing semantic authority

The paper proposes using the current RRT line while prefetching the next line from DRAM. This makes policy metadata availability part of the refresh scheduling path.

A useful decomposition is:

```text
RRT semantic state
    !=
currently staged RRT line
    !=
next-line prefetch state
```

Losing or delaying a prefetched line is not, by itself, proof that the underlying RRT semantic state was destroyed; conversely, preserving the backing bits does not prove that the controller always had the required policy data available at the required decision time.

The paper proposes prefetch to hide lookup latency but does not provide a full deadline/fault analysis for missed or corrupted prefetches.

Therefore:

```text
state retained
    !=
state available at the time of decision
```

This is an engineering reconstruction, not an AVATAR-authored theorem.

---

## 13. Policy-bit corruption has asymmetric semantic consequences

With the documented encoding:

```text
0 = SlowRefresh
1 = FastRefresh
```

not all logical misclassifications have the same consequence.

A wrong `0 -> 1` classification spends extra refresh work. A wrong `1 -> 0` classification can cause a row that needs Fast Refresh to receive Slow Refresh.

Thus:

```text
classification error
    !=
uniform consequence
```

and, at the policy level:

```text
false-fast
    -> conservative inefficiency

false-slow
    -> potential retention risk
```

This directionality is reconstructed from the paper's encoding and refresh semantics. The AVATAR paper does not present a measured RRT-bit fault-injection study quantifying either outcome.

Triplication is therefore historically relevant, but the repository does not infer a quantified residual error rate from it.

---

## 14. Mutable replicated policy state has an update-consistency problem distinct from data redundancy

AVATAR's logical RRT is mutable because runtime ECC/scrub can upgrade rows and later testing can downgrade them.

If three copies are used, a practical implementation must decide when the copies become authoritative relative to one another.

Potential questions include:

```text
upgrade discovered
    -> update copy A
    -> update copy B
    -> update copy C
    -> when is the new policy effective?
```

and similarly for downgrade.

The source does not provide this state machine. Consequently this record does **not** claim:

- atomic three-copy updates;
- linearizable RRT semantics;
- majority-vote read repair;
- write ordering guarantees;
- crash consistency;
- persistence across controller reset.

The important distinction is:

```text
redundant representation
    !=
consistent mutable representation
```

---

# Functional analogy

## 15. Bounded analogy to “metadata protecting metadata” systems

A functional analogy can be made to other systems in this repository where maintenance authority or recovery work depends on metadata that itself needs protection.

The common relation is:

```text
payload cannot be maintained correctly
unless control metadata remains valid
```

This resembles, at a very abstract level:

- SSD/controller metadata that tells garbage collection or refresh work what to do;
- distributed-storage metadata that records which cleanup obligations remain;
- filesystems that protect allocation/recovery metadata separately from user blocks.

The analogy stops at dependency structure. AVATAR's RRT is not historically derived from those systems, and its failure model is DRAM VRT rather than flash wear, crash recovery, or distributed consensus.

No genealogy is asserted.

---

## 16. Controlled comparison with RAIDR is historically stronger than a generic analogy

RAIDR is not merely an analogy: it is explicit prior art cited by AVATAR, and the AVATAR footnote directly compares its RRT representation with RAIDR's Bloom filters.

Still, the historically supported relation is limited:

```text
RAIDR
    sparse weak-row bins
    Bloom-filter representation
    controller-resident state
    profile may be saved/restored across boots

AVATAR
    larger FastRefresh population in target regime
    direct one-bit-per-row RRT
    runtime upgrades/downgrades
    optional reserved-DRAM backing
    optional triple replication for VRT errors in RRT
```

This does not prove a simple linear evolution in commercial products, and it does not show that any shipped memory controller implemented either exact research design.

---

# Philosophical interpretation

## 17. The state that says “how to remember” can itself need remembering

The narrow conceptual pressure from this slice is recursive:

> A system may preserve payload by retaining a description of how aggressively that payload must be maintained; if that description is stored on the same fallible substrate, the description itself becomes an object of retention.

The resulting chain is:

```text
remember payload
    requires
remember maintenance policy
    may require
protect the representation of maintenance policy
```

This is a philosophical/engineering interpretation of the documented design relation. It is not language used by the AVATAR authors, and it should not be turned into anthropomorphic claims about DRAM “remembering how to remember.”

---

# Cross-case result

## 18. Case 43 now has two distinct feedback problems

The existing case establishes **semantic feedback**:

```text
substrate behavior changes
    -> observed correctable failure
    -> revise row refresh class
```

This deepening adds **representation feedback/protection**:

```text
row refresh class is represented as metadata
    -> metadata can live on the same volatile substrate
    -> metadata can suffer retention errors
    -> metadata representation therefore needs protection too
```

Together they show two independent ways a maintenance policy can fail:

```text
policy meaning becomes stale
    !=
policy representation becomes corrupted
```

AVATAR addresses the first with runtime ECC/scrub-driven reclassification and later testing; it acknowledges the second for a DRAM-resident RRT by proposing triplication.

The source does not show that these two protections form a completely closed fault-tolerant system under every reset, crash, or multi-copy fault.

---

# Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| AVATAR uses an RRT with one-bit Slow/Fast row classification in its studied multirate-refresh design | Historical record | original paper |
| The 8 GB / 8 KB-row example has a 128 KB RRT | Historical record | original paper |
| For the target case, 10% or more rows can require Fast Refresh, making Bloom-filter storage less attractive | Historical record | original paper footnote |
| RRT information is assumed available at the memory controller | Historical record | original paper |
| The paper proposes optionally storing the RRT in reserved DRAM to avoid SRAM overhead | Historical record | original paper footnote |
| The next RRT line can be prefetched while decisions for the current 512-row RRT line are used | Historical record | original paper footnote |
| A DRAM-resident RRT can be replicated three times to tolerate VRT-related RRT errors | Historical record | original paper footnote |
| The paper reports roughly 0.005% total storage overhead for the triplicated DRAM-resident RRT option | Historical record | original paper footnote |
| AVATAR's logical RRT is mutable through ECC/scrub upgrades and later retention-test downgrades | Historical record | original design section |
| RAIDR stores sparse retention bins using Bloom filters in the memory controller | Historical record | RAIDR 2012 |
| RAIDR profile results may be saved by the OS and restored on future boots under RAIDR's static-retention assumption | Historical record | RAIDR 2012 |
| RAIDR Bloom-filter false positives cause extra refresh rather than under-refresh under the abstract data-structure semantics | Historical record / Engineering reconstruction | RAIDR discussion of false positives/no false negatives and refresh consequences |
| Controller decision locus and complete-table physical storage locus are separable | Engineering reconstruction | derived from AVATAR controller-availability + DRAM-backing statements |
| A DRAM-resident RRT is second-order retention state | Engineering reconstruction | project terminology |
| `0 -> 1` and `1 -> 0` policy corruptions have asymmetric consequences | Engineering reconstruction | derived from documented encoding and refresh semantics |
| Triplication by itself proves atomic updates or crash consistency | **Not established** | protocol not specified |
| AVATAR specifies cross-reboot persistence of runtime row upgrades | **Not established** | bounded source is silent |
| AVATAR specifies how RRT-hosting rows are bootstrapped/refreshed before RRT lookup is available | **Not established** | bounded source is silent |
| RAIDR Bloom filters are physically immune to bit corruption | **False / unsupported generalization** | no-false-negative property assumes normal Bloom-filter semantics, not arbitrary hardware faults |
| AVATAR or RAIDR was commercially deployed exactly as proposed | **Not established** | research designs |

---

# Explicit non-claims

This slice does **not** claim that:

1. AVATAR invented retention-aware refresh;
2. AVATAR invented redundant metadata;
3. the optional DRAM-resident RRT was used in a commercial controller;
4. every AVATAR implementation must place the RRT in DRAM;
5. the paper's 128 KB figure applies to arbitrary memory capacities;
6. the three RRT replicas necessarily use majority voting;
7. the three replicas are placed in independent fault domains;
8. the paper specifies read repair;
9. the paper specifies write repair;
10. triplication provides crash consistency;
11. triplication provides protection against every multi-bit or correlated fault;
12. triplication provides protection against controller logic faults;
13. the paper specifies atomic upgrade/downgrade of all copies;
14. the RRT is itself protected by SECDED in the proposed DRAM placement;
15. RRT rows necessarily use Fast Refresh;
16. RRT rows necessarily participate in the same optimized refresh policy as ordinary rows;
17. the paper specifies a bootstrap map for locating/protecting RRT rows;
18. prefetched RRT lines are architecturally caches in any particular commercial sense;
19. a missed prefetch necessarily destroys policy state;
20. preservation of backing bits proves timely availability at the controller;
21. RAIDR's no-false-negative Bloom-filter property survives arbitrary physical bit flips;
22. AVATAR's one-bit RRT is less reliable than RAIDR's Bloom filters in all physical implementations;
23. controller SRAM is nonvolatile across power loss;
24. DRAM-resident RRT copies survive power loss;
25. AVATAR persists runtime upgrades across reboot;
26. AVATAR intentionally discards runtime upgrades across reboot;
27. the yearly retest interval is a JEDEC requirement;
28. the AVATAR modeled reliability figures are deployed field lifetimes;
29. AVATAR and distributed-storage metadata have a historical design genealogy;
30. recursive control-state protection implies human-like self-knowledge or self-awareness.

---

# Open debts exposed by this slice

The highest-value follow-up questions are now narrower:

1. **Replicated-RRT read semantics** — find any author artifact, simulator code, dissertation, or follow-on paper that specifies how three copies are read and reconciled.
2. **Replicated-RRT update semantics** — determine whether runtime row upgrades/downgrades have an ordering or repair protocol across copies.
3. **Bootstrap protection** — determine how RRT-hosting rows are refreshed/classified before or while RRT metadata is staged.
4. **Epoch/reboot lifetime** — determine whether AVATAR runtime upgrades are intended to survive reboot, and if so in what representation.
5. **Fault injection** — construct a small model separating `Fast -> Slow` corruption, `Slow -> Fast` corruption, replica disagreement, and missed RRT-line availability.
6. **Representation comparison** — quantify the safety/performance consequences of exact RRT bits, Bloom-filter false positives, and physically corrupted membership metadata without conflating algorithmic and storage faults.

These are implementation/evidence debts, not reasons to inflate the current case status.

---

# Sources

## Primary — AVATAR

Moinuddin K. Qureshi, Dae-Hyun Kim, Samira Khan, Prashant J. Nair, and Onur Mutlu, **“AVATAR: A Variable-Retention-Time (VRT) Aware Refresh for DRAM Systems,”** 45th Annual IEEE/IFIP International Conference on Dependable Systems and Networks (DSN), 2015, pp. 427–437, DOI `10.1109/DSN.2015.58`.

Author / institutional mirrors inspected:

- <https://users.ece.cmu.edu/~omutlu/pub/avatar-dram-refresh_dsn15.pdf>
- <https://memlab.ece.gatech.edu/papers/DSN_2015_1.pdf>

Key inspected locations:

- multirate-refresh RRT implementation and footnote on one-bit-per-row storage, reserved-DRAM placement, prefetch, and three replicas: printed pp. 429–430 / PDF page around the paper's Section II-C;
- AVATAR design, ECC/scrub upgrade path, and infrequent retention testing: printed pp. 433–434 / Section VI-A.

## Primary — prior art comparison

Jamie Liu, Ben Jaiyen, Richard Veras, and Onur Mutlu, **“RAIDR: Retention-Aware Intelligent DRAM Refresh,”** Proceedings of the 39th Annual International Symposium on Computer Architecture (ISCA), 2012.

Author / institutional mirrors inspected:

- <https://users.ece.cmu.edu/~omutlu/pub/raidr-dram-refresh_isca12.pdf>
- <https://www.pdl.cmu.edu/PDL-FTP/NVM/raidr-isca12_abs.shtml>

Key inspected locations:

- controller-resident retention bins and 1.25 KB evaluated overhead;
- OS file saving/restoration of profiling results across future boots;
- Bloom-filter representation and its false-positive/no-false-negative abstract semantics;
- discussion of permanent profile storage in fuses/ROM for permanently coupled 3D/eDRAM designs.

---

# PDF inspection note

Page-resolved text from both original author-hosted PDFs was inspected. The available screenshot endpoint successfully rendered the relevant RAIDR implementation page. Screenshot retrieval for the AVATAR PDF mirrors was attempted but the endpoint returned a cache-miss error; no claim in this record depends uniquely on visual interpretation of an AVATAR figure. The RRT placement/replication statements are present in the extracted primary-source text.

---

# Related-repository check

Before writing this slice, `tmzncty/computing-archaeology` was searched for `AVATAR`, `VRT`, `RRT`, and DRAM retention-refresh coverage. No dedicated reusable packet was found.

Accordingly, this record keeps only the retention-specific relation:

```text
maintenance-policy metadata
    can share the failure substrate it governs
    and therefore needs its own protection/lifetime contract
```

A broader history of DRAM refresh research, controller architecture, RAIDR/AVATAR genealogy, or commercial adoption remains appropriate for `computing-archaeology` rather than being duplicated here.
