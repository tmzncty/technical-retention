# Abacus as Retained Position

> **Research question:** when does a spatial configuration inside a calculation count as technical retention rather than merely as a visible aid?

**Status:** first-pass case study; historically grounded, conceptually provisional.

## Scope

- **Object / system:** counting boards and especially the Chinese bead abacus (`算盤`, suanpan).
- **Date range:** long prehistory of counting devices, with the historical core of this case centered on late-imperial Chinese bead-abacus practice and Cheng Dawei's *Suanfa Tongzong* (1592).
- **Why this case matters:** it is a deliberately difficult boundary case. The abacus is not a stored-program computer, but its bead configuration can preserve a numerical state across successive operations. This lets the project test whether `retention` can be defined before electronic memory without quietly projecting modern computer architecture backward.

This case does **not** claim that the abacus is the historical ancestor of the CPU register. It asks a narrower functional question:

> Can a manually maintained spatial configuration serve as an operationally retained intermediate state?

The answer appears to be yes, provided that the claim is kept at the level of functional reconstruction rather than historical vocabulary.

---

## Claim ledger

| ID | Claim | Type | Status |
| --- | --- | --- | --- |
| A1 | Abaci perform arithmetic by moving counters or beads into spatial configurations. | historical record | strong |
| A2 | Chinese suanpan practice used place-value positions and explicit rules for positioning results. | historical record | strong |
| A3 | Cheng Dawei's 1592 text contains instructions in which a completed result is left unmoved on the abacus. | historical record | strong, OCR should be checked against facsimile for quotation-level use |
| A4 | A bead configuration can therefore preserve an intermediate numerical state between operations. | engineering / operational reconstruction | strong |
| A5 | This makes the configuration `register-like` in one limited respect: a value remains available for a later operation. | functional analogy | useful but deliberately narrow |
| A6 | The abacus is a register, memory hierarchy, or direct ancestor of modern computer registers. | historical claim | **rejected** |

---

## Historical vocabulary

The most important rule is to begin with period vocabulary rather than with `register`.

Cheng Dawei's *新編直指筭法統宗* (*Suanfa Tongzong*, 1592) uses terms including:

- `筭盤` / `算盤` — abacus;
- `定位` — positioning / fixing place value;
- `實` and `法` in procedural arithmetic contexts;
- named units and decimal positions placed on the calculating surface.

The text's first volume includes a section titled `定位秘訣` and gives procedural directions for assigning positional value on the abacus. A particularly important instruction says, in substance, that after a multiplication is completed the obtained number should be left unmoved. The Chinese Text Project transcription is OCR-derived and explicitly warns that it may contain errors, so exact philological quotation should be checked against the facsimile before publication-grade use.

The point is not the modern word `state`. The historically safer observation is that a **configured board was intentionally left in place as part of an ongoing computational procedure**.

### Source anchors

- Cheng Dawei, *新編直指筭法統宗*, 1592, CText transcription, vol. 1: <https://ctext.org/wiki.pl?chapter=946408&if=en>
- Public-domain facsimile of the 1592 edition, volume 1: <https://commons.wikimedia.org/wiki/File:NLC892-411999021914-37275_%E6%96%B0%E7%B7%A8%E7%9B%B4%E6%8C%87%E7%AE%97%E6%B3%95%E7%B5%B1%E5%AE%97_%E7%AC%AC1%E5%86%8A.pdf>

---

## Historical record

### What an abacus physically does

The Smithsonian describes the abacus as a calculating device on which arithmetic is performed by sliding counters — beads, pebbles, or discs — along rods, wires, or lines. In the Chinese suanpan, counters move along rods or wires in a rectangular frame; beads above and below the crossbar carry different numerical values.

This supports a minimal historical statement:

> calculation is performed by intentionally changing a persistent spatial arrangement of counters.

Source:

- Smithsonian / National Museum of American History, "The Abacus and the Numeral Frame": <https://www.si.edu/spotlight/the-abacus-the-numeral-frame-and-counters/introduction>
- Smithsonian, "The Chinese Abacus": <https://americanhistory.si.edu/collections/object-groups/the-abacus-the-numeral-frame-and-counters/the-chinese-abacus>

### Origin is not settled enough for a simple invention story

The project should avoid the common internet narrative in which a single civilization simply "invented the abacus" at a precise date. The Smithsonian explicitly notes disagreement about how long Asian abaci have been made and whether they were influenced by Greek counting devices. The British Museum likewise treats the exact date of Chinese adoption as uncertain while describing substantial use by the Ming period.

For this repository, the disputed origin does not block the case. The retention question does not require an invention-priority claim.

Sources:

- Smithsonian, "The Chinese Abacus": <https://americanhistory.si.edu/collections/object-groups/the-abacus-the-numeral-frame-and-counters/the-chinese-abacus>
- British Museum collection essay / object record: <https://www.britishmuseum.org/collection/object/A_1909-0611-1>

### Counting rods and bead abaci should not be collapsed

Frank Swetz's historical discussion for the Mathematical Association of America treats the bead abacus as emerging from earlier Chinese counting-rod and counting-board practice and emphasizes the transition from rod numerals to a more mechanically constrained bead device. Even if particular details of chronology remain debatable, the distinction is analytically valuable:

- a **counting board** permits counters or rods to be arranged on an open surface;
- a **bead frame** constrains the counters to rods/wires and therefore constrains legal positions and motions.

That mechanical constraint matters for retention because it reduces ambiguity about where a counter belongs and what configurations are stable.

Source:

- Frank J. Swetz, "Reflections on Chinese Numeration Systems: Transition to the Abacus," Mathematical Association of America: <https://old.maa.org/press/periodicals/convergence/reflections-on-chinese-numeration-systems-transition-to-the-abacus>

---

## Retained state

The retained state is **not the bead itself**. It is the interpreted configuration of beads relative to:

1. the frame;
2. the crossbar;
3. the rod/column position;
4. the chosen place-value convention;
5. the procedural context of the calculation.

A physical configuration alone is therefore insufficient. The same arrangement can mean different numbers if the unit or radix interpretation changes.

This gives the first important result of the repository:

> **retention is substrate + configuration + interpretation.**

A future operation can use a past result only if the convention that makes the configuration meaningful also persists.

---

## Physical / logical substrate

### Physical distinction

A bead is either in a position that contributes to the represented value or in one that does not, relative to the crossbar and the conventions of the particular abacus.

The substrate is macroscopic and mechanically stable:

- wood, metal, bamboo, or similar material;
- frame and rods/wires;
- bead position under ordinary friction and gravity;
- humanly visible and manually writable state.

Unlike DRAM, there is no refresh circuit. Unlike a delay line, the state need not circulate. Unlike magnetic core, the distinction is not encoded in microscopic remanence. The persistence is simply the persistence of a mechanical arrangement until an external force changes it.

### Logical distinction

The machine does not independently interpret the value. The numerical meaning is enacted by a user who knows the place-value system and operation rules.

This is why the abacus belongs near the boundary between:

- retained **representation**;
- retained **machine state**;
- and externalized **human working state**.

---

## Retention mechanism

The state persists primarily through **passive positional stability**.

No energy must be continuously supplied by the calculating system to keep the beads in their current configuration. However, this should not be romanticized as maintenance-free persistence. Retention still assumes:

- that the frame is not bumped or tilted enough to change the configuration;
- that the operator does not accidentally disturb the beads;
- that the mapping between columns and place values remains known;
- that the calculation is not intentionally cleared.

In other words, the system has low active maintenance but nonzero environmental and procedural requirements.

---

## Addressing and access geometry

The abacus is spatially addressable by the operator.

A particular decimal position is selected by reaching a particular rod/column. This resembles indexed spatial access more than sequential media such as tape, but the analogy has limits:

- there is no electronic address decoder;
- the user performs selection;
- position has meaning through convention rather than a machine-readable address bus;
- several rods can be inspected visually in parallel.

The device therefore makes a useful point for later storage history:

> **addressability can exist as a human-machine convention before it exists as an automatic electronic mechanism.**

---

## Read semantics

Reading is normally **nondestructive at the physical level**: looking at the bead configuration does not require changing it.

However, reading is not autonomous. Interpretation requires a trained user. There is no clean separation between storage device and reader comparable to a later memory bus or storage controller.

This makes the abacus a valuable counterexample to definitions of memory that require machine-autonomous readout.

---

## Write and erasure semantics

### Write

Writing is manual repositioning of counters/beads.

The operator transforms one valid configuration into another according to arithmetic rules. Calculation is therefore not something performed elsewhere and merely copied into the abacus afterward; the transformation of the retained configuration is itself a central part of the computational process.

### Erasure / reset

Erasure is mechanical clearing or repositioning. Nothing analogous to secure erasure exists at the substrate level: once the beads have been moved, the previous arrangement normally leaves no durable trace in the frame itself.

That gives a useful distinction:

- **state persistence:** strong enough to bridge operations;
- **history persistence:** essentially absent unless separately recorded.

The abacus can retain the **current state** without retaining a log of previous states.

---

## Time

There is no intrinsic electronic retention interval. The practical interval is determined by mechanical stability and human use.

This makes the abacus radically different from later memories whose retention is characterized by leakage, refresh periods, coercivity, charge loss, or media decay.

Nevertheless, time is still structurally present:

```text
operation at t0
    ↓
beads remain configured
    ↓
operator pauses / checks / performs another step
    ↓
configuration is reused at t1
```

The configuration transports an operational value across the interval between `t0` and `t1`.

That is the minimal sense in which this case qualifies as technical retention.

---

## Maintenance and labor

The abacus exposes labor that later storage systems progressively hide.

The user performs functions that later become divided among hardware and software:

- writes state;
- selects positions;
- reads state;
- verifies plausibility;
- decides when a result is final;
- preserves a configuration when it must be reused;
- resets the device;
- maintains the mapping between physical columns and numerical meaning.

Later memory systems automate much of this work, but the functions do not disappear. They migrate into decoders, refresh logic, controllers, firmware, error correction, metadata, and protocols.

This suggests a cross-period research question:

> When storage becomes "automatic," which former operator actions become hidden machine labor?

---

## Failure / forgetting modes

The single word `forgetting` hides several distinct failures even in this simple case:

1. **physical disturbance** — beads are moved accidentally;
2. **intentional reset** — the configuration is cleared;
3. **procedural error** — the operator performs an incorrect transformation;
4. **interpretive loss** — the configuration remains physically intact but its place-value convention is no longer known;
5. **context loss** — the number remains readable but its role in the larger calculation is forgotten;
6. **device destruction** — the physical arrangement can no longer be preserved.

The fourth and fifth cases are especially important. A state can survive physically while becoming useless because the interpretive system that makes it actionable has vanished.

---

## Engineering / operational reconstruction

### Why `register-like` is defensible in a narrow sense

A modern register normally has several properties:

- it holds a value in an operational system;
- the value persists long enough to be used by subsequent operations;
- it can be read and rewritten;
- its position or identity determines how it participates in computation.

An abacus configuration shares only some of these properties:

- **yes:** it holds an operational numerical value;
- **yes:** it can preserve an intermediate or final value between manual operations;
- **yes:** it is readable and rewritable;
- **partly:** spatial position determines numerical significance;
- **no:** it is not electronically addressed;
- **no:** it is not automatically read by a processor;
- **no:** historical users did not describe it with the modern architecture concept `register`.

Therefore the safe formulation is:

> **An abacus can provide register-like retained working state, but it is not historically a CPU register and should not be placed in a direct evolutionary lineage without separate evidence.**

### Why this matters

The analogy is valuable because it isolates a minimal function that later memories elaborate:

> keep an actionable result available after the operation that produced it has ended.

This function does not require electronics, microscopic media, or autonomous machine control.

---

## Philosophical / media-theoretical interpretation

### Retention before autonomous machine memory

This case complicates any philosophy that treats technical retention as if it begins with writing, recording media, or digital storage.

The abacus is neither a durable archival inscription nor a purely transient mental state. It externalizes a working configuration into a manipulable technical support.

The strongest philosophical question is therefore not "is the abacus memory?" but:

> **What changes when a calculational state can be placed outside the body, remain materially available, and be resumed later?**

This question can later be compared with Stiegler's tertiary retention, but the case should not be forced into that vocabulary prematurely.

### Availability without archive

The abacus also separates **availability** from **archival durability**.

A number can be immediately available for the next operation while leaving no durable record once the beads are moved. Retention therefore has timescales and purposes:

- working retention;
- session retention;
- durable record;
- archival preservation.

They should not be collapsed into one concept.

### The current state is not its history

The abacus preserves one configuration but normally not the sequence of transformations that produced it.

This anticipates a distinction that will recur throughout the repository:

> **state retention is not history retention.**

A CPU register, a DRAM cell, a disk block, a database row, and a consensus state can each preserve a current value while requiring separate mechanisms — logs, journals, snapshots, traces, versioning — to preserve how that value came to be.

---

## Counterexamples and limits

### Limit 1 — a stable object is not automatically storage

A chair also retains a position, but that does not make every chair a storage device. The relevant difference is that the bead position belongs to an explicit representational and operational convention.

### Limit 2 — external representation is broader than computer memory

If every externalized working mark counts as `memory`, the category may become too broad to be useful. Pencil arithmetic, chess pieces, slide rules, marked gauges, and mechanical indicators then become neighboring cases.

Rather than excluding them by definition, the project should use comparison axes:

- Is the retained configuration part of the transformation procedure?
- Can it be resumed after interruption?
- Is it directly actionable?
- Is it machine-readable or only human-readable?
- Does the medium constrain legal states?

### Limit 3 — no direct genealogy has been established

The functional resemblance between bead positions and modern registers does not establish technological descent.

### Limit 4 — the Chinese case is not the whole history of the abacus

Greek, Roman, medieval European, Russian, Japanese, and other counting devices have different geometries and histories. This first pass uses the Chinese suanpan because period procedural sources are readily available, not because it uniquely defines the category.

---

## What this case establishes for the project

This first case supports five provisional conclusions:

1. **Retention can be operational rather than archival.** A state need only survive long enough to become input to a later operation.
2. **Retention is relational.** Bead position has meaning only within a frame, positional convention, and procedure.
3. **State and history differ.** The current configuration may persist while the sequence that produced it disappears.
4. **Maintenance can be human.** Before refresh controllers and firmware, the operator can supply selection, interpretation, protection, and reset.
5. **`register-like` can be a disciplined functional analogy** if historical vocabulary and genealogy are kept separate.

The most important result is methodological:

> We can compare ancient and modern retained states without pretending that ancient actors were secretly doing computer architecture.

---

## Related repositories

### `computing-archaeology`

Use for the larger engineering history of mechanical computation and later memory mechanisms:

- <https://github.com/tmzncty/computing-archaeology>
- mechanical track: <https://github.com/tmzncty/computing-archaeology/tree/main/docs/mechanical>
- memory track: <https://github.com/tmzncty/computing-archaeology/tree/main/docs/memory>

### `problem-history`

Use its anti-anachronism discipline when distinguishing historical actors' concepts from later reconstruction:

- <https://github.com/tmzncty/problem-history>

### `mechanical-computing-playground`

A future physical or software abacus experiment may belong there rather than here:

- <https://github.com/tmzncty/mechanical-computing-playground>

---

## Sources

### Primary / near-primary

1. Cheng Dawei (程大位), *新編直指筭法統宗* (*Suanfa Tongzong*), 1592. CText OCR transcription, vol. 1: <https://ctext.org/wiki.pl?chapter=946408&if=en>
2. Cheng Dawei, *新編直指筭法統宗*, 1592 edition, public-domain facsimile, vol. 1: <https://commons.wikimedia.org/wiki/File:NLC892-411999021914-37275_%E6%96%B0%E7%B7%A8%E7%9B%B4%E6%8C%87%E7%AE%97%E6%B3%95%E7%B5%B1%E5%AE%97_%E7%AC%AC1%E5%86%8A.pdf>

### Museum / institutional

3. Smithsonian Institution / National Museum of American History, "The Abacus and the Numeral Frame": <https://www.si.edu/spotlight/the-abacus-the-numeral-frame-and-counters/introduction>
4. National Museum of American History, "The Chinese Abacus": <https://americanhistory.si.edu/collections/object-groups/the-abacus-the-numeral-frame-and-counters/the-chinese-abacus>
5. British Museum, Chinese abacus object record and contextual note: <https://www.britishmuseum.org/collection/object/A_1909-0611-1>
6. Whipple Museum of the History of Science, "A Brief History of Calculating Devices": <https://www.whipplemuseum.cam.ac.uk/explore-whipple-collections/calculating-devices/brief-history-calculating-devices>

### Secondary

7. Frank J. Swetz, "Reflections on Chinese Numeration Systems: Transition to the Abacus," Mathematical Association of America, *Convergence*: <https://old.maa.org/press/periodicals/convergence/reflections-on-chinese-numeration-systems-transition-to-the-abacus>
8. Keith F. Sugden, "A History of the Abacus," *Accounting Historians Journal* 8.2 (1981): 1–22. DOI landing page: <https://publications.aaahq.org/ahj/article/8/2/1/5408/A-HISTORY-OF-THE-ABACUS>
9. Smithsonian bibliography for further deepening, including J. M. Pullan and Joseph Needham: <https://americanhistory.si.edu/collections/object-groups/the-abacus-the-numeral-frame-and-counters/resources>

---

## Next evidence work

Before upgrading this case from `first-pass` to `mature`:

- inspect the 1592 facsimile directly and record exact folio/page locations for `定位`, `筭盤`, and the instruction to leave a computed result unmoved;
- compare multiple editions of *Suanfa Tongzong* where possible;
- recover the older counting-rod vocabulary instead of assuming a seamless board → bead transition;
- check Needham, Pullan, Martzloff, and specialist Chinese mathematics scholarship against newer work;
- add at least one non-Chinese comparison case, probably a European counting board or Roman abacus;
- decide whether `working retention` should become a controlled vocabulary term.
