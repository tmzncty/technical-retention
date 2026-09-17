# Evidence 10 Addendum — Xilinx Spartan-6 MCB / Micron Mobile LPDDR Refresh-Authority Boundary, 2009–2010

## Status

**`bounded deepening complete`** — named controller/device-family integration evidence separating controller-owned periodic AUTO REFRESH cadence, controller-selected self-refresh coverage, user/controller orchestration of SELF REFRESH entry/exit, and device-internal SELF REFRESH cadence.

This addendum does **not** close the still-open direct-inspection debt for the 2005–2007 normative JEDEC TCSR clause. It instead uses contemporaneous manufacturer documentation from both sides of an LPDDR interface to establish a narrower engineering boundary that can be grounded without reconstructing the standard from secondary descriptions.

---

## Purpose

Case 10 already establishes several distinct refresh-control arrangements:

- early leakage-derived self-refresh circuits in which an on-chip physical condition participates in deciding when maintenance begins;
- a Toshiba pseudo-SRAM product boundary showing that named-product `Self Refresh` does not by itself prove deployment of the earlier leak-monitor circuit;
- Micron 2005–2009 Mobile DDR / LPDDR documentation separating temperature sensing, TCSR control-field visibility, effective cadence authority, and PASR coverage policy.

One remaining integration question is especially useful for technical retention:

> When a real memory controller supports a real LPDDR product family, does `the controller supports self refresh` mean the controller owns the self-refresh maintenance cadence?

For the bounded Xilinx Spartan-6 Memory Controller Block (MCB) and Micron 512Mb Mobile LPDDR documentation inspected here, the answer is no.

The controller has meaningful retention authority, but that authority is partitioned:

```text
controller periodic AUTO REFRESH cadence
    !=
SELF REFRESH entry / exit orchestration
    !=
SELF REFRESH internal cadence
    !=
SELF REFRESH array-coverage policy
```

The result is not a generic LPDDR theorem. It is a named, contemporaneous controller/device-family witness showing that temporal and spatial preservation authority can be split across an interface.

---

## Source identity and chronology

### Xilinx UG388, Spartan-6 FPGA Memory Controller

**Xilinx, _Spartan-6 FPGA Memory Controller User Guide (UG388)_, v2.3, 9 August 2010.**

Official AMD/Xilinx archive:

- <https://docs.amd.com/v/u/en-US/ug388>

The inspected v2.3 guide documents the hard Memory Controller Block (MCB) used with Spartan-6 devices. It explicitly includes LPDDR among supported memory types and provides both configuration attributes and supported-device tables.

The revision history records earlier UG388 revisions, including an initial release in 2009. This addendum does not back-project every v2.3 statement into the first release; historical claims below are bounded to the inspected 2010 v2.3 text unless an earlier date is independently established.

### Micron 512Mb Mobile LPDDR, Rev. I, December 2009

**Micron Technology, Inc., _512Mb: x16, x32 Mobile LPDDR SDRAM_, Rev. I, 12/09, PDF identifier `09005aef82d5d305`; device families include `MT46H32M16LF` and `MT46H16M32LF`.**

The surviving manufacturer-primary text was inspected through preserved datasheet mirrors/indexes. Useful preservation points include:

- <https://datasheet.eeworld.com.cn/view/7768840.html>
- <https://www.micro-semiconductor.com/datasheet/43-MT46H16M32LFCM-6-L-IT-B.pdf>

The document's revision history places production-document revisions in 2008 and identifies Rev. I as December 2009. The arguments here use the Rev. I content as the contemporaneous device-side witness.

A later revision of the same family was also visually checked only as a continuity/control aid for the relevant tables and mode descriptions. It is **not** used to move later wording backward into 2009 when the Rev. I text does not already support it.

### Supported-family relation

UG388's supported-device table includes the Micron `MT46H32M16xxxx-5` 512Mb ×16 LPDDR family. The Micron Rev. I document covers the `MT46H32M16LF` 512Mb ×16 family.

This supplies a bounded manufacturer-side integration relation:

```text
Xilinx MCB LPDDR support
    +
Micron 512Mb x16 Mobile LPDDR family listed in the controller guide
```

It does **not** prove that one particular deployed Spartan-6 board used one exact Micron suffix, nor does it prove that every Xilinx-supported Micron ordering code exercised every optional feature discussed below.

---

## Direct historical / implementation record

### H/P — the Spartan-6 MCB explicitly supports LPDDR

UG388 lists DDR, DDR2, DDR3, and LPDDR among the memory types supported by the Spartan-6 MCB.

This matters because the following controller attributes are not generic software abstractions detached from a memory interface; they are part of a concrete FPGA memory-controller configuration surface.

### H/P — Xilinx exposes a Partial Array Self-Refresh coverage setting

UG388 defines the memory-device attribute:

- `C_MEM_MOBILE_PA_SR` — **Partial Array Self-Refresh Size**.

For LPDDR the listed values are `Full` or `Half`.

The controller therefore exposes a host/controller-side choice about the **coverage** of data retention while the device is in self refresh.

This is a spatial policy variable:

```text
which portion of the LPDDR array is requested to remain refreshed?
```

It is not, by itself, a refresh-frequency variable.

### H/P — Xilinx explicitly separates MCB periodic refresh from self-refresh interval

UG388 defines:

- `C_MEM_TREFI` — **Average Periodic Refresh Interval**.

Crucially, the guide states that this is the rate at which the **MCB refreshes the memory**, **not the self-refresh interval**.

That sentence is the central controller-side boundary for this slice. It prevents the common shortcut:

```text
controller tREFI setting
    =
device self-refresh cadence
```

For the documented MCB interface, those are different timing domains.

### H/P — Xilinx exposes SELF REFRESH entry and exit as a user-visible operation

UG388's `Self Refresh` section documents a user request that causes the memory to enter self refresh and a corresponding path for exit. It describes self refresh as supported for LPDDR, DDR2, and DDR3.

This establishes controller/user participation in the **mode transition**.

It does not say that the external controller generates each internal self-refresh restoration event once the DRAM has entered that mode.

### H/P — Xilinx lists the Micron 512Mb ×16 LPDDR family

UG388's supported-device table includes `MT46H32M16xxxx-5` as a 512Mb ×16 Micron LPDDR family.

This does not turn the Xilinx guide into a Micron datasheet. It does, however, justify comparing the controller's documented division of responsibility with the contemporaneous Micron family documentation as a bounded integration pair rather than as two unrelated examples.

### H/P — Micron places TCSR cadence control behind an on-chip temperature sensor

The Micron Rev. I device documentation describes two self-refresh-related features:

- Temperature-Compensated Self Refresh (TCSR);
- Partial-Array Self Refresh (PASR).

For the documented device, TCSR is controlled by an automatic on-chip temperature sensor. The TCSR bits remain part of the mode-register vocabulary, but the datasheet says they have no effect on this device because the on-die sensor controls the self-refresh oscillator at the appropriate factory-programmed rate for device temperature.

Thus, on this device family:

```text
TCSR field exists
    !=
external TCSR field owns effective cadence
```

### H/P — Micron leaves PASR as an externally configurable coverage policy

The same Micron documentation describes PASR as configurable through the extended mode register.

The available retention coverage includes fractions such as full, half, quarter, eighth, and sixteenth of the array. It also warns that data in regions not selected for self refresh is not retained during that mode.

This is a different control axis from TCSR:

```text
PASR
    -> which array region receives self-refresh preservation

TCSR / internal sensor-oscillator relation
    -> how self-refresh cadence is selected
```

The two policies coexist without having the same authority placement.

### H/P — Micron says SELF REFRESH scheduling is internal and may differ from tREFI

The Micron SELF REFRESH operation description states that refresh intervals are scheduled internally while the device remains in self refresh. It also allows those internal intervals to vary and to differ from the externally specified periodic `tREFI` relation used for ordinary AUTO REFRESH operation.

The datasheet further warns that SELF REFRESH is not to be used as a substitute for AUTO REFRESH.

This independently matches the Xilinx-side warning that the controller's `C_MEM_TREFI` is **not** the self-refresh interval.

The two manufacturer documents therefore agree on a bounded interface distinction without requiring us to infer it solely from one side.

---

## Engineering reconstruction

### E — refresh authority is not one scalar property

A phrase such as `the controller controls refresh` is too coarse for this integration.

The documented relation is better decomposed as:

```text
ordinary powered operation
    controller owns periodic AUTO REFRESH request cadence
        -> C_MEM_TREFI

mode transition
    user/controller participates in SELF REFRESH entry / exit

inside SELF REFRESH
    DRAM owns internal cadence through its temperature-sensor / oscillator path

coverage policy
    external configuration can select PASR coverage
```

Thus:

```text
mode-entry authority
    !=
cadence authority
    !=
coverage authority
    !=
row-restoration execution
```

The last term is deliberately generic: this addendum does not reconstruct undocumented internal row-machine details beyond what the manufacturer documents require.

### E — controller support for SELF REFRESH does not imply controller ownership of its maintenance clock

The controller can be essential to entering and exiting a preservation mode while the device itself owns the maintenance cadence during that mode.

This gives a useful retention distinction:

```text
orchestrating preservation-mode transition
    !=
executing / timing every preservation action inside the mode
```

That distinction matters whenever a software or controller interface exposes a high-level power/retention state but the physical preservation mechanism is hidden behind the device boundary.

### E — temporal and spatial preservation policy can have different owners

The Micron device internalizes the temperature-to-self-refresh-cadence decision while still allowing external configuration of PASR coverage.

Therefore one physical array can simultaneously have:

```text
internal temporal policy authority
    +
external spatial coverage authority
```

This is a stronger result than simply saying that TCSR and PASR are different features. It shows that the preservation relation itself can be partitioned across components by dimension.

### E — `tREFI` is a boundary contract for one maintenance regime, not a universal retention clock

Xilinx's wording makes the scope unusually explicit: `C_MEM_TREFI` controls the rate at which the MCB refreshes memory and is not the self-refresh interval.

Micron independently says internal self-refresh intervals may vary and may differ from `tREFI`.

A bounded reconstruction is therefore:

```text
same DRAM payload
    can be maintained under

external periodic-refresh scheduling
    or
internal self-refresh scheduling
```

The payload-retention obligation persists, while the authority and timing representation used to satisfy it change across the mode boundary.

### E — a visible control surface need not expose every causally effective preservation variable

Xilinx exposes `C_MEM_MOBILE_PA_SR` and `C_MEM_TREFI`; Micron exposes PASR/TCSR mode-register vocabulary. Yet the effective self-refresh cadence for the documented Micron device is controlled by the on-die sensor/oscillator path rather than the nominal TCSR bits.

Therefore:

```text
interface-visible state
    !=
complete preservation-policy state
```

This is consistent with the earlier Micron TCSR addendum, but the controller/device pairing makes the division concrete at an actual integration boundary.

---

## Failure and forgetting boundaries

The authority decomposition implies distinct failure classes that should not be collapsed into `refresh failed`.

### Wrong periodic AUTO REFRESH cadence

If controller-driven refresh is too infrequent during ordinary operation, the failure lies in the controller-side periodic-refresh regime or its configuration.

That is not the same as a defective internal self-refresh oscillator.

### Wrong internal SELF REFRESH cadence

A device-side temperature sensor, oscillator, or internal policy path can in principle choose an unsafe maintenance cadence while the external controller's ordinary `tREFI` setting remains correct.

The manufacturer documents establish the authority boundary, not a measured failure rate for this Micron family.

### Wrong PASR coverage

A controller may intentionally or accidentally select a retention region smaller than the data that must survive self refresh.

Micron explicitly states that unselected regions do not retain their data in self refresh.

This is a **coverage-policy failure**, not evidence that cells within the selected region exceeded their refresh deadline.

### SELF REFRESH entry/exit failure

A mode-transition failure can prevent the device from reaching or leaving self refresh even if the device's internal cadence machinery would otherwise be correct.

Thus:

```text
transition correctness
    !=
maintenance cadence correctness
    !=
coverage correctness
```

### Preserved controller configuration does not necessarily preserve complete effective refresh policy

Saving and restoring Xilinx controller attributes such as `C_MEM_TREFI` would reconstruct the controller's ordinary periodic-refresh timing but would not thereby serialize the Micron device's effective temperature-sensor state or factory internal cadence relation.

This is an engineering boundary, not a claim about the exact persistence/reset behavior of the sensor across a power cycle.

---

## Functional comparison to Cases 03, 09, and earlier Case-10 evidence

This section is **functional analogy / contrast**, not genealogy.

### Case 03 — why restoration is required

Case 03 grounds dynamic retention as bounded physical survival plus scheduled restoration. It establishes that a stable logical address does not remove the refresh deadline.

### Case 09 — row enumeration can be internal while cadence remains external

The CAS-before-RAS case shows that a DRAM can internalize refresh-row enumeration while the external controller still determines when refresh cycles occur.

### Earlier Case 10 — the maintenance trigger/cadence can also move on chip

The Hitachi/Toshiba/Sharp evidence shows several physical-condition-derived ways of moving more of the refresh-timing decision behind the device boundary.

### This integration slice — authority can move again at a mode boundary

The Xilinx/Micron pairing shows a system where, for the same device family:

```text
outside SELF REFRESH:
    controller-side periodic refresh timing is explicit

inside SELF REFRESH:
    device-side cadence is internal

for retained spatial scope:
    external PASR policy remains meaningful
```

This is not a single historical line from 1980s leakage monitors to Xilinx or Micron. It is a functional comparison showing that the location of retention authority is itself an engineering variable.

---

## Philosophical interpretation

The exact technical fact that creates the conceptual problem is narrow:

> the component that requests a preservation mode need not be the component that determines the cadence of preservation work inside that mode, and the component that owns cadence need not own the spatial scope of what is preserved.

A cautious interpretation follows. Technical `care for the same state` can be distributed as a relation among components rather than localized in one memory object or one controller. The future availability of the payload depends on a coordinated partition of authority:

- one component can decide **when to enter** a preservation regime;
- another can decide **how often** restoration occurs inside it;
- an externally visible policy can decide **what region** is worth preserving.

This does not imply that historical Xilinx or Micron engineers formulated a philosophy of distributed retention authority. It is a project-level interpretation of the documented engineering relation.

---

## Explicit non-claims

This addendum does **not** claim that:

1. Xilinx invented LPDDR self refresh, TCSR, or PASR;
2. Micron invented TCSR or PASR;
3. UG388 directly reproduces or proves the full normative semantics of JESD209/JESD209A;
4. the still-open 2005–2007 JEDEC TCSR normative-clause debt is closed;
5. Xilinx's MCB controls the Micron device's on-die temperature sensor;
6. Xilinx's `C_MEM_TREFI` is the Micron self-refresh oscillator interval;
7. the external controller owns every self-refresh row transition;
8. the Micron TCSR bits are causally effective merely because they are named in the register map;
9. every LPDDR device ignores TCSR bits in the same way;
10. every Micron 512Mb ordering code supports identical optional behavior;
11. Xilinx's `Full`/`Half` PASR configuration surface exposes every PASR fraction that the Micron device family can represent;
12. one particular deployed board is proven to have paired Spartan-6 MCB with one exact Micron ordering suffix;
13. PASR is a form of unpowered nonvolatile retention;
14. data loss in a PASR-excluded region proves a physical defect in cells within the retained region;
15. Xilinx's self-refresh entry/exit orchestration is the same mechanism as Micron's internal temperature-compensated scheduling;
16. the 1980s Hitachi/Toshiba/Sharp leakage-monitor designs are genealogical ancestors of the Xilinx/Micron integration;
17. preserving controller-register values is sufficient to preserve every hidden internal maintenance-policy state;
18. the inspected documents establish a universal LPDDR architecture across vendors and generations.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Spartan-6 MCB supports LPDDR | H/P | Xilinx UG388 v2.3 |
| UG388 lists a Micron `MT46H32M16xxxx-5` 512Mb ×16 LPDDR family | H/P | Xilinx supported-device table |
| Xilinx exposes `C_MEM_MOBILE_PA_SR` with Full/Half LPDDR coverage choices | H/P | Xilinx UG388 memory-device attributes |
| Xilinx defines `C_MEM_TREFI` as MCB periodic-refresh rate and explicitly says it is not the self-refresh interval | H/P | Xilinx UG388 |
| Xilinx exposes user/controller SELF REFRESH entry and exit | H/P | Xilinx UG388 `Self Refresh` section |
| Micron Rev. I 12/09 documents on-chip temperature-sensor control of self-refresh cadence | H/P | Micron 512Mb Mobile LPDDR datasheet |
| Micron says the TCSR bits have no effect on this device because the on-die sensor controls the self-refresh oscillator | H/P | Micron 512Mb Mobile LPDDR datasheet |
| Micron exposes PASR as a separately configurable coverage policy and warns that unselected regions do not retain data | H/P | Micron 512Mb Mobile LPDDR datasheet |
| Micron says self-refresh intervals are internally scheduled and may differ from `tREFI` | H/P | Micron SELF REFRESH operation text |
| Controller periodic-refresh cadence and device self-refresh cadence are separate authority domains in this bounded integration | E | reconstruction from Xilinx + Micron interface evidence |
| Self-refresh mode-entry authority, cadence authority, and coverage authority can be split across the system | E | reconstruction from Xilinx + Micron interface evidence |
| External spatial retention policy can coexist with internal temporal retention policy | E | reconstruction from PASR + TCSR boundary |
| `controller supports self refresh` means the controller owns the internal self-refresh clock | X | contradicted by the paired documentation |
| `tREFI` is one universal refresh interval across ordinary and self-refresh modes | X | explicitly contradicted by both manufacturer documents |
| Presence of TCSR fields proves externally effective cadence authority | X | contradicted by Micron's device-specific note |
| This slice establishes the normative JEDEC TCSR clause | X | normative standard not directly inspected here |

---

## Related-repository audit

A repository search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `TCSR Temperature Compensated Self Refresh` did not surface a dedicated history packet to reuse. This addendum therefore keeps only the retention-specific authority decomposition needed here.

A broader history of Mobile DDR / LPDDR standardization, FPGA hard memory controllers, self-refresh command sequencing, temperature sensors, and DRAM-controller product competition belongs primarily in `computing-archaeology` if developed later.

`tmzncty/problem-history` remains the methodological guard against turning the modern project term `refresh authority` into supposed period vocabulary.

---

## Remaining evidence debt

This slice deliberately leaves several bounded tasks open:

- direct inspection of the relevant 2005–2007 normative JEDEC TCSR/PASR clauses and their revision/ballot chronology;
- exact Xilinx command / EMR-write sequence by which `C_MEM_MOBILE_PA_SR` becomes an LPDDR PASR setting;
- whether and how a particular Spartan-6 design preserves or reapplies PASR configuration across controller reset;
- device-side characterization or fault-injection evidence for wrong TCSR cadence versus wrong PASR coverage;
- a fielded-board witness tying one exact Spartan-6 design to one exact Micron ordering code, if deployment history becomes relevant;
- earlier or cross-vendor controller/device pairings that would show whether this authority split was conventional, optional, or vendor-specific.

None of these are needed for the bounded conclusion established here.

---

## Sources

1. Xilinx, **_Spartan-6 FPGA Memory Controller User Guide (UG388)_**, v2.3, 9 August 2010, official AMD/Xilinx archive: <https://docs.amd.com/v/u/en-US/ug388>.
2. Micron Technology, Inc., **_512Mb: x16, x32 Mobile LPDDR SDRAM_**, Rev. I, December 2009, PDF identifier `09005aef82d5d305`, device families including `MT46H32M16LF` / `MT46H16M32LF`; preserved manufacturer-document index: <https://datasheet.eeworld.com.cn/view/7768840.html>.
3. Preserved PDF mirror for the same Micron family / document chain: <https://www.micro-semiconductor.com/datasheet/43-MT46H16M32LFCM-6-L-IT-B.pdf>.
4. Existing Case-10 TCSR evidence used as the direct precursor for the authority question: [`10-micron-2005-2009-temperature-compensated-self-refresh-control-boundary.md`](10-micron-2005-2009-temperature-compensated-self-refresh-control-boundary.md).
5. Existing Case-09 refresh-address/cadence boundary: [`../cases/09-dram-cbr-refresh-address-internalization.md`](../cases/09-dram-cbr-refresh-address-internalization.md).
6. Existing Case-03 scheduled-restoration baseline: [`../cases/03-dram-refresh-as-scheduled-restoration.md`](../cases/03-dram-refresh-as-scheduled-restoration.md).
