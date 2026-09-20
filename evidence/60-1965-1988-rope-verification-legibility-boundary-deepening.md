# Case 60 Evidence Deepening — Core-Rope Verification, Rework, and Legibility Boundaries (1965–1988)

**Status:** `bounded deepening complete`

## Scope

This slice deepens [`../cases/60-apollo-core-rope-wired-topology.md`](../cases/60-apollo-core-rope-wired-topology.md) at one deliberately narrow boundary:

> once a program has been manufactured into a physically fixed rope, what still has to be demonstrated before that artifact can be treated as the correct, readable program?

The question is not whether Apollo core rope was nonvolatile. Case 60 already establishes that the program bit is carried by manufactured wire/core topology rather than by a remanent magnetic bit state. The narrower issue here is that **topological persistence does not collapse three other predicates**:

1. the topology was manufactured to the intended bit pattern;
2. the manufactured artifact can be read through a usable electrical signal path;
3. the artifact is the approved/current program for the intended flight configuration.

This slice uses three evidence roles that must not be confused:

- the **October 4, 1967 NASA software-development and verification plan** as a contemporary normative process record;
- **Harry Putterman's April 23, 1965 patent application, published March 11, 1969 as US3432834A**, as a contemporary competing-design / prior-art problem-framing witness;
- **James E. Tomayko, _Computers in Spaceflight: The NASA Experience_, NASA-CR-182505 (March 1988)** as a later NASA-sponsored institutional synthesis describing Raytheon factory checking and the practical rework boundary.

The last source is valuable but retrospective. It is not substituted for a Raytheon shop traveler, acceptance-test procedure, discrepancy report, or mission-specific anomaly record.

A fresh search of `tmzncty/computing-archaeology` for `core rope Raytheon delivery tape` found no dedicated reusable packet. Broader Apollo manufacturing history, vendor genealogy, and general core-rope engineering archaeology remain companion-repository work.

---

## Source identity and chronology

### 1965 application / 1969 publication — Harry Putterman, US3432834A

Google Patents records:

- title: **`Non-destructive read-out memory`**;
- inventor: **Harry Putterman**;
- original assignee: **General Precision Systems Inc.**;
- filing / priority date: **April 23, 1965**;
- publication / grant date: **March 11, 1969**.

The filing date and publication date are kept separate. The application is a contemporary primary record of what the inventor chose to describe as prior art and as a problem his design sought to improve. It is not an independent Apollo qualification report.

### 1967 — NASA Manned Spacecraft Center verification plan

The existing Case 60 evidence packet already grounds the NASA plan dated **October 4, 1967**. It requires the approved fixed-memory program and manufactured flight fixed memory to be compared **bit for bit**, with formal MSC acceptance/certification and later configuration control.

That source establishes the normative correspondence requirement.

### 1988 — NASA-CR-182505

NASA NTRS identifies James E. Tomayko's **_Computers in Spaceflight: The NASA Experience_** as:

- NASA Contractor Report **CR-182505**;
- author: **James E. Tomayko**, Wichita State University;
- publication date: **March 1, 1988**;
- prepared under NASA contract **NASW-3714**.

Its Apollo chapter is a retrospective historical synthesis, not a contemporary manufacturing instruction. For this slice it is used to show how the production/correction boundary was later reconstructed from NASA/contractor records and interviews.

---

## Historical record

### 1. The 1967 plan treats manufacture and acceptance as separate states

The October 4, 1967 NASA plan does not equate `program approved` with `flight rope accepted`.

Its fixed-memory process distinguishes:

```text
approved software
    -> hard-memory fabrication
    -> rope check / acceptance comparison
    -> formal acceptance / certification
```

Section 5.5.1 requires procedures that make the approved program delivered by the software contractor **identical bit for bit** to the manufactured flight fixed memory. Figure 5-1 separately depicts manufacture and checking paths.

Historical consequence:

```text
manufactured
!= verified against approved program
!= accepted/certified for flight
```

This is a process distinction directly present in the contemporary NASA record.

### 2. Tomayko's NASA history describes actual factory comparison against the delivery tape

Tomayko's 1988 Apollo chapter says software intended for core rope had to be delivered early enough for the rope to be **manufactured and tested**. It further states that Raytheon could eliminate **hard-wiring errors introduced during manufacture** by testing rope modules against the **delivery tape of the programs**, and that the company built a device to perform this comparison.

The same passage says errors found before a rope system was complete could be corrected at the factory, while later corrections became much harder.

For Case 60, this adds an implementation-level institutional witness to the 1967 normative plan:

```text
reference program representation
    -> manufactured topology
    -> read/test manufactured module
    -> compare with delivery representation
    -> correct manufacturing divergence while rework is still available
```

The source does not supply the electrical schematic, algorithm, sampling policy, exact device name, failure thresholds, or shop traveler for that comparison apparatus.

### 3. Factory rework and post-installation change are different operations

Tomayko also emphasizes the practical boundary created by sealing/installing the rope. Once manufactured, changing the stored program was difficult because changing bits required physical rewiring; errors discovered early in the fabrication cycle could be corrected at the factory, while later software errors could require operational workarounds or a new/reworked memory artifact.

This is consistent with NASA SP-8070's earlier report that Apollo program changes could require roughly a **four-week** new-module production cycle and that verification cycles were at least as long.

The important historical distinction is not `rope is absolutely immutable`. It is:

```text
before final manufacture / acceptance:
physical rework remains part of the production process

normal installed operation:
ordinary software execution has no write authority over rope contents

later program revision:
requires controlled physical replacement/rework + renewed verification
```

`Read-only` is therefore an operational interface property, not a claim that humans literally cannot change the artifact.

### 4. A 1965 competing patent identifies readout noise as a distinct core-rope design problem

Putterman's patent description explicitly names the **Apollo Computer** as using an MIT-designed core-rope memory and treats core rope as an already existing `wired-in memory` class.

The patent says core rope had found acceptance in airborne applications because of low component count, but then criticizes its operational reliability on the ground that interrogation required a **multitude of current pulses** that generated noise. Its example says a 512-word core-rope memory required coincidence of **nine currents**.

This is useful contemporary evidence for one bounded claim:

> engineers in 1965 could describe the persistence of the wired program and the electrical reliability of retrieving it as different design questions.

But the wording is part of a patent whose purpose is to motivate the inventor's alternative NDRO design. It is therefore **not** treated as an independently measured Apollo failure rate, qualification result, or proof that the final Block II flight rope was unreliable.

The 512-word / nine-current / roughly `100 kilocycles` example is kept attached to Putterman's described prior-art example. This slice does not silently map those figures onto every Apollo rope revision or the final Block II implementation.

### 5. Putterman's own alternative makes the same distinction visible from another direction

The patent's proposed memory still uses magnetic cores and wired reset paths, but it devotes substantial detail to signal/noise behavior, half-selected cores, bias current, current accuracy, and temperature range.

That matters here only as a period engineering witness:

```text
fixed-program embodiment
    does not remove
signal-margin / sensing / selection engineering
```

The patent's claims for its own improved design are inventor assertions unless separately validated. They are not used as Apollo measurements.

---

## Engineering reconstruction

The following is modern analytical language, not claimed as NASA, MIT, Raytheon, or General Precision Systems period terminology.

### Finding 1 — durable topology is not self-verifying topology

A wire routed through the wrong core can be extremely stable and still encode the wrong bit.

Therefore:

```text
physical persistence of manufactured relation
!= correctness of manufactured relation
```

The bit-for-bit comparison requirement and Tomayko's factory-test account exist precisely because fixedness does not prove correct manufacture.

### Finding 2 — payload persistence and legibility are separate retention relations

The payload can remain physically embodied while the read path becomes unable to recover it correctly.

Case 60 already records open/short sense or inhibit wiring and associated-diode failure as relevant failure modes. Putterman's contemporary critique adds a different category: even without changing the intended wire topology, a read architecture can face signal/noise and current-coincidence constraints.

Thus:

```text
payload-bearing topology survives
    +
selection/read channel remains within usable margins
    -> readable logical program
```

Neither predicate subsumes the other.

### Finding 3 — verification evidence is not the payload

The delivery tape, approved software configuration, check path, and acceptance record are evidence **about** the manufactured rope. They are not themselves the flight rope payload.

So a fuller retention relation is:

```text
artifact payload
!= reference representation
!= comparison result
!= acceptance authority
```

The system can preserve the first while losing evidence for the others; conversely, preserving an old reference tape does not make a damaged or replaced flight artifact readable.

### Finding 4 — rework authority has a lifecycle window

During manufacture, changing a routing error can be ordinary rework. After sealing, acceptance, installation, and mission integration, the same logical change becomes much more expensive and may require replacement, renewed testing, configuration approval, or an operational workaround.

This suggests a lifecycle state machine:

```text
program definition
    -> fabrication-in-progress
        -> correction/rework still locally admissible
    -> manufactured artifact
        -> compare against reference
    -> accepted/certified artifact
        -> configuration-controlled
    -> installed flight artifact
        -> ordinary runtime has read-only authority
```

The physical possibility of rewiring has not vanished; the **authorized and economical change path** has changed.

### Finding 5 — low runtime mutability can increase the value of predeployment evidence

Core rope strongly suppresses accidental runtime overwrite. That does not eliminate correctness work. It moves more of the burden to:

- source/program verification;
- controlled manufacturing inputs;
- fabrication inspection;
- readback/comparison;
- acceptance/certification;
- configuration control.

Hence:

```text
reduced runtime write authority
!= reduced lifecycle verification burden
```

### Finding 6 — `reliable retention` is conjunctive, not one property

For the bounded Apollo rope case, a useful reconstruction is:

```text
retained program usable for flight
=
physical bit-defining topology survives
AND selection/read path remains usable
AND manufactured contents correspond to approved program
AND artifact remains the authorized/current configuration
```

These conditions can fail independently.

---

## Controlled functional comparisons

### Case 70 — magnetic-core half-select disturbance and margin

Case 70 studies ordinary core-memory state whose readable correctness depends on current margins and disturbance behavior. Case 60 differs because the program bit is topological rather than a remanent core polarity.

The bounded comparison is only:

```text
information-bearing state can survive
while read/selection margin becomes the limiting relation
```

No shared circuit, lineage, or identical failure mode is asserted.

### Case 62 — IBM transformer read-only storage

Case 62 is another manufactured/read-only transformer-memory case. A useful functional comparison is that `runtime fixed` does not mean `manufacturing transfer requires no verification`.

This slice does not establish a NASA↔IBM genealogy.

### Later ROM / firmware programming

A later manufactured ROM or firmware image may likewise distinguish source artifact, programmed physical artifact, readback/verification evidence, and deployment authorization.

That is a functional analogy only. Apollo rope is not retroactively described as secure boot, cryptographic signing, reproducible builds, or modern firmware attestation.

---

## Philosophical / media-theoretical interpretation — bounded

One limited interpretation follows from the engineering evidence:

> **persistence of inscription is not identical to legibility of inscription.**

The wire/core relation can endure while a sensing path fails, while a manufacturing mistake preserves the wrong relation, or while the artifact loses configuration authority.

This is not evidence that NASA, MIT, Raytheon, or Putterman used the philosophical category `legibility`. It is a project-level interpretation of the separated engineering predicates.

A second bounded interpretation is that making information physically difficult to alter does not remove mediation. It often increases dependence on records and procedures that establish correspondence between representations.

That conclusion should remain downstream of the historical process evidence.

---

## Explicit non-claims

This slice does **not** claim that:

1. Putterman's patent independently measured Apollo flight-computer reliability;
2. the patent's phrase `not very reliable` is accepted here as an objective verdict on the final Block II AGC;
3. the 512-word / nine-current example describes every Apollo rope revision;
4. the patent's performance claims for its own NDRO design were independently validated here;
5. the patent proves that General Precision Systems influenced MIT/Raytheon design decisions;
6. the patent proves that MIT/Raytheon influenced Putterman's claimed invention beyond the explicit prior-art description;
7. any direct genealogy between Putterman's design and Apollo core rope has been established;
8. Tomayko's 1988 synthesis is a contemporary Raytheon manufacturing procedure;
9. Tomayko's sentence about a factory comparison device identifies its complete implementation;
10. the factory test guaranteed detection of every possible manufacturing defect;
11. bit-for-bit agreement guaranteed the semantic correctness of the approved software;
12. bit-for-bit agreement guaranteed the absence of latent electrical or mechanical faults;
13. a sealed or accepted rope was physically impossible to rework;
14. every late software defect required manufacturing a completely new rope rather than any other controlled response;
15. the four-week SP-8070 figure was a universal manufacturing duration for all ropes and missions;
16. a stable physical rope was necessarily readable after every associated circuit failure;
17. signal/noise limitations imply that the retained topology itself had decayed;
18. a reference tape or acceptance record is part of the runtime payload stored in rope;
19. Apollo rope verification was equivalent to modern cryptographic attestation;
20. Apollo established later ROM/firmware verification practice;
21. a `read-only` interface removes all human or manufacturing authority to change the artifact;
22. `fixed memory` and `high reliability` are synonyms;
23. this slice settles the invention priority of core-rope or wired-in memory;
24. the NASA history closes the need for mission-specific anomaly, rework, discrepancy, or acceptance records;
25. all of the 1988 history's underlying footnote sources have been independently inspected in this slice.

---

## Claim ledger

| Claim | Type | Evidence strength | Status |
| --- | --- | --- | --- |
| NASA's 1967 plan required a distinction between approved software, hard-memory fabrication, comparison, and flight acceptance/certification | H/P | direct contemporary NASA process record | supported |
| The manufactured fixed memory was to match the approved program bit for bit | H/P | direct §5.5.1 evidence | supported |
| Tomayko reports that Raytheon tested manufactured rope modules against the delivery tape and built a device for that purpose | H/R | strong NASA-sponsored retrospective institutional synthesis | supported, retrospective |
| Tomayko reports factory-stage correction of hard-wiring errors and a narrower correction window after completion | H/R | NASA-sponsored retrospective synthesis | supported, retrospective |
| Putterman's 1965-filed patent explicitly identifies Apollo/MIT core rope as existing wired-in memory prior art | H/P | direct contemporary patent description | supported |
| Putterman problem-frames core-rope interrogation noise from multiple current pulses and gives a 512-word / nine-current example | H/P | direct patent text | supported as inventor/problem framing |
| Putterman's critique proves final Block II Apollo rope had an unacceptable reliability rate | X | no independent qualification/failure evidence | rejected |
| Durable topology can still encode the wrong bit if manufactured incorrectly | E | direct inference from bit-for-bit checking and hard-wiring-error correction | supported |
| Correct topology and readable signal path are distinct predicates | E | mechanism + patent problem framing + existing failure modes | supported, bounded |
| Reference representation, comparison evidence, and acceptance authority are distinct from the flight payload | E | reconstruction from production/certification chain | supported |
| The authorized/economical ability to change a fixed artifact narrows across manufacture→acceptance→installation | E | reconstruction from factory rework + configuration-control evidence | supported, bounded |
| Persistence of inscription is not identical to legibility of inscription | I | philosophical abstraction from engineering distinction | bounded interpretation |
| Apollo rope verification was historically equivalent to modern firmware attestation | A/X | functional analogy only | rejected as historical identity |

---

## Navigation consequence

This slice closes a narrower part of Case 60's existing `mission-specific rope anomaly, acceptance-test, rework, or configuration-change records` debt:

- the repository now has a NASA-sponsored historical witness that **Raytheon compared manufactured rope modules against the program delivery tape and could correct hard-wiring errors during the factory window**;
- it also has a contemporary competing-patent witness that **wired-program persistence and electrical readout quality were treated as separate engineering problems**.

The debt is **not fully closed**. Still valuable are:

1. direct Raytheon shop procedures, acceptance-test equipment drawings, travelers, discrepancy reports, or rework records;
2. mission/program-specific rope mismatch, late-change, or installed-rope anomaly records;
3. the underlying archival sources behind Tomayko's footnotes 58–59;
4. a directly inspectable acceptance test showing exact comparison granularity and failure disposition;
5. a direct AGC qualification source quantifying fixed-memory signal/noise margin or read-channel rejection criteria.

Case 60 should therefore remain `grounded`, not be promoted solely because this bounded slice was added.

---

## Sources

1. **NASA Manned Spacecraft Center, Guidance Software Validation Committee, _Apollo Guidance Software — Development and Verification Plan_, October 4, 1967.** Especially §5.5 / §5.5.1, Figure 5-1, and §7.1.1. Facsimile: https://www.ibiblio.org/apollo/hrst/archive/1695.pdf ; NASA Office of Logic Design index/transcription: https://klabs.org/history/history_docs/mit_docs/sw.htm
2. **Harry Putterman, `Non-destructive read-out memory`, U.S. Patent 3,432,834, filed April 23, 1965, published/granted March 11, 1969, assigned to General Precision Systems Inc.** Google Patents: https://patents.google.com/patent/US3432834A/en
3. **James E. Tomayko, _Computers in Spaceflight: The NASA Experience_, NASA Contractor Report CR-182505, March 1988.** NTRS record: https://ntrs.nasa.gov/citations/19880069935 ; optimized PDF: https://ntrs.nasa.gov/api/citations/19880069935/downloads/19880069935_Optimized.pdf . Relevant Apollo discussion is around pp. 38–39 and the verification discussion around p. 48.
4. **NASA, _Spaceborne Digital Computer Systems — Space Vehicle Design Criteria_, NASA SP-8070, March 1971.** NTRS: https://ntrs.nasa.gov/citations/19710024203
5. **Case 60 canonical and existing grounding packets.** [`../cases/60-apollo-core-rope-wired-topology.md`](../cases/60-apollo-core-rope-wired-topology.md)

---

## Evidence status

**`bounded deepening complete`.**

The new evidence supports a precise retention boundary: a manufactured program can be physically fixed yet still require independent correspondence checking, can still be wrong because of fabrication divergence, and can still depend on a separate read/selection channel whose quality is not guaranteed merely by payload persistence. The direct factory procedure and mission-specific anomaly record remain open evidence work.