from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
CASE_PATH = "cases/66-nvme14-persistent-event-log-history.md"
EVIDENCE_PATH = "evidence/66-nvme14-2019-persistent-event-log-grounding.md"

case = r'''# NVM Express 1.4 Persistent Event Log: Retained Device History, Selective Forgetting, and Snapshot-Consistent Retrieval

## Status

**`grounded`** — bounded to the Persistent Event Log (`PEL`, Log Identifier `0Dh`) standardized in NVM Express Base Specification Revision 1.4, dated 10 June 2019. The case uses the ratified specification as the primary source and NVM Express's 2019 institutional description only as corroboration of intended operational use.

Grounding record: [`../evidence/66-nvme14-2019-persistent-event-log-grounding.md`](../evidence/66-nvme14-2019-persistent-event-log-grounding.md).

## Scope

This case asks a narrow question left outside Case 55:

> What changes when a storage controller standardizes a persistent **event history**, rather than only cumulative health counters or current warning state, and that history has explicit rules for persistence, suppression, deletion, sanitization, and consistent retrieval?

The bounded object is the NVMe 1.4 `Persistent Event Log`, especially:

- persistence across power cycles and resets;
- subsystem-global event identity;
- finite/vendor-specific event capacity;
- repeated-event suppression and full-log deletion policy;
- interaction with `Sanitize`;
- the temporary `persistent event log reporting context` used for multi-command retrieval;
- event classes including SMART/Health snapshots, firmware commits, timestamp changes, resets, hardware errors, namespace changes, format/sanitize operations, feature changes, telemetry creation, and thermal excursions.

This is **not**:

- a generic history of event logging, black-box recorders, audit logs, SMART, ATA, or SCSI;
- a claim that NVMe invented persistent device-event histories;
- evidence that every NVMe 1.4 SSD implements every optional event type or the same retention capacity;
- proof of a named commercial drive's PEL implementation or physical storage layout;
- a claim that PEL is a complete command trace, a complete NAND-wear history, or user payload history;
- a claim that PEL persistence is indefinite or immutable;
- a claim that `Sanitize` preserves or removes any particular event category beyond what the standard specifies;
- a substitute for Cases 44 and 47 on user-data sanitization semantics and empirical remanence.

## Historical record

### NVMe 1.4 defines a subsystem-global persistent event history

The ratified NVM Express Base Specification Revision 1.4 is dated **June 10, 2019**. Section 5.14.1.13 defines the `Persistent Event Log (Log Identifier 0Dh)` as information about significant events not specific to one command.

The normative text states that information in the PEL **shall be retained across power cycles and resets**, and recommends subsystem design for minimal loss of event information on power failure. It also makes the log **global to the NVM subsystem** rather than private to one ordinary namespace or one host-visible LBA range.

This yields the first bounded distinction:

> **persistent device-event history ≠ user payload**.

The controller can preserve facts about changes to, failures of, and maintenance actions on the device even though those facts are not application blocks.

### Capacity and history selection are explicitly bounded

NVMe 1.4 does not define the PEL as an unlimited archive. The number of supported events is vendor specific, and the maximum log size is reported through `PELS` in Identify Controller. The specification says capacity **should** be large enough not to reach the supported maximum during the usable life of the subsystem, but then defines behavior for cases where size, total event count, or category-specific count reaches a limit.

It also permits repeated-event suppression when one supported event occurs above a vendor-specific frequency threshold. If space must be reclaimed, the choice of events to delete is vendor specific; the specification explicitly allows an important older event to be retained while newer events are deleted.

Therefore:

> **retained event history ≠ complete device history**.

and:

> **newest event ≠ automatically highest retention priority**.

The retention policy is not reducible to append forever or simple FIFO aging.

### Sanitization may intentionally alter the retained history

Section 5.14.1.13 explicitly says a `Sanitize` operation may alter the PEL, including removing or modifying events to prevent derivation of user data from log-page information. Which events are removed is unspecified.

This blocks two opposite shortcuts:

> **sanitize completion ≠ immutable preservation of device-event history**.

and:

> **PEL alteration during sanitize ≠ evidence that all PEL entries are removed**.

The standard recognizes that diagnostic/history metadata can itself leak information about user activity, but does not impose one universal deletion set.

### Event types preserve heterogeneous past facts

NVMe 1.4 defines PEL event types including:

- `SMART / Health Log Snapshot`;
- `Firmware Commit`;
- `Timestamp Change`;
- `Power-on or Reset`;
- `NVM Subsystem Hardware Error`;
- `Change Namespace`;
- `Format NVM Start` / `Completion`;
- `Sanitize Start` / `Completion`;
- `Set Feature`;
- `Telemetry Log Created`;
- `Thermal Excursion`;
- vendor-specific and TCG-defined events.

The important retention fact is not that these are all equivalent. They are heterogeneous events placed into one standardized historical interface.

For example, the `Set Feature` event persists data from a successful supported `Set Features` command when the controller setting changes. A later operation can therefore recover evidence of a prior configuration change without replaying the original command stream.

### PEL can retain historical SMART snapshots without becoming SMART itself

Case 55 established that NVMe SMART/Health mixes cumulative lifetime counters, model-derived endurance estimates, spare state, and current/nonpersistent warning information.

NVMe 1.4 adds a different relation: a PEL-capable subsystem creates `SMART / Health Log Snapshot` events according to the conditions in §5.14.1.13.1.1, at least once every 24 power-on hours for the relevant controllers. Event data contains a snapshot of the SMART/Health Information Log.

Therefore:

> **SMART/Health snapshot event ≠ live SMART/Health state**.

and:

> **PEL event history ≠ SMART cumulative counters and estimates**.

A snapshot turns the state of another diagnostic interface at a past moment into one event-bearing historical record.

## Retained states and control state

The bounded regime contains several separable states:

1. **user payload** — namespace/LBA data, outside the PEL itself;
2. **persistent event entries** — historical records of supported significant events;
3. **event metadata** — event type/revision plus time/controller and event-specific information;
4. **capacity and retention policy** — supported size/count and vendor-specific suppression/deletion behavior;
5. **reporting context** — a temporary controller-created selection/view describing what one PEL retrieval should include;
6. **current controller/subsystem state** — the live state from which some later events may be generated;
7. **other diagnostic state** — SMART/Health and telemetry, which may be snapshotted or referenced but are not identical to PEL.

This composition matters because only some of these states share the same lifetime.

## Engineering reconstruction

### Persistence across reset does not imply indefinite retention

The normative requirement is strong but bounded: event information survives power cycles and resets. The same section also defines suppression, finite capacity, and event deletion.

Therefore:

> **persistence across power cycles/resets ≠ indefinite retention**.

This is a useful correction to a loose use of `persistent`. The word identifies a failure/transition boundary that the state crosses; it does not mean the state has no later reclamation policy.

### Usable-life sizing is a design objective, not an archival guarantee

The standard says PEL size/count **should** be large enough not to hit the maximum during the usable life of the NVM subsystem. This is not equivalent to a normative guarantee that every event will remain for the entire usable life, because the same section permits frequency suppression and defines deletion behavior for limit cases.

Thus:

> **usable-life sizing objective ≠ guarantee that every event survives usable life**.

The history can be durable while still being lossy by policy.

### Event occurrence is not identical to one retained record

Supported event occurrences are normally logged, but repeated high-frequency events may be suppressed after a vendor-specific threshold.

Therefore:

> **event occurrence ≠ guaranteed one retained entry per occurrence**.

The log may preserve the fact-pattern needed for diagnostics without retaining one-to-one event cardinality.

### The reporting context is a retained view, not the log itself

PEL data can be larger than one host transfer. NVMe therefore defines an `Action` field for Get Log Page that can establish a reporting context, read from an existing context, or release it.

The controller should retain that context until release, reset, or a vendor-specific interval long enough for retrieval. Events that occur while a reporting context exists are still logged, but **shall not be reported in the existing context**.

This gives three distinct relations:

> **reporting context ≠ persistent event log**.

> **stable retrieval view ≠ frozen ongoing device history**.

> **reporting-context lifetime ≠ event-retention lifetime**.

A reader can obtain a stable bounded view while the underlying device continues to accumulate later events.

### Retrieval consistency itself can require retained control state

A multi-command read needs the controller to remember which event population belongs to the established reporting context. The exact internal representation is vendor specific: the specification permits the context to be the log-page data itself or a set of pointers to events.

Therefore:

> **historical persistence can require a second-order retained retrieval state**.

That second-order state is not the history being preserved. It is temporary machinery that makes one recovery of that history coherent across multiple commands.

### One subsystem-wide event need not be multiplied by controller count

For events that affect multiple controllers, such as an NVM subsystem reset, the standard says the event should be logged once by a vendor-selected controller and not by the others.

Therefore:

> **one subsystem event ≠ one record per controller**.

Physical/controller multiplicity does not by itself define logical event multiplicity.

### Report order is useful but not a universal causal clock

NVMe says newer events should generally be reported earlier, while the method by which the subsystem determines event order is vendor specific.

Therefore:

> **reported event order ≠ universally specified physical event chronology**.

The log is historical, but its ordering contract should not be upgraded into a stronger distributed-clock or forensic-causality guarantee than the standard supplies.

### Selective forgetting is part of the history mechanism

PEL is interesting because its retention semantics include explicit conditions under which some history may be compressed by suppression, displaced by capacity policy, or altered during sanitize.

Thus:

> **retained device history can itself require selective forgetting**.

The mechanism is not an accidental failure of an otherwise perfect archive. Boundedness is part of the standardized operational model.

## Cross-case boundaries

### Versus Case 55 — NVMe SMART / Health

Case 55:

```text
current warning
    !=
cumulative counters
    !=
reserve/endurance estimate
```

Case 66:

```text
significant event occurrence
    -> persistent event entry
    -> bounded/suppressible/deletable event population
    -> reporting context
    -> host-recovered historical view
```

The two can compose because PEL includes SMART/Health snapshots, but they remain separate interfaces and temporal regimes.

### Versus Cases 44 and 47 — sanitization

Cases 44 and 47 ask whether user data becomes inaccessible or physically unrecoverable under interface and implementation-level erase/sanitize behavior.

Case 66 asks a different question: what happens to **device history metadata** when sanitize itself may reveal information about prior user activity.

Therefore:

> **sanitize-event record ≠ payload sanitization itself**.

A `Sanitize Completion` event reports historical evidence about an operation; it does not perform the media erasure.

### Versus ordinary telemetry

A current telemetry buffer or warning can disappear on reset without violating the PEL requirement. Conversely, an event entry can persist after the live condition that generated it is gone.

Therefore:

> **retained historical evidence ≠ current diagnostic condition**.

## Failure and forgetting boundaries

Distinct failure/forgetting modes include:

- a power failure may still cause some event-information loss despite the design recommendation for minimal loss;
- unsupported event classes are outside the standardized retained history;
- high-frequency repeated events may be suppressed;
- bounded size/count may force vendor-specific deletion;
- sanitize may remove or modify unspecified events for privacy/security reasons;
- a reporting context may disappear on reset while underlying PEL entries remain;
- event timestamps/order may not justify stronger chronology claims than the vendor-specific ordering contract;
- the controller may become unavailable even while some physical PEL embodiment survives;
- a named device may implement only the event types required for its supported command/features.

Forgetting in this case can therefore be **policy-mediated historical omission**, not only physical media decay or explicit payload erasure.

## Historical record / engineering reconstruction / interpretation ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| NVMe 1.4 §5.14.1.13 requires PEL information to survive power cycles and resets | `H/P` | official ratified specification |
| PEL is global to the NVM subsystem | `H/P` | explicit normative text |
| repeated high-frequency events may be suppressed under vendor-specific policy | `H/P` | explicit normative text |
| full-log deletion policy is vendor specific and may retain an older important event over newer events | `H/P` | explicit normative text |
| sanitize may alter PEL to prevent derivation of user data; exact removed events are unspecified | `H/P` | explicit normative text |
| PEL reporting context excludes events that occur after that context is established while those events are still logged | `H/P` | explicit normative text |
| SMART/Health snapshots can become PEL historical events | `H/P` | §5.14.1.13.1.1 |
| PEL therefore preserves every event over the entire usable life of every NVMe 1.4 device | `X` | contradicted by optional event support, suppression, finite capacity, and deletion rules |
| reporting context is the persistent history itself | `X` | context has a shorter/reset-sensitive lifetime and vendor-specific representation |
| NVMe 1.4 invented persistent event logging | `X` | no such priority claim is made or needed |
| a stable reporting context freezes device activity | `X` | later events are logged but omitted from the existing context |
| selective retention policy makes device history technically unlike a complete archive | `E/I` | bounded reconstruction from normative retention/suppression/deletion rules |

## Philosophical interpretation — bounded

This case supports one narrow conceptual pressure:

> **Technical retention of history is not equivalent to preserving every trace. A standard can define a history precisely by deciding which events become records, which repetitions may be suppressed, which records may be displaced, which records a security operation may alter, and how one reader stabilizes a recoverable view.**

That is not a claim that an SSD `remembers` in a human sense. It is an engineering observation about the conditions under which a device's past becomes selectively available to later operations.

The case also sharpens the repository's distinction between `state retention` and `history retention`: PEL is explicitly history-bearing, yet even here `history retention` does not mean an exhaustive archive.

## Cross-case result

Case 66 adds this chain:

```text
significant device event
    !=
current device state
    !=
persistent event entry
    !=
complete device-event sequence
    !=
SMART/Health aggregate state
    !=
PEL retention/suppression/deletion policy
    !=
reporting context
    !=
one recovered historical view
```

The strongest new result is that **persistent history can be both durable across failures and deliberately incomplete by design**, and that reading such a history coherently may itself require temporary retained control state.

## Prior art and anti-anachronism

NVM Express's 2019 public description presents PEL as enabling robust drive history for issue triage and debugging at scale. That is useful period institutional context for the feature's intended role, but the detailed semantics above come from the ratified Revision 1.4 specification.

This case does not claim that NVMe invented event logging, audit histories, black-box recording, or drive-health diagnostics. A full ATA/SCSI/vendor event-log genealogy would be a different historical slice. The defensible claim here is narrower:

> **By NVMe 1.4 in 2019, NVM Express standardized a host-visible, subsystem-global significant-event history with explicit cross-reset persistence, bounded/suppressible/deletable retention, sanitize interaction, and a reporting-context mechanism for coherent retrieval.**

## Sources

1. NVM Express, Inc., **NVM Express Base Specification Revision 1.4**, 10 June 2019, especially §5.14.1.13–5.14.1.13.1.15, printed pp. 138–151: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf>
2. NVM Express, Inc., **“New NVM Express, Inc. Specifications Bolster Cloud and Enterprise Advancements,”** 2019, describing PEL as robust drive history for issue triage/debug: <https://nvmexpress.org/new-nvm-express-inc-specifications-bolster-cloud-and-enterprise-advancements/>

## Related repositories

A repository search found no dedicated NVMe Persistent Event Log case in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). Broader controller/SSD chronology and ATA/SCSI event-log genealogy should be developed there if needed; this case keeps the retention-specific history semantics in `technical-retention`.
'''

evidence = r'''# Grounding Record — NVMe 1.4 Persistent Event Log (2019)

## Purpose

This record grounds [`../cases/66-nvme14-persistent-event-log-history.md`](../cases/66-nvme14-persistent-event-log-history.md).

The bounded claim is not that NVMe invented event logs. It is that **NVM Express Base Specification Revision 1.4 (10 June 2019) directly standardizes a persistent, subsystem-global significant-event history whose survival, capacity, suppression/deletion, sanitize interaction, and retrieval-context semantics are explicit enough to support a retention-specific case.**

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

A current search of `tmzncty/computing-archaeology` for `Persistent Event Log NVMe` returned no dedicated case. This record therefore keeps the retention-specific analysis here while leaving general SSD/controller history and ATA/SCSI genealogy to that repository if pursued later.

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

1. NVM Express, Inc., **NVM Express Base Specification Revision 1.4**, 10 June 2019, §5.14.1.13–5.14.1.13.1.15: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf>
2. NVM Express, Inc., **“New NVM Express, Inc. Specifications Bolster Cloud and Enterprise Advancements,”** 2019: <https://nvmexpress.org/new-nvm-express-inc-specifications-bolster-cloud-and-enterprise-advancements/>
'''

readme_case_line = "- [`cases/66-nvme14-persistent-event-log-history.md`](cases/66-nvme14-persistent-event-log-history.md) — grounded NVMe device-history bridge: Revision 1.4 Persistent Event Log retains significant events across power cycles/resets while making capacity, repeated-event suppression, vendor-specific deletion, sanitize interaction, and reporting-context retrieval explicit; persistent history is durable but deliberately bounded rather than a complete audit trace."
readme_evidence_line = "- [`evidence/66-nvme14-2019-persistent-event-log-grounding.md`](evidence/66-nvme14-2019-persistent-event-log-grounding.md) — Case-66 grounding record: directly inspected NVMe 1.4 §5.14.1.13 anchors cross-reset persistence, subsystem scope, finite/suppressible/deletable event retention, sanitize modification, reporting-context semantics, event types, and the SMART-snapshot boundary against Case 55."

case_index_row = "| [NVM Express 1.4 Persistent Event Log: Retained Device History, Selective Forgetting, and Snapshot-Consistent Retrieval](cases/66-nvme14-persistent-event-log-history.md) | **grounded** | subsystem-global persistent significant-event records + finite vendor-specific capacity/policy + sanitize interaction + temporary reporting context | separate persistent history from payload and complete trace; cross-reset persistence from indefinite retention; live SMART state from historical snapshot; underlying event accumulation from one stable retrieval view | [2019 NVMe 1.4 PEL grounding](evidence/66-nvme14-2019-persistent-event-log-grounding.md); ATA/SCSI genealogy, named-device implementation/compliance, physical PEL layout, later NVMe evolution, and failure-injection validation remain separate work |"

matrix_row = "| NVMe 1.4 Persistent Event Log / 2019 | subsystem-global significant-event entries + event metadata + bounded vendor retention policy + temporary reporting context | entries persist across power cycles/resets; repeated high-frequency events may be suppressed; bounded logs may delete selected events; sanitize may alter history | nondestructive Get Log Page retrieval; multi-command reads use an established reporting context while newer events continue to be logged outside that view | log identifier + event type/metadata + log offsets; reporting context selects one recoverable event population | physical embodiment is unspecified; reset need not erase events, while capacity/sanitize policy may retire or alter them | explicit event history, but policy-shaped and incomplete rather than a complete command/media trace |"

findings = r'''## Case 66 — NVMe 1.4 Persistent Event Log findings

733. **persistent event log ≠ user payload** — NVMe 1.4 makes significant device events a subsystem-global retained object separate from namespace/LBA contents;
734. **retained event history ≠ complete device history** — optional event support, frequency suppression, finite capacity, and deletion policy prevent the PEL from being treated as an exhaustive trace;
735. **persistence across power cycles/resets ≠ indefinite retention** — the same normative section that requires cross-reset persistence also defines later policy-mediated omission/deletion;
736. **usable-life sizing objective ≠ guarantee that every event survives usable life** — `should`-sized capacity coexists with explicit behavior for size/count/category limits;
737. **event occurrence ≠ guaranteed one retained entry per occurrence** — repeated events above a vendor-specific frequency threshold may be suppressed;
738. **newer event ≠ automatically higher retention priority** — NVMe explicitly permits an important older event to survive while newer events are deleted to make room;
739. **sanitize completion ≠ immutable preservation of device-event history** — sanitize may remove or modify PEL records to prevent derivation of user data;
740. **sanitize-event record ≠ payload sanitization itself** — PEL can retain a start/completion record about an operation without that event record performing the erasure;
741. **SMART/Health snapshot event ≠ live SMART/Health state** — PEL can preserve a past snapshot of the separate health interface;
742. **PEL event history ≠ SMART cumulative counters/estimates** — Case 55's aggregate/model/current health regimes and Case 66's event-oriented history can compose without becoming one state class;
743. **reporting context ≠ persistent event log** — the context is temporary vendor-specific retrieval state whose lifetime can end while underlying event entries remain;
744. **stable retrieval view ≠ frozen ongoing device history** — events occurring after context establishment continue to be logged but are excluded from that existing context;
745. **reporting-context lifetime ≠ event-retention lifetime** — release/reset can end the view without defining the retention lifetime of the PEL entries it selected;
746. **one subsystem-wide event ≠ one record per controller** — events affecting multiple controllers should be logged once by a vendor-selected controller;
747. **reported event order ≠ universally specified physical event chronology** — newer events are generally earlier, but the ordering method is vendor specific;
748. **retained device history can itself require selective forgetting** — suppression, bounded-capacity deletion, and sanitize modification make controlled omission part of the retention regime rather than merely an accidental failure.
'''


def insert_after_line_with(text, needle, new_line):
    if new_line in text:
        return text
    lines = text.splitlines()
    matches = [i for i, line in enumerate(lines) if needle in line]
    if not matches:
        raise RuntimeError(f"anchor not found: {needle}")
    lines.insert(matches[-1] + 1, new_line)
    return "\n".join(lines).rstrip() + "\n"


def patch_readme(text):
    text = insert_after_line_with(text, "cases/65-3d-nand-early-retention-loss-age-aware-reading.md", readme_case_line)
    text = insert_after_line_with(text, "evidence/65-3d-nand-2010-2018-early-retention-grounding.md", readme_evidence_line)
    return text


def patch_roadmap(text):
    if CASE_PATH in text:
        return text
    lines = text.splitlines()
    idx = next((i for i, line in enumerate(lines) if "SSD FTL/controller-mediated persistence" in line), None)
    if idx is None:
        raise RuntimeError("SSD roadmap anchor not found")
    line = lines[idx]
    line2, n = re.subn(r"55, 59, and 65\*\*", "55, 59, 65, and 66**", line, count=1)
    if n == 0:
        line2, n = re.subn(r"and 65\*\*", "65, and 66**", line, count=1)
    if n == 0:
        raise RuntimeError("could not update SSD case list")
    desc = " [`cases/66-nvme14-persistent-event-log-history.md`](cases/66-nvme14-persistent-event-log-history.md), grounded by [`evidence/66-nvme14-2019-persistent-event-log-grounding.md`](evidence/66-nvme14-2019-persistent-event-log-grounding.md), adds an explicit device-history regime above payload retention: NVMe 1.4 PEL keeps significant events across power cycles/resets but bounds that history through vendor-specific capacity, repeated-event suppression/deletion, sanitize modification, and a separate reporting context that stabilizes one multi-command read while newer events continue to accumulate. This deepens Case 55's aggregate health-history line without turning PEL into a complete audit trail or claiming NVMe invented event logging."
    marker = " The broad item stays unchecked because"
    if marker not in line2:
        raise RuntimeError("SSD broad-item marker not found")
    line2 = line2.replace(marker, desc + marker, 1)
    lines[idx] = line2
    return "\n".join(lines).rstrip() + "\n"


def patch_case_index(text):
    if CASE_PATH not in text:
        text = insert_after_line_with(text, "cases/65-3d-nand-early-retention-loss-age-aware-reading.md", case_index_row)
    if matrix_row not in text:
        lines = text.splitlines()
        h = next((i for i, line in enumerate(lines) if line.strip() == "## Comparison matrix — provisional"), None)
        if h is None:
            raise RuntimeError("comparison matrix heading not found")
        start = next((i for i in range(h + 1, len(lines)) if lines[i].startswith("| Case |")), None)
        if start is None:
            raise RuntimeError("comparison matrix table not found")
        end = start + 2
        while end < len(lines) and lines[end].startswith("|"):
            end += 1
        lines.insert(end, matrix_row)
        text = "\n".join(lines).rstrip() + "\n"
    if "## Case 66 — NVMe 1.4 Persistent Event Log findings" not in text:
        text = text.rstrip() + "\n\n" + findings.rstrip() + "\n"
    return text


def run(*args):
    return subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)


def main():
    subprocess.run(["git", "pull", "--ff-only", "origin", "main"], cwd=ROOT, check=True)

    (ROOT / CASE_PATH).write_text(case.rstrip() + "\n", encoding="utf-8")
    (ROOT / EVIDENCE_PATH).write_text(evidence.rstrip() + "\n", encoding="utf-8")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
    index = (ROOT / "CASE_INDEX.md").read_text(encoding="utf-8")

    (ROOT / "README.md").write_text(patch_readme(readme), encoding="utf-8")
    (ROOT / "ROADMAP.md").write_text(patch_roadmap(roadmap), encoding="utf-8")
    (ROOT / "CASE_INDEX.md").write_text(patch_case_index(index), encoding="utf-8")

    nums = sorted(int(p.name[:2]) for p in (ROOT / "cases").glob("[0-9][0-9]-*.md"))
    if nums != list(range(67)):
        raise RuntimeError(f"case-number ledger mismatch: {nums[:3]} ... {nums[-5:]}")
    for p in [CASE_PATH, EVIDENCE_PATH]:
        if not (ROOT / p).exists():
            raise RuntimeError(f"missing {p}")
    for nav in ["README.md", "ROADMAP.md", "CASE_INDEX.md"]:
        t = (ROOT / nav).read_text(encoding="utf-8")
        if CASE_PATH not in t:
            raise RuntimeError(f"{nav} missing case 66 path")
    idx_text = (ROOT / "CASE_INDEX.md").read_text(encoding="utf-8")
    if "733. **persistent event log" not in idx_text or "748. **retained device history" not in idx_text:
        raise RuntimeError("case 66 findings missing")
    if idx_text.count(CASE_PATH) < 1:
        raise RuntimeError("case 66 index row missing")
    run("git", "diff", "--check")

    subprocess.run(["git", "config", "user.name", "github-actions[bot]"], cwd=ROOT, check=True)
    subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], cwd=ROOT, check=True)
    subprocess.run(["git", "add", "README.md", "ROADMAP.md", "CASE_INDEX.md", CASE_PATH, EVIDENCE_PATH], cwd=ROOT, check=True)
    subprocess.run(["git", "rm", "-f", ".github/scripts/integrate_case66.py", ".github/workflows/integrate-case66.yml"], cwd=ROOT, check=True)
    subprocess.run(["git", "commit", "-m", "case66: ground NVMe persistent event history and retrieval context"], cwd=ROOT, check=True)
    subprocess.run(["git", "push", "origin", "HEAD:main"], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
