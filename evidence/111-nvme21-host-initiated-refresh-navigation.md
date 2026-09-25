# Case 111 navigation addendum — NVMe Host-Initiated Refresh

Case 111 remains **grounded**. This addendum routes the standards-level HIR observability, terminal-outcome, product-adoption, and reset-contract comparison slices without changing the repository-wide maturity ledger.

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

3. [Memblaze PBlaze7 NVMe 2.1 / HIR adoption guardrail](111-memblaze-pblaze7-nvme21-hir-adoption-guardrail-deepening.md)
   - compares the dated 3-Sep-2024 NVMe-2.0 launch record with the current NVMe-2.1 product page;
   - records current `Advanced Device Self-Test` plus `3 months @ 40°C` power-off-retention wording;
   - rejects `NVMe 2.1 + Device Self-test = HIR implemented`;
   - treats absence from a marketing feature list as insufficient to prove implementation absence.

4. [Case 111 / Case 148 Device Self-test reset-contract divergence](111-148-nvme-dst-reset-contract-divergence-deepening.md)
   - compares short DST, extended DST, and HIR inside the shared Device Self-test framework;
   - records short DST reset-abort versus extended DST reset/power-restoration resume;
   - records HIR abort on a Controller Level Reset affecting the performing controller, while a reset on another controller does not impact that HIR;
   - rejects `same Device Self-test command/log family = same persistence horizon`;
   - introduces `operation-coded persistence contract` only as project engineering vocabulary.

## Read with

- [Case 111 evidence index](111-enterprise-ssd-extended-shutdown-evidence-index.md)
- [Case 111 / Case 148 reset-contract navigation](111-148-nvme-dst-reset-contract-divergence-navigation.md)
- [Case 148 named Device Self-test reset-conformance witness](148-ulink-2026-lexar-dst-controller-reset-conformance-deepening.md)
- [Micron industrial eMMC refresh-vs-BKOPS boundary](111-micron-2023-2025-industrial-emmc-refresh-vs-bkops-completion-boundary-deepening.md)
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

same Device Self-test command/log family
    != same reset/power continuity contract

extended DST reset/power resume
    != HIR reset resume

standards-defined HIR
    != named commercial implementation
```

## Debt update

The standards-level questions “can refresh-specific progress be public?”, “can a HIR episode have a refresh-specific terminal outcome distinct from command completion?”, and “does the shared Device Self-test framework imply one common reset-persistence model?” are now boundedly closed.

Case-111 P1 should next target **named product adoption**: a first-party shipping SSD/NVMe product or strong named-device record that advertises HIR and exposes `RHIRI`, `HIRT`, current progress, and terminal result behavior. A real device trace through successful completion and at least one interruption/reset path would be stronger still.

The PBlaze7 guardrail sharpens this target: **NVMe 2.1 conformance, Advanced Device Self-Test, and a power-off-retention rating are still insufficient to attribute optional HIR to a named product.** Require explicit HIR naming, Identify Controller evidence, a named conformance artifact, or a device trace.

Case 148 retains a separate implementation debt: the public extended-DST contract requires operation continuity across reset/power restoration, but the exact hidden checkpoint/reconstitution embodiment remains undisclosed.

Fresh companion searches for `Host-Initiated Refresh`, `TP4058`, `Device Self-test reset Host-Initiated Refresh`, and `NVMe extended self-test reset` found no dedicated packet in `tmzncty/computing-archaeology`; broad NVMe feature/Device-Self-test genealogy and product-adoption history remain routed there.
