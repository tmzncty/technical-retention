# Case 38 Deepening — Intel S3700 PLI Self-Test Cadence Persistence Boundary

## Status

**`bounded deepening complete`**

This note deepens [`../cases/38-intel-dc-s3700-pli-self-test-validation.md`](../cases/38-intel-dc-s3700-pli-self-test-validation.md) around one deliberately narrow question:

> Intel documents a host-configurable interval for the DC S3700 power-safe-write-cache capacitor self-test. Does the public product record also establish that the selected interval survives a reset or full power cycle?

The bounded answer is **no public product-specific persistence proof has been found in the inspected material**.

That is not the same claim as saying the interval is volatile. The inspected ATA/SCT command model contains an explicit per-feature persistence mechanism, while Intel's S3700 product specification identifies the capacitor-test interval as a vendor-specific SCT Feature Control feature. What remains missing is a product-specific statement or trace binding Intel feature `D000h` to one particular persistence option across reset classes.

This distinction closes a small but important seam in Case 38:

```text
host can configure maintenance cadence
    !=
configured cadence is proven restart-persistent
```

No maturity promotion follows. Case 38 remains `grounded`.

---

## Related-repository check

Before writing this slice, `tmzncty/computing-archaeology` was searched for the S3700 `D000h` capacitor-test interval and SCT Feature Control persistence semantics. No dedicated reusable packet surfaced in the current search surface.

Accordingly, this note does **not** reconstruct the broader history of SMART Command Transport, ATA software-settings preservation, SATA reset classes, or vendor-specific enterprise-SSD management. Those belong in the technical-history repository if developed later.

The present record keeps only the retention-specific boundary:

```text
maintenance policy can be set
    !=
maintenance policy is known to survive loss of volatile controller state
```

---

## Sources inspected

### Primary product source

**Intel, _Intel Solid-State Drive DC S3700 Product Specification_, order 328171-001US, October 2012.**

Intel-hosted copy:

- <https://download.intel.com/newsroom/kits/ssd/pdfs/Intel_SSD_DC_S3700_Product_Specification.pdf>

Relevant printed pages / sections:

- printed p. 24, §5.6 `SMART Command Transport (SCT)`;
- printed p. 25, §5.12 `Software Settings Preservation`.

The directly inspected product specification says that the S3700 supports SCT Feature Control codes `0001h`, `0002h`, `0003h`, and vendor feature `D000h`, described as `Power Safe Write Cache capacitor test interval`. The same specification separately states that the drive supports the SET FEATURES parameter for enabling or disabling Software Settings Preservation.

### Primary standards record

**Technical Committee T13, _ATA/ATAPI Command Set - 3 (ACS-3)_, T13/2161-D Revision 5, 28 October 2013.**

T13 document index:

- <https://t13.org/docsearch>

A directly searchable mirror of the same d2161r5 working draft used for clause inspection:

- <https://people.freebsd.org/~imp/asiabsdcon2015/works/d2161r5-ATAATAPI_Command_Set_-_3.pdf>

Relevant clauses:

- §8.3.4.1, SCT Feature Control command and feature-code table;
- §8.3.4.2, Options Flags;
- §8.3.4.3, SCT Feature Control command status response.

ACS-3 is a **later standards witness** than the October-2012 Intel product specification. It is used here to establish the generic SCT control semantics visible by late 2013, not to claim that every detail of ACS-3 was necessarily implemented identically in the S3700's June/October-2012 firmware.

---

## Historical / source record

### H/P — Intel exposes a named maintenance-policy control

The October-2012 S3700 specification lists `D000h` under SCT Feature Control and labels it:

`Power Safe Write Cache capacitor test interval`

The same section distinguishes it from standard feature codes for write cache, write-cache reordering, and temperature-logging interval, and from other Intel-specific power/thermal governor controls.

For Case 38 this directly establishes a named product relation:

```text
PLI capacitor self-test
    -> host-visible SCT control
    -> configurable test interval
```

This is **maintenance-policy state**: it controls how often a future readiness test should occur. It is not itself a self-test result, a power-loss event counter, or the payload protected by PLI.

### H/P — Intel does not state the D000h reset/power-cycle rule in the inspected product section

The same S3700 specification says separately that the drive supports Software Settings Preservation through SET FEATURES.

That statement is useful but insufficient to bind `D000h` to a persistence rule. In the inspected product text Intel does not say:

- that `D000h` participates in Software Settings Preservation;
- that a D000h-selected interval is retained across COMRESET;
- that it is retained across hardware reset;
- that it is retained across power-on reset;
- that it returns to a default after any of those events;
- or that its persistence is controlled by a named SCT option flag.

Therefore the product contract inspected here supports:

```text
D000h cadence is configurable
```

but does not by itself support:

```text
D000h cadence survives reset/power cycle
```

or the opposite claim.

### H/P — ACS-3 gives SCT Feature Control an explicit per-feature persistence semantic

ACS-3 §8.3.4 defines SCT Feature Control with a feature code, a state, and associated option flags.

Its feature-code table assigns `D000h..FFFFh` to the **Vendor Specific** range. Thus Intel's product-specific `D000h` sits exactly in a range for which the standard does not define the semantic meaning of the feature state itself.

At the same time, §8.3.4.2 defines an option flag associated with each Feature Code: bit 0, `FEATURE STATE VOLATILITY`.

The standard distinguishes two policies:

- bit 0 clear: after a hardware reset, the associated feature state reverts to the default or last non-volatile setting;
- bit 0 set: the associated feature state is preserved across all resets, explicitly including power-on resets.

ACS-3 also defines a Feature Control status operation that can return the option flags associated with a feature code.

The important structural point is therefore:

```text
feature state
    + persistence option
```

rather than:

```text
feature state automatically implies one reset behavior
```

### H/P — the generic persistence mechanism does not prove Intel's D000h choice

The standards record supplies a mechanism by which an SCT feature can have defined reset persistence. Intel supplies the vendor-specific feature code and maintenance meaning.

But the two records do not contain the missing binding:

```text
Intel D000h
    -> FEATURE STATE VOLATILITY = ?
```

The public product specification inspected here does not publish that option value or an equivalent reset/power-cycle guarantee for the capacitor-test interval.

Therefore the strongest safe source-level statement is:

```text
generic SCT machinery can express reset persistence
    !=
public evidence that S3700 D000h uses a particular persistence mode
```

### H/P — Software Settings Preservation is a separate advertised capability, not a wildcard proof

Intel's §5.12 statement that the S3700 supports Software Settings Preservation shows that the product participates in an ATA/SATA ecosystem where some host-programmable settings have explicit reset-survival rules.

It does **not** license the inference:

```text
S3700 supports Software Settings Preservation
    -> every vendor SCT feature is preserved
```

The inspected Intel text does not make that universal claim, and ACS-3's SCT Feature Control already has its own per-feature option mechanism.

This distinction prevents two different control surfaces from being collapsed merely because both concern settings and resets.

---

## Engineering reconstruction

Everything in this section is repository analysis, not historical Intel/T13 vocabulary unless quoted above.

### E/R — maintenance policy is a third state layer beside execution and result

Existing Case 38 evidence already separates the PLI mechanism, self-test execution, and retained self-test result/history. The D000h persistence question makes another layer explicit:

```text
maintenance policy state
    !=
maintenance execution state
    !=
maintenance-result / health state
```

For this named product:

```text
D000h-selected interval
    -> maintenance policy state

capacitor test currently running
    -> maintenance execution state

AFh latest-result / recency / lifetime-count fields
    -> maintenance-result/history state
```

Losing or resetting one layer does not logically imply loss of the others.

### E/R — current policy and durable policy are different claims

A host may successfully set a non-default cadence and read it back while the controller is running. That only establishes current policy materialization.

The persistence claim requires an additional boundary:

```text
host writes non-default cadence
    -> device accepts current policy
    -> reset / power-cycle boundary
    -> policy reconstructed or reverted
    -> host re-observes resulting policy
```

So:

```text
configured now
    !=
retained for the next controller epoch
```

The repository term **maintenance-policy persistence horizon** is useful for this distinction. It is not an Intel or T13 historical term.

### E/R — a persistent maintenance mechanism can still depend on a non-persistent schedule

PLI hardware, capacitor health records, and the future emergency-write path may remain present even if a host-selected test cadence returns to a default after reset.

Conversely, a persistent cadence would not prove that the next self-test actually ran, passed, or covered the whole future failure path.

Thus:

```text
policy persistence
    !=
policy execution
    !=
execution success
    !=
protection-path qualification
```

This is the principal anti-collapse result of the slice.

### E/R — reset class is part of the question

A rigorous test should not use the single word `restart` as if all transitions were equivalent.

At minimum, evidence should distinguish:

- software reset where applicable;
- SATA link / COMRESET behavior where applicable;
- hardware reset semantics;
- full removal and restoration of device power.

The standards language itself distinguishes reset classes. A product experiment that tests only one transition cannot automatically prove behavior across the others.

---

## Proposed fault / persistence trace

This is a **future experiment design**, not an observed S3700 result.

Use a real S3700 with a controllable host and power path. Select a deliberately non-default D000h interval far enough from the documented default to make reversion obvious.

For each transition class:

1. read the current D000h feature state and, where exposed, its SCT option flags;
2. set a non-default capacitor-test interval;
3. read back the state before reset;
4. record AFh `Minutes since last test` and lifetime test count as independent execution/result witnesses;
5. apply exactly one reset or power transition;
6. after re-enumeration, read D000h state and option flags again;
7. wait long enough to observe whether the next self-test actually follows the retained, reverted, or vendor-specific cadence;
8. read AFh again so `policy readback` and `test actually occurred` remain separate observations.

A useful matrix is:

| Cut / transition | D000h before | D000h after | option flag after | next observed test timing | interpretation |
| --- | --- | --- | --- | --- | --- |
| no reset control | non-default | ? | ? | ? | control |
| soft reset | non-default | ? | ? | ? | bounded reset result |
| COMRESET / link reset | non-default | ? | ? | ? | bounded reset result |
| hardware reset if independently controllable | non-default | ? | ? | ? | bounded reset result |
| full power cycle | non-default | ? | ? | ? | power-epoch result |

The experiment should not infer persistence solely from AFh test timing if D000h can be read directly, nor infer execution solely from a retained policy value.

---

## Functional comparisons

These are **functional analogies only**. They are not genealogy claims.

### Case 116 — HDFS maintenance state

Case 116 distinguishes externally retained maintenance intent from a controller's current in-memory materialization of that intent.

The analogous shape here is:

```text
maintenance obligation / policy
    !=
current controller materialization
```

HDFS and an enterprise SSD are historically and architecturally unrelated at this layer; the comparison is only about the control-state distinction.

### Case 101 — SCSI Background Medium Scan

Case 101 shows that a host-visible maintenance observable may be scoped to a power epoch and may not uniquely prove a prior maintenance history.

The bounded analogy is:

```text
maintenance state visible now
    !=
proof of what survived the preceding power boundary
```

Again, this is not evidence that Intel D000h has the same persistence semantics as SCSI BMS.

---

## Philosophical interpretation

This subsection is interpretation, not historical source language.

A system that depends on periodic validation has more to retain than payload bits and more to retain than the latest validation result. It may also need to retain the **policy that causes future validation to happen**.

That suggests a layered retention question:

```text
retain payload
    + retain evidence that the protection path is healthy
    + retain enough maintenance policy to keep producing new evidence
```

The S3700 source set is valuable precisely because it prevents that observation from turning into an unsupported product claim. The product publicly exposes the schedule control, while the public documents inspected here stop short of proving exactly how that schedule crosses reset and power boundaries.

The epistemic gap is itself useful evidence: **configurability is not durability**.

---

## Explicit non-claims

This packet does **not** claim that:

1. S3700 D000h is volatile.
2. S3700 D000h is non-volatile.
3. D000h always reverts to the default after a reset.
4. D000h always survives a power cycle.
5. Software Settings Preservation necessarily covers D000h.
6. Software Settings Preservation necessarily excludes D000h.
7. ACS-3 Revision 5 exactly describes every behavior of 2012 S3700 firmware.
8. Intel implemented every ACS-3 option exactly as later standardized.
9. Setting an SCT feature proves that the requested maintenance action later executed.
10. Reading the same value after a reset proves that the value was stored in NAND rather than reconstructed from another source.
11. AFh health telemetry and D000h policy have the same persistence horizon.
12. AFh lifetime test count is reset-volatile or reset-persistent beyond what Intel explicitly documents.
13. A persistent cadence proves a passing capacitor self-test.
14. A passing capacitor self-test proves whole-device power-loss correctness.
15. A cadence reset would imply loss of user data.
16. A cadence reset would imply PLI was disabled.
17. A reset that preserves D000h implies a full power removal will preserve it.
18. A full-power-cycle result automatically characterizes every S3700 firmware revision.
19. the T13 `FEATURE STATE VOLATILITY` name was Intel's product documentation vocabulary.
20. the project term `maintenance-policy persistence horizon` is historical terminology.
21. Case 101 or Case 116 is a historical ancestor of this Intel behavior.
22. lack of a public persistence statement means Intel firmware lacks an internal persistent policy.
23. a host tool's cached display is sufficient evidence of device-side persistence.
24. a single post-reset readback is sufficient without controlling the reset class and pre-reset state.

---

## What this closes

Before this slice, Case 38 already grounded:

- a named PLI capacitor self-test;
- retained health/result/recency counters;
- a host-configurable test cadence;
- a wider distinction between readiness testing and full power-loss validation;
- later evidence about degraded PLI and write-cache authority.

This slice closes the narrower documentary question:

> Does `host-configurable PLI self-test cadence` itself prove `restart-persistent maintenance policy`?

**No.** The named S3700 source establishes the configurable D000h cadence, while the ATA/SCT standard exposes a separate feature-state persistence mechanism. The inspected public product record does not publish the missing D000h-to-persistence binding.

The remaining high-value debt is therefore behavioral rather than terminological:

```text
non-default D000h
    -> controlled reset / power-cycle
    -> D000h readback + option-flag readback
    -> actual next-test timing
    -> AFh result/history observation
```

That trace could turn today's source-level boundary into a measured product result.

---

## Repository classification

- **Case:** 38
- **Case maturity:** remains `grounded`
- **Slice type:** source / interface-semantics deepening
- **Historical record:** Intel S3700 product specification + T13 ACS-3 SCT semantics
- **Engineering reconstruction:** policy state vs execution state vs result state; maintenance-policy persistence horizon
- **Functional analogy:** Case 116 and Case 101 only
- **Philosophical interpretation:** maintenance policy may itself be retention-relevant
- **No promotion:** yes
- **No CASE_INDEX rewrite:** yes
