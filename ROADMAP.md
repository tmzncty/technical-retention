# Roadmap

The repository should grow from defensible cases outward. Do not begin with a total philosophy of storage.

`CASE_INDEX.md` is the authoritative case-maturity ledger. This roadmap records what to do next rather than duplicating every established claim.

## Phase 0 — Scaffold — complete

- [x] Define project thesis and boundary with ordinary storage history.
- [x] Establish claim types and anti-anachronism rules.
- [x] Create initial prior-art map.
- [x] Create technical and philosophical spines.
- [x] Link related repositories.
- [x] Add a compact controlled vocabulary / glossary.
- [x] Add a case index and evidence-status convention.

Future scaffold changes should be driven by failures discovered in actual cases rather than by adding abstract categories in advance.

---

## Phase 1 — Prove the method with contrasting cases

### 1. Abacus / counting-board retained position — `grounded`

- [x] bounded case: [`cases/00-abacus-retained-position.md`](cases/00-abacus-retained-position.md);
- [x] test the `register-like` analogy without anachronism;
- [x] recover period vocabulary and actual use (`算盤`, `定位`, positional instructions);
- [x] distinguish operational current state from durable/history retention;
- [x] inspect a 1592 facsimile directly: Source Library digital scan p. 70 / 82, `直指定位訣`, including `因乘完畢待數莫動`;
- [x] deepen older Chinese counting-rod vocabulary while preserving the evidence boundary between procedural text and reconstructed material operation;
- [x] add a non-Chinese primary comparison: Adam Ries, *Rechnung auff der Linihen* (1525), line reckoning with positional counters;
- [x] check related repositories for duplication;
- [x] grounding record: [`evidence/00-abacus-rod-line-reckoning-grounding.md`](evidence/00-abacus-rod-line-reckoning-grounding.md);
- [x] promote from `first-pass` to `grounded`.

Future maturation work is narrow: edition/folio cleanup and specialist historiography, not another generic abacus history.

### 2. Mercury delay-line memory — `first-pass`

- [x] bounded case: [`cases/01-mercury-delay-line-circulation.md`](cases/01-mercury-delay-line-circulation.md);
- [x] retention as circulation;
- [x] time as access geometry;
- [x] continuous regeneration as apparent persistence;
- [x] establish primary vocabulary through the 1947 Eckert–Mauchly `Memory system` patent and Wilkes's 1949 EDSAC report;
- [x] distinguish logical identity from identity of one physical pulse;
- [ ] add exact patent column / figure anchors and direct 1949 IRE page anchors;
- [ ] add machine-specific primary evidence for temperature control;
- [ ] promote to `grounded` only after source deepening.

This case is now the only Phase-1 case below `grounded`; grounding it is useful but no longer blocks the mechanism-variety gate because grounded DRAM already supplies active regeneration.

### 3. Magnetic core memory — `grounded`

- [x] bounded case: [`cases/02-magnetic-core-destructive-read.md`](cases/02-magnetic-core-destructive-read.md);
- [x] remanence as quiescent retention without periodic refresh;
- [x] destructive read and rewrite as an access-triggered retention obligation;
- [x] primary patent and machine-specific read–rewrite evidence;
- [x] contemporary nondestructive-read counterexamples;
- [x] distinguish element-level nonvolatility from whole-machine restart persistence;
- [x] grounding record: [`evidence/02-magnetic-core-1951-1954-grounding.md`](evidence/02-magnetic-core-1951-1954-grounding.md).

Remaining archival cleanup: obtain a directly renderable full scan of Papian's 1952 IRE paper; central claims no longer depend uniquely on it.

### 4. DRAM — `grounded`

- [x] bounded case: [`cases/03-dram-refresh-as-scheduled-restoration.md`](cases/03-dram-refresh-as-scheduled-restoration.md);
- [x] establish 1T1C retained charge, leakage, destructive-read restore, and periodic regeneration from Dennard's 1967-filed patent;
- [x] separate access-triggered restore from time-triggered regeneration;
- [x] add commercial nondestructive-read + mandatory-refresh boundary evidence;
- [x] add primary sense/restore evidence from commercial documentation;
- [x] grounding record: [`evidence/03-dram-1967-1982-grounding.md`](evidence/03-dram-1967-1982-grounding.md).

Do not expand this into a general DRAM history; route broader semiconductor-memory history to `computing-archaeology`.

### 5. Mapped Flash — `grounded`

- [x] bounded case: [`cases/04-flash-virtual-mapping-logical-identity.md`](cases/04-flash-virtual-mapping-logical-identity.md);
- [x] erase-before-write geometry and out-of-place update;
- [x] virtual/logical/physical address separation;
- [x] identity persistence while physical location changes;
- [x] logical invalidation versus later physical erase;
- [x] transfer/reclamation as copy-current → erase-old → remap;
- [x] mapping/allocation metadata as retained state;
- [x] establish `Flash Translation Layer` terminology no later than Intel AP-619 (August 1995) without retroactively renaming earlier systems;
- [x] separate reclamation from wear leveling using early 1990s primary evidence;
- [x] add bounded later NAND evidence for bad blocks, ECC, and block replacement;
- [x] grounding record: [`evidence/04-flash-1992-1998-grounding.md`](evidence/04-flash-1992-1998-grounding.md).

Remaining cleanup: directly inspect Masuoka et al. 1987 IEDM full text if available. TRIM/deallocation/secure erase should be a separate later case.

### 6. RADOS replicated objects — `grounded`

- [x] bounded system: 2006–2007 Ceph/RADOS rather than generic cloud storage;
- [x] case: [`cases/05-rados-replicated-object-repair.md`](cases/05-rados-replicated-object-repair.md);
- [x] object → PG → ordered OSD placement through CRUSH/current cluster map;
- [x] primary-copy ordering, versioning, replica acknowledgement;
- [x] replica multiplicity versus retained currentness;
- [x] failure/membership-triggered repair, peering, re-replication and stale/missing recovery;
- [x] replicated volatile acknowledgement versus later durable commit;
- [x] qualify “no privileged copy”: no permanently privileged physical home while temporary protocol authority still exists;
- [x] compare 2006 and 2007 semantics rather than merging them silently;
- [x] contemporaneous PG-log persistence/recovery implementation artifact;
- [x] grounding record: [`evidence/05-rados-2006-2007-grounding.md`](evidence/05-rados-2006-2007-grounding.md).

Future work should be narrow semantic/version archaeology, not generic Ceph expansion.

### Phase-1 gate status

The mechanism-variety gate is now satisfied:

- [x] at least four contrasting cases at `grounded` or better — currently five;
- [x] passive-position case — grounded abacus / reckoning comparison;
- [x] active refresh/regeneration case — grounded DRAM;
- [x] nonvolatile physical state — grounded magnetic core and mapped Flash;
- [x] logical identity survives physical relocation — grounded mapped Flash;
- [x] logical identity survives replica loss/replacement — grounded RADOS.

This authorizes **bounded synthesis work**, not a grand conclusion. The first synthesis task should audit provisional theses against the five grounded regimes and record counterexamples before writing a philosophical overview.

Detailed cross-case findings live in [`CASE_INDEX.md`](CASE_INDEX.md).

---

## Phase 2 — Build missing technical bridges

Coordinate with `computing-archaeology` rather than duplicating it.

Priority bridges:

- [ ] latch / flip-flop / register;
- [ ] SRAM and cache;
- [ ] DRAM evolution and refresh machinery beyond the bounded case;
- [ ] ROM → PROM → EPROM → EEPROM → Flash;
- [ ] HDD geometry, bad-sector remapping, CHS → LBA;
- [ ] virtual memory and paging;
- [ ] file-system crash consistency;
- [ ] SSD FTL/controller-mediated persistence beyond the bounded Ban/1990s case;
- [ ] RAID / scrubbing / rebuild;
- [ ] distributed replication and erasure coding beyond RADOS.

A bridge belongs here only when it changes the retention comparison. Generic technical history belongs primarily in `computing-archaeology`.

---

## Phase 3 — Retention / transfer / computation boundary

Research problems:

- [ ] When is a buffer `storage`?
- [ ] When does transfer become retention across time?
- [ ] How much delay is required before a state is usefully called stored?
- [ ] When does a retained state become part of computation rather than merely input/output?
- [ ] How do cache and memoization complicate the boundary?
- [ ] What is the difference between state, memory, store, archive, log, file, record, and trace?
- [ ] Does `working retention` remain useful across human-mediated positional calculation and autonomous machine memory?
- [ ] Should `passive positional retention` and `human-mediated addressability` become controlled terms?
- [ ] Does `recurrence` deserve a separate controlled term from `refresh`?
- [ ] Should the project formally distinguish quiescent retention, continuous maintenance, access-triggered restoration, deadline-driven maintenance, capacity/reclaim-triggered maintenance, wear/lifetime-triggered placement, and failure/repair-triggered maintenance?
- [ ] When a mapping layer moves state, is the retained object data, address, relation, or all three?
- [ ] When replicas disagree, is `currentness` itself retained metadata/protocol state?
- [ ] How should `acknowledged`, `visible`, `replicated`, and `durably committed` be separated across systems?

This phase should engage Ernst directly only after the mechanism comparison is explicit.

---

## Phase 4 — Technical forgetting

Build a mechanism-sensitive map of:

- [ ] physical disturbance / reset of positional working state;
- [ ] interpretive or procedural-context loss while physical state survives;
- [ ] decay and leakage;
- [ ] power loss;
- [ ] refresh failure;
- [ ] overwrite;
- [ ] physical erase;
- [ ] logical deletion / invalidation;
- [ ] garbage collection / reclamation;
- [ ] loss of index or mapping metadata;
- [ ] loss of currentness/version metadata;
- [ ] key destruction;
- [ ] bit rot;
- [ ] controller failure;
- [ ] replica divergence and failed repair;
- [ ] media obsolescence;
- [ ] format/software obsolescence;
- [ ] institutional abandonment.

Goal: replace the single word `forgetting` with a vocabulary tied to actual failure and invalidation mechanisms.

---

## Phase 5 — Maintenance and invisible work

Study why persistence appears static even when it depends on activity.

Cases and functions may include:

- human protection, selection, interpretation, and reset of working state;
- circulation/regeneration;
- destructive-read restore;
- refresh logic and sense/restore infrastructure;
- storage controllers;
- ECC;
- disk servo systems;
- SSD firmware, reclamation, wear management, bad-block replacement;
- data scrubbing;
- RAID rebuild;
- distributed peering/repair/anti-entropy;
- tape migration;
- backup operators;
- archival format migration;
- data-center facilities.

The cross-period question is not whether human work disappears, but **where retention work migrates when it becomes automated or infrastructural**.

Coordinate labor/manufacturing evidence with related repositories where relevant.

---

## Phase 6 — Philosophical synthesis

The mechanism gate is open, so philosophical comparison may now begin — but claim by claim.

### First bounded synthesis pass

- [ ] audit README thesis 1, “persistence is often an activity disguised as a property,” against passive position, core, DRAM, mapped Flash, and RADOS; identify the passive-position counterexample/qualification;
- [ ] audit “storage is temporal transport” and decide whether it adds explanatory power or merely redescribes retention;
- [ ] audit the role of addressability across human-mediated positional selection, coordinate-selected memory, logical mapping, and distributed placement;
- [ ] audit “logical persistence becomes detached from privileged physical location” as a historically staged claim rather than a universal definition;
- [ ] build a counterexample ledger before promoting any provisional thesis to a conclusion.

### Philosophical tests after the audit

- [ ] test Stiegler's tertiary retention against operational working state without assuming every retained bit/token is tertiary retention in the same sense;
- [ ] test whether Heideggerian availability/ordering is actually clarified by addressability and storage infrastructure; keep `Bestand ≠ storage` explicit;
- [ ] compare Ernst's operational/microtemporal account with passive positional state, scheduled refresh, and long-duration preservation;
- [ ] extend Kirschenbaum's forensic materiality through Flash remapping, logical invalidation, copy-on-write-like relocation, encryption, and distributed storage;
- [ ] decide whether `technical retention` names one coherent operation or a family of mechanisms linked only by carefully stated invariants.

Do not write a grand `What Is Technical Retention?` chapter until this bounded thesis audit exists.

---

## Research quality gates

Before marking a major case `grounded`:

- [ ] historical vocabulary recovered;
- [ ] at least one strong primary technical/historical source where available;
- [ ] exact source location recorded for central primary claims;
- [ ] mechanism described below the user-interface metaphor;
- [ ] maintenance requirements stated;
- [ ] failure / forgetting modes separated;
- [ ] modern analogy labeled as analogy;
- [ ] philosophical interpretation separated from historical record;
- [ ] counterexample or limit included;
- [ ] related-repository duplication checked.

Before marking a case `mature`, additionally require that it survive cross-case comparison and that its central claims no longer depend on a single source, source family, or fragile analogy.
