# Case 70 deepening — Olsen/Best 1959–1964 core-drive margin prior art

**Case:** 70 — coincident-current magnetic-core half-select disturbance  
**Status:** grounded deepening; no maturity promotion  
**Slice:** drive-source architecture as a retention-margin control, not a general history of magnetic-core memory  
**Principal primary source:** Kenneth H. Olsen and Richard L. Best, *Magnetic core memory*, US3161861A, filed 1959-11-12, published/granted 1964-12-15, assigned to Digital Equipment Corporation  
**Companion-history boundary:** broad magnetic-core history remains in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md)

---

## 1. Why this slice belongs in Case 70

Case 70 already establishes that coincident-current core memory cannot be reduced to the slogan “one half-current does nothing, two half-currents switch.”

The retained magnetic state is protected only if the physical system preserves a usable operating window:

```text
one-coordinate / half-select excitation
    must remain below unintended switching

coincident X + Y excitation
    must be sufficient for intended switching
```

Existing Case-70 evidence already covers:

- early material-level disturbance and signal-ratio experiments;
- shared sense-path disturbance;
- later named-machine operating-margin checks;
- temperature, strobe, current, inhibit, and service-calibration concerns.

The Olsen/Best patent adds a different layer.

It treats the **drive circuit itself** as a way to make the current delivered to each selected coordinate conductor more reproducible. The important retention question is therefore not simply:

> what current did a technician intend to set?

but also:

> what source/impedance architecture makes the delivered pulse less sensitive to unwanted circuit variation?

That is a bounded prior-art deepening of the half-select margin problem.

It is **not** evidence for a new payload-bearing mechanism.

---

## 2. Source ladder and provenance

### 2.1 Primary source

Kenneth H. Olsen and Richard L. Best, **“Magnetic core memory,” US3161861A**.

Google Patents record:

- title: *Magnetic core memory*;
- inventors: Kenneth H. Olsen and Richard L. Best;
- original/current assignee shown: Digital Equipment Corporation;
- filing / priority date: **1959-11-12**;
- publication and grant date: **1964-12-15**;
- application: US852274A.

Source:

- <https://patents.google.com/patent/US3161861A/en>

The patent is the source for the historical claims below about:

- the coincident-current arrangement assumed by the inventors;
- the one-half switching-current relation for row and column drives;
- the claimed reliability problem posed by current variation;
- the use of a substantially constant-voltage / regulated source;
- low-impedance switching;
- series resistors / impedance elements that dominate smaller switch and conductor impedances;
- pulse rise-time control and peak-current control.

### 2.2 Repository-local context

The canonical Case 70 record remains:

- [`../cases/70-magnetic-core-half-select-disturbance.md`](../cases/70-magnetic-core-half-select-disturbance.md)

The broader historical and manufacturing context remains:

- [`tmzncty/computing-archaeology/docs/memory/why-core-memory-was-worth-weaving.md`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md)

This file deliberately does **not** recreate that history.

---

## 3. Chronology boundary: filing is not publication

The patent was filed on **1959-11-12** but published/granted on **1964-12-15**.

Those dates must not be collapsed.

For this repository:

```text
1959-11-12
    = filing / design chronology witness

1964-12-15
    = public patent publication / grant witness
```

Therefore this file may say:

> Olsen and Best filed this drive-circuit design in 1959.

It should not say:

> the public could read US3161861A in 1959.

Likewise, filing date alone does not prove first conception, first prototype, first product shipment, or first commercial use.

---

# Part I — Historical record

## 4. The patent assumes a conventional coincident-current selection problem

The patent describes magnetic cores arranged in rows and columns, with X and Y conductors magnetically coupled to the cores.

Its claims describe an energizing arrangement in which a selected row conductor and a selected column conductor each receive approximately **one half of the current required to reverse the magnetization** of the selected core.

At their intersection, the selected core receives the combined excitation required for reversal.

In bounded schematic form:

```text
selected X conductor
    -> ~1/2 switching current

selected Y conductor
    -> ~1/2 switching current

selected X ∩ selected Y
    -> coincident excitation sufficient for reversal
```

That architecture implies the same retention constraint already central to Case 70:

```text
single-coordinate excitation
    must not cause an unintended stable-state reversal
```

The patent is useful here because it places the current-control circuit directly inside that selection contract.

---

## 5. The historical reliability problem is current control, not merely logical addressing

Olsen and Best describe their invention as an improved magnetic-core memory intended to improve reliability in reading and writing.

Their argument is not that row/column addressing is logically misunderstood.

Rather, the physical current delivered through the conductors must be controlled closely enough that the magnetic operation remains reproducible.

The patent discusses disadvantages of then-existing current-control arrangements and presents its own circuitry as a way to obtain improved control of magnetization.

The historically important point for Case 70 is:

> the X/Y coincidence relation does not by itself guarantee a safe or reliable magnetic operation; the delivered electrical pulse has to stay inside the usable switching margin.

This is a historical engineering concern, not a modern philosophical gloss.

---

## 6. The proposed source architecture

The patent's principal drive idea uses:

- a regulated / substantially constant-voltage source;
- low-impedance switching means;
- a separate series resistor or impedance element associated with a selected conductor;
- source and switch impedances made small compared with the series resistance.

The patent states that the voltage and resistance relation controls peak current, and that the series resistance can also be selected with the conductor inductance to obtain the desired current-pulse rise time.

In simplified form:

```text
regulated voltage source
        |
low-impedance switching
        |
series impedance / resistor
        |
selected X or Y conductor
        |
magnetic-core load
```

The claimed design intent is that the **deliberately chosen series impedance** dominates smaller unwanted resistance changes in switches and conductors.

That makes delivered current less sensitive to those smaller parasitic variations.

---

## 7. Peak-current stability and pulse-shape control are related but not identical

The patent treats two aspects of the drive pulse:

1. **peak current**, set primarily by regulated source voltage and resistance;
2. **rise time**, influenced by the series element together with line inductance.

These should not be collapsed into one scalar “current setting.”

A memory can in principle have the intended nominal peak while still having an undesirable transient waveform, or an acceptable rise time while the peak is wrong.

Thus the period source supports a richer historical object:

```text
magnetic switching excitation
    = amplitude relation
    + temporal waveform relation
```

The exact safe window is device- and system-specific; this patent does not provide a universal core-memory margin number.

---

## 8. The patent makes circuit impedance part of the memory contract

The patent repeatedly emphasizes that switch and conductor resistances are intended to be small relative to the deliberately inserted series resistance.

That relation matters because it reduces the fraction of the total current-setting impedance represented by less-controlled circuit elements.

Historically, this means the memory's retention/switching behavior cannot be assigned only to ferrite material.

The effective operating point is produced by a coupled system:

```text
core hysteresis characteristics
+
coordinate geometry
+
source voltage regulation
+
series impedance
+
switch impedance
+
line inductance / waveform
```

The patent addresses only part of that coupled system, but it plainly treats drive-circuit architecture as relevant to reliable magnetic-state manipulation.

---

# Part II — Engineering reconstruction

## 9. A useful switching-window model

The following notation is a modern engineering reconstruction, not Olsen/Best terminology.

Let:

- `I_half` = excitation delivered by one selected coordinate line;
- `I_full` = effective coincident excitation at the selected intersection;
- `I_unintended-switch` = condition at which a half-selected core may cross into an unintended stable state;
- `I_required-switch` = condition needed for reliable intended reversal of the selected core.

A simplified safe relation is:

```text
I_half < unintended-switch boundary

and

I_full > required-switch boundary
```

For an idealized symmetric X/Y scheme:

```text
I_full ~= I_X + I_Y
```

The real machine also has variation in cores, wiring, temperature, pulse timing, transistor behavior, supply regulation, and sensing.

Therefore the practical requirement is not merely one equality at a nominal operating point.

It is a **window with margin**.

---

## 10. Why delivered-current variation matters to retention

Suppose nominal half-select current is correctly chosen but varies with conductor resistance or switch impedance.

An upward excursion can reduce the distance between a half-selected core and its switching boundary.

A downward excursion can reduce the selected intersection's switching margin.

So the same variation can threaten two different sides of the contract:

```text
half-select too strong
    -> unintended-neighbor transition risk / disturbance-margin loss

selected coincidence too weak
    -> intended transition may fail
```

The patent's source/impedance design can therefore be read as an attempt to stabilize the electrical precondition from which magnetic-state reliability follows.

This is an engineering reconstruction of the patent's reliability argument.

It is not proof of a measured field-failure rate.

---

## 11. Series resistance can reduce sensitivity without removing variation

The patent's design intuition can be reconstructed with a simple relation.

For a selected path:

```text
I ~= V / (R_series + R_switch + R_line + other effective impedance)
```

If:

```text
R_series >> R_switch + R_line
```

then a fixed absolute change in `R_switch` or `R_line` becomes a smaller fraction of total path resistance.

This can reduce current sensitivity to those terms.

But it does **not** imply:

```text
all current variation = 0
```

Nor does it remove:

- supply-regulation error;
- resistor tolerance and temperature coefficient;
- line inductance and distributed effects;
- core-to-core magnetic variation;
- temperature dependence of the cores;
- timing skew;
- sense-path variation.

The design moves some burden; it does not abolish the margin problem.

---

## 12. Architectural control and service calibration are different control surfaces

Case 70's later DEC service evidence shows technicians or factory procedures checking / adjusting quantities such as current, strobe, slice, field select, and temperature tracking in actual production memory systems.

The Olsen/Best patent represents a different control surface:

```text
circuit architecture
    -> makes one class of delivered-current variation less influential

service / factory calibration
    -> chooses or verifies an operating point in an assembled system
```

These can coexist.

A design can be less sensitive to one parasitic term and still need calibration for other terms.

Therefore:

```text
architectural stabilization
    !=
calibration elimination
```

and:

```text
lower sensitivity to one variation source
    !=
self-calibrating memory
```

---

## 13. Retention here includes preventing an unwanted transition during someone else's access

Magnetic core is nonvolatile in the ordinary sense that remanent state can persist without continuous power.

But Case 70 concerns a different interval:

```text
state is already stored
+
other locations are being accessed
+
this core is physically half selected
```

During that interval, successful retention means the non-target core does **not** cross the wrong switching boundary.

The drive circuit therefore participates in retention even though it does not hold the payload while power is off.

This is a useful technical distinction:

```text
payload substrate persistence
    !=
operational non-disturbance margin
```

Both can be necessary for the same logical bit to remain recoverable over its intended lifetime.

---

## 14. Coverage state is not the issue in this slice

Many other technical-retention cases involve remembering which location must next be refreshed, scrubbed, trimmed, or repaired.

The Olsen/Best drive circuit is different.

There is no evidence here of a retained per-core maintenance queue or next-address counter.

The relevant retained relation is instead an **operating constraint embodied by circuit parameters**:

```text
source regulation
+
resistor values
+
impedance hierarchy
+
line behavior
    -> delivered excitation stays in intended region
```

Calling those components a “maintenance log” would be misleading.

---

# Part III — Controlled functional comparison

## 15. Comparison with Papian 1952

Papian's 1952 work, already grounded in Case 70, asks how core material and pulse conditions tolerate repeated nonselecting disturbance and how useful signal remains distinguishable.

Olsen/Best address a different layer:

```text
Papian-style question
    -> given nonselecting excitation, how does the core / signal behave?

Olsen/Best-style question
    -> how can the driver make the intended excitation more reproducible?
```

These are complementary.

They are not the same experiment, and this file does not claim direct procedural genealogy from Papian to Olsen/Best.

---

## 16. Comparison with later DEC MM8-E service evidence

The later PDP-8/E MM8-E material already in Case 70 exposes a concrete service regime with X/Y-current choices, strobe positioning, temperature tracking, and diagnostic memory patterns.

At a high level:

```text
1959 Olsen/Best filing
    -> drive-circuit architecture constrains pulse variability

1973 MM8-E service documentation
    -> installed system exposes operating-margin checks / adjustments
```

Both are about keeping a magnetic memory inside a usable switching/readout region.

But the present evidence does **not** establish:

```text
US3161861A
    -> direct implementation in MM8-E
```

Same company lineage is not enough.

A product-specific schematic, engineering change record, bill of materials, design memo, or equivalent source would be required for a direct adoption claim.

---

## 17. Comparison with DRAM refresh and Flash disturbance cases

A controlled analogy is possible at one abstract level only.

Across several memory technologies:

```text
operation on target state
    can impose a physical burden on non-target state
```

But magnetic-core half-select, DRAM row disturbance, and NAND read/program disturbance have different substrates, mechanisms, timescales, addressing structures, and mitigation techniques.

Therefore this file permits only the functional analogy:

```text
non-target operation burden
    -> retention margin must remain adequate
```

It does **not** assert mechanism identity or genealogy.

---

# Part IV — Philosophical interpretation

## 18. Retention can depend on disciplined non-action

The philosophical interpretation here is deliberately modest.

A memory system often appears to preserve a state by “doing nothing” to it.

Coincident-current core memory shows that operationally this is false in a useful sense:

- the non-target core may still be magnetically excited;
- the engineering task is to keep that excitation on the safe side of a transition boundary.

Thus retention can require preserving not just a state but a **distance from an unwanted transition**.

A modern interpretive phrase for this is:

> **negative-action margin** — the budget within which neighboring operations may affect a state without authorizing a state transition.

This phrase is repository interpretation, not historical terminology.

---

## 19. “The bit is nonvolatile” is not a complete reliability statement

For magnetic core:

```text
remanence at rest
    !=
robustness under half-select traffic
    !=
correct intended switching
    !=
adequate sense discrimination
```

The Olsen/Best patent strengthens only the middle operational layer by showing that drive architecture was treated as part of reliable read/write control.

It does not weaken the historical fact that magnetic core is nonvolatile in the ordinary power-off sense.

The lesson is narrower:

> substrate persistence does not eliminate the need to control operations that can push the substrate across a state boundary.

---

# Part V — Explicit non-claims

## 20. What this evidence does not establish

1. **Filing in 1959 does not mean publication in 1959.** US3161861A was published/granted in 1964.
2. **The patent is not proof of first invention** of every constant-voltage or resistor-dominated magnetic-memory driver concept.
3. **The patent is not proof of first commercial use.**
4. **The patent is not proof that a particular DEC product shipped this exact circuit.**
5. **The patent is not proof that the PDP-8/E MM8-E used this exact patented topology.**
6. **Inventor/company continuity is not product genealogy.**
7. **A substantially constant-voltage source does not mean mathematically invariant voltage.**
8. **Series resistance does not eliminate all current variation.**
9. **Dominating switch resistance does not eliminate resistor tolerance.**
10. **Dominating conductor resistance does not eliminate line inductance.**
11. **Peak-current control does not by itself guarantee ideal pulse shape.**
12. **Rise-time control does not by itself guarantee correct peak current.**
13. **Correct nominal half-current does not prove every core in an array has adequate worst-case margin.**
14. **Half-select non-switching does not imply zero magnetic excursion.**
15. **Half-select non-switching does not imply zero sense-line disturbance.**
16. **Reliable write current does not prove reliable read discrimination.**
17. **Reliable excitation does not prove successful destructive-read rewrite.**
18. **Drive-circuit reliability does not prove power-off retention lifetime.**
19. **Nonvolatile remanence does not prove immunity to powered operational disturbance.**
20. **The patent does not provide a universal magnetic-core switching-current threshold.**
21. **The patent does not provide a universal safe half-select pulse count.**
22. **The patent does not provide a universal operating-temperature envelope.**
23. **The patent does not prove that service calibration became unnecessary.**
24. **The patent does not prove that fabrication variation became irrelevant.**
25. **This evidence does not establish a Papian-to-Olsen/Best invention genealogy.**
26. **This evidence does not establish an Olsen/Best-to-MM8-E product genealogy.**
27. **Functional similarity to DRAM or NAND disturbance is not mechanism identity.**
28. **A patent claim is not the same as a controlled production reliability study.**
29. **A circuit architecture that narrows one error source is not a full-system retention proof.**
30. **The repository phrase “negative-action margin” is interpretation, not period vocabulary.**

---

# Part VI — What this slice closes and what remains open

## 21. Closed / strengthened in this slice

This evidence closes one part of Case 70's earlier device/circuit-level prior-art gap:

- by 1959, a DEC-assigned filing explicitly treated drive-current reproducibility as a magnetic-core read/write reliability problem;
- the filing tied a substantially constant-voltage source, low-impedance switching, and larger series resistances to control of peak current and pulse rise behavior;
- the source therefore supplies a primary-source bridge between abstract half-select switching margin and concrete driver-circuit architecture.

It also strengthens the distinction:

```text
logical address selection
    !=
physical excitation correctness
```

and:

```text
nominal current setting
    !=
delivered pulse reproducibility
```

---

## 22. Remaining evidence debt

Still open:

1. **Named-product adoption.** Find schematics or engineering records showing whether this exact topology entered a particular DEC memory product.
2. **Cross-vendor driver genealogy.** Compare contemporary IBM, RCA, Bell Labs, MIT, or other driver approaches before making broader claims about what was typical.
3. **Earlier priority / prior-art search.** The patent itself is one historical witness, not a complete invention-history search.
4. **Quantified margin data.** Find primary records connecting source/impedance variation to measured half-select / selected-current margins on the same plane.
5. **Lab notebooks / engineering memos.** Prefer contemporaneous design records if accessible.
6. **Temperature coupling.** Find direct evidence for how this particular source topology interacted with core-temperature compensation.
7. **Failure reproduction.** A circuit simulation or hardware experiment could test sensitivity reduction, but would be Experiment (E), not historical evidence.
8. **Patent-family context.** Check citations and related filings only if they materially clarify the specific driver lineage.

---

## 23. Repository relation

This file should be read in the following order:

```text
Case 02
    broad magnetic-core retained state / destructive read

Case 70 canonical
    half-select disturbance / sense disturbance / inhibit / operating margin

this evidence
    drive-source architecture as one margin-control layer
```

For the wider technical history of core memory, including weaving, manufacturing, coincidence-current architecture, destructive read, and historical system context, use the companion repository instead of expanding this file:

- <https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md>

---

## 24. Compact finding

```text
remanent magnetic state
    survives only if operational excitation remains legal

legal excitation window
    depends partly on delivered pulse amplitude / waveform

Olsen/Best 1959 filing
    moves part of that control burden into
    regulated voltage + low-impedance switching + dominant series impedance

therefore
    nonvolatile substrate
    !=
    self-sufficient retention contract
```

That is the bounded contribution of this slice.