# Micron LPDDR4 MR4 Thermal Offset: Sensor-Placement Error, Status Freshness, and Refresh Authority

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
