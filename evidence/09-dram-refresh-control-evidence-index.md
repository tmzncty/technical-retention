# Case 09 evidence index — DRAM refresh-control partitions and qualification

Canonical case: [`../cases/09-dram-cbr-refresh-address-internalization.md`](../cases/09-dram-cbr-refresh-address-internalization.md)

Current maturity: **`grounded`**.

This index is the focused navigation surface for Case 09. It does not replace `CASE_INDEX.md`, and it does not promote the case. Its purpose is to keep the already-grounded refresh-control evidence from being repeatedly rediscovered while making the remaining seams explicit.

The case asks a narrower question than a general history of DRAM:

> **When dynamic payload requires periodic reconstruction, where do refresh cadence, row enumeration, deadline evidence, initialization, access arbitration, and operational qualification live, and how do their retention horizons differ?**

Historical record, engineering reconstruction, functional analogy, and philosophical interpretation remain separate below.

---

## Evidence chains

### 1. Canonical TI CBR grounding

[`09-ti-cbr-refresh-address-grounding.md`](09-ti-cbr-refresh-address-grounding.md)

Role:

- grounds the central CAS-before-RAS comparison;
- separates externally supplied row addresses from an on-chip refresh-address counter;
- establishes that moving row enumeration on-chip does not by itself remove the external refresh-cadence obligation;
- keeps ordinary DRAM retention deadlines distinct from refresh-address authority.

Use this packet before reopening the basic question `what does CBR internalize?`.

### 2. Refresh-counter initialization and testability

[`09-dram-refresh-counter-initialization-test-deepening.md`](09-dram-refresh-counter-initialization-test-deepening.md)

Role:

- TI patent evidence for a disclosed refresh-counter embodiment with a power-on-zero phase;
- Motorola product evidence for a named CBR refresh-counter test;
- separates refresh cadence from row-coverage correctness;
- separates bounded maintenance-path test success from indefinite future maintenance correctness;
- establishes that maintenance-control state can have a persistence horizon different from the logical payload relation it supports.

Do **not** generalize TI's disclosed power-on-zero circuit into a universal normal-mode counter-start rule for all DRAMs.

### 3. 1973–1982 public prior-art control partitions

[`09-1973-1982-early-self-refresh-control-partitions-prior-art-deepening.md`](09-1973-1982-early-self-refresh-control-partitions-prior-art-deepening.md)

Role:

- corrects any overly linear story in which refresh automation simply moved from board to chip in one step;
- distinguishes memory-system self-initiating refresh, row-age/deadline-driven schemes, external cadence + internal enumeration, and internally timed refresh;
- keeps public-patent prior art distinct from product deployment, invention priority, and direct influence genealogy.

### 4. GTE 1971–1973 system-boundary witness

[`09-gte-1971-1973-self-initiating-refresh-system-boundary-deepening.md`](09-gte-1971-1973-self-initiating-refresh-system-boundary-deepening.md)

Role:

- directly inspects GTE's self-initiating refresh system around commercial Intel 1103 DRAMs;
- places the free-running clock, pulse generation, row counter, address gating, and memory-busy relation at the memory-system boundary;
- blocks the shortcut `automatic relative to CPU == self-refresh circuitry inside the DRAM package`.

### 5. 1103 product refresh contract

[`09-1972-1975-1103-refresh-product-contract-deepening.md`](09-1972-1975-1103-refresh-product-contract-deepening.md)

Role:

- grounds the commercial 1103-family coverage/deadline contract in period product documentation;
- separates `how many rows must be restored by when` from one particular scheduler/counter implementation;
- shows that related device variants can keep the same coverage geometry while changing the allowed refresh interval.

### 6. Early autonomous-self-refresh publication evidence

[`09-1981-1983-autonomous-self-refresh-prior-art-deepening.md`](09-1981-1983-autonomous-self-refresh-prior-art-deepening.md)

Role:

- preserves contemporary publication evidence for internal timer / arbiter / refresh-counter architectures;
- complements rather than replaces the earlier public-patent floor;
- keeps scholarly publication chronology distinct from first invention, shipment, or direct implementation lineage.

### 7. Micron 1999 AUTO REFRESH vs SELF REFRESH

[`09-micron-1999-sdram-auto-vs-self-refresh-deepening.md`](09-micron-1999-sdram-auto-vs-self-refresh-deepening.md)

Role:

- supplies a later same-product interface contrast;
- separates externally repeated AUTO REFRESH commands from SELF REFRESH mode in which recurring refresh clocking moves inside the SDRAM after mode entry;
- makes clear that `mode entry authority` and `recurring cadence authority` are separate control functions.

This is a functional successor comparison, not a genealogy from the earlier asynchronous DRAM sources.

### 8. Hyundai 1992 powered-clockless bias and reinitialization

[`09-hyundai-1992-powered-clockless-bias-reinitialization-deepening.md`](09-hyundai-1992-powered-clockless-bias-reinitialization-deepening.md)

Role:

- grounds a named commercial DRAM requirement for eight initialization cycles after power-up;
- more importantly, grounds the same initialization requirement after an extended period of **bias without clocks greater than the refresh interval**;
- separates power continuity from maintenance continuity and operational qualification;
- keeps eight initialization cycles distinct from the documented 512-cycle full refresh coverage requirement;
- refuses to infer a hidden normal-mode counter reset value that the product sheet does not expose.

This closes the seam `continued power == continued refresh-control qualification?` for one bounded 1992 product. The answer, at the published interface-contract level, is **no**.

### 9. Mosel Vitelic 1997 cross-vendor powered-clockless witness

[`09-mosel-1997-powered-clockless-reinitialization-cross-vendor-deepening.md`](09-mosel-1997-powered-clockless-reinitialization-cross-vendor-deepening.md)

Role:

- independently corroborates the Hyundai powered-clockless rule in a different manufacturer's product documentation;
- grounds Mosel Vitelic V53C16129H Rev. 1.2 (July 1997), with a 512-cycle / 8 ms refresh contract and an internal nine-bit CBR row counter;
- grounds a 200 µs power-on pause plus eight RAS-bearing initialization cycles;
- grounds renewed eight-cycle initialization after **extended periods of bias without clocks greater than the Refresh Interval**;
- upgrades the pattern from one named product witness to a bounded **cross-vendor product-contract pattern**;
- explicitly refuses to infer a shared standard, copied wording, identical silicon cause, universal asynchronous-DRAM behavior, or a known counter reset value.

This closes the previous highest-value debt `find a second vendor witness` at a bounded level. It leaves genealogy and hidden-state cause open.

---

## Unified technical chain

The evidence now supports the following project-level decomposition:

```text
physical charge leakage
    -> finite refresh deadline
    -> coverage requirement
    -> cadence authority
    -> refresh trigger / mode control
    -> row-enumeration authority
    -> access-vs-refresh arbitration
    -> sense / restoration
    -> initialization / operational qualification
```

Different historical systems place these functions at different boundaries:

```text
external controller / memory system
        |
        +-- cadence
        +-- row counter
        +-- gating / arbitration

DRAM package
        |
        +-- row counter only
        +-- counter + timer + arbitration
        +-- later self-refresh recurrence after mode entry
```

The Hyundai + Mosel pair adds another axis:

```text
VDD continuity
    != qualifying refresh activity continuity
    != immediate post-interruption qualification
```

For both named products, one continuously powered interval can contain a prolonged clockless segment after which initialization is required again.

This should not be collapsed into one generic property called `refresh state`.

---

## Historical vocabulary vs project vocabulary

### Historical/source vocabulary

Use source terms as written when making historical claims:

- `refresh`;
- `self-initiating refresh`;
- `self-refreshing memory`;
- `mandatory refresh` / `voluntary refresh`;
- `on-chip refresh`;
- `RAS-only refresh`;
- `CAS-before-RAS refresh`;
- `hidden refresh`;
- `refresh address`;
- `refresh counter`;
- `AUTO REFRESH`;
- `SELF REFRESH`;
- Hyundai and Mosel Vitelic's `initialization cycles` and `extended periods of bias without clocks`.

### Engineering reconstruction vocabulary

The following are repository analytical terms, not retroactive historical quotations:

- `cadence authority`;
- `row-enumeration authority`;
- `maintenance-control state`;
- `maintenance-qualified epoch`;
- `powered-bias requalification boundary`;
- `control-state qualification`;
- `coverage obligation`;
- `cross-vendor product-contract pattern`.

Use these only when the source-level facts have already been stated and bounded.

---

## Anti-collapse map

```text
power present
    != refresh work performed

refresh requests frequent enough
    != row coverage verified

row coverage mechanism correct
    != deadline necessarily met

internal row counter
    != autonomous refresh scheduler

automatic relative to CPU
    != chip-local self-refresh

same historical word "self refresh"
    != same implementation boundary

mode entry
    != recurring cadence authority

maintenance-control state
    != application history

maintenance-control persistence
    != payload persistence

8 initialization cycles
    != 512-row refresh coverage

powered continuously
    != continuously maintenance-qualified

two vendor product sheets with similar rule
    != universal DRAM behavior

near-identical wording
    != proven standard provenance or direct copying
```

This anti-collapse map is the preferred starting point for future Case 09 work.

---

## Cross-case comparison links

These are functional comparisons only unless a future source establishes genealogy.

### Case 03 — physical DRAM retention

Case 03 owns the lower-level physical premise: dynamic charge decays and therefore needs periodic reconstruction. Case 09 starts one layer higher and should not duplicate the physical-device history.

### Case 04 — Flash mapping / reuse admission

Case 04 separates erase completion, post-erase preparation, and reuse admission. The useful analogy is only:

```text
physical substrate condition
    != control-layer eligibility
```

### Case 10 — leakage-tracked self refresh

Case 10 concerns condition-derived / autonomous refresh timing. Case 09 concerns the broader historical distribution of cadence, enumeration, initialization, and arbitration authority.

### Case 38 — SSD PLI maintenance

Case 38 separates maintenance policy, execution, and readiness evidence. It is useful as a modern anti-collapse comparison, not as DRAM lineage.

### Case 83 — HDFS scanner cursor

Case 83 provides a very different persistence contract for maintenance traversal state across process/restart boundaries. The comparison helps show that `maintenance-control state` is not one universal checkpoint semantics.

### Case 101 — SCSI Background Medium Scan

Case 101 distinguishes power-epoch observability from maintenance progress. The Hyundai + Mosel pair complements it by showing that a single gross power interval can contain more than one maintenance-qualified regime.

---

## Prior-art and related-repository boundary

`tmzncty/computing-archaeology` has been searched for dedicated HY534256, V53C16129H, CBR-initialization, and `extended periods of bias without clocks` packets. No directly reusable packet was identified in the current passes.

Therefore this repository retains only the **retention-specific control boundaries** needed for Case 09. A broader history of asynchronous DRAM startup rules, repeated vendor wording, standards provenance, counter-test modes, or vendor families should be developed in `computing-archaeology` and linked back rather than duplicated here.

The existing repository-level link in [`../RELATED_REPOS.md`](../RELATED_REPOS.md) remains the correct boundary marker.

---

## Current status

**Case 09 remains `grounded`.**

This index does not change the maturity ledger in `CASE_INDEX.md`.

The evidence base now covers:

- early commercial refresh coverage/deadline contracts;
- system-level self-initiating refresh;
- public-patent variations in deadline/cadence/enumeration placement;
- on-chip CBR row enumeration;
- maintenance-counter initialization/testability;
- contemporary autonomous-self-refresh publications;
- later AUTO REFRESH vs SELF REFRESH interface partition;
- a named 1992 Hyundai powered-but-clockless reinitialization boundary;
- an independent 1997 Mosel Vitelic product witness publishing the same bounded operational relation.

The earlier question `is this only a Hyundai-specific published contract?` is now answered **no** for the public record inspected here.

What the evidence still does **not** contain is:

- a provenance chain explaining why the two vendors publish near-identical wording;
- a manufacturer explanation binding the renewed initialization requirement to one specific internal state;
- a real hardware trace tying the published rule to measured hidden-state and payload behavior.

---

## Highest-value remaining debt

1. **Genealogy / standard provenance.** Search earlier vendor handbooks, JEDEC material, application notes, or controller design guides for the source of the near-identical powered-clockless initialization wording. Put broad technical history in `tmzncty/computing-archaeology` and link back.
2. **Hidden-state binding.** Find a manufacturer source that explicitly identifies which internal state makes the reinitialization sequence necessary after prolonged clocklessness.
3. **Earlier independent witness.** Find a late-1980s/early-1990s non-Hyundai product sheet with the same rule if available; keep publication floor separate from invention priority.
4. **Hardware trace.** Hold VDD continuously, sweep clockless gaps across the refresh interval, then separately measure payload correctness, initialization behavior, and CBR counter-test progression.
5. **Counter initialization discipline.** Continue refusing to infer normal-mode counter values from diagnostic test-mode behavior unless a product source explicitly binds them.

A useful next experimental matrix remains:

```text
A: VDD removed and restored
B: VDD retained, normal refresh continues
C: VDD retained, clock gap < refresh interval
D: VDD retained, clock gap > refresh interval

observe independently:
    payload correctness
    normal-access admission / behavior
    initialization-cycle requirement
    counter-test progression
```

Until such a trace exists, the Hyundai and Mosel results remain strong **product-interface contracts**, not transistor-level explanations.