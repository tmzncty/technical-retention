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
