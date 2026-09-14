# Deepening Record — 1970–1973 Magnetic-Core Temperature Compensation and Operating Margins

## Target case

[`cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md)

## Status

**`bounded deepening complete`**

This record closes one narrow item in Case 02's remaining evidence debt: **temperature dependence of a usable magnetic-core memory system**.

The purpose is not to claim a universal ferrite retention-vs-temperature law. The primary sources used here are later U.S. patents filed in 1970 and 1971, plus a 1973-filed Ampex counterexample. They show a narrower engineering fact: even when remanent core state does not require periodic refresh, the currents used to select, inhibit, read, and write cores can require temperature-dependent operating margins.

The bounded result is:

```text
remanent state survives at rest
    !=
fixed read/write current remains valid over all temperatures

payload retention
    !=
access-margin control
```

This is a later operating-margin deepening. It does not replace the 1950–1954 MIT evidence that grounds Case 02, and it is not evidence that Whirlwind used any of the compensation circuits described below.

---

## Why this slice matters

Case 02 already separates:

```text
quiescent retention
    != read invariance
    != whole-machine restart continuity
```

The temperature evidence adds another distinction:

```text
state remains physically magnetized
    !=
state can be safely and correctly accessed with one fixed electrical operating point
```

That distinction is easy to miss because `nonvolatile` sounds like a property of the storage element alone. In a coincident-current memory, however, useful retention also depends on preserving enough margin among several operations:

- selected switching;
- half-selected non-switching;
- inhibit cancellation;
- sense discrimination;
- restore/write completion.

Temperature can change the electrical conditions under which those relations remain valid without implying that the idle magnetic bit has spontaneously disappeared.

---

## Historical record

### H/P — 1970 Documentor Sciences patent: temperature changes the required inhibit relation

Henry M. Call filed U.S. Patent 3,626,393, **“Temperature Compensation Circuit for Magnetic Core Memories,”** on February 13, 1970. The patent describes a three-wire core memory in which one winding is time-shared for inhibit and sense functions.

The patent explicitly frames ambient-temperature change as an operating problem. In its description:

- an inhibit signal must counteract a coincident-current selection signal enough to prevent unwanted switching;
- the inhibit current must not be so large that it overcomes the intended setting current;
- the magnetic core's hysteresis characteristics change with temperature;
- at higher temperature, less current can be required to change the core state;
- therefore the inhibit current should also be reduced as temperature rises.

Its proposed solution uses the temperature-dependent resistance of the inhibit/sense winding and series resistance so that increasing temperature reduces inhibit current.

**Primary source:** Henry M. Call, U.S. Patent 3,626,393, filed 1970-02-13, issued 1971-12-07, Google Patents: <https://patents.google.com/patent/US3626393A/en>

The patent is evidence for a proposed compensation mechanism and for the engineering problem as articulated by the inventor. It is not by itself evidence of field deployment, shipment volume, or reliability statistics.

### H/P — Call's patent makes the margin relational rather than scalar

The useful engineering point is not merely that `temperature matters`. The patent's inhibit discussion expresses a **relation among currents and switching thresholds**.

A simplified reconstruction of the stated constraint is:

```text
inhibit current must be large enough
    to prevent an unwanted selected write

but

inhibit current must not be so large
    that intended setting current is defeated
```

As temperature changes the switching characteristics of the core, both sides of that window can move.

Therefore a fixed current value is not the retained object of interest. The relevant property is an **operating margin** among drive, inhibit, and switching behavior.

The phrase `operating margin` is an engineering reconstruction used by this repository; the patent itself discusses current relationships and temperature compensation.

### H/P — 1971 Hewlett-Packard patent: required drive current depends on temperature and activity

Robert J. Frankenberg filed Hewlett-Packard's U.S. Patent 3,750,119, **“Computer Memory Temperature Compensation,”** on October 20, 1971.

The patent describes magnetic core memories divided into core stacks and states that the necessary drive current varies with memory temperature. It also identifies two distinct heat contributions:

1. heat from computer circuitry outside the memory;
2. heat developed within the memory by current passing through it.

The source further says that a simple ambient-temperature scheme created particular difficulty when the memory had **cooled after not being used for a long period of time**.

Its proposed compensation scheme estimates average core-stack temperature from ambient temperature plus activity-related heating and adjusts the common memory power-supply drive current accordingly.

**Primary source:** Robert J. Frankenberg, U.S. Patent 3,750,119, filed 1971-10-20, issued 1973-07-31, assigned to Hewlett-Packard Company, Google Patents: <https://patents.google.com/patent/US3750119A/en>

Again, this is primary patent evidence for a proposed control arrangement and its stated problem, not proof that every HP core-memory product implemented this exact circuit.

### H/P — the HP source makes workload history part of the thermal operating condition

The HP patent says the temperature rise of each modeled resistor is proportional to current passing through the corresponding core stack and uses the combined ambient and activity-related temperature estimate to adjust drive current.

That gives a bounded historical witness for a useful distinction:

```text
recent memory activity
    -> thermal state
    -> required drive-current adjustment

recent memory activity
    != payload value itself
```

A stack that has been busy and a stack that has been idle for a long period can therefore present different electrical operating conditions even if the same logical data remain stored.

The source does not say that the data contents encode this thermal history, nor that the temperature estimator is a durable state variable. The thermal condition is an operating context that the controller senses or approximates.

### H/P — 1973 Ampex filing provides a bounded counterexample to “all core memory needs compensation”

Ampex filed U.S. Patent 3,905,026, **“Large, High Speed Two Dimensional Core Memory,”** on November 15, 1973. Its abstract and description propose highly temperature-stable cores plus tightly controlled large, short-duration drive pulses so that the memory can operate **without need for temperature compensation** over the intended design range.

The patent discusses commercial core types and treats temperature stability, drive-current magnitude, switching time, and disturb behavior as coupled design variables.

**Primary patent record:** U.S. Patent 3,905,026, filed 1973-11-15, issued 1975-09-09, Ampex Corporation. Preserved text: <https://www.freepatentsonline.com/3905026.html>

This source is useful as a negative control:

```text
some core-memory designs used or proposed compensation
    !=
temperature compensation is an invariant feature of all core memories
```

A design can instead spend material, pulse-shaping, timing, or current margin to reduce the need for active compensation.

This patent is later than the Case 02 grounding period and should not be projected backward into the Whirlwind implementation.

---

## Engineering reconstruction

### E — quiescent remanence and access admissibility are separate properties

Case 02's base mechanism is remanent magnetic state. The 1970–1973 compensation sources show that useful access requires another condition:

```text
stored polarity remains
    +
selection / inhibit / sense / restore margins remain valid
    ->
logical value can be accessed reliably
```

The first condition can hold while the second becomes marginal.

Therefore:

```text
retained physical state
    != guaranteed readable/writable service state
```

This does not imply a data-loss event. It identifies a boundary between **payload persistence** and **operational admissibility**.

### E — temperature compensation is maintenance of a relation, not refresh of the payload

The compensation schemes do not periodically rewrite all stored bits merely because time has passed. They adjust the conditions under which later read/write operations are performed.

That is technically different from DRAM refresh:

```text
core temperature compensation:
    adjust operating parameters so access remains within margin

DRAM refresh:
    actively restore decaying stored charge on a schedule
```

Both belong to `maintenance` only at a broad functional level.

### E — an access-margin controller need not preserve a durable history

The HP proposal senses or approximates the current thermal condition and adjusts the drive supply. The Call proposal exploits temperature-dependent resistance in the inhibit path.

Neither source requires a durable log of prior temperatures or prior current settings.

This is important for the repository's retained-state vocabulary:

```text
state required for reliable retention/service
    != state that itself must persist across power loss
```

Some control state can be **re-derived from present conditions** each time the powered system operates.

### E — cold after long idle can be an operating-transition problem without being forgetting

The HP source's `cooled after not being used for a long period of time` example is especially useful because it separates two questions that ordinary language can collapse:

1. did the magnetic cores keep their stored polarity while idle?
2. is the currently chosen drive current appropriate for the now-cool stack?

The source addresses the second problem. It does not report that cooling during idle erased the stored contents.

Therefore this repository should not write:

```text
memory cooled
    -> data decayed
```

The supported reconstruction is narrower:

```text
memory cooled
    -> operating point changed
    -> fixed drive assumption may be wrong
```

### E — thermal state is partly endogenous to maintenance and workload

The HP patent treats core-stack temperature as the combination of ambient conditions and self-heating caused by memory current.

This produces a feedback relation:

```text
memory activity
    -> heating
    -> changed switching/current requirement
    -> compensation
    -> continued reliable access
```

The physical medium is therefore not simply sitting in an externally imposed environment. The act of operating the memory helps create the environment in which later operations occur.

This is an engineering interpretation of the patent's thermal model, not terminology used by HP.

---

## Functional analogy

### A — relation to Case 03 DRAM refresh

Case 03 shows that DRAM's stored charge requires periodic restoration and that refresh-control state can live outside the array.

Case 02's temperature-compensation deepening is different:

```text
magnetic core:
    remanence can preserve payload while idle
    operating parameters may need temperature adaptation for access

DRAM:
    payload charge itself decays on the operating timescale
    scheduled refresh is part of preserving the payload
```

The bounded analogy is only that **payload state and the control conditions required to keep it usable are distinct**.

No historical genealogy is claimed.

### A — relation to Case 70 half-select disturbance

Case 70 already gives direct 1952 evidence that half-selected cores must tolerate repeated nonselecting excitation.

The temperature-compensation evidence adds a later system-level warning: switching and inhibit margins can move with temperature.

That does **not** provide a quantitative temperature coefficient for Papian's 1952 test cores and does not establish that the later three-wire systems used the same material or current geometry.

The relation is therefore:

```text
Case 70:
    disturbance tolerance as an early cell/array requirement

this deepening:
    later evidence that access/inhibit margins can be temperature-dependent
```

---

## Philosophical / media-theoretical boundary

A narrow conceptual observation is permitted:

> A technical state can remain physically present while the system temporarily lacks a safe operating point for observing or modifying it.

That helps separate `exists` from `is presently accessible under the normal protocol`.

The source material does not support a broader claim that information exists independently of every reading apparatus, nor does it establish a general philosophy of media. Those questions remain outside this evidence record.

---

## Explicit non-claims

This record does **not** claim that:

1. Whirlwind used Call's 1970 compensation circuit;
2. Whirlwind used HP's 1971 compensation scheme;
3. every magnetic-core memory required active temperature compensation;
4. temperature change necessarily erased an idle core bit;
5. a cooled core stack necessarily contained corrupted payload;
6. the cited patents prove production deployment or shipment volume;
7. Call's patent invented temperature compensation for core memory;
8. HP's patent invented temperature compensation for core memory;
9. the patents establish a universal temperature coefficient for ferrite cores;
10. all core materials had the same temperature dependence;
11. the Ampex design proves temperature effects disappeared physically;
12. compensation and refresh are the same mechanism;
13. workload-derived heat is itself user payload;
14. a temperature sensor or compensation current must be durable across power loss;
15. a patent's statement of prior-art difficulty is equivalent to an independently measured industry-wide failure rate.

---

## Claim ledger

| Claim | Label | Evidence | Strength / boundary |
| --- | --- | --- | --- |
| Call filed a 1970 patent specifically for temperature compensation in three-wire magnetic-core memory | `H/P` | US 3,626,393 | strong primary patent record |
| Call describes inhibit current as constrained by temperature-dependent switching behavior | `H/P` | US 3,626,393 description | strong for the proposed system; not deployment proof |
| HP filed a 1971 patent in which core-stack drive current depends on temperature and self-heating | `H/P` | US 3,750,119 | strong primary patent record |
| HP explicitly identifies difficulty after memory has cooled following long inactivity | `H/P` | US 3,750,119 description | strong for stated design problem |
| recent memory activity can affect thermal operating condition without being payload state | `E` | reconstructed from HP thermal model | bounded engineering reconstruction |
| retained remanence does not imply one fixed access current is valid under all conditions | `E` | Call + HP | strong bounded synthesis |
| Ampex proposed a later design intended to avoid temperature compensation through material and pulse-margin choices | `H/P` | US 3,905,026 | primary patent record / negative control |
| all magnetic-core memories need temperature compensation | `X` | contradicted by bounded Ampex counterexample and design variability | rejected universalization |
| temperature variation by itself proves payload forgetting | `X` | not supported by these sources | rejected overreach |

---

## Source hierarchy and custody

### Primary technical sources

1. Henry M. Call, **“Temperature Compensation Circuit for Magnetic Core Memories,”** U.S. Patent 3,626,393, filed 1970-02-13, issued 1971-12-07. <https://patents.google.com/patent/US3626393A/en>
2. Robert J. Frankenberg, **“Computer Memory Temperature Compensation,”** U.S. Patent 3,750,119, filed 1971-10-20, issued 1973-07-31, Hewlett-Packard Company. <https://patents.google.com/patent/US3750119A/en>
3. **“Large, High Speed Two Dimensional Core Memory,”** U.S. Patent 3,905,026, filed 1973-11-15, issued 1975-09-09, Ampex Corporation. Preserved text: <https://www.freepatentsonline.com/3905026.html>

The first two were inspected through full-text patent records. The Ampex patent is used only as a bounded counterexample to a universal compensation claim.

### Related repository routing

The repository already delegates broad magnetic-core engineering history, manufacturing labor, and Whirlwind adoption to:

- [`tmzncty/computing-archaeology/docs/memory/why-core-memory-was-worth-weaving.md`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md)
- [`tmzncty/computing-archaeology/experiments/core-memory/`](https://github.com/tmzncty/computing-archaeology/tree/main/experiments/core-memory)

A repository search did not surface an existing temperature-compensation note there, so this record keeps only the retention-specific boundary and does not build a broader controller/material genealogy.

---

## Remaining evidence debt

This slice closes the generic `temperature dependence` item in Case 02 only at the level of later primary patent evidence. It leaves narrower work:

1. inspect a named production core-memory service manual with page-level temperature-compensation circuitry and specified operating range;
2. obtain a period core-manufacturer datasheet or material paper with quantitative switching-current / temperature curves;
3. compare cold-start, warm steady-state, and high-temperature margins on one named system rather than across patents;
4. keep material genealogy and vendor history in `computing-archaeology` unless they directly change a retention claim;
5. do not infer a universal shelf-retention lifetime from access-margin temperature data.

The useful advance is therefore not `core memory has a temperature problem`. It is the narrower retained-state distinction:

```text
remanent payload state
    != thermal operating condition
    != drive / inhibit calibration
    != proof of successful access
```
