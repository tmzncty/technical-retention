# Case 03 deepening — Hitachi 1993–1995 self-refresh multi-horizon control state

## Scope

This slice asks one narrow question left open by the Case 03 evidence index:

> Once DRAM self-refresh cadence has moved on-chip, what *control state* is actually required to make the autonomous interval correct, and does one physical counter necessarily correspond to one maintenance role?

Hitachi's 1993-priority self-refresh patent family gives an unusually detailed circuit-level answer. The Japanese application `JP5095260A`, published as `JPH06282985A` on 7 October 1994, and its U.S. family member `US5453959A`, granted on 26 September 1995, describe a DRAM self-refresh controller in which:

- a low-current ring oscillator produces the basic internal clock;
- one multi-purpose binary counter is reused sequentially to detect **self-refresh mode-entry time**, **completion of one whole-array burst-refresh pass**, and **maximum pause time**;
- a separate refresh-address counter advances the row-refresh address;
- an internal RAS generator turns oscillator activity into refresh operations;
- programmable/fuse-set detection thresholds compensate for product specification and process variation;
- dummy-cell leakage and supply-voltage fluctuation can terminate a nominal pause early.

The retention-specific point is not merely that the patent contains an oscillator and counters. It exposes a stronger decomposition:

```text
physical counter embodiment
    != one maintenance-control role

whole-array completion counter
    != refresh-address / coverage-position counter

nominal pause deadline
    != sole trigger for renewed maintenance

self-refresh control state
    != durable restart checkpoint
```

This is **patent-design evidence**, not proof that a particular shipping Hitachi DRAM implemented every disclosed block. Case 03 remains `grounded`; this slice does not justify a maturity promotion.

---

## Source custody and chronology

### Primary patent family

**Japanese publication**

- Hitachi Ltd. / Texas Instruments Japan Ltd., `JPH06282985A`, **Dynamic RAM**.
- Japanese filing / priority date: **30 March 1993**.
- Publication date: **7 October 1994**.
- Inventors: Toshiyuki Sakuta and Tomohiro Suzuki.
- Public transcription: <https://patents.google.com/patent/JPH06282985A/en>

Google Patents identifies the original assignees as Hitachi Ltd. and Texas Instruments Japan Ltd. and preserves the translated description with the oscillator, counter, internal-RAS, refresh-address-counter, and pause-control details used below.

**U.S. family member**

- `US5453959A`, **Semiconductor memory device having a self-refreshing control circuit**.
- U.S. filing: **30 March 1994**.
- Grant: **26 September 1995**.
- Public transcription: <https://patents.justia.com/patent/5453959>

The U.S. text is useful because it provides a detailed English description and claims. The Japanese publication is used to anchor the earlier public date and family chronology.

### Historical-status boundary

The U.S. specification says that, before the claimed simplification, the inventors had developed a three-counter control arrangement. It also characterizes the corresponding earlier figure as not publicly known.

Therefore this packet does **not** backdate public prior art from the patent's internal design history. The safe chronology is:

```text
1993-03-30
    Japanese filing / priority

1994-10-07
    Japanese public publication

1995-09-26
    U.S. grant/publication
```

The disclosure can describe earlier internal engineering activity without proving that the earlier circuit was already public.

---

# Historical record

## H1 — Hitachi defines self-refresh as internal-clocked recurrence, not merely internal row addressing

The U.S. family member describes self-refresh as operation without an externally supplied clock once the qualifying CBR state has persisted long enough. A basic on-chip oscillator supplies the timing pulses used to enter and run the self-refresh regime.

This reinforces an existing Case 03 distinction already grounded by TI/NEC and Micron evidence:

```text
internal refresh-address generation
    !=
internal refresh-cadence generation
```

But this patent goes further by showing how the cadence generator participates in several different control decisions rather than acting as one opaque `refresh timer`.

Primary anchors:

- `US5453959A`, summary and claims 1, 7, 10–12;
- `JPH06282985A`, translated paragraphs around the basic oscillator and binary counter.

---

## H2 — one oscillator feeds a multi-purpose binary counter

The disclosed embodiment uses a basic oscillator formed, for example, as a low-current CMOS ring oscillator. Its pulse train is supplied to a binary counter.

The U.S. description explicitly calls the counter **multi-purpose** and assigns it three sequential functions:

1. measure the duration required before the CBR condition is accepted as self-refresh entry;
2. measure the number of refresh operations required for a complete whole-array pass;
3. measure the later pause interval before the next burst refresh begins.

The Japanese abstract states the same design objective in condensed form: a shared counter and output-identification logic produce a mode-entry output (`ME`), refresh-count/completion output (`RC`), and pause-limit output (`PL`).

This is direct historical evidence that:

```text
one physical counter
    can embody several temporally exclusive control roles
```

It is therefore too coarse to infer one state category from one hardware block.

---

## H3 — the 19-bit counter partitions different maintenance horizons

In the detailed embodiment, the patent describes a 19-bit binary counter for a 4K-refresh-cycle example.

The lower-order region is used first to recognize the mode-entry interval. During burst refresh, lower bits count oscillator-linked refresh operations. A carry/change around the transition from `C12` to `C13` indicates that the required 4096 operations have been completed. Higher bits are then used to measure the pause interval.

The exact bit allocation belongs to the disclosed example, not to all self-refresh DRAMs. What matters historically is that one counter chain is intentionally reused across distinct horizons:

```text
entry qualification horizon
    -> whole-array refresh-run horizon
    -> inter-burst pause horizon
```

These horizons are not interchangeable merely because they share one physical counter.

Primary anchors:

- `US5453959A`, description of counter `CNTR` / bits `C1`–`C19`;
- `JPH06282985A`, translated paragraphs describing `C1`–`C19`, `C13`, and the pause-time bits.

---

## H4 — refresh-count completion and refresh-address progression are separate state

The patent does **not** use the multi-purpose 19-bit counter itself as the row-address generator.

During ordinary CBR refresh, a refresh-address counter produces the internal row address from RAS-derived activity. In self-refresh, the internal RAS generator supplies `INTRAS` pulses instead. Those pulses drive the separate refresh-address counter.

The multi-purpose counter counts the same oscillator-linked rhythm so that it can detect when one complete refresh pass has occurred, but the specification explicitly distinguishes that measurement function from the address counter itself.

That yields a particularly important retention boundary:

```text
coverage-completion evidence
    !=
coverage-position state
```

or more concretely:

```text
"4096 refresh operations have occurred"
    !=
"this counter is the row-address pointer"
```

The two states are synchronized by the refresh rhythm but have different roles and embodiments.

Primary anchor: `US5453959A`, description of `INTRAS`, the refresh-address counter, and the `C1`–`C12` completion count.

---

## H5 — mode entry is itself measured state, not a timeless command label

The disclosed controller does not treat the first CBR-like signal combination as instantaneous proof that the device is already in self-refresh.

The CBR condition releases the normally reset counter. Oscillator pulses are counted until a programmable threshold corresponding to the self-refresh mode-entry interval is reached. If the qualifying condition disappears before that threshold, the sequence does not become a completed self-refresh entry.

The historical circuit therefore separates:

```text
entry condition observed
    !=
entry dwell time satisfied
    !=
self-refresh regime established
```

This makes transition-state timing part of the maintenance-control state rather than merely an external waveform annotation.

---

## H6 — the patent exposes a whole-array completion signal before the pause interval begins

Once self-refresh is established, the internal RAS generator produces a burst of refresh operations from the oscillator rhythm. In the 4K example, completion of the burst causes a counter transition that generates the `RC` completion indication / pause-start relation.

The controller then disables the internal refresh pulses and begins timing the pause.

Thus, within the patent's own architecture:

```text
refresh activity running
    !=
whole-array pass complete
    !=
pause interval active
```

The mode remains `self-refresh` across both the active refresh burst and the pause. Mode membership is therefore coarser than the maintenance phase inside that mode.

---

## H7 — the nominal pause timer is an upper bound, not the only reason to restart refresh

The detailed embodiment does not rely solely on the programmed maximum-pause count.

It also describes:

- a dummy-cell charge/leak monitor; and
- power-supply fluctuation (`bump`) detectors.

Either can terminate the pause early and cause another refresh burst to begin.

This gives direct period evidence for a hybrid maintenance policy:

```text
scheduled maximum pause
    OR
observed retention-risk evidence
    OR
supply-disturbance evidence
        -> resume refresh work
```

Therefore:

```text
refresh cadence policy
    != one fixed periodic timer only
```

The patent does not prove that every commercial device enabled all of these options. It proves that the disclosed control architecture explicitly composes deadline and observed-condition triggers.

---

## H8 — programmable thresholds compensate for specification and process variation

The patent uses programmable/fuse-set detection thresholds around the shared counter outputs. The specification explains that these settings can accommodate different DRAM specifications and oscillation-period variation caused by manufacturing process variation.

This is a useful maintenance-policy boundary:

```text
same logical self-refresh function
    !=
one immutable physical timing constant across dies/products
```

A device can preserve the same external functional category while parameterizing the internal timing relation against process-dependent oscillator behavior.

The programmable threshold is not itself evidence of field-adaptive calibration or runtime learning; the disclosed mechanism is bounded to the patent's programmable/fuse setting arrangement.

---

## H9 — leaving self-refresh discards the shared counter's regime-local phase

The patent describes the multi-purpose counter as normally forced into reset outside the relevant self-refresh sequence. Loss of the CBR/self-refresh condition resets the mode and forces the counter back into its reset state.

This is historically important because it blocks a modern persistence reading of the control state:

```text
self-refresh timer/count state
    = powered regime-local operational state

not

self-refresh timer/count state
    = nonvolatile restart checkpoint
```

The patent does not describe these phase/count values as surviving loss of power or controller reset.

---

## H10 — whole-array completion is defined relative to a particular refresh geometry

The patent's worked example uses 4K / 4096 refresh operations as the count for a complete pass. It also says the design may be adapted to different refresh-cycle counts such as 1K, 2K, or other values.

So the correct historical relation is:

```text
whole-array completion
    = completion under the configured product refresh geometry
```

not:

```text
whole-array completion
    = universally 4096 operations
```

This keeps the completion signal tied to device organization rather than turning an example constant into a general DRAM law.

---

# Engineering reconstruction

The following vocabulary is project reconstruction, not Hitachi's period terminology.

## E1 — control-state role and physical embodiment are orthogonal

The most important result of this slice is that **one hardware register/counter block is not necessarily one semantic state category**.

A naïve architecture inventory might say:

```text
oscillator
counter
address counter
controller
```

The retention analysis needs a different decomposition:

```text
entry-qualification state
whole-array completion-count state
pause/deadline state
coverage-position state
refresh-pulse generation state
mode state
risk-observation state
```

Several of these can occupy the same physical counter at different phases, while two seemingly similar `counts` can live in distinct counters because they answer different questions.

Thus:

```text
state role
    !=
state storage element
```

---

## E2 — progress evidence and position evidence should not be collapsed

The `RC` relation answers roughly:

> Has the required number of refresh operations for this pass completed?

The refresh-address counter answers roughly:

> Which refresh row/address is next?

Those are related but not identical.

A useful reconstruction is:

```text
coverage position
    -> selects next maintenance target

completion count
    -> qualifies transition out of the active refresh phase
```

A system can therefore have correct-looking activity without a correct next-target relation, or have a plausible address pointer without sufficient evidence that the current pass has completed.

The patent does not analyze such faults explicitly; that is an engineering inference from the separated blocks and roles.

---

## E3 — self-refresh mode is a container for several maintenance phases

The patent distinguishes at least:

```text
entry qualification
    -> burst refresh
    -> pause
    -> burst refresh
    -> pause
    ...
```

while all of this belongs to one higher-level self-refresh regime.

Therefore:

```text
mode state
    !=
maintenance phase
    !=
coverage completion
```

This is useful when comparing DRAM to other systems in the repository that also expose a broad maintenance mode but require finer internal progress state.

---

## E4 — maintenance recurrence can be deadline-conditioned and evidence-conditioned at once

The maximum-pause counter supplies a deadline-like upper bound. The dummy-cell and supply-bump paths can shorten that interval.

The reconstructed policy therefore has two independent inputs:

```text
time since last completed burst
    + observed physical-risk signals
        -> next maintenance admission
```

That blocks a common simplification:

```text
self-refresh = fixed periodic refresh
```

At least in this disclosed architecture, the recurrence rule can be conditional even while the interface still presents one self-refresh mode.

---

## E5 — the shared counter is an economy of implementation, not a proof of semantic equivalence

The patent's stated design motivation includes circuit simplification by sharing counting resources because the relevant counting operations do not occur simultaneously.

That is exactly why semantic interpretation must not follow block count mechanically:

```text
shared hardware because phases are mutually exclusive
    !=
shared meaning across phases
```

The same bits can successively mean:

- elapsed entry time;
- refresh-operation count;
- elapsed pause time.

This is a strong counterexample to treating every persistent or operational register as having one timeless interpretation independent of control phase.

---

## E6 — these control states have short persistence horizons but high authority while live

The patent's control state is not described as durable across power loss. Yet while the self-refresh regime is active, the counter, address progression, completion signal, and pause logic directly determine whether the payload continues to receive timely restoration.

So:

```text
short persistence horizon
    !=
low correctness authority
```

This complements the repository's existing maintenance-control-state synthesis: some highly authoritative retention state only needs to survive within one powered maintenance episode because it can be reinitialized when the regime is exited.

---

## E7 — internal autonomy remains conditional on retained infrastructure

The self-refresh interval is autonomous only relative to the external clock/refresh schedule. It still depends on:

- VCC;
- the internal oscillator/current source;
- counter/control logic;
- refresh-address progression;
- sense/restore circuitry;
- timing thresholds;
- the integrity of the mode condition.

Thus:

```text
external autonomy
    !=
maintenance-free retention
```

The locus of responsibility has moved inward; the dependency graph has not disappeared.

---

# Functional comparison

## A1 — relation to the existing 1984–1988 TI/NEC Case 03 deepening

The earlier Case 03 evidence already established:

```text
on-chip refresh-address counter
    !=
on-chip autonomous cadence
```

and a patent-level distinction between CBR refresh and timer-backed self-refresh.

The Hitachi family should therefore not be presented as the first discovery of that distinction.

Its added value is different:

```text
older bounded evidence:
where coverage state and cadence generation can reside

Hitachi 1993-priority architecture:
how one on-chip cadence/control design multiplexes
entry qualification + pass completion + pause timing
while keeping refresh-address progression separate
```

This is a mechanism deepening, not an invention-priority claim.

---

## A2 — relation to Micron 1993 named-product self-refresh evidence

Micron's March-1993 `MT4C8512/3 S` documentation grounds a named-product manufacturer-document witness for internal self-refresh clocking plus an internal refresh counter/controller, but the data sheet does not expose the exact oscillator/counter circuit.

The Hitachi patent supplies circuit-level design evidence from the same historical neighborhood, but it is **not** used to fill in Micron's undocumented internals.

Therefore:

```text
Micron named-product behavior
    +
Hitachi circuit-level patent design
    !=
proof that Micron implemented the Hitachi circuit
```

The sources are complementary only at the functional comparison level.

---

## A3 — relation to Hitachi HM5118165L 1996–1997 handoff evidence

The later Hitachi product datasheet grounds explicit entry/exit and whole-array coverage obligations for a named EDO DRAM family.

The present patent family reveals a much deeper internal phase/control design, but no direct document inspected in this slice maps `US5453959A/JPH06282985A` onto the `HM5118165L` implementation.

Therefore:

```text
same vendor
    + similar self-refresh interface
    + compatible date order
    !=
proven product implementation lineage
```

A future named-product linkage would require a product block diagram, design note, die/circuit disclosure, patent marking, or other direct evidence.

---

# Philosophical interpretation

The technical fact that supports a narrow conceptual observation is not simply that DRAM `needs refresh`.

Here, continuity is produced by a control apparatus in which the same small physical counter can successively mean different things because the maintenance regime changes its interpretation over time.

A bounded interpretation is:

> retained availability depends not only on preserving values, but on preserving or correctly reconstituting the *relations that make control-state values meaningful in their current phase*.

That does not make the DRAM counter an archive, memory in the human sense, or a historical narrative. The observation stops at the documented phase-dependent control mechanism.

---

# Explicit non-claims

This slice does **not** establish that:

1. Hitachi invented DRAM self-refresh;
2. `JPH06282985A` is the first self-refresh patent;
3. the Japanese filing date is the first date on which anyone built this circuit;
4. the inventors' earlier three-counter design was publicly available before the patent disclosure;
5. the disclosed embodiment shipped in a specific Hitachi DRAM product;
6. `HM5118165L`, `HM51S4170C`, `HM5241605`, or any other named part implemented this exact circuit;
7. a common vendor and plausible chronology prove product genealogy;
8. every self-refresh DRAM uses burst-refresh-plus-pause rather than distributed refresh;
9. every self-refresh DRAM uses a ring oscillator;
10. every self-refresh DRAM uses one shared multi-purpose counter;
11. 4096 refresh operations is a universal whole-array count;
12. the shared counter itself generates the refresh row address;
13. the `RC` completion indication is a host-visible status bit;
14. internal completion indication is a durable checkpoint;
15. counter state survives reset or power loss;
16. the patent proves arbitrary brownout behavior;
17. the dummy-cell leakage monitor was enabled in every implementation covered by the claims;
18. the supply-bump path provides a quantified power-failure guarantee;
19. fuse-set thresholds imply runtime adaptive learning;
20. process compensation removes all retention-time variation;
21. a whole-array pass guarantees every cell has equal remaining margin;
22. self-refresh mode membership proves the current burst/pause phase;
23. internal cadence autonomy proves foreground read availability;
24. this patent establishes JEDEC self-refresh standard chronology;
25. functional similarity to later DRAM or other maintenance systems proves historical continuity.

---

# What this changes in Case 03

The existing Case 03 model already separated payload, cadence, coverage, arbitration, mode, and handoff. This slice adds a new internal control-state distinction:

```text
payload charge state
    ↓
refresh-address / next-target state
    ↓
refresh-operation completion count
    ↓
maintenance phase
    ↓
mode-entry / pause timing state
    ↓
condition-trigger evidence
    ↓
self-refresh regime
```

The arrows are not a claim of one universal pipeline. They indicate separable relations that the Hitachi design composes.

Most importantly:

```text
control-state semantic role
    !=
physical control-state embodiment
```

and:

```text
coverage-position state
    !=
coverage-completion evidence
```

The slice therefore partially closes the evidence-index debt for **internal self-refresh timer/counter architecture** at the patent-design level. It does **not** close the stronger debt for a **named shipping/product-family implementation** of that exact architecture.

---

# Remaining evidence debt

The most valuable next work is now narrower:

1. **Named-product implementation linkage.** Find a manufacturer product datasheet, application note, circuit block diagram, die description, or patent-marking trail that directly associates a shipping/named DRAM with an oscillator + refresh-address counter + completion/pause counter architecture.
2. **Production/shipment evidence.** Keep product availability separate from patent disclosure and from `ADVANCE` manufacturer documentation.
3. **Fault behavior.** Determine what happens if the oscillator, counter, address progression, or pause logic is disturbed mid-self-refresh.
4. **Transition observability.** Identify whether any period controller/product exposes externally observable evidence for internal whole-array completion rather than only mode entry/exit timing.
5. **JEDEC chronology.** Keep standard revision history separate from vendor patents and product documents.
6. **Cross-vendor architecture.** Compare only after obtaining equally detailed circuit evidence; do not infer universal self-refresh internals from one patent family.

---

# Related-repository routing

Fresh searches of `tmzncty/computing-archaeology` for `HM51S4170C`, `self refresh`, and `5453959` found no dedicated packet to reuse for this slice.

Keep here:

- the distinction between control-state role and physical embodiment;
- refresh-position versus completion evidence;
- mode phase versus mode membership;
- deadline-triggered versus condition-triggered recurrence;
- regime-local control-state persistence horizon;
- strict product/patent genealogy boundary.

Route primarily to `computing-archaeology`:

- broad Hitachi DRAM product genealogy;
- oscillator/counter circuit evolution across vendors;
- semiconductor-process and battery-backup product history;
- patent-network genealogy beyond what changes the retention argument;
- market adoption and shipment chronology.

---

# Sources

## Primary

- Hitachi Ltd. / Texas Instruments Japan Ltd., `JPH06282985A`, **Dynamic RAM**, filed 30 March 1993, published 7 October 1994: <https://patents.google.com/patent/JPH06282985A/en>
- Toshiyuki Sakuta and Tomohiro Suzuki, `US5453959A`, **Semiconductor memory device having a self-refreshing control circuit**, U.S. filing 30 March 1994, granted 26 September 1995: <https://patents.justia.com/patent/5453959>

## Existing repository context

- [`03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md`](03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md)
- [`03-micron-1993-self-refresh-handoff-primary-witness-deepening.md`](03-micron-1993-self-refresh-handoff-primary-witness-deepening.md)
- [`03-hitachi-1996-1997-self-refresh-mode-handoff-deepening.md`](03-hitachi-1996-1997-self-refresh-mode-handoff-deepening.md)
- [`03-dram-refresh-evidence-index.md`](03-dram-refresh-evidence-index.md)

Case 03 remains **`grounded`**.