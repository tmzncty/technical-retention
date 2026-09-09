# Case 09 deepening — DRAM refresh-counter initialization, coverage, and testability

## Scope

This addendum deepens [`../cases/09-dram-cbr-refresh-address-internalization.md`](../cases/09-dram-cbr-refresh-address-internalization.md) at one narrow seam:

> **If an on-chip refresh counter is part of the machinery that keeps DRAM payload refreshed, what state does that counter itself retain, how is its progression made testable, and how long must that maintenance-control state survive?**

The bounded evidence is:

1. Texas Instruments, US4653030A, filed 31 August 1984, for a disclosed CAS-before-RAS on-chip refresh-counter circuit and its power-on state;
2. Motorola's 1989 *Memory Data* documentation for the MCM514256A / MCM51L4256A family, for a named commercial-device `CAS BEFORE RAS REFRESH COUNTER TEST` and the relation between counter-generated row addresses and full-array coverage.

This is **not** a general DRAM built-in-self-test history, a proof that TI's patent is the exact circuit used by Motorola, or a genealogy from one vendor to the other. It also does not turn a refresh counter into application history.

---

## Source custody and evidence class

### TI patent

US4653030A is manufacturer-primary patent evidence. It is useful here because the description exposes internal state transitions that ordinary product sheets need not expose.

The patent identifies Texas Instruments as assignee and describes eight refresh-counter stages coupled into the row-address path. It says a high-resistance device forces the relevant counter latch to a zero state at power-on, then states that the refresh-address counter starts at zero and is selectively incremented on each CAS-before-RAS refresh cycle.

Patent disclosure establishes a disclosed design and its intended operation. It does **not** by itself establish mass deployment in any named DRAM product.

### Motorola product documentation

Motorola's 1989 *Memory Data* documentation for MCM514256A / MCM51L4256A describes a commercial-device refresh interface and a specific `CAS BEFORE RAS REFRESH COUNTER TEST`. The page-preserving Bitsavers scan is manufacturer text preserved by a third-party archive; this addendum treats it as a vendor-primary document with archival mirror custody, not as independent field validation.

The documented test uses the internal refresh counter to generate the row address while the external address supplies the column address. The procedure repeats the counter-test operation across 512 cycles and then checks the written pattern through normal reads. The same section says the test is to be performed only after a minimum of eight CAS-before-RAS initialization cycles.

This directly exposes **counter progression and row-coverage behavior at the product interface**. It does not expose Motorola's transistor-level counter implementation or prove that it shares TI's power-on-zero circuit.

---

## Historical record

### H/P — TI's disclosed counter has an explicit power-on phase

US4653030A does more than say that an internal counter exists. In the disclosed counter stage, a high-resistance transistor forces the latch to zero at power-on; the description then says the refresh counter starts at zero. Successive CAS-before-RAS refresh requests increment the binary count.

That makes the counter's current phase a real sequential state of the disclosed maintenance path rather than a purely combinational derivation from the current external address.

The historical statement is deliberately source-bounded:

> **TI disclosed a power-on-zero refresh-counter embodiment.**

It is not:

> every CBR DRAM standardized the same power-on counter value.

### H/P — the commercial Motorola device exposes a counter test

Motorola documents the internal refresh counter as testable through a read-write sequence. During the test:

- the internal refresh counter generates the row address;
- the external address supplies the column address;
- check data are written as the counter progresses;
- 512 counter-test cycles span the documented 512-row array;
- normal reads are then used to check the resulting pattern;
- the procedure is specified only after at least eight CAS-before-RAS initialization cycles.

The important historical point is not merely that a counter existed. A vendor supplied an operational procedure for checking that its hidden maintenance enumerator progressed through the row set.

### H/P — test operation and ordinary refresh are not the same transaction

The documented counter test deliberately combines the counter-generated row address with an externally supplied column address and a read-write operation so that progression becomes observable in payload cells.

Ordinary CAS-before-RAS refresh, by contrast, uses the internal row address to perform row refresh and does not need an ordinary column data transaction.

Therefore:

> **counter-test visibility != ordinary refresh semantics.**

The diagnostic procedure makes internal maintenance state observable by temporarily coupling it to controlled data writes; it does not show that normal refresh stores counter history in user data.

---

## Engineering reconstruction

### E — maintenance-control state has its own retention horizon

Case 09 already treats the refresh count as maintenance-control state: its current value determines which row will be selected on a subsequent refresh request.

The TI power-on behavior adds an important boundary. In the disclosed embodiment, the counter phase is not preserved as a durable cross-power record; it is deliberately initialized at power-on. That is compatible with the regime it serves because ordinary DRAM payload retention itself is not specified to survive removal of operating power.

So the stronger project rule is:

> **state that organizes retention does not automatically need the same persistence horizon or failure model as the logical payload relation it supports.**

For this bounded DRAM case, counter continuity matters while the powered refresh regime is active. Cross-power preservation of the counter phase is not established as an obligation.

### E — correct refresh cadence and correct coverage are separate obligations

The existing Case 09 evidence already separates the external refresh scheduler from the on-chip row enumerator. The counter test sharpens that split:

```text
external cadence
    asks for refresh cycles often enough

internal counter progression
    distributes those cycles across rows
```

A scheduler can issue enough cycles while a defective enumerator fails to cover the row set. Conversely, a correctly progressing counter cannot rescue data if external logic misses the physical retention deadline.

Thus:

> **enough refresh requests != verified row coverage**

and

> **correct row coverage != proof that the deadline was met.**

### E — test evidence is evidence about the maintenance path, not a durable certificate

The Motorola procedure creates an observable pattern that can reveal whether counter progression covered the expected rows during the test. Once the test is over, that check pattern is not a persistent certificate that all future refresh cycles will remain correct.

This blocks another shortcut:

> **successful maintenance-path test != continuing maintenance correctness.**

The distinction is the same one the repository uses elsewhere between a verification event and indefinite future qualification.

### E — a cyclic enumerator is not a history log

A refresh counter retains only enough phase to select a next row in a cyclic maintenance sequence. It does not retain the sequence of all prior rows as a history.

Even when test code can infer that a full traversal occurred, that does not turn the counter into a log of past refreshes.

> **maintenance phase != maintenance history.**

---

## Functional comparison

### A — Case 83 HDFS scanner cursor: same broad role, different persistence contract

[`../cases/83-apache-hdfs-block-scanner-checksum-verification.md`](../cases/83-apache-hdfs-block-scanner-checksum-verification.md) also contains retained state that organizes maintenance traversal: the HDFS scanner cursor remembers where a volume scan should continue.

The analogy is useful only at the functional level:

- both are control state used to distribute maintenance work across a larger payload population;
- both can fail independently of the payload bytes they are intended to help preserve.

But their persistence contracts differ sharply. HDFS tries to checkpoint scanner progress so process/restart recovery need not repeat the whole traversal. The TI DRAM patent instead initializes the refresh-counter phase at power-on; no cross-power preservation of that phase is required by the disclosed scheme.

Therefore:

> **maintenance-control state != one universal checkpoint semantics.**

This comparison establishes neither DRAM→HDFS genealogy nor a common implementation mechanism.

### A — Case 10 autonomous timing remains a different control function

[`../cases/10-toshiba-leakage-tracked-self-refresh.md`](../cases/10-toshiba-leakage-tracked-self-refresh.md) deepens a different function: how refresh *timing* can move on-chip and become condition-derived. The present Case 09 addendum concerns initialization and verification of the *row enumerator*.

So:

> **refresh-counter initialization/testability != autonomous refresh scheduling.**

---

## Philosophical interpretation

### I — retention infrastructure can have a shorter-lived state than the retention relation it serves

The exact technical fact is modest: a powered DRAM retention regime can depend on a stateful refresh enumerator whose phase is initialized rather than durably preserved across power loss.

This clarifies a general project question about nested retention without turning it into metaphor. Technical persistence can depend on auxiliary states with different required lifetimes. A dependency is constitutive without thereby needing indefinite or even cross-restart persistence.

The interpretation stops there. This evidence does not show that machines `remember how to remember`, does not make the refresh counter an archive, and does not establish a general law that maintenance metadata are always disposable.

---

## Claim ledger

| Claim | Label | Evidence |
| --- | --- | --- |
| TI's disclosed CBR refresh counter starts from a power-on-zero state | `H/P` | US4653030A description of counter-stage initialization and progression |
| TI's counter increments as CBR refresh requests occur | `H/P` | US4653030A counter/carry description |
| Motorola documents a CBR refresh-counter test on MCM514256A / MCM51L4256A | `H/P` | Motorola 1989 *Memory Data*, product section |
| The Motorola test uses internal row selection plus external column selection and controlled read-write data | `H/P` | Motorola counter-test procedure |
| The Motorola procedure uses 512 cycles to exercise the documented row set and requires prior CBR initialization cycles | `H/P` | Motorola counter-test text |
| Motorola's product counter is proven to use TI's power-on-zero transistor circuit | `X` | unsupported cross-vendor implementation identity |
| A successful counter test proves all later refresh deadlines will be met | `X` | test covers bounded counter progression, not indefinite scheduler correctness |
| The refresh count is application history | `X` | it is cyclic maintenance-control state, not a log |
| Maintenance-control state must always persist as long as application payload | `X` | contradicted by the bounded TI power-on initialization relation |
| Maintenance-control state can have a regime-specific persistence horizon | `E` | bounded reconstruction from disclosed counter role and initialization |
| DRAM refresh counter and HDFS scanner cursor are the same checkpoint mechanism | `A/X` | functional analogy only; persistence and authority semantics differ |

---

## Open questions

- direct product-specific evidence for the exact TMS4256/TMS4257 counter initialization value remains open;
- Motorola's transistor-level implementation is not inferred from TI's patent;
- this pass does not establish invention priority for refresh-counter test modes or on-chip refresh counters;
- later SDRAM/DDR refresh commands, per-bank refresh, temperature-compensated refresh, and retention-aware refresh remain separate cases;
- fault-injection or silicon-level validation of a stuck/skipped refresh-counter fault remains open;
- broad DRAM test/history genealogy belongs primarily in `tmzncty/computing-archaeology` if developed.

---

## Sources

1. Tadashi Tachibana, Chitranjan N. Reddy, Ngai H. Hong, `Self refresh circuitry for dynamic memory`, US4653030A, filed 31 August 1984, assigned to Texas Instruments: <https://patents.google.com/patent/US4653030A/en>.
2. Motorola, *Memory Data*, 1989, MCM514256A / MCM51L4256A product section, especially `REFRESH CYCLES` and `CAS BEFORE RAS REFRESH COUNTER TEST`, printed pp. 2-77 onward in the archived data book: <https://www.bitsavers.org/components/motorola/_dataBooks/1989_DL113r6_Motorola_Memory_Data.pdf>.

### Source-boundary note

The TI patent is used for the disclosed circuit's power-on state and increment mechanism. The Motorola product data are used for product-level counter-test semantics. They are **not** fused into one implementation genealogy.
