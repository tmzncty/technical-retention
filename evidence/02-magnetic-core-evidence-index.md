# Case 02 evidence index — magnetic-core retention, destructive read, transition boundaries

**Case:** [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md)  
**Current status:** `grounded`  
**Index role:** navigation and evidence-layer separation; this file does not promote maturity by itself.

---

## What Case 02 is actually about

Case 02 is not a general history of ferrite-core memory.

Its retention question is narrower:

> How can a medium retain a magnetic state without refresh or power, yet require active reconstruction because ordinary reading can destroy the physical representation that was just observed?

The core relation is:

```text
remanent state at rest
    ↓
select + destructive sense
    ↓
old logical value becomes known
    ↓
restore / regenerate
    ↓
remanent state re-established
```

That relation creates several distinct boundaries which must not be collapsed into the single adjective `nonvolatile`.

---

## Evidence chain map

### Chain 1 — 1951–1954 grounding: remanence, destructive read, rewrite, implemented memory

**Record:** [`02-magnetic-core-1951-1954-grounding.md`](02-magnetic-core-1951-1954-grounding.md)

**Role:** principal grounding chain.

This record anchors the case in early MIT / Project Whirlwind material rather than in later textbook summaries.

It supplies evidence for:

- two stable magnetic states;
- coincident-current selection;
- sensing through magnetic reversal;
- destructive read;
- rewrite / regeneration;
- implemented early core-memory behavior;
- bounded nondestructive-read counterexamples.

**What it does not prove:**

- every later production core-memory organization;
- universal numerical retention lifetime;
- whole-machine automatic restart;
- or invention priority over all parallel work.

### Chain 2 — 1964 TCM-32: selected clear/write versus whole-memory clear

**Record:** [`02-1964-tcm32-clear-write-memory-clear-deepening.md`](02-1964-tcm32-clear-write-memory-clear-deepening.md)

**Role:** later named-product operation vocabulary.

The TCM-32 evidence separates:

```text
selected-address clear/write
    !=
whole-stack Memory Clear
    !=
read/regenerate
```

It grounds the fact that a nonvolatile core array can still expose explicit electrical operations that overwrite/reset stored state at different scopes.

**Do not infer:** Flash-style erase semantics or security-grade sanitization.

### Chain 3 — 1965–1966 power transitions: remanence versus transition control

**Record:** [`02-1965-1966-core-power-transition-retention-deepening.md`](02-1965-1966-core-power-transition-retention-deepening.md)

**Role:** named-machine power-boundary evidence.

This chain separates:

```text
state survives while power is absent
    !=
state is immune to power-transition disturbances
    !=
whole machine resumes computation
```

Controlled sequencing around the medium is itself retention work even though the core does not need periodic refresh while idle.

### Chain 4 — 1966–1969 PDP-8 diagnostic: power-cycle retention as an observed machine property

**Record:** [`02-dec-1966-1969-pdp8-memory-power-cycle-diagnostic-deepening.md`](02-dec-1966-1969-pdp8-memory-power-cycle-diagnostic-deepening.md)

**Role:** maintenance/experiment boundary.

The DEC power-on/off diagnostic makes bit dropout/pickup after a simulated power failure something an assembled machine can test.

The important split is:

```text
substrate remanence
    !=
machine transition requirement
    !=
diagnostic coverage
    !=
a particular test pass/fail
    !=
root-cause localization
```

A post-cycle wrong bit does not, by itself, prove that ferrite remanence was the failing physical mechanism.

### Chain 5 — 1970–1973 operating margins: retained payload versus temperature-dependent control

**Record:** [`02-1970-1973-core-temperature-compensation-operating-margin-deepening.md`](02-1970-1973-core-temperature-compensation-operating-margin-deepening.md)

**Role:** later prior-art/control-architecture deepening.

This chain separates remanent payload state from the temperature-dependent drive/inhibit relationships required to access it reliably.

It also preserves a counterexample discipline: different designs used different compensation strategies, so active temperature compensation is not a universal property of all core memories.

### Chain 6 — 1991 security vocabulary: clear, purge, degauss

**Record:** [`02-1991-ncsc-core-clearing-purging-degaussing-deepening.md`](02-1991-ncsc-core-clearing-purging-degaussing-deepening.md)

**Role:** later security-assurance vocabulary.

This chain prevents a common category error:

```text
machine-defined Memory Clear
    !=
security clearing objective
    !=
purging objective
    !=
degaussing operation
```

The 1991 terms are later security vocabulary and must not be projected backward into 1950s or 1964 engineering documents.

### Chain 7 — Papian 1952 facsimile: half-select disturbance and margin detail

**Record:** [`70-papian-1952-half-select-disturbance-facsimile-deepening.md`](70-papian-1952-half-select-disturbance-facsimile-deepening.md)

**Role:** shared evidence with Case 70.

Case 02 consumes only the retention-relevant result: a selected-address architecture must preserve neighboring states under repeated nonselecting disturbances.

The quantitative pulse-pattern and margin analysis remains owned by Case 70 rather than being duplicated here.

### Chain 8 — 1974–1975 Victor: power-fail admission versus an in-flight restore

**Record:** [`02-victor-1974-1975-core-power-fail-inflight-restore-boundary-deepening.md`](02-victor-1974-1975-core-power-fail-inflight-restore-boundary-deepening.md)

**Role:** new power/access-pipeline boundary.

U.S. Patent 3,906,453 places in one named design:

- a nonvolatile magnetic-core RAM;
- a first-part destructive read;
- a second-part write/restore;
- and a `memory fail` path that suppresses further command acceptance/output under abnormal power conditions.

The bounded conclusion is:

```text
power-fail command gating
    !=
proof that an already-started destructive-read restore completed
```

The source does not provide the needed rail-hold-up/current-cycle timing proof. This is therefore a sharpened boundary, not a claim that Victor hardware was unsafe.

---

## Cross-case layer map

Case 02 should be read with several adjacent cases, but their mechanisms and historical vocabularies stay separate.

### Case 70 — selection margin / half-select disturbance

Case 70 owns the narrower quantitative question of how the selection regime preserves unselected or half-selected cores.

Relation:

```text
addressability
    creates
neighbor-disturbance retention constraints
```

This is different from destructive-read restoration of the selected core.

### Case 86 — PDP-8 power-fail save and restart

[`../cases/86-dec-pdp8-core-power-fail-auto-restart.md`](../cases/86-dec-pdp8-core-power-fail-auto-restart.md)

Case 86 asks what survives when a computation crosses a power failure.

Its bounded relation is:

```text
volatile CPU/control state
    ↓ emergency save
core-resident state
    ↓ restart + software restore
reconstructed execution state
```

Case 02 instead asks what happens inside a core-memory access:

```text
remanent bit
    ↓ destructive read
restore obligation
    ↓ rewrite
remanent bit
```

Therefore:

```text
cell/word restore closure
    !=
whole-machine continuation closure
```

### Case 03 — DRAM destructive sensing / restoration

DRAM is useful only as a functional analogy for the relation:

```text
sense
    → state disturbance
    → restoration
```

It must not be treated as the same physical retention mechanism. DRAM charge storage is volatile and refresh-dependent; magnetic core relies on remanence while idle.

### Synthesis 26 — typed event/state persistence horizons

[`synthesis26-reset-event-state-persistence-horizon-deepening.md`](synthesis26-reset-event-state-persistence-horizon-deepening.md)

The Victor deepening reinforces the synthesis rule that an event label such as `power fail` or `reset` is insufficient by itself.

The evidence must identify at least:

```text
state class
× event class
× access phase
× authority/admission behavior
× survival/closure semantics
× evidence layer
```

---

## Current comparison model

Case 02 can now be decomposed into a larger relation without treating every arrow as the same kind of retention:

```text
remanent payload state
    ↓
coordinate selection
    ↓
neighbor half-select disturbance constraint
    ↓
destructive sense
    ↓
read-result capture
    ↓
restore / rewrite obligation
    ↓
post-access remanent state
    ↓
power-transition control
    ↓
post-transition validation
```

Alongside it sit separate state classes:

```text
payload magnetic state
    !=
sense/output latch state
    !=
controller timing state
    !=
power-fail admission state
    !=
CPU execution state
    !=
peripheral/control state
```

This is why `core memory is nonvolatile` is a true but insufficient characterization for retention research.

---

## Historical record / engineering reconstruction boundaries

### Historical record presently grounded

The repository has period or named-product evidence for:

- remanence and stable magnetic states;
- destructive read and rewrite;
- implemented read/regenerate cycles;
- half-select disturbance as a design concern;
- selected-word and whole-stack clearing operations;
- controlled power-transition retention;
- maintenance testing of power-cycle bit preservation;
- temperature-dependent access-margin control;
- later security clearing/purging/degaussing vocabulary;
- a 1974–1975 controller combining destructive read/restore phases with a power-fail admission signal.

### Engineering reconstruction presently warranted

The evidence supports separating:

```text
idle retention
    !=
read invariance
    !=
restore completion
    !=
power-transition immunity
    !=
whole-machine restart
    !=
diagnostic qualification
    !=
security sanitization
```

It also supports the new in-flight relation:

```text
stop admitting new memory work
    !=
prove already-admitted destructive work reached stable closure
```

### What remains only functional analogy

Comparisons to DRAM, later destructive-read NVM, transaction drain, persistence-domain closure, or distributed repair are useful only at the relation level unless direct historical lineage is separately established.

### Philosophical interpretation ceiling

Case 02 can support the bounded observation that logical continuity may depend on reconstruction after an act of observation.

It does not establish a universal philosophy of memory, identity, observation, or forgetting.

---

## Explicit anti-collapse rules

Do not write any of the following as equivalences:

```text
nonvolatile
    = maintenance-free

nonvolatile
    = immune to arbitrary power transitions

read result available
    = restore complete

power-fail signal asserted
    = in-flight destructive read safely closed

main-memory payload survived
    = CPU/peripheral execution state survived

Memory Clear
    = security purge

passing one power-cycle diagnostic
    = universal retention lifetime

half-select robustness
    = selected-core restore correctness

modern destructive-read NVM mitigation
    = direct descendant of historical core controller design
```

---

## Open research debt, ordered by value

### P1 — current-cycle behavior after power-fail detection

Find a production controller/service manual that explicitly answers:

- whether a memory cycle already underway is completed;
- whether new cycles are inhibited before sense;
- where the power-fail threshold lies relative to the current regulators;
- what hold-up time remains after detection;
- and whether restore completion is observable.

This is now the highest-value Case 02 retention gap.

### P2 — phase-specific power-failure diagnostics

Look for maintenance procedures or engineering reports that interrupt power at controlled points in read/regenerate timing.

A useful source would distinguish:

```text
before sense
vs
between sense and restore
vs
after restore
```

### P3 — named-machine hold-up evidence beyond PDP-8/E

Case 86 already has later KP8-E capacitor-hold-up evidence. The next step is a separate named core-memory controller where the hold-up relation is documented at the **memory-cycle** level rather than only at the whole-machine emergency-save level.

### P4 — product/circuit provenance for Victor US 3,906,453

Locate Victor service manuals, parts lists, schematics, or product literature that show whether and where the patented controller shipped.

The patent alone should remain a design/document witness until that link is established.

### P5 — counterexample strategy

Find a core-memory design that solves the same boundary differently, for example:

- suppress destructive sense early enough that no restore debt is created;
- guarantee drain of the current cycle after fail detection;
- retain enough analog energy for one final regenerate;
- or explicitly treat interrupted cycles as invalid and recover by another mechanism.

A strong counterexample would improve the comparison more than another generic core-memory description.

---

## Related-repository boundary

The broader history of core-memory invention, ferrite materials, weaving/manufacture, labor, economics, and machine adoption belongs primarily in:

- [`tmzncty/computing-archaeology/docs/memory/why-core-memory-was-worth-weaving.md`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md)
- [`tmzncty/computing-archaeology/experiments/core-memory/`](https://github.com/tmzncty/computing-archaeology/tree/main/experiments/core-memory)

Case 02 should reuse that work and add only retention-specific evidence and comparisons.

---

## Maturity decision

**Case 02 remains `grounded`.**

The new Victor evidence improves the power/access boundary but does not justify a promotion because the most interesting new question is deliberately still open at the implementation level:

```text
how is an already-started destructive-read cycle closed
when power-fail detection races the read/restore sequence?
```

A future promotion should require at least one named implementation with direct current-cycle/hold-up evidence or an equivalent phase-specific validation record, not simply more secondary statements that core is nonvolatile.
