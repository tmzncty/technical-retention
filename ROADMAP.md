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
   - [x] first-pass case: [`cases/02-magnetic-core-destructive-read.md`](cases/02-magnetic-core-destructive-read.md);
   - [x] remanence as quiescent retention without periodic refresh;
   - [x] destructive read and rewrite as an access-cycle retention problem;
   - [x] establish primary vocabulary and mechanism through Forrester's 1951-filed patent;
   - [x] add contemporary evidence from Papian (1952) for remanent-flux retention under repeated nonselecting disturbances;
   - [x] add operational evidence from Widrow's 1953 MTC testing memorandum for safe operating margins and memory-cycle reliability;
   - [x] distinguish idle nonvolatility from read invariance;
   - [ ] inspect the patent PDF directly and add exact page / figure anchors;
   - [ ] inspect the full Papian 1952 IRE paper directly;
   - [ ] add a machine-specific primary MTC / Whirlwind document showing implemented read–restore sequencing;
   - [ ] add a narrow primary source on nondestructive-read core to bound the case;
   - [ ] promote from `first-pass` to `grounded` only after source deepening.

4. **DRAM**
   - [x] first-pass case: [`cases/03-dram-refresh-as-scheduled-restoration.md`](cases/03-dram-refresh-as-scheduled-restoration.md);
   - [x] use Dennard's 1967-filed patent to establish the one-transistor / one-capacitor retained state, leakage, destructive read, and periodic regeneration;
   - [x] distinguish **access-triggered restore** from **time-triggered regeneration**;
   - [x] record exact patent-page anchors for the central claims;
   - [x] use Intel 1103 manufacturer documentation as a boundary showing dynamic storage + nondestructive read + mandatory refresh;
   - [x] avoid treating Intel 1103 as an implementation of Dennard's exact 1T1C cell;
   - [ ] add an early commercial 1T1C datasheet/manual and primary sense-amplifier / restore evidence;
   - [ ] coordinate a full semiconductor-memory history with `computing-archaeology` rather than expanding this case into a general DRAM survey;
   - [ ] promote from `first-pass` to `grounded` only after source deepening.

5. **Flash / SSD**
   - erase blocks, endurance, ECC, FTL, wear leveling, garbage collection;
   - logical identity separated from physical location;
   - deletion versus physical persistence.

6. **Replicated object storage**
   - logical durability without privileged copy;
   - repair, quorum / consistency, versioning, erasure coding where appropriate;
   - probabilistic durability and institutional infrastructure.

A first synthesis should be attempted only after at least four of these cases have primary technical evidence and reach `grounded` status in [`CASE_INDEX.md`](CASE_INDEX.md).

### Results already exposed by Cases 00–03

The first four cases support several distinctions that should be tested across later systems:

> **state retention is not history retention.**

A system may keep a current state available for later use while preserving none of the sequence that produced it. Later cases should explicitly ask when separate logs, journals, snapshots, traces, or versions appear to retain history rather than only current state.

> **retention does not require one kind of physical persistence.**

An abacus state persists by remaining in place; a delay-line state persists by circulation, regeneration, and retiming; a magnetic-core state can remain as remanent magnetization after the selecting excitation is removed; a DRAM state can survive only for a bounded interval before regeneration.

> **logical identity can survive physical re-creation.**

The delay line shows identity through recurrent signal regeneration. Classic destructive-read core adds sensing followed by re-creation. DRAM adds scheduled regeneration of a decaying electrical state even when useful access has not occurred.

> **idle nonvolatility is not read invariance.**

Magnetic core exposes a useful distinction between a state remaining physically stable while unattended and a state remaining unchanged when accessed.

> **access can create maintenance work.**

Classic destructive-read core and Dennard's bounded 1T1C embodiment can require immediate restore after successful reading.

> **time can create maintenance work.**

DRAM adds a separate obligation: leakage creates a deadline, so the system must revisit retained state even when nobody asks to read it.

> **dynamic retention is not identical to destructive read.**

Dennard's patent disclosed nondestructive alternatives, and Intel 1103 documentation combines nondestructive read with mandatory periodic refresh. Later agents must keep `dynamic`, `destructive`, and `volatile` separate rather than using them as synonyms.

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
- Should the project distinguish **quiescent retention**, **continuous maintenance**, **access-triggered restoration**, and **deadline-driven maintenance** as controlled terms, or can the distinctions remain descriptive?

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

Case 02 adds access-mediated loss:

- destructive read without successful rewrite;
- half-select disturbance;
- sensing or drive failure while the magnetic material itself may remain capable of retention;
- surrounding-system drift outside a safe operating region.

Case 03 adds deadline-mediated loss:

- leakage beyond the recoverable interval;
- missed or late regeneration;
- sense error followed by restoration of the wrong logical value;
- temperature shortening a safe retention interval;
- failure of shared refresh/timing infrastructure affecting many cells.

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

The first four cases now provide four maintenance baselines:

- in the abacus, selection, interpretation, protection, reset, and validation remain visible operator labor;
- in the delay line, preservation, indexing, correction, and timing migrate into automatic circuitry and continuous process;
- in magnetic core, the element can retain state at rest while surrounding circuitry assumes maintenance obligations during selection, sensing, and restore;
- in DRAM, small per-bit state is made viable by shared sensing and a recurring schedule that revisits state before its physical deadline expires.

This shift among **human maintenance**, **continuous process maintenance**, **access-triggered restoration**, and **deadline-driven scheduled maintenance** should remain a major comparative axis.

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
