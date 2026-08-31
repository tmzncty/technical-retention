# Method

`technical-retention` compares very different mechanisms without pretending that they are historically or technically identical.

The project therefore uses a layered method.

## 1. Five claim types

Every substantial claim should be identifiable as one of these.

### A. Historical record

What surviving primary sources, artifacts, patents, manuals, engineering papers, standards, archives, oral histories, and reliable scholarship establish about a particular time and place.

Examples:

- a machine used mercury delay-line memory;
- a DRAM device required refresh according to its datasheet;
- a disk controller exposed a particular geometry;
- a vendor described a storage system using a particular term.

Historical record must not be silently replaced by a later textbook reconstruction.

### B. Engineering reconstruction

What follows from the mechanism even when a historical actor did not explicitly formulate it in the same way.

Examples:

- recirculating delay-line storage makes waiting part of addressability;
- destructive read requires restoration somewhere in the operational cycle;
- a mapping layer can preserve a logical block identity while changing its physical location.

Engineering reconstruction must state its assumptions and should use period-realistic constraints where historical interpretation depends on them.

### C. Philosophical interpretation

A reading of a technical case through a philosophical or media-theoretical problem: retention, exteriorization, temporality, availability, inscription, forgetting, repetition, identity, or maintenance.

This layer is not allowed to overwrite the mechanism.

### D. Functional analogy

A comparison across unlike systems that isolates one function.

Example:

> An abacus bead configuration can be treated as `register-like` because a numerical state remains available between operations.

This does **not** mean an abacus is historically a CPU register or that its users possessed the modern concept.

Functional analogies must always be labeled.

### E. Experiment

A reconstruction, simulation, executable model, replica, or thought experiment that makes one retention constraint visible.

Experiments demonstrate mechanisms or consequences. They do not prove historical intent.

---

## 2. Anti-anachronism rule

Borrow the central discipline of [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history):

> Do not assume that because we can formulate a problem today, historical actors were asking the same problem in the same vocabulary.

For every pre-modern or early technical case, separate:

1. what actors called the object or operation;
2. what problem they explicitly understood themselves to be solving;
3. what a modern engineering description can reconstruct;
4. what later philosophical comparison adds.

A useful analogy is not evidence of conceptual continuity.

---

## 3. Mechanism-first comparison

Before philosophical interpretation, answer the technical questions.

### Retained state

- What changes physically?
- What remains invariant enough to count as a state?
- Is the state discrete, continuous, symbolic, geometric, magnetic, electrical, optical, mechanical, chemical, or distributed?

### Retention work

- Does the state remain without intervention?
- Does it require power?
- Does it require circulation?
- Refresh?
- Error correction?
- Servo control?
- Environmental control?
- Remapping?
- Replication?
- Human maintenance?

### Access

- How is a retained state located?
- Sequentially?
- Spatially?
- By address?
- By content?
- By index?
- By timing?
- Through a controller or mapping layer?

### Read / write / erase

- Is reading destructive or nondestructive?
- Does writing overwrite in place?
- Is erasure local or block-wide?
- Is deletion physical destruction, metadata change, loss of reference, key destruction, or policy state?

### Failure and forgetting

- leakage;
- drift;
- mechanical wear;
- media damage;
- noise;
- bit errors;
- controller failure;
- lost mapping metadata;
- incompatible interfaces or formats;
- failed replication;
- loss of encryption key;
- institutional abandonment.

Do not collapse these into one generic category called `data loss`.

---

## 4. Source hierarchy

Prefer, roughly in this order:

1. primary technical documentation from the relevant period;
2. surviving artifacts and museum documentation tied to provenance;
3. patents and original engineering papers;
4. standards and vendor manuals;
5. scholarly history of computing / media / technology;
6. high-quality institutional retrospectives and oral histories;
7. textbooks and technical retrospectives for reconstruction;
8. tertiary web sources only for navigation.

For philosophy and media theory, cite primary philosophical texts where possible and use scholarship to establish interpretive disputes rather than pretending one reading is uncontested.

---

## 5. Cross-repository reuse

Before writing a technical history from scratch, search [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology).

If that repository already has a defensible mechanism history:

- link to it;
- summarize only what is needed here;
- add the retention-specific comparison here;
- submit corrections to the source repository when the correction concerns its own technical history.

Experiments that mainly demonstrate mechanical or historical computing mechanisms may belong in [`tmzncty/mechanical-computing-playground`](https://github.com/tmzncty/mechanical-computing-playground).

---

## 6. Case-study structure

Use [`CASE_TEMPLATE.md`](CASE_TEMPLATE.md).

A strong case should contain:

1. object and date range;
2. historical vocabulary;
3. retained state and substrate;
4. retention mechanism;
5. addressing and access;
6. read/write/erase semantics;
7. maintenance and labor;
8. failure and forgetting;
9. historical evidence;
10. engineering reconstruction;
11. philosophical interpretation;
12. functional analogies, if any;
13. counterexamples and limits;
14. links to related repositories.

---

## 7. Grand synthesis comes last

Do not begin by declaring that all storage is memory, all memory is technics, or all technical availability is `Bestand`.

The project earns synthesis by accumulating cases in which conceptual claims survive detailed technical comparison.
