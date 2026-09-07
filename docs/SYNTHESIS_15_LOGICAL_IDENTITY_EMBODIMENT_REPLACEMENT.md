# Synthesis 15 — Logical Identity, Resolution Relations, and Embodiment Replacement

## Scope

This is a **bounded cross-case engineering synthesis**, not a new historical case and not a genealogy of disks, Flash translation, DRAM redundancy, or address translation.

It closes one relation-decomposition question already present in the roadmap:

> When a mapping layer moves state, is the retained object data, address, relation, or all three?

The comparison is built from already-grounded repository cases:

- [Case 04 — mapped Flash virtual/logical/physical mapping](../cases/04-flash-virtual-mapping-logical-identity.md);
- [Case 14 — SCSI disk defect reassignment](../cases/14-scsi-disk-defect-reassignment-logical-identity.md);
- [Case 89 — ATA LBA / logical-CHS translation](../cases/89-ata-lba-chs-translation-logical-sector-identity.md);
- [Case 119 — DDR4 Post-Package Repair](../cases/119-ddr4-post-package-repair-row-remapping.md).

Historical claims remain owned by those case and evidence records. The relation types introduced here are **project engineering vocabulary (`E`)** unless explicitly identified as historical vocabulary. Similarity across the cases is a functional comparison, not evidence of technical descent.

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Flash Translation Layer`, defect reassignment, PPR, and logical-address remapping found no dedicated cross-mechanism comparison to reuse. Broader histories of disk translation, semiconductor redundancy, Flash controllers, and repair mappings belong there if developed; this document keeps only the retention-specific decomposition.

---

## The question is underspecified

The phrase `the mapping layer moved the state` can name several technically different events.

At least five relations may be involved:

1. **designation** — the caller-facing address or name through which a retained service is requested;
2. **payload value** — the current user/application value associated with that designation;
3. **resolution relation** — retained metadata or device state that determines which lower-layer embodiment currently answers to the designation;
4. **physical embodiment** — the sector, Flash block/page, DRAM row, or other bearer currently selected by that relation;
5. **retirement / replacement state** — information and reserved capacity that determine whether an old embodiment still counts, has been replaced, can be reclaimed, or can be substituted again.

These are not automatically one object with one lifetime.

The four grounded cases supply direct counterexamples to any universal equation among them:

```text
same designation
    can survive a changed embodiment

changed resolution relation
    need not imply payload movement

changed embodiment
    need not imply payload preservation

persistent resolution state
    can outlive volatile payload

old embodiment no longer current
    need not mean old embodiment is physically erased
```

The useful answer is therefore not `data`, `address`, `relation`, or `all three` in the abstract. A defensible retention claim has to state **which continuity is being asserted across which transition**.

---

## Historical records kept separate

### Case 04 — mapped Flash: relocation and logical update can both change the resolution relation

The 1993-filed M-Systems Flash-file-system patent distinguishes virtual, logical, and physical address spaces. A virtual map resolves a stable-looking virtual designation to the currently selected lower-layer block. When an already-written location is updated, the controller writes the new value into an unwritten location, changes the map so the original virtual address resolves to the new block, and marks the old block unusable/deleted until later erase-unit reclamation.

The same source separately describes transfer/reclamation: still-current blocks are copied to reserved unwritten space before an old unit is erased, while logical unit identity remains stable across physical relocation.

Case 04 therefore contains **two different mapping transitions** that should not be collapsed:

```text
logical update:
    same designation
    + new payload value
    + new current embodiment
    + changed mapping/currentness relation
    + old embodiment becomes stale/deleted

relocation / reclamation of still-current data:
    same designation
    + intended same current payload value
    + new embodiment
    + changed lower-layer resolution relation
    + old erase unit later destroyed
```

This is already enough to reject `mapping change = data change` and `physical movement = logical update`.

### Case 14 — SCSI defect reassignment: designation can survive embodiment replacement even when payload does not

The bounded Seagate `REASSIGN BLOCKS` contract makes a stronger negative case. The drive changes the **physical medium used for a logical block address**, yet the same LBA remains the host-visible designation after reassignment.

But the command description explicitly says that the affected block data are not preserved by reassignment itself. The initiator should recover data beforehand if possible and write the recovered value back to the same LBA afterward.

Thus:

```text
same LBA designation after repair
    + replacement physical sector
    + updated defect/replacement relation
        !=
automatic continuity of old payload
```

This case proves that a retained **service slot / designation relation** can survive a repair transition more strongly than the value previously stored through that slot.

### Case 89 — ATA CHS/LBA translation: a mapping/presentation relation can change without established physical movement

ATA-2/ATA-3 supply the necessary control case. A device can expose mutable logical-CHS translation parameters while retaining the same LBA for a given logical sector. The period standards explicitly say that a given logical sector's LBA does not change when the current logical CHS translation changes.

The 1997 SyQuest implementation witness further states that logical sector addresses do not imply actual physical media location.

So a change in an address representation or presentation mapping does **not** establish that user payload moved physically:

```text
same logical sector / LBA
    + changed logical-CHS presentation relation
        !=
proven data relocation
```

This blocks a common analytical shortcut: not every map-like state is a relocation map, and not every mapping transition is evidence of movement below the interface.

### Case 119 — DDR4 PPR: the replacement relation can outlive the payload whose future location it governs

DDR4 Post-Package Repair supplies a different lifetime counterexample. In the bounded product/platform evidence, a failing row address can be redirected to a spare physical row. Soft PPR is temporary/non-persistent while hard PPR is persistent/permanent.

Ordinary DDR4 payload remains volatile and still depends on power and refresh. Therefore a hard repair relation can survive a later power cycle even though the payload values held during the earlier powered session do not.

For this bounded mechanism:

```text
persistent row-address -> spare-row relation
        !=
nonvolatile user payload
```

The source set also does not establish a universal operation that copies every current bit from the failing row into the spare row before substitution. Thus row-address continuity is not evidence of payload continuity during the repair transition.

---

## Engineering reconstruction: four kinds of continuity

A cross-mechanism analysis is safer if it asks four separate continuity questions.

### 1. Designation continuity

Does the interface-facing address/name remain usable as the same service slot?

Examples:

- Case 04: the virtual/logical designation remains the point through which the current value is requested even while physical placement changes;
- Case 14: the same LBA remains usable after sector reassignment;
- Case 89: the same logical sector keeps the same LBA across logical-CHS re-parameterization;
- Case 119: the same row address can continue to select storage after a spare row is substituted.

Designation continuity is therefore often the **strongest visible invariant** while lower layers change.

But it is not sufficient evidence for either value continuity or embodiment continuity.

### 2. Value continuity

Does the payload value before and after the transition count as the same current information?

The answer depends on the transition:

- Flash reclamation intends to carry still-current data to a new physical region before erasing the old unit;
- Flash logical rewrite intentionally replaces the old value with a new one while preserving the designation;
- SCSI reassignment explicitly does not itself guarantee survival of the old affected payload;
- DDR4 PPR evidence establishes future redirection but not a universal payload-copy operation;
- ATA CHS translation does not establish a payload change at all.

Thus `same address` is neither necessary evidence of a new value nor sufficient evidence of the old value's survival.

### 3. Resolution-relation continuity

Does the map/translator/repair state remain the same?

Often the answer is **no precisely because the higher-level designation is being preserved**.

- mapped Flash updates map/allocation state so a virtual designation can continue to work after a physical move;
- SCSI defect metadata changes so an existing LBA resolves to a replacement location;
- PPR repair state changes so the old row address selects a spare row;
- ATA logical-CHS translation can change one presentation relation while preserving the same stable LBA designation.

This yields an important correction:

> **The mapping relation can be constitutive of retained service without itself being the invariant object that remains unchanged.**

A relation may have to change so that another relation — designation-to-current-service meaning — remains usable.

### 4. Embodiment continuity

Does the same physical bearer remain responsible for the current state?

Case 04, Case 14, and Case 119 all supply mechanisms in which the answer can be no. Case 89 supplies the negative control: changing a presentation relation does not prove that the embodiment changed.

Physical sameness is therefore only one possible continuity criterion, not a universal definition of technical identity.

---

## Four transition classes

The phrase `remapping` is too broad for comparison unless the transition type is named. The grounded cases support at least four engineering classes.

### A. Presentation re-parameterization

```text
payload:          no change established
stable designation: preserved
presentation relation: changes
physical embodiment: no movement established
```

Bounded example: Case 89 logical-CHS translation around stable LBA identity.

This is an address-description transition, not evidenced as relocation.

### B. Failure-triggered replacement

```text
stable designation: preserved
resolution/replacement relation: changes
physical embodiment: replaced
payload continuity: separate question
```

Bounded examples: Case 14 SCSI defect reassignment and Case 119 DDR4 PPR.

The two mechanisms are not historically identical: one is drive-level block/defect management over magnetic media, the other device/platform row substitution inside volatile DRAM.

### C. Current-value relocation

```text
stable designation: preserved
intended current payload value: preserved/re-created
resolution relation: changes
physical embodiment: changes
old embodiment: later retired/reclaimed
```

Bounded example: Case 04 transfer/reclamation of active Flash blocks.

Here physical movement is part of preserving current value across a destructive erase/reclaim operation.

### D. Out-of-place logical update

```text
stable designation: preserved
payload value: intentionally changes
resolution relation: changes
physical embodiment: changes
old embodiment: becomes stale/deleted before later erase
```

Bounded example: Case 04 rewrite to an unwritten block.

This is not migration of an unchanged object. It is a logical update whose stable designation hides a value and embodiment transition beneath it.

---

## A relation matrix

| Case / transition | Designation continuity | Value continuity | Resolution relation | Physical embodiment | Old embodiment retirement |
| --- | --- | --- | --- | --- | --- |
| Case 89 CHS re-parameterization | LBA preserved | no payload change established | presentation mapping changes | movement not established | not applicable |
| Case 14 SCSI reassignment | LBA preserved | **not guaranteed by reassignment** | defect/replacement state changes | sector replaced | old defective sector no longer current; sanitize not established |
| Case 119 DDR4 PPR | row address preserved | universal copy/preservation not established | repair/decoder relation changes; hPPR may persist | spare row substituted | retired-row secure erase not established |
| Case 04 Flash active-data transfer | logical identity preserved | intended current value re-created elsewhere | logical/physical relation changes | Flash location changes | old unit later erased after current data copied |
| Case 04 Flash logical rewrite | virtual designation preserved | value intentionally changes | map/currentness changes | new unwritten block becomes current | old block marked deleted before later physical erase |

The matrix prevents a single phrase such as `the data moved` from hiding which invariant and which transition actually occurred.

---

## Mapping metadata as retained state — but not as the whole retained object

Case 04 and Case 14 make clear that mapping/defect metadata must survive or be reconstructible if the system is to know which lower-layer location currently counts. Case 119 shows a repair relation whose lifetime can be longer than ordinary payload lifetime. Case 89 shows that some current address-presentation state may be comparatively transient while another designation remains stable.

Therefore the project should keep two claims separate:

1. **mapping or repair metadata is itself retained technical state** when later resolution depends on it;
2. **the logical retained object is not therefore identical to that metadata**.

A user asking for `LBA n` or a virtual block normally wants the current value, not the defect list or map table as the payload object. Yet without the relation state, the service may no longer know which embodiment to return.

A better bounded model is:

```text
logical retained service
    = designation semantics
    + current-value state
    + sufficient resolution/currentness state
    + at least one usable current embodiment
    + procedures/resources that can maintain or replace that embodiment
```

This is an engineering decomposition, not a claim that every system literally stores one structure with those five fields.

---

## Replacement capacity is infrastructure, not identity

Case 14's spare sectors, Case 119's spare rows, and Case 04's free/transfer space show another recurring relation. Reserved capacity can be essential to future retention even while it is not part of the current user payload.

It should be described as **retention infrastructure / repair slack**, not silently counted as the logical object's current embodiment.

The distinction matters because exhaustion produces a different failure mode:

```text
current payload still readable
    + current designation still resolves
    + no replacement capacity remains
        -> present service may still work
        -> future repair margin is reduced or exhausted
```

Current correctness and future retainability are not the same state.

---

## Currentness and retirement are separate from physical destruction

Mapped Flash supplies the clearest example: an old block can be marked deleted/unusable before its erase unit is later physically erased. Case 14 likewise establishes that a reassigned LBA no longer uses the old defective sector without establishing a secure erasure contract for that retired physical sector. Case 119 similarly does not establish secure deletion of a retired DRAM row.

Therefore:

> **old embodiment no longer authoritative/current ≠ old embodiment physically destroyed ≠ old value forensically unrecoverable.**

This is the identity-side counterpart of the repository's sanitization work in Cases 44 and 47. Replacement answers `which embodiment counts now?`; sanitization answers a different question about how far obsolete embodiments have actually been made unavailable.

---

## Functional comparisons, not genealogy

The four cases share one bounded function: keeping some caller-visible service stable while an address representation, resolution relation, or physical bearer changes.

That does **not** establish a historical line such as:

```text
semiconductor spare rows
    -> disk defect reassignment
    -> Flash Translation Layer
    -> DDR4 PPR
```

No such genealogy is claimed.

The mechanisms solve different constraints:

- ATA logical CHS translation manages address presentation;
- disk defect reassignment manages media failure and spare substitution;
- mapped Flash manages erase-before-write geometry, out-of-place updates, and reclamation;
- DDR4 PPR manages defective-row substitution inside a volatile semiconductor array.

A similar relation type is an analytical bridge, not evidence of descent, shared terminology, or implementation identity.

---

## Historical, engineering, analogy, and philosophical boundaries

### Historical record

No new historical event is asserted here. Dates, mechanisms, period vocabulary, and source provenance remain controlled by Cases 04, 14, 89, and 119 and their grounding records.

External spot-checks in this synthesis round confirmed that the Ban patent explicitly describes virtual-to-physical remapping and unchanged logical-unit identity across physical movement, ATA-era text preserves an LBA across logical-CHS translation, and Lenovo's platform documentation still distinguishes boot-lifetime soft PPR from permanent hard PPR. Those checks do not expand the historical scope of the source cases.

### Engineering reconstruction

`designation continuity`, `value continuity`, `resolution relation`, `embodiment continuity`, and the four transition classes are project analytical terms. They are derived from the grounded mechanisms and should not be attributed to the historical actors unless a source uses equivalent language explicitly.

### Functional analogy

The cases are compared only where they preserve a higher-layer service across changed representation or bearer. Their physical media, triggers, lifetimes, and authority structures remain distinct.

### Philosophical interpretation

The cases permit a narrow later question about identity: technical sameness need not mean material sameness of one bearer. But they do **not** prove that technical identity is immaterial. The stable designation works only because material relation state, controllers/decoders, spare capacity, current embodiments, and maintenance procedures continue to exist.

A safer philosophical bridge is:

> **technical identity can be maintained through a rule-governed succession of embodiments, while the rule, value, designation, and bearer remain separately fallible material relations.**

That remains downstream of the engineering evidence.

---

## Counterexamples to common shortcuts

| Shortcut | Counterexample | Correct boundary |
| --- | --- | --- |
| `same address = same physical place` | Cases 04, 14, 119 | designation continuity != embodiment continuity |
| `same address = same value survived` | Case 14 reassignment | designation continuity != payload continuity |
| `mapping changed = data moved` | Case 89 CHS translation | presentation relation change != physical relocation |
| `physical relocation = logical update` | Case 04 active-data transfer | unchanged current value can be re-created at a new location |
| `persistent mapping = persistent payload` | Case 119 hPPR | repair-state lifetime != DRAM payload lifetime |
| `mapping metadata is merely metadata` | Cases 04 and 14 | resolution state can be constitutive of recoverable service |
| `mapping metadata is the logical object` | all four cases | infrastructure relation != user payload identity |
| `replacement = erasure` | Cases 04, 14, 119 | authority/currentness retirement != secure physical forgetting |
| `unused spare space = irrelevant capacity` | Cases 04, 14, 119 | reserved capacity can be future retention infrastructure |
| `similar remapping = shared genealogy` | all four cases | functional relation similarity != historical descent |

---

## Relation to other syntheses

[Synthesis 03](SYNTHESIS_03_ADDRESSABILITY_AND_CURRENTNESS.md) decomposes designation, resolution, currentness/admissibility, embodiment, and recovery more generally. Synthesis 15 narrows that framework onto **transitions in which representation, resolution, or embodiment changes** and tests what continuity actually survives.

[Synthesis 04](SYNTHESIS_04_AVAILABILITY_VS_PHYSICAL_PRESENCE.md) separates physical survival from usable availability. The present synthesis supplies one mechanism-level reason for that gap: payload bits can survive while the retained relation that identifies them as current is changed or lost.

[Synthesis 13](SYNTHESIS_13_DURABILITY_HANDOFF_PERSISTENCE_DOMAIN.md) concerns when state crosses persistence boundaries and what failure model is covered. Synthesis 15 instead asks **which state is being carried across a replacement or remapping transition**. A transition can preserve a designation yet fail to preserve a value, or preserve a relation across power loss while the payload remains volatile.

These syntheses compose but should not be merged into one universal lifecycle.

---

## What this synthesis does not close

The following remain open:

- a historical genealogy of logical/physical address indirection across disks, semiconductor repair, Flash controllers, virtual memory, filesystems, and distributed storage;
- exact terminology history for `mapping`, `remapping`, `relocation`, `reassignment`, `translation`, and `repair` across standards communities;
- whether later FTLs preserve mapping state through journals/checkpoints in one common pattern — Case 39 handles one crash-recovery slice only;
- empirical recovery after deliberate corruption of map/defect/PPR state;
- forensic reachability of retired HDD sectors, Flash pages, or DRAM rows after replacement;
- secure-erasure composition across every hidden stale embodiment;
- distributed-object identity when there are multiple simultaneous embodiments rather than one current lower-layer target;
- formal criteria for when a copied/reconstructed value counts as the `same` informational state rather than merely an equivalent value.

These require separate cases or syntheses.

---

## Bounded result

The roadmap question can be closed only in a typed form:

> **When a mapping or repair layer changes, there is no universal answer that the retained object is simply `the data`, `the address`, `the relation`, or `all three`. A defensible claim must separately audit designation continuity, payload-value continuity, resolution/currentness relation, and physical-embodiment continuity. Mapping state may be constitutive of a retained service while changing precisely to preserve a higher-level designation; an embodiment may be replaced without preserving its old payload; a presentation map may change without moving payload at all; and a persistent repair relation may outlive the volatile values it later governs.**

The four strongest counterexamples are deliberately asymmetric:

- **Case 89:** mapping/presentation can change without established physical movement;
- **Case 14:** embodiment replacement can preserve an LBA without automatically preserving its payload;
- **Case 119:** persistent repair relation can outlive volatile payload state;
- **Case 04:** one stable logical designation can cover both unchanged-value relocation and intentional out-of-place value replacement, depending on which transition is occurring.

That is a bounded engineering synthesis, not a universal metaphysics of identity and not a historical genealogy of remapping.