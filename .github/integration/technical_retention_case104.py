from pathlib import Path

case_path = Path('cases/104-micron-lpddr-selective-adaptive-self-refresh.md')
evidence_path = Path('evidence/104-micron-2009-2014-lpddr-tcsr-pasr-grounding.md')
if case_path.exists() or evidence_path.exists():
    raise SystemExit('Case/Evidence 104 already exists; refusing duplicate integration')

case = r'''# Micron LPDDR TCSR/PASR: Variable Refresh Rate and Selective Retention Scope

## Status

**`grounded`** — bounded to Micron 512Mb x16/x32 Mobile/Automotive LPDDR documentation from the 2009–2014 document family, with older TI and Toshiba patents used only as prior-art boundaries for on-chip refresh-address generation and autonomous self-refresh scheduling.

Grounding record: [`../evidence/104-micron-2009-2014-lpddr-tcsr-pasr-grounding.md`](../evidence/104-micron-2009-2014-lpddr-tcsr-pasr-grounding.md).

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

## Retained state and control state

At least four state classes must remain distinct:

1. **payload state** — charge-encoded data in DRAM cells;
2. **retention-scope policy** — PASR mode-register state selecting which regions receive maintenance;
3. **maintenance-rate control** — temperature-sensor / self-refresh-oscillator relation that determines internal cadence;
4. **power/mode state** — whether the device is in ordinary operation, self refresh, or DPD.

The project terms `retention-scope policy` and `maintenance-rate control` are engineering reconstructions, not Micron's historical vocabulary.

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
| retention coverage and ordinary addressable capacity can differ | E | bounded reconstruction from PASR semantics |
| maintenance rate and maintenance scope are independent comparison axes | E/A | bounded cross-feature comparison |
| PASR exclusion is equivalent to secure erase | X | not established; no sanitization or exact decay-completion semantics are specified |
| Micron invented adaptive/partial self refresh | X | blocked by earlier prior art and outside source scope |

## Related repositories

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated PASR/TCSR case. A full LPDDR/JEDEC refresh-feature genealogy, controller implementation history, per-bank refresh, modern retention-aware scheduling, and RowHammer-era refresh policy should be developed there if pursued broadly. This repository keeps only the bounded retention-scope/rate argument.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) remains the anti-anachronism guard: `retention-scope policy`, `maintenance-rate control`, and `selective forgetting` are present analytical terms, not vocabulary attributed to Micron engineers.

## Sources

1. Micron Technology, Inc., _512Mb: x16, x32 Automotive LPDDR SDRAM_, `t67m_embedded_lpddr_512mb.pdf`, Rev. D, February 2014, especially pp. 34, 55–56, and 90. Preserved manufacturer document via DigiKey/device-report mirrors: <https://media.digikey.com/pdf/Data%20Sheets/Micron%20Technology%20Inc%20PDFs/MT46H16M32LF%28LG%29_MT46H32M16LF.pdf> and <https://device.report/m/ee2b8a56e871864419dcf093c9a7d59531ea90387f192f2bd45316bda78a9f79>.
2. Lionel S. White, Jr. and G. R. Mohan Rao, Texas Instruments, US4207618A, _On-chip refresh for dynamic memory_, filed 26 June 1978, published 10 June 1980: <https://patents.google.com/patent/US4207618A/en>.
3. Takayasu Sakurai and Tetsuya Iizuka, Toshiba Corp., US4682306A, _Self-refresh control circuit for dynamic semiconductor memory device_, Japanese priority 20 August 1984, US publication 21 July 1987: <https://patents.google.com/patent/US4682306A/en>.
'''
case_path.write_text(case, encoding='utf-8')

evidence = r'''# Micron LPDDR 2009–2014 TCSR/PASR grounding record

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
'''
evidence_path.write_text(evidence, encoding='utf-8')

# Cross-link the immediately preceding self-refresh case without rewriting its history.
case21_path = Path('cases/21-micron-sdram-refresh-mode-handoff.md')
case21 = case21_path.read_text(encoding='utf-8')
anchor21 = 'Cases 03, 09, and 10 established the first distinctions across different historical designs. Case 21 adds a named SDRAM family in which **one device crosses between external recurring-command responsibility and internal recurring self-refresh work, then crosses back on exit**.'
addition21 = anchor21 + '\n\nCase 104 now continues this decomposition for a later Micron LPDDR family by separating **self-refresh maintenance rate** (temperature-compensated internal cadence) from **self-refresh maintenance coverage** (PASR-selected array regions). That continuation is functional and source-bounded; it does not establish a direct product genealogy.'
if case21.count(anchor21) != 1:
    raise SystemExit('Case21 cross-link anchor mismatch')
case21_path.write_text(case21.replace(anchor21, addition21, 1), encoding='utf-8')

# Add a bounded completed roadmap slice at the top of Phase 2.
roadmap_path = Path('ROADMAP.md')
roadmap = roadmap_path.read_text(encoding='utf-8')
roadmap_item = "- [x] Micron LPDDR temperature-compensated / partial-array self-refresh retention-policy boundary — [`cases/104-micron-lpddr-selective-adaptive-self-refresh.md`](cases/104-micron-lpddr-selective-adaptive-self-refresh.md), grounded by [`evidence/104-micron-2009-2014-lpddr-tcsr-pasr-grounding.md`](evidence/104-micron-2009-2014-lpddr-tcsr-pasr-grounding.md): a named 512Mb LPDDR family separates internally variable temperature-aware self-refresh cadence from PASR-selected maintenance coverage, while DPD separately removes array power. This closes only the bounded `maintenance rate vs maintenance scope` relation; full JEDEC/LPDDR genealogy, per-bank refresh, modern retention-aware scheduling, controller implementation, RowHammer-era policy, and fault injection remain open."
if '104-micron-lpddr-selective-adaptive-self-refresh.md' in roadmap:
    raise SystemExit('ROADMAP already references Case104')
phase2 = '## Phase 2 — Build missing technical bridges\n'
if roadmap.count(phase2) != 1:
    raise SystemExit('ROADMAP Phase2 anchor mismatch')
roadmap = roadmap.replace(phase2, phase2 + '\n' + roadmap_item + '\n', 1)
roadmap_path.write_text(roadmap, encoding='utf-8')

# Add Case104 to maturity table and append findings.
index_path = Path('CASE_INDEX.md')
index = index_path.read_text(encoding='utf-8')
if 'cases/104-micron-lpddr-selective-adaptive-self-refresh.md' in index or '\n1608.' in index:
    raise SystemExit('CASE_INDEX already contains Case104/findings')

# Table insertion after the Case103 row if present; otherwise after Case21 row as a guarded fallback.
lines = index.splitlines()
insert_at = None
for i, line in enumerate(lines):
    if line.startswith('| [') and 'cases/103-' in line:
        insert_at = i + 1
        break
if insert_at is None:
    for i, line in enumerate(lines):
        if line.startswith('| [') and 'cases/21-micron-sdram-refresh-mode-handoff.md' in line:
            insert_at = i + 1
            break
if insert_at is None:
    raise SystemExit('CASE_INDEX table insertion anchor not found')
row = '| [Micron LPDDR TCSR/PASR: Variable Refresh Rate and Selective Retention Scope](cases/104-micron-lpddr-selective-adaptive-self-refresh.md) | **grounded** | volatile LPDDR payload + on-die temperature-compensated self-refresh cadence + mode-register-selected partial-array maintenance coverage + separate deep-power-down forgetting boundary | separate maintenance rate from maintenance scope; addressable capacity from low-power retained set; maintenance withdrawal from explicit/secure erase; and payload from retention-policy control state | [2009–2014 Micron LPDDR TCSR/PASR grounding](evidence/104-micron-2009-2014-lpddr-tcsr-pasr-grounding.md); full JEDEC/LPDDR feature genealogy, per-bank/retention-aware refresh, controller behavior, RowHammer-era policy, and fault validation remain separate work |'
lines.insert(insert_at, row)
index = '\n'.join(lines).rstrip() + '\n'

findings = r'''

## Case 104 — Micron LPDDR TCSR/PASR findings

1608. **self refresh ≠ fixed refresh cadence** — Micron states that self-refresh intervals are scheduled internally and may vary; internal autonomy does not imply a constant interval.
1609. **ordinary `tREFI` ≠ self-refresh internal interval** — the manufacturer explicitly allows self-refresh timing to differ from the normal-operation refresh-interface cadence and forbids substituting SELF REFRESH for ordinary AUTO REFRESH.
1610. **temperature measurement ≠ payload measurement** — the on-die sensor qualifies maintenance timing, not the semantic value or correctness of individual stored words.
1611. **temperature-compensated rate ≠ disappearance of the refresh obligation** — TCSR changes how often internal maintenance runs while dynamic charge still requires restoration.
1612. **physical/addressable array capacity ≠ self-refresh retained set** — PASR permits the full array to remain normally readable/writable while only a selected subset is maintained during self refresh.
1613. **PASR coverage state ≠ user payload** — a small mode-register relation determines which much larger payload region receives future retention work.
1614. **PASR exclusion ≠ explicit erase** — the documented mechanism withdraws refresh from excluded regions; it does not specify an erase pulse or immediate physical blanking.
1615. **PASR exclusion ≠ secure sanitization** — Micron's statement that excluded data will be lost does not establish when every cell becomes unrecoverable or whether residual forensic traces are absent.
1616. **maintenance withdrawal ≠ instantaneous forgetting time** — ending refresh support removes the retention guarantee without specifying one universal moment of physical data disappearance.
1617. **TCSR rate control ≠ PASR scope control** — the two features reduce self-refresh work along different axes and can be combined without becoming the same mechanism.
1618. **PASR ≠ deep power-down** — PASR preserves selected regions through continued refresh, while DPD removes memory-array power and carries no data-retention promise.
1619. **no external clocking ≠ no temporal work** — self refresh hides recurring timing inside the device; system-level quiescence can conceal active device-local maintenance.
1620. **on-chip refresh addressing ≠ autonomous refresh scheduling** — TI's 1978-filed on-chip-refresh patent still requires an external refresh command, so address-locus migration must not be conflated with schedule-locus migration.
1621. **earlier adaptive self-refresh prior art ≠ demonstrated Micron genealogy** — Toshiba's 1984-priority self-refresh control blocks an origin claim but does not prove direct design descent into the later Micron LPDDR family.
1622. **DRAM refresh cases form a functional decomposition, not a linear invention ladder** — Cases 03/09/10/21/69/104 isolate deadline, row enumeration, autonomous scheduling, authority handoff, scheduling elasticity, rate adaptation, and scope selection without asserting that the cases form one historical lineage.
'''
index = index.rstrip() + findings + '\n'
index_path.write_text(index, encoding='utf-8')
