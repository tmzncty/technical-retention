# Evidence 150 — T13 2007–2010 ATA TRIM Read Semantics: Logical Retirement, Read Contract, and Physical Reclamation Boundaries

## Status

**`bounded deepening complete`**

## Why this slice exists

Case 150 already separates host/filesystem retirement, ATA TRIM/deallocation knowledge, controller-local garbage collection, and eventual erase-block reclamation. What remained underdeveloped was the **host-visible read contract after TRIM**.

That distinction matters because a block-interface device can change what a host is entitled to observe at an LBA **before** any source establishes that the underlying NAND cells have been physically erased or that a garbage-collection cycle has completed.

This slice therefore asks one bounded question:

> **What did the T13 ATA8-ACS2 proposal chain from 2007 through 2010 say about reads from trimmed LBAs, and what does that establish — or fail to establish — about logical retirement versus physical reclamation?**

It does **not** reconstruct Crucial M550 firmware. It does not claim that the M550 advertised DRAT or RZAT, that its controller implemented any particular post-TRIM return path, or that these T13 proposals describe Micron/Crucial internal garbage collection.

---

## Source-class note

The evidence chain uses two source classes together:

1. the **current T13 document index**, which preserves document numbers, titles, authors, and submission dates; and
2. readable facsimiles/mirrors of the historical T13 proposal PDFs where the current T13 site's direct PDF links were not reliably fetchable during this review.

The T13 index is the provenance anchor. The mirrors are used for proposal text inspection. This is weaker than an origin-hosted byte-for-byte archival chain, so the repository does not claim archival custody of the mirrored PDFs.

The relevant T13 index entries include:

- `e07154r0`, **Notification for Deleted Data Proposal for ATA-ACS2**, Frank Shu (Microsoft), 23 April 2007;
- `e07154r1` through `e07154r6`, **Data Set Management Proposal for ATA-ACS2**, culminating in the 10 January 2008 T13 index entry for r6;
- `e08137r0` through `e08137r4`, **DRAT - Deterministic Read After Trim**, Frederick Knight, October–December 2008;
- `e09117r0/r1`, **Read Zero after Trim**, Frederick Knight, April–June 2009;
- `e09158r0/r1/r2`, **Trim Clarifications**, Fred Knight, December 2009–February 2010.

Official T13 document index:

- <https://t13.org/index.php/documents?created%5Bmax%5D=&created%5Bmin%5D=&order=field_author&page=115&sort=desc>
- <https://t13.org/docsearch?field_author_value=&field_document_number_value=&field_document_stage_target_id=All&field_document_type_target_id=All&field_document_type_target_id_1=All&order=field_document_number&page=70&sort=asc&title=>

---

# I. Historical record

## 1. 2007: Data Set Management starts as host-to-device knowledge about data no longer needed

The r6 facsimile of Frank Shu's **Data Set Management Commands Proposal for ATA8-ACS2** records a revision history beginning from a proposal that had been called a `Trim` command proposal. Its introduction describes the purpose as carrying information related to deleted data blocks from host to device so that the device can optimize internally; it then generalizes the mechanism into `data set attributes`.

Readable facsimile:

<https://www.sgv417.jp/~makopi/blog/wp-content/uploads/2018/05/e07154r6-Data-Set-Management-Proposal-for-ATA-ACS2.pdf>

The r6 text makes the post-TRIM logical state explicit:

- when Trim is set, data in the specified logical blocks becomes **indeterminate**;
- once a trimmed LBA is written again, the data in that logical block becomes **determinate** and contains the written data;
- Trim does not add or remove LBAs from the NV Cache Pinned Set.

This is already enough to reject a simplistic equation:

```text
TRIM
    = command to physically erase the NAND now
```

The proposal defines a **logical/interface state transition** for addressed LBAs. It does not, in the inspected text, define a NAND erase-block transaction whose completion proves physical destruction of the old cell contents.

### Historical boundary

The repository therefore records the 2007 proposal conservatively as:

```text
host says specified logical data are no longer required
    -> device receives a Data Set Management / Trim relation
    -> post-Trim logical read contents are not required to remain the old written payload
```

It does **not** convert that into:

```text
Trim accepted
    -> corresponding NAND pages physically erased synchronously
```

That second arrow would require lower-layer implementation evidence that the proposal does not provide.

---

## 2. 2008: deterministic read after TRIM is proposed because indeterminacy is itself an interface problem

T13's current index records the `e08137` DRAT proposal series from October through December 2008. Revision 4 is dated **17 December 2008** in the readable facsimile and records an initial revision on 18 October 2008 plus later meeting-driven revisions.

Readable facsimile:

<https://pcper.com/wp-content/uploads/2009/04/b2e2-e08137r4-drat-deterministic-read-after-trim.pdf>

The proposal explicitly says `e07154r6` added DATA SET MANAGEMENT and TRIM and that its non-deterministic read behavior could cause host problems. It therefore proposes a way for a host to identify whether a device provides deterministic or non-deterministic behavior after TRIM.

The key rule is not “all trimmed LBAs become zero.” Instead, DRAT means that after a trimmed LBA has been read, the logical block becomes determinate: subsequent reads return the same data until a later successful write to that LBA. Without DRAT, data read after TRIM may remain indeterminate.

The proposal also adds a security-oriented constraint: data returned for a trimmed LBA must not be sourced from data previously received from an application client for **another** LBA.

### Historical boundary

By late 2008, the T13 proposal discussion was therefore separating at least three questions:

```text
1. was this LBA trimmed?
2. if the trimmed LBA is read, is the result deterministic?
3. what value, if any, must that deterministic read return?
```

The third question was not yet equivalent to “zero.”

---

## 3. 2009: Read Zero after Trim adds another advertised semantic layer

T13's index records `e09117r0` on 13 April 2009 and `e09117r1` on 16 June 2009. The readable r1 facsimile describes the motivation as host use cases where reads after TRIM return all zero bits and the need for ATA identification compatible with SCSI/SAT translation.

Readable facsimile:

<https://www.sgv417.jp/~makopi/blog/wp-content/uploads/2018/05/e09117r1-Read-Zero-after-Trim.pdf>

The proposal distinguishes:

- TRIM support;
- deterministic read after TRIM;
- read-zero-after-TRIM behavior.

For the proposed read-zero case, a read of a trimmed LBA returns words cleared to zero. If deterministic behavior is advertised without the read-zero property, the determinate value may instead contain any words. If deterministic behavior is not advertised, post-TRIM read data may be indeterminate.

This matters because it makes the host-visible post-retirement contract **explicitly richer than physical erase state**.

A device can promise:

```text
read(trimmed LBA) -> zero
```

without that proposition, by itself, proving:

```text
old physical NAND embodiment has already been erased
```

The former is a block-interface observation contract. The latter is a lower-layer media-state claim.

---

## 4. 2009–2010: DRAT/RZAT clarification turns the distinctions into an explicit interaction table

T13's current index records `e09158r0` and `e09158r1` on **14 December 2009**, and r2 on **22 February 2010**. The readable r1 facsimile is dated 14 December 2009; the r2 transcription/facsimile record says the revision incorporated February plenary comments.

Readable r1 facsimile:

<https://www.sgv417.jp/~makopi/blog/wp-content/uploads/2018/05/e09158r1-Trim-Clarifications.pdf>

T13 index entry for r2:

<https://t13.org/index.php/documents?created%5Bmax%5D=&created%5Bmin%5D=&order=field_author&page=115&sort=desc>

The clarification identifies three independent advertised bits/relations:

- TRIM support — IDENTIFY DEVICE word 169 bit 0;
- DRAT — word 69 bit 14;
- RZAT — word 69 bit 5.

Its interaction table distinguishes:

```text
TRIM unsupported

TRIM supported + DRAT not supported
    -> indeterminate read-after-TRIM behavior

TRIM supported + DRAT supported + RZAT not supported
    -> deterministic read-after-TRIM behavior
       with words allowed to have any value

TRIM supported + DRAT supported + RZAT supported
    -> deterministic read-after-TRIM behavior
       with words returned as zero
```

The same proposal retains two important limits:

1. data returned for a trimmed LBA shall not be retrieved from payload previously written by an application client to some **other** LBA;
2. after a trimmed LBA is successfully written, its logical data become determinate as the written data.

---

# II. Engineering reconstruction

The terms in this section are project-level analytical vocabulary unless quoted above. They are not retroactively attributed to T13 participants.

## 5. TRIM creates a controller-relevant negative-currentness relation

For Case 150, the useful engineering reconstruction is:

```text
upper layer no longer needs old logical payload
    -> host communicates Trim for LBA range
    -> device may stop treating the old payload as required current data
    -> device gains freedom for internal optimization / reclamation
```

This is a **negative-currentness authority**: the device receives evidence that preserving the prior payload at those logical addresses is no longer part of the host's current-data contract.

But that authority is not the same thing as a completed physical reclaim operation.

So keep separate:

```text
host retirement decision
    != Trim delivery
    != post-Trim read contract
    != internal stale/invalid-page bookkeeping
    != victim-block selection
    != live-page relocation
    != block erase
    != reusable free-block completion
```

---

## 6. Interface forgetting can precede physical forgetting

The DRAT/RZAT proposal chain makes a particularly useful state separation visible.

At the ATA interface, a trimmed logical address may already cease to expose its former payload as authoritative current data. Under RZAT, for example, the host-visible result is zero. Yet the inspected T13 proposals do not require that this zero result be implemented by synchronously erasing the physical NAND cells that previously embodied the logical payload.

Therefore:

```text
old payload no longer host-visible at the LBA
    != old cell pattern proved physically absent
```

This is a critical Case-150 boundary because garbage collection can occur later:

```text
logical retirement / deallocation knowledge
    -> controller may classify old embodiments as unnecessary
    -> GC can later avoid preserving them during live-data relocation
    -> erase block may later be reclaimed
```

The host can therefore lose **logical observability** before the controller has necessarily completed **physical reclamation**.

---

## 7. Determinism is not erase evidence

DRAT and RZAT are read-behavior contracts.

They answer questions like:

- can repeated reads return changing values?
- once a value becomes determinate, must subsequent reads remain the same until rewrite?
- must that value be zero?

They do **not**, by themselves, answer:

- has the prior NAND page been erased?
- has a containing mixed erase block been selected as a GC victim?
- have still-live pages been copied elsewhere?
- has old mapping metadata been retired?
- has free-block accounting been updated?
- is every physical embodiment of the old payload irrecoverable by privileged/internal means?

Hence:

```text
DRAT/RZAT satisfaction
    != garbage-collection completion evidence
    != sanitize completion evidence
```

---

## 8. The proposal chain exposes multiple kinds of retained state

The mechanism is especially relevant to a repository about retention because the device may need to retain different classes of state even after the old user payload is logically retired.

Conceptually, a controller may still need enough control information to know:

- which LBA ranges have been trimmed;
- what post-TRIM read behavior it advertises;
- whether a later host write re-establishes current payload for that LBA;
- which physical pages may be omitted from preservation during GC;
- which live pages in the same erase block still must be preserved.

The T13 proposals establish the **interface obligations**, not the specific internal representation of that state. They do not say that an M550 uses a trim bitmap, journal, flash-resident invalid-page table, or any particular cache structure.

Thus:

```text
old payload may become non-current
    while
control state about how that LBA must behave remains necessary
```

Forgetting payload can require retaining policy/currentness information.

---

## 9. Cross-LBA non-substitution is a separate confidentiality boundary

The DRAT and later clarification proposals state that data returned from a trimmed LBA must not be retrieved from data previously received from an application client for another LBA.

This is important but narrow.

It means the device is not allowed to satisfy post-TRIM read freedom by exposing another logical address's prior host payload. It does **not** prove that the trimmed LBA's own prior physical bits are gone, nor does it prove that all spare/remapped/cache copies have been purged.

So:

```text
cross-LBA substitution forbidden
    != own-LBA remanence eliminated
    != sanitize guarantee
```

---

# III. Functional comparison

## 10. Case 150 — managed SSD garbage collection

This evidence deepens Case 150's existing split:

```text
TRIM/deallocation knowledge
    != garbage collection
```

The T13 proposal chain adds a middle layer:

```text
host retirement
    -> Trim/deallocation knowledge
    -> post-Trim read contract changes
    -> controller internal reclamation authority/opportunity
    -> live-data relocation if needed
    -> erase-block reclamation
```

Not every implementation must expose these as separately timed internal events, but the source evidence does not permit collapsing them into one atomic physical erase.

---

## 11. Case 44 — NVMe Deallocate / sanitize boundary

Case 44 is a functional comparison, not a genealogy claim.

Both ATA TRIM and NVMe Deallocate belong to the broad family of host-to-device statements that some logical data need no longer remain current. Security sanitize operations have a different completeness/authority goal.

The comparison is therefore useful only at this level:

```text
logical deallocation
    != security purge
```

The ATA DRAT/RZAT bit semantics must not be imported into NVMe unless the NVMe specification independently defines equivalent behavior.

---

## 12. Case 145 — JFFS2 raw-flash GC

JFFS2 exposes stale/obsolete-node state and reclamation machinery in filesystem code. ATA TRIM instead crosses a block-interface boundary into a managed device whose internal mapping and victim-selection logic are hidden.

Both can express “this old embodiment no longer needs preservation,” but their authority locations and observability differ.

Shared functional relation does not prove shared implementation or historical descent.

---

# IV. Philosophical interpretation — bounded

The source-backed engineering relation supports one restrained observation:

> **A system can stop presenting an old value as current before the material substrate that once carried it is proved destroyed.**

This is not metaphysics. It is an interface/currentness distinction.

For a trimmed LBA, the system may have already changed the rule governing what counts as the current readable value, while physical reclamation remains a separate lower-layer process.

A second bounded observation follows:

> **Forgetting one payload can require retaining the rule that it is no longer authoritative.**

Again, this is an engineering statement about control state, not a general theory of memory or human forgetting.

---

# V. Explicit non-claims

This deepening does **not** claim any of the following:

1. T13 invented logical deallocation.
2. T13 invented SSD garbage collection.
3. Frank Shu or Frederick Knight invented every mechanism discussed by the proposals.
4. `e07154r6` is the first historical appearance of every TRIM-like concept.
5. the proposal sequence proves direct genealogy into Crucial M550 firmware.
6. the M550 advertises DRAT.
7. the M550 advertises RZAT.
8. the M550 returns zero after every TRIM.
9. a successful TRIM command synchronously erases NAND.
10. DRAT proves that NAND was erased.
11. RZAT proves that NAND was erased.
12. a zero returned by the block interface is a direct read of erased NAND cells.
13. post-TRIM indeterminacy means the device may expose another LBA's old user data; the proposals explicitly constrain cross-LBA substitution.
14. a trimmed LBA's own old physical pattern is necessarily recoverable.
15. ordinary TRIM is a sanitize operation.
16. ordinary garbage collection is a sanitize operation.
17. the proposals specify victim-block selection.
18. the proposals specify live-page relocation order.
19. the proposals specify FTL map-publication atomicity.
20. the proposals specify crash recovery for TRIM bookkeeping.
21. the proposals specify how trim state survives sudden power loss.
22. the proposal PDFs mirrored outside T13 have authenticated origin-host archival custody.
23. the reviewed proposal wording is necessarily byte-identical to the final published ANSI/INCITS ACS-2 text.
24. the 2007–2010 proposal chronology proves influence on any particular SSD controller product without separate product evidence.

---

# VI. Claim ledger

| Claim | Evidence | Strength | Limit |
|---|---|---|---|
| T13 records a 2007 `Notification for Deleted Data` / Data Set Management proposal sequence by Frank Shu | current T13 document index | high for document chronology | document listing is not implementation evidence |
| `e07154r6` makes trimmed logical-block data indeterminate until rewrite | readable r6 facsimile | high for proposal text | not proof of physical erase |
| late-2008 `e08137r4` introduces deterministic vs non-deterministic read-after-TRIM behavior | T13 index + readable r4 facsimile | high | proposal, not M550 product behavior |
| `e08137r4` forbids returning another LBA's prior client data for a trimmed LBA | readable r4 facsimile | high | not a sanitize guarantee |
| 2009 `e09117` adds a way to advertise read-zero-after-TRIM | T13 index + readable r1 facsimile | high | not proof zeroes come from erased NAND |
| 2009–2010 `e09158` explicitly separates TRIM, DRAT, and RZAT bits/behaviors | T13 index + readable r1/r2 record | high | proposal/clarification chain, not final-standard archival proof |
| host-visible post-TRIM currentness can change without source-backed proof of synchronous physical erase | engineering reconstruction from proposal semantics | strong | does not assert that old bits necessarily remain |
| DRAT/RZAT completion is not GC or sanitize completion evidence | scope comparison | strong | lower-layer implementation can choose many mechanisms |
| this chain directly describes M550 firmware | unsupported | reject | requires product-specific evidence |

---

# VII. Remaining evidence debt

1. Obtain an origin-hosted or standards-library copy of the final ATA8-ACS2/ACS-2 text and compare the final published clauses against the proposal chain without assuming unchanged wording.
2. Find product-specific IDENTIFY DEVICE captures or Micron/Crucial documentation for the M550 family if the repository later wants to say anything about actual M550 DRAT/RZAT advertisement.
3. Keep the broader ATA/SCSI deallocation genealogy, Windows 7 adoption history, controller-vendor adoption, and SATA transport history in `tmzncty/computing-archaeology`; this file should remain a retention/currentness boundary, not a general TRIM history.
4. If a controlled named-device experiment is added later, instrument at least command delivery, read-after-TRIM behavior, powered-idle interval, internal-write evidence where observable, and post-idle read behavior. Do not infer physical NAND erase solely from host reads.
5. Preserve the distinction between block-interface observability, controller mapping/currentness state, actual erase-block reclamation, and security sanitization.

---

# VIII. Related repository routing

A fresh search of `tmzncty/computing-archaeology` for `DRAT RZAT TRIM ATA` and `e07154` returned no dedicated packet to reuse in this run.

Division of responsibility:

- **`technical-retention` keeps:** logical retirement -> TRIM/deallocation knowledge -> post-TRIM read contract -> later reclamation/sanitize boundary.
- **`computing-archaeology` should keep if pursued:** T13/T10 proposal genealogy, Windows 7/WinHEC adoption, vendor/controller uptake, SATA transport evolution, product-by-product behavior, and actor-to-actor influence.

This avoids turning Case 150 into a general history of TRIM while still preserving the interface semantics needed to reason about retention and reclamation.
