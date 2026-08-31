# Roadmap

The repository should grow from defensible cases outward. Do not begin with a total philosophy of storage.

## Phase 0 — Scaffold

- [x] Define project thesis and boundary with ordinary storage history.
- [x] Establish claim types and anti-anachronism rules.
- [x] Create initial prior-art map.
- [x] Create technical and philosophical spines.
- [x] Link related repositories.
- [x] Add a compact controlled vocabulary / glossary.
- [x] Add a case index and evidence-status convention.

Phase 0 is complete. Future scaffold changes should be driven by failures discovered in actual cases rather than by adding more abstract categories in advance.

## Phase 1 — Prove the method with contrasting cases

Choose cases that force the method to distinguish very different kinds of retention.

Recommended first set:

1. **Abacus / counting-board retained position**
   - [x] first-pass case: [`cases/00-abacus-retained-position.md`](cases/00-abacus-retained-position.md);
   - [x] test the `register-like` analogy without anachronism;
   - [x] recover an initial layer of historical vocabulary and actual use (`筭盤`, `定位`, positional instructions);
   - [x] distinguish operational intermediate state from durable record;
   - [ ] inspect the 1592 facsimile directly and record exact folio/page anchors;
   - [ ] deepen counting-rod vocabulary and add a non-Chinese comparison;
   - [ ] promote from `first-pass` to `grounded` only after source deepening.

2. **Mercury delay-line memory**
   - [x] first-pass case: [`cases/01-mercury-delay-line-circulation.md`](cases/01-mercury-delay-line-circulation.md);
   - [x] retention as circulation;
   - [x] time as access geometry;
   - [x] continuous operation as apparent persistence;
   - [x] establish primary vocabulary through the 1947 Eckert–Mauchly `Memory system` patent and Wilkes's 1949 EDSAC report;
   - [x] distinguish logical identity from identity of one physical pulse;
   - [ ] add exact patent column / figure anchors and direct 1949 IRE page anchors;
   - [ ] add machine-specific primary evidence for temperature control;
   - [ ] promote from `first-pass` to `grounded` only after source deepening.

3. **Magnetic core memory**
   - remanence;
   - destructive read and rewrite;
   - nonvolatility without effortless access.

4. **DRAM**
   - retention as scheduled refresh;
   - stable addresses over unstable charge;
   - hierarchy and latency.

5. **Flash / SSD**
   - erase blocks, endurance, ECC, FTL, wear leveling, garbage collection;
   - logical identity separated from physical location;
   - deletion versus physical persistence.

6. **Replicated object storage**
   - logical durability without privileged copy;
   - repair, quorum / consistency, versioning, erasure coding where appropriate;
   - probabilistic durability and institutional infrastructure.

A first synthesis should be attempted only after at least four of these cases have primary technical evidence and reach `grounded` status in [`CASE_INDEX.md`](CASE_INDEX.md).

### Results already exposed by Cases 00–01

The first two cases support several distinctions that should be tested across later systems:

> **state retention is not history retention.**

A system may keep a current state available for later use while preserving none of the sequence that produced it. Later cases should explicitly ask when separate logs, journals, snapshots, traces, or versions appear to retain history rather than only current state.

> **retention does not require physical stillness.**

An abacus state persists by remaining in place; a delay-line state persists by circulation, regeneration, and retiming.

> **logical identity can survive physical re-creation.**

The delay line already shows a weak but important form of substrate discontinuity: a stable logical pattern can persist through successive regenerated physical signals.

## Phase 2 — Build the missing technical bridges

Coordinate with `computing-archaeology` rather than duplicating it.

Priority bridges:

- latch / flip-flop / register;
- SRAM and cache;
- DRAM evolution and refresh machinery;
- ROM → PROM → EPROM → EEPROM → Flash;
- HDD geometry and remapping;
- virtual memory;
- file-system crash consistency;
- SSD FTL and controller-mediated persistence;
- RAID / scrubbing / rebuild;
- distributed replication and erasure coding.

## Phase 3 — Retention / transfer / computation boundary

Research problems:

- When is a buffer `storage`?
- When does transfer become retention across time?
- How much delay is required before we intuitively call a state stored?
- When does a retained state become part of computation rather than merely input/output?
- How do cache and memoization complicate the boundary?
- What is the difference between state, memory, store, archive, log, file, record, and trace?
- Does `working retention` name a useful cross-period category, or is it too broad?
- Does `recurrence` deserve a separate controlled term from `refresh`?

This phase should engage Ernst directly and use concrete mechanisms rather than terminology alone.

## Phase 4 — Technical forgetting

Build a comparative map of:

- decay;
- power loss;
- refresh failure;
- overwrite;
- erase;
- logical deletion;
- garbage collection;
- loss of index;
- key destruction;
- bit rot;
- controller / metadata loss;
- media obsolescence;
- format / software obsolescence;
- institutional abandonment.

Goal: replace the single word `forgetting` with a mechanism-sensitive vocabulary.

Case 00 already adds two non-destructive physical-loss modes that later cases should preserve where applicable:

- loss of interpretation while the physical state survives;
- loss of procedural context while the represented value remains readable.

Case 01 adds process-failure modes:

- loss of circulation;
- timing drift;
- failed regeneration;
- environmental drift that destroys the timing relation even though the apparatus remains physically present.

## Phase 5 — Maintenance and invisible work

Study why persistence appears static even when it depends on activity.

Cases may include:

- human preservation and interpretation of working state;
- refresh logic;
- storage controllers;
- ECC;
- disk servo systems;
- SSD firmware;
- data scrubbing;
- RAID rebuild;
- distributed anti-entropy / repair;
- tape migration;
- backup operators;
- archival format migration;
- data-center facilities.

Coordinate labor and manufacturing evidence with existing repositories where relevant.

The first two cases already form a useful baseline:

- in the abacus, selection, interpretation, protection, reset, and validation remain visible operator labor;
- in the delay line, preservation, indexing, correction, and timing migrate into automatic circuitry.

This shift from **visible human maintenance** to **hidden machine maintenance** should remain a major comparative axis.

## Phase 6 — Philosophical synthesis

Only after technical cases are mature:

- test Stiegler's tertiary retention against different machine retention regimes;
- test whether Heideggerian availability / ordering is clarified by addressability and storage infrastructures;
- compare Ernst's operational / microtemporal account with long-duration preservation;
- extend Kirschenbaum's forensic materiality through Flash, remapping, copy-on-write, encryption, and distributed storage;
- decide whether `technical retention` names one coherent operation or a family of related mechanisms.

## Research quality gates

Before marking a major case mature:

- [ ] historical vocabulary recovered;
- [ ] at least one strong primary technical source where available;
- [ ] exact source location recorded for central primary claims;
- [ ] mechanism described below the user-interface metaphor;
- [ ] maintenance requirements stated;
- [ ] failure / forgetting modes separated;
- [ ] modern analogy labeled as analogy;
- [ ] philosophical interpretation separated from historical record;
- [ ] counterexample or limit included;
- [ ] related-repository duplication checked.
