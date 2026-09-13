# Evidence 10 Addendum — Micron 2005–2009 Temperature-Compensated Self-Refresh Control Boundary

## Status

**`bounded deepening complete`** — later LPDDR / Mobile DDR evidence for a materially different way of making refresh cadence condition-dependent: temperature-derived self-refresh scheduling, including both controller-programmed and on-die-sensor implementations.

This addendum does **not** claim that Micron's 2005–2009 TCSR implementation descends from the Hitachi/Toshiba/Sharp leakage-monitor patents in Case 10, does not reconstruct a complete JEDEC ballot history, and does not treat a standards-visible control field as proof that a particular product gives that field effective control authority.

---

## Purpose

Case 10 already grounds several direct leakage-derived self-refresh mechanisms:

- Hitachi's 1982-filed / 1984-published two-capacitor leakage-simulation comparator;
- Toshiba's 1984-priority preferred single-monitor-capacitor / threshold path;
- Sharp's 1997-priority / 1998-published array-coupled and substrate/back-bias-derived paths.

Those sources show that an internal physical condition can participate in deciding when refresh work occurs. They do not establish that later standards-era `temperature-compensated self refresh` is the same mechanism.

Micron's mobile-DRAM technical notes provide a bounded negative control. They expose a standards-era refresh policy in which **temperature** is the observed condition, and they explicitly distinguish two authority placements:

1. an on-board DRAM temperature sensor can adjust self-refresh interval automatically;
2. when no on-board sensor exists, the memory controller can use its own temperature sensor and program the appropriate DRAM control bits.

A later Micron note then documents a low-power DDR implementation in which an **on-die temperature sensor supersedes the externally programmable TCSR bits for effective interval control**: the JEDEC-standard TCSR bits are present in the register vocabulary but have no effect on that device.

The narrow research question is therefore:

> **Does a standard-visible maintenance control field necessarily identify the component that actually decides the maintenance cadence?**

For the Micron LPDDR witness inspected here, the answer is no.

---

## Source identity and chronology

### Micron TN-46-12

**Micron Technology, Inc., TN-46-12, _Mobile DRAM Power-Saving Features and Power Calculations_.**

The inspected manufacturer text is preserved in a third-party mirror:

- <https://dtsheet.com/doc/1384408/tn-46-12--mobile-dram-power-saving-features-calculations>

The document's own revision history states:

- **Rev. A — October 2005** — first draft;
- **Rev. B — May 2009** — limited equation/document cleanup.

Micron's current DRAM power-calculator page still lists `Mobile LPDRAM TN-46-12` among its related technical notes:

- <https://www.micron.com/sales-support/design-tools/dram-power-calculator>

The surviving mirror is therefore used for text access, while authorship and continuing document identity remain attributable to Micron. This is manufacturer-primary content accessed through a mirror, not a claim that the mirror publisher authored the engineering guidance.

### Micron TN-46-15

**Micron Technology, Inc., TN-46-15, _Low-Power Versus Standard DDR SDRAM_, Rev. A, 22 January 2007.**

Inspected surviving copy:

- <https://dtsheet.com/doc/1384279/tn4615--low-power-versus-standard-ddr-sdram>

The document identifies itself as `TN4615.fm - Rev. A 1/22/07 EN` and carries Micron's 2007 copyright.

A Freescale/NXP MPC5121e DRAM-controller design guide preserves the original Micron download location in its references:

- `http://download.micron.com/pdf/technotes/DDR/tn4615.pdf`
- surviving guide text: <https://manuals.plus/m/fd2a88e34742801074da475b621e1bec8a57e5b296ebe5e29d01ecf797b92919>

That same guide separately cites the JEDEC low-power-DDR specification family and, in its self-refresh section, directs implementers to JESD209 for Mobile-DDR behavior. This corroborates the standards-era context but is **not** used here as a substitute for direct inspection of a paid/controlled JEDEC normative clause.

### JEDEC-number chronology guardrail

A standards registry records that the first LPDDR specification was originally numbered **JESD79-4** from May 2006 to August 2007 and was corrected to **JESD209** on 17 September 2007:

- <https://standards.globalspec.com/std/1236521/jedec-jesd-209>

Because TN-46-15 is dated January 2007, this addendum does **not** retroactively assign its `JEDEC-standard TCSR bits` statement to a later JESD209 revision or invent a clause number. The bounded claim is only that Micron itself described those bits as JEDEC-standard in January 2007.

---

## Direct historical record

### H/P — Micron described TCSR as a JEDEC-member power-saving feature by 2005

TN-46-12 Rev. A dates to October 2005. Its opening power-management section says that Micron and other JEDEC members had defined three mobile-DRAM power-saving features:

- Temperature Compensated Self Refresh (TCSR);
- Partial Array Self Refresh (PASR);
- Deep Power-Down (DPD).

For TCSR, the note says that during normal self-refresh operation, power can be saved by adjusting internal self-refresh intervals to the ambient temperature of the DRAM component.

This is direct period evidence for `Temperature Compensated Self Refresh` vocabulary in Micron's standards-oriented mobile-DRAM documentation. It does not by itself establish the exact first JEDEC ballot, first implementation, or invention priority.

### H/P — TN-46-12 exposes two different control placements

TN-46-12 states that temperature compensation is accomplished using a temperature sensor, then gives two implementation/control cases.

If the temperature sensor is on the DRAM, the self-refresh intervals can be adjusted automatically according to temperature at intervals specified in the product datasheet.

If a particular DRAM does **not** have an on-board temperature sensor, the memory controller can use its own temperature sensor and program the appropriate control bits in the DRAM according to measured ambient temperature.

The historical record therefore directly supports:

```text
same named feature: TCSR
    can be exposed through

on-DRAM sensing + automatic interval adjustment

or

controller-side sensing + programmed DRAM control bits
```

The note does not say these are electrically identical implementations.

### H/P — temperature compensation changes refresh interval, not the underlying volatility class

TN-46-12 frames TCSR as a way to reduce self-refresh current by changing how often refresh occurs as temperature changes. Its example current-versus-temperature discussion shows lower self-refresh current at lower temperature and says TCSR and PASR can work together to reduce self-refresh current.

The payload remains DRAM state maintained by self refresh. Temperature compensation changes maintenance cadence; it does not make the array nonvolatile.

### H/P — TN-46-15 documents an on-die sensor with effective cadence authority

Micron's January 2007 TN-46-15 states that low-power DDR SDRAM uses an **on-chip temperature sensor** that controls the refresh interval based on device temperature.

It further states that programming the **JEDEC-standard TCSR bits will not have an effect on the device**. Instead, the on-chip self-refresh oscillator continues refreshing the array at a factory-optimized rate for the device temperature.

The note also says TCSR applies to **self refresh**, not to **auto refresh**.

This is an especially useful control-boundary witness because it separates three things that can otherwise be collapsed:

```text
standardized register field exists
    !=
field has effective control on this implementation
    !=
condition-to-refresh decision is external
```

### H/P — the extended-mode-register diagram preserves the inert-field boundary explicitly

TN-46-15's extended-mode-register figure labels TCSR bits in the low-power-DDR register map, but its note says:

> on-die temperature sensor is used in place of TCSR; setting these bits will have no effect.

The same register figure also exposes PASR controls that **do** select how much of the array is refreshed.

The historical document therefore places an effective spatial-retention control and an ineffective temporal-control field in the same extended-mode-register context.

That supports a bounded distinction:

```text
register visibility
    !=
effective policy authority
```

without requiring any speculation about undocumented internal implementation beyond Micron's own statements.

### H/P — higher temperature causes more frequent self-refresh in the documented LPDDR behavior

TN-46-15's self-refresh-current discussion says that, for a given PASR option, current rises with temperature and that at higher temperatures the array is refreshed more frequently.

This is direct evidence for the intended relation:

```text
device temperature
    ->
self-refresh cadence
    ->
self-refresh current / maintenance work
```

It does not establish a cell-by-cell temperature-retention transfer function.

---

## Engineering reconstruction

### E — temperature is a retention-relevant proxy, not a direct charge-decay measurement

The earlier Case-10 patents include designs that derive timing from electrical leakage or leakage-coupled physical behavior.

Micron's TCSR documents instead expose **temperature** as the measured condition.

A bounded reconstruction is:

```text
temperature condition
    ->
retention-risk / leakage-related policy estimate
    ->
selected self-refresh interval
    ->
refresh work
```

The middle relation is a product/policy relation rather than a direct observation of every payload cell's charge state.

Therefore:

```text
temperature-derived maintenance
    !=
direct leakage-state sensing
```

This is the central negative control added by the slice.

### E — sensor location and policy authority are separate design dimensions

TN-46-12 explicitly permits controller-side sensing plus programmed DRAM control fields as one TCSR route, while TN-46-15 documents a Micron implementation with an on-die sensor that makes the TCSR bits ineffective.

That yields a stronger decomposition:

```text
condition observed
    !=
sensor location
    !=
policy calculation location
    !=
control-field visibility
    !=
effective cadence authority
    !=
refresh execution location
```

A host-visible field may describe a standards-level control surface even when a particular device has moved the effective policy decision behind that interface.

### E — standards-visible state can be semantically inert on a conforming product path

TN-46-15 is especially important because the TCSR bits are not absent from the diagram. They remain named, but Micron tells the integrator that setting them has no effect because the on-die sensor has taken over the function.

Thus:

```text
control state representable
    !=
control state causally effective
```

For retention analysis, preserving a register value is not automatically enough to preserve the behavior one might infer from the register name.

This is an engineering reconstruction from Micron's documented interface behavior, not a claim about every JEDEC-compliant LPDDR device.

### E — temporal and spatial retention policies remain independent axes

TCSR adjusts **when** self-refresh maintenance occurs.

PASR adjusts **which portion of the array** is included in self refresh.

TN-46-15's register discussion makes the distinction unusually visible because PASR remains actively selectable while the TCSR bits are superseded by automatic on-die sensing.

The resulting relation is:

```text
maintenance cadence policy
    !=
maintenance coverage policy
```

and more specifically:

```text
automatic cadence control
    can coexist with
controller-selected retention coverage
```

This prevents a generic phrase such as `adaptive self refresh` from hiding two separate control problems.

### E — lowering refresh frequency is still active retention maintenance

At lower temperature the device can refresh less often and consume less self-refresh current. The preservation mechanism remains recurring restoration of dynamic state.

Therefore:

```text
less maintenance work
    !=
maintenance-free retention
```

and:

```text
condition-dependent interval
    !=
nonvolatile state
```

---

## Functional comparison to Hitachi / Toshiba / Sharp Case-10 mechanisms

This section is a **functional analogy / contrast**, not genealogy.

### Shared function

All of the compared mechanisms can be described at a high level as making refresh timing depend on a condition rather than exposing one fixed externally supplied cadence.

### Different observed condition

- Hitachi: simulated leakage represented by two capacitor voltages and comparator behavior;
- Toshiba: preferred monitor capacitor crossing a threshold, with the monitor allowed to be conservative relative to ordinary cells;
- Sharp: aggregate leakage demand on bit-line-precharge infrastructure or substrate/back-bias activity;
- Micron TCSR: device/ambient temperature used to select self-refresh interval.

Therefore:

```text
condition-derived refresh timing
    !=
one canonical condition sensor
```

### Different authority placement

The 1980s patent cases focus on internal circuit paths that decide when a refresh pass begins.

Micron TN-46-12 explicitly allows either DRAM-side or controller-side temperature sensing, while TN-46-15 documents an on-die implementation that leaves standards-visible TCSR bits ineffective.

Therefore:

```text
same named maintenance objective
    !=
same authority boundary
```

### No genealogy claim

Nothing inspected here proves:

- Hitachi's leakage comparator influenced Micron TCSR;
- Toshiba's 1984 patent led to the JEDEC TCSR field;
- Sharp's later array-coupled patent was incorporated into Micron LPDDR;
- the word `temperature-compensated` represents a renamed continuation of `leakage-tracked` self refresh.

Those would require proposal histories, standards ballots, inventor/assignee citation chains, or other actor-to-actor evidence not established in this slice.

---

## Historical / normative boundary

### What is directly grounded

- Micron used `Temperature Compensated Self Refresh (TCSR)` in Mobile DRAM documentation by October 2005.
- Micron said it and other JEDEC members had defined TCSR, PASR, and DPD as power-saving features.
- Micron documented both on-board automatic sensing and controller-sensor/programmed-bit TCSR control placements.
- Micron's January 2007 TN-46-15 called the TCSR fields `JEDEC-standard`.
- The same note documented a product behavior where those TCSR bits had no effect because an on-die sensor controlled refresh interval.

### What is not directly grounded here

The actual normative JEDEC text of the relevant 2005–2007 TCSR fields was not directly inspected in this slice.

A secondary standards registry provides useful numbering chronology for JESD79-4 → JESD209, but this addendum does not use that registry to invent normative bit semantics, mandatory/optional status, compliance language, or clause numbers.

The correct repository boundary is:

```text
manufacturer says "JEDEC-standard TCSR bits"
    !=
this slice has inspected the normative JEDEC clause
```

That remaining evidence debt is explicit rather than silently filled with later datasheets.

---

## Failure / forgetting boundaries

### Wrong temperature estimate is not the same failure as wrong leakage sentinel behavior

A controller-sensed TCSR implementation can be wrong because its temperature observation, mapping from temperature to programmed setting, or programming action is wrong.

An on-die automatic implementation can instead fail in the sensor, internal policy path, oscillator control, or refresh execution path.

The shared symptom may be a bad refresh cadence, but the fault boundaries differ.

### A preserved mode-register image does not guarantee preserved effective refresh policy

In the TN-46-15 implementation, preserving/reapplying the TCSR bit pattern would not reconstruct the active temperature-to-refresh decision because those bits do not control the device's TCSR behavior.

Thus:

```text
saved configuration bits
    !=
complete saved maintenance policy
```

when effective policy lives behind the interface.

This is a bounded interface lesson, not a claim about boot persistence of the specific Micron device's internal sensor state.

### PASR misconfiguration and TCSR misbehavior have different retention scopes

PASR can exclude portions of the array from self refresh; TN-46-15 explicitly warns that data is not retained in array portions not selected for refresh.

TCSR instead changes the maintenance interval for the retained region.

Therefore:

```text
wrong coverage
    !=
wrong cadence
```

Both can endanger retention, but they are not the same error class.

---

## Philosophical interpretation

The technical fact that creates the conceptual problem is narrow: a visible control representation can survive while the effective preservation decision occurs elsewhere.

A retained register field therefore need not exhaust the retained **policy relation** of the system. In the 2007 Micron witness, the meaningful maintenance behavior depends on an internal sensor-to-oscillator relation that the nominal TCSR bits no longer control.

This can support a cautious interpretation:

> technical retention sometimes depends not only on preserving state values, but on preserving or re-establishing the authority relation that makes some state causally effective.

The interpretation stops at the mechanism. It is not a claim that Micron or JEDEC engineers were formulating a philosophy of authority, representation, or institutional delegation.

---

## Explicit non-claims

This addendum does **not** claim that:

1. Micron invented TCSR;
2. October 2005 is the first public TCSR disclosure;
3. the inspected TN-46-12 mirror is itself a primary publisher;
4. every Mobile DDR / LPDDR device has an on-die temperature sensor;
5. every JEDEC-compliant device ignores the TCSR bits;
6. a JEDEC-standard field must be mandatory in every implementation;
7. the 2007 Micron product behavior is the normative meaning of JESD209;
8. the exact relevant JEDEC clause was inspected here;
9. temperature is a direct measurement of each DRAM cell's retained charge;
10. temperature alone determines every DRAM cell's retention time;
11. Micron TCSR is electrically identical to Hitachi, Toshiba, or Sharp leakage-monitor circuits;
12. the 1980s leakage-monitor patents caused or directly influenced JEDEC TCSR;
13. PASR and TCSR are one policy merely because they share an extended mode-register context;
14. lower self-refresh current means retention has become passive or nonvolatile;
15. an inert TCSR field means the whole extended mode register is inert;
16. preserving the external register image preserves all internal maintenance-control state;
17. a factory-optimized interval proves worst-cell coverage under every operating condition;
18. manufacturer technical-note behavior proves a named die revision's transistor-level implementation beyond the described functional boundary.

---

## Claim ledger

| Claim | Label | Evidence | Strength |
| --- | --- | --- | --- |
| Micron TN-46-12 Rev. A dates to October 2005 | H/P | document revision history | strong |
| Micron described TCSR, PASR, and DPD as power-saving features defined by Micron and other JEDEC members | H/P | TN-46-12 | strong |
| TN-46-12 allows on-DRAM automatic temperature sensing or controller-side sensing + programmed control bits | H/P | TN-46-12 | strong |
| Micron TN-46-15 Rev. A is dated 22 Jan 2007 | H/P | document footer | strong |
| TN-46-15 says an on-chip temperature sensor controls refresh interval | H/P | TN-46-15 | strong |
| TN-46-15 calls the TCSR fields JEDEC-standard | H/P | TN-46-15 | strong |
| The documented Micron implementation ignores programmed TCSR bits because on-die sensing controls cadence | H/P | TN-46-15 text + extended-mode-register note | strong |
| TCSR applies to self refresh rather than auto refresh in the TN-46-15 behavior | H/P | TN-46-15 | strong |
| Higher temperature causes more frequent self refresh in the documented behavior | H/P | TN-46-15 | strong |
| Sensor location, control-field visibility, and effective cadence authority are separate dimensions | E | bounded reconstruction across TN-46-12 / TN-46-15 | strong |
| Temperature-derived cadence is functionally equivalent to direct leakage sensing at circuit level | X | different observed condition and undocumented genealogy | rejected |
| A standards-visible field necessarily has effective control on every product | X | directly contradicted by TN-46-15 | rejected |
| The relevant JESD209 normative clause and mandatory/optional semantics are established here | X | normative standard text not directly inspected | open |

---

## Related repositories

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `TN-46-15` and `temperature compensated self refresh` found no dedicated treatment to reuse.

The broader history of LPDDR standardization, DRAM temperature sensing, oscillator design, standards ballots, and vendor competition belongs primarily in `computing-archaeology` if developed as a technical-history track.

This repository keeps the narrower retention comparison: **what condition is observed, where the maintenance policy is decided, what interface state is visible, and which state actually has authority over preservation work.**

---

## Remaining evidence debt

1. Directly inspect the relevant 2005–2007 JEDEC LPDDR normative text or ballot material and identify the exact TCSR field semantics without relying on manufacturer paraphrase.
2. Recover the proposal / ballot genealogy for TCSR to determine when temperature-conditioned self-refresh became a standardized interface and which actors proposed it.
3. Tie the TN-46-15 behavior to one or more named Micron part-number datasheets with revision dates and explicit TCSR-bit / on-die-sensor wording.
4. Add one independent contemporary vendor implementation that distinguishes automatic on-die TCSR from controller-programmed TCSR.
5. If a stronger safety claim is needed, locate characterization evidence connecting temperature bins to actual worst-cell retention coverage rather than inferring it from power-management documentation.
6. Keep later LPDDR2/3/4 temperature-status and refresh-policy mechanisms separate unless their normative semantics are directly inspected.

---

## Sources

1. Micron Technology, Inc., **TN-46-12: _Mobile DRAM Power-Saving Features and Power Calculations_**, Rev. A Oct. 2005 / Rev. B May 2009, inspected manufacturer text preserved at: <https://dtsheet.com/doc/1384408/tn-46-12--mobile-dram-power-saving-features-calculations>.
2. Micron Technology, Inc., **TN-46-15: _Low-Power Versus Standard DDR SDRAM_**, Rev. A, 22 Jan. 2007, inspected manufacturer text preserved at: <https://dtsheet.com/doc/1384279/tn4615--low-power-versus-standard-ddr-sdram>.
3. Micron Technology, **DRAM power calculators**, current support page listing `Mobile LPDRAM TN-46-12` under related technical notes: <https://www.micron.com/sales-support/design-tools/dram-power-calculator>.
4. Freescale Semiconductor, **_MPC5121e DRAM Controller_**, Rev. 2 (2009), surviving copy preserving Micron TN-46-15's legacy original URL and separately referencing JESD209 for Mobile-DDR self-refresh behavior: <https://manuals.plus/m/fd2a88e34742801074da475b621e1bec8a57e5b296ebe5e29d01ecf797b92919>.
5. GlobalSpec standards record, **JEDEC JESD209 — Low Power Double Data Rate (LPDDR) SDRAM Standard**, used only for numbering/publication chronology, not normative TCSR semantics: <https://standards.globalspec.com/std/1236521/jedec-jesd-209>.
