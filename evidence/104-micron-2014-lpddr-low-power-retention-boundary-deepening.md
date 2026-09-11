# Case 104 Deepening — Micron Mobile LPDDR Low-Power Retention Boundaries (2014)

## Purpose

This record deepens [`../cases/104-micron-lpddr-selective-adaptive-self-refresh.md`](../cases/104-micron-lpddr-selective-adaptive-self-refresh.md) around one bounded question:

> when one named LPDDR device offers ordinary Power-Down, SELF REFRESH, and Deep Power-Down, which of those low-power states actually retains payload, by what maintenance relation, and what happens on exit?

The answer is deliberately narrower than a history of LPDDR power management. A Micron 512Mb Mobile LPDDR datasheet, Rev. I (January 2014), exposes three different contracts inside one product family:

```text
ordinary Power-Down
    refresh temporarily stops
    -> retention remains deadline-bounded

SELF REFRESH
    device performs refresh internally
    -> payload is retained while powered and within specified conditions

Deep Power-Down
    array power / refresh support is withdrawn
    -> payload retention is not promised
    -> full DRAM initialization is required on exit
```

The document is a manufacturer-origin technical publication preserved on a Texas Instruments support site rather than a current Micron origin host, so historical claims from this copy are tagged `H/P*` under repository policy.

## Primary source inspected

Micron Technology, Inc., _512Mb: x16, x32 Mobile LPDDR SDRAM_, document `t67m_512mb_mobile_lpddr.pdf`, Rev. I, January 2014, especially printed pp. 90–94 (PDF pp. 89–93), preserved by Texas Instruments:

<https://e2e.ti.com/cfs-file/__key/telligent-evolution-components-attachments/00-791-00-00-00-38-27-14/T67M_5F00_512Mb_5F00_mobile_5F00_lpddr_5F00_sdram.pdf>

The same 2009–2014 Micron family is already the bounded object of Case 104. This record does not introduce a new product lineage or priority claim; it tightens one power-state seam in the existing case.

## Historical record — ordinary Power-Down is retentive only inside the refresh deadline

The datasheet says that entering Power-Down disables input/output buffers other than CKE. It then states that Power-Down duration is **limited by the refresh requirements of the device**. The timing figure reinforces the point with `Must not exceed refresh device limits`, and exit requires the normal `tXP` delay before another valid command.

The bounded historical result is therefore:

```text
Power-Down
    !=
power removed from the DRAM array

Power-Down
    !=
self-refresh maintenance
```

Ordinary Power-Down is a lower-activity interval during which the existing charge state may survive, but the device is not performing the recurring refresh work needed for an arbitrarily long stay in that state. The allowed interval is bounded by the same retention deadline that makes refresh necessary.

This blocks the shorthand `power-down = powered off`.

## Historical record — SELF REFRESH retains payload by continuing internal maintenance

The same datasheet says SELF REFRESH can retain data while the rest of the system is powered down and that external clocking is not needed. The device nevertheless continues refresh internally. Refresh intervals are scheduled inside the device and may vary; temperature sensing and PASR/TCSR policy discussed in the main Case 104 determine cadence and scope.

Thus the low external activity is not passive retention:

```text
external clock absent
    !=
refresh absent
```

SELF REFRESH is a maintenance-bearing state. The payload survives because the device continues the constitutive work that dynamic charge requires.

## Historical record — Deep Power-Down intentionally crosses the retention boundary

Micron describes Deep Power-Down (DPD) as the maximum-power-reduction mode obtained by eliminating power to the memory array. The datasheet states that data **will not be retained** after entering DPD.

The exit contract is equally important. After CKE is raised to leave DPD, Micron requires a **full DRAM initialization sequence** before normal operation resumes. The timing figure repeats that requirement.

This produces a stronger distinction than merely saying “DPD uses less power”:

```text
exit ordinary Power-Down
    -> wait tXP, continue service with retained payload

exit SELF REFRESH
    -> wait tXSR / complete internal refresh, continue with retained payload

exit DPD
    -> full DRAM initialization required; prior payload is outside the retention contract
```

The required initialization is evidence that DPD exit is not a resume path for retained array contents.

## Engineering reconstruction — low-power depth is not one retention axis

The three modes are useful precisely because energy state and retention state do not collapse into one scalar ordering.

A bounded engineering reconstruction is:

| Mode | Refresh work while resident | Payload contract | Exit relation |
| --- | --- | --- | --- |
| ordinary Power-Down | no recurring refresh in the mode | retained only within refresh timing limits | `tXP`, then ordinary command service |
| SELF REFRESH | internal device refresh continues | retained under the documented powered/operating conditions and selected PASR scope | `tXSR`, then ordinary service |
| Deep Power-Down | retention support withdrawn | data not retained | full DRAM initialization |

The table is a present engineering comparison of manufacturer-defined states, not historical vocabulary supplied by Micron.

Therefore:

> **lower power != stronger retention**

and

> **low-power state != one retention class**.

## Engineering reconstruction — retention can fail by deadline expiry or by policy withdrawal

The same part exposes two different paths out of the retention guarantee:

1. remain too long in ordinary Power-Down without performing the refresh work required by the device; or
2. enter DPD, which intentionally withdraws array-power / refresh support and declares data non-retained.

Those paths should not be flattened into the same event. One is a **deadline-bounded maintenance omission**; the other is a **mode transition that explicitly retires the retention contract**.

This complements Case 104's PASR result. PASR can withdraw maintenance from selected regions while keeping others alive; DPD withdraws the whole-array retention promise.

## Engineering reconstruction — reinitialization is not restoration

The DPD exit sequence requires the DRAM to be initialized again. That requirement restores the device to an operationally admissible state; it does not reconstruct the pre-DPD payload.

Therefore:

```text
service reinitialization
    !=
payload restoration
```

The distinction matters because “the device is usable again” and “the previous data remain current” are different relations.

## Negative evidence / security boundary

The datasheet gives a host-visible retention contract, not a sanitization proof.

It establishes that prior payload is **not promised to remain valid after DPD**. It does not establish:

- the exact time at which every capacitor's residual charge becomes physically unrecoverable;
- whether specialized laboratory techniques can recover any remanent information over some interval;
- a media-sanitization assurance level;
- a verified erase pass;
- cryptographic erasure;
- an overwrite or readback-verification procedure.

Accordingly:

> **`data not retained` != `verified sanitization`**.

DPD is a power-management / retention boundary, not evidence of a security-erasure mechanism.

## Functional comparison — magnetic core and dynamic RAM cross the power boundary differently

Case 02 now has named IBM/DEC evidence that magnetic-core payload can remain during an unpowered interval even though power transitions still need protection and surrounding control state may be reset. This LPDDR witness exposes the opposite bounded relation: dynamic payload in SELF REFRESH still depends on powered internal maintenance, while DPD intentionally removes the condition under which payload survival is promised.

The comparison is functional only:

```text
magnetic core: quiescent payload may remain without sustaining power
LPDDR self refresh: payload remains through powered periodic reconstruction
LPDDR DPD: deepest power-saving mode abandons payload retention
```

No common mechanism, invention genealogy, or historical vocabulary is inferred.

## Philosophical interpretation — retention is a mode contract, not a synonym for “still powered a little”

A bounded project-level interpretation is that apparent persistence depends on which relations a mode continues to support. The three modes use different combinations of power, maintenance, timing, and re-entry procedure; none can be understood from the word “low-power” alone.

This is a philosophical interpretation of the engineering contrast, not wording attributed to Micron or JEDEC.

## Prior-art and anti-anachronism boundaries

This deepening does **not** claim:

- that Micron invented Power-Down, SELF REFRESH, DPD, or LPDDR low-power modes;
- that Rev. I January 2014 is the first public appearance of these functions;
- a JEDEC ballot chronology or direct genealogy between earlier SDRAM and this implementation;
- that Power-Down internally refreshes the array;
- that SELF REFRESH means the array is unpowered;
- that DPD is secure erase or sanitization;
- that the datasheet reveals exact cell-level remanence after DPD;
- that all LPDDR generations use identical entry, exit, or retention semantics.

A broader standards / low-power-memory genealogy belongs primarily in `tmzncty/computing-archaeology`. A repository search found no dedicated Deep Power-Down history there at the time of this deepening, so this record keeps only the bounded product semantics needed by `technical-retention`.

## Resulting bounded distinctions

```text
Power-Down != powered off
Power-Down != SELF REFRESH
SELF REFRESH != no maintenance
SELF REFRESH != passive nonvolatility
DPD != PASR
DPD exit != retained-state resume
full DRAM initialization != payload restoration
data not retained != verified sanitization
low-power state != one retention class
```

## Open work deliberately left outside this slice

- JEDEC normative introduction and revision history of LPDDR DPD / self-refresh modes;
- earlier vendor products implementing DPD;
- cross-vendor differences in entry/exit timing and supply behavior;
- hardware measurement of payload decay or remanence after DPD;
- controller policy deciding among ordinary Power-Down, SELF REFRESH, and DPD;
- broader mobile-memory power-management genealogy.
