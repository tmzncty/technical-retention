# Case 03 — Refresh-Control Evidence Navigation

**Canonical case:** [`../cases/03-dram-refresh-as-scheduled-restoration.md`](../cases/03-dram-refresh-as-scheduled-restoration.md)

**Canonical maturity:** `grounded`

This index is a navigation aid for Case 03's growing refresh-control evidence. It does not replace the case, `ROADMAP.md`, or the repository's status conventions.

The files below answer different bounded questions. Chronological adjacency is not treated as genealogy.

---

## Evidence chain

### 1. Physical retention obligation and regeneration

[`03-dram-1967-1982-grounding.md`](03-dram-1967-1982-grounding.md)

Core Case 03 grounding: Dennard's charge-retention/regeneration relation, destructive-read restoration, commercial dynamic-memory refresh requirements, and the distinction between access-triggered restore and time-triggered regeneration.

### 2. Late-1970s row-coverage contract and RAS-only standby

[`03-mostek-1977-1979-ras-only-refresh-boundary-deepening.md`](03-mostek-1977-1979-ras-only-refresh-boundary-deepening.md)

Mostek MK4116 evidence separates:

```text
refresh-capable access
    !=
access-triggered retention regime

activity count
    !=
row-set coverage

RAS-only refresh
    !=
self-refresh

reduced-power standby
    !=
maintenance-free retention
```

### 3. 1979–1980 on-chip RFSH counter whose own state is dynamic

[`03-mostek-1979-1980-rfsh-dynamic-counter-deepening.md`](03-mostek-1979-1980-rfsh-dynamic-counter-deepening.md)

Mostek MK4164 documentation moves the public-documentation floor for an on-chip refresh counter earlier than the later TI/NEC witness. The 1980 data-book text additionally says the internal refresh counter is itself dynamic and requires refreshing; the same RFSH recurrence that services the memory array is adequate to maintain the counter.

Bounded result:

```text
payload state
    !=
maintenance-control state

maintenance-control state
    !=
maintenance-free state

on-chip coverage progression
    !=
autonomous cadence
```

This is a documentation/prior-art floor, not a first-invention or first-shipment claim.

### 4. Early-1980s hidden refresh and explicit external controller state

[`03-intel-1982-1984-hidden-refresh-controller-state-deepening.md`](03-intel-1982-1984-hidden-refresh-controller-state-deepening.md)

Intel 2164A / 8203 evidence separates output-visibility behavior from timer, next-row, and arbitration state and fixes:

```text
hidden refresh
    !=
autonomous refresh
```

### 5. 1975–1983 dedicated-controller genealogy and control-state failure

[`03-intel-1975-1983-refresh-control-failure-boundary-deepening.md`](03-intel-1975-1983-refresh-control-failure-boundary-deepening.md)

Intel 8222 / 8202A evidence moves the dedicated external-controller floor earlier and supplies concrete maintenance-control failure modes: TEST can disturb/reset coverage progression before payload loss is immediately visible, while refresh lock-out shows that excessive/badly coupled maintenance can destroy useful-service liveness.

### 6. 1984–1988 CAS-before-RAS internal coverage versus self-refresh cadence

[`03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md`](03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md)

TI/NEC/Samsung material remains the important later witness for a different boundary:

```text
internal refresh-address generation
    !=
internal refresh-cadence generation

CAS-before-RAS refresh
    !=
self-refresh
```

The MK4164 deepening changes the chronological prior-art floor for **on-chip refresh counting**; it does not replace this later evidence about CAS-before-RAS and timer-backed self-refresh semantics.

### 7. 1979–1984 cross-vendor 64K refresh organization

[`03-1979-1984-64k-dram-refresh-organization-cross-vendor-deepening.md`](03-1979-1984-64k-dram-refresh-organization-cross-vendor-deepening.md)

Mostek MK4164, TI TMS4164, and Intel 2164A manufacturer records now close the previously open bounded comparison at the interface-contract level. The devices share the broad 64K × 1 generation but do **not** expose one uniform maintenance contract:

```text
Mostek MK4164
    128 cycles / 2 ms
    pin 1 = RFSH
    on-chip next-refresh-row counter in RFSH mode

TI TMS4164
    256 rows / 4 ms
    pin 1 = NC
    externally presented refresh row in RAS-only mode

Intel 2164A
    128 cycles / 2 ms
    externally presented refresh row in bounded RAS-only / hidden mode
```

The comparison establishes:

```text
same logical capacity
    !=
same refresh-coverage cardinality
    !=
same refresh deadline
    !=
same coverage-state locus

package compatibility
    !=
maintenance-control compatibility
```

It is not an invention-priority, transistor-topology, or product-interchangeability claim.

---

## Current bounded decomposition

Across these records, Case 03 can now keep the following relations distinct:

```text
physical charge-retention obligation
    !=
maintenance deadline
    !=
refresh invocation / cadence
    !=
refresh-address / coverage cardinality
    !=
refresh-address / coverage state
    !=
restore execution
    !=
access arbitration
    !=
useful-service visibility
```

The Mostek MK4164 adds:

```text
state coordinating maintenance
    can itself be dynamic retained state
```

The cross-vendor 64K comparison adds:

```text
logical capacity
    !=
maintenance geometry

package/pin compatibility
    !=
maintenance-semantic identity
```

The existence of one recurrent RFSH stream servicing both the array and the counter does not collapse them into one retained object. Likewise, a family resemblance at the package or logical-capacity level does not establish one shared refresh-control topology.

---

## Status discipline

**Case 03 remains `grounded`.**

The cross-vendor 64K slice closes the previously listed interface-level refresh-organization comparison debt for the bounded Mostek / TI / Intel set. It does not justify a maturity promotion because important work remains outside the bounded evidence:

- invention / priority history for the earliest on-chip DRAM refresh counter;
- verified first-silicon and first-shipment chronology for MK4164 RFSH;
- exact internal counter circuit topology;
- transistor-level comparison of the named 64K DRAM refresh organizations;
- controlled hardware observation of counter-phase loss or corruption;
- board-level substitution / mixed-vendor compatibility evidence if such a claim is ever needed;
- broader semiconductor-memory genealogy, which should be routed to `tmzncty/computing-archaeology` rather than duplicated here.

---

## Related-repository routing

Earlier searches of `tmzncty/computing-archaeology` for `MK4164 RFSH refresh battery backup Mostek` and `Mostek DRAM refresh` returned no dedicated technical-history packet. A fresh search for `MK4164` during the cross-vendor deepening likewise returned no dedicated packet to reuse.

If that repository later develops the 64K-DRAM product/genealogy story, Case 03 should link it and retain only the retention-specific distinctions above.