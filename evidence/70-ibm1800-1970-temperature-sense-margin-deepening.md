# Case 70 Deepening — IBM 1800 Core-Storage Temperature and Sense-Margin Qualification (1970)

## Status

**bounded deepening complete**

## Purpose

Case 70 already has two complementary evidence layers:

- Papian's 1952 laboratory characterization of repeated nonselecting disturbance and disturbed-signal ratios;
- DEC's 1973 PDP-8/E MM8-E field-maintenance procedure, which exposes discrete current, slice, temperature-tracking, and strobe controls plus a checkerboard-qualified working window.

The remaining roadmap debt was broader: obtain a **second named production/service machine from another vendor** so that one DEC procedure is not silently treated as representative of all installed coincident-current memories.

This slice uses IBM's February 1970 1800 field-engineering manuals. It closes only a bounded cross-machine witness:

```text
same ferrite-remanence principle
!=
same service margin geometry

quiescent retained polarity
!=
environment-independent recoverability

half-selected cores remain logically unselected
!=
zero contribution at the sense path
```

It does not attempt a general IBM 1800 history, a vendor-wide core-memory survey, or a statistical distribution of deployed margins.

## Sources and inspection boundary

Primary vendor documents:

1. International Business Machines Corporation, **_1800 Data Acquisition and Control System Processor-Controller: Field Engineering Theory of Operation_**, Order No. `SY26-5912-4`, Fifth Edition, February 1970. The manual identifies the 1801/1802 Processor-Controllers and includes the core-storage addressing, drive-current, inhibit/sense, and timing sections. Searchable reproduction: <https://manuals.plus/m/6a52c8f6a4c6271b0377de2d2fbb4a0f9e85fa7664c54f0fc366b0c3d34a04b6>
2. International Business Machines Corporation, **_1800 Data Acquisition and Control System: Field Engineering Maintenance Manual_**, Order No. `SY26-5956-6`, Seventh Edition, February 1970. The preface explicitly says that it covers the 1801/1802 Processor-Controllers and the 1803 Core Storage Unit. Searchable reproduction: <https://manuals.plus/m/9309685d528c91a62ad1e5c75b40c09becd58c088be4d41de6fb0ff3f02a83c0>

Archival copies are also indexed at Bitsavers, including the same February-1970 order numbers. The present environment could inspect the searchable text reproductions and printed page markers but could not fetch the large PDF binaries through the web tool. Accordingly this record does not claim facsimile-level verification of waveform drawing geometry or typography; it limits itself to text, printed-page labels, and quantitative values preserved in the searchable reproductions.

## Historical / primary record (H/P)

### 1. IBM explicitly makes drive current temperature-dependent

The February-1970 *Field Engineering Theory of Operation* distinguishes four-microsecond and two-microsecond core-storage drive circuitry, but both use a temperature-compensated reference.

For the four-microsecond storage, the manual states that a temperature-compensated voltage reference is applied to the current-control circuit. On printed p. 2-17 it further says that the `V-Reference` applied to that circuit is temperature compensated so that the X-Y drive current tracks its optimum value over a specified temperature range.

For the two-microsecond storage, a temperature-compensated reference is applied to both the read source and write sink; printed p. 2-18 says the current magnitude is controlled by a temperature-controlled `V Ref`.

This is direct period evidence that the selection-current operating point is not one fixed electrical value independent of environment.

### 2. The maintenance manual ties single-address failures to environment, current, strobe, and sense threshold

In the *Field Engineering Maintenance Manual*, §1.7.7 `Trouble Diagnosis`, item 5 `Single-Address Failures`, printed p. 1-46, IBM lists several interacting causes:

- a weak or early-peaking core;
- low `VRef`, which determines drive-current level;
- poor current balance in two-microsecond storage;
- a late strobe;
- high `Vsa - Ve`, which determines the sense-amplifier threshold for a one bit in the four-microsecond design;
- a large deviation from a nominal **60 °F–90 °F room environment**.

This list is important because IBM does not isolate `the core` from its drive, sampling, threshold, and environmental apparatus when diagnosing whether a stored bit is recoverable.

### 3. Temperature shifts the relation between core waveform and fixed strobe time

The same p. 1-46 description states that, as temperature rises, cores peak earlier and higher, while ideally the strobe itself does not move. IBM then notes that the sampled signal can therefore be lower because the unchanged strobe occurs later relative to the shifted core signal.

At lower temperature, the manual says that more current drive is required for the same output; some cores can produce very low output, their peaks occur later, and in four-microsecond storage this can cause a bit-dropping problem severe enough to justify replacing the storage unit. It mentions increasing `VRef` or lowering the applicable sense threshold as a possible temporary fix.

The historical claim is therefore not simply `temperature changes ferrite properties`. IBM's own service text connects temperature to **relative signal/strobe timing, required drive current, observed bit dropping, and maintenance action**.

### 4. IBM names half-selected-core sense contribution and gives a quantitative strobe-time criterion

The maintenance manual's core-storage waveform material gives an unusually direct named-machine witness for the Case-70 sense-disturbance layer.

In the discussion accompanying the two-microsecond storage read envelope, the manual defines `Delta noise` as signal on the sense line from **half selected cores — cores with either X or Y drive current but not both**. It says this delta noise should decay to **less than 7 mV at strobe time**.

This is not a universal ferrite constant. It is a production/service criterion for this IBM 1800 storage implementation and its documented waveform/test setup.

The same waveform section also says, for a single-address sense-line example, that strobe timing matters so that noise is not mistaken for a bit.

Thus IBM supplies a second production-level witness for the distinction already reconstructed from Bauer/Haynes:

```text
half-selected core does not switch as the addressed bit
!=
half-selected core contributes no sense-path signal
```

### 5. Temperature tracking constrains the maintenance procedure itself

Section 4.4.3 `Core Storage Adjustments`, printed p. 4-3, says the core-storage adjustments are set for optimum operation and should not be changed casually. IBM says adjustment pots carry sealing compound to preserve factory settings, although the seal may be broken when field adjustment is required.

More unusually, the manual states that **proper operation of the core-storage temperature-tracking circuits requires the core-storage cover to remain closed except briefly**. New production machines include a hole allowing `VRef` adjustment while the cover remains closed, and IBM cites a service aid for modifying older covers similarly.

This is direct evidence that the maintenance apparatus was expected to preserve the relevant thermal condition while the current-control setting was adjusted. Opening the apparatus for service could otherwise change part of the environment that the compensation loop was meant to track.

## Engineering reconstruction (E)

### E1 — the stored magnetic state and the currently recoverable symbol are different layers

The IBM evidence supports:

```text
remanent polarity survives
+
drive/current relation remains adequate
+
sense threshold remains adequate
+
strobe samples an adequate part of the waveform
+
background half-select noise has decayed sufficiently
->
bit recoverable through the installed read path
```

This arrow is a modern engineering reconstruction. IBM does not use this repository's `retention relation` vocabulary.

The key boundary is:

```text
state still physically present
!=
symbol currently recoverable with the configured apparatus
```

A temperature-induced timing/amplitude shift can make the installed sampling relation marginal even without evidence that the core has lost all remanent polarity.

### E2 — environmental compensation is part of effective addressing/recovery geometry

Case 70 already argues that coincident-current addressing is partly a material-margin problem. The IBM 1800 evidence makes that relation concrete in a named machine:

```text
address decode
+
half-select/full-select current relation
+
temperature-compensated VRef
+
strobe timing
+
sense threshold/noise margin
->
usable selected-bit recovery
```

Therefore `row + column = address` is logically correct but technically incomplete as a description of what makes an installed address reliable.

### E3 — a fixed strobe creates a relative-time margin, not a universal absolute timing law

The p. 1-46 temperature discussion is especially useful because it explains a failure mode through **relative timing**. If the magnetic response peak moves while strobe time stays fixed, the same nominal strobe can sample a less favorable part of the waveform.

So:

```text
unchanged strobe setting
!=
unchanged sampling margin
```

This does not establish an exact transfer function versus temperature, nor a universal temperature coefficient for ferrite materials.

### E4 — the `<7 mV` delta-noise criterion is a system/service limit, not a core-material property

The manual's delta-noise number belongs to a documented IBM 1800 waveform/setup and sense path. It should not be converted into:

- a universal half-select disturbance voltage;
- a universal magnetic-core noise floor;
- a universal acceptable signal-to-noise ratio;
- a direct measure of remanent-state degradation.

It is better classified as a **sense-path operating criterion** at the time the strobe samples the read envelope.

### E5 — maintenance can perturb the condition being calibrated

The closed-cover requirement exposes a reflexive service problem:

```text
open apparatus to adjust memory
->
change thermal condition
->
change the operating point being measured/adjusted
```

IBM's access hole is therefore not merely a convenience. It is evidence that field maintenance practice was designed so the thermal relation remained representative while `VRef` was adjusted.

This does not prove a particular temperature transient, equilibration time, or error probability after opening the cover.

### E6 — replacement can be a margin-recovery action without proving payload-media destruction

IBM says sufficiently low-output cores in the four-microsecond storage can produce bit dropping severe enough to warrant replacement of the storage unit. That is a service response to inadequate recoverability margin.

It does not prove that every failing core had permanently lost its stored magnetic polarity, nor that replacement sanitized or physically erased the removed array.

## Functional comparison (FA)

### IBM 1800 (1970) versus DEC MM8-E (1973)

The two named-machine witnesses now prevent one maintenance implementation from standing in for all core memory.

DEC MM8-E exposes:

- discrete slice choices;
- discrete X/Y current-control settings;
- thermistor-based temperature tracking;
- six 10-ns strobe positions;
- a checkerboard procedure that requires at least three consecutive working positions and then chooses an interior position.

IBM 1800 exposes a different service surface:

- temperature-compensated `VRef` controlling drive current;
- explicit diagnosis of a nominal 60 °F–90 °F room environment;
- temperature-dependent signal-peak timing/amplitude effects relative to a fixed strobe;
- a `<7 mV at strobe time` criterion for half-select `delta noise` in the documented two-microsecond waveform;
- a closed-cover requirement during temperature-tracking adjustment.

The bounded comparison is:

```text
same broad retention problem
!=
same exposed calibration variables
!=
same diagnostic procedure
!=
same quantitative service limits
```

No IBM→DEC, DEC→IBM, or Papian→IBM/DEC procedural genealogy is asserted.

### IBM 1800 versus Papian 1952

Papian varies pulse amplitude, duration, spacing, and count to characterize candidate-core disturbance and signal ratios. IBM 1800 field engineering instead diagnoses and maintains an installed system with temperature compensation, strobe timing, sense thresholds, and waveform limits.

Therefore:

```text
material/pulse characterization
!=
installed-system qualification
```

The two evidence layers are complementary, not interchangeable.

## Philosophical interpretation — bounded

The IBM witness strengthens one narrow project interpretation already suggested by Case 70:

> **A retained state may depend on a surrounding apparatus preserving the conditions under which that state remains discriminable.**

Here, the magnetic core's remanence is not the whole technical fact of persistence. Recoverability also depends on environment-responsive drive control, sampling time, threshold, and noise. The field manual even shows that opening the machine for maintenance can perturb the condition that the calibration procedure is trying to preserve.

This is a present-day philosophical interpretation disciplined by the mechanism. IBM's manuals do not claim a philosophy of retention.

## Rejected / unsupported upgrades (X)

This slice does **not** establish that:

- 60 °F–90 °F is a universal allowable room range for magnetic-core memory;
- operation outside that range necessarily causes immediate data loss;
- `<7 mV` is a universal half-select-noise limit;
- the IBM 1800's temperature compensation is identical to DEC's MM8-E thermistor network;
- the two-microsecond and four-microsecond IBM storage units have identical adjustment paths;
- every IBM 1800 field installation used exactly the same core vendor, material lot, or waveform margins;
- the core-storage cover requirement gives a quantitative thermal time constant;
- bit dropping at low temperature proves irreversible loss of remanent polarity;
- replacing a core-storage unit constitutes secure erase or sanitization;
- the February-1970 manuals establish invention priority for temperature compensation, strobe-margin testing, or half-select-noise measurement;
- similarity among Papian, IBM, and DEC proves direct influence or shared procedure lineage.

## What this slice closes

This closes one bounded part of the Case-70 roadmap debt:

- a **second named vendor/machine production-service witness** now exists alongside DEC;
- the IBM witness supplies an explicit environmental service range, relative temperature/strobe failure explanation, and a quantitative half-select sense-noise criterion;
- cross-machine comparison can now say that the broad operating-margin problem recurs while exposed variables and qualification procedures differ.

Still open:

- anything approaching a statistically meaningful distribution of production/service margins across many machines;
- actual deployed core-material and vendor-lot distributions;
- quantitative temperature coefficients/curves for the specific IBM 1800 core material;
- earlier factory acceptance records and manufacturing correspondence;
- direct actor-to-actor genealogy among laboratory tests and vendor field procedures;
- hardware reproduction of either IBM or DEC maintenance procedures.

Broader core-memory engineering history and any attempt at a multi-vendor service-history survey belong primarily in `tmzncty/computing-archaeology`.

## Navigation / related work

- Parent case: [`../cases/70-magnetic-core-half-select-disturbance.md`](../cases/70-magnetic-core-half-select-disturbance.md)
- Previous production/service deepening: [`70-dec-pdp8e-1973-operating-margin-deepening.md`](70-dec-pdp8e-1973-operating-margin-deepening.md)
- Direct Papian facsimile deepening: [`70-papian-1952-half-select-disturbance-facsimile-deepening.md`](70-papian-1952-half-select-disturbance-facsimile-deepening.md)
- General core-memory history to reuse rather than duplicate: <https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md>

A repository search for `IBM 1800 core storage temperature` in `tmzncty/computing-archaeology` found no dedicated IBM-1800 treatment during this pass, so this evidence adds only the retention-specific service-margin slice rather than rewriting a general history there.

## Source anchors

### IBM FETO `SY26-5912-4`, Fifth Edition, February 1970

- title/preface and edition: searchable reproduction lines corresponding to printed front matter;
- printed pp. 2-17–2-18: four- and two-microsecond drive-current generation; temperature-compensated voltage reference; X-Y current tracking; temperature-controlled `V Ref`;
- printed p. 2-19: sense-amplifier sensitivity/control relation and temperature/voltage compensation context.

Searchable reproduction: <https://manuals.plus/m/6a52c8f6a4c6271b0377de2d2fbb4a0f9e85fa7664c54f0fc366b0c3d34a04b6>

### IBM FEMM `SY26-5956-6`, Seventh Edition, February 1970

- printed p. 1-46: single-address failures; nominal 60 °F–90 °F room environment; temperature-dependent peak timing/amplitude; low-temperature current requirement and bit dropping;
- waveform discussion around printed pp. 1-50–1-51: `delta noise` defined as sense-line signal from half-selected cores and required to decay below 7 mV at strobe time;
- printed p. 4-3: optimum core-storage adjustments, sealing of factory pots, closed-cover requirement for temperature tracking, and `VRef` adjustment access hole.

Searchable reproduction: <https://manuals.plus/m/9309685d528c91a62ad1e5c75b40c09becd58c088be4d41de6fb0ff3f02a83c0>
