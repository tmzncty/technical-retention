# Case 111 navigation addendum — Linux NVMe HIR host tooling

Case 111 remains **grounded**. This addendum routes the Linux NVMe userspace adoption slice without changing the repository-wide maturity ledger.

## Evidence

[Linux NVMe HIR host-tooling / wait-policy boundary](111-linux-nvme-2024-2026-hir-host-tooling-wait-policy-boundary-deepening.md)

The bounded source sequence is:

```text
5 Aug 2024 — NVMe 2.1 ratified
    -> 6 Dec 2024 — libnvme adds RHIRI / HIRT
    -> 20 Dec 2024 — libnvme adds HIRS + STC=3h
    -> 9 Jan 2025 — nvme-cli adds HIR command/result presentation
```

The inspected 2026 userspace source can expose HIR capability-adjacent fields and submit Host-Initiated Refresh. The same source also preserves a narrower software-policy boundary:

```text
HIR field exposed
    != HIR-specific wait policy

HIRT visible
    != HIRT consumed by wait_self_test()

live completion percentage polled
    != newest terminal Self-test Result interpreted by the wait helper

host-tool HIR support
    != named-device HIR adoption
```

The generic `wait_self_test()` path derives its no-progress threshold from `EDSTT`, not `HIRT`. Treat this as an implementation-observation boundary only; it is not evidence that a controller violates the NVMe specification.

The inspected libnvme source also has typed HIR command/result constants while `enum nvme_st_curr_op` lacks a named HIR current-operation constant. The raw current-operation byte remains exposed, so this is a host-library taxonomy asymmetry, not a controller-conformance finding.

## Debt update

Case-111 P1 remains unchanged in substance and sharper in evidentiary form:

> Find a first-party named shipping NVMe SSD that explicitly advertises HIR or reports `HIRS=1`, recover its `RHIRI` / `HIRT`, and obtain a successful HIR trace plus at least one interruption/reset trace with terminal result evidence.

Mainstream Linux host-tool support is useful prior art and makes such an experiment practical, but it does not substitute for named-device adoption evidence.

## Related-repository routing

Fresh searches in `tmzncty/computing-archaeology` for `Host-Initiated Refresh`, `RHIRI HIRT`, and adjacent reset terms found no dedicated packet. Broader libnvme/nvme-cli feature history belongs there if expanded; this repository keeps only the retention-specific observability and authority boundary.
