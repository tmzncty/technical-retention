# Case 153 deepening — Ceph 2011 SnapTrimmer replica-apply / completion-ordering state machine

**Status:** `bounded deepening complete`  
**Canonical:** [`../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md`](../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md)  
**Canonical maturity:** `grounded` — unchanged by this slice.  
**Scope:** the June-2011 Ceph `ReplicatedPG` patch series that turns an acknowledged snap-trim race into an explicit state-machine ordering rule.  
**Question:** when may the primary advance retained `purged_snaps` / publish PG completion information relative to replicated object-removal application, and what does that prove — or not prove — about reclamation completion?

## Bounded conclusion

The June-2011 public Ceph source makes a previously implicit safety dependency explicit:

```text
object-removal repops issued
    !=
replica application observed
    !=
completion state safe to advance
    !=
updated PG info safe to publish
```

Commit `34cb737f25a68d00945b544431039e45efc8ba99` states the concrete failure mode: the old `snap_trimmer` could update PG info with a removed snapshot and send that info before replicas had applied the corresponding object-removal transactions. If the info arrived first, replica collection removal could race ahead of filesystem object removal and fail with `ENOTEMPTY`, crashing the OSD.

Its direct child, commit `923617dca1d72bb8bcfa04820339c55f05297e18`, fills out the state machine. The new `WaitingOnReplicas` state retains the in-flight `RepGather` objects and refuses to advance while any tracked repop is not locally marked `applied` or still has outstanding acknowledgement waiters. Only after that condition clears does it:

1. insert the snapshot into `info.purged_snaps`;
2. erase it from runtime `snap_trimq`;
3. queue a transaction that writes PG info and removes the snapshot collection;
4. set `need_share_pg_info`, causing the outer trim worker to publish updated PG info;
5. return toward `NotTrimming` for the next obligation.

The same source also makes scheduling and state predicates distinct. Each trim repop is marked `queue_snap_trimmer = true`; `eval_repop()` requeues the snap-trim worker only when both `waitfor_ack` and `waitfor_disk` have emptied. The state transition itself checks `applied` plus `waitfor_ack.empty()`. Therefore:

```text
state-machine completion predicate
    !=
worker wakeup predicate
```

and neither should be silently renamed “globally durable completion.”

The following child, `3f4e11e1116e6998f9b9b43a6fa1a5e7433f8757`, separately repairs replica-side collection cleanup. Rather than relying on cleanup operations shipped by the primary that were not represented in the recovery log, a sufficiently recovered replica derives local cleanup from retained `purged_snaps`. This turns `purged_snaps` into more than a display/status bit: under a recovery/currentness gate it is an authority-bearing relation from which replica cleanup work can be regenerated.

The strongest retention-specific statement is therefore:

```text
replicated cleanup effect
    -> wait for application/ack condition
    -> advance retained completion relation (`purged_snaps`)
    -> publish newer PG info

and, on a sufficiently recovered replica:

retained `purged_snaps`
    + local snapshot-collection relation
    -> regenerate local cleanup work
```

This slice **does not** prove synchronous cross-replica media durability, atomic cluster-wide reclamation, allocator reuse, secure erasure, or crash consistency below Ceph's then-current ObjectStore / filesystem boundary.

---

## Claim-type discipline

### Historical record

Historical claims below come from exact public Ceph commits, their ancestry, commit messages, and source at those commits.

### Engineering reconstruction

Terms such as `completion publication`, `cleanup authority`, `completion relation`, `application barrier`, and `regenerated cleanup obligation` are project vocabulary summarizing source relations. They are not silently attributed to Ceph developers as period terminology.

### Functional analogy

Comparisons to replicated-log commit indexes, filesystem orphan cleanup, maintenance checkpoints, or modern distributed-GC barriers are limited to specific functions such as “do not publish completion before required subordinate effects are admitted as applied.” No implementation or invention genealogy is implied.

### Philosophical interpretation

The bounded interpretive point is only that a retained statement of completion has temporal/authority conditions: a later state may be representable before it is safe to treat as authoritative. This does not turn `purged_snaps` into a generic philosophical category of forgetting.

---

# Primary source ladder

| Source | Authored / committed | Evidence class | Use here |
| --- | --- | --- | --- |
| Ceph commit `79f76dcaf00c957e2fe86908e70a53c945e02adf`, `ReplicatedPG,PG: update snap_collections on replica` | authored 2011-06-08; committed 2011-06-22 | `H/P` | replica `snap_collections` currentness is updated from replicated log entries so later purge-driven cleanup has the relation it needs |
| Ceph commit `33395c8b5b1842b2b182ac6a79f3c1a6a27761da`, `split get_obs_to_trim from snap_trimmer` | authored 2011-06-06; committed 2011-06-22 | `H/P` | factorization immediately preceding the state-machine conversion |
| Ceph commit `e53c60db77f00caaf4c95f65dc43b3e86e916a1a`, `factor object trimming out of snap_trimmer` | authored 2011-06-06; committed 2011-06-22 | `H/P` | isolates per-object trim operation before state-machine conversion |
| Ceph commit `34cb737f25a68d00945b544431039e45efc8ba99`, `SnapTrimmer state machine skeleton` | authored 2011-05-20; committed 2011-06-22 | `H/P` | explicit race statement; introduces state-machine skeleton and reset behavior |
| Ceph commit `923617dca1d72bb8bcfa04820339c55f05297e18`, `fill out state machine` | authored 2011-06-07; committed 2011-06-22 | `H/P` | implements `TrimmingObjects` → `WaitingOnReplicas` → advance `purged_snaps` / share PG info |
| Ceph commit `3f4e11e1116e6998f9b9b43a6fa1a5e7433f8757`, `Replica collection removal` | authored 2011-06-14; committed 2011-06-22 | `H/P` | replaces non-log-reconstructible shipped collection-removal side effects with replica-local cleanup derived from `purged_snaps` after recovery qualification |

Primary URLs:

- <https://github.com/ceph/ceph/commit/79f76dcaf00c957e2fe86908e70a53c945e02adf>
- <https://github.com/ceph/ceph/commit/33395c8b5b1842b2b182ac6a79f3c1a6a27761da>
- <https://github.com/ceph/ceph/commit/e53c60db77f00caaf4c95f65dc43b3e86e916a1a>
- <https://github.com/ceph/ceph/commit/34cb737f25a68d00945b544431039e45efc8ba99>
- <https://github.com/ceph/ceph/commit/923617dca1d72bb8bcfa04820339c55f05297e18>
- <https://github.com/ceph/ceph/commit/3f4e11e1116e6998f9b9b43a6fa1a5e7433f8757>

The inspected Git commit ancestry establishes the relevant linear patch sequence:

```text
79f76dca
  -> 33395c8b
  -> e53c60db
  -> 34cb737f
  -> 923617dc
  -> 3f4e11e1
```

This matters because GitHub search displays several members with the same committer timestamp (`2011-06-22T18:41:17Z`). The ancestry, not result ordering or wall-clock tie-breaking, establishes their sequence.

The author timestamps are also different from the integration timestamp. Therefore:

```text
patch authored date
    !=
commit integrated date
```

The conservative public-tree chronology used here is commit ancestry plus the recorded author/committer metadata, not an invented total order from same-second search results.

---

# Historical record

## H1 — replica snapshot-collection state had its own currentness bug

Commit `79f76dca` says that replica `snap_collections` previously were not updated as replicated modifications arrived. Consequently, a replica could receive newer `purged_snaps` from the primary yet lack the local snapshot-collection relation needed to trim the corresponding collection.

The patch scans log entries in `sub_op_modified` and updates possible first/last snapshot collections from clone entries.

Retention-specific boundary:

```text
completion relation received
    !=
local cleanup relation is necessarily complete/current
```

This is important precondition evidence for the later state machine. A correct publication order is not enough if the replica's local index of what needs cleanup is itself stale.

It also prevents a too-simple reading of `purged_snaps` as self-sufficient. `purged_snaps` is one retained relation among several.

---

## H2 — the skeleton commit documents the race in first-party terms

Commit `34cb737f` is unusually strong because the commit message itself gives the failure ordering.

The old path could:

1. issue replicated object-removal `repops`;
2. not wait for replicas to apply them;
3. advance PG info to record the removed snapshot;
4. send the newer info outward;
5. let a replica act on that info and remove its collection before the object-removal transaction had reached its filesystem;
6. hit `-39 ENOTEMPTY` and crash the OSD.

The failure is therefore not merely “snap trimming is asynchronous.” It is specifically:

```text
completion/control information overtakes subordinate data-plane cleanup
```

The patch introduces a `SnapTrimmer` state machine skeleton and resets that machine in `ReplicatedPG::on_change()`.

That reset matters for retention reasoning:

```text
PG role/epoch/reset transition
    -> transient trim execution state may be discarded
```

which remains compatible with Case 153's larger pattern:

```text
transient worker state can disappear
    while cleanup obligation / completion relations remain reconstructible
```

The skeleton commit does not itself finish the ordering fix. The direct child does.

---

## H3 — the direct child fills out the state machine

Git commit metadata shows `923617dc` is a direct child of `34cb737f`.

At that commit, the old monolithic `snap_trimmer()` body is moved into a state-machine sequence. The relevant states include:

```text
NotTrimming
    -> TrimmingObjects
    -> WaitingOnReplicas
    -> NotTrimming
```

### `NotTrimming`

The state admits primary trimming only when the PG is primary, active, and clean, with scrub-finalization handled separately. It obtains the next snapshot/collection/object set.

If there are no objects left for a snapshot, the path can advance `purged_snaps` directly and remove the empty collection. The distributed waiting issue studied in this slice concerns the branch where actual object-removal repops are issued.

### `TrimmingObjects`

For each object to trim, the state calls `trim_object()`. For a real repop it:

- sets `repop->queue_snap_trimmer = true`;
- logs and issues the replicated operation;
- evaluates it;
- retains a reference to that `RepGather` in the state machine's `repops` set.

The retained set is transient execution state, not the durable cleanup ledger.

When all objects have been submitted, the machine transitions to `WaitingOnReplicas`.

### `WaitingOnReplicas`

This state is the central evidence.

For every tracked `RepGather`, it checks:

```text
repop->applied
and
repop->waitfor_ack.empty()
```

If any repop has not been applied or still has outstanding acknowledgement waiters, the state discards the current trim event and does **not** advance snapshot completion.

Only after all tracked repops satisfy that condition does the state:

```text
info.purged_snaps.insert(sn)
snap_trimq.erase(sn)
```

then queue an ObjectStore transaction containing:

```text
write_info(...)
remove_collection(...)
```

and set:

```text
need_share_pg_info = true
```

The outer `snap_trimmer()` notices that flag and calls `share_pg_info()`.

The ordering relation is therefore directly visible:

```text
tracked object-removal repops
    -> application/ack gate
    -> advance `purged_snaps`
    -> queue PG-info + collection-removal transaction
    -> share updated PG info
```

This closes the narrow race identified in the parent commit: the primary no longer deliberately advances and publishes `purged_snaps` while tracked replica object-removal repops are still below the state machine's application/ack gate.

---

## H4 — wakeup and transition use different evidence

The surrounding `eval_repop()` path supplies a second distinction.

When a trim repop is marked `queue_snap_trimmer`, the worker is requeued only when:

```text
waitfor_ack.empty()
and
waitfor_disk.empty()
```

By contrast, `WaitingOnReplicas::react()` tests:

```text
applied
and
waitfor_ack.empty()
```

Therefore the implementation has at least two related but non-identical conditions:

```text
revisit/wakeup condition
    !=
state-transition condition
```

In the ordinary repop completion path, the worker wakeup may occur only after the stronger `waitfor_ack + waitfor_disk` sets have both emptied. But the state machine's explicit semantic gate is still the source-level predicate shown above.

This slice does **not** rename either one “durable on every replica.” The 2011 code's `ack`, `disk`, local `applied`, ObjectStore submission, and filesystem persistence semantics are separate historical questions.

---

## H5 — advancing `purged_snaps` is not proven to wait for primary local transaction commit

After the replica/application gate clears, `WaitingOnReplicas` queues the local transaction that writes PG info and removes the collection, then flags `need_share_pg_info`.

The inspected source does not show an additional callback in this state that waits for that newly queued local PG-info/collection-removal transaction to commit before `share_pg_info()` is called by the outer worker.

Therefore the safe claim is:

```text
replica apply/ack ordering is enforced before completion publication
```

not:

```text
primary local durable commit is proven to precede every completion publication
```

This is exactly why the repository must keep these layers separate:

```text
application ordering
    !=
local transaction submission
    !=
local durable commit
    !=
remote durable commit
```

A future FileStore/ObjectStore-specific crash-semantics slice would be required to strengthen that claim.

---

## H6 — `3f4e11e1` makes replica cleanup relation-based and recovery-qualified

Git metadata shows `3f4e11e1` is a direct child of the filled state-machine commit `923617dc`.

Its commit message explains the previous flaw: replica snapshot collections and contents had been removed by a transaction shipped from the primary, but those cleanup operations were not represented in the log and therefore were not reconstructed during recovery.

The replacement design waits until the replica has advanced sufficiently:

```text
last_complete_ondisk.epoch >= info.history.last_epoch_started
```

Then replica-side logic can combine local `snap_collections` with retained `info.purged_snaps`, queue local snapshot trimming, remove the objects from each purged snapshot collection, and remove the collection itself.

The source also changes processing of primary PG info so `purged_snaps` changes are acted on only after that recovery/currentness qualification.

This yields a strong retention relation:

```text
historical cleanup message/transaction not replayable
    !=
cleanup obligation lost
```

because:

```text
retained completion relation (`purged_snaps`)
    + sufficiently recovered replica
    + local snapshot-collection relation
    -> regenerated replica cleanup work
```

This is not an append-only history of every trim operation. It is a retained relation from which the needed local cleanup can be recovered.

---

# Engineering reconstruction

## E1 — completion is a published relation, not merely the last worker instruction

The 2011 race shows that “cleanup complete” cannot be inferred merely because the primary has issued all intended object-removal operations.

For this mechanism, the useful stages are:

```text
trim obligation exists
    -> object removals selected
    -> replicated removals issued
    -> required apply/ack evidence arrives
    -> `purged_snaps` advances
    -> updated PG info is published
    -> replica-local collection cleanup may be regenerated
```

The exact worker instruction pointer is not the retained fact of interest.

## E2 — publication lag is a correctness condition

The parent commit's documented race demonstrates a general but bounded engineering principle:

```text
newer control/completion state
must not outrun effects that make that state safe to consume
```

This is **not** asserted as a universal distributed-systems law in historical vocabulary. It is an engineering reconstruction from this specific failure and fix.

## E3 — control-state currentness and payload-effect currentness are different

Replica correctness here depends on multiple relations:

- whether object-removal repops have been applied/acknowledged;
- whether PG completion information has advanced;
- whether the replica has caught up far enough to trust/use `purged_snaps` for cleanup;
- whether local `snap_collections` reflects clone history sufficiently to locate cleanup work.

Thus:

```text
PG info current
    !=
local cleanup index current
    !=
all subordinate effects complete
```

## E4 — recovery qualification is part of the authority of a retained marker

`purged_snaps` bytes existing on a replica are not, by themselves, enough to authorize immediate cleanup in the June-2011 path. The replica gate checks recovery progress against `last_epoch_started`.

So:

```text
marker present
    !=
marker currently admissible for action
```

This aligns with the repository's broader currentness distinction without claiming the same protocol as Kafka, Raft, HDFS, or other cases.

## E5 — reconstructible cleanup can replace replayable cleanup history

The child patch deliberately stops depending on a cleanup operation that was not represented in the recovery log.

The alternative is relation-based:

```text
what is already purged
    + what local snapshot collections still exist
    -> what cleanup remains locally actionable
```

That is a different retention strategy from preserving every cleanup command in a replay log.

---

# Controlled functional comparisons

## A1 — Case 153 v21→v22 migration

The May-2010 migration deepening shows a change from persisting pending `snap_trimq` to persisting completion evidence `purged_snaps` and reconstructing pending work.

This 2011 slice shows the additional constraint required once that completion evidence becomes distributed authority:

```text
retaining completion evidence
    !=
advancing it at an arbitrary time
```

The representation can be recoverable yet still be wrong if its publication gets ahead of required subordinate effects.

## A2 — replicated-log commit/frontier cases

There is a narrow functional analogy to replicated-log commit/frontier mechanisms:

```text
some later-visible control frontier
is allowed to advance only after qualifying subordinate progress
```

Do not infer shared algorithms, quorum semantics, consensus, or genealogy. The 2011 SnapTrimmer uses Ceph's then-current repop and PG-info machinery, not Raft/Paxos commit rules.

## A3 — filesystem orphan / deferred cleanup

There is also a narrow analogy to orphan/deferred-cleanup cases: a cleanup operation need not itself be perfectly replayable if a retained relation allows the obligation to be rediscovered after recovery.

Again:

```text
functional similarity
    !=
shared implementation lineage
```

---

# Philosophical interpretation

The source supports only a modest interpretive statement.

A completion marker is not merely a description of what “has happened.” In this system it participates in what other replicas are authorized to do next. Its timing therefore matters.

The race shows:

```text
future-readable statement of completion
can become false-in-practice if published before
its enabling effects have reached the required stage
```

The state machine makes this temporal dependency explicit.

This does not mean Ceph developers were doing philosophy of temporality, nor does `purged_snaps` mean secure forgetting. The interpretive layer stops at the technical fact that retained completion information has ordering and authority conditions.

---

# Explicit non-claims

This slice does **not** establish any of the following:

1. that `34cb737f` is the first historical discovery of the race;
2. that the author date equals the public integration date;
3. that every same-timestamp June-2011 commit can be ordered without inspecting Git ancestry;
4. that `RepGather::applied` means durable media commit on every participant;
5. that `waitfor_ack.empty()` means `waitfor_disk.empty()`;
6. that the state-machine transition predicate and worker-requeue predicate are identical;
7. that the primary waits for its newly queued `write_info + remove_collection` transaction to durably commit before sharing PG info;
8. that all replica media are durable before `purged_snaps` is published;
9. that the fix makes snapshot reclamation one atomic cluster-wide transaction;
10. that `purged_snaps` is a cryptographic or sanitization guarantee;
11. that collection removal implies physical block erasure;
12. that allocator reuse occurs at the same instant as RADOS logical reclamation;
13. that `purged_snaps` alone is sufficient without replica recovery/currentness qualification;
14. that `purged_snaps` alone is sufficient without a usable local snapshot-collection relation;
15. that all cleanup operations are represented in the PG log after this patch series;
16. that the replica-local cleanup path is proof of exact-once deletion;
17. that re-running cleanup is always consequence-free;
18. that later SnapMapper-era implementations use the same representation;
19. that later Ceph releases preserve these exact predicates;
20. that the June-2011 patch series proves the first production deployment date;
21. that the commits prove invention priority for asynchronous snapshot reclamation;
22. that `ENOTEMPTY` was the only possible consequence of the old ordering;
23. that the documented race necessarily caused user payload loss;
24. that `last_complete_ondisk.epoch >= last_epoch_started` is a universal currentness rule outside this historical code;
25. that a replica receiving newer PG info is immediately authorized to act on every field;
26. that “applied” and “committed” are interchangeable words in Ceph's 2011 implementation;
27. that the state machine itself is durably checkpointed across PG reset;
28. that transient `RepGather` state survives restart;
29. that cleanup-history replay and relation-based cleanup reconstruction are equivalent in cost or observability;
30. that any functional analogy below establishes genealogy.

---

# Related-repository routing

A fresh code search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `SnapTrimmer`, `purged_snaps`, and Ceph snapshot trimming found no dedicated packet to reuse in this round.

Keep in `technical-retention`:

- the exact completion-ordering race because it changes what retained `purged_snaps` can safely mean;
- the distinction between apply/ack evidence, wakeup evidence, publication, and local transaction durability;
- recovery qualification of replica use of retained completion state;
- relation-based regeneration of cleanup work when the historical cleanup operation itself is not replayable;
- bounded cross-case comparisons about completion/currentness.

Route primarily to `computing-archaeology` if pursued:

- complete `RepGather` / FileStore / journal acknowledgement history;
- full OSD replication-protocol history in 2010–2012;
- the complete lineage of `snap_collections` and later `SnapMapper` structures;
- performance consequences of disk-thread scheduling and state-machine conversion;
- deployment/adoption chronology across historical Ceph releases.

---

# Remaining debt after this slice

This slice closes the Case-153 index item:

> finish the June-2011 state-machine series around replica-apply acknowledgement and completion publication.

What remains is narrower:

- establish the first source/runtime point at which the 2008 trimmer can be demonstrated functional rather than merely present/fixed/tagged;
- if needed, retrieve and hash the historical `ceph-0.21.tar.gz` against the v0.21 tag;
- inspect FileStore/ObjectStore callback and crash semantics if a stronger claim about **local durable completion before PG-info publication** becomes necessary;
- fault-inject interruption at object-removal application, PG-info publication, collection removal, and replica-local regenerated cleanup boundaries;
- trace later peering/currentness repair for stale or divergent `purged_snaps` state;
- trace lower-layer allocator reuse separately from RADOS logical reclamation;
- keep sanitization / forensic remanence separate.

Case 153 remains **`grounded`**. This is a bounded evidence deepening, not a maturity promotion.
