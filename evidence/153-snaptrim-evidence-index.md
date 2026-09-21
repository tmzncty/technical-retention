# Case 153 — Ceph RADOS snap-trim evidence navigation

**Canonical case:** [`../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md`](../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md)  
**Canonical maturity:** `grounded` — unchanged by this navigation update.  
**Purpose:** keep the Case-153 snapshot-reclamation evidence chain legible without treating later representations as if they had existed unchanged in earlier Ceph.

## Evidence chain

| Slice | Evidence | What it establishes | Boundary |
| --- | --- | --- | --- |
| **18-Aug-2008 introduction boundary** | [`153-ceph-2008-08-snaptrimmer-introduction-boundary-deepening.md`](153-ceph-2008-08-snaptrimmer-introduction-boundary-deepening.md) | commit `e8e57d9a`, `osd: rough trimmer, non-functional`, directly adds OSD/PG/ReplicatedPG `snap_trimmer` machinery; its inspected parent lacks the named implementation; Sep/Oct commits are later refinement witnesses | public-tree implementation introduction != invention priority != working implementation != first release/deployment |
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

Two source-history floors should now be kept separate.

First, the inspected public tree directly introduces the early trimmer machinery on **18 August 2008** in commit `e8e57d9a`, whose own title calls it `rough` and `non-functional`:

```text
source implementation introduced
    != working implementation
    != shipped implementation
```

Second, the stronger retention relation:

```text
retained removed-snapshot relation
    - retained purged/completed relation
    -> reconstruct runtime trim work
```

is directly visible in public Ceph source by **15 May 2010**.

These dates do **not** imply that the August-2008, May-2010, 2016, or 2017–2019 representations are identical. The useful continuity is the bounded engineering relation, not a claim of unchanged data structures or direct genealogy across every internal refactor.

## Historical / engineering / analogy / interpretation boundary

### Historical record

Use exact Ceph source commits, parent/source state, release documentation, and source-tree documents to establish what a particular version/date actually represented and executed. The August-2008 parent/child diff is a source-tree introduction boundary; it is not an invention or release claim.

### Engineering reconstruction

Project terms such as `cleanup obligation`, `completion frontier`, `worker embodiment`, `introduction boundary`, and `reconstructed maintenance debt` describe relations visible in the source. They are not silently attributed to Ceph developers as historical vocabulary.

### Functional analogy

Comparisons to orphan cleanup, repair retry, filesystem GC, or other retention cases are limited to explicit functions such as `obligation survives one execution episode` or `retirement creates later cleanup work`. They are not implementation or invention genealogies.

### Philosophical interpretation

Any interpretation about forgetting/reclamation remains downstream of the exact mechanism. `purged`, `removed`, or `snaptrim_error` are not generic philosophical categories and do not imply secure erasure.

## Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for the Ceph `snap_trimmer` / `purged_snaps` history found no dedicated packet to reuse in this round.

Keep in `technical-retention`:

- exact retained-state / completion-state decomposition needed to make the retention claim;
- source-level introduction boundary where it changes the retention chronology;
- restart/activation reconstruction of cleanup obligation;
- maintenance observability and authority/currentness boundaries;
- bounded cross-case comparison.

Route primarily to `computing-archaeology` if pursued:

- broad Ceph snapshot API and clone-history archaeology;
- FileStore/SnapMapper implementation genealogy beyond the retention seam;
- release-by-release product/deployment history;
- performance history and operator practice not needed to establish the retention relation.

## Remaining debt

The case remains **`grounded`**. The August-2008 slice closes the specific earlier debt to locate the public-tree introduction of the already-existing pre-17-Oct-2008 `snap_trimmer`, but it does not justify a maturity promotion.

Still open:

- map the August/September/October 2008 source changes and the May-2010 state change to exact first shipping release/tag rather than substituting commit date for release date;
- establish the first source point at which the 2008 trimmer can be demonstrated functional rather than merely present/fixed;
- inspect the complete PG-info v21→v22 migration behavior around `snap_trimq` / `purged_snaps`;
- finish the June-2011 state-machine series around replica-apply acknowledgement and completion publication;
- fault-inject interruption at clone removal, replicated application, PG-info update, and collection-removal boundaries;
- trace lower-layer allocator reuse separately from RADOS logical reclamation;
- keep sanitization / forensic remanence as separate evidence questions.
