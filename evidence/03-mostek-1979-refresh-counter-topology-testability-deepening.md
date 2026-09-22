# Case 03 Deepening — Mostek 1979 Refresh-Counter Topology and Testability Boundary

**Status:** `bounded deepening complete`

## Research question

Case 03 already has strong product-document evidence that Mostek's MK4164 exposed a dedicated `RFSH` input, used an on-chip refresh counter in that mode, and required 128 refresh cycles within 2 ms. The 1980 Mostek material further says that the internal refresh counter is itself dynamic and requires refreshing.

One debt remained deliberately open:

> What, if anything, can contemporary Mostek primary material establish about the internal refresh-counter circuit, rather than merely its externally visible behavior?

A second question follows immediately:

> If the refresh counter is internal, how did a manufacturer determine that its hidden coverage progression was actually correct rather than merely observing that payload bits happened to survive a test interval?

Two Mostek-assigned patent families filed in 1979 materially narrow those questions:

1. Robert James Proebsting's **refresh-counter test** filing, priority **15 May 1979**, which treats an internal refresh counter as hidden state whose sequence cannot be read directly and proposes making its selected row observable through a controlled write side effect;
2. Sargent S. Eaton, Jr. and Paul R. Schroeder's **refresh counter** filing, filed **13 August 1979**, which gives a concrete on-chip counter embodiment that reuses ordinary address-buffer circuitry, stores per-bit refresh state, and conditionally inverts that state at the end of refresh cycles.

The bounded result is:

```text
product documentation says an internal counter exists
    !=
product documentation exposes its circuit topology

same-vendor contemporary patent exposes a counter topology
    !=
that topology is proven to be the MK4164 production implementation

payload survives a bounded refresh test
    !=
all internal refresh rows were necessarily visited

hidden maintenance-control state
    -> may need a separate observability / test path
```

This slice therefore **partially closes** the MK4164 topology debt. It supplies a concrete Mostek company-level candidate circuit and a contemporary Mostek testability mechanism, but it does not identify either patent as the exact MK4164 silicon implementation.

---

## Why this slice is not a duplicate

The existing files answer adjacent but different questions:

- [`03-mostek-1979-1980-rfsh-dynamic-counter-deepening.md`](03-mostek-1979-1980-rfsh-dynamic-counter-deepening.md) establishes the **named-product interface and maintenance-state behavior** of the MK4164;
- [`03-ti-1978-onchip-refresh-counter-prior-art-topology-deepening.md`](03-ti-1978-onchip-refresh-counter-prior-art-topology-deepening.md) establishes an earlier **TI filing/priority floor** plus one TI latch/adder counter embodiment;
- this file asks what contemporary **Mostek** patent material says about internal topology and about verifying hidden coverage-state correctness.

The distinction matters because a product brief, a patent embodiment, and a production mask set are different evidence objects.

```text
named product behavior
    !=
patented circuit embodiment
    !=
verified product transistor topology
```

---

## Source custody and dating

### Primary product-document context — Mostek MK4164

The existing Case 03 evidence directly inspected Mostek's 1979 and 1980 memory documentation. The 1979 product brief names:

- `128 cycle refresh (2ms)`;
- `On chip refresh counter on pin 1`;
- pin 1 as `RFSH`.

The later detailed Mostek material supplies the stronger maintenance-state claim that the internal refresh counter is dynamic and itself requires refresh.

Those product records remain the primary source for **what Mostek advertised for the named MK4164**. This file does not replace them with patent inference.

See:

- [`03-mostek-1979-1980-rfsh-dynamic-counter-deepening.md`](03-mostek-1979-1980-rfsh-dynamic-counter-deepening.md)

### Primary patent — Proebsting / Mostek refresh-counter test

**Robert James Proebsting, “Refresh counter test,” Mostek Corporation.**

Checked patent-family records:

- US family member: `US4347589A`;
- US priority / filing date: **1979-05-15**;
- US grant / publication date: **1982-08-31**;
- European application: `EP0019150A1`;
- European publication date: **1980-11-26**;
- original assignee shown in the checked European record: **Mostek Corp**.

Public records:

- <https://patents.google.com/patent/US4347589A/en>
- <https://patents.google.com/patent/EP0019150A1/en>

The European publication is especially useful because its description states the test problem and the interface assumptions explicitly. It says that some RAMs have an on-chip refresh counter whose output cannot be read directly. It then describes a separate refresh input that selects an internally generated row address and a test sequence that permits writing into the row chosen by that internal counter.

**Chronology boundary:** the 15-May-1979 filing/priority date is not itself a 1979 public patent publication. The checked European A-publication is dated 26-Nov-1980. The existing 1979 MK4164 product document therefore remains a separate public-product witness.

### Primary patent — Eaton / Schroeder / Mostek refresh-counter circuit

**Sargent S. Eaton, Jr. and Paul R. Schroeder, “Refresh counter,” `US4296480A`.**

- original assignee: **Mostek Corporation**;
- US filing / priority date: **1979-08-13**;
- US publication / grant date: **1981-10-20**;
- British A-publication in the family: `GB2056138A`, **1981-03-11**.

Public records:

- <https://patents.google.com/patent/US4296480A/en>
- <https://patents.google.com/patent/GB2056138A/en>

The checked US text says the purpose is to place a refresh counter on chip while minimizing extra area by reusing circuitry already present in the DRAM, especially the address buffers.

Again, the filing date is evidence of a filed Mostek design claim, not a public-disclosure date and not proof of shipment.

---

## Historical record

### H/P — Mostek's 1979 test filing treats refresh progression as hidden internal state

Proebsting's filing begins from a manufacturing-test problem. It says that in many earlier RAM arrangements the refresh counter was external, but that other RAMs have the refresh counter on chip. For the latter, the counter output cannot simply be read directly.

The test problem is therefore not merely whether data survive. It is whether the **coverage mechanism** actually visits the intended rows.

The source explains why a naive retention wait is weak evidence: the guaranteed retention requirement might be about 2 ms, while many particular bits can hold data for far longer — the description gives examples on the order of 200 ms or more. A row skipped by a defective counter could therefore still appear correct during a shorter test because the bits in that row had not yet leaked enough to fail.

That gives a direct historical boundary:

```text
payload still readable after a test interval
    !=
refresh counter proven to have covered every required row
```

The problem is not philosophical. The patent frames it as manufacturing test cost and certainty.

### H/P — the test method converts hidden coverage state into an observable payload side effect

The proposed test writes a known background, then uses the refresh path to select a row according to the internal refresh counter. In a special sequence, row-address strobe, column-address strobe, and write control are allowed to write into the row selected by the refresh counter.

The sequence is repeated until every row should have been selected. The memory is then read through the ordinary address path. If the expected location in every row was changed exactly as intended, the test has evidence that the internal counter reached those rows.

The important historical relation is:

```text
internal refresh-counter state
    -> selects hidden row address
    -> controlled write side effect
    -> ordinary readback
    -> counter-coverage evidence
```

The test does not make the counter value itself an ordinary user-readable register. It makes **the consequences of the hidden state** observable.

### H/P — the test filing keeps internal and external address authority distinct

The Proebsting description shows separate paths for:

- an externally supplied row address;
- an internally generated refresh-counter address;
- gating controlled by the refresh signal so one or the other reaches the row decoder.

In the illustrated arrangement, the refresh signal disables the external-row-address gate and enables the internal-refresh-counter gate.

Thus the same row decoder can be driven by different address authorities depending on mode:

```text
ordinary access
    -> external row address

refresh
    -> internal counter address
```

This is relevant to technical retention because `which row is next for maintenance` is real operational state even when that state is not part of the ordinary architectural address interface.

### H/P — Eaton / Schroeder explicitly aim to reuse ordinary address-buffer circuitry

`US4296480A` says that a separate counter, shift register, or ring counter would consume extra circuitry and chip area. Its proposed alternative is to use circuitry already needed by the DRAM.

The patent says:

- address buffers already produce high-level true and complement address signals;
- their inputs can select either external user addresses or internal refresh addresses;
- buffer outputs are transferred to refresh-storage nodes;
- a transfer clock occurring at the end of a refresh cycle causes selected stored bits to be inverted;
- this inversion advances the refresh count.

The source therefore supports a stronger distinction than `payload state != maintenance-control state`:

```text
logical function separation
    !=
physical circuit separation
```

The maintenance counter can be logically distinct while reusing parts of the ordinary access-address path.

### H/P — the preferred embodiment is a conditional-inversion binary up-counter

The preferred embodiment describes a binary count in which bit `i` is inverted when all required lower-order inputs are true. The first-order unit changes on every transfer-clock event; higher-order units change when the relevant lower-order state enables them.

The patent illustrates a three-order example progressing through ordinary binary states. It then says the individual units and gating may be arranged differently, including binary down or other counting arrangements.

At the unit level, the patent identifies:

- an address buffer;
- refresh storage;
- control means;
- two transfer devices;
- a decoder;
- a transfer clock;
- lower-order address-bit inputs used by the decoder.

This is a circuit-level mechanism claim, not merely the word `counter` in a block diagram.

### H/P — the patent's refresh storage is described as a cross-coupled MOSFET flip-flop

In the detailed unit description, the patent says the refresh storage is a cross-coupled flip-flop made from two MOSFETs, with each gate tied to the other device's drain. Two transfer MOSFETs connect the address-buffer outputs to those storage nodes under decoder control.

This gives a concrete Mostek patent embodiment for retaining a counter bit between refresh-cycle updates.

However, the source must **not** be silently substituted for the MK4164's exact circuit. The named-product documentation elsewhere calls the MK4164 internal refresh counter `dynamic`; the patent text here calls its illustrated refresh storage a cross-coupled flip-flop and does not name the MK4164. Without a product schematic, mask analysis, die reverse engineering, or an explicit Mostek statement linking patent and part, the relationship remains unproven.

### H/P — counter advancement is tied to the refresh-cycle boundary

The Eaton / Schroeder patent says the transfer clock is designed to occur only at the end of a refresh cycle. The selected refresh-storage bits are then inverted so the counter advances for the next cycle.

That means the counter encodes a **progress relation** rather than a log of past refresh operations:

```text
current refresh-address state
    + refresh-cycle completion event
    -> next refresh-address state
```

Nothing in the inspected text requires retention of a complete history of which earlier refresh commands occurred.

### H/P — Mostek's two 1979 filings expose different parts of the same problem class without proving one product identity

The Proebsting filing is about **testing hidden refresh-counter behavior**. The Eaton / Schroeder filing is about **implementing an on-chip refresh counter with low additional circuit area**.

They are both Mostek-assigned, both filed in 1979, and both concern an internal refresh counter feeding DRAM row selection. Those facts justify treating them as contemporary company-level evidence for the problem class.

They do **not** justify:

```text
same company
    + same year
    + same functional vocabulary
    -> same production circuit
```

No checked patent text names `MK4164`, and no checked MK4164 product document cites these patent numbers.

---

## Engineering reconstruction

The following section is reconstruction from the primary sources, not language used by Mostek.

### E — the refresh counter is a retained progress pointer

A refresh counter need not remember the whole past. It needs enough state to choose a next maintenance target such that the required row set is covered before the deadline.

In the Eaton / Schroeder preferred embodiment:

```text
retained counter state C_t
    + end-of-refresh transfer event
    -> C_(t+1)
```

The logical role is therefore closer to a **maintenance progress pointer** than to an audit history.

### E — ordinary address infrastructure can become retention infrastructure

Because the patent reuses address buffers for counter operation, the hardware that normally interprets an external address also participates in maintaining the internal sequence used to preserve payload.

Thus:

```text
ordinary access infrastructure
    can also be
retention-maintenance infrastructure
```

This does not mean the two modes are semantically identical. It means physical reuse can hide a real logical boundary.

### E — hidden control-state faults can be masked by payload retention margin

The Proebsting test rationale gives a particularly useful failure model. Suppose a counter skips one row. Immediately after the skip, the payload in that row may still be perfectly readable because the cell's actual retention time exceeds the guaranteed minimum by a large margin.

Therefore:

```text
maintenance-control fault at t0
    -> no immediate payload error necessarily visible at t0
    -> latent retention risk increases
    -> payload failure may appear only later
```

This is the same broad structural relation that later Case 03 evidence sees when coverage-state control is disturbed, but here it appears directly as a 1979 manufacturing-test problem.

### E — verification can require changing the object being observed

The counter-test method does not merely passively inspect an internal register. It lets counter-selected addressing cause controlled writes and then inspects the payload array.

So the test path is an example of **active verification**:

```text
hidden maintenance state
    -> deliberately induced externally visible effect
    -> verification
```

That is different from ordinary retained-payload readout.

### E — matching interface shape is evidence of compatibility, not circuit identity

The MK4164 product documents and the Proebsting test filing share a recognizable interface shape:

- separate refresh control from ordinary row address selection;
- internal refresh-address generation;
- ordinary RAS/CAS-style DRAM timing context.

That similarity makes the patent family relevant to the MK4164-era Mostek design space. It is still insufficient to identify a transistor-level implementation.

A safe evidence ladder is:

```text
Mostek patent mechanism
    -> company-level design evidence

Mostek product documentation
    -> named-product behavior evidence

both together
    -> stronger historical context

but not
    -> verified patent-to-product implementation mapping
```

---

## Functional comparison

### A — TI White/Rao and Mostek Eaton/Schroeder solve similar placement problems with different disclosed organizations

The 1978-filed TI White/Rao patent in the previous deepening places refresh-address state on chip and gives a preferred organization with clocked D-type latches plus binary adder/counter stages.

The 1979-filed Mostek Eaton/Schroeder patent likewise puts the counter on chip, but its stated area-saving strategy is to reuse ordinary address buffers and conditionally invert refresh-storage bits.

At a functional level both can be summarized as:

```text
external refresh event
    -> on-chip coverage state selects row
    -> row refreshed
    -> on-chip coverage state advances
```

But:

```text
same functional role
    !=
same circuit topology
    !=
documented design genealogy
```

This comparison is deliberately functional, not genealogical.

### A — testability is a different axis from retention mechanism

A memory can have a working refresh mechanism without exposing its internal coverage state directly. Conversely, a test mode can make that state inferable without changing the normal retention contract.

Therefore:

```text
retention mechanism
    !=
observability mechanism
    !=
verification procedure
```

The Proebsting filing is valuable precisely because it makes the latter two visible.

---

## Philosophical interpretation

### I — preserving an object can require preserving an invisible position in a maintenance process

The payload bit is not the only present state that matters. The machine also has to know enough about **where maintenance currently is** to continue refreshing the whole required set.

The counter therefore makes a general retention point concrete:

> A system may retain an object partly by retaining a small amount of process state about what maintenance should happen next.

This is an interpretation of the engineering relation, not period Mostek language.

### I — evidence that preservation happened can require its own channel

The Proebsting test patent adds another layer. A system may successfully expose payload while hiding the mechanism that preserved it. To establish that maintenance coverage is correct, the tester may need a separate observability path.

Thus:

```text
state being preserved
    !=
state coordinating preservation
    !=
evidence that coordination is correct
```

Again, this is project-level interpretation, not a historical claim that Mostek used this vocabulary.

---

## Explicit non-claims

This deepening does **not** establish that:

1. `US4296480A` is the exact circuit used in the MK4164;
2. `US4347589A` / `EP0019150A1` was implemented in every MK4164 production revision;
3. either patent names the MK4164;
4. Mostek's 1979 product brief cites either patent;
5. Eaton / Schroeder invented the first on-chip refresh counter;
6. Proebsting invented refresh-counter testing generally;
7. the 1979 filing dates are public-disclosure dates;
8. the patents prove a 1979 first-shipment date for the MK4164;
9. the patents prove first silicon for the MK4164;
10. the Mostek patent topology is derived from TI White/Rao;
11. the TI topology is derived from Mostek;
12. same-vendor chronology proves internal design genealogy;
13. the patent's cross-coupled refresh-storage description and the product manual's `dynamic` counter wording are identical circuit descriptions;
14. a cross-coupled circuit label by itself proves a particular static-retention or leakage behavior;
15. the product's 128-cycle refresh contract proves how many physical word lines exist at transistor level;
16. ordinary data retention testing can always detect a skipped refresh row quickly;
17. a passing bounded retention test proves the internal counter visits each row exactly once;
18. internal counter state is architecturally user-readable;
19. the test mode is part of the ordinary customer-visible interface;
20. internal coverage state is nonvolatile across power loss;
21. the counter retains a complete history of refresh events;
22. binary up-counting is a universal refresh requirement;
23. shared circuitry makes refresh and ordinary access semantically identical;
24. test observability implies ordinary operational observability;
25. verifying coverage proves the DRAM cells meet every retention specification;
26. verifying counter progression proves the external cadence is correct;
27. correct cadence proves every restore operation succeeds electrically;
28. correct counter logic proves the row decoder itself has no fault;
29. the two Mostek patent families together exhaust the MK4164 refresh design;
30. this slice closes broader 64K DRAM transistor-level genealogy.

---

## Claim ledger

| Claim | Label | Confidence | Basis |
| --- | --- | --- | --- |
| Mostek had a filed internal-refresh-counter test concept by 15-May-1979 | H/P | high | Proebsting patent-family priority metadata |
| The test filing treats the internal refresh-counter output as not directly readable | H/P | high | `EP0019150A1` description |
| Payload can remain readable even when a refresh row was skipped long enough to make short retention tests ambiguous | H/P | high | `EP0019150A1` test rationale |
| The test converts counter-selected row choice into a write/readback side effect | H/P | high | `EP0019150A1` method and circuit description |
| Mostek filed a concrete low-area on-chip refresh-counter circuit on 13-Aug-1979 | H/P | high | `US4296480A` metadata and description |
| The Eaton / Schroeder embodiment reuses address buffers in the counter function | H/P | high | `US4296480A` description |
| Its preferred binary implementation conditionally inverts higher-order state according to lower-order bits | H/P | high | `US4296480A` detailed description |
| Its refresh storage is described as a cross-coupled two-MOSFET flip-flop | H/P | high | `US4296480A` FIG. 4 description |
| Counter advancement occurs at the refresh-cycle boundary in the preferred embodiment | H/P | high | transfer-clock description |
| The patents are relevant company-level context for the MK4164-era Mostek refresh design | E | high | same assignee, period, and problem domain plus named-product documentation |
| Either patent is the exact MK4164 implementation | X | unsupported | no checked source makes that mapping |
| Hidden maintenance-state faults can precede visible payload failure | E | high | direct reconstruction of Proebsting's test rationale |
| Maintenance state may share circuitry with ordinary access state without becoming the same logical state | E/A | high | Eaton / Schroeder address-buffer reuse |
| Verification evidence is a distinct layer from retained payload and maintenance-control state | E/I | medium-high | bounded project interpretation of the test mechanism |

---

## What this changes in Case 03

Before this slice, the evidence index correctly said:

> exact MK4164 internal counter circuit topology remains open.

That sentence is now too coarse. The stronger and more precise status is:

```text
Mostek company-level contemporary counter topology
    = directly documented

exact patent-to-MK4164 production mapping
    = unproven
```

The debt therefore narrows from `find any Mostek circuit topology` to `establish or reject exact product mapping`.

A second debt is newly exposed:

```text
counter coverage correctness
    !=
payload survival during a short test
```

The Proebsting filing supplies the period mechanism for turning otherwise hidden coverage progression into observable test evidence.

---

## Remaining debt

Highest-value next work, in order:

1. find an explicit Mostek source that names `MK4164` together with `US4296480`, `US4347589`, Eaton, Schroeder, or Proebsting;
2. find a die photograph, reverse-engineering report, mask/layout document, or service/training schematic that can identify the production MK4164 refresh-counter circuit;
3. reconcile the product-document phrase that the internal counter is `dynamic` with the patent's illustrated cross-coupled refresh-storage unit without assuming they are the same implementation;
4. determine whether the Proebsting counter-test method appears in production test documentation or a named shipping part;
5. retain the separate unresolved pre-26-Jun-1978 same-die-counter priority search from the TI deepening;
6. route broad Mostek/64K-DRAM design genealogy to `tmzncty/computing-archaeology` if that repository gains an appropriate packet.

---

## Related-repository check

Fresh repository searches on 22-Sep-2026 for `US4296480A` and `MK4164` in `tmzncty/computing-archaeology` returned no dedicated packet to reuse.

Accordingly this file keeps only the retention-specific material:

- hidden maintenance-control state;
- physical sharing versus logical separation;
- maintenance progress versus full history;
- counter-coverage verification versus payload survival;
- patent-to-product evidence boundaries.

A future broader history of Mostek's 64K design organization, personnel, layout, manufacturing, or market deployment belongs in the companion repository.

---

## Source list

### Primary / contemporary

- Robert James Proebsting, **“Refresh counter test,”** Mostek Corporation, priority 15-May-1979; European publication `EP0019150A1`, 26-Nov-1980; US patent `US4347589A`, 31-Aug-1982. <https://patents.google.com/patent/EP0019150A1/en> ; <https://patents.google.com/patent/US4347589A/en>
- Sargent S. Eaton, Jr. and Paul R. Schroeder, **“Refresh counter,”** Mostek Corporation, filed 13-Aug-1979; `US4296480A`, published/granted 20-Oct-1981; British family A-publication `GB2056138A`, 11-Mar-1981. <https://patents.google.com/patent/US4296480A/en> ; <https://patents.google.com/patent/GB2056138A/en>
- Mostek, **1979 Memory Data Book and Designers Guide**, MK4164 product brief — already source-located in [`03-mostek-1979-1980-rfsh-dynamic-counter-deepening.md`](03-mostek-1979-1980-rfsh-dynamic-counter-deepening.md).
- Mostek, **1980 memory / product documentation**, MK4164 detailed refresh behavior — already source-located in the same prior deepening.

### Cross-case primary comparator

- Lionel S. White, Jr. and G. R. Mohan Rao, **“On-chip refresh for dynamic memory,”** Texas Instruments, filed 26-Jun-1978, `US4207618A`, 10-Jun-1980 — used only as a bounded functional/topology comparator; see [`03-ti-1978-onchip-refresh-counter-prior-art-topology-deepening.md`](03-ti-1978-onchip-refresh-counter-prior-art-topology-deepening.md).

---

## Bottom line

The strongest new result is not `we found the MK4164 schematic`. We did not.

It is narrower and more useful:

```text
1979 Mostek product evidence
    -> named MK4164 has on-chip refresh counter

1979 Mostek patent filings
    -> contemporary internal-counter test problem
    -> contemporary concrete low-area counter topology

but

same vendor + same period + matching function
    !=
verified product implementation identity
```

And the test patent adds a second retention lesson that the product manuals alone did not expose:

```text
payload appears retained
    !=
maintenance coverage has been verified

state being retained
    !=
state coordinating retention
    !=
evidence that the coordination is correct
```
