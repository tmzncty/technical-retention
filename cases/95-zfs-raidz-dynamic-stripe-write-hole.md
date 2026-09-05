# ZFS RAID-Z: Dynamic-Width Full-Stripe Writes and Write-Hole Avoidance

**Status:** `grounded`

## Scope

This case asks one bounded question:

> How does RAID-Z change the retained relation around parity updates so that a crash does not leave one logical RAID-Z block represented by a half-updated data/parity stripe?

The historical/mechanism window is deliberately narrow:

- ZFS as shipped in the Solaris Express 12/05 line, where Sun described the filesystem as transactional and copy-on-write;
- Sun/Oracle ZFS administration documentation from the 2000s–2010 period describing RAID-Z's variable-width stripes, full-stripe writes, metadata integration, and RAID-5 write-hole boundary;
- current OpenZFS documentation/source only as a later implementation/institutional witness where useful.

This is **not** a general history of ZFS, RAID-Z2/3, RAID-Z expansion, RAID-Z mathematics, checksumming, scrub/resilver, ZIL/SLOG, snapshots, dRAID, or storage-controller cache durability. Case 18 already treats ZFS scrub/self-healing; Case 20/87 treat lower-layer flush/FUA/cache commitment; Case 88 treats Linux MD Partial Parity Log as a different write-hole closure strategy; Case 94 treats two-known-erasure P+Q reconstruction.

A search of `tmzncty/computing-archaeology` found no existing `RAID-Z`/`ZFS` case to reuse. Broader engineering genealogy remains better placed there.

## Evidence labels and vocabulary

Historical/institutional vocabulary used by the sources:

- `copy-on-write`;
- `transactional`;
- `RAID-Z`;
- `RAID-5 write hole`;
- `variable-width RAID stripes`;
- `full-stripe writes`;
- filesystem `metadata` describing the underlying redundancy model.

Project engineering vocabulary used here:

- **geometry-qualified parity** — parity is usable only together with the stripe geometry to which it belongs;
- **layout-mediated write-hole avoidance** — avoiding an in-place partial-stripe update by changing how a logical write is laid out, rather than first logging enough old/new parity evidence to repair a torn update;
- **interpretive geometry state** — retained metadata needed to recover which device columns/width belong to a particular logical RAID-Z block.

These project terms are `E`; they are not retroactively attributed to Sun engineers as historical wording.

## Historical record

### H/P — Solaris Express 12/05: ZFS arrives as a transactional copy-on-write filesystem

Oracle's surviving Solaris Express release documentation dates ZFS to the **12/05** release and describes its operations as `copy-on-write` transactions with on-disk state kept valid.

This matters for the bounded RAID-Z problem because the old reachable tree is not overwritten in place while a new version is being assembled. The case does **not** infer from this that every latest application write is already durable: later Solaris documentation explicitly allows recently written asynchronous data to be lost while keeping the filesystem state consistent.

### H/P — Sun/Oracle administration documentation names the traditional write hole

The Solaris ZFS Administration Guide describes the conventional RAID-5-like failure mode directly: when only part of a parity stripe is updated and power is lost before all corresponding blocks reach disk, data and parity can cease to describe one coherent stripe state.

The same guide says RAID-Z uses **variable-width RAID stripes so that all writes are full-stripe writes**. It further says this design depends on ZFS integrating filesystem and device management so filesystem metadata carries enough information about the underlying redundancy model to handle those variable-width stripes.

For this case, that is the primary institutional mechanism claim.

### H/P — `full-stripe` does not mean `every disk in the vdev for every logical block`

The administration-guide wording is easy to misread if imported into fixed-width RAID intuition. RAID-Z's stripe width is variable. A logical block is laid out as the complete data-plus-parity stripe appropriate to that block; the width need not equal a single globally fixed stripe width for every block.

Current OpenZFS documentation preserves the same distinction: RAID-Z is described as a distributed-parity vdev with non-constant stripe width and no RAID-5 write hole.

Thus:

**RAID-Z full-stripe write ≠ fixed-width all-member write for every block.**

### H/P — filesystem metadata participates in reconstruction

The Sun/Oracle documentation does not describe variable geometry as self-evident from parity bytes alone. It explicitly ties the design to integrated filesystem/device management and metadata knowledge of the redundancy model.

A surviving 2006-era quotation of Jeff Bonwick's `RAID-Z` weblog likewise describes reconstruction as requiring traversal of filesystem metadata because stripes have different sizes. Because the original Sun weblog URL is not currently a stable first-party page, this case uses that quotation only as a period corroborating witness, not as the sole primary anchor.

The stronger claim retained here is already supported by the official administration guide:

**retained parity/data bytes ≠ sufficient interpretation when the stripe geometry relation is unknown.**

## Retained state

For the bounded write-hole relation, later valid service can depend on retaining:

1. the data components of the committed RAID-Z block;
2. its parity component(s);
3. filesystem block-pointer/tree state that identifies the committed block;
4. enough allocation/redundancy metadata to interpret that block's variable-width RAID-Z geometry;
5. a valid committed filesystem root / transaction state selecting the new tree rather than an incomplete construction;
6. lower-layer device state sufficient to make the writes that ZFS treats as committed actually survive the failure model in question.

Items 3–6 are not ordinary user payload. They are constitutive interpretation, currentness, and durability relations around the coded block.

## Physical / logical substrate

The bounded substrate is layered:

- user-visible logical file/object state;
- ZFS block tree and block pointers;
- RAID-Z logical block split into data/parity columns;
- physical device sectors beneath those columns;
- optional volatile controller/device caches beneath the filesystem's view.

The case therefore rejects a one-layer statement such as `the parity survived, so the file survived`.

## Retention mechanism

### Copy-on-write preserves an old admissible tree while the new tree is constructed

Sun/Oracle documentation states that ZFS does not overwrite the existing data in place for the transactional update. New state is written elsewhere and the operation is either committed or ignored at the filesystem level.

Engineering reconstruction (`E`): this removes one common need to repair an old fixed stripe that has been partially overwritten into a mixed old/new state, because the old committed embodiment remains separately admissible until the new one is selected.

### Variable-width RAID-Z turns each bounded logical write into its own complete parity relation

Rather than updating a subset of one fixed-width standing RAID-5 stripe through a read-modify-write transition, RAID-Z chooses a stripe geometry for the block being written and writes the corresponding data/parity relation as a whole logical stripe.

This is **layout-mediated write-hole avoidance** (`E`). It is not the same mechanism as Case 88 PPL, which retains explicit temporary recovery evidence before releasing an otherwise non-atomic RAID5 update.

### Metadata preserves how to interpret the variable stripe

Because width is not globally fixed, the system must retain enough metadata to know the redundancy/layout relation used by the block. This makes a metadata relation part of parity recoverability.

**parity retention ≠ geometry retention.**

## Addressing and access geometry

An application does not address parity columns directly. ZFS resolves a logical object through the filesystem tree to block pointers and then into the appropriate vdev/RAID-Z layout.

The variable stripe is therefore not merely a physical arrangement; it is recovered through retained higher-level metadata.

A block can keep one logical identity while its physical allocation and column geometry are determined by the integrated allocator/vdev machinery.

## Read semantics

Ordinary reads are not the focus of this case. Case 18 already treats checksum verification, scrub, alternate-copy selection, and self-healing.

The bounded point is interpretive: reconstruction after a missing/corrupt contribution requires the system to know the block's RAID-Z geometry. Readability of individual sectors does not by itself re-establish that relation.

## Write and erasure semantics

### New writes do not require in-place partial-stripe overwrite of an old RAID-Z block

Copy-on-write allocates a new representation. Variable-width RAID-Z then gives that block a complete coded stripe relation.

### Retirement of the old tree is distinct from secure erasure

Once a newer transaction is committed and older blocks become unreachable/reclaimable, their loss of current filesystem authority is not evidence that raw sectors have been securely sanitized. Case 44/47 cover stronger deletion/sanitization questions.

## Time

The important timescales are relational rather than a media-retention lifetime:

- interval while a transaction group / new tree is being assembled;
- device-write and cache-persistence intervals below ZFS;
- later allocation/reclamation of blocks that have lost current-tree authority;
- scrub/resilver schedules, which remain outside this bounded case.

A crash during the first interval can reject the incomplete new state and fall back to the last committed tree; this does not imply that the newest application-visible asynchronous mutation had already become durable.

## Maintenance and labor

The apparent simplicity of `no write hole` depends on continuing hidden work:

- allocation of new blocks rather than in-place overwrite;
- parity calculation for the chosen RAID-Z width;
- maintenance of block pointers and redundancy/layout metadata;
- transaction-group synchronization / root selection;
- lower-layer write ordering and power-loss durability contracts;
- later space reclamation.

RAID-Z therefore does not eliminate maintenance; it changes what must be maintained.

## Failure / forgetting modes

### Traditional partial-stripe write hole

Data/parity pieces can survive individually yet no longer belong to one current stripe state.

### Geometry loss

Data and parity can physically survive while the metadata needed to interpret their variable-width relation is unavailable or corrupt.

### Lower-layer durability failure

A filesystem-level transaction/layout algorithm cannot make volatile device/controller state nonvolatile by definition. Case 87's cache/media boundary remains applicable below ZFS.

### Latest-write loss without structural inconsistency

Solaris documentation explicitly distinguishes filesystem consistency from preservation of the most recently written asynchronous data. Therefore:

**write-hole avoidance ≠ latest-write durability.**

### Silent corruption

RAID-Z write-hole avoidance does not itself prove which present-looking column is wrong. ZFS checksums/scrub/self-healing supply a separate integrity relation, handled in Case 18.

## Engineering reconstruction

The bounded relation can be expressed as follows:

1. preserve the old committed tree while computing a new version;
2. allocate a complete RAID-Z stripe geometry for each new logical block rather than overwrite only part of an old fixed stripe;
3. calculate and issue the data/parity components for that new stripe;
4. retain metadata sufficient to locate and interpret the new geometry;
5. make the new tree authoritative only through the transaction/commit relation;
6. later reclaim no-longer-authoritative blocks according to ordinary ZFS allocation rules.

The retention result is not `nothing ever becomes partial`. Physical device I/O can still be in flight. The stronger and source-supported claim is that an interrupted update need not leave the **authoritative logical block** represented as a fixed stripe whose standing data and parity have been partially overwritten into a mixed currentness state.

## Functional analogy

### Case 88 — Linux MD Partial Parity Log

`A/E`: both address the RAID write-hole class, but the retained evidence differs.

- PPL keeps bounded temporary recovery evidence before a non-atomic standing-stripe update;
- RAID-Z changes the update/layout composition so the new logical block is a complete dynamic stripe under copy-on-write metadata.

No Linux→ZFS or ZFS→Linux genealogy is implied.

### Case 94 — RAID-6 P+Q

`A`: more parity equations increase known-erasure reconstruction margin; they do not by themselves make updates crash-atomic. RAID-Z's write-hole avoidance is about update/layout/currentness, not simply parity count.

### Case 16 — FFS soft updates

`A`: both preserve crash-admissible filesystem state without equating that with latest-write durability, but soft updates constrain in-place metadata ordering while ZFS uses copy-on-write transactional replacement. They are different mechanisms.

### Case 87 — SCSI cache durability

`A`: a correctly composed filesystem/RAID transaction can still depend on whether the lower device has made accepted writes power-loss persistent. Interface durability and layout consistency are orthogonal relations.

## Prior art and genealogy boundary

### Full-stripe writes and parity RAID predate RAID-Z

Traditional RAID literature already distinguishes read-modify-write from full-stripe/reconstruct-write behavior. This case therefore does not claim that Sun invented the idea of writing a complete parity stripe.

### Copy-on-write predates ZFS

Copy-on-write is older than ZFS. The historical claim here is the bounded ZFS composition of copy-on-write transactional filesystem state with variable-width RAID-Z layout, not invention of copy-on-write itself.

### Do not promote vendor priority language into universal history

Some later Oracle documentation calls RAID-Z the first software-only solution to the RAID-5 write hole. This case does **not** adopt that sentence as proven universal invention priority. Establishing priority across parity arrays, WAFL-style filesystems, log-structured systems, and controller designs requires a dedicated genealogy in `computing-archaeology`.

## Philosophical / media-theoretical interpretation

`I` — RAID-Z sharpens the repository's distinction between **material survival** and **admissible continuation**. A collection of surviving sectors is not yet a recoverable block if the relation that says how those sectors form one variable-width coded object has been lost.

`I` — It also supplies a useful counterexample to the intuition that preservation always means keeping *more recovery history*. One way to survive interruption is to retain a repair record; another is to organize mutation so an older admissible embodiment remains intact until a new complete relation becomes authoritative.

These are project interpretations, not claims attributed to Sun/Oracle engineers as philosophical theses.

## Counterexamples and limits

This case does **not** establish:

- that every RAID-Z generation or OpenZFS implementation has identical write-path details;
- that all ZFS writes are immediately durable when an application call returns;
- that device volatile write caches are irrelevant;
- that a `full-stripe write` necessarily touches every device in a vdev;
- that RAID-Z eliminates silent corruption without the separate checksum/integrity machinery;
- that single-parity RAID-Z has RAID-Z2/3 failure tolerance;
- that RAID-Z invented parity RAID, full-stripe writes, copy-on-write, transactional filesystems, or write-hole repair;
- that old COW blocks are securely erased when they cease to be current.

## Related repositories

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — no current RAID-Z/ZFS case found in the repository search; broader ZFS/RAID genealogy and implementation history should go there rather than be duplicated here.
- [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) — useful if later work asks when `write hole`, `transactional`, or `copy-on-write` became the actors' own problem vocabulary rather than a retrospective category.

## Claim ledger

| Claim | Label | Support | Limit |
| --- | --- | --- | --- |
| Solaris Express 12/05 shipped ZFS and described it as transactional/copy-on-write | `H/P` | Oracle Solaris Express release documentation | release/institutional statement, not invention priority |
| traditional partial parity updates can leave data/parity inconsistent after power loss | `H/P` | Solaris ZFS Administration Guide RAID-Z section | bounded write-hole model |
| RAID-Z uses variable-width stripes so writes are full-stripe writes | `H/P` | Sun/Oracle administration guide; current OpenZFS documentation | does not mean fixed all-device width |
| integrated filesystem/device metadata is needed to handle variable stripe geometry | `H/P/E` | Sun/Oracle administration guide | does not prove every internal metadata field |
| RAID-Z write-hole avoidance differs from PPL logging | `E/A` | Case 88 comparison | functional comparison, no genealogy |
| no write hole does not guarantee newest async write durability | `H/P/E` | Solaris transactional-semantics documentation | consistency and durability separated |
| geometry metadata can be constitutive retention state | `E` | variable-width + metadata requirement | project reconstruction |
| RAID-Z does not prove universal priority for write-hole elimination | `X` | scope/prior-art discipline | genealogy left open |

## Sources

### Primary / period institutional

1. Sun/Oracle, **Solaris Express Developer Edition — The ZFS File System**, identifying ZFS as new in Solaris Express 12/05 and describing copy-on-write transactional operation.
   - <https://docs.oracle.com/cd/E19957-01/820-0724/gbjpv/index.html>

2. Sun/Oracle, **Solaris ZFS Administration Guide — RAID-Z Storage Pool Configuration**, surviving 2000s/2010 documentation of the RAID-5 write hole, variable-width RAID-Z stripes, full-stripe writes, and integrated filesystem/device metadata.
   - <https://docs.oracle.com/cd/E19120-01/open.solaris/817-2271/gavwn/index.html>
   - parallel later edition: <https://docs.oracle.com/cd/E19253-01/819-5461/gamtu/index.html>

3. Sun/Oracle, **Solaris ZFS Administration Guide — Transactional Semantics**, copy-on-write and the explicit boundary that the most recently written data may be lost even while on-disk filesystem state remains consistent.
   - <https://docs.oracle.com/cd/E19120-01/open.solaris/817-2271/gaypi/index.html>

### Later institutional / implementation witnesses

4. OpenZFS documentation, **RAIDZ**, current institutional description of variable/non-constant stripe width and write-hole avoidance.
   - <https://openzfs.github.io/openzfs-docs/Basic%20Concepts/RAIDZ.html>

5. OpenZFS documentation, **Copy-on-Write**, current explanation of block-tree replacement, uberblock reachability, and transaction groups. Used as a later explanatory witness, not evidence for the exact 2005 implementation.
   - <https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Copy-on-write.html>

6. OpenZFS, **`module/zfs/vdev_raidz.c`**, current source snapshot used only as an implementation witness for RAID-Z mapping/reconstruction machinery.
   - <https://github.com/openzfs/zfs/blob/master/module/zfs/vdev_raidz.c>

### Period corroborating witness with provenance limit

7. Gary Bannister, **“Understanding RAID-Z,”** 1 June 2006, preserving a quotation and link to Jeff Bonwick's then-live Sun weblog discussion of dynamic stripe width and metadata-dependent reconstruction. Used only as corroboration because the original Sun weblog page is no longer a stable first-party source here.
   - <https://bannister.us/weblog/2006/understanding-raid-z>

## Open work kept outside this case

- original Sun/OpenSolaris RAID-Z source snapshot and code-history archaeology;
- exact Bonwick weblog archival recovery and page-level provenance;
- WAFL/log-structured/COW parity-array prior-art genealogy;
- RAID-Z2/RAID-Z3/dRAID mathematics and fault models;
- modern RAID-Z expansion/reflow semantics;
- ZIL/SLOG and synchronous-write semantics;
- lower-layer flush/FUA/drive-cache fault injection;
- named-production-system crash testing;
- secure deletion/forensic behavior of retired COW blocks.

Those are separate research slices rather than blockers for the bounded mechanism claim established here.
