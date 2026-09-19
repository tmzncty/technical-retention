# Evidence 10 Addendum — Samsung / Infineon 2004 TCSR Control-Authority Product Boundary

## Status

**`bounded deepening complete`** — named-product manufacturer documentation from February 2004 showing two materially different implementations of temperature-compensated self refresh (TCSR): an Infineon Mobile-RAM in which the visible TCSR field can select between automatic on-chip temperature sensing and fixed programmed temperature values, and a Samsung Mobile-SDRAM in which internal temperature sensing controls self-refresh cadence while an externally issued TCSR setting is explicitly ignored.

This addendum does **not** establish the first TCSR product, does not inspect or reconstruct the controlling JEDEC normative clause, does not claim that Samsung and Infineon implemented the same standard revision or circuit, and does not connect either product genealogically to the earlier Hitachi / Toshiba / Sharp leakage-derived self-refresh disclosures in Case 10.

---

## Purpose

Case 10 already establishes several layers that can otherwise be collapsed:

```text
payload retention constraint
    !=
condition sensing
    !=
maintenance-policy decision
    !=
visible control field
    !=
effective cadence authority
    !=
retained spatial coverage
    !=
refresh execution
```

The existing Micron 2005–2009 deepening supplied a particularly useful later witness: a standards-visible TCSR field can remain present while an on-die temperature sensor owns the effective self-refresh cadence and the field has no effect.

That left a chronology and comparison question:

> **Can product documentation from the same earlier Mobile-SDRAM era show that the visible TCSR field did not have one universal authority semantics?**

The answer is yes, within a bounded February-2004 comparison.

Infineon's `HYB25L512160AC-7.5 / HYE25L512160AC-7.5` 512 Mbit Mobile-RAM exposes TCSR in the Extended Mode Register. Its default `TCSR = 00` leaves an on-chip temperature sensor enabled; the other TCSR values select defined temperatures and disable that sensor.

Samsung's `K4M56323LE` 256 Mbit Mobile-SDRAM instead documents `Internal TCSR`, says internal sensor/control units automatically control the self-refresh cycle according to temperature ranges, and says an externally issued TCSR EMRS code is ignored. Its Extended Mode Register still exposes PASR coverage and driver-strength controls.

The bounded result is not simply `both have TCSR`. It is:

```text
same broad feature label
    !=
same visible-field semantics
    !=
same effective cadence authority
```

and, within the Infineon device itself:

```text
TCSR field effective
    !=
on-chip sensor necessarily active
```

---

## Sources inspected

### Infineon — February 2004

**Infineon Technologies AG, _HYB25L512160AC-7.5 / HYE25L512160AC-7.5, 512MBit Mobile-RAM_, Data Sheet Rev. 1.2, February 2004.**

Page-preserving PDF inspected at:

- <https://docs.ampnuts.ru/eevblog.docs/_Datasheets/RAM.SDRAM/Mobile/1-HYB25L512160AC_Rev.1.2.pdf>

The document itself identifies:

- the two device families;
- `512MBit Mobile-RAM`;
- `Data Sheet, Rev. 1.2, Feb. 2004`;
- `Edition 2004-02`;
- Infineon Technologies AG as publisher.

Relevant direct text occurs in the functional-description pages for the Extended Mode Register, PASR, and `Temperature Compensated Self Refresh (TCSR) with On-Chip Temperature Sensor`.

A later Rev. 1.3 April-2004 copy was also used only as text-level corroboration for the same TCSR description:

- <https://datasheet4u.com/pdf-down/H/Y/B/HYB25L512160AC-7.5-Infineon.pdf>

The February-2004 Rev. 1.2 PDF is the chronology anchor for this slice.

The web PDF renderer exposed page-preserving extracted text but failed to return screenshots because of a cache error. No claim in this addendum depends on diagram geometry, visual color, or any feature visible only in an image; all quoted semantics below are present in the extracted manufacturer text.

### Samsung — February 2004

**Samsung Semiconductor, _K4M56323LE - M(E)E/N/S/C/L/R, 2M × 32Bit × 4 Banks Mobile-SDRAM_, February 2004.**

Inspected preserved manufacturer-datasheet text:

- <https://dtsheet.com/doc/304110/samsung-k4m56323le-en80>

The surviving text identifies the family, organization, `Mobile-SDRAM`, February-2004 date, PASR support, and `Internal TCSR (Temperature Compensated Self Refresh)`.

The same preserved document states that Samsung's internal temperature sensor and control units automatically control the self-refresh cycle according to temperature ranges and that an EMRS code for external TCSR is ignored.

A later Samsung Mobile-SDRAM family supplies a same-manufacturer continuity check, not a separate chronology claim:

- Samsung `K4S56163PF`, September 2004, preserved manufacturer-datasheet text: <https://manualmachine.com/datasheet/k4s56163pf/8448986-datasheet-samsung/>.

It repeats the internal-sensor / ignored-external-TCSR relation while exposing PASR as a separate spatial-retention control.

### Source-status note

Both are manufacturer-primary technical documents accessed through surviving third-party mirrors. The mirrors are not treated as the authors of the engineering claims. The bounded claims are attributed to the manufacturer text itself.

No JEDEC normative document is substituted by these product sheets.

---

## Direct historical record

### H/P — Infineon Rev. 1.2 is a February-2004 named-product witness

The Infineon document identifies the `HYB25L512160AC-7.5` and `HYE25L512160AC-7.5` families as 512 Mbit Mobile-RAM and dates itself `Rev. 1.2, Feb. 2004` / `Edition 2004-02`.

This gives the repository a named product-family document rather than only a patent or later technical note.

It does **not** establish first shipment, first commercial availability, first TCSR implementation, or first standards adoption.

### H/P — Infineon's Extended Mode Register separates TCSR and PASR fields

The Infineon functional description says that the Extended Mode Register controls low-power features including PASR and TCSR and retains its stored information until it is programmed again or the device loses power.

The bit assignment is explicit:

```text
A4:A3 -> TCSR
A2:A0 -> PASR
```

The listed TCSR values are:

```text
00 -> 70 °C
01 -> 45 °C
10 -> 15 °C
11 -> 85 °C
```

The PASR field separately selects how much of the array participates in self refresh.

This is direct product evidence that temporal maintenance policy and spatial retention coverage are represented by distinct controls.

### H/P — Infineon's default TCSR state enables the on-chip sensor

The section title itself is `Temperature Compensated Self Refresh (TCSR) with On-Chip Temperature Sensor`.

The text says that DRAM refresh requirement depends strongly on die temperature, with high temperature requiring a shorter refresh period and low temperature allowing a longer one.

It then says the Mobile-RAM contains an on-chip temperature sensor that continuously monitors current die temperature and adjusts the self-refresh period accordingly.

Most importantly for this slice:

```text
TCSR = 00
    -> on-chip temperature sensor enabled by default
```

### H/P — Infineon's nondefault TCSR values disable the sensor

The same paragraph states that the other three TCSR settings use defined temperature values to adjust the self-refresh period **with the on-chip temperature sensor disabled**.

Therefore, for this named product:

```text
visible TCSR field
    can select

automatic sensor-derived cadence

or

programmed fixed-temperature policy with sensor disabled
```

This directly blocks the shortcut:

```text
TCSR field effective
    -> on-chip sensor must be active
```

The field can be causally effective precisely by replacing the sensor-derived policy with a programmed temperature assumption.

### H/P — Infineon PASR changes retention coverage, not merely power accounting

Infineon describes PASR as restricting self refresh to variable portions of the total array.

The document explicitly says data written to non-activated memory sections will be lost after a period defined by `tREF`.

Thus the spatial policy is retention-significant:

```text
excluded from self-refresh coverage
    -> no documented retention obligation for that region
    -> data eventually lost after the relevant refresh period
```

This is not evidence of immediate physical erasure or sanitization.

### H/P — Infineon distinguishes AUTO REFRESH from SELF REFRESH at the command/mode boundary

The command description says AUTO REFRESH and SELF REFRESH share the command encoding while CKE distinguishes the two cases; an internal refresh counter controls row and bank addressing.

This supports a bounded control decomposition:

```text
mode / command entry
    !=
row-bank enumeration
    !=
TCSR cadence policy
    !=
PASR coverage policy
```

It does not reveal the complete internal temperature-to-oscillator circuit.

### H/P — Samsung K4M56323LE is independently dated February 2004

Samsung's `K4M56323LE` document identifies a 2M × 32-bit × 4-bank Mobile-SDRAM family and is dated February 2004.

Its feature list includes:

- PASR;
- `Internal TCSR (Temperature Compensated Self Refresh)`;
- Auto Refresh;
- a 64 ms / 4K-cycle refresh period.

This is a second named product-family witness in the same month/year chronology used here.

### H/P — Samsung documents internal sensing as the effective TCSR path

The Samsung text says that, to save power, the Mobile-DRAM includes internal temperature-sensor and control units that control the self-refresh cycle automatically according to two temperature ranges.

For the documented commercial / extended options, the self-refresh-current table distinguishes a lower-temperature range and a maximum 70/85 °C range.

The important retention fact is not the exact current number. It is the authority statement:

```text
internal temperature sensor + control units
    -> automatic self-refresh-cycle control
```

### H/P — Samsung explicitly says external TCSR EMRS code is ignored

The Samsung document states that if the controller issues EMRS for external TCSR, the TCSR code is ignored.

That is unusually direct interface evidence:

```text
externally representable / issuable TCSR request
    !=
effective cadence authority on this product
```

The document's ordinary Extended Mode Register path is instead used for controls such as PASR and driver strength.

### H/P — Samsung PASR remains a separate effective spatial control

Samsung documents PASR choices for 4 banks, 2 banks, or 1 bank on the `K4M56323LE` family.

So this product places effective temporal and spatial retention policy differently:

```text
self-refresh cadence
    -> internal temperature-sensor/control path

retained array coverage
    -> externally selectable PASR
```

The field that lacks temporal authority does not imply that the whole low-power register interface is inert.

### H/P — September-2004 Samsung family repeats the same boundary

The Samsung `K4S56163PF` September-2004 manufacturer text independently repeats:

- internal temperature sensor and control units automatically control self-refresh cycle;
- external TCSR EMRS is ignored;
- PASR remains configurable as full, half, or quarter array.

This is used only as a same-manufacturer continuity witness for the documented control split. It is not used to claim one unchanged die, firmware, circuit, or exact register implementation across Samsung families.

---

## Chronology result

Before this addendum, Case 10's standards-era named control-boundary discussion was anchored mainly by Micron's October-2005 and January-2007 technical notes.

The bounded product-document floor for **cross-vendor divergence in TCSR authority semantics** can now be placed at least as early as **February 2004** for the inspected named product families:

```text
February 2004 — Infineon HYB/HYE25L512160AC Rev. 1.2
    TCSR field exposed and effective
    default code -> on-chip sensor active
    other codes -> defined temperature policy, sensor disabled
    PASR separately controls spatial coverage

February 2004 — Samsung K4M56323LE
    internal temperature sensor/control owns cadence
    controller-issued external TCSR code -> ignored
    PASR separately controls spatial coverage

October 2005 — Micron TN-46-12
    describes both DRAM-side automatic and controller-sensed/programmed TCSR placements

January 2007 — Micron TN-46-15
    on-chip sensor controls cadence
    JEDEC-standard TCSR bits documented as ineffective on that device
```

This chronology is a public-document floor for the inspected evidence set, not an invention or shipment-priority claim.

---

## Engineering reconstruction

### E — same feature name does not determine the authority graph

The broad feature label `TCSR` does not tell us which component has final control over self-refresh cadence.

The two February-2004 product documents support at least these two graphs:

```text
Infineon:
external TCSR field
    -> choose automatic on-chip sensor
       OR choose programmed fixed-temperature policy
    -> self-refresh cadence

Samsung:
internal sensor/control path
    -> self-refresh cadence

external TCSR request
    -> ignored
```

Therefore:

```text
same broad feature label
    !=
same control topology
```

### E — field visibility, field effectiveness, and sensor activity are three different questions

Across the two products:

```text
field visible / issuable?
field causally effective?
sensor active under current field value?
```

must be answered separately.

Infineon shows an effective field that can disable the sensor.

Samsung shows an external TCSR request that is documented as ineffective because cadence authority remains internal.

So neither of these shortcuts survives:

```text
visible field -> effective field

effective TCSR field -> active temperature sensor
```

### E — control authority can be state-dependent within one product

Infineon's default code and nondefault codes change **who/what supplies the temperature assumption used for cadence selection**.

A useful modern reconstruction is:

```text
TCSR = 00
    -> observed die temperature participates dynamically

TCSR != 00
    -> programmed temperature class substitutes for sensor observation
```

This is not Infineon's historical wording for `authority switching`; it is a reconstruction of the documented behavior.

### E — cadence policy and coverage policy are orthogonal retention dimensions

Both product families expose PASR separately from TCSR behavior.

That permits the retention relation to be represented as at least two axes:

```text
when must retained rows be refreshed?
    -> cadence / TCSR policy

which rows or banks are required to remain retained?
    -> PASR coverage policy
```

The same device can therefore have automatic temporal maintenance while retaining externally selected spatial scope.

### E — policy-state retention is not payload retention

Infineon says the Extended Mode Register holds its programmed state until reprogrammed or power is lost.

That register state can determine preservation behavior while powered, but it is not the payload being preserved.

Thus:

```text
retained maintenance-policy state
    !=
retained user payload
```

and:

```text
loss of policy state at power loss
    !=
proof about the analog remanence of individual DRAM cells
```

The device is volatile DRAM; this addendum does not turn register-reset semantics into a cold-remanence experiment.

### E — an ignored field is still historically informative

A field or command path that is documented as ignored is not `nothing` for retention analysis.

It establishes a boundary between:

```text
interface vocabulary
    and
effective preservation mechanism
```

That boundary matters for restart reconstruction, firmware assumptions, controller interoperability, and any historical claim that infers behavior from a register name alone.

---

## Functional comparison to the earlier Case-10 mechanisms

This section is **functional comparison only**.

### Hitachi 1982-filed / 1984-published

Hitachi's inspected patent uses a two-capacitor leakage-simulation and comparator relation to derive self-refresh behavior.

### Toshiba 1984-priority

Toshiba's preferred patent embodiment uses a monitor capacitor and threshold relation, with the monitor allowed to be conservative relative to ordinary cells.

### Sharp 1997–1998

Sharp discloses materially different leakage-related proxy topologies, including array-coupled leakage demand and substrate/back-bias-related activity.

### Samsung / Infineon 2004

The present product witnesses use temperature as the documented policy condition and expose different authority relations between external control and on-chip sensing.

### Micron 2005–2009

Micron's later notes explicitly discuss both controller-side and on-die sensing placements and document one product path in which nominal TCSR fields do not control cadence.

The useful comparison is:

```text
condition-derived maintenance
    can vary in

observed condition
sensor location
proxy population
control-field visibility
control-field effect
policy-decision location
cadence authority
coverage authority
```

There is no historical claim here that one manufacturer copied or inherited the mechanism of another.

---

## Standards / terminology boundary

The product documents use `Temperature Compensated Self Refresh` / `TCSR` in 2004.

That fact supports a terminology floor for these named manufacturer documents.

It does **not** establish:

- the first use of the term;
- the first JEDEC proposal;
- the exact normative definition of the relevant field;
- whether the field was mandatory, optional, reserved, or vendor-overridden in one specific standards revision;
- the precise compliance theory under which Samsung could ignore an externally issued TCSR code;
- whether Infineon and Samsung cite the same exact normative register layout.

The rule for the repository remains:

```text
manufacturer product vocabulary
    !=
directly inspected normative standards text
```

and:

```text
same label in two products
    !=
proven identical normative semantics
```

A direct JEDEC clause inspection remains separate work.

---

## Failure and forgetting boundaries

### Wrong cadence and wrong coverage remain different failures

A bad temperature-derived cadence can cause insufficient or excessive temporal maintenance of the selected region.

A bad PASR setting can exclude the wrong spatial region from maintenance.

Therefore:

```text
wrong cadence
    !=
wrong coverage
```

### Wrong programmed temperature and bad temperature sensing are different fault paths

For Infineon's documented behavior:

```text
sensor-enabled default
    -> sensor / policy path matters

fixed-temperature TCSR code
    -> programmed assumption matters
    -> sensor is disabled
```

A fault in the sensor is therefore not equivalent to an incorrect programmed fixed-temperature code.

### Ignored external control and stale external control are different problems

For Samsung, a controller that assumes its external TCSR code determines cadence is wrong even if the code value is perfectly preserved and replayed.

This gives a bounded relation:

```text
configuration state retained correctly
    !=
configuration state has the authority software assumes
```

### PASR exclusion is not sanitization

Infineon says data in non-activated regions is lost after the relevant refresh period, and Samsung similarly uses PASR to reduce retained scope.

Neither statement proves secure erasure, immediate clearing, zero analog remanence, or forensic non-recoverability.

Therefore:

```text
no longer maintained for logical retention
    !=
securely sanitized
```

---

## Philosophical interpretation

The technical fact that creates the conceptual issue is precise: a control representation can name a preservation policy without uniquely locating the effective preservation authority.

The Samsung witness is the strongest form: the external TCSR request can be present at the interface while the product documentation says the internal sensor/control path decides cadence instead.

Infineon adds the inverse complication: the visible TCSR field is effective, but one setting delegates policy to an on-chip sensor while other settings disable that sensor and substitute a programmed temperature assumption.

A cautious interpretation is therefore:

> **availability of a policy representation is not identical to possession of policy authority; authority can be delegated, overridden, or switched by state while the interface vocabulary remains stable.**

This is a philosophical interpretation of the engineering relation. It is not attributed to Samsung or Infineon engineers as their own conceptual vocabulary.

---

## Explicit non-claims

This addendum does **not** claim that:

1. February 2004 is the first historical appearance of TCSR.
2. Either Samsung or Infineon invented TCSR.
3. The two devices implement the same JEDEC revision.
4. The relevant JEDEC normative clause has been directly inspected here.
5. Samsung's ignored TCSR request was required by JEDEC to be ignored.
6. Infineon's TCSR encodings are universal across Mobile SDRAM / LPDDR.
7. Samsung's two temperature ranges are universal across its later products.
8. Infineon and Samsung use the same temperature-sensor circuit.
9. The exact sensor transistor / diode / bandgap / leakage structure is known from these documents.
10. The exact mapping from sensed temperature to refresh oscillator timing is reconstructed.
11. A programmed TCSR temperature is a direct measurement of cell retention.
12. TCSR eliminates periodic refresh.
13. TCSR makes DRAM nonvolatile.
14. PASR physically erases excluded regions immediately.
15. PASR is a secure-sanitization mechanism.
16. The 2004 products descend from the Hitachi, Toshiba, or Sharp patents already in Case 10.
17. Samsung influenced Infineon, or Infineon influenced Samsung.
18. A shared feature name proves shared circuit genealogy.
19. A surviving register value proves that the effective maintenance policy has been reconstructed.
20. Product documentation alone proves shipping volume, deployment prevalence, thermal-validation quality, or measured retention-failure rates.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Infineon Rev. 1.2 identifies HYB25L512160AC/HYE25L512160AC 512Mbit Mobile-RAM and is dated Feb. 2004 | H/P | directly inspected manufacturer PDF text |
| Infineon A4:A3 encode TCSR and A2:A0 encode PASR in the Extended Mode Register | H/P | Rev. 1.2 functional description |
| Infineon `TCSR=00` enables the on-chip temperature sensor by default | H/P | Rev. 1.2 §3.2.2.2 |
| Infineon's other TCSR settings use defined temperature values while disabling the on-chip sensor | H/P | Rev. 1.2 §3.2.2.2 |
| Infineon PASR excludes regions from self-refresh maintenance and says data there will be lost after `tREF` | H/P | Rev. 1.2 §3.2.2.1 |
| Infineon Extended Mode Register state is retained until reprogramming or device power loss | H/P | Rev. 1.2 §3.2.2 |
| Samsung K4M56323LE is a Feb.-2004 Mobile-SDRAM family with PASR and Internal TCSR | H/P | preserved Samsung manufacturer datasheet text |
| Samsung says internal temperature sensor/control units automatically control self-refresh cycle | H/P | K4M56323LE TCSR section |
| Samsung says controller-issued external TCSR EMRS code is ignored | H/P | K4M56323LE TCSR section |
| Samsung keeps PASR as a separately selectable retention-coverage control | H/P | K4M56323LE PASR section |
| A Sept.-2004 Samsung family repeats internal-TCSR / ignored-external-TCSR semantics | H/P | K4S56163PF manufacturer text; continuity witness only |
| Same `TCSR` label implies the same field semantics and authority topology across products | X | contradicted by Samsung/Infineon comparison |
| An effective TCSR field necessarily means an on-chip temperature sensor is active | X | contradicted by Infineon nondefault TCSR settings |
| A visible/issuable TCSR request necessarily has effective cadence authority | X | contradicted by Samsung |
| TCSR cadence authority and PASR coverage authority are separable | E | bounded reconstruction from both product documents |
| Maintenance-policy state and retained payload are distinct technical states | E | bounded reconstruction from Infineon register/payload semantics |
| The exact normative JEDEC TCSR clause is established by this addendum | X | normative standard not directly inspected |
| February 2004 is first invention / first shipment of TCSR | X | not established |

---

## Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `TCSR Mobile SDRAM` found no dedicated packet to reuse.

This addendum therefore keeps only the retention-specific seam:

```text
condition observation
    -> maintenance-policy selection
    -> visible / hidden control authority
    -> recurring refresh cadence
    -> retained spatial scope
```

Broader Samsung / Infineon Mobile-SDRAM product genealogy, JEDEC ballot history, temperature-sensor circuit history, mobile-memory market adoption, package/process evolution, and controller interoperability belong primarily in `computing-archaeology` rather than being duplicated here.

`tmzncty/problem-history` remains the methodological guard against turning the modern project terms `authority`, `policy state`, or `control topology` into period actor vocabulary.

---

## Remaining evidence debt

1. Directly inspect the relevant 2003–2005 JEDEC Mobile-SDRAM / Mobile-DDR normative TCSR clauses and revision chronology.
2. Establish whether an earlier named commercial product documents the same authority split before February 2004.
3. Recover official Samsung-hosted archival copies if available rather than relying on preserved manufacturer-datasheet mirrors.
4. Recover an official Infineon archive URL if available; the inspected PDF itself is manufacturer-authored but currently accessed through an archival mirror.
5. If needed for a future mechanism claim, recover circuit-level temperature-sensor / oscillator implementation evidence rather than inferring it from interface behavior.
6. Seek thermal-transient / retention-fault validation before making any claim about how well either policy covers worst-retention cells.
7. Keep product-document chronology separate from first shipment, first volume adoption, and standards-ballot chronology.

---

## Sources

1. Infineon Technologies AG, **_HYB25L512160AC-7.5 / HYE25L512160AC-7.5, 512MBit Mobile-RAM_**, Data Sheet Rev. 1.2, February 2004, preserved page-stable PDF: <https://docs.ampnuts.ru/eevblog.docs/_Datasheets/RAM.SDRAM/Mobile/1-HYB25L512160AC_Rev.1.2.pdf>.
2. Infineon Technologies AG, **_HYB25L512160AC-7.5, 512MBit Mobile-RAM_**, Rev. 1.3, April 2004, text corroboration for the same TCSR description: <https://datasheet4u.com/pdf-down/H/Y/B/HYB25L512160AC-7.5-Infineon.pdf>.
3. Samsung Semiconductor, **_K4M56323LE - M(E)E/N/S/C/L/R, 2M × 32Bit × 4 Banks Mobile-SDRAM_**, February 2004, preserved manufacturer-datasheet text: <https://dtsheet.com/doc/304110/samsung-k4m56323le-en80>.
4. Samsung Semiconductor, **_K4S56163PF Mobile-SDRAM_**, September 2004, preserved manufacturer-datasheet text used only as a same-manufacturer continuity witness: <https://manualmachine.com/datasheet/k4s56163pf/8448986-datasheet-samsung/>.
