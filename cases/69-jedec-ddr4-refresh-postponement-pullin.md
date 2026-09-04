# JEDEC DDR4 Refresh Postponement and Pull-In: Bounded Scheduling Elasticity, Fine-Granularity Refresh, and Maintenance Accounting

## Status

**`grounded`** — bounded to JEDEC's September 2012 DDR4 SDRAM standard, especially JESD79-4 §§4.9 and 4.26, with IBM's 2010 and 2013 refresh-scheduling work used as prior-art and independent engineering context.

Grounding record: [`../evidence/69-jedec-ddr4-2012-refresh-scheduling-grounding.md`](../evidence/69-jedec-ddr4-2012-refresh-scheduling-grounding.md).

## Scope

This case asks a narrow retention question:

> If DRAM must be refreshed periodically, does persistence require one refresh command at every exact nominal `tREFI` instant, or can maintenance work move in time while the retention obligation remains bounded and auditable?

The bounded object is the initial 2012 DDR4 refresh contract:

- the ordinary external `REF` command and average `tREFI` requirement;
- bounded postponement and bounded pull-in of refresh commands;
- the 1x/2x/4x Fine Granularity Refresh (FGR) modes;
- on-the-fly FGR rate changes and their sequencing restrictions;
- the interaction between FGR and Temperature Controlled Refresh in this revision;
- extra refresh work required after some Self Refresh entry histories.

This is **not**:

- a complete JEDEC DDR/DDR2/DDR3/DDR4/DDR5 refresh chronology;
- a claim that DDR4 invented refresh postponement, refresh scheduling, or DRAM refresh;
- a controller implementation study identifying the exact counter/register used to track postponed or pulled-in work;
- a claim that FGR always improves performance or reliability;
- a replacement for Cases 03, 21, 33, 34, 40, 43, 53, or 54.

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
- `Self Refresh entry and exit`.

Project phrases such as `maintenance debt`, `maintenance credit`, `schedule-control state`, and `temporal scheduling elasticity` are **engineering reconstructions**, not JEDEC vocabulary.

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

### The initial DDR4 standard does not freely compose FGR with temperature-controlled refresh

In JESD79-4 §4.9.4, Temperature Controlled Refresh may be enabled only with normal fixed 1x. Selecting another FGR mode requires Temperature Controlled Refresh to be disabled.

This is a useful historical boundary against treating every refresh optimization as an orthogonal switch:

> **temperature-conditioned refresh ≠ automatically composable with every fine-granularity mode**.

Later revisions and products may change the composition and must be sourced separately.

## Prior-art boundary

DDR4 did **not** invent the general idea of shifting refresh commands in time. IBM's 2010 MICRO paper `Elastic Refresh` already describes exploiting the flexibility of then-current JEDEC DDRx specifications to postpone refresh operations and proposes workload-aware scheduling over that allowed range.

The defensible 2012 historical claim is narrower:

> JESD79-4 specifies a DDR4 composition of bounded postpone/pull-in accounting together with 1x/2x/4x FGR timing regimes and explicit transition/self-refresh constraints.

Likewise, IBM's 2013 work does not invent JEDEC FGR; its own abstract describes FGR as a feature recently announced in the DDR4 specification and analyzes/adapts it.

## Retained state and lifetime split

At least six state classes should remain distinct:

1. **DRAM payload state** — charge distinctions that ultimately need refresh;
2. **internal refresh-address state** — device-side row enumeration used when `REF` executes;
3. **external schedule position** — how much ordinary refresh work has recently been postponed or pulled in;
4. **FGR mode state** — the selected fixed or on-the-fly 1x/2x/4x regime;
5. **recent FGR grouping position** — enough history to know whether an even/multiple-of-four transition constraint is satisfied;
6. **Self Refresh mode state** — internal autonomous retention mode whose entry/exit can create catch-up requirements.

The specification does not prove that items 3 and 5 are stored in named registers. They are **logical controller obligations**: a compliant controller must preserve or reconstruct the information needed to obey the schedule contract.

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
```

### Maintenance history can be compressed without becoming payload history

The controller does not need a complete log of every prior refresh forever. It needs only enough recent accounting to know what work is still owed, what work has been prepaid, and whether a mode transition is legal.

This gives a retention-specific relation:

> **refresh scheduling history can become retained control state without becoming retained application history**.

The exact hardware representation is outside the source boundary.

### Maintenance can be moved without becoming optional

Postponement, pull-in, FGR, and Self Refresh all change the temporal placement or authority of maintenance. None turns dynamic cell retention into quiescent nonvolatility.

> **temporal flexibility of maintenance ≠ disappearance of the maintenance requirement**.

## Cross-case boundaries

### Versus Case 03 — basic DRAM refresh deadline

Case 03 establishes leakage plus periodic regeneration. Case 69 refines the externally visible scheduling relation: the nominal interval can have bounded elasticity. This is a scheduling-contract refinement, not a different cell-retention mechanism.

### Versus Case 21 — AUTO REFRESH / SELF REFRESH authority handoff

Case 21 asks who generates recurring refresh work and how responsibility moves across Self Refresh entry/exit. Case 69 asks how externally issued refreshes can move in time and how FGR grouping can leave catch-up work across a Self Refresh boundary.

### Versus Case 33 — DDR5 Same Bank Refresh

Case 33 localizes **where** refresh blocks service. Case 69 changes **when/how frequently** refresh commands are scheduled in the bounded DDR4 regime.

> **temporal refresh scheduling ≠ spatial refresh localization**.

### Versus Case 34 — temperature-dependent refresh

Case 34 treats environmental measurement/policy as cadence-selection state. Case 69 supplies a specific 2012 interface boundary in which Temperature Controlled Refresh and non-1x FGR are not freely composable.

### Versus Cases 53–54 — RowHammer / RFM

Those cases add workload-induced maintenance urgency and a later host/device mitigation split. Case 69 concerns the ordinary data-retention refresh schedule and its bounded timing flexibility. `Postponed REF` and `RFM opportunity` are not interchangeable commands or histories.

## Failure and forgetting boundaries

Distinct failure modes include:

- external scheduling exceeds the allowed postponed-refresh count;
- a gap exceeds the mode-specific maximum interval;
- software/controller logic treats extra pull-ins beyond the cap as additional future exemption;
- recent 2x/4x grouping state is lost or miscomputed before a rate change;
- FGR mode changes without satisfying its sequence constraint;
- Self Refresh exit omits required catch-up refresh work;
- Temperature Controlled Refresh is combined with a disallowed FGR mode in the bounded 2012 contract;
- a controller retains correct payload data now but loses the schedule state needed to guarantee future retention.

These are not all the same as immediate physical bit loss. Several are failures of retained **maintenance authority/accounting** that can later cause the physical retention guarantee to fail.

## Historical record / reconstruction / analogy ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| JESD79-4 defines average `tREFI` plus bounded postpone/pull-in | `H/P` | JEDEC 2012 §4.26 |
| 1x/2x/4x have different `tREFI` and `tRFC` timing regimes | `H/P` | JEDEC 2012 §4.9.2 |
| 2x/4x rate changes have even/multiple-of-four sequencing constraints | `H/P` | JEDEC 2012 §4.9.3 |
| some Self Refresh exits require extra FGR catch-up refreshes | `H/P` | JEDEC 2012 §4.9.5 |
| controller must retain a literal JEDEC-defined `refresh debt counter` | `X` | no such implementation requirement is established; `debt` is project vocabulary |
| recent refresh schedule is control state needed to obey the bounded contract | `E` | follows from postpone/pull-in and transition limits, representation unspecified |
| FGR universally improves performance | `X` | IBM 2013 explicitly reports no one-size-fits-all mode |
| DDR4 invented refresh postponement | `X` | IBM 2010 documents earlier JEDEC DDRx postponement flexibility |
| refresh debt resembles deferred repair/GC debt | `A` | functional analogy only; mechanisms and history differ |

## Philosophical interpretation — bounded

Case 69 adds one narrow conceptual pressure:

> Persistence can depend on a **bounded obligation whose execution is temporally movable**, rather than on either quiescent endurance or perfectly periodic repetition.

The relevant retained thing is not only cell charge. A system must also maintain an admissible relation between past maintenance already performed and maintenance still owed. Calling that relation `memory` would be too loose; calling it **retention-control state** keeps the mechanism visible.

The interpretation stops there. DDR4 refresh scheduling is not evidence that all maintenance is debt, that every temporal obligation is memory, or that JEDEC engineers were theorizing philosophical retention.

## Sources

### Primary

- JEDEC Solid State Technology Association, **JESD79-4: DDR4 SDRAM**, September 2012, especially §§4.9 and 4.26, pp. 35–37 and 123–124. JEDEC-authored PDF mirrored by Texas Instruments E2E: <https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/196/JESD79_2D00_4.pdf>.

### Independent / prior-art context

- Jeffrey Stuecheli, Dimitris Kaseridis, Hillery C. Hunter, Lizy K. John, **“Elastic refresh: Techniques to mitigate refresh penalties in high density memory,”** MICRO 2010. IBM Research record: <https://research.ibm.com/publications/elastic-refresh-techniques-to-mitigate-refresh-penalties-in-high-density-memory>.
- Janani Mukundan, Hillery Hunter, Kyu-Hyoun Kim, Jeffrey Stuecheli, José F. Martínez, **“Understanding and mitigating refresh overheads in high-density DDR4 DRAM systems,”** ISCA 2013, pp. 48–59. IBM Research record: <https://research.ibm.com/publications/understanding-and-mitigating-refresh-overheads-in-high-density-ddr4-dram-systems>.

## Related repositories

`tmzncty/computing-archaeology` was searched for a dedicated Fine Granularity Refresh case before this slice. None was found. Broader DRAM standards/history belongs there if developed; this case keeps only the retention-specific scheduling/accounting argument.
