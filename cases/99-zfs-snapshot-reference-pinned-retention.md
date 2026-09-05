# ZFS Snapshots: Reference-Pinned Old Blocks, Rollback, and Deferred Reclamation

**Status:** `grounded`

## Scope

This case asks a bounded retention question:

> What changes when a copy-on-write filesystem deliberately keeps an older point-in-time tree reachable, so blocks that are no longer current in the live dataset cannot yet be reclaimed?

The ZFS evidence is bounded to Sun/Oracle ZFS snapshot documentation preserved in the **2010 Solaris ZFS Administration Guide**, with current OpenZFS documentation used only as continuity/context. Earlier **WAFL (1994)** is used as a prior-art floor for copy-on-write snapshots.

This case is not:

- a generic ZFS history;
- a second RAID-Z case (Case 95 already covers variable-width full-stripe writes and write-hole avoidance);
- a scrub/self-healing case (Case 18);
- a `zfs send` replication history;
- a clone genealogy;
- proof that ZFS invented filesystem snapshots or copy-on-write;
- evidence that `zfs destroy` securely sanitizes underlying sectors.

A repository search found no dedicated `ZFS snapshot` case in `tmzncty/computing-archaeology`; broader snapshot/COW genealogy belongs there if developed.

## Historical vocabulary

Historical / institutional vocabulary retained from the sources:

- `snapshot`;
- `read-only copy`;
- `referenced`;
- `used`;
- `copy-on-write`;
- `zfs destroy`;
- `zfs rollback`;
- `hold`;
- `user-reference count`;
- `defer_destroy`;
- `clone`.

Project engineering vocabulary:

- **reference-pinned retention** — an older block remains allocated because at least one admissible dataset/snapshot still references it;
- **reachability authority** — metadata/reference state deciding which tree may still name a block as part of an accessible dataset version;
- **reclamation eligibility** — whether an old allocation may return to the free-space pool;
- **forget request** — an administrative request such as snapshot destroy that can itself be blocked or deferred by other retained references.

The project terms are analytical reconstructions, not historical Sun/Oracle terminology.

## Historical record

### H/P — Solaris ZFS snapshots preserve old data by continued reference

The 2010 Solaris ZFS Administration Guide defines a snapshot as a read-only copy of a filesystem or volume. It says snapshot creation is nearly instantaneous and initially consumes no additional pool space. As the active dataset changes, the snapshot continues referencing the old data and thereby prevents the corresponding space from being freed.

This establishes the central retention mechanism without requiring a full duplicate of the dataset at snapshot time.

### H/P — one logical snapshot can be large while its initially unique physical charge is near zero

The same guide distinguishes a snapshot's `referenced` view from its `used` space. At creation, blocks are shared with the live filesystem and possibly other snapshots. As the live filesystem diverges, blocks can become unique to the snapshot and then count toward its `used` property.

Therefore:

> **logical historical coverage ≠ uniquely charged physical space.**

A snapshot can name a complete historical view while initially owning almost no blocks exclusively.

### H/P — retained references can block reclamation and even dataset destruction

The guide states that old data remains referenced by a snapshot and therefore cannot be freed. It also states that a dataset cannot be destroyed while snapshots exist, and that a snapshot with clones cannot simply be destroyed until the clone dependency is handled.

This is stronger than “old bytes happen to remain on disk.” The old blocks remain intentionally admissible because a live metadata relation still reaches them.

### H/P — holds make forgetting authority explicit

The 2010 guide documents `zfs hold`. A hold increases a snapshot's user-reference count and prevents ordinary `zfs destroy` from destroying the snapshot. `zfs destroy -d` can mark a held/cloned snapshot for deferred destruction; `defer_destroy` records that state. The snapshot is destroyed only after the relevant blocking references are released.

Thus:

> **destroy request ≠ immediate destruction.**

Retention can survive an explicit request to forget because another reference/authority relation still says the snapshot must remain.

### H/P — rollback selects an older snapshot as current by discarding later logical changes

The guide documents `zfs rollback`: the filesystem reverts to the snapshot state and changes made since that snapshot are discarded. Rolling back to a snapshot older than the most recent one requires destroying intermediate snapshots; clones can add further constraints.

That gives a separate relation:

> **historical retention ≠ historical currentness.**

A snapshot may remain readable without being the current dataset. Rollback changes authority/currentness; snapshot existence alone does not.

## Retained state

For this bounded case, later access to an old point-in-time state depends on retaining at least:

1. snapshot identity / dataset metadata;
2. a root/reference relation into the old block tree;
3. the data and metadata blocks still reachable from that snapshot;
4. allocation/reference accounting that prevents those blocks from being reused while still referenced;
5. dependency state such as clones and holds that can constrain snapshot destruction;
6. pool/device state sufficient to preserve the referenced blocks physically.

The snapshot name is not the payload. The old blocks are not sufficient without a tree/reference relation that makes them an interpretable historical dataset.

## Physical / logical substrate

The bounded substrate is layered:

```text
snapshot identity / dataset metadata
    ->
reachable historical tree
    ->
shared and snapshot-unique blocks
    ->
pool allocation/reference state
    ->
vdev / device sectors
```

The same physical block can be simultaneously reachable from the live filesystem and one or more snapshots. Later divergence can change which roots still reference it without changing the block immediately.

Hence:

> **one block ≠ one temporal owner.**

Temporal versions can share physical embodiment.

## Retention mechanism

### Copy-on-write preserves old embodiment; the snapshot preserves its authority

Case 95 already establishes the broader ZFS copy-on-write fact: an in-use block is not updated in place as the new tree is assembled.

Case 99 adds the missing second half. Copy-on-write alone can leave an old block temporarily present, but a snapshot deliberately keeps the old tree reachable. The snapshot reference prevents the old allocation from becoming reclaimable merely because the live dataset moved on.

Engineering reconstruction:

```text
old block survives COW transition
    +
snapshot/root still reaches old block
    +
allocator respects surviving reference
    =
old version remains intentionally recoverable
```

Therefore:

> **old-block physical survival ≠ snapshot retention.**

Snapshot retention requires continuing reachability/authority, not just residual bits.

### Shared reference means preservation without eager copying

At snapshot creation, the historical and live views can point to the same blocks. Only later writes to the live dataset create divergence.

This gives a particularly useful counterexample to “retention cost equals size of retained logical object.” A complete point-in-time logical view can initially be represented mostly by shared references.

### Reclamation is reference-conditioned

When the live dataset stops using an old block, that block is not necessarily free. A snapshot can still reference it. Only when no admissible dataset/snapshot/clone relation requires the block does ordinary allocation logic regain the right to reclaim it.

The case intentionally says **reclamation eligibility**, not “immediate overwrite.” Returning an allocation to free space and actually overwriting/sanitizing the underlying medium are separate events.

## Addressing and access geometry

The snapshot is not a second physical disk image with an independent address space copied sector-by-sector. It is a dataset view whose tree continues to reach a point-in-time set of blocks.

The 2010 guide also exposes snapshots through `.zfs/snapshot` for filesystems. That user-visible path is an access surface onto an older retained tree; it does not imply the blocks live in a separate backing store.

Thus:

> **separate temporal namespace ≠ separate physical backing store.**

## Read semantics

Snapshots are read-only. A reader can inspect/recover old file versions while the live dataset continues changing elsewhere.

A successful snapshot read establishes that the required old tree remains reachable and readable under the filesystem's integrity/device assumptions. It does not prove:

- that the block was copied at snapshot creation;
- that no block is shared with the live dataset;
- that every older version has been retained;
- that the underlying media is free of latent errors.

Case 18 remains the dedicated scrub/integrity case.

## Write semantics

Writes go to the active dataset, not into the read-only snapshot. Under copy-on-write, the active dataset's changed state is represented elsewhere while the snapshot continues to point to the older embodiment.

The key retention effect is not “writes duplicate the whole snapshot.” It is that later divergence can turn previously shared blocks into blocks whose continued allocation is attributable to the snapshot.

## Forgetting and reclamation

### Snapshot destroy retires one reachability relation

`zfs destroy dataset@snap` removes the snapshot when dependency rules permit it.

Engineering reconstruction:

> **snapshot destruction retires a logical/reference obligation; it does not by itself prove physical erasure.**

If no other live dataset, snapshot, or clone references certain blocks, those blocks may become reclaimable/free. But reclaimable space can still contain residual physical data until later overwrite, device-internal relocation, sanitize, or other lower-layer action.

Case 44/47 remain the relevant stronger erase/sanitization comparison.

### Holds demonstrate retained anti-forgetting state

A hold is small metadata compared with the data it can keep pinned, yet it can prevent snapshot destruction.

Therefore:

> **small control state can carry large retention consequences.**

This parallels other repository cases where mapping, currentness, or authority metadata is materially tiny but constitutive for the survival or admissibility of much larger payloads.

### Deferred destruction is a two-stage forgetting relation

With deferred destruction, an administrative destroy request can be remembered while destruction itself remains blocked.

So:

> **intent to forget ≠ permission to forget ≠ completed reclamation.**

This is a useful cross-case contrast with Ceph Case 98, where administrator authority is required to abandon an unresolved newer version. In ZFS snapshot holds, administrator intent to destroy can instead be insufficient because other references still constrain removal.

## Time

Relevant times are relational:

- snapshot creation point;
- later live-dataset mutations;
- duration for which old blocks remain referenced;
- hold lifetime;
- deferred-destroy interval;
- later allocator reuse after references disappear.

There is no single media “retention time” implied by the snapshot feature. Snapshot lifetime is a policy/reference lifetime layered over lower media persistence.

## Maintenance and labor

Snapshot retention is not maintenance-free merely because snapshot creation can be nearly instantaneous.

The system still must maintain:

- copy-on-write block-tree updates;
- reference/allocation accounting;
- snapshot and dataset namespace state;
- space accounting as blocks become unique/shared;
- clone and hold dependencies;
- eventual reclamation after references disappear;
- lower-layer integrity and device maintenance.

A cheap creation operation can therefore create a long-lived future space-management obligation.

## Failure boundaries

### Namespace/reference loss

Physical old blocks can survive while the snapshot metadata/root relation needed to reach them is lost or corrupted.

> **payload-sector survival ≠ historical-version recoverability.**

### Pool exhaustion

A snapshot can keep old blocks allocated while the live dataset continues to diverge. Retention therefore competes with future free-space availability.

This is not a defect in snapshot semantics; it is the resource consequence of intentionally keeping prior embodiments admissible.

### Misinterpreting `used`

A snapshot with `used = 0` or near zero at creation is not an empty snapshot. It may reference a large logical dataset through shared blocks.

> **unique-space charge ≠ logical retained extent.**

### Destroy mistaken for sanitization

Destroying the snapshot can make blocks reclaimable, but the source does not establish secure overwrite of every underlying embodiment.

> **logical forget ≠ allocator reclamation ≠ secure erase.**

## Prior art and genealogy boundary

### WAFL 1994 is an explicit earlier copy-on-write snapshot witness

Dave Hitz, James Lau, and Michael Malcolm's USENIX Winter 1994 paper describes WAFL snapshots as read-only clones of the active filesystem and states that WAFL uses copy-on-write to minimize their disk-space cost.

That is enough to block any claim that ZFS invented copy-on-write filesystem snapshots.

The exact historical lineage from WAFL to ZFS is **not** established here. Functional similarity and chronological priority are not proof of direct inheritance.

### Copy-on-write is older than WAFL

This case does not claim WAFL invented copy-on-write either. Establishing the broader genealogy of filesystem/versioning snapshots, shadow paging, persistent trees, and copy-on-write should be a dedicated `computing-archaeology` project.

## Cross-case comparison

### Case 95 — ZFS RAID-Z

Both cases use the same broad ZFS copy-on-write setting, but answer different retention questions.

- Case 95: keep an older committed tree admissible while constructing a new RAID-Z representation, avoiding a standing partial-stripe update.
- Case 99: deliberately retain an older point-in-time tree after the live dataset moves on by continuing to reference old blocks.

Therefore:

> **transactional replacement ≠ historical-version retention.**

### Case 73 — GFS lazy garbage collection

Both involve delayed reclamation, but for different reasons.

- GFS waits before reclaiming deleted namespace/storage state according to its distributed GC policy.
- ZFS snapshots keep blocks non-reclaimable because an explicit historical view still references them.

No genealogy is implied.

### Case 44/47 — deletion and sanitization

ZFS snapshot destruction changes reference/liveness state. NVMe sanitize / forensic verification address stronger media-forgetting claims.

Thus:

> **reference retirement ≠ media sanitization.**

### Case 98 — Ceph unfound/lost

Case 98 preserves a recovery obligation toward a currently absent newer state. Case 99 preserves reachability to an older embodied state.

Both show that retention can reside in authority/reference metadata, but the retained object of obligation differs.

## Functional analogy

A bounded analogy can be made to garbage collectors or persistent data structures: an object remains live while reachable from a root, and old structure can be shared across versions.

The analogy stops at the function. ZFS snapshots are not language-runtime garbage collection, and filesystem block allocation/reference semantics must not be replaced by GC vocabulary in historical claims.

## Philosophical / media-theoretical interpretation

`I` — Case 99 sharpens a distinction between **supersession** and **disappearance**. The live dataset can move to a newer state while an older state remains technically present and intentionally addressable.

`I` — It also shows that “the past” can be retained economically by preserving a relation to shared material rather than by copying every historical object into a separate archive.

`I` — Forgetting is staged: a destroy request can exist while a hold keeps the old state admissible; later reference retirement can make blocks reclaimable without proving physical erasure.

These are project interpretations. They are not claims that Sun, Oracle, NetApp, or OpenZFS authors formulated a philosophy of memory.

## Counterexamples and limits

This case does not establish:

- that every filesystem snapshot uses ZFS's mechanism;
- that snapshots are backups against pool/media loss;
- that snapshot creation copies the full dataset;
- that `used` measures total logical historical coverage;
- that snapshot destroy overwrites underlying sectors;
- that snapshot retention is free of space cost;
- that holds make data immutable against all privileged or destructive operations;
- that current OpenZFS release details can be projected unchanged into 2010 Solaris;
- that WAFL and ZFS have a proven direct genealogy merely because both use copy-on-write snapshots.

## Related repositories

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — repository search found no dedicated `ZFS snapshot` case during this slice; broader COW/snapshot genealogy belongs there rather than being duplicated here.
- [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) — useful for a future study of when `snapshot`, `copy-on-write`, `rollback`, and `retention policy` became actors' own problem vocabulary.

## Claim ledger

| Claim | Label | Evidence | Limit |
| --- | --- | --- | --- |
| ZFS snapshot is a read-only point-in-time copy | `H/P` | 2010 Solaris ZFS Administration Guide | bounded to documented ZFS behavior |
| snapshot initially shares blocks and later pins old blocks as live dataset changes | `H/P` | Solaris guide snapshot + space-accounting sections | not a claim about exact allocator internals in every release |
| snapshot persistence can prevent old space from being freed | `H/P/E` | Solaris guide | reclaimability still differs from media erasure |
| dataset/snapshot destruction can be constrained by snapshots/clones | `H/P` | Solaris guide | release-bounded |
| `zfs hold` increments user-reference state and blocks ordinary destroy | `H/P` | Solaris guide | documented 2010 behavior |
| deferred destroy records intent while destruction remains blocked | `H/P/E` | Solaris guide `defer_destroy` | not secure erase |
| rollback makes an older snapshot state current while discarding later changes | `H/P/E` | Solaris guide rollback section | does not recover discarded newest state |
| WAFL 1994 predates ZFS with COW snapshots | `H/P` | USENIX 1994 Hitz/Lau/Malcolm | prior-art floor, not direct genealogy |
| reference retirement is equivalent to secure media erase | `X` | no source | explicitly rejected |

## Sources

### Primary / period institutional

1. Oracle / Sun, **Solaris ZFS Administration Guide — Overview of ZFS Snapshots** (surviving 2010 edition).
   - snapshot semantics, shared old data, destroy, holds, deferred destruction, rollback:
   - <https://docs.oracle.com/cd/E19120-01/open.solaris/817-2271/gbciq/index.html>

2. Oracle / Sun, **Solaris ZFS Administration Guide — The `used` Property / snapshot space accounting**.
   - shared versus unique snapshot space; deleting snapshots can change which space is unique:
   - <https://docs.oracle.com/cd/E19120-01/open.solaris/817-2271/gcfgz/index.html>

3. Dave Hitz, James Lau, Michael Malcolm, **“File System Design for an NFS File Server Appliance,” USENIX Winter 1994 Technical Conference**.
   - WAFL snapshots as read-only clones; copy-on-write used to minimize snapshot space:
   - <https://www.usenix.org/conference/usenix-winter-1994-technical-conference/file-system-design-nfs-file-server-appliance>

### Later project documentation / continuity

4. OpenZFS, **Snapshots, Clones and Bookmarks**.
   - current continuity for COW reference sharing, snapshot pinning, holds, deferred destruction:
   - <https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Datasets/Snapshots%20and%20Clones.html>

5. OpenZFS, **Copy-on-Write**.
   - current explanatory background on old-tree preservation under COW:
   - <https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Copy-on-write.html>
