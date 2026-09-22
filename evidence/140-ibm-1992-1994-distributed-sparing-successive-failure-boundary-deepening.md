# Evidence 140E — IBM 1992–1994 distributed sparing / successive-failure boundary

**Status:** bounded deepening complete; Case 140 remains `grounded`  
**Case:** [`../cases/140-ibm-double-disk-failure-array-codes.md`](../cases/140-ibm-double-disk-failure-array-codes.md)  
**Claim layer:** historical record + engineering reconstruction + bounded functional analogy  
**Primary question:** when early-1990s IBM disk-array work says an array can be rebuilt into distributed spare space and then sustain later failures, what is actually established about redundancy restoration, layout identity, and a second failure that arrives **before** rebuild finishes?

## Why this slice exists

The existing Case 140 packets establish two different coding facts:

1. early IBM array-code work explicitly targeted up to two unavailable disks/DASDs;
2. the same physical parity budget can have different usable recovery margins for known erasures versus an unknown erroneous source.

That still leaves a temporal ambiguity.

A code may be capable of reconstructing two missing members in its stated model, but operational recovery also has a time axis:

```text
member fails
    -> degraded operation
    -> reconstruction / rebuild
    -> reconstructed material written into spare capacity
    -> post-rebuild layout becomes the new operating layout
```

The important question is whether a source that discusses **successive failures** is proving:

```text
failure F1
    -> rebuild completes
    -> failure F2
```

or the harder overlap case:

```text
failure F1
    -> rebuild only partly complete
    -> failure F2
```

The IBM Research records inspected here strongly support the first relation. They do **not** by themselves establish the second.

This packet exists to keep those two situations separate.

---

## Claim-layer labels

- `H/P` — historical record from an original institutional/publisher record.
- `E` — engineering reconstruction made explicit from the cited mechanism.
- `A` — bounded functional analogy to another repository case.
- `P` — philosophical interpretation, clearly separated from historical claims.
- `X` — stop condition preventing an overclaim.

---

## Source custody

### P1 — Ng & Mattson, IEEE Transactions on Computers, 1994

Spencer W. Ng and Richard L. Mattson, **“Uniform Parity Group Distribution in Disk Arrays with Multiple Failures,”** *IEEE Transactions on Computers* 43(4), 1994, pp. 501–506.

- IBM Research institutional record: <https://research.ibm.com/publications/uniform-parity-group-distribution-in-disk-arrays-with-multiple-failures>
- DOI: <https://doi.org/10.1109/12.278490>
- IBM Research date: **1994-01-01**.
- The inspected public institutional page exposes the abstract, publication venue, authors, and DOI link.

The abstract states that:

- parity groupings can be uniformly distributed so extra work after a disk failure is shared across surviving disks;
- arrays may contain multiple spare disks so service calls can be deferred;
- in **distributed sparing**, spare space is distributed throughout the array;
- **after a rebuild the new array is logically different from the original array**;
- the paper presents an algorithm that maintains distributed-sparing arrays so repeated uniform parity-group distribution is obtained with **each successive failure**.

The evidence level here is deliberately bounded to what the public IBM Research record directly exposes. This packet does not pretend to have inspected every proof or intermediate-state algorithm in the closed IEEE body.

### P2 — Ng & Mattson, HPDC 1992

Spencer W. Ng and Richard L. Mattson, **“Maintaining Good Performance in Disk Arrays During Failure via Uniform Parity Group Distribution,”** HPDC 1992, pp. 260–269.

- IBM Research institutional record: <https://research.ibm.com/publications/maintaining-good-performance-in-disk-arrays-during-failure-via-uniform-parity-group-distribution>
- IBM Research date: **1992-09-09**.

The abstract states that a failed disk's data remains available through parity reconstruction, that rebuilding the repaired disk requires reconstructing its content from associated parity groups, and that their organization permits the reconstruction process to be broken into multiple parallel processes distributed across the array rather than remaining one sequential thread.

This gives a contemporaneous IBM research floor for treating **reconstruction work and its placement/scheduling** as a distinct operational problem rather than as a synonym for the code's bare reconstructability.

### P3 — Ng, Distributed and Parallel Databases, 1994

Spencer W. Ng, **“Sparing for Redundant Disk Arrays,”** *Distributed and Parallel Databases* 2(2), 1994, pp. 133–149.

- IBM Research institutional record: <https://research.ibm.com/publications/sparing-for-redundant-disk-arrays>
- DOI: <https://doi.org/10.1007/BF01267324>
- IBM Research date: **1994-04-01**.

The abstract states that spare drives can replace a failed drive expeditiously, that data may remain reconstructable from the surviving members while performance is degraded, and that it is desirable to leave degraded mode as quickly as possible.

For this packet, P3 is used to establish only a narrow boundary:

```text
fault-tolerant reconstructability
    !=
restoration from degraded mode
```

It is not used as proof of double-failure coding behavior.

### P4 — Menon, Distributed and Parallel Databases, 1994

Jai Menon, **“Performance of RAID5 Disk Arrays with Read and Write Caching,”** *Distributed and Parallel Databases* 2(3), 1994, pp. 261–293.

- IBM Research institutional record: <https://research.ibm.com/publications/performance-of-raid5-disk-arrays-with-read-and-write-caching>
- DOI: <https://doi.org/10.1007/BF01266331>
- IBM Research date: **1994-07-01**.

The abstract explicitly separates:

```text
normal mode
    = all disks operational

degraded mode
    = one disk broken, rebuild not started

rebuild mode
    = one disk broken, rebuild started but not finished
```

and develops models for rebuild time.

P4 concerns RAID5 performance, not Case 140's double-failure code. It is therefore retained as a **source-era terminology witness** showing that IBM-affiliated disk-array work treated `degraded` and `rebuild-in-progress` as different operational states. It does not prove Case 140 survives a second failure in either state.

---

## 1. Historical record: distributed sparing changes the post-rebuild array

P1's most useful sentence for retention research is not simply that distributed sparing exists.

It says that when spare spaces are distributed throughout the array:

> after a rebuild the new array is logically different from the original array.

The safe historical statement is:

```text
pre-failure / pre-rebuild array layout
    !=
post-rebuild distributed-sparing layout
```

while the system is nevertheless intended to remain a valid array capable of maintaining the desired parity-group distribution.

That is a concrete historical counterexample to an overly simple notion that recovery must restore the exact prior physical/logical placement before the array is again valid.

What survives is not necessarily an identical placement map.

What must survive is the information and redundancy relation required by the new valid layout.

The second sentence is engineering reconstruction (`E`), not source wording.

---

## 2. Historical record: `successive failure` is linked to repeated post-rebuild maintenance

P1 describes an algorithm for **constructing and maintaining** distributed-sparing arrays so that repeated uniform parity-group distribution is achieved with each **successive failure**.

Combined with its immediately preceding statement that the array is logically different **after a rebuild**, the strongest bounded reading is:

```text
valid layout L0
    -> failure F1
    -> rebuild into distributed spare space
    -> valid post-rebuild layout L1
    -> later failure F2
    -> maintain / reconstruct again
```

where:

```text
L1 != L0
```

in the source's own `logically different` sense.

This is useful evidence that the maintenance target can move between recovery episodes.

It is **not** enough evidence to rewrite `successive failure` as:

```text
F2 arrives at an arbitrary point while F1 rebuild is only partially complete
```

The public abstract does not state that intermediate case.

---

## 3. Historical record: reconstruction work has an operational duration

P2 says the failed disk's content must be reconstructed and describes a technique for parallelizing that reconstruction across the array.

P3 says spares help a system leave degraded operation quickly.

P4 goes further in terminology and explicitly defines a `rebuild mode` in which rebuild has **started but not finished**.

Together, without merging their specific array designs, these same-era IBM records establish an important historical engineering fact:

```text
rebuild was treated as a process with duration
```

rather than as an instantaneous consequence of `data is mathematically reconstructable`.

This matters to Case 140 because the open risk window lies exactly in that duration.

---

## 4. Engineering reconstruction: six different quantities must not be collapsed

For Case 140, the following are separate state dimensions:

```text
coding margin
    !=
spare capacity
    !=
rebuild admission
    !=
rebuild progress
    !=
post-rebuild placement
    !=
currentness of the reconstructed representation
```

### 4.1 Coding margin

The code determines which combinations of missing/erroneous symbols are mathematically recoverable under its stated model.

Existing Case 140 evidence handles this layer.

### 4.2 Spare capacity

Spare capacity supplies a destination for reconstructed material.

Adding a spare does not, by itself, add an independent parity equation.

### 4.3 Rebuild admission

The controller/system must decide or become able to start reconstruction.

No inspected source here establishes an atomic admission protocol.

### 4.4 Rebuild progress

Once started, only part of the failed member's logical content may have been reconstructed at an intermediate point.

P4 explicitly acknowledges a state where rebuild is started but unfinished, but does not provide Case 140's dual-failure behavior in that state.

### 4.5 Post-rebuild placement

P1 explicitly says distributed sparing can produce an array logically different from the original after rebuild.

Therefore successful recovery does not require restoring the former placement identity.

### 4.6 Currentness

A reconstructed block is useful only if it belongs to the current logical state and satisfies the current code/layout relation.

The inspected abstracts do not describe write-ordering, checkpoint, journal, generation, epoch, or validation machinery that would establish this layer across interrupted rebuild.

---

## 5. Engineering reconstruction: multiple spares do not enlarge the code equation budget

P1 observes that many arrays include multiple spare disks.

That is a capacity / serviceability fact.

It must not be converted into:

```text
number of spares
    = number of additional failures the code can mathematically tolerate
```

A spare starts as destination capacity rather than an additional independent redundancy equation carrying a current coded relation for every protected stripe.

So a useful bounded state model is:

```text
failure tolerance at time t
    = f(
        current valid coded fragments,
        code relation,
        known failure locations,
        rebuild progress,
        validity/currentness of rebuilt fragments
      )

not simply:

failure tolerance at time t
    = number of spare drives installed
```

This is an engineering reconstruction, not a formula supplied by the historical papers.

---

## 6. The central stop condition: `successive` is not `overlapping`

The evidence examined here supports:

```text
F1
    -> reconstruction/rebuild
    -> valid reconfigured array
    -> F2
```

It does **not** yet establish:

```text
F1
    -> partial rebuild
    -> F2
    -> guaranteed continuation/recovery
```

Those are different claims even for a code that can tolerate two unavailable members.

Why?

Because during partial rebuild the array may contain a mixture of:

- surviving old-layout fragments;
- reconstructed fragments already placed in distributed spare space;
- regions not yet rebuilt;
- metadata describing which mapping is authoritative;
- foreground writes that may have modified stripes while reconstruction proceeds.

That list is an engineering reconstruction of possible state classes, not a claim that the 1994 implementation used exactly such metadata.

To prove the overlap case, stronger evidence would need to establish how the implementation identifies the authoritative representation and how it resumes or completes after the second failure.

---

## 7. Cross-case comparison: Case 140 versus Case 17

Case 17 is the single-parity reconstruction boundary.

A single missing member may be reconstructable, but the array operates with no second member-loss margin in the same protection domain.

Case 140's early IBM coding line adds an explicit two-member erasure capability.

The new distributed-sparing slice adds a **different axis**:

```text
Case 140 coding question:
    can the surviving relation solve the missing members?

rebuild question:
    has reconstructed material been restored into a valid current layout?
```

A strong code does not make rebuild state disappear.

---

## 8. Cross-case comparison: Case 136 rebuild policy

Case 136 asks how rebuild work is scheduled and what rebuild-rate policy survives configuration/restart boundaries.

This Case 140 slice asks a prior structural question:

```text
what state exists between
    "still reconstructable"
and
    "rebuilt into a new valid redundancy layout"?
```

The relation is functional only.

No implementation genealogy is asserted between the 1990s IBM array work and later controllers.

---

## 9. Cross-case comparison: Synthesis 09 representation handoff

Synthesis 09 studies representation transitions in distributed/coded systems, including the difference between a conversion being possible and a crash-safe handoff being documented.

Distributed sparing provides a useful older functional analogue:

```text
old valid placement
    -> reconstruction / re-placement
    -> new valid placement
```

But the analogy stops there.

This packet does not claim that Ng & Mattson used modern epoch, transaction, journal, manifest, or two-phase handoff machinery.

---

## 10. Functional analogy: identity can survive re-placement

At the functional level only:

```text
logical payload identity
    !=
physical placement identity
```

P1 is a particularly clean source because it explicitly says the post-rebuild array is logically different from the original while presenting that result as a maintained array organization.

The useful retention analogy is that continuity may be carried by a valid relation and mapping rather than by restoration of the former embodiment.

No historical actor is claimed to have used this philosophical vocabulary.

---

## 11. Philosophical interpretation — clearly non-historical

A bounded philosophical reading is:

> Technical retention can preserve continuity through controlled reconfiguration rather than through material or placement sameness.

That interpretation is useful to the repository's broader thesis, but it is **not** a quotation, design objective, or source-era concept attributed to Ng, Mattson, or Menon.

The historical record stays narrower: distributed sparing can yield a logically different post-rebuild array, and the papers study how failure/rebuild work is distributed and repeated.

---

## 12. Explicit non-claims

This evidence packet does **not** establish any of the following:

1. `successive failure` means an arbitrary second failure during an incomplete first rebuild;
2. a second failure at every possible rebuild offset is recoverable;
3. rebuild-progress metadata survives controller crash or power loss;
4. the post-rebuild mapping is published atomically;
5. reconstructed fragments are validated by a named checksum/generation mechanism before becoming authoritative;
6. foreground-write ordering during rebuild is crash-safe;
7. old and new placement states coexist under an explicitly documented transactional handoff;
8. multiple spare disks provide additional independent parity equations;
9. uniform parity-group distribution proves data integrity or currentness;
10. a logically different array means the logical payload changed;
11. the cited algorithms shipped in a named IBM production controller;
12. the 1994 papers themselves used later `RAID-6` terminology for Case 140's double-failure code;
13. the distributed-sparing work is the direct ancestor of later dRAID, declustered parity, or distributed-storage repair designs;
14. sector-level URE, latent corruption, controller failure, cable/string failure, or arbitrary Byzantine faults are covered by the same model;
15. the IBM Research abstract is a substitute for inspecting the full IEEE algorithm/proof when a stronger claim depends on intermediate-state semantics;
16. completion of a rebuild restores the **original** placement — P1 directly warns that it may not.

---

## 13. What this closes in Case 140

Before this slice, the canonical case had an open item for **second-failure-during-rebuild fault behavior**.

This packet does not close that item completely.

It sharpens it into a testable distinction:

```text
supported by inspected 1992–1994 institutional records:
    reconstruction has duration
    distributed spare space can receive rebuilt content
    post-rebuild layout may differ from the original
    repeated maintenance across successive failures is a design target

still open:
    second failure while the first rebuild is incomplete
    + exact authority/currentness semantics for partially rebuilt regions
    + crash/restart persistence of rebuild progress
```

That is progress because `successive failures` no longer floats ambiguously between completed-rebuild episodes and overlap-failure episodes.

---

## 14. Next highest-value evidence

The next useful work is not another generic statement that RAID rebuilds take time.

Priority targets are:

1. direct inspection of the full 1994 IEEE paper for its precise successive-failure state transition and mapping algorithm;
2. full text or implementation material describing whether reconstruction metadata/checkpoints survive restart;
3. a named production controller/manual with documented behavior when a second member fails during rebuild;
4. fault-injection or service documentation for a second failure at different rebuild completion percentages;
5. write-path evidence showing how parity/currentness is preserved while user writes overlap reconstruction;
6. evidence distinguishing complete rebuild, spare activation, copyback, and restoration of the designed failure margin.

---

## 15. Related-repository boundary

A fresh search of `tmzncty/computing-archaeology` for:

- `Uniform Parity Group Distribution`
- `distributed sparing`

found no dedicated packet to reuse in this run.

Accordingly this file keeps only the retention-specific boundary:

```text
coding margin
    -> degraded operation
    -> rebuild progress
    -> reconfigured valid layout
    -> later failure margin
```

Broader history of IBM disk-array organizations, product lineages, controller architectures, declustering families, and the later RAID terminology should be developed in `computing-archaeology` rather than duplicated here.

---

## Bottom line

The inspected IBM records justify a stronger but narrower statement than `RAID rebuild restores a failed disk`:

> **Early distributed-sparing work explicitly allowed a successful rebuild to produce a logically different array and aimed to preserve good parity-group distribution across successive failures. That establishes recovery as a state-changing reconfiguration process, not restoration of placement identity. It does not, from the inspected public abstracts alone, prove the harder case of a second failure arriving while the first rebuild is only partially complete.**

For retention analysis, the seam is therefore:

```text
recoverable relation
    !=
spare capacity
    !=
rebuild started
    !=
rebuild complete
    !=
new layout authoritative
    !=
second-failure-during-rebuild safety proven
```
