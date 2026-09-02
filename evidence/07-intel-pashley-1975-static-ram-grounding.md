# Case 07 grounding: Intel manufacturer-primary static RAM cell and array boundary

## Purpose

This record closes the main mechanism-source gap in [`../cases/07-static-mos-ram-powered-quiescence.md`](../cases/07-static-mos-ram-powered-quiescence.md) without pretending that one 1975 Intel patent is an identified production schematic for the 1101, 1101A, 2102, or 2102A.

The bounded question is narrower:

> Did Intel itself disclose, in a period primary design source, a static MOS RAM in which a bistable cross-coupled cell is embedded in a decoded array whose sensing and address-selection machinery has separate reliability and timing constraints?

For that claim the answer is now yes.

---

## Primary source

Richard D. Pashley, **“High speed MOS RAM employing depletion loads,”** US Patent 3,946,369, assigned to Intel Corporation, filed 21 April 1975 and published 23 March 1976.

- patent transcription / images entry: <https://www.freepatentsonline.com/3946369.html>
- stable patent identifier: US3946369A.

The filing date places the disclosed design inside the bounded 1968–1975 design window even though publication occurred in 1976.

---

## H/P — period and manufacturer vocabulary

The patent identifies the object as an **MOS static random-access memory (RAM)** and describes static memories as using **bistable circuits for memory cells**.

In the disclosed preferred embodiment Intel specifies:

- an n-channel MOS implementation on a p-type silicon substrate;
- a `1,024 × 1` word organization;
- a `32 × 32` cell array;
- a `+5 V` VCC condition;
- polycrystalline-silicon gates;
- depletion-load devices fabricated by ion implantation.

This is manufacturer-primary evidence for an Intel static-MOS design class. It is stronger than the prior Case-07 chain in one specific respect: the repository no longer has to infer Intel's cell-level static mechanism from a neighboring Fairchild design, a generic NASA cell, a trade-journal drawing, or package-level Intel catalog language alone.

---

## H/P — cell-level bistability in Figure 1

The patent's Figure 1 description places each memory cell between VCC/VSS and a complementary pair of column lines. The preferred cell contains:

- two load devices;
- two drive/storage devices arranged as two branches;
- feedback from each branch's storage node to the opposite drive-device gate;
- two access devices connecting the two internal nodes to the complementary column lines;
- an X-line controlling the access devices.

The source calls the cell a **bistable circuit** and explicitly describes feedback between the two branches.

This directly supports the bounded mechanism claim:

```text
continued powered bias
        +
cross-feedback between two cell branches
        ↓
bistable stored condition
        ↓
X-line selection connects the internal nodes to a complementary column pair
```

### Important topology boundary

The preferred embodiment is an **n-channel depletion-load** static cell. Even if a modern reader counts two load, two drive, and two access devices, that does **not** license relabeling the design as the later canonical complementary-CMOS `6T SRAM` cell. Equal device counts do not establish identical device technology, circuit ratios, power behavior, or historical vocabulary.

---

## H/P — array service is a separate mechanism layer

The same patent makes the surrounding memory organization explicit:

- 32 rows and 32 columns;
- X decoders for row selection;
- Y decoding for column selection;
- paired column lines;
- per-column sense amplifiers;
- a common read bus;
- an output sense amplifier/buffer;
- write-bus connections;
- address buffers generating each address signal and its complement.

The high-speed invention is not mainly a new way to make the bistable state continue to exist. It instead attacks **access-path** constraints:

1. large column-line capacitance slows sensing;
2. the sense-amplifier arrangement is designed to detect small column-line changes before a large swing develops;
3. the address buffer is cross-coupled so true/complement outputs switch together, preventing unintended multiple selections during an address transition.

This gives Case 07 a manufacturer-primary way to separate **retention of state** from **reliable selection and recovery of that state**.

---

## E — engineering reconstruction

The source supports a layered reconstruction:

```text
cell-retention layer
    powered bistable cross-feedback

selection layer
    X/Y decoding + access devices

sensing layer
    column lines + sense amplifier + read bus

interface-transition layer
    address buffers must avoid transient multiple selection
```

A failure at the latter three layers need not mean that the bistable condition in an unselected cell has physically disappeared.

Therefore:

> **retention stability ≠ access-path reliability.**

And more specifically:

> **hold margin, selection integrity, and sensing margin are different engineering questions even inside one static RAM.**

The patent directly supports the selection/sensing side of that distinction. It does not provide a complete product-specific retention-voltage/noise-margin characterization for the Intel 1101A or 2102.

---

## H/P + E — what this closes

Before this record, Case 07 had:

- period generic static-MOS cell mechanisms from NASA and Fairchild;
- period Intel static-MOS / flip-flop vocabulary;
- Intel package-level no-refresh and nondestructive-read behavior;
- an Intel-1101-specific period secondary cell witness;
- an Intel-provenance 1101 mask locator;
- Intel 5101L device-specific low-voltage retention and recovery evidence.

What it lacked was a **manufacturer-primary Intel static-RAM cell design source that could be interpreted at circuit level**.

US3946369A closes that broad evidence-class gap for an Intel `1024 × 1`, `32 × 32`, +5 V static-MOS design filed in 1975.

This is sufficient to ground the Case-07 central comparison:

> powered regenerative/bistable retention survives the move into an Intel monolithic static-MOS array, while decode, sensing, and address-transition integrity remain separate layers of the memory service.

---

## X — what this does not close

Do **not** infer any of the following:

- `US3946369A = Intel 2102`;
- `US3946369A = Intel 2102A`;
- `US3946369A = Intel 1101/1101A`;
- every Intel static RAM of the period used this exact cell;
- depletion-load nMOS = complementary CMOS;
- same transistor count = same SRAM topology;
- a reliable bistable cell guarantees correct address selection or sensing;
- the patent's access-speed/sensing discussion is a measured retention-voltage or static-noise-margin specification.

The patent never needs to be tied to a commercial model to do its job in this repository. Its evidentiary role is **manufacturer-primary mechanism grounding for the static-MOS array class**.

---

## Remaining archival / product-specific cleanup

These tasks remain useful but no longer block the bounded Case-07 mechanism claim:

1. directly inspect a reliable facsimile of Vadasz–Chua–Grove 1971 pp. 43 and 47;
2. find an explicit manufacturer-primary link from a transistor-level cell to the 1101/1101A/2102/2102A if exact product-topology history is later needed;
3. recover a product-specific static hold/noise-margin characterization beyond the already grounded 5101L retention-supply boundary;
4. interpret the Smithsonian 1101 mask only if a layer map or other archival documentation makes that interpretation defensible.

Those are narrower artifact/product questions. They should not be silently converted back into a generic claim that Intel static-cell mechanism is unknown.

---

## Promotion judgment

Case 07 can now be promoted from `first-pass` to **`grounded`** for its bounded retention comparison because it has:

- multiple primary period source families;
- explicit historical vocabulary;
- manufacturer-primary Intel cell-level mechanism evidence;
- Intel product-level static/no-refresh/nondestructive-read behavior;
- a device-specific low-power retention/recovery boundary in the 5101L;
- mechanism-sensitive failure and access distinctions;
- negative controls against dynamic Intel cells and universal 6T normalization;
- a fresh related-repository duplication check.

The promotion is **claim-specific**. It grounds the static-MOS retention regime, not an exact transistor-level genealogy of every Intel commercial SRAM product.
