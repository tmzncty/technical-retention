# Case 04 Deepening — Toshiba 1987 Series-Cell / NAND Patent Chronology Before FTL

## Status

**Bounded deepening complete.**

Parent case: [`../cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md)

Parent device-history evidence: [`04-1987-1989-nand-device-geometry-before-ftl-deepening.md`](04-1987-1989-nand-device-geometry-before-ftl-deepening.md)

This slice closes one narrow item left open by the parent record:

> can primary patent records put firmer dates and circuit structure around Toshiba's 1987 series-connected nonvolatile-cell / NAND work without projecting later FTL semantics backward?

The answer is yes, with an important provenance qualification: **a patent priority or filing date is not automatically a public-disclosure date.**

---

## 1. Research question

The existing Case 04 device-history deepening already separates late-1980s NAND cell/string geometry from the 1992–1995 mapping / FTL evidence.

What remained weak was the patent-side chronology. This pass therefore asks only:

1. what primary patent records can be tied to Toshiba's 1987 series-connected nonvolatile-memory work;
2. what those records actually say about series-cell / NAND geometry and operation granularity;
3. what their priority, filing, and publication dates do — and do not — establish;
4. whether any of this is evidence for logical-to-physical translation, garbage collection, or stable logical identity across relocation.

It is **not** a claim to settle who “invented NAND,” the first commercial NAND shipment, or the complete patent family.

---

## 2. Related-repository check

`tmzncty/computing-archaeology` was searched for `Masuoka`, `5245566`, and the relevant NAND-patent identifiers. No dedicated reusable NAND-patent genealogy module was found.

Accordingly, this file records only the bounded mechanism / chronology needed by `technical-retention`. Broader semiconductor-patent history remains better suited to `computing-archaeology` if that repository later develops the topic.

---

## 3. Sources directly inspected

### 3.1 JP62101427A / JPS63266886A — Masuoka / Toshiba

**Type:** primary patent record; Google Patents rendering includes a machine translation from Japanese.

**Title:** `Nonvolatile semiconductor memory`

**Inventor:** Fujio Masuoka

**Applicant / original assignee shown by the record:** Toshiba Corp.

**Filing / priority date:** 1987-04-24

**Publication:** JPS63266886A, 1988-11-02

**Source:**

- https://patents.google.com/patent/JPS63266886A/en

The record's abstract and claim describe a circuit in which multiple electrically erasable nonvolatile memory cells are connected in series. In the illustrated embodiment, eight cells form one series circuit. The cells have individual control-gate row lines, while their erase-gate electrodes are common within the series circuit and are connected to an erase line through a selectively controlled switching transistor.

The translated abstract states that the arrangement permits selective erasure in byte units while sequential read / write access is performed through the bit and row lines.

The claim is narrower and safer to use than retrospective shorthand: it requires at least two nonvolatile memory cells connected in series, common erase-gate connection within that series circuit, a bit line, row lines, an erase line and a switch transistor controlling the erase connection, plus means for sequentially writing or reading the cells.

### 3.2 US5245566A — later US continuation in the 1987-04-24 priority chain

**Type:** primary patent record in English; useful for inspecting the same priority chain without relying only on machine-translated Japanese prose.

**Title:** `Programmable semiconductor`

**Inventor:** Fujio Masuoka

**US filing:** 1992-06-17

**Publication / grant:** 1993-09-14

**Priority shown:** 1987-04-24, including JP62101427A

**Source:**

- https://patents.google.com/patent/US5245566A/en

The English specification states that the invention includes series circuit units having at least two memory cells connected in series. In its illustrated array, each series circuit unit contains eight series-connected memory cells. It also describes common erase-gate connection inside the series unit and sequential cell read / write behavior.

The specification's stated objectives include reducing wiring and contact overhead while allowing 8-bit / byte-oriented operation.

This US record is useful as a readable continuation-family witness. Its 1993 publication date must not be silently replaced with the 1987 priority date.

### 3.3 US5008856A — Iwahashi / Toshiba explicit NAND-cell structure

**Type:** primary patent record.

**Title:** `Electrically programmable nonvolatile semiconductor memory device with NAND cell structure`

**Inventor:** Hiroshi Iwahashi

**Assignee:** Kabushiki Kaisha Toshiba

**Earliest priority shown:** 1987-06-29

**US filing:** 1988-06-28

**Publication / grant:** 1991-04-16

**Source:**

- https://patents.google.com/patent/US5008856A/en

The specification explicitly describes a selection transistor and multiple floating-gate cell transistors whose current paths are connected in series. It explains the density motivation in terms of sharing the selection transistor across the cell transistors and reducing contact overhead.

The illustrated first embodiment uses four serial cell transistors, while the patent's broader claims / family continue to describe NAND-cell structures rather than a host-visible storage translation layer.

This is a useful primary anchor because the patent itself uses `NAND cell structure` in the title and ties that structure to a 1987-06-29 priority claim.

### 3.4 Masuoka et al. — IEDM 1987 publication record

**Type:** primary peer-reviewed publication record; abstract-level evidence in the parent file, not newly page-by-page inspected here.

**Title:** `New ultra high density EPROM and Flash EEPROM with NAND structure cell`

**Venue:** IEDM 1987, pp. 552–555

**DOI:** `10.1109/IEDM.1987.191485`

The existing parent evidence records the paper's public conference publication in December 1987 and the abstract's NAND-structure density / selective-programming claims.

This matters here because it gives a **public publication node** distinct from the earlier patent priority / filing nodes.

---

## 4. Historical record — three different clocks must stay separate

The patent and paper sources expose at least three different chronological clocks:

```text
priority / filing chronology
    !=
patent publication chronology
    !=
conference-publication chronology
```

For the bounded sources inspected here:

```text
1987-04-24
Masuoka / Toshiba JP62101427A filing + priority
series-connected nonvolatile cells; shared erase relation in the series unit

1987-06-29
Iwahashi / Toshiba earliest priority shown for US5008856A family
explicit NAND-cell structure; serial floating-gate cell transistors

Dec 1987
Masuoka et al. IEDM paper
public NAND-structure publication node already recorded by the parent evidence

1988-11-02
JPS63266886A publication

1991-04-16
US5008856A publication / grant

1993-09-14
US5245566A publication / grant
```

This chronology supports a modest historical statement:

> Toshiba patent records contain 1987 filing / priority claims for series-connected nonvolatile-memory and explicit NAND-cell structures around the same year as the public IEDM NAND paper.

It does **not** support the stronger statement:

> the contents of those later-published patents were necessarily public prior art on their 1987 priority dates.

A priority date is evidence about a patent's claimed filing lineage. Public availability has its own date and evidence.

---

## 5. Patent-priority chronology is not publication chronology

This distinction is important enough to state explicitly:

```text
claimed priority date
    !=
public disclosure date
```

and:

```text
filed before conference
    !=
publicly available before conference
```

For example, US5008856A shows an earliest priority of 1987-06-29, but the US publication / grant shown by the record is 1991-04-16. The inspected source does not justify treating June 1987 as the date on which the later US patent text became public.

Likewise, US5245566A carries a 1987-04-24 priority chain while the US record itself was filed in 1992 and published in 1993.

Therefore this evidence can deepen **internal development / patent-line chronology**, but it must not be used carelessly as a `public prior art no later than 1987-04-24` citation.

This follows the repository's general prior-art discipline: different evidence types answer different dating questions.

---

## 6. Engineering reconstruction — what the patents actually add

### 6.1 Series connection is already an explicit physical organization

Both the Masuoka and Iwahashi patent records expose series-connected cell organization.

A safe physical-layer reconstruction is:

```text
multiple nonvolatile cell transistors
    -> serial current path / shared selection structures
    -> fewer repeated selection/contact structures per stored bit
    -> density advantage and coupled access constraints
```

This is a device-geometry statement.

It is **not** yet:

```text
logical sector LBA
    -> mapping table
    -> current physical page
    -> old physical page invalidated
```

### 6.2 Operation granularity can be structured without being an FTL

The Masuoka priority-chain record describes an eight-cell series unit with common erase-gate relation and byte-oriented erase selection while read / write proceeds sequentially through cells in the series unit.

That yields a bounded distinction:

```text
operation grouping inside a memory array
    !=
logical-address virtualization above the array
```

The Iwahashi patent similarly ties multiple floating-gate cells to one serial NAND structure and shared selection circuitry.

Nothing in these inspected claims requires a host-visible logical identity to survive relocation to another physical location.

### 6.3 Physical sharing creates constraints, not automatically policies

Series organization and shared selection / erase structures can constrain what later controllers must do, but the patents do not thereby establish later policies such as:

- out-of-place update;
- logical-to-physical remapping;
- garbage collection;
- wear leveling;
- TRIM / discard;
- bad-block replacement policy;
- SSD firmware metadata.

The correct relationship is:

```text
physical device geometry
    -> supplies constraints to later storage-system design

physical device geometry
    !=
later controller policy itself
```

---

## 7. Cross-source comparison — the 1987 records are related in time, not proven as one linear genealogy

It is tempting to compress all 1987 Toshiba records into a single line such as:

```text
Masuoka patent -> Iwahashi patent -> IEDM paper -> modern NAND Flash
```

The inspected sources do not justify that arrow chain.

What they safely establish is weaker:

- Masuoka and Toshiba have an April 1987 priority / filing record for series-connected electrically erasable nonvolatile cells;
- Iwahashi and Toshiba have a June 1987 priority record for a patent family explicitly titled around NAND-cell structure;
- Masuoka, Momodomi, Iwata, and Shirota publicly presented a NAND-structure EPROM / Flash EEPROM paper at IEDM later in 1987;
- all are contemporaneous Toshiba-associated technical records around serial nonvolatile-cell density and operation.

That supports **contemporaneous technical proximity**.

It does not by itself prove:

- which document or inventor directly influenced which other document;
- that one patent contains the exact circuit disclosed in the IEDM paper;
- that the patent priority date is an invention date;
- that the patents establish firstness over all other actors;
- that one linear genealogy leads from these records to every later NAND product.

---

## 8. Functional comparison with the later Case 04 mapping layer

The late-1980s device records and the later mapping evidence answer different questions.

### Device-layer question

```text
How can many nonvolatile cells be physically organized,
selected, programmed, read, and erased with high density?
```

### Mapped-storage question

```text
When a logical address is rewritten out of place,
which physical embodiment is authoritative now,
and how is obsolete capacity later reclaimed?
```

The first can exist without the second.

Thus:

```text
serial NAND geometry
    !=
logical identity continuity

shared erase/program structure
    !=
garbage collection

physical current path
    !=
authority relation between old and new physical embodiments
```

This is the core technical-retention reason to keep the patent slice separate from later FTL sources.

---

## 9. Cross-case comparison

### Case 01 / Case 78 — raw NAND physical management

Cases 01 and 78 deal with lower-layer bad-block / reserve relations in raw NAND contexts. The 1987 patent material here is useful only as an earlier physical-geometry anchor: it shows that serial cell structure and shared device resources belong to the medium / array layer.

Functional comparison:

```text
physical NAND geometry and device constraints
    -> lower-layer physical management problem

logical translation / currentness
    -> separate metadata-governance problem
```

No direct genealogy from these patents to a particular later bad-block-management algorithm is claimed.

### Case 04 — FTL / mapped Flash

Case 04 adds a later retained relation that these device patents do not:

```text
logical identity -> current physical embodiment
```

That retained mapping relation is exactly why later Flash systems can preserve stable logical identity while physical embodiment changes.

The 1987 patent evidence strengthens the **boundary before that abstraction**, not an early occurrence of the abstraction itself.

---

## 10. Philosophical interpretation

The technical record can support one bounded project-level interpretation:

> a medium may already have highly structured physical grouping, shared resources, and operation granularity before a storage system introduces a separate retained relation for the continuity of logical identity.

In other words:

```text
physical organization
    !=
identity rule
```

The patents themselves do not use the repository's philosophical vocabulary. This interpretation must remain downstream of the historical and engineering record.

---

## 11. Explicit non-claims

This evidence does **not** claim:

1. that 1987-04-24 or 1987-06-29 is the invention date of NAND Flash;
2. that a patent priority date is automatically a public prior-art date;
3. that US5245566A was publicly available in 1987;
4. that US5008856A was publicly available in June 1987;
5. that Masuoka's April patent family is identical to the December IEDM NAND paper;
6. that Iwahashi's June patent family is identical to the December IEDM NAND paper;
7. that the two patent families prove a direct inventor-to-inventor influence chain;
8. that Toshiba was necessarily the first actor to use every serial-cell, shared-select, EEPROM, or NAND-like technique;
9. that an eight-cell or four-cell example establishes a universal NAND string length;
10. that byte-oriented erasure in the Masuoka patent is the same thing as later NAND block erase;
11. that device-level erase / program grouping is garbage collection;
12. that the patents describe logical-to-physical mapping, wear leveling, TRIM, SSD firmware, or a modern FTL;
13. that patent filing proves commercial implementation or shipment;
14. that later US continuation-family wording can be silently projected into the exact text available in the Japanese application on its filing day;
15. that this bounded slice settles the complete Toshiba NAND patent genealogy.

---

## 12. Resulting bounded distinctions

```text
1987 patent priority / filing node
    !=
1987 public disclosure node

series-connected nonvolatile cells
    !=
FTL

explicit NAND-cell structure
    !=
logical-to-physical remapping

shared selection / erase relations
    !=
garbage collection

physical operation granularity
    !=
host-visible identity granularity

patent chronology
    !=
invention chronology
    !=
commercialization chronology

contemporaneous Toshiba records
    !=
proved linear genealogy
```

---

## 13. What this slice closes

The parent evidence previously left `earlier NAND-string patent / device genealogy` broadly open.

This pass closes a narrow portion of that debt:

> **primary 1987 Toshiba patent records now provide a directly inspected series-cell / explicit-NAND chronology around the IEDM publication, with priority dates kept separate from publication dates and with no FTL semantics projected backward.**

It also establishes a reusable source-control rule for Case 04:

```text
priority date is evidence for patent-line chronology;
publication date is evidence for public availability.
```

---

## 14. Remaining work

Still open:

- obtain and directly inspect the full 1987 IEDM paper if a reliable renderable copy becomes available;
- inspect the original Japanese application images / file wrappers where wording differences from later English continuations matter;
- build the **full** Toshiba 1987–1990 NAND patent-family graph only if that genealogy becomes materially useful;
- directly inspect and pin the earliest PCMCIA `Flash Translation Layer` wording node;
- inspect later NFTL patent / specification chronology where it changes the Case 04 mapping story;
- establish commercial shipment chronology from contemporary Toshiba product announcements, datasheets, catalogs, or trade records rather than retrospective summaries;
- find direct citation / actor evidence before asserting a Toshiba-device-paper -> Ban / PCMCIA / FTL influence chain.

The bounded patent slice itself is complete.