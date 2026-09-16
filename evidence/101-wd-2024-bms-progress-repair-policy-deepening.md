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

### S3 — Hitachi 2008 BMS persistence-horizon deepening

- [`101-hitachi-2008-bms-policy-log-persistence-deepening.md`](101-hitachi-2008-bms-policy-log-persistence-deepening.md)
- **Evidence class:** `H/P` named-product specification plus bounded contemporaneous T10 standards-development interpretation.

The 29 October 2008 Hitachi Ultrastar 15K450 specification supplies an earlier, independent-from-Seagate named-product witness for no in-scan reassignment and, more importantly, directly separates saveable Background Control policy from current progress/log state. Its MODE SELECT contract says `SP=1` mode-page data are saved in the disk Reserved Area and maintained across power cycle/reset, while `SP=0` values expire on power removal/reset. Its BMS status and medium-scan entries expose `DS=0` / `TSD=0`, which the companion record interprets conservatively against period T10 log-save semantics rather than as proof of an atomically durable latest scan position.

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

The 2024 HC590 text inspected here does not by itself identify the storage location or say that the exact suspended LBA survives reset, power cycle, firmware replacement, or format. The companion Hitachi 2008 deepening now closes a narrower documentation-level question: **BMS policy can be stored as saveable mode-page state across reset/power boundaries, while BMS log parameters are save-capable under period SCSI semantics.** It still does not prove that the latest in-flight traversal position is atomically durable across unexpected power loss.

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

The new Hitachi 2008 record shows this was not merely a 2024 Western Digital product choice: a Hitachi Ultrastar SAS product already documented `Reassignment during the background scan is not supported` in 2008. Because Hitachi and later HGST became part of Western Digital, this extends the product-line documentation chronology but should not be counted as two cleanly independent long-run engineering lineages.

### H4 — shared interface vocabulary does not imply identical vendor repair policy

The existing Case 101 Seagate witness says unreadable and recovered-error sites are logged or reallocated according to ARRE/AWRE settings. HC590 uses the same broad BMS control/result family but explicitly does not support reassignment during the scan. Hitachi 15K450 independently documents the latter policy in 2008.

This supports only a product-comparison statement:

`standardized control/reporting relation != identical vendor repair implementation`

It does **not** prove a chronological trend from automatic repair to host-managed repair, nor a Seagate→Hitachi→Western Digital genealogy.

### H5 — scan-result evidence has several horizons

The HC590 contract exposes at least four horizons:

1. current active/suspended/halted status;
2. current scan progress;
3. lifetime scan counts;
4. individual error entries with the power-on minutes when an error was detected.

These should not be collapsed into one `scan history`.

Engineering reconstruction:

`current maintenance state != cumulative summary != event record != payload`

The 2008 companion record adds a fifth distinction at the control plane:

`persistent maintenance policy != current traversal checkpoint`

The sources still do not establish the exact update/atomicity rules for every individual error entry or the newest scan-position checkpoint under abrupt power loss.

---

## Cross-case / canonical-case implications

This deepening strengthens Case 101 rather than creating a second SCSI BMS case.

### Existing Case 101 relation

The canonical case already separates:

`physical presence -> proactive readability check -> defect evidence -> repair permission -> later reassignment`

The HC590 adds a useful implementation counterexample inside that chain: a drive can implement BMS status/progress and defect discovery while declining in-scan reassignment.

The Hitachi 2008 companion evidence further adds a control-state layer:

```text
saved BMS policy
        ↓ power/reset reconstitution
current BMS policy
        ↓ schedule / idle opportunity
BMS execution + progress
        ↓
defect/result evidence
        ↓
repair authority branches
```

So the better generic model is not:

```text
BMS -> automatic sector relocation
```

and not:

```text
BMS enabled -> exact progress checkpoint is crash durable
```

### Case 14 — SCSI defect reassignment

Case 14 remains canonical for logical identity across physical reassignment. HC590 and Hitachi 15K450 reinforce that Case 101's proactive discovery path can stop **before** reassignment and hand authority to the application client.

### Cases 18 / 83 — higher-layer scrub/scanner

Nothing in HC590 changes the existing boundary: drive-local BMS qualifies medium readability under drive error-recovery semantics; ZFS/HDFS verify higher-layer checksum/replica relations. Current drive scan progress or persisted BMS policy cannot stand in for higher-layer integrity evidence.

---

## Philosophical limit

The bounded interpretive addition is about **maintenance evidence and maintenance policy having plural temporal horizons**. A device can retain a maintenance regime across reset/power boundaries, expose a current traversal point, retain cumulative counts, and record event-specific defect evidence without any of them being the user payload or a complete history of the medium.

This strengthens the repository's distinction between first-order retained state and second-order maintenance state, but it does not make a saved mode page, scan counter, or BMS result log an archive, a memory of every sector, or a philosophical `retention` in Stiegler's sense.

---

## Stop conditions

Do **not** infer from these sources that:

- Western Digital, HGST, or Hitachi invented BMS or the SCSI BMS interface;
- 2008 Hitachi or 2024 HC590 semantics describe every SCSI/SAS drive;
- Seagate 2007, Hitachi 2008, and Western Digital 2024 firmware share one implementation lineage;
- different corporate mastheads automatically establish independent engineering lineages;
- the current scan position is atomically crash-durable or power-loss persistent;
- `DS=0` or `TSD=0` means every latest BMS update is already safely stored after every event;
- lifetime scan counts are a complete per-LBA history;
- a successful scan is a timeless integrity certificate;
- `reassignment not supported during BMS` means the drive can never reassign sectors by other paths;
- host/application-client reassignment implies secure erasure of the old physical sector;
- BMS status proves ZFS/HDFS/application end-to-end integrity.

---

## Related-repository boundary

Fresh `tmzncty/computing-archaeology` searches for `C15K600` and `Background Media Scan` returned no dedicated study in this run. Broader cross-vendor BMS/SMART/patrol-read genealogy, Hitachi/HGST/Western Digital firmware continuity, SCSI mode/log persistence history, and implementation experiments should live there if developed; this file remains a narrow Case 101 product-contract deepening.

---

## Remaining debt

- perform abrupt reset/power-loss testing on named drives to determine whether the **latest** BMS traversal position and newest log entries survive, and at what checkpoint granularity; the 2008 Hitachi record closes only the weaker documentation-level facts that BMS policy can be saved across reset/power and BMS log parameters are save-capable/implicitly saveable under period SCSI semantics;
- inspect a final SPC-4 revision around the 2008 product date line-by-line for exact normative DS/TSD/list-parameter semantics;
- compare another genuinely independent later SAS vendor rather than treating Hitachi/HGST/Western Digital corporate-document multiplicity as multiple independent implementations;
- connect BMS progress/persistence to controlled fault/load experiments rather than documentation alone.