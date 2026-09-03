# Case 32 grounding — Intel ADR/eADR power-fail protected domains (2016–2021)

## Purpose

This record grounds [`../cases/32-intel-adr-eadr-power-fail-domain.md`](../cases/32-intel-adr-eadr-power-fail-domain.md).

The bounded research question is:

> **How did Intel document the persistence boundary around processor caches, memory-controller write-pending queues, and persistent-memory DIMMs under ADR and eADR, and what software/energy obligations remained as that boundary moved upstream?**

The case is intentionally narrower than a history of persistent memory. It exists to turn Case 31's abstract SNIA `persistence domain` relation into one concrete platform implementation without pretending that ADR/eADR defines every persistence domain.

---

## Source set

### P1 — Intel, “Deprecating the PCOMMIT Instruction” (2016)

- **Organization:** Intel.
- **Document:** _Deprecating the PCOMMIT Instruction_.
- **ID:** 659301.
- **Updated:** 12 September 2016.
- **URL:** <https://www.intel.com/content/www/us/en/developer/articles/technical/deprecate-pcommit-instruction.html>
- **Role:** primary authority for Intel's `persistence domain` / `Power-fail Protected Domain or Persistent Domain` vocabulary, the `MOV → CPU cache → WPQ → DIMM` path, ADR's power-fail WPQ drain, and the reason `PCOMMIT` was deprecated.

Direct anchors from the page:

- “Enabling Persistent Memory Programming” — `CLWB` and `CLFLUSHOPT` flush stores from CPU cache toward the persistence domain; Intel defines the term as the portion of the platform data path where stores are power-fail safe;
- following paragraph — `PCOMMIT` had been intended for platforms where cache flush alone did not reach the domain and the memory-controller WPQ still needed an explicit drain to the DIMM;
- store-path discussion — `MOV` typically ends in CPU caches; a cache writeback can leave data in the WPQ;
- same discussion — a larger power-fail-safe domain exists on platforms that automatically flush the WPQ on power-fail or shutdown, with ADR named as the platform feature performing that work;
- “The Simpler Programming Model” — ADR support on persistent-memory platforms removes the need for application `PCOMMIT` logic;
- glossary — `Power-fail Protected Domain or Persistent Domain`, `ADR`, `WPQ`, cache-flush instructions, and `PCOMMIT` are defined in Intel's own vocabulary.

**Evidence quality:** strong first-party historical/programming-model evidence.

**Boundary:** the 2016 page describes product/platform planning as well as instruction deprecation. It should not alone be used to claim empirical behavior of every later product; P2/P3 supply later platform corroboration.

### P2 — Intel, SPDK persistent-memory article (2019)

- **Organization:** Intel.
- **Document:** _Enabling Persistent Memory in the Storage Performance Development Kit (SPDK)_.
- **ID:** 659394.
- **Updated:** 25 July 2019.
- **URL:** <https://www.intel.com/content/www/us/en/developer/articles/technical/enabling-persistent-memory-in-the-storage-performance-development-kit-spdk.html>
- **Role:** implementation-era corroboration that Intel Optane DC persistent-memory platforms required ADR and used it to make the memory-controller WPQ survive the sourced power-fail/shutdown path without `PCOMMIT`.

Direct anchor:

- “Committing to Persistence” — after cache flushing, modified data can still be in the memory-subsystem write buffer; the article notes that platforms supporting Intel Optane DC persistent memory are required to support ADR, which guarantees persistence during power-fail or shutdown by automatically flushing the memory-controller WPQ and thereby eliminates `PCOMMIT`.

**Evidence quality:** strong first-party technical corroboration.

**Boundary:** the article contains broader explanatory material about NVDIMMs and SPDK. Only the directly relevant Intel ADR/Optane statement is used here.

### P3 — Intel, third-generation Xeon technical overview (2020)

- **Organization:** Intel.
- **Document:** _Third Generation Intel Xeon Processor Scalable Family Technical Overview_.
- **ID:** 672628.
- **Updated:** 19 June 2020.
- **URL:** <https://www.intel.com/content/www/us/en/developer/articles/technical/intel-xeon-processor-scalable-family-overview.html>
- **Role:** primary authority for ADR versus eADR platform scope, eADR optionality, cache-flush changes, retained `SFENCE`, and OEM stored-energy requirements.

Direct anchors:

- Table 2 — first-generation Intel Optane persistent memory lists `ADR` for data persistence in a power-failure event; the 200-series lists `ADR, eADR (Optional)`;
- “Enhanced - Asynchronous DRAM Refresh (eADR)” — ADR causes memory-controller protected/write-pending buffers to be flushed and does **not** flush processor caches;
- same section — ADR-only software must perform cache flushes through `CLWB`, `CLFLUSH`, `CLFLUSHOPT`, non-temporal stores, or `WBINVD` as applicable;
- same section — eADR extends protection from the memory subsystem into processor caches during power failure;
- same section — PMDK detects eADR and does not need to perform explicit flush operations when it is present;
- same section — `SFENCE` remains required;
- same section — eADR requires additional OEM stored energy such as a backup battery.

**Evidence quality:** strong first-party platform evidence.

### P4 — Intel, two-socket third-generation Xeon overview (2021)

- **Organization:** Intel.
- **Document:** _Third Generation Intel Xeon Processor Scalable Family On Two Socket Platform Technical Overview_.
- **ID:** 660365.
- **Updated:** 21 March 2021.
- **URL:** <https://www.intel.com/content/www/us/en/developer/articles/technical/third-generation-xeon-scalable-family-overview.html>
- **Role:** independent dated Intel corroboration of the same eADR mechanism on the two-socket platform description.

Direct anchors:

- “Enhanced - Asynchronous DRAM Refresh (eADR)” — ADR protects the memory subsystem/WPQ and not processor caches;
- eADR extends protection into processor caches;
- PMDK detects eADR and can omit explicit flush operations;
- `SFENCE` remains required;
- OEM additional stored energy is required.

**Evidence quality:** strong first-party corroboration.

---

## Exact claim anchors

### 1. Intel used `persistence domain` as a power-fail path term in 2016

**Claim:** Intel's 2016 document defines the persistence domain as the portion/point along the platform store path where stores are power-fail safe / considered persistent.

**Evidence:** P1, “Enabling Persistent Memory Programming” and glossary.

**Strength:** high.

**Limit:** this is not a first-use claim. Case 31 already grounds SNIA use of `persistence domain` by 2013.

### 2. store execution can leave state in processor caches

**Claim:** Intel's store-path description says `MOV` typically leaves the store in CPU caches before explicit cache writeback.

**Evidence:** P1 store-path discussion.

**Strength:** high.

**Engineering consequence:** `store execution ≠ ADR-domain arrival` on an ADR-only path.

### 3. cache writeback can still leave state in a memory-controller WPQ

**Claim:** after cache writeback, Intel says the store may remain for some time in a memory-controller WPQ.

**Evidence:** P1 store-path discussion; P2 “Committing to Persistence.”

**Strength:** high.

### 4. ADR power-fail-protects the memory-controller queue by draining it

**Claim:** Intel defines ADR as a platform feature in which imminent power-fail signaling causes memory-subsystem write-pending queues to be flushed; P2 later says Intel Optane DC persistent-memory platforms require ADR and that this automatic WPQ flush guarantees persistence during power-fail/shutdown.

**Evidence:** P1 glossary/store-path discussion; P2.

**Strength:** high.

**Limit:** the sources document the platform contract/mechanism. They are not independent empirical fault-injection qualification of every system build.

### 5. ADR does not protect processor-cache contents by itself

**Claim:** Intel's 2020 platform document explicitly says ADR protects the memory subsystem but does not flush processor caches.

**Evidence:** P3 eADR section.

**Strength:** high.

**Engineering consequence:** `ADR-protected WPQ ≠ processor-cache persistence`.

### 6. eADR is an optional extension for the sourced platform generation

**Claim:** Intel Table 2 lists `ADR, eADR (Optional)` for the 200-series/third-generation platform comparison.

**Evidence:** P3 Table 2.

**Strength:** high.

**Limit:** do not generalize eADR to every Intel Xeon system or every persistent-memory configuration.

### 7. eADR extends protection into processor caches

**Claim:** Intel says eADR extends the power-fail protection from the memory subsystem to processor caches and describes an NMI-assisted cache drain followed by ADR.

**Evidence:** P3; corroborated by P4.

**Strength:** high.

### 8. eADR changes the cache-flush obligation

**Claim:** Intel says PMDK detects eADR and does not need to perform flush operations when eADR is present.

**Evidence:** P3; corroborated by P4.

**Strength:** high.

**Engineering consequence:** the same persistent-memory medium can expose different software persistence work depending on the platform's protected domain.

### 9. eADR does not eliminate `SFENCE`

**Claim:** Intel explicitly states that `SFENCE` remains required under the sourced eADR model.

**Evidence:** P3; corroborated by P4.

**Strength:** high.

**Engineering consequence:** `domain expansion ≠ elimination of ordering/fencing`.

### 10. eADR relies on additional OEM stored energy

**Claim:** Intel says eADR requires the OEM to provide additional stored energy, e.g. a backup battery.

**Evidence:** P3; corroborated by P4.

**Strength:** high.

**Engineering consequence:** energy reserve can be constitutive retention infrastructure without being payload.

### 11. power-fail protected state need not already be on final nonvolatile media

**Claim:** under ADR, a store that has reached the WPQ is inside the sourced power-fail-safe domain because the platform guarantees the queue will be drained when power failure/shutdown is detected; under eADR that protected relation extends farther upstream into cache state.

**Evidence:** P1 + P3/P4.

**Strength:** high as an engineering reconstruction from directly documented platform behavior.

**Label:** E, not historical vocabulary.

### 12. the sourced failure envelope is not universal crash persistence

**Claim:** P1/P2 describe power-fail and shutdown behavior; P3/P4 describe power-failure behavior. These sources do not establish survival guarantees for arbitrary CPU reset, firmware bug, media corruption, software transaction failure, or every crash class.

**Evidence:** scope of P1–P4.

**Strength:** high as a source-boundary control.

---

## Historical terminology control

### `persistence domain`

Case 31 already establishes the exact phrase in SNIA's approved 2013 NVM Programming Model. P1 shows Intel using closely aligned persistence-domain vocabulary by 2016.

Safe statement:

> **Intel documented an ADR-backed power-fail persistence domain by 2016.**

Rejected statement:

> **Intel invented the persistence-domain concept or term.**

No invention-priority claim is supported here.

### `ADR` versus ordinary DRAM refresh

The Intel persistence-memory sources expand `ADR` as `Asynchronous DRAM Refresh`, but the mechanism they describe for this bounded use is platform-level imminent-power-fail signaling and draining of write-pending queues.

Case 21 separately grounds SDRAM `SELF REFRESH` as a recurring retention mode with internal refresh clocking and an explicit exit sequence.

Safe conclusion:

> **Intel ADR power-fail protection ≠ Micron SDRAM self-refresh.**

The shared word `refresh` is not evidence of mechanism identity or genealogy.

---

## Cross-case controls

### Case 31 — SNIA persistence domain

Case 31 establishes a programming-model boundary: data become durable relative to a persistence domain, recovery is failure-qualified, and multiple domain/configuration relations may exist.

Case 32 provides one concrete platform mapping:

```text
ADR:
processor cache  |  WPQ + PMem
     outside     |  power-fail protected


eADR:
processor cache + WPQ + PMem
      power-fail protected path
```

This is a useful implementation bridge but not evidence that every SNIA persistence domain has this topology.

### Case 15 — Intel SSD 320 PLP

Both cases make stored energy part of a failure-triggered transfer guarantee.

Case 15 is an SSD controller/buffer → NAND handoff. Case 32 is a processor-cache / memory-controller-WPQ → persistent-memory path. The analogy is bounded to failure-triggered transfer and stored-energy infrastructure.

### Case 20 — NVMe 1.0

Case 20 uses queued namespace commands, VWC, Flush, FUA, and NVMe atomicity fields. ADR/eADR is not an NVMe command-set mechanism and should not be described with that vocabulary.

### Case 30 — NVMe PMR

Case 30's PMR is a named PCIe persistent-memory region with PMR-specific barriers, readiness, restore, and error status. Case 32 is a cache-coherent CPU/memory-controller path. Functional persistence-barrier comparisons do not establish synonymy.

### Case 21 — SDRAM refresh mode

Micron's `SELF REFRESH` is recurring DRAM retention work. Intel ADR/eADR, despite the acronym expansion, is a power-fail protection path. The comparison exists mainly to prevent a terminology collision.

---

## Prior-art boundary

This case makes **no** first-use or invention claim for:

- persistent memory;
- persistence domains;
- battery/capacitor-backed memory;
- ADR-like power-fail draining;
- NVDIMMs;
- cache-line persistence instructions.

The contribution is narrower:

> **dated Intel first-party material lets the repository follow a concrete protected boundary from memory-controller WPQs under ADR to processor caches under eADR, while separately tracking software flush/fence and stored-energy obligations.**

A genuine historical genealogy of battery-backed memory, NVDIMM-N, ACPI NFIT, JEDEC persistent-memory standards, Intel ISA flush instructions, or non-Intel platform protection belongs in separate work and, where primarily technical history, should normally be routed through `computing-archaeology`.

---

## Related-repository check

The available GitHub search for `tmzncty/computing-archaeology` was queried for dedicated `eADR` / ADR persistent-memory material and returned no obvious matching treatment.

This is a duplication check, not a proof of exhaustive absence. If `computing-archaeology` later develops a broader persistent-memory hardware/platform history, this case should link to it and keep only the retention-specific boundary comparison.

---

## Evidence maturity

**Recommended status: `grounded`.**

Reasons:

1. the central 2016 persistence-domain/ADR semantics are documented by a dated Intel first-party source;
2. a 2019 Intel source ties the ADR behavior to shipped Optane DC persistent-memory platforms;
3. a 2020 Intel platform overview explicitly distinguishes ADR and optional eADR and directly states cache-flush, `SFENCE`, and OEM-energy consequences;
4. a 2021 Intel platform overview independently corroborates the core eADR mechanism;
5. the case does not infer universal reset/crash/media-failure behavior from power-failure sources;
6. `persistence domain`, ADR/eADR, NVMe PMR, SSD PLP, and SDRAM self refresh remain historically distinct;
7. source claims, engineering reconstruction, analogy, and philosophical pressure are labeled separately;
8. no invention-priority claim is made.

Remaining work is outside this bounded case rather than a promotion blocker:

- empirical fault-injection qualification of named ADR/eADR platforms;
- exact firmware/NMI implementation details for particular machines;
- non-Intel persistence-domain implementations;
- FastADR / remote-persistent-memory evolution;
- CPU cache-flush/fence ISA genealogy;
- operating-system/database composition above the platform boundary.