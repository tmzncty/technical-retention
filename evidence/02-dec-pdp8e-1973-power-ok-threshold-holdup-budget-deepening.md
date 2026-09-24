# Case 02 deepening — DEC PDP-8/E 1973 `POWER OK` thresholds and hold-up budget

**Case:** [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md)  
**Case status:** `grounded`  
**This record:** bounded evidence deepening; no maturity promotion  
**Primary historical anchor:** Digital Equipment Corporation, *PDP-8/E, PDP-8/F & PDP-8/M Maintenance Manual, Volume 1: Processor*, DEC-8E-HMM1A-D-D, 7th Printing (Rev.), September 1973  
**Question:** the existing PDP-8/E power-fail packet establishes that loss of `POWER OK` halts normal timing while the current core-memory WRITE is allowed to finish. What concrete electrical evidence caused `POWER OK` to be withdrawn, and what quantitative supply-level hold-up envelope was documented around line-power loss?

---

## Why this slice

The existing Case 02 packet already closes the qualitative in-flight rule:

```text
POWER OK lost
    -> stop normal timing
    -> keep X/Y core drive long enough to complete WRITE
    -> then withdraw current-source capability
```

But that packet deliberately left the electrical trigger quantitative boundary open. Its non-claims included:

- the exact voltage level corresponding to the memory-side `POWER OK` transition;
- the analog supply decay relation around that transition;
- a numeric slow-off delay.

The same September-1973 DEC maintenance manual contains a separate power-supply / voltage-monitor description that closes part, but not all, of that debt.

This record therefore does **not** repeat the destructive-read / restore explanation. It deepens the boundary between:

```text
line-power loss
    != regulated-rail threshold crossing
    != POWER OK withdrawal
    != memory-cycle closure
    != current-source shutdown
```

---

## Source identity and custody

### H/P — DEC maintenance manual

Primary source:

- Digital Equipment Corporation;
- *PDP-8/E, PDP-8/F & PDP-8/M Maintenance Manual, Volume 1: Processor*;
- DEC-8E-HMM1A-D-D;
- 7th Printing (Rev.), September 1973;
- copyright 1971, 1972, 1973 Digital Equipment Corporation.

Archival / catalogue access:

- Bitsavers PDF: <https://bitsavers.org/pdf/dec/pdp8/pdp8e/DEC-8E-HMM1A-D-D_PDP-8e_Maintenance_Manual_Volume_1_Processor_Sep73.pdf>
- MANX catalogue record identifying the same DEC part number and September-1973 edition: <https://manx-docs.org/details.php/1%2C4017>
- searchable text mirror used to locate the relevant paragraphs: <https://device.report/m/f543be6c683c3e08d16eca14f854b69311c27dc3ca837af500c7ec6e85aed20a>
- H724 supply-section mirror used to cross-check the voltage-monitor text: <https://deramp.com/downloads/mfe_archive/011-Digital%20Equipment%20Corporation/02%20PDP-8e/02%20PDP-8e%20Chassis/H724%20PDP-8e%20Power%20Supply/01%20Documentation/H724%20Power%20Supply.pdf>

Relevant manual locations:

- §3.26.4 — memory **Power Fail Circuitry**;
- Figure 3-127 and surrounding voltage-monitor discussion — `POWER OK` rail limits;
- §4.8.2 — **Hold-Up Time**.

### Source-use boundary

This is a named DEC production-family maintenance source. It is strong evidence for the documented PDP-8/E-family implementation and service specification.

It does not by itself establish:

- an oscilloscope trace from a particular field machine;
- a worst-case aged-component distribution;
- the exact elapsed time between `POWER OK` withdrawal and X/Y current removal;
- a universal PDP-8-family power-fail architecture;
- or a universal magnetic-core brownout law.

---

## Historical / implementation record

### H/P — `POWER OK` is derived from explicit regulated-rail limits

The DEC voltage-monitor discussion around Figure 3-127 gives concrete rail conditions for `POWER OK`.

When all monitored regulated voltages remain above their limits, the monitor keeps `POWER OK` asserted at approximately 4.3 V. The manual describes `POWER OK` being driven to ground when any of these monitored conditions fails:

```text
-15 V rail becomes more positive than -13.5 V
or
+15 V rail becomes more negative than +12 V
or
+5 V rail becomes more negative than +4.3 V
    -> POWER OK goes to ground
```

These are historical circuit/service values from DEC's manual. They are not project-defined thresholds.

This materially sharpens the earlier Case 02 statement `when dc voltage drops too low` into a named implementation trigger surface.

### H/P — `POWER OK` is a control signal, not a claim that magnetic state has already failed

Section 3.26.4 says the memory power-fail circuitry responds to the power supply's `POWER OK` signal. When the supply senses an unsafe drop, the line is grounded and the timing chain is shut off, while the memory cycle is nevertheless completed and X/Y current-source turn-off is delayed sufficiently to complete WRITE.

Placed beside Figure 3-127, the historical chain is therefore:

```text
regulated-rail condition reaches monitor limit
    -> POWER OK withdrawn
    -> timing chain halted
    -> already-active memory cycle still reaches WRITE closure
    -> X/Y current source then turns off
```

The manual does **not** say that crossing a `POWER OK` threshold means the ferrite state has already decayed. The signal is part of a protective transition policy.

### H/P — DEC also specifies a supply-level hold-up interval

In the H724 power-supply maintenance section, §4.8.2 states that, under maximum-load conditions, the regulated output voltages should remain stable for a **minimum of 2 ms after loss of line voltage**.

This is a quantitative supply-level service specification.

Its reference event is important:

```text
loss of line voltage
    -> regulated outputs remain stable >= 2 ms under maximum load
```

The manual does **not** define this as:

```text
POWER OK withdrawn
    -> exactly 2 ms remain
```

Those are different event boundaries.

### H/P — the memory-side power-fail circuit remains a separate slow-off stage

DEC separately characterizes the memory power-fail path as a `fast-on/slow-off` behavior: core current is enabled promptly when power is good, but its removal is delayed after power becomes bad so that the WRITE phase can complete.

Therefore the manual exposes at least three distinct layers around the transition:

```text
line / supply behavior
    -> voltage-monitor decision (`POWER OK`)
    -> memory-side completion / current-source shutdown behavior
```

The source does not collapse them into one timer.

---

## Engineering reconstruction

Everything in this section is repository terminology, not DEC's historical vocabulary unless marked above.

### E — failure detection is an admission boundary, not proof of payload failure

The new evidence supports a more precise relation:

```text
rail threshold crossed
    != core payload already lost

rail threshold crossed
    -> protective authority changes
```

`POWER OK` can therefore be reconstructed as a **transition-authority signal**: it says that normal progression should no longer be admitted under the present electrical condition. It is not a measurement of remanent core-bit correctness.

### E — electrical hold-up is a temporary completion resource

The supply does not jump from nominal power to zero capability at the instant line voltage disappears. The documented hold-up interval gives the system a bounded electrical envelope in which control logic can react.

For Case 02, that supports:

```text
upstream power source lost
    != completion capability disappears immediately
```

The memory-side slow-off mechanism then uses the still-available electrical capability to close an already-admitted WRITE before current drive is withdrawn.

This is a **functional decomposition**, not a claim that all 2 ms are reserved for core-memory restore.

### E — do not subtract unlike clocks

It would be tempting to write:

```text
2 ms hold-up
- memory-cycle / power-fail time
= exact safety margin
```

This record explicitly rejects that arithmetic without further evidence.

The 2 ms specification is referenced to **loss of line voltage** under a stated load condition. `POWER OK` changes when monitored regulated rails reach their own limits. The memory-side current-source slow-off interval begins from a control transition within that analog trajectory. The inspected source does not establish that all of those reference points are coincident.

Therefore:

```text
supply hold-up duration
    != post-POWER-OK residual duration
    != memory slow-off delay
    != measured worst-case restore margin
```

### E — retention across power loss is layered

The bounded PDP-8/E case can now be decomposed as:

```text
quiescent magnetic remanence
    +
voltage-monitor thresholding
    +
withdrawal of normal timing/admission
    +
continued completion capability for current WRITE
    +
subsequent current-source shutdown
```

The first item is a medium property. The others are system-transition controls.

This is why `core memory is nonvolatile` is insufficient to describe the machine-level retention contract.

---

## Functional comparisons

These are functional analogies only. They are not historical or implementation genealogies.

### A — Case 86 / emergency-save systems

A power-fail system that uses residual energy or time to copy broader processor state before shutdown shares the abstract shape:

```text
failure detected
    -> finite completion opportunity remains
```

But the Case 02 PDP-8/E memory mechanism here is narrower: it protects closure of an already-active core-memory WRITE path. It does not by itself prove preservation of complete processor execution state.

### A — DRAM / Flash / distributed maintenance

Later systems may likewise separate:

```text
stop admitting new work
    != revoke all completion capability immediately
```

The physical means differ radically: capacitor charge, Flash program/erase state machines, journals, replication protocols, or distributed repair are not magnetic-core current sources.

The analogy is only the control relation.

---

## Philosophical interpretation

The bounded project-level interpretation is that **power loss is not necessarily one instantaneous technical event**.

For this DEC implementation, the evidence exposes multiple boundaries:

- external line power can be lost;
- regulated rails can still remain within an acceptable envelope for a bounded interval;
- a monitor can withdraw permission for normal timing;
- an already-started reconstructive write can still be allowed to finish;
- only then can the core-drive capability be withdrawn.

Technical continuity here is therefore partly produced by the ordering of boundary transitions, not only by the long-lived material state.

This is a project interpretation. It is not a claim that DEC formulated a general philosophy of retention or failure semantics.

---

## Explicit non-claims

This packet does **not** claim:

1. that the three rail limits are universal magnetic-core thresholds;
2. that every PDP-8-family supply used exactly these values;
3. that a rail touching one limit immediately corrupts core bits;
4. that `POWER OK` directly measures ferrite remanence;
5. that the 2 ms hold-up interval starts at `POWER OK` withdrawal;
6. that the memory slow-off delay is numerically 2 ms;
7. that `2 ms - 1 ms` or any similar subtraction is an established safety margin;
8. that all H724 units in the field met the service value after aging or repair;
9. that arbitrary oscillatory brownouts are covered by the documented path;
10. that all destructive-read phases have been independently fault-injected;
11. that the manual proves a durable external `restore complete` indication;
12. that retained core payload implies retained processor/control state;
13. that DEC invented voltage-monitored drain-before-withdraw behavior;
14. that later persistence-domain or crash-consistency vocabulary was used by DEC in 1973.

---

## What this closes

Relative to the preceding PDP-8/E current-cycle packet, this slice closes two source-level debts:

```text
What did `POWER OK` mean electrically?
    -> explicit regulated-rail monitor limits are documented

Was there a quantitative supply-level interval after line-power loss?
    -> >= 2 ms regulated-output hold-up is specified under maximum load
```

It does **not** close the remaining timing chain:

```text
line loss time
    -> exact POWER OK transition time
    -> exact X/Y-current slow-off interval
    -> measured WRITE-complete margin
```

Those event-to-event timings remain open.

---

## Maturity / next debt

Case 02 remains **`grounded`**. No maturity promotion is justified by one additional 1973 maintenance-manual slice.

The next highest-value evidence is no longer another generic statement that core survives power-off. It is one of:

1. an engineering drawing / timing specification that gives the numeric delay between `POWER OK` loss and X/Y current-source removal;
2. a phase-specific fault trace showing power failure during READ, sense/register capture, and WRITE/restore;
3. a counterexample controller that chooses immediate abort or a different completion policy;
4. field or service measurements that distinguish nominal design margin from aged-machine behavior.

`tmzncty/computing-archaeology` was searched for `H724` in this round and no dedicated packet was found. Broader PDP-8/E power-supply history should remain there if developed; this file stays limited to the retention boundary above.
