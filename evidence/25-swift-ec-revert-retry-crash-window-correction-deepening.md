# Case 25 deepening — Swift EC handoff reversion retry/crash window and candidate-set correction

**Status:** bounded deepening complete  
**Canonical case:** [`Case 25 — OpenStack Swift EC Overwrites`](../cases/25-openstack-swift-ec-overwrite-durable-currentness.md)  
**Evidence class:** current implementation / unit-test corroboration / engineering reconstruction  
**Case maturity:** remains `grounded`

## Purpose

This addendum closes two tightly coupled Case 25 debts in one bounded current-implementation slice:

1. correct an earlier repository claim that current Swift intersects per-destination `in_sync_objs` maps before local handoff purge; and
2. bound the **process-crash / later-pass** behavior when destination synchronization has succeeded but local purge has not yet completed.

The correction matters because source-retirement authority should be described from the implementation actually present in Swift, not from an inferred set-algebra policy.

The bounded question is:

> **What survives, and what must be re-established, if the EC reconstructor process stops after some or all remote reversion work but before all local handoff fragments are purged?**

This is not a power-cut validation of the receiver storage stack. It is a source-level process/retry boundary.

---

## Source custody

### P1 — current Swift reconstructor

Current OpenStack Swift master inspected at:

`e60791398bfefc0f2b3c4b0012c292d983248765` — 2026-09-24

<https://github.com/openstack/swift/blob/e60791398bfefc0f2b3c4b0012c292d983248765/swift/obj/reconstructor.py>

The same relevant `_revert()` merge/gate behavior is present in the previously pinned repository witness:

`6b83d7f3fcf95539b17dc1e3f5f1074c29afc487` — 2026-09-20.

### P2 — current SSYNC sender

<https://github.com/openstack/swift/blob/e60791398bfefc0f2b3c4b0012c292d983248765/swift/obj/ssync_sender.py>

### P3 — reconstructor unit tests

Pinned test witness already used by this case:

`6b83d7f3fcf95539b17dc1e3f5f1074c29afc487`

<https://github.com/openstack/swift/blob/6b83d7f3fcf95539b17dc1e3f5f1074c29afc487/test/unit/obj/test_reconstructor.py>

The tests are used only to corroborate multi-pass cleanup and local-retirement behavior already visible in the production path.

### P4 — prior Case 25 handoff-retirement note

[`25-swift-ec-handoff-revert-retirement-boundary-deepening.md`](25-swift-ec-handoff-revert-retirement-boundary-deepening.md)

This addendum supersedes that note only where it described a current **per-object intersection across destination result sets**. The broader ordering claim — successful reversion work before local handoff purge — remains valid.

---

## Historical / implementation record (`H/P`)

### H/P1 — normal REVERT jobs are not generic fan-out replication jobs

The current `process_job()` documentation in P1 distinguishes the job types:

- a primary `SYNC` job may define partner nodes;
- a non-primary `REVERT` job normally defines the proper/new home for the fragment index;
- job construction can produce multiple `sync_to` nodes for the same fragment index when the EC policy has a duplication factor greater than one.

Therefore `job['sync_to']` should not be interpreted as a generic quorum set whose per-object results are necessarily combined by an intersection rule.

### H/P2 — `_revert()` uses map update, not intersection

The current `_revert()` path initializes:

```text
syncd_with = 0
reverted_objs = {}
```

For each destination it calls the SSYNC sender. On success it does:

```text
syncd_with += 1
reverted_objs.update(in_sync_objs)
```

Only after the loop does it call local cleanup, and only when:

```text
syncd_with >= len(job['sync_to'])
```

This is **not** set intersection. It is dictionary merge/update plus an all-required-session success gate.

The earlier repository wording:

```text
purge candidates = I1 ∩ I2 ∩ ... ∩ In
```

was therefore inaccurate for the pinned/current implementation and is superseded by this note.

### H/P3 — one failed required destination withholds the cleanup call

Because `delete_reverted_objs()` is reached only after all required destination sessions have reported success, a partial multi-destination success does not immediately trigger local purge in that pass.

The current ordering is:

```text
for every required sync_to destination:
    run SSYNC
    collect successful-session candidate maps

if successful-session count < required destination count:
    do not call local purge
```

That remains a strong retention gate even though the candidate maps are merged rather than intersected.

### H/P4 — in normal sender mode, successful SSYNC returns the local offered set after requested updates complete

P2 documents the sender return value as `(success, can_delete_objs)` where `can_delete_objs` maps objects that are in sync with the receiver.

In normal mode (`remote_check_objs is None`), the sender:

1. builds `available_map` from the local diskfiles offered during `MISSING_CHECK`;
2. receives `send_map`, the subset/parts the receiver requests;
3. executes `updates(..., send_map)`;
4. if the exchange completes successfully, sets:

```text
can_delete_obj = available_map
```

Thus the normal successful session treats the locally offered set as deletion-eligible **after** the receiver-specific requested work has completed.

This explains why current `_revert()` does not need a separate per-object intersection to express ordinary success for every destination: the whole required destination session must succeed before cleanup is called, and each successful normal sender returns its successfully qualified offered set.

### H/P5 — receiver state is re-observed by `MISSING_CHECK` on every later SSYNC pass

P2's `missing_check()` reconstructs `available_map` by enumerating the sender's current local disk state and builds `send_map` from what the receiver says it still wants.

Therefore a later reconstructor pass does not have to trust an in-memory record saying:

```text
receiver X succeeded last time
```

It can re-run the protocol against the receiver's **current** state.

If the receiver already has suitable state, that object need not cause the same payload transfer again; the missing-check/update protocol re-establishes the synchronization relation from current on-disk state.

### H/P6 — local handoff purge is object-by-object, not one batch transaction

P1's `delete_reverted_objs()` iterates the candidate object map. For each object it reopens the local diskfile by hash/fragment index, selects the matching data state, and calls `df.purge(...)`.

The helper catches `DiskFileNotExist` for an object that disappeared/reclaimed/raced and logs `DiskFileError` without turning the whole candidate map into one atomic deletion transaction.

After object-level work it attempts suffix-directory cleanup.

The source therefore exposes a natural interruption window:

```text
some candidate objects purged
    + some candidate objects still present
```

if the process stops during cleanup.

### H/P7 — unit tests explicitly exercise progress across more than one reconstructor run

P3 includes `test_delete_reverted_max_objects_per_revert`.

With a configured per-pass object limit, the first reconstructor run synchronizes and purges only a subset, leaves one datafile present, and reports a handoff remaining. A subsequent reconstructor run then synchronizes/purges the remaining object.

This is not a crash-injection test, but it is direct implementation-level evidence that:

```text
residual local handoff state after one run
    -> is discoverable and processable in a later run
```

rather than requiring an in-memory continuation object from the earlier run.

### H/P8 — current tests also verify successful reversion can remove the local hashpath

P3 contains REVERT tests where a successful SSYNC callback returns the relevant object/timestamp map and `process_job()` removes the local hashpath. Other tests deliberately mutate the local fragment during SSYNC and verify that inappropriate local removal does not occur.

These tests corroborate that local cleanup is tied to the current local/timestamp state rather than being a blind “remote once acknowledged, delete path unconditionally” action.

---

## Engineering reconstruction (`E`)

### E1 — remote success and local retirement are separate transitions

Current Swift has a non-atomic interval:

```text
remote placement synchronized
    + local handoff still present
```

This interval is not an error by itself. It is temporarily **extra embodiment**.

The old copy becomes locally disposable only when the current pass reaches its cleanup gate and object-level purge actually executes.

### E2 — crash before all required destination sessions complete is fail-retentive for the local handoff

For a multi-destination REVERT job:

```text
D1 succeeds
D2 not yet attempted / fails
process stops
```

Since the cleanup call is after the all-destination success check, the normal source path has not yet authorized local purge.

The local handoff therefore remains available for a later pass, subject to independent races/reclamation not modeled here.

The next pass re-runs SSYNC and re-derives receiver needs from current state.

### E3 — crash after remote success but before local purge leaves an extra old embodiment

For the bounded process-crash seam:

```text
all required SSYNC sessions succeed
process stops before delete_reverted_objs()
```

no local candidate has yet been purged by this path.

On a later pass:

1. surviving local handoff diskfiles are enumerated again;
2. the receiver is asked again what it needs;
3. receiver state created by the earlier successful pass can be recognized as already suitable or can request only missing parts;
4. a newly successful pass can re-authorize local purge.

The important distinction is:

```text
remote success from an earlier process lifetime
    != retained sender-side cleanup authority

receiver state is re-observed
    -> cleanup authority is reconstructed
```

This is a **reconstructive retry** pattern, not proof of a durable sender-side session journal.

### E4 — crash during local purge can leave a mixed local residue

Because cleanup iterates objects individually:

```text
object A purged
object B purged
process stops
object C still present
object D still present
```

A later scan sees only the surviving local objects that still generate work.

Already-purged objects do not need a sender-side continuation record merely to remain absent. Surviving objects still carry the local payload/state needed for a fresh missing-check and reversion attempt.

This supports:

```text
cleanup progress can be embodied by changed local disk state
    rather than one explicit durable cleanup-progress record
```

for this bounded path.

### E5 — a repeated SSYNC does not imply repeated payload transfer

Because missing-check is receiver-relative, retrying the protocol after a process restart is not equivalent to blindly re-copying all bytes.

```text
repeat synchronization protocol
    != repeat full payload transmission
```

The receiver may already be current and request nothing, or request only parts not yet suitable.

This is why re-observation can replace a sender-side “last session succeeded” token without necessarily paying the full data-transfer cost again.

### E6 — candidate aggregation and destination success are different dimensions

The current code has two separate pieces:

```text
candidate aggregation:
    reverted_objs.update(in_sync_objs)

session gate:
    syncd_with >= len(job['sync_to'])
```

Conflating them produced the earlier incorrect “intersection” description.

A better reconstruction is:

```text
candidate membership
    + all required destination sessions succeeded
    -> candidate may enter local cleanup
```

For ordinary single-destination REVERT jobs, there is no cross-destination set algebra to perform at all.

### E7 — sender process memory is not the only place continuity can live

The retry path demonstrates at least three different retention loci:

```text
receiver disk/currentness state
local surviving handoff disk state
current ring/job reconstruction
```

The reconstructor's volatile `reverted_objs` dictionary is useful within one pass, but continuity of the repair obligation does not require that exact dictionary to survive process death.

### E8 — this closes only process-level retry, not lower-stack power-loss persistence

Evidence 25-3 separately shows the receiver-side file/directory sync requests that precede normal SSYNC success in the pinned POSIX path.

This note does not convert those calls into a universal theorem about sudden power loss across filesystem, kernel, controller, device-cache, firmware, or media behavior.

Therefore:

```text
reconstructor process retry is reconstructible
    != receiver state survives every power-loss model
```

---

## Corrected bounded state machine

```text
[local handoff object exists]
        |
        v
[build REVERT job from current local/ring state]
        |
        v
[SSYNC required destination(s)]
        |
        +-- any required session fails ----------+
        |                                        |
        |                                        v
        |                              [no local purge call]
        |                                        |
        |                                        v
        |                              [later pass retries]
        |
        v
[all required sessions succeeded]
        |
        v
[merge successful sender candidate maps]
        |
        v
[delete_reverted_objs(candidate map)]
        |
        +-- process stops before cleanup --------> [all local candidates remain]
        |
        +-- process stops mid-cleanup -----------> [mixed local residue]
        |
        v
[local candidate purged object-by-object]

Later pass for any residue:

[enumerate surviving local state]
        -> [MISSING_CHECK receiver current state]
        -> [send only what receiver requests]
        -> [new successful-session evidence]
        -> [local purge]
```

This is an engineering reconstruction of P1–P3, not an upstream Swift diagram.

---

## Functional analogy (`F`)

### F1 — bounded analogy to restartable cleanup / mark-and-rescan patterns

Functionally, this path resembles systems in which cleanup progress need not be represented by one durable transaction log because the remaining work can be rediscovered from surviving state:

```text
completed part changes durable/observable state
remaining part remains discoverable
next pass recomputes what is still necessary
```

This is only a functional comparison. It is not evidence that Swift derived the design from garbage collection, filesystems, databases, or Flash translation layers.

### F2 — relation to Case 04 mapped Flash

The useful comparison remains:

```text
replacement embodiment/current relation established
    != old embodiment already removed
```

But Swift adds a distributed re-observation boundary: after a process restart, the receiver's current state can be queried again before old local state is retired.

No genealogy is claimed.

---

## Philosophical interpretation (`I`)

A narrow interpretation is:

> The continuity of a maintenance obligation need not consist in preserving the exact volatile control object that represented it during one process lifetime. It can instead be regenerated from retained local state, remote state, and current placement rules.

This should not be generalized into “state never needs checkpoints.” It applies only where enough authoritative/relevant state remains observable to reconstruct the obligation safely.

The correction also sharpens a methodological point for this repository:

> A visually elegant set-theoretic reconstruction must yield to the actual program operation when source code exposes a different control structure.

---

## Explicit non-claims

This deepening does **not** claim:

1. that `reverted_objs.update(...)` is mathematically identical to set union in every timestamp/key-conflict case;
2. that every historical Swift release uses the same candidate aggregation or retry structure;
3. that one successful destination proves whole-object EC durability;
4. that the receiver state necessarily survives arbitrary host/power loss after SSYNC success;
5. that remote synchronization and local purge are atomic;
6. that `delete_reverted_objs()` itself has a durable transaction journal;
7. that the sender persists a durable “destination X succeeded” session record across process restart;
8. that lack of such a sender record is a defect — the current path can re-observe receiver state;
9. that every retry performs zero payload transfer;
10. that ring membership/placement cannot change between passes;
11. that a later pass necessarily chooses the same destination identity after ring change;
12. that object-level `df.purge()` is power-fail atomic;
13. that suffix-directory removal is transactionally coupled to every object purge;
14. that a residual handoff fragment is always the last or only usable coded fragment;
15. that local purge equals logical object deletion;
16. that process-level restart reconstruction proves lower-layer persistence;
17. that the current implementation's normal successful sender semantics apply unchanged to `remote_check_objs` mode;
18. that multi-destination REVERT jobs are the common case — ordinary REVERT jobs normally target the proper/new home, while duplication policies can add destinations;
19. that current unit tests constitute physical fault-injection evidence;
20. that this source correction changes the canonical Case 25 maturity beyond `grounded`.

---

## What this closes

This slice closes two bounded debts for the current implementation:

### Closed A — current candidate-set semantics

The repository must no longer describe current handoff cleanup as a per-destination object-set intersection.

The actual current source uses:

```text
reverted_objs.update(in_sync_objs)
```

and separately requires all configured `sync_to` sessions to succeed before invoking local cleanup.

### Closed B — process restart after remote success / before local cleanup

At source/test level, the retry path is now bounded:

- if cleanup was never reached, local handoff state remains to be rediscovered;
- if cleanup was interrupted, surviving local objects remain discoverable;
- a later pass re-runs missing-check against receiver current state;
- the receiver can avoid requesting payload it already has;
- multi-pass unit tests demonstrate that residual handoff state can be processed and purged on a later run.

The still-open stronger experiment is **explicit crash/fault injection** at the exact instruction boundaries, especially combined with filesystem or host power loss.

---

## Remaining bounded debt

1. **physical power-cut validation** around receiver file/directory sync and durable-name publication;
2. **explicit process-kill fault injection** between final SSYNC return and `delete_reverted_objs()`, and during the object purge loop;
3. **ring/rebalance change between passes**, including whether a different destination set changes retirement reasoning;
4. **historical evolution** of the current `dict.update` + all-session gate and the older reversion cleanup code;
5. **whole-object reconstructability under correlated failures**, kept separate from this local source-retirement path.

---

## Related-repository boundary

Fresh companion searches for `Swift SSYNC` and `OpenStack Swift` found no dedicated reusable packet in `tmzncty/computing-archaeology`.

This note therefore keeps only the retention-specific retry/candidate-authority boundary here. Broad Swift replication history, SSYNC protocol genealogy, filesystem durability history, and cluster-rebalance archaeology remain outside this case unless needed for another bounded retention claim.
