from pathlib import Path

case_path = Path('cases/105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md')
evidence_path = Path('evidence/105-micron-2014-2015-lpddr2-per-bank-refresh-grounding.md')
if case_path.exists() or evidence_path.exists():
    raise SystemExit('Case/Evidence 105 already exists; refusing duplicate integration')

case = r'''# Micron LPDDR2 Per-Bank REFRESH: Maintenance Granularity, Full-Array Obligation, and Service Concurrency

## Status

**`grounded`** — bounded to Micron Mobile LPDDR2 manufacturer documentation from 2014–2015, especially the 168-ball single-channel family, with no invention-priority or complete JEDEC-genealogy claim.

Grounding record: [`../evidence/105-micron-2014-2015-lpddr2-per-bank-refresh-grounding.md`](../evidence/105-micron-2014-2015-lpddr2-per-bank-refresh-grounding.md).

## Scope

Cases 03, 09, 10, 21, 69, and 104 already separate the DRAM refresh deadline, refresh-row enumeration, autonomous scheduling, maintenance-authority handoff, bounded timing elasticity, and self-refresh rate/coverage policy. Case 104 leaves one specific normal-operation question open:

> What changes when one refresh transaction can target **one bank** while the device still owes a recurring refresh obligation across the full bank set?

The bounded object here is Micron's Mobile LPDDR2 `REFpb` / `REFab` contract. The main primary witness is Micron's _168-Ball, Single-channel Mobile LPDDR2 SDRAM_, Rev. A (July 2014), supplemented by a December 2014 automotive LPDDR2 document as a same-manufacturer continuity check.

This case is not a general LPDDR2 or JEDEC history. It does not establish who invented per-bank refresh, when the feature first entered a normative standard, or how every controller scheduled it.

## Historical record

### H/P — Micron names per-bank refresh as a concurrency feature

The July 2014 Micron datasheet lists `8 internal banks for concurrent operation` and `Per-bank refresh for concurrent operation` among the product features. In the REFRESH-command section, Micron distinguishes:

- `REFpb` — a per-bank refresh operation;
- `REFab` — an all-bank refresh operation.

For the documented eight-bank devices, the per-bank sequence is a fixed round-robin over banks 0 through 7. The controller must track which bank is being refreshed, and the bank count can be synchronized to zero by RESET or on exit from self refresh.

This is manufacturer interface vocabulary. `maintenance granularity`, `refresh debt`, and `retained set` below are project-level engineering terms.

### H/P — One target bank is unavailable while other banks may remain in service

Micron states that the target bank is inaccessible for the per-bank refresh cycle time `tRFCpb`. Other banks, however, remain addressable during that interval and may stay active or receive READ/WRITE commands.

When the REFpb cycle completes, the affected bank returns to the idle state. A target bank must have been idle before the REFpb operation begins.

Thus the documented maintenance event can temporarily withdraw service from one bank without imposing a whole-device service blackout.

### H/P — Per-bank transaction scope does not remove the full refresh obligation

The same datasheet defines a minimum number `R` of refresh commands inside each rolling refresh window `tREFW`. For devices supporting per-bank refresh, Micron states that one REFab can be replaced by **a full cycle of eight REFpb commands**.

This is the decisive retention boundary. A single-bank maintenance transaction is not permission to preserve only one bank. The smaller transaction scope is nested inside a continuing coverage obligation over the bank set and rolling refresh window.

### H/P — All-bank refresh and per-bank refresh are not command-identical

REFab requires all banks to be idle and refreshes all banks together. It also synchronizes the controller/device bank count to zero. REFpb instead targets the bank selected by the device's fixed bank counter and permits activity in the non-target banks.

The fact that eight REFpb commands can replace one REFab for the documented refresh-accounting requirement therefore does not make the two command forms operationally identical.

## Retained state and control state

At least four state classes must remain distinct:

1. **payload state** — charge-encoded user data in the DRAM arrays;
2. **maintenance-coverage obligation** — the requirement that sufficient refresh work occur across the rolling refresh window;
3. **bank-target tracking state** — the controller/device relation identifying which bank the next REFpb affects;
4. **service/admission state** — whether the target and non-target banks can accept ordinary accesses during the maintenance interval.

Only the first class is user payload. The other relations help determine whether and when that payload remains maintainable and serviceable.

## Engineering reconstruction

### E — Maintenance transaction scope is not the same thing as retained-set scope

Case 104's PASR can deliberately shrink the subset promised retention in self refresh. REFpb does something different: it shrinks the **scope of one refresh transaction** while the rolling-window requirement still composes those transactions into full-bank maintenance coverage.

> **maintenance transaction scope ≠ retained set**

and, more specifically:

> **REFpb ≠ PASR**.

### E — Localized maintenance can coexist with service concurrency

During `tRFCpb`, the target bank is unavailable while other banks remain usable. The system therefore exposes a three-way distinction:

```text
payload retained in a bank
    !=
bank currently undergoing maintenance
    !=
bank currently admissible for ordinary service
```

Temporary service withdrawal for one bank is not evidence that its data have been forgotten, and concurrent service from another bank is not evidence that the target bank has completed its refresh work.

### E — One refresh event does not discharge the whole refresh obligation

A single REFpb is a completed maintenance transaction for one target bank, but the documented refresh contract is expressed over a rolling window and, for the eight-bank substitution, a complete bank cycle.

> **one completed REFpb ≠ full-array refresh obligation satisfied**.

This matters for retention analysis because `maintenance completed` requires a typed scope and accounting horizon.

### E — Scheduling state can be retention infrastructure

The controller's obligation to track the per-bank sequence is not user data, yet loss or desynchronization of that relation would undermine correct future maintenance scheduling. REFab/RESET/self-refresh-exit synchronization therefore concerns a small control relation whose correctness helps preserve a much larger volatile payload.

This does not establish how the bank counter is physically implemented or retained inside every controller/device.

### E — Scheduling flexibility does not abolish deadlines

Micron permits distributed/burst refresh patterns under explicit rolling-window conditions. Per-bank granularity creates additional scheduling freedom and concurrency, but the minimum refresh requirement remains.

> **more scheduling freedom ≠ maintenance optionality**.

## Contrast with Case 104

Cases 104 and 105 are intentionally adjacent because they expose two superficially similar but technically different meanings of `partial` maintenance:

```text
Case 104 — PASR
    changes which regions are promised maintenance in self refresh
    excluded regions may lose data

Case 105 — REFpb
    changes which bank one normal-operation refresh transaction services
    repeated transactions still satisfy a full-bank rolling-window obligation
```

Thus `partial-array retention` and `per-bank maintenance transaction` must not be collapsed into a single idea of partial refresh.

## Prior-art boundary

This case establishes a dated **Micron product-document floor no later than July 2014** for the bounded LPDDR2 REFpb semantics described above. It makes no claim that Micron originated the mechanism or term.

A complete history would require revision-by-revision JEDEC evidence, earlier vendor/product documents, controller implementations, and cross-vendor comparison. That broader engineering genealogy belongs primarily in `computing-archaeology` if pursued.

## Functional analogy and philosophical limit

A functional analogy to rotating maintenance windows is useful: maintenance can be localized so that other regions remain available. The analogy stops at the engineering relation. A DRAM bank is not an archival collection, REFpb does not perform cultural selection, and bank scheduling supplies no evidence for a philosophical theory of memory or forgetting by itself.

The bounded conceptual result is narrower:

> apparent continuous availability can depend on maintenance whose **transaction scope is local** while whose **retention obligation is global over time**.

## Cross-case result

The DRAM refresh decomposition can now be extended without turning it into a historical ladder:

```text
Case 03   leakage creates a refresh deadline
Case 09   refresh-row enumeration can move on-chip
Case 10   refresh scheduling can become autonomous and condition-derived
Case 21   recurring refresh responsibility can hand off between controller and SDRAM
Case 69   external refresh issue time can have bounded scheduling elasticity
Case 104  self-refresh cadence and retained coverage can vary independently
Case 105  one refresh transaction can be bank-local while the rolling retention obligation remains bank-complete
```

This is a functional decomposition, not a proof of direct genealogy.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| the bounded Micron LPDDR2 family exposes separate REFpb and REFab operations | H/P | Micron Rev. A 07/14, REFRESH-command section |
| REFpb targets one bank selected by a fixed round-robin bank counter | H/P | Micron printed p. 81 |
| the controller must track the bank being refreshed | H/P | Micron printed p. 81; automotive Rev. B 12/14 continuity |
| the REFpb target bank is inaccessible during `tRFCpb` while other banks may be read/written | H/P | Micron printed p. 82 |
| one REFab can be replaced by a full cycle of eight REFpb commands for the documented refresh requirement | H/P | Micron printed p. 83 |
| per-bank transaction scope is equivalent to PASR retention-scope reduction | X | contradicted by the documented full-cycle refresh accounting and Case 104 PASR semantics |
| one completed REFpb proves the whole array is freshly maintained | X | outside command scope; rolling/full-cycle requirement remains |
| Micron invented per-bank refresh in 2014 | X | not established; this is only a dated manufacturer-product witness |

## Related repositories

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated LPDDR2 REFpb / per-bank-refresh case. Full JEDEC chronology, earlier per-bank-refresh prior art, controller scheduling history, and cross-vendor implementation should be developed there if pursued broadly. This repository keeps the bounded retention relation between maintenance-event scope, full-bank coverage, and service concurrency.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) remains the anti-anachronism guard: `maintenance transaction scope`, `refresh debt`, and `retained set` are present analytical terms, not vocabulary attributed to Micron engineers.

## Sources

1. Micron Technology, Inc., _168-Ball, Single-channel Mobile LPDDR2 SDRAM_, `168b_12x12_4-16gb_2e0e_lpddr2.pdf`, Rev. A, July 2014, especially printed pp. 1 and 81–83. Manufacturer PDF preserved by Mouser: <https://www.mouser.com/datasheet/2/671/168b_12x12_4%2016gb_2e0e_mobile%20lpddr2-1283387.pdf>.
2. Micron Technology, Inc., _1Gb: x16, x32 Automotive Mobile LPDDR2 SDRAM_, `1gb_mobile_lpddr2_u88m_ait_aat.pdf`, Rev. B, December 2014, especially printed pp. 55–56 and refresh-requirement tables. Manufacturer text preserved by DTSheet: <https://dtsheet.com/doc/1384685/1gb--x16--x32-automotive-lpddr2-sdram>.
'''
case_path.write_text(case, encoding='utf-8')

evidence = r'''# Micron 2014–2015 LPDDR2 per-bank REFRESH grounding record

This record grounds [`../cases/105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md`](../cases/105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md).

The question is deliberately narrow: can a DRAM refresh transaction be localized to one bank while the retention obligation still covers the full bank set over time, and how does that differ from Case 104's PASR reduction of the retained set?

## Source A — Micron 168-ball single-channel Mobile LPDDR2, Rev. A 07/14

Micron Technology, Inc., _168-Ball, Single-channel Mobile LPDDR2 SDRAM_, PDF ID `09005aef85c99ac2`, filename `168b_12x12_4-16gb_2e0e_lpddr2.pdf`, Rev. A, July 2014.

Manufacturer PDF mirror:
<https://www.mouser.com/datasheet/2/671/168b_12x12_4%2016gb_2e0e_mobile%20lpddr2-1283387.pdf>

The direct PDF text and exact printed-page locations were inspected. Page-image rendering was also attempted in the research environment but the remote cache did not return the page images, so this record does not claim figure-level visual inspection.

### A1. Feature-level scope

**Printed p. 1.**

The feature list gives `8 internal banks for concurrent operation` and `Per-bank refresh for concurrent operation`, while ATCSR, PASR, and DPD are listed as separate features.

This immediately blocks a vocabulary collapse:

> per-bank refresh ≠ PASR ≠ self refresh ≠ DPD.

### A2. REFpb target selection and controller tracking

**Printed p. 81.**

Micron says REFpb performs a per-bank refresh on the bank scheduled by an internal bank counter. For this eight-bank device family, the sequence is fixed round-robin `0-1-2-3-4-5-6-7-...`.

The bank count can be synchronized between controller and SDRAM by resetting it to zero, including through RESET or exit from self refresh. Micron explicitly requires the controller to track the bank being refreshed.

This supports a bounded maintenance-control relation:

> maintenance target tracking state ≠ payload state.

It does not expose the physical implementation of the counter or controller bookkeeping.

### A3. Target-bank unavailability and non-target concurrency

**Printed p. 82.**

Micron states that the target bank is inaccessible during `tRFCpb`, while other banks remain accessible/addressable. Non-target banks may remain active or receive READ/WRITE commands. After the REFpb cycle, the affected bank is idle.

This directly grounds:

- bank-local maintenance ≠ whole-device service blackout;
- target-bank maintenance interval ≠ target-bank ordinary-service interval;
- service availability of non-target banks ≠ completion of target-bank maintenance.

The idle precondition is a command-admission rule, not evidence that the target bank contains no data.

### A4. REFab and bank-count synchronization

**Printed p. 82.**

REFab applies refresh to all banks, requires all banks idle, and synchronizes the bank count between controller and SDRAM to zero.

This establishes that REFab and REFpb differ in service/admission geometry even when later refresh accounting can substitute a complete REFpb cycle for one REFab.

### A5. Rolling-window refresh obligation and full REFpb cycle

**Printed p. 83.**

Micron defines a minimum number `R` of REFab commands within any rolling refresh window `tREFW`. For devices supporting per-bank refresh, it states that one REFab may be replaced by a **full cycle of eight REFpb commands**.

That sentence is the central evidence for Case 105:

> per-bank maintenance-event granularity ≠ partial retained-set policy.

A single REFpb covers one target maintenance event; the refresh obligation composes a sequence of such events across banks and time.

The same section also permits burst/distributed refresh scheduling under window constraints. This supports scheduling elasticity but not unlimited postponement.

## Source B — Micron 1Gb Automotive Mobile LPDDR2, Rev. B 12/14

Micron Technology, Inc., _1Gb: x16, x32 Automotive Mobile LPDDR2 SDRAM_, PDF ID `09005aef85d5f0c6`, filename `1gb_mobile_lpddr2_u88m_ait_aat.pdf`, Rev. B, December 2014.

Text-preserving mirror:
<https://dtsheet.com/doc/1384685/1gb--x16--x32-automotive-lpddr2-sdram>

The refresh-command section repeats the controller-tracking requirement: the controller must track the bank being refreshed by REFpb; the bank count can be synchronized to zero through RESET or exit from self refresh. The document also retains bank-idle and `tRFCpb`/`tRFCab` separation constraints.

Use of Source B is conservative. It is a same-manufacturer product-family continuity check, not an independent lab validation and not evidence of invention priority.

## Relation to Case 104

Case 104 grounds PASR in a later Micron LPDDR family as a **retention coverage** policy: in self refresh, excluded regions are not refreshed and their data are not promised survival.

Source A grounds REFpb as a **maintenance transaction** policy: one bank is refreshed per transaction, but a complete eight-bank cycle substitutes for one all-bank refresh in the rolling refresh accounting.

Therefore:

```text
PASR
    selected maintained set can shrink

REFpb
    one maintenance transaction can shrink in spatial scope
    while aggregate bank coverage remains required
```

The words `partial` and `per-bank` are not interchangeable descriptions of one retention mechanism.

## Source hierarchy and limitations

| Claim | Label | Locator | Strength |
| --- | --- | --- | --- |
| Micron markets per-bank refresh as supporting concurrent operation | H/P | Source A, printed p. 1 | strong manufacturer-primary |
| REFpb follows a fixed eight-bank round-robin target sequence | H/P | Source A, printed p. 81 | strong manufacturer-primary |
| controller tracks the bank being refreshed | H/P | Source A, p. 81; Source B, p. 55 | strong manufacturer-primary, same-vendor corroboration |
| target bank unavailable while other banks may be READ/WRITE-accessed | H/P | Source A, printed p. 82 | strong manufacturer-primary |
| REFab refreshes all banks and resynchronizes bank count | H/P | Source A, printed p. 82 | strong manufacturer-primary |
| one REFab can be replaced by a full cycle of eight REFpb commands | H/P | Source A, printed p. 83 | strong manufacturer-primary |
| transaction scope and retained-set scope are different relations | E | bounded reconstruction from A3/A5 + Case 104 | strong mechanism inference |
| Micron/2014 originated per-bank refresh | X | not established | rejected |
| REFpb and PASR are historically/mechanically identical | X | contradicted by source semantics | rejected |

## Historical cautions

- The main source is a genuine Micron manufacturer PDF preserved by Mouser; the mirror is not independent validation.
- A precise July 2014 product-document witness is not an origin date.
- No complete JEDEC revision chronology is reconstructed here.
- `REFpb cycle completion` must be scoped to one maintenance transaction, not promoted to a whole-array correctness certificate.
- Bank-count synchronization is maintenance bookkeeping, not proof that every payload bit is correct or newly restored.
- The controller-tracking obligation does not tell us how every shipping controller represented or persisted that state.
- Functional similarity to later DDR/LPDDR per-bank/same-bank refresh does not establish direct genealogy.

## Related-repository check

A current GitHub search of `tmzncty/computing-archaeology` for LPDDR2 `REFpb` / `per-bank refresh` did not expose a dedicated case. A full standards genealogy, earlier vendor prior art, controller scheduling implementation, power/performance modeling, and later per-bank/same-bank-refresh evolution belong there if developed comprehensively.
'''
evidence_path.write_text(evidence, encoding='utf-8')

# Cross-link the adjacent PASR/TCSR case without rewriting its history.
case104_path = Path('cases/104-micron-lpddr-selective-adaptive-self-refresh.md')
case104 = case104_path.read_text(encoding='utf-8')
anchor104 = "A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated PASR/TCSR case. A full LPDDR/JEDEC refresh-feature genealogy, controller implementation history, per-bank refresh, modern retention-aware scheduling, and RowHammer-era refresh policy should be developed there if pursued broadly. This repository keeps only the bounded retention-scope/rate argument."
replacement104 = "A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated PASR/TCSR or LPDDR2 REFpb case. [`Case 105`](105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md) now handles the bounded per-bank-refresh transaction-granularity boundary, which is deliberately distinct from Case 104's retained-coverage policy. A full LPDDR/JEDEC refresh-feature genealogy, controller implementation history, modern retention-aware scheduling, and RowHammer-era refresh policy should be developed there if pursued broadly."
if case104.count(anchor104) != 1:
    raise SystemExit('Case104 related-repo anchor mismatch')
case104_path.write_text(case104.replace(anchor104, replacement104, 1), encoding='utf-8')

# Update Phase 2 roadmap: mark the bounded per-bank relation closed while preserving broad genealogy as open.
roadmap_path = Path('ROADMAP.md')
roadmap = roadmap_path.read_text(encoding='utf-8')
if '105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md' in roadmap:
    raise SystemExit('ROADMAP already references Case105')
lines = roadmap.splitlines()
idxs = [i for i, line in enumerate(lines) if '104-micron-lpddr-selective-adaptive-self-refresh.md' in line]
if len(idxs) != 1:
    raise SystemExit(f'ROADMAP Case104 item count mismatch: {len(idxs)}')
i = idxs[0]
old = lines[i]
needle = 'full JEDEC/LPDDR genealogy, per-bank refresh, modern retention-aware scheduling, controller implementation, RowHammer-era policy, and fault injection remain open.'
if needle not in old:
    raise SystemExit('ROADMAP Case104 open-work phrase mismatch')
lines[i] = old.replace(needle, 'full JEDEC/LPDDR genealogy, modern retention-aware scheduling, controller implementation, RowHammer-era policy, and fault injection remain open; the bounded per-bank-refresh transaction slice is now handled separately by Case 105.')
new_item = "- [x] Micron LPDDR2 per-bank REFRESH transaction-granularity / service-concurrency boundary — [`cases/105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md`](cases/105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md), grounded by [`evidence/105-micron-2014-2015-lpddr2-per-bank-refresh-grounding.md`](evidence/105-micron-2014-2015-lpddr2-per-bank-refresh-grounding.md): a July 2014 Micron LPDDR2 product contract makes one bank unavailable during `REFpb` while other banks remain serviceable, yet requires a full cycle of eight REFpb commands to substitute for one all-bank refresh in rolling refresh accounting. This closes only the bounded `maintenance transaction scope vs retained set` relation and the REFpb/PASR distinction; complete JEDEC genealogy, earlier vendor prior art, cross-vendor semantics, controller implementation, later per-bank/same-bank refresh evolution, and fault injection remain open."
lines.insert(i + 1, new_item)
roadmap_path.write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')

# Add Case105 to the maturity table and append findings 1623–1635.
index_path = Path('CASE_INDEX.md')
index = index_path.read_text(encoding='utf-8')
if 'cases/105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md' in index or '\n1623.' in index:
    raise SystemExit('CASE_INDEX already contains Case105/findings')
lines = index.splitlines()
insert_at = None
for j, line in enumerate(lines):
    if line.startswith('| [') and 'cases/104-micron-lpddr-selective-adaptive-self-refresh.md' in line:
        insert_at = j + 1
        break
if insert_at is None:
    raise SystemExit('CASE_INDEX Case104 table row not found')
row = '| [Micron LPDDR2 Per-Bank REFRESH: Maintenance Granularity, Full-Array Obligation, and Service Concurrency](cases/105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md) | **grounded** | volatile LPDDR2 payload + bank-local REFpb maintenance transaction + rolling full-bank refresh obligation + controller/device bank-target tracking + non-target service concurrency | separate maintenance-event scope from retained-set scope; distinguish REFpb from PASR; local maintenance completion from full refresh accounting; target-bank unavailability from device-wide availability | [2014–2015 Micron LPDDR2 per-bank REFRESH grounding](evidence/105-micron-2014-2015-lpddr2-per-bank-refresh-grounding.md); complete JEDEC/origin genealogy, controller implementations, cross-vendor semantics, later same-bank evolution, and fault validation remain separate work |'
lines.insert(insert_at, row)
index = '\n'.join(lines).rstrip() + '\n'

findings = r'''

## Case 105 — Micron LPDDR2 per-bank REFRESH findings

1623. **maintenance transaction scope ≠ retained-set scope** — REFpb services one bank per transaction, while the documented rolling refresh accounting still composes a full eight-bank cycle; a bank-local operation does not define a bank-local retention promise.
1624. **per-bank REFRESH ≠ partial-array self refresh** — Case 105 REFpb changes normal-operation maintenance granularity, whereas Case 104 PASR can withdraw self-refresh maintenance from selected regions and cease promising their data retention.
1625. **one completed REFpb ≠ full-array refresh obligation satisfied** — `tRFCpb` completion returns one affected bank to idle; the broader refresh requirement remains expressed over repeated commands and the rolling refresh window.
1626. **eight REFpb commands substituting for one REFab in refresh accounting ≠ command-semantic identity** — REFab requires all banks idle and refreshes them together, whereas REFpb permits ordinary access to non-target banks.
1627. **target-bank maintenance ≠ whole-device service blackout** — Micron explicitly permits other banks to remain active or accept READ/WRITE commands during the target bank's `tRFCpb` interval.
1628. **non-target-bank availability ≠ target-bank availability** — concurrent service elsewhere in the device does not imply that the bank currently being refreshed can accept ordinary access.
1629. **bank-idle refresh precondition ≠ data absence** — `idle` is a command/admission state required before refresh; it is not evidence that the bank contains no retained payload.
1630. **bank-target tracking state ≠ user payload** — the controller/device bank counter relation identifies future maintenance targets but does not encode the application's stored words.
1631. **bank-count synchronization ≠ payload correctness certificate** — resetting the REFpb counter through REFab/RESET/self-refresh exit repairs target-sequence alignment, not the semantic correctness of every stored bit.
1632. **per-bank scheduling flexibility ≠ unlimited refresh postponement** — Micron permits concurrency and different refresh patterns while retaining minimum rolling-window requirements.
1633. **refresh-command completion ≠ application durability/currentness closure** — REFpb/REFab maintain volatile-cell charge; they do not by themselves establish filesystem/database durability, coherence, or application-level currentness.
1634. **July 2014 Micron documentation ≠ invention priority or complete JEDEC genealogy** — the source establishes a dated product-contract floor only; earlier normative/vendor history remains open.
1635. **Cases 104/105 form a functional decomposition, not a genealogy** — maintenance **coverage policy** (PASR) and maintenance **transaction granularity** (REFpb) are separable axes even within one vendor's LPDDR families; similarity does not prove historical descent or identical implementation.
'''
index_path.write_text(index.rstrip() + findings + '\n', encoding='utf-8')
