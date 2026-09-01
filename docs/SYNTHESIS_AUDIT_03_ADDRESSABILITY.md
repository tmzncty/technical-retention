# Synthesis Audit 03 — Addressability, Selection, and Currentness

> **Question:** does the provisional thesis `addressability changes what retention can do` survive comparison across passive position, coordinate-selected memory, DRAM, mapped Flash, and distributed object storage?

**Status:** bounded pre-synthesis audit.

This document tests README thesis 3 against the five grounded retention regimes. It does not claim that all retained traces are addressable, that later addressing schemes are simply better versions of earlier ones, or that historical actors used the modern umbrella term `addressability` for the same conceptual problem.

Grounded cases used here:

- [`00 — Abacus / reckoning retained position`](../cases/00-abacus-retained-position.md), with [`evidence/00-abacus-rod-line-reckoning-grounding.md`](../evidence/00-abacus-rod-line-reckoning-grounding.md);
- [`02 — Magnetic core destructive read`](../cases/02-magnetic-core-destructive-read.md), with [`evidence/02-magnetic-core-1951-1954-grounding.md`](../evidence/02-magnetic-core-1951-1954-grounding.md);
- [`03 — DRAM scheduled restoration`](../cases/03-dram-refresh-as-scheduled-restoration.md), with [`evidence/03-dram-1967-1982-grounding.md`](../evidence/03-dram-1967-1982-grounding.md);
- [`04 — Mapped Flash logical identity`](../cases/04-flash-virtual-mapping-logical-identity.md), with [`evidence/04-flash-1992-1998-grounding.md`](../evidence/04-flash-1992-1998-grounding.md);
- [`05 — RADOS replica agreement and repair`](../cases/05-rados-replicated-object-repair.md), with [`evidence/05-rados-2006-2007-grounding.md`](../evidence/05-rados-2006-2007-grounding.md).

The mercury delay-line case remains `first-pass` and is excluded from the formal verdict. Its temporal-slot access geometry is important, but the audit should not depend on an ungrounded case to establish a general distinction.

---

## 1. Verdict

The thesis **survives, but only after separating retention from addressability and decomposing addressability into several operations**.

The strongest defensible form is:

> **A retained state can physically or logically persist without being cheaply or autonomously selectable. Addressability is an operational relation layered onto retention: a designation is resolved into one or more candidate embodiments, those candidates may have to satisfy additional currentness or admissibility rules, and a read/recovery operation then makes the chosen state usable. Stable logical designation does not imply stable physical location.**

This rejects several stronger claims:

```text
retention requires a machine-readable address                 -> rejected
an address is simply the physical place where data live       -> rejected
stable address implies stable location                        -> rejected
resolution to a replica proves that replica is current        -> rejected
addressability is one scalar property from poor to good       -> rejected
addressability and availability are synonyms                  -> rejected
```

The cases instead expose a layered path:

```text
designation / identity
        ↓
selection or resolution
        ↓
candidate physical embodiment(s)
        ↓
optional admissibility / currentness test
        ↓
read / reconstruction / interpretation
        ↓
usable retained state
```

Cost, latency, repeatability, and automation change how powerful this relation is, but they are not identical to the existence of the relation itself.

---

## 2. Why `addressability` must not be treated as one thing

The current glossary defines addressability as the ability to select a particular retained state or region from a larger set. The grounded cases support that umbrella definition, but they require at least four separable questions.

### 2.1 Designation

What identifies the requested state before access begins?

Examples in the bounded cases include:

- a rod/column or place in a positional calculating surface;
- coordinate signals for a magnetic-core location;
- row/column address inputs in DRAM;
- a virtual/logical block identity in mapped Flash;
- an object identifier that maps through a placement group in RADOS.

Designation can be conventional, numeric, logical, or derived. It need not already be a physical location.

### 2.2 Selection / resolution

What mechanism turns the designation into an actual target?

This may be:

- a human hand/eye selecting a position;
- coincident currents selecting one core while half-selecting others;
- decoders selecting a DRAM row/column;
- a retained translation map resolving logical to physical Flash placement;
- CRUSH plus a current cluster map resolving object/PG identity to an ordered OSD set.

The resolver can therefore be a person, circuit, table, algorithm, or distributed system state.

### 2.3 Admissibility / currentness

If multiple readable embodiments exist, which one is allowed to answer as current?

This question is weak or absent in some local cases but central in RADOS. A reachable replica may be physically readable yet stale or no longer authorized by the current map/epoch and peering state.

Mapped Flash provides a local precursor: an old physical block can remain materially present after metadata has invalidated it. The mapping relation decides which embodiment currently counts for the logical identity.

Thus `where can bytes be read?` and `which embodiment counts as current?` are not always the same question.

### 2.4 Recovery / interpretation

Selection is not yet successful use.

- an abacus position still requires convention and procedural interpretation;
- a core read may destroy the selected state and require rewrite;
- DRAM selection enters sense/amplify/restore machinery;
- mapped Flash requires the current mapping/allocation relation to survive or be rebuilt;
- RADOS may require version/log/peering state before I/O is admitted.

Addressability is therefore part of a larger recoverability path rather than a synonym for recoverability itself.

---

## 3. Primary-source anchors already grounding the comparison

This audit does not create new historical claims. It reuses the exact primary-source work already grounded in the cases.

| Case | Primary addressability anchor | What the source establishes |
| --- | --- | --- |
| Abacus / positional reckoning | Cheng Dawei, *Suanfa Tongzong* (1592), directly inspected `直指定位訣`, Source Library scan p. 70 / 82 | positions are explicitly designated under a calculation convention and the resulting configuration can be left in place for later use; machine addressing vocabulary is not present |
| Magnetic core | Forrester, US 2,736,880, printed pp. 2–3; Papian 1953, p. 38 | coordinate selection isolates a target by combined excitation while nonselected cores must tolerate lesser disturbances; access semantics and retention interact |
| DRAM | AMD Am9016 (1979), p. 3-63; Intel AP-133 (1982), p. 3-72 | row/column decoders and shared sense/restore infrastructure make selection part of both access and maintenance; selecting a row can refresh it |
| Mapped Flash | Ban/M-Systems US 5,404,485, printed pp. 2–6; Intel AP-619 (1995), p. 3 | a stable virtual/logical designation is translated to a physical location that can change; retained map/allocation state determines the current embodiment |
| RADOS | Ceph OSDI '06 p. 312 §5.1; pp. 313–314 §5.5; CRUSH SC '06; RADOS PDSW '07 pp. 38–39 | object/PG identity resolves through CRUSH and the current cluster map to candidate OSDs, while version/epoch/peering state determines currentness and safe read authority |

The exact bibliographic links and page anchors are preserved in the grounding records listed at the top of this audit.

---

## 4. Cross-case test

### 4.1 Passive position: retention can precede autonomous machine addressability

The grounded abacus / line-reckoning case is the first important limit on the thesis.

A numerical configuration can remain operationally available even though there is:

- no address bus;
- no decoder;
- no machine-issued read request;
- no stored numeric pointer to a bead position.

Selection is performed by the trained operator through spatial convention.

The meaningful relation is therefore:

```text
procedural role / desired place
        ↓
human spatial selection
        ↓
bead or counter position
        ↓
human interpretation
        ↓
actionable numerical state
```

This is enough to support **human-mediated addressability** as an engineering reconstruction. It is not evidence that Cheng or Ries possessed the modern architecture concept `address`.

The case also blocks a progress narrative. Human visual access can inspect several positions in parallel and exploit a spatial field directly. Later machine addressing adds autonomous, programmable selection, but `more modern` should not be equated with one universal scalar called `more addressable`.

**Result:** retention does not require autonomous machine addressability; addressability can be a human–technical relation.

### 4.2 Magnetic core: selection architecture becomes part of what the medium must survive

Forrester and Papian make addressability a physical selection problem.

A coincident-current array does not merely store many individually durable magnetic states. The system must drive one selected core strongly enough to switch/read it while exposing other cores to lesser, nonselecting disturbances that must not destroy their retained states.

Thus access geometry and retention are coupled:

```text
requested coordinate
        ↓
combined selection currents
        ↓
selected core crosses switching/read threshold
        ↓
nonselected cores experience sub-threshold disturbance
        ↓
retention succeeds only if selection margins preserve them
```

The selected core's classic read can itself be destructive, making rewrite part of continued retention.

This rejects the idea that addressability is always an innocent lookup layer sitting above an independent storage medium. Here the method used to select one state constrains the physical properties required of every state in the array.

**Result:** addressability can be constitutive of the retention engineering problem, not merely of the user interface.

### 4.3 DRAM: logical selection is stable while physical state is repeatedly rebuilt

Commercial DRAM sharpens the distinction between **address stability** and **physical-state continuity**.

The logical cell or row remains selectable through a stable address structure while the information-bearing charge leaks and is periodically reconstructed. AMD's Am9016 block diagram explicitly includes row/column decoders and 128 sense-restore amplifiers; Intel AP-133 explains row selection, sensing, amplification, and return-to-cell.

The same row-level access machinery can therefore participate in maintenance:

```text
row designation
        ↓
row decoder / selection
        ↓
weak cell signals exposed on bit lines
        ↓
sense / amplify
        ↓
restored values returned to cells
```

A stable logical address can hide repeated replacement of the immediate physical electrical state.

This gives a precise answer to one question raised in the technical spine: what temporal assumptions are hidden by a stable address interface? At minimum, **the interface can preserve a stable selection relation while the selected state is repeatedly reconstructed underneath it**.

**Result:** address stability does not imply physical-token stability; selection infrastructure can also be retention infrastructure.

### 4.4 Mapped Flash: the address becomes an invariant while location deliberately moves

Mapped Flash is the strongest local case for separating designation from placement.

Ban's 1993-filed system lets the original virtual/logical identity continue while a replacement value is written to a new unwritten physical block. The map is then changed so the same external identity resolves to the new embodiment. Intel AP-619 later gives explicit FTL vocabulary for the same broad translation problem.

The path becomes:

```text
stable virtual/logical designation
        ↓
retained translation/allocation state
        ↓
current physical location
        ↓
read current embodiment
```

After an update, the old physical embodiment can still exist while no longer being the answer to the logical designation.

This means an address is no longer well described as `the place where the data are`. It is better treated as a **stable identity relation whose resolver may change its physical answer over time**.

It also makes metadata loss a special form of technical forgetting: the physical state may survive while the relation needed to find the current embodiment is lost.

**Result:** stable address and stable location are explicitly decoupled; mapping metadata becomes part of operational retention.

### 4.5 RADOS: resolution to a location is still not enough

RADOS forces a second separation that mapped Flash only begins to expose.

In the bounded 2006 design, object identity maps to a placement group and then through CRUSH plus the current cluster map to an ordered list of OSDs. But this calculation only gives candidate members. After failures or map changes, a physically reachable copy can be stale, missing updates, or no longer authorized to serve the current state.

Peering, version information, map epochs, logs, and temporary primary/read authority answer a further question:

> Which of the candidate embodiments currently counts?

The path is therefore closer to:

```text
object identity
        ↓
object -> PG
        ↓
CRUSH + current cluster map
        ↓
candidate OSD set
        ↓
version / epoch / peering / authority checks
        ↓
authorized current state
```

The 2007 RADOS paper makes this especially explicit by blocking stale read authority after membership changes and by examining intervening map epochs during peering.

This is a decisive counterexample to the assumption that `address resolved successfully` implies `current data located successfully`.

**Result:** distributed retention requires separating placement resolution from currentness authorization.

---

## 5. Counterexample ledger

| Candidate claim | Result | Why |
| --- | --- | --- |
| A retained state must have a machine-readable address. | **rejected** | passive positional working retention can be selected and interpreted by a human without an address bus or decoder |
| A physical trace that persists is automatically addressable. | **rejected** | persistence of a state does not guarantee that a selector, map, convention, or index exists to find it |
| Addressability is simply knowledge of physical location. | **rejected** | mapped Flash and RADOS compute current placement from stable logical identities and retained metadata |
| Stable logical address implies stable physical location. | **rejected** | Flash deliberately relocates embodiments while preserving virtual/logical identity; RADOS changes replica membership |
| If a physical copy can be reached, it can safely answer as current. | **rejected** | RADOS stale replicas and outdated read authorities are direct counterexamples |
| Addressability and availability are the same property. | **rejected** | a state can be correctly designated yet unavailable because mapping/currentness metadata, interpretation, interface, or a valid readable embodiment is missing |
| Selection is independent of retention mechanism. | **rejected** | core half-select disturbance and destructive read, DRAM sense/restore, Flash mapping, and RADOS peering couple access machinery to retention conditions |
| Addressability is a single scalar that simply increases historically. | **rejected** | human spatial selection, random coordinate selection, logical translation, and distributed resolution optimize different properties and expose different costs |
| Stable designation can survive replacement of the physical embodiment. | **supported** | DRAM reconstruction, mapped Flash remapping, and RADOS placement/repair support this at different layers |
| Addressability changes operational usefulness even when the physical retention mechanism is unchanged. | **supported** | the same retained state can be easy, slow, ambiguous, or impossible to select depending on geometry, mappings, conventions, and authority state |

---

## 6. What addressability actually changes

### 6.1 It turns persistence into selective reuse

A trace that merely survives may still be historically or forensically discoverable. Addressability adds the ability to request **this** state rather than merely encounter whatever survived.

That matters for computation because repeated algorithms usually need selective reuse, not just undifferentiated persistence.

This does not mean unaddressable traces are not retained. It means the project should distinguish **retention as survival/recoverability in principle** from **operational retention as selectively reusable state**.

### 6.2 It creates new retained relations

Once location is indirect, the resolver itself must persist or be reconstructible.

Mapped Flash needs enough allocation/mapping state to identify the current physical block. RADOS needs cluster-map, placement, version, and recovery state. Those relations are not optional annotations if the user-visible identity is to remain usable.

Addressability can therefore enlarge the object of retention:

```text
value alone
    -> value + position convention
    -> value + logical address relation
    -> value + mapping metadata
    -> value + distributed placement/currentness state
```

This is a functional comparison, not a historical genealogy.

### 6.3 It can impose disturbance and maintenance costs

Selection itself can change what must be retained.

- core selection produces half-select disturbance and classic destructive read;
- DRAM row access invokes shared sensing/restoration;
- Flash updates change mapping and create reclaim obligations;
- RADOS membership/authority resolution after failures invokes peering and repair.

The cost of `being selectable` is therefore partly paid in circuits, metadata, timing margins, spare capacity, protocols, and maintenance work.

### 6.4 It separates logical identity from physical embodiment

This is the most important bridge to the next audit.

A stable logical designation can remain fixed while:

- the immediate electrical state is reconstructed;
- the physical Flash block changes;
- replica membership changes;
- temporary authority moves.

Addressability thus helps create the conditions under which logical persistence can detach from one privileged physical location. But the present audit does **not** assume that this detachment is universal or monotonically increasing. That historical claim still needs its own test.

---

## 7. Addressability is not availability

The glossary currently defines `availability` as the condition in which retained state can actually be called upon for use. The cases now support a stricter distinction:

> **Addressability asks whether a desired state can be designated and resolved toward a target. Availability asks whether that target can actually produce an admissible, meaningful, usable state now.**

Failures can therefore occur at different layers:

```text
state survives physically
    but designation is lost
        -> not addressable

logical designation survives
    but mapping/index is lost
        -> unresolved

candidate replica is reachable
    but stale / unauthorized
        -> resolved but inadmissible

correct embodiment is selected
    but readout/interpretation fails
        -> addressed but unavailable
```

This distinction prevents the project from turning `addressability`, `recoverability`, `readability`, and `availability` into synonyms.

---

## 8. Historical and philosophical cautions

### 8.1 Do not project the modern umbrella term backward

Cheng's `定位`, Forrester's multicoordinate selection, manufacturer row/column decoder vocabulary, Ban's `virtual map`, Intel's FTL terminology, and Ceph's object/PG/CRUSH language belong to different historical problem settings.

The repository may compare them under the modern analytical heading `addressability`, but that is an engineering reconstruction across cases, not evidence of one continuous actor-level concept.

### 8.2 Do not narrate a simple ascent from human to machine addressability

Automation changes who performs selection and what costs can be hidden, but the cases do not establish one universal metric of improvement. Human visual/spatial access, fixed random-access arrays, table-based remapping, and distributed algorithmic placement have different strengths and constraints.

### 8.3 Do not collapse addressability into Heideggerian availability

This audit supplies a more precise technical substrate for a future Heidegger test: some retained things are increasingly organized so they can be designated, resolved, and called upon. But `addressability`, `availability`, and `Bestand` are not synonyms.

Any later philosophical use must identify what the technical selection machinery actually adds before invoking the philosophical concept.

---

## 9. Revised thesis

The original README thesis is useful but too compact:

> `Addressability changes what retention can do. Keeping a trace is not the same as being able to retrieve a chosen trace cheaply, quickly, and repeatedly.`

The grounded evidence supports a more precise formulation:

> **Addressability is a separate operational relation layered onto retention. A state may persist without being autonomously or cheaply selectable; a stable logical designation may also survive changes in physical embodiment. Addressability should be analyzed as designation plus selection/resolution, with currentness/admissibility and read/recovery kept distinct where the mechanism requires them. Its costs include latency, disturbance, metadata, decoding, mapping, authority, and maintenance.**

This preserves the original intuition while preventing four category errors:

- retention ≠ addressability;
- address ≠ physical location;
- resolution ≠ currentness;
- addressability ≠ availability.

---

## 10. Consequence for the next synthesis pass

Thesis 3 can now be treated as **audited and revised**, not promoted to a final conclusion.

The next bounded synthesis question should be README thesis 5:

> `Logical persistence can become increasingly detached from a privileged physical location.`

That audit should not simply cite Flash and RADOS and declare victory. It should test at least four boundaries:

1. whether passive position and magnetic core supply counterexamples in which identity remains tightly location-bound;
2. whether DRAM reconstruction changes physical state without changing the cell's architectural location;
3. whether mapped Flash creates location independence only because a retained mapping relation substitutes for fixed placement;
4. whether RADOS removes a permanent privileged home while still requiring temporary protocol authority and concrete replica placement.

The historical question is therefore not whether storage `became immaterial`, but **which layers of identity became invariant under which kinds of physical replacement, and what new metadata/protocol state had to be retained to make that invariance work**.
