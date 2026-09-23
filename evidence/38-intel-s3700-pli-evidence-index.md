# Case 38 Evidence Index — Intel DC S3700/S3500 PLI Self-Test and Readiness

## Status

**Case 38 maturity: `grounded`**

Canonical case:

- [`../cases/38-intel-dc-s3700-pli-self-test-validation.md`](../cases/38-intel-dc-s3700-pli-self-test-validation.md)

This index groups the Case 38 evidence slices by the distinct retention question they answer. It is navigation, not a new maturity promotion.

The case now has a layered evidence chain:

```text
power-loss protection apparatus
    -> readiness self-test
    -> retained readiness/event evidence
    -> policy controlling test cadence
    -> operator-facing policy/action encoding
    -> safe degradation when readiness is insufficient
    -> wider system-stack power-cut validation
```

The important discipline is that each arrow is separately sourced. A capacitor, a self-test, a test result, a schedule, a management command, and a cache-authority decision are not interchangeable evidence classes.

---

## 1. Canonical bounded relation

### Case 38 — Intel DC S3700/S3500 PLI self-test validation

[`../cases/38-intel-dc-s3700-pli-self-test-validation.md`](../cases/38-intel-dc-s3700-pli-self-test-validation.md)

Core bounded claim:

> Intel's DC S3700/S3500 documentation treats power-loss protection as an apparatus whose future readiness is itself periodically tested and made visible through separate event/history and protection-health state; the manufacturer also distinguishes component/path self-test from broader power-loss validation.

Canonical state separation:

```text
unsafe-power-loss event history
    !=
PLI readiness state
    !=
self-test recency/history
    !=
test-cadence control
    !=
whole-device fault-validation evidence
```

Current maturity remains `grounded` because the manufacturer/interface evidence is strong while device-specific induced-failure traces, exact controller metadata recovery, and several state-transition details remain incomplete.

---

## 2. Evidence chain A — early named-product control surface and chronology

### `38-intel-s3700-2012-pli-self-test-control-surface-prior-art-deepening.md`

[`38-intel-s3700-2012-pli-self-test-control-surface-prior-art-deepening.md`](38-intel-s3700-2012-pli-self-test-control-surface-prior-art-deepening.md)

Question answered:

> How early can the named S3700 self-test / health / cadence control surface be directly grounded?

Contribution:

- moves the named-product documentary floor to the October-2012 S3700 specification;
- keeps Intel's internal June-2012 revision-history statement distinct from independently dated public disclosure;
- establishes separate `AEh` unsafe-power-loss history and `AFh` PLI-health/test state;
- establishes vendor SCT Feature Control `D000h` for the power-safe-write-cache capacitor-test interval;
- prevents the later 2014 explanatory PLI brief from being silently treated as the first evidence for the control surface.

Boundary:

```text
feature existed in inspected product documentation
    !=
complete internal firmware behavior known
```

---

## 3. Evidence chain B — maintenance-policy persistence horizon

### `38-intel-s3700-sct-test-cadence-persistence-boundary-deepening.md`

[`38-intel-s3700-sct-test-cadence-persistence-boundary-deepening.md`](38-intel-s3700-sct-test-cadence-persistence-boundary-deepening.md)

Question answered:

> What does the period SCT Feature Control envelope let us say about current versus preserved maintenance-policy state around vendor feature `D000h`?

Contribution:

- distinguishes current feature state from the last nonvolatile feature state;
- distinguishes setting content from choosing its persistence horizon;
- uses period SCT Feature Control semantics as a protocol-level witness;
- explicitly refuses to upgrade generic SCT persistence capability into a claim that S3700 `D000h` was experimentally shown to survive a power cycle.

Core relation:

```text
maintenance-policy value
    !=
maintenance-policy persistence horizon

current feature state
    !=
last nonvolatile feature state
```

Remaining debt after this slice:

- actual D000h option response;
- device transcript across soft reset, hard reset, and full power cycle;
- exact storage embodiment if a preserved setting is accepted.

---

## 4. Evidence chain C — management property packs policy and immediate action

### `38-intel-dct-2015-pli-interval-immediate-trigger-boundary-deepening.md`

[`38-intel-dct-2015-pli-interval-immediate-trigger-boundary-deepening.md`](38-intel-dct-2015-pli-interval-immediate-trigger-boundary-deepening.md)

Question answered:

> Does Intel's operator-facing `PLITestTimeInterval` property encode only future cadence, or does the same setting also carry an immediate-test semantic?

Contribution:

- uses Intel's September-2015 DCT 2.3.x manufacturer document for the S3700/S3500 management surface;
- shows `PLITestTimeInterval=(0-6)`;
- shows values `0` and `1` both correspond to a 0-minute interval while differing on `no immediate test` versus `do immediate test`;
- shows values `2` through `6` pair nonzero future intervals with `do immediate test`;
- uses the Intel-hosted August-2019 DCT guide as later first-party continuity/custody corroboration;
- separates the DCT high-level property from the lower-level SCT persistence-option dimension.

Core relation:

```text
maintenance cadence
    !=
immediate maintenance-action request

one management property
    can encode both
```

Control-plane boundary:

```text
low-level SCT feature-state / option dimensions
    !=
operator-visible DCT property dimensions
```

Important non-claim:

```text
DCT set accepted
    !=
test completed
    !=
test passed
    !=
AFh durably updated
```

This is the newest Case 38 slice.

---

## 5. Evidence chain D — negative readiness and write-cache authority

### `38-s3700-2013-ocp-2023-pli-failure-write-cache-authority-deepening.md`

[`38-s3700-2013-ocp-2023-pli-failure-write-cache-authority-deepening.md`](38-s3700-2013-ocp-2023-pli-failure-write-cache-authority-deepening.md)

Question answered:

> What changes operationally when readiness evidence becomes negative or insufficient?

Contribution:

- keeps Intel's 2012 manufacturer-primary surfaces separate: AFh health state, write-cache Feature Control, and D000h test cadence;
- records a January-2013 contemporary secondary S3700 report that capacitor failure/degradation triggers a SMART event and cache disablement;
- uses the later OCP 2023 datacenter device requirement to make an explicit safe-degradation topology visible;
- does not claim the OCP rule descended from S3700 or that the later institutional rule proves Intel's exact firmware state machine.

Functional reconstruction:

```text
insufficient PLP readiness
    -> durability-dependent volatile-cache mode becomes inadmissible
```

Boundary:

```text
negative readiness evidence
    !=
payload already lost

mode disabled for safety
    !=
automatic proof of the exact historical S3700 transition sequence
```

---

## 6. Evidence chain E — independent named-product system-stack power-cut witness

### `38-intel-s3500-2014-independent-power-cut-stack-validation-deepening.md`

[`38-intel-s3500-2014-independent-power-cut-stack-validation-deepening.md`](38-intel-s3500-2014-independent-power-cut-stack-validation-deepening.md)

Question answered:

> Is there an independent named-product power-cut witness adjacent to Intel's own PLI validation description?

Contribution:

- anchors the S3500's enhanced power-loss protection and capacitor self-test through Intel product documentation;
- adds a December-2014 independent system-stack test report using an Intel DC S3500 in a Dell R420 / H710p / CentOS 6.5 / XFS environment;
- records hard-power-cut testing of `fsync` and PostgreSQL paths with post-reboot verification;
- preserves the causal boundary that this is a **system-stack observation**, not isolated SSD certification.

Core limit:

```text
repeated successful system-stack power cuts
    !=
complete SSD-only failure-envelope coverage
```

and:

```text
filesystem / database recovery success
    !=
visibility into every hidden FTL or controller-metadata transition
```

---

## 7. Cross-slice state taxonomy

The Case 38 evidence is easiest to navigate if the state classes remain typed:

| State / relation | Example surface | Meaning | Not equivalent to |
| --- | --- | --- | --- |
| user payload | NAND / host-visible LBAs | data being protected | readiness evidence |
| volatile write state | controller temporary buffers | data dependent on PLP during outage | durable NAND state |
| protection apparatus | capacitors + switching + firmware path | mechanism intended to complete emergency transfer | proof it is currently healthy |
| unsafe-shutdown history | SMART `AEh` | cumulative event history | PLI health |
| readiness/test state | SMART `AFh` | latest discharge result, recency, lifetime test count | future outage guarantee |
| cadence policy | SCT `D000h` / DCT `PLITestTimeInterval` | when future testing is intended | test execution |
| immediate-test semantic | DCT value meaning | maintenance action associated with setting | passing result |
| persistence policy | SCT Feature Control option semantics | state lifetime across reset/power boundary | feature value itself |
| cache authority | write-cache control / safe-degradation rule | whether volatile caching is admissible | payload durability itself |
| validation evidence | Intel validation method / independent tests | observed behavior under fault campaigns | universal correctness proof |

This table is an engineering synthesis. Intel does not publish this exact taxonomy.

---

## 8. Historical record / engineering reconstruction / analogy discipline

### Historical record

Use source vocabulary and bounded dates:

- Intel S3700 product specification, 2012;
- period S3700 reporting, 2013, only where explicitly labeled secondary;
- Intel PLI explanatory material and independent S3500 system-stack testing, 2014;
- Intel S3700 product/DCT documentation, 2015;
- later Intel DCT continuity, 2019;
- OCP datacenter requirement, 2023, only as a later institutional comparison.

Do not collapse those dates into one timeless “Intel PLI design.”

### Engineering reconstruction

Repository terms such as:

- `retention-infrastructure readiness`;
- `maintenance cadence policy`;
- `safe degradation`;
- `write-cache authority`;
- `declarative policy` versus `imperative maintenance transition`;

are analytical labels for relations reconstructed from the sources. They are not historical Intel terminology.

### Functional analogy

Case 38 can be compared functionally with:

- Case 03 DRAM refresh scheduling/execution;
- Case 15 SSD 320 emergency-retention versus restart/recovery context;
- Case 88 RAID5 PPL durability obligations;
- Synthesis 26 maintenance restart/progress policy.

These comparisons do **not** establish genealogy.

### Philosophical interpretation

A bounded interpretation is that a technical system may retain not only payload but also:

- evidence that a protection mechanism remains capable;
- policy about when that evidence should be refreshed;
- control state determining whether a risky operating mode is still permitted.

That interpretation must never replace the concrete product/interface claims above.

---

## 9. What is closed versus still open

Closed or substantially bounded:

```text
2012 named S3700 self-test / AEh / AFh / D000h surface
2014-era Intel explanation of periodic PLI verification
period system-stack named-product power-cut witness
protocol-level current-vs-preserved Feature Control distinction
2015 operator-facing PLITestTimeInterval encoding
policy-vs-immediate-test semantic distinction
later safe-degradation comparison
```

Still open:

```text
manufacturer-primary S3700 proof of automatic cache disable on AFh failure
raw S3700/S3500 transcript across induced PLI failure and recovery
exact DCT -> SCT D000h state/option mapping
device-specific D000h reset/power-cycle behavior
immediate-test completion/return ordering
AFh publication atomicity after an immediate test
provenance of periodic vs manual vs configuration-triggered tests
exact cache-transition atomicity and re-enable semantics
controlled component-only power-waveform fault injection
hidden controller/FTL metadata recovery coverage
pre-2023 institutional lineage if historically important
```

These open items are narrower than the already-grounded case and should be selected one at a time.

---

## 10. Related-repository boundary

Before the newest DCT slice, `tmzncty/computing-archaeology` was searched for both `S3700` and `PLITestTimeInterval`; no reusable packet was found.

Accordingly Case 38 remains responsible only for the retention-specific control/evidence questions above. A broader history of Intel SSD management tooling, SCT implementations, SATA enterprise-device genealogy, or Intel product-family evolution should be developed or reused from the archaeology repository rather than duplicated here.

---

## 11. Recommended next slice

The highest-value next Case 38 slice is now:

> **Find a raw command trace, source implementation, firmware-adjacent document, or controlled device experiment that connects DCT `PLITestTimeInterval=(0-6)` to the underlying SCT `D000h` State/Option fields and then crosses a reset/power-cycle boundary.**

That would close the current gap between:

```text
operator-facing management semantics
    -> ?
raw protocol request
    -> ?
device-specific persistence behavior
```

Until such evidence exists, Case 38 should remain **`grounded`** rather than being promoted.
