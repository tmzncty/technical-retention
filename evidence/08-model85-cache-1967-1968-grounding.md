# IBM System/360 Model 85 Cache: 1967–1968 Grounding Record

## Purpose

This record grounds the cache-semantics bridge in [`../cases/08-system360-model85-cache-currentness.md`](../cases/08-system360-model85-cache-currentness.md).

The bounded question is not `what is a cache in general?` It is:

> What additional retention relation appears when a fast store is used as a transparent, dynamically reassigned copy of a slower authoritative store?

The source set is deliberately narrow: IBM's 1967 Model 85 functional-characteristics manual and J. S. Liptay's 1968 IBM Systems Journal paper on the Model 85 cache. Both are period IBM technical sources. Liptay pp. 15–17 and 21 were directly inspected as page images in this research pass. The IBM manual was text-located at the relevant page, but its current archival endpoint did not render a fresh screenshot reliably; claims that depend on visual layout are therefore taken from Liptay, not inferred from the manual scan.

---

## Related-repository check

Fresh searches in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `cache` and for cache/currentness terms returned no dedicated cache case to reuse.

That repository remains the preferred home for a broad history of memory hierarchy, packaging, circuit technology, and later cache evolution. This record stays at the retention-specific policy/interface boundary.

---

## Primary sources

### P1 — J. S. Liptay, 1968

J. S. Liptay, **“Structural aspects of the System/360 Model 85 II: The cache,”** *IBM Systems Journal* 7(1), 1968, pp. 15–21.

Period scan used here:

<https://www.andrew.cmu.edu/course/15-440/assets/READINGS/liptay1968.pdf>

Directly inspected page anchors:

- p. 15 — the storage hierarchy; a small fast store called a `cache`; not program-addressable; holds portions of main storage currently in use; loading/removal occurs without program assistance;
- p. 16 — 16K-byte integrated cache; 1K sectors; dynamically assigned correspondence between cache sectors and main-storage sectors; 14-bit `sector address register`; logical `activity list` ordered by recency of reference;
- p. 17 — 64-byte demand-loaded blocks; per-block `validity bit`; all stores update main storage; resident copies are also updated; reassignment changes the sector address register, resets validity bits, and does not require copying cache data back to main storage; cache fetch first examines sector-address registers and validity bits;
- p. 18 — channel fetches go to main storage; channel stores update an already resident cache copy but do not acquire cache space;
- p. 21 — replacement-algorithm comparison; the activity list chosen for cost/performance; the hierarchy described as transparent to the user; footnote stating that `cache` is synonymous with `high-speed buffer` in other Model 85 documentation.

### P2 — IBM, 1967

IBM, **IBM System/360 Model 85 Functional Characteristics**, Form A22-6916-0, first edition, 1967.

Archive scan:

<https://www.bitsavers.org/pdf/ibm/360/functional_characteristics/A22-6916-0_System_360_Model_85_Functional_Characteristics_1967.pdf>

Relevant text anchor: printed p. 13 / PDF page 12, section `Buffer Storage Control`.

The manual independently states that:

- buffer-storage control handles CPU fetch/store requests and monitors channel store requests so the high-speed buffer can be kept updated;
- CPU fetches check whether the referenced data is in buffer storage;
- all stores update main storage, and an already resident buffer copy is also updated;
- main and buffer storage are related through dynamically established page correspondence;
- block loading occurs on demand;
- channel stores update resident buffer data while channel fetches use main storage;
- `Because data in buffer storage must be current`, pages may be reassigned according to usage.

**Inspection boundary:** the text of this manual page is directly available through the archive's extracted text, but a fresh screenshot request failed in this pass. No figure-layout claim depends on it.

---

## Grounded historical claims

### H/P — period vocabulary is `cache` / `high-speed buffer`, not an imported modern textbook taxonomy

Liptay p. 15 calls the fast store a `cache`; his p. 21 footnote says the term is synonymous with `high-speed buffer` in other Model 85 documentation. The functional manual uses `high-speed buffer storage` and `buffer storage control`.

Historically safe terms for this case include:

- `cache`;
- `high-speed buffer` / `buffer storage`;
- `sector`;
- `block`;
- `sector address register`;
- `validity bit`;
- `activity list`;
- `current` / `updated`;
- `assigned` / `reassigned`.

The repository may use `tag-like`, `write-through`, `coherence-like currentness maintenance`, or `LRU-like` only as explicitly modern engineering/functional classifications. Those words must not replace the source vocabulary.

### H/P — cache residence is a relation, not only a surviving data pattern

Liptay pp. 16–17 directly establish three distinct state classes:

1. cached data bytes;
2. a 14-bit sector address register identifying which main-storage sector a cache sector is assigned to;
3. per-block validity bits recording whether a block has actually been loaded under the current sector assignment.

A processor fetch first examines the sector-address registers and validity bits to decide whether the referenced data is present before reading it from the cache.

### H/P — reassignment deliberately changes admissibility without requiring writeback

When a sector is reassigned, Liptay states that the system need only change the sector address register, reset validity bits, and initiate the demanded block load. It does not need to copy cache contents back because all cached data also exists in main storage.

This source therefore directly supports a bounded architecture in which cache residency can be invalidated/reassigned while authoritative data continuity remains in main storage.

### H/P — currentness is maintained on writes, including channel writes

Liptay and the functional manual independently state that stores always update main storage. If the referenced data is already represented in cache, that cache copy is updated too. Liptay further states that channel stores are treated like processor stores for this purpose, while channel fetches do not allocate or consume cache space.

The functional manual's explicit reason is currentness: buffer data must be kept updated/current.

### H/P — replacement is retained policy state, not physical movement of sectors

Liptay p. 16 explains that enough information is maintained to order cache sectors in an `activity list`, with the most recently referred-to sector at the top. He explicitly warns that this does not mean actual sector movement in the cache; it is a logical ordering. The bottom/least-recently-referred sector is selected for reassignment. P. 21 records the performance study behind choosing the activity-list organization.

---

## Engineering reconstruction

### E — cache-level retention target

For this bounded Model 85 case, a cache hit is not explained by `some bits still exist in fast storage`.

A more exact relation is:

```text
main-storage address requested
        ↓
sector-address correspondence matches
        ↓
requested block is marked valid under that assignment
        ↓
copy is admitted as current cache-resident data
        ↓
fast recovery from cache
```

This is a retention/currentness relation built from payload + designation/correspondence + validity metadata + update discipline.

### E — eviction/reassignment is not system-level forgetting

Because the bounded design writes every store to main storage and never requires a dirty cache sector to be written back on replacement, losing cache residency does not mean losing the current architectural memory value. It means losing one **derivative fast copy**.

This gives a useful cross-case distinction:

> cache-copy retention ≠ authoritative-state retention.

The claim is limited to this Model 85 policy. It does not generalize to later write-back caches.

### E — validity loss ≠ demonstrated physical erasure

Resetting a validity bit causes a block to cease to count as resident under the cache's own lookup rules. The sources do not establish what exact residual electrical pattern remains in every data cell after reassignment.

Therefore the repository may say:

> `valid under the current assignment` can end without any required writeback operation.

It must **not** turn that into the stronger forensic claim `the old bits are physically still there and readable` without a separate source.

### E — currentness maintenance is event-triggered, not scheduled refresh

The cache has no DRAM-like periodic deadline in this evidence set. Instead, currentness obligations are triggered by architectural events:

- processor store to a resident block;
- channel store to a resident block;
- fetch miss and demand load;
- sector reassignment and validity reset.

This is a different maintenance regime from both Case 03 deadline-driven refresh and Case 07 powered-quiescent state holding.

### E — policy state is retention infrastructure but not application history

The activity list retains enough recency ordering to choose a future victim sector. It therefore influences which fast copy survives next.

But it is not a general log of application history. It is bounded replacement-policy state, continuously revised for a specific control decision.

---

## Functional analogies and rejected shortcuts

### A — `sector address register` is tag-like, but `tag` is not substituted for period vocabulary

Modern cache literature would recognize the sector address register as serving a tag-like correspondence role. That is a useful functional analogy only.

**X:** `IBM called this a cache tag in the cited 1968 paper.`

Not established by this source set.

### A — always-updating main storage is write-through-like

The bounded behavior is what later architecture vocabulary normally classifies as write-through: every store updates main storage, and a resident cache copy is also updated.

**X:** `Liptay's paper uses “write-through” as its historical term.`

Not established here.

### X — this case is not a general cache-coherence history

The source set establishes one CPU/cache/main-storage relation plus channel-store updating. It does not establish later multiprocessor coherence protocols, invalidation buses, MESI-like states, dirty bits, or write-back ownership.

### X — cache semantics are not derived from SRAM substrate alone

Liptay's concluding wording is `fast monolithic storage`; this case does not need to identify the exact bit-cell family to ground cache semantics. The cache role is created by correspondence, validity, demand loading, currentness maintenance, and replacement policy above the storage element.

---

## Failure / forgetting boundaries

The primary sources describe the machinery used to prevent stale or misassigned fast copies. From that mechanism, the bounded engineering failure classes are:

- wrong sector-address correspondence → a data array could be associated with the wrong main-storage region;
- wrong validity state → an unloaded/obsolete block could be admitted, or a loaded block unnecessarily missed;
- missed resident-copy update on a processor/channel store → cache/current main-storage disagreement;
- incorrect replacement-policy state → performance/residency error without necessarily changing main-storage data;
- cache-sector reassignment → deliberate loss of fast-copy residency, not loss of authoritative main-storage state.

These are mechanism-level failure classes, not a claim that IBM documented field failures of each type in these two sources.

---

## Why this is enough for `grounded`

The bounded Case 08 claim set no longer depends on a modern cache textbook or a single unspecific retrospective:

- Liptay 1968 supplies directly inspected period pages, vocabulary, organization, validity, replacement, demand loading, and store/update semantics;
- IBM's 1967 functional manual independently corroborates the system-level buffer/currentness behavior;
- related-repository duplication was checked;
- the case records mechanism, currentness maintenance, replacement, failure classes, counterexamples, terminology boundaries, and cross-case limits.

What remains open belongs to **later cache regimes**, not to this promotion:

- write-back / dirty-state retention;
- multi-processor cache coherence and invalidation protocols;
- later set-associative/tag terminology histories;
- cache error-detection/ECC mechanisms;
- exact circuit technology of the Model 85 fast monolithic store if a semiconductor-device history is wanted.

Those should be separate bounded slices rather than silently folded into the Model 85.
