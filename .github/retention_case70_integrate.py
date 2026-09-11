from pathlib import Path

case_path = Path('cases/70-magnetic-core-half-select-disturbance.md')
roadmap_path = Path('ROADMAP.md')
index_path = Path('CASE_INDEX.md')
evidence_path = Path('evidence/70-papian-1952-half-select-disturbance-facsimile-deepening.md')

assert evidence_path.exists(), 'new evidence file missing'

section = '''## Direct Papian facsimile deepening (1952)

The original grounding used MIT's preserved abstract to establish repeated `nonselecting` disturbance as a retention criterion. Direct inspection of the article facsimile now closes that evidence debt; see [`../evidence/70-papian-1952-half-select-disturbance-facsimile-deepening.md`](../evidence/70-papian-1952-half-select-disturbance-facsimile-deepening.md).

The full article adds three boundaries that the abstract alone could not safely support:

- Papian's disturbed-ONE test inserts a large number of **half-amplitude nonselecting pulses** between write and read, while pulse **amplitude, length, spacing, and count are independently variable**;
- repeated nonselecting excitation can move a satisfactory core toward an **asymptotic** disturbed operating point, but the same paper separately requires adequate **disturbed-signal ratio**, so bounded excursion does not itself prove safe readout;
- disturbance can make the ONE output smaller and the ZERO output larger; an over-large magnetizing amplitude can drive their disturbed-signal ratio close to one.

The engineering reconstruction is therefore stricter than `half-select count causes bit flips`:

```text
half-select exposure
!=
one scalar access count

asymptotic disturbed state
!=
adequate discrimination margin

state not fully reversed
!=
state unaffected
!=
symbol reliably recoverable
```

Papian's best metallic test core is reported with disturbed-signal ratio `13`, nonselecting-signal ratio `16`, and about `25 µs` ONE response time. These are bounded experimental results for that tested material and pulse regime, **not universal production-machine limits**.

This direct facsimile strengthens the existing functional analogy to RowHammer/NAND disturbance only at the abstract level of `non-target operation can burden retained state`; it does not establish mechanism identity, quantitative portability, or genealogy.

---

'''

case = case_path.read_text()
if '70-papian-1952-half-select-disturbance-facsimile-deepening.md' not in case:
    marker = '\n---\n\n## Historical record\n'
    assert case.count(marker) == 1, 'historical-record insertion marker changed'
    case = case.replace(marker, '\n---\n\n' + section + '## Historical record\n', 1)

ledger_anchor = '| Repeated nonselecting disturbance was treated as an information-retention criterion | H/P | direct in Papian 1952 abstract preserved by MIT |\n'
ledger_extra = '''| Papian's disturbance test independently varied pulse amplitude, length, spacing, and pulse count | H/P | direct in 1952 facsimile; detailed in Case-70 facsimile evidence |
| Repeated disturbance approaching an asymptotic operating point does not by itself establish adequate read discrimination | H/P + E | facsimile asymptote discussion plus disturbed-signal-ratio criterion |
| A too-large magnetizing amplitude can drive disturbed ONE/ZERO outputs toward a ratio close to one | H/P | direct in 1952 facsimile |
'''
if ledger_extra.strip() not in case:
    assert case.count(ledger_anchor) == 1, 'claim-ledger anchor changed'
    case = case.replace(ledger_anchor, ledger_anchor + ledger_extra, 1)

old_status = 'The case is deliberately narrower than Case 02 and the `computing-archaeology` core-memory history. Remaining work is archival deepening: direct line-by-line facsimile inspection of the full Papian article and additional named-machine quantitative margin measurements if later synthesis requires exact pulse/amplitude numbers.'
new_status = 'The case is deliberately narrower than Case 02 and the `computing-archaeology` core-memory history. Direct line-by-line Papian facsimile inspection is now recorded in [`../evidence/70-papian-1952-half-select-disturbance-facsimile-deepening.md`](../evidence/70-papian-1952-half-select-disturbance-facsimile-deepening.md). Remaining work is narrower archival/production deepening: named-machine quantitative margins, deployed-material distributions, temperature dependence, and invention-priority genealogy if later synthesis requires them.'
if old_status in case:
    case = case.replace(old_status, new_status, 1)
else:
    assert new_status in case, 'evidence-status wording changed unexpectedly'
case_path.write_text(case)

roadmap = roadmap_path.read_text()
roadmap_bullet = '''- [x] **Case 70 deepening — Papian 1952 direct-facsimile half-select disturbance / signal-margin boundary** — [`cases/70-magnetic-core-half-select-disturbance.md`](cases/70-magnetic-core-half-select-disturbance.md), deepened by [`evidence/70-papian-1952-half-select-disturbance-facsimile-deepening.md`](evidence/70-papian-1952-half-select-disturbance-facsimile-deepening.md): direct inspection of Papian's April-1952 IRE facsimile closes the abstract-only evidence debt, grounding repeated half-amplitude nonselecting-pulse tests, independently variable pulse amplitude/length/spacing/count, asymptotic disturbed operating points, disturbed-ONE / disturbed-ZERO signal convergence, and the observed collapse of disturbed-signal ratio toward unity under excessive magnetizing amplitude. This closes the bounded `pulse count != complete disturbance history`, `asymptotic disturbance != safe discrimination`, and `state not fully reversed != symbol reliably recoverable` seams without generalizing tested-core ratios to production machines or claiming RowHammer/NAND mechanism identity or genealogy. Named-machine quantitative margins, material/temperature distributions, production correspondence, and invention-priority history remain open and belong primarily in `computing-archaeology`.
'''
if 'Case 70 deepening — Papian 1952 direct-facsimile' not in roadmap:
    rmarker = '### Recent bounded evidence deepening\n\n'
    assert roadmap.count(rmarker) == 1, 'roadmap recent-deepening marker changed'
    roadmap = roadmap.replace(rmarker, rmarker + roadmap_bullet, 1)
roadmap_path.write_text(roadmap)

idx = index_path.read_text()
old_row = '| [Coincident-Current Magnetic Core Half-Select Disturbance: State Margin, Partial-Select Output, and Inhibit Control](cases/70-magnetic-core-half-select-disturbance.md) | **grounded** | remanent ferrite payload + coordinate half-select excitation + repeated nonselecting-disturbance margin + shared sense-line partial-select outputs + inhibit-qualified write transitions | separate logical nonselection from physical excitation; state disturbance from sense/readout disturbance; target address from physical effect scope; word selection from bit write authorization | [1951–1959 half-select grounding](evidence/70-core-1951-1959-half-select-grounding.md); full Papian facsimile numeric margins, named production-machine measurements, and invention-priority study remain separate archival work |'
new_row = '| [Coincident-Current Magnetic Core Half-Select Disturbance: State Margin, Partial-Select Output, and Inhibit Control](cases/70-magnetic-core-half-select-disturbance.md) | **grounded** | remanent ferrite payload + coordinate half-select excitation + repeated nonselecting-disturbance margin + shared sense-line partial-select outputs + inhibit-qualified write transitions | separate logical nonselection from physical excitation; state disturbance from sense/readout disturbance; target address from physical effect scope; word selection from bit write authorization | [1951–1959 half-select grounding](evidence/70-core-1951-1959-half-select-grounding.md) + [Papian 1952 direct-facsimile deepening](evidence/70-papian-1952-half-select-disturbance-facsimile-deepening.md); named production-machine measurements, deployed-material/temperature distributions, and invention-priority study remain separate archival work |'
if old_row in idx:
    idx = idx.replace(old_row, new_row, 1)
else:
    assert new_row in idx, 'Case 70 index row changed unexpectedly'

findings = '''
- **3482 — H/P:** MIT Libraries' Project Whirlwind record identifies William N. Papian's `A Coincident-Current Magnetic Memory Cell for the Storage of Digital Information` as an April-1952 _Proceedings of the I.R.E._ reprint and exposes the direct facsimile used in the Case-70 deepening.
- **3483 — H/P:** Papian's full article states that repeated `H_M/2` nonselecting read pulses applied to a stored ONE can move its operating point and disturb or destroy the information; a satisfactory hysteresis loop instead approaches a disturbed asymptotic position near the original remanent state.
- **3484 — H/P:** The facsimile distinguishes `undisturbed ONE/ZERO` from `disturbed ONE/ZERO`; repeated nonselecting read pulses usually reduce the later ONE output, while repeated nonselecting write-ONE pulses usually increase the later ZERO output.
- **3485 — H/P:** Papian defines the `disturbed-signal ratio` as disturbed-ONE output divided by disturbed-ZERO output and treats a value much greater than one as necessary for reasonable binary discrimination; retained state quality is therefore tested through output separation as well as flux state.
- **3486 — H/P:** Papian separately defines a `nonselecting signal ratio` comparing disturbed-ONE output with output caused by a nonselecting pulse itself, making partial-select readout noise an explicit experimental criterion.
- **3487 — H/P:** Papian's disturbed-state test independently varies pulse amplitude, pulse length, pulse spacing, and the number of intervening half-amplitude nonselecting pulses.
- **3488 — E:** `half-select exposure != one scalar pulse count`; for the bounded Papian experiment, equivalent counts can represent different disturbance histories when amplitude, width, spacing, starting state, sequence, or hysteresis behavior differs.
- **3489 — H/P:** With an over-large magnetizing-force amplitude in Papian's ferrite test, disturbed-ZERO output increases while disturbed-ONE output decreases, producing an unsatisfactory disturbed-signal ratio close to one.
- **3490 — E:** `disturbance approaches an asymptote != binary discrimination remains adequate`; bounded magnetic-state excursion still has to satisfy the separately measured signal-ratio criterion.
- **3491 — H/P:** Papian's best metallic test core is reported with disturbed-signal ratio `13`, nonselecting-signal ratio `16`, and about `25 microseconds` ONE response time; these are bounded experimental results, not universal production limits.
- **3492 — E:** `state not fully reversed != state unaffected != symbol reliably recoverable`; Case 70 now separates retained polarity, disturbance margin/operating point, and recoverable readout discrimination.
- **3493 — A:** Cases 52, 53, and 59 remain bounded functional comparisons only: NAND read disturb, DRAM RowHammer, NAND program interference, and core half-select disturbance share the abstract pattern that operations targeting one state can burden another, but their substrates, excitation mechanisms, thresholds, and maintenance responses differ.
- **3494 — I:** Project interpretation only: technical forgetting may begin as loss of distinguishability before complete disappearance or inversion of the physical retained state; this is not Papian's historical vocabulary.
- **3495 — X:** No claim is made that all half-selected cores eventually flip, that one universal pulse threshold exists, that Papian's tested ratios describe every production machine, that an asymptotic state is automatically safe, that core disturbance is the ancestor of RowHammer/NAND disturb, or that any disturbed state constitutes sanitization.
'''
if '**3482 — H/P:**' not in idx:
    assert '**3481 — X:**' in idx, 'expected current finding 3481 missing'
    idx = idx.rstrip() + '\n' + findings + '\n'
index_path.write_text(idx)

for p in (case_path, roadmap_path, index_path, evidence_path):
    assert p.exists() and p.stat().st_size > 0, p
print('Case 70 integration patch prepared')
