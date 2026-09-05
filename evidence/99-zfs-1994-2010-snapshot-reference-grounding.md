# Case 99 Grounding — WAFL 1994 and Solaris ZFS 2010 Snapshot Reference Retention

**Case:** [`../cases/99-zfs-snapshot-reference-pinned-retention.md`](../cases/99-zfs-snapshot-reference-pinned-retention.md)

**Status:** `grounded`

## Purpose

This record grounds a narrow mechanism:

> ZFS snapshots keep an older point-in-time filesystem/volume view recoverable by continuing to reference blocks that the live dataset no longer needs, preventing those blocks from being freed while the snapshot relation remains admissible.

It also grounds two adjacent control-state boundaries:

- snapshot/clone/hold references can constrain destruction;
- rollback can make an older retained view current by discarding later logical changes.

The record does **not** ground secure physical erasure, a complete ZFS genealogy, or invention priority.

---

## Source A — 1994 WAFL prior-art floor

**Dave Hitz, James Lau, Michael Malcolm**, “File System Design for an NFS File Server Appliance,” USENIX Winter 1994 Technical Conference.

USENIX landing page:

<https://www.usenix.org/conference/usenix-winter-1994-technical-conference/file-system-design-nfs-file-server-appliance>

### A1. Historical claim

The USENIX abstract states that WAFL's primary focus includes algorithms/data structures for `Snapshots`, described as read-only clones of the active filesystem, and that WAFL uses a copy-on-write technique to minimize the disk space snapshots consume.

### A2. Grounded use

This is sufficient as a **prior-art floor** against any ZFS-first story for copy-on-write filesystem snapshots.

### A3. Limits

This record does not infer:

- that WAFL invented copy-on-write;
- that ZFS directly inherited its snapshot implementation from WAFL;
- that WAFL and ZFS have identical block/reference accounting;
- that the abstract alone is a complete WAFL mechanism history.

Broader snapshot/COW genealogy belongs in `computing-archaeology`.

---

## Source B — 2010 Solaris ZFS Administration Guide: snapshot semantics

Oracle-preserved Sun/Solaris documentation:

<https://docs.oracle.com/cd/E19120-01/open.solaris/817-2271/gbciq/index.html>

The page identifies itself as **Solaris ZFS Administration Guide**, Chapter 7, `Working With ZFS Snapshots and Clones`, and carries © 2010 Oracle Corporation and/or its affiliates.

### B1. Read-only point-in-time copy

The guide defines a snapshot as a read-only copy of a filesystem or volume.

**Grounded use:** snapshot identity denotes an old accessible dataset state rather than merely “some residual blocks.”

### B2. Initial sharing; later old-block pinning

The guide says snapshots can be created almost instantly and initially consume no additional pool space. As active data changes, the snapshot continues to reference old data and prevents that space from being freed.

This directly grounds:

- shared initial embodiment;
- divergence over time;
- old-block retention by continuing reference;
- reclamation blocked by surviving snapshot reachability.

### B3. No separate backing store

The guide says snapshots use no separate backing store and consume space directly from the same pool as the source filesystem/volume.

**Grounded use:** separate temporal identity does not imply a separate full physical copy.

### B4. Destruction constraints

The guide documents `zfs destroy dataset@snap`. It also says a dataset cannot be destroyed while snapshots of it exist and that clones can prevent snapshot destruction.

**Grounded use:** retained references/dependencies constrain reclamation and administrative destruction.

### B5. Holds and user references

The guide documents `zfs hold`, saying a hold prevents a snapshot from being destroyed. It describes a per-snapshot user-reference count that increments when a hold is added and decrements when released.

**Grounded use:** very small authority/control metadata can keep a much larger historical tree retained.

### B6. Deferred destruction

The guide documents `zfs destroy -d` for a held snapshot and the `defer_destroy` property that records whether a snapshot has been marked for deferred destruction.

**Engineering reconstruction:** a system can retain **intent to forget** while the referenced historical state remains admissible. Therefore `destroy requested ≠ destroy permitted ≠ reclamation completed`.

### B7. Snapshot space accounting

The same page says snapshot space is initially shared among snapshot/filesystem/possibly earlier snapshots. As the filesystem changes, previously shared space becomes unique to a snapshot and counts toward `used`; deleting one snapshot can change how space is attributed to neighboring snapshots.

**Grounded use:** a snapshot's `used` value is not its total logical historical extent.

### B8. Rollback

The guide says `zfs rollback` discards changes made since a snapshot and reverts the filesystem to that snapshot state. Rolling back to an older-than-latest snapshot requires destroying intermediate snapshots, with stronger handling when clones exist.

**Grounded use:** retaining an old version and making that version current are separate relations.

### B9. Time anchors visible in the guide

Examples on the page show snapshots/holds dated 2008–2009, while the preserved edition is © 2010. These examples are not treated as feature-introduction dates. This record therefore uses **2010 documentation witness** rather than inventing precise introduction dates for snapshot/hold subfeatures.

---

## Source C — 2010 Solaris ZFS Administration Guide: `used` property

Oracle-preserved page:

<https://docs.oracle.com/cd/E19120-01/open.solaris/817-2271/gcfgz/index.html>

### C1. Shared versus unique space

The guide states that snapshot space begins shared with the filesystem and possibly previous snapshots, and later becomes unique as the filesystem changes.

### C2. Deleting one snapshot can change another snapshot's unique accounting

The page explicitly notes that deleting snapshots can increase the space unique to and therefore counted as used by other snapshots.

**Engineering reconstruction:** physical space attribution is a property of a **reference graph**, not a fixed byte ownership label attached once at snapshot creation.

### C3. Limit

Space-accounting output is not a direct forensic map of which physical sectors retain which old user bytes, and it does not establish secure erasure on snapshot deletion.

---

## Source D — current OpenZFS documentation: continuity only

OpenZFS:

- <https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Datasets/Snapshots%20and%20Clones.html>
- <https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Copy-on-write.html>

Current documentation continues to explain that ZFS does not overwrite in-use blocks in place, that a snapshot is a reference preserving the older tree, that old snapshot-only blocks remain allocated, and that holds/deferred destruction constrain deletion.

This is useful for current conceptual continuity. It is **not** used to backdate every modern command/detail into 2010.

---

## Related-repository duplication check

A GitHub code search during this slice found no dedicated `ZFS snapshot` match in `tmzncty/computing-archaeology`.

Use that narrowly: no matching dedicated case was found by this search. It is not proof that no adjacent filesystem history exists there.

Division of labor:

- full snapshot / shadow-paging / persistent-tree / WAFL → ZFS genealogy: `computing-archaeology`;
- bounded retention relation among old-tree reachability, reference pinning, rollback, destroy, and reclamation: Case 99 here.

---

## Claim ledger

| Claim | Type | Evidence | Status / limit |
| --- | --- | --- | --- |
| ZFS snapshot is a read-only copy of filesystem/volume state | `H/P` | Source B | grounded to documented Solaris ZFS |
| snapshot initially shares blocks and later retains old blocks by continuing references | `H/P` | Sources B–C | grounded |
| old blocks referenced by snapshot are prevented from being freed | `H/P` | Source B | grounded |
| snapshot logical extent can greatly exceed its unique `used` charge | `H/P/E` | Sources B–C | grounded relation; not a universal numeric claim |
| snapshots have separate backing stores | `X` | Source B | explicitly rejected |
| holds can prevent snapshot destruction | `H/P` | Source B | grounded |
| deferred destroy means destroy request can precede actual destruction | `H/P/E` | Source B | grounded control relation |
| rollback makes an old snapshot state current while discarding later changes | `H/P/E` | Source B | grounded |
| snapshot destroy securely overwrites all lower-layer embodiments | `X` | none | unsupported; rejected |
| ZFS invented COW snapshots | `X` | Source A | WAFL 1994 is earlier explicit witness |
| WAFL directly caused ZFS design | `X` | none | genealogy not established |

---

## Controlled conclusions

1. **historical-version retention can be reference-pinned rather than copy-eager**;
2. **logical retained extent ≠ unique physical-space charge**;
3. **superseded in the live dataset ≠ reclaimable while a snapshot still references the block**;
4. **snapshot retention ≠ residual-bit survival** because a valid root/reference relation is constitutive;
5. **destroy request ≠ immediate destruction** when holds/clones remain;
6. **intent to forget ≠ permission to reclaim ≠ physical secure erase**;
7. **rollback changes currentness authority rather than reconstructing a missing latest state**;
8. **small reference/hold metadata can impose large payload-retention consequences**;
9. **WAFL 1994 blocks a ZFS-first claim without proving direct genealogy**.
