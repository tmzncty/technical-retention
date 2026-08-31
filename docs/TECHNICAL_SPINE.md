# Technical Spine

This is a **provisional research map**, not a teleological story of inevitable progress.

The sequence below is organized by changes in what `retention` technically requires, not by a claim that each stage naturally evolves into the next.

## 0. Retained position before electronic computing

### First case

- [`Abacus as Retained Position`](../cases/00-abacus-retained-position.md) — **first-pass**.

The first case already sharpens several distinctions that should remain visible throughout the repository:

- a retained state can be operational without being archival;
- `state retention` is not `history retention`;
- physical persistence is insufficient if the interpretation or procedural context is lost;
- selection, interpretation, protection, validation, and reset can be human labor before they become machine functions;
- `register-like` is acceptable only as a bounded functional analogy, not as historical vocabulary or genealogy.

### Candidate cases

- tally marks and durable inscription;
- counting boards and abaci;
- mechanical counters;
- geared calculators;
- Babbage's `Store`;
- punched cards as persistent symbolic configuration.

### Questions

- When is retained position part of a calculation rather than merely a record of it?
- What makes an intermediate state stable enough to be resumed?
- What is the difference between a human-readable mark and a machine-operational state?
- When does a retained configuration become directly actionable by machinery?
- When does `working retention` become too broad a category to remain useful?
- What additional mechanism is required to preserve not only the current state but the history that produced it?

### Caution

Terms such as `register`, `memory`, and `state` are often modern reconstructions here. Historical vocabulary must be recovered separately.

---

## 1. Retention as moving or circulating process

### First case

- [`Mercury Delay-Line Memory: Retention as Circulation`](../cases/01-mercury-delay-line-circulation.md) — **first-pass**.

### Candidate cases

- acoustic / mercury delay-line memory;
- serial recirculating memories;
- magnetic drum timing-aware storage.

### Core problem

A retained state may persist **because it keeps moving**.

This is an important challenge to the intuitive picture of storage as a thing sitting still somewhere.

### Questions

- Is storage a spatial location, a recurring temporal position, or both?
- How does waiting become address geometry?
- What work is necessary to keep circulation stable?
- Does a recirculating memory retain only current state, or can its circulation itself expose a temporal history?

### Existing technical evidence

See the memory track in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology/tree/main/docs/memory), especially its treatments of delay lines and drums.

---

## 2. Retention as unstable state plus restoration

### First cases

- [`Magnetic Core Memory: Retention at Rest, Destruction in Reading`](../cases/02-magnetic-core-destructive-read.md) — **first-pass** for access-triggered restoration;
- [`DRAM Refresh as Scheduled Restoration`](../cases/03-dram-refresh-as-scheduled-restoration.md) — **first-pass** for deadline-driven regeneration.

### Candidate cases

- Williams-Kilburn tube;
- dynamic semiconductor memory;
- destructive-read memories.

### Core problem

The retained state is not simply durable. Persistence may be produced by **recovery and rewriting** whose trigger depends on the mechanism.

The first cases already require at least two forms:

- access-triggered restore after destructive read;
- time-triggered regeneration before an unstable state crosses a physical deadline.

### Questions

- At what point does repair become constitutive of persistence rather than an exceptional maintenance event?
- Is the `same bit` still the same retained state after repeated restoration?
- What temporal assumptions are hidden by a stable address interface?
- Does restoration preserve identity, or repeatedly recreate an equivalent state?
- Should access-triggered restoration and periodic refresh remain separate controlled terms?

---

## 3. Remanence and nonvolatile physical state

### First case

- [`Magnetic Core Memory: Retention at Rest, Destruction in Reading`](../cases/02-magnetic-core-destructive-read.md) — **first-pass**.

### Candidate cases

- magnetic core;
- magnetic tape;
- magnetic disk;
- later nonvolatile magnetic memories.

### Core problem

A physical substrate can retain a distinction without continuous power, but access, addressing, control, and reliability may still require elaborate machinery.

### Questions

- What does `nonvolatile` hide?
- Which parts persist without power, and which metadata or control systems must survive for the retained state to be useful?
- How do sequential and random access change the meaning of `having` information?
- How does destructive read in core complicate the intuitive opposition between passive persistence and active maintenance?

---

## 4. Semiconductor hierarchy: not one memory but many temporal regimes

### First case

- [`DRAM Refresh as Scheduled Restoration`](../cases/03-dram-refresh-as-scheduled-restoration.md) — **first-pass**.

### Candidate cases

- latch / flip-flop;
- CPU registers;
- SRAM;
- cache;
- DRAM;
- ROM / PROM / EPROM / EEPROM;
- Flash.

### Core problem

Modern computers deliberately combine multiple retention mechanisms because no single substrate simultaneously optimizes latency, density, cost, energy, write endurance, and persistence.

### Questions

- How is `memory` divided into temporal tiers?
- What does the hierarchy ask software to forget about physical differences?
- Which retained states exist only for nanoseconds, milliseconds, process lifetimes, boot lifetimes, or years?
- Which levels retain only current state, and which systems add separate history-retention mechanisms such as logs or snapshots?
- How does a nonvolatile cell acquire new maintenance obligations once finite write/erase endurance and block erase geometry matter?

### Existing gap to coordinate

[`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) already identifies SRAM / DRAM / ROM / EEPROM / Flash / cache / ECC as an important historical middle to deepen. Technical history should primarily be built there and reused here.

---

## 5. Geometry hidden behind logical addresses

### First case

- [`Flash Virtual Mapping: Logical Identity Without Physical Location`](../cases/04-flash-virtual-mapping-logical-identity.md) — **first-pass**.

The bounded 1993 M-Systems patent establishes several points directly from period vocabulary:

- Flash rewrite is constrained by erase-before-write geometry;
- a virtual/logical address can remain current while its physical block changes;
- an old block can be marked `deleted` before the containing erase unit is physically erased;
- current blocks may be copied to a transfer unit before the old unit is erased;
- mapping/allocation metadata is itself retained state needed to recover current identity.

This is the first case where **identity persistence is intentionally separated from location persistence** by an address-translation layer.

### Candidate cases

- HDD tracks / heads / cylinders / sectors;
- bad-sector remapping;
- CHS → LBA;
- controller caches;
- SSD Flash Translation Layers;
- wear leveling;
- garbage collection;
- TRIM / deallocation;
- ECC and scrubbing.

### Core problem

A logical address can appear stable while the physical place holding its content changes.

This is a major transition in the ontology of the retained object:

> persistence of identity no longer requires persistence of location.

The first mapped-Flash case adds a second statement:

> currentness can be changed by metadata before the old physical embodiment is erased.

### Questions

- What exactly remains invariant across remapping?
- How much hidden maintenance is needed to sustain the fiction of stable blocks?
- What does deletion mean when logical invalidation and physical erasure are separated?
- Can a physical trace survive after the logical state has been declared forgotten?
- What metadata must survive for the system to know which embodiment currently counts?
- How much free / reserved capacity is actually retention infrastructure rather than unused space?
- When did `Flash Translation Layer` become the standard vocabulary for this family of mechanisms?
- How should wear leveling, reclamation, garbage collection, bad-block remapping, and host deallocation be distinguished historically rather than collapsed into `SSD maintenance`?

### Caution

Do not treat the 1993 Ban patent as identical to all later SSD FTLs. Its `virtual map`, `transfer unit`, block statuses, and two-level address translation are primary historical mechanisms. Later terms such as `FTL`, `garbage collection`, `TRIM`, and `over-provisioning` require their own source histories.

---

## 6. Virtual and software-defined retained state

### Candidate cases

- virtual memory and paging;
- files and inode/directory structures;
- journaling and crash consistency;
- copy-on-write;
- snapshots;
- database WAL and recovery;
- content-addressed storage;
- immutable logs.

### Core problem

Software introduces additional retention semantics that may be more important to users than the underlying medium.

### Questions

- What makes a state `committed`?
- When does a write count as having happened?
- How is past state reconstructed after interruption?
- How do logical histories coexist with destructive physical rewrites?
- At what point do logs, journals, snapshots, and version stores become explicit **history-retention** systems rather than merely state-retention systems?
- When metadata chooses which physical embodiment counts, is that already a software-defined retained object even below a filesystem?

---

## 7. Replicated and distributed retention

### Candidate cases

- RAID;
- replicated file systems;
- distributed object storage;
- quorum systems;
- erasure coding;
- consensus logs;
- geographically distributed archives;
- cloud object versioning and lifecycle policies.

### Core problem

A logical fact can persist even while every particular physical copy is replaceable.

Persistence becomes a property of **protocol + redundancy + repair + identity rules**, not simply a durable medium.

The mapped-Flash case provides a local precursor to one conceptual question: identity already survives relocation within one managed device. Distributed systems extend this by allowing multiple physical embodiments, disagreement, repair, and no permanently privileged copy.

### Questions

- Where is the retained object?
- What makes replicas count as one object?
- How much disagreement can exist before the object is no longer well-defined?
- Is repair a background operation or part of the definition of persistence?
- Can `durability` be probabilistic rather than absolute?
- Which distributed systems retain current consensus state, and which retain the history needed to reconstruct or audit it?
- Does the metadata/identity lesson from mapped Flash survive when the map itself is distributed and replicated?

---

## 8. Retention at infrastructure scale

### Candidate cases

- tape libraries;
- cold storage;
- data centers;
- environmental control;
- backup rotation;
- migration between generations of media;
- checksums and integrity scanning;
- long-term digital preservation;
- institutional retention policy.

### Core problem

Long-lived storage is often not a long-lived medium. It is a **migration regime**.

### Questions

- What survives when every physical carrier is eventually replaced?
- Which metadata, formats, software, keys, interfaces, organizations, and skills must also be retained?
- When is `preservation` really repeated re-creation?
- Can a bitstream survive while its interpretation becomes technically forgotten?
- When does scheduled migration resemble controller-level reclamation, and where does that analogy break because archival meaning and institutional responsibility enter?

---

## Cross-cutting comparison axes

Every stage should eventually be mapped against:

- volatility;
- retention time;
- refresh / maintenance;
- maintenance trigger: continuous, access-triggered, deadline-driven, capacity/reclaim-triggered, repair-triggered;
- destructive versus nondestructive read;
- overwrite versus erase-before-write;
- logical invalidation versus physical erasure;
- access geometry;
- latency;
- density;
- energy;
- endurance;
- error model;
- redundancy;
- address stability;
- location stability;
- identity semantics;
- mapping / metadata dependence;
- deletion semantics;
- state retention versus history retention;
- interpretation / context dependence;
- migration;
- labor and infrastructure.

The goal is not a winner's timeline. It is a history of **different ways of making a past state available to a future operation**.
