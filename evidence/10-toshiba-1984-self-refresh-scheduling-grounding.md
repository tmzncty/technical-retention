# Evidence 10 — Toshiba 1984 Leakage-Tracked Self-Refresh Scheduling

## Purpose

Ground a narrow post-Case-09 DRAM bridge: a period manufacturer-primary design in which refresh **row enumeration and refresh timing generation are both on-chip**, and the start of an intermittent refresh pass is derived from the decay of a monitor capacitor designed to track memory-cell leakage.

This record does **not** claim that the disclosed patent circuit is the exact implementation of a named Toshiba commercial DRAM or pseudo-SRAM product, and it does not claim priority for adaptive self-refresh as a whole.

---

## Source identity

### Primary source

Takayasu Sakurai and Tetsuya Iizuka, assigned to Toshiba Corp., **US4682306A, _Self-refresh control circuit for dynamic semiconductor memory device_**.

- Japanese priority: **20 August 1984** (`JP59-172754` / `JPS6150287A` family).
- US filing: **20 August 1985**.
- US publication: **21 July 1987**.
- Google Patents transcription and figures: <https://patents.google.com/patent/US4682306A/en>.

Useful locations in the published description:

- opening background: on-chip `self-refresh`, oscillator, refresh-address counter, and removal of formerly external timing/address control;
- prior-art discussion: fixed oscillator frequency, temperature/leakage relation, refresh power, and Japanese Laid-Open Patent 59-56291;
- Fig. 1 discussion: leak-current monitor capacitor, inverter threshold detector, control circuit, self-excited oscillator, refresh-address counter, row decoder;
- Fig. 2 / Fig. 1 operation: monitor-node decay starts oscillator and counter; counter overflow ends the pass and recharges the monitor capacitor;
- Fig. 3 discussion: gated ring oscillator;
- later discussion: intermittent refresh, threshold setting, and deliberately higher monitor-capacitor leakage for margin.

### Prior-art control inside the primary source

The Toshiba patent itself cites **Japanese Laid-Open Patent 59-56291**, Hitachi Ltd., priority 24 September 1982, publication 31 March 1984, as an earlier memory device that automatically controlled refresh frequency using two leak-current monitor capacitors and a comparator.

Therefore:

> **US4682306A is a strong mechanism witness for the bounded Toshiba design; it is not evidence that Toshiba invented leakage-aware or adaptive refresh in general.**

The patent also cites H. Kawamoto et al., **“A 288Kb CMOS Pseudo SRAM,”** ISSCC 1984, pp. 276–277, as period context. This record does not rely on an uninspected full text of that paper for central claims.

---

## Direct historical claims

### H/P — the period source distinguishes self-refresh from formerly external control

The patent says that then-recent dynamic-memory technology could provide a `self-refresh circuit` on the same chip so that memory cells could refresh automatically and eliminate timing or address control circuitry formerly required outside the chip.

It describes the conventional on-chip self-refresh arrangement as containing:

- an oscillator that determines refresh frequency;
- a refresh-address counter that designates memory-cell addresses during standby / non-read-write periods.

This is the direct period contrast Case 09 lacked. Case 09's TI design internalized row enumeration but explicitly left CAS-before-RAS request cadence to an external processor/controller. The Toshiba source explicitly describes an on-chip timing source as part of self-refresh.

### H/P — the patent treats fixed-rate self-refresh as a power problem

The background states that MOS oscillator speed varies with temperature while memory-cell leakage increases with temperature. It argues that designing one fixed oscillator rate for a high-temperature worst case produces unnecessarily frequent low-temperature refresh and therefore unnecessary standby power.

The quantitative statements in that paragraph — including the claimed rough doubling of cell leakage per 10 °C and the example fixed oscillator margin — are **source-specific period engineering statements**, not adopted here as timeless universal laws for all DRAM processes.

### H/P — a monitor capacitor controls when refresh begins

In the preferred embodiment, a leak-current monitor circuit contains capacitor 1 and transfer gate 2. The patent says the monitor capacitor is designed to have characteristics similar to a memory cell.

A CMOS inverter watches the monitor-node voltage. When the voltage falls below a predetermined threshold:

1. the inverter/control path changes state;
2. refresh-address counter 15 is reset;
3. self-excited oscillator 14 starts;
4. oscillator pulses advance the refresh-address counter;
5. the counter produces refresh addresses for the row decoder;
6. memory cells are refreshed during the pass;
7. counter overflow terminates the pass through the second control path and recharges the monitor capacitor.

This establishes a closed bounded sequence:

```text
monitor capacitor charged
    -> monitor state decays by leakage
    -> threshold crossing
    -> on-chip oscillator starts
    -> refresh-address counter walks rows
    -> full refresh pass completes
    -> overflow recharges monitor capacitor
    -> monitoring interval begins again
```

### H/P — refresh frequency follows the monitored leakage condition

The patent explicitly states that refresh occurs more often when monitored leakage is large and less often when leakage is small. Its Fig. 1 embodiment is described as an `intermittent type refresh circuit`: the oscillator starts after the monitor voltage falls below the threshold, and the memory cells are then refreshed one after another.

The important historical fact is not a modern label such as `adaptive controller`; it is the sourced coupling between a monitored leakage proxy and the interval before the next refresh pass.

### H/P — the monitor can be biased toward safety margin

The patent states that the monitor capacitor may be designed with **slightly more leakage current than ordinary memory-cell capacitors**. It presents this as a way to refresh with enough margin to prevent information loss.

That is unusually useful retention evidence because the maintenance schedule is not merely derived from a nominal timer. The control state can be engineered to decay conservatively relative to the protected payload.

---

## Engineering reconstruction

### E — refresh-address internalization ≠ refresh-schedule internalization

Case 09 decomposed refresh into:

```text
physical retention deadline
scheduler / cadence
trigger
row enumeration
row selection
sense / restoration
```

The TI CBR case internalized **row enumeration** while leaving the request cadence external. The Toshiba design adds an on-chip oscillator and a monitor-derived trigger path.

Therefore the two migrations must remain distinct:

> **moving the next refresh row on-chip is not the same design change as moving the decision/timing for when refresh should run on-chip.**

### E — autonomous self-refresh can be condition-derived rather than fixed-rate

The patent's disclosed maintenance is not simply `internal periodic timer -> refresh`. A proxy electrical state is allowed to decay until a threshold condition starts a burst/pass of refresh operations.

A useful modern engineering description is **condition-derived / leakage-tracked maintenance scheduling**. This is reconstruction vocabulary, not a recovered 1984 actor term.

### E — retention infrastructure can depend on a proxy state that is deliberately allowed to decay

The monitor capacitor is not application data. Its value matters because it stands in for how close protected dynamic cells may be to an unsafe retention condition.

Thus the retention system contains a second state with a different role:

- **payload state** — information in DRAM cells that should remain logically recoverable;
- **proxy / sentinel state** — monitor-capacitor charge whose decay is intentionally observed to decide when preservation work should begin.

`Proxy` and `sentinel` are project reconstruction terms. The historical source says `leak current monitor circuit` / capacitor.

### E — the safety margin can be encoded in the relation between proxy and payload

Designing the monitor capacitor to leak slightly faster than ordinary memory cells makes the monitor cross its threshold earlier than a representative payload cell would reach its loss point.

The resulting retention guarantee is relational:

```text
monitor-decay envelope
    must remain conservative relative to
payload-cell decay envelope
```

This is more precise than saying only that `DRAM has a refresh interval`.

### E — reducing refresh work ≠ eliminating refresh work

The patent seeks lower standby power by avoiding unnecessarily frequent refresh. Yet once triggered, the disclosed scheme still drives the counter through the word-line set and performs refresh work.

So:

> **maintenance-frequency optimization does not convert dynamic storage into maintenance-free or nonvolatile storage.**

---

## Failure / forgetting implications

These are architecture-level failure classes inferred from the disclosed partition, not measured failure-rate claims for a commercial product.

### Proxy mismatch — late trigger

If the monitor state decays more slowly than the most vulnerable payload cells under relevant conditions, the trigger can arrive too late. Payload may cross its retention limit before maintenance begins.

### Proxy mismatch — early trigger

If the monitor is too conservative, refresh begins earlier/more often than required. The likely first-order cost is extra standby power / maintenance activity rather than immediate payload loss.

### Threshold / margin error

A threshold or monitor design that fails to maintain the intended conservative relation can shrink the safety margin.

### Oscillator or counter failure

Correct trigger detection is insufficient if the oscillator does not run, the counter does not enumerate rows correctly, or the row-refresh path does not restore the selected cells.

This reinforces Case 09's decomposition: **trigger correctness, enumeration correctness, and restoration correctness are separate obligations.**

---

## Anti-anachronism and evidence limits

### Historical vocabulary retained

Direct source terms include:

- `self-refresh control circuit`;
- `self-refresh operation automatically`;
- `oscillator`;
- `refresh address counter`;
- `leak current monitor circuit`;
- `intermittent type refresh circuit`.

### Modern analytical terms only

The following are useful project vocabulary but are **not** presented as Toshiba's historical terminology:

- `adaptive refresh`;
- `closed-loop maintenance`;
- `sentinel state`;
- `proxy state`;
- `condition-derived scheduling`;
- `offload`.

### Patent disclosure ≠ commercial-product implementation

No claim is made that US4682306A is the exact circuit of a named Toshiba DRAM or pseudo-SRAM product. The case is grounded as a **manufacturer-primary disclosed design regime**, not as a product genealogy.

### Patent mechanism ≠ invention priority

The patent itself describes Hitachi Japanese Laid-Open Patent 59-56291 as prior art that automatically controls refresh frequency using leakage-monitor capacitors. The project therefore makes no `first adaptive self-refresh` claim.

### One process statement ≠ universal DRAM law

Temperature/leakage factors and power numbers quoted in the patent belong to its period engineering argument. They are not generalized across later DRAM generations without separate sources.

---

## Related-repository duplication check

A current code search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `self refresh`, `self-refresh`, and the Toshiba patent/circuit terms found no dedicated case for this mechanism.

A broad history of DRAM self-refresh, pseudo-SRAM, oscillator design, process scaling, and JEDEC command evolution still belongs there if developed. `technical-retention` keeps only the retention-specific comparison about **where the scheduler lives and what state triggers preservation work**.

---

## Grounding decision

**Status: `grounded` for this bounded disclosed design.**

Reason:

- manufacturer-primary period source;
- precise priority/publication identity;
- period vocabulary;
- explicit block-level mechanism and operation sequence;
- explicit prior-art boundary that prevents a false priority claim;
- maintenance, power, address, trigger, failure, and safety-margin consequences can be reconstructed without assigning the design to an unproved commercial model;
- related-repository duplication checked.

This does **not** ground a general history of autonomous DRAM self-refresh. SDRAM `AUTO REFRESH`, later JEDEC self-refresh entry/exit, per-bank refresh, temperature-compensated refresh, retention-aware scheduling, and modern DDR policies remain separate cases.
