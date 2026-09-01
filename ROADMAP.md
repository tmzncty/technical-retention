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

### 1. Abacus / counting-board retained position

- [x] first-pass case: [`cases/00-abacus-retained-position.md`](cases/00-abacus-retained-position.md);
- [x] test the `register-like` analogy without anachronism;
- [x] recover an initial layer of historical vocabulary and actual use (`筭盤`, `定位`, positional instructions);
- [x] distinguish operational intermediate state from durable record;
- [ ] inspect the 1592 facsimile directly and record exact folio/page anchors;
- [ ] deepen counting-rod vocabulary and add a non-Chinese comparison;
- [ ] promote from `first-pass` to `grounded` only after source deepening.

### 2. Mercury delay-line memory

- [x] first-pass case: [`cases/01-mercury-delay-line-circulation.md`](cases/01-mercury-delay-line-circulation.md);
- [x] retention as circulation;
- [x] time as access geometry;
- [x] continuous operation as apparent persistence;
- [x] establish primary vocabulary through the 1947 Eckert–Mauchly `Memory system` patent and Wilkes's 1949 EDSAC report;
- [x] distinguish logical identity from identity of one physical pulse;
- [ ] add exact patent column / figure anchors and direct 1949 IRE page anchors;
- [ ] add machine-specific primary evidence for temperature control;
- [ ] promote from `first-pass` to `grounded` only after source deepening.

### 3. Magnetic core memory

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

### 4. DRAM

- [x] first-pass case: [`cases/03-dram-refresh-as-scheduled-restoration.md`](cases/03-dram-refresh-as-scheduled-restoration.md);
- [x] use Dennard's 1967-filed patent to establish the one-transistor / one-capacitor retained state, leakage, destructive read, and periodic regeneration;
- [x] distinguish **access-triggered restore** from **time-triggered regeneration**;
- [x] record exact patent-page anchors for the central claims;
- [x] use Intel 1103 manufacturer documentation as a boundary showing dynamic storage + nondestructive read + mandatory refresh;
- [x] avoid treating Intel 1103 as an implementation of Dennard's exact 1T1C cell;
- [x] add a commercial one-transistor/capacitor manufacturer source: AMD Am9050 (1976), including nondestructive read, leakage-driven refresh, and row-level 2 ms maintenance;
- [x] add primary commercial sense/restore evidence: AMD Am9016 (1979) sense-restore amplifiers and Intel AP-133 (1982) sense → amplify → return-to-cell row refresh;
- [x] grounding record: [`evidence/03-dram-1967-1982-grounding.md`](evidence/03-dram-1967-1982-grounding.md);
- [x] promote from `first-pass` to `grounded` after source deepening;
- [ ] coordinate a full semiconductor-memory history with `computing-archaeology` rather than expanding this case into a general DRAM survey.

### 5. Flash / SSD

- [x] first-pass case: [`cases/04-flash-virtual-mapping-logical-identity.md`](cases/04-flash-virtual-mapping-logical-identity.md);
- [x] use Ban / M-Systems US 5,404,485 (filed 1993) to establish block erase-before-write as the mapping problem;
- [x] establish virtual/logical/physical address separation and out-of-place update from primary patent evidence;
- [x] show that logical unit identity can remain stable while physical location changes;
- [x] distinguish a block marked `deleted` / not current from the later physical erase of its containing unit;
- [x] establish transfer/reclamation as copy-current-state → erase-old-unit → remap;
- [x] treat mapping/allocation metadata as retained state necessary to recover current identity;
- [x] add later ONFI endurance/ECC evidence without projecting it backward into the 1993 system;
- [ ] inspect the official patent PDF and add exact printed page / figure / column anchors;
- [ ] inspect the full Masuoka et al. 1987 IEDM paper directly;
- [ ] add an early Flash/NAND manufacturer datasheet with concrete program/erase/endurance semantics;
- [ ] recover the first defensible primary use / standardization of `Flash Translation Layer` terminology;
- [ ] add an early wear-leveling source; do not treat reclamation as automatically equivalent to wear leveling;
- [ ] treat TRIM/deallocation/secure erase as a separate later case with standards evidence;
- [ ] promote from `first-pass` to `grounded` only after source deepening.

### 6. Replicated object storage

- [x] bounded system chosen: 2006 Ceph/RADOS prototype rather than generic cloud storage;
- [x] first-pass case: [`cases/05-rados-replicated-object-repair.md`](cases/05-rados-replicated-object-repair.md);
- [x] establish object → placement group → ordered OSD placement through CRUSH and current cluster map;
- [x] establish primary-copy write ordering, per-object/PG versioning, and replica acknowledgement from the OSDI '06 primary paper;
- [x] distinguish **replica multiplicity** from **retained currentness**;
- [x] establish `down` / `out`, temporary primary transfer, re-replication, peering, and stale/missing-object recovery as a repair-triggered retention regime;
- [x] distinguish replicated volatile-cache acknowledgement from later persistent-media `commit` in the bounded design;
- [x] qualify `no privileged copy`: no permanently privileged physical home, while temporary primary authority still exists;
- [x] inspect the OSDI '06 PDF and record printed page / figure anchors;
- [x] inspect the full SC '06 CRUSH paper directly;
- [x] compare the 2007 RADOS paper to the OSDI prototype and record semantic changes rather than merging them silently;
- [x] add a contemporaneous implementation artifact for PG-log persistence/recovery;
- [x] grounding record: [`evidence/05-rados-2006-2007-grounding.md`](evidence/05-rados-2006-2007-grounding.md);
- [x] promote from `first-pass` to `grounded` after source deepening.

A first synthesis should be attempted only after at least four of these cases have primary technical evidence and reach `grounded` status in [`CASE_INDEX.md`](CASE_INDEX.md). Current maturity is **2 / 4 grounded**: DRAM and RADOS.

### Results already exposed by Cases 00–05

The first six cases support distinctions that should be tested across later systems:

> **state retention is not history retention.**

A system may keep a current state available for later use while preserving none of the complete sequence that produced it. Logs and recovery records can preserve bounded history without becoming a full archive of state transitions.

> **retention does not require one kind of physical persistence.**

An abacus state persists by remaining in place; a delay-line state persists by circulation, regeneration, and retiming; a magnetic-core state can remain as remanent magnetization; a DRAM state survives only for a bounded interval before regeneration; mapped Flash can preserve a logical identity while moving its physical embodiment; RADOS can preserve an object while the set of devices embodying it changes.

> **logical identity can survive physical re-creation, relocation, and member replacement.**

The delay line shows identity through recurrent signal regeneration. Classic destructive-read core adds sensing followed by re-creation. DRAM adds scheduled regeneration. Mapped Flash keeps one logical address current across physical relocation. RADOS extends this to distributed repair: a failed replica can be replaced by a newly reconstructed copy on another independently failing device.

> **idle nonvolatility is not read invariance.**

Magnetic core exposes a useful distinction between a state remaining physically stable while unattended and a state remaining unchanged when accessed.

> **access can create maintenance work.**

Classic destructive-read core and Dennard's bounded 1T1C embodiment can require immediate restore after successful reading.

> **time can create maintenance work.**

DRAM adds a separate obligation: leakage creates a deadline, so the system must revisit retained state even when nobody asks to read it.

> **refresh can be shared reconstruction rather than a per-cell timer event.**

Commercial DRAM evidence now makes the maintenance path concrete: row selection exposes weak stored charge to bit-line sensing, shared sense/restore circuitry amplifies the state, and the restored value is returned to the cells. The stable logical address is therefore maintained by shared temporal infrastructure around very small storage elements.

> **space and rewrite geometry can create maintenance work.**

Mapped Flash adds another regime: current data may need to be copied out so an erase unit can be reclaimed under free-space pressure.

> **failure and membership change can create maintenance work.**

RADOS adds repair-triggered retention: after an OSD remains unavailable, replica membership can change and current state is reconstructed onto another OSD to restore the intended redundancy/currentness relation.

> **dynamic retention is not identical to destructive read.**

Dennard's patent disclosed nondestructive alternatives; Intel 1103 documentation combines nondestructive read with mandatory periodic refresh; AMD's 1976 Am9050 directly combines a one-transistor/capacitor storage cell, nondestructive read, and mandatory refresh.

> **logical invalidation is not identical to physical erasure.**

Ban's mapping system can mark a block deleted / non-current before a later unit erase.

> **metadata can be part of what makes state persist as an identity.**

Mapped Flash requires mapping/allocation state; RADOS additionally requires current cluster-map/placement and version/recovery state to determine which replicas should exist and which state is current.

> **replica multiplicity is not identical to retained currentness.**

Distributed copies can disagree or become stale. Currentness requires ordering, version state, authority rules, and recovery semantics in addition to physical duplication.

> **logical success is not identical to durable commit.**

The bounded 2006 RADOS design exposes multiple retention thresholds: an update may be ordered, replicated into volatile caches and acknowledged, then only later receive final persistent-media commit.

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

The mapped-Flash case does **not** close the general SSD/FTL bridge. The RADOS case does **not** close the general distributed-storage bridge. The grounded DRAM case likewise does **not** close the general semiconductor-memory bridge. These cases establish bounded mechanisms whose broader technical history should be coordinated with `computing-archaeology`.

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
- Should the project distinguish **quiescent retention**, **continuous maintenance**, **access-triggered restoration**, **deadline-driven maintenance**, **capacity/reclaim-triggered maintenance**, and **failure/repair-triggered maintenance** as controlled terms?
- When a mapping layer moves state, is the retained object best described as data, address, relation, or all three?
- When replicas disagree, is `currentness` itself retained metadata/protocol state?
- How should `acknowledged`, `visible`, `replicated`, and `durably committed` be separated across systems?

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
- metadata loss;
- key destruction;
- bit rot;
- controller failure;
- replica loss;
- replica staleness;
- loss of enough current replicas/recovery history to establish state;
- placement / membership-state loss;
- correlated failure;
- format / software obsolescence;
- institutional abandonment.

Goal: replace the single word `forgetting` with a mechanism-sensitive vocabulary.

Cases 00–05 already expose distinct failure families: interpretive/context loss; loss of circulation/timing; destructive-access loss; missed refresh deadlines; mapping/reclamation loss; and distributed replica/currentness/recovery failure.

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

The first six cases now provide six maintenance baselines:

- abacus: selection, interpretation, protection, reset, and validation remain visible operator labor;
- delay line: preservation, correction, circulation, and timing become continuous process;
- magnetic core: the element retains state at rest while access can trigger restore work;
- DRAM: a recurring schedule revisits state before its physical deadline expires, using shared row selection and sense/restore circuitry in the grounded commercial evidence;
- mapped Flash: controller metadata, free space, relocation, and reclamation sustain repeated logical rewriting;
- RADOS: failure detection, peering, version comparison, primary transfer, and re-replication sustain logical objects despite member-device loss.

This shift among **human maintenance**, **continuous process maintenance**, **access-triggered restoration**, **deadline-driven scheduled maintenance**, **capacity/reclaim-triggered maintenance**, and **failure/repair-triggered maintenance** should remain a major comparative axis.

## Phase 6 — Philosophical synthesis

Only after technical cases are mature:

- test Stiegler's tertiary retention against different machine retention regimes;
- test whether Heideggerian availability / ordering is clarified by addressability and storage infrastructures;
- compare Ernst's operational / microtemporal account with long-duration preservation;
- extend Kirschenbaum's forensic materiality through Flash, remapping, copy-on-write, encryption, and distributed storage;
- test whether distributed `currentness` and repair require a more explicitly relational account of retained identity;
- decide whether `technical retention` names one coherent operation or a family of related mechanisms.

The mapped-Flash and RADOS cases are especially relevant to later synthesis because both separate logical identity from one stable physical location, but they do so at very different failure/authority scales. Grounded DRAM adds a complementary case in which logical continuity is maintained through repeated local electrical reconstruction under a deadline. Do not perform the synthesis yet.

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
