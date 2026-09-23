# Case 03 — DRAM Refresh Evidence Index

## Canonical case

[`cases/03-dram-refresh-as-scheduled-restoration.md`](../cases/03-dram-refresh-as-scheduled-restoration.md)

## Canonical maturity

**`grounded`**

This index is navigation and evidence-boundary bookkeeping. It does **not** promote Case 03 beyond the maturity recorded in [`CASE_INDEX.md`](../CASE_INDEX.md), and it does not replace the canonical case narrative.

The current evidence set establishes several distinct retention layers that should not be collapsed into one generic word such as `refresh`:

```text
payload charge / logical bit
    != sense / restore machinery
    != refresh-deadline / cadence state
    != refresh-coverage / next-row state
    != refresh/access arbitration state
    != preservation-mode handoff state
    != controller configuration
    != reconstruction clue / resume state
```

A useful current summary is:

```text
physical state may decay
    ↓
maintenance is required
    ↓
maintenance-control state may live outside or inside the DRAM
    ↓
that control state can itself fail or move
    ↓
retention can continue across loss of one controller state
        if preservation authority is safely handed to another regime
```

---

# Evidence chain

## 1. 1967–1982 — Physical mechanism and commercial grounding

**Record:** [`03-dram-1967-1982-grounding.md`](03-dram-1967-1982-grounding.md)

### What it establishes

- Robert Dennard's 1967-filed / 1968-issued patent explicitly distinguishes time-driven regeneration caused by charge leakage from access-driven restoration caused by destructive read in the one-transistor / one-capacitor embodiment.
- Dynamic retention does not logically require destructive read: both the patent's alternative cells and later commercial DRAM documentation provide nondestructive-read examples that still require periodic refresh.
- AMD commercial documentation grounds one-transistor / capacitor storage, leakage-driven refresh, row-level maintenance, and shared sense / restore infrastructure in named products.

### Bounded relation

```text
access-triggered restore
    !=
time-triggered regeneration
```

and:

```text
logical bit
    != exact analog cell voltage
    != shared restoration infrastructure
```

### Evidence role

This is the physical / mechanism foundation of Case 03. Later controller slices should not be used to substitute for it.

---

## 2. 1975–1983 — Dedicated refresh controller and control-state failure

**Record:** [`03-intel-1975-1983-refresh-control-failure-boundary-deepening.md`](03-intel-1975-1983-refresh-control-failure-boundary-deepening.md)

### What it establishes

- Intel documented a separate `8222 — DYNAMIC MEMORY REFRESH CONTROLLER` by 1975.
- The later 8202A documentation exposes timer, refresh-address counter, synchronization, and arbitration as separate maintenance-control state.
- Intel explicitly warns that TEST-mode interference can clear / disrupt the refresh counter and may result in data loss.
- The same material also documents a `Refresh Lock-Out` failure mode in which excessive / badly coupled refresh requests can damage useful-service liveness.

### Bounded relation

```text
payload presently readable
    !=
maintenance-control state correct
    !=
future refresh deadlines guaranteed
```

and:

```text
refresh work occurring
    !=
maintenance policy correct
    !=
useful service live
```

### Evidence role

This is the strongest early Case 03 witness that the state required to retain data can become wrong before the payload itself visibly disappears.

---

## 3. 1982–1984 — Hidden refresh and explicit external timing / coverage state

**Record:** [`03-intel-1982-1984-hidden-refresh-controller-state-deepening.md`](03-intel-1982-1984-hidden-refresh-controller-state-deepening.md)

### What it establishes

- Intel 2164A `Hidden Refresh` can preserve output availability while refresh is still row-addressed and externally coordinated.
- Intel 8203 documentation exposes a refresh timer, refresh counter, address multiplexer, and access / refresh arbitration.
- `Hidden` therefore describes an interface / scheduling property, not disappearance of maintenance-control state.

### Bounded relation

```text
hidden refresh
    !=
autonomous refresh
```

and:

```text
payload state
    != refresh deadline / phase state
    != refresh coverage position
    != arbitration state
```

### Evidence role

This is the clean controller decomposition used by later cross-case work.

---

## 4. 1984–1988 — On-chip CBR coverage state versus autonomous cadence

**Record:** [`03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md`](03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md)

### What it establishes

- TI production documentation for CAS-before-RAS refresh moves refresh-address generation / coverage state on-chip.
- NEC patent evidence separately adds a timer-backed self-refresh path.
- Therefore internalizing the next-row / coverage counter does not by itself internalize refresh cadence or make the device self-refreshing.

### Bounded relation

```text
on-chip refresh-address state
    !=
on-chip refresh-cadence generation
```

### Evidence role

This prevents a common category error: the physical location of maintenance-control state does not determine how much refresh authority has moved with it.

---

## 5. 1998–1999 — SA-1100 sleep self-refresh / controller-state handoff

**Record:** [`03-intel-sa1100-1998-1999-sleep-self-refresh-control-state-handoff-deepening.md`](03-intel-sa1100-1998-1999-sleep-self-refresh-control-state-handoff-deepening.md)

### What it establishes

Intel's StrongARM SA-1100 documentation provides a later named-system power-transition witness in which:

1. ordinary operation uses controller-timed CBR refresh;
2. sleep entry finishes an admitted memory operation;
3. the controller places DRAM into self-refresh before its ordinary state is reset / powered down;
4. a smaller power-management / interface-hold relation keeps RAS / CAS in the self-refresh condition;
5. Intel explicitly says DRAM contents are preserved during sleep while the DRAM control registers lose power;
6. after wake, software reconfigures those control registers while DRAM is still held in self-refresh;
7. only after valid controller configuration exists is the hold released and ordinary access resumed.

The same manual distinguishes software reset, sleep reset, and hardware reset with different DRAM-related consequences.

### Bounded relation

```text
payload retention continuity
    !=
controller-state continuity
```

and:

```text
safe preservation-mode handoff
    + retained hold relation
    + reconstructable controller configuration
    -> payload can remain continuous across ordinary controller loss
```

### Evidence role

This is not a claim that the SA-1100 invented suspend-to-RAM or self-refresh. It is a named-system witness that **maintenance authority itself can be handed off across a power-state transition**, allowing controller reconstruction to occur while the payload remains under a different preservation regime.

---

# Cross-layer comparison

| Question | Evidence chain | Bounded answer |
| --- | --- | --- |
| Why is refresh required at all? | 1967–1982 grounding | charge leakage makes periodic regeneration necessary |
| Is destructive read what makes memory dynamic? | 1967–1982 grounding | no; nondestructive-read dynamic memories still require refresh |
| Can retention-control state exist separately from payload? | 1975–1984 Intel controller records | yes; timer, counter, arbitration, and request state are explicit |
| Can control-state failure precede payload loss? | 1975–1983 failure deepening | yes; disrupted refresh sequencing can create later data-loss risk |
| Does hidden refresh imply autonomous refresh? | 1982–1984 deepening | no |
| Does an on-chip row counter imply on-chip cadence authority? | 1984–1988 CBR deepening | no |
| Can payload survive while ordinary controller configuration is intentionally lost? | 1998–1999 SA-1100 deepening | yes, in the documented sleep/self-refresh handoff |
| Is one generic `reset-survival` flag adequate? | 1998–1999 SA-1100 deepening | no; software, sleep, and hardware reset have different state consequences |

---

# Current state model

Case 03 now supports the following layered model without claiming that every historical DRAM implementation has every layer in the same place:

```text
retained payload
    ↓
cell / row sense-and-restore mechanism
    ↓
refresh coverage relation
    ↓
refresh cadence / deadline relation
    ↓
refresh admission / arbitration relation
    ↓
mode / authority handoff relation
    ↓
controller configuration needed for ordinary service
    ↓
small resume / reconstruction clues where a system chooses to retain them
```

The important separations are:

```text
state being retained
    !=
state required to retain it
```

```text
location of maintenance-control state
    !=
scope of maintenance authority
```

```text
controller-state survival
    !=
payload survival
```

```text
controller reconstruction
    !=
payload reconstruction
```

```text
maintenance handoff
    !=
full execution-state continuation
```

---

# Historical record versus reconstruction

## Historical record

The evidence files record manufacturer / patent claims in period vocabulary: regeneration, dynamic memory, refresh timer / counter, hidden refresh, CAS-before-RAS refresh, self-refresh, sleep reset, DRAM control hold, and controller reconfiguration.

## Engineering reconstruction

Case 03 uses those records to separate payload state, restoration machinery, deadline state, coverage state, arbitration state, handoff state, and reconstructable controller configuration.

## Functional analogy

Links to magnetic-core restart, Mobile-DRAM self-refresh authority, later storage checkpointing, or typed reset persistence are analogies only unless a separate genealogy record establishes historical descent or influence.

## Philosophical interpretation

The repository may interpret these cases as showing that continuity can depend on scheduled maintenance, authority transfer, or reconstruction of supporting state. Historical actors are not credited with that philosophical vocabulary unless a source actually uses it.

---

# Explicit anti-collapse rules

Do not shorten the evidence into any of the following unsupported equations:

```text
dynamic memory = destructive read
```

```text
hidden refresh = self refresh
```

```text
on-chip refresh counter = autonomous refresh
```

```text
DRAM payload retained = refresh controller retained
```

```text
controller reset = immediate payload loss
```

```text
controller reconfiguration = data reconstruction
```

```text
sleep reset = software reset = hardware reset
```

Each of these erases a distinction directly supported by the current evidence set.

---

# Related repositories

Current searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated `SA-1100` / `StrongARM` treatment to reuse for the new power-transition slice.

Broader work that should stay primarily in `computing-archaeology` includes:

- the general history of DRAM generations and controllers;
- StrongARM platform genealogy;
- suspend-to-RAM history;
- processor and memory power-domain design;
- Mobile-SDRAM / LPDDR standardization;
- manufacturer competition and product chronology.

Case 03 should continue to take only the bounded evidence needed to test retention relations.

---

# Remaining high-value debt

The evidence set is already sufficient for `grounded`; remaining work is narrower and should be selected only when it closes a specific relation.

1. **SA-1100 named DRAM pairing:** identify a period board / design with a documented DRAM part and compare its exact self-refresh contract against the controller sequence.
2. **SA-1100 fault-window evidence:** board- or silicon-level tests around sleep entry / wake release would move the new handoff claim from contractual ordering toward implementation validation.
3. **Alternate-master refresh handoff:** the SA-1100 manual separately assigns DRAM-integrity responsibility to an alternate bus master while SA-1100 is unable to refresh; this is a distinct authority-transfer slice and should not be silently merged into sleep self-refresh.
4. **Earlier / cross-vendor power-state handoff witnesses:** useful only if they materially change the relation or establish genealogy.
5. **Physical retention distributions:** temperature / leakage / weak-row distributions belong in a separate empirical slice, not in controller-state navigation.
6. **Broader semiconductor / low-power history:** keep in `computing-archaeology` rather than expanding Case 03 indefinitely.

---

# Status decision

**No maturity change.**

Case 03 remains **`grounded`**. The SA-1100 evidence deepens a power-transition / authority-handoff boundary and adds a useful named-system reset matrix, but it does not by itself justify promotion to a stronger repository-wide maturity category.