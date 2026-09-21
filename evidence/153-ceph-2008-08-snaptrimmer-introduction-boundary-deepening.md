# Case 153 deepening — Ceph August 2008 snap-trimmer introduction boundary

**Status:** `bounded deepening complete`  
**Canonical:** [`../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md`](../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md)  
**Parent evidence:** [`153-ceph-2008-2011-snaptrim-obligation-completion-genealogy-deepening.md`](153-ceph-2008-2011-snaptrim-obligation-completion-genealogy-deepening.md)  
**Scope:** one narrow source-history debt: locate the public Ceph source-tree change that introduces the early `snap_trimmer` implementation already visible in the later 2008 commits.  
**Question:** can the earlier conservative October-2008 public-source floor be replaced by a source-diff-backed introduction boundary without turning commit history into an invention or shipping claim?

## Bounded conclusion

Yes, within the inspected public Git history.

Ceph commit `e8e57d9a1d546d2007a9f82ab54e901464956ad3`, dated **18 August 2008**, is titled:

> `osd: rough trimmer, non-functional`

Its diff directly adds the early snapshot-trimming machinery rather than merely modifying an already-existing named function. Among other changes, it adds:

- `OSD::snap_trimmer()`;
- `OSD::wake_snap_trimmer()`;
- a `SnapTrimmer : public Thread` worker;
- `pgs_pending_snap_removal`;
- `PG::queue_snap_trim()`;
- the `PG_STATE_SNAPTRIMQUEUE` / `PG_STATE_SNAPTRIMMING` execution path;
- the virtual `PG::snap_trimmer()` hook;
- `ReplicatedPG::snap_trimmer()` with object/collection reclamation logic;
- activation/recovery paths that call `queue_snap_trim()` when `info.removed_snaps` is non-empty.

The immediate parent commit `c598d4820b3b59ff14355f37c94eb6036c2648b5` does **not** contain the `snap_trimmer` symbol in `src/osd/ReplicatedPG.cc`, while the `e8e57d9a` diff adds the implementation. That gives a much stronger public-tree introduction boundary than the previously used 17-October-2008 commit, which only modified an existing `snap_trimmer`.

The commit message itself says **`non-functional`**. Therefore the safe chronology is:

```text
snapshot/clone representation already exists
    -> 18 Aug 2008: rough snap-trimmer implementation introduced, explicitly non-functional
    -> 10 Sep 2008: "some snap_trimmer fixes"
    -> 17 Oct 2008: fast-path fix in an established snap_trimmer
    -> 20 Nov 2008: dedicated thread/list converted to snap_trim_wq
```

This closes the earlier repository debt to locate the public-tree introduction commit for the early trimmer implementation. It does **not** close release/tag mapping, first working behavior, first deployment, first shipping release, or invention priority.

---

## Claim-type discipline

### Historical record

Exact Ceph commits, parent/source state, and diffs establish what entered the public source tree on particular dates.

### Engineering reconstruction

Project terms such as `cleanup obligation`, `worker embodiment`, `introduction boundary`, and `maintenance closure` are modern analytic vocabulary. They are not attributed to the 2008 Ceph developers unless they appear as source identifiers or commit wording.

### Functional analogy

The only controlled analogy made here is that a logical retirement relation can exist before or independently of the worker machinery that later discharges its cleanup consequences. No lineage to filesystem GC, SSD GC, TRIM, or other reclamation systems is asserted.

### Philosophical interpretation

A narrow interpretation is allowed only after the mechanism is established: a system can represent that something is retired before it has a functioning mechanism that closes all consequences of retirement. This is project interpretation, not period Ceph terminology.

---

# Primary source ladder

| Source | Date | Evidence class | Use here |
| --- | --- | --- | --- |
| Ceph commit `d86d1c93867f27d70e99159f8c83c281c960ee49`, `osd: add clones to bounding snap collection(s)` | 2008-08-07 | `H/P` | snapshot-collection substrate already exists before the trimmer-introduction change |
| parent `c598d4820b3b59ff14355f37c94eb6036c2648b5`, `src/osd/ReplicatedPG.cc` | before 2008-08-18 | `H/P` | inspected parent file has no `snap_trimmer` symbol |
| Ceph commit `e8e57d9a1d546d2007a9f82ab54e901464956ad3`, `osd: rough trimmer, non-functional` | 2008-08-18 | `H/P` | diff introduces thread/queue hooks and `ReplicatedPG::snap_trimmer()` implementation |
| Ceph commit `bfb5b8d9bd66089978fe092182a113631ff315cf`, `osd: some snap_trimmer fixes` | 2008-09-10 | `H/P` | later named fixes corroborate active refinement after the rough introduction |
| Ceph commit `57965a8849213ddff9260a1e86632687dae58e94`, `osd: fast path if snap collection doesn't exist in snap_trimmer` | 2008-10-17 | `H/P` | later established-function witness; no longer the earliest located boundary |
| Ceph commit `69eea16f39f2255962041de29d6393ecc37bb0cb`, `osd: convert snap trimming to snap_trim_wq` | 2008-11-20 | `H/P` | later worker-embodiment transition from dedicated thread/list to explicit work queue |

Primary URLs:

- <https://github.com/ceph/ceph/commit/d86d1c93867f27d70e99159f8c83c281c960ee49>
- <https://github.com/ceph/ceph/commit/e8e57d9a1d546d2007a9f82ab54e901464956ad3>
- <https://github.com/ceph/ceph/commit/bfb5b8d9bd66089978fe092182a113631ff315cf>
- <https://github.com/ceph/ceph/commit/57965a8849213ddff9260a1e86632687dae58e94>
- <https://github.com/ceph/ceph/commit/69eea16f39f2255962041de29d6393ecc37bb0cb>

---

# Historical record

## H/P — snapshot representation predates the located trimmer introduction

Commit `d86d1c93` on 7 August 2008 adds clones to bounding snapshot collections. It is therefore evidence that snapshot/clone representation and collection organization already existed before the trimmer-introduction change located here.

The safe relation is:

```text
snapshot representation exists
    != retired-snapshot cleanup worker already exists
```

Nothing in this slice claims that `d86d1c93` is the first Ceph snapshot implementation. It is used only as a nearby source-history witness for substrate preceding the trimmer.

## H/P — 18 August 2008: the public diff adds a rough, explicitly non-functional trimmer

Commit `e8e57d9a` is stronger evidence than the October witness because its diff adds the machinery itself.

At the OSD level the diff introduces a `SnapTrimmer` thread wrapper, `wake_snap_trimmer()`, `snap_trimmer()`, locking/condition state, and a list of PGs pending snapshot removal. The OSD constructor gains `snap_trimmer_thread(this)`.

At the PG level it adds `queue_snap_trim()` and a virtual `snap_trimmer()` entry point. Activation/recovery paths queue trimming when retained PG information says removed snapshots remain.

At the replicated-PG level it adds a substantial `ReplicatedPG::snap_trimmer()` body that:

- iterates `info.removed_snaps` while the PG remains active;
- lists objects in the corresponding snapshot collection;
- adjusts/removes snapshot membership and clone state;
- applies object-store transactions;
- erases the processed snapshot from `info.removed_snaps`;
- writes updated PG information when done.

This supports a narrow introduction statement:

> **On 18 August 2008, the inspected public Ceph tree gains the early OSD/PG `snap_trimmer` implementation in commit `e8e57d9a`.**

The same commit's own title qualifies the maturity as `rough` and `non-functional`.

Therefore:

```text
source implementation introduced
    != implementation demonstrated functional
    != production-ready
    != shipped
```

## H/P — the immediate parent does not contain the named implementation

The immediate parent `c598d482...` was inspected at `src/osd/ReplicatedPG.cc`; no `snap_trimmer` symbol is present there. The child diff then adds `ReplicatedPG::snap_trimmer()` and the associated OSD/PG hooks.

That parent/child contrast is why this slice uses **introduction boundary** rather than only **earliest named witness**.

It still does not prove that no private branch, unpublished prototype, alternate source path, design note, or pre-Git implementation existed earlier.

## H/P — September and October are refinement witnesses, not the introduction floor

Commit `bfb5b8d9` on 10 September 2008 is titled `osd: some snap_trimmer fixes`. Commit `57965a88` on 17 October adds a fast path in `snap_trimmer` when a snapshot collection does not exist.

These commits now serve as corroborating chronology:

```text
18 Aug rough/non-functional introduction
    -> Sep fixes
    -> Oct established-function fast-path fix
```

The previous Case-153 deepening was correct to treat the October commit as evidence that a trimmer already existed, but it left the actual introduction as an open debt. This addendum closes that debt within the inspected public history.

## H/P — November changes worker embodiment, not the existence of the obligation

Commit `69eea16f` on 20 November converts the dedicated sleeping thread/list arrangement to `snap_trim_wq`.

That later refactor remains important because it demonstrates:

```text
cleanup obligation / semantic task
    != one specific worker embodiment
```

But the November work-queue transition should no longer be read as the beginning of snap trimming. The public source already contains the rough trimmer three months earlier.

---

# Engineering reconstruction

## E — representation, worker introduction, functionality, and retention design are separate chronology points

The newly resolved source history supports a four-way distinction:

```text
snapshot retirement/clone representation
    != cleanup worker code introduced
    != cleanup worker known functional
    != restart-safe cleanup-obligation representation
```

The first two are already distinct in August 2008. The fourth becomes much clearer only in the May-2010 `purged_snaps` / reconstructed `snap_trimq` design discussed in the parent evidence.

This matters for technical-retention history because a source tree can contain both:

- a durable-ish relation saying something has been removed; and
- an immature or changing mechanism for realizing the consequences of that relation.

Do not use the existence of one to backfill maturity into the other.

## E — logical retirement can precede reliable reclamation closure

The 18-August commit queues trimming when `info.removed_snaps` is non-empty, but the author labels the trimmer non-functional. At the engineering level this gives a useful boundary:

```text
retirement obligation represented
    != reclamation mechanism successfully closes obligation
```

The later 2008 fixes and 2010/2011 completion-state work are evidence that cleanup semantics continued to mature after the first rough worker appeared.

## E — public-source introduction is not release provenance

Commit ancestry establishes source chronology. It does not establish which first released tarball, package, deployment, or production cluster contained a usable version.

The release question remains a separate provenance task:

```text
commit entered public tree
    != first tagged release
    != first shipped binary
    != first production deployment
```

---

# Controlled functional comparison

## A — Case 153 later obligation reconstruction

The 2008 introduction and the 2010 retained-completion design answer different questions.

2008 establishes that Ceph acquired a worker path intended to discharge removed-snapshot cleanup. 2010 establishes a much stronger restart relation in which runtime trim work can be reconstructed from retained removed/purged state.

Thus:

```text
worker exists
    != worker state itself must be retained
```

and:

```text
cleanup capability appears historically
    != cleanup obligation representation has reached later restart semantics
```

## A — other reclamation cases

Filesystem orphan cleanup, LSM compaction, SSD garbage collection, and distributed snapshot reclamation can all exhibit a broad pattern in which logical retirement creates later cleanup work. This file makes no claim that Ceph copied, descended from, or shares a mechanism with any of them.

---

# Philosophical interpretation

## P — retirement and closure can have different histories

A narrow project interpretation is now better grounded:

> A system may acquire the ability to represent that something should no longer belong before it acquires a reliable mechanism for finishing all consequences of that retirement.

In this source history, clone/snapshot representation predates the rough trimmer; the trimmer is introduced explicitly as non-functional; later commits repair and reorganize it; still later retained-state changes make restart reconstruction clearer.

This is not a statement that Ceph developers used philosophical categories of memory, forgetting, or obligation. Those words remain project-level interpretation.

---

# Explicit non-claims

1. **Not invention priority.** `e8e57d9a` is the located public-tree introduction of this implementation, not proof of first conception.
2. **Not first private prototype.** Unpublished/private work is outside the inspected evidence.
3. **Not first Ceph snapshot support.** Snapshot/clone mechanisms already precede the trimmer commit.
4. **Not first working trimmer.** The commit itself says `non-functional`.
5. **Not production readiness.** Source inclusion is weaker than production qualification.
6. **Not first shipping release.** Release/tag mapping remains open.
7. **Not first deployment.** No operational deployment record is established here.
8. **Not a claim that every repository path was exhaustively searched for every pre-2008 prototype.** The parent/child diff and nearby path history establish this bounded public-tree introduction.
9. **Not a claim that the September fixes make the trimmer fully correct.** They are refinement witnesses only.
10. **Not a claim that October 2008 was erroneous evidence.** It remains a valid established-function witness; it is simply no longer the earliest located boundary.
11. **Not a claim that November `snap_trim_wq` created the cleanup obligation.** It changes worker embodiment.
12. **Not a claim that the 2008 queue/thread is restart-persistent.** Later evidence is required for restart reconstruction.
13. **Not a claim that `removed_snaps` means lower-layer physical media blocks were erased.** It is logical/distributed control state.
14. **Not a claim that object/collection removal is sanitization.** Secure-erasure semantics are outside this slice.
15. **Not a claim that 2008 snapshot collections are later `SnapMapper`.** Representation changed.
16. **Not a claim that logical retirement and cleanup completion are simultaneous.** The evidence argues the opposite boundary.
17. **Not a claim that 2008 and 2010 persistence semantics are identical.** The later retained-completion reconstruction is a separate design stage.
18. **Not a claim of monotonic progress.** Commit chronology is not a teleological narrative.
19. **Not a genealogy claim for other storage systems.** Cross-case comparison is functional only.
20. **Not a philosophical attribution to historical actors.** Interpretation remains downstream of the technical record.

---

# Claim ledger

| Claim | Layer | Evidence |
| --- | --- | --- |
| snapshot collection/clone substrate predates the located trimmer introduction | `H/P` | `d86d1c93` |
| immediate parent lacks `snap_trimmer` in inspected `ReplicatedPG.cc` | `H/P` | parent `c598d482...` source inspection |
| 18-Aug-2008 diff introduces OSD/PG/ReplicatedPG snap-trimmer machinery | `H/P` | `e8e57d9a` |
| the introduced trimmer is explicitly labeled rough/non-functional | `H/P` | `e8e57d9a` commit title |
| named fixes follow by 10-Sep-2008 | `H/P` | `bfb5b8d9` |
| 17-Oct-2008 is a later established-function witness, not the introduction floor | `H/P` | `57965a88` plus earlier diff |
| November changes the worker embodiment to `snap_trim_wq` | `H/P` | `69eea16f` |
| worker introduction != working/restart-safe cleanup closure | `E` | chronology reconstruction |
| source introduction != shipping provenance | `E/X` | release evidence absent from this slice |

---

# Relationship to the earlier Case 153 genealogy evidence

This file is an **addendum/correction of one historical floor**, not a replacement for the broader 2008–2011 evidence.

The parent evidence should still be used for:

- November-2008 `snap_trim_wq` transition;
- 2009 pool-level purge-state boundary;
- May-2010 persistent `purged_snaps` plus activation reconstruction;
- one-shot `newly_removed_snaps` input;
- 2011 replica cleanup and completion-ordering state-machine work.

For introduction chronology, this file supersedes only the older bounded statement that 17 October 2008 was the earliest located named `snap_trimmer` witness.

The corrected source-history chain is:

```text
07 Aug 2008 nearby snapshot-collection substrate
18 Aug 2008 rough/non-functional snap-trimmer implementation introduced
10 Sep 2008 snap_trimmer fixes
17 Oct 2008 fast-path fix in established snap_trimmer
20 Nov 2008 worker embodiment converted to snap_trim_wq
15 May 2010 retained completion relation reconstructs runtime trim obligation
22 Jun 2011 distributed completion ordering becomes explicit state-machine work
```

---

# Related-repository check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for the Ceph `snap_trimmer` / `purged_snaps` history found no dedicated packet to reuse.

Accordingly this file keeps only the retention-specific introduction boundary. A full Ceph snapshot implementation archaeology, branch/release mapping, deployment history, or performance history remains better suited to `computing-archaeology`.

---

# Remaining debt after this slice

This slice closes the prior debt **"locate the public-tree introduction commit for the pre-17-Oct-2008 snap_trimmer"** within the inspected history.

Still open:

- map `e8e57d9a` and the later 2008 fixes to the first exact public release/tag that shipped them;
- establish the first source point at which the trimmer can be demonstrated functional rather than merely present/fixed;
- reconstruct the 2010 PG-info v21→v22 upgrade behavior beyond the already inspected compatibility fragment;
- finish the June-2011 state-machine series around replica-apply acknowledgement and completion publication;
- fault-inject interruption at clone removal, replica application, PG-info update, and collection removal boundaries;
- trace lower-layer FileStore allocator reuse separately from RADOS logical reclamation;
- keep sanitization and forensic-remanence questions separate.

**Canonical status remains `grounded`; this genealogy correction does not justify promotion.**
