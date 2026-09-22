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
| **2010 `purged_snaps` release boundary** | [`153-ceph-2010-purged-snaps-v021-release-boundary-deepening.md`](153-ceph-2010-purged-snaps-v021-release-boundary-deepening.md) | direct tagged-source inspection shows `v0.20.1` and `v0.20.2` still encode PG-info v21 `snap_trimq`, while `v0.21` contains PG-info v22 `purged_snaps` plus activation reconstruction `cached_removed_snaps - purged_snaps`; Ceph publicly announced v0.21 on 29-Jul-2010 | development commit date != maintenance-release inclusion; later wall-clock release != inclusion proof; tagged source/release provenance != runtime correctness or bit-for-bit tarball verification |
| **2010 PG-info v21→v22 migration semantics** | [`153-ceph-2010-pginfo-v21-v22-snaptrim-migration-deepening.md`](153-ceph-2010-pginfo-v21-v22-snaptrim-migration-deepening.md) | v21 retains the pending `snap_trimq`; the v22 legacy decoder parses that old field into a local temporary and does not translate it into `purged_snaps`; activation regenerates runtime work from pool-known removed snapshots minus retained purged/completion evidence; 19-May code makes `purged_snaps` explicit trim-completion state | legacy bytes decodable != legacy progress partition preserved; schema compatibility != lossless semantic migration; reconstructable obligation != universal role/propagation correctness |
| **2011 replica-apply / completion ordering** | [`153-ceph-2011-snaptrimmer-replica-apply-completion-ordering-deepening.md`](153-ceph-2011-snaptrimmer-replica-apply-completion-ordering-deepening.md) | the `34cb737f` → `923617dc` state-machine series turns a documented race into an explicit `TrimmingObjects` → `WaitingOnReplicas` gate before advancing `purged_snaps` and sharing newer PG info; `3f4e11e1` then regenerates replica collection cleanup from retained `purged_snaps` after recovery qualification | repops issued != replica apply/ack gate cleared != completion relation advanced != PG info published; state transition != worker wakeup != proven local/remote durable commit |
| **2011 primary-local safe / publication boundary** | [`153-ceph-2011-filestore-local-safe-publication-boundary-deepening.md`](153-ceph-2011-filestore-local-safe-publication-boundary-deepening.md) | at `923617dc`, SnapTrimmer queues `write_info + remove_collection` through FileStore's no-`ondisk` convenience overload, then the outer worker may call `share_pg_info()` without waiting for local apply/readable or journal/commit-safe callbacks; FileStore/JournalingObjectStore expose those as distinct milestones | replica apply/ack ordering != primary-local apply barrier != primary-local safe/durable barrier; queue return != onreadable != ondisk; absence of barrier != demonstrated crash-loss outcome |
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
source state included in a numbered public release line
    !=
cleanup worker demonstrated functional
    !=
snapshot retirement / removed-snapshot relation
    !=
retained completion evidence (`purged` relation)
    !=
legacy progress-state migration
    !=
reconstructed cleanup obligation
    !=
worker scheduling / reservation state
    !=
active trim execution
    !=
replicated cleanup operation issued
    !=
replica application / acknowledgement gate
    !=
completion relation advanced
    !=
primary-local transaction queued
    !=
primary-local readable / applied milestone
    !=
primary-local journal / commit-safe milestone
    !=
completion relation published to peers
    !=
operator-visible maintenance status
    !=
lower-layer physical-space reclamation
    !=
media sanitization
```

The ordering arrows between those states must be established per source path rather than inferred from the list. In particular, the June-2011 source establishes a replica apply/ack gate before completion publication, but the primary-local FileStore deepening shows that publication is **not gated on** the local transaction's apply/readable or `ondisk` callback milestones at the inspected call site.

Four early provenance boundaries should remain separate.

First, the inspected public tree directly introduces the early trimmer machinery on **18 August 2008** in commit `e8e57d9a`, whose own title calls it `rough` and `non-functional`.

Second, exact numbered-tag ancestry establishes:

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

is directly visible in public Ceph source by **15 May 2010 PDT / 16 May UTC** in commit `d006ae93`.

Fourth, the release-boundary deepening shows why that source date must not be projected onto the v0.20 maintenance line. Direct tagged-source inspection gives:

```text
v0.20.1
    -> PG::Info::snap_trimq
    -> encoded PG-info v21

v0.20.2
    -> PG::Info::snap_trimq
    -> encoded PG-info v21

v0.21
    -> PG::Info::purged_snaps
    -> encoded PG-info v22
    -> runtime snap_trimq reconstructed at activation
       from cached_removed_snaps - purged_snaps
```

Ceph publicly announced v0.20.2 on **27 May 2010**, after the development commit, yet the v0.20.2 tagged source still carries the old queue-in-PG-info representation. Ceph publicly announced v0.21 on **29 July 2010**, and the inspected v0.21 tagged tree contains the new representation and reconstruction logic.

Therefore:

```text
commit exists before release date
    !=
release includes commit/state model
```

and:

```text
first source-tree appearance
    !=
first numbered release inclusion
```

The first inspected numbered public release carrying the May-2010 `purged_snaps` relation is **v0.21**. This remains a source/release provenance claim, not a proof that every runtime fault path was already correct or that the historical tarball has been independently hash-matched to the tag.

The migration-semantics slice adds a fifth boundary: **being able to decode old PG-info is not the same thing as translating the old maintenance-progress semantics into the new representation**.

The parent v21 source directly persists:

```text
P = snap_trimq
    = pending trim work
```

whereas v22 persists:

```text
C = purged_snaps
    = completion evidence
```

and reconstructs runtime work as:

```text
R = pool-known removed snapshots
Q = R - C
```

The v22 compatibility decoder's older-version branch consumes the serialized v21 queue into a local temporary `set<snapid_t> snap_trimq` and does not derive `purged_snaps` from it. Consequently:

```text
legacy record legible
    !=
legacy pending/completed partition retained
```

and:

```text
schema compatibility
    !=
lossless progress-state migration
```

The same behavior is present in the tagged v0.21 source, so this is not merely an intermediate development-tree artifact. The 19-May-2010 follow-up commit separately makes `purged_snaps` explicit completion evidence and propagates updated PG info to replicas.

This does not imply that conservative reconstruction is universally harmless. January-2011 fixes document real cases where `snap_trimq` and `purged_snaps` interacted incorrectly, including already-purged snaps reappearing in the trim queue and replicas queueing the trimmer under an invalid role/state condition. The state model and its implementation correctness therefore remain distinct questions.

The June-2011 state-machine slice adds a sixth boundary: **completion evidence may be representable before it is safe to publish as authoritative completion**. Commit `34cb737f` documents an ordering race in which newer PG info could reach a replica before replicated object-removal effects had been applied, causing premature collection removal and `ENOTEMPTY`. Its direct child `923617dc` retains in-flight repops in `WaitingOnReplicas` and advances `purged_snaps` only after its application/acknowledgement gate clears. The worker wakeup path separately waits for both acknowledgement and disk waiter sets to empty, so wakeup and transition predicates are not identical.

```text
object-removal repops issued
    !=
state-machine apply/ack gate cleared
    !=
`purged_snaps` advanced
    !=
newer PG info published
    !=
primary/replica durable-media commit proven
```

The primary-local FileStore slice adds a seventh boundary and strengthens the earlier negative result. At `923617dc`, `WaitingOnReplicas` submits the local `write_info + remove_collection` transaction with FileStore's convenience `queue_transaction(&pg->osr, t)` overload. That overload supplies an `onreadable` transaction-lifetime callback but no `ondisk` callback; FileStore's actual apply work and its journal/commit-safe completion are separately staged. The outer `snap_trimmer()` can then call `share_pg_info()` on the `need_share_pg_info` flag without waiting for either local milestone.

Therefore the exact source-level result is:

```text
replica apply/ack barrier before completion publication
    = established

primary-local apply/readable barrier before publication
    = not enforced at this call site

primary-local ondisk/journal-safe barrier before publication
    = not enforced at this call site
```

This is not by itself a demonstrated crash-loss bug. FileStore journal replay, PG peering, and reconstruction paths can change the eventual restart result. It does, however, close the callback/order question that the previous slice left open.

The direct child `3f4e11e1` adds a complementary recovery relation. Old shipped replica collection-removal side effects were not represented in the recovery log; the replacement path waits for sufficient replica recovery progress and derives local collection cleanup from retained `purged_snaps` plus local `snap_collections`. Therefore:

```text
historical cleanup operation not replayable
    !=
cleanup obligation lost
```

provided the retained completion relation, currentness qualification, and local cleanup relation are still available.

These dates and representations do **not** imply that the August-2008, tagged 2008/2009, May-2010, v0.21, June-2011, 2016, or 2017–2019 implementations are identical. The useful continuity is the bounded engineering relation, not a claim of unchanged data structures or direct genealogy across every internal refactor.

## Historical / engineering / analogy / interpretation boundary

### Historical record

Use exact Ceph source commits, parent/source state, exact tag refs, tagged files, serialization code, packaging metadata, release announcements, ObjectStore/FileStore callback signatures, and source-tree documents to establish what a particular version/date actually represented and executed. The August-2008 parent/child diff is a source-tree introduction boundary. The `v0.4`/`v0.5`/`v0.6` work is an early numbered-tag ancestry boundary. The v0.20.x/v0.21 comparison is a later source-to-public-release boundary. The v21→v22 decoder comparison is a schema/retained-state migration boundary. The June-2011 patch series is an apply/acknowledgement/completion-publication ordering boundary plus a recovery-qualified replica-cleanup reconstruction boundary. The FileStore slice separately establishes that the inspected SnapTrimmer path does not bind local apply/readable or `ondisk` completion as a prerequisite for `share_pg_info()`. None is automatically an invention, deployment, demonstrated crash-loss outcome, hardware durability theorem, or sanitization claim.

### Engineering reconstruction

Project terms such as `cleanup obligation`, `completion frontier`, `worker embodiment`, `introduction boundary`, `tag inclusion boundary`, `release-line inclusion`, `progress partition`, `semantic migration`, `reconstructed maintenance debt`, `completion publication`, `publication barrier`, `local-safe milestone`, and `cleanup authority` describe relations visible in the source. They are not silently attributed to Ceph developers as historical vocabulary.

### Functional analogy

Comparisons to orphan cleanup, repair retry, HDFS restart re-observation, filesystem GC, replicated-log frontiers, firmware/version qualification, branch maintenance, or the repository's earlier EBOFS persistence-boundary evidence are limited to explicit functions such as `obligation survives one execution episode`, `operational work can be reconstructed from retained/re-observed relations`, `retirement creates later cleanup work`, `completion publication waits for some qualifying subordinate progress but not necessarily every local persistence stage`, or `version/date label does not itself prove inclusion/runtime behavior`. They are not implementation or invention genealogies.

### Philosophical interpretation

Any interpretation about forgetting/reclamation or historical identity remains downstream of the exact mechanism. `purged`, `removed`, `snaptrim_error`, commit dates, version labels, callback names, and apply/ack predicates are not generic philosophical categories and do not imply secure erasure, complete behavioral identity, or complete archive identity. The narrow interpretive lessons are only that continuity of an obligation need not imply continuity of its serialized representation, retained completion information can have ordering/currentness conditions before it becomes safe authority for later action, and published completion can be temporally distinct from the strongest local persistence milestone exposed by the storage layer.

## Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `SnapTrimmer`, `purged_snaps`, `FileStore`, and `RepGather` found no dedicated packet to reuse in this round.

Keep in `technical-retention`:

- exact retained-state / completion-state decomposition needed to make the retention claim;
- source-level introduction boundary where it changes the retention chronology;
- exact numbered-tag/release provenance where it prevents an incorrect source/release chronology;
- exact compatibility-decoder behavior where it changes what maintenance progress survives a version transition;
- restart/activation reconstruction of cleanup obligation;
- replica apply/ack ordering where it changes when retained completion state can safely advance or be published;
- primary-local FileStore callback ordering where it changes whether publication is conditioned on local apply/safe milestones;
- recovery qualification where it changes whether a retained completion marker authorizes replica-local cleanup;
- maintenance observability and authority/currentness boundaries;
- bounded cross-case comparison.

Route primarily to `computing-archaeology` if pursued:

- broad Ceph snapshot API and clone-history archaeology;
- complete `RepGather` / FileStore / journal acknowledgement history beyond the retention seam;
- FileStore/SnapMapper implementation genealogy beyond the retention seam;
- full PG-info serialization/feature-bit genealogy;
- complete v0.3–v0.6 or v0.20.x branch/package infrastructure history;
- release-by-release deployment/adoption history;
- performance history and operator practice not needed to establish the retention relation.

## Remaining debt

The case remains **`grounded`**. The August-2008 slice closed the public-tree introduction debt, the early tag-provenance slice closed the numbered-tag mapping for the August/September/October/November-2008 source states, the v0.20.x/v0.21 slice closed the first-numbered-release mapping for the May-2010 `purged_snaps` / reconstructed-queue transition, the migration slice closed the source-level **PG-info v21→v22 compatibility/migration semantics** debt, the June-2011 state-machine slice closed the **replica-apply acknowledgement / completion-publication ordering** debt, and the FileStore slice now closes the **source-level primary-local callback/publication ordering** debt. None justifies a maturity promotion.

Still open:

- establish the first source/runtime point at which the 2008 trimmer can be demonstrated functional rather than merely present/fixed/tagged;
- if bit-for-bit distribution provenance becomes necessary, retrieve and hash/inspect the historical `ceph-0.21.tar.gz` archive against the v0.21 tag rather than assuming identity from the release announcement;
- fault-inject the `923617dc` path at `share_pg_info()` versus FileStore apply/journal-safe boundaries under selected journal modes, and trace the resulting restart/peering behavior;
- determine whether and when later Ceph revisions changed this primary-local publication barrier;
- trace later peering/currentness repair for stale or divergent `purged_snaps` state;
- trace lower-layer allocator reuse separately from RADOS logical reclamation;
- keep hardware persistence validation below FileStore's software safe boundary separate;
- keep sanitization / forensic remanence as separate evidence questions.