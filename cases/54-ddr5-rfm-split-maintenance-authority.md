# DDR5 Refresh Management: Split Maintenance Authority, RAA Accounting, and Platform Enablement

## Status

**`grounded`** — bounded to the public DDR5 Refresh Management (`RFM`) interface and its system-composition problem, using Micron manufacturer DDR5 documentation, Intel platform documentation through May 2025, and the independent USENIX Security 2025 McSee bus-observation study. The case establishes a retention-specific responsibility split without claiming a complete revision-by-revision JEDEC chronology or universal implementation behavior.

Grounding record: [`../evidence/54-ddr5-rfm-2022-2025-grounding.md`](../evidence/54-ddr5-rfm-2022-2025-grounding.md).

## Scope

Case 53 established a bounded 2012–2020 RowHammer / targeted-refresh history: disturbance can make a victim row need extra restoration even when ordinary periodic refresh is otherwise on schedule, and a mitigation label such as `TRR` does not by itself establish implementation-level immunity.

This case asks the next, narrower question:

> What changes when DDR5 exposes a standardized Refresh Management interface in which the DRAM can advertise that extra management is required, the memory controller can maintain activation-pressure accounting and issue an RFM command, and the DRAM then receives time to perform internal mitigation?

The central object is therefore not `RowHammer security` in general. It is **retention work split across the controller/device boundary**.

This case is **not**:

- a complete history of JESD79-5 and every later revision;
- a claim that RFM invented RowHammer-aware refresh or targeted-refresh concepts;
- a claim that every DDR5 device requires RFM;
- a claim that every memory controller implements the same RAA accounting policy;
- a reverse engineering of the hidden in-DRAM mitigation performed during an RFM interval;
- a complete treatment of Adaptive RFM (`ARFM`), Directed RFM (`DRFM`), PRAC, or later DDR5 mitigation revisions;
- a claim that absence of RFM commands proves absence of all RowHammer mitigation;
- independent certification of a named DIMM's resistance to arbitrary RowHammer patterns.

## Historical vocabulary and evidence boundary

### DDR5 RFM as a controller/device contract

A Micron-authored DDR5 SDRAM core datasheet, publicly mirrored by Avnet, contains a `Refresh Management` section. Its historical/engineering vocabulary is unusually explicit:

- `Refresh Management (RFM) Requirement` in read-only mode register `MR58:OP[0]`;
- `RFM not required` versus `RFM required`;
- a suggested controller-side `Rolling Accumulated ACT (RAA)` count;
- per-bank increments for `ACT` commands;
- vendor-specified `RAAIMT` (`RAA Initial Management Threshold`);
- `RFMab` and `RFMsb` commands;
- additional time for the device to `manage refresh internally`.

The same document says that `MR58:OP[0] = 0` means no additional refresh is needed beyond the ordinary REFRESH requirement, while `MR58:OP[0] = 1` means additional refresh management is required to protect data integrity. It suggests that the controller monitor ACT commands per bank as RAA and issue RFM when the vendor-specified threshold is reached.

This creates a clear boundary between **baseline refresh** and **disturbance/activity-conditioned extra management**.

The source used here is manufacturer-authored but accessed through a distributor mirror rather than a current Micron-hosted copy. The grounding record preserves that provenance instead of silently treating the mirror as an official standards archive.

### Requirement can differ by DDR5 device

A Micron 16Gb DDR5 SDRAM die-revision addendum (manufacturer document mirrored on the web, Rev. D, February 2023) lists `RFM not required` in its function matrix and states that RAA threshold/decrement fields apply only when the RFM requirement bit is set.

That is an important counterexample to the shortcut `DDR5 => RFM required`.

The useful historical statement is narrower:

> DDR5 exposes an RFM contract under which a device may advertise that extra management is required; at least one documented Micron 16Gb die revision instead advertises that RFM is not required.

### Platform support is not the same thing as feature enablement

Intel's public processor datasheet, document 743844 Rev. 015 (May 2025), has a section `5.1.20 Refresh Management (RFM)`. It states:

- RFM is supported according to the JEDEC specification;
- LPDDR5/x RFM is enabled;
- DDR5 RFM is **not yet enabled** on the bounded processor/platform family documented there.

This is first-party platform documentation, and it provides a particularly strong implementation boundary:

> **standard/interface support ≠ enabled DDR5 controller behavior**.

The statement is scoped to the Intel processor families covered by that May 2025 datasheet. It is not generalized to every Intel memory controller before or after that document.

### Independent bus observation in 2025

Patrick Jattke et al., `McSee: Evaluating Advanced Rowhammer Attacks and Defenses via Automated DRAM Traffic Analysis`, USENIX Security 2025, built a hardware/software platform that captures and decodes DDR4/DDR5 bus traffic.

For the systems they tested, the authors report that neither the tested Intel nor AMD CPUs issued RFM commands, even though about one third of the DDR5 devices in their test pool advertised that RFM was required for proper RowHammer mitigation. They further observed that the tested Intel platforms performed additional mitigative activations instead of RFM and reverse engineered that behavior.

The evidence is valuable because it is **independent observation of command traffic**, not merely a feature list. Its scope is still bounded to the tested CPUs, firmware/configuration, and DDR5 module pool. It must not be turned into `all Intel/AMD DDR5 systems never issue RFM`.

## Retained states and control relations

The bounded RFM regime contains several distinct states and responsibilities:

1. **DRAM payload charge** — the user data whose integrity must be preserved;
2. **ordinary periodic refresh obligation** — baseline retention maintenance that exists independently of RFM;
3. **device-advertised RFM requirement** — a read-only indication that additional management is required or not required for that device;
4. **vendor-provided activation thresholds** — parameters such as RAAIMT that tell the controller when extra management becomes necessary;
5. **controller-side activation-pressure state** — e.g. a per-bank rolling accumulated ACT quantity;
6. **RFM scheduling/issuance state** — controller logic deciding when an RFM command must be issued;
7. **RFM command scope** — all-bank or same-bank-address forms in the bounded Micron documentation;
8. **in-DRAM mitigation work** — whatever internal operations the DRAM performs during the granted management interval;
9. **platform enablement/configuration** — whether the processor memory controller actually uses the RFM path for DDR5;
10. **independent observed command behavior** — evidence that a nominally supported feature is or is not exercised on a concrete running platform.

Only the first item is application payload. The rest can be **retention infrastructure, policy, interface state, or evidence about whether retention work is actually being performed**.

## Engineering reconstruction

### Ordinary REF and RFM are different maintenance relations

Micron's DDR5 documentation says the device can report that no additional management is needed beyond the ordinary refresh requirement, or that additional management is required. Therefore:

> **ordinary periodic REF ≠ RFM maintenance opportunity**.

RFM does not abolish the basic charge-restoration regime established in Case 03. It adds a second maintenance relation whose trigger is activity pressure rather than elapsed refresh deadline alone.

This matters because one word — `refresh` — otherwise hides two different reasons for intervention:

```text
elapsed time / ordinary DRAM retention obligation
    -> periodic REF

high activation pressure / disturbance risk
    -> additional RFM opportunity
```

Both may renew or protect stored state, but they are not interchangeable scheduling contracts.

### A device can advertise a retention requirement without performing controller scheduling

The RFM requirement bit and vendor thresholds originate from the DRAM device, while the suggested RAA accounting and command issuance live on the controller side.

Therefore:

> **DRAM mitigation requirement ≠ controller-side maintenance execution**.

The memory device can say, in effect, `I require additional management under this activity budget`, while another component is responsible for tracking enough activity pressure and issuing the command before the allowed budget is exhausted.

This is a distinct form of **split maintenance authority**:

```text
DRAM device
    advertises requirement + thresholds

memory controller
    retains/derives activation-pressure state
    schedules RFM

DRAM device
    uses the RFM interval for internal management
```

No single layer, taken alone, constitutes the complete retention mechanism.

### RAA is maintenance state, not a history archive

In the suggested Micron implementation, ACT commands increment a per-bank Rolling Accumulated ACT count and maintenance operations reduce the accumulated pressure.

That makes RAA-like state constitutive of future retention work:

> **per-bank activation-pressure state ≠ payload state**.

But it would be wrong to call the counter an archive of access history. A rolling/credited quantity intentionally forgets detail as refresh/management work earns back budget. It retains only enough of the past to decide whether future activity remains admissible or extra maintenance is due.

Therefore:

> **activity accounting ≠ complete access history**.

This connects to Case 48's maintenance-history metadata in an important but limited way. Cassandra `repairedAt` retains a past completion classification that narrows future repair scope; RAA retains a rolling pressure budget that determines when extra DRAM maintenance is due. Both are second-order retention states, but they do not share protocol semantics or historical lineage.

### RFM command issuance does not expose the hidden in-DRAM defense

The public interface says that executing RFM gives the device additional time to manage refresh internally. It does not, by itself, reveal the device's complete victim-selection logic, internal counters, physical adjacency map, or exact targeted-refresh algorithm.

Therefore:

> **controller command issuance ≠ in-DRAM mitigation algorithm**.

and:

> **host-visible bank accounting ≠ physical victim-row knowledge**.

This sharpens Case 53's finding that aggressor identification and physical-victim resolution can live at different architectural layers. RFM makes that split operational: the controller can police a bank-level activation budget without necessarily learning which physical victim wordlines the DRAM will restore internally.

### Standardized support can exist without enabled platform behavior

Intel's May 2025 documentation is explicit that RFM is supported according to the JEDEC specification while DDR5 RFM is `not yet enabled` on the bounded platform family.

Therefore:

> **standardized command/interface support ≠ enabled platform behavior**.

This is not merely semantic. A retention mechanism that depends on cross-component composition can fail to exist as a working end-to-end path even if both the DRAM standard and processor documentation know the command vocabulary.

The result is analogous to, but not identical with, Cases 20/31/32 on persistence domains: an interface-level durability or maintenance contract is not automatically an implementation-level guarantee. The specific state, failure model, and participants differ.

### Device requirement can differ even within DDR5

The Micron 16Gb die-revision addendum that says `RFM not required` prevents a second shortcut:

> **DDR5 support for RFM ≠ RFM requirement for every DDR5 device**.

A controller therefore cannot infer requirement solely from the generation name `DDR5`; device-advertised capability/requirement data matters.

This is another place where **type membership is weaker than operational state**. `DDR5` names an interface family. It does not fully determine the retention obligations of every compliant physical embodiment.

### No RFM command does not prove there is no mitigation

McSee's independent observation is especially useful because it blocks the mirror-image overgeneralization. The tested Intel controllers did not send RFM commands, but the researchers observed additional mitigative activations and characterized a controller-side probabilistic defense.

Therefore:

> **absence of RFM command ≠ absence of all RowHammer mitigation**.

and:

> **platform mitigation presence ≠ conformance to the device-preferred RFM path**.

The second distinction is important when a DDR5 device advertises an RFM requirement. A controller may perform some other mitigation, but whether that alternative supplies an equivalent guarantee is a separate empirical question; it cannot be inferred merely from the existence of `some mitigation`.

### Independent observation and manufacturer contract answer different questions

Intel's datasheet says what the bounded platform exposes/enables. Micron's documentation says what the bounded DRAM interface can require. McSee observes what commands actually appear on tested buses.

These are complementary evidence layers:

```text
manufacturer DRAM contract
    -> what maintenance may be required

processor/platform documentation
    -> what the controller says it supports/enables

independent bus observation
    -> what commands actually occur under tested conditions
```

Therefore:

> **documented capability ≠ observed execution**.

and the converse also matters:

> **observed behavior in one test pool ≠ universal vendor/platform guarantee**.

The repository should preserve both directions rather than choosing documentation or reverse engineering as the sole authority for all claims.

## Relation to earlier DRAM cases

### Case 03 — periodic refresh

Case 03 establishes ordinary charge-restoration deadlines. Case 54 adds a separate activity-conditioned management path. RFM is extra work above the ordinary refresh relation for devices that require it.

### Case 33 — Same Bank Refresh

Case 33 studies refresh localization for service concurrency: which bank resources are occupied while baseline maintenance occurs. Case 54 uses `RFMsb`/bank-level activity accounting for disturbance-management scope. Similar bank vocabulary does not imply the same trigger or purpose.

> **refresh localization for concurrency ≠ refresh-management scope for disturbance pressure**.

### Cases 40 and 43 — retention profiling and runtime feedback

RAIDR/AVATAR classify future cadence using retention characteristics or observed errors. RFM instead responds to activation pressure under a device-advertised management contract. A row may have ordinary intrinsic retention yet still participate in a bank whose access pressure consumes the RFM budget.

### Case 45 — on-die ECC / ECS

ODECC/ECS correct or scrub errors inside DDR5 devices. RFM grants additional management time intended to prevent disturbance from becoming integrity loss. Error correction, scrubbing, ordinary refresh, and RFM are therefore separate maintenance layers even when they coexist in the same DDR5 device.

### Case 53 — RowHammer targeted refresh

Case 53 provides the historical and physical prerequisite: access to an aggressor can reduce victim retention margin, and targeted-refresh concepts predate DDR5 RFM. Case 54 therefore **must not** describe RFM as the invention of RowHammer-aware retention maintenance.

The new contribution is narrower:

> DDR5 RFM standardizes a later **responsibility split** in which the DRAM can advertise requirement/threshold information while the controller accounts for activation pressure and creates an interval for hidden in-DRAM mitigation.

## Failure and forgetting boundaries

Within this bounded regime, a retention failure can arise even when every stored payload bit still physically exists at the beginning of the episode:

- the device requires RFM but the controller does not implement or enable the path;
- controller activity accounting underestimates or loses activation pressure;
- the RFM command is delayed beyond the device's allowed activity budget;
- platform firmware/configuration prevents an otherwise-defined feature from being used;
- controller mitigation differs from the device's expected RFM path and does not cover the same disturbance patterns;
- hidden in-DRAM mitigation has finite tracking/topology/coverage limits;
- a researcher infers guarantee from `DDR5`, `RFM supported`, or `mitigation present` without verifying the actual end-to-end composition.

The relevant form of forgetting is not simply `the cell leaked because time passed`. It is **failure of a distributed maintenance contract to create restoration opportunity before access-induced disturbance exceeds the retained state's margin**.

## Prior art and anti-anachronism

Case 53 already anchors RowHammer-aware targeted-refresh concepts to Intel work with 2012 priority and distinguishes that record from Kim et al.'s 2014 open characterization/PARA contribution.

Therefore:

> **DDR5 RFM evolution ≠ origin of RowHammer-aware targeted refresh**.

The defensible novelty claim for this case is not invention priority. It is analytical:

> the public DDR5-era evidence makes a retention-maintenance responsibility split directly inspectable across device-advertised requirement, controller activity accounting, command scheduling, hidden in-DRAM work, platform enablement, and independent observed execution.

The phrases `split maintenance authority`, `activation-pressure state`, and `retention contract` are project analytical vocabulary. They are not silently attributed to JEDEC, Micron, Intel, or the McSee authors.

## Philosophical interpretation — bounded

Case 54 creates a narrow conceptual pressure on any picture of persistence as a property located inside one object.

A DRAM cell may physically hold the payload; nevertheless, continued admissibility can depend on a requirement bit exposed by the device, activity state retained or derived in the controller, commands scheduled across an interface, and opaque restoration inside the device. What persists is therefore sustained by a **composed relation among components whose knowledge and authority are incomplete in different ways**.

That observation is an engineering reconstruction used for philosophical comparison. It is not evidence that the historical actors described RFM in those terms.

## Cross-case result

Case 54 adds the following bounded decomposition:

```text
ordinary refresh obligation
    !=
device-advertised RFM requirement
    !=
controller activation-pressure accounting
    !=
RFM scheduling / command issuance
    !=
in-DRAM mitigation work
    !=
platform feature enablement
    !=
independently observed command behavior
    !=
empirical immunity to arbitrary RowHammer patterns
```

The strongest new comparison rule is:

> **a retention obligation can be distributed as a protocol: one component can advertise the need, another can retain the pressure state and schedule maintenance, while a third logical layer of the same device performs opaque repair work.**

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Micron DDR5 documentation exposes an RFM-required bit in MR58 and vendor-specified RAA thresholds | H/P | Micron-authored DDR5 core datasheet, distributor mirror |
| The suggested controller implementation maintains per-bank Rolling Accumulated ACT accounting | H/P | Micron DDR5 core datasheet |
| Executing RFM gives the DRAM additional time to manage refresh internally | H/P | Micron DDR5 core datasheet |
| Ordinary periodic refresh and RFM are the same scheduling obligation | X | source explicitly distinguishes no-extra-refresh from RFM-required operation |
| Every DDR5 device requires RFM | X | Micron 16Gb die-revision addendum documents `RFM not required` |
| Intel document 743844 Rev. 015 says DDR5 RFM is not yet enabled on its bounded platform family | H/P | Intel public datasheet, May 2025, §5.1.20 |
| `supported according to JEDEC spec` proves DDR5 RFM is enabled on that Intel platform | X | same Intel section separates support from enablement |
| Tested Intel/AMD DDR5 controllers in McSee issued no RFM commands | H/S | USENIX Security 2025 independent bus observation |
| McSee found that roughly one third of its tested DDR5 devices required RFM | H/S | USENIX Security 2025 test pool |
| No RFM command means no RowHammer mitigation of any kind | X | McSee observed additional mitigative activations on tested Intel platforms |
| RFM exposes the exact internal physical victim-selection algorithm | X | bounded public interface only provides management opportunity/contract, not full hidden implementation |
| RFM invented RowHammer-aware targeted refresh | X | Case 53 anchors earlier 2012-priority targeted-refresh work |
| RAA-like activation-pressure state can be retention infrastructure without being payload or a complete access-history archive | E | engineering reconstruction from the controller/accounting contract |
| McSee proves universal behavior of all Intel/AMD DDR5 systems | X | sample-bounded empirical study only |

## Sources

### Manufacturer / platform primary evidence

- Micron Technology, **DDR5 SDRAM Product Core Data Sheet**, `Refresh Management` section; manufacturer-authored public copy mirrored by Avnet: <https://www.avnet.com/wcm/connect/dacdfea7-999f-4ee0-b514-6f9e0bf68c6d/ddr5-sdram-core.pdf?MOD=AJPERES>.
- Micron Technology, **16Gb DDR5 SDRAM Die Rev A**, Rev. D, February 2023, manufacturer document mirrored at device.report; function-matrix notes include `RFM not required`: <https://device.report/m/e4760da10ba9aca558ff5b3b6cd76607ea2c4dcd4ebcfe964553bb4d1c5aa6ac>.
- Intel, **13th Generation Intel Core, Intel Core 14th Generation, Intel Core Processor (Series 1/2), Intel Xeon E 2400 and Xeon 6300 Processor Datasheet, Volume 1 of 2**, Doc. 743844 Rev. 015, May 2025, §5.1.20 `Refresh Management (RFM)`: <https://cdrdv2-public.intel.com/743844/743844-015.pdf>.

### Independent research

- Patrick Jattke, Michele Marazzi, Flavien Solt, Max Wipfli, Stefan Gloor, Kaveh Razavi, **“McSee: Evaluating Advanced Rowhammer Attacks and Defenses via Automated DRAM Traffic Analysis,”** 34th USENIX Security Symposium, August 2025, pp. 5621–5640: <https://www.usenix.org/conference/usenixsecurity25/presentation/jattke>.

## Evidence limits / next work

This case is `grounded` for the bounded split-responsibility and platform-composition argument, but the following remain deliberately open:

- direct revision-by-revision inspection of official JESD79-5 / 5A / 5B / 5C / later normative text;
- exact chronology and semantics of ARFM, DRFM, PRAC, and later mitigation extensions;
- exact controller accounting implementation in named commercial CPUs beyond what documentation/bus observation establishes;
- named-DIMM/device fault injection proving end-to-end compliance with an RFM-required contract;
- whether later Intel/AMD platforms changed the DDR5 RFM enablement/issuance behavior observed in the bounded 2025 sources;
- full security evaluation of residual RowHammer patterns.

Those are future bounded cases, not hidden requirements for this one.