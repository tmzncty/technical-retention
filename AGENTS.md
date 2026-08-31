# AGENTS.md

Guidance for research agents working in `technical-retention`.

## Mission

Advance the question:

> **How does a state outlive the moment that produced it?**

Do not turn the repository into a generic storage-device encyclopedia.

## Before every research slice

Read:

1. `README.md`;
2. `ROADMAP.md`;
3. `docs/METHOD.md`;
4. `docs/PRIOR_ART.md`;
5. the relevant part of `docs/TECHNICAL_SPINE.md` or `docs/PHILOSOPHICAL_SPINE.md`;
6. `RELATED_REPOS.md`.

Then search related repositories before assuming a technical topic is uncovered.

## Required claim labels

Keep these layers distinct:

- **Historical record** — sourced claims about actors, artifacts, terminology, dates, and actual systems.
- **Engineering reconstruction** — mechanistic inference from documented design and constraints.
- **Philosophical interpretation** — conceptual analysis applied to the case.
- **Functional analogy** — cross-period or cross-technology comparison used heuristically.
- **Experiment** — model or reconstruction that exposes a mechanism.

Never make a functional analogy look like a historical continuity.

## Source priorities

Prefer:

1. original technical papers, manuals, patents, standards, datasheets, and archival documents;
2. museum or archival records tied to artifacts;
3. scholarly histories and peer-reviewed research;
4. reliable institutional retrospectives and oral histories;
5. technical books for reconstruction;
6. tertiary sources for discovery only.

For philosophy, verify exact text and edition where an argument depends on wording. Do not build a thesis on a loose quotation reproduced by secondary websites.

## Technical requirements for a case

Do not stop at capacity and speed. Recover:

- retained state;
- substrate;
- volatility;
- retention mechanism;
- maintenance / refresh / circulation / repair;
- addressing and access geometry;
- read semantics;
- write and erase semantics;
- latency and relevant timescales;
- failure modes;
- redundancy / ECC / reconstruction where relevant;
- identity and location semantics;
- migration;
- labor and infrastructure where relevant.

## Philosophical requirements

Do not use philosophy as decoration.

A philosophical section must identify:

1. the exact technical fact that creates the conceptual problem;
2. the concept being used;
3. what the concept clarifies;
4. where the analogy or interpretation stops.

Special warnings:

- `tertiary retention` is not automatically identical to computer memory;
- `Bestand` is not a synonym for storage;
- `archive`, `memory`, `storage`, `buffer`, and `register` are not interchangeable;
- `persistent` does not mean `maintenance-free`;
- `deleted` does not necessarily mean physically erased.

## Related-repository routing

### computing-archaeology

Use for detailed historical engineering accounts and constraint-first history. If a technical history already exists there, cite/link it rather than rewriting it here.

### problem-history

Use its anti-anachronism discipline when dealing with historical actors and changing problem formulations.

### mechanical-computing-playground

Prefer it for mechanism demonstrations and hands-on reconstructions when the experiment is more important than the philosophical argument.

## Preferred research unit

Use a bounded case study, not a giant sweep.

Good:

- destructive read in magnetic core as a retention problem;
- DRAM refresh as continuous maintenance;
- FTL mapping and logical identity;
- deletion semantics on copy-on-write storage;
- replica repair as persistence maintenance.

Too broad for one slice:

- history of all storage;
- philosophy of memory from Plato to cloud computing;
- every kind of RAM;
- all distributed databases.

## Writing style

English is the default working language, but bilingual or Chinese material is acceptable when sources or research needs make it useful. Accuracy and structure matter more than language consistency; translation can be done later.

## Contribution rule

A useful contribution should do at least one of these:

- add a strongly sourced case;
- repair a mistaken technical or historical claim;
- deepen prior art enough to change the project's novelty boundary;
- add a cross-mechanism comparison supported by mature cases;
- reveal a counterexample to a current thesis;
- clarify the division of labor with a related repository.

Do not add material merely because it mentions `memory`, `storage`, `archive`, or `time`.
