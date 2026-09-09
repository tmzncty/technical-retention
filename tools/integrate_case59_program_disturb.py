from pathlib import Path

CASE = Path("cases/59-nand-program-interference-write-induced-neighbor-drift.md")
EVIDENCE = Path("evidence/59-nand-2002-2014-program-interference-grounding.md")
ADDENDUM = Path("evidence/59-program-disturb-1997-1999-terminology-mechanism-boundary.md")
ROADMAP = Path("ROADMAP.md")
INDEX = Path("CASE_INDEX.md")


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise SystemExit(f"expected exactly one anchor in {path}: {old[:80]!r}; found {text.count(old)}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


if ADDENDUM.exists():
    raise SystemExit(f"refusing to overwrite existing {ADDENDUM}")

addendum = r'''# Case 59 Addendum — `program disturb` terminology and NAND program-inhibit boundary, 1997–1999

## Purpose

This addendum deepens the prior-art and terminology boundary around [`../cases/59-nand-program-interference-write-induced-neighbor-drift.md`](../cases/59-nand-program-interference-write-induced-neighbor-drift.md).

The narrow question is:

> **What NAND programming failure mechanisms were publicly documented before the 2002 `floating-gate interference` paper, and when may the phrase `program disturb` be used without silently collapsing those mechanisms into Case 59's later cell-to-cell capacitive program-interference model?**

The answer is deliberately split. Public NAND documentation before 2002 already treats **unintended programming of cells that were supposed to remain inhibited during another program operation** as an engineering problem. By 1999, an AMD patent explicitly defines that NAND failure family as `program disturb` and separately names `pass disturb`. That history is relevant prior art, but it is **not automatically the same mechanism** as the 2002–2014 Case 59 lineage in which an intentionally programmed aggressor's threshold transition capacitively shifts an already-programmed neighboring victim.

## Evidence classes

| Source | Public date | Evidence role | What it establishes | What it does not establish |
| --- | --- | --- | --- | --- |
| Samsung, US5677873A | 14 Oct 1997 | `H/P` manufacturer patent | NAND-specific inadvertent-programming problem; selected/adjacent programming can expose nondesignated cells; boosting/inhibit conditions reduce Fowler–Nordheim programming risk | use of the exact phrase `program disturb`; cell-to-cell floating-gate interference as later modeled in Case 59; invention priority |
| Invox, US5818757A | 6 Oct 1998 | `H/P*` bibliographic terminology witness | a public patent title uses `program disturb` for analog/multilevel nonvolatile memory before the directly inspected 1999 NAND definition | NAND-specific mechanism details in this run; origin/coinage of the phrase; direct genealogy into later NAND papers |
| AMD, US5991202A | 23 Nov 1999 | `H/P` manufacturer patent | NAND self-boosting context; explicit definition of `program disturb`; separate `pass disturb`; pulse/pass-voltage mitigation | cell-to-cell aggressor/victim capacitive interference; proof of commercial deployment; universal meaning of every later use of `program disturb` |

`H/P*` is used only to flag that the 1998 item is retained at **title/bibliographic level** in this pass. No mechanism-specific claim below depends on unseen full text from that patent.

## 1997 Samsung NAND inhibit / inadvertent-programming record

**Byeng-Sun Choi and Tae-Sung Jung, Samsung Electronics, US5677873A, “Methods of programming flash EEPROM integrated circuit memory devices to prevent inadvertent programming of nondesignated NAND memory cells therein.”**

Primary record:
<https://patents.google.com/patent/US5677873A>

The record gives a **19 September 1995 priority date**, **19 September 1996 US filing date**, and **14 October 1997 publication date**. These dates are not interchangeable. For a public-evidence chronology this repository uses **14 October 1997** as the directly inspectable US publication floor, while retaining the earlier priority/filing dates only as family chronology.

The patent describes a NAND EEPROM string in which pass/program voltages applied while another cell is being programmed can create a Fowler–Nordheim tunneling risk for nondesignated cells. Its mitigation raises/boosts the source, drain, and channel potential of cells that should remain unprogrammed so the effective program differential is reduced.

Historical result:

> **NAND programming already had an explicit non-target inadvertent-programming / inhibit-control problem in a public 1997 manufacturer record.**

The inspected text does **not** use that result to prove the later Case 59 cell-to-cell interference mechanism. The relevant physical relation here is program-voltage/inhibit bias and tunneling risk in cells that should not program, not an already-retained victim distribution being shifted in proportion to a neighboring aggressor's threshold transition.

## 1998 title-level `program disturb` witness

**Hock C. So and Sau C. Wong, Invox Technology, US5818757A, “Analog and multi-level memory with reduced program disturb,” publication 6 October 1998.**

Stable record:
<https://patents.google.com/patent/US5818757A/en>

The publication metadata/title is enough for one modest chronology statement:

> **the phrase `program disturb` was publicly attached to a nonvolatile-memory patent by October 1998.**

This addendum does not use the item to establish NAND-specific circuit details because the full description was not directly inspected in this pass. It therefore cannot lower the **directly inspected NAND-specific definitional floor** established by the AMD record below.

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

> **by November 1999, `program disturb` was explicit NAND engineering vocabulary for failed program inhibition of non-target cells, and `pass disturb` was separately named in the same manufacturer record.**

It still does not authorize the equation:

> `program disturb` = `cell-to-cell program interference`.

## Mechanism separation

### Program-inhibit / program-disturb family in the 1997–1999 records

The bounded causal chain is approximately:

```text
one cell/wordline is selected for programming
    -> high program/pass voltages also electrically expose cells that should remain inhibited
    -> channel/source/bitline boosting or inhibit margin is insufficient
    -> unintended tunneling / threshold increase can occur in a non-target cell
    -> later logical state may be wrong
```

The important retained/control state includes whether a cell is intended to remain inhibited and whether the selected programming bias leaves enough electrical margin to keep it so.

### Case 59 cell-to-cell program interference from 2002 onward

Case 59's bounded lineage is different:

```text
victim already has a programmed threshold state
    -> neighboring aggressor is intentionally programmed to a new threshold state
    -> parasitic floating-gate coupling shifts the victim threshold distribution
    -> victim read margin changes
    -> later read-reference/ECC work may be needed
```

The central historical distinction is therefore:

> **failed inhibit / unintended programming of a non-target cell ≠ aggressor-threshold-transition-induced capacitive shift of an already-programmed victim.**

The two can share the broad fact that a program operation has effects outside its logical target and can both change threshold voltage. That functional overlap is not enough to merge the mechanisms, vocabulary, mitigation clocks, or genealogies.

## Engineering reconstruction

The primary sources support several retention-specific decompositions.

### Logical target ≠ complete electrical exposure scope

Both the inhibit records and Case 59 make the same high-level correction: the cell/page named by a program command is not necessarily the only state electrically affected by that command.

But:

> **same cross-target effect pattern ≠ same physical mechanism.**

The 1997–1999 program-inhibit sources concern biasing and unintended tunneling in cells meant to remain unprogrammed; Case 59's later interference sources concern parasitic coupling from an aggressor threshold transition into a retained victim.

### Inhibit success is a retention condition without being payload retention

The controller/device must create an electrical condition under which a non-target cell remains outside the programming regime. That inhibit relation is not user payload, yet its successful enforcement protects retained state during another write.

Therefore:

> **retaining a value during a neighboring program operation can depend on transient control/bias state that is not itself the retained payload.**

### Chronology of a word ≠ chronology of one mechanism

A historical phrase can be broader than a later experimental mechanism. The 1998/1999 `program disturb` record cannot be projected forward to make every later `program interference` paper an instance of the same circuit failure; conversely, the 2002 floating-gate-interference paper cannot be projected backward to rename every earlier inadvertent-programming record.

Therefore:

> **terminology continuity ≠ mechanism identity ≠ proven genealogy.**

## Functional analogies — bounded

### Case 52 — read disturb

Safe comparison:

> a nominally successful operation can electrically stress state outside the logical target.

Stop condition:

- read disturb is repeated-read/pass-through stress;
- 1997–1999 program disturb is a programming-inhibit/bias problem;
- Case 59 program interference is cell-to-cell capacitive neighbor coupling.

### Case 70 — magnetic-core half-select

A very narrow analogy is permitted: both a half-selected core and an inhibited NAND cell are **not the intended write target but still receive part of the physical excitation generated by a write operation**.

Stop condition:

> magnetic-field coincidence/half-select margin ≠ NAND wordline/bitline boosting ≠ floating-gate capacitive interference.

No historical genealogy is asserted.

## Philosophical interpretation — bounded

The evidence supports only a modest project-level pressure:

> **writing a new state cannot always be modeled as an operation whose physically relevant scope is identical to its logical target. Preservation can depend on keeping non-target state outside an unintended transition regime.**

This is an interpretation of the engineering evidence, not terminology used by Samsung, Invox, AMD, Lee, or Cai.

## Prior-art / origin guardrails

Do **not** upgrade this addendum into any of the following:

- `program disturb was invented in 1997`, `1998`, or `1999`;
- `US5677873A coined program disturb`;
- the 1995 priority date of US5677873A as a public-disclosure date;
- the 1996 filing date of US5818757A as public terminology use;
- the 1998 filing date of US5991202A as public terminology use;
- `program disturb` as one universal NAND mechanism;
- `pass disturb = program disturb = program interference`;
- proof that the 1997–1999 patented mitigations shipped in named commercial Flash products;
- proof that the 2002/2013 program-interference work descends from any one patent family;
- a teleological 1997 → 1999 → 2002 → 2013 invention chain.

## Related-repository boundary

A fresh search of `tmzncty/computing-archaeology` for `program disturb` / `disturb` surfaced no dedicated case to reuse in the current search surface.

Accordingly, this file keeps only the retention-specific terminology/mechanism boundary needed by Case 59. A broader NAND programming genealogy — self-boosting, local/self-boost variants, ISPP evolution, inhibit circuits, charge-trap/3-D NAND disturb families, vendor implementation history, and patent-family prosecution — belongs primarily in `computing-archaeology` if developed.

## Result

The bounded chronology can now be stated conservatively:

```text
1997 public NAND record:
    inadvertent programming of nondesignated cells is an explicit inhibit problem

1998 public title-level record:
    `program disturb` is attested in nonvolatile-memory patent vocabulary

1999 directly inspected NAND record:
    `program disturb` and `pass disturb` are explicitly distinguished

2002 Case 59 lineage:
    `floating-gate interference` explicitly describes adjacent-threshold-change / parasitic-capacitance coupling

2013 Case 59 characterization:
    `program interference` is experimentally decomposed by victim/aggressor, location, order, and data value
```

The historiographic rule is the important part:

> **earlier disturb vocabulary and non-target programming mechanisms constrain origin claims, but they do not erase the mechanism boundary around cell-to-cell program interference.**
'''
ADDENDUM.write_text(addendum.rstrip() + "\n", encoding="utf-8")

status_old = "**`grounded`** — bounded to floating-gate MLC NAND cell-to-cell **program interference** as documented from 2002 through the 2013 commercial-2Y-nm characterization, with a 2007 manufacturer-linked architecture paper constraining prior art and a 2014 neighbor-assisted correction paper used only as a bounded recovery extension."
status_new = "**`grounded`** — bounded to floating-gate MLC NAND cell-to-cell **program interference** as documented from 2002 through the 2013 commercial-2Y-nm characterization, with a 2007 manufacturer-linked architecture paper constraining prior art and a 2014 neighbor-assisted correction paper used only as a bounded recovery extension. A separate 1997–1999 terminology/prior-art addendum now grounds earlier NAND inhibit / `program disturb` vocabulary without folding those mechanisms into the cell-to-cell genealogy."
replace_once(CASE, status_old, status_new)

case_link_old = "Grounding record: [`../evidence/59-nand-2002-2014-program-interference-grounding.md`](../evidence/59-nand-2002-2014-program-interference-grounding.md)."
case_link_new = case_link_old + "\n\nTerminology/prior-art addendum: [`../evidence/59-program-disturb-1997-1999-terminology-mechanism-boundary.md`](../evidence/59-program-disturb-1997-1999-terminology-mechanism-boundary.md)."
replace_once(CASE, case_link_old, case_link_new)

case_anchor = "### `floating-gate interference` by 2002"
case_insert = r'''### Pre-2002 `program disturb` / NAND inhibit boundary

A separate primary-source deepening now prevents this case from treating 2002 `floating-gate interference` as the beginning of every programming-induced non-target error. Samsung US5677873A (published **14 October 1997**) already documents a NAND inhibit problem in which nondesignated cells can be inadvertently programmed during adjacent programming unless channel/source/bitline potentials are biased or boosted appropriately. The inspected patent does not establish the later cell-to-cell interference model and is retained in its own historical vocabulary.

A later AMD record, US5991202A (published **23 November 1999**), explicitly defines NAND **`program disturb`** as unintended programming of an unselected cell on a selected word line and separately names **`pass disturb`** for another unselected-cell path in the self-boosting/pass-voltage regime. A 6 October 1998 Invox patent title supplies an earlier public title-level `program disturb` witness for multilevel nonvolatile memory, but its full mechanism is not used here without direct inspection.

Therefore the prior-art rule is now stronger:

> **pre-2002 program-disturb / program-inhibit evidence ≠ proof of the 2002+ cell-to-cell capacitive program-interference mechanism.**

And conversely:

> **2002 `floating-gate interference` vocabulary ≠ origin of every NAND programming-induced disturb problem.**

See the dedicated [`program-disturb terminology/mechanism addendum`](../evidence/59-program-disturb-1997-1999-terminology-mechanism-boundary.md) for the source chronology and rejected origin upgrades.

'''
replace_once(CASE, case_anchor, case_insert + case_anchor)

# Link the canonical evidence record to the new addendum and sharpen its terminology section.
ev_link_old = "This record grounds [`../cases/59-nand-program-interference-write-induced-neighbor-drift.md`](../cases/59-nand-program-interference-write-induced-neighbor-drift.md)."
ev_link_new = ev_link_old + "\n\nPre-2002 terminology/mechanism deepening: [`59-program-disturb-1997-1999-terminology-mechanism-boundary.md`](59-program-disturb-1997-1999-terminology-mechanism-boundary.md)."
replace_once(EVIDENCE, ev_link_old, ev_link_new)

ev_anchor = "## 2002 prior-art record"
ev_insert = r'''## 1997–1999 adjacent prior art: program inhibit / `program disturb`

The dedicated addendum directly inspects two manufacturer patent records that precede the 2002 floating-gate-interference paper:

- **Samsung US5677873A, published 14 October 1997** — NAND-specific inadvertent programming of nondesignated cells is an explicit programming/inhibit problem; boosting the channel/source/drain condition reduces Fowler–Nordheim programming risk in cells that should remain unprogrammed.
- **AMD US5991202A, published 23 November 1999** — `program disturb` is explicitly defined for unintended programming of an unselected cell on the selected word line, while `pass disturb` is separately named in the same self-boosting/pass-voltage discussion.

A **6 October 1998** Invox patent title provides an earlier public title-level use of `program disturb` for multilevel nonvolatile memory; because its full description was not directly inspected in this pass, the addendum does not use it for NAND-specific mechanism claims.

This earlier evidence narrows origin language but does **not** extend the Case 59 cell-to-cell lineage backward. The safe distinction is:

> **failed program inhibition / unintended programming ≠ aggressor-threshold-transition-induced capacitive victim shift.**

The common functional relation is only that the logical program target can be narrower than the physical electrical effect scope.

'''
replace_once(EVIDENCE, ev_anchor, ev_insert + ev_anchor)

roadmap_anchor = "- [x] NAND Flash read-disturb historical deepening / duplicate consolidation —"
roadmap_text = ROADMAP.read_text(encoding="utf-8")
if roadmap_text.count(roadmap_anchor) != 1:
    raise SystemExit(f"ROADMAP anchor count {roadmap_text.count(roadmap_anchor)}")
roadmap_bullet = "- [x] Case 59 pre-2002 NAND `program disturb` terminology / program-inhibit boundary — canonical [`cases/59-nand-program-interference-write-induced-neighbor-drift.md`](cases/59-nand-program-interference-write-induced-neighbor-drift.md), with new [`evidence/59-program-disturb-1997-1999-terminology-mechanism-boundary.md`](evidence/59-program-disturb-1997-1999-terminology-mechanism-boundary.md), now adds a 14-Oct-1997 Samsung NAND inadvertent-programming/inhibit witness and a directly inspected 23-Nov-1999 AMD record that explicitly distinguishes `program disturb` from `pass disturb`; a 6-Oct-1998 Invox title remains only a bibliographic terminology witness in this pass. This closes the bounded anti-anachronism gap `pre-2002 disturb vocabulary/mechanisms != Case-59 cell-to-cell capacitive interference`, while pre-1997 genealogy, full Invox facsimile inspection, commercial deployment, later self/local-boost evolution, charge-trap/3-D NAND families, and patent-prosecution history remain open and should primarily live in `computing-archaeology`.\n\n"
ROADMAP.write_text(roadmap_text.replace(roadmap_anchor, roadmap_bullet + roadmap_anchor, 1), encoding="utf-8")

index = INDEX.read_text(encoding="utf-8").rstrip()
if "**2402 —" in index or "## Case 59 deepening — pre-2002" in index:
    raise SystemExit("Case 59 deepening findings already present")
if "**2401 —" not in index:
    raise SystemExit("expected current ledger to include finding 2401")

findings = r'''

## Case 59 deepening — pre-2002 `program disturb` / program-inhibit findings

- **2402 — 1995 priority / 1996 filing ≠ 1997 public NAND evidence:** Samsung US5677873A has earlier family/filing dates but the directly inspectable US publication is 14 October 1997; origin chronology must keep these events distinct. (`H/P`, `X`)
- **2403 — inadvertent NAND programming is publicly documented before the 2002 floating-gate-interference paper:** the 1997 Samsung record treats nondesignated-cell programming during adjacent programming as a real bias/inhibit problem. (`H/P`)
- **2404 — pre-2002 mechanism attestation ≠ later terminology attestation:** the inspected Samsung record grounds inadvertent programming and boosting without establishing that its authors called the mechanism `program disturb`. (`H/P`, `X`)
- **2405 — title-level `program disturb` use is public by October 1998:** US5818757A's public title is `Analog and multi-level memory with reduced program disturb`; this pass uses it only as a bibliographic terminology witness, not for unseen NAND-specific mechanism detail. (`H/P*`, `X`)
- **2406 — directly inspected NAND-specific `program disturb` definition is public by November 1999:** AMD US5991202A explicitly uses the term for unintended programming of an unselected cell on the selected word line. (`H/P`)
- **2407 — `program disturb` ≠ `pass disturb` even inside one 1999 NAND self-boosting record:** AMD separately names the selected-wordline non-target programming path and an unselected-cell path associated with pass/self-boost conditions. (`H/P`, `E`)
- **2408 — program-inhibit failure ≠ Case-59 cell-to-cell program interference:** the former concerns keeping non-target cells outside an unintended tunneling/programming regime; the latter concerns a programmed aggressor's threshold transition capacitively shifting an already-programmed victim. (`H/P`, `E`, `X`)
- **2409 — same cross-target effect pattern ≠ same physical mechanism:** both histories show a program operation affecting state outside its logical target, but shared operation-scope asymmetry does not merge voltage paths, coupling, clocks, or mitigations. (`E`, `A`, `X`)
- **2410 — transient inhibit/bias state can be retention infrastructure without being payload:** maintaining boosted/inhibited electrical conditions during another cell's program can protect non-target retained state even though that control condition is not user data. (`E`)
- **2411 — terminology continuity ≠ mechanism identity ≠ proven genealogy:** an earlier use of `program disturb` cannot silently rename the 2002 `floating-gate interference` mechanism, and the later interference vocabulary cannot be projected backward onto every earlier inadvertent-programming record. (`H/P`, `E`, `X`)
- **2412 — 1997/1999 patents ≠ proof of named-product deployment:** manufacturer patent disclosure establishes technical proposals and vocabulary, not that a particular shipped Flash device used the disclosed mitigation. (`H/P`, `X`)
- **2413 — NAND program inhibit and magnetic-core half-select are functional analogies only:** both expose non-target state to part of a write's physical excitation, but magnetic coincidence fields, NAND boosting/tunneling, and floating-gate neighbor coupling are physically and historically distinct. (`A`, `X`)
- **2414 — related-repository boundary:** a fresh `tmzncty/computing-archaeology` search for `program disturb` / `disturb` surfaced no dedicated case to reuse; Case 59 keeps the retention-specific terminology/mechanism correction while broad NAND programming, boosting, patent, and 3-D disturb genealogy belongs there if developed. (`H/P` project-state record)
'''
INDEX.write_text(index + findings + "\n", encoding="utf-8")

# Basic local invariants before the workflow's git-level validation.
for path in (CASE, EVIDENCE, ADDENDUM, ROADMAP, INDEX):
    text = path.read_text(encoding="utf-8")
    if "\r" in text:
        raise SystemExit(f"CRLF introduced in {path}")
    if not text.endswith("\n"):
        raise SystemExit(f"missing final newline in {path}")

ledger = INDEX.read_text(encoding="utf-8")
for n in range(2402, 2415):
    if ledger.count(f"**{n} —") != 1:
        raise SystemExit(f"finding {n} count != 1")

print("Case 59 program-disturb deepening integrated")
