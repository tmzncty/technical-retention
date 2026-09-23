# Case 02 deepening — DEC PDP-8/E 1973 power-fail current-cycle closure

**Case:** [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md)  
**Case status:** `grounded`  
**This record:** bounded evidence deepening; no maturity promotion  
**Primary historical anchor:** Digital Equipment Corporation, *PDP-8/E, PDP-8/F & PDP-8/M Maintenance Manual, Volume 1: Processor*, DEC-8E-HMM1A-D-D, 7th Printing (Rev.), September 1973  
**Question:** when power becomes unsafe during a destructive-read / rewrite core-memory cycle, does a named production controller merely stop new work, or does it deliberately allow the current cycle to reach its write/restore closure before removing core drive current?

---

## Why this slice

The Case 02 evidence chain already separates several properties that are often collapsed into the adjective `nonvolatile`:

```text
remanent state at rest
    !=
read invariance
    !=
restore completion
    !=
power-transition immunity
    !=
whole-machine restart continuity
```

The immediately preceding Victor 1974–1975 slice sharpened a specific open boundary. Victor documents a `memory fail` admission condition around a two-part destructive-read / restore cycle, but the inspected patent text does not prove that an access already in flight is guaranteed to finish restoration after power-fail detection.

The Case 02 evidence index therefore made this the highest-value open question:

> find a production controller/service manual that says what happens to the memory cycle already underway when power-fail detection occurs.

The September 1973 DEC PDP-8/E maintenance manual supplies exactly such a named implementation witness.

---

## Source identity and custody

### H/P — DEC production maintenance manual

The source is Digital Equipment Corporation's:

- *PDP-8/E, PDP-8/F & PDP-8/M Maintenance Manual, Volume 1: Processor*;
- order number **DEC-8E-HMM1A-D-D**;
- 7th Printing (Rev.), **September 1973**;
- Copyright 1971, 1972, 1973, Digital Equipment Corporation.

The manual is catalogued by MANX with the same DEC part number and September-1973 date, and public archival copies are mirrored by Bitsavers and PDP-8 preservation sites.

Relevant locations in the manual are:

- §3.22–3.23, Memory System general / functional description;
- the memory-cycle timing discussion around Figures 3-31 and 3-32;
- §3.26.4, **Power Fail Circuitry**;
- §3.27.2–3.27.3, READ / WRITE operation;
- §3.27.10–3.27.11, Memory Register and inhibit/write path.

Public custody / access points:

- MANX catalogue entry: <https://manx-docs.org/details.php/1%2C4017>
- Bitsavers archival PDF: <https://bitsavers.org/pdf/dec/pdp8/pdp8e/DEC-8E-HMM1A-D-D_PDP-8e_Maintenance_Manual_Volume_1_Processor_Sep73.pdf>
- searchable mirror used for text-location checking: <https://device.report/m/f543be6c683c3e08d16eca14f854b69311c27dc3ca837af500c7ec6e85aed20a>

### Source-use boundary

This is a service/maintenance manual for a named production family and therefore stronger for implemented circuit behavior than a generic textbook statement.

It still does **not** by itself prove:

- every PDP-8 memory option used identical power-fail circuitry;
- every fielded machine met timing margins after component aging;
- every possible brownout waveform was tolerated;
- ferrite remanence itself was the only possible failure mechanism;
- or that DEC originated the general idea of draining a current memory cycle before power removal.

The claim below is limited to the documented PDP-8/E-family memory implementation described in this manual.

---

## Historical / implementation record

### H/P — one core-memory cycle has a read half and a write half

The manual describes the standard PDP-8/E memory as a coincident-current magnetic read/write core memory with nominal cycle times of **1.2 µs and 1.4 µs**.

Its functional description separates the cycle into two portions:

```text
READ portion
    ↓
selected cores are driven and sensed
    ↓
Sense Amplifier output is strobed into the Memory Register
    ↓
WRITE portion
    ↓
Memory Register or processor data drives the inhibit/write path
    ↓
content is written back into core
```

The timing description states that `WRITE` and `INHIBIT` are generated only during the write half of the memory cycle. Section 3.27 further explains that the Memory Register retains sensed information and can feed the inhibit path for redeposit into core.

For an ordinary read/regenerate path, the logical value can therefore become available in the electronic Memory Register before the core write/redeposit portion has completed.

That makes a power failure during the cycle a real retention-boundary question rather than an abstract analogy.

### H/P — POWER OK loss stops the timing chain, but the manual explicitly says the memory cycle completes

Section 3.26.4 is unusually direct.

The memory power-fail circuit responds to `POWER OK`. When the supply detects voltage dropping too low, `POWER OK` is removed and the timing chain is shut off. The same paragraph explicitly says that this action nevertheless **ensures that the memory cycle is completed**.

This is the key result for the open Case 02 debt.

The documented control relation is not simply:

```text
power becomes unsafe
    -> stop timing
```

It is:

```text
power becomes unsafe
    ↓
POWER OK removed
    ↓
normal timing admission/progression is stopped
    +
current memory cycle is allowed to reach closure
```

The source therefore distinguishes stopping future progression from truncating the already-admitted core-memory operation.

### H/P — X/Y current is intentionally delayed long enough to complete WRITE

The next sentence makes the physical support mechanism clearer.

The manual says the memory power-fail circuitry turns off the X- and Y-current source **after a delay sufficient to complete the WRITE operation**.

That gives the case an implementation-level closure relation:

```text
power-fail detection
    != immediate removal of core drive current

power-fail detection
    -> delayed X/Y current-source shutdown
    -> enough documented interval for WRITE completion
```

This is stronger evidence than a bare `memory fail` or `power fail` signal because the manual places the delay relative to the core-memory write phase itself.

### H/P — the circuit is deliberately asymmetric across power transitions

DEC characterizes the memory power-fail circuit as a **fast-on / slow-off** switch:

- when power is initially good, the current source is activated immediately;
- when power becomes bad, current-source removal is delayed to finish the write operation.

This is a retention-specific power-boundary policy.

The asymmetry exists because the two transition directions carry different obligations:

```text
power becoming valid:
    admit memory drive promptly

power becoming invalid:
    preserve enough drive interval to close already-started memory work
```

### H/P — read-result capture and magnetic closure are separate state locations

Sections 3.27.2 and 3.27.10 describe the sensed value being held in Sense / Memory Register flip-flops and then used during the write portion for redeposit.

Thus, in the named PDP-8/E implementation:

```text
core state
    ↓ destructive read / sense
Sense / Memory Register state
    ↓ write / inhibit path
core state re-established
```

The temporary electronic state is part of the access-time preservation mechanism even though the long-lived quiescent payload is magnetic.

---

## Engineering reconstruction

Everything in this section is project terminology, not DEC's historical vocabulary unless explicitly marked.

### E — this is a drain-before-withdraw pattern

The documented circuit can be reconstructed as a bounded two-stage shutdown policy:

```text
1. withdraw admission / timing for further work
2. retain the physical capability needed to close the operation already in flight
```

For Case 02, the retained capability is not a modern transaction log or capacitor-backed cache. It is continued availability of the core X/Y drive path long enough to finish the memory write phase.

A concise relation is:

```text
stop new work
    !=
remove completion capability immediately
```

### E — closure evidence is phase-specific

The valuable feature of the DEC source is that the manual names the phase whose completion matters: `WRITE`.

That lets the repository improve the older generic relation:

```text
power-fail signal asserted
    !=
restore complete
```

into a named-implementation relation:

```text
PDP-8/E POWER OK removed
    ↓
normal timing chain is stopped
    ↓
X/Y current source remains available for a documented delay
    ↓
WRITE portion completes
    ↓
current memory cycle reaches its intended closure boundary
```

This is not a universal core-memory theorem. It is the documented PDP-8/E policy.

### E — quiescent nonvolatility and in-flight power-loss safety are independent design obligations

Ferrite remanence explains why an already-established core state can survive without continuous holding power.

It does not explain why a bit that has just been destructively sensed survives a power collapse **during** the read/restore trajectory.

The DEC controller supplies a separate answer for that transition:

```text
quiescent retention
    = magnetic remanence relation

in-flight transition closure
    = controller timing + retained current-source availability
```

The same memory can rely on both mechanisms at different phases.

### E — transient electronic state can be constitutive without being the retained payload

The Memory Register / Sense flip-flop state is temporary. It is not the long-term embodiment of the user's stored word.

Yet during destructive read it becomes necessary for reconstructing the magnetic state.

Therefore:

```text
short-lived reconstruction state
    !=
long-lived payload state

but

short-lived reconstruction state
    can be constitutive of successful retention across an access
```

This distinction is useful later in DRAM, mapped storage, journal replay, and distributed repair, while the physical mechanisms remain different.

---

## What this closes — and what it does not

### Closed at named-implementation level

The previous highest-priority Case 02 debt asked whether a production/service manual could explicitly establish current-cycle behavior after power-fail detection.

For the PDP-8/E family described by DEC in 1973, the answer is now directly grounded:

```text
current memory cycle already underway
    -> completed

power-fail detection
    -> does not immediately remove X/Y current

X/Y current removal
    -> delayed sufficiently to complete WRITE
```

This is materially stronger than the Victor patent boundary, where command suppression is documented but current-cycle completion was not established from the inspected text.

### Still open

The source does not, in the passages inspected for this slice, provide all of the following quantitative details:

- the exact voltage level corresponding to the memory-side `POWER OK` transition;
- the analog decay curve of the core-current supply after that point;
- a numeric value for the slow-off delay in §3.26.4;
- worst-case aged-component margin between fail detection and completion;
- an explicit external signal meaning `restore durably complete`;
- controlled fault injection at every nanosecond of the read/write cycle;
- behavior under oscillatory brownout where `POWER OK` repeatedly crosses threshold.

So the bounded conclusion is **documented design intent and implementation behavior**, not a universal measured power-cut survival distribution.

---

## Cross-case comparison

### Case 02 Victor 1974–1975

Victor provides:

```text
two-part destructive read / restore cycle
+
power-fail admission gating
```

but did not close the current-cycle timing question in the inspected patent.

DEC PDP-8/E provides the missing stronger witness:

```text
power-fail response
+
explicit current-cycle completion
+
delayed removal of X/Y drive until WRITE completion
```

This is a comparison of documented control relations, not a claim of lineage between Victor and DEC.

### Case 86 PDP-8 power-fail save / restart

Case 86 concerns a larger state transfer:

```text
CPU / execution state
    -> emergency save into core
    -> power loss
    -> restart / software reconstruction
```

This Case 02 slice is lower-level:

```text
one core-memory access already in flight
    -> write/restore closure before drive removal
```

Therefore:

```text
memory-cycle closure
    !=
whole-machine emergency-save completion
```

The two may coexist in one machine family without being the same retention obligation.

### Case 03 DRAM

DRAM offers only a functional analogy:

```text
sense can create a restore obligation
```

PDP-8/E core uses magnetic remanence plus a destructive-read / rewrite cycle; DRAM uses volatile charge storage and periodic refresh. No direct technical genealogy is claimed here.

---

## Functional analogy boundary

At an abstract level, the PDP-8/E circuit resembles later systems that stop admitting new work while allowing already-admitted work to drain to a safe boundary.

Useful functional analogy:

```text
failure detected
    -> admission changes
    -> completion resources remain temporarily available
    -> in-flight operation reaches closure
    -> resource withdrawal follows
```

Do **not** translate this into claims that DEC implemented:

- transactional commit;
- write-ahead logging;
- persistence domains;
- storage barriers;
- crash consistency in the modern filesystem sense;
- or a direct ancestor of later drain protocols.

The relation is analogous; the historical mechanism is specific.

---

## Philosophical interpretation ceiling

This source supports a bounded project-level observation:

> technical continuity may require a system to preserve not only a state, but also enough **completion capability** to finish reconstructing that state when a boundary event occurs mid-operation.

That interpretation is downstream of the engineering evidence.

It is not a claim that DEC engineers formulated a general philosophy of persistence, identity, or memory.

---

## Explicit non-claims

This record does **not** claim that:

1. all magnetic-core computers completed the current cycle on power failure;
2. every PDP-8 memory option used the identical circuit;
3. the slow-off delay is numerically quantified by the cited paragraph;
4. the delay guarantees success under every brownout waveform;
5. a completed write proves every magnetic core met nominal margin;
6. the CPU's full architectural state survives merely because the memory cycle completes;
7. peripheral state survives;
8. `POWER OK` is equivalent to a modern persistence-domain acknowledgement;
9. DEC invented the general drain-before-power-removal idea;
10. the Victor controller behaved identically;
11. the PDP-8/E mechanism is genealogically linked to modern storage flush/barrier protocols;
12. a manual statement substitutes for phase-by-phase destructive power-cut experiments.

---

## Evidence impact

This slice closes the highest-value open **qualitative** Case 02 question: a named production/service manual explicitly documents what happens to a memory cycle already in flight at power-fail detection.

The Case 02 comparison can now distinguish two historical witnesses:

```text
Victor 1974–1975:
    power-fail admission gate documented
    current-cycle restore closure not established from inspected text

DEC PDP-8/E 1973:
    POWER OK failure documented
    current memory cycle explicitly completed
    X/Y current source shutoff delayed until WRITE can complete
```

Case 02 should remain `grounded`; this is a significant boundary closure, but not a reason by itself to promote maturity.

The next highest-value work is narrower and more empirical:

- phase-specific power-failure tests around read/sense/write timing;
- exact threshold / slow-off timing or schematic component values;
- a second named controller using a different strategy;
- and measured failure behavior when the documented margin is intentionally violated.
