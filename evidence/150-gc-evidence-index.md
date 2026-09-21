# Case 150 evidence index — Crucial M550 managed-SSD garbage collection

## Canonical case

- [`../cases/150-crucial-m550-active-garbage-collection.md`](../cases/150-crucial-m550-active-garbage-collection.md)
- Canonical maturity remains **`grounded`**.

This is a case-local navigation aid, not a replacement for `CASE_INDEX.md`. The repository-level `CASE_INDEX.md` is currently empty even though `ROADMAP.md` still describes it as the authoritative maturity ledger; this index therefore records only the already-established Case 150 status and does not attempt to rebuild the global ledger.

## Evidence chain

### 1. Product / mechanism grounding

- [`150-crucial-2014-2024-active-garbage-collection-grounding.md`](150-crucial-2014-2024-active-garbage-collection-grounding.md)
  - named M550 product feature boundary;
  - Active Garbage Collection and TRIM are separate exposed features;
  - powered-idle controller cleanup plus vendor-neutral live-data-relocation / erase-block-reclaim mechanism;
  - establishes `logical retirement != physical reclamation` and `TRIM knowledge != GC execution`.

### 2. Maintenance opportunity versus power state

- [`150-crucial-powered-idle-sleep-maintenance-opportunity-deepening.md`](150-crucial-powered-idle-sleep-maintenance-opportunity-deepening.md)
  - separates host-visible idle, device/interface sleep, powered maintenance eligibility, and actual GC execution;
  - records the M550's adjacent Device Sleep feature without claiming GC executes in DevSleep/Partial/Slumber.

### 3. Support-page provenance and named-device observation

- [`150-crucial-2013-2015-agc-provenance-experiment-deepening.md`](150-crucial-2013-2015-agc-provenance-experiment-deepening.md)
  - narrows public circulation of Crucial's powered-idle AGC wording;
  - uses the named Crucial m4 experiment as a controlled observability warning;
  - fixes `stale-data recoverability != GC engine absence`.

- [`150-crucial-2013-support-page-version-provenance-deepening.md`](150-crucial-2013-support-page-version-provenance-deepening.md)
  - separates resource/page identity from exact content-version identity;
  - prevents later support wording from being silently backdated to an earlier page-creation timestamp.

### 4. Controller validity / mapping / erase prior art

- [`150-ibm-2009-2012-ssd-gc-validity-map-erase-prior-art-deepening.md`](150-ibm-2009-2012-ssd-gc-validity-map-erase-prior-art-deepening.md)
  - manufacturer-authored controller prior art;
  - separates invalidity evidence, victim selection, live-data recovery/re-storage, map publication, erase eligibility, and actual erase;
  - does not claim IBM's design is the M550 implementation.

### 5. Host-visible retirement semantics reused from Case 04

- [`04-t13-2007-2010-trim-logical-invalidation-read-semantics-deepening.md`](04-t13-2007-2010-trim-logical-invalidation-read-semantics-deepening.md)
  - intentionally reused rather than duplicated;
  - separates host discardability notification, post-TRIM read semantics, later reclamation, and sanitization.

### 6. Reserved capacity / reclamation headroom

- [`150-2009-2012-overprovisioning-reserved-capacity-deepening.md`](150-2009-2012-overprovisioning-reserved-capacity-deepening.md)
  - separates host-visible capacity, controller-reserved maintenance headroom, erased-block readiness, GC completion, and endurance/write-amplification effects;
  - does not project those implementations into M550 firmware.

### 7. Firmware-qualified queued-TRIM trust and maintenance power-loss boundary

- [`150-crucial-m550-2014-2016-ncq-trim-firmware-maintenance-safety-deepening.md`](150-crucial-m550-2014-2016-ncq-trim-firmware-maintenance-safety-deepening.md)
  - Linux's 2014 M550 queued-TRIM blacklist grounds a named-device command-path safety intervention;
  - upstream `ff7f53...` on 27 March 2015 records MU02 as fixing the queued-TRIM issue and narrows the workaround to MU01;
  - Crucial's maintained firmware page independently lists corrected NCQ TRIM error handling while its displayed release-date metadata is contradicted by the 2015 upstream record;
  - a 2016 Micron-domain engineering statement separates protection of already-written / old data during internal activity such as GC from protection of the entire volatile host-write cache;
  - fixes `TRIM advertised != queued-TRIM path trusted`, `firmware fix exists != field fleet converged`, and `maintenance-transaction safety != full in-flight-write durability`.

## Current bounded comparison map

```text
host retires logical data
    ↓
retirement intent exists
    ↓
command path must be admissible for model + firmware
    ↓
retirement/deallocation knowledge reaches controller
    ↓
controller distinguishes live from stale embodiments
    ↓
live data may need relocation
    ↓
internal maintenance must avoid corrupting already-current data
    ↓
old erase block becomes reclaimable
    ↓
physical erase / reusable capacity
```

Keep the following inequalities explicit:

```text
host retirement decision
    != TRIM command
    != safe queued-TRIM transport
    != GC execution
    != physical erase
    != sanitization

host idle
    != controller idle
    != maintenance completion

maintenance power-loss safety
    != full volatile-cache durability

same model family
    != same firmware-qualified command policy
```

## Related cases

- **Case 04** — mapped Flash and T13 TRIM semantics: logical currentness / deallocation before physical erase.
- **Case 15** — SSD power-loss durability handoff: volatile staging, flush, orderly shutdown, capacitor-backed transfer, recovery defects.
- **Case 39** — FTL recovery: payload survival versus mapping/currentness reconstruction.
- **Case 44 / 47** — deallocation and sanitize: ordinary retirement/reclamation must not be confused with sanitization.
- **Case 145** — JFFS2 garbage collection: raw-Flash-filesystem current-node relocation and erase-qualified reuse.
- **Case 153** — Ceph snap-trim: distributed asynchronous reclamation; functional comparison only.

## Related repository routing

`tmzncty/computing-archaeology` remains the home for a broad chronology of:

- ATA Data Set Management / NCQ TRIM development;
- SSD-controller and FTL architecture history;
- Crucial/Micron product and firmware genealogy;
- controller-vendor implementation archaeology;
- performance and deployment history.

A fresh search for `M550 queued TRIM MU02` found no dedicated companion packet to reuse. Case 150 therefore retains only the bounded retention question: **how retirement authority, compatibility state, maintenance execution, and physical reclamation remain separate even inside one named SSD family.**

## Remaining evidence debt

Case 150 remains `grounded`. The highest-value open work is now narrower:

- exact M550 MU01 queued-TRIM failure mechanism and original reproducer traces;
- controlled MU01 vs MU02 hardware tests;
- power-cut fault injection during GC;
- exact GC transaction/progress recovery after interruption;
- exact victim-selection/live-page publication ordering;
- raw-NAND observation of stale embodiments before/after reclaim;
- period-origin Crucial support captures that can authenticate the 2013–2014 wording chain;
- broader managed-SSD GC genealogy in `computing-archaeology` rather than duplicated here.
