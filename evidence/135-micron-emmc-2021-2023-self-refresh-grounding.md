# Evidence Record — Case 135: Micron Automotive eMMC Self-Refresh, 2021–2023

## Research slice

**Question:** In a shipped embedded eMMC integration, can retention renewal depend on retained/supplied time evidence, reset-bounded host participation, idle opportunity, error-threshold selection, and second-order maintenance statistics — and which claims remain ungrounded without controller internals or the full vendor note?

**Bounded object:** Armadillo-IoT Gateway G4 product documentation for its Micron eMMC self-refresh/data-retention feature, cross-checked against Micron's official TN-FC-60 catalog metadata.

**Repository-state check:** before opening this slice, the repository already had grounded Flash/SSD work on Correct-and-Refresh, Samsung 840 EVO periodic refresh, JEDEC SSD retention qualification, enterprise-SSD extended-shutdown maintenance, and maintenance-trigger/control-state/evidence syntheses. This record therefore does not reopen generic Flash refresh or SSD retention. Fresh `computing-archaeology` searches for `Micron eMMC` and `SET_TIME eMMC` returned no dedicated module to reuse.

## Source ledger

| Source | Date / version | Type | Use in this record | Limit |
| --- | --- | --- | --- | --- |
| Atmark Techno, Armadillo-IoT Gateway G4 Product Manual v1.0.0, §9.9 | 2021-12-09 | `H/P` contemporaneous product/integrator manual | product floor; trigger modes; reset/SET_TIME/idle/delay sequence; threshold selection; maintenance stats | not Micron silicon/firmware source code; does not prove invention priority |
| Atmark Techno, maintained Armadillo-IoT G4 manual | current maintained edition | `H/P` product documentation continuity | checks that the same bounded feature remains documented after section renumbering | later text must not be projected backward where v1.0.0 is silent |
| Micron official eMMC software/download page, TN-FC-60 metadata | 2023-04-11 | `H/P*` manufacturer-primary catalog metadata | independently confirms note title/date and automotive eMMC 5.1 refresh-feature scope | full TN body requires account/login and was not inspected here |

`P*` means primary metadata whose linked secured body was not directly inspected. It is not upgraded to clause-level evidence.

## Source A — Atmark Techno v1.0.0 product manual

### Publication floor

The versioned product manual identifies **Version 1.0.0** and **2021/12/09**. Its HTML edition has a dedicated **§9.9 eMMC data retention** section. This supplies a public product-integration floor no later than that manual release.

Accepted claim:

> By 9 December 2021, Atmark Techno publicly documented an automatic eMMC data-retention/self-refresh feature in the Armadillo-IoT Gateway G4 integration.

Rejected overclaim:

> 9 December 2021 is the invention or first-shipment date of Micron eMMC self refresh.

Nothing in the manual establishes that priority.

### Trigger modes and OTP policy

Section 9.9.3 says the automatic feature is called **self refresh** and that one of two trigger modes is chosen. It describes the setting as OTP and says the shipped Armadillo configuration uses the mode that compares an eMMC internal-register value with a value supplied by command and executes when at least one day has elapsed.

The two documented modes are:

1. execute after each reset;
2. compare internal-register and command-supplied values and execute once >=1 day has elapsed.

Accepted boundaries:

- `policy configuration != current maintenance execution`;
- `one-time trigger-mode configuration != one-time self-refresh execution`;
- `>=1 day eligibility != one-day data-loss deadline`.

### Reset → SET_TIME → idle → Delay 2 → self refresh

For mode 2, the manual lists the sequence explicitly:

1. host hardware/software reset;
2. issue **SET_TIME (CMD49)** within a configured `Delay 1`;
3. controller monitors bus activity;
4. after the bus becomes idle and `Delay 2` elapses, self refresh runs.

For Armadillo the displayed values are:

- RTC: ON;
- Delay 1: 60 seconds;
- Delay 2: 100 milliseconds.

This directly rejects several conflations:

```text
reset
    != SET_TIME delivery
    != elapsed-time eligibility
    != idle opportunity
    != maintenance start
    != maintenance completion
```

The source gives no basis for treating a normal boot as proof that all retention work finished.

### Selective error-threshold path

The same implementation section says self refresh is performed only for cells where ECC errors or similar errors exceed **threshold 2**.

Accepted claim:

> The documented policy is selective by local error evidence rather than an unconditional rewrite of the complete medium.

Stop conditions:

- do not infer exact NAND page/block boundaries from the word `cell`;
- do not infer whether corrected data is rewritten in place or relocated;
- do not infer the ECC code, correction strength, raw-bit threshold semantics, or controller scanning algorithm;
- do not infer that cells below the threshold have infinite future retention.

### Retained maintenance statistics

Section 9.9.2 says Micron's `emmcparm` can inspect data-retention statistics stored inside the eMMC, specifically including execution count, the counter value at the last completed retention operation, and current retention progress. The displayed report includes `Self Refresh Loop Count` and `Refresh Count`, and the fuller report vocabulary includes current scan progress, refresh-queue/completion state, and a power-loss counter.

This grounds the second-order-state claim:

> A managed NAND device can retain maintenance history/progress distinct from its user payload.

It does not prove that these fields preserve a complete chronology, a per-cell aging record, or an end-to-end guarantee of future readability.

## Source B — maintained Atmark product documentation

Later maintained editions continue to describe the same key architecture after section renumbering: OTP trigger selection, the internal-value versus `SET_TIME` comparison, reset-bounded Delay 1, bus-idle observation, Delay 2, and selective threshold-triggered self refresh.

Use of this continuity is deliberately conservative:

- it supports that the documented product family continued to expose the mechanism;
- it is **not** used to backdate fields or behavior absent from v1.0.0;
- changes in integration file names or surrounding Linux packaging are not treated as changes in the eMMC retention mechanism without separate evidence.

## Source C — Micron TN-FC-60 catalog metadata

Micron's official eMMC software/download page lists:

**TN-FC-60: _Refresh Features for Micron e.MMC Automotive 5.1 Devices_ — 4.11.2023**

The same page's date formatting across neighboring entries is month.day.year, so this is read as **11 April 2023**. Its description says the technical note covers additional data-refresh features available in Micron automotive eMMC 5.1 devices built with Micron firmware.

Accepted manufacturer-level claim:

> Micron had an official technical note by 11 April 2023 specifically scoped to refresh features in its automotive eMMC 5.1 firmware family.

Rejected uses:

- the catalog metadata is not a substitute for the note's normative/technical body;
- no timing, threshold, persistence, reset, or command-detail claim is attributed to TN-FC-60 unless separately visible in an inspected source;
- the catalog date is not an invention date;
- the title does not establish that every Micron automotive eMMC 5.1 part/firmware revision supports one identical implementation.

## Engineering reconstruction

### 1. Payload retention and maintenance-evidence retention are different objects

The mechanism can be modeled without claiming vendor vocabulary:

```text
payload state
    <-protected by-
selective renewal work
    <-authorized/scheduled by-
elapsed-time evidence + error evidence + idle opportunity
    <-partly observed through-
progress / queue / count / completion telemetry
```

The arrows are analytical relations. None says that the telemetry contains the payload or that payload correctness can be reconstructed from the counters.

### 2. Eligibility, opportunity, and completion are separate

The documented path requires both a temporal condition and a service opportunity. This produces a useful managed-device distinction:

- **eligible:** enough time has elapsed under the configured comparison;
- **schedulable:** the bus reaches an idle state and the delay condition is met;
- **running:** progress indicates maintenance is active;
- **completed/history:** later statistics may record that maintenance ran.

This is an engineering reconstruction over the product sequence, not an eMMC-standard state machine.

### 3. A compressed maintenance record can be useful without being historical archive

Execution counts and a last-completion counter value retain some past information while discarding event-by-event and cell-by-cell detail.

Therefore:

> `retained maintenance evidence != complete maintenance history`.

That boundary should be kept beside Case 66 (NVMe PEL) rather than silently calling every retained counter a `log`.

### 4. Time input is an authority relation, not just a timestamp

Under the shipped RTC policy, the host-provided command value participates in a comparison that may make maintenance due. It is therefore not merely decorative wall-clock metadata.

But the source does not establish authenticated time, monotonic anti-rollback guarantees, or behavior under malicious/backward time injection. Those are explicit open fault cases.

## Cross-case controls

### Case 36 — Flash Correct-and-Refresh

Bounded similarity: error/correction evidence can select renewal work.

Stop condition: academic FCR evaluation and this commercial eMMC integration are not established as implementation-identical or genealogically related.

### Case 37 — Samsung 840 EVO

Bounded similarity: managed Flash can perform powered hidden maintenance against aging-related service degradation.

Stop condition: Samsung's product episode does not supply Micron's trigger mode, time command, error threshold, or physical rewrite semantics.

### Case 111 — enterprise SSD extended shutdown

Bounded similarity: powered time/opportunity can become retention infrastructure.

Stop condition: operator power-up runbook and embedded reset/time/idle protocol are different control layers.

### Syntheses 24 / 26 / 27

This case sharpens three project taxonomies:

- trigger regimes can be **composite** rather than merely periodic/event-driven;
- maintenance-control state has multiple persistence horizons (OTP policy, current progress, historical count, time relation);
- policy evidence can require validity/representativeness checks independent of payload validity.

No historical genealogy is inferred from these comparisons.

## Counterexamples and stop conditions

1. **`self refresh = DRAM refresh` is rejected.** Shared wording does not establish shared substrate mechanism or scheduling semantics.
2. **`one day = retention lifetime` is rejected.** It is a configured eligibility interval.
3. **`SET_TIME = refresh` is rejected.** It supplies control input before later device work.
4. **`reset = refresh` is rejected.** Reset precedes a command window and later execution conditions.
5. **`bus idle = refresh complete` is rejected.** Idleness is an execution opportunity, not completion evidence.
6. **`ECC threshold = exact physical age` is rejected.** It is a local error-related selector/proxy in the inspected product description.
7. **`Refresh Count = full payload integrity proof` is rejected.** It records maintenance activity, not an end-to-end future-retention guarantee.
8. **`selective refresh = whole-medium rewrite` is rejected.** The source explicitly makes selection conditional.
9. **`Micron TN title = clause-level proof` is rejected.** The full note was not inspected.
10. **`2021 product manual = invention priority` is rejected.** It is a public integration floor only.

## Related-repository boundary

Searches of `tmzncty/computing-archaeology` for `Micron eMMC` and `SET_TIME eMMC` returned no dedicated technical-history treatment during this pass.

If a broader history is developed, route to that companion repository:

- eMMC command/version genealogy;
- BKOPS and other managed-NAND maintenance interfaces;
- Micron controller/firmware generations;
- raw-NAND ECC/read-reclaim implementation history;
- host-controller responsibility changes across JEDEC revisions.

Keep here only the retention-specific decomposition and bounded product evidence.

## Evidence result

This slice supports a new grounded case because it has:

- contemporaneous/versioned product documentation with a concrete mechanism path;
- an independently hosted manufacturer-primary catalog entry confirming the vendor feature family;
- explicit historical vocabulary;
- a bounded host/device authority split;
- concrete maintenance-control and maintenance-history state;
- counterexamples preventing `refresh`, time, ECC, or statistics from being overgeneralized;
- a checked related-repository boundary.

The main unresolved dependency is the secured TN-FC-60 body plus implementation/fault evidence. Those gaps limit genealogy and low-level physical claims but do not undermine the bounded product-interface relation above.

## Source URLs

- Atmark Techno v1.0.0 HTML: <https://manual.atmark-techno.com/armadillo-iot-g4/armadillo-iotg-g4_product_manual_ja-1.0.0/ch09.html>
- Atmark Techno v1.0.0 PDF: <https://armadillo.atmark-techno.com/files/downloads/armadillo-iot-g4/document/armadillo-iotg-g4_product_manual_ja-1.0.0.pdf?v=1639041210>
- Atmark Techno maintained manual: <https://manual.atmark-techno.com/armadillo-iot-g4/armadillo-iotg-g4_product_manual_ja/ch06.html>
- Micron eMMC software / technical-note catalog: <https://www.micron.com/sales-support/downloads/software-drivers/emmc-software>
- Related repository: <https://github.com/tmzncty/computing-archaeology>
