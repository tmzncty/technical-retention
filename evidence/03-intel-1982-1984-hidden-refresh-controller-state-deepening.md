# Deepening Record — Intel 1982–1984 Hidden Refresh and Refresh-Control State

## Target case

[`cases/03-dram-refresh-as-scheduled-restoration.md`](../cases/03-dram-refresh-as-scheduled-restoration.md)

## Status

**`bounded deepening complete`**

This record deepens one narrow question left implicit by the original DRAM grounding:

> When a DRAM vendor says refresh can be `hidden`, where does the maintenance schedule and row-selection state actually live, and does hiding refresh from useful data service make the DRAM device autonomous?

The bounded answer is **no** for the Intel 2164A / 8203 system documented here. Intel's April 1982 2164A datasheet makes refresh visually unobtrusive at the data output, but it still describes refresh as operating on an externally supplied row address. Intel's 8203 DRAM-controller documentation then makes the displaced control state explicit: a refresh timer requests work, a refresh counter remembers the next row, an arbiter schedules refresh against ordinary accesses, and an address multiplexer drives the refresh-counter contents onto the DRAM address lines.

This is not a general history of DRAM refresh, an invention-priority claim, or an account of later CAS-before-RAS/self-refresh DRAMs. It is a named Intel product pair used to establish one retention boundary:

```text
refresh hidden from a useful output
    != refresh control absent
    != refresh control located inside the DRAM array/device
```

---

## Why this slice matters

The base case already established:

```text
retained capacitor state
    -> finite retention interval
    -> scheduled regeneration obligation
```

The 2164A / 8203 documentation adds a second layer:

```text
maintenance obligation
    != maintenance-control state

cell charge
    != refresh timer state
    != refresh row-counter state
    != refresh/access arbitration state
```

The logical memory appears continuously available because the system coordinates several different retained or transient states. The value being preserved lives in the DRAM cells; the state that decides **when** and **which row** to restore can live elsewhere in the memory subsystem.

---

## Historical record

### H/P — Intel's April 1982 2164A requires 128 refresh cycles within 2 ms

Intel's April 1982 `2164A FAMILY — 65,536 x 1 BIT DYNAMIC RAM` datasheet lists:

- `128 refresh cycle/2 ms RAS only refresh`;
- extended page mode, read-modify-write, and hidden refresh;
- compatibility with Intel DRAM controllers.

The same first-page description says refreshing is accomplished by RAS-only cycles, hidden refresh cycles, or normal read/write cycles over the required row-address combinations during the 2 ms period.

This is period manufacturer documentation of a concrete device family. It is not evidence that every contemporary 64K DRAM used the same internal geometry or refresh protocol.

**Primary anchor:** Intel Corporation, `2164A FAMILY`, order no. 210425-001, April 1982, printed p. 3-219.

Archived scan: <https://www.minuszerodegrees.net/memory/4164/datasheet_2164A.pdf>

### H/P — the 2164A's RAS-only refresh remains row-addressed

The `Refresh Cycles` section states that the 2164A has 512 sense amplifiers, each controlling 128 storage cells, and is therefore refreshed in 128 cycles. It says the low-order row-address combinations select the rows refreshed during a cycle and recommends RAS-only refresh for reduced system power.

The important retention point is not the exact array topology by itself. It is that a refresh cycle still has an **addressed row**. The device has not abolished row-selection state merely because the operation is maintenance rather than an ordinary read.

**Primary anchor:** Intel 2164A datasheet, printed p. 3-229, `Refresh Cycles`.

### H/P — `Hidden Refresh` hides maintenance from DOUT, not from the row-address discipline

Intel describes Hidden Refresh as a standard feature that allows refresh cycles to occur while valid data remains at the output pin. The documented sequence keeps CAS low while RAS is precharged and then performs a RAS-only refresh cycle.

The following page makes the boundary especially explicit: the useful output can remain valid while the part is refreshed at **the row addressed at the time of the second RAS**.

Thus the historical meaning of `hidden` in this device documentation is bounded:

```text
hidden from output-data availability
    != autonomous selection of the row to refresh
```

It also does not mean that no bandwidth, power, clocks, address state, or arbitration is consumed elsewhere in the system.

**Primary anchors:** Intel 2164A datasheet, printed pp. 3-229–3-230, `Hidden Refresh` and timing figure.

### H/P — after extended bias without clocks, the 2164A requires initialization cycles

The 2164A `Power On` section requires an initial pause followed by at least eight initialization cycles containing RAS clocks. It further says eight initialization cycles are required after extended periods of bias greater than 2 ms without clocks.

This is useful negative evidence against treating supply power alone as the refresh mechanism:

```text
powered DRAM
    != actively maintained DRAM
```

The datasheet does **not** say that payload data remains valid through such an interval. The initialization requirement should therefore not be turned into a claim of post-gap data recovery.

**Primary anchor:** Intel 2164A datasheet, printed p. 3-230, `Power On`.

### H/P — Intel's 8203 makes the displaced refresh-control state explicit

Intel's 8203 is documented as a dynamic-RAM system controller for 16K and 64K DRAMs, including the 2164A family. Its feature list includes:

- address multiplexing and DRAM strobes;
- a refresh timer and refresh counter;
- refresh/access arbitration;
- internally or externally requested refresh cycles.

The controller therefore supplies a concrete system location for work that the DRAM cell itself does not express.

**Primary anchor:** Intel `8203 — 64K DYNAMIC RAM CONTROLLER`, reproduced in Intel's 1984 *Memory Components Handbook* and contemporary datasheet copies.

Canonical handbook archive: <https://www.bitsavers.org/components/intel/_dataBooks/1984_Intel_Memory_Components_Handbook.pdf>

Renderable mirror used for text verification: <https://deramp.com/downloads/mfe_archive/050-Component%20Specifications/Intel/Memory%20Components/1984_Intel_Memory_Components_Handbook.pdf>

### H/P — the 8203 refresh timer remembers when maintenance is due

Intel's `REFRESH TIMER AND COUNTER` section says the refresh timer increments with the controller clock until a preset count causes an internal refresh request. External refresh requests reset the timer but do not disable it.

This gives a concrete maintenance-control state distinct from the stored payload:

```text
DRAM payload state
    != time-since/phase state used to trigger refresh
```

The source does not describe this timer as durable across controller reset or power loss. It is ordinary powered control state.

**Primary anchor:** Intel 1984 *Memory Components Handbook*, 8203 section, p. 3-82, §2.2.3.

### H/P — the 8203 refresh counter remembers which row comes next

The same section says the internal address counter contains the address for the **next refresh cycle** and increments after each refresh. It counts through the refresh-address space before returning to zero.

The 8203 address multiplexer then places the refresh-counter contents on the address bus during a refresh cycle.

This is stronger than saying merely that `a controller refreshes DRAM`. It identifies a specific piece of state whose role is to preserve **coverage progress** through the refresh-address set:

```text
refresh deadline phase
    != refresh coverage position
```

The timer answers roughly `when should another refresh occur?`; the counter answers `which refresh address should this cycle service?`.

**Primary anchor:** Intel 1984 *Memory Components Handbook*, 8203 section, p. 3-82, §§2.2.3–2.2.4.

### H/P — the 8203 arbitrates maintenance against useful memory service

Intel's controller documentation also describes an arbiter resolving read/write and refresh requests. An in-progress refresh can delay a useful access, while simultaneous ordinary-access and refresh requests are ordered by the controller's arbitration rules.

Therefore `hidden` or `transparent` refresh is not literally cost-free simultaneity. It is a system scheduling arrangement that attempts to place maintenance where it least disrupts useful service.

**Primary anchor:** Intel 1984 *Memory Components Handbook*, 8203 §§2.2.2 and 2.2.6.

---

## Engineering reconstruction

### E — the retention mechanism and the maintenance scheduler are different state machines

The 2164A cells hold the values that must survive between accesses. The 8203 holds control state that determines refresh timing and coverage order.

A useful decomposition is:

```text
payload bit state
    = charge/sense state in DRAM array

maintenance deadline/phase state
    = refresh timer

maintenance coverage position
    = refresh address counter

service/maintenance ordering state
    = arbiter and request state
```

Only the first category is the user-visible memory payload, but the others are part of the machinery that allows it to remain valid over time.

### E — `hidden` is a visibility property, not a retention-mechanism class

Intel's Hidden Refresh keeps previously produced output data available while a refresh cycle occurs. That describes what an observer at DOUT sees.

It does not by itself answer:

- who generated the refresh request;
- who retained the next refresh address;
- who arbitrated refresh against useful accesses;
- whether maintenance consumed power or internal cycle time;
- whether the refresh controller state survives reset.

Therefore:

```text
maintenance invisibility at one interface
    != maintenance autonomy
    != maintenance-state persistence
```

### E — refresh coverage is itself an ordered obligation

A 2 ms deadline for `the memory` is not satisfied by repeatedly refreshing one row. The system must revisit the required refresh-address set within the interval.

The 8203 counter is therefore not merely an address generator. Functionally it is a compact representation of unfinished maintenance coverage:

```text
all required rows serviced in interval
    depends on
next-row / coverage-progress state
```

This is a bounded engineering reconstruction from Intel's documented counter behavior. Intel does not use the phrase `maintenance coverage debt`.

### E — powered retention can depend on volatile control state

The DRAM payload is volatile because cell charge decays. The 8203 timer/counter are also powered control state. Yet the payload's continued survival depends on that control state repeatedly causing the right restoration operations.

This yields a useful distinction:

```text
state being retained
    != state required to retain it
```

The latter need not be durable beyond the operating session to be constitutive of retention during that session.

---

## Functional analogy

### A — relation to maintenance-control-state cases elsewhere in the repository

Later repository cases contain durable maintenance maps, scan checkpoints, bad-block tables, and repair-debt metadata. The 8203 timer/counter are functionally comparable only in the limited sense that they encode **maintenance control state**.

They differ sharply in persistence horizon:

```text
8203 refresh timer/counter
    powered, regime-local control state

persistent scan / repair metadata in later systems
    may survive restart or media/controller replacement
```

This comparison supports the repository's existing rule:

> `maintenance-control state` does not imply `durable checkpoint`.

It does not establish historical continuity between early DRAM controllers and later scrub/repair systems.

---

## Philosophical / media-theoretical boundary

### I — apparent continuity can depend on displaced temporal organization

At the software-facing address level, a DRAM location appears to retain one current value. The 2164A / 8203 pair shows that this continuity is distributed across:

- decaying electrical state;
- repeated physical restoration;
- a timer that represents maintenance timing;
- a counter that represents maintenance coverage;
- arbitration that negotiates maintenance with useful service.

This supports a narrow philosophical observation: stable availability can be produced by **displacing temporal discipline into infrastructure that is not itself the represented payload**.

The observation stops there. It does not make a DRAM refresh counter a cultural memory, an archive, `tertiary retention`, or `Bestand`.

---

## Explicit non-claims

This deepening does **not** claim that:

1. Intel invented hidden refresh;
2. Intel invented the external DRAM refresh counter;
3. the 2164A was the first DRAM to support hidden refresh;
4. the 8203 was the first controller with a refresh timer/counter;
5. all 64K DRAMs used the 2164A's exact 128-cycle geometry;
6. all 1980s DRAM systems used an Intel 8203;
7. the 2164A contains no internal circuitry involved in restoration;
8. `hidden refresh` means zero power, zero bandwidth, or zero latency cost;
9. valid DOUT during hidden refresh proves every internal row remains valid indefinitely;
10. eight initialization cycles after a clock gap restore lost payload data;
11. the 8203 refresh counter is nonvolatile;
12. the refresh counter is a user-visible address register;
13. refresh-counter reset necessarily corrupts data immediately;
14. the 8203/2164A arrangement is identical to later CAS-before-RAS or self-refresh DRAM;
15. functional similarity to later maintenance checkpoints proves genealogy.

---

## Claim ledger

| Claim | Label | Evidence |
| --- | --- | --- |
| Intel documented the 2164A in April 1982 as a 64K x1 dynamic RAM requiring 128 refresh cycles within 2 ms | H/P | Intel 2164A datasheet, p. 3-219 |
| The 2164A can perform hidden refresh while maintaining valid output data | H/P | Intel 2164A datasheet, pp. 3-229–3-230 |
| Hidden refresh still acts on the row addressed at the second RAS | H/P | Intel 2164A datasheet, p. 3-230 |
| The 2164A requires initialization cycles after extended bias without clocks | H/P | Intel 2164A datasheet, p. 3-230 |
| Intel's 8203 contains a refresh timer and a refresh address counter | H/P | Intel 1984 Memory Components Handbook, 8203 §2.2.3 |
| The 8203 counter holds the address used for the next refresh and advances after refresh cycles | H/P | same |
| The 8203 address multiplexer drives refresh-counter contents during refresh | H/P | Intel 8203 §2.2.4 |
| Timer state and refresh-address state are distinct from DRAM payload state | E | bounded reconstruction from paired device/controller documentation |
| Hidden refresh is interface invisibility rather than proof of autonomous maintenance | E | bounded reconstruction from 2164A + 8203 documentation |
| Early DRAM control state is historically continuous with later durable scrub/checkpoint metadata | X | explicitly unsupported |

---

## Source ledger

### Primary manufacturer documentation

1. Intel Corporation, **`2164A FAMILY — 65,536 x 1 BIT DYNAMIC RAM`**, order no. 210425-001, April 1982.
   - archived scan: <https://www.minuszerodegrees.net/memory/4164/datasheet_2164A.pdf>
   - printed p. 3-219: headline refresh requirement and overview;
   - printed p. 3-229: `Refresh Cycles`, start of `Hidden Refresh`;
   - printed p. 3-230: hidden-refresh row address, DOUT behavior, power-on / no-clock initialization boundary.
2. Intel Corporation, **`8203 — 64K DYNAMIC RAM CONTROLLER`**, reproduced in *Intel Memory Components Handbook* (1984).
   - canonical Bitsavers archive: <https://www.bitsavers.org/components/intel/_dataBooks/1984_Intel_Memory_Components_Handbook.pdf>
   - alternative renderable archive: <https://deramp.com/downloads/mfe_archive/050-Component%20Specifications/Intel/Memory%20Components/1984_Intel_Memory_Components_Handbook.pdf>
   - p. 3-82: refresh/access arbiter; `REFRESH TIMER AND COUNTER`; multiplexer; internal/external refresh description.

### Source-quality note

The 2164A scan was inspected directly at the cited printed pages, including the timing diagram and `Power On` section. The Intel handbook is a period manufacturer handbook preserved by archival mirrors; OCR/search access is sufficient for the quoted structural claims, but this slice does not depend on interpreting an unreadable schematic detail.

---

## Remaining debt

This slice intentionally leaves several questions open:

- recover an earlier primary genealogy for dedicated DRAM refresh controllers before the Intel 8202A/8203 family;
- determine when `hidden refresh`, CAS-before-RAS refresh, and later self-refresh became distinct vendor terms and implementations, without back-projecting later terminology;
- directly compare a later DRAM with an **on-device** refresh-address counter to this externally controlled 2164A arrangement;
- run a bounded hardware or logic-level experiment showing what happens when refresh-address coverage is deliberately biased or one row is repeatedly omitted;
- move any broad controller genealogy or DRAM-generation history to `tmzncty/computing-archaeology` rather than expanding Case 03 into a general semiconductor-memory history.

The contribution here is narrower: one named Intel device/controller pair now demonstrates that scheduled retention can depend on control state whose timing, coverage, and arbitration are **outside the payload-bearing DRAM state itself**.