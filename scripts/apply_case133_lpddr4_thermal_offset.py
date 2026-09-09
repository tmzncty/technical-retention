from pathlib import Path

CASE_PATH = Path("cases/133-micron-lpddr4-mr4-thermal-offset-refresh-authority.md")
EVIDENCE_PATH = Path("evidence/133-micron-2015-2020-lpddr-temperature-status-thermal-offset-grounding.md")
ROADMAP = Path("ROADMAP.md")
INDEX = Path("CASE_INDEX.md")

case_text = r'''# Micron LPDDR4 MR4 Thermal Offset: Sensor-Placement Error, Status Freshness, and Refresh Authority

## Status

**`grounded`** — bounded to Micron's Rev. E 8/2020 LPDDR4/LPDDR4X product documentation, with Micron's Rev. J 10/15 Automotive Mobile LPDDR2 documentation used as an earlier MR4/TUF/polling floor and SK hynix Rev. 1.1 8/2020 LPDDR4 documentation used only as a contemporaneous cross-vendor optionality witness.

Grounding record: [`../evidence/133-micron-2015-2020-lpddr-temperature-status-thermal-offset-grounding.md`](../evidence/133-micron-2015-2020-lpddr-temperature-status-thermal-offset-grounding.md).

## Scope

This case asks one narrow question left open by Cases 34 and 35:

> What changes when temperature-conditioned DRAM retention depends not only on an on-die sensor, but on a host-visible status whose freshness is bounded and on a controller-supplied offset that compensates for spatial separation between the sensor and an external hot spot?

The bounded Micron LPDDR4/LPDDR4X device exposes in MR4:

- `OP[2:0]` — a read-only refresh-rate / elevated-temperature status;
- `OP[7]` — `TUF`, a read-only temperature-update flag indicating whether `OP[2:0]` changed since the previous MR4 read;
- `OP[6:5]` — a writable `Thermal offset-controller offset to TCSR`;
- an internal temperature-sensor update interval `tTSI`;
- an explicit system-response relation combining sensor-update delay, MR4 polling interval, and controller response delay;
- an explicit spatial warning that a hot spot more than 15°C above the temperature at the sensor location falls outside the documented reliable-self-refresh relation.

This is **not**:

- a complete JEDEC LPDDR2/LPDDR4 standards genealogy;
- proof that Micron or LPDDR4 invented MR4 temperature reporting, TUF, TCSR, or thermal offset;
- a claim that every LPDDR4 vendor supports the thermal-offset field identically;
- a claim that MR4 reports the hottest physical point on the package;
- a claim that TUF stores temperature history;
- a claim that writing an offset calibrates the sensor itself;
- a claim that crossing the documented 15°C gradient means immediate deterministic bit loss;
- a claim about the persistence of MR4 configuration across reset or power loss.

## Relation to earlier DRAM cases

The existing DRAM cases already separate several retention-control relations:

```text
Case 03  physical charge decay and periodic restoration
Case 09  refresh-row enumeration
Case 21  AUTO REFRESH / SELF REFRESH authority handoff
Case 34  temperature-conditioned cadence selection
Case 35  commercial automatic on-die TCSR + PASR selective retention
Case 93  retained row-profile state whose future validity can become stale
Case 133 sensor-location representativeness + MR4 status freshness
         + controller thermal offset + response-time budget
```

Case 133 does not replace Case 35. Case 35 shows a 2005–2008 Mobile DDR product in which an on-die sensor automatically controls self-refresh cadence while documented TCSR programming bits have no effect on that product. Case 133 adds a later LPDDR4 relation in which the controller can both **observe** a temperature-derived refresh-rate class and **supply** a thermal offset that changes the device's TCSR behavior.

## Historical record

### 2015 Micron Automotive Mobile LPDDR2: MR4 status already had a freshness contract

Micron's Rev. J 10/15 `512Mb Automotive Mobile LPDDR2 SDRAM` document predates the bounded LPDDR4 product and already exposes:

- MR4 `OP[2:0]` as a read-only SDRAM refresh-rate status;
- `OP7` as the read-only `Temperature update flag (TUF)`;
- TUF = 1 when `OP[2:0]` changed at any time since the last MR4 read;
- an MR4 read clearing TUF back to 0;
- TUF reset to 0 at power-up;
- a maximum temperature-sensor update delay `tTSI = 32 ms`;
- a system polling constraint
  `TempGradient × (ReadInterval + tTSI + SysRespDelay) ≤ 2°C`;
- a worked example in which a 10°C/s gradient and 1 ms response delay require an MR4 read interval no greater than 167 ms.

The same product note warns that its embedded temperature sensor is not an exact reflection of DRAM `TCASE`, reporting sample variance up to ±7°C for the bounded automotive part.

This earlier record blocks any claim that LPDDR4 introduced the broad function `host reads MR4 temperature-derived refresh status and must poll it within a response budget`.

### 2020 Micron LPDDR4/LPDDR4X: thermal-offset configuration joins the MR4 relation

Micron's Rev. E 8/2020 `LPDDR4/LPDDR4X SDRAM` document for `MT53E1G16D1`, `MT53E1G32D2`, `MT53E2G32D4`, and `MT53E1G64D4` lists an on-chip temperature sensor controlling self-refresh rate.

MR4 now includes three adjacent but analytically distinct relations:

1. `OP[2:0]` — read-only refresh-rate class, including 4x, 2x, 1x, 0.5x, and 0.25x relations plus high/low-temperature-limit codes;
2. `OP[7]` — TUF, set when that reported refresh-rate class changes since the previous MR4 read and cleared by reading MR4;
3. `OP[6:5]` — writable controller thermal offset to TCSR: no offset for a documented 0–5°C gradient, 5°C for 5–10°C, and 10°C for 10–15°C.

The thermal-offset section explains why the offset exists. Tight thermal coupling to an SoC can create hot spots that are not located near the memory's thermal sensor. In that situation the device's temperature-compensated self-refresh circuit may otherwise generate too few refresh cycles to guarantee memory retention. The controller may therefore supply an offset that changes TCSR behavior.

The same section states:

- the offset can take up to 200 µs to be reflected in MR4 `OP[2:0]`;
- if the induced gradient from the memory-sensor location to the controller hot-spot location exceeds 15°C, self-refresh mode will not reliably maintain memory contents;
- the memory thermal-sensor location must be provided to the controller so the gradient can be determined accurately.

### 2020 SK hynix LPDDR4: cross-vendor witness, not a standards chronology

SK hynix's Rev. 1.1 August-2020 `H54G46BYYV(Q/P)X053` LPDDR4 documentation independently presents the same bounded thermal-offset problem: external hot spots may not be near the device sensor, an MR4 thermal offset can compensate TCSR behavior, and a gradient greater than 15°C is outside the reliable-self-refresh relation. Crucially, the document says **support of the thermal-offset function is optional** and instructs readers to consult the vendor datasheet.

This supports a narrow negative conclusion:

> **LPDDR4-family vocabulary/function visibility != proof that every vendor/device implements the option identically.**

It is not a substitute for reading the normative JEDEC revision history.

## Retained state and control state

The payload is still charge-dependent dynamic-array state. Case 133 adds several non-payload relations that participate in preserving it:

1. **temperature-derived refresh-rate status** — MR4 `OP[2:0]`;
2. **change-since-observation status** — TUF in `OP[7]`;
3. **thermal-offset configuration** — controller-written `OP[6:5]`;
4. **internal sensor-update cadence** — bounded by `tTSI`;
5. **host observation cadence** — `ReadInterval`;
6. **system response latency** — `SysRespDelay`;
7. **sensor-location / hot-spot relation** — needed to choose a safe offset under the documented model;
8. **refresh execution** — internal TCSR during self refresh and controller-visible refresh/timing policy outside it.

`Status freshness`, `observation cadence`, and `sensor representativeness` are project engineering terms, not Micron's historical vocabulary.

## Engineering reconstruction

### Sensor observation is not the hottest-point temperature

The strongest boundary is supplied by the vendor itself: SoC hot spots can be spatially separated from the device thermal sensor, and the maximum device temperature can be higher than MR4 indicates.

Therefore:

> **on-die temperature sensing != complete spatial knowledge of the thermal field**.

The problem is not merely sensor numerical precision. It is also **where the sensor is relative to the heat source that matters for retention**.

### Thermal offset is compensation, not sensor calibration

Micron says the controller-provided offset adjusts the **TCSR circuit** and may modify refresh behavior. The source does not say that the offset changes the physical sensor calibration, makes MR4 equal the actual hottest-point temperature, or repairs a faulty sensor.

Therefore:

> **controller thermal offset != sensor calibration**.

The offset is a retention-policy correction for a modeled spatial mismatch.

### A configuration write does not instantly become effective policy

Micron allows up to 200 µs before the offset change is reflected in the reported refresh-rate status.

Therefore:

> **configuration accepted != new maintenance relation already observable/effective everywhere at the same instant**.

The source gives one bounded propagation/settling relation. It does not expose the internal circuit transition in enough detail to claim a transactional update or a specific cell-by-cell switchover point.

### TUF is change evidence, not temperature history

TUF answers one compressed question: has `OP[2:0]` changed since the last MR4 read? Reading MR4 clears the flag.

Therefore:

> **change-since-last-observation flag != event log**

and

> **TUF = 0 != temperature never changed**.

A 0 can mean that the current refresh-rate class has not changed since the last read; it does not preserve intermediate sensor samples, timestamps, physical temperatures, or the sequence by which the current class was reached.

### Status freshness has its own deadline chain

Micron explicitly composes three delays:

```text
internal sensor-to-MR4 update delay
+ host MR4 polling interval
+ system response delay
```

and constrains their sum through the thermal gradient and a 2°C temperature-response margin.

Therefore:

> **physical refresh deadline != status-freshness deadline != controller-response deadline**.

A maintenance policy can fail because the payload was not refreshed often enough, but also because the system learned or acted on the environmental condition too slowly.

The documented 2°C quantity is a **temperature-response margin** in this control relation. It is not evidence of a universal DRAM retention-temperature margin, sensor accuracy, ECC margin, or cell-failure threshold.

### Reported refresh-rate class is not the same as executed refresh work

MR4 `OP[2:0]` is a reported class that informs refresh interval and possibly AC-timing derating. Actual preservation still requires the relevant refresh mechanism to execute under the applicable operating mode.

Therefore:

> **refresh-rate status != refresh execution**.

This keeps Case 133 compatible with the earlier authority decomposition: sensing and reporting can be inside the device, policy adjustment can be split across controller and device, and recurring restoration work still remains a separate operation.

### Self refresh is conditional, not unconditional retention

The product explicitly withholds reliable self-refresh maintenance when the sensor-to-hot-spot gradient exceeds 15°C.

Therefore:

> **self-refresh mode active != unconditional memory-retention guarantee**.

This is a contract boundary, not a deterministic physical erasure timestamp. The source does not say every bit fails immediately at 15.001°C of gradient.

### Control-state lifetime is not established across reset/power loss

MR4 contains writable thermal-offset configuration and read-only status, but the inspected sources are used here only for their operating-regime semantics. This case does not claim that offset configuration, TUF state, or prior sensor status survives reset or loss of power.

Therefore:

> **operationally retained control state != demonstrated durable checkpoint**.

## Failure and forgetting boundaries

The bounded sources support several distinct failure classes:

- **under-refresh from spatial misrepresentation** — sensor location understates a controller-induced hot spot;
- **stale observation** — MR4 status changes but host polling/response is too slow for the documented thermal ramp;
- **insufficient offset** — the chosen policy does not cover the actual sensor-to-hot-spot gradient;
- **out-of-envelope gradient** — >15°C lies outside the documented reliable-self-refresh relation;
- **history loss by compression** — TUF only says whether the class changed since the last read and then clears;
- **unsupported-option assumption** — cross-vendor LPDDR4 evidence warns that thermal-offset support is optional;
- **payload failure** — logically downstream, but not equivalent to any one status/control fault above.

These should not be collapsed into one generic statement that `the temperature sensor failed`.

## Prior art and anti-anachronism

Micron's 2015 LPDDR2 documentation already grounds MR4 refresh-rate status, TUF read-to-clear semantics, `tTSI`, and the polling/response equation. Case 34 separately grounds 1987-priority and 1991-filed temperature-conditioned DRAM-refresh circuitry.

Case 133 therefore makes no invention-priority claim for temperature sensing, TCSR, MR4 polling, or refresh adaptation.

The bounded novelty of this case inside the repository is narrower:

> a later commercial LPDDR4 contract explicitly makes **sensor placement error**, **controller-supplied thermal offset**, **status freshness**, and **response latency** part of the retention-control relation.

## Functional analogy — bounded

### Case 34

Case 34 and Case 133 both connect environmental evidence to refresh cadence. Case 34's bounded 1991 Micron patent uses temperature-band circuitry to select cadence; Case 133 adds a product-level host/device status-and-offset interface plus a spatial hot-spot mismatch. Similar function does not establish circuit identity or genealogy.

### Case 35

Case 35's 2008 Mobile DDR product automatically controls the self-refresh oscillator with an on-die sensor while documented TCSR programming bits are inert. Case 133 instead exposes a controller-writable thermal offset that can alter TCSR behavior. This is a useful authority contrast, not proof of one linear product evolution.

### Case 93

Case 93's row-retention profile and Case 133's MR4 environmental status can both become unsafe policy inputs if the represented relation is no longer conservative/current. But a per-row empirical retention profile is not a coarse temperature-derived status code, and VRT/DPD staleness is not sensor-location thermal error.

## Philosophical interpretation — bounded

A narrow conceptual result follows from the engineering record:

> Persistence can depend not only on retaining payload, but on keeping a sufficiently current and sufficiently representative relation between the payload's environment and the maintenance policy acting on it.

The `knowledge` here is purely operational: sensor status, offset configuration, polling, and response. The claim does not anthropomorphize the device, turn MR4 into memory of temperature history, or imply that every preservation system requires explicit environmental measurement.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Micron LPDDR2 Rev. J 10/15 exposes MR4 refresh-rate status and TUF | H/P | direct manufacturer product document |
| LPDDR2 TUF clears on MR4 read and is 0 at power-up | H/P | direct MR4 definition |
| LPDDR2 already uses `tTSI`, polling interval, response delay, and a 2°C control margin | H/P | direct Temperature Sensor section |
| Micron LPDDR4 Rev. E 8/2020 exposes MR4 thermal offset to TCSR | H/P | direct MR4 definition |
| LPDDR4 hot spots can be displaced from the memory sensor and thereby understate refresh need | H/P | direct Thermal Offset section |
| A controller-provided offset may change TCSR/refresh behavior | H/P | direct Thermal Offset section |
| The offset can take up to 200 µs to appear in MR4 refresh-rate status | H/P | direct Thermal Offset section |
| >15°C sensor-to-hot-spot gradient lies outside reliable self-refresh maintenance in the documented relation | H/P | direct manufacturer warning |
| TUF is a full temperature event log | X | contradicted by read-to-clear change-flag semantics |
| Thermal offset recalibrates the physical sensor | X | not the documented mechanism |
| MR4 status by itself performs refresh | X | status/reporting and restoration execution are separate relations |
| 2°C is a universal retention or sensor-accuracy margin | X | it is a bounded controller-response margin in the inspected timing relation |
| All LPDDR4 devices support the offset identically | X | SK hynix product documentation calls support optional; no normative chronology is claimed |
| This case establishes JEDEC revision genealogy | X | product documents are insufficient for that claim |

## Related repositories

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `LPDDR4 temperature sensor`, `MR4`, `TUF`, and `thermal offset` returned no dedicated case to reuse. A full LPDDR2→LPDDR4→LPDDR5 / JEDEC revision genealogy, controller implementation history, sensor-placement engineering history, and silicon-level validation should primarily live there if developed comprehensively.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) supplies the anti-anachronism discipline: `status freshness`, `sensor representativeness`, and `maintenance authority` are project reconstruction terms, not retroactive vendor vocabulary.

## Sources

1. Micron Technology, Inc., **512Mb Automotive Mobile LPDDR2 SDRAM**, `u67m_512mb_aat-ait_mobile_lpddr2.pdf`, Rev. J 10/15 EN, ©2012 Micron. Relevant locations: MR4 Device Temperature / Table 23 around printed p. 35; Temperature Sensor / Table 47 around printed pp. 73–75. Public manufacturer-document mirror: <https://media.digikey.com/pdf/Data%20Sheets/Micron%20Technology%20Inc%20PDFs/MT42L32M16D1,%2032D2,%20MT42L16M32D1_Web.pdf>.
2. Micron Technology, Inc., **LPDDR4/LPDDR4X SDRAM — MT53E1G16D1, MT53E1G32D2, MT53E2G32D4, MT53E1G64D4**, `z32m_embedded_lpddr4_lpddr4x.pdf`, Rev. E 8/2020 EN, ©2019 Micron. Relevant locations: feature list printed p. 1; MR4 Tables 32–33 printed pp. 57–58; Thermal Offset / Temperature Sensor printed pp. 204–205. Public manufacturer-document mirror: <https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/908/MT53E1G16D1FW_2D00_046-AIT--A-MCR-Datenblatt_2800_P010694655_2900_.pdf>.
3. SK hynix, **H54G46BYYV(Q/P)X053 LPDDR4 16Gb (x16, 2 Channel, 1CS)**, Rev. 1.1, August 2020. Relevant locations: MR4 register around printed p. 26; `5.37 Thermal offset` and `5.38 Temperature Sensor` around printed pp. 182–184. Public manufacturer-document mirror: <https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/791/6888.Automotive_5F00_DA-16Gb-LPDDR4_5F00_H54G46BYYV_2800_Q_2C00_P_2900_X053_5F00_Rev1.1.pdf>.
'''

evidence_text = r'''# Case 133 grounding — LPDDR temperature status, polling freshness, and controller thermal offset (2015–2020)

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
'''

CASE_PATH.write_text(case_text, encoding="utf-8")
EVIDENCE_PATH.write_text(evidence_text, encoding="utf-8")

roadmap = ROADMAP.read_text(encoding="utf-8")
if "Case 133 Micron LPDDR4 MR4 thermal-offset / status-freshness grounding" in roadmap:
    raise SystemExit("ROADMAP already contains Case 133 marker")
roadmap_marker = "- [ ] DRAM evolution and refresh machinery beyond the bounded case —"
if roadmap.count(roadmap_marker) != 1:
    raise SystemExit(f"ROADMAP broad DRAM marker count={roadmap.count(roadmap_marker)}")
roadmap_bullet = "- [x] Case 133 Micron LPDDR4 MR4 thermal-offset / status-freshness grounding — [`cases/133-micron-lpddr4-mr4-thermal-offset-refresh-authority.md`](cases/133-micron-lpddr4-mr4-thermal-offset-refresh-authority.md), grounded by [`evidence/133-micron-2015-2020-lpddr-temperature-status-thermal-offset-grounding.md`](evidence/133-micron-2015-2020-lpddr-temperature-status-thermal-offset-grounding.md): Micron's 2015 Automotive Mobile LPDDR2 product documentation already grounds MR4 refresh-rate status, read-to-clear `TUF`, a 32 ms maximum sensor-update interval, and a polling/response equation; Micron's Rev. E 8/2020 LPDDR4/LPDDR4X product then adds a controller-written MR4 thermal offset to TCSR because SoC hot spots can be spatially displaced from the memory sensor, with up to 200 µs before the offset is reflected in reported refresh status and an explicit >15°C sensor-to-hot-spot gradient boundary beyond which self refresh will not reliably maintain contents. A contemporaneous SK hynix product document independently calls thermal-offset support optional. This closes the bounded `sensor status != hottest-point truth`, `TUF != temperature history`, and `refresh-rate report != refresh execution` seam without claiming normative JEDEC chronology, universal vendor support, sensor calibration, reset persistence, or fault validation."
roadmap = roadmap.replace(roadmap_marker, roadmap_bullet + "\n\n" + roadmap_marker, 1)
if "partially advanced by fourteen grounded bounded sub-slices" in roadmap:
    roadmap = roadmap.replace("partially advanced by fourteen grounded bounded sub-slices", "partially advanced by fifteen grounded bounded sub-slices", 1)
insert_sentence = "[`cases/133-micron-lpddr4-mr4-thermal-offset-refresh-authority.md`](cases/133-micron-lpddr4-mr4-thermal-offset-refresh-authority.md), grounded by [`evidence/133-micron-2015-2020-lpddr-temperature-status-thermal-offset-grounding.md`](evidence/133-micron-2015-2020-lpddr-temperature-status-thermal-offset-grounding.md), adds a later LPDDR4 environmental-control sub-slice in which MR4 status freshness, controller response time, sensor/hot-spot spatial mismatch, and writable TCSR thermal offset are separate retention relations. "
if roadmap.count("The broad item stays unchecked because") != 1:
    raise SystemExit("ROADMAP broad-item continuation marker not unique")
roadmap = roadmap.replace("The broad item stays unchecked because", insert_sentence + "The broad item stays unchecked because", 1)
roadmap = roadmap.replace("later LPDDR sensor/thermal-offset and fault-qualification semantics", "broader cross-vendor LPDDR sensor/thermal-offset fault-qualification and standards genealogy", 1)
ROADMAP.write_text(roadmap, encoding="utf-8")

idx = INDEX.read_text(encoding="utf-8")
if "133-micron-lpddr4-mr4-thermal-offset-refresh-authority.md" in idx:
    raise SystemExit("CASE_INDEX already contains Case 133")
lines = idx.splitlines()
row = "| [Micron LPDDR4 MR4 Thermal Offset: Sensor-Placement Error, Status Freshness, and Refresh Authority](cases/133-micron-lpddr4-mr4-thermal-offset-refresh-authority.md) | **grounded** | dynamic-array payload + on-die temperature-derived refresh status + read-to-clear TUF + controller thermal offset to TCSR + bounded sensor/poll/response freshness | separate sensor observation from hottest-point condition; status/currentness from full history; report from refresh execution; controller compensation from sensor calibration; and self-refresh mode from unconditional retention guarantee | [2015–2020 LPDDR temperature-status / thermal-offset grounding](evidence/133-micron-2015-2020-lpddr-temperature-status-thermal-offset-grounding.md); normative JEDEC chronology, earlier offset genealogy, reset persistence, sensor placement/accuracy, named-controller traces, and fault injection remain open |"
row_pos = None
for i, line in enumerate(lines):
    if line.startswith("| [Cryogenic Serial Flash: Retention Without Full Cryogenic Operability]"):
        row_pos = i + 1
        break
if row_pos is None:
    raise SystemExit("Case 132 table row not found")
lines.insert(row_pos, row)
idx = "\n".join(lines) + "\n"

findings_marker = "## Case 02 deepening — TCM-32 clear/write and whole-stack memory-clear findings"
if idx.count(findings_marker) != 1:
    raise SystemExit(f"CASE_INDEX findings marker count={idx.count(findings_marker)}")
findings = r'''## Case 133 — LPDDR temperature-status freshness / thermal-offset findings

Evidence: [`evidence/133-micron-2015-2020-lpddr-temperature-status-thermal-offset-grounding.md`](evidence/133-micron-2015-2020-lpddr-temperature-status-thermal-offset-grounding.md).

- **2710 — LPDDR4 MR4 temperature-status polling != origin of the broad function.** Micron's Rev. J 10/15 Automotive Mobile LPDDR2 product already exposes MR4 refresh-rate status, read-to-clear TUF, `tTSI`, and a host polling/response equation; the later LPDDR4 evidence must not be written as invention priority. (`H/P`, `X`)
- **2711 — temperature-derived refresh status != exact physical temperature.** The older Micron automotive LPDDR2 document itself warns that its embedded sensor is not an exact reflection of `TCASE`; the later LPDDR4 record separately warns that external hot spots can make the maximum device temperature higher than MR4 indicates. (`H/P`, `E`)
- **2712 — sensor value != complete spatial thermal field.** Micron LPDDR4 explicitly describes SoC hot spots that may not be near the memory thermal sensor, making sensor placement part of the bounded retention-control relation. (`H/P`, `E`)
- **2713 — controller thermal offset != sensor calibration.** MR4 `OP[6:5]` adjusts TCSR/refresh behavior for a modeled sensor-to-hot-spot gradient; the source does not say it recalibrates the physical sensor or makes MR4 equal the hottest-point temperature. (`H/P`, `E`, `X`)
- **2714 — thermal-offset write != instantly reflected refresh status.** Micron allows up to 200 µs before an offset change is reflected in MR4 `OP[2:0]`, so configuration, policy transition, and observed status are not one zero-time event. (`H/P`, `E`)
- **2715 — TUF != temperature event history.** MR4 `OP[7]` records only whether the refresh-rate class changed since the previous MR4 read and is cleared by that read; it retains neither transition count nor timestamps nor sensor samples. (`H/P`, `E`)
- **2716 — TUF = 0 != temperature never changed.** A cleared/no-change flag only qualifies the interval since the relevant observation boundary; it cannot reconstruct older changes or changes that leave the coarse reported class unchanged. (`E`, `X`)
- **2717 — sensor-update latency != host-poll latency != system-response latency.** Micron's equation explicitly composes `tTSI`, `ReadInterval`, and `SysRespDelay`; those are distinct timing obligations even though one 2°C response margin constrains their sum under a thermal gradient. (`H/P`, `E`)
- **2718 — 2°C response margin != universal DRAM retention margin or sensor accuracy.** The quantity belongs to the bounded temperature-response relation between MR4 update and controller reconfiguration; it must not be repurposed as a cell-failure threshold, ECC margin, or general accuracy claim. (`H/P`, `E`, `X`)
- **2719 — refresh-rate report != refresh execution.** MR4 can report a required interval/timing class while preservation still depends on the relevant controller or internal TCSR path actually performing restoration under the active mode. (`H/P`, `E`)
- **2720 — self-refresh mode active != unconditional retention guarantee.** Micron explicitly says a sensor-to-hot-spot gradient greater than 15°C falls outside reliable self-refresh maintenance; mode presence alone is weaker than satisfaction of its environmental contract. (`H/P`, `E`)
- **2721 — >15°C gradient boundary != deterministic immediate bit-loss timestamp.** The vendor states that self refresh will not reliably maintain contents; it does not say every cell fails instantly once the gradient exceeds the boundary. (`H/P`, `X`)
- **2722 — product-level thermal-offset support != universal LPDDR4 implementation.** SK hynix's contemporaneous Rev. 1.1 LPDDR4 document independently presents the function but explicitly calls thermal-offset support optional and vendor-specific. (`H/P`, `X`)
- **2723 — Case 133 environmental status ~= Case 93 retained profile only as a bounded currentness analogy.** Both can become non-conservative maintenance inputs, but coarse temperature/status + sensor placement is not per-row retention profiling, VRT, or DPD, and no genealogy is asserted. (`A`, `X`)
- **2724 — related-repository boundary:** a fresh `tmzncty/computing-archaeology` search for `LPDDR4 temperature sensor`, `MR4`, `TUF`, and `thermal offset` found no dedicated case to reuse; broad JEDEC/LPDDR standards chronology, sensor-placement engineering, controller implementations, and fault validation belong there if developed, while Case 133 keeps the retention-specific status-freshness/compensation boundary. (`H/P` project-state record)

'''
idx = idx.replace(findings_marker, findings + findings_marker, 1)
INDEX.write_text(idx, encoding="utf-8")

# Local bounded assertions. The workflow runs git diff --check separately.
assert CASE_PATH.read_text(encoding="utf-8").count("## Historical record") == 1
assert CASE_PATH.read_text(encoding="utf-8").count("## Engineering reconstruction") == 1
assert CASE_PATH.read_text(encoding="utf-8").count("## Functional analogy — bounded") == 1
assert CASE_PATH.read_text(encoding="utf-8").count("## Philosophical interpretation — bounded") == 1
assert EVIDENCE_PATH.read_text(encoding="utf-8").count("## Historical record") == 1
assert ROADMAP.read_text(encoding="utf-8").count("Case 133 Micron LPDDR4 MR4 thermal-offset / status-freshness grounding") == 1
idx_check = INDEX.read_text(encoding="utf-8")
assert idx_check.count("## Case 133 — LPDDR temperature-status freshness / thermal-offset findings") == 1
for n in range(2710, 2725):
    marker = f"**{n} —"
    assert idx_check.count(marker) == 1, (n, idx_check.count(marker))
print("Case 133 research slice applied successfully")
