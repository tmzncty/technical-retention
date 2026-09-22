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
- uses `mmc-utils` as implementation corroboration that `PERIODIC_WAKEUP[131]` is B45-generation EXT_CSD state;
- inserts e.MMC 4.51 / June 2012 as an explicit intermediate standards epoch;
- rejects the false inference that e.MMC 5.0 was the origin of the feature.

Boundary:

```text
feature present by e.MMC 4.5
    !=
every e.MMC 5.0 clause proven textually identical in 4.5
```

### 5. Named Micron e.MMC 4.51 RTC / `PERIODIC_WAKEUP` product witness

[`135-micron-2013-2014-emmc451-rtc-periodic-wakeup-product-deepening.md`](135-micron-2013-2014-emmc451-rtc-periodic-wakeup-product-deepening.md)

Role:

- inserts a named Micron component between standards-era prior art and the 2021+ Armadillo/Micron integration;
- identifies **MT29PZZZ4D4BKESK-18 W.94H** as a documented 4GB e.MMC + 4Gb LPDDR2 MCP;
- anchors the datasheet to **Rev. A 10/13** through inspected **Rev. D 05/14**;
- records product-level e.MMC 4.51 compliance and `Real-time clock` capability;
- directly exposes `PERIODIC_WAKEUP[131]` in the product EXT_CSD table;
- records the field's `R/W/E` persistence class across power cycle, `RST_n`, and `CMD0` reset;
- separates retained periodic-wakeup policy from BKOPS enable/start state;
- uses the same-package LPDDR2 `SELF REFRESH` section as an anti-collapse counterexample.

Boundary:

```text
named 4.51 product document
    !=
named 4.5 product document
    !=
shipment chronology
    !=
full SET_TIME/CMD49 clause reproduction
```

This closes the weaker product-adoption gap — RTC and `PERIODIC_WAKEUP` are no longer only standards-history abstractions before 2021 — while leaving the direct 4.5-device and B45/B451 normative-text debts open.

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
Micron MT29PZZZ4D4BKESK-18 W.94H / Rev. A Oct 2013
    named 4.51-generation product document
    RTC advertised
    PERIODIC_WAKEUP[131] exposed
    R/W/E persistence class documented
        ↓
Micron product datasheet Rev. D / May 2014
    inspected revision in this evidence slice
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

The chronology is intentionally evidence-layered. Publication of a standard, implementation in a named product document, shipment, product enablement, and customer deployment are not treated as one event. The 2013 Micron product-document witness and the September-2013 e.MMC 5.0 standards epoch overlap chronologically but answer different provenance questions.

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
retained periodic-wakeup policy configuration
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

The named Micron 4.51 datasheet further sharpens the policy-state horizon:

```text
PERIODIC_WAKEUP field implemented
    !=
field configured nonzero
    !=
wakeup event occurred
    !=
maintenance admitted
    !=
maintenance completed
```

and:

```text
reset-surviving policy configuration
    !=
restart-surviving maintenance progress
```

## Evidence-layer boundaries

### Historical record

Direct or near-direct sources can establish:

- which standard revision names a feature;
- which command/register exists;
- which named product exposes a field or capability;
- which reset/power transitions a vendor register table says preserve a configuration value;
- which product manual describes a behavior;
- which vendor document names Self Refresh;
- which implementation source maps a field to a standards generation.

They do not automatically establish the physical NAND operation behind the interface.

### Engineering reconstruction

Project-level reconstruction can separate:

- temporal evidence from maintenance execution;
- retained policy configuration from a wakeup event;
- wakeup opportunity from admission;
- admission from completion;
- standard revision from device implementation epoch;
- product-document availability from shipment/deployment;
- retained payload from second-order maintenance metadata.

These are analytical decompositions, not vendor terminology.

### Functional analogy

Useful controlled comparisons include:

- Case 111 power-up re-observation versus Case 135 time-state reconstitution;
- Case 43 policy metadata versus Case 135 temporal maintenance evidence;
- Case 03 cadence locus versus Case 135 wakeup/authority locus;
- the named Micron MCP's e.MMC `PERIODIC_WAKEUP` policy versus its separate LPDDR2 `SELF REFRESH` mechanism as a vocabulary-collision counterexample.

No shared implementation ancestry is implied by those comparisons.

### Philosophical interpretation

The case can support the bounded proposition that preservation may depend on retaining or reconstructing **enough state to make a future maintenance decision**, rather than preserving a complete history of every event.

The named Micron product adds a particularly concrete version: a future-preservation rule can itself have a persistence horizon across resets and power cycles without thereby becoming completed preservation work.

That interpretation must remain downstream of the technical evidence.

## Current strongest claims

1. The bounded Micron/Armadillo integration exposes a vendor-specific selective self-refresh path with explicit timing and telemetry.
2. Standard e.MMC Background Operations and vendor Self Refresh are distinct mechanisms/control surfaces.
3. By e.MMC 5.0, directly inspected standard text exposes host-supplied time plus periodic wakeup/background-maintenance semantics.
4. e.MMC 5.0 is **not** the origin of RTC-related reliability support: e.MMC 4.5 publicly introduced the RTC capability in June 2011.
5. JEDEC's own later revision history assigns `real time clock` to the 4.41 -> 4.5 transition.
6. `mmc-utils` corroborates `PERIODIC_WAKEUP[131]` as B45-generation EXT_CSD state.
7. A named Micron 4.51-generation component document from 2013–2014 explicitly advertises e.MMC `Real-time clock` and exposes `PERIODIC_WAKEUP[131]`.
8. In that named product's register table, `PERIODIC_WAKEUP` is `R/W/E`, and the datasheet defines that persistence class as surviving power cycle, `RST_n`, and `CMD0` reset.
9. The same Micron MCP datasheet separately documents LPDDR2 `SELF REFRESH`; same package/vendor/vocabulary does not make the DRAM and e.MMC mechanisms identical.
10. The exact B45/B451 clause-level identity with later B50 semantics remains open.

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
PERIODIC_WAKEUP configured nonzero

PERIODIC_WAKEUP configured
    !=
wakeup event occurred

wakeup event
    !=
maintenance completion

reset-surviving policy
    !=
restart-surviving maintenance progress

PERIODIC_WAKEUP
    !=
BKOPS_START
    !=
BKOPS_EN

maintenance opportunity
    !=
maintenance completion

feature-introduction chronology
    !=
clause-level semantic identity

standard revision
    !=
device firmware revision

product document
    !=
shipment / deployment proof

product manual behavior
    !=
generic e.MMC behavior

e.MMC periodic-wakeup maintenance
    !=
LPDDR2 self refresh

current payload is readable
    !=
future retention margin is sufficient
```

## Remaining debt

Priority order for another bounded pass:

1. **Direct JESD84-B45 clause inspection** — exact RTC, `SET_TIME`, and `PERIODIC_WAKEUP` text.
2. **Direct JESD84-B451 clause inspection** — exact delta against B45 and B50.
3. Determine whether `PERIODIC_WAKEUP` encoding, reset/default behavior, optionality, or completion language changed from 4.5 -> 4.51 -> 5.0.
4. Find a **named e.MMC 4.5 component** — not merely 4.51 — whose own datasheet explicitly exposes RTC / periodic-wakeup support.
5. Find contemporaneous ordering/shipment or board/BOM evidence if a claim about actual 2011–2013 deployment is needed; do not infer shipment from datasheet revision date.
6. Trace host-software adoption only if it helps explain the control boundary; do not turn this case into a generic Linux MMC history.
7. Obtain stronger Micron primary material if it becomes publicly inspectable, especially for the internal selective-refresh algorithm, while avoiding inference from generic JEDEC language.

## Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `eMMC PERIODIC_WAKEUP RTC SET_TIME` found no dedicated reusable module in this pass.

Broader e.MMC standards genealogy, Micron MCP product-line history, controller-market history, host-driver adoption, and mobile-platform deployment remain `computing-archaeology` work. This case keeps only the retention-specific relation among temporal evidence, retained wakeup policy, execution opportunity, selective renewal, and maintenance completion/history state.

## Status decision

**Remain `grounded`.**

The named 2013–2014 Micron 4.51 component closes a real evidence gap by moving RTC / `PERIODIC_WAKEUP` from standards-history abstraction into a product-specific register table and by directly exposing a reset/power-cycle persistence class. It does not yet close the exact B45/B451 normative delta, provide a named 4.5 device, prove 2011–2013 shipment/deployment, or establish the physical implementation of the retained policy field, so promotion would be premature.
