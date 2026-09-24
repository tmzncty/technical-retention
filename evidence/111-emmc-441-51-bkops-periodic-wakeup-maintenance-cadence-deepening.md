# Case 111 deepening — eMMC 4.41→5.1 BKOPS, periodic wake-up, and maintenance-completion scope

**Canonical case:** [`../cases/111-enterprise-ssd-extended-shutdown-maintenance.md`](../cases/111-enterprise-ssd-extended-shutdown-maintenance.md)  
**Role:** standards/prior-art and control-surface deepening; **not** an enterprise-SSD implementation claim  
**Case maturity:** remains `grounded`

## Research question

Case 111 already separates standards retention qualification, powered maintenance opportunity, operator scheduling, maintenance telemetry, and retention-specific completion authority.

This slice asks a narrower prior-art/control question:

> Before the later IBM/Dell extended-shutdown runbooks, did a managed-Flash interface already expose a host-visible maintenance obligation, a way to admit/run background work, a way to preempt it for foreground service, and a configured periodic wake cadence that required a background-maintenance run to finish before the device was powered down again?

For JEDEC e•MMC, the bounded answer is **yes** for generic device maintenance.

The answer is **not** yes for the stronger claim that the interface proves completion of retention-refresh work specifically.

That distinction is the reason this evidence belongs in Case 111.

---

## Sources inspected

### Primary standards source

- JEDEC, **JESD84-B51, Embedded Multi-Media Card (e•MMC) Electrical Standard (5.1)**, February 2015. A page-preserving copy is hosted by Texas Instruments:
  - <https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/791/JESD84_2D00_B51-_2800_1_2900_.pdf>

Relevant printed sections/pages in that standard:

- §6.6.25, **Background Operations**, printed p. 93;
- §6.6.26, **High Priority Interrupt (HPI)**, printed pp. 94–95;
- §6.6.35.1, **Periodic Wake-up**, printed p. 111;
- §6.6.36, **Power Off Notification**, printed pp. 112–113;
- §7.4.33, `BKOPS_STATUS`;
- §7.4.82, `BKOPS_EN`;
- §7.4.95, `PERIODIC_WAKEUP`;
- Annex C, especially **C.5 Changes from version 4.4 to 4.41** and **C.10 Changes from version 5.01 to 5.1**.

### Contemporary implementation / publication-context sources

These are supporting chronology/context, not substitutes for the normative standard text:

- EE Times, **“JEDEC announces publication of e-MMC standard update v4.41,”** 10 May 2010:
  - <https://www.eetimes.com/jedec-announces-publication-of-e-mmc-standard-update-v4-41/>
- Linux-kernel mailing-list discussion, **“[PATCH v2 0/4] enable Background operations and HPI feature for eMMC4.41 card,”** 3 December 2010:
  - <https://lkml.indiana.edu/1012.0/01170.html>
- Linux-kernel mailing-list discussion, **“[PATCH v3] mmc: core: Add support for idle time BKOPS,”** 25 November 2012:
  - <https://lkml.iu.edu/1211.3/00159.html>

The Linux material is used only as evidence that hosts were implementing the standardized host/device maintenance handshake. It is not used to redefine JEDEC semantics.

---

## Historical / standards record

### H1 — Background Operations and HPI enter the eMMC revision chain together at 4.41

JESD84-B51 Annex C explicitly lists **Background Operations** and **High Priority Interrupt** as major additions in the change from version 4.4 to 4.41.

The later 5.1 standard therefore supplies a first-party standards-history statement:

```text
4.4
    -> 4.41 adds Background Operations + HPI
```

A contemporary JEDEC-announcement relay in EE Times places JESD84-A441 / eMMC 4.41 in May 2010 and describes host-controlled background processing as a way for the device to indicate that background flash clean-up is needed and for the host to allocate a convenient maintenance interval.

The date/publication report is supporting chronology. The normative feature-history statement comes from JEDEC Annex C.

### H2 — the standard distinguishes foreground service from background maintenance

JESD84-B51 §6.6.25 defines two categories:

```text
foreground operations
    = operations the host needs serviced, such as read/write

background operations
    = device operations executed while the host is not being serviced
```

The standard does not reduce background work to one named internal algorithm. It speaks generically of device maintenance operations.

This is important for Case 111 because `BKOPS` must not be silently normalized into `retention refresh`, `garbage collection`, or `wear leveling` unless a more specific source establishes that relation for the device under study.

### H3 — `BKOPS_STATUS` is a maintenance-obligation / urgency surface

The device reports background-operation status in `BKOPS_STATUS` as four levels:

```text
0x0  no operations required
0x1  operations outstanding — non-critical
0x2  operations outstanding — performance being impacted
0x3  operations outstanding — critical
```

The host is instructed to check the status periodically and start background operations as needed.

At the critical level, foreground operations may exceed their normal timeouts because maintenance can no longer be delayed.

Thus the standard exposes more than a binary capability bit:

```text
background-operation support
    != current maintenance debt
    != urgency of that debt
```

`URGENT_BKOPS` separately gives the host a fast exception-event indication for the higher urgency levels.

### H4 — manual start creates an explicit bounded maintenance run

For manually initiated work, the host writes `BKOPS_START`.

The standard says the device remains busy until **no more background processing is needed**.

That gives a host-visible run boundary:

```text
maintenance outstanding
    -> host admits a BKOPS run
    -> device busy
    -> run reaches the standard-defined completion condition
```

This is stronger than merely saying “the device is powered and may do something in the background.”

But the completion scope is still the standardized background-processing session/current need relation. The text does not say that every retention-sensitive cell has been rewritten or that every possible future maintenance obligation has disappeared.

### H5 — an admitted BKOPS run can be interrupted for foreground priority

§6.6.25 says foreground operations have higher priority and that an ongoing background operation may be interrupted by HPI.

§6.6.26 separately defines HPI as allowing a lower-priority operation to be interrupted before completion.

The interruptibility relation therefore matters:

```text
BKOPS started
    != BKOPS completed

maintenance admitted
    != uninterrupted maintenance execution
```

The 2010 and 2012 Linux-kernel discussions mirror this host-side control problem: the driver must decide when to start BKOPS and may use HPI when a new foreground request arrives.

That implementation evidence is consistent with, but does not replace, the standard.

### H6 — eMMC 5.1 also permits autonomous background-operation control

In JESD84-B51, `AUTO_EN` in `BKOPS_EN` permits the device to start or stop background operations during host-idle time without notifying the host each time.

The host is told to keep device power active when autonomous mode is enabled.

Annex C lists **Background Operation Control** among changes from 5.01 to 5.1.

This evidence supports only the bounded current-standard relation:

```text
host exposes an autonomous-maintenance opportunity
    -> device may choose start/stop timing
```

It does not establish that every detail of the 5.1 `AUTO_EN` behavior originated in precisely one committee change item, nor does it establish a commercial-device implementation.

### H7 — `PERIODIC_WAKEUP` turns maintenance opportunity into a host-visible cadence contract

The strongest Case-111-relevant evidence is §6.6.35.1.

The host may program `PERIODIC_WAKEUP` to indicate how often it will wake the device.

The host must then, at least as often as that configuration requires:

```text
Power up device
    -> execute at least one BKOPS_START background operation
    -> let that operation run to completion without interruption
    -> only then power the device down again
```

The standard additionally says the host must not leave the device powered down longer than the configured period.

The register itself can express wake-up units in:

- months;
- weeks;
- days;
- hours;
- minutes;
- or infinity / no wakeups.

This is a remarkably explicit maintenance-cadence interface:

```text
configured wake interval
    != merely elapsed calendar time

wake event
    != required maintenance run completed
```

The required maintenance run has its own completion condition.

### H8 — planned power removal has a separate completion authority

JESD84-B51 §6.6.36 defines Power Off Notification separately from BKOPS.

For `POWER_OFF_SHORT` or `POWER_OFF_LONG`, the host changes the notification state, waits for the busy line to de-assert, and only then may safely power off the device.

The same section also says `SLEEP_NOTIFICATION` can allow time for autonomous background operations before Sleep.

This means the standard exposes at least two distinct host-visible completion relations near a maintenance/power transition:

```text
BKOPS run complete
    != power-off preparation complete
```

The two may occur in the same operational sequence, but they are not the same authority.

---

## Engineering reconstruction

The following terms are project terms, not JEDEC historical vocabulary:

- `maintenance debt`;
- `maintenance urgency`;
- `maintenance admission`;
- `maintenance cadence`;
- `run-completion authority`;
- `power-removal authority`;
- `retention-specific completion authority`.

They permit a more precise decomposition:

```text
BKOPS capability
    != BKOPS debt / urgency
    != BKOPS execution admitted
    != BKOPS execution currently running
    != BKOPS run complete
    != power-off preparation complete
    != retention-specific coverage complete
    != future offline-retention guarantee
```

### E1 — cadence and completion are separate state relations

`PERIODIC_WAKEUP` is not itself evidence that maintenance happened.

It is a scheduling/obligation parameter.

The required BKOPS run adds an execution relation, and the no-more-background-processing-needed/busy-release condition adds a completion relation.

Thus:

```text
maintenance schedule retained/configured
    != scheduled work executed
    != work completed
```

### E2 — current “no operations required” is not a lifetime certificate

`BKOPS_STATUS = 0` answers the standardized current background-operation need question.

It should not be promoted into:

```text
all NAND cells freshly rewritten
all reclaim debt permanently absent
all future retention guaranteed
all future device maintenance unnecessary
```

Those stronger claims require additional device-specific evidence.

### E3 — foreground service can legitimately postpone maintenance

The combination of BKOPS priority rules and HPI means the maintenance system is intentionally preemptible.

Therefore a host/system can be functioning normally for foreground service while a maintenance obligation remains outstanding or repeatedly interrupted.

This is a useful counterexample to:

```text
normal I/O service
    -> therefore maintenance is complete
```

### E4 — the maintenance cadence does not identify the hidden maintenance mechanism

The standard intentionally abstracts device internals.

A periodic wake interval plus BKOPS completion can be authoritative for the **interface contract** while leaving the exact internal work unspecified.

That distinction is directly relevant to Case 111's unresolved target: a host-visible completion field tied specifically to retention refresh or whole-device data-retention maintenance.

---

## Functional comparisons

### Case 111 — enterprise-SSD extended shutdown

The useful functional analogy is:

```text
eMMC PERIODIC_WAKEUP
    -> interface-level configured wake cadence
    -> required maintenance run to completion

IBM / Dell extended-shutdown guidance
    -> operator/system-level calendar cadence
    -> powered maintenance opportunity / dwell
```

The two are **not** one historical lineage and not one mechanism.

Most importantly, eMMC gives a generic maintenance-run completion relation while the later enterprise-SSD evidence still lacks a named device-interface token explicitly bound to retention-refresh completion.

So this comparison sharpens rather than closes Case 111's P1 debt.

### Case 150 — managed-SSD garbage collection

eMMC 4.41-era Background Operations are useful prior art for host-visible managed-Flash cleanup/maintenance scheduling.

But:

```text
eMMC BKOPS
    != Crucial M550 Active Garbage Collection implementation
```

and:

```text
BKOPS run complete
    != M550 victim relocation complete
    != M550 mapping publication complete
    != M550 erase complete
```

No eMMC→M550 genealogy or controller-architecture identity is claimed.

### Case 135 — Micron automotive eMMC self-refresh

Case 135's later vendor-specific self-refresh path is useful precisely because it prevents over-reading generic BKOPS:

```text
generic background-maintenance completion
    != retention-specific refresh completion
```

Unless a named vendor/product source explicitly binds the two, they remain separate maintenance surfaces.

### Case 20 — shutdown/power-off state machines

There is a functional similarity between eMMC Power Off Notification and other storage-interface shutdown handshakes: both distinguish host shutdown intent from device-side completion/readiness.

No ATA/SCSI/NVMe/eMMC genealogy is asserted here.

---

## Historical record vs engineering reconstruction vs analogy vs interpretation

### Historical / standards record

The primary standard establishes:

- Background Operations and HPI entered the documented eMMC revision chain at 4.41;
- current 5.1 semantics include host-triggered BKOPS, urgency/status reporting, optional autonomous control, HPI interruption, periodic wake-up configuration, and separate Power Off Notification;
- `PERIODIC_WAKEUP` can require a power-up + uninterrupted BKOPS run to completion before power-down.

### Engineering reconstruction

This file reconstructs those mechanisms as separate:

- maintenance debt;
- urgency;
- execution admission;
- service-priority arbitration;
- run completion;
- cadence;
- power-removal admission.

JEDEC does not use this exact project vocabulary.

### Functional analogy

The comparisons to enterprise-SSD operator schedules, M550 GC, Micron automotive eMMC self-refresh, and storage shutdown handshakes compare **functions** only.

They do not establish ancestry or shared implementation.

### Philosophical interpretation

A narrow interpretation is permissible:

> a retained maintenance obligation can itself become part of the technical condition for making stored state reliably available later, even though that obligation is not the stored payload.

That observation must remain subordinate to the exact interface semantics above.

---

## Explicit non-claims

This slice does **not** claim that:

1. BKOPS was invented by JEDEC in 4.41;
2. the 4.41 committee record is a complete prior-art history;
3. every BKOPS operation is garbage collection;
4. every BKOPS operation is wear leveling;
5. every BKOPS operation is retention refresh;
6. every eMMC implementation performs the same hidden maintenance;
7. `BKOPS_STATUS = 0` proves that all data has been refreshed;
8. `BKOPS_STATUS = 0` proves future offline retention for any fixed interval;
9. one completed BKOPS run implies every stale physical NAND embodiment has been erased;
10. one completed BKOPS run implies sanitization;
11. `PERIODIC_WAKEUP` is a NAND-cell retention-time measurement;
12. the configured wake period is a deterministic failure deadline;
13. a host wakeup alone proves maintenance completion;
14. an HPI-interrupted BKOPS run has completed its intended maintenance obligation;
15. Power Off Notification completion is the same as BKOPS completion;
16. Power Off Notification completion is the same as application/filesystem durability;
17. the standard exposes internal victim selection, FTL map publication, erase order, or crash journal state;
18. the standard proves M550 firmware behavior;
19. the standard proves Seagate Pulsar retention-refresh behavior;
20. the standard proves Micron automotive eMMC self-refresh implementation details;
21. Linux's 2010/2012 host implementation choices are normative JEDEC semantics;
22. the EE Times article is a substitute for the normative standard;
23. a generic maintenance-completion token satisfies Case 111's open retention-specific telemetry target;
24. later eMMC revisions preserve every implementation detail identically across vendors.

---

## What this slice closes

It closes one bounded prior-art/control-surface question for Case 111:

> **By the eMMC 4.41→5.1 standards line, managed Flash had a host-visible maintenance-urgency surface, host-controlled/background maintenance admission, foreground preemption, and a later explicit periodic-wake contract that could require an uninterrupted background-maintenance run to completion before power-down.**

It also closes the narrower comparison:

```text
maintenance cadence can be interface-defined
    != maintenance completion is implicit
```

and:

```text
generic maintenance completion can be observable
    != retention-specific maintenance completion is thereby observable
```

---

## Open debt after this slice

Case 111 remains `grounded`; no maturity promotion follows.

The highest-value unresolved target remains:

> **a first-party named SSD/NVMe/SAS device interface in which a host-visible state is explicitly bound to completion or whole-device coverage of retention refresh / data-retention maintenance itself.**

This slice makes that target stricter:

- a generic `background work complete` bit/handshake is not enough;
- a generic scrub/BMS completion token is not enough;
- a maintenance wake-up schedule is not enough;
- the source must bind the completion evidence to the retention-maintenance obligation being claimed.

A secondary open question is whether a named commercial eMMC product documents the internal meaning of its BKOPS levels strongly enough to connect a specific `BKOPS_STATUS` transition to retention refresh, reclaim, wear leveling, or another individually named maintenance class.

That product/controller history should be coordinated with `tmzncty/computing-archaeology` rather than expanded here into a generic eMMC genealogy.

---

## Related-repository routing

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `BKOPS` found no dedicated reusable packet in this pass.

Therefore this file keeps only the retention-specific relation decomposition.

A broader history of:

- eMMC/MMC standards evolution;
- JEDEC proposal/ballot history;
- controller firmware architecture;
- mobile-storage product adoption;
- Linux MMC host-stack evolution;
- eMMC→UFS maintenance-interface genealogy;

belongs primarily in `computing-archaeology` if pursued.
