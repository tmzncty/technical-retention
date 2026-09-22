# Case 38 evidence deepening — Intel DC S3700 `D000h` maintenance-policy persistence boundary

## Research question

Case 38 already establishes that the Intel SSD DC S3700 exposes an SCT Feature Control code `D000h` for the **Power Safe Write Cache capacitor test interval**, that capacitor-health telemetry and write-cache authority are separate surfaces, and that a partial-discharge capacitor self-test is not equivalent to full hot-unplug fault validation.

The remaining question addressed here is narrower:

> What can the surviving public interface evidence prove about persistence of the **configured self-test interval itself** across reset and power loss?

This is a second-order retention question. The interval does not retain user payload. It is policy state that determines when a future check of retention infrastructure is scheduled.

This packet deliberately does **not** attempt to reconstruct the entire S3700 firmware state machine, and it does not claim that a successful capacitor self-test proves correct emergency persistence under every power-failure waveform.

---

## Bottom line

The evidence supports a stronger and more precise statement than either of the two tempting extremes.

The weak extreme would be:

```text
D000h persistence is entirely unknowable.
```

The overclaiming extreme would be:

```text
Because D000h is an SCT Feature Control setting,
its configured interval necessarily survives reset and power loss.
```

Neither is justified.

What is directly supportable is:

```text
Intel S3700 exposes D000h through SCT Feature Control
    +
SCT Feature Control has an explicit persistent/non-volatile option
    +
SCT Feature Control can return per-feature option flags
    +
Intel's public S3700 product specification does not disclose
D000h-specific option flags or a D000h persistence default

therefore

protocol-level persistence machinery is established
    !=
product-specific D000h persistence is established
```

In other words, the command family already knows how to distinguish **volatile policy state** from **policy state preserved through power/reset events**. The unresolved debt is now product-specific: whether S3700 `D000h` accepts/supports the persistent option, what its default is, and what a real drive reports through the option-flag query.

---

# 1. Historical record

## 1.1 Intel's October 2012 S3700 product specification exposes `D000h`

Intel's first-party *Intel Solid-State Drive DC S3700 Product Specification*, order number `328171-001US`, is dated **October 2012**. Its cover states support for ATA8-ACS2 including SCT. Its revision history identifies **June 2012** as the initial release of revision 001; this packet does not infer that every line visible in the October copy was necessarily unchanged in the June release.

In section 5.6, Intel describes SMART Command Transport and says the S3700 supports standard SCT actions including Feature Control. The feature list includes:

- `0001h` — write cache;
- `0002h` — write-cache reordering;
- `0003h` — time interval for temperature logging;
- `D000h` — **Power Safe Write Cache capacitor test interval**;
- additional `D001h`–`D004h` vendor controls for power/thermal governor behavior.

Source:

- Intel, *Intel Solid-State Drive DC S3700 Product Specification*, October 2012, order 328171-001US, §5.6, pp. 23–24 of the PDF.
- https://download.intel.com/newsroom/kits/ssd/pdfs/Intel_SSD_DC_S3700_Product_Specification.pdf

### What this proves

It directly proves that Intel exposed the capacitor-test interval as a host-visible SCT Feature Control code on this named product family.

It does **not** by itself prove:

- the default interval value;
- the legal state-value range;
- whether the setting is persistent by default;
- whether the persistent option is accepted for this vendor-specific feature;
- whether an in-progress capacitor test survives reset;
- whether test results are retained in the same state object as the interval;
- firmware-update persistence.

---

## 1.2 The S3700 separately advertises Software Settings Preservation

The same Intel product specification has a separate §5.12 titled **Software Settings Preservation** and states that the S3700 supports the SET FEATURES parameter used to enable/disable preservation of software settings.

Source:

- Intel S3700 Product Specification, October 2012, §5.12, p. 25 of the PDF.
- same first-party PDF above.

This is useful evidence about the product's broader command-set capabilities, but it is **not** a shortcut for proving `D000h` persistence.

Why not?

Because `D000h` is documented by Intel under **SCT Feature Control**, whereas Software Settings Preservation is a distinct ATA feature surface with its own defined preservation set. The public S3700 text checked here does not state that `D000h` is governed by SSP.

Therefore:

```text
S3700 supports Software Settings Preservation
    !=
D000h is preserved by SSP
```

That distinction matters because otherwise two separate protocol mechanisms would be silently collapsed into one.

---

## 1.3 SCT Feature Control itself carries a persistence selector

A contemporaneous ATA command-set working draft provides the protocol-level rule that makes the S3700 omission meaningful rather than merely mysterious.

`T13/2161-D Revision 1b`, **Working Draft ATA/ATAPI Command Set - 3 (ACS-3)**, dated **17 October 2011**, defines SCT Feature Control in §8.3.4.

The command uses:

- Action Code `0004h` for SCT Feature Control;
- Function Code `0001h` to set feature state;
- Function Code `0002h` to return current feature state;
- Function Code `0003h` to return **feature option flags**.

For a Set State request, Word 4 is `Option Flags`. Bit 0 has explicit persistence semantics:

- bit 0 = 1: the requested feature state change is preserved during power/reset events;
- bit 0 = 0: the requested state is volatile; after hard reset the device returns to the default or last non-volatile setting.

The same draft defines a response path for returning the option flags.

Document identity / public copy consulted:

- T13/2161-D Revision 1b, *Working Draft ATA/ATAPI Command Set - 3 (ACS-3)*, 17 October 2011, §8.3.4, Tables 170–172.
- Public copy: https://nevar.pl/pliki/ATA8-ACS-3.pdf

A separately indexed public transcription of the same draft also exposes the same §8.3.4 wording and table numbers.

### Why the chronology matters

The SCT persistence distinction predates the October 2012 S3700 product specification used here.

That supports this bounded historical statement:

```text
By the time Intel documented S3700 D000h,
SCT Feature Control already had a generic volatile/non-volatile state model.
```

It does **not** prove Intel implemented every optional semantic for every vendor-specific code.

---

## 1.4 Later implementations confirm the persistence bit was not merely editorial wording

Later enterprise-drive manuals reproduce the same SCT Feature Control model: a set operation can request volatile or power-cycle-preserved state, and the device can expose option flags. Modern `smartctl` likewise presents SCT controls with an explicit persistent option (`p`) for standardized feature codes such as SCT temperature interval and error-recovery control.

These later materials are not used to backdate S3700 behavior. They are only corroboration that the SCT persistence distinction was an operational interface concept, not just an interpretive gloss invented for this repository.

Examples:

- smartmontools `smartctl(8)` documentation: SCT temperature interval can be made persistent; otherwise it reverts to the last non-volatile/default setting on reset.
- later Ultrastar SATA manuals reproduce the SCT Feature Control Option Flags bit semantics and the `Return feature option flags` function.

These are secondary / later implementation witnesses, not S3700 product evidence.

---

# 2. The central evidence boundary

## 2.1 The protocol envelope is stronger than the current product-specific proof

The evidence now separates three levels:

```text
Level A — protocol capability
SCT Feature Control defines persistent vs volatile state
and a way to query option flags.

Level B — named-product feature exposure
Intel S3700 exposes vendor feature D000h through SCT Feature Control.

Level C — named-feature persistence contract
Does S3700 D000h specifically accept/support persistence,
what does it report, and what is the default?
```

Levels A and B are directly established.

Level C remains open.

This is more informative than saying merely “the manual does not say.” The standard tells us exactly **which missing observation** would close the gap.

---

## 2.2 `Return feature option flags` is the missing bridge

Because SCT Feature Control includes Function Code `0003h` for returning a feature's option flags, a real S3700 can in principle provide product-specific evidence that no surviving product manual currently provides in the checked corpus.

The most valuable next artifact would therefore be one of:

1. an Intel engineering/interface document showing `D000h` option flags;
2. an SCT transcript from an S3700 returning `D000h` option flags;
3. a controlled set/reset/power-cycle experiment on a preserved S3700;
4. source code from an Intel maintenance tool that explicitly sets/queries `D000h` persistence.

This narrows the prior debt substantially.

---

# 3. Engineering reconstruction

This section is reconstruction, not a claim about undisclosed Intel firmware internals.

## 3.1 The interval is maintenance-policy state

`D000h` is best modeled as a configuration value controlling **when a future capacitor test is requested or scheduled**, not as the capacitor-health result itself.

A useful decomposition is:

```text
configured test interval
    -> policy for when a test should occur

current self-test execution state
    -> whether a test is currently pending/running

self-test result / health telemetry
    -> evidence produced by the test

current write-cache authority
    -> whether volatile buffering is presently permitted

physical PLI capability
    -> actual stored energy + discharge path + firmware behavior
```

These states may interact, but they are not interchangeable.

Consequently:

```text
interval retained
    !=
self-test progress retained
    !=
last result retained
    !=
PLI currently healthy
    !=
emergency flush guaranteed
```

---

## 3.2 Volatile policy and durable policy imply different restart behavior

The generic SCT rule creates two possible policy-state lifetimes.

### Volatile setting

A host changes the interval without the persistent option.

Then a hard reset can cause the drive to return to:

- the manufacturer/default interval, or
- the last non-volatile interval.

The configured schedule seen before reset therefore need not be the schedule used after reset.

### Non-volatile setting

If the feature accepts the persistent option and the host sets it persistently, the protocol contract says the state change is preserved through power/reset events.

That would make the interval a genuine retained control variable.

But this remains conditional for S3700 `D000h` until the feature-specific support is observed.

---

## 3.3 The retained rule can outlive the maintenance event it schedules

If `D000h` supports non-volatile configuration, the system contains at least two temporal objects:

```text
retained scheduling rule
        ↓
future self-test invocation
        ↓
transient execution
        ↓
health observation / policy consequence
```

This is a useful instance of **retention infrastructure retaining its own policy**.

The user payload may survive because of PLI; PLI may be periodically checked; and the rule that determines the check cadence may itself have a persistence contract.

That is a second-order retention structure, but it should not be elevated into a claim about the undocumented implementation.

---

# 4. Cross-case comparison: Case 135 eMMC `PERIODIC_WAKEUP`

This comparison is functional analogy, not genealogy.

Case 135 contains a stronger named-product persistence statement for a different maintenance-control surface. A Micron eMMC 4.51 component exposes `PERIODIC_WAKEUP[131]` with an `R/W/E` access class whose datasheet defines persistence through power cycle, `RST_n`, and `CMD0` reset.

The comparison is therefore:

```text
Case 135 eMMC
named maintenance-policy field
    +
named-product persistence class explicitly documented

Case 38 S3700
named maintenance-policy field
    +
generic protocol persistence mechanism explicitly documented
    +
product-specific D000h persistence option not yet disclosed
```

This difference is evidentiary, not a quality ranking.

It shows why this repository should keep asking **where the persistence contract is actually specified** rather than inferring persistence from the existence of a configuration field.

Related packet:

- `evidence/135-micron-2013-2014-emmc451-rtc-periodic-wakeup-product-deepening.md`

---

# 5. Relationship to Software Settings Preservation

The S3700 product specification places SCT Feature Control and Software Settings Preservation in separate sections.

The safe interpretation is:

```text
SCT Feature Control persistent Option Flag
    = persistence semantic inside SCT Feature Control

ATA Software Settings Preservation
    = separate command-set preservation mechanism
```

Until a standard clause or Intel document explicitly joins them for `D000h`, this repository should not use SSP as evidence for the `D000h` lifetime.

This is especially important because the word **preservation** appears in both contexts but does not make the scopes identical.

---

# 6. What a decisive S3700 experiment should record

No such experiment was performed for this packet. The following is a proposed evidence-closure procedure.

## 6.1 Preconditions

Record at minimum:

- exact SSD model and capacity;
- serial number, if publication policy permits;
- firmware revision;
- host SATA controller / HBA;
- whether commands are passed through directly or translated;
- current SMART `AFh` and `AEh` values;
- current SCT `D000h` state;
- `D000h` option flags, if query succeeds.

## 6.2 Volatile-path test

1. Query `D000h` current state.
2. Query `D000h` option flags.
3. Set a distinctive, valid non-default interval with Option Flag bit 0 cleared.
4. Re-read current state and preserve the raw SCT response.
5. Perform a hard reset under controlled conditions.
6. Re-read `D000h`.
7. Repeat with a full power cycle.

Expected question:

```text
Does D000h revert to default / previous non-volatile value
as generic SCT semantics predict for a volatile setting?
```

## 6.3 Persistent-path test

Only if the drive reports/accepts persistence for `D000h`:

1. set a second distinctive interval with Option Flag bit 0 set;
2. verify current state;
3. hard reset and re-read;
4. full power cycle and re-read;
5. restore the original interval.

The experiment should preserve raw command blocks and response words, not merely a human-readable utility summary.

## 6.4 Keep health/result state separate

Before and after each reset, separately read the relevant SMART telemetry.

This is necessary because a change in interval state must not be mistaken for a change in capacitor-health state.

## 6.5 Firmware-update test is a separate experiment

Nothing in the generic SCT power/reset persistence wording proves survival across firmware replacement or firmware-update migration.

Therefore firmware-update persistence must be treated as a separate, potentially destructive/irreversible experiment and should not be inferred from a successful power-cycle test.

---

# 7. Evidence-strength table

| Claim | Evidence strength | Reason |
|---|---|---|
| S3700 supports SCT Feature Control | High | first-party Intel product specification |
| S3700 exposes `D000h` as capacitor-test interval | High | first-party Intel product specification names code and function |
| SCT Feature Control has volatile vs persistent state semantics | High for protocol layer | contemporaneous T13 ACS-3 working draft |
| SCT provides a function to return feature option flags | High for protocol layer | contemporaneous T13 ACS-3 working draft |
| S3700 supports ATA Software Settings Preservation | High | first-party Intel product specification |
| SSP governs `D000h` | Unproven | no checked source links the two surfaces |
| S3700 `D000h` accepts persistent option | Unproven | no D000h-specific option-flag result found |
| S3700 `D000h` is persistent by default | Unproven | no default/persistence statement found |
| S3700 `D000h` is volatile by default | Unproven | absence of a persistence statement is not proof of volatility |
| `D000h` survives hard reset / power cycle in an actual drive | Open empirical question | protocol machinery exists, product-specific observation absent |
| in-progress self-test survives reset | Unproven | interval policy is not execution state |
| firmware update preserves interval | Unproven | power/reset contract does not imply firmware-migration contract |

---

# 8. Explicit non-claims

This packet does **not** claim any of the following:

1. `D000h` is persistent merely because it is an SCT Feature Control code.
2. `D000h` is volatile merely because Intel's product specification does not state its persistence policy.
3. Software Settings Preservation automatically includes SCT `D000h`.
4. A preserved interval means a capacitor test was actually run.
5. A preserved interval means a prior test result is preserved.
6. A preserved result means the capacitor is currently healthy.
7. A passing capacitor test guarantees all emergency writes complete under arbitrary power-loss waveforms.
8. The protocol's power/reset persistence contract includes firmware update.
9. Later Ultrastar implementation behavior proves S3700 behavior.
10. `smartctl` support for persistent standardized SCT settings proves support for Intel's vendor-specific code.
11. Case 135 eMMC and Case 38 S3700 share implementation ancestry.
12. A maintenance scheduler is equivalent to the maintenance operation it schedules.
13. A host-visible policy field is necessarily the firmware's only source of scheduling state.
14. `D000h` current value reveals an in-progress self-test state.
15. `D000h` option flags, even if observed, would by themselves prove every reset class behaves correctly without a fault test.

---

# 9. Historical record / engineering reconstruction / analogy / interpretation split

## Historical record

Directly grounded here:

- October 2012 Intel S3700 spec identifies SCT support and `D000h` capacitor-test interval;
- the same S3700 spec separately advertises Software Settings Preservation;
- October 2011 ACS-3 working draft defines SCT Feature Control's set/current/option-flags functions and volatile vs persistent Option Flag semantics.

## Engineering reconstruction

Repository-level model:

- `D000h` is maintenance-policy state distinct from health telemetry, execution progress, cache authority, and physical PLI capability;
- a product could therefore have retained policy while transient execution state is lost, or vice versa;
- a direct option-flag transcript plus reset experiment is the shortest path to closing the remaining product-specific gap.

## Functional analogy

- Case 135 eMMC `PERIODIC_WAKEUP` is another retained rule governing future maintenance opportunity;
- its product-level persistence class is explicitly documented, unlike the currently available S3700 `D000h` evidence.

## Philosophical interpretation

A retention system may need to retain not only payload and repair metadata, but also **rules governing when its own protective mechanisms are checked**.

That is useful as an interpretive pattern only after the device-specific evidence boundaries above remain visible.

---

# 10. Consequence for Case 38

The old open question can now be narrowed from:

```text
Does D000h persist across reset/power cycles?
```

into:

```text
Protocol layer:
    persistence option exists                    ESTABLISHED
    option-flags query exists                   ESTABLISHED

Named-product layer:
    S3700 D000h exists                          ESTABLISHED
    D000h option flags on actual S3700          OPEN
    D000h persistent-set acceptance             OPEN
    D000h default persistence policy            OPEN
    hard-reset/power-cycle observed behavior    OPEN
    firmware-update migration behavior          OPEN
```

This is a material improvement because it replaces a vague documentation absence with a concrete interface-level experiment and a sharply bounded product-specific evidence debt.

No Case 38 maturity promotion is justified by this packet alone.

---

# 11. Sources

## Primary / near-primary

1. **Intel**, *Intel Solid-State Drive DC S3700 Product Specification*, order 328171-001US, October 2012. Particularly §§5.6 and 5.12; revision history on p. 28.
   - https://download.intel.com/newsroom/kits/ssd/pdfs/Intel_SSD_DC_S3700_Product_Specification.pdf

2. **T13**, *Working Draft ATA/ATAPI Command Set - 3 (ACS-3)*, T13/2161-D Revision 1b, 17 October 2011. Particularly §8.3.4, Tables 170–172.
   - Public copy consulted: https://nevar.pl/pliki/ATA8-ACS-3.pdf
   - The Intel S3700 specification itself points readers to T13 for the ATA command-set standard family.

## Corroborating implementation / tooling evidence

3. **smartmontools**, `smartctl(8)` documentation. SCT controls expose persistent variants for standardized SCT settings and distinguish volatile from power-cycle-preserved values.
   - https://manpages.debian.org/buster/smartmontools/smartctl.8.en.html

4. Later Ultrastar SATA product manuals reproduce the SCT Feature Control `Option Flags` persistence semantics and `Return feature option flags` function. These are corroborating implementations, not S3700 evidence.

---

# 12. Follow-on work

Highest-value next steps, in order:

1. obtain an actual S3700 and capture raw SCT Feature Control Function `0003h` results for `D000h`;
2. test volatile vs persistent set behavior across hard reset and full power cycle;
3. search Intel SSD Data Center Tool / SSD Toolbox historical binaries, manuals, or source fragments for an explicit `D000h` implementation path;
4. search firmware release notes for reset/default changes affecting capacitor-test interval;
5. only then consider firmware-update migration testing;
6. keep `AFh`, `AEh`, write-cache authority, test interval, test execution, and emergency-flush validation as separate state/evidence lines.

The target for the next deepening should not be another generic statement that the S3700 has capacitor protection. The remaining question is now specific: **what does the named product report and preserve for the policy state that schedules its own PLI self-check?**
