# Toshiba Leakage-Tracked Self-Refresh: Internalizing Refresh Scheduling

## Status

**`grounded`** — bounded to Toshiba's 1984-priority DRAM self-refresh control design disclosed in US4682306A.

Grounding record: [`../evidence/10-toshiba-1984-self-refresh-scheduling-grounding.md`](../evidence/10-toshiba-1984-self-refresh-scheduling-grounding.md).

Prior-art deepening: [`../evidence/10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md`](../evidence/10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md).

Named-product boundary deepening: [`../evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md`](../evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md).

Cross-vendor proxy-topology deepening: [`../evidence/10-sharp-1997-1998-array-coupled-leakage-refresh-deepening.md`](../evidence/10-sharp-1997-1998-array-coupled-leakage-refresh-deepening.md).

Standards-era TCSR control-boundary deepening: [`../evidence/10-micron-2005-2009-temperature-compensated-self-refresh-control-boundary.md`](../evidence/10-micron-2005-2009-temperature-compensated-self-refresh-control-boundary.md).

Named controller/device integration deepening: [`../evidence/10-xilinx-2010-micron-lpddr-refresh-authority-boundary-deepening.md`](../evidence/10-xilinx-2010-micron-lpddr-refresh-authority-boundary-deepening.md).

## Scope

This case asks what changes when DRAM refresh no longer depends on an external controller for refresh cadence and instead uses an on-chip monitor of charge decay to decide when an intermittent refresh pass begins. It is not a general history of DRAM self-refresh and does not identify the patent embodiment with a named Toshiba commercial product.

Primary source: Takayasu Sakurai and Tetsuya Iizuka, Toshiba Corp., US4682306A, _Self-refresh control circuit for dynamic semiconductor memory device_; Japanese priority 20 August 1984, US filing 20 August 1985, publication 21 July 1987.

## Relation to Cases 03 and 09

Case 03 established the underlying relation: dynamic-cell charge leaks, so state must be reconstructed before a retention limit is crossed.

Case 09 then separated the refresh obligation from refresh-row enumeration. In the bounded TI CAS-before-RAS design, the on-chip counter supplies successive refresh-row addresses, but the external processor/controller still determines how often refresh requests occur.

US4682306A describes a different boundary. It places an oscillator and refresh-address counter on the memory chip and, in its preferred embodiment, starts the refresh sequence from the state of a leak-current monitor capacitor.

The comparison is therefore:

```text
Case 03: why refresh is required
Case 09: where the next refresh row comes from
Case 10: where refresh timing/trigger generation comes from
         and what condition determines the interval
```

## Historical vocabulary and record

The patent uses `self-refresh control circuit`, `self-refresh operation automatically`, `oscillator`, `refresh address counter`, `leak current monitor circuit`, and `intermittent type refresh circuit`.

It states that then-recent dynamic-memory technology could provide on-chip self-refresh and eliminate timing or address control circuitry formerly required outside the chip. It describes an oscillator that determines refresh frequency and a refresh-address counter that supplies memory-cell addresses during refresh.

The preferred embodiment contains a monitor capacitor designed to have characteristics similar to a memory cell. A detector observes the monitor-node voltage. When that voltage drops below a designed threshold, the control path starts the oscillator and resets/starts the refresh-address counter. Oscillator pulses advance the counter; refresh addresses go to the row decoder; the array is refreshed row by row; completion recharges the monitor capacitor so a new monitoring interval begins.

The patent explicitly says refresh occurs more often when monitored leakage is large and less often when it is small. It also states that the monitor capacitor may be designed with slightly more leakage than ordinary memory-cell capacitors to provide margin before information loss.

The patent itself cites Hitachi Japanese Laid-Open Patent 59-56291, priority/filing 24 September 1982 and publication 31 March 1984, as earlier work that automatically controlled refresh frequency using leak-monitor capacitors and a comparator. That Hitachi document has now been **independently inspected** rather than used only through Toshiba's retrospective description. Its own text directly discloses a refresh-address counter, oscillator, two-capacitor leakage-simulation circuit, voltage comparator, comparator-derived self-refresh control, internally selected refresh addresses, full-array refresh, and overflow-triggered re-precharge. See the [direct prior-art addendum](../evidence/10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md).

The direct inspection moves the public manufacturer-primary floor for this bounded leakage-derived self-refresh relation to **31 March 1984**. It still does not establish first invention, commercial deployment, or a complete genealogy, and the 24 September 1982 filing/priority date must not be silently reported as the public-disclosure date. Toshiba's later preferred embodiment remains a distinct mechanism witness, notably using one monitor capacitor and a threshold/inverter control path rather than Hitachi's two retained capacitor voltages and differential comparison. This case therefore makes no priority claim for Toshiba and no priority claim for Hitachi beyond the bounded public floor.

## Retained state and maintenance state

The payload remains volatile dynamic-cell state. The refresh-address counter holds temporary maintenance-enumeration state during a refresh pass. The monitor capacitor holds a different kind of technical state: its controlled decay is observed as a proxy for how close the protected array may be to a retention boundary.

This gives a new retention relation:

> **retention infrastructure can preserve payload by intentionally allowing a proxy state to decay toward a maintenance threshold.**

`Proxy` is engineering reconstruction vocabulary, not Toshiba's historical term.

## Engineering reconstruction

### Refresh address internalization is not refresh schedule internalization

Case 09 demonstrates that a device can generate its own refresh row while still relying on an external source for refresh cadence. Case 10 provides a bounded design in which both row enumeration and the timing source/condition for starting refresh are on-chip.

### Maintenance can be condition-derived

The next refresh pass is not only a fixed external deadline event in the disclosed embodiment. A monitored electrical condition crosses a threshold and starts the maintenance sequence. The project term `condition-derived maintenance trigger` is a modern analytical description.

### A preservation system may use a state designed to approach failure first

The patent allows the monitor capacitor to leak slightly faster than ordinary cells. The monitor is therefore deliberately conservative: its decay should reach the control boundary before protected payload cells reach their loss boundary.

This makes the safety margin relational rather than merely a single nominal refresh-period number.

### Reducing maintenance frequency does not eliminate maintenance

The patent's motivation is lower standby power by avoiding refresh that is more frequent than required by the monitored condition. When refresh is needed, however, the disclosed design still performs the array-maintenance pass. Dynamic state has not become nonvolatile.

## Cross-vendor proxy-topology deepening — Sharp, 1997–1998

A later Sharp patent family provides a useful negative control for the idea of a single canonical `leak monitor`. Makoto Ihara / Sharp Corp. US6075739A claims priority from **17 February 1997**; the Japanese family was publicly laid open as JPH10289573A on **27 October 1998**, while the US publication followed on 13 June 2000. The earlier priority date is not treated as a public-disclosure date. See the [cross-vendor proxy-topology addendum](../evidence/10-sharp-1997-1998-array-coupled-leakage-refresh-deepening.md).

Sharp's first embodiment derives timer behavior from leakage demand on an existing bit-line-precharge network. The patent describes many array-connected diffusion / PN-junction leakage sources, a timer capacitor coupled to the pull-up path that compensates that leakage, an oscillator whose rate follows capacitor discharge, and binary counting that emits a refresh clock. It explicitly argues that monitoring many leakage sources averages individual junction variation.

The same patent family also discloses a materially different embodiment in which substrate-potential / back-bias restoration activity supplies the tracked condition from which refresh timing is derived. The bounded cross-vendor result is therefore:

```text
same broad preservation objective
    !=
same monitored physical state
    !=
same proxy population / aggregation boundary
    !=
same comparison or threshold logic
    !=
same refresh-clock generation path
```

Hitachi's two-capacitor differential proxy, Toshiba's deliberately conservative single-monitor preferred embodiment, Sharp's aggregate bit-line-precharge leakage path, and Sharp's substrate/back-bias path are functional relatives but not interchangeable circuits. The comparison does not establish Hitachi→Toshiba→Sharp genealogy or commercial deployment.

This adds a useful engineering distinction. **Physical similarity, conservatism, and population coverage are separate properties of a retention proxy.** An aggregate sensor may reduce sensitivity to one junction's variation without thereby proving that it safely bounds the worst-retention payload cell. Product characterization or fault-validation evidence would be needed for that stronger claim.

## Named-product boundary deepening — Toshiba pseudo-SRAM, 1994–2001

The patent record leaves a product-identity question open. A later Toshiba product-documentation chain now answers only the broad half of that question.

A preserved Toshiba **1994 Static RAM** data-book artifact lists the `TC51832A` family under `Pseudo Static RAM`. The preserved Toshiba family text describes a 32K×8 pseudo-static RAM using a **one-transistor dynamic memory cell**, while exposing an SRAM-like interface. It says the `RFSH` input supports both `Auto Refresh` and `Self Refresh`; the feature list separately says **Self refresh is supported by an internal timer** and **Auto refresh is supported by an internal refresh-address counter**, with 256 refresh cycles / 4 ms. Because the raw Bitsavers PDF could not be directly rendered in this pass and the detailed text was corroborated through a manufacturer-datasheet mirror, these lines are treated as `H/P*` pending direct facsimile page anchors rather than overstated as fully inspected page evidence. See the [named-product evidence addendum](../evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md).

Toshiba's official **18 June 2001** launch announcement supplies a second manufacturer-primary product witness. It names the `TC51W3216XB`, describes a standard SRAM interface over a one-transistor DRAM-like cell, explicitly advertises self refresh, and says a separate DRAM controller / refresh glue logic is unnecessary. The same announcement gives planned sample and full-production timing.

These sources move the product boundary, but they do not collapse it into the patent mechanism:

> **named-product self refresh != named-product leakage-tracked self refresh**

The `TC51832A` product text says `internal timer`; it does not document the preferred US4682306A leak-current-monitor capacitor, threshold detector, or refresh-frequency dependence on measured leakage. A timer cannot be silently renamed a leakage monitor merely because both can start autonomous maintenance.

The stronger decomposition is now:

```text
one-transistor dynamic payload
    !=
SRAM-like service interface
    !=
refresh-row enumeration
    !=
autonomous refresh timing
    !=
leakage-derived/adaptive refresh trigger
```

This also supplies a bounded comparison to Case 21. Both Toshiba pseudo-SRAM and Micron SDRAM can internalize recurring refresh work, but their external interfaces and documented mode semantics differ. The comparison is functional, not a Toshiba→Micron or patent→JEDEC genealogy.

Finally, Toshiba's 2001 statement that a separate refresh controller/glue logic is unnecessary is an interface-placement result, not evidence that maintenance disappeared:

> **external refresh burden removed != refresh obligation removed**.

The physical payload remains dynamic in the named product descriptions, and `Self Refresh` does not establish unpowered nonvolatility.

## Standards-era temperature-proxy / control-authority deepening — Micron, 2005–2009

Micron's Mobile DDR / low-power-DDR technical notes provide a deliberately later negative control for the earlier leakage-derived circuits. See [`../evidence/10-micron-2005-2009-temperature-compensated-self-refresh-control-boundary.md`](../evidence/10-micron-2005-2009-temperature-compensated-self-refresh-control-boundary.md).

TN-46-12, whose revision history records a first draft in **October 2005**, says Micron and other JEDEC members had defined `Temperature Compensated Self Refresh (TCSR)` as a mobile-DRAM power-saving feature. It describes two control placements: an on-DRAM temperature sensor can adjust self-refresh intervals automatically, or—if no on-board sensor exists—the memory controller can use its own temperature sensor and program the appropriate DRAM control bits.

Micron's January **2007** TN-46-15 then documents a stronger implementation boundary. It says low-power DDR uses an **on-chip temperature sensor** to control refresh interval, and that programming the **JEDEC-standard TCSR bits will not have an effect** on that device because the on-chip self-refresh oscillator continues at a factory-optimized rate for the device temperature. The extended-mode-register figure repeats the point: an on-die sensor is used in place of TCSR-bit control. The same figure keeps PASR selection active.

This establishes several bounded relations without claiming circuit genealogy:

```text
temperature-derived maintenance
    !=
direct charge-decay / leakage-state sensing

control field exists
    !=
control field is causally effective on this implementation

sensor location
    !=
policy-decision location
    !=
control-field visibility
    !=
effective cadence authority

maintenance cadence policy
    !=
maintenance coverage policy
```

The comparison is functional. Nothing inspected here proves that Hitachi, Toshiba, or Sharp influenced Micron TCSR or the JEDEC field. Likewise, the actual 2005–2007 normative JEDEC TCSR clause was not directly inspected; the source supports only Micron's historical statement that the bits were JEDEC-standard and the documented implementation behavior in which they were ineffective.

This later evidence changes the conceptual emphasis of Case 10. A preservation system need not derive its maintenance decision from a proxy that physically resembles the payload cell. Temperature can be used as a retention-relevant condition from which cadence is selected. And even when the interface retains a named policy field, the actual authority over preservation work can migrate behind that interface.

## Controller/device integration deepening — Xilinx Spartan-6 MCB + Micron Mobile LPDDR, 2009–2010

The Micron TCSR evidence identifies a device-side authority boundary, but it does not by itself show what a contemporaneous external memory controller actually owns. Xilinx UG388 v2.3 (9 August 2010) now supplies the controller-side half, and its supported-device table includes Micron's `MT46H32M16xxxx-5` 512Mb ×16 LPDDR family. See [`../evidence/10-xilinx-2010-micron-lpddr-refresh-authority-boundary-deepening.md`](../evidence/10-xilinx-2010-micron-lpddr-refresh-authority-boundary-deepening.md).

The key controller attribute is `C_MEM_TREFI`, which UG388 defines as the **Average Periodic Refresh Interval** and explicitly describes as the rate at which the **MCB refreshes the memory, not the self-refresh interval**. The same guide separately exposes SELF REFRESH entry/exit and an LPDDR `C_MEM_MOBILE_PA_SR` Partial Array Self-Refresh setting with `Full` / `Half` choices.

Micron's December-2009 512Mb Mobile LPDDR documentation supplies the matching device-side semantics. Its TCSR cadence is controlled by an automatic on-die temperature sensor; the nominal TCSR fields have no effect on that device, while PASR remains externally configurable through the extended mode register. During SELF REFRESH, refresh intervals are scheduled internally and may vary or differ from ordinary `tREFI`; regions excluded by PASR are not retained.

This produces a named integration-level authority split:

```text
ordinary operation:
    controller periodic AUTO REFRESH cadence
        -> C_MEM_TREFI

mode transition:
    user / controller SELF REFRESH entry and exit

inside SELF REFRESH:
    device-internal temperature-sensor / oscillator cadence

retained spatial scope:
    externally selected PASR coverage
```

The engineering result is therefore:

```text
mode-entry authority
    !=
cadence authority
    !=
coverage authority
    !=
restoration execution
```

and, more specifically:

```text
controller supports SELF REFRESH
    !=
controller owns the internal SELF REFRESH clock
```

The paired documents also show that one retention relation can distribute **temporal policy** and **spatial policy** differently: Micron internalizes effective cadence control while leaving PASR coverage externally selectable. This is a functional control decomposition, not evidence of a historical Toshiba→Micron→Xilinx genealogy.

The slice deliberately does not claim to have inspected the controlling 2005–2007 normative JEDEC TCSR clause. It narrows an implementation boundary with manufacturer-primary controller/device evidence while leaving standard genealogy as a separate debt.

## Failure boundaries

The sourced mechanism separates several failure classes. A monitor that is not conservative enough can initiate maintenance too late; an overly conservative monitor can cause needless refresh and power cost; an incorrect threshold can reduce safety margin; and correct triggering still does not guarantee correct row enumeration or correct row restoration. The Sharp deepening adds another boundary: an aggregate leakage proxy can smooth individual-source variation without proving that it captures the worst-retention cell. The Micron TCSR deepening adds a different class: a controller-sensed design can fail in temperature observation / policy programming, while an on-die automatic design moves the relevant authority and failure path behind the external TCSR field. The Xilinx/Micron integration adds a further separation: wrong controller `tREFI`, wrong device-internal SELF REFRESH cadence, wrong PASR coverage, and failed SELF REFRESH entry/exit are different failure surfaces. These are engineering implications of the documented partitions, not measured failure rates for commercial Toshiba, Sharp, Micron, or Xilinx systems.

## Functional analogy and anti-anachronism

`Adaptive refresh`, `condition-derived scheduling`, `proxy state`, `sentinel`, and `refresh authority` can be useful modern comparisons, but they are not presented as period Toshiba terminology. Historical claims remain in the patents' and manufacturer documents' own vocabulary.

US4682306A is a manufacturer-primary design disclosure, not proof that a named Toshiba DRAM or pseudo-SRAM used the exact preferred embodiment. It also cannot support a `first adaptive self-refresh` claim because the patent itself identifies earlier Hitachi work. Likewise, the Sharp family is design disclosure rather than proof of a named shipping part.

Later SDRAM `AUTO REFRESH`, JEDEC self-refresh entry/exit, DDR per-bank refresh, and modern retention-aware policies remain separate regimes. The Micron addendum narrows one later bridge: standards-era TCSR can use temperature and can place effective cadence authority somewhere other than the host-visible TCSR field. The Xilinx/Micron integration narrows another: an external controller can own ordinary periodic-refresh timing and SELF REFRESH transitions without owning the internal cadence once the DRAM enters SELF REFRESH. Neither comparison turns the later regime into the same mechanism as the 1980s leakage-monitor designs.

## Philosophical limit

A bounded conceptual question follows from the mechanism: apparent persistence can be maintained by instrumenting an approaching loss condition and converting it into maintenance work. The Sharp comparison adds that the useful signal need not be a miniature copy of the payload state; it can be an aggregate signature emitted by surrounding infrastructure. The Micron comparison adds that a visible control representation need not exhaust the effective policy relation: a named field can remain present while the preservation decision has moved to an internal sensor/control path. The Xilinx/Micron integration adds that preservation authority itself can be distributed by dimension: the component that requests a preservation mode need not own its internal cadence, while another externally selected field can still govern the spatial scope of what is preserved. These are interpretations of engineering relations, not historical claims that Toshiba, Hitachi, Sharp, Micron, Xilinx, or JEDEC engineers formulated a philosophy of retention, representation, or authority.

## Cross-case result

The refresh-control decomposition is now:

```text
payload decay / retention constraint
    !=
condition monitor / proxy topology
    !=
proxy aggregation boundary
    !=
sensor / observation location
    !=
maintenance-policy decision location
    !=
control-field visibility
    !=
effective cadence authority
    !=
mode-entry / exit authority
    !=
maintenance trigger
    !=
active-pass timing source
    !=
coverage policy
    !=
row enumeration
    !=
row selection
    !=
sense / restoration
```

Case 09 grounds the separation between external trigger cadence and internal row enumeration. Case 10 grounds designs in which monitored physical conditions participate in generating refresh timing while showing that the monitored proxy, aggregation topology, sensor location, effective policy authority, mode-transition authority, and coverage authority can vary materially across manufacturer disclosures and controller/device boundaries.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Toshiba disclosed same-chip self-refresh with oscillator and refresh-address counter | H/P | US4682306A |
| A monitor capacitor and threshold can start the disclosed refresh sequence | H/P | US4682306A |
| Oscillator pulses advance the refresh-address counter through the refresh pass | H/P | US4682306A |
| The monitor may be designed with slightly greater leakage to provide margin | H/P | US4682306A |
| Hitachi publicly disclosed a two-capacitor leakage-simulation + comparator self-refresh mechanism by 31 March 1984 | H/P | directly inspected JPS5956291A |
| The 1982 Hitachi filing/priority date is itself a public-disclosure date | X | filing/priority must remain distinct from 1984 publication |
| Hitachi's two-capacitor comparator circuit and Toshiba's single-monitor preferred embodiment are the same circuit | X | shared preservation function does not erase circuit differences |
| Sharp publicly disclosed an array-coupled leakage-derived refresh-timing family by 27 Oct 1998 | H/P | JPH10289573A / US6075739A family record |
| Sharp's first embodiment couples timer behavior to leakage demand on the bit-line-precharge network and many array-connected junctions | H/P | US6075739A |
| The Sharp family also discloses substrate/back-bias-cycle-derived refresh timing | H/P | US6075739A |
| Aggregate leakage sensing proves coverage of the worst-retention payload cell | X | patent gives averaging rationale, not worst-cell validation |
| A named Sharp commercial part is proven to use either disclosed mechanism | X | no product tie established here |
| A named Toshiba pseudo-SRAM family is documented with Auto Refresh and Self Refresh | H/P* | Toshiba 1994 data-book artifact + preserved `TC51832A` family text |
| `TC51832A` Self Refresh is documented as using an internal timer while Auto Refresh uses an internal refresh-address counter | H/P* | preserved Toshiba family text; direct facsimile page anchors remain open |
| Toshiba publicly announced a named `TC51W3216XB` pseudo-SRAM with a one-transistor DRAM-like cell, SRAM interface, and self refresh in 2001 | H/P | Toshiba corporate release, 18-Jun-2001 |
| Named-product self refresh proves deployment of the US4682306A leak-monitor threshold path | X | product evidence does not expose the patent's monitor/threshold mechanism |
| A named Toshiba commercial part is proven to use this exact leakage-tracked circuit | X | still unsupported; broad self-refresh productization is now grounded, exact circuit identity is not |
| Micron documented TCSR as a JEDEC-member mobile-DRAM power-saving feature by Oct. 2005 | H/P | TN-46-12 revision history + text |
| TN-46-12 permits either on-DRAM automatic temperature sensing or controller-side sensing + programmed DRAM control bits | H/P | TN-46-12 |
| Micron TN-46-15 states that an on-chip temperature sensor controls the LPDDR self-refresh interval | H/P | TN-46-15, Jan. 2007 |
| TN-46-15 calls the TCSR fields JEDEC-standard but says programming them has no effect on the documented device | H/P | TN-46-15 text + extended-mode-register note |
| A standards-visible maintenance field necessarily has effective policy authority on every implementation | X | directly contradicted by TN-46-15 |
| Temperature-derived TCSR is electrically the same mechanism as the 1980s leakage-monitor patents | X | different observed condition; genealogy not established |
| The exact 2005–2007 normative JEDEC TCSR clause is established by this case | X | normative standard text not directly inspected in this slice |
| Xilinx UG388 v2.3 supports LPDDR and lists Micron `MT46H32M16xxxx-5` as a supported 512Mb ×16 family | H/P | UG388 supported-device table |
| Xilinx `C_MEM_TREFI` is the MCB periodic-refresh interval and explicitly not the self-refresh interval | H/P | UG388 memory-device attributes |
| Xilinx exposes LPDDR Partial Array Self-Refresh coverage with `C_MEM_MOBILE_PA_SR` | H/P | UG388 memory-device attributes |
| Micron Rev. I 12/09 documents internally scheduled SELF REFRESH cadence controlled by an on-die temperature path while PASR remains externally configurable | H/P | Micron 512Mb Mobile LPDDR datasheet |
| Controller periodic-refresh cadence, SELF REFRESH entry/exit, internal cadence, and coverage policy are one undifferentiated authority | X | contradicted by the paired Xilinx/Micron documentation |
| `tREFI` is one universal refresh interval across ordinary operation and SELF REFRESH | X | explicitly rejected by Xilinx and Micron documentation |
| Toshiba invented adaptive refresh generally | X | blocked by the patent's own Hitachi prior-art discussion |
| Internal refresh addressing automatically implies internal refresh scheduling | X | contradicted by the Case-09/Case-10 comparison |
| A deliberately decaying proxy can trigger payload-preservation work | E | bounded reconstruction from the monitor role |
| Leakage-derived refresh can use materially different proxy and aggregation topologies | E | bounded cross-vendor reconstruction from Hitachi, Toshiba, and Sharp records |
| Sensor location, control-field visibility, and effective refresh-cadence authority are separable | E | bounded reconstruction from Micron TN-46-12 / TN-46-15 |
| Mode-transition authority, cadence authority, and coverage authority are separable at a named controller/device boundary | E | bounded reconstruction from Xilinx UG388 + Micron Rev. I 12/09 |

## Related repositories

Current searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for the Toshiba leak-monitor mechanism, `US6075739`, `TN-46-15`, `temperature compensated self refresh`, `UG388`, `MT46H32M16`, and related self-refresh leakage terms found no dedicated treatment to reuse. A broader history of DRAM generations, pseudo-SRAM, LPDDR standardization, FPGA memory controllers, oscillator and back-bias design, temperature sensing, process leakage, manufacturer competition, and later standards belongs there rather than being duplicated here.

`tmzncty/problem-history` remains the methodological guard against projecting later `adaptive refresh`, `refresh authority`, or JEDEC terminology backward.

## Sources

1. Takayasu Sakurai and Tetsuya Iizuka, Toshiba Corp., US4682306A, _Self-refresh control circuit for dynamic semiconductor memory device_: <https://patents.google.com/patent/US4682306A/en>.
2. Hitachi Ltd., JPS5956291A, _MOS storage device_, application/priority 24 September 1982, publication 31 March 1984 — now directly inspected for the two-capacitor leakage-simulation/comparator self-refresh mechanism; detailed anchors and limits are in [`../evidence/10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md`](../evidence/10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md): <https://patents.google.com/patent/JPS5956291A/en>.
3. Toshiba, **1994 Static RAM** data book, preserved scan: <https://www.bitsavers.org/components/toshiba/_dataBook/1994_Toshiba_Static_RAM.pdf>.
4. Toshiba Semiconductor, **TC51832A family / TC51832AP, 32,768 word × 8-bit CMOS Pseudo Static RAM**, preserved manufacturer-datasheet mirror: <https://www.alldatasheet.com/datasheet-pdf/pdf/1462395/TOSHIBA/TC51832AP.html>.
5. Toshiba Corporation, **“Toshiba Announces its 32Mb Pseudo SRAM Solution,”** 18 June 2001: <https://www.global.toshiba/ww/news/corporate/2001/06/pr1802.html>.
6. H. Kawamoto et al., “A 288Kb CMOS Pseudo SRAM,” _ISSCC Digest of Technical Papers_, 1984, pp. 276–277, DOI 10.1109/ISSCC.1984.1156683 — period context cited by the patent, not a central mechanism source in this case.
7. Makoto Ihara / Sharp Corp., US6075739A, _Semiconductor storage device performing self-refresh operation in an optimal cycle_; Japanese family laid open as JPH10289573A on 27 October 1998: <https://patents.google.com/patent/US6075739A/en>.
8. Micron Technology, Inc., **TN-46-12: _Mobile DRAM Power-Saving Features and Power Calculations_**, Rev. A Oct. 2005 / Rev. B May 2009, inspected manufacturer text preserved at: <https://dtsheet.com/doc/1384408/tn-46-12--mobile-dram-power-saving-features-calculations>.
9. Micron Technology, Inc., **TN-46-15: _Low-Power Versus Standard DDR SDRAM_**, Rev. A, 22 Jan. 2007, inspected manufacturer text preserved at: <https://dtsheet.com/doc/1384279/tn4615--low-power-versus-standard-ddr-sdram>.
10. Micron Technology, **DRAM power calculators**, current support page listing Mobile LPDRAM TN-46-12: <https://www.micron.com/sales-support/design-tools/dram-power-calculator>.
11. Freescale Semiconductor, **_MPC5121e DRAM Controller_**, Rev. 2 (2009), surviving copy preserving TN-46-15's legacy Micron URL and separately referencing JESD209: <https://manuals.plus/m/fd2a88e34742801074da475b621e1bec8a57e5b296ebe5e29d01ecf797b92919>.
12. Xilinx, **_Spartan-6 FPGA Memory Controller User Guide (UG388)_**, v2.3, 9 Aug. 2010, official AMD/Xilinx archive: <https://docs.amd.com/v/u/en-US/ug388>.
13. Micron Technology, Inc., **_512Mb: x16, x32 Mobile LPDDR SDRAM_**, Rev. I, Dec. 2009, PDF identifier `09005aef82d5d305`, device families including `MT46H32M16LF` / `MT46H16M32LF`; preserved document index: <https://datasheet.eeworld.com.cn/view/7768840.html>.
