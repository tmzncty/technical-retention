# Synthesis Audit 04 — Privileged Physical Location

> **Question:** does the provisional thesis `logical persistence can become increasingly detached from a privileged physical location` survive comparison across passive position, magnetic core, DRAM, mapped Flash, and RADOS?

**Status:** bounded pre-synthesis audit.

This document tests README thesis 5 against the five grounded retention regimes. It treats `privileged physical location` as a **modern analytical phrase**, not as vocabulary attributed to Cheng Dawei, Forrester, Dennard, Ban, Intel, or the Ceph/RADOS authors.

Grounded cases used here:

- [`00 — Abacus / reckoning retained position`](../cases/00-abacus-retained-position.md), with [`evidence/00-abacus-rod-line-reckoning-grounding.md`](../evidence/00-abacus-rod-line-reckoning-grounding.md);
- [`02 — Magnetic core destructive read`](../cases/02-magnetic-core-destructive-read.md), with [`evidence/02-magnetic-core-1951-1954-grounding.md`](../evidence/02-magnetic-core-1951-1954-grounding.md);
- [`03 — DRAM scheduled restoration`](../cases/03-dram-refresh-as-scheduled-restoration.md), with [`evidence/03-dram-1967-1982-grounding.md`](../evidence/03-dram-1967-1982-grounding.md);
- [`04 — Mapped Flash logical identity`](../cases/04-flash-virtual-mapping-logical-identity.md), with [`evidence/04-flash-1992-1998-grounding.md`](../evidence/04-flash-1992-1998-grounding.md);
- [`05 — RADOS replica agreement and repair`](../cases/05-rados-replicated-object-repair.md), with [`evidence/05-rados-2006-2007-grounding.md`](../evidence/05-rados-2006-2007-grounding.md).

The mercury delay-line case remains `first-pass` and is excluded from the formal verdict.

The historical engineering of early memories should continue to be reused from [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology), especially its [`docs/memory/`](https://github.com/tmzncty/computing-archaeology/tree/main/docs/memory) track and the bounded core-memory study [`why-core-memory-was-worth-weaving.md`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md). This audit adds a retention-specific comparison rather than another device history.

---

## 1. Verdict

The thesis **survives only after `detached` is weakened and `privileged physical location` is decomposed**.

The strongest defensible form is:

> **Some storage layers allow a logical identity to survive replacement of any one permanent physical home. This does not make retained state placeless or substrate-independent. Instead, the invariant can move upward: from fixed physical position, to a stable selected cell whose immediate physical state is repeatedly reconstructed, to a logical identity resolved through mapping metadata, to a distributed identity maintained across replaceable replicas by placement, version, and authority rules.**

The phrase `increasingly detached` is therefore acceptable only as a **bounded functional comparison across selected systems**, not as a universal historical law or a teleological sequence.

Several stronger claims are rejected:

```text
logical persistence never depends on location                  -> rejected
physical reconstruction already means location detachment     -> rejected
remapping makes storage immaterial                             -> rejected
replication eliminates all privileged copies or authorities   -> rejected
later storage is simply more placeless than earlier storage   -> rejected
physical location stops mattering once logical mapping exists -> rejected
```

A more useful layered model is:

```text
logical identity / designation
        ↓
relation that resolves current embodiment(s)
        ↓
physical embodiment(s) that exist somewhere now
        ↓
where needed, currentness / protocol authority
        ↓
read / write / repair / migration
```

The central transition is not from `physical` to `nonphysical`. It is from **identity requiring one stable physical home** toward **identity surviving controlled replacement of its physical embodiments**.

---

## 2. Terms required by the audit

### 2.1 Physical embodiment

The material state that currently realizes a retained value or object: bead position, magnetic remanence in one core, charge in a DRAM cell, programmed Flash cells, or one RADOS replica.

Every grounded case still has physical embodiment. Nothing in this audit supports `logical persistence without material realization`.

### 2.2 Permanent physical home

A physical location whose continuity is required for the identity to remain the same operational state.

This is an analytical category, not period vocabulary. A system may have a stable home at one layer while repeatedly replacing lower-level physical tokens inside that home.

### 2.3 Current physical embodiment

The physical location or set of locations that presently count as realizing a logical identity.

A system can lack a **permanent** home while still requiring one or more **current** embodiments at any given time.

### 2.4 Placement / mapping relation

Retained or reconstructible state that answers where a logical identity is currently embodied.

Mapped Flash makes this explicit through virtual/logical-to-physical mapping and allocation state. RADOS computes placement from object/PG identity plus the current cluster map and CRUSH, then adds version/peering/currentness rules.

### 2.5 Protocol authority

A temporary right to order updates or answer as current in a replicated system.

Removing a permanent physical home does not imply removing authority. The bounded 2006 RADOS design has a primary; the 2007 account documents multiple replication schemes and explicit stale-read exclusion/currentness rules.

---

## 3. Primary-source anchors already grounding the comparison

This audit introduces no new historical facts. It reuses exact source work already recorded in the grounded cases.

| Case | Primary anchor | What matters for the location question |
| --- | --- | --- |
| Abacus / positional reckoning | Cheng Dawei, *Suanfa Tongzong* (1592), directly inspected `直指定位訣`, Source Library scan p. 70 / 82 | the numerical state is constituted partly by where beads/counters remain within a positional convention; moving them changes the operative state |
| Magnetic core | Forrester, US 2,736,880, printed pp. 2–3; Papian 1953, p. 38 | a bounded classic memory location is selected by coordinates and restored at that location after destructive read; remanence is local to the core |
| DRAM | Dennard's 1967-filed patent; AMD Am9016 (1979), p. 3-63; Intel AP-133 (1982), p. 3-72 | charge is repeatedly sensed/restored while row/column selection continues to designate the same bounded physical cell/array position |
| Mapped Flash | Ban/M-Systems US 5,404,485, printed pp. 2–6; Wells/Intel US 5,341,339; Intel AP-619 (1995), p. 3 | a stable logical identity can be rebound to a new physical block; mapping/allocation state determines which embodiment currently counts |
| RADOS | Ceph OSDI '06 pp. 312–314; CRUSH SC '06; RADOS PDSW '07 pp. 38–39 | object identity survives changes in replica membership and primary/read authority; placement and currentness are reconstructed from map/version/peering state rather than one permanent home |

The evidence records linked above preserve exact bibliographic details, scan anchors, and claim boundaries.

---

## 4. Cross-case test

### 4.1 Passive positional retention: location can be constitutive of identity

The abacus / line-reckoning case blocks a universal detachment thesis immediately.

In a positional calculating surface, the operational numerical state is not a token that merely happens to sit somewhere. Position is part of what the configuration means.

For the bounded abacus case:

```text
bead configuration
    + rod/place convention
    + procedural context
        ↓
actionable numerical state
```

If a bead is moved to another valid position, the retained numerical state changes. The location is therefore not accidental metadata surrounding an otherwise location-independent value.

This does **not** mean every early positional device has one machine-style `physical address`, and it does not make an abacus a RAM array. It establishes a simpler point: some retained states are **location-bound by their very interpretation**.

**Result:** logical persistence is not universally detached from location; some operational identities are partly constituted by stable position.

### 4.2 Magnetic core: physical remanence is local, and classic restore returns to the selected home

The bounded magnetic-core case also remains strongly location-bound.

A particular core retains a remanent magnetic state. Coincident-current selection targets that core through coordinates, and the classic destructive-read cycle rewrites the value so continued retention is restored at that selected location.

The logical value survives destruction of the immediately preceding magnetic orientation during read, so **physical-token identity is already weaker than logical identity**. But the value is not relocated to a different core merely by being restored.

This distinction matters:

> replacement of the microscopic physical state is not the same thing as replacement of the physical home.

The grounded nondestructive-read counterexamples also show that destructive read is a regime rather than an essence of core memory, but they do not change this location point.

**Result:** the same logical value can survive physical-state re-creation while remaining tied to one selected physical location.

### 4.3 DRAM: repeated reconstruction without location detachment

DRAM is the strongest counterexample to a sloppy equation:

```text
physical state changes repeatedly
        =
logical identity detached from physical location
```

That equation is false.

In the bounded DRAM evidence, storage-node charge leaks and is periodically reconstructed. Sense/restore machinery can destroy or amplify the weak state and return a restored value to the cell. Yet the architectural row/column selection relation continues to target the same bounded cell/array position.

Thus two forms of continuity separate:

```text
immediate physical charge continuity     -> weak / repeatedly broken
selected-cell location continuity        -> strong in the bounded case
logical value continuity                 -> maintained across restoration
```

DRAM therefore proves that **logical identity can be detached from the identity of one microscopic physical token without being detached from a privileged physical home**.

This is the audit's most important middle case because it prevents a false two-stage story of `fixed matter → placeless logic`.

**Result:** token replacement and location replacement are distinct operations.

### 4.4 Mapped Flash: identity survives deliberate replacement of the physical home

Mapped Flash is where the stronger detachment claim becomes directly grounded.

Ban's 1993-filed system explicitly keeps the original virtual/logical identity while writing replacement data to an unwritten physical block and updating the map. The old block can become `deleted and not writable` before the containing erase unit is physically erased. Unit transfer can copy still-current state elsewhere, erase the old unit, and keep the logical unit number unchanged.

The invariant therefore shifts:

```text
before remapping:
logical identity -> physical block A

after remapping:
logical identity -> physical block B
```

What must remain stable is no longer block A. Instead, the system must retain or reconstruct enough mapping/allocation state to establish that B now counts as the embodiment of the same logical identity.

This is not immateriality. It is **metadata-mediated relocation**.

The physical old embodiment may persist for a while even after losing logical currentness. Physical survival and logical identity therefore separate in both directions:

- the logical identity can survive while location changes;
- the old location can survive physically while no longer counting as the logical object.

**Result:** a stable logical identity can survive replacement of its physical home, but only because another retained relation binds identity to the current embodiment.

### 4.5 RADOS: no permanent home, but physical placement and temporary authority remain constitutive

RADOS extends the location question beyond one-device remapping.

The bounded 2006 design maps object identity to a placement group and then through CRUSH plus the current cluster map to an ordered OSD set. Failure can move primary responsibility and eventually add a new OSD to replace lost replica membership. Peering/version/log state determines the correct current contents before normal I/O resumes.

The 2007 material strengthens the point: membership can change for failure, recovery, expansion, contraction, or new placement policy, and peering examines intervening map epochs so a returning OSD cannot silently answer with stale state.

The object therefore does not require one permanent device to remain its physical home.

But three qualifications are essential.

#### Qualification 1 — replicas are still physical

At any moment the object must be embodied on actual OSD media/caches. Distribution does not abolish locality; it makes locality plural and replaceable.

#### Qualification 2 — topology still matters

CRUSH explicitly treats physical failure domains as placement constraints. Cabinets, power supplies, networks, and other topology remain part of retention engineering. A distributed object can be free of one permanent home while being deeply dependent on **where** replicas are placed relative to correlated failures.

#### Qualification 3 — authority does not disappear with home

The bounded 2006 path has a primary that orders updates. The 2007 paper changes replication/read paths but still requires explicit currentness and stale-read exclusion. A permanent physical home can disappear while **temporary protocol authority becomes more important**.

**Result:** distributed retention removes the need for one permanent physical home but replaces it with placement relations, topology constraints, and currentness/authority state.

---

## 5. The staged claim that survives

The cases support a staged comparison, but not a universal historical staircase.

### Stage A — position is part of the state

Abacus / reckoning surfaces:

```text
identity ~= token + position + convention + procedure
```

Stable location is constitutive.

### Stage B — physical token changes, home remains stable

Classic magnetic-core restore and bounded DRAM restoration:

```text
logical value survives re-creation
while selected physical home remains stable
```

The microscopic carrier is replaceable without relocating the architectural location.

### Stage C — home becomes replaceable through mapping

Mapped Flash:

```text
logical identity
    + retained mapping/allocation relation
        -> current physical embodiment
```

Physical home can change intentionally while identity remains stable.

### Stage D — multiple homes are replaceable and authority is protocol-defined

RADOS:

```text
object identity
    + placement relation
    + membership/version/currentness state
        -> authorized current replica set
```

No single device is permanently privileged, but the protocol still privileges some states/roles temporarily.

These stages are a **functional comparison**. They are not a genealogy asserting that abacus state evolves into DRAM, Flash, and RADOS, nor a claim that all later systems occupy Stage D.

Modern systems routinely contain all four kinds of relation at once: fixed physical cells, stable architectural addresses, remapped blocks, and distributed replicas can coexist in one stack.

---

## 6. Counterexample ledger

| Candidate claim | Result | Why |
| --- | --- | --- |
| Logical persistence is always independent of physical location. | **rejected** | abacus position is constitutive of the operational numerical state; core/DRAM bounded locations remain stable homes |
| Reconstructing physical state means the logical object has moved. | **rejected** | core rewrite and DRAM refresh re-create state at the same selected location |
| Logical identity can survive changes in microscopic physical state. | **supported** | core restore and DRAM regeneration preserve a logical value across re-created physical states |
| A stable logical identity can survive replacement of its physical home. | **supported with scope** | grounded mapped Flash and RADOS do so through mapping/placement/currentness machinery |
| Remapping or replication makes retained state immaterial. | **rejected** | every current embodiment remains physical; the system adds relations that identify which physical embodiments count |
| Once mapping exists, physical location becomes irrelevant. | **rejected** | Flash erase geometry, bad blocks, wear, and RADOS failure-domain topology make location operationally consequential |
| Distributed replication removes every privileged copy. | **rejected** | RADOS removes a permanent home but retains temporary primary/read authority and currentness rules |
| Later technologies are monotonically more `placeless`. | **rejected** | layers coexist; later systems may increase relocation freedom while also increasing metadata, topology, and protocol dependence |
| Location detachment reduces maintenance requirements. | **rejected** | Flash remapping/reclamation and RADOS peering/repair add maintenance precisely because embodiments are replaceable |
| Detachment moves the invariant rather than eliminating it. | **supported** | the invariant shifts from physical position toward address/mapping/placement/currentness relations |

---

## 7. What actually changes when the permanent home is removed

### 7.1 The object of retention expands

A location-bound state may require a substrate plus interpretation.

A relocatable logical state additionally requires a retained or reconstructible relation saying which embodiment is current.

```text
location-bound state:
value + physical position + interpretation

mapped state:
value + logical identity + mapping/allocation state

distributed state:
value + object identity + placement + membership/version/currentness state
```

Removing one invariant creates another retention burden.

### 7.2 Failure changes from `did the place survive?` to `can identity be rebound?`

In a location-bound case, destruction of the privileged home can directly destroy the retained state.

In mapped/distributed cases, a failed physical location can be tolerated if:

- another current embodiment exists or can be reconstructed;
- the identity relation survives;
- enough metadata/currentness history survives to reject stale embodiments;
- repair has somewhere valid to place the reconstructed state.

This is a stronger form of **substitutability**, not absence of substrate.

### 7.3 More mobility can mean more metadata dependence

Mapped Flash and RADOS both expose a paradox:

> the less identity depends on one fixed physical place, the more it may depend on retained relations that say which changing places count.

This is not a universal law, but it is strongly supported in the two grounded relocation cases.

Loss of mapping, cluster-map, version, or recovery state can therefore make physically surviving data operationally ambiguous or stale.

### 7.4 Physical topology remains part of logical durability

RADOS is especially important here. Eliminating a permanent home does not eliminate geography, cabinets, power, switches, or correlated-failure domains. Placement policy actively uses them.

The correct contrast is therefore not:

```text
physical location -> logical abstraction
```

but:

```text
one fixed home
    -> controlled relocation
    -> multiple replaceable embodiments
while physical topology remains an engineering constraint
```

---

## 8. Historical and philosophical boundaries

### Historical record

Period sources establish concrete mechanisms and vocabulary:

- positional instructions and retained configurations;
- coordinate-selected magnetic states;
- DRAM row/column and sense/restore machinery;
- Flash virtual/logical/physical mapping and transfer;
- RADOS placement groups, CRUSH, cluster maps, primaries, versions, peering, and replica repair.

They do **not** establish one transhistorical doctrine called `detachment from privileged physical location`.

### Engineering reconstruction

The staged comparison above is an engineering reconstruction across mechanisms. It identifies which invariant must survive when physical embodiments change.

### Functional analogy

Saying that these systems move an identity invariant `upward` is a functional analogy. It does not imply technical descent, shared purpose, or a single evolutionary line.

### Philosophical interpretation

A later philosophical argument may ask whether technical objects become increasingly defined by relations of availability, substitutability, or reproducibility rather than by enduring carriers. This audit does not settle that question.

It establishes the mechanism-level constraint any such interpretation must respect:

> **logical substitutability never abolishes physical embodiment; it changes which relations must survive for changing embodiments to count as the same retained thing.**

---

## 9. Revised thesis

The README thesis should no longer say simply:

> `Logical persistence can become increasingly detached from a privileged physical location.`

A more defensible form is:

> **Logical persistence can become detached from any one permanent physical home without becoming placeless. Some systems keep a stable location while repeatedly reconstructing physical state; mapped and distributed systems go further by letting identity survive relocation or replica replacement through retained mapping, placement, version, and authority relations. Treat this as a mechanism comparison, not a one-way historical law.**

---

## 10. Next bounded synthesis task

Audits 01–04 now contain local counterexample tables, but the repository still lacks one **cross-audit counterexample ledger** that tracks which provisional theses have been:

- rejected outright;
- narrowed;
- split into multiple layers;
- retained with scope conditions;
- or left untested.

That ledger should be built before any provisional thesis is promoted to a conclusion and before writing a grand `What Is Technical Retention?` chapter.
