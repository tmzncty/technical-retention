# Case 31 grounding — SNIA NVM Programming Model persistence domain (2013)

## Purpose

This record grounds [`../cases/31-snia-nvm-persistence-domain-boundary.md`](../cases/31-snia-nvm-persistence-domain-boundary.md).

The bounded question is deliberately narrower than a history of persistent memory:

> **What does the exact term `persistence domain` mean in SNIA's approved 2013 NVM Programming Model, what durability/recovery guarantees does reaching that domain supply, and what does it *not* supply?**

A second, tightly controlled terminology check asks whether the exact phrase can safely be attributed to the later NVMe PMR interface already studied in Case 30.

The result is a correction to the roadmap's earlier shorthand. The phrase is directly documented in SNIA Version 1 in 2013; ratified NVMe 1.4 and 2.0 use `Persistent Memory Region` / write-barrier vocabulary but the exact phrase `persistence domain` was not found in the inspected PDFs. This does not prove a universal first use or absence from every NVMe revision.

---

## Source set

### P1 — SNIA NVM Programming Model Version 1

- **Organization:** Storage Networking Industry Association (SNIA).
- **Document:** _NVM Programming Model (NPM), Version 1_.
- **Status:** SNIA Technical Position; cover says released and approved by SNIA.
- **Date:** 21 December 2013.
- **Official PDF:** <https://www.snia.org/sites/default/files/technical-work/npm/release/SNIA-NVM-Programming-Model-v1.pdf>
- **Role:** primary authority for `persistence domain`, `durable`, PM synchronization, failure-qualified recoverability, multiple-domain configuration, and atomicity/ordering limits.

Directly inspected text-layer anchors:

- cover / PDF p. 1 — title, Version 1, Technical Position, date;
- foreword printed p. 7 — software/OS behavior and API-independent intent;
- §1 printed pp. 8–9 — scope including SSD/PCI-card NVM and memory-accessed devices; atomicity/durability/error-recovery goals;
- §2 printed p. 9 — NVMe 1.1 listed as a separate approved reference;
- §3.1.1 and §3.1.7 printed p. 10 — `durable` and `persistence domain` definitions;
- §3.1.8 printed p. 10 — `persistent memory` definition;
- §6.9 printed p. 21 — recovery depends on tolerated failure pattern; multiple domains; administrative alignment to volumes/filesystems;
- §10.1 printed p. 57 — mapped writes may remain in processor caches or memory-controller buffers before reaching a persistence domain;
- §10.2.4 printed pp. 59–60 — `NVM.PM.FILE.SYNC` pushes specified ranges to the domain and explicitly does not create write atomicity;
- §10.2.5 printed pp. 60–61 — optimized flush has no atomicity/order guarantee and interrupted progress is indeterminate;
- §10.3.3 printed p. 63 — interrupted-store atomicity is a separately discoverable property.

The official PDF text layer is internally consistent and exposes exact page/section anchors. Attempts to render selected SNIA pages through the research environment returned a cache/fetch error, so this record makes **no layout-, typography-, diagram-, or marginalia-dependent claim** from those failed renders. The claims above depend on official source text, not OCR.

### P2 — NVM Express Base Specification Revision 1.4

- **Organization:** NVM Express, Inc.
- **Document:** _NVM Express Base Specification Revision 1.4_.
- **Date:** 10 June 2019.
- **Official PDF:** <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf>
- **Role:** terminology/interface comparison with Case 30.

Directly checked:

- cover — revision/date;
- printed p. 86 §4.8 — `Persistent Memory Region (PMR)`;
- `PMRCAP.PMRWBM` — PMR write-barrier mechanisms ensuring prior writes have completed and are persistent;
- exact PDF-text search for `persistence domain` — **no match**.

The §4.8 page was also visually rendered and inspected. It identifies PMR as an optional general-purpose PCIe read/write persistent-memory region. This confirms that the comparison is based on a different explicit historical term, not merely on failed text search.

### P3 — NVM Express Base Specification Revision 2.0

- **Organization:** NVM Express, Inc.
- **Document:** _NVM Express Base Specification Revision 2.0_.
- **Date:** 2 June 2021.
- **Official PDF:** <https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-2_0-2021.06.02-Ratified-5.pdf>
- **Role:** later NVMe terminology check.

Directly checked:

- `PMRCAP.PMRWBM` still uses `Persistent Memory Region` write-barrier vocabulary and requires a supported mechanism under which a read completion establishes prior PMR writes as completed and persistent;
- rendered PMRCAP page visually confirms the terminology;
- exact PDF-text search for `persistence domain` — **no match**.

### P4 — NVM Express Specification Archives

- **Organization:** NVM Express, Inc.
- **Official page:** <https://nvmexpress.org/nvm-express-specification-archives/>
- **Role:** provenance/navigation for ratified specification revisions.

The archive lists ratified/previous base specifications including 1.4, 2.0, 2.1, 2.2, and 2.3. The research interface could not ingest the much larger 2.1–2.3 PDFs in this run, so **no exact-phrase absence claim is made for those revisions**. The current NVM Express base-specification page identifies revision 2.4 as the current 2026 specification, but that large current PDF likewise was not part of the exact-text negative check.

---

## Exact claim anchors

### 1. Version/date and institutional status

**Claim:** SNIA _NVM Programming Model Version 1_ is a SNIA Technical Position dated 21 December 2013 and says it has been released and approved by SNIA.

**Evidence:** P1 cover / PDF p. 1.

**Strength:** high.

**Limit:** copyright text on a later page says © 2014 SNIA; this does not alter the cover's explicit Technical Position date. The case reports the source's stated date rather than inferring a separate publication event.

### 2. `durable` is defined via the persistence domain

**Claim:** §3.1.1 defines `durable` as committed to a persistence domain, while §3.1.7 defines the domain as a location where data are guaranteed to preserve contents across restart of the containing device.

**Evidence:** P1 printed p. 10.

**Strength:** high.

**Engineering consequence:** `durability` is expressed as a relation to a boundary/location, not merely by saying the underlying medium is nonvolatile.

### 3. persistence-domain arrival is not universal recovery

**Claim:** §6.9 says data that reached a persistence domain may be recoverable during restart processing, and that recoverability depends on whether the failure pattern can be tolerated by the design/configuration of the domain.

**Evidence:** P1 printed p. 21.

**Strength:** high.

**Engineering consequence:** `domain reached ≠ unconditional recoverability`.

**Limit:** the specification does not enumerate every possible physical failure pattern for every hardware realization. This case therefore does not assign a universal failure envelope.

### 4. one system may have multiple persistence domains

**Claim:** multiple persistence domains may coexist, and aligning them with volumes/filesystems is an administrative act required to preserve compliant behavior.

**Evidence:** P1 printed p. 21.

**Strength:** high.

**Engineering consequence:** `persistence domain ≠ one global machine boundary`; configuration/administration can participate in the durability contract.

### 5. store execution can precede persistence-domain arrival

**Claim:** mapped writes may remain in processor-resident caches or memory-controller buffers before reaching the persistence domain.

**Evidence:** P1 printed p. 57 and §10.2.4 printed p. 59.

**Strength:** high.

**Engineering consequence:** `store execution ≠ persistence qualification`.

### 6. data may reach the domain before explicit synchronization

**Claim:** mapped data may become persistent before `NVM.PM.FILE.SYNC`, and the range named by sync may already have reached a domain before the call.

**Evidence:** P1 §10.1 printed p. 57; §10.2.4 printed pp. 59–60.

**Strength:** high.

**Engineering consequence:** sync completion is a **closure/latest-guaranteed point**, not necessarily the physical instant at which every byte crossed the durability boundary.

### 7. successful sync guarantees domain arrival but not write atomicity

**Claim:** successful `NVM.PM.FILE.SYNC` guarantees that the referenced range reaches the persistence domain by completion, while the same section explicitly says the action does not guarantee write atomicity.

**Evidence:** P1 §10.2.4 printed pp. 59–60.

**Strength:** high.

**Engineering consequence:** `durability closure ≠ atomic transaction`.

### 8. optimized flush adds neither atomicity nor ordering

**Claim:** `NVM.PM.FILE.OPTIMIZED_FLUSH` provides no guarantee of atomicity within/across synchronized ranges and no guarantee of the order in which bytes reach a persistence domain.

**Evidence:** P1 §10.2.5 printed p. 61.

**Strength:** high.

**Engineering consequence:** `persistent arrival ≠ consistency protocol`; software may still need explicit ordering/logging/update rules above the persistence primitive.

### 9. interruption can leave unknown partial persistence progress

**Claim:** if optimized flush is interrupted by failure, various byte ranges may or may not have reached a domain and the action provides no indication of exactly which ranges did.

**Evidence:** P1 §10.2.5 printed p. 61.

**Strength:** high.

**Engineering consequence:** `flush started ≠ known durable subset` and `partial physical progress ≠ retained completion metadata`.

### 10. failure atomicity is separate from durability

**Claim:** `NVM.PM.FILE.INTERRUPTED_STORE_ATOMICITY` separately reports whether aligned stores reach NVM atomically under interruption; absent that property, restart may expose neither the full old nor full new state.

**Evidence:** P1 §10.3.3 printed p. 63.

**Strength:** high.

**Engineering consequence:** `persistent location ≠ power-fail atomic write`.

### 11. `persistence domain` is SNIA historical vocabulary no later than 2013

**Claim:** the exact phrase appears as a defined term in the approved 2013 SNIA Technical Position.

**Evidence:** P1 cover and §3.1.7.

**Strength:** high for the **no-later-than** statement.

**Limit:** no first-use/invention claim is made. A true terminology genealogy would need earlier standards drafts, vendor documents, academic papers, JEDEC/ACPI/NVDIMM sources, and possibly processor/platform documentation.

### 12. SNIA's term should not be silently reassigned to NVMe PMR

**Claim:** the SNIA source defines `persistence domain` and separately cites NVMe 1.1 as a referenced approved standard. Later ratified NVMe 1.4 and 2.0 use `Persistent Memory Region` / PMR write-barrier language; exact text search of the two inspected PDFs found no `persistence domain` match.

**Evidence:** P1 §2 and §3.1.7; P2; P3.

**Strength:** high for the source-vocabulary distinction; medium for any broader protocol-history inference.

**Safe conclusion:** `SNIA persistence domain ≠ NVMe PMR` as historical vocabulary and abstraction shape.

**Rejected overclaim:** `NVMe never uses persistence domain`.

---

## Negative-result control

Exact-phrase absence claims are easy to overstate. This record therefore preserves the following boundary:

```text
Directly checked official ratified PDFs:
  NVMe 1.4 (2019) → no exact `persistence domain` text match
  NVMe 2.0 (2021) → no exact `persistence domain` text match

Not exhaustively text-inspected here:
  NVMe 2.1
  NVMe 2.2
  NVMe 2.3
  NVMe 2.4
  all Technical Proposals / Errata / ECNs
  NVMe-MI / transport / command-set specifications
  vendor implementation documents
```

The NVM Express archive was used to verify those later revision families exist. The research interface rejected the 2.1–2.3 PDFs as too large for ingestion. This is a tooling/evidence boundary, not evidence of absence.

---

## Cross-case controls

### Case 15 — SSD 320 PLP

Case 15 grounds one concrete manufacturer path:

```text
volatile staging
→ power-loss detection
→ capacitor hold-up energy
→ emergency NAND transfer
```

Case 31 does not infer that mechanism. SNIA intentionally defines a cross-hardware durability boundary.

### Case 20 — NVMe 1.0 Flush/FUA

Case 20 uses queued namespace/LBA commands and NVMe's historical terms `VWC`, `Flush`, `FUA`, `AWUN`, and `AWUPF`. Case 31 is a 2013 SNIA programming-model layer for mapped PM and therefore **must not back-project `persistence domain` into NVMe 1.0 vocabulary**.

The functional commonality is only that software needs a point after which a state can be relied upon across a specified interruption.

### Case 30 — NVMe 1.4 PMR

Case 30 grounds:

```text
PCIe PMR writes
→ PMRWBM-supported read barrier
→ prior writes completed and persistent
→ separate ready/health/restore status
```

Case 31 grounds:

```text
mapped PM stores
→ possible processor/controller buffering
→ persistence-domain arrival
→ explicit sync/flush closure
→ failure-qualified recovery
```

The two are useful functional comparisons but are not synonyms. PMR is a named NVMe region/interface; SNIA's domain is a cross-layer durability boundary/location.

### Case 16 — filesystem durability closure

SNIA explicitly models volume/filesystem alignment and native synchronization relations, but it does not collapse durability into transaction consistency. This supports Case 16's lower-layer composition rule: a durability primitive can be necessary while remaining insufficient to establish all filesystem/application invariants.

---

## Prior-art / terminology boundary

The case establishes only a conservative terminology anchor:

> **`persistence domain` is directly documented by SNIA by 21 December 2013.**

It does not establish first use, invention priority, or a direct genealogy into later platform-specific terms.

The prior roadmap phrase `later NVMe persistence domain terminology` is therefore too presumptive. A better open history is:

- earlier origins of the phrase, if any;
- SNIA programming-model evolution after v1;
- platform mappings such as power-fail protected domains/ADR/eADR, each with its own primary sources;
- OS/DAX/PMDK persistence primitives and cache-line flush/fence evolution;
- whether any specific NVMe revision/TP later adopts the exact phrase.

The present case closes only the bounded 2013 terminology/mechanism question.

---

## Related-repository check

`tmzncty/computing-archaeology` was checked through the current repository tree/index and available code search for a dedicated NVMe / PMR / `persistence domain` case. No dedicated matching treatment was found.

This is sufficient to avoid duplicating an obvious existing technical-history case, but it is not a proof that no incidental mention exists anywhere in that repository. The present contribution stays narrow and retention-specific.

A future broad history of persistent-memory hardware/platform evolution belongs primarily in `computing-archaeology`; this repository should reuse it and retain the cross-case durability analysis.

---

## Evidence maturity

**Recommended case status: `grounded`.**

Reasons:

1. the central historical term is directly defined in an approved 2013 primary specification;
2. exact section/page anchors establish durability, recoverability limits, multiple-domain configuration, synchronization, and atomicity/order boundaries;
3. the source itself separates SNIA vocabulary from referenced NVMe 1.1;
4. the later PMR comparison uses official ratified NVMe 1.4 and 2.0 sources;
5. NVMe PMR pages were visually inspected as well as text-inspected;
6. the failed SNIA page-render path is documented and no image-dependent claim is made from it;
7. the negative exact-phrase check is bounded rather than universalized;
8. no first-use, invention-priority, concrete-hardware-substrate, or universal-failure-domain claim is made.

Remaining future work is deliberately outside this bounded promotion:

- pre-2013 terminology genealogy;
- SNIA v1.1/v1.2+ evolution;
- platform-specific ADR/eADR/power-fail-protected-domain history;
- exact NVMe 2.1–2.4 / TP terminology archaeology if evidence becomes ingestible;
- OS/DAX/PMDK cache-flush/fence composition;
- database/filesystem transaction composition;
- named hardware compliance and fault injection.

---

## Source links

- SNIA NVM Programming Model v1: <https://www.snia.org/sites/default/files/technical-work/npm/release/SNIA-NVM-Programming-Model-v1.pdf>
- NVM Express 1.4 ratified PDF: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf>
- NVM Express 2.0 ratified PDF: <https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-2_0-2021.06.02-Ratified-5.pdf>
- NVM Express specification archive: <https://nvmexpress.org/nvm-express-specification-archives/>