# Roadmap

The repository should grow from defensible cases outward. Do not begin with a total philosophy of storage.

## Phase 0 — Scaffold

- [x] Define project thesis and boundary with ordinary storage history.
- [x] Establish claim types and anti-anachronism rules.
- [x] Create initial prior-art map.
- [x] Create technical and philosophical spines.
- [x] Link related repositories.
- [ ] Add a compact controlled vocabulary / glossary.
- [ ] Add a case index and evidence-status convention.

## Phase 1 — Prove the method with contrasting cases

Choose cases that force the method to distinguish very different kinds of retention.

Recommended first set:

1. **Abacus / counting-board retained position**
   - test the `register-like` analogy without anachronism;
   - recover historical vocabulary and actual use;
   - distinguish operational intermediate state from durable record.

2. **Mercury delay-line memory**
   - retention as circulation;
   - time as access geometry;
   - continuous operation as apparent persistence.

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

A first synthesis should be attempted only after at least four of these cases have primary technical evidence.

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

## Phase 5 — Maintenance and invisible work

Study why persistence appears static even when it depends on activity.

Cases may include:

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
- [ ] mechanism described below the user-interface metaphor;
- [ ] maintenance requirements stated;
- [ ] failure / forgetting modes separated;
- [ ] modern analogy labeled as analogy;
- [ ] philosophical interpretation separated from historical record;
- [ ] counterexample or limit included;
- [ ] related-repository duplication checked.
