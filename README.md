# technical-retention

> **How does a state outlive the moment that produced it?**

`technical-retention` is a research repository about **technical retention**: the material, logical, operational, and philosophical conditions under which a state, trace, inscription, value, or record remains available beyond the moment in which it was produced.

This is **not simply a history of computer memory or storage devices**. Those histories already exist, and much of the engineering history is already covered in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology).

The central question here is different:

> What does it technically mean for something to remain?

A bead on an abacus, a wheel left at an angle, a relay state, a flip-flop, a mercury delay line, a magnetic core, a DRAM cell under refresh, a disk sector, trapped charge in Flash, an SSD logical block, a replicated object, and a distributed consensus state can all be studied as different answers to that question.

The project therefore joins two lines that are usually separated:

1. **exact technical history and engineering reconstruction** — what physical state is retained, by what mechanism, for how long, at what cost, with what maintenance, and through what addressing and recovery machinery;
2. **philosophy and media theory of technics, memory, temporality, inscription, availability, and forgetting** — especially Bernard Stiegler, Martin Heidegger, Wolfgang Ernst, media archaeology, and related work.

The point is not to decorate engineering history with philosophical quotations. Philosophy must survive contact with mechanisms, and technical analogies must not be projected backward as historical actors' own concepts.

---

## The basic distinction

A conventional storage history asks:

```text
What devices existed?
Who invented them?
How much did they store?
How fast were they?
What replaced them?
```

This project asks:

```text
What is the retained state?
        ↓
What physically distinguishes one state from another?
        ↓
What prevents the distinction from disappearing?
        ↓
Does retention require continuous work, refresh, circulation, power, repair, or replication?
        ↓
How is the state addressed and recovered?
        ↓
Who or what decides that two recoveries count as "the same" retained thing?
        ↓
How can the state be changed, erased, corrupted, forgotten, copied, migrated, or made unavailable?
        ↓
What form of temporality does this mechanism impose?
```

A stored thing is therefore not assumed to be a static object. In many systems, apparent persistence is the visible effect of continuous activity.

---

## A first technical intuition

Consider a deliberately heterogeneous chain:

```text
abacus bead position
    → a numerical state persists spatially between operations

mechanical wheel / counter
    → angular or positional configuration retains intermediate state

relay / latch / flip-flop
    → an electrical circuit maintains a discrete logical distinction

delay-line memory
    → retention is recirculation through time

Williams tube / DRAM
    → retention includes periodic restoration or refresh

magnetic core
    → remanent magnetization retains state without continuous power

magnetic disk
    → retention becomes spatial address + magnetic configuration + servo/control machinery

Flash
    → retained charge survives power loss, while programming and erasure alter the medium and introduce wear

SSD
    → a logical block persists only through mapping, garbage collection, ECC, wear management, and replacement of physical cells

replicated / distributed storage
    → a logical fact may persist even though no single physical copy is privileged or permanent
```

This chain is a **research heuristic**, not a claim that all of these mechanisms are historically or philosophically identical.

For example, describing an abacus as `register-like` may be a useful **functional reconstruction**, but it would be anachronistic to claim that historical abacus users possessed the modern computer-architecture concept of a register.

---

## Core dimensions

Every substantial case should try to answer as many of these dimensions as the evidence permits:

| Dimension | Question |
| --- | --- |
| State | What exactly is being retained? |
| Substrate | What physical distinction embodies the state? |
| Retention interval | For how long does it remain recoverable? |
| Volatility | What disappears when power, motion, temperature control, or maintenance stops? |
| Maintenance | What work must continue for the state to appear persistent? |
| Addressability | How can a particular retained state be selected? |
| Access geometry | Sequential, random, associative, indexed, temporal, spatial? |
| Read semantics | Does reading preserve, disturb, or destroy the state? |
| Write semantics | What physical operation creates or changes the state? |
| Erasure | What does it mean to delete or reset it? |
| Failure | How does retention fail? Drift, leakage, wear, noise, media damage, controller loss, bit rot? |
| Redundancy | Is persistence local, duplicated, coded, replicated, or reconstructed? |
| Identity | Why do multiple readings/copies count as the same retained object or value? |
| Latency | What temporal distance separates request from recovery? |
| Energy | What energy is required to retain, refresh, access, move, or rewrite the state? |
| Labor | Which operators, maintainers, manufacturing workers, software, firmware, controllers, or institutions sustain retention? |
| Forgetting | Is forgetting passive decay, explicit erasure, overwrite, loss of index, loss of key, policy, or deliberate destruction? |
| Migration | Can the retained state survive a change of substrate? What must remain invariant? |

These dimensions make it possible to compare technologies without pretending they are the same technology.

---
## Philosophical and media-theoretical spine

### Bernard Stiegler — technics and tertiary retention

Stiegler's work is a central starting point because it treats technical supports as constitutive of memory and temporality rather than as optional containers added after human cognition is complete.

This project will use `tertiary retention` carefully: not as a synonym for every computer memory cell, but as a way to ask how exteriorized traces and technical supports condition what can be remembered, repeated, inherited, and anticipated.

The bounded [`Stiegler tertiary-retention test`](docs/PHILOSOPHICAL_TEST_02_STIEGLER_TERTIARY_RETENTION.md) now sharpens that guardrail: `technical retention` is intentionally broader than `tertiary retention`. A silicon support, Flash mapping layer, or replicated object service may sustain a tertiary-retentional trace, but the fact that an internal machine state persists does not by itself establish the thicker relation of exteriorization, repetition, learning, or transmission that Stiegler's concept addresses.

### Martin Heidegger — technics and availability

Heidegger's analysis of modern technology and `Bestand` / standing-reserve is relevant to the transformation of things into what can be ordered, called upon, and made available for further ordering.

But an explicit methodological rule applies:

> **Bestand is not a synonym for computer storage.**

A disk block, database row, object-store object, or cached page may help us test questions of technical availability and ordering, but the philosophical concept must not be collapsed into an engineering noun merely because the English words look similar.

The bounded [`Heidegger orderability test`](docs/PHILOSOPHICAL_TEST_03_HEIDEGGER_ORDERABILITY.md) keeps that boundary while using designation, resolution, currentness/admissibility, replacement, and recovery to make the engineering conditions of `being on call` precise. Technical availability can discipline a Heideggerian interpretation; it does not define `Bestand`.

### Wolfgang Ernst — media archaeology and technical memory

Ernst is the closest prior art to this project's technical-philosophical interface. His media archaeology insists that "memory" in technical systems must be read at the level of actual mechanisms, timing, registers, buffers, access modes, latency, and operational processes rather than treated only as a metaphor for human or cultural memory.

The first named prior-art test, [`docs/PHILOSOPHICAL_TEST_01_ERNST_OPERATIONALITY.md`](docs/PHILOSOPHICAL_TEST_01_ERNST_OPERATIONALITY.md), retains that operational demand but rejects two universalizations: `retained state = continuous operation` and `technically decisive time = microtime only`. The grounded cases require quiescent, access-triggered, deadline-driven, workload/capacity-triggered, wear-triggered, failure-triggered, and interpretive timescales to remain distinct.

His work is therefore both a major source and a warning: this repository must contribute more than a generic claim that digital media are forms of memory.

### Matthew Kirschenbaum — inscription, storage, and forensic materiality

Kirschenbaum's *Mechanisms* is important for treating digital writing through actual storage mechanisms and for foregrounding erasure, variability, repeatability, and survivability.

The bounded [`Kirschenbaum forensic-materiality test`](docs/PHILOSOPHICAL_TEST_04_KIRSCHENBAUM_FORENSIC_MATERIALITY.md) retains the forensic/formal materiality distinction but refuses to generalize hard-drive remanence into a universal law. Mapped Flash, later SSD sanitization evidence, and RADOS require at least two further distinctions: `forensic witness ≠ authoritative current state`, and `logical-object survivability ≠ current-embodiment survivability ≠ forensic-trace survivability`.

---

## Prior-art boundary

Large parts of the territory already have excellent work. The project should **reuse rather than rediscover** them.

Important starting points include:

- Wolfgang Ernst, *Digital Memory and the Archive* and his work on technical storage and media archaeology;
- Bernard Stiegler, *Technics and Time* and later work on tertiary retention;
- Martin Heidegger, "The Question Concerning Technology";
- Matthew G. Kirschenbaum, *Mechanisms: New Media and the Forensic Imagination*;
- Computer History Museum, [The Storage Engine](https://www.computerhistory.org/storageengine/), a major technical-historical timeline from early inscription to modern storage;
- conventional computer architecture and memory-system literature on registers, cache, SRAM, DRAM, disks, Flash, and storage hierarchy.

See [`docs/PRIOR_ART.md`](docs/PRIOR_ART.md) for the working map.

---

## Relationship to other repositories

This project is intentionally linked to, but not merged with, several existing repositories.

### [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology)

**Engineering and historical evidence source.**

That repository asks why historical computing designs made engineering sense under period constraints. It already has substantial work on delay lines, Williams tubes, drums, magnetic core, tape, disk, HBM, manufacturing, materials, reliability, and related systems.

`technical-retention` should link to or reuse those technical treatments instead of rewriting them unless a retention-specific analysis requires a different argument.

### [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history)

**Methodological guard against anachronism.**

The distinction between historical actors' questions and later reconstruction applies here directly. A modern researcher may describe a historical mechanism as `register-like`, `persistent`, or `addressable`; that does not prove that historical actors formulated the same conceptual problem in those terms.

### [`tmzncty/mechanical-computing-playground`](https://github.com/tmzncty/mechanical-computing-playground)

**Hands-on reconstruction and experiments.**

If a retention claim can be made visible by a mechanical or executable model, implementation may belong there while this repository keeps the conceptual and comparative analysis.

See [`RELATED_REPOS.md`](RELATED_REPOS.md).

---

## Repository map

- [`docs/METHOD.md`](docs/METHOD.md) — evidence layers, anti-anachronism rules, and comparison method.
- [`docs/PRIOR_ART.md`](docs/PRIOR_ART.md) — what has already been done and where this project can still contribute.
- [`docs/TECHNICAL_SPINE.md`](docs/TECHNICAL_SPINE.md) — provisional mechanism lineage from retained position to distributed logical state.
- [`docs/PHILOSOPHICAL_SPINE.md`](docs/PHILOSOPHICAL_SPINE.md) — Stiegler, Heidegger, Ernst, Kirschenbaum, and conceptual questions.
- [`cases/06-flip-flop-powered-working-retention.md`](cases/06-flip-flop-powered-working-retention.md) — grounded post-synthesis technical stress test: powered bistable working state from Eccles–Jordan to ENIAC, with a bounded Whirlwind period witness separating flip-flop implementation from register-level organization.
- [`cases/07-static-mos-ram-powered-quiescence.md`](cases/07-static-mos-ram-powered-quiescence.md) — grounded semiconductor-array stress test: period static-MOS / flip-flop / bistable vocabulary, no-refresh powered quiescence, decoded-array semantics, nondestructive read in bounded Intel devices, 5101L retention-supporting supply versus active operation, and an Intel manufacturer-primary feedback-coupled static cell with separate decode/sense/address paths.
- [`cases/08-system360-model85-cache-currentness.md`](cases/08-system360-model85-cache-currentness.md) — grounded architectural bridge: IBM System/360 Model 85 cache as a transparent derivative fast copy whose usability depends on retained sector correspondence, per-block validity/currentness, store-triggered updates, and replacement-policy state.
- [`cases/09-dram-cbr-refresh-address-internalization.md`](cases/09-dram-cbr-refresh-address-internalization.md) — grounded DRAM refresh-responsibility bridge: CBR mode moves refresh-row enumeration on-chip while keeping refresh cadence externally triggered in the bounded TI design.
- [`cases/10-toshiba-leakage-tracked-self-refresh.md`](cases/10-toshiba-leakage-tracked-self-refresh.md) — grounded autonomous-refresh bridge: an on-chip leak monitor, threshold trigger, oscillator, and refresh counter internalize maintenance scheduling in the bounded Toshiba design.
- [`cases/11-intel-frohman-floating-gate-eprom-erasure.md`](cases/11-intel-frohman-floating-gate-eprom-erasure.md) — grounded floating-gate EPROM bridge: trapped-charge nonvolatility, avalanche programming, nondestructive lower-stress read, and a radiation erase path that separates ordinary addressability from erase geometry.
- [`cases/12-intel-2816-eeprom-electrical-erasure.md`](cases/12-intel-2816-eeprom-electrical-erasure.md) — grounded EEPROM bridge: the Intel 2816 moves deliberate erase into electrical/in-system control, exposes both byte and whole-chip erase, keeps erase/write in a distinct high-voltage/timed regime, and makes finite cycling part of the retention/forgetting comparison.
- [`cases/13-early-flash-coarse-erase-asymmetric-rewrite.md`](cases/13-early-flash-coarse-erase-asymmetric-rewrite.md) — grounded early-Flash bridge: one-transistor density pressure and shared/whole-array electrical erase coexist with finer addressed program/read, exposing erase geometry as a distinct retention relation before later mapping/FTL semantics.
- [`cases/14-scsi-disk-defect-reassignment-logical-identity.md`](cases/14-scsi-disk-defect-reassignment-logical-identity.md) — grounded HDD/SCSI defect-reassignment bridge: host-visible LBA can remain stable while a grown-defect repair changes the serving physical sector; reassignment, payload recovery, defect metadata, and finite spare capacity remain separate retention relations.
- [`cases/15-intel-ssd320-power-loss-durability.md`](cases/15-intel-ssd320-power-loss-durability.md) — grounded SSD/controller bridge: volatile write-cache/temporary-buffer state exists in front of nonvolatile NAND; explicit flush, orderly shutdown, and capacitor-backed power-failure emergency transfer are separate durability paths.
- [`cases/16-bsd-ffs-soft-updates-crash-admissibility.md`](cases/16-bsd-ffs-soft-updates-crash-admissibility.md) — grounded filesystem crash-consistency bridge: production 4.4BSD FFS soft updates lets application-visible metadata run ahead of a dependency-safe disk image, separates immediate crash admissibility from latest-operation durability, and gives `fsync` a wider payload-plus-metadata persistence closure.
- [`cases/17-raid-parity-reconstruction-degraded-repair.md`](cases/17-raid-parity-reconstruction-degraded-repair.md) — grounded encoded-redundancy bridge: parity/checksum can reconstruct a missing member contribution without a full duplicate; validity/currentness meta state, reconstruction progress, spare capacity, and background rebuild separate degraded service from restored redundancy margin.
- [`cases/18-zfs-scrub-latent-error-detection.md`](cases/18-zfs-scrub-latent-error-detection.md) — grounded proactive-integrity bridge: explicit whole-pool scrubbing moves verification before ordinary demand, checksum-qualified redundant copies permit conditional self-healing, and scrub remains distinct from replacement-triggered resilvering.
- [`cases/19-facebook-f4-erasure-coded-failure-domains.md`](cases/19-facebook-f4-erasure-coded-failure-domains.md) — grounded distributed-erasure-coding bridge: f4 separates Reed–Solomon fragment algebra from rack/datacenter failure-domain placement, normal direct reads from online requested-BLOB reconstruction, content repair from placement rebalancing, and local RS recovery from geo-XOR composition.
- [`cases/20-nvme10-fua-flush-persistence-ordering.md`](cases/20-nvme10-fua-flush-persistence-ordering.md) — grounded NVMe 1.0 interface bridge: volatile-write-cache classification, Flush, per-write FUA, host-enforced ordering, and separate normal/power-fail atomic-write units keep command completion, media commitment, ordering, and failure atomicity distinct.
- [`cases/21-micron-sdram-refresh-mode-handoff.md`](cases/21-micron-sdram-refresh-mode-handoff.md) — grounded SDRAM interface bridge: normal `AUTO REFRESH` uses externally repeated nonpersistent commands with internal refresh-row addressing, while CKE-controlled `SELF REFRESH` moves recurring clocking/refresh work inside the device until an explicit `tXSR` exit returns responsibility to the external cadence.
- [`cases/22-ibm-system370-paging-backing-copy-currentness.md`](cases/22-ibm-system370-paging-backing-copy-currentness.md) — grounded virtual-memory bridge: a virtual page can outlive one real page frame; page replacement requires page-out only when the selected real copy has changed relative to an extant external copy, while RSM/ASM retain the translation and auxiliary-location relations needed for later page-in.
- [`cases/23-amazon-dynamo-divergent-version-anti-entropy.md`](cases/23-amazon-dynamo-divergent-version-anti-entropy.md) — grounded distributed-currentness bridge: Dynamo can deliberately retain several causally unrelated versions of one key, use vector-clock ancestry to authorize forgetting, separate sloppy-quorum availability from intended-placement convergence through hinted handoff, and repair replica divergence through read repair plus Merkle-tree anti-entropy.
- [`cases/24-windows-azure-lrc-repair-locality-handoff.md`](cases/24-windows-azure-lrc-repair-locality-handoff.md) — grounded repair-locality bridge: Windows Azure Storage LRC separates coded recoverability from reconstruction read cost, on-demand reconstruction from durable repair, and code locality from fault/upgrade-domain placement; its asynchronous validated transition from three full replicas to coded fragments makes completion metadata part of the retention handoff.
- [`cases/25-openstack-swift-ec-overwrite-durable-currentness.md`](cases/25-openstack-swift-ec-overwrite-durable-currentness.md) — grounded mutable erasure-coded currentness bridge: Swift separates fragment presence from committed object retention, requires same-timestamp distinct-index fragment cohorts plus durability evidence for GET, and gates old-version retirement on the newer coded version crossing its commit boundary.
- [`cases/26-google-gfs-inactive-chunk-integrity.md`](cases/26-google-gfs-inactive-chunk-integrity.md) — grounded distributed-integrity bridge: GFS separates chunk-version currentness from per-replica checksum validity, verifies before read return, scans inactive chunks during idle periods, and restores a trustworthy replica count by cloning from another valid copy.
- [`cases/27-ceph-luminous-ec-deep-scrub-checksum-authority.md`](cases/27-ceph-luminous-ec-deep-scrub-checksum-authority.md) — grounded coded-integrity bridge: Luminous ties mutable erasure-coded overwrites to BlueStore checksumming and deep scrub, while the 12.2.6–12.2.8 digest regression shows that integrity metadata itself can become inconsistent, be distrusted, and require a verification/repair pass before ordinary trust is restored.
- [`cases/28-openstack-swift-tombstone-consistency-window.md`](cases/28-openstack-swift-tombstone-consistency-window.md) — grounded distributed-deletion bridge: Swift retains a timestamped `.ts` tombstone as the newest negative object state so deletion can propagate across divergent replicas; payload retirement, deletion convergence, and later tombstone reclamation remain separate retention events.
- [`cases/29-ceph-luminous-ec-scrub-authoritative-repair.md`](cases/29-ceph-luminous-ec-scrub-authoritative-repair.md) — grounded scrub-repair-authority bridge: Luminous `v12.2.8` source separates scrub evidence, operational authoritative-candidate selection, missing-state injection, EC source filtering, `minimum_to_decode` sufficiency, and completed reconstruction; an auth candidate is explicitly not elevated to certainty of correct data.
- [`cases/30-nvme14-pmr-persistence-barriers.md`](cases/30-nvme14-pmr-persistence-barriers.md) — grounded NVMe 1.4 persistent-memory-region bridge: the optional PCIe PMR separates Posted-write completion from persistence barriers, interface persistence from implementation-specific nonvolatile staging, readiness from restored-content continuity, and request completion from valid read/write semantics.
- [`cases/31-snia-nvm-persistence-domain-boundary.md`](cases/31-snia-nvm-persistence-domain-boundary.md) — grounded terminology/programming-model bridge: SNIA's 2013 NVM model defines `durable` through a `persistence domain`, separates store execution and cache/buffer residency from domain arrival, conditions recovery on tolerated failure patterns, and keeps synchronization distinct from atomicity/order; the exact term is not silently reassigned to NVMe PMR.
- [`cases/32-intel-adr-eadr-power-fail-domain.md`](cases/32-intel-adr-eadr-power-fail-domain.md) — grounded platform-persistence bridge: Intel's 2016 ADR model places memory-controller write-pending queues inside a power-fail-protected domain while processor caches remain outside; the 2020–2021 eADR platform description extends protection upstream to processor caches, changes ordinary cache-flush obligations, retains `SFENCE`, and makes OEM stored energy part of the power-fail durability path.
- [`cases/33-micron-ddr5-same-bank-refresh-localization.md`](cases/33-micron-ddr5-same-bank-refresh-localization.md) — grounded DDR5 refresh-localization bridge: Micron `Same Bank Refresh` / `REFsb` targets a bank in each bank group, keeping other banks/groups available and separating the continuing refresh obligation from the spatial scope of maintenance-induced service blocking.
- [`cases/34-micron-temperature-dependent-dram-refresh.md`](cases/34-micron-temperature-dependent-dram-refresh.md) — grounded temperature-conditioned DRAM refresh bridge: Micron’s 1991-filed circuit maps a nearby temperature sensor through discrete comparator bands into oscillator/refresh cadence, separating the continuing refresh obligation from a worst-case fixed maintenance frequency and preserving earlier 1987-priority temperature-adaptive prior art.
- [`cases/35-micron-mobile-ddr-automatic-tcsr.md`](cases/35-micron-mobile-ddr-automatic-tcsr.md) — grounded commercial Mobile DDR TCSR bridge: Micron’s Rev. J 2/08 product contract combines internally clocked self refresh with automatic on-die temperature control of the self-refresh oscillator, keeps PASR retention coverage separately controller-programmable, and distinguishes DPD array-payload loss from surviving mode-register state.
- [`cases/36-nand-flash-correct-and-refresh-maintenance.md`](cases/36-nand-flash-correct-and-refresh-maintenance.md) — grounded NAND-Flash retention-maintenance bridge: Cai et al.’s 2012 FCR proposal periodically reads and ECC-corrects aging MLC NAND, then reprograms in place or remaps to a new block before retention errors outrun correction margin; adaptive cadence, wear metadata, and refresh-induced wear keep nonvolatility distinct from maintenance-free reliable retention.
- [`evidence/06-burks-1947-eniac-flip-flop-grounding.md`](evidence/06-burks-1947-eniac-flip-flop-grounding.md) — Case-06 promotion record: Burks 1947 pp. 757–759 directly supply period remembering-circuit vocabulary, a published simplified ENIAC schematic, two-stable-state/DC-cross-coupling mechanism, trigger/recovery separation, and microsecond timing margins; exact PX-1-105 remains archival cleanup for drawing-specific claims.
- [`evidence/06-flip-flop-register-boundary-addendum.md`](evidence/06-flip-flop-register-boundary-addendum.md) — Case-06 source-deepening ledger: Whirlwind R-221 closes the period `register` vocabulary gap; exact 1919 Eccles–Jordan and ENIAC drawing locators are recorded without pretending locator evidence is direct page/schematic inspection.
- [`evidence/07-intel-pashley-1975-static-ram-grounding.md`](evidence/07-intel-pashley-1975-static-ram-grounding.md) — Case-07 promotion record: Intel/Pashley US3946369A directly grounds a manufacturer-primary `1024 × 1`, `32 × 32`, +5 V static-RAM design with an explicitly bistable feedback-coupled cell and distinct decoder, sensing, read/write, and address-transition layers; it is not silently identified as a specific commercial product.
- [`evidence/08-model85-cache-1967-1968-grounding.md`](evidence/08-model85-cache-1967-1968-grounding.md) — Case-08 grounding record: directly inspected Liptay 1968 pages plus IBM's 1967 functional manual separate cache payload, sector correspondence, block validity, currentness updating, and activity-list replacement state while preserving period vocabulary.
- [`evidence/09-ti-cbr-refresh-address-grounding.md`](evidence/09-ti-cbr-refresh-address-grounding.md) — Case-09 grounding record: separates the refresh obligation from externally supplied cadence, on-chip row enumeration, row restoration, and hidden-refresh interface visibility.
- [`evidence/10-toshiba-1984-self-refresh-scheduling-grounding.md`](evidence/10-toshiba-1984-self-refresh-scheduling-grounding.md) — Case-10 grounding record: documents a manufacturer-primary on-chip leak-current monitor, threshold-derived trigger, oscillator, and refresh-address counter without assigning the patent to an unsupported named product.
- [`evidence/11-intel-1970-1971-floating-gate-eprom-grounding.md`](evidence/11-intel-1970-1971-floating-gate-eprom-grounding.md) — Case-11 grounding record: Intel/Frohman primary patents plus Kahng prior art separate long-term trapped-charge retention, programming, nondestructive reading, radiation discharge, and invention-priority boundaries.
- [`evidence/12-intel-1978-1981-eeprom-electrical-erasure-grounding.md`](evidence/12-intel-1978-1981-eeprom-electrical-erasure-grounding.md) — Case-12 grounding record: directly inspected Intel 2816 product pages plus an Intel tunneling patent separate quiescent floating-gate retention from electrical byte/chip erasure, erase-before-write sequencing, exceptional high-voltage/timed service, and finite cycling.
- [`evidence/13-early-flash-coarse-erase-1980-1988-grounding.md`](evidence/13-early-flash-coarse-erase-1980-1988-grounding.md) — Case-13 grounding record: Toshiba and Intel manufacturer-primary patents plus period-paper abstract evidence separate one-transistor density goals, shared/whole-array erase, fine program/read selection, command control, and verification while preserving facsimile/product-identity boundaries.
- [`evidence/14-disk-lba-defect-reassignment-1990-1997-grounding.md`](evidence/14-disk-lba-defect-reassignment-1990-1997-grounding.md) — Case-14 grounding record: NeXT/Chan and Seagate primary sources separate logical-block designation, physical-sector replacement, payload recovery, defect metadata, physical geometry, and finite spare exhaustion without importing FTL terminology.
- [`evidence/15-intel-ssd320-power-loss-durability-grounding.md`](evidence/15-intel-ssd320-power-loss-durability-grounding.md) — Case-15 grounding record: period ATA standards-development text, Intel SSD 320 product/design evidence, and a bounded FAST ’13 counterexample layer separate volatile staging, flush-to-media completion, shutdown/emergency handoff, stored-energy infrastructure, and empirical fault compliance.
- [`evidence/16-bsd-ffs-soft-updates-1999-2000-grounding.md`](evidence/16-bsd-ffs-soft-updates-1999-2000-grounding.md) — Case-16 grounding record: McKusick/Ganger 1999 and Ganger et al. 2000 separate volatile dependency bookkeeping, dependency-safe stable writeback, immediate crash mountability, bounded residual leaks, and `fsync` durability closure without turning the mechanism into a journal.
- [`evidence/17-raid-parity-reconstruction-1977-1994-grounding.md`](evidence/17-raid-parity-reconstruction-1977-1994-grounding.md) — Case-17 grounding record: Ouchi’s 1977-filed IBM XOR/check-sum recovery patent plus Berkeley RAID sources separate encoded reconstructability, validity/parity currentness meta state, request-time reconstruction, spare capacity, background rebuild, and historical naming/priority boundaries.
- [`evidence/18-zfs-scrub-2004-2010-grounding.md`](evidence/18-zfs-scrub-2004-2010-grounding.md) — Case-18 grounding record: official Solaris ZFS documentation plus 2004 disk-scrubbing prior art and independent latent-sector-error evidence separate physical presence, verified integrity, defect discovery, conditional repair, proactive scan work, and resilver/rebuild semantics.
- [`evidence/19-facebook-f4-2014-erasure-coding-grounding.md`](evidence/19-facebook-f4-2014-erasure-coding-grounding.md) — Case-19 grounding record: directly inspected Facebook/USENIX production evidence separates encoded-fragment sufficiency, failure-domain placement, sub-BLOB online reconstruction, background full-block rebuild, placement convergence, geo-XOR composition, and erasure-code invention priority.
- [`evidence/20-nvme10-2011-flush-fua-grounding.md`](evidence/20-nvme10-2011-flush-fua-grounding.md) — Case-20 grounding record: directly inspected official NVMe 1.0 pages separate VWC classification, volatile→nonvolatile Flush, per-write FUA media commitment, host-enforced ordering, and normal-versus-power-fail atomicity without projecting later `persistence domain` vocabulary backward.
- [`evidence/21-micron-1999-sdram-refresh-mode-grounding.md`](evidence/21-micron-1999-sdram-refresh-mode-grounding.md) — Case-21 grounding record: Micron's Rev. 11/99 product-family documentation separates nonpersistent externally repeated `AUTO REFRESH`, internal row enumeration, CKE-controlled `SELF REFRESH` internal clocking, explicit `tXSR` exit, and the return to external refresh cadence without turning one vendor artifact into a full JEDEC history.
- [`evidence/22-ibm-1972-1976-paging-currentness-grounding.md`](evidence/22-ibm-1972-1976-paging-currentness-grounding.md) — Case-22 grounding record: period IBM OS/VS2 documents separate virtual-page identity, real-frame residency, external-page-storage location, change/reference state, conditional page-out, page-fault recovery, and RSM/ASM auxiliary-location bookkeeping; Atlas 1962 controls invention-priority claims.
- [`evidence/23-amazon-dynamo-2007-version-handoff-antientropy-grounding.md`](evidence/23-amazon-dynamo-2007-version-handoff-antientropy-grounding.md) — Case-23 grounding record: directly inspected 2007 Dynamo pages separate causal supersession from concurrent-version retention, sloppy-quorum success from hinted-placement convergence, Merkle-tree divergence detection from synchronization, read repair from background anti-entropy, and production foreground service from resource-budgeted repair work while preserving earlier epidemic/Bayou prior-art boundaries.
- [`evidence/24-windows-azure-2012-lrc-grounding.md`](evidence/24-windows-azure-2012-lrc-grounding.md) — Case-24 grounding record: directly inspected Microsoft/USENIX 2012 production evidence separates LRC read-set locality, fault/upgrade-domain placement, asynchronous coding progress/completion metadata, validation-gated replica deletion, foreground reconstruction reads, and durable fragment regeneration while preserving Reed–Solomon/Pyramid-code prior-art boundaries.
- [`evidence/25-openstack-swift-2015-2016-ec-currentness-grounding.md`](evidence/25-openstack-swift-2015-2016-ec-currentness-grounding.md) — Case-25 grounding record: exact Swift 2.3.0/2.10.1 source states separate fragment landing, timestamp/index cohort selection, `.durable` commit evidence, safe old-timestamp retirement, later reconstruction/marker propagation, fragment validity, and release-specific quorum semantics.
- [`evidence/26-gfs-2003-integrity-scan-grounding.md`](evidence/26-gfs-2003-integrity-scan-grounding.md) — Case-26 grounding record: the 2003 GFS primary paper separates version staleness, local checksum integrity, demand-time verification, idle inactive-chunk verification, alternate-replica service, cloning repair, and restored replication margin without projecting later `scrub` vocabulary backward.
- [`evidence/27-ceph-luminous-2017-2018-ec-scrub-grounding.md`](evidence/27-ceph-luminous-2017-2018-ec-scrub-grounding.md) — Case-27 grounding record: tag-matched Luminous source documentation and official 2018 correction records separate EC algebra, BlueStore checksum state, scrub coverage, checksum-metadata authority, diagnostic mismatch, and restored integrity confidence without inventing an exact per-shard repair algorithm.
- [`evidence/28-openstack-swift-2016-tombstone-consistency-grounding.md`](evidence/28-openstack-swift-2016-tombstone-consistency-grounding.md) — Case-28 grounding record: Swift 2.10.1 release metadata, replication documentation, on-disk implementation, configuration, and unit tests separate timestamped negative currentness, asynchronous delete propagation, the consistency window, and age-gated tombstone reclamation without equating DELETE with secure erasure.
- [`evidence/29-ceph-luminous-2018-scrub-repair-grounding.md`](evidence/29-ceph-luminous-2018-scrub-repair-grounding.md) — Case-29 grounding record: tag-matched `v12.2.8` `PGBackend.cc`, `PG.cc`, and `ECBackend.cc` establish the source-level handoff from scrub-map error qualification to authoritative candidates, missing/location state, codec-level source filtering, `minimum_to_decode`, and EC reconstruction while preserving the implementation's explicit uncertainty boundary.
- [`evidence/30-nvme14-2019-pmr-grounding.md`](evidence/30-nvme14-2019-pmr-grounding.md) — Case-30 grounding record: the ratified 10 June 2019 NVMe 1.4 specification and NVM Express change record ground PMR introduction, cross-reset/disable persistence, implementation-specific nonvolatile staging, elasticity buffering, read-based persistence barriers, restore/health status, and not-ready completion semantics.
- [`evidence/31-snia-2013-persistence-domain-grounding.md`](evidence/31-snia-2013-persistence-domain-grounding.md) — Case-31 grounding record: official SNIA Version 1 text anchors the 2013 `persistence domain`, multiple-domain/configuration semantics, PM sync/flush closure, failure-qualified recoverability, and atomicity/order limits; official ratified NVMe 1.4 and 2.0 provide a bounded negative terminology check without claiming universal absence or first use.
- [`evidence/32-intel-2016-2021-adr-eadr-grounding.md`](evidence/32-intel-2016-2021-adr-eadr-grounding.md) — Case-32 grounding record: dated Intel first-party sources from 2016–2021 separate processor-cache residency, ADR-protected memory-controller WPQs, optional eADR cache inclusion, PMDK feature-sensitive flush behavior, retained `SFENCE`, and OEM stored-energy requirements without generalizing the sourced power-fail contract into universal crash persistence.
- [`evidence/33-micron-2020-2023-ddr5-same-bank-refresh-grounding.md`](evidence/33-micron-2020-2023-ddr5-same-bank-refresh-grounding.md) — Case-33 grounding record: public Micron DDR5 manufacturer material anchors `Same Bank Refresh` / `REFsb`, one-bank-per-bank-group targeting, and non-target-bank availability while preserving the boundary against a complete JEDEC timing/genealogy claim.
- [`evidence/34-micron-1991-temperature-dependent-refresh-grounding.md`](evidence/34-micron-1991-temperature-dependent-refresh-grounding.md) — Case-34 grounding record: Micron US5278796A anchors sensor → band classification → oscillator → refresh cadence, CardioData’s 1987-priority family blocks a Micron-first claim, and a later self-refresh patent preserves the cadence-versus-authority boundary.
- [`evidence/35-micron-2005-2008-mobile-ddr-tcsr-grounding.md`](evidence/35-micron-2005-2008-mobile-ddr-tcsr-grounding.md) — Case-35 grounding record: Micron’s Rev. J 2/08 Mobile DDR product datasheet directly anchors automatic on-die temperature control of the self-refresh oscillator, inert TCSR programming bits on this version, controller-selectable PASR coverage, internally clocked self refresh, and the DPD split between lost array payload and retained mode-register values.
- [`evidence/36-cai-2012-flash-correct-refresh-grounding.md`](evidence/36-cai-2012-flash-correct-refresh-grounding.md) — Case-36 grounding record: the directly inspected ICCD 2012 paper anchors FCR terminology, ECC-bounded retention-error renewal, remap versus in-place/hybrid repair, adaptive P/E-cycle-based cadence, background/power costs, and the simulation-versus-deployment evidence boundary.
- [`docs/SYNTHESIS_AUDIT_01_MAINTAINED_PERSISTENCE.md`](docs/SYNTHESIS_AUDIT_01_MAINTAINED_PERSISTENCE.md) — first evidence-led audit of a provisional thesis, including counterexamples to a universal active-maintenance model.
- [`docs/SYNTHESIS_AUDIT_02_TEMPORAL_TRANSPORT.md`](docs/SYNTHESIS_AUDIT_02_TEMPORAL_TRANSPORT.md) — audit of the storage/transfer proposition against grounded cases, retaining only a controlled recoverability-relation model across time.
- [`docs/SYNTHESIS_AUDIT_03_ADDRESSABILITY.md`](docs/SYNTHESIS_AUDIT_03_ADDRESSABILITY.md) — audit separating retention from designation, selection/resolution, currentness/admissibility, and recovery across grounded cases.
- [`docs/SYNTHESIS_AUDIT_04_PRIVILEGED_LOCATION.md`](docs/SYNTHESIS_AUDIT_04_PRIVILEGED_LOCATION.md) — audit distinguishing physical-token replacement, stable physical home, metadata-mediated relocation, replaceable replicas, and temporary protocol authority.
- [`docs/SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md`](docs/SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md) — audit separating physical destruction, missed maintenance, logical invalidation, relation/currentness loss, recoverability loss, and masking by redundancy.
- [`docs/SYNTHESIS_AUDIT_06_MAINTENANCE_VISIBILITY.md`](docs/SYNTHESIS_AUDIT_06_MAINTENANCE_VISIBILITY.md) — audit rejecting a monotonic `more reliable -> more hidden maintenance` law while separating reliability, automation, interface invisibility, labor, and infrastructure.
- [`docs/SYNTHESIS_COUNTEREXAMPLE_LEDGER.md`](docs/SYNTHESIS_COUNTEREXAMPLE_LEDGER.md) — cross-audit control ledger recording rejected strong claims, required decompositions, scoped survivors, and thesis status before any conclusion is promoted.
- [`docs/PHILOSOPHICAL_TEST_01_ERNST_OPERATIONALITY.md`](docs/PHILOSOPHICAL_TEST_01_ERNST_OPERATIONALITY.md) — first named prior-art test; preserves operational analysis while rejecting a universal continuous-operation or microtime ontology of retention.
- [`docs/PHILOSOPHICAL_TEST_02_STIEGLER_TERTIARY_RETENTION.md`](docs/PHILOSOPHICAL_TEST_02_STIEGLER_TERTIARY_RETENTION.md) — source-controlled boundary test separating broad mechanism-level technical retention from Stiegler's thicker relation of technical exteriorization and retentional efficacy.
- [`docs/PHILOSOPHICAL_TEST_03_HEIDEGGER_ORDERABILITY.md`](docs/PHILOSOPHICAL_TEST_03_HEIDEGGER_ORDERABILITY.md) — boundary test separating storage/retrieval from Heideggerian `Bestand` while making the engineering conditions of callability explicit.
- [`docs/PHILOSOPHICAL_TEST_04_KIRSCHENBAUM_FORENSIC_MATERIALITY.md`](docs/PHILOSOPHICAL_TEST_04_KIRSCHENBAUM_FORENSIC_MATERIALITY.md) — test of forensic/formal materiality across mapped Flash, later SSD sanitization evidence, and distributed replicas/currentness.
- [`ROADMAP.md`](ROADMAP.md) — staged research program.
- [`RELATED_REPOS.md`](RELATED_REPOS.md) — cross-repository boundaries and reuse rules.
- [`AGENTS.md`](AGENTS.md) — research protocol for human and AI contributors.

The current post-audit technical bridge set now extends through Case 25. Cases 09–10 show that a DRAM retention deadline can remain while row enumeration, trigger cadence, and scheduling responsibility move across the package boundary. Case 21 adds a named late-1990s SDRAM interface in which that responsibility becomes mode-dependent and reversible: **internal refresh addressing ≠ autonomous recurrence**, **retention availability ≠ ordinary service availability**, and **SELF REFRESH entry/exit can transfer recurring refresh work into the device and then return it to externally issued AUTO REFRESH commands**. Cases 11–13 establish the bounded EPROM→EEPROM→early-Flash erase-control bridge and keep device-level erase asymmetry separate from later FTL semantics. Case 14 adds a distinct magnetic-disk indirection regime: **logical-block identity ≠ physical-sector identity**, **reassignment continuity ≠ payload continuity**, and **LBA abstraction ≠ disappearance of physical geometry**. Unlike Case 04's erase-driven routine relocation/reclamation, the bounded HDD path is defect/failure-triggered spare substitution, so the comparison remains functional rather than genealogical. Case 15 then adds a controller-mediated durability boundary above the nonvolatile medium: **nonvolatile NAND ≠ every current state already durable**, **stored energy ≠ stored payload**, and **explicit flush ≠ orderly shutdown ≠ unexpected-power-loss emergency handoff**. Case 16 moves one layer upward again: **application-visible current filesystem state ≠ crash-admissible stable state**, **safe post-crash mountability ≠ newest-operation permanence**, and **`fsync` durability ≠ payload-block completion**. Case 17 adds encoded redundancy: **parity redundancy ≠ replica multiplicity**, **single-failure service continuity ≠ restored redundancy margin**, and **redundant bytes physically present ≠ usable current redundancy**. Case 18 adds proactive integrity verification before demand: **physical presence/readability ≠ verified integrity**, **redundancy availability ≠ defect discovery**, **detection work ≠ repair work**, and **scrub ≠ rebuild/resilver**. Case 19 extends coded retention across distributed failure domains: **erasure-code algebra ≠ failure-domain independence**, **requested-object read availability ≠ completed block repair**, **content reconstruction ≠ restored placement geometry**, and **local reconstruction can compose beneath geo-level recovery**. Case 20 then separates the host/controller persistence contract itself: **command completion ≠ nonvolatile-media commitment unless the applicable contract establishes it**, **per-write FUA persistence ≠ cross-command ordering**, **Flush ≠ FUA**, **interface volatility class ≠ simple physical-substrate class**, and **normal atomicity ≠ power-fail atomicity**. Case 22 adds a capacity/residency-triggered hierarchy relation: **virtual-page identity ≠ page-frame identity ≠ backing-slot identity**, **residency ≠ currentness**, **frame reassignment ≠ forgetting**, and **page replacement ≠ unconditional page-out**; the current copy can move from real storage to external page storage only when required by the documented change relation, while nonresidency can remain recoverable through page fault/page-in without becoming archival durability. Case 23 adds a different distributed-currentness counterexample: **replica multiplicity ≠ one already-selected current value**, **causal ancestry can authorize forgetting while causal incomparability can require continued retention**, **write availability ≠ intended-placement convergence**, and **replica-divergence detection ≠ synchronization completion**. Dynamo therefore complements Case 05 rather than replacing it: bounded RADOS peering and Dynamo's application-visible divergent-version reconciliation are distinct historical currentness regimes. Case 24 adds a repair-cost and representation-transition counterexample inside distributed coding: **coded recoverability ≠ reconstruction cost**, **local reconstruction ≠ physical co-location**, **on-demand reconstruction ≠ durable fragment repair**, and **coded-fragment presence ≠ completed redundancy-regime handoff**. WAS keeps full replicas through asynchronous coding and validation, persists coding progress for resumption, and schedules source-replica deletion only after completion metadata marks the new coded representation. Case 25 then supplies the mutable coded-version counterexample left open by Cases 19 and 24: **fragment presence ≠ committed object retention**, **coded recoverability ≠ version admissibility**, **newer timestamp ≠ safe-forgetting authority**, and **client success ≠ completed repair convergence**. Swift selects a same-timestamp, distinct-index fragment cohort with a durability witness and keeps the older timestamp until the replacement crosses its documented commit boundary. See [`CASE_INDEX.md`](CASE_INDEX.md) for authoritative maturity status and [`ROADMAP.md`](ROADMAP.md) for the next slice.

---

## Current research theses — provisional, not conclusions

The project begins with several hypotheses to test rather than assume:

1. **Persistence is often an achieved relation, not a maintenance-free property.** Some retained states remain quiescently; others require scheduled reconstruction, access-triggered restore, remapping, or repair. The first question is which layer is being kept persistent and what event creates its maintenance obligation. See the bounded [maintenance audit](docs/SYNTHESIS_AUDIT_01_MAINTAINED_PERSISTENCE.md).
2. **Storage can be analyzed as transfer across temporal distance, but only as a recoverability model.** A state established at `t0` may remain or be reconstructed as an agreed recoverable equivalent at `t1`; this does not imply literal physical motion, one unchanging carrier, or active maintenance, and it does not replace mechanism-level distinctions. See the bounded [temporal-transport audit](docs/SYNTHESIS_AUDIT_02_TEMPORAL_TRANSPORT.md).
3. **Addressability is a separate operational relation layered onto retention.** A state may persist without being autonomously or cheaply selectable, while a stable logical designation can survive changes in physical embodiment. Analyze designation and selection/resolution separately from currentness/admissibility and read/recovery; do not equate address with physical location or addressability with availability. See the bounded [addressability audit](docs/SYNTHESIS_AUDIT_03_ADDRESSABILITY.md).
4. **Technical forgetting is layer- and mechanism-specific.** A retained state can cease to remain usable through physical destruction, missed restoration/refresh, logical invalidation, loss of mapping/interpretive/currentness relations, or failed reconstruction. These events are not equivalent to one another or to temporary unavailability, and lower-layer loss can be masked by relocation, reconstruction, or redundancy. See the bounded [technical-forgetting audit](docs/SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md).
5. **Logical persistence can become detached from any one permanent physical home without becoming placeless.** Some systems keep a stable location while repeatedly reconstructing physical state; mapped and distributed systems go further by letting identity survive relocation or replica replacement through retained mapping, placement, version, and authority relations. Treat this as a mechanism comparison, not a one-way historical law. See the bounded [privileged-location audit](docs/SYNTHESIS_AUDIT_04_PRIVILEGED_LOCATION.md).
6. **Reliable retention can depend on maintenance displaced below or beyond the user's interface, but reliability, automation, invisibility, labor, and infrastructure are separate variables.** Ask what failure is being survived, who no longer has to perform or observe the maintenance, which layer now performs it, and which human/material dependencies remain. Do not turn this into a historical law that `more reliable` means `more hidden work`. See the bounded [maintenance-visibility audit](docs/SYNTHESIS_AUDIT_06_MAINTENANCE_VISIBILITY.md).

Each thesis must remain vulnerable to counterexamples. The current cross-audit status and negative results are tracked in [`docs/SYNTHESIS_COUNTEREXAMPLE_LEDGER.md`](docs/SYNTHESIS_COUNTEREXAMPLE_LEDGER.md).

---

## One rule above all

> **Do not confuse an analogy that helps us think with a historical fact that must be proven.**
