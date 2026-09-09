from pathlib import Path

ROOT = Path('.')


def write_text(path, text):
    p = ROOT / path
    p.write_text(text.rstrip() + '\n', encoding='utf-8')


def replace_once(path, old, new):
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected marker once, found {count}: {old[:120]!r}')
    write_text(path, text.replace(old, new, 1))


def replace_line_prefix(path, prefix, new_line):
    p = ROOT / path
    lines = p.read_text(encoding='utf-8').splitlines()
    matches = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    if len(matches) != 1:
        raise SystemExit(f'{path}: expected one line prefix {prefix!r}, found {len(matches)}')
    lines[matches[0]] = new_line
    write_text(path, '\n'.join(lines))


def append_once(path, marker, block):
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    if marker in text:
        raise SystemExit(f'{path}: marker already present: {marker}')
    write_text(path, text.rstrip() + '\n\n' + block.strip())


addendum = r'''# Case 02 deepening — TCM-32 clear/write and whole-stack memory-clear semantics, 1964

This evidence addendum deepens [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md) without reopening the general history of magnetic-core memory.

**Bounded question:** once classic core memory is already known to retain state through remanence and to use destructive read/restore in an important historical regime, what did a later production core-memory manual mean by `Clear/Write` and `Memory Clear`? In particular, does `clear` name a separate Flash-like erase process, a selected-word overwrite step, or a broader electrical reset operation?

The answer matters for the repository's forgetting vocabulary. A nonvolatile state can survive loss of ordinary holding power yet still be deliberately reset by a powered operation; moreover, the historical word `clear` can refer to more than one **scope** of state change inside one product family.

---

## Source A — Computer Control Company TCM-32 manual, May 1964

**Document:** Computer Control Company, Inc. (3C), *Instruction Manual: Magnetic Core Memory Systems, Series TCM-32*, Document No. 71-218, May 1964.

**Preserved scan:** <https://bitsavers.org/pdf/computerControlCompany/71-218_3C_TCM-32_Core_Memory_Maint_May64.pdf>

**Evidence class:** `H/P` — manufacturer operating and maintenance manual for a named production core-memory system. Bitsavers is the preservation host, not the historical author.

This 1964 manual is deliberately used as a **later implementation/terminology witness**. It does not change Case 02's 1950–1954 MIT/Whirlwind anchor and is not evidence that Whirlwind used the same optional bulk-clear circuit.

---

## A1. Static retention does not require holding power

In §3-1.5, **Information Retention**, the manual states that the magnetic-core unit does not require power for its static memory capability: power is needed to switch cores between states, not to hold them there. It attributes the retained state to the retentivity of the magnetic material and says that, absent a severe transient, the core stack retains stored information after power removal.

The manual uses the word `indefinitely`. That wording is useful as a period product claim, but this addendum does **not** turn it into a measured universal retention duration for every ferrite core, array, environment, or machine.

**Historical boundary:** `power-off retention != immunity to a later switching/reset pulse`.

---

## A2. Ordinary writing assumes a selected address has first been cleared to ZERO

In §3-1.4, **Writing**, the manual says that before write half-currents are applied, all cores at the **selected address** have been cleared to the `ZERO` state. The write currents tend to switch the selected word's cores to `ONE`; inhibit currents prevent selected bit planes that should remain zero from making that transition.

This is not a separate block-erase geometry comparable to Flash. It is a state-setting phase inside the magnetic-memory write protocol:

```text
selected address
    -> force selected cores to ZERO reference state
    -> apply write currents
    -> inhibit bit planes that must stay ZERO
    -> new word remains in the selected address
```

**Historical record:** a production core-memory manual can use `clear` for the reference-state step that precedes writing a new selected word.

---

## A3. `Clear/Write` and `Read/Regenerate` have different continuation semantics

The manual's operating-cycle description makes the distinction explicit.

For **Clear/Write**, the selected storage location is first cleared of prior information and then the new information-register word is written into that location. The old stored word is not first transferred into the information register for preservation.

For **Read/Regenerate**, the existing word is read into the information register and then identical information is restored to the selected memory location.

The two operations can therefore share a core-switching substrate while having opposite relations to the old logical value:

```text
Clear/Write:
old word -> intentionally discarded at the selected address -> new word written

Read/Regenerate:
old word -> sensed/copied -> old word restored
```

**Grounded boundary:** `clear/write != destructive read followed by regeneration`, even though both can pass through a ZERO reference state.

---

## A4. The same system also exposes a whole-stack `Memory Clear` option

The manual separately lists **Memory Clear** as an option and describes it as clearing all information contained in the core stack with one operation.

The dedicated **Memory Clear Driver PAC, model S-103** section is even more explicit. The driver supplies clear current to the memory inhibit windings, and the manual states that this current **resets all cores to the ZERO state**.

This gives a scope contrast inside one named system:

```text
selected-address Clear/Write
    !=
whole-stack Memory Clear
```

Both are electrical state-setting operations. The latter is not described as demagnetizing the material into a neutral/non-state condition; it resets the array to the system's defined `ZERO` state.

**Grounded boundary:** `bulk memory clear != physical demagnetization`.

---

## A5. Bulk clear has its own operational recovery constraints

The S-103 section says a memory-clear pulse must not be applied during a normal memory cycle. After a clear pulse, no other system pulses should be applied for **200 microseconds** so the power supply can recover; the manual also limits the number of clear pulses in a 10-millisecond interval.

The exact numbers are product-specific. Their methodological value is more general but still bounded:

> an operation that forgets retained payload can itself impose a temporary power/service recovery obligation.

So `clear completed` and `memory ready for ordinary next-cycle service` need not be the same instant.

---

## Engineering reconstruction

### E1. Quiescent nonvolatility != reset immunity

The TCM-32 can make both claims in the same manual:

- the cores need no holding power for static retention;
- powered clear/write or Memory Clear currents can intentionally switch that retained state.

Therefore `nonvolatile` means neither `immutable` nor `cannot be deliberately forgotten electrically`.

### E2. `Clear` is typed by scope

One historical vocabulary item is insufficient without an operation scope:

```text
clear selected address
clear information register
clear address register
Memory Clear whole core stack
```

The repository should therefore ask **what state population is authorized to change** whenever a source uses `clear`, rather than importing one modern deletion/erase meaning.

### E3. Magnetic-core overwrite != Flash erase-before-write

There is a useful functional comparison and an important stop condition.

Both mechanisms can include a state-reset phase before a desired new value is established. But classic core switching is a reversible transition between remanent magnetic states at the selected word/bit population, whereas Flash erase changes floating-gate/charge state over an erase geometry and carries different programming asymmetry, endurance, and controller consequences.

Safe analogy: `rewrite may require a reference-state transition`.

Rejected identity: `TCM-32 Clear/Write = Flash erase-before-write`.

### E4. Bulk clear != evidence that the previous word remains as a separately addressable stale embodiment

Mapped Flash can leave obsolete physical pages after a logical update. The bounded TCM-32 clear evidence does not establish an equivalent shadow/stale copy. Once the selected cores have been switched to the reference state, ordinary core addressing does not reveal a second preserved embodiment of the prior word merely because the logical write was staged as clear-then-write.

This does not make claims about analog forensic remanence after magnetic switching; no such measurement is present in the manual.

---

## Historical / anti-overclaim boundaries

- The TCM-32 manual is a **1964 implementation witness**, not an invention-priority record for `clear`, `overwrite`, core reset, or bulk memory clearing.
- Its whole-stack Memory Clear option must not be projected backward onto the exact MIT Memory Test Computer / Whirlwind circuitry without separate evidence.
- `Clear/Write` is not a claim that every magnetic-core memory used the identical sequencing, word organization, current levels, or option set.
- The manual's `indefinitely` retention language is a manufacturer operational claim under a stated no-severe-transient condition, not a universal measured lifetime.
- Electrical reset to the ZERO state is not evidence of secure sanitization against every possible lower-level/analog recovery technique.

---

## Related-repository boundary

The broad historical mechanism, coincident-current selection, manufacturing labor, and system-level reasons core memory was attractive are already covered in [`tmzncty/computing-archaeology: Why Was Magnetic-Core Memory Worth Weaving by Hand?`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md).

This addendum keeps only the retention-specific distinction:

> **a quiescently nonvolatile core state can be deliberately replaced through a selected-address clear/write sequence or reset across the whole stack by a separate memory-clear operation; `clear` therefore needs both mechanism and scope before it can be compared with `overwrite`, `erase`, or `forgetting`.**

---

## Readiness assessment

This slice substantially improves Case 02's **write / clear / reset** semantics and partially advances the roadmap's magnetic overwrite / physical-reset vocabulary. It does **not** close magnetic-disk/tape overwrite, degaussing, analog remanence after switching, secure sanitization, or the broader genealogy of memory-clear operations.
'''

add_path = ROOT / 'evidence/02-1964-tcm32-clear-write-memory-clear-deepening.md'
if add_path.exists():
    raise SystemExit(f'{add_path} already exists')
write_text(add_path, addendum)

# Case 02 navigation.
replace_once(
    'cases/02-magnetic-core-destructive-read.md',
    'Grounding record: [`../evidence/02-magnetic-core-1951-1954-grounding.md`](../evidence/02-magnetic-core-1951-1954-grounding.md)',
    'Grounding record: [`../evidence/02-magnetic-core-1951-1954-grounding.md`](../evidence/02-magnetic-core-1951-1954-grounding.md)\n\nClear/write and bulk-reset semantics deepening: [`../evidence/02-1964-tcm32-clear-write-memory-clear-deepening.md`](../evidence/02-1964-tcm32-clear-write-memory-clear-deepening.md). The 1964 TCM-32 source is a later implementation/terminology witness, not a replacement for the case\'s 1950–1954 MIT anchor.'
)

case_marker = '''All can produce absence of the previous logical value, but they are technically different events.

---

## Time: two different retention intervals coexist'''
case_replacement = '''All can produce absence of the previous logical value, but they are technically different events.

### H/P deepening — `clear` can mean selected-word replacement or whole-stack reset

A later named production system makes the vocabulary more precise. Computer Control Company's May 1964 **TCM-32** manual describes `Clear/Write` as clearing all cores at the **selected address** to the `ZERO` state before writing the new information-register word. It separately offers a `Memory Clear` operation whose S-103 driver supplies clear current that resets **all cores** in the stack to `ZERO`.[^tcm32]

That evidence strengthens rather than reverses the statement above. Magnetic core still does not require a separate Flash-style erase block before ordinary rewriting. Instead, the TCM-32 shows a reversible reference-state transition used at two different scopes:

```text
selected address: clear to ZERO -> write new word
whole stack:      reset all cores to ZERO
```

The same manual distinguishes `Clear/Write` from `Read/Regenerate`: the former intentionally replaces the prior selected word, whereas the latter reads the prior word and restores identical information. The bulk clear also has its own service constraint: the manual requires a 200-microsecond power-supply recovery interval before other pulses after a clear command.[^tcm32]

Therefore:

- **quiescent nonvolatility ≠ immunity to explicit electrical reset**;
- **selected-address clear ≠ whole-stack clear**;
- **clear/write ≠ read/regenerate**;
- **core clear ≠ Flash erase ≠ secure sanitization**.

The TCM-32 is a 1964 implementation witness. It does not establish that the early MIT system used the same optional Memory Clear hardware, nor that 3C invented the operation.

---

## Time: two different retention intervals coexist'''
replace_once('cases/02-magnetic-core-destructive-read.md', case_marker, case_replacement)

# Add bounded engineering findings before interpretation.
eng_marker = '''---

## Philosophical / media-theoretical interpretation'''
eng_insert = '''### Finding 5 — nonvolatility is conditional on operation class

The TCM-32 deepening adds an explicit counterexample to `nonvolatile = difficult to reset`. Holding the remanent state requires no continuous power, while changing or clearing it deliberately requires a switching pulse. Persistence under absence of holding power and susceptibility to an authorized reset are independent properties.

### Finding 6 — forgetting operations need a scope as well as a mechanism

`Clear` is too coarse a comparative category by itself. The same 1964 product family exposes selected-address clear/write and whole-stack Memory Clear, with different state populations and continuation semantics. Cross-case comparison should therefore record at least:

```text
trigger / authority
+ target scope
+ physical state transition
+ whether old value is observed first
+ whether a replacement value follows
+ when ordinary service may resume
```

---

## Philosophical / media-theoretical interpretation'''
replace_once('cases/02-magnetic-core-destructive-read.md', eng_marker, eng_insert)

# Add source footnote if absent.
append_footnote_marker = '[^tcm32]:'
case_path = ROOT / 'cases/02-magnetic-core-destructive-read.md'
case_text = case_path.read_text(encoding='utf-8')
if append_footnote_marker in case_text:
    raise SystemExit('Case 02 already contains tcm32 footnote')
write_text(case_path, case_text.rstrip() + '\n\n[^tcm32]: Computer Control Company, Inc., *Instruction Manual: Magnetic Core Memory Systems, Series TCM-32*, Document No. 71-218, May 1964, especially §§3-1.4–3-1.5, Clear/Write operating-cycle description, Memory Clear option, and S-103 Memory Clear Driver PAC description; preserved scan: https://bitsavers.org/pdf/computerControlCompany/71-218_3C_TCM-32_Core_Memory_Maint_May64.pdf. Detailed claim decomposition is in the Case 02 deepening evidence record.')

# CASE_INDEX main row.
replace_line_prefix(
    'CASE_INDEX.md',
    '| [Magnetic Core Memory: Retention at Rest, Destruction in Reading]',
    '| [Magnetic Core Memory: Retention at Rest, Destruction in Reading](cases/02-magnetic-core-destructive-read.md) | **grounded** | remanence + destructive read / restore in the bounded classic scheme + later selected-word clear/write and bounded whole-stack electrical reset | separate idle nonvolatility from read invariance; show access itself can create a retention obligation; distinguish selected overwrite/reset scope from regeneration and from Flash-style erase | [1951–1954 grounding record](evidence/02-magnetic-core-1951-1954-grounding.md) + [1964 TCM-32 clear/write + Memory Clear deepening](evidence/02-1964-tcm32-clear-write-memory-clear-deepening.md); analog post-switch remanence, degaussing, secure sanitization, and broader clear/overwrite genealogy remain open |'
)

findings = r'''## Case 02 deepening — TCM-32 clear/write and whole-stack memory-clear findings

- **2451 — quiescent nonvolatility != immunity to explicit electrical reset.** The TCM-32 manual says holding core state requires no power, while switching/clearing it requires applied current; power-off survival and reset susceptibility are distinct properties. (`H/P`, `E`)
- **2452 — selected-address clear != whole-stack Memory Clear.** `Clear/Write` clears the selected word location to ZERO before writing new information, while the optional Memory Clear operation resets all cores in the stack. (`H/P`)
- **2453 — Clear/Write != Read/Regenerate.** In the named 1964 operating-cycle descriptions, Clear/Write intentionally discards prior selected-word information before replacement, whereas Read/Regenerate senses the old word and restores identical information. (`H/P`, `E`)
- **2454 — magnetic-core clear != Flash erase.** TCM-32 clear is an electrical transition to a defined remanent ZERO state; it does not establish Flash-style coarse erase geometry, charge-removal physics, erase-before-program asymmetry, or cycling wear. (`H/P`, `A`, `X`)
- **2455 — clear-to-reference-state + write-new can implement overwrite without a separately addressable stale embodiment.** The bounded core sequence does not itself establish an FTL-like old physical page that remains ordinarily addressable after logical replacement. (`H/P`, `E`, `X`)
- **2456 — whole-stack Memory Clear != demagnetization.** The S-103 manual text describes clear current as resetting all cores to the system's ZERO state, not removing magnetization into a neutral non-state. (`H/P`, `X`)
- **2457 — payload-reset completion != immediate ordinary-service readiness.** After a Memory Clear pulse, the TCM-32 manual requires a product-specific 200-microsecond no-pulse interval for power-supply recovery. (`H/P`, `E`)
- **2458 — one forgetting operation can create a maintenance/recovery obligation of its own.** The operation that destroys the old payload can temporarily consume power/service margin even though continued retention at rest needs no holding power. (`E`)
- **2459 — product-manual `indefinitely` != universal quantified ferrite retention law.** TCM-32 conditions its power-off statement on absence of a severe transient, and the manual does not establish a measured lifetime for all core materials/systems. (`H/P`, `X`)
- **2460 — `clear` requires target-scope qualification.** The same named system uses clear/reset vocabulary for registers, a selected memory address, and the whole core stack; one historical word is not one universal forgetting geometry. (`H/P`, `E`)
- **2461 — 1964 TCM-32 evidence != invention priority or retroactive Whirlwind circuit evidence.** The manual grounds a later production implementation/terminology boundary but not first invention, direct genealogy, or identical 1953 MIT bulk-clear hardware. (`H/P`, `X`)
- **2462 — related-repository boundary is reused rather than duplicated.** `computing-archaeology` already covers core selection, destructive read, manufacturing labor, and system tradeoffs; this addendum keeps only the retention-specific clear/overwrite/reset semantics. (`H/P` project-state record)'''
append_once('CASE_INDEX.md', '## Case 02 deepening — TCM-32 clear/write and whole-stack memory-clear findings', findings)

# ROADMAP Phase-2 navigation.
phase2_marker = '## Phase 2 — Build missing technical bridges\n'
phase2_entry = '''## Phase 2 — Build missing technical bridges

- [x] Case 02 magnetic-core clear/write and bulk-reset semantics deepening — [`cases/02-magnetic-core-destructive-read.md`](cases/02-magnetic-core-destructive-read.md), deepened by [`evidence/02-1964-tcm32-clear-write-memory-clear-deepening.md`](evidence/02-1964-tcm32-clear-write-memory-clear-deepening.md): the May-1964 Computer Control Company TCM-32 manual separates quiescent no-holding-power retention from explicit switching, selected-address `Clear/Write` from whole-stack `Memory Clear`, and old-value-discarding overwrite from `Read/Regenerate`. The S-103 clear driver resets all cores to the defined ZERO state and imposes a product-specific 200-microsecond power-supply recovery interval. This advances magnetic-core reset/overwrite vocabulary without treating core clear as Flash erase, secure sanitization, degaussing, or invention priority; broader magnetic overwrite/erase history remains open and belongs primarily in `computing-archaeology`.
'''
replace_once('ROADMAP.md', phase2_marker, phase2_entry)

replace_line_prefix(
    'ROADMAP.md',
    '- [ ] physical disturbance / reset of positional working state;',
    '- [ ] physical disturbance / reset of working state — **partially advanced at the magnetic-core electrical-reset layer by grounded Case 02 plus the 1964 TCM-32 deepening**: the named system can retain remanent state without holding power yet intentionally force a selected address or the entire core stack to the ZERO state. This grounds `quiescent retention != reset immunity` and `selected-word clear != whole-stack clear`. Passive positional/manual-state disturbance, accidental reset, magnetic-disk/tape degaussing, analog remanence after switching, and broader reset genealogy remain open;'
)

replace_line_prefix(
    'ROADMAP.md',
    '- [ ] overwrite — **partially advanced at the SSD/interface sanitization layer',
    '- [ ] overwrite — **partially advanced at the SSD/interface sanitization layer by grounded Cases 44 and 47 plus Synthesis 22, and now at the classic magnetic-core selected-word layer by Case 02**: NVMe separates Overwrite from Block Erase and Crypto Erase, FAST ’11 shows host-visible overwrite can miss stale FTL-managed embodiments, while the 1964 TCM-32 explicitly implements selected-address replacement as clear-to-ZERO followed by write-new. This magnetic-core sequence is not Flash erase and does not establish magnetic-disk/tape overwrite or analog-remanence closure. Filesystem/application overwrite under copy-on-write, snapshots, deduplication, replication, magnetic disk/tape overwrite, named contemporary device conformance, and broader overwrite genealogy remain open;'
)

# Remove one-shot integration scaffolding before validation/commit.
for rel in ['tools/tmp_case02_tcm32_clear.py', '.github/workflows/tmp-case02-tcm32-clear.yml']:
    p = ROOT / rel
    if p.exists():
        p.unlink()
