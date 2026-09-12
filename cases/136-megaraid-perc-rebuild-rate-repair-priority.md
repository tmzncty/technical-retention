# MegaRAID/PERC Rebuild Rate: Repair Priority, Service Competition, and Maintenance-Policy Persistence

## Status

**`grounded`** — bounded to publicly documented LSI MegaRAID / Dell PERC rebuild-rate semantics. This case does not claim a general history of RAID rebuild scheduling, exact controller bandwidth allocation, or failure-probability measurements.

Grounding records:

- [`../evidence/136-lsi-2006-dell-perc-rebuild-rate-grounding.md`](../evidence/136-lsi-2006-dell-perc-rebuild-rate-grounding.md) — rebuild-rate / maintenance-policy semantics;
- [`../evidence/136-dell-2013-2018-perc-puncture-source-readability-deepening.md`](../evidence/136-dell-2013-2018-perc-puncture-source-readability-deepening.md) — surviving-source unreadability, rebuild-with-errors, and RAID-puncture boundary.

## Scope

Case 17 already establishes RAID reconstruction as the work that recreates a failed member and restores redundancy margin. Case 136 asks a narrower question:

> Once repair is possible, what retained controller policy determines how aggressively the system spends service capacity on rebuilding, and how is that policy related to rebuild progress, array configuration, and foreground I/O?

The bounded LSI/Dell record exposes a `rebuild rate` control whose semantics are priority/resource allocation rather than a direct promise of wall-clock throughput. It also exposes two especially useful lifetime boundaries: the controller can restart a rebuild after a system reboot, while the configured rebuild rate is documented as unaffected by clearing the array configuration.

This case is **not**:

- a proof that every MegaRAID/PERC generation stores the setting in the same NVRAM field;
- a proof that an interrupted rebuild resumes from the exact previous stripe/progress offset;
- a quantitative model of time-to-rebuild or second-failure probability;
- a history of all RAID rebuild throttling algorithms;
- a claim that `30%` means exactly 30% of disk bandwidth, IOPS, elapsed time, or host-visible throughput;
- a treatment of secure deletion, media sanitization, or physical remanence.

## Historical record

### March 2006 — LSI MegaRAID exposes rebuild as user-scheduled background repair

LSI Logic's `MegaRAID Configuration Software User's Guide`, Version 2.0, document DB15-000269-01 (March 2006), describes automatic hot-spare rebuilds at **user-defined rebuild rates**. It states that if a system goes down during a rebuild, the controller automatically restarts the rebuild after reboot.

The same guide defines `Rebuild Rate` as the percentage of **compute cycles** dedicated to rebuilding failed drives. In this bounded manual:

- `0%` means rebuilding occurs only when the system is otherwise idle;
- `100%` gives rebuild higher priority than other system activity;
- LSI recommends avoiding both extremes;
- the default is `30%`.

This is a primary manufacturer floor for an explicit, host-configurable repair-priority control in this MegaRAID software generation. It is not invention priority for RAID rebuild throttling in general.

### The maintenance policy has a different lifetime from array configuration

The same 2006 guide later instructs operators to check each adapter's rebuild rate and states that the rebuild rate **is not affected when configuration is cleared**. Nearby text separately says array configuration is saved to controller NVRAM and to disks in the array.

The safe conclusion is relational, not a hidden-implementation claim:

> **rebuild-rate policy lifetime != array-configuration lifetime in this documented management regime.**

The guide does not identify the exact physical field that preserves the rate, so this case does not infer a specific NVRAM layout.

### One rate control can govern more than one maintenance task

The 2006 guide also says background initialization rate is controlled by the rebuild rate set in the BIOS Configuration Utility. A changed rate does not affect an already-running background initialization until that initialization is stopped and restarted.

This matters because the label `rebuild rate` does not by itself identify a unique repair object. In this software generation, the setting participates in more than one background-work scheduling path.

### Later Dell PERC documentation preserves the priority interpretation

Dell OpenManage Storage Management documentation describes the rebuild rate as a configurable `0%`–`100%` share of system resources dedicated to reconstructing failed physical disks. It explicitly warns that `0%` does **not** stop or pause a rebuild: it gives rebuild the lowest controller priority and the longest completion time. At `100%`, rebuild receives the highest priority and has the greatest impact on system performance.

Dell's PERC 9 guide adds a controller-specific scheduling detail: above `30%`, PERC modifies command allocation to prioritize rebuild operations when application I/O is consistent in the disk group.

Together these later product documents support a bounded continuity of the operational concept: the configured number expresses a controller scheduling/priority policy, not a literal guaranteed rebuild bandwidth.

## Retained states and relations

At least six states must remain separate:

1. **surviving RAID data/parity state** — the material from which the failed member is reconstructed;
2. **degraded/failed-member state** — the condition that creates a repair obligation;
3. **replacement/hot-spare eligibility** — whether a destination exists and may participate;
4. **rebuild task/progress state** — the work currently being performed or re-entered after interruption;
5. **rebuild-rate policy** — the controller scheduling/resource-allocation preference;
6. **array configuration** — membership/topology state describing the logical array.

The sources do not justify collapsing any pair into one object.

## Engineering reconstruction

### Rebuild rate != rebuild state

Changing a policy value does not itself recreate a failed member. The value determines how controller resources are prioritized while rebuild work exists.

> **repair policy != repair execution != restored redundancy.**

This extends Case 17's degraded/repaired distinction by adding a scheduler state between `repair is owed` and `repair is complete`.

### 0% priority != rebuild disabled

Dell explicitly states that a rebuild rate of 0% does not stop or pause the rebuild. LSI's earlier wording says work proceeds when the system is otherwise idle.

> **lowest maintenance priority != absence of maintenance obligation.**

A system can retain an owed repair while making its execution opportunistic.

### Nominal percentage != linear throughput guarantee

LSI defines the value in compute-cycle/priority terms; Dell describes system-resource allocation, and PERC 9 can change command-allocation strategy above 30% under a stated workload condition.

Therefore:

> **configured percentage != guaranteed fraction of disk bandwidth, IOPS, or elapsed time.**

The control is a scheduling policy exposed as a percentage. Its observed throughput depends on workload, controller behavior, drive performance, and other work.

### Rebooted rebuild != proven exact-progress checkpoint

LSI says the controller automatically restarts rebuilding after a system reboot. That demonstrates continuity of the **repair obligation / automatic repair regime** across this interruption.

It does not tell us whether the controller resumes from an exact stripe offset, reconstructs a progress map, or begins some work again.

> **automatic post-reboot rebuild != demonstrated exact progress-state persistence.**

### Array configuration clear != rebuild-rate reset

The 2006 management guide says clearing configuration does not affect rebuild rate.

> **configuration retirement != maintenance-policy retirement.**

This is a particularly useful retention boundary: a controller-level policy can outlive the logical storage configuration to which a particular rebuild episode belonged.

### Policy update != immediate effect on every active maintenance operation

For background initialization, the 2006 guide says changing rebuild rate does not affect the current operation until that operation is stopped and restarted.

> **stored policy value != necessarily current task's already-admitted scheduling regime.**

This claim is limited to the documented background-initialization path. The source does not establish identical latch/update semantics for an in-flight rebuild.

### Surviving-source readability can limit reconstruction even while rebuild continues

Dell's March 2013 OpenManage guide documents `A Rebuild Completes with Errors` for named PERC 4 controllers: a rebuild can report successful completion while damaged portions cannot be restored. The same guide says medium/bad-block damage discovered during rebuild or degraded operation can cross a recovery boundary that requires restoration from backup.

Dell's November 2018 PowerEdge troubleshooting guide makes the relation more explicit under `RAID puncture` / `rebuild with errors`. Its RAID 5 example starts with one failed/replacement member; if a surviving member has a data error in the same stripe when rebuild reaches it, remaining information is insufficient to reconstruct that stripe. PERC can puncture that stripe and let global rebuild continue.

The guide says puncturing can restore redundancy and return the array to `optimal` while the affected stripe remains lost. Therefore:

> **rebuild progress/completion != reconstructable coverage.**
>
> **redundancy restored / array optimal != complete payload integrity.**
>
> **rebuild rate / repair priority != surviving-source readability.**

Source readability is a constitutive repair input alongside replacement destination and admitted controller resources. More scheduling priority cannot reconstruct information the redundancy code no longer has.

A local unreadable region on a surviving member must also remain distinct from a second whole-device failure. Both can remove a contribution required by a stripe, but they differ in scope and failure object.

Dell says affected punctured data continues to produce uncorrectable errors when accessed and post-puncture Check Consistency does not resolve the existing loss. At project level this supports treating puncture as a retained **negative condition / error relation** on the affected logical extent. It does not identify an undocumented firmware field or where that relation is physically encoded.

### Rebuild urgency != payload correctness

A higher rate may reduce time spent degraded but can consume more foreground resources. A lower rate can protect service performance while leaving the system degraded longer.

The setting therefore mediates **when redundancy margin is restored**, not what the correct reconstructed bytes are. Data correctness still depends on surviving source state, parity/mirror semantics, drive/controller correctness, and any integrity checks.

## Relation to neighboring cases

### Case 17 — RAID parity reconstruction

Case 17 supplies the basic `degraded service -> reconstruction -> restored redundancy margin` mechanism. Case 136 inserts an operational control between trigger and completion:

```text
member failure
    -> repair owed
    -> destination available
    -> rebuild admitted
    -> controller resource-priority policy
    -> rebuild work
    -> redundancy restored
```

The comparison is direct within RAID, but Case 136 does not rewrite the historical RAID taxonomy of Case 17.

### Cases 18 / 101 / 102 — proactive integrity and media scans

The puncture evidence sharpens why proactive observation matters. A consistency check, scrub, medium scan, or patrol-read style operation can expose latent defects while enough redundancy remains to repair or retire them. After a separate member loss consumes redundancy margin, the same local unreadability can become unreconstructable.

This is a functional comparison only:

> **proactive integrity/readability maintenance != rebuild**, and Dell PERC Check Consistency is not thereby equivalent to ZFS scrub or another stack's checksum mechanism.

### Cases 94 / 96 — code margin and repair exposure

Case 94's RAID 6 P/Q example is a counterexample to universalizing Dell's RAID 5 example: code strength changes how many unavailable contributions a stripe can tolerate. Case 96 shows how faster reconstruction can reduce the interval spent degraded.

> **shorter repair exposure != proof that every surviving source region is readable**, and **RAID 5 failure geometry != RAID 6 failure geometry**.

### Case 131 — PERC foreign configuration

Case 131 asks whether topology/configuration can survive controller replacement and become admissible again. Case 136 shows the inverse-looking but separate boundary that one controller maintenance-policy value can survive a **configuration clear** in the bounded 2006 management interface.

> **topology retention != maintenance-policy retention.**

This is a functional comparison, not evidence that later PERC uses the same internal storage layout as 2006 MegaRAID.

## Failure and forgetting boundaries

A rebuild-capable array can still spend a long time degraded if repair is assigned low priority under sustained foreground work. Conversely, a high rebuild priority can reduce service headroom. The exposed control therefore changes the temporal competition between `continue serving now` and `restore redundancy sooner`.

The case also provides two negative controls:

- losing/clearing array configuration does not necessarily erase every controller policy setting;
- surviving a reboot as an automatic rebuild obligation does not prove preservation of exact prior rebuild progress.

Neither claim implies anything about secure erasure of old member contents.

## Prior art and anti-anachronism

The safe historical claim is narrow:

- by March 2006, LSI's MegaRAID management documentation publicly exposed a configurable `Rebuild Rate` with explicit priority/compute-cycle semantics and a 30% default.

This does **not** establish:

- the first RAID implementation of throttled rebuild;
- the first use of the phrase `rebuild rate`;
- genealogy from an earlier controller family to every later PERC generation;
- a universal 30% industry norm.

Broader RAID-controller scheduling history belongs primarily in `computing-archaeology` if developed.

## Philosophical interpretation — bounded

This case offers a narrow extension of the repository's maintenance thesis. Persistence after a failure can depend not only on whether repair is technically possible, but also on a retained policy that assigns **future machine time** to that repair relative to current service.

A cautious formulation is:

> technical continuation can depend on retained scheduling preferences that govern how quickly a damaged redundancy relation is reconstituted.

That is an engineering-derived interpretation. It is not LSI/Dell historical vocabulary, and it does not make every scheduler parameter a `memory` in a philosophical sense.

## Related-repository check

Fresh searches of `tmzncty/computing-archaeology` for `MegaRAID` and `rebuild rate` returned no dedicated overlapping study during this round.

Division of labor:

- `technical-retention`: rebuild priority as retained maintenance policy; policy/progress/configuration separation; cross-case retention comparison;
- `computing-archaeology`: broader RAID-controller genealogy, exact firmware algorithms, controller generations, benchmarks, and device-level reconstruction history.

## Open evidence debt

- earlier pre-2006 rebuild-throttling and pre-2013 rebuild-with-errors / puncture genealogy;
- exact persistence location and reset/default semantics of rebuild-rate policy on named controllers;
- whether in-flight rebuild progress resumes or restarts from an earlier checkpoint after power loss;
- controller-generation-specific telemetry and persistence mechanism for punctured/error locations;
- RAID 6 / multi-parity PERC behavior and cross-vendor handling of surviving-source unreadability;
- probabilistic/correlated URE models and measured rebuild-rate-to-throughput/risk curves;
- interaction among rebuild scheduling, patrol read/check consistency, cache policy, and media mix;
- current PERC 12/13 generation semantics and firmware-specific mutability;
- independent fault injection and second-failure/source-read-error exposure measurements.
