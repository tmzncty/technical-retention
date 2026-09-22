# Case 04 evidence deepening — Toshiba NAND: experimental device, commercialization, sample shipment, and mass-production chronology (1989–1992)

## Scope

This note closes one narrow chronology gap around Case 04:

> What can the currently inspected evidence actually support about the transition from Toshiba's late-1980s experimental 4 Mbit NAND device work to a named commercial NAND part, and which historical verbs must remain distinct?

It does **not** attempt to write a general history of NAND Flash, adjudicate every "first" claim, or move later FTL/controller semantics backward into the device history.

The bounded chronology examined here is:

```text
1989 experimental 4 Mbit NAND technical publication
    -> 1991 retrospective corporate commercialization/development milestone
    -> Nov 1991 reported sample shipments of named TC584000
    -> Apr 1992 reported planned mass production
```

The central methodological result is that the arrows above are **milestone changes**, not synonyms.

---

## Evidence classes used here

Following `docs/METHOD.md`, this file separates:

- **Historical record** — what a source directly states or demonstrates;
- **Engineering reconstruction** — what follows from combining bounded technical/historical facts;
- **Functional analogy** — limited comparisons with other repository cases;
- **Philosophical interpretation** — what the distinction means for technical-retention as a project.

It also preserves source provenance:

- 1989 IEEE technical papers are contemporary technical records;
- the December 1991 *Electronics Australia* item is near-contemporary reporting of a named product and shipment plan;
- current KIOXIA/Toshiba history pages are later first-party retrospectives;
- the IEEE Spectrum account is a later retrospective and is not treated as a contemporaneous shipment record.

---

# 1. Historical record

## H/P — 1989 public evidence explicitly describes an experimental 4 Mbit NAND device

The 1989 ISSCC paper by Yasuo Itoh, Masaki Momodomi, Riichiro Shirota, Yoshihisa Iwata, Ryozo Nakayama, Ryouhei Kirisawa, Tomoharu Tanaka, Koichi Toita, Satoshi Inoue, and Fujio Masuoka is titled:

> `Experimental 4 Mb CMOS EEPROM with a NAND structured cell`

Its abstract describes a 5 V-only CMOS 512K × 8 EEPROM, an eight-bit NAND string between select transistors, page-mode programming, and a dynamic sense amplifier.

Bibliographic anchor:

- Y. Itoh et al., *Digest of Technical Papers — IEEE International Solid-State Circuits Conference*, vol. 32, 1989, pp. 134–135, 314.
- DOI: `10.1109/ISSCC.1989.48209`
- https://doi.org/10.1109/ISSCC.1989.48209
- accessible bibliographic/abstract record: https://scholar.nycu.edu.tw/en/publications/experimental-4-mb-cmos-eeprom-with-a-nand-structured-cell/

The companion 1989 JSSC article is even more explicit in its title:

> `An Experimental 4-Mbit CMOS EEPROM with a NAND-Structured Cell`

It states that the EEPROM was **designed and fabricated**, gives 1.0 μm design rules, block erase, successive programming, random read behavior, timing, and die size.

Bibliographic anchor:

- M. Momodomi et al., *IEEE Journal of Solid-State Circuits* 24(5), 1989, pp. 1238–1243.
- DOI: `10.1109/JSSC.1989.572587`
- https://doi.org/10.1109/JSSC.1989.572587
- accessible bibliographic/abstract record: https://scholar.nycu.edu.tw/en/publications/an-experimental-4-mbit-cmos-eeprom-with-a-nand-structured-cell/

For this repository, the word **experimental** is not decorative. It constrains the historical claim that can be made from the paper itself.

Supported:

```text
1989
    -> public technical disclosure
    -> designed/fabricated experimental 4 Mbit NAND device
```

Not supported by these papers alone:

```text
1989
    -> named shipping product
    -> sample availability
    -> volume production
    -> customer adoption
```

That distinction repairs a common chronology compression in later histories.

---

## H/S — current KIOXIA first-party history assigns commercialization to 1991

KIOXIA's current technology-development history states:

- 1987 — invention/announcement of NAND flash memory;
- **1991 — commercialization of the 4 Mbit NAND flash memory**;
- 1992 — commercialization of a 16 Mbit NAND flash memory.

Source:

- KIOXIA, `Technology Development History`
- https://www.kioxia.com/en-jp/rd/technology/history.html

KIOXIA Holdings' sustainability/history material likewise labels 1991 as commercialization of the 4 Mbit NAND flash memory:

- https://www.kioxia-holdings.com/en-jp/sustainability/materiality/creation/useful.html

This is useful first-party retrospective evidence, but it is **not a 1991 product announcement**. Its historical verb must therefore remain source-qualified:

```text
later KIOXIA retrospective
    -> calls 1991 "commercialization"
```

It should not silently become:

```text
contemporaneous 1991 launch document proves exact shipment date
```

---

## H/S — current Toshiba history uses a different 1991 verb: developed

Toshiba's current corporate chronology records for 1991:

> development of the world's first 4-megabit NAND-type EEPROM

Source:

- Toshiba, `Chronology of History`
- https://www.global.toshiba/ww/outline/corporate/history/chronology.html

A Toshiba integrated-report retrospective also describes the 1991 4-megabit NAND-type EEPROM as a development milestone while elsewhere saying Toshiba commercialized NAND flash in 1991.

The important evidence point is not to decide that one corporate page is "right" and the other is "wrong." It is that the verbs encode different milestone categories:

```text
developed
    !=
commercialized
```

The repository should retain the source's verb rather than normalize both into an undifferentiated event called "invented" or "released."

---

## H/B — December 1991 near-contemporary reporting names TC584000 and separates marketing, sample shipment, and mass production

A December 1991 *Electronics Australia* `Solid State Update` item reports that Toshiba had begun worldwide marketing a 4-megabit NAND EEPROM and gives the product identifier **TC584000**.

The same item distinguishes two further milestones:

- sample shipments were to start in **November 1991**;
- mass production was planned to begin in **April 1992**.

Source scan:

- *Electronics Australia*, December 1991, `Solid State Update`, item `First 4Mb NAND EEPROM`.
- archival scan: https://www.worldradiohistory.com/AUSTRALIA/Electronics-Australia/EA-1991-12.pdf

Evidence class: **near-contemporary secondary reporting**. It is much closer to the commercial event than today's retrospective corporate histories, but it is still not being promoted here into Toshiba's original press release, order book, invoice, or customer shipment ledger.

The source nevertheless closes an important gap because it provides a **named part** and separates commercial stages that a one-year corporate timeline collapses:

```text
worldwide marketing announced / begun
    !=
sample shipment
    !=
mass production
```

It also creates a concrete search target for future primary-source work:

```text
TC584000
```

rather than the generic phrase "4 Mbit NAND."

---

## H/P-later — a later Toshiba-associated patent treats TC584000 as a practically used, available NAND EEPROM

A Toshiba-assigned patent family with 1993 priority describes a 4 Mbit NAND EEPROM `TC584000` available from Toshiba Corporation and refers to such a NAND EEPROM as then practically used.

Source:

- U.S. Patent `US5469399A`, *Semiconductor memory, memory card, and method of driving power supply for EEPROM*.
- priority 16 March 1993.
- https://patents.google.com/patent/US5469399A/en

This is **later technical corroboration that the named device existed as an available/practical component by that later horizon**. It does not by itself date the first sample, first sale, or start of mass production.

Useful relation:

```text
1991 near-contemporary named-product report
    +
1993-priority later technical use of same part number
        ->
stronger named-product continuity
```

But:

```text
later patent says "available"
    !=
first availability date
```

---

## H/S-later — IEEE Spectrum's retrospective assigns a 1989 "hit the market" milestone

A later IEEE Spectrum retrospective labels Toshiba NAND Flash with year **1989** and says Toshiba's first NAND flash "hit the market" in that year.

Source:

- IEEE Spectrum, `Chip Hall of Fame: Toshiba NAND Flash Memory`
- https://spectrum.ieee.org/chip-hall-of-fame-toshiba-nand-flash-memory

This is relevant because it conflicts in wording/date with the later KIOXIA 1991 commercialization chronology and with the December 1991 named-product/sample-shipment report.

The correct repository response is **not** to erase the discrepancy by selecting whichever year looks convenient.

The correct response is to preserve provenance:

```text
1989 primary technical record
    -> experimental device publication

1989 later IEEE Spectrum retrospective
    -> "hit the market"

1991 KIOXIA retrospective
    -> commercialization

Dec 1991 near-contemporary report
    -> TC584000; sample shipments Nov 1991;
       mass production planned Apr 1992
```

This is exactly why `year` without `milestone verb + source class` is not a sufficient historical data model.

---

# 2. Engineering reconstruction

## E — commercialization chronology is a state sequence, not a scalar date

For this bounded case, a more useful event model is:

```text
concept / architecture
    !=
patent filing or priority
    !=
public technical disclosure
    !=
experimental fabricated device
    !=
corporate development milestone
    !=
commercialization claim
    !=
marketing announcement
    !=
sample shipment
    !=
mass-production start
    !=
customer adoption
```

These states can occur close together, overlap, or be reported retrospectively with compressed wording. That does not make them interchangeable.

The practical repository rule should therefore be:

```text
historical date
    = date
    + milestone verb
    + source type
    + provenance
    + confidence / unresolved conflict
```

not:

```text
historical date
    = year only
```

---

## E — the current evidence supports a stronger 1989→1992 chain than the previous generic chronology

Before this slice, the early NAND evidence established experimental device/circuit geometry before FTL-like mapping.

This slice adds a bounded commercialization chain:

```text
1989
    experimental 4 Mbit NAND device publicly documented

1991
    later first-party histories place a development/commercialization milestone here

Nov 1991
    near-contemporary report says TC584000 sample shipments were to begin

Apr 1992
    same report says mass production was planned to begin

1993-priority later Toshiba technical record
    TC584000 described as available / practically used
```

The chain is stronger because it moves from a generic technology label to a named part and distinct supply milestones.

It remains bounded because the April 1992 statement is a **plan reported in December 1991**. This file does not yet contain a primary April 1992 production record proving that the plan was executed exactly as scheduled.

---

## E — experimental device evidence and commercial-product evidence answer different questions

The 1989 papers answer questions such as:

- Was a working 4 Mbit NAND-structured device designed/fabricated?
- What string organization and program/read/erase behavior did it demonstrate?

The 1991–1992 product evidence answers different questions:

- Was there a named product?
- Was it being marketed?
- Were samples scheduled/shipped?
- Was volume production planned or underway?

Therefore:

```text
experimental success
    !=
manufacturing readiness
    !=
supply availability
```

This matters technically because a retention architecture cannot be dated merely by the earliest laboratory demonstration if the question is when a particular fielded population could actually exist.

---

## E — named product identity is a new anchor, but it is not yet customer adoption evidence

`TC584000` is useful because it allows future evidence to be joined across:

- data sheets;
- catalogs;
- price lists;
- application notes;
- board/card designs;
- patents citing an available part;
- customer equipment;
- qualification and reliability documents.

But the part number alone does not prove any specific customer's adoption.

```text
named SKU exists
    !=
customer X bought or deployed it
```

---

# 3. Controlled functional comparisons

## F — comparison with Case 03 refresh-control chronology

Case 03 already requires separation among filing, publication, public product documentation, and product adoption.

Case 04 now exhibits the same general historical discipline in a different technology:

```text
patent / paper chronology
    !=
product / supply chronology
```

This is a **methodological functional comparison**, not evidence that DRAM refresh-control history and NAND commercialization share a causal genealogy.

---

## F — comparison with Case 111 mechanism prior art versus named-product evidence

Case 111 distinguishes a mechanism-level patent/publication floor from later named-product documentation of enterprise-SSD retention maintenance.

Case 04 has the analogous separation:

```text
experimental NAND technical record
    !=
named commercial NAND product record
```

Again, the comparison is about evidence structure, not implementation inheritance.

---

## F — this chronology does not move FTL history backward

The existence of a 4 Mbit NAND product in 1991–1992 does not establish the presence of Ban-style virtual-to-physical mapping, modern garbage collection, wear leveling, TRIM, or an SSD controller.

The canonical Case 04 boundary remains:

```text
NAND device / product chronology
    !=
logical identity maintained by remapping
```

The mapped-storage evidence must stand on its own sources.

---

# 4. Philosophical interpretation

## P — "the year NAND appeared" is an underspecified question

A history that says simply:

```text
NAND appeared in 1989
```

or:

```text
NAND began in 1991
```

has discarded the very distinction the evidence contains.

A more defensible statement is conditional on the event being asked about:

- experimental fabricated/public technical evidence: 1989 in the inspected 4 Mbit papers;
- later KIOXIA commercialization milestone: 1991;
- named TC584000 sample-shipment report: November 1991;
- planned mass-production milestone in that near-contemporary report: April 1992.

The philosophical point for this repository is modest:

> technological existence is not a single transition.

A device may exist as an architecture, a fabricated experiment, a public technical object, a named product, a sample, a volume-manufactured component, and a deployed component at different times.

Those are different forms of technical presence.

---

# 5. Explicit non-claims

This evidence does **not** claim:

1. that 1989 was the first-ever physical NAND implementation;
2. that the 1989 ISSCC/JSSC device was a shipping product;
3. that the 1989 technical papers prove commercial availability;
4. that the later IEEE Spectrum phrase "hit the market" is a contemporaneous shipment record;
5. that IEEE Spectrum's 1989 market date has been reconciled with KIOXIA's 1991 commercialization date;
6. that KIOXIA's later retrospective is equivalent to a 1991 press release;
7. that Toshiba's current `developed` wording and KIOXIA's `commercialized` wording denote the same event;
8. that a corporate `world's first` claim has been independently adjudicated here;
9. that the December 1991 *Electronics Australia* item is Toshiba's original announcement;
10. that `worldwide marketing` means volume availability;
11. that a sample-shipment start means mass production;
12. that the reported November 1991 sample plan was executed on the exact stated day;
13. that the reported April 1992 mass-production plan was executed exactly as scheduled;
14. that TC584000 was the first NAND part sold to any customer anywhere;
15. that a specific customer adopted TC584000 in 1991;
16. that named-product existence proves high-volume customer deployment;
17. that the 1993-priority patent dates first availability of TC584000;
18. that `available from Toshiba` in the later patent means it was available at every earlier date;
19. that 1991 commercialization means invention occurred in 1991;
20. that 1987 invention/announcement, 1989 experimental fabrication, and 1991 commercialization are interchangeable milestones;
21. that patent filing, patent publication, paper publication, development, commercialization, sample shipment, mass production, and adoption are interchangeable;
22. that NAND commercialization proves any FTL was present;
23. that TC584000 implemented Ban's later flash-file-system mapping;
24. that NAND device geometry itself supplies logical-to-physical remapping;
25. that commercializing a component proves a complete storage system was commercially mature;
26. that the near-contemporary report proves long-term reliability or retention performance;
27. that a product datasheet, where later found, would by itself prove shipment volume;
28. that later corporate histories can resolve all contemporary chronology conflicts;
29. that the current chronology is a complete vendor genealogy;
30. that this slice changes Case 04 maturity by itself.

---

# 6. Evidence strength

### Strong for the bounded claim

- 1989 peer-reviewed technical records explicitly label the 4 Mbit device experimental and describe fabrication/operation.
- Current KIOXIA first-party history explicitly labels 1991 commercialization.
- Current Toshiba first-party history explicitly labels 1991 development.
- December 1991 near-contemporary reporting names TC584000 and separates sample shipment from planned mass production.
- A 1993-priority Toshiba-associated patent later names TC584000 as available/practically used.

### Medium / provenance-limited

- The December 1991 report appears to relay contemporary product-news material, but the original Toshiba release has not yet been inspected.
- Current corporate histories are later retrospectives.
- IEEE Spectrum's `hit the market` wording is a later retrospective and conflicts with the 1991 commercialization chronology.

### Still open

- original Toshiba 1991 press release or product announcement;
- contemporaneous Toshiba TC584000 catalog/data-book entry with publication date;
- direct evidence that November 1991 sample shipments actually occurred as planned;
- direct evidence that April 1992 mass production began as planned;
- contemporaneous price/order information;
- named customer qualification or adoption evidence;
- exact first sustained volume-shipment date.

---

# 7. Navigation / effect on Case 04

This file should be read with:

- `evidence/04-toshiba-1987-series-cell-nand-patent-chronology-deepening.md` — concept/patent chronology;
- `evidence/04-1987-1989-nand-device-geometry-before-ftl-deepening.md` — device geometry and experimental technical record;
- `cases/04-flash-virtual-mapping-logical-identity.md` — canonical mapping/identity case.

The sequence is intentionally layered:

```text
series-cell / patent chronology
    -> device / operation geometry
    -> experimental-to-commercial product chronology
    -> later mapped-storage semantics
```

No maturity promotion is claimed from this slice.

---

# 8. Remaining research debt after this slice

The broad question `when did NAND become commercial?` is now too coarse to be useful. The remaining debt is narrower and testable:

1. Find Toshiba's original 1991 announcement for TC584000, if publicly archived.
2. Find a dated Toshiba data book/catalog or pricing record for TC584000.
3. Confirm actual November 1991 sample shipment rather than only the announced plan.
4. Confirm actual April 1992 mass-production start rather than only the announced plan.
5. Find a named early customer/system using TC584000, if evidence survives.
6. Keep broader NAND vendor/product genealogy in `computing-archaeology`; only bring back evidence needed to bound Case 04's retention/mapping chronology.

The working chronology discipline is therefore:

```text
record the source's verb;
record the source's date;
record the source class;
record what is still only planned or retrospective;
do not collapse the result into one magic "first" year.
```
