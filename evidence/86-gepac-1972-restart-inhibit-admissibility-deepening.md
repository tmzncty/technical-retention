# Case 86 deepening — GE-PAC 3010/2 power-fail capture, retained context, and time-bounded restart admission

**Status:** `bounded deepening complete` for the capture-deadline / restart-admission distinction; facsimile rendering and exact timer-revision genealogy remain open.

Canonical case: [`../cases/86-dec-pdp8-core-power-fail-auto-restart.md`](../cases/86-dec-pdp8-core-power-fail-auto-restart.md).

## Scope

This addendum deepens Case 86 at one narrow seam that the DEC material leaves only partly explicit:

> **After a process computer detects impending power loss, how are the deadline for capturing volatile execution state, the physical lifetime of the captured representation, and the later deadline for automatically resuming that representation kept separate?**

The bounded historical witness is General Electric's **GE-PAC 3010/2** process computer. The inspected 1972-era manufacturer documentation exposes three different temporal relations that must not be collapsed:

1. an impending-power interval in which processor state must be transferred into magnetic core before ordinary processor control is cleared or usable logic power disappears;
2. a subsequent interval in which that saved PSW/register representation remains in core without ordinary processor activity;
3. an optional **Restart Inhibit Timer** that can revoke automatic restart after an operator-selected outage interval because the controlled process may no longer be safe to resume automatically.

The new contribution of this pass is the first relation. A GE processor-maintenance manual says the system-clear line (`SCLRO`) becomes true about **three milliseconds after the Power Failure Detector detects power loss**. Before that clear occurs, the micro-program enters its power-failure path, reaches ROM address `X'9E'`, and stores the PSW and General Registers into the core save area selected through the register-save pointer at core address `X'22'`. A separate power-subsystem manual says the detector initiates this save early enough for it to finish before processor logic power drops below its operating level.

This closes a previously open timing-architecture question without claiming that three milliseconds is a ferrite-retention limit, an exact electrical hold-up-energy specification, or a universal GE-PAC restart constant.

This is not:

- a second general history of magnetic core;
- a claim that GE derived the design from DEC;
- a claim that every GE-PAC 3010/2 processor configuration implemented the power-fail save path;
- a universal process-control restart rule;
- evidence that core remanence expires when the restart-inhibit timer expires;
- a proof of the exact capacitor/energy-storage mechanism sustaining the approximately three-millisecond pre-clear interval;
- a claim that the conflicting 10-second and one-minute lower timer limits can already be reconciled.

The broader core-memory engineering history remains work for `tmzncty/computing-archaeology`; fresh searches for `GE-PAC 3010`, `GET-6227`, and the restart-inhibit option found no dedicated companion packet to reuse.

---

## Source custody and evidence class

### General Electric GET-6227, May 1972

General Electric's *GE-PAC 3010/2 General Description*, GET-6227, May 1972, is manufacturer-primary documentation. Its power-fail/restart section states that if primary AC falls to the documented low threshold or disappears for more than one cycle, the contents of the General Register Stack and PSW Register are automatically stored in Core Memory and an orderly shutdown begins.

The same section says that if primary power returns before the optional Restart Inhibit Timer runs out, hardware is initialized and the General Registers and PSW are restored. The restored PSW then determines whether ordinary sequencing resumes directly or the documented machine-malfunction handling path is entered.

Section 4.7.1 names option `3010AB14 Restart Inhibit Timer` and gives a calibrated range of **10 seconds to 10 minutes**. GE explicitly ties the selected interval to the customer's judgement about the process and controls that may back up the computer.

### GE-PAC 3010/2 Power Subsystem manual

The separate GE *3010/2 Power Subsystem* manual supplies a more implementation-oriented account. It states that the Power Failure Detector monitors primary AC and initiates automatic storage of the PSW and General Registers into the core area specified by the register-save pointer at dedicated core address `X'22'`. It says the save sequence is started early enough to finish before the Central Processor's logic power falls below its operating level.

The same manual adds a configuration boundary: **Central Processors A3503 and A3504 have the Power Failure Detector / Automatic Restart options, while A3501 and A3502 do not**. The presence of magnetic core therefore does not by itself prove that the processor configuration can perform this failure-triggered state transfer.

This manual also describes a `B1401 Automatic Restart Inhibit Timer`, but gives a range of **one minute to 10 minutes** rather than GET-6227's 10-seconds-to-10-minutes range.

### GE-PAC 3010/2 Processor maintenance manual

The archived GE processor-maintenance manual supplies the new timing anchor. In its `INITIALIZATION` discussion it states that `SCLRO` goes true about **three milliseconds after the Power Failure Detector detects a power loss** and remains true while power is off. When the Processor is initialized, clock timing is initialized/stopped, alarm and control flip-flops are reset, the ROM address is set to zero, the phase counter is set to phase 3, and memory-control logic is reset.

Crucially, the same passage says that during the interval **before `SCLRO` goes true**, the micro-program enters phase 3, detects the power-failure condition (`PPF`), enters the routine at ROM address `X'9E'`, and stores the PSW and General Registers in the core area specified by the register-save pointer at `X'22'`.

That gives a direct sequencing relation:

```text
Power Failure Detector asserts failure
    ↓
pre-clear micro-program interval
    ↓
phase 3 / PPF path / ROM X'9E'
    ↓
PSW + General Registers copied to core via X'22' save pointer
    ↓
~3 ms after detection: SCLRO asserted
    ↓
processor control state initialized/cleared while power remains off
```

The documentation does **not** justify replacing this with `the machine has exactly 3 ms of usable energy`. It establishes the detector-to-system-clear timing and the required save-before-clear ordering. The Power Subsystem manual separately establishes that the save must complete before logic power falls below its operating level.

### Facsimile boundary

The archived GE documents are manufacturer-primary manuals. The web research system recovered exact searchable text from the archival PDF corpus, but direct page-image rendering of the Bitsavers endpoints remained blocked by the archive/tool transport path during this pass. Exact GE mechanism/range statements therefore remain marked `H/P*`: primary-document text with a source-custody caveat pending direct page-image verification.

This limitation matters for page anchoring and typography, not for silently harmonizing contradictions. In particular, the two Restart Inhibit Timer ranges remain a documented discrepancy.

---

## Historical record

### H/P* — impending power loss triggers a deliberate transfer of execution context into core

GET-6227 says the Central Processor monitors primary AC. At the documented low-voltage / missing-cycle condition, the General Register Stack and PSW are automatically stored in Core Memory and an orderly shutdown is initiated.

The Power Subsystem manual sharpens the same relation: the detector starts the PSW/register storage micro-program early enough for the transfer to finish before logic power falls below its operating level.

Historical relation:

```text
volatile execution context
    + impending-power evidence
        ↓
micro-programmed transfer
        ↓
reserved core-memory continuation representation
        ↓
processor shutdown / control initialization
```

This is stronger than the generic statement `core memory is nonvolatile`.

### H/P* — the save path has a documented pre-clear timing boundary

The Processor maintenance manual says `SCLRO` becomes true about three milliseconds after the Power Failure Detector detects power loss. It also places the save routine before that event: phase 3 sees `PPF`, branches to ROM address `X'9E'`, and writes the PSW and General Registers to the core save area selected by the pointer at `X'22'`.

Safe historical claim:

> **GE documented a roughly three-millisecond detector-to-system-clear interval and placed the register/PSW save micro-program before system clear.**

Unsafe historical claim:

> `3 ms` was the exact energy-hold-up lifetime of every GE-PAC 3010/2 configuration.

The latter is not established by the inspected text.

### H/P* — state capture is configuration-dependent

The Power Subsystem manual says A3503 and A3504 Central Processors have the relevant Power Failure Detector / Automatic Restart options, whereas A3501 and A3502 do not.

Therefore:

```text
core memory installed
    !=
power-fail detector present
    !=
automatic register-save/restart path present
```

This is an implementation/configuration statement for the documented GE-PAC family, not a universal property of core-memory computers.

### H/P* — the saved state occupies a designated core relation

The power-subsystem and processor-maintenance descriptions both connect the saved state to a register-save pointer at dedicated core address `X'22'`. The maintenance text adds the micro-program entry at `X'9E'`.

This makes the saved representation an intentionally created continuation object, not merely whatever application words happened already to reside in core.

This evidence does not reconstruct the full internal save-area layout beyond the manuals' statements.

### H/P* — after the handoff, processor control can be reset while core remains the continuation carrier

The Processor maintenance manual describes `SCLRO` initialization of clocks, control flip-flops, ROM address, phase state, and memory-control logic after the pre-clear save path. The General Description says that after the power-down sequence no further attempts are made to read or write core and that core retains the stored information until power returns.

The bounded historical sequence is therefore not `everything remains unchanged`:

```text
selected execution state copied into core
        ↓
processor/control initialization and power-down
        ↓
core-resident representation remains available
```

### H/P* — restoration is a later operation, not the same event as state survival

GET-6227 says that if power returns under the applicable restart conditions, hardware is initialized and the General Registers and PSW are restored. The Power Subsystem manual likewise describes a restoration micro-program on AC return.

Therefore:

> `saved representation exists in core` **!=** `running processor state has already been reconstructed`.

### H/P* — automatic-restart authority can expire while core state survives

GET-6227's optional `3010AB14 Restart Inhibit Timer` prevents automatic restart after an outage considered too long for safe unattended continuation of the controlled process. The interval is chosen with reference to the process and backup controls.

The Power Subsystem manual preserves the same policy relation for its `B1401` timer, notwithstanding the lower-bound discrepancy.

Historical relation:

```text
saved PSW/register representation can remain in core
        !=
automatic restart remains authorized indefinitely
```

### H/P* — surviving manuals disagree on the timer's lower bound

The two inspected GE manuals agree on the role and **10-minute upper bound** but disagree on the lower adjustable limit:

- GET-6227, May 1972: **10 seconds to 10 minutes**;
- Power Subsystem manual: **1 minute to 10 minutes**.

This pass found no dated option-revision/configuration record strong enough to decide whether the discrepancy reflects a hardware revision, model/configuration difference, documentation revision, or error.

The discrepancy is therefore retained as evidence, not normalized away.

---

## Engineering reconstruction

### E — capture deadline, retention lifetime, and restart-admission deadline are three different clocks

The combined GE documentation supports a more precise decomposition than the earlier two-way `retained context vs restart authority` distinction:

```text
(1) CAPTURE DEADLINE
    failure detected
        → save must finish before system clear / unusable logic power

(2) REPRESENTATION RETENTION
    saved PSW + registers remain in magnetic core during outage

(3) RESTART-ADMISSION DEADLINE
    separately configured timer may expire because the controlled process
    is no longer considered safe for automatic continuation
```

Therefore:

> **capture deadline != physical-retention lifetime != restart-admission deadline.**

The approximately three-millisecond figure belongs to the documented detector-to-system-clear transition, not to the timer and not to core remanence.

### E — a successful checkpoint-like transfer does not guarantee future authority to use it automatically

Once the save micro-program has completed, recoverability and admissibility remain separate questions:

1. **recoverability:** does a valid PSW/register representation remain available and restorable?
2. **admissibility:** is automatic continuation still allowed under process-control policy?

The Restart Inhibit Timer can answer the second question negatively without showing that the first has become false.

> **recoverable saved context != automatically admissible continuation.**

`checkpoint-like` is modern functional vocabulary here, not attributed GE terminology.

### E — failure-transition infrastructure includes timing/control state that is not payload

`SCLRO`, the detector, the phase-3 branch, ROM entry `X'9E'`, and the register-save pointer do not themselves constitute the application payload. Yet they determine whether volatile execution context crosses the power boundary into a substrate that can retain it.

Thus:

> **retention infrastructure can determine whether state survives without itself being the retained payload.**

### E — system clear can support continuity by retiring the wrong state classes after the right ones have been copied

The maintenance manual's ordering is important: selected PSW/register state is copied before system clear resets a range of processor-control state.

This yields a bounded reconstruction:

> **retention can require selective migration followed by deliberate retirement of other control state.**

That is not equivalent to saying every cleared state is irrelevant. It says only that GE's documented continuation path does not require all active control state to remain electrically unchanged across the outage.

### E — option presence is part of the retention relation

A3501/A3502 versus A3503/A3504 shows that the same broad computer family can have nonvolatile core without the automatic failure-triggered save/restart option.

Therefore:

> **substrate capability != configured continuation mechanism.**

The machine's ability to retain ordinary core words and its ability to capture volatile execution state under failure are distinct design/configuration facts.

### E — external-world drift can invalidate continuation without corrupting the saved representation

The timer is explicitly tied to whether restarting the computer's control of the process remains safe. During an outage, pumps, valves, actuators, sensors, mechanisms, or backup controls may change independently of the saved CPU state.

A register/PSW image can therefore remain intact while the relation between that image and the controlled process has become unsuitable for automatic resumption.

`external-world drift` is project reconstruction, not GE's wording.

### E — restart-inhibit interval is not a magnetic-core lifetime

It would be a category error to read either `10 seconds` or `1 minute` as the retention lifetime of ferrite core. The manuals tie the timer to process-safety policy, not to magnetic decay.

> **restart-admission deadline != core-retention deadline.**

### E — the three-millisecond transition is not yet an electrical hold-up mechanism proof

The Processor maintenance manual establishes when `SCLRO` occurs relative to power-failure detection and that the save runs first. The Power Subsystem manual establishes that the save finishes before logic power falls below its operating level.

Those two facts do **not** identify the exact stored-energy component, capacitance, supply-decay curve, or worst-case margin that makes the interval possible.

So:

> **documented save-before-clear timing != proven electrical hold-up implementation.**

This keeps the new timing result from repeating the earlier anti-back-projection error that Case 86 already avoids for DEC KR01 versus later KP8-E capacitor documentation.

---

## Functional comparison

### A — DEC PDP-8 Case 86: same broad handoff role, different implementation boundary

DEC KR01/KP8-family evidence and GE-PAC 3010/2 both show impending-power detection followed by transfer of volatile execution state into magnetic core and later restoration.

The comparison is bounded:

- DEC KR01 documents a software interrupt path with a one-millisecond continued-operation contract and restart through address `0000`;
- GE-PAC documentation exposes a micro-programmed phase-3 power-failure path, ROM entry `X'9E'`, save pointer `X'22'`, and an approximately three-millisecond detector-to-`SCLRO` interval;
- GE additionally documents a process-safety Restart Inhibit Timer.

No DEC→GE, GE→DEC, common circuit, or common option genealogy is established.

### A — later power-loss-protection systems

A later SSD/controller may also detect power loss, exploit a bounded remaining operating interval, and move selected volatile state into a more failure-tolerant representation. The shared abstraction is only:

```text
failure evidence
    → finite transition opportunity
        → selective state handoff
```

GE-PAC's magnetic core, micro-programmed processor save, process-control restart gating, and 1970s option structure are not thereby equivalent to SSD volatile write-cache flush, PLI capacitors, ADR, or persistence domains.

### A/X — restart-inhibit policy is not a lease, epoch, or consensus term

Modern distributed-system notions can make the `saved state survives but authority expires` relation intuitively familiar, but the GE timer is a local process-control safety option. No protocol/genealogy claim follows from the analogy.

---

## Philosophical interpretation — bounded

### I — continuity has at least three temporal conditions here

The exact technical facts are narrow:

- execution context has to be **captured in time** before one transition boundary;
- its physical representation can then **survive** the outage in core;
- permission to turn that representation back into automatic action can **expire earlier than the representation itself** because the external process may have changed.

This supports one limited conceptual point:

> persistence is not only a question of whether an inscription survived; it can also depend on whether the inscription was created before a deadline and whether the relation authorizing its future use is still valid.

The interpretation stops there. The GE-PAC design is not a general theory of memory, process safety, or historical continuity.

---

## Explicit non-claims

This evidence does **not** claim that:

1. GE invented power-fail detection;
2. GE invented automatic restart;
3. GE invented saving processor state in nonvolatile memory;
4. the GE-PAC mechanism descends from DEC KR01;
5. DEC KR01 descends from GE-PAC;
6. every GE-PAC 3010/2 CPU implemented the Power Failure Detector / Automatic Restart path;
7. every machine with magnetic core could automatically save volatile CPU state;
8. the three-millisecond detector-to-`SCLRO` interval is a magnetic-core retention lifetime;
9. the three-millisecond interval is a complete electrical hold-up specification;
10. the documentation proves which capacitor or other energy-storage component sustained that interval;
11. the `X'22'` pointer alone contains the complete saved execution context;
12. the `X'9E'` micro-routine is equivalent to a modern operating-system checkpoint implementation;
13. `SCLRO` clears magnetic core payload;
14. a successful save proves peripheral/external-world state is also consistent for restart;
15. the Restart Inhibit Timer measures ferrite decay;
16. timer expiry proves the saved PSW/register representation is corrupt;
17. manual intervention after timer expiry implies the checkpoint is unrecoverable;
18. the 10-second and one-minute lower bounds can already be merged into one historical constant;
19. the two timer ranges prove a hardware revision without a dated revision/configuration record;
20. process-control restart gating is historically identical to modern leases, epochs, fencing, or distributed freshness protocols.

---

## Claim ledger

| Claim | Label | Evidence / boundary |
| --- | --- | --- |
| GE-PAC 3010/2 GET-6227 documents automatic register-stack + PSW transfer into core on detected power failure | `H/P*` | GE GET-6227 indexed primary text; facsimile rendering pending |
| power-fail trigger includes primary AC at or below the documented low threshold or loss for more than one cycle | `H/P*` | GET-6227 / Power Subsystem primary text |
| Power Subsystem documentation associates the save with a register-save pointer at core address `X'22'` | `H/P*` | GE Power Subsystem manual |
| processor-maintenance documentation places the PPF save path at ROM address `X'9E'` before system clear | `H/P*` | GE Processor maintenance manual |
| `SCLRO` is documented as becoming true about 3 ms after the Power Failure Detector detects a loss | `H/P*` | GE Processor maintenance manual |
| the save is initiated early enough to complete before logic power falls below operating level | `H/P*` | GE Power Subsystem manual |
| A3503/A3504 have the relevant power-fail/restart options while A3501/A3502 do not | `H/P*` | GE Power Subsystem manual; configuration-specific claim |
| power return includes a separate initialization/restoration sequence before continuation | `H/P*` | GET-6227 + Power Subsystem manual |
| GE documents an optional Restart Inhibit Timer whose purpose is preventing unsafe automatic restart after a sufficiently long outage | `H/P*` | GET-6227 + Power Subsystem manual |
| GET-6227 gives 10 s–10 min while Power Subsystem gives 1–10 min | `H/P*` | surviving first-party manuals disagree; discrepancy retained |
| exact timer range is one universal GE-PAC constant | `X` | not established |
| ~3 ms is the physical retention lifetime of core | `X` | category error; different state relation |
| ~3 ms proves a specific hold-up capacitor implementation | `X` | no component-level proof in inspected evidence |
| capture deadline, representation-retention lifetime, and restart-admission deadline are distinct | `E` | bounded reconstruction from the three source relations |
| recoverable saved context can coexist with expired automatic-restart authority | `E` | core-retention + Restart Inhibit Timer relation |
| substrate capability and configured continuation mechanism are distinct | `E` | A3501/A3502 vs A3503/A3504 configuration witness |
| GE-PAC and DEC PDP-8 use the same circuit/protocol | `A/X` | functional handoff analogy only |

---

## Prior-art and genealogy boundary

Case 86 already contains earlier DEC power-fail/restart evidence, so this GE material is not used to claim invention priority for failure-triggered state capture or automatic restart.

The defensible contribution is narrower:

> **By 1972, GE process-computer documentation exposes a three-stage retention relation: a bounded pre-clear interval for capturing processor state into magnetic core, a nonvolatile saved representation surviving the outage, and a separately adjustable process-safety deadline after which automatic use of that surviving representation is inhibited.**

The evidence does not establish that GE introduced this three-stage relation first, nor does chronology establish lineage from DEC, IBM, Interdata, or later systems.

A broader genealogy of process-computer power-fail options, Interdata/GE processor lineage, industrial-control restart policy, and hardware hold-up circuits belongs primarily in `tmzncty/computing-archaeology` if pursued.

---

## Remaining debt after this pass

This pass **partially closes** two earlier open questions:

- the timing relation between failure detection, the save micro-program, and system clear now has a first-party textual anchor: `SCLRO` is about three milliseconds after detection and the PPF save path runs before it;
- CPU configuration dependence is no longer only hypothetical: the Power Subsystem manual distinguishes A3503/A3504 from A3501/A3502 for the relevant options.

Still open:

- obtain directly renderable page-image/facsimile anchors and stable printed-page numbers for the exact GE paragraphs;
- resolve the chronology/configuration behind **10 s–10 min** versus **1–10 min** Restart Inhibit Timer ranges;
- recover the exact electrical hold-up/decay implementation that guarantees the save interval, including component-level energy-storage evidence if surviving documentation permits;
- map the processor-model/option identifiers (`3010AB14`, `B1401`, A3501–A3504) across dated configurators/revisions without assuming name equivalence;
- inspect application-specific GE-PAC deployments before making claims about how operators actually chose timer values;
- keep broad GE-PAC and process-computer restart genealogy in `computing-archaeology` rather than expanding this retention-specific file into a product history.

---

## Sources

1. General Electric, *GE-PAC 3010/2 General Description*, GET-6227, May 1972, especially §4.7 `POWER FAIL DETECTOR AND AUTOMATIC RESTART` and §4.7.1 `Restart Inhibit Timer Option`; archived scan: <https://www.bitsavers.org/pdf/ge/GE-PAC_3010/GET-6227_GE-PAC_3010_2_General_Description_197205.pdf>.
2. General Electric, *3010/2 Power Subsystem*, especially `Power Failure Detector and Automatic Restart Option` and `Automatic Restart Inhibit Timer`; archived scan: <https://www.bitsavers.org/pdf/ge/GE-PAC_3010/3010_Power_Subsystem.pdf>.
3. General Electric, *GE-PAC 3010/2 Processor* maintenance/theory material, especially `INITIALIZATION`, for `SCLRO`, phase-3 `PPF`, ROM `X'9E'`, and register-save pointer `X'22'`; public archive mirror: <https://bitsavers.trailing-edge.com/pdf/ge/GE-PAC_3010/GE-PAC_3010_2_CPU_Maintenance.pdf>.
4. General Electric, *GE-PAC 3010/2 Central Processor Reference Manual*, GET-6174, October 1972, used only for system/context cross-checks rather than the new timing claim: <https://www.bitsavers.org/pdf/ge/GE-PAC_3010/GET-6174_GE-PAC_3010_2_Central_Processor_Reference_Manual_197210.pdf>.
5. BAMA archive index for the surviving GE-PAC 3010 manual set, used for custody/file identification rather than mechanism claims: <https://bama.edebris.com/manuals/bitsavers/pdf/ge/GE-PAC_3010/index-2098439346.html>.

### Source-boundary note

The GE manuals are manufacturer-primary documents. Exact indexed text is available from the archived corpus, but direct page-image rendering remained unavailable in this research environment. Mechanism/range claims therefore remain `H/P*` until facsimile inspection is completed. The new contribution is the independently recovered maintenance-text sequence around `PPF → X'9E' → X'22' save → ~3 ms SCLRO`, together with the configuration witness A3503/A3504 versus A3501/A3502; neither is used to erase the existing source-custody caveat or the timer-range discrepancy.
