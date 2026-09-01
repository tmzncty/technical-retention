# Powered Flip-Flop Working Retention: Eccles–Jordan to ENIAC

## Scope

- **Object / system:** the Eccles–Jordan thermionic trigger/relay principle as a mechanism precursor, then the ENIAC flip-flop as a bounded computer working-state case.
- **Date range:** 1918–1946.
- **Primary question:** when does a very short-lived bistable machine state count as technical retention rather than merely an instantaneous electrical condition?
- **Why this case matters:** the repository's first category-coherence audit found no justified minimum duration for technical retention. A powered flip-flop is an adversarial test because its state may last only long enough to condition a later pulse or gate, yet the machine explicitly depends on that state continuing to count.

This is **not** a general history of bistable circuits, latches, registers, SRAM, or sequential logic. It also does not claim a direct conceptual genealogy from the 1918 patent to every later computer register.

---

## Related-repository check

Before opening this slice, code search in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated Eccles–Jordan / latch / flip-flop / register treatment to reuse. That repository still remains the preferred home for a broad engineering history of electronic state elements and semiconductor memory.

The contribution here is therefore deliberately narrow: use two primary anchors to stress-test the retention boundary, then stop.

---

## Historical vocabulary

### 1918 Eccles–Jordan patent

William Henry Eccles and Frank Wilfred Jordan filed British Patent GB148582A on 21 June 1918 under the title **“Improvements in ionic relays.”** The patent describes a thermionic relay/amplifying apparatus for telegraphic or telephonic work using valves connected with a return connection so that an amplified change is fed back to the first valve by `retroaction`.

The patent does **not** call the device a `flip-flop`, `bit`, `register`, or computer memory. Those are later descriptions and must not be projected backward as the inventors' problem formulation.

### 1946 ENIAC report

The U.S. Army / Moore School report uses machine-specific vocabulary directly relevant to retention:

- `flip-flop`;
- `normal` and `abnormal state`;
- `counter`;
- `accumulator`;
- `stores` / `stored`;
- `remembers`;
- `static communication`;
- `set`, `reset`, and `clear`.

This is unusually useful because the historical source itself says that a decade flip-flop **remembers** a pending carry and that an accumulator **stores** a number. The retention interpretation therefore does not have to depend only on modern metaphor.

---

## Historical record

### H/P — Eccles and Jordan established regenerative state persistence under power

GB148582A describes two three-electrode thermionic valves connected so that a change in the first valve changes the second, whose changed plate-circuit potential is returned to the first valve. Under the patent's unstable adjustment, the retroaction continues after the initiating stimulus until the first valve reaches one limiting current condition and the second reaches the opposite condition. Returning to the initial condition requires interruption of the valve interaction.

The historically safe claim is therefore:

> the 1918 patent documents a powered regenerative relay in which an initiating stimulus can drive the coupled circuit into a continuing limiting condition that is not merely identical to the duration of the stimulus.

It is **not** historically safe to rewrite this as “Eccles and Jordan invented a one-bit computer register” without qualification.

**Primary anchor:** W. H. Eccles and F. W. Jordan, British Patent GB148582A, filed 21 June 1918, published 5 August 1920, especially the abstract / description of Fig. 1 and the discussion of `retroaction` and restoration of the initial condition: <https://patents.google.com/patent/GB148582A/en>.

### H/P — ENIAC explicitly used flip-flops to remember working conditions

The 1 June 1946 *Report on the ENIAC*, Part I, Chapter IV, describes each accumulator as both a memory and arithmetic unit. Its numerical circuits contain decade ring counters and a decade flip-flop. The report states that each decade counter stores one digit and gives the decade flip-flop two roles, one of which is to remember whether carry-over must occur.

In the receive sequence, when a counter passes through stage 9, the decade flip-flop is set. During delayed carry-over, the report says that it continues to remember that a carry-over must take place while ordinary digit pulses continue to arrive. A later reset pulse both resets the flip-flop and participates in propagating the carry.

This supplies an unusually clear bounded retention sequence:

```text
state-setting event
    -> flip-flop enters abnormal state
    -> intervening pulse activity occurs
    -> later circuit behavior depends on that retained state
    -> reset terminates the retained condition
```

**Primary anchor:** *A Report on the ENIAC*, Part I, Chapter IV, §§4.0 and 4.3.2, especially the accumulator summary and delayed-carry discussion: <https://ftp.arl.army.mil/~mike/comphist/46eniac-report/chap4.html>.

### H/P — ENIAC could expose retained state statically without consuming it

Chapter IV §4.3.3 distinguishes `static communication` from the ordinary dynamic transmission of digit pulses. A receiving unit can be connected to the static outputs associated with accumulator counter flip-flops; the state of a flip-flop controls the corresponding selector tube in the receiving unit.

This matters because it supplies a historical counterexample to the idea that a retained working state must be retrieved through a separate destructive read operation. In this bounded ENIAC use, the state can remain present at an output relation and condition another circuit while still being the current state of the counter.

**Primary anchor:** *A Report on the ENIAC*, Part I, Chapter IV, §4.3.3, `Static Communication Between an Accumulator and Another ENIAC Unit`.

### H/P — Power-up state was not automatically admissible state

Part I, Chapter II states that when ENIAC was turned on, it was a matter of chance which flip-flops in numerical/program counters or program controls would come up in the abnormal state. A correct computation therefore required initial clearing to put numerical/program rings and program flip-flops into defined starting states.

The same section says that, with power still on, operators could stop a computation, erase stored accumulator/master-programmer data, clear, and begin again.

This is strong evidence for a distinction between:

- **having a bistable physical degree of freedom**;
- **having a system-admissible retained state**.

**Primary anchor:** *A Report on the ENIAC*, Part I, Chapter II, §2.1.2 `Initial Clearing`: <https://ftp.arl.army.mil/~mike/comphist/46eniac-report/chap2.html>.

### H/P — A flip-flop could retain a future procedural obligation

Chapter II §2.2.1 says the reader start flip-flop is set when a reader program is requested. It is later reset during the card-reading cycle, and can then be set again to remember that another reading is to take place.

The retained target here is not a decimal digit. It is a **pending control condition** whose later consequences depend on the flip-flop state.

That broadens the repository's working-state evidence without requiring a new philosophical category: a retained machine state may encode a value, a pending action, or an enabling condition for later logic.

---

## Retained state

The bounded physical target is a **which-stable-condition** distinction in a powered regenerative valve circuit.

In ENIAC, that circuit condition participates in machine-defined states such as:

- normal / abnormal flip-flop state;
- one selected stage of a counter;
- a pending carry-over condition;
- a reader/program control condition.

The important distinction is therefore:

```text
physical circuit condition
    !=
architectural / procedural meaning
```

The latter depends on where the flip-flop is used and on the surrounding gates, pulses, counters, and program wiring.

---

## Physical / logical substrate

In the Eccles–Jordan patent, coupled thermionic valves and their resistive return connections create regenerative interaction. In the bounded ENIAC case, vacuum-tube flip-flop circuits supply two operationally distinguished states used inside counters and controls.

This case is deliberately earlier than transistor latches and SRAM. It should not silently import CMOS static-power behavior, modern metastability analysis, edge-triggered D flip-flop semantics, or modern register-file architecture into the 1918/1946 mechanisms.

---

## Retention mechanism

The crucial mechanism is **regenerative bistability under operating power**.

A useful engineering reconstruction is:

1. a stimulus establishes one of the circuit's operating conditions;
2. feedback reinforces that condition;
3. while suitable power and circuit conditions remain, no periodic rewrite is required merely because time passes;
4. a later set/reset/clear event can deliberately force a different condition.

This is neither magnetic-core remanence nor DRAM refresh.

It introduces a distinct regime:

> **powered quiescent working retention** — a state can remain stable under power without a scheduled refresh operation that repeatedly reconstructs it.

`Powered quiescent working retention` is a local descriptive phrase in this case, not yet a controlled glossary term.

---

## Is continuous power “maintenance”?

The case forces a useful separation.

### E — continuous power is an enabling condition

The thermionic circuit requires its powered operating conditions for the regenerative state to exist. Removing those conditions destroys continuity of the working state.

### E — continuous power is not the same thing as periodic state maintenance

The primary evidence does not describe a DRAM-like deadline in which each flip-flop must be periodically read and rewritten merely to remain in its current state. Nor does it describe delay-line-style continuous circulation in which the logical pattern survives by repeatedly traversing a path.

Therefore:

> **continuous energy supply ≠ continuous state rewrite / refresh.**

This does not mean power is irrelevant to retention. It means `maintenance` must name the operation being performed rather than treating every ongoing prerequisite as the same kind of maintenance.

---

## Addressing and access geometry

A single flip-flop does not require an address in order to retain its state. Its state can be wired directly into later gates.

At the ENIAC accumulator level, decade counters and program controls impose architecture around the individual state elements. The report's static-communication section shows that particular counter-stage outputs can be wired to corresponding receiving tubes.

This strengthens an earlier repository finding:

> retention and addressability are separable.

It also adds a new boundary:

> later use of retained state need not require a discrete `retrieve` operation at all.

A downstream circuit may simply remain connected to an output that reflects the retained condition and act on that condition later.

---

## Read semantics

In the bounded ENIAC evidence, using a flip-flop output to control a gate or selector is not described as destroying the flip-flop state. Reset is a separate operation.

Thus this case supplies:

- **volatile** state;
- **nondestructive state use / observation** in the bounded circuit role;
- **no periodic refresh requirement established by the source**;
- explicit set/reset/clear semantics.

That combination is important because it blocks the shortcut:

```text
volatile
    = dynamic refresh
    = destructive read
```

The three are independent properties.

---

## Write and erasure semantics

For this bounded case:

- **set / flip** establishes the abnormal condition;
- **reset** returns the flip-flop to its normal condition;
- **clear** initializes or erases machine working state according to the surrounding ENIAC circuits;
- **power loss / power-up** does not preserve the previous logical working condition as an admissible continuation.

ENIAC's initial clear is especially useful because it shows that `physical state exists` is not enough. A system also needs a rule for which starting state is valid.

---

## Time

The case is a direct stress test of duration.

A pending carry may need to survive only from the pulse that sets a decade flip-flop to the later reset/carry phase. A reader-start condition may live only for part of a card-reading cycle. These are short-lived working states, not archives.

Yet the interval is not analytically empty. There is still:

```text
t0: a state is established

intervening activity occurs

t1: later behavior depends on whether the earlier state still holds
```

Therefore the repository currently has no evidence-based minimum duration below which retention automatically stops being meaningful.

The more useful test is functional and counterfactual:

> Would later machine behavior differ if the state failed to remain across the relevant interval?

In the ENIAC carry and control examples, yes.

---

## Maintenance and labor

The state element does not stand alone. Reliable working retention depends on:

- continuous electrical operating conditions;
- correctly biased and functioning valves/components;
- pulse and gate timing;
- reset/clear circuitry;
- operators and maintenance procedures that establish a known machine state after power-up or interruption.

But these dependencies should not be flattened into one phrase such as `the flip-flop is continuously refreshed`. The sources support powered circuit operation and explicit initialization/reset, not periodic state reconstruction analogous to DRAM.

---

## Failure / forgetting modes

This case adds several bounded forms of technical loss:

- loss of operating power, ending continuity of the working state;
- incorrect or indeterminate power-up state;
- failure to clear before computation;
- unintended set/reset from erroneous pulses or circuit faults;
- inability of a later gate/circuit to discriminate the intended state;
- component/power-supply failure that destroys stable operating conditions.

These are not equivalent to DRAM leakage, Flash logical invalidation, or RADOS stale-replica currentness failure.

---

## Engineering reconstruction

### E — short duration does not make retention trivial

The ENIAC carry flip-flop is useful precisely because a condition established earlier must remain available after intervening pulses and before a later reset/carry action. Its lifetime may be extremely short compared with disk or archival storage, but the temporal separation is operationally real.

### E — later admissibility does not require discrete retrieval

The category-coherence audit required a retention target, continuity across time, and later recovery/interpretation/admissibility. This case suggests one wording refinement:

> `later recovery` is too storage-interface-specific if read narrowly. The later event may instead be **state-sensitive use**, because the retained condition can remain continuously exposed at an output and simply condition what downstream circuitry does at `t1`.

The stronger cross-case relation should therefore allow:

```text
later recovery / interpretation / admissibility / state-sensitive use
```

rather than requiring a separate retrieval transaction.

### E — power and maintenance must be decomposed

The flip-flop needs an energy-supported operating regime, but that does not imply a scheduled maintenance operation that periodically recreates the logical state.

The comparison now needs at least:

```text
energy prerequisite
periodic reconstruction
access-triggered restoration
continuous circulation
```

as distinct axes.

### E — initialization is part of usable retention

Random/accidental power-up states are not valid continuations of a prior computation merely because each flip-flop physically occupies some state. ENIAC's initial clear establishes an admissible starting configuration.

This is a local machine-scale version of a broader repository result:

> physical presence ≠ authorized/current/admissible state.

---

## Philosophical / media-theoretical interpretation

### I — working retention is not a miniature archive

The value of this case is not to say that every flip-flop is a tiny archive. Its retained state can be entirely internal to an ongoing computation and may vanish at reset or power-off without any expectation of historical durability.

This supports keeping `technical retention` broader than Stieglerian tertiary retention and broader than archival preservation.

### I — microtemporality matters here, but does not define retention universally

The ENIAC example is highly compatible with Ernst's insistence on machine-specific timing: the difference between set, intervening pulse times, reset, and later gate action is the mechanism.

But the earlier Ernst test already blocks universalizing this regime. Flash reclamation and RADOS repair operate on different triggers and horizons, while core/Flash can remain quiescent without powered bistability.

---

## Functional analogies and limits

### A — flip-flop as the narrow electronic counterpart to a retained working position

There is a bounded functional comparison with the abacus case:

- a state established during an operation remains available to affect a later operation;
- the retained state is current working state, not automatically history;
- reset/clear removes the working condition.

But the mechanisms and historical concepts are radically different. An abacus bead is not genealogically a flip-flop, and a flip-flop is not merely an electronic bead.

### Limit — flip-flop ≠ register

A bistable element is a mechanism for retaining a state. A `register` is an architectural role/aggregation with selection, grouping, and use semantics. ENIAC's own vocabulary distinguishes individual flip-flops, ring counters, and accumulators.

This case therefore does not license the claim that every flip-flop is itself a register.

### Limit — not a transistor/SRAM history

Later transistor latches, static RAM cells, clocked flip-flops, and register files change implementation details, power behavior, fan-out, timing, and access organization. They need separate evidence rather than being treated as straightforward copies of the bounded thermionic case.

### Limit — Eccles–Jordan mechanism history remains incomplete

The patent is a strong primary anchor for the regenerative relay principle, but this first pass has not directly inspected the September 1919 *Electrician* paper / December 1919 *Radio Review* reprint or reconstructed the exact ENIAC flip-flop schematic from the original circuit drawings. Those are the next source-deepening steps before promotion to `grounded`.

---

## Cross-case result

The existing mechanism map can now distinguish:

```text
abacus
    passive positional working state

powered thermionic flip-flop / ENIAC
    powered regenerative working state
    no periodic state refresh established

magnetic core
    unpowered remanent state
    + access-triggered restore in the bounded classic case

DRAM
    powered decaying charge
    + deadline-driven regeneration

mapped Flash
    nonvolatile state
    + mapping/reclamation-mediated logical identity

RADOS
    replicated logical state
    + version/currentness/repair relations
```

The main new result is not another place on a storage hierarchy. It is a category correction:

> **technical retention can be nontrivial at very short timescales, and later continuity can be demonstrated by state-sensitive use rather than by a separate retrieval operation.**

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Eccles and Jordan filed GB148582A in 1918 for `Improvements in ionic relays` | H/P | patent metadata |
| The patent describes regenerative `retroaction` that can continue the coupled-valve condition after the initiating stimulus and requires interruption to restore the initial condition in the specified adjustment | H/P | patent abstract / Fig. 1 description |
| The patent itself is framed as relay/amplification for telegraphic or telephonic work, not as a computer register | H/P | patent abstract and historical vocabulary |
| The 1946 ENIAC report says a decade counter stores a digit and a decade flip-flop remembers whether carry-over must occur | H/P | Part I, Ch. IV §4.0 |
| During delayed carry, the decade flip-flop remains set across intervening digit pulses until a later reset/carry phase | H/P | Part I, Ch. IV §4.3.2 |
| ENIAC supports static use of accumulator counter-state outputs by other units | H/P | Part I, Ch. IV §4.3.3 |
| ENIAC power-up could leave flip-flops in accidental states, requiring initial clear before correct computation | H/P | Part I, Ch. II §2.1.2 |
| A reader-start flip-flop could remember a pending future read request | H/P | Part I, Ch. II §2.2.1 |
| Continuous power is an enabling condition but is not equivalent to periodic state refresh in this bounded implementation | E | mechanism comparison against DRAM/delay line |
| Very short-lived working state can still satisfy a nontrivial retention relation | E/I | bounded inference from delayed carry/control sequencing |
| Later retention must always involve a discrete retrieval operation | X | contradicted by bounded static/state-output use |
| `volatile = dynamic refresh = destructive read` | X | contradicted by this case plus grounded DRAM/core comparisons |
| Every flip-flop is historically or architecturally a register | X | unsupported; ENIAC vocabulary distinguishes elements and architectural units |

---

## Sources

### Primary

1. William Henry Eccles and Frank Wilfred Jordan, **“Improvements in ionic relays,”** British Patent GB148582A, filed 21 June 1918, published 5 August 1920. Google Patents transcription and bibliographic record: <https://patents.google.com/patent/GB148582A/en>.
2. **A Report on the ENIAC (Electronic Numerical Integrator and Computer)**, Report of Work Under Contract No. W-670-ORD-4926, Ordnance Department, U.S. Army / University of Pennsylvania, Moore School of Electrical Engineering, 1 June 1946. U.S. Army Research Laboratory transcription/index: <https://ftp.arl.army.mil/~mike/comphist/46eniac-report/>.
   - Part I, Chapter IV, §§4.0, 4.3.2, 4.3.3: accumulator, decade flip-flop, delayed carry, static communication: <https://ftp.arl.army.mil/~mike/comphist/46eniac-report/chap4.html>.
   - Part I, Chapter II, §§2.1.2 and 2.2.1: initial clearing, accidental power-up state, reader program flip-flops: <https://ftp.arl.army.mil/~mike/comphist/46eniac-report/chap2.html>.

### Next source-deepening targets

- W. H. Eccles and F. W. Jordan, **“A trigger relay utilizing three-electrode thermionic vacuum tubes,”** *The Electrician* 83 (19 September 1919), p. 298; reprinted in *The Radio Review* 1(3), December 1919, pp. 143–146 — inspect a page-preserving scan directly before using it as a central anchor.
- Original ENIAC circuit drawings / Part II circuit description for the specific flip-flop implementation — use to separate the report's functional description from a detailed circuit reconstruction.
- A period primary source that makes the architectural boundary between individual bistable elements and a `register` explicit, before expanding this case to the full `latch / flip-flop / register` bridge.
