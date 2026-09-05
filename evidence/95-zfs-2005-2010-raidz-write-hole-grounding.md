# Grounding record — Case 95: ZFS RAID-Z dynamic stripes and write-hole avoidance

**Case:** [`cases/95-zfs-raidz-dynamic-stripe-write-hole.md`](../cases/95-zfs-raidz-dynamic-stripe-write-hole.md)  
**Status:** `grounded`  
**Bounded window:** 2005–2010 for the historical/institutional mechanism; current OpenZFS only as a later witness.

## Research question

What primary/institutional evidence is sufficient to support the narrow claim that RAID-Z avoids the traditional fixed-stripe partial-update write hole by composing:

1. ZFS copy-on-write transactional state;
2. variable-width RAID-Z stripes;
3. full-stripe writes for each RAID-Z block; and
4. filesystem/device metadata that can interpret the variable redundancy geometry?

The record also asks what that mechanism **does not** prove about latest-write durability, silent corruption, device caches, priority, or all later RAID-Z implementations.

## Evidence classification

| Source | Date / release | Class | What it is used for | What it is not used for |
| --- | --- | --- | --- | --- |
| Solaris Express Developer Edition, `The ZFS File System` | ZFS new in Solaris Express 12/05 | `H/P` official period release documentation | ZFS release anchor; transactional/copy-on-write institutional vocabulary | exact source-code path, universal priority |
| Solaris ZFS Administration Guide, `RAID-Z Storage Pool Configuration` | 2000s/2010 surviving Sun/Oracle guide chain | `H/P` official institutional technical documentation | traditional write-hole description; variable-width stripes; all writes full-stripe; metadata/redundancy integration | proof of every implementation detail or historical first |
| Solaris ZFS Administration Guide, `Transactional Semantics` | 2000s/2010 guide chain | `H/P` official institutional technical documentation | COW; committed-or-ignored filesystem state; explicit newest-data-loss boundary | claim that every returned async write is durable |
| OpenZFS `RAIDZ` / COW docs | current | `P/S` later institutional witness | terminology continuity and modern explanatory check | exact evidence for 2005 code |
| OpenZFS `vdev_raidz.c` | current | `P` implementation witness | confirms RAID-Z remains explicit mapping/reconstruction machinery | historical identity with the first Solaris implementation |
| Gary Bannister preservation of Bonwick weblog quotation | 2006-06-01 | `S/H` period corroboration with provenance limit | corroborates dynamic-width / per-block stripe / metadata-reconstruction explanation | substitute for a directly retrieved original Sun weblog page |

## A. Period release anchor — Solaris Express 12/05

Oracle's surviving `Solaris Express Developer Edition What's New` page states that ZFS was new in the Solaris Express **12/05** release and describes the filesystem as providing transactional semantics and end-to-end integrity. It says operations are `copy-on-write` transactions and presents the on-disk state as valid across that transaction model.

Stable page:

- <https://docs.oracle.com/cd/E19957-01/820-0724/gbjpv/index.html>

### Supported claims

- `ZFS in Solaris Express 12/05` is a defensible period release anchor.
- `copy-on-write` and `transactional` are actor/institutional vocabulary, not project inventions.
- the bounded design already presents state replacement rather than ordinary in-place overwrite as a core filesystem relation.

### Limits

The page's broad marketing phraseology around corruption/integrity is **not** promoted into a universal hardware guarantee. This grounding record relies on the more precise administration-guide text below for write-hole and durability boundaries.

## B. Primary institutional mechanism — RAID-Z storage-pool documentation

The Sun/Oracle Solaris ZFS Administration Guide section on RAID-Z describes the conventional parity update problem and RAID-Z's response. The relevant surviving guide pages include:

- OpenSolaris-era guide: <https://docs.oracle.com/cd/E19120-01/open.solaris/817-2271/gavwn/index.html>
- parallel Solaris ZFS guide edition: <https://docs.oracle.com/cd/E19253-01/819-5461/gamtu/index.html>
- later Oracle Solaris documentation retaining the same mechanism statement: <https://docs.oracle.com/en/operating-systems/solaris/oracle-solaris/11.4/manage-zfs/raid-z-storage-pool-configuration.html>

### B.1 Traditional write-hole boundary

The guide describes a RAID-5-like partial-stripe update in which power loss before all corresponding blocks are written can leave parity out of synchronization with the data.

This supports:

**physically surviving data/parity pieces ≠ one trustworthy current stripe relation.**

It does not claim that every RAID implementation has the same controller/cache failure behavior.

### B.2 Variable width and full-stripe writes

The guide says RAID-Z uses **variable-width RAID stripes** so that **all writes are full-stripe writes**.

This is the central historical/institutional mechanism anchor for Case 95.

The correct bounded reading is:

- stripe width can vary with the RAID-Z block/layout;
- the write is complete relative to that block's chosen data/parity geometry;
- `full-stripe` must not be silently normalized into `always touches every member of the vdev at one fixed width`.

### B.3 Integrated metadata is part of the mechanism

The same guide explicitly says the variable-width design is possible because ZFS integrates filesystem and device management so that filesystem metadata contains enough information about the underlying redundancy model to handle those stripes.

This supports the project engineering reconstruction:

**surviving coded bytes ≠ sufficient reconstruction if the stripe-geometry interpretation relation is lost.**

The project term `interpretive geometry state` is not attributed to the guide.

### B.4 Priority language rejected

Some later Oracle editions add a statement that RAID-Z was the world's first software-only solution to the RAID-5 write hole.

This evidence record deliberately marks that as **not adopted as a universal historical-priority conclusion**. Proving such a priority would require a dedicated comparison with earlier parity arrays, copy-on-write/log-structured filesystems, controller NVRAM/logging schemes, WAFL-like designs, and other write-hole closures.

## C. Transactional semantics — consistency is not latest-write durability

The Solaris ZFS Administration Guide `Transactional Semantics` page states that ZFS manages data through copy-on-write semantics, does not overwrite the current data in place, and treats an operation sequence as committed or ignored for filesystem consistency.

Stable page:

- <https://docs.oracle.com/cd/E19120-01/open.solaris/817-2271/gaypi/index.html>

Crucially, the same page says the **most recently written pieces of data might be lost** even while the filesystem remains consistent, and separately identifies synchronous data as having a stronger return-time guarantee.

This directly blocks an overclaim that would otherwise be tempting in a write-hole case:

**write-hole avoidance ≠ latest asynchronous write durability.**

It also preserves the lower-layer relevance of Cases 20 and 87: a filesystem consistency composition does not redefine volatile device/controller caches as nonvolatile.

## D. Current OpenZFS institutional witness

Current OpenZFS documentation retains the RAID-Z distinction:

- <https://openzfs.github.io/openzfs-docs/Basic%20Concepts/RAIDZ.html>
- <https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Copy-on-write.html>

The COW documentation separately describes the tree/block-pointer/uberblock relation and transaction groups. It is useful to explain why `old committed state remains reachable while new state is assembled`, but because it is current documentation it is labeled as a **later institutional witness**, not as evidence that every exact contemporary internal structure was identical in Solaris Express 12/05.

## E. Current source witness

OpenZFS current source:

- <https://github.com/openzfs/zfs/blob/master/module/zfs/vdev_raidz.c>

The file is used only to establish that RAID-Z today still has explicit mapping/reconstruction machinery rather than being a documentation-only abstraction. Modern expansion/reflow code and current implementation details are outside the historical claim.

No statement in Case 95 uses current source to date a mechanism to 2005.

## F. Bonwick 2006 quotation — useful but provenance-bounded

A 1 June 2006 page by Gary Bannister preserves and links a quotation from Jeff Bonwick's then-live Sun weblog discussion of RAID-Z:

- <https://bannister.us/weblog/2006/understanding-raid-z>

The preserved quotation describes:

- RAID-Z as a data/parity scheme with dynamic stripe width;
- each block as its own RAID-Z stripe;
- every RAID-Z write as a full-stripe write;
- the combination with ZFS copy-on-write transactional semantics;
- reconstruction as requiring filesystem metadata to determine varying RAID-Z geometry.

The original linked Sun URL (`blogs.sun.com/bonwick/entry/raid_z`) is no longer treated here as a stable directly inspected source. Therefore this witness is useful for **period corroboration and vocabulary**, but all central bounded claims are independently supported by surviving official Oracle/Sun documentation.

## G. Related-repository duplication check

GitHub repository search in `tmzncty/computing-archaeology` for:

- `RAID-Z`
- `ZFS`

returned no existing case/source package at the time of this grounding pass.

Resulting boundary:

- Case 95 may retain the RAID-Z-specific retention argument;
- a broader history of ZFS, WAFL/COW ancestry, parity-array genealogy, RAID-Z2/3/dRAID, and controller/product evolution should be built in `computing-archaeology` rather than duplicated here.

## H. Cross-case closure

### H.1 Case 88 — Linux MD PPL

Case 88 logs bounded partial-parity recovery evidence before releasing an otherwise non-atomic standing RAID5 update.

Case 95 instead grounds a different composition:

- old committed ZFS tree remains separately admissible under COW;
- the new block is allocated as a complete variable-width RAID-Z stripe;
- metadata carries the interpretation relation needed for that variable geometry.

Therefore:

**write-hole problem class similarity ≠ recovery-mechanism identity.**

### H.2 Case 94 — RAID-6 P+Q

Case 94 adds a second independent syndrome and asks which known missing contributions can be reconstructed. It explicitly shows that stronger coding does not itself provide crash-atomic currentness.

Case 95 is therefore orthogonal:

**more parity equations ≠ write-hole avoidance.**

### H.3 Case 18 — ZFS scrub

Case 18 handles checksums, proactive verification, alternate-copy repair, and scrub/resilver distinction.

Case 95 does not reuse those integrity operations as an explanation of write-hole avoidance. A stripe can be laid out transactionally and still require checksums to diagnose later silent corruption.

### H.4 Case 87 — SCSI write-back cache

Case 87 demonstrates that command completion can precede physical-medium currentness. Therefore Case 95 explicitly leaves lower-layer persistence semantics intact:

**filesystem-level COW/full-stripe composition ≠ device-cache nonvolatility.**

## I. Rejected claims

The following claims are explicitly unsupported by this grounding record:

1. `RAID-Z invented full-stripe writing` — rejected; full-stripe parity updates predate ZFS.
2. `RAID-Z invented copy-on-write` — rejected.
3. `RAID-Z is proven here to be the first solution to the RAID-5 write hole` — rejected; vendor priority language is not a genealogy.
4. `every RAID-Z write uses every disk in the vdev` — rejected; variable stripe width is the mechanism under study.
5. `no write hole means the latest async write survives a crash` — rejected by Solaris transactional-semantics documentation.
6. `RAID-Z makes volatile drive caches irrelevant` — rejected; lower-layer durability remains a separate relation.
7. `RAID-Z write-hole avoidance detects all silent corruption` — rejected; checksum/integrity authority is separate and handled in Case 18.
8. `old COW blocks are securely erased once superseded` — rejected; logical currentness/reclamation is not sanitization.
9. `current OpenZFS source proves exact Solaris Express 12/05 internals` — rejected.
10. `Bonwick's original Sun weblog was directly inspected in this pass` — rejected; only a period preservation/quotation plus official surviving documentation were inspected.

## J. Evidence-strength conclusion

The bounded mechanism is sufficiently grounded because the core chain does not depend on a secondary reconstruction:

- official Solaris release documentation anchors period ZFS/COW/transactional vocabulary;
- official Sun/Oracle administration documentation directly states the write-hole problem, RAID-Z variable-width/full-stripe response, and metadata/redundancy integration;
- official transactional documentation independently blocks the durability overclaim;
- current OpenZFS documentation/source is used only as a later witness;
- the surviving Bonwick quotation is explicitly provenance-bounded and nonessential to the central claim.

That is enough for `grounded` status while leaving broader genealogy and implementation archaeology open.
