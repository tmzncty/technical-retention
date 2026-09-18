# Case 150 deepening — 2009–2012 over-provisioning as controller maintenance reserve

## Status

**`bounded deepening complete`**

## Scope

This packet deepens [`../cases/150-crucial-m550-active-garbage-collection.md`](../cases/150-crucial-m550-active-garbage-collection.md) around one narrow question:

> When an SSD has more physical NAND capacity than it exposes as host-visible logical capacity, what does that reserved capacity do for retention, reclamation, wear, and future write service?

The bounded historical window is **2009–2012**, with three primary-source anchors:

1. a **2009-priority Shalvi / Sommer / Kasorla adaptive-over-provisioning patent family**, later assigned through Anobit to Apple, which explicitly separates specified host-visible user capacity from a changeable over-provisioning overhead and links that overhead to garbage-collection efficiency, wear, throughput, ECC trade-offs, and reliability criteria;
2. a **2010-priority OCZ patent**, published in 2012, which explicitly models a `User Pool` and `OP Pool`, allows blocks to move between them, allows programmed / partially written blocks to belong to the OP pool, and returns an erased block to the OP pool after consolidation;
3. Intel's **2011 SSD 710 Series** product and High Endurance Technology briefs, which document a named shipping-product configuration in which `20 percent over-provisioning` is associated with higher endurance / random-write performance and where `extra spare area` is described as lowering write amplification alongside background refresh, wear leveling, NAND characterization, and program-state-disturb management.

This is **not** a history of the invention of SSD over-provisioning. It does not claim that these sources introduced the practice, that their controller designs are genealogically related, or that Crucial M550 firmware implemented any one of these mechanisms.

The purpose is narrower: establish from period primary evidence that **capacity hidden from the host can be operational maintenance infrastructure rather than merely unused space**, while preventing several common collapses:

```text
physical NAND capacity
    != host-visible logical capacity

host-visible free LBA space
    != controller-reserved over-provisioning capacity

over-provisioning-pool membership
    != erased / empty NAND state

reserved maintenance headroom
    != reclamation already completed
```

---

## Why this slice is needed

Case 150 already grounds:

- host-visible retirement / TRIM as distinct from physical reclamation;
- controller garbage collection as live-data preservation plus stale-embodiment retirement;
- powered idle as a maintenance opportunity rather than proof of maintenance completion;
- invalidity evidence, victim selection, live-data copying, mapping update, erase, and reusable capacity as separable stages.

What remained comparatively under-specified was the **capacity condition that makes those transformations easier or even feasible under sustained load**.

The repository's technical spine already asks:

> How much free / reserved capacity is actually retention infrastructure rather than unused space?

The sources here make that question historically concrete without pretending that one numerical over-provisioning ratio is universal.

---

## Source set and custody notes

### P1 — Shalvi / Sommer / Kasorla, adaptive over-provisioning

- **US8479080B1**, `Adaptive over-provisioning in memory systems`.
- Prior-art / priority date listed by Google Patents: **12 July 2009**.
- U.S. filing: **24 June 2010**.
- Publication / grant: **2 July 2013**.
- Inventors: Ofir Shalvi, Naftali Sommer, Yoav Kasorla.
- Assignment history visible in the public patent record includes assignment to **Anobit Technologies Ltd.** in 2010 and to **Apple Inc.** in 2012.
- Public transcription: <https://patents.google.com/patent/US8479080B1/en>.

Because the public U.S. publication occurred in 2013, this source is used as **2009-priority prior art**, not as evidence that the terminology was publicly circulating in 2009.

### P2 — OCZ, User Pool / OP Pool and internal consolidation

- **US20120117309A1**, `NAND flash-based solid state drive and method of operation`.
- Prior-art / priority date: **7 May 2010**.
- U.S. filing: **9 May 2011**.
- Publication: **10 May 2012**.
- Inventor: Franz Michael Schuette.
- Original assignee: **OCZ Technology Group, Inc.**
- Public transcription: <https://patents.google.com/patent/US20120117309A1/en>.

This is a patent disclosure, not proof that every OCZ product shipped with the exact claimed state machine.

### P3 — Intel SSD 710 Series product brief

- Intel Corporation, **`Intel Solid-State Drive 710 Series`**, Product Brief, copyright **2011**, document 325843-001US.
- Current Intel-hosted PDF: <https://www.intel.com/content/dam/doc/product-brief/ssd-710-series-brief.pdf>.

The directly inspected brief says the 300 GB SSD 710 can reach up to 1.5 PB 4 KB write endurance with **20 percent over-provisioning**, gives separate endurance rows for baseline and `20% Over-provisioning`, and gives random-write figures qualified by the same configuration.

### P4 — Intel SSD 710 High Endurance Technology brief

- Intel Corporation, **`High Endurance Technology in the Intel Solid-State Drive 710 Series`**, Technology Brief, copyright **2011**, document 325778-001US.
- Current Intel-hosted PDF mirror: <https://www.intel.co.jp/content/dam/www/public/us/en/documents/technology-briefs/ssd-710-series-het-brief.pdf>.

The directly inspected brief says HET aims to lower write amplification while increasing NAND P/E-cycle capability; separately lists background data refresh, wear leveling, NAND characterization / program-state-disturb management; and says the SSD has **extra spare area that lowers write amplification**. Its endurance table notes that the higher comparison values are based on **20% over-provisioning**.

These Intel documents are manufacturer-primary product literature. They support the documented configuration and claimed product relationship, not a universal law for all SSDs.

---

# Historical record

## H/P — over-provisioning was explicitly defined as a capacity relation, not merely “empty NAND”

The adaptive-over-provisioning patent states that a memory system can have an **actual physical storage capacity larger than the specified logical capacity available to a host**.

It then defines over-provisioning overhead in relation to memory areas that **do not hold valid data** and explains that the aggregate size of those areas can be maintained at or above a specified overhead.

The historical relation is therefore already more precise than:

```text
OP = some spare chips sitting empty
```

The disclosed abstraction is instead a relation among:

```text
physical storage locations
    -> current valid-data occupancy
    -> logical address range exposed to the host
    -> controller-maintained non-valid-data headroom
```

The same source explicitly says the controller may modify the number of physical locations involved in the mapping **without changing the predefined logical-address range / user capacity**.

So, in this source:

```text
fixed host-visible user capacity
    != fixed internal over-provisioning allocation
```

This is especially useful for `technical-retention`: the quantity of internal maintenance slack can change while the retained host-visible designation space remains stable.

## H/P — more over-provisioning was linked to more efficient compaction / garbage collection

The Shalvi / Sommer / Kasorla disclosure explains the ordinary Flash problem in period engineering terms:

- page updates are written to new physical locations;
- old physical locations cease to hold valid data;
- garbage collection compacts valid data from partially programmed blocks;
- increasing over-provisioning reduces the number of copy operations required per compaction / consolidation;
- the source states that garbage-collection efficiency increases with over-provisioning ratio and links increased over-provisioning to reduced cell wear and increased programming throughput.

The important bounded result is not that “more OP is always better.” It is that the source explicitly treats reserved non-valid-data capacity as a variable that changes the **cost and feasibility of future maintenance work**.

## H/P — over-provisioning could be traded against other reliability resources

The same patent does not present OP as the only reliability mechanism. Its adaptive scheme allows the controller to vary over-provisioning in response to criteria including:

- wear level / health;
- expected error level;
- desired storage reliability;
- workload-change frequency;
- programming-speed versus capacity preferences.

It also describes possible trade-offs between:

- over-provisioning and ECC redundancy;
- over-provisioning and bits-per-cell / programming density;
- over-provisioning and compression;
- over-provisioning assigned among memory portions with different expected endurance.

This is strong historical evidence against one-dimensional language such as:

```text
more reserved capacity = one universal reliability scalar
```

Instead, at least in this disclosure, reserved capacity participates in a controller-level resource-allocation problem alongside coding, density, wear, and workload.

## H/P — OCZ explicitly separated `User Pool` and `OP Pool`

The OCZ publication describes NAND blocks partitioned into two virtual address spaces:

- a **user-accessible pool**;
- an **over-provisioning pool**.

It says the controller can virtually assign blocks to either pool and **transition blocks between the two**.

This matters because it gives period vocabulary for a distinction that modern explanations often flatten into “extra capacity.” The source's OP pool is not simply a permanently fixed group of physically special cells.

At least in this disclosure:

```text
pool role
    is controller-assigned / transitionable
```

rather than necessarily being a permanent physical identity.

## H/P — an OP-pool block need not be erased or empty

This is the most useful counterexample in the packet.

The OCZ disclosure explicitly says:

- data may be written to pages of blocks assigned to either the User Pool or the OP Pool;
- partially written blocks may belong to either pool during consolidation;
- after valid pages are copied elsewhere, the source block is erased;
- the resulting erased block can then be cycled / assigned into the OP Pool to maintain OP-pool capacity.

Therefore:

```text
block is in OP Pool
    != block is necessarily erased now
    != block is necessarily empty now
```

The OP pool is a **controller role / address-space classification** in this design. Erased-block state is a separate physical / lifecycle condition.

This distinction prevents a recurring simplification in SSD discussions: “over-provisioned space” is not always a synonym for “a pile of erased blocks immediately ready for programming.”

## H/P — the OCZ disclosure allows internal reorganization without a host TRIM / erase command

The same source describes copying pages from one partially written block to another, then erasing the source block, **without requiring a TRIM or erase command from the host system**.

That does not make TRIM irrelevant. It demonstrates only that:

```text
host deallocation signal
    != sole possible trigger / prerequisite for every controller-local consolidation step
```

A controller may reorganize data for its own housekeeping / pool-capacity policy using its existing knowledge of which data are current or occupied.

## H/P — Intel documented a named shipping SSD configuration in which 20% over-provisioning changes product endurance / performance ratings

Intel's 2011 SSD 710 Product Brief presents baseline endurance ratings and separate `20% Over-provisioning` ratings.

For example, the 300 GB model's product spotlight gives:

- 4 KB endurance up to **1.1 PB** in the baseline row;
- up to **1.5 PB** in the `20% Over-provisioning` row;
- 8 KB endurance up to **1.8 PB** in the baseline row;
- up to **3.0 PB** in the `20% Over-provisioning` row.

The same brief qualifies random-write performance figures with the 20% over-provisioning configuration.

The point for this packet is not the exact benchmark magnitude. It is the product-level historical fact that Intel exposed **over-provisioning as an explicit configuration variable tied to endurance / performance claims**.

## H/P — Intel separately described `extra spare area` as lowering write amplification

Intel's HET technology brief first defines SSD endurance in JEDEC terms, including both written-data volume and end-of-life retention / error-rate criteria. It then explains write amplification as NAND writes exceeding host writes and says HET aims to reduce that overhead.

The brief separately identifies several system-level mechanisms:

- background data refresh;
- wear leveling;
- NAND characterization;
- program-state-disturb management;
- **extra spare area that lowers write amplification**.

The source says the combined effect helps meet the drive's endurance and retention requirements.

This source therefore supports a useful negative statement:

```text
spare area
    != background refresh
    != wear leveling
    != disturb management
```

They are co-operating mechanisms, not interchangeable names.

---

# Engineering reconstruction

## E — reserved capacity is a maintenance resource because relocation needs somewhere to land

Case 150 already establishes the generic GC sequence:

```text
mixed block
    -> preserve / relocate live pages
    -> retire stale embodiments
    -> erase source block
    -> regain reusable erase-block capacity
```

The present source set adds the capacity constraint beneath that sequence.

To relocate current data before erasing its old block, a controller needs **destination capacity that is admissible for new physical embodiments**. More available headroom can reduce how much still-live data must be shuffled merely to free one erase block.

Thus, for this bounded managed-Flash setting:

```text
maintenance headroom
    is not retained payload

but

maintenance headroom
    can be constitutive of the system's ability
    to preserve payload while replacing embodiments
```

This is why “unused” capacity can be retention infrastructure.

## E — four different meanings of “free” must remain separate

The combined Case 150 evidence now requires at least four different states:

```text
1. host-visible free logical address
2. trimmed / discardable logical range known to the device
3. controller-reserved / over-provisioned capacity
4. physically erased NAND pages / blocks ready for programming
```

None is safely substituted for another.

For example:

- an LBA may be free in the filesystem but the SSD may not yet know that;
- a trimmed LBA may no longer require old payload preservation while its old cells are not yet erased;
- an OP-pool block can contain live / occupied pages in the OCZ disclosure;
- an erased block may be allocated into the OP pool, but `erased` is a physical-state condition while `OP pool` is a controller-assignment condition.

So:

```text
logical freedom
    != discard authority
    != maintenance reserve
    != erased-media readiness
```

## E — over-provisioning is not proof that reclamation debt is zero

A drive can have reserved capacity while still having:

- mixed blocks;
- invalid pages awaiting consolidation;
- live pages that must be moved;
- erase work not yet performed;
- wear-balancing / refresh work pending.

Therefore:

```text
OP exists
    != garbage collection complete
    != all reserved capacity is immediately writable
    != all stale embodiments are physically erased
```

This extends Case 150's existing rule:

```text
maintenance opportunity
    != maintenance completion
```

into a capacity dimension:

```text
maintenance headroom
    != maintenance completion
```

## E — over-provisioning can alter write amplification without changing logical identity

The adaptive-OP patent explicitly allows the controller to change the physical-location count / OP overhead while preserving the specified host-visible user capacity.

That means the logical namespace can remain stable while the internal ratio of current data, holes, reserved capacity, ECC overhead, and other physical resources changes.

For the repository's identity vocabulary:

```text
same logical address range
    can coexist with
changed physical maintenance budget
```

No host-visible logical mutation is required merely because the controller changes how much physical capacity it reserves for future maintenance.

## E — an OP pool is not equivalent to a permanent physical partition

The OCZ source's block transitions show that `User Pool` and `OP Pool` can be controller-defined roles.

Therefore the safer abstraction is:

```text
physical block
    + current controller classification
    + mapping / occupancy state
    -> present maintenance role
```

rather than:

```text
physical block
    -> permanently user or permanently spare
```

This is a source-specific implementation pattern, not a universal SSD rule.

## E — endurance improvement is not the same relation as retention-time extension

Intel's HET brief intentionally joins several criteria: amount of host data written over lifetime, error rate, and end-of-life powered-off retention. It describes 20% over-provisioning as one input to lower write amplification and higher endurance.

The engineering relationship is therefore indirect:

```text
more maintenance headroom
    -> potentially fewer internal NAND writes / less write amplification
    -> slower consumption of finite P/E-cycle budget under a workload
    -> larger host-write endurance envelope under the product's qualification conditions
```

That does **not** license:

```text
20% OP
    -> 20% longer passive data-retention time
```

Nor does it mean over-provisioning itself refreshes charge. Intel separately names background data refresh.

## E — reserve capacity is a resource, not a certificate

A useful project-level distinction follows:

```text
capacity resource
    != policy
    != execution
    != completion evidence
```

Reserved capacity may make a maintenance action feasible, but additional state still determines:

- which pages are current;
- which pages may be discarded;
- which block is selected;
- where live data move;
- when mapping authority changes;
- when source blocks are actually erased;
- whether the resulting state satisfies endurance / integrity / service goals.

Thus headroom should be analyzed as **one input to a retention-maintenance process**, not as a stand-alone guarantee.

---

# Functional comparison

## A — OP is functionally comparable to replacement / repair headroom, but not historically identical

Other repository cases include finite spare sectors, spare rows, replacement blocks, replica-placement capacity, and repair bandwidth.

Over-provisioned SSD capacity is functionally comparable in one narrow sense:

> some capacity is withheld from ordinary immediate payload occupancy so that future state transitions remain possible.

But the analogy stops there.

- SCSI spare sectors are not an SSD OP pool.
- DRAM spare rows are not GC headroom.
- distributed spare capacity does not share NAND erase geometry.
- repair bandwidth is not physical Flash capacity.

No shared genealogy follows from the comparison.

## A — OP and filesystem free space can both provide slack, but their authorities differ

Host-visible free space and controller OP can both influence how much physical work the SSD ultimately performs, but they arise under different authorities.

A filesystem can decide an LBA no longer carries useful host data. The controller owns the lower-level mapping, erase geometry, physical occupancy, pool assignment, and reclaim policy.

TRIM can transfer some host retirement knowledge downward, but:

```text
host semantic free space
    != controller maintenance-reserve state
```

This distinction remains true even when user-created unallocated LBAs indirectly increase a controller's usable slack on a particular implementation; this packet does not generalize that behavior without device-specific evidence.

## A — Intel HET shows co-operation, not equivalence, among maintenance mechanisms

The Intel 710 HET brief is useful precisely because it lists multiple mechanisms in one named product family:

- background refresh;
- wear leveling;
- programming / disturb management;
- extra spare area / over-provisioning.

Their co-presence blocks a common conceptual shortcut:

```text
all SSD reliability maintenance = garbage collection
```

A better decomposition is:

```text
capacity headroom
    supports some future transformations

mapping/currentness state
    says which embodiment counts

wear policy
    distributes finite mutation budget

background refresh
    renews vulnerable data embodiments

GC / compaction
    converts fragmented invalidity into reusable erase blocks
```

These functions can interact without becoming one mechanism.

---

# Philosophical interpretation

## I — “unused” can be an active condition of future persistence

The technically interesting point is not that empty capacity is mysteriously productive. It is more precise:

> a system may preserve part of its material capacity from immediate host-visible occupation so that it retains the **ability to transform itself later without losing what must remain current**.

In this bounded SSD case, persistence is therefore conditioned not only by the material cells that currently embody data, but also by **uncommitted transformation capacity**.

This can support later philosophical work on availability and reserve, but it must not be collapsed into Heidegger's `Bestand`. `Over-provisioning`, `spare area`, `User Pool`, and `OP Pool` are engineering relations with specific controller semantics, not synonyms for standing-reserve.

## I — retention infrastructure can include absence / non-occupation

A NAND area that does not currently hold valid host payload is not thereby meaningless to the retention system. Its non-occupation can be a controlled resource that allows:

- current payload to be relocated;
- stale embodiments to be retired;
- erase blocks to be regenerated for future writes;
- write amplification and wear pressure to be reduced.

The important limit is that **non-occupation is not enough by itself**. The controller must still possess mapping/currentness knowledge, admissible policy, executable maintenance opportunity, and successful completion paths.

So the conceptual result is relational:

```text
absence of current payload
    can be intentionally retained
    as capacity for future continuity
```

not:

```text
empty space itself stores data
```

---

# Explicit non-claims

This packet does **not** claim that:

1. Shalvi, Sommer, or Kasorla invented SSD over-provisioning.
2. OCZ invented the User Pool / OP Pool distinction.
3. Intel invented product over-provisioning.
4. the 2009-priority adaptive-OP application was publicly available in 2009.
5. a patent disclosure proves a shipping controller implemented every claimed mechanism.
6. the OCZ patent describes all OCZ SSD firmware.
7. the Intel SSD 710's 20% configuration is a universal optimum.
8. 20% over-provisioning gives 20% more passive retention time.
9. more over-provisioning always improves every workload or reliability metric.
10. an OP-pool block is necessarily erased or empty.
11. an erased block is necessarily assigned to OP rather than user service.
12. host-visible free space is identical to controller over-provisioning.
13. TRIM is identical to over-provisioning.
14. garbage collection is identical to over-provisioning.
15. wear leveling is identical to garbage collection.
16. background data refresh is identical to garbage collection.
17. over-provisioning completion proves stale physical cells have been sanitized.
18. over-provisioning provides power-loss protection.
19. reserve capacity alone proves crash-consistent mapping updates.
20. Intel SSD 710 behavior proves Crucial M550 internal implementation.
21. OCZ's transitionable OP pool proves every SSD uses dynamic pool membership.
22. adaptive over-provisioning proves all commercial controllers dynamically change OP at runtime.
23. manufacturer endurance ratings are direct measurements of analog-cell remanence under every condition.
24. chronology among these sources establishes actor-to-actor influence or genealogy.
25. the project term `maintenance headroom` is period vocabulary.

---

# Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| A 2009-priority adaptive-OP disclosure separates physical capacity from specified host-visible logical capacity | H/P | direct patent text |
| That disclosure allows OP overhead to change while specified user capacity remains unchanged | H/P | direct patent text |
| It links greater OP to more efficient garbage collection, lower wear, and higher throughput in the disclosed model | H/P | direct patent text |
| It permits trade-offs among OP, ECC redundancy, density, compression, wear/health and reliability criteria | H/P | direct patent text |
| The 2012 OCZ publication defines separate User Pool and OP Pool roles | H/P | direct patent text |
| OCZ permits blocks to transition between the pools | H/P | direct patent text |
| OCZ permits data / partially written blocks in the OP pool | H/P | direct patent text |
| Therefore OP-pool membership is not identical to erased-block state in that design | E | bounded inference from direct patent text |
| OCZ describes erase after live-page relocation without requiring a host TRIM/erase command | H/P | direct patent text |
| Intel 2011 SSD 710 literature documents 20% OP configurations with higher product endurance / random-write figures | H/P | directly inspected Intel product brief |
| Intel HET literature says extra spare area lowers write amplification | H/P | directly inspected Intel technology brief |
| Intel separately names background refresh, wear leveling, disturb management, and spare area | H/P | directly inspected Intel technology brief |
| Reserved capacity can function as relocation / reclamation headroom | E | mechanism reconstruction bounded by patent + product evidence |
| Maintenance headroom is not proof of maintenance completion | E | relation decomposition |
| Host-visible free space, discard authority, OP capacity, and erased-media readiness should remain distinct | E | cross-source reconstruction |
| OP is historically identical to spare sectors / spare DRAM rows / distributed repair capacity | X | explicitly unsupported |
| Over-provisioning is `Bestand` | X | explicitly unsupported |

---

# Remaining evidence debt

This packet closes only the bounded relation **physical capacity > host-visible capacity → reserved maintenance headroom → lower relocation/GC pressure / write amplification under cited designs → endurance/service consequences**.

Still open:

- earlier public uses of `over-provisioning`, `spare area`, and vendor-specific equivalents before the 2009–2012 source window;
- precise chronology from raw-Flash spare blocks / card controllers into managed SATA SSD terminology;
- shipping-product measurements that separate factory OP, user-configured OP, host-unallocated LBAs, TRIM availability, workload, and firmware policy;
- exact controller crash-consistency treatment when moving a block between user and OP roles;
- device-specific evidence for whether and how OP-pool role metadata persist across reset / power loss;
- cross-vendor differences in whether OP means a fixed physical partition, a logical accounting relation, a dynamic pool, or some combination;
- the relation among factory bad-block reserve, replacement reserve, GC headroom, ECC/parity overhead, and marketed user capacity in named products;
- whether Intel SSD 710's user-configurable / documented 20% OP condition changes namespace size, accessible LBA span, or another exposed configuration in the exact product workflow;
- independent fault / workload experiments for the three primary-source mechanisms used here;
- broader vendor genealogy and manufacturing / product-market history.

Those broader engineering-history questions belong primarily in `tmzncty/computing-archaeology`. A fresh connector search for `over-provisioning SSD 710` found no dedicated companion packet during this run, so this repository keeps only the retention-specific capacity-headroom seam.

---

# Related repository boundary

## `tmzncty/computing-archaeology`

Keep there:

- invention / terminology genealogy of SSD over-provisioning;
- controller-vendor lineage;
- factory capacity binning and NAND-yield history;
- bad-block reserve / spare-block implementation history;
- commercial product adoption and configuration tooling;
- cross-vendor benchmarks and firmware archaeology;
- the broader transition from raw-Flash management to SATA/NVMe managed SSDs.

Keep here:

```text
physical capacity
    != host-visible capacity
    -> reserved maintenance headroom can exist

reserved headroom
    + currentness/mapping authority
    + relocation/erase machinery
    -> makes some future preservation/reclamation transitions feasible

but

reserved headroom
    != those transitions already completed
```

---

# Sources

## Primary

1. Ofir Shalvi, Naftali Sommer, Yoav Kasorla, **`Adaptive over-provisioning in memory systems`**, US8479080B1, prior-art date 12 July 2009, filed 24 June 2010, published / granted 2 July 2013. Google Patents transcription and assignment timeline: <https://patents.google.com/patent/US8479080B1/en>.
2. Franz Michael Schuette, **`NAND flash-based solid state drive and method of operation`**, US20120117309A1, priority 7 May 2010, filed 9 May 2011, published 10 May 2012, original assignee OCZ Technology Group, Inc.: <https://patents.google.com/patent/US20120117309A1/en>.
3. Intel Corporation, **`Intel Solid-State Drive 710 Series`**, Product Brief, 2011, 325843-001US: <https://www.intel.com/content/dam/doc/product-brief/ssd-710-series-brief.pdf>.
4. Intel Corporation, **`High Endurance Technology in the Intel Solid-State Drive 710 Series`**, Technology Brief, 2011, 325778-001US: <https://www.intel.co.jp/content/dam/www/public/us/en/documents/technology-briefs/ssd-710-series-het-brief.pdf>.

## Source-use note

The patents are used as period primary design disclosures and prior-art witnesses, not as evidence of universal or shipped behavior. The Intel briefs are used as manufacturer-primary evidence for one named product family's documented over-provisioning / endurance / write-amplification relation. No source here establishes that Crucial M550 firmware used the Shalvi/Sommer/Kasorla adaptive scheme or OCZ's exact pool-transition mechanism.