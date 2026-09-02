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

- [x] at least four contrasting cases at `grounded` or better — currently five within Phase 1;
- [x] passive-position case — grounded abacus / reckoning comparison;
- [x] active refresh/regeneration case — grounded DRAM;
- [x] nonvolatile physical state — grounded magnetic core and mapped Flash;
- [x] logical identity survives physical relocation — grounded mapped Flash;
- [x] logical identity survives replica loss/replacement — grounded RADOS.

This authorizes **bounded synthesis work**, not a grand conclusion. The first synthesis task should audit provisional theses against the five grounded Phase-1 regimes and record counterexamples before writing a philosophical overview.

Detailed cross-case findings live in [`CASE_INDEX.md`](CASE_INDEX.md).

---

## Phase 2 — Build missing technical bridges

Coordinate with `computing-archaeology` rather than duplicating it.

Priority bridges:

- [x] latch / flip-flop / register — the bounded bridge in [`cases/06-flip-flop-powered-working-retention.md`](cases/06-flip-flop-powered-working-retention.md) is now **`grounded`**. The promotion record is [`evidence/06-burks-1947-eniac-flip-flop-grounding.md`](evidence/06-burks-1947-eniac-flip-flop-grounding.md), alongside [`evidence/06-flip-flop-register-boundary-addendum.md`](evidence/06-flip-flop-register-boundary-addendum.md), [`evidence/06-eniac-timing-retention-deepening.md`](evidence/06-eniac-timing-retention-deepening.md), and [`evidence/06-eccles-jordan-1919-proceedings-deepening.md`](evidence/06-eccles-jordan-1919-proceedings-deepening.md). Burks's 1947 _Proceedings of the I.R.E._ paper, pp. 757–759, directly supplies period remembering-circuit vocabulary, a published simplified ENIAC schematic, an explicit two-stable-state / direct-current cross-coupling mechanism, separation of steady-state stability from triggering/recovery dynamics, and microsecond timing margins. This closes the general circuit-mechanism blocker without pretending Burks Fig. 3 is the uninspected PX-1-105 production drawing. Exact PX-1-105 and exact 1919 periodical facsimiles remain archival cleanup for artifact-specific claims rather than promotion blockers;
- [x] SRAM and cache — the **static-MOS / SRAM substrate-array sub-slice is `grounded`** in [`cases/07-static-mos-ram-powered-quiescence.md`](cases/07-static-mos-ram-powered-quiescence.md), with promotion record [`evidence/07-intel-pashley-1975-static-ram-grounding.md`](evidence/07-intel-pashley-1975-static-ram-grounding.md). The separate **cache policy/interface sub-slice is now `grounded`** in [`cases/08-system360-model85-cache-currentness.md`](cases/08-system360-model85-cache-currentness.md), with grounding record [`evidence/08-model85-cache-1967-1968-grounding.md`](evidence/08-model85-cache-1967-1968-grounding.md). Liptay 1968 and IBM's 1967 Model 85 manual directly establish a transparent derivative fast copy with retained sector-address correspondence, per-block validity, event-triggered update/currentness, demand loading, and activity-list replacement state. This closes the bounded SRAM→cache bridge while preserving the historical vocabulary (`sector address register`, `validity bit`, `activity list`) rather than retroactively normalizing it into later tag/write-through/coherence terminology. Later write-back/dirty-state retention, multiprocessor cache coherence, ECC, and exact Model-85 fast-store circuit technology remain separate regimes, not hidden completion criteria for this bounded bridge;
- [ ] DRAM evolution and refresh machinery beyond the bounded case — **partially advanced by two grounded bounded sub-slices**: [`cases/09-dram-cbr-refresh-address-internalization.md`](cases/09-dram-cbr-refresh-address-internalization.md) separates the refresh deadline from the source of refresh-row addresses, and [`cases/10-toshiba-leakage-tracked-self-refresh.md`](cases/10-toshiba-leakage-tracked-self-refresh.md) separates address internalization from schedule/trigger internalization. SDRAM command semantics, standardized self-refresh entry/exit, per-bank refresh, and later retention-aware policy remain distinct open regimes, so the broad item stays unchecked;
- [x] ROM → PROM → EPROM → EEPROM → Flash — **the retention-specific bounded bridge is now closed through three grounded sub-slices plus the already-grounded mapped-Flash case**. [`cases/11-intel-frohman-floating-gate-eprom-erasure.md`](cases/11-intel-frohman-floating-gate-eprom-erasure.md) separates trapped-charge nonvolatility, avalanche-injection programming, nondestructive lower-stress read, and radiation erase. [`cases/12-intel-2816-eeprom-electrical-erasure.md`](cases/12-intel-2816-eeprom-electrical-erasure.md) moves erase into electrical/in-system control while preserving byte versus chip erase geometry, a distinct 21 V/timed erase-write regime, erase-before-write sequencing, and finite cycling. [`cases/13-early-flash-coarse-erase-asymmetric-rewrite.md`](cases/13-early-flash-coarse-erase-asymmetric-rewrite.md), grounded by [`evidence/13-early-flash-coarse-erase-1980-1988-grounding.md`](evidence/13-early-flash-coarse-erase-1980-1988-grounding.md), then grounds the device-level shift to shared/whole-array electrical erase with finer read/program selection and a one-transistor density objective. Case 04 separately grounds the historically later mapping/copy/reclaim response. This checkbox means the **bounded retention-mechanism bridge**, not an exhaustive genealogy of mask ROM, fuse PROM, every EEPROM family, NOR/NAND process history, or invention priority; those broader histories belong in `computing-archaeology` or dedicated future cases;
- [ ] HDD geometry, bad-sector remapping, CHS → LBA — **partially advanced by grounded bounded Case 14**: [`cases/14-scsi-disk-defect-reassignment-logical-identity.md`](cases/14-scsi-disk-defect-reassignment-logical-identity.md) uses 1990–1997 period-primary evidence to separate host LBA from physical target, manufacturer-defect slipping from grown-defect replacement, defect metadata from payload, and successful physical reassignment from payload preservation. Seagate's `REASSIGN BLOCKS` semantics make one LBA capable of traversing multiple physical addresses until spare locations are exhausted. The broad item stays unchecked because the general CHS→LBA interface chronology, earlier standards lineage, ATA/IDE transition, zone translation, and vendor-specific controller histories remain distinct work;
- [ ] virtual memory and paging;
- [ ] file-system crash consistency;
- [ ] SSD FTL/controller-mediated persistence beyond the bounded Ban/1990s case — **partially advanced by grounded Case 15**: [`cases/15-intel-ssd320-power-loss-durability.md`](cases/15-intel-ssd320-power-loss-durability.md) uses 2007 ATA8-ACS standards-development text plus Intel's 2011 SSD 320 product/design material to separate volatile write-cache/temporary-buffer state, nonvolatile NAND, explicit `FLUSH CACHE` completion, orderly `STANDBY IMMEDIATE` handoff, and a power-failure-triggered capacitor-backed emergency transfer. The broad item stays unchecked because filesystem `fsync`, NVMe FUA / volatile-write-cache / persistence-domain semantics, controller-metadata recovery, enterprise PLP qualification, and later SSD interfaces remain distinct regimes; the independent FAST '13 fault-injection evidence is retained as a contract-versus-compliance boundary rather than silently assigned to the SSD 320;
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

The first direct Ernst test is now complete; later work in this phase should reuse its timescale decomposition rather than treating `microtemporality` as a catch-all answer.

The grounded flip-flop stress test adds one concrete correction for this phase: a later retained-state relation need not appear as a discrete `retrieve` operation. In the ENIAC static-output and carry cases, a state can remain continuously available at a circuit output and become significant only when a later gate/pulse acts on it. Part II p. IV-43 adds a second boundary case: an external switch event can be retained in one flip-flop, transferred into a machine-timed flip-flop by a later central programming pulse, and only then drive a reliable transmitter action. Burks 1947 adds a third: even a microsecond-scale state has separate stability, transition, and recovery constraints. Future boundary work should therefore test **later state-sensitive use**, **event/timing retention**, and **state-holding versus transition/recovery** alongside explicit recovery/read operations. Modern clock-domain/metastability language remains analogy, not 1946 vocabulary.

The grounded static-MOS bridge adds two further controls. First, `power dependence` is not one Boolean property: Intel's 5101L documentation separates a lower-voltage state-retention condition from ordinary active operation and defines an operation-recovery relation between them. Second, Pashley's 1975 Intel filing separates the bistable cell from X/Y selection, column sensing, read-bus, output, write, and address-transition machinery. Future boundary work should therefore compare **retention-supporting supply**, **active-operation supply**, **transition/recovery between power modes**, and **state survival versus selection/sensing recoverability** rather than treating `volatile/static`, `needs power`, or `cell still holds a bit` as sufficient service descriptors.

The grounded Model 85 cache bridge adds the architectural layer that the SRAM case intentionally excluded. Program-visible main-storage addresses remain stable while fast-copy residency changes; a cache hit requires retained sector correspondence plus per-block validity; processor/channel stores maintain the currentness of already resident copies; and replacement can deliberately end cache-copy retention without losing authoritative main-storage state. Future cache-boundary work must therefore distinguish **payload retention**, **copy identity/correspondence**, **validity/currentness**, **replacement-policy state**, and **authority**. Later write-back caches should be allowed to break the Model 85 result by introducing cache-local dirty/authoritative state rather than being forced into a write-through model.

The grounded EPROM bridge adds a different access/control boundary. An insulated floating gate can retain state without continuous operating power, X/Y electrical selection can program and nondestructively read cells, yet the bounded erase path can be radiation applied to the physical device rather than an ordinary addressed electrical command. The grounded EEPROM bridge then changes that partition: Intel's 2816 makes byte erase/write electrically and in-system controllable, but READ, BYTE ERASE, BYTE WRITE, and CHIP ERASE remain distinct modes; erase/write still requires elevated VPP and millisecond timing, byte rewrite is erase-before-write, and finite cycling makes repeated alteration a lifetime constraint. The grounded early-Flash bridge adds the next correction: electrical control can deliberately become **coarser** at erase time while read/program remain finer, and whole-array erase can still require address-by-address verification. Future semiconductor comparisons should therefore separate **hold**, **read**, **program**, **erase authority**, **erase granularity**, **verification granularity**, **exceptional-operation infrastructure**, and **endurance** rather than assuming `electrically erasable` describes one uniform operation.

The grounded HDD defect-reassignment bridge adds a second, non-Flash form of logical/physical indirection. A host can continue naming the same LBA after the controller changes its physical sector, but Seagate's command semantics explicitly allow the remap to succeed without preserving the affected payload. Future address/identity work must therefore separate **designation continuity**, **physical-embodiment continuity**, **payload continuity**, **repair metadata**, and **finite replacement capacity**. The comparison to mapped Flash is useful only at that relational level: failure-triggered spare substitution is not erase-driven FTL relocation.

The grounded SSD power-loss bridge adds a durability boundary that neither Flash-cell nonvolatility nor FTL mapping alone supplies. A host-visible write can pass through volatile cache/temporary buffers before becoming recoverable nonvolatile state; `FLUSH CACHE`, orderly shutdown, and unexpected-power-loss protection are distinct transition authorities; and a capacitor can retain only energy while still being constitutive infrastructure for preserving payload and system state. Future boundary work should therefore separate **write acknowledgement**, **visibility**, **volatile staging**, **flush completion**, **nonvolatile-media residency**, **post-restart logical currentness**, and **fault-path compliance** rather than treating `SSD is nonvolatile` as an end-to-end persistence claim.

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
- [ ] defect growth, failed reassignment, or spare exhaustion;
- [ ] loss of volatile controller/buffer state before a durability handoff;
- [ ] failed flush, shutdown transfer, or power-loss emergency transfer;
- [ ] key destruction;
- [ ] bit rot;
- [ ] controller failure;
- [ ] replica divergence and failed repair;
- [ ] media obsolescence;
- [ ] format/software obsolescence;
- [ ] institutional abandonment.

Goal: replace the single word `forgetting` with a vocabulary tied to actual failure and invalidation mechanisms.

The first bounded cross-case forgetting audit is now complete in [`docs/SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md`](docs/SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md). It establishes a five-case decomposition among physical disturbance/destruction, missed maintenance obligations, logical invalidation/deauthorization, relation/metadata loss, and service/recoverability loss. It also records the counterexamples `physical loss ≠ logical forgetting`, `physical survival ≠ retained current state`, and `unavailability ≠ forgetting`. The unchecked items above remain open because key destruction, obsolescence, bit rot, and several controller/institutional mechanisms have not yet been grounded by dedicated cases.

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
- disk defect-list maintenance, spare allocation, and reallocation;
- SSD firmware, reclamation, wear management, bad-block replacement;
- volatile write-cache / temporary-buffer handoff;
- host-issued flush or orderly-shutdown commands;
- power-fail detection, supply isolation, hold-up energy, and emergency NAND transfer;
- data scrubbing;
- RAID rebuild;
- distributed peering/repair/anti-entropy;
- tape migration;
- backup operators;
- archival format migration;
- data-center facilities.

The cross-period question is not whether human work disappears, but **where retention work migrates when it becomes automated or infrastructural**.

The first bounded maintenance-visibility audit is complete in [`docs/SYNTHESIS_AUDIT_06_MAINTENANCE_VISIBILITY.md`](docs/SYNTHESIS_AUDIT_06_MAINTENANCE_VISIBILITY.md). It rejects a monotonic `more reliable -> more hidden maintenance` law and requires future claims to separate reliability, automation, observer/interface visibility, labor, and infrastructure. It supports work displacement across interfaces, not a universal claim that automation reduces total human labor.

Coordinate labor/manufacturing evidence with related repositories where relevant. Broader labor-history claims remain open and require dedicated sources rather than inference from controller diagrams.

---

## Phase 6 — Philosophical synthesis

The mechanism gate is open, so philosophical comparison may now begin — but claim by claim.

### First bounded synthesis pass — complete

- [x] audit README thesis 1, “persistence is often an activity disguised as a property,” against passive position, core, DRAM, mapped Flash, and RADOS; identify the passive-position counterexample/qualification — completed in [`docs/SYNTHESIS_AUDIT_01_MAINTAINED_PERSISTENCE.md`](docs/SYNTHESIS_AUDIT_01_MAINTAINED_PERSISTENCE.md); the thesis was revised rather than simply confirmed;
- [x] audit “storage is temporal transport” and decide whether it adds explanatory power or merely redescribes retention — completed in [`docs/SYNTHESIS_AUDIT_02_TEMPORAL_TRANSPORT.md`](docs/SYNTHESIS_AUDIT_02_TEMPORAL_TRANSPORT.md); retained as a recoverability relation across time, not as literal physical motion or a sufficient mechanism definition;
- [x] audit the role of addressability across human-mediated positional selection, coordinate-selected memory, logical mapping, and distributed placement — completed in [`docs/SYNTHESIS_AUDIT_03_ADDRESSABILITY.md`](docs/SYNTHESIS_AUDIT_03_ADDRESSABILITY.md); retention was separated from designation, selection/resolution, currentness/admissibility, and recovery;
- [x] audit “logical persistence becomes detached from privileged physical location” as a historically staged claim rather than a universal definition — completed in [`docs/SYNTHESIS_AUDIT_04_PRIVILEGED_LOCATION.md`](docs/SYNTHESIS_AUDIT_04_PRIVILEGED_LOCATION.md); the audit separates microscopic state reconstruction, stable physical home, metadata-mediated relocation, replaceable replicas, and temporary protocol authority;
- [x] build a counterexample ledger before promoting any provisional thesis to a conclusion — completed in [`docs/SYNTHESIS_COUNTEREXAMPLE_LEDGER.md`](docs/SYNTHESIS_COUNTEREXAMPLE_LEDGER.md); it records rejected strong claims, required decompositions, scoped survivors, and current thesis status;
- [x] audit README thesis 4, `Forgetting has mechanisms`, against the five grounded regimes — completed in [`docs/SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md`](docs/SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md); the thesis now separates physical loss, missed maintenance, logical invalidation, relation/currentness loss, and service/recoverability loss, with explicit counterexamples to equating loss at one layer with forgetting at another;
- [x] audit README thesis 6, “more reliable retention can hide more of its maintenance from experience,” against the same grounded cases — completed in [`docs/SYNTHESIS_AUDIT_06_MAINTENANCE_VISIBILITY.md`](docs/SYNTHESIS_AUDIT_06_MAINTENANCE_VISIBILITY.md); the monotonic law was rejected and the surviving claim now separates reliability, automation, interface invisibility, labor, and infrastructure.

Audits 01–06 and the cross-audit ledger establish a negative discipline for synthesis: a universal `persistence = activity` formulation fails; literal `storage = physical transport` fails; `retention = addressability`, `address = physical location`, `resolution = currentness`, and `addressability = availability` fail; `logical = placeless` and a monotonic historical ascent toward placelessness fail; `physical destruction = logical forgetting`, `logical invalidation = physical erasure`, and `unavailable now = forgotten` fail; `more reliable -> more hidden maintenance`, `automated -> invisible to everyone`, and `self-healing -> maintenance-free` also fail. The surviving formulations remain provisional and layer-sensitive.

### Named philosophical/prior-art tests

- [x] **Wolfgang Ernst operationality / microtemporality** — completed in [`docs/PHILOSOPHICAL_TEST_01_ERNST_OPERATIONALITY.md`](docs/PHILOSOPHICAL_TEST_01_ERNST_OPERATIONALITY.md). The test retains Ernst's operational analysis as a major methodological prior art while rejecting `retained state = continuous operation` and `technically decisive time = microtime only`; it requires plural timescales and separates retention-time, access-time, maintenance-time, and interpretive operations.
- [x] **Bernard Stiegler / tertiary retention boundary** — completed in [`docs/PHILOSOPHICAL_TEST_02_STIEGLER_TERTIARY_RETENTION.md`](docs/PHILOSOPHICAL_TEST_02_STIEGLER_TERTIARY_RETENTION.md). The test uses primary Stiegler anchors and grounded abacus, DRAM, mapped-Flash, and RADOS cases to separate broad mechanism-level `technical retention` from the thicker relation of technical exteriorization, repetition, learning, and transmission; it rejects `every retained machine state = tertiary retention` while also rejecting a human-readable/durable-media-only restriction.
- [x] **Heidegger / availability and ordering** — completed in [`docs/PHILOSOPHICAL_TEST_03_HEIDEGGER_ORDERABILITY.md`](docs/PHILOSOPHICAL_TEST_03_HEIDEGGER_ORDERABILITY.md). The test preserves `Bestand ≠ storage`, uses Lovitt's printed pp. 16–23 to separate storage from standing-reserve/orderability, and tests the addressability chain plus mapped Flash/RADOS against the narrower question of how a state becomes technically callable for further operations.
- [x] **Kirschenbaum / forensic materiality beyond disk** — completed in [`docs/PHILOSOPHICAL_TEST_04_KIRSCHENBAUM_FORENSIC_MATERIALITY.md`](docs/PHILOSOPHICAL_TEST_04_KIRSCHENBAUM_FORENSIC_MATERIALITY.md). The test keeps Kirschenbaum's forensic/formal distinction but rejects a universal hard-drive-remanence model; grounded mapped Flash and RADOS plus the bounded FAST 2011 SSD comparison require `forensic witness ≠ authoritative current state` and distinguish logical-object, current-embodiment, and forensic-trace survivability.
- [x] decide whether `technical retention` names one coherent operation or a family of mechanisms linked only by carefully stated invariants — completed in [`docs/SYNTHESIS_AUDIT_07_TECHNICAL_RETENTION_COHERENCE.md`](docs/SYNTHESIS_AUDIT_07_TECHNICAL_RETENTION_COHERENCE.md). The audit rejects both a single common physical mechanism and an unconstrained `anything that lasts` umbrella. The current bounded result is one minimal analytical relation — an operationally typed retention target remains or is reconstructed across temporal separation and later counts as an admissible continuation under an explicit sameness/currentness/interpretation rule — implemented through many cross-cutting mechanisms rather than exclusive subfamilies.

**Grounded technical stress test:** [`cases/06-flip-flop-powered-working-retention.md`](cases/06-flip-flop-powered-working-retention.md) is `grounded`; see [`evidence/06-burks-1947-eniac-flip-flop-grounding.md`](evidence/06-burks-1947-eniac-flip-flop-grounding.md). Its source set supports short-duration retention, continuous-power/refresh separation, later state-sensitive use without a discrete retrieval transaction, period register boundaries, staged pending-event retention, and a directly inspected period-published ENIAC circuit in which steady-state stability is explicitly separated from triggering/recovery. Exact PX-1-105 visual inspection remains archival cleanup for drawing-specific questions.

**Grounded semiconductor stress test:** [`cases/07-static-mos-ram-powered-quiescence.md`](cases/07-static-mos-ram-powered-quiescence.md) is `grounded`; see [`evidence/07-intel-pashley-1975-static-ram-grounding.md`](evidence/07-intel-pashley-1975-static-ram-grounding.md). The bounded source set supports period static-MOS / flip-flop / bistable vocabulary, no-refresh static operation, nondestructive read in cited Intel products, decoded-array organization, a 5101L low-voltage retention/operation-recovery boundary, and an Intel manufacturer-primary feedback-coupled static cell embedded in a decoded/sensed `1024 × 1` design. The source set also forces a new distinction: **cell-state retention ≠ reliable selection/sensing/recovery**. Exact commercial-product topology and the Vadasz facsimile remain archival cleanup, not central mechanism blockers.

**Grounded cache stress test:** [`cases/08-system360-model85-cache-currentness.md`](cases/08-system360-model85-cache-currentness.md) is `grounded`; see [`evidence/08-model85-cache-1967-1968-grounding.md`](evidence/08-model85-cache-1967-1968-grounding.md). Period IBM evidence makes cache currentness a relation among derivative payload, sector correspondence, block validity, store-triggered updating, and replacement policy. The Model 85 is especially useful because every store updates main storage: cache reassignment can terminate fast-copy retention without terminating authoritative-state retention. Modern `tag`, `write-through`, `LRU`, and coherence terms remain labeled reconstructions rather than substituted historical vocabulary.

**Grounded DRAM refresh-responsibility continuation:** Cases [`09`](cases/09-dram-cbr-refresh-address-internalization.md) and [`10`](cases/10-toshiba-leakage-tracked-self-refresh.md) are `grounded`. Together they separate the physical refresh deadline from row enumeration, externally supplied trigger cadence, on-chip scheduling, and condition-derived triggering. They do not close the broad history of later standardized refresh interfaces.

**Grounded floating-gate EPROM stress test:** [`cases/11-intel-frohman-floating-gate-eprom-erasure.md`](cases/11-intel-frohman-floating-gate-eprom-erasure.md) is `grounded`; see [`evidence/11-intel-1970-1971-floating-gate-eprom-grounding.md`](evidence/11-intel-1970-1971-floating-gate-eprom-grounding.md). It adds quiescent trapped-charge nonvolatility together with an explicit separation among avalanche programming, nondestructive read, and radiation erase. The key correction is that **nonvolatility is not immutability and access geometry need not equal erase geometry**.

**Grounded EEPROM electrical-erasure stress test:** [`cases/12-intel-2816-eeprom-electrical-erasure.md`](cases/12-intel-2816-eeprom-electrical-erasure.md) is `grounded`; see [`evidence/12-intel-1978-1981-eeprom-electrical-erasure-grounding.md`](evidence/12-intel-1978-1981-eeprom-electrical-erasure-grounding.md). The Intel 2816 product evidence makes electrical erase callable at byte granularity and also exposes whole-chip erase, while keeping erase/write distinct from ordinary read through VPP, timing, mode sequencing, and finite cycling. The source pair therefore adds **electrical erasure ≠ ordinary service equivalence**, **electrical erasability ≠ one erase geometry**, **erase-before-write can make forgetting part of update**, and **nonvolatility ≠ unlimited mutability**.

**Grounded early-Flash erase-geometry stress test:** [`cases/13-early-flash-coarse-erase-asymmetric-rewrite.md`](cases/13-early-flash-coarse-erase-asymmetric-rewrite.md) is `grounded`; see [`evidence/13-early-flash-coarse-erase-1980-1988-grounding.md`](evidence/13-early-flash-coarse-erase-1980-1988-grounding.md). Toshiba and Intel manufacturer-primary evidence grounds one-transistor density pressure, shared/whole-array electrical erase, finer addressed program/read, command control, and address-walking verify/retry. It forces three new separations: **program addressability ≠ erase addressability**, **fast bulk erase ≠ fast arbitrary rewrite**, and **erase asymmetry ≠ FTL**. Masuoka 1984 and Kynett 1988 full facsimiles remain archival cleanup; their indexed abstracts are not treated as figure-level inspection.

**Grounded HDD defect-reassignment stress test:** [`cases/14-scsi-disk-defect-reassignment-logical-identity.md`](cases/14-scsi-disk-defect-reassignment-logical-identity.md) is `grounded`; see [`evidence/14-disk-lba-defect-reassignment-1990-1997-grounding.md`](evidence/14-disk-lba-defect-reassignment-1990-1997-grounding.md). Period NeXT/Seagate evidence shows that a stable LBA can traverse physical sectors after defects while `REASSIGN BLOCKS` itself does not preserve the affected payload. It also makes defect-list state and finite spare capacity part of the continuation mechanism. The case therefore forces **logical-block identity ≠ physical-sector identity**, **reassignment continuity ≠ payload continuity**, and **LBA abstraction ≠ disappearance of geometry**, while keeping the comparison to Flash FTL explicitly functional rather than genealogical.

**Grounded SSD power-loss-durability stress test:** [`cases/15-intel-ssd320-power-loss-durability.md`](cases/15-intel-ssd320-power-loss-durability.md) is `grounded`; see [`evidence/15-intel-ssd320-power-loss-durability-grounding.md`](evidence/15-intel-ssd320-power-loss-durability-grounding.md). Period ATA text and Intel product/design evidence put a volatile staging layer in front of nonvolatile NAND and distinguish host-requested flush, clean-shutdown transfer, and device-triggered emergency work under stored capacitor energy. FAST '13 is used only as an independent boundary against equating interface/design claims with measured compliance. This case adds **nonvolatile medium ≠ end-to-end durable state**, **stored energy ≠ stored payload**, and **durability handoff ≠ ordinary media retention**.

**Next highest-value unit:** move to one still-open Phase-2 bridge that changes the retention comparison rather than extending the now-grounded SSD 320 slice. Prefer **file-system crash consistency** if period-primary design evidence can cleanly separate volatile cache state, write ordering, commit/recovery rules, and post-crash admissible state; otherwise choose **RAID / scrubbing / rebuild** or a bounded **NVMe persistence-domain** case. Do not expand Case 15 into a generic SSD chapter or use it to infer filesystem `fsync` semantics.

The first generic thesis-audit sequence, four named philosophical/prior-art tests, the first category-coherence audit, and the post-audit technical stress tests are now grounded at bounded maturity. Do not promote the bounded relational criterion into a grand `What Is Technical Retention?` chapter yet. Cases 06–15 continue to add counterexample pressure: short working-state retention, static-array power boundaries, cache currentness, refresh-responsibility migration, condition-derived maintenance, external-versus-electrical erase authority, erase granularity, verification granularity, endurance, logical/physical disk indirection, payload-recovery separation, finite repair slack, volatile durability windows, explicit flush boundaries, and failure-triggered emergency handoff must all remain distinct.

---

## Research quality gates

Before marking a major case `grounded`:

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