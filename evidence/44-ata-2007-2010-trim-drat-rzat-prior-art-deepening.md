# Case 44 deepening — ATA TRIM, DRAT, and RZAT before NVMe Deallocate

## Status

**`bounded deepening complete`** — bounded to the 2007–2010 T13 proposal trail that turned a deleted-data notification into ATA `DATA SET MANAGEMENT` / `Trim`, then separated post-Trim read behavior into indeterminate, deterministic, and deterministic-zero contracts.

Parent case: [`../cases/44-nvme13-deallocate-sanitize-forgetting.md`](../cases/44-nvme13-deallocate-sanitize-forgetting.md).

This record deepens the **prior-art and terminology boundary** for Case 44. It does not replace the NVMe 1.3 grounding and does not claim a direct ATA→NVMe implementation genealogy.

---

## Research question

Case 44 already records that NVMe 1.3 explicitly compares its `Deallocate` behavior with ATA Trim and SCSI UNMAP, and already warns against an `NVMe invented deallocation` story. The remaining narrower question is:

> What did the ATA proposal trail actually mean by `Trim`, and when did the host-visible read-after-deallocation contract become a separately advertised property rather than an automatic consequence of the deallocation request itself?

That question matters because several relations are easy to collapse:

```text
host says data is no longer needed
    != logical range has a Trim/deallocation state
    != future host reads return one fixed value
    != future host reads return zero
    != old physical embodiment has been erased
    != media has been sanitized
```

The 2007–2010 T13 trail is unusually useful because the vocabulary itself changes while the committee is negotiating those distinctions.

---

## Source and evidence classes

### Primary institutional provenance

The official T13 document archive records the proposal family and submission dates:

- `e07154r0` — **Notification for Deleted Data Proposal for ATA-ACS2**, Frank Shu (Microsoft), submitted **2007-04-23**;
- `e07154r1` — **Data Set Management Proposal for ATA-ACS2**, submitted **2007-08-19**;
- `e07154r2` — the same proposal family, submitted **2007-09-06**;
- `e07154r6` — **Data Set Management Proposal for ATA-ACS2**, submitted **2008-01-10**; the document's internal revision history records the December 2007 plenary revision;
- `e08137r0` through `e08137r4` — **DRAT - Deterministic Read After Trim**, October–December 2008;
- `e09117r0/r1` — **Read Zero after Trim**, April/June 2009;
- `e09158r0/r1/r2` — **Trim Clarifications**, December 2009–February 2010.

The T13 archive is used as the authoritative identity/date record for these proposal artifacts.

### Proposal-text witnesses

The T13 server currently exposes the document identities but direct PDF retrieval may reject automated access. Exact proposal text was therefore checked through preserved public facsimiles/text renderings while retaining the official T13 archive as the provenance anchor.

Evidence strength is therefore split explicitly:

- **strong for document identity, title, author, and submission sequence** — official T13 archive;
- **strong-to-moderate for proposal wording** — page-preserving public facsimiles / extracted proposal text matching the T13 document numbers;
- **not a final-standard claim** — these are proposal/draft artifacts unless stated otherwise.

---

## Historical record 1 — April 2007 begins as deleted-data notification

T13 `e07154r0` is titled **Notification for Deleted Data Proposal for ATA8-ACS2**. The preserved proposal text describes a host command whose purpose is to tell the device that specified LBA ranges contain deleted / invalid data.

The proposal's mechanism-level rationale is already SSD-specific. After receiving deleted-data information, the device can mark the transferred LBAs as invalid, disregard those data during later merge and wear-leveling work, and, when whole erase blocks become disposable, may pre-erase them for later write performance.

This establishes an early control relation:

```text
host/filesystem knowledge of obsolete data
    -> notification to device
    -> device may stop treating those LBAs as data worth preserving during internal maintenance
```

What it does **not** establish is equally important:

```text
notification of deleted data
    != immediate NAND erase
    != verified physical disappearance
    != sanitize operation
```

The proposal is about communicating **currentness/usefulness information** across a host/device boundary so the device can optimize later maintenance.

### Terminology note

The April 2007 title uses `Notification for Deleted Data`, not the later stable framing of a generic `Data Set Management` command with a `Trim` attribute. That historical vocabulary should be preserved rather than silently rewritten with later terms.

---

## Historical record 2 — the proposal broadens from one delete command to generic data-set attributes

By `e07154r6`, the proposal is titled **Data Set Management Commands Proposal for ATA8-ACS2**. Its introduction says that the first version had been a `Trim` command proposal carrying information about deleted data blocks, but that other host-supplied access-behavior information could also be useful to the device. The proposal therefore generalizes the interface around **data set attributes**.

Its revision history is useful evidence of terminology negotiation:

- the October 2007 revisions move `Trim` into an extensible attribute space;
- the **2007-11-01** revision records the decision to name the attribute **`Trim` instead of `Deallocated`**;
- later November/December revisions refine the Trim description and integrate the proposal with ATA-ACS text.

The historical point is not merely lexical. The proposal architecture separates:

```text
DATA SET MANAGEMENT command framework
    -> attribute namespace
        -> Trim as one attribute
```

So `Trim` is not best reconstructed as a universal synonym for every data-management or erase operation.

### Engineering boundary

A host can transmit a statement about the status/usefulness of an LBA range without prescribing the physical mechanism by which the device realizes that statement.

That yields:

> **range-status information != physical maintenance algorithm**.

This is engineering reconstruction from the proposal structure, not T13's philosophical language.

---

## Historical record 3 — `e07154r6` deliberately permits indeterminate reads

The December-2007 revision text says that when Trim is set, data in the addressed logical blocks become **indeterminate**. A later successful write makes the block determinate again.

That is a much weaker contract than `erase this NAND page now` or even `return zero from now on`.

The immediate retention consequence is:

```text
Trimmed LBA
    -> old logical value no longer has to remain the host-visible value
    -> read value may be indeterminate
    -> later write re-establishes an ordinary determinate value
```

The proposal therefore already blocks a common retrospective shortcut:

> **Trim != zero fill**.

It also blocks:

> **Trim != proof of material erasure**.

The interface weakens the device's obligation to preserve a prior host-visible association; it does not, in this proposal text, define a forensic media-sanitization proof.

---

## Historical record 4 — 2008 DRAT turns read-after-Trim behavior into an advertised capability

T13 `e08137r4`, **Deterministic TRIM Proposal for ATA8-ACS2**, dated **2008-12-17**, explicitly states that `e07154r6` introduced `DATA SET MANAGEMENT` / Trim with non-deterministic read behavior. The proposal says this can create host problems, including possible data corruption, and notes the need to coordinate with the parallel T10/SCSI work and SAT translation.

Its proposed solution is not to redefine Trim as physical erase. Instead it adds an **IDENTIFY DEVICE capability bit** telling the host whether post-Trim reads are deterministic or non-deterministic.

The proposed contract is subtle:

- if deterministic-read-after-Trim is supported, then after a trimmed LBA is read, subsequent reads of that LBA return the same data until a later successful write;
- if it is not supported, reads remain indeterminate;
- data returned for a trimmed LBA must not be sourced from data previously received for some **other** LBA.

This separates at least three state relations:

```text
Trim state
    != read determinism state
    != provenance constraint on returned read data
```

The third relation matters. Even while the proposal permits non-deterministic or arbitrary values in some cases, it constrains cross-LBA leakage. `Indeterminate` is therefore not equivalent to `the controller may expose any other user's old sector contents`.

### Bounded terminology

`DRAT` is used here as **Deterministic Read After Trim**. This record does not assume that every later ATA/SATA document places the capability in exactly the same IDENTIFY word/bit position as every intermediate proposal revision; bit assignments changed during standardization and clarification.

---

## Historical record 5 — 2009 Read Zero after Trim adds a stronger value contract

T13 `e09117r1`, **Read zero after TRIM Proposal for ATA8-ACS2**, dated June 2009 in the preserved facsimile, starts from a narrower interoperability requirement: some host/SCSI use cases need reads after Trim to return all zeroes.

The proposal therefore adds another advertised capability layered on top of deterministic read-after-Trim. Its text distinguishes:

```text
Trim supported
    + DRAT not supported
        -> indeterminate read behavior

Trim supported
    + DRAT supported
        -> determinate read behavior

Trim supported
    + DRAT supported
    + read-zero capability
        -> post-Trim reads return zero
```

The key retention boundary is:

> **deterministic read after Trim != deterministic read zero after Trim**.

A fixed host-visible value and a zero host-visible value are separate guarantees.

And neither guarantee establishes by itself that the old physical Flash embodiment has already been erased.

---

## Historical record 6 — 2009–2010 clarification stabilizes the three-way read taxonomy

The official T13 archive records `e09158r0/r1/r2` as **Trim Clarifications**, with `r2` submitted in February 2010. The preserved proposal text explicitly coordinates three signals:

- Trim support;
- DRAT;
- RZAT / read-zero-after-Trim.

The clarification table distinguishes:

1. **indeterminate read after Trim** — different reads may return different data;
2. **deterministic read after Trim** — after a read is processed, subsequent reads to that LBA return the same data until a later write;
3. **deterministic read zero after Trim** — the deterministic returned value is zero.

It retains the cross-LBA provenance constraint: data read from a trimmed LBA must not be retrieved from data previously written by the application client to another LBA.

This is the bounded point at which the proposal trail becomes especially useful for Case 44:

```text
allocation/currentness hint
    != host-visible read-value contract
    != physical-media state
```

The first two are both standardized-interface concerns, but they are different interface concerns.

---

## Engineering reconstruction — deallocation has multiple observable surfaces

The ATA proposal trail supports a more precise decomposition than simply saying `TRIM deletes blocks`:

```text
filesystem/application currentness
    -> host knows range is no longer useful

host/device notification state
    -> Trim range is communicated to device

allocation / preservation obligation
    -> device may stop preserving the old association during maintenance

read-value contract
    -> indeterminate / deterministic / deterministic-zero

internal reclamation eligibility
    -> controller may omit stale data during merge/GC and may pre-erase eligible blocks

physical embodiment
    -> old NAND state may or may not have been erased yet

sanitization assurance
    -> separate stronger claim requiring its own mechanism and evidence
```

This reconstruction is project terminology. T13 did not present it as a seven-layer ontology.

The benefit of the decomposition is negative as much as positive:

```text
RZAT observed
    != raw NAND erase observed

DRAT observed
    != old payload physically absent

Trim command accepted
    != garbage collection completed

old physical page erased later
    != proof that Trim itself was a sanitize command
```

---

## Functional comparison with NVMe 1.3 Case 44

NVMe 1.3 itself says its Deallocate behavior is similar to ATA DATA SET MANAGEMENT with Trim. The proposal history makes the comparison more disciplined.

### Shared functional structure

Both interface families can express a host/device relation weaker than sanitization:

```text
host no longer requires prior LBA contents as ordinary current data
    -> device gains freedom to change allocation/reclamation handling
```

Both also separate deallocation from a stronger media-sanitization objective.

### Important semantic difference

The exact read-after-deallocation contracts are not identical across the historical documents.

The ATA proposal trail explicitly negotiates indeterminate, deterministic, and deterministic-zero behaviors. NVMe 1.3's deallocated-LBA contract, as grounded in Case 44, permits specific returned-value classes and gives its own deterministic semantics.

Therefore:

> **ATA Trim prior art != proof that NVMe copied ATA bit-for-bit or behavior-for-behavior.**

The relation here is **functional prior art plus terminology/interface comparison**, not implementation genealogy.

---

## Cross-case comparison

### With Case 04 — mapped Flash

Case 04 shows that a logical block can become non-current before its old physical embodiment is erased. The ATA Trim trail adds a later host/controller signal by which the host can tell the storage device that certain logical data no longer need preservation.

Functional relation only:

```text
logical invalidation/currentness change
    -> reclamation eligibility may change
    -> physical erase may happen later
```

This is not a claim that the 1993 mapped-Flash mechanism directly evolved into ATA Trim.

### With Case 47 — SSD sanitization verification

Case 47 asks whether an SSD's erase/sanitize mechanism actually makes prior data unrecoverable, including hidden Flash embodiments and key-bearing metadata.

The ATA Trim trail is a useful negative control:

```text
Trim semantics / read-value semantics
    != sanitize-compliance evidence
```

A standard host read returning zero after Trim is an interface observation. It is not the same evidence class as raw-Flash inspection or key-store verification.

### With Case 150 — garbage collection / reclamation

Case 150 already separates GC presence, reclaim eligibility, execution, physical erase, and observed recoverability. The ATA 2007 proposal provides an earlier interface-level witness for one way **reclaim eligibility information** can cross from host knowledge into device policy.

Again, this is functional comparison, not a claim that all controllers implement Trim through the same garbage-collection algorithm.

---

## Historical record vs reconstruction vs analogy vs interpretation

### Historical record

The following are period-source claims:

- T13 document numbers, titles, authors, and proposal dates;
- `e07154r0` framing as deleted-data notification;
- `e07154r6` broadening to Data Set Management / data-set attributes;
- the revision-history rename from `Deallocated` to `Trim`;
- `e07154r6` indeterminate post-Trim read semantics;
- `e08137r4` DRAT proposal and deterministic-vs-nondeterministic distinction;
- `e09117r1` read-zero-after-Trim proposal;
- `e09158r2` clarification of Trim / DRAT / RZAT interaction.

### Engineering reconstruction

Project-level reconstructions include:

- deallocation/currentness, read-value semantics, reclamation eligibility, physical erasure, and sanitization assurance are separate state relations;
- read-zero is an interface value contract, not direct evidence of erased cells;
- Trim transfers negative/currentness information that can change what the controller needs to preserve during later maintenance.

### Functional analogy

The comparison to NVMe Deallocate, Case 04 invalidation/reclamation, Case 47 sanitization, and Case 150 garbage collection is functional unless a source explicitly states an interface relationship.

NVMe 1.3's own statement that Deallocate is similar to ATA Trim is historical interface comparison; it still does not prove shared implementation.

### Philosophical interpretation

A narrow project interpretation follows:

> A storage system can withdraw an obligation to preserve one logical association before it has destroyed every material trace capable of embodying the old value.

And:

> What counts as `forgotten` depends on the observation layer: the host read contract can change before the medium's physical history has disappeared.

These are repository interpretations, not statements of T13 authorial intent.

---

## Explicit non-claims

This deepening does **not** claim that:

1. T13 `e07154r0` is the first deallocation/discard idea in storage history;
2. Microsoft or Frank Shu invented logical deallocation;
3. ATA Trim invented garbage collection, invalid-page marking, or Flash reclamation;
4. the April 2007 proposal was identical to the final published ATA standard;
5. every intermediate proposal bit assignment survived unchanged;
6. `Trim` and `Deallocated` were merely stylistic synonyms with no interface-design context;
7. Trim acceptance means NAND erase has completed;
8. DRAT means the returned value is zero;
9. RZAT proves that old NAND charge is physically gone;
10. indeterminate read behavior permits cross-LBA leakage;
11. a controller must perform garbage collection immediately after Trim;
12. ATA Trim and SCSI UNMAP are implementation-identical;
13. ATA Trim and NVMe Deallocate are implementation-identical;
14. NVMe's later deallocation semantics are a direct line-by-line descendant of these ATA proposals;
15. Trim is a sanitization command;
16. successful host-level undelete failure proves raw-media unrecoverability;
17. a later raw-media erase, if it occurs, proves that Trim itself supplied sanitize assurance;
18. all SSDs implement the proposal's optimization opportunities the same way.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| T13 records `e07154r0` as `Notification for Deleted Data Proposal for ATA-ACS2` submitted 2007-04-23 | H/P | official T13 archive |
| T13 records `e07154r1` as `Data Set Management Proposal for ATA-ACS2` submitted 2007-08-19 | H/P | official T13 archive |
| `e07154r6` generalizes the interface around Data Set Management / data-set attributes | H/P | preserved proposal facsimile/text + official document identity |
| `e07154r6` revision history records renaming the attribute from `Deallocated` to `Trim` on 2007-11-01 | H/P | preserved proposal revision history |
| `e07154r6` says Trim makes addressed logical-block data indeterminate until a later write makes it determinate | H/P | preserved proposal text |
| `e08137r4` explicitly identifies `e07154r6` as non-deterministic and proposes advertised deterministic-read-after-Trim behavior | H/P | proposal facsimile + official T13 identity |
| `e08137r4` prohibits satisfying a trimmed-LBA read with data previously received for another LBA | H/P | proposal text |
| `e09117r1` proposes separately identifying read-zero-after-Trim capability | H/P | proposal facsimile + official T13 identity |
| `e09158r2` clarifies Trim / DRAT / RZAT as distinct advertised behavior combinations | H/P | preserved proposal text + official T13 identity |
| `DRAT == RZAT` | X | contradicted by the proposal sequence and capability split |
| `RZAT == physical erase` | X | no physical-erasure claim follows from the host read-value contract |
| `Trim == sanitize` | X | proposal purpose/read semantics are weaker than media-sanitization assurance |
| `deallocation/currentness != read-value contract != physical-media state` | E | reconstruction from the proposal family |
| the ATA trail and NVMe 1.3 share a bounded host-to-device deallocation function | F/H | functional comparison; NVMe 1.3 itself notes similarity to ATA Trim |

---

## Sources

### Primary institutional index

- Technical Committee T13, **Documents / Document Search** — official entries for `e07154r0/r1/r2/r6`, `e08137r0-r4`, `e09117r0/r1`, and `e09158r0-r2`: <https://t13.org/docsearch>.

### Period proposal artifacts / preserved facsimiles

- Frank Shu (Microsoft), **T13/e07154r0, Notification for Deleted Data Proposal for ATA8-ACS2**, April 2007. Official T13 identity/date; preserved text mirror used for content inspection.
- Frank Shu (Microsoft), **T13/e07154r6, Data Set Management Commands Proposal for ATA8-ACS2**, revision dated December 12, 2007; official T13 archive records submission January 10, 2008. Preserved PDF/text facsimile: <https://www.sgv417.jp/~makopi/blog/wp-content/uploads/2018/05/e07154r6-Data-Set-Management-Proposal-for-ATA-ACS2.pdf>.
- Fred Knight, **T13/e08137r4, Deterministic TRIM Proposal for ATA8-ACS2**, December 17, 2008. Official T13 identity; preserved facsimile: <https://pcper.com/wp-content/uploads/2009/04/b2e2-e08137r4-drat-deterministic-read-after-trim.pdf>.
- Fred Knight, **T13/e09117r1, Read zero after TRIM Proposal for ATA8-ACS2**, 2009. Official T13 identity; preserved facsimile: <https://www.sgv417.jp/~makopi/blog/wp-content/uploads/2018/05/e09117r1-Read-Zero-after-Trim.pdf>.
- Fred Knight, **T13/e09158r2, Trim Clarifications**, February 2010. Official T13 identity; preserved public text rendering inspected for the Trim / DRAT / RZAT table and wording.

### Contemporary secondary context

- PC Watch, **SSDに関するWindows 7の3つの特徴**, 2009. Used only as contemporary context for why indeterminate post-Trim reads drew interoperability concern; not used to replace T13 proposal text.

---

## Related repository check

`tmzncty/computing-archaeology` was searched again before writing for `TRIM` and `DATA SET MANAGEMENT`; no dedicated ATA Trim / Data Set Management history was returned. This evidence therefore records only the retention-specific proposal semantics needed by Case 44. A broader genealogy of filesystem discard, SCSI UNMAP, SATA queued Trim, OS adoption, controller firmware, and the final ATA standardization path belongs primarily in `computing-archaeology` if developed later.

---

## Remaining evidence debt

This bounded slice closes the immediate **2007–2010 ATA proposal-semantic prior-art gap** for Case 44, but does not close the broader history.

Useful next work would be:

- directly inspect a final/published ATA8-ACS / ACS-2 normative edition and map which proposal wording survived;
- inspect T10 `08-347` and the SAT/SCSI work cited by `e08137r4` rather than inferring the interoperability problem only from the ATA proposal;
- trace when `RZAT` became the stable abbreviation and exactly which IDENTIFY word/bit assignments survived into published revisions;
- add a named early commercial SSD/firmware that advertises Trim + DRAT/RZAT and test its actual read behavior;
- separate standard host reads from raw-NAND/diagnostic observations in a controlled experiment;
- move any full ATA/SCSI discard genealogy into `computing-archaeology` and link it back rather than duplicating it here.
