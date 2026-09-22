# Case 04 evidence deepening — Toshiba TC584000: dated databook witness, supply-status caution, and SSD system boundary (1991–1993)

## Scope

This note closes one bounded gap left by the existing Case 04 commercialization chronology:

> Can the named `TC584000` be anchored to a dated Toshiba databook, and what do near-contemporary 1991–1993 sources actually establish about product status and solid-state-disk use without collapsing component availability into a shipping SSD system?

The answer is now stronger but still deliberately limited.

The currently inspected evidence supports:

```text
Dec 1991
    near-contemporary report:
    worldwide marketing begun;
    samples reported as due to start Nov 1991;
    mass production reported as planned for Apr 1992

6 Apr 1992
    near-contemporary Dataquest analysis:
    Toshiba "plans to introduce" TC584000;
    device explicitly positioned for rigid-disk / solid-state-storage use

24 Aug / 6 Nov 1992
    near-contemporary Dataquest records:
    IBM + Toshiba technology agreement to develop solid-state files
    using Toshiba NAND technology + IBM controller/interface technology

1993
    Toshiba MOS Memory (Non-Volatile) Databook
    contains a TC584000P/F/FT/TR datasheet
    (publication identity independently recorded by USPTO/PTAB)

16 Mar 1993 priority horizon
    Toshiba-authored patent background:
    TC584000 described as available and practically used
```

This slice does **not** prove that the December-1991 April-1992 mass-production plan was executed on schedule, identify the first paying customer, or establish that the IBM/Toshiba solid-state-file work used `TC584000` specifically.

It also does not move later FTL terminology or controller semantics backward into the component record.

---

## Evidence classes and source custody

Following `docs/METHOD.md`, the layers below remain explicit:

- **Historical record** — what dated sources say about the named component, its publication status, and system/application plans;
- **Engineering reconstruction** — what can safely be inferred from the separation among NAND component, controller/interface, and system product;
- **Functional analogy** — bounded comparison with other repository cases only at the level of evidence structure or logical/physical separation;
- **Philosophical interpretation** — a downstream observation about technological presence and retained identity, never a substitute for the product record.

Source hierarchy in this slice:

1. Toshiba-authored patent material with 1993 priority;
2. official USPTO/PTAB records identifying the Toshiba 1993 databook/datasheet as a printed publication;
3. near-contemporary Dataquest industry analysis dated 1991–1992;
4. the already-inspected December-1991 *Electronics Australia* report for the earlier marketing/sample/mass-production-plan chain.

A web-searchable mirror of the Toshiba datasheet is useful for source discovery, but the current research environment could not retrieve the PDF for page-level inspection. This note therefore does **not** claim a fresh facsimile audit of every electrical/timing table. The dated publication identity is instead anchored by the official USPTO/PTAB record, while technical claims are kept to what the inspected source text directly supports.

---

# 1. Historical record

## H/B — December 1991 already separates marketing, samples, and planned mass production

The existing commercialization chronology established from *Electronics Australia* (December 1991) that Toshiba had begun worldwide marketing of the 4 Mbit NAND EEPROM `TC584000`.

That same near-contemporary report says:

- sample shipments were **to start in November 1991**;
- mass production **will begin in April 1992**.

Source:

- *Electronics Australia*, December 1991, `Solid State Update`, `First 4Mb NAND EEPROM`;
- archival scan: <https://www.worldradiohistory.com/AUSTRALIA/Electronics-Australia/EA-1991-12.pdf>.

The wording matters. It supports a reported plan/status chain, not an audited shipment ledger:

```text
marketing begun
    !=
sample-shipment plan
    !=
confirmed sample shipment
    !=
mass-production plan
    !=
confirmed volume-production execution
```

This slice keeps that distinction intact rather than treating `April 1992` as already-proven volume production.

---

## H/B — 6 April 1992 Dataquest still uses future-tense `plans to introduce`

A Dataquest `Memories Worldwide` report dated **6 April 1992** discusses contemporary Flash offerings and says:

> `Finally Toshiba plans to introduce the TC584000, 5V-only 4MB flash EEPROM with block erase capability ...`

The same passage says that some Flash EEPROM designs trade speed for die-size reduction and are aimed at rigid-disk applications where electromechanical-disk-like access time is acceptable; it explicitly says the Toshiba `TC584000` fits that category.

Source:

- Nicolas Samaras, Dataquest, `Memories Worldwide`, `MMRY-SEG-DP-9202`, 6 April 1992;
- searchable archival reproduction: <https://manuals.plus/m/367d3722d10ebe69bcfa8b0fd2958ee3baa35cfcf696ac7e31efa344e5179bc5>.

This is a useful chronology check because the date is essentially the same month that the December-1991 report had named as the planned start of mass production.

But it must be interpreted conservatively:

```text
Dataquest says "plans to introduce" on 6 Apr 1992
    !=
proof that Toshiba had not begun any production by that date
```

Possible explanations include editorial lag, different milestone vocabulary, or a real schedule change. No inspected source presently resolves that ambiguity.

Therefore the evidence changes the repository's confidence in one direction only:

```text
reported Apr-1992 mass-production plan
    !=
confirmed Apr-1992 production execution
```

It does **not** establish the opposite claim that production definitely had not started.

---

## H/B — late-1991 Dataquest positions the NAND component toward SSD use, but application target is not deployment

A Dataquest memory-card / solid-state-storage discussion dated **December 1991** describes companies working on solid-state-disk replacement and treats Toshiba's dense 5 V NAND EEPROM as aimed at the SSD market and architecturally suitable for SSD implementations.

The searchable OCR renders the part number once as `TC58400`, apparently dropping one zero. Because other contemporary and Toshiba records consistently identify the 4 Mbit part as `TC584000`, this note does **not** silently use that OCR token as a separate product identity. The passage is used only as application-positioning evidence.

Source:

- Dataquest, `Memories Worldwide`, memory-card / solid-state-storage discussion, December 1991;
- searchable archival reproduction: <https://manuals.plus/m/367d3722d10ebe69bcfa8b0fd2958ee3baa35cfcf696ac7e31efa344e5179bc5>.

The bounded result is:

```text
NAND component positioned for SSD implementation
    !=
shipping SSD subsystem
    !=
named customer deployment
```

The distinction matters because the same Dataquest discussion separately names actual SSD subsystem vendors/products. Component positioning and subsystem shipment are different evidence categories.

---

## H/B — 1992 IBM/Toshiba agreement makes the component/controller boundary historically visible

Dataquest's **24 August 1992** `Memories Worldwide` analysis states that IBM and Toshiba had, within the preceding months, negotiated a technology agreement to develop **solid-state files (SSFs)** using:

- Toshiba's NAND Flash technology; and
- IBM's advanced controller and interface technology.

A Dataquest Europe report dated **6 November 1992** repeats the same bounded point.

Sources:

- Dataquest, `Memories Worldwide`, 24 August 1992, searchable archival reproduction: <https://manuals.plus/m/367d3722d10ebe69bcfa8b0fd2958ee3baa35cfcf696ac7e31efa344e5179bc5>;
- Dataquest Europe, `Semiconductors Europe`, 6 November 1992, Computer History Museum archive: <https://archive.computerhistory.org/resources/access/text/2013/04/102723261-05-01-acc.pdf>.

This is valuable for Case 04 because a near-contemporary source itself separates the ingredients:

```text
Toshiba NAND technology
    +
IBM controller/interface technology
    ->
planned/developing solid-state-file system
```

The source does **not** state that the system used `TC584000` specifically, nor does it identify a shipping SSF model in the cited passage.

Therefore:

```text
IBM/Toshiba SSF development agreement
    !=
TC584000 design-in proven
    !=
shipping named IBM/Toshiba SSD proven
```

The evidence is system-architecture / development-intent evidence, not customer-adoption evidence.

---

## H/P-provenance — official USPTO/PTAB records identify a Toshiba 1993 databook containing the TC584000 datasheet

The earlier Case 04 evidence index listed a dated Toshiba databook/catalog/order document for `TC584000` as an open debt.

That broad debt can now be narrowed substantially.

In `IPR2014-00113`, the U.S. Patent Trial and Appeal Board's public record identifies:

> `1993 MOS Memory (Non-Volatile) Databook containing Datasheet for Toshiba's TC584000P/F/FT/TR CMOS NAND`

as Exhibit 1009 / the `1993 Databook`.

The accompanying expert declaration likewise identifies the exhibit as:

> `Datasheet for TC584000P/F/FT/TR CMOS NAND E²PROM ... published in Toshiba 1993 MOS Memory (Non-Volatile) Databook`

Sources:

- USPTO/PTAB, `IPR2014-00113`, public record / decision identifying Exhibit 1009: <https://ptacts.uspto.gov/ptacts/public-informations/petitions/1460512/download-documents?artifactId=a-JLWeC3jUOnKDZ3ruY7jT9eY0cN3FEGNClCIvbIoFc0g4K9QP7k5Bw>;
- supporting expert declaration identifying the same Toshiba publication: <https://ptacts.uspto.gov/ptacts/public-informations/petitions/1460512/download-documents?artifactId=yRCVJkGgUuRI7cc5vzOHIPujlsiputbEHGnBim9D5OnZjU-kxAIXFh4>.

This is a **later official institutional provenance record about a 1993 printed Toshiba publication**. It establishes a dated databook witness much more strongly than an undated third-party datasheet mirror.

Supported:

```text
1993 Toshiba MOS Memory (Non-Volatile) Databook
    -> contains TC584000P/F/FT/TR datasheet
```

Not supported by this record alone:

```text
1993 databook date
    -> first product availability date

1993 datasheet
    -> product first shipped in 1993

1993 printed publication
    -> proves Apr-1992 mass-production plan executed
```

The dated-databook debt is therefore **partially closed at the 1993 publication horizon**, while the earlier 1991–1992 ordering/catalog/price-list chronology remains open.

---

## H/P-later — Toshiba-authored 1993-priority patent describes TC584000 as available and practically used

A Toshiba-assigned patent family with priority **16 March 1993** describes a NAND EEPROM used in an IC memory-card arrangement and states that a 4 Mbit NAND EEPROM such as `TC584000`, available from Toshiba Corporation, is `practically used at present`.

The same background separates:

- NAND EEPROM media;
- a control IC mounted in the memory card;
- the NAND device's internal high-voltage generation needed for write/erase;
- the external card/interface environment.

Source:

- Toshiro Sato et al., `US5469399A`, *Semiconductor memory, memory card, and method of driving power supply for EEPROM*;
- priority 16 March 1993;
- <https://patents.google.com/patent/US5469399A/en>.

For chronology, this gives a useful later lower-bound corroboration:

```text
by the 16-Mar-1993 priority horizon
    TC584000 is described by Toshiba inventors
    as available / practically used
```

It still does not identify first sample date, first commercial sale, production volume, or first customer.

For system architecture, the patent also reinforces a distinction that matters to Case 04:

```text
NAND device
    !=
control IC
    !=
complete memory-card / storage-system behavior
```

That is contemporary engineering vocabulary, not a modern FTL label being projected backward.

---

# 2. Engineering reconstruction

## E — supply status must remain multi-valued

The combined evidence now blocks any attempt to encode `commercialization` as one Boolean or one year.

A safer event-state model is:

```text
public technical device
    ->
marketing / announcement
    ->
planned samples
    ->
confirmed samples
    ->
planned mass production
    ->
confirmed mass production
    ->
dated databook / datasheet presence
    ->
practical availability statement
    ->
named customer / system adoption
```

The present record occupies several of those states but not all of them.

Most importantly:

```text
Dec-1991 plan says Apr-1992 mass production
    +
6-Apr-1992 analyst report says "plans to introduce"
        ->
Apr-1992 execution remains unresolved
```

This is not a contradiction that should be forcibly harmonized. It is a provenance-sensitive uncertainty that should remain visible until a Toshiba production, ordering, or customer record closes it.

---

## E — a dated datasheet is a product-document witness, not an availability timestamp

The USPTO/PTAB record closes a useful document-history gap:

```text
1993 Toshiba databook
    -> named TC584000 datasheet definitely present
```

But the temporal inference must stop there.

A datasheet can remain in a databook after a product has already been introduced, can precede broad volume availability, or can describe variants not equally available in every market.

Therefore:

```text
dated product documentation
    !=
first sample
    !=
first sale
    !=
first high-volume shipment
```

This is the same chronology discipline already used elsewhere in the repository for DRAM patents, SSD manuals, and standards-era feature documentation.

---

## E — NAND substrate availability does not itself create stable logical identity

The 1992 IBM/Toshiba development report makes a system boundary visible in period terms:

```text
NAND Flash technology
    !=
controller/interface technology
```

A raw component can provide nonvolatile cells, page/block operations, and a physical addressing organization without yet providing the host-visible logical-identity semantics studied in the canonical Case 04.

The later Case 04 mapping evidence requires additional state and machinery, including currentness/allocation relations and logical-to-physical resolution.

Therefore:

```text
NAND chip exists
    !=
solid-state file exists
    !=
FTL exists
    !=
stable logical block identity across relocation proven
```

This is more than an abstract modern distinction because the 1992 Dataquest report itself assigns NAND technology and controller/interface technology to different sides of the IBM/Toshiba development agreement.

---

## E — block erase remains a substrate operation, not garbage collection

The April-1992 Dataquest description calls out block-erase capability for the `TC584000` and explicitly places the device in disk-like application discussions.

That combination is exactly where later terminology can become tempting but anachronistic.

The safe relation is:

```text
physical block erase capability
    +
storage application target
        !=
controller-level garbage collection proven
```

Likewise:

```text
page/block NAND organization
    !=
logical invalidation
    !=
copy-current / erase-old reclamation
    !=
wear-leveling policy
```

Those later mapping/maintenance claims must continue to stand on their own sources.

---

## E — application positioning is weaker than system adoption

The Dataquest sources make it clear that contemporaries already saw dense NAND as suitable for disk-replacement use.

That matters historically, but it should not be overread:

```text
technology judged suitable for SSD
    !=
controller completed
    !=
qualified subsystem shipped
    !=
customer deployed it
```

The IBM/Toshiba agreement strengthens the system-level development context but still remains an agreement to develop, not a shipment record.

---

# 3. Controlled functional comparisons

## F — comparison with Case 03 patent/product chronology

Case 03 already separates:

```text
patent filing
    !=
patent publication
    !=
product documentation
    !=
shipping implementation
```

This Case 04 slice shows the analogous commercial-document boundary:

```text
marketing report
    !=
sample plan
    !=
production plan
    !=
dated databook
    !=
practical-availability statement
    !=
customer adoption
```

This is a **functional comparison of evidence states**, not a shared technical genealogy.

---

## F — comparison with later mapped Flash

The early component/system split provides a bounded precursor to the later Case 04 logical-identity problem:

```text
physical medium
    +
controller/interface
```

is already a system composition in 1992.

But the stronger later relation:

```text
logical identity remains stable
while physical embodiment changes
```

requires independent mapping evidence and must not be back-projected into this 1991–1993 component chronology.

---

## F — comparison with SSD named-product evidence

Later SSD cases in this repository often distinguish:

```text
mechanism prior art
    !=
named product
    !=
firmware / implementation epoch
    !=
operator-visible behavior
```

The TC584000 chronology demands the same discipline at an earlier level:

```text
NAND mechanism/device
    !=
named component
    !=
application positioning
    !=
subsystem implementation
```

Again, this is methodological comparison only.

---

# 4. Philosophical interpretation

## P — technical presence is layered by apparatus

The narrow conceptual result is not that a component is somehow `incomplete` until it becomes an SSD.

Rather, different retained objects appear at different apparatus layers:

```text
TC584000 cell / array state
    -> physical nonvolatile component state

controller + interface + policy state
    -> host-resolvable storage behavior

complete solid-state file / memory card
    -> service-level retained object for a system/user
```

A component can be historically and materially real before a later logical-storage object exists.

For `technical-retention`, this reinforces a recurring rule:

> retention properties belong to a specified layer and access apparatus, not automatically to every system built from the same medium.

This is a project-level interpretation. It is not a claim that Toshiba, IBM, or Dataquest used the repository's philosophical vocabulary.

---

# 5. Explicit non-claims

This evidence does **not** claim:

1. that the December-1991 report proves sample shipments occurred exactly as planned;
2. that mass production definitely began in April 1992;
3. that Dataquest's 6-April-1992 `plans to introduce` phrase proves production had not begun;
4. that one source's `introduction`, another's `marketing`, and another's `mass production` are synonyms;
5. that the 1993 databook is the first Toshiba document to list TC584000;
6. that the 1993 databook date is the product's first availability date;
7. that every package suffix `P/F/FT/TR` had identical introduction timing;
8. that a dated datasheet proves volume shipment;
9. that the IBM/Toshiba SSF agreement named `TC584000`;
10. that the IBM/Toshiba agreement produced a shipping SSD by 1992;
11. that the agreement proves a specific FTL implementation;
12. that block erase is garbage collection;
13. that NAND page/block geometry is logical remapping;
14. that an SSD application target is customer adoption;
15. that `solid-state file`, `solid-state disk`, and later standards-era `SSD` denote one unchanged product category in every source;
16. that a control IC in the 1993 patent is equivalent to a later standardized FTL;
17. that current third-party datasheet mirrors alone establish original publication date;
18. that this slice resolves the 1989-versus-1991 retrospective commercialization-date conflict already recorded elsewhere;
19. that any one document settles invention priority;
20. that broader Toshiba/IBM NAND-controller genealogy belongs in this repository rather than `computing-archaeology`.

---

# 6. Related-repository routing

A fresh search of `tmzncty/computing-archaeology` for:

- `NAND flash TC584000 solid-state file 1991 Toshiba IBM`

returned no dedicated packet to reuse in this round.

That does not move the broad engineering history here.

Keep in `technical-retention` only the retention-specific seams:

- component state versus controller/interface state;
- product-document chronology versus supply/adoption chronology;
- physical block operation versus later logical-identity semantics;
- application positioning versus retained service contract.

Route broad work on Toshiba/IBM SSF development, controller architecture, semiconductor manufacturing, vendor competition, and exact commercial genealogy primarily to `computing-archaeology` if/when it is developed.

---

# 7. What this slice closes

Before this slice, the Case 04 device index contained the broad debt:

> obtain a dated Toshiba data book, catalog, price list, or ordering document for `TC584000`.

The result is now narrower:

```text
1993 dated Toshiba databook / datasheet witness
    = established through official USPTO/PTAB provenance record

1991–1992 original Toshiba catalog / price / ordering evidence
    = still open

exact first sample / first sale / mass-production execution
    = still open
```

The second improvement is architectural rather than chronological:

```text
1992 near-contemporary system-development record
    separates NAND technology
    from controller/interface technology
```

That gives Case 04 a period-grounded guardrail against projecting later logical-storage semantics directly onto the existence of the NAND chip.

---

# 8. Remaining bounded debt

Highest-value follow-ons are now:

1. locate Toshiba's original 1991 `TC584000` announcement / press material;
2. locate a **1991 or 1992** Toshiba catalog, price list, sample notice, distributor sheet, or order code for the named part;
3. confirm whether the reported November-1991 sample shipments occurred, and on what scope/geography;
4. confirm whether the planned April-1992 mass-production milestone was executed, delayed, or described differently by Toshiba;
5. locate the original 1993 Toshiba databook scan/exhibit with page-level provenance if a later argument needs exact electrical/timing anchors;
6. identify a named early customer, board, memory card, or system using `TC584000`;
7. investigate the IBM/Toshiba SSF program only if a source can tie a named NAND part, controller, prototype, or shipment to it;
8. keep FTL terminology, mapping recovery, garbage collection, and wear-leveling chronology on their independent evidence chains;
9. route broad Toshiba/IBM product genealogy and semiconductor-market history to `computing-archaeology`.

---

## Status

Case 04 remains **`grounded`** in the canonical case and ROADMAP.

`CASE_INDEX.md` is currently empty on `main`, so this slice does not invent or reconstruct a maturity-ledger entry and makes no maturity promotion.

The contribution is narrower and evidence-bearing:

```text
named NAND component
    !=
confirmed supply milestone
    !=
dated product documentation
    !=
controller/interface system
    !=
shipping storage product
    !=
later mapped-storage semantics
```

That separation closes a document-provenance gap while preserving the unresolved commercialization and adoption questions instead of papering them over.