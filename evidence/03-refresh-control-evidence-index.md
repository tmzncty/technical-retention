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

Mostek MK4164 documentation moves the public-product-documentation floor for an on-chip refresh counter earlier than the later public TI/NEC witnesses. The 1980 data-book text additionally says the internal refresh counter is itself dynamic and requires refreshing; the same RFSH recurrence that services the memory array is adequate to maintain the counter.

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

This is a product-documentation/prior-art floor, not a first-invention or first-shipment claim.

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

The MK4164 deepening changes the public-product-documentation floor for **on-chip refresh counting**; it does not replace this later evidence about CAS-before-RAS and timer-backed self-refresh semantics.

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

### 8. 1978-filed TI on-chip refresh counter and traversal-order prior art

[`03-ti-1978-onchip-refresh-counter-prior-art-topology-deepening.md`](03-ti-1978-onchip-refresh-counter-prior-art-topology-deepening.md)

White/Rao `US4207618A`, assigned to Texas Instruments, adds an earlier **filing / priority** boundary plus a concrete claimed counter embodiment. The US application was filed on 26-Jun-1978; the checked family first becomes publicly visible here through `GB2024474A` on 9-Jan-1980, followed by the US publication/grant on 10-Jun-1980. Thus the filing chronology and the existing 1979 Mostek public product-document chronology must remain separate.

The TI architecture places refresh-address progression and address selection on the DRAM chip while retaining an externally supplied refresh command. Its preferred embodiment describes eight clocked D-type latches holding addresses generated by binary adder/counter stages. The patent also explicitly permits a nonnumerical sequence, including a pseudo-random shift-counter alternative, provided the required rows are all covered in time without address repetition in the relevant traversal.

The same slice uses Shuba / GTE `US3729722A` as an earlier system-level boundary: by 1971-filed / 1973-public evidence, a free-running clock, refresh pulse generator, external row-address counter, and gating could already create self-initiating system refresh for Intel 1103 memories. That earlier system-level autonomy is not the same claim as a same-die refresh counter.

Bounded results:

```text
system-level autonomous cadence
    !=
same-die coverage-state storage

on-chip refresh-address counter
    !=
on-chip refresh timer

coverage obligation
    !=
mandatory numerical traversal order

filing / priority date
    !=
public disclosure date
    !=
product-document date
    !=
shipping implementation
```

This slice does not establish invention priority, named TI product adoption, or a TI→Mostek circuit genealogy.

### 9. 1979-filed Mostek counter topology and hidden-state testability

[`03-mostek-1979-refresh-counter-topology-testability-deepening.md`](03-mostek-1979-refresh-counter-topology-testability-deepening.md)

Two Mostek-assigned 1979 patent families now narrow the previously broad MK4164 topology debt without pretending to identify the production mask set.

Proebsting's 15-May-1979-priority refresh-counter test filing treats an on-chip counter as hidden state whose output cannot simply be read directly. It explains why bounded payload survival is not enough to prove correct refresh coverage: cells may retain data far beyond the guaranteed minimum, masking a row skipped by a faulty counter. The proposed test instead makes the counter-selected row produce a controlled write side effect that can be checked through ordinary readback.

Eaton / Schroeder's 13-Aug-1979 filing gives a concrete Mostek counter embodiment. It reuses ordinary address-buffer circuitry, transfers buffer outputs into refresh-storage nodes, conditionally inverts selected bits at the end of a refresh cycle, and describes the refresh storage as a cross-coupled two-MOSFET flip-flop. The preferred embodiment is a binary up-counter, while the patent allows other counting arrangements.

Bounded results:

```text
payload survives a test interval
    !=
refresh coverage proven correct

hidden maintenance-control state
    -> may require a separate observability path

logical function separation
    !=
physical circuit separation

same-vendor contemporary patent topology
    !=
verified MK4164 production implementation
```

This is company-level circuit and testability evidence. No checked source names `MK4164` in either patent or links either patent number to the product, so the exact patent-to-product mapping remains open.

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
coverage traversal order
    !=
restore execution
    !=
access arbitration
    !=
useful-service visibility
    !=
maintenance-state observability / verification
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

The TI filing / GTE prior-art slice adds:

```text
coverage-state locus
    !=
cadence locus

complete row-set coverage before deadline
    !=
one required numerical row order

sufficient state to continue maintenance
    !=
complete history of maintenance events
```

The Mostek patent/testability slice adds:

```text
payload correctness observed now
    !=
maintenance coverage proven correct

state being retained
    !=
state coordinating retention
    !=
evidence that the coordination is correct

named-product behavior
    !=
company-level patent embodiment
    !=
verified product transistor topology
```

The existence of one recurrent RFSH stream servicing both the array and the counter does not collapse them into one retained object. Likewise, a family resemblance at the package or logical-capacity level does not establish one shared refresh-control topology. A patent filing, a public patent publication, a product-document witness, and a shipping implementation remain separate provenance claims even when they concern a similar function. Finally, successful payload readback can coexist for a time with a latent maintenance-control fault, so verification of the preserved object and verification of the preservation process are separate evidence layers.

---

## Status discipline

**Case 03 remains `grounded`.**

The cross-vendor 64K slice closed the previously listed interface-level refresh-organization comparison debt for the bounded Mostek / TI / Intel set. The TI / GTE prior-art slice partially closed and sharply narrowed the invention/priority debt by establishing a 26-Jun-1978 TI filing/priority floor for the currently inspected same-die refresh-counter sources, a 9-Jan-1980 British-family public-patent floor, and an earlier 1971-filed / 1973-public system-level autonomous-refresh counter boundary.

The new Mostek patent/testability slice **partially closes the exact-topology debt in a different direction**: a concrete Mostek company-level counter circuit is now directly documented, as is a contemporary Mostek technique for verifying hidden counter coverage. It does not justify a maturity promotion because the central unresolved question is now narrower rather than eliminated:

- pre-26-Jun-1978 same-die refresh-counter prior art / true invention-priority history remains open;
- named TI product adoption of the White/Rao architecture remains unproven;
- verified first-silicon and first-shipment chronology for MK4164 RFSH remains open;
- exact **MK4164** production counter topology remains unproven — a contemporary Mostek candidate circuit now exists, but no checked source maps `US4296480A` or the Proebsting test family to the named product;
- the relationship between the MK4164 manual's `dynamic` counter wording and Eaton / Schroeder's illustrated cross-coupled refresh-storage unit remains unresolved;
- transistor-level comparison of the named 64K DRAM refresh organizations remains open;
- production use of the Proebsting counter-test method remains unproven;
- controlled hardware observation of counter-phase loss or corruption remains open;
- board-level substitution / mixed-vendor compatibility evidence remains optional unless such a claim becomes necessary;
- broader semiconductor-memory genealogy should be routed to `tmzncty/computing-archaeology` rather than duplicated here.

---

## Related-repository routing

Earlier searches of `tmzncty/computing-archaeology` for `MK4164 RFSH refresh battery backup Mostek`, `Mostek DRAM refresh`, `MK4164`, `US4207618A`, and `on-chip refresh dynamic memory` returned no dedicated technical-history packet. During the present Mostek topology/testability deepening, fresh searches for `US4296480A` and `MK4164` likewise returned no dedicated packet to reuse.

If that repository later develops the 64K-DRAM product/genealogy story, Case 03 should link it and retain only the retention-specific distinctions above.