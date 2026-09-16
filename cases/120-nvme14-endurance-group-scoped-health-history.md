# Case 120 — NVMe 1.4 Endurance Groups: Scoped Wear History, Mixed-Lifetime Health State, and Hidden Media Work

## Status

**`grounded`** — bounded to the ratified **NVM Express Base Specification Revision 1.4 (10 June 2019)** and NVM Express's own Revision-1.4 change record, with a later bounded **Revision 2.0 / TP4052c lifecycle-management deepening**. The case establishes an optional host-visible hierarchy in which namespaces belong to NVM Sets, each NVM Set belongs to exactly one Endurance Group, and endurance may be managed either within one NVM Set or across several NVM Sets. It also separates group-lifetime cumulative/estimated health information from current nonpersistent warning state, separates host-written bytes from controller/media writes, and now distinguishes **reportable Endurance Group scope** from the later interoperable authority to create/delete that scope. The case does **not** infer a particular Flash Translation Layer, erase-unit layout, wear-leveling algorithm, physical NAND partition, invention priority for endurance pooling, or secure-erasure semantics from group deletion.

Grounding/deepening records: [`../evidence/120-nvme14-2019-endurance-group-grounding.md`](../evidence/120-nvme14-2019-endurance-group-grounding.md), [`../evidence/120-nvme14-2019-namespace-group-association-deepening.md`](../evidence/120-nvme14-2019-namespace-group-association-deepening.md), and [`../evidence/120-nvme-2019-2021-endurance-group-lifecycle-management-deepening.md`](../evidence/120-nvme-2019-2021-endurance-group-lifecycle-management-deepening.md).

---

## Scope

Case 55 established that NVMe can retain health/endurance evidence about a controller across power cycles without that evidence being the user payload. Case 76 separately established an SSD qualification relation in which workload, host TBW, write amplification, error limits, and later power-off retention have to be kept distinct.

Case 120 asks a different question:

> What changes when the interface gives endurance history and endurance-management authority a **scope smaller than the whole subsystem/controller but potentially larger than one namespace or one NVM Set**?

The object is the optional NVMe 1.4 **Endurance Group**, together with:

- the NVM Set → Endurance Group relation;
- the Endurance Group Information log (`Log Identifier 09h`);
- current/nonpersistent critical-warning bits;
- `Available Spare`, `Percentage Used`, and `Endurance Estimate`;
- host-side `Data Units Written` versus `Media Units Written` that also include controller writes such as garbage collection;
- group-specific asynchronous warning/event handling;
- and, in the bounded Revision-2.0 deepening, the host-visible lifecycle/configuration state created by Capacity Management.

This is deliberately **not**:

- a general history of SSD wear leveling;
- a claim that an Endurance Group is a physical NAND die/channel/plane/erase-block partition;
- a claim that every NVMe 1.4 or 2.0 device implements Endurance Groups or dynamic group management;
- a claim that every field in the Endurance Group Information log has one identical reset/persistence rule;
- a claim that `Percentage Used = 100` means physical failure;
- a claim that host writes equal NAND program/erase work;
- a claim that NVMe 1.4 invented endurance partitioning, spare pools, wear domains, over-provisioning, or health telemetry;
- a claim that deleting an Endurance Group sanitizes its former NAND embodiments or reverses physical wear.

Broader SSD/NAND controller architecture and wear-leveling genealogy belongs primarily in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) if developed there. A fresh repository search for `Endurance Group` / `TP4052` and related capacity-management terms found no dedicated overlapping case to reuse.

---

## Historical record

### Revision 1.4 explicitly introduces the optional Endurance Group feature

The official NVM Express **Revision 1.4**, dated **10 June 2019**, states that it incorporates Revision 1.3 plus a listed set of technical proposals, including **TP4018b** and **TP4050**.

NVM Express's own page **“Changes in NVMe Revision 1.4”** lists both **NVM Sets** and **Endurance Groups** among the optional features added in the revision. The change page defines an Endurance Group as a mechanism allowing endurance management either within a single NVM Set or across a collection of NVM Sets and points to TP4018b/TP4050.

This supports a safe historical statement:

> **NVMe Revision 1.4 is the public ratified NVMe-specification floor for the Endurance Group feature in this repository.**

It does **not** establish that 2019 is the invention date for endurance grouping as a general storage-engineering idea. The inspected source is a standards-change record, not an invention-priority study.

Primary sources:

- NVM Express, **Base Specification Revision 1.4**, 10 June 2019: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf>
- NVM Express, **Changes in NVMe Revision 1.4**: <https://nvmexpress.org/changes-in-nvme-revision-1-4/>
- NVM Express, **Specification Archives**: <https://nvmexpress.org/nvm-express-specification-archives/>

### Namespace Management selects an NVM Set; it does not provision an Endurance Group

The bounded Namespace Management path adds an important lifecycle distinction. Revision 1.4 §4.9 says each NVM Set is associated with exactly one Endurance Group and that namespace creation supplies the target **NVM Set Identifier**. Section 5.20 Figure 262 confirms `NVMSETID` is host-specified during create; it does **not** list `ENDGID` as a host-specified create field. Figure 245 separately reports both `NVMSETID` and `ENDGID` for an existing namespace.

Namespace deletion likewise removes the namespace and detaches it from controllers; the command does not specify Endurance Group deletion or reset of group-lifetime endurance information. Therefore this case closes one narrow 1.4 boundary:

> **namespace lifecycle != automatically Endurance Group lifecycle.**

and:

> **reported Endurance Group association != direct Endurance Group provisioning through Namespace Management.**

The fuller source record and stop conditions are in [`../evidence/120-nvme14-2019-namespace-group-association-deepening.md`](../evidence/120-nvme14-2019-namespace-group-association-deepening.md).

### Revision 2.0 / TP4052c adds the previously missing interoperable lifecycle-management layer

The later deepening in [`../evidence/120-nvme-2019-2021-endurance-group-lifecycle-management-deepening.md`](../evidence/120-nvme-2019-2021-endurance-group-lifecycle-management-deepening.md) closes the bounded provisioning question without projecting later semantics backward into 1.4.

NVM Express development material dated 11 June 2019 already distinguished a fixed Media Unit Endurance Group Management approach from **Capacity Endurance Group Management**, the latter intended to let storage systems dynamically create Endurance Groups and NVM Sets. The same slides show draft create/delete operations, but they contain development placeholders and an operation layout that differs from the final standard; they are therefore evidence of public design direction, not the ratified command contract.

**NVM Express Base Specification Revision 2.0**, dated 13 May 2021, incorporates **TP4052c**. NVM Express's official Revision-2.0 change document names **NVM Set and Endurance Group Management**, describes it as an interface for interoperable management of the two entities, and maps that feature to TP4052c.

Revision 2.0 §5.3 then adds the **Capacity Management** command with separate operations for:

- selecting a Capacity Configuration;
- creating an Endurance Group;
- deleting an Endurance Group;
- creating an NVM Set;
- deleting an NVM Set.

Deleting an Endurance Group deletes all NVM Sets and namespaces contained by that group. Creating a group selects a non-zero Endurance Group Identifier not currently assigned to an existing group in the relevant Domain and allocates Media Units or NVM capacity according to the supported regime.

The resulting chronology is now bounded as:

```text
NVMe 1.4
    Endurance Group / NVM Set scope, association, reporting
    != interoperable group provisioning through Namespace Management

June 2019 development-stage NVM Express material
    fixed-configuration concept
    + dynamic capacity-management concept

NVMe 2.0 / TP4052c
    interoperable Capacity Management lifecycle interface
```

This is a proposal-layer refinement, not an invention-priority claim.

### Revision 2.0 distinguishes fixed and variable group-management regimes

Revision 2.0 §8.3.2 **Fixed Capacity Management** lets the host select from supported capacity configurations; successful selection allocates Media Units into Endurance Groups and NVM Sets according to the selected complete configuration.

Revision 2.0 §8.3.3 **Variable Capacity Management** explicitly allows dynamic creation and deletion of Endurance Groups and NVM Sets. Its typical allocation order is:

```text
Domain capacity
    -> Endurance Group
    -> NVM Set
    -> namespace
```

with the typical deallocation order reversed.

The interface can therefore expose multiple management regimes over the same broad entity vocabulary. `Endurance Group support` must not be silently equated with `dynamic Endurance Group creation/deletion support`.

### Group creation and group deletion have different transition semantics in Revision 2.0

Revision 2.0 §8.3.1 specifies the exposed updates for **Endurance Group creation** as an **atomic operation**: the relevant unallocated-capacity state is changed and the new group identifier is added to the Endurance Group List.

For **Endurance Group deletion**, the specification instead defines a sequence:

1. remove the group identifier from the Endurance Group List;
2. clear the deleted group identifier from applicable Media Unit Status descriptors;
3. delete every NVM Set in the group;
4. return the former group capacity to the Domain's unallocated pool.

If an entity modified by this sequence is accessed after the sequence has started but before it has completed, the result is specified as indeterminate.

Therefore:

> **group creation transition semantics != group deletion transition semantics.**

This is not, by itself, a statement about arbitrary power-failure/crash atomicity. The inspected clause defines the normative visible transition/observation contract, not every hidden controller persistence boundary.

### Endurance Group deletion is not NVMe sanitization

The Capacity Management delete path retires the group identity, cascades to contained NVM Sets/namespaces, clears specified membership fields, and makes capacity available for later allocation. It does **not** state that all former NAND embodiments are physically erased, cryptographically erased, or independently verified as forgotten.

Therefore:

> **Endurance Group deletion != physical-media sanitization.**

and:

> **capacity returned to an unallocated pool != physical endurance restored or prior media state proved unrecoverable.**

NVMe has separate sanitize semantics; the case keeps lifecycle retirement and media forgetting separate.

### NVM Set and Endurance Group are different scopes

Revision 1.4 §4.9 defines an **NVM Set** as a collection of NVM separate logically and potentially physically from NVM in other NVM Sets. One or more namespaces may be created within an NVM Set, and a namespace is wholly contained within one NVM Set.

The same section states:

- every NVM Set has an NVM Set Identifier;
- each NVM Set is associated with **exactly one Endurance Group**.

Section 8.17 then defines the larger endurance relation:

- endurance may be managed within one NVM Set;
- or endurance may be managed across a collection of NVM Sets;
- if multiple NVM Sets share one Endurance Group Identifier, endurance is managed across that collection;
- if only one NVM Set belongs to the Endurance Group, endurance is managed locally to that NVM Set.

The standard's own example puts NVM Sets A and B together in one Endurance Group Y while NVM Set C alone forms Endurance Group Z.

The historical interface relation is therefore:

```text
namespace
    -> exactly one NVM Set
    -> exactly one Endurance Group for that NVM Set

while

one Endurance Group
    -> may govern endurance across multiple NVM Sets
```

The arrows are a compact **engineering reconstruction of the normative containment/association rules**, not a claim that the standard physically lays NAND out in this hierarchy.

### The Endurance Group Information log is explicitly group-scoped

Revision 1.4 §5.14.1.9 defines **Endurance Group Information (Log Identifier 09h)**. The specification says:

- the log provides endurance information based on the Endurance Group;
- an Endurance Group consists of zero or more NVM Sets;
- the information provided is **over the life of the Endurance Group**;
- the Endurance Group Identifier is supplied as the log-specific identifier.

This matters because the scope is neither simply `namespace` nor simply `whole controller`. A host may address one group and obtain health/endurance information accumulated for that group.

The `zero or more NVM Sets` wording also prevents a stronger identity claim:

> **Endurance Group identity is not definitionally identical to one currently populated namespace or one currently populated NVM Set.**

Revision 2.0 now establishes explicit creation/deletion of that wider entity, but field-specific initialization/reset behavior across deletion and any later identifier reuse remains evidence debt rather than being guessed from the word `life`.

### One group log contains different temporal semantics

The first byte of the Endurance Group Information log is `Critical Warning`. Revision 1.4 explicitly says these bits represent the **current associated state** and are **not persistent**.

The same log then contains quantities with longer or cumulative semantics, including:

- `Available Spare` for the Endurance Group;
- `Percentage Used`, a vendor-specific estimate based on actual usage and predicted NVM life;
- `Endurance Estimate`, an estimate of total bytes that may be written over the lifetime of the Endurance Group assuming write amplification of one;
- total `Data Units Read` and `Data Units Written` for the Endurance Group;
- `Media Units Written` for the Endurance Group;
- host read/write command counts;
- media/data-integrity error count;
- number of Error Information log entries for the group, with that field described in terms of the life of the controller.

The specification therefore blocks the shortcut:

> **one log page ≠ one temporal lifetime class.**

The page mixes a current nonpersistent warning surface with cumulative or lifetime-qualified measurements/estimates. Case 66 already showed a related mixed-lifetime problem in NVMe diagnostic history; Case 120 adds the **Endurance Group scope** rather than treating all such state as controller-global.

### Host writes and media writes are separately exposed

Revision 1.4 makes an especially useful distinction:

- `Data Units Written` counts total data bytes written to the Endurance Group but excludes controller writes due to internal operations such as garbage collection;
- `Media Units Written` includes **both host and controller writes**, with garbage collection given as an example.

This is direct primary evidence that the host-visible mutation stream and the internal media-write stream can diverge.

The standard does not disclose the controller's exact Flash Translation Layer or erase/program schedule. It exposes a difference in accounting scope while leaving the implementation underneath abstract.

### NVMe itself explicitly places wear leveling below the interface

Revision 1.4 §1.3 says the interface is specified **above** nonvolatile-memory management such as wear leveling and that erases and other NAND-management tasks are abstracted.

That statement is a central guardrail for this case. Endurance Groups make an endurance-management scope visible to the host, but they do not thereby reveal the exact physical entities over which wear leveling, garbage collection, bad-block replacement, or erase scheduling occurs.

Therefore:

> **host-visible endurance-management scope ≠ disclosed physical wear-leveling geometry.**

### Endurance warnings have their own event lifecycle

Section 8.17.1 allows the host to configure asynchronous events per Endurance Group. The host can read an Endurance Group Event Aggregate log to discover which groups have outstanding events and then read a specific group's Endurance Group Information log to determine the warning state.

A successful group-log read with `Retain Asynchronous Event = 0` clears the events for that group.

This adds another state class:

```text
underlying cumulative/estimated endurance state
    != current Critical Warning state
    != outstanding event-notification state
```

Clearing notification state is not evidence that spare capacity, usage counters, or physical wear have been reset.

---

## Retained states and relations

The bounded NVMe 1.4 plus Revision-2.0 lifecycle regime contains at least these different states:

1. **namespace payload** — logical user data;
2. **namespace identity** — host-visible namespace identity;
3. **NVM Set identity and membership** — the set containing that namespace;
4. **Endurance Group identity / active existence** — a wider management entity;
5. **NVM Set → Endurance Group association** — the group governing the set's endurance-management scope;
6. **Endurance Group List membership** — host-visible evidence that a group currently exists in the 2.0 management regime;
7. **Domain unallocated capacity** — capacity available for creation/allocation;
8. **group total/unallocated capacity**;
9. **Media Unit assignment**, when that management regime is supported;
10. **group-level available-spare state**;
11. **group-level percentage-used estimate**;
12. **group-level endurance estimate**;
13. **group-level host data-unit counters**;
14. **group-level media-write counters** that include controller work;
15. **current Endurance Group critical-warning state**, explicitly nonpersistent in the 1.4 log semantics;
16. **outstanding asynchronous-event state** for the group;
17. **multi-entity lifecycle transition state** while a 2.0 delete sequence is in progress;
18. **underlying controller/NAND management state** — wear-leveling, garbage collection, mapping, erase/program bookkeeping, which the NVMe interface does not specify.

Only item 1 is the application payload. Items 3–17 are host-visible or host-relevant organizational/health/control relations. Item 18 may be constitutive of actual endurance but is deliberately not reconstructed from the interface fields alone.

---

## Engineering reconstruction

### Namespace identity is narrower than endurance-history scope

A namespace is wholly contained in one NVM Set. An Endurance Group may contain several NVM Sets. Therefore health/endurance history can be accumulated over a scope that contains multiple namespaces even though each namespace remains individually addressable.

So:

> **namespace identity ≠ endurance-history scope.**

and:

> **per-namespace logical isolation ≠ per-namespace endurance isolation.**

The second statement is bounded carefully. It does not say every device physically shares wear across every namespace; it says the standard allows endurance management for several NVM Sets to be grouped under one Endurance Group.

### NVM Set separation does not imply independent endurance management

The standard calls NVM Sets logically and potentially physically separate. Yet two or more NVM Sets may share an Endurance Group and have endurance managed across the collection.

Therefore:

> **NVM Set separation ≠ Endurance Group separation.**

A useful hierarchy emerges:

```text
logical service partition
    may be finer than
endurance-management partition
```

This is a functional relation inside one normative standard, not a claim about hidden silicon topology.

### Namespace lifecycle is not Endurance Group lifecycle

The 1.4 Namespace Management evidence first made the scope difference operationally visible: create selects an NVM Set, not a new Endurance Group, and delete retires the namespace without defining group destruction.

Revision 2.0 now adds the missing positive lifecycle evidence by giving Endurance Groups and NVM Sets their own Capacity Management create/delete operations. The case can therefore distinguish more strongly:

> **namespace creation != Endurance Group creation**

> **namespace deletion != Endurance Group deletion**

> **host-selected `NVMSETID` in 1.4 Namespace Management != later 2.0 Endurance Group provisioning authority**

> **`ENDGIDMAX` != group-lifetime generation counter**

> **currently unassigned `ENDGID` != proven never-before-used identifier**

The hierarchy is now a lifecycle hierarchy, not merely an absence-of-semantics observation.

### Reportable scope is not the same as provisioning authority

Revision 1.4 could report the Endurance Group associated with a namespace and retrieve group-scoped information. Revision 2.0 adds interoperable group create/delete authority.

Therefore:

```text
scope exists and is reportable
    !=
host can provision/retire that scope through the same interface revision
```

This is a useful standards-history boundary: later control authority must not be projected backward simply because the object name already existed.

### Group retirement can cascade through logical identities without proving physical forgetting

Revision 2.0 Delete Endurance Group retires the group and its nested NVM Sets/namespaces and returns capacity to the Domain pool.

But:

> **administrative identity retirement != media sanitization.**

> **reusable capacity != erased remanent embodiment.**

> **unallocated capacity restored != physical endurance restored.**

This is a bounded functional comparison to mapped-Flash invalidation/reclamation and the erase/invalidation/sanitization synthesis, not evidence for a particular FTL implementation.

### Lifecycle transition semantics can be asymmetric

The 2.0 create path specifies a set of exposed updates as atomic. The delete path specifies a multi-step sequence and declares intermediate access indeterminate.

Therefore:

> **creation boundary != deletion boundary.**

Do not upgrade that into a universal crash-consistency statement. The standard text grounds the interface transition/observation contract; hidden persistence and arbitrary-power-loss outcomes still need separate evidence.

### Host workload and media work are different historical quantities

Because `Data Units Written` excludes internal controller writes while `Media Units Written` includes them, one user-visible workload history does not exhaust the physical write work performed on behalf of that workload.

Therefore:

> **host-written bytes ≠ media-written bytes.**

and:

> **logical mutation history ≠ complete media-maintenance history.**

Garbage collection is the standard's explicit example. The difference can be important for endurance because internal relocation consumes media-write work without corresponding one-for-one host writes.

This does not authorize a hidden-algorithm claim such as `Media Units Written difference = exact garbage-collection cost`: other controller writes may be included, and the standard does not disclose the full cause decomposition.

### `Endurance Estimate` is a model relation, not a guaranteed residual-physical-capacity counter

The standard defines `Endurance Estimate` assuming **write amplification = 1**. `Percentage Used` is separately vendor-specific and based on actual usage plus the manufacturer's prediction of NVM life; `100` may indicate estimated endurance consumed without necessarily indicating NVM failure.

Therefore:

> **endurance estimate ≠ deterministic failure clock.**

> **percentage used ≠ direct raw-cell wear measurement.**

> **100% estimated use ≠ proven device failure.**

The host obtains a model-derived service-health relation, not transparent access to every cell's P/E-cycle count or threshold-voltage margin.

### Group lifetime and controller lifetime must not be silently normalized

The Endurance Group Information log is generally described as providing information over the life of the Endurance Group. Yet `Number of Error Information Log Entries` is described as a count over the **life of the controller for the Endurance Group**.

Therefore:

> **`life of Endurance Group` ≠ automatically `life of controller` for every field.**

The standard itself uses different lifetime anchors within the same group-scoped structure. Revision 2.0 now supplies group creation/deletion, but the exact field-by-field initialization/reset behavior across that lifecycle remains open; it should not be guessed from the phrase `life of Endurance Group` alone.

### Current warning, outstanding event, and underlying wear are different states

A warning bit is current and nonpersistent. An event notification can be cleared by a qualifying log read. Neither transition says that the underlying spare pool or cumulative write history has been replenished/reset.

Thus:

> **warning cleared ≠ wear reversed.**

> **event acknowledged/cleared ≠ endurance history erased.**

> **current warning state ≠ cumulative group history.**

This is a useful counterexample to treating operational health telemetry as one homogeneous persistent record.

### Endurance Group identifier is an interface designation, not a physical erase-unit label

Section 8.17 gives Endurance Groups a 16-bit identifier and host-visible associations. Section 1.3 simultaneously keeps wear leveling and erase management below the interface.

Therefore:

> **Endurance Group Identifier ≠ physical die/channel/plane/block identifier.**

It may select an endurance-management and reporting domain without exposing the implementation geometry that realizes that domain.

This is analogous at a very high functional level to other repository cases where a stable designation selects a relation whose physical embodiment remains hidden. It is not an FTL genealogy claim.

---

## Historical record vs engineering reconstruction vs analogy

### Historical record (`H/P`)

- NVMe Revision 1.4 is dated 10 June 2019 and includes TP4018b/TP4050 among incorporated proposals;
- the official Revision-1.4 change page lists Endurance Groups as an optional new feature;
- each namespace is wholly contained in one NVM Set;
- each NVM Set is associated with exactly one Endurance Group;
- one Endurance Group may govern endurance across multiple NVM Sets;
- the Endurance Group Information log is group-scoped and described over the life of the group;
- Critical Warning bits are current and nonpersistent;
- host data-unit counts exclude internal controller writes while Media Units Written includes controller writes such as garbage collection;
- NVMe explicitly places wear leveling and NAND erase-management below the specified interface;
- NVM Express June-2019 development material publicly discusses fixed and dynamic Endurance Group management approaches but is not the final normative command contract;
- NVMe Revision 2.0 incorporates TP4052c, and the official change record maps it to interoperable NVM Set / Endurance Group Management;
- Revision 2.0 Capacity Management defines separate create/delete operations for Endurance Groups and NVM Sets;
- group deletion cascades to contained NVM Sets/namespaces and returns capacity;
- group creation's specified exposed updates are atomic, whereas group deletion is a sequence with indeterminate intermediate access.

### Engineering reconstruction (`E`)

From those records the repository can safely distinguish:

```text
namespace identity
    != NVM Set identity/membership
    != Endurance Group association
    != Endurance Group active existence
    != group-list membership
    != endurance-history scope
    != Domain/group capacity-allocation state
    != current warning state
    != outstanding event state
    != host-write history
    != media-write history
    != estimated life state
    != lifecycle-transition state
    != hidden physical wear-leveling state
```

### Functional analogy (`A`) only

- **Case 55** — both retain device-health/endurance information, but Case 55's foundational SMART/Health relation is controller-oriented while Case 120 isolates optional Endurance Group scope and its later lifecycle management.
- **Case 76** — both discuss endurance, but JESD218 qualification is a test/service-rating relation over workload, TBW, retention, UBER/FFR/capacity criteria; an NVMe Endurance Group log is live management/telemetry state for a named group.
- **Case 04** — Flash mapping/wear management can make host writes diverge from physical work, but NVMe deliberately abstracts the underlying FTL. Case 120 therefore uses Case 04 only as a lower-layer functional reminder, not as evidence of Endurance Group implementation.
- **Case 66** — both show mixed temporal semantics in NVMe logs, but PEL/Error Information concerns diagnostic history while Case 120 concerns a group-scoped endurance-management surface.
- **Synthesis 22** — the erase/invalidation/sanitization distinction is a useful boundary for 2.0 group deletion: retiring an administrative scope and returning capacity does not itself prove physical sanitization.

No analogy establishes implementation identity or genealogy.

---

## Prior-art / novelty boundary

### What Revision 1.4 can safely claim here

The official NVM Express change record supports this bounded claim:

> **By the ratified 10 June 2019 Revision 1.4, NVMe publicly specifies optional Endurance Groups that can scope endurance management across one or more NVM Sets and exposes a group-specific Endurance Group Information log.**

### What Revision 2.0 adds without rewriting the 1.4 history

The official 2.0 front matter and change record support a second bounded claim:

> **By Revision 2.0, TP4052c has added an interoperable NVM Set / Endurance Group management interface, including Capacity Management creation/deletion semantics and fixed versus variable capacity-management regimes.**

This does not mean TP4052c invented the Endurance Group concept. The safer proposal-layer sequence is:

```text
TP4018b / TP4050 -> NVMe 1.4 Endurance Group / NVM Set feature floor
TP4052c -> NVMe 2.0 interoperable lifecycle-management deepening
```

The original standalone TP bodies have not all been directly inspected, so exact internal proposal chronology remains open.

### What neither revision can claim here

Case 55 already establishes earlier NVMe retained SMART/Health state in the **2011 Revision 1.0** family. Therefore:

> **NVMe 1.4 Endurance Groups ≠ invention of retained storage-health history.**

Likewise, this slice has not established the invention priority of:

- spare pools;
- SSD/NAND wear leveling;
- endurance partitioning;
- storage resource pools;
- namespace/resource isolation;
- dynamic capacity-pool provisioning;
- over-provisioning;
- drive-health telemetry.

The 2019–2021 evidence is a **standard-specific feature/lifecycle chronology**, not a generic invention-priority proof.

---

## Philosophical / media-theoretical interpretation

Case 120 adds a bounded conceptual point without turning telemetry into a metaphor for memory:

> A storage system can retain **history about the consumption of its own future capacity to retain other states**, and that history can have an administratively defined scope different from the identity of any one payload object.

The Revision-2.0 lifecycle deepening adds one further constraint: **the history-bearing management scope can itself be created, nested, allocated, and deleted while the underlying physical media and their accumulated wear do not thereby cease to have a history.**

The interesting object is second-order. The bytes written by applications are one history; the media work needed to keep serving them is another; an Endurance Group accumulates/estimates information about that service capacity across a defined group of storage resources; the administrative identity of that group has its own lifecycle.

The philosophical claim must stop there. An Endurance Group is not automatically a Stieglerian tertiary retention, its identifier is not Heideggerian `Bestand`, and the wear history is not a transparent physical autobiography of the NAND. The normative interface deliberately abstracts the physical management beneath it.

A safer formulation is:

> **technical retention may depend on retained state about how much retention margin and maintenance work a resource population has already consumed, even when the physical work itself remains hidden below the interface and the management domain that reports it can later be administratively retired.**

---

## Counterexamples and limits

1. **Endurance Group support is optional.** Revision 1.4 does not make every conforming controller expose multiple groups, and Revision 2.0 dynamic lifecycle support has its own capability conditions.
2. **One namespace does not define one Endurance Group.** Multiple namespaces can sit in NVM Sets that share a group.
3. **One NVM Set does not prove one physical NAND partition.** The standard says logically and potentially physically separate.
4. **One Endurance Group does not disclose one wear-leveling pool implementation.** Wear leveling and erases are explicitly below the interface.
5. **`Data Units Written` does not equal physical media writes.** Internal controller writes are excluded from that field.
6. **`Media Units Written` does not reveal a complete causal breakdown.** Garbage collection is an example, not an exhaustive internal-work ledger.
7. **`Percentage Used = 100` does not necessarily mean failure.** The specification says so directly.
8. **`Endurance Estimate` is not an exact physical residual-life meter.** It is an estimate under a stated WAF=1 assumption.
9. **Current warning state is not persistent history.** The standard explicitly makes Critical Warning bits current and nonpersistent.
10. **Clearing an asynchronous event is not erasing wear.** Event lifecycle and endurance state are different relations.
11. **`life of Endurance Group` is not silently equated with `life of controller`.** The Error Information count field uses the latter wording within the same log page.
12. **2019 is not claimed as the invention date of endurance partitioning.** It is the checked public NVMe 1.4 feature floor.
13. **The June-2019 management slides are not the final Revision-2.0 command contract.** Their draft encoding/layout differs from the ratified interface.
14. **TP4052c is not treated as the invention of Endurance Groups.** It is the checked 2.0 management/lifecycle layer over a feature already present in 1.4.
15. **Delete Endurance Group is not Sanitize.** Cascading namespace/NVM-Set deletion and capacity return do not prove physical erase or crypto erase.
16. **Atomic create wording is not promoted into arbitrary power-fail atomicity for all hidden metadata.** The inspected text defines the specified transition, not every failure model.
17. **Deletion's sequenced transition does not itself determine every crash outcome.** Intermediate access is indeterminate; fault behavior still needs separate evidence.
18. **A currently unassigned `ENDGID` is not a generation number.** The evidence does not prove never-reuse or continuity on later reuse.
19. **Group deletion does not yet prove every endurance-history field's reset semantics.** Field-by-field initialization/reuse rules remain open.
20. **Group health is not payload history.** It qualifies future service margin without archiving application values or their mutation sequence.

---

## Related repositories

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — broader histories of SSD wear leveling, over-provisioning, internal resource pools, Flash-controller topology, and the proposal/committee genealogy around Endurance Group management belong there. Fresh searches found no dedicated NVMe Endurance Group / TP4052 case to reuse, so this repository keeps only the retention-specific scope/lifecycle relation.
- [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) — use its anti-anachronism rule: `second-order retention history`, `retention margin`, and the decomposition in this case are present engineering vocabulary, not terms attributed to the NVMe committee unless the source itself uses them.

---

## Evidence debt / future work

- inspect the original ratified texts/change histories of **TP4018b**, **TP4050**, and especially standalone **TP4052c** (plus any recoverable TP4052/a/b predecessors) to establish exact proposal/ballot chronology rather than relying only on integrated specifications and official change summaries;
- find earlier ATA/SCSI/vendor resource-domain or wear-pool lifecycle mechanisms to bound generic endurance-group prior art without forcing a genealogy;
- trace Revision 1.4a/1.4b/1.4c and later NVMe 2.0a–2.4 changes to Endurance Group lifecycle/reconfiguration semantics beyond the now-grounded 2.0 Capacity Management floor;
- determine exact initialization/reset behavior for every Endurance Group Information field across group creation/deletion rather than extrapolating from the broad `life of Endurance Group` wording;
- establish whether and how numerical Endurance Group identifiers are reused, and whether any other structure supplies a generation discriminator;
- establish controller-replacement, subsystem-reprovisioning, and reset/power-cycle behavior for fixed/variable capacity-management configuration;
- add a named controller/SSD that exposes multiple Endurance Groups and, if supported, Capacity Management create/delete; capture `nvme-cli` Identify/Get Log/management behavior;
- fault-inject reset or power loss during create/delete on a supporting device instead of assuming the normative atomic/sequenced wording closes the physical persistence model;
- compare group-scoped `Data Units Written` and `Media Units Written` under a controlled workload without assuming the difference is entirely garbage collection;
- correlate host-visible group telemetry with independent NAND/FTL instrumentation if an open controller or research SSD makes that possible;
- test asynchronous-event clearing separately from cumulative health counters on a named device;
- keep physical Flash retention/wear physics in the existing Flash/SSD cases and broader controller history in `computing-archaeology` rather than duplicating them here.

None of these debts invalidates the bounded 1.4 feature findings or the bounded 2.0 lifecycle-management deepening above.