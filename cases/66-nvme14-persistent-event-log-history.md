# NVM Express 1.4 Persistent Event Log: Retained Device History, Selective Forgetting, and Snapshot-Consistent Retrieval

## Status

**`grounded`** — bounded to the Persistent Event Log (`PEL`, Log Identifier `0Dh`) standardized in NVM Express Base Specification Revision 1.4, dated 10 June 2019. Earlier NVMe Revision 1.0 (2011) and Revision 1.3c (2018) are used only to establish a narrower prior-art and lifetime contrast for diagnostic state; they are not treated as the PEL mechanism itself.

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

### The same NVMe interface family contains deliberately different history lifetimes

PEL is easier to misread if every diagnostic log is treated as one generic history store. Earlier NVMe revisions already expose a different lifetime decomposition.

NVM Express Revision 1.0, ratified **1 March 2011**, defines the Error Information entry's 64-bit `Error Count` as an incrementing identifier retained across power-off conditions. The same revision describes SMART / Health information as information over the life of the controller that is retained across power cycles. This is an earlier NVMe floor for **retained diagnostic summary/ordinal state**, not for the later PEL mechanism.

By Revision 1.3c, dated **24 May 2018**, §5.14.1.1 describes the controller-global Error Information log as a bounded recent-error list. If full, the controller **should** insert the new entry and discard the oldest, and it **should** remove all entries on power cycle and reset. The `Error Count`, however, is still specified as retained across power-off conditions.

Revision 1.4 preserves this contrast while adding PEL. In the same specification family:

- Error Information is **controller-global** in Revision 1.3c/1.4;
- its recent detailed entries are recommended to be cleared on power/reset boundaries;
- the per-error `Error Count` survives power-off conditions;
- PEL is **NVM-subsystem-global** and its event information **shall** survive power cycles and resets, subject to the separate suppression/deletion/sanitize rules already discussed above.

Therefore:

> **detailed diagnostic entry lifetime ≠ diagnostic count lifetime ≠ persistent event-history lifetime**.

and:

> **controller-local history scope ≠ subsystem-global history scope**.

The standard can preserve a long-lived ordinal/aggregate trace while allowing a richer recent-entry population to disappear at a failure boundary, then separately provide another log whose event records cross that boundary.

## Retained states and control state

The bounded regime contains several separable states:

1. **user payload** — namespace/LBA data, outside the PEL itself;
2. **persistent event entries** — historical records of supported significant events;
3. **event metadata** — event type/revision plus time/controller and event-specific information;
4. **capacity and retention policy** — supported size/count and vendor-specific suppression/deletion behavior;
5. **reporting context** — a temporary controller-created selection/view describing what one PEL retrieval should include;
6. **current controller/subsystem state** — the live state from which some later events may be generated;
7. **other diagnostic state** — SMART/Health and telemetry, which may be snapshotted or referenced but are not identical to PEL.
8. **Error Information state** — controller-local recent detailed entries plus a cross-power `Error Count` whose lifetime is not the same as the entry population or PEL.

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

### A retained count can outlive the detailed records it once identified

The Error Information contrast makes the repository's `history retention` category more precise. A controller may retain the monotonically advancing `Error Count` across power-off while the richer recent Error Information entries are recommended to be cleared at power/reset boundaries.

Therefore:

> **retained historical count/ordinal ≠ retained historical detail**.

A later observer may learn that error-history state advanced without recovering the queue ID, command ID, status, LBA, namespace, parameter-error location, or other fields of the discarded earlier entry. Persistence of the summary relation does not reconstruct the forgotten event record.

This also blocks a scope shortcut:

> **same Get Log Page command family ≠ same retention regime**.

NVMe log pages can differ in scope, persistence boundary, capacity policy, and historical granularity even when they share a retrieval command family.

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

Case 55 and the pre-PEL Error Information path already show that diagnostic state can split by lifetime:

```text
current warning
    !=
cumulative/lifetime counters
    !=
recent detailed Error Information entries
    !=
cross-power Error Count ordinal
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
| NVMe 1.3c recommends clearing detailed Error Information entries on power cycle/reset while retaining the entry `Error Count` across power-off | `H/P` | official Revision 1.3c §5.14.1.1; preserve `should` strength |
| NVMe 1.4 keeps Error Information controller-global while PEL is NVM-subsystem-global and cross-reset persistent | `H/P` | official Revision 1.4 §§5.14.1.1, 5.14.1.13 |
| a retained error count reconstructs the discarded detailed error entry | `X` | count/ordinal persistence does not preserve queue, command, status, LBA, namespace, parameter-error location, or other discarded fields |
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
recent Error Information entry population
    !=
cross-power Error Count ordinal
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

This case does not claim that NVMe invented event logging, audit histories, black-box recording, or drive-health diagnostics. Even inside NVMe, Revision 1.0 in 2011 already retained Error Count across power-off and SMART/Health information across power cycles, while Revision 1.3c in 2018 explicitly paired a reset-cleared recent Error Information population with a cross-power Error Count. These are earlier floors for retained diagnostic state and mixed history lifetimes, not the PEL mechanism itself.

A full ATA/SCSI/vendor event-log genealogy would be a different historical slice. The defensible 2019 claim is narrower:

> **By NVMe 1.4 in 2019, NVM Express standardized a host-visible, subsystem-global significant-event history with explicit cross-reset persistence, bounded/suppressible/deletable retention, sanitize interaction, and a reporting-context mechanism for coherent retrieval.**

## Sources

1. NVM Express, Inc., **NVM Express Base Specification Revision 1.4**, 10 June 2019, especially §5.14.1.1 (printed p. 120) and §5.14.1.13–5.14.1.13.1.15 (printed pp. 138–151): <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf>
2. NVM Express, Inc., **NVM Express Revision 1.3c**, 24 May 2018, §5.14.1.1, printed p. 103: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_3c-2018.05.24-Ratified.pdf>
3. NVM Express / NVMHCI Workgroup, **NVM Express Revision 1.0**, ratified 1 March 2011, §5.10.1.1–5.10.1.2, printed pp. 63–64: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_0-Gold.pdf>
4. NVM Express, Inc., **“New NVM Express, Inc. Specifications Bolster Cloud and Enterprise Advancements,”** 2019, describing PEL as robust drive history for issue triage/debug: <https://nvmexpress.org/new-nvm-express-inc-specifications-bolster-cloud-and-enterprise-advancements/>

## Related repositories

A repository search found no dedicated NVMe Persistent Event Log case in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). Broader controller/SSD chronology and ATA/SCSI event-log genealogy should be developed there if needed; this case keeps the retention-specific history semantics in `technical-retention`.

## 2021 implementation and reporting-generation deepening

The original Case 66 boundary remains the ratified NVMe 1.4 PEL contract of 10 June 2019. This section adds **later implementation evidence and post-1.4 retrieval-validity evolution** without projecting those later rules backward into the 2019 standard.

### 2019 host tooling exposed support and size before a full PEL decoder landed

Two `linux-nvme/nvme-cli` commits dated **25 August 2019** added host-side Identify Controller visibility for the new NVMe 1.4 PEL surface:

- `81b5524bc887cb63447f5acbe41bb128bf62cb8c` — `id-ctrl: show Persistent Event Log Size(PELS)`;
- `cf98706f0051d44cea4e72abc43c78555040e77b` — `id-ctrl: show Persistent Event Log support in LPA`.

These are primary implementation-history artifacts for the Linux NVMe tooling ecosystem. They show that software could expose whether a controller advertised PEL support and its maximum log size shortly after NVMe 1.4 was ratified.

They do **not** prove that the tool could yet reconstruct the complete event population, that any named controller obeyed the cross-reset persistence requirement, or that 25 August 2019 is the origin date of PEL. The normative mechanism remains grounded in the earlier NVMe 1.4 standard.

Therefore:

> **advertised PEL support / size ≠ demonstrated PEL retrieval correctness.**

### January 2021 adds a full host-side PEL retrieval/parser path

On **11 January 2021**, `linux-nvme/nvme-cli` commit `6879ac41fcc62c468452a8c3e18c60c41e7eac62` added support for Persistent Event Log Page retrieval and decoding, explicitly citing NVMe 1.4 §5.14.1.13 and its cross-power/reset persistence contract.

This is useful implementation evidence because it establishes a concrete host software path from the standardized log to operator-visible event history. It is still not device-conformance evidence:

> **host parser implementation ≠ controller implementation or conformance.**

The host can know the wire format and still encounter controller-specific unsupported events, malformed data, tool bugs, or transfer-consistency problems.

### A November 2021 parser fix contains a named Samsung PM1735 retrieval artifact

Commit `d7c2dd59633fb0485edb5f6093d87154b19ace72`, dated **11 November 2021**, fixes a crash/misparse in the PEL path and includes an actual command/output artifact from a Samsung **PM1735**, reported as `PCIe4 1.6TB NVMe Flash Adapter x8`. The captured header shows a nontrivial PEL population and then demonstrates the parser losing event boundaries and producing implausible event types before the fix.

This is deliberately used at a narrow level:

- it is a **named hardware/tooling retrieval witness**;
- it proves that a real PM1735 exposed enough PEL data for the Linux tool to parse and fail on it;
- it does **not** prove cross-power-cycle persistence by controlled test;
- it does **not** prove that every PEL field/event on that drive conforms to every NVMe 1.4 requirement;
- it does **not** reveal the physical medium or controller metadata layout used to retain PEL entries.

The artifact supplies an important retention boundary:

> **underlying event-history presence ≠ correct host reconstruction of that history.**

A software decoding failure can make retained history operationally illegible without establishing that the controller forgot the history itself.

### NVMe 2.0a makes multi-command retrieval validity explicitly checkable

The ratified **NVM Express Base Specification Revision 2.0a**, dated **26 July 2021**, adds an explicit `Generation Number` and reporting-context information to the PEL header. For a PEL not read in one Get Log Page command, the host is instructed to:

1. establish a reporting context;
2. read the Generation Number before collecting the remainder of the log;
3. read the log through that context;
4. reread the Generation Number after the entire transfer;
5. reread the log if the two generation numbers do not match.

Revision 2.0a says a mismatch means the reporting context **may have been lost**, the collected PEL contents **may be invalid**, and host software should reread the log. The Generation Number increments when a reporting context is established and the log page returns data different from the previous reporting context, with defined rollover behavior.

Two `nvme-cli` commits dated **15 November 2021** implement this later contract:

- `303e03c6e228f9296b2fa70ec899db620f2e10f6` — verifies the Generation Number around a multi-command PEL collection and rereads on inconsistency;
- `82ea68f15b5b5bb0426dc28185fee07baa3729bb` — adds the NVMe 2.0a Generation Number and Reporting Context Information fields.

This creates a stronger distinction than the original 2019 case could establish:

> **persistent log ≠ valid retrieved image.**

> **successful chunk transfers ≠ one coherent historical view.**

> **reporting-context establishment ≠ proof that the same context survived the complete retrieval.**

The later Generation Number is a validation relation over the **host's recovered view** of retained history. It is not itself the event history and it is not evidence that every event has been preserved indefinitely.

### Generation mismatch is not itself proof of event loss

The NVMe 2.0a wording is intentionally conditional: when the numbers differ, the context may have been lost and the contents may be invalid. That does not establish which event entries physically disappeared, whether the underlying PEL changed legitimately, or whether the host merely crossed reporting contexts during retrieval.

Therefore:

> **retrieval-generation mismatch ≠ proven event erasure.**

and conversely:

> **matching generation ≠ archival completeness.**

A matching generation qualifies one collected image as belonging to one stable reporting generation. The separate NVMe 1.4/2.0a capacity, suppression, deletion, sanitize, and supported-event rules still bound what history can exist in that image.

### Reporting-context loss and PEL loss remain different failure classes

Case 66 already separated the temporary reporting context from the longer-lived PEL. The 2.0a Generation Number makes that separation operationally testable:

```text
persistent event population
    != temporary reporting context
    != reporting-generation validation token
    != host transfer buffers
    != decoded operator-visible history
```

A controller reset can invalidate the reporting context while the PEL's cross-reset retention contract still applies to event information. Host software then has reconstruction work to do again. This is not media repair; it is **re-establishment and validation of a retrieval relation**.

### Cross-case boundary: Case 90 is analogy, not genealogy

Case 90's later Kafka leader-epoch history shows a different system in which retained recovery metadata may physically exist yet be incomplete or ineligible for the recovery decision being attempted. The useful comparison is only functional:

> **retained metadata presence ≠ metadata admissibility for a particular recovery/retrieval operation.**

PEL Generation Number validation and Kafka leader-epoch admissibility are not the same mechanism, do not share a demonstrated lineage, and operate at different layers.

### Related-repository boundary

A fresh repository search in this round found no dedicated NVMe Persistent Event Log case in `tmzncty/computing-archaeology`. The broad ATA/SCSI/NVMe diagnostic-log genealogy, device-controller architecture, and physical firmware implementation remain better candidates for that companion repository. Case 66 keeps only the retention-specific lifetime, selection, retrieval, and validity relations.

## Sources added in this deepening

1. NVM Express, Inc., **NVM Express Base Specification Revision 2.0a**, 26 July 2021, Persistent Event Log reporting-context / Generation Number provisions: <https://nvmexpress.org/wp-content/uploads/NVMe-NVM-Express-2.0a-2021.07.26-Ratified.pdf>
2. `linux-nvme/nvme-cli`, `81b5524bc887cb63447f5acbe41bb128bf62cb8c`, **“id-ctrl: show Persistent Event Log Size(PELS)”**, 25 August 2019: <https://github.com/linux-nvme/nvme-cli/commit/81b5524bc887cb63447f5acbe41bb128bf62cb8c>
3. `linux-nvme/nvme-cli`, `cf98706f0051d44cea4e72abc43c78555040e77b`, **“id-ctrl: show Persistent Event Log support in LPA”**, 25 August 2019: <https://github.com/linux-nvme/nvme-cli/commit/cf98706f0051d44cea4e72abc43c78555040e77b>
4. `linux-nvme/nvme-cli`, `6879ac41fcc62c468452a8c3e18c60c41e7eac62`, **“nvme: add support for persistent event log page”**, 11 January 2021: <https://github.com/linux-nvme/nvme-cli/commit/6879ac41fcc62c468452a8c3e18c60c41e7eac62>
5. `linux-nvme/nvme-cli`, `d7c2dd59633fb0485edb5f6093d87154b19ace72`, **“libnvme: core dump when running nvme persistent-event-log”**, 11 November 2021: <https://github.com/linux-nvme/nvme-cli/commit/d7c2dd59633fb0485edb5f6093d87154b19ace72>
6. `linux-nvme/nvme-cli`, `303e03c6e228f9296b2fa70ec899db620f2e10f6`, **“nvme: PEL need to check gen number for verification of collected log”**, 15 November 2021: <https://github.com/linux-nvme/nvme-cli/commit/303e03c6e228f9296b2fa70ec899db620f2e10f6>
7. `linux-nvme/nvme-cli`, `82ea68f15b5b5bb0426dc28185fee07baa3729bb`, **“Add New fields on PEL based on NVMe 2.0a”**, 15 November 2021: <https://github.com/linux-nvme/nvme-cli/commit/82ea68f15b5b5bb0426dc28185fee07baa3729bb>

## 2019 public-release / operation-phase evidence deepening

This bounded addendum closes two small evidence gaps without changing Case 66's mechanism scope. NVM Express' first-party announcement is precisely dated **23 July 2019**; the ratified Revision 1.4 document itself is dated **10 June 2019**. Therefore `specification document date != public-release announcement date != invention / first-implementation date`.

Sections 5.14.1.13.1.7-10 sharpen the event-history/effect boundary. `Format NVM Start` is recorded after parameter validation but **before modifying any NVM contents**; `Format NVM Completion` is recorded after a Format command that modified NVM contents completes and carries status/incomplete-format information. `Sanitize Start` is recorded at operation start, while `Sanitize Completion` is recorded at completion and carries sanitize progress/status information.

Therefore `retained operation-start evidence != evidence that the operation completed`, and `controller-reported completion/status evidence != independent proof of lower-layer physical erasure`. Case 66 concerns retained historical evidence; Cases 44 and 47 remain responsible for command-level sanitize semantics and empirical remanence. The Start/Completion pairing shows that a retained history can preserve **phase-qualified evidence** about one maintenance action rather than an undifferentiated fact that “format happened” or “sanitize happened.”
