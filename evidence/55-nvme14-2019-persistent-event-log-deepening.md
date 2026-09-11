# Case 55 deepening evidence — NVMe 1.4 Persistent Event Log and selected device history (2019)

## Status

**`grounded`** for a bounded interface-history deepening of Case 55. The official **NVM Express Base Specification Revision 1.4, 10 June 2019** directly defines the optional **Persistent Event Log (PEL)**, while NVM Express's own Revision-1.4 change ledger identifies PEL as a new feature in that revision.

This record establishes a narrow transition from retained health counters and bounded diagnostic logs to a standardized heterogeneous event-history interface. It does **not** establish the invention of persistent device history, a direct ATA→NVMe genealogy, a particular SSD-controller implementation, or independent proof that a recorded sanitize completion physically erased every prior embodiment.

## Research question

Case 55 already separates current warning state, cumulative/lifetime counters, model-derived endurance estimates, and the bounded 1999 ATA/ATAPI-5 SMART self-test log. This pass asks:

> What changes when NVMe itself standardizes a persistent log of selected significant events rather than only present condition and cumulative summaries?

The answer is not simply `the device now has history`. The interface also exposes rules for **selection, suppression, deletion, retrieval consistency, reset/power-cycle persistence, and sanitization-driven modification of that history**.

## Sources and provenance

### Primary normative source

NVM Express, **NVM Express Base Specification, Revision 1.4**, 10 June 2019, especially §5.14.1.13 and §5.14.1.13.1:

<https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf>

The directly inspected text establishes:

- PEL as Log Identifier `0Dh`;
- retention across power cycles and resets;
- subsystem-global scope;
- the weaker recommendation that implementations be designed for minimal event-information loss on power failure;
- vendor-specific event-count and maximum-size bounds;
- suppression of repeated same-type events above a vendor-specific frequency threshold;
- vendor-specific deletion policy when log limits are reached;
- a persistent-event-log reporting context for retrieval;
- logging of new events while an established reporting context continues to report the older selected view;
- event types including SMART/Health snapshots, firmware commits, timestamp changes, power-on/reset, hardware errors, namespace changes, Format/Sanitize start and completion, feature changes, telemetry-log creation, thermal excursions, and vendor/TCG events;
- a SMART/Health snapshot event at least once every 24 power-on hours for the controller scope specified by the standard when PEL is supported;
- permission for sanitize to remove or modify PEL events to prevent derivation of user data, with removed events left unspecified.

### First-party revision-history source

NVM Express, **Changes in NVMe Revision 1.4**:

<https://nvmexpress.org/changes-in-nvme-revision-1-4/>

This first-party change ledger labels Persistent Event Log a **new optional feature** in Revision 1.4 and lists the standardized event categories. It references Technical Proposals `4007a` and `4042a`, but those proposals are **not independently inspected in this pass**. The page therefore supports the bounded revision boundary `PEL is new in NVMe 1.4`, not proposal-level drafting chronology, priority, or invention claims.

### Earlier prior-art floor already grounded in Case 55

Case 55 already uses **ATA/ATAPI-5 Revision 2, 13 December 1999** to ground a 21-entry circular SMART self-test log carrying test result, power-on-life timestamp, failure checkpoint, and sometimes a failing LBA. That earlier interface is enough to reject `NVMe 1.4 PEL = invention of drive-retained diagnostic history`. The ATA log and NVMe PEL have different schemas, scopes, event vocabularies, capacities, and control semantics; no direct ATA→NVMe design genealogy is asserted.

## Historical record

### Revision 1.4 adds an optional persistent-event-history interface

Revision 1.4 is dated **10 June 2019**. NVM Express's own change ledger identifies PEL as a new optional Revision-1.4 feature. Normative §5.14.1.13 describes a log of significant events not tied to one particular command and requires its information to be retained across **power cycles and resets**. The log is global to the NVM subsystem.

This is materially different from treating one error bit or lifetime counter as the whole historical interface. A PEL entry may retain a typed event with event-specific data and timestamp while the log has its own reporting-context metadata.

### Reset/power-cycle persistence is not a lossless abrupt-power-failure guarantee

The standard requires PEL information to be retained across power cycles and resets, but its immediately following power-failure language is weaker: NVM subsystems **should** be designed for minimal loss of event information upon power failure. Modal force matters. The inspected contract therefore supports `retained across power cycle/reset` but not `every event is guaranteed to survive every abrupt power failure`.

### The standardized history is explicitly bounded and selective

The number of events and maximum PEL size are vendor-specific. The standard recommends sizing them so ordinary usable life should not exhaust them, but it also specifies behavior when limits are reached. Repeated same events may be suppressed above a vendor-specific frequency threshold. When size/count/category limits are reached, deletion policy is vendor-specific; the text even allows an older important event to be retained while a newer event is deleted.

Thus chronological recency is not the only retention authority. Importance/category/frequency policy can shape which traces survive.

### PEL retains heterogeneous episodes rather than one scalar

Revision 1.4 defines event types spanning SMART/Health snapshots, firmware commit, timestamp change, power-on/reset, subsystem hardware error, namespace change, Format NVM start/completion, Sanitize start/completion, Set Features, telemetry-log creation, thermal excursion, and vendor/TCG events. The distinction between start and completion is especially important: `operation started != operation completed`. A trace that an operation began is not itself a completion certificate.

### SMART/Health gains periodic historical snapshots

For an NVM subsystem supporting PEL, Revision 1.4 requires a SMART/Health Log Snapshot Event at least once every **24 power-on hours** for the controller/primary-controller scope specified by the virtualization rules. The payload is a snapshot of SMART/Health Information Log data.

The same health interface can therefore participate in two temporal forms: current/cumulative SMART/Health fields and retained timestamped SMART/Health snapshots. Those snapshots still do not become raw NAND error history, complete FTL history, or an independent physical-wear measurement.

### Reporting context stabilizes the retrieval view while logging continues

The host can establish a **persistent event log reporting context**, read data associated with it, and release it. Events occurring while the context exists are still logged but are **not reported in that existing context**. The interface therefore distinguishes the continuing underlying event stream from the bounded historical view being read.

### Sanitization may intentionally modify retained history

Revision 1.4 explicitly permits sanitize to alter PEL data, including removing or modifying events to prevent derivation of user data. Which events are removed is unspecified. Persistent diagnostic history is therefore not automatically immutable simply because it persists across reset/power-cycle boundaries.

At the same time, `PEL records Sanitize Completion != independently verified media sanitization`. An event record documents an interface-visible episode/result; it does not independently inspect every stale embodiment or prove laboratory unrecoverability.

## Engineering reconstruction

The following are project reconstructions from the documented interface, not historical NVMe vocabulary.

### Persistent history is not complete history

```text
event occurs
    -> event type supported?
    -> repetition/suppression policy
    -> event admitted to retained log
    -> finite size/category bounds
    -> vendor deletion policy
    -> later reportable trace
```

Therefore **`persistent event history != complete event history`**. PEL preserves more event structure than a scalar counter but remains a selected operational history.

### Persistence contract and failure-time materialization are separate

The `shall retain across power cycles/resets` and `should minimize loss upon power failure` statements should not be collapsed. Therefore **`power-cycle/reset persistence != guaranteed lossless abrupt-power-failure capture`**.

### Reporting context is a stable read view, not a frozen log

Because newer events continue to be logged while an existing reporting context excludes them, **`reporting context != frozen underlying log`**. This is a bounded read-consistency reconstruction, not a claim that PEL is database MVCC or snapshot isolation.

### Event-retention policy can privilege significance over recency

Vendor-specific deletion can preserve an older important event while deleting a newer one. Therefore **`newer event != automatically stronger retention priority`**.

### Historical SMART snapshots remain interface/model history

A periodic SMART/Health snapshot retains the standardized health abstraction at a point in device power-on life. It does not expose every ECC correction, FTL move, NAND program/erase, garbage-collection copy, read-reclaim decision, or per-cell threshold state. Therefore **`historical SMART snapshot != complete physical-media history`** and **`snapshot cadence != media-maintenance cadence`**.

### Persistent history can itself be subject to forgetting policy

Sanitize may modify/delete PEL records where the retained history itself could expose user data. Thus **`persistent != immutable`** and **`retention policy != unconditional preservation`**.

## Functional comparisons and stop conditions

The 1999 ATA/ATAPI-5 self-test log is earlier evidence that a drive can retain bounded diagnostic history. PEL is a later standardized heterogeneous event log. The comparison is functional only: both preserve selected evidence about device operation beyond the immediate operation. It does **not** prove direct ATA→NVMe genealogy.

Case 15's unsafe-shutdown telemetry provides another bounded comparison: a cumulative count and a typed event trace are different compressed histories of power-transition episodes. PEL does not reveal the controller's emergency-flush implementation or prove that user payload survived an unsafe shutdown.

Cases 44/47 remain the sanitization stop condition. PEL makes the interaction visible because sanitize may change diagnostic history, but a sanitize-completion event is not independent verification that every stale physical embodiment is unrecoverable.

## Philosophical interpretation — bounded

Project-level interpretation only:

> Retaining history is itself an act of selection. A technical object may preserve traces of its past while suppressing repetition, discarding some newer events in favor of older important ones, and later allowing a sanitization policy to erase or transform parts of the historical record.

The point is not that an SSD `remembers like a person`. It is that history retention has its own **admission, persistence, read-consistency, capacity, priority, and forgetting rules**. This interpretation remains downstream of the interface evidence.

## Claim ledger

| Claim | Label | Status |
| --- | --- | --- |
| Revision 1.4 is dated 10 June 2019 and the first-party change ledger identifies PEL as a new optional feature in that revision | `H/P` | strong revision/spec boundary; not invention proof |
| PEL is retained across power cycles/resets and is subsystem-global | `H/P` | explicit normative semantics |
| the same clause only recommends minimal event-information loss on power failure | `H/P` | explicit modal distinction |
| PEL event count/size are vendor-specific and repeated same events may be suppressed | `H/P` | explicit normative semantics |
| deletion under log/category pressure is vendor-specific and may preserve older important events | `H/P` | explicit normative semantics |
| `persistent event history != complete event history` | `E` | bounded reconstruction |
| PEL defines heterogeneous event types including separate Format/Sanitize start and completion events | `H/P` | explicit event table |
| PEL-supported subsystems create SMART/Health snapshots at least once every 24 power-on hours under specified scope rules | `H/P` | explicit normative semantics |
| new events continue to be logged while an existing reporting context excludes them | `H/P/E` | explicit interface semantics + bounded reconstruction |
| sanitize may remove/modify PEL events to prevent user-data derivation | `H/P` | explicit normative semantics |
| ATA/ATAPI-5 1999 is earlier bounded prior art for retained diagnostic history | `H/P/A` | previously grounded; analogy only |
| PEL proves complete/lossless history, hidden NAND/FTL algorithm, direct ATA→NVMe genealogy, or verified physical sanitization | `X` | rejected |

## Open evidence debt

- inspect TP `4007a` and `4042a` directly before proposal-level chronology claims;
- identify named shipping NVMe 1.4 products with documented PEL behavior before product-adoption claims;
- independently test abrupt power failure, log-capacity pressure, suppression, reset, and sanitize behavior before compliance claims;
- do not infer the physical medium, update atomicity, wear-management strategy, or firmware journaling used to retain PEL state;
- broader storage-device logging genealogy belongs primarily in `tmzncty/computing-archaeology` if pursued.

## Sources

1. NVM Express, **NVM Express Base Specification, Revision 1.4**, 10 June 2019, especially §5.14.1.13 and §5.14.1.13.1: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf>
2. NVM Express, **Changes in NVMe Revision 1.4**, first-party revision summary: <https://nvmexpress.org/changes-in-nvme-revision-1-4/>
3. T13, **AT Attachment with Packet Interface - 5 (ATA/ATAPI-5), Working Draft T13/1321D Revision 2**, 13 December 1999, already grounded in Case 55; period draft mirror: <https://studylib.net/doc/25730948/ata-atapi-5>

## Related repositories

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated Persistent Event Log history. If proposal genealogy, product adoption, controller implementation, or broader drive-event-logging lineage is developed, it should primarily be built there and linked back here. This record keeps only the retention-specific distinctions.
