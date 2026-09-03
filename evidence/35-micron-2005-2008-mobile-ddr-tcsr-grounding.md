# Grounding Record — Micron 2005–2008 Mobile DDR Automatic TCSR

## Status

**`grounded`** for the bounded retention claim in Case 35: a documented Micron Mobile DDR product combines internally clocked self refresh with automatic on-die temperature control of the self-refresh oscillator, while separately exposing controller-selectable partial-array retention and a deep-power-down mode that abandons array payload.

Case: [`../cases/35-micron-mobile-ddr-automatic-tcsr.md`](../cases/35-micron-mobile-ddr-automatic-tcsr.md).

This record deliberately separates three evidence layers:

1. **manufacturer product contract** — Micron's 512Mb Mobile SDRAM Rev. J 2/08 datasheet is the central primary source;
2. **manufacturer technical context** — TN-46-12 Rev. A 10/05 explains TCSR/PASR/DPD and distinguishes on-device automatic temperature sensing from controller-programmed TCSR;
3. **cross-case reconstruction** — Cases 21 and 34 supply earlier bounded comparisons for self-refresh responsibility and temperature-conditioned cadence. They are not used to overwrite the product's own vocabulary.

## Primary source A — Micron 512Mb Mobile SDRAM Rev. J 2/08

### Identity

- **Title:** `512Mb: 32 Meg x 16, 16 Meg x 32 Mobile SDRAM`
- **Families named:** `MT48H32M16LF`; `MT48H16M32LF/LG`
- **Document marker:** `MT48H32M16LF_1.fm - Rev. J 2/08 EN`
- **Copyright line:** ©2005 Micron Technology, Inc.
- **Public PDF mirror:** <https://media.digikey.com/pdf/Data%20Sheets/Micron%20Technology%20Inc%20PDFs/MT48H(16,32)MxxL(F,G).pdf>

The mirror preserves the Micron-branded manufacturer PDF, page headers, revision marker, and document/source identifiers. Claims below are tied to locations in that document rather than inferred from distributor catalog metadata.

### Feature-list anchors — PDF p. 1

The product feature list directly names:

- `Auto refresh and self refresh modes`;
- `On-chip temperature sensor to control refresh rate`;
- `Partial-array self refresh (PASR)`;
- `Deep power-down (DPD)`.

This anchors the case in a named product family rather than a patent-only disclosure.

### Extended Mode Register / TCSR / PASR — PDF p. 17 (viewer page 16)

The EMR section says the mobile-device power-reduction functions include TCSR control, PASR, and output drive strength.

Figure 8 retains fields labelled `TCSR` and `PASR`, but its note says:

- an **on-die temperature sensor is used in place of TCSR**;
- setting the TCSR bits has no effect.

The prose under `Temperature-Compensated Self Refresh (TCSR)` then states that, on this Mobile DDR SDRAM version:

- a temperature sensor is implemented for automatic control of the self-refresh oscillator;
- programming the TCSR bits has no effect;
- the self-refresh oscillator continues refreshing at the factory-programmed rate appropriate to device temperature.

This is the direct source for the case's strongest interface counterexample:

> A historically named register field can remain visible in the interface description while having no effective software-control semantics on the bounded product version.

### PASR coverage — PDF pp. 17–18

The PASR section says the controller can select the amount of memory refreshed during self refresh. The documented choices include all four banks, two banks, one bank, half a bank, and a quarter bank; the EMR figure also shows fractional-array encodings.

The next page explicitly says that normal READ/WRITE commands may address any bank during ordinary operation, but only the PASR-selected banks or bank segments are refreshed during self refresh, and data in unused banks or portions of banks will be lost.

This grounds the separation between:

- **cadence selection** — automatic on-die temperature/sensor/oscillator relation;
- **retention coverage selection** — controller-programmed PASR relation.

### AUTO REFRESH and SELF REFRESH — PDF p. 21 (viewer page 20)

The command description says:

- normal AUTO REFRESH is nonpersistent and must be issued each time refresh is required;
- the 512Mb SDRAM requires 8,192 AUTO REFRESH cycles every 64 ms under the ordinary specified regime;
- SELF REFRESH can retain data even if the rest of the system is powered down;
- in SELF REFRESH, the device retains data without external clocking;
- after entry, the SDRAM provides its own internal clocking and performs its own refresh cycles;
- it may remain in self refresh indefinitely beyond the minimum entry interval under the documented operating contract.

This is direct product evidence for:

> `no external clock` does not mean `no recurring retention work`.

The temperature-conditioned oscillator claim from the EMR section can therefore be joined to an independently documented self-refresh authority relation without conflating the two.

### Ordinary power-down is not self refresh — PDF pp. 34–35

The ordinary power-down section says no refresh operations are performed in that mode and therefore the device may not remain there longer than the 64 ms refresh period.

This supplies a useful negative boundary: low-power state alone does not imply a retention-maintenance mechanism. SELF REFRESH and ordinary power-down have different preservation semantics.

### Deep Power-Down — PDF pp. 35–36 (viewer pages 34–35)

The Deep Power-Down section says DPD maximizes power savings by shutting off power to the entire memory array and explicitly says array data **will not be retained** once DPD is executed.

The DPD exit procedure then separately states that the **mode register and extended mode register values are retained upon exiting deep power-down**.

This is direct evidence for:

> **array-payload retention ≠ documented control-state retention**.

The source does not identify the physical storage mechanism used to preserve those register values through DPD; this record therefore does not speculate about it.

## Primary source B — Micron TN-46-12 Rev. A 10/05

### Identity and bounded use

- **Title:** `TN-46-12: Mobile DRAM Power-Saving Features/Calculations`
- **Revision:** `Rev. A, 10/05 EN`
- **Copyright:** ©2005 Micron Technology, Inc.
- **Public archival mirror:** <https://notes-application.abcelectronique.com/024/24-19986.pdf>

The note says Micron and other JEDEC members had defined several mobile-DRAM power-saving features, including TCSR, PASR, and DPD.

For TCSR, it describes a general manufacturer-period design space:

- if the temperature sensor is on the DRAM, self-refresh intervals can be automatically adjusted for temperature;
- if the device lacks an on-board sensor, the memory controller can use its own temperature sensor and program the appropriate device control bits.

For PASR, it says refresh can be limited to the portion of memory in which data need to be preserved. For DPD, it describes the case where actual DRAM data retention is not required and array circuitry can be powered down more aggressively.

### Evidence boundary

This technical note is useful for **historical terminology and implementation-locus context**, but it is not substituted for an inspected JEDEC normative standard. Safe wording is:

> In 2005 Micron described TCSR, PASR, and DPD as mobile-DRAM power-saving features discussed by Micron and other JEDEC members, and described both on-device automatic and controller-programmed TCSR implementations.

Unsafe wording would be:

> `TN-46-12 proves the complete JEDEC TCSR standard genealogy.`

That broader standards-history claim remains open.

## Claim-to-source matrix

| Claim | Source | Strength / limit |
| --- | --- | --- |
| The Rev. J 2/08 Micron 512Mb Mobile SDRAM lists on-chip temperature-controlled refresh, PASR, and DPD | product datasheet p. 1 | direct manufacturer product record |
| An on-die sensor automatically controls the self-refresh oscillator | product datasheet p. 17 | direct mechanism/interface statement |
| Programming the displayed TCSR bits has no effect on this version | product datasheet Figure 8 + TCSR prose | direct negative interface semantics |
| SELF REFRESH uses internal clocking and performs its own refresh without external clocking | product datasheet p. 21 | direct command semantics |
| PASR makes retention coverage controller-selectable | product datasheet pp. 17–18 | direct product semantics |
| Data outside the PASR-selected region are lost in self refresh | product datasheet p. 18 | direct warning |
| DPD does not retain array payload | product datasheet p. 35 | direct product semantics |
| Mode-register and EMR values are retained after exiting DPD | product datasheet p. 36 | direct product semantics; physical mechanism unspecified |
| Micron documented on-device versus controller-sensor TCSR implementations in 2005 | TN-46-12 Rev. A 10/05 | manufacturer technical context |
| The on-die sensor measures each row's exact retention margin | none | **unsupported / rejected** |
| Visible TCSR bits imply host cadence authority | product datasheet directly says the opposite | **rejected** |
| This source set establishes the full JEDEC revision chronology | none | **unsupported / rejected** |

## Engineering reconstruction enabled by the evidence

### 1. Field presence versus effective authority

The TCSR-labelled EMR positions and the explicit `no effect` statement permit a precise methodological distinction:

> **register-field presence ≠ effective software authority**.

Interface archaeology must inspect product-version semantics, not infer function from field labels alone.

### 2. Cadence authority versus coverage authority

Automatic temperature control changes *when* self-refresh work recurs. PASR changes *which* array state receives that work. The two controls coexist in one product but have different authorities and failure consequences.

### 3. Self-refresh authority versus environmental condition

Internal clocking establishes where recurring maintenance originates during SELF REFRESH. The on-die sensor establishes one condition used to modulate that internal maintenance. Their co-location is a historical implementation fact; their analytical roles remain distinct.

### 4. Retention mode versus retention entitlement

PASR makes continued preservation selective. A location can be fully valid and addressable during ordinary operation, then become deliberately outside the retained set during a subsequent self-refresh interval.

### 5. Payload state versus control state

DPD supplies a bounded counterexample to treating a device as one homogeneous retained-state domain: the array payload is explicitly abandoned while mode/extended-mode-register values are documented to survive exit.

### 6. Energy reduction versus forgetting mode

TCSR, PASR, and DPD reduce power through different retention transformations:

```text
TCSR
    reduce maintenance frequency under cooler conditions

PASR
    reduce the amount of state receiving maintenance

DPD
    stop preserving the array payload
```

They should not be flattened into one `low power = weaker refresh` story.

## Prior art and anti-anachronism

Case 34 already establishes that temperature-conditioned DRAM refresh predates this product and even predates Micron's 1991 patent through a 1987-priority CardioData family. This product therefore is not used for invention priority.

Likewise, `retention coverage authority`, `selective retention`, and `control-state retention` are project reconstruction terms. Historical claims use the product's own `TCSR`, `PASR`, `SELF REFRESH`, `DPD`, and `self refresh oscillator` vocabulary.

## Related-repository check

Current GitHub code searches of `tmzncty/computing-archaeology` for `temperature compensated self refresh`, `TCSR`, and mobile/LPDDR refresh returned no dedicated case to reuse. A comprehensive standards/device genealogy should go there if pursued broadly; this evidence record remains bounded to the retention-specific product semantics.

## Remaining gaps

This record does **not** close:

- revision-by-revision JEDEC TCSR / PASR standards genealogy;
- exact relationship between this product and later naming as LPDDR;
- sensor placement/calibration and thermal-gradient fault qualification;
- exact physical implementation retaining MR/EMR values through DPD;
- later LPDDR temperature-sensor status / thermal-offset semantics;
- per-row retention-time profiling and retention-aware refresh;
- RowHammer-oriented refresh policy;
- empirical power/fault testing of this exact device.

Those are separate bounded slices rather than reasons to enlarge Case 35.
