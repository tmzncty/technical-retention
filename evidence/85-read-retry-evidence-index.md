# Case 85 — Read-Retry Evidence Navigation

**Canonical case:** [`../cases/85-toshiba-nand-shift-read-retry-recoverability.md`](../cases/85-toshiba-nand-shift-read-retry-recoverability.md)

**Canonical status:** `grounded`

This compact page groups the source-level deepenings for Case 85. It is navigation only: the canonical case remains authoritative for scope, claims, and maturity. Where an older evidence packet deliberately left a narrower source question unresolved, a later packet may supersede only that explicit open boundary without rewriting unrelated claims.

## Evidence chain

1. [`85-flash-2000-2021-read-threshold-retry-grounding.md`](85-flash-2000-2021-read-threshold-retry-grounding.md)
   - core grounding for adaptive/reference-voltage rereading, Toshiba shift/retry read, ECC-bound recoverability, and the separation between read-side recovery and later refresh/rewrite;
   - includes the 2000-priority prior-art control and 2021 empirical 3D TLC witness.

2. [`85-onfi-2006-2011-feature-reset-eznand-retry-deepening.md`](85-onfi-2006-2011-feature-reset-eznand-retry-deepening.md)
   - ONFI 1.0/2.0 feature-state reset semantics;
   - ONFI 2.3 EZ NAND automatic-retry capability and feature-`50h` `Retry Disable` control;
   - distinguishes standardized retry policy/admission from vendor-specific raw-NAND retry parameter representation;
   - keeps feature `89h` inside the ONFI vendor-specific namespace rather than mislabeling it as a cross-vendor standard.

3. [`85-linux-2014-2017-vendor-read-retry-parameter-state-deepening.md`](85-linux-2014-2017-vendor-read-retry-parameter-state-deepening.md)
   - upstream Linux witnesses for Micron and Hynix vendor-specific retry capability/calibration state;
   - separates generic retry hooks from vendor parameter representation and OTP-derived calibration.

4. [`85-micron-2015-read-retry-mode-power-boundary-deepening.md`](85-micron-2015-read-retry-mode-power-boundary-deepening.md)
   - Micron L83A product-family witness for feature `89h`, eight retry options, and a selected-mode lifetime extending across reads until rewrite of the feature or power-down;
   - its earlier deliberate non-claim about exact `89h` survival across `FFh` is superseded only on that narrow point by evidence item 6 below.

5. [`85-micron-2018-2020-read-retry-reset-class-boundary-deepening.md`](85-micron-2018-2020-read-retry-reset-class-boundary-deepening.md)
   - later Micron-primary design witness separating ordinary-reset examples from `Hard Reset (FDh)` and power-cycle retirement of custom retry state;
   - deliberately does not back-project `FDh` semantics onto the 2015 L83A family.

6. [`85-micron-2015-read-retry-reset-survival-correction-deepening.md`](85-micron-2015-read-retry-reset-survival-correction-deepening.md)
   - exact-family correction using the same May-2015 L83A datasheet's `Configuration Operations` and reset sections;
   - grounds the vendor rule that feature-address values remain unchanged across host `RESET (FFh, FCh, FAh)` unless a feature-specific exception says otherwise;
   - feature `89h` is `Read Retry` and its table contains no reset-specific exception, while the read-retry section separately ends the selected mode at feature rewrite or power-down;
   - keeps this reset-surviving reader configuration separate from in-flight array work, command state, and data/cache-register contents that RESET may cancel or invalidate.

## Current bounded result

The evidence chain now requires at least these distinct layers:

```text
physical NAND threshold state
    !=
ECC / recoverability margin
    !=
retry capability / calibration state
    !=
currently selected retry mode
    !=
in-flight array-operation state
    !=
data/cache-register working state
    !=
higher-layer remembered retry advice
```

For the named 2015 Micron L83A family, the event-specific state lifetime can now be stated more precisely:

```text
feature 89h = option N
    -> persists across subsequent reads
    -> survives documented FFh / FCh / FAh reset classes
    -> can be changed/retired by explicit 89h rewrite
    -> does not survive power-down

while

FFh / FCh / FAh
    -> can cancel pending array work
    -> can invalidate data/cache-register contents
    !=
feature 89h automatically restored to default
```

So:

```text
operation aborted
    !=
reader configuration retired
```

and:

```text
command-to-command persistence
    !=
reset persistence
    !=
cross-power persistence
```

The ONFI deepening adds another important split:

```text
standardized recovery control surface
    !=
standardized internal recovery interpretation state
```

ONFI 2.3 does standardize a higher-level EZ NAND automatic-retry control, so `ONFI standardized no retry behavior` is too broad. But ONFI does not thereby standardize Micron feature `89h`, one raw-NAND retry table, or one threshold-search algorithm.

## Historical / reconstruction / analogy / interpretation boundary

### Historical record

The direct source set establishes adaptive read/retry vocabulary and prior art, vendor-specific Linux retry surfaces, Micron L83A feature `89h`, its read-to-read and power lifetime, the exact-family ordinary-reset survival rule, and later Micron design evidence for a stronger `FDh` reset class.

### Engineering reconstruction

The project derives:

- `recoverability renewal != representation renewal`;
- `capability state != selected state`;
- `operation aborted != reader configuration retired`;
- state continuity must be expressed as a relation between a named state class and a named event class.

### Functional analogy

Receiver/calibration analogies may clarify mutable interpretation state but establish no NAND implementation genealogy.

### Philosophical interpretation

A bounded downstream interpretation is that one device can contain overlapping temporal horizons: a reset may terminate work without terminating the interpretation condition used by later reads, while power-down can retire that interpretation state without erasing the nonvolatile payload.

## Prior-art / genealogy guardrails

Do not infer from this evidence that Toshiba or Micron invented read retry; that the 2014 Linux merge date is a first-commercial-use date; that ONFI standardizes Micron feature `89h`; that the 2018-priority Micron family proves the 2015 L83A's `FDh` behavior; that all NAND reset commands restore all runtime state; or that read retry refreshes, relocates, or sanitizes payload. Broader adaptive-sensing and proprietary-command genealogy belongs in `tmzncty/computing-archaeology` if pursued.

## Open debt

The highest-value narrow follow-ups are:

- real-device transcript on an L83A-family part: select nonzero `89h`, exercise `FFh`, `FCh`, and where supported `FAh`, then query `89h` again;
- distinguish specified power-down from brownout or partial power-domain collapse and observe reinitialization;
- identify the physical carrier of selected feature state without inferring it from interface semantics;
- named managed-SSD/controller evidence for durable per-page or per-block retry advice above the raw-NAND feature layer;
- named shipping-product evidence for ONFI EZ NAND automatic-retry behavior;
- named Micron product documentation for later `Hard Reset (FDh)` plus feature-`89h` semantics;
- cross-vendor reset-class comparison only after enough vendor-primary evidence exists;
- broader ONFI/Toggle/vendor retry genealogy only if routed to `tmzncty/computing-archaeology` rather than duplicated here.

The former `exact Micron L83A feature-89h behavior across RESET (FFh)` debt is now closed at the datasheet-contract level by evidence item 6.

**Status remains `grounded`; no maturity promotion is implied by this navigation update.**