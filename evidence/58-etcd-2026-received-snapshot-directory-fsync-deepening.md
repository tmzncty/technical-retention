# etcd received-snapshot directory durability: file sync, rename, directory sync, and later WAL admission (2026)

**Canonical case:** [`58 — Raft Snapshotting: Committed State Beyond the Replicated-Log Prefix`](../cases/58-raft-snapshot-log-compaction.md)  
**Status:** `bounded deepening complete`  
**Evidence range:** etcd `v3.5.15` source as the pre-fix comparison; upstream etcd PR #22314 / commit `cf31e1f6033f0752f0c55d2456a0771be0c5ba80`, merged to `main` on 3 September 2026; verified backports to `release-3.7` and `release-3.6` on 9–10 September 2026; Linux `fsync(2)` documentation for the file-vs-directory durability contract.

This slice closes one narrow item explicitly left open by Case 58:

> **A received snapshot database can have its file contents synced and be renamed into its final pathname while the durability of the containing directory entry is still a separate persistence obligation.**

The result is deliberately smaller than “etcd snapshot durability is solved.” It concerns one local publication seam on the **received snapshot database** path. It does not replace the 2014 Raft protocol record, does not prove hardware-level sudden-power-loss behavior for every filesystem/device stack, and does not claim that a process `SIGKILL` reproduces loss of an unsynced directory entry.

---

## 1. Why this slice matters

The existing Case 58 deepening already separates several stages that the word `snapshot` can hide:

```text
snapshot candidate / Raft state
    -> local snapshot file
    -> WAL snapshot marker
    -> restart admission
    -> in-memory application
    -> server/application publication
    -> later release of older recovery material
```

For etcd `v3.5.15`, the canonical case already grounds a useful boundary:

```text
snapshot file exists
    !=
matching WAL restart marker exists
    !=
restart loader admits that snapshot
```

The 2026 change exposes one still-lower layer inside the first term. Before the fix, `SaveDBFrom` did this for an incoming database snapshot:

```text
write temporary file
    -> fsync temporary file
    -> close file
    -> rename temporary file to <snapshot-index>.snap.db
    -> return success
```

The code did **not** explicitly fsync the containing snapshot directory after the rename.

The fix adds:

```text
write temporary file
    -> fsync temporary file
    -> close file
    -> rename temporary file to <snapshot-index>.snap.db
    -> fsync containing snapshot directory
    -> only then return success
    -> only then allow receiver to process the Raft message
```

That change gives Case 58 a more precise persistence decomposition:

```text
snapshot file-content persistence
    !=
final pathname / directory-entry persistence
    !=
later WAL snapshot-marker persistence
    !=
restart-time snapshot admission
```

The difference is not philosophical wordplay. It appears in an upstream etcd durability fix, code comments, error propagation, unit tests, failpoints, E2E tests, and explicit test-scope limitations.

---

## 2. Source set and custody

### S1 — etcd v3.5.15 pre-fix `SaveDBFrom`

Source:

- <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/api/snap/db.go>

The exact tagged source shows that `SaveDBFrom`:

1. creates a temporary file in the snapshot directory;
2. copies the received bytes into it;
3. calls `fileutil.Fsync(f)` on that file;
4. closes it;
5. if the final snapshot pathname already exists, removes the temporary file and returns success;
6. otherwise calls `os.Rename(f.Name(), fn)`;
7. logs success and returns.

There is no explicit directory `fsync` in this function in `v3.5.15`.

The pre-fix comment says the function “guarantees the save operation is atomic.” This historical wording must not be silently upgraded into a stronger durability guarantee than the implementation actually establishes.

### S2 — etcd v3.5.15 received-snapshot ordering

Source:

- <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/api/rafthttp/http.go>

The snapshot HTTP handler first calls:

```text
h.snapshotter.SaveDBFrom(...)
```

If it returns an error, the handler returns an HTTP error and does not continue to normal Raft-message processing. Only after `SaveDBFrom` succeeds does it call:

```text
h.r.Process(context.TODO(), m)
```

This is important because the later Raft processing path can eventually lead to the WAL-side snapshot record that the existing Case 58 implementation deepening already analyzes.

The 2026 fix therefore strengthens an already meaningful ordering seam rather than adding an unrelated flush.

### S3 — upstream 2026 fix commit and PR

Primary source:

- commit `cf31e1f6033f0752f0c55d2456a0771be0c5ba80`, dated 25 August 2026: <https://github.com/etcd-io/etcd/commit/cf31e1f6033f0752f0c55d2456a0771be0c5ba80>
- PR #22314, created 20 August 2026 and merged into `main` on 3 September 2026: <https://github.com/etcd-io/etcd/pull/22314>
- merge commit `e9e56564d6f13af87747cdb785bc1832791090b4`: <https://github.com/etcd-io/etcd/commit/e9e56564d6f13af87747cdb785bc1832791090b4>

The PR/commit message states the defect boundary directly:

- `SaveDBFrom` synced the received snapshot database **before** renaming it;
- it did **not** sync the containing directory;
- Linux `fsync(2)` requires a separate directory sync to ensure the directory entry is persisted;
- the receiver calls `SaveDBFrom` before processing the Raft message;
- that later processing can eventually sync the WAL snapshot record;
- therefore the fix syncs the snapshot directory before allowing processing to continue.

This is unusually strong source evidence because the maintainers themselves formulate the persistence-order relation the retention analysis needs.

### S4 — current upstream implementation after the fix

Source:

- <https://github.com/etcd-io/etcd/blob/main/server/etcdserver/api/snap/db.go>

The current function now states that, before a successful return, it syncs both the file and containing directory so the rename is durable **on storage that honors fsync**. It adds a directory-sync call after rename and also on the already-existing-final-file path.

The latter is important. The code comment explains that an earlier `SaveDBFrom` may have renamed the final file and crashed before syncing the directory. A retry that merely sees the final pathname cannot treat that observation alone as proof that the prior rename was durably recorded. The retry therefore syncs the directory again before returning success.

### S5 — Linux `fsync(2)` contract

Authoritative manual-page source:

- <https://man7.org/linux/man-pages/man2/fsync.2.html>

The Linux manual explicitly states that `fsync()` on a file does not necessarily ensure that the entry in the containing directory has reached disk; an explicit `fsync()` on a file descriptor for the directory is also needed.

This source supports the operating-system contract relied upon by the etcd fix. It does not by itself prove every storage device truthfully honors flush commands, nor does it replace filesystem/device sudden-power-loss validation.

### S6 — release-branch backports

Verified upstream PRs:

- `release-3.7`: PR #22378, created 3 September 2026 and merged 9 September 2026: <https://github.com/etcd-io/etcd/pull/22378>
- `release-3.6`: PR #22401, created 8 September 2026 and merged 10 September 2026: <https://github.com/etcd-io/etcd/pull/22401>

These establish that the fix was not left only on `main`; it was deliberately carried into the then-maintained 3.7 and 3.6 release lines. This slice makes no claim about a 3.5 backport unless separately sourced.

---

## 3. Historical record

### H/P — v3.5.15 synced the received snapshot file before rename

The tagged `v3.5.15` implementation writes the incoming database snapshot to a temporary file and calls `fileutil.Fsync(f)` before closing the file.

The bounded historical statement is therefore:

> **The pre-fix implementation did contain an explicit file-content synchronization boundary before publication under the final snapshot pathname.**

The 2026 issue is not accurately described as “etcd forgot to fsync the snapshot.” It forgot a **different synchronization object**: the containing directory after namespace publication.

### H/P — v3.5.15 then renamed without explicitly syncing the directory

After file sync/close, the function calls `os.Rename` into the final `<index>.snap.db` path and returns success. No directory `fsync` appears in this function.

Thus the exact pre-fix sequence is:

```text
snapshot bytes copied
    -> file fsync succeeds
    -> file closed
    -> final pathname created by rename
    -> no explicit directory fsync here
    -> SaveDBFrom success
```

This is a source-level fact. The stronger proposition “a power loss definitely loses the pathname on filesystem X” would require a concrete filesystem/device fault experiment and is **not** asserted here.

### H/P — the receiver processes the Raft message only after snapshot-file save success

The v3.5.15 receiver directly orders `SaveDBFrom` before `h.r.Process`.

Therefore a failure reported by `SaveDBFrom` already acts as an admission barrier: if local snapshot publication fails at that stage, the receiver does not simply continue the normal Raft-message path.

### H/P — upstream explicitly identified the directory-durability gap in 2026

PR #22314 and commit `cf31e1f...` explicitly say that file sync did not necessarily persist the containing directory entry and that the directory must be synced.

This is not a project inference retrofitted onto old code. It is the defect model recorded by the etcd maintainers in the fix itself.

### H/P — the fix adds directory sync after rename

The post-fix `SaveDBFrom` calls a helper that:

```text
open snapshot directory
    -> fileutil.Fsync(directory fd)
```

The function performs that step after the final rename and before successful completion.

The code comment states the intended relation:

```text
file already synced
    + directory synced after rename
    -> rename considered durable on storage honoring fsync
```

### H/P — directory-sync errors now stop snapshot receive before Raft processing

The new code returns the directory-sync error rather than logging and proceeding.

Because the HTTP receiver already treats a `SaveDBFrom` error as failure and returns before `h.r.Process`, the new sync is placed on the admission path, not as a best-effort telemetry event after Raft processing.

The 2026 commit message states the intended ordering explicitly: the snapshot database publication should be established before later processing can persist a WAL snapshot record.

### H/P — the already-existing final file path is also re-synced

The post-fix implementation does not say:

```text
final pathname exists
    -> therefore prior rename must already be durable
```

Instead, when `fn` already exists, it deletes the new temporary file and syncs the directory before returning success.

Its comment gives the reason: a previous attempt may have renamed the file and crashed before the directory sync.

This makes the restart/retry semantics especially useful for technical retention:

> **current namespace visibility is not treated as retrospective proof that the namespace transition previously crossed the intended durability boundary.**

### H/P — unit tests cover both publication paths and error propagation

The fix adds direct unit coverage for:

- a newly published snapshot pathname;
- an already-existing snapshot pathname;
- invocation of directory sync in both paths;
- propagation of directory-sync failure.

The tests inject the sync function rather than claiming to emulate actual storage-device power loss.

### H/P — E2E tests deliberately limit what they claim

The added E2E test file contains an explicit methodological warning: the tests cover error/recovery paths around directory sync, but **do not simulate loss of an unsynced directory entry**; that behavior is attributed to the operating-system `fsync` contract.

The crash-window test pauses after rename and before directory sync, kills the member, restarts it, and verifies later snapshot recovery. Its own comment states that `SIGKILL` does **not** test directory-entry durability.

This explicit negative claim is important enough to retain verbatim in substance:

```text
process crash-window control-flow test
    !=
sudden-power-loss proof of directory-entry persistence
```

### H/P — mainline fix was backported to release-3.7 and release-3.6

PR #22314 merged to `main` on 3 September 2026. Automated/manual backport PRs then merged the fix into:

- `release-3.7` on 9 September 2026;
- `release-3.6` on 10 September 2026.

This is release-maintenance evidence, not proof that every deployed etcd binary was upgraded.

---

## 4. Engineering reconstruction

### E — file-content durability and pathname durability are different retained relations

A snapshot database is not operationally useful to restart code merely because its data blocks have crossed a file-level synchronization boundary. The system also needs a stable relation that lets later code **find those bytes under the expected name in the expected directory**.

For this bounded path:

```text
snapshot byte content
    !=
filesystem name -> file relation
```

Both participate in future recoverability.

This does not mean filenames are “payload.” It means naming/namespace state can be retention infrastructure for locating payload after failure.

### E — visibility now is not identical to durability after crash

After `rename`, a running process can observe the final pathname. The 2026 retry-path comment nevertheless treats a prior rename followed by crash-before-directory-sync as a reason to sync the directory again.

Therefore:

```text
currently observable pathname
    !=
proven persistence of pathname across the intended crash model
```

The distinction is specific to the documented filesystem durability contract. It should not be generalized into “visible writes are never durable.”

### E — rename atomicity and rename durability are different questions

The pre-fix source called `SaveDBFrom` atomic. The 2026 change does not simply delete the idea of atomic publication; it adds the missing durability step for the directory entry.

The safe project distinction is:

```text
namespace transition appears atomically published
    !=
namespace transition is durably recorded across crash
```

This slice does not attempt a complete cross-filesystem proof of `rename(2)` atomicity semantics. It only observes that the upstream fix itself treats directory synchronization as a separate requirement after rename.

### E — persistence ordering can cross multiple artifacts

The fix makes one local ordering intention more explicit:

```text
received snap.db bytes synced
    -> final directory entry synced
    -> SaveDBFrom succeeds
    -> Raft message may be processed
    -> later WAL snapshot record may be synced
```

This matters because recovery authority is distributed across more than one artifact. A system can require a partial order among durable relations, not merely “all the files eventually exist.”

### E — one durable artifact can be a prerequisite for authorizing another

The 2026 code uses directory-sync success as a gate before proceeding to the Raft path that can later produce a WAL snapshot marker.

Thus:

```text
snapshot database durability evidence
    -> permits later control-record progression
```

The relation is not symmetric. The snapshot database is the material state that the marker will later help identify/admit; allowing marker progression while the pathname publication remains unproven could create a mismatched recovery representation.

The exact consequences of every possible crash interleaving still depend on the restart code and lower storage stack. The case therefore stops at the source-grounded ordering intent.

### E — “already exists” is a recovery observation, not a complete durability certificate

The existing-file retry path is especially revealing:

```text
final path observed
    -> prior operation probably reached rename
    !=
prior directory update proven durable
    -> sync directory now
    -> then report success
```

A later observation can help reconstruction, yet the software still performs a maintenance action to re-establish the desired persistence boundary.

### E — error propagation is part of the retention mechanism

The new directory sync would be weaker if failure merely produced a warning and normal Raft processing continued. Instead, the error causes `SaveDBFrom` to fail, and the receiver stops before `Process`.

So the retention mechanism includes not only flushing but also **admission control on failed durability work**:

```text
persistence operation requested
    !=
persistence operation succeeded
    !=
later state transition authorized
```

### E — retry can repair incomplete publication without claiming prior success

The E2E error test injects a directory-sync failure, observes snapshot receive failure, removes the failure, and verifies later recovery. This demonstrates a control path in which failure to establish the local persistence relation is not silently converted into success; the operation can be retried and the member can catch up later.

The test does not prove how raw disk state behaves under abrupt power loss.

---

## 5. Controlled functional comparisons

### A — relation to earlier Case 58 etcd v3.5.15 snapshot/WAL evidence

The prior implementation deepening established:

```text
snapshot file
    !=
WAL snapshot record
    !=
restart-admitted snapshot
```

The 2026 fix inserts another layer before the first boundary:

```text
file contents synced
    !=
final directory entry synced
    !=
WAL snapshot record synced
    !=
restart admission succeeds
```

This is the same implementation family at different times, but the 2026 fix must not be projected backward as behavior already present in `v3.5.15`.

### A — relation to Case 56 Kafka checkpoint coverage

Case 56 shows that a checkpoint file can be successfully rewritten while semantically omitting a still-relevant high-watermark relation.

The present etcd slice shows a different failure dimension:

```text
Kafka Case 56
    representation file can be structurally successful
    while semantic coverage is incomplete

etcd Case 58 / 2026
    snapshot bytes can be file-synced
    while namespace-publication durability is not yet closed
```

Therefore:

```text
semantic completeness
    !=
filesystem publication durability
```

This is a functional comparison only. No Kafka→etcd genealogy or shared implementation is claimed.

### A — relation to mapped-Flash recovery evidence

Case 04 distinguishes surviving payload pages from the retained/reconstructable mapping state needed to resolve logical identities after power loss. The present case similarly shows that surviving bytes and the relation needed to locate/admit them can have different persistence paths.

The analogy stops there. Flash translation metadata and POSIX/Linux directory entries are different mechanisms, authorities, failure models, and historical lineages.

### A — relation to Bigtable re-observation

Case 57 shows that an observer can reconstruct current control knowledge from authoritative metadata even if a notification was lost. In this etcd slice, the question is lower-level: whether the local namespace relation needed to locate a received recovery artifact crossed the intended persistence boundary.

Thus:

```text
re-observable authoritative relation
    !=
durable local namespace publication
```

The two cases should not be merged under a generic “metadata survives” label.

---

## 6. Philosophical / media-theoretical interpretation

### I — retention can depend on preserving a relation of locatability

The exact technical fact is narrow: the received snapshot's byte contents and the directory entry that makes those contents findable under the intended final pathname cross separate synchronization boundaries.

That supports a bounded conceptual statement:

> **For a technical state to remain available, retaining its material content may be insufficient if the relation by which later machinery can locate and admit that content is not also retained.**

This is not a claim that a pathname is philosophically identical to memory, identity, or meaning. It is an engineering-grounded example of availability depending on retained relations around an artifact.

### I — “the object survived” can be underspecified

At too high a level one might say “the snapshot was saved.” The fix forces a more exact question:

```text
Which part was saved?

bytes?
final name?
directory update?
WAL marker?
restart admission relation?
```

The philosophical value of the case is methodological: persistence claims need an explicit **object and boundary**.

### I — successful continuation may require refusing premature success

The added error propagation shows a negative form of retention work. The system preserves recoverability partly by declining to advance when one persistence precondition cannot be established.

This does not turn every error return into a philosophy of memory. The concept is useful here only because the source establishes a concrete causal ordering between snapshot publication and later Raft/WAL progression.

---

## 7. Explicit non-claims

This evidence **does not claim** any of the following:

1. etcd `v3.5.15` never persisted received snapshot pathnames in practice.
2. every crash between rename and directory fsync necessarily loses the directory entry.
3. one specific filesystem or controller is proven to lose the entry in that window.
4. `SIGKILL` is equivalent to sudden power loss.
5. the added E2E test proves directory-entry durability under power failure.
6. the upstream tests claim such a proof; they explicitly reject it.
7. the pre-fix code omitted file `fsync`; it did call `fileutil.Fsync(f)` before rename.
8. the fix proves every storage device honestly honors `fsync`/flush commands.
9. Linux `fsync(2)` documentation is a hardware fault-injection result.
10. `rename` visibility and directory durability are the same property.
11. `rename` atomicity and crash durability are the same property.
12. the 2026 change proves all possible filesystem rename semantics.
13. a directory entry is the snapshot payload.
14. a pathname alone is sufficient for restart authority.
15. directory fsync alone is sufficient for restart authority.
16. a WAL snapshot marker alone is sufficient for restart authority.
17. successful `SaveDBFrom` means application state has already been published.
18. local `SaveDBFrom` is identical to the Raft `InstallSnapshot` protocol abstraction.
19. the 2026 fix changes Raft's 2014 consensus safety rules.
20. this defect is evidence that the Raft paper itself specified an incorrect persistence API.
21. every etcd snapshot path before 2026 used exactly the same local code.
22. every deployed etcd release received the fix immediately after mainline merge.
23. this slice proves a `release-3.5` backport.
24. `release-3.6` and `release-3.7` backports prove all downstream distributions incorporated the patch.
25. observation that a final file exists after restart proves the prior rename was durably committed before the crash.
26. directory fsync establishes semantic correctness of snapshot contents.
27. a valid snapshot file establishes that it matches the current/committed Raft boundary.
28. the fix makes snapshot-file and WAL-marker updates one atomic transaction.
29. a persistence ordering between two artifacts means they share one failure domain.
30. “durable” here means immutable, permanent, archival, or secure against deletion.
31. replacing or releasing older snapshots means secure erasure of their physical remnants.
32. a successful retry proves the first attempt crossed the same durability frontier.
33. file-content retention and namespace retention are historically or physically the same mechanism.
34. this Linux/filesystem case is a direct genealogy of Flash mapping or database catalog metadata.
35. the project term `locatability relation` is etcd maintainer vocabulary.

---

## 8. Claim ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| etcd v3.5.15 `SaveDBFrom` fsyncs the temporary received snapshot file before rename | H/P | tagged `db.go` | supported |
| v3.5.15 `SaveDBFrom` then renames to the final `.snap.db` pathname without an explicit directory fsync in that function | H/P | tagged `db.go` | supported |
| v3.5.15 snapshot HTTP receive calls `SaveDBFrom` before `h.r.Process` | H/P | tagged `rafthttp/http.go` | supported |
| upstream PR #22314 identified the missing containing-directory sync as a durability gap | H/P | PR body + fix commit | supported |
| Linux `fsync(2)` documents that file fsync does not necessarily persist the containing directory entry | H/P | Linux man-pages `fsync(2)` | supported |
| the 2026 fix syncs the snapshot directory after rename before `SaveDBFrom` succeeds | H/P | fix commit/current `db.go` | supported |
| the existing-final-file retry path also syncs the directory before success | H/P | fix commit/current `db.go` | supported |
| directory-sync failure propagates out of `SaveDBFrom` | H/P | fix commit/tests | supported |
| receiver failure therefore stops normal Raft-message processing at this point | H/P/E | `SaveDBFrom` error path + receiver ordering | supported |
| the added unit test covers both new and existing final-file paths and sync-error propagation | H/P | fix commit | supported |
| the E2E tests explicitly say they do not simulate loss of an unsynced directory entry | H/P | fix commit test comment | supported |
| the crash-window E2E test explicitly says SIGKILL does not test directory-entry durability | H/P | fix commit test comment | supported |
| PR #22314 merged to main on 3 September 2026 | H/P | GitHub PR metadata | supported |
| fix was backported to release-3.7 on 9 September 2026 | H/P | PR #22378 | supported |
| fix was backported to release-3.6 on 10 September 2026 | H/P | PR #22401 | supported |
| file-content persistence and final-path namespace persistence are separate relations in this code path | E | pre/post-fix comparison + Linux contract | supported |
| currently visible final pathname proves prior directory persistence across crash | X | retry path explicitly re-syncs directory | rejected |
| file fsync alone proves final pathname durability | X | upstream fix + Linux contract | rejected |
| SIGKILL test proves sudden-power-loss directory durability | X | test explicitly rejects this claim | rejected |
| directory fsync proves snapshot semantic/currentness correctness | X | no such evidence | rejected |
| snapshot DB + WAL marker form one atomic local transaction | X | existing Case 58 evidence + separate persistence boundaries | rejected |
| mainline merge proves every release/deployment contains the fix | X | backports are branch-specific; deployment evidence absent | rejected |

---

## 9. What this changes in Case 58

Before this slice, the exact etcd implementation comparison could safely say:

```text
stable snapshot file
    !=
WAL snapshot marker
    !=
restart-admitted snapshot
```

After the 2026 fix record, the first term needs decomposition:

```text
received snapshot bytes copied
    -> file fsync
    -> rename to final pathname
    -> directory fsync
    -> received snapshot publication accepted locally
    -> Raft message may advance
    -> WAL snapshot marker may later sync
    -> restart code may later admit the matching snapshot
```

The resulting retention controls are:

1. **file-content persistence ≠ directory-entry persistence**;
2. **rename visibility ≠ rename durability**;
3. **namespace atomicity ≠ crash durability**;
4. **final pathname exists ≠ prior publication is retrospectively proven durable**;
5. **snapshot publication durability ≠ WAL marker durability**;
6. **WAL marker durability ≠ restart admission**;
7. **persistence operation attempted ≠ persistence operation succeeded ≠ later progression authorized**;
8. **process-crash control-flow test ≠ sudden-power-loss storage validation**.

This closes the previously explicit Case-58 debt around the **2026 received-snapshot directory-fsync fix and its release/backport chronology** at a source level. It does **not** close the separate hardware/filesystem fault-injection debt.

---

## 10. Remaining evidence debt

Useful next work is now narrower:

- perform or locate a true sudden-power-loss / filesystem-level experiment for the rename-before-directory-sync window rather than treating `SIGKILL` as equivalent;
- test concrete ext4/XFS/btrfs and storage-cache configurations only if a later claim requires filesystem-specific behavior;
- trace whether and when the fix reaches additional supported/downstream branches, but do not infer deployment from upstream merge;
- inspect restart behavior under deliberately constructed combinations of snapshot DB presence/absence and WAL marker presence/absence;
- preserve the existing Case-58 fault-injection plan around snapshot-file sync, WAL snapshot-marker sync, in-memory apply, publication, and release as separate stages;
- keep broader etcd persistence/filesystem engineering history in `computing-archaeology` if it grows beyond this retention-specific seam.

---

## 11. Related-repository boundary

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `SaveDBFrom` and `etcd snapshot fsync` found no dedicated packet to reuse.

The broader history of:

- etcd storage-layout evolution;
- WAL/snapshot implementation genealogy;
- filesystem crash-consistency engineering;
- Go file APIs;
- distribution-specific backports;
- device-cache and power-loss behavior;

belongs primarily in `computing-archaeology` if developed.

`technical-retention` should keep the narrow seam:

```text
payload bytes
    != namespace relation
    != control marker
    != restart authority
```

and the ordering rules that keep those layers mutually usable after failure.

---

## 12. Sources

1. etcd `v3.5.15`, `server/etcdserver/api/snap/db.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/api/snap/db.go>.
2. etcd `v3.5.15`, `server/etcdserver/api/rafthttp/http.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/api/rafthttp/http.go>.
3. Gyuho Lee, etcd commit `cf31e1f6033f0752f0c55d2456a0771be0c5ba80`, `fix: fsync snap directory when saving a received snapshot db`, 25 August 2026: <https://github.com/etcd-io/etcd/commit/cf31e1f6033f0752f0c55d2456a0771be0c5ba80>.
4. etcd PR #22314, same fix, created 20 August 2026, merged 3 September 2026: <https://github.com/etcd-io/etcd/pull/22314>.
5. etcd current `main`, post-fix `server/etcdserver/api/snap/db.go`: <https://github.com/etcd-io/etcd/blob/main/server/etcdserver/api/snap/db.go>.
6. Michael Kerrisk / Linux man-pages project, `fsync(2)`: <https://man7.org/linux/man-pages/man2/fsync.2.html>.
7. etcd PR #22378, automated cherry-pick to `release-3.7`, merged 9 September 2026: <https://github.com/etcd-io/etcd/pull/22378>.
8. etcd PR #22401, backport to `release-3.6`, merged 10 September 2026: <https://github.com/etcd-io/etcd/pull/22401>.

---

## Bounded conclusion

The 2026 etcd fix provides a unusually clean retention lesson because the maintainers corrected both the code and the claim boundary:

```text
snapshot bytes synced
    !=
final snapshot name durably published
    !=
WAL marker durably recorded
    !=
restart has admitted a usable snapshot
```

The E2E tests then impose the equally important methodological limit:

```text
controlled process crash / retry behavior
    !=
direct proof of sudden-power-loss directory durability
```

The strongest conclusion is therefore not “fsync makes snapshots safe.” It is narrower and more useful:

> **A retained recovery object can depend on several separately persisted relations — content, namespace publication, control marker, and restart admission — and correct failure handling may require refusing to advance from one layer until the preceding durability obligation has been established.**
