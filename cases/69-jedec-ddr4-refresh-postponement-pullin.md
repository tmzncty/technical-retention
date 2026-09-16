# JEDEC DDR4 Refresh Postponement and Pull-In: Bounded Scheduling Elasticity, Fine-Granularity Refresh, and Maintenance Accounting

## Status

**`grounded`** — bounded to JEDEC's September 2012 DDR4 SDRAM standard, especially JESD79-4 §§4.9, 4.26, and 4.27, with IBM's 2010 and 2013 refresh-scheduling work used as prior-art and independent engineering context and later Samsung/Micron DDR4 documentation used as implementation-facing continuity witnesses.

Grounding record: [`../evidence/69-jedec-ddr4-2012-refresh-scheduling-grounding.md`](../evidence/69-jedec-ddr4-2012-refresh-scheduling-grounding.md).

Self Refresh Abort / refresh-counter deepening: [`../evidence/69-ddr4-2012-2017-self-refresh-abort-counter-credit-deepening.md`](../evidence/69-ddr4-2012-2017-self-refresh-abort-counter-credit-deepening.md).

## Scope

This case asks a narrow retention question:

> If DRAM must be refreshed periodically, does persistence require one refresh command at every exact nominal `tREFI` instant, or can maintenance work move in time while the retention obligation remains bounded and auditable?

The bounded object is the initial 2012 DDR4 refresh contract:

- the ordinary external `REF` command and average `tREFI` requirement;
- bounded postponement and bounded pull-in of refresh commands;
- the 1x/2x/4x Fine Granularity Refresh (FGR) modes;
- on-the-fly FGR rate changes and their sequencing restrictions;
- the interaction between FGR and Temperature Controlled Refresh in this revision;
- extra refresh work required after some Self Refresh entry histories;
- MR4-controlled **Self Refresh Abort**, including the distinction between an internal refresh being in progress, the refresh counter advancing, and foreground commands becoming admissible after exit.

This is **not**:

- a complete JEDEC DDR/DDR2/DDR3/DDR4/DDR5 refresh chronology;
- a claim that DDR4 invented refresh postponement, refresh scheduling, Self Refresh Abort, or DRAM refresh;
- a controller implementation study identifying the exact counter/register used to track postponed or pulled-in work;
- a transistor-level account of what fraction of an interrupted internal refresh physically completed before abort;
- a claim that FGR always improves performance or reliability;
- a replacement for Cases 03, 21, 33, 34, 40, 43, 53, 54, or 106.

## Historical vocabulary

The 2012 standard directly uses:

- `Refresh command (REF)`;
- `average periodic interval of tREFI`;
- `postponing` and `pulling-in` refresh commands;
- `Fine Granularity Refresh Mode`;
- `Fixed 1x`, `Fixed 2x`, `Fixed 4x`;
- `on-the-fly` 1x/2x and 1x/4x modes;
- `tREFI1`, `tREFI2`, `tREFI4`;
- `tRFC1`, `tRFC2`, `tRFC4`;
- `Temperature Controlled Refresh mode`;
- `Self Refresh entry and exit`;
- `Self Refresh Abort` at MR4 A9;
- `tXS`, `tXS_ABORT`, and `refresh counter` in the Self Refresh exit rules.

Project phrases such as `maintenance debt`, `maintenance credit`, `schedule-control state`, `maintenance-accounting state`, and `temporal scheduling elasticity` are **engineering reconstructions**, not JEDEC vocabulary.

## Historical record

### `tREFI` is an average cadence, not one exact command timestamp

JESD79-4 §4.26 describes the normal-operation `REF` command as nonpersistent: the controller must issue a command whenever refresh is required. The device internally generates refresh addresses, but the external command cadence remains a system responsibility in this mode.

The same section does **not** require each command to occur at one exact periodic instant. It explicitly allows some flexibility in the absolute interval for scheduling efficiency.

In 1x mode, at most eight refresh commands may be postponed. If eight are postponed consecutively, the interval between the surrounding refresh commands may grow to at most `9 × tREFI`. In 2x and 4x modes, the corresponding maxima are sixteen/thirty-two postponed commands and gaps of `17 × tREFI2` / `33 × tREFI4`.

Therefore:

> **nominal refresh interval ≠ exact per-command timestamp**.

and:

> **bounded postponement ≠ canceled refresh obligation**.

The standard changes *when* bounded maintenance is performed; it does not waive the requirement that the deferred work be accounted for.

### Pull-in can pre-pay later refresh work, but only within a bound

JESD79-4 §4.26 also permits refresh commands to be issued in advance. In 1x mode, up to eight pulled-in commands can each reduce the number of regular commands required later by one; the corresponding limits are sixteen and thirty-two in 2x/4x modes.

Issuing more than those limits does not buy additional future exemption.

This yields:

> **pulled-in refresh ≠ unbounded future refresh credit**.

A controller may move bounded work earlier, but the specification caps how much later work that history is allowed to replace.

### FGR pairs refresh frequency with refresh-cycle time

JESD79-4 §4.9 makes both refresh-cycle time (`tRFC`) and average refresh interval (`tREFI`) mode-dependent. The initial standard defines fixed 1x, 2x, and 4x modes plus on-the-fly 1x/2x and 1x/4x operation.

For the bounded table, moving from 1x to 2x halves the nominal interval and uses a shorter `tRFC2`; 4x quarters the nominal interval and uses a still shorter `tRFC4`. The point is not simply `more refresh`. The command frequency and duration of each service-blocking refresh are changed together.

IBM's 2013 ISCA analysis describes the same feature as a trade-off between refresh latency and refresh frequency and reports that no one FGR mode is best for every workload.

Thus:

> **shorter individual refresh pause ≠ necessarily lower aggregate refresh overhead**.

and:

> **FGR mode ≠ a simple retention-strength ranking**.

### On-the-fly mode changes retain sequencing constraints

JESD79-4 §4.9.3 states that changing refresh rate applies the corresponding new `tREFI` and `tRFC` parameters immediately, but the change is not unconstrained.

For 2x operation, an even number of `REF2x` commands must satisfy the relevant grouping conditions before certain rate changes; for 4x, the analogous requirement is a multiple of four. The standard explicitly says that if the listed conditions are not met, DDR4 data retention cannot be guaranteed.

This means the admissibility of a future mode transition depends on the recent maintenance sequence:

> **mode-register change ≠ schedule-history reset**.

The standard does not prescribe that a memory controller use one particular counter representation. The project therefore infers only that a compliant controller must retain or derive enough schedule position to avoid illegal transitions and over-postponement.

### Self Refresh can close a mode boundary without erasing all prior scheduling state

JESD79-4 §4.9.5 allows Self Refresh entry from 1x/2x/4x without first completing a particular FGR grouping. But on exit, an incomplete pre-entry 2x or 4x grouping can require extra `REF1x`, `REF2x`, or `REF4x` commands. Those catch-up commands are explicitly excluded from the average-`tREFI` calculation.

So:

> **Self Refresh entry/exit ≠ automatic erasure of prior fine-granularity accounting**.

A mode handoff can preserve data while still leaving a bounded maintenance obligation that must be discharged on the other side.

### Self Refresh Abort separates maintenance activity, accounting progress, and service admission

The initial September 2012 standard already defines MR4 A9 as `Self Refresh Abort`. In ordinary Self Refresh exit, `tXS` is `tRFC + 10 ns`; §4.27 explains that this delay allows any refresh already started internally by the DRAM to complete.

With MR4 A9 enabled, the alternative path is explicit: the DRAM may abort an ongoing refresh and **does not increment the refresh counter**. Commands in the applicable non-DLL-locked class may become valid after `tXS_ABORT`; the inspected timing table defines that minimum in terms of `tRFC4 + 10 ns`.

This gives a standard-level distinction rather than a project metaphor:

```text
internal refresh is in progress
    !=
refresh counter has advanced

Self Refresh exit requested
    !=
all internal maintenance completed
    !=
foreground commands already admissible
```

The source does not say that a partially executed refresh performed no physical restoration. It specifies the externally relevant abort and counter semantics.

### Self Refresh exit leaves an explicit re-entry obligation even when abort is disabled

JESD79-4 §4.27 also warns that raising CKE to exit Self Refresh can cause an internally timed refresh event to be missed. Before the device is put back into Self Refresh, at least one extra refresh command is required.

Crucially, the standard keeps this requirement **irrespective of the Self Refresh Abort setting**.

Therefore:

> **successful Self Refresh exit ≠ closed maintenance history**.

and:

> **faster abort-enabled exit ≠ permission to treat the interrupted refresh as completed maintenance**.

This §4.27 obligation should remain distinct from the §4.9.5 FGR-grouping catch-up rule. Both can constrain the same broad entry/exit boundary, but they have different stated triggers and should not be silently merged into one generic `catch-up` concept.

Samsung's October 2014 DDR4 Device Operation document and Micron DDR4 product datasheets from 2017 document the same MR4 A9 / abort / no-counter-increment / extra-refresh interface behavior. They are implementation-facing continuity witnesses, not independent invention claims.

### The initial DDR4 standard does not freely compose FGR with temperature-controlled refresh

In JESD79-4 §4.9.4, Temperature Controlled Refresh may be enabled only with normal fixed 1x. Selecting another FGR mode requires Temperature Controlled Refresh to be disabled.

This is a useful historical boundary against treating every refresh optimization as an orthogonal switch:

> **temperature-conditioned refresh ≠ automatically composable with every fine-granularity mode**.

Later revisions and products may change the composition and must be sourced separately.

## Prior-art boundary

DDR4 did **not** invent the general idea of shifting refresh commands in time. IBM's 2010 MICRO paper `Elastic Refresh` already describes exploiting the flexibility of then-current JEDEC DDRx specifications to postpone refresh operations and proposes workload-aware scheduling over that allowed range.

The defensible 2012 historical claim is narrower:

> JESD79-4 specifies a DDR4 composition of bounded postpone/pull-in accounting, 1x/2x/4x FGR timing regimes, explicit transition/self-refresh constraints, and an MR4-controlled Self Refresh Abort path in which an interrupted internal refresh does not receive refresh-counter progress.

Likewise, IBM's 2013 work does not invent JEDEC FGR; its own abstract describes FGR as a feature recently announced in the DDR4 specification and analyzes/adapts it.

No invention-priority claim is made for Self Refresh Abort, internal refresh counters, low-latency Self Refresh exit, or compensating refresh after a mode transition. Earlier DDR/LPDDR ancestry remains separate prior-art work.

## Retained state and lifetime split

At least nine state classes should remain distinct:

1. **DRAM payload state** — charge distinctions that ultimately need refresh;
2. **internal refresh-address state** — device-side row enumeration used when refresh executes;
3. **external schedule position** — how much ordinary refresh work has recently been postponed or pulled in;
4. **FGR mode state** — the selected fixed or on-the-fly 1x/2x/4x regime;
5. **recent FGR grouping position** — enough history to know whether an even/multiple-of-four transition constraint is satisfied;
6. **Self Refresh mode state** — internal autonomous retention mode whose entry/exit can create catch-up requirements;
7. **internal maintenance activity state** — whether an autonomous refresh has begun and may still be underway at Self Refresh exit;
8. **internal refresh-counter progress** — the protocol-visible distinction explicitly withheld when that ongoing refresh is aborted;
9. **re-entry obligation state** — the requirement that an extra refresh occur before a later Self Refresh entry after exit.

The specification does not prove that items 3, 5, 7, or 9 each correspond to one named physical register. They are logical/device-controller relations that must be maintained or derived well enough to obey the interface contract. Item 8 is stronger: the standard itself explicitly names a `refresh counter`, while still not exposing its circuit implementation.

## Engineering reconstruction

### A retention deadline can be represented as bounded scheduling slack

Case 03 establishes that DRAM persistence needs time-triggered regeneration. Case 69 adds that an interface may expose that obligation not as `one command exactly every nominal interval`, but as an average cadence plus a bounded deviation envelope.

The important invariant is therefore not one timestamp but a constrained relation among:

```text
nominal cadence
+ recent refresh schedule
+ postpone/pull-in bounds
+ maximum gap
+ active FGR mode
+ legal transition grouping
+ Self Refresh transition state
+ any still-open re-entry obligation
```

### Maintenance history can be compressed without becoming payload history

The controller does not need a complete log of every prior refresh forever. It needs only enough recent accounting to know what work is still owed, what work has been prepaid, and whether a mode transition is legal.

This gives a retention-specific relation:

> **refresh scheduling history can become retained control state without becoming retained application history**.

The exact hardware representation is outside the source boundary.

### Maintenance execution and maintenance credit are not the same event

Self Refresh Abort adds a sharper distinction than postpone/pull-in alone. An internal refresh may already be underway, yet the abort rule says the refresh counter does not advance.

The project therefore separates:

```text
maintenance activity
    != maintenance accounting progress
    != service admission after the transition
```

`Maintenance credit` is project vocabulary for the second relation; the historical source's exact language is the refresh counter not being incremented.

### Faster service restoration can leave preservation work outstanding

Ordinary `tXS` lets an internally started refresh complete; abort-enabled `tXS_ABORT` allows an earlier transition path by aborting that work. A later extra-refresh requirement remains before re-entering Self Refresh.

So:

> **lower exit latency ≠ disappearance of the interrupted maintenance obligation**.

This is not evidence that the aborted refresh was physically useless. It is evidence that the protocol does not count it as completed refresh progress.

### Maintenance can be moved or interrupted without becoming optional

Postponement, pull-in, FGR, Self Refresh, and Self Refresh Abort change temporal placement, authority, or completion treatment of maintenance. None turns dynamic cell retention into quiescent nonvolatility.

> **temporal flexibility of maintenance ≠ disappearance of the maintenance requirement**.

## Cross-case boundaries

### Versus Case 03 — basic DRAM refresh deadline

Case 03 establishes leakage plus periodic regeneration. Case 69 refines the externally visible scheduling relation: the nominal interval can have bounded elasticity, and an autonomous refresh may also be interrupted at a mode boundary without receiving counter progress. These are scheduling/transition-contract refinements, not different cell-retention physics.

### Versus Case 21 — AUTO REFRESH / SELF REFRESH authority handoff

Case 21 asks who generates recurring refresh work and how responsibility moves across Self Refresh entry/exit. Case 69 asks how externally issued refreshes can move in time, how FGR grouping can leave catch-up work across a Self Refresh boundary, and what happens when autonomous refresh work is already in progress at exit.

### Versus Case 33 — DDR5 Same Bank Refresh

Case 33 localizes **where** refresh blocks service. Case 69 changes **when/how frequently** refresh commands are scheduled and, at Self Refresh exit, whether an ongoing internal refresh is allowed to complete or is aborted.

> **temporal refresh scheduling ≠ spatial refresh localization**.

### Versus Case 106 — DDR5 REFsb maintenance accounting

Case 106 adds a later DDR5 rule in which a repeated same-bank refresh can refresh the same row again without advancing the global refresh counter. Case 69's 2012 rule is different: an **ongoing autonomous refresh is aborted** and the refresh counter does not increment.

The bounded functional comparison is:

> **maintenance-related activity ≠ maintenance-frontier/counter progress**.

This is not evidence that DDR4 Self Refresh Abort and DDR5 REFsb share an internal counter implementation or direct technical genealogy.

### Versus Case 34 — temperature-dependent refresh

Case 34 treats environmental measurement/policy as cadence-selection state. Case 69 supplies a specific 2012 interface boundary in which Temperature Controlled Refresh and non-1x FGR are not freely composable.

### Versus Cases 53–54 — RowHammer / RFM

Those cases add workload-induced maintenance urgency and a later host/device mitigation split. Case 69 concerns the ordinary data-retention refresh schedule and its bounded timing/transition flexibility. `Postponed REF`, aborted Self Refresh work, and an `RFM` opportunity are not interchangeable commands or histories.

## Failure and forgetting boundaries

Distinct failure modes include:

- external scheduling exceeds the allowed postponed-refresh count;
- a gap exceeds the mode-specific maximum interval;
- software/controller logic treats extra pull-ins beyond the cap as additional future exemption;
- recent 2x/4x grouping state is lost or miscomputed before a rate change;
- FGR mode changes without satisfying its sequence constraint;
- Self Refresh exit omits required FGR catch-up refresh work;
- an abort-enabled controller treats an interrupted internal refresh as if the refresh counter had advanced;
- a controller re-enters Self Refresh without satisfying the §4.27 extra-refresh requirement;
- software collapses the §4.9.5 FGR catch-up rule and the §4.27 re-entry rule without establishing that one concrete command sequence satisfies both;
- Temperature Controlled Refresh is combined with a disallowed FGR mode in the bounded 2012 contract;
- a controller retains correct payload data now but loses the schedule/transition state needed to guarantee future retention.

These are not all the same as immediate physical bit loss. Several are failures of retained **maintenance authority/accounting** that can later cause the physical retention guarantee to fail.

## Historical record / reconstruction / analogy ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| JESD79-4 defines average `tREFI` plus bounded postpone/pull-in | `H/P` | JEDEC 2012 §4.26 |
| 1x/2x/4x have different `tREFI` and `tRFC` timing regimes | `H/P` | JEDEC 2012 §4.9.2 |
| 2x/4x rate changes have even/multiple-of-four sequencing constraints | `H/P` | JEDEC 2012 §4.9.3 |
| some Self Refresh exits require extra FGR catch-up refreshes | `H/P` | JEDEC 2012 §4.9.5 |
| MR4 A9 already defines Self Refresh Abort in September 2012 | `H/P` | inspected MR4 table + §4.27 |
| aborting an ongoing refresh does not increment the refresh counter | `H/P` | JEDEC 2012 §4.27 |
| `tXS_ABORT` is a distinct command-admission timing from ordinary `tXS` | `H/P` | JEDEC 2012 §4.27 + timing table |
| at least one extra refresh is required before Self Refresh re-entry regardless of abort setting | `H/P` | JEDEC 2012 §4.27 |
| Samsung 2014 and Micron 2017 document the same interface behavior | `H/P` | manufacturer device/product documents |
| controller must retain a literal JEDEC-defined `refresh debt counter` | `X` | no such implementation requirement is established; `debt` is project vocabulary |
| recent refresh schedule is control state needed to obey the bounded contract | `E` | follows from postpone/pull-in and transition limits, representation unspecified |
| maintenance activity and maintenance-accounting progress are distinct relations | `E` | follows from explicit abort + no-counter-increment rule |
| an aborted refresh performed zero physical work | `X` | not established by interface-level source |
| one §4.27 extra REF automatically discharges every §4.9.5 FGR obligation | `X` | not established |
| FGR universally improves performance | `X` | IBM 2013 explicitly reports no one-size-fits-all mode |
| DDR4 invented refresh postponement or Self Refresh Abort | `X` | postponement has prior art; abort priority not researched |
| Case 69 and Case 106 use the same internal counter mechanism | `A/X` | functional comparison only; implementation identity unsupported |
| refresh debt resembles deferred repair/GC debt | `A` | functional analogy only; mechanisms and history differ |

## Philosophical interpretation — bounded

Case 69 adds one narrow conceptual pressure:

> Persistence can depend on a **bounded obligation whose execution is temporally movable or interruptible**, rather than on either quiescent endurance or perfectly periodic repetition.

The Self Refresh Abort rule sharpens the point: a maintenance process can already have begun yet still fail to become completed maintenance history under the system's own accounting rule. The relevant retained thing is therefore not only cell charge or physical activity, but an admissible relation between work performed, work credited, and work still owed.

Calling that relation `memory` would be too loose; calling it **retention-control state** keeps the mechanism visible.

The interpretation stops there. DDR4 refresh scheduling is not evidence that all maintenance is debt, that every interrupted action is forgetting, or that JEDEC engineers were theorizing philosophical retention.

## Sources

### Primary

- JEDEC Solid State Technology Association, **JESD79-4: DDR4 SDRAM**, September 2012, especially §§4.9, 4.26, and 4.27, MR4 on printed p. 20, Self Refresh exit/abort on printed p. 125, and Reset/Self Refresh timing on printed p. 190. JEDEC-authored PDF mirrored by Texas Instruments E2E: <https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/196/JESD79_2D00_4.pdf>.
- Samsung Electronics, **Device Operation — DDR4 SDRAM**, Rev. 1.1, October 2014, §2.27 Self Refresh Operation. Indexed manufacturer PDF URL: <https://image.semiconductor.samsung.com/resources/data-sheet/DDR4_Device_Operations_Rev11_Oct_14-0.pdf>.
- Micron Technology, **4Gb: x4, x8, x16 DDR4 SDRAM**, Rev. G, January 2017, Self Refresh / DLL switching sections; indexed copy: <https://www.alldatasheetde.com/html-pdf/928196/MICRON/MT40A512M8RH-075E/16466/71/MT40A512M8RH-075E.html>.
- Micron Technology, **8Gb: x4, x8, x16 DDR4 SDRAM**, Rev. M, October 2017, Self Refresh Abort section; indexed copy: <https://www.micron-electronic.com/pdf-80/mt40a1g8sa-075-h.pdf>.

### Independent / prior-art context

- Jeffrey Stuecheli, Dimitris Kaseridis, Hillery C. Hunter, Lizy K. John, **“Elastic refresh: Techniques to mitigate refresh penalties in high density memory,”** MICRO 2010. IBM Research record: <https://research.ibm.com/publications/elastic-refresh-techniques-to-mitigate-refresh-penalties-in-high-density-memory>.
- Janani Mukundan, Hillery Hunter, Kyu-Hyoun Kim, Jeffrey Stuecheli, José F. Martínez, **“Understanding and mitigating refresh overheads in high-density DDR4 DRAM systems,”** ISCA 2013, pp. 48–59. IBM Research record: <https://research.ibm.com/publications/understanding-and-mitigating-refresh-overheads-in-high-density-ddr4-dram-systems>.

## Related repositories

`tmzncty/computing-archaeology` was searched again for dedicated Fine Granularity Refresh / Self Refresh Abort coverage before this slice. None was found. Broader DDR refresh-interface and committee genealogy belongs there if developed; this case keeps only the retention-specific scheduling, transition, accounting, and compensation argument.
