# Evidence 100 — OpenZFS 2026 Scan-Finish / TXG-Sync Wait Boundary

**Status:** `bounded deepening complete`

**Canonical case:** [Case 100 — ZFS Dirty Time Log: Retained Failure Intervals and Selective Resilver](../cases/100-zfs-dirty-time-log-selective-resilver.md)

## Scope

This packet asks one narrow control-state question left implicit by the earlier DTL persistence and retirement work:

> When a scrub or healing resilver has reached its in-memory `DSS_FINISHED` state, has the final DTL/configuration transition already reached the ZFS on-disk transaction boundary strongly enough that a user-visible `zpool wait` completion may safely be reported?

A September 2026 OpenZFS bug fix supplies an unusually direct answer. Before the fix, `dsl_scan_done()` could mark the scan finished and wake waiters while the transaction group carrying the DTL reassessment, scan-state update, configuration changes, and label writes was still being synced. `zpool wait -t scrub` or `zpool wait -t resilver` could therefore return during a persistence handoff that had not yet completed at the ZFS transaction-group level.

The merged fix introduces a runtime `scn_finished_txg` barrier and keeps the activity reported as in progress until:

```text
spa_last_synced_txg(spa) >= scn_finished_txg
```

This packet treats that change as a bounded retention/control-plane witness. It does **not** claim that transaction-group sync is a universal hardware durability guarantee, that all storage devices have identical cache/power-loss semantics, or that the same wait rule applies to sequential rebuild.

## Source classification

Primary implementation and review witnesses:

- **[implementation-primary]** OpenZFS commit `92a3904afc93c3a70584f13db8f26816dc79328d`, **2026-09-09**, `Wait for the txg that finished a scan to sync`;
- **[implementation-primary]** merged OpenZFS PR #19066, opened 2026-09-06 and closed/merged 2026-09-09, with motivation, observed failure timeline, and validation notes;
- **[implementation-primary]** `module/zfs/dsl_scan.c` at the merged commit, especially `dsl_scan_done()`;
- **[implementation-primary]** `module/zfs/spa.c` at the merged commit, especially `spa_activity_in_progress()` and the added waiter notification in `spa_sync()`;
- **[operator-contract primary]** `man/man8/zpool-wait.8` at the merged commit, dated 2026-05-26, defining `zpool wait` as waiting until selected background activity has ceased.

A repository search of `tmzncty/computing-archaeology` for `Dirty Time Log`, `DTL`, `resilver`, and `vdev_dtl` found no dedicated packet to reuse. Broader OpenZFS transaction-group / spa-sync implementation history belongs there if developed later.

## Historical / implementation record

### P — the public wait contract is expressed as cessation of background activity

The `zpool-wait(8)` manual at the merged commit says that `zpool wait` waits until all requested background activity types have ceased. For the relevant activities it names:

- `resilver` — resilver to cease;
- `scrub` — scrub to cease.

The manual also says the activity may cease because it completed, was paused/canceled, or because the pool was exported/destroyed.

This is an operator-facing completion/cessation contract. It does not itself specify the exact internal persistence frontier at which cessation becomes observable.

### P — before the fix, scan state could become `DSS_FINISHED` before the same txg finished syncing

The merged commit describes the old ordering directly:

```text
dsl_scan_done()
    -> mark scan DSS_FINISHED in syncing context
    -> final config / label writes of that txg still pending
```

Before the change, `spa_activity_in_progress()` treated a scrub/resilver as active primarily when:

```text
scn_state == DSS_SCANNING
```

Once `dsl_scan_done()` changed the state to `DSS_FINISHED`, a waiter could observe `in_progress = false` even though the transaction group that contained the final bookkeeping had not completed `spa_sync()`.

The bug therefore existed between two different completion frontiers:

```text
in-core activity-state completion
    !=
final txg sync completion
```

### P — DTL reassessment occurs before the scan state is marked finished

At the merged commit, `dsl_scan_done()` first handles the DTL transition for scrub/healing resilver.

For a completed scrub/resilver without the pool-checkpoint exception, it calls:

```text
vdev_dtl_reassess(
    spa->spa_root_vdev,
    tx->tx_txg,
    scn->scn_phys.scn_max_txg,
    B_TRUE,
    B_FALSE)
```

Only after this reassessment and related finishing work does it assign:

```text
scn->scn_phys.scn_state = DSS_FINISHED
```

The implementation comment added by the fix then states that the new state plus configuration and label updates reach disk when that transaction group syncs.

Thus the end of the maintenance traversal, the DTL retirement/reassessment decision, the in-memory finished flag, and the on-disk publication of the resulting configuration are separate events in one finishing sequence.

### P — the observed race was not merely theoretical

PR #19066 records a concrete failure timeline from FreeBSD testing with an injected 100 ms write delay:

- `zpool wait` returned about **10 ms after** `dsl_scan_done()`;
- the same transaction group's `spa_sync()` finished **seconds later**;
- a `zdb -PC` issued immediately after the premature wait return could encounter pool labels while they were still being rewritten and fail to open the pool with `Device not configured`.

The pull request also links CI observations where this timing problem surfaced.

This provides a rare direct engineering witness that:

> a user-visible completion notification can race ahead of persistence/control-plane publication even when the underlying maintenance algorithm itself has already reached a finished state.

### P — the fix adds a runtime finishing barrier tied to the finishing transaction group

The change adds:

```text
uint64_t scn_finished_txg;
```

to the in-core `dsl_scan_t` structure.

`dsl_scan_done()` records:

```text
scn->scn_finished_txg = tx->tx_txg;
```

when it marks the scan finished/canceled.

`spa_activity_in_progress()` then computes a separate `finishing` condition:

```text
scn_finished_txg != 0
AND
spa_last_synced_txg(spa) < scn_finished_txg
```

and reports the activity as still in progress while either:

```text
scanning || finishing
```

holds, subject to the existing scrub/resilver activity checks.

The key implementation relation is therefore:

```text
DSS_FINISHED observed in memory
    + finishing txg not yet synced
    -> zpool wait still blocks

finishing txg synced
    -> waiter may observe the activity as ceased
```

### P — `spa_sync()` now explicitly wakes waiters after the txg is on disk

The same commit adds `spa_notify_waiters(spa)` near the end of `spa_sync()` after the implementation updates the synced uberblock state.

Its new source comment states the intended contract explicitly: an activity that ended in this transaction group is only over for a reader of the pool once the transaction group is on disk.

This closes the wakeup side of the barrier. It is not enough to retain the finishing txg number; waiters also need to be re-evaluated after the relevant sync frontier advances.

### P — validation covered FreeBSD and Linux, but was a bounded bug-fix validation

PR #19066 says the fix was verified in VMs on:

- FreeBSD 14.3;
- FreeBSD 15.1;
- Linux.

The same DTrace instrumentation showed `zpool wait` returning after the final `spa_sync()`, and the `zpool_wait`, `zpool_wait/scan`, and `vdev_zaps` test groups passed.

The PR also explicitly says the original race did not reproduce on an idle machine; the diagnosis depended on the widened timing window and observed event order. This should be preserved as part of the evidence strength rather than rewritten as a universal always-reproducible failure.

## Retained-state decomposition

This slice adds one short-lived but important maintenance-control state to the Case 100 decomposition:

```text
payload / block data
    !=
DTL_MISSING repair-debt intervals
    !=
DTL_SCRUB exception intervals
    !=
scan traversal/progress
    !=
in-memory scan state (`DSS_SCANNING` / `DSS_FINISHED`)
    !=
DTL/config mutation prepared in syncing context
    !=
finishing transaction-group identity (`scn_finished_txg`)
    !=
last synced transaction-group frontier
    !=
persisted config / label publication
    !=
user-visible `zpool wait` completion
```

`scn_finished_txg` is particularly useful because it is **not** another long-lived repair-history record. It is a runtime barrier token whose job is to bridge a short interval between logical completion in syncing context and publication at the transaction-group persistence frontier.

This yields a new retention horizon:

> **some control state only needs to survive long enough to carry one completion relation across an asynchronous persistence handoff.**

That is different from DTL state, whose purpose is to survive a device outage/restart long enough to constrain later repair.

## Engineering reconstruction

The merged implementation supports the following bounded reconstruction:

```text
scan / healing resilver performs repair work
    ->
dsl_scan_done() enters syncing context
    ->
vdev_dtl_reassess() updates repair-debt relation
    ->
config / labels are dirtied in the same txg
    ->
in-memory scan state becomes DSS_FINISHED
    ->
record scn_finished_txg
    ->
user-visible wait still sees "finishing"
    ->
spa_sync() completes the txg's on-disk publication
    ->
last-synced frontier reaches scn_finished_txg
    ->
notify waiters
    ->
`zpool wait` may return
```

Project term:

> **completion-publication barrier** — runtime state that prevents a completion observer from treating an operation as finished before the transaction carrying its final persistent control-plane consequences reaches the required publication frontier.

This is project engineering vocabulary, not an OpenZFS historical term.

## Why this belongs in Case 100

Case 100 already distinguishes:

```text
maintenance activity ended
    !=
repair debt retired
```

The 2026 fix adds another independent boundary:

```text
repair debt reassessed / scan state finished in memory
    !=
final reassessment/config state synced to disk
    !=
completion safely reportable to a reader waiting on that activity
```

These are three different questions:

1. **did the maintenance algorithm reach its end path?**
2. **what repair-debt state did that end path produce?**
3. **has the transaction publishing that state crossed the wait command's completion frontier?**

The bug existed because question 1 was being used as a proxy for question 3.

## Persistence-horizon boundary

The new `scn_finished_txg` field should not be mistaken for another durable maintenance checkpoint.

Its required horizon is much shorter:

```text
created when scan is marked finished
    -> retained in memory while final txg is syncing
    -> no longer needed once last_synced_txg reaches it
```

A crash before that final transaction group reaches disk does not require `scn_finished_txg` itself to survive. The durable question after restart is instead answered by whatever scan/config/DTL state actually made it into the pool's committed on-disk state.

Therefore:

> **runtime completion barrier != restart checkpoint.**

and:

> **short-lived control-state retention can still be necessary for correct completion semantics.**

## Completion semantics

The source gives several distinct completion notions that must not be collapsed:

### Traversal completion

The scan has finished issuing/processing the relevant maintenance traversal.

### DTL reassessment completion

`vdev_dtl_reassess()` has computed the new repair-debt relation for the finishing path.

### In-memory scan-state completion

`scn_state` has become `DSS_FINISHED` or `DSS_CANCELED`.

### Transaction-group sync completion

The txg carrying the state/config/label consequences has completed `spa_sync()` and advanced the pool's last-synced frontier.

### Wait-interface completion

A waiting user process is allowed to observe the activity as ceased and return.

The September 2026 change deliberately moves the last boundary later so that it follows transaction-group sync rather than only in-memory state transition.

## Failure / edge boundaries

### F — premature completion notification

Before the fix, a waiter could return in the interval:

```text
DSS_FINISHED
    ...
final txg still syncing
```

This is a control-plane ordering failure, not evidence that the repaired user payload itself was corrupt.

### F — reader enters while labels are mid-rewrite

The recorded `zdb -PC` failure shows that a command run immediately after premature wait return could encounter labels during the final rewrite window.

The bounded conclusion is:

> **maintenance state finished != every post-maintenance reader can yet rely on the final on-disk control state.**

It is not a claim that every reader fails or that label rewrite necessarily corrupts the pool.

### F — wakeup before durability/publication frontier

A condition variable or waiter notification can itself be too early if the condition being exposed is defined by a later persistence frontier.

The fix therefore changes both:

- the predicate (`finishing` until txg sync);
- the notification point (wake again after `spa_sync()`).

Retaining only one side would not provide the intended interface relation.

## Functional analogy

A bounded analogy is a database commit callback:

```text
transaction logic decides "done"
    !=
commit record / durable publication completed
    !=
client callback safely released
```

This analogy is functional only. OpenZFS transaction groups, vdev labels, DTLs, and `zpool wait` are not being identified with a relational-database WAL protocol, and no genealogy is claimed.

A second bounded analogy is a hardware completion queue whose producer has finished computation but must not publish the completion entry until earlier writes cross the required visibility barrier. Again, this is only a relation-level comparison.

## Philosophical / media-theoretical interpretation

`I` — The maintenance event does not become operationally past at one instant. It crosses several boundaries: work can end, repair-debt state can be recomputed, the in-memory status can become finished, the final transaction can become part of the on-disk pool state, and only then can a waiting observer be released under the strengthened contract.

`I` — This is a small but concrete example of technical retention depending on **temporal ordering among retained relations**, not only on preservation of payload. The final repair relation must not merely exist; the system must delay the social/operational fact of “finished” until that relation is published across the chosen persistence boundary.

`I` — The added field is intentionally temporary. Its significance is not longevity but its ability to hold open a relation between two moments that would otherwise be collapsed. Technical retention therefore includes very short-lived state when that state is what preserves ordering across an asynchronous handoff.

These are project interpretations, not claims made by the OpenZFS developers.

## Cross-case comparison

### Case 13 / durability-handoff synthesis

The repository's durability-handoff work separates operation completion, intermediate residence, persistence-boundary arrival, failure model, and recovery. This OpenZFS slice is a concrete control-plane instance of the same broad distinction:

```text
operation-state completion != persistence-boundary arrival
```

The comparison is functional. A ZFS txg sync is not automatically equivalent to SCSI FUA, NVMe FLUSH, ADR/eADR, or any one hardware persistence-domain contract.

### Earlier Case 100 DTL retirement deepening

The 2.1.11 retirement packet established:

```text
scan/rebuild completion != unconditional repair-debt clearance
```

The 2026 packet adds:

```text
qualified repair-debt update performed
    !=
update's final txg synced
    !=
wait-interface completion
```

Together they prevent a single undifferentiated `finished` bit from standing for traversal, repair obligation, durable control state, and observer release.

## Explicit non-claims

This packet does **not** establish:

1. that OpenZFS transaction-group sync is an unconditional guarantee against every hardware power-loss failure mode;
2. that `spa_sync()` bypasses every volatile device cache or controller cache;
3. that the 2026 change alters the DTL repair algorithm itself;
4. that `DSS_FINISHED` was incorrect as an internal scan-state label;
5. that every command issued after the old premature wait return failed;
6. that every pool label was corrupt during the observed window;
7. that the observed FreeBSD timing reproduces on every machine;
8. that `scn_finished_txg` is a durable on-disk restart checkpoint;
9. that `scn_finished_txg` must survive process/kernel restart;
10. that sequential rebuild now uses the same finishing-txg wait barrier — the commit explicitly leaves the rebuild predicate above this path alone;
11. that a scrub/resilver finishing txg contains all user payload ever repaired by the operation;
12. that synced final metadata proves all latent corruption has been found;
13. that wait-interface completion proves future hardware cannot fail;
14. that a user-visible completion callback and a data-integrity certificate are the same thing;
15. that this September 2026 merged commit is already present in every downstream OpenZFS release/distribution;
16. that an implementation bug fix by itself establishes how historical Solaris ZFS behaved in 2005–2007.

## Evidence strength

### Strong

- merged upstream implementation commit with exact code diff;
- accepted PR containing developer-authored diagnosis, observed timing, and test environment;
- source inspection of `dsl_scan_done()` and `spa_activity_in_progress()` at the merged commit;
- operator man page establishing the public wait/cessation vocabulary.

### Bounded

- the failure was timing-sensitive and intentionally widened with delayed writes;
- the new relation is verified at the ZFS txg/on-disk publication level, not every possible lower hardware persistence domain;
- the commit is current upstream source, not a universal downstream-release witness;
- sequential rebuild is explicitly outside the new scan-finishing predicate.

## Sources

Primary sources:

- OpenZFS commit `92a3904afc93c3a70584f13db8f26816dc79328d`, `Wait for the txg that finished a scan to sync`, merged 2026-09-09: <https://github.com/openzfs/zfs/commit/92a3904afc93c3a70584f13db8f26816dc79328d>
- OpenZFS PR #19066, opened 2026-09-06, merged 2026-09-09: <https://github.com/openzfs/zfs/pull/19066>
- `module/zfs/dsl_scan.c` at the merged commit: <https://github.com/openzfs/zfs/blob/92a3904afc93c3a70584f13db8f26816dc79328d/module/zfs/dsl_scan.c>
- `module/zfs/spa.c` at the merged commit: <https://github.com/openzfs/zfs/blob/92a3904afc93c3a70584f13db8f26816dc79328d/module/zfs/spa.c>
- `man/man8/zpool-wait.8` at the merged commit: <https://github.com/openzfs/zfs/blob/92a3904afc93c3a70584f13db8f26816dc79328d/man/man8/zpool-wait.8>

Repository context:

- [Case 100 canonical](../cases/100-zfs-dirty-time-log-selective-resilver.md)
- [OpenZFS 2.1.11 DTL persistence/reload deepening](100-openzfs-211-dtl-persistence-reload-deepening.md)
- [OpenZFS 2.1.11 DTL retirement/excision deepening](100-openzfs-211-dtl-retirement-excision-deepening.md)

## Remaining evidence debt

This slice closes only the bounded **scan-finished vs finishing-txg sync vs wait-return** seam. It leaves several narrower questions open:

- identify the first release/tag that contains commit `92a3904a` and record downstream adoption separately from upstream merge;
- inspect whether any earlier illumos/OpenZFS lineage had an equivalent final-sync wait barrier under different code/vocabulary;
- test a deliberately delayed-I/O mirror locally and capture the old-vs-new event ordering with exact txg/label traces if experimental infrastructure is available;
- keep sequential rebuild separate and inspect its own `zpool wait` completion boundary rather than projecting this scan-path fix onto it;
- if a later claim needs hardware-level durability, pair this txg-level witness with the relevant cache flush / device persistence-domain evidence rather than treating `spa_sync()` as the bottom of the stack.
