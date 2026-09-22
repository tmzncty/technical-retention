# Case 135 evidence index — e.MMC time-triggered maintenance and Micron Self Refresh

## Case

Canonical case:

[`../cases/135-micron-emmc-self-refresh-time-trigger-maintenance.md`](../cases/135-micron-emmc-self-refresh-time-trigger-maintenance.md)

Current local case status: **`grounded`**.

This index organizes the evidence around one question:

> How does a managed nonvolatile device use host-supplied time, maintenance scheduling, internal eligibility, selective renewal, and retained telemetry to preserve payload across long service intervals?

The evidence must keep standard e.MMC control surfaces separate from Micron's vendor-specific Self Refresh implementation.

## Evidence chains

### 1. Product grounding — Micron/Armadillo Self Refresh

[`135-micron-emmc-2021-2023-self-refresh-grounding.md`](135-micron-emmc-2021-2023-self-refresh-grounding.md)

Role:

- named product/integration witness;
- automatic eMMC `data retention` / `self refresh` path;
- host `SET_TIME (CMD49)` participation;
- elapsed-time eligibility;
- bus-idle gating;
- ECC-threshold-conditioned block selection;
- execution/progress/completion telemetry;
- reset and power-loss counters.

Boundary:

```text
Micron / Armadillo product behavior
    !=
generic behavior of every e.MMC device
```

### 2. Generic Background Operations maintenance opportunity

[`135-jedec-emmc51-bkops-maintenance-opportunity-deepening.md`](135-jedec-emmc51-bkops-maintenance-opportunity-deepening.md)

Role:

- separates standardized BKOPS from vendor Self Refresh;
- identifies maintenance opportunity, status, host enablement, start, and execution as different states;
- preserves the earlier e.MMC 4.41 lineage for generic Background Operations.

Boundary:

```text
BKOPS capability / status
    !=
Micron selective Self Refresh algorithm
```

### 3. Directly inspected e.MMC 5.0 time-maintenance semantics

[`135-jesd84-b50-2013-rtc-periodic-wakeup-time-maintenance-deepening.md`](135-jesd84-b50-2013-rtc-periodic-wakeup-time-maintenance-deepening.md)

Role:

- direct repository clause-level floor for `SET_TIME (CMD49)`;
- absolute vs relative time information;
- host updates after power-up / wake / periodically;
- `PERIODIC_WAKEUP[131]`;
- periodic maintenance wake-up sequence;
- at least one Background Operation completed before the relevant power-down sequence.

Boundary:

```text
2013 e.MMC 5.0 direct clause floor
    !=
feature-origin date
```

### 4. e.MMC 4.5 / 4.51 RTC prior-art chronology

[`135-emmc45-451-2011-2012-rtc-periodic-wakeup-prior-art-deepening.md`](135-emmc45-451-2011-2012-rtc-periodic-wakeup-prior-art-deepening.md)

Role:

- moves RTC-related reliability lineage back to **e.MMC 4.5 / June 2011**;
- uses JEDEC's later Annex C revision history to assign RTC to the 4.41 -> 4.5 transition;
- uses `mmc-utils` as implementation corroboration that `PERIODIC_WAKEUP[131]` is B45-generation;
- inserts e.MMC 4.51 / June 2012 as an explicit intermediate standards epoch;
- rejects the false inference that e.MMC 5.0 was the origin of the feature.

Boundary:

```text
feature present by e.MMC 4.5
    !=
every e.MMC 5.0 clause proven textually identical in 4.5
```

## Chronology

```text
e.MMC 4.41 / 2010
    generic Background Operations lineage
        ↓
e.MMC 4.5 / 15 Jun 2011
    RTC-related host/device reliability capability publicly documented
    later JEDEC history assigns RTC to 4.41 -> 4.5
    PERIODIC_WAKEUP[131] associated with B45 by mmc-utils
        ↓
e.MMC 4.51 / Jun 2012
    intervening revision / clarification epoch
        ↓
e.MMC 5.0 / Sep 2013
    direct clause-level repository floor for
    SET_TIME / RTC / PERIODIC_WAKEUP semantics
        ↓
e.MMC 5.1 / 2015
    later standards epoch / clarification context
        ↓
Armadillo-IoT G4 / Micron / 2021+
    named vendor product self-refresh path
```

The chronology is intentionally evidence-layered. Publication of a standard, implementation in silicon, product enablement, and customer deployment are not treated as one event.

## Technical decomposition

Case 135 should keep the following state and transition boundaries separate:

```text
user payload
    ↓ protected by
media / controller reliability mechanisms

host temporal source
    ↓
host-supplied absolute or relative time evidence
    ↓
device temporal relation
    ↓
time-based maintenance eligibility
    ↓
maintenance opportunity / wakeup
    ↓
policy authority and admission
    ↓
internal media observation / ECC evidence
    ↓
selective renewal queue
    ↓
maintenance execution
    ↓
completion
    ↓
retained progress / history / counters
```

None of the arrows should be collapsed into a single state named `refresh`.

## Evidence-layer boundaries

### Historical record

Direct or near-direct sources can establish:

- which standard revision names a feature;
- which command/register exists;
- which product manual describes a behavior;
- which vendor document names Self Refresh;
- which implementation source maps a field to a standards generation.

They do not automatically establish the physical NAND operation behind the interface.

### Engineering reconstruction

Project-level reconstruction can separate:

- temporal evidence from maintenance execution;
- wakeup opportunity from admission;
- admission from completion;
- standard revision from device implementation epoch;
- retained payload from second-order maintenance metadata.

These are analytical decompositions, not vendor terminology.

### Functional analogy

Useful controlled comparisons include:

- Case 111 power-up re-observation versus Case 135 time-state reconstitution;
- Case 43 policy metadata versus Case 135 temporal maintenance evidence;
- Case 03 cadence locus versus Case 135 wakeup/authority locus.

No shared implementation ancestry is implied by those comparisons.

### Philosophical interpretation

The case can support the bounded proposition that preservation may depend on retaining or reconstructing **enough state to make a future maintenance decision**, rather than preserving a complete history of every event.

That interpretation must remain downstream of the technical evidence.

## Current strongest claims

1. The bounded Micron/Armadillo integration exposes a vendor-specific selective self-refresh path with explicit timing and telemetry.
2. Standard e.MMC Background Operations and vendor Self Refresh are distinct mechanisms/control surfaces.
3. By e.MMC 5.0, directly inspected standard text exposes host-supplied time plus periodic wakeup/background-maintenance semantics.
4. e.MMC 5.0 is **not** the origin of RTC-related reliability support: e.MMC 4.5 publicly introduced the RTC capability in June 2011.
5. JEDEC's own later revision history assigns `real time clock` to the 4.41 -> 4.5 transition.
6. `mmc-utils` corroborates `PERIODIC_WAKEUP[131]` as B45-generation EXT_CSD state.
7. The exact B45/B451 clause-level identity with later B50 semantics remains open.

## Explicit non-collapse rules

```text
RTC support
    !=
Self Refresh

host time supplied
    !=
maintenance executed

PERIODIC_WAKEUP field exists
    !=
every device requires periodic wakeup

maintenance opportunity
    !=
maintenance completion

feature-introduction chronology
    !=
clause-level semantic identity

standard revision
    !=
device firmware revision

product manual behavior
    !=
generic e.MMC behavior

current payload is readable
    !=
future retention margin is sufficient
```

## Remaining debt

Priority order for another bounded pass:

1. **Direct JESD84-B45 clause inspection** — exact RTC, `SET_TIME`, and `PERIODIC_WAKEUP` text.
2. **Direct JESD84-B451 clause inspection** — exact delta against B45 and B50.
3. Determine whether `PERIODIC_WAKEUP` encoding, reset/default behavior, optionality, or completion language changed from 4.5 -> 4.51 -> 5.0.
4. Find a **named shipping e.MMC 4.5 component** whose datasheet explicitly exposes RTC / periodic-wakeup support, rather than relying only on version compliance.
5. Trace host-software adoption only if it helps explain the control boundary; do not turn this case into a generic Linux MMC history.
6. Obtain stronger Micron primary material if it becomes publicly inspectable, especially for the internal selective-refresh algorithm, while avoiding inference from generic JEDEC language.

## Status decision

**Remain `grounded`.**

The 2011–2012 chronology correction materially strengthens prior art and prevents a false e.MMC 5.0 origin claim. It does not yet close the exact B45/B451 normative delta or provide a named early shipping device implementation, so promotion would be premature.