# Case 25 evidence index — OpenStack Swift EC retention/currentness

**Case:** [`25 — OpenStack Swift EC overwrite/durable currentness`](../cases/25-openstack-swift-ec-overwrite-durable-currentness.md)  
**Current maturity:** `grounded`  
**Purpose:** evidence navigation, scope control, and bounded-debt tracking

## Why this index exists

Case 25 now has several distinct evidence layers. They all concern retained state in Swift's erasure-coded object path, but they answer different questions and should not be collapsed into a generic statement that “Swift keeps enough copies.”

The current evidence chain separates at least:

```text
fragment payload identity
    != filesystem persistence completion
    != Swift durable/current cohort evidence
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

Use the canonical case for the overall architecture and maturity claim. Use the evidence deepenings below for narrow revision, persistence, or disposal boundaries.

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

**Do not infer:** that local handoff state was the last usable fragment, that the cleanup decision by itself proves whole-object EC reconstructability, or that current all-destination intersection semantics existed unchanged in the earliest EC reconstructor.

---

## Evidence chain 3 — SSYNC receiver filesystem persistence and EC durability qualification

### E25-3 — receiver persistence boundary before SSYNC success

[`25-swift-ec-ssync-receiver-persistence-boundary-deepening.md`](25-swift-ec-ssync-receiver-persistence-boundary-deepening.md)

**Question:** what filesystem persistence actions occur on the receiving object server before a normal durable-fragment SSYNC update can be reported as successful?

**Pinned current implementation (`openstack/swift` `6b83d7f3fcf95539b17dc1e3f5f1074c29afc487`, 2026-09-20):**

```text
source durable fragment
    -> SSYNC PUT without X-Backend-No-Commit
    -> receiver routes PUT to object server
    -> payload written to temp file
    -> object metadata written
    -> fsync(fragment file)
    -> non-durable EC pathname published
    -> destination directory path(s) fsynced
    -> EC commit renames to durable-name form
    -> object data directory fsynced
    -> object server returns HTTP success
    -> receiver reports clean UPDATES completion
    -> sender accepts session success
```

The current POSIX diskfile implementation therefore gives direct source-level support for a lower-layer persistence chain beneath SSYNC's protocol acknowledgement.

But the same code also makes two boundaries explicit.

First, a non-durable source fragment is transferred with:

```text
X-Backend-No-Commit: True
```

so the receiver may complete ordinary file finalization and filesystem sync work while deliberately skipping the EC durable-name transition:

```text
filesystem-persisted fragment
    != Swift-qualified durable EC fragment
```

Second, if the receiver already has the exact offered fragment but lacks durable state, `_check_local()` can call `writer.commit()` locally and become durably in-sync without retransmitting the payload:

```text
receiver becomes durably in-sync
    != payload bytes necessarily moved in this SSYNC exchange
```

**Important limit:** the implementation proves that Swift requests and waits for file/directory synchronization at these boundaries. It does **not** by itself prove survival under every kernel/filesystem/HBA/controller/device-cache/firmware or arbitrary power-loss failure model. Physical power-cut validation remains separate work.

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
    |        |
    |        +--> receiver-side file persistence work
    |                 |
    |                 +--> payload + metadata fsync
    |                 +--> pathname publication + directory sync
    |
    +--> durable/current cohort evidence
             |
             +--> old representation: separate .durable inode
             |
             +--> newer representation: #d in data filename
                          |
                          +--> current commit rename + directory fsync
    |
    +--> placement state
             |
             +--> primary fragment placement
             |
             +--> temporary handoff embodiment
                        |
                        v
                  SSYNC synchronization evidence
                        |
                        v
              all-required-destination intersection
                        |
                        v
                  source-retirement authority
```

Four kinds of continuity therefore need separate language:

1. **payload continuity** — usable coded fragment state remains available;
2. **filesystem persistence continuity** — the current implementation has completed the file/directory sync operations associated with publishing receiver-side state;
3. **currentness/durability continuity** — Swift retains enough evidence to identify the relevant committed timestamped state;
4. **placement continuity** — temporary and primary embodiments change without prematurely discarding a copy that a repair/reversion path is still obliged to retain.

These layers compose, but they are not synonyms.

---

## Cross-case comparison

### Case 04 — flash virtual mapping

[`../cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md)

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

A bounded functional comparison is now stronger than before: both cases separate an upper-layer completion decision from lower persistence work and from later authority/retirement state.

For Case 25:

```text
receiver update success
    != mere byte receipt
    != universal stable-media theorem
    != whole-object reconstructability
```

For Case 88, asynchronous completion, cache-flush success, member authority, and recovery obligation likewise remain distinct. The mechanisms and histories are otherwise different.

---

## What is closed

The current Case 25 package now has direct or implementation-level support for:

- EC fragment archives as versioned/timestamped coded embodiments;
- durable/current timestamp-cohort evidence distinct from mere fragment-file existence;
- migration of durability witness representation across Swift 2.11.0 while retaining legacy readability in newer software;
- temporary handoff embodiments as a distinct placement state;
- current EC reconstructor cleanup being gated by successful destination SSYNC outcomes;
- per-object cleanup eligibility being an intersection of destination-specific in-sync results in the pinned current implementation;
- local handoff purge being placement cleanup rather than logical object deletion;
- current SSYNC receiver success being downstream of actual object-server subrequest success rather than mere network receipt;
- current POSIX diskfile finalization writing metadata then fsyncing the fragment file before publishing its pathname;
- rename/link publication using directory synchronization in the current helpers;
- EC durable-state publication performing an additional durable-name rename plus object-directory fsync before the normal durable PUT can return success;
- non-durable SSYNC transfer deliberately preserving the distinction between filesystem-persisted fragment state and Swift durable qualification;
- commit-only promotion allowing already-present payload to acquire durable state without retransmitting payload bytes.

The former top-priority debt — tracing receiver persistence work far enough to state what precedes SSYNC success — is therefore closed for the pinned current implementation.

Case 25 remains `grounded`. None of these narrow deepenings alone justify a maturity promotion.

---

## Remaining bounded debt

Priority order for future one-round slices:

### 1. Physical power-cut validation of the receiver persistence path

Find or build named-stack fault-injection evidence at exact cut points around file fsync, pathname publication, EC durable-name rename, directory fsync, and SSYNC response.

Target distinction:

```text
Swift requested/completed filesystem sync calls
    != empirically validated survival under every lower-stack failure model
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

### 4. Historical evolution of receiver persistence semantics

Find the exact historical commits that introduced or materially changed:

- file fsync-before-publish behavior;
- directory syncing in rename/link helpers;
- EC durable filename publication;
- `X-Backend-No-Commit` handling;
- commit-only durable promotion during missing-check.

The pinned current implementation is not evidence that all of these were present unchanged in the first EC release.

### 5. Ring/rebalance movement during a reversion job

Bound destination identity/currentness when placement changes while reversion is in progress.

### 6. Historical evolution of modern all-destination intersection semantics

Find the exact commit(s) that introduced or materially changed the current per-object/all-destination intersection rule. The original EC reconstructor proves only the weaker historical fact that cleanup followed successful reversion work.

### 7. Whole-object reconstructability under correlated placement failures

Keep this separate from local source-retirement logic. A local purge gate and one receiver's durable-state publication are not by themselves a theorem about all cluster-wide failure combinations.

---

## Source-custody note

For the handoff-retirement and receiver-persistence deepenings, current implementation claims are pinned to OpenStack Swift commit:

`6b83d7f3fcf95539b17dc1e3f5f1074c29afc487` — **2026-09-20**.

Historical reconstructor introduction remains anchored at:

`647b66a2ce4c85c43dcca49776d35c5ebb9cf15e`.

The receiver-persistence deepening deliberately treats the current sender, receiver, object-server, diskfile, and filesystem-helper paths as a **current implementation witness** rather than silently projecting their exact ordering backward across Swift's history.

A fresh companion search found no dedicated Swift EC / SSYNC packet in `tmzncty/computing-archaeology`; broader Swift, filesystem, XFS, block-flush, controller, and storage-hardware history therefore remains outside this evidence index unless a retention-specific boundary requires it.
