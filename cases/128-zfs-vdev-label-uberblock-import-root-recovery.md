# ZFS Vdev Labels and Uberblocks: Retained Pool Topology and Restart Roots

**Status:** `grounded`

## Scope

This case asks one bounded retention question:

> When process-local or host-local control state disappears, what on-device ZFS metadata is retained so a storage pool can be rediscovered, its topology interpreted, and a current committed root selected again?

The historical core is bounded to Sun Microsystems' **9 December 2005 draft ZFS On-Disk Specification**, especially Chapter One sections 1.2–1.3.4. Current OpenZFS documentation and pinned OpenZFS source are used only as later implementation/operational witnesses for import-time discovery and best-uberblock selection.

This case is not:

- a generic ZFS history;
- a second scrub case (Case 18);
- a second RAID-Z write-hole case (Case 95);
- a second dirty-time-log/resilver case (Case 100);
- proof that ZFS invented superblocks, restart roots, redundant labels, or copy-on-write roots;
- proof that four label copies make every pool recoverable after arbitrary device damage;
- proof that a physically present payload is importable without surviving control metadata;
- proof that an importable pool has restored redundancy or passed a complete integrity scan;
- a claim about vendor RAID-controller metadata or hardware-HBA replacement.

A fresh search of `tmzncty/computing-archaeology` found no dedicated ZFS vdev-label / uberblock case to reuse. Broad superblock history, ZFS genealogy, storage-controller history, and filesystem implementation archaeology belong there if developed.

## Historical vocabulary

Historical/source vocabulary retained here:

- `vdev` / `virtual device`;
- `physical vdev` / `leaf vdev`;
- `root vdev` / `top-level vdev`;
- `vdev label`;
- `name-value pair list`;
- `uberblock`;
- `transaction group` / `txg`;
- `pool_guid`, `top_guid`, `guid`;
- `ub_guid_sum`;
- `ub_rootbp`;
- `MOS` / Meta Object Set.

Project engineering vocabulary:

- **restart root** — a retained root pointer plus qualification state from which the current storage graph can be traversed after volatile control state is gone;
- **topology witness** — retained metadata that identifies pool/vdev relationships needed to interpret member devices;
- **root admissibility** — the relation by which one physically present candidate root is qualified for use rather than merely observed.

These project terms are analytical reconstructions, not claims about Sun's historical vocabulary.

## Historical record

### H/P — each physical vdev carries redundant labels

The 2005 Sun on-disk specification states that each physical vdev contains a 256 KB vdev label. It says the label describes that physical vdev and the related vdevs sharing its top-level-vdev ancestor.

The specification states that **four copies** are written on each physical vdev, with two near the front and two near the back. The stated rationale is to improve the chance that some label remains accessible after contiguous media failure or accidental overwrite.

This is retained control metadata, not four copies of all pool payload.

### H/P — label update uses an overwrite-safe staged sequence

Unlike most ZFS copy-on-write data, the fixed-location labels are overwritten. The 2005 specification therefore describes a two-stage update: even labels are written first while odd labels remain valid; after the even labels reach stable storage, the odd labels are updated.

The historical claim is narrow: the design tries to keep at least one valid label copy available across an interrupted label update. It is not a proof against arbitrary multi-location corruption.

### H/P — the label carries topology/configuration relations

The label's name-value-pair area includes pool/vdev identity and transaction state. The specification explicitly documents fields including `txg`, `pool_guid`, `top_guid`, and per-vdev `guid`, alongside a nested vdev-tree description.

Thus a member device retains more than a payload address space. It also retains relations needed to answer questions such as:

```text
which pool is this device part of?
which top-level vdev subtree does it belong to?
which configuration generation does this label describe?
```

### H/P — each label contains an uberblock array

The same specification divides the label into blank space, boot-header space, a name/value area, and **128 KB of 1 KB uberblock structures**.

Section 1.3.4 says the uberblock contains information necessary to access pool contents. In the bounded 2005 description, the active uberblock is the candidate with the highest transaction-group number and a valid SHA-256 checksum.

The specification also says an active uberblock is not overwritten in place; an updated uberblock is written into another element of the uberblock array, and uberblocks are written round-robin across pool vdevs.

### H/P — `ub_rootbp` anchors traversal into the MOS

The 2005 specification identifies `ub_rootbp` as a block pointer locating the MOS. The pool's larger object/metadata graph is therefore not recovered by scanning every payload block and guessing its role; a qualified uberblock supplies a root pointer into the metadata tree.

The same section documents `ub_guid_sum` as a check against the GUIDs of leaf vdevs encountered when opening a pool. This is another reminder that root selection and member availability are relational, not merely a matter of choosing the newest-looking bytes.

### H/P — modern OpenZFS retains the same broad root-selection architecture

Current OpenZFS documentation describes the pool as a tree rooted at the uberblock, says each device carries four label copies and each label carries a 128 KiB uberblock ring, and states that import chooses a valid uberblock with the highest transaction number.

Pinned current source at OpenZFS commit `33ae06bb617f586d43eb0a443cd69dad2f15467d` contains `vdev_uberblock_load()` and explicitly comments that configuration is read from the same vdev as the best uberblock. The implementation also has `vdev_uberblock_compare()` and modern MMP-related tie/activity logic, so this case does **not** reduce every current selection path to the historical shorthand `max(txg)`.

This is later continuity only; it is not projected backward as proof of every 2005 implementation detail.

### H/S — current `zpool import` can rediscover pools by scanning devices

Current OpenZFS `zpool-import(8)` documents pool discovery by scanning devices when no cachefile is supplied and reports pool identity, vdev layout, and health for candidate pools. This operational interface is consistent with the on-device label/configuration design.

It does not prove that every damaged set of labels is recoverable or that scanning alone validates all reachable payload.

## Retained state

The bounded restart/import path requires several different retained things:

1. payload and metadata blocks reachable from a usable root;
2. vdev-label copies on member devices;
3. pool/vdev identity and topology relations inside label configuration state;
4. multiple uberblock candidates carrying transaction/root state;
5. checksums and other qualification fields used to reject invalid candidates;
6. at least one `ub_rootbp` that reaches a usable MOS tree;
7. enough member devices / redundancy to satisfy the pool's availability requirements;
8. software capable of interpreting the on-disk format.

None of these is interchangeable with the others.

## Physical / logical substrate

At the bounded on-disk level:

```text
member block device
  -> fixed-position redundant vdev labels
      -> configuration nvlist + uberblock ring
          -> selected/admissible uberblock
              -> ub_rootbp
                  -> MOS and the rest of the reachable pool tree
```

The pool's logical continuity therefore depends on retained **relations among control structures**, not only on survival of user-data sectors.

## Retention mechanism

### Redundant fixed-location control metadata

Four separated label copies reduce dependence on one small physical region. Their placement is itself part of the recovery geometry.

### Staged overwrite of labels

Because labels are fixed-location structures, the 2005 design retains one old valid subset while writing another subset. This is a different consistency mechanism from copy-on-write replacement of ordinary tree blocks.

### Rotating root candidates

The uberblock ring retains several root candidates instead of overwriting the sole root in place. Qualification state — transaction number plus integrity/availability checks in the bounded sources — allows software to choose among candidates.

### Copy-on-write tree handoff

Current OpenZFS documentation describes a transaction group as reaching the committed pool state when the new root/uberblock is written after the changed path through the tree. Older roots can remain physically present in the ring while a newer committed root becomes current.

Engineering reconstruction:

> **root replacement can preserve restartability by retaining both an old admissible root and a newly written candidate until the newer state crosses its qualification boundary.**

## Addressing and access geometry

Restart/import is layered addressing:

1. discover candidate member devices;
2. read fixed-position label areas;
3. interpret pool/vdev identities and topology;
4. inspect uberblock candidates;
5. select an admissible root candidate;
6. follow `ub_rootbp` into the MOS;
7. traverse block pointers to recover higher-level objects and datasets.

This is not the same access path as an already-open file read. The restart path first has to recover the relations that make ordinary logical addressing meaningful.

## Read semantics

Reading a vdev label or uberblock is not described as destructive. The important read-side problem is **interpretive qualification**: a physically readable candidate can be stale, invalid, incompatible, or otherwise not the root software should use.

Thus:

> **physically readable control metadata ≠ current restart authority.**

## Write and erasure semantics

Label updates overwrite fixed regions using the staged even/odd sequence. Uberblock updates use different ring slots rather than replacing the only candidate in place.

Old labels/uberblocks can therefore survive physically after they stop being current. Their survival is not equivalent to a user-visible snapshot or guaranteed rollback point.

> **old restart-root bytes ≠ intentionally retained historical version.**

## Time

Several temporal relations are separate:

- a label-copy lifetime;
- a label-configuration `txg` generation;
- an uberblock candidate's transaction generation;
- the interval while a new label subset is being written;
- the interval while a txg is syncing before its root becomes committed;
- the later import/restart time needed to rediscover and traverse the pool.

A control structure can be physically old yet still useful as a fallback; another can be newer yet inadmissible because its integrity/reachability relation fails.

## Maintenance and labor

Persistence here depends on hidden work even though the on-device structures themselves are nonvolatile:

- generating and updating topology/configuration metadata;
- maintaining separated label copies;
- staging label writes so an older valid copy remains;
- computing and checking integrity metadata;
- rotating uberblock writes;
- importing/scanning candidate devices after restart;
- interpreting feature/version compatibility;
- diagnosing insufficient or inconsistent member sets.

The medium does not autonomously reconstruct a pool. Software must re-establish legibility from retained structures.

## Failure / forgetting modes

Distinct bounded failures include:

- all useful label copies on a required member becoming unreadable/corrupt;
- topology/configuration evidence becoming stale or inconsistent with the available member set;
- uberblock candidates being physically present but failing validity checks;
- the selected root pointer reaching unavailable/corrupt metadata;
- too few required vdev contributions surviving for the pool to open;
- format/feature incompatibility preventing interpretation;
- administrative rewind selecting an older state and intentionally discarding later logical history;
- ordinary payload corruption discovered only after import.

These are not one generic event called `data loss`.

## Engineering reconstruction

The central relation is:

```text
payload/media survival
    + topology witness survival
    + admissible restart-root survival
    + interpreter availability
    -> possible pool re-legibility
```

This yields the following guarded conclusions:

> **payload survival ≠ restart legibility.**

> **label presence ≠ label admissibility.**

> **uberblock presence ≠ active/current root.**

> **restart-root recovery ≠ complete integrity verification.**

> **pool import ≠ restored redundancy.**

> **on-device control metadata ≠ controller-independent hardware semantics.**

## Prior art and genealogy boundary

The 2005 specification itself says the uberblock is similar to the UFS superblock. Superblock-like restart roots therefore plainly predate ZFS.

The safe historical claim is only that the bounded ZFS design combines redundant vdev labels, topology/configuration state, an uberblock ring, transaction qualification, and a root block pointer in this documented way.

Chronology/function does not support:

> `ZFS invented superblocks`.

Nor does the existence of earlier superblocks establish a complete direct genealogy for every ZFS label/uberblock design choice.

## Cross-case comparison

### Case 46 — GFS master log/checkpoint recovery

Both cases retain compact control state that makes a larger store legible after restart. GFS combines replicated log/checkpoint state with re-observation of chunk locations; ZFS embeds topology/root evidence on member devices and traverses a copy-on-write object tree.

Functional comparison only:

> **recovery root ≠ one universal checkpoint mechanism.**

### Case 58 — Raft snapshotting

Raft snapshots replace committed command history and carry continuation metadata for consensus repair. A ZFS uberblock is a root into a committed storage tree, not a consensus snapshot and not a replacement for follower log lineage.

### Case 90 — Kafka leader-epoch admissibility

Both cases show that retained metadata must be qualified before it may authorize recovery. The mechanism and history are unrelated.

> **metadata presence ≠ metadata admissibility.**

### Case 95 — RAID-Z write-hole avoidance

Case 95 asks whether a multi-block coded update leaves an admissible on-disk state. Case 128 asks how restart discovers and chooses a root/topology after volatile control state is gone. Update consistency and restart legibility are adjacent but distinct.

### Case 100 — ZFS DTL selective resilver

Case 100 retains failure-exposure history to bound later repair scope. Case 128 retains topology/root state to make the pool interpretable in the first place.

> **repair-scope evidence ≠ restart-root evidence.**

## Functional analogy

A bounded analogy is a self-describing archive with several catalog covers and several recent root indexes: the content can survive, but a reader still needs an admissible catalog/root to know how the pieces compose.

This is only a functional analogy. It must not replace the historical ZFS vocabulary or imply that a filesystem is literally an archive institution.

## Philosophical / media-theoretical interpretation

`I` — Case 128 sharpens a distinction between **material survival** and **technical legibility**. Persistence is not exhausted by whether payload bits remain on media; the relations that make those bits addressable as *this pool, this topology, this current tree* must also survive or be reconstructable.

`I` — The retained root is not a miniature duplicate of the whole store. A small relation can organize access to a much larger body of surviving state.

`I` — Forgetting can therefore occur through loss of a root or topology witness even when much of the underlying material remains physically present.

These are project interpretations, not historical claims about Sun/OpenZFS authors' philosophy.

## Counterexamples and limits

This case does not establish:

- that four labels guarantee recovery after arbitrary corruption;
- that the newest physically readable uberblock is always safe to use;
- that modern MMP/import logic is identical to the 2005 draft;
- that every old uberblock is a supported rollback point;
- that successful import proves all files are intact;
- that successful import restores missing redundancy;
- that label redundancy duplicates the user payload;
- that host cachefile loss is the only reason import scanning is needed;
- that hardware RAID/HBA controller metadata behaves like ZFS labels;
- that ZFS originated the superblock/restart-root idea.

## Related repositories

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — fresh searches for `ZFS`, `uberblock`, and `vdev label` found no dedicated case to reuse. Broad superblock history, ZFS source genealogy, controller history, and filesystem implementation archaeology belong there if developed.
- [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) — a future problem-history slice could ask how actors distinguished `consistent on-disk state`, `import`, `recovery`, `rollback`, and `repair` across filesystem generations.

## Claim ledger

| Claim | Label | Evidence | Limit |
| --- | --- | --- | --- |
| each physical vdev carries four separated label copies | `H/P` | Sun 2005 on-disk spec §1.2.1 | bounded to documented design |
| fixed labels use a two-stage even/odd update | `H/P` | Sun 2005 §1.2.2 | not proof against arbitrary corruption |
| label nvlist retains pool/vdev identity and topology relations | `H/P` | Sun 2005 §1.3.3 | not a complete history of configuration changes |
| label contains a 128 KB uberblock array | `H/P` | Sun 2005 §1.3 / §1.3.4 | historical layout witness |
| bounded 2005 active root uses highest txg plus valid SHA-256 | `H/P` | Sun 2005 §1.3.4 | do not universalize to all modern tie/activity logic |
| `ub_rootbp` locates the MOS | `H/P` | Sun 2005 §1.3.4 | root pointer is not payload duplication |
| modern OpenZFS import retains the broad label/ring/best-root architecture | `H/P` later continuity | OpenZFS docs + pinned `vdev_label.c` | later implementation witness only |
| payload survival guarantees importability | `X` | mechanism decomposition | rejected |
| physically newest candidate is automatically authoritative | `X` | validity/selection requirements | rejected |
| successful import proves complete integrity and restored redundancy | `X` | operation-scope comparison | rejected |
| ZFS invented superblocks/restart roots | `X` | Sun spec's own UFS analogy + prior art | rejected |

## Sources

- Sun Microsystems, **ZFS On-Disk Specification**, draft 2005-12-09, Chapter One §§1.2–1.3.4, preserved PDF: <https://www.filibeto.org/~aduritz/truetrue/solaris10/ondiskformatfinal.pdf>
- Matthew Ahrens preservation repository for the original on-disk specification artifacts: <https://github.com/ahrens/zfsondisk>
- OpenZFS, **Copy-on-Write** documentation, current documentation witness: <https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Copy-on-write.html>
- OpenZFS pinned source, `module/zfs/vdev_label.c`, commit `33ae06bb617f586d43eb0a443cd69dad2f15467d`: <https://github.com/openzfs/zfs/blob/33ae06bb617f586d43eb0a443cd69dad2f15467d/module/zfs/vdev_label.c>
- OpenZFS, **zpool-import(8)**, current manual: <https://openzfs.github.io/openzfs-docs/man/master/8/zpool-import.8.html>
