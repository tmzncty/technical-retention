# Case 111 — Alliance 2023 Auto Read Refresh boundary

**Status:** Case 111 remains `grounded`.

## Scope

Alliance Memory's July-2023 32/64/128GB industrial eMMC 5.1 datasheet gives an independent commercial-product witness for the open Case-111 completion-authority question.

## Historical record

The first-party datasheet explicitly documents:

- **Read Disturb Management**: reads are monitored per region and content is conditionally refreshed after critical levels;
- **Auto Read Refresh**: interruptible background maintenance for read-disturb effects and retention degradation associated with high temperature;
- Device Health Report plus Alliance proprietary Lifetime Monitor data.

The same EXT_CSD table exposes generic eMMC maintenance fields:

```text
BKOPS_SUPPORT   [502]
BKOPS_STATUS    [246]
BKOPS_START     [164]
BKOPS_EN        [163]
PERIODIC_WAKEUP [131]
```

It also exposes standard lifetime/pre-EOL fields and `FFU_STATUS [26]`.

The inspected public datasheet does **not** identify any field as Auto Read Refresh progress, refresh coverage, or refresh completion, and does not state that BKOPS, health, or lifetime fields certify Auto Read Refresh completion.

Primary source: Alliance Memory, *32GB/64GB/128GB eMMC — ASFC Series Industrial embedded MMC 5.1*, Rev. 1.0, July 2023. Relevant printed pages: 3–4, 37, 40.

https://www.alliancememory.com/wp-content/uploads/AllianceMemory__32GB_64GB_128GB_ASFC32G31T3-51BIN_ASFC64G31T5-51BIN_ASFC.pdf

## Engineering reconstruction

```text
retention-targeted refresh exists
    != generic BKOPS completion identifies that refresh

refresh work executed for some interval
    != whole-device refresh coverage complete

health / lifetime telemetry exists
    != refresh-progress or refresh-completion evidence
```

Because Alliance calls Auto Read Refresh interruptible, execution and coverage completion must remain separate predicates.

These are project engineering distinctions, not Alliance or JEDEC terminology.

## Cross-vendor comparison

Read with the existing Micron product packet. Micron publicly names BKOPS plus host/auto refresh; Alliance independently names retention-targeted Auto Read Refresh plus generic BKOPS. Neither inspected public product interface binds generic BKOPS completion to retention-refresh completion.

This is a functional/engineering comparison only; it does not establish shared firmware, controller ancestry, or algorithm identity.

## Reuse boundary

A fresh search of `tmzncty/computing-archaeology` found no dedicated Alliance Memory / Auto Read Refresh packet. Broader eMMC/controller genealogy belongs there if pursued.

## Remaining debt

Case 111 P1/P6 remains open: find a first-party named SSD/NVMe/SAS/eMMC interface that explicitly binds a host-visible terminal state, progress field, or coverage result to **retention refresh / data refresh completion itself**.

## Bounded result

```text
explicit retention-targeted Auto Read Refresh
    + interruptible execution
    + generic BKOPS
    + health/lifetime telemetry

but:
generic maintenance status
    != public retention-refresh completion certificate
```
