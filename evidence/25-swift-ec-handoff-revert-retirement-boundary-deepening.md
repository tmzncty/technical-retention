# Case 25 deepening — Swift EC handoff reversion and source-retirement boundary

**Status:** bounded deepening complete  
**Canonical case:** [`Case 25 — OpenStack Swift EC Overwrites`](../cases/25-openstack-swift-ec-overwrite-durable-currentness.md)  
**Evidence class:** implementation / historical implementation / protocol reconstruction  
**Case maturity:** remains `grounded`

## Purpose

This addendum deepens one narrow retention boundary in OpenStack Swift's erasure-coded object reconstructor:

> **When an EC fragment exists on a handoff device, what evidence is required before Swift may retire that local handoff embodiment after sending state back toward primary placements?**

The question is intentionally narrower than generic EC durability, rebalance correctness, or object reconstruction. The canonical case already establishes fragment-archive identity, timestamp cohorts, durable-state representation, GET reconstruction, reconstructor repair, and durable-marker propagation. This note instead isolates the disposal boundary for a redundant handoff embodiment.

The useful distinction is:

```text
handoff fragment exists
    != primary placement restored

SSYNC session attempted
    != receiver update succeeded

one destination synchronized
    != local handoff copy safe to purge

local handoff copy purged
    != logical object/version deleted
```

The strongest current implementation evidence is pinned to OpenStack Swift master commit:

`6b83d7f3fcf95539b17dc1e3f5f1074c29afc487` (2026-09-20).

A historical anchor is the original EC reconstructor change:

`647b66a2ce4c85c43dcca49776d35c5ebb9cf15e`.

---

## Source set

### P1 — historical EC reconstructor introduction

OpenStack Swift commit `647b66a2ce4c85c43dcca49776d35c5ebb9cf15e` introduced the EC reconstructor and included reversion cleanup logic:

<https://github.com/openstack/swift/commit/647b66a2ce4c85c43dcca49776d35c5ebb9cf15e>

The historical implementation is relevant for one bounded point only: EC handoff cleanup was coupled to successful reversion/synchronization work rather than being performed before that work.

This addendum does **not** claim that every detail of the 2026 per-object/all-destination intersection rule existed unchanged in this first implementation.

### P2 — current reconstructor implementation

Pinned current source:

<https://github.com/openstack/swift/blob/6b83d7f3fcf95539b17dc1e3f5f1074c29afc487/swift/obj/reconstructor.py>

The `_revert()` path:

1. iterates the destinations in `job['sync_to']`;
2. invokes an SSYNC sender for each destination;
3. receives `(success, in_sync_objs)`;
4. aborts the reversion pass on a failed destination session;
5. intersects the per-destination `in_sync_objs` sets/maps;
6. calls `_delete_reverted_objs()` only for objects surviving that intersection.

The cleanup helper then purges the local handoff fragment state for those selected objects and updates reconstructor statistics.

### P3 — current SSYNC sender

Pinned current source:

<https://github.com/openstack/swift/blob/6b83d7f3fcf95539b17dc1e3f5f1074c29afc487/swift/obj/ssync_sender.py>

The sender performs the missing-check / update exchange and returns session success together with per-object synchronization information. The exchange distinguishes receiver state already considered matching from receiver state that requires PUT/POST/DELETE subrequests.

### P4 — current SSYNC receiver

Pinned current source:

<https://github.com/openstack/swift/blob/6b83d7f3fcf95539b17dc1e3f5f1074c29afc487/swift/obj/ssync_receiver.py>

The receiver executes object-server subrequests during the update phase and reports subrequest outcomes. Update failures can make the replication session fail rather than silently count as successful synchronization.

### P5 — current reconstructor tests

Pinned current tests:

<https://github.com/openstack/swift/blob/6b83d7f3fcf95539b17dc1e3f5f1074c29afc487/test/unit/obj/test_reconstructor.py>

These tests provide implementation-level corroboration for reversion/purge behavior. They are secondary to the production path for this note.

### P6 — Swift EC overview

Current EC overview:

<https://github.com/openstack/swift/blob/6b83d7f3fcf95539b17dc1e3f5f1074c29afc487/doc/source/overview_erasure_code.rst>

The documentation explains the object reconstructor's role in repairing and moving EC fragment archives, including handoff reversion. It is used here as product documentation, not as a substitute for the cleanup condition in code.

---

## Historical record (`H/P`)

### H/P1 — handoff placement is a temporary embodiment, not a new logical object

Swift may store an EC fragment archive on a handoff location when a normal primary destination cannot accept the fragment. The handoff copy therefore represents the same logical object/version and fragment state under a temporary placement condition.

The retention problem is not:

```text
should this object still exist?
```

but:

```text
has enough replacement placement state been established
that this temporary local embodiment may be retired?
```

### H/P2 — the original EC reconstructor already orders reversion work before local cleanup

P1's historical implementation introduced explicit cleanup of reverted handoff objects after successful synchronization/reversion work.

This is enough to establish a historical ordering relation:

```text
attempt replacement placement / synchronization
    -> successful reversion evidence
    -> local handoff cleanup
```

It is **not** enough to establish that the initial implementation had exactly the same modern intersection semantics, error paths, or SSYNC result representation.

### H/P3 — current `_revert()` requires successful destination sessions before local purge

In P2, the reconstructor loops over every destination in `job['sync_to']`. If a destination's SSYNC operation reports failure, `_revert()` returns before the local purge step.

Thus, for the current pinned implementation:

```text
one required destination SSYNC fails
    -> this reversion pass does not reach local handoff purge
```

That is a stronger statement than saying merely that Swift “tries to copy data before deleting it.” The cleanup is gated by protocol outcome.

### H/P4 — session success alone is not the complete per-object purge condition

Each successful destination SSYNC returns an `in_sync_objs` result. `_revert()` intersects those results across the destinations.

Therefore a particular handoff object becomes locally purge-eligible only if it remains in the intersection after all required destination exchanges in the job.

The current implementation can be represented as:

```text
R := unset

for destination D in job.sync_to:
    success, I_D := ssync(D)

    if not success:
        stop; do not purge in this pass

    if R is unset:
        R := I_D
    else:
        R := R ∩ I_D

purge locally only objects in R
```

The exact Python data representation is less important than the observable policy: local source retirement is based on **per-object agreement across the destination exchanges**, not merely one successful connection or one successful target.

### H/P5 — SSYNC separates missing-state discovery from state transfer

P3's sender performs a missing-check phase before the update phase. A receiver may already have matching state, or it may require a PUT/POST/DELETE update.

Consequently:

```text
object is in-sync with receiver after exchange
```

is broader than:

```text
sender transmitted a new payload body during this exchange
```

Some objects require no transfer because the receiver already has suitable state. The retained evidence needed for source retirement is a synchronization relation, not a byte counter.

### H/P6 — protocol attempt != receiver update success

P3/P4 distinguish initiating SSYNC from completing required receiver-side object-server subrequests. Failed update work is tracked and may fail the session.

Therefore:

```text
TCP/protocol session existed
    != receiver update succeeded
    != sender may infer the object is synchronized
```

This matters because otherwise a transiently reachable primary could be mistaken for a restored placement.

### H/P7 — successful reversion culminates in local fragment purge, not logical deletion

P2's `_delete_reverted_objs()` removes local handoff fragment state selected by the successful intersection and records reconstructor statistics.

The operation is a **placement cleanup**. It is not a client DELETE and does not mean the logical object/version has been retired from Swift.

---

## Engineering reconstruction (`E`)

### E1 — the handoff fragment carries a retention obligation while placement repair is incomplete

A handoff fragment can be modeled as a temporary embodiment with a conditional retirement rule:

```text
handoff embodiment H exists
    + primary-placement repair not yet sufficiently evidenced
    -> retain H
```

Once the current reconstructor has accumulated sufficient destination-specific synchronization evidence for an object:

```text
all required destination SSYNC sessions succeed
    + object belongs to each destination's in-sync result
    -> H becomes eligible for local retirement
```

“Eligible” is deliberately used instead of “globally unnecessary.” The code proves a local cleanup condition, not every possible global durability property.

### E2 — placement currentness is distinct from payload existence

At least two state classes are involved:

```text
A. payload-bearing state
   local EC fragment archive on the handoff device

B. placement/currentness evidence
   whether required destination exchanges establish
   that the object's relevant state is synchronized there
```

A may remain byte-for-byte intact while B is false. Conversely, B can become strong enough to authorize disposal of A.

This is a direct technical distinction, not a metaphor.

### E3 — source-retirement authority is accumulated relationally

For a multi-destination revert, the current cleanup decision is not attached to a single receiver. It is the result of combining destination-specific evidence.

```text
I_1 = objects synchronized with destination 1
I_2 = objects synchronized with destination 2
...
I_n = objects synchronized with destination n

purge candidates = I_1 ∩ I_2 ∩ ... ∩ I_n
```

This yields an important retention principle:

```text
replacement evidence can be compositional
```

The payload copy being retired is local, but the evidence authorizing its retirement is distributed across relationships to several remote placements.

### E4 — failed destination work preserves the old embodiment by withholding retirement authority

A failed destination SSYNC does not need to mutate the handoff payload to preserve it. The reconstructor can preserve retention simply by failing to reach the purge operation.

Thus:

```text
preservation
    != explicit copy operation
```

Sometimes preservation is achieved by withholding permission to discard an already-retained embodiment.

### E5 — receiver-side “in sync” evidence is stronger than reachability but weaker than a universal stable-media theorem

SSYNC success is meaningful protocol evidence: required receiver-side updates must complete successfully enough for the sender to report success/in-sync state.

But this addendum does not elevate that result to a stronger storage claim than the sources support.

Specifically:

```text
SSYNC success / in-sync evidence
    != proof that every byte is physically on nonvolatile media
       under every filesystem, controller, cache, or power-failure model
```

The receiver/object-server persistence boundary is a separate research slice.

### E6 — local retirement is not equivalent to whole-object EC reconstructability

The reconstructor operates on fragment archives and placement jobs. Its local purge condition is not itself the mathematical statement:

```text
there exist >= ec_ndata mutually usable fragments
for the same timestamp under every simultaneous failure scenario
```

The canonical case treats coded-cohort reconstructability separately.

Therefore:

```text
safe under this local handoff-retirement rule
    != universal proof of whole-object durability
```

### E7 — a temporary redundant embodiment can outlive the event that created it

The handoff copy may have been created because a primary was unavailable earlier. Once created, it persists until later repair/reversion evidence authorizes cleanup.

The retention interval is therefore bounded by **repair state**, not just by the duration of the original outage:

```text
primary unavailable
    -> handoff created
primary later available
    != immediate handoff disposal
successful reversion evidence
    -> disposal becomes allowed
```

### E8 — retirement is a distinct transition from publication

A remote destination may accept synchronized state before the source handoff fragment is purged. That interval is meaningful:

```text
replacement placement established
    + old handoff embodiment still exists
```

The system temporarily has extra redundancy while cleanup lags synchronization.

This is different from protocols that make replacement publication and old-copy invalidation one atomic event.

---

## Bounded state machine

A compact reconstruction of the current source-retirement path is:

```text
[local handoff fragment exists]
        |
        v
[SSYNC destination 1]
        |
        +-- failure ------------------------------+
        |                                         |
        |                                         v
        |                              [retain local handoff]
        v
[per-object in-sync set I1]
        |
        v
[SSYNC destination 2 ... n]
        |
        +-- any failure --------------------------+
        |                                         |
        |                                         v
        |                              [retain local handoff]
        v
[intersection I1 ∩ I2 ... ∩ In]
        |
        v
[object is in intersection?]
        |
        +-- no --> [retain local handoff]
        |
        v yes
[eligible for local purge]
        |
        v
[handoff embodiment retired]
```

This graph is an engineering reconstruction of P2/P3, not an upstream Swift diagram.

---

## Functional analogy (`F`)

### F1 — bounded analogy to Case 04 flash relocation

Case 04 distinguishes establishing a replacement physical embodiment from retiring the old one. Swift handoff reversion has a similar **functional shape**:

```text
old / temporary embodiment retained
    -> replacement/current placement receives state
    -> evidence of successful publication/currentness accumulates
    -> old embodiment may be retired
```

This analogy is useful because both cases warn against collapsing:

```text
new location has been attempted
```

into:

```text
old location is already disposable
```

### F2 — no genealogy claim

Nothing in P1–P6 establishes that Swift's designers borrowed this pattern from flash FTLs, filesystems, RAID repair, database replication, or any other specific technology.

The comparison is **functional only**.

---

## Philosophical interpretation (`I`)

A minimal interpretation is:

> Retention can be an obligation to keep a redundant embodiment until replacement placement has accumulated sufficient evidence to authorize disposal.

This is weaker and more precise than saying “the data survives because there are copies.” The engineering question is not only whether multiple copies physically exist, but which relations make one copy legitimately disposable.

A second bounded observation follows:

```text
continuity of payload
    != continuity of a particular physical copy
```

Swift may preserve the logical object's coded state while intentionally retiring one handoff embodiment after replacement placement has been sufficiently established.

These are interpretations of the engineering pattern, not statements from OpenStack project documentation.

---

## Explicit non-claims

This deepening does **not** claim:

1. that one primary acknowledgement proves the whole EC object durable;
2. that an SSYNC success means every receiver byte has reached stable nonvolatile media under every crash/power-failure model;
3. that the local handoff fragment being purged was the last surviving usable fragment;
4. that local handoff purge is a logical object/version DELETE;
5. that remote synchronization and local purge form one globally atomic transaction;
6. that every historical Swift release has the current 2026 all-destination/per-object intersection semantics;
7. that `handoff_delete` from the object replicator defines EC reconstructor behavior;
8. that a successful protocol exchange proves the ring cannot change immediately afterward;
9. that all destination nodes are failure-independent;
10. that current code by itself proves behavior under sudden process death between remote success and local purge;
11. that the sources establish an fsync/stable-media boundary for every receiver-side update;
12. that a handoff is semantically equivalent to a permanent primary placement;
13. that Swift derives this pattern from flash mapping, RAID, databases, or another prior-art lineage.

---

## What this closes

This slice closes the narrow Case 25 question:

> **Does Swift EC immediately discard a handoff fragment after merely attempting to send it toward a primary?**

For the pinned current implementation, no. Local purge is downstream of successful destination SSYNC outcomes and per-object intersection of destination-specific in-sync evidence.

It also establishes a historical lower bound: the original EC reconstructor already placed successful reversion/synchronization before cleanup, without assuming today's exact implementation shape existed unchanged.

---

## Remaining bounded debt

The highest-value next slices are now narrower:

1. **receiver persistence boundary** — what exact object-server/diskfile conditions stand behind a successful SSYNC update response, including rename/fsync ordering where applicable;
2. **crash between remote success and local purge** — show concrete restart behavior when the process or host dies after destination success but before `_delete_reverted_objs()` completes;
3. **partial success across passes** — determine how repeated reconstructor runs reuse or rediscover earlier successful destination state rather than relying on volatile sender evidence;
4. **ring evolution during reversion** — bound what happens when placement changes while a handoff job is being reverted;
5. **historical evolution** — identify when the modern per-object intersection semantics entered the reconstructor and whether earlier releases had materially different source-retirement gates;
6. **receiver-side fault injection** — distinguish acknowledged object-server subrequest success from storage-device power-loss persistence under realistic filesystems/controllers.

These should remain separate slices. None is required to support the narrower conclusion established here.

---

## Project-level retention summary

```text
handoff payload retained
    until
replacement placement is sufficiently evidenced

replacement placement evidence
    = per-destination synchronization result
      combined across required destinations

retirement of the local handoff embodiment
    != deletion of the logical object
    != proof of universal EC durability
```

The important retention object in this case is therefore not only a fragment archive. It is also the **authority to stop retaining that fragment at a temporary location**.
