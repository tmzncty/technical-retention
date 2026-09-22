# Case 02 deepening — Victor 1974–1975 core-memory power-fail gating versus in-flight restore

**Case:** [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md)  
**Case status:** `grounded`  
**This record:** `bounded evidence deepening` — no maturity promotion  
**Primary historical anchor:** U.S. Patent 3,906,453, filed 27 March 1974, published 16 September 1975, Victor Comptometer Corporation  
**Question:** when a destructively read core memory has separate read and restore/write phases, what does a documented power-fail gate prove about an access already in flight?

---

## Why this slice

Case 02 already establishes the classic relation:

```text
remanent magnetic state
    ↓
destructive read / sense
    ↓
old logical value becomes observable
    ↓
restore / rewrite
    ↓
remanent state is re-established
```

It also already separates unpowered remanence from whole-machine restart, power-transition sequencing, and diagnostic validation.

A narrower boundary remained easy to blur:

> If a machine inhibits new memory commands after a power-fail indication, does that by itself prove that a destructive read which had already begun will complete its restore phase before memory power becomes unusable?

The Victor source is unusually useful because one document places three facts next to one another:

1. the magnetic-core RAM is explicitly nonvolatile;
2. its memory cycle is split into sequential read and write/restore portions;
3. a `memory fail` signal is used for orderly start-up/shut-down and suppresses further command acceptance/output under abnormal supply conditions.

The source therefore supports a strong **boundary claim** even though it does not close the underlying in-flight timing question.

---

## Source identity and custody

### A — period primary technical/legal record

**U.S. Patent 3,906,453**, Victor Comptometer Corporation.

The indexed metadata gives:

- filing date: **1974-03-27**;
- publication date: **1975-09-16**;
- assignee: **Victor Comptometer Corporation**;
- subject: a core-memory control circuit that allows sequentially read/written magnetic-core RAM to substitute for a semiconductor RAM interface designed around different bus timing.

The searchable patent text is available through:

- Google Patents identifier: <https://patents.google.com/patent/US3906453A/en>
- FreePatentsOnline transcription: <https://www.freepatentsonline.com/3906453.html>

The indexed title is inconsistently OCRed in public databases (`Care memory control circuit` appears in some indexes), while the patent abstract and body repeatedly describe a **core memory control circuit**. This record therefore refers to the patent primarily by number rather than treating the OCR title as historical vocabulary.

### Source-use boundary

A patent is primary evidence for what the document specifies and claims. It is not, by itself, proof of:

- shipment volume;
- fleet-wide field behavior;
- every implementation sold by Victor;
- invention priority over all earlier power-fail/core-memory work;
- or the exact analog behavior of a particular installed power supply during collapse.

The value of the source here is the explicit organization of a named control design.

---

## Historical record

### H/P — the magnetic-core RAM has a two-part sequential cycle

The patent describes a known nonvolatile magnetic-core RAM whose repetitive memory cycle has a first and a second part.

In the first part:

- output data are retrieved;
- the selected core is read;
- the design is explicitly described as destructively read.

In the second part:

- writing occurs;
- or, when preservation of the prior value is required, the destructively read data are restored.

The detailed description says that reading occurs in the first part of each cycle and that writing **or restoration of destructively read data** occurs in the second part.

This is not a retrospective model imposed on the machine. The sequential phase distinction is explicit in the period document.

A bounded state sketch is therefore historically warranted:

```text
phase 0: selected core holds remanent state

phase 1: read currents select the core
         ↓
         possible magnetic reversal produces sense output

phase 2: write / restore currents act
         ↓
         selected core is placed in the intended post-cycle state
```

The patent further describes the data-latch and timing circuitry that holds information for the second portion of the cycle.

### H/P — the read result becomes available before the restore/write portion is complete

The patent's timing discussion separates:

- the core access interval and `DATA OUT` behavior in the first part;
- the later input-data stabilization and write/restore behavior in the second part.

That matters because it prevents a misleading shorthand:

```text
host received / latched a read result
    =
core restoration already complete
```

The period design itself treats these as different phases.

### H/P — a `memory fail` signal participates in orderly start-up and shut-down

The preferred embodiment connects the magnetic-core RAM to a `memory fail` signal from the CPU.

The patent says this signal is used to effect orderly start-up and shut-down when core power is applied or removed, and that abnormal supply conditions prevent further acceptance of commands and output of data.

This is strong evidence for a **power-boundary admission gate**:

```text
abnormal power detected
    ↓
memory-fail condition
    ↓
new command acceptance / output is suppressed
```

The source therefore does more than say that ferrite is nonvolatile. It documents surrounding control logic that treats power transition as a state requiring different admission behavior.

### H/P — the patent does not state an in-flight restore-completion guarantee

The same source does **not** establish, in the passages inspected for this slice:

- the exact voltage threshold at which `memory fail` is asserted;
- how much usable rail energy remains at that instant;
- whether a read already in its first half is allowed to finish its second-half restore;
- whether the controller aborts a partly started cycle;
- whether analog hold-up guarantees completion of the current cycle;
- whether a particular power-fail phase can leave a selected core in an unintended post-read state;
- or a fault-injection result demonstrating every possible phase of supply loss.

That absence is the central result of this packet.

The patent proves **admission shutdown**. It does not, from the inspected text alone, prove **in-flight restore atomicity**.

---

## Engineering reconstruction

Everything in this section is a project reconstruction from the period source, not period Victor terminology unless explicitly marked otherwise.

### E — destructive read creates a temporary restore obligation

Once a destructive read has sensed the old value, preserving that logical value requires the later restore/write portion to complete successfully.

A useful state model is:

```text
S0  stable remanent representation
    ↓ destructive sense/read begins
S1  old value has been observed or latched;
    selected magnetic state may have been forced toward read reference state
    ↓ restore/write phase completes
S2  intended remanent representation established again
```

Between `S1` and `S2`, the system carries a **restore obligation**.

This does not mean the controller is necessarily unsafe in that interval. It means safety through that interval requires some additional relation — sufficient hold-up, cycle-completion logic, rollback/recovery, redundancy, or another mechanism — beyond the bare fact of magnetic remanence.

### E — command admission and in-flight completion are different predicates

The key separation is:

```text
new command rejected after power-fail indication
    !=
current destructive-read cycle proven restored
```

A controller can correctly stop *new* work while still needing a separate answer for work already admitted.

This distinction appears throughout later storage systems under many different mechanisms. Here it is grounded only as an engineering boundary around the Victor source; no claim is made that Victor used modern transaction vocabulary.

### E — output availability and media closure are different predicates

Because the source separates first-part read/output from second-part write/restore, another relation follows:

```text
read result available to surrounding logic
    !=
physical representation closed back into a stable intended state
```

This is a useful retention distinction. A system can know what the old bit was while still owing work to make that bit safely retained again.

### E — nonvolatile-at-rest is weaker than power-loss-safe-at-every-microphase

For classic destructive-read core:

```text
power removed while core is quiescent in a stable state
    ≠
power removed during an arbitrary access phase
```

Therefore:

```text
nonvolatile at rest
    !=
crash-safe throughout every destructive-read microphase
```

The left-hand property concerns remanence of an already-established state. The right-hand property concerns the protocol that temporarily disturbs and reconstructs that state.

### E — power-fail protection must be located relative to the access pipeline

A stronger future implementation proof would need at least:

```text
power-fail detection threshold
+ detection latency
+ access phase at detection
+ remaining usable rail / hold-up time
+ current-cycle policy
+ restore completion indication
+ post-transition validation
```

Without those relations, `memory fail exists` is insufficient to infer current-cycle closure.

---

## Functional analogy — later destructive-read NVM makes the abstract hazard explicit

This section is deliberately **not genealogy**.

### A/H/P* — Texas Instruments destructive-read NVM, 2015-priority family

Texas Instruments' patent family titled **“Methods and apparatus to detect and correct errors in destructive read non-volatile memory”** claims priority from **2015-11-20**; one U.S. application was published as `US20190004897A1` on **2019-01-03**, and the divisional grant `US11016842B2` issued **2021-05-25**.

The family explicitly states that some nonvolatile memories require a value read destructively to be written back, and that unexpected power loss during read or write-back can leave the original value malformed or unavailable.

Its claimed power-control relation is especially useful as a modern comparison:

- commanded power-off removes power only after pending read-restore work is complete;
- status state distinguishes normal commanded shutdown from an abnormal power-varying event;
- recovery can run error correction after an abnormal event.

Primary source:

- <https://patents.google.com/patent/US11016842B2/en>
- related publication: <https://patents.google.com/patent/US20190004897A1/en>

### Why the analogy is useful

The later TI design gives an explicit nameable answer to the abstract relation left unclosed in the Victor source:

```text
power-off requested
    ↓
wait for pending read-restore closure
    ↓
record clean shutdown state
    ↓
remove power
```

And, for abnormal loss:

```text
unexpected power variation during read/write-back
    ↓
clean closure not guaranteed
    ↓
recovery evidence / correction is needed
```

This helps identify what evidence would be required to strengthen the 1974–1975 historical case.

### Stop condition — no genealogy claim

The TI patent is **not** evidence that:

- Victor anticipated this exact controller structure;
- TI descended from Victor's design;
- magnetic core and the later DRNVM share a physical mechanism;
- the modern patent establishes historical priority for the generic read/restore problem;
- or Victor's system actually corrupted data in the same way during power failure.

The comparison is relation-level only:

```text
destructive observation
+ deferred restoration
+ asynchronous power boundary
```

---

## Cross-case comparison — Case 02 versus Case 86

Case 86 documents a different layer of the same broad power-boundary problem.

The PDP-8 KR01 path gives software approximately one millisecond after a power-low interrupt to move active CPU state into known core-memory locations, then later enters a restore routine after power becomes satisfactory.

That relation is:

```text
volatile execution/control state
    ↓ emergency save
core-resident state
    ↓ later software restore
reconstructed execution state
```

The Victor slice here is narrower and lower-level:

```text
core bit in stable remanent state
    ↓ destructive read
restore obligation
    ↓ second cycle portion
stable remanent state again
```

The two must not be collapsed.

Case 86 shows why **whole-machine continuation** needs state migration and restart logic even when core payload survives.

This packet shows why **one core access** can itself contain a temporary retention obligation even though the medium is nonvolatile at rest.

Together they give two nested seams:

```text
cell / word seam:
read completion != restore completion

machine seam:
main-memory survival != execution-state continuation
```

The later PDP-8/E KP8-E evidence in Case 86 explicitly documents power-supply filter capacitors that preserve enough operating time for the emergency save path. That later named implementation must not be projected backward onto Victor's 1974 filing or onto the 1966 KR01 implementation.

---

## Historical record / engineering reconstruction / analogy / philosophy ledger

| Statement | Class | Support |
| --- | --- | --- |
| US 3,906,453 was filed 1974-03-27 and published 1975-09-16 for Victor Comptometer Corp. | `H/P` | patent metadata |
| the described core RAM has sequential first-part read and second-part write/restore behavior | `H/P` | patent body |
| the described core RAM is destructively read | `H/P` | patent body |
| `memory fail` is used for orderly power transition behavior and suppresses further command acceptance/output under abnormal supply conditions | `H/P` | patent body |
| the inspected patent text guarantees an already-started destructive-read restore before power becomes unusable | `X` | not established |
| the inspected patent text gives rail hold-up duration or phase-specific fault-injection results | `X` | not established |
| destructive read creates a temporary restore obligation if logical continuity is required | `E` | reconstruction from the two-part cycle |
| new-work admission gating and in-flight completion are distinct safety predicates | `E` | reconstruction |
| read-result availability and restored-media closure are distinct predicates | `E` | reconstruction |
| TI's later DRNVM family explicitly guards commanded power-off against pending read-restore and handles abnormal loss separately | `H/P*` | later primary patent; not Victor history |
| TI and Victor share a direct technical lineage | `X` | not established |
| observation can create temporary maintenance debt in an otherwise stable medium | `P` | bounded interpretation, not period vocabulary |

---

## Philosophical interpretation

The case supplies a narrow technical basis for one interpretive claim:

> a medium can be stable while unattended yet temporarily become dependent on active reconstruction precisely because it is being observed.

That is more precise than saying simply that “reading destroys memory.”

The retained relation passes through different states:

```text
stable but unread
    → observed and temporarily owed restoration
    → stable again
```

The important conceptual object is therefore not only the magnetic token but the **closure of the read–restore relation**.

This remains a philosophical interpretation. Victor's patent does not use the vocabulary of `maintenance debt`, `closure`, `transaction`, or `commit`.

---

## Explicit non-claims

This packet does **not** claim that:

1. every magnetic-core memory had the same two-phase controller;
2. every destructive-read core system was vulnerable to data loss on every power failure;
3. Victor's system lacked adequate analog hold-up or current-cycle completion logic;
4. Victor's system guaranteed current-cycle completion;
5. assertion of `memory fail` occurred at a particular point inside the 5-microsecond processor timing cycle;
6. a sensed value had necessarily already been consumed by the CPU when a hypothetical restore failure occurred;
7. the patent establishes field failure frequency;
8. Victor invented destructive-read restore, power-fail gating, or core-memory nonvolatility;
9. the 2015-priority TI family is genealogically descended from this Victor design;
10. the PDP-8 KR01/KP8-E implementation details apply to Victor hardware;
11. `nonvolatile` means safe under arbitrary brownout waveforms;
12. suppressing new commands is sufficient evidence of crash consistency.

---

## What this closes

Before this deepening, Case 02 already had evidence for:

- remanent idle retention;
- destructive read and regeneration;
- controlled power-transition retention;
- machine-level power-cycle diagnostics;
- whole-machine restart as a separate problem in Case 86.

This packet closes a narrower conceptual ambiguity:

```text
power-fail command gating
    !=
proof of in-flight destructive-read restore completion
```

It also adds a named 1974–1975 controller witness in which the read/restore phase split and a power-fail admission mechanism appear in the same source.

---

## What remains open

The next useful work is no longer another generic statement that “core is nonvolatile.” It is implementation evidence that resolves the in-flight boundary.

Priority open debts:

1. a production core-memory controller manual explicitly saying whether the **current cycle completes** after power-fail detection;
2. a schematic/manual giving the power-fail threshold relative to memory-current regulators and cycle timing;
3. measured or specified **hold-up time** for the core-memory read/restore circuitry;
4. a maintenance diagnostic or fault-injection procedure that interrupts power at controlled points inside a destructive-read cycle;
5. post-failure evidence that distinguishes `read result captured` from `core restored`;
6. a named machine showing an alternative strategy, such as cycle inhibition before destructive sense or guaranteed current-cycle drain;
7. revision-specific Victor service documentation, if surviving, that connects US 3,906,453 to shipped hardware and its power supply.

These are stronger targets than accumulating additional general descriptions of destructive read.

---

## Related repository routing

The broad history of magnetic-core engineering, weaving, selection geometry, and manufacturing labor remains in:

- [`tmzncty/computing-archaeology/docs/memory/why-core-memory-was-worth-weaving.md`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md)

This packet does not duplicate that history. It keeps only the retention-specific seam among destructive observation, restore, and asynchronous loss of power.

Related Technical Retention cases:

- [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md) — base magnetic-core case;
- [`../cases/86-dec-pdp8-core-power-fail-auto-restart.md`](../cases/86-dec-pdp8-core-power-fail-auto-restart.md) — core-resident emergency state save and restart;
- [`03-dram-refresh-evidence-index.md`](03-dram-refresh-evidence-index.md), where available, for a different destructive-sense / restoration regime whose volatility and refresh mechanism must not be equated with core;
- [`synthesis26-reset-event-state-persistence-horizon-deepening.md`](synthesis26-reset-event-state-persistence-horizon-deepening.md) for the broader rule that event type, state class, and survival semantics must be typed rather than reduced to one scalar `survives reset` claim.

---

## Source notes

### Victor U.S. Patent 3,906,453

Primary period patent record. The searchable transcription establishes the two-part core-memory cycle, destructive read, second-part write/restoration, and the `memory fail` connection used for orderly start-up/shut-down and command/output suppression under abnormal supply conditions.

Metadata cross-checks in patent indexes give the filing/publication dates and Victor Comptometer Corporation assignee. This packet deliberately does not infer missing rail-hold-up or current-cycle semantics from the presence of the fail signal.

Links:

- <https://patents.google.com/patent/US3906453A/en>
- <https://www.freepatentsonline.com/3906453.html>

### Texas Instruments US 11,016,842 / US 2019/0004897

Primary later patent family, priority 20 November 2015. It is used only as a functional-analogy witness because it expressly treats destructive-read/write-back work as something that can be interrupted by power variation and makes pending read-restore completion a condition for commanded power removal.

Links:

- <https://patents.google.com/patent/US11016842B2/en>
- <https://patents.google.com/patent/US20190004897A1/en>

### Internal cross-case evidence

Case 86's DEC documentation is independently grounded and should remain the source for PDP-8 power-fail save/restart details. Its later KP8-E capacitor hold-up evidence is a separate named implementation and is not imported into Victor's design.

---

## Result

**Status after this slice:** Case 02 remains `grounded`; no promotion.

The new bounded result is:

```text
nonvolatile remanent medium
    + destructive two-part access
    + power-fail admission gating

still does not, by itself, prove

in-flight read/restore closure under arbitrary power loss
```

That boundary is now explicit enough to guide the next archival search rather than being hidden inside the generic statement that core memory is nonvolatile.
