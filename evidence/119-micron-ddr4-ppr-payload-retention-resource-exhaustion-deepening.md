# Evidence 119 — Micron DDR4 PPR payload-retention and repair-resource bounds

## Purpose

This record deepens [`../cases/119-ddr4-post-package-repair-row-remapping.md`](../cases/119-ddr4-post-package-repair-row-remapping.md) around two explicit evidence debts left by the first-pass PPR grounding:

1. what a DDR4 PPR sequence does and does not promise about **payload preservation while a row is repaired**; and
2. what happens when the device has **no repair resource left** for the requested bank.

The bounded result is deliberately narrower than a JEDEC-wide PPR genealogy. It uses Micron-authored DDR4 product documentation as a manufacturer witness and keeps product behavior, engineering reconstruction, cross-case analogy, and philosophical interpretation separate.

**Cross-vendor follow-on:** [`119-samsung-2014-ddr4-ppr-cross-vendor-resource-transition-deepening.md`](119-samsung-2014-ddr4-ppr-cross-vendor-resource-transition-deepening.md) now compares this Micron product envelope against Samsung's September/October 2014 DDR4 operation document. It closes the bounded claim that shared `PPR` / `sPPR` vocabulary does **not** imply identical repair-resource geometry or identical soft-to-hard transition preconditions. SK hynix, exact JEDEC adoption chronology, and hidden physical spare/fuse topology remain open.

## Evidence classification

- **H/P** — historical / manufacturer-primary technical record.
- **E** — engineering reconstruction constrained by that record.
- **A** — bounded functional analogy only.
- **I** — project-level philosophical interpretation, not source vocabulary.
- **X** — explicitly rejected stronger inference.

---

## Source A — Micron 16Gb DDR4 SDRAM, Rev. G, August 2020

### Identity and provenance

Micron Technology, **16Gb: x4, x8, x16 DDR4 SDRAM**, document family `16gb_ddr4_dram.pdf`, Rev. G, `08/2020`, including the `sPPR Row Repair` and `Hard Post Package Repair` sections.

Publicly indexed copies used for this deepening include:

- TI E2E-hosted copy / extraction:
  <https://e2echina.ti.com/cfs-file/__key/communityserver-discussions-components-files/120/MT40A1G16-16gb_5F00_ddr4_5F00_sdram.pdf>
- NXP Community-hosted copy:
  <https://community.nxp.com/pwmxy87654/attachments/pwmxy87654/Layerscape/12126/2/MICT_S_A0010972464_1-2574446.pdf>
- indexed HTML extraction of the relevant Micron page:
  <https://htmlapp.alldatasheet.com/html-pdf/2170148/MICRON/MT40A512M16PM-068AT%3AG/36985/136/MT40A512M16PM-068AT%3AG.html>

The document text and copyright are Micron's; the presently accessible copies are public mirrors rather than a stable Micron-hosted archive. That provenance limitation is retained explicitly.

### sPPR: preserving data requires an explicit backup / restore obligation

The `sPPR Row Repair` section states that the bank receiving the sPPR change is expected to retain array data **except for the seed row and its associated row addresses**. It then makes the preservation condition explicit: if data in the bank under repair must be retained, the seed row and associated rows should be **backed up before sPPR and restored after sPPR completes**.

The same section gives a table of associated-row address bits and says that the association matters specifically when the bank's data must be retained.

Historical record safely established:

```text
sPPR mapping change
    does not by itself preserve every affected payload bit

required payload preservation
    -> backup relevant seed/associated rows
    -> perform sPPR
    -> restore backed-up data
```

This is stronger evidence than the original Case-119 negative statement that “row replacement does not prove data migration.” The manufacturer documentation positively identifies a **separate payload-preservation workflow around the repair operation**.

### Repair-resource exhaustion: capability does not imply remaining capacity

The same Micron section states that when the hard-PPR resource for a bank is used up, that bank should be assumed not to have available resources for soft PPR. It then states that if a repair sequence is issued to a bank with **no repair resource available**, the DRAM **ignores the programming sequence**.

This establishes a concrete finite-capacity boundary:

```text
PPR feature supported by device
    != repair resource available for this bank now

repair sequence issued
    != new repair mapping necessarily installed
```

The source supports a bank-scoped resource-exhaustion behavior for this documented Micron family. It does not support a universal spare-row count or topology across all DDR4 products.

---

## Source B — Micron 8Gb DDR4 SDRAM hPPR sequence witness

### Identity and provenance

Micron Technology, **8Gb: x4, x8, x16 DDR4 SDRAM**, publicly indexed manufacturer datasheet copies include Rev. L (`09/2017`) and later revisions. Representative public extraction:

<https://www.micron-electronic.com/pdf-80/mt40a1g8sa-075-h.pdf>

A page-preserving HTML extraction is also publicly indexed for the Micron 8Gb family:

<https://www.alldatasheet.com/html-pdf/2171300/MICRON/MT40A512M16TB-075E%3AH/35765/132/MT40A512M16TB-075E%3AH.html>

### hPPR exposes two different data-retention envelopes

The Micron `Hard Post Package Repair` section describes **two forms of hPPR command sequence**:

- the first uses `WRA` and supports data retention with refresh, subject to the documented exception/scope around the bank containing the repaired row;
- the second uses `WR`, cannot perform refresh in that sequence, and **does not support data retention for the target DRAM**.

The important historical point is not that one mode is “better.” It is that **persistent row repair and payload-retention behavior are independent enough to have distinct command-sequence envelopes in the same product family**.

Safe use:

> a permanent/persistent hPPR result does not, by itself, imply that the payload present before the repair transition was retained through that transition.

Unsafe use:

> every hPPR destroys data, or every hPPR preserves data.

The actual documented answer depends on the selected sequence and its refresh/data-retention envelope.

---

## Cross-source engineering reconstruction

### 1. Persistent remapping and payload preservation are different obligations

The original case already separated the lifetime of the repair mapping from ordinary DRAM volatility. The direct PPR sequence text makes a second separation possible:

```text
logical row-address continuity
    != repair-mapping persistence
    != payload preservation across repair
```

A PPR operation can establish or change which physical row answers to an address while payload preservation is handled by a different mechanism or workflow.

For sPPR, Micron explicitly exposes that separation through backup/restore of seed and associated rows. For hPPR, Micron exposes two command sequences with different data-retention envelopes.

### 2. “Repair succeeded” is not identical to “repair was requested”

The resource-exhaustion rule gives a clean counterexample:

```text
PPR command path exists
    + repair sequence is issued
    + no repair resource remains
    -> programming sequence ignored
```

Therefore:

> **repair invocation != repair-state transition.**

Any platform telemetry that records an attempted PPR needs a separate completion/success signal before it can safely be treated as evidence that a new spare-row relation was installed.

### 3. Repair capacity is itself retained maintenance infrastructure

A spare/repair resource is not ordinary user payload, but its availability changes whether future row defects remain repairable. Consuming a hard repair resource therefore changes the device's future maintenance option set.

Bounded reconstruction:

> **maintainability has state.**

More concretely:

```text
remaining repair resource
    -> constrains admissible future PPR transitions
```

This does not imply that the resource is exposed as a host-readable scalar, nor that every vendor allocates it in the same geometry.

### 4. Data-retaining repair is a compound protocol

For the bounded sPPR path, “preserve the bank's data while changing repair state” is not one indivisible operation. It is a compound protocol:

```text
identify affected seed/associated rows
    -> back up payload
    -> perform repair/remap transition
    -> restore payload
```

That permits a stronger methodological distinction:

> **address identity preservation != payload migration != payload restoration.**

All three may participate in a successful maintenance episode, but they are not the same retained relation.

---

## Functional comparison only

### Case 14 — SCSI defect reassignment

[`../cases/14-scsi-disk-defect-reassignment-logical-identity.md`](../cases/14-scsi-disk-defect-reassignment-logical-identity.md) remains the closest bounded comparison. Both cases can preserve an externally meaningful address while substituting a defective physical embodiment, and both force the researcher to ask separately how payload continuity is achieved.

The analogy stops there. Disk reassignment operates through drive-level block/defect machinery; DDR4 PPR operates inside a volatile semiconductor array with row-repair resources and PPR command sequences.

### Case 04 — mapped Flash

[`../cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md) provides another identity/location comparison, but Flash relocation is governed by erase/program/reclamation and FTL metadata rather than DDR4 row-repair semantics.

### Finite maintenance-resource analogy

A consumed DDR4 repair resource can be compared functionally with exhausted disk spare-sector or Flash spare-block capacity only at the abstract level:

> finite hidden maintenance capacity can determine whether a future defect is still repairable.

No common physical mechanism, resource geometry, controller policy, or genealogy is claimed.

---

## Philosophical / media-theoretical interpretation

Project interpretation only:

> technical persistence can require preserving both a **relation of identity** and enough **maintenance possibility** to re-establish a usable embodiment later.

Case 119 now shows that these are separable from payload survival. A logical address may remain callable through a new row; the mapping may persist; the payload may require backup/restore; and future repairability may still be reduced because a finite repair resource has been consumed.

This is not Micron's historical vocabulary. It is a repository-level interpretation constrained by the engineering record.

---

## Explicit stop conditions

This deepening does **not** establish any of the following:

1. **No universal DDR4 resource count.** The documented Micron family is not projected onto Samsung, SK hynix, other Micron densities/revisions, or later DDR generations.
2. **No universal physical spare topology.** “Repair resource” is kept at the interface/documentation level unless a source directly identifies the underlying physical implementation.
3. **No claim that every sPPR preserves the whole bank automatically.** The source instead requires explicit backup/restore for the seed/associated rows when their data must survive.
4. **No claim that every hPPR preserves data.** Micron documents two command sequences with different retention envelopes.
5. **No claim that every hPPR destroys data.** One documented hPPR sequence supports data retention under its stated refresh conditions.
6. **No claim that an issued PPR command changed the mapping.** With no repair resource available, the documented DRAM ignores the programming sequence.
7. **No sanitization inference.** Backing up/restoring data, retiring a row, consuming a spare, or establishing a permanent repair mapping does not prove that the old physical row has been overwritten, erased, degaussed, or rendered forensically unrecoverable.
8. **No JEDEC-first claim.** This record does not establish when hPPR/sPPR first entered JESD79-4 or which ballot introduced the relevant behavior.
9. **No direct genealogy claim.** The older redundant-row patent floor in the base evidence is not turned into a proven line of descent to Micron's DDR4 PPR.

---

## Related-repository check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `PPR`, `DDR4`, and `Post Package Repair` found no dedicated PPR technical-history module to reuse. Broader semiconductor redundancy chronology, vendor implementation history, and exact JEDEC adoption chronology should still be routed there rather than duplicated here if developed later.

---

## Result

This slice closes two bounded Case-119 debts for the cited Micron DDR4 families:

```text
persistent PPR mapping
    != automatic payload preservation

sPPR payload preservation when required
    -> explicit backup + repair + restore workflow

PPR capability
    != currently available repair resource

repair sequence issued
    != repair mapping changed

row retired / mapping changed
    != retired physical row sanitized
```

The Samsung follow-on now closes the narrower **cross-vendor operation-contract** question: the same public PPR vocabulary can coexist with different repair-resource geometry and different soft-to-hard transition preconditions. Remaining work is narrower: exact JEDEC chronology, SK hynix comparison, named Samsung/Micron product-level physical implementation evidence, named-platform completion telemetry, and physical/fault characterization of repair-resource topology/exhaustion.