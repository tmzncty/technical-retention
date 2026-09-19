# Case 70 Deepening — DEC MF11-U/UP Field Verification, Factory Calibration, and Replacement Authority (1973–1974)

## Status

**bounded deepening complete**

## Purpose

Case 70 already has three named production/service witnesses for magnetic-core operating margin: IBM 1800, DEC MM11-S, and DEC PDP-8/E MM8-E. Those records establish that installed magnetic-core reliability depended on current, timing, temperature, sense/noise, and service qualification rather than on remanence alone.

One narrower question remains useful for the retention project:

> when a service organization can *observe* that a core-memory operating margin is wrong, does it also possess authority to *re-establish* the underlying calibration locally?

Digital Equipment Corporation's **MF11-U/UP Core Memory System Maintenance Manual**, first edition September 1973 and second printing revised March 1974, provides a unusually explicit answer for the bounded G235 X-Y Driver path. The manual exposes:

- product X-Y current margins;
- temperature-compensated current-generation circuitry;
- a six-month preventive-maintenance cadence;
- direct field checks of sense-strobe delay and drive-current proxy;
- deliberate high/low drive-current and early/late strobe margin tests;
- diagnostic acceptance criteria;
- factory-cut calibration jumpers that field personnel are told not to change;
- module replacement and factory return when correction would require jumper reconfiguration.

The resulting retention-specific boundary is:

```text
field observability
    !=
field calibration authority
    !=
module replacement authority
    !=
factory repair authority
```

This slice does **not** turn Case 70 into a general PDP-11 memory history. It isolates how a retained magnetic state depends on an operating region whose verification and adjustment rights are organizationally distributed.

---

## Source and inspection boundary

Primary source:

- Digital Equipment Corporation, **_MF11-U/UP Core Memory System Maintenance Manual_**, `DEC-11-HMFMA-B-D`, first edition September 1973, second printing (rev.) March 1974. Archival searchable scan: <https://bitsavers.org/pdf/dec/pdp11/memory/MF11-U/DEC-11-HMFMA-B-D_MF11-U_UP_Core_Memory_System_Maintenance_Manual_197403.pdf>.

The same manual family is also preserved under later/alternate archive copies, including `EK-MF11U-MM-003`. The source itself records first edition September 1973 and second printing (rev.) March 1974; the present slice uses the March-1974 archival path as the bounded baseline.

The web research environment exposed page-preserving searchable text from the scanned PDF. Attempts to open/render the large PDF through the available screenshot path failed because the archive endpoint returned either access or document-size errors. Therefore this record makes **no claim that depends on visual interpretation of schematics, waveform geometry, line weight, or typography**. Claims are limited to searchable text/tables from the manual, especially Table 1-1, §§3.6.3–3.6.4, 5.2.3, 5.3, and 5.4.2.

A later community summary at Computer History Wiki was used only as discovery assistance; where the manual is available, the historical claims below rest on the DEC manual itself.

---

## Historical record (H/P)

### H1 — the MF11-U/UP is a named coincident-current core-memory product with published current margins

DEC's Table 1-1 identifies the MF11-U as magnetic-core, read/write, coincident-current, random-access memory in a planar 3D, 3-wire organization. It gives X-Y current margins of:

- `±6% @ 0°C`;
- `±7% @ 25°C`;
- `±6% @ 50°C`.

The same product table gives an ambient operating range of `0°C to 50°C`.

These are product specifications, not universal ferrite-memory constants and not a measured distribution of all shipped units.

### H2 — DEC explicitly ties correct core switching to controlled pulse amplitude, duration, and shape

In the drive-current theory section, DEC states that optimum core switching requires current pulses of precise **amplitude, duration, and shape**. It says current amplitude is controlled by the DC bias-current supply, which is **temperature compensated**; pulse shaping uses resistors, diodes, zeners, and anti-overshoot circuitry; pulse duration is controlled by timing pulses from delay lines.

The manual therefore does not present magnetic-core operation as a binary choice between `has current` and `has no current`. It exposes a controlled analog operating region around the logical operation.

### H3 — the bias reference uses a stack thermistor and provides an explicit margining interface

The same section describes a resistor network including a **stack thermistor** that supplies a temperature-compensated reference to the bias-current control amplifier.

It also exposes two margining inputs on the G235 path: grounding one pin through a `470 kΩ` resistor changes the bias-current amplitude in one direction, while grounding the other through the same resistance changes it in the other direction. DEC states that this capability is important for **margining the memory**.

Thus the product contains both:

```text
normal compensated operating control
and
deliberate service perturbation inputs
```

The latter are not evidence that normal operation continually sweeps the margin range.

### H4 — some bias calibration is explicitly factory-set

The manual cautions that G235 jumpers `W5`, `W6`, and `W7` are **factory cut** to adjust bias current to its optimum value and **should not be changed**.

This is an unusually direct historical statement about calibration authority. The hardware is physically configurable, but the maintenance contract does not treat that configurability as ordinary field-service permission.

### H5 — read-X current rise time is singled out because it strongly affects the recovered core signal

DEC says the read-X current generator contains additional control because the **core output signal is more dependent on read-X current rise time than any other** current generator in the memory. The manual explains that read-Y current flows before read-X, so read-X performs the actual core switching.

That is a product-specific relation among drive waveform and recoverable signal. It should not be generalized into a universal statement about all coincident-current arrays.

### H6 — inhibit-current description supplies another bounded current witness

For the G114 inhibit driver, the manual says each leg of the sense/inhibit path sees approximately half the inhibit current, about `370 mA`.

This value is a bounded circuit witness, not a product-wide tolerance specification and not a universal inhibit-current requirement for core memory.

### H7 — preventive maintenance is explicitly periodic, but it is not refresh

Section 5.3 defines preventive maintenance as tasks performed at intervals to detect conditions that could lead to performance deterioration or malfunction. DEC recommends the following **every six months**:

- visual inspection;
- voltage measurements;
- sense-strobe delay check;
- drive-current check;
- parity timing check where applicable;
- strobe and drive-current margin checks;
- MAINDEC testing.

The manual also states that tests and adjustments are to be performed at an ambient temperature of `20°C to 30°C`.

This six-month cadence is a **human/service diagnostic schedule**. It is not an electrical refresh period, not a requirement to rewrite every stored word every six months, and not the quiescent retention lifetime of the ferrite state.

### H8 — field service can directly verify sense-strobe timing

Section 5.3.3 gives a check on the G235 Driver Module. It specifies a sense-strobe delay of `160 ns ±20%` after the X read driver turns on and defines the measurement between explicit voltage points on two waveforms/pins.

This establishes a field-observable timing acceptance relation.

It does not by itself authorize changing the factory jumper configuration that establishes the underlying timing circuitry.

### H9 — field service can directly verify a drive-current proxy

Section 5.3.4 instructs the technician to connect a digital voltmeter between pin `AK2` and `+5 V` on the G235 Driver Module. DEC says the drive current is **factory-set to provide appropriate drive margins** and should yield `365 mV ±15% below +5 V at 25°C` at that measurement point.

The manual's theory section explains why this voltage tracks the bias current sufficiently accurately for service measurement.

Therefore the service document distinguishes:

```text
factory-set current operating point
!=
field-measurable proxy for that operating point
```

### H10 — installation/service margining deliberately perturbs both current and timing

The strobe/drive margin procedure refers to installation steps 15–20. Those steps instruct the technician to:

1. run the applicable diagnostics normally;
2. use a `470 kΩ` resistor at one G235 margin input and run two passes of the memory exerciser at one drive-current margin;
3. move that resistor to the other input and run two passes at the opposite drive-current margin;
4. use a `3.9 kΩ` resistor to force the sense strobe **early** and run two passes;
5. move the same resistor to force the sense strobe **late** and run two passes;
6. remove the resistor and rerun the diagnostic to reverify normal operation.

The manual calls the two drive-current conditions `high` and `low` memory drive current in this procedure.

This is an installed-system margin test, not a direct material hysteresis experiment and not a measurement of shelf-retention duration.

### H11 — diagnostic acceptance is explicit but bounded

Section 5.3.7 says to run all applicable MAINDEC diagnostic programs for a **minimum of two passes** and that **no errors are permitted**.

That is an operational acceptance criterion under the documented test conditions. It is not a statistical bit-error-rate estimate, a lifetime guarantee, or proof that every possible access pattern has been exercised.

### H12 — failure can be observable in the field while correction remains factory-authorized

Section 5.4.2 is the key authority boundary. DEC states that correction of a sense-strobe-delay or drive-current failure on the G235 that would require reconfiguration of circuit jumpers **should not be attempted in the field**. The instruction is to:

```text
replace the faulty G235 with a spare
    ->
return the faulty G235 to the factory for repair
```

The same manual has already given the field technician the checks needed to determine that timing/current behavior is outside the allowed service condition.

Hence the historical record directly supports:

```text
field detection authority
!=
field calibration authority
```

and, for this failure path:

```text
field correction by module replacement
!=
field correction by jumper retuning
```

---

## Engineering reconstruction (E)

### E1 — retention margin is partly an organizationally maintained relation

The ferrite core's remanence is material, but a usable stored symbol in the MF11-U/UP depends on drive amplitude, waveform, timing, temperature compensation, sensing, and acceptance testing.

The manual adds a further layer: the organization decides **who may change the controls that establish that operating region**.

A bounded reconstruction is therefore:

```text
remanent magnetic state
    +
qualified drive/sense operating region
    +
maintenance observability
    +
authorized correction path
    ->
continued service recoverability
```

`authorized correction path` is a project-level reconstruction, not DEC's philosophical vocabulary.

### E2 — observability does not imply mutability

The manual gives field personnel instrumentation points and pass/fail criteria for strobe delay and drive current, yet tells them not to reconfigure the relevant jumpers when that would be needed to correct a failure.

So:

```text
state is observable
!=
state is field-adjustable
```

This is a useful retention distinction beyond magnetic core. Technical systems frequently expose enough evidence to diagnose a maintenance state without granting the observer authority to mutate the state that controls it.

### E3 — replacement can restore service without preserving calibration identity

If a G235 fails a field check requiring jumper reconfiguration, DEC's documented correction is to replace it with a spare rather than locally reproduce the factory calibration of the failed board.

The safest reconstruction is:

```text
restore acceptable memory service
!=
preserve identity of the original calibrated module
```

The source does not prove that every spare has identical analog values, nor does it disclose the factory procedure by which every spare's jumpers were selected. It establishes only that DEC's service contract treats replacement as the approved field path.

### E4 — a service cadence is a maintenance schedule, not a payload-restoration clock

The six-month preventive-maintenance recommendation periodically checks conditions that may precede malfunction. Ferrite payload state does not need rewriting on that schedule merely to remain magnetized.

Thus:

```text
human preventive-maintenance cadence
!=
payload refresh cadence
!=
remanent retention lifetime
```

This prevents a cross-technology terminology mistake when comparing magnetic-core service practice with DRAM refresh or Flash rewrite/reclaim.

### E5 — operating envelope and service-test envelope remain different contracts

The product table gives `0–50°C` ambient operation while the maintenance chapter constrains tests/adjustments to `20–30°C`.

Therefore:

```text
supported operating environment
!=
allowed/controlled calibration-test environment
```

This matches the same methodological boundary already seen in the MM11-S evidence, but here it is tied directly to a different product family's field/factory authority split.

### E6 — deliberate perturbation creates evidence about margin, not a new payload state

The high/low current and early/late strobe tests deliberately move the system away from its normal service point while diagnostics check correct operation.

The result is evidence about the **operating region**. It should not be confused with the retained user payload itself.

```text
payload state
!=
maintenance perturbation state
!=
diagnostic result
```

### E7 — a passing diagnostic is evidence with a bounded horizon and scope

Two passing MAINDEC passes under the prescribed margin conditions establish the manual's acceptance requirement at that time. They do not prove indefinite future correctness.

The evidence relation is therefore:

```text
qualified now under named conditions
!=
guaranteed forever
```

This is a general engineering lesson, but the historical premise is confined to DEC's documented test procedure.

---

## Functional comparison (FA)

### MF11-U/UP versus MM11-S

Both are DEC coincident-current core-memory products and both publish the same three-point X/Y-current margins (`±6%`, `±7%`, `±6%` at `0/25/50°C`). That similarity should not be inflated into full design identity.

The useful contrast is in the service surface documented here:

- MF11-U/UP exposes a `365 mV ±15%` field check at the G235 bias-current measurement point;
- MF11-U/UP's preventive-maintenance path deliberately forces high/low current and early/late strobe conditions with external resistors;
- MF11-U/UP explicitly forbids field jumper reconfiguration for the relevant correction and directs module replacement/factory return;
- MM11-S evidence instead emphasizes its own factory-set `410 ±5 mA` current, product strobe margins, midpoint strobe error-boundary search, and worst-case-plane-noise diagnostic.

Therefore:

```text
same vendor
+
same broad current-margin specification
!=
same maintenance interface
!=
same calibration authority surface
```

No direct design-lineage claim is made.

### MF11-U/UP versus MM8-E

The MM8-E witness in Case 70 exposes some controls that the service manual distinguishes as field-adjustable and others that are factory-only. MF11-U/UP sharpens the boundary further for a named module: field personnel may measure and margin-test the G235, but a correction requiring jumper reconfiguration is explicitly redirected to module replacement and factory repair.

The shared functional lesson is only:

> installed core-memory retention depends on a qualified operating region whose maintenance controls can have different administrative owners.

The procedures and circuitry are not treated as identical.

### MF11-U/UP versus IBM 1800

IBM 1800 evidence in Case 70 exposes temperature-related signal/strobe relations, a half-select delta-noise criterion, and a closed-cover requirement during adjustment. MF11-U/UP instead makes the **division of service authority** unusually explicit.

The cross-machine comparison therefore broadens Case 70 from numeric margins alone to the control relation around those margins:

```text
margin quantity
+
measurement method
+
allowed adjustment context
+
repair authority
```

These are comparable dimensions, not evidence of shared IBM/DEC genealogy.

### MF11-U/UP versus DRAM refresh — functional analogy only

Both may involve scheduled maintenance activity, but the schedules are categorically different:

- DRAM refresh revisits payload state before an electrical retention deadline;
- MF11-U/UP six-month preventive maintenance checks the operating apparatus for deterioration/malfunction.

So:

```text
periodic maintenance
!=
periodic payload refresh
```

No historical continuity is asserted.

---

## Philosophical interpretation — bounded

This slice supports one narrow project-level interpretation:

> Technical persistence may depend not only on a material state and a physical apparatus, but on an institutional distribution of observation, intervention, replacement, and repair authority.

The MF11-U/UP manual makes that visible without needing a metaphor. A technician can know that the operating relation has failed while being instructed **not** to recreate the factory calibration locally. Continued availability is restored through an authorized replacement path and a different repair locus.

That is a present-day interpretation disciplined by the manual. DEC did not describe the arrangement as a philosophy of retention, institutional memory, or distributed agency.

---

## Rejected / unsupported upgrades (X)

This evidence does **not** establish that:

- `±6%`, `±7%`, `160 ns ±20%`, `365 mV ±15%`, or `370 mA` are universal magnetic-core constants;
- every MF11-U/UP shipped with exactly identical analog calibration;
- the product always fails immediately outside the listed current or timing limits;
- the `20–30°C` maintenance-test range is the only supported operating range;
- the `0–50°C` product range means the documented adjustment procedure is valid everywhere in that range;
- the six-month preventive-maintenance interval is a payload refresh period or ferrite retention lifetime;
- two clean MAINDEC passes establish a lifetime BER, field reliability distribution, or exhaustive fault coverage;
- high/low current or early/late strobe margin tests intentionally corrupt payload state;
- a failed timing/current check proves that the ferrite cores themselves are defective;
- replacing the G235 preserves the exact analog calibration values or identity of the removed module;
- spare-module replacement proves that all G235 boards are freely interchangeable under every hardware revision;
- the manual discloses DEC's full factory jumper-selection procedure;
- factory return is evidence that the factory necessarily repaired rather than replaced every failed board;
- MF11-U/UP and MM11-S share identical internal circuitry merely because their published X/Y current-margin percentages match;
- DEC and IBM service methods have a demonstrated genealogy;
- this record settles invention priority for temperature compensation, margining, module replacement, or preventive maintenance;
- magnetic-core service margining is technically identical to DRAM refresh, RowHammer mitigation, or NAND read reclaim.

---

## What this slice closes

This closes a bounded part of Case 70's remaining **cross-machine operating-margin** debt by adding a fourth named production/service witness with a distinct research value:

- IBM 1800 exposes temperature/sense/noise relations;
- DEC MM11-S exposes temperature-indexed current/strobe margins and worst-case traffic qualification;
- DEC MM8-E exposes service working-window selection and split adjustment authority;
- DEC MF11-U/UP now exposes **field verification + deliberate margin perturbation + factory calibration restriction + module-replacement/factory-return authority** in one manual.

The new result is not another universal tolerance number. It is the bounded relation:

```text
observable margin state
    -> field qualification evidence
    -> if correction requires protected calibration change:
       replace module in field
       + move calibration repair to factory
```

Still open:

- statistically meaningful unit-to-unit and lot-to-lot margin distributions;
- field-return/failure-rate records;
- factory calibration worksheets or production correspondence explaining how G235 jumpers were selected;
- deployed ferrite/core-vendor distributions;
- controlled hardware reproduction of the high/low-current and early/late-strobe procedures;
- exact revision-by-revision interchangeability limits for G235/H217 combinations;
- broader PDP-11 core-memory product genealogy and manufacturing organization.

Those broader engineering-history questions belong primarily in `tmzncty/computing-archaeology`.

---

## Related-repository reuse

The general magnetic-core mechanism, manufacturing labor, coincident-current selection, and destructive-read history are already covered in:

- <https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md>

Fresh searches for `MF11-U` and its margin/calibration authority boundary did not find a dedicated companion packet. This evidence therefore keeps only the retention-specific seam:

```text
remanent payload
    -> qualified analog operating region
    -> field-observable margin evidence
    -> bounded field intervention authority
    -> module replacement / factory repair path
    -> restored service qualification
```

A fuller MF11-U/MM11-U hardware genealogy, manufacturing/calibration history, option/backplane evolution, and board-revision archaeology should be developed in `computing-archaeology` rather than duplicated here.

---

## Claim ledger

| ID | Claim | Type | Evidence status |
| --- | --- | --- | --- |
| 70-MF-01 | DEC's MF11-U/UP manual publishes X/Y current margins of ±6% @0°C, ±7% @25°C, ±6% @50°C | H/P | direct in Table 1-1 |
| 70-MF-02 | The product operating range is 0–50°C while service tests/adjustments are constrained to 20–30°C | H/P + E | direct in Table 1-1 and §5.3; bounded comparison |
| 70-MF-03 | DEC describes drive amplitude as temperature compensated and tied to a stack-thermistor reference | H/P | direct in §3.6.3 |
| 70-MF-04 | G235 W5/W6/W7 bias-current jumpers are factory cut and should not be changed | H/P | direct caution in drive-current section |
| 70-MF-05 | Sense-strobe delay is field-checkable at 160 ns ±20% | H/P | direct in §5.3.3 |
| 70-MF-06 | Drive-current proxy is field-checkable at 365 mV ±15% below +5 V at 25°C and is described as factory-set for appropriate margins | H/P | direct in §5.3.4 |
| 70-MF-07 | Service margining deliberately forces high/low current and early/late strobe conditions and reruns diagnostics | H/P | direct in installation steps 16–20 / §5.3.6 |
| 70-MF-08 | Preventive maintenance is recommended every six months and includes margin/diagnostic checks | H/P | direct in §5.3 |
| 70-MF-09 | Applicable MAINDEC tests require at least two passes with no errors | H/P | direct in §5.3.7 |
| 70-MF-10 | A G235 correction requiring jumper reconfiguration is not to be attempted in the field; replace the module and return it to the factory | H/P | direct in §5.4.2 |
| 70-MF-11 | Field observability does not imply field calibration authority | E | bounded reconstruction from §§5.3.3–5.4.2 |
| 70-MF-12 | Module replacement can restore service without preserving the original module's calibration identity | E | bounded reconstruction; exact spare calibration not claimed |
| 70-MF-13 | Six-month preventive maintenance is not a payload refresh clock or ferrite retention lifetime | E | bounded maintenance-trigger distinction |
| 70-MF-14 | Same published current-margin percentages do not establish identical MM11-S/MF11-U maintenance or circuit semantics | FA | bounded cross-product comparison |
| 70-MF-15 | DEC's service-authority boundary is historically identical to later firmware privilege or distributed repair authority | X | explicitly unsupported |

---

## Primary-source anchors

1. Digital Equipment Corporation, **_MF11-U/UP Core Memory System Maintenance Manual_**, `DEC-11-HMFMA-B-D`, 1st ed. September 1973; 2nd Printing (Rev) March 1974. <https://bitsavers.org/pdf/dec/pdp11/memory/MF11-U/DEC-11-HMFMA-B-D_MF11-U_UP_Core_Memory_System_Maintenance_Manual_197403.pdf>
   - Table 1-1: product type, X/Y current margins, operating environment;
   - §3.6.3: temperature-compensated bias-current supply, stack thermistor, margining inputs, factory-cut W5/W6/W7, read-X rise-time significance;
   - §3.6.4: bounded inhibit-current description;
   - §5.2.3 steps 15–20: deliberate high/low-current and early/late-strobe margin testing;
   - §5.3: six-month preventive-maintenance schedule and 20–30°C test/adjustment condition;
   - §5.3.3: `160 ns ±20%` sense-strobe delay check;
   - §5.3.4: `365 mV ±15%` drive-current proxy at 25°C;
   - §5.3.7: minimum two diagnostic passes, no errors permitted;
   - §5.4.2: no field jumper reconfiguration for the bounded G235 failure path; replace spare / return faulty module to factory.

2. Digital Equipment Corporation, **_MF11-U/UP Core Memory System Maintenance Manual_**, later archive copy `EK-MF11U-MM-003`, used only as a continuity/alternate-access witness where searchable extraction was clearer. <https://bitsavers.trailing-edge.com/www.computer.museum.uq.edu.au/pdf/EK-MF11U-MM-003%20MF11-U%26UP%20Core%20Memory%20System%20Maintenance%20Manual.pdf>

## Secondary discovery only

- Computer History Wiki, **"MM11-U core memory"**, useful for locating the same G235 jumper/service passage but not used where the DEC manual directly supports the claim: <https://gunkies.org/wiki/MM11-U_core_memory>.
