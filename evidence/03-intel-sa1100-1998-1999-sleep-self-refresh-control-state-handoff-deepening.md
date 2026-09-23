# Deepening Record — Intel SA-1100 1998–1999 Sleep Self-Refresh / Control-State Handoff

## Target case

[`cases/03-dram-refresh-as-scheduled-restoration.md`](../cases/03-dram-refresh-as-scheduled-restoration.md)

## Status

**`bounded deepening complete`**

Canonical maturity remains **`grounded`** in [`CASE_INDEX.md`](../CASE_INDEX.md). This record does not promote the case and does not turn Case 03 into a general StrongARM, low-power, suspend/resume, or DRAM-controller history.

## Research question

Case 03 already separates the DRAM payload from refresh timer / coverage / arbitration state. Earlier Intel controller evidence shows that maintenance-control state can fail before the payload visibly fails, while TI / NEC evidence shows that refresh-address state and refresh-cadence authority can move across the controller / device boundary.

This slice asks a narrower later-system question:

> Can a named controller deliberately lose its ordinary DRAM control registers and refresh-counter state across a low-power transition while the DRAM payload remains retained, because preservation authority has first been handed to the DRAM's self-refresh mode and a smaller hold / resume state survives long enough to reconstruct the controller?

For Intel's StrongARM SA-1100 documentation, the answer is **yes**.

The important relation is not simply `self refresh retains DRAM`. The documents expose a staged authority handoff:

```text
normal run
    controller schedules CBR refresh
    ↓
sleep entry
    finish admitted memory operation
    ↓
place DRAM in self-refresh
    ↓
reset / power down ordinary memory-controller state
    ↓
DRAM maintains its own retention relation
    ↓
wake
    keep DRAM held in self-refresh
    ↓
software reconstructs controller configuration
    ↓
release self-refresh
    ↓
resume ordinary controller-managed accesses / refresh
```

Thus:

```text
payload survives
    != controller configuration survives

controller reset
    != preservation relation necessarily disappears

reconfigure controller
    != reconstruct payload

sleep-state continuity
    != ordinary execution-state continuity
```

---

## Source set and provenance

### Source A — Intel SA-1100 Technical Reference Manual, September 1998

Intel Corporation, **SA-1100 Microprocessor Technical Reference Manual**, September 1998, Order Number `278088-001`.

Public archival PDF mirror:

<https://stuff.mit.edu/afs/sipb/contrib/doc/specs/ic/cpu/arm/sa1100-techref.pdf>

The inspected PDF identifies itself as Intel documentation and is explicitly marked an intermediate draft. Therefore this slice uses it as a **manufacturer-primary draft artifact**, not as proof that every later production stepping had identical behavior.

Relevant inspected sections / printed pages:

- §9.5.3.3, `The Sleep Shutdown Sequence`, printed p. 9-28;
- §9.5.3.6–7, boot / DRAM revival, printed pp. 9-29 to 9-30;
- §9.5.7.5–6, DRAM hold and scratchpad state, printed pp. 9-38 to 9-39;
- §9.6, reset-controller semantics, printed p. 9-40;
- §10.3.3–4, DRAM refresh / self-refresh, printed p. 10-18;
- §10.7.1, post-reset / post-sleep memory-interface flow, printed pp. 10-30 to 10-31.

### Source B — Intel SA-1100 Developer's Manual, August 1999

Intel Corporation, **Intel StrongARM SA-1100 Microprocessor Developer's Manual**, August 1999, Order Number `278088-004`.

Publicly indexed mirror:

<https://www.manualsdir.com/manuals/126682/intel-strongarm-sa-1100.html>

The later manual's public page index preserves the same relevant section structure and page locations, including:

- sleep shutdown at p. 9-28;
- DRAM revival at p. 9-30;
- DRAM control hold at p. 9-38;
- refresh / self-refresh in chapter 10;
- memory-interface initialization after sleep / reset.

Source B is used as a later-edition confirmation that the boundary was not only present in the inspected September-1998 draft. Where this record makes a detailed operational claim, the exact wording was checked in the inspected Intel PDF in Source A; the 1999 manual is a confirming edition witness.

### Related-repository check

Current GitHub searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `SA-1100` and `StrongARM` found no dedicated treatment to reuse. A broader history of StrongARM, mobile power management, suspend-to-RAM, DRAM-controller design, and processor power domains belongs there if later developed. This record keeps only the retention-specific authority / state boundary.

---

# Historical record

## H/P — During ordinary operation, the SA-1100 owns refresh cadence while the DRAM supplies the CBR-internal row progression

Intel §10.3.3 says the SA-1100 supports CAS-before-RAS (`CBR`) refresh. When the DRAM interface is enabled and the programmed refresh interval is nonzero, the controller's refresh counter counts memory cycles. When the programmed interval is reached, the controller records that a refresh is due, clears / restarts its interval count, waits for the current transaction to complete, and performs a CBR refresh.

The same section gives an unusually useful reset distinction:

- **hardware reset clears the refresh counter**;
- **software reset does not affect it**.

This means the manufacturer documentation itself does not treat `reset` as one uniform persistence boundary.

For the bounded relation here:

```text
ordinary-run retention obligation
    ↓
SA-1100 refresh-interval state
    ↓
externally initiated CBR cycle
    ↓
DRAM-internal CBR refresh-row progression
```

The controller's interval counter is maintenance-control state. It is not the DRAM payload and is not itself a durable representation of application data.

**Primary anchor:** Intel SA-1100 TRM, September 1998, §10.3.3, printed p. 10-18.

---

## H/P — Sleep entry drains the currently admitted memory operation before handing retention to DRAM self-refresh

Intel §9.5.3.3 defines a three-step sleep shutdown sequence. During the first step, before the later internal reset and power removal, the memory controller:

1. **finishes whatever memory operation might be in progress**;
2. places the DRAMs into self-refresh;
3. drives the relevant RAS / CAS pins into the state used to keep the DRAMs in self-refresh.

Only in the next shutdown step does Intel say that an internal reset is applied to the SA-1100 and the units are reset. In the third step, the main internal supply can be disabled.

This ordering supplies a direct named-system witness for:

```text
stop / power transition requested
    != immediately erase controller execution context
```

Instead, the documented sequence first closes the already-admitted memory operation and establishes a replacement preservation regime.

The source does **not** prove that every possible external power collapse affords enough time to complete this sequence. Intel separately routes `VDD_FAULT` / `BATT_FAULT` through the same sleep state machine, but this record does not infer analog hold-up margins that the inspected section does not specify.

**Primary anchor:** Intel SA-1100 TRM, §9.5.3.3, printed p. 9-28.

---

## H/P — Self-refresh is established before ordinary controller power / clocks disappear

Intel §10.3.4 states that before entering sleep, the SA-1100 puts the DRAM into self-refresh by asserting CAS and then RAS in the appropriate sequence and **maintains them in the self-refresh state while power and clocks are turned off**.

This is not merely a low-power label. It identifies the point where maintenance authority crosses a boundary:

```text
before sleep:
    SA-1100 owns refresh request timing

inside sleep:
    DRAM self-refresh owns the recurring retention work
```

The transition is therefore not `refresh stops because the processor sleeps`. The controller first changes which component is responsible for making refresh continue.

**Primary anchor:** Intel SA-1100 TRM, §10.3.4, printed p. 10-18.

---

## H/P — Sleep reset can reset the memory controller while a smaller power-manager relation keeps the DRAM in self-refresh

Intel §9.6 distinguishes four reset types: hardware, software, watchdog, and sleep reset.

For **sleep reset**, the manual says the majority of the chip loses power and receives reset. It explicitly says that although the memory controller is in reset, the RAS / CAS pins are held in the self-refresh state required by the DRAMs.

This is the core historical witness for this slice:

```text
ordinary memory-controller state reset
    +
self-refresh interface relation retained
    ->
DRAM payload may continue to be retained
```

The retention path is therefore not identical to the ordinary controller state that existed before sleep.

A smaller always-available power-management domain preserves the condition needed to leave the DRAM in its autonomous maintenance mode while the larger controller domain is reset.

**Primary anchor:** Intel SA-1100 TRM, §9.6, printed p. 9-40.

---

## H/P — The manual explicitly says the DRAM payload survives sleep while the DRAM control registers do not

Intel §9.5.3.7 says that because the DRAMs were placed into self-refresh before sleep shutdown, **their contents are preserved during sleep**.

The next sentence gives the negative half of the same boundary: after wake, software must **reconfigure the DRAM control registers, which lost power during sleep mode**, and only then take the DRAMs out of self-refresh.

This is unusually direct primary evidence for:

```text
retained payload
    != retained controller configuration
```

and for:

```text
loss of the old controller state
    != loss of the payload
```

provided that the self-refresh preservation relation remains intact.

**Primary anchor:** Intel SA-1100 TRM, §9.5.3.7, printed p. 9-30.

---

## H/P — Wake keeps the DRAM protected while software reconstructs controller state

The SA-1100 does not release the DRAM from self-refresh as soon as the CPU wakes.

Intel's `DH` (`DRAM control hold`) state is set on exit from sleep. The manual says the RAS / CAS pins continue to be held in the self-refresh state, and software should clear `DH` **after the DRAM interface has been configured but before any DRAM access is attempted**.

The chapter-10 initialization sequence says the same thing operationally:

1. boot from ROM;
2. program the memory configuration registers while leaving DRAM banks disabled;
3. if waking from sleep, release the RAS / CAS self-refresh hold only after the interface is configured;
4. wait the DRAM-specific post-self-refresh precharge interval;
5. then enable the DRAM banks / perform ordinary accesses.

So the wake path contains a deliberate overlap:

```text
old controller configuration gone
    ↓
DRAM still self-refreshing
    ↓
new controller configuration reconstructed
    ↓
self-refresh hold released
    ↓
ordinary access resumes
```

This overlap is the safety boundary. Reconstruction of maintenance-control state occurs while the payload is still being actively retained by the previous preservation regime.

**Primary anchors:** Intel SA-1100 TRM, §9.5.7.5, printed p. 9-38; §10.7.1, printed pp. 10-30 to 10-31.

---

## H/P — A tiny retained scratchpad can bridge configuration reconstruction without retaining the controller itself

Intel also documents a `Power Manager Scratch Pad Register (PSPR)` powered from the VDDx domain. Its contents survive sleep and can be used, for example, to index ROM information used to retrieve memory-controller configuration.

This is not a DRAM payload copy and not a persistent clone of all controller registers. It is a much smaller retained clue that can help reconstruct lost operating configuration.

The system therefore contains at least three distinct retention classes across sleep:

```text
DRAM payload
    -> retained by DRAM self-refresh

ordinary memory-controller configuration
    -> lost; reconstructed after wake

small power-manager scratch / hold state
    -> survives long enough to coordinate reconstruction
```

This is a particularly clean historical example of **reconstructability substituting for full state retention**.

**Primary anchor:** Intel SA-1100 TRM, §9.5.7.6, printed p. 9-39; §9.5.3.6, printed pp. 9-29 to 9-30.

---

## H/P — Software reset, sleep reset, and hardware reset deliberately have different retention consequences

Intel §9.6 makes the reset matrix explicit.

### Software reset

The majority of the SA-1100 is reset, but the manual says **DRAM refresh and configuration are not cleared**, allowing DRAM contents to survive software reset. Watchdog reset follows the same reset sequence as software reset.

### Sleep reset

The majority of the chip loses power and the memory controller is reset, but the self-refresh pin state is maintained. Controller registers then need reconfiguration after wake while the DRAM payload has been preserved.

### Hardware reset

The memory controller receives a full reset; Intel says **all DRAM contents will be lost during hardware reset**.

The resulting event table is not a simple scalar `stronger reset = more state lost` abstraction. It is a typed contract:

| Event | ordinary controller configuration | refresh / self-refresh continuity | documented DRAM payload consequence |
| --- | --- | --- | --- |
| software reset | refresh + configuration preserved | ordinary refresh continuity preserved | contents may survive |
| watchdog reset | same sequence as software reset | ordinary refresh continuity preserved | contents may survive under same path |
| sleep reset | ordinary controller state reset / later reconfigured | DRAM held in self-refresh by power-management logic | contents preserved during sleep |
| hardware reset | full memory-controller reset | no documented preservation bridge | manual says DRAM contents are lost |

This table is a historical description of the SA-1100 contract, not a universal taxonomy of processor resets.

**Primary anchor:** Intel SA-1100 TRM, §9.6, printed p. 9-40.

---

## H/P — Post-sleep recovery is not the same operation as power-on DRAM initialization

Intel §10.7.1 explicitly separates the two paths.

After **sleep**, software reprograms the memory interface while the DRAM is still held in self-refresh, releases the self-refresh pins, waits the device-specific post-self-refresh interval, and then resumes normal use.

After **power-on reset**, the manual instead calls for the part-specific power-up wait and the number of initialization refreshes required by the DRAM before enabling the banks.

This supports another bounded distinction:

```text
wake from retained self-refresh payload
    != cold initialization of an untrusted / newly powered DRAM state
```

Reinitializing the controller is therefore not evidence that the payload itself was re-created.

---

# Engineering reconstruction

The following relations are **E — engineering reconstructions** from the documented system behavior. They are not period Intel philosophical vocabulary.

## E1 — Maintenance authority can move while payload identity remains continuous

A useful state machine is:

```text
RUN
    payload retained through controller-triggered refresh
        ↓
SLEEP ENTRY
    finish in-flight memory operation
        ↓
HANDOFF
    DRAM enters self-refresh
        ↓
CONTROLLER LOSS
    ordinary memory-controller state resets / loses power
        ↓
SLEEP
    DRAM performs autonomous retention work
        ↓
WAKE HOLD
    power returns, but DRAM remains in self-refresh
        ↓
RECONSTRUCTION
    software rebuilds memory-controller configuration
        ↓
RELEASE
    leave self-refresh after safe configuration
        ↓
RUN
```

The continuity of the application-visible memory contents therefore does not require continuity of one controller instance's full internal state.

---

## E2 — A preservation bridge can outlive the controller that created it

The sleep transition creates a relation that is deliberately left in force while the larger controller is reset:

```text
controller establishes self-refresh condition
    ↓
controller ordinary state disappears
    ↓
held interface state + DRAM self-refresh continue preservation
```

Thus:

```text
creator of preservation regime disappears
    != preservation regime immediately disappears
```

The source proves this only for the documented SA-1100 sleep path, not for arbitrary DRAM controllers.

---

## E3 — Reconstruction can target control state rather than payload state

The wake sequence is easy to misdescribe as `restore memory after sleep`. The manual's own decomposition is more precise:

```text
payload
    already retained in DRAM

controller configuration
    must be reconstructed
```

Therefore:

```text
controller reinitialization
    != payload recovery
```

and:

```text
resume preparation
    != data reconstruction
```

This distinction matters when comparing restart procedures across storage / memory systems. A procedure may be elaborate because control authority must be rebuilt even when the payload never disappeared.

---

## E4 — Small retained state can substitute for retaining a much larger controller image

The power-manager scratchpad can survive sleep and point software toward configuration information, while the ordinary DRAM control registers do not survive.

The architecture therefore demonstrates:

```text
retain full controller image
    not required
if
    enough state survives to reconstruct a valid controller configuration
```

This should not be inflated into a claim that PSPR alone guarantees correct resume. ROM contents, software, wiring, DRAM-specific timing, and the surviving self-refresh relation are all part of the reconstruction path.

---

## E5 — Reset persistence is state-class × event-class specific

Within one named chip, the following are all simultaneously true:

```text
software reset
    preserves DRAM refresh/configuration relation

sleep reset
    discards ordinary controller state
    but preserves the self-refresh hold relation

hardware reset
    removes the preservation bridge relied upon here
```

The engineering lesson is therefore:

```text
"survives reset"
    is incomplete
```

unless the statement names:

```text
state class
× reset/event class
× power domain / interface relation
× survival semantics
```

This is consistent with, but independent from, the repository's later Synthesis 26 reset-event analysis.

---

# Functional analogy

The following comparisons are **F — functional analogies only**. They do not assert historical influence or shared implementation lineage.

## F1 — Case 10: mode-entry authority versus internal refresh-cadence authority

Case 10's later Mobile-DRAM evidence shows that an external controller can request / exit self-refresh while effective cadence inside self-refresh belongs to the DRAM.

The SA-1100 witness adds a power-transition dimension:

```text
controller owns transition into preservation mode
    != controller must remain powered to execute preservation cadence
```

This is a functional comparison, not evidence that the SA-1100 sleep design derives from the Mobile-DDR TCSR implementations studied in Case 10.

## F2 — Case 86: retained memory payload versus whole-machine continuation

The SA-1100 can preserve DRAM contents across sleep even though ordinary processor / memory-controller execution state is reset and boot software runs again.

Functionally this resembles the repository's magnetic-core machine boundary:

```text
memory contents survive
    != machine execution resumes from identical live microstate
```

The substrates, historical contexts, and preservation mechanisms are unrelated unless separate genealogy evidence is found.

## F3 — Synthesis 26: typed reset persistence

Synthesis 26 argues that reset should not be treated as one scalar persistence horizon. SA-1100 gives a compact named-hardware illustration because software reset, sleep reset, and hardware reset intentionally preserve different classes of DRAM-related state.

This is supporting comparison, not retroactive evidence for every reset family covered by Synthesis 26.

---

# Philosophical interpretation

The following is **Φ — interpretation**, not an Intel historical claim.

A technical object's continuity need not mean that one complete mechanism remains continuously instantiated in one place. The SA-1100 sleep path preserves memory by changing the **organization of responsibility**:

```text
one regime maintains the payload
    ↓
that regime creates a safe handoff condition
    ↓
its ordinary control state disappears
    ↓
a different regime keeps the payload viable
    ↓
control is reconstructed and responsibility is handed back
```

The strongest bounded philosophical statement is therefore not `the same memory survives because its state is unchanged`.

It is:

> continuity can be maintained through an orderly transfer of preservation authority, provided enough boundary state remains to keep the payload valid while the ordinary controller is reconstructed.

That interpretation belongs to this repository. Intel's manual documents engineering behavior, not a philosophy of identity, memory, or persistence.

---

# Explicit non-claims

This slice **does not claim** any of the following:

- that the SA-1100 invented suspend-to-RAM or DRAM self-refresh;
- that Intel's 1998 draft was the first or final public description of the mechanism;
- that every shipping SA-1100 stepping behaved identically to every statement in the September-1998 draft;
- that self-refresh preserves DRAM without electrical power to the DRAM array;
- that ordinary controller registers are themselves nonvolatile;
- that sleep preserves CPU execution state, caches, DMA state, or peripheral state generally;
- that PSPR stores a complete memory-controller image;
- that reprogramming the controller reconstructs payload data;
- that hardware reset physically erases every DRAM cell at the instant reset is asserted; the bounded claim is Intel's documented system-level consequence that DRAM contents are lost under that reset path;
- that the sleep sequence guarantees survival under an arbitrarily fast or out-of-spec power collapse;
- that `VDD_FAULT` detection proves a particular analog hold-up energy margin;
- that SA-1100 CBR row progression and later SDRAM / LPDDR internal refresh mechanisms are electrically identical;
- that the functional comparisons above establish genealogy.

---

# Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| SA-1100 normal DRAM operation uses controller-timed CBR refresh | H/P | Intel §10.3.3 |
| Hardware reset clears the SA-1100 refresh counter while software reset does not | H/P | Intel §10.3.3 |
| Sleep entry finishes an in-progress memory operation before placing DRAM in self-refresh | H/P | Intel §9.5.3.3 |
| Ordinary internal reset follows establishment of DRAM self-refresh during sleep shutdown | H/P | Intel §9.5.3.3 |
| During sleep reset the memory controller can be in reset while RAS/CAS are still held in the DRAM self-refresh state | H/P | Intel §9.6 |
| Intel documents DRAM contents as preserved during sleep | H/P | Intel §9.5.3.7 |
| DRAM control registers lose power during sleep and must be reconfigured after wake | H/P | Intel §9.5.3.7 |
| DRAM remains held in self-refresh after wake until software has configured the interface and releases `DH` | H/P | Intel §9.5.7.5 + §10.7.1 |
| PSPR can retain a small configuration clue across sleep | H/P | Intel §9.5.7.6 |
| Software reset preserves DRAM refresh/configuration sufficiently for documented DRAM-content survival | H/P | Intel §9.6 |
| Hardware reset is documented to lose DRAM contents | H/P | Intel §9.6 |
| Post-sleep controller reconstruction is the same thing as reconstructing payload data | X | contradicted by documented retained DRAM contents + lost controller configuration |
| One undifferentiated `reset persistence` property describes software, sleep, and hardware reset | X | contradicted by Intel's reset-specific semantics |
| A preservation relation can outlive the ordinary controller state that established it | E | bounded reconstruction from self-refresh hold + controller reset |
| Full controller-state retention is unnecessary when safe payload maintenance continues and enough state exists to reconstruct valid control | E | bounded reconstruction; does not reduce correctness to PSPR alone |
| SA-1100 behavior proves genealogy to later LPDDR TCSR / self-refresh implementations | X | no genealogy evidence established |

---

# What this closes

This slice closes a bounded Case 03 debt that earlier controller evidence left implicit:

> **Can DRAM payload retention remain continuous even when the ordinary refresh-controller state itself is intentionally discarded across a power transition?**

For the documented SA-1100 sleep path, yes, because retention authority is handed to DRAM self-refresh before controller reset, the self-refresh relation is held across the reset / low-power interval, and controller state is rebuilt before that hold is released.

The resulting compact relation is:

```text
payload retention continuity
    != controller-state continuity

safe handoff to alternate maintenance authority
    + retained boundary / hold state
    + reconstructable controller configuration
    -> possible payload continuity across controller loss
```

---

# Remaining debt

The most useful next work is now narrower than another generic self-refresh source:

1. **named DRAM pairing** — identify a period SA-1100 board / design with a documented DRAM part and compare the controller sleep sequence against that device's exact self-refresh entry / exit contract;
2. **fault-window evidence** — find board-level or silicon-level tests that cut / disturb supplies at controlled points around sleep entry and wake release;
3. **hold-domain implementation** — find implementation or patent evidence for exactly which SA-1100 power domain drives the retained RAS/CAS hold and how its electrical margin was qualified;
4. **1999 final-manual facsimile cleanup** — obtain a directly renderable archived final Intel PDF if needed for line-for-line comparison against the inspected September-1998 draft;
5. **alternate-master handoff** — the same manual separately says an alternate memory-bus master must assume responsibility for DRAM integrity while SA-1100 cannot refresh; this deserves its own slice rather than being folded into the sleep-state argument;
6. **broader history** — StrongARM platform genealogy, suspend-to-RAM history, and low-power controller evolution belong primarily in `computing-archaeology`.

None of these debts blocks the bounded engineering result established here.