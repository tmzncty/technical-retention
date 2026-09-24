# Case 04 — PCMCIA duplicate-LogicalEUN recovery navigation

Canonical navigation: [04-flash-mapping-evidence-index.md](04-flash-mapping-evidence-index.md)

Bounded packets:
- [04-pcmcia-1999-linux-2005-duplicate-logicaleun-recovery-boundary-deepening.md](04-pcmcia-1999-linux-2005-duplicate-logicaleun-recovery-boundary-deepening.md)
- [04-linux-ftl-2005-header-before-bam-restart-admission-deepening.md](04-linux-ftl-2005-header-before-bam-restart-admission-deepening.md)

**Status:** Case 04 remains `grounded`.

Closed here at source/format-semantics level: PCMCIA Unit Recovery `FFFFh -> 7FFFh -> source LogicalEUN`, the documented temporary duplicate-LogicalEUN overlap after successful copy, and Linux v2.6.12 restart collapse by physical scan order.

Closed at source/control-path level in the follow-up packet: a clean `FFFFh` header can re-admit the transfer-unit role without proving the BAM stub completed, but that partial transfer-unit BAM is not consumed as the live logical map; relocation rebuilds the destination BAM from the source before logical-identity promotion.

Still open: lower-media torn/programmed-field behavior, reset/power-loss traces around EUH/BAM writes and promotion, named-card validation, and modern NAND/SSD free-pool comparison.

Related-repository check: no dedicated `LogicalEUN` / PCMCIA FTL duplicate-recovery packet was found in `tmzncty/computing-archaeology`; broader genealogy stays routed there.
