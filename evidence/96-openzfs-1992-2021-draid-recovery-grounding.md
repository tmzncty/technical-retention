# Grounding record — Case 96: OpenZFS dRAID distributed spare and sequential resilver

**Case:** [`cases/96-openzfs-draid-distributed-spare-sequential-resilver.md`](../cases/96-openzfs-draid-distributed-spare-sequential-resilver.md)  
**Status:** `grounded`  
**Bounded window:** 2017–2021 for the OpenZFS mechanism; 1992–1994 CMU work only as earlier parity-declustering/distributed-sparing prior art.

## Research question

What primary and high-quality historical evidence is sufficient to support the narrow claim that OpenZFS dRAID reduces the time spent with reduced redundancy by composing:

1. declustered fixed-width RAID-Z redundancy groups;
2. deterministic permutation mappings across many children;
3. distributed spare capacity;
4. sequential device reconstruction; and
5. a later checksum-verification phase?

The record also asks what that mechanism **does not** prove about parity count, latent corruption, UREs, failure domains, invention priority, or probabilistic durability.

## Evidence classification

| Source | Date / release | Class | Used for | Not used for |
| --- | --- | --- | --- | --- |
| OpenZFS dRAID HOWTO wiki revision | 2017-03-15 revision | `H/P` project-development documentation | early mechanism vocabulary; all-device participation; space-map scan; sequential I/O; checksum limitation | production release date or final terminology |
| OpenZFS PR #10102 | opened 2020-03-04; merged 2020-11-13 | `H/P` primary development record | accepted dRAID composition; benchmark-bounded traditional-spare bottleneck and distributed-spare speedup; test coverage | universal performance number |
| OpenZFS 2.1.0 release | published 2021-07-02 | `H/P` primary release record | production/release anchor; dRAID as major feature; stated faster redundancy restoration | invention priority |
| `vdev_draid.c`, tag `zfs-2.1.0` | 2021 release source | `H/P` primary implementation | distributed groups, permutation maps, distributed spare capacity, compatibility/mapping constraint | all later dRAID variants |
| `vdev_rebuild.c`, tag `zfs-2.1.0` | 2021 release source | `H/P` primary implementation | sequential vs healing reconstruction, fixed-width requirement, checksum limitation, follow-up scrub | universal RAID rebuild model |
| current OpenZFS dRAID docs / `zpoolconcepts(7)` | current | `P/S` later institutional witness | surviving explanation; fixed width; distributed spare; sequential resilver; rebalancing distinction | exact 2017 vocabulary |
| Holland & Gibson ASPLOS V | 1992 | `S/H` peer-reviewed scholarly prior art | parity declustering predates dRAID; recovery-load/recovery-time motivation | direct OpenZFS lineage |
| Holland CMU dissertation | 1994 | `S/H` scholarly prior art | distributed sparing predates dRAID; spare bottleneck motivation | proof OpenZFS copied the design |

## A. Release anchor — OpenZFS 2.1.0

The OpenZFS GitHub release record for `zfs-2.1.0` was published on **2021-07-02 at 18:34:51 UTC**.

Stable record:

- <https://github.com/openzfs/zfs/releases/tag/zfs-2.1.0>

Under `Major New Features`, it lists **Distributed Spare RAID (dRAID)** and describes it as a distributed variant of RAID-Z using integrated hot spares to enable dramatically faster resilvering. It states that full redundancy can be restored in a fraction of the time normally required for a full disk replacement.

### Supported claims

- dRAID is a released OpenZFS 2.1.0 feature, not merely an old design sketch;
- restoring **full redundancy** is an explicit project goal of the feature;
- the speed claim is tied to recovery/resilvering rather than ordinary foreground I/O alone.

### Limits

The release note is not used to establish:

- a numerical universal speedup;
- a claim that dRAID invented distributed sparing or parity declustering;
- a claim that faster rebuild alone guarantees data integrity.

## B. Accepted development record — PR #10102

OpenZFS PR #10102, **Distributed Spare (dRAID) Feature**, is an unusually strong primary development source because it records the mechanism, benchmark context, configuration vocabulary, test coverage, and merge point in one place.

Stable record:

- <https://github.com/openzfs/zfs/pull/10102>

The PR was opened **2020-03-04** and merged **2020-11-13**.

### B.1 All-device participation is the central design move

The PR states that dRAID allows all dRAID children to participate when rebuilding to a distributed hot spare, substantially reducing time to restore full parity after a failed device.

This supports the bounded retention relation:

**same spare capacity ≠ same repair bandwidth.**

A conventional dedicated spare can become the write bottleneck. Distributing the recovery destination allows many devices to contribute write bandwidth as well as source/reconstruction bandwidth.

### B.2 Benchmark numbers are configuration-bounded

The PR describes a 90-HDD pool filled to 100% and reconstruction of a failed 16 TB device. It reports a traditional spare at roughly 150–160 MB/s and approximately 30 hours, whereas the default stripe-width dRAID test completes in roughly 7–8 hours (less than 25% of the traditional-hot-spare time in that particular test).

The grounding record preserves the **test configuration** because stripping it away would turn an implementation benchmark into a false universal law.

Case 96 may use these numbers as a primary engineering-development witness for bottleneck removal, but may not write `dRAID is always 4x faster`.

### B.3 The configuration exposes independent axes

The PR exposes:

- parity level `P`;
- data devices per group `D`;
- child count `C`;
- distributed spare count `S`.

The stated tradeoff is also important: narrower redundancy groups can rebuild faster because fewer devices need to be read for each missing contribution, but reduce usable capacity relative to wider groups.

Therefore:

**repair speed ≠ parity count ≠ usable capacity.**

These axes must remain separate in cross-case comparison.

## C. Released implementation — `vdev_draid.c`

Primary source:

- <https://github.com/openzfs/zfs/blob/zfs-2.1.0/module/zfs/vdev_draid.c>

The release-tag source says a dRAID vdev consists of multiple RAID-Z redundancy groups spread over the dRAID children. It applies a permutation mapping to child ordering in order to distribute parity and avoid recovery hot spots.

It further states that reserving a fraction of every child's capacity permits **virtual distributed spare disks** and that spanning all children lets rebuild/resilver operations use more IOPS and bandwidth, reducing the time to restore full parity.

### C.1 Repair parallelism is encoded in layout

This is stronger than a generic statement that `parallelism is good`.

The source ties recovery participation to an explicit on-disk/logical mapping regime:

- data/parity group position;
- physical child selection;
- permutation number;
- distributed spare position.

Engineering reconstruction (`E`): **repair parallelism is partly retained layout state.**

### C.2 Mapping continuity is a recoverability requirement

The source comments around the precomputed mapping table are unusually explicit: the map values are hard coded and **must never be changed**, because existing pools depend on regenerating the same mapping to locate their data. Changing the mappings would render existing pools inaccessible.

This supports a retention-specific result that is easy to miss in a performance-only account:

**payload-sector survival ≠ future interpretability if the mapping algorithm/constants cease to reproduce the same layout.**

The constants are not user payload, but software compatibility with them participates in storage persistence.

### C.3 Do not overstate the mapping witness

This evidence does not prove that every piece of dRAID geometry exists only in source code. Pool labels/configuration and other on-disk structures also participate. The bounded statement is merely that compatibility depends on the same deterministic mapping being reproducible.

## D. Released implementation — `vdev_rebuild.c`

Primary source:

- <https://github.com/openzfs/zfs/blob/zfs-2.1.0/module/zfs/vdev_rebuild.c>

The file's introductory design comment directly distinguishes two recovery forms.

### D.1 Healing reconstruction

Historically, ZFS resilver/scrub walks block-aware state, allowing checksums to be verified as blocks are read and repaired. The source says this advantage can come with a less sequential/randomer disk I/O pattern and longer time to restore redundancy.

### D.2 Sequential reconstruction / device rebuild

The alternative sequential reconstruction behaves like a traditional RAID rebuild:

- reconstruction proceeds in LBA order;
- only allocated capacity is reconstructed;
- I/O can span ZFS block boundaries and therefore be larger;
- reconstruction is driven per top-level vdev;
- it **does not verify block checksums during the reconstruction phase**.

The source explicitly says that when this first phase completes, redundancy has been restored, allowing the pool to withstand another device failure within the configured redundancy model; afterward a second scrub phase verifies checksums.

This is direct primary support for:

**redundancy restoration ≠ integrity revalidation.**

### D.3 Fixed stripe width is a recovery-enabling constraint

The same source says sequential reconstruction is not possible on ordinary RAID-Z in this implementation because RAID-Z has variable stripe width. dRAID uses fixed stripe width to avoid that limitation, at some usable-capacity cost.

This creates a precise cross-case contrast with Case 95 without making either design universal:

- Case 95: variable width participates in RAID-Z's write-hole avoidance and allocation efficiency;
- Case 96: fixed width makes a different recovery traversal possible.

### D.4 Follow-up scrub is not incidental

`vdev_rebuild.c` defines `zfs_rebuild_scrub_enabled = 1` and describes automatically starting a pool scrub after the last active sequential resilver so the checksums of rebuilt blocks are verified. The source calls this strongly recommended.

That default is evidence that the implementation itself treats `reconstructed enough to restore redundancy` and `checksum-verified` as different states.

## E. 2017 dRAID wiki — period project-development witness

Preserved revision:

- <https://github.com/openzfs/zfs/wiki/dRAID-HOWTO/001b44728e1ac3329a4d91be97bcd565a8f351b7>

The selected revision was edited **2017-03-15**.

It uses older project terminology: the new sequential process is called `rebuild`, contrasted with ordinary `resilver`.

The page says the rebuild:

- scans space-map objects rather than the complete block-pointer tree;
- proceeds sequentially, metaslab by metaslab;
- is not constrained to ZFS block boundaries;
- cannot verify block checksums because it lacks block pointers;
- uses all surviving dRAID devices in the illustrated failure instead of only one traditional RAID-Z redundancy group plus a dedicated spare.

### Terminology boundary

Current OpenZFS documentation commonly says `sequential resilver`, while the 2017 wiki says `rebuild`.

Case 96 therefore keeps a chronology-aware vocabulary:

**term evolution ≠ proof that the underlying mechanism was identical in every revision.**

The 2021 released source is authoritative for the release slice; the 2017 wiki is used as earlier development evidence.

## F. Current OpenZFS documentation — later institutional witness

Current documentation:

- <https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Pool%20Structure/dRAID%20Howto.html>
- <https://openzfs.github.io/openzfs-docs/man/master/7/zpoolconcepts.7.html>

These pages preserve several design relations:

- dRAID is a RAID-Z variant with integrated distributed hot spares;
- internal redundancy groups are distributed across children;
- permutation maps distribute physical roles;
- dRAID uses fixed stripe width, padding as needed, to permit sequential resilvering;
- sequential resilver to a distributed spare can scale with many devices and reduce restoration time;
- rebalancing after a physical replacement can use a healing resilver because the pool is no longer in the same degraded urgency state and checksum verification is desirable.

Because these are current pages, they are treated as later institutional witnesses, not as proof that every 2017 implementation detail already matched current OpenZFS.

## G. Prior art — parity declustering

Mark Holland and Garth A. Gibson, **“Parity Declustering for Continuous Operation in Redundant Disk Arrays,”** ASPLOS V, 1992:

- abstract: <https://www.cs.cmu.edu/~riedel/ftp/Declustering/ASPLOS.abstract.html>
- preserved paper: <https://www.pdl.cmu.edu/PDL-FTP/Declustering/ASPLOS.pdf>

The paper explicitly presents **parity declustering** as a way to distribute parity/recovery load, improve degraded-mode throughput, and/or shorten reconstruction time.

Therefore the following claim is rejected:

`OpenZFS dRAID invented parity declustering.`

The CMU paper is used only as earlier scholarly prior art. It does not prove a direct implementation lineage into OpenZFS.

## H. Prior art — distributed sparing

Mark Holland's 1994 CMU dissertation, **On-Line Data Reconstruction in Redundant Disk Arrays** (CMU-CS-94-164), contains a chapter titled `Distributed Sparing`:

- <https://www.pdl.cmu.edu/PDL-FTP/Declustering/Thesis.pdf>

The chapter explicitly motivates distributing online spare capacity across all array disks instead of dedicating one or more spare disks and explains that combining distributed sparing with parity declustering can remove the dedicated spare as the reconstruction bottleneck.

This is extremely close functionally to one of dRAID's retention-relevant moves, so the priority boundary must be explicit:

**OpenZFS composition ≠ invention of distributed sparing.**

Again, functional/prior-art similarity is not evidence of direct source-code descent.

## I. Earlier reconstruction-algorithm prior art

Holland, Gibson, and Siewiorek, **“Fast, On-Line Failure Recovery in Redundant Disk Arrays,”** FTCS-23, 1993:

- <https://www.pdl.cmu.edu/PDL-FTP/Declustering/FTCS.abstract.shtml>

This work evaluates parallel/online reconstruction algorithms and demonstrates that reconstruction scheduling and data layout were already explicit engineering problems decades before OpenZFS dRAID.

Case 96 therefore does not use phrases such as `first sequential rebuild` or `first parallel RAID recovery`.

## J. Cross-case closure

### J.1 Case 17 — parity reconstruction

Case 17 already establishes the generic algebraic relation: redundancy can reconstruct a missing contribution without a duplicate copy and a system can remain degraded until repair restores its redundancy margin.

Case 96 adds a different dimension:

**reconstructability ≠ reconstruction duration.**

Two systems can tolerate the same one-device erasure yet expose the retained object to different lengths of reduced redundancy because their recovery layouts and bottlenecks differ.

### J.2 Case 94 — P+Q dual erasure

Case 94 asks how many known missing contributions the parity equations can solve.

Case 96 asks how quickly a missing contribution can be rebuilt with a given code/layout and what confidence is restored in which phase.

Therefore:

**number of tolerated erasures ≠ time to restore erasure margin.**

### J.3 Case 95 — RAID-Z write geometry

Case 95's bounded RAID-Z mechanism depends on variable-width stripes. dRAID's released rebuild source says fixed width is necessary for its sequential reconstruction.

Therefore:

**one geometry can close one retention problem while obstructing another recovery optimization.**

This is an engineering comparison, not a historical contradiction.

### J.4 Case 18 — scrub/integrity

Sequential reconstruction can restore coded redundancy without block checksums in the first phase. Case 18's checksum-qualified scrub machinery is therefore not redundant with Case 96.

The two form a deliberately staged relation:

**restore redundancy first; revalidate integrity second.**

## K. Related-repository duplication check

The current `tmzncty/computing-archaeology` index covers delay lines, Williams tubes, core, tape, RAMAC/direct-access disk, and identifies storage/controller history as an area for further deepening, but it does not contain a dRAID case in the current repository search/index.

Resulting boundary:

- Case 96 may retain the dRAID-specific retention argument;
- full parity-declustering history, distributed-sparing genealogy, ZFS/RAID controller history, and product/implementation lineage should be built in `computing-archaeology` and linked back later.

## L. Rejected claims

The following claims are explicitly unsupported by this grounding record:

1. `dRAID invented parity declustering` — rejected by 1992 prior art.
2. `dRAID invented distributed sparing` — rejected by the 1994 dissertation and its cited earlier studies.
3. `dRAID invented sequential RAID reconstruction` — rejected; released source itself compares the method to traditional RAID rebuild.
4. `dRAID is always four times faster` — rejected; PR #10102 numbers are configuration/workload-specific.
5. `same parity count means same durability` — rejected as an oversimplification; degraded-window duration and failure model also matter, though this case does not calculate universal probabilities.
6. `faster rebuild proves block integrity` — rejected; sequential reconstruction does not verify block checksums in the first phase.
7. `distributed spare = extra complete replica` — rejected.
8. `fixed stripe width is universally better than variable RAID-Z width` — rejected; the geometries serve different constraints.
9. `dRAID eliminates URE and correlated-failure risk` — rejected; those remain separate failure models.
10. `current OpenZFS documentation proves every detail of the 2017 prototype` — rejected.
11. `hard-coded permutation maps are user payload` — rejected; they are interpretation/compatibility infrastructure.
12. `parity declustering paper proves direct OpenZFS lineage` — rejected; it establishes prior art, not genealogy.

## M. Evidence-strength conclusion

The bounded case reaches `grounded` because the central chain is supported by multiple primary project records and earlier high-quality prior art:

- the 2021 release provides the production anchor;
- PR #10102 documents the accepted feature and bottleneck rationale;
- `vdev_draid.c` establishes distributed redundancy/spare mapping and compatibility constraints in the released source;
- `vdev_rebuild.c` explicitly establishes fixed-width sequential reconstruction, first-phase checksum limits, redundancy restoration, and follow-up scrub;
- the 2017 wiki preserves earlier project vocabulary and mechanism state;
- current docs are used only as later institutional explanation;
- CMU's 1992–1994 work blocks false novelty claims about parity declustering and distributed sparing.

That evidence is sufficient for the narrow retention conclusion:

> In OpenZFS dRAID, the duration of reduced redundancy is partly a property of retained layout, distributed transition capacity, and recovery traversal—not merely of parity count—while rapid first-phase redundancy restoration remains distinct from later checksum-qualified integrity validation.
