# Evidence 120 — NVMe 1.4 Endurance Group grounding, 2019

## Purpose

This record grounds [`../cases/120-nvme14-endurance-group-scoped-health-history.md`](../cases/120-nvme14-endurance-group-scoped-health-history.md).

The bounded question is:

> What primary evidence supports treating NVMe 1.4 Endurance Groups as a host-visible endurance-management and health-history scope that may span multiple NVM Sets, while keeping namespace identity, host workload, internal media work, current warning state, and hidden wear-leveling implementation separate?

The evidence is strong for the **ratified 2019 interface contract**. It does not establish generic invention priority for endurance pooling, a universal physical NAND layout, or the implementation of a named commercial controller.

## Evidence labels

- **H/P** — historical / primary standards record.
- **E** — engineering reconstruction constrained by the primary record.
- **A** — bounded functional analogy.
- **X** — rejected or unsupported stronger inference.

---

## Source A — NVM Express Base Specification Revision 1.4, 10 June 2019

### Identity

NVM Express, **NVM Express Base Specification, Revision 1.4**, dated **June 10, 2019**.

Official NVM Express PDF:

<https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf>

Official archive:

<https://nvmexpress.org/nvm-express-specification-archives/>

Front matter states that Revision 1.4 incorporates Revision 1.3 plus a listed set of ECNs/Technical Proposals, including **TP4018b** and **TP4050**.

### Claim strength

- **Strong H/P** for the ratified document identity/date and normative interface semantics used below.
- **No invention-priority claim** follows merely from inclusion in the 2019 standard.

---

## Source B — NVM Express “Changes in NVMe Revision 1.4”

### Identity

NVM Express, **Changes in NVMe Revision 1.4**:

<https://nvmexpress.org/changes-in-nvme-revision-1-4/>

### Relevant change record

The official change page lists:

- **NVM Sets (optional)** — a collection of NVM separate logically and potentially physically from NVM in other NVM Sets, referencing TP4018b;
- **Endurance Groups (optional)** — a mechanism enabling endurance management within one NVM Set or across a collection of NVM Sets, referencing TP4018b and TP4050.

### Safe use

> **NVMe Revision 1.4 is the checked public ratified NVMe-specification floor for the Endurance Group feature in this repository.**

### Unsafe use

> `2019 = invention date of endurance grouping / endurance partitioning / wear pools`.

The source is a standards-change history, not an invention-priority study.

### Claim strength

- **Strong H/P** for NVMe's own revision-level feature chronology.
- **Strong X** against turning a standard-introduction date into generic invention priority.

---

## Source C — Revision 1.4 §1.3, “Outside of Scope”

### Primary text relation

Revision 1.4 §1.3 says the interface is specified above nonvolatile-memory management such as **wear leveling** and that erases and other management tasks for NAND-like NVM are abstracted.

### Safe inference

The standard can expose an endurance-management **scope** without specifying the physical wear-leveling mechanism or erase geometry used underneath it.

Therefore:

> **Endurance Group Identifier != physical wear-leveling geometry.** (`E`)

and:

> **group-scoped health information != transparent FTL/NAND internal state.** (`E`)

### Rejected inference

The source does **not** justify mapping one Endurance Group directly to:

- one NAND die;
- one channel;
- one plane;
- one erase-block population;
- one over-provisioned spare pool;
- one particular FTL table.

### Claim strength

- **Strong H/P** for the interface/implementation boundary.
- **Strong X** against hidden-geometry reconstruction from the group identifier alone.

---

## Source D — Revision 1.4 §4.9, NVM Sets

### Normative relation

Section 4.9 defines an **NVM Set** as a collection of NVM separate logically and potentially physically from NVM in other NVM Sets.

The same section states:

- one or more namespaces may be created within an NVM Set;
- namespaces inherit attributes of the NVM Set;
- a namespace is wholly contained within a single NVM Set and shall not span more than one NVM Set;
- each NVM Set is associated with exactly one Endurance Group.

### Bounded reconstruction

```text
namespace
    -> one NVM Set
    -> exactly one Endurance Group association for that set
```

This is a hierarchy of normative interface relations. It does not establish a one-to-one physical media hierarchy.

### Findings supported

- **namespace identity != NVM Set identity** (`H/P`, `E`);
- **NVM Set identity != Endurance Group identity** (`H/P`, `E`);
- **logical/potential physical separation of NVM Sets != independent endurance management** (`H/P`, `E`), because §8.17 explicitly permits multiple NVM Sets to share one Endurance Group.

### Claim strength

- **Strong H/P** for containment/association rules.

---

## Source E — Revision 1.4 §8.17, Endurance Groups

### Normative relation

Section 8.17 states that endurance may be managed:

- within a single NVM Set; or
- across a collection of NVM Sets.

It then specifies:

- each NVM Set is associated with an Endurance Group;
- when two or more NVM Sets have the same Endurance Group Identifier, the NVM subsystem manages endurance across that collection;
- when only one NVM Set has a given Endurance Group Identifier, endurance is managed locally to that set;
- Endurance Group support requires the subsystem/controllers to report support, expose the namespace-associated Endurance Group Identifier, and support the Endurance Group Information log.

The section's example groups NVM Sets A and B under Endurance Group Y while NVM Set C alone forms Endurance Group Z.

### Findings supported

> **namespace/service partition can be finer than endurance-management partition.** (`E`)

> **NVM Set separation != Endurance Group separation.** (`H/P`, `E`)

> **one Endurance Group may aggregate endurance state/work across multiple NVM Sets.** (`H/P`)

### Boundaries

The section says **where endurance is managed at the interface level**, not how individual NAND cells are wear-leveled.

### Claim strength

- **Strong H/P** for group scope.
- **Strong X** against reading the diagram as a physical NAND placement diagram.

---

## Source F — Revision 1.4 §5.14.1.9, Endurance Group Information log

### Log identity and scope

Section 5.14.1.9 defines **Endurance Group Information, Log Identifier 09h**.

It states that:

- the log provides endurance information based on the Endurance Group;
- an Endurance Group consists of **zero or more NVM Sets**;
- the information is provided **over the life of the Endurance Group**;
- the Endurance Group Identifier is supplied in the Log Specific Identifier field.

### Safe use of the zero-set wording

The wording blocks the identity shortcut:

> **Endurance Group identity != one currently populated namespace/NVM Set by definition.** (`E`)

It does **not** by itself reveal the administrative creation/deletion/reuse lifecycle for group identifiers. Those semantics remain evidence debt.

### Current Critical Warning state

The first byte is `Critical Warning`. The standard states that these bits:

- indicate current critical-warning conditions for the Endurance Group;
- may trigger asynchronous events;
- represent the **current associated state**;
- are **not persistent**.

This supports:

> **current warning state != retained/cumulative endurance history.** (`H/P`, `E`)

and:

> **one log page != one persistence lifetime.** (`E`)

### Available Spare

`Available Spare` is a normalized percentage of spare capacity remaining for the Endurance Group. A separate threshold may trigger an asynchronous event.

Safe boundary:

> **spare-threshold warning != demonstrated spare exhaustion != immediate device failure.** (`H/P`, `E`)

This continues the warning/reserve/failure distinction already grounded at controller scope in Case 55.

### Percentage Used

`Percentage Used` is a **vendor-specific estimate** based on actual usage and the manufacturer's prediction of NVM life. The specification says that `100` indicates estimated endurance consumed but **may not indicate NVM failure**, and values may exceed 100.

Safe findings:

> **Percentage Used != direct physical wear sensor.** (`H/P`, `E`)

> **100% estimated use != proven failure.** (`H/P`, `X`)

The field is updated once per power-on hour when the controller is not in a sleep state.

### Endurance Estimate

`Endurance Estimate` is an estimate of total data bytes that may be written to the Endurance Group over the group's lifetime **assuming write amplification of 1**.

Safe finding:

> **Endurance Estimate != deterministic remaining-life counter.** (`H/P`, `E`)

The explicit WAF=1 assumption makes the estimate/model boundary part of the interface definition rather than an external interpretation.

### Data Units Written versus Media Units Written

The log separately defines:

- `Data Units Written` — total bytes written to the Endurance Group excluding controller writes due to internal operations such as garbage collection;
- `Media Units Written` — total bytes written to the Endurance Group **including host and controller writes**, with garbage collection given as an example.

This is the strongest mechanism-level relation in the case:

```text
host-visible write history
    !=
media-write history including hidden controller work
```

Safe findings:

> **host-written bytes != media-written bytes.** (`H/P`, `E`)

> **logical mutation history != complete media-maintenance history.** (`E`)

Unsafe finding:

> `Media Units Written - Data Units Written = exact garbage-collection write cost`.

The standard names garbage collection as an example of controller writes; it does not provide an exhaustive causal decomposition.

### Error-count lifetime wording

The same log defines `Number of Error Information Log Entries` as the number of Error Information log entries **over the life of the controller for the Endurance Group**.

This differs from the log introduction's broad wording `over the life of the Endurance Group`.

Safe finding:

> **life of Endurance Group != automatically life of controller for every field.** (`H/P`, `E`)

The source itself uses different lifetime anchors and should not be normalized into one inferred reset epoch.

### Claim strength

- **Strong H/P** for every field-level relation above.
- **Strong E** for the scope/lifetime decomposition.

---

## Source G — Revision 1.4 §8.17.1, Endurance Group events

### Event lifecycle

Section 8.17.1 allows host configuration of asynchronous events per Endurance Group.

The host can:

1. configure which conditions for a particular Endurance Group trigger entries;
2. read the Endurance Group Event Aggregate log to discover which groups have outstanding events;
3. read the Endurance Group Information log for a specific group to determine the condition;
4. clear group events by successfully reading that group log with `Retain Asynchronous Event = 0`.

### Retention-specific decomposition

```text
underlying spare/use/media state
    != current Critical Warning bit
    != outstanding event-notification state
```

Therefore:

> **event clear != wear reversal.** (`E`)

> **event acknowledgement/clearing != cumulative endurance-history erasure.** (`E`)

The standard describes clearing the event-reporting state, not restoring spare capacity or zeroing all group counters.

### Claim strength

- **Strong H/P** for event configuration/clearing semantics.
- **Strong E** for the retained-state decomposition.

---

## Prior-art / chronology boundary

### Earlier NVMe retained health state

Case 55 already grounds NVM Express Revision 1.0 / 1.0e SMART / Health information as controller-lifetime retained health/endurance state, including cross-power-cycle information.

Therefore:

> **Revision 1.4 Endurance Groups != invention of retained drive/controller health history.** (`H/P`, `X`)

What Revision 1.4 adds in this bounded case is a **group-scoped** endurance-management/reporting relation attached to NVM Sets.

### What remains ungrounded

This round does not establish whether earlier ATA, SCSI, proprietary SSD controllers, storage arrays, or research FTLs exposed an equivalent host-visible resource group for endurance pooling. It also does not inspect the original full text/history of TP4018b or TP4050.

Therefore:

> **2019 public NVMe feature floor != generic endurance-pooling invention date.** (`X`)

### Claim strength

- **Strong H/P** for NVMe-family chronology.
- **Open** for broader prior art/genealogy.

---

## Cross-case comparison

### Case 55 — NVMe SMART / Health

Case 55 establishes controller-oriented retained health history and already separates cumulative counters/estimates from current warning state.

Case 120 adds:

- NVM Set association;
- Endurance Group scope;
- possible multi-NVM-Set endurance management;
- group-specific lifetime/current/event distinctions;
- group-scoped host-vs-media write accounting.

Safe relation:

> **controller SMART history ~= Endurance Group health history only as a health-state analogy/evolution inside NVMe; their scopes are not identical.** (`A`, `E`)

### Case 76 — JESD218 SSD endurance qualification

Case 76 asks whether a rated SSD meets a workload/TBW/error/retention service contract.

Case 120 asks what a running NVMe subsystem reports and groups for endurance management.

Therefore:

> **qualification rating != live Endurance Group telemetry.** (`A`, `X`)

The `Endurance Estimate` references a WAF=1 assumption and `Percentage Used` points to JEDEC endurance measurement techniques, but the log page does not become a full JESD218 qualification record.

### Case 04 — mapped Flash

Case 04 grounds the lower-layer relation in which FTL mapping/reclamation can make physical writes and logical updates diverge.

Case 120's `Data Units Written` vs `Media Units Written` exposes the divergence at the standardized reporting surface, but Revision 1.4 explicitly keeps wear leveling/erase management abstract.

Therefore:

> **host/media write-accounting difference != disclosed FTL implementation.** (`A`, `X`)

### Case 66 — diagnostic log lifetimes

Case 66 shows that NVMe log pages differ in lifetime/scope and that retained summary/detail/current state must be separated.

Case 120 provides an independent group-health instance in which one group log contains current nonpersistent warning bits beside cumulative/lifetime-qualified measurements.

Safe comparison:

> **mixed temporal semantics recur across different NVMe information surfaces, but diagnostic history and endurance history remain different retained objects.** (`A`, `E`)

---

## Cross-source synthesis

The checked 2019 primary sources support this decomposition:

```text
namespace payload
    != namespace identity
    != NVM Set identity/membership
    != Endurance Group identity/association
    != endurance-management scope
    != current critical-warning state
    != outstanding event state
    != host-write count
    != media-write count
    != model-derived percentage-used/endurance estimate
    != hidden wear-leveling / GC / erase-management implementation
```

### Grounded finding 1 — endurance history can have a scope larger than one namespace

A namespace is contained in one NVM Set, while multiple NVM Sets may share one Endurance Group.

**Strength:** strong H/P + E.

### Grounded finding 2 — logical/resource separation and endurance separation are different relations

NVM Sets are separate logically and potentially physically, yet their endurance may be managed together under one group.

**Strength:** strong H/P + E.

### Grounded finding 3 — host workload and media write work are separately retained/accounted

The standard explicitly excludes internal controller writes from `Data Units Written` and includes them in `Media Units Written`.

**Strength:** strong H/P.

### Grounded finding 4 — one group information page has mixed temporal semantics

Critical Warning is current/nonpersistent while the page also exposes cumulative/lifetime-qualified health/work fields.

**Strength:** strong H/P + E.

### Grounded finding 5 — group scope remains an abstraction above wear leveling

The standard itself declares wear leveling/erase management below the interface.

**Strength:** strong H/P + strong X against physical-topology inference.

### Grounded finding 6 — event-state forgetting is not wear-state forgetting

Group warning/event notification can be cleared through the reporting protocol without any normative statement that physical wear or cumulative counters are reset.

**Strength:** strong H/P + E.

---

## Rejected stronger claims

- **`NVMe 1.4 invented endurance monitoring`** — rejected by earlier NVMe SMART/Health evidence.
- **`NVMe 1.4 invented endurance partitioning generally`** — unsupported; only the NVMe feature floor is established.
- **`Endurance Group = NAND die/channel/plane/block pool`** — rejected by the interface abstraction boundary.
- **`NVM Set separation = independent endurance pool`** — rejected; several NVM Sets may share one Endurance Group.
- **`namespace = endurance-history unit`** — rejected; group scope may include several sets/namespaces.
- **`Data Units Written = physical NAND writes`** — rejected by the separate Media Units Written field.
- **`Media Units Written difference = exact garbage-collection cost`** — unsupported; garbage collection is an example, not a complete decomposition.
- **`Percentage Used 100 = failure`** — explicitly rejected by the standard.
- **`Endurance Estimate = exact remaining life`** — rejected; it is an estimate with a WAF=1 assumption.
- **`Critical Warning is retained lifetime history`** — explicitly rejected; the bits are current and nonpersistent.
- **`cleared warning/event = restored endurance`** — unsupported/rejected.
- **`life of Endurance Group = life of controller for every field`** — rejected because the log itself uses both lifetime anchors.

---

## Related-repository check

The current [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) tree was checked in this round. No dedicated `NVMe Endurance Group` / `Endurance Group` technical-history case was found to reuse.

Division of labor:

- **technical-retention** keeps the bounded relation among payload scope, NVM Set scope, Endurance Group scope, cumulative health/work history, current warning/event state, and hidden media work;
- **computing-archaeology** should own a broader genealogy of SSD wear leveling, spare pools, over-provisioning, controller resource topology, and pre-NVMe endurance domains if developed.

---

## Evidence debt

1. Inspect the complete original ratified **TP4018b** and **TP4050** texts/change histories and establish proposal chronology.
2. Search ATA/SCSI/vendor/research-controller prior art for host-visible endurance domains or wear pools before 2019.
3. Trace 1.4a/1.4b/1.4c and NVMe 2.x changes to Endurance Group lifecycle and reconfiguration.
4. Establish field-by-field persistence/reset semantics rather than treating `over the life of the Endurance Group` as a universal persistence sentence.
5. Determine identifier behavior across Endurance Group deletion/recreation, NVM Set reconfiguration, controller replacement, namespace deletion/recreation, and reset.
6. Add a named commercial SSD/controller exposing more than one Endurance Group.
7. Capture `nvme-cli` Identify and Log Identifier 09h output on a named device.
8. Compare `Data Units Written` with `Media Units Written` under controlled workloads while avoiding the assumption that their difference is only garbage collection.
9. Independently correlate group telemetry with physical-media/FTL evidence if an open controller makes that possible.
10. Test event clearing independently of cumulative health counters.

None of these debts invalidates the bounded 2019 interface findings.
