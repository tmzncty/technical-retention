# Powered Flip-Flop Working Retention: Eccles–Jordan to ENIAC

## Scope

- **Status:** `grounded` — promotion record: [`evidence/06-burks-1947-eniac-flip-flop-grounding.md`](../evidence/06-burks-1947-eniac-flip-flop-grounding.md).
- **Object / system:** the Eccles–Jordan thermionic trigger/relay principle as a mechanism precursor, then the ENIAC flip-flop as a bounded computer working-state case; a 1954 Whirlwind report is used only as a later period witness for the architectural `register` boundary.
- **Date range:** 1918–1947 for the core mechanism/evidence sequence, with a bounded 1954 terminology/architecture comparison.
- **Primary question:** when does a very short-lived bistable machine state count as technical retention rather than merely an instantaneous electrical condition?
- **Why this case matters:** the repository's first category-coherence audit found no justified minimum duration for technical retention. A powered flip-flop is an adversarial test because its state may last only long enough to condition a later pulse or gate, yet the machine explicitly depends on that state continuing to count.

This is **not** a general history of bistable circuits, latches, registers, SRAM, or sequential logic. It also does not claim a direct conceptual genealogy from the 1918 patent to every later computer register.

---

## Related-repository check

Fresh code searches in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated Eccles–Jordan / ENIAC / latch / flip-flop / register treatment to reuse. That repository remains the preferred home for a broad engineering history of electronic state elements and semiconductor memory.

The contribution here is deliberately narrow: use period primary anchors to stress-test the retention boundary, then stop.

---

## Historical vocabulary

### 1918–1919 Eccles–Jordan sources

William Henry Eccles and Frank Wilfred Jordan filed British Patent GB148582A on 21 June 1918 under the title **“Improvements in ionic relays.”** The patent describes a thermionic relay/amplifying apparatus for telegraphic or telephonic work using valves connected with a return connection so that an amplified change is fed back to the first valve by `retroaction`.

The British Association's published proceedings for the 1919 Bournemouth meeting records their **“A Trigger Relay utilising Three Electrode Thermionic Vacuum Tubes”** and uses period vocabulary including `trigger relay`, resistance coupling, back coupling, electrical stimulus, and `no restoring influence`.

Neither source calls the mechanism a `bit`, `register`, or computer memory. Those later terms must not be projected backward as the inventors' problem formulation.

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

This is unusually useful because the historical source itself says that a decade flip-flop **remembers** a pending carry and that an accumulator **stores** a number. The retention interpretation therefore does not depend only on modern metaphor.

### 1947 Burks paper

Arthur W. Burks's **“Electronic Computing Circuits of the ENIAC”**, _Proceedings of the I.R.E._ 35(8), August 1947, pp. 756–767, provides the strongest bounded circuit-level anchor used in this case. On p. 757 Burks explicitly classifies the flip-flop among ENIAC's remembering circuits. On p. 758 he prints a simplified accumulator program-control circuit and separates steady-state stability from flipping/triggering dynamics. On p. 759 he gives microsecond-scale set and recovery margins.

This paper is a period primary source by an ENIAC engineer, not a later textbook reconstruction.

### 1954 Whirlwind report — bounded `register` boundary witness

M. F. Mann, R. R. Rathbone, and J. B. Bennett's MIT Project Whirlwind Report R-221, *Whirlwind I Operation Logic* (1 May 1954), calls the A-register (`AR`) a **`simple flip-flop register`** while defining AR through machine-level functions: receiving from storage, transmitting to the accumulator, holding operands, and participating in sign-related operations.

The same report also uses `storage register` language for magnetic-core storage. Period `register` vocabulary is therefore neither identical to one elementary flip-flop nor safely reducible to today's narrow CPU-register category.

Source-control notes are recorded in [`evidence/06-flip-flop-register-boundary-addendum.md`](../evidence/06-flip-flop-register-boundary-addendum.md).

---

## Historical record

### H/P — Eccles and Jordan established a regenerative trigger mechanism under power

GB148582A describes two three-electrode thermionic valves connected so that a change in the first valve changes the second, whose changed plate-circuit potential is returned to the first valve. Under the patent's specified adjustment, the retroaction continues after the initiating stimulus until the first valve reaches one limiting current condition and the second reaches the opposite condition. Returning to the initial condition requires interruption of the valve interaction.

The 1919 British Association proceedings independently describe a resistance-coupled cascade with back coupling from the last valve to the first, initiated by an electrical stimulus and followed by mutually reinforcing changes with `no restoring influence`.

The historically safe claim is therefore:

> the contemporary Eccles–Jordan sources document a powered regenerative trigger/relay in which a stimulus can initiate a continuing circuit condition that is not merely identical to the duration of the stimulus.

It is **not** historically safe to rewrite this as “Eccles and Jordan invented a one-bit computer register.”

**Primary anchors:** W. H. Eccles and F. W. Jordan, British Patent GB148582A, filed 21 June 1918, published 5 August 1920: <https://patents.google.com/patent/GB148582A/en>; British Association 1919 proceedings, Transactions of Section G, pp. 271–272: <https://archive.org/details/reportofbritisha20adva>.

### H/P — ENIAC explicitly used flip-flops to remember working conditions

The 1 June 1946 *Report on the ENIAC*, Part I, Chapter IV, describes each accumulator as both a memory and arithmetic unit. Its numerical circuits contain decade ring counters and a decade flip-flop. The report states that each decade counter stores one digit and gives the decade flip-flop two roles, one of which is to remember whether carry-over must occur.

In the receive sequence, when a counter passes through stage 9, the decade flip-flop is set. During delayed carry-over, it continues to remember that a carry-over must take place while ordinary digit pulses continue to arrive. A later reset pulse both resets the flip-flop and participates in propagating the carry.

```text
state-setting event
    -> flip-flop enters abnormal state
    -> intervening pulse activity occurs
    -> later circuit behavior depends on that retained state
    -> reset terminates the retained condition
```

**Primary anchor:** *A Report on the ENIAC*, Part I, Chapter IV, §§4.0 and 4.3.2: <https://ftp.arl.army.mil/~mike/comphist/46eniac-report/chap4.html>.

### H/P — ENIAC could expose retained state statically without consuming it

Chapter IV §4.3.3 distinguishes `static communication` from ordinary dynamic transmission of digit pulses. A receiving unit can be connected to static outputs associated with accumulator counter flip-flops; the state of a flip-flop controls the corresponding selector tube in the receiving unit.

This supplies a historical counterexample to the idea that retained working state must be recovered through a separate destructive read transaction. In this bounded use, state can remain present at an output relation and condition another circuit while still being the current counter state.

### H/P — Power-up state was not automatically admissible state

Part I, Chapter II states that when ENIAC was turned on, it was a matter of chance which flip-flops in numerical/program counters or program controls would come up in the abnormal state. Correct computation required initial clearing to put numerical/program rings and program flip-flops into defined starting states.

This establishes a distinction between:

- **having a bistable physical degree of freedom**;
- **having a system-admissible retained state**.

**Primary anchor:** *A Report on the ENIAC*, Part I, Chapter II, §2.1.2: <https://ftp.arl.army.mil/~mike/comphist/46eniac-report/chap2.html>.

### H/P — A flip-flop could retain a future procedural obligation

Chapter II §2.2.1 says the reader start flip-flop is set when a reader program is requested. It is later reset during the card-reading cycle and can then be set again to remember that another reading is to take place.

The retained target here is not a decimal digit. It is a **pending control condition** whose later consequences depend on the flip-flop state.

### H/P — ENIAC Part II documents staged event/timing retention

Part II p. IV-43 describes an incoming switch pulse setting an `unsynchronized flip-flop`. That state enables a synchronizing gate through which a later central programming pulse sets a `synchronized flip-flop`; the second state enables a transmitter gate; a later central program pulse is transmitted and resets both flip-flops.

The report explains the second stage in terms of avoiding an unreliable reduced-magnitude pulse if the unsynchronized switch event overlaps a central program pulse. This supplies a period machine-specific sequence in which **an event is retained until machine timing can qualify it for later action**.

Detailed source record: [`evidence/06-eniac-timing-retention-deepening.md`](../evidence/06-eniac-timing-retention-deepening.md).

### H/P — Burks directly grounds two stable states and their cross-coupled mechanism

On p. 758 Burks states that the ENIAC flip-flop shown in Fig. 3 (tubes 1–4) has **two stable states** because direct-current connections run from the plate of each tube to the grid of the opposite tube. He explains the mutually reinforcing bias relation and discusses resistor ratios, tube variation, plate resistance, and power-supply regulation as variables relevant to stability.

Burks explicitly separates two design aspects:

1. steady-state stability, depending on direct-current connections;
2. flipping/triggering action, depending on alternating-current connections as well.

This closes the mechanism-level gap below the word `flip-flop`: the primary source itself explains why the circuit can remain in one of two stable conditions and why transition/recovery behavior is a separate design problem.

**Primary anchor:** Arthur W. Burks, “Electronic Computing Circuits of the ENIAC,” _Proceedings of the I.R.E._ 35(8), August 1947, pp. 757–759: <https://archive.computerhistory.org/resources/text/Knuth_Don_X4100/PDF_index/k-8-pdf/k-8-r5367-1-ENIAC-circuits.pdf>.

### H/P — Burks gives explicit microsecond-scale set and recovery margins

On p. 759 Burks reports that the Fig. 3 flip-flop can be set in about **one microsecond** and is ready to reset in about **four microseconds**. In ENIAC operation it has at least **2.5 microseconds** in which to be set and is **never reset sooner than ten microseconds after being set**.

These figures matter because they show that a very short retained state still has a nontrivial engineering time structure: state holding, transition, and readiness for a later transition have distinct constraints.

### H/P — Whirlwind makes the flip-flop / register distinction explicit in period vocabulary

R-221 says the basic Whirlwind register length is sixteen binary digits and describes the A-register as a `simple flip-flop register`. Its listed functions are architectural and operational rather than merely physical. The same report calls core-memory locations `storage registers`.

The safe conclusion is two-sided:

> an individual bistable mechanism is not automatically a register; but a period computer could explicitly organize flip-flops as a register, and the word `register` itself could span more than one physical retention substrate.

**Primary anchor:** M. F. Mann, R. R. Rathbone, J. B. Bennett, *Whirlwind I Operation Logic*, Project Whirlwind Report R-221, 1 May 1954, introduction p. 1-1 and §2.231 / p. 2-12: <https://www.bitsavers.org/pdf/mit/whirlwind/R-series/R-221_Whirlwind_I_Operational_Logic_May54.pdf>.

---

## Retained state

The bounded physical target is a **which-stable-condition** distinction in a powered regenerative valve circuit.

In ENIAC, that circuit condition participates in machine-defined states such as:

- normal / abnormal flip-flop state;
- one selected stage of a counter;
- a pending carry-over condition;
- a reader/program control condition;
- a pending unsynchronized event awaiting later machine-timed qualification.

The important distinction is:

```text
physical circuit condition
    !=
architectural / procedural meaning
```

The latter depends on where the flip-flop is used and on surrounding gates, pulses, counters, and program wiring.

---

## Physical / logical substrate

In the Eccles–Jordan sources, coupled thermionic valves and resistive return/back-coupling create regenerative interaction. In the bounded ENIAC evidence, vacuum-tube flip-flop circuits supply two operationally distinguished stable states used inside counters and controls.

Burks 1947 adds a directly inspected period-published schematic and explicit DC cross-coupling explanation. The original PX-1-105 drawing itself remains uninspected, so no PX-specific drafting/component claims are inferred from Burks's simplified figure.

This case is deliberately earlier than transistor latches and SRAM. It should not silently import CMOS static-power behavior, modern metastability analysis, edge-triggered D flip-flop semantics, or modern register-file architecture into the thermionic mechanisms.

---

## Retention mechanism

The crucial mechanism is **regenerative bistability under operating power**.

A useful engineering reconstruction is:

1. a stimulus establishes one of the circuit's operating conditions;
2. cross-coupled feedback reinforces that condition;
3. while suitable power and circuit conditions remain, no periodic rewrite is required merely because time passes;
4. a later set/reset/clear event can force a different condition;
5. transition and recovery-to-ready timing are separate constraints from steady-state holding.

This is neither magnetic-core remanence nor DRAM refresh.

A bounded descriptive phrase is:

> **powered quiescent working retention** — a state can remain stable under power without a scheduled refresh operation that repeatedly reconstructs it.

The phrase remains local to this case rather than a controlled glossary term.

---

## Is continuous power “maintenance”?

### E — continuous power is an enabling condition

The thermionic circuit requires powered operating conditions for the regenerative state to exist. Removing those conditions destroys continuity of the working state.

### E — continuous power is not the same thing as periodic state maintenance

The primary evidence does not describe a DRAM-like deadline in which each flip-flop must periodically be rewritten merely to remain in its current state. Nor does it describe delay-line-style circulation in which the logical pattern survives by repeatedly traversing a path.

> **continuous energy supply ≠ continuous state rewrite / refresh.**

This does not mean power is irrelevant or the circuit maintenance-free. Burks makes component tolerance, bias/stability, power regulation, triggering, and recovery explicit engineering concerns.

---

## Addressing and access geometry

A single flip-flop does not require an address in order to retain its state. Its output can be wired directly into later gates.

At the ENIAC accumulator/control level, counters and program controls add organization around individual state elements. Part II also shows a retained control condition enabling a later timing gate. Whirlwind adds another layer: R-221's A-register is defined through bus/gate connectivity and machine functions.

The comparison must therefore keep **element retention**, **grouping**, **selection/connectivity**, **architectural role**, and **interface/use semantics** distinct.

---

## Read semantics

In the bounded ENIAC evidence, using a flip-flop output to control a gate or selector is not described as destroying the state. Reset is a separate operation.

Thus this case supplies:

- **volatile** state;
- **nondestructive state use / observation** in the bounded role;
- **no periodic refresh requirement established by the source**;
- explicit set/reset/clear semantics.

It blocks the shortcut:

```text
volatile
    = dynamic refresh
    = destructive read
```

The three are independent properties.

---

## Write and erasure semantics

For this bounded case:

- **set / flip** establishes a different stable/control condition;
- **reset** returns the flip-flop to its designated normal condition;
- **clear** initializes or erases machine working state according to surrounding ENIAC circuits;
- **power loss / power-up** does not preserve the previous logical working condition as an admissible continuation.

ENIAC's initial clear shows that `physical state exists` is not enough. A system also needs a rule for which state is valid.

---

## Time

The case directly stress-tests duration. A pending carry or control event may need to survive only for microseconds, not archival years.

Yet the interval is not analytically empty:

```text
t0: state/event is established

intervening machine activity and settling occur

t1: later behavior depends on whether the earlier condition still holds or has recovered in time
```

Burks's p. 759 timing values make this concrete: roughly 1 µs set, roughly 4 µs readiness for reset, at least 2.5 µs allowed for setting, and no reset sooner than 10 µs after set in ENIAC.

The repository therefore has no evidence-based minimum duration below which retention automatically stops being meaningful. The useful test is functional and counterfactual:

> Would later machine behavior differ if the state failed to remain across the relevant interval or failed to recover in time?

For the bounded ENIAC examples, yes.

---

## Maintenance and labor

Reliable working retention depends on:

- continuous electrical operating conditions;
- correctly biased and functioning valves/components;
- component tolerances and power-supply regulation;
- pulse and gate timing;
- transition/recovery margins;
- reset/clear circuitry;
- operators and maintenance procedures that establish a known machine state after power-up or interruption.

These dependencies must not be flattened into `the flip-flop is continuously refreshed`. The sources support powered circuit operation and explicit initialization/reset, not periodic state reconstruction analogous to DRAM.

---

## Failure / forgetting modes

This case adds several bounded forms of technical loss:

- loss of operating power, ending continuity of the working state;
- incorrect or indeterminate power-up state;
- failure to clear before computation;
- unintended set/reset from erroneous pulses or circuit faults;
- insufficient stability margin under component/power variation;
- failure to complete a transition or recover before the next required operation;
- inability of a later gate/circuit to discriminate the intended state;
- component/power-supply failure that destroys stable operating conditions.

These are not equivalent to DRAM leakage, Flash logical invalidation, or RADOS stale-replica currentness failure.

---

## Engineering reconstruction

### E — short duration does not make retention trivial

The ENIAC carry/control flip-flops matter precisely because a condition established earlier must remain available after intervening machine events and before later action. Burks's microsecond timing margins show that very short retention can still have explicit design constraints.

### E — later admissibility does not require discrete retrieval

The later event may be **state-sensitive use**: retained condition can remain continuously exposed at an output and simply condition what downstream circuitry does at `t1`.

The cross-case relation should therefore allow:

```text
later recovery / interpretation / admissibility / state-sensitive use
```

rather than requiring a separate storage-style retrieval transaction.

### E — power and maintenance must be decomposed

The comparison needs at least:

```text
energy prerequisite
periodic reconstruction
access-triggered restoration
continuous circulation
```

as distinct axes.

### E — state holding and state transition/recovery must be decomposed

Burks explicitly separates steady-state stability from flipping/triggering action and recovery. A mechanism can therefore be excellent at holding one of two states while still having separate constraints on how quickly or reliably it can change state and become ready for another operation.

This distinction should carry forward into SRAM/static-cell work.

### E — initialization is part of usable retention

Random/accidental power-up states are not valid continuations of a prior computation merely because each flip-flop physically occupies some state. Initial clear establishes an admissible starting configuration.

### E — element substrate and register role must be separated

The Whirlwind witness strengthens `flip-flop ≠ register`. A bounded register-level description needs retained elements plus grouping/connectivity and a machine-defined use relation. The same period report also uses `register` for magnetic-core storage, so neither `register = flip-flop array` nor `register = modern CPU register` is safe as a universal historical rule.

For later SRAM/cache work, keep separate:

```text
state element / substrate
organization / grouping
selection and connectivity
architectural role
interface / use semantics
```

---

## Philosophical / media-theoretical interpretation

### I — working retention is not a miniature archive

The value of this case is not to say that every flip-flop is a tiny archive. Its retained state can be entirely internal to ongoing computation and may vanish at reset or power-off without any expectation of historical durability.

This supports keeping `technical retention` broader than Stieglerian tertiary retention and archival preservation.

### I — microtemporality matters here, but does not define retention universally

The ENIAC example is highly compatible with Ernst's insistence on machine-specific timing: set, stable interval, later gate action, reset, and recovery are technically decisive here.

But the earlier Ernst test blocks universalizing this regime. Flash reclamation and RADOS repair operate on different triggers and horizons, while core/Flash can remain quiescent without powered bistability.

---

## Functional analogies and limits

### A — flip-flop as a narrow electronic counterpart to retained working position

A bounded functional comparison with the abacus case is possible:

- a state established during an operation remains available to affect a later operation;
- the retained state is current working state, not automatically history;
- reset/clear removes the working condition.

But the mechanisms and historical concepts are radically different. An abacus bead is not genealogically a flip-flop, and a flip-flop is not merely an electronic bead.

### Limit — flip-flop ≠ register

A bistable element is a mechanism for retaining state. A `register` adds architectural organization/use. ENIAC's vocabulary distinguishes flip-flops, ring counters, and accumulators; Whirlwind R-221 later makes the implementation/architecture relation explicit with `simple flip-flop register` while also using `storage register` for core storage.

### Limit — not a transistor/SRAM history

Later transistor latches, static RAM cells, clocked flip-flops, register files, and caches change implementation, power behavior, fan-out, timing, array selection, and interface semantics. They require separate evidence rather than being treated as copies of the thermionic case.

### Limit — published primary schematic ≠ original PX-1-105 drawing

Burks 1947 directly grounds the bounded ENIAC bistability mechanism through a period-published simplified schematic and explicit explanation. The original PX-1-105 `Flip-Flop Circuit` drawing has still not been reliably rendered and inspected in this research sequence.

Therefore:

```text
Burks 1947 published simplified schematic
    = mechanism-level primary evidence

Burks Fig. 3
    != facsimile verification of PX-1-105
```

PX-1-105 remains archival cleanup for drawing-specific topology, revision, annotation, or drafting claims. It is no longer a generic blocker for the bounded mechanism claims. The exact 1919 _Electrician_ / _Radio Review_ page images likewise remain archival cleanup because the contemporary mechanism is independently anchored by the patent and British Association proceedings.

---

## Cross-case result

The mechanism map can distinguish:

```text
abacus
    passive positional working state

powered thermionic flip-flop / ENIAC
    powered regenerative working state
    state-holding stability distinct from transition/recovery timing
    no periodic state refresh established

Whirlwind A-register boundary witness
    grouped / connected architectural working state
    explicitly described as a flip-flop register

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

The main result is a category correction:

> **technical retention can be nontrivial at microsecond timescales; later continuity can be demonstrated by state-sensitive use rather than a separate retrieval operation; state-holding stability and transition/recovery are separate engineering dimensions; and the physical state element must be compared separately from the architectural organization that makes a retained value a register-level machine state.**

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Eccles and Jordan filed GB148582A in 1918 for `Improvements in ionic relays` | H/P | patent metadata |
| The patent describes regenerative `retroaction` continuing the coupled-valve condition after the initiating stimulus under the specified adjustment | H/P | patent abstract / Fig. 1 description |
| British Association 1919 proceedings directly describe trigger-relay resistance/back coupling, electrical stimulus, reinforcing changes, and `no restoring influence` | H/P | Transactions of Section G, pp. 271–272 |
| The early Eccles–Jordan sources frame the device as relay/amplification/trigger circuitry rather than a computer register | H/P | period vocabulary |
| The 1946 ENIAC report says a decade counter stores a digit and a decade flip-flop remembers whether carry-over must occur | H/P | Part I, Ch. IV |
| During delayed carry, the decade flip-flop remains set across intervening digit pulses until a later reset/carry phase | H/P | Part I, Ch. IV §4.3.2 |
| ENIAC supports static use of accumulator counter-state outputs by other units | H/P | Part I, Ch. IV §4.3.3 |
| ENIAC power-up could leave flip-flops in accidental states, requiring initial clear | H/P | Part I, Ch. II §2.1.2 |
| A reader-start flip-flop could remember a pending future read request | H/P | Part I, Ch. II §2.2.1 |
| Part II p. IV-43 directly documents staged unsynchronized/synchronized retained control state | H/P | machine-specific primary technical text |
| Burks 1947 calls the flip-flop a remembering circuit type | H/P | p. 757 |
| Burks directly explains two stable states through DC plate-to-opposite-grid cross-coupling | H/P | p. 758 |
| Burks separates steady-state stability from triggering/recovery dynamics | H/P | p. 758 |
| Burks reports about 1 µs set, 4 µs ready-reset, ≥2.5 µs set allowance, and no reset earlier than 10 µs after set | H/P | p. 759 |
| R-221 calls the Whirlwind A-register a `simple flip-flop register` and assigns machine-level functions | H/P | 1 May 1954 R-221, §2.231 / p. 2-12 |
| R-221 also uses `storage register` for magnetic-core storage | H/P | R-221 introduction / p. 1-1 |
| Continuous power is an enabling condition but not equivalent to periodic state refresh in this bounded implementation | E | mechanism comparison against DRAM/delay line |
| Very short-lived working state can satisfy a nontrivial retention relation | E/I | bounded inference supported by report sequences and Burks timing |
| Later retention must always involve a discrete retrieval operation | X | contradicted by bounded static/state-output use |
| `volatile = dynamic refresh = destructive read` | X | contradicted by this case plus grounded DRAM/core comparisons |
| State-holding stability and transition/recovery are one identical property | X | contradicted by Burks's explicit design decomposition |
| Every flip-flop is historically or architecturally a register | X | unsupported; ENIAC and Whirlwind separate element/use levels |
| Every period `register` is the modern CPU-register category | X | contradicted by R-221's broader vocabulary |
| Burks Fig. 3 is a facsimile of PX-1-105 | X | not established |
| Register role and physical retention substrate should be separate comparison axes | E | bounded Whirlwind/ENIAC reconstruction |

---

## Sources

### Primary

1. William Henry Eccles and Frank Wilfred Jordan, **“Improvements in ionic relays,”** British Patent GB148582A, filed 21 June 1918, published 5 August 1920: <https://patents.google.com/patent/GB148582A/en>.
2. Eccles and Jordan, **“A Trigger Relay utilising Three Electrode Thermionic Vacuum Tubes,”** in _Report of the Eighty-Seventh Meeting of the British Association for the Advancement of Science: Bournemouth: 1919_, Transactions of Section G, pp. 271–272: <https://archive.org/details/reportofbritisha20adva>.
3. **A Report on the ENIAC (Electronic Numerical Integrator and Computer)**, U.S. Army / University of Pennsylvania, Moore School of Electrical Engineering, 1 June 1946: <https://ftp.arl.army.mil/~mike/comphist/46eniac-report/>.
   - Part I, Chapter IV: <https://ftp.arl.army.mil/~mike/comphist/46eniac-report/chap4.html>.
   - Part I, Chapter II: <https://ftp.arl.army.mil/~mike/comphist/46eniac-report/chap2.html>.
4. Arthur W. Burks, **“Electronic Computing Circuits of the ENIAC,”** _Proceedings of the Institute of Radio Engineers_ 35(8), August 1947, pp. 756–767, especially pp. 757–759: <https://archive.computerhistory.org/resources/text/Knuth_Don_X4100/PDF_index/k-8-pdf/k-8-r5367-1-ENIAC-circuits.pdf>.
5. M. F. Mann, R. R. Rathbone, J. B. Bennett, **_Whirlwind I Operation Logic_**, Project Whirlwind Report R-221, MIT Digital Computer Laboratory, 1 May 1954, especially introduction p. 1-1 and §2.231 / p. 2-12: <https://www.bitsavers.org/pdf/mit/whirlwind/R-series/R-221_Whirlwind_I_Operational_Logic_May54.pdf>.

### Evidence records

- [`evidence/06-burks-1947-eniac-flip-flop-grounding.md`](../evidence/06-burks-1947-eniac-flip-flop-grounding.md) — grounding/promotion record.
- [`evidence/06-flip-flop-register-boundary-addendum.md`](../evidence/06-flip-flop-register-boundary-addendum.md) — period register boundary and artifact-specific gap ledger.
- [`evidence/06-eniac-timing-retention-deepening.md`](../evidence/06-eniac-timing-retention-deepening.md) — Part-II staged timing-retention evidence.
- [`evidence/06-eccles-jordan-1919-proceedings-deepening.md`](../evidence/06-eccles-jordan-1919-proceedings-deepening.md) — 1919 authorial mechanism evidence.

### Remaining archival cleanup

- exact _Electrician_ 83 (19 September 1919), p. 298 / _Radio Review_ 1(3), December 1919, pp. 143–146 page-preserving facsimiles;
- original ENIAC PX-1-105 `Flip-Flop Circuit` drawing for drawing-specific details.

Neither cleanup item blocks the bounded `grounded` status because the central mechanism claims now rest on multiple independent period primary anchors, including a directly inspected published ENIAC schematic and explicit circuit/timing account.