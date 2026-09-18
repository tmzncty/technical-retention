# MegaRAID/PERC Rebuild Rate: Repair Priority, Service Competition, and Maintenance-Policy Persistence

## Status

**`grounded`** — bounded to publicly documented MegaRAID / LSI / Dell PERC rebuild-rate and maintenance-continuation semantics. This case does not claim a general history of RAID rebuild scheduling, exact controller bandwidth allocation, or failure-probability measurements.

Grounding records:

- [`../evidence/136-megaraid-2000-2002-rebuild-policy-prior-art-deepening.md`](../evidence/136-megaraid-2000-2002-rebuild-policy-prior-art-deepening.md) — pre-2006 documentation floor for rebuild priority, restart-continuation policy, and policy lifetime across configuration clear;
- [`../evidence/136-lsi-2006-dell-perc-rebuild-rate-grounding.md`](../evidence/136-lsi-2006-dell-perc-rebuild-rate-grounding.md) — rebuild-rate / maintenance-policy semantics;
- [`../evidence/136-lsi-2006-flexraid-powerfail-maintenance-continuation-deepening.md`](../evidence/136-lsi-2006-flexraid-powerfail-maintenance-continuation-deepening.md) — named `FlexRAID PowerFail` cross-restart continuation policy for reconstruction, rebuild, and consistency-check work;
- [`../evidence/136-dell-2013-2018-perc-puncture-source-readability-deepening.md`](../evidence/136-dell-2013-2018-perc-puncture-source-readability-deepening.md) — surviving-source unreadability, rebuild-with-errors, and RAID-puncture boundary.

## Scope

Case 17 already establishes RAID reconstruction as the work that recreates a failed member and restores redundancy margin. Case 136 asks a narrower question:

> Once repair is possible, what retained controller policy determines how aggressively the system spends service capacity on rebuilding, and what retained control relation lets selected maintenance work continue after interruption?

The bounded MegaRAID/LSI/Dell record exposes a `rebuild rate` control whose semantics are priority/resource allocation rather than a direct promise of wall-clock throughput. It also exposes two especially useful lifetime boundaries: the controller can re-enter selected maintenance work after system restart through the named `FlexRAID PowerFail` policy, while the configured rebuild rate is documented as unaffected by clearing the array configuration.

This case is **not**:

- a proof that every MegaRAID/PERC generation stores the setting in the same NVRAM field;
- a proof that an interrupted rebuild resumes from the exact previous stripe/progress offset;
- a quantitative model of time-to-rebuild or second-failure probability;
- a history of all RAID rebuild throttling algorithms;
- a claim that `30%` means exactly 30% of disk bandwidth, IOPS, elapsed time, or host-visible throughput;
- a claim that `FlexRAID PowerFail` uses one specific hidden progress-checkpoint format;
- a treatment of secure deletion, media sanitization, or physical remanence.

## Historical record

### April 2000 — MegaRAID documentation already exposes user-defined rebuild priority

The preliminary *MegaRAID Express 500 Hardware Guide*, MAN-475 dated 14 April 2000, describes automatic rebuild with **user-definable rebuild rates**. It defines rebuild rate as the fraction of compute cycles devoted to rebuilding failed drives:

- `0%` means rebuilding occurs only while the system is otherwise idle;
- `100%` gives rebuilding higher priority than other system activity.

The guide also says a rebuild is restarted if the system goes down during rebuild.

Because the surviving guide is explicitly marked `Preliminary Draft`, it is evidence of published manufacturer documentation/design state, not by itself proof of a particular shipping-firmware behavior on that date.

### July 2000 — priority, continuation, and configuration lifetime are already separate management relations

The *MegaRAID RAID Controller Configuration Software Guide*, MAN-MR-GENSW dated 20 July 2000, exposes `Rebuild Rate` and `FlexRAID PowerFail` as separate adapter properties. Its Power Console Plus description treats rebuild rate as the amount of system resources devoted to failed-drive rebuild; a higher setting leaves fewer resources for ordinary RAID operations. The same guide describes `FlexRAID PowerFail` as allowing drive reconstruction to continue when the system restarts after a power failure.

Operational guidance in the same document says that rebuild rate **is not affected when configuration is cleared**.

This pushes three Case 136 relations earlier than the former 2006 documentation floor:

```text
while maintenance runs:
    Rebuild Rate -> how aggressively maintenance competes for resources

after interruption:
    FlexRAID PowerFail -> whether documented reconstruction continues after restart

across configuration retirement:
    clear array configuration -/-> rebuild-rate policy necessarily cleared
```

The manual does not disclose the exact physical storage of either property or the exact rebuild-progress representation.

See [`136-megaraid-2000-2002-rebuild-policy-prior-art-deepening.md`](../evidence/136-megaraid-2000-2002-rebuild-policy-prior-art-deepening.md).

### August 2002 — LSI SCSI 320-1 preserves the same broad rebuild-rate semantics

LSI Logic's *MegaRAID SCSI 320-1 Hardware Guide*, MAN-520 dated 16 August 2002 and marked `Initial release`, independently documents user-definable rebuild rates, the same `0%` idle-only / `100%` higher-priority endpoints, and `User-specified rebuild rate: Yes` among controller features.

This strengthens the historical claim from a single preliminary 2000 document to a repeated MegaRAID operator concept before 2006. It does **not** prove the same scheduler implementation, firmware code, persistence field, or uninterrupted product genealogy.

### March 2006 — LSI MegaRAID preserves rebuild as user-scheduled background repair

LSI Logic's `MegaRAID Configuration Software User's Guide`, Version 2.0, document DB15-000269-01 (March 2006), describes automatic hot-spare rebuilds at **user-defined rebuild rates**. It states that if a system goes down during a rebuild, the controller automatically restarts the rebuild after reboot.

The same guide defines `Rebuild Rate` as the percentage of **compute cycles** dedicated to rebuilding failed drives. In this bounded manual:

- `0%` means rebuilding occurs only when the system is otherwise idle;
- `100%` gives rebuild higher priority than other system activity;
- LSI recommends avoiding both extremes;
- the default is `30%`.

This remains a strong later manufacturer witness, but it is no longer the earliest directly checked documentation floor for the operator-visible repair-priority concept in this case.

### March 2006 — `FlexRAID PowerFail` broadens the documented restart classes

The same manual's BIOS Configuration Utility lists a named `FlexRAID PowerFail` option that allows drive reconstruction to continue when the system restarts after a power failure. The WebBIOS Adapter Properties table is broader: it says the feature allows **drive reconstruction, rebuild, or check consistency** to continue after a **power failure, reset, or hard boot**, and documents the default as `Enabled`.

This supports:

> **maintenance priority != cross-restart maintenance continuation.**

It also supports a bounded terminology warning:

> **`PowerFail` product label != power-removal-only interruption semantics**, because the 2006 WebBIOS description explicitly includes reset and hard boot.

The manual does **not** disclose whether reconstruction resumes at the exact previous stripe/LBA, how much work can be replayed, or where the relevant progress representation is physically retained. The source-level deepening is therefore about **maintenance-task continuity**, not an inferred exact-progress checkpoint.

See [`136-lsi-2006-flexraid-powerfail-maintenance-continuation-deepening.md`](../evidence/136-lsi-2006-flexraid-powerfail-maintenance-continuation-deepening.md).

### The maintenance policy has a different lifetime from array configuration

Both the July 2000 configuration guide and the March 2006 guide instruct operators to check each adapter's rebuild rate and state that the rebuild rate **is not affected when configuration is cleared**. The 2006 guide separately says array configuration is saved to controller NVRAM and to disks in the array.

The safe conclusion is relational, not a hidden-implementation claim:

> **rebuild-rate policy lifetime != array-configuration lifetime in this documented management regime.**

The inspected guides do not identify the exact physical field that preserves the rate, so this case does not infer a specific NVRAM layout.

### One rate control can govern more than one maintenance task

The 2006 guide also says background initialization rate is controlled by the rebuild rate set in the BIOS Configuration Utility. A changed rate does not affect an already-running background initialization until that initialization is stopped and restarted.

This matters because the label `rebuild rate` does not by itself identify a unique repair object. In this software generation, the setting participates in more than one background-work scheduling path.

### Later Dell PERC documentation preserves the priority interpretation

Dell OpenManage Storage Management documentation describes the rebuild rate as a configurable `0%`–`100%` share of system resources dedicated to reconstructing failed physical disks. It explicitly warns that `0%` does **not** stop or pause a rebuild: it gives rebuild the lowest controller priority and the longest completion time. At `100%`, rebuild receives the highest priority and has the greatest impact on system performance.

Dell's PERC 9 guide adds a controller-specific scheduling detail: above `30%`, PERC modifies command allocation to prioritize rebuild operations when application I/O is consistent in the disk group.

Together these product documents support a bounded continuity of the operational concept: the configured number expresses a controller scheduling/priority policy, not a literal guaranteed rebuild bandwidth.

## Retained states and relations

At least seven states must remain separate:

1. **surviving RAID data/parity state** — the material from which the failed member is reconstructed;
2. **degraded/failed-member state** — the condition that creates a repair obligation;
3. **replacement/hot-spare eligibility** — whether a destination exists and may participate;
4. **rebuild task/progress state** — the work currently being performed or re-entered after interruption;
5. **rebuild-rate policy** — the controller scheduling/resource-allocation preference;
6. **cross-restart maintenance-continuation policy** — the bounded `FlexRAID PowerFail` relation governing whether documented reconstruction/rebuild/check-consistency work continues after selected restart classes;
7. **array configuration** — membership/topology state describing the logical array.

The sources do not justify collapsing any pair into one object.

## Engineering reconstruction

### Rebuild rate != rebuild state

Changing a policy value does not itself recreate a failed member. The value determines how controller resources are prioritized while rebuild work exists.

> **repair policy != repair execution != restored redundancy.**

This extends Case 17's degraded/repaired distinction by adding a scheduler state between `repair is owed` and `repair is complete`.

### 0% priority != rebuild disabled

The 2000 and 2002 MegaRAID hardware guides explicitly describe 0% as idle-only rebuild; later Dell documentation likewise says 0% does not stop or pause the rebuild.

> **lowest maintenance priority != absence of maintenance obligation.**

A system can retain an owed repair while making its execution opportunistic.

### Nominal percentage != linear throughput guarantee

Early MegaRAID manuals define the value in compute-cycle/resource-priority terms; Dell describes system-resource allocation, and PERC 9 can change command-allocation strategy above 30% under a stated workload condition.

Therefore:

> **configured percentage != guaranteed fraction of disk bandwidth, IOPS, or elapsed time.**

The control is a scheduling policy exposed as a percentage. Its observed throughput depends on workload, controller behavior, drive performance, and other work.

### Cross-restart continuation policy != exact progress checkpoint

MegaRAID documentation says the controller restarts or continues reconstruction after documented restart conditions. The 2000 and 2006 configuration guides expose `FlexRAID PowerFail` as a distinct continuation control.

This demonstrates continuity of the **maintenance obligation / task regime** across the documented interruption classes.

It still does not tell us whether the controller resumes from an exact stripe offset, reconstructs a bitmap, stores only a coarse percentage/frontier, or repeats some prior work.

> **maintenance-task continuity != demonstrated exact progress-state persistence.**

and:

> **restart continuation != exactly-once maintenance execution.**

A named cross-restart policy is stronger evidence than a bare verb such as `restarts`, but it is not a license to invent an undocumented checkpoint representation.

### Rebuild priority != restart continuity

`Rebuild Rate` and `FlexRAID PowerFail` appear as separate adapter properties in the July 2000 management guide and remain separately represented in later MegaRAID documentation.

They answer different questions:

- `Rebuild Rate`: how much priority/resource share should the task receive while running?
- `FlexRAID PowerFail`: should the documented maintenance work continue after selected restart events?

Therefore:

> **maintenance scheduling aggressiveness != interruption-continuation policy.**

### Shared continuation policy != identical maintenance semantics

The 2006 WebBIOS description spans reconstruction, rebuild, and check consistency. That shared continuation feature does not make those maintenance operations identical.

> **one continuation policy can govern multiple task classes without collapsing verification and reconstruction into one mechanism.**

### Array configuration clear != rebuild-rate reset

The July 2000 and March 2006 management guides say clearing configuration does not affect rebuild rate.

> **configuration retirement != maintenance-policy retirement.**

This is a particularly useful retention boundary: a controller-level policy can outlive the logical storage configuration to which a particular rebuild episode belonged.

The inspected sources do not establish the corresponding clear/default lifetime of `FlexRAID PowerFail`, so the persistence horizons of those two controller properties must not be assumed identical.

### Policy update != immediate effect on every active maintenance operation

For background initialization, the 2006 guide says changing rebuild rate does not affect the current operation until that operation is stopped and restarted.

> **stored policy value != necessarily current task's already-admitted scheduling regime.**

This claim is limited to the documented background-initialization path. The source does not establish identical latch/update semantics for an in-flight rebuild.

### Same label across generations != same hidden implementation

The 2000 Express 500, 2002 SCSI 320-1, 2006 MegaRAID, and later Dell/PERC materials expose closely related operator concepts. That supports a documentation-level continuity of rebuild-priority semantics.

It does not prove a single scheduler implementation, one firmware lineage, one persistent field, or identical percentage accounting across those generations.

> **interface-semantic continuity != demonstrated implementation identity.**

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

Case 17 supplies the basic `degraded service -> reconstruction -> restored redundancy margin` mechanism. Case 136 inserts both scheduling and interruption-continuation controls between trigger and completion:

```text
member failure
    -> repair owed
    -> destination available
    -> rebuild admitted
    -> controller resource-priority policy
    -> rebuild work
    -> interruption
    -> cross-restart continuation policy
    -> rebuild work re-entered
    -> redundancy restored
```

The comparison is direct within RAID, but Case 136 does not rewrite the historical RAID taxonomy of Case 17.

### Case 83 — HDFS BlockScanner cursor checkpointing

Case 83 exposes a maintenance traversal with a concrete saved cursor and a fallback to a fresh iterator if that cursor cannot be loaded. The MegaRAID sources instead expose the **policy and behavior of task continuation** but not the exact progress representation.

> **explicit maintenance continuation != disclosed maintenance-progress checkpoint format.**

This is a functional control-state comparison, not genealogy.

### Case 148 — NVMe Device Self-test

Case 148 separately models a standardized background diagnostic operation, progress/result state, and specified reset/power behavior. MegaRAID's earlier vendor-specific `FlexRAID PowerFail` shows that selected maintenance continuation across restart can also be exposed as a controller-management property.

This is a functional analogy only; it is not a claim that NVMe Device Self-test descends from MegaRAID.

### Cases 18 / 101 / 102 — proactive integrity and media scans

The puncture evidence sharpens why proactive observation matters. A consistency check, scrub, medium scan, or patrol-read style operation can expose latent defects while enough redundancy remains to repair or retire them. After a separate member loss consumes redundancy margin, the same local unreadability can become unreconstructable.

This is a functional comparison only:

> **proactive integrity/readability maintenance != rebuild**, and Dell PERC Check Consistency is not thereby equivalent to ZFS scrub or another stack's checksum mechanism.

### Cases 94 / 96 — code margin and repair exposure

Case 94's RAID 6 P/Q example is a counterexample to universalizing Dell's RAID 5 example: code strength changes how many unavailable contributions a stripe can tolerate. Case 96 shows how faster reconstruction can reduce the interval spent degraded.

> **shorter repair exposure != proof that every surviving source region is readable**, and **RAID 5 failure geometry != RAID 6 failure geometry**.

### Case 131 — PERC foreign configuration

Case 131 asks whether topology/configuration can survive controller replacement and become admissible again. Case 136 shows the inverse-looking but separate boundary that one controller maintenance-policy value can survive a **configuration clear** in the bounded 2000 and 2006 MegaRAID management interfaces.

> **topology retention != maintenance-policy retention.**

This is a functional comparison, not evidence that later PERC uses the same internal storage layout as an early MegaRAID controller.

## Failure and forgetting boundaries

A rebuild-capable array can still spend a long time degraded if repair is assigned low priority under sustained foreground work. Conversely, a high rebuild priority can reduce service headroom. The exposed control therefore changes the temporal competition between `continue serving now` and `restore redundancy sooner`.

The `FlexRAID PowerFail` evidence adds a different failure boundary: the documented restart event need not end the maintenance obligation. The controller can retain enough relation to continue documented maintenance after restart. But the sources do not prove that exact micro-progress, every intermediate read result, or every prior reconstructed stripe is represented as a durable checkpoint.

The case therefore provides three negative controls:

- losing/clearing array configuration does not necessarily erase every controller policy setting;
- cross-restart maintenance continuity does not prove preservation of exact prior rebuild progress;
- a continuation policy does not erase the distinction between policy state and maintenance execution.

None of these claims implies anything about secure erasure of old member contents.

## Prior art and anti-anachronism

The safe historical claim is now narrower and earlier:

- by 14 April 2000, a preliminary MegaRAID Express 500 hardware guide publicly described user-definable rebuild rates with explicit idle-only / high-priority endpoints;
- by 20 July 2000, MegaRAID configuration-software documentation exposed `Rebuild Rate` and `FlexRAID PowerFail` as separate adapter properties and stated that clearing configuration did not affect rebuild rate;
- by 16 August 2002, an LSI Logic SCSI 320-1 initial-release guide independently preserved the same broad 0%–100% rebuild-priority semantics;
- by March 2006, LSI documentation additionally gives the 30% default and broader WebBIOS continuation wording used elsewhere in this case.

This does **not** establish:

- the first RAID implementation of throttled rebuild;
- the first use of the phrase `rebuild rate`;
- that the feature already existed in every pre-2000 revision listed in the 2000 software guide's revision history;
- invention priority for cross-restart RAID maintenance or rebuild checkpoints;
- genealogy from an earlier controller family to every later PERC generation;
- a universal 30% industry norm.

Broader RAID-controller scheduling and restart-continuation history belongs primarily in `computing-archaeology` if developed.

## Philosophical interpretation — bounded

This case offers a narrow extension of the repository's maintenance thesis. Persistence after a failure can depend not only on whether repair is technically possible, but also on retained policy that assigns **future machine time** to repair and retained control relation that allows unfinished maintenance to remain an obligation after restart.

A cautious formulation is:

> technical continuation can depend on retained scheduling and continuation preferences that govern how damaged or unchecked redundancy relations are reconstituted across time and interruption.

That is an engineering-derived interpretation. It is not MegaRAID/LSI/Dell historical vocabulary, and it does not make every scheduler or restart parameter a `memory` in a philosophical sense.

## Related-repository check

Fresh searches of `tmzncty/computing-archaeology` for exact early-source terms including `MegaRAID SCSI 320-1` and `MAN-MR-GENSW FlexRAID PowerFail` returned no dedicated overlapping study during this round.

Division of labor:

- `technical-retention`: rebuild priority as retained maintenance policy; interruption-continuation policy; policy/progress/configuration separation; cross-case retention comparison;
- `computing-archaeology`: broader MegaRAID/RAID-controller genealogy, ownership/product evolution, exact firmware algorithms, controller generations, progress-checkpoint representation, benchmarks, and device-level reconstruction history.

## Open evidence debt

- pre-2000 direct product/manual evidence and cross-vendor rebuild-priority controls;
- exact persistence location and reset/default semantics of rebuild-rate and `FlexRAID PowerFail` policy on named controllers;
- whether in-flight rebuild resumes from an exact progress checkpoint or replays a bounded region after power loss;
- controller-generation-specific telemetry and persistence mechanism for punctured/error locations;
- RAID 6 / multi-parity PERC behavior and cross-vendor handling of surviving-source unreadability;
- probabilistic/correlated URE models and measured rebuild-rate-to-throughput/risk curves;
- interaction among rebuild scheduling, patrol read/check consistency, cache policy, and media mix;
- current PERC 12/13 generation semantics and firmware-specific mutability;
- independent power-cut/fault injection measuring both task continuity and progress continuity after interruption.
