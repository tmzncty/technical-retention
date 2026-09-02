# IBM System/360 Model 85 Cache: Currentness in a Transparent Fast Copy

## Scope

- **Status:** `grounded`.
- **Object / system:** IBM System/360 Model 85 high-speed buffer / cache, bounded to the 1967 functional manual and J. S. Liptay's 1968 IBM Systems Journal account.
- **Date range:** 1967–1968.
- **Primary question:** what additional retention relation appears when a fast memory is no longer merely an addressable array, but a dynamically assigned, transparent copy of portions of another storage level?
- **Why this case matters:** Case 07 grounded powered-quiescent semiconductor array retention and separated cell holding from selection/sensing. A cache introduces another layer: the data bits are useful only when retained correspondence, validity, currentness, and replacement-policy state say that those bits still count as the current fast copy of a particular main-storage region.

This is **not** a general cache history. It does not cover write-back caches, dirty bits, later tag terminology, set associativity, multi-processor coherence protocols, MESI-like state machines, modern SRAM cache cells, or virtual-index/tag questions.

Grounding record:

- [`../evidence/08-model85-cache-1967-1968-grounding.md`](../evidence/08-model85-cache-1967-1968-grounding.md).

---

## Related-repository check

Fresh searches in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `cache` and cache/currentness terms found no dedicated cache case to reuse.

A broad engineering history of memory hierarchy still belongs primarily there. The contribution here is narrower: use one well-documented early cache to test what `retention` means when fast storage is **derivative, dynamically reassigned, and admissible only through retained metadata relations**.

---

## Historical vocabulary

### 1967 IBM manual — `high-speed buffer storage`, `buffer storage control`, `current`

IBM's 1967 *System/360 Model 85 Functional Characteristics* describes a `high-speed buffer storage` controlled by a `buffer storage control` area. It states that the control handles CPU fetch/store requests and monitors channel store operations so that the high-speed buffer can be kept updated.

The same section says that:

- CPU fetches check whether referenced data is in buffer storage;
- all stores update main storage;
- an already resident buffer copy is also updated;
- buffer pages are related to main-storage pages by a correspondence established during operation;
- block loading is demand-driven;
- channel stores update resident buffer data;
- `Because data in buffer storage must be current`, buffer pages can be reassigned according to usage.

**Primary anchor:** IBM, *IBM System/360 Model 85 Functional Characteristics*, Form A22-6916-0, 1967, `Buffer Storage Control`, printed p. 13 / PDF p. 12: <https://www.bitsavers.org/pdf/ibm/360/functional_characteristics/A22-6916-0_System_360_Model_85_Functional_Characteristics_1967.pdf>.

### 1968 Liptay — `cache`, `sector address register`, `validity bit`, `activity list`

J. S. Liptay's 1968 *IBM Systems Journal* paper uses `cache` directly and notes on p. 21 that the term is synonymous with `high-speed buffer` in other Model 85 documentation.

Its period vocabulary includes:

- `cache`;
- `storage hierarchy`;
- `sector` and `block`;
- `sector address register`;
- `validity bit`;
- `activity list`;
- `assigned` / `reassigned`;
- data `currently being used`;
- cache data being `updated`.

**Primary anchor:** J. S. Liptay, “Structural aspects of the System/360 Model 85 II: The cache,” *IBM Systems Journal* 7(1), 1968, pp. 15–21: <https://www.andrew.cmu.edu/course/15-440/assets/READINGS/liptay1968.pdf>.

The scanned pp. 15–17 and 21 were directly inspected in this research pass.

### Anti-anachronism boundary

Modern architecture vocabulary can describe this mechanism compactly, but it must remain labeled as reconstruction or analogy:

- the `sector address register` is **tag-like**, but Liptay's historical term is `sector address register`;
- the all-stores-update-main policy is **write-through-like** in later taxonomy, but this source set is not used to claim that `write-through` was Liptay's term;
- channel-store monitoring is relevant to later coherence questions, but this case does not rename it `snooping` or project later multiprocessor coherence protocols backward;
- the activity-list replacement rule is recency-based, but modern `LRU` vocabulary should not replace the period description unless separately sourced.

---

## Historical record

### H/P — the cache is a transparent fast store, not a separately program-addressable memory

Liptay p. 15 describes a hierarchy consisting of 1.04-microsecond main storage and a small fast store called a cache, integrated into the CPU. The cache is **not addressable by a program**. It holds contents of portions of main storage currently in use, and loading/removal must occur without program assistance so the Model 85 remains compatible with the System/360 line.

This already separates cache semantics from Case 07's simple random-access-array semantics:

> the program continues to name main-storage addresses while the machine privately changes whether and where a fast duplicate exists.

### H/P — correspondence between cache and main storage is retained explicitly

Liptay p. 16 states that both cache and main storage are logically divided into 1K-byte sectors. During operation, each cache sector can be assigned to a main-storage sector.

Each cache sector has a **14-bit sector address register** holding the address of the main-storage sector to which it is assigned.

The assignment is dynamically adjusted as the program's current references change.

This is not merely an array-access fact. The cache must retain a relation:

```text
this cache sector
        ↕
currently represents this main-storage sector
```

### H/P — validity is separate retained metadata

A newly assigned sector does not immediately receive all 1K bytes. Liptay p. 17 explains that each sector is divided into sixteen 64-byte blocks and blocks are loaded on demand.

Each cache block has a **`validity bit`** recording whether that block has been loaded. The bit is turned on when the block is loaded and off when the sector is reassigned.

Therefore correspondence alone is insufficient: after a sector assignment exists, the machine must separately know which blocks under that assignment have actually become admissible cache copies.

### H/P — a fetch tests metadata before using data

Liptay p. 17 states that the first processor cycle of a cache fetch examines the sector address registers and validity bits to determine whether the data is in the cache; a later cycle reads the cache data itself. If the data is absent, the block is loaded from main storage.

The bounded historical mechanism is therefore not:

```text
address → fast-memory bits
```

but:

```text
main-storage address
        ↓
assignment/correspondence test
        ↓
block-validity test
        ↓
cache copy admitted for read
```

### H/P — main storage remains updated on every store

Liptay p. 17 says **store operations always cause main storage to be updated**. If the changed main-storage sector has a cache sector assigned, the cache copy is also updated; otherwise there is no cache action.

This has a major retention consequence for this specific architecture: every cache data value is also represented in main storage, so sector reassignment does not require copying data from cache to main storage. Reassignment changes the sector-address register, resets validity bits, and begins the demanded block load.

### H/P — channel stores participate in currentness maintenance

Liptay p. 18 states that channel fetches obtain data from main storage without referring to the cache, but channel stores are handled like processor stores: if a channel changes data that is in cache, the cache is updated.

IBM's functional manual independently says the buffer-storage control monitors channel store requests to keep high-speed buffer storage updated, and explicitly says buffer data must be current.

This makes cache `currentness` a period engineering requirement rather than a concept imported solely from the repository's later distributed-storage vocabulary.

### H/P — replacement depends on retained activity state

Liptay p. 16 states that enough information is maintained to order cache sectors in an **activity list**. The most recently referred-to sector is moved to the top; the sector at the bottom has gone longest without reference and is selected for reassignment.

Liptay explicitly says that movement in the activity list is a **logical ordering**, not actual movement of the cache sectors themselves. P. 21 reports that the activity-list organization was chosen for its cost/performance balance.

Thus the cache retains not only data/currentness metadata but also a compact policy state governing which derivative copy is most likely to be discarded next.

### H/P — the hierarchy is intended to be transparent to the user

Liptay p. 21 describes the fast monolithic storage integrated with the CPU and the large core storage as a combined hierarchy that is `transparent to the user`.

This is a period statement about interface hiding, not a philosophical claim that the underlying hierarchy ceases to exist materially.

---

## Retained state and substrate

### H/P

The Model 85 cache is a fast monolithic store integrated with the CPU, while the larger main storage is core storage. This case does not need to identify a modern SRAM bit-cell topology to establish the cache role.

The retained cache-level state includes at least:

1. **payload copy** — bytes copied from main storage;
2. **correspondence state** — sector address register relating a cache sector to a main-storage sector;
3. **validity state** — per-block indication that a block has actually been loaded under the current assignment;
4. **replacement-policy state** — activity-list ordering used to choose a sector for reassignment.

### E

The useful retention target is therefore not simply `fast bits stayed stable`.

For a later fetch to count as successful cache retention, the fast bits must remain embedded in a still-admissible relation:

```text
payload remains
+ cache sector still corresponds to requested main sector
+ requested block remains valid under that correspondence
+ no intervening store has made the cache copy stale
= current fast copy recoverable as the requested value
```

This is a stricter target than Case 07's bounded `cell still holds its logical condition`.

---

## Retention mechanism: derivative currentness

### E

A simplified Model 85 cache-retention cycle is:

```text
main-storage block demanded
        ↓
cache sector assigned / correspondence retained
        ↓
requested block copied in
        ↓
validity bit set
        ↓
copy remains usable while correspondence + validity + currentness hold
        ↓
processor/channel stores update main storage and any resident copy
        ↓
future fetch tests correspondence + validity
        ↓
copy is used, or a miss causes new loading
```

The key mechanism change from static RAM is architectural:

> cache retention is retention of a **derivative current copy under a relation**, not merely retention of one locally addressable bit pattern.

### Cache currentness is event-triggered, not deadline-refreshed

Nothing in this bounded source set establishes a periodic cache refresh obligation analogous to DRAM.

Currentness work is instead triggered by events:

- a fetch miss creates/loads a derivative copy;
- a store updates main storage and, if resident, the derivative cache copy;
- a channel store likewise updates a resident cache copy;
- sector reassignment changes correspondence and clears validity;
- references revise replacement-policy state.

This should be kept distinct from Case 03's time/deadline-triggered regeneration and Case 05's failure/repair-triggered replication.

---

## Addressing and access geometry

### H/P

The program addresses main storage, not the cache directly. The processor's main-storage reference is resolved against retained sector correspondence and block validity.

Cache-sector assignment can change dynamically while the program-visible address remains the same.

### E

This creates an important contrast with mapped Flash:

- in mapped Flash, mapping metadata can be constitutive of **which physical embodiment is the current logical object**;
- in the Model 85 cache, correspondence metadata is constitutive of **whether a derivative fast copy can serve the request**, while main storage remains the authoritative location updated by every store.

Both use retained relations, but they do not have the same identity semantics.

---

## Read / write / replacement semantics

### Read

**H/P:** a fetch checks sector-address correspondence and validity before reading cache data. A miss loads a block from main storage.

**E:** a cache hit is therefore an **admissibility result**, not proof that a matching byte pattern merely exists somewhere in the fast store.

### Write

**H/P:** every store updates main storage. If the target already has a cache representation, the cache is updated too.

**A/E:** later vocabulary would normally classify this behavior as write-through-like. That label is useful for comparison, not treated as Liptay's own term.

### Replacement / invalidation

**H/P:** on sector reassignment, the sector-address register changes, validity bits are reset, and the demanded block begins loading. No cache-to-main copy is required because main storage already holds the current data.

**E:** replacement terminates **cache-copy residency**, not the architectural memory state's continuity.

---

## Failure and forgetting

### 1. Wrong correspondence

**E:** if a sector-address register no longer correctly names the main-storage sector represented by a cache sector, surviving payload bits can no longer safely be interpreted as the requested current copy.

This is relation/currentness failure, not necessarily payload-bit decay.

### 2. Wrong validity

**E:** if validity state is wrong, an unloaded/obsolete block could be admitted or a correctly loaded block could be treated as absent.

Again, payload-state retention and admissibility-state retention are separate.

### 3. Missed update

**H/P + E:** IBM explicitly monitors processor/channel stores so resident data is kept updated/current. Mechanistically, failure of that obligation would allow main storage and its derivative fast copy to disagree.

The sources establish the prevention mechanism; they are not being cited as a field-failure report.

### 4. Reassignment

**H/P:** reassignment clears validity under the old relation.

**E:** this is deliberate cache-level forgetting: the old fast copy ceases to count as resident. It is **not system-level forgetting** because the current architectural value remains in main storage.

### 5. Physical residue is not inferred

The sources do not say what residual cell pattern is forensically accessible after a validity reset or sector reassignment.

**X:** `invalid cache block = physically erased`.

**X:** `invalid cache block = proven physically recoverable stale data`.

Neither claim is justified here.

---

## Maintenance and labor

The retention work in this case is mostly automated hardware control:

- maintain sector correspondence;
- maintain per-block validity;
- load demanded blocks;
- update resident copies on stores;
- maintain activity-list policy state;
- choose and reassign victim sectors.

The historical sources frame this as automatic organization required for compatibility and performance. They do not support a broad claim that human maintenance disappears; physical service, machine operation, manufacturing, and broader system administration are outside this bounded cache-semantics slice.

---

## Engineering reconstruction

### E — `cache-copy retention ≠ authoritative-state retention`

The Model 85 provides a clean counterexample to treating all loss of a stored copy as forgetting of the system's current data. A cache sector may be reassigned while main storage retains the authoritative value.

### E — `validity ≠ physical presence`

A block's validity bit records whether it is admitted as loaded under the current sector assignment. This lets the system withdraw a block from cache service by metadata state rather than requiring an authoritative writeback or documented physical erasure.

### E — `currentness metadata can matter even when authority is singular`

RADOS needed versions/epochs/peering because several replicas could disagree. The Model 85 needs correspondence/validity/update relations for a simpler reason: one authoritative memory value can have a derivative fast duplicate whose usability still depends on currentness.

`currentness` is therefore not a concept unique to distributed storage.

### E — `replacement-policy retention ≠ content retention`

The activity list is retained state that affects future system behavior, but it does not itself contain the application data being cached. It is control/policy state about **which copy gets to keep existing in the fast tier**.

---

## Functional analogies

### A — tag-like correspondence

The sector address register is functionally comparable to what later cache organization calls tag state.

This analogy helps compare architectures; it is not evidence that Liptay used `tag` in the cited text.

### A — write-through-like authority relation

Always updating main storage makes cache copies replaceable without a writeback step. Later terminology normally classifies that behavior as write-through.

This analogy should be used precisely because it highlights what the bounded Model 85 case **does not have**: a cache-local dirty copy that has become newer than main storage.

### A — coherence-like currentness, not a multiprocessor coherence protocol

Updating a resident cache copy when a channel stores to the same main-storage region is functionally relevant to currentness/coherence. But a one-CPU Model 85 cache plus I/O channels is not silently rewritten as a later multi-cache coherence protocol.

---

## Philosophical interpretation

### I — availability depends on retained relations, not only retained matter

The cache sharpens a project-wide point: a physical pattern can be useful later only under a relation that says **what it is a copy of and whether it still counts**.

This is valuable for the repository's technical notion of admissibility/currentness. It does not prove a Heideggerian claim about `Bestand` merely because the data is made rapidly available.

### I — apparent immediacy is produced by hidden replacement

Liptay's own conclusion emphasizes user transparency: program-visible storage appears as one System/360-compatible address space while fast-copy placement changes automatically beneath it.

The philosophical interest is not that the cache is `immaterial`, but the opposite: stable callability can be produced by material copying, metadata retention, and selective forgetting at a lower layer.

---

## Cross-case comparison

| Comparison | Model 85 cache adds |
| --- | --- |
| Case 07 static MOS RAM | substrate-level state holding is insufficient; cache adds hidden correspondence, validity, derivative-copy currentness, and replacement policy |
| Case 03 DRAM | cache currentness maintenance is event-driven by loads/stores/reassignment rather than deadline-driven refresh merely because time passes |
| Case 04 mapped Flash | both depend on retained mapping-like relations, but Model 85 main storage remains authoritative while the cache copy is disposable; Flash mapping can identify the current physical embodiment itself |
| Case 05 RADOS | both distinguish physical copy existence from current admissibility, but Model 85 has a single authoritative main-memory copy and no replica-election/peering protocol |
| Case 06 register | cache policy state and correspondence registers show that retained control metadata can govern later retention of other state, without every register becoming `storage` in the same architectural sense |

---

## Counterexamples and limits

1. **Cache ≠ SRAM.** A fast memory substrate can be used in many architectural roles. Cache semantics come from copy/currentness/replacement relations, not from bistability alone.
2. **Eviction ≠ data loss.** In this write-main-on-every-store design, reassignment discards a derivative fast copy while main storage remains current.
3. **Validity loss ≠ physical erasure.** The source establishes an admissibility bit, not forensic disappearance.
4. **Cache copy ≠ permanently privileged home.** Assignment moves; nevertheless the underlying main-storage address remains the authoritative program-visible location in this bounded system.
5. **One early cache ≠ all caches.** Write-back dirty state, multi-cache coherence, later set associativity, ECC, and virtual-memory interactions require their own cases.
6. **Historical terms ≠ modern normalization.** `sector address register`, `validity bit`, and `activity list` should remain visible instead of being silently rewritten as `tag`, `valid`, and `LRU metadata` everywhere.

---

## Claim ledger

| Claim | Label | Evidence / boundary |
| --- | --- | --- |
| Model 85 used a small fast CPU-integrated store called a `cache` and not program-addressable | H/P | Liptay 1968 p. 15 |
| Cache/main correspondence was retained per 1K cache sector in a 14-bit `sector address register` | H/P | Liptay p. 16 |
| Demand-loaded 64-byte blocks had per-block `validity bits` | H/P | Liptay p. 17 |
| Fetches examined correspondence + validity before cache read | H/P | Liptay p. 17 |
| Every store updated main storage; resident cache copies were also updated | H/P | Liptay p. 17; IBM 1967 manual p. 13 |
| Channel stores updated resident cache data to keep the buffer current | H/P | Liptay p. 18; IBM 1967 manual p. 13 |
| Reassignment changed correspondence, reset validity, and required no cache-to-main writeback | H/P | Liptay p. 17 |
| Activity-list state logically ordered sectors for replacement | H/P | Liptay pp. 16, 21 |
| Cache hit/current fast-copy status is a relation of payload + correspondence + validity + update discipline | E | bounded reconstruction from primary mechanism |
| Eviction/reassignment ends cache-copy retention without ending architectural-memory retention | E | depends on all-stores-update-main policy; not universal to write-back caches |
| Sector address register is tag-like | A | modern functional comparison only |
| Store policy is write-through-like | A | modern classification only; not claimed as Liptay vocabulary |
| Cache currentness illustrates technical admissibility | I | does not equate cache with Heideggerian `Bestand` |
| Model 85 establishes general multiprocessor cache coherence | X | outside source/system scope |
| Invalidity proves physical erase or forensic survival | X | neither established |

---

## Current assessment

Case 08 is **`grounded`** for the bounded 1967–1968 Model 85 cache regime.

The primary evidence directly establishes period vocabulary, hidden cache assignment, block validity, demand loading, currentness maintenance, discardable derivative copies, and replacement-policy state. IBM's functional manual independently corroborates the currentness/update behavior. The relevant Liptay pages were directly inspected, and related-repository duplication was checked.

The bridge therefore closes the immediate Phase-2 question `what changes when a fast retained array becomes a cache?` without pretending to close later cache history.

The most important surviving result is:

> **cache retention can require retaining not just data, but the relation that says what the data is a copy of, whether that copy is valid/current, and which copy may be discarded next. In the bounded Model 85 policy, losing the derivative cache copy is not losing the authoritative state.**
