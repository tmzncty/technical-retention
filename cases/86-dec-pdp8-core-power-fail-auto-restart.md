# DEC PDP-8 Automatic Restart: Core-Resident Power-Fail Save and Reconstructed Execution State

**Status:** `grounded`

Grounding record: [`../evidence/86-dec-1960-1970-core-power-restart-grounding.md`](../evidence/86-dec-1960-1970-core-power-restart-grounding.md)

## Scope

This case asks a deliberately narrow question left open by the magnetic-core case:

> If magnetic-core words survive a loss of primary power, what additional state and work are required for a computer to continue the interrupted program rather than merely retain some memory contents?

The historical center is Digital Equipment Corporation's **PDP-8 Automatic Restart Type KR01**, documented in the March 1966 *Programmed Data Processor-8 Users Handbook*. DEC's option detects impending loss of primary power, gives the processor a bounded **1 millisecond** interval in which an interrupt routine can save active register contents and the program count into known core-memory locations, then, after power becomes satisfactory, restarts execution at address `0000` so software can restore that saved context and continue the interrupted program.

A 1968 PDP-8/L / 1970 Small Computer Handbook witness shows the same basic relation persisted in the later KP8/L / KP8/I option family. An IBM 7090 operator manual is used only as an earlier comparative witness that operator-level `reset` could clear processor/control state while leaving core storage unaffected, whereas a separate `clear` operation zeroed the cores. It is **not** evidence that DEC derived KR01 from IBM.

This is not:

- a general history of magnetic-core memory;
- a claim that all core-memory computers automatically resumed after power failure;
- a claim that magnetic remanence preserves CPU registers, I/O registers, peripheral mechanical state, timing state, or external-world progress;
- a claim that DEC invented power-fail detection, automatic restart, or software state save;
- a claim that the KR01 is a modern checkpoint/restore system in historical vocabulary;
- a claim that the 1 ms operating interval was specifically capacitor-backed unless a separate DEC power-supply source establishes that physical mechanism;
- a replacement for the core-device engineering in Cases 02 and 70 or in `computing-archaeology`.

The broader magnetic-core engineering history is already routed to [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology), especially its core-memory work. A repository search for this slice found no existing dedicated PDP-8 power-fail/restart treatment there, so only the retention-specific whole-system boundary is developed here.

---

## Historical vocabulary

The DEC sources give unusually useful period terms. They should remain visible rather than being silently replaced by later operating-system language:

- `AUTOMATIC RESTART TYPE KR01`;
- `power interrupt`;
- `power low flag`;
- `restart circuit`;
- `RESTART switch`;
- `SKIP ON POWER LOW (SPL)`;
- `active registers`;
- `program count` / `program counter`;
- `known core memory locations`;
- `address 0000`;
- `Power Clear`;
- `internal controls`;
- `I/O device registers`.

The later DEC handbook uses `POWER FAILURE DETECTION AND RESTART KP8/I [KP8/L]` and describes a `shut-down sequence circuit` plus a restart circuit.

The following expressions are **project engineering-reconstruction terms**, not claimed DEC vocabulary:

- `execution-state survival`;
- `core-resident emergency save`;
- `state-class migration`;
- `restart closure`;
- `continuation relation`.

`Checkpoint` is useful only as a modern functional analogy. The sources inspected for this case are not used to claim that DEC called KR01 a checkpoint mechanism.

---

## Retained state: one power failure exposes several different state classes

### 1. Ordinary core-memory words

The PDP-8 uses magnetic core as its main memory. Case 02 already establishes the bounded physical point relevant here: classic core can retain remanent magnetic state without periodic refresh, although normal access can require destructive-read restoration.

Case 86 therefore does not re-derive ferrite hysteresis, coincident-current selection, sense signals, or restore cycles.

### 2. Active processor state

DEC separately names the `AC`, `L`, `MQ`, `program count`, and other active registers as state that must be copied into known core-memory locations during the power-low interval.

The central historical fact is negative as well as positive:

> the presence of nonvolatile core memory did **not** make the currently active processor state automatically nonvolatile.

If those values are needed to continue the interrupted computation, they must cross a substrate/state boundary before ordinary logic can no longer operate reliably.

### 3. Restart-entry state

After power becomes satisfactory, KR01 does not somehow resume at the last electronic register state. DEC clears the program counter and arranges for execution to begin at **address `0000`**. The instruction there is made a `JMP` to the restore routine.

Address `0000` is therefore a retained **entry relation** into recovery. It is not a complete record of the old machine state.

### 4. Peripheral and internal-control state

The same restart sequence generates a `Power Clear` pulse. DEC says this clears internal controls and I/O device registers. The handbook also warns that with automatic restart disabled, manual restart may require resetting peripheral equipment or restarting the interrupted program from the beginning.

So the bounded continuation mechanism does not establish transparent preservation of every state coupled to the computation.

---

## Historical record

### H/P — KR01 turns power failure into an interrupt with a bounded save interval

DEC's 1966 *PDP-8 Users Handbook*, Chapter 9, describes KR01 as a prewired option that protects an operating program if the source of computer primary power fails. A power interrupt sets a `power low flag` and causes a program interrupt. The option then allows the computer logic to continue operating for **1 millisecond**.

DEC states what this interval is for: the interrupt routine is to detect the power-low condition and store active register contents — explicitly including `AC`, `L`, `MQ`, and the program count — in known core-memory locations.

This is a strong period-primary statement that whole-program continuation depends on more than passive survival of the ordinary memory array.

### H/P — the power-low test is deliberately first because save time is finite

The same chapter defines `SKIP ON POWER LOW (SPL)` and says that, because operation after a power failure can be extended for only 1 ms, the power-low flag should be the **first status check** made by the program-interrupt subroutine.

DEC gives a timing witness: on the basic PDP-8 with extended arithmetic element, the beginning of the interrupt subroutine containing `SPL` plus the power-fail program sequence can be executed in **25.5 microseconds** before the remainder of the save path.

The technical point is not that 25.5 μs is a universal recovery constant. It is that **failure detection, save latency, and remaining reliable-operation time are explicitly composed** in the period design.

### H/P — power restoration starts a restore program; it does not resurrect volatile registers in place

DEC says that when power is restored, the power-low flag clears and a routine beginning in address `0000` starts automatically. That routine restores the active registers and program counter to the conditions that existed when the interrupt occurred, then continues the interrupted program.

The restart circuit clears the PC so address `0000` is executed, and DEC requires that location to transfer control to the restore subroutine.

Thus the historical sequence is:

```text
power-low detection
    ↓
interrupt
    ↓
software save of active state into core
    ↓
ordinary powered execution ends
    ↓
power becomes satisfactory
    ↓
restart at 0000
    ↓
software restores active state from core
    ↓
interrupted program continues
```

This is stronger evidence than simply saying that ferrite cores are nonvolatile.

### H/P — restart is deliberately delayed and includes a control clear

With automatic restart enabled, the 1966 handbook describes a **200 millisecond** delay after power conditions are satisfactory before simulating the console `START` function. DEC explains this delay as giving slow mechanical devices such as Teletype equipment time to come to a complete stop before the program resumes.

The simulated start generates a `Power Clear` pulse that clears internal controls and I/O device registers.

The important boundary follows directly from DEC's own description:

> preserving core-resident program/context state can coexist with deliberately clearing other machine state before continuation.

### H/P — later PDP-8-family documentation preserves the same relation

DEC's 1968 PDP-8/L handbook and the 1970 *Small Computer Handbook* describe the later `KP8/L` / `KP8/I` power-failure detection and restart option in substantially the same terms: power low causes an interrupt, about 1 ms of continued operation permits software to save active registers and program count in known core locations, and restored power begins at address `0000` so a routine can restore context.

The 1970 description explicitly calls out a `shut-down sequence circuit` and a restart circuit. This later witness is useful because the retention relation is not confined to one sentence in the original 1966 KR01 chapter.

It is not used to claim that every circuit detail of KR01, KP8/L, and KP8/I is identical.

### H/P — IBM 7090 separates processor reset from core clear before KR01

The *IBM 7090 Operator's Guide* provides an earlier comparative control-state witness. Under the IBM 7151 Console Control description:

- the `Clear Key` sets all magnetic cores to zero and also resets registers/indicators;
- the `Reset Key` resets logical-section registers and indicators but explicitly **does not affect core storage**.

This is enough to show that by the early 1960s a commercial core-memory computer's operator interface could distinguish **clearing volatile/control state** from **clearing core contents**.

It is not evidence of direct influence on DEC, not an automatic-restart design, and not a priority claim for the full KR01 relation.

---

## Engineering reconstruction

### E — core-content survival ≠ processor execution-state survival

The most important distinction is:

```text
core words remain magnetized
        ≠
CPU execution context remains available in powered registers
```

DEC's save routine exists precisely because active processor state has to be **moved into the more power-loss-tolerant substrate** before the ordinary logic stops being usable.

This sharpens the warning already present in Case 02: element-level nonvolatility does not imply whole-system restart persistence.

### E — nonvolatile memory ≠ automatic program continuation

Even if all ordinary program and data words survive, continuation still depends on at least:

1. detecting power failure early enough;
2. obtaining a bounded interval of reliable operation;
3. saving the required active context;
4. preserving a usable recovery entry point;
5. detecting sufficiently stable restored power;
6. resetting/initializing enough control state to execute again;
7. restoring the saved processor context;
8. deciding what to do about peripheral state that was not preserved.

`Core is nonvolatile` establishes only part of that closure.

### E — failure detection ≠ state capture

The power-low flag tells software **why** an interrupt occurred. It does not itself preserve AC, MQ, link state, or the interrupted PC.

DEC therefore separates:

```text
detect impending loss
    → classify interrupt as power low
        → copy selected state to core
```

This is a useful retention pattern beyond this machine, but only the DEC-specific relation is historical evidence here.

### E — the 1 ms interval is retention infrastructure, not retained payload

The brief interval in which logic remains operational is not the saved state. It is a **temporal resource** that permits volatile state to be transferred into core before normal execution becomes impossible.

This is comparable in function to later emergency power-fail work, but the case does not infer a capacitor, battery, or other particular energy-storage implementation from the user handbook alone.

### E — state-class migration can be the decisive retention act

Before the interrupt routine runs:

```text
AC / MQ / PC / Link → active processor state
```

After the save routine completes:

```text
encoded copies of AC / MQ / PC / Link → core-memory words
```

The logical information can cross power loss because it has changed **where and how it is embodied**.

This is a small, historically concrete example of retention by migration between state classes rather than retention by making every state-bearing element equally nonvolatile.

### E — restart entry ≠ restored computation

Starting at address `0000` establishes only a path into recovery. Actual continuation still depends on the restore routine reconstructing the active state.

Therefore:

> `restart vector/entry survives ≠ previous machine configuration has already been restored`.

This is analogous to later recovery entry points only at the functional level.

### E — control reset can be part of continuity rather than its opposite

At first glance `Power Clear` looks like forgetting. But in this bounded design, deliberately clearing internal controls and I/O registers is part of making the post-power machine enter a known condition from which the preserved core-resident context can be used.

So:

> some state may have to be forgotten so that selected state can be resumed safely.

The historical fact is the DEC clear/restart sequence. Calling this a general `restart hygiene` principle would be modern reconstruction.

### E — restart closure is narrower than whole-world continuity

The saved CPU context does not prove that an electromechanical peripheral completed, aborted, or can repeat the external action associated with an interrupted I/O operation.

DEC's 200 ms Teletype rationale and warning about resetting peripherals make the limit concrete. Processor continuation can be reconstructed while external device state remains a separate recovery problem.

---

## Failure and forgetting modes

### Power falls too quickly for the save contract

KR01's documented scheme depends on a finite post-detection operating interval. If the relevant logic cannot execute the save path within that reliable interval, processor state that existed only in active registers may be lost even though older core contents remain.

The user handbook establishes the timing contract, not every electrical failure envelope.

### Power-low interrupt is not recognized first

DEC explicitly recommends testing the power-low flag first because the save window is bounded. A program interrupt path that spends too long handling other causes can consume the available interval before the required state is safely copied.

### Incomplete context save

If software saves only part of the state needed for correct continuation, the machine may retain many program/data words yet fail to reconstruct the interrupted computation.

### Core-resident save is damaged or overwritten

The restart mechanism depends on designated core locations and a valid address-0000 transfer to the restore routine. Core nonvolatility does not protect against later overwrite, program bugs, destructive-read/restore failure, or unrelated memory faults.

### Peripheral divergence

Internal controls and I/O device registers are cleared, and slow mechanical peripherals may have their own motion/progress. CPU-state restoration does not prove exactly-once external I/O continuation.

### Automatic restart disabled

The manual `RESTART` switch changes restart policy, not magnetic remanence. With the switch off, the power-low state can be cleared while the program still requires manual restart.

Thus:

> `automatic restart disabled ≠ core ceased to retain`.

---

## Cross-case comparison

### Case 02 — magnetic-core destructive read

[`02-magnetic-core-destructive-read.md`](02-magnetic-core-destructive-read.md) asks how one core bit persists and survives access. It explicitly warns that power-off core retention does not imply transparent restart of a complete computer.

Case 86 supplies a concrete answer to that warning:

> a historical machine can exploit core nonvolatility only by **capturing the volatile execution relation into core and later reconstructing it**.

The two cases are complementary rather than duplicates.

### Case 06 — powered flip-flop working retention

[`06-flip-flop-powered-working-retention.md`](06-flip-flop-powered-working-retention.md) shows short-lived powered bistable state. KR01 makes the power boundary operationally visible: some of the working states needed for continuation are copied out of the powered-register regime into core before that regime disappears.

This is a functional comparison, not a claim that PDP-8 registers have the same implementation as ENIAC's circuits.

### Cases 15 / 32 / 38 — later power-fail retention work

The SSD 320 power-loss case, Intel ADR/eADR, and enterprise PLI cases all contain a later family resemblance: a system detects or tolerates power failure and uses protected time/energy/domain structure to preserve selected state.

The analogy must stop there.

KR01:

- protects a running CPU program by software-saving active register context into magnetic core;
- is documented in 1966 vocabulary of interrupt, restart, core locations, and active registers;
- does not establish the later SSD/controller concepts of volatile write cache, media flush, PLI capacitor health, ADR, or persistence domains.

So:

> `bounded power-fail save analogy ≠ technical genealogy`.

### Cases 46 / 58 / 71 — recovery state in later storage/distributed systems

GFS log/checkpoint recovery, Raft snapshots, and ZooKeeper fuzzy snapshots all retain state from which a service can later reconstruct a working configuration. KR01 is functionally comparable only in the narrow sense that **surviving representation plus a recovery procedure** can recreate working state.

It is not a distributed log, consensus snapshot, or filesystem checkpoint.

### IBM 7090 — reset versus clear

The IBM operator guide offers a useful control comparison:

```text
Reset → logical registers/indicators reset; core survives
Clear → core is deliberately zeroed too
```

DEC KR01 adds a different relation: selected volatile state is intentionally copied into core before failure, then a controlled restart reconstructs processor execution.

The common lesson is functional — **core survival and machine-control survival are separable** — not historical lineage.

---

## Philosophical / media-theoretical interpretation

### I — continuity may depend on changing embodiment before interruption

The technical fact is specific: DEC does not make every active state nonvolatile. It notices an approaching interruption and uses the remaining operational interval to transfer selected information into core.

This supports one bounded interpretation:

> technical continuity need not mean an uninterrupted substrate. It can mean preserving enough relations across a break that a later machine state can be reconstructed as continuation of the earlier one.

The philosophical value is that **interruption** and **retention** are not opposites here. The failure signal itself activates the work that makes continuation possible.

### I — selective forgetting can support retention

`Power Clear` removes some internal/I/O control state before the restore routine recreates the selected CPU context. This gives a concrete counterexample to any thesis that persistence means maximizing the amount of state kept unchanged.

A system may instead preserve a **carefully chosen subset**, erase/reset another subset, and use the retained subset to rebuild an admissible working configuration.

This is an interpretation of the engineering relation, not DEC's own philosophical vocabulary.

---

## Claim ledger

| Claim | Type | Evidence / status |
| --- | --- | --- |
| KR01 is documented by DEC in the 1966 PDP-8 Users Handbook | H/P | direct manufacturer handbook, Chapter 9 |
| power low triggers interrupt and approximately 1 ms of continued operation | H/P | DEC 1966 Chapter 9 |
| active registers and program count are stored in known core locations | H/P | DEC 1966 Chapter 9 |
| restored power restarts via address 0000 and a software restore routine | H/P | DEC 1966 Chapter 9 |
| automatic restart waits about 200 ms after satisfactory power and generates Power Clear | H/P | DEC 1966 Chapter 9 |
| Power Clear clears internal controls and I/O device registers | H/P | DEC 1966 Chapter 9 |
| later KP8/L/KP8/I documentation preserves the same basic save/restart relation | H/P | DEC 1968 / 1970 handbook witness |
| IBM 7090 Reset can spare core while Clear zeros core | H/P | IBM 7090 Operator's Guide, IBM 7151 Console Control keys 26–27 |
| core-content survival is insufficient for CPU execution-state survival | E | reconstruction from DEC's explicit save requirement |
| state is migrated from active registers into core before power loss | E | reconstruction; `state-class migration` is project terminology |
| address 0000 is a recovery entry, not a complete saved state | E | reconstruction from DEC restart flow |
| processor restart does not establish complete peripheral/external-world continuity | E | bounded by Power Clear + 200 ms Teletype rationale + manual-reset warning |
| KR01 is historically a `checkpoint` system | X | useful modern analogy only; not established as DEC vocabulary |
| KR01 was capacitor-backed | X | not established by the handbook evidence used here |
| all core-memory computers automatically resume after arbitrary power failure | X | explicitly rejected |
| IBM 7090 directly influenced DEC KR01 | X | no lineage evidence established |

---

## Sources

### Primary / contemporary

1. **Digital Equipment Corporation, _Programmed Data Processor-8 Users Handbook_, F-85, March 1966** (reprinted/revised 1966–1967), Chapter 9, `AUTOMATIC RESTART TYPE KR01`, especially the description around printed p. 48 and the following power-fail program sequence. Direct scan: <https://bitsavers.org/pdf/dec/pdp8/handbooks/1966_PDP8_UsersHandbook.pdf>. Searchable extraction used as an inspection aid: <https://manuals.plus/m/7bf964f156fe2d7a4c9fd352acca0dc596ead2350a42fdaa517152d5d97e9568>.
2. **Digital Equipment Corporation, _PDP-8/L Users Handbook_, 1968**, KP8/L power-failure/restart section, around printed p. 48. Public scan: <https://commons.princeton.edu/motorcycledesign/wp-content/uploads/sites/70/2018/07/DEC-PDP-8L-Users-Handbook-1968.pdf>.
3. **Digital Equipment Corporation, _Small Computer Handbook_, 1970**, Section 6-2, `POWER FAILURE DETECTION AND RESTART KP8/I [KP8/L]`, around printed p. 56. Public scan: <https://bitsavers.org/pdf/dec/pdp8/handbooks/SmallComputerHandbook_1970.pdf>.
4. **IBM, _IBM 7090 Data Processing System Operator's Guide_**, early-1960s edition/revision, `IBM 7151 Console Control`, panel keys 26 `Clear Key` and 27 `Reset Key`. Public scan/extraction: <https://manualzz.com/doc/19740167/ibm-7090-data-processing-system-operator%E2%80%99s-guide>.

### Institutional metadata

5. **Smithsonian National Museum of American History**, catalog record for DEC's 1966 *Programmed Data Processor-8 Users Handbook*. Used only for artifact/publication provenance, not as the mechanism source: <https://americanhistory.si.edu/collections/object/nmah_692491>.

### Related-repository reuse

6. [`tmzncty/computing-archaeology: Why Was Magnetic-Core Memory Worth Weaving by Hand?`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md) — broader core-memory engineering, manufacturing, and historical constraint analysis. Case 86 deliberately does not rewrite it.

---

## Evidence boundary

This case is `grounded` for the bounded retention relation because manufacturer-primary documentation directly establishes:

- an explicit impending-power-failure event;
- a finite post-detection operating interval;
- software transfer of active processor state into known core-memory locations;
- a separate restart entry after power restoration;
- software restoration of that context before continuation;
- clearing of other internal/I/O state during restart;
- and a later PDP-8-family witness preserving the same basic relation.

The case does **not** establish:

- the exact energy-storage/power-supply circuit that physically provides the 1 ms interval;
- survival of every core word under every possible power fault;
- exactly-once peripheral I/O continuation;
- full KR01/KP8/L/KP8/I circuit identity;
- invention priority for power-fail restart;
- or direct genealogy from IBM or later checkpoint/power-loss-protection systems.

Those limits are deliberate. The value of Case 86 is the narrower conclusion:

> **nonvolatile main memory can preserve program/data state while whole-computer continuity still depends on detecting interruption, migrating volatile execution state into that memory, resetting selected control state, and later reconstructing a runnable context.**
