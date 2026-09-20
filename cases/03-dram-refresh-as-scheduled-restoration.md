# DRAM Refresh as Scheduled Restoration

## Scope

- **Object / system:** Robert H. Dennard's one-transistor / one-capacitor field-effect-transistor memory, with the Intel 1103 used only as a bounded commercial comparison, the Intel 2164A/8203 used as a bounded external refresh-control comparison, and later TI/NEC evidence used only to separate on-chip refresh-address state from autonomous self-refresh cadence.
- **Date range:** 1967–1975 for the central grounding, with a bounded 1982–1984 deepening for hidden refresh and external refresh-control state, plus a bounded 1984-filed/1986–1988 deepening for CAS-before-RAS on-chip coverage state versus self-refresh timing control.
- **Why this case matters for technical retention:** it separates two obligations that magnetic core had partially joined: **restoration caused by access** and **restoration caused merely by the passage of time**.

This case does **not** attempt a general history of DRAM, SDRAM, DDR, sense amplifiers, row-buffer organization, or modern refresh policy. Those belong primarily in `computing-archaeology` when that repository fills its identified semiconductor-memory gap.

The question here is narrower:

> What kind of persistence is it when the retained state is expected to decay even if nobody reads it, and the system must schedule work simply to keep the present state present?

### Evidence navigation

- grounding record: [`../evidence/03-dram-1967-1982-grounding.md`](../evidence/03-dram-1967-1982-grounding.md);
- bounded controller-state deepening: [`../evidence/03-intel-1982-1984-hidden-refresh-controller-state-deepening.md`](../evidence/03-intel-1982-1984-hidden-refresh-controller-state-deepening.md) — Intel 2164A hidden refresh plus 8203 timer/counter/arbitration separate payload retention from refresh-control state and fix `hidden refresh != autonomous refresh`;
- bounded on-chip coverage-state deepening: [`../evidence/03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md`](../evidence/03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md) — TI CAS-before-RAS documentation moves refresh-address generation / coverage state on-chip while NEC's 1984-filed record keeps a distinct timer-backed self-refresh mode, fixing `on-chip coverage != autonomous cadence`.
- bounded earlier-controller / control-failure deepening: [`../evidence/03-intel-1975-1983-refresh-control-failure-boundary-deepening.md`](../evidence/03-intel-1975-1983-refresh-control-failure-boundary-deepening.md) — Intel's 1975 8222 establishes a dedicated external refresh-controller witness; AP-97A's 8202A timer/counter/arbiter and TEST-mode counter reset show that maintenance-control state can fail before payload failure, while a separate `Refresh Lock-Out` example shows that excessive or badly coupled maintenance can break useful-service liveness.

---

## Historical vocabulary

The 1968 patent is titled **"Field-effect transistor memory"**, not "DRAM". It speaks of:

- `random access memory`;
- `memory cell`;
- `storage node`;
- `read-write cycle`;
- `destructive memory`;
- information being `retained in storage`;
- periodic `regeneration`.

Modern terminology such as **1T1C DRAM**, **refresh**, and **dynamic memory** is useful for classification, but it should not replace the patent's own vocabulary when describing what Dennard actually claimed.

A later Intel data catalog explicitly calls the 1103 a **1024-bit dynamic memory** and specifies a **refresh period**. Intel's 1982 2164A documentation uses `RAS-only refresh` and `Hidden Refresh`; the 1984 8203 controller documentation separately names a `refresh timer`, `refresh counter`, and refresh/access arbitration.

The earlier-controller deepening adds period Intel terms that should also be preserved: the 1975 `8222` is explicitly a **`DYNAMIC MEMORY REFRESH CONTROLLER`** with an `Adjustable Refresh Request Oscillator`; AP-97A describes the 8202A's `refresh counter`, `TEST mode`, arbitration, and `Refresh Lock-Out`. These are not interchangeable labels for one generic `refresh mechanism`.

Later period sources add still more specific control vocabulary. TI documentation uses `CAS-before-RAS refresh` and `on-chip refresh counter`; NEC's 1984-filed / 1986-published patent explicitly distinguishes a `CAS-before-RAS refresh mode` from a `self-refresh mode`. These labels should be preserved rather than normalized into one timeless category such as `automatic refresh`.

---

## Historical record

### H/P — Dennard's patent makes leakage constitutive, not exceptional

Robert H. Dennard filed U.S. Patent 3,387,286 on 14 July 1967; it was granted on 4 June 1968.

The abstract describes an embodiment in which each cell uses **one field-effect transistor and one capacitor**. Information is represented by whether the capacitor is charged. The same transistor connects the storage capacitor to the bit line for writing and reading.

Most importantly for this project, the patent states in its opening disclosure that the capacitor charge leaks away and therefore the stored information must be **periodically regenerated**.

The summary sharpens the point: capacitor storage is said not to be `remanent` in the same sense as a latch or magnetic core because charge tends to leak away with time. Dennard nevertheless argues that the charge remains usable for long enough relative to the read-write cycle that regeneration can consume only a fraction of the memory's operating time.

**Primary anchor:** U.S. Patent 3,387,286, printed pp. 1–2, especially the abstract and `Summary of the invention`; PDF pages 4/9 in the scanned file.

### H/P — In the 1T1C embodiment, reading creates a second restoration obligation

The patent's detailed description of the FIG. 1 array states that its one-transistor / one-capacitor storage is a **destructive memory**: reading discharges the capacitor, so information that must continue to exist has to be rewritten.

The same passage then separately states that capacitor charge storage is not permanent and therefore requires periodic regeneration. Suggested regeneration methods include dedicating recurring memory cycles to regeneration or sequentially reading and rewriting word positions.

This distinction matters. The patent itself gives us two different reasons to rewrite a logical value:

1. **access-triggered restore** — a read has destroyed the physical state;
2. **time-triggered regeneration** — leakage will eventually destroy the physical distinction even if no useful read occurs.

The required regeneration frequency depends substantially on capacitor size and leakage paths. Dennard also notes that leakage is temperature-sensitive.

**Primary anchor:** U.S. Patent 3,387,286, printed pp. 5–6, description of the FIG. 1 array and regeneration; PDF page 6/9 in the scanned file.

### H/P — Dynamic retention does not logically require destructive read

The same patent also discloses other cells in which charge is stored in the gate-to-substrate capacitance of a second field-effect transistor and readout can be nondestructive.

A useful commercial boundary appears in Intel's later 1103 documentation. Intel's 1975 data catalog describes the 1103 as a **1024 word by 1-bit dynamic memory**, says that stored information is **non-destructively read**, and nevertheless requires all 1024 bits to be refreshed every **two milliseconds**, accomplished in 32 read cycles.

Therefore:

> destructive read is one possible source of restoration work, but it is not what makes a memory `dynamic` in the relevant retention sense.

The deeper feature is that the information-bearing electrical state is not assumed to remain indefinitely without periodic system action.

The Computer History Museum's semiconductor-memory history identifies the Intel 1103 as using a three-transistor dynamic cell derived from work by Honeywell's William Regitz; it should therefore not be silently treated as an implementation of Dennard's one-transistor cell.

### H/P — Intel 8222 places refresh control in a dedicated component by 1975

Intel's September 1975 *8080 Microcomputer Systems User's Manual* documents the `8222 — DYNAMIC MEMORY REFRESH CONTROLLER`. Its feature list names an adjustable refresh-request oscillator and internal address multiplexer; the prose describes an accurate refresh timer plus the control and I/O circuitry needed to satisfy dynamic-RAM refresh requirements.

This moves one part of the Case 03 control boundary earlier than the existing 8203 witness:

```text
DRAM payload array
    != dedicated external refresh-control component
```

The source is not used to claim that the 8222 was the first such controller, that it contained the same refresh-counter structure as the 8202A, or that a direct 8222→8202A design genealogy has been established.

**Deepening record:** [`../evidence/03-intel-1975-1983-refresh-control-failure-boundary-deepening.md`](../evidence/03-intel-1975-1983-refresh-control-failure-boundary-deepening.md).

### H/P — Intel 8202A makes maintenance-control failure explicit before payload failure

Intel's 1983 *Memory Components Handbook* AP-97A documents an 8202A refresh timer, a seven-bit refresh-address counter, and arbitration between refresh and ordinary memory traffic. It says the counter advances after refresh cycles.

The same source documents a TEST mode that clears the refresh counter. Intel warns that TEST mode should not occur during normal operation because it interferes with refresh; the command-decoder discussion further says that the interrupted refresh sequence **may result in data loss**. Pull-ups are recommended to reduce inadvertent TEST entry when processor read/write signals are three-stated during RESET or HOLD.

The historical boundary is therefore direct rather than hypothetical:

```text
maintenance coverage state disturbed
    != payload immediately erased

but

maintenance coverage state disturbed
    -> later retention risk
```

AP-97A also supplies the opposite failure mode. Its `Refresh Lock-Out` example shows an improperly coupled transparent-refresh request circuit repeatedly causing refresh while the processor remains in wait states. Thus maintenance can be present in excess while useful service fails.

Intel separately states that the 8203 is an extension of the 8202A architecture. That supports a bounded 8202A→8203 same-vendor architectural relation, but still does not prove 8222→8202A descent.

**Deepening record:** [`../evidence/03-intel-1975-1983-refresh-control-failure-boundary-deepening.md`](../evidence/03-intel-1975-1983-refresh-control-failure-boundary-deepening.md).

### H/P — Intel 2164A `Hidden Refresh` preserves output availability while refresh remains row-addressed

Intel's April 1982 2164A datasheet specifies **128 refresh cycles within 2 ms** and documents RAS-only and hidden refresh. In the `Hidden Refresh` description, valid data can remain on DOUT while a refresh cycle is performed, but the following page states that the part is internally refreshed at **the row addressed at the time of the second RAS**.

The historical term `hidden` therefore describes a bounded interface behavior. It does not establish that the DRAM has eliminated refresh addressing, refresh scheduling, or system-level refresh control.

The same datasheet requires initialization cycles after extended periods of bias without clocks, providing a useful negative boundary:

```text
powered device
    != actively refreshed device
```

This does not imply that payload survives such a clock gap; the datasheet does not make that claim.

**Deepening record:** [`../evidence/03-intel-1982-1984-hidden-refresh-controller-state-deepening.md`](../evidence/03-intel-1982-1984-hidden-refresh-controller-state-deepening.md).

### H/P — Intel 8203 makes refresh timing and coverage state explicit in a separate controller

Intel's 8203 dynamic-RAM controller documentation identifies a refresh timer, refresh counter, address multiplexer, and refresh/access arbiter. The timer requests refresh after a clock-derived interval; the counter contains the address for the next refresh cycle and advances after each refresh; during refresh the multiplexer places that counter value on the address outputs.

This provides a named historical implementation in which the state being preserved and the state coordinating preservation are physically and functionally distinct:

```text
DRAM payload state
    != refresh-deadline / phase state
    != refresh-coverage position
    != refresh/access arbitration state
```

The controller documentation does not describe these timer/counter states as nonvolatile. They are powered operational control state, not durable checkpoints.

**Deepening record:** [`../evidence/03-intel-1982-1984-hidden-refresh-controller-state-deepening.md`](../evidence/03-intel-1982-1984-hidden-refresh-controller-state-deepening.md).

### H/P — TI CAS-before-RAS moves refresh-address generation on-chip without moving cadence authority

The inspected Texas Instruments TMS4256/TMS4257 production datasheet is marked `MAY 1983 — REVISED JANUARY 1988`. It requires refresh of the 256 refresh rows within a 4 ms period. During CAS-before-RAS refresh, the external address is ignored and the refresh address is generated internally.

TI's 1986 *MOS Memory Data Book* applications material makes the control state more explicit: it describes an **on-chip refresh counter** that removes the need for an external refresh counter, while the CAS-before-RAS sequence itself is still invoked by externally supplied CAS/RAS timing. The adjacent RAS-only discussion describes the older external timer/counter arrangement.

This is a bounded relocation of **coverage state**, not evidence that all refresh control has become autonomous.

**Deepening record:** [`../evidence/03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md`](../evidence/03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md).

### H/P — NEC explicitly separates CAS-before-RAS refresh from timer-backed self-refresh

NEC's JPS6157097A was filed on 27 August 1984 and published on 22 March 1986. Its translated description treats a CAS-before-RAS arrangement with an internal refresh/address counter as the starting point, then adds a timer and refresh-timing generator so the device can enter a distinct self-refresh mode.

This primary patent evidence establishes a period control distinction:

```text
internal refresh-address / coverage state
    != internal refresh-cadence generation
```

The patent is not used as proof that a shipping NEC product implemented the design in 1984, nor as an invention-priority claim.

**Deepening record:** [`../evidence/03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md`](../evidence/03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md).

---

## Retained state

In the bounded one-transistor / one-capacitor case, a binary value is represented by the electrical condition of the storage node and capacitor:

```text
logical distinction
    -> charged / uncharged capacitor state
    -> storage-node voltage
```

The exact voltage is not the logical object of interest. The memory system needs the physical state to remain far enough from the decision boundary that sensing and restoration can recover the intended bit.

This is already a useful distinction between:

- **physical state** — an analog electrical quantity that drifts;
- **logical state** — the binary value the system repeatedly reconstructs from it.

The 2164A/8203 deepening adds a third category that should not be folded into either of those:

- **maintenance-control state** — timer phase, next-row/coverage position, and arbitration/request state used to make refresh occur in time and over the required address set.

The 8202A failure deepening shows that this maintenance-control state can itself become wrong while the payload remains momentarily recoverable. Resetting or disturbing coverage state is therefore not the same event as erasing payload, even though it can create a later path to forgetting.

The later CAS-before-RAS deepening shows that even this maintenance-control state has no single necessary location: the next-row / coverage counter can move from a separate controller into the DRAM package while the cadence trigger remains external.

Thus:

```text
state being retained
    != state required to retain it
    != correctness of that maintenance-control state
    != fixed physical location of the maintenance-control state
```

---

## Physical substrate

The primary FIG. 1 embodiment uses:

- a field-effect transistor as the access device;
- a capacitor as the storage element;
- word and bit lines;
- word-line drivers;
- bit-line drivers and sense amplifiers.

The storage element is therefore small only because selection, sensing, rewriting, and scheduling are displaced into circuitry shared across many cells.

This is a recurring retention pattern:

> density at the retained-state site can increase by moving maintenance work into shared infrastructure.

The later controller/device comparisons make that displacement concrete at system scale: refresh timing, address progression, and access arbitration can reside in a dedicated controller, while a later device can internalize the refresh-address counter without necessarily internalizing refresh cadence.

---

## Retention mechanism

The capacitor does not retain information because it reaches a permanently stable state. It retains information because:

1. the access transistor is normally off and presents a high-impedance path;
2. leakage is slow relative to a memory cycle;
3. before leakage destroys the usable distinction, the system regenerates the information.

So the relevant persistence is neither the passive positional stability of the abacus nor the remanent stability of magnetic core.

It is better described as:

> **bounded physical survival + scheduled restoration.**

A DRAM cell can be left electrically undisturbed for a while, but not indefinitely.

The controller/device deepening further shows that scheduled restoration can require separable control variables: a cadence trigger for **when**, a counter for **which refresh address**, and arbitration for **when maintenance may occupy the shared memory interface**. Those variables need not reside in the same component.

The 8202A adds a further boundary: the existence of those variables is not enough. They must remain correctly coupled. A request can exist before admission; a counter can be reset without immediate payload erasure; repeated refresh can occur while ordinary service is starved.

---

## Addressing and access geometry

Dennard's patent describes an array selected through **word lines and bit lines**. A selected word line connects the cells of that word to bit lines and sense circuitry.

Compared with the mercury delay line, the key change is that the requested state does not have to circulate to a unique access point. Selection is spatial/electrical rather than primarily phase-of-circulation.

But random access does not abolish time. It creates a new temporal obligation underneath the stable address:

```text
logical address remains stable
while
stored charge decays
and
periodic regeneration revisits the array
```

The address looks timeless only because the maintenance schedule is hidden below it.

Intel's 2164A/8203 pair sharpens that statement: ordinary access addresses and refresh addresses share part of the same physical address path, while the controller can substitute a refresh-counter value during a maintenance cycle. Stable logical addressability therefore coexists with a second, maintenance-specific traversal of the row-address space.

The 8202A evidence gives that traversal a failure mode: its counter represents where the maintenance walk will proceed next, and TEST mode clears that state. Intel's warning that this can interrupt the sequence and lead to data loss shows that refresh-address generation is part of the retention relation, not merely address-format plumbing.

The later TI CAS-before-RAS evidence moves that maintenance traversal boundary again: during the documented CBR cycle the external address is ignored and the refresh address is generated internally. The DRAM can therefore own the next-row / coverage progression while still depending on external CAS/RAS timing to make another refresh opportunity occur.

---

## Read semantics

### Dennard FIG. 1 1T1C embodiment

Readout discharges the storage capacitor and is explicitly described as destructive. If the logical state must persist, it must be written back.

### Boundary: dynamic but nondestructively read storage

Dennard's patent includes nondestructive-read alternatives, and Intel's 1103 data-sheet description likewise combines nondestructive reads with mandatory periodic refresh.

Therefore this case must not collapse:

```text
dynamic retention
```

into:

```text
destructive read
```

They are separable mechanisms.

### Boundary: output visibility is not maintenance autonomy

Intel's 2164A can keep useful output data valid during a hidden refresh sequence. That is a read-interface property. It does not mean refresh has disappeared, that the row-selection obligation has vanished, or that the DRAM device itself owns all timing/coverage state needed to maintain the array.

The later TI evidence also warns against assuming that the same label fixes the same address locus forever: on the inspected CBR-capable TI device, hidden refresh can use internally generated refresh addressing. `Hidden` remains an interface/service description, not a synonym for `self-refresh`.

---

## Write and erasure semantics

In the FIG. 1 embodiment, writing establishes a charged or uncharged condition on the capacitor through the selected transistor.

There is no separate archival concept of `delete`. A new write replaces the currently represented bit value. Loss can also occur unintentionally if the state decays below recoverability or restoration fails.

This is **state retention**, not history retention. The cell does not preserve previous values merely because a new value is written.

---

## Time

DRAM forces several timescales into one object:

### Read-write cycle

The useful computation/access timescale.

### Charge-retention interval

The interval over which leakage has not yet destroyed the recoverable distinction.

### Regeneration / refresh interval

The system-maintenance schedule chosen to revisit state before the retention interval is exceeded.

### Refresh-controller phase and coverage

The Intel 8203 comparison adds a controller timescale inside the refresh interval: a timer determines when another refresh request becomes due, while a row counter determines which refresh address comes next. These are not the payload's retention time; they are operational state used to satisfy it.

The 8202A arbitration evidence adds another timescale between `due` and `executed`: a refresh request may wait behind ordinary memory traffic. In the documented arrangement Intel says refresh can be delayed by at most one RAM cycle. That local admission bound is part of how the controller keeps the larger refresh deadline meaningful.

The TI/NEC deepening shows that those two control variables need not migrate together. A DRAM may internalize the coverage counter while cadence remains externally invoked; a distinct self-refresh design can then add timer/timing-generation circuitry.

### Temperature-dependent leakage timescale

The patent explicitly connects leakage, and thus usable storage time, to junction temperature.

This makes DRAM a particularly clean example of a claim central to this repository:

> a logical state can appear continuously present even though its physical embodiment has a deadline.

---

## Maintenance and labor

At the cell level, the retained state seems minimal: one transistor and one capacitor in the key embodiment.

At system level, that simplicity requires surrounding work:

- selection;
- sensing;
- rewrite after destructive read where applicable;
- periodic regeneration / refresh scheduling;
- refresh-address coverage;
- arbitration between refresh and useful access;
- timing;
- temperature-aware design margins;
- power and control circuitry.

The historical move is therefore not simply from `complicated memory` to `simple memory`.

It is also a redistribution of complexity:

> **fewer devices per stored bit, more coordinated maintenance around the array.**

The 1975 8222 witness shows that some of this work could already be packaged as a dedicated external controller role. The 8202A then makes the control-state failure surface unusually explicit: timer, counter, request synchronization, and arbitration all have to cooperate. The 2164A/8203 pair makes another redistribution visible: `hidden` maintenance at one interface can still depend on explicit controller state elsewhere. The later TI/NEC comparison shows a second redistribution: the next-row counter can move inward without abolishing the external timing obligation, and a later self-refresh design can internalize still more of that control.

---

## Failure / forgetting modes

This case adds several distinct forms of technical forgetting:

- leakage until the charge difference is no longer recoverable;
- missed or late refresh;
- incomplete refresh-address coverage even if refresh cycles continue to occur;
- 8202A refresh-counter reset / sequence interruption creating later retention risk without immediate physical erasure;
- badly coupled refresh admission producing repeated refresh while useful processor service is locked out;
- failed restore after destructive read;
- sense error followed by rewriting the wrong logical value;
- temperature increase shortening the safe retention interval;
- failure of shared refresh / sense / timing infrastructure affecting many cells;
- loss or corruption of powered refresh-control state followed by incorrect maintenance sequencing.

These should not all be called merely `volatile memory loss`.

The 8202A evidence is especially useful because it demonstrates two opposite mistakes:

```text
maintenance sequence disrupted
    -> retention risk

maintenance repeatedly over-admitted
    -> service-liveness risk
```

---

## Engineering reconstruction

### E — DRAM adds a deadline to quiescent retention

Magnetic core can retain a remanent state while idle without scheduled rewriting. Dennard's capacitor state cannot be treated that way: even an untouched bit has a finite maintenance deadline.

Thus **quiescent** does not mean **maintenance-free**.

### E — Refresh is temporal multiplexing of maintenance

Dennard's examples allocate recurring memory cycles to regeneration. In functional terms, array bandwidth is periodically borrowed from ordinary work so that the current state remains available for future work.

Persistence consumes time.

### E — the refresh deadline and refresh coverage are separate obligations

The Intel controller deepening shows that `refresh every N milliseconds` is not one scalar action. The system must both trigger maintenance often enough **and** distribute those cycles over the required refresh addresses.

In the 8203 implementation:

```text
refresh timer
    -> when maintenance becomes due

refresh counter
    -> which refresh address comes next
```

Repeatedly servicing the wrong row set would not satisfy the array-wide retention requirement merely because refresh cycles were occurring.

### E — request generation, admission, execution, and coverage are distinct relations

The earlier 8202A material makes the path more explicit:

```text
physical retention obligation
    -> refresh request becomes due / is generated
    -> request is synchronized or held pending
    -> arbiter admits it against useful traffic
    -> refresh cycle executes
    -> coverage counter advances
    -> required row set is revisited before deadline
```

Therefore:

```text
refresh configured
    != refresh requested
    != refresh admitted
    != refresh executed
    != correct coverage completed
    != payload guaranteed recoverable
```

A controller can be active and still fail the retention relation at one of these boundaries.

### E — maintenance-control failure can precede visible payload failure

At the instant the 8202A TEST mode clears the refresh counter, DRAM cells may still hold recoverable charge. The first failure is therefore not necessarily a payload-bit failure. It can be a failure of the state that organizes future restoration.

Thus:

```text
present payload correctness
    != future-retention process correctness
```

The payload may become endangered before it becomes observably wrong.

### E — hidden refresh is a visibility property, not autonomous retention

The 2164A can hide a refresh cycle from the useful data output, but the row remains addressed and a controller can still own the timer, counter, request, and arbitration state.

Therefore:

```text
maintenance hidden from one interface
    != maintenance absent
    != maintenance autonomous
    != maintenance-control state durable
```

The later TI device sharpens the warning: a hidden-refresh implementation can also use internally generated refresh addresses, so the label itself does not fix the location of coverage state.

### E — coverage-state integration is independent of cadence autonomy

The paired Intel/TI/NEC evidence supports a more precise control decomposition:

```text
external-controller arrangement
    timer/cadence external
    + next-row counter external

CAS-before-RAS arrangement
    refresh opportunity externally invoked
    + next-row counter on-chip

self-refresh arrangement (bounded NEC patent witness)
    next-row counter on-chip
    + timer/timing generation on-chip
```

Therefore:

```text
on-chip coverage authority
    != autonomous cadence authority
```

This is an engineering reconstruction from the named sources, not a claim of direct product genealogy.

### E — maintenance has a service-liveness budget as well as a retention budget

The AP-97A `Refresh Lock-Out` example shows that excessive or incorrectly coupled refresh work can starve ordinary memory service. The controller therefore balances at least two obligations:

```text
retention obligation
    revisit rows before physical deadlines

service obligation
    allow ordinary reads / writes to make progress
```

Maintenance activity alone is not evidence that the system is healthy.

### E — The logical bit survives repeated analog replacement

After regeneration, the charge configuration is newly established. The system treats that restored physical state as the continuation of the same logical bit.

This strengthens a cross-case finding already exposed by delay-line regeneration and destructive-read core:

> logical identity does not require identity of one uninterrupted physical token.

---

## Philosophical / media-theoretical interpretation

### I — Persistence as scheduled return

The delay line retains by continuous recurrence; DRAM introduces a different temporal regime. The state can remain locally quiescent for an interval, but the system must **return to it before a deadline**.

This suggests a useful distinction for later comparison:

```text
continuous maintenance
    delay-line circulation

access-triggered maintenance
    classic destructive-read core

periodic deadline-driven maintenance
    DRAM refresh
```

These are engineering categories first. They should not yet be promoted into a universal philosophy of memory.

### I — Availability rests on invisible temporal discipline

To software, a memory location appears simply available at its address. Physically, the cell's state is decaying and must be restored on schedule.

The controller/device evidence sharpens the point: part of that discipline can be displaced into timer, counter, and arbitration infrastructure that is not itself the represented payload; individual control variables can also migrate across the package boundary without the retention relation becoming independent of the rest of the system.

The 8202A failure boundary adds one more precision: the present can remain intact while the machinery organizing its future maintenance has already become wrong. Persistence therefore depends not just on repeated activity but on correctly organized future return.

The philosophical value of the case is therefore not that DRAM is a metaphor for human memory. It is that it demonstrates mechanically how **stable availability can be an effect produced by hidden temporal organization whose technical boundary can move or fail without immediately changing the payload**.

That observation can later be tested against Ernst's operational / microtemporal account. It should not yet be equated with Stiegler's tertiary retention or Heidegger's `Bestand`.

---

## Functional analogy and limits

### A — Similarity to magnetic core

Both classic destructive-read core and the Dennard FIG. 1 cell may require rewrite after read.

But the mechanisms are different:

- core: remanent magnetic state can remain at rest; access may destroy it;
- capacitor cell: access may destroy it **and** time-dependent leakage creates a restoration obligation even without useful access.

### A — Similarity to delay line

Both can preserve a logical pattern through repeated recreation.

But:

- delay line requires continuous circulation as the retention mechanism;
- DRAM gives each cell an interval of local persistence before scheduled regeneration.

### A — similarity to later maintenance-control metadata is functional only

The 8202A/8203 timer/counter, later on-chip refresh counters, and repository cases involving scrub checkpoints, repair maps, or retained maintenance policy can all encode control state about maintenance. But their persistence horizons, physical locations, and authority are different. The early DRAM control state discussed here is ordinary powered operational state; later systems may checkpoint maintenance progress durably.

Therefore:

```text
maintenance-control state
    != durable maintenance checkpoint
```

No historical genealogy is implied.

### A — relation to later maintenance admission failures is functional only

The 8202A now offers an early hardware case in which a maintenance request, its admission against useful work, and the coverage state that follows are distinct. Later HDFS scanner and disk patrol cases expose structurally similar layers at software/device timescales.

The comparison is only:

```text
maintenance mechanism exists
    != maintenance correctly admitted
    != coverage completed
```

It does not assert a shared physical mechanism, terminology, or lineage.

### A — relation to Case 09 `automatic refresh` terminology is functional only

Case 09's 1972 Signetics evidence shows that `automatic refresh` could name access/address-coupled internal restoration without autonomous recurring cadence. The present slice adds a different arrangement: CAS-before-RAS can internalize coverage/address progression while refresh opportunities remain externally invoked, and the NEC patent then adds timing generation for a distinct self-refresh mode.

Thus:

```text
same broad maintenance function
    != same control split
    != same historical term
    != shared genealogy
```

### Limit — not every DRAM read is destructive

The Intel 1103 boundary case and nondestructive embodiments in Dennard's own patent show that `dynamic` cannot be defined merely by destructive readout.

### Limit — `hidden refresh` and CAS-before-RAS do not mean self-refresh

For the 2164A evidence used here, hidden refresh preserves output availability while a refresh cycle occurs but the refreshed row remains externally addressed. In the later TI CBR-capable device, hidden refresh can use internally generated refresh addressing. The same `hidden` label therefore does not even guarantee a fixed address-generation locus, and neither arrangement should be silently renamed `self-refresh`.

### Limit — not a complete modern DRAM account

Modern DRAM adds much richer sensing, row-buffer, refresh, error, packaging, power, and controller behavior. This case deliberately does not project later architecture backward into the 1967 patent or turn the 1970s–1980s examples into a complete genealogy.

---

## Cross-case result

Cases 00–03 now expose four distinct retention regimes:

```text
abacus
    retained position

mercury delay line
    continuous circulation / regeneration

magnetic core
    remanence at rest + access-triggered restore

Dennard 1T1C memory
    decaying state + periodic regeneration
    (+ destructive-read restore in the bounded embodiment)
```

The important new distinction is:

> **maintenance can be triggered by time even when no useful access occurs.**

The 1975–1983 Intel controller deepening adds:

> **maintenance-control state has its own failure surface: it can become incorrect before the payload fails, and maintenance can also be over-admitted strongly enough to break useful-service liveness.**

The 1982–1984 Intel deepening adds another:

> **the state being maintained can be different from the control state that schedules and covers the maintenance.**

The 1984-filed/1986–1988 deepening adds a further distinction:

> **maintenance-control state can migrate across a device boundary one variable at a time: internal coverage state does not imply internal cadence authority.**

This will matter later for Flash retention/read-disturb management, SSD background work, scrubbing, replica repair, lease renewal, and long-term archival migration — but those comparisons must be established case by case rather than assumed now.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Dennard filed the `Field-effect transistor memory` patent in 1967 and it issued in 1968 | H/P | exact patent metadata |
| One disclosed embodiment uses one FET and one capacitor | H/P | patent abstract + FIG. 1 description |
| Capacitor leakage requires periodic regeneration | H/P | patent abstract, summary, and detailed description |
| The FIG. 1 one-capacitor embodiment has destructive readout and requires rewrite if information is to remain | H/P | patent pp. 5–6 |
| Regeneration can be scheduled independently of ordinary accesses | H/P/E | patent's recurring-cycle and sequential regeneration examples |
| Intel 1103 documentation combines dynamic storage, nondestructive read, and a 2 ms refresh requirement | H/P | Intel 1975 Data Catalog, p. 2-7 |
| Dynamic retention is therefore not identical to destructive read | E | bounded inference from the patent + Intel commercial comparison |
| Intel's September 1975 manual documents the 8222 as a dedicated `DYNAMIC MEMORY REFRESH CONTROLLER` with refresh timer / request-oscillator and address-multiplexing functions | H/P | Intel 8080 manual, 8222 p. 5-99 |
| Intel AP-97A documents an 8202A timer, seven-bit refresh counter, and refresh/access arbitration | H/P | Intel 1983 *Memory Components Handbook*, AP-97A pp. 3-119–3-123 |
| Intel warns that 8202A TEST-mode counter reset interrupts the refresh sequence and may result in data loss | H/P | same |
| Intel documents a `Refresh Lock-Out` failure in which badly coupled external refresh requests can leave the processor waiting while refresh repeats | H/P | same |
| Intel describes the 8203 as an extension of the 8202A architecture | H/P | Intel 1983 handbook, 8203 section |
| Maintenance-control failure can precede visible payload failure | E | bounded reconstruction from 8202A counter-reset warning + retention deadline |
| Intel 2164A documentation combines a 128-cycle/2 ms refresh requirement with Hidden Refresh that keeps output data valid while refresh remains row-addressed | H/P | Intel 2164A datasheet, pp. 3-219, 3-229–3-230 |
| Intel 8203 documentation places refresh timing, next-row coverage state, and refresh/access arbitration in a dedicated controller | H/P | Intel 1984 Memory Components Handbook, 8203 §§2.2.2–2.2.6 |
| TI's inspected TMS4256/TMS4257 revision requires 256-row/4 ms refresh and generates the CBR refresh address internally while ignoring the external address | H/P | TI TMS4256/TMS4257 production datasheet, printed p. 4-5 |
| TI's 1986 applications material names an on-chip refresh counter that eliminates the external refresh counter for CBR | H/P | TI *MOS Memory Data Book* (1986), Applications Information p. 9-52 |
| NEC's 1984-filed/1986-published patent distinguishes CAS-before-RAS refresh from a timer/timing-generator-backed self-refresh mode | H/P | JPS6157097A abstract and description |
| Hidden refresh is not evidence of autonomous or durable refresh-control state | E | bounded device/controller reconstruction |
| On-chip refresh coverage is not evidence of autonomous cadence | E | bounded TI + NEC reconstruction |
| DRAM exposes periodic deadline-driven maintenance as distinct from continuous circulation and access-triggered restore | E/I | cross-case reconstruction |
| DRAM is identical to tertiary retention or `Bestand` | X | explicitly unsupported |

---

## Related repositories

### `tmzncty/computing-archaeology`

That repository currently identifies SRAM / DRAM / ROM / EEPROM / Flash / cache / ECC as a missing historical middle. A future full technical history of semiconductor memory should be developed there. This case should remain focused on the retention problem and link outward rather than pre-empting that work.

A direct search for `2164A`, `8202A`, `8203`, and the paired hidden-refresh/controller-state question did not find an existing companion-repository treatment during the earlier deepening. A fresh search for `CAS-before-RAS refresh TMS4256` likewise found no dedicated packet to reuse. This round additionally searched `8203 refresh controller` in `computing-archaeology` and found no dedicated reusable packet. This repository therefore keeps only the retention-specific seams:

```text
dedicated external refresh control
    -> request / cadence state
    -> coverage-counter state
    -> arbitration / admission
    -> control-state failure before payload failure

external coverage state
    -> on-chip coverage state
    -> separately internalized cadence/timing generation
```

Broader 8222/3222/8202/8202A/8203 controller genealogy, first-invention/first-shipment chronology, vendor-by-vendor CBR adoption, JEDEC history, self-refresh genealogy, and semiconductor-memory generation history remain better candidates for `computing-archaeology`.

Current relevant memory track:

<https://github.com/tmzncty/computing-archaeology/tree/main/docs/memory>

### `tmzncty/problem-history`

Use its anti-anachronism rule here: `DRAM`, `refresh`, and `1T1C` are useful modern organizing terms, but the 1968 patent's own wording is `Field-effect transistor memory`, `regeneration`, `destructive memory`, and `retained in storage`. Likewise, Intel's `DYNAMIC MEMORY REFRESH CONTROLLER`, `TEST mode`, `Refresh Lock-Out`, `Hidden Refresh`, TI's `CAS-before-RAS refresh`, and NEC's `self-refresh mode` should not be silently collapsed into one later vocabulary.

---

## Sources

### Primary

1. Robert H. Dennard, **"Field-effect transistor memory,"** U.S. Patent 3,387,286, filed 14 July 1967, issued 4 June 1968. Google Patents transcription: <https://patents.google.com/patent/US3387286A/en>. Public-domain scan: <https://commons.wikimedia.org/wiki/File:MOS_DRAM_patent.pdf>.
   - printed pp. 1–2: abstract, prior art, and summary;
   - FIG. 1 / FIGS. 4A–4B: one-transistor / one-capacitor array and read-write timing;
   - printed pp. 5–6: destructive read, rewrite obligation, regeneration schemes, leakage and temperature dependence.
2. Intel Corporation, **1975 Intel Data Catalog**, `1103 — Fully Decoded Random Access 1024 Bit Dynamic Memory`, p. 2-7. Bitsavers scan: <https://www.bitsavers.org/components/intel/_dataBooks/1975_Intel_Data_Catalog.pdf>.
   - states dynamic operation;
   - nondestructive read;
   - refresh of all 1024 bits in 32 read cycles;
   - required refresh period of 2 ms for 0–70 °C ambient.
3. Intel Corporation, **8080 Microcomputer Systems User's Manual**, September 1975, `8222 — DYNAMIC MEMORY REFRESH CONTROLLER`, printed p. 5-99. Canonical archival scan: <https://www.bitsavers.org/components/intel/MCS80/98-153B_Intel_8080_Microcomputer_Systems_Users_Manual_197509.pdf>. Searchable page transcription: <https://manualsdump.com/en/manuals/intel-8080model/110758/165>.
   - dedicated refresh-controller role;
   - adjustable refresh-request oscillator;
   - internal address multiplexer;
   - refresh timer and control / I/O circuitry.
4. Intel Corporation, **Memory Components Handbook** (1983), AP-97A, `Interfacing Dynamic RAMs to iAPX 86/88 Systems Using the Intel 8202A and 8203`, pp. 3-117–3-127. Canonical archive: <https://www.bitsavers.org/components/intel/_dataBooks/1983_Memory_Component_Handbook.pdf>. Searchable transcript: <https://www.studylib.net/doc/25790501/1983-memory-component-handbook>.
   - timer and seven-bit refresh counter;
   - request synchronization and arbitration;
   - TEST-mode counter clear and data-loss warning;
   - bounded refresh-delay behavior;
   - `Refresh Lock-Out` example;
   - 8203 described as an extension of 8202A architecture.
5. Intel Corporation, **SBC 104/108 boards manual**. Public manual transcript: <https://manualzz.com/doc/6680590/intel-sbc-104-108-boards-manual>.
   - bounded implementation witness for 8222 mediation of ordinary RAM requests and internally generated refresh requests.
6. Intel Corporation, **`2164A FAMILY — 65,536 x 1 BIT DYNAMIC RAM`**, order no. 210425-001, April 1982. Archived scan: <https://www.minuszerodegrees.net/memory/4164/datasheet_2164A.pdf>.
   - p. 3-219: 128 refresh cycles / 2 ms and Hidden Refresh feature;
   - p. 3-229: refresh-row geometry and start of Hidden Refresh description;
   - p. 3-230: hidden-refresh row-address boundary, DOUT behavior, and initialization after extended bias without clocks.
7. Intel Corporation, **`8203 — 64K DYNAMIC RAM CONTROLLER`**, reproduced in *Intel Memory Components Handbook* (1984). Bitsavers archive: <https://www.bitsavers.org/components/intel/_dataBooks/1984_Intel_Memory_Components_Handbook.pdf>. Alternative archive: <https://deramp.com/downloads/mfe_archive/050-Component%20Specifications/Intel/Memory%20Components/1984_Intel_Memory_Components_Handbook.pdf>.
   - p. 3-82: refresh/access arbiter; refresh timer and counter; refresh-address multiplexer; internal/external refresh description.
8. Texas Instruments, **`TMS4256, TMS4257 — 262,144-BIT DYNAMIC RANDOM-ACCESS MEMORIES`**, inspected manufacturer scan; device section marked `MAY 1983 — REVISED JANUARY 1988`: <https://www.ardent-tool.com/datasheets/TI_TMS4256_7.pdf>.
   - printed p. 4-3: revision line and feature list;
   - printed p. 4-5: 4 ms / 256-row refresh requirement; CBR external-address-ignore and internal refresh-address generation.
9. Texas Instruments, **MOS Memory Data Book** (1986), Applications Information. Canonical archive: <https://bitsavers.org/components/ti/_dataBooks/1986_SMYD006_TI_MOS_Memory_Data_Book.pdf>. Section mirror: <https://garyopa.hopto.org/WHTech/ftp.whtech.com/datasheets%20and%20manuals/Datasheets%20-%20TI/MOSMemory-1986/MOSMemory-1986-09-Applications%20Information.pdf>.
   - printed p. 9-52: external timer/counter description for RAS-only refresh; on-chip refresh counter for CAS-before-RAS.
10. Kazuo Nakaizumi / NEC Corporation, **`Dynamic semiconductor memory`**, JP59177905A / JPS6157097A, filed 27 August 1984, published 22 March 1986: <https://patents.google.com/patent/JPS6157097A/en>.
   - translated abstract/description: refresh/address counter; timer; refresh timing generator; separate CAS-before-RAS and self-refresh modes.
11. Samsung Semiconductor, **1988 MOS Memory Data Book**, KM41256A/KM41257A device-operation section. Public converted transcript: <https://manuals.plus/m/85b83593adbc036de4142423dbf452ec188a6445ad476820abc659b82e7f2ade>.
   - corroborates on-chip CBR refresh-address counter increment and counter-test behavior; not used for fine diagram interpretation.

### Institutional secondary / artifact context

12. The Henry Ford, **Manual, `INTEL 8080 Microcomputer Systems User's Manual, 1975`**, Object ID 95.22.2.3: <https://www.thehenryford.org/collections/explore/artifact/379548>.
   - records Intel Corporation as creator and September 1975 as date made.
13. Smithsonian National Museum of American History, **Manuals Relating to the Intel 8080 Microprocessor and Its Applications**, ID 1991.3201.25: <https://americanhistory.si.edu/collections/object/nmah_1401237>.
   - collection record includes Intel 8080 manual editions from July and September 1975.
14. Computer History Museum, **"1970: Semiconductors Compete with Magnetic Cores,"** *The Storage Engine*: <https://www.computerhistory.org/storageengine/semiconductors-compete-with-magnetic-cores/>.
   - useful for placing Intel 1103's three-transistor dynamic cell in the early semiconductor-memory transition;
   - not used as the primary source for Dennard's 1T1C mechanism.
15. Computer History Museum, **Intel 1103 1024-bit (1K) DRAM** object record: <https://www.computerhistory.org/revolution/memory-storage/8/368/1017>.

## Source notes

The patent is the authoritative source for what Dennard disclosed and for the distinction between destructive read and periodic regeneration. The 1975 Intel catalog is later than the 1103's 1970 introduction, so it should be treated as primary manufacturer documentation of the product family rather than as evidence for the exact first-shipment specification. The 1103 comparison is intentionally used to bound the concept of dynamic retention, not to claim that the 1103 implements Dennard's exact one-transistor cell.

The 1975 8222 and 1983 AP-97A claims in the latest deepening rest on Intel-authored period documentation. This run checked searchable text/transcripts against canonical archival-document metadata and page numbering. It did **not** obtain a reliable fresh page-image render of every cited Intel page, so the new evidence does not claim facsimile-level inspection of diagrams; no claim depends on interpreting a faint circuit line. The exact source-custody boundary is recorded in [`../evidence/03-intel-1975-1983-refresh-control-failure-boundary-deepening.md`](../evidence/03-intel-1975-1983-refresh-control-failure-boundary-deepening.md).

The 2164A scan was directly inspected at printed pp. 3-219, 3-229, and 3-230, including the Hidden Refresh timing diagram and Power On section. The 8203 handbook text is used to locate refresh timer/counter/arbitration state in a named Intel controller; it is not used to claim invention priority or universal 1980s practice.

For the later deepening, the TI TMS4256/TMS4257 scan was directly inspected at printed pp. 4-3 and 4-5. The inspected copy is explicitly a **January 1988 revision**, so no visible feature is silently back-projected into the original May-1983 revision. The 1986 TI applications prose is used only for its explicit external-counter/on-chip-counter distinction. The NEC patent is a primary filing but the accessible English text is a translation, so it is used for structural mode/control distinctions rather than delicate wording claims. The Samsung 1988 source is a converted transcript and is corroborative. See the dedicated deepening records for full non-claim and source ledgers.

---

## Status

**`grounded` — unchanged.**

The 1975–1983 deepening closes a bounded earlier-controller / control-failure seam: a dedicated Intel refresh-controller role is directly documented by 1975, and AP-97A directly grounds timer, coverage-counter, arbitration, counter-reset risk, and a separate refresh-overadmission service-liveness failure. It does **not** close first-controller priority, 8222→8202A genealogy, non-Intel controller chronology, controller clock/power fault behavior, or modern refresh-management failures. Those remain narrow future work rather than a maturity blocker for the central Case 03 claim.