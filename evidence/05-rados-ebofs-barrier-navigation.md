# Case 05 evidence navigation — EBOFS barrier boundary

Case 05 remains **grounded**. This addendum routes the new lower-layer persistence evidence without changing the authoritative maturity ledger.

## New chain

- [Ceph 2007 EBOFS queue barrier versus media-persistence barrier](05-ceph-2007-ebofs-queue-barrier-vs-media-flush-boundary-deepening.md)
  - closes the source-level meaning of `dev.barrier()`;
  - separates Ceph scheduler ordering from the contemporary Linux hard-I/O-barrier / cache-flush interface;
  - adds the bounded anti-collapse `queue-order completion != BlockDevice completion != media-persistence completion`;
  - preserves the non-claim that source inspection alone proves neither universal safety nor universal data loss under sudden power failure.

## Relation to existing Case 05 evidence

Read this after:

1. [RADOS 2006–2007 grounding](05-rados-2006-2007-grounding.md);
2. [OSDMap restart persistence](05-ceph-2007-osdmap-restart-persistence-deepening.md);
3. [EBOFS journal persistence boundary](05-ceph-2007-ebofs-journal-persistence-boundary-deepening.md).

The new slice narrows an explicit debt in item 3. It does not alter the higher-layer conclusions about map currentness, PG peering, distributed commit, or repair completion.

## Next bounded debt

If Case 05 is revisited, prefer one of:

- exact Linux v2.6.22 `O_SYNC|O_DIRECT` raw-block completion semantics;
- a named 2007-era controller/disk/write-cache power-cut stack;
- a controlled historically pinned EBOFS fault experiment.

Broader Linux barrier and Ceph local-store genealogy belongs primarily in `computing-archaeology`.
