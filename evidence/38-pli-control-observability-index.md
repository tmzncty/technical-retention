# Case 38 — PLI control / observability evidence navigation

Status: **navigation only**

Canonical case: [`../cases/38-intel-dc-s3700-pli-self-test-validation.md`](../cases/38-intel-dc-s3700-pli-self-test-validation.md)

Canonical maturity remains: **`grounded`**

This is a focused navigation page for the recent Case 38 control-state and observability deepenings. It is **not** intended to replace the complete Case 38 evidence inventory or `CASE_INDEX.md`.

---

## 1. Two adjacent but distinct questions

### A. How long does the self-test policy state live?

[`38-2006-2012-sct-feature-control-persistence-boundary-deepening.md`](38-2006-2012-sct-feature-control-persistence-boundary-deepening.md)

Bounded question:

> The DC S3700 exposes a vendor SCT Feature Control item for the capacitor-test interval. What does the surrounding SCT control framework say about current versus persistent feature state, and what may or may not survive reset boundaries?

Core boundary:

```text
self-test cadence policy state
    !=
PLI capacitor hardware state
    !=
self-test result telemetry
```

That packet closes only the **protocol-level existence of persistence semantics**. It does not claim that Intel's D000h item supports every persistence option or establish D000h behavior across every reset/power transition.

### B. How much historical distinction does self-test telemetry preserve?

[`38-2014-2015-pli-smart-counter-saturation-observability-deepening.md`](38-2014-2015-pli-smart-counter-saturation-observability-deepening.md)

Bounded question:

> Do the documented AFh fields preserve an indefinitely exact history of PLI self-test recency and count?

Core boundary:

```text
maintenance telemetry retained
    !=
exact maintenance history retained
```

Intel documents saturation of the minutes-since-last-test and lifetime-test fields, and documents that the lifetime-test counter excludes power-cycle tests.

That packet therefore treats AFh as a bounded observability surface rather than a lossless event history.

---

## 2. Do not collapse the layers

For Case 38, keep at least the following objects distinct:

```text
PLI energy-reserve hardware state
    !=
self-test cadence / scheduling policy
    !=
current embodiment of that policy
    !=
persistent/fallback policy state
    !=
self-test execution
    !=
self-test result
    !=
test freshness / recency
    !=
lifetime test accounting
    !=
power-loss-event accounting
    !=
current PLI readiness
```

A result in one layer should not silently be promoted into a claim about another.

Examples:

```text
D000h policy retained
    !=
a recent self-test occurred

AFh pass result visible
    !=
the result is fresh

AFh counter saturated
    !=
self-testing stopped

telemetry remains readable
    !=
exact history remains recoverable
```

---

## 3. Controlled cross-case links

These are functional comparisons only.

- [`../docs/SYNTHESIS_29_MAINTENANCE_OBSERVABILITY_COVERAGE_ACCOUNTING.md`](../docs/SYNTHESIS_29_MAINTENANCE_OBSERVABILITY_COVERAGE_ACCOUNTING.md) — provides the broader observability contract: an observable needs target, scope, horizon, producer, and update semantics before it can support a closure claim.
- Case 14 — SCSI repair-policy Current / Saved / Default state is a useful comparison for control-state lifetime, but does not imply the same persistence mechanism as SCT Feature Control.
- Case 67 — SSD maintenance counters are a useful comparison for accounting/closure boundaries, but do not imply the same counters, firmware, or genealogy as S3700 AFh.
- Case 85 — ONFI feature/reset state is a useful comparison for state-class-specific reset semantics, but is a different interface and technology layer.

---

## 4. Current bounded status

The recent Case 38 work now supports two independent conclusions:

```text
standardized control framework may expose
feature-state lifetime / persistence semantics
```

and:

```text
vendor maintenance telemetry may intentionally
collapse multiple distinct histories into one bounded state
```

Neither conclusion changes Case 38's canonical maturity beyond **`grounded`**.

No maturity promotion is warranted merely because another control/telemetry boundary has been documented.

---

## 5. Open debt worth pursuing next

The strongest remaining bounded questions are:

1. Obtain Intel documentation or physical-device evidence for D000h `Return feature option flags` and the exact state/persistence options implemented by S3700 firmware.
2. Observe D000h across ATA hard reset, COMRESET, controller reset, and full power cycle without conflating those events.
3. Determine the reset/clear lifetime of AFh event/test counters and pass/fail state.
4. Determine exactly how a new self-test updates AFh recency/result when the prior recency field has saturated.
5. Bound the meaning of Intel's "power-cycle test" and why it is excluded from the lifetime-test counter.
6. Look for firmware-version differences rather than treating one product specification as proof of all revisions.
7. If hardware is available, capture before/after SMART and SCT state under controlled reset/fault conditions.

These debts can be pursued independently; none requires reopening the already-bounded conclusions above.

---

## 6. Related repository routing

Targeted searches in `tmzncty/computing-archaeology` during these two deepenings did not identify a dedicated S3700 PLI / AFh / SCT packet to reuse.

If a broader ATA/SCT/SMART historical packet appears there later, Case 38 should link to it for chronology and keep this repository focused on retention-state and observability boundaries.
