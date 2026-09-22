# Case 153 deepening — Ceph 2011 FileStore local-safe / PG-info publication boundary

**Status:** `bounded deepening complete`  
**Canonical:** [`../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md`](../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md)  
**Canonical maturity:** `grounded` — unchanged by this slice.  
**Follow-on to:** [`153-ceph-2011-snaptrimmer-replica-apply-completion-ordering-deepening.md`](153-ceph-2011-snaptrimmer-replica-apply-completion-ordering-deepening.md)  
**Scope:** exact source-level ordering between SnapTrimmer completion-state advancement, the primary's local `ObjectStore` transaction, FileStore apply/safe milestones, and `share_pg_info()` in the June-2011 state-machine implementation.  
**Question:** after the June-2011 SnapTrimmer waits for its replica apply/ack gate, does it also wait for the primary-local `write_info + remove_collection` transaction to reach an apply or durable/safe milestone before publishing the newer PG info?

## Bounded conclusion

At Ceph commit [`923617dca1d72bb8bcfa04820339c55f05297e18`](https://github.com/ceph/ceph/commit/923617dca1d72bb8bcfa04820339c55f05297e18), the answer is **no at the source-level contract exposed by this path**.

After `WaitingOnReplicas` has cleared its replica-facing gate, it advances `info.purged_snaps`, erases the runtime `snap_trimq` entry, builds a local transaction containing `write_info()` plus `remove_collection()`, and submits that transaction through:

```cpp
pg->osd->store->queue_transaction(&pg->osr, t);
```

That call uses FileStore's convenience overload with **no `ondisk` callback**. The overload supplies only a transaction-deletion callback in the `onreadable` position and delegates to the asynchronous `queue_transactions()` machinery.

The state machine then sets `need_share_pg_info = true`. The outer `snap_trimmer()` observes that flag immediately after `process_event(SnapTrim())` and calls `share_pg_info()`; it does not wait on an `onreadable`, `onreadable_sync`, `ondisk`, journal-completion, or commit callback from the local transaction.

Therefore the source establishes a stronger and more precise boundary than the previous slice's deliberately cautious formulation:

```text
replica apply/ack gate cleared
    -> advance in-memory `purged_snaps`
    -> queue primary-local PG-info + collection-removal transaction
    -> request/share newer PG info

but not:

replica apply/ack gate cleared
    -> wait for primary-local durable/safe callback
    -> share newer PG info
```

FileStore and `JournalingObjectStore` themselves keep several milestones distinct: transaction submission, later filesystem/application work, journal/safe notification, and later commit/checkpoint state. The SnapTrimmer call site does not install a barrier on those milestones before publication.

The strongest retention-specific conclusion is thus:

> **The June-2011 fix establishes a replica apply/ack ordering barrier before advancing/publishing snapshot-trim completion state, but it does not establish a primary-local stable-storage barrier before that publication.**

This is a source-level ordering result. It is **not** evidence that a particular crash necessarily loses `purged_snaps`: journal replay or later recovery can preserve/reconstruct state depending on FileStore mode, filesystem state, journal state, and failure timing. It also does not establish the behavior of later Ceph or BlueStore.

---

## Claim-type discipline

### Historical record

Historical claims below come from the exact `923617dc` Ceph source tree: `ReplicatedPG.cc`, `ObjectStore.h`, `FileStore.cc`, `FileStore.h`, `JournalingObjectStore.{h,cc}`, `FileJournal.cc`, and `PG.cc`.

### Engineering reconstruction

Terms such as **publication barrier**, **local-safe milestone**, **primary-local durability gate**, and **publication-before-safe window** are project vocabulary for relations exposed by the source. They are not attributed to Ceph developers as period terminology.

### Functional analogy

The controlled comparison to the repository's 2007 EBOFS evidence is limited to one function: both implementations distinguish an update being submitted/applied from a later local safe/persistence milestone. This is not a claim that EBOFS and 2011 FileStore have identical journals, callbacks, crash behavior, or implementation genealogy.

### Philosophical interpretation

The narrow interpretive point is that **published completion and locally stabilized completion are different temporal relations**. A system can make a completion fact available to another actor before every lower-layer embodiment of that fact has reached the strongest local persistence milestone exposed by the storage API. This is not a general theory of truth, memory, or forgetting.

---

# Primary source ladder

| Source | Evidence class | Use here |
| --- | --- | --- |
| Ceph commit `923617dc...`, `ReplicatedPG, PG: fill out state machine` | `H/P` | exact June-2011 SnapTrimmer path and commit boundary |
| `src/osd/ReplicatedPG.cc` at `923617dc` | `H/P` | local transaction is queued, then `need_share_pg_info` causes publication without a callback wait |
| `src/os/ObjectStore.h` at `923617dc` | `H/P` | API explicitly separates `onreadable`, `ondisk`, and `onreadable_sync` callback roles |
| `src/os/FileStore.cc` / `FileStore.h` at `923617dc` | `H/P` | convenience overload installs only `onreadable`; queued operation is applied asynchronously; journal modes carry separate `ondisk` continuation |
| `src/os/JournalingObjectStore.{h,cc}` at `923617dc` | `H/P` | `applied_seq`, `committing_seq`, `committed_seq`, journal callbacks, and commit waiters are separate states |
| `src/os/FileJournal.cc` at `923617dc` | `H/P` | journal submission queues an `oncommit` completion; writer completion and device-cache assumptions are separate concerns |
| `src/osd/PG.cc` at `923617dc` | `H/P` | `share_pg_info()` sends the updated `PG::Info` to acting replicas |

Primary URLs:

- <https://github.com/ceph/ceph/commit/923617dca1d72bb8bcfa04820339c55f05297e18>
- <https://github.com/ceph/ceph/blob/923617dca1d72bb8bcfa04820339c55f05297e18/src/osd/ReplicatedPG.cc>
- <https://github.com/ceph/ceph/blob/923617dca1d72bb8bcfa04820339c55f05297e18/src/os/ObjectStore.h>
- <https://github.com/ceph/ceph/blob/923617dca1d72bb8bcfa04820339c55f05297e18/src/os/FileStore.cc>
- <https://github.com/ceph/ceph/blob/923617dca1d72bb8bcfa04820339c55f05297e18/src/os/FileStore.h>
- <https://github.com/ceph/ceph/blob/923617dca1d72bb8bcfa04820339c55f05297e18/src/os/JournalingObjectStore.cc>
- <https://github.com/ceph/ceph/blob/923617dca1d72bb8bcfa04820339c55f05297e18/src/os/JournalingObjectStore.h>
- <https://github.com/ceph/ceph/blob/923617dca1d72bb8bcfa04820339c55f05297e18/src/os/FileJournal.cc>
- <https://github.com/ceph/ceph/blob/923617dca1d72bb8bcfa04820339c55f05297e18/src/osd/PG.cc>

---

# Historical record

## H1 — the SnapTrimmer local completion transaction has no callback barrier

In `WaitingOnReplicas::react()`, after all tracked repops satisfy the state-machine gate, the code advances:

```text
info.purged_snaps
runtime snap_trimq
```

It then creates one primary-local `ObjectStore::Transaction` containing:

```text
write_info(...)
remove_collection(...)
```

and submits it with the two-argument convenience call:

```cpp
queue_transaction(&pg->osr, t)
```

There is no callback argument at this call site.

Immediately afterward the state machine sets:

```text
need_share_pg_info = true
```

This is enough to reject a stronger reading in which the SnapTrimmer state itself explicitly waits for an ObjectStore safe callback before allowing publication.

Historical boundary:

```text
local transaction submitted
    !=
local safe callback observed by SnapTrimmer
```

No such callback is installed here.

---

## H2 — `snap_trimmer()` publishes after the state event, not after local completion

The outer `ReplicatedPG::snap_trimmer()` calls:

```text
snap_trimmer_machine.process_event(SnapTrim())
```

and then, in the same worker invocation, checks `need_share_pg_info`. When set, it clears the flag and calls `share_pg_info()` after the PG/map-lock handoff.

The code between those two events contains no wait on the previously queued local transaction.

Therefore the source-level sequence is:

```text
state-machine event
    -> queue local ObjectStore transaction
    -> set publication flag
    -> return from state-machine event
    -> share_pg_info()
```

not:

```text
queue local transaction
    -> local onreadable/ondisk callback
    -> share_pg_info()
```

`PG::share_pg_info()` is itself an outward control-plane action: it constructs `MOSDPGInfo` messages for the acting replicas. The publication studied here is therefore not merely an in-memory flag inside the primary.

---

## H3 — the ObjectStore API distinguishes readable and on-disk completion

At the same source revision, `ObjectStore` exposes:

```text
onreadable
ondisk
onreadable_sync
```

as distinct callback positions on queued transactions.

That API distinction matters because it blocks the shortcut:

```text
queue_transaction returned
    = transaction became readable
    = transaction became on-disk/safe
```

The interface does not define those as one event.

This is historical implementation evidence, not merely a modern interpretation imposed on old code.

---

## H4 — FileStore's convenience overload supplies only `onreadable`

The concrete FileStore overload used by SnapTrimmer performs the equivalent of:

```text
make a one-element transaction list
call queue_transactions(...,
    onreadable = delete-this-transaction callback,
    ondisk = null)
```

The deletion callback is a resource-lifetime/readable-path callback; it is not an `ondisk` callback.

Consequently, the exact SnapTrimmer call site does not ask FileStore to notify it when this transaction reaches the backend's safe/on-disk milestone.

This gives a source-level negative fact stronger than simply saying that no callback was noticed in `WaitingOnReplicas`:

> **the specific overload selected by the call does not bind an `ondisk` continuation at all.**

---

## H5 — queue submission and later application are different FileStore events

In FileStore's queued path, `queue_transactions()` builds an `Op`, assigns a sequence number, performs journal-mode-specific submission/queueing, and returns.

Actual transaction application is performed later by the operation workqueue in `_do_op()`, which calls:

```text
do_transactions(...)
op_apply_finish(...)
```

and later `_finish_op()` dispatches readable callbacks in operation order.

This means the asynchronous API permits:

```text
queue_transaction() returned
    while
filesystem/application work is still pending
```

Whether a particular runtime schedule actually publishes before application on every invocation is not established or required here. The stronger and defensible statement is that **the SnapTrimmer does not impose an application barrier**, and the FileStore API/path is asynchronous enough that submission return cannot be treated as proof of application completion.

---

## H6 — journal/safe completion is another separate milestone

`JournalingObjectStore` tracks at least:

```text
applied_seq
committing_seq
committed_seq
```

and maintains commit waiters separately from operation application.

Its journal submission path encodes transactions and hands them to `journal->submit_entry(...)` with an optional completion context. If a journal completion cannot be used directly, the callback can instead be retained in `commit_waiters` until the relevant commit sequence finishes.

`FileJournal::submit_entry()` itself queues completion state and kicks the writer; submission is not the same function call as later writer completion.

Therefore:

```text
FileStore operation applied/readable
    !=
journal / commit-safe milestone
```

and the SnapTrimmer path waits for neither through a callback before `share_pg_info()`.

---

## H7 — “on-disk” is still not a universal hardware theorem

`FileJournal.cc` is unusually useful as a built-in boundary witness. Its raw-block-device path checks write-cache conditions and warns that journaling is not reliable on older kernels when the disk write cache is enabled. Direct-I/O journal mode adds `O_DIRECT | O_SYNC`.

That evidence supports two distinct statements:

1. Ceph had an explicit local safe/on-disk layer in its software contract;
2. the developers themselves treated actual device/cache behavior as a further condition on reliability.

So even if this SnapTrimmer path had waited for `ondisk`, the repository still should not silently rewrite that as:

```text
proof of physical nonvolatile persistence
under every controller / disk / power-loss model
```

The present source is even narrower: SnapTrimmer does not install the local `ondisk` wait in the first place.

---

# Engineering reconstruction

## E1 — the completion relation crosses two different barriers

Combining the previous June-2011 evidence with this lower-layer slice gives a more exact decomposition:

```text
replicated object-removal operations issued
    ↓
replica apply/ack condition clears
    ↓
in-memory `purged_snaps` advances
    ↓
primary-local PG-info + collection-removal transaction is queued
    ↓
new PG info may be published by `share_pg_info()`

while, separately, the primary-local backend has milestones such as:

queued/submitted
    -> applied/readable
    -> journal/commit-safe
```

The source enforces the first barrier:

```text
replica apply/ack gate
    before
completion publication
```

It does not enforce:

```text
primary-local safe milestone
    before
completion publication
```

These are different correctness dimensions.

---

## E2 — publication can outrun one embodiment without making the relation meaningless

A PG-info message carrying newer `purged_snaps` can be sent while the primary's local representation of that same completion is still below some FileStore milestone.

That does **not** imply the completion relation is fictitious. It means the relation has multiple embodiments with different stabilization times:

```text
primary RAM state
primary queued ObjectStore transaction
primary filesystem/journal embodiment
replica PG-info embodiment
```

The retention question is therefore not merely “does `purged_snaps` exist?” but:

> Which embodiment is authoritative after which failure, and which lower-layer milestone has actually been crossed?

Answering the crash outcome for a particular failure instant requires additional experiment or recovery-path tracing; this slice stops at the exact source-level ordering contract.

---

## E3 — source-level absence of a barrier is not a demonstrated crash bug

The following inference is allowed:

```text
no local-safe wait before publication
    -> publication is not conditioned on that local-safe milestone
```

The following inference is **not** allowed without a fault trace:

```text
no local-safe wait before publication
    -> a crash necessarily leaves replicas believing an unrecoverable false completion
```

Journal replay, PG peering, retained remote info, re-trimming, and other recovery relations can alter the eventual state. Case 153 already shows that some cleanup obligations can be reconstructed rather than replayed byte-for-byte.

So the evidence changes the ordering model without claiming a failure outcome the source does not directly demonstrate.

---

# Controlled comparison — Case 05 EBOFS 2007

[`05-ceph-2007-ebofs-journal-persistence-boundary-deepening.md`](05-ceph-2007-ebofs-journal-persistence-boundary-deepening.md) established an earlier Ceph implementation boundary:

```text
working-state application
    !=
journal admission
    !=
safe callback
    !=
later checkpoint
```

The 2011 FileStore evidence is functionally comparable because its API and implementation again expose distinct submission/application/safe states.

The useful comparison is:

```text
2007 EBOFS:
caller return / update application
    != local safe callback

2011 FileStore:
queued operation / onreadable path
    != ondisk / journal-safe path
```

The comparison stops there. It does **not** claim:

- identical journal formats;
- identical checkpoint algorithms;
- unchanged code descent from EBOFS into FileStore;
- identical hardware assumptions;
- identical RADOS acknowledgement contracts.

The reason to retain the comparison in `technical-retention` is narrower: **a higher-level statement of progress can cross an API boundary whose local persistence stages remain distinct.**

---

# Explicit non-claims

This slice does **not** establish any of the following:

1. that `queue_transaction()` loses data;
2. that `share_pg_info()` always executes before local filesystem application in every schedule/configuration;
3. that FileStore's `onreadable` callback is a stable-storage guarantee;
4. that FileStore's `ondisk` callback is equivalent to physical NAND/platter persistence under every device-cache model;
5. that the June-2011 SnapTrimmer fix was incorrect in the race it explicitly targeted;
6. that replica `waitfor_disk` and primary-local FileStore `ondisk` mean the same event;
7. that `RepGather::applied` means local durable media commit;
8. that `waitfor_ack.empty()` means every remote medium is durably committed;
9. that `waitfor_disk.empty()` by itself proves every relevant lower-layer cache is power-fail safe;
10. that PG-info publication is a client-visible write acknowledgement;
11. that a crash in the publication-before-safe window necessarily produces an unrecoverable inconsistency;
12. that journal replay cannot recover the primary-local transaction;
13. that replica-local retained `purged_snaps` can never help recover/reconstruct cleanup state;
14. that `purged_snaps` alone is sufficient authority under every peering/currentness state;
15. that collection removal equals lower-layer allocator reuse;
16. that allocator reuse equals sanitization;
17. that 2011 FileStore behavior applies unchanged to later FileStore revisions;
18. that this ordering applies to BlueStore;
19. that EBOFS and FileStore share an identical durability implementation;
20. that same-company/source-tree chronology alone proves a direct implementation genealogy.

---

# Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `SnapTrimmer`, `purged_snaps`, `FileStore`, and `RepGather` found no dedicated packet covering this seam.

Keep here:

- the exact SnapTrimmer call-site ordering;
- the `onreadable` / `ondisk` distinction needed to qualify completion publication;
- the bounded relation between retained completion evidence and its local persistence embodiment;
- the controlled Case-05 comparison.

Route primarily to `computing-archaeology` if later pursued:

- full FileStore journal-mode evolution;
- detailed `FileJournal` / kernel / filesystem history;
- EBOFS → FileStore design genealogy;
- device-cache / barrier support across kernels and controllers;
- performance consequences of journal mode selection.

---

# Remaining debt after this slice

This slice closes the **source-level callback/order** part of the former debt “inspect FileStore/ObjectStore callback and crash semantics if a stronger claim about primary-local durable completion before PG-info publication becomes necessary.”

Still open:

- fault-inject the exact 2011 path at `share_pg_info()` versus FileStore apply/journal-safe boundaries under selected journal modes;
- trace restart/peering outcomes for those exact interruption points;
- determine whether and when later Ceph revisions introduced, removed, or changed a primary-local publication barrier for snapshot-trim completion;
- keep hardware persistence validation below FileStore's software safe boundary separate;
- keep allocator reuse and sanitization as separate evidence questions.

No canonical maturity promotion follows. Case 153 remains **`grounded`**.