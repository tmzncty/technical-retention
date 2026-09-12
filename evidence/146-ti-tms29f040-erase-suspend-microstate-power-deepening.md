# Evidence 146B — Texas Instruments TMS29F040 Erase-Suspend Microstate and Power-Transition Boundary

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
