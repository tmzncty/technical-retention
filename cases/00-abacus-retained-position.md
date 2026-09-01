# Abacus as Retained Position

> **Research question:** when does a spatial configuration inside a calculation count as technical retention rather than merely as a visible aid?

**Status:** grounded case study; central late-Ming claim checked against a 1592 scan, older counting-rod evidence is explicitly layered, and a non-Chinese positional-counter comparison has been added.

Grounding record: [`../evidence/00-abacus-rod-line-reckoning-grounding.md`](../evidence/00-abacus-rod-line-reckoning-grounding.md)

## Scope

- **Primary bounded object:** the Chinese bead abacus (`算盤`, suanpan), especially Cheng Dawei's *Suanfa Tongzong* (1592).
- **Older comparison inside China:** counting-rod procedural vocabulary in early mathematical texts, treated cautiously because the surviving texts do not specify every material operation.
- **Non-Chinese comparison:** Adam Ries's *Rechnung auff der Linihen* (1525), a European line-reckoning manual using counters on a positional line schema.
- **Why this case matters:** it tests whether `technical retention` can include manually maintained, operationally meaningful physical state without quietly turning every stable object into storage or projecting modern computer architecture backward.

This case does **not** claim that an abacus or reckoning board is historically a CPU register. It asks a narrower functional question:

> Can a manually maintained spatial configuration preserve an actionable numerical state across successive operations?

The evidence supports **yes**.

---

## Claim ledger

| ID | Claim | Type | Status |
| --- | --- | --- | --- |
| A1 | Premodern arithmetic could be carried out by transforming counters or beads arranged in positional configurations. | historical record | **strong**; primary evidence in Cheng 1592 and Ries 1525 |
| A2 | Cheng Dawei's 1592 text directly uses `算盤`, gives explicit `定位` rules, and instructs that after multiplication the obtained number be left unmoved (`待數莫動`). | historical record | **strong**; 1592 scan p. 70 / 82 inspected directly |
| A3 | Older Chinese mathematical texts use procedural placement/positional language, while exact counting-rod material operations sometimes require specialist reconstruction. | historical record + scholarly reconstruction | **strong with explicit boundary** |
| A4 | A configured bead/counter field can preserve an intermediate or completed numerical state for subsequent inspection or transformation. | engineering / operational reconstruction | **strong** |
| A5 | Chinese suanpan and European line reckoning can be compared as different realizations of passive positional working retention. | functional analogy | **strong but non-genealogical** |
| A6 | Such configurations are `register-like` in the limited respect that an operational value remains available between operations. | functional analogy | useful and bounded |
| A7 | The abacus is a register, memory hierarchy, or direct ancestor of modern CPU registers. | historical claim | **rejected** |
| A8 | The evidence establishes a continuous counting-rods → suanpan → modern-register genealogy. | historical claim | **rejected** |

---

## Historical vocabulary

### Cheng Dawei: `算盤`, `定位`, and `待數莫動`

The most important rule is to begin with period vocabulary rather than with `register`, `memory`, or `state`.

Cheng Dawei's *新編直指筭法統宗* / *算法統宗* (1592) uses:

- `算盤` / `筭盤` — abacus;
- `定位` — determination/fixing of position or place value;
- `實` and `法` in procedural arithmetic contexts;
- decimal and metrological positions designated on the calculating surface.

The central primary anchor is now directly checked rather than accepted from OCR alone. In the 1592 scan, digital p. **70 / 82**, the section `直指定位訣` includes:

> `預先以算盤上寫定萬千百十...因乘完畢待數莫動`

The historically important content is narrow and concrete:

1. positions on the abacus are designated in advance;
2. multiplication is carried out under that positional convention;
3. when the multiplication is complete, the resulting number is instructed to remain unmoved.

Source:

- Cheng Dawei, *Systematic Treatise on Arithmetic*, vol. 1 (1592), Source Library scan p. 70 / 82: <https://sourcelibrary.org/book/suanfa-tongzong-systematic-treatise-on-arithmetic-vol-1-dawei/page-number/70>

This page is the exact digital anchor used by the case. A separately catalogued NLC 1592 facsimile exists, but this case does not pretend that Source Library's digital page number is automatically an NLC folio number.

### Older counting-rod vocabulary: evidence and reconstruction must remain separate

Earlier Chinese mathematical writing supplies genuine positional and procedural vocabulary, but the material instrument cannot always be read straight off the words.

In the `方程` procedure of *The Nine Chapters on Mathematical Procedures*, the text says in part:

> `置...於右方。中、左禾列如右方。`

The verbs `置` (place/set down) and `列` (arrange) and the explicit right/middle/left locations are primary evidence for a spatially organized procedure.

Searchable text:

- *九章算術*, `方程`: <https://www.shidianguji.com/zh/book/SBCK080/chapter/SBCK080_15>

Yiwen Zhu's specialist study is useful because it refuses to turn this evidence into false material certainty. Zhu notes that historians generally understand many such procedures as operations using counting rods (`筭籌`, *suan chou*) but also stresses that direct evidence for exactly how rods were manipulated is limited. The article discusses terms including:

- `筭籌` — counting rods;
- `借筭` — a borrowed counting rod in a root-extraction procedure;
- `等` — a positional/rank term whose interpretation is debated;
- `位` — place/position in *Master Sun*;
- `筭圖` — later counting diagrams.

Source:

- Yiwen Zhu, “The interplay between textual procedures and material operations from the viewpoint of Chinese mathematical texts,” *Science in Context* 36(3), published online 9 October 2025, DOI 10.1017/S0269889725100860: <https://www.cambridge.org/core/journals/science-in-context/article/interplay-between-textual-procedures-and-material-operations-from-the-viewpoint-of-chinese-mathematical-texts/7E654BC8863452F26F2E0C43892699F4>

The resulting method is deliberately layered:

- **historical record:** surviving texts explicitly tell operators to place, arrange, move, stop, or position quantities;
- **historical reconstruction:** specialist historians connect many of those procedures to counting-rod material practices;
- **rejected overreach:** the repository does not invent a fully specified marked board or an uninterrupted rod-to-abacus mechanism when the sources do not provide one.

---

## Non-Chinese comparison: Adam Ries's line reckoning

Adam Ries's *Rechnung auff der Linihen* (Erfurt, 1525) supplies an independent European comparison.

The directly inspected public-domain scan shows a positional line schema in which lines and intervening spaces carry different values, followed by the section `Addirn / odder summiren`. Counters/numerical tokens are laid out and transformed as the arithmetic proceeds.

Primary scan:

- Adam Ries, *Rechnung auff der Linihen* (1525), Columbia University / Plimpton Library copy via Wikimedia Commons / Internet Archive: <https://commons.wikimedia.org/wiki/File:Rechnung_auff_der_Linihen_(IA_ldpd_13272232_000).pdf>

Because the historical leaves are unnumbered, the grounding record uses the digital PDF image indices around **12–13** rather than inventing printed page numbers.

The Adam-Ries-Bund independently describes the method as `Rechnen auf den Linien`, with `Rechenpfennige` or stones placed on a line schema / reckoning board and transformed during calculation:

- <https://www.adam-ries-bund.de/forschung/erstes/>

This comparison establishes neither transmission nor common origin. Its value is mechanistic:

| Dimension | Cheng / suanpan | Ries / line reckoning |
| --- | --- | --- |
| physical counter | bead | loose counter / reckoning token |
| positional constraint | rods and frame strongly constrain motion | line-and-space schema constrains meaning more than movement |
| write | move beads | place/remove/convert counters |
| read | human visual/manual interpretation | human visual/manual interpretation |
| retention work | preserve bead configuration | preserve counter layout |
| autonomous machine readout | no | no |

The difference is useful. A bead frame mechanically constrains valid positions more strongly than an open reckoning board. Thus **the degree to which a medium constrains legal states** becomes a comparison axis rather than an unnoticed assumption.

---

## Retained state

The retained state is **not the bead or counter itself**. It is an interpreted relation among:

1. the physical counters;
2. their positions relative to a frame, rods, lines, spaces, or neighboring columns;
3. a place-value or metrological convention;
4. the current procedural role of the represented number.

A physical arrangement without its convention may remain perfectly intact while losing its mathematical meaning.

This case therefore grounds a stronger formulation than the first pass:

> **passive positional retention = substrate + constrained configuration + interpretation + procedural availability.**

The word `passive` refers only to the fact that the physical position need not be continually regenerated by a machine. It does **not** mean that interpretation, protection, selection, and procedural context require no work.

---

## Physical / logical substrate

### Suanpan

A bead's significance depends on its position relative to the frame, crossbar, rod/column, and the current place-value convention. Ordinary mechanical stability lets a configuration remain after the hand that produced it has stopped moving.

### Line reckoning

A loose counter's significance depends on the line or intervening space on which it lies and on the rule system used by the operator. The physical substrate constrains valid states less strongly than the suanpan: a counter can be displaced continuously across the surface even though only some placements have arithmetic meaning.

### Consequence

The same broad retention regime can therefore contain different degrees of **state constraint**:

```text
open surface + convention
        ↕
line schema + convention
        ↕
rod/frame + convention
```

This is an engineering comparison, not a historical evolutionary sequence.

---

## Retention mechanism

The state persists primarily through **passive positional stability**.

No refresh cycle, circulating signal, remanent magnetic state, charge-restoration schedule, mapping controller, or replica-repair protocol is required merely to keep the current configuration physically present.

But retention still has conditions:

- the counters must not be accidentally disturbed;
- the positional convention must remain known;
- the operator must remember what role the displayed number has in the larger procedure;
- the device or surface must remain available;
- the configuration must not be intentionally cleared.

This creates a baseline for later cases. A state can require **little or no active substrate maintenance** while still depending heavily on human and procedural maintenance.

---

## Addressing and access geometry

Both bounded examples are spatially selectable by the operator.

On the suanpan, a place is selected by reaching/looking at a rod or column. In Ries's line reckoning, value is selected/interpreted through the line-and-space geometry.

Calling this `addressability` is an engineering reconstruction, not period vocabulary. It is useful only if the human role remains visible:

- there is no address bus;
- there is no decoder;
- the operator performs selection;
- multiple positions may be inspected visually without serial electronic access.

The defensible cross-period statement is:

> **spatial selection of retained state can be a human–technical convention before it becomes an autonomous machine addressing mechanism.**

---

## Read semantics

Reading is normally **physically nondestructive**: observing a bead/counter arrangement does not require changing it.

However, readout is not autonomous. The operator supplies the interpretation. This separates two properties often collapsed in modern memory systems:

1. a physical configuration remains readable;
2. a machine can autonomously decode that configuration.

The first is sufficient for this bounded form of technical working retention; the second becomes a major difference in later machine memory.

---

## Write and erasure semantics

### Write / transformation

Writing is manual transformation of the retained configuration.

Calculation is not simply performed elsewhere and copied onto the surface. In both bounded traditions, transforming the counter field is part of the arithmetic procedure itself.

### Reset / forgetting

Clearing or moving the counters destroys the previous configuration without normally leaving a durable trace of it in the calculating surface.

Therefore:

> **state retention is not history retention.**

The device can hold the current operational state while preserving none of the sequence that produced it.

---

## Time

There is no fixed refresh deadline analogous to DRAM and no circulation period analogous to a delay line.

The practical retention interval is bounded by disturbance, procedure, and human use:

```text
operation at t0
    ↓
configuration remains physically in place
    ↓
pause / inspection / next procedural step
    ↓
configuration remains available at t1
```

This is the minimal temporal claim: an actionable state produced at one moment remains available to an operation at a later moment.

---

## Maintenance and labor

This case makes human work unusually visible. The operator may perform functions that later memory/storage systems distribute among hardware, software, controllers, firmware, metadata, and protocols:

- write or transform state;
- select a position;
- interpret a position;
- protect the current configuration from disturbance;
- validate a result;
- decide whether a displayed number is intermediate or final;
- maintain the positional convention;
- reset the representation.

The later automation of these functions should not be narrated as their disappearance. It is often a **migration of retention work** from explicit operator action into less visible technical infrastructure.

---

## Failure / forgetting modes

Even this simple regime distinguishes several failures:

1. **physical disturbance** — counters/beads move accidentally;
2. **intentional reset** — the current configuration is cleared;
3. **procedural transformation error** — the wrong counter movement creates the wrong state;
4. **interpretive loss** — the arrangement survives but its positional convention is no longer known;
5. **context loss** — the number remains readable but its role in the larger computation is forgotten;
6. **surface/device loss** — the physical configuration can no longer be preserved.

The fourth and fifth are especially important. A physical state can persist while ceasing to be operationally recoverable as **that** numerical state.

---

## Engineering / operational reconstruction

### Why `register-like` remains defensible — and narrow

A modern register normally:

- holds an operational value;
- keeps it available across a short interval;
- permits read and rewrite;
- has an identity/position within a computational system.

The bounded positional cases share some of those functions:

- **yes:** an operational numerical value is materially externalized;
- **yes:** it can survive between successive operations;
- **yes:** it can be inspected and rewritten;
- **partly:** spatial position gives numerical significance;
- **no:** there is no electronic decoder or processor-autonomous access;
- **no:** the historical sources do not use the modern architecture concept `register`;
- **no:** no direct genealogy to CPU registers has been established.

Therefore:

> **These configurations are register-like retained working state only as a functional comparison. They are not historical CPU registers.**

### The machine/non-machine boundary

Grounding this case makes one repository boundary explicit:

> **technical retention does not have to begin where autonomous machine memory begins.**

That does not mean every external mark is memory. The narrower inclusion criteria are:

- the configuration represents a state under an explicit convention;
- that configuration is part of an operational transformation procedure;
- it can remain available across a temporal gap;
- a later operation can act on or from it.

This excludes the trivial claim that every stable physical object is a storage device while retaining a meaningful pre-electronic comparison class.

---

## Philosophical / media-theoretical interpretation

### Availability without archive

The abacus and reckoning board are strong cases of **availability without archival durability**.

A number can remain immediately available for the next step but leave no durable record after the counters are moved. This requires distinctions among:

- working retention;
- session retention;
- durable record;
- archival preservation.

They are not synonyms.

### Exteriorization without autonomous readout

The retained numerical state is materially outside the operator's body, yet its readout and interpretation still depend on a trained person. This gives a more precise question for later philosophical work than simply asking whether an abacus “is memory”:

> What changes when a calculational state is exteriorized into a technical support that can survive interruption, even though the technical support cannot autonomously interpret itself?

This can later be tested against Stiegler, Ernst, and other theories of technical memory. The historical case itself does not prove that those philosophical categories were present in sixteenth-century arithmetic.

### Relation rather than isolated token

The retained thing is not identical to one physical bead/counter. Its identity depends on relations among token, position, convention, and procedure.

That prepares a comparison with later cases in which identity similarly depends on relations that become increasingly automated:

- coordinate selection in core memory;
- row/column and restore infrastructure in DRAM;
- logical-to-physical maps in Flash;
- placement/version/recovery metadata in RADOS.

The analogy is conceptual and functional, not genealogical.

---

## Counterexamples and limits

### Limit 1 — stable position is not enough

A chair retains its position too. This case belongs in the repository because the configuration participates in an explicit representational and operational convention.

### Limit 2 — the category can still become too broad

Pencil arithmetic, chess positions, slide rules, marked gauges, and mechanical indicators are neighboring cases. Their inclusion should depend on bounded research questions, not on the mere fact that they have state.

Useful comparison questions are:

- Is the configuration part of the transformation procedure?
- Can calculation resume from it after interruption?
- Is it directly actionable?
- Is it human-readable, machine-readable, or both?
- How strongly does the medium constrain legal states?

### Limit 3 — counting-rod practice is not fully visible in surviving texts

The repository must preserve Zhu's evidence warning: procedural language and later diagrams support reconstruction, but not every ancient material movement or surface marking is directly documented.

### Limit 4 — Chinese and European examples are comparison, not genealogy

Ries 1525 shows that passive positional arithmetic is not unique to the Chinese bead frame. It does **not** prove transmission, shared origin, or conceptual identity.

### Limit 5 — no modern register ancestry has been established

The functional resemblance between retained numerical position and a modern register remains a heuristic comparison only.

---

## What this grounded case establishes for the project

1. **Passive positional retention is historically real, not merely a modern metaphor.** Cheng's 1592 scan explicitly tells the operator to designate abacus positions and leave a completed number unmoved.
2. **Retention can be operational rather than archival.** A state need only remain long enough to be used again.
3. **Technical retention can precede autonomous machine readout.** Human interpretation does not make the material support irrelevant; it changes where the retention work is located.
4. **Retention is relational.** Counter + position + convention + procedural context together constitute the actionable state.
5. **Medium constraint matters.** A rod/frame constrains legal positions differently from an open line-reckoning surface.
6. **State retention is not history retention.** Clearing the configuration normally destroys its computational past.
7. **Cross-cultural similarity does not establish genealogy.** Cheng and Ries support a functional class while remaining historically distinct.
8. **`register-like` remains disciplined only when explicitly labeled as analogy.**

The methodological result is now grounded strongly enough to close the repository's passive-position mechanism gate:

> **Ancient or pre-electronic retained states can be compared with modern machine state without pretending that their users were secretly doing computer architecture.**

---

## Related repositories

A repository search found no existing bounded treatment of `abacus`, `suanpan`, or `counting rod` in the current related repositories.

### `computing-archaeology`

Use for broader engineering histories and later machine-autonomous memory mechanisms:

- <https://github.com/tmzncty/computing-archaeology>

### `problem-history`

Use its anti-anachronism discipline when reconstructing what historical actors themselves understood the problem to be:

- <https://github.com/tmzncty/problem-history>

### `mechanical-computing-playground`

Future physical/software demonstrations of passive positional retention belong there if experiment becomes the main contribution:

- <https://github.com/tmzncty/mechanical-computing-playground>

---

## Sources

### Primary / digitized primary

1. Cheng Dawei (程大位), *算法統宗* / *新編直指筭法統宗*, vol. 1 (1592), Source Library digital scan, especially p. 70 / 82, `直指定位訣`: <https://sourcelibrary.org/book/suanfa-tongzong-systematic-treatise-on-arithmetic-vol-1-dawei/page-number/70>
2. Cheng Dawei, *新編直指筭法統宗*, NLC 1592 volume catalogued through Wikimedia Commons: <https://commons.wikimedia.org/wiki/File:NLC892-411999021914-37275_%E6%96%B0%E7%B7%A8%E7%9B%B4%E6%8C%87%E7%AE%97%E6%B3%95%E7%B5%B1%E5%AE%97_%E7%AC%AC1%E5%86%8A.pdf>
3. *九章算術*, `方程`, searchable historical-text transcription: <https://www.shidianguji.com/zh/book/SBCK080/chapter/SBCK080_15>
4. Adam Ries, *Rechnung auff der Linihen* (Erfurt, 1525), Columbia University / Plimpton Library copy: <https://commons.wikimedia.org/wiki/File:Rechnung_auff_der_Linihen_(IA_ldpd_13272232_000).pdf>

### Scholarly / institutional

5. Yiwen Zhu, “The interplay between textual procedures and material operations from the viewpoint of Chinese mathematical texts,” *Science in Context* 36(3), published online 9 October 2025, DOI 10.1017/S0269889725100860: <https://www.cambridge.org/core/journals/science-in-context/article/interplay-between-textual-procedures-and-material-operations-from-the-viewpoint-of-chinese-mathematical-texts/7E654BC8863452F26F2E0C43892699F4>
6. Adam-Ries-Bund, “1. Rechenbuch — Rechnung auff der Linihen”: <https://www.adam-ries-bund.de/forschung/erstes/>
7. Smithsonian Institution / National Museum of American History, “The Abacus and the Numeral Frame”: <https://www.si.edu/spotlight/the-abacus-the-numeral-frame-and-counters/introduction>
8. National Museum of American History, “The Chinese Abacus”: <https://americanhistory.si.edu/collections/object-groups/the-abacus-the-numeral-frame-and-counters/the-chinese-abacus>
9. British Museum, Chinese abacus object record: <https://www.britishmuseum.org/collection/object/A_1909-0611-1>
10. Frank J. Swetz, “Reflections on Chinese Numeration Systems: Transition to the Abacus,” Mathematical Association of America, *Convergence*: <https://old.maa.org/press/periodicals/convergence/reflections-on-chinese-numeration-systems-transition-to-the-abacus>

---

## Further maturation work

The case is now `grounded`; further work should be archival/comparative cleanup rather than a condition of its central claim:

- compare multiple editions of *Suanfa Tongzong* and record traditional folio anchors where possible;
- inspect specialist work by Needham, Pullan, Martzloff, Chemla, and Chinese/Japanese historians against newer scholarship;
- broaden the comparative set only if a new case changes the mechanism boundary rather than adding another example;
- decide at the synthesis stage whether `working retention`, `passive positional retention`, and `human-mediated addressability` deserve controlled-vocabulary status.
