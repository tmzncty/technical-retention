# Case 70 evidence index — magnetic-core half-select disturbance and operating margin

**Case:** 70 — coincident-current magnetic-core half-select disturbance  
**Canonical case:** [`../cases/70-magnetic-core-half-select-disturbance.md`](../cases/70-magnetic-core-half-select-disturbance.md)  
**Current maturity:** `grounded`  
**Purpose:** navigation only; this file does not promote maturity or replace the canonical case.

---

## 1. Scope

Case 70 isolates a narrow retention problem inside magnetic-core memory:

> a logically unselected core can still be physically excited, and a bit that remains in the correct remanent state can still participate in a disturbed shared-sense event.

The canonical case already grounds four distinct historical/engineering layers:

1. **retained-state margin under repeated nonselecting excitation**;
2. **shared-sense disturbance from half-selected cores**;
3. **inhibit control / write authorization**;
4. **production and service operating-margin qualification** in later named systems.

The wider history of core-memory manufacture, weaving, destructive read, coincidence-current architecture, and product context belongs in the companion repository rather than being duplicated here:

- [`tmzncty/computing-archaeology — why core memory was worth weaving`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md)

---

## 2. Canonical evidence chain

The canonical Case 70 currently uses the following source families.

### A. 1951 Forrester multicoordinate-storage evidence

**Role:** historical mechanism grounding.

Supports the period distinction between:

```text
one coordinate excitation
    -> partial change / below stable-state transition threshold

coincident coordinate excitation
    -> selected stable-state transition
```

Retention relevance:

```text
logical nonselection
    !=
zero physical excitation
```

### B. 1952 Papian nonselecting-disturbance experiments

**Role:** historical material / repeated-disturbance grounding.

Papian's period vocabulary includes nonselecting disturbances, information-retention ratio, and signal ratio. This is the core historical witness that resistance to repeated sub-selection excitation was treated as an explicit quantitative design problem rather than a later metaphor.

Retention relevance:

```text
non-target excitation history
    can consume physical state / signal margin
```

### C. 1954-filed IBM Bauer/Haynes disturbance-cancellation evidence

**Role:** historical readout-path grounding.

Supports a second disturbance channel:

```text
half-selected-core outputs
    -> shared sense winding
    -> disturbed one/zero discrimination
```

This must remain separate from permanent payload corruption:

```text
sense disturbance
    !=
stable-state corruption
```

The same source family also grounds the distinction between word selection and per-bit inhibit authorization.

### D. 1970–1974 named-machine service / operating-margin evidence

**Role:** later production/service witness.

IBM 1800 and DEC MM11-S / PDP-8/E MM8-E / MF11-U/UP material show that practical core-memory reliability still depended on operating margins involving current, timing/strobe, temperature tracking, inhibit behavior, and diagnostic/service procedures.

This later material should not be projected backward as proof that every early core plane used the same service regime.

---

## 3. New deepening: Olsen/Best 1959–1964 drive-source architecture

### File

- [`70-olsen-best-1959-1964-core-drive-margin-prior-art-deepening.md`](70-olsen-best-1959-1964-core-drive-margin-prior-art-deepening.md)

### Primary source

Kenneth H. Olsen and Richard L. Best, **“Magnetic core memory,” US3161861A**, assigned to Digital Equipment Corporation; filed **1959-11-12**, published/granted **1964-12-15**.

### What it adds

The new slice does not add another general core-memory history. It adds a **driver-circuit layer** to the existing half-select margin model.

The patent treats reliable magnetic switching as depending on reproducible electrical excitation and describes a drive arrangement using:

- a substantially constant / regulated voltage source;
- low-impedance switching;
- deliberately larger series impedance/resistance;
- peak-current control through source-voltage / resistance relation;
- rise-time control involving the series element and conductor inductance.

The bounded retention relation is:

```text
coincident-current addressing rule
    !=
proof that the delivered electrical pulse is correct

source / switch / line / series-impedance behavior
    -> delivered pulse amplitude and waveform
    -> selected / half-selected magnetic margin
    -> recoverable retained state
```

### New boundary strengthened

```text
logical address selection
    !=
physical excitation correctness
```

and:

```text
architectural sensitivity reduction
    !=
calibration elimination
```

The evidence does **not** establish that a particular later DEC memory product used the exact patent topology.

---

## 4. Evidence-layer separation

### Historical record

Period sources establish that engineers explicitly cared about:

- partial / coincident excitation;
- resistance to nonselecting disturbances;
- disturbance signals in shared sensing;
- inhibit pulses;
- reproducible current/pulse generation;
- later service-level operating margins.

### Engineering reconstruction

Repository reconstruction separates:

```text
half-select state margin
selected-switching margin
sense-discrimination margin
pulse-amplitude margin
pulse-waveform / timing margin
```

These interact but are not interchangeable.

A useful simplified relation is:

```text
I_half < unintended-switch boundary
and
I_selected > required-switch boundary
```

Real systems add device spread, temperature, line impedance/inductance, switch behavior, timing, sense thresholds, and other variation.

### Functional analogy

Case 70 may be compared functionally with later disturbance cases only at a high level:

```text
operation on target state
    can impose a physical burden on non-target state
```

Magnetic-core half-select, DRAM disturbance, and NAND read/program disturbance are **not the same mechanism** and should not be placed in a single technical genealogy without direct evidence.

### Philosophical interpretation

The bounded interpretive point is:

> retention can require maintaining a safe distance from an unwanted state transition during operations directed elsewhere.

The phrase `negative-action margin`, used in the new Olsen/Best deepening, is repository vocabulary rather than period terminology.

---

## 5. Current cross-case comparison hooks

Case 70 is useful as an early counterexample to several simplifications found elsewhere in the repository.

```text
nonvolatile substrate
    !=
operational immunity
```

```text
not logically targeted
    !=
not physically affected
```

```text
payload state preserved
    !=
readout path undisturbed
```

```text
nominal control value
    !=
delivered physical excitation
```

These comparisons should remain functional unless an actual historical or engineering lineage is found.

---

## 6. What this navigation does not claim

- It does not make Case 70 `mature`; status remains `grounded`.
- It does not claim that the 1959 Olsen/Best filing was the first constant-voltage or resistor-dominated core driver.
- It does not claim that filing date equals public availability; publication/grant was in 1964.
- It does not identify a named DEC production machine as an implementation of US3161861A.
- It does not collapse half-select retained-state disturbance into shared-sense disturbance.
- It does not treat inhibit as Flash-style erase.
- It does not claim zero physical effect from a nonselecting pulse.
- It does not claim that architectural stabilization removes calibration, component tolerance, temperature, timing, or magnetic-material variation.
- It does not turn the companion `computing-archaeology` history into duplicated prose in this repository.

---

## 7. Remaining evidence debt

The most useful next Case-70 slices are now narrower:

1. **Named-product adoption:** locate product schematics / engineering records that can prove or falsify use of the Olsen/Best topology in a specific DEC memory system.
2. **Cross-vendor driver comparison:** compare contemporary IBM, RCA, Bell Labs, MIT, or other current-driver architectures before claiming what was typical.
3. **Quantified circuit-to-margin evidence:** find a primary source that measures delivered-current variation and selected / half-selected margin on the same plane.
4. **Earlier priority / prior art:** search earlier drive-source patents and technical reports rather than treating US3161861A as an invention-priority endpoint.
5. **Temperature coupling:** connect core-temperature behavior, drive compensation, and service settings with primary evidence.
6. **Fault / lab reproduction:** if later performed, classify circuit simulation or hardware replay as Experiment (E), not historical evidence.

---

## 8. Compact map

```text
remanent magnetic payload
    |
    +-- repeated nonselecting excitation
    |      -> retained-state margin
    |
    +-- shared sense response
    |      -> discrimination margin
    |
    +-- write inhibit
    |      -> transition authorization
    |
    +-- drive-source architecture
    |      -> pulse amplitude / waveform reproducibility
    |
    +-- service / calibration regime
           -> installed-system operating margin
```

Case 70 remains strongest when these layers stay separate and are only joined where a source actually supports the connection.