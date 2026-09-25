# Case 111 — Memblaze PBlaze7 NVMe 2.1 / HIR adoption guardrail

**Status:** Case 111 remains `grounded`.

## Scope

This slice tests a narrow product-evidence question: does a named SSD page that says `NVMe 2.1` and advertises Device Self-test support establish Host-Initiated Refresh (HIR) adoption?

For the inspected Memblaze record, **no**. The sources support a product-level anti-collapse rule, not a claim that HIR is absent.

## Historical / source record

### Dated launch record

Memblaze's first-party PBlaze7 7A40 launch announcement is dated **3 September 2024**. It identifies the 7A40 as an enterprise PCIe 5.0 NVMe SSD, says units were being shipped to customers for testing and opened for pre-orders, and advertises:

```text
NVMe 2.0
NVMe-MI 1.2b
```

The launch record does not name HIR, `RHIRI`, `HIRT`, HIR progress, or HIR terminal results.

NVM Express 2.1 had been ratified on 5 August 2024, so the dated product launch and the later/current product page must be kept distinct.

### Current product pages

The current first-party PBlaze7 7A40 page, retrieved **25 September 2026**, advertises:

```text
Protocol: NVMe 2.1
Advanced Feature Support: Advanced Device Self-Test
Power off Retention: 3 months @ 40°C
```

The current PBlaze7 7A40 Ocean page exposes the same public-facing combination: NVMe 2.1, Advanced Device Self-Test, and three-month / 40°C power-off retention.

Neither inspected current feature list names Host-Initiated Refresh, `RHIRI`, `HIRT`, HIR percentage-complete reporting, or a HIR terminal result.

That omission is **not** proof that the firmware lacks HIR. Product marketing tables are not guaranteed to enumerate every optional capability.

It does establish that the public pages do not supply the source-level binding needed to infer HIR from the protocol and Device Self-test labels alone.

## Source chronology

The first-party records expose a bounded chronology:

```text
2024-09-03 launch record
    -> NVMe 2.0

current page retrieved 2026-09-25
    -> NVMe 2.1
```

The inspected sources do not establish when or why that public conformance label changed. Possible explanations include later firmware qualification, a family revision, later variants, or web-documentation consolidation.

Therefore:

```text
current product-page conformance label
    != launch-day conformance label

documentation change
    != proved firmware-change date
    != proved hardware-revision date
    != proved HIR-adoption date
```

## Engineering reconstruction

The existing Case-111 NVMe evidence establishes HIR as an optional NVMe-2.1 capability with its own support indication and refresh-specific fields.

The Memblaze pages therefore support:

```text
NVMe 2.1 conformance
    != every optional NVMe-2.1 feature implemented

Advanced Device Self-Test
    != every Device Self-test subtype implemented

power-off retention rating
    != HIR adoption

named NVMe 2.1 SSD
    + Device Self-test support
    + retention rating
    != named-product HIR closure
```

These are project-level engineering distinctions, not Memblaze terminology.

The three-month / 40°C retention specification must also remain separate from mechanism attribution:

```text
retention rating
    != evidence that HIR produces that rating

HIR support, if later demonstrated
    != arbitrary future offline-retention guarantee
```

## What this changes in Case 111

The prior HIR slices closed the standards-level progress and terminal-result semantics but left named-product adoption open.

This slice **does not close** that product target. It sharpens the evidence bar.

A future named-product closure should require at least one of:

1. a first-party product manual explicitly naming **Host-Initiated Refresh**;
2. an Identify Controller capture showing HIR support plus `RHIRI` / `HIRT`;
3. a vendor or conformance report naming the exact device and exercising `STC=3h`;
4. a real-device trace through HIR progress and terminal result.

## Functional comparison

Micron and Alliance eMMC product documents explicitly name refresh while separately exposing generic BKOPS. The Memblaze pages, by contrast, expose Device Self-test but do not publicly name HIR in the inspected feature lists.

This is a source-observability comparison only. It does not imply common firmware, controller design, NAND behavior, or genealogy.

The earlier Seagate Pulsar-family manuals are likewise stronger only for the narrow claim that they explicitly describe powered retention monitoring / refresh. They are not asserted as historical ancestors of NVMe HIR.

## Philosophical interpretation

A narrow project interpretation follows:

> A standard defines a space of possible relations; a product source determines which of those relations may actually be attributed to that product.

Possibility, implementation, public observability, and operational authority are distinct layers.

## Anti-collapse rules

```text
NVMe 2.1 compliance
    != HIR support proved

Advanced Device Self-Test
    != HIR support proved

power-off retention rating
    != HIR support proved

current product-page label
    != launch-day protocol label

absence of HIR from a marketing table
    != proof that firmware lacks HIR

same product-family name across years
    != unchanged firmware / hardware / conformance surface
```

## Related-repository boundary

Fresh searches of `tmzncty/computing-archaeology` for `Host-Initiated Refresh`, `PBlaze7 7A40`, `NVMe 2.1 refresh`, and `RHIRI` found no dedicated packet to reuse.

Broad Memblaze product genealogy, controller history, firmware-revision archaeology, and NVMe conformance history belong primarily there. Case 111 keeps the retention-specific boundary between standards capability, product claims, refresh adoption, observability, and offline-retention qualification.

## Remaining debt

1. Find a first-party named SSD/NVMe implementation explicitly advertising HIR.
2. Prefer an Identify Controller dump or conformance artifact exposing HIR support plus `RHIRI` / `HIRT`.
3. Capture a real HIR run through success and at least one reset/abort path.
4. Determine when the PBlaze7 7A40 public conformance statement moved from the launch record's NVMe 2.0 to the current page's NVMe 2.1.
5. Do not bind the published three-month / 40°C retention rating to HIR without explicit Memblaze evidence.

## Primary sources

- Memblaze, **“Memblaze Releases PBlaze7 7A40 Series PCIe 5.0 Enterprise SSDs with 4K Random Write at Millions of IOPS,”** 3 September 2024: https://www.memblaze.com/en/about-company/news/758.html
- Memblaze, **PBlaze7 7A40 Series NVMe SSD**, retrieved 25 September 2026: https://memblaze.com/en/product/pblaze7/816.html
- Memblaze, **PBlaze7 7A40 Ocean Series NVMe SSD**, retrieved 25 September 2026: https://memblaze.com/en/product/pblaze7/818.html

## Internal context

- [NVMe 2.1 HIR progress / completion boundary](111-nvme21-2024-host-initiated-refresh-progress-completion-deepening.md)
- [NVMe 2.1/2.2 HIR terminal-outcome / reset boundary](111-nvme21-22-hir-terminal-outcome-reset-boundary-deepening.md)
- [Case 111 evidence index](111-enterprise-ssd-extended-shutdown-evidence-index.md)
