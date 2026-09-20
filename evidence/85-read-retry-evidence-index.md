# Case 85 — Read-Retry Evidence Navigation

**Canonical case:** [`../cases/85-toshiba-nand-shift-read-retry-recoverability.md`](../cases/85-toshiba-nand-shift-read-retry-recoverability.md)

**Canonical status:** `grounded`

This compact page groups the source-level deepenings for Case 85. It is navigation only: the canonical case remains authoritative for scope, claims, and maturity.

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
   - Micron L83A product-family witness for feature `89h`, eight retry options, and a selected-mode lifetime extending across reads until rewrite of the feature or power-down.

5. [`85-micron-2018-2020-read-retry-reset-class-boundary-deepening.md`](85-micron-2018-2020-read-retry-reset-class-boundary-deepening.md)
   - later Micron-primary design witness separating ordinary-reset examples from `Hard Reset (FDh)` and power-cycle retirement of custom retry state;
   - deliberately does not back-project those semantics onto the 2015 L83A family.

## Current bounded result

The evidence chain now supports five distinct layers:

```text
physical NAND threshold state
    !=
ECC / recoverability margin
    !=
retry capability / calibration state
    !=
current retry admission or selected mode
    !=
reset / power event that retires that state
```

The ONFI deepening adds another important split:

```text
standardized recovery control surface
    !=
standardized internal recovery interpretation state
```

ONFI 2.3 does standardize a higher-level EZ NAND automatic-retry control, so `ONFI standardized no retry behavior` is too broad. But ONFI does not thereby standardize Micron feature `89h`, one raw-NAND retry table, or one threshold-search algorithm.

## Open debt

The highest-value narrow follow-ups are:

- exact Micron L83A feature-`89h` behavior across `RESET (FFh)` for the 2015 family;
- named shipping-product evidence for ONFI EZ NAND automatic-retry behavior;
- independent timing/fault observation connecting a named device's extended read latency to retry attempts;
- broader ONFI/Toggle/vendor retry genealogy only if routed to `tmzncty/computing-archaeology` rather than duplicated here.

**Status remains `grounded`; no maturity promotion is implied by this navigation update.**
