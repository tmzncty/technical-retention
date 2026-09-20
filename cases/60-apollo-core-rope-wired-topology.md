# Apollo Core Rope Memory: Fixed Program State in Wiring Topology

## Scope

- **Object / system:** Block II Apollo Guidance Computer (AGC) fixed memory, with the MIT Instrumentation Laboratory core-rope implementation as the principal bounded system;
- **Date range:** approximately 1964–1972 for the principal contemporary evidence, with a bounded 1988 NASA-sponsored retrospective production witness;
- **Institutions:** MIT Instrumentation Laboratory / Charles Stark Draper Laboratory, NASA, and manufacturing contractors including Raytheon;
- **Why this case matters for technical retention:** core rope is a magnetic-memory-looking technology in which the **payload bit is not the remanent magnetic state of the ferrite core**. The retained program is encoded by whether a sense wire physically threads or bypasses a core. The core switches during access, but the stored program does not thereby change.

This case is deliberately not a general history of the Apollo Guidance Computer, ferrite memories, software engineering, or aerospace computing. It isolates a narrower retention problem:

> What changes when a retained bit moves from a reversible material state to a manufactured wiring relation?

It therefore complements, rather than duplicates, [`Case 02`](02-magnetic-core-destructive-read.md). Case 02 studies classic coincident-current read/write core memory, where remanent magnetization itself carries the bit and a read may destroy that state. Case 60 studies a fixed transformer memory whose readable program is carried by **wiring topology** while the selected core is intentionally switched as part of the read process.

A repository search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated core-rope case at the time of this slice, so no parallel engineering history is reproduced here. Later checks for `Apollo core rope verification` and `core rope Raytheon delivery tape` likewise found no reusable dedicated treatment.

---

## Evidence navigation

- [`../evidence/60-apollo-core-rope-1964-1972-grounding.md`](../evidence/60-apollo-core-rope-1964-1972-grounding.md) — principal mechanism/history grounding for the 1964–1972 bounded case.
- [`../evidence/60-nasa-1967-flight-fixed-memory-certification-deepening.md`](../evidence/60-nasa-1967-flight-fixed-memory-certification-deepening.md) — NASA approval → hard-memory fabrication → bit-for-bit manufactured-memory comparison → acceptance/certification and configuration-control deepening.
- [`../evidence/60-1965-1988-rope-verification-legibility-boundary-deepening.md`](../evidence/60-1965-1988-rope-verification-legibility-boundary-deepening.md) — contemporary readout-noise problem framing plus NASA-sponsored factory comparison/rework evidence, separating physical fixedness from correct manufacture and readable retrieval.

---

## Historical vocabulary

MIT's 1972 final report calls the AGC program store a **`nondestructive read out (core rope) memory of the transformer type that has the information wired in`** and says its contents cannot be changed by ordinary program steps.[^r700]

The same report's fixed-memory section uses several terms that matter for the retention analysis:

- `fixed memory`;
- `transformer type`;
- `core rope`;
- `sense lines`;
- `set/reset line`;
- `inhibit lines`;
- `address decoding`;
- and information `permanently wired in during manufacture`.[^r700]

NASA's 1971 design-criteria report describes fixed/read-only memories more generally as memories whose contents are manufactured into them and therefore require physical modification when the contents are changed.[^nasa-sp8070]

A 1966-filed MIT manufacturing patent uses the broader contemporary vocabulary **`wired-in memories`** and states that their data are stored according to the **geometry of the wiring configuration**.[^mit-wired-patent]

A separate 1965-filed General Precision Systems patent also uses `wired-in memory` vocabulary and explicitly identifies the Apollo Computer as using an MIT-designed `core-rope memory`. Its criticism of core-rope interrogation noise is kept as a **competing inventor's period problem framing**, not treated as an independent Apollo qualification verdict.[^putterman]

These period terms are strong enough that the modern phrase `topological retention` below should be understood as an **engineering reconstruction**, not as historical actor vocabulary.

---

## Retained state: the bit is a relation, not the core's momentary polarity

The most important technical fact is easy to miss if all ferrite-core technologies are grouped together.

MIT's final report states that in the AGC rope:

```text
sense wire threads selected core  → stored 1
sense wire does not thread core   → stored 0
```

The report gives the Block II organization as six modules, each with 512 cores and 192 sense lines. A core can therefore participate in many stored bits rather than carrying only one bit in its own remanent magnetization.[^r700]

The retained program state is consequently a **geometric coupling relation**:

```text
sense conductor
    ↕
passes through / bypasses
    ↕
magnetic core
```

What survives between reads is principally the manufactured routing of conductors and the integrity of the associated module, not a unique `0`/`1` magnetization left in each core for each program bit.

This gives a sharp counterexample to the loose equation:

```text
magnetic memory = information retained as magnetic polarity
```

The AGC rope uses ferrite magnetic behavior to **read** the stored relation, while the program bit itself is wired into the module.

---

## Read semantics: switching the core without changing the program

The Block II fixed-memory read cycle deliberately changes magnetic state.

MIT describes selection by set/reset and inhibit currents that leave one core uninhibited. The selected core switches. That changing flux induces a voltage in every sense line that threads the core. The machine then selects the appropriate subset of sense lines for the requested word. Afterward a reset current is passed through all cores; only the core that was just set changes state again.[^r700]

So a physical core undergoes a state transition during an ordinary read:

```text
address selects one core
    ↓
core switches
    ↓
threading sense lines receive induced voltage
    ↓
selected 16-bit word is sensed
    ↓
core is reset
```

Yet this is a **nondestructive logical read** of the program because the bit-defining relation — whether each sense line threads the core — has not changed.

This yields one of the case's strongest distinctions:

> **state-bearing structure ≠ state-changing transducer.**

The ferrite core can change magnetic state twice in a read cycle while the stored program remains invariant because the program is embodied in the wiring geometry.

That is almost the inverse of the classic destructive-read core-memory case:

```text
Case 02 classic core RAM:
core magnetization carries bit
read can destroy bit state
rewrite restores logical continuity

Case 60 AGC core rope:
wire/core topology carries bit
core switching is read transduction
reset restores device operating condition, not program payload
```

The two systems can therefore share ferrite material and switching physics while having different retention semantics.

---

## Addressability: part of the decoder is also wired into the retained artifact

The rope's wiring does more than encode payload bits.

MIT says the core rope incorporates an **address-decoding property** in its wiring. In the bounded Block II design, set/reset lines initially try to switch groups of cores while successive inhibit-line pairs eliminate halves of the candidate group until only one core remains uninhibited. Additional diode/resistor switching chooses which sense-line group reaches the sense amplifiers.[^r700]

Thus the fixed-memory module contains at least two distinct classes of durable relation:

1. **payload-bearing sense-line routing** — which sense lines thread which cores;
2. **selection infrastructure** — inhibit wiring and local switching structure that make the intended core/word recoverable.

This is another reminder that retained payload and retained recoverability infrastructure are not the same state even when they are manufactured into the same module.

A rope with intact bit-pattern wiring but failed addressing or selection circuitry may still physically embody the program while no longer being able to return the correct word on demand.

---

## Write and erase semantics: changing the program means changing the artifact

The AGC cannot rewrite core-rope words through normal program instructions. MIT's report explicitly contrasts erasable core memory with fixed rope memory and says the logical difference is that the rope contents cannot be changed by program steps.[^r700]

NASA's 1971 design criteria make the lifecycle consequence explicit: fixed-memory contents are manufactured into the device, so content change requires physical modification. For the Apollo core-rope program memory, NASA reports roughly a **four-week production cycle** to procure new memory modules for program changes.[^nasa-sp8070]

The retention/forgetting boundary is therefore radically different from RAM, EEPROM, or Flash:

```text
ordinary operation:
read selected word
program geometry remains fixed

program change:
change source/software definition
    ↓
translate new bit pattern into manufacturing instructions
    ↓
thread / route new physical wiring pattern
    ↓
assemble + verify new module
    ↓
replace or rework physical memory artifact
```

There is no ordinary electrical `erase` operation for the fixed program image.

A bit can cease to be current because a different module is manufactured and installed even though the old module still physically preserves the previous program. Therefore:

> **program supersession ≠ physical disappearance of the superseded program artifact.**

---

## Manufacturing: software becomes retained geometry

MIT's final report describes a tape-controlled machine that determines the routing of the sense wires for the operator, translating software requirements into a physical wire path. The operator then threads each wire through, or bypasses, the indicated cores.[^r700]

This makes manufacturing part of the retention mechanism in an unusually literal way.

The handoff is approximately:

```text
program / fixed constants
    ↓
verified bit pattern
    ↓
machine-guided routing instructions
    ↓
operator threading decisions
    ↓
wire/core topology
    ↓
flight-readable fixed memory
```

The 1966 MIT patent makes the broader wired-memory principle explicit: data are stored according to wiring geometry, and a program-controlled Jacquard-like process can separate conductors into logical-one and logical-zero groups before the harness is mounted on magnetic cores.[^mit-wired-patent]

The process should not be romanticized as a metaphorical act of `weaving software` and left there. The technical point is stronger and narrower:

> **manufacturing correctness becomes information correctness.**

A routing error is not merely a defect in packaging around an otherwise correct memory state; it can *be* a wrong stored bit.

---

## 1967 flight fixed-memory certification: topology alone is not configuration identity

NASA's October 4, 1967 **_Apollo Guidance Software Development and Verification Plan_** now supplies a direct process-level witness for what happened after the program was approved. See [`../evidence/60-nasa-1967-flight-fixed-memory-certification-deepening.md`](../evidence/60-nasa-1967-flight-fixed-memory-certification-deepening.md).[^nasa-1967-verification]

The report separates software approval from hard-memory fabrication, verification, and KSC system testing. Section 5.5.1 then requires procedures to ensure that the approved program delivered by the software contractor is **identical, bit for bit, to the manufactured flight fixed memory**, with formal MSC acceptance/certification and comparison of the manufactured contents against the MSC-approved fixed-memory software configuration.[^nasa-1967-verification]

That adds a lifecycle distinction to the mechanism-level argument above:

```text
approved software configuration
!=
manufacturing/control representation
!=
manufactured rope artifact
!=
certified flight artifact
```

The rope's physical topology may be stable and runtime read-only while still requiring evidence that it embodies the authorized bit pattern. A wrongly manufactured topology would not become correct merely because normal AGC instructions could not rewrite it.

The same 1967 plan says that after the First Article Configuration Inspection, changes to the configuration-controlled program require Guidance Software Control Panel approval, including changes to any memory cell. It also allows a previous flight's fixed memory to be approved for a later flight under a reduced cycle.[^nasa-1967-verification]

The engineering reconstruction is therefore:

```text
physical persistence
!=
bitwise correspondence to approved software
!=
configuration authority / mission currentness
```

NASA SP-8070 sharpens the time boundary: the Apollo example had an approximately four-week new-module production cycle, while its verification cycles were reported as at least as long as production cycles.[^nasa-sp8070] `manufacturing time`, `verification time`, and `total revision-to-flight latency` should therefore not be collapsed into one rope-production constant.

This is not evidence that the 1967 plan specifies every Raytheon manufacturing detail, that every mission followed the diagram without deviation, or that bit-for-bit acceptance proved absence of latent hardware faults or correctness of the software requirements themselves.

---

## 1965–1988 verification / legibility boundary: fixed does not mean self-authenticating or self-reading

The newer deepening packet adds two different evidence roles that sharpen the 1967 process without pretending to be the same kind of source. See [`../evidence/60-1965-1988-rope-verification-legibility-boundary-deepening.md`](../evidence/60-1965-1988-rope-verification-legibility-boundary-deepening.md).[^putterman][^tomayko]

First, Tomayko's 1988 NASA-sponsored history reports that Raytheon tested manufactured rope modules against the **program delivery tape**, built a device for that comparison, and could correct hard-wiring errors introduced during manufacture while the factory rework window remained available.[^tomayko]

That supplies an implementation-level retrospective witness for the relation already required normatively in 1967:

```text
reference program representation
!= manufactured topology
!= comparison evidence
!= accepted flight artifact
```

Second, Putterman's 1965-filed competing NDRO patent explicitly identifies Apollo/MIT core rope as existing prior art and criticizes the multiple-current interrogation scheme for generating noise. Its 512-word / nine-current example is useful as a **period problem framing**, not as a measured failure rate for the final Block II AGC.[^putterman]

The two observations together support a sharper retention boundary:

```text
payload-bearing topology survives
    != topology was manufactured correctly
    != read/selection channel is within usable margin
    != artifact is currently authorized for flight
```

Thus physical fixedness protects against ordinary runtime rewrite but does not make the artifact self-verifying or guarantee that the retained relation remains electrically legible.

---

## Time: retention interval and revision latency diverge

Core rope creates two very different timescales.

### 1. Quiescent program retention

Once correctly manufactured, the fixed bit pattern does not require periodic refresh or rewrite merely to preserve its logical value. NASA lists program retention through power loss or electrical malfunction among the advantages of fixed memory in spaceborne computers.[^nasa-sp8070]

### 2. Program revision latency

Changing the fixed program is slow because the new state must travel through a manufacturing and verification process. NASA's approximately four-week procurement cycle for Apollo program changes is evidence that **revision latency can be much longer than read latency or quiescent retention maintenance time**.[^nasa-sp8070]

The 1967 verification plan makes that lifecycle more explicit: acceptance of the software authorizes hard-memory fabrication, while the manufactured fixed memory still requires comparison, formal acceptance, and certification.[^nasa-1967-verification]

Tomayko's later production history adds a lifecycle asymmetry: a hard-wiring error found while the rope was still in the factory could be corrected as production rework, whereas a logical change after completion/installation crossed into a much more expensive replacement, rework, approval, and verification path.[^tomayko]

This creates a retention regime in which stability is bought partly by making ordinary modification difficult.

The right conclusion is not `immutable = reliable`. Instead:

```text
easy accidental rewrite is strongly reduced
but
intentional revision becomes a manufacturing + verification operation
```

Retention strength and update flexibility trade against one another.

---

## Failure and technical forgetting modes

### Physical destruction

MIT's report says the permanently wired information is nondestructible in ordinary operation except by physical destruction or failure in associated semiconductor diodes.[^r700]

### Open or shorted sense / inhibit wiring

The same final report describes fixed-memory checking intended to detect failures such as open or shorted sense and inhibit lines. Such a failure can make an otherwise manufactured bit pattern unreadable or incorrectly selected.[^r700]

### Selection / diode failure

Payload topology can survive while the local selection path no longer routes the appropriate induced signal to the sense amplifiers.

### Read-channel margin / interrogation noise

A contemporary competing patent framed multiple-current core-rope interrogation as a noise problem. Because that statement comes from an inventor motivating an alternative design, it is not accepted as a quantified Apollo reliability result. It is nevertheless period evidence that **stable wired payload** and **successful electrical retrieval** were separable engineering questions.[^putterman]

### Manufacturing misrouting

A wire routed through a core when it should bypass it, or vice versa, directly changes the manufactured bit pattern.

The 1967 NASA certification procedure is especially important here because it treats manufactured contents as something that must be compared against the approved configuration rather than presumed correct.[^nasa-1967-verification] Tomayko's later NASA history reports that Raytheon actually tested rope modules against the program delivery tape and could correct hard-wiring errors during production.[^tomayko]

### Configuration divergence

A physical rope may contain a readable fixed program yet fail the stronger relation `this artifact matches the currently approved flight configuration`. That is a configuration/authority failure, not magnetic decay.

### Supersession without destruction

A replaced rope module can remain a perfectly readable artifact containing an obsolete program. Logical currentness changes because a different module is designated for flight, not because the older program automatically vanishes.

These failure modes should not be collapsed into `the core lost its magnetization`.

---

## Historical record

### Primary / contemporary institutional sources

1. **MIT Instrumentation Laboratory / Charles Stark Draper Laboratory, _MIT's Role in Project Apollo, Volume III: Computer Subsystem_, R-700 (1972).** Section 2.3.6 identifies the transformer-type core rope as nondestructive fixed program memory; §3.5.2 and Figs. 3-12/3-13 describe thread/bypass encoding, core switching, inhibit selection, sense-line readout, and six-module organization; the mechanical-construction section describes tape-guided operator threading.[^r700]
2. **NASA SP-8070, _Spaceborne Digital Computer Systems_ (March 1971).** The memory section distinguishes fixed/read-only memory from read-write memory, identifies manufactured contents and physical modification as the update path, names the Apollo core-rope program memory, reports an approximately four-week production cycle for program changes, and notes verification cycles at least as long as production cycles.[^nasa-sp8070]
3. **Ramon L. Alonso, Robert E. Oleksiak, William B. Turner, MIT, U.S. Patent 3,451,129, filed January 5, 1966.** Contemporary primary evidence that wired-in computer memories stored data in wiring geometry, with threading/bypass choices encoding binary values and a tape-controlled Jacquard-derived manufacturing method.[^mit-wired-patent]
4. **Hayden A. Nelson, U.S. Patent 3,419,855, filed December 24, 1964.** Contemporary evidence for a read-only wired-core fixed-information memory in which storage resides in the physical configuration of drive windings; useful for bounding Apollo/MIT novelty claims.[^nelson]
5. **NASA Manned Spacecraft Center, Guidance Software Validation Committee, _Apollo Guidance Software — Development and Verification Plan_, October 4, 1967.** Direct process evidence for release of accepted software to hard-memory fabrication, fixed-memory bit-for-bit comparison against the approved configuration, formal MSC acceptance/certification, and configuration-control authority over later memory-cell changes.[^nasa-1967-verification]
6. **Harry Putterman, U.S. Patent 3,432,834, filed April 23, 1965 and published March 11, 1969.** Contemporary competing-design evidence identifying Apollo/MIT core rope as prior art and problem-framing multiple-current interrogation noise; not treated as independent Apollo failure measurement.[^putterman]

### Later institutional synthesis

7. **James E. Tomayko, _Computers in Spaceflight: The NASA Experience_, NASA-CR-182505 (March 1988).** NASA-sponsored retrospective evidence that Raytheon compared manufactured ropes with the program delivery tape, built a device for the comparison, and could correct hard-wiring errors during the factory window.[^tomayko]

### Related-repository check

8. `tmzncty/computing-archaeology` was searched for `core rope`, `Apollo core rope verification`, and `core rope Raytheon delivery tape`; no dedicated case was found during these slices. Broader magnetic-core, Apollo manufacturing, and vendor history remains routed there rather than being reconstructed here.

---

## Engineering reconstruction

### Finding 1 — retained information can be geometric while access energy is magnetic

The memory is read through magnetic switching and transformer induction, but the bit is defined by a conductor-routing relation. The energetic read mechanism and the retained information-bearing structure are therefore different things.

### Finding 2 — a changing physical component need not be the changing retained state

The selected ferrite core switches and resets during every read. That does not mean the stored program bit is destructively read, because the bit resides in topology that the switching cycle does not alter.

### Finding 3 — manufacturability can become part of write semantics

When electrical write authority is absent, `writing memory` becomes fabrication: prepare a verified bit pattern, route conductors accordingly, assemble, test, and install the artifact.

### Finding 4 — fixedness can move maintenance from runtime to production

Core rope requires little runtime work merely to preserve the program, but it demands expensive correctness work before deployment. Retention labor has not disappeared; much of it has moved earlier in the lifecycle.

### Finding 5 — physical persistence and current program identity can diverge

An old rope can still retain every bit after it is replaced. Whether that bit pattern is the **current flight program** depends on designation and installation history, not on physical survivability alone.

### Finding 6 — a manufactured state can require retained evidence of correspondence

The 1967 NASA process treats the approved software configuration and manufactured fixed memory as distinct representations that must be compared before the artifact is accepted.

Thus a retention analysis of fixed memory needs one more relation beyond substrate persistence:

```text
artifact payload survives
+
artifact remains readable
+
artifact corresponds to approved configuration
+
artifact remains authorized/current for its mission context
```

Those predicates may coincide in a healthy flight unit, but they are not logically identical.

### Finding 7 — durable topology can be durably wrong

Tomayko's factory-testing account sharpens the previous point. A routing error can be physically stable and still require correction. Therefore:

```text
persistent artifact
!= correctly manufactured artifact
```

The more difficult ordinary rewrite becomes, the more important it is to preserve and apply trustworthy reference/comparison evidence before deployment.

### Finding 8 — payload survival and legibility are independent enough to fail separately

Putterman's period critique, bounded to its source role, highlights that a core-rope read channel can face signal/noise constraints without implying that the wire/core topology has disappeared.

Therefore:

```text
payload embodiment
!= read-channel qualification
```

A complete retention account needs both the thing that persists and the mechanism that can still recover it.

---

## Functional analogy

### Mask ROM

A limited analogy to later mask ROM is useful: in both cases, ordinary operation reads a manufactured pattern that is not electrically rewritten by the executing program.

The analogy stops there. Core rope uses magnetic transformer coupling and conductor topology; semiconductor mask ROM uses a different fabrication substrate and circuit mechanism. No direct genealogy is asserted here.

The 1967 certification and 1988 factory-comparison evidence add only an abstract lifecycle comparison: a manufactured read-only payload can still require a reference configuration, post-manufacture verification, and a qualified read path. That is not a claim that Apollo rope established later ROM-verification practice.

### Classic magnetic-core RAM

This is a stronger **contrast** than an analogy.

- classic coincident-current core RAM: one core's remanent magnetic state can represent one bit;
- AGC rope: many sense-line bits are represented by physical thread/bypass relations around a core, while core magnetization changes as part of access.

Shared ferrite material therefore does not imply shared retention semantics.

### Case 70 — magnetic-core half-select / margin

Case 70 provides a bounded functional comparison: in both ordinary core RAM and core-rope readout, the information-bearing relation and the electrical margin needed to recover it should not be collapsed. Case 70's payload mechanism is remanent magnetic state; Case 60's is manufactured topology. No shared circuit or genealogy is claimed.

---

## Philosophical / media-theoretical interpretation

This case tests one narrow proposition:

> A retained technical state can reside primarily in a **relation among components** rather than in the momentary state of one component.

That proposition is engineering-grounded here: the selected magnetic core changes state, but the program remains because the wire/core relation remains.

It is tempting to say that the Apollo program was `literally woven into hardware`. That phrase can be useful, but only after the mechanism is kept exact. The retention claim is not that software became mystical material memory. It is that the executable program's fixed bits were materially constrained by routing decisions made during manufacture, and ordinary electrical operation lacked authority to revise those relations.

The certification and factory-comparison evidence add another bounded interpretation: making the program physically stable does not eliminate mediation. It creates a need to preserve correspondence among approved software, manufacturing representations, the woven artifact, and its authorized mission identity. And the read-channel evidence adds a second boundary: **persistence of inscription is not identical to legibility of inscription**. These are project-level interpretations of documented engineering distinctions, not NASA/MIT historical philosophical vocabulary.

For a Stieglerian or media-archaeological reading, this offers a particularly strong example of exteriorized technical inscription. But the case does not establish that every manufactured ROM is `tertiary retention`, nor that labor-intensive fabrication automatically supplies philosophical significance.

The technical result is sufficient on its own:

> **persistence can be topological even when access is dynamically magnetic, and stable topology still requires correct manufacture plus a working read path.**

---

## Counterexamples and limits

### Core rope is not ordinary magnetic-core RAM

Calling both technologies `core memory` without mechanism detail hides the central difference of this case.

### Nondestructive logical read does not mean nothing physical changes

The selected core switches and is reset. What remains unchanged is the bit-bearing wiring relation.

### Fixed does not mean impossible to change

The executing AGC cannot rewrite the rope electrically, but humans can manufacture, repair, replace, or destroy modules. `Read-only` is an interface/operational property, not a metaphysical claim.

### Bit-for-bit acceptance is not universal correctness proof

The 1967 plan requires comparison of manufactured fixed-memory contents against the approved configuration. Passing that comparison establishes the intended correspondence relation; it does not by itself prove the absence of every latent hardware fault or that the approved program requirements and algorithms are correct.[^nasa-1967-verification]

### Factory comparison does not prove a perfect manufacturing process

Tomayko reports a Raytheon comparison device and correction of hard-wiring errors. That is evidence that divergence was expected to be detectable and correctable, not evidence that every defect was always detected or that no accepted module ever contained a latent fault.[^tomayko]

### A competing patent's critique is not an Apollo failure statistic

Putterman's statement about operational reliability and interrogation noise is inventor problem framing in support of another design. It is valid evidence that such a design concern was articulated in 1965, but not a measured failure rate for final flight hardware.[^putterman]

### Apollo did not invent the general idea of wired-in fixed memory

By the mid-1960s, contemporary patents and technical literature already treated wired-in / wired-core read-only memories and geometry-based encoding as an existing class. This case makes no priority claim for Apollo, MIT, or Raytheon beyond the specific bounded implementation and manufacturing evidence used here.[^mit-wired-patent][^nelson][^putterman]

### The four-week figure is a program-change production-cycle witness, not a universal rope-manufacturing constant

NASA SP-8070 gives an approximately four-week procurement cycle in the Apollo context and separately notes verification cycles at least as long. Different module versions, production phases, verification regimes, and later retrospective accounts may report different elapsed times.

---

## Claim ledger

| Claim | Type | Evidence strength | Status |
| --- | --- | --- | --- |
| AGC fixed memory was a transformer-type core rope with information wired in | H/P | strong MIT final-report evidence | supported |
| A sense line threading a core represented one value and bypassing it represented the other | H/P | strong MIT final-report evidence | supported |
| The selected core switched and reset during read while the logical fixed program remained unchanged | H/P + E | strong circuit/operation description | supported |
| The program bit is better reconstructed as wiring topology than as remanent core polarity | E | direct inference from thread/bypass encoding and access cycle | supported |
| Rope wiring also embodied part of address decoding | H/P | strong MIT final-report evidence | supported |
| Normal program steps could not rewrite rope contents | H/P | strong MIT final-report evidence | supported |
| Apollo program change could require roughly a four-week new-module production cycle | H/P | contemporary NASA design-criteria evidence | supported, bounded |
| NASA SP-8070 reports verification cycles at least as long as Apollo rope production cycles | H/P | contemporary NASA design-criteria evidence | supported, bounded |
| Tape-guided operator threading translated software requirements into physical routing | H/P | strong MIT construction description | supported |
| NASA's 1967 plan required the manufactured fixed memory to be identical bit for bit to the approved program and formally accepted/certified | H/P | direct §5.5.1 evidence | supported |
| After FACI, configuration-controlled changes including any memory-cell change required GSCP approval | H/P | direct §7.1.1 evidence | supported |
| Tomayko reports Raytheon compared manufactured rope modules against the program delivery tape and built a device for the comparison | H/R | strong NASA-sponsored retrospective synthesis | supported, retrospective |
| Tomayko reports factory-stage correction of hard-wiring errors | H/R | NASA-sponsored retrospective synthesis | supported, retrospective |
| Putterman's 1965-filed patent identifies Apollo/MIT core rope as prior art and problem-frames multiple-current interrogation noise | H/P | direct contemporary patent text | supported as problem framing |
| Putterman's critique proves final Block II Apollo rope had a measured unacceptable reliability rate | X | no independent Apollo qualification measurement | rejected |
| Runtime read-only status, bitwise correspondence, read-channel usability, and mission authorization/currentness are distinct predicates | E | reconstruction from mechanism + production/readout evidence | supported, bounded |
| Apollo/MIT invented wired-in read-only memory | X | contradicted by contemporary prior-art record | rejected |
| Core rope and classic core RAM have the same retention mechanism because both use ferrite cores | X | contradicted by state-bearing mechanism | rejected |
| Core rope is historically equivalent to semiconductor mask ROM | A/X | functional analogy only; no genealogy established | rejected as historical identity |
| Core-rope fixedness proves a philosophical theory of technical memory | I/X | interpretation exceeds evidence | rejected |
| Bit-for-bit fixed-memory acceptance proves the approved program itself was semantically correct or the hardware fault-free | X | exceeds the 1967 acceptance claim | rejected |

---

## Next evidence work

Useful later deepening is narrow:

1. inspect a directly renderable facsimile of the 1964 Hayden A. Nelson `A Wired Core Memory for Airborne Computers` article;
2. trace the pre-Apollo wired-in / Dimond-ring / transformer-ROM genealogy only if a future prior-art argument requires it;
3. retrieve **direct Raytheon acceptance-test equipment/procedure, traveler, discrepancy, or rework records**, or mission/program-specific rope mismatch and configuration-change records; the 1988 NASA-sponsored history now establishes the factory-comparison/rework claim at a retrospective institutional level but does not replace those primary records;
4. inspect the underlying archival sources behind Tomayko's footnotes 58–59 if available;
5. obtain a direct AGC qualification source quantifying fixed-memory read/signal-margin criteria rather than relying on a competing patent's problem framing;
6. test a physical or simulated rope reader in `mechanical-computing-playground` if an experiment would clarify topology-versus-magnetization semantics.

The former broad `mission-specific rope production/configuration records` gap is now partially closed at both the 1967 plan/certification level and the 1988 NASA-sponsored production-history level. None of the remaining items blocks the bounded Case 60 claims above, and the case remains appropriately `grounded` rather than promoted by evidence volume alone.

---

## Sources

[^r700]: MIT Instrumentation Laboratory / Charles Stark Draper Laboratory, _MIT's Role in Project Apollo: Final Report on Contracts NAS 9-153 and NAS 9-4065, Volume III — Computer Subsystem_, Report R-700, August 1972, especially §2.3.6 and §3.5.2, pp. 46 and 90–92, plus the memory-module construction discussion around Figs. 3-33/3-34. Archived scan: https://www.ibiblio.org/apollo/Documents/R-700.pdf

[^nasa-sp8070]: NASA, _Spaceborne Digital Computer Systems — Space Vehicle Design Criteria_, NASA SP-8070, March 1971, §2.2.2 `Memory`. NTRS record: https://ntrs.nasa.gov/citations/19710024203 ; NTRS PDF: https://ntrs.nasa.gov/api/citations/19710024203/downloads/19710024203.pdf ; accessible historical HTML transcription: https://klabs.org/history/history_docs/sp-8070/ch2/2p2/2p2p2_memory.htm

[^mit-wired-patent]: Ramon L. Alonso, Robert E. Oleksiak, William B. Turner, `Process for manufacturing digital computer memories`, U.S. Patent 3,451,129, filed January 5, 1966, assigned to MIT. https://patents.google.com/patent/US3451129A/en

[^nelson]: Hayden A. Nelson, `Coincident current wired core memory for computers`, U.S. Patent 3,419,855, filed December 24, 1964. https://patents.google.com/patent/US3419855

[^nasa-1967-verification]: NASA Manned Spacecraft Center, Guidance Software Validation Committee, _Apollo Guidance Software — Development and Verification Plan_, October 4, 1967, especially summary pp. 2-1–2-2, §5.5 / §5.5.1, Fig. 5-1, and §7.1.1. Facsimile: https://www.ibiblio.org/apollo/hrst/archive/1695.pdf ; NASA Office of Logic Design index/transcription: https://klabs.org/history/history_docs/mit_docs/sw.htm

[^putterman]: Harry Putterman, `Non-destructive read-out memory`, U.S. Patent 3,432,834, filed April 23, 1965, published/granted March 11, 1969, assigned to General Precision Systems Inc. Google Patents: https://patents.google.com/patent/US3432834A/en

[^tomayko]: James E. Tomayko, _Computers in Spaceflight: The NASA Experience_, NASA Contractor Report CR-182505, March 1988, Apollo chapter especially pp. 38–39 and verification discussion around p. 48. NTRS record: https://ntrs.nasa.gov/citations/19880069935 ; optimized PDF: https://ntrs.nasa.gov/api/citations/19880069935/downloads/19880069935_Optimized.pdf