# Evidence 120 Deepening — NVMe 1.4 Namespace → NVM Set → Endurance Group Association Boundary

## Status and bounded question

**`grounded`** for one narrow NVMe Revision 1.4 interface relation:

> When host software creates or deletes a namespace, does that Namespace Management operation itself create, delete, directly select, or reset the Endurance Group whose health/endurance history may cover the namespace?

The inspected answer is narrower than a general Endurance Group lifecycle history. In ratified **NVM Express Base Specification Revision 1.4 (10 June 2019)**, host namespace creation selects an **NVM Set Identifier (`NVMSETID`)**. Each NVM Set is associated with exactly one Endurance Group, while Identify Namespace separately reports the namespace's **Endurance Group Identifier (`ENDGID`)**. The Namespace Management host-specified field list includes `NVMSETID` but not `ENDGID`; namespace deletion removes the namespace and detaches it from controllers, but that command does not define Endurance Group destruction or history reset.

This supports a bounded engineering reconstruction:

```text
namespace creation
    -> host selects an NVM Set
    -> that NVM Set already has exactly one Endurance Group association
    -> namespace reports the corresponding NVMSETID and ENDGID
```

It does **not** establish how an Endurance Group itself is provisioned, destroyed, re-created, or reused, nor what happens to every group-lifetime field under controller replacement or subsystem reprovisioning.

---

## Sources and evidence class

### Primary normative source (`H/P`)

- NVM Express, **NVM Express Base Specification Revision 1.4**, ratified 10 June 2019:
  <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf>
  - §4.9 `NVM Sets`, especially Figure 134 and the NVM Set / Endurance Group association text;
  - §5.20 `Namespace Management command`, especially Figure 262 `Host Software Specified Fields`;
  - Figure 245 `Identify Namespace Data Structure`, especially `NVMSETID` and `ENDGID`;
  - Figure 247 `Identify Controller Data Structure`, especially `NSETIDMAX` and `ENDGIDMAX`;
  - §8.17 `Endurance Groups (Optional)` and §8.17.1 event configuration.

### Official revision-change record (`H/P`)

- NVM Express, **Changes in NVMe Revision 1.4**:
  <https://nvmexpress.org/wp-content/uploads/Changes-in-NVMe-Revision-1.4.pdf>
  - identifies NVM Sets as an optional new feature and points to TP4018b;
  - identifies Endurance Groups as an optional new feature and points to TP4018b and TP4050.

The individual TP4018b / TP4050 proposal bodies were **not** inspected in this slice. The official change record therefore supports proposal attribution, but not proposal-internal chronology, authorship, invention priority, or a claim that one specific TP introduced every field discussed below.

### Related-repository check (`H/P` project-state record)

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Endurance Group`, `TP4018b`, and `TP4050` found no dedicated overlapping case to reuse. Broader NVMe proposal history, controller provisioning, and SSD implementation genealogy should move there if developed; this repository keeps only the retention-specific scope/lifetime relation.

---

## Historical record

### 1. Revision 1.4 makes NVM Sets and Endurance Groups optional features

The NVM Express Revision-1.4 change record lists **NVM Sets** as an optional new feature and cites TP4018b. It lists **Endurance Groups** separately as optional and describes them as allowing endurance management within one NVM Set or across a collection of NVM Sets, citing TP4018b and TP4050.

This is a safe public-standard floor for the feature set. It is **not** an invention-priority claim for endurance pooling or wear domains in storage generally.

### 2. A namespace is created *in* an NVM Set

Revision 1.4 §4.9 states that a namespace is wholly contained within a single NVM Set. Figure 134 then states that Namespace Management's create action includes the **NVM Set Identifier as a host-specified field**.

The same section says:

- each NVM Set is associated with **exactly one Endurance Group**;
- when the host creates a namespace, it specifies the NVM Set Identifier of the NVM Set in which the namespace is to be created;
- the created namespace inherits attributes from that NVM Set;
- if NVM Sets are supported, controllers also support Endurance Groups and indicate each NVM Set's associated Endurance Group.

Therefore the historical interface exposes an indirection:

```text
namespace -> selected NVM Set -> associated Endurance Group
```

The specification does not say that Namespace Management creates a fresh Endurance Group for the namespace.

### 3. Namespace Management exposes `NVMSETID`, not a host-specified `ENDGID`

Revision 1.4 §5.20 defines Namespace Management create/delete. Figure 262 enumerates fields host software may specify when creating a namespace. Among the listed fields is:

- bytes `101:100`: **NVM Set Identifier (`NVMSETID`) — Yes**.

`ENDGID` is not one of the host-specified fields in that create table. Reserved fields must be zeroed by host software.

This is stronger than merely noticing that NVM Sets and Endurance Groups both exist. In the bounded Namespace Management interface, the host chooses the NVM Set; it does not directly provide a novel Endurance Group Identifier as part of namespace creation.

This does **not** prove that no management mechanism anywhere in an NVMe subsystem can provision Endurance Groups. It proves only what this Revision-1.4 Namespace Management command surface does.

### 4. Identify Namespace reports both association levels

Figure 245 reports:

- `NVMSETID`: the NVM Set with which the namespace is associated;
- `ENDGID`: the Endurance Group with which the namespace is associated.

This gives the host two observable association levels even though Namespace Management create directly supplies only `NVMSETID` among them.

Thus:

> **reported association != direct provisioning field**.

A field can expose the result of a relation without being the field through which that relation is created in the command under study.

### 5. Namespace delete removes the namespace; it does not define Endurance Group destruction

Section 5.20 says Namespace Management delete makes the namespace no longer present in the system and detaches it from all controllers. It also says there is **no data structure transferred for the delete operation**.

The inspected delete semantics do not say that deleting a namespace:

- deletes its NVM Set;
- deletes its Endurance Group;
- resets Endurance Group health counters;
- clears the Endurance Group Information log's lifetime-qualified fields;
- creates a new group-generation epoch.

The correct historical statement is consequently limited:

> **Namespace Management defines namespace deletion, not Endurance Group lifecycle destruction.**

Absence of such semantics in this command is not positive proof that all group state survives every possible administrative reprovisioning event.

### 6. Endurance Group identifiers select existing group-scoped actions

Section 8.17 defines `ENDGID` as a 16-bit value specifying the Endurance Group with which an action is associated; zero is reserved/invalid. Section 8.17.1 allows the host to configure events per Endurance Group using an Endurance Group Event Configuration feature.

This is selection/configuration **of an Endurance Group**. It should not be re-described as an Endurance Group creation command.

The group remains a wider reporting/management scope: two or more NVM Sets may share one `ENDGID`, while one NVM Set may be the sole member of a group.

### 7. `ENDGIDMAX` is an identifier bound, not a lifecycle epoch

Identify Controller reports `ENDGIDMAX` as the maximum value of a valid Endurance Group Identifier and states that the number of Endurance Groups supported by the subsystem is **less than or equal to** that maximum.

Therefore:

- `ENDGIDMAX` is not necessarily the current number of populated groups;
- `ENDGID` is not shown to be a monotonically increasing generation number;
- the fields do not establish identifier-reuse semantics.

A bounded numeric identifier space must not be silently turned into a retained chronology.

---

## Engineering reconstruction (`E`)

### Namespace lifecycle is narrower than Endurance Group lifecycle

The interface relation supports these distinctions:

> **namespace creation != Endurance Group creation**

> **namespace deletion != Endurance Group deletion**

> **host-selected `NVMSETID` != direct host provisioning of `ENDGID` in Namespace Management**

> **reported `ENDGID` association != proof of Endurance Group creation/reset semantics**

A namespace can be a narrower identity participating in a wider endurance-management/history scope. That wider scope may include several NVM Sets and therefore several namespaces.

The evidence does not prove every possible namespace churn sequence against a real controller, but it blocks an especially tempting wrong model:

```text
create namespace
    -> automatically create a new Endurance Group
    -> automatically start a new group-lifetime history
```

Revision 1.4 does not specify that chain.

### `delete all namespaces` is not demonstrated `delete all Endurance Groups`

Namespace Management even defines deletion of all namespaces (`NSID = FFFFFFFFh`), but the command text still frames the operation as namespace deletion. Because Endurance Groups are separately identified management/reporting scopes associated with NVM Sets, the stronger conclusion that deleting all namespaces necessarily destroys every Endurance Group or resets group history would require additional lifecycle evidence.

So:

> **absence of narrower members != demonstrated destruction of the wider retention-history scope**.

This is a scope relation, not a claim that an empty Endurance Group must persist forever.

### Identity, membership, and history scope have different lifetimes

Case 120 already separated namespace identity, NVM Set membership, Endurance Group association, group health/history, warning state, and hidden media work. The Namespace Management evidence adds a lifetime warning:

```text
namespace lifetime
    != automatically
NVM Set lifetime
    != automatically
Endurance Group lifetime/history epoch
```

The first inequality is grounded only in the sense that namespace create/delete operates on namespaces within NVM Sets. The second remains deliberately open at the actual NVM-Set/Endurance-Group provisioning layer; Revision 1.4's namespace command does not expose enough evidence to reconstruct it.

### A stable wider scope can aggregate work from changing narrower identities

Because Endurance Group accounting is group-scoped while namespaces are narrower objects inside NVM Sets, it is possible at the interface level for endurance information to concern a management domain broader than one namespace's identity.

The safe conclusion is relational:

> **per-namespace identity/history != group-scoped endurance history**.

Do not upgrade this into a claim about how any named controller handles namespace recreation, group-ID reuse, or physical NAND pool reassignment without device evidence.

---

## Functional analogies (`A`) and stop conditions

### Case 04 — mapped Flash

Only a narrow analogy is useful: a host-visible designation can reach a lower-level management relation through indirection. An NVMe namespace → NVM Set → Endurance Group association is **not** an FTL mapping and reveals no logical-to-physical NAND placement.

### Case 55 / Case 76 — health and endurance evidence

Case 55 already separates retained controller health/history from payload; Case 76 separates SSD qualification workload, host TBW, write amplification, error criteria, and later retention. Case 120 adds a **live group-scoped management/history identity** and this deepening adds its namespace-lifecycle boundary. No standards genealogy is inferred among those cases.

### Case 78 — bounded identifiers and currentness

Linux MTD BBT versions and NVMe Endurance Group identifiers are not one mechanism. The only reusable warning is methodological: a bounded numeric field must not be treated as a complete historical epoch without evidence for its comparison/reuse semantics.

### Stop conditions

This slice does **not** establish:

- how an Endurance Group is physically provisioned;
- whether a vendor exposes group creation/deletion through another management interface;
- whether `ENDGID` values are ever reused, or how reuse affects counters;
- exact persistence/reset rules for every field in Endurance Group Information;
- controller-replacement or subsystem-reprovisioning behavior;
- named-controller conformance;
- `nvme-cli` behavior on a real multi-group device;
- any NAND die/channel/plane/block correspondence;
- TP4018b/TP4050 internal proposal chronology or invention priority.

Those are separate evidence debts rather than conclusions inferred from Namespace Management.

---

## Narrow philosophical interpretation (`I`)

A retention system can let a narrower service identity appear and disappear while a wider management/history relation is defined at another scope. The useful conceptual point is only that **the lifetime of what is named for use need not be the lifetime of the retained evidence used to manage its substrate**.

This is not a claim that an Endurance Group is a philosophical subject, a memory of memory, or an archive. It is an engineering constraint on any later interpretation of persistence across identity churn.

---

## Result

The bounded Case-120 deepening establishes:

```text
namespace creation
    -> host chooses NVMSETID
    -> NVM Set has exactly one associated Endurance Group
    -> Identify Namespace reports NVMSETID + ENDGID

namespace deletion
    -> namespace disappears / is detached
    != specified Endurance Group deletion
    != specified group-history reset
```

The remaining question is now narrower and better stated: **what interface or implementation establishes Endurance Group provisioning, reuse, and lifetime epochs themselves?** That belongs to later proposal/device archaeology, not to an inference from ordinary Namespace Management.
