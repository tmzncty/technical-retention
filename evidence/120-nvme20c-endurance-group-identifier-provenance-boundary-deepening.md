# Case 120 evidence — NVMe 2.0c Endurance Group identifier provenance boundary

## Status

**Grounded deepening; no Case 120 maturity change.**

This record narrows one lifecycle/provenance question left open by the existing Endurance Group evidence:

> If two observations use the same numeric Endurance Group Identifier (`ENDGID`), is that alone evidence that both observations belong to the same Endurance Group lifetime?

For the bounded NVMe 2.0c interfaces inspected here, the answer is **no**.

The specification makes `ENDGID` a selector for a currently existing Endurance Group and requires creation to choose a non-zero identifier that is **not assigned to an existing Endurance Group**. It also permits Endurance Groups to be deleted. The inspected Create/Delete/List/Endurance-Group-Information path does not add a generation or epoch discriminator to `ENDGID` that would, by itself, prove historical continuity across a possible delete/recreate boundary.

The bounded conclusion is therefore:

```text
current ENDGID assignment
    != lifecycle-generation identity
    != historical-continuity evidence
```

and, more operationally:

```text
ENDGID(t1) == ENDGID(t2)
    + intervening delete/recreate cannot be excluded
    != proof of the same Endurance Group lifetime
```

This is a statement about **evidence sufficiency**, not a claim that any particular controller is known to reuse identifiers.

---

## Why this is a separate slice

The existing lifecycle-management deepening already established several necessary facts:

- NVMe 1.4 exposes Endurance Group scope and health history;
- Revision 2.0 / TP4052c adds interoperable Capacity Management for creating and deleting Endurance Groups and NVM Sets;
- Create Endurance Group selects a non-zero identifier not currently assigned to an existing group;
- Delete Endurance Group retires the current group and its contained entities through a specified lifecycle sequence;
- `currently unassigned` must not be silently rewritten as `never used before`;
- no observed controller-reuse trace was established by that earlier slice.

See:

- [`120-nvme-2019-2021-endurance-group-lifecycle-management-deepening.md`](120-nvme-2019-2021-endurance-group-lifecycle-management-deepening.md)
- [`../cases/120-nvme14-endurance-group-scoped-health-history.md`](../cases/120-nvme14-endurance-group-scoped-health-history.md)

The present slice starts **after** those facts and asks what historical inference a telemetry consumer may safely make from the numeric identifier itself.

---

## Primary sources

### NVM Express Base Specification Revision 2.0c

NVM Express, **NVM Express Base Specification, Revision 2.0c**, ratified 4 October 2022:

<https://www.nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-2.0c-2022.10.04-Ratified.pdf>

Relevant bounded locations include:

- Capacity Management, Create/Delete Endurance Group operations, around §5.3 / pp. 155–157 of the specification;
- Endurance Group Information log, Figure 217 and surrounding text, around pp. 196–198;
- Endurance Group management/containment material elsewhere in the Base Specification as referenced by those sections.

The current NVM Express specification archive is useful for version provenance:

<https://nvmexpress.org/specifications/>

A later ratified 2.2 revision preserves the same broad Create Endurance Group rule that creation selects a non-zero Endurance Group Identifier not assigned to an existing Endurance Group. It is only corroboration here, not the historical anchor for this slice:

<https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-Revision-2.2-2025.03.11-Ratified-1.pdf>

---

## Historical record

### 1. Create Endurance Group chooses an identifier that is not currently assigned

Revision 2.0c's Capacity Management text requires Create Endurance Group to select a non-zero Endurance Group Identifier that is **not assigned to an existing Endurance Group** in the specified domain. The completion reports the created element identifier.

This wording establishes a current allocation rule:

```text
create time
    -> choose non-zero ENDGID
    -> ENDGID must not be assigned to an existing group in that domain
```

It does **not** say:

```text
ENDGID must never have been used before
```

Nor does the inspected clause define the selected number as a permanent, generation-stable historical object identifier.

The distinction matters because `unassigned now` and `unused over all prior history` are different predicates.

### 2. Delete Endurance Group removes a current group

Revision 2.0c defines a Delete Endurance Group operation and rejects deletion when the supplied identifier does not designate an existing group (or is zero, under the specified invalid cases).

The broader lifecycle semantics already documented by the existing Case 120 lifecycle deepening show that deleting a group retires the current group and cascades through contained NVM Sets/namespaces according to the specification's lifecycle rules.

Therefore an observation sequence may contain a lifecycle discontinuity:

```text
time t1
    ENDGID = x designates existing group G1

later
    G1 is deleted

still later
    a new Endurance Group is created
```

The present source set does not need to prove that the controller chooses `x` again to establish the evidentiary boundary. It is enough that the creation rule is phrased in terms of **current assignment**, while deletion makes an identifier cease designating the prior current group.

### 3. Endurance Group Information is scoped by current Endurance Group identity

The Endurance Group Information log is addressed for an Endurance Group and includes group-scoped health/endurance fields such as:

- `Available Spare`;
- `Percentage Used`;
- `Endurance Estimate`;
- `Data Units Read`;
- `Data Units Written`;
- `Media Units Written`;
- media/data-integrity error information;
- other counters and warning state already analyzed in the canonical case.

Revision 2.0c describes `Endurance Estimate` in terms of the **lifetime of the Endurance Group**, and multiple fields are explicitly group-scoped.

That wording gives the counters a lifecycle-bearing object scope. It does not transform the numeric selector used to address the current group into a separately versioned historical generation identifier.

### 4. The inspected interface path does not expose a generation field alongside ENDGID

For this bounded slice, the inspected path is intentionally narrow:

```text
Capacity Management:
    Create Endurance Group
    Delete Endurance Group

current enumeration / selection:
    Endurance Group List / current group identifiers

telemetry:
    Endurance Group Information
```

Within that path, the group is selected/addressed by `ENDGID`; the inspected structures do not add a separate `ENDGID generation`, `epoch`, `creation sequence number`, or equivalent discriminator whose equality could independently establish the same historical lifetime across a delete/recreate interval.

This negative finding is deliberately narrow. It is **not** a claim that no NVMe mechanism anywhere in any revision could contribute external provenance context.

---

## Engineering reconstruction

### Selector identity and historical-object identity are different relations

A useful model is:

```text
(controller/domain scope, ENDGID)
    -> current protocol selector

(current protocol selector, lifecycle interval)
    -> historical Endurance Group instance
```

The first tuple is sufficient to address a current group under the relevant interface contract.

It is not, by itself, a proof that two observations separated in time refer to the same lifecycle instance.

Define a telemetry observation as:

```text
O = {
    controller_or_domain_scope,
    ENDGID,
    metric,
    value,
    observation_time
}
```

Then:

```text
O1.ENDGID == O2.ENDGID
```

does not imply:

```text
lifecycle(O1) == lifecycle(O2)
```

unless the observer can also exclude a lifecycle break or establish continuity by independent evidence.

### Current uniqueness is not historical uniqueness

The Create rule constrains the set of **existing** Endurance Groups:

```text
for current groups in one domain:
    selected ENDGID must be unassigned at creation
```

This supports current disambiguation.

It does not establish an eternal uniqueness property:

```text
one numeric ENDGID
    -> exactly one Endurance Group over all time
```

The latter would require additional normative text or observed lifecycle evidence not established by this slice.

### A lifetime counter needs a lifetime boundary

A field described as accumulating over the lifetime of an Endurance Group has an implicit object-history relation:

```text
counter value
    -> accumulated within one Endurance Group lifetime
```

A historical database that instead keys only on raw `ENDGID` risks silently assuming:

```text
same selector
    -> same lifetime
```

That implication is precisely what the inspected interface contract does not prove.

### Provenance context is separate retained state

For historical telemetry, a safer engineering reconstruction is:

```text
current telemetry sample
    + controller/domain identity
    + configuration/lifecycle provenance
    + observation time
    -> defensible historical correlation
```

Possible provenance evidence may include, depending on the system collecting it:

- observed Create/Delete Capacity Management events;
- configuration snapshots that bound when a group existed;
- a management-plane generation/epoch maintained outside the NVMe selector;
- controller replacement/reset-of-inventory context where relevant;
- explicit evidence that no delete/recreate interval occurred between two samples.

These are **engineering recommendations for evidence preservation**, not requirements imposed by NVMe 2.0c.

---

## Telemetry boundary

### Same identifier is enough for current addressing, not necessarily for longitudinal joining

For a current query, `ENDGID = x` may be exactly the correct selector.

For a historical join, the question is stronger:

```text
sample at t1 with ENDGID x
sample at t2 with ENDGID x

were both produced by one uninterrupted Endurance Group lifetime?
```

The numeric equality alone answers only the selector-equality part.

A longitudinal data model should therefore avoid treating raw `ENDGID` as an automatically permanent primary key unless the collector has separately established a no-reuse/no-recreation invariant for the system under observation.

### Counter discontinuity is evidence, but not a substitute for lifecycle provenance

If a future observed controller presents the same numeric identifier with unexpectedly lower lifetime-style counters, that may be a clue that the object lifecycle changed, the controller changed, telemetry semantics changed, or another discontinuity occurred.

This record does **not** define counter regression as a normative lifecycle detector. Counter initialization/reset semantics for a newly created Endurance Group need their own field-by-field source grounding.

Therefore:

```text
counter discontinuity
    may motivate provenance investigation

counter discontinuity
    != standards-defined generation token
```

---

## Retention relation exposed by this slice

Case 120 now contains at least four separable forms of retained relation:

```text
physical/media wear history
    != host-visible Endurance Group health accounting
    != current ENDGID allocation state
    != historical provenance that proves one lifecycle continued
```

The first may survive independently of administrative object lifecycle.

The second is interface-visible health/endurance state scoped to a group.

The third says which current group a numeric selector designates.

The fourth is evidence required by an external historian/telemetry system if it wants to prove that two observations belong to one uninterrupted lifecycle.

This gives a general technical-retention pattern:

```text
retaining a current name
    != retaining the history needed to prove what that name denoted earlier
```

---

## Cross-case comparison

### Case 04 — Flash logical mapping identity

Case 04 separates logical identity/current mapping authority from a particular physical embodiment.

The safe functional comparison is:

```text
Case 04:
    current logical selector / mapping relation
        != historical identity of one physical embodiment

Case 120:
    current ENDGID selector
        != proven continuity of one Endurance Group lifecycle
```

This is a **functional analogy only**. It is not a claim that NVMe Endurance Group identifiers descend from FTL mapping designs or that the mechanisms share implementation ancestry.

### Case 55 / Case 66 — retained health and mixed-lifetime telemetry

Those cases help establish that diagnostic/health information can have lifetimes different from payload and from current warning state.

Case 120 adds a different problem: even if a field is properly understood as lifetime-scoped, the observer still has to know **which lifecycle instance** the sample belongs to.

```text
temporal semantics of the field
    != provenance identity of the object carrying the field
```

### Synthesis 26 — typed persistence horizons

Synthesis 26 argues that survival claims need an explicit state class and event boundary. The present slice is complementary:

```text
state survived across time
```

and

```text
observer proved both samples belong to the same object generation
```

are not the same proposition.

Again, this is a cross-case analytical comparison, not a genealogy claim.

---

## Historical record vs engineering reconstruction vs analogy vs interpretation

### Historical record

Supported directly by the NVMe specification path inspected here:

- Create Endurance Group selects a non-zero `ENDGID` not assigned to an existing Endurance Group in the specified domain.
- Delete Endurance Group operates on an existing current group.
- Endurance Group Information is group-scoped and includes lifetime-qualified/endurance-related fields.
- the bounded Create/Delete/List/Information path addresses groups with `ENDGID` and does not expose a separate generation/epoch discriminator alongside that selector.

### Engineering reconstruction

Derived from those records:

- current selector identity and historical lifecycle identity are different relations;
- equality of `ENDGID` at two times is insufficient, by itself, to prove one uninterrupted group lifetime when intervening delete/recreate cannot be excluded;
- longitudinal telemetry should preserve lifecycle/configuration provenance if it needs historical identity stronger than current addressing.

### Functional analogy

Current handles, file descriptors, inode numbers, object IDs, or resource selectors in other systems may likewise be valid current locators without being eternal historical identities.

No genealogy or implementation inheritance is claimed.

### Philosophical interpretation

A name can remain numerically identical while the evidentiary basis for saying “this is the same historical object” changes.

The technical point does not require a metaphysical identity theory. It is enough to say that **selector equality is weaker evidence than lifecycle continuity**.

---

## Explicit non-claims

This record does **not** claim any of the following:

1. that a known shipping controller has been observed reusing a deleted Endurance Group Identifier;
2. that NVMe requires an implementation to reuse a previously used `ENDGID`;
3. that NVMe forbids such reuse forever;
4. that a recreated group must initialize every Endurance Group Information field to zero;
5. that all Endurance Group counters have identical initialization, reset, persistence, or overflow rules;
6. that deletion sanitizes former media contents;
7. that deleting and recreating a group reverses physical wear;
8. that the same `ENDGID` implies the same physical Media Units or NAND embodiment;
9. that the same physical media necessarily implies the same `ENDGID`;
10. that the entire NVMe specification contains no possible external provenance aid;
11. that controller replacement, subsystem reset, firmware update, namespace recreation, NVM Set recreation, and Endurance Group recreation are equivalent lifecycle events;
12. that a counter decrease is a standards-defined proof of identifier reuse;
13. that an external collector must implement a specific generation-counter design.

---

## What this closes

This slice closes one bounded inference debt in Case 120:

```text
same ENDGID
    != automatically same historical Endurance Group lifetime
```

It turns the earlier `currently unassigned != never-before-used` observation into an explicit telemetry/provenance rule.

The result is useful because Case 120 is about **retained health history**. Retaining the counters is only half of a longitudinal evidence problem; a historian or monitoring system also needs enough retained provenance to know what lifecycle object those counters belonged to.

---

## Remaining evidence debt

High-value next steps are narrower now:

1. **field initialization semantics** — find normative text for the initial value of each relevant Endurance Group Information counter/state on group creation;
2. **observed identifier reuse** — obtain a real controller, conformance test, emulator, vendor document, or fault/configuration trace showing whether and when an `ENDGID` is reused after deletion;
3. **delete/recreate telemetry trace** — observe list membership, group log availability, and counter behavior across a real lifecycle transition;
4. **NVM Set / namespace provenance** — test how contained-object recreation and reassignment should be correlated with the parent group lifecycle;
5. **controller/domain identity** — determine what additional scope a telemetry collector must preserve so that identical `ENDGID` values from different domains/controllers are never accidentally joined;
6. **revision comparison** — inspect later NVMe revisions for any lifecycle-generation or management provenance mechanism that changes this bounded 2.0c conclusion.

Until such evidence is added, the repository should preserve the conservative rule:

```text
ENDGID
    = current protocol selector

ENDGID alone
    != demonstrated generation-stable historical identity
```
