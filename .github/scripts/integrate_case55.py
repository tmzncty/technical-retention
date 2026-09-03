from pathlib import Path


def insert_after_line(text: str, needle: str, new_line: str, *, label: str) -> str:
    lines = text.splitlines()
    matches = [i for i, line in enumerate(lines) if needle in line]
    if len(matches) != 1:
        raise SystemExit(f"{label}: expected exactly one anchor, found {len(matches)}")
    lines.insert(matches[0] + 1, new_line)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def replace_once(text: str, old: str, new: str, *, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"{label}: expected exactly one occurrence, found {n}")
    return text.replace(old, new, 1)


CASE = Path("cases/55-nvme-smart-health-endurance-telemetry.md")
EVIDENCE = Path("evidence/55-nvme10-13-smart-health-endurance-grounding.md")
if CASE.exists() or EVIDENCE.exists():
    raise SystemExit("Case 55 or evidence file already exists; refusing duplicate integration")

case_text = r'''# NVM Express SMART / Health Endurance Telemetry: Retained Device History Without Payload History

## Status

**`grounded`** — bounded to the NVMe 1.0e/1.3 SMART / Health Information interface and a 2014 Intel DC P3700 product witness. The case establishes that an SSD can retain cumulative health/endurance evidence across power cycles and expose it to host software without that evidence being the user payload or a complete physical wear history.

Grounding record: [`../evidence/55-nvme10-13-smart-health-endurance-grounding.md`](../evidence/55-nvme10-13-smart-health-endurance-grounding.md).

## Scope

This case asks a narrow retention question:

> What changes when the storage device retains facts about **its own past use and degradation** in order to qualify future service?

The object is the NVMe `SMART / Health Information` log, especially:

- `Percentage Used`;
- `Available Spare` and `Available Spare Threshold`;
- `Data Units Written`;
- `Power Cycles`, `Power On Hours`, and `Unsafe Shutdowns`;
- `Media and Data Integrity Errors` / `Media Errors`;
- the distinction between cumulative/lifetime information and the current `Critical Warning` state.

This is not a general history of SMART, NAND endurance, wear leveling, SSD failure prediction, or enterprise fleet management. It also does not claim that the standardized host-visible counters expose the controller's complete internal P/E-cycle distribution, write amplification, bad-block map, ECC history, or physical degradation model.

## Historical record

### NVMe 1.0e already defines retained health history

The official NVM Express 1.0e specification states in §5.10.1.2 that the SMART / Health Information log provides information `over the life of the controller` and that the information is `retained across power cycles`.

Figure 60 then defines, among other fields:

- `Available Spare` as a normalized percentage of remaining spare capacity;
- `Available Spare Threshold`, whose crossing may cause an asynchronous event;
- `Percentage Used` as a **vendor-specific estimate** of device life used, based on actual usage and the manufacturer's prediction of device life;
- a value of `100` as estimated endurance consumed, explicitly **not necessarily device failure**;
- `Data Units Written` as the amount of host data written to the controller, excluding metadata;
- power-cycle, power-on-hour, unsafe-shutdown, media-error, and lifetime error-log-entry counters.

The specification says `Percentage Used` is updated once per power-on hour while the controller is not asleep. It points to JEDEC JESD218 for SSD life/endurance measurement techniques.

The NVM Express specification archive records the 1.0 family, and the 1.0e front matter says NVMe 1.0 was ratified on 1 March 2011. Therefore this case must not attribute the basic SMART/endurance fields to NVMe 1.3.

### NVMe 1.3 clarifies a mixed temporal regime inside one log page

NVMe 1.3 §5.14.1.2 preserves the same broad SMART/Health model but makes an especially useful distinction explicit: the `Critical Warning` bits represent the **current associated state and are not persistent**.

The same log page still includes cumulative/lifetime quantities such as host data written, power cycles, unsafe shutdowns, media/data-integrity errors, and lifetime error-information entries, while `Percentage Used` remains a vendor-specific life estimate and may exceed 100.

Thus `SMART / Health` is not one uniform kind of memory. It mixes at least:

```text
current condition / warning state
        !=
retained cumulative usage/error history
        !=
model-derived endurance estimate
```

### Intel DC P3700: a named 2014 product witness

Intel's July 2014 `Intel Solid-State Drive DC P3700 Series Product Specification`, order number 330566-002US, states that the P3700 supports the mandatory SMART / Health Information log defined by NVMe 1.0. Its table exposes `Available Spare`, a 10% spare threshold, `Percentage Used Estimate`, and the host data-unit counters. The product document repeats the important boundary that `100` means estimated endurance consumed but may not mean device failure.

The same P3700 product specification also says that a small portion of physical capacity is used for NAND media management and maintenance while the user-addressable LBA count remains stable for the life of the drive. That is product-level evidence that visible logical capacity and hidden maintenance capacity are not the same relation.

The surviving copy used here is an Intel-authored document preserved through manual/document mirrors rather than a current Intel-hosted PDF. The document identity, order number, July 2014 revision, and page transcript are preserved in the grounding record; this provenance is not silently upgraded to a current-vendor URL.

## Retained states and their different meanings

### 1. User payload

Application data addressed through namespaces/LBAs.

### 2. Cumulative host-usage counters

`Data Units Written`, command counts, power cycles, power-on hours, unsafe shutdowns, and related quantities retain summaries of past interaction with the controller.

They are **history-bearing state**, but not a complete event log.

### 3. Error-history counters

The media/data-integrity error count records controller-detected **unrecovered** integrity errors. The lifetime count of Error Information log entries is another retained historical quantity.

Neither is a complete record of every raw cell error or every successful ECC correction.

### 4. Endurance estimate

`Percentage Used` is not defined as a direct physical sensor reading. The standard calls it vendor specific and bases it on actual usage plus the manufacturer's prediction of life.

It is therefore retained/derived **model state about future margin**.

### 5. Spare-capacity state

`Available Spare` represents remaining spare capacity and can be compared with a threshold that can trigger host notification.

This is reserve/maintenance state, not filesystem free space and not application payload.

### 6. Current warning state

By NVMe 1.3, `Critical Warning` is explicitly current and nonpersistent. A device can therefore expose a present warning that differs categorically from its cumulative counters and endurance estimate even though they share one log page.

## Engineering reconstruction

### The device can retain evidence about its own retention margin

An SSD does not only retain user data. It may also preserve across power cycles enough controller state to report how much work it has seen, how many unsafe power losses occurred, how many unrecovered media/data-integrity errors were detected, how much spare capacity remains, and an estimated fraction of endurance consumed.

Therefore:

> **retained device-health state ≠ retained user payload**.

Yet the distinction does not make health state unimportant. A future administrator, controller, or monitoring system can use it to decide whether a device should remain in service, be replaced, or be investigated.

### `Percentage Used` is an estimate, not a countdown to a deterministic death instant

The specification itself blocks a tempting shortcut: `100` means estimated endurance consumed but may not indicate failure, and the value may exceed 100.

Therefore:

> **100% Percentage Used ≠ device failure**.

and:

> **vendor-specific endurance estimate ≠ direct measurement of every cell's remaining life**.

The field compresses device history and a manufacturer model into an operationally useful scalar. That compression is precisely why it is useful, and precisely why it must not be treated as a complete physical history.

### Host writes are not the physical NAND write history

`Data Units Written` is defined at the host/controller interface: data the host wrote to the controller, excluding metadata. The field is not specified as a count of NAND page programs, block erases, garbage-collection copies, mapping writes, ECC metadata writes, or other internal controller traffic.

Therefore:

> **host Data Units Written ≠ physical NAND program/erase work**.

This matters when comparing the host-visible usage history with the wear mechanisms in Cases 36 and 52. A host counter can be a useful workload witness without being the substrate's complete stress ledger.

### Spare capacity is maintenance reserve, not ordinary free user space

The NVMe `Available Spare` field refers to remaining spare capacity. Intel's P3700 separately documents physical capacity reserved for NAND management/maintenance while keeping the logical LBA count stable.

The bounded reconstruction is:

> **spare/maintenance reserve ≠ user-addressable free capacity**.

The P3700 document does not establish that every hidden management byte is counted directly by NVMe `Available Spare`; this case deliberately keeps those quantities distinct.

### Warning state and history state can share an interface without sharing persistence semantics

NVMe 1.3 explicitly says `Critical Warning` bits are current and nonpersistent while the SMART/Health interface also exposes lifetime/cumulative state.

Therefore:

> **current warning state ≠ retained cumulative health history**.

This is a useful counterexample to any assumption that one log page has one temporal ontology.

### A retained counter does not imply a complete archive

`Data Units Written`, unsafe-shutdown count, power-on hours, and error counts summarize categories. They do not preserve order, timing of every event, causal links among events, per-LBA history, or raw internal-media observations.

Therefore:

> **retained lifetime counter ≠ complete device history**.

This is a controller-scale version of the repository's broader `state retention ≠ history retention` distinction, with an important twist: here some **history is intentionally retained**, but only in lossy aggregate form.

### Telemetry cadence and maintenance cadence are separate

NVMe specifies that `Percentage Used` is updated once per power-on hour under the stated condition. That does not mean NAND refresh, garbage collection, wear leveling, bad-block replacement, scrub, read reclaim, or host replacement decisions all run hourly.

Therefore:

> **telemetry update cadence ≠ media-maintenance cadence**.

The field records/updates a model output; it does not itself perform the physical retention work.

## Relation to existing cases

### Case 36 — NAND correct-and-refresh

Case 36 concerns physical error accumulation, ECC margin, and rewrite/refresh policy. Case 55 concerns host-visible retained evidence about overall device use/health. A health estimate may influence operational policy, but it is not the same thing as restoring charge distributions or correction margin.

### Case 38 — Intel PLI self-test validation

Case 38 studies a product-specific capacitor-readiness/self-test path and SMART/event state for power-loss protection. Case 55 is broader and more standardized: generic NVMe health/endurance history. Therefore:

> **generic NVMe SMART/Health telemetry ≠ product-specific PLI readiness validation**.

### Case 52 — NAND read disturb

Case 52 shows that reads can consume physical margin. Case 55's `Data Units Written` field cannot be used as a universal physical-wear ledger, and a write counter in particular does not encode read-hotness/read-disturb history.

### Cases 44 and 47 — sanitization

A drive can report health telemetry while separate erase/sanitize semantics determine whether prior user data remains recoverable. Good health does not prove sanitization; sanitization does not reset the conceptual distinction between payload and health history.

### Cases 48 and 54 — second-order maintenance state

Cassandra `repairedAt` and DDR5 RAA-like state already show non-payload state governing future maintenance. NVMe health telemetry adds a different regime: cumulative/estimated **device aging evidence** that can qualify future service without itself being the payload being preserved.

These are functional comparisons only, not shared genealogy or protocol semantics.

## Failure and forgetting boundaries

Several forms of failure remain distinct:

- user data may be fully readable while `Percentage Used` reaches or exceeds 100;
- spare reserve may fall below threshold before immediate payload loss;
- media/data-integrity errors count only unrecovered events defined by the interface, not every corrected raw error;
- a current `Critical Warning` may clear while cumulative lifetime counters remain;
- a controller can retain aggregated history while forgetting the sequence of events that produced the aggregate;
- the health log itself can be unavailable if the controller cannot operate, even though some NAND embodiments physically survive;
- a healthy-looking interface report does not independently verify hidden physical wear distribution or future failure time.

The repository should therefore reject `SMART says healthy` as a synonym for `all retained payload is safe indefinitely`.

## Prior art and anti-anachronism

NVMe 1.0 was ratified in 2011, and the official 1.0e specification already contains the SMART/Health fields central to this case. Intel's 2014 P3700 product specification explicitly implements the NVMe 1.0 mandatory SMART/Health log.

Accordingly:

> **NVMe 1.3 clarification ≠ invention of NVMe endurance telemetry**.

The bounded value of comparing 1.0e and 1.3 is semantic, not priority-seeking: 1.3 makes the persistence boundary of `Critical Warning` explicit while preserving cumulative and estimated health fields.

This case does not attempt a full ATA SMART genealogy or claim that NVMe invented drive-health monitoring. That history belongs in a separate bounded standards/genealogy slice if needed.

## Philosophical interpretation — bounded

This case permits one narrow formulation:

> A technical object can preserve not only a payload but also a compressed account of the conditions under which that payload-bearing object has been used up.

The interesting point is not anthropomorphic `the SSD remembers its age`. Technically, the device retains counters, reserve state, and a model-derived estimate that make past use relevant to future decisions. Some of this history is durable across power cycles; some nearby warning state is explicitly current and nonpersistent.

The case therefore sharpens a distinction between **retaining the thing** and **retaining evidence about the remaining conditions of retention**.

That is a project-level interpretation. It is not terminology attributed to NVM Express or Intel.

## Claim ledger

| Claim | Label | Status |
| --- | --- | --- |
| NVMe 1.0e SMART/Health information is described as lifetime information retained across power cycles | `H/P` | strong, official specification |
| NVMe 1.0e defines Available Spare, Percentage Used, host data-unit counters, power/unsafe-shutdown counters, and media-error history | `H/P` | strong, official specification |
| `Percentage Used = 100` may occur without device failure | `H/P` | explicit normative wording |
| `Data Units Written` is host/controller-interface traffic rather than a normative count of internal NAND programs/erases | `H/P/E` | strong bounded reconstruction from field definition |
| NVMe 1.3 explicitly marks Critical Warning bits as current and nonpersistent | `H/P` | strong, official specification |
| Intel DC P3700 2014 implements the mandatory NVMe 1.0 SMART/Health log and exposes the relevant endurance fields | `H/P` | named product document, mirror provenance retained |
| health/endurance state can be retention infrastructure without being payload | `E` | bounded case reconstruction |
| a SMART percentage proves exact remaining lifetime for every physical NAND cell | `X` | rejected by vendor-specific-estimate wording |
| NVMe 1.3 invented SSD health/endurance telemetry | `X` | contradicted by NVMe 1.0e and 2014 P3700 evidence |
| NVMe health telemetry is historically/technically identical to Cassandra repair state or DDR5 RAA | `X` | rejected; functional analogy only |

## Sources

1. NVM Express, **NVM Express 1.0e**, official specification PDF, especially §5.10.1.2 and Figure 60, printed pp. 67–69: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_0e.pdf>
2. NVM Express, **NVM Express Revision 1.3**, official specification PDF, especially §5.14.1.2 and Figure 93, printed pp. 98–100: <https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf>
3. NVM Express, **Specification Archives**, historical revision index: <https://nvmexpress.org/nvm-express-specification-archives/>
4. Intel, **Intel Solid-State Drive DC P3700 Series Product Specification**, Order Number 330566-002US, July 2014; surviving transcript/mirror used for product-specific tables: <https://manualzilla.com/doc/7195133/intel-dcp3700-1.6tb>
5. NVM Express, **Features for Error Reporting, SMART, Log Pages, Failures and management capabilities in NVMe Architectures**, later institutional explanation used only as operational corroboration, not historical priority evidence: <https://nvmexpress.org/resource/features-for-error-reporting-smart-log-pages-failures-and-management-capabilities-in-nvme-architectures/>

## Related repositories

A repository search found no dedicated NVMe SMART/endurance case in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). Broader SSD/NAND engineering chronology should remain there if developed; this case keeps only the retention-specific interface/history distinction.
'''

evidence_text = r'''# NVMe SMART / Health endurance telemetry grounding record

Companion to [`../cases/55-nvme-smart-health-endurance-telemetry.md`](../cases/55-nvme-smart-health-endurance-telemetry.md).

**Canonical maturity status is tracked in [`../CASE_INDEX.md`](../CASE_INDEX.md).**

## Grounding question

Can the project establish, from primary interface documentation and a named product witness, that an SSD retains non-payload history/health state across power cycles, while keeping cumulative history, current warning state, host workload counters, spare reserve, and model-derived endurance estimates technically distinct?

The answer is yes for the bounded NVMe 1.0e–1.3 record.

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
'''

CASE.write_text(case_text, encoding="utf-8")
EVIDENCE.write_text(evidence_text, encoding="utf-8")

# README navigation
p = Path("README.md")
readme = p.read_text(encoding="utf-8")
readme_case = "- [`cases/55-nvme-smart-health-endurance-telemetry.md`](cases/55-nvme-smart-health-endurance-telemetry.md) — grounded NVMe SMART/Health endurance-telemetry case: retained lifetime counters, spare-capacity state, host workload counters, model-derived `Percentage Used`, and current nonpersistent warning state remain distinct; Intel's 2014 P3700 supplies a named-product witness without turning host-visible telemetry into a complete physical wear history."
if "cases/55-nvme-smart-health-endurance-telemetry.md" not in readme:
    readme = insert_after_line(readme, "cases/54-ddr5-rfm-split-maintenance-authority.md", readme_case, label="README case navigation")
readme_evidence = "- [`evidence/55-nvme10-13-smart-health-endurance-grounding.md`](evidence/55-nvme10-13-smart-health-endurance-grounding.md) — Case-55 grounding record: official NVMe 1.0e/1.3 SMART/Health sections establish cross-power-cycle health history, vendor-specific endurance estimation, host-interface counters, and the 1.3 current/nonpersistent Critical Warning boundary; Intel 330566-002US supplies a bounded 2014 implementation witness with mirror provenance retained."
if "evidence/55-nvme10-13-smart-health-endurance-grounding.md" not in readme:
    readme = insert_after_line(readme, "evidence/54-ddr5-rfm-2022-2025-grounding.md", readme_evidence, label="README evidence navigation")
p.write_text(readme, encoding="utf-8")

# ROADMAP SSD/controller bridge
p = Path("ROADMAP.md")
roadmap = p.read_text(encoding="utf-8")
roadmap = replace_once(
    roadmap,
    "partially advanced by grounded Cases 15, 20, 30, 31, 32, 36, 37, 38, 39, 44, 47, and 52",
    "partially advanced by grounded Cases 15, 20, 30, 31, 32, 36, 37, 38, 39, 44, 47, 52, and 55",
    label="ROADMAP SSD case list",
)
lines = roadmap.splitlines()
ssd_idxs = [i for i, line in enumerate(lines) if "SSD FTL/controller-mediated persistence beyond the bounded Ban/1990s case" in line]
if len(ssd_idxs) != 1:
    raise SystemExit(f"ROADMAP SSD bridge: expected one line, found {len(ssd_idxs)}")
i = ssd_idxs[0]
if "cases/55-nvme-smart-health-endurance-telemetry.md" not in lines[i]:
    anchor = " The broad item stays unchecked because"
    if anchor not in lines[i]:
        raise SystemExit("ROADMAP SSD bridge broad-item anchor missing")
    addition = (
        " [`cases/55-nvme-smart-health-endurance-telemetry.md`](cases/55-nvme-smart-health-endurance-telemetry.md), "
        "grounded by [`evidence/55-nvme10-13-smart-health-endurance-grounding.md`](evidence/55-nvme10-13-smart-health-endurance-grounding.md), "
        "adds a controller-history/health regime: NVMe 1.0e already exposes lifetime SMART information retained across power cycles, including spare state, host traffic, unsafe-shutdown/error counts, and a vendor-specific endurance estimate; NVMe 1.3 makes the neighboring Critical Warning bits explicitly current/nonpersistent, while a 2014 Intel P3700 product document supplies a named implementation witness. This separates payload retention, cumulative health history, model-derived remaining-margin state, current warning state, host workload, and hidden physical NAND wear."
    )
    lines[i] = lines[i].replace(anchor, addition + anchor, 1)
roadmap = "\n".join(lines) + ("\n" if roadmap.endswith("\n") else "")
p.write_text(roadmap, encoding="utf-8")

# CASE_INDEX: case row, comparison row, counts, findings
p = Path("CASE_INDEX.md")
idx = p.read_text(encoding="utf-8")
lines = idx.splitlines()
case_row = "| [NVM Express SMART / Health Endurance Telemetry: Retained Device History Without Payload History](cases/55-nvme-smart-health-endurance-telemetry.md) | **grounded** | user payload + cross-power-cycle cumulative SMART counters + spare-capacity state + vendor-specific endurance estimate + current/nonpersistent warning bits | separate payload retention from retained health history; host workload from physical NAND work; reserve from user free space; current warnings from cumulative counters; estimate from deterministic failure time | [NVMe 1.0e–1.3 SMART/Health grounding](evidence/55-nvme10-13-smart-health-endurance-grounding.md); ATA SMART genealogy, JESD218 methodology, independent named-device calibration, modern telemetry/endurance-group evolution, and fleet policy remain separate work |"
if not any("cases/55-nvme-smart-health-endurance-telemetry.md" in line for line in lines):
    anchors = [i for i, line in enumerate(lines) if "cases/54-ddr5-rfm-split-maintenance-authority.md" in line and line.startswith("|")]
    if len(anchors) != 1:
        raise SystemExit(f"CASE_INDEX case row: expected one Case-54 row, found {len(anchors)}")
    lines.insert(anchors[0] + 1, case_row)

matrix_row = "| NVMe SMART/Health endurance telemetry / 1.0e–1.3 + 2014 P3700 witness | payload + retained cumulative usage/error counters + spare reserve + vendor-specific endurance estimate + current warning state | controller accumulates selected lifetime summaries across power cycles and derives/updates health state; host may observe thresholds/warnings and decide service/replacement policy | ordinary I/O may remain successful even when estimated endurance reaches/exceeds 100; unrecovered-error counters do not enumerate all corrected raw errors | namespace/LBA access remains separate from global/per-controller health-log addressing; telemetry summarizes the device rather than locating one payload embodiment | logical capacity can remain stable while hidden maintenance reserve is consumed; health state may change without moving the logical object | intentionally lossy aggregate history: counters/estimate survive while event order, per-cell wear distribution, and complete internal-media history are not exposed |"
if not any(line.startswith("| NVMe SMART/Health endurance telemetry /") for line in lines):
    anchors = [i for i, line in enumerate(lines) if line.startswith("| DDR5 RFM / 2022–2025 bounded regime |")]
    if len(anchors) != 1:
        raise SystemExit(f"CASE_INDEX matrix row: expected one Case-54 matrix row, found {len(anchors)}")
    lines.insert(anchors[0] + 1, matrix_row)

idx = "\n".join(lines) + ("\n" if idx.endswith("\n") else "")
idx = replace_once(
    idx,
    "After fifty-five bounded cases, **all fifty-five cases are now `grounded`.**",
    "After fifty-six bounded cases, **all fifty-six cases are now `grounded`.**",
    label="CASE_INDEX case count",
)
idx = replace_once(idx, "currently fifty-five;", "currently fifty-six;", label="CASE_INDEX synthesis count")

if "559. **retained device-health state ≠ retained user payload**" not in idx:
    lines = idx.splitlines()
    anchors = [i for i, line in enumerate(lines) if line.startswith("558. **DDR5 RFM evolution ≠ origin of RowHammer-aware targeted refresh**")]
    if len(anchors) != 1:
        raise SystemExit(f"CASE_INDEX finding anchor: expected 558 once, found {len(anchors)}")
    new_findings = [
        "559. **retained device-health state ≠ retained user payload** — NVMe 1.0e explicitly defines SMART/Health information over the life of the controller and retained across power cycles, so an SSD can preserve non-payload state about its own use/condition;",
        "560. **retained lifetime counter ≠ complete device history** — host data, power-cycle/hour, unsafe-shutdown, and error counters preserve category totals without retaining event order, per-LBA sequence, causality, or the controller's complete internal media history;",
        "561. **vendor-specific endurance estimate ≠ direct measurement of every cell's remaining life** — `Percentage Used` is normatively an estimate based on actual usage plus the manufacturer's prediction of NVM life, not a disclosed per-cell physical-wear census;",
        "562. **100% Percentage Used ≠ device failure** — NVMe 1.0e and 1.3 explicitly allow the estimate to reach/exceed 100 while warning that 100 may not indicate device/subsystem failure;",
        "563. **host Data Units Written ≠ physical NAND program/erase work** — the standardized counter measures data the host wrote to the controller and excludes metadata; it is not normatively a count of internal page programs, block erases, GC copies, mapping writes, or write amplification;",
        "564. **Available Spare ≠ user-addressable free capacity** — the field describes remaining spare capacity for the device, while user-visible namespace/filesystem free space is a different address/capacity relation;",
        "565. **spare-threshold crossing ≠ immediate payload loss** — the threshold can produce a health/asynchronous notification before the interface asserts that current user data has become unreadable; warning margin and present payload availability remain distinct;",
        "566. **current Critical Warning state ≠ retained cumulative health history** — NVMe 1.3 explicitly says Critical Warning bits describe the current associated state and are nonpersistent even though the surrounding SMART/Health interface contains cumulative/lifetime information;",
        "567. **one SMART/Health log page ≠ one temporal regime** — current warning bits, retained counters, reserve state, instantaneous/composite temperature, and a model-derived endurance estimate coexist in one structure without sharing the same persistence semantics;",
        "568. **unrecovered media/data-integrity error count ≠ all ECC/correction work** — the NVMe field counts controller-detected unrecovered integrity errors, so successful correction or raw-error activity cannot be inferred from that counter alone;",
        "569. **telemetry update cadence ≠ media-maintenance cadence** — `Percentage Used` has a specified update interval, but that cadence is not the schedule for NAND refresh, garbage collection, wear leveling, read reclaim, bad-block replacement, or host retirement;",
        "570. **stable logical capacity ≠ absence of hidden maintenance capacity** — Intel's 2014 P3700 document keeps user LBA count stable while separately reserving some physical capacity for NAND management/maintenance; the logical namespace need not visibly shrink as reserve is consumed;",
        "571. **hidden maintenance capacity ≠ automatically identical to NVMe Available Spare** — the P3700 capacity note proves non-user management reserve exists, but the bounded sources do not establish a byte-for-byte identity between every hidden physical reserve and the standardized Available Spare percentage;",
        "572. **health telemetry can qualify future service without itself preserving the payload** — cumulative errors, remaining spare, and endurance estimates can guide investigation/replacement while the physical retention/refresh/remapping mechanisms remain separate layers;",
        "573. **generic NVMe SMART/Health telemetry ≠ product-specific PLI readiness validation** — Case 38's Intel capacitor self-test/event semantics are a distinct health relation; a generic standardized endurance log does not prove a particular backup-power subsystem has been self-tested or is ready;",
        "574. **NVMe 1.3 clarification ≠ invention of NVMe endurance telemetry** — official 1.0e already contains the core SMART/Health endurance fields and Intel's 2014 P3700 implements the mandatory NVMe 1.0 log, so 1.3 is used here for a persistence-boundary clarification rather than an origin claim."
    ]
    lines[anchors[0] + 1:anchors[0] + 1] = new_findings
    idx = "\n".join(lines) + "\n"

p.write_text(idx, encoding="utf-8")

# Assertions
readme = Path("README.md").read_text(encoding="utf-8")
roadmap = Path("ROADMAP.md").read_text(encoding="utf-8")
idx = Path("CASE_INDEX.md").read_text(encoding="utf-8")
assert CASE.exists() and EVIDENCE.exists()
assert readme.count("cases/55-nvme-smart-health-endurance-telemetry.md") == 2
assert readme.count("evidence/55-nvme10-13-smart-health-endurance-grounding.md") == 2
assert "Cases 15, 20, 30, 31, 32, 36, 37, 38, 39, 44, 47, 52, and 55" in roadmap
assert roadmap.count("cases/55-nvme-smart-health-endurance-telemetry.md") == 2
assert idx.count("cases/55-nvme-smart-health-endurance-telemetry.md") == 1
assert idx.count("| NVMe SMART/Health endurance telemetry / 1.0e–1.3 + 2014 P3700 witness |") == 1
assert "After fifty-six bounded cases, **all fifty-six cases are now `grounded`.**" in idx
assert "currently fifty-six;" in idx
assert "After fifty-five bounded cases" not in idx
assert "currently fifty-five;" not in idx
for n in range(559, 575):
    assert idx.count(f"{n}. **") == 1, n
print("Case 55 research/navigation/status integration validated")
