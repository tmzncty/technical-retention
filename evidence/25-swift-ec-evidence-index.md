# Case 25 evidence index — OpenStack Swift EC retention/currentness

**Case:** [`25 — OpenStack Swift EC overwrite/durable currentness`](../cases/25-openstack-swift-ec-overwrite-durable-currentness.md)  
**Current maturity:** `grounded`  
**Purpose:** evidence navigation, scope control, and bounded-debt tracking

## Why this index exists

Case 25 now has several distinct evidence layers. They all concern retained state in Swift's erasure-coded object path, but they answer different questions and should not be collapsed into a generic statement that “Swift keeps enough copies.”

The current evidence chain separates at least:

```text
fragment payload identity
    != timestamp-cohort identity
    != durable/current cohort evidence
    != durability-witness representation
    != placement/currentness evidence
    != authority to retire a handoff embodiment
```

This index keeps those layers navigable and records what remains open.

---

## Canonical case

### C25 — overwrite, durable currentness, and EC reconstruction

[`../cases/25-openstack-swift-ec-overwrite-durable-currentness.md`](../cases/25-openstack-swift-ec-overwrite-durable-currentness.md)

The canonical case establishes the broad technical structure, including:

- EC fragment archives keyed by timestamp and fragment index;
- first-phase fragment writes versus durable/committed state;
- cleanup gating and non-durable fragment handling;
- the distinction between fragment existence and a usable same-timestamp coded cohort;
- GET reconstruction constraints;
- reconstructor repair and durability/currentness propagation;
- the evolution from separate `.durable` witnesses to durable state encoded in fragment filenames;
- the later `commit_window` boundary.

Use the canonical case for the overall architecture and maturity claim. Use the evidence deepenings below for narrow revision or disposal boundaries.

---

## Evidence chain 1 — durability witness changes representation

### E25-1 — Swift 2.11.0 durability-witness representation migration

[`25-swift-2016-durable-marker-representation-migration-deepening.md`](25-swift-2016-durable-marker-representation-migration-deepening.md)

**Question:** can the retained fact that an EC timestamp cohort is durable survive a change in the filesystem representation used to encode that fact?

**Bounded result:** yes, within the documented 2.10/2.11 boundary. Swift moved new durability witnesses from a separate:

```text
<timestamp>.durable
```

file into:

```text
<timestamp>#<frag_index>#d.data
```

while retaining recognition of legacy `.durable` files and normalizing the two representations into the same abstract consistency state for relevant hashing logic.

**Important distinction:**

```text
durability relation
    != durability-witness inode/name representation
```

**Do not infer:** symmetric downgrade compatibility, universal rename crash-atomicity, or a change to erasure-code mathematics.

---

## Evidence chain 2 — handoff reversion and source retirement

### E25-2 — EC handoff reversion / local source-retirement boundary

[`25-swift-ec-handoff-revert-retirement-boundary-deepening.md`](25-swift-ec-handoff-revert-retirement-boundary-deepening.md)

**Question:** what evidence is required before a temporary local EC handoff embodiment may be purged after reversion toward primary placements?

**Historical lower bound:** the original EC reconstructor already ordered cleanup after successful reversion/synchronization work rather than deleting the handoff first.

**Pinned current implementation (`openstack/swift` master `6b83d7f3fcf95539b17dc1e3f5f1074c29afc487`):**

```text
for each destination in job['sync_to']:
    run SSYNC
    if destination session fails:
        no local purge in this pass

    retain destination-specific in-sync object set

intersect the in-sync sets across destinations
    -> only objects surviving the intersection
       become eligible for local handoff purge
```

This closes several previously implicit boundaries:

```text
handoff fragment exists
    != primary placement restored

SSYNC attempt
    != successful receiver synchronization

one destination succeeds
    != local source is disposable

local handoff fragment purged
    != logical object/version deleted
```

It also introduces a useful retention category:

```text
payload-bearing handoff state
    != placement/currentness evidence
    != authority to stop retaining the handoff copy
```

**Do not infer:** that SSYNC success proves stable-on-media persistence under every storage stack, that the local handoff was the last usable fragment, or that the cleanup decision by itself proves whole-object EC reconstructability.

---

## Combined technical picture

The evidence chain now supports a layered model:

```text
logical object/version
    |
    v
same-timestamp EC fragment cohort
    |
    +--> fragment-index identity / coded payload
    |
    +--> durable/current cohort evidence
             |
             +--> old representation: separate .durable inode
             |
             +--> newer representation: #d in data filename
    |
    +--> placement state
             |
             +--> primary fragment placement
             |
             +--> temporary handoff embodiment
                        |
                        v
                  SSYNC reversion evidence
                        |
                        v
                  source-retirement authority
```

Three kinds of continuity therefore need separate language:

1. **payload continuity** — usable coded fragment state remains available;
2. **currentness/durability continuity** — the implementation retains enough evidence to identify the relevant committed timestamped state;
3. **placement continuity** — temporary and primary embodiments change without prematurely discarding the only state that a repair/reversion path is still obliged to retain.

---

## Cross-case comparison

### Case 04 — flash virtual mapping

[`../cases/04-flash-virtual-mapping.md`](../cases/04-flash-virtual-mapping.md)

Functional analogy only:

```text
replacement embodiment established
    + publication/currentness evidence
    -> old embodiment may later be retired
```

Both Case 04 and Case 25 warn against treating “new location has been attempted” as equivalent to “old location is already disposable.”

There is **no genealogy claim** that Swift derived this pattern from flash translation layers.

### Case 88 — RAID5 PPL

[`../cases/88-linux-md-raid5-partial-parity-log.md`](../cases/88-linux-md-raid5-partial-parity-log.md)

A weaker functional comparison is possible: both distinguish payload/home state from separate evidence or obligations that govern when an earlier protection mechanism may retire. The mechanisms are otherwise very different; PPL crash-recovery evidence should not be equated with Swift placement synchronization evidence.

---

## What is closed

The current Case 25 package now has direct or implementation-level support for:

- EC fragment archives as versioned/timestamped coded embodiments;
- durable/current timestamp-cohort evidence distinct from mere fragment-file existence;
- migration of durability witness representation across Swift 2.11.0 while retaining legacy readability in newer software;
- temporary handoff embodiments as a distinct placement state;
- current EC reconstructor cleanup being gated by successful destination SSYNC outcomes;
- per-object cleanup eligibility being an intersection of destination-specific in-sync results in the pinned current implementation;
- local handoff purge being placement cleanup rather than logical object deletion.

Case 25 remains `grounded`. None of these narrow deepenings alone justify a maturity promotion.

---

## Remaining bounded debt

Priority order for future one-round slices:

### 1. Receiver persistence boundary

Trace a successful SSYNC update through the object server and diskfile implementation far enough to state exactly what filesystem persistence actions occur before the receiver reports success.

Target distinction:

```text
object-server subrequest succeeded
    != automatically proven stable-on-media under arbitrary power loss
```

### 2. Crash after remote success but before local purge

Use tests, implementation paths, or fault injection to show what happens if the reconstructor dies after destinations are synchronized but before `_delete_reverted_objs()` completes.

Likely retention question:

```text
extra old embodiment survives
    vs
replacement-placement evidence must be rediscovered
```

Do not infer this from current code silence alone.

### 3. Partial success across reconstructor passes

Determine how a later pass recognizes receiver state created during an earlier partially successful pass and whether that history is represented only by receiver disk state rather than durable sender-side session metadata.

### 4. Ring/rebalance movement during a reversion job

Bound destination identity/currentness when placement changes while reversion is in progress.

### 5. Historical evolution of modern intersection semantics

Find the exact commit(s) that introduced or materially changed the current per-object/all-destination intersection rule. The original EC reconstructor proves only the weaker historical fact that cleanup followed successful reversion work.

### 6. Whole-object reconstructability under correlated placement failures

Keep this separate from local source-retirement logic. A local purge gate is not by itself a theorem about all cluster-wide failure combinations.

---

## Source-custody note

For the handoff-retirement deepening, current implementation claims are pinned to OpenStack Swift commit:

`6b83d7f3fcf95539b17dc1e3f5f1074c29afc487` — **2026-09-20**.

Historical introduction is anchored at:

`647b66a2ce4c85c43dcca49776d35c5ebb9cf15e`.

The evidence files preserve the distinction between what the historical change proves and what only the modern implementation proves. This avoids silently projecting present-day cleanup semantics backward across the entire Swift EC history.
