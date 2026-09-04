# NVM Express 1.4 Persistent Event Log: Retained Device History, Selective Forgetting, and Snapshot-Consistent Retrieval

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
