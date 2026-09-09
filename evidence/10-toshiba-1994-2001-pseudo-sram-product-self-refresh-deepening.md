# Toshiba pseudo-SRAM product self-refresh: named-product boundary (1994–2001)

**Canonical case:** [`10 — Toshiba Leakage-Tracked Self-Refresh`](../cases/10-toshiba-leakage-tracked-self-refresh.md)  
**Purpose:** test the open `named-product implementation` boundary without equating a commercial `SELF REFRESH` feature with the specific leakage-monitor trigger disclosed in Toshiba's 1984-priority patent.  
**Evidence range:** a 1994 Toshiba static-RAM data-book artifact for the `TC51832A` pseudo-static-RAM family plus Toshiba's official 18-June-2001 `TC51W3216XB` pseudo-SRAM launch announcement.

This is a retention-specific productization check, not a general history of pseudo-SRAM, not a JEDEC chronology, and not a patent-to-product genealogy.

---

## 1. Why this slice matters

Case 10 already grounds two manufacturer-primary circuit disclosures:

- Hitachi's 1982-filed / 31-March-1984-published leakage-simulation + comparator self-refresh design;
- Toshiba's 1984-priority / 1987-published self-refresh design with an oscillator, refresh-address counter, and a preferred leak-current-monitor threshold path.

Those sources establish that leakage-derived autonomous refresh was proposed. They did **not** establish that a named shipping memory part used the exact preferred circuit.

The present slice asks a narrower product question:

> Can named Toshiba pseudo-SRAM products be grounded as using autonomous self-refresh, and if so, does the product documentation establish the same leakage-tracked trigger as US4682306A?

The answer is asymmetric:

> **yes for named-product self-refresh; no for the exact leakage-tracked trigger.**

---

## 2. Source A — Toshiba 1994 Static RAM data book / `TC51832A` family

A scanned Toshiba **1994 Static RAM** data book is preserved at Bitsavers:

- <https://www.bitsavers.org/components/toshiba/_dataBook/1994_Toshiba_Static_RAM.pdf>

The indexed table of contents places `TC51832A` under **Pseudo Static RAM** and identifies a 256K, 32K×8 family. The underlying Toshiba family datasheet is also preserved through a third-party datasheet mirror:

- <https://www.alldatasheet.com/datasheet-pdf/pdf/1462395/TOSHIBA/TC51832AP.html>

### 2.1 Source-custody note

The Bitsavers artifact is a scanned manufacturer data book, but the raw PDF returned HTTP 403 to this research environment during this pass. Search indexing exposed the Toshiba title/catalog entry, and the `TC51832AP` Toshiba datasheet text was independently recoverable through the mirror. Therefore the mechanism claims below are marked **`H/P*`** rather than pretending this pass completed page-image facsimile inspection.

This is stronger than relying on an unsourced parts database, but weaker than a directly rendered manufacturer page. A future facsimile pass can close the page-anchor debt without changing the bounded conclusion unless the scan contradicts the mirrored text.

### 2.2 What the named family directly says

The preserved Toshiba datasheet identifies the `TC51832A` family as a 256K-bit high-speed CMOS **pseudo static RAM**, organized 32,768×8. Its description says the array uses a **one-transistor dynamic memory cell** with CMOS peripheral circuitry while exposing a static-RAM-like interface.

The same product text separates two refresh paths behind the `RFSH` input:

- `Auto refresh`;
- `Self refresh`.

Its feature list says:

- **Self refresh is supported by an internal timer**;
- **Auto refresh is supported by an internal refresh-address counter**;
- the family requires **256 refresh cycles / 4 ms**.

The retention-specific point is not merely that the word `self refresh` appears. The product documentation separates the recurrence source and the row-enumeration mechanism:

```text
one-transistor dynamic payload
    !=
internal refresh-address counter
    !=
internal self-refresh timer
    !=
SRAM-like external access interface
```

### 2.3 Product-family documentation floor, not first-sale chronology

The safe historical claim is:

> **By Toshiba's 1994 static-RAM data-book record, a named `TC51832A` pseudo-static-RAM family was documented with internal-timer self refresh and internal-counter auto refresh.**

This does not establish:

- first invention of pseudo-SRAM;
- first Toshiba product with self refresh;
- first sale or shipment date of `TC51832A`;
- the exact circuit underneath the phrase `internal timer`;
- compliance with a later SDRAM/JEDEC self-refresh contract.

---

## 3. Source B — Toshiba `TC51W3216XB`, 18 June 2001

Toshiba's still-live corporate press archive gives a second, cleaner manufacturer-primary product witness:

- Toshiba Corporation, **“Toshiba Announces its 32Mb Pseudo SRAM Solution,”** 18 June 2001: <https://www.global.toshiba/ww/news/corporate/2001/06/pr1802.html>

The announcement names the **`TC51W3216XB`** and explicitly describes:

- a **standard SRAM interface**;
- a **1-transistor DRAM-like memory cell**;
- a **self-refresh feature**;
- no requirement for a separate DRAM controller;
- no external glue logic normally associated with standard-DRAM refresh operation.

It also states an availability plan: sample quantities in early Q3 2001 and full production approximately two months later.

This source therefore grounds a genuine manufacturer-announced commercialization boundary:

> **Toshiba publicly marketed a named pseudo-SRAM product whose dynamic-cell payload was presented through an SRAM-like interface while self-refresh work was internalized enough to remove the separate DRAM-controller/glue-logic burden described in the announcement.**

The source still does not expose the internal timer/sensor circuit of `TC51W3216XB`.

---

## 4. Engineering reconstruction — what moved behind the interface

### 4.1 Pseudo-static interface ≠ static retention mechanism

`Pseudo static RAM` is historical product vocabulary here. The bounded `TC51832A` documentation simultaneously says the payload uses a one-transistor dynamic memory cell.

Therefore:

> **SRAM-like interface ≠ SRAM-like physical retention.**

The interface can make ordinary use more static-RAM-like while internal refresh continues to preserve a dynamic substrate.

### 4.2 Internal row enumeration ≠ internal recurrence scheduling

The `TC51832A` feature list separately names an internal refresh-address counter for Auto Refresh and an internal timer for Self Refresh. Even in a product that exposes both capabilities, these are not one state or one responsibility.

This independently reinforces the Case-09 / Case-10 decomposition:

> **where the next refresh row comes from ≠ what causes autonomous refresh work to recur.**

### 4.3 Self refresh ≠ leakage-tracked self refresh

This is the central negative result.

Toshiba US4682306A's preferred embodiment derives the start of a refresh sequence from a leak-current monitor capacitor crossing a threshold. The `TC51832A` product text available in this pass says **internal timer**. It does not mention:

- a leak-current monitor capacitor;
- a leakage-simulation capacitor pair;
- a threshold detector/comparator tied to payload-like leakage;
- refresh interval variation as measured leakage changes.

No inference from the word `timer` can fill that gap.

Therefore:

> **named-product autonomous self refresh ≠ named-product leakage-tracked self refresh.**

And:

> **commercial productization of the broad function ≠ deployment proof for the patent's preferred circuit.**

The internal timer could conceivably be influenced by environmental or process conditions in ways the short product description does not disclose, but that possibility is not evidence.

### 4.4 Hidden maintenance ≠ eliminated maintenance

Toshiba's 2001 announcement emphasizes that a separate DRAM controller and external refresh glue logic are unnecessary for its pseudo-SRAM. That is an interface/system-integration statement.

It does not mean dynamic refresh ceased to exist. The same announcement explicitly identifies self refresh and a one-transistor DRAM-like cell.

Thus:

> **external refresh burden removed ≠ refresh obligation removed.**

A product can make persistence *look* static to the surrounding system by internalizing maintenance work.

### 4.5 Self refresh ≠ nonvolatility

Neither named product source says data persists after device power removal. `Self refresh` is a powered maintenance mode for dynamic state, not evidence of intrinsic nonvolatile storage.

Therefore:

> **autonomous refresh ≠ unpowered retention.**

---

## 5. Historical record, reconstruction, analogy, interpretation

### Historical record (`H/P`, `H/P*`)

- Toshiba's 1994 static-RAM data-book artifact lists the named `TC51832A` pseudo-static-RAM family.
- The preserved Toshiba family text describes a one-transistor dynamic array, SRAM-like interface, Auto Refresh, Self Refresh, an internal self-refresh timer, and an internal auto-refresh address counter.
- Toshiba's official 18-June-2001 announcement names `TC51W3216XB`, a one-transistor DRAM-like pseudo-SRAM with SRAM interface and self refresh, and states planned sampling/full-production timing.

### Engineering reconstruction (`E`)

- SRAM-like service can be achieved while dynamic retention maintenance remains internal.
- Refresh-address enumeration and recurring self-refresh timing are distinct control relations.
- Product documentation for broad self-refresh functionality does not establish the patent's leakage-derived trigger.

### Functional analogy (`A`)

Case 21's 1999 Micron SDRAM also distinguishes externally caused refresh from an internal self-refresh regime. The bounded analogy is maintenance-responsibility internalization. The mechanisms/interfaces remain different:

```text
Toshiba TC51832A pseudo-SRAM
    SRAM-like external interface
    RFSH-selected Auto/Self Refresh
    product text names internal timer + refresh-address counter

Micron 64Mb SDR SDRAM (Case 21)
    synchronous command interface
    AUTO REFRESH is externally repeated
    SELF REFRESH is entered with refresh command encoding + CKE LOW
    exit has explicit tXSR service-recovery timing
```

This does not establish Toshiba→Micron genealogy, JEDEC descent, or identical internal circuits.

### Philosophical interpretation (`I`)

The narrow conceptual lesson is that **maintenance can disappear from the user's operational surface without disappearing from the retained state's conditions of persistence**. Internalization can make a dynamic mechanism present itself as a simpler stable service relation.

The limit is equally important: this is not evidence that all apparently passive storage hides continuous work, and it is not historical evidence that Toshiba engineers formulated a philosophy of invisible maintenance.

---

## 6. What this changes in Case 10

Before this slice, Case 10 could say only:

- leakage-derived self-refresh was disclosed in patents;
- named-product implementation of the exact circuit was open.

After this slice, the boundary is more precise:

1. **named Toshiba pseudo-SRAM product families with self refresh are grounded**;
2. a 1994 product-family document explicitly names an **internal timer** and **internal refresh-address counter**;
3. a 2001 official Toshiba product launch confirms commercial productization of dynamic-cell pseudo-SRAM with self refresh and reduced external refresh-controller burden;
4. **the exact leakage-monitor/comparator mechanism of the 1984-priority patent remains unproven in a named product**.

The old open item is therefore not `named-product self refresh?` anymore. It is:

> **named-product deployment of the specific leakage-derived/adaptive trigger, plus the broader patent→product→standards genealogy.**

---

## 7. Related-repository boundary

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `TC518512`, `TC51832`, and `pseudo SRAM` returned no dedicated treatment to reuse.

A broad history of pseudo-SRAM products, asynchronous DRAM interfaces, controller integration, standards, patents, and product generations belongs there if developed. `technical-retention` keeps only the retention-specific distinction among:

- dynamic payload;
- internal refresh-row enumeration;
- autonomous recurrence timing;
- external interface simplification;
- evidence for a specific adaptive/leakage-derived trigger.

---

## 8. Open limits

This slice does **not** close:

- direct page-image inspection and exact page anchors for the 1994 Toshiba data-book copy;
- `TC51832A` first-sale / first-shipment chronology;
- first Toshiba pseudo-SRAM with self refresh;
- transistor-level implementation of the `TC51832A` internal timer;
- proof that any named Toshiba product implemented US4682306A's preferred leak-monitor threshold circuit;
- Hitachi/Toshiba patent-to-product genealogy;
- JEDEC or pseudo-SRAM standards genealogy;
- temperature/process compensation of named-product self-refresh timing;
- production fault injection or retention testing.

Those are separate slices.

## Sources

1. Toshiba, **1994 Static RAM** data book, preserved scan: <https://www.bitsavers.org/components/toshiba/_dataBook/1994_Toshiba_Static_RAM.pdf>.
2. Toshiba Semiconductor, **TC51832A family / TC51832AP, 32,768 word × 8-bit CMOS Pseudo Static RAM**, preserved manufacturer-datasheet mirror: <https://www.alldatasheet.com/datasheet-pdf/pdf/1462395/TOSHIBA/TC51832AP.html>.
3. Toshiba Corporation, **“Toshiba Announces its 32Mb Pseudo SRAM Solution,”** 18 June 2001: <https://www.global.toshiba/ww/news/corporate/2001/06/pr1802.html>.
4. Toshiba Corp., Takayasu Sakurai and Tetsuya Iizuka, **US4682306A, “Self-refresh control circuit for dynamic semiconductor memory device”**: <https://patents.google.com/patent/US4682306A/en>.
5. Hitachi Ltd., **JPS5956291A, “MOS storage device”**, published 31 March 1984: <https://patents.google.com/patent/JPS5956291A/en>.
