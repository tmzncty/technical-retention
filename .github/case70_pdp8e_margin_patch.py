from pathlib import Path
import re


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"anchor missing in {path}: {old[:180]!r}")
    if text.count(old) != 1:
        raise SystemExit(f"anchor not unique in {path}: {old[:180]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


def insert_after_once(path: str, anchor: str, addition: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if anchor not in text:
        raise SystemExit(f"anchor missing in {path}: {anchor[:180]!r}")
    if text.count(anchor) != 1:
        raise SystemExit(f"anchor not unique in {path}: {anchor[:180]!r}")
    p.write_text(text.replace(anchor, anchor + addition, 1), encoding="utf-8")


evidence_path = Path("evidence/70-dec-pdp8e-1973-operating-margin-deepening.md")
case_path = "cases/70-magnetic-core-half-select-disturbance.md"
roadmap_path = "ROADMAP.md"
index_path = Path("CASE_INDEX.md")

if evidence_path.exists():
    raise SystemExit(f"evidence already exists: {evidence_path}")

EVIDENCE = r'''# Case 70 Deepening — DEC PDP-8/E MM8-E Production Operating-Margin Qualification (1973)

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
'''

evidence_path.write_text(EVIDENCE, encoding="utf-8")

# Scope: preserve the early mechanism focus but declare the bounded 1973 named-machine witness.
replace_once(
    case_path,
    "- **Date range:** 1951–1959 for the evidence used here, with the principal design work concentrated in 1951–1954 and one 1954-filed IBM patent published in 1959;\n- **Principal sources:** Jay W. Forrester's 1951-filed multicoordinate-storage patent, William N. Papian's April 1952 IRE paper as preserved by MIT, and Edwin W. Bauer / Munro K. Haynes's 1954-filed IBM disturbance-cancellation patent;",
    "- **Date range:** 1951–1959 for the principal mechanism evidence, with one bounded 1973 named-machine production/service witness for operating-margin qualification;\n- **Principal sources:** Jay W. Forrester's 1951-filed multicoordinate-storage patent, William N. Papian's April 1952 IRE paper as preserved by MIT, Edwin W. Bauer / Munro K. Haynes's 1954-filed IBM disturbance-cancellation patent, and DEC's September 1973 PDP-8/E MM8-E maintenance manual;"
)

pdp_section = r'''
## PDP-8/E MM8-E production operating-margin deepening (1973)

The earlier sources establish *why* coincident-current arrays need disturbance and sensing margin. DEC's September 1973 PDP-8/E maintenance manual now supplies a named production/service witness for *how an installed machine operationalized part of that margin*. See [`../evidence/70-dec-pdp8e-1973-operating-margin-deepening.md`](../evidence/70-dec-pdp8e-1973-operating-margin-deepening.md).

For the MM8-E, DEC lists separately controlled field-select, strobe, slice, X/Y-current, and temperature-tracking variables. Slice has four discrete levels (`-4.3`, `-4.8`, `-5.3`, `-6.0 V`); the X/Y current-control table gives four control-voltage offsets (`+3.7%`, `+2.2%`, nominal `~3.5 V at 25 °C`, `-1.7%`) and a corresponding nominal X/Y current of `370 mA`; nominal inhibit current is `340 mA`. A thermistor-resistor divider feeds the current-control circuit for temperature tracking.[^dec]

The strobe procedure is especially useful. A six-position switch moves timing in `10 ns` increments. Field service runs `Memory Checkerboard`, walks the strobe until errors appear in each direction, requires at least **three consecutive working positions**, selects the middle working position, and during checkout runs the adjacent left/right positions for at least **15 minutes** without errors.[^dec]

This yields a production-level distinction not present in the laboratory evidence alone:

```text
remanent state survives at rest
!=
installed memory has adequate powered operating margin
!=
a chosen service setting has passed qualification
```

The passing strobe window is an **operational diagnostic margin**, not a measured shelf-retention lifetime. The 15-minute adjacent-position check is not a bit-error-rate or lifetime guarantee. Likewise, the listed current/slice alternatives are calibration choices, not proof that every stack passes at every setting.

DEC also divides adjustment authority: strobe and field select can be set by factory or field service, while slice, X/Y current control, and temperature tracking are factory-only. Thus `manufacturing calibration authority != field maintenance authority` for this bounded machine.[^dec]

Papian and DEC should not be collapsed. Papian measures material/pulse-regime disturbance and signal ratios; DEC qualifies an installed system's service operating region. They are complementary layers, and no direct procedural genealogy is asserted.

---

'''
insert_anchor = "---\n\n## Historical record"
replace_once(case_path, insert_anchor, pdp_section + "## Historical record")

# Add DEC as a primary source before the reused-history subsection and renumber that reused item.
replace_once(
    case_path,
    "### Reused engineering history\n\n4. [`computing-archaeology: Why Was Magnetic-Core Memory Worth Weaving by Hand?`]",
    "4. **Digital Equipment Corporation, _PDP-8/E, PDP-8/F & PDP-8/M Maintenance Manual, Volume 1: Processor_, DEC-8E-HMM1A-D-D, 7th Printing (Rev), September 1973.** Sections 4.7.2–4.7.9 give MM8-E current, slice, temperature-tracking, and strobe-setting controls plus a checkerboard-based working-window procedure.[^dec]\n\n### Reused engineering history\n\n5. [`computing-archaeology: Why Was Magnetic-Core Memory Worth Weaving by Hand?`]"
)

# Extend the claim ledger with the bounded named-machine evidence.
ledger_anchor = "| Word selection can differ from bit-level permission to switch in the bounded inhibit scheme | H/P + E | IBM patent description |\n"
ledger_add = "| MM8-E service documentation exposes separate strobe, slice, X/Y-current, temperature-tracking, and field-selection controls | H/P | direct in DEC September 1973 maintenance manual §§4.7.2–4.7.9 |\n| A reliable MM8-E is required to show at least three consecutive working 10-ns strobe positions before midpoint selection | H/P | direct in DEC strobe-setting procedure |\n| Adjacent-position checkerboard runs for at least 15 minutes are service qualification, not a measured remanent-retention lifetime | E | bounded reconstruction from the DEC acceptance procedure |\n| Factory-only slice/current/temperature controls differ from field-adjustable strobe/field select | H/P + E | DEC Table 4-6 plus maintenance-authority reconstruction |\n| Papian material disturbance testing and DEC installed-system margin qualification are complementary but not identical evidence layers | FA | bounded cross-source comparison; no genealogy asserted |\n"
insert_after_once(case_path, ledger_anchor, ledger_add)

# Add named-machine-specific limit after the universal-threshold caution.
limit_anchor = "### The current evidence does not establish one universal half-select failure threshold\n\nCore materials, geometry, pulse amplitude, temperature, winding organization, and sense circuitry varied. Papian establishes that repetitive nonselecting disturbance was measured and materially discriminating; this case does not infer one universal pulse count or margin.\n"
limit_add = r'''
### The PDP-8/E maintenance numbers are not universal core constants

The MM8-E's `370 mA` nominal X/Y current, `340 mA` nominal inhibit current, discrete slice levels, and 10-ns strobe taps are settings of this bounded DEC design. The checkerboard working window qualifies service operation; it is not a universal material-switching curve, a continuous symmetric timing tolerance, or a remanent shelf-life measurement.

'''
insert_after_once(case_path, limit_anchor, "\n" + limit_add)

# Add DEC source note.
source_anchor = "[^bauer]: Edwin W. Bauer and Munro K. Haynes, **\"Magnetic Memory System with Disturbance Cancellation,\"** U.S. Patent 2,889,540, application filed July 14, 1954, issued June 2, 1959, International Business Machines Corporation. Google Patents HTML transcription: https://patents.google.com/patent/US2889540A/en\n"
source_add = "\n[^dec]: Digital Equipment Corporation, **_PDP-8/E, PDP-8/F & PDP-8/M Maintenance Manual, Volume 1: Processor_**, `DEC-8E-HMM1A-D-D`, 7th Printing (Rev), September 1973, especially §§4.7.2–4.7.9 / printed pp. 4-20–4-22. Archival catalogue: https://manx-docs.org/details.php/1%2C4017 ; searchable extraction of the original manual: https://device.report/m/f543be6c683c3e08d16eca14f854b69311c27dc3ca837af500c7ec6e85aed20a . The extraction, not the facsimile typography/figures, was inspected in this pass.\n"
insert_after_once(case_path, source_anchor, source_add)

# Close only the named-machine witness debt in status.
replace_once(
    case_path,
    "Remaining work is narrower archival/production deepening: named-machine quantitative margins, deployed-material distributions, temperature dependence, and invention-priority genealogy if later synthesis requires them.",
    "One named-machine production/service operating-margin slice is now closed by [`../evidence/70-dec-pdp8e-1973-operating-margin-deepening.md`](../evidence/70-dec-pdp8e-1973-operating-margin-deepening.md). Remaining work is narrower archival/production deepening: cross-machine margin distributions, deployed-material distributions, quantitative temperature dependence, earlier production correspondence, and invention-priority genealogy if later synthesis requires them."
)

# ROADMAP: close the Phase-1 wording and record this completed Phase-2 bridge.
replace_once(
    roadmap_path,
    "Remaining magnetic-core work is production/named-machine quantitative margin evidence, temperature/material distributions, and broader genealogy, primarily under Case 70 / `computing-archaeology`.",
    "One named-machine production/service operating-margin slice is now closed by Case 70's PDP-8/E MM8-E deepening. Remaining magnetic-core work is cross-machine margin distributions, temperature/material distributions, earlier production correspondence, and broader genealogy, primarily under Case 70 / `computing-archaeology`."
)

phase2_anchor = "## Phase 2 — Build missing technical bridges\n\n"
phase2_item = "- [x] **Case 70 DEC PDP-8/E MM8-E named-machine operating-margin deepening:** [`cases/70-magnetic-core-half-select-disturbance.md`](cases/70-magnetic-core-half-select-disturbance.md) + [`evidence/70-dec-pdp8e-1973-operating-margin-deepening.md`](evidence/70-dec-pdp8e-1973-operating-margin-deepening.md) close one explicit production/named-machine quantitative-margin debt with DEC's September 1973 maintenance procedure. MM8-E documentation exposes discrete slice/current settings, `370 mA` nominal X/Y current, `340 mA` nominal inhibit current, thermistor-based temperature tracking, and a six-position 10-ns strobe sweep that requires at least three consecutive working positions plus 15-minute error-free checks at adjacent positions before final acceptance. The bounded conclusion is `quiescent remanence != powered operating margin != qualified service setting`; the diagnostic window is not promoted into a retention lifetime, universal core constant, continuous ±tolerance, or failure probability. Papian's laboratory material/pulse evidence and DEC's installed-system qualification are treated as complementary layers without asserting genealogy. Cross-machine margin distributions, deployed material/temperature distributions, earlier production correspondence, and priority history remain open; broader core-memory engineering history stays in `computing-archaeology`.\n\n"
insert_after_once(roadmap_path, phase2_anchor, phase2_item)

# CASE_INDEX: allocate the next 16 IDs dynamically so a concurrent case cannot collide.
idx = index_path.read_text(encoding="utf-8")
if "Case 70 DEC PDP-8/E MM8-E production operating margin" in idx:
    raise SystemExit("Case 70 PDP-8/E findings already present")
nums = [int(x) for x in re.findall(r"\*\*(\d+)\s+—", idx)]
if not nums:
    raise SystemExit("could not find existing finding numbers in CASE_INDEX.md")
start = max(nums) + 1
entries = [
    ("H/P", "DEC's September 1973 `DEC-8E-HMM1A-D-D` maintenance manual supplies a named PDP-8/E MM8-E production/service witness rather than a laboratory-only core-material record."),
    ("H/P", "MM8-E Table 4-6 treats field select, strobe, slice, X/Y current control, and temperature tracking as distinct memory-circuit variables rather than one scalar margin setting."),
    ("H/P", "The same table assigns strobe and field select to factory or field service while slice, X/Y current control, and temperature tracking are factory-only settings."),
    ("H/P", "DEC lists four slice levels for the G104 path: `-4.3 V`, `-4.8 V`, `-5.3 V`, and `-6.0 V`, and explicitly warns against field adjustment."),
    ("H/P", "The G227 X/Y current-control table exposes four discrete control-voltage choices (`+3.7%`, `+2.2%`, nominal `~3.5 V at 25 °C`, `-1.7%`) and gives a corresponding nominal X/Y current of `370 mA`."),
    ("H/P", "MM8-E inhibit current is documented as fixed in adjustment but proportional to the `-15 V` supply, with nominal value `340 mA`."),
    ("H/P", "A thermistor-resistor network on the memory stack board feeds a temperature-sensitive divider into the current-control circuit, making temperature tracking part of the documented operating-control path."),
    ("H/P", "The MM8-E strobe uses a six-position switch with discrete `10 ns` steps; field service is instructed to run `Memory Checkerboard` while moving toward error boundaries in both timing directions."),
    ("H/P", "DEC's reliability criterion requires at least three consecutive working strobe positions and then selects the middle working position, favoring the more delayed center position when the count is even."),
    ("H/P", "Checkout requires the checkerboard to run at the middle position and for at least `15 minutes` at each adjacent position without error; acceptance is run only at the final strobe position."),
    ("E", "The observed checkerboard pass window is evidence of an installed-system operational timing margin; it is not a measurement of unpowered remanent-retention duration."),
    ("E/X", "Three or more passing 10-ns taps plus midpoint selection support a robustness reconstruction but do not prove a continuous symmetric `±10 ns` analog tolerance or a quantified failure probability."),
    ("E", "Temperature-sensitive current control means the nominal room-temperature voltage/current point is not the whole operating relation; this evidence still does not supply a core-material temperature coefficient or deployed-material distribution."),
    ("E", "`manufacturing calibration authority != field maintenance authority`: DEC intentionally restricts slice/current/temperature settings while allowing field adjustment of strobe and field select."),
    ("FA", "Papian's 1952 material/pulse-regime disturbance measurements and DEC's 1973 installed-system service qualification are complementary margin evidence layers; the comparison does not establish direct procedural genealogy."),
    ("X", "The MM8-E values (`370 mA`, `340 mA`, slice levels, 10-ns taps, 15-minute checkout) are not universal magnetic-core constants, retention guarantees, sanitization evidence, or proof that every available calibration setting passes."),
]
end = start + len(entries) - 1
lines = [f"### Findings {start}–{end} — Case 70 DEC PDP-8/E MM8-E production operating margin", ""]
for i, (kind, text) in enumerate(entries, start):
    lines.append(f"- **{i} — {kind}** — {text}")
index_path.write_text(idx.rstrip() + "\n\n" + "\n".join(lines) + "\n", encoding="utf-8")

print(f"created {evidence_path}")
print(f"appended CASE_INDEX findings {start}-{end}")
