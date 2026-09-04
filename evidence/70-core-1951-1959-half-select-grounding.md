# Case 70 Grounding Record — Coincident-Current Core Half-Select Disturbance, 1951–1959

## Purpose

This record grounds [`../cases/70-magnetic-core-half-select-disturbance.md`](../cases/70-magnetic-core-half-select-disturbance.md).

The bounded question is not `how did magnetic-core memory work?` That engineering/history account already exists in Case 02 and in `tmzncty/computing-archaeology`.

The narrower question is:

> **What contemporary evidence shows that non-target cores could be physically excited during coordinate selection, that repeated nonselecting pulses were a retention criterion, and that partial-select output could disturb the shared readout even without a stable-state reversal?**

The case is promoted directly to `grounded` because the central distinction is triangulated across three contemporary primary-source lines.

---

## Source A — Jay W. Forrester, U.S. Patent 2,736,880

- **Title:** `Multicoordinate Digital Information Storage Device`
- **Inventor:** Jay W. Forrester
- **Application date:** 1951-05-11
- **Issue date:** 1956-02-28
- **Primary source:** https://patents.google.com/patent/US2736880A/en
- **Evidence role:** coordinate-selection mechanism and below-threshold / partial-select semantics.

### What the source establishes

The patent claims a multi-coordinate storage/selection system using elements with substantially rectangular hysteresis behavior.

Several claims are especially important for this case:

- one coordinate energization can be sufficient to effect a **partial change of state**;
- coincidental energization of the selected coordinate combination drives the chosen element above the level needed for a stable-state transfer;
- unselected elements that share one energized coordinate remain below that stable-switching level;
- another claim describes below-threshold excitation as having substantially no effect **after being removed**;
- the two-dimensional magnetic-core claim describes row and column wires in which either one produces partial change and the simultaneous row/column excitation switches the intersection.

### Retention interpretation allowed

This supports:

> `logical nonselection ≠ zero physical excitation`

and:

> `selected address ≠ complete physical effect scope`.

It also shows that material threshold behavior is part of the selection mechanism rather than an incidental property added after logical decoding.

### What it does not establish

It does not by itself prove:

- one universal half-select current ratio for every production memory;
- one universal number of nonselecting pulses that causes failure;
- that normal half selection permanently corrupts neighboring bits;
- that the Forrester patent settles every magnetic-memory priority dispute.

The Google Patents text is an OCR/HTML transcription of the patent. The argument uses clear claim-level mechanism, not typographic details that would require trusting a garbled OCR fragment.

---

## Source B — William N. Papian, _Proceedings of the I.R.E._, April 1952

- **Title:** `A Coincident-Current Magnetic Memory Cell for the Storage of Digital Information`
- **Author:** William N. Papian
- **Publication:** _Proceedings of the I.R.E._, vol. 40, no. 4, April 1952
- **Institutional record:** MIT Libraries / Project Whirlwind Reports
- **Source:** https://dome.mit.edu/handle/1721.3/40248
- **Evidence role:** explicit contemporary retention vocabulary under repetitive nonselecting disturbance.

### What the MIT record establishes

MIT's record preserves the article metadata and abstract. The abstract states that:

- a ring-shaped ferromagnetic core with suitable rectangular B-H characteristics reverses flux polarity only under the correct coincident combination;
- a usable core must retain a large percentage of remanent flux of the proper polarity despite repeated **`nonselecting` disturbances**;
- repetitive pulse-pattern testing was used to obtain quantitative **`information-retention ratios`** and **`signal ratios`**;
- only some core materials satisfied those requirements.

### Retention interpretation allowed

This is unusually direct primary evidence that early coincident-current memory designers treated retention not only as idle remanence but as survival under repeated normal array traffic.

It supports:

> `quiescent remanence ≠ disturbance immunity`

and:

> `repetitive nonselecting-pulse testing ≠ static shelf-retention testing`.

### Evidence boundary

This run uses the MIT institutional **abstract** as inspected evidence. It does not claim line-by-line inspection of the complete 1952 article.

Therefore this record does not attach:

- numerical information-retention ratios;
- exact pulse amplitudes;
- exact tested material compositions;
- full-paper figure or page claims not present in the inspected abstract.

Those would require direct full-facsimile inspection in a later archival slice.

---

## Source C — Bauer and Haynes, U.S. Patent 2,889,540

- **Title:** `Magnetic Memory System with Disturbance Cancellation`
- **Inventors:** Edwin W. Bauer and Munro K. Haynes
- **Assignee:** International Business Machines Corporation
- **Application date:** 1954-07-14
- **Issue/publication date:** 1959-06-02
- **Primary source:** https://patents.google.com/patent/US2889540A/en
- **Evidence role:** half-selected-core sense disturbance, shared-winding aggregation, cancellation, inhibit, and amplifier-recovery effects.

### Dating rule

This is treated as a **1954-filed design record published in 1959**.

The later issue date must not be silently rewritten as proof that every detail was publicly available in 1954. Conversely, the filing date is relevant evidence that the engineering problem and claimed design existed in the application by July 1954.

### What the patent establishes

The patent says that:

- partially excited cores can contribute `disturbance signals`;
- those contributions may prevent reliable one/zero recognition;
- cancellation is aimed specifically at disturbance from `half selected cores` during readout;
- in a unipolar sense arrangement, half-selected cores on the selected row/column contribute to the shared output signal;
- an opposing voltage can be introduced to cancel those contributions;
- inhibit and post-write-disturb pulses can also create undesirable amplifier effects;
- a described three-coordinate arrangement uses X/Y to select a word line while a Z inhibit force prevents selected bit positions from changing.

### Retention interpretation allowed

This directly grounds the separation:

> `state preservation ≠ zero sense-line contribution`

and supports the engineering reconstruction:

> `recoverability failure can occur in the readout path even when the intended remanent payload remains intact`.

It also supports a bounded distinction between:

- word/address selection;
- bit-level transition authorization through inhibit.

### What it does not establish

The patent does not prove:

- universal adoption of this exact cancellation circuit;
- that every half-selected output corresponds to permanent magnetic-state corruption;
- that every historical core-memory architecture used the same inhibit geometry;
- commercial reliability statistics for a named deployed machine.

---

## Related-repository duplication check

The companion file

- https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md

already covers:

- two stable magnetic states;
- coincident-current selection;
- half selection;
- destructive read / restoration;
- random-access implications;
- manufacturing labor and economics.

Case 70 therefore does **not** rewrite those topics.

Its additional retention-specific contribution is the three-way split:

```text
non-target remanent-state margin
≠
non-target sense-line contribution
≠
selected-bit destructive-read restore
```

plus the write-side split:

```text
word selection
≠
bit transition authorization
```

This is the reason for keeping Case 70 in `technical-retention` rather than moving the whole slice into `computing-archaeology`.

---

## Prior-art / priority boundary

No invention-priority claim is made.

The sources are used to establish a bounded engineering problem and period vocabulary, not to award invention of:

- ferrite-core memory;
- destructive read;
- coincident-current selection;
- inhibit writing;
- half-select disturbance;
- disturbance cancellation.

The early magnetic-memory field contains parallel and contested lines. A priority study would require a separate source program, including An Wang, RCA/Rajchman, MIT, IBM, patents, papers, laboratory notebooks, and litigation/licensing history.

For this case, the safe historical claim is narrower:

> By 1951–1954, primary records already treated coordinate partial excitation and retention under nonselecting disturbance as explicit design concerns; a 1954-filed IBM record further documents half-selected sense disturbance and cancellation as an engineering problem.

---

## Claim-source matrix

| Claim | Forrester 1951-filed patent | Papian 1952 | Bauer/Haynes 1954-filed patent | Status |
| --- | --- | --- | --- | --- |
| one coordinate excitation can physically affect non-target cores without intended stable-state switching | direct | compatible | direct | **grounded** |
| repeated nonselecting disturbances are a retention/material criterion | compatible | direct | compatible | **grounded** |
| half-selected cores can contribute readout disturbance | compatible | signal-ratio vocabulary | direct | **grounded** |
| shared sense output can fail discrimination without proving payload corruption | indirect | compatible | direct | **grounded** as bounded reconstruction |
| cancellation acts on readout disturbance rather than rewriting payload | — | — | direct circuit purpose | **grounded** |
| X/Y word selection can be further qualified by inhibit at bit/plane level in the bounded IBM design | — | — | direct | **grounded** |
| normal half selection routinely produces permanent bit flips | no | no | no | **rejected / unsupported** |
| exact IBM cancellation circuit was universal production practice | no | no | no | **rejected / unsupported** |
| core half-select is the technical ancestor of RowHammer/NAND disturb | no | no | no | **rejected / analogy only** |

---

## Cross-case comparison boundary

### Case 02 — magnetic-core destructive read

Case 02 asks what happens to the **selected** core when reading deliberately forces it toward a known state and therefore may require rewrite.

Case 70 asks what happens to **non-target** cores and to the **shared sense path** during selection.

Therefore:

> `selected-core destructive read / restore ≠ neighbor half-select disturbance`.

### Case 53 — DRAM RowHammer

Functional analogy only:

> target-directed access can impose a retention burden on other physical state.

No shared mechanism, terminology, or historical genealogy is claimed.

### Cases 52 and 59 — NAND disturb / program interference

Again, functional analogy only. NAND pass-voltage stress and capacitive/charge coupling are not magnetic half selection.

The useful shared comparison is only:

> `logical operation target ≠ complete physical effect scope`.

---

## Findings suitable for synthesis

The evidence supports the following bounded synthesis claims:

1. **Half-selected is not unexcited.**
2. **Logical nonselection is weaker than physical noninteraction.**
3. **Quiescent nonvolatility does not imply immunity to operational disturbance.**
4. **Retention under traffic can be a different engineering criterion from retention at rest.**
5. **A correct stored state can become unrecoverable because the sense path loses discrimination.**
6. **Sense-noise cancellation is not payload-state restoration.**
7. **The physical effect scope of an address can exceed the logical target set.**
8. **Write selection can be layered: choosing a word is not identical to authorizing every bit to switch.**

These claims are retention-specific and can be compared later without pretending that the historical actors used the repository's general vocabulary.

---

## Evidence status

**`grounded`**

Promotion rationale:

- **primary evidence:** three contemporary technical records;
- **historical vocabulary:** `partial change`, `nonselecting disturbances`, `information-retention ratios`, `signal ratios`, `half selected cores`, `disturbance signals`, `inhibit pulse`;
- **mechanism:** coordinate partial excitation, remanent-state margin, shared sense aggregation, cancellation, inhibit;
- **limits:** no universal failure threshold, no named-product adoption claim, no priority claim, no mechanism-identification with later disturbance cases;
- **related-repository duplication checked:** yes.

### Remaining archival work

Not a blocker for `grounded` status:

- inspect the full Papian 1952 facsimile line by line if later work needs exact numeric ratios, material tables, figures, or page anchors;
- inspect named production-machine manuals for measured half-select/sense margins;
- conduct a separate invention/priority study only if the repository later needs one.
