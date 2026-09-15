# Case 02 Deepening — IBM 7090 Power-On Clear: Nonvolatile Core vs Restart Preservation Policy (1960–1962)

**Status:** `bounded deepening complete`

## Purpose

This record deepens [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md) around one narrow gap left by the existing 1965 IBM 1401 / 1966 DEC PDP-7 power-transition evidence:

> if a core array can retain magnetic state without continuous power, does a machine therefore preserve the previous core image across an ordinary restart?

For the IBM 7090, the answer is **no as a machine policy**. IBM documentation from 1960–1962 distinguishes an operator `Reset`, which leaves core storage unchanged, from `Clear`, which resets core storage to zeros; the ordinary Power On path requires a clear operation as power is applied. This creates a useful named-machine counterexample to any simple equation between a materially nonvolatile substrate and a restart policy that preserves the old logical image.

The bounded distinction is:

```text
remanent core capability
    !=
power-transition behavior
    !=
restart preservation policy
    !=
post-restart service state
```

This record does **not** prove what every individual core contained at every electrical instant during the 7090 power sequence. It establishes IBM's documented operational/control semantics.

Claim layers follow repository policy: **Historical record**, **Engineering reconstruction**, **Functional analogy**, and **Philosophical interpretation** remain separate.

## Sources inspected

### IBM 7090 Customer Engineering Instruction-Reference, Form 223-6895-1

IBM, **IBM 7090 Data Processing System — Customer Engineering Instruction-Reference**, Form `223-6895-1`, Major Revision, **September 1961**. The document states that this edition supersedes Form 223-6895 and earlier editions.

Preserved scan:

- <https://www.bitsavers.org/pdf/ibm/7090/ce/223-6895-1_7090_CE_Reference_System_Fundamentals_7100_7151_7606_Sep61.pdf>
- archive directory: <https://bitsavers.computerhistory.org/pdf/ibm/7090/ce/>

The power-control material distinguishes several operations:

- normal Power On starts a sequence that brings the machine to ready state;
- as power comes on, a **clear operation** is performed;
- the power-on reset resets machine control state and **sets core storage to all zeros**;
- Normal Off uses a staged power-down sequence rather than simply dropping every supply simultaneously;
- Emergency Off removes power immediately and is documented as an emergency action rather than the normal shutdown path.

The same reference distinguishes power-on/interlock/operator reset behavior from the deliberate core-storage zeroing associated with power-on reset.

**Source-custody note:** the preserved IBM scan and bibliographic identity were checked. In the current research environment the PDF image itself could not be re-opened reliably for page rendering, so exact claims here are limited to the indexed text of the manufacturer document and are cross-checked against the independently accessible 1962 IBM installation instructions below. No claim depends on reconstructing a circuit from an uninspected figure.

### IBM 7090 Data Processing System — Installation Instructions

IBM, **Installation Instructions: IBM 7090 Data Processing System**, archived scan dated **9 April 1962** in the filename/scan collection.

Preserved scan:

- <https://bitsavers.computerhistory.org/pdf/ibm/7090/ce/Installation_Instructions_IBM_7090_Data_Processing_System_19620409.pdf>

The system-testing section is especially useful because it places `Reset`, `Clear`, and `Power On` next to one another as different machine operations.

In §§5.1.9–5.1.12 the instructions state, in substance:

- **Power On:** from Normal Off, Power On restores power and **a clear operation must occur as power is applied**;
- **Reset:** the console reset clears machine registers/triggers as specified but **does not affect core-storage contents** and does not reset the machine clock;
- **Clear:** in Automatic, Clear performs the Reset functions and additionally resets the machine clock and **resets all core-storage locations to zeros**.

The same test sequence separately describes Normal Off and Emergency Off. Normal Off is staged; Emergency Off removes system power immediately except for specified hot circuits.

This is the strongest source for the bounded retention distinction because one IBM document directly contrasts a control operation that leaves core contents alone with another that intentionally replaces them, and then requires the latter during ordinary power-on.

**Inspection note:** the text layer of the archived IBM PDF was directly inspected. Page-image rendering was attempted in the research tool but the archive renderer returned a cache/fetch failure, so this record does not claim a fresh visual inspection of diagrams or handwritten marks.

### IBM 7090 / 709 General Information Manual, August 1960 — contextual control

IBM, **709·7090 Data Processing System — General Information Manual**, August 1960.

Preserved scan:

- <https://bitsavers.computerhistory.org/pdf/ibm/7090/D22-6508-2_709_7090_General_Information_Manual_Aug1960.pdf>

This document is used only as contextual confirmation for the 7090's core-storage architecture and period terminology. It is **not** used to infer the exact power-on clearing sequence where the 1961/1962 customer-engineering documents are more direct.

## Historical record — IBM distinguishes Reset from Clear

The 1962 Installation Instructions make the most important boundary explicit at the operator/control level.

`Reset` is not defined as a blanket destruction of all machine state. It affects the console-visible machine registers/triggers and channels specified by the procedure while **leaving core-storage contents unchanged**.

`Clear` is a different operation. In Automatic mode it includes the Reset functions but adds a stronger state transition: it resets the machine clock and resets all core-storage locations to zeros.

Therefore the period machine exposes at least two distinct control-authority classes:

```text
Reset
    -> reinitialize selected control state
    -> preserve core-storage payload

Clear
    -> perform Reset functions
    -> additionally replace core-storage payload with zeros
```

This matters because the physical substrate is the same in both cases. The difference is not whether the core is magnetic; the difference is **which operation the machine authorizes**.

The documentation therefore blocks the shortcut:

> `nonvolatile core = reset always preserves memory`.

It does not.

## Historical record — ordinary Power On requires Clear

The same 1962 installation instructions state that when the system is in Normal Off status and Power On is initiated, **a clear operation must occur as power is applied**.

The 1961 Customer Engineering reference independently describes the power-on sequence as performing a clear / power-on reset that sets core storage to zeros.

Thus the bounded historical relation is:

```text
Normal Off
    -> Power On
    -> required Clear / power-on reset
    -> core storage becomes all zeros
    -> machine enters a defined startup state
```

This is not merely a diagnostic convenience performed by an operator after startup. In the documented ordinary power-on path, clearing is part of the startup transition itself.

That makes the 7090 a useful counterexample to the nearby IBM 1401 evidence already present in Case 02. The 1401 Operator's Guide documents a prescribed `ALTER` procedure under which information in core storage is retained across power-off/power-on. The 7090 documentation instead makes ordinary startup clear the core image.

The correct historical conclusion is therefore **machine-specific variation**, not a universal IBM policy.

## Historical record — power sequencing and startup clearing are separate relations

The 7090 customer-engineering material also separates Normal Off from Emergency Off and describes staged removal of power in the normal path.

That distinction matters because two different questions could otherwise be collapsed:

1. **What happens electrically while supplies are being removed or restored?**
2. **What logical state does the machine intentionally establish before returning to normal service?**

On the 7090, the ordinary startup answer to the second question includes clearing core storage. Even perfect electrical preservation of a pre-existing magnetic pattern during some earlier portion of the transition would not make that pattern the post-startup service state once the machine performs the documented clear.

Therefore:

> **transition protection / sequencing != restart preservation policy.**

The existing PDP-7 evidence is useful as the complementary control. DEC documents circuitry designed to avoid transient destruction of stored core while deliberately clearing RUN and memory-control flip-flops. The 7090 adds a case where startup policy intentionally goes further and replaces the core payload itself.

## Engineering reconstruction — material survival and service continuity are different tests

The IBM documents support a four-layer reconstruction:

```text
1. material embodiment
   remanent magnetic orientation of cores

2. transition condition
   what currents / rails / control signals occur while power changes

3. startup authority
   which Reset / Clear / power-on operation is invoked

4. admitted service state
   which payload and control state the machine presents after startup
```

A bit pattern can be physically retainable at layer 1 without being institutionally or operationally preserved through layers 3–4.

For the 7090, the historical evidence is strongest for layers 3–4: ordinary Power On requires Clear, and Clear sets core storage to zero.

The documentation does **not** establish that every old magnetic bit survived intact immediately before the clear pulse. That would require a different electrical or experimental witness.

Hence:

```text
possible pre-clear remanence
    !=
documented preservation of the old image

and

documented startup zeroing
    !=
proof that the old image had already decayed before zeroing
```

## Engineering reconstruction — `retained` needs an operation class

The 7090 makes a general project rule more precise: asking whether a state is `retained` is incomplete unless the operation boundary is named.

For the same core payload:

```text
through Reset:
    documented as preserved

through Clear:
    documented as replaced with zeros

through ordinary Power On:
    Clear is required, so old payload is not preserved as service state
```

Therefore the retention predicate is operation-relative:

> **retained through Reset != retained through Clear != retained through Power On.**

This is not semantic hair-splitting. The three operations have different machine effects in the IBM documentation.

## Engineering reconstruction — restart can intentionally retire a materially surviving state

The 7090 adds a useful negative-retention form that is different from decay, accidental corruption, or failure to restore after destructive read.

The old core image can cease to be the machine's state because startup deliberately establishes a known zero image.

Conceptually:

```text
old core image
    -> machine is powered down
    -> old magnetic embodiment may or may not remain physically readable
       at every intermediate instant (not established here)
    -> Power On invokes Clear
    -> machine writes startup zero state
    -> old image is intentionally retired from ordinary service
```

This supports a bounded distinction:

> **physical survival opportunity != preservation authority.**

The word `authority` here is an engineering reconstruction: the machine's documented control path determines which state is established for service. IBM does not use this modern analytical vocabulary.

## Engineering reconstruction — known startup state can be more important than preserving prior payload

The 7090 design documents show that ordinary startup is not optimized around preserving whatever was previously in core. Instead, the machine establishes a known cleared state before service.

A narrow mechanism-level inference is therefore:

```text
nonvolatile substrate capability
    can coexist with
startup policy that intentionally discards prior payload
```

This does **not** justify speculation about IBM's organizational motive, operating-system philosophy, security policy, or every use case. The sources show the machine behavior; they do not supply a general theory of why IBM chose it.

## Cross-case control — IBM 1401: same broad medium class, different startup policy

Case 02's 1965 IBM 1401 evidence documents a prescribed `ALTER` power procedure in which information in core storage is retained through the controlled power transition.

The 7090 therefore prevents an overgeneralization from that later IBM witness:

```text
IBM 1401 controlled power transition
    -> documented payload preservation

IBM 7090 ordinary Power On
    -> documented core clearing
```

This is a comparison of named-machine operating contracts. It is **not** evidence that the machines share identical power-control circuitry, memory-stack construction, or historical development path.

## Cross-case control — DEC PDP-7: protect payload, reset control state

The 1966 PDP-7 Maintenance Manual documents a third pattern:

```text
core payload
    -> protected from switching transients

RUN / memory-control flip-flops
    -> deliberately cleared / initialized
```

The 7090 shows that the payload/control distinction is not universal in scope. A machine may choose to clear control state while protecting payload, or it may choose a startup operation that clears both selected control state **and core storage**.

Thus:

> **retained substrate class != universal restart-state partition.**

## Cross-case control — Case 86 PDP-8 automatic restart

Case 86 studies a different problem: a PDP-8 family system can use remanent core plus explicit power-fail save / restart machinery so that selected execution context survives a failure boundary and can participate in automatic restart.

The 7090 evidence is a deliberate negative control:

- core remanence alone does not create automatic restart;
- a system may actively preserve restart context;
- a different system may actively clear the old core image during ordinary startup.

This is only a functional comparison. No technical descent is claimed.

## Cross-case control — TCM-32 whole-stack Memory Clear

The existing 1964 TCM-32 evidence already shows that magnetic core can expose an explicit whole-stack electrical reset to the machine-defined zero state.

The 7090 deepening adds a different relation:

> the whole-memory clear is not merely an available maintenance/operator operation; it is **required as part of ordinary power-on** in the inspected 7090 procedure.

This strengthens the repository's separation among substrate nonvolatility, explicit forgetting operation, and restart policy without claiming that the IBM and 3C clear circuits are the same.

## Functional analogy — durable embodiment vs recovery admission

At a functional level only, the 7090 resembles later systems in which a durable or potentially durable representation can exist while recovery/startup policy decides whether that representation is admitted, replayed, ignored, truncated, reformatted, or replaced before service.

The analogy stops at the relation:

```text
physical survival
    !=
authoritative recovery state
```

Magnetic-core clear, filesystem recovery, log truncation, snapshot admission, and distributed-currentness protocols use different mechanisms and historical vocabularies. No genealogy follows from the analogy.

## Philosophical interpretation — persistence can be refused by re-entry policy

The exact technical pressure point is limited but useful: a medium's capacity to continue bearing an old state does not force a machine to continue recognizing or presenting that state after a boundary event.

A bounded interpretation is:

> technical endurance includes not only whether an embodiment can remain, but whether the apparatus that returns to operation elects to carry that embodiment forward as its current state.

This is project vocabulary. It is not a claim that IBM engineers framed the 7090 in terms of `retention`, `authority`, `admissibility`, or a philosophy of memory.

The interpretation also stops short of saying that an intentionally cleared 7090 core image is analogous in every respect to modern deletion or sanitization. The physical operation, assurance goal, and historical context differ.

## Prior-art / anti-anachronism boundaries

This deepening does **not** claim:

- that IBM invented power-on clear, memory initialization, or magnetic-core startup sequencing;
- that the 7090 is the first core-memory machine to clear storage on startup;
- that all IBM machines used the 7090 policy;
- that all 7090-family revisions, options, or field configurations had identical electrical sequences without further documentation;
- that core storage necessarily preserved every old bit physically until the exact instant of the documented clear;
- that a documented Clear proves the old state was physically readable immediately beforehand;
- that ordinary `Clear` is equivalent to security `clearing`, `purging`, degaussing, or later media sanitization;
- that zeroing core storage proves forensic irrecoverability under every laboratory method;
- that Normal Off guarantees arbitrary brownout or uncontrolled-outage safety;
- that Emergency Off preserves core contents;
- that the 7090 Reset / Clear terminology is universal historical vocabulary for other manufacturers;
- that the 7090 and 1401 use the same power-control circuit;
- that the 7090 and PDP-7 share a direct design lineage;
- that later terms such as `persistence domain`, `recovery admission`, `crash consistency`, or `secure erase` were IBM's vocabulary here;
- that preserving or clearing core storage says anything by itself about peripheral state, tapes, channels, clocks, or higher-level application restart.

## Resulting bounded distinctions

```text
magnetic nonvolatility
    !=
restart preservation policy

Reset
    !=
Clear
    !=
Power On

core survives without refresh power
    !=
old core image is retained through startup

power sequencing
    !=
startup payload policy

pre-existing physical embodiment
    !=
post-startup admitted service state

startup zeroing
    !=
proof of prior physical decay

whole-memory clear
    !=
security sanitization

one IBM machine's policy
    !=
universal IBM or magnetic-core behavior
```

## Evidence strength

| Claim | Label | Evidence strength |
| --- | --- | --- |
| IBM 7090 `Reset` is documented not to affect core-storage contents | `H/P` | strong manufacturer primary, 1962 installation instructions |
| IBM 7090 `Clear` additionally resets core-storage locations to zeros | `H/P` | strong manufacturer primary, 1962 installation instructions |
| ordinary Power On requires a clear operation as power is applied | `H/P` | strong manufacturer primary, 1962 installation instructions; independently consistent with 1961 CE reference |
| 1961 CE reference describes power-on reset as setting core storage to all zeros | `H/P` | manufacturer primary, indexed archival scan; image rendering unavailable in this run |
| 7090 material nonvolatility does not entail preservation of the old logical image through startup | `E` | direct reconstruction from operation contrast |
| Reset / Clear / Power On must be treated as different retention boundaries | `E` | direct reconstruction from manufacturer semantics |
| the 7090 proves all core machines intentionally clear memory on startup | `X` | rejected; 1401/PDP-7 provide counterexamples |
| startup Clear is a security sanitization guarantee | `X` | rejected; assurance objective and verification absent |

## What this changes in Case 02

The existing Case 02 power-transition evidence already established:

```text
quiescent magnetic retention
    !=
power-transition immunity
    !=
whole-machine execution continuity
```

The 7090 adds a different axis:

```text
quiescent magnetic retention
    !=
policy to preserve the old payload across re-entry
```

This partially closes the former `earlier machine-specific power-transition circuits and operating procedures` debt by moving the named-machine public documentation boundary back from the 1965 IBM 1401 / 1966 DEC PDP-7 examples to a **1960–1962 IBM 7090 startup-policy witness**.

It does not close the earlier 1950s Whirlwind / Memory Test Computer power-transition genealogy, arbitrary brownout behavior, or circuit-level comparison across machines.

## Related-repository routing

A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for an existing IBM 7090 power-on/core-clear treatment found no dedicated reusable slice in the current repository index.

If later work expands into:

- the full 7090 power-distribution circuit;
- motor-generator sequencing;
- 7302 core-storage hardware genealogy;
- IBM 704/709/7090/7094 startup-policy evolution;
- cross-vendor power-control design history;

that broader engineering history belongs primarily in `computing-archaeology`.

`technical-retention` should keep only the bounded relation among remanent substrate capability, transition behavior, startup authority, and the post-restart state admitted to service.

## Open work deliberately left outside this slice

- pre-1960 / 1950s named-machine startup and shutdown procedures for core memory;
- Whirlwind / Memory Test Computer power-transition primary evidence;
- direct circuit-level analysis of the 7090's clear path and 7302 core-storage drivers;
- exact comparison of IBM 7090, 7094, 1401, and System/360 restart-state policies;
- controlled brownout / partial-rail behavior;
- evidence for the physical readability of a pre-existing 7090 core pattern immediately before startup clear;
- field-service reports showing actual failure or retention outcomes under malformed transitions;
- security-remanence experiments on cleared historical core planes.

These are separate historical-engineering or experimental tasks, not prerequisites for the bounded conclusion established here.

## Source list

1. IBM, *IBM 7090 Data Processing System — Customer Engineering Instruction-Reference*, Form 223-6895-1, Major Revision, September 1961. Preserved scan: <https://www.bitsavers.org/pdf/ibm/7090/ce/223-6895-1_7090_CE_Reference_System_Fundamentals_7100_7151_7606_Sep61.pdf>.
2. IBM, *Installation Instructions: IBM 7090 Data Processing System*, archived 1962-04-09 scan. Preserved scan: <https://bitsavers.computerhistory.org/pdf/ibm/7090/ce/Installation_Instructions_IBM_7090_Data_Processing_System_19620409.pdf>.
3. IBM, *709·7090 Data Processing System — General Information Manual*, August 1960. Preserved scan: <https://bitsavers.computerhistory.org/pdf/ibm/7090/D22-6508-2_709_7090_General_Information_Manual_Aug1960.pdf>.
4. Bitsavers IBM 7090 Customer Engineering directory, used to verify the preserved document set and neighboring 1959/1961/1962 manuals: <https://bitsavers.computerhistory.org/pdf/ibm/7090/ce/>.

## Final bounded conclusion

The IBM 7090 is a useful reminder that **nonvolatility is a capability of a retained physical relation, not a promise that every machine boundary preserves the previous logical image**. IBM's 1962 instructions explicitly let `Reset` leave core contents unchanged while `Clear` zeros them, and ordinary Power On requires that clear. The same core substrate therefore participates in different retention outcomes depending on the operation class selected by the machine.

For this repository the durable result is:

```text
material capacity to persist
    + transition behavior
    + startup operation / authority
    -> post-boundary retained service state
```

The terms after the plus signs are analytically distinct. A core can be nonvolatile and still be deliberately forgotten at startup.