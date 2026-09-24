# Case 04 — PCMCIA duplicate-LogicalEUN recovery navigation

Canonical navigation: [04-flash-mapping-evidence-index.md](04-flash-mapping-evidence-index.md)

New bounded packet:
- [04-pcmcia-1999-linux-2005-duplicate-logicaleun-recovery-boundary-deepening.md](04-pcmcia-1999-linux-2005-duplicate-logicaleun-recovery-boundary-deepening.md)

**Status:** Case 04 remains `grounded`.

Closed here at source/format-semantics level: PCMCIA Unit Recovery `FFFFh -> 7FFFh -> source LogicalEUN`, the documented temporary duplicate-LogicalEUN overlap after successful copy, and Linux v2.6.12 restart collapse by physical scan order.

Still open: lower-media interrupted-write behavior, the `prepare_xfer()` header-before-BAM reconstruction seam, named-card validation, and modern NAND/SSD free-pool comparison.

Related-repository check: no dedicated `LogicalEUN` / PCMCIA FTL duplicate-recovery packet was found in `tmzncty/computing-archaeology`; broader genealogy stays routed there.
