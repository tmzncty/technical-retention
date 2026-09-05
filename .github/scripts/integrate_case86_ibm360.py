from pathlib import Path
import re

ROOT = Path('.')


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


def write(path, text):
    (ROOT / path).write_text(text, encoding='utf-8')


def replace_once(path, old, new):
    text = read(path)
    if new in text:
        return
    if old not in text:
        raise SystemExit(f'anchor missing in {path}: {old[:120]!r}')
    text = text.replace(old, new, 1)
    write(path, text)


def insert_before(path, anchor, block, marker):
    text = read(path)
    if marker in text:
        return
    if anchor not in text:
        raise SystemExit(f'anchor missing in {path}: {anchor[:120]!r}')
    text = text.replace(anchor, block.rstrip() + '\n\n' + anchor, 1)
    write(path, text)


def insert_after(path, anchor, block, marker):
    text = read(path)
    if marker in text:
        return
    if anchor not in text:
        raise SystemExit(f'anchor missing in {path}: {anchor[:120]!r}')
    text = text.replace(anchor, anchor + '\n\n' + block.rstrip(), 1)
    write(path, text)


# ---------------------------------------------------------------------------
# Case 02: reconcile stale first-pass wording with its already-grounded record.
# This is status/source maintenance, not a new historical claim.
# ---------------------------------------------------------------------------
case02 = 'cases/02-magnetic-core-destructive-read.md'
text = read(case02)
if '**Status:** `grounded`' not in text:
    title = '# Magnetic Core Memory: Retention at Rest, Destruction in Reading\n'
    if title not in text:
        raise SystemExit('Case 02 title anchor missing')
    text = text.replace(
        title,
        title + '\n**Status:** `grounded`\n\nGrounding record: [`../evidence/02-magnetic-core-1951-1954-grounding.md`](../evidence/02-magnetic-core-1951-1954-grounding.md)\n',
        1,
    )
    write(case02, text)

replace_once(
    case02,
    'The current first-pass rests on four evidence layers.',
    'The case is now `grounded` through the dedicated evidence record. The layers below remain useful orientation, while that record adds exact primary-source anchors, an implemented read–rewrite witness, and bounded nondestructive-read counterexamples.'
)

text = read(case02)
if '## Grounding status and remaining archival cleanup' not in text:
    pattern = re.compile(
        r"## Evidence gaps before `grounded`\n\nThis case remains `first-pass` until at least the following are done:\n\n"
        r"(?:- .*\n)+\n---",
        flags=re.MULTILINE,
    )
    replacement = '''## Grounding status and remaining archival cleanup

This case is `grounded`. The dedicated grounding record closes the former promotion blockers with:

- direct Forrester patent page/figure anchors for two stable states, destructive read, and rewrite;
- Papian's 1953 *The M.I.T. Magnetic-Core Memory* as a machine-specific implemented destructive-read / rewrite witness;
- Mayer & Papian M-2121 for the address/buffer-register and write-part-of-cycle control path;
- Widrow 1954 and Brown's 1953-filed patent as bounded contemporary nondestructive-read counterexamples;
- a separate Case 86 system-level witness showing why remanent main-memory state must not be equated with whole-machine restart state.

Remaining archival cleanup is narrower: obtain a conveniently renderable full scan of Papian's 1952 IRE paper for direct page-level inspection. The central Case-02 claims no longer depend uniquely on its abstract.

---'''
    text2, n = pattern.subn(replacement, text, count=1)
    if n != 1:
        raise SystemExit('Case 02 stale grounding block not found exactly once')
    write(case02, text2)

replace_once(
    case02,
    "Papian's IRE paper is contemporary technical evidence. This first pass currently uses the MIT archival abstract for its explicit statement about remanent flux and repeated nonselecting disturbances; the full paper still requires direct inspection.",
    "Papian's 1952 IRE paper remains contemporary technical evidence for remanence and repeated nonselecting disturbances; direct page-level inspection of a conveniently renderable full scan remains archival cleanup. The case no longer depends uniquely on that abstract because the grounding record adds Papian's 1953 implemented-memory paper, Mayer & Papian M-2121, and other primary witnesses."
)

insert_before(
    case02,
    '- [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history)',
    '- [`Case 86 — DEC PDP-8 core-resident power-fail save and automatic restart`](86-dec-pdp8-core-power-fail-auto-restart.md) — system-level boundary: remanent main-memory contents can survive a power transition while volatile execution/control state still requires a separate save, reset, and restart protocol;',
    'Case 86 — DEC PDP-8 core-resident power-fail save'
)

# ---------------------------------------------------------------------------
# Case 86: deepen with IBM System/360 Model 65 controlled power sequencing.
# ---------------------------------------------------------------------------
case86 = 'cases/86-dec-pdp8-core-power-fail-auto-restart.md'

scope_anchor = "A 1968 PDP-8/L / 1970 Small Computer Handbook witness shows the same basic relation persisted in the later KP8/L / KP8/I option family. An IBM 7090 operator manual is used only as an earlier comparative witness that operator-level `reset` could clear processor/control state while leaving core storage unaffected, whereas a separate `clear` operation zeroed the cores. It is **not** evidence that DEC derived KR01 from IBM."
insert_after(
    case86,
    scope_anchor,
    "A separate IBM System/360 Model 65 primary manual supplies a different 1968 boundary witness. Its normal `POWER ON` sequence performs a system reset while preserving main storage, and its normal `POWER OFF` sequence preserves main-storage contents — but explicitly not the storage-associated controls for the protection feature — when the CPU is stopped, with a five-second delay before power removal. This is evidence for controlled power-transition state-class separation, **not** for automatic restart after an arbitrary power failure and not for lineage into DEC KR01.",
    'five-second delay before power removal'
)

historical_block = '''### H/P — IBM System/360 Model 65 preserves main storage across controlled power sequencing while excluding protection controls

IBM's *System/360 Model 65 Functional Characteristics*, Fourth Edition (September 1968), gives a useful contemporary counterexample to any simple equation between `system reset`, `power off`, and `memory erase`.

Under `POWER ON`, IBM states that the power-on sequence performs a **system reset** so that no instructions or I/O operations occur until explicitly directed, while **the contents of main storage are preserved**.

Under `POWER OFF`, IBM states that pressing the button initiates the power-off sequence and that:

- main-storage contents are preserved **provided the CPU is in the stopped state**;
- the `controls in storage associated with the protection feature` are explicitly excluded from that preservation statement;
- there is a **5-second delay** between pressing `POWER OFF` and removal of power.

This is a strong period-primary witness for three bounded distinctions:

```text
system reset ≠ main-storage erase
main-storage preservation ≠ preservation of every storage-associated control
controlled power-off preservation ≠ automatic restart after arbitrary power failure
```

The source does not say that the 5-second delay itself is the physical cause of magnetic retention, and this case does not infer such a mechanism. The delay and stopped-state precondition are treated as parts of the documented transition protocol, not as proof of a particular storage-substrate implementation.'''
insert_before(
    case86,
    '### H/P — IBM 7090 separates processor reset from core clear before KR01',
    historical_block,
    'IBM System/360 Model 65 preserves main storage across controlled power sequencing'
)

engineering_block = '''### E — controlled transition protocol can be retention infrastructure without being retained payload

The Model 65 witness adds a different retention path from KR01. DEC's bounded failure path moves selected volatile execution state into core before ordinary powered logic disappears. IBM's documented normal power-off path instead requires the CPU to be stopped and delays removal of power while preserving main storage and excluding a class of protection controls from the preservation statement.

The shared engineering reconstruction is only this:

> the survival of a useful state across a power boundary can depend on **which state class is being discussed and which transition protocol is followed**.

It does **not** follow that a normal shutdown sequence and a sudden-failure save routine are the same mechanism.

### E — payload continuity and protection/control continuity can diverge

The explicit IBM exception matters because `main storage survives` is not equivalent to `every relation that governs use of main storage survives`.

This yields the bounded distinction:

```text
payload-addressed main-storage state
        ≠
protection/control state associated with storage
```

That distinction is historically grounded by IBM's wording; treating it as a general `state-class persistence` principle is project reconstruction.'''
insert_before(
    case86,
    '### E — core-content survival ≠ processor execution-state survival',
    engineering_block,
    'controlled transition protocol can be retention infrastructure without being retained payload'
)

cross_block = '''### IBM System/360 Model 65 — controlled power-off versus emergency restart

The 1968 Model 65 manual supplies a deliberately different power-boundary witness:

```text
normal POWER ON → system reset + main storage preserved
normal POWER OFF → CPU stopped + main storage preserved
                 → protection-associated storage controls excluded
                 → 5-second delay before power removal
```

DEC KR01 instead detects impending power loss during operation and uses a short save window to move active CPU context into core before later reconstructing execution.

Therefore:

> `controlled power-off preservation ≠ failure-triggered automatic restart`.

The comparison is useful because both systems separate storage survival from other machine/control state, but no historical lineage or circuit equivalence is claimed.'''
insert_before(
    case86,
    '### IBM 7090 — reset versus clear',
    cross_block,
    'IBM System/360 Model 65 — controlled power-off versus emergency restart'
)

claim_anchor = '| core-content survival is insufficient for CPU execution-state survival | E | reconstruction from DEC\'s explicit save requirement |'
insert_before(
    case86,
    claim_anchor,
    '| Model 65 power-on can perform system reset while preserving main storage | H/P | IBM System/360 Model 65 Functional Characteristics, Fourth Edition, System Control Panel |\n| Model 65 normal power-off preserves main storage only under a stopped-CPU condition and excludes protection-associated controls | H/P | IBM 1968, `POWER OFF Pushbutton` |\n| controlled power-off preservation is not evidence of arbitrary-failure automatic restart | E | bounded comparison between IBM 1968 and DEC KR01 |',
    'Model 65 power-on can perform system reset while preserving main storage'
)

source_anchor = '4. **IBM, _IBM 7090 Data Processing System Operator\'s Guide_**, early-1960s edition/revision, `IBM 7151 Console Control`, panel keys 26 `Clear Key` and 27 `Reset Key`. Public scan/extraction: <https://manualzz.com/doc/19740167/ibm-7090-data-processing-system-operator%E2%80%99s-guide>.'
insert_after(
    case86,
    source_anchor,
    '5. **IBM, _IBM System/360 Model 65 Functional Characteristics_, Fourth Edition, September 1968, Form A22-6884-3**, `System Control Panel`, printed pp. 13–14, `POWER ON Pushbutton` / `POWER OFF Pushbutton`. Direct scan: <https://www.bitsavers.org/pdf/ibm/360/functional_characteristics/GA22-6884-3_System_360_Model_65_Functional_Characteristics_196809.pdf>. Searchable transcription used as an inspection aid: <https://manualzilla.com/doc/5665606/ibm-360-65---bitsavers.org>.',
    'GA22-6884-3_System_360_Model_65_Functional_Characteristics_196809.pdf'
)

replace_once(case86, '5. **Smithsonian National Museum of American History**', '6. **Smithsonian National Museum of American History**')
replace_once(case86, '6. [`tmzncty/computing-archaeology:', '7. [`tmzncty/computing-archaeology:')

insert_before(
    case86,
    '- and a later PDP-8-family witness preserving the same basic relation.',
    '- a contemporary IBM Model 65 witness that system reset / normal power-off can preserve main storage while a named protection-control class is excluded;\n',
    'contemporary IBM Model 65 witness'
)

# ---------------------------------------------------------------------------
# Evidence 86: add a source-specific grounding section and comparison rows.
# ---------------------------------------------------------------------------
ev86 = 'evidence/86-dec-1960-1970-core-power-restart-grounding.md'
source_e = '''### E — IBM System/360 Model 65 Functional Characteristics, September 1968

**Source:** IBM, *IBM System/360 Model 65 Functional Characteristics*, Fourth Edition, September 1968, Form A22-6884-3.  
**Primary status:** manufacturer-primary / contemporary.  
**Direct scan:** <https://www.bitsavers.org/pdf/ibm/360/functional_characteristics/GA22-6884-3_System_360_Model_65_Functional_Characteristics_196809.pdf>  
**Searchable inspection aid:** <https://manualzilla.com/doc/5665606/ibm-360-65---bitsavers.org>  
**Location:** `System Control Panel`, printed pp. 13–14, `POWER ON Pushbutton` and `POWER OFF Pushbutton`.

#### Directly supported facts

The manual states that:

1. the `POWER ON` pushbutton initiates the power-on sequence;
2. that sequence performs a **system reset** so no instructions or I/O operations occur until explicitly directed;
3. **the contents of main storage are preserved** across that power-on/reset sequence;
4. the `POWER OFF` pushbutton initiates the system power-off sequence;
5. main-storage contents are preserved on normal power-off **provided the CPU is in the stopped state**;
6. the manual explicitly excludes `controls in storage associated with the protection feature` from that preservation statement;
7. there is a **5-second delay** between depression of `POWER OFF` and removal of power.

#### Why it matters here

This is not another KR01 witness. It supplies a contrasting contemporary transition protocol in which ordinary main-storage state survives a normal reset/power cycle while a named class of storage-associated control state does not share the same preservation contract.

It therefore strengthens the bounded distinctions:

- `system reset ≠ main-storage erase`;
- `main-storage payload continuity ≠ protection/control continuity`;
- `controlled power-off preservation ≠ automatic restart after arbitrary failure`.

The source does **not** establish:

- that the 5-second delay is the physical cause of storage retention;
- that an unplanned power failure preserves the same state;
- that the machine automatically resumes an interrupted program after power returns;
- that IBM's design influenced DEC KR01;
- or that every Model 65 storage/control component has the same physical retention mechanism.'''
insert_before(ev86, '### E — Smithsonian publication artifact metadata', source_e, 'IBM System/360 Model 65 Functional Characteristics, September 1968')
replace_once(ev86, '### E — Smithsonian publication artifact metadata', '### F — Smithsonian publication artifact metadata')
replace_once(ev86, '### F — related-repository source reuse', '### G — related-repository source reuse')

insert_before(
    ev86,
    '| core-content survival ≠ execution-context survival | DEC sources + Case 02 | E | strong reconstruction | project phrasing, not DEC terminology |',
    '| Model 65 power-on reset preserves main storage | IBM 1968 Model 65 manual | H/P | strong | normal documented sequence only |\n| Model 65 normal power-off preserves main storage but excludes protection-associated controls | IBM 1968 Model 65 manual | H/P | strong | requires stopped CPU; not arbitrary failure |\n| controlled shutdown preservation ≠ failure-triggered automatic restart | IBM 1968 + DEC 1966 | E | strong bounded comparison | no lineage/circuit equivalence claim |',
    'Model 65 power-on reset preserves main storage'
)

prior_anchor = 'The IBM 7090 witness already demonstrates an earlier commercially documented distinction between resetting processor/control state and deliberately clearing core storage. Other machines likely had power-fail, restart, and nonvolatile-core operational practices as well. Establishing a full chronology would require a wider survey of vendor manuals, power-supply circuitry, operating practices, and software conventions.'
replace_once(
    ev86,
    prior_anchor,
    prior_anchor + '\n\nThe September 1968 IBM Model 65 witness is used differently: it is a contemporary **counterexample/control boundary** showing that a normal reset/power sequence can preserve main storage while excluding a named protection-control class. It is not evidence of a DEC→IBM or IBM→DEC genealogy and does not extend the KR01 sudden-failure contract to the Model 65.'
)

hist_anchor = 'IBM explicitly documents separate `Clear` and `Reset` effects on core versus processor/control state.'
replace_once(
    ev86,
    hist_anchor,
    hist_anchor + '\n\nIBM Model 65 documentation separately states that power-on system reset preserves main storage and that normal power-off preserves main storage, subject to a stopped-CPU condition, while excluding protection-feature controls and delaying power removal for five seconds.'
)

eng_anchor = '- `processor continuation ≠ peripheral/external-world continuity`.'
replace_once(
    ev86,
    eng_anchor,
    eng_anchor + '\n- `controlled power-transition preservation ≠ arbitrary-failure restart`;\n- `main-storage continuity ≠ protection/control continuity`.'
)

cross_ev_block = '''### IBM System/360 Model 65 controlled-transition comparison

Use the 1968 IBM source only to establish a contrasting state-class and transition boundary:

```text
power-on system reset + main storage preserved
normal power-off + stopped CPU + main storage preserved
protection-associated controls explicitly excluded
```

Do not convert this into evidence that the Model 65 automatically resumed an interrupted program after sudden power loss. DEC KR01 remains the failure-triggered save/restart mechanism in this case.'''
insert_before(ev86, '### IBM 7090 comparison', cross_ev_block, 'IBM System/360 Model 65 controlled-transition comparison')

# ---------------------------------------------------------------------------
# README navigation: deepen the existing Case-86 map entry, no new case count.
# ---------------------------------------------------------------------------
readme = 'README.md'
old_readme_line = "- [`cases/86-dec-pdp8-core-power-fail-auto-restart.md`](cases/86-dec-pdp8-core-power-fail-auto-restart.md) — grounded magnetic-core/system-restart bridge: DEC's 1966 PDP-8 KR01 turns impending primary-power loss into a bounded 1 ms save interval in which software copies active register/program-count state into known core locations; restored power enters through address 0000 and reconstructs execution state while Power Clear separately resets internal/I/O control state; see [`evidence/86-dec-1960-1970-core-power-restart-grounding.md`](evidence/86-dec-1960-1970-core-power-restart-grounding.md)."
new_readme_line = "- [`cases/86-dec-pdp8-core-power-fail-auto-restart.md`](cases/86-dec-pdp8-core-power-fail-auto-restart.md) — grounded magnetic-core/system-restart bridge: DEC's 1966 PDP-8 KR01 turns impending primary-power loss into a bounded 1 ms save interval in which software copies active register/program-count state into known core locations; restored power enters through address 0000 and reconstructs execution state while Power Clear separately resets internal/I/O control state. A 1968 IBM System/360 Model 65 counterexample now separates controlled power-on/off preservation of main storage from protection-control continuity and from sudden-failure automatic restart; see [`evidence/86-dec-1960-1970-core-power-restart-grounding.md`](evidence/86-dec-1960-1970-core-power-restart-grounding.md)."
replace_once(readme, old_readme_line, new_readme_line)

# ---------------------------------------------------------------------------
# ROADMAP: record this bounded magnetic-core/system transition deepening.
# ---------------------------------------------------------------------------
roadmap = 'ROADMAP.md'
roadmap_anchor = '- [x] NAND Flash read-disturb historical deepening / duplicate consolidation'
roadmap_block = "- [x] Magnetic-core/system power-transition deepening — canonical [`cases/86-dec-pdp8-core-power-fail-auto-restart.md`](cases/86-dec-pdp8-core-power-fail-auto-restart.md) now adds IBM's September 1968 System/360 Model 65 normal power-sequence witness: system reset can preserve main storage, and normal `POWER OFF` preserves main storage only under a stopped-CPU condition while explicitly excluding protection-associated controls and delaying removal of power for five seconds. This sharpens `main-storage continuity ≠ control-state continuity` and `controlled shutdown ≠ failure-triggered automatic restart` without duplicating broad core-memory history from `computing-archaeology`. The same pass reconciles stale `first-pass` language in grounded Case 02 with its existing evidence record; remaining Case-02 work is direct Papian-1952 facsimile cleanup rather than promotion work."
insert_before(roadmap, roadmap_anchor, roadmap_block, 'Magnetic-core/system power-transition deepening')

# ---------------------------------------------------------------------------
# CASE_INDEX: enrich the canonical Case-86 row and append cross-case findings.
# ---------------------------------------------------------------------------
index = 'CASE_INDEX.md'
idx = read(index)
if '1968 IBM Model 65 controlled-transition counterexample' not in idx:
    lines = idx.splitlines()
    candidates = [i for i, line in enumerate(lines) if 'cases/86-dec-pdp8-core-power-fail-auto-restart.md' in line and line.startswith('|')]
    if len(candidates) != 1:
        raise SystemExit(f'expected one Case-86 table row, got {len(candidates)}')
    i = candidates[0]
    line = lines[i]
    if ' | ' not in line:
        raise SystemExit('Case-86 row format unexpected')
    # Add the deepening to the methodological-use cell without changing status/case count.
    parts = line.split(' | ')
    if len(parts) < 5:
        raise SystemExit('Case-86 row has too few cells')
    parts[-2] = parts[-2] + '; 1968 IBM Model 65 controlled-transition counterexample separates main-storage preservation from protection-control continuity and sudden-failure restart'
    lines[i] = ' | '.join(parts)
    write(index, '\n'.join(lines) + ('\n' if idx.endswith('\n') else ''))

idx = read(index)
if '### Case 86 deepening — IBM System/360 Model 65 controlled power-transition boundary' not in idx:
    if not idx.endswith('\n'):
        idx += '\n'
    idx += '''
### Case 86 deepening — IBM System/360 Model 65 controlled power-transition boundary

1275. **planned power-off preservation ≠ automatic execution restart** — the 1968 Model 65 manual preserves main storage through its normal power sequence, but this does not establish continuation of an interrupted instruction stream; DEC KR01 remains the separate failure-triggered save/restart witness.

1276. **main-storage payload continuity ≠ protection-control continuity** — IBM explicitly preserves main-storage contents during normal power-off while excluding `controls in storage associated with the protection feature` from that preservation statement.

1277. **system reset ≠ main-storage erase** — the Model 65 power-on sequence performs a system reset while preserving main storage, reinforcing the earlier IBM 7090 Reset-vs-Clear boundary without claiming identical controls or lineage.

1278. **transition protocol can be retention infrastructure without being retained payload** — the stopped-CPU precondition and five-second delayed power removal are operational conditions surrounding preservation, not user payload and not evidence that the delay physically stores the bits.

1279. **controlled shutdown path ≠ sudden-failure path** — IBM's normal `POWER OFF` witness must not be projected onto DEC KR01's approximately 1 ms emergency save interval or onto arbitrary external power failure.

1280. **element nonvolatility ≠ uniform state-class nonvolatility** — Case 02 grounds remanent core state at the memory-element/access-cycle level, while Case 86 and the IBM counterexample show that processor, protection, I/O, and main-storage state can cross the same power lifecycle under different preservation rules.
'''
    write(index, idx)

# Basic assertions before workflow-level diff checks.
for p in [case02, case86, ev86, readme, roadmap, index]:
    t = read(p)
    if '\r\n' in t:
        raise SystemExit(f'CRLF unexpectedly introduced in {p}')

print('Case 86 IBM System/360 deepening and Case 02 status reconciliation staged successfully.')
