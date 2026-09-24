# Case 04 deepening — PCMCIA FTL duplicate-LogicalEUN recovery boundary

**Case 04 remains `grounded`.**

PCMCIA/JEIDA Release 7.0 Volume 7 (February 1999) and Linux v2.6.12 together show a bounded Unit Recovery handoff: `LogicalEUN = 7FFFh` marks recovery in progress; after successful copy the destination takes the source LogicalEUN; before the old unit is recycled two physical erase units may carry the same logical designation. The standard allows either equivalent unit to be kept. Linux `build_maps()` concretely accepts the first physical occurrence and reconstructs a later duplicate as `XFER_UNKNOWN`.

This supports `duplicate physical designation != necessarily conflicting logical versions`, `destination promotion != old-embodiment retirement`, and `physical recency != restart authority ordering` for this documented path. `Embodiment-equivalence overlap` and `restart collapse authority` are repository engineering terms, not historical vocabulary.

The comparison to replica currentness is functional only. No genealogy to distributed storage or modern SSD firmware is asserted.

The separate `prepare_xfer()` header-before-BAM reconstruction seam remains open and is the highest-value next fault-trace target.

Sources: PCMCIA/JEIDA, *PC Card Standard Release 7.0, Volume 7: Media Storage Formats Specification*, §§5.1.3.1, 5.1.4, 5.1.6.3; Linux v2.6.12 `drivers/mtd/ftl.c` and `include/linux/mtd/ftl.h`.
