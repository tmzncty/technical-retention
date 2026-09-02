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

### 2. Mercury delay-line memory — `grounded`

- [x] bounded case: [`cases/01-mercury-delay-line-circulation.md`](cases/01-mercury-delay-line-circulation.md);
- [x] retention as circulation;
- [x] time as access geometry;
- [x] continuous regeneration as apparent persistence;
- [x] establish primary vocabulary through the 1947 Eckert–Mauchly `Memory system` patent and Wilkes's 1949 EDSAC report;
- [x] distinguish logical identity from identity of one physical pulse;
- [x] add exact patent column / figure anchors and direct 1949 IRE p. 855 facsimile evidence;
- [x] add machine-specific primary evidence for temperature control through the 1958 UNIVAC I maintenance manual;
- [x] grounding record: [`evidence/01-mercury-delay-line-1947-1958-grounding.md`](evidence/01-mercury-delay-line-1947-1958-grounding.md);
- [x] promote from `first-pass` to `grounded` after source deepening.

Remaining work is archival or scope-specific cleanup rather than a promotion blocker: obtain a conveniently renderable full facsimile of the 1949 IRE pp. 856–861 if a later argument needs additional page/figure anchors, and require EDSAC-specific primary thermal-control evidence before making an EDSAC-specific thermal-control claim. The broader engineering history remains in `computing-archaeology`.

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

The mechanism-variety gate is now satisfied and all six Phase-1 cases are `grounded`:

- [x] at least four contrasting cases at `grounded` or better — currently six within Phase 1;
- [x] passive-position case — grounded abacus / reckoning comparison;
- [x] active circulation/regeneration case — grounded mercury delay line;
- [x] active deadline refresh/regeneration case — grounded DRAM;
- [x] nonvolatile physical state — grounded magnetic core and mapped Flash;
- [x] logical identity survives physical relocation — grounded mapped Flash;
- [x] logical identity survives replica loss/replacement — grounded RADOS.

This authorizes **bounded synthesis work**, not a grand conclusion. The synthesis audits and later adversarial bridges must continue to treat the six Phase-1 regimes as evidence-bearing counterexamples rather than force them under one mechanism.

Detailed cross-case findings live in [`CASE_INDEX.md`](CASE_INDEX.md).

---

## Phase 2 — Build missing technical bridges

Coordinate with `computing-archaeology` rather than duplicating it.

Priority bridges:

- [x] latch / flip-flop / register — the bounded bridge in [`cases/06-flip-flop-powered-working-retention.md`](cases/06-flip-flop-powered-working-retention.md) is now **`grounded`**. The promotion record is [`evidence/06-burks-1947-eniac-flip-flop-grounding.md`](evidence/06-burks-1947-eniac-flip-flop-grounding.md), alongside [`evidence/06-flip-flop-register-boundary-addendum.md`](evidence/06-flip-flop-register-boundary-addendum.md), [`evidence/06-eniac-timing-retention-deepening.md`](evidence/06-eniac-timing-retention-deepening.md), and [`evidence/06-eccles-jordan-1919-proceedings-deepening.md`](evidence/06-eccles-jordan-1919-proceedings-deepening.md). Burks's 1947 _Proceedings of the I.R.E._ paper, pp. 757–759, directly supplies period remembering-circuit vocabulary, a published simplified ENIAC schematic, an explicit two-stable-state / direct-current cross-coupling mechanism, separation of steady-state stability from triggering/recovery dynamics, and microsecond timing margins. This closes the general circuit-mechanism blocker without pretending Burks Fig. 3 is the uninspected PX-1-105 production drawing. Exact PX-1-105 and exact 1919 periodical facsimiles remain archival cleanup for artifact-specific claims rather than promotion blockers;
- [x] SRAM and cache — the **static-MOS / SRAM substrate-array sub-slice is `grounded`** in [`cases/07-static-mos-ram-powered-quiescence.md`](cases/07-static-mos-ram-powered-quiescence.md), with promotion record [`evidence/07-intel-pashley-1975-static-ram-grounding.md`](evidence/07-intel-pashley-1975-static-ram-grounding.md). The separate **cache policy/interface sub-slice is now `grounded`** in [`cases/08-system360-model85-cache-currentness.md`](cases/08-system360-model85-cache-currentness.md), with grounding record [`evidence/08-model85-cache-1967-1968-grounding.md`](evidence/08-model85-cache-1967-1968-grounding.md). Liptay 1968 and IBM's 1967 Model 85 manual directly establish a transparent derivative fast copy with retained sector-address correspondence, per-block validity, event-triggered update/currentness, demand loading, and activity-list replacement state. This closes the bounded SRAM→cache bridge while preserving the historical vocabulary (`sector address register`, `validity bit`, `activity list`) rather than retroactively normalizing it into later tag/write-through/coherence terminology. Later write-back/dirty-state retention, multiprocessor cache coherence, ECC, and exact Model-85 fast-store circuit technology remain separate regimes, not hidden completion criteria for this bounded bridge;
- [ ] DRAM evolution and refresh machinery beyond the bounded case — **partially advanced by three grounded bounded sub-slices**: [`cases/09-dram-cbr-refresh-address-internalization.md`](cases/09-dram-cbr-refresh-address-internalization.md) separates the refresh deadline from the source of refresh-row addresses; [`cases/10-toshiba-leakage-tracked-self-refresh.md`](cases/10-toshiba-leakage-tracked-self-refresh.md) separates address internalization from schedule/trigger internalization; and [`cases/21-micron-sdram-refresh-mode-handoff.md`](cases/21-micron-sdram-refresh-mode-handoff.md), grounded by [`evidence/21-micron-1999-sdram-refresh-mode-grounding.md`](evidence/21-micron-1999-sdram-refresh-mode-grounding.md), uses Micron's November 1999 64Mb SDRAM product-family documentation to separate externally repeated nonpersistent `AUTO REFRESH` commands from CKE-entered `SELF REFRESH`, internal clocking during the retention mode, explicit `tXSR` exit, and return to externally issued refresh cadence. The broad item stays unchecked because a true JEDEC standards chronology, later DDR refresh semantics, per-bank refresh, temperature-compensated refresh, and retention-aware policy remain distinct open regimes;
- [x] ROM → PROM → EPROM → EEPROM → Flash — **the retention-specific bounded bridge is now closed through three grounded sub-slices plus the already-grounded mapped-Flash case**. [`cases/11-intel-frohman-floating-gate-eprom-erasure.md`](cases/11-intel-frohman-floating-gate-eprom-erasure.md) separates trapped-charge nonvolatility, avalanche-injection programming, nondestructive lower-stress read, and radiation erase. [`cases/12-intel-2816-eeprom-electrical-erasure.md`](cases/12-intel-2816-eeprom-electrical-erasure.md) moves erase into electrical/in-system control while preserving byte versus chip erase geometry, a distinct 21 V/timed erase-write regime, erase-before-write sequencing, and finite cycling. [`cases/13-early-flash-coarse-erase-asymmetric-rewrite.md`](cases/13-early-flash-coarse-erase-asymmetric-rewrite.md), grounded by [`evidence/13-early-flash-coarse-erase-1980-1988-grounding.md`](evidence/13-early-flash-coarse-erase-1980-1988-grounding.md), then grounds the device-level shift to shared/whole-array electrical erase with finer read/program selection and a one-transistor density objective. Case 04 separately grounds the historically later mapping/copy/reclaim response. This checkbox means the **bounded retention-mechanism bridge**, not an exhaustive genealogy of mask ROM, fuse PROM, every EEPROM family, NOR/NAND process history, or invention priority; those broader histories belong in `computing-archaeology` or dedicated future cases;
- [ ] HDD geometry, bad-sector remapping, CHS → LBA — **partially advanced by grounded bounded Case 14**: [`cases/14-scsi-disk-defect-reassignment-logical-identity.md`](cases/14-scsi-disk-defect-reassignment-logical-identity.md) uses 1990–1997 period-primary evidence to separate host LBA from physical target, manufacturer-defect slipping from grown-defect replacement, defect metadata from payload, and successful physical reassignment from payload preservation. Seagate's `REASSIGN BLOCKS` semantics make one LBA capable of traversing multiple physical addresses until spare locations are exhausted. The broad item stays unchecked because the general CHS→LBA interface chronology, earlier standards lineage, ATA/IDE transition, zone translation, and vendor-specific controller histories remain distinct work;
- [ ] virtual memory and paging — **partially advanced by grounded Case 22**: [`cases/22-ibm-system370-paging-backing-copy-currentness.md`](cases/22-ibm-system370-paging-backing-copy-currentness.md), grounded by [`evidence/22-ibm-1972-1976-paging-currentness-grounding.md`](evidence/22-ibm-1972-1976-paging-currentness-grounding.md), uses IBM OS/VS2 period documentation to separate virtual-page identity, real-frame residency, external-page-storage location, reference/change state, conditional page-out, and page-fault/page-in recovery. A changed selected page must be moved out before its frame is reused, while an unchanged page need not be moved when a usable external copy already exists. The broad item stays unchecked because Atlas→IBM genealogy, segmentation/DAT/TLB history, working-set/replacement policy, copy-on-write/demand-zero, Unix swap, memory-mapped files, and later VM semantics remain distinct regimes;
- [ ] file-system crash consistency — **partially advanced by grounded Case 16**: [`cases/16-bsd-ffs-soft-updates-crash-admissibility.md`](cases/16-bsd-ffs-soft-updates-crash-admissibility.md) uses 1999–2000 period-primary author/implementation evidence to separate volatile application-visible metadata, dependency-safe stable writeback, immediate crash-admissible mount state, explicit `fsync` durability closure, and later resource reclamation. The broad item stays unchecked because write-ahead logging/replay, copy-on-write/checkpoint consistency, transactional filesystems, modern `fsync`/rename semantics, and lower-layer device-persistence composition remain distinct regimes;
- [ ] SSD FTL/controller-mediated persistence beyond the bounded Ban/1990s case — **partially advanced by grounded Cases 15 and 20**. [`cases/15-intel-ssd320-power-loss-durability.md`](cases/15-intel-ssd320-power-loss-durability.md) uses 2007 ATA8-ACS standards-development text plus Intel's 2011 SSD 320 product/design material to separate volatile write-cache/temporary-buffer state, nonvolatile NAND, explicit `FLUSH CACHE` completion, orderly `STANDBY IMMEDIATE` handoff, and a power-failure-triggered capacitor-backed emergency transfer. [`cases/20-nvme10-fua-flush-persistence-ordering.md`](cases/20-nvme10-fua-flush-persistence-ordering.md), grounded by [`evidence/20-nvme10-2011-flush-fua-grounding.md`](evidence/20-nvme10-2011-flush-fua-grounding.md), separately uses the official ratified NVMe 1.0 specification to distinguish VWC classification, volatile→nonvolatile Flush, per-write FUA media commitment, cross-command ordering, and normal-versus-power-fail atomicity. The broad item stays unchecked because later NVMe persistence-domain terminology/revision history, controller-metadata recovery, enterprise PLP qualification, named-controller fault compliance, and filesystem/database composition remain distinct regimes; the independent FAST '13 fault-injection evidence in Case 15 remains a contract-versus-compliance boundary rather than silently assigned to a named product;
- [ ] RAID / scrubbing / rebuild — **partially advanced by grounded Cases 17 and 18**: [`cases/17-raid-parity-reconstruction-degraded-repair.md`](cases/17-raid-parity-reconstruction-degraded-repair.md) uses Ouchi’s 1977-filed IBM XOR/check-sum recovery patent and 1987–1994 Berkeley RAID sources to separate encoded reconstructability from replica multiplicity, physically present parity from parity currentness, request-time degraded service from completed background reconstruction, and spare capacity from payload. [`cases/18-zfs-scrub-latent-error-detection.md`](cases/18-zfs-scrub-latent-error-detection.md), grounded by [`evidence/18-zfs-scrub-2004-2010-grounding.md`](evidence/18-zfs-scrub-2004-2010-grounding.md), separately establishes proactive all-pool verification, checksum-qualified self-healing, latent-before-demand defects, and a scrub-versus-resilver distinction while preserving 2004 disk-scrubbing prior art. The broad item stays unchecked because double-parity/RAID-6, named production-controller rebuild/crash semantics, rebuild throttling, later URE-aware policy, and distributed scrub protocols remain distinct work;
- [ ] distributed replication and erasure coding beyond RADOS — **partially advanced by grounded Cases 19, 23, 24, 25, and 26**. [`cases/19-facebook-f4-erasure-coded-failure-domains.md`](cases/19-facebook-f4-erasure-coded-failure-domains.md), grounded by [`evidence/19-facebook-f4-2014-erasure-coding-grounding.md`](evidence/19-facebook-f4-2014-erasure-coding-grounding.md), separates Reed–Solomon fragment algebra from failure-domain placement, direct reads from online reconstruction, content repair from placement convergence, and local recovery from geo-level composition. [`cases/23-amazon-dynamo-divergent-version-anti-entropy.md`](cases/23-amazon-dynamo-divergent-version-anti-entropy.md), grounded by [`evidence/23-amazon-dynamo-2007-version-handoff-antientropy-grounding.md`](evidence/23-amazon-dynamo-2007-version-handoff-antientropy-grounding.md), adds mutable replicated currentness: causally unrelated versions can remain simultaneously admissible until reconciliation; hinted handoff separates successful availability from intended placement; and read repair plus Merkle-tree anti-entropy separate request completion, divergence detection, synchronization, and convergence. [`cases/24-windows-azure-lrc-repair-locality-handoff.md`](cases/24-windows-azure-lrc-repair-locality-handoff.md), grounded by [`evidence/24-windows-azure-2012-lrc-grounding.md`](evidence/24-windows-azure-2012-lrc-grounding.md), adds repair-cost geometry and a validated transition from full replication to coded retention for immutable sealed extents. [`cases/25-openstack-swift-ec-overwrite-durable-currentness.md`](cases/25-openstack-swift-ec-overwrite-durable-currentness.md), grounded by [`evidence/25-openstack-swift-2015-2016-ec-currentness-grounding.md`](evidence/25-openstack-swift-2015-2016-ec-currentness-grounding.md), adds a bounded mutable EC regime: same-timestamp distinct-index fragment cohorts and a `.durable` witness separate algebraic reconstructability from current-version admissibility, while the newer version must cross its commit boundary before older timestamped state is retired. [`cases/26-google-gfs-inactive-chunk-integrity.md`](cases/26-google-gfs-inactive-chunk-integrity.md), grounded by [`evidence/26-gfs-2003-integrity-scan-grounding.md`](evidence/26-gfs-2003-integrity-scan-grounding.md), adds distributed integrity qualification under replication: chunk-version currentness and per-copy checksum validity are separate, read-time validation can fall back before durable repair completes, and idle `scan and verify` work prevents an undiscovered corrupt replica from falsely satisfying the valid-replica goal. The broad item stays unchecked because other mutable-EC consistency protocols, delete/tombstone semantics, coded-fragment distributed integrity scrubbing, cross-region coded maintenance, later Swift durability-marker/on-disk evolution, later GFS/Colossus integrity semantics, and additional repair-bandwidth/failure models remain separate regimes. These systems build on earlier coding/replication techniques rather than supporting invention-priority claims for those ingredients.

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
- [ ] How should `command completion`, `volatile-cache residence`, `nonvolatile-media commitment`, `cross-command ordering`, and `power-fail atomicity` be separated at storage interfaces?
- [ ] How should `returned/visible`, `crash-admissible`, `explicitly durable`, and `reclaimed/converged` be separated in filesystem regimes?
- [ ] How should `encoded reconstructability`, `degraded-service continuity`, and `restored redundancy margin` be separated in coded-storage regimes?
- [ ] How should `physical presence`, `verified integrity`, `defect discovery`, `repairability`, and `restored redundancy` be separated in proactively checked storage?
- [ ] In distributed integrity maintenance, how should `version currentness`, `checksum validity`, `demand-time versus idle-time discovery`, `fallback read availability`, `valid-replica count`, `clone repair`, and `restored replication goal` be separated?
- [ ] In distributed coded storage, how should `coded recoverability`, `read availability`, `full-fragment repair`, and `restored failure-domain placement` be separated?
- [ ] In locality-aware coded storage, how should `recoverability`, `reconstruction read-set/cost`, `on-demand read recovery`, `durable fragment repair`, and `redundancy-regime handoff completion` be separated?
- [ ] In mutable erasure-coded object storage, how should `fragment presence`, `version/timestamp coherence`, `coded reconstructability`, `commit/durability evidence`, `old-version retirement`, and `repair convergence` be separated?
- [ ] In divergent-version replication, how should `causally superseded`, `concurrent/admissible`, `returned`, `read-repaired`, `anti-entropy synchronized`, and `placement-converged` states be separated?
- [ ] In refresh-driven memory, how should `retention deadline`, `row enumeration`, `recurring command generation`, `self-refresh mode authority`, `ordinary service availability`, and `exit/recovery timing` be separated?
- [ ] In paging, how should `virtual designation`, `real-frame residency`, `backing-copy currentness`, `external-location state`, `page-out obligation`, and `page-fault recovery` be separated?

The first direct Ernst test is now complete; later work in this phase should reuse its timescale decomposition rather than treating `microtemporality` as a catch-all answer.

The grounded flip-flop stress test adds one concrete correction for this phase: a later retained-state relation need not appear as a discrete `retrieve` operation. In the ENIAC static-output and carry cases, a state can remain continuously available at a circuit output and become significant only when a later gate/pulse acts on it. Part II p. IV-43 adds a second boundary case: an external switch event can be retained in one flip-flop, transferred into a machine-timed flip-flop by a later central programming pulse, and only then drive a reliable transmitter action. Burks 1947 adds a third: even a microsecond-scale state has separate stability, transition, and recovery constraints. Future boundary work should therefore test **later state-sensitive use**, **event/timing retention**, and **state-holding versus transition/recovery** alongside explicit recovery/read operations. Modern clock-domain/metastability language remains analogy, not 1946 vocabulary.

The grounded static-MOS bridge adds two further controls. First, `power dependence` is not one Boolean property: Intel's 5101L documentation separates a lower-voltage state-retention condition from ordinary active operation and defines an operation-recovery relation between them. Second, Pashley's 1975 Intel filing separates the bistable cell from X/Y selection, column sensing, read-bus, output, write, and address-transition machinery. Future boundary work should therefore compare **retention-supporting supply**, **active-operation supply**, **transition/recovery between power modes**, and **state survival versus selection/sensing recoverability** rather than treating `volatile/static`, `needs power`, or `cell still holds a bit` as sufficient service descriptors.

The grounded Model 85 cache bridge adds the architectural layer that the SRAM case intentionally excluded. Program-visible main-storage addresses remain stable while fast-copy residency changes; a cache hit requires retained sector correspondence plus per-block validity; processor/channel stores maintain the currentness of already resident copies; and replacement can deliberately end cache-copy retention without losing authoritative main-storage state. Future cache-boundary work must therefore distinguish **payload retention**, **copy identity/correspondence**, **validity/currentness**, **replacement-policy state**, and **authority**. Later write-back caches should be allowed to break the Model 85 result by introducing cache-local dirty/authoritative state rather than being forced into a write-through model.

The grounded EPROM bridge adds a different access/control boundary. An insulated floating gate can retain state without continuous operating power, X/Y electrical selection can program and nondestructively read cells, yet the bounded erase path can be radiation applied to the physical device rather than an ordinary addressed electrical command. The grounded EEPROM bridge then changes that partition: Intel's 2816 makes byte erase/write electrically and in-system controllable, but READ, BYTE ERASE, BYTE WRITE, and CHIP ERASE remain distinct modes; erase/write still requires elevated VPP and millisecond timing, byte rewrite is erase-before-write, and finite cycling makes repeated alteration a lifetime constraint. The grounded early-Flash bridge adds the next correction: electrical control can deliberately become **coarser** at erase time while read/program remain finer, and whole-array erase can still require address-by-address verification. Future semiconductor comparisons should therefore separate **hold**, **read**, **program**, **erase authority**, **erase granularity**, **verification granularity**, **exceptional-operation infrastructure**, and **endurance** rather than assuming `electrically erasable` describes one uniform operation.

The grounded HDD defect-reassignment bridge adds a second, non-Flash form of logical/physical indirection. A host can continue naming the same LBA after the controller changes its physical sector, but Seagate's command semantics explicitly allow the remap to succeed without preserving the affected payload. Future address/identity work must therefore separate **designation continuity**, **physical-embodiment continuity**, **payload continuity**, **repair metadata**, and **finite replacement capacity**. The comparison to mapped Flash is useful only at that relational level: failure-triggered spare substitution is not erase-driven FTL relocation.

The grounded SSD power-loss bridge adds a durability boundary that neither Flash-cell nonvolatility nor FTL mapping alone supplies. A host-visible write can pass through volatile cache/temporary buffers before becoming recoverable nonvolatile state; `FLUSH CACHE`, orderly shutdown, and unexpected-power-loss protection are distinct transition authorities; and a capacitor can retain only energy while still being constitutive infrastructure for preserving payload and system state. Future boundary work should therefore separate **write acknowledgement**, **visibility**, **volatile staging**, **flush completion**, **nonvolatile-media residency**, **post-restart logical currentness**, and **fault-path compliance** rather than treating `SSD is nonvolatile` as an end-to-end persistence claim.

The grounded NVMe 1.0 interface bridge sharpens that device boundary without repeating Case 15's product mechanism. Revision 1.0 exposes VWC, Flush, FUA, AWUN, and AWUPF as distinct interface relations; a FUA Write must reach nonvolatile media before that command completes but explicitly carries **no implied ordering with other commands**; required ordering among independent commands remains a host/application responsibility; and a cache guaranteed to drain on power loss is considered nonvolatile for the VWC feature even though the standard does not prescribe the underlying physical mechanism. Future persistence work should therefore separate **generic command completion**, **per-command media-commit guarantee**, **cache-class transition**, **cross-command ordering**, **normal atomicity**, **power-fail atomicity**, and **empirical implementation compliance**. Later `persistence domain` terminology should be sourced in its own revision-specific case rather than projected back onto 2011.

The grounded Micron SDRAM refresh-mode bridge adds a reversible maintenance-authority boundary to the earlier DRAM cases. In normal operation, Micron calls `AUTO REFRESH` nonpersistent: external control must issue each refresh command while the internal controller/counter supplies row addressing. In `SELF REFRESH`, CKE-controlled entry lets the device provide its own internal clocking and recurring refresh cycles; normal inputs cease to matter; exit requires stable CLK and `tXSR` before externally issued AUTO REFRESH resumes. Future DRAM work should therefore keep **refresh deadline**, **row enumeration**, **recurring event generation**, **mode authority**, **retention availability**, **ordinary read/write availability**, and **service-recovery timing** distinct. This manufacturer-product case does not substitute for a JEDEC standards chronology.

The grounded BSD FFS soft-updates bridge adds a higher-level crash-admissibility boundary. The newest application-visible metadata may exist only in volatile memory while the disk is deliberately kept at an older or partially advanced state that still satisfies pointer/allocation invariants. `fsync` then requests a stronger closure that reaches across payload, allocation maps, indirection, inode, and naming state, while later `fsck` reclamation can remain outstanding after service resumes. Future filesystem comparisons should therefore distinguish **returned/visible state**, **crash-admissible stable state**, **explicit durability closure**, **recovery/replay state**, and **post-crash reclamation/convergence**. This layer must be composed with, not substituted for, the device-level flush/FUA boundaries grounded in Cases 15 and 20.

The grounded RAID parity-reconstruction bridge adds an encoded-redundancy boundary. A missing disk contribution can remain logically recoverable even when no complete duplicate survives, because parity/checksum plus the other members constrain a reconstruction. Chen et al. further show that the array may serve degraded requests while whole-member reconstruction is still incomplete, and that parity/sector validity plus reconstruction progress are retained `meta state`. Future redundancy comparisons should therefore distinguish **copy multiplicity**, **encoded reconstructability**, **currentness/validity of redundancy**, **repair frontier**, **spare/replacement capacity**, and **restored future failure margin**. This is functionally comparable to RADOS repair and HDD spare substitution but not historically or mechanically identical to either.

The grounded ZFS scrubbing bridge adds a proactive-verification boundary before the known-failure/rebuild state. The bounded documentation lets defects be encountered either through ordinary demand or through an explicit whole-pool scrub; filesystem-layer checksums help decide whether returned blocks are acceptable; and a trustworthy redundant copy permits self-healing after detection. Resilvering remains a separate device-restoration process whose completion restores the desired redundancy state. Future maintenance comparisons should therefore distinguish **defect existence**, **defect discovery**, **integrity verification**, **conditional repair**, **proactive scan coverage**, and **rebuild/resilver completion**. Unlike DRAM refresh, scheduled scrub work need not rewrite healthy retained state; unlike Case 17 reconstruction, it can discover a problem before a member is already known failed.

The grounded f4 distributed-erasure bridge adds a topological repair boundary beyond disk-array coding. Reed–Solomon `(10,4)` determines which fragment sets can reconstruct data, but the system separately tries to distribute stripe members across racks and repairs placement violations after failure/reconstruction/replacement. A failure-case read can reconstruct only the requested BLOB before the full missing block is rebuilt, and full content repair can still precede restoration of the intended failure-domain geometry. Geo-XOR recovery can in turn depend on lower-level Reed–Solomon reconstruction of its inputs. Future distributed-storage comparisons should therefore separate **coding algebra**, **failure-domain placement**, **requested-object read availability**, **full-fragment repair**, **placement convergence**, and **cross-layer reconstruction composition**.

The grounded Windows Azure LRC bridge adds a repair-cost and representation-transition boundary to the distributed-coded cases. The 2012 production design makes `reconstruction cost` an explicit code property, yet separately places fragments across hardware fault domains and planned upgrade domains; a smaller dependency set is therefore not a claim of physical co-location. It also keeps sealed extents under full replication while asynchronous coding proceeds, persists conversion progress for resumption, validates reconstructed data/CRC before completion, records fragment boundaries/completion flags, and only then schedules the old replicas for deletion. Future coded-storage work should therefore distinguish **mathematical recoverability**, **repair read-set/cost**, **foreground reconstruction availability**, **durable fragment repair**, **physical/administrative placement**, and **representation-handoff admissibility**. Mutable coded-object currentness remains open.

The grounded OpenStack Swift EC bridge adds the mutable coded-currentness relation that the f4 and WAS cases intentionally left open. In the bounded 2015–2016 implementation, fragment archives can exist before a PUT is committed; GET requires enough distinct fragment indexes at one timestamp plus same-timestamp durability evidence; and the previous timestamp is not deleted until the replacement crosses the multi-phase commit boundary. Later reconstruction can still propagate missing fragments and durability markers. Future coded-storage work should therefore distinguish **fragment existence**, **version coherence**, **algebraic reconstructability**, **commit/admissibility state**, **source-version retirement**, and **repair convergence**, while keeping release-specific quorum rules explicit rather than treating `Swift EC durability` as one timeless property.

The grounded IBM OS/VS2 paging bridge adds a capacity-triggered embodiment-replacement boundary. A virtual page can leave one real page frame without ceasing to be the current page, but the safe transition depends on whether the real copy has changed relative to a usable external copy. Changed pages must be propagated before frame reuse; unchanged pages can relinquish the frame without another page-out when the external copy is already sufficient. RSM/ASM separately retain residency/translation and auxiliary-location state, while a later page fault triggers page-in before ordinary service resumes. Future hierarchy work should therefore distinguish **virtual designation**, **real residency**, **copy currentness**, **backing location**, **replacement obligation**, **recovery latency**, and **crash durability**. This is functionally comparable to cache eviction, Flash relocation, and HDD reassignment only at the relation level; the triggers and historical mechanisms remain distinct.

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
- [ ] FUA/Flush misuse, missing host-enforced ordering, or power-fail atomicity assumptions that exceed the interface contract;
- [ ] unsafe filesystem dependency ordering or incomplete durability closure;
- [ ] post-crash resource leakage / unreclaimed allocation state;
- [ ] inconsistent parity, stale/invalid reconstruction state, second failure before rebuild, or unreadable surviving data needed for reconstruction;
- [ ] latent integrity defect remaining undiscovered until another failure removes the available repair path;
- [ ] coded-fragment loss concentrated in one failure domain, incomplete rebuild, or placement violation that silently reduces future repair margin;
- [ ] failed/asynchronous redundancy-mode conversion, stale/incomplete completion metadata, or deleting source replicas before coded-state validation;
- [ ] cross-timestamp fragment mixing, missing durability witness, stale pre-commit fragments, or premature old-version retirement during mutable EC overwrite;
- [ ] missed externally issued refresh cadence, failed self-refresh entry, loss of the powered self-refresh regime, or premature service resumption across a refresh-mode exit;
- [ ] reusing a changed real page frame before required page-out, stale/lost residency or auxiliary-location state, backing-store exhaustion, or page-in failure;
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
- external AUTO REFRESH scheduling, CKE-controlled self-refresh entry/exit, internal self-refresh clocking, and service-resumption timing;
- storage controllers;
- ECC;
- disk servo systems;
- disk defect-list maintenance, spare allocation, and reallocation;
- SSD firmware, reclamation, wear management, bad-block replacement;
- volatile write-cache / temporary-buffer handoff;
- host-issued flush or orderly-shutdown commands;
- per-write FUA, host/application ordering enforcement, and controller-reported power-fail atomicity;
- power-fail detection, supply isolation, hold-up energy, and emergency NAND transfer;
- filesystem dependency tracking and dependency-safe writeback;
- explicit durability closure such as bounded `fsync` work;
- post-crash mount-time reconstruction and background resource reclamation;
- page-frame selection/reclamation, reference/change tracking, conditional page-out, page-fault/page-in recovery, and auxiliary-location bookkeeping;
- parity validity/currentness bookkeeping;
- failure detection and invalidation in redundant arrays;
- demand reconstruction, background rebuild, and spare provisioning;
- data scrubbing, checksum verification, and conditional self-healing;
- erasure-coded online sub-object reconstruction, full-fragment rebuild, and failure-domain placement balancing;
- asynchronous replica-to-erasure-code conversion, coding-progress persistence, validation-gated source-replica deletion, locality-aware reconstruction, and fault/upgrade-domain placement;
- timestamp-cohort selection, `.durable`-marker propagation, EC reconstruction, handoff reversion, and stale pre-commit fragment cleanup;
- geo-level coded recovery composed with lower-level reconstruction;
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

**Grounded DRAM refresh-responsibility continuation:** Cases [`09`](cases/09-dram-cbr-refresh-address-internalization.md), [`10`](cases/10-toshiba-leakage-tracked-self-refresh.md), and [`21`](cases/21-micron-sdram-refresh-mode-handoff.md) are `grounded`. Together they separate the physical refresh deadline from row enumeration, externally supplied trigger cadence, on-chip scheduling, condition-derived triggering, and a later product-interface handoff between externally repeated AUTO REFRESH and CKE-controlled SELF REFRESH. Case 21 additionally separates retained payload from ordinary service availability during the low-power mode and makes `tXSR` part of service restoration. These cases do not close the broad history of standardized JEDEC refresh interfaces, per-bank refresh, or later retention-aware policies.

**Grounded floating-gate EPROM stress test:** [`cases/11-intel-frohman-floating-gate-eprom-erasure.md`](cases/11-intel-frohman-floating-gate-eprom-erasure.md) is `grounded`; see [`evidence/11-intel-1970-1971-floating-gate-eprom-grounding.md`](evidence/11-intel-1970-1971-floating-gate-eprom-grounding.md). It adds quiescent trapped-charge nonvolatility together with an explicit separation among avalanche programming, nondestructive read, and radiation erase. The key correction is that **nonvolatility is not immutability and access geometry need not equal erase geometry**.

**Grounded EEPROM electrical-erasure stress test:** [`cases/12-intel-2816-eeprom-electrical-erasure.md`](cases/12-intel-2816-eeprom-electrical-erasure.md) is `grounded`; see [`evidence/12-intel-1978-1981-eeprom-electrical-erasure-grounding.md`](evidence/12-intel-1978-1981-eeprom-electrical-erasure-grounding.md). The Intel 2816 product evidence makes electrical erase callable at byte granularity and also exposes whole-chip erase, while keeping erase/write distinct from ordinary read through VPP, timing, mode sequencing, and finite cycling. The source pair therefore adds **electrical erasure ≠ ordinary service equivalence**, **electrical erasability ≠ one erase geometry**, **erase-before-write can make forgetting part of update**, and **nonvolatility ≠ unlimited mutability**.

**Grounded early-Flash erase-geometry stress test:** [`cases/13-early-flash-coarse-erase-asymmetric-rewrite.md`](cases/13-early-flash-coarse-erase-asymmetric-rewrite.md) is `grounded`; see [`evidence/13-early-flash-coarse-erase-1980-1988-grounding.md`](evidence/13-early-flash-coarse-erase-1980-1988-grounding.md). Toshiba and Intel manufacturer-primary evidence grounds one-transistor density pressure, shared/whole-array electrical erase, finer addressed program/read, command control, and address-walking verify/retry. It forces three new separations: **program addressability ≠ erase addressability**, **fast bulk erase ≠ fast arbitrary rewrite**, and **erase asymmetry ≠ FTL**. Masuoka 1984 and Kynett 1988 full facsimiles remain archival cleanup; their indexed abstracts are not treated as figure-level inspection.

**Grounded HDD defect-reassignment stress test:** [`cases/14-scsi-disk-defect-reassignment-logical-identity.md`](cases/14-scsi-disk-defect-reassignment-logical-identity.md) is `grounded`; see [`evidence/14-disk-lba-defect-reassignment-1990-1997-grounding.md`](evidence/14-disk-lba-defect-reassignment-1990-1997-grounding.md). Period NeXT/Seagate evidence shows that a stable LBA can traverse physical sectors after defects while `REASSIGN BLOCKS` itself does not preserve the affected payload. It also makes defect-list state and finite spare capacity part of the continuation mechanism. The case therefore forces **logical-block identity ≠ physical-sector identity**, **reassignment continuity ≠ payload continuity**, and **LBA abstraction ≠ disappearance of geometry**, while keeping the comparison to Flash FTL explicitly functional rather than genealogical.

**Grounded SSD power-loss-durability stress test:** [`cases/15-intel-ssd320-power-loss-durability.md`](cases/15-intel-ssd320-power-loss-durability.md) is `grounded`; see [`evidence/15-intel-ssd320-power-loss-durability-grounding.md`](evidence/15-intel-ssd320-power-loss-durability-grounding.md). Period ATA text and Intel product/design evidence put a volatile staging layer in front of nonvolatile NAND and distinguish host-requested flush, clean-shutdown transfer, and device-triggered emergency work under stored capacitor energy. FAST '13 is used only as an independent boundary against equating interface/design claims with measured compliance. This case adds **nonvolatile medium ≠ end-to-end durable state**, **stored energy ≠ stored payload**, and **durability handoff ≠ ordinary media retention**.

**Grounded NVMe 1.0 persistence-semantics stress test:** [`cases/20-nvme10-fua-flush-persistence-ordering.md`](cases/20-nvme10-fua-flush-persistence-ordering.md) is `grounded`; see [`evidence/20-nvme10-2011-flush-fua-grounding.md`](evidence/20-nvme10-2011-flush-fua-grounding.md). The official 2011 Revision 1.0 specification directly grounds VWC, Flush, Write FUA, host/application ordering responsibility, and distinct AWUN/AWUPF values. FUA requires one write to reach nonvolatile media before that command completes while explicitly providing no implied ordering with other commands; the VWC feature separately treats a cache with a guaranteed power-loss drain as nonvolatile for that interface feature. This case therefore forces **command completion ≠ media persistence unless the applicable contract establishes it**, **per-command persistence ≠ cross-command ordering**, **Flush ≠ FUA**, **interface volatility class ≠ simple substrate class**, and **normal atomicity ≠ power-fail atomicity**. Later `persistence domain` terminology remains a separate revision-specific question.

**Grounded SDRAM refresh-mode stress test:** [`cases/21-micron-sdram-refresh-mode-handoff.md`](cases/21-micron-sdram-refresh-mode-handoff.md) is `grounded`; see [`evidence/21-micron-1999-sdram-refresh-mode-grounding.md`](evidence/21-micron-1999-sdram-refresh-mode-grounding.md). Micron's Rev. 11/99 64Mb SDRAM document directly grounds a nonpersistent normal AUTO REFRESH command, internal refresh-row addressing, CKE-controlled SELF REFRESH entry, internal clocking/refresh while that mode is active, explicit `tXSR` exit, and resumption of externally issued AUTO REFRESH. The case therefore forces **refresh obligation ≠ recurring command-generation responsibility**, **internal refresh addressing ≠ autonomous recurrence**, **retention availability ≠ ordinary service availability**, and **self-refresh autonomy ≠ nonvolatility**. A full JEDEC standards genealogy remains separate.

**Grounded virtual-memory paging stress test:** [`cases/22-ibm-system370-paging-backing-copy-currentness.md`](cases/22-ibm-system370-paging-backing-copy-currentness.md) is `grounded`; see [`evidence/22-ibm-1972-1976-paging-currentness-grounding.md`](evidence/22-ibm-1972-1976-paging-currentness-grounding.md). IBM's 1972 OS/VS2 Planning Guide and 1976 System Logic Library directly separate virtual pages, real page frames, external page storage, reference/change state, RSM/ASM responsibility, dynamically allocated page-data-set slots, conditional page-out, and page-fault/page-in recovery. The bounded mechanism forces **virtual-page identity ≠ frame identity ≠ backing-slot identity**, **residency ≠ currentness**, **frame reassignment ≠ forgetting**, **page replacement ≠ unconditional page-out**, and **working backing storage ≠ crash-durable application retention**. Atlas 1962 supplies prior-art control without establishing direct genealogy.

**Grounded filesystem crash-admissibility stress test:** [`cases/16-bsd-ffs-soft-updates-crash-admissibility.md`](cases/16-bsd-ffs-soft-updates-crash-admissibility.md) is `grounded`; see [`evidence/16-bsd-ffs-soft-updates-1999-2000-grounding.md`](evidence/16-bsd-ffs-soft-updates-1999-2000-grounding.md). McKusick/Ganger 1999 and Ganger et al. 2000 make the stable retention target a dependency-safe filesystem image rather than simply the newest visible operation. Fine-grained dependency state shapes delayed writeback through temporary rollback/roll-forward; immediate post-crash service can coexist with unclaimed resources; and `fsync` drives a broader payload-plus-metadata closure. This case therefore forces **application-visible currentness ≠ crash-admissible stable state**, **safe mountability ≠ newest-operation durability**, **consistency-control metadata ≠ necessarily persistent recovery metadata**, and **filesystem durability closure ≠ device flush boundary**.

**Grounded parity-reconstruction stress test:** [`cases/17-raid-parity-reconstruction-degraded-repair.md`](cases/17-raid-parity-reconstruction-degraded-repair.md) is `grounded`; see [`evidence/17-raid-parity-reconstruction-1977-1994-grounding.md`](evidence/17-raid-parity-reconstruction-1977-1994-grounding.md). Ouchi’s 1977-filed IBM patent grounds XOR/check-sum recovery across failure-independent storage units before the RAID name; Patterson/Gibson/Katz ground the later RAID nomenclature; Chen et al. ground validity/currentness meta state, parity-consistency state, demand reconstruction, stand-by spares, and background reconstruction. This case therefore forces **parity redundancy ≠ replica multiplicity**, **degraded service continuity ≠ restored redundancy margin**, **physically present parity ≠ usable current redundancy**, and **repair progress/spare capacity can be constitutive retention infrastructure**.

**Grounded proactive-scrubbing stress test:** [`cases/18-zfs-scrub-latent-error-detection.md`](cases/18-zfs-scrub-latent-error-detection.md) is `grounded`; see [`evidence/18-zfs-scrub-2004-2010-grounding.md`](evidence/18-zfs-scrub-2004-2010-grounding.md). Official Solaris ZFS documentation directly grounds explicit whole-pool scrubbing, filesystem-layer checksumming/self-healing, and device-replacement resilvering; Schwarz et al. 2004 prevents a false ZFS-invention narrative; independent latent-sector-error work supports the category of damage that exists before access reveals it. This case therefore forces **physical presence/readability ≠ verified integrity**, **redundancy availability ≠ defect discovery**, **detection work ≠ repair work**, **scrub ≠ rebuild/resilver**, and **scheduled maintenance ≠ periodic restoration of every healthy state**.

**Grounded distributed-erasure-coding stress test:** [`cases/19-facebook-f4-erasure-coded-failure-domains.md`](cases/19-facebook-f4-erasure-coded-failure-domains.md) is `grounded`; see [`evidence/19-facebook-f4-2014-erasure-coding-grounding.md`](evidence/19-facebook-f4-2014-erasure-coding-grounding.md). Facebook's 2014 f4 paper directly grounds Reed–Solomon `(10,4)` data stripes, separately triple-replicated index files, rack-aware block placement, sub-BLOB online reconstruction, offline full-block rebuilding, placement balancing after reconstruction/replacement, and a geo-XOR layer whose inputs can themselves require local reconstruction. The case therefore forces **erasure-code algebra ≠ failure-domain independence**, **read availability ≠ completed repair**, **content reconstruction ≠ restored placement geometry**, and **one system can use different redundancy mechanisms for different constitutive state classes**. Its related-work section explicitly prevents a false coding-invention claim.

**Next highest-value unit:** the Phase-1 evidence set is fully grounded, and Cases 21–22 have separately grounded refresh-mode responsibility handoff and capacity-triggered paging currentness. Prefer a new bounded bridge that adds a genuinely different retention relation: a **mutable coded-object currentness** case, a **local-reconstruction-code repair-geometry** case, **distributed scrub/anti-entropy**, or a revision-specific **later NVMe persistence-domain** case if primary normative text changes the failure/persistence comparison. Do not reopen the IBM paging, mercury-delay-line, or Micron SDRAM cases merely to accumulate generic technology history.

The first generic thesis-audit sequence, four named philosophical/prior-art tests, the first category-coherence audit, and the post-audit technical stress tests are now grounded at bounded maturity. Do not promote the bounded relational criterion into a grand `What Is Technical Retention?` chapter yet. Cases 06–22 continue to add counterexample pressure: short working-state retention, static-array power boundaries, cache currentness, refresh-responsibility migration, condition-derived maintenance, **mode-mediated and reversible refresh responsibility**, **retention availability versus ordinary service availability**, external-versus-electrical erase authority, erase granularity, verification granularity, endurance, logical/physical disk indirection, payload-recovery separation, finite repair slack, volatile durability windows, explicit flush boundaries, failure-triggered emergency handoff, per-command FUA media commitment, host-enforced ordering, power-fail atomicity, crash-admissible stable state, relational `fsync` closure, encoded reconstruction, redundancy-currentness metadata, degraded-versus-repaired fault margin, proactive integrity verification before demand, failure-domain placement, sub-object online reconstruction, background full-fragment repair, placement-geometry convergence, and **virtual-page identity across real-frame replacement with conditional backing-store propagation** must all remain distinct.

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
