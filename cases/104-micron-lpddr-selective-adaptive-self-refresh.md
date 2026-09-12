# Micron LPDDR TCSR/PASR: Variable Refresh Rate and Selective Retention Scope

## Status

**`grounded`** — bounded to Micron 512Mb x16/x32 Mobile/Automotive LPDDR documentation from the 2009–2014 document family, with older TI and Toshiba patents used only as prior-art boundaries for on-chip refresh-address generation and autonomous self-refresh scheduling.

Grounding record: [`../evidence/104-micron-2009-2014-lpddr-tcsr-pasr-grounding.md`](../evidence/104-micron-2009-2014-lpddr-tcsr-pasr-grounding.md).

Low-power-state retention-boundary deepening: [`../evidence/104-micron-2014-lpddr-low-power-retention-boundary-deepening.md`](../evidence/104-micron-2014-lpddr-low-power-retention-boundary-deepening.md). This product-level slice separates ordinary Power-Down, SELF REFRESH, and DPD without turning DPD content loss into a sanitization claim.

Earlier DPD product-availability / optionality deepening: [`../evidence/104-micron-hynix-2008-2009-dpd-product-availability-deepening.md`](../evidence/104-micron-hynix-2008-2009-dpd-product-availability-deepening.md). This earlier named-product slice moves the bounded public-document floor to June 2008 and adds Hynix May-2009 optional-feature plus MR/EMR-loss evidence without turning product chronology into JEDEC or invention genealogy.

## Scope

Cases 03, 09, 10, 21, and 69 already establish why DRAM requires refresh, how refresh addressing/scheduling can move on-chip, how SDRAM hands recurring refresh responsibility between controller and device, and how DDR4 permits bounded scheduling elasticity. This case asks a narrower question left open by Case 21:

> What changes when self-refresh maintenance can vary not only in **when** it runs, but also in **which parts of the array are kept alive**?

The bounded object is Micron's `MT46H32M16LF` / `MT46H16M32LF` / `MT46H16M32LG` 512Mb LPDDR family, especially the automotive document `t67m_embedded_lpddr_512mb.pdf`, Rev. D (February 2014).

This is not a general LPDDR or JEDEC history and makes no invention-priority claim for TCSR, PASR, self refresh, or low-power DRAM.

## Historical record

### H/P — The product exposes TCSR, PASR, and deep power-down as different retention controls

Micron's feature list names `temperature-compensated self refresh (TCSR)`, `partial-array self refresh (PASR)`, and `deep power-down (DPD)` separately. The same document specifies a 64 ms refresh interval in its ordinary operating envelope and a 32 ms requirement for automotive temperature.

This vocabulary matters because the three features alter different relations:

- TCSR changes self-refresh cadence according to temperature;
- PASR changes which array regions are refreshed during self refresh;
- DPD removes array power and does not promise payload retention.

They are not three names for the same low-power state.

### H/P — Temperature compensation changes maintenance rate, not the existence of the refresh obligation

The extended-mode-register section states that the device contains a temperature sensor used for automatic control of the self-refresh oscillator. In this documented part, programming the TCSR bits has no effect; the oscillator continues at an `optimal factory-programmed rate for the device temperature`.

The self-refresh operation section makes the interface consequence explicit: during self refresh, refresh intervals are scheduled internally and **may vary**, and those intervals may differ from ordinary `tREFI`. Micron therefore warns that SELF REFRESH must not be used as a substitute for AUTO REFRESH during normal operation.

The historical claim is limited to this manufacturer contract. It does not establish a universal temperature-to-refresh function or expose the proprietary oscillator law.

### H/P — PASR turns retention coverage into programmed control state

Micron documents PASR through extended-mode-register bits that select:

- full array;
- one-half array;
- one-quarter array;
- one-eighth array;
- one-sixteenth array.

The crucial sentence is not merely the power-saving claim. Micron states that normal READ and WRITE commands can still address the full array during standard operation, but during self refresh **only the selected regions are refreshed**, and data in regions not selected **will be lost**.

Thus host-visible physical capacity and self-refresh retention coverage are explicitly separable in one named product family.

### H/P — Deep power-down is a different forgetting boundary

The same document describes DPD as maximum power reduction by eliminating power to the memory array and states that data are not retained after entry.

PASR therefore cannot be collapsed into DPD:

- PASR continues refresh work for a selected subset;
- DPD removes the array-power condition needed for dynamic retention.

### H/P* — Power-Down, SELF REFRESH, and DPD expose different retention contracts

A second January-2014 Micron Mobile LPDDR datasheet tightens the low-power boundary. Ordinary **Power-Down** disables most interface activity, but the manufacturer explicitly limits its duration by the device refresh requirement; it is therefore not an indefinite retention mode and it is not equivalent to removing power. **SELF REFRESH** instead keeps the dynamic payload current by scheduling refresh internally without an external clock. **Deep Power-Down** crosses a different boundary: Micron says memory-array power is eliminated, prior data are not retained, and exit requires a full DRAM initialization sequence.

The bounded state relation is therefore:

```text
ordinary Power-Down
    -> no refresh while resident; duration bounded by refresh deadline

SELF REFRESH
    -> internal refresh continues; selected payload remains under the documented conditions

Deep Power-Down
    -> retention support withdrawn; data not retained; full reinitialization on exit
```

This supports `Power-Down != powered off`, `SELF REFRESH != passive nonvolatility`, and `DPD exit != retained-state resume`. The source is a vendor-origin Micron datasheet preserved on a Texas Instruments site, so these claims are recorded as `H/P*` rather than current-origin `H/P`.

The content-loss statement is still not a sanitization guarantee. The datasheet does not establish the cell-level remanence horizon, laboratory recoverability, or verified physical erasure after DPD.

### H/P* — named Mobile-DDR DPD product documents are visible by 2008–2009, with optionality still explicit

Micron's earlier Mobile DDR Rev. H document (June 2008) already lists Deep Power-Down for the `MT46H16M16LF` / `MT46H8M32LF/LG` family and gives the same broad non-retentive boundary: memory-array power is eliminated, payload is not retained, and exit is followed by 200 microseconds of valid clocks plus PRECHARGE ALL and the full initialization sequence.

Hynix's `H5MS2G22MFR` / `H5MS2G32MFR` Rev. 1.2 document (May 2009) independently describes Deep Power Down, but marks it as an **optional feature**. Its DPD section says internal voltage generators stop, all memory data are lost, and Mode Register plus Extended Mode Register information are also lost; exit requires a 200-microsecond wait and complete device reinitialization.

These dated documents are product-document lower bounds, not invention or JEDEC-standardization dates. They add two bounded distinctions:

```text
product-family documentation includes DPD
    !=
every ordering/configuration necessarily implements DPD

DPD payload loss
    can coexist with
configuration/control-state loss
```

The Hynix optionality statement is especially important: presence of interface vocabulary and a command description is not by itself proof of universal feature availability.

Detailed source treatment: [`../evidence/104-micron-hynix-2008-2009-dpd-product-availability-deepening.md`](../evidence/104-micron-hynix-2008-2009-dpd-product-availability-deepening.md).

## Retained state and control state

At least four state classes must remain distinct:

1. **payload state** — charge-encoded data in DRAM cells;
2. **retention-scope policy** — PASR mode-register state selecting which regions receive maintenance;
3. **maintenance-rate control** — temperature-sensor / self-refresh-oscillator relation that determines internal cadence;
4. **power/mode state** — whether the device is in ordinary operation, self refresh, or DPD;
5. **device-configuration state** — mode-register settings that may need to be reconstructed after a deep-power transition; the May-2009 Hynix product document explicitly says MR/EMR information is lost in DPD.

The project terms `retention-scope policy` and `maintenance-rate control` are engineering reconstructions, not Micron's or Hynix's historical vocabulary. The Hynix MR/EMR statement is a named-product witness and must not be universalized to every LPDDR generation.

## Engineering reconstruction

### E — Self refresh does not imply a fixed cadence

Case 21 established that self refresh moves recurring refresh generation inside the SDRAM. Case 104 adds that `inside` does not mean `fixed`: the device can vary its internally scheduled intervals according to temperature while still satisfying its retention contract.

> **self refresh ≠ fixed refresh cadence**

### E — Array capacity and maintained-retention set can diverge

PASR makes a strong retention distinction visible:

```text
addressable array during standard operation
    !=
array subset selected for maintenance during self refresh
```

A region can belong to the device's ordinary address space yet intentionally fall outside the set whose charge state the low-power mode promises to maintain.

### E — Forgetting can be implemented by withdrawing maintenance

For PASR-excluded regions, Micron does not specify an explicit erase pulse. The documented guarantee is weaker and more interesting: those regions are no longer refreshed in self refresh, and their data will be lost.

Therefore, in this bounded mechanism:

> **retention-policy withdrawal ≠ explicit physical erase**.

It is also not a secure-sanitization guarantee. The document does not specify the exact instant at which every excluded cell becomes unrecoverable or whether forensic remnants can persist temporarily.

### E — Maintenance effort has independent scope and rate axes

TCSR and PASR can be analyzed as orthogonal control dimensions:

```text
rate axis
    how often maintenance occurs

scope axis
    which regions receive maintenance
```

The same dynamic substrate can therefore reduce low-power work by varying cadence and/or by shrinking the maintained set.

### E — Retention metadata is constitutive without being payload

PASR selection bits do not hold user data, but they change which user data are promised survival across self refresh. Likewise, temperature sensing does not measure payload semantics, yet it changes the refresh cadence that keeps payload recoverable.

Small control states can therefore govern the future survivability of a much larger payload.

## Prior art boundary

Texas Instruments' 1978-filed US4207618A already places a refresh-address counter and multiplexing circuitry on a DRAM chip, but still requires an **external refresh command**. That evidence is an earlier floor for `on-chip refresh addressing`, not proof of autonomous self-refresh scheduling.

Toshiba's US4682306A has Japanese priority in 1984 and describes a self-refresh circuit with an oscillator and refresh-address counter, including leakage/temperature-sensitive control. Case 10 already grounds that history. It blocks any claim that the 2009–2014 Micron product family invented adaptive self refresh.

Case 104 therefore contributes neither a first-invention claim nor a direct genealogy. It contributes a named-product retention contract in which maintenance **rate** and maintenance **coverage** are separately controllable.

## Functional analogy and philosophical limit

A functional analogy to archival retention policy is tempting: some records are selected for continued preservation while others are allowed to lapse. The engineering similarity is only the selective-maintenance relation. PASR does not establish institutional appraisal, human meaning, archival authority, or Stieglerian tertiary retention.

The bounded conceptual result is smaller:

> apparent persistence can be produced by a policy that allocates maintenance selectively in both time and space.

That is an engineering fact first, not a universal philosophy of forgetting.

## Cross-case result

The DRAM chain can now be decomposed without flattening the historical mechanisms:

```text
Case 03  leakage creates a refresh deadline
Case 09  refresh-row enumeration can move on-chip
Case 10  refresh scheduling can become autonomous and condition-derived
Case 21  recurring refresh responsibility can hand off between controller and SDRAM
Case 69  external refresh issue time can have bounded scheduling elasticity
Case 104 self-refresh cadence can be temperature-adaptive and its retained coverage can be selectively reduced
```

This is a functional comparison. It is not a claim of one linear invention genealogy.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Micron's 512Mb LPDDR family exposes TCSR, PASR, and DPD as separate features | H/P | manufacturer datasheet |
| an on-die temperature sensor controls the self-refresh oscillator in the bounded part | H/P | Micron extended-mode-register text, p. 55 |
| self-refresh intervals may vary and may differ from ordinary `tREFI` | H/P | Micron self-refresh operation, p. 90 |
| PASR can select full, 1/2, 1/4, 1/8, or 1/16 array coverage | H/P | Micron extended-mode-register/PASR text, pp. 55–56 |
| data in PASR-excluded regions are not retained by self refresh | H/P | Micron p. 56 |
| DPD eliminates array power and does not retain payload | H/P | Micron command/general-description text |
| ordinary Power-Down duration is bounded by refresh requirements rather than providing indefinite retention | H/P* | Micron Mobile LPDDR Rev. I 01/14 pp. 90–93 |
| SELF REFRESH retains payload through internally scheduled refresh without external clocking | H/P* | Micron Mobile LPDDR Rev. I 01/14 pp. 89–90 |
| exit from DPD requires a full DRAM initialization sequence | H/P* | Micron Mobile LPDDR Rev. I 01/14 pp. 93–94 |
| Micron Rev. H 6/08 publicly documents DPD for a named Mobile DDR product family, with non-retention and full-init exit semantics | H/P* | Micron vendor document preserved by archival mirror |
| Hynix Rev. 1.2 05/09 documents DPD as optional and states that payload plus MR/EMR state are lost | H/P* | Hynix vendor datasheet preserved by distributor |
| appearance of DPD in a product-family document proves universal availability across every listed configuration | X | contradicted by Hynix's explicit optional-feature language |
| DPD content loss is equivalent to verified sanitization | X | not established; no remanence / recovery / erase-assurance evidence |
| retention coverage and ordinary addressable capacity can differ | E | bounded reconstruction from PASR semantics |
| maintenance rate and maintenance scope are independent comparison axes | E/A | bounded cross-feature comparison |
| PASR exclusion is equivalent to secure erase | X | not established; no sanitization or exact decay-completion semantics are specified |
| Micron invented adaptive/partial self refresh | X | blocked by earlier prior art and outside source scope |

## Related repositories

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated PASR/TCSR or LPDDR2 REFpb case. [`Case 105`](105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md) now handles the bounded per-bank-refresh transaction-granularity boundary, which is deliberately distinct from Case 104's retained-coverage policy. A full LPDDR/JEDEC refresh-feature genealogy, controller implementation history, modern retention-aware scheduling, and RowHammer-era refresh policy should be developed there if pursued broadly.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) remains the anti-anachronism guard: `retention-scope policy`, `maintenance-rate control`, and `selective forgetting` are present analytical terms, not vocabulary attributed to Micron engineers.

## Sources

1. Micron Technology, Inc., _512Mb: x16, x32 Automotive LPDDR SDRAM_, `t67m_embedded_lpddr_512mb.pdf`, Rev. D, February 2014, especially pp. 34, 55–56, and 90. Preserved manufacturer document via DigiKey/device-report mirrors: <https://media.digikey.com/pdf/Data%20Sheets/Micron%20Technology%20Inc%20PDFs/MT46H16M32LF%28LG%29_MT46H32M16LF.pdf> and <https://device.report/m/ee2b8a56e871864419dcf093c9a7d59531ea90387f192f2bd45316bda78a9f79>.
2. Lionel S. White, Jr. and G. R. Mohan Rao, Texas Instruments, US4207618A, _On-chip refresh for dynamic memory_, filed 26 June 1978, published 10 June 1980: <https://patents.google.com/patent/US4207618A/en>.
3. Takayasu Sakurai and Tetsuya Iizuka, Toshiba Corp., US4682306A, _Self-refresh control circuit for dynamic semiconductor memory device_, Japanese priority 20 August 1984, US publication 21 July 1987: <https://patents.google.com/patent/US4682306A/en>.
4. Micron Technology, Inc., _512Mb: x16, x32 Mobile LPDDR SDRAM_, `t67m_512mb_mobile_lpddr.pdf`, Rev. I, January 2014, especially pp. 90–94; vendor-origin datasheet preserved via Texas Instruments: <https://e2e.ti.com/cfs-file/__key/telligent-evolution-components-attachments/00-791-00-00-00-38-27-14/T67M_5F00_512Mb_5F00_mobile_5F00_lpddr_5F00_sdram.pdf>.
5. Micron Technology, Inc., Mobile DDR SDRAM `MT46H16M16LF` / `MT46H8M32LF/LG`, Rev. H, June 2008, especially feature list and Deep Power-Down operation; vendor-origin text preserved by AllDatasheet: <https://www.alldatasheet.com/html-pdf/75876/MICRON/MT46H16M16LF/185/1/MT46H16M16LF.html> and <https://www.alldatasheet.com/html-pdf/75876/MICRON/MT46H16M16LF/9123/49/MT46H16M16LF.html>.
6. Hynix Semiconductor, _2Gbit Mobile DDR SDRAM_, `H5MS2G22MFR` / `H5MS2G32MFR`, Rev. 1.2, May 2009, especially feature list and Deep Power Down operation; vendor datasheet preserved by Farnell: <https://www.farnell.com/datasheets/1750885.pdf>.
