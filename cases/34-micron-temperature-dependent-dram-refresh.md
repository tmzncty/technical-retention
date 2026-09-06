# Micron Temperature-Dependent DRAM Refresh: Guardband, Environmental Sensing, and Adaptive Maintenance

## Status

**`grounded`** — bounded to Micron Technology's 1991-filed US5278796A temperature-dependent DRAM refresh circuit, with an earlier 1987-priority CardioData patent family used to control invention-priority claims. A later Micron 2Gb DDR3 product datasheet (Rev. S 02/16) now supplies a product-interface witness for distinct manual `SRT` and automatic `ASR` self-refresh policies; the 2004–2006 temperature-dependent self-refresh patent remains a separate later locus/authority comparison. The later sources deepen policy/authority boundaries but are not treated as proof of direct implementation genealogy from the 1991 patent.

Grounding record: [`../evidence/34-micron-1991-temperature-dependent-refresh-grounding.md`](../evidence/34-micron-1991-temperature-dependent-refresh-grounding.md).

## Scope

This case asks one narrow question left open by Cases 03, 09, 10, 21, and 33:

> What changes when a DRAM system treats refresh cadence as conditional on measured operating temperature instead of always using one worst-case refresh cadence?

The bounded Micron design places a solid-state temperature sensor near the DRAM array, converts its output into discrete temperature bands, uses those bands to control an oscillator, and then uses that oscillator output to drive system logic that produces the DRAM refresh sequence.

This is **not**:

- proof that a named Micron commercial DRAM or computer shipped with this exact circuit;
- a complete JEDEC history of temperature-compensated self refresh;
- a claim that Micron invented temperature-adaptive DRAM refresh;
- a universal law that every DRAM technology has exactly the same temperature/retention relation;
- per-row retention profiling or retention-aware row scheduling;
- RowHammer mitigation;
- a claim that sensing temperature measures the stored charge or retention time of each cell directly.

The case therefore grounds an **environment-conditioned refresh-policy relation**, not a general history of DRAM temperature behavior.

## Relation to the earlier DRAM cases

The existing DRAM cases separate several responsibilities that are easy to collapse into the single phrase `refresh`:

```text
Case 03
    why dynamic-cell state needs periodic restoration

Case 09
    where refresh-row enumeration comes from

Case 10
    how an on-chip leakage-related proxy can trigger self-refresh work

Case 21
    who generates recurring maintenance in normal AUTO REFRESH
    versus SELF REFRESH, and how that authority returns on exit

Case 33
    which bank subset is blocked by a refresh operation
    and which non-target resources can remain serviceable

Case 34
    how measured environment can change the chosen refresh cadence
    without removing the underlying dynamic-cell retention obligation
```

Case 34 therefore adds **environment-conditioned cadence selection**. It does not replace the row-address, authority, mode, or target-geometry distinctions already grounded elsewhere.

## Historical vocabulary and record

The central primary source is US5278796A, filed by Micron Technology on **12 April 1991** and published/granted on **11 January 1994**. The patent's historical vocabulary includes:

- `Temperature-dependent DRAM refresh circuit`;
- `temperature compensated DRAM refresh`;
- `temperature sensor`;
- `comparators`;
- `encoder`;
- `oscillator`;
- `refresh counter and gate circuit`;
- `guardbanding`.

The patent states that DRAM refresh is basic to the dynamic-cell storage technique because charge stored on a capacitor leaks. It further states that leakage is strongly temperature dependent, so conventional refresh timing is specified for the highest allowed operating temperature. Within the patent's stated period/technology assumptions, lower temperature therefore permits a less frequent refresh cadence and lower refresh power.

Micron's preferred embodiment places a solid-state temperature sensor in proximity to the DRAM array. Four comparators divide the sensed signal into five temperature bands. A priority encoder and weighted resistors turn the band result into a control voltage for an RC oscillator. System logic uses that oscillator output to produce a DRAM refresh sequence.

The patent gives an illustrative five-band schedule: above 56 °C, 8 ms; 42–56 °C, 16 ms; 28–42 °C, 32 ms; 14–28 °C, 64 ms; below 14 °C, 128 ms. Those numbers are **not** treated here as a timeless DRAM rule: the patent itself explicitly says the temperature ranges, number of bands, and refresh rates may change with technology.

The patent also states that adding more comparators can improve refresh-rate granularity, but at some point the control circuit's own power consumption exceeds the refresh-power savings. This makes the sensing/control apparatus part of the retention cost rather than a free optimization layer.

### Later product-interface witness — Micron 2Gb DDR3 `SRT` / `ASR` (Rev. S 02/16)

Micron's later **2Gb x4/x8/x16 DDR3 SDRAM** datasheet, document `09005aef826aaadc`, Rev. S 02/16, exposes a useful product-level policy split in Mode Register 2. This source is more than a generic statement that hotter DRAM needs more refresh: it separately documents **manual temperature-range declaration**, **automatic self-refresh rate selection**, and the still-external refresh requirement outside self refresh.

The bounded interface says:

- `MR2[7]` selects **Self Refresh Temperature (`SRT`)** when ASR is disabled. Enabling SRT forces the internal self-refresh rate from 1x to 2x **regardless of actual case temperature** so the extended 0–95 °C operating range can be supported during self refresh.
- `MR2[6]` selects **Auto Self Refresh (`ASR`)**. With ASR enabled, the DRAM automatically changes its internal self-refresh rate between 1x and 2x over the supported temperature range.
- the datasheet explicitly says the automatic transition need not occur at exactly 85 °C; it may occur at a lower temperature while still maintaining data integrity.
- if case temperature exceeds 85 °C during **externally managed refresh**, the user/controller must provide 2x refresh by reducing the refresh period from 64 ms to 32 ms. SRT/ASR govern the self-refresh side of the contract rather than eliminating that external obligation.
- SRT and ASR are mutually exclusive in this interface.

This later product witness adds two control forms that the 1991 patent did not expose as a mode-register pair: a **declared conservative operating envelope** (`SRT`) and an **automatic temperature-conditioned self-refresh policy** (`ASR`). It does not establish that the product implements US5278796A, that Micron invented these interface semantics, or that this one datasheet is a complete JEDEC DDR3 chronology.

## Prior art before the Micron filing

US5278796A itself identifies U.S. Patent 4,920,489 as earlier work. That patent family has **1987 priority** and describes a system in which a thermistor and resistor form a voltage divider, a processor digitizes the value with an A/D converter, and a table is used to select DRAM refresh rate as a function of ambient temperature.

The earlier patent's detailed embodiment says a worst-case refresh recommendation can be relaxed at lower temperature, gives example refresh periods of roughly 150 ms at 25 °C and 80 ms at 45 °C for its bounded application, and explicitly presents temperature-dependent refresh as a way to reduce power without sacrificing the required data-retention behavior.

Therefore this case makes **no `first temperature-compensated DRAM refresh` claim for Micron**. Micron's bounded contribution here is useful because its patent makes the sensor → comparator bands → encoder → oscillator → refresh-sequence mechanism especially explicit and directly discusses guardband/granularity tradeoffs.

## Retained state and control state

The user payload remains dynamic-cell state whose electrical distinction decays if required restoration work does not recur in time.

Case 34 adds several non-payload relations that participate in preserving that state:

1. **physical environment** — the temperature experienced by the DRAM array;
2. **measured proxy** — the sensor voltage intended to reflect array temperature;
3. **policy classification** — comparator outputs / encoded temperature band;
4. **cadence control** — oscillator frequency and refresh-counter timing;
5. **maintenance execution** — the actual refresh sequence that restores dynamic state.

`Measured proxy`, `environment-conditioned maintenance`, and `policy classification` are project reconstruction terms, not Micron's historical vocabulary.

## Engineering reconstruction

### Retention deadline is not one fixed refresh interval

The most important bounded result is:

> **retention constraint ≠ one universal fixed refresh interval**.

Micron's design exists precisely because the refresh requirement can be conservatively scheduled at a worst-case high-temperature rate while the usable maintenance interval is longer under cooler conditions in the bounded technology assumptions.

A fixed interface or datasheet cadence can therefore be a **policy chosen to cover an environmental envelope**, not a direct statement that the underlying physical loss process has one temperature-independent deadline.

### Retention obligation is not worst-case maintenance frequency

Temperature adaptation does not make DRAM nonvolatile. The patent repeatedly treats refresh as constitutive of the dynamic-cell storage technique.

Therefore:

> **retention obligation ≠ worst-case maintenance frequency**.

The obligation remains; the amount of maintenance work selected to satisfy it can change with the sensed environment.

This is important for cross-case comparison because reduced maintenance must not be misread as reduced dependence on maintenance.

### Environmental measurement is not payload measurement

The solid-state temperature sensor is placed near the DRAMs so that its voltage reflects their temperature. It does not read stored user bits, directly assay every cell's remaining charge, or measure each row's actual retention time.

Therefore:

> **temperature observation ≠ direct payload-retention measurement**.

The system uses one measured environmental relation as a proxy for a maintenance requirement.

That proxy relation can be useful without being identical to the physical state being protected.

### Guardband reduction is not elimination of safety margin

Micron describes 14 °C comparator steps as providing guardbanding against its stated approximately 12 °C refresh-rate relation. Temperature adaptation therefore does not remove conservative engineering margins in general. It replaces a single worst-case global cadence with another bounded policy that depends on sensor placement, thresholds, band selection, and technology assumptions.

Thus:

> **adaptive refresh ≠ zero guardband**.

The patent abstract's language about removing refresh guardbanding is interpreted narrowly as removing the need to operate the entire temperature range at one worst-case cadence, not as proof that all measurement or design margin disappears.

### Measurement granularity is not physical-retention granularity

The preferred embodiment maps a continuous environmental variable into five bands. The patent explicitly says more comparators improve accuracy, while one comparator yields only two coarse rates.

Therefore:

> **temperature-band granularity ≠ cell-retention granularity**.

The five-band representation is a control-policy discretization. It is not evidence that DRAM cells themselves possess five natural retention states.

### More accurate control is not free

The patent gives a direct engineering tradeoff: more comparators can improve refresh-rate accuracy, but eventually the control circuit consumes more power than the reduced refresh activity saves.

Therefore:

> **maintenance optimization ≠ zero-cost retention infrastructure**.

A mechanism that reduces constitutive maintenance can itself require sensing, comparison, encoding, oscillation, and power.

This makes retention cost relational across payload maintenance and the apparatus that decides when that maintenance is needed.

### Temperature-conditioned refresh is not self-refresh authority

Micron's 1991 design sends the temperature-derived oscillator output to **system logic**, which then produces the DRAM refresh sequence. It therefore does not by itself establish the later package-internal `SELF REFRESH` responsibility relation grounded in Case 21 or the leakage-monitor self-refresh circuitry disclosed in Case 10.

A later 2004-filed temperature-dependent self-refresh patent explicitly integrates a temperature sensor, encoder, programmable oscillator, and sampled/latched temperature state into a self-refresh circuit. That later source is useful as a boundary precisely because it shows that two questions are separable:

> **what condition changes refresh cadence ≠ where recurring refresh authority resides**.

Temperature adaptation can be external/system-level, on-chip, or combined with self-refresh. The shared function does not prove historical mechanism identity.

### Extended-temperature support is not automatic temperature adaptation

The DDR3 product interface gives a direct counterexample to treating `supports hotter operation` and `measures/adapts to temperature` as synonyms. `SRT` can support the extended range by forcing 2x self refresh even when the device is cooler; `ASR` instead changes internal self-refresh rate automatically over the supported range.

Therefore:

> **extended-temperature support ≠ automatic temperature adaptation**.

A conservative fixed maintenance policy and an adaptive maintenance policy can protect the same bounded retention envelope while requiring different evidence and control relations.

### SRT declaration is not a temperature measurement

When ASR is disabled, the user programs `SRT` to indicate the operating-temperature range to be protected during self refresh. That bit is policy/configuration state. It does not, by itself, report a measured temperature.

Therefore:

> **declared operating envelope ≠ measured environmental condition**.

This sharpens the 1991 sensor/comparator case: environment, measurement, classification, and chosen cadence can be represented by different mechanisms, and a product may expose only some of them to software.

### External refresh responsibility is not internal self-refresh policy

Above 85 °C, the same DDR3 datasheet requires externally managed refresh to move from the 64 ms to 32 ms period, while self refresh must use either SRT or ASR.

Therefore:

> **external refresh-rate responsibility ≠ internal self-refresh cadence selection**.

The physical temperature constraint can be shared while the locus and representation of maintenance authority change with mode. This is a product-level continuation of the Case-21 responsibility distinction, not evidence that the controller and DRAM use one scheduler.

### Contract boundary is not an exact physical switching point

The datasheet says ASR may switch from 1x to 2x below exactly 85 °C while preserving data integrity. The contractual 85 °C boundary therefore must not be reconstructed as a measured cell-level retention cliff or an exact sensor trip point.

Therefore:

> **specified temperature boundary ≠ exact automatic transition point ≠ per-cell retention limit**.

This is also a concrete guard against reading a mode table as a direct map of semiconductor physics.

### Temperature-conditioned refresh is not per-row retention-aware refresh

The bounded Micron design selects a refresh cadence for the DRAM array from a small set of temperature bands. It does not characterize individual rows and then refresh weak and strong rows at different rates.

Therefore:

> **environment-conditioned array refresh ≠ per-row retention-aware scheduling**.

Later retention-aware research needs separate evidence and should not be retroactively projected onto this 1991 circuit.

## Failure and forgetting boundaries

The source set supports several bounded failure questions without supplying product-level fault statistics:

- a sensor that does not adequately reflect array temperature can select a cadence that is too slow or unnecessarily fast;
- comparator thresholds and band granularity can encode an inappropriate policy for a different DRAM generation;
- improving measurement resolution can consume enough power to negate the intended maintenance-power saving;
- a correct temperature classification does not by itself prove correct row enumeration, correct refresh execution, or correct cell restoration;
- the historical examples do not prove that every cell in a real array has identical retention behavior;
- using old illustrative 8/16/32/64/128 ms values as a modern universal timing table would exceed the patent's explicit technology-dependent boundary.

The conceptual forgetting risk is therefore not only `refresh stops`. A retained value can also be lost because **the relation between environment and required maintenance is mismeasured or misclassified**.

## Prior art and anti-anachronism

This case does not claim that Micron invented temperature-dependent DRAM refresh. The Micron patent itself cites U.S. Patent 4,920,489, whose 1987-priority family already describes ambient-temperature-controlled DRAM refresh using a thermistor, A/D conversion, processor logic, and a table.

Nor does this case call the 1991 design `retention-aware refresh` as historical vocabulary. `Environment-conditioned maintenance`, `proxy`, `policy classification`, and `retention envelope` are modern engineering-reconstruction terms introduced to compare the mechanism with other cases.

Likewise, the patent's statement that refresh rate doubles for a particular temperature increment is retained as a **period engineering assertion for the disclosed technology context**, not generalized into a universal semiconductor law.

## Functional analogy and philosophical limit

A bounded functional analogy can compare temperature-dependent DRAM refresh with any retention system whose maintenance effort changes after observing an environmental or health condition. The comparable function is **maintenance conditioned by evidence about the preservation environment**.

The analogy stops there. A DRAM temperature sensor is not RAID health state, distributed replica membership, Flash wear metadata, or an archival preservation policy.

A narrow conceptual pressure does follow:

> The future interval over which a technical state can safely remain unattended may be partly constituted by the environment and by the system's retained model of that environment.

That is a philosophical/engineering interpretation of the mechanism. It is not evidence that Micron engineers formulated a theory of technological temporality.

## Cross-case result

The DRAM retention decomposition can now be extended:

```text
dynamic-cell payload / charge-loss process
    !=
retention constraint under an environmental condition
    !=
measurement of that condition
    !=
classification / guardband policy
    !=
chosen refresh cadence
    !=
recurring refresh authority
    !=
refresh-row enumeration
    !=
refresh target geometry
    !=
maintenance-induced service blocking
    !=
sense / restoration execution
```

Cases 03, 09, 10, 21, and 33 established the other dimensions. Case 34 adds the fact that **maintenance frequency can be adapted to an observed preservation environment without changing the underlying need for dynamic-state restoration**.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Micron filed US5278796A on 12 April 1991 for a temperature-dependent DRAM refresh circuit | H/P | US5278796A metadata |
| The Micron circuit uses a temperature sensor near the DRAM array, comparator-defined bands, an encoder, oscillator, and system logic to generate temperature-compensated refresh | H/P | US5278796A summary and detailed description |
| The patent gives an illustrative five-band 8/16/32/64/128 ms schedule | H/P | US5278796A detailed description; explicitly technology-dependent |
| More comparator bands improve cadence granularity but can consume enough power to erase the savings | H/P | US5278796A summary |
| Micron invented temperature-adaptive DRAM refresh | X | contradicted by the Micron patent's own citation/description of U.S. Patent 4,920,489 |
| The temperature sensor directly measures every DRAM cell's remaining charge or retention time | X | not the documented mechanism |
| Temperature adaptation eliminates the refresh obligation | X | contradicted by the patent's DRAM-refresh premise |
| Five temperature bands are intrinsic physical retention states of DRAM cells | X | control-policy discretization, not sourced physics |
| The patent's numerical temperature/refresh table is a universal modern DDR timing rule | X | patent explicitly says ranges/rates may change with technology |
| Environment-conditioned refresh cadence can be separated from refresh-row enumeration, target geometry, and self-refresh authority | E | bounded cross-case reconstruction |

| Micron's Rev. S 02/16 2Gb DDR3 datasheet exposes mutually exclusive SRT and ASR controls in MR2 | H/P | direct later manufacturer product/interface record |
| SRT forces 2x internal self refresh regardless of case temperature, while ASR automatically adjusts between 1x and 2x over the supported range | H/P | direct later product semantics |
| Above 85 °C, externally managed refresh still requires 2x cadence (64 ms → 32 ms) even though self refresh can use SRT or ASR | H/P | direct extended-temperature contract |
| ASR's automatic transition is guaranteed for data integrity but need not occur at exactly 85 °C | H/P | direct product boundary; not a per-cell retention measurement |
| The 2016 product interface proves direct implementation descent from Micron's 1991 patent | X | chronology and shared assignee are insufficient for genealogy |

## Related repositories

Current searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `temperature compensated refresh DRAM`, `temperature-dependent DRAM`, and `adaptive DRAM refresh` found no dedicated case to reuse. A comprehensive history of DRAM temperature dependence, device leakage physics, JEDEC temperature-compensated self refresh, mobile-memory standards, and modern retention-aware scheduling would belong there if pursued broadly.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) supplies the methodological guard: a modern phrase such as `environment-conditioned maintenance policy` must not be attributed to the historical actors unless their own sources use it.

## Sources

1. Charles W. Tillinghast, Michael S. Cohen, and Thomas W. Voshell, Micron Technology, Inc., **US5278796A, “Temperature-dependent DRAM refresh circuit,”** filed 12 April 1991, published/granted 11 January 1994: <https://patents.google.com/patent/US5278796A/en>.
2. Mark Hubelbank and David Shadmon, CardioData Corp., **DE3827808A1 / U.S. Patent 4,920,489 family, “Apparatus and method for solid state storage of episodic signals,”** priority 14 August 1987; the detailed storage embodiment uses a thermistor, processor A/D conversion, and a lookup table to vary DRAM refresh with ambient temperature: <https://patents.google.com/patent/DE3827808A1/en>.
3. Chien-Yi Chang, Elite Semiconductor Memory Technology, Inc., **US7035157B2, “Temperature-dependent DRAM self-refresh circuit,”** priority 27 August 2004, filed 14 September 2004, granted 25 April 2006 — used only as a later comparison showing temperature-conditioned cadence integrated with self-refresh sensing/latching/oscillator control: <https://patents.google.com/patent/US7035157B2/en>.
4. Micron Technology, Inc., **2Gb: x4, x8, x16 DDR3 SDRAM**, PDF `09005aef826aaadc`, `2Gb_DDR3_SDRAM.pdf - Rev. S 02/16 EN`, especially Mode Register 2 pp. 146–147 and Extended Temperature Usage pp. 182–183 — later manufacturer product/interface witness for SRT, ASR, external 2x refresh above 85 °C, and the non-exact automatic transition boundary. Public preserved copy inspected: <https://file.hstatic.net/1000180878/file/mt41j128m16_2gb_ddr3_sdram.pdf>.
