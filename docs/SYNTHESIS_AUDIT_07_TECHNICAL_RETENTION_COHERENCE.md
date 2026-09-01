# Synthesis Audit 07 — Does `technical retention` cohere?

> **Bounded question:** after six thesis audits and four named philosophical/prior-art tests, does the repository's own category `technical retention` name one defensible analytical relation, several separate subfamilies, or only a loose heuristic umbrella?

**Status:** bounded cross-case synthesis.

This document does **not** introduce a new historical case, promote any case to `mature`, or declare a final philosophy of retention. It adversarially tests the repository's category against the five cases currently marked `grounded` in [`CASE_INDEX.md`](../CASE_INDEX.md):

- [`00-abacus-retained-position.md`](../cases/00-abacus-retained-position.md);
- [`02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md);
- [`03-dram-refresh-as-scheduled-restoration.md`](../cases/03-dram-refresh-as-scheduled-restoration.md);
- [`04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md);
- [`05-rados-replicated-object-repair.md`](../cases/05-rados-replicated-object-repair.md).

The mercury delay-line case remains `first-pass` and is therefore used only as a future stress test, not as evidence needed to make the verdict work.

The evidence here is inherited from the source-controlled case and grounding records. No new historical vocabulary is attributed to Cheng Dawei, magnetic-core designers, Dennard, Flash engineers, or Ceph/RADOS authors. `Technical retention` remains a **project analytical term**, not a claim about what historical actors thought they were doing.

---

## 1. Verdict

The current evidence rejects both extremes.

### Rejected extreme A — one common physical or engineering mechanism

There is no single mechanism shared by all five grounded cases.

The cases retain state through radically different means:

- positional mechanical stability interpreted by a trained operator;
- magnetic remanence, with restore obligations created by some read regimes;
- charge storage plus deadline-driven regeneration;
- nonvolatile physical state plus mapping, invalidation, relocation, and reclamation;
- replicated logical state plus placement, version/currentness, temporary authority, and repair.

Any definition that says retention **is** remanence, refresh, active maintenance, addressability, physical persistence, replication, or one particular kind of storage operation is already refuted by the existing cases.

### Rejected extreme B — an unconstrained family resemblance among anything that lasts

The category also cannot mean merely:

> `something at t1 was causally affected by something at t0`.

That criterion is too broad. A scratch, stain, thermal residue, displaced object, or accidental material trace can survive a prior event without functioning as the retained state of any technical procedure. The repository would then lose the boundary that originally distinguished technical retention from generic physical persistence.

The grounded cases themselves supply stricter negative controls:

- an abacus configuration can remain physically intact while losing its numerical meaning if the positional convention or procedural role is lost;
- an obsolete Flash embodiment can remain physically readable after it no longer counts as the current logical unit;
- a RADOS replica can remain reachable while stale or unauthorized to answer as current.

Physical survival alone is therefore not sufficient.

### Current bounded result — one minimal analytical relation, many mechanisms

Across the five grounded cases, one minimal relation survives adversarial comparison:

> **Technical retention is the technically organized continuation of an operationally typed state across a temporal separation such that, at a later moment, a state can be recovered, interpreted, or admitted as equivalent/current according to a rule relevant to a later operation.**

This is deliberately a **relational criterion**, not a physical essence.

It requires the analysis to name at least:

1. **retention target** — what state, value, identity, relation, trace, or currentness claim is supposed to continue;
2. **temporal separation** — some nonzero interval between establishment and later use/recovery, without imposing a minimum duration;
3. **continuity mechanism** — passive stability, reconstruction, remapping, replication, procedure, or another mechanism that connects the two moments;
4. **recovery / interpretation / admissibility operation** — how the later system or operator obtains a usable candidate state;
5. **sameness / currentness rule** — why that later candidate counts as the retained target rather than merely as some surviving physical trace.

The category therefore has **more structure than a loose family resemblance**, but less unity than a single engineering operation.

The best current description is:

> **a controlled analytical family organized by one minimal recoverability relation and several independent mechanism axes.**

That formulation remains provisional. A later case can still break it.

---

## 2. Why `operationally typed state` is necessary

The phrase is meant to stop the category from swallowing all durable matter.

A state is `operationally typed` when a convention, interface, procedure, architecture, or protocol establishes what distinctions matter and what a later operation is allowed to do with them.

This does **not** require machine autonomy.

### Abacus

In the grounded abacus case, bead/counter position is meaningful only through positional convention and procedural context. Cheng's `待數莫動` evidence matters because the configuration is not merely left physically unchanged; it is left as a numerical state that remains available to the calculation.

The human supplies selection and interpretation. That is still technically organized retention because the artifact, positional convention, and procedure jointly determine what later use of the configuration means.

### Magnetic core and DRAM

In core and DRAM, the typing is architectural and electrical: a selected cell is treated as holding a logical value, and the read/restore machinery determines how that value remains available across access or time.

The immediate physical token may change, but the selected logical state remains typed by the memory organization.

### Mapped Flash

In mapped Flash, a stable logical designation plus retained mapping/allocation state determines which physical embodiment currently realizes the logical unit. An older embodiment may survive physically while no longer satisfying the current logical type.

### RADOS

In RADOS, object identity, PG placement, version/currentness, map epoch, and temporary protocol authority constrain which reachable copy is admissible as the current retained object.

The result is important:

> **The retained target is never identified by material survival alone. It is identified by material survival or reconstruction under a technical rule that says what later state counts.**

This is an engineering/methodological synthesis, not historical vocabulary.

---

## 3. Five-case adversarial matrix

| Grounded case | Retention target | Continuity mechanism | Later recovery / admissibility | Counterexample that blocks an overbroad definition |
| --- | --- | --- | --- | --- |
| Abacus / positional reckoning | actionable numerical configuration under positional/procedural convention | passive mechanical stability + human protection/context | human spatial selection and interpretation | physical arrangement can survive while numerical/procedural meaning is lost |
| Magnetic core | logical value associated with a selected core in the bounded regime | remanent magnetization; restore when a destructive read creates the obligation | coordinate selection + sensing + rewrite where required | quiescent retention disproves `retention = continuous maintenance`; destructive access disproves `nonvolatile = read-invariant` |
| DRAM | logical cell value under row/column selection | bounded charge retention + scheduled sense/restore; access restore in the bounded Dennard embodiment | decoder/sense infrastructure returns and restores the logical value | physical charge continuity is not required; fixed physical home can remain while microscopic state is rebuilt |
| Mapped Flash | current logical unit/value plus mapping/allocation relation | nonvolatile cell state + out-of-place update + mapping + deferred reclaim | logical designation resolves through current mapping to an admissible physical embodiment | stale/invalid embodiment can survive after current identity moved elsewhere |
| RADOS | current logical object under version/placement/authority rules | multiple replicas + ordered updates + version/currentness state + peering/repair | object → PG → placement candidates → currentness/authority → read/recovery | reachable replica does not automatically count as current; physical copy multiplicity does not define retained currentness |

No single material process appears in every row. The common structure is instead the relation between a **typed target at one moment** and an **admissible/recoverable continuation at a later moment**.

---

## 4. Candidate definitions tested and rejected

### 4.1 `Technical retention = physical state survives`

**Rejected.**

It fails in both directions.

A higher-level retained state can survive while lower-level physical embodiments are reconstructed, erased as obsolete, or replaced. Conversely, a physical embodiment can survive after its interpretive meaning, logical currentness, or protocol authority is gone.

This repeats and consolidates earlier findings:

- `physical loss ≠ higher-level forgetting`;
- `physical survival ≠ retained current state`;
- `forensic witness ≠ authoritative current state`.

### 4.2 `Technical retention = same physical token remains`

**Rejected.**

Core restore, DRAM regeneration, Flash relocation, and RADOS replica replacement all preserve a higher-level state across material nonidentity.

The rule deciding sameness therefore belongs in the analysis.

### 4.3 `Technical retention = active maintenance keeps a state alive`

**Rejected.**

Abacus position, quiescent magnetic remanence, and idle Flash provide direct counterexamples. Maintenance is one possible condition of retention, not its universal form.

### 4.4 `Technical retention = a state has an address`

**Rejected.**

Human-mediated positional selection is enough for the bounded abacus case. Conversely, resolving a logical designation to a physical candidate is not sufficient when currentness/admissibility is still undecided.

### 4.5 `Technical retention = a state is available now`

**Rejected.**

Temporary unavailability does not prove forgetting, and a surviving state can require later reconstruction or restoration before service resumes. Retention concerns continuity across time; availability concerns successful use at a particular moment.

### 4.6 `Technical retention = durable storage`

**Rejected.**

The abacus case is explicitly working/session retention, and DRAM is volatile despite being a canonical mechanism of memory retention. No minimum duration can be extracted from the grounded set without arbitrarily excluding cases the project has already sourced and bounded.

### 4.7 `Technical retention = any recoverable trace`

**Too broad unless the target and recovery rule are named.**

Kirschenbaum/forensics work already forced the distinction between current logical state and surviving forensic witness. A stale Flash page or old RADOS replica can be recoverable **as evidence of a prior state** while not being recoverable **as the current operational state**.

Thus the criterion cannot simply ask `can anything be recovered?` It must ask:

> **recovered as what, for which later operation, under which sameness/currentness rule?**

This is the strongest boundary produced by the present audit.

---

## 5. Does `technical retention` require subfamilies?

The cases clearly form different regimes, but the current evidence does **not** justify turning them into a small set of mutually exclusive subfamilies.

Why not?

Because the important differences cross-cut one another.

A single technology can combine several regime features:

- magnetic core is quiescent at rest yet can become access-triggered restore;
- DRAM combines stable logical selection, destructive or nondestructive access regimes, and deadline-driven regeneration;
- mapped Flash combines quiescent nonvolatile state with workload/capacity-triggered reclaim, mapping-mediated mobility, and wear/failure management;
- RADOS combines replication, temporary authority, failure-triggered repair, and distinct acknowledgement/durable-commit thresholds.

A forced taxonomy such as `passive / active / distributed` would hide more than it reveals.

The better current structure is a set of **independent comparison axes**.

### Axis A — what continuity is preserved?

- one physical distinction;
- logical value across physical reconstruction;
- logical identity across relocation;
- currentness/authority across replica multiplicity;
- interpretability/procedural role;
- forensic trace rather than current service state.

### Axis B — what triggers retention work?

- no recurring work merely to remain;
- access-triggered restoration;
- deadline-driven regeneration;
- workload/capacity-triggered reclamation;
- wear/lifetime-triggered placement;
- failure/membership-triggered repair;
- human/procedural protection and interpretation.

### Axis C — what may change while identity survives?

- microscopic physical state only;
- physical home;
- mapping relation;
- replica membership;
- temporary authority;
- interface used for recovery.

### Axis D — who or what performs recovery?

- trained human operator;
- fixed sensing/decoder machinery;
- refresh/sense infrastructure;
- controller/mapping layer;
- distributed protocol and repair machinery;
- forensic tooling outside the ordinary service interface.

### Axis E — what kind of later claim is being made?

- `the same operational value is still usable`;
- `the same logical identity is still current`;
- `a reconstructible equivalent exists`;
- `a historical/forensic trace survives`;
- `the service can continue despite embodiment failure`.

These axes make the category disciplined without pretending that all cases instantiate one engineering machine type.

---

## 6. What the audit changes about the project's central question

The opening question remains useful:

> **How does a state outlive the moment that produced it?**

But it is now too permissive if left alone. The bounded cases require a second question immediately after it:

> **What rule makes the later state count as the continuation of that retained target?**

This second question prevents three recurring category errors:

1. treating any material residue as the retained operational state;
2. treating logical identity as if it required one unchanged embodiment;
3. treating a reachable candidate as if it were necessarily current or admissible.

A more precise project workflow is therefore:

```text
What is the retention target?
        ↓
What technical convention / interface / protocol types that target?
        ↓
What changes between t0 and t1?
        ↓
What continuity mechanism bridges the interval?
        ↓
How is a candidate recovered or interpreted at t1?
        ↓
What rule says that candidate is the same / current / admissible target?
        ↓
Which failures break physical survival, logical identity, currentness,
interpretability, serviceability, or trace recoverability separately?
```

This is more restrictive than `anything that lasts`, while remaining broad enough to include manually interpreted positional state, volatile regenerated memory, remapped nonvolatile storage, and distributed replicated objects.

---

## 7. Claim-type discipline

The verdict contains several different kinds of claims and they must remain separated.

### Historical record (`H/P/S`)

Historical and technical facts remain in the individual cases and grounding records: Cheng's positional instructions, core read/restore evidence, Dennard/commercial DRAM refresh evidence, early Flash mapping terminology/mechanisms, and 2006–2007 RADOS semantics.

This audit adds no new historical actor vocabulary.

### Engineering / methodological reconstruction (`E`)

The five-part relation — target, temporal separation, continuity mechanism, recovery/admissibility, sameness/currentness rule — is a project reconstruction derived from the grounded mechanisms.

### Functional comparison (`A`)

Comparing a human-interpreted abacus state, an electronic memory cell, a remapped logical block, and a replicated object under one schema is a functional comparison. It does not establish genealogy, equivalent architecture, or shared historical purpose.

### Philosophical interpretation (`I`)

Calling this a `relational analytical category` rather than a physical essence is a philosophical/methodological interpretation of the comparison. It is not a claim that the five technical traditions themselves articulated one philosophy of retention.

---

## 8. Current category boundary

For the next research slices, a proposed case should not enter merely because it contains the words `memory`, `storage`, `state`, `trace`, or `persistence`.

A candidate case should be able to answer all of the following at least provisionally:

1. **What is the retained target?**
2. **What later operation, interpretation, or decision makes retention of that target matter?**
3. **What technical arrangement or procedure connects the earlier state to that later use?**
4. **What transformations are allowed without counting as loss of identity?**
5. **What rule distinguishes an admissible continuation from an obsolete, stale, accidental, or merely surviving trace?**

If a candidate cannot answer questions 2–5, it may be an interesting material trace or historical artifact, but it has not yet earned inclusion as a technical-retention case.

This criterion intentionally allows a forensic case to qualify when the **retention target itself is the prior trace**. In that situation, the admissibility rule is forensic rather than service-currentness. The audit therefore does not privilege only current operational state; it requires the analyst to state which target is being retained.

---

## 9. Counterexample search: what could still break this result?

The present invariant has survived only five grounded regimes. Several roadmap bridges could still expose a failure.

Especially valuable stress tests are:

- **latch / flip-flop / register** — tests how little temporal separation is needed before the relation becomes analytically useful rather than trivial;
- **cache / buffer** — tests whether expected near-future reuse is enough, and when transfer/computation overwhelms the retention description;
- **HDD remapping and bad-sector substitution** — tests whether the same identity/currentness logic appears without Flash erase geometry;
- **SSD controller-mediated persistence** — tests host acknowledgement, volatile controller state, flush/FUA/power-loss boundaries, and whether a logical write is retained before durable media commit;
- **file-system crash consistency** — tests whether the retained target is a value, a set of ordering invariants, or a recoverable state transition;
- **RAID / erasure coding** — tests recoverable equivalence without complete replicas;
- **distributed consensus / logs** — tests whether agreement/currentness can become more important than any one stored copy.

A particularly dangerous counterexample would be a technically organized state that clearly matters to a later operation yet cannot be described in terms of a target plus some rule of later equivalence/currentness/admissibility. Finding such a case should force this audit to be revised rather than expanding the words until the counterexample disappears.

---

## 10. Relationship to prior audits and named philosophical tests

This audit does not replace the earlier results. It depends on their negative discipline.

- [`SYNTHESIS_AUDIT_01_MAINTAINED_PERSISTENCE.md`](SYNTHESIS_AUDIT_01_MAINTAINED_PERSISTENCE.md) blocks `retention = continuous maintenance`.
- [`SYNTHESIS_AUDIT_02_TEMPORAL_TRANSPORT.md`](SYNTHESIS_AUDIT_02_TEMPORAL_TRANSPORT.md) supplies the recoverability-across-time model while blocking literal transport as a universal mechanism.
- [`SYNTHESIS_AUDIT_03_ADDRESSABILITY.md`](SYNTHESIS_AUDIT_03_ADDRESSABILITY.md) separates designation, resolution, currentness/admissibility, and recovery.
- [`SYNTHESIS_AUDIT_04_PRIVILEGED_LOCATION.md`](SYNTHESIS_AUDIT_04_PRIVILEGED_LOCATION.md) blocks the assumption that logical sameness requires one permanent physical home.
- [`SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md`](SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md) makes the retention target layer-specific.
- [`SYNTHESIS_AUDIT_06_MAINTENANCE_VISIBILITY.md`](SYNTHESIS_AUDIT_06_MAINTENANCE_VISIBILITY.md) blocks a universal automation/reliability narrative.
- [`PHILOSOPHICAL_TEST_01_ERNST_OPERATIONALITY.md`](PHILOSOPHICAL_TEST_01_ERNST_OPERATIONALITY.md) requires mechanism-specific operations/times without making operation continuous by definition.
- [`PHILOSOPHICAL_TEST_02_STIEGLER_TERTIARY_RETENTION.md`](PHILOSOPHICAL_TEST_02_STIEGLER_TERTIARY_RETENTION.md) blocks `technical retention = tertiary retention`.
- [`PHILOSOPHICAL_TEST_03_HEIDEGGER_ORDERABILITY.md`](PHILOSOPHICAL_TEST_03_HEIDEGGER_ORDERABILITY.md) blocks `technical availability = Bestand`.
- [`PHILOSOPHICAL_TEST_04_KIRSCHENBAUM_FORENSIC_MATERIALITY.md`](PHILOSOPHICAL_TEST_04_KIRSCHENBAUM_FORENSIC_MATERIALITY.md) forces current-state retention and forensic-trace survivability to remain separable.

The new result should therefore be read as a synthesis **under constraint**, not as a fresh totalizing definition.

---

## 11. Bounded conclusion

The repository's long-term question asked whether `retention` is one operation or only a family resemblance imposed across unlike mechanisms.

The five grounded cases currently support a middle answer:

> **There is no single physical retention operation. There is, however, a nontrivial common analytical relation: a technically organized, operationally typed target remains or is reconstructed across temporal separation so that a later state can count as an admissible continuation under an explicit sameness/currentness/interpretation rule.**

That relation is narrow enough to reject generic physical persistence and broad enough to survive the current mechanical, magnetic, dynamic-electrical, mapped-semiconductor, and distributed cases.

The mechanisms should therefore continue to be compared through independent axes rather than forced into exclusive subfamilies.

This is **not yet a final definition of technical retention**. It is the first bounded category-coherence result and should be stress-tested by the next technical bridge rather than promoted into a grand philosophical chapter.
