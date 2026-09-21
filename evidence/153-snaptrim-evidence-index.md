# Case 153 — Ceph RADOS snap-trim evidence navigation

**Canonical case:** [`../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md`](../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md)  
**Canonical maturity:** `grounded` — unchanged by this navigation update.  
**Purpose:** keep the Case-153 snapshot-reclamation evidence chain legible without treating later representations as if they had existed unchanged in earlier Ceph.

## Evidence chain

| Slice | Evidence | What it establishes | Boundary |
| --- | --- | --- | --- |
| **18-Aug-2008 introduction boundary** | [`153-ceph-2008-08-snaptrimmer-introduction-boundary-deepening.md`](153-ceph-2008-08-snaptrimmer-introduction-boundary-deepening.md) | commit `e8e57d9a`, `osd: rough trimmer, non-functional`, directly adds OSD/PG/ReplicatedPG `snap_trimmer` machinery; its inspected parent lacks the named implementation; Sep/Oct commits are later refinement witnesses | public-tree implementation introduction != invention priority != working implementation != first release/deployment |
| **2008–2009 tag / package provenance** | [`153-ceph-2008-v04-v06-snaptrim-tag-provenance-deepening.md`](153-ceph-2008-v04-v06-snaptrim-tag-provenance-deepening.md) | `v0.4` contains the Aug introduction + Sep fixes; `v0.5` contains Oct refinements but predates `snap_trim_wq`; `v0.6` contains the Nov work-queue / post-trim collection-removal state; package-version/changelog metadata do not update at exactly the tag boundaries | source in numbered tag != demonstrated functionality != package-publication/binary deployment; Git tag chronology != Debian changelog chronology |
| **2008–2011 early source genealogy** | [`153-ceph-2008-2011-snaptrim-obligation-completion-genealogy-deepening.md`](153-ceph-2008-2011-snaptrim-obligation-completion-genealogy-deepening.md) | Nov-2008 `snap_trim_wq`; May-2010 `purged_snaps` retained completion state plus activation-time reconstruction of runtime `snap_trimq`; 2011 replica/repop completion-ordering evidence | early snapshot collections are not later `SnapMapper`; worker embodiment is not retained cleanup obligation |
| **2013 bounded grounding** | [`153-ceph-2013-snaptrim-asynchronous-reclamation-grounding.md`](153-ceph-2013-snaptrim-asynchronous-reclamation-grounding.md) | first canonical grounding of asynchronous snapshot retirement/reclamation from a first-party source-tree document plus maintained documentation | logical snapshot retirement != completed clone reclamation != sanitization |
| **2016 activation reconstruction** | [`153-ceph-2016-pg-activation-trim-obligation-reconstruction-deepening.md`](153-ceph-2016-pg-activation-trim-obligation-reconstruction-deepening.md) | activation reconstructs trim work from retained removed-vs-purged relations | retained cleanup obligation != retained byte-identical worker queue or exact cursor |
| **2017 observability / error stop** | [`153-ceph-2017-snaptrim-observability-error-stop-deepening.md`](153-ceph-2017-snaptrim-observability-error-stop-deepening.md) | `snaptrim_wait`, `snaptrim`, and `snaptrim_error` distinguish queued/waiting, executing, and error-stopped reclamation | status publication != successful reclamation completion |
| **2017–2019 representation transition** | [`153-ceph-2017-2019-removed-snaps-representation-transition-deepening.md`](153-ceph-2017-2019-removed-snaps-representation-transition-deepening.md) | removed-snapshot obligation moves through OSDMap / `PeeringState` / activation-local representations while preserving the underlying cleanup relation | same obligation relation != same container, owner, or transient worker representation |

## Current bounded synthesis

The evidence chain now supports the following retention-specific decomposition:

```text
snapshot / clone representation
    !=
cleanup worker introduced
    !=
source state included in a numbered tag
    !=
cleanup worker demonstrated functional
    !=
snapshot retirement / removed-snapshot relation
    !=
retained completion evidence (`purged` relation)
    !=
reconstructed cleanup obligation
    !=
worker scheduling / reservation state
    !=
active trim execution
    !=
distributed application / completion ordering
    !=
operator-visible maintenance status
    !=
lower-layer physical-space reclamation
    !=
media sanitization
```

Three early provenance boundaries should now be kept separate.

First, the inspected public tree directly introduces the early trimmer machinery on **18 August 2008** in commit `e8e57d9a`, whose own title calls it `rough` and `non-functional`.

Second, exact numbered-tag ancestry now establishes:

```text
v0.4
    -> contains Aug introduction + Sep fixes

v0.5
    -> contains Oct refinements
    -> predates 20-Nov snap_trim_wq conversion

v0.6
    -> contains Nov snap_trim_wq + post-trim collection removal
```

But the repository's own early version-bearing artifacts are not perfectly simultaneous: the `v0.4` tag predates the in-tree Debian `0.4-1` changelog entry by two days, and the `v0.5` tagged tree still says `AM_INIT_AUTOMAKE(ceph, 0.4)` while its Debian changelog only carries the earlier `0.4-1` entry. Therefore:

```text
Git tag label
    !=
package metadata update time
    !=
mechanism-specific functional proof
    !=
binary/package distribution or deployment
```

Third, the stronger retention relation:

```text
retained removed-snapshot relation
    - retained purged/completed relation
    -> reconstruct runtime trim work
```

is directly visible in public Ceph source by **15 May 2010**.

These dates do **not** imply that the August-2008, tagged 2008/2009, May-2010, 2016, or 2017–2019 representations are identical. The useful continuity is the bounded engineering relation, not a claim of unchanged data structures or direct genealogy across every internal refactor.

## Historical / engineering / analogy / interpretation boundary

### Historical record

Use exact Ceph source commits, parent/source state, exact tag refs, packaging metadata, release documentation, and source-tree documents to establish what a particular version/date actually represented and executed. The August-2008 parent/child diff is a source-tree introduction boundary. The `v0.4`/`v0.5`/`v0.6` work is a numbered-tag ancestry boundary. Neither is automatically an invention, runtime-correctness, binary-shipping, or deployment claim.

### Engineering reconstruction

Project terms such as `cleanup obligation`, `completion frontier`, `worker embodiment`, `introduction boundary`, `tag inclusion boundary`, and `reconstructed maintenance debt` describe relations visible in the source. They are not silently attributed to Ceph developers as historical vocabulary.

### Functional analogy

Comparisons to orphan cleanup, repair retry, filesystem GC, firmware/version qualification, or other retention cases are limited to explicit functions such as `obligation survives one execution episode`, `retirement creates later cleanup work`, or `version label does not itself prove runtime behavior`. They are not implementation or invention genealogies.

### Philosophical interpretation

Any interpretation about forgetting/reclamation or historical identity remains downstream of the exact mechanism. `purged`, `removed`, `snaptrim_error`, and version labels are not generic philosophical categories and do not imply secure erasure or complete behavioral identity.

## Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `snap_trimmer` and `Ceph snapshot trim` found no dedicated packet to reuse in this round.

Keep in `technical-retention`:

- exact retained-state / completion-state decomposition needed to make the retention claim;
- source-level introduction boundary where it changes the retention chronology;
- exact numbered-tag provenance where it prevents an incorrect source/release chronology;
- restart/activation reconstruction of cleanup obligation;
- maintenance observability and authority/currentness boundaries;
- bounded cross-case comparison.

Route primarily to `computing-archaeology` if pursued:

- broad Ceph snapshot API and clone-history archaeology;
- FileStore/SnapMapper implementation genealogy beyond the retention seam;
- full v0.3–v0.6 release/package infrastructure history;
- release-by-release deployment/adoption history;
- performance history and operator practice not needed to establish the retention relation.

## Remaining debt

The case remains **`grounded`**. The August-2008 slice closed the public-tree introduction debt, and the tag-provenance slice now closes the numbered-tag mapping for the August/September/October/November-2008 source states. Neither justifies a maturity promotion.

Still open:

- establish the first source/runtime point at which the 2008 trimmer can be demonstrated functional rather than merely present/fixed/tagged;
- if a stronger **shipping release** claim is needed, locate archival tarball/download/package-publication evidence rather than treating Git tag or in-tree changelog timestamps as shipment;
- map the May-2010 `purged_snaps` / reconstructed-queue state change to its exact first numbered tag/release boundary;
- inspect the complete PG-info v21→v22 migration behavior around `snap_trimq` / `purged_snaps`;
- finish the June-2011 state-machine series around replica-apply acknowledgement and completion publication;
- fault-inject interruption at clone removal, replicated application, PG-info update, and collection-removal boundaries;
- trace lower-layer allocator reuse separately from RADOS logical reclamation;
- keep sanitization / forensic remanence as separate evidence questions.
