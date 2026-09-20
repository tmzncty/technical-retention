# Evidence 67G — OCP `Refresh Counts`: standardized integrity-maintenance accounting versus background data refresh

## Status

**`bounded deepening complete`** for the OCP telemetry-semantic boundary around `Refresh Counts` / SMART-10, and for the distinction between that counter and the OCP background-data-refresh obligation.

This packet deepens Case 67 after the PM9D3a telemetry packet (`67F`). It resolves one ambiguity left there: the PM9D3a field named `Refresh Counts` is **not merely an opaque Samsung label**. The same field name, byte range, and integrity-maintenance description are defined by the Open Compute Project (OCP) NVMe cloud/datacenter SSD specification.

It does **not** recover Samsung firmware internals, prove which PM9D3a events increment the field, prove that OCP SMART-10 counts exactly the events required by the OCP background-data-refresh section, or equate OCP `refresh` with DRAM refresh, NAND charge restoration, Case 36 correct-and-refresh, or SK hynix read reclaim.

Related canonical case: [`../cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md`](../cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md).

Related PM9D3a product-interface packet: [`67-samsung-pm9d3a-maintenance-telemetry-boundary-deepening.md`](67-samsung-pm9d3a-maintenance-telemetry-boundary-deepening.md).

---

## Question

Evidence 67F established that the Samsung PM9D3a datasheet separately exposes:

```text
Lifetime read Reclaim count
Patrol Read Reclaim Count
Refresh Counts
```

It deliberately stopped at the interface label and treated `Refresh Counts` as semantically underdefined.

The remaining bounded question was:

> Is `Refresh Counts` Samsung-local vocabulary, or does the OCP specification define what class of work the counter is intended to summarize?

The OCP primary sources answer that question strongly enough to narrow the boundary:

```text
OCP SMART-10 / Refresh Counts
    = count of blocks re-allocated to maintain data integrity
    != ordinary garbage-collection space creation
```

Later OCP wording also explicitly excludes block relocation due to wear leveling.

At the same time, OCP separately requires a device-level **background data refresh** process for powered-on retention. The two pieces are related by maintenance purpose, but the inspected specification text does not explicitly state that their event sets are identical.

Therefore the safe relation is:

```text
OCP background-data-refresh obligation
    != necessarily the exact event set counted by SMART-10
```

---

## Source custody and evidence grade

### Primary source A — OCP NVMe Cloud SSD Specification v1.0

Open Compute Project, **NVMe Cloud SSD Specification, Version 1.0 (03182020)**:

<https://www.opencompute.org/documents/nvme-cloud-ssd-specification-v1-0-3-pdf>

The document identifies Ross Stenfort and Ta-Yu Wu (Facebook) and Lee Prewitt (Microsoft) as authors and states that it defines requirements for a cloud-based NVMe SSD for datacenter use.

The OCP Storage Project approved-contributions page records:

- specification: `NVMe Cloud SSD Specification`;
- version: `v1.0`;
- submit date: **22 May 2020**;
- contributors: **Facebook, Microsoft**;
- license: **OWF CLA**.

OCP approved-contributions page:

<https://www.opencompute.org/wiki/Storage_Project_Approved_Contributions>

This packet treats the PDF itself as the primary technical source and the approved-contributions page as institutional provenance.

### Primary source B — later OCP Datacenter NVMe SSD specifications

Open Compute Project, **Datacenter NVMe SSD Specification, Version 2.6**:

<https://www.opencompute.org/documents/datacenter-nvme-ssd-specification-v2-6-2-pdf>

Open Compute Project, **Datacenter NVMe SSD Specification, Version 2.7**:

<https://www.opencompute.org/documents/datacenter-nvme-ssd-specification-v2-7-final-pdf>

The later specifications retain SMART-10 at bytes `87:81` and describe `Refresh Counts` as blocks re-allocated to maintain data integrity, while explicitly excluding ordinary garbage collection and wear-leveling relocation from the count.

### Product witness — Samsung PM9D3a

The product-level field remains grounded by the Samsung-authored PM9D3a U.2 datasheet mirror discussed in Evidence 67F:

- **Samsung SSD PM9D3a Specification (PCIe NVMe U.2), Rev. 1.3, May 2024**;
- mirrored at: <https://www.xfusion.com/wp-content/uploads/2025/11/PM9D3a-NVMe-U.2-Datasheet.pdf>.

Evidence 67F already records the custody caveat: this copy is publicly reachable and Samsung-authored, but is not hosted on a Samsung domain and carries `CONFIDENTIAL` markings.

OCP also has a public product page for the Samsung PM9D3a stating support for the OCP Datacenter NVMe SSD Specification v2.5:

<https://www.opencompute.org/products/441/samsung-pm9d3a-pcie-gen5-nvme-ssd>

This product page is useful for OCP/product association, not for reconstructing the firmware implementation of the counter.

---

## Historical record

### 1. `Refresh Counts` is already standardized in the 2020 v1.0 OCP specification

In the v1.0 SMART Cloud Attributes log page, requirement **SMART-10** assigns bytes `87:81` to:

```text
Refresh Counts
```

The field description says that it counts blocks that have been **re-allocated to maintain data integrity** and excludes creating free space due to garbage collection.

This is important because it moves the terminology boundary away from a 2024 Samsung-only reading:

```text
2020 OCP v1.0
    SMART-10 / 87:81 / Refresh Counts
        -> integrity-maintenance block reallocation accounting

2024 PM9D3a datasheet
    OCP cloud attribute 0xC0 / 87:81 / Refresh Counts
        -> product implementation of an OCP-defined field
```

Therefore:

```text
PM9D3a Refresh Counts
    != Samsung-local field name by default
```

The OCP definition is the stronger semantic prior for this specific OCP field.

### 2. OCP v1.0 separately requires background data refresh

Section **6.6 Background Data Refresh** of v1.0 contains three requirements:

- **BKGND-1**: the device shall support background data refresh while powered on to prevent data loss from power-on retention issues;
- **BKGND-2**: the design/test regime must account for normal NAND operating temperature;
- **BKGND-3**: background data refresh shall cover the entire device and be designed to run continuously in the background, not only during idle periods.

This is much stronger than a generic label such as `refresh supported`.

It establishes an explicit maintenance obligation with at least three dimensions:

```text
purpose
    -> prevent powered-on retention loss

coverage
    -> entire device

service regime
    -> continuously available in background,
       not restricted to idle periods
```

The specification does not expose the internal scan cursor, exact cadence, error threshold, victim-selection policy, relocation granularity, or scheduling algorithm.

### 3. `Refresh Counts` and `Background Data Refresh` are adjacent concepts, not proven identical event sets

The v1.0 document contains both:

```text
SMART-10 Refresh Counts
    -> blocks re-allocated to maintain data integrity
```

and:

```text
BKGND-1..3 Background Data Refresh
    -> powered-on retention protection
    -> whole-device coverage
    -> continuous background service
```

But the inspected passages do not explicitly cross-reference SMART-10 to BKGND-1..3 or state that every background-refresh relocation increments SMART-10 exactly once.

Nor do they state that SMART-10 is retention-only.

Therefore:

```text
same specification + related maintenance vocabulary
    != proof of one-to-one accounting identity
```

A controller may conceivably count a broader class of integrity-driven relocations under SMART-10, while background refresh remains one mandated maintenance regime. The primary text here does not resolve that mapping.

### 4. Later OCP wording sharpens the negative boundary

The later Datacenter NVMe SSD specification retains SMART-10 at bytes `87:81` and says the counter records blocks re-allocated to maintain data integrity.

By v2.6/v2.7, the exclusion is explicit for both:

```text
ordinary garbage collection
wear leveling
```

Thus the standardized telemetry category is intentionally **not** just “all internal block movement.”

The historical continuity is bounded:

```text
v1.0: exclude GC free-space creation
later: exclude GC and wear-leveling reallocation explicitly
```

This does not prove that all conforming devices before the later wording used identical accounting rules internally. It establishes the specification text, not hidden firmware history.

### 5. PM9D3a appears after this OCP field already existed

The PM9D3a Rev. 1.3 document is dated May 2024. OCP v1.0 predates it by roughly four years and already places `Refresh Counts` at the same `87:81` byte range.

That means the safest historical description is:

> PM9D3a exposes an already-standardized OCP maintenance counter alongside Samsung-specific or Samsung-documented reclaim counters.

It is not:

> Samsung invented the `Refresh Counts` category for PM9D3a.

---

## Engineering reconstruction

The following section is engineering reconstruction constrained by the specification. It is not firmware disclosure.

### 1. The host-visible counter is maintenance accounting, not the maintenance mechanism

The OCP field records a cumulative count of qualifying block reallocations.

It does not expose:

- source block identity;
- destination block identity;
- logical-page identity;
- reason code per event;
- retention age;
- ECC margin before relocation;
- read-disturb exposure;
- patrol-scan position;
- temperature history;
- whether one relocation repaired user data, metadata, or both;
- the scheduling decision that admitted the work.

Therefore:

```text
maintenance accounting counter
    != maintenance decision state
    != maintenance event log
    != physical media condition
```

### 2. The OCP field is more semantically bounded than Evidence 67F could previously establish

Evidence 67F correctly warned that a field name alone cannot prove a physical mechanism. The OCP source now supplies a stronger semantic boundary:

```text
Refresh Counts
    -> integrity-maintenance block reallocation count
```

So the field is no longer completely opaque.

But the stronger boundary still stops well before:

```text
retention-only relocation
read-disturb-only relocation
patrol-only relocation
physical charge refresh without relocation
exact Case 36 correct-and-refresh
```

None of those identities follows from SMART-10 alone.

### 3. OCP background refresh is a coverage obligation, not just an error-triggered reaction

BKGND-3 requires whole-device coverage and continuous background operation, including outside idle-only service.

Functionally this means the maintenance contract cannot be reduced to:

```text
host read fails
    -> repair the failed block
```

The specification instead requires a proactive service regime capable of covering data that may not be receiving host reads.

That creates a retention relation of the form:

```text
retained payload
    + powered-on time / temperature exposure
    -> background inspection/refresh obligation
    -> whole-device coverage requirement
```

The exact internal evidence used to select each block remains implementation-specific.

### 4. Coverage state, trigger state, and accounting state remain distinct

A device that satisfies BKGND-3 must in some way ensure whole-device coverage over time. That implies an implementation needs enough control state to avoid permanently omitting regions, but the specification does not prescribe what that state looks like.

Possible implementations could use scan cursors, age buckets, priority queues, block metadata, or other structures. Those are examples, not claims about PM9D3a.

The safe abstraction is:

```text
coverage-control state
    != trigger/qualification state
    != relocation/currentness state
    != SMART-10 accounting state
```

The host-visible seven-byte counter cannot substitute for the internal state needed to prove coverage.

### 5. Excluding GC and wear leveling makes trigger semantics part of telemetry meaning

Two physical operations may both copy valid data to a new block, yet only one may count toward SMART-10.

For example, at the functional level:

```text
copy because free space is needed
    -> GC class
    -> excluded from SMART-10

copy because wear distribution is being equalized
    -> wear-leveling class
    -> excluded in later OCP wording

copy to maintain data integrity
    -> SMART-10 accounting class
```

This shows why mechanism shape alone is insufficient to classify a maintenance event.

```text
same physical primitive (copy / reallocation)
    != same maintenance cause
    != same accounting category
```

### 6. A cumulative counter cannot prove completion of the coverage obligation

Suppose SMART-10 increases. That proves that qualifying integrity-maintenance reallocations were counted under the interface contract.

It does not prove:

- all device regions were inspected;
- the whole-device refresh cycle completed;
- no region is overdue;
- a particular logical payload was refreshed;
- the next scheduled maintenance point is safe.

So:

```text
Refresh Counts increased
    != whole-device refresh coverage proved
```

The counter is maintenance evidence, but not complete maintenance authority.

---

## Controlled functional comparisons

### Versus Samsung PM9D3a `Lifetime read Reclaim count`

PM9D3a exposes both the Samsung-documented lifetime read-reclaim field and OCP SMART-10.

The OCP source now lets the repository strengthen the distinction:

```text
Lifetime read Reclaim count
    = vendor/product reclaim accounting vocabulary

OCP Refresh Counts
    = standardized integrity-maintenance block-reallocation accounting vocabulary
```

This does **not** prove disjoint underlying event sets.

A single physical relocation could theoretically satisfy more than one internal accounting rule; the inspected documentation does not tell us whether PM9D3a does that.

### Versus PM9D3a `Patrol Read Reclaim Count`

The patrol counter remains less well specified publicly than OCP SMART-10.

The safe relation is:

```text
patrol-associated reclaim counter
    != OCP integrity-maintenance reallocation counter
```

at the interface level.

Whether patrol work is one source of SMART-10 increments remains open.

### Versus Case 36 — Flash Correct-and-Refresh

Case 36 concerns a more specific correct-and-renew function.

OCP SMART-10 supplies host-visible accounting for integrity-driven block relocation, while OCP BKGND-1..3 supplies a system-level background refresh obligation.

The functional resemblance is real but bounded:

```text
OCP background data refresh
    ~= proactive physical maintenance for retention
```

but:

```text
OCP wording
    != proof of Case 36's exact trigger / correction / rewrite sequence
```

### Versus DRAM refresh

OCP background refresh is whole-device storage maintenance involving NAND data integrity over long operating intervals.

DRAM refresh is periodic restoration of volatile cell charge required for ordinary continued representation.

Therefore:

```text
same English word "refresh"
    != same retention timescale
    != same physical failure process
    != same address scheduler
    != same rewrite primitive
```

### Versus Case 52 / read disturb

Read disturb can create an integrity-maintenance need. OCP SMART-10 does not say that read disturb is the only qualifying cause.

Thus:

```text
read-disturb repair may be integrity maintenance
    != SMART-10 is a read-disturb counter
```

### Versus garbage collection and wear leveling

This is the strongest negative comparison because the OCP text itself draws the boundary.

```text
integrity-maintenance relocation
    != ordinary GC relocation
    != wear-leveling relocation
```

The physical copy machinery may overlap; the maintenance reason and accounting category differ.

---

## Historical / engineering / comparison / interpretation ledger

| ID | Layer | Claim | Boundary |
| --- | --- | --- | --- |
| H-67G.1 | Historical record | OCP NVMe Cloud SSD Specification v1.0 is dated 2020 and OCP records it as an accepted contribution on 2020-05-22 | OCP primary/institutional sources |
| H-67G.2 | Historical record | v1.0 SMART-10 assigns bytes `87:81` to `Refresh Counts` | direct OCP specification |
| H-67G.3 | Historical record | v1.0 defines SMART-10 as blocks re-allocated to maintain data integrity and excludes GC free-space creation | direct OCP specification |
| H-67G.4 | Historical record | v1.0 BKGND-1 requires powered-on background data refresh against retention loss | direct OCP specification |
| H-67G.5 | Historical record | v1.0 BKGND-3 requires entire-device coverage and continuous background operation, not idle-only execution | direct OCP specification |
| H-67G.6 | Historical record | later OCP Datacenter NVMe SSD specs retain SMART-10 and explicitly exclude ordinary GC and wear-leveling relocation | direct OCP specification |
| H-67G.7 | Historical record | PM9D3a later exposes OCP `Refresh Counts` at the same byte range in its documented cloud-attribute page | Samsung-authored product evidence; custody caveat in 67F |
| E-67G.1 | Engineering reconstruction | SMART-10 is an accounting surface, not a complete maintenance state machine | counter form + missing implementation detail |
| E-67G.2 | Engineering reconstruction | whole-device refresh coverage requires more control information than a cumulative count alone supplies | follows from BKGND-3 obligation |
| E-67G.3 | Engineering reconstruction | the same relocation primitive may belong to different maintenance classes depending on why work was admitted | OCP explicitly excludes GC/wear leveling from SMART-10 |
| E-67G.4 | Engineering reconstruction | an increment in SMART-10 cannot prove completion of a whole-device refresh pass | cumulative count lacks coverage identity |
| F-67G.1 | Functional comparison | OCP background refresh and Case 36 both concern proactive physical renewal, but exact mechanisms are not equated | cross-case only |
| F-67G.2 | Functional comparison | OCP `refresh` and DRAM `refresh` share vocabulary but not a demonstrated physical/control identity | terminology boundary |
| F-67G.3 | Functional comparison | Samsung reclaim/patrol counters and OCP SMART-10 are distinct interface categories; event-set overlap remains unknown | PM9D3a + OCP sources |
| I-67G.1 | Interpretation | maintenance telemetry can preserve evidence that work occurred without preserving enough state to prove full maintenance coverage | downstream project interpretation only |

---

## Explicit non-claims

This packet does **not** claim that:

1. OCP invented background NAND data refresh;
2. OCP invented integrity-driven block relocation;
3. OCP invented SMART or NVMe health telemetry;
4. SMART-10 was first implemented commercially in 2020;
5. every NVMe SSD implements OCP SMART-10;
6. every OCP-compliant SSD uses the same internal refresh algorithm;
7. every PM9D3a firmware branch implements identical accounting semantics;
8. the mirrored PM9D3a datasheet has official Samsung public-distribution custody;
9. PM9D3a's OCP support statement proves conformance to every optional requirement in every OCP revision;
10. SMART-10 counts only retention-triggered relocations;
11. SMART-10 counts read-disturb repair specifically;
12. SMART-10 counts patrol-read reclaim specifically;
13. every background-refresh relocation increments SMART-10;
14. every SMART-10 increment comes from BKGND-1 background refresh;
15. one relocated block always produces exactly one counter increment under every implementation;
16. the counter is an event log with block identities or timestamps;
17. the counter proves which logical payload was moved;
18. the counter proves the source block became unreadable;
19. relocation implies the source block was already uncorrectable;
20. relocation implies secure erasure of the source embodiment;
21. `Refresh Counts` is physically analogous to DRAM row refresh;
22. `Refresh Counts` proves charge restoration in place;
23. OCP background refresh uses an in-place rewrite rather than relocation;
24. OCP background refresh uses relocation rather than some other safe renewal path in every case;
25. BKGND-3 prescribes a particular scan cursor implementation;
26. BKGND-3 prescribes a fixed refresh interval;
27. BKGND-3 proves all blocks receive equal refresh frequency;
28. later wording that excludes wear leveling proves earlier implementations counted wear-leveling work;
29. later OCP revisions preserve every v1.0 detail unchanged;
30. PM9D3a's `Lifetime read Reclaim count`, `Patrol Read Reclaim Count`, and OCP `Refresh Counts` have disjoint event sets;
31. the three counters have identical persistence/reset semantics;
32. a `Lifetime` counter necessarily survives every power-loss interleaving;
33. SMART-10 itself is the authority that decides which block is current after relocation;
34. increasing SMART-10 proves the background refresh coverage obligation is currently satisfied;
35. zero SMART-10 proves no integrity maintenance occurred;
36. zero SMART-10 proves no retention risk exists;
37. the OCP specification is a disclosure of Samsung controller microcode;
38. the OCP specification is a disclosure of SK hynix controller microcode;
39. functional similarity establishes genealogy among OCP, Samsung, SK hynix, or earlier refresh schemes;
40. the philosophical interpretation below is terminology used by the historical actors.

---

## Philosophical / media-theoretical interpretation

This section is downstream interpretation only.

The OCP split is useful because it shows at least three different kinds of retained relation around maintenance:

```text
payload state
    -> what must remain recoverable

maintenance-control state
    -> what the controller needs in order to decide / schedule / cover work

maintenance-accounting state
    -> host-visible evidence that some class of work occurred
```

A telemetry counter can outlive many individual maintenance events while remaining radically less informative than the internal maintenance state that produced them.

Therefore:

> **retaining evidence that maintenance happened is not the same as retaining enough evidence to prove the maintenance obligation is satisfied.**

That distinction is a project-level interpretation. It is not attributed to OCP authors or Samsung engineers.

---

## What this closes

This packet closes the narrow debt left by Evidence 67F:

```text
"What does PM9D3a OCP Refresh Counts mean?"
```

at the standardized interface level.

The answer is now bounded to:

```text
OCP SMART-10
    -> count of blocks re-allocated to maintain data integrity
    -> excludes ordinary GC
    -> later wording also explicitly excludes wear leveling
```

It also establishes that OCP separately mandates powered-on, whole-device, continuously available background data refresh for retention protection.

What it does **not** close is the product-internal mapping between those two OCP concepts or between SMART-10 and Samsung's two reclaim counters.

---

## Remaining evidence debt

High-value follow-up is now narrower:

1. **PM9D3a counter overlap experiment** — determine whether controlled patrol/background/read-heavy workloads increment `Lifetime read Reclaim count`, `Patrol Read Reclaim Count`, and OCP SMART-10 independently or together.
2. **Persistence/reset semantics** — establish behavior of all three counters across normal power cycle, sudden power loss, firmware update, format, sanitize, and namespace operations.
3. **Coverage evidence** — find vendor/OCP qualification material that shows how whole-device background refresh coverage is validated rather than merely required.
4. **Versioned OCP diff** — trace exact wording changes to SMART-10 and BKGND requirements across v1.0, v2.0, v2.5, v2.6, and v2.7 without assuming semantic changes where only editorial text changed.
5. **Samsung implementation evidence** — find firmware/tooling/qualification material that says which PM9D3a maintenance events increment OCP SMART-10.
6. **Patrol semantics** — find a manufacturer-primary definition of `Patrol Read Reclaim Count`, including cadence/coverage/trigger relations.

---

## Related-repository routing

A search of `tmzncty/computing-archaeology` for OCP / NVMe SSD / `Refresh Counts` did not surface an existing dedicated packet to reuse in this slice.

If broader historical work is added later, route these topics to `computing-archaeology` rather than expanding this case into a general NVMe/OCP history:

- OCP storage-project institutional history;
- NVMe vendor-unique/cloud log-page genealogy;
- Meta/Facebook + Microsoft cloud-SSD specification history;
- vendor adoption chronology;
- OCP conformance tooling and certification history;
- NVMe telemetry standardization beyond the retention-specific seam.

Keep this repository focused on the retention relation:

```text
integrity-maintenance obligation
    -> background coverage / renewal work
    -> host-visible maintenance accounting
```

and on the boundaries among those layers.

---

## Sources

### Primary / institutional

- Open Compute Project, **NVMe Cloud SSD Specification, Version 1.0 (03182020)**: <https://www.opencompute.org/documents/nvme-cloud-ssd-specification-v1-0-3-pdf>
- Open Compute Project, **Storage Project Approved Contributions**: <https://www.opencompute.org/wiki/Storage_Project_Approved_Contributions>
- Open Compute Project, **Datacenter NVMe SSD Specification, Version 2.6**: <https://www.opencompute.org/documents/datacenter-nvme-ssd-specification-v2-6-2-pdf>
- Open Compute Project, **Datacenter NVMe SSD Specification, Version 2.7**: <https://www.opencompute.org/documents/datacenter-nvme-ssd-specification-v2-7-final-pdf>
- Open Compute Project, **Samsung PM9D3a PCIe Gen5 NVMe SSD** product page: <https://www.opencompute.org/products/441/samsung-pm9d3a-pcie-gen5-nvme-ssd>

### Product-interface source with custody caveat

- Samsung Electronics, **Samsung SSD PM9D3a Specification (PCIe NVMe U.2), Rev. 1.3, May 2024**, xFusion-hosted mirror: <https://www.xfusion.com/wp-content/uploads/2025/11/PM9D3a-NVMe-U.2-Datasheet.pdf>

### Existing repository packets

- [`67-samsung-pm9d3a-maintenance-telemetry-boundary-deepening.md`](67-samsung-pm9d3a-maintenance-telemetry-boundary-deepening.md)
- [`67-samsung-pm963-2016-2018-read-reclaim-telemetry-deepening.md`](67-samsung-pm963-2016-2018-read-reclaim-telemetry-deepening.md)
- [`../cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md`](../cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md)
