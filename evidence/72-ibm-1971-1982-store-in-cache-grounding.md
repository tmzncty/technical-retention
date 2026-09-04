# Case 72 grounding record — IBM store-in cache, 1971–1982

## Result

**Promote Case 72 directly as `grounded`.**

The bounded question is supported by two independent IBM period-primary source classes — a 1971-filed patent with explicit store-bit/currentness semantics and a January 1982 IBM engineering paper for the named 3081 production machine — plus a contemporary high-quality scholarly survey that controls later `copy-back` / `dirty bit` vocabulary.

## Research question

> When a cache can become newer than main storage, what retained state tells the machine that the backing copy is stale, and what must happen before the modified cache embodiment can be replaced or another requester can safely use the backing address?

This is the specific gap Case 08 left open. Case 08's Model 85 always updates main storage on a store; Case 72 tests the opposite authority relation without turning the project into a general cache-coherence history.

## Source A — IBM US3735360A, filed 1971-08-25

**Type:** manufacturer-primary patent / period design record.

**URL:** <https://patents.google.com/patent/US3735360A/en>

**Directly inspected anchors:**

- bibliographic record: IBM assignee; filed 25 August 1971; published 22 May 1973;
- `Prior Art`: the patent says there were currently three store-handling methods, naming store-through, store-wherever, and the store-in-buffer method to which the invention is primarily adapted;
- description of `store bit 56`: set by a processor store into the private buffer; binary one means that the private block has been modified and is no longer identical to the block retained in shared main storage;
- replacement path: when a valid block selected for replacement has been stored into, transfer to shared storage is initiated before replacement; resetting the store bit then records renewed agreement;
- multiprocessor request path: when another processor's private copy is modified, the source requires transfer back to shared storage so the requester receives the most current value;
- claim language: private→shared transfer is conditioned on the private block having been stored into and therefore differing from shared storage;
- summary: the store bit allows transfer to be omitted for an unmodified block.

**Evidence strength:** high for the disclosed 1971 IBM design and terminology.

**Limits:**

- patent evidence is not proof of deployment in a named machine;
- the source itself blocks an IBM-first `store-in` claim by treating the store-policy class as prior art;
- `store bit 56` must not be asserted as the exact 3081 directory implementation without a source linking them.

## Source B — Gustafson & Sparacio, IBM 3081, January 1982

**Type:** manufacturer-primary engineering paper for a named production processor.

**Citation:** R. N. Gustafson and F. J. Sparacio, “IBM 3081 Processor Unit: Design Considerations and Design Process,” *IBM Journal of Research and Development* 26(1), January 1982, pp. 12–21.

**Inspected copy:** <https://bitsavers.org/pdf/ibm/IBM_Journal_of_Research_and_Development/261/ibmrd2601C.pdf>

**Directly inspected anchors:**

- printed p. 15: the buffer control element contains a 32-Kbyte cache with a store-in-cache algorithm, 128-byte lines, four-way set associativity, and LRU replacement;
- printed p. 16: IBM says store-in-cache was selected over store-through for the relevant central-storage access-time/performance regime;
- printed p. 16: changed data can reside in CP caches, making central-storage content `not always valid`;
- printed p. 16: the system controller keeps duplicate CP-cache directory information and determines whether a central-storage request would return valid data;
- printed p. 16: on conflict the SC initiates casting out the specific line from cache to central storage and the requesting unit then refetches it;
- printed p. 16: cache lines carry read-only (RO) or exclusive (EX) status; EX is required before a store can complete, one EX copy is permitted, and multiple RO copies may coexist while no store occurs.

**Evidence strength:** high for the named 3081 production retention/currentness relation.

**Limits:**

- the paper is sufficient for system-level semantics, not transistor-level directory-cell implementation;
- it does not make the 1971 patent and 3081 one implementation artifact;
- its checkpoint/retry mechanism is adjacent but intentionally outside this bounded case.

## Source C — Alan Jay Smith, “Cache Memories,” 1982

**Type:** high-quality contemporary scholarly survey / terminology and comparison control.

**Publisher record:** <https://dl.acm.org/doi/10.1145/356887.356892>

**Inspected page-preserving copy:** <https://people.engr.tamu.edu/djimenez/taco/utsa-www/cs5513-fall07/reader/smith-cache-memories.pdf>

**Directly inspected anchors:**

- §2.5 identifies two general main-memory update approaches: write/store-through versus copy-back;
- printed p. 501 says copy-back writes main memory when a replaced line has been modified and defines a dirty bit as indicating cache modification;
- the same section distinguishes consistency/reliability consequences of store-through and copy-back;
- printed p. 502 explicitly lists IBM 3081 as using copy-back while IBM 370/168 and 3033 use store-through.

**Evidence strength:** strong secondary corroboration and period taxonomy.

**Limits:** the survey is not substituted for IBM primary evidence where the exact 3081 mechanism is at issue.

## Prior-art boundary

The most important novelty control comes from IBM's own 1971 source: it explicitly calls three store-policy methods current prior art and includes the store-in-buffer class. Therefore:

- **do not claim** IBM 1971 invented write-back/store-in caching;
- **do not claim** IBM 3081 was the first copy-back machine;
- **do not claim** the generic dirty-bit concept originates in this patent;
- **do claim only** that the 1971 IBM disclosure gives unusually explicit period-primary metadata semantics and that the 1982 3081 paper independently demonstrates the same class of currentness inversion in a named machine.

A full Conti / Amdahl / IBM / DEC cache-write-policy genealogy belongs in `computing-archaeology` or a later dedicated historical slice.

## Cross-case control

### Case 08 — IBM System/360 Model 85

Case 08 grounds a transparent fast copy under a store policy where main storage is updated on every store. It therefore establishes:

```text
cache replacement
    -> derivative copy can be dropped
    -> no payload writeback is required to preserve the architectural value
```

Case 72 establishes a different relation:

```text
cache-local modification
    -> cache may become newer than backing storage
    -> modified/currentness metadata must survive
    -> replacement or conflicting request may require castout first
```

This is a genuine cross-case difference in retention authority, not merely a new cache-performance parameter.

### Case 04 — mapped Flash

Functional analogy only: both can preserve a stable logical designation while the embodiment that currently counts changes. The mechanisms, fault models, latency scales, and historical genealogies differ.

### Distributed-currentness cases

Functional analogy only: a physically surviving copy can fail the system's currentness/admissibility rule. This does not make cache directories ancestors or instances of distributed consensus/version protocols.

## Evidence classification

| Proposition | Label | Grounding |
| --- | --- | --- |
| store-in is an existing store-policy class by the 1971 IBM filing | H/P | US3735360A prior-art section |
| IBM's `store bit` can mark private/shared divergence | H/P | US3735360A description and claims |
| modified private replacement triggers transfer to shared storage in the disclosed design | H/P | US3735360A replacement path |
| the 3081 uses store-in-cache | H/P | Gustafson & Sparacio 1982 pp. 15–16 |
| 3081 central storage can be stale/invalid while cache holds changed data | H/P | Gustafson & Sparacio 1982 p. 16 |
| 3081 conflict handling can cast out then refetch | H/P | Gustafson & Sparacio 1982 p. 16 |
| physical backing-copy survival does not establish current authority | E | follows from supported divergence/currentness mechanism |
| modified-state metadata can encode a future preservation obligation | E | follows from store-bit + replacement semantics |
| cache-local currentness is analogous to nonvolatile persistence | X | explicitly rejected; no power-fail evidence |
| `store bit` and `dirty bit` are historically interchangeable terms in 1971 IBM vocabulary | X | rejected by source terminology control |
| IBM invented copy-back/write-back caching | X | contradicted by the patent's own prior-art framing |
| castout is secure physical erase | X | no sanitization evidence |

## Related-repository check

Before drafting, code searches in `tmzncty/computing-archaeology` for `3081`, `store-in cache`, and `cache` returned no dedicated case. The current contribution is therefore not a duplicate of an existing technical-history package.

If a broad cache-history line is later built there, this case should link to it and keep only the retention/currentness analysis.

## Promotion rationale

The case can be `grounded` now because the central historical mechanism is triangulated without an invention claim:

1. a period IBM patent explicitly defines modified private/shared divergence and the metadata-conditioned transfer obligation;
2. a named 1982 IBM production-machine paper independently says store-in-cache can make central storage not always valid and documents castout/currentness control;
3. a contemporary ACM survey confirms the generic copy-back/dirty-bit taxonomy and independently classifies the IBM 3081 in that family;
4. the exact 1971-patent-to-3081 implementation identity is explicitly withheld;
5. power-fail durability, exact hardware bit-cell design, full coherence genealogy, and fault injection remain outside the bounded claim.

## Remaining work that does not block this case

- exact IBM 3081 Functional Characteristics / theory-of-operation pages for directory/change-bit fields;
- exact 3081 castout fault/retry traces or independent hardware experiments;
- Amdahl / IBM / DEC write-policy genealogy before and after 1971;
- line/subline dirty-bit implementation history;
- multiprocessor coherence-protocol genealogy and later MESI-family state machines;
- cache error-correction and power-loss behavior.
