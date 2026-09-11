# Case 20 evidence deepening — NVMe 1.0 shutdown notification, completion, and unsafe-shutdown telemetry (2011)

**Status:** `grounded`

**Case:** [Case 20 — NVM Express 1.0 Volatile Write Cache and FUA](../cases/20-nvme10-fua-flush-persistence-ordering.md)

**Scope:** the original NVM Express Revision 1.0 shutdown state machine and its SMART/Health `Unsafe Shutdowns` counter. This slice asks how a host's declaration that power-off is imminent, the controller's completion of shutdown processing, the later loss of power, and retained telemetry about that transition are separated at the interface. It does **not** claim that NVMe invented orderly shutdown, that a shutdown-status bit proves application/database commit, that `Unsafe Shutdowns` directly counts data-loss incidents, or that the interface reveals the controller's capacitor/FTL/NAND implementation.

## Research question

Case 20 already separates generic command completion, volatile-cache state, Flush/FUA persistence, and AWUPF power-fail atomicity. A remaining transition question is narrower:

> **When power-off is imminent, does NVMe treat “the host requested shutdown,” “the controller finished shutdown processing,” and “later telemetry calls the event unsafe” as one fact?**

Revision 1.0 answers no. It exposes three different pieces of state:

```text
CC.SHN          host-written shutdown notification / requested path
CSTS.SHST       controller-reported shutdown-processing state
Unsafe Shutdowns
      cumulative telemetry keyed to whether CC.SHN was received before power loss
```

That makes the bounded retention result:

```text
shutdown intent/request
    != shutdown processing complete
    != power actually removed
    != unsafe-shutdown telemetry classification
    != demonstrated data-loss outcome
```

## Primary source

NVMHCI Workgroup / NVM Express, **_NVM Express Revision 1.0_**, ratified **1 March 2011**, official NVM Express-hosted Gold PDF:

<https://nvmexpress.org/wp-content/uploads/NVM-Express-1_0-Gold.pdf>

Primary anchors inspected directly:

- printed p. 35, Controller Configuration `CC.SHN` — normal versus abrupt shutdown notification and the requirement to consult `CSTS.SHST` for completion;
- printed p. 36, Controller Status `CSTS.SHST` — normal/no-shutdown, processing, and processing-complete states;
- printed p. 66, SMART / Health Information — `Unsafe Shutdowns` counter definition;
- §7.6.2, printed p. 112 — separate normal and abrupt host shutdown procedures.

The document is an interface specification. It can ground host/controller transition semantics, but not the internal persistence mechanism of a named SSD.

## Historical record

### H1 — `CC.SHN` expresses a host notification and selects a shutdown path

Controller Configuration bits 15:14 are **Shutdown Notification (SHN)**. Revision 1.0 assigns:

- `00b` — no notification / no effect;
- `01b` — normal shutdown notification;
- `10b` — abrupt shutdown notification;
- `11b` — reserved.

The field description says a normal notification expects that the controller is given time to process shutdown, whereas for an abrupt notification the host may not wait for shutdown processing to complete before power is lost. It explicitly directs software to `CSTS.SHST` to determine when processing is complete.

This is direct historical evidence that:

> **`CC.SHN written != shutdown processing complete`.**

The distinction is in the 2011 interface itself; it is not a later project abstraction.

### H2 — `CSTS.SHST` is a separate controller-reported progress/completion state

Controller Status bits 3:2 report **Shutdown Status (SHST)**:

- `00b` — normal operation / no shutdown requested;
- `01b` — shutdown processing occurring;
- `10b` — shutdown processing complete;
- `11b` — reserved.

Thus the controller exposes an intermediate state between host intent and completed transition work. A notification may have been issued while the controller still reports processing rather than completion.

### H3 — normal and abrupt shutdown are distinct procedures, not synonyms

Section 7.6.2 gives separate sequences.

For a **normal shutdown**, the host is told to stop issuing new I/O, allow outstanding commands to complete, delete the I/O Submission Queues, delete the I/O Completion Queues, then set `CC.SHN=01b`; the controller reports completion with `CSTS.SHST=10b`.

For an **abrupt shutdown**, the host stops new I/O and sets `CC.SHN=10b`; the controller again reports completed processing through `CSTS.SHST=10b`.

The same completion code does not erase the fact that the requested path and pre-shutdown host work differ.

So:

> **`normal shutdown request != abrupt shutdown request`, even though both can eventually reach the same reported shutdown-complete state.**

### H4 — `Unsafe Shutdowns` is keyed to missing notification before power loss

The SMART / Health Information log defines **Unsafe Shutdowns** as a lifetime-style counter incremented when a shutdown notification (`CC.SHN`) is **not received before loss of power**.

The definition is important for what it does *not* say. It does not define the counter as:

- number of writes lost;
- number of torn writes;
- number of filesystems requiring recovery;
- number of shutdowns for which `CSTS.SHST` failed to reach complete;
- number of application transactions lost.

It records a protocol-observed transition condition: power was lost without prior shutdown notification.

### H5 — notification telemetry and completion telemetry are therefore different observables

Revision 1.0 provides a live `CSTS.SHST` progress/completion field but defines `Unsafe Shutdowns` only in terms of whether `CC.SHN` was received before loss of power. The latter definition does not say it records whether `SHST=10b` had been reached.

Therefore a later SMART/Health reader must not silently reinterpret the counter as a historical log of completed-versus-incomplete controller shutdown processing.

This yields the bounded historical relation:

```text
prior SHN receipt
    != proof that SHST had reached shutdown complete
```

and conversely:

```text
Unsafe Shutdowns increment
    == evidence for the specification's no-prior-SHN condition
    != direct evidence for a particular payload-loss outcome
```

## Engineering reconstruction

The following terms are project reconstructions, not NVMe Revision 1.0 vocabulary.

### E1 — intent-to-transition and completed transition work are separate retention states

The `SHN` / `SHST` split is a clean example of a transition contract with at least two moments:

```text
host declares imminent transition
        -> controller performs shutdown work
        -> controller reports transition work complete
```

The first edge does not collapse into the third state. For retention analysis this matters because a storage system may require time/work to move from ordinary service into a state admissible for power removal.

### E2 — `power-off imminent != already safe to remove power`

A shutdown notification exists precisely because the host can know that power loss is approaching before controller-side processing has necessarily finished. The interface exposes `SHST` so completion can be observed separately.

This is an interface-level statement about transition sequencing. It does not specify which internal bytes are copied, which NAND pages are programmed, whether a journal is replayed, or whether stored energy is used.

### E3 — unsafe-shutdown telemetry is not a data-loss oracle

The `Unsafe Shutdowns` counter classifies one condition: lack of prior SHN at power loss. The specification does not make actual payload loss a condition for incrementing it.

Therefore:

```text
Unsafe Shutdowns count
    != count of data-loss incidents
    != count of lost host writes
    != count of torn writes
```

A power loss without notification may increment the counter even when no application-visible payload is ultimately lost; conversely, a notification being received is not proof that every higher-layer semantic obligation had already been made durable.

### E4 — shutdown completion participates in a persistence boundary but is not a filesystem/database commit

The existing Case 20 evidence from NVMe 1.1b shows that volatile-cache writes lacking FUA/Flush can be exposed to older-value reappearance when the specified shutdown procedure is not completed. That later clause makes shutdown procedure completion relevant to the device-level persistence contract.

But the interface still cannot prove:

- a filesystem ordered its metadata correctly;
- a database transaction log was flushed at the correct semantic point;
- an application issued every required persistence operation;
- every downstream replica acknowledged a higher-level commit.

So:

> **`controller shutdown complete != higher-layer semantic commit`.**

### E5 — protocol-level shutdown semantics do not identify the physical mechanism

Nothing in `CC.SHN`, `CSTS.SHST`, or the SMART/Health counter demonstrates a particular power-loss-protection design. A conforming interface does not by itself prove the presence of capacitors, batteries, a specific FTL journal, copy-on-write mapping, NAND program granularity, or one exact firmware sequence.

`interface transition contract != named internal mechanism`

## Functional comparisons — bounded

### Case 15 — ATA / Intel SSD power-loss protection

[Case 15](../cases/15-intel-ssd320-power-loss-durability.md) contains earlier ATA durability semantics plus a named Intel SSD implementation path. It is useful only as a functional comparison: both cases involve persistence obligations around power transition, but the NVMe `SHN/SHST` state machine is not evidence that Intel's ATA-era controller used the same protocol or implementation.

No ATA→NVMe shutdown genealogy is claimed here.

### Case 55 — NVMe SMART / Health telemetry

[Case 55](../cases/55-nvme-smart-health-endurance-telemetry.md) treats host-visible health counters as retained reporting state. `Unsafe Shutdowns` fits that reporting family, while this slice adds a sharper warning: a cumulative counter may encode a **protocol classification** rather than a complete causal record of physical damage or payload loss.

`telemetry category != complete physical event history`

This is functional comparison only; it does not turn the counter into the NVMe 1.4 Persistent Event Log or imply identical retention policy.

## Project interpretation — bounded

**Project interpretation only:** retention is not always a steady-state property of a medium. A system can expose a temporary interval in which one actor has declared an impending transition while another actor still owes work before the transition is considered complete.

That makes a useful project-level distinction:

> **transition intent is not transition admissibility.**

The phrase is not historical NVMe terminology. It is a way to compare this interface with other cases where quiescent retention, transition safety, current control state, or maintenance completion must be kept separate.

## Stop conditions / anti-overclaim

This record does **not** establish any of the following:

- `SHN received => SHST complete`;
- `SHST complete => every application/database transaction is durable`;
- `abrupt SHN => zero data loss`;
- `Unsafe Shutdowns increment => actual payload loss occurred`;
- `Unsafe Shutdowns unchanged => no payload loss occurred`;
- `shutdown complete => sanitization or verified erasure`;
- a particular PLP capacitor, battery, FTL journal, or NAND recovery design;
- NVMe invention priority for orderly shutdown, abrupt shutdown, shutdown notification, or persistent power-loss telemetry.

Broader ATA/SCSI shutdown-command genealogy, proposal chronology, and named-product power-cut validation remain open. A search of `tmzncty/computing-archaeology` found no existing dedicated NVMe shutdown-history module at the time of this slice; any broad interface genealogy should be routed there rather than duplicated here.

## Bounded result

The 2011 NVMe interface supports the following compact model:

```text
CC.SHN = host intent / requested shutdown class
        !=
CSTS.SHST = controller processing/completion state
        !=
loss of power = external transition event
        !=
Unsafe Shutdowns = retained no-prior-SHN telemetry
        !=
actual payload / application-semantic loss outcome
```

This deepens Case 20 without replacing its existing Flush/FUA or AWUPF results. The case now has three distinct power-failure axes:

1. **persistence control** — volatile cache, Flush, FUA;
2. **failure atomicity** — AWUPF / torn-write result envelope;
3. **power-transition protocol** — SHN request, SHST completion, and retained unsafe-shutdown classification.

