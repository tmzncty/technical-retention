# Case 38 — Intel DC S3700/S3500 PLI evidence index

Canonical case:

- [`cases/38-intel-dc-s3700-pli-self-test-validation.md`](../cases/38-intel-dc-s3700-pli-self-test-validation.md)

This index separates four evidence questions that are easy to collapse into a single vague statement that an enterprise SSD “has power-loss protection.”

The useful decomposition is instead:

```text
physical emergency-energy capability
    !=
health / self-test evidence
    !=
maintenance-policy state
    !=
write-cache authority
    !=
full fault-validation evidence
```

No maturity promotion is implied by creating this index.

---

## 1. 2012 S3700 PLI self-test and host control surface

Packet:

- [`38-intel-s3700-2012-pli-self-test-control-surface-prior-art-deepening.md`](38-intel-s3700-2012-pli-self-test-control-surface-prior-art-deepening.md)

Primary question:

> What did Intel expose to the host for inspecting and controlling PLI-related behavior on the named S3700 product?

Evidence line:

```text
power-loss capacitor hardware
    ↓
partial-discharge self-test
    ↓
SMART health / status surfaces
    ↓
SCT Feature Control
    ↓
D000h capacitor-test interval
```

Key boundary:

```text
host-visible health / control surface
    !=
proof of full emergency-write correctness
```

Use this packet for the original product/interface grounding.

---

## 2. PLI failure and volatile-write-cache authority

Packet:

- [`38-s3700-2013-ocp-2023-pli-failure-write-cache-authority-deepening.md`](38-s3700-2013-ocp-2023-pli-failure-write-cache-authority-deepening.md)

Primary question:

> What should happen to write-cache authority when PLI is no longer trusted?

Evidence line:

```text
PLI fault detected
    ↓
retention guarantee weakened
    ↓
volatile write-cache authority must change
    ↓
operator-visible fault / degraded mode
```

Key boundary:

```text
failure detected
    !=
safe degraded behavior proven
```

The later OCP evidence is useful as a contract comparison, not as proof that the original S3700 firmware used an identical state machine.

---

## 3. Independent S3500 power-cut / hot-unplug validation

Packet:

- [`38-intel-s3500-2014-independent-power-cut-stack-validation-deepening.md`](38-intel-s3500-2014-independent-power-cut-stack-validation-deepening.md)

Primary question:

> How does full-stack fault validation differ from the device's own capacitor self-test?

Evidence line:

```text
self-test
    -> controlled internal health probe

power-cut / hot-unplug test
    -> external fault injection
    -> host/controller/drive interaction
    -> emergency persistence path exercised
```

Key boundary:

```text
capacitor test passes
    !=
power-cut behavior validated
```

This packet is the place to route claims about repeated external fault validation and test-stack conditions.

---

## 4. `D000h` maintenance-policy persistence boundary

Packet:

- [`38-intel-s3700-d000h-policy-persistence-boundary-deepening.md`](38-intel-s3700-d000h-policy-persistence-boundary-deepening.md)

Primary question:

> Does the configured capacitor-test interval itself survive reset and power loss, and what evidence would prove it?

Newly established split:

```text
S3700 D000h exposed through SCT Feature Control
    = established at named-product layer

SCT Feature Control persistent/non-volatile option
    = established at protocol layer

SCT Return feature option flags function
    = established at protocol layer

D000h-specific option flags on S3700
    = not yet observed

D000h persistent-set acceptance/default
    = not yet established
```

This narrows an earlier vague persistence debt into a concrete command-level experiment.

The packet also separates:

```text
configured test interval
    !=
current test execution
    !=
last test result
    !=
current capacitor health
    !=
write-cache authority
    !=
actual emergency-flush success
```

---

# Cross-case comparison

## Case 135 — eMMC periodic wake-up policy

Related packet:

- [`135-micron-2013-2014-emmc451-rtc-periodic-wakeup-product-deepening.md`](135-micron-2013-2014-emmc451-rtc-periodic-wakeup-product-deepening.md)

Useful comparison:

```text
Case 135
named maintenance-policy field
+ named-product persistence class explicitly documented

Case 38
named maintenance-policy field
+ generic protocol persistence mechanism documented
+ product-specific persistence result still missing
```

This is a **functional/evidentiary comparison**, not implementation genealogy.

The common retention pattern is that a rule governing future maintenance can itself have a persistence lifetime.

---

# Current state model

A compact Case 38 model is now:

```text
                 ┌─────────────────────────────┐
                 │ physical PLI energy reserve │
                 └──────────────┬──────────────┘
                                │
                                v
                 ┌─────────────────────────────┐
                 │ capacitor self-test / health│
                 └──────────────┬──────────────┘
                                │
                    health evidence / policy
                                │
                                v
                 ┌─────────────────────────────┐
                 │ volatile write-cache        │
                 │ authority / degradation     │
                 └──────────────┬──────────────┘
                                │
                                v
                 ┌─────────────────────────────┐
                 │ emergency persistence path  │
                 └─────────────────────────────┘

orthogonal control state:

D000h configured test interval
    -> decides when future PLI self-check is scheduled
    -> may itself be volatile or non-volatile under SCT semantics
    -> exact S3700 feature-specific persistence remains to be observed
```

The orthogonal state is important. A drive can have a healthy capacitor while the interval policy has reverted, or preserve the interval while a current self-test execution does not survive reset.

---

# Evidence boundaries to preserve

Do not collapse the following:

```text
self-test
    !=
fault injection

health telemetry
    !=
cache authority

maintenance interval
    !=
maintenance progress

protocol persistence option
    !=
named-feature persistence support

Software Settings Preservation
    !=
SCT Feature Control persistent Option Flag

power/reset persistence
    !=
firmware-update migration

later OCP requirement
    !=
2012 S3700 implementation proof

S3500 validation result
    !=
all S3700 firmware/capacity behavior
```

---

# Highest-value remaining debts

## A. Direct `D000h` transcript

On a preserved S3700, capture raw SCT Feature Control for:

- current `D000h` state;
- `D000h` option flags;
- volatile set;
- persistent set, if accepted;
- hard-reset result;
- full-power-cycle result.

This is currently the shortest path to a stronger named-product persistence claim.

## B. Firmware-update migration

Do not infer from power/reset persistence. Search Intel release notes / service tooling first; only then design a controlled update experiment.

## C. Self-test progress and result retention

Determine separately whether:

- a running test resumes/restarts after reset;
- the last result survives reset/power loss;
- result age / last-test time is exposed;
- a missed scheduled test produces a distinct state.

## D. Failure-to-authority ordering

Obtain evidence for the exact ordering among:

```text
PLI fault recognized
    -> cached writes drained / secured
    -> volatile write cache disabled
    -> host-visible health state changed
    -> attempts to re-enable cache rejected or accepted
```

Do not infer atomicity from the existence of all individual states.

## E. Capacity / firmware variation

Case 38 spans product-family and later cross-product evidence. Exact behavior should be tied to:

- capacity;
- firmware revision;
- form factor if relevant;
- command-interface revision.

---

# Related repository routing

A fresh search of `tmzncty/computing-archaeology` for `S3700` and `D000h` did not surface a dedicated historical packet that can be reused directly.

Therefore this index keeps only the retention-specific material here:

- PLI readiness;
- self-test evidence;
- maintenance-policy persistence;
- cache-authority consequences;
- external fault validation.

Broader SSD-controller, SATA-command, capacitor-technology, or Intel product-history work should remain in the companion technical-history repository if it is later developed there.

---

# Next recommended slice

The next Case 38 slice should **not** be another descriptive SSD/PLI overview.

Prefer one of these bounded targets:

1. an actual S3700 `D000h` SCT transcript;
2. Intel maintenance-tool evidence for `D000h` defaults and persistence;
3. firmware release-note evidence for PLI-failure state transitions;
4. an external fault-injection trace that correlates SMART health, cache authority, and reset behavior.

Until then, the correct conclusion remains:

```text
The product exposes a rule for scheduling its PLI self-check.
The protocol has a concept of retaining such feature state.
The exact S3700 D000h persistence contract is not yet directly observed.
```
