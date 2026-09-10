from pathlib import Path

CASE = Path("cases/136-megaraid-perc-rebuild-rate-repair-priority.md")
EVID = Path("evidence/136-lsi-2006-dell-perc-rebuild-rate-grounding.md")

CASE.write_text(r'''# MegaRAID/PERC Rebuild Rate: Repair Priority, Service Competition, and Maintenance-Policy Persistence

## Status

**`grounded`** — bounded to publicly documented LSI MegaRAID / Dell PERC rebuild-rate semantics. This case does not claim a general history of RAID rebuild scheduling, exact controller bandwidth allocation, or failure-probability measurements.

Grounding record: [`../evidence/136-lsi-2006-dell-perc-rebuild-rate-grounding.md`](../evidence/136-lsi-2006-dell-perc-rebuild-rate-grounding.md).

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

### Cases 18 / 102 — scrub and patrol read

Scrub/patrol read govern proactive discovery/verification work; rebuild rate governs reconstruction after a member-loss repair obligation exists. Both consume background service capacity, but:

> **integrity-scan scheduling != rebuild scheduling.**

The 2006 MegaRAID guide itself helps keep this distinction visible by separately naming patrol read, consistency check, background initialization, and rebuild even where some controller-rate controls are reused.

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

- earlier pre-2006 RAID-controller rebuild-throttling genealogy;
- exact persistence location and reset/default semantics of the rebuild-rate property on named controllers;
- whether in-flight rebuild progress resumes or restarts from an earlier checkpoint after power loss on named MegaRAID/PERC generations;
- measured rebuild-rate-to-throughput mapping under controlled foreground workloads;
- rebuild-rate interaction with URE handling, patrol read, consistency check, cache policy, and SSD/HDD media mix;
- current PERC 12/13 generation semantics and firmware-specific mutability;
- fault injection and second-failure exposure measurements.
''', encoding="utf-8")

EVID.write_text(r'''# Evidence 136 — LSI MegaRAID / Dell PERC Rebuild-Rate Scheduling and Policy Lifetime

## Scope

This record grounds one bounded relation:

> RAID reconstruction can be governed by a separately retained controller scheduling policy whose lifetime and semantics are not identical to rebuild progress, array configuration, or a literal bandwidth quota.

The record does not claim invention priority for rebuild throttling, a universal controller implementation, or quantitative reliability benefits for any particular percentage.

## Source 1 — LSI Logic, `MegaRAID Configuration Software User's Guide`, Version 2.0, March 2006

**Type:** manufacturer-primary product/software manual (`H/P`)

- Document: `DB15-000269-01`
- Edition: Second Edition / Version 2.0, March 2006
- Current first-party-successor host: Broadcom documentation
- URL: https://docs.broadcom.com/doc/12353347

The title page identifies LSI Logic Corporation, the document number, March 2006 date, and states that the manual is the primary reference for the MegaRAID software tools/utilities.

### Locator A — §2.4.13 `Disk Rebuilds`, printed p. 2-11 (PDF p. 32)

The manual says a failed physical drive can be rebuilt by recreating its data; the controller can use hot spares automatically and transparently at user-defined rebuild rates. If the system goes down during a rebuild, the controller automatically restarts the rebuild after reboot.

**Supported historical claims:**

- rebuild is an explicit controller-managed repair operation;
- it can be automatically triggered when a suitable hot spare is available;
- the repair regime can be re-entered automatically after a system reboot.

**Not supported:**

- exact progress offset survives reboot;
- the rebuild performs a secure erase of the failed drive;
- all RAID levels/controllers use this mechanism.

### Locator B — §2.4.13.1 `Rebuild Rate`, printed p. 2-12 (PDF p. 33)

The manual defines rebuild rate as the percentage of **compute cycles** dedicated to rebuilding failed drives. It states:

- 0%: rebuild occurs only if the system is not doing anything else;
- 100%: rebuild has higher priority than other system activity;
- LSI recommends not using 0% or 100%;
- default: 30%.

**Supported relation:**

> `rebuild rate` is a priority/resource-scheduling control, not direct evidence of a fixed physical transfer rate.

### Locator C — §2.4.6 `Background Initialization`, printed p. 2-4/2-5 (PDF p. 25)

The manual says background initialization is an automatic consistency-check-like operation on newly created logical drives and that its rate is controlled by the rebuild-rate setting. It further states that changing the rebuild rate does not affect a running background initialization until BGI is stopped and restarted.

**Supported relations:**

- a setting labeled `rebuild rate` can govern another background maintenance path;
- stored policy update can be distinct from the scheduling regime already applied to an active BGI task.

This does **not** prove identical update-latching semantics for an in-flight rebuild.

### Locator D — §5.5.5 / §5.5.7, printed pp. 5-24–5-25 (PDF pp. 125–126)

The guide says array configuration is saved to both controller NVRAM and disks in the array. It then instructs operators to inspect rebuild rate per adapter and states that rebuild rate is **not affected when configuration is cleared**.

**Supported relation:**

> controller maintenance-policy lifetime can differ from array-configuration lifetime.

**Not supported:**

The source does not identify the physical field or exact storage medium that preserves the rebuild-rate value, so no specific NVRAM-layout claim is made.

## Source 2 — Dell Server Administrator Storage Management 11.0.0.0, `Setting the Rebuild Rate`

**Type:** manufacturer-primary current operational documentation (`P`)

URL: https://www.dell.com/support/manuals/en-us/openmanage-server-administrator-v11.0.0.0/omss_11.0.0.0_ug_olh_pub/setting-the-rebuild-rate?guid=guid-b09c0743-1e58-42e8-b92d-103aa5be613e&lang=en-us

Dell defines a configurable 0%–100% rebuild rate as the percentage of system resources dedicated to reconstruction. It explicitly states:

- 0% is the lowest controller priority and maximum completion time;
- **0% does not mean stopped or paused**;
- 100% is highest priority, minimum completion time, and greatest system-performance impact.

Dell also documents reuse of the controller's rebuild-rate setting for consistency check, background/full initialization, and reconfiguration on supported PERC controllers.

**Supported engineering boundary:**

> `lowest priority != disabled`, and the exposed percentage is a controller resource-allocation policy.

This current guide is not used to back-project every later PERC detail into 2006 LSI hardware.

## Source 3 — Dell `PowerEdge RAID Controller 9 User's Guide`, `Enhanced rebuild prioritization`

**Type:** manufacturer-primary product-family documentation (`P`)

URL: https://www.dell.com/support/manuals/en-us/poweredge-t140/perc9ugpublication/enhanced-rebuild-prioritization?guid=guid-2b87d691-c539-480e-b756-6c6f787f59e9&lang=en-us

Dell states that when PERC rebuild rate is set above 30%, the controller modifies its command-allocation strategy to prioritize rebuild operations when application I/O is consistent in the disk group.

**Supported engineering boundary:**

> the percentage is not safely interpreted as a linear fixed share of disk bandwidth or IOPS; at least one named PERC generation applies a thresholded scheduling-policy change.

The source does not expose the internal scheduling algorithm or prove a particular throughput curve.

## Claim ledger

| Claim | Type | Strength | Source basis |
| --- | --- | --- | --- |
| By March 2006 MegaRAID exposes user-defined rebuild rate | `H/P` | high | LSI 2006 §2.4.13/13.1 |
| 2006 rebuild rate is defined in compute-cycle/priority terms | `H/P` | high | LSI 2006 p. 2-12 |
| 0% means idle-only work, not necessarily disabled | `H/P` + later `P` corroboration | high | LSI 2006 + Dell OpenManage |
| interrupted rebuild is automatically restarted after reboot | `H/P` | high for bounded manual | LSI 2006 p. 2-11 |
| exact in-flight rebuild progress survives reboot | `X` | unsupported | manual says restart, not checkpoint semantics |
| rebuild-rate property survives configuration clear | `H/P` | high for bounded management regime | LSI 2006 p. 5-25 |
| rebuild rate is stored in a specific NVRAM field | `X` | unsupported | storage location not identified |
| rebuild rate can govern BGI as well as rebuild scheduling | `H/P` | high | LSI 2006 §2.4.6 |
| changing rate immediately changes an active BGI | `X` | contradicted | LSI requires stop/restart for effect |
| PERC 9 can change command-allocation strategy above 30% | `P` | high for named product-family docs | Dell PERC 9 |
| N% rebuild rate guarantees N% disk bandwidth/IOPS | `X` | unsupported | source semantics are priority/resource scheduling |
| higher rebuild rate restores redundancy faster with greater foreground impact | `P/E` | high at Dell operational level | Dell OpenManage |
| rebuild rate determines reconstructed byte correctness | `X` | unsupported | no such contract |

## Engineering reconstruction

A minimal state relation is:

```text
surviving redundant state + member failure
    -> repair obligation
    -> eligible replacement / hot spare
    -> rebuild task
          |
          +-- controller rebuild-rate policy
          |       -> foreground/background resource competition
          |
          +-- progress / interruption state
    -> reconstructed member
    -> restored redundancy margin
```

A separate lifetime relation appears in the 2006 management interface:

```text
array configuration --clear--> retired/reset configuration
controller rebuild-rate policy ---------> still present
```

This is evidence that a maintenance policy can have a persistence horizon different from the logical storage configuration it once governed. It does not identify a universal physical persistence mechanism.

## Counterexamples / stop conditions

1. **0% != off.** Both early LSI semantics and later Dell guidance treat it as lowest-priority/opportunistic work.
2. **rate != progress.** A policy parameter is not evidence of how much of a particular member has been rebuilt.
3. **restart != resume checkpoint.** Automatic post-reboot rebuilding does not prove exact progress persistence.
4. **percentage != throughput fraction.** PERC 9 exposes thresholded command-allocation behavior.
5. **configuration clear != all controller state cleared.** The 2006 guide explicitly preserves rebuild rate across this operation.
6. **rebuild != scrub/patrol read.** Discovery/verification and reconstruction are separate jobs even if a controller exposes related background-work rate controls.
7. **rebuild completion != sanitization.** Restored redundancy says nothing about erasing old failed-member traces.
8. **manufacturer documentation != field fault validation.** No fault injection or measured reliability curve was performed in this slice.

## Related-repository check

Fresh GitHub searches of `tmzncty/computing-archaeology` for `MegaRAID` and `rebuild rate` returned no dedicated overlapping research item in this round.

If a broader history is built later, controller genealogy, firmware scheduler evolution, exact NVRAM layout, and benchmark/fault-injection work should live there first. `technical-retention` keeps the narrower retention relation: scheduling-policy state, repair obligation, progress, array configuration, and restored redundancy must not be collapsed.

## Remaining evidence debt

- pre-2006 RAID rebuild-rate/throttling terminology and implementations;
- exact later MegaRAID/PERC persistence/reset semantics for the rate property;
- exact rebuild-progress persistence/restart behavior after power loss;
- controlled throughput/latency measurements across rate settings;
- URE/correlated-failure behavior while rebuild is throttled;
- cross-vendor controller comparison;
- PERC 12/13 firmware-specific mutability and later task-priority semantics.
''', encoding="utf-8")

# Add the new case to the canonical case table immediately after Case 135.
idx = Path("CASE_INDEX.md")
s = idx.read_text(encoding="utf-8")
newrow = "| [MegaRAID/PERC Rebuild Rate: Repair Priority, Service Competition, and Maintenance-Policy Persistence](cases/136-megaraid-perc-rebuild-rate-repair-priority.md) | **grounded** | redundant RAID state + failed-member repair obligation + controller scheduling/resource-priority policy + automatic rebuild re-entry | separate rebuild policy, task/progress, array configuration, foreground-service competition, and restored redundancy; show lowest priority is not disabled and maintenance-policy lifetime can outlive configuration clear | [2006 LSI + later Dell PERC grounding](evidence/136-lsi-2006-dell-perc-rebuild-rate-grounding.md); pre-2006 genealogy, exact persistence location, reboot progress checkpoints, cross-vendor comparison, and fault/throughput validation remain open |"
if "cases/136-megaraid-perc-rebuild-rate-repair-priority.md" not in s:
    lines = s.splitlines()
    pos = next((i for i, line in enumerate(lines) if "cases/135-micron-emmc-self-refresh-time-trigger-maintenance.md" in line), None)
    if pos is None:
        raise SystemExit("CASE_INDEX Case 135 row marker not found")
    lines.insert(pos + 1, newrow)
    s = "\n".join(lines) + ("\n" if s.endswith("\n") else "")

findings = r'''

## Case 136 — MegaRAID/PERC rebuild-rate findings

Grounding record: [`evidence/136-lsi-2006-dell-perc-rebuild-rate-grounding.md`](evidence/136-lsi-2006-dell-perc-rebuild-rate-grounding.md).

- **2895 — repair obligation != repair execution:** a failed-member condition can make rebuild necessary while controller scheduling still determines when/how aggressively work runs. (`H/P`, `E`)
- **2896 — rebuild-rate policy != rebuild progress:** the configured percentage is a scheduling/resource-priority setting, not evidence of completed reconstruction extent. (`H/P`, `E`)
- **2897 — 0% rebuild rate != rebuild disabled:** LSI 2006 makes work idle-only at 0%; Dell later explicitly says 0% is neither stopped nor paused. (`H/P`, `P`, `X`)
- **2898 — 100% priority != free acceleration:** later Dell guidance couples highest rebuild priority/minimum completion time to the greatest impact on system performance. (`P`, `E`)
- **2899 — nominal percentage != fixed bandwidth fraction:** LSI defines compute-cycle priority and PERC 9 documents a >30% command-allocation strategy change; the field is not a guaranteed disk-bandwidth/IOPS fraction. (`H/P`, `P`, `E`, `X`)
- **2900 — reboot interruption != forgotten repair obligation:** LSI 2006 says a rebuild interrupted by system downtime is automatically restarted after reboot. (`H/P`)
- **2901 — automatic restart != proven exact-progress checkpoint:** the manual does not establish whether prior stripe/progress state is resumed exactly or work is redone. (`H/P`, `E`, `X`)
- **2902 — array-configuration clear != rebuild-rate reset:** the 2006 management guide explicitly says the rebuild-rate property is not affected when configuration is cleared. (`H/P`)
- **2903 — maintenance-policy lifetime != array-configuration lifetime:** Case 136 therefore supplies a bounded controller example in which a scheduling preference outlives the logical array-configuration clear operation. (`H/P`, `E`)
- **2904 — rebuild-rate label != rebuild-only use:** LSI 2006 also uses the setting to control background-initialization rate. (`H/P`)
- **2905 — stored policy update != immediate active-task regime:** for the documented BGI path, a rate change takes effect only after stop/restart; this is not generalized to in-flight rebuild without evidence. (`H/P`, `E`, `X`)
- **2906 — rebuild scheduling != integrity-discovery scheduling:** rebuild, consistency check, background initialization, and patrol read remain distinct maintenance jobs even where rate controls are reused. (`H/P`, `E`, `A`)
- **2907 — rebuild urgency != reconstructed-byte correctness:** rate governs service/resource priority, not parity/mirror correctness or source-data integrity. (`E`, `X`)
- **2908 — rebuild completion != secure erasure:** restored redundancy does not establish physical deletion or sanitization of the failed member. (`E`, `X`)
- **2909 — topology retention != maintenance-policy retention:** Case 131 foreign-configuration recovery and Case 136 rebuild-rate survival across configuration clear expose separate controller-state lifetimes; no shared internal storage layout is inferred. (`A`, `X`)
- **2910 — related-repository boundary:** fresh `computing-archaeology` searches for `MegaRAID` and `rebuild rate` found no dedicated overlap; broader controller genealogy, scheduler internals, benchmarks, and fault injection belong there if developed. (`H/P` project-state record)
'''
if "## Case 136 — MegaRAID/PERC rebuild-rate findings" not in s:
    if "**2894 —" not in s:
        raise SystemExit("CASE_INDEX final finding marker not found")
    s = s.rstrip() + findings + "\n"
idx.write_text(s, encoding="utf-8")

road = Path("ROADMAP.md")
r = road.read_text(encoding="utf-8")
item = "- [x] Case 136 MegaRAID/PERC rebuild-rate / repair-priority policy slice — [`cases/136-megaraid-perc-rebuild-rate-repair-priority.md`](cases/136-megaraid-perc-rebuild-rate-repair-priority.md) + [`evidence/136-lsi-2006-dell-perc-rebuild-rate-grounding.md`](evidence/136-lsi-2006-dell-perc-rebuild-rate-grounding.md): LSI 2006 and later Dell PERC documentation separate repair obligation, rebuild execution/progress, controller resource-priority policy, array configuration, and restored redundancy; they also ground `0% != disabled`, automatic post-reboot rebuild re-entry without claiming exact progress persistence, and a rebuild-rate property that survives configuration clear. Pre-2006 throttling genealogy, exact policy/progress persistence location, cross-vendor controllers, URE interaction, throughput curves, and fault injection remain open.\n\n"
marker = "## Phase 2 — Build missing technical bridges\n\n"
if item not in r:
    if marker not in r:
        raise SystemExit("ROADMAP Phase 2 marker not found")
    r = r.replace(marker, marker + item, 1)
road.write_text(r, encoding="utf-8")

# Bounded assertions before the workflow commits anything.
assert CASE.exists() and EVID.exists()
assert "cases/136-megaraid-perc-rebuild-rate-repair-priority.md" in idx.read_text(encoding="utf-8")
assert "**2910 — related-repository boundary:**" in idx.read_text(encoding="utf-8")
assert "Case 136 MegaRAID/PERC rebuild-rate / repair-priority policy slice" in road.read_text(encoding="utf-8")
