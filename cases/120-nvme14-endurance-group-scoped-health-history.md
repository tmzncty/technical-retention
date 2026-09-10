# Case 120 — NVMe 1.4 Endurance Groups: Scoped Wear History, Mixed-Lifetime Health State, and Hidden Media Work

## Status

**`grounded`** — bounded to the ratified **NVM Express Base Specification Revision 1.4 (10 June 2019)** and NVM Express's own Revision-1.4 change record. The case establishes an optional host-visible hierarchy in which namespaces belong to NVM Sets, each NVM Set belongs to exactly one Endurance Group, and endurance may be managed either within one NVM Set or across several NVM Sets. It also separates group-lifetime cumulative/estimated health information from current nonpersistent warning state and separates host-written bytes from controller/media writes. The case does **not** infer a particular Flash Translation Layer, erase-unit layout, wear-leveling algorithm, physical NAND partition, or invention priority for endurance pooling.

Grounding records: [`../evidence/120-nvme14-2019-endurance-group-grounding.md`](../evidence/120-nvme14-2019-endurance-group-grounding.md) and [`../evidence/120-nvme14-2019-namespace-group-association-deepening.md`](../evidence/120-nvme14-2019-namespace-group-association-deepening.md).

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
- group-specific asynchronous warning/event handling.

This is deliberately **not**:

- a general history of SSD wear leveling;
- a claim that an Endurance Group is a physical NAND die/channel/plane/erase-block partition;
- a claim that every NVMe 1.4 device implements Endurance Groups;
- a claim that every field in the Endurance Group Information log has one identical reset/persistence rule;
- a claim that `Percentage Used = 100` means physical failure;
- a claim that host writes equal NAND program/erase work;
- a claim that NVMe 1.4 invented endurance partitioning, spare pools, wear domains, over-provisioning, or health telemetry.

Broader SSD/NAND controller architecture and wear-leveling genealogy belongs primarily in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) if developed there. A repository-tree search in this round found no dedicated `Endurance Group` / NVMe endurance-group case to reuse.

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

Namespace deletion likewise removes the namespace and detaches it from controllers; the command does not specify Endurance Group deletion or reset of group-lifetime endurance information. Therefore this case now closes one narrow negative boundary:

> **namespace lifecycle != automatically Endurance Group lifecycle.**

and:

> **reported Endurance Group association != direct Endurance Group provisioning through Namespace Management.**

The fuller source record and stop conditions are in [`../evidence/120-nvme14-2019-namespace-group-association-deepening.md`](../evidence/120-nvme14-2019-namespace-group-association-deepening.md). Actual Endurance Group provisioning/reuse, controller replacement, NVM Set reprovisioning, and named-device behavior remain open.

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

The exact creation/deletion/reconfiguration lifetime of Endurance Group identifiers is not reconstructed here; that remains evidence debt rather than being guessed from the zero-set allowance.

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

The bounded NVMe 1.4 regime contains at least these different states:

1. **namespace payload** — logical user data;
2. **namespace identity** — host-visible namespace identity;
3. **NVM Set membership** — the set containing that namespace;
4. **Endurance Group association** — the group governing the set's endurance-management scope;
5. **group-level available-spare state**;
6. **group-level percentage-used estimate**;
7. **group-level endurance estimate**;
8. **group-level host data-unit counters**;
9. **group-level media-write counters** that include controller work;
10. **current Endurance Group critical-warning state**, explicitly nonpersistent;
11. **outstanding asynchronous-event state** for the group;
12. **underlying controller/NAND management state** — wear-leveling, garbage collection, mapping, erase/program bookkeeping, which the NVMe interface does not specify.

Only item 1 is the application payload. Items 3–11 are host-visible organizational/health/control state. Item 12 may be constitutive of actual endurance but is deliberately not reconstructed from the interface fields alone.

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

Namespace Management makes the scope difference operationally visible: create selects an NVM Set, not a new Endurance Group, and delete retires the namespace without defining group destruction. The case can therefore distinguish:

> **namespace creation != Endurance Group creation**

> **namespace deletion != Endurance Group deletion**

> **host-selected `NVMSETID` != direct `ENDGID` provisioning in Namespace Management**

> **`ENDGIDMAX` != group-lifetime generation counter**

These are interface/lifetime boundaries, not claims that an Endurance Group necessarily survives every administrative operation. In particular, deleting all namespaces does not by itself prove either survival or destruction of every Endurance Group; the group-provisioning layer remains ungrounded here.

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

The standard itself uses different lifetime anchors within the same group-scoped structure. This case preserves that wording instead of inventing one universal reset epoch.

Revision 1.4 now closes one narrower point: ordinary Namespace Management create/delete does not itself define Endurance Group provisioning or history reset. Exact behavior under Endurance Group creation/deletion/recreation, controller replacement, NVM Set reprovisioning, subsystem reconfiguration, identifier reuse, or namespace migration between management domains remains open.

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
- NVMe explicitly places wear leveling and NAND erase-management below the specified interface.

### Engineering reconstruction (`E`)

From those records the repository can safely distinguish:

```text
namespace identity
    != NVM Set membership
    != Endurance Group association
    != endurance-history scope
    != current warning state
    != outstanding event state
    != host-write history
    != media-write history
    != estimated life state
    != hidden physical wear-leveling state
```

### Functional analogy (`A`) only

- **Case 55** — both retain device-health/endurance information, but Case 55's foundational SMART/Health relation is controller-oriented while Case 120 isolates optional Endurance Group scope and the NVM Set hierarchy introduced in Revision 1.4.
- **Case 76** — both discuss endurance, but JESD218 qualification is a test/service-rating relation over workload, TBW, retention, UBER/FFR/capacity criteria; an NVMe Endurance Group log is live management/telemetry state for a named group.
- **Case 04** — Flash mapping/wear management can make host writes diverge from physical work, but NVMe 1.4 deliberately abstracts the underlying FTL. Case 120 therefore uses Case 04 only as a lower-layer functional reminder, not as evidence of the Endurance Group implementation.
- **Case 66** — both show mixed temporal semantics in NVMe logs, but PEL/Error Information concerns diagnostic history while Case 120 concerns a group-scoped endurance-management surface.

No analogy establishes implementation identity or genealogy.

---

## Prior-art / novelty boundary

### What Revision 1.4 can safely claim here

The official NVM Express change record supports this bounded claim:

> **By the ratified 10 June 2019 Revision 1.4, NVMe publicly specifies optional Endurance Groups that can scope endurance management across one or more NVM Sets and exposes a group-specific Endurance Group Information log.**

### What it cannot claim

Case 55 already establishes earlier NVMe retained SMART/Health state in the **2011 Revision 1.0** family. Therefore:

> **NVMe 1.4 Endurance Groups ≠ invention of retained storage-health history.**

Likewise, this slice has not established the invention priority of:

- spare pools;
- SSD/NAND wear leveling;
- endurance partitioning;
- storage resource pools;
- namespace/resource isolation;
- over-provisioning;
- drive-health telemetry.

The 2019 evidence is a **standard-specific feature floor**, not an invention-priority proof. The original text/history of TP4018b and TP4050 and any earlier vendor/standards endurance-domain mechanisms remain open prior-art work.

---

## Philosophical / media-theoretical interpretation

Case 120 adds a bounded conceptual point without turning telemetry into a metaphor for memory:

> A storage system can retain **history about the consumption of its own future capacity to retain other states**, and that history can have an administratively defined scope different from the identity of any one payload object.

The interesting object is second-order. The bytes written by applications are one history; the media work needed to keep serving them is another; an Endurance Group accumulates/estimates information about that service capacity across a defined group of storage resources.

The philosophical claim must stop there. An Endurance Group is not automatically a Stieglerian tertiary retention, its identifier is not Heideggerian `Bestand`, and the wear history is not a transparent physical autobiography of the NAND. The normative interface deliberately abstracts the physical management beneath it.

A safer formulation is:

> **technical retention may depend on retained state about how much retention margin and maintenance work a resource population has already consumed, even when the physical work itself remains hidden below the interface.**

---

## Counterexamples and limits

1. **Endurance Group support is optional.** Revision 1.4 does not make every conforming controller expose multiple groups.
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
13. **The interface does not prove physical co-location or isolation.** Named logical/resource scopes are not forensic maps of NAND geometry.
14. **Group health is not payload history.** It qualifies future service margin without archiving application values or their mutation sequence.

---

## Related repositories

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — broader histories of SSD wear leveling, over-provisioning, internal resource pools, Flash-controller topology, and the pre-2019 genealogy of endurance isolation belong there. The current repository-tree check found no dedicated NVMe Endurance Group topic to reuse.
- [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) — use its anti-anachronism rule: `second-order retention history`, `retention margin`, and the decomposition in this case are present engineering vocabulary, not terms attributed to the NVMe committee unless the source itself uses them.

---

## Evidence debt / future work

- inspect the original ratified texts/change histories of **TP4018b** and **TP4050** to establish exact proposal chronology rather than relying only on the Revision-1.4 incorporation/change pages;
- find earlier ATA/SCSI/vendor resource-domain or wear-pool mechanisms to bound generic endurance-group prior art without forcing a genealogy;
- trace Revision 1.4a/1.4b/1.4c and NVMe 2.x changes to Endurance Group lifecycle/reconfiguration semantics;
- determine exact persistence/reset behavior for every Endurance Group Information field rather than extrapolating from the page's broad `life of Endurance Group` wording;
- establish how Endurance Group identifiers behave across administrative reconfiguration, controller replacement, namespace deletion/recreation, and subsystem reset;
- add a named controller/SSD that exposes multiple Endurance Groups and capture `nvme-cli` Identify/Get Log behavior;
- compare group-scoped `Data Units Written` and `Media Units Written` under a controlled workload without assuming the difference is entirely garbage collection;
- correlate host-visible group telemetry with independent NAND/FTL instrumentation if an open controller or research SSD makes that possible;
- test asynchronous-event clearing separately from cumulative health counters on a named device;
- keep physical Flash retention/wear physics in the existing Flash/SSD cases and broader controller history in `computing-archaeology` rather than duplicating them here.

None of these debts invalidates the bounded 2019 interface findings above.
