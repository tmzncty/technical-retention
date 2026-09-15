# Case 59 deepening — 2006–2007 Samsung/Micron product program-order contracts

## Status

**`bounded deepening complete`**

This addendum closes one narrow evidence debt in Case 59: direct vendor datasheet evidence for **named planar NAND parts whose legal page-program history is constrained**, while refusing to infer the physical cause of that constraint from the datasheet alone.

The strongest new witness is Samsung's **K9GAG08U0M / K9GAG08B0M** 16-Gbit, two-bit-per-cell NAND datasheet, revision 0.6 dated **12 February 2007**. It states that pages in a block must be programmed consecutively from the least-significant page to the most-significant page and that random page-address programming is prohibited. The same document limits consecutive partial-page programming without erase to **one** program cycle for the page.

A same-period Micron product document supplies an important control comparison. Micron's **MT29F4G08AAA / MT29F8G08BAA / MT29F8G08DAA / MT29F16G08FAA** SLC NAND datasheet, Rev. B **February 2007** (initial Rev. A August 2006), likewise requires consecutive least-to-most-significant page programming and prohibits random page programming, while allowing up to four partial-page programming operations under its stated rule.

The cross-vendor result is deliberately limited:

> **a product datasheet's sequential-programming rule is direct evidence of an interface/usage contract, but is not by itself proof that cell-to-cell MLC program interference is the reason for that rule.**

The Micron SLC counterexample is particularly useful because it shows that a broadly similar ordering rule can exist outside the exact two-bit-MLC interference regime bounded by Case 59.

## Research question

Case 59 already had:

- 2002 evidence for floating-gate interference;
- 2007–2008 Samsung-linked research on interference-aware MLC page architecture/program order;
- 2013 commercial-chip characterization showing strong order dependence;
- 2014 neighbor-assisted recovery.

But its Remaining work still asked for:

> `exact vendor datasheet/page-program-order constraints for named planar-NAND parts`.

This addendum asks:

1. Did an actual named MLC NAND product document in the same historical window expose page-program ordering as an enforceable usage condition?
2. Can that product rule be treated as direct proof of the physical program-interference mechanism?
3. What does a same-period SLC product contract do to that inference?

## Source ladder and provenance

### A. Samsung K9GAG08U0M / K9GAG08B0M datasheet

Manufacturer-authored document, mirrored publicly as:

- Samsung Electronics, **K9GAG08U0M / K9GAG08B0M / K9LBG08U1M**, *2G x 8 Bit NAND Flash Memory*, preliminary Rev. 0.6.
- Revision history:
  - 0.0 initial issue: **12 April 2006**;
  - 0.1: 21 September 2006;
  - 0.2: 8 December 2006;
  - 0.3: 12 December 2006;
  - 0.4: 21 December 2006;
  - 0.5: 12 January 2007;
  - 0.6: **12 February 2007**.
- Public mirror inspected: <https://opendevices.ru/wp-content/uploads/2011/11/K9GAG08U0M.pdf>.
- Additional distributor mirror: <https://docs.rs-online.com/b7c3/0900766b80defffe.pdf>.

The document itself identifies the part as:

- 2G × 8-bit / 16-Gbit NAND;
- **2 bit / memory cell**;
- 4,224-byte page;
- floating-gate NAND product for solid-state mass storage;
- on-chip write controller with program/erase pulse repetition, verification, and margining.

This is direct named-product documentation, not an academic characterization of an anonymous chip.

### B. Micron MT29F4G08AAA / MT29F8G08BAA / MT29F8G08DAA / MT29F16G08FAA datasheet

Manufacturer-authored document, publicly mirrored in several archival/distributor collections:

- Micron Technology, **4Gb, 8Gb, and 16Gb x8 NAND Flash Memory**.
- Named parts: `MT29F4G08AAA`, `MT29F8G08BAA`, `MT29F8G08DAA`, `MT29F16G08FAA`.
- Technology: **single-level cell (SLC)**.
- Rev. A initial release: **August 2006**.
- Rev. B: **February 2007**.
- Public text mirror inspected: <https://studylib.net/doc/8343321/mt29fxg08xaa---digi-key>.
- A copy of the manufacturer datasheet is also preserved in USPTO PTAB public records: <https://ptacts.uspto.gov/ptacts/public-informations/petitions/1544922/download-documents?artifactId=Gaz2p22wnz7JIP8TNNKPNQt6NuP5glGQRpo_XvDZShTeDlySjz8oH14>.

This source is used as a **counterexample against causal over-reading**, not as evidence about MLC cell-to-cell interference.

## Historical record

### 1. Samsung's 2007 named MLC product requires monotone page progression inside a block

The K9GAG08U0M Rev. 0.6 datasheet's `NAND Flash Technical Notes` states under `Addressing for program operation` that pages within a block must be programmed consecutively from the LSB page toward the MSB page and that **random page-address programming is prohibited**.

The diagram explicitly contrasts:

```text
From the LSB page to MSB page
```

with:

```text
Random page program (Prohibition)
```

The later `PAGE PROGRAM` section repeats that addressing should be sequential inside a block.

This is a product-interface/usage contract. It is stronger evidence than a later research paper saying manufacturers *generally recommend* sequential order because the named part's own documentation directly tells the system/controller how the device must be programmed.

### 2. The same Samsung product constrains partial reprogramming of a page

The AC-characteristics table gives:

```text
Number of Partial Program Cycles in the Same Page ... 1 cycle
```

The `PAGE PROGRAM` prose further says that consecutive partial-page programming without an intervening erase must not exceed one time for the page.

Therefore two different histories that might look superficially equivalent at a logical-address level are **not equally legal histories at the NAND interface**:

```text
program page once with final intended payload
    !=
repeatedly mutate portions of the same physical page before erase
```

The document does not state that cell-to-cell interference is the sole reason for the one-cycle partial-program rule, so this addendum does not supply one.

### 3. The Samsung product is explicitly two-bit MLC

The same document identifies:

```text
Memory Cell : 2bit / Memory Cell
```

and its ID-definition table distinguishes cell types including 2-level, 4-level, 8-level, and 16-level cells.

For this case, the important point is simply that the named K9GAG08X0M family is a **two-bit-per-cell NAND product** in the exact broad technology class where Case 59 discusses MLC program-order history.

This still does not prove that the precise 2013 Cai et al. victim/aggressor model describes every internal state transition of this 2007 part.

### 4. Samsung's product contract and Samsung-linked 2007–2008 research are contemporaneous but not automatically one genealogy

Case 59 already cites Samsung-linked VLSI 2007 / JSSC 2008 work on a temporary-LSB / parallel-MSB architecture intended to reduce cell-to-cell interference and the number of neighbors programmed after a selected cell.

The K9GAG08U0M datasheet revision history spans April 2006 through February 2007. Thus the named product rule and the Samsung-linked research program are **contemporaneous**.

Safe statement:

> by 2007, Samsung's public technical record contains both a named MLC product with explicit sequential page-program constraints and research publications treating program order/cell-to-cell interference as a scaling problem.

Unsafe statement, not made here:

> the K9GAG08U0M sequential rule was implemented specifically because of the Park et al. architecture or because of the exact mechanism quantified by Cai et al. in 2013.

No inspected source establishes that causal/genealogical bridge.

### 5. Micron's same-period SLC products expose a similar sequential rule

Micron's Rev. B February-2007 SLC datasheet names four planar NAND products and says:

```text
Pages must be programmed consecutively within a block,
from the least significant page address to the most significant page address.
Random page address programming is prohibited.
```

The document additionally allows up to four partial-page programming operations under its stated constraint.

This matters because the Micron parts are explicitly **SLC**. The existence of a similar product-level sequencing rule in SLC NAND shows that:

> **sequential page-program requirement ≠ sufficient evidence for MLC cell-to-cell program interference.**

The rule may be compatible with multiple device-internal constraints, algorithms, verify assumptions, disturb controls, or architecture requirements. This addendum does not attempt to infer which combination explains Micron's rule.

## Engineering reconstruction

### Product usage contract and physical causal model are different evidence layers

A datasheet can prove a controller-visible constraint:

```text
legal page-program history
    -> sequential within block
    -> no random page-address programming
```

It cannot, without explanatory text or an independently linked design source, prove:

```text
why that rule exists physically
```

Therefore:

```text
named-product sequencing rule
    !=
identified physical mechanism
```

and:

```text
same-looking rule across vendors
    !=
same silicon cause
```

This distinction is central to Case 59 because the repository already has a strong physical mechanism account. The datasheet evidence should **anchor deployment-facing constraints**, not be used to inflate the mechanism genealogy.

### A controller must retain enough order state to avoid issuing an illegal history

The Samsung and Micron datasheets state ordering rules, not an FTL implementation. Nevertheless, an engineering system that writes such devices must arrange its physical-page allocation so that the sequence presented to a block obeys the product contract.

Bounded reconstruction:

```text
block has an already-programmed prefix / current frontier
    -> next legal physical-page choices are constrained
```

Thus a controller or software layer generally needs some way to know which physical pages are already programmed and which next page is legal.

But this addendum does **not** claim:

- that either device stores a host-visible `current page` variable;
- that a specific SSD FTL persisted this frontier in a particular metadata structure;
- that the ordering frontier survives sudden power loss in any particular way;
- that violating the rule produces a specific failure mode rather than simply leaving behavior outside the product contract.

The source-level fact is the rule. `program frontier` is the repository's engineering reconstruction of the information needed to obey it.

### Sequential legality is distinct from successful status of an individual program command

Both families expose program-completion/status mechanisms. A command can report completion or pass/fail while the broader history still has to obey per-block ordering rules.

Therefore:

```text
one page-program command reports success
    !=
entire block program history is contract-compliant
```

This is not evidence that the device accepts every illegal history and silently corrupts data. It only separates **transaction outcome** from **history validity**.

### Partial-program budget is another history dimension

For Samsung's named two-bit MLC part, the inspected document permits only one partial-program cycle per page before erase; Micron's named SLC family permits up to four under its rule.

Thus even among same-period planar NAND products:

```text
sequential page order
    !=
identical per-page reprogram budget
```

This is a useful warning against turning `NAND pages are sequentially programmed` into a universal device law with one universal numerical budget.

## Functional comparison

### With the 2013 Cai et al. program-interference characterization

Cai et al. experimentally show that out-of-order programming can expose a victim to additional/larger neighbor-program events and substantially shift victim threshold distributions in their tested 2Y-nm commercial MLC NAND.

The 2007 Samsung datasheet establishes a product rule that is **compatible** with the importance of order:

```text
named product says sequential order is required
    +
research later demonstrates order-sensitive interference in commercial MLC NAND
```

But compatibility is not identity:

```text
product rule
    !=
proof of Cai et al.'s exact mechanism on K9GAG08U0M
```

### With Samsung-linked Park et al. 2007–2008 work

Safe functional relation:

- product documentation constrains externally legal sequence;
- architecture research changes internal/architectural programming strategy to reduce interference exposure.

Stop condition:

- the datasheet does not cite the Park et al. paper;
- the paper is not treated here as a K9GAG08U0M implementation manual;
- temporal proximity is not technology-transfer proof.

### With Micron SLC

The Micron counterexample provides the strongest methodological guardrail in this addendum:

```text
same broad sequential-program contract
    can exist in a different cell-encoding regime
```

Therefore cross-vendor rule similarity is a **functional analogy at the interface**, not proof of identical failure physics.

## Retained-state decomposition

This addendum adds or sharpens the following separable relations:

1. **payload bits** — user/data content intended for the page;
2. **physical page identity** — page location within a block;
3. **block program frontier** — analytical description of which page region has already been consumed by the legal sequence;
4. **per-page partial-program budget** — how many allowed program cycles remain under the product contract;
5. **command completion/status** — result of an individual program transaction;
6. **physical interference margin** — Case 59's separate victim/aggressor threshold-voltage relation;
7. **FTL mapping / controller metadata** — implementation-dependent system state that may be needed to select legal physical pages.

These must not be collapsed:

```text
payload retained
    !=
page legal to program again
    !=
next block page legal to program
    !=
individual program command status
    !=
neighbor-interference margin
```

## Historical record / engineering reconstruction / analogy / interpretation ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| Samsung K9GAG08X0M Rev. 0.6 is dated 12 Feb 2007 and identifies a two-bit-per-cell NAND product | `H/P` | manufacturer datasheet revision history + feature list |
| Samsung requires consecutive LSB→MSB page programming and prohibits random page-address programming | `H/P` | manufacturer technical note |
| Samsung limits partial-page program cycles to one for the page | `H/P` | AC table + PAGE PROGRAM prose |
| Micron's named Rev. B Feb-2007 SLC family also requires consecutive page programming and prohibits random page programming | `H/P` | manufacturer datasheet |
| a system using these parts must track enough allocation/order state to issue a legal sequence | `E` | engineering reconstruction; implementation not specified |
| the Samsung product rule is compatible with program-order-sensitive interference | `A` | functional compatibility only |
| the Micron SLC rule shows that sequencing language alone cannot identify MLC interference as the cause | `E/A` | cross-source counterexample |
| product-contract history can be constitutive of correct retention behavior even when the physical cause is not stated | `I` | bounded project interpretation, not vendor vocabulary |

## Bounded philosophical interpretation

The narrow conceptual pressure is that **retention conditions can include a legal history of later operations**.

A page can contain a valid retained payload while the block also carries a history-dependent constraint on what may legally be programmed next. The medium therefore exposes at least two different kinds of persistence:

```text
retained payload state
    vs
retained admissibility/history relation
```

This does not mean the datasheets describe memory philosophically, nor that the ordering rule is itself stored as a durable metadata object inside the NAND. It means an adequate system description cannot always be reduced to the current bits alone; correct future operations can depend on how the block reached its present state.

## Explicit non-claims

This addendum does **not** claim:

1. Samsung invented sequential NAND page programming.
2. The April-2006 initial K9GAG08U0M draft is the first product document ever to state such a rule.
3. The K9GAG08U0M rule exists solely because of cell-to-cell capacitive program interference.
4. The Park et al. 2007/2008 architecture was implemented in K9GAG08U0M.
5. The 2013 Cai et al. measured device was K9GAG08U0M.
6. Micron SLC and Samsung MLC share the same physical reason for sequential programming.
7. Random page programming necessarily produces immediate corruption on every device; the source establishes prohibition, not a universal failure trace.
8. A successful READ STATUS result certifies that the complete block history obeyed all usage constraints.
9. The analytical `block program frontier` is a vendor term or a named on-die register.
10. The controller's frontier metadata is necessarily persisted in NAND, DRAM, NOR, or any particular location.
11. One partial-page program on Samsung and four on Micron are universal limits for all NAND.
12. Product datasheet constraints prove a shipped SSD controller's FTL policy.
13. Sequential page programming alone proves anything about modern 3D charge-trap NAND.

## Related repositories

A fresh code search in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `program interference` returned no dedicated case. This addendum therefore keeps only the retention-specific product-contract boundary here.

If `computing-archaeology` later develops a broader NAND device-interface or page-programming genealogy, the vendor-document chronology belongs there; Case 59 should retain the narrower distinction among **product rule, physical mechanism, and controller-retained history state**.

## Sources

1. Samsung Electronics, **K9GAG08U0M / K9GAG08B0M / K9LBG08U1M, 2G × 8 Bit NAND Flash Memory**, preliminary Rev. 0.6, 12 February 2007. Public mirror: <https://opendevices.ru/wp-content/uploads/2011/11/K9GAG08U0M.pdf>. Distributor mirror: <https://docs.rs-online.com/b7c3/0900766b80defffe.pdf>.
2. Micron Technology, **4Gb, 8Gb, and 16Gb x8 NAND Flash Memory**, parts MT29F4G08AAA / MT29F8G08BAA / MT29F8G08DAA / MT29F16G08FAA, Rev. B, February 2007; revision history records Rev. A initial release August 2006. Public text mirror: <https://studylib.net/doc/8343321/mt29fxg08xaa---digi-key>. USPTO PTAB-hosted copy: <https://ptacts.uspto.gov/ptacts/public-informations/petitions/1544922/download-documents?artifactId=Gaz2p22wnz7JIP8TNNKPNQt6NuP5glGQRpo_XvDZShTeDlySjz8oH14>.
3. Ki Tae Park et al., **“A zeroing cell-to-cell interference page architecture with temporary LSB storing program scheme for sub-40nm MLC NAND flash memories and beyond,”** *2007 Symposium on VLSI Circuits*, DOI `10.1109/VLSIC.2007.4342709`.
4. Ki Tae Park et al., **“A zeroing cell-to-cell interference page architecture with temporary LSB storing and parallel MSB program scheme for MLC NAND flash memories,”** *IEEE Journal of Solid-State Circuits* 43(4), 2008, DOI `10.1109/JSSC.2008.917558`.
5. Yu Cai et al., **“Program Interference in MLC NAND Flash Memory: Characterization, Modeling, and Mitigation,”** ICCD 2013, DOI `10.1109/ICCD.2013.6657034`.

## What this closes, and what remains open

Boundedly closed:

- direct named-product evidence that a Samsung two-bit MLC NAND part in 2007 required sequential in-block page programming;
- direct named-product evidence for its one-cycle partial-page-program limit;
- same-period Micron SLC product evidence showing a similar sequence rule but a different partial-program budget;
- the inference boundary `datasheet sequencing rule != identified program-interference cause`.

Still open:

- a vendor document that explicitly ties a named product's sequencing rule to cell-to-cell program interference;
- a shipped-controller/FTL trace showing how program-order frontier state is retained/recovered across sudden power loss;
- exact program-order contracts for later planar MLC/TLC generations and transition to 3D NAND;
- independent fault tests that intentionally violate the product sequence and characterize resulting error modes;
- the broader historical genealogy of page-order constraints, which belongs primarily in `computing-archaeology` if developed there.
