# Case 25 deepening — Swift EC handoff reversion and source-retirement boundary

**Status:** bounded deepening complete; current-source correction applied 2026-09-24  
**Canonical case:** [`Case 25 — OpenStack Swift EC Overwrites`](../cases/25-openstack-swift-ec-overwrite-durable-currentness.md)  
**Evidence class:** implementation / historical implementation / protocol reconstruction  
**Case maturity:** remains `grounded`

## Correction notice

An earlier revision of this note incorrectly described the current reconstructor as taking an **intersection** of per-destination `in_sync_objs` maps before local purge.

Direct reinspection of current OpenStack Swift source shows that `_revert()` actually does:

```text
reverted_objs.update(in_sync_objs)
```

for every successful destination session, and separately requires:

```text
syncd_with >= len(job['sync_to'])
```

before calling `delete_reverted_objs()`.

The current implementation therefore has a **candidate-map merge/update + all-required-session-success gate**, not a per-object intersection rule.

The correction and the process-retry consequences are developed in:

[`25-swift-ec-revert-retry-crash-window-correction-deepening.md`](25-swift-ec-revert-retry-crash-window-correction-deepening.md).

The broader conclusion of this note remains intact: Swift does not purge a local handoff embodiment merely because a send was attempted; purge is downstream of successful reversion work.

---

## Purpose

This addendum isolates one narrow retention boundary in OpenStack Swift's erasure-coded object reconstructor:

> **When an EC fragment exists on a handoff device, what evidence is required before Swift may retire that local handoff embodiment after sending state back toward its proper placement?**

The useful distinctions are:

```text
handoff fragment exists
    != proper placement restored

SSYNC attempted
    != receiver synchronization succeeded

successful remote synchronization
    != local handoff already purged

local handoff fragment purged
    != logical object/version deleted
```

Current implementation claims are checked against OpenStack Swift master commit:

`e60791398bfefc0f2b3c4b0012c292d983248765` (2026-09-24),

with the same relevant behavior present in the earlier pinned witness:

`6b83d7f3fcf95539b17dc1e3f5f1074c29afc487` (2026-09-20).

A historical anchor remains the original EC reconstructor change:

`647b66a2ce4c85c43dcca49776d35c5ebb9cf15e`.

---

## Source set

### P1 — historical EC reconstructor introduction

<https://github.com/openstack/swift/commit/647b66a2ce4c85c43dcca49776d35c5ebb9cf15e>

This establishes the historical lower bound that EC handoff cleanup followed successful reversion/synchronization work rather than preceding it.

It does not establish that all modern details existed unchanged at introduction.

### P2 — current reconstructor implementation

<https://github.com/openstack/swift/blob/e60791398bfefc0f2b3c4b0012c292d983248765/swift/obj/reconstructor.py>

Current `process_job()` documentation distinguishes:

- `SYNC` work from primary nodes;
- `REVERT` work from non-primary/handoff or rebalance state;
- ordinary REVERT targeting the proper/new home for the fragment index;
- possible multiple `sync_to` nodes when the EC duplication factor requires them.

Current `_revert()`:

1. iterates `job['sync_to']`;
2. invokes an SSYNC sender;
3. receives `(success, in_sync_objs)`;
4. increments `syncd_with` and merges candidates with `reverted_objs.update(in_sync_objs)` on success;
5. calls `delete_reverted_objs()` only after all configured destination sessions succeeded.

### P3 — current SSYNC sender

<https://github.com/openstack/swift/blob/e60791398bfefc0f2b3c4b0012c292d983248765/swift/obj/ssync_sender.py>

In normal sender mode, SSYNC:

1. builds a local `available_map` during `MISSING_CHECK`;
2. receives a receiver-specific `send_map` describing what data/meta is wanted;
3. performs the required update subrequests;
4. after successful completion, returns `available_map` as `can_delete_obj`.

Thus a successful session represents more than reachability or byte transmission: the receiver-specific requested work has completed successfully for the offered local set.

### P4 — current SSYNC receiver

The receiver executes object-server subrequests and reports update failures as protocol failures rather than silently treating them as successful synchronization.

### P5 — reconstructor tests

<https://github.com/openstack/swift/blob/6b83d7f3fcf95539b17dc1e3f5f1074c29afc487/test/unit/obj/test_reconstructor.py>

The tests corroborate that:

- successful REVERT work can remove the local hashpath;
- failed work withholds normal local cleanup;
- `max_objects_per_revert` can leave residual handoff state for a later reconstructor run;
- a later run can synchronize and purge that residual state.

---

## Historical / implementation record (`H/P`)

### H/P1 — a handoff is a temporary placement of the same logical coded state

The retention question is not whether a new logical object has been created. It is whether a temporary local embodiment can be retired after the proper placement has been sufficiently re-established.

### H/P2 — the original EC reconstructor already ordered reversion before cleanup

The historical implementation supports the bounded ordering:

```text
replacement-placement / synchronization work
    -> successful reversion evidence
    -> local handoff cleanup
```

No stronger claim about current candidate-map semantics is projected backward.

### H/P3 — current `_revert()` gates cleanup on successful required sessions

For every current configured `sync_to` destination, the reconstructor invokes SSYNC. Local cleanup is called only if the count of successful sessions reaches the number of required destinations.

Therefore:

```text
required destination session fails
    -> this pass does not call local handoff purge
```

### H/P4 — candidate maps are merged, not intersected

Current source performs:

```text
reverted_objs.update(in_sync_objs)
```

not:

```text
reverted_objs = reverted_objs ∩ in_sync_objs
```

This distinction is now explicit repository policy: do not describe the current implementation as an all-destination per-object intersection.

### H/P5 — normal sender success qualifies the local offered set after receiver-specific updates

The normal sender first asks the receiver what it wants. Only after requested updates complete does it return the local `available_map` as deletion-eligible state.

Thus:

```text
object offered locally
    + receiver requests nothing
```

can still count as synchronized: the receiver may already have suitable state.

Likewise:

```text
object offered locally
    + receiver requests update
    + update succeeds
```

can become synchronized without any separate candidate-intersection stage.

### H/P6 — protocol attempt is weaker than successful synchronization

A connection or SSYNC attempt by itself does not authorize cleanup. Receiver update failures can fail the session, which withholds the all-session cleanup gate.

### H/P7 — local purge is placement cleanup, not logical DELETE

`delete_reverted_objs()` removes the matching local handoff fragment/timestamp state. It is not a client object deletion and is not itself a theorem about cluster-wide EC reconstructability.

---

## Engineering reconstruction (`E`)

### E1 — the handoff copy carries a conditional retention obligation

```text
handoff embodiment exists
    + reversion not sufficiently qualified
    -> retain handoff embodiment
```

After required destination sessions succeed and the object is present in the merged cleanup candidate map:

```text
candidate may enter local cleanup
```

“May enter local cleanup” is deliberately narrower than “globally unnecessary.”

### E2 — payload state and disposal authority are different things

The handoff payload can remain byte-for-byte unchanged while the system lacks sufficient evidence to retire it.

Conversely, remote synchronization can become strong enough to authorize local disposal while the old handoff bytes still remain until cleanup runs.

```text
payload existence
    != source-retirement authority
```

### E3 — all-session gating and candidate aggregation must be kept separate

Current source has two dimensions:

```text
candidate aggregation:
    merge successful sender candidate maps

session gate:
    every required sync_to session succeeded
```

This is more precise than the superseded intersection model.

### E4 — failed destination work preserves the old embodiment by withholding cleanup

Preservation does not require copying the handoff fragment again. It can occur simply because the cleanup condition was not reached.

```text
preservation
    != explicit duplicate-write operation
```

### E5 — receiver “in sync” evidence is stronger than reachability but weaker than universal media durability

A successful current SSYNC exchange means the protocol's required receiver update work completed successfully enough for the sender to return success.

It does not prove survival under every filesystem, HBA, controller-cache, firmware, device-cache, media, or sudden-power-loss model.

### E6 — local retirement is not whole-object EC reconstructability

The local cleanup rule does not by itself prove that every possible correlated-failure scenario retains `ec_ndata` usable same-version fragments.

### E7 — temporary redundant embodiment may outlive the outage that created it

The handoff can persist after the original primary outage has ended. Availability of a primary again does not itself delete the handoff; successful reversion and later cleanup are separate events.

### E8 — remote publication and local retirement are separate transitions

A meaningful intermediate state exists:

```text
remote placement synchronized
    + old local handoff still exists
```

That state becomes central in the companion retry/crash-window deepening.

---

## Corrected bounded state machine

```text
[local handoff fragment exists]
        |
        v
[SSYNC required destination(s)]
        |
        +-- any required session fails --> [no local purge this pass]
        |
        v
[all required sessions succeeded]
        |
        v
[merge successful-session candidate maps]
        |
        v
[delete_reverted_objs(candidate map)]
        |
        v
[matching local handoff embodiments purged]
```

No per-destination object-set intersection is asserted.

---

## Functional analogy (`F`)

### F1 — bounded analogy to Case 04 mapped Flash

Both cases support the narrow shape:

```text
old / temporary embodiment remains
    -> replacement/current embodiment established
    -> sufficient currentness/publication evidence
    -> old embodiment may later be retired
```

This is functional only. No historical or implementation genealogy is claimed.

---

## Philosophical interpretation (`I`)

A minimal interpretation remains:

> Retention can include an obligation to keep a redundant embodiment until the system has enough evidence to authorize disposal.

The source correction sharpens this further: the conceptual language must follow the actual control mechanism. A clean set-theoretic description is not preferable to an uglier but accurate program path.

---

## Explicit non-claims

This deepening does **not** claim:

1. that one destination acknowledgement proves the whole EC object durable;
2. that SSYNC success proves stable-media survival under every lower-stack failure model;
3. that the purged handoff was the last usable fragment;
4. that local handoff purge is logical object deletion;
5. that remote synchronization and local purge form one atomic transaction;
6. that every historical Swift release uses the current merge/update + all-session gate;
7. that `reverted_objs.update(...)` should be re-described as an intersection;
8. that ordinary REVERT always has multiple destinations;
9. that a successful protocol exchange freezes the ring;
10. that all destination nodes are failure-independent;
11. that the local cleanup decision proves whole-object reconstructability;
12. that sender process memory is a durable repair journal;
13. that Swift derives the pattern from Flash, RAID, databases, or another lineage.

---

## What this closes

This slice closes the narrow question:

> **Does current Swift EC discard a handoff fragment merely after attempting to send it?**

No. Current local purge is downstream of successful required destination SSYNC sessions and merged sender-provided cleanup candidates.

It also repairs the repository's earlier technical misstatement:

```text
current implementation
    != per-destination in-sync intersection
```

The current source is:

```text
candidate-map update/merge
    + all-required-session success gate
```

---

## Remaining bounded debt

The former process-crash / later-pass debt is now handled by:

[`25-swift-ec-revert-retry-crash-window-correction-deepening.md`](25-swift-ec-revert-retry-crash-window-correction-deepening.md).

Remaining high-value work is narrower:

1. explicit process-kill fault injection at the final SSYNC-return / cleanup boundary;
2. lower-stack power-cut validation of receiver persistence;
3. ring/rebalance movement between reversion attempts;
4. historical evolution of the current candidate merge and session gate;
5. whole-object reconstructability under correlated placement failures.

---

## Project-level retention summary

```text
handoff payload retained
    until
required reversion work succeeds

successful remote synchronization
    != local embodiment already gone

candidate-map merge
    + all-required-session success
    -> local cleanup may run

local handoff retirement
    != logical deletion
    != universal durability proof
```

The retention object here is therefore both the temporary fragment embodiment and the **authority to stop retaining it**.
