# technical-retention

> **How does a state outlive the moment that produced it?**

`technical-retention` is a research repository about **technical retention**: the material, logical, operational, and philosophical conditions under which a state, trace, inscription, value, or record remains available beyond the moment in which it was produced.

This is **not simply a history of computer memory or storage devices**. Those histories already exist, and much of the engineering history is already covered in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology).

The central question here is different:

> What does it technically mean for something to remain?

A bead on an abacus, a wheel left at an angle, a relay state, a flip-flop, a mercury delay line, a magnetic core, a DRAM cell under refresh, a disk sector, trapped charge in Flash, an SSD logical block, a replicated object, and a distributed consensus state can all be studied as different answers to that question.

The project therefore joins two lines that are usually separated:

1. **exact technical history and engineering reconstruction** — what physical state is retained, by what mechanism, for how long, at what cost, with what maintenance, and through what addressing and recovery machinery;
2. **philosophy and media theory of technics, memory, temporality, inscription, availability, and forgetting** — especially Bernard Stiegler, Martin Heidegger, Wolfgang Ernst, media archaeology, and related work.

The point is not to decorate engineering history with philosophical quotations. Philosophy must survive contact with mechanisms, and technical analogies must not be projected backward as historical actors' own concepts.

---

## The basic distinction

A conventional storage history asks:

```text
What devices existed?
Who invented them?
How much did they store?
How fast were they?
What replaced them?
```

This project asks:

```text
What is the retained state?
        ↓
What physically distinguishes one state from another?
        ↓
What prevents the distinction from disappearing?
        ↓
Does retention require continuous work, refresh, circulation, power, repair, or replication?
        ↓
How is the state addressed and recovered?
        ↓
Who or what decides that two recoveries count as "the same" retained thing?
        ↓
How can the state be changed, erased, corrupted, forgotten, copied, migrated, or made unavailable?
        ↓
What form of temporality does this mechanism impose?
```

A stored thing is therefore not assumed to be a static object. In many systems, apparent persistence is the visible effect of continuous activity.

---

## A first technical intuition

Consider a deliberately heterogeneous chain:

```text
abacus bead position
    → a numerical state persists spatially between operations

mechanical wheel / counter
    → angular or positional configuration retains intermediate state

relay / latch / flip-flop
    → an electrical circuit maintains a discrete logical distinction

delay-line memory
    → retention is recirculation through time

Williams tube / DRAM
    → retention includes periodic restoration or refresh

magnetic core
    → remanent magnetization retains state without continuous power

magnetic disk
    → retention becomes spatial address + magnetic configuration + servo/control machinery

Flash
    → retained charge survives power loss, while programming and erasure alter the medium and introduce wear

SSD
    → a logical block persists only through mapping, garbage collection, ECC, wear management, and replacement of physical cells

replicated / distributed storage
    → a logical fact may persist even though no single physical copy is privileged or permanent
```

This chain is a **research heuristic**, not a claim that all of these mechanisms are historically or philosophically identical.

For example, describing an abacus as `register-like` may be a useful **functional reconstruction**, but it would be anachronistic to claim that historical abacus users possessed the modern computer-architecture concept of a register.

---

## Core dimensions

Every substantial case should try to answer as many of these dimensions as the evidence permits:

| Dimension | Question |
| --- | --- |
| State | What exactly is being retained? |
| Substrate | What physical distinction embodies the state? |
| Retention interval | For how long does it remain recoverable? |
| Volatility | What disappears when power, motion, temperature control, or maintenance stops? |
| Maintenance | What work must continue for the state to appear persistent? |
| Addressability | How can a particular retained state be selected? |
| Access geometry | Sequential, random, associative, indexed, temporal, spatial? |
| Read semantics | Does reading preserve, disturb, or destroy the state? |
| Write semantics | What physical operation creates or changes the state? |
| Erasure | What does it mean to delete or reset it? |
| Failure | How does retention fail? Drift, leakage, wear, noise, media damage, controller loss, bit rot? |
| Redundancy | Is persistence local, duplicated, coded, replicated, or reconstructed? |
| Identity | Why do multiple readings/copies count as the same retained object or value? |
| Latency | What temporal distance separates request from recovery? |
| Energy | What energy is required to retain, refresh, access, move, or rewrite the state? |
| Labor | Which operators, maintainers, manufacturing workers, software, firmware, controllers, or institutions sustain retention? |
| Forgetting | Is forgetting passive decay, explicit erasure, overwrite, loss of index, loss of key, policy, or deliberate destruction? |
| Migration | Can the retained state survive a change of substrate? What must remain invariant? |

These dimensions make it possible to compare technologies without pretending they are the same technology.

---

## Philosophical and media-theoretical spine

### Bernard Stiegler — technics and tertiary retention

Stiegler's work is a central starting point because it treats technical supports as constitutive of memory and temporality rather than as optional containers added after human cognition is complete.

This project will use `tertiary retention` carefully: not as a synonym for every computer memory cell, but as a way to ask how exteriorized traces and technical supports condition what can be remembered, repeated, inherited, and anticipated.

### Martin Heidegger — technics and availability

Heidegger's analysis of modern technology and `Bestand` / standing-reserve is relevant to the transformation of things into what can be ordered, called upon, and made available for further ordering.

But an explicit methodological rule applies:

> **Bestand is not a synonym for computer storage.**

A disk block, database row, object-store object, or cached page may help us test questions of technical availability and ordering, but the philosophical concept must not be collapsed into an engineering noun merely because the English words look similar.

### Wolfgang Ernst — media archaeology and technical memory

Ernst is the closest prior art to this project's technical-philosophical interface. His media archaeology insists that "memory" in technical systems must be read at the level of actual mechanisms, timing, registers, buffers, access modes, latency, and operational processes rather than treated only as a metaphor for human or cultural memory.

His work is therefore both a major source and a warning: this repository must contribute more than a generic claim that digital media are forms of memory.

### Matthew Kirschenbaum — inscription, storage, and forensic materiality

Kirschenbaum's *Mechanisms* is important for treating digital writing through actual storage mechanisms and for foregrounding erasure, variability, repeatability, and survivability.

---

## Prior-art boundary

Large parts of the territory already have excellent work. The project should **reuse rather than rediscover** them.

Important starting points include:

- Wolfgang Ernst, *Digital Memory and the Archive* and his work on technical storage and media archaeology;
- Bernard Stiegler, *Technics and Time* and later work on tertiary retention;
- Martin Heidegger, "The Question Concerning Technology";
- Matthew G. Kirschenbaum, *Mechanisms: New Media and the Forensic Imagination*;
- Computer History Museum, [The Storage Engine](https://www.computerhistory.org/storageengine/), a major technical-historical timeline from early inscription to modern storage;
- conventional computer architecture and memory-system literature on registers, cache, SRAM, DRAM, disks, Flash, and storage hierarchy.

See [`docs/PRIOR_ART.md`](docs/PRIOR_ART.md) for the working map.

---

## Relationship to other repositories

This project is intentionally linked to, but not merged with, several existing repositories.

### [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology)

**Engineering and historical evidence source.**

That repository asks why historical computing designs made engineering sense under period constraints. It already has substantial work on delay lines, Williams tubes, drums, magnetic core, tape, disk, HBM, manufacturing, materials, reliability, and related systems.

`technical-retention` should link to or reuse those technical treatments instead of rewriting them unless a retention-specific analysis requires a different argument.

### [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history)

**Methodological guard against anachronism.**

The distinction between historical actors' questions and later reconstruction applies here directly. A modern researcher may describe a historical mechanism as `register-like`, `persistent`, or `addressable`; that does not prove that historical actors formulated the same conceptual problem in those terms.

### [`tmzncty/mechanical-computing-playground`](https://github.com/tmzncty/mechanical-computing-playground)

**Hands-on reconstruction and experiments.**

If a retention claim can be made visible by a mechanical or executable model, implementation may belong there while this repository keeps the conceptual and comparative analysis.

See [`RELATED_REPOS.md`](RELATED_REPOS.md).

---

## Repository map

- [`docs/METHOD.md`](docs/METHOD.md) — evidence layers, anti-anachronism rules, and comparison method.
- [`docs/PRIOR_ART.md`](docs/PRIOR_ART.md) — what has already been done and where this project can still contribute.
- [`docs/TECHNICAL_SPINE.md`](docs/TECHNICAL_SPINE.md) — provisional mechanism lineage from retained position to distributed logical state.
- [`docs/PHILOSOPHICAL_SPINE.md`](docs/PHILOSOPHICAL_SPINE.md) — Stiegler, Heidegger, Ernst, Kirschenbaum, and conceptual questions.
- [`docs/SYNTHESIS_AUDIT_01_MAINTAINED_PERSISTENCE.md`](docs/SYNTHESIS_AUDIT_01_MAINTAINED_PERSISTENCE.md) — first evidence-led audit of a provisional thesis, including counterexamples to a universal active-maintenance model.
- [`docs/SYNTHESIS_AUDIT_02_TEMPORAL_TRANSPORT.md`](docs/SYNTHESIS_AUDIT_02_TEMPORAL_TRANSPORT.md) — audit of the storage/transfer proposition against grounded cases, retaining only a controlled recoverability-relation model across time.
- [`docs/SYNTHESIS_AUDIT_03_ADDRESSABILITY.md`](docs/SYNTHESIS_AUDIT_03_ADDRESSABILITY.md) — audit separating retention from designation, selection/resolution, currentness/admissibility, and recovery across grounded cases.
- [`docs/SYNTHESIS_AUDIT_04_PRIVILEGED_LOCATION.md`](docs/SYNTHESIS_AUDIT_04_PRIVILEGED_LOCATION.md) — audit distinguishing physical-token replacement, stable physical home, metadata-mediated relocation, replaceable replicas, and temporary protocol authority.
- [`ROADMAP.md`](ROADMAP.md) — staged research program.
- [`RELATED_REPOS.md`](RELATED_REPOS.md) — cross-repository boundaries and reuse rules.
- [`AGENTS.md`](AGENTS.md) — research protocol for human and AI contributors.

---

## Current research theses — provisional, not conclusions

The project begins with several hypotheses to test rather than assume:

1. **Persistence is often an achieved relation, not a maintenance-free property.** Some retained states remain quiescently; others require scheduled reconstruction, access-triggered restore, remapping, or repair. The first question is which layer is being kept persistent and what event creates its maintenance obligation. See the bounded [maintenance audit](docs/SYNTHESIS_AUDIT_01_MAINTAINED_PERSISTENCE.md).
2. **Storage can be analyzed as transfer across temporal distance, but only as a recoverability model.** A state established at `t0` may remain or be reconstructed as an agreed recoverable equivalent at `t1`; this does not imply literal physical motion, one unchanging carrier, or active maintenance, and it does not replace mechanism-level distinctions. See the bounded [temporal-transport audit](docs/SYNTHESIS_AUDIT_02_TEMPORAL_TRANSPORT.md).
3. **Addressability is a separate operational relation layered onto retention.** A state may persist without being autonomously or cheaply selectable, while a stable logical designation can survive changes in physical embodiment. Analyze designation and selection/resolution separately from currentness/admissibility and read/recovery; do not equate address with physical location or addressability with availability. See the bounded [addressability audit](docs/SYNTHESIS_AUDIT_03_ADDRESSABILITY.md).
4. **Forgetting has mechanisms.** Decay, overwrite, erase, deletion, unlinking, key destruction, failed indexing, incompatible formats, and institutional loss are different technical forms of forgetting.
5. **Logical persistence can become detached from any one permanent physical home without becoming placeless.** Some systems keep a stable location while repeatedly reconstructing physical state; mapped and distributed systems go further by letting identity survive relocation or replica replacement through retained mapping, placement, version, and authority relations. Treat this as a mechanism comparison, not a one-way historical law. See the bounded [privileged-location audit](docs/SYNTHESIS_AUDIT_04_PRIVILEGED_LOCATION.md).
6. **The more reliable retention becomes, the more its maintenance disappears from experience.** This makes maintenance labor and hidden machinery historically important.

Each thesis must be vulnerable to counterexamples.

---

## One rule above all

> **Do not confuse an analogy that helps us think with a historical fact that must be proven.**

The repository may compare an abacus bead with a register, a delay line with temporal circulation, DRAM refresh with active maintenance, or distributed replication with substrate-independent persistence. But every comparison must state whether it is:

- historical evidence;
- engineering reconstruction;
- philosophical interpretation;
- functional analogy;
- or experiment.

Those layers must never silently collapse into one another.

---

## Status

Early research-program scaffold. The first phase is to establish prior art, vocabulary, a defensible technical spine, and several narrowly sourced case studies before attempting a grand synthesis.
