from pathlib import Path

CASE = Path('cases/86-dec-pdp8-core-power-fail-auto-restart.md')
EVIDENCE = Path('evidence/86-dec-1960-1970-core-power-restart-grounding.md')
ROADMAP = Path('ROADMAP.md')
INDEX = Path('CASE_INDEX.md')
SELF = Path('scripts/deepen_case86_kp8e_hold_up.py')
WORKFLOW = Path('.github/workflows/deepen-case86-kp8e-hold-up.yml')


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding='utf-8')
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected one match, found {n}')
    path.write_text(text.replace(old, new, 1), encoding='utf-8')


def replace_single_line(path: Path, prefix: str, new_line: str, label: str) -> None:
    lines = path.read_text(encoding='utf-8').splitlines()
    hits = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    if len(hits) != 1:
        raise SystemExit(f'{label}: expected one line, found {len(hits)}')
    lines[hits[0]] = new_line
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


# Case 86: correct the old evidence boundary without back-projecting later KP8-E hardware.
replace_once(
    CASE,
    '- a claim that the 1 ms operating interval was specifically capacitor-backed unless a separate DEC power-supply source establishes that physical mechanism;',
    '- a claim that the **1966 KR01** 1 ms interval used the same capacitor hold-up mechanism later documented for PDP-8/E KP8-E; the later 1971–1974 KP8-E sources now ground filter-capacitor hold-up only for that later option/configuration;',
    'Case86 capacitor boundary',
)

case_deepening = r'''### H/P — 1971–1974 KP8-E closes the later PDP-8/E hold-up mechanism without rewriting KR01

A 9 July 1971 DEC engineering specification for `POWER FAIL AND AUTO-RESTART, KP8/E` adds a later PDP-8/E implementation witness. Its overall description says the option protects active-register contents **when properly programmed** and restarts the computer after AC power returns. The specification also separates the lower threshold that sets the Power Low flag / generates the interrupt request from the upper threshold used for restart, gives the programmer one millisecond after Power Low is set, and makes restart independently disableable by the option switch.

The January 1974 *PDP-8/E Maintenance Manual, Volume 2* closes one physical question that the 1966 KR01 handbook left open. In the KP8-E chapter, DEC explicitly says that **filter capacitors in the power supply** guarantee continued operation for one millisecond, enough for the interrupt request to be recognized and the interrupt routine to run. The same chapter again says the power-fail sequence stores PC, AC, MQ, and Link in known memory locations and that restart enters through a configured memory location.

This later source changes the evidence boundary, but only locally:

```text
1974 PDP-8/E KP8-E: capacitor-backed hold-up is directly documented
        ≠
1966 PDP-8 KR01: exact energy-storage implementation established
```

The later manual therefore permits a stronger engineering reconstruction for KP8-E — stored electrical energy preserves **time to transfer state**, while memory preserves the transferred computational state — without retroactively assigning the same circuit or supply implementation to KR01, KP8/L, or KP8/I.

Primary sources for this deepening:

- DEC, *Engineering Specification: Power Fail and Auto-Restart, KP8/E*, A-SP-KP8-E-1, 9 July 1971, rev. A 16 July 1971: <https://deramp.com/downloads/mfe_archive/011-Digital%20Equipment%20Corporation/02%20PDP-8e/03%20PDP-8e%20Options/KP8-E%20M848%20Power%20Fail%20Detect/01%20KP8-E%20Documentation/KP8-E_PwrFail_EngrDrws_May73.pdf>.
- DEC, *PDP-8/E Maintenance Manual, Volume 2: Internal Bus Options*, January 1974, Part 4 Chapter 1 `KP8-E Power Fail and Auto-Restart`: <https://bitsavers.computerhistory.org/pdf/dec/pdp8/pdp8e/DEC-8E-HMM2A-D-D_PDP-8e_Maintenance_Manual_Volume_2_Internal_Bus_Options_Jan74.pdf>.

'''
replace_once(
    CASE,
    '### H/P — IBM System/360 Model 65 preserves main storage across controlled power sequencing while excluding protection controls\n',
    case_deepening + '### H/P — IBM System/360 Model 65 preserves main storage across controlled power sequencing while excluding protection controls\n',
    'Case86 deepening insertion',
)

replace_once(
    CASE,
    'This is comparable in function to later emergency power-fail work, but the case does not infer a capacitor, battery, or other particular energy-storage implementation from the user handbook alone.',
    'For the 1966 KR01, the user handbook alone still does not identify the exact energy-storage implementation. The later PDP-8/E KP8-E manual does: its filter capacitors guarantee the documented one-millisecond operating interval. This supports `hold-up energy ≠ retained payload` for KP8-E while preserving the anti-back-projection boundary for KR01.',
    'Case86 engineering hold-up paragraph',
)

replace_once(
    CASE,
    '| KR01 was capacitor-backed | X | not established by the handbook evidence used here |',
    '| PDP-8/E KP8-E filter capacitors guarantee the documented 1 ms operating interval | H/P | DEC 1974 Volume 2, KP8-E Chapter 1 |\n| the 1966 KR01 used the same capacitor hold-up implementation | X | later KP8-E evidence cannot be back-projected to the earlier option |',
    'Case86 claim ledger',
)

replace_once(
    CASE,
    '- the exact energy-storage/power-supply circuit that physically provides the 1 ms interval;',
    '- the exact energy-storage/power-supply implementation that provides the 1966 KR01 1 ms interval (the later PDP-8/E KP8-E path is now explicitly grounded to power-supply filter capacitors, but that evidence is not back-projected);',
    'Case86 evidence boundary',
)

# Evidence 86: extend the date range and add the later primary-source ledger.
replace_once(
    EVIDENCE,
    '# Grounding Record 86 — DEC PDP-8 Core-Resident Power-Fail Save and Automatic Restart, 1960–1970',
    '# Grounding Record 86 — DEC PDP-8 Core-Resident Power-Fail Save and Automatic Restart, 1960–1974',
    'Evidence86 title',
)

evidence_deepening = r'''### H — DEC KP8/E Engineering Specification, 9 July 1971 (rev. A 16 July 1971)

**Source:** Digital Equipment Corporation, *Engineering Specification: Power Fail and Auto-Restart, KP8/E*, A-SP-KP8-E-1, dated 9 July 1971, revision A 16 July 1971.  
**Primary status:** manufacturer-primary / contemporary engineering specification.  
**Surviving scan:** <https://deramp.com/downloads/mfe_archive/011-Digital%20Equipment%20Corporation/02%20PDP-8e/03%20PDP-8e%20Options/KP8-E%20M848%20Power%20Fail%20Detect/01%20KP8-E%20Documentation/KP8-E_PwrFail_EngrDrws_May73.pdf>.

#### Directly supported facts

The specification states that:

1. KP8/E protects active-register contents **when properly programmed** and restarts the computer when AC power is restored;
2. a lower threshold sets the Power Low flag and generates the interrupt request, while a separate upper threshold is used for restart;
3. `SPL` 6102 should be first in the interrupt-service skip chain;
4. after Power Low is set, the programmer has **one millisecond** before supply levels fall below operating levels;
5. the option's enable/disable switch can prevent automatic restart after power returns.

#### Boundary

This is a later PDP-8/E implementation witness. It does not establish that every earlier PDP-8-family option used identical thresholds, circuitry, or restart logic.

---

### I — DEC PDP-8/E Maintenance Manual, Volume 2, January 1974

**Source:** Digital Equipment Corporation, *PDP-8/E Maintenance Manual, Volume 2: Internal Bus Options*, January 1974, Part 4 Chapter 1, `KP8-E Power Fail and Auto-Restart`.  
**Primary status:** manufacturer-primary / contemporary maintenance manual.  
**Direct scan:** <https://bitsavers.computerhistory.org/pdf/dec/pdp8/pdp8e/DEC-8E-HMM2A-D-D_PDP-8e_Maintenance_Manual_Volume_2_Internal_Bus_Options_Jan74.pdf>.

#### Directly supported facts

The chapter states that:

1. KP8-E monitors the primary-power condition through the machine supply;
2. when line voltage falls below the lower condition, `UP` is negated, `PWR LOW` is set, and the OMNIBUS interrupt request is asserted;
3. **filter capacitors in the power supply guarantee continued operation for 1 ms**, sufficient for interrupt recognition and the program-interrupt routine;
4. because the interval is bounded, `SPL` should be the first status check;
5. the shutdown routine stores PC, AC, MQ, and Link in known memory locations before ordinary operation stops.

#### Why this source changes the case

Earlier Case-86 evidence deliberately refused to infer the physical source of the 1966 KR01 one-millisecond interval. The 1974 KP8-E manual now directly grounds a capacitor-backed hold-up path for the later PDP-8/E implementation.

The safe historical statement is therefore:

```text
later KP8-E capacitor hold-up = directly documented
1966 KR01 capacitor hold-up = still unproven by the inspected KR01 source
```

This is a source-deepening correction, not a reason to create a second PDP-8 power-fail case.

---

'''
replace_once(
    EVIDENCE,
    '## Evidence table\n',
    evidence_deepening + '## Evidence table\n',
    'Evidence86 deepening insertion',
)

replace_once(
    EVIDENCE,
    '| KR01 uses capacitor-backed hold-up | inspected source does not say | X | unsupported | do not infer physical implementation |',
    '| PDP-8/E KP8-E filter capacitors guarantee the 1 ms continued-operation interval | DEC 1974 Volume 2, KP8-E Ch. 1 | H/P | strong | later KP8-E implementation only |\n| 1966 KR01 uses the same capacitor hold-up implementation | later KP8-E evidence only | X | unsupported back-projection | exact KR01 supply mechanism remains open |',
    'Evidence86 claim-table boundary',
)

replace_once(
    EVIDENCE,
    'The 1968/1970 DEC witnesses show that this relation persisted in the later PDP-8 family.\n',
    'The 1968/1970 DEC witnesses show that this relation persisted in the later PDP-8 family. The 1971/1974 KP8-E sources then deepen the later implementation by directly identifying a one-millisecond programming budget and, in the maintenance manual, the filter-capacitor hold-up that sustains it. They do **not** move the 1966 historical floor or justify back-projecting the later power-supply implementation into KR01.\n',
    'Evidence86 prior-art boundary',
)

# Roadmap: update the existing canonical Case 86 line and the broader power-loss status line.
replace_single_line(
    ROADMAP,
    '- [x] magnetic-core whole-system power-fail / restart boundary — ',
    '- [x] magnetic-core whole-system power-fail / restart boundary — [`cases/86-dec-pdp8-core-power-fail-auto-restart.md`](cases/86-dec-pdp8-core-power-fail-auto-restart.md), grounded by [`evidence/86-dec-1960-1970-core-power-restart-grounding.md`](evidence/86-dec-1960-1970-core-power-restart-grounding.md), now deepened through DEC\'s 9-Jul-1971 KP8/E engineering specification and January-1974 PDP-8/E Volume-2 maintenance manual. The later KP8-E evidence explicitly identifies power-supply filter capacitors as the source of the one-millisecond continued-operation window, while retaining `when properly programmed`, distinct failure/restart thresholds, and independently disableable auto-restart. This closes the bounded `hold-up energy vs saved execution state vs nonvolatile main memory vs restart authority` relation for KP8-E without back-projecting the capacitor implementation into the 1966 KR01. Pre-DEC genealogy, exact KR01 hold-up circuitry, peripheral-state recovery, field fault injection, and later solid-state-memory restart evolution remain separate work for `computing-archaeology`.',
    'ROADMAP Case86 line',
)

replace_single_line(
    ROADMAP,
    '- [ ] power loss — ',
    '- [ ] power loss — **substantially advanced at the DRAM physical-state, SSD-device, access-authority, and whole-computer execution-state layers by grounded Cases 127, 15, 126, and 86**: Case 127 shows that removing power/refresh can end ordinary DRAM service before all physical bit state becomes unrecoverable; Case 15 separates volatile staging, explicit flush, orderly shutdown, capacitor-backed SSD transfer, and a named recovery defect/fix; Case 126 shows reservation/registration coordination state whose power-loss survival is controlled by `PTPL`; and the Case-86 KP8-E deepening now grounds a 1971–1974 DEC path in which power-failure detection plus filter-capacitor hold-up buys one millisecond for software to move volatile CPU context into memory before later restart. Together these ground `power loss ≠ one universal forgetting boundary`, `hold-up energy ≠ retained computational state`, `nonvolatile main memory ≠ resumable computation`, `documented protection architecture ≠ bug-free recovery`, and `payload durability ≠ access-authority durability`. Independent named-device post-fix SSD fault injection, later-DRAM platform validation, exact 1966 KR01 hold-up circuitry, peripheral recovery, controller families, physical-cell loss across other media, and broader power-failure genealogies remain open;',
    'ROADMAP power-loss line',
)

# CASE_INDEX: append a bounded deepening section rather than creating duplicate Case 129.
index = INDEX.read_text(encoding='utf-8').rstrip()
if '## Case 86 deepening — PDP-8/E KP8-E hold-up findings' in index:
    raise SystemExit('Case86 deepening already present')
if '**2238 — related-repository boundary:**' not in index:
    raise SystemExit('expected current finding 2238 not found')
if any(f'**{n} —' in index for n in range(2239, 2251)):
    raise SystemExit('finding collision in 2239–2250')
section = r'''## Case 86 deepening — PDP-8/E KP8-E hold-up findings

- **2239 — later KP8-E capacitor evidence ≠ retrospective proof of KR01 circuitry:** DEC's January-1974 PDP-8/E manual explicitly assigns the one-millisecond continued-operation interval to power-supply filter capacitors, while the inspected 1966 KR01 handbook still leaves its exact energy source unspecified. (`H/P`, `X`)
- **2240 — hold-up energy ≠ retained execution payload:** KP8-E capacitors preserve enough electrical energy/time for interrupt and save work; PC/AC/MQ/Link values are retained later in memory rather than in the capacitors as computational state. (`H/P`, `E`)
- **2241 — one-millisecond programming budget ≠ core-retention interval:** the 1971 engineering specification bounds how long software has before supply levels fall below operating levels; it is not a shelf-life statement for magnetic-core words. (`H/P`, `E`, `X`)
- **2242 — failure threshold ≠ restart threshold:** the KP8/E engineering specification separates the lower threshold that sets Power Low / requests interruption from the upper threshold used for restart, so shutdown admission and restart admission are distinct control relations. (`H/P`, `E`)
- **2243 — `when properly programmed` ≠ autonomous hardware checkpoint:** DEC's own specification makes software arrangement part of preserving active-register contents; option presence alone does not prove that a complete context was saved. (`H/P`, `X`)
- **2244 — Power Low interrupt ≠ checkpoint completion:** detection and interrupt admission only open a bounded save opportunity; required register-to-memory transfers must still finish before operating voltage is lost. (`H/P`, `E`)
- **2245 — checkpoint survival ≠ automatic-restart authority:** KP8/E can prevent restart with its enable/disable switch even if memory contents remain available. (`H/P`, `E`)
- **2246 — nonvolatile main memory ≠ resumable computation:** a useful restart still composes surviving program/data, successfully serialized volatile CPU context, restart control, and restoration software. (`H/P`, `E`)
- **2247 — later implementation detail ≠ historical-origin shift:** 1971–1974 KP8-E evidence deepens how the later PDP-8/E path works; it does not move the documented 1966 KR01 floor forward or prove first invention. (`H/P`, `X`)
- **2248 — same broad save/restart function ≠ identical option implementation:** KR01, KP8/L, KP8/I, and KP8/E can be compared as a PDP-8-family continuity relation without assuming identical threshold, power-supply, timing, or circuit details. (`H/P`, `A`, `X`)
- **2249 — PDP-8 hold-up analogy ≠ SSD power-loss-protection genealogy:** Case 15 and the later KP8-E path both use stored energy to finish failure-triggered retention work, but software-to-core and controller-to-NAND are different mechanisms and histories. (`A`, `X`)
- **2250 — related-repository boundary:** fresh searches still found no dedicated KP8-E / PDP-8 power-fail case in `tmzncty/computing-archaeology`; broad minicomputer power-fail, supply, and restart genealogy belongs there, while this deepening remains bounded to retention handoff and restart authority. (`H/P` project-state record)
'''
INDEX.write_text(index + '\n\n' + section.rstrip() + '\n', encoding='utf-8')

# One-shot integration infrastructure must not survive the canonical commit.
if SELF.exists():
    SELF.unlink()
if WORKFLOW.exists():
    WORKFLOW.unlink()
