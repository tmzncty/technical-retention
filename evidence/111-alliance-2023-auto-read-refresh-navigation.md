# Case 111 navigation addendum — Alliance Auto Read Refresh

Case 111 remains **grounded**. This addendum routes an independent commercial-eMMC witness without changing the repository-wide maturity ledger.

## New evidence

- [Alliance Memory 2023 Auto Read Refresh versus generic BKOPS completion](111-alliance-2023-auto-read-refresh-vs-bkops-completion-boundary-deepening.md)
  - names retention-targeted Auto Read Refresh on a commercial industrial eMMC family;
  - records that the process is explicitly interruptible background work;
  - separates generic BKOPS control/status from refresh-specific progress, coverage, and completion;
  - separates Device Health / Lifetime Monitor observability from refresh-completion authority;
  - adds an independent-vendor comparison to the existing Micron product witness.

## Read after

1. [Case 111 evidence index](111-enterprise-ssd-extended-shutdown-evidence-index.md)
2. [eMMC 4.41→5.1 BKOPS / periodic-wakeup deepening](111-emmc-441-51-bkops-periodic-wakeup-maintenance-cadence-deepening.md)
3. [Micron industrial eMMC refresh-vs-BKOPS boundary](111-micron-2023-2025-industrial-emmc-refresh-vs-bkops-boundary-deepening.md)

## Updated bounded model

```text
retention-targeted refresh capability
    != generic maintenance status

refresh execution
    != refresh coverage completion

health / lifetime telemetry
    != refresh-specific completion evidence

two vendors show refresh + BKOPS coexistence
    != BKOPS completion is a refresh certificate
```

## Open debt

P1/P6 remains open. The next useful source must explicitly bind a visible terminal state, progress field, or coverage result to retention-refresh / data-refresh completion itself.

Fresh companion search found no dedicated Alliance Memory / Auto Read Refresh packet in `tmzncty/computing-archaeology`; broader product/controller history should stay there rather than being duplicated here.
