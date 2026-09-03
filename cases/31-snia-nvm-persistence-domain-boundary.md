# SNIA NVM Programming Model v1: Persistence Domain as a Durability Boundary

## Scope

- **Object / system:** SNIA _NVM Programming Model (NPM) Version 1_.
- **Bounded period:** 2013, with narrow terminology checks against ratified NVMe 1.4 (2019) and NVMe 2.0 (2021).
- **Institution:** Storage Networking Industry Association (SNIA).
- **Primary question:** what did the 2013 programming model mean by `persistence domain`, and what must software distinguish before it may call directly stored persistent-memory data `durable`?

This is not a general history of NVDIMMs, storage-class memory, byte-addressable NVM, CPU cache flush instructions, ADR/eADR, PMDK, DAX, NVMe, or database persistence. It is a terminology-and-interface bridge chosen because Cases 20 and 30 left an explicit open question about later `persistence domain` language.

The bounded result is corrective rather than teleological:

> **`persistence domain` is directly documented no later than SNIA's 2013 cross-layer NVM programming model. It should not be projected backward onto NVMe 1.0, and it should not be assumed to be an NVMe-defined term merely because later NVMe PMR mechanisms also expose persistence barriers.**

The official ratified NVMe 1.4 and 2.0 PDFs were checked for the exact phrase `persistence domain`; no matching text was found in those two revisions. That negative result is deliberately bounded to those inspected revisions and is not a claim that the phrase never appears anywhere in the NVMe family or later revisions.

---

## Historical vocabulary

SNIA Version 1 itself uses:

- `durable`;
- `persistence domain`;
- `persistent memory` / `PM`;
- `NVM.PM.FILE`;
- `NVM.PM.FILE.SYNC`;
- `NVM.PM.FILE.OPTIMIZED_FLUSH`;
- `NVM.PM.FILE.OPTIMIZED_FLUSH_AND_VERIFY`;
- `processor resident caches`;
- `memory controller buffers`;
- `recoverability`;
- `write atomicity`;
- `INTERRUPTED_STORE_ATOMICITY`;
- `volume` and `file system`.

The following are **project engineering terms**, not SNIA's period vocabulary:

- `durability boundary`;
- `boundary-crossing obligation`;
- `failure-qualified recoverability`;
- `persistence qualification`;
- `recovery envelope`;
- `cross-layer retention relation`.

This case therefore does not silently rewrite SNIA's `persistence domain` as an NVMe `PMR`, Intel `ADR`, a capacitor-backed cache, a CPU cache hierarchy, or one particular physical memory technology.

---

## Historical record

### H/P — SNIA Version 1 is a 2013 software-behavior specification

The cover of _NVM Programming Model (NPM) Version 1_ identifies the document as a **SNIA Technical Position** dated **21 December 2013**. Its foreword says the specification defines recommended behavior between user-space and operating-system-kernel components supporting NVM, and explicitly says it does not prescribe one specific API.

Its scope includes flash packaged as SSDs and PCI cards as well as solid-state nonvolatile devices that may be accessed as memory. It identifies atomicity, durability, error/failure recovery, data granularity, and capacity reclamation as programming-model concerns.

**Primary anchors:** cover / PDF p. 1; foreword printed p. 7; §1 printed pp. 8–9.

### H/P — `durable` is defined through a `persistence domain`

SNIA §3.1.1 defines `durable` as being **committed to a persistence domain**. Section 3.1.7 defines `persistence domain` as a location for data guaranteed to preserve its contents across a restart of the device containing that data.

This is a historical vocabulary claim, not a modern reconstruction.

**Primary anchor:** §3.1.1 and §3.1.7, printed p. 10.

### H/P — reaching the persistence domain does not promise recovery under every failure

Section 6.9 says that once data has reached a persistence domain, it **may be recoverable** during processing after a system restart. Recoverability depends on whether the particular failure pattern affecting the system can be tolerated by the design and configuration of the persistence domain.

Thus SNIA itself does not equate `in the persistence domain` with `unconditionally recoverable under any failure`.

**Primary anchor:** §6.9, printed p. 21.

### H/P — a system may contain multiple persistence domains

The same section states that multiple persistence domains may exist within one system. It further says that aligning persistence domains with volumes and/or file systems is an **administrative act** that must preserve programming-model behavior from the point of view of each compliant volume or file system.

This is direct evidence that the term does not necessarily name one globally uniform physical boundary for an entire machine.

**Primary anchor:** §6.9, printed p. 21.

### H/P — mapped stores can remain before the domain in processor or memory-controller state

In the `NVM.PM.FILE` discussion, SNIA notes that memory-mapped writes may be retained within processor-resident caches or memory-controller buffers before they reach a persistence domain. It also allows the bytes to become persistent before the application invokes the corresponding synchronization action.

The source therefore distinguishes at least three things:

```text
store has executed
    ≠
bytes have necessarily reached the persistence domain
    ≠
software has executed a synchronization action proving the requested range has reached it
```

**Primary anchors:** §10.1, printed p. 57; §10.2.4, printed pp. 59–60.

### H/P — `NVM.PM.FILE.SYNC` closes a durability relation, not an atomic transaction

Section 10.2.4 says the purpose of `NVM.PM.FILE.SYNC` is to assure durability and enable recovery by forcing data to reach the persistence domain. It is responsible for ensuring data held in processor or memory buffers reaches that domain.

But the same section explicitly says:

- updates may become persistent in any order before the sync;
- sync on a shared mapping does not guarantee write atomicity;
- the byte range may already have reached the domain before sync;
- successful completion guarantees only that the referenced range has reached the persistence domain by that completion point.

Atomicity, where present, comes from some other mechanism.

**Primary anchor:** §10.2.4, printed pp. 59–60.

### H/P — optimized flush also does not supply order or atomicity

`NVM.PM.FILE.OPTIMIZED_FLUSH` has the same general purpose of forcing one or more ranges to the persistence domain, but SNIA explicitly states that it supplies no guarantee of atomicity within or across those ranges and no guarantee of the order in which bytes reach the domain.

If failure interrupts the operation, progress is indeterminate: some ranges may have reached the domain and others may not, with no indication of exactly which ones did.

**Primary anchor:** §10.2.5, printed pp. 60–61.

### H/P — interrupted-store atomicity is separately discoverable

SNIA separately defines `NVM.PM.FILE.INTERRUPTED_STORE_ATOMICITY`. If the relevant capability is absent, an aligned store interrupted by reset, power loss, or system crash may leave persistent memory containing neither the complete pre-store nor complete post-store value.

This is period-primary evidence that persistence-domain arrival, durability, and failure atomicity are not one property.

**Primary anchor:** §10.3.3, printed p. 63.

### H/P — SNIA treats NVMe 1.1 as a separate referenced standard

The Version-1 reference list includes **NVMe 1.1, NVM Express Revision 1.1** as a separate approved standard. In the same SNIA document, `persistence domain` is defined in SNIA's own terminology and programming-model clauses.

This is not proof that no NVMe text could ever use the phrase. It is, however, a strong anti-anachronism control against calling `persistence domain` an NVMe-owned term merely because SNIA's model also encompasses NVM block devices.

**Primary anchor:** §2 References, printed p. 9; §3.1.7 printed p. 10.

### H/P — inspected NVMe 1.4 and 2.0 retain PMR vocabulary without the exact phrase

The official ratified NVMe 1.4 PDF (10 June 2019) introduces the optional **Persistent Memory Region (PMR)** and defines PMR write-barrier mechanisms. The official ratified NVMe 2.0 PDF (2 June 2021) retains the PMR capability and write-barrier language. Exact-text searches of both inspected PDFs found no match for `persistence domain`.

This bounded negative check prevents Case 30's PMR from being renamed with an unsupported historical term. It does **not** establish absence from NVMe 2.1+, technical proposals, implementation documentation, PCIe specifications, ACPI/NVDIMM standards, or vendor literature.

**Primary anchors:** NVMe 1.4 §4.8 and `PMRCAP.PMRWBM`; NVMe 2.0 `PMRCAP.PMRWBM`; exact-phrase searches of the ratified PDFs.

---

## Retained state

This case is about more than payload bytes.

### 1. Application-visible PM bytes

The intended data ultimately must survive the restart conditions represented by the selected persistence domain.

### 2. Mapping and designation state

`NVM.PM.FILE` maps persistent-file ranges into an application's address space. The mapping determines which application addresses designate the persistent state during access.

### 3. Pre-domain write state

Stores may remain in processor caches, write pipelines, or memory-controller buffers before reaching the persistence domain. These are not automatically equivalent to durable PM state.

### 4. Synchronization obligation

Software needs a mechanism that closes the gap between `a store was executed` and `the required range has reached the persistence domain`. `NVM.PM.FILE.SYNC` and optimized flush are explicit relations for that purpose.

### 5. Failure-model and configuration relation

SNIA conditions recoverability on the failure pattern tolerated by the design/configuration of the persistence domain. Which failure boundary the system can survive is therefore constitutive of what the durability promise means.

### 6. Administrative alignment

When multiple persistence domains exist, their relationship to volumes and filesystems must be configured so that the programming-model guarantees remain true. This administrative relation is not payload, but it participates in making the software-visible durability contract valid.

---

## Physical / logical substrate

The programming model is intentionally hardware-generic. It can describe block NVM, persistent-memory devices, NVDIMMs, PCIe cards, and other NVM technologies.

Accordingly, this bounded case does **not** identify the persistence domain with one physical component. The domain is a software-visible durability location/boundary whose concrete realization depends on platform design and configuration.

This is precisely why it changes the retention comparison: the historical source itself defines durability at a cross-layer boundary while leaving the particular physical embodiment open.

---

## Retention mechanism

The bounded operational chain is:

```text
application store
    ↓
processor/cache/write-pipeline and/or memory-controller state may still hold the update
    ↓
write may reach the persistence domain before explicit synchronization
    ↓
SYNC / OPTIMIZED_FLUSH can force the named range(s) across the boundary
    ↓
successful sync establishes that the requested range has reached the persistence domain
    ↓
a later restart may recover the data if the experienced failure pattern is within the domain's tolerated design/configuration
```

The mechanism therefore includes both movement of data and qualification of a failure boundary. It is not simply `the medium is nonvolatile`.

---

## Addressing and access geometry

`NVM.PM.FILE` exposes a PM file through direct load/store mapping. This differs from the queued namespace/LBA command path in Case 20 and from the NVMe PMR BAR/address relation in Case 30.

The relevant resolution chain is approximately:

```text
file / mapped range
→ process virtual address
→ PM-aware mapping / underlying PM volume
→ implementation-specific hardware path
→ persistence domain
```

The persistence domain answers a different question from the mapping:

- mapping asks **which retained bytes does this address designate?**
- persistence-domain qualification asks **how far through the write/recovery path must the update travel before software may rely on survival across the stated restart boundary?**

---

## Read semantics

Direct loads may read persistent memory through the normal memory model. SNIA also discusses asynchronous hardware error reporting because a mapped load/store lacks the ordinary function-call acknowledgement available to traditional I/O.

This case does not attempt a full machine-check or PM error-handling history. The relevant retention point is narrower: readable addressability, durable placement, and verified recovery are separable relations.

---

## Write and erasure semantics

### Store

A store changes the program-visible memory path but may still leave the new value outside the persistence domain in processor or controller buffering.

### Sync / optimized flush

These operations provide the explicit software closure that forces specified ranges to the persistence domain. They do not create write atomicity or cross-range ordering by themselves.

### Failure during synchronization

For optimized flush, some ranges may cross the boundary before interruption while others may not, and the source supplies no per-range completion map after the interrupted operation.

### Erasure

Secure erase exists elsewhere in the SNIA model, but it is outside this case. A persistence domain is a durability/recovery relation, not itself a forgetting primitive.

---

## Time

This case separates several times:

- the time a CPU store executes;
- the time dirty data leave processor/cache/write-pipeline state;
- the time data leave memory-controller buffering;
- the time data actually cross the persistence-domain boundary;
- the time a synchronization action begins;
- the time successful sync provides a latest guaranteed completion point for the requested range;
- the time a failure/restart occurs;
- the later time at which recovery determines whether the failure pattern was survivable.

A particularly useful negative result follows directly from the source: successful sync does not tell us the exact instant each byte became persistent, because the bytes may have crossed the boundary before the sync call.

---

## Maintenance and labor

The persistence promise depends on work distributed across layers:

- CPU and cache/write-pipeline behavior;
- memory-controller buffering;
- kernel/filesystem implementation of PM mapping and synchronization;
- application selection of the ranges that require durability;
- platform/device design of the persistence domain;
- administrator alignment of domains with volumes/filesystems where more than one domain exists;
- recovery logic after restart.

Persistence can therefore appear to software as a simple property while being maintained by both automatic mechanisms and explicit configuration/administration.

---

## Failure / forgetting modes

Distinct failure modes include:

- relying on a store while its new value is still outside the persistence domain;
- assuming that successful sync also supplied atomicity or write ordering;
- interruption of an optimized flush, leaving unknown partial progress;
- a failure pattern exceeding what the configured persistence domain can tolerate;
- incorrect administrative alignment between domains and volumes/filesystems;
- an interrupted store whose implementation does not provide the claimed failure atomicity;
- loss/corruption of the mapping or recovery machinery needed to interpret the persistent bytes;
- confusing `data reached the persistence domain` with `data is guaranteed recoverable after every imaginable fault`.

These are different from physical medium decay, secure erasure, or ordinary logical deletion.

---

## Engineering reconstruction

### E — persistence domain ≠ persistent medium

SNIA defines the domain as the location/boundary at which durability is established for the programming model. The source deliberately spans multiple hardware forms. Treating the domain as the name of one NVM chip or device would collapse an abstraction the source keeps open.

### E — durability boundary reached ≠ unconditional recoverability

Section 6.9 explicitly conditions post-restart recoverability on the failure pattern tolerated by the persistence-domain design and configuration. The durability guarantee is therefore failure-qualified.

### E — store execution ≠ persistence qualification

Processor caches and memory-controller buffers may retain an update before it reaches the domain. Executing the store and establishing persistence are distinct events.

### E — successful sync ≠ atomic commit or ordering barrier for all semantics

SNIA explicitly withholds atomicity and ordering guarantees from the synchronization actions described here. A higher-level protocol still needs whatever ordering, logging, copy-on-write, or atomic-update mechanism its consistency model requires.

### E — sync completion ≠ exact persistence timestamp

A range may cross the domain before the sync call. Successful completion establishes an upper bound for the requested range, not a precise timestamp for each byte's persistence.

### E — persistence domain ≠ one global machine boundary

Multiple domains may coexist. The durability boundary is therefore potentially scoped to a volume/filesystem relation rather than one universal machine-wide line.

### E — durability configuration can be constitutive retention state

The administrative alignment of persistence domains to software-visible storage objects helps determine whether the promised restart behavior is valid. Configuration and failure-model relations can be part of the technical conditions under which state remains recoverable.

---

## Functional analogies

### A — Case 15, Intel SSD 320 power-loss protection

Case 15 grounds one named product's path from volatile staging to NAND using stored capacitor energy during an unexpected power event. SNIA Version 1 instead defines a cross-platform programming boundary and does not prescribe that mechanism.

Functional similarity: both ask when a newer state has crossed a power-failure vulnerability boundary.

Historical identity: **rejected**.

### A — Case 20, NVMe 1.0 Flush/FUA

Case 20 operates through namespace/LBA commands, VWC, Flush, FUA, and command completion. SNIA's PM mode uses direct mapped stores plus synchronization to a persistence domain.

The comparison shows a shared durability question expressed through different interfaces. `persistence domain` must not be projected backward as NVMe 1.0 historical vocabulary.

### A — Case 30, NVMe 1.4 PMR

NVMe PMR also needs a stronger relation than merely issuing a write: supported read-based barriers establish that preceding Posted PCIe writes have completed and are persistent. But PMR is a named NVMe region/interface feature, while SNIA's persistence domain is a programming-model durability location that can exist across different hardware stacks.

Therefore:

> **SNIA persistence domain ≠ NVMe Persistent Memory Region.**

They are functionally comparable around persistence qualification, not synonyms or proof of genealogy.

### A — Case 16, filesystem `fsync`

Both cases show that an explicit synchronization operation can close a durability obligation without itself proving every higher-level consistency property. Case 16's filesystem object is relational across payload/allocation/inode/naming state; the SNIA PM case focuses on moving specified mapped ranges across a persistence boundary. The comparison is functional only.

---

## Philosophical / media-theoretical interpretation

### I — persistence is not exhausted by the material adjective `nonvolatile`

The case pressures any interpretation that treats technical persistence as a simple property located wholly inside a medium. The historical programming model itself requires a boundary, a failure assumption, a synchronization relation, and a recovery path.

That supports a narrow interpretation:

> what remains technically available after interruption can depend on where a system draws and enforces a recoverability boundary, not only on whether some underlying material can retain a physical distinction.

This does not establish a general philosophical thesis about memory, archive, or `Bestand`. It only supplies a mechanism-level constraint that later interpretation must respect.

---

## Counterexamples and limits

This case does **not** establish that:

- SNIA invented the phrase or concept `persistence domain`;
- the phrase first appeared in December 2013;
- every implementation places the boundary at the same physical component;
- every persistence domain survives every system or device failure;
- `NVM.PM.FILE.SYNC` is equivalent to every operating system's later `msync`, `fsync`, `clwb`, `sfence`, or PMDK primitive;
- SNIA's domain is identical to Intel ADR/eADR or any named platform's power-fail protected domain;
- `persistence domain` is an NVMe term;
- the phrase is absent from every NVMe revision or related technical proposal;
- NVMe PMR and SNIA persistence domains are historically one mechanism;
- reaching a persistence domain supplies transaction atomicity, ordering, or application consistency.

The negative NVMe terminology check is limited to the directly inspected ratified NVMe 1.4 and 2.0 PDFs. NVMe 2.1–2.4 PDFs were not exhaustively text-inspected in this slice because the available research interface could not ingest their larger files; no absence claim is made for them.

---

## Prior art / terminology boundary

The safest positive historical statement is:

> **The exact term `persistence domain` is documented in an approved SNIA Technical Position no later than 21 December 2013.**

The document itself cites NVMe 1.1 as a separate approved standard. Later official NVMe 1.4 and 2.0 specifications use their own `Persistent Memory Region` and persistence-barrier vocabulary without an exact-text match for `persistence domain` in the inspected PDFs.

This corrects the earlier roadmap shorthand `later NVMe persistence-domain terminology`: the research problem is better framed as **cross-layer persistence-domain terminology and implementation history**, with NVMe PMR as one separate comparison rather than the assumed origin of the term.

Broader priority work—earlier NVDIMM standards, ACPI NFIT, JEDEC, Intel platform documentation, academic persistent-memory systems, PCIe write-protection domains—belongs to a future terminology/genealogy study if it changes the retention comparison.

---

## Related repositories

Before writing this case, `tmzncty/computing-archaeology` was checked for a dedicated NVMe / PMR / `persistence domain` case through its current tree/index and available code search. No dedicated matching treatment was found.

Therefore this repository keeps only the retention-specific boundary argument. A general history of NVDIMMs, persistent-memory hardware, cache-flush instructions, ADR/eADR, or NVMe evolution should be routed to [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) if developed.

The anti-anachronism rule follows [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history): terminology must stay attached to the source that actually uses it.

---

## Sources

### Primary

1. Storage Networking Industry Association (SNIA), _NVM Programming Model (NPM), Version 1_, SNIA Technical Position, 21 December 2013. Official PDF: <https://www.snia.org/sites/default/files/technical-work/npm/release/SNIA-NVM-Programming-Model-v1.pdf>. Key anchors: cover; foreword printed p. 7; §1 pp. 8–9; §2 p. 9; §3.1 pp. 10–11; §6.9 p. 21; §10.1 p. 57; §10.2.4 pp. 59–60; §10.2.5 pp. 60–61; §10.3.3 p. 63.
2. NVM Express, Inc., _NVM Express Base Specification Revision 1.4_, 10 June 2019. Official PDF: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf>. Key anchors: `PMRCAP.PMRWBM`, §4.8 `Persistent Memory Region`; exact-phrase check for `persistence domain` returned no match.
3. NVM Express, Inc., _NVM Express Base Specification Revision 2.0_, 2 June 2021. Official PDF: <https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-2_0-2021.06.02-Ratified-5.pdf>. Key anchor: `PMRCAP.PMRWBM`; exact-phrase check for `persistence domain` returned no match.
4. NVM Express, `NVM Express Specification Archives`: <https://nvmexpress.org/nvm-express-specification-archives/>. Used only to control revision provenance and locate official ratified PDFs.

---

## Case status

**`grounded`**

The central vocabulary and mechanism are directly stated in the 2013 SNIA primary specification, the failure/atomicity limits are explicit, the later NVMe comparison uses official ratified specifications, and the negative terminology claim is carefully bounded to the revisions actually inspected.