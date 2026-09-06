# NVMe SMART / Health endurance telemetry grounding record

Companion to [`../cases/55-nvme-smart-health-endurance-telemetry.md`](../cases/55-nvme-smart-health-endurance-telemetry.md).

**Canonical maturity status is tracked in [`../CASE_INDEX.md`](../CASE_INDEX.md).**

## Grounding question

Can the project establish, from primary interface documentation and a named product witness, that an SSD retains non-payload history/health state across power cycles, while keeping cumulative history, current warning state, host workload counters, spare reserve, and model-derived endurance estimates technically distinct?

The answer is yes for the bounded NVMe 1.0–1.3 record. The original 2011 Gold revision additionally grounds the boundary between spare-threshold warning, lack of spare locations, and command failure.

## Source 0 — official NVM Express Revision 1.0 Gold

**Document:** `NVM Express Revision 1.0`, ratified **1 March 2011**.

Official PDF: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_0-Gold.pdf>

The official PDF was directly inspected in this slice, including facsimile inspection of the structured SMART/Health table.

### 0.1. The original 1.0 log already retains lifetime health information

**§5.10.1.2, printed p. 64; Figure 59, printed p. 65.**

Revision 1.0 says SMART/general health information is provided over the life of the controller and retained across power cycles. Figure 59 already defines `Available Spare`, `Available Spare Threshold`, `Percentage Used`, and the separate critical-warning bits for spare threshold, reliability degradation, and read-only media.

`Percentage Used` already carries the explicit boundary that 100 means estimated endurance consumed but **may not indicate device failure** and may exceed 100.

This prevents a false chronology in which those relations first appear in 1.0e or 1.3.

### 0.2. Spare-threshold notification is not spare exhaustion

**Asynchronous Event Request status table, printed p. 55.**

Revision 1.0 defines a `Spare Below Threshold` condition: available spare space has fallen below the threshold. The condition describes a threshold crossing, not zero remaining reserve.

Therefore the primary source itself supports keeping:

`spare below threshold ≠ spare exhausted`.

### 0.3. Lack of spare locations is a possible cause of Write Fault

**Generic Command Status, printed p. 49.**

Status `80h Write Fault` says the write data could not be committed to the media and that this **may** be due to lack of available spare locations reported as an asynchronous event. Status `81h Unrecovered Read Error` is separately defined as read data that could not be recovered from the media.

This grounds a bounded failure bridge:

```text
remaining reserve / threshold evidence
        ≠
actual inability to commit a write
        ≠
unrecovered read failure
```

The word `may` is important. It allows `lack of spare locations -> possible Write Fault cause`; it does **not** allow the converse claim `every Write Fault -> proven spare exhaustion`.

### 0.4. Interface evidence does not expose the internal replacement mechanism

Revision 1.0 reports reserve and failure semantics but does not, in these clauses, define a particular NAND bad-block table, FTL allocation algorithm, physical replacement-pool geometry, or automatic reassignment sequence. Those mechanisms must be grounded from lower-layer/product evidence such as Case 78 rather than inferred from host telemetry.

## Source A — official NVM Express 1.0e

**Document:** `NVM Express 1.0e`, NVM Express, Inc.; the front matter says revision 1.0 was ratified 1 March 2011 and 1.0e incorporates later ECNs.

Official PDF: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_0e.pdf>

### A1. SMART/Health is lifetime information retained across power cycles

**§5.10.1.2, printed p. 67.**

The specification says the SMART / Health Information log provides SMART and general health information, that the information is `over the life of the controller`, and that it is `retained across power cycles`.

This is direct primary evidence for **history-bearing controller state** rather than a reconstruction from modern tooling.

### A2. Available Spare and threshold are maintenance/reserve state

**Figure 60, printed p. 68.**

`Available Spare` is a normalized 0–100% value for remaining spare capacity. `Available Spare Threshold` can cause an asynchronous event when the remaining spare falls below the threshold.

The standard does not call this filesystem free space or user payload capacity.

### A3. Percentage Used is a vendor-specific estimate, not a failure bit

**Figure 60, printed p. 68.**

The field is defined as a `vendor specific estimate` of percentage of device life used based on actual usage plus the manufacturer's prediction of device life. The specification explicitly says:

- 100 means estimated endurance has been consumed;
- this **may not indicate device failure**;
- the value may exceed 100;
- values greater than 254 are represented as 255;
- the value is updated once per power-on hour when the controller is not asleep.

The standard refers to JEDEC JESD218 for SSD endurance measurement techniques.

This wording directly blocks `100% = dead` and `Percentage Used = exact physical remaining life`.

### A4. Data Units Written is a host-interface quantity

**Figure 60, printed p. 68.**

`Data Units Written` counts 512-byte units the **host has written to the controller**, excludes metadata, and is reported in thousands. It is not normatively defined as NAND page-program count, erase count, garbage-collection traffic, or write-amplified physical bytes.

The safe reconstruction is therefore:

> host workload evidence is not identical to the hidden physical-media work ledger.

### A5. The same log retains other compressed histories

**Figure 60, printed pp. 68–69.**

The interface also includes power cycles, power-on hours, unsafe shutdowns, media errors, and number of Error Information log entries over the life of the controller.

`Media Errors` in 1.0e counts **unrecovered** integrity errors such as uncorrectable ECC, CRC failure, or LBA-tag mismatch. This does not license the claim that every corrected raw-media error is represented there.

## Source B — official NVM Express Revision 1.3

Official PDF: <https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf>

### B1. Lifetime retention remains, but Critical Warning is explicitly current/nonpersistent

**§5.14.1.2, printed pp. 98–99.**

Revision 1.3 again describes SMART/Health information as lifetime information retained across power cycles. Figure 93 then adds a crucial sentence to `Critical Warning`: the bits represent the **current associated state and are not persistent**.

The same figure continues to expose Available Spare, Percentage Used, host data-unit counters, power/unsafe-shutdown counts, and lifetime error counts.

This supports a mixed temporal model within one host-visible structure:

```text
current nonpersistent warning bits
    !=
cumulative retained counters
    !=
model-derived endurance estimate
```

### B2. Percentage Used remains an estimate in 1.3

**Figure 93, printed p. 99.**

Revision 1.3 keeps the vendor-specific-estimate language, says 100 means estimated endurance consumed but may not mean subsystem failure, permits values above 100, and specifies once-per-power-on-hour updating.

The persistence distinction is therefore not a reason to reinterpret the estimate as a deterministic failure timer.

### B3. Unrecovered errors remain distinct from all error-correction work

**Figure 93, printed p. 100.**

`Media and Data Integrity Errors` counts controller-detected **unrecovered** integrity errors, including examples such as uncorrectable ECC, CRC failure, or LBA-tag mismatch. That wording matters when comparing this interface to Case 45 ECS/ODECC or Case 36 NAND ECC: successful correction work can exist without entering this unrecovered-error count.

## Source C — NVM Express Specification Archives

Official archive: <https://nvmexpress.org/nvm-express-specification-archives/>

The archive lists the 1.0e, 1.1, 1.2, 1.3 and later families. It is used only to bound version chronology and prevent a false `1.3 invented SMART/Health endurance telemetry` narrative.

## Source D — Intel DC P3700 Product Specification, July 2014

**Document:** Intel, `Intel Solid-State Drive DC P3700 Series Product Specification`, order number **330566-002US**, July 2014.

Surviving transcript/mirror inspected: <https://manualzilla.com/doc/7195133/intel-dcp3700-1.6tb>

### D1. Named-product support for the mandatory NVMe 1.0 health log

The product specification says the P3700 supports the mandatory log pages defined in NVMe 1.0, including `SMART / Health Information (Log Identifier 02h)`.

Its SMART table includes:

- `Available Spare`, starting from 100 and decrementing;
- `Available Spare Threshold`, set to 10% for the bounded product;
- `Percentage Used Estimate`, including the same `100 may not indicate device failure` boundary;
- `Data Units Read` and `Data Units Write` plus command counters.

This is a named commercial device witness from 2014, not just a standards proposal.

### D2. Hidden maintenance capacity and stable logical capacity are separately documented

The P3700 specification says its user-addressable LBA count remains the same throughout drive life while a small portion of physical capacity is used for NAND media management and maintenance.

This supports:

> stable host-visible capacity does not imply absence of reserved physical maintenance capacity.

It does **not** prove that all non-user physical capacity is exactly the same pool represented by `Available Spare`; the case refuses that stronger inference.

### Provenance limit

The Intel document is authoritatively identified by title, order number, revision date, and internal page text, but the accessible copy in this environment is a third-party preservation/transcript rather than a current Intel-hosted PDF. Product-specific claims are therefore labeled with that provenance. The core normative claims depend on the official NVM Express PDFs.

## Source E — later NVM Express institutional explanation

NVM Express later published `Features for Error Reporting, SMART, Log Pages, Failures and management capabilities in NVMe Architectures`:

<https://nvmexpress.org/resource/features-for-error-reporting-smart-log-pages-failures-and-management-capabilities-in-nvme-architectures/>

It describes `Percentage Used` as the main endurance-monitoring quantity and Available Spare as another endurance-related health indicator. This is useful later institutional corroboration of operational interpretation, but it is **not** used to establish 2011/2014 priority or original wording.

## Evidence ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| Original NVMe 1.0 already exposes Available Spare and Spare Below Threshold | `H/P` | NVMe 1.0 Fig. 59 + asynchronous-event status | strong official 2011 primary |
| Lack of spare locations is one possible cause of `Write Fault` | `H/P` | NVMe 1.0 Generic Command Status 80h | strong official 2011 primary |
| `Write Fault` and `Unrecovered Read Error` are separate statuses | `H/P/E` | NVMe 1.0 status 80h vs 81h | strong official primary; relation-level reconstruction |
| A spare-threshold event proves reserve exhaustion or current payload loss | `X` | threshold wording does not say this | rejected |
| Every `Write Fault` proves spare exhaustion | `X` | contradicted by normative `may be due` wording | rejected |
| SMART/Health includes information retained across power cycles | `H/P` | NVMe 1.0e §5.10.1.2; NVMe 1.3 §5.14.1.2 | strong official primary |
| Percentage Used is vendor-specific and 100 need not mean failure | `H/P` | NVMe 1.0e Fig. 60; NVMe 1.3 Fig. 93 | strong official primary |
| Data Units Written measures host-to-controller data, not normatively internal NAND work | `H/P/E` | NVMe 1.0e/1.3 field definition | strong bounded reconstruction |
| 1.3 Critical Warning bits are current and nonpersistent | `H/P` | NVMe 1.3 Fig. 93 | strong official primary |
| media/data-integrity error count concerns unrecovered errors | `H/P` | NVMe 1.0e Fig. 60; NVMe 1.3 Fig. 93 | strong official primary |
| P3700 2014 implements mandatory NVMe 1.0 SMART/Health | `H/P` | Intel 330566-002US product spec | strong named-product witness, mirror provenance |
| P3700 has non-user physical capacity for NAND management/maintenance while LBA count stays stable | `H/P` | Intel 330566-002US product spec | strong named-product witness, mirror provenance |
| SMART/Health exposes complete physical wear history | `X` | not supported; counter/estimate definitions are aggregated/interface-level | rejected |
| Percentage Used exactly predicts failure time | `X` | explicitly contradicted by 100-may-not-indicate-failure wording | rejected |
| NVMe 1.3 invented these endurance fields | `X` | contradicted by 1.0e and 2014 P3700 | rejected |

## Cross-case boundary

- **Case 14:** SCSI grown-defect reassignment directly grounds finite spare-location consumption and a `NO DEFECT SPARE LOCATION AVAILABLE` failure; NVMe 1.0 is compared only as a later host-interface reserve/failure relation, not as genealogy.
- **Case 78:** Micron NAND bad-block management directly grounds reserved replacement blocks and BBT-controlled exclusion. NVMe `Available Spare` does not prove that a conforming SSD uses that exact internal mechanism.
- **Case 76:** JEDEC workload-qualified endurance and NVMe `Percentage Used` concern life/endurance qualification; they must not be collapsed into the separate `Available Spare` reserve relation.
- **Case 36:** physical NAND error/refresh mechanism ≠ host-visible health estimate.
- **Case 38:** product-specific PLI readiness/self-test state ≠ generic NVMe SMART/endurance telemetry.
- **Case 45:** correctable ECC/ECS work ≠ unrecovered-error counter.
- **Case 52:** access-induced read-disturb stress ≠ host Data Units Written.
- **Case 54:** activity-pressure state that directly schedules DRAM maintenance ≠ SSD lifetime estimate/counter exposed for health management.

These are functional comparisons only.

## Related-repository check

A GitHub search of `tmzncty/computing-archaeology` for NVMe SMART / `Percentage Used` / P3700 endurance telemetry returned no dedicated case. Therefore no existing technical history was duplicated. If a broad history of SSD health monitoring, ATA SMART, JEDEC endurance methodology, or controller wear modeling is later written, it belongs primarily in `computing-archaeology`; this repository should retain the narrower state/history distinction.

## Readiness assessment

The bounded case is ready for `grounded` status because it has:

- official normative evidence from two historical NVMe revisions;
- exact section/figure/page anchors;
- an explicit chronology boundary back to NVMe 1.0;
- a named 2014 commercial-device witness;
- a provenance caveat for the preserved Intel copy;
- explicit rejected claims about exact physical wear, failure prediction, and invention priority;
- cross-case boundaries to physical refresh, ECC, PLI validation, read disturb, and maintenance-state cases.

Future work should be separate slices: ATA SMART genealogy; JEDEC JESD218 methodology; independent calibration of `Percentage Used` against named-device physical wear/failure; modern NVMe telemetry/endurance-group extensions; and fleet-level replacement policy.
