# Case 03 Deepening — 1979–1984 64K DRAM Refresh Organization Across Vendors

**Status:** `bounded deepening complete`

## Research question

Case 03 already establishes that DRAM retention depends on recurrent restoration and that refresh-control state can live outside the array, inside a dedicated controller, or partly inside the DRAM package. Its evidence index still leaves one narrow comparison open:

> **Within the same 64K × 1 DRAM generation, did similar capacity and package compatibility imply the same refresh-coverage geometry or the same location of refresh-control state?**

The bounded answer is **no**.

Three manufacturer-primary records are especially useful:

1. Mostek's 1979–1980 MK4164 material documents **128 refresh cycles / 2 ms** and a dedicated pin-1 `RFSH` path backed by an **on-chip refresh counter**;
2. Texas Instruments' TMS4164 material, first dated **July 1980** and revised **October 1983** in the 1984 data book, documents **256 row strobes / 4 ms**, ordinary RAS-only refresh addressing, and explicitly leaves **pin 1 unconnected** for compatibility with other 64K RAMs that use that pin for an extra function;
3. Intel's April 1982 2164A material documents **128 refresh cycles / 2 ms** and hidden/RAS-only refresh whose refreshed row is still selected by an **externally supplied row address**; Intel's 8203 controller supplies a concrete external timer/counter implementation for that organization.

The result is not a vendor ranking or an invention-priority claim. It is a retention-contract comparison:

```text
same logical capacity
    != same refresh-coverage cardinality
    != same refresh deadline
    != same location of coverage state
    != same package-pin use
```

and:

```text
package compatibility
    != maintenance-control compatibility
```

---

## Why this slice is not a duplicate

Existing Case 03 deepenings answer narrower single-vendor or single-mechanism questions:

- [`03-mostek-1979-1980-rfsh-dynamic-counter-deepening.md`](03-mostek-1979-1980-rfsh-dynamic-counter-deepening.md) asks whether Mostek already documented an on-chip refresh counter and whether that counter itself was dynamic;
- [`03-intel-1982-1984-hidden-refresh-controller-state-deepening.md`](03-intel-1982-1984-hidden-refresh-controller-state-deepening.md) asks where timer, next-row, and arbitration state live in the Intel 2164A / 8203 arrangement;
- [`03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md`](03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md) asks why later CAS-before-RAS internal addressing still does not equal self-refresh.

The present slice does something different: it places contemporaneous **64K × 1** products beside one another and asks which aspects of their retention contract are actually interchangeable.

That comparison matters because part names and package-era similarity can tempt a later reader to infer one generic `4164 refresh mechanism`. The sources do not support that simplification.

---

## Claim-type discipline

### Historical record — `H/P`

Statements about named devices, dates, refresh-cycle counts, pin functions, and vendor-described operating modes come from contemporary manufacturer material or archival scans of that material.

### Engineering reconstruction — `E`

Terms such as `coverage cardinality`, `coverage-state locus`, `maintenance contract`, and `compatibility envelope` are project vocabulary used to compare the mechanisms.

### Functional analogy — `A`

Cross-vendor comparisons identify similar functional obligations. They do not imply shared transistor layouts, direct copying, or one technical genealogy.

### Philosophical interpretation — `I`

Any statement about identity or persistence remains downstream of the device-level evidence and is explicitly marked as interpretation.

---

# 1. Historical record

## H/P — Mostek's 1979 MK4164 product brief combines a 128-cycle deadline with an on-chip refresh counter

Mostek's *1979 Memory Data Book and Designers Guide* includes an MK4164 product brief for a 65,536 × 1 dynamic RAM. The feature list includes:

- `128 cycle refresh (2ms)`;
- `On chip refresh counter on pin 1`.

The 1980 *Memory Data Book and Designers Guide* then names pin 1 `RFSH` and explains the mechanism in more detail. Bringing `RFSH` low while RAS is inactive enables an internal refresh operation using the on-chip counter; returning `RFSH` high advances the counter to the next refresh address.

The same 1980 text states that the internal refresh counter is itself **dynamic** and requires refresh, and that the recurring RFSH activity needed by the array is sufficient to maintain it.

Thus, for the bounded Mostek RFSH path:

```text
external system
    supplies refresh invocation / cadence

MK4164 pin-1 RFSH path
    selects row from on-chip coverage state
    performs refresh
    advances on-chip coverage state
```

This is a public-documentation floor, not proof that Mostek invented the on-chip refresh counter or was first to ship it.

**Primary archives:**

- Mostek, *1979 Memory Data Book and Designers Guide*: <https://www.bitsavers.org/components/mostek/_dataBooks/1979_Mostek_Memory_Data_Book_and_Designers_Guide.pdf>
- Mostek, *1980 Memory Data Book and Designers Guide*: <https://bitsavers.trailing-edge.com/components/mostek/_dataBooks/1980_Mostek_Memory_Data_Book_and_Designers_Guide.pdf>

The detailed source custody and source-boundary notes are already recorded in [`03-mostek-1979-1980-rfsh-dynamic-counter-deepening.md`](03-mostek-1979-1980-rfsh-dynamic-counter-deepening.md).

## H/P — TI's TMS4164 uses a different refresh geometry: 256 row strobes in 4 ms

Texas Instruments' 1984 *MOS Memory Data Book* contains the TMS4164 / SMJ4164 entry. The entry itself is dated **July 1980 — revised October 1983** and describes a 65,536-bit dynamic RAM.

Its retention requirement is not the same as the Mostek product brief above. TI says:

- the refresh period is **4 milliseconds**;
- during that period **each of 256 rows must be strobed with RAS** in order to retain data;
- CAS may remain high during the refresh sequence to conserve power.

The device therefore exposes a 256-row RAS-refresh obligation:

```text
TMS4164 bounded requirement
    = cover 256 refresh rows
      within 4 ms
```

That is already enough to block the inference that equal 64K logical capacity implies one universal refresh-row count or one universal cadence contract.

**Primary manufacturer archive:** Texas Instruments, *MOS Memory Data Book* (1984), TMS4164 / SMJ4164 entry: <https://www.bitsavers.org/components/ti/_dataBooks/1984_TI_MOS_Memory_Data_Book.pdf>.

An archival text index of the same vendor scan preserves the TMS4164 description and its July-1980 / October-1983 dating.

## H/P — TI explicitly leaves pin 1 unconnected while acknowledging that other 64K RAMs use it for an extra function

The same TI entry states that **pin 1 has no internal connection** and gives the compatibility reason: this allows compatibility with other 64K RAMs that use pin 1 for an additional function.

That sentence is unusually valuable for a cross-vendor retention comparison because the contemporaneous Mostek documentation supplies one concrete example of exactly such an additional function:

```text
Mostek MK4164
    pin 1 = RFSH
    on-chip refresh-counter path

TI TMS4164
    pin 1 = NC
    256 externally strobed refresh rows
```

The safe claim is only that the two primary records exhibit different uses of the same package position while remaining in the same broad 64K-DRAM package generation.

Do **not** silently strengthen TI's generic phrase `other 64K RAMs` into a historical statement that TI was specifically referring to Mostek. The comparison is ours, based on two independently documented products.

## H/P — TI's RAS-only refresh still requires the system to present the refresh-row sequence

TI says that strobing each of the 256 row addresses with RAS refreshes the device. In this bounded product path, the DRAM therefore does not need to own the next-refresh-row sequence internally in order to satisfy the documented RAS-only interface.

The source establishes:

```text
external row-address presentation
    -> DRAM row restoration
```

It does not establish which exact external implementation supplied that sequence in every TI-based system. A board could use a dedicated refresh counter, a memory controller, processor logic, or another arrangement satisfying the interface contract.

Accordingly:

```text
external refresh address required
    != one mandatory external-controller implementation
```

## H/P — Intel's April 1982 2164A is also 64K × 1, but its bounded refresh contract is 128 cycles in 2 ms

Intel's April 1982 `2164A FAMILY — 65,536 x 1 BIT DYNAMIC RAM` datasheet specifies:

- `128 refresh cycle/2 ms RAS only refresh`;
- RAS-only refresh;
- hidden refresh;
- ordinary access cycles that can also contribute refresh when the required row combinations are covered.

The `Refresh Cycles` section says the device has 512 sense amplifiers, each associated with 128 storage cells, and requires coverage of the 128 refresh-address combinations.

Thus:

```text
Intel 2164A
    logical capacity = 64K x 1
    refresh coverage = 128 address combinations / 2 ms

TI TMS4164
    logical capacity = 64K x 1
    refresh coverage = 256 rows / 4 ms
```

Logical capacity alone therefore does not tell the system how many distinct refresh-address steps are required.

**Primary archive:** Intel, `2164A FAMILY`, order no. 210425-001, April 1982: <https://www.minuszerodegrees.net/memory/4164/datasheet_2164A.pdf>.

Detailed source notes are already preserved in [`03-intel-1982-1984-hidden-refresh-controller-state-deepening.md`](03-intel-1982-1984-hidden-refresh-controller-state-deepening.md).

## H/P — Intel hidden refresh hides output disruption, not refresh-address ownership

Intel's hidden-refresh sequence allows valid data to remain at DOUT while a RAS-only refresh occurs. The datasheet nevertheless says that the refreshed row is the row addressed at the time of the second RAS.

So the 2164A gives another 64K-generation organization distinct from the Mostek RFSH path:

```text
Intel hidden refresh
    output can remain valid
    + refreshed row is externally addressed

Mostek RFSH
    refresh row comes from on-chip counter
```

This is a direct warning against reading the word `hidden` as `self-selecting`, `self-scheduled`, or `self-refreshing`.

## H/P — Intel's 8203 shows one concrete external control structure for externally addressed refresh

Intel's 1984 *Memory Components Handbook* describes the 8203 DRAM controller with:

- a refresh timer;
- a refresh counter holding the address for the next refresh;
- refresh/access arbitration;
- an address multiplexer that places refresh-counter contents on the DRAM address bus.

The 8203 therefore supplies a concrete implementation of the control state that an externally addressed DRAM interface can leave outside the memory device:

```text
refresh deadline / phase
    -> controller timer

next refresh row
    -> controller counter

maintenance vs useful access
    -> controller arbitration
```

This does not mean every Intel 2164A system used an 8203. It is a named manufacturer-supported architecture showing where the displaced state could live.

**Primary archive:** Intel, *Memory Components Handbook* (1984), 8203 section: <https://www.bitsavers.org/components/intel/_dataBooks/1984_Intel_Memory_Components_Handbook.pdf>.

---

# 2. Controlled cross-vendor comparison

The historically supported comparison can be summarized as follows.

| Device / source state | Logical organization | Documented refresh requirement | Refresh-row source in bounded path | Pin-1 relation | What remains external |
| --- | --- | --- | --- | --- | --- |
| Mostek MK4164, 1979 brief / 1980 detailed entry | 65,536 × 1 | 128 cycles / 2 ms | on-chip refresh counter in `RFSH` mode | `RFSH` | recurrence / invocation of RFSH |
| TI TMS4164, July 1980 / rev. Oct 1983 entry | 65,536 × 1 | 256 rows / 4 ms | externally presented row address for RAS-only refresh | NC; explicitly retained for package compatibility with devices using an extra pin-1 function | row sequence + recurrence |
| Intel 2164A, April 1982 | 65,536 × 1 | 128 cycles / 2 ms | externally presented refresh row in the bounded RAS-only / hidden path | no on-chip-counter claim used here | row sequence + recurrence; 8203 is one concrete external controller |

This table is a comparison of **documented interface contracts**, not an assertion that the three dies share or do not share a particular transistor-level floorplan.

---

# 3. Engineering reconstruction

## E — logical capacity does not determine maintenance coverage geometry

All three products expose 65,536 logical one-bit locations. Yet their documented refresh contracts differ in how many refresh-row selections must occur within the specified interval.

Therefore:

```text
logical address cardinality
    != refresh-address cardinality
```

The refresh geometry depends on internal array/sense organization and vendor design choices that are not recoverable from the marketing capacity alone.

This is an important retention boundary because the maintenance controller must satisfy the device's physical coverage contract, not merely know how many logical bits exist.

## E — the deadline and the coverage count are separate parameters

A shorthand such as `refresh every few milliseconds` is not enough to characterize the obligation.

The bounded records show at least two independent dimensions:

```text
coverage set
    = how many refresh-address classes must be visited

coverage deadline
    = how long the system has to visit the required set
```

For these records:

```text
Mostek MK4164: 128 / 2 ms
Intel 2164A:   128 / 2 ms
TI TMS4164:    256 / 4 ms
```

The same average number of row-refresh opportunities per unit time would not, by itself, prove that arbitrary scheduling satisfies each device; ordering, timing minima/maxima, and interface constraints still matter.

## E — moving coverage state on-chip changes the support boundary without eliminating the retention obligation

Mostek's `RFSH` path internalizes next-row state. TI and Intel's bounded RAS-only paths leave refresh-row presentation external.

The useful decomposition is:

```text
physical charge-retention obligation
    != refresh deadline
    != refresh-row coverage state
    != refresh invocation
    != restore execution
```

Mostek moves one of these relations across the package boundary:

```text
coverage state
    external -> on-chip
```

but it does not thereby internalize cadence generation. An external RFSH recurrence is still required.

Thus:

```text
on-chip next-row state
    != self-refresh
```

## E — pin compatibility can deliberately coexist with maintenance-semantic diversity

TI's decision to leave pin 1 unconnected is especially revealing. A package can preserve electrical/mechanical interchangeability at one pin while different vendors assign different maintenance functions to that position.

This gives a bounded distinction:

```text
pinout compatibility envelope
    != identical control-state topology
```

A system designer therefore cannot infer the complete refresh contract from:

- `64K × 1` capacity;
- a `4164`-like part number;
- a 16-pin package;
- one pin being safely unconnected on a particular vendor's part.

The correct contract has to come from the named device documentation.

## E — maintenance portability requires satisfying the target device's contract, not merely preserving ordinary read/write compatibility

Two parts may be sufficiently similar for ordinary address/data service while differing in refresh-cycle count, refresh deadline, or special refresh pin use.

So:

```text
ordinary service compatibility
    != retention-maintenance compatibility
```

A replacement or mixed-vendor board would need a controller/timing arrangement that satisfies every installed device's refresh requirements. This is an engineering consequence of the documented contracts.

This file does **not** claim that any specific historical board failed because of such a substitution; that would require board schematics, controller configuration, and an observed failure record.

## E — maintenance-control state has both a semantic role and a physical location

Across the three products, the role `remember which refresh row comes next` remains intelligible even though its embodiment moves:

```text
Mostek bounded RFSH path
    -> on-chip counter

Intel 8203-supported path
    -> external controller counter

TI bounded RAS-only interface
    -> external system must supply the row sequence
       but the exact external embodiment is unspecified by the DRAM datasheet
```

This is precisely why `control state` should be treated as a role rather than as a fixed component class.

---

# 4. Functional analogy boundaries

## A — relation to later CAS-before-RAS DRAM

Later TI TMS4256/TMS4257 CAS-before-RAS documentation also moves refresh-address generation on-chip, but it does so without requiring a dedicated `RFSH` package pin.

The functional similarity is:

```text
Mostek MK4164 RFSH
    and
later CBR DRAM

both can internalize next-refresh-row state
```

The historical/interface difference is:

```text
Mostek RFSH
    dedicated pin-1 invocation path

later CBR
    CAS/RAS ordering invokes internal refresh addressing
```

No genealogy is asserted from one to the other.

## A — relation to Case 09 and Case 10

Case 09 studies CAS-before-RAS refresh-address internalization as its own regime. Case 10 studies the further move from internal coverage state to internal scheduling/condition-derived trigger state.

The present 64K comparison therefore helps preserve a three-stage conceptual distinction without forcing a linear historical story:

```text
externally supplied refresh row
    !=
on-chip refresh-row progression
    !=
on-chip refresh cadence / self-refresh
```

These are separable functions. Different devices can combine them differently.

## A — relation to compatibility tables in later storage systems

Later cases in this repository show software remembering device-specific quirks or command restrictions. The 64K DRAM comparison is only functionally analogous at a high level: the system must respect device-specific retention semantics even when a broader interface looks compatible.

There is no claim of shared implementation or direct historical descent.

---

# 5. Philosophical interpretation

## I — technical identity is layered rather than exhausted by interchangeable appearance

A 64K × 1 DRAM can be `the same kind of thing` at one interface level while being different at another:

```text
same broad logical role
    + similar package
    + similar read/write vocabulary

can coexist with

different maintenance geometry
    + different control-state location
    + different refresh timing contract
```

For this project, that is useful only as a downstream interpretation. The historical actors did not need the vocabulary `layered identity` to design the devices.

The primary evidence remains the vendor-defined refresh contract.

---

# 6. Explicit non-claims

This slice does **not** establish that:

1. Mostek invented the on-chip refresh counter;
2. MK4164 was the first 64K DRAM with such a counter;
3. the 1979 product brief proves volume shipment in 1979;
4. TI's phrase `other 64K RAMs` specifically names or targets Mostek;
5. TI TMS4164 and Intel 2164A have identical internal arrays because both are externally refreshed;
6. 128-cycle parts are generally better or worse than 256-cycle parts;
7. 2 ms and 4 ms specifications can be compared without considering the corresponding coverage counts and timing constraints;
8. all 64K DRAMs of the period were pin-compatible;
9. package compatibility guarantees electrical, timing, or maintenance compatibility;
10. the string `4164` denotes one standardized internal refresh architecture;
11. hidden refresh means self-refresh;
12. on-chip next-row counting means autonomous cadence generation;
13. an externally addressed refresh interface requires one particular counter IC;
14. the Intel 2164A requires the Intel 8203 specifically;
15. every normal read/write sequence necessarily satisfies refresh coverage;
16. merely issuing the right number of refresh cycles guarantees correct ordering or all timing margins;
17. the Mostek dynamic refresh-counter implementation is shared by TI or Intel;
18. the same physical row count is directly exposed as the same logical-row geometry across vendors;
19. a mixed-vendor historical board necessarily malfunctioned;
20. a specific board was designed to exploit pin-1 compatibility;
21. the compared products share one invention genealogy;
22. later CAS-before-RAS designs descended directly from Mostek RFSH;
23. vendor package compatibility was motivated primarily by refresh semantics;
24. a pin marked NC is safe to repurpose without consulting the complete named-device specification;
25. the comparison establishes transistor-level topology;
26. refresh-control location alone determines reliability;
27. moving state on-chip makes it persistent across power loss or reset;
28. any refresh counter is itself dynamic unless the vendor says so;
29. `refresh row` and user-visible logical row are interchangeable terms;
30. broad functional similarity proves historical continuity.

---

# 7. What this closes for Case 03

The existing Case 03 evidence index listed **cross-vendor 64K DRAM refresh-organization comparison** as open work.

This slice closes that debt at the interface-contract level for the bounded Mostek / TI / Intel comparison:

```text
64K logical capacity
    -> does not fix refresh-row count

similar package generation
    -> does not fix pin-1 maintenance semantics

refresh requirement
    -> can leave next-row state outside the DRAM
       or move it on-chip

on-chip next-row state
    -> still does not imply autonomous cadence
```

It does **not** close:

- transistor-level comparison of the three vendors' refresh counters/array organizations;
- first-invention or first-shipment chronology;
- controlled hardware substitution tests;
- exact board-level compatibility histories;
- the broader 64K-DRAM product genealogy, which belongs primarily in `tmzncty/computing-archaeology` if pursued.

Case 03 should therefore remain **`grounded`** rather than being promoted on the basis of this comparison alone.

---

# 8. Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `MK4164` returned no dedicated technical-history packet to reuse in this round.

Keep in `technical-retention`:

- the refresh deadline / coverage decomposition;
- the cross-vendor location of next-row state;
- package compatibility versus retention-maintenance compatibility;
- the anti-anachronism boundary around `hidden`, `automatic`, and `self-refresh`.

Route to `computing-archaeology` if expanded:

- full vendor-by-vendor 64K DRAM release chronology;
- die/process comparison;
- JEDEC pinout-standardization history;
- pricing, market adoption, sourcing, and board-design history;
- invention-priority disputes unrelated to the retention seam.

---

## Sources

### Primary / contemporary manufacturer records

- Mostek, *1979 Memory Data Book and Designers Guide*, MK4164 product brief: <https://www.bitsavers.org/components/mostek/_dataBooks/1979_Mostek_Memory_Data_Book_and_Designers_Guide.pdf>.
- Mostek, *1980 Memory Data Book and Designers Guide*, MK4164 detailed `RFSH` description: <https://bitsavers.trailing-edge.com/components/mostek/_dataBooks/1980_Mostek_Memory_Data_Book_and_Designers_Guide.pdf>.
- Texas Instruments, *MOS Memory Data Book* (1984), TMS4164 / SMJ4164 entry dated July 1980, revised October 1983: <https://www.bitsavers.org/components/ti/_dataBooks/1984_TI_MOS_Memory_Data_Book.pdf>.
- Intel, `2164A FAMILY — 65,536 x 1 BIT DYNAMIC RAM`, April 1982: <https://www.minuszerodegrees.net/memory/4164/datasheet_2164A.pdf>.
- Intel, *Memory Components Handbook* (1984), 8203 DRAM controller section: <https://www.bitsavers.org/components/intel/_dataBooks/1984_Intel_Memory_Components_Handbook.pdf>.

### Repository evidence reused rather than duplicated

- [`03-mostek-1979-1980-rfsh-dynamic-counter-deepening.md`](03-mostek-1979-1980-rfsh-dynamic-counter-deepening.md)
- [`03-intel-1982-1984-hidden-refresh-controller-state-deepening.md`](03-intel-1982-1984-hidden-refresh-controller-state-deepening.md)
- [`03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md`](03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md)
