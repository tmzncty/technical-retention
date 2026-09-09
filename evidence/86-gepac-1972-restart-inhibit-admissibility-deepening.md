# Case 86 deepening — GE-PAC 3010/2 power-fail handoff and time-bounded restart admission

## Scope

This addendum deepens [`../cases/86-dec-pdp8-core-power-fail-auto-restart.md`](../cases/86-dec-pdp8-core-power-fail-auto-restart.md) at one narrow seam that the DEC material leaves only partly explicit:

> **If volatile execution state has already been copied into nonvolatile core and still physically survives, is automatic restart therefore always authorized?**

The bounded historical witness is General Electric's **GE-PAC 3010/2** process computer, documented in 1972 manufacturer manuals. The machine is useful because its power-fail path combines three relations that must not be collapsed:

1. impending-power detection and transfer of the General Register Stack plus Processor Status Word (`PSW`) into core;
2. later restoration of that context when power returns;
3. an optional **Restart Inhibit Timer** that can revoke automatic restart after an operator-selected outage interval because the controlled process may no longer be safe to resume automatically.

This is not a second general history of magnetic core, not a claim that GE derived the design from DEC, not a universal process-control restart rule, and not evidence that core remanence itself expires when the restart-inhibit timer expires. The broader core-memory engineering history remains in `tmzncty/computing-archaeology`.

---

## Source custody and evidence class

### General Electric GET-6227, May 1972

General Electric's *GE-PAC 3010/2 General Description*, GET-6227, May 1972, is manufacturer-primary documentation. Its power-fail/restart section states that sufficiently low or interrupted primary AC causes automatic storage of the General Register Stack and PSW in Core Memory before orderly shutdown; after acceptable power returns, hardware initialization and automatic restoration occur, subject to the restart policy and restored PSW state.

The same manual describes option `3010AB14 Restart Inhibit Timer` and gives a calibrated range of **10 seconds to 10 minutes**, chosen according to the customer's judgement about whether automatic restart remains safe for the process and backup controls.

### GE-PAC 3010/2 power-subsystem documentation

A separate GE *3010/2 Power Subsystem* manual preserved in the same archive gives a more implementation-oriented account. It says the Power Failure Detector starts the PSW/general-register storage micro-program early enough for completion before processor logic power falls below its operating level. It describes a core area selected through the register-save pointer at dedicated core address `X'22'`, and says that after AC returns a restoration micro-program can return the running program to its prior point.

That manual also describes an Automatic Restart Inhibit Timer, but gives an adjustable range of **one minute to 10 minutes**, rather than GET-6227's 10-seconds-to-10-minutes range.

This addendum does **not** silently harmonize those values. They may reflect revision, option, configuration, or documentation differences. Until exact document chronology/configuration is resolved, the safe historical claim is only that GE documented a customer-adjustable, minutes-scale restart-admission timer whose purpose was process-safety gating.

### Facsimile boundary

The archived GE documents are primary manufacturer manuals, but the direct PDF endpoints could not be rendered page-by-page in this research pass. The exact mechanism statements used here are therefore marked `H/P*`: primary-document text recovered from indexed archival copies, with direct facsimile/page-image verification still open. This is a source-custody limitation, not a reason to downgrade the engineering distinctions reconstructed from the documented relation.

---

## Historical record

### H/P* — impending power loss triggers state transfer into core

GET-6227 says the processor monitors its primary AC supply. If line voltage falls to the documented low threshold or is absent for more than one AC cycle, the General Register Stack and PSW are automatically stored in Core Memory and an orderly shutdown begins.

The power-subsystem manual supplies the more explicit sequencing witness: the Power Failure Detector starts the register/PSW storage micro-program early enough that the transfer completes before processor logic power falls below its usable level.

The historical relation is therefore stronger than `core memory survives power loss`:

```text
volatile execution context
        ↓ impending-power detection
micro-programmed transfer
        ↓
reserved core-memory state
        ↓
processor shutdown
```

### H/P* — the saved state occupies a designated core relation

The power-subsystem documentation associates the save with the core area specified through the register-save pointer at dedicated core address `X'22'`. This is not merely passive preservation of whatever application words happened already to reside in core; the machine intentionally creates a restart representation of volatile processor state inside the nonvolatile memory system.

This addendum does not infer the full internal layout of that save area beyond what the manual states.

### H/P* — after the save sequence, ordinary core activity stops while core retains the result

GE's general description states that once system functions are initialized at the end of the power-down sequence, the processor makes no further attempts to read from or write to core, and the core memory retains its stored information until power returns.

This is useful because it places the machine in two successive regimes:

```text
powered failure-handoff interval:
    active micro-program + core writes

post-handoff power-loss interval:
    no ordinary core access + remanent retained state
```

The first regime is active transfer; the second is quiescent magnetic retention. They are not one mechanism called `refresh`.

### H/P* — restoration is a separate operation after power returns

GET-6227 says that when primary power returns within the applicable automatic-restart conditions, hardware is initialized and the General Registers and PSW are automatically restored. The restored PSW then participates in deciding whether instruction sequencing continues from the point where shutdown occurred or enters the documented malfunction/restart handling path.

Thus `saved context exists in core` and `processor has already resumed the old computation` are historically separate states.

### H/P* — automatic-restart authority can expire while core state survives

The key new witness is the optional Restart Inhibit Timer. GET-6227 says its purpose is to prevent automatic restart when enough time has passed since power failure that restarting the computer without manual intervention may no longer be safe for the controlled process. The selected interval is explicitly tied to the customer's judgement about the process and backup controls.

The separate power-subsystem manual preserves the same policy relation even though its documented adjustable range differs.

This means the historical machine distinguishes:

```text
saved execution state remains embodied in core
        ≠
automatic restart remains admissible
```

The timer changes the **authority to act on the retained state**, not the ferrite's magnetic retention mechanism.

---

## Engineering reconstruction

### E — nonvolatile execution checkpoint and restart admission are different retained relations

Case 86 already establishes that nonvolatile main memory is insufficient for whole-computer continuation: selected volatile CPU state must first be copied into core. GE-PAC adds another layer.

Even after that copy has succeeded, continuation still has at least two questions:

1. **recoverability:** is the saved register/PSW representation still available and restorable?
2. **admissibility:** is automatic continuation still allowed under the machine/process restart policy?

The Restart Inhibit Timer can answer the second question negatively without showing that the first has become false.

Therefore:

> **recoverable saved context != automatically admissible continuation.**

### E — the restart-inhibit timer is not a core-retention lifetime

It would be a category error to read the selected 10-second/minute-scale timer as a shelf-life specification for magnetic core. The GE description ties the interval to the external controlled process, backup controls, and safe restart policy.

The timer says when **automatic use of retained context** becomes unsafe without manual intervention. It does not say when the core bits physically disappear.

So:

> **restart-admission deadline != physical-retention deadline.**

### E — external-world drift can invalidate continuation without corrupting the checkpoint

A process-control computer does not operate in a closed symbolic world. During an outage, pumps, valves, sensors, mechanisms, or backup controls can change independently of the saved CPU state. A register/PSW image can therefore remain perfectly intact while the world to which it referred has moved beyond the conditions under which automatic replay/continuation is safe.

GE's timer is direct historical evidence that designers treated this as an operational concern. The broader formulation `external-world drift can revoke checkpoint admissibility` is project engineering reconstruction.

### E — failure-triggered handoff is not refresh

The power-fail routine performs a one-time event-triggered transfer of volatile execution state into core because ordinary powered logic is about to disappear. This is not periodic restoration needed to preserve core magnetization.

The distinction is:

```text
core remanence:
    keeps already-written magnetic state without recurring refresh

power-fail handoff:
    creates additional core-resident continuation state before logic power is lost
```

Calling both `maintenance` may be useful at a high level, but calling the second `refresh` would erase the trigger and state-class boundary.

### E — restart policy can be retention infrastructure without being payload

The timer and its admission logic do not contain the application payload or the saved register values. Yet they determine whether the surviving representation may automatically become a running computation again.

This is another instance of a repository-wide distinction:

> **state that qualifies use of retained payload can be constitutive of recoverability/service without being the payload itself.**

---

## Functional comparison

### A — DEC PDP-8 Case 86: same broad handoff role, different restart policy

DEC KR01/KP8-family evidence and GE-PAC 3010/2 both show impending-power detection followed by transfer of volatile execution state into magnetic core and later restoration.

The comparison is useful only at that functional level. DEC's documented interrupt/software save, address-`0000` restore entry, Power Clear behavior, and later KP8-E capacitor witness are not silently assigned to GE. Conversely, GE's process-safety Restart Inhibit Timer is not projected backward onto DEC.

No DEC→GE, GE→DEC, or common-origin genealogy is established.

### A — Intel SSD 320 Case 15: failure-triggered durability handoff only

Case 15 provides a much later functional analogy. Intel documents power-fail detection and stored capacitor energy used to move controller-buffer state into NAND. GE documents an impending-power sequence that moves processor context into magnetic core before logic power becomes unusable.

The shared abstraction is narrow:

```text
failure signal
    → finite remaining operational opportunity
        → move selected state into a more failure-tolerant embodiment
```

The physical mechanisms and historical vocabularies differ. The GE sources inspected here do not establish an SSD-like dedicated capacitor hold-up mechanism, and the Intel SSD does not implement a process-control restart-inhibit policy merely because both systems react to power failure.

### A/X — restart-inhibit policy is not a distributed-consensus lease or epoch

A modern reader could compare an expiring restart permission to leases, epochs, or freshness/admission bounds in distributed systems. That can be heuristically suggestive, but this evidence does not establish mechanism identity or genealogy. GE's timer is a local process-control safety policy around machine restart.

---

## Philosophical interpretation

### I — survival and permission-to-resume are not the same temporal relation

The exact technical fact is modest: a saved machine context can remain in nonvolatile core while a separate timer makes automatic resumption inadmissible because the external process may have changed.

This clarifies a bounded philosophical point about technical continuity. Persistence is not exhausted by the question `did the inscription survive?` A surviving state may also need a still-valid relation to the world in which it is to be acted upon.

The interpretation stops there. The GE-PAC timer is not a general theory of memory, does not prove that all retained records have expiration dates, and should not be redescribed as Heideggerian or Stieglerian vocabulary without a separate argument.

---

## Claim ledger

| Claim | Label | Evidence |
| --- | --- | --- |
| GE-PAC 3010/2 documents automatic register-stack + PSW transfer into core on detected power failure | `H/P*` | GE GET-6227 + power-subsystem manual indexed archival text |
| the power-subsystem path associates the save with a register-save pointer at core address `X'22'` | `H/P*` | GE power-subsystem manual |
| GE documents no further ordinary core reads/writes after the power-down initialization sequence and says core retains stored information until power returns | `H/P*` | GET-6227 |
| power return includes a separate initialization/restoration sequence before continuation | `H/P*` | GET-6227 + power-subsystem manual |
| GE documents an optional Restart Inhibit Timer whose purpose is preventing unsafe automatic restart after a sufficiently long outage | `H/P*` | GET-6227 + power-subsystem manual |
| exact timer range is one universal GE-PAC constant | `X` | surviving GE manuals disagree: 10 s–10 min vs 1–10 min |
| restart-inhibit interval is a magnetic-core retention specification | `X` | source ties it to process/control restart safety, not ferrite decay |
| saved context can remain recoverable while automatic continuation becomes inadmissible | `E` | bounded reconstruction from core retention + restart-inhibit policy |
| GE-PAC and DEC PDP-8 use the same circuit/protocol | `A/X` | functional handoff analogy only |
| GE-PAC power-fail handoff and Intel SSD 320 PLP are one mechanism | `A/X` | functional failure-triggered transfer analogy only |

---

## Open questions

- obtain direct renderable facsimile/page-image anchors for the exact GE paragraphs used here;
- resolve the chronology/configuration behind the 10-seconds-to-10-minutes versus one-minute-to-10-minutes Restart Inhibit Timer ranges;
- recover exact electrical hold-up/time-budget details between power-fail detection, the save micro-program, system clear, and loss of usable processor logic power;
- inspect whether different 3010/2 CPU/power-option configurations changed the save/restart contract;
- do not infer which external process variables operators used to choose the timer setting without application-specific evidence;
- broader GE-PAC processor/power-subsystem history and cross-vendor automatic-restart genealogy belong primarily in `tmzncty/computing-archaeology` if developed.

---

## Sources

1. General Electric, *GE-PAC 3010/2 General Description*, GET-6227, May 1972, especially §4.7 `POWER FAIL DETECTOR AND AUTOMATIC RESTART` and §4.7.1 `Restart Inhibit Timer Option`; archived scan: <https://www.bitsavers.org/pdf/ge/GE-PAC_3010/GET-6227_GE-PAC_3010_2_General_Description_197205.pdf>.
2. General Electric, *3010/2 Power Subsystem*, especially `Power Failure Detector and Automatic Restart Option` and `AUTOMATIC RESTART INHIBIT TIMER`; archived scan: <https://www.bitsavers.org/pdf/ge/GE-PAC_3010/3010_Power_Subsystem.pdf>.
3. General Electric, *GE-PAC 3010/2 Central Processor Reference Manual*, GET-6174, October 1972, used only for system context such as the 16 General Registers, micro-programmed control, and core-memory organization; archived scan: <https://www.bitsavers.org/pdf/ge/GE-PAC_3010/GET-6174_GE-PAC_3010_2_Central_Processor_Reference_Manual_197210.pdf>.
4. BAMA archive index for the surviving GE-PAC 3010 manual set, used for custody/file identification rather than mechanism claims: <https://bama.edebris.com/manuals/bitsavers/pdf/ge/GE-PAC_3010/index-2098439346.html>.

### Source-boundary note

The GE manuals are manufacturer-primary documents. Because direct page-image rendering failed in this pass, exact GE mechanism/range claims remain `H/P*` until facsimile inspection is completed. The two timer ranges are preserved as a documentary discrepancy rather than normalized into one value.
