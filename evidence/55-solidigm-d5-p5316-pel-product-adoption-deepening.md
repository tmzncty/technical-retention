# Case 55 deepening evidence — D5-P5316 named-product PEL adoption and conformance-label boundary (2020–2024)

## Status

**`grounded`** for a bounded named-product adoption deepening of Case 55.

Case: [`../cases/55-nvme-smart-health-endurance-telemetry.md`](../cases/55-nvme-smart-health-endurance-telemetry.md).

Earlier standardized-interface deepening: [`55-nvme14-2019-persistent-event-log-deepening.md`](55-nvme14-2019-persistent-event-log-deepening.md).

This slice closes one explicit evidence debt left by the NVMe 1.4 Persistent Event Log pass: identify a named commercial SSD family whose first-party product documentation actually exposes PEL. It uses the Intel/Solidigm D5-P5316 family because the public record creates an unusually useful boundary: NVM Express introduced PEL as an optional feature in Revision 1.4, while Solidigm's D5-P5316 product brief simultaneously advertises **Persistent Event Log** and describes the drive as **NVMe 1.3c-compliant**.

The result is not a contradiction. It is evidence that **feature adoption, advertised interface-revision conformance, product-family chronology, and exact firmware behavior are different historical and engineering claims**.

This record does **not** prove that launch firmware exposed PEL, that every D5-P5316 firmware has identical PEL behavior, that the product is wholly NVMe 1.4-conformant, or that a manufacturer feature bullet independently validates reset/power-failure/sanitize semantics.

## Bounded question

The 2019 NVMe 1.4 evidence already establishes PEL's standardized interface semantics. What was still missing was a named-product bridge:

> Can a commercial SSD family be documented as implementing PEL even when its product brief advertises an older base NVMe revision, and what does that let us infer about retained-history capability?

The D5-P5316 record supports a narrow answer:

```text
NVMe 1.4 standardizes optional PEL in 2019
    ↓
Intel introduces the D5-P5316 product family in December 2020
    ↓
Solidigm later documents the same product family as
    NVMe 1.3c-compliant + Persistent Event Log capable
    ↓
feature-level adoption is visible
but
whole-revision conformance and first-support firmware remain separate questions
```

## Sources and provenance

### E1 — NVM Express Revision 1.4 and first-party change ledger, 2019

NVM Express, **NVM Express Base Specification Revision 1.4**, 10 June 2019, §5.14.1.13, and **Changes in NVMe Revision 1.4**:

- <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf>
- <https://nvmexpress.org/wp-content/uploads/Changes-in-NVMe-Revision-1.4.pdf>

The first-party change ledger labels **Persistent Event Log** an optional feature added in Revision 1.4 and points to Technical Proposals 4007a and 4042a. The earlier Case 55 deepening already audits PEL's reset/power-cycle persistence, finite/suppressible/deletion-governed history, reporting-context behavior, periodic SMART snapshots, and sanitize interaction.

This source establishes a standards revision boundary, not a product-adoption date or invention priority.

### E2 — Intel D5-P5316 product-family introduction, 16 December 2020

Intel, **Intel Announces Its Next Generation Memory and Storage Products**, 16 December 2020:

<https://www.intel.com/content/www/us/en/newsroom/news/next-generation-memory-storage-products.html>

Intel's first-party newsroom record identifies the D5-P5316 as its 144-layer QLC warm-storage SSD and states that Intel introduced the D5-P5316 in **December 2020**.

This establishes the named product-family introduction floor. The page does not document PEL and therefore is not used to claim that December-2020 launch firmware already exposed PEL.

### E3 — Solidigm D5-P5316 Product Brief, published 10 October 2023

Solidigm, **Solidigm D5-P5316 Product Brief**, published 10 October 2023, identifying the product as **Formerly Intel SSD D5-P5316**:

- <https://www.solidigm.com/products/data-center/product-briefs/d5-p5316-product-brief.html>
- downloadable product-brief PDF: <https://www.solidigm.com/content/dam/solidigm/en/site/products/data-center/product-briefs/d5-p5316-product-brief/documents/d5-p5316-product-brief.pdf>

Under `Firmware enhancements for drive performance, IT efficiency, data security, and manageability`, the brief lists both:

- `NVMe 1.3c and NVMe-MI 1.0a-compliant`; and
- `Persistent Event Log exposes deeper drive history for debugging at scale`.

The same page separately describes Telemetry as exposing stored data plus error tracking/logging. The coexistence of the `NVMe 1.3c` conformance label and PEL feature statement is the central product-level evidence in this slice.

The page's performance-test notes identify D5-P5316 testing on firmware `ACV10100` as of March 2021. Those notes are **not** a PEL validation record, so they are retained only as a bounded firmware/test chronology witness.

### E4 — Solidigm Product Change Notification 0000019376-00, 31 May 2024

Solidigm, **Intel SSD D5-P5316 (Intel-branded version), Product Discontinuance**, PCN `0000019376-00`, 31 May 2024:

<https://www.solidigm.com/content/dam/solidigm/en/site/products/documents/pcn/PCN0000019376-00.pdf>

The PCN says Solidigm would end-of-life Intel-branded D5-P5316 versions, continue selling the drives under the Solidigm brand with initial availability by end of Q3 2024, take final Intel-branded orders through 30 November 2024, and ship them through 28 February 2025.

This supports continuity of the named commercial product family across the Intel/Solidigm branding transition. It does not itself specify PEL semantics.

## Historical record

### 1. PEL is a Revision-1.4 optional-feature boundary in the NVMe standard record

NVM Express's 2019 first-party change ledger places Persistent Event Log in Revision 1.4 and calls it optional. The earlier Case 55 evidence already establishes the normative details of what that log can retain and how its history remains selective rather than complete.

Historical record:

```text
10 June 2019
    NVMe Revision 1.4
    -> optional Persistent Event Log standardized
```

That standards-history statement is independent of when any particular vendor product implemented the feature.

### 2. Intel introduced the D5-P5316 product family in December 2020

Intel's newsroom record directly dates the D5-P5316 family introduction to December 2020. It identifies the product as a 144-layer QLC design targeted at warm storage.

Historical record:

```text
December 2020
    -> D5-P5316 product family introduced
```

The source does not mention PEL, so this date is **not** silently converted into a PEL-adoption date.

### 3. Solidigm later documents D5-P5316 PEL support and an NVMe 1.3c conformance label in the same product brief

The 10 October 2023 Solidigm product brief calls the product `Formerly Intel SSD D5-P5316`. In the same firmware/manageability section it lists `NVMe 1.3c and NVMe-MI 1.0a-compliant` and advertises `Persistent Event Log` as exposing deeper drive history for debugging at scale.

This is direct named-product adoption evidence:

```text
named D5-P5316 product documentation
    -> PEL feature exposed
    +
    -> NVMe 1.3c conformance label exposed
```

It is **not** evidence that PEL belonged to the NVMe 1.3c standard. The standards record still places the optional feature in Revision 1.4.

### 4. The public product record crosses an Intel→Solidigm branding transition

The 2023 product brief explicitly says `Formerly Intel SSD D5-P5316`. The May-2024 PCN then documents the end-of-life of Intel-branded variants while continuing the D5-P5316 under the Solidigm brand.

This gives a commercial-lineage witness strong enough for this bounded purpose: the later Solidigm PEL statement applies to a product line explicitly tied to the former Intel D5-P5316 identity.

It does not prove byte-for-byte firmware identity across branding, form factor, capacity, or every shipment.

### 5. March-2021 ACV10100 is a test-config chronology witness, not a PEL-compliance result

The 2023 Solidigm web page says its cited D5-P5316 performance testing was done as of March 2021 on firmware `ACV10100`. That is useful only as a named firmware/version date inside the product record.

The page does not say that the March-2021 tests exercised PEL, so the repository does not infer:

```text
ACV10100 tested in March 2021
    -> therefore PEL was present and conformant in ACV10100
```

That upgrade remains unsupported.

## Engineering reconstruction

### 1. Feature support is not the same claim as whole-revision conformance

The product-level counterexample is unusually clean:

```text
standard history:
    PEL -> optional feature added in NVMe 1.4

product brief:
    D5-P5316 -> NVMe 1.3c-compliant
    D5-P5316 -> Persistent Event Log
```

The defensible reconstruction is:

> **feature support != whole-revision conformance claim**.

A vendor may implement an optional capability standardized in a later revision without advertising the entire device as conformant to that later revision. Conversely, one feature statement cannot be promoted into a claim of complete Revision-1.4 conformance.

### 2. Advertised interface revision is not an exclusive ceiling on implemented optional capabilities

The phrase `NVMe 1.3c-compliant` tells us something about the product's advertised conformance baseline. It does not, in this record, function as a complete enumeration of every implemented optional command/log feature.

Therefore:

> **advertised interface revision != exclusive feature ceiling**.

This is an engineering reading of the coexistence of two first-party statements. It is not a rewrite of standards genealogy.

### 3. Product-family introduction date is not the feature-introduction date

Intel's December-2020 product-introduction date and Solidigm's later PEL documentation bound two different facts. Unless an earlier product specification, release note, firmware matrix, Identify/Log capture, or independent test is recovered, the repository must preserve:

> **product-family introduction != first PEL-support firmware/date**.

The current evidence establishes a product-family floor and a later public feature-attestation floor, not the transition point between them.

### 4. `PEL supported` does not prove every standardized event type or every normative edge condition

A feature bullet establishes product exposure, not a full event-support matrix. It does not independently demonstrate which optional/vendor-specific event types are recorded, how much history the device retains, what happens at capacity, whether every abrupt-power event is captured, or how every sanitize/reset boundary behaves in each firmware release.

Therefore:

> **PEL feature statement != complete PEL conformance matrix**.

The earlier NVMe 1.4 evidence remains the normative interface contract; named-product validation requires separate product evidence.

### 5. `deeper drive history` is still selected technical history, not an archive of everything the NAND/controller did

Solidigm's phrase is useful manufacturer vocabulary for the operational purpose of PEL, but it does not override the base-specification limits already grounded in Case 55: finite event capacity, repeated-event suppression, vendor-specific deletion under pressure, reporting-context selection, and possible sanitize-driven modification.

Thus:

> **deeper drive history != complete immutable device history**.

Nor does the PEL expose every FTL relocation, ECC correction, NAND threshold shift, garbage-collection copy, or physical program/erase episode.

### 6. First-party product documentation is adoption evidence, not independent compliance validation

The Intel/Solidigm record is strong historical evidence that the feature was publicly attached to a named commercial family. It is not an independent power-cut/sanitize/reset test.

Therefore:

> **manufacturer feature documentation != independent behavioral validation**.

Independent testing remains necessary before claiming exact persistence or fault-boundary compliance for a particular firmware/device sample.

## Functional comparisons

### PM9A3 vendor telemetry layout

The earlier PM9A3 deepening shows that one named SSD can expose standard NVMe SMART/Health plus several vendor/OCP-style telemetry namespaces with different accounting and persistence contracts. D5-P5316 adds a different warning: a product's **revision label** also cannot be treated as a complete feature inventory.

Functional comparison only:

> product-level telemetry/diagnostic capability may exceed what a coarse namespace or revision label suggests, but this does not establish shared Samsung/Intel/Solidigm implementation, firmware lineage, or standards genealogy.

### ATA SMART and earlier diagnostic history

ATA/ATAPI-5's 1999 circular self-test log remains earlier prior art for retained drive diagnostic history. D5-P5316 PEL product adoption does not create a direct ATA→NVMe product genealogy and does not alter the earlier priority boundary.

## Philosophical interpretation — bounded

The exact technical fact is modest: one standards revision label does not exhaust the operational capabilities through which a device can retain evidence of its own past.

The bounded interpretation is:

> **classification persistence and capability persistence are not the same relation**. A product can remain publicly classified under one conformance baseline while exposing a retained-history mechanism standardized in another revision.

This is a project-level interpretation. It is not terminology attributed to Intel, Solidigm, or NVM Express, and it does not make revision labels philosophically equivalent to memory.

## Rejected upgrades / stop conditions

- **`D5-P5316 says NVMe 1.3c, therefore PEL was part of NVMe 1.3c` — rejected.** NVM Express's own revision ledger places PEL in Revision 1.4.
- **`Intel introduced D5-P5316 in December 2020, therefore launch firmware supported PEL` — not established.** The 2020 Intel source does not mention PEL.
- **`ACV10100 appears in March-2021 test notes, therefore ACV10100 PEL behavior was validated` — rejected.** The cited tests are not identified as PEL tests.
- **`PEL bullet = full NVMe 1.4 compliance` — rejected.** Optional-feature adoption and whole-revision conformance are different claims.
- **`PEL bullet = all PEL event types and edge cases implemented identically in every firmware` — rejected.** A product feature summary is not a per-firmware conformance matrix.
- **`deeper drive history = complete immutable history` — rejected.** The standardized PEL history is already known to be selective and governable.
- **`manufacturer documentation = independent fault validation` — rejected.** Abrupt power, capacity pressure, reset, and sanitize behavior still need independent testing.
- **`Intel→Solidigm product continuity = byte-identical firmware across every variant` — rejected.** The PCN establishes commercial-lineage continuity, not implementation identity.
- **`PEL support = hidden NAND/FTL algorithm disclosure, sanitization proof, or invention priority` — rejected.** None follows from these sources.

## Claim ledger

| Claim | Label | Status |
| --- | --- | --- |
| NVM Express's 2019 change ledger identifies PEL as a new optional Revision-1.4 feature | `H/P` | strong first-party standards-history boundary |
| Intel states that it introduced the D5-P5316 family in December 2020 | `H/P` | strong first-party product chronology |
| Solidigm's 2023 D5-P5316 brief identifies the line as formerly Intel D5-P5316 and publicly advertises PEL | `H/P` | strong first-party named-product adoption evidence |
| The same Solidigm brief advertises NVMe 1.3c compliance | `H/P` | strong first-party product-interface label |
| The Solidigm page's March-2021 ACV10100 test note proves PEL existed/was validated in that firmware | `X` | rejected; test note is not a PEL result |
| The 2024 Solidigm PCN documents the Intel-branded→Solidigm-branded D5-P5316 commercial transition | `H/P` | strong first-party product-line continuity witness |
| `feature support != whole-revision conformance claim` | `E` | bounded reconstruction from standards/product records |
| `advertised interface revision != exclusive feature ceiling` | `E` | bounded reconstruction, not standards genealogy |
| `product-family introduction != first feature-support date` | `E` | chronology guardrail |
| PEL product support proves complete immutable history, all event types, fault compliance, or hidden FTL behavior | `X` | rejected |

## Open evidence debt

- recover the earliest D5-P5316 product specification/release note/firmware matrix that explicitly names PEL;
- determine the first firmware release that exposed PEL rather than inferring it from the December-2020 product-family launch;
- obtain a product/firmware-specific PEL event-support matrix if one is public;
- independently test reset, abrupt power loss, log-capacity pressure, reporting-context, and sanitize behavior on a named D5-P5316 firmware/device before compliance claims;
- inspect TP4007a/4042a directly before proposal-level chronology claims;
- route broader product-adoption genealogy and NVMe revision/implementation history to `tmzncty/computing-archaeology` rather than duplicating it here.

## Related repositories

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated D5-P5316/Persistent Event Log treatment. If a broader chronology of NVMe optional-feature adoption, firmware-version practice, or Intel/Solidigm SSD lineage is developed, it should primarily live there. This evidence record keeps only the retention-specific product-adoption and conformance-label boundary.
