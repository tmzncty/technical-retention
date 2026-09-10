# Evidence 136 — LSI MegaRAID / Dell PERC Rebuild-Rate Scheduling and Policy Lifetime

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
