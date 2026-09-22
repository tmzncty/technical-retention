# Case 111 Deepening — Oracle F640 / 6.4 TB NVMe SSD v1: Full-Media Refresh Duration and RF30

## Scope

This packet deepens [`111-enterprise-ssd-extended-shutdown-maintenance.md`](../cases/111-enterprise-ssd-extended-shutdown-maintenance.md) around one narrow question:

> Can a named enterprise NVMe product expose not only an extended-power-off risk and a powered maintenance policy, but also a bounded full-media coverage time and a firmware-versioned mitigation?

The answer for the Oracle 6.4 TB NVMe SSD v1 / related Flash Accelerator F640 family is **yes, within the exact limits of Oracle's November-2021 product notes**.

This is not a general SSD-retention survey, not a NAND-physics derivation, and not a claim that all 6.4 TB devices require two weeks of powered maintenance.

Current Case 111 maturity remains **`grounded`**.

## Source set and source roles

### Primary product documentation

1. Oracle, *Oracle 6.4 TB NVMe SSD v1 Product Notes*, updated November 2021, section **“Secure Erase Drives Before Use”**:
   - <https://docs.oracle.com/cd/E87231_01/html/F36828/gtlea.html>
   - primary named-product operational source;
   - directly documents Bug ID 27759886, RF30, long-unpowered failure symptoms, powered background refresh, approximately 14-day all-bit coverage, and the secure-erase / powered-wait workarounds.

2. Oracle, same product notes, **“Fixed Issues”**:
   - <https://docs.oracle.com/cd/E87231_01/html/F36828/gsjba.html>
   - primary firmware-release source;
   - places Bug ID 27759886 among issues fixed in RF30 and says secure erase implements the fix immediately, otherwise two weeks of powered operation fully resolves the issue.

3. Oracle, same product notes, **“Minimum Supported Oracle 6.4 TB NVMe SSD v1 Firmware Version”**:
   - <https://docs.oracle.com/cd/E87231_01/html/F36828/gpsdn.html>
   - primary firmware-version context;
   - records the RF30 release path and describes Bug ID 27759886 as a condition where a device left unpowered for several weeks may report uncorrectable-error symptoms or assert.

4. Oracle, *Oracle Flash Accelerator F640 PCIe Card v1 Product Notes*, **“Secure Erase Cards Before Use”**:
   - <https://docs.oracle.com/cd/E87231_01/html/E87232/gtbtj.html>
   - primary sibling-product witness;
   - repeats the same Bug ID, RF30 boundary, three-month unpowered risk framing, approximately 14-day full-bit refresh time, and powered-wait workaround for the F640 card form factor.

5. Oracle, F640 product notes, **“Minimum Supported Card Firmware Version”**:
   - <https://docs.oracle.com/cd/E87231_01/html/E87232/gpmga.html>
   - primary firmware-lineage witness;
   - documents the F640 firmware upgrade sequence and lists Bug ID 27759886 among RF30 key fixes.

### Adjacent internal comparison

- [`76-ocp-2021-2026-datacenter-nvme-retention-profile-deepening.md`](76-ocp-2021-2026-datacenter-nvme-retention-profile-deepening.md)
  - standards/profile comparison only;
  - do not treat the OCP qualification profile as an implementation description of Oracle firmware.

A fresh repository search in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) did not surface a dedicated Oracle F640 / RF30 retention-refresh packet. This document therefore keeps only the retention-specific control, timing, firmware, and evidence-boundary material here rather than rebuilding a broad F640 product history.

---

## Historical record

### H1 — Oracle documents a named extended-power-off failure condition

Oracle's November-2021 product notes identify **Bug ID 27759886**, marked **Fixed in Firmware Release RF30**.

For the **Oracle 6.4 TB NVMe SSD v1**, Oracle says the device may report uncorrectable errors or assert after being left unpowered for three or more months. The same section says that if the NAND media is not refreshed for approximately three months, media errors may occur.

The F640 card product notes repeat the same Bug ID and the same broad power-off / media-refresh condition.

This is a named-product and named-firmware product-support record. It is stronger than a generic statement that NAND charge decays while unpowered, but it remains bounded to Oracle's documented product context.

### H2 — Oracle explicitly describes powered background refresh

The Oracle SSD product note states that, while the drive remains powered, **drive firmware policy refreshes the media in the background**.

This is direct product-level evidence for:

```text
power available
    -> firmware-policy background refresh opportunity
```

It does not by itself expose the scheduler, scan order, media geometry, rewrite threshold, ECC threshold, or mapping operation used internally.

### H3 — Oracle gives an unusually explicit all-bit coverage time

Oracle says that if the drive has been powered long enough for the background refresh policy to be applied to **all bits**, the drive is not at risk for this documented issue, and that the time required to refresh all bits is **approximately 14 days and varies by product**.

The workaround is correspondingly explicit: keep the drive powered for **two weeks** for media refresh before using it.

The fixed-issues table independently says that, unless the immediate secure-erase sequence is used, **after two weeks of device power-on the issue will be fully resolved**.

This gives Case 111 a named-product timing witness that is materially more specific than a generic “leave it powered for maintenance” instruction.

### H4 — Oracle exposes two different remediation paths

Oracle gives two alternatives before use:

1. use the RF30 mitigation firmware and perform secure erase; or
2. wait two weeks while the drive remains powered for media refresh.

Oracle warns that erase destroys all device data.

The source later says that if an immediate refresh of all bits is desired, secure erase can be used.

These two procedures must not be collapsed into one operation:

```text
non-destructive powered background maintenance
    !=
destructive secure erase remediation
```

The fact that both can remove the documented risk does not make them semantically equivalent with respect to payload preservation.

### H5 — RF30 is a retention-relevant firmware epoch

Oracle's fixed-issues table places Bug ID 27759886 among issues fixed in **QDV1RF30**. The firmware summary likewise says the SFF device may report UE errors or assert after sitting unpowered for several weeks, and that secure erase immediately implements the fix while two weeks of powered operation fully resolves the issue.

The product notes also show later RF35 firmware and identify Oracle 6.4 TB NVMe SSD examples with Intel as manufacturer and model strings including `7335940:ICDPC2DD2ORA6.4T` / `7335943:ICDPC5ED2ORA6.4T`.

This supports:

```text
inventory-level product identity
    !=
retention-relevant firmware epoch
```

It does **not** reveal which exact internal algorithm changed between RE14 / RD28 / RF30, nor whether the approximately-14-day policy first appeared in RF30.

### H6 — Oracle distinguishes correctable margin exhaustion from host-visible failure

Oracle explains that if the number of affected bits exceeds ECC capability, an uncorrectable read error may result. During normal operation, such errors can increase SMART media-error counts; during power-on, the drive may instead report ASSERT or BAD_CONTEXT codes.

This is useful because the documented hazard is not simply “three months elapsed.” The operational symptom depends on accumulated media condition relative to error-correction capability and on when the error becomes visible.

The source does not provide a quantitative ECC-margin curve or a deterministic time-to-failure distribution.

---

## Engineering reconstruction

The following reconstruction is project analysis, not Oracle terminology.

### E1 — Case 111 now has a direct coverage-duration witness

A minimal state decomposition for this product episode is:

```text
extended unpowered interval
    ↓
retention margin degrades on some NAND state
    ↓
power restored
    ↓
background refresh policy admitted
    ↓
media coverage progresses
    ↓
policy applied to all bits
    ↓
documented issue no longer presents the same risk
```

The key addition is that Oracle supplies a bounded statement about **coverage completion time**:

```text
approximately 14 days
for the policy to reach all bits
```

That is not merely a recommended calendar dwell chosen without an implementation claim; Oracle directly connects the two-week powered interval to all-bit refresh coverage for this product issue.

### E2 — Opportunity, progress, and completion remain separate states

Oracle's wording supports this distinction:

```text
powered on
    !=
background refresh admitted / running
    !=
all-bit coverage reached
```

The two-week duration matters precisely because power restoration is only a maintenance opportunity. The source does not say that a brief boot or several hours under power is equivalent to completion.

### E3 — Approximate 14-day completion is not a capacity-scaling law

The device is a named **6.4 TB** NVMe SSD, and Oracle explicitly says the all-bit refresh time is approximately 14 days and **varies by product**.

That supports one measured/defined product point:

```text
named 6.4 TB product
    -> approximately 14-day documented all-bit refresh time
```

It does not support:

```text
refresh duration = capacity / universal constant
```

No inspected source gives a throughput figure, used-data dependency, NAND-channel model, background-idle fraction, or scaling equation. Case 111 should therefore use this as a named-product timing witness, not as a formula for other drives.

### E4 — “All bits” is vendor coverage vocabulary, not an exposed physical traversal trace

Oracle's product note says the background refresh policy is applied to all bits and that all bits can be refreshed.

For evidence discipline, this is retained as Oracle's product-level coverage description. It is not silently expanded into claims that the host can observe:

- every NAND page address;
- every physical cell rewrite;
- a particular block-by-block order;
- an FTL relocation for every logical sector;
- a full-device host read;
- a sanitize operation.

The internal mechanics remain opaque in the inspected source.

### E5 — Firmware fix and maintenance execution are different layers

RF30 is documented as fixing the issue, while the operational text still offers two ways to reach a safe state: immediate destructive erase or approximately two weeks of powered background refresh.

A useful model is therefore:

```text
firmware epoch / policy capability
    !=
current media state
    !=
maintenance progress
    !=
maintenance completion
```

Installing or possessing RF30 is not, by itself, proof that payload already written under an earlier or long-unpowered condition has completed the background refresh pass.

### E6 — Secure erase is a different kind of “reset” of the retention problem

Secure erase can quickly remove the documented old-media condition, but it also destroys payload.

For a retention atlas this is important:

```text
restore future medium margin while preserving payload
    !=
restore medium state by discarding payload
```

Both can be operationally valid remediation paths while carrying opposite consequences for the object being retained.

---

## Functional comparison

### F1 — IBM / Dell / Oracle show implementation-specific maintenance time

Case 111 already contains operator guidance where IBM and Dell assign powered dwell windows after extended shutdown and where Dell warns that capacity can increase required powered duration.

Oracle adds a much more product-specific point: approximately **14 days for all-bit coverage** on the documented 6.4 TB NVMe SSD v1 / F640 issue.

The safe cross-product conclusion is:

```text
extended-offline maintenance duration
    is implementation / product / workload dependent
```

The unsafe conclusion would be to transfer Oracle's two-week number to IBM, Dell, another Intel SSD, or another 6.4 TB NVMe device.

### F2 — Case 76 qualification profile is not Oracle's recovery procedure

Case 76 documents OCP datacenter-NVMe retention profiles and temperature / lifetime assumptions. Those profiles describe qualification and required behavior at a standards/profile layer.

Oracle's product note instead documents a particular field issue, firmware epoch, remediation, and all-bit background refresh time.

Keep the layers distinct:

```text
retention qualification profile
    !=
field-failure manifestation
    !=
firmware repair
    !=
operator recommissioning procedure
    !=
all-bit maintenance completion time
```

No historical genealogy between the OCP profile and Oracle's RF30 behavior is asserted here.

### F3 — Relation to Intel firmware-version evidence

The separate Case 111 Intel firmware-history packet establishes that named Intel SSD families can receive firmware revisions described as changes to NAND-refresh algorithms.

Oracle's product note shows a different but complementary pattern: a named Oracle/Intel NVMe product has a firmware-versioned fix tied to an explicit long-unpowered issue and a documented background-refresh completion duration.

Do not merge the two evidence chains into one implementation genealogy merely because Oracle's examples identify Intel as manufacturer.

```text
same manufacturer name in product inventory
    !=
same refresh algorithm
    !=
same firmware lineage as another Intel retail/OEM family
```

---

## Philosophical interpretation

The interpretive value of this episode is not that “data fades unless humans remember to turn machines on.” That slogan loses the technical structure.

A more disciplined interpretation is:

> A retained payload can depend on a maintenance process whose **opportunity, coverage, duration, and implementation epoch** are themselves separate states. A system may be powered and readable before the maintenance relation that makes a future offline interval trustworthy has finished.

Oracle's destructive alternative also sharpens a second distinction:

> A medium can be returned to a technically favorable state either while retaining the payload or by discarding it. “The medium is healthy again” and “the information was retained” are therefore not equivalent propositions.

These are project interpretations, not historical claims about Oracle's design intent.

---

## Explicit non-claims

This packet does **not** claim that:

1. all enterprise SSDs fail after three months unpowered;
2. three months is a universal physical NAND deadline;
3. all 6.4 TB SSDs require approximately 14 days of powered refresh;
4. refresh time scales linearly with advertised capacity;
5. Oracle exposes the internal traversal order of the refresh pass;
6. “all bits” proves a host-observable rewrite of every NAND cell;
7. every bit is physically rewritten rather than examined and conditionally renewed;
8. the host can query exact background-refresh percentage complete;
9. the source exposes a device-local completion telemetry field;
10. refresh progress survives a reset or interrupted power cycle;
11. an interrupted two-week interval resumes exactly where it stopped;
12. RF30 installation itself proves all pre-existing payload has been refreshed;
13. RF30's internal algorithm is the same as the Intel 540s, Pro 5450s, 760p, or Coulson patent mechanisms elsewhere in Case 111;
14. secure erase preserves existing user payload;
15. secure erase and background refresh are the same maintenance primitive;
16. a SMART media-error count is a direct measure of retention margin;
17. absence of SMART errors proves completion of the background refresh pass;
18. an Oracle F640 card and every Oracle 6.4 TB SFF implementation are identical below the documented common issue / firmware family boundary;
19. November 2021 is the first historical appearance of the underlying RF30 behavior;
20. a product-note update date is an invention, implementation, or first-shipment date.

---

## What this closes in Case 111

This packet materially advances three existing debts.

### Capacity / duration

**Partially closed.** There is now a direct named-capacity / named-product witness for an approximately 14-day all-bit refresh duration.

Still open: scaling law, used-data dependence, bandwidth, idle dependence, and independent measurement.

### Firmware-policy drift tied to operator-visible behavior

**Partially closed.** Oracle ties Bug ID 27759886 to RF30 and provides a concrete operator recovery window and mitigation path in the same product documentation.

Still open: exact algorithm delta and whether the approximately-14-day traversal duration itself changed between firmware revisions.

### Post-offline recovery semantics

**Strengthened but not closed.** Oracle documents both powered background recovery and destructive secure erase after the long-unpowered condition.

Still open: progress persistence, restart after interruption, and non-destructive completion telemetry.

---

## New high-value follow-up

The next useful slice is no longer “find another SSD that says refresh.” Higher-value questions are:

1. Does this firmware expose any vendor log, SMART field, event, or diagnostic that proves the approximately-14-day pass has completed?
2. If power is interrupted during the two-week refresh, is progress retained, reconstructed, or restarted?
3. Can an older Oracle product-note revision date the first appearance of Bug 27759886 / RF30 guidance more tightly than the November-2021 maintained manual?
4. Is there a contemporaneous Intel OEM firmware advisory that maps the Oracle model strings to a specific Intel platform while preserving the product/firmware evidence boundary?
5. Is there a controlled measurement showing error-margin or media-error change before and after the full-media pass?

## Status decision

**No maturity promotion.**

Case 111 remains `grounded`.

The Oracle evidence is unusually strong for a named product's **coverage duration** and for separating destructive immediate remediation from non-destructive powered background maintenance. It still does not establish progress persistence across interruption, device-local completion telemetry, a general capacity-scaling law, or independent validation.