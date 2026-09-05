# Grounding Record 86 — DEC PDP-8 Core-Resident Power-Fail Save and Automatic Restart, 1960–1970

**Supports:** [`../cases/86-dec-pdp8-core-power-fail-auto-restart.md`](../cases/86-dec-pdp8-core-power-fail-auto-restart.md)  
**Status:** `grounded`  
**Research question:** What primary evidence shows that magnetic-core content survival and whole-computer program continuation were separate retention problems, and how did DEC's PDP-8 KR01 bridge them?

## Why this slice was chosen

Case 02 already establishes classic magnetic-core remanence, destructive read, restore, and the explicit limit that **nonvolatile core does not imply whole-system crash/restart persistence**. Case 70 separately deepens half-select disturbance. The remaining bounded question is therefore not another history of ferrite cores; it is the system boundary:

> What must be preserved when the memory array can survive power loss but the currently executing processor state does not automatically survive with it?

A repository search found no dedicated PDP-8 power-fail/automatic-restart slice in `technical-retention` or `computing-archaeology`. This record therefore adds the retention-specific evidence while linking back to the companion repository for general core-memory history.

---

## Source ledger

### A — DEC PDP-8 Users Handbook, March 1966

**Source:** Digital Equipment Corporation, *Programmed Data Processor-8 Users Handbook*, F-85, March 1966; revised/reprinted through 1967.  
**Primary status:** manufacturer-primary / contemporary.  
**Direct scan:** <https://bitsavers.org/pdf/dec/pdp8/handbooks/1966_PDP8_UsersHandbook.pdf>  
**Searchable inspection aid:** <https://manuals.plus/m/7bf964f156fe2d7a4c9fd352acca0dc596ead2350a42fdaa517152d5d97e9568>  
**Location:** Chapter 9, `AUTOMATIC RESTART TYPE KR01`, around printed p. 48 and the following power-fail sequence.

#### Directly supported facts

The chapter states that:

1. `Automatic Restart Type KR01` is a prewired option intended to protect an operating program against failure of computer primary power.
2. A power failure causes a program interrupt.
3. The option permits continued operation for **1 millisecond**.
4. During that interval, the interrupt routine can detect the `power low` condition and store active register contents — explicitly `AC`, `L`, `MQ`, etc. — plus the program count in **known core memory locations**.
5. When power returns, the power-low flag clears and a routine beginning at **address `0000`** starts automatically.
6. That routine restores active registers and the program counter, then continues the interrupted program.
7. The restart circuit can keep the machine inoperative through fluctuating power and, with automatic restart enabled, simulate console START about **200 ms after power is satisfactory**.
8. DEC explains the 200 ms delay as allowing slow mechanical devices such as Teletype equipment to stop before resumption.
9. Simulated START generates `Power Clear`, which clears internal controls and I/O device registers.
10. With automatic restart disabled, the program must be started manually, potentially after resetting peripheral equipment or restarting the program from the beginning.
11. The `SPL` (`SKIP ON POWER LOW`) instruction lets software distinguish power-low interrupt state.
12. Because the available interval is limited to 1 ms, DEC says the power-low flag should be the first status check in the interrupt routine.
13. DEC gives a bounded execution-time example: the opening interrupt sequence containing `SPL` and the power-fail sequence takes **25.5 μs** on a basic PDP-8 with the extended arithmetic element.
14. The example sequence saves processor context in designated core locations and arranges the restore call through location `0000`.

#### What this source does not by itself prove

- It does not specify in the inspected chapter whether capacitor, battery, magnetic energy, or another exact power-supply implementation supplies the 1 ms interval.
- It does not establish that all possible power-failure waveforms satisfy the interval.
- It does not establish persistence of every peripheral state.
- It does not settle invention priority for power-fail restart.

The case therefore uses `brief remaining reliable-operation interval`, not `capacitor-backed hold-up`, unless separately sourced.

---

### B — DEC PDP-8/L Users Handbook, 1968

**Source:** Digital Equipment Corporation, *PDP-8/L Users Handbook*, 1968.  
**Primary status:** manufacturer-primary / contemporary.  
**Public scan:** <https://commons.princeton.edu/motorcycledesign/wp-content/uploads/sites/70/2018/07/DEC-PDP-8L-Users-Handbook-1968.pdf>  
**Location:** KP8/L power-failure / automatic-restart option, around printed p. 48.

#### Directly supported facts

The PDP-8/L documentation repeats the core relation:

- impending power loss causes an interrupt;
- about 1 ms of continuing operation is made available;
- software stores active register state and the program count in known core locations;
- restored power restarts at address `0000`;
- a restore routine reconstructs processor state and continues the interrupted program;
- automatic restart can be enabled/disabled independently of the shutdown behavior.

This is used as a **later same-family witness**, not as evidence that all circuit details are identical to KR01.

---

### C — DEC Small Computer Handbook, 1970

**Source:** Digital Equipment Corporation, *digital Small Computer Handbook*, 1970 edition.  
**Primary status:** manufacturer-primary / contemporary.  
**Direct scan:** <https://bitsavers.org/pdf/dec/pdp8/handbooks/SmallComputerHandbook_1970.pdf>  
**Location:** Section 6-2, `POWER FAILURE DETECTION AND RESTART KP8/I [KP8/L]`, around printed p. 56.

#### Directly supported facts

The later handbook explicitly separates three functions:

- power-interrupt detection / `power low` flag;
- a `shut-down sequence circuit` that allows about 1 ms for the save routine and then halts operation;
- a restart circuit that waits for suitable power, clears the flag, and restarts via a selectable/defined entry.

The same source again states that active registers/program count are stored in known core locations and that restart can generate power clear for internal controls and I/O registers.

This witness is useful because it makes the **detection → shutdown/save opportunity → restart** decomposition explicit in DEC's own later wording.

---

### D — IBM 7090 Operator's Guide, early 1960s

**Source:** IBM, *IBM 7090 Data Processing System Operator's Guide*, early-1960s edition/revision.  
**Primary status:** manufacturer-primary / contemporary.  
**Searchable public copy:** <https://manualzz.com/doc/19740167/ibm-7090-data-processing-system-operator%E2%80%99s-guide>  
**Location:** `IBM 7151 Console Control`, panel keys **26 `Clear Key`** and **27 `Reset Key`**.

#### Directly supported facts

The IBM console documentation distinguishes:

- `Clear Key`: sets **all magnetic cores to zero** and resets registers/indicators;
- `Reset Key`: resets registers and indicators in the logical section, while explicitly stating that **core storage is not affected**.

#### Why it matters here

This is a clean period-primary witness that a core-memory computer could expose **different forgetting authorities for processor/control state and core storage** before the PDP-8 KR01 documentation.

It does **not** establish:

- automatic power-fail save;
- software register-to-core migration;
- historical descent from IBM to DEC;
- first invention of reset/clear separation.

It is therefore categorized as **prior-art/comparative boundary evidence**, not lineage.

---

### E — IBM System/360 Model 65 Functional Characteristics, September 1968

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
- or that every Model 65 storage/control component has the same physical retention mechanism.

### F — Smithsonian publication artifact metadata

**Source:** Smithsonian National Museum of American History, catalog record for DEC *Programmed Data Processor-8 Users Handbook*.  
**Status:** institutional provenance / secondary metadata.  
**URL:** <https://americanhistory.si.edu/collections/object/nmah_692491>

Used only to corroborate the existence/provenance of the 1966 DEC publication. Mechanism claims remain anchored in DEC's manual itself.

---

### G — related-repository source reuse

**Source:** [`tmzncty/computing-archaeology/docs/memory/why-core-memory-was-worth-weaving.md`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md).

**Reuse boundary:** broader core-memory physics, Whirlwind engineering, manufacturing labor, and historical constraint analysis belong there. This slice reuses only the already-grounded premise that ferrite-core main memory provides a power-independent remanent state at the element level and then studies the separate program-restart relation.

---

## Evidence table

| Claim | Source | Evidence class | Strength | Boundary |
| --- | --- | --- | --- | --- |
| KR01 protects an operating PDP-8 program against primary-power failure | DEC 1966, Ch. 9 | H/P | strong | bounded to documented option |
| power failure creates an interrupt and ~1 ms continued-operation opportunity | DEC 1966, Ch. 9 | H/P | strong | not a universal failure envelope |
| AC/L/MQ/program count are saved to known core locations | DEC 1966, Ch. 9 | H/P | strong | selected execution context, not every state |
| restored power begins recovery at address 0000 | DEC 1966, Ch. 9 | H/P | strong | entry point, not complete restored state |
| software restores active registers and PC before continuation | DEC 1966, Ch. 9 | H/P | strong | depends on valid save/restore code and core words |
| power-low test is time-critical | DEC 1966, Ch. 9 | H/P | strong | DEC's documented 1-ms contract |
| 200-ms delay serves slow mechanical-device settling | DEC 1966, Ch. 9 | H/P | strong | not a retention-lifetime claim |
| Power Clear clears internal controls and I/O device registers | DEC 1966, Ch. 9 | H/P | strong | does not imply physical core erase |
| same basic save/restart relation continues in KP8/L/KP8/I family | DEC 1968; DEC 1970 §6-2 | H/P | strong | no claim of exact circuit identity |
| processor/control reset and core clear can be separate authorities | IBM 7090 Operator's Guide | H/P | strong | comparative prior art only |
| Model 65 power-on reset preserves main storage | IBM 1968 Model 65 manual | H/P | strong | normal documented sequence only |
| Model 65 normal power-off preserves main storage but excludes protection-associated controls | IBM 1968 Model 65 manual | H/P | strong | requires stopped CPU; not arbitrary failure |
| controlled shutdown preservation ≠ failure-triggered automatic restart | IBM 1968 + DEC 1966 | E | strong bounded comparison | no lineage/circuit equivalence claim |

| core-content survival ≠ execution-context survival | DEC sources + Case 02 | E | strong reconstruction | project phrasing, not DEC terminology |
| active state is migrated into a stronger power-loss substrate | DEC sources | E | strong reconstruction | `state-class migration` is modern wording |
| restart entry ≠ restored runnable context | DEC sources | E | strong reconstruction | address 0000 only initiates restore |
| CPU continuation ≠ complete peripheral/external continuity | DEC 1966 | E | strong reconstruction | supported by Power Clear / Teletype / manual-reset warnings |
| KR01 is a modern checkpoint/restore system | none | A/X | rejected as historical terminology | functional analogy only |
| KR01 uses capacitor-backed hold-up | inspected source does not say | X | unsupported | do not infer physical implementation |

---

## Prior-art boundary

This record intentionally makes **no first-invention claim**.

The IBM 7090 witness already demonstrates an earlier commercially documented distinction between resetting processor/control state and deliberately clearing core storage. Other machines likely had power-fail, restart, and nonvolatile-core operational practices as well. Establishing a full chronology would require a wider survey of vendor manuals, power-supply circuitry, operating practices, and software conventions.

The September 1968 IBM Model 65 witness is used differently: it is a contemporary **counterexample/control boundary** showing that a normal reset/power sequence can preserve main storage while excluding a named protection-control class. It is not evidence of a DEC→IBM or IBM→DEC genealogy and does not extend the KR01 sudden-failure contract to the Model 65.

The defensible historical claim is narrower:

> **By March 1966, DEC documented a PDP-8 automatic-restart option in which power-failure detection provided a bounded interval for software to copy active processor state into core, and restored power invoked a core-resident restore path before the interrupted program continued.**

The 1968/1970 DEC witnesses show that this relation persisted in the later PDP-8 family.

---

## Historical record vs engineering reconstruction

### Historical record

DEC explicitly documents:

- power-low detection;
- interrupt;
- 1 ms of continued operation;
- save of named active registers/program count to known core locations;
- restart at address 0000;
- restore routine;
- 200 ms restart delay;
- Power Clear of other controls/I/O registers;
- manual-vs-automatic restart policy.

IBM explicitly documents separate `Clear` and `Reset` effects on core versus processor/control state.

IBM Model 65 documentation separately states that power-on system reset preserves main storage and that normal power-off preserves main storage, subject to a stopped-CPU condition, while excluding protection-feature controls and delaying power removal for five seconds.

### Engineering reconstruction

From those documented operations, this project infers:

- `core-content survival ≠ processor execution-state survival`;
- `power-fail detection ≠ state capture`;
- `state-class migration` from volatile active registers into core;
- `restart entry ≠ restored computation`;
- `selected state preservation can coexist with deliberate control-state reset`;
- `processor continuation ≠ peripheral/external-world continuity`.
- `controlled power-transition preservation ≠ arbitrary-failure restart`;
- `main-storage continuity ≠ protection/control continuity`.

These are mechanism-level reconstructions, not quotations from DEC.

### Functional analogy

The case can be compared narrowly with:

- later SSD power-loss protection, because both use a bounded failure transition to preserve selected state;
- persistent-memory power-fail domains, because both distinguish ordinary working state from failure-qualified retained state;
- snapshot/checkpoint recovery, because surviving encoded state plus a recovery procedure reconstructs later working state.

No historical or technical genealogy is claimed from KR01 to those later systems.

### Philosophical interpretation

The case supports a bounded interpretation that continuity can be produced by **selective transfer and reconstruction across an interruption**, not by keeping every state-bearing component unchanged. It also shows that deliberate reset/forgetting of some control state can be part of recovering a selected continuity relation.

That interpretation must remain downstream of the concrete KR01 mechanism.

---

## Cross-case boundary record

### Case 02 — classic magnetic core

Case 02 supplies element-level remanence and read/restore semantics. Case 86 supplies the missing system-level counterexample:

```text
nonvolatile core payload
    ≠
whole processor context
    ≠
automatic program continuation
```

### Case 06 — powered working state

Case 06 shows state that exists only while a powered bistable system is operating. KR01 shows one historical technique for moving selected working-state information out of that vulnerable regime before power disappears.

### Cases 15, 32, 38 — later power-fail retention

Only functional comparison is permitted. Do not back-project `PLP`, `ADR`, `eADR`, `persistence domain`, `hold-up capacitor`, or modern durability terminology into DEC 1966.

### IBM System/360 Model 65 controlled-transition comparison

Use the 1968 IBM source only to establish a contrasting state-class and transition boundary:

```text
power-on system reset + main storage preserved
normal power-off + stopped CPU + main storage preserved
protection-associated controls explicitly excluded
```

Do not convert this into evidence that the Model 65 automatically resumed an interrupted program after sudden power loss. DEC KR01 remains the failure-triggered save/restart mechanism in this case.

### IBM 7090 comparison

Use only to establish that core storage and logical/register reset were already separable control domains. Do not claim lineage into DEC KR01.

---

## Open follow-up, not promotion blockers

1. Locate and inspect the KR01 engineering drawings / power-supply documentation to identify the exact electrical mechanism that guarantees the 1-ms post-failure operating interval.
2. Determine whether DEC software libraries shipped a canonical power-fail save/restore routine beyond the handbook example.
3. Compare named peripheral controllers to determine what restart semantics were possible after `Power Clear` and interrupted I/O.
4. If the broader technical chronology becomes important, route a multi-vendor power-fail/restart genealogy to `computing-archaeology` rather than expanding this case into generic core-memory history.
5. An independent surviving-machine experiment could be useful later, but it would be labeled **Experiment**, not evidence of 1966 deployment practice.

---

## Promotion rationale

`grounded` is justified because the central claim does not depend on retrospective lore or on an analogy to modern nonvolatile systems. DEC's manufacturer-primary documentation directly supplies the failure event, time budget, named state to be saved, core destinations, restart entry, restore action, clear behavior, and peripheral caution. Later DEC documentation independently preserves the same basic relation, while IBM primary documentation supplies a bounded earlier comparative control-state distinction.

The remaining gaps concern circuit-level power-hold implementation, broader invention chronology, and peripheral-specific recovery — all intentionally outside the bounded claim.
