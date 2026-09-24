# Case 71 Deepening — ZooKeeper 3.4.14 Purge, Preceding-Log Preservation, and Recovery-Set Retirement

## Status

**`bounded deepening complete`**

Canonical case: [`../cases/71-apache-zookeeper-fuzzy-snapshot-replay-recovery.md`](../cases/71-apache-zookeeper-fuzzy-snapshot-replay-recovery.md)

This record closes one deliberately narrow debt left after the 3.4.14 snapshot-admission deepening:

> **When ZooKeeper 3.4.14 retires old snapshot/log artifacts, what relation is it actually preserving, and is the configured snapshot-retention count the same thing as a count of restart-admissible recovery bases?**

The bounded answer is:

```text
configured snapshot-retention count
    -> choose recent snapshot-looking filenames
    -> derive a zxid purge frontier from the oldest chosen name
    -> preserve the transaction log that can straddle that frontier
    -> preserve all newer logs
    -> retire older snapshot/log names outside that retained closure
```

but:

```text
recent snapshot-looking filename
    != lightweight-valid snapshot
    != checksum-admissible restart snapshot
```

The purge path and the restart-admission path deliberately use different source routines in this release. That distinction is the center of this packet.

This is **not** a claim that ZooKeeper 3.4.14 necessarily loses recoverability when a recent snapshot is incomplete, nor a claim that `autopurge.snapRetainCount` is broken. The source establishes a control-boundary asymmetry; a destructive failure claim would require a concrete file-set/fault trace proving that no remaining snapshot/log combination can reconstruct state.

---

## Exact release anchor

All source claims below are bounded to Apache ZooKeeper `release-3.4.14`, release commit:

- `4c25d480e66aadd371de8bd2fd8da255ac140bcf`

Primary source root:

- <https://github.com/apache/zookeeper/tree/4c25d480e66aadd371de8bd2fd8da255ac140bcf>

The companion Case 71 source deepening already establishes the snapshot-write and restart-admission path for this exact release. This packet does not silently project later ZooKeeper behavior backward.

---

## Historical / source record

### H/P — automatic cleanup is a policy layer above `PurgeTxnLog`

In 3.4.14, `DatadirCleanupManager` describes itself as managing cleanup of snapshots and corresponding transaction logs. It takes:

- `autopurge.snapRetainCount`;
- `autopurge.purgeInterval`.

If the purge interval is positive, it schedules a `PurgeTask`, and that task calls:

```java
PurgeTxnLog.purge(new File(logsDir), new File(snapsDir), snapRetainCount);
```

Source:

- `zookeeper-server/src/main/java/org/apache/zookeeper/server/DatadirCleanupManager.java`
- exact release commit `4c25d480...`

Thus automatic cleanup does not have a separate recovery-set selection algorithm in this release. Its retention behavior is inherited from `PurgeTxnLog`.

### H/P — `PurgeTxnLog.purge()` selects the N most recent snapshot names, not the N most recent restart-admissible snapshots

`PurgeTxnLog.purge(...)` requires a count of at least three, then executes:

```java
List<File> snaps = txnLog.findNRecentSnapshots(num);
int numSnaps = snaps.size();
if (numSnaps > 0) {
    purgeOlderSnapshots(txnLog, snaps.get(numSnaps - 1));
}
```

The important word in the called method is **`Recent`**, not `Valid`.

`FileTxnSnapLog.findNRecentSnapshots(n)` delegates to `FileSnap.findNRecentSnapshots(n)`.

In `FileSnap`, the method comment is explicit:

> `find the last n snapshots. this does not have any checks if the snapshot might be valid or not`

Its loop accepts a file when `Util.getZxidFromName(...) != -1`; it does not call `Util.isValidSnapshot()`, deserialize the file, or verify the Adler32 checksum.

Sources:

- `zookeeper-server/src/main/java/org/apache/zookeeper/server/PurgeTxnLog.java`
- `zookeeper-server/src/main/java/org/apache/zookeeper/server/persistence/FileTxnSnapLog.java`
- `zookeeper-server/src/main/java/org/apache/zookeeper/server/persistence/FileSnap.java`
- exact release commit `4c25d480...`

This directly supports:

```text
counted by purge as a recent snapshot
    != admitted by restart as a usable snapshot
```

### H/P — restart uses a different, stricter snapshot-admission path

The earlier Case 71 deepening established the contrasting restart path. `FileSnap.deserialize()` first calls `findNValidSnapshots(100)`.

That helper:

1. sorts snapshot files newest first;
2. invokes `Util.isValidSnapshot()`;
3. accepts only files passing the lightweight end-marker test.

`FileSnap.deserialize()` then performs the stronger admission step:

- parse the snapshot header;
- deserialize the snapshot;
- recompute/check Adler32;
- fall back to an older candidate if an `IOException` rejects the newer one.

Therefore the exact 3.4.14 source contains two different selection relations:

```text
purge selection:
    parseable snapshot name + recency

restart selection:
    lightweight structural validity
    + successful deserialize/header
    + checksum equality
```

This is not a vocabulary accident. The methods and call sites are distinct.

### H/P — the oldest selected recent snapshot name becomes the purge frontier

`purgeOlderSnapshots(...)` derives:

```java
leastZxidToBeRetain = Util.getZxidFromName(
    snapShot.getName(), PREFIX_SNAPSHOT);
```

from the oldest snapshot in the recent-name set chosen above.

The deletion filter then considers snapshot and log files with a filename zxid lower than that threshold to be old candidates, subject to one important exception for transaction logs.

So the purge frontier is source-visible and simple:

```text
oldest selected snapshot filename zxid
    -> leastZxidToBeRetain
```

It is not recomputed from the snapshot that `FileSnap.deserialize()` would actually admit on a hypothetical restart at that moment.

### H/P — a transaction-log filename older than the snapshot frontier can still belong to the retained recovery set

`PurgeTxnLog` contains a detailed implementation comment explaining why a transaction log named below snapshot `X` may still be required: a log file starts at one zxid but may contain transactions with zxids greater than `X`.

The code therefore constructs `retainedTxnLogs` with:

```java
txnLog.getSnapshotLogs(leastZxidToBeRetain)
```

and excludes those logs from deletion even when the log filename zxid is lower than the snapshot-retention frontier.

This directly establishes:

```text
log filename starts before snapshot frontier
    != log is obsolete for that snapshot
```

### H/P — `FileTxnLog.getLogFiles()` implements “one predecessor plus all later logs” conservatively

`FileTxnSnapLog.getSnapshotLogs(zxid)` delegates to `FileTxnLog.getLogFiles(...)`.

That method first finds the greatest log starting zxid `<= snapshotZxid`:

```text
logZxid = max(start_zxid where start_zxid <= snapshotZxid)
```

It then returns every log whose starting zxid is `>= logZxid`.

The resulting retained log set is therefore conservatively shaped as:

```text
newest log whose start <= snapshot frontier
    + every newer log
```

This is stronger than the naive rule:

```text
keep only logs whose filename zxid >= snapshot zxid
```

and is exactly the kind of relation-level retention this repository is trying to distinguish from simple file age.

### H/P — Apache issue history records this predecessor-log boundary as a real recovery concern

ASF JIRA `ZOOKEEPER-2420`, created 2 May 2016, describes an earlier autopurge behavior that could delete the log file preceding the oldest retained snapshot even though restore might need transactions from that file. The report explains that snapshot/log roll timing means the preceding log can contain zxids newer than the snapshot boundary. The issue was later resolved as a duplicate of `ZOOKEEPER-2574`.

Primary project issue record:

- <https://issues.apache.org/jira/browse/ZOOKEEPER-2420>

This historical issue is useful because it shows the predecessor-log exception was not invented by retrospective repository analysis. It was an explicit project recovery problem.

The 3.4.14 source inspected above already contains the conservative predecessor-log preservation logic.

### H/P — the release tests verify the predecessor-log exception and concurrent purge boundary

`PurgeTxnTest` in the same release contains tests whose comments and assertions match the source logic.

`testSnapFilesGreaterThanToRetain()` and related tests deliberately preserve:

> the newest log file preceding the oldest retained snapshot

because it may contain transactions newer than that snapshot.

The test then verifies that older unneeded files are deleted while:

- the chosen snapshots remain;
- their newer logs remain;
- the required preceding log remains.

`testPurgeWhenLogRollingInProgress()` separately exercises purge while clients create znodes and logs/snapshots can roll. `PurgeTxnLog` documents that snapshots/logs created after the current selection pass are excluded from that purge cycle.

These tests support the bounded claims about purge-frontier and predecessor-log preservation. They do **not** by themselves establish arbitrary crash safety during deletion.

### H/P — the release test for `findNRecentSnapshots()` is filename/type oriented, not full recovery admission

`testFindNRecentSnapshots()` constructs simulated log and snapshot files and verifies that `findNRecentSnapshots()` returns snapshot files rather than log files and returns the requested recent count when available.

That test does not deserialize the selected files or validate their snapshot checksum.

This matches the implementation contract of `findNRecentSnapshots()` itself: it is a recent-snapshot-name selector, not the restart-admission routine.

### H/P — invalid recent snapshots are not merely hypothetical in ZooKeeper history

ASF JIRA `ZOOKEEPER-713` (March 2010) records a production incident involving an invalid snapshot produced while the server encountered an `OutOfMemoryError` during snapshot creation. In the issue discussion, ZooKeeper developer Benjamin Reed explains that the invalid file could be bypassed because recovery could use an older snapshot.

Primary project issue record:

- <https://issues.apache.org/jira/browse/ZOOKEEPER-713>

This issue is used only to establish the historical reality of incomplete/invalid snapshot artifacts and older-snapshot fallback. It is **not** evidence that 3.4.14 autopurge actually retired the only usable fallback in production.

---

## Retained-state decomposition

The purge path adds another layer to the existing Case 71 recovery model.

A 3.4.14 data directory can contain at least these distinct relations:

1. **snapshot filename recency** — ordering by zxid encoded in names;
2. **lightweight snapshot structural validity** — end-marker based filtering;
3. **full snapshot restart admission** — deserialize/header/checksum success;
4. **selected snapshot replay boundary** — zxid of the candidate actually admitted by restart;
5. **transaction-log file start zxid** — a file-level locator, not its maximum contained zxid;
6. **log replay coverage** — the actual transaction range needed after the snapshot boundary;
7. **configured retention count** — administrative quantity controlling purge selection;
8. **purge frontier** — filename zxid of the oldest selected recent snapshot;
9. **predecessor-log exception** — a lower-named log retained because it can straddle that frontier;
10. **deletion set** — older named files outside the source-derived retained closure;
11. **physical deletion completion** — per-file `File.delete()` outcomes, which can fail independently;
12. **restart recoverability** — a higher-level relation over an admissible snapshot (if used), adequate log coverage, and replay semantics.

Do not collapse these into one `latest checkpoint` or `retention count` variable.

---

## Engineering reconstruction

The terms in this section are repository reconstruction language, not ZooKeeper historical vocabulary.

### E — retention count ≠ count of admissible recovery bases

The exact source gives a direct counterexample to the tempting equation:

```text
autopurge.snapRetainCount = N
    -> N checksum-admissible restart snapshots are guaranteed retained
```

That implication is not established by the 3.4.14 selection code, because purge counts `findNRecentSnapshots()` results, while restart admits snapshots through a different validity/checksum path.

The safe reconstructed relation is:

```text
policy count
    -> N recent parseable snapshot names are selected when available
```

Any stronger statement about N independently usable recovery bases needs additional validation or a fault trace.

### E — recovery-set retirement authority is relational rather than per-file

The purge code cannot decide whether an old log is disposable from its own filename alone. It must relate that log to the oldest retained snapshot boundary and preserve the predecessor that may carry newer transactions.

Therefore:

```text
artifact age
    != retirement authority
```

A file becomes retireable only relative to the recovery set the system chooses to preserve.

`recovery-set retirement authority` is a project term for this relation.

### E — a lower-named artifact can remain semantically newer than part of a higher-named recovery boundary

Because one transaction-log file covers a range while its name exposes only its starting zxid:

```text
start(log) < snapshot boundary
    and
end(log) > snapshot boundary
```

can both be true.

This is a concrete example of:

```text
identifier ordering
    != dependency ordering
```

The log is `older` as a file start point while still carrying history needed to reconstruct a later state.

### E — purge frontier ≠ restart frontier

The source supports two frontiers:

```text
purge frontier
    = zxid encoded by oldest recent snapshot name selected for retention

restart frontier
    = zxid encoded by the snapshot candidate that actually passes restart admission
```

They can coincide in the normal case, but the source does not make them definitionally identical.

This is the most important new anti-collapse in this packet.

### E — preserving fallback representations and retiring history are coupled but not identical objectives

`FileSnap.deserialize()` can make an older snapshot useful when a newer candidate is rejected. `PurgeTxnLog`, meanwhile, exists to retire old artifacts once enough recent names are retained.

So ZooKeeper exposes two competing but legitimate control goals:

```text
retain alternative recovery bases
    vs
bound data-directory growth
```

The configured count is a policy compromise between them; it is not itself a proof that every retained candidate is equally admissible.

### E — a named-but-incomplete snapshot can influence purge selection without being eligible for restart admission

From the source alone, one can construct this bounded possibility:

```text
snapshot.A      valid older candidate
snapshot.B      valid recent candidate
snapshot.C      parseable name, incomplete/corrupt content
snapshot.D      valid recent candidate

purge name selection
    may count B/C/D by filename recency

restart selection
    can reject C by structural/checksum admission
```

Whether a particular purge run then destroys recoverability depends on the complete file set, retained transaction-log coverage, initial-state behavior, and exact failure timing. This packet therefore **does not** upgrade the source asymmetry into a data-loss result.

The right next experiment is a file-set fault matrix, not a stronger prose claim.

### E — purge completion ≠ atomic retirement transaction

`PurgeTxnLog` constructs a list of files and then calls `File.delete()` one file at a time. If a delete fails, it prints an error and continues.

Therefore:

```text
purge invocation returned from its loop
    != all selected obsolete artifacts necessarily disappeared
```

and:

```text
retirement set decision
    != atomic retirement of the whole set
```

Residual old files after a partial purge are primarily a bounded-growth/cleanup issue unless separately shown to affect restart selection. This source shape is not evidence of corruption by itself.

### E — “history no longer needed” is a stronger claim than “history falls below a policy frontier”

The purge algorithm is intentionally conservative about the predecessor log because filename position alone is insufficient to prove irrelevance.

The repository should therefore distinguish:

```text
below configured purge frontier
    != proven outside every retained recovery closure
```

The code adds the predecessor-log exception precisely because a naive frontier-only rule previously failed this distinction.

---

## Functional comparisons

These are heuristic comparisons only. No genealogy is asserted.

### A — Case 58 Raft snapshot-prefix retirement

Raft Case 58 also couples a materialized state representation to a history-retirement boundary, but its snapshot relation is different: the retained snapshot contains a stable committed/applied state plus continuation metadata such as the last included index/term.

ZooKeeper Case 71 is deliberately fuzzier: a snapshot may contain a temporally mixed image, and conservative ordered replay is part of making it recovery-equivalent.

Shared functional shape:

```text
materialized recovery representation
    -> permits some older replay history to be retired
```

Boundary:

```text
ZooKeeper fuzzy snapshot semantics
    != Raft stable snapshot semantics
```

### A — Case 05 RADOS PG-log retirement authority

Case 05's early Ceph source shows a peer-bounded completion frontier authorizing PG-log trimming. ZooKeeper's 3.4.14 purge frontier instead arises from a retained-snapshot policy plus replay-coverage geometry.

The useful comparison is only:

```text
current state established
    != old recovery evidence immediately disposable
```

The systems derive retirement authority differently and have no genealogy claimed here.

### A — Case 42 Kafka cleaner/checkpoint currentness

Kafka Case 42 separately demonstrates that a retained progress/checkpoint artifact can be working control state rather than payload state. ZooKeeper's purge count is another control quantity, but its role is not equivalent to Kafka cleaner checkpoints.

The comparison is useful only to block:

```text
maintenance metadata exists
    -> maintenance metadata is itself a correctness certificate
```

---

## Philosophical interpretation

This layer is interpretive, not historical evidence.

The new technical fact is that forgetting old recovery artifacts requires a relation among representations. ZooKeeper cannot simply say `old file -> forget it`; it must preserve enough of a cross-file recovery closure, including a log whose filename may appear older than the snapshot it supports.

A restrained philosophical formulation is:

> Technical forgetting can require retained evidence of how the present may still be reconstructed. A system earns the right to discard a trace only relative to another surviving representation plus the continuation relation that makes that representation operationally sufficient.

The interpretation stops at the mechanism. `PurgeTxnLog` is not a philosophical theory of forgetting, and `zxid` ordering should not be redescribed as human memory or archival meaning.

---

## Evidence-strength assessment

### Strong / direct

- exact 3.4.14 autopurge call path to `PurgeTxnLog`;
- recent-snapshot-name selection via `findNRecentSnapshots()`;
- explicit source comment that `findNRecentSnapshots()` performs no snapshot-validity checks;
- contrasting restart path with lightweight structural filtering and full checksum admission;
- purge frontier derived from oldest selected snapshot filename;
- predecessor-log retention through `getSnapshotLogs()` / `getLogFiles()`;
- test coverage of predecessor-log preservation and concurrent purge/log rolling;
- ASF JIRA historical record for the predecessor-log bug class and invalid-snapshot fallback.

### Engineering reconstruction

- `policy retention count != number of admissible recovery bases`;
- `purge frontier != restart frontier` as a conceptual distinction even when they coincide in the normal case;
- recent invalid/incomplete snapshot names can affect name-based purge selection;
- retirement authority is recovery-set-relative rather than a property of one file.

### Not established here

- a reproducible 3.4.14 data-loss trace caused by invalid snapshots being counted by purge;
- a guarantee that logs alone always recover every 3.4.14 deployment state after all snapshots are absent;
- crash-atomic or power-fail-atomic deletion;
- filesystem/device-cache durability of snapshot/log/delete operations;
- behavior of every ZooKeeper release before or after 3.4.14;
- whether a later release changed purge selection to validity-qualified candidates;
- an invention or priority claim for recovery-set-aware cleanup.

---

## Explicit non-claims

This packet does **not** claim that:

1. every recent snapshot is corrupt;
2. `autopurge.snapRetainCount=3` guarantees exactly three checksum-valid snapshots;
3. `autopurge.snapRetainCount=3` guarantees fewer than three valid snapshots either;
4. the purge implementation necessarily causes data loss;
5. a parseable snapshot filename is a valid snapshot;
6. the lightweight `/` end marker is equivalent to the Adler32 check;
7. Adler32 success proves lower-layer power-fail durability;
8. the snapshot zxid names the newest transaction embodied anywhere in a fuzzy snapshot;
9. a log whose starting zxid precedes a snapshot is necessarily obsolete;
10. the predecessor log is always needed in every file layout;
11. the conservative predecessor-log rule is minimal;
12. purge is a transaction over all deleted files;
13. a failed `File.delete()` corrupts service state;
14. retaining more files always increases correctness;
15. retaining fewer files is equivalent to logical forgetting of current ZooKeeper state;
16. ZooKeeper invented snapshot/log recovery;
17. ZooKeeper invented checkpoint garbage collection;
18. ZooKeeper's fuzzy snapshots are equivalent to Raft snapshots;
19. ZooKeeper purge semantics are equivalent to Ceph PG-log trimming;
20. this packet establishes later 3.5/3.6/3.7/3.8 behavior;
21. `ZOOKEEPER-2420` proves the new validity-count asymmetry described here;
22. `ZOOKEEPER-713` proves an autopurge failure;
23. filename-recency selection was intended as a formal recovery-proof rule;
24. the source-level distinction alone proves a production incident.

---

## Cross-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `PurgeTxnLog` / ZooKeeper purge did not locate a dedicated packet to reuse.

Accordingly, this repository keeps only the retention-specific slice:

```text
snapshot-name retention policy
    != snapshot restart admission

file identifier order
    != recovery dependency order

current-state recoverability
    -> can depend on a retained cross-file closure
    -> which in turn authorizes bounded retirement of older history
```

Broader ZooKeeper/Zab release genealogy, implementation chronology, operational tuning, and purge-feature evolution belong primarily in `computing-archaeology` if developed later.

---

## Highest-value next debt

The next useful step is no longer another source-reading pass over `PurgeTxnLog`. It is a small, explicit **3.4.14 file-set fault matrix**:

1. create several valid snapshots and rolled transaction logs;
2. manufacture one recent parseable-but-incomplete snapshot and one checksum-invalid recent snapshot;
3. run `PurgeTxnLog.purge(..., 3)`;
4. record exactly which snapshot/log files remain;
5. restart from the resulting directory;
6. record which snapshot is admitted and which log file the iterator opens first;
7. repeat with interruption between individual `File.delete()` calls;
8. distinguish `restart succeeds`, `restart reaches latest zxid`, `fallback redundancy decreased`, and `directory cleanup incomplete`.

That experiment can convert the source-level asymmetry in this packet into either:

- a demonstrated failure mode;
- a demonstrated safe fallback under the tested file geometry;
- or a narrower condition under which the distinction is operationally irrelevant.

Until then, the disciplined conclusion is only:

> **ZooKeeper 3.4.14's purge policy counts recent snapshot names, while restart separately qualifies snapshot candidates; the purge algorithm nevertheless contains a deliberately recovery-aware exception for transaction-log ranges that cross the snapshot frontier.**
