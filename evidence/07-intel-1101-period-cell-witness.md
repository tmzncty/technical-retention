# Case 07 source deepening — Intel 1101 period cell witness and artifact locator

## Purpose

This note deepens [`cases/07-static-mos-ram-powered-quiescence.md`](../cases/07-static-mos-ram-powered-quiescence.md) without pretending that a period trade-journal schematic or a museum catalog record is an Intel primary circuit-design disclosure.

The bounded question is:

> Can the open Intel-specific cell gap be narrowed beyond generic Fairchild/NASA static-MOS witnesses without lowering the repository's primary-source standard?

The answer is **yes, but only partially**. A 1973 period technical article supplies an Intel-1101-specific cell drawing and explicitly identifies the 1101 cell as static. Intel's current historical archive independently identifies the 1101 as a 1969 static random-access memory using MOS and silicon-gate technology. The Smithsonian records an Intel-supplied 1101 RAM mask dated February 1972. Together these sources make the remaining gap much more precise, but they do **not** yet justify promotion of Case 07 to `grounded`.

---

## Source 1 — George Sideris, *Electronics*, 26 April 1973

### Bibliographic record — H/S, period technical reporting

- George Sideris, **“The Intel 1103: The MOS memory that defied cores,”** *Electronics*, 26 April 1973, pp. 108–113.
- Period issue scan indexed by World Radio History: <https://www.worldradiohistory.com/Archive-Electronics/70s/73/Electronics-1973-04-26.pdf>.
- Alternate scan indexed by Bitsavers: <https://bitsavers.trailing-edge.com/magazines/Electronics/Electronics_V46_N09_19730426_Intel_1103.pdf>.

The indexed issue text identifies Sideris as the magazine's San Francisco bureau manager. This is therefore **contemporaneous technical journalism**, not an Intel-authored paper, patent, datasheet, mask drawing, or internal design memorandum.

### Intel-1101-specific cell witness — H/S

Figure 1 in the indexed issue text is a cell-comparison figure. Its first diagram is explicitly labeled **`(a) 1101 CELL`**. The figure caption states that the static cell used by Intel in the 1101 RAM was too slow and costly for mainframe memories and contrasts it with dynamic-cell alternatives leading to the 1102 and 1103.

This matters because the Case-07 source set previously had two different kinds of evidence that had to remain separate:

1. **generic period cell-level evidence** — Fairchild US3530443A and NASA-CR-108672;
2. **Intel product-level behavior** — 1101A/2102/5101 catalog documentation.

Sideris adds a third, intermediate layer:

3. **Intel-product-specific period cell evidence from a secondary technical source**.

The indexed figure is strong enough to establish that a period technical publication circulated a cell-level representation specifically labeled as the Intel 1101 cell and treated it as static. It is **not** strong enough to establish that the drawing is an Intel production schematic, a mask-level reconstruction, or an exact transistor-by-transistor manufacturer disclosure.

### Source-inspection boundary — X

The current web-access path exposes indexed/OCR text from the period issue, including the figure labels and caption, but the PDF endpoints did not yield a reliably renderable page image in this run. Therefore:

- `indexed period figure text` **≠** `direct visual inspection of the facsimile page`;
- no line geometry, device count, transistor connectivity, or fine schematic detail is claimed from the unrendered image;
- the figure is recorded as a period source locator and cell-specific witness, not as a visually verified primary schematic.

This preserves the same claim-specific evidence rule already used elsewhere in the repository.

---

## Source 2 — Intel historical archive, “The 1101”

### Record — H/S, institutional retrospective

Intel's historical timeline identifies the 1101 as a **1969 static random-access memory** and states that it was the first commercial chip to successfully implement both metal-oxide-semiconductor and silicon-gate technologies. The page also includes a die-shot caption for the 1101.

Source: Intel, **“The 1101,”** Intel historical timeline: <https://timeline.intel.com/1969/the-1101>.

This is useful for product identity, period placement, and technology lineage, but it is a modern corporate retrospective rather than a 1969 engineering disclosure. Its die shot is an archival visual locator; without layer annotation or an independently checked reconstruction it does not by itself establish the bit-cell topology.

### X — prohibited inference

Do not infer from the Intel timeline alone that:

- the exact 1101 bit cell has been reconstructed;
- the die-shot image proves a modern canonical `6T SRAM` topology;
- every structure visible in a die image can be assigned a retention function without additional design evidence.

---

## Source 3 — Smithsonian Intel 1101 RAM mask

### Artifact record — H/S, institutional artifact provenance

The Smithsonian National Museum of American History catalogs an **“Intel 1101 Random Access Memory (RAM) Mask”**:

- object ID: `1984.0124.11`;
- object type: integrated-circuit mask;
- credit line: **from Intel Corporation**;
- related date: **1972-02**;
- maker: Intel Corporation;
- material: glass.

Source: National Museum of American History, **“Intel 1101 Random Access Memory (RAM) Mask”**: <https://americanhistory.si.edu/collections/object/nmah_713505>.

This is valuable because it locates a surviving Intel-provenance manufacturing artifact tied specifically to the 1101. It changes the archival situation from “perhaps a product-specific artifact exists” to “a cataloged Intel-supplied 1101 mask is known.”

It does **not** yet close the circuit-design gap. The catalog entry does not identify the mask layer, annotate storage cells, or provide a verified cell-level interpretation.

### E — what the artifact could support later

A future source-deepening pass could use a directly inspectable high-resolution mask image, layer identification, and a period or specialist design reference to test whether the cell-specific topology can be reconstructed independently of the Sideris trade-journal figure.

That would be a materially stronger result than simply assuming a transistor count from later SRAM textbooks.

---

## Engineering consequence for Case 07

### E — the source gap is now narrower

Before this note, the open gap could be summarized as:

> obtain Intel-specific cell-level evidence rather than transferring a Fairchild or generic NASA cell to the Intel 1101/2102.

After this note, that formulation can be sharpened:

> **Intel-1101-specific cell-level evidence now exists in period technical reporting, and a surviving Intel-provenance 1101 manufacturing mask is institutionally cataloged; what is still missing is a directly inspected primary Intel design source or directly interpretable artifact evidence sufficient to ground the exact cell mechanism.**

That distinction matters. The repository no longer needs to search blindly for proof that the 1101 had some identifiable static cell. It needs to search specifically for the **evidence class required for promotion**.

### E — product identity, cell witness, and exact topology remain different layers

Case 07 should therefore keep three layers separate:

```text
Intel product identity / static behavior
        ↓
period Intel-specific cell witness
        ↓
exact manufacturer or artifact-grounded cell mechanism
```

The first layer is already strong. This run materially improves the second. The third remains open.

---

## What this does **not** change

Case 07 remains `first-pass`.

Still open before promotion:

1. direct visual inspection of Vadasz–Chua–Grove 1971 pp. 43 and 47;
2. a primary Intel schematic/design disclosure for the 1101/1101A or 2102-class static cell, **or** directly inspectable artifact evidence that can support an equivalent bounded mechanism claim;
3. device-specific hold/failure/noise-margin evidence for one of the bounded Intel static products rather than transferring Fairchild margins;
4. cache semantics remain deferred.

The Sideris figure is useful precisely because it narrows the gap without erasing it.

---

## Claim ledger

| Claim | Type | Status |
| --- | --- | --- |
| a 1973 *Electronics* article contains a figure whose first diagram is labeled `(a) 1101 CELL` | H/S | supported by indexed period-issue text |
| the same figure caption describes the Intel 1101 cell as static | H/S | supported by indexed period-issue text |
| the Sideris figure is an Intel-authored production schematic | X | unsupported |
| the exact transistor connectivity/count of the Sideris 1101 figure has been visually verified in this run | X | not established; PDF facsimile was not reliably rendered |
| Intel's historical archive identifies the 1101 as a 1969 static RAM using MOS and silicon-gate technology | H/S | supported |
| the Smithsonian catalogs an Intel-supplied 1101 RAM mask dated February 1972 | H/S | supported |
| the Smithsonian catalog record by itself reveals the bit-cell topology | X | unsupported |
| the Intel-specific source gap has been narrowed from generic cell evidence to primary/artifact-level mechanism evidence | E | supported |
| Case 07 is ready to promote to `grounded` | X | not yet |

---

## Sources

1. George Sideris, **“The Intel 1103: The MOS memory that defied cores,”** *Electronics*, 26 April 1973, pp. 108–113. Period issue indexed by World Radio History and Bitsavers.
2. Intel, **“The 1101,”** Intel historical timeline: <https://timeline.intel.com/1969/the-1101>.
3. National Museum of American History, **“Intel 1101 Random Access Memory (RAM) Mask,”** object `1984.0124.11`: <https://americanhistory.si.edu/collections/object/nmah_713505>.

## Related-repository check

A fresh search in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `SRAM`, `static RAM`, and `Intel 1101` still returned no dedicated case to reuse. Broad semiconductor-memory history should remain routed there; this note contributes only the retention-specific source boundary needed by Case 07.