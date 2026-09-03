# NVM Express SMART / Health Endurance Telemetry: Retained Device History Without Payload History

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
