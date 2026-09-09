from pathlib import Path
import re

CASE = Path("cases/10-toshiba-leakage-tracked-self-refresh.md")
EVIDENCE = Path("evidence/10-toshiba-1984-self-refresh-scheduling-grounding.md")
ADDENDUM = Path("evidence/10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md")
ROADMAP = Path("ROADMAP.md")
INDEX = Path("CASE_INDEX.md")

addendum = """# Evidence 10 Addendum — Hitachi 1982–1984 Leakage-Comparator Self-Refresh Prior Art

## Purpose

Independently inspect the Hitachi record that Toshiba US4682306A cited as prior art, so Case 10 no longer depends on Toshiba's retrospective description for the earlier leakage-aware self-refresh boundary.

This addendum is deliberately narrow. It establishes a **manufacturer-primary public mechanism floor by 31 March 1984** for a DRAM automatic/self-refresh design whose trigger is derived from leakage-simulation capacitor state. It does not establish the first invention of leakage-aware refresh, a named commercial implementation, or a direct Hitachi-to-Toshiba implementation genealogy.

---

## Source identity and chronology

**Hitachi Ltd., JPS5956291A, _MOS storage device_** (Japanese publication; Google Patents supplies a machine-translated transcription of the period document).

- application / priority: **JP57164829A, 24 September 1982**;
- publication: **JPS5956291A, 31 March 1984**;
- inventors listed in the record: Kiyobumi Uchibori, Norimasa Yasui, Yoshiaki Onishi, Hiroshi Kawamoto;
- assignee: Hitachi Ltd.;
- directly inspected transcription: <https://patents.google.com/patent/JPS5956291A/en>.

Chronology guardrail:

> **24 September 1982 filing/priority ≠ 31 March 1984 public disclosure.**

The earlier date is relevant to the family chronology. The directly inspectable public-document floor used by this repository is the publication date.

---

## Direct historical record

### H/P — the source distinguishes externally requested refresh from a fully automatic objective

The description begins from dynamic-memory charge leakage and the need to read, amplify, and rewrite information before it is lost. It then discusses an earlier `automatic refresh` arrangement driven through an external refresh-control terminal and says that requiring the external control signal means that arrangement cannot be regarded as fully automatic refresh.

The Hitachi invention's stated objective is therefore not merely `DRAM needs refresh`; it is to internalize more of the decision/control path while reducing unnecessary refresh power.

### H/P — fixed conservative self-refresh is treated as an energy problem

The source says actual cell leakage varies, including with temperature, and argues that a fixed refresh period sized with margin for the worst condition performs refresh more frequently than necessary in less demanding conditions. The exact quantitative/process relations in the document remain period- and design-specific rather than universal DRAM laws.

### H/P — automatic refresh includes address, oscillation, and leakage-simulation blocks

The disclosed automatic-refresh circuit contains a refresh-address counter, a leakage-current simulation circuit, and an oscillation circuit. The oscillator produces pulses for address stepping during self-refresh, while the refresh-address counter forms internal refresh addresses.

This independently confirms that the design combines two relations that must not be collapsed:

```text
when maintenance should start
    !=
which row maintenance should address next
```

### H/P — two retained analog control states are compared

The principal embodiment uses two precharged capacitors, C1 and C2, in the leakage-current simulation circuit. Their initial levels, capacitances, and/or leakage are deliberately arranged so that the held voltage of C2 falls faster than that of C1 in relation to the desired memory-cell refresh period.

A voltage-comparison circuit receives the two held voltages. The important historical relation is therefore comparative rather than a single fixed timer value:

```text
held state Va on C1
    compared with
held state Vb on C2
    -> relation reverses as leakage proceeds
```

The patent also discusses alternative ways to obtain the required relation, including equal capacitance with different leakage and structures whose capacitor/leakage characteristics can be engineered to track the memory-cell problem.

### H/P — comparison reversal activates self-refresh work

When the C1/C2 voltage relation reverses, the comparator-derived self-refresh control signal changes state. That state admits oscillator pulses to the refresh counter, selects the counter's internally formed address path, and marks self-refresh as in progress. The described interface blocks outside writes/reads during this interval.

The counter then supplies refresh addresses so that the full memory-cell set is refreshed. Counter overflow precharges C1/C2 again and ends the self-refresh pass, beginning another monitoring interval.

A bounded state-machine reconstruction is:

```text
C1/C2 precharged
    -> leakage changes their held voltages at intentionally different rates
    -> comparator relation reverses
    -> self-refresh control state asserted
    -> oscillator pulses reach refresh-address counter
    -> internal refresh addresses traverse the array
    -> counter overflow
    -> C1/C2 re-precharged
    -> monitoring interval restarts
```

### H/P — the claims preserve the same relation

Claim 1 names first and second precharged capacitors, a voltage-comparison circuit receiving their held voltages, and an automatic-refresh control circuit activated by the comparator's inverted output to self-refresh dynamic memory cells according to an internally generated address signal. Claim 4 separately allows the automatic-refresh circuit also to be activated by an external control signal.

This claim structure keeps **autonomous condition-derived triggering** separate from the continued possibility of an externally requested refresh path.

---

## Prior-art effect on Case 10

Before this direct inspection, Case 10 knew JPS5956291A only through Toshiba US4682306A's explicit prior-art discussion. That was enough to block a Toshiba priority claim, but not enough to ground Hitachi's circuit details independently.

Direct inspection changes the evidence status:

```text
before:
Toshiba says earlier Hitachi work used two leakage-monitor capacitors + comparator

now:
Hitachi's own 1984 public document directly shows
    two precharged leakage-simulation capacitors
    + voltage comparison
    + comparator-derived self-refresh control
    + internal oscillator/counter/address path
    + full-pass completion/re-precharge cycle
```

The defensible novelty boundary for Toshiba therefore becomes narrower. Toshiba US4682306A remains a strong later mechanism witness for its own preferred **single monitor-capacitor + threshold/inverter + intermittent refresh-pass** design, but it is not the repository's earliest directly inspected leakage-derived self-refresh mechanism.

---

## Engineering reconstruction

### E — payload retention state ≠ maintenance-proxy state

The user payload is the dynamic-cell information being preserved. C1/C2 hold different state: intentionally decaying analog control evidence used to decide when preservation work should begin.

The project may call these `proxy` or `sentinel` states, but those are reconstruction terms, not Hitachi's recovered vocabulary. The source itself uses leakage-current simulation / comparison language.

### E — trigger authority ≠ enumeration authority ≠ completion evidence

The comparator decides when the condition is met; the oscillator provides pulses; the counter enumerates refresh addresses; overflow marks the end of the pass and reinitializes the monitoring state. Correctness of one relation does not automatically prove correctness of the others.

### E — a preservation mechanism can retain a deliberately unstable control relation

The leakage-simulation capacitors are useful precisely because their stored voltages change. Their controlled decay is not a failure of the retention system; it is the measurement process that schedules work on the payload.

### E — self-refresh availability ≠ ordinary read/write availability

The source's self-refresh-in-progress handling blocks normal external read/write service during the pass. Preserving state can therefore temporarily reduce foreground availability without implying payload loss.

---

## Functional comparison with Toshiba — not genealogy

| Relation | Hitachi JPS5956291A | Toshiba US4682306A |
| --- | --- | --- |
| Public document | 31 Mar 1984 | 21 Jul 1987 (Japanese priority 20 Aug 1984) |
| Condition state | two precharged leakage-simulation capacitors | preferred monitor capacitor |
| Detection | voltage relation/comparator | monitor threshold/inverter/control path |
| Active refresh work | oscillator + refresh-address counter + internally selected addresses | oscillator + refresh-address counter + row decoder |
| Completion/reset | counter overflow re-precharges monitor capacitors | pass completion resets/recharges monitor state |

This is a **functional/mechanism comparison**, not proof that Toshiba copied Hitachi, that the circuits are transistor-for-transistor descendants, or that one patent family exhausts the historical genealogy.

---

## Anti-anachronism and evidence limits

- `adaptive refresh`, `closed-loop refresh`, `proxy`, and `sentinel` remain modern analytical vocabulary unless a period source uses them.
- `self-refresh` / `automatic refresh` are used here only where supported by the period documents; their exact distinction is source-specific and must not be projected into later JEDEC command semantics.
- one directly inspected 1984 publication does **not** establish first invention or complete prior art;
- patent disclosure does **not** establish a named shipping DRAM or pseudo-SRAM implementation;
- a shared objective and similar block roles do **not** prove direct Hitachi→Toshiba genealogy;
- machine translation is adequate here for mechanism discovery/cross-checking against circuit labels and claims, but a later priority dispute or wording-sensitive historiographic claim should consult the Japanese facsimile or a specialist translation.

---

## Related-repository boundary

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `JPS5956291A` and `self-refresh` found no dedicated treatment to reuse.

`technical-retention` therefore keeps this narrow correction because it changes the retention-specific novelty boundary. A broader history of Hitachi/Toshiba DRAM families, pseudo-SRAM, leakage monitors, oscillator design, process scaling, standards, and commercial deployment belongs primarily in `computing-archaeology` if developed.

---

## Grounding decision

**Status: direct primary prior-art deepening accepted.**

The source independently grounds a public 1984 leakage-comparator self-refresh mechanism and converts what had been an indirect Toshiba citation into direct manufacturer-primary evidence. It narrows Toshiba's novelty boundary without creating a new invention-priority claim.
"""
ADDENDUM.write_text(addendum.rstrip() + "\n", encoding="utf-8")

case = CASE.read_text(encoding="utf-8")
ground = "Grounding record: [`../evidence/10-toshiba-1984-self-refresh-scheduling-grounding.md`](../evidence/10-toshiba-1984-self-refresh-scheduling-grounding.md)."
deep = "Prior-art deepening: [`../evidence/10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md`](../evidence/10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md)."
if deep not in case:
    assert ground in case
    case = case.replace(ground, ground + "\n\n" + deep, 1)

old = "The patent itself cites Hitachi Japanese Laid-Open Patent 59-56291, priority 24 September 1982 and publication 31 March 1984, as earlier work that automatically controlled refresh frequency using leak-monitor capacitors and a comparator. This case therefore makes no priority claim for Toshiba."
new = """The patent itself cites Hitachi Japanese Laid-Open Patent 59-56291, priority/filing 24 September 1982 and publication 31 March 1984, as earlier work that automatically controlled refresh frequency using leak-monitor capacitors and a comparator. That Hitachi document has now been **independently inspected** rather than used only through Toshiba's retrospective description. Its own text directly discloses a refresh-address counter, oscillator, two-capacitor leakage-simulation circuit, voltage comparator, comparator-derived self-refresh control, internally selected refresh addresses, full-array refresh, and overflow-triggered re-precharge. See the [direct prior-art addendum](../evidence/10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md).

The direct inspection moves the public manufacturer-primary floor for this bounded leakage-derived self-refresh relation to **31 March 1984**. It still does not establish first invention, commercial deployment, or a complete genealogy, and the 24 September 1982 filing/priority date must not be silently reported as the public-disclosure date. Toshiba's later preferred embodiment remains a distinct mechanism witness, notably using one monitor capacitor and a threshold/inverter control path rather than Hitachi's two retained capacitor voltages and differential comparison. This case therefore makes no priority claim for Toshiba and no priority claim for Hitachi beyond the bounded public floor."""
if new not in case:
    assert old in case
    case = case.replace(old, new, 1)

anchor = "| A named Toshiba commercial part is proven to use this exact circuit | X | unsupported product-identity leap |"
if "directly inspected JPS5956291A" not in case:
    assert anchor in case
    rows = """| Hitachi publicly disclosed a two-capacitor leakage-simulation + comparator self-refresh mechanism by 31 March 1984 | H/P | directly inspected JPS5956291A |
| The 1982 Hitachi filing/priority date is itself a public-disclosure date | X | filing/priority must remain distinct from 1984 publication |
| Hitachi's two-capacitor comparator circuit and Toshiba's single-monitor preferred embodiment are the same circuit | X | shared preservation function does not erase circuit differences |
"""
    case = case.replace(anchor, rows + anchor, 1)

oldsrc = "2. Hitachi Ltd., JPS5956291A, _MOS storage device_, priority 24 September 1982, publication 31 March 1984 — used here only through Toshiba's explicit prior-art description/citation unless independently inspected: <https://patents.google.com/patent/JPS5956291A/ja>."
newsrc = "2. Hitachi Ltd., JPS5956291A, _MOS storage device_, application/priority 24 September 1982, publication 31 March 1984 — now directly inspected for the two-capacitor leakage-simulation/comparator self-refresh mechanism; detailed anchors and limits are in [`../evidence/10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md`](../evidence/10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md): <https://patents.google.com/patent/JPS5956291A/en>."
if newsrc not in case:
    assert oldsrc in case
    case = case.replace(oldsrc, newsrc, 1)
CASE.write_text(case.rstrip() + "\n", encoding="utf-8")

ev = EVIDENCE.read_text(encoding="utf-8")
start = ev.index("### Prior-art control inside the primary source")
end = ev.index("\n---\n\n## Direct historical claims", start)
replacement = """### Prior-art control — Hitachi source now independently inspected

The Toshiba patent itself cites **Japanese Laid-Open Patent 59-56291 / JPS5956291A**, Hitachi Ltd., application/priority 24 September 1982 and publication 31 March 1984, as earlier leakage-aware self-refresh work. The repository has now inspected that Hitachi document directly rather than relying only on Toshiba's retrospective description.

The Hitachi source itself discloses an automatic-refresh circuit containing a refresh-address counter, oscillator, and leakage-current simulation circuit. Its principal embodiment precharges two capacitors whose held voltages evolve at intentionally different rates, compares those voltages, and uses reversal of their relation to assert a self-refresh control state. Oscillator pulses then advance internal refresh addresses through the array; counter overflow re-precharges the monitoring capacitors and ends the pass. Claim 1 preserves the first/second-capacitor + comparator + internally addressed automatic-refresh relation, while claim 4 separately allows external triggering.

Detailed direct anchors, chronology, and the Hitachi/Toshiba mechanism comparison are recorded in [`10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md`](10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md).

Therefore:

> **US4682306A is a strong mechanism witness for the bounded Toshiba design; it is not evidence that Toshiba invented leakage-aware or adaptive refresh in general. Direct JPS5956291A inspection establishes an earlier public manufacturer-primary floor by 31 March 1984, but not first invention, product deployment, or complete genealogy.**

The Hitachi filing/priority date (**24 September 1982**) is not silently substituted for its public publication date (**31 March 1984**).

The Toshiba patent also cites H. Kawamoto et al., **“A 288Kb CMOS Pseudo SRAM,”** ISSCC 1984, pp. 276–277, as period context. This record does not rely on an uninspected full text of that paper for central claims.
"""
if "Hitachi source now independently inspected" not in ev:
    ev = ev[:start] + replacement.rstrip() + ev[end:]

old_limit = """### Patent mechanism ≠ invention priority

The patent itself describes Hitachi Japanese Laid-Open Patent 59-56291 as prior art that automatically controls refresh frequency using leakage-monitor capacitors. The project therefore makes no `first adaptive self-refresh` claim."""
new_limit = """### Patent mechanism ≠ invention priority

Direct inspection of Hitachi JPS5956291A strengthens the prior-art boundary: the earlier public document itself shows leakage-simulation capacitors, voltage comparison, internal self-refresh control, oscillator/counter work, and internal refresh addressing. It still does not establish that Hitachi was historically first, that a named product shipped the exact circuit, or that Toshiba's preferred circuit is a direct implementation descendant. The project therefore makes no `first adaptive self-refresh` claim for either bounded patent family."""
if new_limit not in ev:
    assert old_limit in ev
    ev = ev.replace(old_limit, new_limit, 1)

old_rel = "A current code search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `self refresh`, `self-refresh`, and the Toshiba patent/circuit terms found no dedicated case for this mechanism."
new_rel = "Fresh code searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `self-refresh` and `JPS5956291A` found no dedicated treatment to reuse."
if new_rel not in ev:
    assert old_rel in ev
    ev = ev.replace(old_rel, new_rel, 1)
EVIDENCE.write_text(ev.rstrip() + "\n", encoding="utf-8")

road = ROADMAP.read_text(encoding="utf-8")
entry = """- [x] Case 10 Hitachi 1982/1984 leakage-comparator self-refresh prior-art deepening — canonical [`cases/10-toshiba-leakage-tracked-self-refresh.md`](cases/10-toshiba-leakage-tracked-self-refresh.md), with [`evidence/10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md`](evidence/10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md), now independently inspects JPS5956291A instead of relying only on Toshiba's later citation: the 31-March-1984 public Hitachi document directly grounds two precharged leakage-simulation capacitors, voltage comparison, comparator-derived self-refresh control, oscillator/counter internal addressing, full-array refresh, and overflow-triggered monitor re-precharge. This narrows Toshiba's later novelty boundary to its distinct preferred monitor/threshold implementation without claiming Hitachi priority beyond this public floor. The 24-September-1982 filing/priority date remains distinct from publication; first invention, pre-1982 genealogy, named-product deployment, standards lineage, and wider DRAM circuit/product history remain open and should primarily live in `computing-archaeology`."""
if "Case 10 Hitachi 1982/1984 leakage-comparator self-refresh prior-art deepening" not in road:
    marker = "- [x] Case 93 AVATAR VRT-aware runtime-requalification deepening"
    assert marker in road
    road = road.replace(marker, entry + "\n" + marker, 1)
ROADMAP.write_text(road.rstrip() + "\n", encoding="utf-8")

idx = INDEX.read_text(encoding="utf-8")
lines = idx.splitlines()
found = False
for i, line in enumerate(lines):
    if line.startswith("| [Toshiba Leakage-Tracked Self-Refresh: Internalizing Refresh Scheduling]"):
        lines[i] = "| [Toshiba Leakage-Tracked Self-Refresh: Internalizing Refresh Scheduling](cases/10-toshiba-leakage-tracked-self-refresh.md) | **grounded** | dynamic payload + decaying on-chip leak-monitor/comparison state + condition-derived refresh trigger + oscillator + refresh-address counter | separate refresh-address internalization from refresh-schedule internalization; show condition-derived maintenance and deliberately decaying control state; independently bound pre-Toshiba leakage-comparator prior art | [Toshiba 1984 self-refresh scheduling grounding](evidence/10-toshiba-1984-self-refresh-scheduling-grounding.md) + [Hitachi 1982–1984 prior-art deepening](evidence/10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md); pre-1982 genealogy, named-product implementation, later standards/self-refresh evolution, and modern retention-aware policy remain separate work |"
        found = True
        break
assert found
idx = "\n".join(lines).rstrip() + "\n"

heading = "## Case 10 deepening — Hitachi 1982/1984 leakage-comparator self-refresh prior-art findings"
if heading not in idx:
    assert "**2426 —" in idx
    findings = """## Case 10 deepening — Hitachi 1982/1984 leakage-comparator self-refresh prior-art findings

- **2427 — 24-September-1982 filing/priority ≠ 31-March-1984 public disclosure.** JPS5956291A's family chronology can bound an earlier application date, but this pass uses the 1984 publication as the directly inspectable public technical floor. (`H/P`, `X`)
- **2428 — direct Hitachi evidence ≠ Toshiba-only retrospective inference.** The earlier mechanism is now grounded in JPS5956291A's own description/claims rather than only in US4682306A's later prior-art paragraph. (`H/P`)
- **2429 — externally requested automatic refresh ≠ the source's fully automatic self-refresh objective.** Hitachi explicitly treats a scheme that still requires an external refresh-control signal as not fully automatic, preserving a period control-locus distinction rather than a modern label alone. (`H/P`)
- **2430 — internal refresh-address generation ≠ leakage-derived refresh triggering.** The Hitachi circuit contains both an internal refresh counter/address path and a separate leakage-simulation/comparison relation that decides when self-refresh begins; Case 09 already shows why those authorities must remain distinct. (`H/P`, `E`)
- **2431 — two-capacitor differential comparison ≠ Toshiba's later preferred single-monitor threshold path.** Both designs derive maintenance from decaying control state, but their directly documented detection circuits are not identical. (`H/P`, `A`, `X`)
- **2432 — same preservation function ≠ same circuit mechanism or proven genealogy.** Shared roles such as leakage sensing, oscillator activation, row enumeration, and monitor reset support a bounded functional comparison only. (`A`, `X`)
- **2433 — payload state ≠ leakage-simulation control state.** C1/C2 are retained analog control evidence used to schedule preservation of dynamic-cell information; they are not the user payload being preserved. (`H/P`, `E`)
- **2434 — comparator threshold/relation crossing ≠ full refresh-pass completion.** Trigger assertion, oscillator pulses, counter enumeration, array restoration, overflow, and monitor re-precharge remain separate obligations in the source's sequence. (`H/P`, `E`)
- **2435 — self-refresh service exclusion ≠ payload forgetting.** JPS5956291A blocks ordinary external read/write during the self-refresh interval, showing that foreground unavailability can be part of preservation work rather than evidence of state loss. (`H/P`, `E`)
- **2436 — direct 1984 prior art narrows Toshiba novelty ≠ proof that Hitachi invented leakage-aware refresh.** One earlier manufacturer-primary publication is sufficient to reject a Toshiba-first claim for the bounded relation but not to close pre-1982 priority or circuit genealogy. (`H/P`, `X`)
- **2437 — patent disclosure ≠ named-product deployment or standards adoption.** Neither JPS5956291A nor the Toshiba patent alone proves that a specific shipping DRAM/pseudo-SRAM implemented the exact preferred circuit or that later JEDEC self-refresh inherited it. (`H/P`, `X`)
- **2438 — related-repository boundary remains explicit.** Fresh `tmzncty/computing-archaeology` searches for `JPS5956291A` and `self-refresh` found no dedicated case to reuse; this repository keeps the retention-specific prior-art correction while broader DRAM product/circuit/standards genealogy belongs there if developed. (`H/P` project-state record)
"""
    idx = idx.rstrip() + "\n\n" + findings.rstrip() + "\n"
INDEX.write_text(idx.rstrip() + "\n", encoding="utf-8")

for p in [CASE, EVIDENCE, ADDENDUM, ROADMAP, INDEX]:
    s = p.read_text(encoding="utf-8")
    assert s.endswith("\n") and not s.endswith("\n\n"), p
assert ADDENDUM.stat().st_size > 3000
assert ADDENDUM.name in CASE.read_text(encoding="utf-8")
assert "Hitachi source now independently inspected" in EVIDENCE.read_text(encoding="utf-8")
assert "Case 10 Hitachi 1982/1984 leakage-comparator self-refresh prior-art deepening" in ROADMAP.read_text(encoding="utf-8")
ind = INDEX.read_text(encoding="utf-8")
assert ADDENDUM.name in ind
for n in range(2427, 2439):
    assert len(re.findall(rf"\*\*{n} —", ind)) == 1, n
