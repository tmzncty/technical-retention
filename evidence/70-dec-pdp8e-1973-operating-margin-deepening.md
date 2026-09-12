# Case 70 Deepening — DEC PDP-8/E MM8-E Production Operating-Margin Qualification (1973)

## Purpose

Case 70 already establishes, from Forrester, Papian, and Bauer/Haynes, that coincident-current core memory depends on half-select disturbance margin and sense discrimination. The remaining roadmap debt was narrower: find a **named production machine** whose own service documentation exposes quantitative operating-margin practice rather than another laboratory material characterization.

This record uses Digital Equipment Corporation's September 1973 revision of the *PDP-8/E, PDP-8/F & PDP-8/M Maintenance Manual, Volume 1: Processor* (`DEC-8E-HMM1A-D-D`), specifically the MM8-E memory maintenance material in §§4.7.2–4.7.9. The manual is a period vendor primary source for an installed commercial machine. It is not used to infer universal magnetic-core constants.

The bounded result is:

```text
remanent state can persist at rest
!=
installed memory has adequate powered operating margin
!=
a particular timing/current setting has passed service qualification
```

## Source and inspection boundary

The manual is catalogued by Manx as DEC part `DEC-8E-HMM1A-D-D`, dated September 1973, with an archival Bitsavers copy. The accessible text used for this pass is a line-indexed extraction of that original manual hosted by device.report. The extraction preserves section/table labels, printed page markers, and the numerical maintenance procedure used below.

This pass **does not claim facsimile-level inspection of the typography, schematics, or waveform drawings**. The Bitsavers PDF endpoint was independently identified through the Manx catalogue, but the research environment could not retrieve that PDF directly. Accordingly, claims below are limited to text that can be checked in the extracted manual plus bibliographic identity from the archival catalogue.

Primary access paths:

- Manx catalogue record, DEC `DEC-8E-HMM1A-D-D`, September 1973: <https://manx-docs.org/details.php/1%2C4017>
- Bitsavers archival PDF listed by Manx: <http://bitsavers.org/pdf/dec/pdp8/pdp8e/DEC-8E-HMM1A-D-D_PDP-8e_Maintenance_Manual_Volume_1_Processor_Sep73.pdf>
- searchable extraction of the same manual: <https://device.report/m/f543be6c683c3e08d16eca14f854b69311c27dc3ca837af500c7ec6e85aed20a>
- independent PDP-8 document catalogue entry: <https://www.pdp8online.com/pdp8cgi/query_docs/view.pl?id=48>

## Historical / primary record (H/P)

### 1. DEC treats the MM8-E operating point as several separately controlled variables

Section 4.7.2 and Table 4-6 list `Field Select`, `Strobe`, `Slice`, `X/Y Current Control`, and `Temperature Tracking`. The table also separates who is authorized to set them:

- field select — factory or field service;
- strobe — factory or field service;
- slice — factory only;
- X/Y current control — factory only;
- temperature tracking — factory only.

This is direct evidence that the production/service operating point was not represented by a single scalar `core margin`, and that DEC distinguished manufacturing calibration authority from ordinary field adjustment.

### 2. Slice and drive-current calibration are discrete and quantitative

Section 4.7.5 gives four slice-level choices at the G104 test point: `-4.3 V`, `-4.8 V`, `-5.3 V`, and `-6.0 V`, followed by an explicit warning not to field-adjust the slice level.

Section 4.7.6 says the G227 X/Y current control has four discrete calibration settings. It gives current-control-voltage offsets of `+3.7%`, `+2.2%`, nominal (`~3.5 V at 25 °C`), and `-1.7%`; the corresponding nominal X/Y current is `370 mA`, measured between the drive and stack board. The manual again says not to field-adjust that control voltage.

Section 4.7.8 gives a nominal inhibit current of `340 mA`, while stating that it varies proportionally with the `-15 V` supply.

These figures are machine/module settings in this DEC design. They are not promoted into universal ferrite-core switching thresholds.

### 3. Temperature is part of the control relation

Section 4.7.7 states that a thermistor-resistor combination on the memory stack board forms a temperature-sensitive divider connected to the current-control circuit. Section 4.7.6 separately states that the nominal current-control voltage varies with temperature.

The historical fact is therefore modest but important: the MM8-E did not treat one room-temperature voltage/current number as the entire operating condition. This source does **not** supply a temperature coefficient, core-material distribution, or whole-environment failure surface.

### 4. Strobe margin is qualified by sweeping to observed error boundaries

Section 4.7.4 says the six-position rotary switch changes strobe positioning in discrete `10 ns` steps. Section 4.7.9 then directs service personnel to run the `Memory Checkerboard` program, move the strobe one position at a time until errors occur in one timing direction, repeat in the other direction, and remember both error positions.

The manual states that a reliable system must have **at least three consecutive working positions**. The final strobe is set to the middle working position; for an even number of working positions, the more delayed of the two center positions is preferred.

Checkout then requires the checkerboard to run in the middle and, for **at least 15 minutes**, in the positions immediately to the left and right of middle without errors. Acceptance itself is run only in the final strobe position.

This is unusually useful for retention analysis because the maintenance procedure operationalizes margin as a **tested error-free timing region around the accepted operating point**, rather than merely publishing one nominal timing number.

### 5. DEC's symptom table connects data errors to the same control variables

The memory-maintenance material also associates random/all-one/all-zero data errors with X/Y current or voltage, slice voltage, and inhibit current/voltage being too high or too low. This reinforces that the quantitative settings above are part of a coupled recoverability envelope, not decorative factory constants.

## Engineering reconstruction (E)

### E1 — nonvolatile remanence is not enough for a working installed memory

Case 02 establishes that ferrite remanence can persist without periodic refresh. The MM8-E maintenance procedure adds a different layer:

```text
quiescent remanent persistence
+
selection-current margin
+
sense/slice margin
+
strobe timing margin
+
temperature compensation
->
usable powered memory operation
```

The arrow is an engineering reconstruction. DEC did not formulate this repository's retention vocabulary.

### E2 — a diagnostic pass window is operational margin, not a retention lifetime

The checkerboard sweep gives evidence about the set of discrete strobe positions over which the installed memory behaves correctly under that diagnostic. It does **not** measure how long an unpowered core retains remanence, nor does the 15-minute adjacent-position run establish a statistical bit-error rate or lifetime guarantee.

Therefore:

```text
15 minutes error-free at adjacent strobe settings
!=
15-minute information-retention time
!=
quantified long-term failure probability
```

### E3 — midpoint selection is robustness practice, not a universal analog tolerance

With 10-ns switch increments and at least three consecutive passing positions, the service procedure deliberately chooses an interior point rather than the first merely functioning edge setting. That supports a bounded reconstruction of **operating-point robustness**.

It does not justify saying that every MM8-E has a continuous symmetric `±10 ns` tolerance. The procedure observes discrete switch positions and error boundaries under a particular diagnostic; it does not map the complete analog pass/fail surface between taps.

### E4 — available calibration settings are not guaranteed passing settings

The four slice levels and four current-control-voltage choices are adjustment alternatives. Their existence does not show that a given stack passes at all of them. The strobe procedure is explicitly about finding the working region; the current/slice tables similarly should be read as calibration state space, not guaranteed tolerance bounds.

### E5 — maintenance authority is itself part of the technical control surface

Table 4-6 separates field-adjustable strobe/field-select settings from factory-only slice/current/temperature choices. For this case that supports:

```text
manufacturing calibration authority
!=
field maintenance authority
```

This is not merely organizational trivia. It constrains which retained/configuration states a field technician is expected to alter while restoring reliable operation.

### E6 — temperature compensation makes the operating point relational

Because the current-control path includes temperature-sensitive compensation, the nominal `~3.5 V at 25 °C` setting is not the whole state that determines selection behavior. The safe operating relation includes environment-responsive control circuitry.

The evidence does not establish the exact core chemistry or temperature distribution, so no material-specific temperature law is reconstructed here.

## Functional comparison (FA)

Papian's 1952 evidence and DEC's 1973 service manual operate at different layers.

Papian experimentally varies nonselecting pulse conditions and evaluates information-retention / signal ratios of candidate cores. DEC gives a named production machine's maintenance procedure for keeping the complete installed memory inside a working timing/current/sense region.

The useful comparison is:

```text
material / pulse-regime characterization
!=
installed-system service qualification
```

They are complementary, not interchangeable. No direct genealogy from Papian's particular laboratory test procedure to the PDP-8/E service routine is asserted.

A second bounded comparison is with Case 02:

```text
nonvolatile core element
!=
margin-free memory subsystem
```

The MM8-E still requires calibrated currents, timing, sense slicing, temperature tracking, and diagnostic qualification even though its payload-bearing elements are magnetically nonvolatile.

## Philosophical interpretation — bounded

The case supports one narrow later interpretation: a technically persistent state can depend on keeping the surrounding machine inside a **safe operational relation**, not only on the persistence of the payload-bearing substrate itself.

That is a project-level interpretation. The DEC manual is a maintenance document; it does not claim a philosophy of technical retention.

## Rejected / unsupported upgrades (X)

This evidence does **not** establish that:

- `370 mA`, `340 mA`, any listed slice voltage, or any 10-ns step is a universal magnetic-core constant;
- every PDP-8 family memory stack used identical MM8-E calibration values;
- three consecutive passing taps imply a continuous symmetric timing tolerance of a specified width;
- a 15-minute checkerboard run is a retention-duration or reliability guarantee;
- every available slice/current calibration setting must pass;
- the thermistor network proves a particular ferrite formulation, temperature coefficient, or deployed-material distribution;
- the 1973 manual establishes who invented coincident-current margin testing or midpoint calibration;
- this maintenance procedure demonstrates the physical state of cores during arbitrary power failure, secure erasure, or sanitization;
- chronological compatibility with Papian's earlier work proves direct influence or genealogy.

## What this slice closes

This closes one explicit roadmap debt: **a named-machine quantitative production/service operating-margin witness** now exists for magnetic core memory. It supplements, rather than replaces, Papian's laboratory disturbance measurements.

Still open:

- cross-machine distributions of actual production/service margins;
- deployed core-material/vendor distributions;
- quantitative temperature coefficients and environmental margin curves;
- earlier manufacturing correspondence or acceptance-test records;
- invention/priority and actor-to-actor genealogy;
- hardware reproduction of the MM8-E adjustment procedure.

Those broader engineering-history questions belong primarily in `tmzncty/computing-archaeology`; this record exists only for the retention-specific relation among remanent state, operating margin, configuration, and recoverability.

## Related repository reuse

The general core-memory history, coincident-current mechanism, destructive read, and manufacturing rationale are already covered in:

- <https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md>

This case reuses that history and adds only the production/service margin evidence required by `technical-retention`.
