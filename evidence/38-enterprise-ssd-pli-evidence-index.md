# Case 38 Evidence Index — Enterprise SSD PLI Readiness, Policy, and Safe Degradation

## Status

- **Case:** [`../cases/38-intel-dc-s3700-pli-self-test-validation.md`](../cases/38-intel-dc-s3700-pli-self-test-validation.md)
- **Current maturity:** `grounded`
- **This index:** navigation only; no maturity promotion
- **Primary named product:** Intel SSD DC S3700, with S3500 included only where the inspected Intel PLI brief explicitly covers both

This index keeps the Case 38 evidence chain from collapsing four different questions into one:

```text
power-loss protection exists
    !=
protection path is currently qualified
    !=
qualification work is scheduled by a retained policy
    !=
negative qualification evidence changes operating authority
```

The case is about the retention infrastructure that protects acknowledged writes during external power loss, but the evidence is deliberately split by historical/source layer and by control-state role.

---

## Evidence chain

### 1. Canonical case — PLI mechanism, readiness telemetry, and validation scope

**File:** [`../cases/38-intel-dc-s3700-pli-self-test-validation.md`](../cases/38-intel-dc-s3700-pli-self-test-validation.md)

Grounds the core named-product relation:

```text
PLI capacitors / switching / NAND transfer
    -> periodic capacitor self-test
    -> host-visible AFh readiness evidence
    -> separate event history in AEh
    -> separate wider fault-validation campaign
```

Important anti-collapse:

```text
self-test result
    !=
whole-device power-loss correctness
```

The canonical case also keeps NAND data-retention qualification separate from the short emergency-energy path used by PLI.

### 2. 2012 chronology and early control surface

**File:** [`38-intel-s3700-2012-pli-self-test-control-surface-prior-art-deepening.md`](38-intel-s3700-2012-pli-self-test-control-surface-prior-art-deepening.md)

Purpose:

- moves the directly inspected named-product documentary floor to Intel's October-2012 S3700 Product Specification;
- keeps the internal June-2012 revision-history entry distinct from the October printed document date and 12-November-2012 public fact sheet;
- grounds `AEh`, `AFh`, capacitor self-test, and SCT `D000h` interval control without importing later explanatory wording into 2012.

Control relation:

```text
power-loss-protection mechanism
    !=
readiness result/history
    !=
test-interval control
```

### 3. Negative readiness evidence and write-cache authority

**File:** [`38-s3700-2013-ocp-2023-pli-failure-write-cache-authority-deepening.md`](38-s3700-2013-ocp-2023-pli-failure-write-cache-authority-deepening.md)

Purpose:

- distinguishes Intel first-party product state from contemporary secondary reporting and later OCP institutional requirements;
- asks whether failed/insufficient PLP evidence can constrain use of volatile write-back caching;
- does not turn later OCP requirements into retroactive S3700 product history.

Engineering reconstruction:

```text
readiness evidence
    -> qualification of future durability path

negative readiness evidence
    -> preserve already-cached work
    -> revoke risk-bearing volatile-cache authority
```

The source levels remain explicit: Intel 2012 does not itself prove the full automatic cache-disable chain attributed to the named S3700 by the 2013 secondary witness.

### 4. PLI cadence policy and its reset/power-cycle persistence boundary

**File:** [`38-intel-s3700-pli-cadence-persistence-boundary-deepening.md`](38-intel-s3700-pli-cadence-persistence-boundary-deepening.md)

Purpose:

- starts from Intel's named `D000h` `Power Safe Write Cache capacitor test interval`;
- checks the generic SCT Feature Control persistence semantics in T13 ACS-3;
- separates current configurability from persistence across reset/power-cycle boundaries;
- identifies the missing product-specific binding between Intel `D000h` and the SCT per-feature persistence option.

Key anti-collapse:

```text
host can configure maintenance cadence
    !=
configured cadence is proven restart-persistent
```

and:

```text
generic SCT persistence mechanism exists
    !=
public product proof that D000h uses one particular persistence mode
```

This is the current deepest policy-state boundary for Case 38.

---

## Unified Case 38 state model

The evidence now supports keeping at least five layers separate:

```text
1. protected payload / acknowledged write state
        |
        v
2. PLI emergency-transfer mechanism
        |
        v
3. PLI readiness / health evidence
        |
        +---------------------------+
        |                           |
        v                           v
4. maintenance policy         5. operating authority
   (when to retest)              (e.g. whether a risky
                                  volatile mode remains allowed)
```

A more chronological control chain is:

```text
PLI hardware exists
    -> cadence policy determines future self-test opportunity
    -> self-test executes
    -> readiness evidence is updated
    -> management / firmware can react to degraded evidence
    -> future power-loss event exercises the protection path
```

The evidence does **not** justify collapsing these arrows into an assertion that every state has the same persistence horizon.

---

## Historical vocabulary vs repository vocabulary

### Historical / source vocabulary

Use these when describing the Intel/T13 record:

- `Power safe write cache with built in self-test`
- `Power Loss Capacitor Test`
- `Power Safe Write Cache capacitor test interval`
- `D000h`
- `SMART Command Transport (SCT)`
- `AEh Unexpected Power Loss`
- `AFh Power Loss Protection Failure`
- `Software Settings Preservation`
- `FEATURE STATE VOLATILITY`
- `Vendor Specific`

### Engineering reconstruction vocabulary

These are repository terms, not Intel/T13 historical wording:

- `retention-infrastructure readiness`
- `maintenance-of-maintenance`
- `qualification closure`
- `write-cache authority`
- `maintenance policy state`
- `maintenance execution state`
- `maintenance-policy persistence horizon`
- `safe degradation`

Do not back-project the second list into the sources.

---

## Source hierarchy

For Case 38, prefer evidence in this order when making product claims:

1. Intel S3700/S3500 first-party product specifications and Intel PLI documentation.
2. T13 ATA/SCT standards for generic interface semantics, with chronology kept explicit.
3. Later institutional requirements such as OCP only for bounded functional comparison or later control-policy evidence.
4. Contemporary secondary product reporting only when no first-party clause closes the exact product behavior, and label it as secondary.
5. Repository engineering reconstruction after the historical/source layer is complete.

A generic ATA mechanism never substitutes for a product-specific proof about `D000h`.

---

## Cross-case links

These are functional comparisons only.

### Case 15 — Intel SSD 320 power-loss protection

Use for the earlier controller-mediated emergency durability handoff. Case 38 should not repeat Case 15's basic capacitor-backed transfer mechanism history.

### Case 101 — SCSI Background Medium Scan

Useful comparison for maintenance observability across power epochs:

```text
maintenance state visible now
    !=
proof of what survived a prior power boundary
```

No genealogy claim.

### Case 116 — HDFS DataNode maintenance state

Useful comparison for maintenance intent/policy versus current controller materialization:

```text
maintenance obligation
    !=
current controller-local state
```

No genealogy claim.

---

## What is closed

Case 38 now has bounded evidence for:

- PLI as a named emergency durability mechanism;
- periodic capacitor self-test;
- separate power-loss event history and PLI-health state;
- result, recency, and lifetime-test-count telemetry;
- host-visible cadence control through SCT `D000h`;
- a source-level distinction between cadence configurability and cadence persistence;
- negative readiness evidence as a possible constraint on volatile-cache authority, with source levels kept separate;
- whole-device power-loss validation as a different evidence class from the capacitor self-test.

---

## Highest-value remaining debt

### P1 — measured D000h persistence trace

Run a named S3700 through:

```text
set non-default D000h
    -> read back
    -> controlled reset class
    -> read back D000h / option flags
    -> observe actual next self-test timing
    -> inspect AFh result/history
```

Separate software reset, link/COMRESET, hardware reset where controllable, and full power removal.

### P2 — product-specific SCT option documentation

Find an Intel first-party management manual, engineering note, tool transcript, or firmware/interface document that explicitly reports the option flags or reset semantics for `D000h`.

### P3 — physical fault validation of readiness-to-authority chain

Independently induce a bounded PLI-health failure and observe whether the named S3700 firmware actually changes write-cache state, while distinguishing manufacturer contract, host-visible state, and measured behavior.

### P4 — persistence of AFh subfields

Determine which AFh readiness/history fields survive each reset/power transition on a named drive rather than assuming that `lifetime`, `minutes since last test`, and latest discharge result share one persistence domain.

---

## Related repository boundary

The current `tmzncty/computing-archaeology` search surface did not expose a reusable dedicated S3700 `D000h` / SCT-persistence packet during the latest deepening pass.

Broader histories of ATA SCT, SMART, SATA Software Settings Preservation, Intel enterprise-SSD generations, and capacitor-backed storage belong there if later developed. `technical-retention` should keep only the evidence needed to reason about:

```text
mechanism
    -> maintenance policy
    -> execution
    -> readiness evidence
    -> operating authority
    -> future fault survival
```

---

## Maturity decision

**Remain `grounded`.**

Reason:

- the historical product/interface evidence is strong enough to deepen the case;
- the exact D000h reset/power-cycle behavior remains unmeasured and publicly under-specified in the inspected Intel product record;
- no new independent product fault trace justifies promotion.

`CASE_INDEX.md` should therefore remain unchanged for this slice.
