# Case 70 Deepening — DEC MM11-S Temperature-Indexed Operating Margins and Worst-Case Noise Qualification (1972)

## Status

**bounded deepening complete**

## Purpose

Case 70 already separates three different layers of magnetic-core retention:

- remanent state under repeated nonselecting disturbance (Papian, 1952);
- sense-path disturbance from half-selected cores (Bauer/Haynes, 1954-filed IBM patent);
- installed-machine operating-margin qualification (DEC MM8-E, 1973; IBM 1800, 1970).

One remaining roadmap debt is narrower: obtain more **machine-specific quantitative temperature/margin evidence** without pretending that a few manuals constitute a statistical distribution of all deployed core memories.

This slice uses Digital Equipment Corporation's 1972 **MM11-S 8K Core Memory and Control** maintenance manual for PDP-11/45 systems. It is valuable because the same vendor document places four things in one bounded production/service record:

1. X/Y-current margin at three temperatures;
2. strobe-pulse margin at the same three temperatures;
3. a factory-set current-generator amplitude and a narrower field-service adjustment temperature range;
4. a named `Worst Case Noise Test` that deliberately constructs high-noise memory patterns and flags locations affected by previous memory operations.

The bounded result is:

```text
published operating margin
!=
field adjustment condition
!=
per-unit measured margin distribution
!=
remanent shelf-retention lifetime

and

worst-case memory-traffic qualification
!=
Papian-style material characterization
```

The evidence deepens Case 70; it does not create a new general history of DEC core memory.

---

## Source and inspection boundary

Primary source:

- Digital Equipment Corporation, **_MM11-S Core Memory Maintenance Manual_**, `DEC-11-HCMMC-D`, first printing July 1972, second printing revised November 1972. Archival PDF: <https://bitsavers.trailing-edge.com/pdf/dec/pdp11/memory/MM11-S/DEC-11-HCMMC-D_MM11-S_Core_Memory_Maintenance_Manual_197202.pdf>

Independent mirrors/indexes used only to confirm document identity and preserve an alternate access path:

- RCS/RI PDP-11 library: <https://www.rcsri.org/library/dec-pdp11/index.shtml>
- RCS/RI copy of the broader MM11 core-memory manual family: <https://www.rcsri.org/library/dec-pdp11/MM11-Core-Memory.pdf>

The archival PDF endpoint exposed page-preserving searchable text in this research environment. Attempts to render screenshots of the relevant PDF pages through the available screenshot path returned a cache-miss error, so this record makes **no claims that depend on visual interpretation of waveform drawings, schematic geometry, line weight, or typography**. The quantitative claims below are confined to the text and tables associated with printed pages 1-2, 3-1–3-2, and 3-11–3-12 as represented in the searchable PDF extraction.

---

## Historical record (H/P)

### H1 — DEC specifies X/Y current margin at three temperatures

Table 1-1, `MM11-S Memory Specifications`, identifies the device as a magnetic-core, read/write, coincident-current, random-access memory and gives the following X/Y-current margins:

- `±6% @ 0°C`;
- `±7% @ 25°C`;
- `±6% @ 50°C`.

The same table gives an ambient operating-temperature range of `0°C to 50°C`.

This is a **product-level specification** for the MM11-S. It is not evidence for a universal ferrite-core current tolerance and it is not a distribution measured across all shipped units.

### H2 — DEC specifies strobe margin at the same three temperatures

The same Table 1-1 gives strobe-pulse margins:

- `±30 ns @ 0°C`;
- `±40 ns @ 25°C`;
- `±30 ns @ 50°C`.

This matters because temperature is not represented only as a condition on the magnetic material. DEC publishes a temperature-indexed margin for **when the sense path samples the memory**, as well as for X/Y drive current.

The table therefore directly supports the period fact that the installed memory's usable operating envelope was characterized in more than one control dimension.

### H3 — nominal generator amplitude is factory-set, not a field tuning knob

Section 3.2.2 states that each X and Y current generator is factory set to `410 ±5 mA` and is **not adjustable in the field**. It provides current loops for probe measurement and says the read-current pulse should measure `410 ±5 mA` while the `+5 V` and `-15 V` supplies are within `±3%`.

This separates at least three historical states:

```text
factory-set nominal current
!=
field-observed current check
!=
field-authorized adjustment
```

The service technician may verify the current, but this manual does not authorize them to retune that generator in the ordinary preventive-maintenance procedure.

### H4 — field tests/adjustments use a narrower ambient range than the product operating specification

Section 3.2.1 says that **all tests and adjustments must be performed at 20°C to 30°C**.

That is narrower than Table 1-1's `0°C to 50°C` ambient operating range.

The source therefore directly distinguishes:

```text
specified operating environment
!=
service calibration / adjustment environment
```

This is especially important when using maintenance manuals as historical evidence: the conditions under which a technician is instructed to tune or qualify the machine need not span the full environment for which the product is specified to operate.

### H5 — strobe adjustment is an error-boundary search under worst-case patterns

Section 3.3.1 calls strobe delay a **critical adjustment**. It says it is factory adjusted and should be changed only when one of the three memory modules is replaced.

The strobe is to be set while cycling worst-case patterns. The technician moves strobe time from earliest to latest, finds the two endpoints where the memory begins to error, and sets the proper value **mid-way between those two error endpoints**. The procedure also tells the technician to allow enough time to cycle completely through the worst-case pattern at every strobe position.

This is an installed-system qualification method, not a direct measurement of quiescent remanent lifetime.

### H6 — the diagnostic suite deliberately manufactures worst-case plane noise

Section 3.4.5 describes `Worst Case Noise Test (MAINDEC-11-D1G)`.

The manual states that the purpose of the program is to generate the **maximum possible amount of plane noise** during memory-reference instructions and to check operation under worst-case conditions. It says plane noise is distributed algebraically across the core plane and adds to ordinary dynamic noise on the sense lines, potentially causing stored low/high data to be misread.

The program uses alternating `-1` and `0` configurations and repeatedly performs read/write/complement operations. After loading the patterns it scans again with a read-complement-read-complement (`RCRC`) loop. A location detected as being **disturbed by a previous RCRC operation** is flagged as an error; the complementary pattern is then used so cores are exercised in both logical states.

This is a named production diagnostic, not a generic modern reconstruction.

### H7 — the manual itself separates margin/noise variables rather than naming one scalar `core margin`

Across the specification and maintenance sections, DEC exposes at least these distinct variables:

- X/Y-current margin;
- strobe-pulse margin;
- supply-voltage tolerance;
- factory-set current amplitude;
- ambient temperature for adjustment;
- plane/dynamic noise under data patterns;
- sense-path sampling under strobe timing.

The historical vocabulary is not identical to this repository's later `retention relation` language, but the source itself blocks a one-number account of installed core-memory reliability.

---

## Engineering reconstruction (E)

### E1 — a three-point temperature margin table is not a material temperature coefficient

The product table gives three operating-margin values for current and strobe timing. It does **not** disclose:

- ferrite composition;
- permeability/coercivity versus temperature curves;
- the transfer function of every compensation component;
- individual stack distributions;
- a continuous function between `0°C`, `25°C`, and `50°C`.

So:

```text
three temperature-indexed product margins
!=
material temperature coefficient
!=
continuous environmental failure curve
```

The evidence nevertheless closes a useful smaller gap: a shipped memory product published **different quantitative current/timing margins at different temperatures**.

### E2 — operating range and calibration range are different contracts

Combining Table 1-1 with §3.2.1 yields:

```text
0–50°C product operating specification
!=
20–30°C field test/adjustment condition
```

The narrower service condition does not imply the memory is unsupported outside 20–30°C; conversely, the 0–50°C product range does not authorize performing the documented calibration procedure at every temperature in that range.

This is a useful cross-case control against treating any one temperature number as `the retention temperature`.

### E3 — nominal setpoint, tolerance, and observed failure boundaries must remain separate

The manual gives a nominal current pulse (`410 ±5 mA`), published X/Y current margins (`±6/±7/±6%` at three temperatures), and a strobe procedure that searches for observed error endpoints.

Those are different kinds of evidence:

```text
nominal setpoint
!=
published allowable margin
!=
observed per-machine error boundary
!=
chosen centered service setting
```

A historical manual can contain all four categories without making them interchangeable.

### E4 — midpoint strobe adjustment is robustness seeking, not proof of symmetric analog margin

The procedure deliberately chooses a point between empirically observed early and late failure edges. That supports an engineering reconstruction of **operating-point robustness**.

It does not prove that the underlying analog pass region is perfectly symmetric, that every unit has the same continuous timing window, or that the published `±30/±40 ns` product margins are literally the measured endpoints of the field adjustment on every machine.

### E5 — worst-case-noise qualification exercises a coupled state/readout relation

The diagnostic intentionally chooses patterns and operation sequences expected to maximize plane/sense noise, then checks whether later reads still classify values correctly.

For Case 70, the safest reconstruction is:

```text
retained magnetic state
+
neighbor/plane electrical activity
+
sense-path noise
+
strobe sampling
->
observed symbol correctness under diagnostic traffic
```

The source does not always distinguish whether a flagged `disturbed` location reflects a permanently altered remanent state, a transient/noise-induced misread, or another circuit fault. Therefore the diagnostic should **not** be rewritten as a measured half-select bit-flip rate.

### E6 — service qualification can intentionally create hostile traffic without being destructive testing

The program tries to maximize plane noise and repeatedly toggles/complements patterns. That is stronger than merely reading an idle retained word, yet the intended outcome is still correct continued operation.

This supports a bounded project distinction:

```text
ordinary quiescent retention
!=
qualified retention/recoverability under adversarial diagnostic traffic
```

The term `adversarial` here is modern engineering shorthand for deliberately stressful patterns; it is not DEC's historical vocabulary.

---

## Functional comparison (FA)

### MM11-S (1972) versus PDP-8/E MM8-E (1973)

Both are DEC production/service witnesses, but they expose different qualification surfaces.

MM8-E evidence already in Case 70 gives:

- discrete X/Y-current-control settings;
- discrete slice settings;
- thermistor-based temperature tracking;
- six 10-ns strobe positions;
- checkerboard qualification requiring at least three consecutive working positions and adjacent-position runs.

MM11-S gives:

- explicit product X/Y-current margins at `0/25/50°C`;
- explicit strobe-pulse margins at the same temperatures;
- a factory-set `410 ±5 mA` current pulse that field personnel verify but do not adjust;
- a `20–30°C` maintenance adjustment condition despite `0–50°C` product operation;
- a continuous error-boundary/midpoint strobe procedure described independently of the MM8-E's six-position switch;
- a separate worst-case plane-noise diagnostic.

The bounded conclusion is:

```text
same vendor
+
same broad coincident-current retention problem
!=
same exposed service controls
!=
same qualification procedure
```

This is useful precisely because it prevents the MM8-E procedure from becoming a stand-in for DEC core memory as a whole.

### MM11-S versus IBM 1800 (1970)

The already-grounded IBM 1800 slice supplies a different service surface: temperature-compensated `VRef`, explicit temperature-related signal-peak motion relative to a fixed strobe, a `<7 mV at strobe time` half-select `delta noise` criterion in one waveform context, and a closed-cover requirement for maintaining the thermal relation during adjustment.

MM11-S instead publishes temperature-indexed **product margin values** and explicitly separates operating range from service-adjustment temperature.

Therefore:

```text
IBM mechanism/service explanation
!=
DEC three-point product margin specification
```

They support cross-machine comparison but not a shared implementation or genealogy claim.

### MM11-S versus Papian 1952

Papian's laboratory procedure varies nonselecting pulse amplitude, length, spacing, and count to characterize candidate cores and their disturbed signal/retention ratios.

MM11-S `MAINDEC-11-D1G` is a production-system diagnostic that generates worst-case data patterns, repeated memory-reference traffic, and sense-plane noise.

So:

```text
material/pulse-regime characterization
!=
installed-system worst-case traffic qualification
```

The shared abstract pattern is only that **non-target/neighbor activity can reduce the margin with which a retained symbol remains recoverable**.

---

## Philosophical interpretation — bounded

This slice supports one narrow project-level interpretation:

> A persistent state is not fully characterized by the fact that its substrate can remain magnetized. The machine also defines an environment and an operating region within which that magnetization continues to count as a reliably recoverable symbol.

The 1972 manual makes that region visible through current margin, strobe margin, temperature, service authority, and stress-pattern testing.

This is a present-day interpretation disciplined by the engineering record. DEC did not formulate a philosophy of technical retention.

---

## Rejected / unsupported upgrades (X)

This evidence does **not** establish that:

- `±6%`, `±7%`, `±30 ns`, `±40 ns`, or `410 ±5 mA` are universal magnetic-core constants;
- Table 1-1 reports the measured distribution of every shipped MM11-S unit;
- three temperature points define a continuous material temperature coefficient;
- every MM11-S necessarily fails immediately outside the listed margins;
- the `20–30°C` service-adjustment condition is the product's only supported operating temperature;
- the `0–50°C` ambient range means the maintenance adjustment may be performed anywhere in that range;
- a location flagged by the Worst Case Noise Test necessarily suffered permanent remanent-state reversal;
- `MAINDEC-11-D1G` is equivalent to Papian's 1952 nonselecting-pulse material test;
- the MM11-S strobe midpoint procedure is identical to the PDP-8/E MM8-E six-position checkerboard procedure;
- same-vendor similarity proves a direct design lineage between the two memory modules;
- IBM and DEC service practices share a demonstrated genealogy;
- the manual settles invention priority for margin testing, temperature compensation, or worst-case pattern diagnostics;
- the diagnostic is a shelf-retention, secure-erasure, or sanitization test.

---

## What this slice closes

This closes a bounded portion of Case 70's remaining `quantitative temperature dependence` and `cross-machine margin` debt:

- a third named production/service memory witness is now available when combined with IBM 1800 and DEC MM8-E;
- unlike the previous witnesses, MM11-S publishes **three-point temperature-indexed current and strobe margins** in one product specification;
- it separately exposes the narrower field adjustment temperature and a named worst-case plane-noise diagnostic.

Still open:

- anything statistically representative of production/service margins across a large population of machines;
- measured unit-to-unit or lot-to-lot distributions;
- deployed ferrite material and core-vendor distributions;
- continuous temperature coefficients or physical material curves for the MM11-S cores;
- factory acceptance records, manufacturing correspondence, and field-return data;
- direct actor-to-actor genealogy among Papian, IBM, and DEC procedures;
- hardware reproduction of the maintenance/diagnostic procedures.

Those broader engineering-history questions belong primarily in `tmzncty/computing-archaeology`.

---

## Related repository reuse

The general magnetic-core history, manufacturing labor, coincident-current logic, and destructive-read mechanism already belong to:

- <https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md>

A fresh repository search for `MM11-S` in `tmzncty/computing-archaeology` returned no dedicated packet during this pass. This file therefore keeps only the retention-specific seam:

```text
remanent state
-> temperature-indexed current/timing margin
-> service adjustment condition
-> worst-case traffic qualification
-> recoverable symbol
```

It does not duplicate a general PDP-11/45 or DEC memory-system history.

---

## Navigation

- Parent case: [`../cases/70-magnetic-core-half-select-disturbance.md`](../cases/70-magnetic-core-half-select-disturbance.md)
- Papian direct-facsimile deepening: [`70-papian-1952-half-select-disturbance-facsimile-deepening.md`](70-papian-1952-half-select-disturbance-facsimile-deepening.md)
- IBM 1800 cross-vendor production/service witness: [`70-ibm1800-1970-temperature-sense-margin-deepening.md`](70-ibm1800-1970-temperature-sense-margin-deepening.md)
- DEC PDP-8/E MM8-E production/service witness: [`70-dec-pdp8e-1973-operating-margin-deepening.md`](70-dec-pdp8e-1973-operating-margin-deepening.md)

---

## Source anchors

### DEC `DEC-11-HCMMC-D`, 1972

Archival PDF: <https://bitsavers.trailing-edge.com/pdf/dec/pdp11/memory/MM11-S/DEC-11-HCMMC-D_MM11-S_Core_Memory_Maintenance_Manual_197202.pdf>

- title/front matter: `MM11-S core memory maintenance manual`, `DEC-11-HCMMC-D`; first printing July 1972, second printing revised November 1972;
- Table 1-1 / printed p. 1-2: `X-Y Current Margins` = `±6% @ 0°C`, `±7% @ 25°C`, `±6% @ 50°C`; `Strobe Pulse Margins` = `±30 ns @ 0°C`, `±40 ns @ 25°C`, `±30 ns @ 50°C`; ambient temperature `0°C to 50°C`;
- §3.2.1 / printed p. 3-1: all tests and adjustments at `20°C to 30°C`;
- §3.2.2 / printed p. 3-2: X/Y current pulse factory set to `410 ±5 mA`, not field adjustable; measurement with supply rails within `±3%`;
- §3.3.1 / printed p. 3-2: strobe is a critical adjustment; cycle worst-case patterns; locate earliest/latest error endpoints; choose the midpoint;
- §3.4.5 / printed pp. 3-11–3-12: `Worst Case Noise Test`, deliberate maximum plane-noise patterns, RCRC scan, and errors for locations detected as disturbed by previous RCRC operations.

Secondary mirror/index only: <https://www.rcsri.org/library/dec-pdp11/index.shtml>
