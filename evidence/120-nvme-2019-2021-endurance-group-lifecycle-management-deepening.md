# Evidence 120 Deepening — NVMe 2019–2021 Endurance Group Lifecycle / Capacity Management

## Status and bounded question

**`bounded deepening complete`** for one narrow lifecycle question left open by the original NVMe 1.4 Case 120:

> **When did the host-visible Endurance Group stop being only a reported/selected endurance-management scope and acquire an interoperable standard interface for creating and deleting that scope itself? What does that later interface say about nested NVM Sets, namespaces, capacity, and the transition between “group exists” and “group no longer exists”?**

The bounded answer is:

- NVMe 1.4 (10 June 2019) already standardized NVM Sets, Endurance Groups, group-scoped health/endurance reporting, and namespace-to-NVM-Set association, but the inspected Namespace Management path did **not** create or delete Endurance Groups;
- an NVM Express presentation on 11 June 2019 already discussed two prospective management regimes, including capacity-based dynamic creation/deletion for storage-system use, but that presentation was **development-stage explanatory material**, not the final normative contract;
- NVM Express Base Specification Revision 2.0, dated 13 May 2021 and publicly released in June 2021, incorporates **TP4052c**;
- NVM Express's official Revision-2.0 change record names **“NVM Set and Endurance Group Management”** as a new feature and maps it to TP4052c;
- Revision 2.0 adds the **Capacity Management** command and separately defines fixed-capacity configuration selection and variable-capacity dynamic creation/deletion;
- deleting an Endurance Group deletes the NVM Sets and namespaces contained by that group and returns capacity to the domain-level unallocated pool;
- group creation is specified as an atomic update of the relevant exposed configuration state, while group deletion is specified as a **sequence** whose intermediate observations are indeterminate;
- none of those lifecycle semantics is, by itself, evidence of NAND sanitization, secure erase, complete reset of every historical endurance counter, or power-fail atomicity of the whole deletion transition.

This closes the previously open **1.4 → 2.0 Endurance Group provisioning/lifecycle interface** seam. It does **not** close exact TP4052c ballot chronology, physical media behavior, identifier-reuse history, every counter-reset rule, named-device conformance, or later NVMe 2.x evolution.

---

## Sources and evidence classes

### H/P — ratified normative source

NVM Express, **NVM Express Base Specification Revision 2.0**, dated **13 May 2021**:

<https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-2_0-2021.06.02-Ratified-4.pdf>

Relevant anchors:

- title page and front matter: Revision 2.0 date and incorporated Technical Proposals, including **TP4052c**;
- §5.3, especially Figure 149, **Capacity Management** command operations;
- §5.3.1, **Media Unit Configuration Selection**;
- §5.3.2, **Endurance Group Operations**;
- §8.3.1, Capacity Management create/delete state transitions;
- §8.3.2, **Fixed Capacity Management**;
- §8.3.3, **Variable Capacity Management**.

Evidence class: **historical / normative primary (`H/P`)**.

### H/P — official revision-change map

NVM Express, **Changes in NVM Express Revision 2.0**:

<https://nvmexpress.org/wp-content/uploads/NVM-Express-Revision-2.0-Changes.pdf>

The official change record names **NVM Set and Endurance Group Management**, describes it as an interface for interoperable management of those entities, points to the relevant Base Specification 2.0 sections, and names **Technical Proposal 4052c**.

Evidence class: **historical / official primary (`H/P`)**.

This is sufficient to attribute the integrated 2.0 management feature to TP4052c at the official change-record level. The standalone TP4052c proposal body and ballot/change chronology were **not** directly inspected in this slice, so proposal-internal authorship, exact submission dates, and revision-to-revision wording remain open.

### H/P* — development-stage NVM Express presentation

Mark Carlson and John Kim, NVM Express webcast presentation, **“Powering the Data Center With NVM Express”**, 11 June 2019:

<https://nvmexpress.org/wp-content/uploads/June-2019-Powering-the-Data-Center-with-NVM-Express.pdf>

Relevant slides/pages:

- “Endurance Group Management” — two management methods;
- “Capacity Endurance Group Management” — dynamic creation of Endurance Groups and NVM Sets without requiring the host to understand underlying Media Units;
- “Storage Systems Users” — create/resize/delete requirements and the separate group/set operations;
- the draft command table for create/delete Endurance Group and create/delete NVM Set.

Evidence class: **manufacturer/standards-organization development-stage primary (`H/P*`)**.

The slides contain draft placeholders and an operation layout that is not identical to the final Revision-2.0 command table. They are therefore used to establish **public development direction in June 2019**, not final normative semantics.

### Related-repository check

Fresh code search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Endurance Group`, `TP4052`, and capacity-management combinations found no dedicated overlapping technical-history slice to reuse. Broader NVMe committee/proposal genealogy and SSD allocation architecture still belong primarily there if developed.

---

## Historical record

### 1. The 1.4 boundary was real: group association existed before an interoperable group-lifecycle command

Case 120's earlier 1.4 grounding and namespace-association deepening already establish:

```text
namespace create
    -> host supplies NVMSETID
    -> selected NVM Set has exactly one associated Endurance Group
    -> Identify Namespace reports NVMSETID + ENDGID
```

while ordinary Namespace Management did not expose a host-specified `ENDGID` creation field and namespace deletion did not specify Endurance Group deletion or group-history reset.

That earlier result should **not** be rewritten as “NVMe 1.4 had no Endurance Group lifecycle at all.” It establishes a narrower interface fact:

> **The checked 1.4 Namespace Management path could participate in an already existing Endurance Group association without being the interoperable command that provisions the group itself.**

The 2.0 evidence below adds the missing provisioning layer instead of retroactively projecting it into 1.4.

### 2. One day after the 1.4 ratification date, NVM Express publicly discussed two distinct management regimes

The NVM Express webcast presentation is dated **11 June 2019**, one day after the Revision-1.4 ratification date used by this repository.

Its “Endurance Group Management” slide separates:

1. **Media Unit Endurance Group Management**;
2. **Capacity Endurance Group Management**.

For the Media Unit approach, the presentation describes selection from a fixed set of complete configurations and says the selected configuration would *typically* persist for the lifetime of the NVM subsystem. It also says incremental configuration was not intended for that method and that changing configuration after media use was not supported in the described design direction.

The next slide gives the contrasting capacity-based idea:

> systems dynamically create Endurance Groups and NVM Sets by specifying capacity without needing to understand the underlying Media Units.

The important historical point is not the exact phrase `lifetime of the NVM subsystem` as a universal standard guarantee. This is a presentation-stage statement about one method under development.

The safe chronology is:

```text
NVMe 1.4 ratified feature floor
    -> Endurance Group / NVM Set scope exists

June 2019 NVM Express public development material
    -> fixed-configuration management concept
    + dynamic capacity-based lifecycle concept

NVMe 2.0 / TP4052c integration
    -> interoperable normative management interface
```

This prevents a common chronology error: **the later 2.0 lifecycle command should not be projected backward into the ratified 1.4 Namespace Management interface merely because the design was already being discussed publicly in June 2019.**

### 3. The June 2019 storage-system use case explicitly asks for creation, resizing, and deletion

The presentation's “Storage Systems Users” slide states a need to **create, resize and delete Endurance Groups within a Domain** and describes capacity as drawn from the Domain. It calls for separate operations to create Endurance Groups and NVM Sets and says group deletion also deletes contained NVM Sets and namespaces.

The following draft command table includes operations corresponding to:

- selecting/releasing a media-unit configuration;
- creating/deleting an Endurance Group;
- creating/deleting an NVM Set.

The draft operation values/layout differ from the final Revision-2.0 Figure 149. That difference is useful evidence of an evolving proposal rather than a reason to normalize the documents silently.

Therefore:

> **public draft interface != ratified command encoding**.

The presentation establishes requirement/design direction; the 2021 specification establishes the normative contract used below.

### 4. Revision 2.0 officially maps interoperable NVM Set / Endurance Group management to TP4052c

The Revision-2.0 front matter states that Base Specification 2.0 incorporates Revision 1.4 plus a list of ECNs and Technical Proposals that includes **TP4052c**.

NVM Express's official 2.0 change document then names the new feature:

> **NVM Set and Endurance Group Management**

and describes it as an interface for interoperable management of Endurance Groups and NVM Sets. The same entry cites Base Specification sections including §5.3 and §8.3 and names **TP4052c**.

This supports a bounded proposal-layer distinction:

```text
TP4018b / TP4050 in NVMe 1.4
    -> Endurance Group / NVM Set feature family and reporting/association floor

TP4052c integrated in NVMe 2.0
    -> interoperable management / lifecycle interface
```

This is **not** a claim that TP4052c invented Endurance Groups. The group concept is already present in the prior ratified revision.

### 5. Revision 2.0 Capacity Management gives group and set lifecycles separate command operations

Base Specification 2.0 §5.3 Figure 149 defines the Capacity Management command. Its operations include:

- Select Capacity Configuration;
- Create Endurance Group;
- Delete Endurance Group;
- Create NVM Set;
- Delete NVM Set.

For **Delete Endurance Group**, the command description says the specified Endurance Group is deleted and **all namespaces and NVM Sets contained by the Endurance Group are deleted**.

For **Delete NVM Set**, the command description separately says the specified NVM Set is deleted and all namespaces in that NVM Set are deleted.

This final normative separation matters:

```text
namespace deletion
    != NVM Set deletion
    != Endurance Group deletion
```

The objects are nested, but their lifecycle operations are not collapsed into one generic `delete storage object` action.

A wider-scope delete can cascade downward; a narrower delete is not thereby the same wider-scope operation.

### 6. Creating an Endurance Group allocates a currently unassigned identifier and capacity

Revision 2.0 §5.3.2 says that for **Create Endurance Group**, the controller selects a **non-zero Endurance Group Identifier not assigned to an existing Endurance Group** in the specified Domain. If no non-zero unassigned identifier is available, the command aborts with Identifier Unavailable.

Depending on support, the controller then selects Media Units or NVM capacity from the Domain for allocation to the new group.

This establishes a host-visible transition stronger than 1.4's reported association:

```text
currently unassigned group identifier
    + available domain capacity
    -> newly existing Endurance Group
    -> group identifier returned to host
```

It does **not** establish a generation counter or permanent never-reuse rule. “Not assigned to an existing Endurance Group” is a current-allocation predicate, not historical uniqueness evidence.

Therefore:

> **currently unassigned identifier != never-before-used identifier**.

No claim about actual identifier reuse is made here without an explicit reuse trace or rule.

### 7. Fixed configuration selection can create a complete group/set configuration

Revision 2.0 §5.3.1 defines **Media Unit Configuration Selection**. When a selected configuration is applied from the Supported Capacity Configuration List, the controller creates an Endurance Group for each Endurance Group Configuration Descriptor and creates the specified NVM Sets in those groups.

If the Select Capacity Configuration operation is issued with the configuration identifier cleared to zero, the controller clears the configuration by performing a sequence that includes:

1. deleting all namespaces in the Domain;
2. deleting all NVM Sets in the Domain;
3. deleting all Endurance Groups in the Domain;
4. clearing the Selected Configuration field in the Media Unit Status log.

This is the ratified fixed-configuration counterpart to the June-2019 presentation's “complete configuration” concept.

The final specification should be used for normative behavior. The presentation's claim that one selected configuration would *typically* last for the subsystem lifetime remains historical design commentary, not an immutable 2.0 lifetime rule.

### 8. Revision 2.0 explicitly distinguishes Fixed and Variable Capacity Management

Section 8.3.2 defines **Fixed Capacity Management**. A supporting host selects a supported capacity configuration and, after successful completion, each Media Unit is allocated to one Endurance Group and one NVM Set.

Section 8.3.3 defines **Variable Capacity Management** and states that it allows the **dynamic creation and deletion of Endurance Groups and NVM Sets**. A controller supporting this mode shall support Create Endurance Group and may support Delete Endurance Group; if it supports NVM Sets it shall support Create NVM Set and may support Delete NVM Set.

This blocks a second shortcut:

> **Endurance Group management != one universal reconfiguration regime.**

The standard exposes at least a fixed-configuration regime and a variable dynamic-allocation regime. They have related objects but different host control surfaces.

### 9. Allocation and deallocation order makes the scope hierarchy operational

Revision 2.0 §8.3.3 gives a typical variable-capacity allocation sequence:

```text
Domain capacity
    -> create Endurance Group
    -> create NVM Set inside the group
    -> create namespace inside the NVM Set
```

and the corresponding typical deallocation sequence:

```text
delete namespace
    -> delete NVM Set
    -> delete Endurance Group
```

It also says that if a Domain lacks sufficient unallocated capacity for a new Endurance Group, the host may delete one or more groups and create a new group using some or all of the resulting available capacity.

That wording makes the hierarchy more than a reporting taxonomy. It is a capacity-allocation lifecycle.

Yet the relation remains interface-level. It does not reveal which NAND dies, channels, planes, blocks, spare pools, or FTL regions physically implement a particular group.

### 10. Group creation and group deletion have different transition semantics

Revision 2.0 §8.3.1 is especially important for a retention analysis.

For **Endurance Group creation**, the controller performs the relevant exposed updates **as an atomic operation**:

- change Unallocated NVM Capacity according to the requested capacity/allocation rule;
- add the Endurance Group Identifier to the Endurance Group List.

For **Endurance Group deletion**, the specification instead gives a **sequence**:

1. remove the Endurance Group Identifier from the Endurance Group List;
2. if Media Unit Status is supported, clear the deleted group's identifier from Media Unit Status descriptors that referred to it;
3. delete every NVM Set in the Endurance Group;
4. increase Unallocated NVM Capacity by the group's former total capacity.

The specification then says that if an entity modified by that sequence is accessed after the sequence begins and before it completes, the result is **indeterminate**.

So the ratified interface itself blocks the simplification:

```text
create transition semantics
    == delete transition semantics
```

They are not specified the same way.

A bounded retention result follows:

> **a control object can have a normatively atomic creation boundary while its retirement is a multi-entity transition whose intermediate visibility is not a valid stable interpretation point.**

That is an engineering relation grounded in the specification wording. It is **not** evidence that deletion is or is not power-fail atomic, because the inspected clause does not by itself define every reset/power-loss outcome during that sequence.

### 11. Deletion retires the management entity and returns capacity; it does not specify secure media erasure

Deleting an Endurance Group:

- removes the group identifier from the active group list;
- clears related assignment fields where specified;
- deletes contained NVM Sets/namespaces;
- returns capacity to the Domain's unallocated pool.

Nothing in the inspected Capacity Management clauses says that this operation is a **Sanitize** operation, that all old NAND embodiments are physically erased, that all remanent copies are unrecoverable, or that crypto keys are destroyed.

Therefore:

> **Endurance Group deletion != media sanitization.**

and:

> **capacity becomes available for reuse != previous physical embodiments proved forgotten.**

The NVMe specification has separate sanitize semantics. This slice does not collapse lifecycle deletion into them.

### 12. Deleting an Endurance Group is not yet evidence for a complete “history reset” rule

Case 120's original group information log uses lifetime-qualified language for several fields. The new 2.0 lifecycle interface now tells us how a group can be created/deleted, but the inspected clauses do not state a general rule such as:

```text
Delete Endurance Group
    -> every Endurance Group Information counter is securely zeroized
    -> any future reuse of the numerical ENDGID creates a provably distinct generation
```

The group entity is deleted and capacity is returned, but **counter-reset semantics and identifier-generation semantics remain separate evidence questions**.

It is tempting to infer that a newly created group necessarily begins all counters at zero because it is “new.” This file does not make that inference without a field-specific normative clause or device trace.

---

## Retained-state decomposition after the 2.0 deepening

The Case 120 state map now requires at least these layers to remain separate:

1. **namespace payload** — application data;
2. **namespace identity**;
3. **NVM Set identity**;
4. **Endurance Group identity / active existence**;
5. **namespace → NVM Set membership**;
6. **NVM Set → Endurance Group membership**;
7. **Endurance Group List membership** — host-visible evidence that the group currently exists;
8. **Domain unallocated capacity**;
9. **Endurance Group total/unallocated capacity**;
10. **Media Unit assignment**, if that management regime is supported;
11. **group-level health/endurance counters and estimates**;
12. **current Critical Warning state**;
13. **outstanding event-notification state**;
14. **underlying wear-leveling / GC / mapping / erase state**, kept below the NVMe abstraction;
15. **transition state while a multi-object delete sequence is in progress**.

The new evidence adds items 4, 7–10, and 15 as lifecycle/configuration relations that cannot be inferred from namespace identity alone.

---

## Engineering reconstruction (`E`)

### Existence/reporting of a scope is different from authority to provision that scope

NVMe 1.4 already exposed group identity and group-scoped health. Revision 2.0 adds an interoperable management path for creating/deleting the group.

Therefore:

```text
scope is reportable
    != scope is host-provisionable through this interface

association is visible
    != association's wider container can be created/deleted by the same older command
```

The distinction is historically useful because it prevents later administrative powers from being projected backward into an earlier revision merely because the object name already existed.

### A history-bearing management domain can itself have a lifecycle

Case 120's original conceptual interest was second-order: an Endurance Group retains state about consumption of future retention capacity.

Revision 2.0 adds a further engineering layer:

> **the scope to which that history belongs can itself become an explicitly created/deleted management entity.**

Thus the repository should distinguish:

```text
payload lifetime
    != namespace lifetime
    != NVM Set lifetime
    != Endurance Group lifetime
    != lifetime of physical media wear
```

Deleting the administrative/history-bearing scope does not make accumulated physical wear disappear.

### Cascading deletion is authority over membership, not proof of physical forgetting

The group delete operation has authority to retire nested NVM Sets and namespaces. That makes it a strong **administrative currentness/identity transition**.

But:

```text
nested logical identities deleted
    != physical NAND state erased
    != controller internal stale embodiments sanitized
```

This is a bounded functional comparison to mapped-Flash invalidation/reclamation and the repository's erase/invalidation/sanitization synthesis, not evidence that the implementations are the same.

### Capacity return is not endurance restoration

When group deletion returns capacity to the unallocated pool, the capacity becomes administratively available for later allocation. Nothing in the inspected clauses says the physical cells have had their wear reversed.

Therefore:

> **unallocated capacity restored != physical endurance restored.**

A later group may receive capacity that comes from a media population with prior wear history; whether and how the standard exposes continuity of that history is a separate question.

### Atomic creation does not imply crash-atomic lifecycle management

The specification's phrase “as an atomic operation” for creation is a direct normative property of the listed exposed updates. The delete path is separately a sequence with indeterminate access during transition.

Do not expand that into:

- proof of persistence after arbitrary power loss at every internal point;
- proof that a successfully completed command has updated every lower-layer nonvolatile structure atomically;
- proof that all counters/history are transactional with the list update;
- proof that delete is non-atomic with respect to every possible failure model.

The safe statement is only:

> **the normative interface gives creation and deletion different transition/observation contracts.**

### Identifier availability is current allocation state, not historical identity

The create path chooses an identifier not assigned to an existing group. The rule does not define a generation number.

So:

```text
ENDGID = 7 is available now
    != ENDGID 7 has never existed before

ENDGID = 7 appears later
    != automatically same historical Endurance Group as an earlier ENDGID 7
```

The second line is a caution, not a claim that actual reuse occurs. A trace or explicit rule is still needed.

---

## Functional analogies (`A`) and boundaries

### Case 04 — mapped Flash

Both cases distinguish a stable/host-visible management relation from hidden physical NAND work. The analogy stops there. Endurance Group membership is not an FTL logical-to-physical map.

### Case 55 / 66 — NVMe health and event history

Case 55 and Case 66 show retained diagnostic/health history and mixed-lifetime logging. Case 120 adds a **management scope whose own existence and capacity allocation can be changed**. The comparison does not imply that PEL and Endurance Group Information share one reset or persistence mechanism.

### Synthesis 22 — erase / invalidation / sanitization

Endurance Group deletion is another strong counterexample to `logical/admin deletion = sanitization`. The Capacity Management interface retires names/membership and returns allocatable capacity, while sanitize remains a separate command family.

This is a functional comparison, not a claim that Endurance Group deletion uses a particular FTL invalidation implementation.

### Case 129 — asynchronous destroy / compatibility state

Only a narrow analogy is useful: a high-level administrative transition may have an internal multi-step lifecycle rather than one instant. OpenZFS async destroy and NVMe Endurance Group deletion are otherwise unrelated mechanisms with different historical vocabularies and failure contracts.

---

## Prior-art / proposal boundary

The new evidence sharpens the NVMe-local chronology without making a generic priority claim:

```text
10 Jun 2019 — NVMe 1.4 ratification
    Endurance Groups / NVM Sets standardized as optional feature family
    group scope/reporting/association exists

11 Jun 2019 — NVM Express webcast
    public design material discusses fixed Media Unit management
    + dynamic Capacity Endurance Group management
    + create/delete group/set direction

13 May 2021 — NVMe Base Specification Revision 2.0 document date
    incorporates TP4052c
    ratified Capacity Management interface

NVMe official 2.0 change record
    TP4052c -> interoperable NVM Set / Endurance Group Management
```

This supports:

> **TP4052c is a management/lifecycle deepening of an already existing NVMe Endurance Group feature, not the first appearance of the Endurance Group concept in NVMe.**

It does **not** establish:

- exact TP4052c submission/approval/publication dates;
- exact text of intermediate TP4052 / a / b revisions;
- who first proposed the management model;
- invention priority for dynamic storage-pool partitioning;
- a direct genealogy from older SCSI/ATA/vendor pool-management mechanisms.

Those remain broader standards-history work, preferably coordinated with `computing-archaeology`.

---

## Narrow philosophical interpretation (`I`)

A bounded conceptual point survives the mechanism:

> **A retention system can retain history about the wear and service margin of a resource domain, while the administrative identity of that history-bearing domain is itself created, nested, reallocated, and deleted.**

This complicates any simple equation of “the thing that persists” with one object name. The physical media can outlive a group identifier; accumulated physical wear can outlive one administrative allocation; namespace identities can disappear before the wider group; and the group itself can disappear before its former capacity is reused.

The interpretation stops there. An Endurance Group is not automatically a philosophical archive or subject, and deleting it is not metaphysical forgetting. The evidence is an engineering lifecycle with explicit scope and authority transitions.

---

## Negative controls / stop conditions

This deepening does **not** claim that:

1. NVMe 1.4 already contained the final 2.0 Capacity Management command merely because NVM Express discussed it in June 2019.
2. The June-2019 slide command encodings are final normative encodings; the final Figure 149 differs.
3. TP4052c invented Endurance Groups; the feature existed in Revision 1.4.
4. Create Endurance Group reveals exact NAND allocation geometry.
5. Delete Endurance Group performs secure erase, sanitize, key destruction, or physical block erase.
6. Returning capacity to `UNVMCAP` restores physical media endurance.
7. An atomic create transition proves arbitrary power-fail/crash atomicity for all hidden controller metadata.
8. The deletion sequence's indeterminate intermediate reads prove a particular power-failure result.
9. Deleting a group necessarily resets every lifetime counter in every later group that may receive the capacity.
10. An available `ENDGID` value is a never-before-used globally unique generation.
11. A later reuse of the same numeric identifier, if it occurs, automatically means continuity of the old Endurance Group.
12. Fixed and Variable Capacity Management have identical lifecycle contracts.
13. Namespace deletion and Endurance Group deletion are interchangeable operations.
14. Similar pool-management concepts in older storage systems establish direct genealogy into NVMe without actor/source evidence.

---

## Result

The bounded Case-120 lifecycle deepening establishes the following transition model:

```text
NVMe 1.4
    Endurance Group exists as host-visible endurance-management / reporting scope
    namespace creation selects NVM Set
    namespace reports associated ENDGID
    ordinary Namespace Management does not provision Endurance Group

June 2019 development-stage material
    fixed Media Unit configuration concept
        vs
    capacity-based dynamic group/set lifecycle concept

NVMe 2.0 / TP4052c
    Capacity Management becomes interoperable normative interface

variable-capacity allocation:
    Domain unallocated capacity
        -> Create Endurance Group
        -> active ENDGID + group-list membership
        -> Create NVM Set
        -> Create namespace

variable-capacity deallocation:
    namespace delete
        -> NVM Set delete
        -> Endurance Group delete
        -> group removed from active list
        -> capacity returns to Domain pool

but:
    administrative deletion
        != sanitization
        != physical wear reversal
        != demonstrated reset of every historical field

and:
    atomic create update
        != same transition contract as
    sequenced delete update
```

This closes the original **“how is an Endurance Group itself provisioned/deleted after 1.4?”** debt at the Revision-2.0 interface level.

---

## Remaining work

- directly inspect the standalone **TP4052c** proposal text and, if available, TP4052/a/b predecessors plus ballot/change history;
- inspect TP4018b and TP4050 themselves to refine the 1.4 proposal layering rather than relying on official change summaries;
- determine field-specific Endurance Group Information initialization/reset semantics on group creation/deletion;
- determine whether and under what rules numerical `ENDGID` values are reused, and whether any generation discriminator exists elsewhere;
- test a named multi-group controller with `nvme-cli` or equivalent tooling, including group create/delete if hardware actually supports Variable Capacity Management;
- fault-inject reset/power loss during create/delete on a device that exposes the feature, without assuming normative “atomic operation” wording closes the failure model;
- trace NVMe 2.0a–2.4 changes to Endurance Group management without collapsing later revisions into the 2.0 contract;
- establish any earlier SCSI/ATA/vendor storage-pool lifecycle prior art only with direct period sources and without inventing a genealogy;
- keep physical NAND wear-leveling/allocation history in `computing-archaeology` or lower-layer Flash cases rather than duplicating it here.
