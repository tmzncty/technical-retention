# Intel ADR/eADR: Moving the Power-Fail Protected Domain Upstream

## Scope

- **Object / system:** Intel persistent-memory platform semantics around ADR and eADR.
- **Bounded period:** 2016–2021, with a 2019 Intel implementation-oriented corroborating source.
- **Primary question:** how can volatile state in a processor/memory path count as power-fail protected before it physically resides in persistent memory, and what changes when the protected boundary expands from memory-controller queues to processor caches?

This is not a general history of NVDIMMs, Intel Optane persistent memory, PMDK, DAX, cache-coherence protocols, power supplies, or persistent-memory programming. It is a bounded platform bridge chosen because Case 31 deliberately left **ADR/eADR as a concrete persistence-domain implementation** open.

The central result is:

> **On the sourced Intel platforms, persistence is not reducible to “the bytes are already in the final nonvolatile DIMM.” ADR makes memory-controller write-pending queues power-fail protected by guaranteeing a failure-triggered drain; eADR extends that protected relation upstream into processor caches. Expanding the domain changes software cache-flush obligations, but it does not erase ordering/fencing requirements or the platform-energy assumptions that make the emergency transfer possible.**

The source boundary is equally important. The Intel documents ground behavior for the power-failure/shutdown regimes they describe. They do not license a universal claim about every reset, software crash, media failure, corruption event, or non-Intel platform.

---

## Historical vocabulary

The Intel sources themselves use:

- `persistence domain`;
- `Power-fail Protected Domain or Persistent Domain`;
- `ADR` / `Asynchronous DRAM Refresh`;
- `eADR` / `Enhanced - Asynchronous DRAM Refresh`;
- `Write Pending Queue (WPQ)`;
- `CLWB`;
- `CLFLUSHOPT`;
- `CLFLUSH`;
- `PCOMMIT`;
- `SFENCE`;
- `power-fail` / `power failure`;
- `processor caches`;
- `stored energy`.

The following are **project engineering terms**, not Intel historical vocabulary:

- `domain expansion`;
- `protected volatile state`;
- `future-transfer durability`;
- `software persistence obligation`;
- `persistence-path relocation`;
- `failure-triggered retention work`.

The acronym `ADR` must also not be normalized into ordinary DRAM self-refresh. In this bounded Intel persistence-memory context, the sourced behavior is a platform power-fail signal followed by flushing memory-subsystem write-pending queues. That is historically and operationally distinct from Case 21's recurring SDRAM `SELF REFRESH` mode.

---

## Historical record

### H/P — Intel defined persistence as a point along a store path, not simply a media label

Intel's 12 September 2016 article **“Deprecating the PCOMMIT Instruction”** defines the `persistence domain` as the portion of a platform data path where stores are power-fail safe. Its glossary similarly defines the `Power-fail Protected Domain or Persistent Domain` as the point along the path where a store is considered persistent.

This is a historical vocabulary claim from Intel, not a project paraphrase of SNIA Case 31.

**Primary anchor:** Intel, _Deprecating the PCOMMIT Instruction_, updated 2016-09-12, “Enabling Persistent Memory Programming” and glossary.

### H/P — a normal store can stop first in processor caches

The same 2016 Intel account describes a `MOV` store as typically ending in CPU caches. `CLWB`, `CLFLUSHOPT`, or related instructions can move modified state out of those caches toward memory. After cache writeback, the store may still spend time in a memory-controller `Write Pending Queue (WPQ)` before reaching the persistent-memory DIMM.

The source therefore exposes at least this path:

```text
MOV store
    ↓
processor cache
    ↓  CLWB / CLFLUSHOPT / CLFLUSH class operation
memory-controller WPQ
    ↓
persistent-memory DIMM
```

**Primary anchor:** Intel 2016 article, store-path discussion and glossary.

### H/P — ADR makes the WPQ part of the power-fail-safe persistence relation

Intel describes ADR as a platform-level feature in which the power supply signals that power failure is imminent and the memory-subsystem write-pending queues are flushed. On a platform that automatically drains the WPQ during power-fail or shutdown, Intel's larger dashed persistence-domain boundary includes that queue.

This was the reason Intel could deprecate `PCOMMIT`: on platforms planned to support the Intel persistent-memory DIMM, ADR was planned as a required platform feature, so software no longer needed an additional application-visible instruction to force the WPQ into the DIMM.

**Primary anchor:** Intel 2016 article, store-path discussion, “The Simpler Programming Model,” and glossary.

### H/P — 2019 Intel documentation ties Optane DC persistent-memory platforms to ADR

A 25 July 2019 Intel article on persistent memory and SPDK states that platforms supporting Intel Optane DC persistent memory are required to support ADR. It describes ADR as guaranteeing data persistence during power-fail or shutdown by automatically flushing the memory-controller WPQ, eliminating the need for `PCOMMIT`.

This is useful corroboration that the 2016 programming-model simplification was not merely an abandoned proposal.

**Primary anchor:** Intel, _Enabling Persistent Memory in the Storage Performance Development Kit (SPDK)_, updated 2019-07-25, “Committing to Persistence.”

### H/P — ADR does not include processor caches

Intel's 19 June 2020 third-generation Xeon technical overview states that ADR protects data at the memory-subsystem level and **does not flush processor caches**. The same document says applications therefore need cache-flush operations such as `CLWB`, `CLFLUSH`, `CLFLUSHOPT`, non-temporal stores, or `WBINVD` when operating under the ordinary ADR path.

The table in that document lists the first-generation Intel Optane persistent-memory family with `ADR` and the 200-series generation with `ADR, eADR (Optional)` for data persistence during a power-failure event.

**Primary anchor:** Intel, _Third Generation Intel Xeon Processor Scalable Family Technical Overview_, updated 2020-06-19, Table 2 and “Enhanced - Asynchronous DRAM Refresh (eADR).”

### H/P — eADR extends power-fail protection into processor caches

The same Intel overview says eADR extends protection from the memory subsystem to the processor caches during power failure. Its described sequence uses an NMI routine to flush processor caches and then an ADR event to carry the state through the memory subsystem.

Intel further states that PMDK can detect eADR and, when it is present, applications using PMDK do not need to perform the cache flush operations otherwise required for ADR.

**Primary anchor:** Intel 2020 technical overview, eADR section.

### H/P — eADR does not eliminate all software persistence ordering

Intel explicitly states that `SFENCE` is **still required** under eADR for persistence of globally visible stores. Therefore the source itself prevents the inference that extending the protected domain into the processor caches makes every persistence-related software operation disappear.

**Primary anchor:** Intel 2020 technical overview, eADR section.

### H/P — eADR depends on additional platform stored energy

Intel states that eADR requires the OEM to provide additional stored energy, for example a backup battery, specifically to allow this functionality.

This makes the platform's energy reserve part of the documented power-fail-protection path, without making that energy itself payload state.

**Primary anchor:** Intel 2020 technical overview, eADR section.

---

## Retained state

This bounded case concerns several different state classes.

### 1. Intended persistent payload

The application ultimately wants modified bytes to remain available after the sourced power-failure event.

### 2. Processor-cache copies

A recently executed store may exist in modified cache lines before those lines have been written toward memory. Under ADR these lines remain outside the sourced protected domain; under eADR the platform protection extends to them.

### 3. Memory-controller WPQ entries

Under the sourced ADR regime, entries that have reached the memory-controller write-pending queue are included in a failure-triggered drain relation that is intended to carry them into persistent memory.

### 4. Ordering / visibility relation

Intel retains a distinct `SFENCE` requirement even under eADR. The intended persistent result therefore depends not only on which physical buffers are power-fail protected but also on whether software has established the required ordering/visibility relation.

### 5. Platform capability state

PMDK detects whether eADR is present and changes its flush behavior accordingly. Platform capability therefore participates in deciding which persistence work software must still perform.

### 6. Stored energy reserve

The OEM's additional stored energy is not application data. It is nevertheless retention infrastructure because the sourced eADR mechanism relies on it to complete failure-triggered draining work after normal power begins to disappear.

---

## Physical / logical substrate

The relevant path spans several physically different layers:

```text
processor cache hierarchy
        ↓
memory-controller write-pending queues
        ↓
Intel persistent-memory DIMM
```

The crucial point is that Intel's `persistence domain` is a **platform relation across this path**, not the name of one storage cell.

With ADR, the sourced boundary includes the memory-controller queue but excludes processor caches. With eADR, the protected relation expands upstream into processor caches.

That difference can exist even when the final persistent-memory medium remains the same broad class of device.

---

## Retention mechanism

### ADR path

The bounded ADR sequence is approximately:

```text
application store
    ↓
modified line may remain in processor cache
    ↓  software cache writeback / flush
memory-controller WPQ
    ↓  power-fail/shutdown signal + ADR drain
persistent-memory DIMM
```

The software obligation is therefore to move relevant dirty cache state at least into the ADR-protected portion of the path and establish the required ordering.

### eADR path

The bounded eADR sequence is approximately:

```text
application store
    ↓
modified line may remain in processor cache
    ↓  power-fail event
platform/NMI-assisted processor-cache flush
    ↓
ADR memory-subsystem drain
    ↓
persistent-memory DIMM
```

When the platform reports eADR, PMDK can omit the ordinary cache-flush instructions that are necessary under ADR. Intel nevertheless retains `SFENCE`, and the platform must have enough stored energy to carry out the promised drain.

The state can therefore count as protected before its final transfer has occurred **because the platform guarantees a specific future transfer under the sourced failure event**.

That final sentence is an engineering reconstruction of Intel's documented mechanism, not Intel's own philosophical formulation.

---

## Addressing and access geometry

This case is a direct load/store persistent-memory path rather than a queued block-I/O path.

The software-visible designation can be simplified as:

```text
application virtual address
→ cache-coherent processor/memory path
→ persistent-memory physical range
```

Persistence qualification overlays a second relation:

```text
where is the latest modified copy now?
    +
which parts of that path are covered by the platform's power-fail drain guarantee?
    +
what ordering/flush obligations remain for software?
```

The same persistent-memory address can therefore have a different durability path depending on whether the platform exposes ADR alone or eADR.

---

## Read semantics

Ordinary read behavior is not the central bounded question here. The critical issue is the **write-side survival path** before a later read after power restoration can retrieve the intended value.

This case does not claim that eADR makes all processor architectural state persistent. Intel specifically discusses processor **caches**, not registers, execution pipelines, operating-system state, or arbitrary machine state.

---

## Write semantics

### Store execution

Executing the store changes program-visible cache-coherent state but does not by itself establish that the update has reached the ADR-protected WPQ on an ADR-only system.

### Cache writeback under ADR

`CLWB`, `CLFLUSHOPT`, `CLFLUSH`, or other documented paths move modified state out of processor caches toward the memory subsystem. This is a different operation from the failure-triggered ADR drain of the WPQ.

### eADR protection

With eADR, processor-cache contents participate in the platform's power-fail protection path. Intel says PMDK can omit explicit flush operations when eADR is detected.

### Fence

`SFENCE` remains required in Intel's eADR description. Domain expansion therefore changes one persistence obligation without collapsing all ordering semantics into the hardware failure path.

---

## Time

This case distinguishes at least these times:

- the time a CPU store executes;
- the time a modified cache line becomes globally visible in the relevant ordering relation;
- the time software explicitly writes a line back under ADR;
- the time the line enters a memory-controller WPQ;
- the time a power-fail condition is detected;
- the time cache/WPQ emergency draining begins;
- the time the protected volatile state reaches the persistent-memory DIMM;
- the later restart/recovery time.

Under ADR/eADR, the moment at which a state becomes **power-fail protected** need not equal the later moment at which the final media transfer finishes.

---

## Maintenance, energy, and labor

The durability promise is distributed across:

- application/library selection of persistence primitives;
- cache-coherence and cache-writeback machinery;
- memory-controller WPQ behavior;
- platform firmware/NMI handling in the eADR description;
- power-failure signaling;
- ADR drain logic;
- PMDK feature detection;
- OEM provision of sufficient stored energy;
- persistent-memory media.

This is a direct example of retention work crossing traditional `software`, `CPU`, `memory controller`, `power`, and `media` boundaries.

---

## Failure / forgetting modes

Distinct bounded failure modes include:

- treating a cache-resident ADR-only update as persistent before software has moved it into the protected memory-subsystem path;
- omitting a required `SFENCE` because eADR is mistaken for a universal ordering/transaction guarantee;
- assuming eADR is present when the platform does not expose/support it;
- failure of the platform/OEM energy assumptions needed to complete the emergency drain;
- a failure outside the sourced power-fail/shutdown model;
- media corruption or device failure after the transfer, which ADR/eADR does not by itself solve;
- confusing persistence with application-level atomicity, logging, or transaction consistency;
- treating Intel's `ADR` acronym as evidence of ordinary SDRAM self-refresh semantics.

---

## Engineering reconstruction

### E — persistence-domain membership ≠ physical nonvolatile-media residency

Under ADR, a store in the WPQ can be inside Intel's power-fail-safe persistence domain even though the final transfer to the DIMM occurs later during the failure-handling path. Under eADR the same logic extends farther upstream into processor caches.

### E — persistent qualification can depend on guaranteed future transfer work

The platform can classify volatile intermediate state as protected because power-fail signaling, stored energy, and drain logic promise to move it to persistent memory before energy is exhausted. Persistence here is partly a guarantee over a future failure-triggered operation.

### E — domain expansion can change software obligations without changing the final medium

ADR leaves processor caches outside the protected region, requiring cache-line writeback. eADR brings those caches into the protected path, allowing PMDK to omit that flush work when the feature is detected.

### E — domain expansion ≠ elimination of ordering

Intel explicitly retains `SFENCE` under eADR. Enlarging the set of protected physical locations does not automatically establish every ordering relation required by persistent software.

### E — power-fail protection ≠ universal failure survivability

The sources ground power-failure behavior and, for ADR, shutdown behavior. They do not establish survival of every reset, CPU fault, firmware error, media corruption, software bug, or transaction failure.

### E — platform capability can be constitutive of the persistence contract

PMDK's behavior depends on detection of eADR. The persistence algorithm is therefore conditional on retained/discoverable platform capability rather than fixed solely by the memory module.

### E — stored energy ≠ payload, while stored energy can be retention infrastructure

The eADR source explicitly requires OEM stored energy. That energy carries no user bytes, but without the promised energy reserve the failure-triggered transfer path described by Intel would not have the same guarantee.

---

## Functional analogies

### A — Case 31, SNIA persistence domain

Case 31 grounds a 2013 cross-platform programming-model concept: durability is established relative to a persistence domain and recoverability depends on the domain's design/configuration and tolerated failure pattern.

Case 32 supplies a concrete Intel platform realization in which that boundary can sit after processor caches (ADR) or extend to include them (eADR).

The relationship is a useful implementation comparison, not proof that every SNIA persistence domain is ADR/eADR.

### A — Case 15, Intel SSD 320 power-loss protection

Both cases use stored energy and failure-triggered transfer work.

But Case 15 is a controller-internal SSD path moving volatile controller/buffer state toward NAND. Case 32 is a platform memory path spanning processor caches, a memory-controller WPQ, and persistent memory. The similarity is functional, not protocol or hardware identity.

### A — Cases 20 and 30, NVMe

NVMe Case 20 uses queued namespace commands, Flush/FUA, and interface atomicity properties. NVMe Case 30 uses a PCIe Persistent Memory Region and PMR-specific barriers/readiness/restore-health state.

ADR/eADR should not be renamed as either mechanism. This case concerns the Intel CPU/memory-controller/persistent-memory load/store path.

### A — Case 21, SDRAM self refresh

Case 21's `SELF REFRESH` is a DRAM retention mode in which the device internally performs recurring refresh while ordinary service is suspended.

Intel ADR/eADR uses `Asynchronous DRAM Refresh` as a historical platform feature name in a power-fail persistence path. The shared word `refresh` does not make the mechanisms equivalent.

---

## Philosophical pressure — bounded

The case creates a useful conceptual pressure point:

> A technical system may call a state `persistent` even while the currently embodying bits are still in a physically volatile cache or queue, provided the platform has a sufficiently specified power-fail transfer guarantee.

That does not prove that persistence is “immaterial” or merely contractual. The guarantee depends on material cache state, controller logic, signal paths, persistent media, and stored energy. The case instead sharpens a narrower point: **technical persistence can be relational and prospective**, depending on what the system is guaranteed to do when a particular failure arrives.

This is a project interpretation, not Intel's historical philosophical claim.

---

## Counterexamples and limits

- eADR is documented as **optional** for the sourced Intel Optane persistent-memory 200-series platform; do not generalize it to every Intel system.
- The Intel sources discuss processor caches, not all processor architectural state.
- `SFENCE` remains required in the sourced eADR model; do not equate eADR with transaction durability.
- The failure envelope is bounded to the sourced power-failure/shutdown behavior; reset, media failure, corruption, firmware defects, and empirical energy-margin compliance require independent evidence.
- This case does not establish first use or invention priority for `persistence domain`, ADR, or battery/capacitor-backed persistence. Case 31 already provides an earlier SNIA terminology anchor for `persistence domain`.
- The 2016 Intel article describes planned support and PCOMMIT deprecation; the 2019 and 2020 Intel sources provide later implementation/platform corroboration.
- A platform specification/feature description is not empirical fault-injection proof that every product/configuration meets the claimed boundary.

---

## Related-repository check

`tmzncty/computing-archaeology` was searched for a dedicated `eADR` / ADR persistent-memory treatment and no obvious matching case was found through the available repository search.

This is not proof that no incidental mention exists. A broad history of NVDIMM-N, Optane, CPU cache-flush ISA evolution, platform power-fail architecture, and persistent-memory hardware belongs primarily in `computing-archaeology` if developed. This repository keeps the bounded retention comparison: **where the power-fail-protected boundary sits, what volatile state it includes, and how that changes software obligations.**

---

## Claim ledger

| Claim | Layer | Evidence status |
| --- | --- | --- |
| Intel used `persistence domain` / `Power-fail Protected Domain or Persistent Domain` language in 2016 | H/P | strong Intel first-party source |
| ADR drains memory-subsystem WPQs on imminent power failure | H/P | strong Intel first-party source, corroborated in 2019/2020 |
| ADR leaves processor caches outside the protected path | H/P | strong 2020 Intel platform source |
| eADR extends power-fail protection into processor caches | H/P | strong 2020 Intel platform source |
| PMDK can omit explicit cache flushes when it detects eADR | H/P | strong 2020 Intel platform source |
| `SFENCE` remains required under the sourced eADR model | H/P | strong 2020 Intel platform source |
| eADR requires additional OEM stored energy | H/P | strong 2020 Intel platform source |
| persistence-domain membership can precede final media residency | E | direct reconstruction from sourced ADR/eADR drain path |
| protected volatile state can depend on guaranteed future transfer work | E | direct reconstruction from power-fail signal + drain + energy relation |
| ADR/eADR are equivalent to NVMe Flush/FUA/PMR | X | rejected; different interfaces and historical mechanisms |
| Intel ADR is the same mechanism as SDRAM self refresh | X | rejected; shared terminology does not establish mechanism identity |
| eADR makes every machine state persistent or crash-atomic | X | rejected; source is narrower and retains SFENCE |
| Intel invented `persistence domain` | X | rejected; Case 31 already grounds SNIA use by 2013 and this case makes no priority claim |

---

## Sources

### Primary / first-party technical sources

1. Intel, **“Deprecating the PCOMMIT Instruction,”** ID 659301, updated 12 September 2016.  
   <https://www.intel.com/content/www/us/en/developer/articles/technical/deprecate-pcommit-instruction.html>

2. Intel, **“Enabling Persistent Memory in the Storage Performance Development Kit (SPDK),”** ID 659394, updated 25 July 2019.  
   <https://www.intel.com/content/www/us/en/developer/articles/technical/enabling-persistent-memory-in-the-storage-performance-development-kit-spdk.html>

3. Intel, **“Third Generation Intel Xeon Processor Scalable Family Technical Overview,”** ID 672628, updated 19 June 2020.  
   <https://www.intel.com/content/www/us/en/developer/articles/technical/intel-xeon-processor-scalable-family-overview.html>

4. Intel, **“Third Generation Intel Xeon Processor Scalable Family On Two Socket Platform Technical Overview,”** ID 660365, updated 21 March 2021.  
   <https://www.intel.com/content/www/us/en/developer/articles/technical/third-generation-xeon-scalable-family-overview.html>

The 2020 and 2021 Intel pages independently preserve the same core ADR/eADR distinction. This case uses the dated first-party pages as historical/platform evidence rather than relying on a living glossary alone.

---

## Status

**`grounded`**

The bounded promotion is justified because the central platform behavior is documented by multiple dated Intel first-party sources across 2016–2021, the ADR/eADR boundary is explicit, eADR optionality and remaining `SFENCE`/stored-energy obligations are directly stated, cross-case vocabulary is controlled, and failure claims are kept inside the sourced power-fail envelope.

Future work should not simply extend this case indefinitely. Separate slices are preferable for empirical fault qualification, non-Intel persistence domains, FastADR/RPMEM, CPU-ISA flush/fence genealogy, or filesystem/database composition.