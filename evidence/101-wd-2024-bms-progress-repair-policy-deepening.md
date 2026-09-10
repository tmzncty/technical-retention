# Evidence 101 deepening — Western Digital 2024 BMS progress and repair-policy boundary

**Canonical case:** [`../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md`](../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md)

**Bounded question:** does later first-party product evidence support treating SCSI Background Medium Scan as one fixed `scan-and-repair` behavior, or does the interface preserve distinct lifetimes and authorities for scan progress, cumulative scan evidence, defect discovery, and reassignment?

**Status:** `grounded` for the named Western Digital Ultrastar DC HC590 SAS product contract, with the existing 2005 T10 / 2007 Seagate Case 101 evidence used only for comparison. This is a deepening of Case 101, **not a new BMS case**.

---

## Source ledger

### S1 — Western Digital, *Ultrastar DC HC590 SAS Hard Disk Drive Specification*, Rev. 1.0

- **Date:** 31 October 2024.
- **Models named on title page:** WUH722626AL5201 / AL5204 and WUH722624AL5201 / AL5204.
- **Manufacturer:** Western Digital.
- **URL:** <https://documents.westerndigital.com/content/dam/doc-library/en_us/assets/public/western-digital/product/data-center-drives/ultrastar-dc-hc500-series/product-manual-ultrastar-dc-hc590-sas.pdf>
- **Evidence class:** `H/P` — first-party named-product specification.
- **Primary locations:** §8.8.12, printed pp. 126–127, Log Sense Page 15; §8.11.15.1, printed p. 181, Background Control Subpage 01h.

The title page identifies Revision 1.0 and 31 October 2024. The BMS status page exposes current BMS status, `Number of Background Scans Performed`, `Medium Scan Progress`, and `Number of Background Medium Scans Performed`. The text states that the count fields accumulate **over the life of the drive**. The medium-scan parameter contains error-time power-on minutes, reassignment status, error codes, and location data.

The same section explicitly says: **“Reassignment during the background scan is not supported.”** The product instead exposes states in which reassignment is pending a host `REASSIGN` or write, an error has been successfully rewritten, or an application client has successfully reassigned it.

The Background Control page states that setting `EN_BMS` from one to zero during a scan suspends it; re-enabling BMS resumes from the suspended location. The page also separately exposes the BMS interval and minimum idle time.

### S2 — existing Case 101 grounding record

- [`101-t10-2004-2007-background-medium-scan-grounding.md`](101-t10-2004-2007-background-medium-scan-grounding.md)
- **Evidence class:** existing `H/P` primary-source grounding.

The canonical record already grounds T10 `04-198r5`, the 2005 approval/2006 clarification path, and a 2007 Seagate Cheetah 15K.5 product witness. It already establishes that the standardization work separated detection, logging, ARRE/AWRE permission, repair/reassignment, pre-scan, foreground preemption, and scan coverage. This deepening does not repeat that work.

---

## Historical / product findings

### H1 — current scan progress and lifetime scan count are different retained maintenance state

HC590 §8.8.12 reports both:

- a current `Medium Scan Progress` fraction; and
- counts of background scans / background medium scans performed **over the life of the drive**.

This creates a direct named-product distinction:

`current traversal state != cumulative maintenance-history summary`

The lifetime count is still only a summary. It does not identify which LBA passed which scan at what time and therefore is not a complete per-sector verification history.

### H2 — BMS status can outlive one execution burst without becoming payload

The status page distinguishes no scan active, BMS active, halted states, and suspension until the interval timer expires. The control page separately allows an in-progress scan to be suspended by clearing `EN_BMS` and later resumed from the suspended location.

The safe bounded claim is:

`maintenance execution lifetime != maintenance-control/progress lifetime`

This is not evidence for power-loss persistence. The specification does not, in the inspected text, identify the storage location or say that the suspended LBA survives reset, power cycle, firmware replacement, or format.

### H3 — later named-product behavior blocks a universal `BMS = automatic reassignment` reading

HC590 states directly that reassignment **during the background scan is not supported**. Its result-state table instead includes:

- no reassignment needed;
- reassignment pending host REASSIGN or write;
- successful rewrite;
- successful reassignment by the application client.

This is a strong counterexample to a generic description in which `BMS` necessarily means that the drive scans and automatically relocates every suspect block.

Therefore:

`BMS support != automatic in-scan reassignment support`

and:

`defect detected != device-side relocation completed`

### H4 — shared interface vocabulary does not imply identical vendor repair policy

The existing Case 101 Seagate witness says unreadable and recovered-error sites are logged or reallocated according to ARRE/AWRE settings. HC590 uses the same broad BMS control/result family but explicitly does not support reassignment during the scan.

This supports only a product-comparison statement:

`standardized control/reporting relation != identical vendor repair implementation`

It does **not** prove a chronological trend from automatic repair to host-managed repair, nor a Seagate→Western Digital genealogy.

### H5 — scan-result evidence has several horizons

The HC590 contract exposes at least four horizons:

1. current active/suspended/halted status;
2. current scan progress;
3. lifetime scan counts;
4. individual error entries with the power-on minutes when an error was detected.

These should not be collapsed into one `scan history`.

Engineering reconstruction:

`current maintenance state != cumulative summary != event record != payload`

The source does not establish how long every individual error entry survives, whether logs wrap, or whether those entries survive every power/reset boundary.

---

## Cross-case / canonical-case implications

This deepening strengthens Case 101 rather than creating a second SCSI BMS case.

### Existing Case 101 relation

The canonical case already separates:

`physical presence -> proactive readability check -> defect evidence -> repair permission -> later reassignment`

The HC590 adds a useful implementation counterexample inside that chain: a drive can implement BMS status/progress and defect discovery while declining in-scan reassignment.

So the better generic model is:

```text
BMS control + scan progress
        ↓
proactive readability observation
        ↓
defect/result evidence
        ↓
repair authority branches
   ┌───────────────┬────────────────┐
   │ rewrite       │ host reassign  │
   │ (if supported)│ / later write  │
   └───────────────┴────────────────┘
```

not:

```text
BMS -> automatic sector relocation
```

### Case 14 — SCSI defect reassignment

Case 14 remains canonical for logical identity across physical reassignment. HC590 reinforces that Case 101's proactive discovery path can stop **before** reassignment and hand authority to the application client.

### Cases 18 / 83 — higher-layer scrub/scanner

Nothing in HC590 changes the existing boundary: drive-local BMS qualifies medium readability under drive error-recovery semantics; ZFS/HDFS verify higher-layer checksum/replica relations. Current drive scan progress cannot stand in for higher-layer integrity evidence.

---

## Philosophical limit

The only bounded interpretive addition is about **maintenance evidence having plural temporal horizons**. A device can retain a current traversal point, a cumulative count, and event-specific defect evidence without any of them being the user payload or a complete history of the medium.

This strengthens the repository's distinction between first-order retained state and second-order maintenance state, but it does not make a scan counter an archive, a memory of every sector, or a philosophical `retention` in Stiegler's sense.

---

## Stop conditions

Do **not** infer from this source that:

- Western Digital invented BMS or the SCSI BMS interface;
- 2024 HC590 semantics describe every SCSI/SAS drive;
- Seagate 2007 and Western Digital 2024 firmware share one implementation lineage;
- the current scan position is crash-durable or power-loss persistent;
- lifetime scan counts are a complete per-LBA history;
- a successful scan is a timeless integrity certificate;
- `reassignment not supported during BMS` means the drive can never reassign sectors by other paths;
- host/application-client reassignment implies secure erasure of the old physical sector;
- BMS status proves ZFS/HDFS/application end-to-end integrity.

---

## Related-repository boundary

A fresh `tmzncty/computing-archaeology` search for `background media scan SCSI` returned no dedicated study in this run. Broader cross-vendor BMS/SMART/patrol-read genealogy and implementation history should live there if developed; this file remains a narrow Case 101 product-contract deepening.

---

## Remaining debt

- test named-drive BMS progress/log persistence across reset and power loss;
- compare another contemporary SAS vendor for in-scan reassignment semantics;
- recover exact normative SBC/SPC wording for the HC590 generation and distinguish mandatory interface semantics from optional vendor behavior;
- connect BMS progress to controlled fault/load experiments rather than documentation alone.