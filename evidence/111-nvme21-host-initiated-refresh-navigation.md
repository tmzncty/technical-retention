# Case 111 navigation addendum — NVMe Host-Initiated Refresh

Case 111 remains **grounded**. This addendum routes the standards-level HIR observability and terminal-outcome slices without changing the repository-wide maturity ledger.

## Evidence

1. [NVMe 2.1 Host-Initiated Refresh progress / completion boundary](111-nvme21-2024-host-initiated-refresh-progress-completion-deepening.md)
   - records TP4058 / Environmental Extremes Management as the Revision-2.1 introduction point;
   - separates refresh scheduling, nominal duration, live progress, operation scope, and operation end;
   - keeps all-media operation scope distinct from a claim that every physical page is rewritten;
   - keeps standards capability distinct from named-product adoption.

2. [NVMe 2.1/2.2 HIR terminal-outcome / reset boundary](111-nvme21-22-hir-terminal-outcome-reset-boundary-deepening.md)
   - separates Device Self-test command completion from background HIR completion;
   - records terminal outcome evidence separately from live percentage progress;
   - uses UNH-IOL's 2025 conformance procedure to bind Controller Level Reset, Sanitize, Format NVM, and explicit Device Self-test abort to HIR terminal results;
   - records that Controller Level Reset aborts the observed HIR episode and creates a newest result entry rather than demonstrating exact-progress resume;
   - treats the rolling result log as bounded episode history, not a durable internal refresh checkpoint.

## Read with

- [Case 111 evidence index](111-enterprise-ssd-extended-shutdown-evidence-index.md)
- [Micron industrial eMMC refresh-vs-BKOPS boundary](111-micron-2023-2025-industrial-emmc-refresh-vs-bkops-boundary-deepening.md)
- [Alliance Memory Auto Read Refresh boundary](111-alliance-2023-auto-read-refresh-vs-bkops-completion-boundary-deepening.md)

## Updated bounded model

```text
RHIRI / HIRT
    -> scheduling and nominal-duration evidence

HIR current percentage
    -> live progress evidence

Device Self-test terminal result
    -> bounded success / abort / error outcome evidence

but:
command Successful Completion
    != HIR operation completed

live progress
    != terminal success
    != restartable maintenance checkpoint

terminal result
    != exact internal refresh trajectory
    != future offline-retention guarantee

standards-defined HIR
    != named commercial implementation
```

## Debt update

The standards-level questions “can refresh-specific progress be public?” and “can a HIR episode have a refresh-specific terminal outcome distinct from command completion?” are now boundedly closed.

Case-111 P1 should next target **named product adoption**: a first-party shipping SSD/NVMe product or strong named-device record that advertises HIR and exposes `RHIRI`, `HIRT`, current progress, and terminal result behavior. A real device trace through successful completion and at least one interruption/reset path would be stronger still.

Fresh companion searches for `Host-Initiated Refresh`, `TP4058`, and `Device Self-test refresh` found no dedicated packet in `tmzncty/computing-archaeology`; broad NVMe feature genealogy and product-adoption history remain routed there.
