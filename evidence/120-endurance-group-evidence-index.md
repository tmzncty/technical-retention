# Case 120 — Endurance Group evidence index

## Status

**Case maturity: `grounded`.**

This index is navigation for the bounded evidence chains behind [`../cases/120-nvme14-endurance-group-scoped-health-history.md`](../cases/120-nvme14-endurance-group-scoped-health-history.md). It does not promote Case 120 and does not collapse later NVMe lifecycle-management semantics backward into the original 2019 NVMe 1.4 feature definition.

The evidence currently supports four distinct layers:

```text
2019 scope/reporting
    -> namespace / NVM Set / Endurance Group relations

2019 namespace-association boundary
    -> reporting association != direct group provisioning through Namespace Management

2019–2021 lifecycle-management deepening
    -> Capacity Management creates/deletes current Endurance Group objects

2022-spec provenance deepening
    -> current ENDGID selector != proven historical lifecycle generation
```

---

## 1. Canonical case

### Case 120 — NVMe 1.4 Endurance Groups

[`../cases/120-nvme14-endurance-group-scoped-health-history.md`](../cases/120-nvme14-endurance-group-scoped-health-history.md)

Canonical claims include:

- Endurance Group is a host-visible endurance-management scope distinct from namespace and NVM Set;
- one Endurance Group may cover one or more NVM Sets;
- the Endurance Group Information log mixes current/nonpersistent warning state with longer-lived or lifetime-qualified health/endurance state;
- `Data Units Written` and `Media Units Written` expose different accounting scopes;
- host-visible Endurance Group scope does not disclose exact NAND wear-leveling geometry;
- later Capacity Management lifecycle authority is not projected backward into NVMe 1.4.

Status remains **`grounded`**.

---

## 2. Evidence chains

### A. 2019 — original Endurance Group grounding

[`120-nvme14-2019-endurance-group-grounding.md`](120-nvme14-2019-endurance-group-grounding.md)

Primary role:

- anchors the feature to ratified NVMe 1.4;
- establishes Endurance Group / NVM Set scope and group-scoped health information;
- separates host writes from media/controller writes;
- preserves the boundary between interface-visible endurance scope and hidden NAND-management implementation.

Use this file when the claim concerns **what NVMe 1.4 exposed**.

### B. 2019 — namespace / group association boundary

[`120-nvme14-2019-namespace-group-association-deepening.md`](120-nvme14-2019-namespace-group-association-deepening.md)

Primary role:

- shows namespace creation selects an NVM Set rather than directly provisioning an Endurance Group;
- separates namespace lifecycle from Endurance Group lifecycle;
- prevents a reported `ENDGID` association from being misread as a namespace command that creates/manages that group.

Use this file when the claim concerns **association versus provisioning authority**.

### C. 2019–2021 — lifecycle-management deepening

[`120-nvme-2019-2021-endurance-group-lifecycle-management-deepening.md`](120-nvme-2019-2021-endurance-group-lifecycle-management-deepening.md)

Primary role:

- traces the bounded path from 2019 development material to NVMe 2.0 / TP4052c;
- establishes interoperable Capacity Management operations for Endurance Groups and NVM Sets;
- distinguishes fixed and variable capacity-management regimes;
- records create/delete transition semantics;
- establishes the important wording that a newly created group receives a non-zero identifier **not assigned to an existing group**;
- keeps `currently unassigned` separate from `never used before`;
- keeps group deletion separate from sanitization or reversal of physical wear.

Use this file when the claim concerns **current Endurance Group lifecycle and management authority**.

### D. NVMe 2.0c — identifier provenance boundary

[`120-nvme20c-endurance-group-identifier-provenance-boundary-deepening.md`](120-nvme20c-endurance-group-identifier-provenance-boundary-deepening.md)

Primary role:

- carries the lifecycle result into longitudinal telemetry/provenance reasoning;
- distinguishes a current protocol selector from a historical object generation;
- shows why equal numeric `ENDGID` values at two observation times do not, by themselves, prove one uninterrupted Endurance Group lifetime if intervening deletion/recreation cannot be excluded;
- recommends retaining lifecycle/configuration provenance when stronger historical correlation is required;
- explicitly avoids claiming observed identifier reuse without a real trace.

Core boundary:

```text
current ENDGID assignment
    != lifecycle-generation identity
    != historical-continuity evidence
```

Use this file when the claim concerns **telemetry joins, historical identity, or provenance**.

---

## 3. Claim-routing guide

| Question | Preferred evidence |
| --- | --- |
| When did NVMe publicly ratify Endurance Groups? | 2019 grounding |
| Is Endurance Group scope identical to namespace or NVM Set scope? | 2019 grounding |
| Does Namespace Management directly create an Endurance Group in NVMe 1.4? | namespace/group association deepening |
| When does interoperable create/delete authority appear? | 2019–2021 lifecycle deepening |
| Does group deletion mean physical sanitization? | lifecycle deepening + canonical non-claims |
| Does `not assigned to an existing group` mean `never used before`? | lifecycle deepening |
| Does the same `ENDGID` at two times prove one uninterrupted lifetime? | identifier-provenance deepening |
| Does Case 120 show a real shipping controller reusing ENDGIDs? | **No — still evidence debt** |
| Are all group-log fields one persistence/lifetime class? | canonical grounding |
| Do host writes equal all physical media writes? | canonical grounding |

---

## 4. Layer discipline

Case 120 uses four labels consistently.

### Historical record

Reserved for what the NVM Express specifications, change records, proposals, or later direct device traces actually say/show.

Examples:

- NVMe 1.4 exposes Endurance Groups;
- NVMe 2.0 adds Capacity Management create/delete operations;
- Create Endurance Group selects a non-zero identifier not assigned to an existing group.

### Engineering reconstruction

Used for relations derived from those records without presenting the derivation as specification wording.

Examples:

```text
current selector
    != historical generation identity
```

and:

```text
field temporal semantics
    != provenance identity of the lifecycle object
```

### Functional analogy

Used when comparing Case 120 with other systems, such as current resource handles, file descriptors, inode-like selectors, or Case 04 mapping identity.

Such comparisons do **not** establish genealogy.

### Philosophical interpretation

May observe that identical naming is weaker than historical-object continuity, but this layer must not be used to manufacture hardware or standards facts.

---

## 5. Cross-case comparison points

### Case 04 — Flash mapping identity

Useful comparison:

```text
current selector / current mapping authority
    != historical identity of one embodiment or lifecycle
```

Functional analogy only; no implementation descent claimed.

### Case 55 / Case 66 — health and diagnostic history

Useful comparison:

```text
retained health history
    != payload retention
```

Case 120 adds the question of **which scoped lifecycle object owns that history**.

### Synthesis 26 — typed persistence horizons

Useful comparison:

```text
state surviving an event
    != proof that two observations belong to the same lifecycle generation
```

Persistence horizon and provenance identity are separate dimensions.

---

## 6. Current evidence debt

Do not close these without new primary evidence:

1. actual shipping-controller or emulator evidence showing `ENDGID` reuse after deletion;
2. field-by-field initialization semantics for Endurance Group Information after creation/recreation;
3. a delete/recreate telemetry trace showing list membership and counter behavior;
4. provenance behavior across NVM Set and namespace recreation/reassignment;
5. controller/domain scoping rules needed by long-term telemetry stores;
6. later-revision review for any generation/epoch mechanism that changes the current bounded conclusion;
7. fault/configuration experiments that distinguish selector reuse from controller replacement or wider subsystem reconfiguration.

The conservative repository rule remains:

```text
ENDGID
    = current protocol selector

ENDGID alone
    != demonstrated generation-stable historical identity
```

---

## 7. Related repository boundary

Broader SSD/NVMe architecture, controller history, and storage-interface genealogy should be reused from [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) when a dedicated technical-history package exists.

A fresh search for `Endurance Group`, `ENDGID`, and `Capacity Management NVMe` found no dedicated overlapping package there during this deepening, so this index keeps only the technical-retention-specific evidence relations rather than recreating a general NVMe history.
