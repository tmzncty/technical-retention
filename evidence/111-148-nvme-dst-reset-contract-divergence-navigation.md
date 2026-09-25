# Case 111 / Case 148 — NVMe Device Self-test reset-contract divergence navigation

Canonical navigation:

- [Case 111 evidence index](111-enterprise-ssd-extended-shutdown-evidence-index.md)
- [Case 111 HIR navigation](111-nvme21-host-initiated-refresh-navigation.md)
- [Case 148 named reset conformance witness](148-ulink-2026-lexar-dst-controller-reset-conformance-deepening.md)
- [Synthesis 26 — maintenance-control state persistence horizons](../docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md)

New bounded packet:

- [NVMe Device Self-test reset-contract divergence deepening](111-148-nvme-dst-reset-contract-divergence-deepening.md)

## Status

Case 111 remains **`grounded`**.  
Case 148 remains **`grounded`**.  
No maturity promotion is made.

## Closed bounded seam

The shared Device Self-test command/log framework does **not** define one shared restart-persistence model:

```text
short DST
    Controller Level Reset -> abort

extended DST
    Controller Level Reset / restoration of power -> persist + resume

HIR
    reset affecting performing controller -> abort + terminal result
    reset on non-performing controller -> no impact
```

Project vocabulary introduced here:

- `operation-coded persistence contract`.

It is engineering reconstruction vocabulary, not NVM Express historical terminology.

## Still open

- Case 111: named shipping HIR implementation with explicit HIR support / `RHIRI` / `HIRT`, plus a real success and interruption trace.
- Case 148: exact hidden checkpoint/reconstitution embodiment used to satisfy extended-DST resume semantics.
- Broad Device Self-test / TP001a / TP4058 proposal genealogy and vendor firmware history remain routed to `tmzncty/computing-archaeology`.

Fresh companion searches found no dedicated reusable packet.
