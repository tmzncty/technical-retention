from pathlib import Path
import re
import subprocess
import textwrap

ROOT = Path('.')
CASE_PATH = ROOT / 'cases/72-ibm-store-in-cache-currentness-castout.md'
EVIDENCE_PATH = ROOT / 'evidence/72-ibm-1971-1982-store-in-cache-grounding.md'
WORKFLOW_PATH = ROOT / '.github/workflows/integrate-case72.yml'
SELF_PATH = ROOT / '.github/scripts/integrate_case72.py'


def clean(s: str) -> str:
    return textwrap.dedent(s).lstrip('\n').rstrip() + '\n'


CASE = clean(r'''
# IBM Store-In Cache: Cache-Local Current State, Store Bits, and Castout to Shared Memory

## Status

**`grounded`** — bounded to IBM's 1971-filed multiprocessor store-in-buffer design record and the IBM 3081 Processor Unit account published in the *IBM Journal of Research and Development* in January 1982, with Alan Jay Smith's 1982 *ACM Computing Surveys* article used as a high-quality contemporary taxonomy/control source.

Grounding record: [`../evidence/72-ibm-1971-1982-store-in-cache-grounding.md`](../evidence/72-ibm-1971-1982-store-in-cache-grounding.md).

## Scope

This case asks one narrow cache-retention question that Case 08 intentionally left open:

> **What changes when a cache is allowed to retain a newer current value than main storage, so that eviction or another request can no longer treat the cache as a disposable derivative copy?**

The bounded relation is:

```text
shared / central-storage block
    -> copied into a private store-in cache
    -> processor modifies the cache-resident line
    -> retained directory/currentness state records divergence or exclusive update authority
    -> the backing copy may remain physically present but stale
    -> replacement or a conflicting request triggers castout / transfer back
    -> central storage becomes current before the modified cache embodiment is discarded or another requester refetches it
```

This is **not** a general history of write-back caches, cache coherence, MESI-like protocols, dirty-bit invention, multiprocessor consistency, IBM 3081 checkpoint/retry, or cache-circuit technology. It also does not claim that the exact `store bit 56` disclosed in IBM's 1971 patent is the exact directory bit implementation used by the production 3081.

The retention-specific contribution is narrower:

> **a cache can temporarily become the locus of the current payload while an older backing copy still physically survives. In that regime, retained metadata is not merely hit/miss metadata: it can encode a future obligation to preserve the only current value before the cache embodiment is forgotten.**

`cache-local current authority`, `writeback obligation`, and `backing-copy staleness` below are project engineering terms. IBM's period terms include `store-in buffer`, `store bit`, `store-in-cache`, `cast out`, `read-only (RO)`, `exclusive (EX)`, `central storage`, and `system controller`.

## Related-repository check

Fresh searches in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `3081`, `store-in cache`, and `cache` found no dedicated case to reuse before drafting.

A full history of cache organizations and coherence belongs there if developed later. This case keeps only the retention/currentness distinction needed to break Case 08's Model-85 write-through-like authority relation.

## Historical vocabulary

### IBM 1971 — `store through`, `store wherever`, `store-in buffer`, `store bit`

IBM US3735360A, filed 25 August 1971, explicitly says there were already three methods in the prior art for store operations. It names `store through`, `store wherever`, and a third method that brings the block from main storage and then stores new data into the block in the buffer. The patent is primarily adapted to this third `store-in buffer` method.

The same source calls one directory bit a **`store bit`**. When set, it records that the data in a private high-speed buffer has been modified and is no longer identical to the corresponding block retained in shared main storage.

Do not silently replace this period term with `dirty bit` in historical claims.

### IBM 3081, 1982 — `store-in-cache`, `cast out`, `RO`, `EX`

R. N. Gustafson and F. J. Sparacio's January 1982 IBM engineering paper describes the 3081 Processor Unit's 32-Kbyte cache as using a **`store-in-cache algorithm`**. It says the algorithm was selected over store-through for the machine's performance conditions.

The same paper states that changed data can reside in the processor caches so that central-storage contents are **not always valid**. The system controller maintains duplicate copies of the processor cache directories, determines whether a central-storage request would return valid data, and on conflict causes the line to be **cast out** from cache to central storage before the requesting unit refetches it.

The paper also uses `read-only (RO)` and `exclusive (EX)` line status and requires EX status before a store can complete to a line.

### Contemporary taxonomy — `copy-back`, `dirty bit`

Alan Jay Smith's 1982 survey uses the later-general taxonomy `write-through` versus `copy-back`, defines a `dirty bit` as indicating that a line has been modified while in the cache, and explicitly lists the IBM 3081 among machines using copy-back.

That survey is useful for comparison and terminology control. It does **not** authorize replacing IBM's 1971 `store bit` or 3081 `store-in-cache` vocabulary in period-specific claims.

## Historical record

### H/P — the 1971 IBM patent itself blocks an IBM-first store-in claim

US3735360A's prior-art section says there were **currently three** store-handling methods and includes `store-in buffer` among them. It also cites C. J. Conti's 1969 buffer-storage article and earlier associative-buffer work.

Therefore this case does not claim that the patent invented store-in/write-back caching. Its value here is that it gives unusually explicit period-primary state semantics for a modified private copy.

**Primary anchor:** US3735360A, `Prior Art` and the store-operation discussion, especially the passages corresponding to Google Patents lines 301–324.

### H/P — IBM's `store bit` directly records cache/backing divergence

The 1971 source says `store bit 56` is set when the associated processor stores into a block in private storage. A set store bit means that the private-storage block has been modified and is **no longer identical** to the same block retained in shared main storage.

This is stronger than ordinary validity metadata. A valid cache block can be current specifically because it differs from the still-existing backing copy.

**Primary anchor:** US3735360A, description of `store bit 56`, especially the passages corresponding to lines 147–155 and 368–372.

### H/P — modified replacement must first transfer the current block back

When replacement selects a valid private block whose store bit is set, the 1971 design transfers that block back to shared main storage. The store bit is then reset to indicate that the private and shared copies again agree.

The patent's claims make the relation explicit: transfer from private to shared storage is required when the private block has been stored into and therefore differs from the shared copy.

**Primary anchor:** US3735360A, replacement/store-bit description and claims 6–7.

### H/P — an unmodified block can be replaced without the same transfer

The same source explains the purpose of retaining the store bit: if the block has not been stored into, the machine can avoid an unnecessary transfer back to shared storage when replacement occurs.

Thus replacement has at least two retention cases:

```text
clean / unchanged cache copy
    -> replacement can retire the derivative copy

modified cache copy
    -> replacement first preserves the newer value in shared storage
    -> only then may the cache embodiment be retired
```

**Primary anchor:** US3735360A, store-bit summary and claim language, including the passage corresponding to line 424.

### H/P — a remote request can also force restoration of a modified private value

The 1971 multiprocessor design searches other processors' directories. If another private buffer contains the requested block and its store bit says that block was modified, that block must first be transferred back to shared storage so the requesting processor can receive the most current value.

This makes `main-storage address exists` insufficient as a proof that the bytes currently retained there are the value another processor should receive.

**Primary anchor:** US3735360A, broadcast/interlock description, especially the passages corresponding to lines 111–115 and 178–183.

### H/P — the production 3081 independently exhibits the same retention relation

Gustafson and Sparacio describe the IBM 3081 Processor Unit's buffer control element as containing a 32-Kbyte cache using a store-in-cache algorithm, 128-byte lines, four-way set associativity, and LRU replacement.

They then state that store-in-cache creates a data-integrity problem because changed data resides in the processor caches and central-storage content is not always valid. The system controller retains duplicate cache-directory information so it can determine whether a central-storage request will return valid data. On conflict it initiates castout of the specific cache line to central storage and then allows the requesting unit to refetch it.

This is direct manufacturer-primary production-machine evidence that the `current value may be in cache while central storage is stale` relation was not merely a patent thought experiment.

**Primary anchor:** R. N. Gustafson and F. J. Sparacio, “IBM 3081 Processor Unit: Design Considerations and Design Process,” *IBM Journal of Research and Development* 26(1), January 1982, printed pp. 15–16, especially p. 16.

### H/P — update authority is qualified by RO/EX state in the 3081

The 3081 paper says each cache line has `read-only (RO)` or `exclusive (EX)` status and a line must have EX status before a store can complete. The system controller permits only one EX copy, while multiple RO copies can coexist when no store activity occurs.

The exact later coherence taxonomy is outside this case, but the historical fact matters: payload bits alone do not encode who may create the next current value.

**Primary anchor:** Gustafson and Sparacio 1982, printed p. 16.

## Retained state and mechanism

The bounded store-in regime contains several distinct state classes:

1. **cache payload** — a line that may be the newest/current embodiment;
2. **shared/central-storage payload** — a backing embodiment that can remain physically present yet temporarily stale;
3. **address/directory relation** — which cache line represents which shared/central-storage block;
4. **validity/currentness qualification** — whether the cached relation may be used;
5. **modified/divergence state** — IBM's 1971 `store bit`, or the later generic `dirty` relation, recording that cache and backing store no longer agree;
6. **sharing/update-authority state** — in the 3081 source, RO/EX status and system-controller directory knowledge;
7. **replacement state** — the policy that can create a future castout obligation by selecting a modified line.

The key relation is therefore not:

```text
cache = disposable duplicate of main storage
```

but:

```text
cache payload
+ retained identity/currentness metadata
+ possible modified/exclusive state
= current value that may need preservation before cache retirement
```

## Engineering reconstruction

### E — physical backing-copy survival ≠ authoritative currentness

A shared/central-storage block can remain physically present while a newer cache-resident value is the one the system must treat as current. This directly breaks the shortcut `main memory exists, therefore main memory is authoritative now`.

### E — modified-state metadata can encode a future preservation obligation

The 1971 `store bit` does not contain the operand. It records a relation: **the cache copy differs from backing storage**. If replacement later selects that line, the bit changes what must happen before the cache embodiment can be forgotten.

Retention infrastructure can therefore preserve not only `what is current` but `what work remains necessary before one embodiment may be retired`.

### E — clean replacement ≠ modified replacement

Case 08's bounded Model 85 updates main storage on every store, so cache reassignment does not need a cache-to-main copy. In a store-in/cache-copy-back regime, an unchanged line can still be discarded cheaply, but a modified line carries a writeback/castout obligation.

The same operation name, `replacement`, therefore has different retention semantics under different authority policies.

### E — backing-store staleness can be deliberate normal operation

The 3081 paper's statement that central storage is not always valid is not a field-failure report. It describes an engineered store-in-cache condition that the system controller must interpret correctly.

`stale` therefore does not automatically mean `broken`: it can be a protocol-authorized intermediate relation so long as enough metadata and castout machinery survive to return the system to an admissible current state when required.

### E — currentness authority can migrate without changing the architectural designation

The program continues to address the same logical/shared-memory location while the current payload's operative embodiment can shift:

```text
central storage current
    -> line enters cache
    -> cache-local store makes cache current / central storage stale
    -> castout makes central storage current again
```

The designation remains stable while the currentness relation changes.

### E — cache-local currentness ≠ nonvolatile durability

Neither the 1971 patent nor the 1982 3081 paper turns the cache into power-fail-persistent storage. Indeed, Smith's contemporary survey treats reliability as one tradeoff of copy-back because the only valid copy of a line may be in cache.

This case therefore does not infer crash/power-loss durability from `current value lives in cache`.

## Read / write / replacement semantics

### Read

**H/P:** the 1971 design searches local/remote directory state so that a processor receives the most current value. In the 3081, the system controller determines whether a central-storage request would return valid data and can force castout/refetch on conflict.

**E:** successful address resolution to central storage is not sufficient; currentness qualification can redirect the recovery path through a cache embodiment first.

### Write

**H/P:** a store-in operation can modify the cache while leaving the shared/central-storage block unchanged for the moment. The 1971 design sets the store bit; the 3081 requires EX status before a store completes.

**E:** write completion at the cache level can create a temporary inversion of the intuitive hierarchy: the nominal backing store contains the older embodiment.

### Replacement / castout

**H/P:** modified private data is transferred back before replacement in the 1971 design; the 3081 controller can cast out a conflicting line from cache to central storage and then allow a requester to refetch it.

**E:** castout is a **currentness transfer**, not merely space reclamation. It preserves the current logical value while ending one cache-local embodiment.

## Failure and forgetting

### Lost or incorrect modified-state evidence

If a system forgets that a cache line differs from backing storage, it can incorrectly treat replacement as disposal of a redundant copy. The historical sources ground the metadata and transfer logic; this failure consequence is an engineering reconstruction, not a reported IBM incident.

### Loss of the modified cache embodiment before castout

If the only current value resides in volatile cache and is lost before it has been transferred to an authoritative surviving location, the stale backing copy does not magically become the newer value.

This is a current-payload loss boundary, not evidence about the 3081's full fault-recovery design.

### Clean eviction

Retiring an unchanged cache copy is cache-level forgetting without architectural-data forgetting because an equivalent current backing copy remains.

### Modified eviction after castout

The cache embodiment can cease to count after its current value has been transferred back. This is embodiment replacement with logical continuity.

### Castout ≠ secure erasure

No cited source establishes forensic sanitization of the displaced cache cells. Losing residency/current authority is a logical/architectural transition, not proof of physical erasure.

## Functional analogies and boundaries

### A — Case 08 Model 85 write-through-like cache vs Case 72 store-in cache

Case 08 grounds a cache in which every store updates main storage, so cache data remains derivative and reassignment can clear validity without writing payload back.

Case 72 supplies the intended counterexample: a cache-local store can make the cached line newer than main storage, making modified-state/currentness metadata and castout constitutive of preserving the architectural value.

Therefore:

> **cache-copy retention ≠ one universal authority relation.**

### A — mapped Flash (Case 04)

Both cases let a stable higher-level designation survive a change in which physical embodiment currently matters, and both rely on retained metadata to say which embodiment counts.

The analogy stops there. Flash remapping responds to erase geometry and controller allocation; store-in caching is a volatile hierarchy/currentness policy in which castout returns a modified line toward the backing tier.

### A — distributed currentness

A stale central-storage embodiment and a stale distributed replica are functionally comparable only at the level `physical/readable copy ≠ authorized current copy`. The cache protocol, timescale, failure assumptions, and historical genealogy are different.

## Prior art and novelty boundary

No invention-priority claim is made.

IBM's own 1971 patent explicitly places `store-in buffer` among then-current prior-art store methods. Alan Jay Smith's 1982 survey likewise treats write-through/copy-back as an established design choice and discusses multiple vendors and systems.

The defensible historical claim is narrower:

> **IBM's 1971 source gives period-primary modified/private-copy metadata semantics, and the 1982 IBM 3081 engineering account gives a named production system in which store-in-cache makes central storage temporarily invalid and requires directory-qualified castout before some requests can use it.**

That is enough to ground a retention/currentness regime without claiming IBM invented write-back caching, the dirty bit, or cache coherence.

## Philosophical interpretation

### I — the place called `main` need not be the place where the current state resides

This bounded mechanism disciplines any philosophical claim that technical retention is simply the persistence of a thing in its nominal storage location. A physically surviving backing copy can remain available while no longer being the state the system may treat as current.

The philosophical use is modest: **technical availability depends on retained relations of identity, currentness, and transfer obligation, not only on physical presence.** This does not turn cache coherence into a theory of human memory or establish any Heideggerian category by itself.

## Source ledger

1. D. Anderson, R. Gustafson, L. Johnson, F. Sparacio / IBM, **“High speed buffer operation in a multi-processing system,”** US3735360A, filed 25 August 1971, published 22 May 1973: <https://patents.google.com/patent/US3735360A/en>.
   - prior-art store-through / store-wherever / store-in-buffer distinctions;
   - `store bit` meaning;
   - modified-block replacement transfer;
   - remote-request restoration for the most current value.
2. R. N. Gustafson and F. J. Sparacio, **“IBM 3081 Processor Unit: Design Considerations and Design Process,”** *IBM Journal of Research and Development* 26(1), January 1982, pp. 12–21; relevant printed pp. 15–16: <https://bitsavers.org/pdf/ibm/IBM_Journal_of_Research_and_Development/261/ibmrd2601C.pdf>.
   - named production 3081 store-in-cache organization;
   - performance choice against store-through;
   - central-storage invalidity under cache-local changed data;
   - duplicate directory/currentness checking, castout, RO/EX status.
3. Alan Jay Smith, **“Cache Memories,”** *ACM Computing Surveys* 14(3), September 1982, pp. 473–530, DOI 10.1145/356887.356892: <https://dl.acm.org/doi/10.1145/356887.356892>.
   - contemporary scholarly taxonomy of `write-through` versus `copy-back`;
   - dirty-bit definition and copy-back obligation;
   - IBM 3081 identified as using copy-back.
   - accessible page-preserving copy inspected for this pass: <https://people.engr.tamu.edu/djimenez/taco/utsa-www/cs5513-fall07/reader/smith-cache-memories.pdf>.

## Claim ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| IBM's 1971 source treats store-in buffer as an already existing store-policy class | H/P | US3735360A prior-art section | supported |
| a store bit can record that private-buffer data differs from shared main storage | H/P | US3735360A description/claims | supported |
| a modified replacement is transferred back before the private embodiment is retired in the disclosed design | H/P | US3735360A replacement path | supported |
| the IBM 3081 used a store-in-cache algorithm | H/P | Gustafson & Sparacio 1982 pp. 15–16 | supported |
| 3081 central storage could temporarily be invalid because changed data resided in CP caches | H/P | Gustafson & Sparacio 1982 p. 16 | supported |
| 3081 controller could force castout before a conflicting central-storage request refetched data | H/P | Gustafson & Sparacio 1982 p. 16 | supported |
| IBM 1971 `store bit 56` was the exact bit circuit used by the 3081 | X | no implementation-identity evidence | rejected |
| `store bit` was historically called `dirty bit` by IBM in the 1971 source | X | US3735360A vocabulary | rejected |
| cache-local currentness implies power-fail durability | X | no such fault-domain evidence | rejected |
| IBM invented write-back/store-in caching | X | IBM patent itself identifies prior art | rejected |
| castout proves secure erasure of the old cache embodiment | X | no sanitization evidence | rejected |

## Case findings

1. **physical backing-copy survival ≠ authoritative currentness.**
2. **store-bit / modified-state retention ≠ payload retention.**
3. **store-bit set ≠ data already propagated to shared storage.**
4. **clean cache replacement ≠ modified cache replacement.**
5. **modified cache replacement can create a preservation-before-forgetting obligation.**
6. **backing-store staleness can be an engineered normal state rather than a failure.**
7. **currentness authority can migrate while architectural designation remains stable.**
8. **cache-local currentness ≠ nonvolatile durability.**
9. **central-storage address resolution ≠ proof that central-storage bytes are current.**
10. **remote demand can trigger currentness transfer before the requester reads.**
11. **sharing/update-authority state ≠ modified/divergence state.**
12. **cache coherence/currentness metadata ≠ complete store history.**
13. **cache eviction ≠ always disposal of a redundant copy.**
14. **castout/writeback ≠ secure erasure.**
15. **Model-85 write-through-like currentness ≠ 3081 store-in currentness.**
16. **IBM 1971/3081 evidence ≠ invention-priority proof for write-back caching.**
''')


EVIDENCE = clean(r'''
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
''')


FINDINGS = clean(r'''
## Case 72 — IBM store-in-cache currentness findings

829. **physical backing-copy survival ≠ authoritative currentness** — IBM's store-in designs allow shared/central storage bytes to remain physically present while a newer cache-resident value is the one that must count;
830. **modified-state metadata ≠ payload** — the 1971 `store bit` records a divergence relation between private buffer and shared storage rather than containing the operand itself;
831. **store bit set ≠ data already propagated to shared storage** — in the bounded design the set bit means precisely that the private block has been modified and is no longer identical to the shared copy;
832. **clean cache replacement ≠ modified cache replacement** — an unchanged derivative copy can be retired without the same transfer, while a valid modified block must first preserve its newer value in shared storage;
833. **cache eviction ≠ always disposal of a redundant copy** — once a cache-local store has made the cache embodiment newer, eviction can become a preservation-before-forgetting event rather than simple capacity reclamation;
834. **backing-store staleness can be engineered normal state rather than failure** — the 3081 paper explicitly says store-in-cache leaves central storage not always valid and supplies controller logic to manage that condition;
835. **currentness authority can migrate while architectural designation remains stable** — one shared-memory address can continue naming the object while the operative current embodiment moves cache-local and later returns to central storage by castout;
836. **cache-local currentness ≠ nonvolatile durability** — the sources establish which copy is current during powered operation, not that cache-local modified state survives arbitrary processor/cache power loss;
837. **central-storage address resolution ≠ proof that central-storage bytes are current** — the 3081 system controller first qualifies whether a central-storage request would return valid data and can interpose castout/refetch;
838. **remote demand can trigger currentness transfer before the requester reads** — the 1971 multiprocessor design restores a modified remote private block to shared storage so another processor receives the most current value;
839. **sharing/update-authority state ≠ modified/divergence state** — the 3081 RO/EX relation answers who may store, while a store/change relation answers whether a cache copy has diverged from backing storage; these roles must not be collapsed;
840. **cache currentness metadata ≠ complete store history** — directory/store/RO-EX state preserves enough relation for present admissibility and future transfer without archiving every processor store that produced it;
841. **castout can be currentness transfer rather than mere space reclamation** — replacement and conflicting requests can both cause transfer of the current cache value toward central storage;
842. **castout/writeback ≠ secure erasure** — loss of cache residency/current authority does not establish forensic sanitization of the displaced cache cells;
843. **Model-85 write-through-like currentness ≠ 3081 store-in currentness** — Case 08 keeps main storage current on every store, while Case 72 permits the cache to become newer and therefore changes the retention semantics of replacement;
844. **IBM 1971/3081 evidence ≠ invention-priority proof for write-back caching** — IBM's own 1971 prior-art section already treats store-in as an existing store-policy class, so the grounded claim is the explicit IBM mechanism plus named 3081 production witness, not first invention.
''')


README_LINE = '- [`cases/72-ibm-store-in-cache-currentness-castout.md`](cases/72-ibm-store-in-cache-currentness-castout.md) — grounded cache-authority counterexample to Case 08: IBM period-primary store-in evidence shows a modified cache line can be newer than shared/central storage, making retained modified/currentness state and castout part of preserving the architectural value before cache replacement.'

CASE_INDEX_ROW = '| [IBM Store-In Cache: Cache-Local Current State, Store Bits, and Castout to Shared Memory](cases/72-ibm-store-in-cache-currentness-castout.md) | **grounded** | private/store-in cache + directory/valid/modified authority state + shared/central backing copy that may be stale + castout path | separate physical backing-copy survival from authoritative currentness; modified-cache authority from main-storage authority; clean replacement from writeback-required replacement; currentness metadata from payload | [1971–1982 IBM store-in-cache grounding](evidence/72-ibm-1971-1982-store-in-cache-grounding.md); broader write-back/coherence genealogy, exact 3081 directory implementation, fault injection, power-fail behavior, and later protocol families remain separate work |'

MATRIX_ROW = '| IBM store-in cache / 1971–1982 bounded regime | private-cache payload + directory/valid/modified and RO/EX currentness state + shared/central backing copy that may be stale | processor stores can create cache-local newer state; replacement or competing demand can trigger castout; controller qualifies backing-store currentness | local cache can supply the current line; a conflicting central-storage request can be redirected through castout then refetch in the 3081 | shared-memory address remains stable while cache directory/currentness state determines which embodiment may serve it and who may update it | current authority can reside temporarily in cache before castout makes central storage current again | no complete store history; bounded metadata retains current divergence/authority and the obligation to preserve a modified line before retirement |'


def insert_after_first_line_containing(text: str, needle: str, new_line: str) -> str:
    lines = text.splitlines()
    hits = [i for i, line in enumerate(lines) if needle in line]
    if not hits:
        raise RuntimeError(f'anchor not found: {needle}')
    idx = hits[0]
    if new_line in lines:
        return text
    lines.insert(idx + 1, new_line)
    return '\n'.join(lines) + '\n'


def patch_readme():
    p = ROOT / 'README.md'
    text = p.read_text()
    if 'cases/72-ibm-store-in-cache-currentness-castout.md' in text:
        return
    text = insert_after_first_line_containing(
        text,
        'cases/71-apache-zookeeper-fuzzy-snapshot-replay-recovery.md',
        README_LINE,
    )
    p.write_text(text)


def patch_roadmap():
    p = ROOT / 'ROADMAP.md'
    text = p.read_text()
    if 'cases/72-ibm-store-in-cache-currentness-castout.md' not in text:
        old = 'Later write-back/dirty-state retention, multiprocessor cache coherence, ECC, and exact Model-85 fast-store circuit technology remain separate regimes, not hidden completion criteria for this bounded bridge;'
        new = 'The separate store-in/write-back currentness sub-slice is now **`grounded`** in [`cases/72-ibm-store-in-cache-currentness-castout.md`](cases/72-ibm-store-in-cache-currentness-castout.md), with grounding record [`evidence/72-ibm-1971-1982-store-in-cache-grounding.md`](evidence/72-ibm-1971-1982-store-in-cache-grounding.md): cache-local stores can make the cache newer than main storage, so modified/currentness metadata and castout become preservation obligations rather than mere hit-policy state. Broader multiprocessor-coherence genealogy, ECC, and exact Model-85/3081 directory-circuit archaeology remain separate regimes, not hidden completion criteria for these bounded bridges;'
        if text.count(old) != 1:
            raise RuntimeError(f'ROADMAP Phase-2 cache anchor count={text.count(old)}')
        text = text.replace(old, new, 1)

        q = '- [ ] How do cache and memoization complicate the boundary?'
        qa = '- [x] In a store-in/write-back cache, separate cache residency, backing-copy physical presence, cache-local current authority, modified/divergence state, update authority, castout obligation, and clean-versus-modified replacement — grounded in [`cases/72-ibm-store-in-cache-currentness-castout.md`](cases/72-ibm-store-in-cache-currentness-castout.md), with [`evidence/72-ibm-1971-1982-store-in-cache-grounding.md`](evidence/72-ibm-1971-1982-store-in-cache-grounding.md); the broader cache/memoization boundary remains open.'
        text = insert_after_first_line_containing(text, q, qa)

        old2 = 'Later write-back caches should be allowed to break the Model 85 result by introducing cache-local dirty/authoritative state rather than being forced into a write-through model.'
        new2 = 'Case 72 now supplies that counterexample: IBM store-in-cache permits cache-local changed state to outrun main storage, so modified/currentness metadata can encode a preservation-before-replacement obligation and central storage can be physically present yet temporarily non-current. Future cache work should now test broader multiprocessor-coherence genealogy, finer dirty-granularity, fault/power-loss behavior, and memoization rather than forcing every cache into either the Model-85 or 3081 authority relation.'
        if text.count(old2) != 1:
            raise RuntimeError(f'ROADMAP Phase-3 cache paragraph anchor count={text.count(old2)}')
        text = text.replace(old2, new2, 1)
    p.write_text(text)


def patch_case_index():
    p = ROOT / 'CASE_INDEX.md'
    text = p.read_text()
    if 'cases/72-ibm-store-in-cache-currentness-castout.md' not in text:
        # Insert the main ledger row after Case 71, before the comparison-matrix divider.
        marker = '## Comparison matrix — provisional'
        head, tail = text.split(marker, 1)
        head = insert_after_first_line_containing(
            head,
            'cases/71-apache-zookeeper-fuzzy-snapshot-replay-recovery.md',
            CASE_INDEX_ROW,
        )
        text = head + marker + tail

        # Insert the comparison row next to the Model-85 row it directly contrasts.
        text = insert_after_first_line_containing(
            text,
            '| IBM System/360 Model 85 cache |',
            MATRIX_ROW,
        )

        if not text.endswith('\n'):
            text += '\n'
        text += '\n' + FINDINGS
    p.write_text(text)


def validate():
    assert CASE_PATH.exists() and EVIDENCE_PATH.exists()
    case_files = sorted((ROOT / 'cases').glob('[0-9][0-9]-*.md'))
    ids = sorted(int(x.name[:2]) for x in case_files)
    if ids != list(range(73)):
        raise RuntimeError(f'case ledger not contiguous 00-72: {ids[:5]} ... {ids[-5:]} count={len(ids)}')

    readme = (ROOT / 'README.md').read_text()
    roadmap = (ROOT / 'ROADMAP.md').read_text()
    index = (ROOT / 'CASE_INDEX.md').read_text()
    for text, name in [(readme, 'README'), (roadmap, 'ROADMAP'), (index, 'CASE_INDEX')]:
        if '72-ibm-store-in-cache-currentness-castout' not in text:
            raise RuntimeError(f'Case72 navigation missing from {name}')
    for n in range(829, 845):
        if f'{n}. **' not in index:
            raise RuntimeError(f'finding {n} missing')
    if '845. **' in index:
        raise RuntimeError('unexpected finding 845 already present; possible concurrent integration')
    if index.count('cases/72-ibm-store-in-cache-currentness-castout.md') < 1:
        raise RuntimeError('Case72 ledger row missing')
    if index.count('| IBM store-in cache / 1971–1982 bounded regime |') != 1:
        raise RuntimeError('Case72 comparison row missing or duplicated')

    subprocess.run(['git', 'diff', '--check'], check=True)


def main():
    if CASE_PATH.exists() or EVIDENCE_PATH.exists():
        raise RuntimeError('Case72 target already exists; refusing duplicate integration')

    CASE_PATH.write_text(CASE)
    EVIDENCE_PATH.write_text(EVIDENCE)
    patch_readme()
    patch_roadmap()
    patch_case_index()
    validate()

    # Remove one-shot integration machinery from the committed tree.
    if WORKFLOW_PATH.exists():
        WORKFLOW_PATH.unlink()
    if SELF_PATH.exists():
        SELF_PATH.unlink()

    subprocess.run(['git', 'add', '-A'], check=True)
    subprocess.run(['git', 'diff', '--cached', '--check'], check=True)
    subprocess.run(['git', 'status', '--short'], check=True)
    subprocess.run(['git', 'commit', '-m', 'case72: ground IBM store-in cache currentness'], check=True)
    subprocess.run(['git', 'push', 'origin', 'HEAD:main'], check=True)


if __name__ == '__main__':
    main()
