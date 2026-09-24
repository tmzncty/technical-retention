# Case 25 evidence index — OpenStack Swift EC retention/currentness

**Case:** [`25 — OpenStack Swift EC overwrite/durable currentness`](../cases/25-openstack-swift-ec-overwrite-durable-currentness.md)  
**Current maturity:** `grounded`  
**Purpose:** evidence navigation, correction control, and bounded-debt tracking

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
    != completion of local cleanup
```

A 2026-09-24 source reinspection also corrected one earlier repository mistake: current handoff reversion does **not** intersect per-destination `in_sync_objs` maps. The implementation merges successful-session candidate maps with `dict.update()` and separately requires all configured destination sessions to succeed before cleanup.

---

## Canonical case

### C25 — overwrite, durable currentness, and EC reconstruction

[`../cases/25-openstack-swift-ec-overwrite-durable-currentness.md`](../cases/25-openstack-swift-ec-overwrite-durable-currentness.md)

The canonical case establishes the broad technical structure:

- EC fragment archives keyed by timestamp and fragment index;
- first-phase fragment writes versus durable/committed state;
- cleanup gating and non-durable fragment handling;
- same-timestamp coded-cohort requirements;
- GET reconstruction constraints;
- reconstructor repair and durability/currentness propagation;
- migration from separate `.durable` witnesses to durable state encoded in fragment filenames;
- later `commit_window` behavior.

Use the evidence deepenings below for narrow representation, persistence, reversion, retry, and cleanup boundaries.

---

## Evidence chain 1 — durability witness changes representation

### E25-1 — Swift 2.11.0 durability-witness representation migration

[`25-swift-2016-durable-marker-representation-migration-deepening.md`](25-swift-2016-durable-marker-representation-migration-deepening.md)

**Question:** can the retained fact that an EC timestamp cohort is durable survive a change in filesystem representation?

**Bounded result:** yes, within the documented 2.10/2.11 boundary. Swift moved new durability witnesses from:

```text
<timestamp>.durable
```

to:

```text
<timestamp>#<frag_index>#d.data
```

while newer software retained recognition of the legacy representation.

**Important distinction:**

```text
durability relation
    != durability-witness inode/name representation
```

**Do not infer:** symmetric downgrade compatibility, universal rename crash-atomicity, or a change to erasure-code mathematics.

---

## Evidence chain 2 — handoff reversion and source-retirement gate

### E25-2 — EC handoff reversion / local source-retirement boundary

[`25-swift-ec-handoff-revert-retirement-boundary-deepening.md`](25-swift-ec-handoff-revert-retirement-boundary-deepening.md)

**Question:** what current implementation evidence stands between a temporary local EC handoff embodiment and its local purge?

**Historical lower bound:** the original EC reconstructor already ordered cleanup after successful reversion/synchronization work rather than deleting the handoff first.

**Corrected current implementation:**

```text
for each required destination in job['sync_to']:
    run SSYNC
    if success:
        syncd_with += 1
        reverted_objs.update(in_sync_objs)

if syncd_with >= len(job['sync_to']):
    delete_reverted_objs(job, reverted_objs)
```

This is a **candidate-map merge/update plus all-required-session-success gate**.

It is **not**:

```text
I1 ∩ I2 ∩ ... ∩ In
```

The previous intersection wording has been removed from the source-retirement note and superseded by direct source inspection.

Current `process_job()` documentation also matters: ordinary non-primary REVERT work normally targets the proper/new home for the fragment index; multiple destinations can arise when the EC duplication factor requires them. A generic multi-replica quorum model should not be projected onto every REVERT job.

**Important distinctions:**

```text
handoff fragment exists
    != proper placement restored

SSYNC attempted
    != required destination session succeeded

remote synchronization succeeded
    != local handoff already purged

local handoff purge
    != logical object/version deletion
```

---

## Evidence chain 3 — SSYNC receiver filesystem persistence and EC durability qualification

### E25-3 — receiver persistence boundary before SSYNC success

[`25-swift-ec-ssync-receiver-persistence-boundary-deepening.md`](25-swift-ec-ssync-receiver-persistence-boundary-deepening.md)

**Question:** what filesystem persistence work precedes a normal durable-fragment SSYNC update being reported as successful?

**Pinned implementation witness (`6b83d7f3fcf95539b17dc1e3f5f1074c29afc487`, 2026-09-20):**

```text
source durable fragment
    -> SSYNC PUT without X-Backend-No-Commit
    -> receiver routes PUT to object server
    -> payload written to temp file
    -> object metadata written
    -> fsync(fragment file)
    -> non-durable EC pathname published
    -> destination directory path(s) synced
    -> EC commit renames to durable-name form
    -> object data directory synced
    -> object-server success
    -> receiver clean UPDATES completion
    -> sender session success
```

Two boundaries remain essential.

First:

```text
filesystem-persisted fragment
    != Swift-qualified durable EC fragment
```

because a non-durable source fragment can be transferred with `X-Backend-No-Commit: True`, deliberately skipping EC durable qualification.

Second:

```text
receiver becomes durably in-sync
    != payload bytes necessarily moved in that exchange
```

because commit-only promotion can upgrade already-present receiver state.

**Important limit:** source-level `fsync`/directory-sync ordering is not universal empirical proof of survival under every kernel/filesystem/HBA/controller/device-cache/firmware or sudden-power-loss model.

---

## Evidence chain 4 — process restart, re-observation, and interrupted local cleanup

### E25-4 — reversion retry/crash-window correction deepening

[`25-swift-ec-revert-retry-crash-window-correction-deepening.md`](25-swift-ec-revert-retry-crash-window-correction-deepening.md)

**Question:** what happens at source/test level if remote synchronization succeeds but the reconstructor process stops before local handoff cleanup completes?

**Current implementation result:** the cleanup path is reconstructible from surviving state rather than requiring the volatile `reverted_objs` dictionary to survive process death.

The current sender rebuilds `available_map` from local disk state on each `MISSING_CHECK`, asks the receiver what it still wants, performs only requested updates, and on success returns the offered local map as cleanup candidates.

The current local cleanup helper iterates candidates object-by-object with `df.purge(...)`; it is not one batch transaction.

Therefore the source-level crash windows can be bounded as:

```text
A. process stops before all required destination sessions succeed
   -> local purge is not called
   -> handoff state remains for a later pass

B. all required sessions succeed, process stops before cleanup starts
   -> remote replacement may already exist
   -> all local candidates still remain
   -> later pass re-observes receiver current state

C. process stops during object-by-object cleanup
   -> already-purged objects are absent
   -> unpurged local objects remain discoverable
   -> later pass processes the residue
```

`test_delete_reverted_max_objects_per_revert` provides direct multi-pass corroboration: one run can leave residual handoff data and report handoffs remaining; a later run then synchronizes and purges the remaining object.

**Important distinction:**

```text
remote success from an earlier process lifetime
    != durable sender-side cleanup authority

receiver/local state re-observed on later pass
    -> cleanup authority reconstructed
```

This closes the former process-retry debt at source/test level, while leaving explicit kill/fault-injection and physical power-loss validation open.

---

## Combined technical picture

The evidence chain now supports this layered model:

```text
logical object/version
    |
    v
same-timestamp EC fragment cohort
    |
    +--> fragment-index identity / coded payload
    |
    +--> receiver-side persistence work
    |        |
    |        +--> payload/metadata file sync
    |        +--> pathname/directory publication sync
    |
    +--> durable/current cohort evidence
    |        |
    |        +--> legacy .durable representation
    |        +--> newer #d filename representation
    |
    +--> placement state
             |
             +--> primary/proper fragment placement
             +--> temporary handoff embodiment
                        |
                        v
                 SSYNC current-state exchange
                        |
                        v
              required session success gate
                        |
                        v
            merged local cleanup candidates
                        |
                        v
               object-by-object local purge
```

Five kinds of continuity therefore need separate language:

1. **payload continuity** — usable coded fragment state remains available;
2. **filesystem persistence continuity** — the implementation completed its file/directory synchronization requests;
3. **currentness/durability continuity** — Swift retains enough evidence to qualify the relevant committed timestamp state;
4. **placement continuity** — temporary and proper embodiments change without premature local disposal;
5. **maintenance-obligation continuity** — after process loss, remaining reversion/cleanup work can be regenerated from surviving local/remote/ring state.

These compose, but they are not synonyms.

---

## Cross-case comparison

### Case 04 — mapped Flash

[`../cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md)

Functional analogy only:

```text
replacement embodiment established
    + currentness/publication evidence
    -> old embodiment may later be retired
```

Both cases reject:

```text
new location attempted
    == old location already disposable
```

Swift additionally shows that after a process restart, replacement state can be **re-observed** and cleanup authority reconstructed.

No genealogy is claimed.

### Case 88 — RAID5 PPL

[`../cases/88-linux-md-raid5-partial-parity-log.md`](../cases/88-linux-md-raid5-partial-parity-log.md)

Bounded functional comparison only: both cases separate upper-layer completion/authority decisions from lower persistence work and from later cleanup/recovery obligations.

For Swift:

```text
receiver update success
    != mere byte receipt
    != universal stable-media theorem
    != whole-object reconstructability
```

The mechanisms and histories are otherwise different.

---

## What is closed

The current Case 25 package now has direct or implementation-level support for:

- EC fragment archives as versioned/timestamped coded embodiments;
- durable/current timestamp-cohort evidence distinct from mere fragment-file existence;
- migration of the durability witness representation across Swift 2.11.0;
- temporary handoff embodiments as a distinct placement state;
- current handoff cleanup being gated by successful required SSYNC sessions;
- **correction:** current cleanup candidates are merged with `reverted_objs.update(in_sync_objs)`, not intersected across destination maps;
- normal sender success returning the local offered set after receiver-specific requested updates complete;
- local handoff purge being placement cleanup rather than logical object deletion;
- current receiver success being downstream of actual object-server update success;
- current POSIX diskfile finalization performing file/directory synchronization before normal durable PUT success;
- non-durable transfer preserving the distinction between filesystem persistence and Swift durable qualification;
- commit-only durable promotion without retransmitting already-present payload;
- process-level retry after remote success being reconstructible from surviving state;
- object-by-object local cleanup allowing a later pass to process residual handoff state;
- multi-pass unit-test corroboration that residual handoff work can be completed on a later reconstructor run.

Case 25 remains `grounded`. These bounded deepenings do not by themselves justify a maturity promotion.

---

## Remaining bounded debt

Priority order for future one-round slices:

### 1. Physical power-cut validation of the receiver persistence path

Find or build named-stack fault-injection evidence around:

- file fsync;
- pathname publication;
- EC durable-name rename;
- directory fsync;
- SSYNC response.

Target distinction:

```text
Swift completed filesystem sync calls
    != empirically validated survival under every lower-stack failure model
```

### 2. Explicit process-kill fault injection at the reversion cleanup seam

The source/test-level retry model is now bounded, but a direct test should kill the reconstructor:

- after the final successful SSYNC return but before `delete_reverted_objs()`;
- during the per-object purge loop.

Then verify the exact next-pass behavior.

### 3. Ring/rebalance movement between passes

Bound destination identity/currentness when placement changes between the successful remote transfer and the later cleanup/retry pass.

### 4. Historical evolution of current reversion semantics

Find the commits that introduced or materially changed:

- the current `reverted_objs.update(in_sync_objs)` merge;
- the all-required-session cleanup gate;
- `max_objects_per_revert` retry behavior;
- current non-durable/include-non-durable reversion behavior.

Do not project today's source structure backward to the first EC reconstructor.

### 5. Historical evolution of receiver persistence semantics

Find exact commits for:

- file sync-before-publish behavior;
- directory syncing in rename/link helpers;
- EC durable filename publication;
- `X-Backend-No-Commit` handling;
- commit-only durable promotion.

### 6. Whole-object reconstructability under correlated placement failures

Keep this separate from local source-retirement logic. A local purge gate and receiver-side durable-state publication are not by themselves a theorem about all cluster-wide failure combinations.

---

## Source-custody note

The 2026-09-24 correction/retry slice inspected OpenStack Swift master at:

`e60791398bfefc0f2b3c4b0012c292d983248765`.

The earlier receiver-persistence work remains pinned to:

`6b83d7f3fcf95539b17dc1e3f5f1074c29afc487` — 2026-09-20.

Historical reconstructor introduction remains anchored at:

`647b66a2ce4c85c43dcca49776d35c5ebb9cf15e`.

Fresh companion searches for `Swift SSYNC` and `OpenStack Swift` found no dedicated reusable packet in `tmzncty/computing-archaeology`. Broad Swift replication history, SSYNC genealogy, filesystem durability history, and rebalance archaeology therefore remain outside this evidence index unless another retention-specific boundary requires them.
