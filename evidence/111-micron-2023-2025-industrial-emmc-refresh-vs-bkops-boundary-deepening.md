# Case 111 deepening — Micron industrial e.MMC refresh versus generic BKOPS

Canonical case: [`../cases/111-enterprise-ssd-extended-shutdown-maintenance.md`](../cases/111-enterprise-ssd-extended-shutdown-maintenance.md)

**Status:** bounded evidence deepening; Case 111 remains `grounded`.

## Research question

A previous Case-111 slice established that JEDEC e.MMC exposes a generic background-maintenance control surface (`BKOPS_SUPPORT`, `BKOPS_STATUS`, `BKOPS_START`, `BKOPS_EN`, `PERIODIC_WAKEUP`) but that generic BKOPS completion must not be promoted into retention-refresh completion without a named product source that explicitly binds the two.

This slice asks a narrower product-level question:

> On a named commercial e.MMC family that explicitly advertises retention-oriented refresh, does the public product datasheet identify that refresh as the same thing as BKOPS, or expose a refresh-specific completion/status relation through the public ECSD table?

The bounded answer from Micron's 32/64/128/256GB industrial e.MMC documentation is **no**. The family publicly lists `BKOPS control`, `Auto initiated refresh`, and `Host initiated refresh` as separate features. Its public ECSD table exposes the standard BKOPS support/status/start/enable fields, while the same datasheet does not identify a refresh-specific status/completion field or state that `BKOPS_STATUS` certifies completion of Micron refresh.

That is useful negative evidence because it sharpens the evidentiary bar:

```text
same managed-Flash product supports BKOPS
    + same product supports named refresh features

therefore:
BKOPS support/completion
    != source-level proof that refresh is what completed
```

This is a product-interface boundary, not a claim about hidden firmware implementation.

---

## Sources and exact document floor

### Micron industrial e.MMC Rev. F — October 2023

Micron-authored datasheet:

- **32GB, 64GB, 128GB, 256GB: Industrial e.MMC**
- document identifier `CCM005-841846911-10503`
- **Rev. F — 10/2023**
- product family includes `MTFC32GBCAQTC-IT`, `MTFC64GBCAQTC-IT`, `MTFC128GBCAQTC-IT`, `MTFC256GBCAQTC-IT` and WT variants.

Inspected mirror:

- <https://datasheet.octopart.com/MTFC32GBCAQTC-IT-Micron-datasheet-176140705.pdf>

The first page lists, in the same product feature block:

- JEDEC/MMC 5.1 compliance;
- `BKOPS control`;
- `Auto initiated refresh`;
- `Host initiated refresh`;
- device health reporting;
- background operation;
- power-off notification;
- a retention line of **1 year at 55°C at maximum PE** and **2 years at 55°C at 10% of maximum PE**.

The Product Features page separately lists `Host initiated refresh` and `Auto initiated refresh` under the main Micron-supported features.

The revision history explicitly says Rev. F updated the Features section by **adding** `auto initiated refresh` and `host initiated refresh` (along with other product-feature documentation).

### Micron industrial e.MMC Rev. I — January 2025

Micron-authored datasheet:

- same document identifier `CCM005-841846911-10503`;
- **Rev. I — 01/2025**.

Inspected distributor mirror:

- <https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/8606/industrial-emmc-32-64-128-256gb.pdf>

Rev. I still lists:

- `BKOPS control`;
- `Auto initiated refresh`;
- `Host initiated refresh`;
- background operation;
- power-off notification.

Its Architecture page also recommends use of Power Off Notification and a refresh mechanism as a best practice in the context of proper data loading/storage over device life.

Its revision history says Rev. I **removed retention values from Features**. That is a documentation change. It is not evidence that the physical product suddenly lost or gained a particular retention mechanism in January 2025.

---

## Historical / source record

### H1 — BKOPS and Micron refresh are separately named capabilities

Both the directly inspected Rev. F and Rev. I feature lists put `BKOPS control`, `Auto initiated refresh`, and `Host initiated refresh` on separate bullets.

Safe source-level claim:

```text
Micron public product vocabulary in this family
contains generic BKOPS vocabulary
and separately named Micron refresh vocabulary.
```

Unsafe upgrade:

```text
therefore BKOPS and refresh are implemented by wholly independent firmware engines
```

The public datasheet does not disclose enough firmware detail for that conclusion.

### H2 — the public ECSD table exposes generic BKOPS fields

Rev. I's ECSD table exposes the standard e.MMC control/status surface, including:

```text
BKOPS_SUPPORT   ECSD[502]
BKOPS_STATUS    ECSD[246]
BKOPS_START     ECSD[164]
BKOPS_EN        ECSD[163]
PERIODIC_WAKEUP ECSD[131]
```

The documented values for this product include `BKOPS_SUPPORT = 01h` and `BKOPS_EN = 02h` in the published table.

The same ECSD table also contains a vendor-proprietary health-report region and vendor-specific fields, but the public datasheet does not decode those as a refresh-progress/completion interface.

### H3 — no public refresh-specific completion field is identified in the inspected datasheet

The inspected Rev. F / Rev. I public documentation names host-initiated and auto-initiated refresh, but does **not** identify a public ECSD field as:

- refresh progress;
- refresh coverage;
- refresh completion;
- retention-refresh completion;
- last-refresh cursor;
- whole-device refresh epoch.

This is a bounded document finding, not a claim that no such state exists internally or in non-public Micron material.

### H4 — Rev. F couples refresh documentation with an explicit retention envelope

Rev. F is particularly useful because the same first-page product feature block contains both refresh features and a stated power-off retention envelope:

```text
1 year @ 55°C at maximum PE
2 years @ 55°C at 10% of maximum PE
```

That makes this a stronger retention-relevant witness than a generic e.MMC datasheet that merely mentions background maintenance.

However, adjacency in a feature list is not an interface-semantic equation. Rev. F does not say that `BKOPS_STATUS = 0` means those retention-oriented refresh obligations have completed.

---

## Engineering reconstruction

The project can safely reconstruct four distinct relations:

```text
retention envelope / requirement
    != refresh capability
    != generic background-work control
    != refresh-specific completion evidence
```

For this named product family:

```text
Micron refresh capability
    = publicly named

JEDEC-style BKOPS control/status
    = publicly exposed

public binding:
BKOPS completion -> retention-refresh completion
    = not established in the inspected datasheet
```

The strongest useful anti-collapse is therefore:

```text
same product has BKOPS
    + same product has refresh
    != BKOPS_STATUS is a refresh-completion certificate
```

This is stronger than the previous standards-only warning because it now comes from one concrete commercial product family containing both feature classes.

### Host-initiated does not automatically mean host-observable completion semantics are complete

`Host initiated refresh` proves that the host can cause or request a Micron-defined refresh operation under some documented product contract.

It does **not** by itself prove that the public datasheet gives the host:

- a coverage denominator;
- an exact progress cursor;
- an operation-generation identifier;
- a terminal success/failure code specific to refresh;
- proof that every retention-sensitive physical region was rewritten.

Therefore:

```text
host can initiate
    != host can independently certify whole-device completion
```

### Generic completion may still be useful without identifying the maintenance class

The e.MMC BKOPS interface remains useful evidence that a bounded generic maintenance run can be admitted and completed.

But if several internal maintenance classes can share that execution opportunity, then a generic completion relation does not by itself identify which hidden obligation was satisfied.

Project reconstruction:

```text
maintenance execution completion
    != maintenance-class attribution
    != whole-device refresh-coverage completion
```

---

## Documentation-lineage boundary

Rev. F's revision history says the refresh feature bullets were added to the datasheet in October 2023.

That establishes a conservative public-documentation floor for this exact surviving datasheet lineage:

```text
October 2023 documentation floor
    != October 2023 implementation date
    != October 2023 invention date
    != first Micron refresh product
```

Likewise, Rev. I's January-2025 removal of the numeric retention lines is only a documentation-revision fact:

```text
retention values removed from feature page
    != physical retention suddenly removed
    != refresh mechanism removed
```

The refresh bullets remain present in Rev. I.

---

## Functional comparisons

### Case 111 eMMC standards slice

The standards slice established:

```text
BKOPS support
    != current maintenance debt
    != admitted run
    != completed run
```

This Micron slice adds:

```text
completed generic run
    != source-identified refresh completion
```

The comparison is at interface semantics. It is not a JEDEC-to-Micron genealogy claim beyond Micron's explicit e.MMC 5.1 compliance.

### Case 135 — automotive eMMC self-refresh

Case 135 remains a useful counterexample to treating all e.MMC maintenance as one thing. A product can expose or document a retention-specific refresh mechanism while also implementing the generic e.MMC maintenance framework.

This Micron evidence reinforces that distinction but does not establish identical triggers, firmware, scan geometry, or coverage semantics across vendors.

### Case 67 — OCP background refresh / refresh counters

Case 67 already separates maintenance activity accounting from whole-device coverage completion.

The Micron product makes a parallel interface point:

```text
named refresh feature exists
    != public completion/coverage authority is exposed
```

No OCP/e.MMC implementation identity is asserted.

---

## Philosophical interpretation

A narrow permissible interpretation is that a maintenance obligation may be technically real and operator-relevant even when the public interface exposes only partial authority over it.

The host can know that a device supports refresh, can know that generic background work exists, and can still lack a public retention-specific completion certificate.

That is a difference between **the existence of maintenance**, **the ability to invoke maintenance**, and **the ability to know exactly what maintenance has been completed**.

Do not turn this into a universal claim that hidden firmware is unknowable or that all vendor health state is opaque.

---

## Explicit non-claims

This packet does **not** claim:

1. BKOPS never performs refresh on this Micron product.
2. BKOPS always performs refresh on this Micron product.
3. Host-initiated refresh is implemented outside the BKOPS scheduler.
4. Auto-initiated refresh is implemented inside the BKOPS scheduler.
5. `BKOPS_STATUS = 0` proves no refresh work is pending.
6. `BKOPS_STATUS = 0` proves refresh is complete.
7. The public ECSD table exposes all vendor-internal maintenance state.
8. Vendor-proprietary health-report bytes do not contain useful refresh information.
9. The vendor-specific ECSD region has no refresh semantics.
10. Rev. F's numeric retention envelope is a deterministic failure deadline.
11. Rev. I's removal of numeric retention values changes device physics.
12. October 2023 is the implementation or invention date of Micron refresh.
13. Micron's refresh mechanism is identical to Seagate SSD retention rewrite.
14. Micron's refresh mechanism is identical to OCP background refresh.
15. Micron's refresh mechanism is identical to Case-36 Correct-and-Refresh.
16. Host initiation implies whole-device coverage.
17. Automatic refresh implies a fixed cadence.
18. Refresh completion implies future offline retention for an arbitrary duration.
19. A successful generic BKOPS run implies Power Off Notification completion.
20. Power Off Notification completion implies refresh completion.
21. Refresh support implies every customer configuration enables or invokes it identically.
22. The product's JEDEC 5.1 compliance makes Micron vendor refresh a JEDEC-standard refresh command.
23. The same controller/NAND/firmware applies to every Micron e.MMC family.
24. A distributor-hosted copy is independent third-party engineering validation; it is used here as a surviving mirror of Micron-authored primary documentation.

---

## Why this matters for Case 111

This slice does not satisfy the highest-priority Case-111 target of a host-visible **retention-specific completion authority**. Instead, it makes that target more precise with a named commercial counterexample:

```text
named product has explicit refresh capability
    + named product has generic BKOPS status/control
    + public datasheet still does not bind
      BKOPS completion to refresh completion
```

Therefore the next source must do more than mention both BKOPS and refresh. It must explicitly connect a visible terminal state, status field, coverage indicator, or operation result to the refresh obligation itself.

---

## Reuse boundary

A fresh search of `tmzncty/computing-archaeology` for Micron e.MMC refresh found no dedicated packet to reuse in this pass.

Broader Micron embedded-flash product genealogy, controller generations, NAND generations, vendor-specific command history, e.MMC adoption, and JEDEC proposal/ballot history belong primarily in `computing-archaeology`.

This packet stays bounded to:

```text
named retention-relevant product
    -> separately named refresh and BKOPS capabilities
    -> public status/control asymmetry
    -> unresolved retention-specific completion authority
```
