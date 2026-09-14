# Evidence 18 — OpenZFS Scrub Progress and Completion Durability, 2017–2026

## Status

**`bounded deepening complete`**

This evidence note deepens Case 18 without changing its `grounded` maturity. The original case remains bounded historically to 2004–2010 ZFS scrub semantics. This note adds a later OpenZFS implementation slice because it exposes a retention question that the older administration documentation cannot answer:

> **What scan-control state must survive interruption, and when is a scrub/resilver actually complete for a caller that waits for the operation?**

The answer is not simply `scan state = finished`.

The bounded implementation chain examined here is:

```text
2017 OpenZFS pause/resume
    -> persistent on-disk scrub state
    -> paused state can survive interruption

OpenZFS 2.1-era implementation/documentation
    -> scrub progress periodically checkpointed
    -> resume after restart/export starts from last on-disk checkpoint
    -> live traversal frontier may be ahead of durable checkpoint

2026 OpenZFS completion-wait fix
    -> dsl_scan_done() can set DSS_FINISHED in syncing context
    -> final txg still has config/label work to reach disk
    -> old zpool-wait predicate could return too early
    -> record finishing txg
    -> keep scan logically "in progress" to waiters until that txg syncs
```

This note does **not** retroactively assign these later implementation details to Solaris/OpenSolaris ZFS of the 2004–2010 Case 18 period.

---

## Research question

The original Case 18 distinguishes:

- payload survival;
- integrity verification;
- redundancy availability;
- repair opportunity;
- scrub versus resilver.

The later implementation adds another state class:

> **maintenance execution state itself can require retention.**

A scrub can have already verified a large fraction of the pool, yet after a reboot it should not necessarily restart from zero. Conversely, a runtime field can say `DSS_FINISHED` while the txg carrying the final scan/config/label updates is still being written.

The useful distinctions are therefore:

```text
scrub work already performed
    != durable scrub checkpoint

runtime scan state
    != on-disk scan state

DSS_FINISHED observed in memory
    != final scan transaction group durably synced

operation completion notification
    != merely changing an in-core enum
```

`durable maintenance frontier`, `completion-durability boundary`, and `maintenance-control retention` below are project engineering terms, not OpenZFS historical vocabulary.

---

## Historical / implementation record

### H/P — 2017 pause/resume explicitly introduces persistent on-disk scrub state

OpenZFS commit `0ea05c64f8d08c20439dd2a06e949a2aa4115101`, authored in July 2017, is titled **“Implemented zpool scrub pause/resume.”** Its commit message says the feature is achieved by maintaining a **persistent on-disk scrub state**. While that state is paused, no more blocks are scrubbed, although scan housekeeping continues.

This is strong project-primary evidence that pause/resume was not designed as a process-local convenience variable. Persistence of the maintenance state is part of the feature contract.

**Primary anchor:** OpenZFS commit `0ea05c64f8d08c20439dd2a06e949a2aa4115101`:
<https://github.com/openzfs/zfs/commit/0ea05c64f8d08c20439dd2a06e949a2aa4115101>

### H/P — the 2.1 manual documents checkpointed progress across restart/export

The OpenZFS 2.1 `zpool-scrub(8)` documentation states that scrub pause state and progress are periodically synced to disk. If the machine restarts or the pool is exported while a scrub is paused, the scrub remains paused after import and resumes from the place where it was **last checkpointed to disk**.

That wording supplies an important negative boundary:

```text
last work actually performed
    != necessarily last work durably checkpointed
```

The persistence guarantee is tied to an on-disk checkpoint, not to every individual read issued by the scan.

**Primary documentation:** OpenZFS 2.1 `zpool-scrub(8)`:
<https://openzfs.github.io/openzfs-docs/man/v2.1/8/zpool-scrub.8.html>

### H/P — OpenZFS 2.1.11 loads scan state from the pool directory

In OpenZFS 2.1.11, `dsl_scan_init()` looks up `DMU_POOL_SCAN` in the pool directory and loads it into `scn->scn_phys`. The code explicitly comments that it may be **restarting after a reboot**. It reconstructs an issued-work counter from the persisted examined/skipped values and reloads the scan queue object into in-core state when one exists.

The implementation therefore distinguishes:

```text
persistent scan record + queue object
    -> load/reconstruction
    -> in-core scan execution state
```

The in-core object is not itself the durable representation.

**Primary source:** OpenZFS 2.1.11 `module/zfs/dsl_scan.c`, `dsl_scan_init()`:
<https://github.com/openzfs/zfs/blob/zfs-2.1.11/module/zfs/dsl_scan.c>

### H/P — scan state is only checkpointed at a consistency-safe point

OpenZFS 2.1.11 `dsl_scan_sync_state()` says it writes a persistent `dsl_scan_phys_t` record to the pool directory. The source also explains why it cannot blindly persist the live structure at every instant: when the block-sorting queues are nonempty, the stored state would be inconsistent with the amount of actual scanning progress.

The normal persistent write is therefore gated on `scn_queues_pending == 0`. In that safe condition, the scan queue is synced if present and `DMU_POOL_SCAN` is updated through the pool-directory ZAP.

This is a stronger implementation-level statement than the manual's generic phrase `periodically synced to disk`:

```text
live scan frontier
    != always safe persistent frontier

safe checkpoint
    requires internal queue state to be reconcilable
```

**Primary source:** OpenZFS 2.1.11 `module/zfs/dsl_scan.c`, `dsl_scan_sync_state()`:
<https://github.com/openzfs/zfs/blob/zfs-2.1.11/module/zfs/dsl_scan.c>

### H/P — the 2026 bug exposed an early-completion window

OpenZFS PR #19066 and commit `92a3904afc93c3a70584f13db8f26816dc79328d`, merged **2026-09-09**, document a race in the completion contract used by `zpool wait -t scrub` and `zpool wait -t resilver`.

The commit explains the sequence:

1. `dsl_scan_done()` runs in syncing context;
2. it asks `vdev_dtl_reassess()` to update DTL state and dirties configuration state;
3. it marks the scan `DSS_FINISHED`;
4. the same txg still has configuration and label writes to complete later in `spa_sync()`;
5. the old wait predicate looked at the scan state and could therefore return after step 3 but before step 4 had reached disk.

The reported failure was not merely theoretical. The PR says `zdb -PC` run immediately after `zpool wait -t resilver` could observe labels in the middle of rewrite and fail to open the pool. A DTrace experiment in a FreeBSD VM with an injected 100 ms disk-write delay observed `zpool wait` returning about **10 ms after `dsl_scan_done()` while `spa_sync()` still took seconds to finish**.

**Primary anchors:**

- OpenZFS commit `92a3904afc93c3a70584f13db8f26816dc79328d`:
  <https://github.com/openzfs/zfs/commit/92a3904afc93c3a70584f13db8f26816dc79328d>
- OpenZFS PR #19066:
  <https://github.com/openzfs/zfs/pull/19066>

### H/P — the fix records a finishing txg rather than treating `DSS_FINISHED` as sufficient

The merged fix adds `scn_finished_txg` to the in-core `dsl_scan_t`. In `dsl_scan_done()`, after setting `DSS_FINISHED`/`DSS_CANCELED`, the code records `tx->tx_txg` with the explicit comment that the new state plus config/label updates reach disk **when this txg syncs**, and that `zpool wait` must not return before then.

**Primary source:** `dsl_scan.c` at commit `92a3904...`, `dsl_scan_done()`:
<https://github.com/openzfs/zfs/blob/92a3904afc93c3a70584f13db8f26816dc79328d/module/zfs/dsl_scan.c#L1290-L1345>

### H/P — the wait predicate now has a distinct `finishing` state

At the same commit, `spa_activity_in_progress()` computes:

```text
finishing =
    scn_finished_txg != 0
    && spa_last_synced_txg(spa) < scn_finished_txg
```

and reports scrub/resilver activity as in progress while either `scanning` **or** `finishing` is true, subject to the existing pause/function distinctions.

This is direct implementation evidence that the observable operation-completion predicate is now intentionally wider than the scan-state enum.

**Primary source:** `spa.c` at commit `92a3904...`, `spa_activity_in_progress()`:
<https://github.com/openzfs/zfs/blob/92a3904afc93c3a70584f13db8f26816dc79328d/module/zfs/spa.c#L11890-L11955>

### H/P — the fix waits for the already-running txg, not an extra synthetic durability round

The commit message is careful about the boundary: the fix waits for the txg that already contains the scan completion/config/label updates. It does **not** add a new independent transaction solely to certify completion.

This matters because the new relation is:

```text
scan completion work belongs to txg N
    -> wait until txg N is synced
```

not:

```text
scan completes
    -> create unrelated txg N+1 as an extra proof token
```

That distinction keeps the engineering reconstruction tied to the actual implementation.

---

## Retained-state decomposition

This slice requires at least seven state classes that should not be collapsed.

### 1. User payload / metadata being verified

The blocks whose continued readability/integrity is the purpose of the scrub.

### 2. Integrity evidence and redundant repair sources

Checksums and alternate copies used by the verification/self-healing path. These remain the core Case 18 retained state.

### 3. Scan policy / mode

Whether the maintenance operation is a scrub or resilver and whether a scrub is paused.

### 4. Live scan progress

The work the running implementation has actually traversed/issued so far.

### 5. Durable scan checkpoint

The persisted `dsl_scan_phys_t`/scan-queue state from which traversal can be reconstructed after restart/import.

### 6. Completion-related configuration state

The DTL/configuration/label updates associated with finishing a scan/resilver and represented in the final txg.

### 7. Wait/API completion predicate

The condition exposed to a caller waiting for the maintenance operation. After the 2026 fix this includes the `finishing` interval through final-txg sync, not just `DSS_SCANNING`.

These are related but not equivalent:

```text
payload state
    != verification evidence
    != live maintenance progress
    != durable maintenance checkpoint
    != final maintenance txg
    != API-visible completion predicate
```

---

## Engineering reconstruction

### E — retained payload ≠ retained maintenance progress

The pool may retain all payload needed for a scrub while losing some recent scan progress after interruption. Repeating already-completed verification work is not the same failure as losing user data.

### E — periodic checkpointing intentionally permits bounded rework

Because the manual promises restart from the **last on-disk checkpoint**, the implementation is allowed to redo work performed after that checkpoint but before interruption.

Therefore:

```text
repeated scrub work after restart
    != proof that the earlier verification never occurred
```

It may instead reflect a deliberately coarser durable progress frontier.

### E — progress durability ≠ per-block verification-history durability

Nothing in this slice proves that OpenZFS persists an exact timestamp or permanent certificate for every block successfully checked. The checkpoint is traversal/control state, not a timeless per-block attestation database.

### E — pause persistence ≠ exact instruction-pointer persistence

A paused scrub can survive export/restart while still resuming from a checkpoint rather than from the exact last block touched in RAM.

The useful relation is:

```text
maintenance intention survives
    + bounded progress survives
    != every transient execution detail survives
```

### E — in-memory terminal state ≠ durable completion

The 2026 bug is a concrete counterexample to treating an in-core enum transition as sufficient evidence that all state participating in maintenance completion is already on stable media.

```text
DSS_FINISHED
    != final txg synced
```

before the fix's new wait logic closes that observability window.

### E — API completion is a system contract, not merely a UI label

`zpool wait -t scrub/resilver` is used by a caller to sequence subsequent work. If it returns while final labels/configuration are still being written, the caller can immediately perform an operation against an incompletely materialized maintenance result.

Thus the completion predicate itself participates in recoverability/control semantics.

### E — sync completion ≠ universal hardware permanence proof

The 2026 patch makes the OpenZFS wait contract cover the completion txg's `spa_sync()` and its configuration/label work. This note does **not** upgrade that software boundary into a universal claim about every controller cache, drive firmware, capacitor, or medium under arbitrary power failure.

The lower-layer durability contract remains a separate question.

---

## Functional comparisons

### A — Case 100 ZFS DTL persistence

Case 100 studies a different retained control object: the DTL records replication/redundancy debt that remains to be repaired. Case 18 here studies scan execution progress and when a verification/reconstruction activity is observably complete.

The useful functional comparison is:

```text
Case 100:
    persistent maintenance debt
        -> what still needs repair

Case 18 deepening:
    persistent maintenance progress/completion state
        -> how far verification has safely advanced
        -> when callers may treat the activity as finished
```

Both show that user payload is not the only state required for storage maintenance, but they are not the same metadata and this is not a historical genealogy claim.

### A — Case 101 controller Patrol Read state

Case 101's Dell PERC material records maintenance summaries/scheduling in NVRAM but documents restart behavior in which an automatic Patrol Read can start over. OpenZFS instead documents an on-disk scrub checkpoint from which a paused scrub can resume.

The comparison is functional only:

```text
maintenance survives interruption
    can mean different things:

remember that maintenance exists
    != remember a reusable progress frontier
    != preserve every live execution detail
```

No shared implementation lineage is claimed.

### A — transaction completion and distributed commit are not interchangeable

The `txg` in this OpenZFS slice is a ZFS transaction-group durability boundary. It should not be silently renamed a Raft term, Kafka high watermark, database commit index, or distributed consensus epoch.

The analogy is only that several systems distinguish a logical state transition from the later durability/visibility boundary that makes that transition safe for subsequent actors to rely upon.

---

## Philosophical boundary

The technical result is modest but useful:

> **Maintenance can itself leave a trace that must be retained before the system may safely claim that maintenance has completed.**

That does not imply that a scrub checkpoint is `memory` in a phenomenological sense, that repetition after restart means forgetting, or that a txg is a philosophical present. The defensible mechanism-level distinctions are only:

- work performed;
- work durably checkpointed;
- terminal state reached in memory;
- terminal state durably materialized;
- completion exposed to another actor.

---

## Explicit non-claims

This evidence does **not** claim that:

1. Solaris/OpenSolaris ZFS in 2004–2010 already had the 2017 pause/resume implementation;
2. the 2017 pause/resume commit is the invention of persistent maintenance progress in storage systems;
3. every individual scrubbed block has a durable per-block verification timestamp;
4. OpenZFS persists every transient sorting-queue detail at every instant;
5. resuming from a checkpoint means zero work can ever be repeated;
6. `DSS_FINISHED` before the 2026 fix meant user payload was corrupt;
7. the 2026 race proves that every completed scrub result was lost on crash;
8. `zpool wait` returning early necessarily caused user-visible data loss;
9. the DTrace timing reported in PR #19066 is a universal latency measurement;
10. `spa_sync()` completion is a universal proof of physical-media permanence under all hardware failures;
11. scrub and resilver have identical goals merely because the wait fix covers both;
12. DTL state from Case 100 is the same object as scrub checkpoint state;
13. Dell PERC Patrol Read and OpenZFS scrub share historical lineage;
14. a periodically synced progress record is equivalent to a transactional per-block verification ledger;
15. a modern OpenZFS implementation detail may be back-projected into the bounded Sun-era Case 18 record.

---

## Claim ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| 2017 OpenZFS pause/resume was implemented with persistent on-disk scrub state | H/P | commit `0ea05c64` message/diff | supported |
| OpenZFS 2.1 documents scrub pause/progress being periodically synced to disk | H/P | `zpool-scrub(8)` | supported |
| a paused scrub survives restart/export-import and resumes from last on-disk checkpoint | H/P | `zpool-scrub(8)` | supported |
| 2.1.11 loads `DMU_POOL_SCAN` state and reconstructs in-core scan state after reboot | H/P | `dsl_scan_init()` | supported |
| 2.1.11 only writes normal persistent scan state when sorting queues are safe/empty | H/P | `dsl_scan_sync_state()` | supported |
| before the 2026 fix, waiters could observe `DSS_FINISHED` before final scan txg config/label writes completed | H/P | PR #19066; commit `92a3904` | supported |
| observed test instrumentation showed the old wait returning before `spa_sync()` finished | H/P | PR #19066 / commit message | supported, bounded to reported test |
| fix records `scn_finished_txg` when scan terminal state is set | H/P | `dsl_scan_done()` | supported |
| fix keeps scan/resilver reported in progress until `spa_last_synced_txg >= scn_finished_txg` | H/P | `spa_activity_in_progress()` | supported |
| durable maintenance progress is distinct from live maintenance progress | E | manual + implementation relation | supported reconstruction |
| terminal runtime state is distinct from durable operation completion | E | 2026 race/fix | strongly supported reconstruction |
| repeated work after restart can reflect checkpoint granularity rather than payload loss | E | documented checkpoint-resume semantics | supported reconstruction |
| final txg sync proves universal hardware permanence | E | none | **not claimed** |

---

## Source ledger

### Project-primary implementation / review record

1. OpenZFS, **“Implemented zpool scrub pause/resume”**, commit `0ea05c64f8d08c20439dd2a06e949a2aa4115101`, 2017-07-07:
   <https://github.com/openzfs/zfs/commit/0ea05c64f8d08c20439dd2a06e949a2aa4115101>
   - Explicitly identifies persistent on-disk scrub state as the pause/resume mechanism.
2. OpenZFS 2.1.11, `module/zfs/dsl_scan.c`:
   <https://github.com/openzfs/zfs/blob/zfs-2.1.11/module/zfs/dsl_scan.c>
   - `dsl_scan_init()`: reload/reconstruct after reboot.
   - `dsl_scan_sync_state()`: persistent `dsl_scan_phys_t`, queue-safe checkpoint conditions.
3. OpenZFS, **“Wait for the txg that finished a scan to sync”**, commit `92a3904afc93c3a70584f13db8f26816dc79328d`, merged 2026-09-09:
   <https://github.com/openzfs/zfs/commit/92a3904afc93c3a70584f13db8f26816dc79328d>
   - Records final scan txg and extends wait completion through txg sync.
4. OpenZFS PR #19066, **“Wait for the txg that finished a scan to sync”**, opened 2026-09-06, merged 2026-09-09:
   <https://github.com/openzfs/zfs/pull/19066>
   - Motivation, observed CI failure, DTrace timing, multi-OS validation.

### Project documentation

5. OpenZFS 2.1, `zpool-scrub(8)`:
   <https://openzfs.github.io/openzfs-docs/man/v2.1/8/zpool-scrub.8.html>
   - Pause/progress persistence and resume-from-last-checkpoint semantics.

### Existing Case 18 historical grounding

6. Sun/Oracle, _Solaris ZFS Administration Guide_, `Controlling ZFS Data Scrubbing`:
   <https://docs.oracle.com/cd/E19120-01/open.solaris/817-2271/gbbxi/index.html>
7. Thomas Schwarz et al., **“Disk Scrubbing in Large Archival Storage Systems,”** MASCOTS 2004:
   <https://www.ssrc.us/pub/schwarz-mascots04.html>

---

## Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `OpenZFS scrub`, `zpool wait`, and `dsl_scan` found no dedicated technical-history case to reuse.

The broader genealogy of ZFS scan architecture, txg machinery, Illumos/OpenZFS portability, and scan-sorting redesign belongs there if it becomes a research target. This repository should retain only the retention-specific argument:

```text
verification maintenance
    -> progress state
    -> durable checkpoint
    -> terminal state
    -> final txg durability
    -> safe completion observation
```

---

## Remaining evidence debt

This bounded slice closes the basic `pause/progress persistence` and `runtime finished vs final txg synced` distinction, but several questions remain open:

1. Trace the earliest Illumos/OpenZFS revision in which scan progress itself became restartable independently of the 2017 explicit pause UI.
2. Reproduce a paused scrub across export/import or reboot on a controlled pool and measure bounded rework between live and last-persisted frontier.
3. Reproduce the pre-`92a3904` `zpool wait` race using the historical parent commit and injected write delay, preserving exact event timing.
4. Determine precisely which completion-side state is carried by labels/configuration versus MOS objects for scrub and resilver; do not infer this only from high-level terminology.
5. Keep lower-layer flush/controller/media guarantees separate from the OpenZFS txg-sync contract.

No user decision is needed for these follow-ons; they are ordinary future evidence-deepening slices.