# Case 38 deepening — Intel DC S3700 PLI SMART counter saturation and bounded observability (2014–2015)

Status: **bounded deepening complete**

Canonical case: [`../cases/38-intel-dc-s3700-pli-self-test-validation.md`](../cases/38-intel-dc-s3700-pli-self-test-validation.md)

Related Case 38 deepening:

- [`38-2006-2012-sct-feature-control-persistence-boundary-deepening.md`](38-2006-2012-sct-feature-control-persistence-boundary-deepening.md) — SCT Feature Control lifetime/persistence semantics for the self-test-interval control plane.

This note isolates a different question:

> What history does the S3700 PLI SMART telemetry actually preserve, and what historical distinctions are lost when its finite counters saturate or omit a class of tests?

It does **not** re-open the electrical PLI design, capacitor chemistry, ATA SMART history, or SCT command history except where needed to bound this observability claim.

---

## 1. Why this slice exists

The existing Case 38 material establishes several distinct things:

1. the drive contains power-loss-imminent protection hardware;
2. the capacitor subsystem is periodically tested;
3. Intel exposes PLI-related state through SMART attribute `AFh` / decimal 175;
4. Intel also exposes an SCT feature controlling the capacitor-test interval.

Those facts are enough to show that the protection mechanism has both maintenance policy and telemetry.

They are **not** enough to say that the telemetry preserves an indefinitely precise maintenance history.

Two Intel documents provide a narrow but unusually clean counterexample:

- the "minutes since last test" field saturates at its maximum representable value;
- the "lifetime number of tests" field also saturates;
- the lifetime-test field does not count a power-cycle test.

Thus a still-readable SMART record can be a deliberately lossy projection of the underlying maintenance history.

That is the boundary deepened here.

---

## 2. Source ledger

### S1 — Intel, *Power Loss Imminent (PLI) Technology Brief* (2014)

Vendor-authored technology brief, currently hosted by Solidigm as an Intel-origin document:

- https://www.solidigm.com/content/dam/solidigm/en/site/products/technology/power-loss-imminent-technology-brief/Power-Loss-Imminent-Technology-Brief.pdf

Relevant material is on the page describing SMART attribute 175 / `AFh` and PLI health reporting.

The brief states, in substance, that:

- the capacitor bank is periodically tested;
- SMART attribute 175 (`AFh`) identifies PLI health;
- one raw-value field records minutes since the last test and saturates at a maximum value;
- another records the lifetime number of tests, is not incremented for a power-cycle test, and saturates at a maximum value;
- a further field reports the test result.

Source class: **primary vendor technical document**.

### S2 — Intel, *Intel Solid-State Drive DC S3700 Series Product Specification*, January 2015, document 328171-010US

Intel product specification for the shipping product family.

Official Intel-hosted PDF:

- https://www.intel.com/content/dam/www/public/us/en/documents/product-specifications/ssd-dc-s3700-spec.pdf

Relevant SMART table: attribute `AFh`, "Power Loss Protection Failure".

The table defines:

- bytes 0–1: power-loss event count;
- bytes 2–3: minutes since the last test, saturating at the maximum value;
- bytes 4–5: lifetime number of tests, not incremented on a power-cycle test, saturating at the maximum value;
- byte 6: test failure indication (`1` failed, `0` passed).

The 16-bit counter fields have a maximum representable value of 65,535.

Source class: **primary vendor product specification**.

### Source-custody note

The two sources are not independent manufacturers: both are Intel-origin documents and therefore do not provide independent third-party validation of firmware behavior. They are, however, strong evidence for the interface semantics Intel documented for the product.

This note does not claim that every firmware revision was experimentally checked against the documentation.

---

## 3. Historical record

This section records only what the period/vendor documents expose.

### 3.1 PLI self-test health was externally observable

By 2014–2015 Intel documented PLI health through SMART attribute 175 / `AFh` on the DC S3700 family.

The exposed object was not a single Boolean "PLI good" bit. It included multiple fields representing different relations:

```text
power-loss-event count
minutes since last test
lifetime number of tests
test result
```

The interface therefore distinguished at least event accounting, test recency, test-count accounting, and pass/fail outcome.

### 3.2 The recency field is finite and saturating

Intel documents the "minutes since last test" field as saturating at its maximum value.

For the 16-bit field documented in the product specification, the representable ceiling is 65,535 minutes.

Therefore the interface does not preserve arbitrary test age as an exact indefinitely increasing integer.

### 3.3 The lifetime-test field is also finite and saturating

Intel likewise documents the lifetime number of tests as saturating at its maximum representable value.

Once the field reaches that ceiling, further counted tests do not create a new larger externally visible value in that field.

### 3.4 The lifetime-test field omits a documented event class

Intel explicitly says the lifetime number of tests is **not incremented on a power-cycle test**.

Therefore, even below saturation, the field is not documented as "the number of every occasion on which the PLI subsystem was exercised."

It is a counter with a defined inclusion rule.

### 3.5 Pass/fail and freshness are separate fields

Intel exposes the test result separately from minutes since the last test.

That interface structure itself is historical evidence that:

```text
test outcome
    !=
test recency
```

A parser that reads only the pass/fail byte discards information that Intel deliberately exposes separately.

---

## 4. Engineering reconstruction

Everything in this section is an engineering reconstruction from the documented interface semantics, not vocabulary attributed to Intel.

### 4.1 A finite telemetry field is a projection, not the history itself

Let:

- `H` be the underlying sequence of self-test-related events and elapsed time;
- `O` be the externally readable AFh telemetry state.

The drive exposes a mapping:

```text
H -> O
```

Because at least two fields saturate, this mapping is many-to-one.

Distinct histories can yield the same externally visible state.

For the recency field:

```text
actual elapsed time = 65,535 minutes
actual elapsed time = 70,000 minutes
actual elapsed time = 100,000 minutes

        ->

same saturated "minutes since last test" value
```

provided no later event resets/updates the field in a way that changes the observation.

For the lifetime-test field:

```text
65,535 counted tests
65,536 counted tests
80,000 counted tests

        ->

same saturated lifetime-test-count value
```

within an unchanged counter epoch and under the documented saturation rule.

### 4.2 Saturation creates loss of exact distinguishability, not necessarily loss of function

The safe claim is:

```text
counter saturated
    ->
exact larger value is no longer distinguishable through that field
```

The unsafe claim is:

```text
counter saturated
    ->
device stopped testing
```

Intel documents saturation of the telemetry representation, not cessation of the underlying maintenance activity.

Likewise:

```text
minutes field saturated
    !=
PLI hardware failed
```

and:

```text
lifetime-test counter saturated
    !=
self-test scheduler failed
```

### 4.3 A "lifetime" counter is still governed by an inclusion rule

The phrase "lifetime number of tests" is easy to over-read.

Intel's explicit exclusion of power-cycle tests means:

```text
visible lifetime-test count
    !=
count of every PLI test-like exercise or trigger
```

This is true independently of saturation.

There are therefore at least two different observability limits:

1. **event-class omission** — a documented class is not added to this counter;
2. **numeric saturation** — additional included events cease to create a distinguishable larger count after the ceiling.

### 4.4 Test result does not establish test freshness

A passing result field says something about the result represented by that field.

It does not, by itself, answer how recently the represented test occurred.

Thus:

```text
last represented test passed
    !=
last represented test is recent
```

The separately exposed recency field must be interpreted according to its own update and saturation semantics.

At saturation, "65,535" is not safely interpretable as "exactly 65,535 minutes ago." It is the ceiling state of that field.

### 4.5 Telemetry survival is weaker than exact-history survival

Case 38 can therefore distinguish:

```text
telemetry record remains readable
    !=
telemetry retains exact event cardinality
    !=
telemetry retains exact event age
    !=
underlying maintenance is current
    !=
PLI hardware is presently ready
```

A readable AFh attribute is evidence that an observability surface exists.

It is not proof that every relevant distinction in the subsystem's history remains recoverable from that surface.

### 4.6 Bounded counters preserve useful relations despite losing exact history

The bounded nature of the counters does not make them useless.

Before saturation, and subject to reset/update semantics, the fields can still provide useful ordering, recency, and activity evidence.

After saturation, the state can still communicate a bounded proposition such as:

```text
represented quantity reached at least the interface ceiling
```

But the exact stronger proposition is unavailable from that field alone.

The distinction is:

```text
useful retained evidence
    !=
lossless historical record
```

### 4.7 A maintenance-observability contract must include update semantics

A useful abstraction for this case is:

```text
observable O
produced by mechanism P
about target relation R
over scope S
with lifetime/reset horizon H
and update semantics U
```

For AFh, `U` matters materially because it includes at least:

- saturation;
- the exclusion of power-cycle tests from one counter;
- separate update meanings for age, count, event count, and pass/fail fields.

Merely naming the attribute is not enough to interpret it.

---

## 5. Controlled functional comparison

These comparisons are functional only. They do not establish common implementation, terminology, or genealogy.

### 5.1 Synthesis 29 — maintenance observability

[`../docs/SYNTHESIS_29_MAINTENANCE_OBSERVABILITY_COVERAGE_ACCOUNTING.md`](../docs/SYNTHESIS_29_MAINTENANCE_OBSERVABILITY_COVERAGE_ACCOUNTING.md) distinguishes schedule, admission, execution, coverage, accounting, closure, and revalidation.

The S3700 AFh fields provide a concrete device-level example of why an observability contract needs explicit update semantics:

```text
counter exists
    !=
counter distinguishes every relevant historical state
```

and:

```text
pass/fail exists
    !=
freshness established
```

### 5.2 Case 67 — SSD refresh accounting

Case 67 uses device counters to reason about maintenance-related activity.

The controlled comparison is only:

```text
maintenance counter value
    !=
complete proof of maintenance closure
```

Case 38 contributes a specific additional reason: finite saturation and event-class inclusion rules can constrain what can be inferred from a counter.

No shared firmware mechanism is claimed.

### 5.3 The immediately previous Case 38 SCT persistence deepening

The previous Case 38 deepening asks whether the **policy controlling test cadence** has volatile/persistent lifetime semantics.

This note asks whether the **telemetry reporting test history** preserves all historical distinctions.

Keep them separate:

```text
self-test cadence policy state
    !=
self-test history telemetry state
```

A policy can be correctly retained while history telemetry is lossy; telemetry can remain readable while the policy has changed.

---

## 6. Philosophical interpretation

This section is interpretation, not historical vocabulary.

A saturating counter is a compact example of technical retention that intentionally preserves only a bounded relation to the past.

The system does not need to retain an infinitely precise biography of its maintenance activity in order to remain useful. It can retain enough evidence for a particular operational purpose while collapsing distinctions that the interface no longer represents.

In that narrow interpretive sense:

```text
retention
    can preserve operationally useful evidence
    without preserving exact history
```

And technical forgetting can occur not only through deletion of an artifact, but through **many-to-one representation**:

```text
multiple distinct pasts
    ->
one current observable state
```

This is an analytical interpretation only. Intel does not describe AFh saturation using the language of "forgetting."

---

## 7. Explicit non-claims

This evidence does **not** claim that:

1. AFh saturation causes PLI hardware failure.
2. AFh saturation stops future capacitor tests.
3. a saturated lifetime-test count means the drive has executed exactly 65,535 total PLI exercises of every kind.
4. a value of 65,535 minutes means the last test occurred exactly 65,535 minutes ago once the field has saturated.
5. power-cycle tests never exercise the PLI subsystem; the documented claim is only that they do not increment the lifetime-test field.
6. the pass/fail byte alone proves current PLI readiness.
7. the recency field alone proves the capacitor bank will sustain a future power-loss event.
8. SMART AFh preserves a complete event log.
9. the AFh raw fields form an append-only audit trail.
10. the counters survive every reset, sanitize, firmware update, secure erase, factory process, or controller replacement.
11. "lifetime" means an independently verified immutable lifetime across every possible device transition.
12. Intel's two documents constitute independent third-party validation.
13. every S3700 firmware revision was empirically tested in this evidence packet.
14. every vendor encodes PLI telemetry using the same fields or saturation rules.
15. saturation semantics imply wraparound; Intel documents saturation, not wraparound.
16. saturation semantics imply the field is frozen permanently; a later relevant update may change fields according to firmware semantics.
17. exact history can never be recovered from any other source; the claim is only about what this AFh field itself distinguishes.
18. a non-saturated counter necessarily proves continuity across an undocumented reset boundary.
19. the power-loss-event counter has the same inclusion and saturation semantics as the lifetime-test counter unless separately documented.
20. telemetry loss of distinguishability is payload-data loss.
21. telemetry saturation is equivalent to media wear-out.
22. telemetry saturation is equivalent to maintenance debt.
23. a passing PLI self-test proves host data was successfully protected during every prior power-loss event.
24. a high lifetime-test count proves tests occurred at the intended cadence.
25. the AFh counters establish why a particular test was scheduled.
26. the AFh counters expose the SCT feature value that scheduled testing.
27. the AFh counters and SCT D000h state share the same persistence horizon.
28. this evidence establishes the exact reset/clear behavior of every AFh raw field.
29. this evidence establishes a genealogy from S3700 telemetry to later SSD telemetry standards.
30. the analytical term "technical forgetting" is Intel's historical terminology.

---

## 8. Claim ledger

| Claim | Evidence class | Strength | Boundary |
|---|---|---:|---|
| S3700 exposes PLI health through SMART AFh / 175 | Intel vendor docs | high | product-family interface semantics |
| minutes-since-last-test saturates at maximum | Intel vendor docs | high | documented field behavior |
| lifetime-number-of-tests saturates at maximum | Intel vendor docs | high | documented field behavior |
| lifetime test counter omits power-cycle test | Intel vendor docs | high | documented inclusion rule |
| test result is a separate field from test recency | Intel vendor docs | high | interface decomposition |
| saturated field cannot distinguish larger exact values | engineering reconstruction | high | follows from saturation semantics |
| AFh is a lossy projection of full maintenance history | engineering reconstruction | high | limited to the exposed fields described here |
| readable telemetry does not prove freshness/readiness | engineering reconstruction | medium-high | requires interpreting fields according to their separate meanings |
| bounded representation is a form of technical forgetting | philosophical interpretation | interpretive | not historical vendor vocabulary |

---

## 9. What this closes

This packet closes the bounded Case 38 question:

> Does the documented PLI SMART interface preserve an indefinitely exact history of test age and test count?

No.

Intel explicitly documents finite saturating fields, and the lifetime-test count has a documented exclusion rule for power-cycle tests.

The strongest supported reconstruction is:

```text
maintenance telemetry retained
    !=
exact maintenance history retained
```

and:

```text
observable value
    must be interpreted with
    update semantics + event inclusion + saturation boundary
```

---

## 10. Remaining debt

The following questions remain open and should not be silently inferred from this packet:

1. Which AFh raw fields, if any, are cleared or reinitialized by ATA hard reset, COMRESET, power cycle, secure erase, sanitize, firmware update, or factory procedures?
2. Is the documented saturation behavior identical across all S3700 firmware revisions?
3. What precise operation does Intel mean by the excluded "power-cycle test" in each firmware generation?
4. Does a new self-test after the recency field has saturated reset the field immediately and under what completion/failure conditions?
5. How is an old pass/fail result invalidated or superseded if testing becomes stale?
6. Can Intel service/debug logs preserve distinctions that AFh collapses?
7. Can a physical S3700/S3500 experiment observe the relevant reset and update transitions without relying solely on documentation?
8. Can firmware or emulator instrumentation reproduce the 65,535 ceiling transitions without impractical wall-clock waiting?

These are suitable future deepening slices. They are not prerequisites for the bounded saturation conclusion above.

---

## 11. Related-repository routing

A targeted search of `tmzncty/computing-archaeology` for S3700 `AFh`, PLI, and the 65,535 counter semantics did not identify a dedicated reusable packet during this pass.

Accordingly this evidence keeps only the retention-specific interface analysis here.

If `computing-archaeology` later develops a broader Intel SSD SMART / PLI chronology, that technical-history material should be linked rather than duplicated.
