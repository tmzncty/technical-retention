# Case 04 deepening — PCMCIA FTL duplicate-LogicalEUN recovery boundary

**Status:** Case 04 remains `grounded`.

This bounded slice connects the PCMCIA/JEIDA *PC Card Standard Release 7.0, Volume 7: Media Storage Formats Specification* (February 1999) to Linux v2.6.12 `ftl.c`. It asks what the FTL is allowed to retain when relocation has copied a logical erase unit but the old physical unit has not yet been recycled.

## Historical record

PCMCIA Unit Recovery uses a persistent `LogicalEUN` field in the Erase Unit Header. A prepared Transfer Unit normally has the erased-state logical number `FFFFh`. Before recovery copying begins, the destination is changed to `7FFFh`; after the allocated blocks have been transferred successfully, the destination is changed to the source `LogicalEUN`.

The standard explicitly covers interruption after that promotion but before the old erase unit is recycled: two physical erase units can then contain the same data under the same logical number, and either can be used as the Logical Erase Unit while the other becomes a Transfer Unit. Partition Recognition independently permits either duplicate to be treated as the Transfer Unit.

Linux v2.6.12 implements the matching sequence in `copy_erase_unit()`: write `0x7fff`, copy source data and BAM state, then write the source logical number. On restart, `build_maps()` scans physical erase units in order; the first valid occurrence fills `EUNInfo[LogicalEUN]`, while a later duplicate falls through to `XFER_UNKNOWN`.

The uninterrupted Linux path later swaps the runtime source/transfer roles and schedules the old physical unit for erase. Destination promotion and old-unit retirement are therefore separate events.

## Engineering reconstruction

The source-controlled transition is:

```text
prepared transfer unit: FFFFh
    -> Unit Recovery in progress: 7FFFh
    -> successful copy / BAM reconstruction
    -> destination promotion to source LogicalEUN
    -> bounded duplicate-embodiment overlap
    -> restart collapses overlap if needed
    -> losing/old embodiment re-enters erase + preparation lifecycle
```

This supports:

```text
duplicate physical designation
    != necessarily conflicting logical versions

destination promotion
    != old-embodiment retirement

physical recency
    != required restart authority ordering
```

For repository comparison, **embodiment-equivalence overlap** names the bounded post-copy state, and **restart collapse authority** names the rule that reduces it to one working mapping. These are repository terms, not PCMCIA, JEIDA, M-Systems, Hinds, or Linux historical vocabulary.

The claim is deliberately conditional on the standard's successful-copy path. It does not prove that arbitrary duplicate `LogicalEUN` values are harmless, that a torn field update is atomic, or that Linux verifies byte-for-byte equality before selecting a duplicate.

A separate open seam remains: `prepare_xfer()` writes the `FFFFh` header before its BAM stub is complete, while `build_maps()` visibly reconstructs `XFER_PREPARED` from the header condition. That remains a fault-trace target; this packet does not label it safe or unsafe.

## Functional analogy

The overlap can be compared to replica-currentness cases only at one structural level: **physical multiplicity does not itself decide authority**.

The analogy stops there. This PCMCIA path expects equivalent data after a successful copy and permits either embodiment to survive restart. RADOS, Kafka, Swift, or other distributed systems can require version, epoch, membership, quorum, peering, or lineage evidence. No genealogy from PCMCIA FTL to distributed storage or modern SSD firmware is asserted.

## Philosophical interpretation

A narrow retention point follows from the mechanism: logical continuity need not require uninterrupted privilege of one material embodiment. During this handoff, identity can remain available while two physical copies are temporarily acceptable because a retained recovery rule can later collapse the overlap and retire one copy.

That is an interpretation of the documented recovery relation, not a historical claim about what the standard's authors thought retention or identity meant.

## Evidence boundary and next work

This packet closes the post-copy duplicate-`LogicalEUN` overlap at the source/format-semantics level. It does **not** close lower-media interrupted-write behavior.

Highest-value next work is the Linux `prepare_xfer()` header-before-BAM fault trace, followed by a named-card trace across `7FFFh`, destination promotion, duplicate selection under opposite physical ordering, and losing-copy requalification.

A fresh search of `tmzncty/computing-archaeology` for `prepare_xfer` / `build_maps`, `LogicalEUN` `FFFFh` / `7FFFh`, and PCMCIA duplicate-unit recovery found no dedicated packet to reuse. Broader PCMCIA/FTL genealogy remains routed there.

## Sources

1. PCMCIA/JEIDA, *PC Card Standard Release 7.0, Volume 7: Media Storage Formats Specification*, first printing February 1999, §§5.1.3.1, 5.1.4, 5.1.6.3. Archival copy: <https://0x04.net/~mwk/doc/pcmcia/volumes/07-ms-70.pdf>.
2. Linux v2.6.12, `drivers/mtd/ftl.c`: <https://github.com/torvalds/linux/blob/v2.6.12/drivers/mtd/ftl.c>.
3. Linux v2.6.12, `include/linux/mtd/ftl.h`: <https://github.com/torvalds/linux/blob/v2.6.12/include/linux/mtd/ftl.h>.
4. Existing continuity packet: [04-linux-ftl-2005-transfer-unit-reuse-admission-deepening.md](04-linux-ftl-2005-transfer-unit-reuse-admission-deepening.md).
