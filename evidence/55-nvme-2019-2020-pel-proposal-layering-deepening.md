# Case 55 deepening evidence — NVMe Persistent Event Log proposal layering (2019–2020)

## Status

**`bounded deepening complete`** for a narrow standards-history slice of Case 55.

This record tightens the open proposal-history boundary around the NVMe 1.4 **Persistent Event Log (PEL)**. It uses first-party NVM Express revision material and an NVM Express-sponsored June 2020 presentation to distinguish a first PEL proposal layer identified as **TP 4007** from a later event-set expansion identified as **TP 4042**.

The exact TP `4007a` and `4042a` proposal PDFs have **not** been directly inspected here. Therefore this record does not claim exact proposal submission dates, ballot chronology, author priority, line-by-line amendment history, or invention priority. It closes only the bounded question of whether the final NVMe 1.4 PEL event vocabulary can defensibly be treated as one undifferentiated single-step design.

## Research question

Case 55 already establishes that NVMe 1.4 added a persistent, selective event-history interface whose entries survive named power-cycle/reset boundaries but remain subject to suppression, bounded capacity, deletion, reporting-context, and sanitize-modification rules.

This pass asks a narrower historical question:

> Did the event vocabulary exposed by the ratified NVMe 1.4 PEL arrive as one indivisible proposal, or do NVM Express's own later materials preserve evidence of proposal-layered expansion?

The bounded answer is that first-party material explicitly distinguishes a **first version (TP 4007)** from a later event-set expansion and separately labels event groups as **TP 4007 events** and **TP 4042 events**.

## Sources and provenance

### 1. NVM Express — Changes in NVMe Revision 1.4

NVM Express's first-party revision summary identifies Persistent Event Log as a **new optional** NVMe 1.4 feature and points readers to **Technical Proposal `4007a`, `4042a`**.

It lists the ratified event families including:

- SMART/Health Log Snapshot;
- Firmware Commit;
- Timestamp Change;
- Power-on or Reset;
- NVM Subsystem Hardware Error;
- Change Namespace;
- Format NVM Start & Completion;
- Sanitize Start & Completion;
- Set Feature;
- Telemetry Log Created;
- Thermal Excursion;
- Vendor Specific;
- TCG Reserved Event.

Source:

<https://nvmexpress.org/changes-in-nvme-revision-1-4/>

This source establishes the **ratified-revision-to-TP reference relation**. It does not, by itself, say which event type entered through which proposal.

### 2. NVM Express-sponsored presentation — 30 June 2020

The presentation **_NVMe SSD Management, Error Reporting and Logging Capabilities_**, dated **30 June 2020**, is explicitly marked **Sponsored by NVM Express**. Speakers include Rohit Gupta, Bill Martin, and Jonmichael Hands; one slide identifies Hands as Intel SSDs / Co-Chair of the NVMe Marketing WG.

Official NVM Express-hosted PDF:

<https://nvmexpress.org/wp-content/uploads/June-2020-NVMe%E2%84%A2-SSD-Management-Error-Reporting-and-Logging-Capabilities.pdf>

Two slides are decisive for this bounded chronology.

#### Slide 16 — “First version (TP 4007)” versus “Second version”

The PEL table explicitly labels one column **`First version (TP 4007)`**. It assigns to that first version:

- SMART / Health Log Snapshot;
- Firmware Commit Event;
- Timestamp Change;
- Power-On or Reset;
- Vendor Specific.

A separate **`Second version`** column lists:

- Subsystem hardware error;
- Set Feature;
- Format;
- Sanitize;
- Namespace Create/Delete;
- TCG;
- Temperature Excursion.

A third **`Future work`** column lists ideas such as Power Excursion, Voltage Excursion, Rebuild Assist notification, NVMe-MI failures, IO Determinism, and Performance stats.

The three-column presentation matters because it prevents a later reader from collapsing:

```text
first proposal layer
    == ratified final event set
    == later contemplated event set
```

Those are explicitly different categories in the 2020 first-party presentation.

#### Slide 28 — explicit TP 4007 / TP 4042 event grouping

A later PEL slide explicitly labels two groups **`TP 4007 events`** and **`TP 4042 events`**.

The TP 4007 group contains:

- Firmware Commit;
- SMART/Health Log Snapshot;
- Timestamp Change;
- Power On or Reset;
- Vendor defined.

The TP 4042 group contains:

- NVM Subsystem HW Reset;
- Change Namespace;
- Format NVM Start;
- Format NVM Completion;
- Sanitize Start;
- Sanitize Completion;
- Set Feature;
- Thermal;
- Telemetry.

This is the strongest first-party evidence recovered in this pass for **proposal-layered event-taxonomy expansion**.

### 3. Official specification archive

The NVM Express specification archive lists NVMe 1.4 and a downloadable **NVM Express 1.4 Ratified TPs** package.

<https://nvmexpress.org/nvm-express-specification-archives/>

The archive proves that a ratified-TP package is part of the official revision archive. In this pass the package could not be decomposed into directly inspectable individual TP texts through the available retrieval path. The project therefore retains a strict distinction between:

```text
first-party retrospective mapping of event groups to TP numbers
    !=
direct inspection of the normative proposal texts
```

## Historical record

### NVMe 1.4 PEL is tied by NVM Express to two technical proposals

NVM Express's revision-1.4 change ledger lists PEL as a new optional feature and references **TP 4007a and TP 4042a**.

That is enough to reject a description in which the entire ratified PEL feature is casually attributed to only one proposal.

It is not enough to determine exact proposal chronology, because the change ledger is a summary rather than the proposal file itself.

### NVM Express later describes TP 4007 as the “first version”

The June 2020 presentation uses the explicit phrase **`First version (TP 4007)`** and gives it a smaller core event set centered on:

- health snapshot;
- firmware commit;
- timestamp change;
- power/reset;
- vendor-defined event.

This is a first-party retrospective characterization, not language recovered from TP 4007 itself.

The bounded historical claim is therefore:

> By June 2020, NVM Express publicly described the PEL design as having a first version associated with TP 4007.

It does **not** establish the date at which TP 4007 was first submitted, the date of each revision, or whether an earlier private draft existed.

### TP 4042 is presented as an event-taxonomy expansion

The later slide's side-by-side labels map the broader set of management/lifecycle events to **TP 4042**: subsystem hardware reset, namespace change, Format start/completion, Sanitize start/completion, Set Feature, Thermal, and Telemetry.

The first-version/second-version slide gives the same broad division without putting `TP 4042` in the second-column heading; the explicit TP mapping appears on the later slide. Taken together, these slides support a bounded reconstruction:

```text
TP 4007
    -> core persistent-event framework + initial event families

TP 4042
    -> additional event families / richer lifecycle observability

ratified NVMe 1.4
    -> one combined PEL interface exposing both groups
```

The arrows are **historical reconstruction from first-party retrospective material**, not a substitute for line-by-line TP diffing.

### The expansion changes what history can be represented

The TP 4007 group mainly records health/configuration/boot chronology:

- SMART/Health state snapshots;
- firmware commits;
- timestamp changes;
- power/reset episodes;
- vendor-defined events.

The TP 4042 group makes more operational lifecycle transitions representable:

- hardware reset;
- namespace change;
- formatting;
- sanitization;
- feature changes;
- thermal events;
- telemetry creation.

In particular, separate **Format Start / Format Completion** and **Sanitize Start / Sanitize Completion** events preserve a stronger distinction between an operation being initiated and it reaching its reported completion state.

This historical observation does not prove that TP 4042 invented the underlying operations, their completion semantics, event logging generally, or persistent storage of diagnostic history.

### “Future work” is not silently backdated into NVMe 1.4

The 2020 slide separates ratified first/second-version event classes from a **Future work** column. That column includes additional proposed categories such as power/voltage excursions and performance statistics.

Therefore:

```text
mentioned in an NVM Express presentation
    !=
already ratified as an NVMe 1.4 PEL event type
```

This is a useful anti-anachronism guardrail when using later presentations to reconstruct an earlier standard.

## Engineering reconstruction

The following are project terms, not period NVM Express terminology.

### Event-log framework and event vocabulary are separate layers

A persistent log can exist as an interface framework while the event taxonomy that populates it expands.

```text
PEL persistence / retrieval machinery
    !=
set of event classes admitted to that machinery
```

The 2020 TP grouping makes this distinction visible without requiring an undocumented claim about firmware internals.

### Event-taxonomy expansion is a change in observability, not necessarily a change in the underlying operation

Format, Sanitize, namespace change, Set Feature, thermal events, and telemetry already have technical meanings outside the PEL taxonomy. Adding them as PEL event types changes the standardized historical trace that software may later retrieve.

Therefore:

```text
operation existed
    !=
operation had a standardized persistent event trace
```

and:

```text
new event type
    !=
new physical mechanism
```

### Start and completion are distinct retained facts

The TP 4042 event group separately names Format and Sanitize start/completion states. This supports the same bounded relation already used elsewhere in Case 55:

```text
operation requested / started
    !=
operation reported complete
    !=
independent physical verification of its objective
```

For sanitize specifically, a completion event is not forensic proof that every stale physical embodiment is unrecoverable.

### More event categories do not strengthen the persistence guarantee by themselves

The proposal-layering evidence concerns **what event classes can be represented**. It does not strengthen NVMe 1.4's already-grounded persistence boundary.

Therefore:

```text
richer event taxonomy
    !=
lossless abrupt-power capture
    !=
immutable history
    !=
complete history
```

The normative 1.4 rules about reset/power-cycle persistence, suppression, finite bounds, deletion, and sanitize modification remain the authority for those questions.

### Retrospective proposal mapping is weaker than proposal-text inspection

The 2020 presentation is first-party and highly useful, but it remains retrospective explanatory material.

Therefore:

```text
NVM Express says “TP 4007 events / TP 4042 events” in 2020
    !=
all wording, dates, and intermediate revisions of TP 4007a / 4042a have been recovered
```

This distinction is important enough to preserve in the evidence status.

## Functional analogy — bounded

The 1999 ATA/ATAPI-5 self-test log remains earlier evidence for a storage device retaining bounded diagnostic history. The comparison is only functional:

```text
ATA self-test history
    -> bounded history of diagnostic executions/results

NVMe PEL
    -> bounded typed history of heterogeneous subsystem events
```

This pass does **not** establish a direct ATA→NVMe genealogy.

Within NVMe itself, proposal-layered PEL taxonomy can be compared functionally to schema evolution: a later interface version can make additional kinds of past event legible without changing the fact that earlier events physically occurred. This is an engineering analogy only; PEL is not being redescribed as a database schema migration mechanism.

## Philosophical interpretation — bounded

Project-level interpretation only:

> What a technical object can later “remember” depends not only on how long bits survive, but also on which event categories the interface makes nameable and retainable.

The proposal-layering evidence sharpens that point. Expanding the event taxonomy expands the **representable history** available to later software: a Sanitize start, a Sanitize completion, a namespace change, or a thermal excursion can become a standardized retained trace rather than remaining only an underlying episode.

The limit is strict. This does not mean an unlogged event did not occur, that the event taxonomy is culturally or philosophically neutral, or that standardizing a trace is identical to preserving a complete past.

## Claim ledger

| Claim | Label | Status |
| --- | --- | --- |
| NVM Express's NVMe 1.4 change ledger associates PEL with TP `4007a` and `4042a` | `H/P` | strong first-party revision-history mapping |
| A June 30, 2020 NVM Express-sponsored presentation labels a PEL `First version (TP 4007)` | `H/P` | strong first-party retrospective standards-history evidence |
| The same presentation groups SMART/Health snapshot, firmware commit, timestamp change, power/reset, and vendor-defined events under TP 4007 | `H/P` | strong presentation evidence |
| The presentation separately labels hardware-reset, namespace, Format, Sanitize, Set Feature, Thermal, and Telemetry families as TP 4042 events | `H/P` | strong first-party retrospective mapping |
| TP 4042 expanded the standardized PEL event vocabulary beyond the TP 4007 core | `H/P/E` | bounded reconstruction from first-party grouping; exact proposal diff still open |
| The final NVMe 1.4 PEL event set should be treated as a single undifferentiated proposal with no internal drafting layers | `X` | contradicted by first-party TP grouping |
| An event-taxonomy expansion proves a stronger persistence/durability guarantee | `X` | rejected; taxonomy and persistence contract are separate relations |
| Format/Sanitize start events are equivalent to completion events | `X` | rejected; first-party event taxonomy distinguishes them |
| A Sanitize Completion PEL event independently verifies physical sanitization | `X` | rejected; retained event history is not forensic verification |
| TP 4007/4042 grouping proves invention priority, exact ballot dates, exact revision diffs, or direct ATA→NVMe genealogy | `X` | rejected; individual TP texts were not directly inspected |
| Categories shown as `Future work` in the 2020 presentation were already ratified NVMe 1.4 PEL event types | `X` | rejected by the presentation's own three-way classification |

## Open evidence debt

This pass **partially closes** the earlier `TP4007a/4042a proposal chronology` debt by recovering a first-party proposal-layer mapping. It does not fully close proposal archaeology.

Still open:

- directly inspect individual ratified TP `4007a` and `4042a` texts;
- recover proposal submission/revision/ballot dates and author/editor metadata before making exact chronology claims;
- compare the proposal texts line-by-line against ratified NVMe 1.4 §5.14.1.13;
- determine whether any event classes moved between proposals during intermediate revisions;
- do not infer controller firmware implementation, persistent-medium layout, update atomicity, or abrupt-power-failure behavior from the proposal taxonomy;
- broader NVMe standards genealogy should be developed in `tmzncty/computing-archaeology` if it grows beyond this retention-specific boundary.

## Sources

1. NVM Express, **Changes in NVMe Revision 1.4**, first-party revision summary; PEL references TP `4007a`, `4042a`: <https://nvmexpress.org/changes-in-nvme-revision-1-4/>
2. NVM Express-sponsored, **_NVMe SSD Management, Error Reporting and Logging Capabilities_**, 30 June 2020, especially the PEL “First version (TP 4007) / Second version / Future work” slide and the later “TP 4007 events / TP 4042 events” slide: <https://nvmexpress.org/wp-content/uploads/June-2020-NVMe%E2%84%A2-SSD-Management-Error-Reporting-and-Logging-Capabilities.pdf>
3. NVM Express, **NVM Express Specification Archives**, listing NVMe 1.4 and the `NVM Express 1.4 Ratified TPs` archive: <https://nvmexpress.org/nvm-express-specification-archives/>
4. Existing Case 55 normative PEL evidence, [`55-nvme14-2019-persistent-event-log-deepening.md`](55-nvme14-2019-persistent-event-log-deepening.md), for the ratified NVMe 1.4 persistence/suppression/deletion/reporting-context/sanitize semantics.

## Related repositories

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated TP4007/TP4042 or Persistent Event Log standards-history slice. This record therefore retains the bounded proposal-layering result here. A full NVMe technical-proposal genealogy, committee process history, or controller-implementation lineage belongs primarily in `computing-archaeology` and should be linked back rather than duplicated here.