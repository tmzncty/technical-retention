from pathlib import Path
import re

ROOT = Path('.')

EVIDENCE = ROOT / 'evidence/01-03-1947-1976-recirculation-regeneration-refresh-terminology.md'
SYNTH = ROOT / 'docs/SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md'

EVIDENCE_TEXT = r'''# Delay-line recirculation, DRAM regeneration, and `refresh` terminology (1947–1976)

**Related cases:** [`01 — Mercury delay-line circulation`](../cases/01-mercury-delay-line-circulation.md), [`03 — DRAM scheduled restoration`](../cases/03-dram-refresh-as-scheduled-restoration.md)  
**Purpose:** close the bounded terminology question `recurrence` versus `refresh` without turning a cross-case analogy into a false historical vocabulary or genealogy.  
**Evidence range:** 1947–1976, with one 1973 public patent publication used as a terminology floor and a 1976 manufacturer data book used as a commercial-product vocabulary anchor.

This file is not a general history of delay-line memory or DRAM. The broader delay-line engineering history already belongs in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-memory-was-a-tube-of-sound.md). The retention-specific question here is narrower:

> when several technologies repeatedly produce a usable successor to an earlier physical state, when is it defensible to call that operation `refresh`, and when is `recurrence` only a later analytical description of logical identity across repeated re-instantiation?

---

## 1. Source A — Eckert and Mauchly, US2629827A, 1947-filed / 1953-published

J. Presper Eckert Jr. and John W. Mauchly, **“Memory system,”** US2629827A, filed 31 October 1947, published 24 February 1953.

- HTML: <https://patents.google.com/patent/US2629827A/en>
- PDF: <https://patentimages.storage.googleapis.com/f7/97/cd/c2e4049f574d4d/US2629827.pdf>

The directly inspected patent language is strong enough to keep the historical term separate from later DRAM vocabulary.

### 1.1 The source says `circulation`, `recirculation`, and repetition of the cycle

The patent describes coded pulses that circulate through a path, are taken from the path, and are transmitted back to the input for **repetition of the cycle**. It also describes **continuous recirculation** of all or part of the circulating pattern.

Printed cols. 3–4 and the Figure-1 discussion additionally tie the loop to:

- pulse reforming;
- pulse retiming;
- erasure;
- pulse insertion / substitution;
- indexed control of portions of the circulating pattern.

These are historical/source terms and mechanisms, not a modern recoding of delay-line memory as DRAM.

### 1.2 `Refresh` is not the term established by this inspected patent

A text search of the inspected Google Patents transcription returns no `refresh` occurrence. That negative check is useful only at a bounded level:

> **the inspected Eckert–Mauchly patent does not give this repository a historical basis for calling its continuous pulse loop `refresh`.**

It does **not** prove that no delay-line engineer ever used the word elsewhere, and it is not an invention-priority or first-usage claim.

### 1.3 Retention-specific reconstruction

Case 01 can legitimately reconstruct the mechanism as a recurring production of corrected successor pulse patterns. But the historical record should still say `recirculation`, `repetition`, `reforming`, and `retiming` where those are the source terms.

Thus:

> **logical recurrence is an engineering/interpretive description of what recirculation accomplishes, not a replacement historical noun for the apparatus.**

---

## 2. Source B — Dennard, US3387286A, 1967-filed / 1968-issued

Robert H. Dennard, **“Field-effect transistor memory,”** US3387286A, filed 14 July 1967, issued 4 June 1968.

- <https://patents.google.com/patent/US3387286A/en>

Dennard gives a different maintenance relation. Charge stored on the cell capacitance leaks with time, so the information must be **periodically regenerated**. The patent describes regeneration by recurring cycles or by periodically reading and rewriting word positions. The regeneration interval depends on capacitance, leakage paths, and temperature.

The same patent separately says that the Figure-1 read is destructive and that information must be rewritten if it is to remain retained.

This establishes two distinct trigger relations before later project terminology is applied:

```text
selected destructive access
    -> rewrite / restore obligation

elapsed time + leakage
    -> periodic regeneration obligation
```

Dennard's historical term in the inspected passages is `regenerate` / `regeneration`. The repository should not silently rewrite every occurrence as `refresh`, even though later DRAM sources make `refresh` normal vocabulary.

---

## 3. Source C — General Instrument, US3765003A, 1973 public `data refresh` witness

J. Paivinen, R. Rubinstein, L. Cohen, and L. Baker, **“Read-write random access memory system having single device memory cells with data refresh,”** US3765003A, published 9 October 1973. Google Patents records a priority lineage to 21 March 1969 and the displayed continuation application filing on 13 November 1972.

- <https://patents.google.com/patent/US3765003A/en>

The public patent title itself contains **`data refresh`**. The description uses `refresh`, `refreshing`, `refresh amplifier`, and `data refresher`, and explains that capacitive stored levels tend to drain/leak and therefore need refreshing. It also describes row-associated refreshing during read operations.

For this repository the safe terminology conclusion is only:

> **`refresh` is directly attested in a public semiconductor-memory patent publication by 1973.**

Do not turn the 1969 priority lineage into a 1969 public-disclosure date. Do not claim that this patent coined `refresh`, invented dynamic-memory maintenance, or supplied a direct genealogy into every later DRAM product.

This source is useful precisely because it prevents a false binary in which `regeneration` belongs to the 1960s and `refresh` suddenly appears only in late-1970s product manuals. Public terminology overlaps and changes before the AMD witness below.

---

## 4. Source D — AMD Am9050, 1976 commercial-product `REFRESH` vocabulary

Advanced Micro Devices, **1976 AMD MOS/LSI Data Book**, `Am9050 — 4096-Bit Dynamic R/W Random Access Memory`.

- <https://www.bitsavers.org/components/amd/_dataBooks/1976_AMD_MOS_LSI_Data_Book.pdf>

Printed p. 3-13 has an explicit **`REFRESH`** section. AMD says information is stored as presence or absence of charge, that leakage eventually drains charge, and that data loss is prevented by restoring the charge level before too much leaks away. Each cell must be refreshed at least once every **2 ms** worst case; cycling a location in a row refreshes all 64 cells in the row, so all 64 row addresses must be accessed within the interval.

This is a strong commercial manufacturer anchor for the narrower technical meaning used in Case 03:

```text
bounded charge-retention interval
    + leakage risk
    + restoration before data loss
    = manufacturer-described DRAM refresh relation
```

It is not evidence that `refresh` always means exactly this mechanism in Flash, storage controllers, filesystems, or distributed systems.

---

## 5. Historical vocabulary timeline — bounded, not a coinage claim

| Date | Source | Directly grounded vocabulary | What may safely be inferred |
| --- | --- | --- | --- |
| 1947 filing / 1953 publication | Eckert–Mauchly delay-line patent | `circulate`, `continuous recirculation`, repetition of the cycle, reforming, retiming | delay-line retention was described as a circulating/repeating process; this source does not ground retroactive `refresh` terminology |
| 1967 filing / 1968 issue | Dennard dynamic-memory patent | `periodically regenerate`, regeneration, rewrite after destructive read | leakage-driven periodic maintenance and access-triggered restoration were already technically distinct in the invention disclosure |
| 1973 publication | General Instrument US3765003A | `data refresh`, `refreshing`, `refresh amplifier`, `data refresher` | public semiconductor-memory `refresh` vocabulary exists no later than this publication; no first-coinage claim |
| 1976 product data book | AMD Am9050 | `REFRESH`, refreshed, 2 ms requirement | `refresh` is explicit commercial DRAM operating vocabulary tied to a leakage/restoration deadline |

The table is deliberately not a universal terminology genealogy. A first-use claim would require a dedicated search across patents, technical reports, vendor manuals, committee material, and non-US literature.

---

## 6. Engineering reconstruction — why `recurrence` and `refresh` answer different questions

The cases expose three distinct analytical axes:

1. **identity relation:** does a later physical state count as the same logical retained value?
2. **maintenance trigger:** what makes preservation work due?
3. **response mechanism:** what operation is performed when work is due?

`Recurrence` is useful only on the first axis. It describes a retained logical relation in which an equivalent state appears again across a sequence of physical events or successor embodiments.

`Refresh` normally belongs on the third axis and, in bounded DRAM evidence, is tied to the second: leakage plus an elapsed-time requirement makes restoration due.

Therefore:

> **recurrence ≠ refresh**

and:

> **a refresh can produce recurrence, but recurrence does not tell us that the response was refresh or why it occurred.**

### Delay line

The state exists through continuing propagation and recirculation. There is no long quiescent cell waiting for a refresh deadline in the bounded mechanism.

### DRAM

A charge state can remain locally quiescent between restoration events, but leakage creates a deadline. Refresh periodically reconstructs usable levels before that deadline.

### Magnetic-core destructive read

A selected state may be remanently stable at rest yet require rewrite/restore after destructive access. That can also be described as logical state re-instantiation, but calling it `refresh` would erase the access-triggered mechanism and the historical `Read/Regenerate` / rewrite vocabulary.

These examples are enough to reject `recurrence` as a synonym for `refresh`.

---

## 7. Functional analogy boundary

A bounded functional analogy is valid:

> delay-line recirculation, DRAM refresh, destructive-read restore, some Flash renewal, and some reconstruction paths can all preserve a logical relation by producing a successor physical embodiment rather than leaving one original token untouched.

But that shared function does **not** establish:

- identical trigger conditions;
- identical physical mechanisms;
- a historical lineage;
- shared period vocabulary;
- identical failure semantics;
- one universal maintenance cadence.

Synthesis 24 already supplies the stronger engineering discipline: classify the trigger/obligation relation first. `Recurrence` must not be used to undo that decomposition.

---

## 8. Philosophical interpretation boundary

Case 01's phrase **`retention as recurrence`** remains useful, but only as an explicitly analytical/philosophical proposition:

> persistence can consist in the successful production of state-equivalent successors rather than in the untouched survival of one physical token.

That proposition asks an identity question: what invariant makes repeated successors count as the same retained value?

It does not justify the stronger claims that:

- all retention is recurrence;
- all recurrence is periodic;
- all technical repetition is memory;
- every recurrent maintenance operation is `refresh`;
- historical actors possessed this repository's philosophical category.

The phrase therefore remains downstream of mechanism and source vocabulary.

---

## 9. Terminology decision

**Decision:** retain `recurrence` in the controlled glossary only as an **analytical descriptor of identity across repeated re-instantiation**, not as a maintenance-mechanism class and not as a historical synonym for `refresh`.

`Refresh` remains source-sensitive and mechanism-sensitive. Use it when:

- the historical/technical source itself uses `refresh`; or
- an engineering reconstruction is explicitly scoped to a mechanism whose ordinary technical description is restoration/renewal before a bounded retention/reliability loss.

Do not use `refresh` merely because a process repeats.

Do not use `recurrence` to infer the maintenance trigger. For trigger classification, use the regime vocabulary in [`SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md`](../docs/SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md).

---

## 10. Related-repository boundary

`tmzncty/computing-archaeology` already has the broader delay-line mechanism/history article:

- <https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-memory-was-a-tube-of-sound.md>

A fresh repository search found no dedicated cross-technology `recurrence` versus `refresh` terminology study to reuse. If a full history of `refresh` terminology, semiconductor-memory naming, or delay-line regeneration vocabulary is later pursued, the historical genealogy should primarily live there. `technical-retention` keeps only this retention-specific terminology boundary.

---

## 11. Open limits

This slice does **not** close:

- first coinage of `refresh` in computer-memory engineering;
- first use of `recurrence` or analogous philosophical vocabulary in media theory;
- full patent genealogy between early dynamic-memory refresh designs;
- non-US / non-English terminology;
- modern vendor uses of `refresh` in NAND/SSD products;
- whether a future mechanism requires a more specific identity-through-reinstantiation term.

Those remain separate research questions.
'''

SYNTH_TEXT = r'''# Synthesis 25 — Recurrence Is Not Refresh: a Terminology Boundary

> **Roadmap question:** does `recurrence` deserve a controlled term distinct from `refresh`?

**Status:** bounded terminology synthesis grounded in Cases 01 and 03 plus the new [`1947–1976 terminology evidence`](../evidence/01-03-1947-1976-recirculation-regeneration-refresh-terminology.md). It resolves a project-vocabulary question; it does not claim a historical lineage or invention priority.

## 1. Verdict

Yes — but only under a narrow rule.

> **`Recurrence` may be used as a project analytical descriptor for identity across repeated re-instantiation. It is not a maintenance mechanism, not a trigger regime, and not a historical synonym for `refresh`.**

`Refresh` remains a source-sensitive technical term for a maintenance response that restores/renews retained state. In the bounded DRAM evidence it is tied to leakage and an elapsed-time requirement; in other technologies the source must establish what `refresh` means there.

The distinction matters because otherwise a seductive sentence — “the state comes back, therefore it was refreshed” — collapses several different relations.

```text
identity relation:
    what makes a later successor count as the same retained value?

trigger relation:
    what makes preservation work due?

response relation:
    what operation is performed when it becomes due?
```

`Recurrence` addresses the first question. `Refresh` usually names an operation on the third, and its trigger must still be separately reconstructed.

---

## 2. Historical vocabulary comes first

The primary-source sequence blocks retroactive vocabulary flattening.

- **Eckert–Mauchly, 1947-filed / 1953-published:** the delay-line patent says pulses `circulate`, undergo `continuous recirculation`, return for repetition of the cycle, and are reformed/retimed. The inspected transcription does not establish `refresh` as this source's term.
- **Dennard, 1967-filed / 1968-issued:** the dynamic-memory patent says charge leakage makes it necessary to **periodically regenerate** stored information and separately describes rewrite after destructive read.
- **General Instrument, public 1973 patent:** US3765003A explicitly uses `data refresh`, `refreshing`, `refresh amplifier`, and `data refresher`; this is a public semiconductor-memory terminology floor, not a first-coinage claim.
- **AMD, 1976 product data book:** the Am9050 has an explicit `REFRESH` section and a worst-case two-millisecond row-coverage requirement tied to charge leakage.

This chronology is deliberately modest. Historical vocabulary overlaps. A later familiar word must not overwrite an earlier source's own mechanism language.

---

## 3. Case comparison

| Case | What persists? | What repeats? | What makes work due? | Period/source vocabulary | Project use of `recurrence` |
| --- | --- | --- | --- | --- | --- |
| Mercury delay line | coded pulse pattern | propagation → sensing → reforming/retiming → recirculation | continuing loop is constitutive | circulation / recirculation / repetition | useful analytical descriptor of logical identity across successor pulses |
| DRAM elapsed-time maintenance | logical cell/row values | sense/amplify/restore cycles | leakage + refresh deadline | regeneration; later `refresh` | refresh can instantiate recurrence, but recurrence does not define the deadline |
| Classic destructive-read core | remanent logical bit | selected-state rewrite/restore after read | destructive access | read/regenerate / rewrite in bounded sources | state re-instantiation is comparable, but `refresh` would misname the trigger |

The table shows why a single repetition word cannot replace mechanism reconstruction.

---

## 4. Controlled glossary rule

### `recurrence`

Use only when the analytical point is:

> a later physical event/state is treated as a state-equivalent successor to an earlier one, so logical persistence does not require one untouched physical token.

Do **not** infer from `recurrence`:

- periodic timing;
- a decay deadline;
- refresh authority;
- a particular physical substrate;
- a historical term;
- a direct genealogy.

### `refresh`

Use as a source-sensitive technical operation. A refresh claim should identify, where the evidence permits:

- target retained state;
- deterioration/risk being answered;
- trigger or deadline;
- restoration operation;
- scope/granularity;
- authority/controller responsible;
- completion/admissibility condition.

Do not use `refresh` as the repository's umbrella noun for every repeated preservation action.

---

## 5. Relation to Synthesis 24

[`Synthesis 24`](SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md) classifies **what makes retention work due**. It already distinguishes continuous maintenance, access-triggered restoration, deadline-driven maintenance, capacity/reclaim pressure, wear/lifetime policy, and failure/repair triggers.

Synthesis 25 adds a different axis:

> **recurrence describes possible identity continuity across successive embodiments; it does not classify the trigger.**

Therefore:

- delay-line recurrence can occur under **continuous maintenance**;
- core-state recurrence can occur under **access-triggered restoration**;
- DRAM recurrence can occur under **deadline-driven refresh**;
- reconstruction/relocation can sometimes produce a successor embodiment under **failure**, **capacity**, or other triggers.

This yields a useful guardrail:

> **same identity-through-reinstantiation pattern ≠ same maintenance regime.**

---

## 6. Why `refresh` cannot be inferred from repetition

Repeated preservation can have very different causes.

A delay-line pulse is reformed because the loop itself is the store. A core value is rewritten because reading disturbed the selected magnetic state. A DRAM row is restored because leakage creates a bounded deadline. Flash data may be relocated because free-space reclamation is due, or rewritten because retention/error evidence calls for renewal. RAID data may be reconstructed because a member failed.

All of these may produce a successor physical embodiment.

Only some sources call the operation `refresh`.

Thus:

> **repeated successor production ≠ refresh by definition.**

And, following Synthesis 24:

> **response name ≠ trigger regime.**

---

## 7. `Recurrence` does not mean history retention

Case 01 already supplies the decisive counterexample. A delay-line bit pattern returns cycle after cycle, but this does not preserve all earlier machine states. Once a bit is changed, the new recurring pattern replaces the old one unless another mechanism records history.

Therefore:

> **state recurrence ≠ history retention.**

The same caution applies to refresh. Repeatedly restoring the current value does not automatically create a log of earlier values.

---

## 8. `Recurrence` does not require carrier identity

The term is useful precisely because it permits physical-token discontinuity.

In a delay line, sensing/reforming/retiming produces corrected successor pulses. In a DRAM restore, a decayed electrical state is driven back toward a usable level. In reconstruction or migration, a logical relation may survive in an entirely different embodiment.

The invariant has to be stated at the right layer:

```text
physical token identity
    may change

logical/state relation
    may remain admissibly equivalent
```

But equivalence is system-specific. `Same bit value`, `same object version`, `same logical block`, and `same reconstructed coded object` are not one universal identity test.

---

## 9. Historical and prior-art boundary

The newly inspected terminology sequence supports only bounded chronology:

- a 1947-filed delay-line design explicitly uses circulation/recirculation/repetition language;
- Dennard's 1967-filed DRAM disclosure uses periodic regeneration;
- a public 1973 semiconductor-memory patent explicitly uses `data refresh`;
- a 1976 AMD product manual uses `REFRESH` as an operating requirement.

It does **not** support:

- first coinage of `refresh`;
- invention priority for refresh;
- a direct Eckert → Dennard → General Instrument → AMD genealogy;
- the claim that earlier engineers lacked equivalent concepts under other words.

Chronology constrains vocabulary claims; it does not manufacture descent.

---

## 10. Functional analogy and philosophy

### Functional analogy

A bounded cross-case analogy survives:

> several retention mechanisms preserve a logical relation by repeatedly producing state-equivalent successors.

That analogy is useful for comparing identity across physical change. It is not evidence of shared architecture or history.

### Philosophical interpretation

`Retention as recurrence` can remain a productive philosophical phrase for asking:

> when does repeated re-production count as persistence of the same retained thing?

But the philosophy must remain downstream of the engineering decomposition. The term cannot erase the difference between continuous circulation, access repair, deadline refresh, capacity relocation, and failure reconstruction.

The strongest surviving philosophical claim is narrow:

> **technical persistence can sometimes preserve identity through controlled succession rather than through untouched carrier endurance.**

Nothing in this synthesis shows that all memory, all persistence, or all repetition has that structure.

---

## 11. Usage checklist

Before writing `recurrence`, ask:

1. What state-equivalence relation is recurring?
2. Are the physical tokens actually being replaced/re-instantiated, or merely left unchanged?
3. Is this source vocabulary, engineering reconstruction, or philosophical interpretation?
4. What separately triggers the maintenance, if any?
5. Would a more precise source term — `recirculation`, `regeneration`, `rewrite`, `refresh`, `reconstruction`, `migration` — be better?

Before writing `refresh`, ask:

1. Does the source use the term, or is the engineering mapping explicitly justified?
2. What degradation/risk is being answered?
3. What makes the work due?
4. What is restored and at what granularity?
5. Does completion restore current correctness, future margin, or both?

---

## 12. Related repositories and open work

`computing-archaeology` already owns the broader engineering history of mercury delay lines. This synthesis does not duplicate it. A future full genealogy of `refresh`, `regeneration`, `restore`, and related memory-maintenance vocabulary should also primarily live there.

Open questions remain:

- first public and first technical-community use of `refresh` for memory;
- non-English terminology and standards vocabulary;
- how NAND/SSD vendors repurpose `refresh` for controller-mediated renewal;
- whether `recurrence` remains useful once more migration, coding, and archival cases are compared.

For now, the roadmap terminology question is closed at the bounded project-vocabulary level.
'''


def write_new(path: Path, text: str):
    if path.exists():
        raise SystemExit(f'{path} already exists; refusing to overwrite')
    path.write_text(text.rstrip() + '\n', encoding='utf-8')


def replace_once(path: Path, old: str, new: str):
    text = path.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected exactly one replacement anchor, found {count}')
    path.write_text(text.replace(old, new, 1), encoding='utf-8')


write_new(EVIDENCE, EVIDENCE_TEXT)
write_new(SYNTH, SYNTH_TEXT)

# Refine controlled vocabulary without making recurrence a maintenance regime.
glossary = ROOT / 'docs/GLOSSARY.md'
old_refresh = '''## refresh

Periodic restoration required because the physical state would otherwise decay or become unreliable.

Refresh is not merely maintenance performed after failure. In some systems it is **constitutive of ordinary persistence**.
'''
new_refresh = '''## refresh

A source-sensitive technical term for restoration / renewal used to keep retained state recoverable or reliable. In the bounded DRAM evidence, leakage creates an elapsed-time obligation and `refresh` restores charge/state before the service deadline is missed.

Do **not** use `refresh` as an umbrella for every preservation action that repeats. Delay-line recirculation, destructive-read core rewrite, Flash reclamation, scrub, reconstruction, migration, and rebuild have their own mechanisms and trigger relations unless a source independently calls a bounded operation `refresh`.

Refresh is not merely maintenance performed after failure. In some systems it is **constitutive of ordinary persistence**. A refresh claim should still identify its target, trigger/deadline, scope, authority, and completion condition where the evidence permits.

See [`SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md`](SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md).

## recurrence

A project analytical descriptor for **identity across repeated re-instantiation**: a later physical event or embodiment is treated as a state-equivalent successor to an earlier one even though one untouched physical token need not survive.

`Recurrence` is **not** a maintenance-mechanism class, not a trigger regime, and not historical vocabulary to project onto every source. It can describe the logical relation produced by delay-line recirculation, DRAM restoration, destructive-read rewrite, or some reconstruction/migration cases while leaving their triggers and mechanisms distinct.

Therefore:

- recurrence does not imply periodic timing;
- recurrence does not imply a decay deadline;
- recurrence does not imply `refresh`;
- recurrence does not imply history retention;
- recurrence does not establish genealogy or shared period vocabulary.

Use the source's own term (`recirculation`, `regeneration`, `rewrite`, `refresh`, `reconstruction`, etc.) for historical claims, and use `recurrence` only when the analytical question is what makes successive physical realizations count as the same retained state.

See [`SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md`](SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md).
'''
replace_once(glossary, old_refresh, new_refresh)

# Close the explicit open terminology item in the Case-01 grounding record.
ev01 = ROOT / 'evidence/01-mercury-delay-line-1947-1958-grounding.md'
old_ev01 = '- decide separately whether `recurrence` deserves a controlled-vocabulary entry distinct from `refresh`;'
new_ev01 = '- the `recurrence` versus `refresh` terminology question is now closed at the bounded project-vocabulary level by [`Synthesis 25`](../docs/SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md): `recurrence` is an analytical identity-through-re-instantiation descriptor, not a historical synonym for `refresh`;'
replace_once(ev01, old_ev01, new_ev01)

# README navigation: keep this in the synthesis/audit cluster rather than expanding the huge case list.
readme = ROOT / 'README.md'
readme_text = readme.read_text(encoding='utf-8')
nav_line = '- [`docs/SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md`](docs/SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md) — bounded terminology synthesis separating identity-through-re-instantiation (`recurrence`) from source-sensitive maintenance operations (`refresh`), grounded by 1947–1976 delay-line/DRAM primary vocabulary and explicitly rejecting a shared-mechanism or genealogy claim.\n'
anchor = '- [`docs/SYNTHESIS_COUNTEREXAMPLE_LEDGER.md`](docs/SYNTHESIS_COUNTEREXAMPLE_LEDGER.md)'
if nav_line.strip() in readme_text:
    raise SystemExit('README already contains Synthesis 25 navigation')
if anchor not in readme_text:
    raise SystemExit('README synthesis navigation anchor not found')
readme.write_text(readme_text.replace(anchor, nav_line + anchor, 1), encoding='utf-8')

# ROADMAP: replace the unique recurrence/refresh open question regardless of nearby wording.
roadmap = ROOT / 'ROADMAP.md'
road_text = roadmap.read_text(encoding='utf-8')
lines = road_text.splitlines()
candidates = [i for i, line in enumerate(lines) if 'recurrence' in line.lower() and 'refresh' in line.lower()]
unchecked = [i for i in candidates if '- [ ]' in lines[i]]
if len(unchecked) != 1:
    raise SystemExit(f'ROADMAP: expected one unchecked recurrence/refresh item, found {len(unchecked)}; candidates={[(i+1, lines[i]) for i in candidates]}')
i = unchecked[0]
lines[i] = '- [x] Resolve `recurrence` versus `refresh` terminology — [`docs/SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md`](docs/SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md) plus [`evidence/01-03-1947-1976-recirculation-regeneration-refresh-terminology.md`](evidence/01-03-1947-1976-recirculation-regeneration-refresh-terminology.md) reserve `recurrence` as an analytical identity-through-re-instantiation descriptor rather than a maintenance-mechanism class. Eckert–Mauchly grounds circulation/recirculation/repetition, Dennard grounds periodic regeneration, a 1973 public semiconductor-memory patent directly uses `data refresh`, and AMD 1976 grounds commercial `REFRESH` vocabulary. This closes the bounded project-vocabulary question while leaving first coinage, full terminology genealogy, non-English usage, and later NAND/SSD uses open.'
roadmap.write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')

# Append findings after the verified current tail.
index = ROOT / 'CASE_INDEX.md'
idx = index.read_text(encoding='utf-8')
if '- **2560 — related-repository boundary:**' not in idx:
    raise SystemExit('CASE_INDEX current tail 2560 not found')
if '**2561 —' in idx:
    raise SystemExit('CASE_INDEX already contains Synthesis 25 findings')
findings = r'''

## Synthesis 25 — Recurrence versus refresh terminology findings

Evidence: [`evidence/01-03-1947-1976-recirculation-regeneration-refresh-terminology.md`](evidence/01-03-1947-1976-recirculation-regeneration-refresh-terminology.md) and [`docs/SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md`](docs/SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md).

- **2561 — delay-line recirculation ≠ retroactive `refresh` vocabulary.** Eckert–Mauchly's 1947-filed patent directly uses circulation, continuous recirculation, repetition of the cycle, reforming, and retiming; the inspected transcription does not establish `refresh` as that source's term. (`H/P`, `X`)
- **2562 — negative term search ≠ universal historical absence.** No `refresh` match in the inspected patent transcription blocks a source-specific wording shortcut but does not prove that no delay-line engineer, manual, patent, or later publication ever used the word. (`H/P`, `X`)
- **2563 — Dennard periodic `regeneration` ≠ later vocabulary silently back-projected.** The 1967-filed DRAM patent grounds leakage-driven periodic regeneration and separate destructive-read rewrite before later product manuals normalize `refresh`. (`H/P`)
- **2564 — public 1973 `data refresh` witness ≠ 1969 public-disclosure date or first coinage.** US3765003A's title/text directly use refresh vocabulary when published in 1973; its recorded 1969 priority lineage must not be substituted for the publication date or inflated into an origin claim. (`H/P`, `X`)
- **2565 — AMD 1976 `REFRESH` is a commercial operating term tied to leakage and a deadline.** The Am9050 data book requires every cell to be refreshed within two milliseconds worst case and explains row-wide restoration through accesses. (`H/P`)
- **2566 — `regeneration`, `restore`, and `refresh` sharing a broad function ≠ identical historical vocabulary or mechanism.** A source term must remain attached to its bounded apparatus and period unless a separate genealogy is proven. (`H/P`, `A`, `X`)
- **2567 — recurrence ≠ refresh.** Project `recurrence` asks whether a later physical event/embodiment counts as a state-equivalent successor; `refresh` names a maintenance operation whose target and trigger still need to be reconstructed. (`E`)
- **2568 — refresh can instantiate recurrence without exhausting the recurrence category.** DRAM refresh can recreate a usable successor state, but delay-line circulation and destructive-read rewrite can also preserve identity across successive embodiments under different trigger regimes. (`E`, `A`)
- **2569 — continuous recurrence ≠ deadline-driven refresh.** In the bounded delay-line case the continuing loop constitutes the store; in bounded DRAM a locally retained charge state can sit between restorations until leakage makes work due before a deadline. (`H/P` inherited, `E`, `A`)
- **2570 — access-triggered re-instantiation ≠ elapsed-time refresh.** Classic destructive-read core can require rewrite because access disturbed the selected state even when no periodic refresh clock caused the event. (`H/P` inherited, `E`, `A`)
- **2571 — state recurrence ≠ history retention.** Reappearance of the current logical value does not preserve the sequence of earlier values; a changed delay-line pattern can recur while the prior pattern disappears unless another history mechanism exists. (`E`, `X`)
- **2572 — recurrence ≠ physical-token identity.** The descriptor is useful specifically where a logical invariant survives corrected/reconstructed successor tokens; it must not be read as evidence that one original pulse, charge packet, magnetic transition, or replica survives untouched. (`E`)
- **2573 — recurrence is not a retention-maintenance regime.** Synthesis 24 classifies what makes work due; recurrence is orthogonal identity language and cannot replace continuous/access/deadline/capacity/wear/failure trigger distinctions. (`E`)
- **2574 — analytical recurrence ≠ historical actor vocabulary.** `Retention as recurrence` remains a project engineering/philosophical interpretation and must not be attributed to Eckert, Mauchly, Dennard, AMD, or core-memory engineers unless a source independently uses the term in that sense. (`I`, `X`)
- **2575 — related-repository boundary:** `computing-archaeology` already owns the broad delay-line mechanism history and a fresh search found no dedicated cross-technology recurrence/refresh terminology study; any full word/genealogy history belongs there, while Synthesis 25 keeps only the retention-specific vocabulary boundary. (`H/P` project-state record)
'''
index.write_text(idx.rstrip() + findings.rstrip() + '\n', encoding='utf-8')

# Cheap self-checks before the workflow's git diff validation.
for p in (EVIDENCE, SYNTH):
    if not p.exists() or p.stat().st_size < 4000:
        raise SystemExit(f'{p}: missing or unexpectedly small')

idx2 = index.read_text(encoding='utf-8')
for n in range(2561, 2576):
    marker = f'**{n} —'
    if idx2.count(marker) != 1:
        raise SystemExit(f'finding {n} count is {idx2.count(marker)}')

if any('recurrence' in line.lower() and 'refresh' in line.lower() and '- [ ]' in line for line in roadmap.read_text(encoding='utf-8').splitlines()):
    raise SystemExit('ROADMAP still has an unchecked recurrence/refresh item')

print('Synthesis 25 research slice applied successfully')
