#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
git pull --ff-only origin main

python3 - <<'PY'
from pathlib import Path
import re

case = Path('cases/02-magnetic-core-destructive-read.md')
evidence = Path('evidence/02-1965-1966-core-power-transition-retention-deepening.md')
index = Path('CASE_INDEX.md')
roadmap = Path('ROADMAP.md')

for p in [case, index, roadmap, Path('AGENTS.md'), Path('docs/METHOD.md'), Path('docs/PRIOR_ART.md'), Path('docs/TECHNICAL_SPINE.md'), Path('RELATED_REPOS.md')]:
    if not p.exists():
        raise SystemExit(f'missing prerequisite: {p}')
if evidence.exists():
    raise SystemExit(f'refusing to overwrite existing evidence file: {evidence}')

evidence_text = r'''# Case 02 Deepening — Magnetic-Core Power-Off Retention, Transition Hazards, and Restart Apparatus (1965–1966)

## Purpose

This record deepens [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md) around one bounded question that the main case already warns about but does not yet ground with named-machine operating evidence:

> if magnetic core is nonvolatile while unpowered, what still has to be preserved or controlled when an actual computer is powered down and powered back up?

The answer is not simply `nothing`. Two period machine manuals show that core contents could be intended to survive power removal while the **transition into and out of the powered state** still required explicit operational or circuit protection.

This deepening therefore separates:

```text
quiescent magnetic retention
    !=
power-transition immunity
    !=
whole-machine execution continuity
```

Claim layers follow repository policy: **Historical record**, **Engineering reconstruction**, **Functional analogy**, and **Philosophical interpretation** remain distinct.

## Sources inspected

### IBM 1401 Data Processing System — Operator's Guide, Form A24-3144-2

Manufacturer document, **Major Revision, March 1965**. The original IBM publication is accessed here through archival mirrors rather than a current IBM origin host.

Archival copies / records:

- <https://bitsavers.trailing-edge.com/pdf/ibm/1401/A24-3144-2_1401_operGuide.pdf>
- <https://www.eserviceinfo.com/downloadsm/90766/IBM_A24-3144-2%201401%20operGuide.html>
- Computer History Museum 1401 restoration index linking the same IBM manual: <https://ibm1401.computerhistory.org/>

The relevant operating instructions are on printed p. 129 in the archived copy. The guide tells the operator to place the 1401 mode switch in `ALTER` for controlled power transitions. On power-on in that mode, **information in core storage is retained**. On power-off in that mode, **information is retained in core storage until power is turned on again**. The same instructions also mention relay sequencing used to avoid damage from repeated switching.

**Evidence boundary:** this is named-machine operating evidence for an IBM 1401 and its prescribed controlled procedure. It is not a universal guarantee that every magnetic-core computer preserves all memory through every arbitrary outage or malformed transition.

### Digital Equipment Corporation PDP-7 Maintenance Manual, F-77A (1966)

Manufacturer maintenance manual for PDP-7 systems with serial numbers 100 and above, archived as:

- <https://bitsavers.org/pdf/dec/pdp7/F-77A_pdp7maint_1966.pdf>
- alternate archival mirror: <https://www.soemtron.org/downloads/decinfo/f77apdp7maint1966.pdf>

The relevant power-control description is printed p. 3-6. DEC states that during turn-on the memory is energized only after a delay allowing AC transients to decay. During turn-off, the **memory power supplies are de-energized immediately while computer logic power remains for five seconds**. The manual gives the reason explicitly: the delay prevents switching transients from producing current surges that could destroy information stored in core memory.

During the same turn-on delay, `PWR CLK` / `PWR CLR` activity repeatedly clears the RUN and memory-control flip-flops and establishes initial conditions in peripheral equipment, so a stored program is not accidentally started or disturbed.

**Evidence boundary:** this is a PDP-7/A-family power-control design witness. It demonstrates that one core-memory computer treated power-transition circuitry as part of preserving core contents while intentionally resetting other machine state. It does not establish identical sequencing on IBM, Whirlwind, or every core-memory system.

## Historical record — IBM distinguishes retained core contents from the act of turning power on or off

The IBM 1401 guide does not present core retention as an abstract materials fact only. It places retention inside an operator procedure:

```text
mode switch -> ALTER
power transition
core information retained
```

The important historical fact is not that `ALTER` magically supplies the remanence. Magnetic remanence is already the physical basis of the storage element. The manual instead shows that IBM treated **how the powered system enters or leaves service** as relevant to preserving the stored information.

The wording also blocks a careless universalization. The guide's promise is tied to the documented operating sequence; it is not a blanket statement about every uncontrolled interruption.

## Historical record — PDP-7 explicitly protects nonvolatile core from switching transients

DEC's maintenance manual is even more explicit about the transition hazard. The core array can retain information without powered refresh, yet the surrounding electronics can still generate destructive currents while supplies rise or fall.

The PDP-7 design therefore sequences power domains:

```text
turn on:
logic/control powered first
    -> wait for AC transients to decay
    -> energize memory

turn off:
de-energize memory immediately
    -> keep logic power for ~5 s
```

The manual states that this sequencing prevents current surges from destroying core-memory information.

This is a direct counterexample to the shortcut:

> `nonvolatile = power transitions are irrelevant`.

They are not irrelevant. The medium may not require power to retain its quiescent magnetic state, while the **system transition** can still threaten that state electrically.

## Historical record — preserved core payload coexists with deliberately reset control state

The PDP-7 manual also separates two classes of machine state during turn-on.

While the core contents are being protected from destructive transients, power-clock / power-clear logic clears RUN and memory-control flip-flops and establishes peripheral initial conditions. In other words:

```text
core payload: intended to remain undisturbed
selected control state: intentionally reinitialized
```

The stored program may physically remain in core, but the processor is prevented from simply resuming an uncontrolled pre-power-transition execution state.

This grounds a named-system version of a distinction already stated cautiously in Case 02:

> **element-level nonvolatility != whole-machine restart persistence**.

## Engineering reconstruction — power-off is a state; power-down and power-up are operations

The manuals support a useful three-stage model:

1. **powered operation** — drivers, sense circuits, timing, and control state are active;
2. **quiescent unpowered interval** — remanent magnetization can preserve core contents without refresh power;
3. **power transition** — supply rails and logic states move through intermediate conditions that can create unintended currents or commands.

The engineering implication is:

> **surviving stage 2 does not prove immunity during stages 1→2 or 2→1.**

This is not a new physical theory of ferrite. It is a system reconstruction directly motivated by the machine manuals' operating and circuit precautions.

## Engineering reconstruction — nonvolatile medium can still require retention apparatus at its boundary

A narrow definition of `maintenance` might say that magnetic core needs none while idle because there is no periodic refresh. That is correct for the quiescent bit state, but incomplete for an operational computer.

The PDP-7 supplies a different kind of retention work:

- not periodic restoration of the stored bit;
- not continuous recirculation;
- but **transition control that prevents the support electronics from accidentally rewriting or disturbing the bit**.

Thus:

```text
no steady-state refresh obligation
    !=
no system-level retention obligation
```

The obligation is concentrated at a boundary event rather than repeated on a deadline.

## Engineering reconstruction — restart continuity is compositional

The two manuals support a more precise restart model:

```text
retained core contents
+
safe power-transition behavior
+
known processor/control initialization
+
operator/software restart procedure
=
possible useful restart continuity
```

No single term in that sum is equivalent to the others.

In particular:

- physical retention of words does not preserve registers that are deliberately cleared;
- preservation of words does not prove that external devices retain compatible state;
- safe power sequencing does not prove that a program can resume at the exact interrupted instruction;
- restartability does not imply that every power failure was handled gracefully.

This is why `nonvolatile` is a property of the retained substrate relation, not a complete crash-consistency or restart contract.

## Functional analogy — persistence-domain boundaries, without shared mechanism

At a functional level only, the PDP-7 case resembles later systems in which a durable payload survives while volatile control state must be reconstructed or reinitialized before service resumes.

The analogy stops at that relation. Magnetic-core remanence, modern nonvolatile media, persistent-memory domains, journal replay, and distributed recovery use different substrates, failure models, and protocols. No genealogy is inferred from the comparison.

## Philosophical interpretation — endurance can depend on the manner of re-entry

The technical fact is unusually concrete: a state can remain materially present while unpowered and still be endangered by the operation that reconnects it to an active machine.

A bounded interpretation is therefore:

> persistence is not exhausted by surviving absence of power; availability again depends on a controlled re-entry into an operational apparatus.

This is a project interpretation of the engineering evidence, not language attributed to IBM or DEC engineers.

## Prior-art and anti-anachronism boundaries

This deepening does **not** claim:

- that IBM or DEC invented power-safe core-memory sequencing;
- that the IBM 1401 and PDP-7 use the same power-control circuit;
- that every core-memory computer preserves contents over arbitrary outage, brownout, transient, or service procedure;
- that preserved core contents imply exact instruction-level resume;
- that magnetic-core nonvolatility is equivalent to modern persistent-memory semantics;
- that control flip-flops cleared by PDP-7 power logic are themselves stored in the core array;
- that later terms such as `persistence domain`, `crash consistency`, or `NVDIMM` were historical vocabulary for these systems.

The broader history of power sequencing, fail-safe memory electronics, and machine restart belongs primarily in `tmzncty/computing-archaeology`. This record exists only to tighten Case 02's retention boundary.

## Resulting bounded distinctions

```text
core remanence while unpowered
    !=
power-transition immunity

power-off interval
    !=
power-down / power-up operation

retained core payload
    !=
retained processor-control state

stored program remains
    !=
program automatically resumes

nonvolatile medium
    !=
maintenance-free system boundary

safe power sequencing
    !=
crash consistency

named IBM / DEC behavior
    !=
universal magnetic-core contract
```

## Open work deliberately left outside this slice

- earlier 1950s machine-specific power-transition circuits and operating procedures;
- Whirlwind / Memory Test Computer startup-shutdown primary evidence;
- exact circuit-level comparison between IBM 1401 and DEC PDP-7 power sequencing;
- behavior under uncontrolled brownouts and partial-rail failures;
- diagnostic or restoration experiments on surviving historical machines;
- genealogy from core-memory power protection into later semiconductor-memory power-fail designs.

Those are separate historical-engineering or experimental tasks rather than prerequisites for the bounded retention distinction established here.
'''
evidence.write_text(evidence_text, encoding='utf-8')

# Link the deepening record near the existing Case 02 evidence links.
s = case.read_text(encoding='utf-8')
deep = 'Power-transition retention deepening: [`../evidence/02-1965-1966-core-power-transition-retention-deepening.md`](../evidence/02-1965-1966-core-power-transition-retention-deepening.md). This later IBM/DEC machine evidence grounds `unpowered retention != transition immunity != whole-machine restart continuity`; it does not replace the case\'s 1950–1954 MIT anchor.'
if '02-1965-1966-core-power-transition-retention-deepening.md' not in s:
    anchor = 'Security-erasure vocabulary deepening: [`../evidence/02-1991-ncsc-core-clearing-purging-degaussing-deepening.md`](../evidence/02-1991-ncsc-core-clearing-purging-degaussing-deepening.md). The 1991 NCSC source is a later security-assurance witness, not evidence that early MIT or the 1964 TCM-32 used the same policy vocabulary.'
    if anchor not in s:
        raise SystemExit('Case02 deepening-link anchor missing')
    s = s.replace(anchor, anchor + '\n\n' + deep, 1)

section_heading = '## Power-off retention is not power-transition immunity'
if section_heading not in s:
    anchor = '## Time: two different retention intervals coexist'
    if anchor not in s:
        raise SystemExit('Case02 time-section anchor missing')
    section = r'''## Power-off retention is not power-transition immunity

Later named-machine manuals sharpen the case's warning that core nonvolatility is not a whole-machine restart contract.

IBM's March-1965 **1401 Operator's Guide** tells operators to place the mode switch in `ALTER` for controlled power transitions. In that procedure, information in core storage is retained when power is turned off and is retained when power is turned on again. This is operating-procedure evidence, not a universal promise about arbitrary outages.

DEC's **1966 PDP-7 Maintenance Manual** exposes the electrical reason the boundary matters. Its power-control logic delays energizing memory on turn-on until AC transients have decayed; on turn-off it de-energizes the memory supplies immediately while leaving computer logic powered for about five seconds. DEC states that this sequencing prevents switching-transient current surges from destroying information stored in core memory. During turn-on, other power-clear logic deliberately resets RUN and memory-control flip-flops and initializes peripheral control so the stored program is not accidentally started or disturbed.

Therefore:

```text
core remanence while unpowered
    !=
power-transition immunity

retained core payload
    !=
retained control state

stored program remains
    !=
exact execution resumes
```

The retention work here is not periodic refresh. It is **boundary control**: preventing the active support circuitry from disturbing a medium that otherwise retains its magnetic state without power. This is a later system-level witness and does not change the early MIT chronology that grounds the main case.

See the dedicated deepening record for sources, limits, and the division of labor with `computing-archaeology`.

---

'''
    s = s.replace(anchor, section + anchor, 1)
case.write_text(s, encoding='utf-8')

# Add numbered findings immediately before the comparison matrix. Number from the current ledger maximum.
s = index.read_text(encoding='utf-8')
marker = '## Comparison matrix — provisional\n'
if marker not in s:
    raise SystemExit('CASE_INDEX comparison-matrix marker missing')
route = 'Case 02 magnetic-core power-transition retention deepening'
if route not in s:
    nums = [int(m.group(1)) for m in re.finditer(r'(?m)^(\d+)\.\s', s)]
    if not nums:
        raise SystemExit('CASE_INDEX contains no numbered findings')
    n = max(nums) + 1
    findings = [
        'IBM 1401 Operator\'s Guide A24-3144-2 (Major Revision, March 1965) prescribes `ALTER` mode for controlled power transitions and states that information in core storage is retained across the documented power-off/power-on procedure.',
        'The IBM 1401 evidence is a named-machine operating contract, not a universal guarantee for arbitrary outages; `core nonvolatility != every power-failure path is harmless`.',
        'DEC PDP-7 Maintenance Manual F-77A (1966) delays memory energization on turn-on until AC transients decay and de-energizes memory immediately on turn-off while logic power remains for about five seconds.',
        'DEC explicitly gives preservation of information stored in core memory as the reason for the PDP-7 power sequencing: switching-transient current surges could otherwise destroy retained information.',
        '`quiescent unpowered retention != power-transition immunity`: a nonvolatile magnetic state can survive without refresh yet remain vulnerable to unintended currents while supply/control circuits cross transitional states.',
        'PDP-7 turn-on logic clears RUN and memory-control flip-flops and initializes peripheral control while protecting core contents, grounding `retained core payload != retained processor-control state`.',
        '`stored program remains != exact execution automatically resumes`; useful restart continuity composes retained payload, safe re-entry, initialized control state, and operator/software restart procedure.',
        '`no periodic refresh obligation != no system-level retention obligation`; PDP-7 retention work is concentrated at a power boundary rather than repeated on a refresh deadline.',
        'The IBM and DEC witnesses are complementary but not identical implementations: shared outcome-level retention concerns do not establish common circuit design or direct genealogy.',
        'Functional comparison to later persistent-memory or crash-recovery systems is limited to `durable payload + reconstructed/reinitialized volatile control state`; substrates, protocols, failure models, and historical vocabulary remain distinct.',
        'The deepening does not claim IBM/DEC invention priority for power-safe core sequencing and leaves earlier 1950s power-control genealogy and Whirlwind/MTC startup-shutdown evidence open.',
        'The companion `computing-archaeology` core-memory history already covers nonvolatility and cautions that power loss does not imply perfect resume; this slice adds machine-specific retention-boundary evidence instead of duplicating the general engineering history.'
    ]
    block = '### Case 02 magnetic-core power-transition retention deepening\n\n'
    for i, text in enumerate(findings):
        block += f'{n+i}. {text}\n'
    block += '\n'
    s = s.replace(marker, block + marker, 1)
    index.write_text(s, encoding='utf-8')

# Record the completed bounded deepening in ROADMAP beside Case 02 when possible.
s = roadmap.read_text(encoding='utf-8')
road_line = '- [x] **Case 02 magnetic-core power-transition retention deepening** — [`cases/02-magnetic-core-destructive-read.md`](cases/02-magnetic-core-destructive-read.md) + [`evidence/02-1965-1966-core-power-transition-retention-deepening.md`](evidence/02-1965-1966-core-power-transition-retention-deepening.md): IBM 1401 (March 1965) operator procedure and DEC PDP-7 (1966) power-control documentation now ground the boundary between quiescent magnetic nonvolatility, power-transition hazard, and whole-machine restart. The PDP-7 witness further separates preserved core contents from intentionally reset RUN/memory-control flip-flops. This closes the bounded `unpowered retention != transition immunity`, `retained payload != retained control state`, and `stored program != automatic resume` seams without claiming arbitrary-outage safety, shared IBM/DEC circuitry, invention priority, or modern crash-consistency semantics. Earlier 1950s power-sequencing genealogy, Whirlwind/MTC startup evidence, uncontrolled brownout behavior, and hardware restoration experiments remain open; broader machine/power engineering history belongs primarily in `computing-archaeology`.'
if '02-1965-1966-core-power-transition-retention-deepening.md' not in s:
    lines = s.splitlines()
    anchors = [i for i, line in enumerate(lines) if 'cases/02-magnetic-core-destructive-read.md' in line]
    if anchors:
        lines.insert(anchors[0] + 1, road_line)
    else:
        # Keep Phase-2 additions together if the old Case-02 phase entry has no one-line path anchor.
        phase2 = next((i for i, line in enumerate(lines) if line.strip() == '## Phase 2 — Build missing technical bridges'), None)
        if phase2 is not None:
            lines.insert(phase2 + 2, road_line)
        else:
            lines.append(road_line)
    roadmap.write_text('\n'.join(lines) + ('\n' if s.endswith('\n') else ''), encoding='utf-8')

# Integrity checks.
for p in [case, evidence, index, roadmap]:
    if not p.exists() or p.stat().st_size == 0:
        raise SystemExit(f'empty/missing output: {p}')
if '02-1965-1966-core-power-transition-retention-deepening.md' not in case.read_text(encoding='utf-8'):
    raise SystemExit('Case02 does not link deepening evidence')
if 'Case 02 magnetic-core power-transition retention deepening' not in index.read_text(encoding='utf-8'):
    raise SystemExit('CASE_INDEX findings missing')
if '02-1965-1966-core-power-transition-retention-deepening.md' not in roadmap.read_text(encoding='utf-8'):
    raise SystemExit('ROADMAP status missing')
PY

rm -f .github/workflows/deepen-case02-power-transition.yml scripts/deepen_case02_power_transition_retention.sh

git add -A
if git diff --cached --quiet; then
  echo "No changes to commit"
  exit 0
fi
git commit -m "case02: ground core power-transition retention"
git push origin main
