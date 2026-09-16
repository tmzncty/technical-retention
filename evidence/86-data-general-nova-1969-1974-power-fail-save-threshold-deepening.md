# Case 86 deepening — Data General NOVA power-fail warning, core-resident save, and restart-threshold semantics (1969–1974)

**Status:** `bounded deepening complete`

**Canonical case:** [`../cases/86-dec-pdp8-core-power-fail-auto-restart.md`](../cases/86-dec-pdp8-core-power-fail-auto-restart.md)

## Research question

Case 86 is centered on DEC's PDP-8 KR01 / KP8-family power-fail and automatic-restart path. This slice asks a narrower cross-vendor question:

> Did another late-1960s / early-1970s core-memory minicomputer also distinguish an early power-failure warning, a bounded interval for moving volatile processor state into core, a later hard-stop/reset boundary, and a separately controlled restart entry?

Data General's NOVA documentation answers **yes**, but the result must remain a bounded historical comparison rather than a genealogy claim.

The useful retention problem is not simply `core memory survives power loss`. It is the layered transition:

```text
core payload can remain
        !=
volatile processor context remains
        !=
software has time to migrate context
        !=
hardware still authorizes ordinary execution
        !=
automatic restart is enabled
        !=
restored execution context is already reconstructed
```

## Scope

This evidence record uses three Data General primary-document layers:

1. the archived **1969 NOVA Maintenance Manual**, which already documents the optional power monitor, separate Power Failure / restart behavior, and a 1–2 ms warning-to-stop interval;
2. **How To Use The Nova Computers**, Ordering No. `015-000009`, Rev. 09, October 1974, which gives the programmer-visible save/restart contract across the NOVA line;
3. the **NOVA 2 Technical Manual**, Ordering No. `015-000026`, Rev. 01, November 1974, which exposes processor-level `PWR FAIL` / `MEM OK` sequencing and power-supply threshold signals for the NOVA 2.

This slice does **not** attempt a general Data General history, a NOVA power-supply genealogy, or a circuit-by-circuit comparison with DEC. Broader minicomputer and magnetic-core engineering remains primarily the responsibility of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). A repository search there for `Nova power fail` found no dedicated treatment to reuse in this slice.

---

## Source custody and inspection boundary

The Data General manuals are preserved as scanned primary PDFs on Bitsavers. In this research environment, the host allowed indexed text retrieval but rejected page screenshots with HTTP 403 for the NOVA 2 PDF. The October-1974 system-reference text was independently recoverable through a Computer History Museum scan and a searchable manual extraction.

Accordingly:

- claims from the October-1974 system reference are treated as **H/P — strong primary**, because exact manufacturer text is independently exposed through more than one preserved copy;
- claims from the 1969 maintenance manual and November-1974 NOVA 2 Technical Manual are marked **H/P\*** where page-render verification remains pending, even though the indexed text comes from the manufacturer-primary scans;
- no claim below treats OCR spelling or punctuation as authoritative when the technical meaning is otherwise clear;
- page/section anchors such as `2-13`, `2-40`, `C-8`, and `P-7` refer to the printed/manual section numbering exposed by the preserved text.

This source-custody label is a research-process boundary, not a judgment that indexed primary text is equivalent to a secondary source.

---

## Historical record

### H/P* — the 1969 NOVA Maintenance Manual already documents an early-warning / later-stop sequence

The archived 1969 NOVA maintenance manual's processor-options discussion says that the optional power monitor is shown in drawing 11. An incipient failure in the main supply output sets the **Power Failure** flag; **1 to 2 ms later `RUN` clears**. After adequate levels return in both memory and logic power, a one-shot sets `RESTART` if the console key is in the locked position.

The bounded historical sequence is therefore already present in the 1969 manufacturer documentation:

```text
main-supply failure begins
    -> Power Failure flag set
    -> approximately 1–2 ms remains
    -> RUN clears

adequate memory + logic power return
    -> restart one-shot may set RESTART
       if console key is locked
```

This is stronger than simply finding the words `power fail` in a later manual. It shows that the NOVA option was documented as a staged transition in the machine's maintenance literature by 1969.

It does **not** establish the exact publication month of the preserved scan, first shipment of the option, invention priority, or identity with the later NOVA 2 circuitry.

### H/P — October 1974: power-on preserves core while processor registers begin indeterminate

*How To Use The Nova Computers*, Rev. 09, states in its `Power Monitor and Auto Restart` section that when AC power is applied to the central processor:

- **core memory is unaltered**;
- the initial states of the PC, accumulators, and flags are **indeterminate**;
- the processor is halted.

That one paragraph supplies a particularly clean state-class boundary:

```text
surviving core contents
    !=
known processor execution state after power return
```

The manual therefore does not let `nonvolatile core` stand in for `whole processor state survived`.

### H/P — October 1974: the power-fail interrupt provides a minimum 1–2 ms software window

The same section says that if chassis AC power fails, there is a **minimum delay of 1 to 2 milliseconds after the power-fail interrupt before the processor shuts down**.

Data General also says the processor **always completes a memory cycle** and sequences power off so that memory contents are unaffected.

Two obligations must therefore be kept separate:

```text
finish the in-flight memory-cycle relation
    !=
use the remaining processor interval to save volatile execution state
```

The first protects the current core-memory operation from being abandoned arbitrarily. The second is a software continuation obligation.

Neither number is a ferrite shelf-retention interval.

### H/P — the optional power monitor requests an interrupt, but software must recognize it first

The power monitor sets the **Power Failure** flag and automatically requests an interrupt. Data General explicitly notes that the monitor does not respond to the ordinary `INTA` identification path, so a program on a machine with the option should test the Power Failure flag **before** giving `INTA` or testing other devices.

The logic is the same kind of finite-window scheduling problem Case 86 already sees in DEC, but this is an independent Data General historical witness:

```text
failure warning arrives
    -> interrupt requested
    -> software must classify power failure promptly
    -> save path runs while reliable execution time remains
```

The similarity does not prove DEC-to-Data-General transfer, common circuitry, or common software.

### H/P — the save contract names what software must move into core

The October-1974 manual says that on power failure the program should:

- save the accumulators and **Carry** in memory;
- save **location 0** so the interrupted program's PC can later be restored properly;
- put a `JMP` to the desired restart location in location 0;
- then `HALT`.

This gives a useful historical decomposition:

```text
ordinary program/data already in core
+
accumulators + Carry copied to core
+
old location-0 / interrupted-PC relation retained somewhere
+
new location-0 restart transfer
```

Location 0 is not a complete checkpoint image. It is part of the NOVA interrupt/restart linkage: the processor's interrupt machinery uses location 0 in handling PC state, and the power-fail routine temporarily repurposes the location to make the later restart path possible.

### H/P — restart authority depends on the console power-switch position

The same manual says the action after adequate power returns depends on the operator-console power switch:

- with the switch in **ON**, power returns with the machine stopped;
- with the switch in **LOCK**, the processor later executes `JMP 0` and resumes normal instruction sequencing from location 0.

Thus:

```text
core state survived
    !=
automatic restart is authorized
```

The operator-console setting is a policy/control condition around the retained core state. It does not change the magnetic remanence mechanism.

### H/P* — NOVA 2 processor logic distinguishes `PWR FAIL` from later `MEM OK` loss

The November-1974 *NOVA 2 Technical Manual*, processor section `C-8`, says the processor always monitors `MEM OK` from the power-fail module. When `MEM OK` goes low, `HLT PND` and `HRST` are set; the manual characterizes this as equivalent to a console RESET, including an `IORST` pulse to devices.

With the Power Monitor and Auto Restart option installed, the processor also monitors `PWR FAIL`. The manual states that on failure **`PWR FAIL` is the first to go low, approximately 1 to 2 ms before `MEM OK`**. That assertion sets the `PWR LOW` flag and causes an interrupt request.

This is a direct hardware/processor witness for an ordered transition frontier:

```text
PWR FAIL
    -> early warning / software interrupt opportunity

~1–2 ms later

MEM OK low
    -> halt/reset boundary
```

The project term `warning frontier` is an engineering reconstruction; Data General's period signal names are `PWR FAIL`, `PWR LOW`, and `MEM OK`.

### H/P* — NOVA 2 restart occurs only after power signals recover, with a documented short delay

The same `C-8` section says that after `MEM OK` and `PWR FAIL` are both high again, the NOVA 2 begins a **2 ms delay**. If the console power switch is ON, no further action occurs. If the switch is LOCK, the processor performs `RESTART`, causing a direct jump to location 0.

So the NOVA 2 manual separates:

```text
power signals recovered
    !=
immediate execution
    !=
automatic restart necessarily enabled
```

### H/P — the general October-1974 manual and the NOVA 2 technical manual publish different restart delays

The broader *How To Use The Nova Computers* reference says that in LOCK position the processor executes `JMP 0` **50 ms after power comes back on**.

The model-specific NOVA 2 technical manual says its restart sequence waits **2 ms after `MEM OK` and `PWR FAIL` have both gone high**.

These numbers should **not** be merged into one `NOVA restart delay`.

The sources differ in scope and time origin:

- one is a programming/system-reference manual covering multiple NOVA-line machines;
- the other is a NOVA 2 hardware technical manual;
- `power comes back on` is not textually demonstrated to be the same measurement origin as `MEM OK and PWR FAIL have both gone high`.

Without a revision/model genealogy, the correct historical conclusion is simply:

> restart delay is model/document specific in the surviving evidence.

This is a useful source-control result rather than an inconsistency to paper over.

### H/P* — the NOVA 2 power-fail module exposes multiple analog status thresholds

The NOVA 2 power-supply section, `Power Fail Module` / printed `P-7`, says the module monitors both the +5 V DC output and the non-regulated bridge-rectifier output (`+30VNR`). It exposes three status signals: `PWR FAIL`, `PWR OK`, and `+5V OK`.

The manual says:

- `PWR FAIL` is asserted when the bridge output falls to **+24 V**;
- `PWR OK` clears when the +5 V DC line falls below **+4.7 V**;
- `+5V OK` clears later as the +5 V line continues to fall;
- on power-up, `+5V OK` returns as the +5 V line approaches normal, and `PWR OK` is asserted / `PWR FAIL` cleared when +5 V reaches +4.7 V.

This grounds a staged power-validity apparatus rather than one undifferentiated `power is on/off` bit.

However, the current inspected text does **not** explicitly map the processor's `MEM OK` signal one-to-one onto `PWR OK` or `+5V OK`. This record therefore refuses the shortcut:

```text
MEM OK = PWR OK = +5V OK
```

unless a schematic or explicit signal mapping is later inspected.

### H/P* — the analog threshold belongs to transition control, not magnetic retention physics

The +24 V and +4.7 V figures are thresholds in the NOVA 2 power-fail/control apparatus. They do not measure core coercivity, remanent decay, or a magnetic retention lifetime.

Their role is to decide when the machine still has time to react and when logic/memory operation is no longer considered safe enough for ordinary execution.

So:

```text
power-fail sensing threshold
    !=
core-retention threshold
```

is a source-bounded engineering distinction.

---

## Engineering reconstruction

### E — retention across a power fault has at least three different frontiers

The NOVA evidence supports a useful decomposition:

```text
material-retention frontier
    core words can remain magnetized across primary-power loss

warning frontier
    PWR FAIL / Power Failure gives software a bounded interval

execution-admissibility frontier
    MEM OK loss / RUN clear ends ordinary reliable execution
```

The system succeeds only if state that exists solely in the volatile execution regime is transferred before the warning-to-stop interval closes.

This is project vocabulary, not Data General terminology.

### E — completing a memory cycle and saving CPU context are different retention acts

Data General says the machine completes the current memory cycle before shutdown so core contents are unaffected. Separately, the power-fail routine must save accumulators/Carry and preserve the interrupted-PC relation.

Therefore:

```text
in-flight core operation completed safely
    !=
volatile processor context captured
```

A system can satisfy the first and still fail the second.

### E — the warning interval is a temporal transfer resource

The 1–2 ms interval is not itself a retained state. It is a **time budget** in which software can move information from powered processor registers into the more power-loss-tolerant core substrate.

This parallels the later DEC KP8-E evidence at a relation level, but the exact energy-storage circuitry must remain machine-specific.

### E — restart entry is an address relation, not restored execution state

`JMP 0` gives the restarted processor a known path into recovery. The old accumulator/Carry/PC-related state still has to be restored by software.

Thus:

```text
restart entry available
    !=
interrupted computation already reconstructed
```

### E — restart authorization can be orthogonal to retained-state survival

The ON/LOCK distinction shows that automatic resumption is a controllable policy even after core contents survive and power returns.

This is weaker than GE-PAC's time-bounded process-safety timer, but it establishes the same abstract separation:

```text
recoverable retained context
    !=
automatic continuation authorized
```

The historical mechanisms are not identical.

### E — staged analog sensing converts a continuous electrical decline into discrete software/control obligations

The NOVA 2 power supply observes changing voltages, but the processor sees named logical conditions such as `PWR FAIL` and `MEM OK`.

At the engineering level:

```text
continuous supply decline
    -> comparator / status transition
    -> interrupt opportunity
    -> later reset/halt boundary
```

This is not a philosophical claim that all technical thresholds are `memory`. It is a concrete case in which a retention protocol depends on transforming an analog transition into ordered control events.

### E — one historical product family can carry more than one restart-delay contract

The 50 ms system-reference statement and the 2 ms NOVA 2 hardware statement warn against flattening product-family documentation.

A cross-machine comparison should retain at least:

```text
machine/model
+ document revision
+ signal/event used as timing origin
+ automatic-restart policy state
+ measured/published delay
```

rather than extracting one decontextualized number.

---

## Cross-vendor comparison with DEC Case 86

### Functional analogy only

Data General NOVA and DEC PDP-8 expose a strikingly similar bounded architecture:

```text
impending power loss detected
    -> interrupt
    -> short continued-execution interval
    -> software moves volatile CPU context into core
    -> processor stops / resets
    -> power later becomes acceptable
    -> known restart entry in core
    -> software reconstructs execution context
```

That is enough for a **functional analogy** and a cross-vendor historical comparison.

It is **not** enough for:

- a claim that Data General copied DEC's KR01;
- a claim that both companies used the same comparator or hold-up circuit;
- a claim that the same registers were saved;
- a claim that their timing constants were interchangeable;
- a claim that `location 0` had identical interrupt semantics in both machines merely because both restart paths use low core addresses;
- invention priority.

### The Data General witness adds a clearer warning-versus-stop hardware boundary

DEC KR01 documentation already provides the power-low interrupt and finite save interval. Later KP8-E documentation supplies power-supply filter-capacitor hold-up.

The NOVA 2 technical manual additionally states the relative order of two processor-visible signals: `PWR FAIL` precedes `MEM OK` by about 1–2 ms, and `MEM OK` loss drives halt/reset behavior.

For Case 86 this strengthens the general reconstruction:

```text
early failure knowledge
    can be deliberately generated
    before execution becomes inadmissible
```

without making that relation a universal design law.

### GE-PAC remains a different restart-admission case

GE-PAC 3010/2 adds a customer-adjustable Restart Inhibit Timer tied to process safety. Data General's ON/LOCK switch instead controls whether automatic restart occurs after power returns.

Both show:

```text
retained context
    !=
automatic restart authority
```

but only GE in the current evidence makes that authority explicitly depend on outage duration.

---

## Philosophical interpretation — bounded

### I — an interruption can be managed as a sequence rather than a single instant

The NOVA manuals make `power failure` technically non-instantaneous. The machine observes an early warning, performs bounded work, crosses a later point where normal execution ends, and then later applies a restart policy after supply recovery.

A limited interpretation follows:

> technical continuity can depend on retaining enough structure **through a staged transition**, not on denying that a break occurred.

The value of the case is the exact mechanism: warning, transfer, stop/reset, preserved core, restart entry, reconstruction.

This does **not** license a universal metaphysics of interruption, nor does it turn every voltage comparator into a memory device.

### I — useful persistence can require intentionally not preserving every state class

The processor may reset control/device state while selected execution information has been migrated into core. Continuity therefore depends on selective preservation plus reconstruction, not on preserving every pre-failure electrical state unchanged.

This interpretation is bounded by the historical machine behavior and is not Data General's own philosophical vocabulary.

---

## Claim ledger

| Claim | Type | Evidence strength | Boundary |
| --- | --- | --- | --- |
| 1969 NOVA maintenance documentation describes an optional power monitor whose Power Failure flag precedes RUN clear by about 1–2 ms | H/P* | strong indexed manufacturer-primary | exact scan publication month / page-image verification still open |
| after adequate memory and logic power return, the 1969 NOVA restart one-shot can set RESTART when the key is locked | H/P* | strong indexed manufacturer-primary | does not prove identical later NOVA 2 circuitry |
| October-1974 NOVA system reference says AC power-on leaves core unaltered while PC/accumulator/flag initial states are indeterminate | H/P | strong primary | product-family statement, not universal core-machine law |
| the same manual gives a minimum 1–2 ms interval after the power-fail interrupt before shutdown | H/P | strong primary | timing contract, not ferrite retention lifetime |
| the processor completes a memory cycle and sequences power off so memory contents are unaffected | H/P | strong primary | does not prove every arbitrary electrical fault is safe |
| software should save accumulators, Carry, and the interrupted-PC/location-0 relation in memory | H/P | strong primary | exact application save set may be larger |
| LOCK permits automatic restart via location 0 while ON leaves the machine stopped | H/P | strong primary | restart policy != core remanence |
| NOVA 2 `PWR FAIL` precedes `MEM OK` by about 1–2 ms | H/P* | strong indexed manufacturer-primary | page render pending |
| NOVA 2 `MEM OK` low drives halt/reset behavior including I/O reset | H/P* | strong indexed manufacturer-primary | model-specific behavior |
| NOVA 2 waits 2 ms after `MEM OK` and `PWR FAIL` recover before optional LOCK-position restart | H/P* | strong indexed manufacturer-primary | do not merge with 50 ms system-reference delay |
| NOVA 2 power module asserts `PWR FAIL` when bridge output falls to +24 V and clears `PWR OK` below +4.7 V on +5 V line | H/P* | strong indexed manufacturer-primary | control thresholds, not core-retention thresholds |
| `MEM OK` is identical to `PWR OK` or `+5V OK` | X | rejected | explicit mapping not yet inspected |
| 50 ms and 2 ms are contradictory measurements of one universal NOVA delay | X | rejected | manuals differ in model scope and timing origin |
| early-warning threshold != later execution-admissibility threshold | E | strong | project reconstruction from ordered signals |
| memory-cycle completion != CPU-context save | E | strong | two separately documented obligations |
| save-window duration != core-retention lifetime | E | strong | timing resource vs material persistence |
| Data General's design proves direct descent from DEC KR01 | X | rejected | no genealogy evidence |
| similar location-0 restart semantics prove identical interrupt architecture | X | rejected | only a bounded functional analogy is used |
| automatic-restart option was installed in every NOVA | X | rejected | manuals describe an option |

---

## Why this changes Case 86

Before this slice, Case 86 already established from DEC and GE that core nonvolatility is insufficient for whole-computer continuation and that restart authority can be separated from surviving saved context.

The Data General evidence adds three stronger boundaries:

1. **cross-vendor primary evidence by 1969** that the power-fail path was explicitly staged as warning -> bounded execution -> stop -> conditional restart;
2. **hardware-visible sequencing** in NOVA 2 where `PWR FAIL` precedes `MEM OK`, making `failure knowledge != execution already impossible` explicit;
3. **document/model-specific restart timing** (`50 ms` in the broad system reference versus `2 ms after recovered signals` in the NOVA 2 manual), demonstrating why product-family timing must not be flattened.

The bounded conclusion is now:

```text
nonvolatile core payload
    + early power-failure warning
    + finite state-migration time
    + safe completion/stop boundary
    + retained restart entry
    + restart policy
    + software reconstruction

can support program continuation across a power interruption
```

but none of those relations is identical to magnetic remanence itself.

---

## Remaining work

- directly render and inspect the 1969 NOVA Maintenance Manual pages containing drawing 11 and the power-monitor text;
- directly render the NOVA 2 `C-8` / `P-7` pages from a host that does not reject page retrieval;
- recover earlier revisions of *How To Use The Nova Computers* to determine when the programmer-visible 1–2 ms save / location-0 restart contract first appears in that manual series;
- reconcile the broad manual's `50 ms after power comes back on` with the NOVA 2 manual's `2 ms after MEM OK and PWR FAIL have both gone high` by exact model, revision, and timing origin rather than assumption;
- inspect schematics for the explicit mapping among processor `MEM OK` and power-module `PWR OK` / `+5V OK` signals;
- identify the exact hold-up energy path for the original NOVA and NOVA 2 without importing DEC KP8-E capacitor evidence;
- find surviving Data General operating-system or application power-fail handlers that show how real software used the save contract;
- route any broader Data General machine/power-supply history to `computing-archaeology` rather than expanding Case 86 into a NOVA encyclopedia.

---

## Sources

### Data General primary documentation

1. **Data General Corporation, _NOVA Maintenance Manual_ (archived 1969 scan)**, processor-options discussion, printed p. `2-13`, optional power monitor and restart sequence. Bitsavers: <https://bitsavers.org/pdf/dg/NovaMaint_1969.pdf>.
2. **Data General Corporation, _How To Use The Nova Computers_, Ordering No. 015-000009, Rev. 09, October 1974**, §2.6 `Power Monitor and Auto Restart`, printed pp. `2-39`–`2-40`. Preserved scan indexed by Bitsavers as `015-000009-09_HowToUseNova.pdf`; Computer History Museum access copy: <https://archive.computerhistory.org/resources/access/text/2024/06/102776244-05-0001-acc.pdf>.
3. **Data General Corporation, _NOVA 2 Technical Manual_, Ordering No. 015-000026, Rev. 01, November 1974**, processor power-fail/restart description at `C-8`, Figure `C-4`, and Power Fail Module description at `P-7`. Bitsavers: <https://www.bitsavers.org/pdf/dg/Nova_2/015-000026-01_Nova2Tech_Nov74.pdf>.

### Related internal sources

- [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md) — remanent payload, destructive-read restore, and whole-system nonvolatility boundary.
- [`../cases/86-dec-pdp8-core-power-fail-auto-restart.md`](../cases/86-dec-pdp8-core-power-fail-auto-restart.md) — DEC-centered canonical case.
- [`86-dec-1960-1970-core-power-restart-grounding.md`](86-dec-1960-1970-core-power-restart-grounding.md) — DEC grounding record.
- [`86-gepac-1972-restart-inhibit-admissibility-deepening.md`](86-gepac-1972-restart-inhibit-admissibility-deepening.md) — GE-PAC restart-admission comparison.
- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — broader machine-history destination; no dedicated `Nova power fail` slice was found in the repository search performed for this deepening.
