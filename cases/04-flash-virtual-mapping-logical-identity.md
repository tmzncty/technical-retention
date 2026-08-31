# Flash Virtual Mapping: Logical Identity Without Physical Location

## Scope

- **Bounded primary system:** Amir Ban / M-Systems, U.S. Patent 5,404,485, **“Flash file system,”** filed 8 March 1993 and issued 4 April 1995.
- **Earlier device context:** Fujio Masuoka et al., 1987 IEDM NAND-structure Flash EEPROM paper, used only to establish the emergence of dense NAND-structured nonvolatile Flash—not to project later SSD controller behavior backward into that device paper.
- **Later boundary evidence:** ONFI 2.1 and a Samsung SSD technical white paper, used to show that program/erase endurance and page-write/block-erase asymmetry remain explicit engineering constraints in later NAND systems.
- **Why this case matters for technical retention:** it is the first case in this repository where the identity presented to the user or operating system can remain stable **while the physical location embodying that identity changes deliberately**.

This is **not** a general history of Flash memory, NAND, SSDs, wear leveling, TRIM, secure erase, or modern Flash Translation Layers. `computing-archaeology` already identifies ROM → PROM → EPROM → EEPROM → Flash and SSD/FTL history as technical bridges that should be built there.

The narrower question here is:

> What kind of persistence is it when a logical address can continue to name “the same” retained data even though rewriting that data means writing somewhere else, invalidating the old location, and later reclaiming physical space by copying and erasing?

---

## Historical vocabulary

The 1993-filed Ban patent does **not** organize its account around the later umbrella term `Flash Translation Layer`.

Its own vocabulary includes:

- `flash memory`;
- `physical address space`;
- `virtual address space`;
- `virtual map`;
- `logical unit` and `logical unit number`;
- `block`;
- `unit` and `zone`;
- `transfer unit`;
- block states such as `free and writable`, `deleted and not writable`, and `allocated and contains user data`;
- `block erase before write` as the underlying constraint.

Modern terms such as **FTL**, **garbage collection**, **out-of-place update**, **write amplification**, **wear leveling**, **TRIM**, and **over-provisioning** may be useful for later comparison, but they should not silently replace the patent's own terminology.

In this case, `out-of-place update` is used as an engineering description of a documented operation: changed data are written to an unwritten physical block and the mapping is changed so the original virtual identity now resolves to the new physical location.

`Garbage collection` is used only as a **functional analogy** to later SSD practice. The patent itself speaks of transferring active blocks and periodically reclaiming physical memory space.

---

## Historical record

### H/P — NAND Flash entered the record as a high-density nonvolatile memory structure before this mapping case

Masuoka, Momodomi, Iwata, and Shirota's 1987 IEDM paper, **“New ultra high density EPROM and Flash EEPROM with NAND structure cell,”** proposed a NAND-structured cell to reduce area per bit and described it as applicable to high-density nonvolatile EPROM and Flash EEPROM.

For this repository, the paper matters mainly as a historical boundary:

- dense NAND-structured Flash is not a later SSD invention;
- the device-level nonvolatile medium predates the controller-mapping problem examined below;
- the 1987 paper should not be made to “contain” later FTL semantics that it did not discuss.

**Primary bibliographic anchor:** F. Masuoka, M. Momodomi, Y. Iwata, R. Shirota, IEDM Technical Digest 1987, pp. 552–555, DOI `10.1109/IEDM.1987.191485`.

### H/P — Ban's patent begins from block erase-before-write, not from an abstract disk model

U.S. Patent 5,404,485 was filed by Amir Ban for M-Systems Flash Disk Pioneers Ltd. on 8 March 1993.

Its background describes Flash as nonvolatile and electrically erasable, but emphasizes a constraint that prevents it from behaving like ordinary rewritable random-access storage: a previously written area generally cannot simply be written again without erasing a larger region first.

The patent's stated goal is therefore not merely to store bits. It is to make this constrained medium **appear to an existing computer operating system as a storage device in which arbitrary locations can be read and written**.

That distinction is central to `technical-retention`:

```text
physical medium semantics
    block erase before rewrite

presented logical semantics
    stable-looking rewritable address space
```

The gap between the two is filled by mapping and maintenance.

**Primary anchor:** US 5,404,485, `Background of the invention` and `Summary of the invention`; Google Patents transcription lines 243–259.

### H/P — A rewrite moves the data and preserves the virtual identity by changing the map

The patent defines a virtual address space and a physical address space connected by a `virtual map`.

When a write targets a virtual address whose current physical block has already been written, the controller does not simply overwrite the same location. It finds an **unwritten block**, writes the new data there, and changes the map so that the original virtual address now resolves to the new physical block.

The old physical block is marked unusable / deleted and remains unavailable for rewriting until the larger erase unit containing it is erased.

The patent later makes the identity/location separation explicit at the unit level: because data move physically during transfer, a **logical unit number remains unchanged even when the physical location of that unit changes**.

That is unusually strong primary evidence for this project's central question. The source itself distinguishes an address/identity intended to remain stable from a physical location expected to change.

**Primary anchors:**

- US 5,404,485, description lines 253–261;
- FIGS. 4–6 discussion, lines 299–310;
- claim 1, especially the steps that write to an unwritten block and update the virtual map, lines 334–367.

### H/P — “Deleted” is a mapping/allocation status before it is a physical erase

The block-allocation map in the patent includes a status explicitly described as **“block deleted and not writable.”**

During a rewrite, the old block is changed to deleted while the replacement block becomes written and the virtual map is updated to point to the replacement.

Crucially, the source then describes physical reclamation as a later operation:

1. select a unit;
2. read its still-active blocks;
3. write those active blocks into the reserved transfer unit;
4. erase the original unit as a larger physical region;
5. update the logical-to-physical map.

Thus, within this bounded system:

> **logical invalidation precedes physical erasure.**

The old block can cease to be the current logical object while its physical region has not yet undergone the later erase operation.

This is not a claim that every historical or modern Flash implementation preserves recoverable stale data for a specific duration. It is a narrower claim about the documented semantics of this system: the state `deleted` and the physical operation `erased` are distinct events.

**Primary anchors:** US 5,404,485, allocation-map and transfer description, lines 295–314; claims 1 and 4.

### H/P — Reclamation copies current state before destroying the old erase unit

The patent reserves an unwritten `TRANSFER UNIT` so active data can survive reclamation of a unit containing deleted/unusable blocks.

Its transfer procedure reads active blocks from the selected unit, writes them to the transfer unit, erases the selected unit, then changes the map so the physical roles of the units have effectively changed while the logical unit number remains stable.

This means physical erasure is not simply “delete the old thing.” It is a compound maintenance operation that first **extracts the still-current state from a mixed region**, recreates it elsewhere, and only then destroys the old erase unit.

Retention therefore depends on coordinated destruction and recreation.

### H/P — The map is itself retained state

The mapping layer is not an abstract mathematical convenience. It is state that must survive or be reconstructed.

The patent discusses storing most of the virtual map in nonvolatile Flash while keeping a smaller secondary map in volatile RAM. It then explains how the volatile secondary map can be reconstructed at startup by scanning block-usage information retained in Flash.

This gives the case a second retention layer:

```text
user data
    retained in Flash blocks

identity metadata
    retained in maps / headers / usage state
```

The physical bits holding user data are insufficient by themselves to provide the logical storage service. The system also needs retained metadata that tells later operations **which physical block currently counts as the value of a virtual address**.

**Primary anchor:** US 5,404,485, map-storage and reconstruction discussion, lines 315–328.

### H/P — Later NAND standards expose finite program/erase endurance as part of the interface

The Open NAND Flash Interface (ONFI) 2.1 specification defines a parameter-page field for **block endurance** as the maximum number of program/erase cycles for the addressable page/block, and states that the value assumes at least the minimum ECC correctability reported by the device.

This should not be projected backward into Ban's exact 1993 implementation. It is later primary standards evidence that Flash persistence cannot be described only as “nonvolatile.” Rewriting and erasing consume a finite device-level endurance budget, and error correction is part of the contract by which later NAND remains usable.

**Primary anchor:** ONFI 2.1, §5.6.1.21, bytes 105–106, `Block endurance`.

### H/S — A later SSD vendor description shows the same asymmetry at page/block scale

A Samsung SSD technical white paper describes a later NAND/SSD regime in which host writes occur at finer granularity while erasure occurs in blocks. It explains that valid pages are migrated so blocks dominated by invalid pages can be erased and returned to the free pool.

This is **not** evidence that Ban's transfer-unit algorithm is identical to a modern Samsung SSD controller. It is boundary evidence that the underlying retention problem persists in a later engineering form:

- overwritten logical state migrates;
- old physical state becomes invalid;
- free erase units must be recreated;
- maintenance itself causes additional physical writes.

---

## Retained state

This case has at least three distinct retained states.

### 1. Device-level physical state

Flash cells retain electrical state without continuous power.

At this layer, `nonvolatile` is meaningful.

### 2. Current user-data state

A logical block or virtual address has a current value.

That value may move from one physical region to another during rewriting or transfer.

### 3. Mapping / allocation state

Metadata establishes:

- which physical block currently embodies a virtual address;
- which blocks are free;
- which are deleted / unusable;
- which logical unit number corresponds to which physical unit.

For this case, the retained user object is therefore not adequately described as:

> data bits sitting in one Flash block.

A better bounded description is:

> **data + a retained mapping relation that identifies which physical embodiment currently counts.**

---

## Physical / logical substrate

The bounded patent intentionally abstracts over exact Flash-cell physics. It assumes block-erasable nonvolatile Flash and builds a controller / mapping architecture above it.

The relevant substrate is therefore layered:

```text
nonvolatile Flash cells / erase regions
        +
block allocation metadata
        +
virtual -> logical -> physical mapping
        +
controller procedures
```

This is the first case in the repository where `substrate` clearly cannot be equated with a single fixed material location.

The logical retained object is distributed across data-bearing cells and identity-bearing metadata.

---

## Retention mechanism

The retention mechanism also has layers.

### Quiescent physical retention

Flash cell state can remain without continuous power.

### Logical retention through remapping

When the value at a virtual address is rewritten, continuity is maintained by making the **same virtual address** resolve to a new physical block.

### Retention through reclamation

When an erase unit contains a mixture of active and deleted blocks, active blocks are copied to reserved space before the old unit is erased.

Thus some current state survives precisely because the system recreates it elsewhere before destroying the region in which an earlier embodiment lived.

### Retention through metadata

The mapping and block-status information must itself survive or be reconstructible so the system can recover logical identity after restart.

The resulting persistence is not well described by a single adjective such as `nonvolatile`.

It is:

> **nonvolatile physical state + metadata-governed identity + relocation and reclamation procedures.**

---

## Addressing and access geometry

Addressing is the heart of this case.

The patent explicitly separates:

- computer-generated / virtual address;
- logical unit address;
- physical Flash address.

A two-stage translation can preserve logical unit identity even as physical placement changes.

This is a major contrast with earlier cases:

```text
abacus
    state is tied closely to a visible spatial position

delay line
    state is tied to a recurring temporal slot

magnetic core
    logical cell is tied closely to one selected core

DRAM
    logical cell remains associated with one selected storage site while charge is regenerated

mapped Flash
    logical identity can intentionally survive a change of physical location
```

The map turns **location** into an implementation detail rather than an identity criterion.

---

## Read semantics

In the bounded patent, a read resolves the virtual address through the map to the current physical block and reads that block.

The case does not yet attempt to cover NAND read disturb, read-retry, retention drift, ECC decoding, or modern controller recovery.

Those are later source-deepening opportunities.

The main read-semantic point here is relational:

> reading the “same” virtual address at two different times may read from different physical locations while the system presents continuity of logical identity.

---

## Write semantics

A write to an already-written logical location is implemented as an **out-of-place update** in the bounded system:

1. locate an unwritten physical block;
2. write the new data there;
3. change allocation status;
4. update the map so the original virtual address resolves to the new location;
5. leave the old physical block in a deleted / unusable state until later reclamation.

The important retention fact is:

> a rewrite can preserve an address-level identity by **not** preserving physical location.

This reverses a common intuition inherited from paper files, magnetic core, or a simple disk-sector mental model in which the retained object's identity seems naturally tied to “where it is.”

---

## Erasure and deletion semantics

This case requires a controlled separation.

### Logical deletion / invalidation

A block can be marked deleted and cease to be the block mapped as current user data.

### Physical erasure

A larger erase unit later undergoes the Flash erase operation that returns its locations to unwritten/free state.

Therefore:

```text
no longer logically current
    !=
physically erased now
```

This distinction is one of the most important contributions of the case.

It should not be exaggerated into a universal forensic claim. Whether stale cell state remains recoverable, for how long, and by what technique depends on the Flash technology, controller, erase history, encryption, ECC, and device generation.

The source-controlled result is narrower and stronger:

> the architecture itself treats logical invalidation and physical erase as separate operations.

---

## Time

Mapped Flash introduces several timescales not present in the previous four cases.

### Nonvolatile retention interval

The cell state is intended to survive power removal for a much longer interval than DRAM charge.

### Update interval

Logical state may change at host/application timescales.

### Reclamation interval

Old invalid physical locations need not be erased immediately after each logical update. Reclamation can be deferred until the system selects an erase unit for transfer / erase.

### Endurance lifetime

Later NAND interfaces explicitly report finite program/erase endurance. Physical rewriting therefore has a cumulative lifetime cost even though individual retained states are nonvolatile.

The case therefore adds a new temporal pattern:

> **maintenance can be deferred until space and erase constraints make it necessary.**

This is neither continuous maintenance, access-triggered restore, nor deadline-driven refresh.

It is closer to **capacity-pressure / reclaim-triggered maintenance**.

That term remains provisional until more Flash and SSD cases test it.

---

## Maintenance and labor

A Flash device can appear wonderfully passive while powered off, but a rewritable storage service above it requires continuing controller work.

In the bounded system that work includes:

- maintaining virtual/logical/physical maps;
- maintaining block allocation state;
- locating unwritten blocks;
- changing mappings during updates;
- reserving transfer space;
- copying still-active blocks out of a unit selected for erasure;
- erasing the old unit;
- reconstructing volatile mapping state after startup.

Later SSDs add much more:

- ECC;
- bad-block management;
- wear leveling;
- garbage collection;
- read-retry and refresh strategies;
- power-loss recovery;
- over-provisioning;
- host deallocation interfaces.

Those later features are **not** silently attributed to the 1993 patent.

The narrower lesson is already sufficient:

> nonvolatile cells do not make a maintenance-free rewritable storage system.

---

## Failure / forgetting modes

This case adds new, mechanism-specific failure modes.

### Loss of mapping while physical bits survive

If data remain physically present but the metadata that identifies their current virtual address is lost or inconsistent, the system can lose **logical availability without immediate material destruction**.

This is an engineering reconstruction from the patent's dependence on maps; the patent's startup-reconstruction procedure is itself evidence that mapping state is operationally necessary.

### Logical invalidation without physical erasure

A block can become deleted / unusable in the allocation system before its erase unit is physically erased.

### Reclamation failure

If active data are not successfully preserved before erase, reclaiming physical space can destroy current logical state.

This is a mechanistic consequence of the documented transfer-before-erase sequence, not a claim about a particular observed historical failure incident.

### Endurance exhaustion

Later ONFI NAND explicitly exposes finite program/erase endurance. A medium can remain nonvolatile yet lose its ability to support indefinite rewriting.

### Loss of free / reclaimable space

A log-structured or out-of-place update regime depends on unwritten space and reclamation. Free space is therefore not merely unused capacity; it is part of the maintenance machinery that allows logical persistence under repeated change.

---

## Engineering reconstruction

### E — Identity persistence no longer requires location persistence

The patent deliberately keeps logical unit identity stable while data move physically.

For this case:

```text
same logical object
    does not mean
same physical block
```

This is stronger than the earlier observation that a delay-line pulse or DRAM charge can be physically regenerated. Here, the system can move the retained state to a **different addressable physical region** and preserve continuity through metadata.

### E — Retention becomes relational

The current state of a virtual address is not determined solely by inspecting every physical block and choosing the most intact bit pattern.

It is determined by a relation maintained in maps and allocation state.

The object is retained partly by retaining the rule:

> **this physical embodiment is the one that currently counts.**

### E — Deletion can be semantic before it is material

The patent's `deleted and not writable` status makes a block cease to count as current before the later unit erase.

This gives `technical forgetting` a new mechanism:

> a system can forget by withdrawing reference / currentness before destroying the old physical embodiment.

### E — Reclamation is preservation-through-destruction

To reclaim an erase unit, current blocks are first copied out, then the old unit is erased.

Persistence is therefore maintained by a cycle that intentionally combines:

```text
selection of what still counts
        ->
re-creation elsewhere
        ->
destruction of the old mixed region
```

### E — Free space is retention infrastructure

The reserved transfer unit is not merely empty capacity. It is what makes relocation-before-erasure possible.

This suggests a useful cross-system question for later SSD and distributed-storage cases:

> how much apparently “unused” capacity is actually required to keep a changing retained state safely maintainable?

---

## Philosophical / media-theoretical interpretation

### I — Continuity can be a rule of identification rather than persistence of one carrier

The philosophical pressure point is exact and technical:

- the physical location changes;
- the virtual/logical identity remains;
- mapping metadata decides which embodiment counts as current.

This makes Flash mapping a strong case for separating:

- persistence of matter;
- persistence of signal;
- persistence of location;
- persistence of logical identity.

The case should not yet be generalized into a theory that “all identity is metadata.” It shows only that one storage architecture deliberately constructs continuity this way.

### I — Forgetting can precede destruction

A logically deleted block may still await physical erase.

That mechanism can later be brought into dialogue with Kirschenbaum's attention to digital erasure and forensic materiality. For now the technical result comes first:

> the system's declaration that a block no longer counts and the medium's physical erasure operation are distinct.

### I — Availability depends on hidden identity-maintenance

A host sees a stable addressable object. The controller sustains that appearance by mapping, relocating, reclaiming, and reconstructing metadata.

This may later sharpen discussions of technical availability, but it should **not** be equated directly with Heidegger's `Bestand`.

Likewise, this machine-operational mapping layer should not automatically be called Stieglerian tertiary retention.

---

## Functional analogies and limits

### A — Flash Translation Layer

The patent is clearly relevant to the historical development of Flash address translation, and its virtual-to-physical mapping performs a function later associated with FTLs.

But this case does **not** claim:

- that US 5,404,485 defines every later FTL;
- that modern SSD mapping granularity matches the patent's units/blocks;
- that modern NAND garbage collection is algorithmically identical to its transfer-unit procedure.

`FTL-like` is acceptable as a bounded functional description; `the modern SSD FTL is exactly this patent` is not.

### A — Copy-on-write

The update sequence resembles copy-on-write in the limited sense that changed state is written to a new location before the reference is switched.

But this is not a claim of genealogy or identical crash-consistency semantics.

### Limit — Flash is not one erase geometry

The patent intentionally generalizes across block-erasable Flash. NAND page/program and block-erase geometry, NOR erase sectors, device-specific partial-program rules, bad-block handling, and modern 3D NAND differ substantially.

### Limit — “Deleted” does not mean forensically recoverable

The architecture proves only a separation between allocation invalidation and physical erase. It does not by itself establish practical stale-data recovery on any particular device.

### Limit — Wear leveling is not established here

Finite program/erase endurance is established by later NAND standards, but this case does not yet source a historical wear-leveling algorithm or show that Ban's transfer-unit policy equalizes wear.

### Limit — Host deallocation is a later layer

TRIM / DEALLOCATE / dataset-management semantics are not covered here. A future case should distinguish:

- file deletion;
- host deallocation command;
- controller invalidation;
- garbage collection;
- media erase;
- crypto-erase.

---

## Cross-case result

Cases 00–04 now expose five importantly different ways in which a later operation can encounter “the same” retained state:

```text
abacus
    same visible position

mercury delay line
    same logical pattern through recurrent signal regeneration

magnetic core
    same logical value through remanence and, after destructive read, restoration

DRAM
    same logical value through bounded charge survival + scheduled regeneration

mapped Flash
    same logical address / object while the physical storage location changes
```

The new result is:

> **retained identity can migrate while remaining current.**

The case also adds a distinct form of technical forgetting:

> **logical invalidation can occur before physical erasure.**

And a distinct maintenance trigger:

> **space/rewrite constraints can create deferred reclamation work even when the retained medium is nonvolatile.**

These are engineering conclusions. Their philosophical significance should be tested only after more mapped-storage and distributed-storage cases are grounded.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Masuoka et al. published a NAND-structure Flash EEPROM proposal at IEDM 1987 | H/P | bibliographic record + DOI / abstract |
| Ban filed `Flash file system` for M-Systems on 8 March 1993 | H/P | exact patent metadata |
| The patent begins from a block erase-before-rewrite constraint | H/P | patent background |
| Rewriting an already-written virtual address can place new data in an unwritten physical block and update the map | H/P | patent description + claim 1 |
| The patent keeps logical unit identity stable while unit data move to a new physical location | H/P | FIG. 3–4 discussion |
| A block can be marked deleted before its containing erase unit is physically erased | H/P | allocation-map + transfer procedure |
| Reclamation preserves active blocks by copying them before erasing the old unit | H/P | FIGS. 7–8 discussion + claim 1 |
| Mapping metadata is itself retained / reconstructed system state | H/P/E | patent map-storage and startup-reconstruction discussion |
| Later ONFI NAND reports finite program/erase endurance and ECC requirements | H/P | ONFI 2.1 parameter-page specification |
| Stable logical identity can therefore survive deliberate physical relocation | E | direct reconstruction from mapping mechanism |
| Logical deletion is identical to physical erasure | X | contradicted by bounded patent sequence |
| US 5,404,485 is identical to every modern SSD FTL | X | explicitly unsupported |
| Flash mapping is automatically equivalent to Stieglerian tertiary retention or Heideggerian `Bestand` | X | explicitly unsupported |

---

## Related repositories

### `tmzncty/computing-archaeology`

The memory track currently covers early memory, tape, disk, and HBM, while its audit explicitly identifies the semiconductor-memory and storage-geometry middle as unfinished. A complete history of Flash cells, NAND, SSD controllers, FTL algorithms, wear leveling, ECC, and host interfaces belongs primarily there.

Relevant entry points:

- <https://github.com/tmzncty/computing-archaeology/tree/main/docs/memory>
- <https://github.com/tmzncty/computing-archaeology/blob/main/AUDIT.md>

This case should reuse that future work rather than become a duplicate SSD encyclopedia.

### `tmzncty/problem-history`

The anti-anachronism rule is especially useful here. `FTL`, `garbage collection`, and `copy-on-write` are later / cross-domain organizing terms. The 1993 patent's own vocabulary—`virtual map`, `transfer unit`, `deleted`, `unwritten`, `physical address`—must remain visible.

---

## Sources

### Primary

1. Amir Ban, **“Flash file system,”** U.S. Patent 5,404,485, filed 8 March 1993, issued 4 April 1995, original assignee M-Systems Flash Disk Pioneers Ltd. Google Patents: <https://patents.google.com/patent/US5404485A/en>.
   - metadata: filing and issue dates;
   - `Background of the invention`: block erase-before-write constraint;
   - `Summary of the invention`: virtual / physical mapping;
   - FIGS. 3–6: logical unit identity, address translation, out-of-place update;
   - FIGS. 7–8: transfer and reclamation;
   - FIG. 9: map-in-Flash and startup reconstruction;
   - claim 1: unwritten-block write, remap, transfer, erase, remap sequence.
2. Fujio Masuoka, Masaki Momodomi, Yoshihisa Iwata, Riichiro Shirota, **“New ultra high density EPROM and Flash EEPROM with NAND structure cell,”** *Technical Digest — International Electron Devices Meeting*, 1987, pp. 552–555. DOI: <https://doi.org/10.1109/IEDM.1987.191485>.
3. Open NAND Flash Interface Working Group, **Open NAND Flash Interface Specification 2.1**, especially §5.6.1.21 `Block endurance`: <https://onfi.org/files/onfi_2_1_gold.pdf>.

### Later vendor boundary / engineering context

4. Samsung Electronics, **“Over-Provisioning White Paper,”** 2019. Vendor explanation of page write / block erase asymmetry, migration of valid pages, garbage collection, and reserved free space: <https://download.semiconductor.samsung.com/resources/white-paper/S190311-SAMSUNG-Memory-Over-Provisioning-White-paper.pdf>.

## Evidence gaps before `grounded`

- inspect the official patent PDF directly and record printed page / figure / column anchors rather than relying only on HTML transcription;
- obtain and inspect the full 1987 Masuoka IEDM paper rather than relying on bibliographic abstract text;
- add an early manufacturer Flash / NAND datasheet that documents concrete page/program/block-erase semantics and endurance;
- add a primary historical source that explicitly uses `Flash Translation Layer` terminology, so the vocabulary transition from Ban's `virtual map` to later FTL can be dated rather than inferred;
- add a bounded early wear-leveling source instead of assuming reclamation equals wear leveling;
- treat TRIM / deallocation / secure erase as a separate later case with standards-level evidence;
- add power-failure / atomicity evidence before making claims about mapping-update crash consistency.