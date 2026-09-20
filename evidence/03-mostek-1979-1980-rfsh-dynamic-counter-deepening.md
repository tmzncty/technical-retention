# Case 03 Deepening — Mostek MK4164 RFSH and a Dynamic Refresh Counter, 1979–1980

**Status:** `bounded deepening complete`

## Research question

Case 03 already distinguishes the DRAM payload from the control state used to preserve it. Existing evidence covers external refresh timers/counters, the late-1970s MK4116 `RAS-only` deadline/coverage contract, Intel's later controller state, and 1980s CAS-before-RAS devices that move refresh-address generation on-chip.

This slice asks one narrower prior-art question:

> By 1979–1980, did a commercial DRAM vendor already document an on-chip refresh counter, and what did that documentation say about the counter's own retention requirements?

Mostek's MK4164 documentation supplies an unusually useful answer. A 1979 product brief already advertises an `On chip refresh counter on pin 1`. The 1980 *Memory Data Book and Designers Guide* then describes the `RFSH` path in detail and states that the internal refresh counter is itself **dynamic** and requires refreshing; the same recurrent RFSH activity used to maintain the memory array is adequate to maintain that counter.

The bounded result is therefore:

```text
state being maintained
    !=
state coordinating maintenance

but

maintenance-control state
    can itself require maintenance
```

This is a documentation/prior-art floor, not an invention-priority claim and not proof of first commercial shipment.

---

## Why this slice is not a duplicate

The earlier Case 03 Mostek deepening, [`03-mostek-1977-1979-ras-only-refresh-deepening.md`](03-mostek-1977-1979-ras-only-refresh-deepening.md), is about the MK4116 and closes a different relation:

```text
ordinary access can earn row-refresh credit
    !=
refresh is access-triggered

RAS-only refresh
    !=
self-refresh

reduced-power standby
    !=
maintenance-free retention
```

The 1984–1988 CAS-before-RAS deepening, [`03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md`](03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md), establishes a later product/period distinction between on-chip **coverage state** and autonomous **cadence generation**.

The present slice changes the chronology and adds a different mechanism boundary:

1. public Mostek documentation places an **on-chip refresh counter** at least as early as 1979;
2. the 1980 MK4164 text explicitly says that this counter is a **dynamic counter**;
3. its own retained state therefore depends on recurrent refresh activity;
4. despite internalizing refresh-address progression, the device still needs externally asserted `RFSH` events to advance and exercise the mechanism.

So this file does not repeat the MK4116 story and does not erase the later TI/NEC evidence. It supplies an earlier vendor-primary prior-art floor plus a direct example of **maintenance of maintenance-control state**.

---

## Source custody and dating

### Primary vendor anchor — Mostek 1979 product brief

Mostek's *1979 Memory Data Book and Designers Guide* contains a `PRODUCT BRIEF` for the `MK4164(J/N)-12`, described as a 65,536 × 1-bit dynamic RAM. Its feature list includes:

- `128 cycle refresh (2ms)`;
- `On chip refresh counter on pin 1`;
- a single +5 V supply;
- low standby power;
- page mode and read/write capabilities.

Archival scans / indexed copies:

- Bitsavers: <https://www.bitsavers.org/components/mostek/_dataBooks/1979_Mostek_Memory_Data_Book_and_Designers_Guide.pdf>
- alternate indexed scan: <https://electronicsandbooks.com/edt/manual/Electronic%20Component%20Databook%20Datasheet/Brand/Mostek%20%28SGS%29/Databook/1979%20Mostek%20Memory%20Data%20Book%20and%20Designers%20Guide%20c20130806%20%5B494%5D.pdf>

**Evidence boundary:** the page is explicitly a product brief. It establishes public Mostek technical vocabulary and a documentation floor. It does not by itself establish first shipment, production volume, invention priority, or the detailed transistor-level implementation of the counter.

### Primary vendor mechanism anchor — Mostek 1980 data book

Mostek's *1980 Memory Data Book and Designers Guide* contains a detailed MK4164(N/E)-12/15 entry. Surviving scans are available through archival mirrors; the indexed extract used here identifies the source as that 1980 Mostek data book.

- full data-book mirror: <https://bitsavers.trailing-edge.com/components/mostek/_dataBooks/1980_Mostek_Memory_Data_Book_and_Designers_Guide.pdf>
- alternate full scan: <https://manuals.plus/m/3ff276e731a5bdb7be47c07dad25c5a0e24fcb583cdb0ae2a21867886ba8d7d9.pdf>
- indexed MK4164 extract identifying the 1980 Mostek source: <https://www.crocoware.com/wp-content/uploads/pdf/Mostek-MK4164E-12.pdf>

The detailed text describes pin 1 as `RFSH`. When `RFSH` is brought low while RAS is inactive, an on-chip refresh counter is enabled and an internal refresh operation occurs. When `RFSH` returns high, the internal refresh-address counter is incremented for the next refresh cycle.

The same page then makes the crucial statement for this case: the **internal refresh counter is a dynamic counter and requires refreshing**. It says that the 128 RFSH cycles every 2 ms already required to refresh the memory cells are adequate for that purpose, and that only RFSH-activated cycles affect the internal counter.

The document further says that using the RFSH mode removes the need to generate refresh addresses externally and permits address, CAS, and WRITE drivers to be powered down during battery-backup standby operation.

### Contemporaneous product-plan corroboration — Mostek 1980 product guide

Mostek's 1980 *Circuits and Systems Product Guide* lists the MK4164(J/N)-10/12 as `Available Soon` and describes:

- 128-cycle / 2 ms refresh through conventional RAS-only or pin-1 (`RFSH`) refresh;
- pin-1 refresh as reducing refresh-support hardware;
- low-power battery-backup operation.

Archive:

- <https://www.bitsavers.org/components/mostek/_dataBooks/1980_Mostek_Circuits_and_Systems_Product_Guide.pdf>

This source is useful precisely because it blocks an overclaim: in that product guide the device is still presented as `Available Soon`. Accordingly, this record uses 1979–1980 as a **public documentation / product-plan floor**, not as a proven shipping date.

---

## Historical record

### H/P — Mostek publicly names an on-chip refresh counter by 1979

The 1979 product brief uses the explicit feature wording:

```text
On chip refresh counter on pin 1
```

This moves the public-documentation floor for Case 03's on-chip refresh-counter concept earlier than the 1984–1988 TI/NEC material currently used to demonstrate the later CAS-before-RAS/self-refresh distinction.

The safe historical conclusion is narrow:

> **Mostek publicly documented an MK4164 on-chip refresh counter in a 1979 product brief.**

It does not follow that Mostek invented the idea, shipped it first, or that every 64K DRAM used the same organization.

### H/P — `RFSH` internalizes refresh-address progression, not refresh cadence

The 1980 MK4164 description says that asserting pin-1 `RFSH` during RAS-inactive time enables the on-chip refresh counter and causes an internal refresh operation. Returning `RFSH` high increments the internal refresh-address counter for the next cycle.

The documented division of labor is therefore:

```text
external system:
    decides when to assert RFSH

MK4164:
    uses internal counter state to select refresh address
    performs internal refresh
    increments internal counter after the RFSH cycle
```

This is a direct historical counterexample to:

```text
on-chip refresh counter
    =
self-refresh
```

The counter internalizes address/coverage progression; it does not eliminate the external recurrence that invokes each `RFSH` cycle.

### H/P — the refresh counter is itself documented as dynamic state

The most important sentence in the 1980 MK4164 entry is not merely that a counter exists. Mostek explicitly says the **internal refresh counter is a dynamic counter and requires refreshing**.

The vendor then states that the recurrent RFSH cycles already needed by the memory cells are adequate to keep the counter refreshed.

That gives a rare period product-level relation in which the state required to preserve payload is itself explicitly retention-dependent:

```text
DRAM cell charge
    requires refresh

internal refresh-address counter state
    also requires refresh
```

The source does not expose the counter's transistor topology or its exact decay time independently of the specified RFSH cadence, so this record makes no such claim.

### H/P — the same recurrence maintains two different retained relations

The MK4164 documentation says that 128 RFSH activations every 2 ms are required when RFSH refresh is used for the memory cells, and that this activity is also adequate to refresh the dynamic internal counter.

That does **not** mean payload bits and counter bits are the same state. It means one recurrent interface activity can close two distinct maintenance obligations:

```text
RFSH recurrence
    -> refresh target DRAM row
    -> keep internal dynamic counter viable
    -> advance refresh-address progression
```

The array payload and the controller's coverage state remain semantically different even when one maintenance stream supports both.

### H/P — battery-backup standby preserves a minimum refresh apparatus, not full service

The 1980 entry says that when RFSH refreshing is used, address drivers, CAS drivers, and WRITE drivers may be powered down during battery-backup standby operation.

This continues the boundary already visible in the MK4116 evidence, but with a changed locus of refresh-address generation:

```text
MK4116 bounded standby witness:
    keep external timing/address refresh support alive

MK4164 RFSH witness:
    refresh-address progression can reside on-chip
    while external RFSH recurrence still has to remain
```

The important point is not that the MK4164 is `nonvolatile`; it is not. The standby path reduces the apparatus needed for retention while preserving the recurrence required to keep dynamic state viable.

---

## Engineering reconstruction

### E — maintenance-control state can be subject to the same broad failure class as payload

Case 03 already separates:

```text
payload state
    !=
refresh-control state
```

The MK4164 adds a second-order qualification:

```text
refresh-control state
    !=
maintenance-free state
```

A control structure can be logically distinct from the data it protects while still being physically dynamic and therefore retention-dependent.

This is not a paradox once the layers are kept separate. `Control state` names a role in the maintenance relation, not a promise about the substrate used to implement it.

### E — internalization changes location of authority without eliminating dependency

The RFSH mode removes externally generated refresh addresses, but the external system still supplies the event that activates the internal refresh path.

A useful decomposition is:

```text
refresh deadline obligation
    !=
refresh invocation / cadence
    !=
refresh-address / coverage state
    !=
restore execution
```

For the bounded MK4164 RFSH path:

```text
cadence / invocation       -> still external
coverage position          -> on-chip dynamic counter
restore execution          -> on-chip DRAM circuitry
```

Moving one state boundary into the package is therefore not equivalent to moving every maintenance responsibility into the package.

### E — a maintenance dependency can be recursive without being infinite

Because the refresh counter needs refresh, a loose description might suggest an infinite regress: if maintenance control needs maintenance, what maintains the maintainer?

The product contract gives a concrete answer. The same RFSH recurrence that services the array is sufficient for the counter. There is no need to posit an additional independent maintenance scheduler for the counter in the documented interface.

So the engineering structure is not:

```text
counter needs counter needs counter ...
```

but:

```text
externally recurrent RFSH event
    -> services array retention
    -> exercises / refreshes dynamic counter
    -> advances next-row state
```

The recurrence closes both obligations at one interface boundary.

### E — retained-control correctness still differs from retained-control existence

The source establishes that the counter needs refresh and is incremented through RFSH operation. It does not establish that every surviving counter state is necessarily correct, nor does it expose independent integrity checking for the counter.

Therefore:

```text
counter state physically survives
    !=
counter state is correct
    !=
full row coverage is proved
```

This keeps the new result compatible with the later Intel 8202A TEST-mode evidence, where maintenance-control state can be disturbed before payload loss becomes visible.

### E — standby reveals a minimum retention apparatus

The MK4164 battery-backup statement identifies logic that may be removed from the active set while the retained relation is still maintained. In the documented RFSH regime:

- normal address drivers may be powered down;
- CAS drivers may be powered down;
- WRITE drivers may be powered down;
- an external recurrence still has to assert RFSH;
- the chip's internal refresh path and counter remain active enough to maintain the dynamic state.

This yields:

```text
apparatus needed for full random-access service
    !=
apparatus needed for retention-only standby
```

The source does not quantify a universal minimum-retention power tree for all MK4164 systems, so the conclusion remains interface-level.

---

## Functional comparisons — not genealogy

### A — earlier MK4116 RAS-only standby

The MK4116 evidence shows that a DRAM system can stop ordinary useful service while keeping external RAS timing and refresh-address logic alive.

The MK4164 RFSH path can move the refresh-address counter on-chip and thereby reduce external standby logic.

Controlled functional comparison:

```text
same broad retention obligation
    +
different placement of coverage state
```

This does not establish a complete MK4116 -> MK4164 circuit genealogy beyond Mostek's own product-brief description of the MK4164 as a successor generation.

### A — later TI CAS-before-RAS and NEC self-refresh

The 1984–1988 Case 03 evidence remains valuable because it gives a later, different command sequence and a period-authored distinction between an on-chip refresh counter and timer-backed self-refresh.

The new prior-art correction is chronological only:

```text
on-chip refresh-counter documentation
    exists by Mostek 1979

therefore

1984–1988 TI/NEC evidence
    must not be treated as the first public appearance of the concept
```

The later sources still provide different evidence about CAS-before-RAS semantics and autonomous cadence generation.

No direct Mostek -> TI or Mostek -> NEC genealogy is asserted.

### A — Case 21 self-refresh handoff

Case 21's much later SDRAM/LPDDR evidence treats self-refresh as a regime in which the device owns internal recurring maintenance while ordinary external service is suspended.

The MK4164 is a useful counterexample to collapsing internal address state into that later autonomy:

```text
on-chip row progression
    !=
on-chip recurrence generation
```

This is a functional comparison across different interface generations, not historical continuity.

### A — Synthesis 26 maintenance-control persistence horizons

Synthesis 26 distinguishes maintenance-control states by persistence horizon and reconstruction behavior. The MK4164 supplies an early concrete device-level witness for one special class:

```text
regime-local maintenance-control state
    physically dynamic
    maintained only while the recurrence regime continues
```

The synthesis vocabulary is modern project analysis. Mostek did not describe its counter in those terms.

---

## Philosophical interpretation — bounded

### I — preservation can depend on preserving the machinery of preservation

The exact technical fact is simple: the array is dynamic, and Mostek says the internal counter used for refresh is dynamic too.

A bounded interpretation is therefore:

> some technical retention regimes preserve not only their payload but also a transient state that tells the system how to continue preserving that payload.

This does not support a universal `all persistence is self-maintenance` thesis. Magnetic remanence, passive positional state, and other repository counterexamples remain decisive.

### I — internalization is not autonomy

The MK4164 also gives a clean check on a common language drift. A function can become hidden inside a package without the package becoming independent of external temporal support.

The bounded interpretive distinction is:

```text
less visible maintenance state
    !=
less dependent retention relation
```

Again, this is project interpretation downstream of the documented interface, not historical Mostek terminology.

---

## Prior-art correction

Before this slice, Case 03's strongest explicit on-chip refresh-counter witness was the later 1984–1988 TI/NEC material.

The 1979 Mostek product brief requires the novelty boundary to move earlier:

```text
by 1979:
    public Mostek documentation already names
    an on-chip refresh counter on the MK4164

by 1980:
    detailed Mostek documentation says
    the internal counter is dynamic and requires refreshing
```

What remains **unproved** is equally important:

- first invention of an on-chip DRAM refresh counter;
- first silicon implementation;
- first customer shipment;
- exact internal circuit topology;
- actor-to-actor influence from Mostek into TI, NEC, Samsung, or JEDEC practice.

Those are genealogy questions for a later archival slice, preferably coordinated with `tmzncty/computing-archaeology` rather than reconstructed speculatively here.

---

## Explicit non-claims

This evidence does **not** claim that:

1. Mostek invented DRAM refresh;
2. Mostek invented the on-chip refresh counter;
3. 1979 is the first implementation date of an on-chip refresh counter;
4. the 1979 product brief proves volume shipment;
5. the 1980 `Available Soon` product-guide wording proves earlier shipment;
6. every MK4164 revision had identical refresh behavior;
7. every device sold under a `4164` number used the Mostek refresh organization;
8. `RFSH` is identical to later CAS-before-RAS refresh;
9. `RFSH` is identical to self-refresh;
10. an on-chip counter implies an on-chip refresh timer;
11. internal refresh-address generation implies autonomous cadence generation;
12. a dynamic refresh counter has the same circuit topology as the DRAM cell array;
13. the counter's retention time equals one DRAM cell's retention time;
14. the counter cannot fail except through charge leakage;
15. 128 RFSH activations prove correct row coverage if the counter is already wrong;
16. refreshing the counter proves the counter's logical state is correct;
17. battery-backup standby makes the DRAM nonvolatile;
18. battery-backup standby means every external circuit may be turned off;
19. powering down address/CAS/WRITE drivers proves zero useful-service capability of every system design;
20. reduced standby apparatus means maintenance has disappeared;
21. Mostek's successor-language proves a complete MK4116 -> MK4164 circuit genealogy;
22. Mostek influenced the later TI or NEC designs used elsewhere in Case 03;
23. TI/NEC first disclosed on-chip refresh counting in 1984;
24. the present documentation floor is an invention-priority result;
25. a product brief is equivalent to a final production datasheet;
26. a public interface description exposes every hidden maintenance state;
27. `dynamic counter` is modern project vocabulary rather than Mostek's own wording;
28. maintaining control state is the same thing as maintaining payload identity;
29. a retained maintenance-control state is automatically authoritative or correct;
30. the bounded engineering relation establishes a universal philosophy of technical memory.

---

## Resulting bounded distinctions

```text
payload state
    !=
maintenance-control state

maintenance-control state
    !=
maintenance-free state

on-chip refresh-address counter
    !=
on-chip refresh timer

internal coverage progression
    !=
autonomous cadence

RFSH recurrence
    can maintain array state
    + maintain dynamic counter viability
    + advance coverage state

one maintenance stream
    !=
one retained object

counter survives
    !=
counter correct
    !=
coverage proved

battery-backed retention-only standby
    !=
full random-access service

1979 public product brief
    !=
first invention
    !=
first shipment
```

---

## Open work deliberately left outside this slice

1. locate earlier Mostek engineering papers, patents, or internal chronology for the pin-1 refresh design;
2. determine the earliest verified silicon / customer-shipment date for MK4164 RFSH capability;
3. inspect whether earlier 64K DRAM proposals from other vendors already contained an internal refresh counter;
4. reconstruct the exact MK4164 counter circuit only if primary circuit evidence becomes available;
5. test whether particular surviving MK4164 devices preserve/lose counter phase under controlled interruption of the RFSH cadence;
6. compare vendor-specific 64K DRAM refresh organizations without assuming that the `4164` label implies one geometry;
7. keep broader semiconductor-memory product genealogy in `tmzncty/computing-archaeology` and link it here if that repository later develops the topic.

---

## Bounded conclusion

Mostek's 1979 MK4164 product brief already publicly names an **on-chip refresh counter**. Its 1980 data-book description goes further: pin-1 `RFSH` invokes internal refresh and advances the internal refresh-address counter, while the counter itself is explicitly described as **dynamic** and as requiring refresh. The same recurrent RFSH activity that maintains the DRAM array is said to be adequate for maintaining the counter.

The resulting Case 03 refinement is not merely that refresh control moved on-chip earlier than the later TI evidence. It is that, in this documented design, the **state coordinating retention is itself a retained state with a maintenance requirement**.

That gives a clean historical-engineering boundary:

```text
state that preserves
    can itself need preservation

and

internalized maintenance state
    !=
autonomous maintenance schedule
```

Case 03 remains `grounded`; this deepening changes the prior-art floor and control-state decomposition, not the case's maturity level.