# Evidence 09 — 1972–1975 1103 refresh product-contract deepening

**Status:** `bounded deepening complete`

**Parent case:** [`../cases/09-dram-cbr-refresh-address-internalization.md`](../cases/09-dram-cbr-refresh-address-internalization.md)

**Adjacent records:**

- [`09-1973-1982-early-self-refresh-control-partitions-prior-art-deepening.md`](09-1973-1982-early-self-refresh-control-partitions-prior-art-deepening.md)
- [`09-gte-1971-1973-self-initiating-refresh-system-boundary-deepening.md`](09-gte-1971-1973-self-initiating-refresh-system-boundary-deepening.md)

**Bounded question:** can period product documentation independently corroborate the refresh geometry and deadline assumed by GTE's 1971-filed / 1973-published Intel-1103 refresh-controller example, and what boundary does that establish between a DRAM device's retention contract and the external apparatus that schedules and arbitrates maintenance?

This is intentionally **not** a general Intel 1103 history, a semiconductor-memory priority claim, a second-source genealogy, or a claim that GTE's exact controller was shipped with a particular Intel memory product. It closes a narrower evidence gap: the existing GTE patent gave a system-level refresh design and quoted the Intel 1103's required refresh geometry, but Case 09 did not yet have a directly inspected product-document witness for the same `32 read cycles / two milliseconds` contract.

---

## Result in one sentence

A 1972 Signetics MOS handbook documents its 1103 as a `1024 word by 1 bit` dynamic memory whose entire 1024-bit array is refreshed in **32 read cycles every two milliseconds**, while Intel's own 1975 data catalog independently gives the same **32-read-cycle / 2 ms** contract for the Intel 1103; this corroborates the product-side maintenance obligation used in GTE's earlier controller example while keeping the system's free-running clock, row counter, address gating, and `memory busy` arbitration distinct from the DRAM device contract.

A useful bounded decomposition is therefore:

```text
DRAM device contract
    finite refresh deadline
    + row-coverage geometry / restorative access primitive

external retention apparatus
    recurring cadence
    + coverage traversal state
    + refresh/service arbitration
    + address-source selection

meeting the first
    requires some implementation of the second

but
    device retention contract
        != one unique maintenance scheduler
        != on-chip self-refresh
```

---

## Sources and inspection boundary

### 1. GTE Automatic Electric Laboratories, US3729722A

- Title: `Dynamic mode integrated circuit memory with self-initiating refresh means`.
- Inventor: Joseph Patrick Shuba.
- Filed: **17 September 1971**.
- Granted / public patent date: **24 April 1973**.
- Direct public transcript: <https://patents.google.com/patent/US3729722A/en>.
- Independent patent rendering used for text cross-check: <https://uspto.report/patent/grant/3729722>.
- Existing detailed repository record: [`09-gte-1971-1973-self-initiating-refresh-system-boundary-deepening.md`](09-gte-1971-1973-self-initiating-refresh-system-boundary-deepening.md).

The patent explicitly identifies the Intel 1103 as a commercially available MOS memory used in its worked embodiment, describes the device as 1,024 cells arranged as 32 rows by 32 columns, says each bit must be refreshed at least once every two milliseconds, and derives a 16 kHz system refresh clock so one row is serviced every 62.5 microseconds and all 32 rows within two milliseconds.

The patent separately places the free-running clock, refresh pulse generator, row-address counter, gating, and busy/service relation in the surrounding memory-system apparatus. That control partition is already grounded elsewhere; this record uses it only as the system-side half of the product-contract comparison.

### 2. Signetics, 1972 MOS handbook, 1103 / 1103-1

- Corporate source: Signetics Corporation.
- Copyright: **1972**.
- Section title: `FULLY DECODED RANDOM ACCESS 1024 BIT DYNAMIC MEMORY`.
- Device: `1103 / 1103-1`.
- Directly inspected PDF preserved by device.report: <https://device.report/m/dafd5c77c72a981090c96e4a55aefea73e10f1e24d60e279806c3cf4fb8a94a5.pdf>.
- Relevant printed page: **23**.

The product description says:

- the Signetics 1103 is a `1024 word by 1 bit` random-access memory;
- stored information is non-destructively read;
- refreshing all 1,024 bits is accomplished in **32 read cycles**;
- those cycles are required every **two milliseconds**;
- the feature list independently states `REFRESH PERIOD — 2 MILLISECONDS FOR 0-70°C AMBIENT`;
- the block diagram identifies a memory matrix of **32 rows × 32 columns (1024 bits)** and `1 of 32` row selection.

This is a manufacturer-authored 1972 product document, but it is **Signetics**, not Intel. It is therefore evidence for a contemporary second-source/product-family contract, not proof that every electrical or cell-level implementation detail was identical to Intel's.

The handbook's front matter also warns that information on newly announced products may be preliminary and subject to change. That warning is retained rather than silently converting the handbook into a production-lot certification.

### 3. Intel, *1975 Data Catalog*, Intel 1103

- Corporate source: Intel Corporation.
- Catalog: **1975 Intel Data Catalog**.
- Device heading: `Silicon Gate MOS 1103` / `FULLY DECODED RANDOM ACCESS 1024 BIT DYNAMIC MEMORY`.
- Directly inspected PDF mirror: <https://deramp.com/downloads/mfe_archive/050-Component%20Specifications/Intel/Memory%20Components/1975_Intel_Data_Catalog.pdf>.
- Relevant PDF page: **24** (catalog page `2-7`).

Intel's own product description independently states that:

- the 1103 is intended for main-memory applications;
- it is a 1,024-word × 1-bit dynamic memory;
- stored information is non-destructively read;
- all 1,024 bits are refreshed in **32 read cycles**;
- the refresh is required every **two milliseconds**;
- the feature list gives a `2 milliseconds` refresh period for `0-70°C` ambient.

This later vendor-origin catalog is direct Intel product evidence for the same bounded contract that GTE's earlier patent attributes to the Intel 1103.

It is **not** an exact 1971 Intel datasheet. It therefore corroborates the device-family relation without proving that the specific 1103 revision available to GTE in September 1971 was documented by identical wording or identical characterization limits.

### 4. Intel 1975 catalog, 1103A and faster 1103A-1

The same catalog provides a useful anti-generalization control.

For the standard Intel **1103A**, the catalog again says that all 1,024 bits are refreshed in 32 read cycles and that this is required every **two milliseconds**.

For the higher-speed **1103A-1**, however, Intel still says that all 1,024 bits are refreshed in 32 read cycles while requiring those cycles every **one millisecond**; its AC-characteristics table likewise gives `tREF` as 1 ms.

The important bounded conclusion is not a complete 1103-family chronology. It is simply:

```text
same 1024-bit / 32-cycle coverage geometry
    != one invariant refresh deadline across related variants
```

This blocks the temptation to promote `2 ms` from a checked product contract into a universal property of 1103-derived parts or DRAM generally.

---

## Historical record

### H/P — a 1972 second-source 1103 exposes the 32-cycle / 2 ms contract directly

Signetics' 1972 product handbook is a direct period product-document witness. Its 1103 description ties three facts together in one manufacturer-authored page:

```text
1024 bits
    organized as 32 rows × 32 columns

whole-array refresh
    accomplished in 32 read cycles

refresh deadline
    every 2 ms at the documented ambient range
```

This is stronger than reconstructing the requirement from capacity alone. The product text itself says how many restorative read cycles constitute full coverage and how often that coverage is required.

### H/P — Intel's 1975 catalog independently gives the same bounded contract for Intel's 1103

Intel's catalog independently documents the same `32 read cycles / two milliseconds` relation for its own 1103.

That matters because GTE's 1971-filed patent had already used an Intel 1103 as the worked component and stated the same 32-row / two-millisecond requirement. The later Intel catalog is therefore an independent manufacturer-origin corroboration of the device-family contract, even though its 1975 date cannot by itself establish the exact text of Intel documentation available in 1971.

### H/P — GTE's 16 kHz cadence is system-side scheduling derived from the device requirement

The GTE patent does not merely repeat a two-millisecond number. It derives a system refresh cadence:

```text
32 rows / 2 ms
    -> one row per 62.5 µs
    -> 16 kHz refresh-event rate
```

It then implements that schedule with a free-running clock, refresh pulse generator, row counter, address gating, and service deferral.

The historical distinction is direct:

```text
1103 product requirement
    how much coverage is required by when

GTE controller
    one specific apparatus for producing that coverage
```

### H/P — the product can use ordinary read-cycle semantics as a restorative primitive without containing an autonomous scheduler

Both Signetics 1972 and Intel 1975 describe whole-array refresh in terms of 32 read cycles. Neither cited product page thereby documents a free-running internal refresh timer or autonomous internal row counter comparable to the later Case-09 self-refresh/on-chip-refresh mechanisms.

The bounded historical statement is therefore:

> **a product can expose a restorative access primitive plus a deadline while leaving recurring maintenance scheduling and traversal to surrounding apparatus.**

The analytical phrase `restorative access primitive` is project vocabulary; the period sources say `read cycles` and `refresh`.

### H/P — related Intel variants preserve coverage count while changing deadline

Intel's 1975 1103A-1 keeps the `32 read cycles` whole-array coverage relation but requires it every one millisecond rather than every two milliseconds.

That gives a period product-level counterexample to a simple equation among geometry, traversal count, and deadline:

```text
same number of refresh cycles
    != same allowed time window
```

No claim is made here about the physical reason for the shorter specified window.

---

## Engineering reconstruction

### E — device retention obligation and scheduler policy are separable state/control layers

The source set supports a clean split:

```text
payload substrate
    dynamic MOS charge state

maintenance coverage contract
    every required row must receive a restorative cycle

maintenance deadline
    full required coverage within the documented interval

traversal state
    which row is next

cadence authority
    when the next refresh event occurs

service arbitration
    what happens when ordinary access collides with maintenance
```

The 1103 product documentation directly constrains the first three. GTE's surrounding controller supplies the latter three in its worked architecture.

This is not merely terminology. Losing or violating each relation produces a different failure:

- cell state can decay even if controller logic is otherwise correct;
- sufficient event frequency can still fail coverage if traversal is wrong;
- correct traversal can still miss the retention deadline if cadence is too slow;
- correct maintenance can still alter service latency if arbitration is wrong or undocumented.

### E — a maintenance deadline does not dictate one scheduler implementation

From `32 cycles every 2 ms`, a designer can derive an average spacing no slower than one event per 62.5 microseconds if the work is uniformly distributed. GTE chooses exactly that regular cadence in its worked example.

But the product contract alone does not prove that refresh events must be uniformly spaced. Other schedules could satisfy the same coverage/deadline relation if their worst-case timing remains safe.

Therefore:

```text
retention deadline
    != fixed periodic phase
    != one unique controller design
```

This distinction becomes important in later Cases 69 and 105, where standards explicitly expose scheduling elasticity or finer maintenance granularity. The comparison is functional only; no direct historical genealogy is asserted.

### E — product-family geometry and retention margin are independent enough to require separate evidence

The 1103A-1 counterexample shows that a familiar geometry does not carry its retention deadline by logical necessity. The deadline is a product/electrical contract that must be sourced separately.

Thus:

```text
row count
    -> number of row-selective restorative events needed for coverage

but not by itself
    -> guaranteed retention interval
```

This prevents later engineering reconstruction from treating `rows × refresh interval` as a timeless DRAM constant.

### E — non-destructive logical read can still participate in physical retention work

The product documents say that user information is non-destructively read while also saying that read cycles accomplish refresh.

That creates an important vocabulary boundary:

```text
logical read is non-destructive
    != read has no restorative physical side effect
```

Case 03 already establishes sense/restore as part of dynamic-memory operation. This slice only adds a product-contract witness showing that period manufacturers could describe refresh coverage directly through read-cycle activity.

### E — external retention infrastructure can be constitutive without being part of the memory chip

In the GTE arrangement, the dynamic memory's useful persistence depends on surrounding timing, traversal, gating, and arbitration machinery. The payload cells alone do not execute the complete maintenance regime.

Therefore the retained object at system level depends on more than the physical cell state:

```text
cell capable of retaining charge for bounded interval
    + functioning refresh path
    + timely coverage
    + valid address selection
    + sufficient power
    -> continued operational payload retention
```

This remains a mechanism claim, not a philosophical thesis about infrastructure in general.

---

## Functional analogy

### A — later DRAM maintenance contracts also separate obligation from control placement

Case 09's later CBR/AUTO/SELF material and Case 105's LPDDR2 per-bank-refresh material likewise distinguish what maintenance coverage is required from who selects targets and who supplies recurring cadence.

The 1103 evidence is useful as an earlier functional comparison:

```text
early 1103 product contract
    refresh coverage + deadline visible at device interface
    external apparatus owns recurring scheduling/traversal in the checked system example

later CBR/AUTO regimes
    row enumeration may be internal
    recurring command cadence may remain external

later SELF REFRESH regimes
    recurring cadence may also move inside the device
```

This is **not** a claim that GTE's controller directly evolved into CBR, SDRAM AUTO REFRESH, or LPDDR per-bank refresh.

### A — similar numerical cadence does not prove common mechanism

A controller derived from `32 rows / 2 ms` and another system with a superficially similar event rate are not historically or physically linked merely because the arithmetic matches.

Timing arithmetic is evidence about one contract, not a genealogy.

---

## Philosophical interpretation

### I — maintenance obligation can be distributed across an interface

The exact technical fact is modest but conceptually useful: the dynamic device can define **what must repeatedly happen before a deadline** without containing the full apparatus that decides **when the next maintenance event occurs** or **how maintenance contends with ordinary service**.

Persistence is therefore not always a property exhausted by the retained substrate. It can be an operational relation distributed across device and controller.

This sharpens, rather than replaces, the project's broader claim that apparent persistence may be the result of continuing work.

### I — a deadline is not a memory of its own execution history

The two-millisecond product requirement constrains future action; it does not by itself retain a log of which rows have actually been serviced. Coverage/traversal state must exist somewhere in a concrete implementation if refresh is to be distributed correctly.

The distinction matters because:

> **a retention requirement is not itself evidence that the maintenance obligation has been discharged.**

No Stieglerian, Heideggerian, or Ernstian category is claimed as historical vocabulary for Intel, Signetics, or GTE.

---

## Explicit non-claims

This slice does **not** claim that:

1. the 1975 Intel catalog is the exact Intel 1103 datasheet GTE consulted in 1971;
2. the 1975 wording proves an identical characterization limit for every 1970–1975 Intel 1103 stepping;
3. Signetics' 1972 1103 is electrically or physically identical in every respect to Intel's 1103;
4. Signetics' document proves a legal or technical licensing relation with Intel;
5. GTE's patent proves shipment or commercial deployment of its refresh controller;
6. GTE invented automatic DRAM refresh;
7. Intel or Signetics invented the `32 read cycles` organization;
8. the patent citation chain proves engineering influence;
9. `self-initiating refresh` means on-chip self-refresh;
10. the Intel 1103 contains the GTE free-running clock, system row counter, or `memory busy` logic;
11. the Signetics 1103 contains those GTE controller blocks;
12. `32 read cycles` means 32 software-visible CPU load instructions;
13. every ordinary read schedule automatically guarantees complete refresh coverage;
14. a two-millisecond refresh period is a universal DRAM constant;
15. a 32-row organization implies a two-millisecond retention window;
16. the 1103A-1 one-millisecond contract explains why its physical cells retain less charge;
17. a one-millisecond specified refresh period measures raw cell-leakage time directly;
18. non-destructive logical read means no physical restoration occurs;
19. meeting average refresh frequency alone proves every row met its deadline;
20. an external refresh scheduler is historically or functionally the same as later CBR/AUTO/SELF REFRESH;
21. system-level automatic refresh and chip-level autonomous refresh are one mechanism;
22. the 1972 Signetics handbook's preliminary-data warning invalidates the documented contract; it instead limits what can be inferred about final production characterization;
23. the 1975 Intel catalog establishes the first public Intel disclosure of the 1103 refresh contract;
24. this slice closes first-shipment, first-datasheet, first-invention, or exact stepping chronology;
25. the numerical relation `32 × 62.5 µs = 2 ms` proves that all compliant controllers used a uniform 16 kHz schedule.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Signetics' 1972 1103 product document says all 1,024 bits are refreshed in 32 read cycles every two milliseconds | H/P | directly inspected manufacturer handbook, printed p. 23 |
| Signetics' block diagram shows 32 rows × 32 columns / 1-of-32 row selection | H/P | directly inspected manufacturer handbook, printed p. 23 |
| Intel's 1975 1103 catalog says all 1,024 bits are refreshed in 32 read cycles every two milliseconds | H/P | directly inspected Intel catalog, catalog p. 2-7 |
| GTE's 1971-filed patent uses a commercial Intel 1103 example with 32 rows and a two-millisecond requirement | H/P | directly inspected public patent text; already grounded in adjacent evidence |
| GTE derives a 16 kHz / 62.5 µs-per-row system schedule from that requirement | H/P | directly inspected patent example |
| GTE's refresh clock/counter/gating/busy logic is surrounding system apparatus rather than an on-chip 1103 self-refresh engine | H/P | directly inspected patent architecture; already grounded in adjacent evidence |
| Intel's 1975 standard 1103A also uses 32 read cycles every two milliseconds | H/P | directly inspected Intel catalog |
| Intel's 1975 1103A-1 still uses 32 read cycles but requires them every one millisecond | H/P | directly inspected Intel catalog, catalog p. 2-20 / AC table p. 2-22 |
| same coverage count does not imply one invariant refresh deadline | E | bounded reconstruction from Intel variants |
| device retention deadline is distinct from scheduler cadence and traversal implementation | E | bounded reconstruction from product docs + GTE system design |
| 1975 Intel evidence proves the exact 1971 product-document wording | X | explicitly rejected |
| 2 ms is a universal DRAM retention constant | X | contradicted by related Intel variant and broader case evidence |
| automatic system refresh equals on-chip self-refresh | X | contradicted by GTE system boundary |
| 32 ordinary software reads necessarily satisfy whole-array refresh | X | product document describes electrical read cycles/row coverage, not software access policy |
| the checked documents prove invention priority or direct genealogy | X | outside source scope |

---

## Remaining evidence debt

1. Find and directly inspect an **Intel-origin 1970–1972 1103 datasheet/catalog** or equally early Intel product document, ideally close to GTE's September-1971 filing, to close the exact vendor-document chronology rather than relying on a 1975 Intel corroboration.
2. Identify whether a surviving Intel documentation revision lets the exact 1103 stepping/package used by GTE's worked example be bounded more tightly.
3. If a product-implementation argument later requires it, separate datasheet refresh semantics from actual deployed controller timing using a named 1971–1973 system manual or logic print.
4. Do not expand this into a complete Intel/Signetics second-source or 1103 commercial-history project here. That broader genealogy belongs primarily in `tmzncty/computing-archaeology`.
5. First-invention, licensing, patent-influence, and shipment chronology remain explicitly open.

---

## Related-repository boundary

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `1103`, `Intel 1103 refresh`, and `Signetics dynamic memory` found no dedicated packet to reuse.

This repository should keep only the retention-specific seam:

```text
product refresh deadline / coverage primitive
    -> external maintenance cadence
    -> traversal state
    -> service arbitration
    -> completed whole-array coverage before deadline
```

A broad history of the Intel 1103, second-source production, DRAM product competition, exact stepping changes, early board-level refresh controllers, manufacturing, pricing, and system adoption belongs in `computing-archaeology` if developed.

---

## Sources

1. Joseph Patrick Shuba, GTE Automatic Electric Laboratories, `Dynamic mode integrated circuit memory with self-initiating refresh means`, US3729722A, filed 17 September 1971, public patent 24 April 1973: <https://patents.google.com/patent/US3729722A/en>; independent public rendering: <https://uspto.report/patent/grant/3729722>.
2. Signetics Corporation, 1972 MOS handbook, `1103 / 1103-1 — Fully Decoded Random Access 1024 Bit Dynamic Memory`, printed p. 23, archived PDF: <https://device.report/m/dafd5c77c72a981090c96e4a55aefea73e10f1e24d60e279806c3cf4fb8a94a5.pdf>.
3. Intel Corporation, *1975 Intel Data Catalog*, Intel 1103, catalog p. `2-7`, archived PDF: <https://deramp.com/downloads/mfe_archive/050-Component%20Specifications/Intel/Memory%20Components/1975_Intel_Data_Catalog.pdf>.
4. Intel Corporation, same catalog, Intel 1103A and 1103A-1 sections, especially catalog pp. `2-15`, `2-20`, and `2-22`, for the 32-cycle coverage relation and the 2 ms versus 1 ms variant boundary.
