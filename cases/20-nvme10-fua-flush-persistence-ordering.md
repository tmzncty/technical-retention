# NVM Express 1.0 Volatile Write Cache and FUA: Completion, Media Persistence, and Power-Fail Atomicity

## Scope

- **Bounded period:** 2011.
- **Primary source:** **_NVM Express Revision 1.0_**, ratified 1 March 2011, official NVM Express-hosted Gold PDF.
- **Research question:** how does an early NVMe host/controller contract separate ordinary command completion, volatile-cache state, explicit flushing, per-command nonvolatile-media commitment, command ordering, and atomicity during power failure?

This is **not** a general history of NVMe, PCIe SSDs, filesystems, `fsync`, controller firmware, or later NVMe persistence-domain terminology. Case 15 already grounds a concrete ATA/Intel SSD power-loss-protection mechanism. This case begins at a different layer:

> **What did the 2011 NVMe 1.0 interface itself require the host and controller to distinguish when software wanted a write to outlive volatile staging or a power transition?**

The source is unusually useful because it states several negative boundaries directly: a controller need not order independent commands for the host; FUA does not imply ordering with other commands; normal-operation and power-fail atomic-write units may differ; and a cache can be treated as nonvolatile by the interface when the controller guarantees its contents will reach nonvolatile media on power loss.

---

## Historical vocabulary

The 2011 specification itself uses:

- `Volatile Write Cache (VWC)`;
- `Volatile Write Cache Enable (WCE)`;
- `Flush`;
- `Force Unit Access (FUA)`;
- `non-volatile media` / `non-volatile memory`;
- `command completion`;
- `Submission Queue` and `Completion Queue`;
- `Atomic Write Unit Normal (AWUN)`;
- `Atomic Write Unit Power Fail (AWUPF)`;
- `power fail condition`.

The following are **project engineering terms**, not claims about 2011 NVMe vocabulary:

- `durability boundary`;
- `per-command persistence guarantee`;
- `persistence ordering`;
- `power-fail atomicity regime`;
- `interface recovery guarantee`;
- `retention handoff`.

This case deliberately does **not** call the bounded 2011 mechanism a `persistence domain`. Later NVMe specifications use richer persistence terminology, but importing that terminology into Revision 1.0 would erase the historical interface boundary this case is meant to inspect.

---

## Historical record

### H/P — Revision 1.0 is a ratified 2011 interface specification

The official Gold PDF identifies itself as **NVM Express Revision 1.0** and states that it was ratified on **1 March 2011**. Its stated scope is the register interface and standard command set used by host software to communicate with an NVM subsystem. The document also says the interface sits above technology-specific NVM management such as NAND wear leveling and does not specify caching algorithms.

That scope matters methodologically: this source can ground **host/controller contract semantics**, but not the physical design of a particular SSD cache, capacitor bank, firmware journal, or FTL.

**Primary anchors:** Revision 1.0, printed pp. 2 and 8, especially §§1.1–1.3.

### H/P — a controller can explicitly report the presence of a volatile write cache

The Identify Controller data structure contains **Volatile Write Cache (VWC)**. Bit 0 indicates whether a volatile write cache is present. If present, the host may issue Flush commands and control the cache through Set Features using the Volatile Write Cache feature identifier.

The same table separately reports:

- **Atomic Write Unit Normal (AWUN)** — atomic write size during normal operation;
- **Atomic Write Unit Power Fail (AWUPF)** — atomic write size during a power-fail condition.

Thus the 2011 interface makes cache volatility and power-failure atomicity explicit host-visible properties rather than silently assuming them from the phrase `non-volatile memory`.

**Primary anchor:** Identify Controller data structure, printed p. 70, fields 525 and 527:526 / 529:528.

### H/P — interface `volatile` is partly defined by a power-loss guarantee, not merely by physical substrate

The Volatile Write Cache feature contains a critical note:

> if a controller can guarantee that data present in a write cache are written to nonvolatile media when power is lost, that write cache is **considered non-volatile** for this feature and the VWC setting does not apply to it.

This is not evidence that physically volatile memory has become intrinsically nonvolatile. It is evidence about the **interface classification**: for this feature, a cache with a guaranteed power-loss handoff is treated differently from a cache whose contents may be lost.

**Primary anchor:** §5.12.1.6 `Volatile Write Cache (Feature Identifier 06h)`, printed p. 79.

### H/P — Flush is a separate volatile-storage → nonvolatile-memory operation

Revision 1.0 §6.7 states that the **Flush** command is used by the host to indicate that data in volatile storage should be flushed to nonvolatile memory. The section then defines command completion through the normal I/O Completion Queue status mechanism.

The bounded historical claim is intentionally narrow. The 1.0 wording establishes a distinct flush operation and its volatile/nonvolatile target relation. This case does **not** silently import later-revision wording about every prior completed command or later persistence-domain definitions.

**Primary anchor:** §6.7 `Flush command`, printed p. 93.

### H/P — Write FUA ties one write's completion to nonvolatile-media commitment

For the Write command, bit 30 of Command Dword 12 is **Force Unit Access (FUA)**. The specification states that with FUA, the data must be written to **non-volatile media before indicating command completion**.

It then immediately adds:

> **There is no implied ordering with other commands.**

This is unusually clean period-primary evidence that two properties which are often casually merged are distinct:

```text
this write is on nonvolatile media before its completion
        ≠
this write is ordered for persistence relative to every other command
```

**Primary anchor:** Write command, Figure 128, printed p. 97.

### H/P — the controller is not the general ordering authority for independent commands

Section 6.3, `Command Ordering Requirements and Atomic Write Unit`, says that except for fused operations each command is independent and that if commands have ordering requirements, **host software or the associated application is required to enforce that ordering above the level of the controller**.

The same section states that the controller's normal atomic write unit may differ from its power-fail atomic write unit. Later controller-architecture text also permits command processing/reordering and does not impose a simple received-order rule for commitment to the NVM medium.

The specification separately requires that after a write has completed, later-completing reads of that location return the data from that write rather than an older value. Thus **read-visible currentness after completion** is constrained even though a general cross-command persistence order is not supplied automatically.

**Primary anchors:** §6.3, printed p. 88; controller command-processing discussion around printed p. 100.

---

## Retained state

This case requires several states/relations to remain distinct.

### 1. Host-visible logical block state

The host addresses logical blocks through namespace/LBA semantics. A completed write changes what subsequent reads of the same location may return under the specification's currentness rule.

### 2. Data in a volatile write cache

When VWC is present and enabled, the interface explicitly recognizes a state that may be in controller-side volatile storage rather than yet committed to nonvolatile media.

### 3. Nonvolatile-media representation

Flush and Write FUA both name a transition or guarantee involving nonvolatile memory/media. The specification defines this at the interface level and does not require one particular NAND/SCM technology or internal placement algorithm.

### 4. Ordering relation among commands

Ordering is not reducible to the persistence of either payload. If the application requires command A to become ordered before command B, the 1.0 controller does not generally invent that ordering on its behalf.

### 5. Atomicity capability under normal and failing power

AWUN and AWUPF are distinct reported capabilities. The property that a write is atomic under ordinary power does not by itself establish the same atomic unit during power failure.

---

## Retention mechanism

### Volatile-cache path

When a volatile write cache is present, the device can hold current write state in a layer whose continued survival is not automatically equivalent to nonvolatile-media residency.

### Flush path

The host can issue a separate Flush operation to request that volatile-storage data be moved to nonvolatile memory.

### FUA path

The host can mark a particular Write so that its payload must be on nonvolatile media before completion of **that command**.

### Power-loss-guaranteed cache path

The Volatile Write Cache feature note allows a different implementation relation: if the controller guarantees that cached data reach nonvolatile media on power loss, the interface treats that write cache as nonvolatile for this feature.

The specification does not prescribe how the guarantee is achieved. Capacitors, batteries, inherently nonvolatile cache memory, firmware sequencing, or other mechanisms must be sourced separately for a named implementation.

---

## Addressing and access geometry

The host uses namespace and logical-block addressing. This case stays above the internal FTL geometry that Case 04 analyzes.

The important address-related relation is instead **scope of the persistence command**:

- Flush refers to volatile storage as a cache/state class rather than selecting one LBA in the way a normal write does;
- FUA is attached to an individual Read/Write command and its addressed range;
- ordering requirements among several commands remain an additional relation that host software/application must establish.

So `same LBA`, `same command`, `same cache`, and `same ordered persistence sequence` are different units of analysis.

---

## Read / write / flush semantics

### Ordinary command completion

Revision 1.0 defines a command as completed when the controller finishes processing it, updates status, and posts the completion entry. The mere generic definition of completion is **not itself** a statement that all ordinary writes have reached nonvolatile media.

The specification provides separate mechanisms precisely for stronger statements: VWC disclosure/control, Flush, and FUA.

This case therefore uses the conservative formulation:

> **generic command completion should not be silently upgraded into a nonvolatile-media persistence guarantee unless the applicable command/feature contract establishes that guarantee.**

### FUA Write

FUA explicitly requires the addressed write data to reach nonvolatile media before completion, but provides no implied ordering with other commands.

### Flush

Flush explicitly asks the controller to move volatile-storage data to nonvolatile memory. It is a different control shape from FUA: it is not simply another spelling of a per-write FUA bit.

### Read currentness

After a write completes, later-completing reads for that location must return that write's data rather than an older value. This constrains what can answer as current, but it still does not create an operation history or a general durable ordering among unrelated commands.

---

## Time and ordering

This case adds several different temporal relations:

- command submission;
- controller processing/reordering;
- command completion posting;
- residence in volatile cache;
- explicit Flush completion;
- FUA write commitment before that command's completion;
- application-enforced ordering among commands;
- power-fail transition and the separately reported AWUPF atomicity regime.

The key result is that **later** is not one thing. A command can finish later than another without the specification thereby giving the application every persistence-order relation it might need. Likewise a state can be visible as current to a later read while the relevant crash/power-failure guarantee still depends on which persistence controls were used.

---

## Maintenance and labor

The standard moves retention work across an interface rather than eliminating it:

- the controller may maintain and drain a write cache;
- firmware/hardware must implement whatever guarantee is advertised;
- the host driver or higher-level software must issue Flush or FUA where its persistence contract requires them;
- software/application layers must enforce inter-command ordering when needed;
- controller designers must define/report normal versus power-fail atomicity;
- conformance testing remains necessary to distinguish a written contract from an implementation that actually survives faults.

Revision 1.0 does not provide evidence for the human labor, capacitor maintenance, firmware journal, or media-management design of a particular product. Those belong to named implementation cases.

---

## Failure / forgetting modes

Distinct failure surfaces include:

- loss of data that remains only in a volatile cache when the relevant power-loss guarantee is absent;
- omission of a Flush/FUA operation required by the host's higher-level persistence semantics;
- assuming FUA orders unrelated commands when Revision 1.0 explicitly says it does not;
- assuming normal-operation atomicity applies unchanged during power failure when AWUPF is separately reported;
- a controller violating the interface semantics it advertises;
- successful media commitment of individual writes while a higher-level filesystem/database ordering invariant is still wrong;
- later media/controller failure after a successful persistence transition, which is a different retention regime.

These failures should not all be called `data loss`. Some are payload-loss failures, some are ordering failures, some are atomicity failures, and some are contract/compliance failures.

---

## Engineering reconstruction

### E — command completion ≠ nonvolatile-media commitment by default

The specification's generic completion mechanism is broader than its explicit FUA media-before-completion guarantee. VWC and Flush also expose a state in which volatile and nonvolatile residency are distinct. Therefore an analysis that equates every completion with media persistence discards distinctions the 2011 interface itself exposes.

### E — per-command persistence ≠ cross-command ordering

FUA is the strongest primary-source counterexample in this case: it couples nonvolatile-media residency to one command's completion while explicitly refusing to imply ordering with other commands.

### E — interface volatility class ≠ simple physical-substrate class

For VWC purposes, a cache whose contents are guaranteed to reach nonvolatile media on power loss is considered nonvolatile. This is a **contract/recovery classification**. It must not be rewritten as a claim that physically volatile cells became intrinsically nonvolatile.

### E — normal atomicity ≠ power-fail atomicity

AWUN and AWUPF make power-fail behavior a separate reported capability. An application cannot infer one from the other without checking the controller's advertised relation.

### E — current visibility ≠ persistence order

A later-completing read must see a completed write at that location, while §6.3 still makes higher-level ordering the host/application's responsibility. `Which value may answer now?` and `In what durable order do several updates become safe?` are different questions.

---

## Functional analogies

### A — Case 15, Intel SSD 320 power-loss protection

Case 15 grounds a **named implementation path**: volatile buffers, power-fail detection, stored capacitor energy, prioritized firmware work, and NAND transfer. Case 20 grounds a **standard interface contract**.

Their relationship is functional, not identity:

```text
NVMe interface guarantee / control
        ≠
Intel SSD 320 physical PLP mechanism
```

Revision 1.0's VWC note is intentionally implementation-agnostic. It does not imply that every qualifying controller uses the SSD 320's capacitance design.

### A — Case 16, BSD FFS soft updates

Case 16 shows that a filesystem can require a relational durability closure across payload and metadata. Case 20 shows lower-layer commands that can establish device persistence and ordering relations.

Neither layer substitutes for the other:

```text
filesystem crash-admissibility / fsync relation
        ≠
NVMe Flush/FUA device contract
```

A higher layer must compose its own ordering/consistency requirements with the lower layer's persistence semantics.

### A — Case 04, mapped Flash

Case 04 asks which physical embodiment currently realizes a logical Flash block. Case 20 asks whether an interface-visible write has crossed a volatile/nonvolatile boundary and whether its ordering/atomicity properties are sufficient for a failure model. Mapping currentness and command persistence are therefore complementary but non-identical relations.

---

## Philosophical interpretation

### I — persistence can be a typed promise rather than a substrate adjective

This case disciplines a common intuition about `nonvolatile storage`: the medium category alone does not tell us what a completed host operation promises. In Revision 1.0, continued availability after a power transition is articulated through features and command semantics — VWC, Flush, FUA, and power-fail atomicity — not simply through the noun `NVM`.

The philosophical use should remain bounded. This does **not** prove that persistence is merely linguistic or contractual: the guarantee still depends on actual controller/media behavior. It shows instead that at a software/hardware boundary, what counts as retained is partly specified by an operational contract whose physical realization lies below the interface.

---

## Claim ledger

| Claim | Type | Evidence / limit |
| --- | --- | --- |
| NVMe 1.0 was ratified 1 March 2011 | H/P | official Gold PDF, printed p. 2 |
| VWC reports whether a volatile write cache is present | H/P | Identify Controller, printed p. 70 |
| AWUN and AWUPF separately report normal and power-fail atomic write units | H/P | Identify Controller p. 70; §6.3 p. 88 |
| a cache guaranteed to drain to nonvolatile media on power loss is considered nonvolatile for VWC | H/P | §5.12.1.6, printed p. 79 |
| Flush requests volatile-storage data be flushed to nonvolatile memory | H/P | §6.7, printed p. 93 |
| Write FUA requires media commitment before that command's completion | H/P | Figure 128, printed p. 97 |
| FUA implies no ordering with other commands | H/P | Figure 128, printed p. 97 |
| general inter-command ordering is a host/application responsibility | H/P | §6.3, printed p. 88 |
| command completion, media persistence, ordering, and power-fail atomicity must be compared separately | E | reconstruction from the independently specified interface relations above |
| NVMe 1.0 specifies a physical PLP design | X | rejected; implementation lies below the interface and must be sourced separately |
| NVMe invented Flush/FUA | X | not claimed; Case 15 already grounds ATA Flush semantics before 2011, and this slice does not attempt a full SCSI/ATA invention genealogy |
| 2011 NVMe uses modern `persistence domain` vocabulary | X | rejected for this bounded case unless separately sourced from the 1.0 text |

---

## Prior-art and related-repository boundary

Case 15 already places ATA8-ACS `FLUSH CACHE` standards-development text in 2007, before NVMe Revision 1.0. Therefore this case makes **no invention-priority claim for Flush** and treats NVMe's contribution here as the bounded semantics of its 2011 interface.

A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `NVM Express`, `NVMe`, `volatile write cache`, `FUA`, and `Flush` found no existing dedicated treatment at the time of this slice. No generic NVMe history is duplicated here; any later engineering chronology should be routed there if it grows beyond the retention comparison.

---

## Primary source

- NVMHCI Workgroup / NVM Express, **_NVM Express Revision 1.0_**, ratified 1 March 2011, official Gold PDF: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_0-Gold.pdf>.
  - printed p. 2 — ratification/date;
  - printed pp. 8–9 — scope and abstraction boundary;
  - printed p. 70 — VWC, AWUN, AWUPF;
  - printed p. 79 — VWC feature and power-loss-guaranteed-cache note;
  - printed p. 88 — ordering requirements and normal/power-fail atomicity distinction;
  - printed p. 93 — Flush command;
  - printed p. 97 — Write FUA and explicit no-ordering clause;
  - printed p. 100 — controller processing/reordering boundary.

Grounding details and direct facsimile checks are recorded in [`../evidence/20-nvme10-2011-flush-fua-grounding.md`](../evidence/20-nvme10-2011-flush-fua-grounding.md).

---

## Status

**`grounded`** for the bounded 2011 NVMe 1.0 interface-semantics question.

The status does **not** mean that later NVMe persistence-domain terminology, controller-specific cache topology, product fault compliance, filesystem composition, or NVMe-over-Fabrics persistence semantics are closed. They remain separate regimes.