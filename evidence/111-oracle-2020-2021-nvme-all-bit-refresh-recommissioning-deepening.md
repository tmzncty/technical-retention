# Evidence 111 — Oracle 6.4 TB NVMe all-bit refresh / recommissioning deepening

## Status

**`bounded deepening complete`** for one narrow question:

> Can Case 111 ground a named enterprise NVMe product in which a long-unpowered retention problem has an explicit device-local background-refresh timescale, a scoped completion statement, and an alternative destructive path that reaches the same named issue boundary without preserving the old payload?

The answer is **yes, for Oracle's 6.4 TB NVMe SSD v1 / related F640 documentation and Bug ID 27759886**.

Oracle's June 2020 product guide specifies three months of power-off data retention at rated write endurance and 40 °C. The November 2021 product notes describe Bug ID 27759886 as fixed in RF30 and state that, after prolonged unpowered storage, the firmware refresh policy works in the background while powered; applying that policy to all bits takes approximately fourteen days and varies by product. The same notes say that two weeks powered resolves the named issue, while secure erase provides an immediate all-bit-refresh path but destroys all device data.

This is unusually useful because one first-party product family exposes all of the following at once:

```text
product retention specification
    != elapsed unpowered history
    != powered maintenance opportunity
    != all-bit refresh-policy completion for one named issue
    != preservation of the old logical payload
```

The evidence does **not** establish a universal SSD refresh duration, Oracle invention priority, the exact NAND-page rewrite geometry of the background policy, or an independent Oracle controller lineage from Intel.

---

## Scope

### Object

The bounded object is Oracle's **6.4 TB NVMe SSD v1**, device name `7335940 / ICDPC2DD2ORA6.4T`, together with the closely related Oracle Flash Accelerator F640 PCIe Card v1 documentation where the same Bug ID appears.

Oracle's product guide identifies the SFF drive as using TLC 3D NAND, one Intel Flash Memory NVMe Controller, and Intel custom/proprietary PCIe-to-NAND controller firmware.

### Time boundary

Two first-party documentation snapshots are used:

1. Oracle 6.4 TB NVMe SSD User Guide, updated **June 2020**;
2. Oracle 6.4 TB NVMe SSD v1 Product Notes, updated **November 2021**.

Those update dates date the surviving documentation used here. They are **not** treated as firmware invention dates or as the first dates on which the hardware existed.

### Research question

This slice asks only:

> How does the documented long-offline risk move through product retention specification, ECC margin, powered background refresh, issue-scoped completion, and destructive reinitialization?

It does not attempt a general Intel enterprise-SSD firmware history.

---

## Source 1 — Oracle 6.4 TB NVMe SSD User Guide, June 2020

**Primary vendor documentation:**
<https://docs.oracle.com/cd/E87231_01/html/E87242/goica.html>

### H/P — product retention is stated as an endurance- and temperature-conditioned relation

Oracle's reliability table defines `Data Retention` as the period for retaining data in NAND at maximum rated endurance and gives:

```text
three months power-off retention
    once rated write endurance is reached
    at 40 °C
```

The same table separately gives endurance and UBER properties.

For this case the important historical boundary is:

```text
three-month product retention specification
    != deterministic failure instant for every individual drive
```

The source states a product reliability relation under named conditions; it does not say every device becomes unreadable exactly at the three-month boundary.

### H/P — Oracle identifies Intel controller / firmware lineage in the same product family

Oracle's Characteristics page identifies:

- device `7335940 / ICDPC2DD2ORA6.4T`;
- manufacturing name `SSDPE2ME064T4S`;
- one **Intel Flash Memory NVMe Controller**;
- **Intel custom and proprietary PCIe to NAND flash controller** firmware;
- NVMe SMART endurance-remaining monitoring.

Primary page:
<https://docs.oracle.com/cd/E87231_01/html/E87242/gohej.html>

This matters for source criticism. Oracle is a first-party system/product-documentation source for the operational contract, but the corporate masthead does not by itself prove an independent controller/firmware engineering lineage from Intel.

Therefore:

```text
separate vendor/system documentation
    != separate controller lineage
```

and:

```text
Oracle-branded operational evidence
    != proof that Oracle authored the underlying controller firmware
```

---

## Source 2 — Oracle v1 Product Notes, November 2021

**Primary vendor documentation:**
<https://docs.oracle.com/cd/E87231_01/html/F36828/gtlea.html>

### H/P — Bug 27759886 links prolonged power-off to media errors and host-visible failure modes

The product notes identify **Bug ID 27759886**, fixed in firmware release **RF30**.

For Oracle 6.4 TB NVMe SSD v1, the notes state that after not being powered for three or more months the device may report uncorrectable errors or assert. They additionally state that if NAND media is not refreshed for approximately three months, media errors may occur.

The wording is probabilistic and issue-scoped. It supports:

```text
long unpowered interval
    -> increased risk under this documented issue
```

not:

```text
three months elapsed
    -> every device has failed
```

### H/P — powered time is an explicit device-local maintenance interval

The same notes state that the drive firmware policy refreshes media **in the background while the drive remains powered-on**.

They then provide a much stronger boundary than a generic instruction to restore power:

- if the drive remains powered long enough for the background refresh policy to be applied to **all bits**, the drive is not at risk for **this issue**;
- the time required to refresh all bits is **approximately 14 days**;
- the time **varies by product**.

Thus the historical product record itself separates:

```text
power applied
    != background refresh policy applied to all bits
```

and it blocks universalization:

```text
~14 days for this documented product/issue family
    != universal SSD maintenance duration
```

### H/P — the same latent degradation can surface differently depending on when it is encountered

Oracle says that if affected bits exceed ECC capability, an uncorrectable read error can result.

It then distinguishes two host-visible manifestations:

- during normal operation: increased SMART media errors can be reported;
- during drive power-on: the host can receive `ASSERT` or `BAD_CONTEXT` errors.

The product notes give example firmware `QDV1RD28` codes including `ASSERT_100452A0`, `BAD_CONTEXT_1042`, and `BAD_CONTEXT_1043`.

Therefore the record directly supports:

```text
one underlying long-offline / media-margin problem
    != one invariant externally visible failure mode
```

The manifestation can depend on the operational phase in which the failing read is encountered.

### H/P — two weeks powered is a named issue-resolution path

Oracle's workaround allows the operator to **wait two weeks for media refresh while the drive is powered on before using it**.

The separate `Fixed Issues` page states that Bug 27759886 can be handled immediately by the secure-erase sequence, **otherwise after two weeks of device power-on the issue will be fully resolved**.

Primary page:
<https://docs.oracle.com/cd/E87231_01/html/F36828/gsjba.html>

The completion language must remain scoped:

```text
after two weeks powered -> Bug 27759886 fully resolved
```

is not equivalent to:

```text
after two weeks powered -> every possible future SSD health / retention risk certified absent
```

This is **issue-scoped completion semantics**, not a universal health certificate.

### H/P — secure erase is an alternative immediate all-bit-refresh path and destroys payload

Oracle also says that if **immediate refresh of all bits** is desired, the operator can secure erase the drive.

The same page gives an explicit caution that **all device data will be destroyed after an erase**.

Thus one product document directly establishes a retention-critical non-equivalence:

```text
renewing / refreshing the physical medium state
    != preserving the old logical payload
```

The background powered-time path is intended to preserve the device's existing usable data while the maintenance policy operates. The secure-erase path deliberately destroys the old payload while immediately bringing the medium through the documented all-bit-refresh path.

This is stronger than the generic observation that erase is destructive because both paths appear as alternatives for the same named long-offline issue.

### H/P — firmware/update output also exposes Intel device identity

The secure-erase procedure's example device inventory labels the affected NVMe controllers as `Intel`, with PCI vendor ID `0x8086` in later verification output.

This independently reinforces the source-lineage caution already visible in the User Guide. It does not prove that every Intel product using a related controller has the same Oracle firmware policy or issue.

---

## Closely related F640 witness

Oracle's Flash Accelerator F640 PCIe Card v1 Product Notes carry the same Bug ID **27759886** and the same background-refresh relation: prolonged unpowered storage can expose errors; powered background policy reaches all bits in approximately fourteen days, with duration varying by product; secure erase is the immediate alternative.

Primary page:
<https://docs.oracle.com/cd/E87231_01/html/E87232/gtbtj.html>

The F640 record is useful for product-family continuity, not for counting a second independent implementation. Oracle's user documentation identifies Intel controller ASICs for both product forms, and the product notes treat the firmware line as shared/related.

Therefore:

```text
same Bug ID across SFF and AIC Oracle products
    != two independent engineering witnesses
```

and:

```text
shared issue / firmware family
    != proof of identical internal refresh geometry or timing in every SKU
```

Oracle itself says the all-bit refresh duration varies by product.

---

## Engineering reconstruction

The following terms are project reconstruction unless attributed above.

### E — maintenance opportunity, coverage, and issue closure are three different states

The Oracle sequence gives an unusually clear state decomposition:

```text
powered on
    -> firmware has maintenance opportunity

background policy running over time
    -> maintenance coverage advances

policy applied to all bits
    -> documented issue-specific risk boundary is closed
```

Therefore:

```text
maintenance opportunity
    != maintenance coverage complete
    != issue-scoped completion
```

A power transition starts the interval in which maintenance can happen; it is not itself the completion event.

### E — completion can be semantically strong without being host-observable progress telemetry

Oracle states a duration and an issue-resolution condition, but the inspected pages do not expose a host-visible percentage-complete counter for the all-bit refresh sweep.

Thus:

```text
vendor-documented completion semantics
    != operator-visible progress telemetry
```

This differs from IBM ESS Case 111 evidence where the storage-system layer gives per-vdisk scrub-completion log messages.

### E — retention margin failure can cross interface layers

The source connects a physical/electrical retention problem to ECC and then to different software-visible outcomes:

```text
media state drifts beyond sufficient margin
    -> errors accumulate
    -> ECC capability may be exceeded
    -> uncorrectable read
    -> SMART-media-error increase OR power-on ASSERT/BAD_CONTEXT
```

The exact internal path is not fully specified, so this chain should not be promoted into a transistor- or page-level implementation reconstruction. But the source clearly shows that one retention problem can be observed through several interface states.

### E — medium renewal and object retention are orthogonal

Because secure erase is offered as an immediate all-bit-refresh route, while the powered wait is a non-destructive operational route, the same maintenance target can be reached under different payload contracts:

```text
background powered refresh
    -> renew medium margin while retaining payload contract

secure erase
    -> immediate all-bit refresh path
    -> old payload deliberately destroyed
```

Thus:

> **renewal of the substrate's service margin is not identical to retention of the same logical object.**

That is an engineering distinction; Oracle does not use this philosophical vocabulary.

### E — issue-scoped completion is not timeless future safety

`fully resolved` in the fixed-issues table names Bug 27759886. It does not erase future wear, future offline aging, later firmware defects, or unrelated failure modes.

Therefore:

```text
named issue closed now
    != future maintenance obligation abolished
```

---

## Functional comparison

### A — Dell Case 111: minimum powered duration without one universal number

Dell's current Case 111 evidence recommends a minimum three-week powered interval for its affected enterprise-SSD/NVMe context and says larger capacity can require longer.

Oracle supplies a named-device complement: approximately fourteen days for its all-bit background-refresh policy, explicitly varying by product.

The bounded comparison is:

```text
vendor-specified powered dwell can be part of retention infrastructure
```

while preserving:

```text
Dell three weeks
    != Oracle ~14 days
    != universal SSD constant
```

The products, firmware, evidence dates, and operator contexts differ.

### A — Hitachi/HGST FlashMAX: cadence without duration vs Oracle duration with issue closure

The existing FlashMAX deepening supplies an earlier periodic instruction to power the stored server once every three months, but the inspected Hitachi/HGST guide does not specify how long power must remain applied or provide a retention-specific completion witness.

Oracle closes precisely that narrower comparison gap for a different product family:

```text
periodic power-on cadence only
    != minimum powered dwell
    != issue-scoped completion semantics
```

No direct Hitachi -> Oracle or Oracle -> Dell genealogy is asserted.

### A — IBM ESS: system-level completion telemetry vs device-policy completion statement

IBM ESS exposes a per-vdisk `End scrubbing tracks ...` log witness for a system-level scrub. Oracle instead documents device-local background-refresh coverage and an approximate all-bit duration, but the inspected page does not expose per-device refresh-progress telemetry.

Therefore:

```text
system-level observable scrub completion
    != device-policy all-bit completion statement
```

Both help reject `power restored = maintenance complete`, but through different evidence layers.

### A — Case 37 Samsung 840 EVO

Case 37 already gives a commercial SSD example in which a powered periodic refresh addresses old-data read-performance degradation and does not operate while powered off.

Oracle's named issue is different: the documented long-offline condition may exceed ECC capability and surface as uncorrectable reads or power-on asserts.

The functional analogy is only:

```text
powered controller activity can be part of maintaining Flash serviceability
```

It is not evidence of one algorithm or one firmware genealogy.

### A — Case 36 Correct-and-Refresh

The Oracle pages do not identify the academic `Correct-and-Refresh` algorithm, its thresholds, or its rewrite policy. Similarity of purpose does not establish implementation identity.

---

## Philosophical / project interpretation

### I — maintenance completion is relation-scoped, not absolute

Oracle's `fully resolved` language is valuable because it sounds strong yet remains bounded by the named bug.

For this project it illustrates a general caution:

> a technical system can have a genuine completion state for one maintenance relation without becoming absolutely “healthy,” timeless, or maintenance-free.

That interpretation is the project's, not Oracle's terminology.

### I — the same medium can be “renewed” under opposite payload contracts

The paired background-refresh and secure-erase paths sharpen another project distinction. A medium can be brought into a refreshed physical condition either while retaining the logical payload or while intentionally destroying it.

So `physical renewal` cannot be used as a synonym for `retention of the same object`.

---

## Prior art / related-repository boundary

No invention-priority claim is made for Oracle, Intel, background Flash refresh, secure erase, or powered retention maintenance.

A fresh search of `tmzncty/computing-archaeology` for `Oracle 6.4 TB NVMe SSD`, `27759886`, and this firmware/product context returned no dedicated reusable history. The broader Intel/Oracle controller, platform, and firmware genealogy belongs there if developed later. This file retains only the retention-specific distinctions needed by Case 111.

The source-lineage rule is especially important here: Oracle documentation is independent of IBM/Dell/Hitachi as an operator-facing documentary corpus, but Oracle itself identifies the drive controller and firmware as Intel. It should not be double-counted as evidence of an independent controller architecture without further supply-chain / firmware evidence.

---

## Explicit stop conditions / unsupported upgrades

This record does **not** establish:

- Oracle or Intel invented background Flash refresh;
- RF30 was first released in November 2021;
- the June 2020 / November 2021 documentation dates are hardware shipment dates;
- every drive fails after three months unpowered;
- approximately fourteen days is a universal SSD refresh duration;
- every physical NAND page is literally rewritten once during the documented background policy;
- the source phrase `all bits` reveals exact NAND program/erase geometry;
- two weeks powered certifies the drive against every future retention or health problem;
- `fully resolved` means anything broader than Bug 27759886 in the cited fixed-issue table;
- secure erase preserves the prior logical payload — the source explicitly says it destroys device data;
- secure erase is interchangeable with independent sanitization verification or forensic proof beyond the vendor operation described;
- Oracle's corporate masthead proves independent controller-firmware lineage from Intel;
- the SFF drive and F640 card are independent implementation witnesses merely because they have different form factors;
- Oracle implemented Case 36 FCR or Samsung Case 37's exact algorithm;
- direct historical genealogy from FlashMAX, Samsung, IBM, or Dell to this Oracle firmware policy.

---

## Sources

### Oracle, June 2020 — product retention specification

Oracle, **Oracle 6.4 TB NVMe SSD User Guide**, `Reliability Specifications`, updated June 2020:
<https://docs.oracle.com/cd/E87231_01/html/E87242/goica.html>

Relevant statements: three months power-off retention at rated write endurance / 40 °C; UBER and endurance are separately specified.

### Oracle, June 2020 — device/controller identity

Oracle, **Oracle 6.4 TB NVMe SSD User Guide**, `Characteristics`, updated June 2020:
<https://docs.oracle.com/cd/E87231_01/html/E87242/gohej.html>

Relevant statements: device `7335940 / ICDPC2DD2ORA6.4T`; Intel Flash Memory NVMe Controller; Intel custom/proprietary PCIe-to-NAND controller firmware; SMART endurance monitoring.

### Oracle, November 2021 — long-offline issue and all-bit refresh

Oracle, **Oracle 6.4 TB NVMe SSD v1 Product Notes**, `Secure Erase Drives Before Use`, updated November 2021:
<https://docs.oracle.com/cd/E87231_01/html/F36828/gtlea.html>

Relevant statements: Bug 27759886 / RF30; uncorrectable errors or assert after long unpowered storage; background refresh while powered; approximately fourteen days for policy to cover all bits; product variation; normal-operation SMART errors versus power-on ASSERT/BAD_CONTEXT; two-week powered wait; destructive secure-erase immediate all-bit-refresh path.

### Oracle, November 2021 — issue-scoped completion wording

Oracle, **Oracle 6.4 TB NVMe SSD v1 Product Notes**, `Fixed Issues`, updated November 2021:
<https://docs.oracle.com/cd/E87231_01/html/F36828/gsjba.html>

Relevant statement: Bug 27759886 is fixed in QDV1RF30 and, absent the immediate secure-erase sequence, is `fully resolved` after two weeks of device power-on.

### Oracle, November 2021 — related F640 product-family witness

Oracle, **Oracle Flash Accelerator F640 PCIe Card v1 Product Notes**, `Secure Erase Cards Before Use`, updated November 2021:
<https://docs.oracle.com/cd/E87231_01/html/E87232/gtbtj.html>

Relevant statements: same Bug ID / RF30 family and approximately fourteen-day powered all-bit refresh relation; useful as product-family continuity rather than an independent implementation count.

---

## Bounded conclusion

Oracle's surviving first-party documentation supplies a named enterprise-NVMe witness in which **powered dwell has an explicit device-local maintenance meaning**. The three-month product retention specification is distinct from the roughly fourteen-day all-bit background-refresh interval; simply restoring power is distinct from completing that policy; and `fully resolved` is scoped to one named firmware issue rather than absolute future health.

Most importantly, the same document presents two paths around the named long-offline problem:

```text
wait ~2 weeks powered
    -> background refresh policy reaches all bits
    -> existing payload intended to remain usable

secure erase
    -> immediate all-bit-refresh path
    -> all old device data destroyed
```

That makes a particularly sharp retention boundary:

> **renewing the medium's service margin is not the same relation as retaining the same logical payload.**
