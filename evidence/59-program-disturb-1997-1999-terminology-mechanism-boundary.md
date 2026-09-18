# Case 59 Addendum — `program disturb` terminology and mechanism boundary, 1997–1999

## Status

**`bounded deepening complete`** — the 1998 Invox item is no longer used only as a title-level terminology witness. Its public patent abstract is now inspected directly enough to establish a non-NAND-specific analog/multilevel Flash mechanism in which later programming can disturb the threshold state of already-written, unselected cells, and in which row-history information selects different protective word-line bias. The full 1998 specification/facsimile remains a separate source-custody debt, so details not present in the inspected abstract are not projected backward from later related patents.

## Purpose

This addendum deepens the prior-art and terminology boundary around [`../cases/59-nand-program-interference-write-induced-neighbor-drift.md`](../cases/59-nand-program-interference-write-induced-neighbor-drift.md).

The narrow question is:

> **What programming-induced non-target state changes were publicly documented before the 2002 `floating-gate interference` paper, and when may the phrase `program disturb` be used without silently collapsing distinct physical mechanisms into Case 59's later cell-to-cell capacitive program-interference model?**

The answer is now three-way rather than two-way. Before 2002, public records already document:

1. NAND-specific failed-inhibit / inadvertent-programming risk;
2. analog/multilevel nonvolatile-memory `program disturb` in which a later write can perturb the threshold state of already-programmed unselected cells, with protection conditioned on row programming history; and
3. NAND self-boosting literature that explicitly defines `program disturb` and separately names `pass disturb`.

Those records constrain origin claims, but they are **not automatically the same mechanism** as the 2002–2014 Case 59 lineage in which an intentionally programmed aggressor's threshold transition capacitively shifts an already-programmed neighboring victim.

## Evidence classes

| Source | Public date | Evidence role | What it establishes | What it does not establish |
| --- | --- | --- | --- | --- |
| Samsung, US5677873A | 14 Oct 1997 | `H/P` manufacturer patent | NAND-specific inadvertent-programming problem; selected/adjacent programming can expose nondesignated cells; boosting/inhibit conditions reduce Fowler–Nordheim programming risk | use of the exact phrase `program disturb`; cell-to-cell floating-gate interference as later modeled in Case 59; invention priority |
| Invox, US5818757A | 6 Oct 1998 | `H/P` primary patent record, abstract-level mechanism inspection | public `program disturb` terminology; disturbance of threshold voltages of unselected cells during another write; different bias treatment for already-written versus erased/virgin rows; sequential row-fill and row-history flags as disclosed control structure | NAND-specific geometry; the 2002 aggressor/victim capacitive-coupling model; exact full-specification circuit details not present in the inspected abstract; deployment; invention priority |
| AMD, US5991202A | 23 Nov 1999 | `H/P` manufacturer patent | NAND self-boosting context; explicit definition of `program disturb`; separate `pass disturb`; pulse/pass-voltage mitigation | cell-to-cell aggressor/victim capacitive interference; proof of commercial deployment; universal meaning of every later use of `program disturb` |
| So/Wong / SanDisk, US6285593B1 | 4 Sep 2001 | `H/P` later same-inventor continuity witness | later detailed description of program/drain-disturb risk to previously programmed unselected floating-gate cells, and explicit citation/incorporation of US5818757 | permission to back-project every 2001 embodiment, voltage, latch implementation, or terminology into the 1998 patent |

`H/P` means historical/primary technical record. The Invox row is deliberately called **abstract-level mechanism inspection** rather than `full facsimile inspection`.

## 1997 Samsung NAND inhibit / inadvertent-programming record

**Byeng-Sun Choi and Tae-Sung Jung, Samsung Electronics, US5677873A, “Methods of programming flash EEPROM integrated circuit memory devices to prevent inadvertent programming of nondesignated NAND memory cells therein.”**

Primary record:
<https://patents.google.com/patent/US5677873A>

The record gives a **19 September 1995 priority date**, **19 September 1996 US filing date**, and **14 October 1997 publication date**. These dates are not interchangeable. For a public-evidence chronology this repository uses **14 October 1997** as the directly inspectable US publication floor, while retaining the earlier priority/filing dates only as family chronology.

The patent describes a NAND EEPROM string in which pass/program voltages applied while another cell is being programmed can create a Fowler–Nordheim tunneling risk for nondesignated cells. Its mitigation raises/boosts the source, drain, and channel potential of cells that should remain unprogrammed so the effective program differential is reduced.

Historical result:

> **NAND programming already had an explicit non-target inadvertent-programming / inhibit-control problem in a public 1997 manufacturer record.**

The inspected text does **not** use that result to prove the later Case 59 cell-to-cell interference mechanism. The relevant physical relation here is program-voltage/inhibit bias and tunneling risk in cells that should not program, not an already-retained victim distribution being shifted in proportion to a neighboring aggressor's threshold transition.

## 1998 Invox `program disturb`: no longer only a title-level witness

**Hock C. So and Sau C. Wong, Invox Technology, US5818757A, “Analog and multi-level memory with reduced program disturb,” publication 6 October 1998.**

Stable record:
<https://patents.google.com/patent/US5818757A/en>

Public patent metadata and the indexed patent abstract identify the inventors, Invox Technology as assignee, a **22 July 1996 filing date**, and **6 October 1998** patent/publication date. The earlier filing date is retained as application chronology; the public terminology floor used here is the 1998 publication.

The abstract is mechanism-bearing, not merely bibliographic. It says that applying a bias voltage to **unselected word-lines** reduces `program disturb` of the **threshold voltages of unselected memory cells during a write**. It then makes the mitigation explicitly history-sensitive: the bias is applied to cells/rows that have **already been written** above a minimum threshold, while erased or `virgin` cells are treated differently. The disclosed sequential-recording example fills one row before moving to the next, and **bias flag circuits** in the row decoder indicate which rows are already filled so the appropriate word-line bias can be selected.

The retention-specific historical statement can therefore be upgraded from the old title-only claim:

> **By October 1998, `program disturb` was publicly used for a nonvolatile-memory mechanism in which writing one state could perturb the threshold state of unselected cells, and the disclosed mitigation depended on whether those unselected rows already contained programmed data.**

This is stronger than `the phrase appeared in a patent title`, but it remains narrower than a NAND claim. The patent is explicitly framed around **analog and multi-level nonvolatile memory**; the inspected abstract does not establish NAND-string geometry, NAND self-boosting, or the later wordline-to-wordline floating-gate coupling model.

### Why the row-history detail matters

The abstract exposes a control relation that is directly relevant to technical retention:

```text
row already contains programmed state
    -> later write creates a disturb risk for that retained state
    -> controller/decoder must choose protective bias for that row

row still erased / virgin
    -> different electrical treatment is admissible
```

The important retained relation is not simply `cell has charge`. A later write is conditioned on **the prior programming state of non-target rows**.

That supports two engineering decompositions:

> **same current write target ≠ same safe bias policy under different prior row histories**;

and

> **payload state ≠ the control knowledge needed to preserve that payload during a later write**.

The second sentence does **not** claim that the Invox bias flags themselves are power-loss-persistent metadata. The inspected abstract establishes their role in recording/indicating row-filled state for bias selection, but not their persistence horizon, restart behavior, reconstruction algorithm, or exact implementation technology.

### Later same-inventor continuity is evidence, not back-projection

A later So/Wong/SanDisk patent, **US6285593B1, “Word-line decoder for multi-bit-per-cell and analog/multi-level memories with improved resolution and signal-to-noise ratio,”** provides a useful continuity witness. Its public description discusses high programming voltages creating a large floating-gate/drain field in **unselected, previously programmed cells**, leading to Fowler–Nordheim charge loss and threshold-voltage reduction; it calls this `drain disturb` and says the maximum usable threshold voltage can be limited by `program disturb (or drain disturb)`. The same document explicitly cites US5818757 as related prior work.

Later record:
<https://patents.justia.com/patent/6285593>

This later description helps classify the Invox line as an already-programmed-state preservation problem, but it is **not** silently treated as the missing full 1998 specification. In particular, exact voltages, later decoder embodiments, volatile/nonvolatile flag alternatives, and the later patent's broader threshold-window discussion are not attributed to US5818757 unless independently present in the 1998 source.

## 1999 AMD NAND-specific `program disturb` / `pass disturb` record

**Narbeh Derhacobian and Hao Fang, Advanced Micro Devices, US5991202A, “Method for reducing program disturb during self-boosting in a NAND flash memory.”**

Primary record:
<https://patents.google.com/patent/US5991202A/en>

The record gives a **24 September 1998 filing/prior-art date** and **23 November 1999 publication date**. Again, filing is not silently rewritten as public terminology use.

The inspected description explicitly distinguishes two non-target programming problems in a NAND self-boosting regime:

1. **`program disturb`** — an unselected cell on the selected word line can be unintentionally programmed because the word-line programming voltage also electrically affects cells that are not the intended target;
2. **`pass disturb`** — leakage/voltage conditions associated with the selected bit line and pass-voltage regime can disturb other unselected cells.

The patent's mitigation uses pulsed program and pass voltages during self-boosting and discusses the trade-off between programming time and tolerated disturb.

This grounds a strong terminology boundary:

> **By November 1999, `program disturb` was explicit NAND engineering vocabulary for failed program inhibition of non-target cells, and `pass disturb` was separately named in the same manufacturer record.**

It still does not authorize the equation:

> `program disturb` = `cell-to-cell program interference`.

## Mechanism separation

### 1997 Samsung: NAND program-inhibit failure risk

The bounded causal chain is approximately:

```text
one NAND cell/wordline is selected for programming
    -> high program/pass voltages also electrically expose cells that should remain inhibited
    -> channel/source/bitline boosting or inhibit margin is insufficient
    -> unintended tunneling / threshold increase can occur in a non-target cell
    -> later logical state may be wrong
```

The critical relation is **selected programming bias versus inhibited non-target state**.

### 1998 Invox: history-sensitive protection of already-written unselected threshold state

The abstract-level chain is different:

```text
some rows already contain programmed threshold states
    -> another cell/row is written
    -> unselected cells can suffer threshold-voltage program disturb
    -> row history determines which protective word-line bias is selected
    -> sequential row fill + bias flags make that history usable by the decoder
```

This mechanism is important for Case 59 because it demonstrates an early **write-history-sensitive preservation problem**, but it is not yet the 2002 floating-gate-neighbor interference model.

### 1999 AMD: NAND self-boosting program/pass disturb

The bounded chain is:

```text
selected NAND wordline receives programming conditions
    -> unselected NAND strings/cells rely on self-boosting / pass-voltage conditions
    -> insufficient inhibit margin can unintentionally program a non-target cell
    -> program/pass disturb terminology distinguishes failure paths
```

Again, the critical relation is **program inhibition under NAND string biasing**.

### Case 59 cell-to-cell program interference from 2002 onward

Case 59's bounded lineage is different:

```text
victim already has a programmed threshold state
    -> neighboring aggressor is intentionally programmed to a new threshold state
    -> parasitic floating-gate coupling shifts the victim threshold distribution
    -> victim read margin changes
    -> later read-reference/ECC work may be needed
```

The central historical rule is therefore:

> **shared non-target threshold movement ≠ one shared physical mechanism.**

The three earlier records and the 2002+ interference lineage overlap functionally, but they differ in array context, electrical cause, mitigation, and the relation between target and victim.

## Engineering reconstruction

### Logical write target ≠ complete electrical effect scope

All three pre-2002 records correct the naive assumption that the cell/page named by a program operation is the only physically relevant state.

But:

> **same cross-target effect pattern ≠ same mechanism identity.**

Samsung/AMD emphasize NAND inhibit/self-boost conditions; Invox's inspected abstract emphasizes threshold disturb of already-written unselected cells and state-dependent row bias; Case 59's later sources emphasize parasitic neighbor coupling from an aggressor transition.

### Safe programming policy can depend on prior non-target state

The Invox evidence adds a more precise retention relation than the earlier version of this addendum contained. The protective bias decision changes according to whether an unselected row is already programmed or remains erased/virgin.

Therefore:

> **program safety can be history-dependent even when the current logical target is unchanged.**

And:

> **current payload arrangement can induce control obligations for future writes.**

Those are project engineering reconstructions. They do not imply a modern FTL, a crash-consistent metadata structure, or a durable per-row database in the 1998 design.

### Inhibit / bias control is retention infrastructure without being payload

The device must create electrical conditions under which non-target states remain outside an unintended transition regime. That bias/inhibit relation is not user payload, yet its successful enforcement protects retained state during another write.

Therefore:

> **retaining a value during a neighboring or same-array program operation can depend on transient control/bias state that is not itself the retained payload.**

### Chronology of a word ≠ chronology of one mechanism

The evidence now makes this warning stronger. `Program disturb` appears in a 1998 analog/multilevel nonvolatile-memory context and in a 1999 NAND self-boosting context, yet the bounded mechanisms are not identical. The later 2002 `floating-gate interference` paper should neither be projected backward to rename every earlier disturb mechanism nor treated as the first public recognition that a write can damage non-target stored state.

Therefore:

> **terminology continuity ≠ mechanism identity ≠ proven genealogy.**

## Functional analogies — bounded

### Case 52 — NAND read disturb

Safe comparison:

> a nominally successful operation can electrically stress state outside the logical target.

Stop condition:

- read disturb is repeated-read/pass-through stress;
- 1997/1999 NAND program disturb is a programming-inhibit/bias problem;
- 1998 Invox program disturb is an analog/multilevel write-history-sensitive threshold-disturb problem;
- Case 59 program interference is cell-to-cell capacitive neighbor coupling.

### Case 70 — magnetic-core half-select

A very narrow analogy is permitted: both a half-selected core and an unselected nonvolatile-memory cell are **not the intended write target but still receive part of the physical excitation generated by a write operation**.

Stop condition:

> magnetic-field coincidence/half-select margin ≠ nonvolatile wordline/bitline bias ≠ NAND self-boosting ≠ floating-gate capacitive interference.

No historical genealogy is asserted.

### Case 93 / Case 43 — control knowledge can age or be wrong independently of payload

Only a functional comparison is permitted. AVATAR's refresh classification and the Invox row-history/bias-selection relation both show that preserving payload can depend on **control knowledge about payload state**. But AVATAR concerns DRAM refresh classification and runtime revalidation; the 1998 patent concerns write-time bias selection in nonvolatile memory. No technical genealogy is claimed.

## Philosophical interpretation — bounded

The evidence supports only a modest project-level pressure:

> **Writing a new state cannot always be modeled as an operation whose physically relevant scope is identical to its logical target. Preservation can depend on knowing which non-target states already carry meaning and choosing a control regime that keeps them outside an unintended transition.**

This is an interpretation of the engineering evidence, not terminology used by Samsung, Invox, AMD, Lee, or Cai.

## Prior-art / origin guardrails

Do **not** upgrade this addendum into any of the following:

- `program disturb was invented in 1997`, `1998`, or `1999`;
- `US5818757 coined program disturb`;
- the 1995 priority date of US5677873A as a public-disclosure date;
- the 1996 filing date of US5818757A as public terminology use;
- the 1998 filing date of US5991202A as public terminology use;
- `US5818757 is a NAND patent`;
- `US5818757 already described the 2002 cell-to-cell floating-gate interference model`;
- `bias flags are proven persistent across reset/power loss`;
- `sequential row recording in US5818757 is the ancestor of later NAND page-order rules`;
- `program disturb` as one universal NAND/nonvolatile-memory mechanism;
- `pass disturb = program disturb = program interference`;
- proof that the 1997–1999 patented mitigations shipped in named commercial Flash products;
- proof that the 2002/2013 program-interference work descends from any one patent family;
- a teleological 1997 → 1998 → 1999 → 2002 → 2013 invention chain.

## Source-custody limits and remaining debt

This pass closes one bounded gap and leaves another explicit.

Closed:

- the 1998 Invox item is no longer merely a title-level vocabulary witness;
- its inspected public abstract supports a mechanism-level statement about threshold disturbance of unselected cells during another write;
- the abstract directly supports state-dependent treatment of already-written versus erased/virgin rows and the existence of bias flags used for that decision.

Still open:

- direct page-by-page inspection of the complete 1998 US5818757 facsimile/specification;
- exact claim scope and embodiment details beyond the public abstract;
- whether any bias-history state survives reset/power loss, or is reconstructed;
- named commercial implementation of the 1998 Invox design;
- pre-1998 `program disturb` use in directly inspected nonvolatile-memory full texts;
- direct genealogy, if any, into later NAND self-boosting or cell-to-cell interference work.

A later related patent is used only as a continuity/cross-check source; it does not erase these open source-custody items.

## Related-repository boundary

A fresh search of `tmzncty/computing-archaeology` for `Invox program disturb`, `program disturb`, and `SSD/NAND disturb` surfaced no dedicated case to reuse in the current search surface.

Accordingly, this file keeps only the retention-specific terminology/mechanism boundary needed by Case 59. A broader nonvolatile-memory programming genealogy — Invox/SanDisk analog/multilevel architecture, self-boosting/local-boost variants, ISPP evolution, inhibit circuits, charge-trap/3-D NAND disturb families, vendor implementation history, and patent-family prosecution — belongs primarily in `computing-archaeology` if developed.

## Result

The bounded chronology can now be stated conservatively:

```text
1997 public NAND record:
    inadvertent programming of nondesignated cells is an explicit inhibit problem

1998 public Invox record:
    `program disturb` is mechanism-bearing vocabulary
    + writing can perturb threshold state of unselected cells
    + already-written vs erased/virgin row history changes protective bias policy

1999 directly inspected NAND record:
    `program disturb` and `pass disturb` are explicitly distinguished in self-boosting context

2002 Case 59 lineage:
    `floating-gate interference` explicitly describes adjacent-threshold-change / parasitic-capacitance coupling

2013 Case 59 characterization:
    `program interference` is experimentally decomposed by victim/aggressor, location, order, and data value
```

The historiographic rule is the important part:

> **Earlier disturb vocabulary and non-target programming mechanisms constrain origin claims, but they do not erase mechanism boundaries. The 1998 Invox record additionally shows that protection against later writes could already be conditioned on whether non-target state had previously been programmed.**
