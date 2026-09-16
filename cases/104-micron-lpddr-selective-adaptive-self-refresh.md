# Micron LPDDR TCSR/PASR: Variable Refresh Rate and Selective Retention Scope

## Status

**`grounded`** — bounded to Micron Mobile SDRAM / Mobile DDR / LPDDR product documentation from 2002–2014, with older TI and Toshiba patents used only as prior-art boundaries for on-chip refresh-address generation and autonomous self-refresh scheduling.

Grounding record: [`../evidence/104-micron-2009-2014-lpddr-tcsr-pasr-grounding.md`](../evidence/104-micron-2009-2014-lpddr-tcsr-pasr-grounding.md).

Low-power-state retention-boundary deepening: [`../evidence/104-micron-2014-lpddr-low-power-retention-boundary-deepening.md`](../evidence/104-micron-2014-lpddr-low-power-retention-boundary-deepening.md). This product-level slice separates ordinary Power-Down, SELF REFRESH, and DPD without turning DPD content loss into a sanitization claim.

Earlier DPD product-availability / optionality deepening: [`../evidence/104-micron-hynix-2008-2009-dpd-product-availability-deepening.md`](../evidence/104-micron-hynix-2008-2009-dpd-product-availability-deepening.md). This slice remains useful for 2008 Micron continuity and Hynix May-2009 optional-feature plus explicit MR/EMR-loss evidence, but it is no longer the earliest product-document floor in this case.

**May-2002 pre-LPDDR / Mobile-SDRAM DPD deepening:** [`../evidence/104-micron-2002-mobile-sdram-dpd-command-repurposing-deepening.md`](../evidence/104-micron-2002-mobile-sdram-dpd-command-repurposing-deepening.md). Micron's `ADVANCE` `MT48V16M16LFFG` / `MT48H16M16LFFG` document pushes the bounded manufacturer-document floor back to May 2002 and adds two new boundaries: DPD exit requires substantial reinitialization before service resumes, and the command sequence used for DPD on this mobile/BAT-RAM family is explicitly identified as Burst Terminate on traditional SDRAM. The source is development-stage documentation, not shipment or invention evidence.

## Scope

Cases 03, 09, 10, 21, and 69 already establish why DRAM requires refresh, how refresh addressing/scheduling can move on-chip, how SDRAM hands recurring refresh responsibility between controller and device, and how DDR4 permits bounded scheduling elasticity. This case asks a narrower question left open by Case 21:

> What changes when self-refresh maintenance can vary not only in **when** it runs, but also in **which parts of the array are kept alive** — and how do deeper low-power modes alter the retention contract altogether?

The primary grounded object remains Micron's `MT46H32M16LF` / `MT46H16M32LF` / `MT46H16M32LG` 512Mb LPDDR family, especially the automotive document `t67m_embedded_lpddr_512mb.pdf`, Rev. D (February 2014). Earlier Mobile SDRAM / Mobile DDR documents are used to deepen chronology and state-transition boundaries without silently back-projecting later LPDDR terminology onto the 2002 part.

This is not a general LPDDR or JEDEC history and makes no invention-priority claim for TCSR, PASR, self refresh, DPD, or the command encodings used to invoke them.

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

### H/P* — Micron already documented the three-way low-power boundary in May 2002, at development-document status

Micron's `MT48V16M16LFFG` / `MT48H16M16LFFG` **256Mb x16 Mobile SDRAM** datasheet carries the internal footer `MobileRamY26L_A.p65 – Pub. 5/02`, ©2002 Micron, and is explicitly designated **`ADVANCE`**. The designation note says this category contains initial descriptions of products still under development.

The same document already separates:

```text
ordinary Power-Down
    -> no refresh is performed
    -> residence may not exceed the 64 ms refresh period

SELF REFRESH
    -> internal clocking performs refresh cycles

Deep Power-Down
    -> whole-array power is shut off
    -> payload is not retained
```

This moves Case 104's bounded manufacturer-document floor for named-product DPD semantics from 2008 to **May 2002**, but only as a **development-stage public-document witness**. It does not establish volume shipment, first silicon, first publication anywhere, or invention priority.

Detailed source treatment: [`../evidence/104-micron-2002-mobile-sdram-dpd-command-repurposing-deepening.md`](../evidence/104-micron-2002-mobile-sdram-dpd-command-repurposing-deepening.md).

### H/P* — the 2002 DPD exit path distinguishes leaving the power state from regaining normal service

The May-2002 Micron document requires, after CKE is raised to exit Deep Power-Down:

1. at least 200 microseconds of NOP conditions;
2. PRECHARGE for all banks;
3. eight or more AUTO REFRESH commands;
4. MODE REGISTER initialization;
5. EXTENDED MODE REGISTER initialization.

The same document says the Extended Mode Register retains its state until reprogrammed or device power is lost, and uses that register for TCSR/PASR control.

The historical interface therefore exposes three different transition points:

```text
Deep Power-Down electrical exit
    !=
normal-command admissibility restored
    !=
pre-DPD payload restored
```

The source gives an initialization contract, not a payload-recovery contract.

### H/P* — the same command sequence can denote Burst Terminate on traditional SDRAM and DPD on this mobile family

Micron's 2002 command-table notes explicitly state that Deep Power-Down is a power-saving feature of the Mobile SDRAM / BAT-RAM device and that **the same command is Burst Terminate on traditional SDRAM components**, while the mobile/BAT-RAM part assigns that command sequence to Deep Power-Down.

That is direct period evidence that electrical command form and functional semantics must be kept separate:

```text
same command encoding
    !=
same operation across device contracts
```

The phrase `device contract` is project engineering vocabulary; Micron's historical claim is the explicit Burst-Terminate/Deep-Power-Down reassignment.

### H/P* — named Mobile-DDR DPD documents in 2008–2009 add continuity and optionality, not the earliest known floor

Micron's Mobile DDR Rev. H document (June 2008) lists Deep Power-Down for the `MT46H16M16LF` / `MT46H8M32LF/LG` family and gives the same broad non-retentive boundary: memory-array power is eliminated, payload is not retained, and exit is followed by 200 microseconds of valid clocks plus PRECHARGE ALL and the full initialization sequence.

Hynix's `H5MS2G22MFR` / `H5MS2G32MFR` Rev. 1.2 document (May 2009) independently describes Deep Power Down, but marks it as an **optional feature**. Its DPD section says internal voltage generators stop, all memory data are lost, and Mode Register plus Extended Mode Register information are also lost; exit requires a 200-microsecond wait and complete device reinitialization.

These documents remain useful because they add later named-product continuity and explicit optionality:

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

At least five state classes must remain distinct:

1. **payload state** — charge-encoded data in DRAM cells;
2. **retention-scope policy** — PASR mode-register state selecting which regions receive maintenance;
3. **maintenance-rate control** — temperature-related TCSR state and, in later products, the sensor/self-refresh-oscillator relation that determines internal cadence;
4. **power/mode state** — whether the device is in ordinary operation, Power-Down, SELF REFRESH, or DPD;
5. **device-configuration state** — mode-register settings needed to establish service behavior after a deep-power transition. The May-2002 Micron document requires MR/EMR initialization after DPD; the May-2009 Hynix document explicitly says MR/EMR information is lost in DPD.

The project terms `retention-scope policy`, `maintenance-rate control`, and `command-admission state` are engineering reconstructions, not Micron's or Hynix's historical vocabulary. The exact physical storage implementation of each control bit is outside this case.

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

### E — low-power mode depth does not map monotonically onto one retention category

The 2002 witness makes this especially clear:

```text
Power-Down
    -> less interface activity
    -> refresh paused, deadline continues to age

SELF REFRESH
    -> low external activity
    -> internal maintenance remains active

Deep Power-Down
    -> deeper power saving
    -> documented payload-retention condition withdrawn
```

`lower power` therefore does not by itself tell us whether persistence is actively maintained, merely deadline-bounded, or explicitly outside the product contract.

### E — electrical state transition completion ≠ service restoration ≠ payload recovery

The 2002 DPD exit sequence requires time, refresh/precharge work, and register initialization before a new ordinary command is admissible. Thus:

```text
left DPD
    !=
ready for ordinary service
    !=
old data recovered
```

The last inequality is decisive because the same source says the old array data are not retained by DPD.

### E — command identity is contract-relative

The 2002 document's explicit Burst-Terminate/DPD reassignment shows that command semantics cannot safely be reconstructed from an electrical pin pattern alone. The applicable product/state-machine contract is part of the interpretation machinery.

This does not mean `the command itself is retained state`. It means historical recovery of interface behavior requires preserving which specification/device family gives the code its meaning.

### E — Retention metadata is constitutive without being payload

PASR selection bits do not hold user data, but they change which user data are promised survival across self refresh. Likewise, temperature-related control does not measure payload semantics, yet it changes the refresh cadence that keeps payload recoverable.

Small control states can therefore govern the future survivability of a much larger payload.

## Prior art boundary

Texas Instruments' 1978-filed US4207618A already places a refresh-address counter and multiplexing circuitry on a DRAM chip, but still requires an **external refresh command**. That evidence is an earlier floor for `on-chip refresh addressing`, not proof of autonomous self-refresh scheduling.

Toshiba's US4682306A has Japanese priority in 1984 and describes a self-refresh circuit with an oscillator and refresh-address counter, including leakage/temperature-sensitive control. Case 10 already grounds that history. It blocks any claim that the 2002–2014 Micron product chain invented adaptive self refresh.

The May-2002 Micron ADVANCE datasheet is now the earliest **named-product/public manufacturer-document witness currently held by this case for DPD**, not a claim about invention or standardization. It is also not silently labeled `LPDDR`; the source's own title is Mobile SDRAM and its text also uses BAT-RAM terminology.

Case 104 therefore contributes neither a first-invention claim nor a direct genealogy. It contributes bounded product contracts in which maintenance **rate**, maintenance **coverage**, power-state support, configuration recovery, and command meaning can be separated.

## Functional analogy and philosophical limit

A functional analogy to archival retention policy is tempting: some records are selected for continued preservation while others are allowed to lapse. The engineering similarity is only the selective-maintenance relation. PASR does not establish institutional appraisal, human meaning, archival authority, or Stieglerian tertiary retention.

The 2002 command-repurposing evidence adds a separate interpretive caution: a surviving bit/pin pattern does not by itself preserve the operation it once denoted if the device contract needed to interpret that pattern is missing. This is an interface-level engineering result, not a general theory of hermeneutics.

The bounded conceptual result is smaller:

> apparent persistence can be produced by a policy that allocates maintenance selectively in time and space, while deeper power-state transitions can withdraw the retention contract and require reconstruction of service/control state before the device again becomes operational.

That is an engineering fact first, not a universal philosophy of forgetting.

## Cross-case result

The DRAM chain can now be decomposed without flattening the historical mechanisms:

```text
Case 03  leakage creates a refresh deadline
Case 09  refresh-row enumeration can move on-chip
Case 10  refresh scheduling can become autonomous and condition-derived
Case 21  recurring refresh responsibility can hand off between controller and SDRAM
Case 69  external refresh issue time can have bounded scheduling elasticity
Case 104 low-power modes can pause, internalize, selectively narrow, or withdraw retention support; DPD exit can require reinitialization before service
Case 35  later Mobile-DDR products can move temperature-conditioned cadence authority inside the device while PASR remains a separate coverage axis
```

This is a functional comparison. It is not a claim of one linear invention genealogy.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Micron's 512Mb LPDDR family exposes TCSR, PASR, and DPD as separate features | H/P | manufacturer datasheet |
| an on-die temperature sensor controls the self-refresh oscillator in the bounded later part | H/P | Micron extended-mode-register text, p. 55 |
| self-refresh intervals may vary and may differ from ordinary `tREFI` | H/P | Micron self-refresh operation, p. 90 |
| PASR can select full, 1/2, 1/4, 1/8, or 1/16 array coverage | H/P | Micron extended-mode-register/PASR text, pp. 55–56 |
| data in PASR-excluded regions are not retained by self refresh | H/P | Micron p. 56 |
| DPD eliminates array power and does not retain payload | H/P | Micron command/general-description text |
| ordinary Power-Down duration is bounded by refresh requirements rather than providing indefinite retention | H/P* | Micron Mobile LPDDR Rev. I 01/14 pp. 90–93; also May-2002 Mobile SDRAM witness |
| SELF REFRESH retains payload through internally scheduled refresh without external clocking | H/P* | Micron Mobile LPDDR Rev. I 01/14; May-2002 Mobile SDRAM continuity |
| exit from DPD requires substantial initialization before ordinary service | H/P* | Micron May-2002 and later Mobile-DDR/LPDDR documents |
| Micron `MT48V16M16LFFG` / `MT48H16M16LFFG` ADVANCE document publicly describes DPD by May 2002 | H/P* | manufacturer document on archival mirror; document itself says product still under development |
| May-2002 DPD exit requires 200 µs NOP, all-bank PRECHARGE, eight or more AUTO REFRESH operations, and MR/EMR initialization | H/P* | explicit operation text, printed p. 24 |
| May-2002 Micron says the command is Burst Terminate on traditional SDRAM but assigned to DPD on the mobile/BAT-RAM part | H/P* | explicit command-table note |
| May-2002 ADVANCE documentation proves volume shipment | X | explicitly rejected by development-stage designation |
| same command encoding guarantees the same functional operation across device families | X | contradicted by Micron command note |
| Micron Rev. H 6/08 publicly documents DPD for a named Mobile DDR family | H/P* | later continuity witness, no longer earliest floor in case |
| Hynix Rev. 1.2 05/09 documents DPD as optional and states that payload plus MR/EMR state are lost | H/P* | Hynix vendor datasheet preserved by distributor |
| appearance of DPD in a product-family document proves universal availability across every listed configuration | X | contradicted by Hynix's explicit optional-feature language |
| DPD content loss is equivalent to verified sanitization | X | not established; no remanence / recovery / erase-assurance evidence |
| retention coverage and ordinary addressable capacity can differ | E | bounded reconstruction from PASR semantics |
| maintenance rate and maintenance scope are independent comparison axes | E/A | bounded cross-feature comparison |
| DPD electrical exit is the same event as service readiness or old-payload recovery | X | contradicted by mandatory initialization sequence plus non-retention statement |
| PASR exclusion is equivalent to secure erase | X | not established; no sanitization or exact decay-completion semantics are specified |
| Micron invented adaptive/partial self refresh or DPD | X | outside source scope; earlier prior art/genealogy remains separate |

## Related repositories

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for the exact 2002 part number and for `Deep Power Down` found no dedicated module to reuse. [`Case 105`](105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md) handles the bounded per-bank-refresh transaction-granularity boundary, deliberately distinct from Case 104's retained-coverage and power-state policy.

A full Mobile SDRAM / BAT-RAM / Mobile DDR / LPDDR nomenclature and standards genealogy, JEDEC DPD introduction history, controller policy, product shipment history, and power-domain circuit archaeology should be developed in `computing-archaeology` if pursued broadly. This case retains only the retention-specific mode/maintenance/configuration/interface boundary.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) remains the anti-anachronism guard: `retention-scope policy`, `maintenance-rate control`, `command-admission state`, and `contract-relative command identity` are present analytical terms, not vocabulary attributed to Micron engineers.

## Sources

1. Micron Technology, Inc., _512Mb: x16, x32 Automotive LPDDR SDRAM_, `t67m_embedded_lpddr_512mb.pdf`, Rev. D, February 2014, especially pp. 34, 55–56, and 90. Preserved manufacturer document via DigiKey/device-report mirrors: <https://media.digikey.com/pdf/Data%20Sheets/Micron%20Technology%20Inc%20PDFs/MT46H16M32LF%28LG%29_MT46H32M16LF.pdf> and <https://device.report/m/ee2b8a56e871864419dcf093c9a7d59531ea90387f192f2bd45316bda78a9f79>.
2. Lionel S. White, Jr. and G. R. Mohan Rao, Texas Instruments, US4207618A, _On-chip refresh for dynamic memory_, filed 26 June 1978, published 10 June 1980: <https://patents.google.com/patent/US4207618A/en>.
3. Takayasu Sakurai and Tetsuya Iizuka, Toshiba Corp., US4682306A, _Self-refresh control circuit for dynamic semiconductor memory device_, Japanese priority 20 August 1984, US publication 21 July 1987: <https://patents.google.com/patent/US4682306A/en>.
4. Micron Technology, Inc., _256Mb: x16 Mobile SDRAM_, `MT48V16M16LFFG` / `MT48H16M16LFFG`, `ADVANCE`, footer `MobileRamY26L_A.p65 – Pub. 5/02`, ©2002 Micron Technology, Inc. Manufacturer document preserved by archival HTML transcription: <https://dtsheet.com/doc/503993/micron-mt48v16m16lffg>. Relevant anchors include printed pp. 9, 23–24, 28, and 58.
5. Micron Technology, Inc., _512Mb: x16, x32 Mobile LPDDR SDRAM_, `t67m_512mb_mobile_lpddr.pdf`, Rev. I, January 2014, especially pp. 90–94; vendor-origin datasheet preserved via Texas Instruments: <https://e2e.ti.com/cfs-file/__key/telligent-evolution-components-attachments/00-791-00-00-00-38-27-14/T67M_5F00_512Mb_5F00_mobile_5F00_lpddr_5F00_sdram.pdf>.
6. Micron Technology, Inc., Mobile DDR SDRAM `MT46H16M16LF` / `MT46H8M32LF/LG`, Rev. H, June 2008, especially feature list and Deep Power-Down operation; vendor-origin text preserved by AllDatasheet: <https://www.alldatasheet.com/html-pdf/75876/MICRON/MT46H16M16LF/185/1/MT46H16M16LF.html> and <https://www.alldatasheet.com/html-pdf/75876/MICRON/MT46H16M16LF/9123/49/MT46H16M16LF.html>.
7. Hynix Semiconductor, _2Gbit Mobile DDR SDRAM_, `H5MS2G22MFR` / `H5MS2G32MFR`, Rev. 1.2, May 2009, especially feature list and Deep Power Down operation; vendor datasheet preserved by Farnell: <https://www.farnell.com/datasheets/1750885.pdf>.
