# Case 02 Deepening — Magnetic-Core Power-Off Retention, Transition Hazards, and Restart Apparatus (1965–1966)

## Purpose

This record deepens [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md) around one bounded question that the main case already warns about but does not yet ground with named-machine operating evidence:

> if magnetic core is nonvolatile while unpowered, what still has to be preserved or controlled when an actual computer is powered down and powered back up?

The answer is not simply `nothing`. Two period machine manuals show that core contents could be intended to survive power removal while the **transition into and out of the powered state** still required explicit operational or circuit protection.

This deepening therefore separates:

```text
quiescent magnetic retention
    !=
power-transition immunity
    !=
whole-machine execution continuity
```

Claim layers follow repository policy: **Historical record**, **Engineering reconstruction**, **Functional analogy**, and **Philosophical interpretation** remain distinct.

## Sources inspected

### IBM 1401 Data Processing System — Operator's Guide, Form A24-3144-2

Manufacturer document, **Major Revision, March 1965**. The original IBM publication is accessed here through archival mirrors rather than a current IBM origin host.

Archival copies / records:

- <https://bitsavers.trailing-edge.com/pdf/ibm/1401/A24-3144-2_1401_operGuide.pdf>
- <https://www.eserviceinfo.com/downloadsm/90766/IBM_A24-3144-2%201401%20operGuide.html>
- Computer History Museum 1401 restoration index linking the same IBM manual: <https://ibm1401.computerhistory.org/>

The relevant operating instructions are on printed p. 129 in the archived copy. The guide tells the operator to place the 1401 mode switch in `ALTER` for controlled power transitions. On power-on in that mode, **information in core storage is retained**. On power-off in that mode, **information is retained in core storage until power is turned on again**. The same instructions also mention relay sequencing used to avoid damage from repeated switching.

**Evidence boundary:** this is named-machine operating evidence for an IBM 1401 and its prescribed controlled procedure. It is not a universal guarantee that every magnetic-core computer preserves all memory through every arbitrary outage or malformed transition.

### Digital Equipment Corporation PDP-7 Maintenance Manual, F-77A (1966)

Manufacturer maintenance manual for PDP-7 systems with serial numbers 100 and above, archived as:

- <https://bitsavers.org/pdf/dec/pdp7/F-77A_pdp7maint_1966.pdf>
- alternate archival mirror: <https://www.soemtron.org/downloads/decinfo/f77apdp7maint1966.pdf>

The relevant power-control description is printed p. 3-6. DEC states that during turn-on the memory is energized only after a delay allowing AC transients to decay. During turn-off, the **memory power supplies are de-energized immediately while computer logic power remains for five seconds**. The manual gives the reason explicitly: the delay prevents switching transients from producing current surges that could destroy information stored in core memory.

During the same turn-on delay, `PWR CLK` / `PWR CLR` activity repeatedly clears the RUN and memory-control flip-flops and establishes initial conditions in peripheral equipment, so a stored program is not accidentally started or disturbed.

**Evidence boundary:** this is a PDP-7/A-family power-control design witness. It demonstrates that one core-memory computer treated power-transition circuitry as part of preserving core contents while intentionally resetting other machine state. It does not establish identical sequencing on IBM, Whirlwind, or every core-memory system.

## Historical record — IBM distinguishes retained core contents from the act of turning power on or off

The IBM 1401 guide does not present core retention as an abstract materials fact only. It places retention inside an operator procedure:

```text
mode switch -> ALTER
power transition
core information retained
```

The important historical fact is not that `ALTER` magically supplies the remanence. Magnetic remanence is already the physical basis of the storage element. The manual instead shows that IBM treated **how the powered system enters or leaves service** as relevant to preserving the stored information.

The wording also blocks a careless universalization. The guide's promise is tied to the documented operating sequence; it is not a blanket statement about every uncontrolled interruption.

## Historical record — PDP-7 explicitly protects nonvolatile core from switching transients

DEC's maintenance manual is even more explicit about the transition hazard. The core array can retain information without powered refresh, yet the surrounding electronics can still generate destructive currents while supplies rise or fall.

The PDP-7 design therefore sequences power domains:

```text
turn on:
logic/control powered first
    -> wait for AC transients to decay
    -> energize memory

turn off:
de-energize memory immediately
    -> keep logic power for ~5 s
```

The manual states that this sequencing prevents current surges from destroying core-memory information.

This is a direct counterexample to the shortcut:

> `nonvolatile = power transitions are irrelevant`.

They are not irrelevant. The medium may not require power to retain its quiescent magnetic state, while the **system transition** can still threaten that state electrically.

## Historical record — preserved core payload coexists with deliberately reset control state

The PDP-7 manual also separates two classes of machine state during turn-on.

While the core contents are being protected from destructive transients, power-clock / power-clear logic clears RUN and memory-control flip-flops and establishes peripheral initial conditions. In other words:

```text
core payload: intended to remain undisturbed
selected control state: intentionally reinitialized
```

The stored program may physically remain in core, but the processor is prevented from simply resuming an uncontrolled pre-power-transition execution state.

This grounds a named-system version of a distinction already stated cautiously in Case 02:

> **element-level nonvolatility != whole-machine restart persistence**.

## Engineering reconstruction — power-off is a state; power-down and power-up are operations

The manuals support a useful three-stage model:

1. **powered operation** — drivers, sense circuits, timing, and control state are active;
2. **quiescent unpowered interval** — remanent magnetization can preserve core contents without refresh power;
3. **power transition** — supply rails and logic states move through intermediate conditions that can create unintended currents or commands.

The engineering implication is:

> **surviving stage 2 does not prove immunity during stages 1→2 or 2→1.**

This is not a new physical theory of ferrite. It is a system reconstruction directly motivated by the machine manuals' operating and circuit precautions.

## Engineering reconstruction — nonvolatile medium can still require retention apparatus at its boundary

A narrow definition of `maintenance` might say that magnetic core needs none while idle because there is no periodic refresh. That is correct for the quiescent bit state, but incomplete for an operational computer.

The PDP-7 supplies a different kind of retention work:

- not periodic restoration of the stored bit;
- not continuous recirculation;
- but **transition control that prevents the support electronics from accidentally rewriting or disturbing the bit**.

Thus:

```text
no steady-state refresh obligation
    !=
no system-level retention obligation
```

The obligation is concentrated at a boundary event rather than repeated on a deadline.

## Engineering reconstruction — restart continuity is compositional

The two manuals support a more precise restart model:

```text
retained core contents
+
safe power-transition behavior
+
known processor/control initialization
+
operator/software restart procedure
=
possible useful restart continuity
```

No single term in that sum is equivalent to the others.

In particular:

- physical retention of words does not preserve registers that are deliberately cleared;
- preservation of words does not prove that external devices retain compatible state;
- safe power sequencing does not prove that a program can resume at the exact interrupted instruction;
- restartability does not imply that every power failure was handled gracefully.

This is why `nonvolatile` is a property of the retained substrate relation, not a complete crash-consistency or restart contract.

## Functional analogy — persistence-domain boundaries, without shared mechanism

At a functional level only, the PDP-7 case resembles later systems in which a durable payload survives while volatile control state must be reconstructed or reinitialized before service resumes.

The analogy stops at that relation. Magnetic-core remanence, modern nonvolatile media, persistent-memory domains, journal replay, and distributed recovery use different substrates, failure models, and protocols. No genealogy is inferred from the comparison.

## Philosophical interpretation — endurance can depend on the manner of re-entry

The technical fact is unusually concrete: a state can remain materially present while unpowered and still be endangered by the operation that reconnects it to an active machine.

A bounded interpretation is therefore:

> persistence is not exhausted by surviving absence of power; availability again depends on a controlled re-entry into an operational apparatus.

This is a project interpretation of the engineering evidence, not language attributed to IBM or DEC engineers.

## Prior-art and anti-anachronism boundaries

This deepening does **not** claim:

- that IBM or DEC invented power-safe core-memory sequencing;
- that the IBM 1401 and PDP-7 use the same power-control circuit;
- that every core-memory computer preserves contents over arbitrary outage, brownout, transient, or service procedure;
- that preserved core contents imply exact instruction-level resume;
- that magnetic-core nonvolatility is equivalent to modern persistent-memory semantics;
- that control flip-flops cleared by PDP-7 power logic are themselves stored in the core array;
- that later terms such as `persistence domain`, `crash consistency`, or `NVDIMM` were historical vocabulary for these systems.

The broader history of power sequencing, fail-safe memory electronics, and machine restart belongs primarily in `tmzncty/computing-archaeology`. This record exists only to tighten Case 02's retention boundary.

## Resulting bounded distinctions

```text
core remanence while unpowered
    !=
power-transition immunity

power-off interval
    !=
power-down / power-up operation

retained core payload
    !=
retained processor-control state

stored program remains
    !=
program automatically resumes

nonvolatile medium
    !=
maintenance-free system boundary

safe power sequencing
    !=
crash consistency

named IBM / DEC behavior
    !=
universal magnetic-core contract
```

## Open work deliberately left outside this slice

- earlier 1950s machine-specific power-transition circuits and operating procedures;
- Whirlwind / Memory Test Computer startup-shutdown primary evidence;
- exact circuit-level comparison between IBM 1401 and DEC PDP-7 power sequencing;
- behavior under uncontrolled brownouts and partial-rail failures;
- diagnostic or restoration experiments on surviving historical machines;
- genealogy from core-memory power protection into later semiconductor-memory power-fail designs.

Those are separate historical-engineering or experimental tasks rather than prerequisites for the bounded retention distinction established here.
