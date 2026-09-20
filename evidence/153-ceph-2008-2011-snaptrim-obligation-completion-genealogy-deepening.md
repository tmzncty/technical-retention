# Case 153 deepening — Ceph 2008–2011 snap-trim obligation, completion, and worker-state genealogy

**Status:** `bounded deepening complete`  
**Canonical:** [`../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md`](../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md)  
**Scope:** public Ceph upstream source history from August 2008 through June 2011.  
**Question:** how early can the public Ceph record establish asynchronous snapshot reclamation, and when does the source clearly separate durable/reconstructible cleanup obligation from transient worker-queue state and completion evidence?

## Bounded conclusion

The already-grounded Case 153 starts from a 2013 source-tree description and later deepens the 2016 activation-reconstruction relation and the 2017–2019 representation transition. This slice moves the public source floor materially earlier without claiming invention priority.

The inspected upstream history establishes the following bounded chain:

1. by **17 October 2008**, a `snap_trimmer` already exists in the OSD path;
2. on **20 November 2008**, Ceph converts snap trimming from a dedicated sleeping thread/list into `snap_trim_wq`, making the asynchronous worker relation explicit;
3. on **24 November 2008**, the trimmer removes a snapshot collection after its contents have been trimmed;
4. on **15 May 2010**, Ceph replaces persistent `PG::Info::snap_trimq` with persistent `PG::Info::purged_snaps`, while reconstructing an in-memory `snap_trimq` at PG activation as removed snapshots minus already-purged snapshots;
5. on **19 May 2010**, trimming is sent through replicated OSD operations;
6. on **8 June 2010**, a fix makes newly removed snapshots a one-shot input rather than repeatedly re-adding the same trim work;
7. on **22 June 2011**, source changes make replica-side cleanup and SnapTrimmer completion ordering more explicit, including a state-machine redesign motivated by a race in which completion information could advance before replicas had applied object removals.

The strongest retention-specific result is therefore not simply that "Ceph had snap trimming before 2013." It is:

```text
retired-snapshot relation
    + retained completion frontier (`purged_snaps`)
    -> reconstruct transient trim obligation on activation

reconstructed obligation
    != exact pre-crash worker-queue embodiment
```

The May-2010 source is direct historical evidence for that decomposition.

This slice **does not** establish the first invention of Ceph snapshot trimming. The October/November-2008 commits already refer to an existing `snap_trimmer`; therefore the safe result is a conservative public implementation floor, not an origin claim.

---

## Claim-type discipline

### Historical record

Exact upstream Ceph commit messages and diffs establish what the public source tree implemented or changed at the listed dates.

### Engineering reconstruction

Terms such as `cleanup obligation`, `completion frontier`, `reconstructible maintenance debt`, and `worker embodiment` are project vocabulary used to describe the source relation. They are not period Ceph terminology unless explicitly quoted as identifiers.

### Functional analogy

Comparisons to later Case-153 representations and to other reclamation cases concern only the function of retaining a cleanup obligation while allowing transient execution state to disappear. They are not genealogy claims.

### Philosophical interpretation

The philosophical reading is deliberately weak: persistence may belong to a relation that can regenerate work, rather than to preservation of the exact worker state that happened to embody that work before interruption.

---

## Primary source ladder

| Source | Date | Evidence class | Use here |
| --- | --- | --- | --- |
| Ceph commit `d86d1c93867f27d70e99159f8c83c281c960ee49`, `osd: add clones to bounding snap collection(s)` | 2008-08-07 | `H/P` | early snapshot-collection substrate preceding the located trimmer commits |
| Ceph commit `57965a8849213ddff9260a1e86632687dae58e94`, `osd: fast path if snap collection doesn't exist in snap_trimmer` | 2008-10-17 | `H/P` | conservative public source floor showing a named `snap_trimmer` already exists |
| Ceph commit `69eea16f39f2255962041de29d6393ecc37bb0cb`, `osd: convert snap trimming to snap_trim_wq` | 2008-11-20 | `H/P` | explicit asynchronous work-queue embodiment replaces dedicated trimmer thread/list |
| Ceph commit `4f8fb979e833fd1dbda8cc46e598cb67f3e590f0`, `osd: remove snap collection after it is trimmed` | 2008-11-24 | `H/P` | collection retirement follows trimming |
| Ceph commit `1c3fe5649d425e7d6d52fe7f9551606082add561`, `osd: purge snaps on a per-pool basis` | 2009-06-05 | `H/P` | per-pool removed-snapshot control state; commit explicitly says trimming is not yet performed by this change |
| Ceph commit `d006ae9331216d413b5b0ef44b7b69ab8580d669`, `osd: purged_snaps in PG::Info, queue snap trim on primary` | 2010-05-15 | `H/P` | persistent completion set replaces persistent exact trim queue; activation reconstructs transient queue |
| Ceph commit `46891dd0e9867cf08a6e846471a519e8e2bd0798`, `osd: trim snaps via replicated osd ops` | 2010-05-19 | `H/P` | reclamation becomes explicitly replicated through OSD operations |
| Ceph commit `fb1c3b92b3c3398c829de6ce00f92758bb9770fa`, `osd: clear newly_removed_snaps on osdmap update if unchanged` | 2010-06-08 | `H/P` | one-shot consumption boundary for newly removed snapshot input; duplicate application caused repeated trimming/crash |
| Ceph commit `3f4e11e1116e6998f9b9b43a6fa1a5e7433f8757`, `ReplicatedPG: Replica collection removal` | 2011-06-22 | `H/P` | replica cleanup follows `purged_snaps` after sufficient recovery progress because old shipped collection removals were not log-reconstructible |
| Ceph commit `34cb737f25a68d00945b544431039e45efc8ba99`, `ReplicatePG,PG: SnapTrimmer state machine skeleton` | 2011-06-22 | `H/P` | completion-ordering race motivates state-machine redesign |

Primary URLs:

- <https://github.com/ceph/ceph/commit/d86d1c93867f27d70e99159f8c83c281c960ee49>
- <https://github.com/ceph/ceph/commit/57965a8849213ddff9260a1e86632687dae58e94>
- <https://github.com/ceph/ceph/commit/69eea16f39f2255962041de29d6393ecc37bb0cb>
- <https://github.com/ceph/ceph/commit/4f8fb979e833fd1dbda8cc46e598cb67f3e590f0>
- <https://github.com/ceph/ceph/commit/1c3fe5649d425e7d6d52fe7f9551606082add561>
- <https://github.com/ceph/ceph/commit/d006ae9331216d413b5b0ef44b7b69ab8580d669>
- <https://github.com/ceph/ceph/commit/46891dd0e9867cf08a6e846471a519e8e2bd0798>
- <https://github.com/ceph/ceph/commit/fb1c3b92b3c3398c829de6ce00f92758bb9770fa>
- <https://github.com/ceph/ceph/commit/3f4e11e1116e6998f9b9b43a6fa1a5e7433f8757>
- <https://github.com/ceph/ceph/commit/34cb737f25a68d00945b544431039e45efc8ba99>

---

# Historical record

## H/P — August–October 2008: snapshot collections precede the located trimmer floor

Commit `d86d1c93` adds clones to bounding snapshot collections on 7 August 2008. This is useful context because the early trimmer works against snapshot collections rather than the later `SnapMapper` representation.

On 17 October 2008, commit `57965a88` adds a fast path when a snapshot collection does not exist in `snap_trimmer`. That commit is the earliest named `snap_trimmer` witness located in this pass.

The wording matters:

```text
located earliest named snap_trimmer commit
    != first implementation of snapshot trimming
```

The commit modifies an already-existing function. It therefore gives a conservative public floor only.

This also blocks a backward projection from the 2013 `SnapMapper` representation: the 2008 trimmer is operating over the older snapshot-collection organization.

---

## H/P — 20 November 2008: snap trimming becomes an explicit work queue

Commit `69eea16f` is unusually useful because its diff exposes both the removed and added execution structures.

Before the change, the OSD contains:

- `snap_trimmer_lock`;
- `snap_trimmer_thread`;
- `pgs_pending_snap_removal`;
- a condition variable that sleeps when no PGs need trimming;
- a loop that pops a PG and calls `pg->snap_trimmer()`.

The change removes that dedicated thread/list arrangement and introduces:

- `snap_trim_queue`;
- `SnapTrimWQ : WorkQueue<PG>`;
- `_enqueue()` / `_dequeue()` methods;
- `_process(PG *pg) { pg->snap_trimmer(); }`;
- queue start/stop with OSD startup/shutdown;
- pause/unpause around OSD map handling;
- dequeue on PG removal.

At the PG level, `queue_snap_trim()` changes from manually adding the PG to `pgs_pending_snap_removal` and waking a thread to simply queueing the PG on `snap_trim_wq`.

This establishes by November 2008:

```text
snapshot reclamation obligation
    -> asynchronous OSD worker scheduling
```

But it does **not** establish that the work queue itself is a durable restart checkpoint. The work queue is an execution structure started and stopped with the OSD.

That distinction becomes explicit in the 2010 source.

---

## H/P — 24 November 2008: collection retirement follows object trimming

Commit `4f8fb979` removes a snapshot collection after it has been trimmed.

The safe historical statement is narrow:

> By late November 2008, the public OSD source had an asynchronous trimming path in which snapshot collection cleanup followed trimming work.

Do not turn this into a claim that all lower-layer physical blocks were erased at the same moment. The source-level action is RADOS/FileStore reclamation bookkeeping and object/collection removal, not media sanitization.

---

## H/P — June 2009: pool-level purge state is not yet the same as physical trim execution

Commit `1c3fe564` introduces a refcounted `PGPool` object to track pool-wide state including snapshot-trimming information and changes snapshot purge organization to per-pool state.

Its commit message explicitly says:

> `Doesn't trim per-pool snaps just yet.`

This is valuable negative evidence. It separates:

```text
retirement / purge intent represented at pool level
    != reclamation already executed
```

The source history itself therefore warns against equating a retired snapshot relation with completed cleanup.

---

## H/P — 15 May 2010: persistent completion evidence replaces persistent exact worker queue

Commit `d006ae93` is the core source for this slice.

Before the change, `PG::Info` contains a `snap_trimq`: a set of snapshots to trim that is encoded as part of the PG information.

The change replaces that persistent field with:

```text
interval_set<snapid_t> purged_snaps
```

and bumps the encoded PG-info version from 21 to 22.

At the same time, an `interval_set<snapid_t> snap_trimq` remains as ordinary PG runtime state rather than as the encoded `PG::Info` field.

Most importantly, `PG::activate()` reconstructs it:

```text
snap_trimq = pool->cached_removed_snaps;
snap_trimq.subtract(info.purged_snaps);
```

and queues trimming if the result is non-empty.

That is direct historical evidence for the relation:

```text
retained removed-snapshot set
    - retained completed/purged set
    -> reconstructed current trim obligation
```

The exact in-memory worker queue does not need to survive for the obligation to be recreated.

This supports two different statements which must not be collapsed:

1. `purged_snaps` is retained PG information;
2. `snap_trimq` is reconstructed execution state.

Therefore:

```text
cleanup obligation survives/reconstructs
    != exact worker state survives
```

This is not merely a modern conceptual analogy. The source literally moves the encoded state from the queue itself to the completion set and computes the queue at activation.

### Compatibility boundary

The decoder still consumes the older encoded `snap_trimq` for pre-version-22 PG info, but the inspected diff does not promote that old set into the new `purged_snaps` relation in the shown compatibility branch.

This slice does not infer a full upgrade-migration story from that fragment. The safe claim is only that the on-disk schema changed and compatibility code recognized older input.

---

## H/P — the trim worker is primary/active-qualified

The same May-2010 change tightens worker admission:

- activation queues trimming only when the PG is primary;
- `ReplicatedPG::snap_trimmer()` loops only while the PG remains primary and active;
- clearing primary state clears/dequeues the runtime trim queue.

So even when cleanup debt can be reconstructed:

```text
cleanup debt present
    != this PG instance currently authorized to execute cleanup
```

The obligation and execution authority are separate relations.

---

## H/P — 19 May 2010: trimming moves through replicated OSD operations

Commit `46891dd0`, four days later, changes snapshot trimming to use replicated OSD operations.

This supplies an important distributed-system boundary:

```text
primary decides/initiates trim
    != replica effects are already durably complete
```

It also makes the subsequent 2011 ordering work easier to interpret: snapshot reclamation is not only a local worker loop; replica application and completion ordering matter.

This slice does not claim that every trim-side effect is synchronously atomic across replicas.

---

## H/P — 8 June 2010: newly removed snapshots are one-shot input, not an indefinitely replayable event

Commit `fb1c3b92` says `newly_removed_snaps` should be applied only once on an OSD-map update. Without the fix, the same snapshots could be scheduled for trimming multiple times and the OSD could crash when the duplicate work attempted to reinsert an already represented interval.

This separates:

```text
snapshot remains retired
    != its "newly removed" transition event remains newly consumable forever
```

A durable/enduring relation may outlive the event that first caused the relation to be updated.

It also provides negative evidence against a simplistic event-log reading of `newly_removed_snaps`: the field is transition input whose repeated reapplication was a bug, not a canonical append-only history of deletion.

---

## H/P — 22 June 2011: replica cleanup uses retained purge evidence after recovery qualification

Commit `3f4e11e1` explains that replica snapshot-collection removals had previously been shipped in transactions but were not represented in the log and therefore were not reconstructed during recovery.

The replacement strategy is relation-based: once replica recovery has advanced sufficiently, the replica uses `purged_snaps` and removes objects/collections for purged snapshots locally.

The commit message states the authority condition in historical terms: once a snapshot has entered `purged_snaps`, no further operation should require that snapshot collection.

For this project, that gives:

```text
replica has enough recovery/currentness qualification
    + snapshot is in retained purged set
    -> replica cleanup is authorized
```

and:

```text
old shipped cleanup operation missing from replay log
    != cleanup obligation irrecoverably lost
```

The cleanup can be regenerated from a stronger retained relation.

This is not evidence that every lower-layer deletion is perfectly idempotent or that all later Ceph versions use the same representation.

---

## H/P — 22 June 2011: completion ordering becomes an explicit state-machine problem

Commit `34cb737f`, `SnapTrimmer state machine skeleton`, describes a concrete race in the old implementation:

- the primary could submit replicated object-removal operations;
- it did not wait for replicas to apply those removals;
- it could then update PG information to say the snapshot had been removed and send that information outward;
- on a replica, the updated information could arrive before the object-removal transaction reached the filesystem;
- collection removal could then fail with `ENOTEMPTY` and crash the OSD.

The commit proposes/moves toward a state-machine organization so the trimmer can wait for replica responses without blocking a worker thread and so trimmer state is cleaned up when the PG resets.

The retention boundary is precise:

```text
cleanup operation dispatched
    != replicas applied cleanup
    != completion/currentness information safe to advance
```

This is a distributed completion-ordering issue, not merely a scheduling-performance issue.

It also supplies a historical negative example for a recurring repository distinction:

> **publishing completion evidence too early can be wrong even when the intended cleanup operation has already been issued.**

Do not upgrade that statement into a claim of user payload loss in this exact bug. The documented immediate symptom is an ordering race and OSD crash around collection removal.

---

# Engineering reconstruction

## E — retain a completion frontier, regenerate the worker queue

The May-2010 change is a particularly clean instance of a general engineering pattern:

```text
canonical-ish obligation source
    = removed snapshots

retained completion frontier
    = purged snapshots

transient work set
    = removed - purged
```

This is stronger than saying only that "queues can be rebuilt." The source identifies what makes rebuilding possible: a retained relation describing what has been retired and a retained relation describing what reclamation has already completed.

The exact queue order, worker object, thread state, and pre-crash instruction pointer need not be retained.

## E — obligation persistence and cursor persistence are different designs

Nothing in this slice establishes a byte/object-level exact continuation cursor across restart.

The design can instead recompute a set of still-required trim work.

Therefore:

```text
reconstructible maintenance obligation
    != exact-progress checkpoint
```

A repeated or coarser restart may be correct even if it does extra work, provided the retained relations preserve safety/currentness.

## E — completion evidence has authority conditions

`purged_snaps` is not useful merely because bytes representing it exist. The 2011 replica cleanup path ties its use to sufficient recovery progress, and the trimmer itself is primary/active-qualified.

Thus:

```text
completion marker present
    != every actor may immediately act on it
```

Authority/currentness qualification remains part of the retained relation.

## E — reclamation completion is layered

The early history contains at least four completion notions:

1. a snapshot is retired/removed at the control level;
2. trim work is queued;
3. clone/object removal operations are issued/applied;
4. collection/reclamation metadata advances to `purged`.

The 2011 race exists because these cannot safely be collapsed into one instant.

No claim is made here about the exact lower-layer block allocator or physical-media erase timing.

---

# Controlled functional comparisons

## A — later Case 153 representation transitions

Later Case-153 evidence shows the removed-snapshot obligation moving through OSDMap `removed_snaps_queue`, `new_removed_snaps` / `new_purged_snaps`, `PeeringState::to_trim`, and runtime `snap_trimq` representations in 2017–2019.

This early slice shows that the more fundamental distinction predates those containers:

```text
retained retirement/completion relation
    != transient worker queue
```

Functional continuity of that relation does **not** mean the 2008 snapshot-collection implementation is technically identical to the later `SnapMapper`/OSDMap implementation.

## A — Case 125 filesystem orphan cleanup

A filesystem orphan list can retain that cleanup is still owed even though the exact cleanup worker execution does not survive a crash. Ceph `removed - purged -> trim obligation` is functionally comparable at that narrow level.

No filesystem/distributed-object-store genealogy is implied.

## A — Case 142 repair retry state

Case 142 shows a repair/backfill obligation can survive the failure of one admission attempt and be retried later. Case 153 shows a reclamation obligation can be regenerated from retirement/completion relations after worker-state loss.

The shared functional point is only:

```text
one execution episode ends
    != maintenance obligation necessarily disappears
```

The mechanisms, triggers, and correctness conditions are different.

---

# Philosophical interpretation

## P — persistence can belong to a regenerating relation rather than an execution trace

A narrow project interpretation follows from the May-2010 source:

> The continuity of maintenance need not consist in preserving the exact process that was doing the maintenance. It can consist in retaining enough relational evidence to regenerate what remains to be done.

Here the technically decisive past is not "what instruction was the trimmer executing?" but the relation between removed snapshots and snapshots already accepted as purged.

This does not turn `purged_snaps` into human memory, archival history, or Stieglerian tertiary retention by definition. It is machine-operational control state.

## P — forgetting worker detail can coexist with retaining obligation

The replacement of persistent exact `snap_trimq` with reconstructible runtime `snap_trimq` demonstrates a bounded form of intentional state reduction:

- exact queue embodiment can be discarded;
- a smaller/stronger completion relation is retained;
- work can be recomputed later.

That is an engineering observation first. Any broader philosophical claim must remain subordinate to it.

---

# Explicit non-claims

1. **Not invention priority.** The first located named `snap_trimmer` commit modifies an existing function.
2. **Not first Ceph snapshot support.** Snapshot creation/clone history is broader than this slice.
3. **Not a claim that 2008 and current Ceph use the same representation.** They do not.
4. **Not a claim that `snap_trim_wq` is durable.** The 2008 work queue is runtime execution state.
5. **Not a claim that `purged_snaps` is an append-only user audit log.** It is control/reclamation state.
6. **Not a claim that snapshot retirement equals physical media erasure.** This is logical/distributed reclamation.
7. **Not a claim that collection removal sanitizes old media.** No sanitize/forensic guarantee follows.
8. **Not a claim that reconstructing `snap_trimq` restores an exact pre-crash cursor.** The relation is set reconstruction.
9. **Not a claim that every repeated trim action is harmless.** The June-2010 duplicate-input bug is evidence that repetition can matter.
10. **Not a claim that every trim action is represented in the PG log.** The 2011 replica-cleanup commit explicitly discusses operations that were not.
11. **Not a claim that `purged_snaps` alone is universally sufficient.** Recovery/currentness and primary/active authority also matter.
12. **Not a claim that issuing replicated removal equals replica completion.** The 2011 state-machine race disproves that shortcut.
13. **Not a claim that a queue becoming empty proves lower-layer space has been physically reclaimed.** This slice does not inspect allocator/media timing.
14. **Not a claim that 2011 state-machine code proves all races were eliminated.** It addresses a documented ordering problem.
15. **Not a claim that 2013 `SnapMapper` is a direct semantic synonym for 2008 snapshot collections.** It is a later representation transition.
16. **Not a claim that all removed snapshots have distinct physical clone objects.** Object sharing/clone semantics complicate reclamation.
17. **Not a claim that `purged` means secure deletion.** It is a Ceph reclamation/currentness term.
18. **Not a claim of monotonic architectural improvement.** The commits are source-history witnesses, not a progress narrative.
19. **Not a claim that old-format compatibility is fully reconstructed here.** Only the inspected schema boundary is described.
20. **Not a genealogy claim for other distributed stores or filesystems.** Cross-case comparisons are functional only.

---

# Claim ledger

| Claim | Layer | Evidence |
| --- | --- | --- |
| a named `snap_trimmer` exists publicly by 17 Oct 2008 | `H/P` | `57965a88` |
| snapshot trimming is moved to an explicit OSD work queue by 20 Nov 2008 | `H/P` | `69eea16f` |
| collection removal follows trimming in the late-2008 path | `H/P` | `4f8fb979` |
| 2009 pool-level purge-state work explicitly does not itself perform per-pool trimming | `H/P` | `1c3fe564` |
| 2010 replaces encoded `snap_trimq` with encoded `purged_snaps` | `H/P` | `d006ae93` |
| activation computes runtime trim work as removed minus purged | `H/P` | `d006ae93` |
| trimmer execution is primary/active-qualified | `H/P` | `d006ae93` |
| trimming is routed through replicated OSD ops in May 2010 | `H/P` | `46891dd0` |
| `newly_removed_snaps` must not be reapplied indefinitely | `H/P` | `fb1c3b92` |
| replica cleanup can be regenerated from `purged_snaps` after recovery qualification | `H/P` | `3f4e11e1` |
| 2011 source identifies a race between dispatched replica removals and prematurely advanced completion info | `H/P` | `34cb737f` |
| cleanup obligation can survive without exact worker-queue persistence | `E` | reconstruction from `d006ae93` |
| operation dispatched is weaker than distributed completion | `E/H` | `34cb737f` |
| exact queue/cursor retention is not required by this design | `E` | activation reconstruction |
| `purged` does not mean sanitized media | `X` | outside source scope |

---

# Relationship to existing Case 153 evidence

This slice should be read as an earlier source-history floor, not as a replacement for the existing evidence chain:

- [`153-ceph-2013-snaptrim-asynchronous-reclamation-grounding.md`](153-ceph-2013-snaptrim-asynchronous-reclamation-grounding.md) — first bounded canonical grounding from a 2013 source-tree document plus maintained docs;
- [`153-ceph-2016-pg-activation-trim-obligation-reconstruction-deepening.md`](153-ceph-2016-pg-activation-trim-obligation-reconstruction-deepening.md) — later explicit activation reconstruction;
- [`153-ceph-2017-2019-removed-snaps-representation-transition-deepening.md`](153-ceph-2017-2019-removed-snaps-representation-transition-deepening.md) — later ownership/container transition;
- the existing snaptrim observability/error-stop deepening — user-visible queue/running/error state and stop-on-error behavior.

The new historical correction is important:

> The relation `retained retirement/completion evidence -> reconstructed trim work` is visible directly in public Ceph source by **15 May 2010**, not only in the 2016 documentation/source slice.

That does not make the 2010 and 2016 implementations identical. It moves the conservative public source floor for the relation.

---

# Related-repository check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Ceph snap_trimmer purged_snaps` found no dedicated packet to reuse.

Accordingly, this file keeps only the retention-specific early control-state genealogy needed by Case 153. A broad Ceph snapshot implementation history—client/API evolution, `snapc`, clone semantics, FileStore representation, SnapMapper design, product/release deployment, performance, and operational archaeology—still belongs primarily in `computing-archaeology`.

---

# Remaining debt after this slice

This bounded deepening closes a substantial part of the previously open **pre-2016 introduction chronology**, but it deliberately leaves narrower debts:

- find the commit that first introduced the already-existing pre-17-Oct-2008 `snap_trimmer`, if public history permits;
- map the exact public release/tag in which the 2008 and May-2010 relations first shipped, without substituting commit date for release date;
- reconstruct the 2010 on-disk v21->v22 upgrade behavior beyond the inspected decoder fragment;
- inspect the full June-2011 state-machine series and identify the exact point at which replica-apply acknowledgement gates `purged` advancement;
- fault-inject interruption at clone removal, replica application, PG-info update, and collection removal boundaries;
- trace lower-layer FileStore allocator reuse separately from RADOS logical snap trimming;
- keep sanitization/forensic-remanence questions in their own evidence chain.

The bounded status remains **Case 153: grounded; early genealogy deepened, not promoted beyond grounded.**
