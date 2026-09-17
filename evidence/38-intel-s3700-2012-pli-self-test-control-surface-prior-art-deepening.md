# Case 38 Deepening — Intel S3700 2012 PLI Self-Test Control Surface and Documentary Chronology

## Purpose

This record deepens [`../cases/38-intel-dc-s3700-pli-self-test-validation.md`](../cases/38-intel-dc-s3700-pli-self-test-validation.md) around one bounded chronology / prior-art question:

> how early can the repository directly ground a named Intel data-center SSD product surface in which power-loss-protection readiness is itself testable, reportable, and schedulable?

The existing Case 38 is grounded mainly from Intel's 2014-era _Power Loss Imminent (PLI) Technology_ brief and the January-2015 S3700 product specification. Those sources explain the later PLI mechanism and validation vocabulary well, but they are not the earliest Intel documentation now directly inspected for the named S3700 product.

The newly inspected source is Intel's **October 2012** _Intel Solid-State Drive DC S3700 Product Specification_, order **328171-001US**. Its own revision-history table additionally records **June 2012 — revision 001 — Initial release**. A separate Intel news fact sheet dated **12 November 2012** describes the S3700 as newly unveiled and publicly advertises a `Power safe write cache with built in self-test`.

This slice therefore establishes a conservative earlier documentary boundary while keeping three dates distinct:

```text
June 2012
    Intel specification's internal revision-history record:
    revision 001 / "Initial release"

October 2012
    date printed throughout the surviving Intel-hosted 328171-001US PDF

12 November 2012
    directly dated Intel public news fact sheet:
    newly unveiled S3700 + "Power safe write cache with built in self-test"
```

The June entry is an **internal revision-history statement inside the October-dated document**, not independently reconstructed proof of the exact day the PDF became publicly downloadable. The November fact sheet independently establishes public product vocabulary by a concrete date. No invention-priority claim follows.

**Evidence status:** `bounded deepening complete`.

---

## Related-repository check

Before writing, `tmzncty/computing-archaeology` was searched for `S3700` and did not expose a dedicated indexed S3700 / PLI module in the current search surface. The broader history of SSD controller design, enterprise SSD product development, capacitor-backed caches, and ATA/SATA evolution remains better suited to that companion repository if developed later.

This record keeps only the retention-specific chronology and control-state boundary:

```text
emergency-retention mechanism
    !=
readiness evidence about that mechanism
    !=
control over when readiness is tested
```

---

## Sources directly inspected

### A. Intel SSD DC S3700 Product Specification — 328171-001US

**Type:** Historical record / manufacturer-primary product documentation (`H/P`).

**Document:** Intel Corporation, _Intel Solid-State Drive DC S3700 Product Specification_, order 328171-001US.

**Surviving Intel-hosted PDF date:** October 2012.

**Internal revision-history statement:** printed p. 28 records `June 2012 | 001 | Initial release`.

Direct Intel-hosted PDF:

<https://download.intel.com/newsroom/kits/ssd/pdfs/Intel_SSD_DC_S3700_Product_Specification.pdf>

Directly inspected locations:

- printed p. 5: feature list includes `Enhanced power-loss data protection` and `Power loss protection capacitor self-test`;
- printed p. 11, §2.9: `Power Loss Capacitor Test` and monitoring through SMART attribute `(175, AFh)`;
- printed p. 19, SMART table: separate `AEh Unexpected Power Loss` and `AFh Power Loss Protection Failure` records;
- printed p. 24, §5.6 SMART Command Transport: vendor feature `D000h (Power Safe Write Cache capacitor test interval)`;
- printed p. 28, §9 revision history: `June 2012 001 Initial release`.

### B. Intel News Fact Sheet — 12 November 2012

**Type:** Historical record / manufacturer-primary dated public product announcement (`H/P`).

**Title:** _Intel Solid-State Drive DC S3700 Series Engineered to Eliminate Bottlenecks for Breakthrough High Performance Computing_.

**Date:** 12 November 2012.

Direct Intel-hosted PDF:

<https://download.intel.com/newsroom/kits/xeon/phi/pdfs/FactSheet_Intel_SSDs_for_HPC_SC12.pdf>

The first page describes Intel's `newly unveiled Intel SSD DC S3700 Series` and lists under `Strong Data Protection`:

- `Full data path and non-data path protection`;
- `Power safe write cache with built in self-test`.

The fact sheet does not expose the AFh field layout or D000h scheduling control. Its role here is narrower: it provides a concretely dated public-facing Intel witness that the S3700's protected write-cache self-test was part of named-product vocabulary by 12 November 2012.

### C. Intel _Power Loss Imminent (PLI) Technology_ brief — later explanatory comparison

**Type:** Historical record / later manufacturer-primary explanatory document (`H/P`), used only to compare what later documentation adds.

**Document:** Intel 330275-001US, ©2014; references include sample pricing as of 28 February 2014.

Direct Intel-hosted PDF:

<https://www.intel.com/content/dam/www/public/us/en/documents/technology-briefs/ssd-power-loss-imminent-technology-brief.pdf>

This later brief explains details that are **not** silently back-projected into the 2012 product specification, including:

- partial discharge of the backup PLI capacitors during self-test;
- the stated 25 µs minimum for S3700/S3500;
- the interpretation of AFh output fields as three health-check values;
- administrator use of SCT to invoke a new test or alter test intervals;
- the wider hot-unplug / repeated validation flow.

The 2012 specification establishes the named-product test/control surface. The 2014-era brief supplies a later explanatory mechanism and validation narrative.

---

## Historical record

### H/P — by the October-2012 specification, PLI self-test is already a named product feature

The S3700 overview does not merely say that the device has power-loss protection. It lists two distinct product features:

```text
Enhanced power-loss data protection
Power loss protection capacitor self-test
```

This separation matters. The document presents the protection path and the act of testing that path as distinct capabilities.

A safe historical statement is therefore:

> **The Intel-hosted October-2012 S3700 product specification already documents a named power-loss-protection capacitor self-test.**

The stronger statement `Intel invented PLI self-test in 2012` is not licensed by this source and is not made.

### H/P — §2.9 exposes the capacitor test as monitorable through AFh

Section 2.9 says the S3700 supports testing of the power-loss capacitor and that the test can be monitored through SMART attribute **175 / AFh**.

This means the product documentation already distinguishes:

```text
physical protection component/path
    !=
management-visible evidence about a test of that component/path
```

The specification does not require the reader to infer self-test health from a generic drive-health bit. It names a specific management attribute for the power-loss capacitor test.

### H/P — the 2012 SMART table separates event history from readiness-test history

The SMART table contains two adjacent but non-equivalent records:

- **AEh — Unexpected Power Loss**: cumulative unclean shutdowns over device life; an unclean shutdown is defined by removal of power without `STANDBY IMMEDIATE` as the last command, `regardless of PLI activity using capacitor power`;
- **AFh — Power Loss Protection Failure**: last test result in microseconds to discharge the capacitor, plus minutes since the last test and lifetime number of tests.

This is already enough in 2012 to reject:

```text
unclean-power event count
    =
power-loss-protection failure count
```

and:

```text
one latest readiness result
    =
complete history of external power-loss events
```

The event and readiness records answer different operational questions.

### H/P — AFh already retains result, recency, and cumulative test count in the 2012 specification

The 2012 AFh row reports three separable temporal dimensions:

1. a **latest test result** expressed as capacitor-discharge microseconds;
2. **minutes since last test**;
3. **lifetime number of tests**.

So the later 2014 explanatory brief did not introduce the basic idea that readiness evidence has a result, an age, and a cumulative test-history summary. That state decomposition is already visible in the 2012 named-product specification.

The 2012 row, however, is terse. It does not by itself explain that the test uses a partial discharge or supply the later brief's explicit 25 µs explanatory threshold. Those details remain sourced to the later document unless separately grounded elsewhere.

### H/P — SCT exposes a capacitor-test interval control surface in the 2012 specification

Section 5.6 lists vendor feature **D000h**, described as:

`Power Safe Write Cache capacitor test interval`.

This matters because it adds **test cadence / policy control** to the relation. The device does not only expose a passive observation of a self-test; the documented management interface includes a setting for the test interval.

The safe claim is:

```text
2012 named-product documentation exposes a test-interval control
```

The source does **not** state in the inspected passage whether D000h survives power cycle, firmware update, reset, or replacement. Therefore:

```text
host-visible test-interval control
    !=
demonstrated persistent policy across every restart boundary
```

No stronger persistence claim is made.

### H/P — November 2012 public product vocabulary independently names the built-in self-test

Intel's 12 November 2012 fact sheet calls the S3700 `newly unveiled` and publicly lists `Power safe write cache with built in self-test` under `Strong Data Protection`.

That source is important for chronology because it has a precise external date and a public product-news role. It independently shows that the self-test was not merely an internal field name found in a later-maintained specification copy.

The fact sheet still does not establish every AFh/D000h detail. Those remain anchored in the product specification.

### H/P — the current surviving 2012 PDF contains two different document dates that must not be collapsed

The PDF repeatedly prints `October 2012 Product Specification`, while §9 says:

```text
June 2012 | 001 | Initial release
```

A defensible repository chronology must preserve both facts.

The revision-history row is evidence that **Intel's document records revision 001 as an initial release in June 2012**. It is not, by itself, independent archival proof that the exact presently hosted PDF bytes were publicly downloadable in June.

Accordingly this record uses:

- **June 2012** as an Intel-internal revision-history date;
- **October 2012** as the printed date of the directly inspected surviving specification;
- **12 November 2012** as an independently dated Intel public fact-sheet witness.

This avoids the common prior-art error `revision history date = independently proven public-disclosure date`.

---

## Engineering reconstruction

### E — readiness evidence has its own temporal state

The AFh fields imply that a readiness statement is not timeless. A latest result can age, which is why the drive also retains time since that result.

```text
last measured capability
    +
age of that measurement
    !=
current capability known without qualification
```

The repository can therefore treat test recency as a constitutive part of readiness evidence without claiming that Intel used the term `epistemic state` or any philosophical equivalent.

### E — maintenance cadence is different from maintenance result

The D000h interval and AFh result are different control relations:

```text
when should the next readiness test occur?
    !=
what did the last readiness test observe?
```

A device can expose both a maintenance policy surface and maintenance-evidence state.

### E — mechanism lifetime rating is different from runtime readiness evidence

Case 15's earlier SSD 320 material describes capacitors selected/rated to support the product's power-loss behavior over device life. The S3700's 2012 control surface adds a different relation: observe/test the current state of the protection apparatus while the product is in service.

Thus:

```text
design-time / lifetime component qualification
    !=
run-time per-device readiness evidence
```

This is a same-vendor functional comparison, not proof that the SSD 320 and S3700 share the same circuitry or firmware.

### E — medium retention and emergency-transfer readiness are different retention horizons

The same 2012 S3700 specification separately states a NAND `Data Retention` requirement of **3 months power-off retention after the SSD reaches rated write endurance at 40 °C**, and separately documents the power-loss capacitor test.

These are not two measurements of one property:

```text
NAND payload-retention horizon after power is absent
    !=
short-term energy reserve needed to finish an emergency handoff as power disappears
```

A product can therefore have a specified nonvolatile-media retention horizon and, independently, a health/test regime for the infrastructure that moves in-flight state into that medium.

### E — a failing readiness test is not itself evidence that payload has already been lost

AFh concerns the protection apparatus. Its failure can indicate reduced confidence in surviving a future power-loss event without proving that existing NAND-resident payload is already corrupt.

Conversely, a passing self-test is not a proof of every future power-loss outcome, because the wider path also includes voltage detection, switching, firmware, NAND programming, mapping/currentness, host ordering, and the actual power waveform.

---

## Functional analogy

### A — comparison with proactive integrity scanning

At a very narrow functional level, the S3700 self-test resembles proactive integrity-maintenance cases such as HDFS block scanning or ZFS scrub in one respect only:

> work is performed before an observed demand failure so that latent loss of capability can be discovered earlier.

The analogy stops there.

- a scrub verifies stored payload / redundancy relations;
- the S3700 capacitor self-test checks the readiness of **infrastructure that may later preserve in-flight payload during a power event**.

No common mechanism or genealogy is implied.

### A — comparison with Case 15 SSD 320

Case 15 demonstrates finite stored energy as retention infrastructure. This 2012 S3700 slice adds a management relation in which the infrastructure itself has test evidence and a test cadence.

The comparison is useful precisely because:

```text
retention infrastructure exists
    !=
retention infrastructure is recently qualified
```

---

## Philosophical interpretation — bounded

The technical fact is modest but conceptually sharp:

> the apparatus intended to preserve future state can itself become an object of retained evidence — latest result, elapsed time since test, cumulative test count, and test cadence.

This means that technical persistence can include a second-order temporal relation: past maintenance evidence conditions present confidence in a mechanism whose decisive work may only occur during a future failure.

The limit is strict. This does not make AFh a cultural memory, a complete history, or a philosophical subject. It is a controller-management record whose significance comes from a specific engineering dependency.

---

## Prior-art / anti-anachronism boundaries

This deepening does **not** claim:

- that Intel invented capacitor-backed write caches;
- that Intel invented SMART, self-test, health monitoring, or fault injection;
- that June 2012 is independently proven as the exact public-web publication date of the surviving PDF;
- that the October 2012 PDF's revision-history row proves shipment on the same date;
- that the November 2012 fact sheet exposes AFh or D000h field semantics;
- that the 2012 AFh row, by itself, proves the later 2014 description of a **partial** capacitor discharge;
- that the 25 µs explanatory minimum in the later brief should be silently attributed to the 2012 specification;
- that D000h is proven to persist across power cycles or firmware updates;
- that a self-test pass proves whole-drive correctness under every power waveform;
- that a self-test failure proves already-retained NAND payload has been lost;
- that SSD 320 and S3700 use identical capacitor chemistry, circuitry, firmware, or test methods;
- that the S3700 product specification is an independent compliance test;
- that Intel's product chronology establishes a general industry genealogy.

---

## Resulting bounded distinctions

```text
protection mechanism
    !=
protection readiness test
    !=
readiness-result telemetry
    !=
readiness-test cadence control

AEh unclean-shutdown history
    !=
AFh PLI readiness/test state

latest test result
    !=
time since test
    !=
lifetime number of tests

NAND data-retention specification
    !=
PLI capacitor readiness

June-2012 internal revision-history entry
    !=
October-2012 printed surviving document date
    !=
12-November-2012 dated public fact-sheet witness

2012 terse product control surface
    !=
2014-era explanatory mechanism / validation narrative
```

---

## What this changes in Case 38

Before this deepening, the canonical case's main manufacturer chronology began with the 2014-era PLI brief and January-2015 S3700 product specification.

After direct inspection, the narrower chronology should read:

```text
2012 S3700 product documentation
    -> named capacitor self-test
    -> AFh result / recency / lifetime-test state
    -> AEh separately counts unclean shutdowns
    -> D000h exposes capacitor-test interval control

12 Nov 2012 public fact sheet
    -> "Power safe write cache with built in self-test"

2014-era PLI technology brief
    -> explains partial-discharge self-test semantics
    -> names 25 µs minimum for S3700/S3500
    -> explains administrator invocation / action
    -> documents wider PLI validation flow

Jan 2015 product specification
    -> later product-spec continuity
    -> adds/retains the mature product contract used by the canonical case
```

This is a **chronology and source-role correction**, not a new mechanism claim and not a reason to change Case 38's maturity from `grounded`.

---

## Remaining work

Still open after this bounded slice:

- locate a separately archived June-2012 copy, release notice, or web capture if an exact public-disclosure date earlier than November 2012 becomes important;
- compare the June/October 2012 revision against later S3700 specification revisions if field semantics changed;
- identify earlier industry/controller precedents for capacitor-health self-test without assuming Intel priority;
- controlled component-only S3700/S3500 power-waveform replication;
- lifetime/temperature aging coverage for the capacitor-test relation;
- deeper controller-metadata recovery evidence under interrupted power-loss handling.

Broader enterprise-SSD and capacitor-backed-cache genealogy belongs primarily in `computing-archaeology`.

---

## Source ledger

| Claim | Type | Source strength |
| --- | --- | --- |
| October-2012 S3700 spec lists enhanced PLP and capacitor self-test separately | H/P | strong manufacturer-primary product documentation |
| §2.9 says power-loss capacitor testing is monitored through SMART AFh | H/P | strong manufacturer-primary |
| 2012 AFh stores last discharge-test result, minutes since last test, lifetime test count | H/P | strong manufacturer-primary SMART table |
| 2012 AEh counts unclean shutdowns regardless of PLI capacitor activity | H/P | strong manufacturer-primary SMART table |
| 2012 SCT section exposes D000h capacitor-test interval | H/P | strong manufacturer-primary interface documentation |
| revision history says June 2012 revision 001 initial release | H/P | strong for Intel's own revision-history statement; not independent proof of exact public-web date |
| 12 Nov 2012 Intel fact sheet publicly advertises a power-safe write cache with built-in self-test | H/P | strong dated manufacturer-primary public product witness |
| 2014-era brief explains partial discharge and 25 µs minimum | H/P | strong later manufacturer-primary explanatory document |
| readiness result, recency, and cadence are distinct control relations | E | strongly supported reconstruction from separate fields/control surface |
| 2012 establishes Intel invention priority for PLP self-test | X | explicitly rejected |
| D000h proves restart-persistent test policy | X | explicitly rejected |
| passing AFh proves every future power-loss transfer succeeds | X | explicitly rejected |

---

## Status

**`bounded deepening complete`**.

The earlier named-product chronology is now directly grounded without changing Case 38's overall `grounded` maturity. The main remaining chronology question is no longer whether an S3700 self-test/control surface existed before the 2014-era brief; it is whether an independently archived public copy can pin the product specification's public-disclosure date closer to the internal `June 2012` revision-history entry.