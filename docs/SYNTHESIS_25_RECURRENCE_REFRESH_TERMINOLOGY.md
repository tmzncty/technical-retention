# Synthesis 25 — Recurrence Is Not Refresh: a Terminology Boundary

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
