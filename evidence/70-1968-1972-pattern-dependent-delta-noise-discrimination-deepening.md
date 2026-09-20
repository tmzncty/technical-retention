# Evidence 70F — 1968–1972 pattern-dependent delta noise and read-discrimination control

**Status:** `bounded deepening complete`

## Research slice

This packet deepens Case 70 along one narrow boundary:

> In a coincident-current ferrite-core array, can the target bit remain physically correct while the *stored pattern in other cores* changes the aggregate sense-line noise enough to threaten read classification, and what kinds of control were proposed to preserve discrimination?

It does **not** reopen the general history of magnetic-core memory. Case 70 already establishes half-select disturbance, shared-sense effects, temperature/current/strobe margins, and several named production/service witnesses. This packet adds two 1968–1969-filed primary patent records that make the **pattern dependence, array-size dependence, and discrimination-control response** unusually explicit.

The relevant distinction is:

```text
retained target state
    !=
neighbor-data pattern
    !=
aggregate sense-line waveform
    !=
discriminator threshold/timing state
    !=
successful symbolic read
```

---

## Sources inspected

### P1 — General Motors, US 3,564,517

William E. McLean, Hayden A. Nelson, and David E. Ruch, **“Combined DRO and NDRO Coincident Current Memory,”** US Patent 3,564,517, filed 24 June 1968, issued 16 February 1971, original assignee General Motors Corporation.

Public primary-text rendering:

- Google Patents: <https://patents.google.com/patent/US3564517A/en>

The patent is used here as a **1968-filed design record**, not as proof that every GM computer, every production core stack, or every contemporary vendor used the disclosed arrangement.

### P2 — Core Memories Inc., US 3,646,531

**“Magnetic Core Signal Discrimination Method,”** US Patent 3,646,531, application 04/865373, filed 10 October 1969, published/issued 29 February 1972; the public patent record identifies Core Memories Inc. as the assignee in the title record.

Public text transcription inspected:

- FreePatentsOnline: <https://www.freepatentsonline.com/3646531.html>

This is a public transcription of the patent text rather than a newly page-inspected facsimile in this pass. Accordingly, this packet uses it for claim/content-level evidence and preserves that custody limitation explicitly.

### Companion-repository check

A fresh search of `tmzncty/computing-archaeology` for `3646531 delta noise worst-case core memory` and for broader core-memory margin terms found no dedicated packet for these two records. The broad magnetic-core history remains there; this packet keeps only the retention-specific seam.

---

# I. Historical record

## H1 — Pattern-dependent partial-select noise was treated as a read-discrimination problem

P2 says conventional ferrite-core memories attempted to cancel partial-select or `zero` noise by how the sense winding was threaded. It then identifies a residual component caused by asymmetry/nonlinearity of the cores’ B-H behavior: half-selected cores containing different stored states do not necessarily generate identical waveforms, leaving non-cancelled **delta noise**.

The patent explicitly says this residual can add to or subtract from the selected core’s sensed `zero` or `one` signal.

The historical point is stronger than the generic statement `half-selected cores make noise`:

```text
same selected address
+ same drive operation
+ different surrounding stored pattern
    -> different aggregate sense-line interference
```

In the vocabulary of P2, there is a **“worst-case” pattern** that maximizes uncancelled delta noise for a given plane/winding arrangement.

This is primary evidence that engineers treated the *contents of neighboring cores* as part of the electrical read context even when those neighbors were not the logical target.

## H2 — P2 gives bounded array-size examples rather than a universal scaling law

P2 gives two concrete examples.

For its illustrated `64 core plane`, selecting one core leaves seven unselected cores in each selected row/column half-selected; under the described worst-case pattern the patent states that seven delta-noise contributions can remain in the sensed output.

It then says that as an array is expanded, additional rows/columns can contribute additional worst-case noise, and gives a `64 × 64` plane example with **63 delta-noise contributions** adding to or subtracting from the selected-core signal. The patent says this total can be comparable to a low-amplitude `one` signal.

These numbers are bounded examples from the disclosed geometry and winding organization. They are **not** a universal law that every 64 × 64 ferrite plane produces exactly 63 equal noise contributions, nor a measured population distribution for shipped memories.

## H3 — The noise and the desired turnover signal occupy different temporal regions

P2 says the delta noise arises largely from reversible flux change associated with changing drive current, while the selected-core switching/turnover signal peaks later. It therefore treats discrimination as a **waveform-in-time** problem, not merely an amplitude-at-rest problem.

The patent contrasts a conventional constant threshold plus strobe with a proposed time-dependent threshold:

1. hold the discrimination threshold high during the early high-noise interval;
2. after the noise peak, lower the threshold;
3. place the later threshold between expected maximum noise and minimum valid turnover-signal envelopes;
4. sample near the useful turnover-signal interval.

P2’s disclosed implementation uses a threshold-control amplifier and an RC-shaped decaying threshold. That circuit is a proposed implementation, not proof of universal production practice.

## H4 — P2 explicitly exposes a material-selection / circuitry tradeoff

P2 says that one way to tolerate a poor signal-to-noise ratio is to reject cores whose turnover signal is not sufficiently above the maximum expected delta noise, but that this produces a high rejection rate. Its variable-threshold method is presented as a way to discriminate a wider range of valid turnover signals in a noisy environment.

Thus the historical record itself exposes at least two possible engineering levers:

```text
narrow accepted core population
or
change the read discriminator
```

This packet does not infer production yield numbers from the phrase `high rejection rate`; the patent supplies no population statistic here.

## H5 — P1 shows a different route: reshape geometry/timing so aggregate shuttle noise remains discriminable

P1 combines an alterable destructive-readout (`DRO`) region with a fixed-program nondestructive-readout (`NDRO`) region that shares parts of the addressing/sensing apparatus.

The fixed region encodes some information by **omitting cores at selected locations**. P1 explains that these omissions can unbalance normally cancelling shuttle-noise contributions on the sense line. Under a worst-case condition, remaining cores on a drive line may contribute shuttle signals of the same polarity, allowing the contributions to combine rather than cancel.

For the **described embodiment**, P1 states that the core/sense-amplifier combination can tolerate up to **12 uncancelled shuttles** while preserving an acceptable signal-to-shuttle-noise ratio. It immediately treats larger possible counts as a design problem.

That `12` is explicitly bounded to the described embodiment. It must not be converted into a universal ferrite-core limit.

## H6 — P1 distributes the response across timing and sense topology

P1 describes several controls for the disclosed combined DRO/NDRO design:

- concentrate the larger delta/minor-loop effects into one axis by the arrangement of core positions;
- drive X and Y with different rise behavior;
- start one axis earlier so its delta-noise transient can decay before the other axis produces the switching condition;
- use a more slowly rising Y current to reduce the relevant delta-noise contribution;
- split the sense winding so the number of uncancelled shuttle contributions reaching any one sense amplifier remains within the bounded tolerable count.

The patent therefore supplies a period example where preserving readability is not one `sense amplifier margin` knob. Geometry, current waveform, relative timing, and sense partitioning are coordinated.

## H7 — P1 and P2 are not one technical lineage established by this packet

P1 was filed in 1968 by General Motors personnel; P2 was filed in 1969 and assigned to Core Memories Inc. Both address pattern-dependent/partial-select readout noise, but this packet has not established that one copied, licensed, descended from, or directly influenced the other.

Their safe relation here is a **contemporaneous functional comparison**:

```text
P1: control the interference presented to a sense amplifier
P2: adapt the discriminator threshold to the interference over time
```

No genealogy is asserted.

---

# II. Engineering reconstruction

## E1 — Neighbor payload can become read-context state without becoming target payload

The surrounding cores retain ordinary payload bits. During a read of another address, those values can alter the aggregate partial-select waveform seen by the shared sense path.

Therefore, for this bounded architecture:

```text
target logical value
    !=
neighbor logical values

but

neighbor logical values
    -> read-context-dependent noise
    -> target recoverability margin
```

This does **not** mean the neighbors become metadata or control state. They remain payload. Their current arrangement has an incidental electrical role in whether another payload item is recoverable.

## E2 — Physical survival and symbolic recoverability remain separable

Neither P1 nor P2 requires the target core’s remanent state to have already been destroyed in order for a read error to occur. A correctly retained `one` can be missed if its turnover signal falls below the discriminator under the present noise/threshold condition; a `zero` can be threatened if aggregate noise crosses the discrimination boundary.

So:

```text
correct remanent state
    !=
correct sense classification
```

This extends Case 70’s earlier `sense disturbance != stored-state corruption` boundary with an explicit pattern/array-scaling witness.

## E3 — Readability margin is relational, not a property of one core alone

A per-core statement such as `this core produces a valid turnover pulse` is insufficient to characterize system readability.

The effective margin depends on relations among:

```text
selected-core signal
neighbor-state pattern
array geometry
sense-winding topology
drive-current waveforms
relative timing
discriminator threshold
strobe time
```

The exact list varies by design. The point is not that every machine uses these exact controls; the point is that the cited primary records demonstrate a system-level relation in which a bit’s recoverability cannot be reduced to its isolated remanence.

## E4 — Array scaling can consume read margin without changing quiescent retention

P2’s 64 × 64 example and P1’s aggregate-shuttle reasoning both show a bounded way that a larger shared-sense structure can create more opportunities for non-target contributions to accumulate.

This supports the engineering distinction:

```text
quiescent magnetic retention
    !=
readout scalability margin
```

The packet does not infer a monotonic universal `array size -> failure rate` equation. Winding patterns, partitioning, current timing, core uniformity, thresholds, and circuit design can change the relation.

## E5 — Discrimination control is not payload restoration

P2’s moving threshold improves the receiver’s decision boundary. P1’s timing/topology choices reduce or redistribute interfering contributions. Neither operation, by itself, rewrites a degraded target bit.

Therefore:

```text
read-discrimination control
    !=
payload restoration
    !=
neighbor refresh
```

A successful read may still be followed by normal destructive-read restore in a DRO memory, but that is a separate stage.

## E6 — Timing can trade latency against noise exposure

P2 explicitly notes that separating the two half-select-current applications in time can let one noise transient decay before the next, but at the cost of increased access time; its proposed variable threshold instead tries to exploit the temporal separation between early noise and later turnover signal.

P1 likewise deliberately staggers/reshapes axis currents in its NDRO read path.

The bounded engineering relation is:

```text
more temporal separation
    -> potentially easier discrimination
    -> possible access-time / waveform-design cost
```

This is not a universal quantitative latency law.

## E7 — A `worst-case pattern` is a test/adversarial context, not a second copy of the data

The stored pattern already exists as payload. Calling one arrangement `worst case` does not create a separate retained metadata object. The term identifies a payload arrangement that stresses the shared read path.

This matters for later comparisons with explicit maintenance metadata: a machine can have a hidden dependency on retained context without separately storing a `noise state` record.

---

# III. Controlled cross-case comparison

## FA1 — Relation to Case 53 RowHammer and Case 52 NAND read disturb

The safe functional analogy is only:

> Operations or states outside the logical target can influence whether the target or neighboring retained state remains usable.

The mechanisms differ sharply:

- ferrite core: partial-select magnetic response plus shared analog sense summation;
- DRAM RowHammer: repeated activation-associated electrical disturbance of neighboring cells;
- NAND read disturb: pass/read-bias stress and charge-threshold movement.

The core case here is primarily a **read-discrimination context** problem; the later semiconductor cases can involve actual stored-state degradation. No ancestry or quantitative mapping is claimed.

## FA2 — Relation to Case 65 NAND read-reference adaptation

A still narrower analogy exists between P2’s time-varying discrimination threshold and later systems that adapt read references: in both cases the receiver’s interpretation boundary can be changed without immediately rewriting the payload.

But:

```text
ferrite time-dependent voltage discriminator
    !=
NAND threshold-voltage read-reference optimization
```

They operate on different physical signals, failure mechanisms, timescales, and historical lineages. The analogy is useful only for the repository-level distinction:

```text
change how retained state is interpreted
    !=
change the retained physical state itself
```

## FA3 — Relation to error-correcting or replica repair systems

P1/P2 attempt to preserve **first-pass analog discrimination**. They are not ECC decoders, scrubbing mechanisms, quorum repair, or replica reconciliation.

Do not translate `noise margin` into `redundancy margin` without an explicit intervening mechanism.

---

# IV. Philosophical / media-theoretical interpretation — bounded

The technical evidence supports one narrow project-level interpretation:

> **A retained state can remain materially present while its availability depends on the simultaneous state of other retained objects and on a transient interpretive apparatus.**

This is stronger than saying `reading needs electronics`, but weaker than claiming that every stored bit is ontologically distributed across the whole machine.

For the bounded core arrays here, the target’s recoverability is relational because shared conductors and analog summation make surrounding payload patterns electrically relevant at read time.

A second bounded formulation is:

```text
persistence of inscription
    !=
isolation from context
```

The target is not protected by being physically untouched by the rest of the plane. It is made usable by keeping context-dependent interference inside a discriminable region.

These are later project interpretations. P1 and P2 did not formulate a philosophy of contextuality or technical memory.

---

# V. Explicit non-claims / stop conditions

1. `worst-case pattern` does **not** mean all ordinary workloads frequently realize the patent’s maximum-noise configuration.
2. `64 × 64 -> 63 delta noises` in P2 does **not** define a universal formula for every ferrite plane.
3. P1’s `12 uncancelled shuttles` is **not** a universal production tolerance.
4. A patent’s described embodiment is **not** proof of broad commercial deployment.
5. Filing date is **not** automatically first invention, first use, first shipment, or first discovery of delta noise.
6. P1 and P2 do **not** establish a direct GM → Core Memories Inc. genealogy.
7. Aggregate sense noise does **not** prove permanent corruption of the half-selected neighbors.
8. A missed `one` due to threshold/noise does **not** prove the target remanent state had decayed.
9. Variable thresholding does **not** restore payload state.
10. Staggered X/Y timing does **not** constitute periodic refresh.
11. Sense-winding partitioning does **not** change the logical contents merely because it changes readout topology.
12. Core rejection mentioned by P2 does **not** provide a measured production yield or vendor-lot distribution.
13. The patent examples do **not** establish a statistical field-error rate.
14. Array-size examples do **not** prove larger arrays are universally less reliable; designers can change topology and circuits.
15. `neighbor payload influences read context` does **not** make neighbor payload into controller metadata.
16. A worst-case test pattern is **not** a retained maintenance-history log.
17. `read discrimination` is **not** synonymous with ECC.
18. `noise margin` is **not** synonymous with redundancy margin.
19. The moving-threshold analogy to NAND read-reference optimization is functional only, not historical or physical identity.
20. No claim is made that Forrester/Papian/Bauer-Haynes directly anticipated the exact P1/P2 circuits.
21. No claim is made that every machine used a single shared sense line across an entire plane.
22. No claim is made that delta noise is the only source of ferrite-memory read error.
23. No claim is made that quiescent remanence is indefinite under every temperature, magnetic field, or mechanical condition.
24. No claim is made that successful symbolic read proves all operating margins are healthy.
25. No claim is made that a successful worst-case-pattern test proves a lifetime reliability guarantee.

---

# VI. Claim ledger

| Claim | Type | Evidence strength / boundary |
| --- | --- | --- |
| P2 describes residual pattern-dependent delta noise from half-selected cores | H/P | direct patent text transcription |
| P2 names a `worst-case` stored pattern for maximum uncancelled noise | H/P | direct patent text transcription |
| P2 gives a bounded 64 × 64 example with 63 delta-noise contributions | H/P | direct disclosed example; not universalized |
| P2 distinguishes early delta-noise peak from later turnover-signal peak | H/P | direct patent mechanism description |
| P2 proposes a time-dependent decreasing discrimination threshold | H/P | claim + disclosed implementation |
| P2 says strict signal/noise acceptance can cause core rejection | H/P | direct background statement; no yield statistic inferred |
| P1 says omitted fixed-memory core positions can unbalance cancelling shuttle noise | H/P | direct Google Patents text |
| P1 gives a bounded tolerance of up to 12 uncancelled shuttles in its described embodiment | H/P | direct embodiment-specific statement |
| P1 uses waveform timing/rise behavior and split sense windings to keep interference discriminable | H/P | direct patent description |
| Neighbor payload can function as read context without becoming metadata | E | reconstruction from pattern-dependent shared-sense mechanism |
| Correct remanent state can coexist with failed symbolic classification | E | reconstruction bounded by P1/P2 discrimination problem |
| Quiescent retention and readout scalability margin are distinct | E | bounded system reconstruction |
| Variable threshold / timing / sense partitioning are discrimination controls, not payload restoration | E | mechanism reconstruction |
| Core delta-noise control is historically identical to NAND read-reference optimization | X | rejected |
| Patent examples establish universal ferrite-array tolerance constants | X | rejected |

---

# VII. Navigation / repository placement

This packet belongs under **Case 70 — Coincident-Current Magnetic Core Half-Select Disturbance** because it deepens the existing split between retained-state disturbance and sense-line disturbance. It does not create a new generic magnetic-core case.

The broad technical history remains in:

- `tmzncty/computing-archaeology/docs/memory/why-core-memory-was-worth-weaving.md`

A fresh companion search found no dedicated packet for US 3,564,517 / US 3,646,531 or their pattern-dependent read-discrimination seam. Broader patent genealogy, commercial use by specific manufacturers, production yield, core-vendor sorting, and the general history of sense-amplifier design should remain `computing-archaeology` work if pursued.

For `technical-retention`, the durable addition is the controlled relation:

```text
retained payload may remain physically correct
while
other retained payload + shared read topology + transient discriminator state
determine whether it is presently recoverable
```

---

# VIII. Remaining evidence debt after this slice

This packet does **not** close Case 70’s broader production-distribution debt. High-value follow-ons remain:

- factory core-sorting or lot-acceptance records with measured signal/noise distributions;
- production worksheets connecting individual stack margin measurements to acceptance/rework decisions;
- field-return records tying observed read failures to pattern/noise margin rather than other causes;
- direct named-product evidence that a time-varying threshold like P2’s was shipped;
- quantitative comparison of array geometry/sense partitioning across vendors;
- earlier primary records tracing when `delta noise`, `worst-case pattern`, and `shmoo` vocabulary became routine engineering terms.

Those are archival/technical-history questions, not prerequisites for the bounded conclusion established here.
