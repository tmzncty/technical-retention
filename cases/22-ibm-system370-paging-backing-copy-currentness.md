# IBM System/370 OS/VS2 Paging: Virtual-Page Identity, Backing-Copy Currentness, and Conditional Writeback

## Status

**`grounded`** — bounded to the virtual-page / real-page-frame / external-page-storage relations documented for IBM OS/VS2 in 1972 and its RSM/ASM implementation description in 1976.

Grounding record: [`../evidence/22-ibm-1972-1976-paging-currentness-grounding.md`](../evidence/22-ibm-1972-1976-paging-currentness-grounding.md).

## Scope

This case asks one narrow question:

> When a virtual page stops occupying one real-storage page frame, what must remain true for the page to count as the same current retained state later?

The bounded system is IBM System/370 OS/VS2 as described in the July 1972 _OS/VS2 Planning Guide_ and the July 1976 _OS/VS2 System Logic Library, Volume 1_. The case focuses on page identity, residency, page-in/page-out, change/reference state, external page storage, and auxiliary-storage location bookkeeping.

This is **not** a general history of virtual memory, an Atlas-to-System/370 genealogy, a TLB/segmentation history, or a claim that IBM invented paging. It does not treat external page storage as an archival or crash-durable application record.

## Relation to Cases 08, 14, 04, and 16

The nearest existing cases expose superficially similar relocation relations but with different triggers and authority rules:

```text
Case 08 — Model 85 cache
    fast derivative copy can be discarded because bounded main storage remains authoritative

Case 14 — SCSI defect reassignment
    failure triggers physical-sector substitution behind a stable LBA

Case 04 — mapped Flash
    erase geometry drives out-of-place update, mapping, and reclamation

Case 16 — BSD FFS soft updates
    crash-admissible stable filesystem state is constrained by dependency ordering

Case 22 — OS/VS2 paging
    capacity/residency pressure reassigns real frames;
    an unchanged page can be dropped when an external copy already exists,
    but a changed real page must first be propagated to external page storage
```

The similarities are functional comparisons only. The historical mechanisms and vocabularies remain distinct.

## Historical vocabulary

The 1972 IBM guide uses `virtual storage`, `real storage`, `external page storage`, `page`, `page frame`, `page-in`, `page-out`, `page fault`, `page table`, `page fixing`, `change bit`, `reference bit`, and `paging supervisor`.

The 1976 System Logic Library additionally describes `real storage management (RSM)`, `auxiliary storage management (ASM)`, `auxiliary storage`, `page data set`, and 4096-byte `slots`.

This case uses **`changed page` / `change bit`** when describing the historical mechanism. `Dirty page` may be a modern explanatory gloss, but it is not substituted for IBM's period vocabulary.

## Historical record

### Page, frame, and external page storage are distinct objects

IBM's 1972 glossary defines a `page` as a fixed-length block transferable between real storage and external page storage, a `page frame` as the block of real storage that can contain a page, `page-in` as moving a page from external page storage into real storage, and `page-out` as moving it in the opposite direction.

The guide's explanatory diagrams and text distinguish virtual storage, real storage, and external page storage. A program can have a much larger virtual address space than the subset of pages currently mapped into real storage.

The 1972 glossary also defines a `page fault` as a reference to a page marked as not in real storage and describes the page table as indicating whether a page is in real storage and correlating virtual and real addresses.

### Page replacement uses reference/change information

When the supply of available page frames becomes low, the 1972 guide says the paging routines select page frames for reassignment, with selection based primarily on the `change` and `reference` bits.

The crucial conditional is explicit:

- if the selected page **has changed**, the changed page is moved to external page storage before the page frame is made available;
- if the page **has not changed**, it is not moved out when a copy already exists in external page storage.

IBM therefore documents two different outcomes of the same frame-reclamation event. Reassigning a frame does not by itself determine whether data transfer is required; that depends on whether another usable copy already represents the current page state.

### RSM and ASM preserve different parts of the relation

The 1976 System Logic Library describes RSM as administering real storage, assigning and repossessing page frames, associating virtual and real addresses, and directing page movement between real and auxiliary storage in 4096-byte blocks.

ASM performs the paging I/O and keeps track of auxiliary-storage locations for virtual pages. Its page data sets are formatted into 4096-byte `slots`, and a slot is allocated dynamically when a page must be moved out of real storage.

This later implementation description does not turn a page into its slot. It shows instead that a virtual page's recoverability can depend on retained location/control state outside the payload bytes themselves.

### Not every page is freely pageable

IBM also defines `page fixing` and describes pages that must remain in real storage for system reasons. RSM treats a page as pageable unless it has been fixed or belongs to resident system code/data.

This is an important counterexample to a simplistic `virtual address means physical location never matters` story. Virtual-memory abstraction can permit frame replacement without making every real-storage residency relation disposable.

## Retained state and substrate

At least four distinct state classes participate in the bounded mechanism:

1. **virtual-page contents** — the current bytes associated with the virtual page;
2. **residency/translation state** — whether the page is currently in real storage and which real frame answers for it;
3. **currentness/change state** — whether the real copy has diverged from the existing external copy enough to require page-out before frame reuse;
4. **external-location state** — the page data set / slot relation used to recover a nonresident page.

The page frame and external slot are embodiments or service locations. Neither should be silently equated with the virtual page's identity.

## Retention mechanism

The bounded retention mechanism is not one physical medium. It is a controlled relation across a hierarchy:

```text
virtual page identity
    ↓
current residency / translation state
    ↓
real page frame, when resident
    ↕
conditional page-out / page-in
    ↕
external page-storage copy + ASM location state
```

Frame pressure can terminate real-storage residency. Whether this requires copying the page first depends on currentness: a changed page must be propagated; an unchanged page with a valid external copy can lose its real frame without losing the virtual page's recoverable current state.

## Addressing and access geometry

The program addresses virtual storage. When the page is resident, translation resolves that designation to a real-storage page frame. When the page is marked nonresident and is referenced, a page fault transfers control to paging machinery, which recovers the page into real storage before execution can continue normally.

The stable designation therefore outlives one real frame, but **address continuity does not imply uninterrupted service**. A page fault inserts recovery work and latency between designation and ordinary access.

## Read semantics

Ordinary reads of a resident page do not, in this bounded evidence, create a destructive-read restoration obligation like magnetic core or a periodic retention deadline like DRAM.

A reference can, however, affect replacement policy through the reference state. The historical source makes page selection depend primarily on reference/change bits, so ordinary use can alter control state that influences which embodiment will later be displaced.

## Write and erasure semantics

A write to a resident page can make the real-storage representation newer than the external copy, recorded through the bounded change-state mechanism. That does not immediately require page-out. The transfer obligation becomes relevant when the frame is selected for reuse.

If the page is unchanged and an external copy already exists, IBM explicitly allows frame reassignment without another page-out. Thus:

> **page replacement ≠ page-out obligation**.

This is not an erasure mechanism in the Flash sense. Reassigning the frame ends that embodiment's residency; it does not establish that every lower-level trace has been physically erased.

## Time

The case exposes several different timescales:

- the lifetime of one virtual-page designation;
- the interval during which that page occupies one real page frame;
- the interval between a page becoming changed and the later event that forces page-out;
- page-fault recovery time when a nonresident page is demanded;
- longer-lived ASM/page-data-set location bookkeeping while the page is backed externally.

There is no justified inference that an external paging copy constitutes a durable historical record across arbitrary system failures.

## Maintenance and labor

Persistence of the virtual page as an operational object depends on work spread across hardware and OS layers:

- page-table translation/residency state;
- reference/change recording used by replacement policy;
- page-frame selection and replenishment;
- conditional page-out before frame reuse;
- page-in after a fault;
- RSM frame accounting;
- ASM paging I/O and auxiliary-location bookkeeping;
- external page-storage capacity;
- page fixing for states that cannot tolerate ordinary replacement.

The user-level illusion of a large stable address space is therefore not evidence that embodiment and maintenance disappeared.

## Failure / forgetting modes

Keep the following distinct:

- loss/corruption of the only current page contents;
- reusing a changed real frame before its newer contents are propagated when required;
- stale or incorrect residency/translation state;
- stale or lost auxiliary-location metadata for a nonresident current page;
- unavailable or exhausted external page-storage capacity;
- a page fault that cannot complete page-in;
- incorrectly treating a required fixed/resident page as freely replaceable;
- ordinary frame reassignment of an unchanged page **when a valid external copy already exists**, which is specifically *not* forgetting under the bounded IBM mechanism.

## Engineering reconstruction

### Virtual-page identity is not page-frame identity or backing-slot identity

A page can be in one real frame, later absent from real storage, then paged back into real storage. The 1976 ASM can dynamically allocate external slots when pages are moved out. The current virtual page therefore cannot be identified with one permanent real frame or one inherent backing-slot identity.

This is a project-level reconstruction from IBM's page/frame/slot distinctions, not IBM philosophical vocabulary.

### Residency is not currentness

The page table's resident/nonresident relation answers **where ordinary service can currently resolve the page**. The change-state relation answers a different question: **whether the real copy has become newer than the extant external copy and therefore must be propagated before the real frame is reused**.

Thus:

> **residency ≠ currentness**.

A page can be resident and unchanged relative to its backing copy; it can also be resident and changed, making the real embodiment the source that must be retained before displacement.

### Frame reassignment is not forgetting

IBM's explicit unchanged-page case provides a strong counterexample. If an external copy already exists and the real page has not changed, the real frame can be made available without writing the page out again.

The real embodiment ceases to be retained, yet the virtual page remains recoverable as the current operational state.

### Conditional writeback exposes version relation

The changed/unchanged distinction is not merely a performance hint. In the documented replacement path it determines whether frame reuse is safe without first creating/updating an external copy.

The retention obligation is therefore relational:

> **page-out is required when the soon-to-be-discarded real embodiment contains current information not already represented by the usable external copy**.

`Current information` is analytical vocabulary here; IBM's historical control is the documented change-state relation.

### Nonresidency is not loss

A page fault is specifically a reference to a page marked not in real storage. The system can recover it through page-in. Nonresidency therefore denotes a service-location condition, not by itself loss or forgetting.

Yet nonresidency is also not identical to immediate availability: fault handling and page-in must succeed before ordinary execution resumes.

### External page storage is not archival persistence

The sources describe a working virtual-storage subsystem whose external page storage backs pages that are not currently resident. They do **not** establish that this backing copy is an application durability promise across OS crashes, machine failure, reboot, or administrative reuse.

Therefore:

> **backing-store retention ≠ crash-durable application retention**.

## Prior art and anti-anachronism

This case makes **no claim that IBM invented virtual memory, paging, or automatic transfer between fast and backing stores**.

Kilburn, Edwards, Lanigan, and Sumner's 1962 paper on the Manchester Atlas describes an automatic `one-level storage system` combining fast core storage and drum storage. Its period mechanism uses pages/page-address registers, a `not equivalence` condition that interrupts to the transfer routine, a directory updated on transfers, and automatic movement between core and drum. That is sufficient to block a novelty story for IBM's 1972 paging mechanism.

The Atlas evidence is used only as prior-art control. This case does not infer an IBM design genealogy from Atlas without a separate historical source.

Likewise, `dirty page`, `backing-copy currentness`, `authority`, and `embodiment` are modern analytical terms where used. IBM's own period terms remain visible alongside them.

## Functional analogy and philosophical limit

### Model 85 cache

Both cache replacement and paging can remove a faster in-memory embodiment while preserving a higher-level designation. But Case 08's bounded Model 85 store policy keeps main storage authoritative on every store. In Case 22, by contrast, a changed real page can be newer than the extant external copy and must be moved out before that frame is safely reusable.

So:

> **discardable derivative copy ≠ conditionally authoritative current embodiment**.

### Mapped Flash and HDD defect reassignment

Mapped Flash relocates due erase/rewrite geometry and controller policy; SCSI defect reassignment relocates because a physical sector has failed or become defective; OS/VS2 page replacement reallocates scarce real frames under residency/capacity pressure. Stable designation across changed embodiment is the useful analogy. The triggers and mechanisms are not genealogically identical.

### Philosophical limit

The case sharpens a general question about identity: a technically retained object can remain `the same` while the system relinquishes one physical embodiment, provided another current embodiment plus the relations needed to recover it survive.

That does not establish a metaphysics of immaterial information. The virtual page remains dependent on real frames, external page storage, translation/location state, controller/software behavior, and recoverable bytes.

## Cross-case result

The bounded paging relation can be written as:

```text
virtual designation
    !=
real-frame residency
    !=
external backing location
    !=
currentness of the resident copy relative to the backing copy
    !=
need to page out before frame reuse
    !=
immediate service availability
    !=
crash-durable persistence
```

This adds a new retention regime to the repository: **workload/capacity-triggered embodiment replacement in which the need to preserve before replacement is conditional on a currentness relation between copies**.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| IBM OS/VS2 distinguishes virtual pages, real page frames, external page storage, page-in, page-out, page faults, and page tables | H/P | IBM `GC28-0600-1`, July 1972, explanatory text and glossary |
| Replacement selection uses change/reference state | H/P | IBM `GC28-0600-1`, printed p. 32 |
| A changed selected page is moved to external page storage before frame reuse | H/P | IBM `GC28-0600-1`, printed p. 32 |
| An unchanged selected page need not be moved when an external copy already exists | H/P | IBM `GC28-0600-1`, printed p. 32 |
| RSM assigns/repossesses frames and ASM tracks auxiliary locations and paging I/O | H/P | IBM `SY28-0761-0`, July 1976, printed pp. 42–43 |
| ASM page data sets use 4096-byte slots allocated when a page must move out | H/P | IBM `SY28-0761-0`, printed p. 48 |
| Virtual-page identity is not identical to one page frame or one backing slot | E | bounded reconstruction from IBM page/frame/slot separation |
| Residency and currentness are distinct relations | E | bounded reconstruction from resident state + change-conditioned page-out |
| Frame reassignment of an unchanged page can preserve current virtual-page retention | E | directly constrained by IBM's no-page-out-if-copy-exists rule |
| External page storage is a crash-durable application record | X | not established by the bounded IBM paging sources |
| IBM invented virtual memory/paging | X | blocked by primary Atlas one-level-store evidence from 1962 |
| Paging is historically the same mechanism as cache eviction, FTL relocation, or disk defect reassignment | X/A | comparison is functional only; triggers and mechanisms differ |

## Related repositories

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `paging`, `virtual storage`, and dirty-page/backing-store combinations did not find a dedicated case. If a broad Atlas→System/360/370→Unix virtual-memory history is later developed, its engineering chronology belongs there; this repository should retain only the retention-specific comparison.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) remains the anti-anachronism guard. Modern vocabulary such as `dirty page`, `authoritative copy`, `working-set policy`, or later Unix VM taxonomy must not be projected into IBM's 1972 documentation without period evidence.

## Sources

1. IBM, _OS/VS2 Planning Guide_, form `GC28-0600-1`, First Edition, July 1972, especially printed pp. 8–11 (virtual/real/external page-storage relation), p. 32 (page-out/page-in and change/reference-conditioned frame reuse), pp. 57–58 (external-page-storage backing capacity), and p. 94 (page/page frame/page fault/page table/page-in/page-out glossary). Preserved scan: <https://bitsavers.org/pdf/ibm/370/OS_VS2/Release_1_1972/GC28-0600-1_OS_VS2_Planning_Guide_Jul72.pdf>.
2. IBM, _OS/VS2 System Logic Library, Volume 1_, VS2 Release 3.7, form `SY28-0761-0`, First Edition, July 1976, especially printed pp. 42–43 (RSM/ASM, real-frame assignment and auxiliary-location tracking) and p. 48 (page data sets, 4096-byte slots, dynamic slot allocation). Preserved scan: <https://www.bitsavers.org/pdf/ibm/370/OS_VS2/PLM/SY28-0761-0_OS_VS2_System_Logic_Library_Vol_1_Rel_3.7_Jul76.pdf>.
3. T. Kilburn, D. B. G. Edwards, M. J. Lanigan, and F. H. Sumner, "One-Level Storage System," _IRE Transactions on Electronic Computers_ EC-11(2), April 1962, pp. 223–235, DOI `10.1109/TEC.1962.5219356`. Accessible author/institutional reprint: <https://www.dcs.gla.ac.uk/~wpc/grcs/kilburn.pdf>.
