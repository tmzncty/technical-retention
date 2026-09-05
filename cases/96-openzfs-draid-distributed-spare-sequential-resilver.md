# OpenZFS dRAID: Distributed Spare Capacity, Sequential Resilver, and the Duration of Reduced Redundancy

**Status:** `grounded`

## Scope

This case asks one bounded question:

> How does OpenZFS dRAID change the *time required to restore redundancy after a device failure*, and what retention tradeoff follows from using distributed spare capacity plus sequential reconstruction?

The historical/mechanism window is deliberately narrow:

- OpenZFS dRAID design documentation preserved in the project wiki in 2017;
- the accepted dRAID feature work merged in 2020;
- the released OpenZFS 2.1.0 implementation and release record from 2 July 2021;
- current OpenZFS documentation only as a later institutional explanation where it clarifies the surviving design.

This is **not** a general history of RAID, parity declustering, ZFS, RAID-Z2/3, storage-array rebuild algorithms, URE modeling, fault-domain-aware dRAID width, or modern OpenZFS expansion. Case 17 already handles generic parity reconstruction and degraded repair; Case 18 handles ZFS checksum scrub/self-healing; Case 94 separates parity count from corruption diagnosis; Case 95 handles RAID-Z write-hole avoidance and variable-width stripes.

A search of `tmzncty/computing-archaeology` found no existing dRAID case to reuse. Broader parity-declustering, distributed-sparing, RAID controller, and ZFS implementation genealogy belongs there rather than being recreated here.

## Evidence labels and vocabulary

Historical/project vocabulary used by the primary sources:

- `dRAID` / `Distributed Spare RAID`;
- `distributed hot spare`;
- `sequential reconstruction`;
- `device rebuild`;
- `healing reconstruction` / `healing resilver`;
- `fixed stripe width`;
- `permutation mapping`;
- `restore full parity` / `restore full redundancy`;
- `scrub` after sequential reconstruction.

Project engineering vocabulary used here:

- **redundancy-restoration interval** — the period between entering a degraded state and regaining the redundancy margin required by the bounded failure model;
- **repair-parallelism state** — layout/mapping/spare organization that determines how much surviving-device bandwidth can participate in reconstruction;
- **transition capacity** — capacity reserved not as an ordinary current payload copy, but to receive reconstructed state during failure recovery;
- **two-phase confidence restoration** — first restore coded redundancy quickly, then separately perform checksum-qualified verification.

These project terms are `E`; they are not retroactively attributed to the OpenZFS developers as their historical wording.

## Historical record

### H/P — dRAID was released as a major OpenZFS 2.1.0 feature

The OpenZFS 2.1.0 release, published on **2 July 2021**, lists `Distributed Spare RAID (dRAID)` as a major new feature. The release describes it as a distributed RAID-Z variant with integrated hot spares intended to reduce resilver time so that full redundancy can be restored in a fraction of the time required by a conventional full-disk replacement.

This release anchor establishes the bounded production-era claim. It does not establish invention priority for parity declustering, distributed sparing, or sequential rebuild.

### H/P — the merged feature proposal makes the bottleneck explicit

OpenZFS PR #10102, opened in March 2020 and merged on **13 November 2020**, describes the new top-level `draid` vdev type and states the central recovery objective: allow all dRAID children to participate when rebuilding to a distributed spare.

Its 90-HDD, 16-TB-drive example reports approximately 30 hours for a traditional hot-spare reconstruction constrained by the replacement drive's write bandwidth, versus roughly 7–8 hours with the default distributed-spare configuration used in that test. The exact numbers are workload/configuration-specific; this case uses them only as an implementation-development witness for the claimed bottleneck shift.

The stronger mechanism claim is independent of the benchmark number:

**spare capacity presence ≠ spare-path bandwidth.**

### H/P — released source distributes parity and spare participation

`vdev_draid.c` in the `zfs-2.1.0` tag describes dRAID as multiple RAID-Z redundancy groups spread across the dRAID children. A permutation mapping changes which physical children play each role so parity and reconstruction work are distributed rather than concentrated on a fixed neighborhood.

The same source states that reserving a fraction of each child's capacity creates virtual distributed spare devices and that the resulting all-child participation can substantially reduce the time needed to restore full parity after a disk failure.

This is the primary implementation anchor for **repair parallelism as a layout property**.

### H/P — fixed stripe width is deliberate recovery infrastructure

Released `vdev_rebuild.c` states that sequential reconstruction cannot be used on ordinary RAID-Z because RAID-Z has variable stripe width; dRAID avoids that limitation by using a **fixed stripe width**, at a usable-capacity cost.

This creates a direct boundary with Case 95:

- Case 95: variable-width RAID-Z is part of the write-hole-avoidance composition;
- Case 96: fixed-width dRAID is part of enabling LBA-ordered sequential reconstruction.

Neither width choice is simply `better`; each is tied to a different retention/recovery obligation.

### H/P — sequential reconstruction restores redundancy before checksum verification

`vdev_rebuild.c` explicitly distinguishes traditional `healing reconstruction` from `sequential reconstruction`.

Healing reconstruction follows block-aware data and can verify checksums as blocks are read and repaired, but tends toward less sequential I/O. Sequential reconstruction instead rebuilds in LBA order and **does not verify block checksums during that first phase**.

The source makes the tradeoff explicit: after sequential reconstruction completes, redundancy has been restored; a subsequent scrub is started by default to verify checksums. Thus the released implementation separates:

1. **restore redundancy margin quickly**;
2. **restore checksum-qualified confidence afterward**.

That distinction is central to this case.

### H/P — the 2017 project wiki preserves earlier terminology and the same tradeoff

A March 2017 revision of the OpenZFS dRAID HOWTO uses the term `rebuild` for the new sequential process. It contrasts a conventional RAID-Z example in which only one redundancy group plus one spare participate with a dRAID layout in which all surviving devices take part.

The same document says the rebuild scans space-map objects rather than the entire block-pointer tree, proceeds sequentially, can issue I/O spanning block boundaries, and cannot verify block checksums because it lacks the block pointers needed for that verification.

Current OpenZFS documentation mostly presents the operation as `sequential resilver`. The vocabulary changed; the bounded mechanism should not be rewritten as if every period used one term.

## Retained state

For this recovery relation, later durable service can depend on retaining more than the surviving user blocks themselves:

1. surviving data and parity contributions;
2. the dRAID redundancy-group geometry (`D`, `P`, children, distributed spare capacity);
3. deterministic permutation/mapping information needed to recover which physical children hold which logical group positions;
4. allocation/space-map state sufficient for sequential reconstruction of allocated regions;
5. on-disk rebuild progress/state so an interrupted recovery can be resumed or reasoned about;
6. enough spare transition capacity to receive reconstructed contributions;
7. checksum/block-pointer information for the later verification phase.

Items 2–7 are not ordinary user payload. They are recovery, interpretation, and confidence infrastructure.

## Physical / logical substrate

The bounded substrate is layered:

- logical ZFS blocks and block pointers;
- dRAID redundancy groups;
- parity/data roles distributed across physical child devices;
- distributed spare regions reserved across those devices;
- space maps and rebuild progress metadata;
- checksums used by later healing/scrub verification.

A failed leaf device therefore does not merely create `one missing disk`. It changes which retained relations are available and how rapidly the system can reconstruct the missing contribution.

## Retention mechanism

### Distributed sparing turns one replacement target into a many-device recovery surface

With a dedicated spare device, reconstruction can be constrained by the write bandwidth of that one target even if many surviving drives can supply data.

In dRAID, spare capacity is distributed across the children. Reconstruction traffic can therefore write into many physical devices while surviving devices simultaneously provide the source/parity reads.

Engineering reconstruction (`E`): the spare is not just a quantity of capacity; its **placement and parallel accessibility** are part of the retention mechanism.

### Parity declustering spreads reconstruction obligation

The permutation mapping prevents one fixed set of neighboring drives from bearing all reconstruction work for one failed child. Instead, redundancy groups are mixed across the vdev.

This turns recovery load distribution into retained layout structure.

### Fixed-width layout enables sequential first-phase recovery

Sequential reconstruction can scan allocated address ranges in LBA order, issue larger I/O spanning ZFS block boundaries, and avoid full block-tree traversal during the first phase.

That speed comes with a cost: without block pointers it cannot perform the ordinary per-block checksum verification during reconstruction.

### Scrub restores a different relation after redundancy is back

Once sequential reconstruction restores the missing coded contributions, OpenZFS can tolerate the next device failure according to the configured parity model again. A default follow-up scrub then verifies block checksums.

Thus:

**redundancy restored ≠ integrity fully revalidated.**

## Addressing and access geometry

Ordinary application addressing remains through ZFS logical blocks and the filesystem tree. dRAID recovery adds another geometry:

- redundancy groups have a fixed data+parity width;
- permutation maps spread group roles across all children;
- distributed spare regions supply recovery destinations;
- sequential reconstruction walks allocated LBA/space-map ranges rather than treating the block-pointer tree as the sole recovery traversal.

Recovery addressability is therefore not identical to ordinary logical read addressability.

## Read semantics

Ordinary reads are not the focus of this case.

During sequential reconstruction, readable surviving contributions are used to recreate missing data/parity at the device-address level. That use does not itself prove that every source block's checksum was verified in the same pass.

A later scrub/healing pass supplies the stronger block-pointer/checksum relation.

## Write and erasure semantics

The critical writes here are reconstruction writes into distributed spare capacity.

They are not ordinary application writes, and the distributed spare is not an independent user-visible replica. It is reserved transition capacity whose role changes when a leaf device is lost and reconstructed state is written there.

Replacing the failed physical device later can trigger a healing rebalancing/resilver back from distributed spare usage. Current OpenZFS documentation recommends a healing resilver for that rebalancing step because the pool is no longer in the same degraded urgency state and checksums can be verified during the move.

## Time

Time is the central retention dimension of this case.

After one device fails, a parity-protected vdev may still serve data, but its remaining failure margin is smaller. The period before reconstruction completes is therefore not merely a performance interval; it is a **redundancy-restoration interval** in which the admissible next-failure set is reduced.

Engineering reconstruction (`E`): if two layouts have the same nominal parity level but one can reconstitute the lost contribution substantially faster under the same workload/failure assumptions, they do not expose the retained object to the same *duration* of reduced redundancy.

This does not yield a universal durability number. Actual risk still depends on device failure rates, latent errors, workload, capacity, controller behavior, enclosure/failure domains, and which additional failures the configured code tolerates.

## Maintenance and labor

The apparently simple claim `faster resilver` depends on hidden maintenance work:

- generation and preservation of compatible permutation maps;
- allocation of distributed spare regions;
- tracking allocated space through space maps;
- scheduling sequential recovery I/O across many devices;
- persisting rebuild progress;
- monitoring failed-device/spare state;
- initiating a later scrub for checksum verification;
- replacing failed hardware and reclaiming distributed spare capacity.

The maintenance burden is changed, not eliminated.

## Failure / forgetting modes

### Dedicated-spare bottleneck

Adequate spare *capacity* can exist while the target device's write bandwidth keeps the array degraded for a long period.

### Mapping incompatibility

The released `vdev_draid.c` comments say the valid permutation maps are hard-coded and must never change because existing pools depend on the same mapping being regenerated to find the correct locations. A software change that preserved all payload sectors but changed that mapping relation could make the pool inaccessible.

Thus:

**physical block survival ≠ layout interpretability across software evolution.**

### Fast reconstruction without checksum verification

Sequential reconstruction can restore parity redundancy while carrying forward an undetected corrupt-but-readable source contribution. The automatic/default follow-up scrub exists because these are different confidence relations.

### Additional failure during the degraded interval

Faster recovery shortens the period of reduced margin; it does not abolish the possibility of another device failure before recovery completes.

### Correlated/failure-domain loss

A distributed layout does not automatically prove that arbitrary enclosure/rack/controller-correlated failures are tolerated. Modern dRAID failure-domain configuration is outside this historical 2017–2021 slice.

## Engineering reconstruction

The bounded retention relation can be expressed as:

1. a device failure removes one physical contribution from many dRAID redundancy groups;
2. the deterministic mapping identifies which surviving children contribute to each affected group;
3. distributed spare capacity provides recovery destinations spread over the vdev rather than one dedicated write target;
4. sequential reconstruction scans allocated regions in device/LBA order and reconstructs the missing contributions using many surviving devices;
5. after the first phase, the configured coded redundancy is restored;
6. a later scrub/healing phase re-enters block-pointer/checksum space to verify integrity.

This is **two-phase confidence restoration** (`E`): fast coded redundancy first, checksum-qualified validation second.

## Functional analogies

### Case 17 — generic RAID degraded repair

`A/E`: Case 17 establishes that parity can reconstruct missing contributions and that degraded service differs from restored redundancy. Case 96 adds a bounded mechanism for changing the *duration and bandwidth structure* of that transition.

No claim is made that dRAID changes the basic parity algebra itself.

### Case 94 — RAID-6 P+Q

`A`: parity count controls which known erasure combinations are algebraically recoverable. dRAID repair parallelism controls how rapidly a missing contribution can be rebuilt under a given parity configuration.

Therefore:

**redundancy margin ≠ redundancy-restoration speed.**

### Case 95 — RAID-Z dynamic-width write-hole avoidance

`A/E`: ordinary RAID-Z uses variable-width stripes as part of its write-path composition; released dRAID deliberately uses fixed stripe width to permit sequential reconstruction. This is a useful counterexample to the idea that one geometry is universally optimal.

### Case 18 — ZFS scrub

`A`: dRAID sequential reconstruction can restore redundancy without verifying block checksums in that phase; scrub supplies the later integrity qualification. Fast repair and checksum-qualified repair must remain distinct.

## Prior art and genealogy boundary

### Parity declustering predates dRAID

Mark Holland and Garth Gibson's 1992 ASPLOS paper, **“Parity Declustering for Continuous Operation in Redundant Disk Arrays,”** explicitly studied declustered parity as a way to distribute failure-recovery load and shorten recovery or preserve user throughput.

This case therefore does **not** claim OpenZFS invented parity declustering.

### Distributed sparing also predates OpenZFS dRAID

Mark Holland's 1994 CMU dissertation includes a chapter on **Distributed Sparing**, explicitly motivating the distribution of spare capacity across all disks instead of dedicating whole spare disks and combining that idea with parity declustering to remove the spare-device reconstruction bottleneck.

This case therefore does **not** claim OpenZFS invented distributed sparing.

### Sequential reconstruction is older than dRAID

The released OpenZFS source itself describes sequential reconstruction as behaving like a traditional RAID rebuild. The historical claim here is the specific OpenZFS composition and released format/implementation, not invention of sequential rebuild.

### Bounded novelty claim

The defensible historical statement is:

> OpenZFS dRAID 2.1.0 composes fixed-width declustered RAID-Z groups, deterministic permutation mappings, distributed spare capacity, and sequential reconstruction so that many devices can participate in restoring redundancy; it then separates that first-phase restoration from later checksum verification.

Broader genealogy remains a `computing-archaeology` task.

## Philosophical / media-theoretical interpretation

`I` — dRAID makes one usually hidden temporal fact unusually visible: **redundancy is not only a count of surviving copies/equations; after failure it is also a margin that must be reconstituted through time.**

`I` — Spare capacity can therefore be interpreted as *future transition capacity*: it is retained not because its present bytes are valuable user content, but because its availability and placement make a future recovery trajectory possible.

These are project interpretations. They are not claims that OpenZFS engineers used philosophical `retention` vocabulary.

## Counterexamples and limits

This case does **not** establish:

- that dRAID invented parity declustering, distributed sparing, or sequential rebuild;
- that every dRAID configuration is faster than every RAID-Z configuration;
- that the PR #10102 benchmark generalizes beyond its stated test pool;
- that faster resilvering changes the configured parity count;
- that restoring parity redundancy proves all reconstructed data is checksum-valid;
- that a distributed spare is an independent full replica;
- that dRAID eliminates latent sector errors, UREs, correlated failures, controller failures, or failure-domain design problems;
- that fixed stripe width is universally superior to RAID-Z variable width;
- that current OpenZFS terminology exactly matches the 2017 project wiki;
- that deterministic mapping constants are ordinary user payload;
- that faster repair alone yields a complete probabilistic durability model.

## Related repositories

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — no existing dRAID case found in the current index/search. Broader parity-declustering/distributed-sparing history, RAID controller genealogy, and ZFS implementation archaeology belong there.
- [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) — useful for a later study of when `rebuild`, `resilver`, `degraded`, `distributed spare`, and `continuous operation` became actors' own problem vocabularies.

## Claim ledger

| Claim | Label | Support | Limit |
| --- | --- | --- | --- |
| dRAID shipped as a major OpenZFS 2.1.0 feature on 2021-07-02 | `H/P` | OpenZFS 2.1.0 release | release anchor, not invention priority |
| dRAID spreads redundancy groups and spare capacity across children so many devices can participate in reconstruction | `H/P` | `vdev_draid.c`; PR #10102; project docs | bounded OpenZFS implementation |
| dRAID fixed stripe width enables sequential reconstruction that ordinary variable-width RAID-Z cannot use in this implementation | `H/P` | `vdev_rebuild.c`; OpenZFS docs | not a universal theorem about all RAID designs |
| sequential reconstruction restores redundancy before later checksum verification | `H/P/E` | `vdev_rebuild.c` | checksum confidence requires later scrub |
| repair bandwidth and degraded-window duration are retention-relevant even at unchanged parity count | `E` | mechanism reconstruction across Cases 17/94/96 | not a quantified universal durability probability |
| stable dRAID permutation mapping is required to interpret existing pools | `H/P/E` | `vdev_draid.c` comments | mapping compatibility is not user payload |
| parity declustering and distributed sparing predate dRAID | `H/S` | CMU 1992 paper; 1994 dissertation | no claim of direct code lineage |

## Sources

### Primary / project records

1. OpenZFS, **OpenZFS 2.1.0 release**, published 2 July 2021; dRAID listed as a major new feature.
   - <https://github.com/openzfs/zfs/releases/tag/zfs-2.1.0>

2. OpenZFS, **Distributed Spare (dRAID) Feature**, PR #10102, opened 4 March 2020, merged 13 November 2020.
   - <https://github.com/openzfs/zfs/pull/10102>

3. OpenZFS 2.1.0 source, `module/zfs/vdev_draid.c` — distributed groups, permutation mapping, distributed spare capacity, mapping-compatibility warning.
   - <https://github.com/openzfs/zfs/blob/zfs-2.1.0/module/zfs/vdev_draid.c>

4. OpenZFS 2.1.0 source, `module/zfs/vdev_rebuild.c` — sequential versus healing reconstruction, fixed-width dRAID boundary, checksum-verification limitation, automatic/default follow-up scrub.
   - <https://github.com/openzfs/zfs/blob/zfs-2.1.0/module/zfs/vdev_rebuild.c>

5. OpenZFS project wiki, **dRAID HOWTO**, revision edited 15 March 2017 — earlier `rebuild` terminology, space-map scan, sequential I/O, all-device participation, checksum limitation.
   - <https://github.com/openzfs/zfs/wiki/dRAID-HOWTO/001b44728e1ac3329a4d91be97bcd565a8f351b7>

6. OpenZFS documentation, **dRAID HOWTO** and `zpoolconcepts(7)` — current institutional description of distributed spare, fixed stripe width, sequential resilver, and rebalancing/healing distinction.
   - <https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Pool%20Structure/dRAID%20Howto.html>
   - <https://openzfs.github.io/openzfs-docs/man/master/7/zpoolconcepts.7.html>

### Earlier scholarly prior art

7. Mark Holland and Garth A. Gibson, **“Parity Declustering for Continuous Operation in Redundant Disk Arrays,”** ASPLOS V, 1992.
   - <https://www.cs.cmu.edu/~riedel/ftp/Declustering/ASPLOS.abstract.html>
   - preserved paper: <https://www.pdl.cmu.edu/PDL-FTP/Declustering/ASPLOS.pdf>

8. Mark Holland, **On-Line Data Reconstruction in Redundant Disk Arrays**, PhD dissertation, Carnegie Mellon University, CMU-CS-94-164, 1994; see Chapter 5, `Distributed Sparing`.
   - <https://www.pdl.cmu.edu/PDL-FTP/Declustering/Thesis.pdf>

9. Mark Holland, Garth A. Gibson, and Daniel P. Siewiorek, **“Fast, On-Line Failure Recovery in Redundant Disk Arrays,”** FTCS-23, 1993 — earlier reconstruction-algorithm work.
   - <https://www.pdl.cmu.edu/PDL-FTP/Declustering/FTCS.abstract.shtml>
