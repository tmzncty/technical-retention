# Case 77 deepening — Data General 1985 sniff maintenance versus failed-page exclusion

## Status

**`bounded deepening complete`**

Canonical case: [`../cases/77-data-general-dram-sniff-refresh-ecc-scrub.md`](../cases/77-data-general-dram-sniff-refresh-ecc-scrub.md)

This evidence pass closes one narrow open question from Case 77:

> How can periodic correction/scrubbing coexist with memory that has already crossed from `correctable error` into `failed carrier that should no longer participate in maintenance coverage`?

The central primary witness is Data General's US4908749A, filed **15 November 1985** and granted **13 March 1990**, together with its international patent-family text. The patent is formally about a system-bus protocol, but its preferred embodiment exposes a memory-controller control path in which `SNIFF`, ordinary error correction, and a `PAGEINH` signal for failed memory pages coexist.

This is a later Data General witness than US4380812A. It is used to deepen the **classification and coverage boundary** around `sniff`; it is **not** treated as proof that the 1985 preferred embodiment is the same circuit as the 1980-filed patent, nor as proof of deployment in a named shipping machine.

---

## Research boundary

### Included

- Data General's own 1985-filed patent-family description of a memory control unit;
- the explicit statement that `sniff` detects/corrects memory errors, including errors attributed in the document to alpha-particle hits;
- the explicit `PAGEINH` behavior for memory described as bad/failed/no longer in use;
- the statement that `REFRESH` and `SNIFF` can skip such a page;
- the distinction between transient/correctable-error maintenance and failed-page exclusion;
- a bounded comparison with Case 78's NAND bad-block exclusion semantics.

### Excluded

- identifying a specific commercial Data General system as the exact implementation;
- inferring the physical hard-failure mechanism of a page from `PAGEINH` alone;
- claiming that every error attributed to an alpha particle is transient;
- claiming that every Data General memory controller used this signal set;
- reconstructing the complete double-bit-error-correction algorithm;
- treating `page inhibit` as equivalent to modern OS page offlining, DRAM row sparing, NAND bad-block marking, or DDR5 post-package repair;
- asserting invention priority for memory sparing/offlining or scrub exclusion.

---

## Source identity and chronology

### H/P — Data General US4908749A patent family

**US publication:** US4908749A, *System for controlling access to computer bus having address phase and data phase by prolonging the generation of request signal*.

**Inventors:** Peter G. Marshall and Robert Feldstein.

**Original assignee:** Data General Corporation.

**US filing / priority:** **1985-11-15**.

**US grant:** **1990-03-13**.

Patent-family members include CA1273117A and JPS62163160A. The family text is useful because searchable copies expose the preferred-embodiment memory-controller details even though the claimed invention is primarily the bus protocol.

Primary / patent-family records:

- <https://patents.google.com/patent/JPS62163160A/en>
- <https://patents.google.com/patent/CA1273117A/en>
- <https://patents.justia.com/patent/4908749>

The chronology is later than Case 77's central Data General witness, US4380812A (filed 1980-04-25). This pass therefore establishes a **later same-manufacturer control boundary**, not a first occurrence.

---

## Historical record

### H/P — the 1985 preferred embodiment still uses `sniff`

The patent describes a memory control unit that monitors memory traffic, checks returned data, and can hold the system-bus transaction while corrected data are produced. Within the preferred embodiment it states that the memory control unit can generate the bus `FREZ` signal while it performs a `sniff operation`.

The text describes `sniff` as an operation used by the memory control unit to **detect and correct errors in memory locations**, and specifically gives errors from an **alpha particle hit** as the motivating example.

This establishes a later Data General usage floor for the term/mechanism family:

```text
1980-filed Data General US4380812A
    refresh-coupled `sniff` + corrective writeback

1985-filed Data General US4908749A family
    memory-controller `sniff` still present in preferred embodiment
```

The safe historical statement is only that Data General continued to document a controller-level `sniff` operation in a later patent embodiment. It does not prove unchanged implementation continuity across five years.

### H/P — the same embodiment separately recognizes failed memory

The later patent introduces a signal named `PAGEINH` (`page inhibit`). It says that this signal is issued by a memory module when **bad memory / memory that has failed** is being addressed.

The document then explains why the signal is useful: it avoids unnecessary operations on memory that is **no longer in use**.

Most importantly for Case 77, the patent explicitly names both recurring maintenance paths:

- `REFRESH` operations; and
- `SNIFF` operations;

and says that these operations, which would otherwise range across memory, can be warned by `PAGEINH` and **skip that page**.

This is direct period-primary evidence for a maintenance-coverage boundary.

### H/P — maintenance coverage is conditional on page admissibility

The document therefore does not describe the memory as one undifferentiated physical address space over which maintenance must always continue forever.

At least two operational classes appear in the preferred embodiment:

```text
page remains in use
    -> participates in ordinary memory service
    -> refresh/sniff remain meaningful maintenance

page is marked failed / no longer in use
    -> PAGEINH
    -> refresh/sniff may skip that page
```

This is not merely an optimization about scan speed. The patent's own rationale is to avoid performing unnecessary operations on memory that is no longer used.

### H/P — correctable-error service remains distinct from failed-page exclusion

Elsewhere in the same patent, the memory control unit checks data returned on the bus and can prolong the transaction while corrected data are generated. The description includes syndrome bits for error detection/correction and separately mentions more complicated double-bit-error-correction handling.

The page-inhibit path is different. It does not say `correct this word and write it back`; it says the addressed memory page has been classified as bad/failed/no longer in use and allows recurring `REFRESH` / `SNIFF` work to bypass it.

Therefore the source itself supports a categorical boundary:

> **correctable error path != failed-page exclusion path.**

---

## Engineering reconstruction

The following terms are project reconstructions, not Data General quotations.

### E — maintenance is defined over an admissible carrier set, not all physically present carriers

Case 77 previously emphasized `coverage`: recurring sniff work has to reach the protected words on the assumed interval.

The 1985 source adds a necessary qualifier. Coverage is not necessarily:

```text
visit every physically addressable location forever
```

It can instead be:

```text
visit every location that remains admitted to active memory service
```

Once a page has crossed into the source's failed/no-longer-used state, skipping it is not automatically a coverage bug. It can be the correct consequence of exclusion.

Therefore:

> **maintenance omission over an active page can be a fault; maintenance omission over an explicitly retired page can be policy.**

### E — correction cannot substitute indefinitely for carrier qualification

The earlier Case 77 mechanism shows how ECC correction plus later writeback can renew redundancy margin after a bounded correctable error.

The later `PAGEINH` witness shows the other side of that limit: a system can classify a page so that continuing normal refresh/sniff work is no longer the appropriate response.

This yields:

```text
correctable error
    -> recover / correct
    -> possibly write back
    -> continue maintenance coverage

failed carrier classification
    -> exclude page from use
    -> recurring refresh/sniff may skip it
```

Repeated rewrite is therefore not a universal repair for failed hardware.

### E — maintenance eligibility is itself retained control state

For a controller to skip a failed page deliberately rather than accidentally, some control relation must remain available that answers:

```text
is this page still part of the active maintenance/service set?
```

`PAGEINH` is the observed signal in the bounded embodiment. The patent does not fully establish where the persistent failure classification originates or how long it survives reset/power loss, so this evidence does **not** claim a complete retained bad-page table.

The narrower result is that the maintenance engine consumes a classification signal in addition to raw addressability.

### E — physical presence does not force maintenance authority

A failed page can remain electrically present in the machine while the memory controller is told not to treat it as an ordinary target for recurring maintenance.

Thus:

> **physical presence != service admissibility != maintenance eligibility.**

This is the DRAM/system-memory counterpart of a pattern seen elsewhere in the repository, while the specific mechanisms remain different.

---

## Functional comparison — not genealogy

### A — Case 78, NAND bad-block exclusion

Case 78 shows that a NAND block can remain electrically addressable while bad-block state says it must not be used for ordinary allocation. It also emphasizes that negative media-qualification state can be constitutive of continued storage service.

The Data General `PAGEINH` witness has a bounded functional resemblance:

```text
negative carrier qualification
    -> ordinary maintenance/allocation path changes
```

But the mechanisms are not the same:

- NAND Case 78 uses factory/runtime bad-block evidence, BBTs, and replacement blocks;
- Case 77's 1985 witness exposes a memory-module/controller `PAGEINH` signal and skip behavior for refresh/sniff;
- no shared genealogy is claimed;
- no claim is made that Data General's page classification was nonvolatile or used a flash-like table.

The useful comparison is only:

> **retention machinery can depend on remembering which physical carriers no longer count.**

### A — Case 45, DDR5 ODECC / ECS

Case 45's Error Check and Scrub is a later device-standard maintenance regime. The Data General witness remains a system/controller-level design and uses different vocabulary, timing, and exclusion mechanisms.

Do not translate `PAGEINH` into a DDR5 repair primitive or treat `sniff` as an early version of every later ECS implementation.

### A — Case 14, SCSI reassignment

Both can respond to a carrier becoming unsuitable by changing future treatment of that carrier. Case 14, however, is about logical-block continuity across disk-sector reassignment; the present slice does not establish a transparent replacement mapping for the excluded Data General page.

`skip failed page` and `reassign logical block` are therefore not interchangeable descriptions.

---

## Historical record versus reconstruction

### Historical record

The patent-family text supports these statements directly:

- a Data General preferred embodiment filed in 1985 contains a memory controller;
- that controller performs a `sniff operation` for detecting/correcting memory errors;
- an alpha-particle hit is named as an example error source;
- `PAGEINH` is issued when bad/failed memory is addressed;
- memory described as failed is no longer in use;
- recurring `REFRESH` and `SNIFF` operations can skip the inhibited page.

### Engineering reconstruction

The repository infers only bounded relations:

- active-set coverage differs from raw physical-address coverage;
- maintenance eligibility depends on carrier qualification;
- exclusion can be a correct maintenance outcome rather than a maintenance failure;
- a corrective path and a retirement/exclusion path are different policy classes.

### Functional analogy

Comparisons to NAND bad-block tables, SCSI reassignment, DDR5 ECS, or later page offlining are comparison tools only.

### Philosophical interpretation

A restrained project-level statement is possible:

> continuity may require not only recurring repair of what still counts, but also retained knowledge of what has ceased to count as a valid carrier.

No stronger philosophical equivalence follows from the engineering relation.

---

## Explicit non-claims

1. US4908749A does **not** prove the exact US4380812A circuit shipped unchanged.
2. This pass does **not** identify a named commercial Data General machine implementing the exact preferred embodiment.
3. `PAGEINH` is **not** assumed to be a nonvolatile bad-page table.
4. The source does **not** establish how a page first becomes classified as failed.
5. The source does **not** establish whether the classification survives a power cycle.
6. The source does **not** establish a transparent replacement mapping for the failed page.
7. An alpha-particle example does **not** prove every sniff-corrected error is an alpha-particle soft error.
8. A correctable syndrome does **not** prove the underlying carrier is permanently healthy.
9. A failed page does **not** mean every bit in that page is unreadable.
10. Skipping a failed page does **not** prove its physical cells stop leaking charge; it means the bounded system no longer treats that page as ordinary in-use memory for these maintenance operations.
11. `PAGEINH` is **not** equated with NAND bad-block markers, OS memory offlining, DDR row sparing, or post-package repair.
12. Data General is **not** claimed to have invented scrub exclusion or bad-memory sparing.
13. The 1985 filing date is a documented floor for this inspected embodiment, not an invention-priority date.
14. A patent preferred embodiment is not independent field-deployment evidence.
15. The bus-protocol patent's main claim scope should not be misrepresented as a patent specifically on memory scrubbing.

---

## Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| Data General documented a later controller-level `sniff` operation in a 1985-filed patent | H/P | grounded by US4908749A family |
| the patent describes sniff as detecting/correcting memory errors | H/P | grounded |
| the text names alpha-particle hits as an example source of sniff-targeted errors | H/P | grounded |
| `PAGEINH` identifies bad/failed memory in the preferred embodiment | H/P | grounded |
| `REFRESH` and `SNIFF` may skip a page identified through `PAGEINH` | H/P | grounded |
| correctable-error maintenance and failed-page exclusion are separate control paths | H/P/E | grounded by separate paths; relation is reconstruction |
| maintenance coverage can be defined over active/admissible memory rather than every physical page | E | bounded reconstruction |
| physical presence != service admissibility != maintenance eligibility | E | bounded reconstruction |
| PAGEINH survives reboot/power loss | X | not established |
| the embodiment transparently remaps failed pages | X | not established |
| US4908749A proves a named shipping product | X | not established |
| Data General invented memory scrubbing or memory offlining | X | not investigated / unsupported |

---

## Source ledger

### Primary / contemporary

1. Peter G. Marshall and Robert Feldstein / Data General Corporation, **US4908749A**, *System for controlling access to computer bus having address phase and data phase by prolonging the generation of request signal*, filed 15 Nov 1985, granted 13 Mar 1990. Searchable patent-family records:
   - <https://patents.google.com/patent/JPS62163160A/en>
   - <https://patents.google.com/patent/CA1273117A/en>
   - <https://patents.justia.com/patent/4908749>
2. Michael L. Ziegler II et al. / Data General Corporation, **US4380812A**, *Refresh and error detection and correction technique for a data processing system*, filed 25 Apr 1980, granted 19 Apr 1983: <https://patents.google.com/patent/US4380812A/en>.

### Repository context

- Canonical Case 77: [`../cases/77-data-general-dram-sniff-refresh-ecc-scrub.md`](../cases/77-data-general-dram-sniff-refresh-ecc-scrub.md)
- Case 78: [`../cases/78-micron-nand-bad-block-marker-management.md`](../cases/78-micron-nand-bad-block-marker-management.md)
- Case 45: [`../cases/45-ddr5-odecc-error-check-scrub.md`](../cases/45-ddr5-odecc-error-check-scrub.md)
- Case 14: [`../cases/14-scsi-disk-defect-reassignment-logical-identity.md`](../cases/14-scsi-disk-defect-reassignment-logical-identity.md)

A fresh `tmzncty/computing-archaeology` search for `Data General sniff memory ECC` found no directly reusable case, so this file keeps only the retention-specific classification/maintenance boundary rather than building a broad Data General architecture history.

---

## Remaining evidence debt

This pass closes the narrow question of whether Data General documented a later architecture in which sniff/refresh maintenance could explicitly skip memory already classified as failed.

Still open:

- identify a named shipping Data General machine/manual that exposes the same `PAGEINH` / sniff behavior;
- recover period service documentation showing how a page entered the failed/no-longer-used state;
- establish whether and where the page-failure classification was retained across restart/power loss;
- determine whether the preferred embodiment used replacement/spare memory after page exclusion;
- separate single-bit correction, the patent's mentioned double-bit-error-correction handling, and permanent hardware diagnosis with machine/service documentation;
- trace Data General's use of `sniff` after 1985 without assuming identical implementations.
