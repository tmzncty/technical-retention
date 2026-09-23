# Case 03 deepening — Micron 1993 self-refresh handoff as an earlier named-product primary witness

## Scope

This slice asks one narrow question left open by the Case 03 evidence index:

> Can a named DRAM product be grounded earlier than the existing 1996–1997 Hitachi witness as a primary-document example in which refresh cadence is handed from the external system to the DRAM and then handed back under explicit exit-side coverage rules?

The answer is **yes, at the level of named-product manufacturer documentation**. Micron Semiconductor's *1993 Specialty DRAM Data Book* documents the `MT4C8512/3 S` 512K × 8 Wide DRAM with SELF REFRESH, internal clocking during sleep mode, an internal refresh counter/controller for row-address control, and explicit exit-side requirements that depend on the system's external refresh regime.

The source is marked **ADVANCE**, and Micron's own 1993 data-book preface defines `Advance` as an initial description of products still under development. Therefore this slice does **not** turn the document into proof of production shipment, commercial deployment, invention priority, or first-product status.

Case 03 remains `grounded`.

---

## Why this is retention-specific

The useful relation is not merely that an old DRAM datasheet contains the words `SELF REFRESH`.

The source exposes a maintenance-authority transition:

```text
external refresh regime
    -> qualified self-refresh entry
    -> DRAM-internal refresh cadence + row traversal
    -> qualified self-refresh exit
    -> external refresh regime re-established
```

The transition is not semantically free. Micron distinguishes what the system may do after exit according to the external refresh strategy that will resume.

That makes the source useful for the repository's central separation:

```text
payload retained
    !=
maintenance regime current
    !=
maintenance coverage correctly handed off
    !=
foreground service immediately admissible
```

---

## Source custody and status

### Primary source

Micron Semiconductor, Inc., *1993 Specialty DRAM Data Book*.

Archival scan:

- https://www.bitsavers.org/components/micron/_dataBooks/1993_Micron_Specialty_DRAM_Data_Book.pdf

The indexed scan identifies itself in the preface as the **1993 Specialty DRAM Data Book** and explains the data-sheet status labels:

- `Advance` — initial descriptions of products still under development;
- `Preliminary` — initial characterization limits subject to change;
- no marking — production-device limits over the specified range.

The relevant `MT4C8512/3 S` pages are marked `ADVANCE`, `REV. 3/93`, ©1993 Micron Semiconductor, Inc.

Useful printed-page anchors in the scan:

- `1-34` — functional block diagram;
- `1-35` — pin descriptions;
- `1-36` — functional description, self-refresh entry/exit and refresh handoff;
- `1-38` — truth table including `SELF REFRESH`.

### Inspection boundary

The archival PDF is web-indexed and the extracted text preserves the printed page labels and revision marking, but the browser fetch path used in this research slice did not render the Bitsavers PDF pages directly. Claims below are therefore tied conservatively to the indexed primary-document text and printed-page anchors rather than described as a fresh visual facsimile inspection.

This is still stronger than using a later textbook or third-party summary, but a future page-image custody pass would be useful if exact typography or timing-diagram geometry becomes important.

---

## Historical record

### H/P — the 1993 data book is manufacturer documentation with explicit document-status semantics

Micron's preface says that the *1993 Specialty DRAM Data Book* contains specifications for specialty and derivative products based on its DRAM process. It also defines the status labels used on individual data sheets.

That matters because the relevant part is not silently promoted into a shipping-product witness.

The correct historical statement is:

> By March 1993, Micron manufacturer documentation for the named `MT4C8512/3 S` described a SELF REFRESH design and its handoff semantics; the data sheet itself was marked `ADVANCE`.

Do **not** rewrite this as:

> Micron was shipping the first commercial self-refresh DRAM in March 1993.

The source does not establish that claim.

Primary anchor: Micron 1993 Specialty DRAM Data Book, preface `v`, and `MT4C8512/3 S`, Rev. 3/93.

### H/P — ordinary retention and CBR already use a refresh counter/controller

The `MT4C8512/3 S` functional description says memory data remains correct by maintaining power and ensuring all 1,024 RAS-address combinations are exercised within the specified refresh interval.

It further states that a CBR refresh cycle invokes the **refresh counter and controller for row-address control**.

This establishes a named-device control relation:

```text
external CBR timing event
    -> internal row-address generation / progression
```

That is not yet autonomous self-refresh. External control still initiates the CBR event.

So the older Case 03 distinction remains valid here:

```text
on-chip refresh-address coverage state
    !=
on-chip autonomous cadence
```

The same product documentation then adds SELF REFRESH as the separate case in which cadence moves inward.

Primary anchor: Micron 1993 Specialty DRAM Data Book, `MT4C8512/3 S`, printed p. `1-36`.

### H/P — SELF REFRESH moves clocking for maintenance inside the DRAM

Micron describes battery-backup refresh as a CBR refresh performed at an extended refresh rate with low-current conditions.

It then distinguishes SELF REFRESH by saying that the DRAM provides its **own internal clocking during sleep mode**, so an external clock is not required.

That is the critical historical witness for the cadence handoff.

The bounded control decomposition is:

```text
CBR refresh:
external timing / command
    + internal refresh counter/controller

SELF REFRESH:
qualified entry
    + internal clocking
    + internal row-refresh progression
```

This is an earlier named-product primary-document witness than the Case 03 Hitachi 1996–1997 slice.

It is not evidence that Micron invented self-refresh, that no earlier device implemented it, or that the product had reached production shipment.

Primary anchor: Micron 1993 Specialty DRAM Data Book, `MT4C8512/3 S`, printed p. `1-36`.

### H/P — entry is a protocol transition, not an ambient mode

Micron says SELF REFRESH is initiated by executing a CBR REFRESH cycle and then holding RAS and CAS low for a specified time. The data sheet gives `tRASS` as 100 µs minimum and calls that value an `industry standard`.

The historical vocabulary should be preserved exactly:

- `CBR REFRESH`;
- `SELF REFRESH`;
- `tRASS`;
- `industry standard`.

The last phrase is a vendor statement in a 1993 data book. It is **not** by itself a JEDEC adoption chronology and should not be promoted into one.

The retention implication is limited but important:

```text
self-refresh-capable device
    !=
device currently in self-refresh
```

A qualified command/timing sequence establishes the regime.

Primary anchor: Micron 1993 Specialty DRAM Data Book, `MT4C8512/3 S`, printed p. `1-36`.

### H/P — exit is conditioned by the refresh regime that resumes

Micron says SELF REFRESH is terminated by taking RAS high for a minimum interval (`tRPS`).

The source then distinguishes two exit cases.

#### Case A — external system resumes distributed CBR refresh

Micron says normal accesses may begin immediately if the system uses distributed CBR refresh as its normal refresh method.

But the transition is not obligation-free: the first external CBR pulse must occur within the external refresh-rate timing envelope, and the data sheet gives a bounded upper relation in terms of external refresh-rate periods.

Micron explains the immediate-access allowance by stating that it uses a **distributed CBR SELF REFRESH scheme internally**.

#### Case B — external system does not resume distributed CBR refresh

Micron instead requires a refresh of all rows before ordinary use when the controller relies on another standard refresh pattern such as burst/RAS-only behavior.

The key historical relation is therefore:

```text
same retained payload
    + same self-refresh mode exit
    + different resuming external refresh regime
    -> different handoff work before normal service
```

This is stronger than the generic statement `self refresh keeps data` because it exposes the transition contract between two maintenance regimes.

Primary anchor: Micron 1993 Specialty DRAM Data Book, `MT4C8512/3 S`, printed p. `1-36`.

### H/P — Micron itself warns that other manufacturers may impose different exit behavior

The data sheet says Micron devices permit immediate access after exit under the distributed-CBR condition, while other manufacturers' devices may require a full burst regardless of external refresh type. Micron therefore recommends that a controller designer may choose the conservative burst strategy to avoid compatibility problems.

This is useful negative evidence against universalizing one vendor's handoff semantics:

```text
SELF REFRESH as a broad functional class
    !=
one universal exit protocol across vendors
```

It also means that a system controller cannot infer every transition-side obligation merely from the existence of a `SELF REFRESH` capability label.

Primary anchor: Micron 1993 Specialty DRAM Data Book, `MT4C8512/3 S`, printed p. `1-36`.

---

## Engineering reconstruction

The following terms are project reconstruction, not Micron's historical vocabulary.

### 1. Maintenance authority is decomposable

The named device supports at least three distinct control dimensions:

```text
refresh cadence authority
refresh-address / coverage progression
maintenance-regime membership
```

During ordinary CBR refresh, cadence remains external while address progression is internal.

During SELF REFRESH, both cadence generation and row-refresh progression are internal for the duration of the mode.

Thus:

```text
maintenance is internal
    !=
all maintenance-control dimensions were always internal
```

### 2. Handoff correctness includes residual coverage/deadline obligations

The source's exit rules imply that leaving self-refresh does not erase the refresh obligation merely because the logical payload is currently readable.

The system must re-enter an external regime in a way that preserves whole-array deadline/coverage correctness.

A useful project reconstruction is:

```text
mode exit
    !=
maintenance debt erased
```

and:

```text
foreground access may become admissible
    while
refresh-handoff deadline still constrains the next maintenance action
```

That relation is especially visible in Micron's distributed-CBR exit case.

### 3. A capability bit/part suffix is not the retained state

The `S` product option identifies a product supporting SELF REFRESH, but the retained payload during a particular interval depends on:

- maintained power;
- correct entry;
- internal self-refresh operation;
- correct exit;
- timely resumption of the next refresh regime.

So:

```text
feature availability
    !=
feature activation
    !=
maintenance execution
    !=
coverage correctness
    !=
payload retention guarantee under arbitrary misuse
```

### 4. Controller compatibility is part of retention correctness

Micron's cross-vendor warning makes a system-level point visible: a controller can be electrically capable of issuing self-refresh commands while still being too optimistic about exit semantics for a different vendor's device.

In retention terms:

```text
compatible command vocabulary
    !=
compatible maintenance-transition contract
```

This is a system-integration relation, not a claim that 1993 designers used the project's vocabulary.

---

## Functional analogy

A bounded functional comparison can be made with two other Case 03 slices.

### Against external refresh controllers

Intel 8202A/8203 evidence shows timer/counter/arbitration state external to the payload device.

Micron 1993 SELF REFRESH instead places cadence generation inside the DRAM during the sleep interval.

Functional comparison only:

```text
external maintenance controller
    <->
mode-bounded internal maintenance controller
```

This does not establish a direct Intel-to-Micron genealogy.

### Against Hitachi 1996–1997 self-refresh handoff

Both primary witnesses show that self-refresh entry/exit has transition-side coverage obligations.

But their exact controller-facing rules should not be merged into one timeless protocol. Micron's 1993 data sheet explicitly conditions post-exit behavior on the external refresh strategy and even warns about other manufacturers.

That makes the cross-vendor difference itself evidence-bearing.

---

## Philosophical interpretation

A very narrow interpretation is justified:

> During self-refresh, the logical memory state appears quiescent to the surrounding system only because responsibility for recurrence has moved behind the interface.

The important point is not that the state becomes maintenance-free. The apparatus changes **where the maintenance obligation is enacted** and **who must resume it afterward**.

This is a technical example of persistence through delegated maintenance, not evidence for a universal philosophy of memory.

---

## Explicit non-claims

This slice does **not** establish any of the following:

1. that `MT4C8512/3 S` was in production shipment in March 1993;
2. that it was the first Micron self-refresh DRAM;
3. that it was the first commercial self-refresh DRAM;
4. that Micron invented DRAM self-refresh;
5. that the phrase `industry standard` proves a particular JEDEC ballot or revision date;
6. that the internal self-refresh oscillator architecture is known from this data sheet;
7. that the exact timer circuit is known;
8. that the exact counter implementation is known beyond the documented refresh counter/controller function;
9. that all manufacturers used distributed CBR self-refresh internally;
10. that all manufacturers allowed immediate post-exit access;
11. that a payload read immediately after exit proves whole-array refresh coverage is safe;
12. that maintained VCC alone is sufficient for retention;
13. that SELF REFRESH survives power loss;
14. that self-refresh mode state is nonvolatile;
15. that internal refresh phase/counter state survives reset;
16. that the source establishes fault behavior for malformed entry or exit waveforms;
17. that the source establishes temperature limits beyond the documented part conditions;
18. that the source is a JEDEC standard;
19. that the Micron and Hitachi designs share circuitry or direct lineage;
20. that an archived OCR/index extraction substitutes for page-image inspection when diagram geometry becomes material.

---

## What this closes

This slice substantially closes the current Case 03 evidence-index item:

> Earlier named-product self-refresh witness with directly inspectable primary documentation.

with one qualification:

> it closes the **earlier named-product manufacturer-document floor**, not an earlier **production/shipment** floor, because Micron marks the data sheet `ADVANCE`.

It also strengthens, but does not fully close, the item:

> Named-product internal timer/counter architecture rather than patent-only architecture.

The source directly establishes internal clocking and a refresh counter/controller role, but it does not expose enough circuit detail to claim an exact timer/counter architecture.

---

## Remaining high-value debt

The next useful work is narrower now:

1. find an earlier or contemporary **production-status / shipping** self-refresh DRAM primary document;
2. find a named product whose primary source exposes the internal self-refresh timer/oscillator and row counter more explicitly;
3. recover JEDEC self-refresh revision chronology from standards records rather than vendor `industry standard` wording;
4. find board/controller documentation that implements the controller-side entry/exit handoff rules against a named DRAM;
5. perform or locate fault injection around malformed entry, interrupted self-refresh, and missed exit-side coverage deadlines.

Do not expand this into a general 1990s DRAM market history.

---

## Related-repository boundary

Fresh searches of `tmzncty/computing-archaeology` for `MT4C8512` and `self refresh DRAM` found no dedicated reusable packet.

Keep here:

- maintenance-authority transfer;
- entry/exit handoff obligations;
- distinction between internal row progression and internal cadence;
- evidence-status distinction between named documentation and production shipment.

Route primarily to `computing-archaeology`:

- Micron product-family genealogy;
- semiconductor process history;
- 1990s DRAM market chronology;
- first-shipment / pricing / vendor-competition history;
- detailed oscillator/counter circuit genealogy beyond what is needed for the retention argument.

---

## Source list

### Primary

- Micron Semiconductor, Inc., *1993 Specialty DRAM Data Book*, preface `v`, and `MT4C8512/3 S`, Rev. 3/93, printed pp. `1-34`–`1-38`. Archival scan: https://www.bitsavers.org/components/micron/_dataBooks/1993_Micron_Specialty_DRAM_Data_Book.pdf

### Existing repository context

- [`03-dram-refresh-evidence-index.md`](03-dram-refresh-evidence-index.md)
- [`03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md`](03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md)
- [`03-hitachi-1996-1997-self-refresh-mode-handoff-deepening.md`](03-hitachi-1996-1997-self-refresh-mode-handoff-deepening.md)
- [`../cases/03-dram-refresh-as-scheduled-restoration.md`](../cases/03-dram-refresh-as-scheduled-restoration.md)
