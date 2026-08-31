# Technical Spine

This is a **provisional research map**, not a teleological story of inevitable progress.

The sequence below is organized by changes in what `retention` technically requires, not by a claim that each stage naturally evolves into the next.

## 0. Retained position before electronic computing

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

### Caution

Terms such as `register`, `memory`, and `state` are often modern reconstructions here. Historical vocabulary must be recovered separately.

---

## 1. Retention as moving or circulating process

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

### Existing technical evidence

See the memory track in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology/tree/main/docs/memory), especially its treatments of delay lines and drums.

---

## 2. Retention as unstable state plus restoration

### Candidate cases

- Williams-Kilburn tube;
- dynamic semiconductor memory;
- destructive-read memories.

### Core problem

The retained state is not simply durable. Persistence is produced by **periodic recovery and rewriting**.

### Questions

- At what point does repair become constitutive of persistence rather than an exceptional maintenance event?
- Is the `same bit` still the same retained state after repeated restoration?
- What temporal assumptions are hidden by a stable address interface?

---

## 3. Remanence and nonvolatile physical state

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

---

## 4. Semiconductor hierarchy: not one memory but many temporal regimes

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

### Existing gap to coordinate

[`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) already identifies SRAM / DRAM / ROM / EEPROM / Flash / cache / ECC as an important historical middle to deepen. Technical history should primarily be built there and reused here.

---

## 5. Geometry hidden behind logical addresses

### Candidate cases

- HDD tracks / heads / cylinders / sectors;
- bad-sector remapping;
- CHS → LBA;
- controller caches;
- SSD Flash Translation Layers;
- wear leveling;
- garbage collection;
- TRIM;
- ECC and scrubbing.

### Core problem

A logical address can appear stable while the physical place holding its content changes.

This is a major transition in the ontology of the retained object:

> persistence of identity no longer requires persistence of location.

### Questions

- What exactly remains invariant across remapping?
- How much hidden maintenance is needed to sustain the fiction of stable blocks?
- What does deletion mean when logical invalidation and physical erasure are separated?

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

### Questions

- Where is the retained object?
- What makes replicas count as one object?
- How much disagreement can exist before the object is no longer well-defined?
- Is repair a background operation or part of the definition of persistence?
- Can `durability` be probabilistic rather than absolute?

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

---

## Cross-cutting comparison axes

Every stage should eventually be mapped against:

- volatility;
- retention time;
- refresh / maintenance;
- destructive versus nondestructive read;
- overwrite versus erase-before-write;
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
- deletion semantics;
- migration;
- labor and infrastructure.

The goal is not a winner's timeline. It is a history of **different ways of making a past state available to a future operation**.
