# Case 83 — HDFS block-scanner evidence index

Status: **navigation only**. Canonical case maturity remains **`grounded`**.

Canonical:

- [`cases/83-apache-hdfs-block-scanner-checksum-verification.md`](../cases/83-apache-hdfs-block-scanner-checksum-verification.md)

This index exists because Case 83 now has several distinct evidence lines. They should not be collapsed into a single generic claim that "HDFS scrubs blocks". Each line establishes a different retention boundary.

## Evidence map

| Evidence | Main question | Boundary established |
|---|---|---|
| [`83-hadoop-2003-2016-block-scanner-grounding.md`](83-hadoop-2003-2016-block-scanner-grounding.md) | What is the historical / technical foundation of HDFS block scanning and checksum verification? | background scan, checksum qualification, and repair escalation are distinct operations |
| [`83-hadoop-2012-verification-log-rollover-rescan-cadence-deepening.md`](83-hadoop-2012-verification-log-rollover-rescan-cadence-deepening.md) | What happens if recent verification history is discarded too early? | successful maintenance, retained completion evidence, worker wakeup cadence, and effective rescan cadence are distinct |
| [`83-hadoop-270-271-blockscanner-default-enable-regression-deepening.md`](83-hadoop-270-271-blockscanner-default-enable-regression-deepening.md) | Can scanner code exist but fail to run under default configuration? | implementation present != maintenance effectively admitted / enabled |
| [`83-hdfs-2016-volume-scanner-concurrent-append-coherence-deepening.md`](83-hdfs-2016-volume-scanner-concurrent-append-coherence-deepening.md) | How can scanner metadata become incoherent with a concurrently changing replica? | checksum metadata view must correspond to the payload extent being qualified |
| [`83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md`](83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md) | What does scanner traversal persistence require across restart / wall-clock changes? | traversal cursor persistence != correct time-domain interpretation |
| [`83-hdfs-2018-finalized-partial-checksum-cache-deepening.md`](83-hdfs-2018-finalized-partial-checksum-cache-deepening.md) | What if a scanner-side checksum optimization cache is lost? | reconstructible performance state != integrity authority |

## Chronological reading path

A useful chronological path is:

```text
grounding / early scanner history
    -> 2012 verification-log rollover and pathological rescan
    -> 2.7.0 / 2.7.1 enable-state regression
    -> 2016 concurrent-append coherence
    -> cursor / clock-domain persistence
    -> 2018 reconstructible partial-checksum cache
```

The mechanisms change across these documents. Chronological adjacency does **not** establish direct implementation genealogy unless a source does so explicitly.

## Retained-state distinctions now covered

Case 83 collectively distinguishes at least the following state classes:

```text
payload bytes
checksum / integrity metadata
recent verification-time history
scanner enable / admission configuration
current traversal cursor
cursor timestamp / time-domain interpretation
reconstructible checksum optimization cache
runtime scanner thread / wakeup state
```

These are not interchangeable.

In particular, the 2012 HDFS-3828 evidence now adds:

```text
successful verification at t1
    !=
retained evidence at t2 that the block is not yet due again
```

and:

```text
worker wakes every few seconds
    !=
block should be verified every few seconds
```

That slice is intentionally separate from later `VolumeScanner` cursor work. A verification-time history answers a different scheduling question from a traversal-position checkpoint.

## Controlled cross-case links

Useful functional comparisons, without historical-lineage claims:

- **Case 26 / GFS integrity evidence:** some historical records are consumed by future correctness or maintenance decisions, while other diagnostic history is optional.
- **Case 101 / SCSI Background Medium Scan:** configured maintenance interval, execution opportunity, progress, and medium-error outcome are distinct.
- **Synthesis 29 / maintenance observability:** schedule, admission, execution, coverage, accounting, and closure should not be collapsed. The HDFS-3828 slice adds a concrete case where completion history feeds later scheduling eligibility.

Do not use these comparisons to claim that HDFS verification logs descend from SCSI scan counters or GFS metadata structures.

## Current open debts

Case 83 remains `grounded`; this index does not promote it. High-value remaining work includes:

1. tag-by-tag / branch-by-branch release genealogy for the 2012 HDFS-3828 correction, rather than equating the 2012 source integration with its later 2.5.0 changelog placement;
2. exact pre/post-HDFS-3828 verification-log generation format and restart semantics;
3. controlled fault / restart observation showing which scanner progress and verification-history state survives DataNode restart versus process crash;
4. a tighter genealogy from `DataBlockScanner` / `BlockPoolSliceScanner` state into later `VolumeScanner` cursor and iterator mechanisms;
5. empirical traces for pathological over-scan, missed scan, corrupted checksum metadata, and repair escalation under realistic multi-volume loads;
6. sharper separation between correctness-critical integrity authority and reconstructible scanner acceleration state across later releases.

## Related-repository reuse status

`tmzncty/computing-archaeology` was checked for `DataBlockScanner` / HDFS block-scanner material before the 2012 deepening was written. No directly reusable packet was found.

If a broader Hadoop scanner technology-history packet is later added there, Case 83 should link to it and keep this repository focused on retained-state / maintenance semantics rather than duplicating the general technical history.
