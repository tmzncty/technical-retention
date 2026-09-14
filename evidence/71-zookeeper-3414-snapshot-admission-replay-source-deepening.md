# Case 71 Deepening — ZooKeeper 3.4.14 Snapshot Admission, Fallback, and Replay Source Path

## Status

**`bounded deepening complete`**

Canonical case: [`../cases/71-apache-zookeeper-fuzzy-snapshot-replay-recovery.md`](../cases/71-apache-zookeeper-fuzzy-snapshot-replay-recovery.md)

This record closes one deliberately narrow evidence debt left by the Case 71 grounding record:

> **In the exact Apache ZooKeeper 3.4.14 release source, how is a fuzzy snapshot materialized, how does restart distinguish a merely present snapshot file from an admissible recovery snapshot, and where does ordered transaction-log replay begin?**

It does **not** attempt to reconstruct all ZooKeeper/Zab persistence history, later snapshot formats, every filesystem crash mode, or a general checkpointing genealogy.

---

## Why this slice matters

The existing Case 71 record already establishes from Apache documentation and the 2010 ZooKeeper paper that:

- snapshots are deliberately fuzzy;
- a snapshot can correspond to no actual instantaneous tree state;
- ordered idempotent replay supplies the missing temporal closure;
- current recovery depends on a set of snapshot/log artifacts rather than one privileged file.

One implementation-level question remained open: the canonical case still referred to `latest complete fuzzy snapshot` without pinning down what `complete` means in the 3.4.14 code path.

The release source shows that there are several distinct stages:

```text
snapshot pathname exists
    != snapshot has end marker
    != snapshot passes full deserialize + checksum
    != snapshot is selected as restart base
    != recovered state has reached end of retained log
```

This is a useful retention distinction because a crash can leave bytes and even a correctly named snapshot file without leaving an admissible recovery representation.

---

## Exact release anchor

Apache's `release-3.4.14` tag resolves to annotated tag object:

- tag object: `39004dc929c88ef875cbb111e97b7dc1844a2c91`
- release commit: `4c25d480e66aadd371de8bd2fd8da255ac140bcf`
- tag message: `ZooKeeper 3.4.14 release.`
- tagger date: 2019-04-01

All implementation claims below are bounded to that commit unless explicitly marked otherwise.

Primary source root:

- <https://github.com/apache/zookeeper/tree/4c25d480e66aadd371de8bd2fd8da255ac140bcf>

This matters because current ZooKeeper source has continued to evolve; later `SnapStream`, digest, compression, or snapshot behavior must not be silently projected backward onto 3.4.14.

---

## Historical record

### H/P — periodic snapshotting is launched in a separate thread

In `SyncRequestProcessor.run()`, after enough logged requests have accumulated, ZooKeeper:

1. rolls the transaction log;
2. checks whether an earlier snapshot thread is still alive;
3. starts a new `ZooKeeperThread("Snapshot Thread")`;
4. calls `zks.takeSnapshot()` inside that separate thread;
5. continues the request-processing loop independently.

Source:

- `zookeeper-server/src/main/java/org/apache/zookeeper/server/SyncRequestProcessor.java`
- exact release commit `4c25d480...`

This gives implementation-level support to the already-grounded fuzzy-snapshot description. Snapshot serialization is not implemented as a stop-the-world copy under this path.

It does **not** prove that every object read during serialization is unconstrained; the 2010 paper remains the stronger source for the per-znode consistency explanation.

### H/P — snapshot filename is chosen before serialization from `lastProcessedZxid`

`ZooKeeperServer.takeSnapshot()` calls `txnLogFactory.save(...)`.

`FileTxnSnapLog.save()` then:

```text
lastZxid = dataTree.lastProcessedZxid
snapshotFile = snapDir / Util.makeSnapshotName(lastZxid)
snapLog.serialize(dataTree, sessionsWithTimeouts, snapshotFile)
```

Source:

- `zookeeper-server/src/main/java/org/apache/zookeeper/server/ZooKeeperServer.java`
- `zookeeper-server/src/main/java/org/apache/zookeeper/server/persistence/FileTxnSnapLog.java`

Thus the filename boundary is captured before the snapshot payload has finished being materialized.

This aligns with the administrator documentation's statement that the suffix is a snapshot-start replay boundary rather than the maximum transaction whose effect might later appear in the fuzzy payload.

### H/P — 3.4.14 writes directly to the final `snapshot.<zxid>` pathname

`FileSnap.serialize(..., File snapShot)` opens:

```text
new FileOutputStream(snapShot)
```

on the file supplied by `FileTxnSnapLog.save()`.

The method then:

1. wraps the file in buffered output;
2. wraps that in an Adler32 `CheckedOutputStream`;
3. writes the snapshot header and serialized data tree/session state;
4. obtains the checksum value;
5. writes that checksum as `val`;
6. writes the string `/` as the final path marker;
7. flushes and closes the stream.

There is no temporary snapshot pathname and no rename in this bounded method chain.

There is also no explicit `FileDescriptor.sync()` or `FileChannel.force(...)` in `FileSnap.serialize()`.

This directly narrows the old evidence debt. For ZooKeeper 3.4.14, the source path inspected here is **not** a `write temp -> fsync -> atomic rename` snapshot publication protocol.

That negative finding must be kept narrow:

- it is about this 3.4.14 snapshot-writing path;
- it is not a universal claim about every ZooKeeper release;
- it does not by itself establish what every filesystem/device does after Java close/flush;
- it does not imply that an incomplete snapshot will be accepted on restart.

### H/P — an incomplete final-named snapshot is an expected crash case

`Util.isValidSnapshot(File f)` contains an unusually explicit comment:

> snapshot may be invalid if it is incomplete when the server dies while storing a snapshot.

The method first requires a parsable `snapshot.<zxid>` name. It then performs a lightweight structural check:

- file length must be at least 10 bytes;
- the final five bytes must encode a Jute string of length one containing `/`.

The `/` is therefore a completion marker for the bounded format.

The source comment in `FileSnap.findNValidSnapshots()` is equally important: this end-marker check does **not** mean the snapshot is truly valid; it only gives high-probability validity before full deserialize/checksum verification.

Therefore:

```text
final filename exists
    != structurally complete snapshot
```

and:

```text
structural end marker present
    != fully verified snapshot
```

### H/P — restart can fall back from a newer unusable snapshot to an older one

`FileSnap.deserialize()` does not simply open the lexically/latest-zxid file and trust it.

It:

1. asks for up to 100 recent snapshots that pass the lightweight end-marker filter;
2. considers them newest first;
3. deserializes the candidate through an Adler32 `CheckedInputStream`;
4. checks the `ZKSN` file-header magic;
5. deserializes the data tree and sessions;
6. reads the stored checksum value;
7. compares it with the checksum accumulated during the read;
8. catches an `IOException`, logs a warning, and tries the next candidate;
9. fails only if no candidate can be accepted.

After a candidate succeeds, `FileSnap.deserialize()` sets `dt.lastProcessedZxid` from the **selected snapshot filename**.

This supports:

```text
newest snapshot pathname
    != newest admissible snapshot
```

and:

```text
retained older snapshot
    -> can remain a live recovery fallback
```

within the bounded search of up to 100 structurally plausible snapshots.

It does not prove that retaining 100 snapshots is a deployment recommendation. `100` is the implementation's bounded search limit in this method, not the administrator guide's purge policy.

### H/P — snapshot admission has two different validity layers

The release code separates two checks that are easy to collapse conceptually:

**Layer 1 — lightweight structural completion check**

`Util.isValidSnapshot()` checks filename shape, minimum length, and the trailing `/` marker.

**Layer 2 — full deserialize/checksum admission**

`FileSnap.deserialize()` checks file-header magic, parses the snapshot, and validates the Adler32 value.

So:

```text
completion marker
    != content-integrity verification
```

The source itself warns that the first is only a high-probability filter.

This is important for retention terminology: `complete` and `valid` are not one undifferentiated property.

### H/P — restore explicitly composes selected snapshot state with later transaction-log replay

`FileTxnSnapLog.restore()` performs exactly two top-level operations:

```text
snapLog.deserialize(dt, sessions)
fastForwardFromEdits(dt, sessions, listener)
```

`fastForwardFromEdits()` opens the transaction log at:

```text
dt.lastProcessedZxid + 1
```

and processes records in sequence, updating the high restored zxid as it proceeds.

The selected snapshot filename therefore supplies the replay boundary after the snapshot has passed admission.

This is a more precise implementation statement than:

> `load snapshot and then some logs`.

The bounded chain is:

```text
select checksum-valid snapshot candidate
    -> derive replay boundary from selected snapshot filename
    -> read txn log from boundary + 1
    -> apply records in order
    -> reach highest retained replayed zxid
```

### H/P — the source explicitly recognizes replay over a fuzzy snapshot

`FileTxnSnapLog.processTransaction()` includes the implementation comment:

> snapshots are lazily created, so later transactions can make it into the snapshot.

It then explains that restoring such a snapshot can cause `NONODE` / `NODEEXISTS` results while replaying transactions whose effects are already embodied in the fuzzy image, and says these failures are safe to ignore in this recovery context.

This is direct source-level confirmation of the paper's central fuzzy-replay argument.

It should **not** be generalized into:

- all transaction errors are safe to ignore;
- replay order does not matter;
- arbitrary duplicate client requests are idempotent;
- an arbitrary corrupted snapshot becomes valid merely because replay exists.

### H/P — transaction-log durability and snapshot-file publication use visibly different source paths

`FileTxnLog.commit()` flushes transaction-log streams and, when `forceSync` is enabled, calls:

```text
log.getChannel().force(false)
```

By contrast, the bounded `FileSnap.serialize()` path writes, flushes, and closes the final-named snapshot but contains no corresponding explicit `force()` call.

This is a source-level implementation difference, not a complete storage-stack durability proof.

The safe claim is:

```text
transaction-log force path
    != snapshot-file write path
```

The unsafe claim would be:

> therefore every committed transaction survives every power failure while every snapshot does not.

That stronger conclusion requires filesystem, kernel, controller, device-cache, mount-option, and power-failure evidence not supplied by these Java methods.

---

## Retained-state decomposition

The exact 3.4.14 source supports a more detailed decomposition than the original canonical case:

1. **live in-memory data tree** — serving state;
2. **transaction-log records** — ordered replay history;
3. **snapshot filename zxid** — conservative replay boundary captured before serialization completes;
4. **snapshot payload bytes** — fuzzy durable materialization;
5. **trailing completion marker** — lightweight evidence that serialization reached the end of the bounded format;
6. **stored Adler32 value** — integrity evidence checked during full deserialize;
7. **snapshot candidate ordering** — newest-first selection policy;
8. **older retained snapshot candidates** — fallback recovery bases when a newer candidate is unusable;
9. **selected snapshot boundary** — the filename zxid of the candidate actually admitted;
10. **post-boundary transaction-log suffix** — history needed to advance the selected image;
11. **transaction order and replay semantics** — semantic condition that makes fuzzy reapplication admissible;
12. **lower-layer persistence behavior** — assumed below this Java-level path, not proven by it.

The useful relation is therefore:

```text
named snapshot artifact
    != structurally complete snapshot
    != checksum-admissible snapshot
    != selected recovery base
    != recovered current state
```

---

## Engineering reconstruction

### E — publication by final pathname can precede recovery admissibility

Because `FileTxnSnapLog.save()` chooses the final `snapshot.<zxid>` name and `FileSnap.serialize()` writes directly to it, file existence can begin before serialization reaches its completion marker.

The reader-side admission path compensates for that possibility by refusing structurally incomplete candidates and then fully validating surviving candidates.

This is not the same design as hiding incomplete state behind a temporary filename and publishing it by rename.

### E — validation state is part of recoverability even though it is not application payload

The `/` end marker and checksum do not represent ZooKeeper znodes. They are control evidence used to decide whether snapshot bytes are eligible to become a recovery base.

Thus:

```text
payload bytes retained
    != evidence sufficient to admit those bytes for recovery
```

### E — retaining an older snapshot can preserve recoverability when the newest artifact is unusable

A newer final-named file can fail structural or checksum admission while an older candidate remains usable.

Therefore snapshot retention is not only about having `the newest file`. Multiple retained candidates can provide **recovery-option redundancy** at the representation level.

This is distinct from ZooKeeper ensemble replication. The copies here are different temporal recovery representations on one server's storage path, not peer replicas of one current znode state.

### E — snapshot filename zxid has two roles but not unlimited authority

After the candidate payload is accepted, 3.4.14 reconstructs `lastProcessedZxid` from the selected filename and uses it to start transaction-log replay.

That makes the filename a control boundary with real recovery consequences.

But it still does not mean:

```text
snapshot filename zxid
    = maximum zxid whose effects appear anywhere in fuzzy payload
```

The fuzzy-snapshot semantics explicitly reject that equivalence.

### E — reader-side fallback is not crash-atomic publication

The implementation can survive some incomplete/corrupt latest snapshots because recovery checks candidates and can fall back.

That must not be relabeled as `atomic snapshot commit`.

The source instead shows a different construction:

```text
direct final-name write
    + completion marker
    + checksum
    + newest-to-older fallback
```

Those mechanisms can improve recoverability without making publication an indivisible storage transaction.

### E — a valid snapshot is still not a complete recovery set

Passing structural and checksum admission proves only that the snapshot candidate can be deserialized under the bounded format.

It does not prove that the retained transaction logs cover the replay interval needed for current-state recovery.

Thus:

```text
snapshot admissibility
    != recovery-set completeness
```

The original Case 71 file-set argument remains necessary.

---

## Functional comparisons — analogy only

### A — Case 56 Kafka checkpoint membership

Case 56 shows that small recovery-control metadata can materially alter how surviving payload is interpreted after restart.

ZooKeeper's snapshot completion marker/checksum/filename boundary likewise influence whether surviving bytes are admitted and where replay begins.

The analogy stops there:

- Kafka's bounded case concerns replica high-watermark checkpoint membership and follower truncation/resync behavior;
- ZooKeeper Case 71 concerns fuzzy materialization admission and ordered transaction-log replay.

No common implementation or historical lineage is claimed.

### A — Case 18 OpenZFS scrub completion

Case 18 distinguishes work performed, progress durably checkpointed, and a safe completion-observation boundary.

ZooKeeper similarly distinguishes a file being present from serialization having reached its completion marker and from full checksum admission.

Again this is only a functional comparison about **completion evidence**. A ZooKeeper snapshot is not an OpenZFS scan checkpoint.

### A — Case 58 Raft snapshot

The existing Case 71 boundary remains unchanged. Raft's stable snapshot carries a different consensus/log-compaction contract; ZooKeeper 3.4.14 can restore from a deliberately fuzzy image whose start boundary may precede effects already embodied in the payload.

---

## Philosophical boundary

### I — persistence of bytes is not identical to persistence of an admissible representation

The bounded engineering record permits one careful interpretive statement:

> A technical artifact can continue to exist physically while the system refuses to treat it as a legitimate memory of state.

Here that refusal is concrete and mechanized: malformed/incomplete structure or checksum failure prevents a candidate snapshot from becoming the restart base.

Do not generalize this into claims about human memory, archival authenticity, or epistemology. The source supports an engineering admission relation, not a universal theory of remembrance.

---

## Explicit non-claims

This deepening does **not** claim that:

1. ZooKeeper 3.4.14 publishes snapshots with an atomic rename;
2. the absence of rename makes recovery unsafe;
3. Java `flush()` or `close()` alone proves persistence through every sudden power loss;
4. the trailing `/` marker proves all snapshot bytes are uncorrupted;
5. the Adler32 checksum proves cryptographic authenticity;
6. the newest snapshot filename is always the snapshot selected for recovery;
7. retaining 100 snapshots is an operator recommendation;
8. `autopurge.snapRetainCount=3` follows from the 100-candidate search limit;
9. any checksum-valid snapshot alone is sufficient if required transaction logs are missing;
10. any replay order is safe;
11. arbitrary client requests are idempotent;
12. every replay error is safely ignorable;
13. ZooKeeper invented fuzzy snapshots, WAL recovery, completion markers, checksums, or fallback recovery;
14. the 3.4.14 implementation path is unchanged in current ZooKeeper;
15. a source-level `force(false)` call proves every lower storage layer obeys the intended durability boundary;
16. purge or replacement of a snapshot proves secure physical erasure.

---

## Claim ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| `release-3.4.14` resolves to commit `4c25d480...` | H/P | Apache ZooKeeper Git tag object | supported |
| periodic snapshot work is launched in a separate snapshot thread in the bounded request-processing path | H/P | `SyncRequestProcessor.run()` | supported |
| final snapshot filename is chosen from `dataTree.lastProcessedZxid` before serialization finishes | H/P | `FileTxnSnapLog.save()` | supported |
| `FileSnap.serialize()` writes directly to the final supplied path | H/P | `FileSnap.serialize()` | supported |
| bounded snapshot writer uses temp-file + atomic rename publication | X | no such step in inspected 3.4.14 path | rejected for this path |
| trailing `/` acts as lightweight structural completion evidence | H/P | `Util.isValidSnapshot()`; `FileSnap.serialize()` | supported |
| end-marker check alone proves full content validity | X | `FileSnap` comment and checksum path | rejected |
| full deserialize validates header and Adler32 checksum | H/P | `FileSnap.deserialize()` | supported |
| recovery can skip a newer unusable candidate and try older candidates | H/P | `FileSnap.deserialize()` | supported |
| successful candidate filename determines restored `lastProcessedZxid` | H/P | `FileSnap.deserialize()` | supported |
| transaction replay starts at selected `lastProcessedZxid + 1` | H/P | `FileTxnSnapLog.fastForwardFromEdits()` | supported |
| implementation explicitly expects later transactions to appear in a lazy snapshot | H/P | `FileTxnSnapLog.processTransaction()` comment/path | supported |
| snapshot checksum validity proves recovery-set completeness | X | restore/log dependency | rejected |
| Java source alone proves whole-storage-stack crash durability | X | lower-layer evidence absent | rejected |

---

## Source ledger

### Primary source A — exact release tag

Apache ZooKeeper `release-3.4.14`:

- <https://github.com/apache/zookeeper/tree/4c25d480e66aadd371de8bd2fd8da255ac140bcf>
- tag object: <https://api.github.com/repos/apache/zookeeper/git/tags/39004dc929c88ef875cbb111e97b7dc1844a2c91>

### Primary source B — snapshot serialization and candidate admission

`FileSnap.java` at the release commit:

- <https://github.com/apache/zookeeper/blob/4c25d480e66aadd371de8bd2fd8da255ac140bcf/zookeeper-server/src/main/java/org/apache/zookeeper/server/persistence/FileSnap.java>

Evidence used:

- newest-to-older candidate loop;
- Adler32 verification;
- header magic check;
- `lastProcessedZxid` reconstruction from selected filename;
- direct final-path `FileOutputStream`;
- checksum + trailing `/` write.

### Primary source C — lightweight snapshot validity check

`Util.java` at the release commit:

- <https://github.com/apache/zookeeper/blob/4c25d480e66aadd371de8bd2fd8da255ac140bcf/zookeeper-server/src/main/java/org/apache/zookeeper/server/persistence/Util.java>

Evidence used:

- comment that server death during snapshot storage can leave an invalid/incomplete snapshot;
- filename recognition;
- minimum length check;
- trailing five-byte Jute string marker check.

### Primary source D — save and restore composition

`FileTxnSnapLog.java` at the release commit:

- <https://github.com/apache/zookeeper/blob/4c25d480e66aadd371de8bd2fd8da255ac140bcf/zookeeper-server/src/main/java/org/apache/zookeeper/server/persistence/FileTxnSnapLog.java>

Evidence used:

- snapshot filename from current `lastProcessedZxid`;
- `restore()` composition;
- replay from `lastProcessedZxid + 1`;
- lazy/fuzzy snapshot replay comment and tolerated duplicate-effect errors.

### Primary source E — asynchronous snapshot launch

`SyncRequestProcessor.java` at the release commit:

- <https://github.com/apache/zookeeper/blob/4c25d480e66aadd371de8bd2fd8da255ac140bcf/zookeeper-server/src/main/java/org/apache/zookeeper/server/SyncRequestProcessor.java>

### Primary source F — transaction-log force/read boundary

`FileTxnLog.java` at the release commit:

- <https://github.com/apache/zookeeper/blob/4c25d480e66aadd371de8bd2fd8da255ac140bcf/zookeeper-server/src/main/java/org/apache/zookeeper/server/persistence/FileTxnLog.java>

Evidence used only for the narrow comparison that `commit()` has a conditional `FileChannel.force(false)` path while `FileSnap.serialize()` does not.

---

## Related-repository duplication check

A fresh search of `tmzncty/computing-archaeology` for `ZooKeeper snapshot transaction log zxid` returned no dedicated material to reuse.

Accordingly this file stays retention-specific. A broader source genealogy of ZooKeeper/Zab persistence, Jute snapshot formats, or historical changes in snapshot publication belongs in `computing-archaeology` if pursued later.

---

## Findings suitable for synthesis

1. **Final pathname existence ≠ completed snapshot materialization.**
2. **Completion marker ≠ full content-integrity verification.**
3. **Checksum-admissible snapshot ≠ complete recovery set.**
4. **Newest snapshot filename ≠ necessarily selected recovery base.**
5. **Retained older representations can provide recovery fallback even when they are not the newest state image.**
6. **Snapshot filename zxid is a replay-control boundary, not a maximum-embodied-update certificate.**
7. **Reader-side validation/fallback ≠ crash-atomic publication.**
8. **Payload bytes ≠ evidence authorizing those bytes to participate in recovery.**
9. **3.4.14 direct final-name snapshot writing ≠ temp-file/atomic-rename protocol.**
10. **Transaction-log force path ≠ snapshot-file write path.**

---

## Remaining evidence debt

This slice closes the old `exact release-tag source archaeology for snapshot creation/atomic rename and replay restore paths` debt for ZooKeeper 3.4.14.

Still open, and intentionally not inferred from source inspection alone:

- controlled kill/power-cut experiments at multiple points in `FileSnap.serialize()`;
- direct tests that leave a final-named file before the trailing marker and verify fallback to the previous snapshot;
- deliberate snapshot body/checksum corruption with a structurally intact trailing marker;
- missing/corrupt transaction-log segments after an otherwise valid snapshot;
- exact filesystem/device persistence behavior for snapshot close/flush versus transaction-log `force(false)`;
- evolution of this snapshot publication/admission path before 3.4.14 and in later releases;
- interaction with later digest/compression/snapshot APIs;
- broader Zab epoch/history recovery, which is outside this case.

None of those remaining debts changes the bounded source-level conclusion established here.