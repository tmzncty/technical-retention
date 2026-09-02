# Evidence Record 22 — IBM OS/VS2 Paging, 1972–1976

## Decision

**Promotion decision: `grounded`.**

The bounded claim is not `IBM invented virtual memory`. The claim is that period IBM OS/VS2 documentation directly supports a retention-specific decomposition among virtual-page identity, real-frame residency, external-page-storage location, change/currentness state, conditional page-out, and page-fault recovery.

Case: [`../cases/22-ibm-system370-paging-backing-copy-currentness.md`](../cases/22-ibm-system370-paging-backing-copy-currentness.md).

## Scope of grounding

The evidence set supports only this bounded mechanism:

```text
virtual page
    ↓
resident? + current real-frame mapping
    ↓
real frame
    ↓ selected for reuse
changed relative to extant external copy?
    ├── yes → page-out before frame release
    └── no + copy already exists → no page-out required

later nonresident reference
    → page fault
    → page-in
    → ordinary service resumes
```

The 1976 RSM/ASM implementation material adds auxiliary-storage location bookkeeping and dynamically allocated page-data-set slots.

Out of scope:

- complete Atlas→IBM virtual-memory genealogy;
- segmentation, DAT hardware, TLB design, working-set policy, or performance history except where needed to identify the retention relation;
- Unix swap, copy-on-write, demand-zero, memory-mapped files, or later VM semantics;
- application/process crash durability;
- any claim that external page storage is archival storage;
- any equation of paging with cache, FTL, or disk defect remapping.

## Primary source A — IBM OS/VS2 Planning Guide, July 1972

### Bibliographic identity

IBM, _OS/VS2 Planning Guide_, form `GC28-0600-1`, First Edition, July 1972.

Preserved scan:
<https://bitsavers.org/pdf/ibm/370/OS_VS2/Release_1_1972/GC28-0600-1_OS_VS2_Planning_Guide_Jul72.pdf>

The directly inspected PDF text identifies the edition as July 1972.

### Printed pp. 8–11 — virtual, real, and external page storage

The guide explains the relationship among virtual storage, real storage, and external page storage, including the fact that only the pages currently required for execution need occupy real storage while other virtual pages can be represented externally.

Evidence use:

- `virtual page` cannot be reduced to `currently occupied real frame`;
- external page storage is part of the working virtual-storage hierarchy.

### Printed p. 32 — page-out/page-in and the conditional writeback rule

This is the central source location for the case.

IBM says that when the supply of available page frames is low, paging routines select page frames for reassignment, primarily using `change` and `reference` bits.

The mechanism then branches:

- if the selected page **has changed**, it is moved to external page storage before the page frame is made available;
- if the page **has not changed**, it is not moved when a copy already exists in external page storage.

The same section describes page-out as real→external transfer and page-in as external→real transfer, and describes the paging supervisor as recognizing transfer requirements, selecting frames, replenishing the free-frame supply, saving pages changed in real storage, and recognizing pages that cannot be transferred.

Evidence use:

- changed-state/currentness influences whether preservation work is required before embodiment reuse;
- page-frame reassignment is not itself identical to page-out;
- loss of one real embodiment need not be forgetting when a usable external current copy already exists.

### Printed p. 57 — external-page-storage backing capacity

IBM describes external page storage as backing virtual pages and discusses the amount of backing required for address spaces/regions.

Evidence use:

- backing capacity is finite infrastructure, not metaphysical `virtual space` detached from hardware;
- this source is not used to claim archival durability.

### Printed p. 94 — period definitions

The glossary directly defines or describes:

- `page` — a fixed-length block transferable between real storage and external page storage;
- `page frame` — the real-storage block that can contain a page;
- `page fault` — a reference to a page marked not in real storage;
- `page fixing` — marking a page nonpageable so it remains in real storage;
- `page-in` and `page-out`;
- `page table` — indicates whether a page is in real storage and correlates virtual and real addresses;
- `paging` and `paging supervisor`.

Evidence use:

- historical vocabulary;
- virtual-page / real-frame distinction;
- nonresidency / fault / recovery distinction;
- fixed pages as a counterexample to `all physical residency is disposable`.

### Facsimile boundary

The PDF text layer was directly inspected at the source locations above. Attempts to render page screenshots for the key p. 32 and glossary p. 94 locations returned archive/cache failures in the research environment. Therefore this record makes **no visual-layout, figure, typography, or marginalia claim** from those pages. The text itself remains directly source-controlled by the PDF extraction.

## Primary source B — IBM OS/VS2 System Logic Library, July 1976

### Bibliographic identity

IBM, _OS/VS2 System Logic Library, Volume 1_, VS2 Release 3.7, form `SY28-0761-0`, First Edition, July 1976.

Preserved scan:
<https://www.bitsavers.org/pdf/ibm/370/OS_VS2/PLM/SY28-0761-0_OS_VS2_System_Logic_Library_Vol_1_Rel_3.7_Jul76.pdf>

### Printed pp. 42–43 — RSM and ASM

The directly inspected text describes Real Storage Management (RSM) as:

- administering real storage;
- directing movement of virtual pages between auxiliary and real storage in 4096-byte blocks;
- assigning page frames and associating virtual and real addresses;
- repossessing frames when storage is needed;
- treating pages as pageable unless fixed/resident for bounded system reasons.

It describes Auxiliary Storage Management (ASM) as performing paging I/O and keeping track of auxiliary-storage locations for virtual pages.

Evidence use:

- current page recovery depends on control/location state in addition to payload;
- the virtual→real relation and the external-location relation are separate maintained relations.

### Printed p. 48 — page data sets and slots

The text says page data sets form the page-space portion of auxiliary storage, store pageable virtual-page contents, and are formatted into 4096-byte records called `slots`. A slot is allocated dynamically whenever a page must be moved out of real storage.

Evidence use:

- external backing is concretely organized and allocated;
- `virtual page` is not synonymous with one permanent auxiliary slot;
- auxiliary capacity and allocation machinery are retention infrastructure.

### Facsimile boundary

The p. 48 text layer was directly inspected. A screenshot/render attempt was rejected by the archive endpoint (HTTP 403 in the research environment), so no visual-layout claim is made from that page.

## Prior-art control — Manchester Atlas, 1962

T. Kilburn, D. B. G. Edwards, M. J. Lanigan, and F. H. Sumner, "One-Level Storage System," _IRE Transactions on Electronic Computers_ EC-11(2), April 1962, pp. 223–235, DOI `10.1109/TEC.1962.5219356`.

Accessible reprint:
<https://www.dcs.gla.ac.uk/~wpc/grcs/kilburn.pdf>

The paper was directly inspected both as text and as rendered page images for the relevant pages.

It describes an automatic one-level storage system combining fast core storage and drum storage. The period design uses pages/page-address registers, a `not equivalence` condition that invokes a transfer routine, a directory updated on transfers, and automatic transfers that can free a core block and bring the demanded block from drum.

Evidence use:

- blocks any claim that IBM's 1972 OS/VS2 material marks the invention of paging/automatic hierarchy transfer;
- supplies prior-art chronology only;
- does **not** prove direct genealogy from Atlas to IBM OS/VS2.

## Related-repository check

Searches in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for:

- `paging`;
- `virtual storage`;
- `virtual memory paging dirty page backing store`;

returned no dedicated case on the current default branch during this research slice.

Accordingly, the retention-specific IBM case is not duplicating an existing technical-history treatment. A broader virtual-memory engineering chronology should still be routed to `computing-archaeology` if developed.

## Claim-by-claim grounding

| Claim | Type | Primary anchor | Strength / limit |
| --- | --- | --- | --- |
| OS/VS2 distinguishes page, page frame, external page storage, page-in, page-out, page fault, and page table | H/P | `GC28-0600-1`, pp. 8–11, 32, 94 | direct IBM period text |
| Replacement selection uses change/reference state | H/P | `GC28-0600-1`, p. 32 | direct IBM period text |
| Changed selected page is moved to external page storage before frame reuse | H/P | `GC28-0600-1`, p. 32 | central directly inspected text claim |
| Unchanged selected page need not be moved if an external copy already exists | H/P | `GC28-0600-1`, p. 32 | central directly inspected text claim |
| Page fault identifies demand for a page marked nonresident | H/P | `GC28-0600-1`, p. 94 | direct IBM glossary |
| Some pages may be fixed/nonpageable | H/P | `GC28-0600-1`, p. 94; `SY28-0761-0`, pp. 42–43 | direct IBM period text |
| RSM assigns/repossesses frames and ASM tracks auxiliary locations | H/P | `SY28-0761-0`, pp. 42–43 | direct IBM period text |
| Page data sets contain dynamically allocated 4096-byte slots | H/P | `SY28-0761-0`, p. 48 | direct IBM period text |
| Virtual-page identity ≠ frame identity ≠ slot identity | E | synthesis of IBM page/frame/slot distinctions | project reconstruction, not IBM wording |
| Residency ≠ currentness | E | resident relation + p. 32 changed/unchanged branch | project reconstruction constrained by primary source |
| Frame reassignment ≠ forgetting | E | p. 32 unchanged-page/no-page-out branch | strong bounded inference |
| Page-out obligation is conditional on currentness/copy relation | E | p. 32 changed/unchanged branch | `currentness` is analytical vocabulary |
| External page storage = crash-durable application record | X | no supporting source | explicitly rejected |
| IBM invented paging/virtual memory | X | Atlas 1962 primary paper | explicitly rejected |
| Paging = cache / FTL / defect remap | A/X | Cases 08/04/14 comparison | functional analogy only |

## Why `grounded`, not `first-pass`

The case satisfies the repository's grounding gates:

- strong period-primary IBM documentation exists for the central mechanism;
- exact printed locations are recorded;
- historical terms remain visible;
- the mechanism is described below the user-facing `virtual memory` metaphor;
- failure/forgetting modes are separated;
- modern `dirty/current/authority` language is labeled analytical rather than historical;
- Atlas 1962 supplies a direct primary prior-art control;
- a fixed/nonpageable-page counterexample limits the strongest abstraction claim;
- `computing-archaeology` duplication was checked;
- screenshot failures are recorded rather than silently treated as visual inspection.

## Promotion result

The bounded IBM OS/VS2 paging slice can therefore support these project-level distinctions:

> **virtual-page identity ≠ page-frame identity ≠ backing-location identity**

> **residency ≠ currentness**

> **frame reassignment ≠ forgetting**

> **page replacement ≠ unconditional page-out**

> **nonresidency ≠ loss, but recovery work may be required before service**

> **working backing storage ≠ crash-durable archival persistence**

These claims should remain bounded to the documented paging regime unless separately established for another virtual-memory system.
