# Coincident-Current Magnetic Core Half-Select Disturbance: State Margin, Partial-Select Output, and Inhibit Control

## Scope

- **Object / system:** early coincident-current ferrite-core memory arrays, treated as a bounded deepening of Case 02 rather than a second general history of magnetic core memory;
- **Date range:** 1951–1959 for the evidence used here, with the principal design work concentrated in 1951–1954 and one 1954-filed IBM patent published in 1959;
- **Principal sources:** Jay W. Forrester's 1951-filed multicoordinate-storage patent, William N. Papian's April 1952 IRE paper as preserved by MIT, and Edwin W. Bauer / Munro K. Haynes's 1954-filed IBM disturbance-cancellation patent;
- **Research question:** what must remain stable in the *non-target* cores and in the shared sensing path when one address is selected?

Case 02 already establishes remanent magnetic state, coincident-current selection, destructive read, and rewrite. The broader engineering history, including manufacturing and the systems logic of half selection, is already developed in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md). This case therefore isolates a narrower retention problem:

> **a core can be logically unselected while still being physically excited, and a retained bit can remain magnetically intact while the shared readout path is nevertheless disturbed.**

That distinction matters because it prevents `not selected`, `not switched`, `not physically affected`, and `not visible in the sense circuit` from collapsing into one claim.

---

## Historical vocabulary and source boundary

The period sources supply the relevant vocabulary directly.

Forrester's patent describes coordinate conductors whose separate excitation is sufficient to effect a **partial change of state**, while coincident excitation of the selected element exceeds the threshold required to move it between stable states. In another claim, below-threshold excitation is described as having substantially no effect **after being removed**.[^forrester]

Papian's 1952 paper makes the retention requirement explicit in its abstract: a usable coincident-current core must retain a large percentage of remanent flux of the proper polarity despite repeated **"nonselecting" disturbances**. The same abstract describes repetitive pulse-pattern tests that produce quantitative **"information-retention ratios"** and **"signal ratios."**[^papian]

Bauer and Haynes's IBM patent uses the vocabulary **"half selected cores," "disturbance signals," "inhibit pulse,"** and **"post-write-disturb pulse."** It states that partially excited cores can contribute outputs to a shared sense winding and that those contributions may make a stored one and zero difficult to distinguish.[^bauer]

These are not modern terms invented for this repository. The modern phrases `retention-control state`, `physical effect scope`, and `write authorization` below are engineering reconstructions and are labeled as such.

---

## Retained state and substrate

As in Case 02, the payload-bearing state is the direction of remanent magnetic flux in a ferrite core after the selecting currents are removed.

The new point is that this state lives in an array whose addressing mechanism intentionally exposes many non-target elements to some of the same electrical activity used to select the target.

In the classic two-coordinate scheme:

```text
selected X line
    → partial excitation of every core on that line

selected Y line
    → partial excitation of every core on that line

X ∩ Y
    → coincident excitation above the switching threshold
```

The selected core should cross the switching threshold. Cores that receive only one coordinate excitation should not end in the opposite stable remanent state.

Thus the array depends on more than `two stable states`. It depends on a usable separation between:

```text
subthreshold excursion
and
stable-state reversal
```

Forrester's claims make this separation part of the addressing apparatus itself.[^forrester]

---

## Half-selected does not mean untouched

A simplified logical account often says:

> one half-current does nothing; two half-currents switch the selected core.

That sentence is useful only if `does nothing` means **does not leave the core in the unintended opposite stable state**.

The primary evidence is more precise.

Forrester repeatedly describes one coordinate excitation as capable of producing a **partial change**, while requiring the coincident total to exceed the critical level for a stable-state transfer.[^forrester] Papian then makes repeated nonselecting disturbance a material-selection problem: the remanent state must retain adequate polarity/magnitude under those pulses.[^papian]

The engineering distinction is therefore:

```text
logical nonselection
≠
zero magnetic excursion
```

A core can be correctly nonselected in the logical sense while still traversing a minor part of its magnetic response during a neighboring access.

This also means that the physical effect scope of an access is larger than the logical target set.

---

## Two disturbance channels must remain separate

The historical sources expose at least two different meanings of `disturbance`.

### 1. Retained-state margin under repeated nonselecting excitation

Papian's concern is whether repeated nonselecting pulse patterns leave enough correct remanent flux for reliable storage. His abstract explicitly treats information retention under disturbance as a quantitative core-material criterion.[^papian]

This is a **retention-state** problem.

The non-target bit can fail if accumulated or poorly tolerated excitation moves its remanent condition far enough that the intended binary distinction is no longer reliable.

The present evidence does **not** establish a universal number of half-select pulses required to corrupt a bit, nor does it show that normal historical machines routinely suffered permanent half-select bit flips. It establishes that engineers treated resistance to repeated nonselecting disturbance as a design criterion.

### 2. Sense-line disturbance without stored-state corruption

The IBM Bauer/Haynes patent exposes a different failure surface. It explains that partially excited cores can produce voltage contributions in a shared output winding. Because real core hysteresis curves are not perfectly rectangular and cores are not identical, the summed disturbance may interfere with amplitude discrimination between the selected core's stored one and zero.[^bauer]

This can break **recoverability** even when the non-target cores remain in their intended stable states.

The patent's proposed cancellation circuitry develops an opposing voltage to reduce those half-select contributions. The intervention is in the readout path:

```text
half-selected core outputs
        +
selected-core output
        ↓
shared sense winding

cancellation network
        ↓
better one/zero discrimination
```

That is not the same operation as restoring a corrupted magnetic payload.

So:

> **state preservation ≠ zero sense-line contribution**

and:

> **sense disturbance ≠ stored-state corruption**

must remain separate.

---

## Addressing is partly a material-margin problem

Coincident-current selection is usually drawn as geometry:

```text
row + column = address
```

But geometry alone does not make the address safe.

The address works only if the coupled system preserves a separation between:

- the response of a fully selected core;
- the response of many half-selected cores;
- variation among core hysteresis characteristics;
- drive-current variation;
- sense threshold / amplifier recovery;
- outputs caused by inhibit or other maintenance pulses.

Forrester's threshold-based claims and Papian's retention/signal ratios show that the material response is part of the effective decoder.[^forrester][^papian] Bauer and Haynes show that even when the state-selection threshold succeeds, the shared sensing network still has to suppress or tolerate partial-select outputs.[^bauer]

Thus:

```text
address correctness
=
selection geometry
+
magnetic switching margin
+
sense discrimination margin
```

This equation is an engineering reconstruction, not period vocabulary.

---

## Shared sensing makes a local access electrically nonlocal

The IBM patent describes an output winding linked through many cores. When a selected X and Y coordinate are pulsed, half-selected cores along those coordinates can each contribute some voltage to the common sense path.[^bauer]

The logical operation is local:

```text
read this address
```

The electrical event is not:

```text
many cores respond weakly
+
one selected core may respond strongly
+
shared wiring sums what reaches the amplifier
```

The desired bit therefore remains recoverable only if the readout machinery can distinguish the selected event from the aggregate response of non-target elements.

This adds another retention relation beyond Case 02's destructive-read rewrite:

- **target retention obligation:** if the selected core is destructively read, reconstruct the old logical value when required;
- **neighbor retention obligation:** half-selected cores must preserve sufficient remanent margin under nonselecting pulses;
- **readout obligation:** the shared sense path must preserve enough signal discrimination to recover the selected value.

They are technically different obligations even though one memory cycle can exercise all three.

---

## Write semantics: word selection and bit authorization can differ

Bauer and Haynes also describe a three-coordinate arrangement in which the selected X/Y intersection determines a word line while a Z-plane **inhibit** pulse prevents selected word-line cores from changing state for particular bit positions.[^bauer]

In that bounded design:

```text
X/Y coincidence
    → selects a word line

without inhibit
    → a core on that word line may switch to the written state

with opposing inhibit
    → net magnetomotive force is reduced so that the core remains in the other state
```

This gives a useful distinction:

> **word selection ≠ bit write authorization**

A core can lie on the selected word line yet be intentionally prevented from changing.

The inhibit operation is also not an `erase` operation in the Flash sense. It is a control action that prevents a particular state transition during a write sequence.

---

## Maintenance, labor, and infrastructure

This case does not repeat the hand-threading and manufacturing history already covered in `computing-archaeology`.

For retention purposes, the important maintenance infrastructure is instead the chain of margins and compensations that makes the stored remanent distinction recoverable under ordinary array traffic:

- ferrite material with suitable hysteresis;
- controlled drive amplitudes;
- coordinate wiring geometry;
- sense-winding topology;
- sense amplification and timing;
- cancellation or balancing techniques where required;
- inhibit timing and amplifier recovery.

The IBM patent is especially useful because it shows that a disturbance problem can be attacked without changing the payload-bearing mechanism. One can preserve the same remanent storage scheme while changing the readout circuitry so that non-target responses are less consequential.[^bauer]

---

## Failure and technical forgetting modes

This bounded case distinguishes several failure modes that should not be called simply `the bit was disturbed`.

### Stable-state corruption

A non-target core no longer reliably retains the intended remanent state after repeated nonselecting excitation.

### Retention-margin degradation

The core still has the intended polarity, but the margin is degraded enough that later operation becomes less reliable.

The current sources establish the design concern but do not supply one universal quantitative failure threshold.

### Sense-discrimination failure

The target core may be in the correct state, yet aggregate disturbance on the sense path makes one and zero insufficiently distinguishable.

### Amplifier-recovery failure

The IBM patent also notes that inhibit or post-write-disturb pulses can drive amplifier capacitances strongly enough to require recovery time before a useful subsequent output can be amplified.[^bauer]

This is a **readout-path temporal failure**, not a magnetic payload decay process.

### Inhibit failure

A bit that should have been prevented from switching changes state during a word write.

### Destructive-read restore failure

The selected bit is read correctly but the required rewrite fails. This remains the Case-02 mechanism and must not be confused with neighbor half-select disturbance.

---

## Historical record

### Primary / contemporary evidence

1. **Jay W. Forrester, U.S. Patent 2,736,880, "Multicoordinate Digital Information Storage Device," filed May 11, 1951, issued February 28, 1956.** The claims explicitly describe coordinate excitations that can produce partial change, coincident excitation above the threshold for stable-state switching, and unselected elements held below that level.[^forrester]

2. **William N. Papian, "A Coincident-Current Magnetic Memory Cell for the Storage of Digital Information," _Proceedings of the I.R.E._ 40(4), April 1952.** MIT's Project Whirlwind record preserves the abstract, which explicitly requires retention of remanent flux despite repeated nonselecting disturbances and names `information-retention ratios` and `signal ratios` from repetitive pulse-pattern testing.[^papian]

3. **Edwin W. Bauer and Munro K. Haynes, U.S. Patent 2,889,540, "Magnetic Memory System with Disturbance Cancellation," filed July 14, 1954, issued June 2, 1959, assigned to IBM.** This is used as a 1954-filed design record with later publication: it documents half-selected-core output disturbance, shared sense-winding contributions, cancellation, inhibit pulses, and post-write-disturb effects.[^bauer]

### Reused engineering history

4. [`computing-archaeology: Why Was Magnetic-Core Memory Worth Weaving by Hand?`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md) already explains coincident-current selection, half selection, destructive read, manufacturing labor, and the system-level trade. This case does not reproduce that history.

---

## Engineering reconstruction

### Finding 1 — retention can mean immunity to ordinary neighboring traffic

Quiescent nonvolatility answers:

> will the core keep a remanent state when left alone?

The half-select problem asks something else:

> will the core keep a usable state while the array is actively addressing other locations?

A memory technology can therefore have excellent idle retention while still requiring an engineered **disturbance margin** for ordinary operation.

### Finding 2 — physical nonlocality can hide behind logical locality

One address names one target, but shared coordinate wires physically excite many cores.

`target address` therefore does not define the complete physical effect scope of the operation.

### Finding 3 — recoverability can fail without payload corruption

The IBM disturbance-cancellation problem shows that the physical bit can remain correct while the sense circuit cannot reliably classify it.

Thus technical retention must distinguish:

```text
state survives
from
state is recoverable through the current read path
```

### Finding 4 — cancellation is not restoration

A cancellation transformer or balanced sense geometry can remove an unwanted electrical contribution from the readout path.

It does not thereby rewrite a degraded remanent bit.

### Finding 5 — selection can be nested

In the bounded IBM arrangement, X/Y chooses the word while Z inhibit decides whether a given bit is allowed to switch.

The project should therefore avoid treating `selected` as one indivisible relation when the hardware itself separates location selection from transition authorization.

---

## Functional analogies

A limited analogy to later disturbance mechanisms is useful:

- Case 53 RowHammer: repeated activation of aggressor rows can endanger physical neighbors;
- Case 52 NAND read disturb: repeated reads can stress non-target cells;
- Case 59 NAND program interference: programming one cell/page can shift neighboring retained states.

The shared functional pattern is:

> **an operation aimed at one logical target can impose a retention burden on other retained states.**

The analogy stops there.

Magnetic-core half-select disturbance involves ferrite hysteresis, shared coordinate currents, and sense-winding behavior. RowHammer involves DRAM cell coupling/disturbance under repeated activation. NAND disturb/interference involves pass-voltage or capacitive/charge effects. No technical genealogy or mechanism identity is claimed.

---

## Philosophical / media-theoretical interpretation — bounded

This case supports one narrow project-level interpretation:

> **technical persistence is often selective immunity rather than isolation.**

The retained bit does not survive because the rest of the machine leaves it untouched. It survives because the array is designed so that ordinary non-target traffic may act on it **without crossing the boundary that changes what counts as its stored state**, while the readout path suppresses effects that would otherwise make the state unavailable.

This is not a historical claim that Forrester, Papian, Bauer, or Haynes formulated a philosophy of retention. It is a later interpretation disciplined by their engineering evidence.

It also limits a common intuition about `storage`: the past state may remain available not by being sealed away from present operations, but by being engineered to tolerate and discriminate among them.

---

## Counterexamples and limits

### Half-select disturbance is not identical to permanent bit corruption

The IBM patent is centrally about sense disturbance from partially excited cores. Its evidence must not be rewritten as proof that all half-selected cores undergo permanent state corruption.

### The current evidence does not establish one universal half-select failure threshold

Core materials, geometry, pulse amplitude, temperature, winding organization, and sense circuitry varied. Papian establishes that repetitive nonselecting disturbance was measured and materially discriminating; this case does not infer one universal pulse count or margin.

### The IBM cancellation circuit is not claimed as universal production practice

The 1954-filed patent proves an engineering problem and a proposed/claimed solution in period vocabulary. This case does not claim that every IBM or non-IBM core-memory product used the exact circuit shown.

### This is not a new invention-priority claim

The early history of magnetic memory includes parallel and contested work. This case makes no claim that the sources used here settle the invention of magnetic core memory, coincident-current selection, destructive read, inhibit writing, or disturbance cancellation.

### Full-core history belongs elsewhere

Manufacturing, economics, Whirlwind chronology, and the broader reason core displaced earlier memories remain in `computing-archaeology`. This file exists only because the retention-specific split among neighbor state, sense output, and write authorization changes the cross-case comparison.

---

## Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| Separate coordinate excitation can produce partial response while coincidence drives selected stable-state switching | H/P | direct in Forrester patent claims |
| Repeated nonselecting disturbance was treated as an information-retention criterion | H/P | direct in Papian 1952 abstract preserved by MIT |
| Half-selected cores can contribute disturbance voltage to a shared sense winding | H/P | direct in Bauer/Haynes patent |
| Sense cancellation addresses readout disturbance rather than restoring payload state | E | reconstruction from IBM circuit purpose and operation |
| Logical nonselection does not imply zero physical excitation | E | reconstruction from Forrester/Papian mechanisms |
| A target address does not define the complete physical effect scope | E | reconstruction from shared X/Y coordinate geometry |
| Word selection can differ from bit-level permission to switch in the bounded inhibit scheme | H/P + E | IBM patent description |
| Core half-select disturbance is functionally comparable to RowHammer/NAND neighbor stress | A | bounded analogy only |
| Core half-select disturbance is the ancestor of RowHammer or NAND disturb | X | unsupported and rejected |
| Every historical core-memory product used the IBM cancellation circuit | X | unsupported and rejected |

---

## Related repositories

- [`tmzncty/computing-archaeology/docs/memory/why-core-memory-was-worth-weaving.md`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md) — the reusable engineering/history account; this case adds the retention-specific state-disturbance / sense-disturbance split.
- [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) — relevant to the priority and vocabulary caution: modern `retention burden` is not projected backward as the historical actors' own general problem category.

---

## Sources

[^forrester]: Jay W. Forrester, **"Multicoordinate Digital Information Storage Device,"** U.S. Patent 2,736,880, application filed May 11, 1951, issued February 28, 1956. Google Patents HTML transcription: https://patents.google.com/patent/US2736880A/en

[^papian]: William N. Papian, **"A Coincident-Current Magnetic Memory Cell for the Storage of Digital Information,"** _Proceedings of the I.R.E._ 40(4), April 1952. MIT Libraries / Project Whirlwind record and abstract: https://dome.mit.edu/handle/1721.3/40248

[^bauer]: Edwin W. Bauer and Munro K. Haynes, **"Magnetic Memory System with Disturbance Cancellation,"** U.S. Patent 2,889,540, application filed July 14, 1954, issued June 2, 1959, International Business Machines Corporation. Google Patents HTML transcription: https://patents.google.com/patent/US2889540A/en

---

## Evidence status

**Status: `grounded`.**

The central bounded claims are supported by three contemporary primary-source lines with different roles:

- Forrester: threshold / partial-select coordinate logic;
- Papian: retention under repetitive nonselecting disturbance;
- Bauer/Haynes: half-select sense disturbance, cancellation, and inhibit/readout effects.

The case is deliberately narrower than Case 02 and the `computing-archaeology` core-memory history. Remaining work is archival deepening: direct line-by-line facsimile inspection of the full Papian article and additional named-machine quantitative margin measurements if later synthesis requires exact pulse/amplitude numbers.
