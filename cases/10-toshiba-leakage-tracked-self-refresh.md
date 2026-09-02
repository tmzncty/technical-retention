# Toshiba Leakage-Tracked Self-Refresh: Internalizing Refresh Scheduling

## Status

**`grounded`** — bounded to Toshiba's 1984-priority DRAM self-refresh control design disclosed in US4682306A.

Grounding record: [`../evidence/10-toshiba-1984-self-refresh-scheduling-grounding.md`](../evidence/10-toshiba-1984-self-refresh-scheduling-grounding.md).

## Scope

This case asks what changes when DRAM refresh no longer depends on an external controller for refresh cadence and instead uses an on-chip monitor of charge decay to decide when an intermittent refresh pass begins. It is not a general history of DRAM self-refresh and does not identify the patent embodiment with a named Toshiba commercial product.

Primary source: Takayasu Sakurai and Tetsuya Iizuka, Toshiba Corp., US4682306A, _Self-refresh control circuit for dynamic semiconductor memory device_; Japanese priority 20 August 1984, US filing 20 August 1985, publication 21 July 1987.

## Relation to Cases 03 and 09

Case 03 established the underlying relation: dynamic-cell charge leaks, so state must be reconstructed before a retention limit is crossed.

Case 09 then separated the refresh obligation from refresh-row enumeration. In the bounded TI CAS-before-RAS design, the on-chip counter supplies successive refresh-row addresses, but the external processor/controller still determines how often refresh requests occur.

US4682306A describes a different boundary. It places an oscillator and refresh-address counter on the memory chip and, in its preferred embodiment, starts the refresh sequence from the state of a leak-current monitor capacitor.

The comparison is therefore:

```text
Case 03: why refresh is required
Case 09: where the next refresh row comes from
Case 10: where refresh timing/trigger generation comes from
         and what condition determines the interval
```

## Historical vocabulary and record

The patent uses `self-refresh control circuit`, `self-refresh operation automatically`, `oscillator`, `refresh address counter`, `leak current monitor circuit`, and `intermittent type refresh circuit`.

It states that then-recent dynamic-memory technology could provide on-chip self-refresh and eliminate timing or address control circuitry formerly required outside the chip. It describes an oscillator that determines refresh frequency and a refresh-address counter that supplies memory-cell addresses during refresh.

The preferred embodiment contains a monitor capacitor designed to have characteristics similar to a memory cell. A detector observes the monitor-node voltage. When that voltage drops below a designed threshold, the control path starts the oscillator and resets/starts the refresh-address counter. Oscillator pulses advance the counter; refresh addresses go to the row decoder; the array is refreshed row by row; completion recharges the monitor capacitor so a new monitoring interval begins.

The patent explicitly says refresh occurs more often when monitored leakage is large and less often when it is small. It also states that the monitor capacitor may be designed with slightly more leakage than ordinary memory-cell capacitors to provide margin before information loss.

The patent itself cites Hitachi Japanese Laid-Open Patent 59-56291, priority 24 September 1982 and publication 31 March 1984, as earlier work that automatically controlled refresh frequency using leak-monitor capacitors and a comparator. This case therefore makes no priority claim for Toshiba.

## Retained state and maintenance state

The payload remains volatile dynamic-cell state. The refresh-address counter holds temporary maintenance-enumeration state during a refresh pass. The monitor capacitor holds a different kind of technical state: its controlled decay is observed as a proxy for how close the protected array may be to a retention boundary.

This gives a new retention relation:

> **retention infrastructure can preserve payload by intentionally allowing a proxy state to decay toward a maintenance threshold.**

`Proxy` is engineering reconstruction vocabulary, not Toshiba's historical term.

## Engineering reconstruction

### Refresh address internalization is not refresh schedule internalization

Case 09 demonstrates that a device can generate its own refresh row while still relying on an external source for refresh cadence. Case 10 provides a bounded design in which both row enumeration and the timing source/condition for starting refresh are on-chip.

### Maintenance can be condition-derived

The next refresh pass is not only a fixed external deadline event in the disclosed embodiment. A monitored electrical condition crosses a threshold and starts the maintenance sequence. The project term `condition-derived maintenance trigger` is a modern analytical description.

### A preservation system may use a state designed to approach failure first

The patent allows the monitor capacitor to leak slightly faster than ordinary cells. The monitor is therefore deliberately conservative: its decay should reach the control boundary before protected payload cells reach their loss boundary.

This makes the safety margin relational rather than merely a single nominal refresh-period number.

### Reducing maintenance frequency does not eliminate maintenance

The patent's motivation is lower standby power by avoiding refresh that is more frequent than required by the monitored condition. When refresh is needed, however, the disclosed design still performs the array-maintenance pass. Dynamic state has not become nonvolatile.

## Failure boundaries

The sourced mechanism separates several failure classes. A monitor that is not conservative enough can initiate maintenance too late; an overly conservative monitor can cause needless refresh and power cost; an incorrect threshold can reduce safety margin; and correct triggering still does not guarantee correct row enumeration or correct row restoration. These are engineering implications of the disclosed partition, not measured failure rates for a commercial Toshiba device.

## Functional analogy and anti-anachronism

`Adaptive refresh`, `condition-derived scheduling`, `proxy state`, and `sentinel` can be useful modern comparisons, but they are not presented as period Toshiba terminology. Historical claims remain in the patent's own vocabulary.

US4682306A is a manufacturer-primary design disclosure, not proof that a named Toshiba DRAM or pseudo-SRAM used the exact preferred embodiment. It also cannot support a `first adaptive self-refresh` claim because the patent itself identifies earlier Hitachi work.

Later SDRAM `AUTO REFRESH`, JEDEC self-refresh entry/exit, DDR per-bank refresh, temperature-compensated refresh, and modern retention-aware policies remain separate regimes.

## Philosophical limit

A bounded conceptual question follows from the mechanism: apparent persistence can be maintained by instrumenting an approaching loss condition and converting it into maintenance work. This is an interpretation of the engineering relation, not a historical claim that Toshiba engineers formulated a philosophy of retention or precarity.

## Cross-case result

The refresh-control decomposition is now:

```text
payload decay / retention constraint
    !=
condition monitor
    !=
maintenance trigger
    !=
active-pass timing source
    !=
row enumeration
    !=
row selection
    !=
sense / restoration
```

Case 09 grounds the separation between external trigger cadence and internal row enumeration. Case 10 grounds a disclosed design in which an on-chip monitored condition starts the oscillator/counter sequence.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Toshiba disclosed same-chip self-refresh with oscillator and refresh-address counter | H/P | US4682306A |
| A monitor capacitor and threshold can start the disclosed refresh sequence | H/P | US4682306A |
| Oscillator pulses advance the refresh-address counter through the refresh pass | H/P | US4682306A |
| The monitor may be designed with slightly greater leakage to provide margin | H/P | US4682306A |
| A named Toshiba commercial part is proven to use this exact circuit | X | unsupported product-identity leap |
| Toshiba invented adaptive refresh generally | X | blocked by the patent's own Hitachi prior-art discussion |
| Internal refresh addressing automatically implies internal refresh scheduling | X | contradicted by the Case-09/Case-10 comparison |
| A deliberately decaying proxy can trigger payload-preservation work | E | bounded reconstruction from the monitor role |

## Related repositories

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated treatment of this Toshiba leak-monitor self-refresh mechanism. A broader history of DRAM generations, pseudo-SRAM, oscillator design, process leakage, and later standards belongs there rather than being duplicated here.

`tmzncty/problem-history` remains the methodological guard against projecting later `adaptive refresh` or JEDEC terminology backward.

## Sources

1. Takayasu Sakurai and Tetsuya Iizuka, Toshiba Corp., US4682306A, _Self-refresh control circuit for dynamic semiconductor memory device_: <https://patents.google.com/patent/US4682306A/en>.
2. Hitachi Ltd., JPS5956291A, _MOS storage device_, priority 24 September 1982, publication 31 March 1984 — used here only through Toshiba's explicit prior-art description/citation unless independently inspected: <https://patents.google.com/patent/JPS5956291A/ja>.
3. H. Kawamoto et al., “A 288Kb CMOS Pseudo SRAM,” _ISSCC Digest of Technical Papers_, 1984, pp. 276–277, DOI 10.1109/ISSCC.1984.1156683 — period context cited by the patent, not a central mechanism source in this case.
