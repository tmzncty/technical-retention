# Evidence deepening — Case 96: OpenZFS 2.1.0 device-rebuild progress, restart, and maintenance-state horizons

**Case:** [`cases/96-openzfs-draid-distributed-spare-sequential-resilver.md`](../cases/96-openzfs-draid-distributed-spare-sequential-resilver.md)  
**Status:** `grounded` (no maturity promotion in this slice)  
**Bounded release:** OpenZFS `zfs-2.1.0`, released 2021-07-02  
**Release commit:** `4f92fe0f5c822f6802c6ec675809d7c112a46f2e`  
**Research slice:** what rebuild state survives export/import or process/runtime loss, what is reconstructed, and what remains separately represented as repair need.

---

## Research question

Case 96 already establishes that OpenZFS dRAID can use distributed spare capacity and sequential reconstruction to shorten the interval of reduced redundancy, while leaving checksum verification to a later scrub.

This deepening asks a narrower question:

> **If a sequential device rebuild is interrupted by pool export/import or loss of its in-core scan thread, what state must survive so that the maintenance obligation can continue without replaying the entire prior scan as history?**

The answer in the OpenZFS 2.1.0 implementation is not `the rebuild thread survives` and not `every issued I/O is journaled`.

The released source instead separates at least four layers:

```text
repair need / missing-TXG relation
    != persisted rebuild activity + progress frontier
    != in-core per-TXG scan offsets / inflight-I/O state
    != reconstructed payload already materialized on replacement/spare paths
```

The most important bounded result is:

> **A rebuild can survive an export/import by persisting a compact restart frontier and rebuilding its in-core scan machinery, while the deeper repair obligation remains represented separately by DTL state.**

This is a maintenance-state retention claim, not a claim that the exact microstate of the old thread or every completed I/O is preserved.

---

## Evidence classification

| Source | Date / version | Class | Used for | Not used for |
| --- | --- | --- | --- | --- |
| OpenZFS tag `zfs-2.1.0` | 2021-07-02 | `H/P` release provenance | immutable release boundary | later OpenZFS behavior |
| `include/sys/vdev_rebuild.h` at 2.1.0 | 2021 release source | `H/P` primary implementation | explicit split between on-disk `vdev_rebuild_phys_t` and in-core rebuild fields | lower-layer media-atomicity proof |
| `module/zfs/vdev_rebuild.c` at 2.1.0 | 2021 release source | `H/P` primary implementation | checkpoint update, load, restart, export/import resumption, completion/DTL handoff | universal RAID rebuild semantics |
| `module/zfs/spa.c` at 2.1.0 | 2021 release source | `H/P` primary implementation | pool-load path explicitly resumes an active rebuild before ordinary DTL resilver checking | proof that every crash/power-cut point has been fault-injected |
| OpenZFS PR #10102 | opened 2020-03-04; merged 2020-11-13 | `H/P` project-development record | dRAID feature merge and test-development context | exact release-state durability beyond code inspected here |
| Case 100 DTL evidence | repository comparison | `A/E` functional comparison | distinguishes repair-need evidence from scan-progress evidence | historical genealogy |
| Case 83 HDFS scanner evidence | repository comparison | `A/E` functional comparison | bounded comparison of restartable maintenance cursors | equivalence of failure consequences |

`H/P` = historical/project primary evidence.  
`E` = engineering reconstruction by this repository.  
`A` = functional analogy only.

---

## 1. Release provenance

The signed `zfs-2.1.0` tag points to commit:

```text
4f92fe0f5c822f6802c6ec675809d7c112a46f2e
```

Primary provenance:

- tag ref: <https://github.com/openzfs/zfs/releases/tag/zfs-2.1.0>
- immutable source commit: <https://github.com/openzfs/zfs/tree/4f92fe0f5c822f6802c6ec675809d7c112a46f2e>
- accepted dRAID feature PR: <https://github.com/openzfs/zfs/pull/10102>

The release boundary matters because rebuild persistence is an implementation property. Later source may refine, replace, or extend these structures and must not be silently projected backward into 2.1.0.

---

## 2. Historical record: the implementation explicitly defines on-disk rebuild state

Primary source:

- <https://github.com/openzfs/zfs/blob/4f92fe0f5c822f6802c6ec675809d7c112a46f2e/include/sys/vdev_rebuild.h>

The header describes `vdev_rebuild_phys_t` as **on-disk rebuild configuration and state** and defines twelve `uint64_t` entries:

```text
vrp_rebuild_state
vrp_last_offset
vrp_min_txg
vrp_max_txg
vrp_start_time
vrp_end_time
vrp_scan_time_ms
vrp_bytes_scanned
vrp_bytes_issued
vrp_bytes_rebuilt
vrp_bytes_est
vrp_errors
```

The same header separately defines the in-core `vdev_rebuild_t`, including:

```text
vr_scan_offset[TXG_SIZE]
vr_prev_scan_time_ms
vr_bytes_inflight_max
vr_bytes_inflight
vr_pass_start_time
vr_pass_bytes_scanned
vr_pass_bytes_issued
```

and embeds the on-disk `vdev_rebuild_phys_t` as `vr_rebuild_phys`.

### Supported historical claim

The release source itself therefore distinguishes:

```text
persisted rebuild representation
    != all live execution state used while the scan is running
```

This distinction is direct implementation evidence. It does not require reconstructing intent from variable names alone; the header comments explicitly mark one structure as on-disk and the other fields as in-core state/progress.

### Boundary

The source does **not** establish that every field reaches stable physical media at the instant a CPU assignment occurs. The bounded historical claim is about the ZFS on-disk transaction/state model visible in this implementation, not an unqualified power-fail guarantee for every controller/cache/device below ZFS.

---

## 3. Historical record: rebuild start creates a persistent active state and captures repair scope

Primary source:

- <https://github.com/openzfs/zfs/blob/4f92fe0f5c822f6802c6ec675809d7c112a46f2e/module/zfs/vdev_rebuild.c>
- function: `vdev_rebuild_initiate_sync()`

At rebuild initiation, the implementation:

1. zeroes the physical rebuild structure;
2. sets `vrp_rebuild_state = VDEV_REBUILD_ACTIVE`;
3. records the rebuild start time;
4. calls `vdev_resilver_needed()` to derive `vrp_min_txg` and `vrp_max_txg` from the missing-DTL relation;
5. writes the rebuild structure into the top-level vdev ZAP under `VDEV_TOP_ZAP_VDEV_REBUILD_PHYS`;
6. starts the rebuild thread.

The source comment is especially important: device rebuilds are currently used when replacing a device, **in which case there must be `DTL_MISSING` entries**.

### Engineering reconstruction

This gives two distinct kinds of retained maintenance evidence:

```text
DTL_MISSING / missing-TXG relation
    = why repair is still owed

VDEV_TOP_ZAP_VDEV_REBUILD_PHYS
    = state/progress of this particular sequential rebuild episode
```

The two relations cooperate, but they are not identical.

A rebuild episode does not invent the missing-data obligation. It is one mechanism for discharging an already represented obligation.

---

## 4. Historical record: scan progress is folded from in-core per-TXG state into on-disk state

Primary source:

- same released `vdev_rebuild.c`
- function: `vdev_rebuild_update_sync()`

The sync task checks the in-core per-TXG `vr_scan_offset[txg & TXG_MASK]`. When it is non-zero, the code transfers that value into:

```text
vrp->vrp_last_offset
```

and clears the in-core slot.

It then updates accumulated scan time and performs:

```text
zap_update(...,
    VDEV_TOP_ZAP_VDEV_REBUILD_PHYS,
    ...,
    vrp,
    tx)
```

### Supported historical claim

The release implementation deliberately **compresses live scan progress into a persistent restart representation**.

It does not persist every loop iteration, every I/O object, every queue entry, or every thread-local fact.

### Engineering reconstruction

The retained state is therefore a frontier, not a transcript:

```text
complete execution history
    unnecessary for restart

persisted last-offset frontier
    + current allocation/space-map state
    + retained repair-need relation
    -> enough information to continue the maintenance process
```

This is a direct example of **state retention without history retention** inside a repair mechanism.

---

## 5. Historical record: the restart path treats `vrp_last_offset` as a completed lower-bound frontier

Primary source:

- same released `vdev_rebuild.c`
- `vdev_rebuild_thread()`

For each metaslab, the rebuild thread reconstructs the current allocated range set from the space map, adding unflushed allocations and removing unflushed frees.

The release source then says:

> remove ranges which have already been rebuilt based on the last offset; this can happen when restarting a scan after exporting and re-importing the pool.

The code performs:

```text
range_tree_clear(vr->vr_scan_tree, 0, vrp->vrp_last_offset)
```

Another source comment in `vdev_rebuild_update_bytes_est()` says that only allocated capacity beyond `vrp_last_offset` must be considered because all lower offsets must already have been rebuilt.

### Supported historical claim

OpenZFS 2.1.0 explicitly uses `vrp_last_offset` as restart evidence after export/import.

This is stronger than merely finding a progress counter in a status command. The source consumes the retained frontier to change future repair work.

### Engineering reconstruction

A progress number becomes constitutive maintenance state when it changes which work is still admissible/required:

```text
persistent frontier F
    -> ranges below F treated as already rebuilt
    -> current allocated ranges at/above F remain candidates
```

Thus:

```text
progress telemetry
    != necessarily constitutive progress state

but here

vrp_last_offset
    participates directly in restart work selection
```

---

## 6. Historical record: export/suspension preserves the active episode rather than converting it to completion

Primary source:

- same released `vdev_rebuild.c`
- end of `vdev_rebuild_thread()`
- `vdev_rebuild_stop_all()`

When the rebuild thread stops for reasons that are neither successful completion, explicit cancellation, nor reset/restart caused by attaching a new device, the source states that the operation is **suspended**.

The comment names pool export as one such reason and says the rebuild is left in the active state so that it will be resumed.

`vdev_rebuild_stop_all()` likewise says it stops all rebuild operations while leaving them active so that they can be resumed when the pool is imported.

### Boundary

This is not `completion survives export`.

It is:

```text
unfinished maintenance obligation
    + active-episode state
    + restart frontier
    survive the administrative stop/import boundary
```

The operation remains unfinished precisely because completion has not been established.

---

## 7. Historical record: pool load explicitly resumes the active rebuild

Primary source:

- <https://github.com/openzfs/zfs/blob/4f92fe0f5c822f6802c6ec675809d7c112a46f2e/module/zfs/spa.c>
- same release's `vdev_rebuild.c`: `vdev_rebuild_active()` and `vdev_rebuild_restart()`

The pool-load path contains an explicit comment and branch:

```text
Check if a rebuild was in progress and if so resume it.
Then check all DTLs to see if anything needs resilvering.
The resilver will be deferred if a rebuild was started.
```

If `vdev_rebuild_active()` reports active state, it invokes `vdev_rebuild_restart(spa)`.

The restart implementation starts a new rebuild thread only when the retained rebuild state is `VDEV_REBUILD_ACTIVE`, the vdev is writable, and there is not already a running rebuild thread.

### Supported historical claim

The continuation identity of the maintenance episode is represented by retained state; it is **not** the identity of one continuously surviving kernel thread.

### Engineering reconstruction

```text
old thread lifetime
    != rebuild episode lifetime

restart after import
    = reconstruct new execution machinery
      from retained maintenance state
```

This is a clean instance of logical maintenance continuity through execution-process discontinuity.

---

## 8. Historical record: a missing or damaged rebuild checkpoint does not block pool import

Primary source:

- released `vdev_rebuild.c`
- function: `vdev_rebuild_load()`

The loader retrieves `VDEV_TOP_ZAP_VDEV_REBUILD_PHYS` from the top-level vdev ZAP.

Its comment is unusually explicit:

> A missing or damaged `VDEV_TOP_ZAP_VDEV_REBUILD_PHYS` should not prevent a pool from being imported. Clear the rebuild status allowing a new resilver/rebuild to be started.

For `ENOENT`, `EOVERFLOW`, or `ECKSUM`, the code zeroes the rebuild structure rather than failing the import.

### Supported historical claim

Pool importability is not made equivalent to preservation of the sequential-rebuild checkpoint.

### Engineering reconstruction

This yields a particularly useful retention boundary:

```text
pool payload / metadata sufficiently recoverable for import
    != saved sequential-rebuild episode still recoverable
```

And because the same source subsequently checks DTL state for resilver need:

```text
loss of one maintenance-progress representation
    != automatic loss of the underlying repair obligation
```

The rebuild checkpoint can be disposable/reconstructible at one layer while DTL and pool state still make the need for repair visible at another.

### Important non-claim

This does **not** mean a damaged checkpoint is harmless in performance terms. Clearing it can discard useful progress information and may require broader repeated work. The source only establishes that the pool should remain importable and another repair pass can be started.

---

## 9. Historical record: completion retires one repair relation and opens another verification relation

Primary source:

- released `vdev_rebuild.c`
- `vdev_rebuild_complete_sync()` and completion path in `vdev_rebuild_thread()`

On successful completion, the implementation:

1. sets `vrp_rebuild_state = VDEV_REBUILD_COMPLETE`;
2. records end time;
3. persists the rebuild physical structure;
4. calls `vdev_dtl_reassess()` for the relevant TXG range;
5. decrements the active device-rebuild feature state;
6. may start a scrub when no active sequential rebuild remains.

The thread-side comment says that after a successful rebuild the DTLs for ranges missing when the rebuild started can be cleared because all allocated space has been reconstructed.

### Engineering reconstruction

The first-phase completion relation therefore is not merely `thread exited normally`.

It changes the retained maintenance graph:

```text
DTL repair obligation
    -> sequential rebuild
    -> completed reconstruction
    -> DTL reassessment / cleared missing relation
    -> optional/default scrub verification obligation
```

Case 96 already established:

```text
redundancy restored
    != checksum integrity fully revalidated
```

This deepening adds:

```text
rebuild progress retained
    != rebuild completion established
    != DTL repair debt retired
    != later checksum verification completed
```

---

## 10. State decomposition

The released implementation supports a more precise Case-96 state model.

### 10.1 Repair-need state

Examples:

- DTL missing intervals;
- `vrp_min_txg` / `vrp_max_txg` captured for the rebuild episode.

Question answered:

> What history interval / target relation still requires reconstruction?

### 10.2 Persistent rebuild-episode state

Examples:

- `vrp_rebuild_state`;
- `vrp_last_offset`;
- timing/counter/error fields;
- saved min/max TXG bounds.

Question answered:

> Is a sequential rebuild active/complete/canceled, and what restart frontier has been retained?

### 10.3 In-core execution state

Examples:

- per-TXG `vr_scan_offset[]`;
- in-flight byte count;
- current metaslab/range tree;
- thread/condition-variable/lock state;
- current pass counters.

Question answered:

> What is the currently executing repair machinery doing right now?

### 10.4 Material reconstruction state

Examples:

- reconstructed contributions already written to spare/replacement paths;
- still-missing contributions.

Question answered:

> Which redundancy relation has actually been materialized?

### 10.5 Verification state

Examples:

- later scrub/checksum observations.

Question answered:

> Has the reconstructed relation also been revalidated at the block/checksum layer?

These layers must not be collapsed.

---

## 11. Central retention findings

### Finding 1 — maintenance-process identity does not require execution-thread identity

A rebuild may be stopped for export, later imported, and resumed by creating a new rebuild thread.

Therefore:

```text
same maintenance obligation / episode
    != same continuously living thread
```

### Finding 2 — restartable progress can be compressed to a frontier

The implementation does not persist the complete scan path as a history log. It persists a last-offset frontier and reconstructs the current workset from space maps.

Therefore:

```text
restartability
    != full execution-history retention
```

### Finding 3 — current allocation state participates in restart semantics

On restart, the code reloads allocated ranges from current space maps and also accounts for unflushed allocations/frees before applying the persisted last-offset frontier.

Therefore:

```text
persisted cursor alone
    != complete restart workset
```

The cursor is interpreted together with current allocation metadata.

### Finding 4 — repair need and repair progress are separately retained

The DTL expresses missing-replication history/need; the rebuild ZAP state expresses the progress of one sequential reconstruction episode.

Therefore:

```text
why repair is owed
    != how far this repair pass has progressed
```

### Finding 5 — loss of progress evidence need not equal loss of repair obligation

The loader intentionally permits pool import after a missing/damaged rebuild-state object, clearing the episode state so another resilver/rebuild can start.

Therefore:

```text
maintenance checkpoint loss
    != necessarily payload loss
    != necessarily repair-need loss
```

### Finding 6 — progress persistence is not exact microstate persistence

Per-TXG offsets and in-flight I/O accounting exist in memory; restart uses the persisted physical structure and reconstructs fresh execution state.

Therefore:

```text
restart from retained frontier
    != continuation of exact pre-stop microstate
```

### Finding 7 — repair completion is an authority transition

Only successful completion leads to the completion sync task, DTL reassessment, feature-state transition, and later scrub setup.

Therefore:

```text
some bytes reconstructed
    != repair obligation retired
```

---

## 12. Cross-case comparison — Case 100 ZFS DTL

Case 100 studies Dirty Time Log state as a bounded summary of replication exposure: a target may have missed writes during a TXG interval, and that retained interval can guide selective resilver work.

Case 96's rebuild checkpoint answers a different question.

```text
Case 100 DTL:
    which transaction-time interval may be missing on this target?

Case 96 rebuild frontier:
    how far through this sequential reconstruction episode has work progressed?
```

The two are related but non-substitutable.

### Functional comparison only

```text
repair-scope evidence
    != repair-progress evidence
```

No claim is made that DTL and `vrp_last_offset` share one historical origin or one data structure.

---

## 13. Cross-case comparison — Case 83 HDFS scanner cursor

Case 83 preserves a maintenance cursor for periodic integrity scanning. HDFS can reload scan progress after restart, while corruption/missing cursor state can cause the scanner to recreate its iterator rather than making block payload unrecoverable.

Case 96 provides a stronger redundancy-repair version of a similar relational shape:

```text
maintenance target population
    + retained progress frontier
    + restart reconstruction
```

But the consequences differ.

- HDFS scanner progress primarily controls verification coverage latency.
- dRAID rebuild progress participates in how quickly reduced redundancy is eliminated.

Therefore this is a **functional analogy only**, not a shared mechanism or genealogy.

---

## 14. Cross-case comparison — Case 148 NVMe extended self-test

Case 148 distinguishes a reset-surviving diagnostic operation from the exact internal checkpoint state used to resume it.

Case 96 supplies an implementation-visible counterpoint: here the release source exposes an explicit persisted frontier (`vrp_last_offset`) and reconstructs the runtime worker from it.

The comparison supports:

```text
operation identity survival
    != exact execution-state survival
```

It does not imply that NVMe self-test and ZFS rebuild use comparable checkpoint formats.

---

## 15. Prior-art / terminology boundary

This slice does **not** reopen the broad history of RAID rebuild checkpointing.

The repository's `computing-archaeology` companion should own questions such as:

- earliest disk-array rebuild progress checkpoint;
- vendor RAID controller implementations;
- parity-declustering implementation genealogy;
- distributed spare history beyond the already cited CMU work;
- historical evolution of ZFS scan/resilver persistence generally.

This file is narrower:

> the exact maintenance-state separation visible in the released OpenZFS 2.1.0 device-rebuild implementation.

Period/project vocabulary retained here includes:

- `device rebuild`;
- `sequential reconstruction`;
- `rebuild state`;
- `last offset`;
- `DTL_MISSING`;
- `resilver`;
- `scrub`.

Project analytical vocabulary includes:

- **restart frontier**;
- **repair obligation**;
- **maintenance-process identity**;
- **repair-progress evidence**.

Those project terms must not be retroactively attributed to OpenZFS developers.

---

## 16. Philosophical / media-theoretical interpretation

`I` — A long-running maintenance process can persist without its execution apparatus persisting continuously. What survives is a relation sufficient to reconstruct the next admissible action.

`I` — The stored rebuild frontier is neither user payload nor a complete memory of past operations. It is a deliberately compressed trace whose value lies in constraining future maintenance.

`I` — The implementation therefore makes a useful distinction between **remembering that repair is owed**, **remembering how far repair got**, and **remembering every event that occurred during repair**.

These are project interpretations, not period OpenZFS philosophical claims.

---

## 17. Explicit non-claims

This evidence does **not** establish any of the following:

1. that OpenZFS invented rebuild checkpointing;
2. that `vrp_last_offset` records every completed I/O individually;
3. that every in-flight I/O survives export/import;
4. that the same kernel thread survives export/import;
5. that saved progress proves every reconstructed block checksum is correct;
6. that the rebuild checkpoint is the sole source of repair need;
7. that losing the checkpoint implies losing user payload;
8. that losing the checkpoint is performance-free;
9. that `zap_update()` alone proves stable-media persistence under every disk/controller cache policy;
10. that a successful pool import proves every rebuild target is already fully redundant;
11. that a completed first-phase device rebuild proves the follow-up scrub has completed;
12. that current OpenZFS retains exactly the same fields/semantics as 2.1.0;
13. that ordinary RAID-Z has the same restart geometry as dRAID sequential rebuild;
14. that HDFS scanner cursors, NVMe self-test resume state, and ZFS rebuild checkpoints share one genealogy;
15. that this source-level analysis substitutes for hardware power-cut or crash fault injection.

---

## 18. Remaining evidence debt

The next useful work should be narrow rather than generic dRAID expansion.

### High-value follow-ups

- locate the 2.1.0 ZTS test that explicitly interrupts a device rebuild with export/import or reboot and verify what progress is expected to survive;
- trace the exact transaction ordering from rebuild I/O completion to `vrp_last_offset` advancement under the TXG root, without assuming more than the source establishes;
- fault-inject pool export/import, process/module interruption, and host power loss at controlled rebuild offsets;
- measure whether work beyond the last persisted frontier is safely repeated after restart;
- test missing/corrupt `VDEV_TOP_ZAP_VDEV_REBUILD_PHYS` while DTL still records repair need;
- compare later OpenZFS releases for changes to rebuild checkpoint representation or restart policy;
- inspect lower persistence layers if making a strict power-loss durability claim about the rebuild ZAP update itself.

### Lower-value / out-of-scope for this case

- generic `what is RAID` material;
- another broad dRAID performance summary;
- repeating the already grounded distributed-spare benchmark;
- full ZFS history;
- broad parity-declustering genealogy better suited to `computing-archaeology`.

---

## 19. Source ledger

### OpenZFS 2.1.0 release / tag

- <https://github.com/openzfs/zfs/releases/tag/zfs-2.1.0>
- tag target commit: `4f92fe0f5c822f6802c6ec675809d7c112a46f2e`

### Rebuild state structure

- <https://github.com/openzfs/zfs/blob/4f92fe0f5c822f6802c6ec675809d7c112a46f2e/include/sys/vdev_rebuild.h>
- key symbols: `REBUILD_PHYS_ENTRIES`, `vdev_rebuild_phys_t`, `vdev_rebuild_t`

### Rebuild implementation

- <https://github.com/openzfs/zfs/blob/4f92fe0f5c822f6802c6ec675809d7c112a46f2e/module/zfs/vdev_rebuild.c>
- key symbols:
  - `vdev_rebuild_initiate_sync()`;
  - `vdev_rebuild_update_sync()`;
  - `vdev_rebuild_load()`;
  - `vdev_rebuild_thread()`;
  - `vdev_rebuild_active()`;
  - `vdev_rebuild_restart()`;
  - `vdev_rebuild_stop_all()`;
  - `vdev_rebuild_complete_sync()`.

### Pool-load restart path

- <https://github.com/openzfs/zfs/blob/4f92fe0f5c822f6802c6ec675809d7c112a46f2e/module/zfs/spa.c>
- relevant pool-load comment: resume an in-progress rebuild, then inspect DTLs for any additional resilver need.

### Development record

- OpenZFS PR #10102, `Distributed Spare (dRAID) Feature`: <https://github.com/openzfs/zfs/pull/10102>
- opened 2020-03-04; merged 2020-11-13.

---

## 20. Compact result

The evidence chain for this slice is:

```text
DTL says repair is owed
    ↓
new sequential rebuild captures missing-TXG scope
    ↓
ACTIVE rebuild state is persisted in top-level ZAP
    ↓
live scan maintains richer in-core execution state
    ↓
per-TXG scan progress is folded into persisted vrp_last_offset
    ↓
export can stop the worker while leaving rebuild ACTIVE
    ↓
pool import loads persisted rebuild state
    ↓
ACTIVE state causes a new rebuild thread to be created
    ↓
current space-map ranges are reconstructed
    ↓
ranges below persisted last_offset are excluded as already rebuilt
    ↓
successful completion reassesses/clears the relevant DTL repair debt
    ↓
follow-up scrub can restore checksum-qualified confidence
```

The bounded Case-96 conclusion is therefore:

> **OpenZFS 2.1.0 retains enough maintenance-control state to continue a sequential device rebuild across export/import without retaining the old worker's exact execution microstate or a complete repair history. The retained rebuild checkpoint is distinct from the DTL relation that says repair is still owed, and both are distinct from later checksum-verification evidence.**
