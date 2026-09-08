from pathlib import Path

CASE_PATH = Path('cases/129-dec-pdp8-power-fail-core-checkpoint-restart.md')
EVIDENCE_PATH = Path('evidence/129-dec-pdp8-1970-1974-power-fail-restart-grounding.md')
README_PATH = Path('README.md')
ROADMAP_PATH = Path('ROADMAP.md')
INDEX_PATH = Path('CASE_INDEX.md')
SELF_PATH = Path('scripts/integrate_case129_pdp8_power_fail.py')
WORKFLOW_PATH = Path('.github/workflows/integrate-case129-pdp8-power-fail.yml')

CASE = r'''# DEC PDP-8 Power-Fail Restart: Core-Resident Checkpoint Handoff Before Auto-Restart

**Status:** `grounded`

Grounding record: [`../evidence/129-dec-pdp8-1970-1974-power-fail-restart-grounding.md`](../evidence/129-dec-pdp8-1970-1974-power-fail-restart-grounding.md)

## Scope

This case asks one bounded retention question:

> If a computer's main magnetic-core memory can survive removal of operating power, what additional work is required for the *running computation* to survive a power interruption?

The principal historical object is Digital Equipment Corporation's **KP8-E Power-Fail and Auto-Restart** option for the PDP-8/E family, grounded in a 9 July 1971 engineering specification and the 1972–1974 PDP-8/E maintenance documentation. DEC's 1970 *Small Computer Handbook* supplies an earlier PDP-8/I `KP8/I` power-failure/restart witness and therefore a prior-art floor inside the same machine family.

The retention-specific focus is the handoff from short-lived processor state to memory state before power collapses:

```text
power-low detection
    -> interrupt request
    -> about 1 ms of continued powered operation
    -> software saves active CPU context into known memory locations
    -> operating power can disappear
    -> magnetic-core state remains
    -> power returns
    -> hardware restart sequence fetches from location 0000
    -> software restores context and resumes
```

This is not a general PDP-8 history, not a generic magnetic-core history, and not a claim that KP8-E invented power-failure checkpointing or automatic restart.

A fresh search of `tmzncty/computing-archaeology` found no dedicated `KP8-E` / PDP-8 power-fail-restart case to reuse. Broad PDP-8 engineering history, minicomputer power-fail genealogy, power-supply history, and peripheral-restart history belong there if developed.

## Historical vocabulary

Period/source vocabulary used by DEC includes:

- `POWER-FAIL AND AUTO-RESTART`;
- `PWR LOW` / `Power Low flag`;
- `interrupt request`;
- `SPL` (`Skip on PWR LOW flag`, IOT 6102);
- `power-fail routine`;
- `auto-restart logic`;
- `UP` and `DOWN`;
- `MEM START`;
- `known memory locations`;
- `core memory locations` in the 1970 PDP-8/I handbook;
- `location 0000` as the restart bootstrap location in the inspected PDP-8/E documentation.

Project engineering vocabulary used below:

- **checkpoint handoff** — transferring volatile execution context into a state expected to survive the coming interruption;
- **hold-up window** — the bounded interval of continued powered operation after failure detection;
- **restart bootstrap** — the small retained/control relation that re-enters software recovery after power returns;
- **resumption closure** — the point at which enough processor/software state has been re-established to continue the interrupted computation.

These project terms are analytical reconstructions. They are not projected backward as DEC's historical terminology.

## Historical record

### H/P — KP8-E detects falling line power and requests an interrupt

DEC's KP8-E maintenance chapter says the option monitors the computer's primary power source. If the monitored line drops below the selected minimum, the `PWR LOW` flip-flop is set and the OMNIBUS interrupt request is asserted.

The 9 July 1971 engineering specification states the same boundary more compactly: the lower threshold sets the Power Low flag, which generates an interrupt request; a separate upper threshold is used for restart as line power returns.

The hardware therefore does not itself contain the whole saved computation. Its first retention role is to create **advance warning and control transfer** while ordinary processor logic still has time to execute.

### H/P — power-supply capacitors preserve about 1 ms of operation, not the program by themselves

The PDP-8/E maintenance chapter explicitly states that filter capacitors in the power supply guarantee continued operation for **1 ms** after the low-power condition, sufficient for the interrupt request to be recognized and for the program interrupt routine to run. Because the window is limited, DEC says `SPL` should be the first status check in the interrupt routine.

The engineering specification likewise says that, after Power Low is set, the programmer has one millisecond of programming time before supply levels fall below operating levels.

This is a strong historical separation between:

```text
stored electrical energy
and
stored computational state
```

The capacitors retain enough **energy/time** for a transfer. They are not the long-lived embodiment of PC/AC/MQ/Link values.

### H/P — software must move active register state into memory before the window closes

The KP8-E maintenance chapter says the power-fail sequence protects the operating program by storing the contents of the `PC Register`, `AC Register`, `MQ Register`, and `Link` in known memory locations. The engineering specification qualifies the promise with the phrase **when properly programmed**.

This matters. The retained checkpoint is a hardware/software composition:

- hardware detects the condition and requests service;
- residual supply energy keeps the machine alive briefly;
- software recognizes `PWR LOW` and performs the state transfer;
- memory then carries the state across the interval in which processor registers no longer can.

### H/P — the PDP-8/E standard memory is magnetic core

DEC's September 1973 PDP-8/E processor maintenance manual describes the standard `MM8-E` memory as a random-access, coincident-current, magnetic READ/WRITE core memory, with a basic 4K × 12-bit organization.

The KP8-E chapter itself says only `known memory locations`, so this case does **not** claim that every possible KP8-E installation was forced to use one specific memory technology. The core-specific reconstruction is bounded to the standard MM8-E-equipped PDP-8/E configuration and is independently strengthened by the earlier PDP-8/I handbook, which explicitly says its power-fail program stores active registers and the program count in designated **core memory locations**.

### H/P — auto-restart begins at a known bootstrap location rather than reconstructing volatile context by magic

The PDP-8/E maintenance chapter says that resumption must begin by executing the instruction the power-fail routine stored in **location 0000, field 0**. The auto-restart logic sets up processor state for a FETCH cycle and ultimately asserts `MEM START`, causing the computer to fetch the instruction at location 0000.

The chapter also states that if the hardware ENABLE/DISABLE switch is disabled, the low-power flag can clear when power returns but the program must be restarted manually.

Thus:

> **automatic restart authority is separate from checkpoint content.**

The restart circuit supplies a deterministic entry point. Software still has to arrange a useful instruction there and restore the saved execution state.

### H/P — return of line power has its own admission delay

After `UP` is asserted on restored power, the PDP-8/E auto-restart sequence waits about **1500 ms** before beginning the CPU restart choreography. DEC explains that this interval allows system equipment to complete operations initiated by OMNIBUS `INITIALIZE`.

This is not a claim that every peripheral has recovered its exact pre-failure state. It is a separate **restart-admission delay** before processor execution resumes.

### H/P — even a short power disturbance can trigger the whole sequence

The maintenance text notes that the power-fail sequence is carried out even if line power recovers almost instantaneously after the low condition is detected. Detection therefore crosses a control boundary: a brief excursion can commit the machine to the shutdown/restart choreography even when the external condition disappears quickly.

### H/P — the same retention relation predates KP8-E inside the PDP-8 family

DEC's 1970 *Small Computer Handbook*, §6-2, documents the earlier `KP8/I [KP8/L]` Power Failure Detection and Restart option. It says the option provides roughly 1 ms of continued operation, directs software to save active registers and the program count in designated **core memory locations**, places a restart transfer at address 0000, and after power restoration runs a subroutine that restores the active registers and continues the interrupted program.

Therefore the safe historical statement is:

> **KP8-E documents a PDP-8/E implementation of an already documented PDP-8-family power-fail/restart relation; it is not an origin claim.**

## Retained state

The bounded system contains several different state classes:

1. **volatile active CPU state** — PC, AC, MQ where applicable, Link, interrupt/control context;
2. **power-low indication/control state** — meaningful only while enough logic remains powered to act on it;
3. **core-resident checkpoint words** — software-created representations of execution context intended to survive the outage;
4. **restart-bootstrap word at location 0000** — an entry relation that redirects the restarted processor into recovery software;
5. **ordinary program/data already resident in nonvolatile core**;
6. **hardware configuration/authority** — including whether automatic restart is enabled;
7. **peripheral/device state** — not automatically equivalent to any of the above.

The central mistake this case blocks is treating item 5 — `core is nonvolatile` — as if it automatically implied survival of items 1, 3, 4, and 7.

## Physical / logical substrate

For the standard core-memory configuration:

```text
active register values
    embodied in powered processor logic
        |
        | power-low interrupt + software save
        v
selected MM8-E/PDP-8-family core words
    embodied in remanent ferrite state
        |
        | power removed / restored
        v
restart fetch from 0000
        |
        v
software reloads architectural state
```

The retained computation therefore changes embodiment **before** the failure transition completes.

## Retention mechanism

Several mechanisms compose rather than collapse into one:

### Magnetic remanence

Core memory can retain written bits without continuous operating power. Case 02 grounds the element-level remanence/destructive-read relation separately.

### Advance failure detection

The KP8 option monitors line power soon enough to request an interrupt before normal operating levels disappear.

### Energy hold-up

Filter capacitors keep processor logic usable for roughly one millisecond after the low-power condition.

### Software state serialization

The interrupt routine converts live register state into memory words at known locations.

### Deterministic restart bootstrap

After power returns and startup timing completes, the auto-restart logic fetches from a defined location so software can restore the saved state.

None of these alone is the whole retention mechanism for **resumable computation**.

## Addressing and access geometry

Checkpoint recovery depends on fixed conventions:

- the interrupt path must test `PWR LOW` promptly;
- software must know where checkpoint words are stored;
- restart logic enters through location 0000 in the inspected PDP-8/E documentation;
- the instruction at that location must direct execution into the recovery routine;
- recovery software must know how to map saved words back into architectural registers.

A physically surviving core word that no longer has a valid role in this convention is not, by itself, a resumable computation.

## Read semantics

At the core-device layer, Case 02 already shows classic destructive read and rewrite. This case does not repeat that mechanism.

At the restart layer, the important read is the **bootstrap fetch** from location 0000. Fetching that word does not itself restore the interrupted architectural state; it only begins the procedure that can do so.

Thus:

> **restart fetch ≠ restored execution context.**

## Write and erasure semantics

The power-fail routine must deliberately overwrite designated checkpoint locations with the newest active context before power falls too far. It may also place/relocate the restart transfer at location 0000.

An older checkpoint can therefore be logically superseded by a newer one without any need for a Flash-like erase operation. Conversely, if the save routine never finishes, surviving older core contents can remain physically readable while failing to describe the interrupted computation.

## Time

This case separates at least five clocks:

1. **line-failure detection time** — threshold crossing and interrupt assertion;
2. **hold-up window** — about 1 ms of continued operation available for shutdown software;
3. **core retention interval** — the nonpowered interval over which saved core state remains usable;
4. **restart-admission delay** — about 1.5 s after `UP` in the PDP-8/E sequence before CPU restart choreography proceeds;
5. **software restoration time** — the later interval needed to reload state and reach the interrupted computation.

`1 ms` is therefore not the memory's shelf-life specification, and `1.5 s` is not the retention interval of the checkpoint.

## Maintenance and labor

Persistence here depends on work performed before and after the outage:

- power-supply design must provide the promised hold-up interval;
- threshold hardware must detect failure early enough;
- the programmer must install a power-fail routine and put `SPL` early enough in the interrupt chain;
- the routine must save all state required by the intended application;
- restart location 0000 must contain a meaningful recovery transfer;
- auto-restart must be enabled when unattended restart is desired;
- peripheral/device behavior across `INITIALIZE` must be understood by system software/operators;
- maintenance personnel must keep the power-fail option itself working.

Core remanence reduces one physical retention burden. It does not remove this system labor.

## Failure / forgetting modes

Distinct failure modes include:

- the falling-power event is not detected early enough;
- hold-up energy is insufficient to complete the software save;
- the interrupt routine checks another condition first and consumes too much of the 1 ms window;
- required architectural state is omitted from the checkpoint;
- checkpoint locations or the restart word are overwritten/corrupted;
- core state survives but sense/write/control electronics fail after power returns;
- automatic restart is disabled;
- restart executes a stale or invalid recovery transfer;
- peripheral state is reset or diverges even though CPU/core state survives;
- software restores a syntactically valid but semantically inconsistent execution context.

These are not one generic event called `memory loss`.

## Engineering reconstruction

The bounded mechanism supports this relation:

```text
nonvolatile main-memory payload
    + early power-fail detection
    + bounded hold-up energy/time
    + successful software transfer of volatile CPU state
    + retained restart bootstrap
    + usable restart hardware
    + recovery software
    -> possible computation resumption
```

This yields the following project conclusions:

> **core nonvolatility ≠ CPU-context survival.**

> **power-fail detection ≠ checkpoint completion.**

> **hold-up energy ≠ retained payload.**

> **checkpoint presence ≠ automatic restart authority.**

> **automatic restart ≠ exact hardware continuation at the interrupted instruction.**

> **processor resumption ≠ peripheral-state continuity.**

The case is especially valuable because the transition crosses two retention regimes: volatile processor state is deliberately translated into nonvolatile core state while enough residual energy remains to perform the translation.

## Prior art and genealogy boundary

The directly inspected 1970 DEC handbook already documents the KP8/I/KP8/L form of the same broad power-fail/restart relation before the 1971 KP8-E engineering specification.

This case therefore rejects:

- `KP8-E invented power-failure restart`;
- `PDP-8 invented checkpointing`;
- `magnetic core naturally implied automatic restart`.

A complete genealogy of power-fail interrupts, battery/hold-up supply, restart vectors, process checkpointing, UPS systems, and later nonvolatile processor state remains outside this slice.

## Functional comparisons, not genealogy

### Case 02 — magnetic-core destructive read

Case 02 explains why a core bit can remain without power yet require restore after destructive access. Case 129 begins one level higher: **which machine state must first be moved into those durable core bits before power disappears?**

Functional relation only:

> **nonvolatile element ≠ restartable system.**

### Case 06 — powered flip-flop working retention

Processor registers are a powered working-state regime. Case 129 shows that a system can preserve their *logical values* by changing substrate before the powered regime ends.

Functional relation only; no claim that all PDP-8 registers use the exact flip-flop circuits studied in Case 06.

### Case 15 — Intel SSD 320 power-loss protection

Both cases use stored electrical energy to buy time for a state transfer during power failure. But their mechanisms, controllers, media, interfaces, and historical lineages differ radically.

The useful comparison is narrow:

> **stored energy can be retention infrastructure without being the retained payload.**

### Case 127 — DRAM power-off remanence

Case 127 studies residual physical recoverability after a volatile-maintenance regime stops. Case 129 instead uses an **engineered pre-failure transfer** into a nonvolatile substrate.

Thus:

> **residual remanence ≠ checkpoint protocol.**

## Philosophical / media-theoretical interpretation

**Philosophical interpretation, not historical vocabulary:** this case makes technical persistence look less like an object's passive refusal to disappear and more like an anticipatory **handoff of identity across a failure boundary**. The computation survives only if the system recognizes that one embodiment is about to become unavailable and translates enough relations into another embodiment before the transition closes.

The philosophical limit is equally important: this mechanism does not show that every form of memory is checkpointing, nor that continuity of computation is identical to cultural or human memory. It is a bounded technical counterexample to the intuition that nonvolatile storage alone is sufficient for continuity.

## Counterexamples and limits

This case does **not** establish:

- a universal 1 ms power-fail window for PDP-8 systems or other computers;
- that every KP8-E installation necessarily used MM8-E core memory;
- that every peripheral resumes exactly where it stopped;
- that the power-fail routine captures every possible device/controller state;
- that auto-restart proves application-level consistency;
- that a brief outage can never corrupt state despite the documented sequence;
- that DEC originated the general idea of power-fail save/restart;
- that a historical PDP-8 operator called the saved words a `checkpoint`.

## Related repositories

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — broad PDP-8, minicomputer, power-supply, core-memory, and restart engineering history belongs here if developed. A fresh search found no dedicated KP8-E case to reuse.
- [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) — supplies the anti-anachronism rule used here: `checkpoint handoff` is current project vocabulary, not projected onto DEC engineers.

## Sources

Primary sources used in the grounding record:

1. Digital Equipment Corporation, **PDP-8/E Maintenance Manual, Volume 2: Internal Bus Options**, Chapter 7, `KP8-E Power-Fail and Auto-Restart`, 1972–1974 printing lineage; surviving chapter extract: <https://deramp.com/downloads/mfe_archive/011-Digital%20Equipment%20Corporation/02%20PDP-8e/03%20PDP-8e%20Options/KP8-E%20M848%20Power%20Fail%20Detect/01%20KP8-E%20Documentation/KP8-E%20Documentation.pdf>.
2. Digital Equipment Corporation, **Engineering Specification: Power Fail and Auto-Restart, KP8/E**, A-SP-KP8-E-1, dated 9 July 1971, rev. A 16 July 1971; surviving drawing/specification set: <https://deramp.com/downloads/mfe_archive/011-Digital%20Equipment%20Corporation/02%20PDP-8e/03%20PDP-8e%20Options/KP8-E%20M848%20Power%20Fail%20Detect/01%20KP8-E%20Documentation/KP8-E_PwrFail_EngrDrws_May73.pdf>.
3. Digital Equipment Corporation, **Small Computer Handbook, 1970 Edition**, §6-2 `Power Failure Detection and Restart KP8/I [KP8/L]`: <https://bitsavers.org/pdf/dec/pdp8/handbooks/SmallComputerHandbook_1970.pdf>.
4. Digital Equipment Corporation, **PDP-8/E Maintenance Manual, Volume 1: Processor**, September 1973, standard `MM8-E` core-memory description: <https://bitsavers.org/pdf/dec/pdp8/pdp8e/DEC-8E-HMM1A-D-D_PDP-8e_Maintenance_Manual_Volume_1_Processor_Sep73.pdf>.
'''

EVIDENCE = r'''# Evidence 129 — DEC PDP-8 power-fail / auto-restart grounding, 1970–1974

**Case:** [`cases/129-dec-pdp8-power-fail-core-checkpoint-restart.md`](../cases/129-dec-pdp8-power-fail-core-checkpoint-restart.md)

## Research question

What primary evidence supports the bounded claim that PDP-8 power-fail/restart continuity required a timed handoff from volatile processor state into memory state before supply collapse, followed by a separate restart bootstrap after power returned?

## Evidence discipline

This record distinguishes:

- `H/P` — historical/primary source statement;
- `H/S` — later or institutional historical witness;
- `E` — project engineering reconstruction;
- `A` — functional analogy;
- `I` — philosophical interpretation;
- `X` — rejected/unsupported overclaim.

The central historical vocabulary is DEC's: `Power Low flag`, `SPL`, `power-fail routine`, `known memory locations`, `core memory locations`, `auto-restart`, and location `0000`. `Checkpoint handoff`, `hold-up window`, and `resumption closure` are project terms only.

## Source P1 — DEC PDP-8/E Maintenance Manual, Volume 2, Chapter 7

Surviving DEC-authored chapter extract:

<https://deramp.com/downloads/mfe_archive/011-Digital%20Equipment%20Corporation/02%20PDP-8e/03%20PDP-8e%20Options/KP8-E%20M848%20Power%20Fail%20Detect/01%20KP8-E%20Documentation/KP8-E%20Documentation.pdf>

Document family: `DEC-8E-HR2C-D` / PDP-8/E internal-options maintenance material, Chapter 7, `KP8-E POWER-FAIL AND AUTO-RESTART`. The inspected archive is a page-preserving scan/extract; the broader Volume 2 printing lineage reaches the 1972–1974 maintenance-manual editions.

### P1.1 — controlled shutdown and saved active registers

Printed p. 7-1 says the option monitors primary power and initiates a controlled shutdown on failure. It states that the power-fail sequence protects the operating program by storing the contents of the PC, AC, MQ, and Link in known memory locations.

**Supports:** active processor context must be transferred into memory before ordinary operation stops. (`H/P`)

**Does not support:** that the KP8-E hardware itself serializes every register without software. The same page says the interrupt routine must carry out the power-fail routine. (`X`)

### P1.2 — 1 ms continued-operation window

Printed p. 7-1 states that power-supply filter capacitors guarantee continued operation for **1 ms**, enough for the interrupt request to be recognized and the program interrupt routine to execute. It explicitly says `SPL` 6102 should be the first status check because of the time limitation.

**Supports:** retained electrical energy buys a bounded execution window for state transfer. (`H/P`, `E`)

**Does not support:** one millisecond as the retention lifetime of magnetic core. (`X`)

### P1.3 — low-power flag and interrupt are control state, not checkpoint payload

The same section says the monitor sets `PWR LOW` and asserts the OMNIBUS interrupt request when voltage is below the selected minimum.

**Supports:** failure detection/control transfer precede software checkpoint work. (`H/P`, `E`)

### P1.4 — a short excursion can commit the sequence

Printed p. 7-2 says that even if line power recovers almost instantaneously, the power-fail sequence is carried out once the monitor detects the qualifying missing/low half-cycle.

**Supports:** threshold-crossing can commit the system to a retention/restart protocol even when the external disturbance is brief. (`H/P`)

### P1.5 — restart begins from the word the power-fail routine placed at 0000

Printed p. 7-4 says the computer must resume by executing the instruction stored at location `0000`, field 0, by the power-fail routine. The auto-restart logic prepares CPMA/major-state and optional IF/DF state so timing restarts in FETCH.

Printed pp. 7-5–7-6 describe the later `MEM START` assertion and fetch from location `0000`.

**Supports:** restart authority and saved execution payload are different state relations. (`H/P`, `E`)

**Does not support:** that fetching location 0000 alone has already restored all interrupted state. (`X`)

### P1.6 — restart can be disabled

Printed p. 7-6 says that if the ENABLE/DISABLE switch is in `DISABLE`, PWR LOW clears when AC returns but the program must be restarted manually.

**Supports:** checkpoint survival does not itself imply automatic restart authority. (`H/P`, `E`)

### P1.7 — 1500 ms restart admission delay

Printed p. 7-6 says `UP` triggers a 1500 ms interval during which system equipment can complete operations initiated by OMNIBUS `INITIALIZE`; only later does CPU restart sequencing proceed.

**Supports:** return of power, peripheral initialization opportunity, and processor execution restart are separate temporal boundaries. (`H/P`, `E`)

**Does not support:** exact restoration of all peripheral pre-failure state. (`X`)

## Source P2 — DEC Engineering Specification, KP8/E, 9 July 1971

Surviving DEC drawing/specification set:

<https://deramp.com/downloads/mfe_archive/011-Digital%20Equipment%20Corporation/02%20PDP-8e/03%20PDP-8e%20Options/KP8-E%20M848%20Power%20Fail%20Detect/01%20KP8-E%20Documentation/KP8-E_PwrFail_EngrDrws_May73.pdf>

The inspected Engineering Specification is titled `POWER FAIL AND AUTO-RESTART, KP8/E`, dated **7/9/71**, with revision A marked `REVISED & RETYPED` on 7/16/71.

### P2.1 — `when properly programmed`

The Overall Description says the option, **when properly programmed**, prevents loss of the contents of active registers in an AC power failure and restarts the computer when AC power is restored.

**Supports:** software arrangement is part of the retention contract; the hardware option is not a self-sufficient register archive. (`H/P`, `E`)

### P2.2 — separate falling and rising thresholds

General Specifications state that an upper threshold restarts the computer while a lower threshold sets the Power Low flag and generates an interrupt request.

**Supports:** shutdown admission and restart admission are distinct threshold/control relations. (`H/P`)

### P2.3 — SPL first and one millisecond available

Programming §§3.1–3.3 define `SPL` 6102 as `Skip if Power Low Flag = 1`, say it should be first in the interrupt-service skip chain, and state that when Power Low is set the programmer has **one millisecond** before power-supply levels fall below operating levels.

**Supports:** software scheduling latency is part of the power-fail retention budget. (`H/P`, `E`)

### P2.4 — automatic restart is a separately enabled policy

Programming §3.4 says the enable/disable switch can prevent computer restart when power returns.

**Supports:** restart policy/authority is separate from saved state. (`H/P`, `E`)

## Source P3 — DEC Small Computer Handbook, 1970 Edition, §6-2

<https://bitsavers.org/pdf/dec/pdp8/handbooks/SmallComputerHandbook_1970.pdf>

Section 6-2 is titled `POWER FAILURE DETECTION AND RESTART KP8/I [KP8/L]`.

### P3.1 — earlier PDP-8-family core-memory checkpoint

The handbook says the power-fail option permits about 1 ms of continued operation. It instructs the interrupt routine to detect the Power Low condition and store active registers and the program count in designated **core memory locations**.

**Supports:** the volatile-register -> core-memory handoff is directly documented before KP8-E. (`H/P`)

### P3.2 — location 0000 is prepared as restart bootstrap

The handbook's sample power-fail sequence saves the program count and deposits a restart transfer at location 0000. It then describes the power-restore subroutine restoring active registers and continuing the interrupted program.

**Supports:** saved context, restart transfer, and later restoration are distinct phases. (`H/P`, `E`)

### P3.3 — prior-art boundary

Because this directly inspected 1970 handbook precedes the 9 July 1971 KP8-E engineering specification, KP8-E cannot be presented here as the first PDP-8-family expression of the relation.

**Supports:** conservative prior-art floor only. (`H/P`, `X`)

**Does not support:** DEC-wide or industry-wide invention priority. (`X`)

## Source P4 — DEC PDP-8/E Maintenance Manual, Volume 1, September 1973

<https://bitsavers.org/pdf/dec/pdp8/pdp8e/DEC-8E-HMM1A-D-D_PDP-8e_Maintenance_Manual_Volume_1_Processor_Sep73.pdf>

The standard PDP-8/E memory section describes `MM8-E` as a random-access, coincident-current, magnetic READ/WRITE **core memory**, with a basic 4096 × 12-bit organization.

**Supports:** the standard PDP-8/E configuration supplies the nonvolatile core substrate used for the core-specific engineering reconstruction. (`H/P`)

**Boundary:** P1 says `known memory locations`, not `MM8-E-only`. This case therefore does not universalize one memory technology across every possible KP8-E installation. (`X`)

## Source P5 — archived KP8-E engineering drawings / option evidence

The same P2 drawing set includes a DEC master drawing list and M848 power-fail/auto-restart circuit drawings. The master list records `POWER FAIL AND AUTO-RESTART` as the KP8-E option and shows PDP-8/E use; the engineering drawing set supplies the historical hardware artifact context for the specification.

**Supports:** this is a concrete option implementation/document family, not merely a later textbook thought experiment. (`H/P`)

**Boundary:** circuit presence does not by itself prove field reliability or successful checkpoint completion under every outage waveform. (`X`)

## Claim matrix

| ID | Claim | Label | Best source | Strength / boundary |
| --- | --- | --- | --- | --- |
| G-129.1 | KP8-E power-low detection generates an interrupt before operating power disappears | `H/P` | P1, P2 | direct DEC description |
| G-129.2 | filter capacitors provide about 1 ms continued operation | `H/P` | P1, P2 | direct DEC timing statement |
| G-129.3 | SPL should be tested first because the save window is bounded | `H/P` | P1, P2 | direct programming requirement |
| G-129.4 | PC/AC/MQ/Link are stored in known memory locations during power-fail handling | `H/P` | P1 | direct DEC maintenance statement |
| G-129.5 | automatic restart fetches from a power-fail-prepared location 0000 | `H/P` | P1 | direct restart mechanism |
| G-129.6 | automatic restart can be disabled independently | `H/P` | P1, P2 | direct policy/control distinction |
| G-129.7 | restart waits about 1500 ms for initialization-related operations | `H/P` | P1 | direct timing statement |
| G-129.8 | 1970 KP8/I docs already place saved active state in core memory and restore it later | `H/P` | P3 | direct earlier witness |
| G-129.9 | standard PDP-8/E MM8-E is magnetic core memory | `H/P` | P4 | direct machine-specific substrate witness |
| G-129.10 | core nonvolatility alone preserves volatile CPU-register context | `X` | P1/P3 mechanism | rejected |
| G-129.11 | 1 ms hold-up energy is itself the saved program state | `X` | P1/P2 | rejected |
| G-129.12 | restart fetch at 0000 equals full state restoration | `X` | P1/P3 | rejected |
| G-129.13 | successful CPU auto-restart proves all peripheral state survived | `X` | P1 scope boundary | rejected |
| G-129.14 | KP8-E invented power-failure checkpoint/restart | `X` | P3 chronology | rejected |

## Engineering reconstruction

The primary sources support this bounded decomposition:

```text
volatile execution context
    -> falling-power detection
    -> interrupt admission
    -> bounded hold-up execution budget
    -> software writes context into memory
    -> nonpowered retention interval
    -> rising-power restart admission
    -> fixed bootstrap fetch
    -> software restores context
    -> possible resumed computation
```

Project reconstructions, not source quotations:

- `core nonvolatility ≠ CPU-context survival`;
- `power-fail detection ≠ checkpoint completion`;
- `hold-up energy ≠ retained payload`;
- `checkpoint state ≠ restart authority`;
- `restart bootstrap ≠ restored execution context`;
- `processor resumption ≠ peripheral-state continuity`;
- `brief power recovery ≠ cancellation of an already-entered failure protocol`.

## Functional comparisons, not genealogy

- **Case 02 / magnetic core:** element-level remanence and destructive-read restore are necessary background, but they do not explain how volatile processor state becomes restartable.
- **Case 06 / flip-flop:** powered working state can preserve its logical value across outage only by changing embodiment; no exact circuit identity is claimed.
- **Case 15 / Intel SSD 320:** both use stored energy to complete a failure-triggered state transfer, but PDP-8 software-to-core and SSD controller-to-NAND are historically and technically different.
- **Case 127 / DRAM remanence:** accidental/residual recoverability after maintenance withdrawal differs from a deliberate pre-failure save protocol.

## Related-repository check

Fresh GitHub searches for `KP8-E` in both `tmzncty/technical-retention` and `tmzncty/computing-archaeology` returned no existing dedicated case before this integration.

Broad PDP-8 / minicomputer architecture, power-supply engineering, power-fail interrupt genealogy, and field-service history should be built primarily in `computing-archaeology` if pursued. This record retains only the bounded state-handoff/restart relation.

## Open gaps

This slice intentionally leaves open:

- direct inspection of the earliest 1968 KP8/I option document listed in surviving PDP-8 archives;
- power-fail/restart mechanisms before DEC's PDP-8 family;
- exact field failure rates and oscilloscope/fault-injection traces for KP8-E;
- peripheral-specific restart semantics across Teletype, disk, tape, communications, and real-time I/O;
- later PDP-8/E semiconductor-memory configurations and whether/how restart assumptions changed;
- complete DEC option-revision genealogy;
- broader UPS, battery-backed memory, process checkpointing, and nonvolatile CPU-state history.

Those gaps must not be inferred closed from this case.
'''

README_TABLE = '| [DEC PDP-8 Power-Fail Restart: Core-Resident Checkpoint Handoff Before Auto-Restart](cases/129-dec-pdp8-power-fail-core-checkpoint-restart.md) | **grounded** | falling-power detection + ~1 ms hold-up + software-saved PC/AC/MQ/Link + memory-resident checkpoint/restart bootstrap + delayed restart fetch at 0000 | separate core nonvolatility, volatile CPU context, failure detection, checkpoint completion, hold-up infrastructure, restart authority, software restoration, and peripheral readiness | [1970–1974 grounding record](evidence/129-dec-pdp8-1970-1974-power-fail-restart-grounding.md); pre-DEC genealogy, earliest 1968 KP8/I source, field fault traces, peripheral recovery, and later memory-option evolution remain open |'

README_BULLET = '- [`cases/129-dec-pdp8-power-fail-core-checkpoint-restart.md`](cases/129-dec-pdp8-power-fail-core-checkpoint-restart.md) — grounded PDP-8 power-fail/restart bridge: falling-power detection and a roughly 1 ms hold-up window let software transfer volatile execution context into memory before supply collapse; auto-restart later fetches from location 0000 and re-enters software restoration, making core nonvolatility, checkpoint completion, restart authority, and resumed service distinct relations. See [`evidence/129-dec-pdp8-1970-1974-power-fail-restart-grounding.md`](evidence/129-dec-pdp8-1970-1974-power-fail-restart-grounding.md).'

ROADMAP_BULLET = '- [x] DEC PDP-8 power-fail / auto-restart core-checkpoint handoff — [`cases/129-dec-pdp8-power-fail-core-checkpoint-restart.md`](cases/129-dec-pdp8-power-fail-core-checkpoint-restart.md), grounded by [`evidence/129-dec-pdp8-1970-1974-power-fail-restart-grounding.md`](evidence/129-dec-pdp8-1970-1974-power-fail-restart-grounding.md): DEC\'s 1970 PDP-8/I handbook already documents a roughly 1 ms power-fail window in which software stores active registers/program count in designated core-memory locations and prepares address 0000 for restore; the 9-Jul-1971 KP8-E engineering specification and 1972–1974 PDP-8/E maintenance material separate lower-threshold interrupt admission, bounded filter-capacitor hold-up, properly programmed save work, nonvolatile memory state, a separately enabled auto-restart path, and a ~1500 ms restart-admission delay. This closes only the bounded `core nonvolatility vs volatile CPU context vs failure detection vs checkpoint completion vs hold-up infrastructure vs restart bootstrap` relation; pre-DEC genealogy, 1968 KP8/I facsimile inspection, peripheral-state recovery, later semiconductor-memory configurations, and fault injection remain open.'

INDEX_SECTION = r'''## Case 129 — DEC PDP-8 power-fail / auto-restart findings

- **2239 — core-memory nonvolatility ≠ volatile CPU-context survival:** remanent program/data words can outlive power while PC/AC/MQ/Link still require an explicit transfer into memory before powered processor state disappears. (`H/P`, `E`)
- **2240 — power-fail detection ≠ checkpoint completion:** setting `PWR LOW` and requesting an interrupt only opens the save path; software must still recognize the condition and write required state within the bounded window. (`H/P`, `E`)
- **2241 — one-millisecond hold-up ≠ one-millisecond memory retention:** DEC's ~1 ms figure is continued powered execution time provided by filter capacitors, not the shelf-life of magnetic core. (`H/P`, `E`, `X`)
- **2242 — hold-up energy ≠ retained payload:** capacitors preserve enough electrical energy to perform the state transfer; the architectural values themselves are retained later in memory. (`H/P`, `E`)
- **2243 — interrupt request ≠ power-fail routine execution:** `SPL` must be reached promptly, and DEC explicitly warns that the time limit makes interrupt-service ordering part of the retention contract. (`H/P`, `E`)
- **2244 — checkpoint words ≠ active-register embodiment:** after the save, the same logical PC/AC/MQ/Link values have changed physical/logical embodiment from powered processor state to memory words. (`E`)
- **2245 — surviving program payload ≠ resumable computation:** ordinary core-resident instructions/data can survive while the machine still lacks the latest volatile execution context or a valid restart bootstrap. (`H/P`, `E`)
- **2246 — restart bootstrap ≠ saved execution context:** location `0000` provides a deterministic re-entry relation; it is not a complete copy of all interrupted register state. (`H/P`, `E`)
- **2247 — automatic restart ≠ hardware-only continuation at the interrupted instruction:** PDP-8/E restart logic establishes a FETCH from 0000, after which software restoration is still required. (`H/P`, `E`, `X`)
- **2248 — checkpoint survival ≠ automatic-restart authority:** the enable/disable switch can suppress automatic restart even when memory contents remain. (`H/P`, `E`)
- **2249 — restored line power ≠ immediate service admission:** the PDP-8/E path retains a ~1500 ms interval for initialization-related equipment operations before CPU restart sequencing proceeds. (`H/P`, `E`)
- **2250 — processor resumption ≠ peripheral-state continuity:** DEC's restart delay gives system equipment time to respond to initialization; it does not establish exact preservation of every peripheral's pre-failure state. (`H/P`, `E`, `X`)
- **2251 — brief power recovery ≠ cancellation of an entered failure protocol:** the maintenance manual says the power-fail sequence proceeds even if line power recovers almost immediately after the qualifying low condition. (`H/P`)
- **2252 — magnetic-core remanence ≠ maintenance-free restart:** reliable continuity also requires threshold detection, hold-up supply behavior, interrupt scheduling, save software, restart wiring/logic, recovery code, and working post-power electronics. (`H/P`, `E`)
- **2253 — KP8-E 1971 ≠ origin of the PDP-8-family relation:** DEC's directly inspected 1970 KP8/I/KP8/L handbook already documents the ~1 ms save window, designated core-memory locations, address-0000 restart transfer, and later register restoration. (`H/P`, `X`)
- **2254 — PDP-8 hold-up comparison ≠ SSD power-loss-protection genealogy:** Case 15 and Case 129 both use stored energy to complete a failure-triggered transfer, but software-to-core and controller-to-NAND are different mechanisms and histories. (`A`, `X`)
- **2255 — DRAM residual remanence ≠ engineered pre-failure checkpoint:** Case 127 studies state that remains after maintenance/power withdrawal; Case 129 deliberately changes embodiment before power disappears far enough to stop execution. (`A`, `E`)
- **2256 — related-repository boundary:** fresh searches found no dedicated `KP8-E` case in `tmzncty/computing-archaeology`; broad PDP-8, minicomputer power-fail, power-supply, and restart genealogy belongs there if developed, while Case 129 remains bounded to the retention handoff/restart relation. (`H/P` project-state record)
'''


def insert_after_unique(lines, predicate, new_line, label):
    pos = [i for i, line in enumerate(lines) if predicate(line)]
    if len(pos) != 1:
        raise SystemExit(f'Expected exactly one {label} anchor, found {len(pos)}')
    lines.insert(pos[0] + 1, new_line)


if CASE_PATH.exists() or EVIDENCE_PATH.exists():
    raise SystemExit('Case 129 files already exist; refusing duplicate integration')

CASE_PATH.write_text(CASE.rstrip() + '\n', encoding='utf-8')
EVIDENCE_PATH.write_text(EVIDENCE.rstrip() + '\n', encoding='utf-8')

# README table and compact navigation list.
readme = README_PATH.read_text(encoding='utf-8')
if '129-dec-pdp8-power-fail-core-checkpoint-restart.md' in readme:
    raise SystemExit('README already contains Case 129')
rlines = readme.splitlines()
insert_after_unique(
    rlines,
    lambda line: line.startswith('| [') and '(cases/128-zfs-vdev-label-uberblock-import-root-recovery.md)' in line,
    README_TABLE,
    'README table Case 128',
)
insert_after_unique(
    rlines,
    lambda line: line.startswith('- [`cases/') and '(cases/128-zfs-vdev-label-uberblock-import-root-recovery.md)' in line,
    README_BULLET,
    'README compact-nav Case 128',
)
README_PATH.write_text('\n'.join(rlines) + '\n', encoding='utf-8')

# Phase-2 status/navigation entry.
roadmap = ROADMAP_PATH.read_text(encoding='utf-8')
if '129-dec-pdp8-power-fail-core-checkpoint-restart.md' in roadmap:
    raise SystemExit('ROADMAP already contains Case 129')
rmlines = roadmap.splitlines()
insert_after_unique(
    rmlines,
    lambda line: line.startswith('- [x]') and '(cases/128-zfs-vdev-label-uberblock-import-root-recovery.md)' in line,
    ROADMAP_BULLET,
    'ROADMAP Case 128',
)
ROADMAP_PATH.write_text('\n'.join(rmlines) + '\n', encoding='utf-8')

# Append findings only if the current authoritative tail is Case 128 / 2238.
index = INDEX_PATH.read_text(encoding='utf-8').rstrip()
if '## Case 129 — DEC PDP-8 power-fail / auto-restart findings' in index:
    raise SystemExit('CASE_INDEX already contains Case 129')
if '**2238 — related-repository boundary:**' not in index:
    raise SystemExit('CASE_INDEX expected current finding 2238 not found')
if any(f'**{n} —' in index for n in range(2239, 2257)):
    raise SystemExit('CASE_INDEX finding-number collision in 2239–2256')
INDEX_PATH.write_text(index + '\n\n' + INDEX_SECTION.rstrip() + '\n', encoding='utf-8')

# One-shot integration infrastructure must not survive the research commit.
if SELF_PATH.exists():
    SELF_PATH.unlink()
if WORKFLOW_PATH.exists():
    WORKFLOW_PATH.unlink()
