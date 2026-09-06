# Micron LPDDR 2009–2014 TCSR/PASR grounding record

This record grounds [`../cases/104-micron-lpddr-selective-adaptive-self-refresh.md`](../cases/104-micron-lpddr-selective-adaptive-self-refresh.md).

The question is narrow: in a named LPDDR family, can the work that makes volatile data survive self refresh be varied both by **rate** and by **coverage**, and what does that imply for technical retention?

## Source A — Micron 512Mb LPDDR family

Micron Technology, Inc., _512Mb: x16, x32 Automotive LPDDR SDRAM_, `t67m_embedded_lpddr_512mb.pdf`, Rev. D, February 2014. The surviving copies used here are manufacturer-document mirrors; they are primary manufacturer text but not independent validation.

### A1. Feature-level separation

**Printed p. 1 and general description around p. 34.**

Micron lists `Temperature-compensated self refresh (TCSR)`, `Partial-array self refresh (PASR)`, and `Deep power-down (DPD)` as distinct features. The general description says TCSR and PASR offer additional self-refresh power savings and can be combined, while DPD removes power from the memory array and does not retain data.

This supports the first boundary:

> TCSR ≠ PASR ≠ DPD.

### A2. Temperature-compensated self refresh

**Printed p. 55, `Temperature-Compensated Self Refresh`.**

The document says an on-die temperature sensor automatically controls the self-refresh oscillator. For this device, programming the TCSR bits has no effect; the oscillator continues at a factory-programmed rate appropriate to device temperature.

**Printed p. 90, `SELF REFRESH Operation`.**

Micron states that self-refresh intervals are scheduled internally and may vary, and may differ from specified `tREFI`. It explicitly warns that SELF REFRESH is not a substitute for AUTO REFRESH during normal operation.

This grounds:

- self refresh is not a fixed-cadence promise;
- temperature sensing can control maintenance cadence;
- ordinary refresh-interface timing and internal self-refresh timing are separate contracts.

The document does not publish the proprietary transfer function from sensed temperature to oscillator frequency, so no such function is reconstructed here.

### A3. Partial-array self refresh

**Printed pp. 55–56, extended mode register and `Partial-Array Self Refresh`.**

The documented PASR field selects full, one-half, one-quarter, one-eighth, or one-sixteenth array coverage. Micron then gives the decisive retention statement: READ/WRITE can still address the full array in standard operation, but during self refresh only selected regions are refreshed and data in non-selected regions will be lost.

This directly grounds:

> ordinary addressability ≠ self-refresh retention coverage.

It also grounds a controlled form of maintenance withdrawal. It does **not** ground secure erase, deterministic decay time, or immediate physical absence.

### A4. DPD is a distinct boundary

The same manufacturer document says DPD achieves maximum power reduction by eliminating power to the memory array and that data are not retained after entry.

That establishes a stronger transition than PASR exclusion in one respect: the array-power precondition itself is withdrawn. It still does not establish secure sanitization.

## Source B — TI 1978 on-chip refresh-address prior art

Texas Instruments, US4207618A, _On-chip refresh for dynamic memory_, filed 26 June 1978, published 10 June 1980.

Google Patents transcription and scan locator:
<https://patents.google.com/patent/US4207618A/en>

The patent describes a dynamic RAM with on-chip refresh-address counter and multiplexing circuitry. Crucially, it still says an external refresh command is needed; the on-chip counter supplies the row address and increments after refresh.

Use of this source is deliberately negative/bounding:

> on-chip refresh address generation ≠ autonomous refresh scheduling.

It also records that external refresh logic was a nontrivial system burden, helping explain why moving maintenance-control functions onto the chip was engineering-relevant without claiming that TI invented every later self-refresh form.

## Source C — Toshiba 1984-priority adaptive self-refresh prior art

Takayasu Sakurai and Tetsuya Iizuka, Toshiba Corp., US4682306A, _Self-refresh control circuit for dynamic semiconductor memory device_, Japanese priority 20 August 1984, US publication 21 July 1987.

<https://patents.google.com/patent/US4682306A/en>

The patent describes on-chip self refresh with an oscillator and refresh-address counter and discusses temperature/leakage sensitivity. Its proposed control observes a capacitor designed to track memory-cell behavior and triggers intermittent refresh as the monitored voltage falls.

This is not used as a product-implementation ancestor for Micron. It is an earlier primary prior-art floor demonstrating that condition-sensitive autonomous refresh scheduling predates the 2009–2014 Micron LPDDR witness.

The Toshiba patent itself cites still-earlier automatic refresh-frequency work, so it is not treated as an origin claim either.

## Evidence ledger

| Claim | Type | Evidence | Strength |
| --- | --- | --- | --- |
| Micron LPDDR separately exposes TCSR, PASR, and DPD | H/P | Micron Rev. D pp. 1, 34 | strong manufacturer-primary |
| on-die temperature sensing controls the bounded self-refresh oscillator | H/P | Micron p. 55 | strong manufacturer-primary |
| self-refresh cadence may vary and differ from normal `tREFI` | H/P | Micron p. 90 | strong manufacturer-primary |
| PASR selects a subset of the physical array for self-refresh maintenance | H/P | Micron pp. 55–56 | strong manufacturer-primary |
| data in PASR-excluded regions are not promised retention | H/P | Micron p. 56 | strong manufacturer-primary |
| DPD removes array power and does not retain data | H/P | Micron command/general-description text | strong manufacturer-primary |
| on-chip refresh addressing existed in a 1978 TI filing while cadence still required an external command | H/P | US4207618A | strong patent-primary |
| adaptive autonomous self-refresh control predates the Micron witness | H/P | US4682306A, 1984 priority | strong patent-primary prior-art floor |
| PASR is secure erase or has a defined instantaneous forgetting time | X | not stated by sources | rejected |
| TI/Toshiba→Micron direct genealogy | X | chronology/functional similarity alone | explicitly unsupported |

## What this changes in the repository

Case 21 established a **maintenance-authority handoff**: recurring refresh commands can move from controller to SDRAM and later move back. Case 104 adds two dimensions inside the self-refresh regime itself:

```text
maintenance rate
    temperature-sensitive / internally scheduled

maintenance scope
    full or selected array region
```

This makes a broader repository point more precise: a retention system need not merely answer `maintain or do not maintain`. It can retain control state describing **how much maintenance** to perform and **which current states remain inside the protected set**.

## Historical cautions

- The Micron PDFs are manufacturer documents preserved by distributors/mirrors; they are not independent laboratory evidence.
- Do not infer a complete JEDEC TCSR/PASR chronology from one Micron family.
- Do not infer Micron's internal circuit from the Toshiba patent.
- Do not equate PASR exclusion with secure deletion or a known physical decay instant.
- Do not back-project the project terms `retention-scope policy` or `selective forgetting` into historical vendor vocabulary.

## Related-repository check

A current GitHub search of `tmzncty/computing-archaeology` for DRAM/PASR/TCSR/self-refresh did not expose a dedicated case. Full LPDDR standards history, controller implementation, refresh-power modeling, modern per-bank refresh, retention-aware refresh, and RowHammer mitigation belong there if developed comprehensively.
