# Grounding Record — Micron 1991 Temperature-Dependent DRAM Refresh

## Status

**`grounded`** for the bounded retention claim in Case 34: a DRAM refresh cadence can be selected from measured temperature rather than held at one worst-case cadence, while the underlying dynamic-cell refresh obligation remains intact.

Case: [`../cases/34-micron-temperature-dependent-dram-refresh.md`](../cases/34-micron-temperature-dependent-dram-refresh.md).

This record deliberately separates three historical layers:

1. **earlier prior art** — a 1987-priority CardioData patent family already describes ambient-temperature-controlled DRAM refresh using a thermistor, processor A/D conversion, and a table;
2. **bounded Micron mechanism** — US5278796A, filed 12 April 1991, gives a particularly explicit sensor → comparator bands → encoder → oscillator → refresh-sequence design and discusses guardband/granularity/power tradeoffs;
3. **later comparison only** — US7035157B2, priority 2004, integrates temperature measurement and sampled/latching control into an explicitly named DRAM self-refresh circuit. It is not used to project later self-refresh semantics backward into the 1991 Micron design.

## Primary source A — Micron US5278796A

### Identity and date

- **Title:** `Temperature-dependent DRAM refresh circuit`
- **Inventors:** Charles W. Tillinghast; Michael S. Cohen; Thomas W. Voshell
- **Original assignee:** Micron Technology, Inc.
- **Application:** US07/684,422
- **Filing / priority:** 12 April 1991
- **Publication / grant:** 11 January 1994
- **Primary text:** <https://patents.google.com/patent/US5278796A/en>

### Historical vocabulary anchored by the source

The patent itself uses:

- `temperature-dependent DRAM refresh circuit`;
- `temperature compensated DRAM refresh`;
- `temperature sensor`;
- `comparators`;
- `encoder`;
- `oscillator`;
- `refresh counter and gate circuit`;
- `guardbanding`.

The project should preserve these words when making historical claims. `Environment-conditioned maintenance`, `measurement proxy`, and `retention envelope` are later reconstruction terms.

### Background relation: dynamic state, leakage, temperature, refresh

In the `BACKGROUND OF THE INVENTION`, Micron states that the need for refresh is basic to the DRAM storage technique: data are represented by capacitor charge, leakage requires periodic recharge/refresh, and refresh requirements are conventionally specified at the highest allowed operating temperature because leakage accelerates with temperature.

The patent then gives a period engineering rule of thumb relating refresh rate to temperature and motivates reducing refresh frequency at lower temperature to reduce memory power in portable systems.

**Evidence boundary:** the stated temperature multiplier is treated as a historical engineering assertion for the patent's technology context, not a universal law for all later DRAM generations.

### Mechanism path

The `SUMMARY OF THE INVENTION` and preferred embodiment establish the following path:

```text
DRAM-array temperature
    ↓
solid-state temperature sensor located near the array
    ↓
analog sensor voltage
    ↓
four comparators / five temperature bands
    ↓
priority encoder
    ↓
weighted resistor summing node
    ↓
RC oscillator frequency
    ↓
system logic / refresh counter and gate
    ↓
DRAM refresh sequence at a selected cadence
```

The patent says the sensor is in physical proximity to the DRAM array and its voltage therefore **reflects** DRAM temperature. That wording is important: it supports a proxy relation but not direct per-cell retention measurement.

The preferred embodiment switches comparators at 14 °C, 28 °C, 42 °C, and 56 °C to classify five bands. Its example refresh schedule is:

| Temperature band | Example refresh interval |
| --- | ---: |
| above 56 °C | 8 ms |
| 42–56 °C | 16 ms |
| 28–42 °C | 32 ms |
| 14–28 °C | 64 ms |
| below 14 °C | 128 ms |

The patent immediately limits the universality of these numbers: temperature ranges, number of ranges, and refresh rates may change with technology.

### Guardband and control-cost evidence

Micron says the embodiment uses 14 °C steps while describing a roughly 12 °C refresh-rate relation, and explicitly says the 14 °C steps allow `guardbanding`.

It also says that adding comparators can increase refresh-rate accuracy, but eventually the **power consumed by the temperature/control circuit exceeds the power saved by reducing refresh frequency**.

This directly supports two retention-specific distinctions:

- environment adaptation does not imply elimination of engineering margin;
- retention-optimization infrastructure has its own energy cost.

### Minimal embodiment

The patent also describes a single-comparator embodiment with only two possible refresh rates and calls its granularity gross/limited. This is useful evidence that the control representation is a discretization choice rather than a physical five-state property of DRAM retention.

## Primary source B — 1987-priority CardioData patent family

### Identity and bounded use

- **Family member inspected:** DE3827808A1, `DEVICE AND METHOD FOR THE SOLID STORAGE OF EPISODIC SIGNALS`
- **Inventors:** Mark Hubelbank; David Shadmon
- **Original assignee:** CardioData Corp.
- **Priority:** 14 August 1987
- **Publication:** 18 May 1989
- **U.S. family member cited by Micron:** U.S. Patent 4,920,489
- **Primary text:** <https://patents.google.com/patent/DE3827808A1/en>

The overall patent concerns solid-state storage of episodic signals, not DRAM refresh as a standalone invention. Its detailed storage embodiment nevertheless gives a clear earlier temperature-dependent DRAM-refresh mechanism.

The patent says a thermistor and resistor form a voltage divider, the processor digitizes that output through A/D conversion, and software/processor logic selects the DRAM refresh rate from a table using the measured value. It gives illustrative lower-temperature refresh periods and states that changing refresh rate with ambient temperature can reduce power without sacrificing the needed data-retention behavior.

Micron's 1991 patent independently describes U.S. Patent 4,920,489 in substantially the same mechanism terms and contrasts its own comparator/oscillator implementation with the earlier processor/table method.

### Prior-art consequence

This source blocks a Micron invention-priority claim:

> **Micron US5278796A is not evidence that Micron was first to condition DRAM refresh cadence on ambient temperature.**

The bounded historical value of the Micron patent is instead its explicit control path and tradeoff discussion.

## Primary source C — later temperature-dependent self-refresh boundary

### Identity

- **Patent:** US7035157B2, `Temperature-dependent DRAM self-refresh circuit`
- **Inventor:** Chien-Yi Chang
- **Original assignee:** Elite Semiconductor Memory Technology, Inc.
- **Priority:** 27 August 2004
- **Filing:** 14 September 2004
- **Grant:** 25 April 2006
- **Primary text:** <https://patents.google.com/patent/US7035157B2/en>

### Why it is included

This later patent explicitly describes:

- a temperature sensor;
- comparator / sampling and latching state;
- an encoder;
- a programmable oscillator;
- a temperature-dependent refresh signal;
- a sensor that can be switched to a low-power state during self refresh and periodically re-powered to detect temperature changes.

It also cites US5278796A among prior circuits that adjusted refresh using ambient temperature.

This source is **not** used to claim that Micron's 1991 circuit had the same self-refresh locus. Its role is to show that `temperature-conditioned cadence` and `self-refresh authority` are historically separable dimensions that could later be combined explicitly.

## Claim-to-source matrix

| Claim | Source | Strength / limit |
| --- | --- | --- |
| Micron filed a temperature-dependent DRAM refresh circuit patent in 1991 | US5278796A metadata | direct primary record |
| Micron's bounded design senses temperature near the DRAM array and converts it into comparator-defined bands | US5278796A summary + preferred embodiment | direct primary mechanism |
| Encoded band state controls an oscillator whose output drives a refresh sequence | US5278796A summary + detailed description | direct primary mechanism |
| The preferred embodiment gives five example cadence bands from 8 ms to 128 ms | US5278796A preferred embodiment | direct, but explicitly technology-specific |
| More measurement bands can improve refresh-rate accuracy but eventually consume more power than they save | US5278796A summary | direct tradeoff claim |
| A 1987-priority system already varied DRAM refresh with ambient temperature | DE3827808A1 / US4920489A family + Micron's own prior-art discussion | strong prior-art boundary; no Micron-first claim |
| The 1991 Micron design is an on-chip DRAM self-refresh circuit | none | **unsupported / rejected** |
| Temperature sensing directly measures every row/cell's actual retention time | none | **unsupported / rejected** |
| The 8/16/32/64/128 ms schedule applies universally to later DDR/DDR5 | none; Micron explicitly says technology may change the values | **rejected** |
| Later temperature-dependent self-refresh can sample/latch temperature and change oscillator timing | US7035157B2 | direct later primary record; comparison only |

## Engineering reconstruction enabled by the evidence

### 1. Retention obligation versus selected cadence

The source set allows the repository to separate the **need for periodic restoration** from the **frequency selected to satisfy that need under current environmental assumptions**.

A worst-case cadence can be a conservative policy for an environmental envelope; it is not identical to a temperature-independent physical decay constant.

### 2. Environment versus measured proxy versus policy state

The actual DRAM temperature, sensor voltage, comparator outputs, encoded band, oscillator state, and refresh sequence are different states and relations.

The protected payload can therefore depend on control state that does not contain the payload itself.

### 3. Guardband versus adaptation

Adaptive cadence does not logically imply zero margin. The Micron embodiment explicitly uses a discretized, guardbanded threshold structure.

### 4. Maintenance savings versus control overhead

The patent's comparator-count tradeoff makes the energy cost of retention infrastructure explicit. More exact maintenance control can itself become wasteful.

### 5. Environmental conditioning versus self-refresh locus

The 1991 Micron design and 2004–2006 self-refresh patent support a controlled comparison: the condition that modulates cadence and the place where recurring maintenance authority resides can evolve independently.

## Anti-anachronism and rejected claims

Do **not** write:

- `Micron invented temperature-compensated DRAM refresh`;
- `US5278796A is JEDEC temperature-compensated self refresh`;
- `the sensor measures cell retention time`;
- `DRAM retention always doubles every exactly 12 °C`;
- `five temperature bands are physical retention states`;
- `temperature compensation is per-row retention-aware refresh`;
- `lower refresh frequency means DRAM became less dependent on maintenance`.

Safe historical wording is narrower:

> By 1991, Micron filed a design that classified a nearby temperature sensor into discrete bands and used the encoded band to select oscillator/refresh cadence; its own patent acknowledged earlier ambient-temperature-driven DRAM refresh prior art.

## Cross-case consequences

Case 34 should be compared with the existing DRAM cases without merging their mechanisms:

- **Case 03:** physical reason refresh exists;
- **Case 09:** internal versus external refresh-row enumeration;
- **Case 10:** leakage-related proxy triggering an on-chip self-refresh sequence;
- **Case 21:** external AUTO REFRESH versus SELF REFRESH responsibility handoff;
- **Case 33:** bank/bank-group refresh target and service-blocking geometry;
- **Case 34:** environmental sensing and guardband policy change the selected cadence.

The resulting analytical chain is:

```text
payload decay
    !=
environmental condition
    !=
condition measurement
    !=
policy/guardband classification
    !=
refresh cadence
    !=
refresh authority
    !=
row enumeration
    !=
target geometry
    !=
restoration execution
```

## Related-repository check

Current GitHub code searches of `tmzncty/computing-archaeology` for:

- `temperature compensated refresh DRAM`;
- `temperature-dependent DRAM`;
- `adaptive DRAM refresh`;

returned no dedicated treatment to reuse. This case therefore retains only the retention-specific mechanism and comparison. A broad history of DRAM leakage physics, JEDEC TCSR/ASR semantics, LPDDR, or modern retention-aware scheduling should be routed to `computing-archaeology` if developed comprehensively.

## Remaining gaps

This record does **not** close:

- commercial-product use of the exact Micron circuit;
- a JEDEC standards genealogy for temperature-compensated self refresh;
- exact modern DDR/LPDDR temperature-band/timing semantics;
- sensor calibration or fault-injection evidence;
- row-to-row retention-time variation;
- modern per-row retention-aware refresh;
- RowHammer-oriented refresh policy;
- measured whole-system energy savings on a named product.

Those are separate bounded slices rather than reasons to overgrow Case 34.
