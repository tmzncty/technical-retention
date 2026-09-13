# Evidence 150C — Crucial Active Garbage Collection: powered-idle maintenance opportunity and host power-policy gating

## Status

**Deepening record for Case 150.**

Target case: [`../cases/150-crucial-m550-active-garbage-collection.md`](../cases/150-crucial-m550-active-garbage-collection.md)

Parent grounding: [`150-crucial-2014-2024-active-garbage-collection-grounding.md`](150-crucial-2014-2024-active-garbage-collection-grounding.md)

Earlier Micron prior-art deepening: [`150-micron-2011-ftl-garbage-collection-prior-art-deepening.md`](150-micron-2011-ftl-garbage-collection-prior-art-deepening.md)

## Research question

Crucial's maintained support material already says Active Garbage Collection (ACG) operates when an SSD is powered but not actively reading or writing. What additional retention boundary becomes visible when the same first-party support procedure tells the operator to preserve that powered-idle interval through host power-management settings?

The narrow answer is:

> **Host inactivity is not by itself a maintenance opportunity. The vendor's operational procedure requires the SSD to remain powered and available while foreground I/O is absent, and it explicitly changes host power-management policy to preserve that condition.**

This is an operational / maintenance-opportunity deepening. It is **not** a reconstruction of M550 firmware, SATA DEVSLP semantics, NVMe controller power states, a garbage-collection completion timer, or a universal SSD policy.

---

## Source ledger

### P1 — Crucial maintained support article — first-party current family guidance — `H/P`

Crucial Support, **"Mi SSD solía ser mucho más rápida, pero recientemente va más lenta… ¿Qué ha pasado?"**:

<https://www.crucial.es/support/articles-faq-ssd/ssd-used-to-be-faster-but-has-slowed-down>

The inspected first-party page states that:

- Crucial SSDs have Active Garbage Collection integrated into the SSD controller;
- ACG performs background cleanup while the SSD has power but is not actively reading or writing;
- idle periods are required for ACG to run;
- available empty space is also required for the cleanup/data-movement process;
- for best results, Crucial recommends keeping at least **10%** of the SSD free;
- if performance has degraded, Crucial's procedure is to leave the SSD **powered and idle for 6–8 hours**, for example by leaving a PC in BIOS/UEFI or a Mac at the Startup Manager;
- Crucial then recommends power settings that keep the SSD powered during host sleep: for SATA, the Windows disk power-off setting should be `Never`; for NVMe, PCIe `Link State Power Management` should be `Off`; on macOS, the option to put disks to sleep when possible should be disabled.

The page footer is ©2024 Micron Technology, Inc. The page is used as a maintained Crucial family-level operational contract, not as a 2014 M550 firmware trace.

### P2 — existing 2014 M550 product grounding — inherited context

The parent grounding record retains the 29-Jan-2014 M550 product flyer and 18-Mar-2014 Micron availability announcement. Those sources establish that M550 publicly listed `Active Garbage Collection` and `TRIM support` as product features.

They are not re-read here to infer the quantitative 6–8 hour procedure or the modern host power settings.

### P3 — Micron TN-29-60 (2011) — inherited functional prior art

[`150-micron-2011-ftl-garbage-collection-prior-art-deepening.md`](150-micron-2011-ftl-garbage-collection-prior-art-deepening.md) already records Micron's April-2011 SLC FTL note describing select/copy/erase garbage collection and an optional background feature during system idle time, with a power-consumption trade-off.

This supplies a pre-M550 functional-prior-art floor. It does not establish direct genealogy from that note to M550 or to Crucial's maintained support procedure.

---

## Historical record

### H/P — vendor guidance couples inactivity with continued device power

Crucial's current support language is not merely “wait while the host is quiet.” It explicitly requires the SSD to have power while it is not actively reading/writing. The recovery procedure is constructed to hold the system in a state such as BIOS/UEFI where the SSD remains powered but ordinary storage activity is absent.

The historical/current vendor record therefore directly supports the operational conjunction:

```text
foreground I/O absent
    +
SSD remains powered
    ->
ACG is given an execution opportunity
```

It does **not** support the stronger statement that every such interval necessarily causes a particular GC pass to start or finish.

### H/P — the 6–8 hour interval is an operator procedure, not a firmware SLA

Crucial recommends leaving a degraded-performing SSD powered and idle for **6–8 hours** and then rebooting/power cycling. That is a concrete runbook duration.

The source does not expose:

- a firmware countdown equal to 6 or 8 hours;
- a maximum completion time;
- the amount of data guaranteed to be relocated in that window;
- a completion flag proving all reclaimable blocks were processed;
- whether the recommendation is identical across all Crucial SSD generations.

Therefore:

> **6–8 h recommended opportunity window != 6–8 h garbage-collection completion bound.**

### H/P — host power policy can preserve or withdraw the recommended opportunity

The same Crucial page tells Windows users to prevent SATA disk power-off and to disable PCIe Link State Power Management for NVMe, and tells Mac users not to put disks to sleep when possible. The stated purpose is to keep the SSD powered so ACG can run during otherwise idle/sleep periods.

This gives a concrete cross-layer operational fact: a host can be “idle” in the human/application sense while a power-management transition removes the device condition the vendor asks operators to preserve for background maintenance.

The safe statement is:

> **host inactivity != guaranteed device maintenance opportunity.**

Do not infer from this general support procedure that any specific SATA DEVSLP, HIPM/DIPM, APST, or NVMe power-state transition has a particular undocumented ACG behavior.

### H/P — free-capacity guidance is a recommendation, not a published controller threshold

Crucial says available empty space is needed because cleanup involves moving data and recommends keeping at least **10%** free for best results.

That establishes a vendor operational recommendation. It does **not** establish that `10%` is:

- an exact firmware trigger;
- a hard lower bound below which GC cannot execute;
- the M550's over-provisioning ratio;
- a universal SSD rule.

Therefore:

> **10% free-space recommendation != exact GC scheduler threshold.**

---

## Engineering reconstruction

The first-party procedure supports a useful state decomposition:

```text
I_host = host has no foreground storage activity
P_dev  = SSD remains powered / available under host power policy
W_gc   = controller has a maintenance opportunity
C_gc   = relevant garbage-collection work has completed
```

The bounded engineering relation is:

```text
I_host + P_dev
    may provide
W_gc

W_gc
    !=
C_gc
```

`I_host` by itself is insufficient to characterize the opportunity because host power policy can remove `P_dev`. Conversely, maintaining `P_dev` does not mean that foreground I/O is absent, and a powered busy device may not have the idle opportunity described by Crucial's support path.

### E — “idle” is a cross-layer word

At least four different states can be hidden behind everyday use of `idle`:

1. the user is not interacting with the system;
2. the OS is not issuing foreground storage I/O;
3. the host permits the SSD to remain powered / link-available;
4. the controller actually schedules background maintenance.

The Crucial procedure matters because it prevents those states from being collapsed into one. A host can look idle to the user while power management has put the device into a condition outside the vendor's recommended ACG opportunity.

### E — maintenance opportunity is neither maintenance demand nor completion

Case 150 already distinguishes stale-page/reclamation pressure from the later copy/erase work. This deepening adds a scheduling boundary:

```text
reclamation debt / pressure
    !=
powered-idle opportunity
    !=
GC execution
    !=
GC completion
```

The 6–8 hour runbook is evidence for reserving opportunity, not evidence that the controller exposes a durable “all GC complete” state at the end of that interval.

### E — host power-management policy participates without owning the reclaim algorithm

The host can help create or destroy an execution window, but the inspected Crucial source still describes ACG as integrated in the SSD controller.

Thus:

```text
host: preserves an operating opportunity
controller: owns hidden reclamation scheduling/mechanics
```

This is a cross-layer control relation, not evidence that the OS selects victim blocks or directly moves NAND pages.

---

## Cross-case comparison

### Case 135 — Micron automotive eMMC self-refresh

Case 135 documents a different managed-Flash maintenance path: the host supplies reset/time conditions, then the eMMC waits for bus idleness and a configured delay before controller-local self-refresh work. Case 150C documents a consumer-SSD support procedure in which the host preserves powered idleness so controller-local ACG has an opportunity to run.

The functional similarity is bounded:

> **device-local maintenance can depend on a host-created service opportunity even when the host does not select the physical maintenance target.**

The mechanisms are not equated. Case 135 has a documented reset/time command window, ECC-threshold selection, and eMMC-specific telemetry; Case 150 does not expose those semantics. No genealogy or shared firmware implementation is claimed.

### Case 111 — enterprise SSD extended-shutdown maintenance

Case 111 likewise treats powered maintenance time as an operational resource. The comparison is functional only: operator/host scheduling can reserve time in which hidden controller maintenance proceeds. It does not establish identical trigger logic or retention mechanisms across product families.

---

## Explicit non-claims / stop conditions

This evidence does **not** establish:

1. **M550-specific 6–8 hour behavior.** The quantitative procedure comes from maintained Crucial family guidance, not a 2014 M550 firmware trace.
2. **A 10% firmware constant.** Ten percent is vendor operational guidance for best results, not an observed scheduler threshold.
3. **A completion SLA.** Six to eight hours is a recommended powered-idle opportunity, not a guaranteed GC deadline.
4. **Specific low-power-state semantics.** The source does not expose SATA DEVSLP/HIPM/DIPM or NVMe APST/controller-state internals.
5. **Idle-only garbage collection.** The support path explains idle-time ACG; it does not prove that urgent/foreground reclamation never occurs.
6. **Crash atomicity or restart semantics.** Nothing here reveals mapping-commit order, journals, checkpoints, scan recovery, or retry state.
7. **Sanitization.** Performance-oriented reclamation is not a verified secure-purge mechanism.
8. **Direct genealogy.** Similar idle/power opportunity relations in Micron TN-29-60, Case 111, or Case 135 do not prove design descent.

---

## Related-repository check

A fresh code search in `tmzncty/computing-archaeology` for `active garbage collection` returned no dedicated reusable study. Broader SSD background-maintenance history, SATA/NVMe power-state genealogy, controller lineages, and early commercial GC scheduling remain better candidates for that companion repository if pursued.

This record therefore keeps only the bounded retention relation:

> **maintenance opportunity can depend on preserving a device-level powered-idle condition across a host/device boundary, while neither that opportunity nor its duration proves maintenance completion.**

---

## Follow-on debt

1. Find a contemporaneous 2010–2014 Crucial/Micron support or service document that gives M550-era idle/power operational guidance directly.
2. Obtain device traces that distinguish host I/O quiescence, device/link power state, background NAND writes, and reclaimed free space on a named SSD.
3. Find first-party firmware/controller documentation exposing whether and how a partially completed GC pass survives specific power-state transitions or power failure.
4. Keep broad power-management and SSD-GC history in `computing-archaeology`; retain only the maintenance-opportunity/currentness relation here.
