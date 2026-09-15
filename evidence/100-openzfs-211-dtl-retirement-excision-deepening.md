# Evidence 100 — OpenZFS 2.1.11 DTL Retirement, Qualified Excision, and Repair-Completion Boundary

**Status:** `bounded deepening complete`

**Canonical case:** [Case 100 — ZFS Dirty Time Log: Retained Failure Intervals and Selective Resilver](../cases/100-zfs-dirty-time-log-selective-resilver.md)

## Scope

This packet asks one narrow implementation question left open by the earlier DTL persistence deepening:

> In OpenZFS 2.1.11, when may retained `DTL_MISSING` repair-debt state actually be removed after a resilver, scrub, or sequential rebuild, and what prevents a generic “scan finished” event from erasing still-relevant repair history?

The bounded answer is that DTL retirement is **qualified, range-bounded, and exception-preserving**. The implementation does not equate completion of a maintenance activity with unconditional deletion of its retained repair evidence.

The source path separates at least four decisions:

1. whether a scan/rebuild reached a completion path that permits excision to be considered;
2. whether a particular leaf vdev was eligible to have its DTL excised for that maintenance interval;
3. which transaction-group range may be removed from `DTL_MISSING`;
4. which scan-discovered exceptions must survive that removal.

This packet is source-level and version-bounded to OpenZFS 2.1.11. It does not claim that the same conditions existed unchanged in early Solaris/ZFS releases, nor does it close the full cross-version genealogy requested by the canonical case.

## Source classification

Primary implementation witnesses:

- **[implementation-primary]** OpenZFS 2.1.11 `module/zfs/vdev.c` — DTL class definitions, `vdev_dtl_should_excise()`, `vdev_dtl_reassess()`, and DTL update/persistence-related state transitions;
- **[implementation-primary]** OpenZFS 2.1.11 `module/zfs/dsl_scan.c` — scan completion/cancel paths that call `vdev_dtl_reassess()`;
- **[implementation-primary]** OpenZFS 2.1.11 `module/zfs/vdev_rebuild.c` — sequential-rebuild completion path and the call into `vdev_dtl_reassess()`.

A search of `tmzncty/computing-archaeology` for `DTL` / `resilver` found no dedicated DTL/resilver research packet to reuse. Broader ZFS repair genealogy still belongs there if developed later.

## Historical / implementation record

### P — OpenZFS distinguishes missing, partial, scrub-exception, and outage DTL classes

OpenZFS 2.1.11 documents four distinct DTL meanings in `vdev.c`:

- `DTL_MISSING` — transaction groups for which the vdev has no valid copies of the data;
- `DTL_PARTIAL` — transaction groups for which data is available but not fully replicated;
- `DTL_SCRUB` — transaction groups that could not be repaired by the last scrub; on scrub completion, this state replaces `DTL_MISSING` inside the scrubbed range;
- `DTL_OUTAGE` — transaction groups that cannot currently be read, whether due to persistent errors or an offline device.

The source vocabulary itself therefore blocks a single-bit model of `needs repair`.

For this packet the key point is `DTL_SCRUB`: a successful traversal/completion path can coexist with transaction-group intervals that the scan could not repair, and those exceptions are carried into the post-scan missing map rather than silently forgotten.

### P — scan cancellation/restart does not present the same retirement frontier as completed scanning

In `dsl_scan.c`, cancellation calls:

```text
dsl_scan_done(scn, B_FALSE, tx)
```

and scan restart logic likewise closes the prior scan with `complete = B_FALSE` before setting up a new scan.

By contrast, when scan issuing is complete, `dsl_scan_done(scn, B_TRUE, tx)` is invoked.

Inside `dsl_scan_done()`, the complete path, when a pool checkpoint does not block the update, calls:

```text
vdev_dtl_reassess(root,
    current_txg,
    scn_max_txg,
    scrub_done = B_TRUE,
    rebuild_done = B_FALSE)
```

whereas the non-complete branch calls `vdev_dtl_reassess()` with `scrub_txg = 0`.

Thus cancellation/restart and successful completion are not represented by the same DTL-retirement input.

### P — `vdev_dtl_should_excise()` explicitly rejects several leaves before retirement

For leaf vdevs, `vdev_dtl_should_excise()` first rejects a device whose state is below `VDEV_STATE_DEGRADED` and rejects a device with `vdev_resilver_deferred` set.

If `DTL_MISSING` is already empty, the function can return true because there is no missing range to protect.

The more important cases concern non-empty missing state and whether the relevant maintenance operation actually covered the leaf's debt.

### P — traditional healing resilver excision is tied to the scan's txg coverage

For the non-sequential-rebuild path, source comments say that when a resilver begins, the scan's `scn_max_txg` is assigned to the highest transaction group that exists in all DTLs. A device whose maximum DTL transaction group is not part of that scan is not eligible for excision.

The implementation checks:

```text
vdev_dtl_max(vd) <= scn->scn_phys.scn_max_txg
```

before returning true for this branch, with assertions relating `scn_min_txg`, the leaf's `vdev_resilver_txg`, and `scn_max_txg`.

A `vdev_resilver_txg == 0` path is explicitly treated as `resilver not initiated by attach` and may return true without that attach-specific coverage test.

The bounded implication is not “every completed scan clears every old DTL.” It is that the implementation preserves a relation between the maintenance operation's txg frontier and the leaf repair history that may be retired.

### P — sequential rebuild has its own completion and coverage qualification

For `rebuild_done`, `vdev_dtl_should_excise()` uses the top-level vdev rebuild state.

A rebuild not initiated by attach (`vdev_rebuild_txg == 0`) is treated separately. For the attach-driven case, the function requires the recorded rebuild state to be `VDEV_REBUILD_COMPLETE` and the leaf's maximum DTL transaction group to be no greater than the rebuild's `vrp_max_txg` before returning true.

The assertions further bind the rebuild's minimum txg, the leaf's `vdev_rebuild_txg`, and the maximum txg.

This is a different implementation path from healing resilvering; identical words such as `resilver` in operator language should not erase that distinction.

### P — the sequential-rebuild completion path also checks that the rebuild was clean enough to consider excision

`vdev_rebuild_complete_sync()` records `VDEV_REBUILD_COMPLETE`, persists the rebuild physical state, and calls:

```text
vdev_dtl_reassess(vd,
    current_txg,
    vrp_max_txg,
    scrub_done = B_TRUE,
    rebuild_done = B_TRUE)
```

Within the leaf portion of `vdev_dtl_reassess()`, however, `check_excise` is set for a completed rebuild only when the rebuild configuration is present and `vrp_errors == 0`.

So even a rebuild reaching its completion routine is not, by itself, the entire DTL-retirement predicate.

### P — ordinary scrub/resilver completion is likewise not equivalent to “all repair evidence may vanish”

For the non-rebuild branch, `vdev_dtl_reassess()` determines whether excision should be considered from the scan/scrub state, including the scan error state. It then requires all of the following before entering the missing-map excision transform:

```text
scrub_txg != 0
AND check_excise
AND vdev_dtl_should_excise(vd, rebuild_done)
```

The maintenance completion signal is therefore only one input to the retirement decision.

### P — retirement is bounded by a txg frontier, not implemented as “clear the map”

When the leaf is eligible, `vdev_dtl_reassess()` does not simply vacate `DTL_MISSING`.

It constructs a reference tree from the existing missing map, subtracts the interval:

```text
[0, scrub_txg)
```

and then overlays `DTL_SCRUB` with a positive reference contribution before generating the new `DTL_MISSING` map.

The source comment explains the transform directly: the beginning of `DTL_MISSING` is excised through a `-1` segment over `[0, scrub_txg)`, while `DTL_SCRUB` is added with weight `2` so entries representing scrub failures remain positive in the resulting missing map.

Thus:

```text
maintenance frontier reached
    -> eligible old missing interval can be removed

but

scan-discovered unrepaired interval
    -> survives in the regenerated missing map
```

### P — scrub-exception state is cleared only after it has served the reassessment

After the new `DTL_MISSING` relation has been computed, the implementation reconstructs `DTL_PARTIAL` from `DTL_MISSING`. When `scrub_done` is true, it then vacates `DTL_SCRUB`.

This ordering matters: `DTL_SCRUB` can be transient as an independent runtime class while still affecting the durable/continuing `DTL_MISSING` result before it disappears.

A control structure can therefore be safely forgotten only after its information has been folded into the state that must continue to constrain repair.

### P — attach/rebuild markers are reset only after the relevant DTL classes become empty

The leaf reassessment code contains another later boundary. If `txg != 0` and both `DTL_MISSING` and `DTL_OUTAGE` are empty, the implementation resets either `vdev_rebuild_txg` or `vdev_resilver_txg` and dirties the top-level configuration so that the change is persisted.

This supplies a second retirement relation:

```text
maintenance operation finished
    !=
repair-start marker immediately disposable

missing/outage debt empty
    -> marker may be reset and persisted
```

The source therefore has multiple retirement layers rather than one global `repair complete` bit.

## Engineering reconstruction

The implementation supports the following bounded reconstruction:

```text
retained DTL_MISSING repair debt
    + maintenance operation begins
    ->
operation gets a bounded txg coverage frontier
    ->
scan / rebuild performs work
    ->
completion path reached
    ->
check clean-enough / eligible-for-excision conditions
    ->
check that this leaf's missing history lies within the covered frontier
    ->
subtract eligible pre-frontier missing interval
    ->
reinsert scan-discovered unrepaired exceptions from DTL_SCRUB
    ->
recompute dependent DTL views
    ->
if missing/outage debt is now empty, retire attach/rebuild marker
```

Project term:

> **qualified repair-debt retirement** — removing maintenance-control history only after the implementation has evidence that the relevant repair scope was covered, while preserving exceptions that still encode unresolved debt.

This is an engineering reconstruction, not OpenZFS historical vocabulary.

## Retained-state decomposition

For this slice, at least these states should remain separate:

```text
payload / block data
    !=
DTL_MISSING repair-debt intervals
    !=
DTL_SCRUB scan-discovered unrepaired intervals
    !=
DTL_PARTIAL derived partial-replication state
    !=
DTL_OUTAGE current unreadability state
    !=
scan / rebuild progress
    !=
scan / rebuild completion state
    !=
scan/rebuild txg coverage frontier
    !=
vdev_resilver_txg / vdev_rebuild_txg marker
    !=
post-repair persisted configuration
```

Several useful negative controls follow immediately:

> **maintenance activity ended ≠ maintenance debt retired.**

> **maintenance traversal completed ≠ every targeted item repaired.**

> **repair debt narrowed ≠ all repair debt cleared.**

> **transient exception map removed ≠ exception information forgotten.**

> **repair marker reset ≠ payload securely erased or history globally forgotten.**

## Failure and edge boundaries

### Interrupted scan

A canceled or restarting scan reaches `dsl_scan_done(..., B_FALSE, ...)` and does not present the same nonzero `scrub_txg` retirement frontier as the completed path.

Therefore an interrupted traversal must not be paraphrased as a completed repair whose only remaining task is metadata cleanup.

### Deferred resilver

`vdev_resilver_deferred` causes `vdev_dtl_should_excise()` to reject excision. The presence of deferred work is therefore a direct counterexample to treating a generic completion event elsewhere in the pool as sufficient to retire this leaf's history.

### Device not covered for the required interval

A leaf whose DTL maximum lies outside the relevant scan/rebuild frontier is not eligible under the attach-driven coverage checks. This protects against using one maintenance pass as evidence for repair work it did not cover.

### Rebuild errors

The leaf reassessment path requires zero recorded rebuild errors before setting the rebuild branch's `check_excise` flag. A completion-state transition and an error-free retirement qualification are therefore distinct.

### Scan-discovered repair failures

`DTL_SCRUB` exists precisely to preserve intervals that the last scrub could not repair. Its overlay into the new `DTL_MISSING` map prevents the “frontier subtraction” step from laundering those exceptions into apparent health.

## Functional comparison

### Case 48 — Cassandra incremental repair session cleanup

Case 48 shows that a repair session cannot safely be deleted merely because normal workflow/age conditions suggest cleanup if SSTables still reference that session. Case 100 supplies a different implementation of the same **functional** boundary:

```text
workflow completion
    !=
control-state retirement authority
```

Cassandra uses session/SSTable reference state; OpenZFS uses DTL classes, txg frontiers, scan/rebuild status, and exception maps. No shared implementation or genealogy is asserted.

### Case 153 — Ceph snaptrim

Case 153 distinguishes active trim execution from a still-outstanding reclamation obligation, especially under `snaptrim_error`. Case 100 similarly distinguishes completion/termination of an execution path from retirement of the maintenance debt it was intended to discharge. Again, this is a functional analogy only.

### Case 141 — PostgreSQL replication slots

Case 141 separates a retained continuation/retention-control object from the live process using it. Case 100 adds a different lesson: even when maintenance work has occurred, retiring its control evidence requires a separate bounded predicate. This is not a claim of technical descent.

## Philosophical / media-theoretical limit

`I` — This source slice makes forgetting itself conditional. The system is permitted to forget a repair-relevant interval only after enough other state demonstrates that the corresponding obligation has been discharged or transformed into a narrower surviving exception.

`I` — The important object is not “the past” in general. What survives is precisely the part of the past that still constrains future repair. Once a covered portion no longer constrains repair, it can be subtracted; an unrepaired exception remains because it still has operational force.

`I` — This is not evidence that OpenZFS authors formulated a philosophy of memory, debt, or forgetting. Those are project-level interpretations disciplined by the implementation.

## Explicit non-claims

This packet does **not** establish:

1. that OpenZFS 2.1.11 introduced these retirement semantics;
2. that Solaris 2005–2007 used the same `vdev_dtl_should_excise()` implementation;
3. that every modern OpenZFS release has identical predicates or DTL classes;
4. that `scan complete` means every read or repair succeeded;
5. that `VDEV_REBUILD_COMPLETE` alone authorizes DTL deletion;
6. that zero `vrp_errors` proves all payload is globally correct;
7. that a txg frontier is a checksum/integrity certificate;
8. that `DTL_SCRUB` is independently durable across every restart point;
9. that clearing `DTL_SCRUB` loses its information when that information has already been folded into `DTL_MISSING`;
10. that an empty `DTL_MISSING` proves absence of latent corruption;
11. that an empty `DTL_OUTAGE` proves every future read will succeed;
12. that resetting `vdev_resilver_txg` / `vdev_rebuild_txg` means all maintenance history has been erased from every log or history facility;
13. that DTL retirement is secure data erasure;
14. that DTL retirement and free-space reclamation are the same operation;
15. that a completed sequential rebuild has already performed the later checksum-verification scrub described by `vdev_rebuild.c`;
16. that traditional healing resilver and sequential rebuild have identical verification semantics;
17. that source-level chronology establishes invention priority.

## Claim ledger

| Claim | Label | Evidence | Limit |
| --- | --- | --- | --- |
| OpenZFS 2.1.11 distinguishes `DTL_MISSING`, `DTL_PARTIAL`, `DTL_SCRUB`, and `DTL_OUTAGE` | `P` | `vdev.c` source comment | version-specific implementation vocabulary |
| canceled/restarting scan uses `dsl_scan_done(..., B_FALSE, ...)`, while completed scan uses `B_TRUE` | `P` | `dsl_scan.c` | scan-control path only |
| completed scan passes a nonzero scan frontier into `vdev_dtl_reassess()`; incomplete path passes zero | `P` | `dsl_scan.c` | does not itself prove repair success |
| deferred / insufficiently covered leaf can be rejected by `vdev_dtl_should_excise()` | `P` | `vdev.c` | exact predicate is implementation-specific |
| attach-driven healing resilver uses the scan's txg coverage to qualify leaf DTL excision | `P` | `vdev.c` | not a generic distributed-repair rule |
| sequential rebuild has a distinct complete-state / txg-coverage qualification | `P` | `vdev.c`, `vdev_rebuild.c` | rebuild-specific |
| recorded rebuild errors prevent the rebuild branch from enabling excision consideration | `P` | `vdev.c` | zero errors is not a universal correctness proof |
| eligible DTL retirement subtracts `[0, scrub_txg)` rather than unconditionally clearing `DTL_MISSING` | `P` | `vdev.c` | bounded to this implementation |
| `DTL_SCRUB` exceptions are overlaid so unrepaired intervals remain in the resulting missing map | `P` | `vdev.c` | does not prove every error source |
| after reassessment, `DTL_SCRUB` can be vacated while its surviving exception information remains represented by `DTL_MISSING` | `P/E` | `vdev.c` ordering | engineering statement about information flow |
| rebuild/resilver marker reset waits for empty `DTL_MISSING` and `DTL_OUTAGE`, then dirties config | `P` | `vdev.c` | not all possible repair/history state |
| completed maintenance always authorizes forgetting all repair debt | `X` | source predicates and exception overlay | rejected |
| DTL retirement proves payload integrity | `X` | DTL/scrub semantic separation | rejected |
| DTL retirement is secure erasure | `X` | mechanism boundary | rejected |

## Source ledger

### OpenZFS 2.1.11 `module/zfs/vdev.c`

<https://github.com/openzfs/zfs/blob/zfs-2.1.11/module/zfs/vdev.c>

Relevant regions:

- DTL class explanatory comment (`DTL_MISSING`, `DTL_PARTIAL`, `DTL_SCRUB`, `DTL_OUTAGE`);
- `vdev_dtl_should_excise()`;
- `vdev_dtl_reassess()`;
- leaf DTL recomputation and marker-reset logic.

### OpenZFS 2.1.11 `module/zfs/dsl_scan.c`

<https://github.com/openzfs/zfs/blob/zfs-2.1.11/module/zfs/dsl_scan.c>

Relevant regions:

- `dsl_scan_done()`;
- cancel/restart calls with `complete = B_FALSE`;
- completed issuing path calling `dsl_scan_done(..., B_TRUE, ...)`;
- `vdev_dtl_reassess()` calls with completed versus zero `scrub_txg` frontier.

### OpenZFS 2.1.11 `module/zfs/vdev_rebuild.c`

<https://github.com/openzfs/zfs/blob/zfs-2.1.11/module/zfs/vdev_rebuild.c>

Relevant regions:

- sequential-reconstruction design comment;
- `vdev_rebuild_complete_sync()`;
- persisted `VDEV_REBUILD_COMPLETE` state;
- call to `vdev_dtl_reassess(..., vrp_max_txg, B_TRUE, B_TRUE)`;
- subsequent optional checksum-verification scrub setup.

## Remaining evidence debt

This packet closes the **OpenZFS 2.1.11 implementation slice** for qualified DTL retirement. It does not close the broader historical/version question. Remaining useful follow-ons are:

- identify the commit/release in which the current-style excision predicates and `DTL_SCRUB` overlay entered the lineage;
- compare Solaris/illumos/OpenZFS revisions and document semantic changes rather than assuming continuity;
- run a controlled test with an interrupted resilver and verify that repair debt remains after restart;
- run a controlled test that injects a repair error during scrub/resilver and observe the resulting DTL classes;
- trace sequential rebuild → automatic scrub across a real pool and distinguish restored redundancy from later checksum-qualified confidence;
- test marker/config persistence across export/import after DTL state becomes empty.

Those belong to later slices; they are not inferred from source inspection alone.
