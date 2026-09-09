# Delay-line recirculation, DRAM regeneration, and `refresh` terminology (1947–1976)

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
