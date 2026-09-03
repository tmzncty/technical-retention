# Micron DDR5 Same-Bank Refresh: Localizing Maintenance Interference Without Removing the Refresh Obligation

## Status

**`grounded`** — bounded to public Micron manufacturer documentation describing DDR5 `Same Bank Refresh` / `REFsb` after the July 2020 JEDEC DDR5 standard announcement and in 2021–2023 DDR5 enablement/deployment material.

Grounding record: [`../evidence/33-micron-2020-2023-ddr5-same-bank-refresh-grounding.md`](../evidence/33-micron-2020-2023-ddr5-same-bank-refresh-grounding.md).

## Scope

This case asks one narrow question left open by Cases 03, 09, 10, and 21:

> What changes when periodic DRAM refresh no longer forces the whole bank set to be treated as one service-blocking unit, but can target the same bank position across bank groups while other banks remain available?

The bounded object is Micron's public description of DDR5 `Same Bank Refresh` / `REFsb`. Micron's 2021 ecosystem article describes DDR5 Same Bank Refresh as targeting **one bank per bank group**. Its current DDR4-versus-DDR5 feature table likewise says DDR5 adds `same bank` refresh and that `REFsb enables refreshing a bank in each BG`. A 2023 Micron server-platform article describes the practical availability consequence: same-bank refresh keeps other bank groups available to service processor accesses while refresh is occurring.

This is **not**:

- a complete JEDEC DDR5 refresh-standard chronology;
- a normative reconstruction of every `JESD79-5` timing rule;
- an invention-priority claim for bank-localized refresh;
- a claim that Micron invented `REFsb`;
- a study of temperature-compensated refresh or retention-aware refresh scheduling;
- a claim that `Same Bank Refresh` is historically synonymous with every earlier/later use of `per-bank refresh`.

The public manufacturer evidence is strong enough to ground the bounded command/availability relation, but exact normative timing, fine-granularity-refresh interactions, later DDR5 revisions, and LPDDR/per-bank genealogies remain separate work.

## Relation to Cases 03, 09, 10, and 21

The earlier DRAM cases progressively separate several different parts of the refresh problem:

```text
Case 03
    why dynamic payload requires periodic restoration

Case 09
    where the next refresh-row address comes from

Case 10
    where an autonomous refresh trigger/schedule can come from

Case 21
    who must generate recurring refresh work in normal AUTO REFRESH
    versus SELF REFRESH mode, and how that responsibility returns on exit

Case 33
    how much of the banked memory organization must be unavailable
    while a refresh command is maintaining dynamic state
```

Case 33 therefore adds **maintenance target/interference geometry** without replacing any of the previous distinctions.

A DDR5 controller can still face a refresh obligation. `REFsb` changes the spatial scope over which that obligation blocks ordinary service.

## Historical vocabulary and record

The historical vocabulary used here is Micron's own public DDR5 terminology:

- `Same Bank Refresh`;
- `REFsb`;
- `bank group` / `BG`;
- `all bank` refresh;
- DDR4 / DDR5.

Micron's DDR5 Technology Enablement Program article states that JEDEC announced the DDR5 standard in **July 2020**. In its list of DDR5 changes, Micron describes improved refresh schemes, specifically `Same Bank Refresh`, as targeting `one bank per bank group`.

Micron's current DDR5 product comparison preserves the same distinction more explicitly. For `REFRESH commands`, it lists DDR4 as `All bank` and DDR5 as `All bank and same bank`; the corresponding explanation says `REFsb enables refreshing a bank in each BG`. The same table shows the bank-group organization separately, which matters because the phrase `same bank` is not evidence that one globally singular bank is the only target.

Micron's 2023 article on DDR5 with 4th Gen Intel Xeon Scalable processors describes the service consequence in less formal prose: where DDR4 all-bank refresh locks all banks together, DDR5's same-bank capability gives greater access by refreshing a smaller bank scope and leaving other bank groups available for processor data access.

The 2023 phrase `refreshing a single bank at a time` is therefore treated as an availability-oriented summary, not as authority to erase the more precise manufacturer wording `one bank per bank group` / `a bank in each BG` found in Micron's other DDR5 material.

## Retained state and control state

The payload remains volatile dynamic-memory state. Case 33 does not change the physical reason DRAM must be restored.

The bounded interface adds a different relation: **which bank subset is selected for one refresh operation and which banks remain available for ordinary service while that maintenance is in progress**.

At least four things must remain distinct:

1. **payload state** — dynamic data whose physical distinction decays without refresh;
2. **refresh obligation** — the requirement that required restoration work continue often enough to preserve that payload;
3. **refresh target geometry** — which bank positions are selected by a refresh operation;
4. **maintenance interference / service availability** — which banked resources cannot serve ordinary accesses while those targets are being refreshed.

`Refresh target geometry` and `maintenance-interference geometry` are project reconstruction terms, not Micron's historical vocabulary.

## Engineering reconstruction

### Refresh obligation is not service-blocking scope

The most important bounded result is:

> **refresh obligation ≠ service-blocking scope**.

DDR5 Same Bank Refresh does not make dynamic memory cease to require refresh. Instead, Micron presents the feature as a way to maintain a smaller bank scope while leaving other banks/bank groups accessible.

This matters for retention analysis because `maintenance exists` does not answer `how much of the system must temporarily stop ordinary service while maintenance occurs`.

Case 21 already showed that retention availability can differ from ordinary service availability during self refresh. Case 33 adds a finer spatial result: ordinary service can be **partially** available across the same device/rank organization while another bank subset is undergoing constitutive maintenance.

### Maintenance localization is not maintenance elimination

Micron consistently presents Same Bank Refresh as an improved refresh scheme, not as a way to stop refreshing.

Therefore:

> **maintenance localization ≠ maintenance elimination**.

A design can reduce the collateral service cost of maintenance while leaving the underlying retention work intact.

This is analogous at a very abstract functional level to other systems that narrow repair or reconstruction scope, but it is not evidence of a historical lineage from distributed repair locality, SSD garbage collection, or storage scrubbing into DDR5 refresh.

### `Same bank` is not one globally singular bank

Micron's more precise descriptions say that Same Bank Refresh targets **one bank per bank group** / `a bank in each BG`.

Therefore:

> **same-bank refresh ≠ one globally singular bank**.

The name describes a bank-correlated selection across the bank-group structure. A simplified statement such as `one bank at a time` is useful for explaining why availability improves, but it must not overwrite the more precise topology in the manufacturer documentation.

This is also why the project should not silently rename the feature `per-bank refresh`. The roadmap previously used `per-bank refresh` as a broad future bucket; Case 33 grounds DDR5's named `Same Bank Refresh` relation instead. LPDDR and other per-bank refresh regimes need their own period/specification evidence.

### Refresh target geometry is not refresh schedule authority

Case 21 distinguishes external `AUTO REFRESH` recurrence from internal `SELF REFRESH` recurrence. Nothing in the bounded Case-33 evidence says that choosing `REFsb` transfers recurring refresh responsibility into the DRAM in the way `SELF REFRESH` does.

Therefore:

> **refresh target geometry ≠ refresh schedule authority**.

One question asks **which banks** a maintenance command affects; another asks **who generates or owns the recurring maintenance sequence**.

These relations can change independently.

### Non-refreshed-bank availability is not refreshed-bank availability

Micron's 2023 description makes the availability asymmetry explicit: the practical value of same-bank refresh is that other banks/groups remain accessible while refresh occurs.

This supports a bounded distinction:

> **non-refreshed-bank service availability ≠ refreshed-bank service availability**.

The device/rank cannot be described adequately with one Boolean `available during refresh` value. Availability is conditional on the selected maintenance scope.

### Greater concurrency is not a new retention substrate

DDR5's bank-group organization and Same Bank Refresh change how ordinary traffic can coexist with refresh. They do not make the dynamic cells nonvolatile, nor do they establish a new stored-state substrate.

Thus:

> **maintenance concurrency ≠ nonvolatility**.

The physical retention target is still dynamic state; what changes is the interface/topological partition of maintenance interference.

## Failure and forgetting boundaries

The bounded evidence exposes several failure or misuse boundaries without inventing unsourced DDR5 fault rates:

- a system can preserve the existence of refresh while still implement or schedule it incorrectly; Case 33 does not supply a controller-compliance test;
- assuming `Same Bank Refresh` means one globally singular bank can mis-model which resources are actually selected;
- assuming non-target banks are also blocked collapses the documented availability benefit;
- assuming all banks remain available collapses the maintenance target itself;
- assuming `REFsb` transfers recurrence authority into the device confuses it with `SELF REFRESH`;
- assuming a manufacturer feature summary supplies every normative timing/deadline rule overstates the evidence;
- successful service of another bank while refresh is occurring does not by itself prove that the refresh schedule remains retention-safe over time.

Exact refresh intervals, command ordering, fine-granularity mode restrictions, timing windows, and controller failure behavior require a directly inspected normative specification or product datasheet before they can be claimed here.

## Prior art and anti-anachronism

This case makes **no claim that Micron invented Same Bank Refresh, bank groups, or localized refresh**.

Micron's July 2020 TEP announcement explicitly situates its work alongside JEDEC approval of the DDR5 standard. The 2021 ecosystem article calls Micron a lead developer of DDR5 specifications, but that is not an invention-priority proof.

The case therefore uses Micron as a manufacturer-primary / institutional witness to the public DDR5 feature semantics, not as a substitute for a complete JEDEC genealogy.

Likewise, `maintenance-interference geometry`, `maintenance localization`, and `service-blocking scope` are modern engineering-reconstruction terms introduced by this repository. The period/manufacturer vocabulary remains `Same Bank Refresh`, `REFsb`, `bank group`, and `all bank`.

The phrase `per-bank refresh` should remain a broader comparative bucket until a specific historical standard/product regime is separately grounded. DDR5 `REFsb` is not retroactively assigned to earlier DRAMs merely because both can be described as localized refresh.

## Functional analogy and philosophical limit

A bounded functional analogy can compare DDR5 Same Bank Refresh with other technologies that narrow the scope of maintenance interference: the object is not to eliminate maintenance but to prevent one maintenance event from monopolizing every service resource.

The analogy stops there. DDR5 refresh is deadline-driven restoration of volatile dynamic state. It is not RAID rebuild locality, distributed replica repair, SSD garbage collection, or a generic scheduling abstraction.

A narrow conceptual result follows:

> A retained system can be **partly on call while another part is undergoing work constitutive of retention**.

This complicates any philosophy that treats availability and maintenance as simple opposites. But it does not establish a universal claim that all technical retention has bank-like spatial partitions or that Micron's designers understood `REFsb` in philosophical terms.

## Cross-case result

The DRAM refresh decomposition can now be extended:

```text
payload decay / retention deadline
    !=
row restoration mechanism
    !=
refresh-row enumeration
    !=
recurring maintenance-event generation
    !=
mode/authority controlling where recurrence occurs
    !=
refresh target geometry
    !=
maintenance-induced service-blocking geometry
    !=
ordinary service availability of non-target resources
    !=
exit/recovery timing where a retention mode suspends service
```

Cases 03, 09, 10, and 21 established the earlier distinctions. Case 33 adds the fact that **maintenance can remain mandatory while its interference with ordinary service becomes spatially localized across a bank-group organization**.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| JEDEC announced the DDR5 standard in July 2020 | H/P | Micron DDR5 TEP article and July 2020 Micron TEP release |
| Micron publicly describes DDR5 Same Bank Refresh as targeting one bank per bank group | H/P | Micron DDR5 TEP article |
| Micron's DDR4/DDR5 product comparison lists DDR5 refresh as `All bank and same bank` and says `REFsb enables refreshing a bank in each BG` | H/P | Micron DDR5 product page |
| Micron's 2023 server-platform article says same-bank refresh keeps other bank groups available for processor access | H/P | Micron 2023 Intel Xeon/DDR5 article |
| Same Bank Refresh changes the service-blocking scope of required maintenance rather than removing the DRAM refresh obligation | E | bounded reconstruction from the documented refresh/availability relation plus Cases 03/21 |
| `Same Bank Refresh` means one globally singular bank is the only target | X | contradicted by Micron's `one bank per bank group` / `a bank in each BG` wording |
| `REFsb` is historically just another name for every `per-bank refresh` regime | X | terminology/generalization not established by the bounded sources |
| `REFsb` transfers refresh scheduling into the DRAM exactly like `SELF REFRESH` | X | not established; conflates target geometry with recurrence authority |
| Micron invented Same Bank Refresh | X | not claimed; source set is not an invention-priority study |
| The bounded manufacturer pages establish every normative DDR5 timing requirement | X | outside source scope; normative timing archaeology remains open |

## Related repositories

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `DDR4 refresh`, `DDR5 refresh`, and `per-bank refresh` found no dedicated case to reuse. The broad engineering history of DDR generations, JEDEC standard evolution, controller scheduling, LPDDR per-bank refresh, temperature-compensated refresh, and retention-aware policies should still be developed there if pursued comprehensively.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) supplies the anti-anachronism guard: do not project the project terms `maintenance localization` or `service-blocking geometry` back into DDR5 standardization discourse as actors' own problem formulation.

## Sources

1. Micron Technology, Inc., **“Micron's DDR5 Technology Enablement Program empowers an ecosystem,”** public manufacturer article, available by 1 June 2021; especially the DDR5-feature list stating that Same Bank Refresh targets one bank per bank group: <https://www.micron.com/about/blog/memory/dram/microns-ddr5-technology-enablement-program-empowers-ecosystem>.
2. Micron Technology, Inc., **“Micron Accelerates Breakthrough Platform Innovation With Advancements Across Industry’s First 176-Layer NAND and 1-Alpha DRAM,”** 1 June 2021, resource list linking the preceding DDR5 TEP article and confirming its existence by that date: <https://investors.micron.com/news/press-release/2021/Micron-Accelerates-Breakthrough-Platform-Innovation-With-Advancements-Across-Industrys-First-176-Layer-NAND-and-1-Alpha-DRAM-06-01-2021/default.aspx>.
3. Micron Technology, Inc., **DDR5 DRAM** product page, DDR4-versus-DDR5 feature table: `REFRESH commands — All bank` versus `All bank and same bank`, with `REFsb enables refreshing a bank in each BG`: <https://www.micron.com/products/memory/dram-components/ddr5-sdram>.
4. Micron Technology, Inc., **“Redefining performance With DDR5 and 4th Gen Intel Xeon scalable processors,”** 2023 public manufacturer article, especially the `Same bank refresh` availability discussion: <https://www.micron.com/about/blog/company/partners/redefining-performance-with-ddr5-and-4th-gen-intel-xeon-scalable>.
5. Micron Technology, Inc., **“Micron Accelerates DDR5 Adoption With Technology Enablement Program,”** 14 July 2020, institutional release tying the TEP launch to JEDEC approval of DDR5: <https://investors.micron.com/node/41136>.

A richer Micron DDR5 white paper was discoverable during this round, but its current asset URL could not be directly inspected through the research interface. Its detailed timing claims are therefore **not** used to ground this case.