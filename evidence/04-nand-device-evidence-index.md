# Case 04 — NAND device / commercialization evidence index

## Scope

This index groups the early NAND substrate and commercialization evidence that feeds the canonical Case 04:

- `cases/04-flash-virtual-mapping-logical-identity.md`

It is intentionally **not** a complete history of NAND Flash, FTLs, SSD controllers, or flash-file systems. Its purpose is to keep five evidence layers from collapsing into one another:

```text
series-cell / patent chronology
    !=
device geometry / experimental fabrication
    !=
commercial product / supply chronology
    !=
component-to-controller / system boundary
    !=
logical-identity remapping semantics
```

The current update does not claim a Case 04 maturity promotion.

`CASE_INDEX.md` is currently empty on `main`; this index therefore does not invent or silently reconstruct the repository-wide maturity ledger. The canonical Case 04 and ROADMAP both remain the local status anchors for this bounded update.

---

# 1. Evidence chain

## 1.1 Series-cell NAND concept and patent chronology

Primary file:

- `evidence/04-toshiba-1987-series-cell-nand-patent-chronology-deepening.md`

Use it for:

- early series-cell NAND patent/publication chronology;
- the distinction among filing/priority, publication, and later historical reconstruction;
- avoiding a false one-date invention story.

Do **not** use it by itself to prove:

- a named shipping product;
- volume manufacture;
- customer adoption;
- FTL-like virtual-to-physical mapping.

---

## 1.2 1987–1989 NAND device geometry before FTL

Primary file:

- `evidence/04-1987-1989-nand-device-geometry-before-ftl-deepening.md`

Use it for:

- series-string / device organization;
- page/block physical operation;
- experimental 4 Mbit NAND technical evidence;
- the boundary between NAND physical geometry and later logical mapping abstractions.

Core guardrail:

```text
NAND string / page / block geometry
    !=
FTL logical identity
```

A physical NAND array can exist without demonstrating later controller-level remapping semantics.

---

## 1.3 1989–1992 experimental-to-commercial chronology

Primary file:

- `evidence/04-toshiba-1989-1992-nand-prototype-commercialization-chronology-deepening.md`

This slice adds the missing commercial milestone vocabulary around the early 4 Mbit NAND record.

Current bounded chain:

```text
1989
    experimental 4 Mbit NAND technical publication

1991
    later first-party development / commercialization milestones

Nov 1991
    near-contemporary report of TC584000 sample shipment start

Apr 1992
    same report's planned mass-production start
```

The evidence intentionally preserves the source's own milestone verb and provenance.

Core guardrails:

```text
experimental technical disclosure
    !=
named product
    !=
commercialization claim
    !=
sample shipment
    !=
mass production
    !=
customer adoption
```

and:

```text
reported plan
    !=
proved execution of that plan
```

The named `TC584000` part is a stronger product anchor than a generic statement that “4 Mbit NAND existed,” but it does not by itself prove an end-user adoption event.

---

## 1.4 1991–1993 TC584000 databook / supply-status / SSD-system boundary

Primary file:

- `evidence/04-toshiba-1991-1993-tc584000-databook-ssd-positioning-deepening.md`

This slice narrows two debts left by the commercialization chronology.

First, official USPTO/PTAB records identify a **1993 Toshiba `MOS Memory (Non-Volatile) Databook` containing the `TC584000P/F/FT/TR` datasheet**. A dated Toshiba databook witness is therefore now established at the 1993 horizon, although the first 1991–1992 catalog/order/price-list appearance remains open.

Second, near-contemporary Dataquest material sharpens the supply and system boundary:

```text
Dec 1991
    marketing / sample / planned-production report

6 Apr 1992
    Dataquest still says Toshiba "plans to introduce" TC584000
    and positions it for disk-like / solid-state-storage use

Aug–Nov 1992
    IBM + Toshiba agreement to develop solid-state files
    = Toshiba NAND technology + IBM controller/interface technology

1993
    dated Toshiba databook witness
    + Toshiba-authored patent describing TC584000 as available / practically used
```

This does **not** prove that April-1992 mass production failed to begin. The April analyst wording may reflect editorial lag, terminology differences, or schedule reality. Its value is narrower:

```text
planned mass-production date
    !=
confirmed production execution
```

The IBM/Toshiba material supplies a historically useful layer boundary:

```text
NAND technology
    !=
controller / interface technology
    !=
complete solid-state-file implementation
```

It does not name `TC584000` as the NAND part used by that program and does not prove a shipping IBM/Toshiba SSD.

Core guardrails:

```text
dated datasheet
    !=
first availability date

SSD application positioning
    !=
customer adoption

physical block erase
    !=
garbage collection

NAND component existence
    !=
FTL semantics
```

---

## 1.5 Canonical mapped-storage semantics

Canonical file:

- `cases/04-flash-virtual-mapping-logical-identity.md`

Use it for the later logical-identity problem:

- physical movement versus logical stability;
- mapping as retained state;
- the difference between payload presence and the metadata needed to recover logical identity.

The early NAND evidence in this index constrains substrate chronology; it must not be used to move FTL history backward without independent mapping/controller evidence.

---

# 2. Cross-layer decomposition

The current Case 04 evidence should be read as a layered sequence rather than a single “origin of NAND” story:

```text
physical series-cell idea
    ->
experimental NAND device
    ->
named commercial component / supply milestones
    ->
component + controller/interface system development
    ->
later mapped-storage semantics
```

Each arrow requires its own evidence.

A claim that is valid at one layer is not automatically valid at the next.

Examples:

```text
paper describes fabricated device
    !=
product shipped

product exists
    !=
customer deployed it

dated databook lists product
    !=
first shipment date

NAND technology is selected for an SSF program
    !=
named NAND part / controller implementation proven

NAND product exists
    !=
FTL exists

physical block replacement is possible
    !=
logical address identity is preserved
```

The 1992 IBM/Toshiba development record is particularly useful because a near-contemporary source itself separates **NAND technology** from **controller/interface technology**. The canonical mapping case should continue to require independent evidence for the metadata/currentness machinery that preserves logical identity across physical replacement.

---

# 3. Historical-chronology discipline

The commercial-chronology deepenings expose a general rule worth making explicit for this case:

```text
date alone
    -> insufficient historical assertion

date
+ milestone verb
+ source class
+ provenance
+ unresolved conflict where present
    -> reviewable historical assertion
```

The repository should therefore keep the following terms separate unless a source explicitly bridges them:

- invention / conception;
- patent filing or priority;
- patent publication;
- experimental fabrication;
- public technical disclosure;
- corporate development milestone;
- commercialization claim;
- marketing announcement;
- planned sample shipment;
- confirmed sample shipment;
- planned mass-production start;
- confirmed mass-production start;
- named-product availability;
- dated databook / datasheet presence;
- application positioning;
- system-development agreement;
- subsystem shipment;
- sustained customer adoption.

This is especially important where later retrospectives disagree in wording or year, or where a contemporaneous analyst uses future-tense language near a previously announced production milestone.

---

# 4. Evidence classes

Following `docs/METHOD.md`:

### Historical record

Directly records what a paper, patent, contemporary report, corporate chronology, manual, databook-provenance record, or other source says or demonstrates.

### Engineering reconstruction

Combines bounded records into a technical relation while keeping inference visible, for example:

```text
experimental success
    !=
manufacturing readiness
    !=
supply availability
```

or:

```text
nonvolatile NAND component
    !=
controller/interface machinery
    !=
logical-identity mapping contract
```

### Functional analogy

May compare the evidence structure with other cases, such as Case 03 filing/publication/product chronology or Case 111 mechanism-prior-art versus named-product evidence.

Such comparisons do not establish genealogy.

### Philosophical interpretation

May discuss why “technological existence” is not a single transition, or why retention properties are layer/apparatus-specific, but it must remain downstream of the historical and engineering record.

---

# 5. Current source-strength picture

## Strong for bounded claims

- 1989 peer-reviewed technical records explicitly present an experimental 4 Mbit NAND device and its operation.
- Current KIOXIA first-party history assigns a 1991 commercialization milestone to 4 Mbit NAND.
- Current Toshiba history uses a 1991 development milestone for 4-megabit NAND-type EEPROM.
- December 1991 near-contemporary product reporting names `TC584000` and separates marketing, sample shipment, and planned mass production.
- 6 April 1992 Dataquest material explicitly names `TC584000`, uses future-tense introduction language, and places it in rigid-disk / solid-state-storage application discussion.
- August/November 1992 Dataquest records identify an IBM/Toshiba agreement to develop solid-state files using Toshiba NAND technology plus IBM controller/interface technology.
- Official USPTO/PTAB records identify a Toshiba **1993 MOS Memory (Non-Volatile) Databook** containing the `TC584000P/F/FT/TR` datasheet.
- A Toshiba-authored patent with 16 March 1993 priority describes `TC584000` as available / practically used by that later horizon.

## Provenance-limited / unresolved

- current corporate histories are retrospective;
- the December 1991 product report is not yet the original Toshiba announcement;
- the exact execution of the November-1991 sample plan remains unverified;
- the reported April-1992 mass-production milestone remains a plan rather than a directly confirmed execution event;
- Dataquest's 6-April-1992 `plans to introduce` wording does not by itself prove either delay or non-production;
- the 1993 databook witness does not date first availability;
- the original 1993 databook pages have not yet been page-level inspected in this research environment;
- the IBM/Toshiba SSF agreement does not identify `TC584000` as its NAND component;
- a later IEEE Spectrum retrospective uses a 1989 `hit the market` formulation that should not simply be merged with KIOXIA's 1991 `commercialization` date.

---

# 6. Remaining research debt

The broad questions `when did NAND become commercial?` and `was TC584000 used in SSDs?` are no longer precise enough. Remaining work should target specific evidence gaps:

1. original Toshiba 1991 `TC584000` announcement or press material;
2. **1991 or 1992** Toshiba catalog, price list, sample notice, distributor sheet, or ordering material for `TC584000` — the broad dated-databook debt is now partly closed by the 1993 databook witness;
3. direct confirmation that the reported November 1991 sample shipment actually occurred;
4. direct confirmation that the planned April 1992 mass-production start occurred, was delayed, or was described differently by Toshiba;
5. the original 1993 Toshiba databook / Exhibit 1009 pages with page-level provenance if exact electrical/timing claims become necessary;
6. a named early customer, board, card, or system using `TC584000`, if surviving evidence exists;
7. a named NAND part, controller, prototype, or shipment tied directly to the IBM/Toshiba 1992 SSF program, if any source survives;
8. direct primary review of any still-indirectly sourced 1988/1989 device-conference pages needed by the earlier chronology;
9. broader NAND vendor/product and IBM/Toshiba SSF genealogy should remain in `tmzncty/computing-archaeology` unless it changes a retention or mapping claim here;
10. do not infer FTL/controller adoption from NAND component availability, block-erase capability, or SSD application positioning.

---

# 7. Related-repository routing

A fresh search of `tmzncty/computing-archaeology` for `NAND flash TC584000 solid-state file 1991 Toshiba IBM` returned no dedicated packet to reuse in this round.

If that repository later develops the Toshiba/IBM SSF or early NAND-product story, Case 04 should link it and retain only the retention-specific distinctions here:

- substrate/component state versus controller/interface state;
- product-document chronology versus supply/adoption chronology;
- physical page/block operations versus logical-identity semantics;
- application positioning versus shipping service contract.

---

# 8. Status

Case 04 remains **`grounded`** in the canonical case and ROADMAP. No maturity promotion is made.

The useful progress is narrower:

```text
before:
    early NAND chronology had a named-product report
    but the dated Toshiba databook and component/controller boundary were still loose

after:
    1993 Toshiba databook provenance is anchored;
    Apr-1992 production execution remains explicitly unresolved;
    1992 NAND-versus-controller/interface system layering is historically attested;
    later FTL semantics remain on their own evidence chain
```

That separation reduces both false commercialization precision and false backward projection of later SSD/FTL semantics into early NAND component history.