from pathlib import Path

EVIDENCE = r'''# Evidence 146B — Texas Instruments TMS29F040 Erase-Suspend Microstate and Power-Transition Boundary

## Scope

This note deepens Case 146 with one named-product counterexample to an overly strong reading of `erase resume`: the Texas Instruments TMS29F040 product contract preserves enough operation identity to resume a suspended sector erase while explicitly resetting one internal progress variable. The same document also gives a bounded power-transition rule: below the low-VCC lockout threshold, command input is disabled and the device is reset to read mode.

The narrow research question is:

> Does `resume the suspended erase` require preservation of every internal progress variable, and does the suspended operation-control state survive a power-down transition?

The answer for this named product is **no** to both strong forms. This does not establish a universal NOR-Flash rule.

---

## Source identity and provenance

### Texas Instruments TMS29F040, SMJS820C

- **Document:** *TMS29F040 — 524288 by 8-Bit Flash Memory*
- **Literature number / revision:** `SMJS820C`
- **Date printed in document:** April 1996, revised June 1998
- **Manufacturer:** Texas Instruments
- **Document status:** `PRODUCTION DATA`
- **Pages used:** 1, 9–11 of the printed document
- **Accessible archival copies:** [Octopart-hosted PDF](https://datasheet.octopart.com/TMS29F04070C5FML-Texas-Instruments-datasheet-114606.pdf); [AllDatasheet page-level mirror](https://www.alldatasheet.com/datasheet-pdf/pdf/204198/TI/TMS29F040.html)
- **Evidence class:** `H/P*` — manufacturer-primary document preserved on third-party datasheet archives, not a current TI origin-hosted copy.

The PDF identifies a 4-Mbit, 5-V device divided into eight 64-Kbyte sectors, with an on-chip state machine controlling automatic byte-program and sector/chip-erase functions. Its feature list includes `Erase-Suspend/Erase-Resume Operation`.

No first-vendor or invention-priority claim is made from this document. The revision is later than the Intel patent line and the November-1996 AMD product witness already used by Case 146.

---

## Historical record

### H/P* — suspend is a state-machine transition, not an instantaneous analog freeze

On printed page 9, TI states that the `B0h` erase-suspend command requests the internal write-state machine to halt at **predetermined breakpoints**. The device typically takes 0.1–15 µs to enter the suspended state. Completion of the suspend transition is observed through the toggle bit; after the toggle stops, sectors not selected for erase can be read, while reading a selected erase sector can return invalid data.

This independently reinforces an existing Case-146 boundary:

```text
host suspend request != device has reached the suspended state
```

It also prevents an undocumented model in which arbitrary high-voltage activity is assumed to freeze at an exact transistor-level instant.

### H/P* — resume preserves operation identity while one internal counter is reset

The same page says that `30h` restarts the suspended sector-erase operation and describes it as continuing the suspended erase from where it was halted toward completion.

Crucially, the immediately following sentence states that when an erase-suspend / erase-resume combination is written:

- the **internal pulse counter is reset to zero**; and
- the exceed-timing-limit indicator `DQ5` is cleared to logic low.

Printed page 10 separately defines the role of this counter: program and erase operations use an internal pulse counter to limit the number of pulses; exceeding the limit sets `DQ5` and indicates operation failure.

The product contract therefore directly supplies a counterexample to:

```text
resume same operation => every internal progress variable preserved unchanged
```

The document itself combines two statements that must be read together:

```text
same suspended sector erase is resumed
+
internal erase/program pulse-count state is reinitialized
```

### H/P* — low-VCC transition resets command/control mode to read mode

Printed page 11, under `low VCC write lockout`, says that during power-up and power-down, write operations are locked out below `VLKO`; when `VCC < VLKO`, command input is disabled and **the device is reset to read mode**. It also states that the device automatically powers up in read mode.

For this named product, that is affirmative evidence against treating suspended erase control state as a crash-persistent checkpoint:

```text
powered suspend/resume context
    -- VCC below VLKO -->
read-mode control state
```

The datasheet does **not** specify a transaction-like restart of the pre-power-loss suspended erase after power returns.

This does not, by itself, specify the exact cell-level condition of a sector whose erase was interrupted by loss of power. `read mode after power-up` is a command/control-state statement, not proof of rollback, completion, or uniform erased data.

---

## Engineering reconstruction

### Operation identity and micro-progress are separable state

A stronger decomposition than the original interface-only shorthand is useful:

```text
S = (O, M, P, H)

O = outstanding erase obligation / target relation
M = current command-state-machine mode
P = implementation-specific progress variables
H = host-visible status/admission state
```

For the bounded TI product, the documentation supports:

```text
active erase
  -> suspend reaches a permitted breakpoint
  -> O remains resumable
  -> resume returns to sector erase
  -> at least one P component (internal pulse counter) = 0
```

Thus the retained state across suspend need only be **sufficient for continuation**, not an identity mapping over all pre-suspend controller state.

A useful formulation is:

```text
continuation identity != microstate identity
```

or, more formally:

```text
resume( project_keep(S_before_suspend), reinitialized_progress )
```

where `project_keep` is an engineering abstraction, not a claim about the exact hidden register layout of the TMS29F040.

### `from where halted` is an interface/operation statement

TI's wording that erase resumes from where it was halted cannot safely be expanded into `all counters, pulse history, voltages, and analog conditions are restored exactly`. The same paragraph explicitly falsifies that expansion for the internal pulse counter.

The strongest supported interpretation is:

> the pending sector-erase **operation** continues from its suspended workflow state, while at least one internal progress/safety counter is deliberately reinitialized.

### Power transition changes the retention horizon

The same chip therefore exposes two different horizons:

1. **powered suspend horizon:** enough state survives the suspend interval for `30h` to continue the pending erase;
2. **low-VCC / power-cycle horizon:** the command/state-machine contract returns to read mode rather than promising suspended-operation continuation.

This is a named-device instance of:

```text
payload nonvolatility != pending-operation-control nonvolatility
```

and also:

```text
state can be retained across one transition but retired across another
```

---

## Functional comparisons — explicitly non-genealogical

### Case 45 — DDR5 maintenance-control-state horizons

Case 45 shows that one device transition can preserve some maintenance/diagnostic state while resetting other state. TMS29F040 supplies a different substrate-level example: sector-erase operation identity remains resumable across a powered suspend while an internal pulse counter is reset.

The comparison is functional only. It does not imply shared circuitry, standards lineage, or historical influence between 1990s NOR Flash and DDR5 ECS.

### Case 138 — Redis AOF rewrite

Case 138 separates a continuing maintenance obligation from local execution/admission state. Case 146B is a hardware-level analogue in one narrow sense: unfinished work can remain the same outstanding operation even though some execution-progress state is reinitialized.

Again, this is not genealogy and does not equate a Flash state machine with a software rewrite job.

---

## Rejected upgrades / limits

### X — no invention-priority claim

The June-1998 revision of SMJS820C is a named-product evidence point, not evidence that TI invented erase suspend, pulse-counter reset on resume, or any broader interruptible-maintenance mechanism.

### X — no universal NOR-Flash rule

The TMS29F040 behavior cannot be projected onto Intel, AMD, Macronix, later NAND, managed SSDs, or even every TMS29 family revision without product-specific evidence.

### X — no exact hidden microarchitecture claim

The document names an internal pulse counter and a state machine but does not expose a complete register-transfer implementation. `O`, `M`, `P`, `H`, and `project_keep` are engineering reconstruction terms.

### X — no rollback/completion claim after power loss

Resetting to read mode below `VLKO` does not establish that an interrupted target sector returns to its pre-erase payload, finishes erasing, becomes uniformly `0xFF`, or remains safely reusable. The cell-level result requires separate evidence or experiment.

### X — no sanitization inference

Neither successful erase, suspended erase, power loss, nor return to read mode establishes secure sanitization or forensic non-recoverability.

---

## What this closes and what remains open

This deepening closes two bounded ambiguities in Case 146:

1. **exact-progress ambiguity:** a named product directly shows that resume of the same pending erase can coexist with reset of an internal pulse counter;
2. **named-product control-state power boundary:** the same product explicitly resets command/control mode to read mode below its low-VCC lockout threshold rather than promising resume of suspended erase after power return.

Still open:

- exact cell-level outcome of power removal at different points in TMS29F040 erase;
- reset-command behavior in every intermediate erase/suspend timing window beyond the documented command rules;
- independent hardware fault/power-cut validation;
- exact Intel shipping-product tie and early command-set genealogy;
- cross-vendor comparison of which progress variables survive suspend;
- later NAND/managed-Flash suspend, abort, recovery, and controller policy.

Broad NOR-Flash command-set and product genealogy should remain primarily in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology); a fresh repository search found no dedicated TMS29F040 / erase-suspend study to reuse.
'''


def replace_once(path: str, old: str, new: str):
    p = Path(path)
    text = p.read_text()
    if old not in text:
        raise SystemExit(f"anchor not found in {path}: {old[:100]!r}")
    if text.count(old) != 1:
        raise SystemExit(f"anchor not unique in {path}: {text.count(old)}")
    p.write_text(text.replace(old, new, 1))


def main():
    ev = Path('evidence/146-ti-tms29f040-erase-suspend-microstate-power-deepening.md')
    if ev.exists():
        raise SystemExit('evidence file already exists')
    ev.write_text(EVIDENCE)

    case = 'cases/146-flash-erase-suspend-pending-operation-state.md'
    replace_once(
        case,
        '**`grounded`** — bounded to the public 1991-priority/1994-published Intel erase-suspend patent line, AMD\'s November-1996 Am29F040 product contract, and later 1996-priority/1998-public refinements used only to expose checkpoint and capability boundaries.',
        '**`grounded`** — bounded to the public 1991-priority/1994-published Intel erase-suspend patent line, AMD\'s November-1996 Am29F040 product contract, Texas Instruments\' 1998 TMS29F040 named-product microstate/power-transition contract, and later 1996-priority/1998-public refinements used only to expose checkpoint and capability boundaries.'
    )
    replace_once(
        case,
        'Grounding record: [`../evidence/146-intel-amd-1991-1998-flash-erase-suspend-grounding.md`](../evidence/146-intel-amd-1991-1998-flash-erase-suspend-grounding.md).',
        'Grounding records: [`../evidence/146-intel-amd-1991-1998-flash-erase-suspend-grounding.md`](../evidence/146-intel-amd-1991-1998-flash-erase-suspend-grounding.md) + [`../evidence/146-ti-tms29f040-erase-suspend-microstate-power-deepening.md`](../evidence/146-ti-tms29f040-erase-suspend-microstate-power-deepening.md).'
    )

    ti_section = r'''### Texas Instruments TMS29F040: same pending erase, reset internal pulse counter

Texas Instruments' TMS29F040 production datasheet `SMJS820C` (April 1996, revised June 1998) supplies a named-product counterexample to an overly strong interpretation of Resume.

The device asks its internal write-state machine to halt a sector erase at **predetermined breakpoints**. Once suspended, unaffected sectors can be read. The Resume command then restarts the suspended sector-erase operation and describes it as continuing from where it was halted.

But the same Resume paragraph explicitly says that an erase-suspend / erase-resume combination **resets the internal pulse counter to zero** and clears `DQ5`. The status section identifies that counter as the limit on program/erase pulses and uses `DQ5` to report an exceeded timing/pulse limit.

Therefore the product directly grounds:

```text
same pending erase obligation
    !=
bit-for-bit preservation of every internal progress variable
```

`from where it was halted` is safely read as operation/workflow continuation, not as a promise that every pulse-level controller coordinate remains unchanged.

The same TI datasheet also documents a power-transition boundary. Below its low-VCC write-lockout threshold, command input is disabled and the device is reset to read mode; power-up also enters read mode. That provides named-product evidence that the powered suspend/resume control relation is not specified as a power-cycle-persistent checkpoint. It does **not** establish the exact cell-level condition of a sector whose erase was interrupted by power loss.

Detailed source treatment: [`../evidence/146-ti-tms29f040-erase-suspend-microstate-power-deepening.md`](../evidence/146-ti-tms29f040-erase-suspend-microstate-power-deepening.md).

'''
    replace_once(case, '### Later Macronix evidence exposes checkpoint semantics', ti_section + '### Later Macronix evidence exposes checkpoint semantics')

    old_limits = '''The sources do not establish one universal internal representation such as a durable program counter or exact analog-progress checkpoint. They also do not prove persistence across:\n\n- power failure;\n- reset;\n- device removal;\n- brownout;\n- controller replacement.\n\nSo the case grounds **powered operation-state retention**, not a crash-persistent transaction checkpoint.'''
    new_limits = '''The sources do not establish one universal internal representation such as a durable program counter or exact analog-progress checkpoint. The TI TMS29F040 in fact supplies a direct counterexample to exact-microstate preservation: its Resume path preserves the pending sector-erase relation while resetting the internal pulse counter to zero.\n\nThe same TI product also resets command/control state to read mode below its low-VCC lockout threshold and on power-up. That is affirmative named-product evidence against treating its suspended erase as a crash-persistent transaction checkpoint. The exact cell-level condition of a power-interrupted target sector remains unspecified here, and the TI rule must not be projected onto every Intel/AMD/Macronix/later-NAND implementation.\n\nSo the case grounds **powered operation-state retention with transition-specific state projection**, not universal preservation of controller microstate and not crash-persistent transaction recovery.'''
    replace_once(case, old_limits, new_limits)

    compare_anchor = '''### Case 15 — SSD power-loss protection\n\nBoth cases distinguish payload nonvolatility from volatile control/maintenance state, but Case 15 has explicit failure-triggered energy/durability concerns. Case 146 has **no evidence** that suspended erase state survives power loss. Suspend must therefore not be analogized to durable SSD transaction recovery.'''
    compare_new = '''### Case 45 — DDR5 maintenance-control-state horizons\n\nCase 45 shows that one device transition can preserve some maintenance/diagnostic state while resetting other control state. The TMS29F040 supplies a different functional instance: the pending erase remains resumable across powered Suspend/Resume even though an internal pulse counter is reinitialized. This is a bounded analogy, not circuitry or genealogy.\n\n### Case 15 — SSD power-loss protection\n\nBoth cases distinguish payload nonvolatility from volatile control/maintenance state, but Case 15 has explicit failure-triggered energy/durability concerns. Case 146's TI deepening instead documents a low-VCC reset to read mode and does **not** establish suspended-erase continuation across power loss. Suspend must therefore not be analogized to durable SSD transaction recovery.'''
    replace_once(case, compare_anchor, compare_new)

    roadmap = 'ROADMAP.md'
    roadmap_anchor = '## Phase 2 — Build missing technical bridges\n\n'
    roadmap_entry = '''- [x] **Case 146 TI TMS29F040 erase-suspend microstate / power-transition deepening:** [`cases/146-flash-erase-suspend-pending-operation-state.md`](cases/146-flash-erase-suspend-pending-operation-state.md) + [`evidence/146-ti-tms29f040-erase-suspend-microstate-power-deepening.md`](evidence/146-ti-tms29f040-erase-suspend-microstate-power-deepening.md) add a June-1998 Texas Instruments production-data contract in which Resume continues the same suspended sector erase while the internal pulse counter is explicitly reset to zero. The same document says low VCC disables command input and resets the part to read mode, closing the bounded `operation continuation != exact microstate preservation` and named-product `powered suspend state != power-cycle-persistent checkpoint` seams. Exact cell-level outcome after power interruption, hardware power-cut validation, cross-vendor progress-state comparison, exact Intel shipping-product tie, and early genealogy remain open; broad NOR-Flash command-set history belongs primarily in `computing-archaeology`.\n\n'''
    replace_once(roadmap, roadmap_anchor, roadmap_anchor + roadmap_entry)

    idx = Path('CASE_INDEX.md')
    text = idx.read_text()
    old_row = '''| [Flash Erase Suspend/Resume: Pending Erasure, Read Availability, and Operation-State Retention](cases/146-flash-erase-suspend-pending-operation-state.md) | **grounded** | sector/block erase + suspend/resume control state + status/admission mode + temporary non-target access | separate pending transformation from completion/abort; distinguish host suspend request from admitted suspended state; other-sector serviceability from target-sector payload authority; operation identity from exact microstate persistence | [1991–1998 grounding](evidence/146-intel-amd-1991-1998-flash-erase-suspend-grounding.md); exact Intel product tie, full early genealogy, reset/power-loss behavior, simultaneous-read/write evolution, silicon validation, and later NAND policy remain open |'''
    new_row = '''| [Flash Erase Suspend/Resume: Pending Erasure, Read Availability, and Operation-State Retention](cases/146-flash-erase-suspend-pending-operation-state.md) | **grounded** | sector/block erase + suspend/resume control state + status/admission mode + temporary non-target access | separate pending transformation from completion/abort; distinguish host suspend request from admitted suspended state; other-sector serviceability from target-sector payload authority; operation identity from exact microstate persistence | [1991–1998 grounding](evidence/146-intel-amd-1991-1998-flash-erase-suspend-grounding.md) + [TI TMS29F040 microstate/power-transition deepening](evidence/146-ti-tms29f040-erase-suspend-microstate-power-deepening.md); exact Intel product tie, full early genealogy, cell-level power-interruption outcome, simultaneous-read/write evolution, silicon validation, cross-vendor progress-state comparison, and later NAND policy remain open |'''
    if old_row not in text:
        raise SystemExit('CASE_INDEX Case146 row anchor not found')
    text = text.replace(old_row, new_row, 1)
    if '**3747 — X**' not in text or '**3748 —' in text:
        raise SystemExit('unexpected CASE_INDEX finding tail')
    findings = r'''

### Findings 3748–3763 — Case 146 TI TMS29F040 suspend/resume microstate and power-transition boundary

- **3748 — H/P*** — Texas Instruments `SMJS820C`, April-1996 / revised-June-1998 production data, identifies the TMS29F040 as an eight-sector 4-Mbit Flash device with automated on-chip program/erase and an advertised Erase-Suspend/Erase-Resume operation.
- **3749 — H/P*** — The TMS29F040 Erase Suspend command asks the internal write-state machine to halt sector erase at predetermined breakpoints rather than promising instantaneous suspension at an arbitrary analog instant.
- **3750 — H/P*** — TI gives a typical 0.1–15 µs suspend-entry interval and requires Toggle Bit observation to determine that suspension has actually taken effect, reinforcing `request != admitted suspended state`.
- **3751 — H/P*** — Once suspension is established, sectors not selected for erase can be read, while reads from a selected erase sector can return invalid data; temporary serviceability is address- and operation-state-qualified.
- **3752 — H/P*** — TI documents `30h` as restarting the suspended sector-erase operation and describes the same pending erase as continuing from where it was halted toward completion.
- **3753 — H/P*** — In that same Resume path, TI explicitly resets the internal pulse counter to zero and clears the DQ5 exceed-timing-limit indicator.
- **3754 — H/P*** — The status section defines the internal pulse counter as limiting applied program/erase pulses and DQ5 as the failure indication when the pulse-count limit is exceeded, making the reset a substantive progress/safety-state reinitialization rather than an unlabeled status cosmetic.
- **3755 — H/P*** — Under low-VCC write lockout, `VCC < VLKO` disables command input and resets the TMS29F040 to read mode; the product also automatically powers up in read mode.
- **3756 — E** — `same pending operation != identical internal microstate`: the named product preserves enough relation for the suspended sector erase to resume while at least one internal progress variable is deliberately reinitialized.
- **3757 — E** — TI's `from where it was halted` wording is therefore safely interpreted at operation/workflow level; it cannot support a stronger claim that every counter, pulse-history coordinate, voltage condition, or analog state is restored exactly.
- **3758 — E** — Case 146 should model suspend retention as a projection sufficient for continuation rather than identity preservation over all controller state: operation/target relation may remain while implementation-specific progress state changes.
- **3759 — E** — The TI part has distinct transition horizons: powered Suspend/Resume preserves resumability, whereas low-VCC transition retires that command/control mode into read mode rather than promising crash-persistent continuation.
- **3760 — E** — `power-up read mode != rollback != erase completion`: the control-mode rule does not establish the exact post-interruption cell state of the sector that had been undergoing erase.
- **3761 — A/E** — Case 45 is a bounded functional comparison because both cases show transition-relative maintenance-control-state horizons; it does not establish shared circuitry, standard lineage, or historical influence between DDR5 ECS and NOR Flash.
- **3762 — X** — The 1998 TI production-data witness does not establish invention priority, a universal NOR-Flash suspend implementation, exact hidden register layout, or behavior of Intel/AMD/Macronix/later-NAND devices.
- **3763 — X** — Suspend, Resume, low-VCC reset to read mode, or even successful sector erase do not by themselves establish secure sanitization, forensic non-recoverability, or a known uniform cell state after an interrupted erase.
'''
    idx.write_text(text.rstrip() + findings + '\n')

    # Minimal sanity checks.
    assert ev.exists()
    assert '3748–3763' in idx.read_text()
    assert 'TI TMS29F040' in Path(roadmap).read_text()
    assert 'internal pulse counter to zero' in Path(case).read_text()


if __name__ == '__main__':
    main()
