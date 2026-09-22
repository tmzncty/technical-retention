# Case 04 — NAND device / commercialization evidence index

## Scope

This index groups the early NAND substrate and commercialization evidence that feeds the canonical Case 04:

- `cases/04-flash-virtual-mapping-logical-identity.md`

It is intentionally **not** a complete history of NAND Flash, FTLs, SSD controllers, or flash-file systems. Its purpose is to keep four evidence layers from collapsing into one another:

```text
series-cell / patent chronology
    !=
device geometry / experimental fabrication
    !=
commercial product / supply chronology
    !=
logical-identity remapping semantics
```

The current update does not claim a Case 04 maturity promotion.

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

## 1.4 Canonical mapped-storage semantics

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

NAND product exists
    !=
FTL exists

physical block replacement is possible
    !=
logical address identity is preserved
```

---

# 3. Historical-chronology discipline

The commercial-chronology deepening exposed a general rule worth making explicit for this case:

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
- sample shipment;
- mass-production start;
- named-product availability;
- sustained customer adoption.

This is especially important where later retrospectives disagree in wording or year.

---

# 4. Evidence classes

Following `docs/METHOD.md`:

### Historical record

Directly records what a paper, patent, contemporary report, corporate chronology, manual, or other source says or demonstrates.

### Engineering reconstruction

Combines bounded records into a technical relation while keeping inference visible, for example:

```text
experimental success
    !=
manufacturing readiness
    !=
supply availability
```

### Functional analogy

May compare the evidence structure with other cases, such as Case 03 filing/publication/product chronology or Case 111 mechanism-prior-art versus named-product evidence.

Such comparisons do not establish genealogy.

### Philosophical interpretation

May discuss why “technological existence” is not a single transition, but it must remain downstream of the historical and engineering record.

---

# 5. Current source-strength picture

## Strong for bounded claims

- 1989 peer-reviewed technical records explicitly present an experimental 4 Mbit NAND device and its operation.
- Current KIOXIA first-party history assigns a 1991 commercialization milestone to 4 Mbit NAND.
- Current Toshiba history uses a 1991 development milestone for 4-megabit NAND-type EEPROM.
- December 1991 near-contemporary product reporting names `TC584000` and separates sample shipment from planned mass production.
- A later Toshiba-associated patent corroborates `TC584000` as an available/practically used named NAND component by its later horizon.

## Provenance-limited / unresolved

- current corporate histories are retrospective;
- the near-contemporary product report is not yet the original Toshiba announcement;
- a later IEEE Spectrum retrospective uses a 1989 `hit the market` formulation that should not simply be merged with KIOXIA's 1991 `commercialization` date;
- the reported April 1992 mass-production milestone is still a plan until separately confirmed as executed.

---

# 6. Remaining research debt

The broad question `when did NAND become commercial?` is no longer precise enough. The remaining work should target specific evidence gaps:

1. original Toshiba 1991 `TC584000` announcement or press material;
2. dated Toshiba data book, catalog, price list, or ordering material for `TC584000`;
3. direct confirmation that the reported November 1991 sample shipment actually occurred;
4. direct confirmation that the planned April 1992 mass-production start occurred;
5. a named early customer, board, card, or system using `TC584000`, if surviving evidence exists;
6. direct primary review of any still-indirectly sourced 1988/1989 device-conference pages needed by the earlier chronology;
7. broader NAND vendor/product genealogy should remain in `tmzncty/computing-archaeology` unless it changes a retention or mapping claim here;
8. do not infer FTL/controller adoption from NAND component availability.

---

# 7. Status

This navigation update does not promote Case 04 maturity.

The useful progress is narrower:

```text
before:
    early NAND chronology could be read as a compressed technology-origin story

after:
    patent / experimental-device / product-supply / mapping layers are separately navigable
```

That separation reduces both false priority claims and false backward projection of later FTL semantics into early NAND device history.
