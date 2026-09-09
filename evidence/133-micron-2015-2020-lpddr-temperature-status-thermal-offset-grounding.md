# Case 133 grounding — LPDDR temperature status, polling freshness, and controller thermal offset (2015–2020)

## Research question

What primary product evidence is sufficient to ground a later LPDDR retention-control relation in which:

1. a device reports a temperature-derived refresh-rate class;
2. that report has bounded update/poll/response freshness;
3. a controller can compensate for a hot spot that is spatially displaced from the on-die sensor;
4. the compensation affects TCSR/refresh behavior;
5. the source itself states a thermal-gradient boundary beyond which self refresh is not reliably retention-safe?

This record is deliberately narrower than a JEDEC standards history and narrower than a general history of LPDDR thermal management.

## Source set and custody

### A. Micron 512Mb Automotive Mobile LPDDR2, Rev. J 10/15

Manufacturer: Micron Technology, Inc.

Document: `u67m_512mb_aat-ait_mobile_lpddr2.pdf - Rev. J 10/15 EN`, ©2012 Micron.

Public copy inspected through DigiKey's manufacturer-datasheet mirror:

<https://media.digikey.com/pdf/Data%20Sheets/Micron%20Technology%20Inc%20PDFs/MT42L32M16D1,%2032D2,%20MT42L16M32D1_Web.pdf>

Important anchors:

- printed p. 35 / PDF page 34: MR4 `SDRAM refresh rate` and `Temperature update flag (TUF)`;
- same table notes: MR4 read resets TUF; TUF is 0 at power-up; TUF is set when `OP[2:0]` changes since the prior read;
- same note set: automotive sensor status is not an exact reflection of `TCASE`, with sampled variance up to ±7°C in the bounded part;
- printed pp. 73–75 / PDF pages 72–74: Temperature Sensor, `tTSI`, `ReadInterval`, `SysRespDelay`, 2°C `TempMargin`, polling equation, worked 167 ms example.

### B. Micron LPDDR4/LPDDR4X, Rev. E 8/2020

Manufacturer: Micron Technology, Inc.

Document: `z32m_embedded_lpddr4_lpddr4x.pdf – Rev. E 8/2020 EN`, ©2019 Micron, parts `MT53E1G16D1`, `MT53E1G32D2`, `MT53E2G32D4`, `MT53E1G64D4`.

Public copy inspected through a TI E2E file attachment:

<https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/908/MT53E1G16D1FW_2D00_046-AIT--A-MCR-Datenblatt_2800_P010694655_2900_.pdf>

Important anchors:

- printed p. 1: `On-chip temperature sensor to control self refresh rate`;
- printed p. 57 / PDF page 56: MR4 `OP[2:0]` refresh-rate status, `OP[6:5]` `Thermal offset-controller offset to TCSR`, and `OP7` TUF;
- printed pp. 57–58: TUF read-to-clear and power-up semantics;
- printed p. 204 / PDF page 203: Thermal Offset + beginning of Temperature Sensor;
- printed p. 205 / PDF page 204: polling relation and `tTSI = 32 ms`, `TempMargin = 2°C` table / worked example.

The Thermal Offset section states, in substance, that tight coupling to an SoC can create hot spots away from the memory sensor, which can leave TCSR generating too few refresh cycles; a controller-provided offset can adjust TCSR. It gives a maximum 200 µs before the change appears in MR4 `OP[2:0]`, requires knowledge of sensor location, and says a sensor-to-hot-spot gradient greater than 15°C falls outside reliable self-refresh retention.

### C. SK hynix LPDDR4, Rev. 1.1 8/2020

Manufacturer: SK hynix.

Document: `H54G46BYYV(Q/P)X053 LPDDR4 16Gb (x16, 2 Channel, 1CS)`, Rev. 1.1, August 2020.

Public copy inspected through a TI E2E file attachment:

<https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/791/6888.Automotive_5F00_DA-16Gb-LPDDR4_5F00_H54G46BYYV_2800_Q_2C00_P_2900_X053_5F00_Rev1.1.pdf>

Important anchors:

- MR4 definition around printed p. 26;
- `5.37 Thermal offset` around printed p. 182;
- `5.38 Temperature Sensor` around printed pp. 183–184.

The source independently uses the same sensor/hot-spot/TCSR compensation relation and explicitly says thermal-offset support is optional and vendor-datasheet-specific. This source is used only to block universal-product claims, not to reconstruct normative JEDEC revision history.

## Historical record

### H/P — MR4 temperature-derived refresh status and TUF are already visible in bounded LPDDR2 product documentation by 2015

Micron's 2015 LPDDR2 document exposes `OP[2:0]` as a refresh-rate classification and TUF as a read-only indicator of whether that classification changed since the preceding MR4 read. The read clears TUF, and TUF starts at 0 after power-up.

This is an earlier public product-document floor for the broad function. It blocks writing the later LPDDR4 interface as the origin of temperature-status polling.

### H/P — the older product already makes observation cadence part of correct thermal response

The LPDDR2 Temperature Sensor section defines:

- `TempGradient`;
- host `ReadInterval`;
- sensor-update delay `tTSI` (max 32 ms);
- `SysRespDelay`;
- a 2°C response margin.

The document constrains them with:

`TempGradient × (ReadInterval + tTSI + SysRespDelay) ≤ 2°C`.

For 10°C/s and 1 ms system response it gives a maximum `ReadInterval` of 167 ms.

The important historical point is not the arithmetic by itself. The product contract already treats **staleness between physical temperature change and controller action** as a bounded timing problem.

### H/P — the bounded LPDDR2 sensor was not an exact case-temperature oracle

The automotive LPDDR2 MR4 notes warn that the embedded sensor is not an accurate reflection of DRAM `TCASE` and report sampled variance up to ±7°C for the product.

This is not reused as the error model of the 2020 LPDDR4 device. It is evidence that `sensor status != exact package temperature` was already explicit manufacturer vocabulary/qualification in an earlier LPDDR generation.

### H/P — Micron LPDDR4 adds a writable controller offset to TCSR

Micron Rev. E 8/2020 defines MR4 `OP[6:5]` as `Thermal offset-controller offset to TCSR` with documented ranges:

- `00b`: no offset, 0–5°C gradient;
- `01b`: 5°C offset, 5–10°C gradient;
- `10b`: 10°C offset, 10–15°C gradient;
- `11b`: reserved.

This is direct manufacturer product evidence that the controller can supply information used by the DRAM's retention-maintenance policy.

### H/P — the reason is spatial representativeness, not merely numerical sensor error

Micron's Thermal Offset prose says an SoC can induce hot spots across the device and that those hot spots may not be near the memory thermal sensor. Because of that displacement, TCSR may produce too few refresh cycles to guarantee memory retention.

The controller offset is therefore a correction for an **environmental relation not fully represented by the sensor location**.

### H/P — control changes and observed status are not instantaneous synonyms

Micron allows up to 200 µs before a thermal-offset change is reflected in MR4 `OP[2:0]`.

The source does not expose internal switch-over atomicity. It does directly establish a bounded delay between writing a control field and observing the resulting refresh-rate status.

### H/P — reliable self-refresh has an explicit thermal-gradient boundary

Micron says that if the induced thermal gradient from the device sensor location to the controller hot-spot location exceeds 15°C, self refresh will not reliably maintain memory contents.

This is a vendor contract boundary. It is **not** a directly observed bit-failure timestamp and not a statement that all bits fail immediately past the threshold.

### H/P — contemporaneous cross-vendor documentation makes thermal-offset support optional

SK hynix August-2020 LPDDR4 documentation presents the same broad relation but says support of thermal offset is optional and vendor-specific.

Therefore the public product record itself blocks a universal implementation claim.

## Engineering reconstruction

### E — sensor reading != complete thermal field

A sensor can be locally accurate enough for its intended role while still being spatially unrepresentative of a hotter point elsewhere on the tightly coupled package/system.

That distinction matters because retention risk depends on the physical condition at memory regions, not on the mere existence of a sensor value.

### E — offset != calibration

The documented target of the offset is TCSR/refresh behavior. There is no basis here for saying it recalibrates the sensor or changes the meaning of the underlying physical measurement.

### E — TUF != history

A read-to-clear flag that records only whether a class changed since last observation is a compressed currentness/change witness. It omits the number of transitions, their timestamps, sensor samples, and their path.

Therefore `TUF = 0` cannot be inflated into `temperature never changed`.

### E — status freshness is a separate maintenance-control deadline

The polling equation separates:

1. environment-changing timescale (`TempGradient`);
2. device status-update latency (`tTSI`);
3. observation latency (`ReadInterval`);
4. actuator/controller response latency (`SysRespDelay`).

These are not the same as the DRAM cell's physical retention time or the refresh command's own execution duration.

### E — the 2°C quantity is not a universal retention margin

The product uses 2°C as a bounded response margin between status change and controller reconfiguration. Nothing in the source authorizes treating it as sensor accuracy, ECC capability, a universal cell thermal tolerance, or a quantitative safety margin for every workload/device.

### E — report != action

MR4 reports a refresh-rate class and can report whether timing derating is required. A report does not itself issue every refresh or reconfigure every controller timing. In self refresh, the device's internal TCSR path performs recurring maintenance; outside that relation, the system/controller still has separate execution authority.

### E — operating-mode label != unconditional preservation

`SELF REFRESH` names a mode and authority arrangement. The >15°C warning proves that the mode's presence alone is weaker than the environmental conditions under which its retention guarantee is valid.

### E — control configuration lifetime remains unproven across reset/power loss

The existence of writable MR4 offset bits grounds an operating control relation only. This record does not establish their persistence horizon across reset, power loss, or package replacement.

## Functional analogy — bounded

### Case 34 — temperature-conditioned cadence

Both cases transform environmental evidence into a refresh-policy change. Case 34 uses a bounded 1991 patent circuit; Case 133 uses later commercial LPDDR product interfaces. Function similarity does not establish component identity or genealogy.

### Case 35 — automatic TCSR with different controller authority

Case 35 is a useful counterpoint because its documented TCSR programming bits have no effect on the bounded 2008 Micron product while an on-die sensor automatically controls the oscillator. Case 133's LPDDR4 device instead gives the controller an explicit offset input to TCSR. The shared vendor name does not by itself establish a linear implementation lineage.

### Case 93 — profile staleness

Both cases show a maintenance policy depending on represented conditions that can become non-conservative. Case 93's representation is empirical row-retention/profile state affected by VRT/DPD; Case 133's is a coarse environmental status plus a controller model of sensor-to-hot-spot gradient. Mechanisms and historical lineages remain distinct.

## Philosophical interpretation — bounded

The technical evidence supports one narrow interpretation:

> Some preservation regimes require not only that a state survive, but that the system keep a sufficiently current and sufficiently representative relation between environmental conditions and the policy used to preserve that state.

This should not be rewritten as `the DRAM remembers its temperature`. MR4/TUF/offset are bounded engineering control relations, and TUF specifically demonstrates how little history may be retained while still supporting present maintenance decisions.

## Rejected claims / stop conditions

- **LPDDR4 invented MR4 temperature reporting** — rejected; Micron LPDDR2 2015 already supplies the bounded function.
- **Micron invented temperature-conditioned refresh** — rejected; Case 34 already grounds older prior art.
- **TUF is a temperature log** — rejected by read-to-clear change semantics.
- **offset is sensor calibration** — not documented.
- **MR4 reports the hottest point** — directly undermined by Micron's spatial-gradient warning.
- **>15°C means immediate deterministic data loss** — not stated; it is a reliability-contract boundary.
- **all LPDDR4 devices support thermal offset** — rejected by SK hynix's explicit optionality statement.
- **the 2°C margin is universal sensor accuracy / cell-retention margin** — rejected; it belongs to the response-time equation.
- **MR4 status persists across power loss** — not established.
- **product documentation equals normative JEDEC chronology** — rejected; standards archaeology remains open.
- **cross-vendor similarity proves genealogy** — rejected.

## Related-repository check

A fresh search of `tmzncty/computing-archaeology` for `LPDDR4 temperature sensor`, `MR4`, `TUF`, and `thermal offset` returned no dedicated case. The broader engineering/standards history should be developed there if pursued, while `technical-retention` keeps the bounded relation between environmental proxy, status freshness, controller compensation, and preservation authority.

## Research result

This slice closes one previously explicit roadmap seam at a product-evidence level:

> **later LPDDR sensor/thermal-offset semantics can now be grounded as a retention-control problem of sensor representativeness + status freshness + controller response + TCSR compensation, without claiming a completed JEDEC or cross-vendor genealogy.**

Still open:

- normative JEDEC revision-by-revision adoption/optionality;
- earlier thermal-offset invention/genealogy;
- exact silicon sensor placement and accuracy on the bounded Micron LPDDR4 parts;
- sensor/offset fault injection and named-platform controller traces;
- reset/power-loss persistence of relevant MR fields;
- cross-vendor compliance/implementation differences;
- LPDDR5/LPDDR5X evolution.
