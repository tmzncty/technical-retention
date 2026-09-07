# Grounding Record — NVMe Persistent Event History and Log-Lifetime Contrast (2011–2019)

## Purpose

This record grounds [`../cases/66-nvme14-persistent-event-log-history.md`](../cases/66-nvme14-persistent-event-log-history.md).

The bounded claim is not that NVMe invented event logs. It is that **NVM Express Base Specification Revision 1.4 (10 June 2019) directly standardizes a persistent, subsystem-global significant-event history whose survival, capacity, suppression/deletion, sanitize interaction, and retrieval-context semantics are explicit enough to support a retention-specific case, while Revision 1.0 (2011) and Revision 1.3c (2018) establish earlier internal-NVMe floors for retained diagnostic state and mixed log lifetimes.**

## Source hierarchy

### A — primary normative source

NVM Express, Inc., **NVM Express Base Specification Revision 1.4**, dated 10 June 2019:

<https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf>

Directly inspected sections/pages:

- front matter, printed p. 1 — Revision 1.4 and date `June 10, 2019`;
- §5.14.1.13, printed pp. 138–140 — Persistent Event Log purpose, persistence, scope, capacity, suppression/deletion, reporting context;
- Figure 213 / §5.14.1.13.1, printed pp. 142–143 — standardized event types;
- §5.14.1.13.1.1, printed p. 143 — SMART/Health Log Snapshot event;
- §5.14.1.13.1.2 onward — firmware/reset/error and other event formats;
- §5.14.1.13.1.9–10, printed pp. 149–150 — Sanitize Start/Completion events;
- §5.14.1.13.1.11, printed pp. 150–151 — Set Feature event.

### B — period institutional corroboration

NVM Express, Inc., **“New NVM Express, Inc. Specifications Bolster Cloud and Enterprise Advancements,”** 2019:

<https://nvmexpress.org/new-nvm-express-inc-specifications-bolster-cloud-and-enterprise-advancements/>

This describes the NVMe 1.4 PEL feature as enabling robust drive history for issue triage and debugging at scale. It is used only for period framing, not to replace normative semantics.

## Verified normative facts

### 1. Cross-reset persistence

§5.14.1.13 says the PEL contains information about significant events not specific to a particular command and that its information **shall be retained across power cycles and resets**. It also says NVM subsystems should be designed for minimal event-information loss upon power failure.

Safe claim:

> PEL has an explicit cross-power/reset persistence contract.

Unsafe upgrade:

> No event can ever be lost on power failure or later policy reclamation.

The former is normative; the latter is contradicted by the weaker power-failure recommendation plus explicit suppression/deletion rules.

### 2. Subsystem scope

The specification says the PEL is global to the NVM subsystem.

Safe claim:

> PEL history is not merely one namespace's payload history.

For multi-controller events such as subsystem reset, the standard says the event should be logged once by a vendor-selected controller rather than once per controller.

### 3. Capacity, suppression, and deletion

The number of supported events is vendor specific. The maximum PEL size is exposed by `PELS`. Capacity should be large enough to avoid hitting the limit during usable life, but the standard still defines limit behavior.

A controller normally logs each supported event occurrence, except that it may suppress further entries when the same event exceeds a vendor-specific frequency threshold.

When size/count/category limits are reached, event deletion choice is vendor specific. The normative example explicitly permits an important older event to survive while newer entries are deleted.

Safe claims:

- persistence is bounded by capacity/policy;
- one event occurrence need not imply one surviving entry under frequency suppression;
- retention priority need not be recency-only.

Unsafe claim:

> PEL is a complete forensic command/event trace.

### 4. Sanitization can alter history

§5.14.1.13 says a sanitize operation may remove or modify PEL events to prevent derivation of user data from the log. Which events are removed is unspecified.

Safe claim:

> the standard allows deliberate history alteration as part of sanitize privacy/security behavior.

Unsafe claims:

- all PEL entries are erased by sanitize;
- no PEL entries are erased by sanitize;
- a particular event class is always preserved or removed.

None follows from Revision 1.4.

### 5. Reporting context creates one recoverable view

PEL Get Log Page defines actions to:

- establish a reporting context and read data;
- read from a preexisting reporting context;
- release the reporting context.

The internal representation is vendor specific. The controller should retain it until explicit release, subsystem/controller reset, or for a vendor-specific interval sufficient for retrieval.

Events occurring while the context exists are still logged, but **shall not be reported in the existing context**.

Safe reconstruction:

> stable retrieval view ≠ frozen underlying event history.

The controller retains a temporary second-order state that stabilizes which records a multi-command read means to recover.

### 6. Event types are heterogeneous historical records

Figure 213 includes SMART/Health snapshot, firmware commit, timestamp change, power/reset, hardware error, namespace change, format start/completion, sanitize start/completion, Set Feature, telemetry creation, thermal excursion, vendor-specific, and TCG-defined event types.

This supports a history-of-device-operation reading, but does not make all event types mandatory in all implementations. The figure's O/M notes and command-support conditions must be preserved.

### 7. SMART snapshot boundary

§5.14.1.13.1.1 requires relevant PEL-capable controllers to create a SMART/Health Log Snapshot event at least once every 24 power-on hours. The event data contains a snapshot of the SMART/Health Information Log.

This directly supports:

> SMART snapshot event ≠ live SMART state.

It also gives the exact boundary against Case 55: Case 55 studies cumulative/current/model-derived health state; Case 66 studies event history that can include historical copies of that state.

### 8. Set Feature event as retained configuration evidence

§5.14.1.13.1.11 says the Set Feature event persists data from a successful supported Set Features command and requires an event when the supported setting changed under the stated conditions.

Safe claim:

> a prior configuration change can remain recoverable as an event after command completion.

This is history evidence, not a substitute for the controller's current live feature state.

## Deepening — Error Information entries, retained Error Count, and PEL

### A — NVMe 1.0 historical floor (2011)

NVM Express Revision 1.0 was ratified **1 March 2011**. In §5.10.1.1, the Error Information entry defines a 64-bit incrementing `Error Count` and says it is retained across power-off conditions. In §5.10.1.2, SMART / Health information is described as information over the life of the controller and retained across power cycles.

Safe claim:

> NVMe retained diagnostic summary/ordinal state across power boundaries from Revision 1.0.

Unsafe upgrade:

> Revision 1.0 already provided the later NVMe 1.4 Persistent Event Log.

It did not. This is prior art inside NVMe for retained diagnostic state, not identity with PEL.

### A — NVMe 1.3c explicit mixed-lifetime error history (2018)

Revision 1.3c §5.14.1.1 makes the lifetime split explicit. Error Information is controller-global and returns a bounded recent-error population. If full, the controller should add the new entry and discard the oldest. The controller **should** remove all entries on power cycle and reset. The `Error Count` field is nevertheless specified as retained across power-off conditions.

The wording strength matters: `should clear` is a recommendation, not a `shall` requirement. The case therefore records the historical contract without upgrading recommendation to mandatory conformance.

Safe relations:

- detailed recent Error Information entries ≠ cross-power Error Count;
- recent-error population ≠ lifetime diagnostic summary;
- controller-global log scope ≠ later PEL subsystem-global scope.

### A — NVMe 1.4 preserves the contrast while adding PEL (2019)

Revision 1.4 §5.14.1.1 retains the same basic Error Information decomposition: controller-global recent entries, oldest-entry displacement under capacity pressure, recommended clearing on power cycle and Controller Level Reset, and a cross-power `Error Count`.

Revision 1.4 §5.14.1.13 then defines a separate PEL whose event information **shall** be retained across power cycles and resets and whose scope is the NVM subsystem.

This is a stronger retention-specific comparison than simply saying that PEL is persistent:

```text
error occurrence
    -> recent detailed Error Information entry
    -> Error Count / ordinal history that can cross power-off

significant device event
    -> PEL event entry
    -> subsystem-global cross-reset history
```

The two paths may refer to related faults, but the specification does not make them the same record population or the same lifetime contract.

### Engineering reconstruction boundary

A retained count/ordinal can survive after richer records have been discarded. It can establish that diagnostic history advanced, but it cannot reconstruct the lost queue ID, command ID, completion status, parameter-error location, LBA, namespace, or vendor-specific fields.

Therefore:

> **historical-summary persistence ≠ historical-detail persistence**.

and:

> **history lifetime is a property of a particular state relation, not of the word `log` in general**.

### Prior-art consequence for the 2019 PEL claim

The safe novelty boundary is now narrower than the first pass:

- 2011 NVMe already has retained error ordinal and lifetime SMART/Health state;
- 2018 NVMe 1.3c explicitly has mixed lifetimes inside one error-reporting path;
- 2019 NVMe 1.4 adds the inspected PEL composition: subsystem-global significant-event detail with explicit cross-reset persistence plus bounded suppression/deletion/sanitize/retrieval-context rules.

Chronology therefore blocks any claim that PEL introduced `retained device history` as such. The bounded contribution is the 2019 **event-detail persistence and retrieval-policy composition**, not first invention of diagnostic memory.

## In-repository prior-art boundary

### Case 55 — SMART / Health

[`../cases/55-nvme-smart-health-endurance-telemetry.md`](../cases/55-nvme-smart-health-endurance-telemetry.md) already establishes:

- lifetime/cumulative NVMe health state across power cycles;
- `Percentage Used` as vendor-specific estimate;
- host usage/error counters;
- current/nonpersistent Critical Warning in NVMe 1.3;
- aggregate retained history ≠ complete physical history.

Case 66 is not a rewrite. It adds an explicitly event-oriented history plus selection/retrieval semantics. The SMART snapshot event is the composition point, not evidence that the interfaces are identical.

### Cases 44 and 47 — sanitization

Those cases ask about user-data forgetting and implementation-level physical remnants. Case 66 uses sanitize only to establish that **history metadata itself may be modified for privacy/security**. It does not make a new empirical claim about raw NAND erasure.

## Related-repository duplication check

Current searches of `tmzncty/computing-archaeology` for `NVMe Persistent Event Log` and `NVMe Error Information SMART Health` returned no dedicated case. This record therefore keeps the retention-specific lifetime/scope analysis here while leaving general SSD/controller history and broader ATA/SCSI/NVMe diagnostic-log genealogy to that repository if pursued later.

## Prior-art / novelty boundary

Do **not** claim:

- NVMe invented event logs;
- NVMe invented black-box/device history;
- NVMe 1.4 invented SMART/health monitoring;
- PEL is the first storage-device diagnostic history;
- standardized PEL proves one physical on-media implementation.

The source-supported 2019 claim is narrower:

> NVMe 1.4 standardizes a host-visible, subsystem-global persistent event history with explicit cross-reset persistence, capacity/suppression/deletion semantics, sanitize interaction, and reporting-context behavior.

That composition is enough for a retention case; invention priority is unnecessary.

## What the source does not establish

Revision 1.4 does not by itself establish:

- the physical medium or controller metadata structure used to store PEL entries;
- exact power-failure atomicity for every event record;
- a universal minimum PEL capacity across vendors;
- a complete event list for every implementation;
- exact chronological/causal ordering beyond the standard's vendor-specific ordering language;
- named commercial SSD compliance;
- exact event removal under sanitize;
- secure physical erasure of user payload;
- ATA/SCSI/event-log genealogy before NVMe 1.4.

These remain separate research slices.

## Sources

1. NVM Express, Inc., **NVM Express Base Specification Revision 1.4**, 10 June 2019, §5.14.1.1 and §5.14.1.13–5.14.1.13.1.15: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf>
2. NVM Express, Inc., **NVM Express Revision 1.3c**, 24 May 2018, §5.14.1.1: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_3c-2018.05.24-Ratified.pdf>
3. NVM Express / NVMHCI Workgroup, **NVM Express Revision 1.0**, ratified 1 March 2011, §5.10.1.1–5.10.1.2: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_0-Gold.pdf>
4. NVM Express, Inc., **“New NVM Express, Inc. Specifications Bolster Cloud and Enterprise Advancements,”** 2019: <https://nvmexpress.org/new-nvm-express-inc-specifications-bolster-cloud-and-enterprise-advancements/>
