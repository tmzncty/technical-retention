# Case 111 navigation addendum — NVMe 2.1 Host-Initiated Refresh

Case 111 remains **grounded**. This addendum routes the standards-level HIR observability slice without changing the repository-wide maturity ledger.

## New evidence

- [NVMe 2.1 Host-Initiated Refresh progress / completion boundary](111-nvme21-2024-host-initiated-refresh-progress-completion-deepening.md)
  - records TP4058 / Environmental Extremes Management as the Revision-2.1 introduction point;
  - separates refresh scheduling, nominal duration, actual progress, operation scope, and operation end;
  - records the all-media NVM-subsystem scope without turning it into a claim that every physical page is rewritten;
  - keeps standards capability distinct from named-product adoption.

## Read with

1. [Case 111 evidence index](111-enterprise-ssd-extended-shutdown-evidence-index.md)
2. [Micron industrial eMMC refresh-vs-BKOPS boundary](111-micron-2023-2025-industrial-emmc-refresh-vs-bkops-boundary-deepening.md)
3. [Alliance Memory Auto Read Refresh boundary](111-alliance-2023-auto-read-refresh-vs-bkops-completion-boundary-deepening.md)

## Updated bounded model

```text
generic maintenance status
    != refresh-specific progress

NVMe 2.1 HIR
    -> recommended interval
    -> nominal duration
    -> current percentage complete
    -> all-media operation scope

but:
standardized HIR observability
    != named commercial implementation
    != disclosed physical rewrite algorithm
    != future offline-retention guarantee
```

## Debt update

The broad standards-level observability question is now boundedly closed. Case-111 P1/P6 should next target **named product adoption**: a first-party SSD/NVMe device or high-quality named-device conformance record that shows HIR support and preferably RHIRI/HIRT plus observed progress/completion behavior.

Fresh companion searches found no dedicated HIR / TP4058 packet in `tmzncty/computing-archaeology`; broad feature genealogy and vendor-adoption history remain routed there.
