# Related Repositories

`technical-retention` is designed as a conceptual bridge across existing projects, not a replacement for them.

## 1. computing-archaeology

<https://github.com/tmzncty/computing-archaeology>

### Role

Primary companion for technical history and engineering reconstruction.

Its question is roughly:

> Why did a historical computing design make sense under its period material, manufacturing, cost, speed, interface, and operational constraints?

It already contains a substantial `docs/memory/` track covering delay lines, Williams tubes, drums, magnetic core, tape, disk, HBM, and related topics, while its audit identifies semiconductor memory and later storage geometry as important work still to deepen.

### Reuse rule

If the historical mechanism is already explained there, `technical-retention` should **link and analyze**, not copy and paraphrase the same technical history.

If new research mainly improves the historical engineering account, contribute it there first.

### Current bounded reuse example

Case 02 now uses [`evidence/02-whirlwind-1953-1954-marginal-checking-recovery-copy-deepening.md`](evidence/02-whirlwind-1953-1954-marginal-checking-recovery-copy-deepening.md) only for the retention-specific boundary between **diagnostic disturbance** and **recovery-copy staging** in 1953–1954 Whirlwind I marginal checking. The broad magnetic-core mechanism, Whirlwind deployment, manufacturing, and engineering context remain in [`computing-archaeology/docs/memory/why-core-memory-was-worth-weaving.md`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md) rather than being duplicated here.

Case 04 now keeps two bounded TrueFFS seams in this repository. [`evidence/04-m-systems-2001-2003-interrupted-erase-recovery-deepening.md`](evidence/04-m-systems-2001-2003-interrupted-erase-recovery-deepening.md) isolates **interruptible destructive erase → retained pending/completion evidence → conservative restart replay → re-established physical-space reuse authority**. [`evidence/04-trueffs-2003-2004-mapping-power-failure-reconstruction-deepening.md`](evidence/04-trueffs-2003-2004-mapping-power-failure-reconstruction-deepening.md) separately isolates **verified replacement → Flash-resident mapping/currentness evidence → reset-time rebuild/verification of the volatile RAM map → recovered logical resolution authority**. Fresh companion searches found no dedicated TrueFFS packet to reuse. Broad TrueFFS/DiskOnChip chronology, on-media format genealogy, Flash erase-circuit history, M-Systems patent-family lineage, and later SSD-FTL crash-consistency history remain `computing-archaeology` work rather than being duplicated here.

Case 43 now uses [`evidence/43-avatar-rrt-same-substrate-metadata-protection-deepening.md`](evidence/43-avatar-rrt-same-substrate-metadata-protection-deepening.md) only for the retention-specific seam between **row-refresh policy authority**, **the RRT's physical embodiment**, **same-substrate VRT exposure of policy metadata**, **triplicated metadata protection**, and the separate problem of **semantic revalidation when row behavior changes**. A fresh companion search found no dedicated AVATAR/VRT/RAIDR packet to reuse. Broad retention-aware-refresh history, memory-controller metadata structures, VRT device physics, and commercial-adoption archaeology remain `computing-archaeology` work rather than being duplicated here.

Case 127 now uses [`evidence/127-2015-2016-ddr3-scrambling-semantic-recovery-deepening.md`](evidence/127-2015-2016-ddr3-scrambling-semantic-recovery-deepening.md) only for the retention-specific seam between **physical DRAM remanence**, **controller-scrambled physical representation**, **scrambler/interleaving interpretation state**, and **semantic reconstruction after reset, cold start, or module transplant**. Fresh companion searches for the Link/May title and cryogenic DRAM found no dedicated packet to reuse. Broad DDR memory-scrambling history, Intel memory-controller genealogy, DDR3/DDR4 platform evolution, and cold-boot-forensics tooling remain `computing-archaeology` work rather than being duplicated here.

Case 38 now uses [`evidence/38-intel-s3700-sct-test-cadence-persistence-boundary-deepening.md`](evidence/38-intel-s3700-sct-test-cadence-persistence-boundary-deepening.md) only for the retention-specific seam between **PLI readiness evidence**, **test-cadence policy**, **current versus saved/nonvolatile Feature Control state**, and the still-unverified **device-specific D000h reset/power-cycle behavior**. Fresh companion searches found no dedicated S3700 / capacitor-PLI packet to reuse. Broad SCT/Software-Settings-Preservation genealogy, enterprise-SSD management-control history, and capacitor-PLP product archaeology remain `computing-archaeology` work rather than being duplicated here.

Case 142 now uses [`evidence/142-ceph-reef-mclock-maintenance-scheduling-boundary-deepening.md`](evidence/142-ceph-reef-mclock-maintenance-scheduling-boundary-deepening.md) only for the retention-specific seam between **repair obligation**, **capacity/reservation admission**, **scheduler service class/resource allocation**, and **repair completion** in the bounded Reef `v18.2.0` baseline. A fresh companion search found no dedicated Ceph mClock recovery/backfill module to reuse. The broad dmClock/mClock algorithm history, pre-Pacific/Pacific/Quincy/Reef scheduler evolution, and benchmark/performance archaeology remain `computing-archaeology` work rather than being duplicated here.

Case 42 now uses [`evidence/42-kafka-081-cleaner-checkpoint-restart-currentness-deepening.md`](evidence/42-kafka-081-cleaner-checkpoint-restart-currentness-deepening.md) only for the retention-specific seam between **cleaner progress checkpoint**, **reconstructed latest-key working state**, **runtime cleaner state**, **segment-swap recovery**, and **checkpoint currentness after log geometry changes**. A fresh companion search found no dedicated Kafka cleaner-checkpoint packet to reuse. A broad Kafka log-cleaner/segment-format/Databus engineering history remains `computing-archaeology` work rather than being duplicated here.

Case 134 now uses [`evidence/134-cypress-copyback-interruption-quarantine-deepening.md`](evidence/134-cypress-copyback-interruption-quarantine-deepening.md) only for the retention-specific seam between **COPYBACK source integrity**, **destination-program completion**, **post-interruption quarantine/reuse admission**, and **restart-visible evidence that an operation was not proven complete**. A fresh companion search found no dedicated NAND copyback packet to reuse. Broader COPYBACK command genealogy, ONFI/Toggle standardization, page-buffer architecture, and controller-adoption history remain `computing-archaeology` work rather than being duplicated here.

Case 148 now uses [`evidence/148-ulink-2026-lexar-dst-controller-reset-conformance-deepening.md`](evidence/148-ulink-2026-lexar-dst-controller-reset-conformance-deepening.md) only for the retention-specific evidence boundary between a **normative reset-surviving maintenance contract**, a **named-product feature witness**, a **named third-party controller-reset conformance result**, and the still-undisclosed **internal resume/checkpoint embodiment**. A fresh companion search found no dedicated NVMe Device Self-test packet to reuse. Broad ATA/SCSI/NVMe diagnostic-command genealogy, conformance-tool history, TP001a drafting history, and vendor firmware archaeology remain `computing-archaeology` work rather than being duplicated here.

Case 149 now uses [`evidence/149-micron-2012-2015-otp-mode-vs-protection-persistence-deepening.md`](evidence/149-micron-2012-2015-otp-mode-vs-protection-persistence-deepening.md) only for the retention-specific boundary between **volatile OTP/access-mode selection** and the separately established **irreversible OTP mutation-authority relation**. Fresh companion searches found no dedicated Micron NAND OTP / `OTP DATA PROTECT` packet to reuse. Broad NAND OTP/security-register genealogy, ONFI committee evolution, exact lock-cell circuitry, physical attack work, and controller-driver history remain `computing-archaeology` work rather than being duplicated here.

Case 152 now uses [`evidence/152-sqlite-wal-recovery-backfill-progress-reset-deepening.md`](evidence/152-sqlite-wal-recovery-backfill-progress-reset-deepening.md) only for the retention-specific seam between **authoritative committed WAL evidence**, **reconstructed WAL geometry**, **discardable checkpoint-progress state**, and **re-established WAL reuse authority** after restart. A fresh companion search for `SQLite` found no dedicated SQLite WAL/checkpoint packet to reuse. Broad System R/ARIES/WAL genealogy, SQLite pager and Fossil-check-in history, VFS evolution, and later checkpoint-mode history remain `computing-archaeology` work rather than being duplicated here.

---

## 2. problem-history

<https://github.com/tmzncty/problem-history>

### Role

Methodological companion.

Its strongest transferable rule is:

> Prove that historical actors had a problem before attributing our modern formulation of that problem to them.

This protects `technical-retention` from claims such as:

- `the abacus was already a register`;
- `ancient record keeping was already database storage`;
- `Babbage anticipated every modern memory abstraction`.

Such comparisons may be useful functional analogies, but they are not automatically historical continuities.

---

## 3. mechanical-computing-playground

<https://github.com/tmzncty/mechanical-computing-playground>

### Role

Hands-on reconstruction, simulation, and mechanism demonstration.

Examples of work that might belong there:

- a mechanical retained-state demonstrator;
- a simple counter or carry mechanism;
- a physical or executable comparison of destructive versus nondestructive read;
- a small model showing recirculating memory.

`technical-retention` can then cite the experiment when making the conceptual comparison.

---

## 4. old-web-archaeology

<https://github.com/tmzncty/old-web-archaeology>

### Role

Concrete historical web-preservation and reconstruction companion.

Its scope is roughly:

> What did the Chinese web of roughly 1995–2015 actually leave behind, why did parts disappear, and what can surviving captures, software, browser assumptions, screenshots, link structures, and other evidence justify reconstructing?

This makes it especially relevant when `technical-retention` reaches long-term access problems involving file formats, character encodings, browser engines, plug-ins, scripts, network dependencies, missing resources, or reconstruction from incomplete captures.

### Reuse rule

If the research problem is primarily about a particular historical website, archived capture, browser/runtime environment, or reconstruction of missing web evidence, develop it in `old-web-archaeology` and cite it here.

`technical-retention` should keep the cross-mechanism analytical question: which retained relations must survive or be reconstituted for a future operation to recover an object as usable/current/meaningful? The bounded OAIS/PREMIS prior-art review in [`docs/PRIOR_ART.md`](docs/PRIOR_ART.md) and [`evidence/prior-art-oais-premis-2002-2024-grounding.md`](evidence/prior-art-oais-premis-2002-2024-grounding.md) supplies the archival-information-model boundary; `old-web-archaeology` supplies concrete historical web cases when needed.

Do not duplicate a capture history here merely to illustrate that old software becomes incompatible.

---

## 5. Future links

Other repositories may become relevant when retention is studied as:

- interface compatibility;
- file-format survivability;
- network state;
- archival practice;
- encoding failure;
- scholarly research protocol.

Old-web preservation is no longer merely a future-link category: `old-web-archaeology` now has an explicit division of labor above.

Add a cross-link only when there is an actual division of labor. Avoid building a decorative graph of every repository.

---

## Boundary summary

```text
computing-archaeology
    historical mechanism + engineering constraint
                │
                ▼
technical-retention
    cross-mechanism comparison + philosophy of retention
                │
       ┌────────┼──────────────────────────┐
       ▼        ▼                          ▼
problem-history mechanical-computing-     old-web-archaeology
anti-anachronism playground               historical captures /
                 reconstruction /         browser-runtime /
                 experiment               reconstruction cases
```