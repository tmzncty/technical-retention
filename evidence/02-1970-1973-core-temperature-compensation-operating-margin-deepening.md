# Deepening Record — 1970–1973 Magnetic-Core Temperature-Compensation Control Architectures

## Target case

[`cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md)

Related named-machine margin work: [`70-dec-pdp8e-1973-operating-margin-deepening.md`](70-dec-pdp8e-1973-operating-margin-deepening.md), including its later IBM 1800 cross-machine follow-on.

Earlier prior-art / access-control follow-on: [`02-1963-1972-core-thermal-control-prior-art-access-throttling-deepening.md`](02-1963-1972-core-thermal-control-prior-art-access-throttling-deepening.md). That record moves the inspected bibliographic floor back to the Kuhlmann / Olympia patent family and adds a separate Siemens activity-history / access-throttling architecture; it does not retroactively assign those mechanisms to the named machines here.

## Status

**`bounded deepening complete`**

This record does **not** reopen the already-closed named-machine operating-margin work in Case 70. Instead it asks a narrower prior-art question:

> Once temperature dependence was recognized in magnetic-core systems, what kinds of control architectures were proposed to keep selection / inhibit / drive relations inside a usable operating window, and was active temperature compensation universal?

The primary sources are later U.S. patents filed in 1970 and 1971, plus a 1973-filed Ampex counterexample. They show that remanent core state and the electrical conditions required to access that state are different things, while also showing that designers could attack temperature sensitivity in different places.

The bounded result is:

```text
remanent state survives at rest
    !=
fixed read/write current remains valid over all temperatures

payload retention
    !=
access-margin control

access-margin control
    !=
one universal compensation architecture
```

This is a later prior-art / control-architecture witness. It does not replace the 1950–1954 MIT evidence that grounds Case 02 and does not establish that Whirlwind used any circuit described below.

---

## Relationship to existing repository evidence

Case 70 already provides stronger **named production/service evidence** than the patents below: DEC's 1973 MM8-E manual exposes discrete current/slice/strobe settings plus thermistor-based temperature tracking, while its IBM 1800 follow-on supplies a second vendor/machine witness.

Accordingly, this file does not claim to close `temperature dependence` generically. Its contribution is different:

```text
Case 70
    -> named installed systems and service qualification

this record
    -> later proposed control architectures and a negative control
```

The broader material/vendor genealogy remains routed to `computing-archaeology`.

---

## Historical record

### H/P — 1970 Documentor Sciences patent: compensate the inhibit relation itself

Henry M. Call filed U.S. Patent 3,626,393, **“Temperature Compensation Circuit for Magnetic Core Memories,”** on February 13, 1970. The patent describes a three-wire core memory in which one winding is time-shared for inhibit and sense functions.

Its description says that:

- inhibit current must counteract a coincident-current selection signal enough to prevent unwanted switching;
- inhibit current must not become so large that it defeats the intended setting current;
- magnetic-core hysteresis characteristics change with temperature;
- at higher temperature less current can be required to switch a core;
- the inhibit current should therefore also be reduced as temperature rises.

The proposed circuit uses the temperature-dependent resistance of the inhibit/sense winding together with series resistance so that increasing temperature reduces inhibit current.

**Primary source:** Henry M. Call, U.S. Patent 3,626,393, filed 1970-02-13, issued 1971-12-07. <https://patents.google.com/patent/US3626393A/en>

The patent is primary evidence for the proposed mechanism and for the stated engineering problem. It is not evidence of field deployment, shipment volume, or an invention-priority claim.

### H/P — the Call source makes the margin relational

The important point is not merely `temperature matters`. The inhibit path must remain in a window:

```text
large enough
    to prevent an unwanted selected write

but not so large
    that intended setting is defeated
```

As temperature changes switching behavior, the appropriate relation among drive, inhibit, and switching threshold moves.

`Operating margin` is the repository's reconstruction of that relation; the patent itself speaks in terms of currents, hysteresis characteristics, and compensation.

### H/P — 1971 Hewlett-Packard patent: compensate ambient temperature plus activity heating

Robert J. Frankenberg filed Hewlett-Packard's U.S. Patent 3,750,119, **“Computer Memory Temperature Compensation,”** on October 20, 1971.

The patent states that the drive current required by a magnetic-core memory depends on memory temperature and identifies two heat sources relevant to that temperature:

1. heat from computer circuitry outside the memory;
2. heat produced inside the memory by current passing through it.

It also says that an ambient-only compensation method created particular difficulty after the memory had **cooled following a long period without use**.

Its proposed scheme places resistive elements in the memory-current paths and senses a thermal combination intended to represent ambient temperature plus average activity-related core-stack heating; the result controls the common drive-current supply.

**Primary source:** Robert J. Frankenberg, U.S. Patent 3,750,119, filed 1971-10-20, issued 1973-07-31, Hewlett-Packard Company. <https://patents.google.com/patent/US3750119A/en>

The patent is evidence for a proposed control arrangement and its stated problem, not proof that every HP core-memory product used the exact circuit.

### H/P — the HP source makes recent workload relevant to the operating condition

In the HP model:

```text
recent memory activity
    -> self-heating
    -> changed thermal operating condition
    -> changed drive-current requirement
```

But:

```text
recent memory activity
    != payload value
```

A stack that has recently been busy and one that has been idle can therefore require different electrical treatment even if both still physically retain the same logical data.

The patent does not describe a durable temperature history. The controller estimates a present condition and adapts current accordingly.

### H/P — 1973 Ampex filing supplies a negative control

Ampex filed U.S. Patent 3,905,026, **“Large, High Speed Two Dimensional Core Memory,”** on November 15, 1973. It proposes highly temperature-stable cores and tightly controlled large, short-duration drive pulses so that the intended memory can operate **without need for temperature compensation** over its design range.

The patent treats core material, drive magnitude, switching timing, temperature stability, and disturb behavior as coupled design choices.

**Primary patent record:** U.S. Patent 3,905,026, filed 1973-11-15, issued 1975-09-09, Ampex Corporation. Preserved text: <https://www.freepatentsonline.com/3905026.html>

This is useful negative evidence:

```text
some designs compensate a temperature-sensitive control path
    !=
all core memories require one temperature-compensation circuit
```

A designer can instead spend margin in material choice, pulse shaping, timing, thermal design, or some combination of those.

The Ampex filing is later than the Case 02 grounding period and is not projected backward into Whirlwind.

---

## Engineering reconstruction

### E — quiescent remanence and access admissibility are separate

Case 02's base mechanism is remanent magnetic state. The compensation sources add another condition:

```text
stored polarity remains
    +
selection / inhibit / sense / restore relations remain valid
    ->
logical value can be accessed reliably
```

Therefore:

```text
retained physical state
    != guaranteed readable/writable service state
```

This distinction does not itself imply a data-loss event. It separates **payload persistence** from **operational admissibility**.

### E — temperature compensation maintains a control relation, not the idle payload

The cited compensation schemes do not periodically rewrite every bit because time has passed. They alter operating parameters for later accesses.

That differs from DRAM refresh:

```text
magnetic-core compensation:
    adapt access currents / margins

DRAM refresh:
    restore decaying payload charge on a schedule
```

They can both be discussed as maintenance only at a high functional level.

### E — control state can be regenerated from present conditions

The HP proposal senses or approximates current thermal condition. The Call proposal exploits temperature-dependent circuit resistance.

Neither requires a durable log of old temperature samples or old compensation settings.

So:

```text
state required for reliable service
    != state that itself must survive power loss
```

A control relation can be reconstructed from present physical conditions after restart.

### E — `cold after idle` is an operating transition, not evidence of forgetting

The HP source's long-idle example must not be rewritten as:

```text
memory cooled
    -> stored bits decayed
```

The supported claim is narrower:

```text
memory cooled
    -> operating point changed
    -> a fixed drive assumption can become inappropriate
```

The payload can remain magnetized while the surrounding drive system needs a different operating point.

### E — workload helps create the environment in which later accesses occur

The HP source treats self-heating as a function of memory current. This gives a feedback relation:

```text
memory activity
    -> heat
    -> changed switching/current requirement
    -> compensation
    -> continued reliable access
```

That is a repository reconstruction of the patent's thermal model, not HP's own conceptual vocabulary.

---

## Functional comparisons

### A — Case 70: service qualification versus control-architecture prior art

Case 70's DEC and IBM material is the stronger source when the question is **what a named installed machine actually exposed to production/service personnel**.

This file is stronger only for a different question: **what compensating architectures inventors were proposing and how those architectures differed**.

Therefore:

```text
patent problem/architecture record
    != installed-machine service record
```

Neither should substitute for the other.

### A — Case 03 DRAM refresh

Case 03 shows that stored charge itself requires periodic restoration. Core compensation instead preserves a safe access relation around an otherwise remanent payload.

The bounded analogy is only:

```text
payload state
    != control conditions required to keep that payload usable
```

No historical genealogy is claimed.

### A — Case 70 half-select disturbance

Papian/Case 70 establishes early disturbance tolerance as a cell/array requirement. The later temperature-compensation sources show that switching/inhibit relations can also depend on temperature.

They do not provide a temperature coefficient for Papian's 1952 cores, do not identify the same material, and do not prove direct influence.

---

## Philosophical boundary

One narrow interpretation is allowed:

> A technical state can remain physically present while the system temporarily lacks the correct normal operating point for observing or modifying it.

This separates `exists` from `is presently accessible under the intended protocol`.

The sources do not establish a general philosophy of information or an apparatus-independent ontology of stored state.

---

## Explicit non-claims

This record does **not** claim that:

1. Whirlwind used Call's 1970 circuit;
2. Whirlwind used HP's 1971 scheme;
3. every magnetic-core memory required active temperature compensation;
4. temperature change necessarily erased an idle core bit;
5. a cooled stack necessarily contained corrupted payload;
6. the cited patents prove production deployment;
7. Call or HP invented core-memory temperature compensation;
8. the patents establish a universal ferrite temperature coefficient;
9. all core materials had the same temperature dependence;
10. Ampex eliminated every physical temperature effect;
11. compensation and refresh are the same mechanism;
12. workload-derived heat is user payload;
13. a temperature sensor or compensation current must be durable across power loss;
14. patent discussion of prior-art difficulty is an industry-wide measured failure rate;
15. this file supersedes Case 70's stronger named-machine quantitative margin evidence.

---

## Claim ledger

| Claim | Label | Evidence | Strength / boundary |
| --- | --- | --- | --- |
| Call filed a 1970 patent specifically for temperature compensation in a three-wire magnetic-core memory | `H/P` | US 3,626,393 | strong primary patent record |
| Call describes inhibit current as constrained by temperature-dependent switching behavior | `H/P` | US 3,626,393 | strong for proposed system; not deployment proof |
| HP filed a 1971 patent in which drive current depends on temperature and self-heating | `H/P` | US 3,750,119 | strong primary patent record |
| HP explicitly identifies difficulty after memory cooled following long inactivity | `H/P` | US 3,750,119 | strong for stated design problem |
| recent activity can affect thermal operating condition without being payload state | `E` | HP thermal model | bounded reconstruction |
| retained remanence does not imply one fixed access-current relation works under all conditions | `E` | Call + HP, consistent with Case 70 | bounded synthesis |
| Ampex proposed a later design intended to avoid active temperature compensation through material/pulse choices | `H/P` | US 3,905,026 | bounded primary patent counterexample |
| all core memories need one active temperature-compensation architecture | `X` | contradicted by design variability / Ampex counterexample | rejected universalization |
| temperature variation alone proves payload forgetting | `X` | unsupported | rejected overreach |

---

## Source hierarchy

### Primary technical sources

1. Henry M. Call, **“Temperature Compensation Circuit for Magnetic Core Memories,”** U.S. Patent 3,626,393, filed 1970-02-13, issued 1971-12-07. <https://patents.google.com/patent/US3626393A/en>
2. Robert J. Frankenberg, **“Computer Memory Temperature Compensation,”** U.S. Patent 3,750,119, filed 1971-10-20, issued 1973-07-31, Hewlett-Packard Company. <https://patents.google.com/patent/US3750119A/en>
3. **“Large, High Speed Two Dimensional Core Memory,”** U.S. Patent 3,905,026, filed 1973-11-15, issued 1975-09-09, Ampex Corporation. Preserved patent text: <https://www.freepatentsonline.com/3905026.html>

The first two were inspected through full-text patent records. The third is used only as a bounded negative control to a universal compensation claim.

### Existing repository evidence deliberately not duplicated

- [`70-dec-pdp8e-1973-operating-margin-deepening.md`](70-dec-pdp8e-1973-operating-margin-deepening.md) — DEC MM8-E named-machine quantitative margin evidence and IBM 1800 follow-on;
- [`70-papian-1952-half-select-disturbance-facsimile-deepening.md`](70-papian-1952-half-select-disturbance-facsimile-deepening.md) — direct 1952 half-select disturbance facsimile inspection;
- [`02-magnetic-core-1951-1954-grounding.md`](02-magnetic-core-1951-1954-grounding.md) — main Case 02 historical grounding.

### Related repository routing

Broad core-memory engineering, manufacturing labor, and Whirlwind adoption remain in:

- <https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md>
- <https://github.com/tmzncty/computing-archaeology/tree/main/experiments/core-memory>

A repository search did not surface a dedicated temperature-compensation history there, so this record keeps only the retention-specific control-architecture boundary rather than building a general genealogy.

---

## Remaining evidence debt

The earlier Kuhlmann debt is now split instead of left as one vague task. [`02-1963-1972-core-thermal-control-prior-art-access-throttling-deepening.md`](02-1963-1972-core-thermal-control-prior-art-access-throttling-deepening.md) closes the **bibliographic chronology / later-citation** part: the Olympia family has a 1963 priority, a 1966 German publication, and the 1967 U.S. Kuhlmann record is cited by multiple later magnetic-memory patents. What remains is implementation-level evidence.

Useful next work would be:

1. recover and directly inspect a full Kuhlmann / Olympia specification or national-family facsimile, then determine whether a named Olympia machine can be tied to that mechanism without inferring deployment from assignment alone;
2. inspect period core-manufacturer material data with quantitative switching-current / temperature curves;
3. compare compensation architectures against named machine manuals without turning chronological compatibility into genealogy;
4. leave vendor/material genealogy in `computing-archaeology` unless it changes a retention claim;
5. do not infer a shelf-retention lifetime from access-margin temperature data.

The retained-state distinction established here is therefore:

```text
remanent payload state
    != thermal operating condition
    != drive / inhibit calibration relation
    != proof of successful access
```
