# Case 144 deepening — ZooKeeper 3.0.0–3.1.2 close-session durability and restart recovery

## Status

**`bounded deepening complete`** — this note closes one narrow evidence debt in Case 144: whether early public ZooKeeper source merely deleted ephemerals in memory, or represented session termination as recoverable transaction/snapshot state that could survive server restart and participate in quorum commit.

It directly inspects the frozen Apache ZooKeeper `release-3.0.0` and `release-3.1.2` source tags. Apache project news dates release 3.0.0 to **27 October 2008** and release 3.1.2 to **14 December 2009**. The Apache archive also preserves the corresponding source release directories.

This note does **not** claim to identify the first pre-release commit that invented ephemeral znodes, session transactions, or Zab. It also does not turn one source inspection into a proof about all later ZooKeeper releases.

## Research question

Case 144 already grounds the user-visible relation:

```text
live session
    -> ephemeral znode remains live

session close / timeout-qualified expiration
    -> closeSession state transition
    -> ephemerals retired from current namespace
```

The remaining source-level question was narrower:

> **In the earliest public-release source, what retained evidence makes session creation/termination and ephemeral retirement reconstructible across server restart, and where does close-session sit relative to disk synchronization and quorum commit?**

The bounded answer is:

```text
session / ephemeral relation
    -> snapshot + transaction-log representation

close / expiration decision
    -> zxid-bearing closeSession transaction
    -> log synchronization
    -> (quorum mode) ACK / majority commit
    -> DataTree.killSession()
    -> current ephemeral deletion

restart
    -> snapshot restores live sessions + DataTree
    -> DataTree rebuilds ephemeralOwner -> path index
    -> transaction-log replay adds/removes sessions and reapplies closeSession
    -> orphan ephemeral owners absent from restored session set are killed
```

That is stronger than `ephemerals are deleted when a process exits`, but weaker than `all historical bytes are erased` or `every timeout decision is itself continuously checkpointed before closeSession exists`.

## Source custody

### Primary frozen source

Apache ZooKeeper GitHub mirror, frozen release tags:

- `release-3.0.0`
- `release-3.1.2`

The inspected files are:

- `src/java/main/org/apache/zookeeper/server/ZooKeeperServer.java`
- `src/java/main/org/apache/zookeeper/server/PrepRequestProcessor.java`
- `src/java/main/org/apache/zookeeper/server/SyncRequestProcessor.java`
- `src/java/main/org/apache/zookeeper/server/DataTree.java`
- `src/java/main/org/apache/zookeeper/server/util/SerializeUtils.java`
- `src/java/main/org/apache/zookeeper/server/persistence/FileTxnSnapLog.java`
- `src/java/main/org/apache/zookeeper/server/quorum/LeaderZooKeeperServer.java`
- `src/java/main/org/apache/zookeeper/server/quorum/ProposalRequestProcessor.java`
- `src/java/main/org/apache/zookeeper/server/quorum/Leader.java`
- `src/java/main/org/apache/zookeeper/server/quorum/Follower.java`
- `src/java/main/org/apache/zookeeper/server/quorum/FollowerZooKeeperServer.java`
- `src/java/main/org/apache/zookeeper/server/quorum/SendAckRequestProcessor.java`

### Release dating

Apache ZooKeeper News records:

- **27 October 2008** — release 3.0.0 available;
- **14 December 2009** — release 3.1.2 available.

Apache's historical distribution archive retains `zookeeper-3.0.0/` and `zookeeper-3.1.2/` directories. The archive timestamp is useful custody corroboration, while the project news is used for release dates.

## Historical record

### H/P — release 3.0.0 already routes expiration through `closeSession`

In `release-3.0.0`, `ZooKeeperServer.expire(sessionId)` calls `closeSession(sessionId)`. `closeSession(...)` submits an `OpCode.closeSession` request through the ordinary request-processing pipeline rather than directly deleting each ephemeral in the timeout detector.

This matters because the failure-detector judgment and the namespace mutation are separate stages:

```text
session tracker decides expiration
    -> submit closeSession request
    -> transaction processing / persistence path
    -> namespace mutation
```

Therefore, even in the first archived 3.0.0 release inspected here:

> `timeout decision != immediate ad-hoc in-memory node deletion`.

### H/P — `closeSession` receives a zxid in the preparation stage

`release-3.0.0` `PrepRequestProcessor` creates a `TxnHeader` for `OpCode.closeSession` using `zks.getNextZxid()`. Before forwarding the request, it also walks the session's ephemerals plus outstanding changes and registers deletion-shaped change records under that zxid.

The same basic structure is still present in `release-3.1.2`.

This directly grounds:

```text
session termination request
    -> ordered transaction identity (zxid)
```

It does not by itself prove durability or quorum commitment; those are later stages.

### H/P — a close-session log record needs the transaction header, not a payload record

Both 3.0.0 and 3.1.2 `SerializeUtils.deserializeTxn(...)` treat `OpCode.closeSession` specially: once the `TxnHeader` is deserialized, the method returns `null` for the transaction body.

The historical representation therefore differs from a create or set-data transaction:

```text
closeSession durable identity
    = TxnHeader(type=closeSession, client/session id, zxid, ...)
    + no separate transaction payload object
```

This is a source-format fact. It should not be generalized into a claim that all session cleanup state in every ZooKeeper version is header-only.

### H/P — standalone processing syncs the log before applying the transaction downstream

`release-3.0.0` `SyncRequestProcessor` describes itself as logging requests to disk and states that a request is not passed to the next request processor until its log has been synced.

Its `flush(...)` path calls the log writer's `commit()` and only then forwards queued requests to the next processor. `release-3.1.2` preserves the same ordering.

For standalone mode this gives the bounded sequence:

```text
prepared closeSession
    -> append to transaction log
    -> commit / sync log
    -> pass downstream
    -> FinalRequestProcessor / DataTree application
```

Thus:

> `closeSession prepared != closeSession durably logged != closeSession applied to current DataTree`.

### H/P — `DataTree.processTxn(closeSession)` performs the namespace retirement

In both inspected releases, `DataTree.processTxn(...)` dispatches `OpCode.closeSession` to `killSession(clientId, zxid)`.

`killSession(...)` removes the session's ephemeral-path set and calls `deleteNode(path, zxid)` for each associated ephemeral.

This is the concrete mutation edge:

```text
committed/replayed closeSession
    -> session-owned ephemeral index consumed
    -> individual current namespace nodes deleted
```

The delete is logical namespace state transition. The source does not say that old transaction logs, old snapshots, filesystem blocks, backups, or storage media are securely erased.

### H/P — snapshots retain both live sessions and ephemeral ownership metadata

`release-3.0.0` `SerializeUtils.serializeSnapshot(...)` writes the current session map as `(session id, timeout)` pairs before serializing the `DataTree`.

The `DataTree` serialization writes each `DataNode`, whose persisted stat contains `ephemeralOwner`. During `DataTree.deserialize(...)`, nonzero `ephemeralOwner` values are used to rebuild the in-memory map from owner session ID to ephemeral paths.

Therefore a snapshot retains two related but distinct state classes:

```text
sessionsWithTimeouts
    = which sessions the restored server treats as live candidates

DataNode.ephemeralOwner
    = which session relation each ephemeral node claims
```

The derived owner->paths index can be rebuilt from node metadata; it need not be independently authoritative.

### H/P — transaction-log replay reconstructs session creation and termination after a snapshot

In both 3.0.0 and 3.1.2 `FileTxnSnapLog.restore(...)`:

1. the snapshot is deserialized into the DataTree and session map;
2. transaction-log entries after the snapshot are replayed;
3. `createSession` inserts the session ID/timeout into the restored session map;
4. `closeSession` removes the session ID and calls `DataTree.processTxn(...)`, which reapplies `killSession(...)`.

This means the restart model is not merely `load latest namespace bytes`:

```text
snapshot base
    + ordered post-snapshot session/data transactions
    -> reconstructed current session set
    + reconstructed current namespace
```

### H/P — startup reconciles ephemeral ownership against the restored live-session set

After restore, `ZooKeeperServer.loadData()` in both releases scans `dataTree.getSessions()`. If an ephemeral owner appears in the DataTree but is absent from `sessionsWithTimeouts`, the session is collected as dead and `killSession(...)` is invoked before startup completes; a clean snapshot is then taken.

This is an important recovery invariant:

```text
restored ephemeralOwner relation
    + no restored live session record
    -> owner treated as dead
    -> ephemerals removed from current namespace
```

So snapshot/tree survival alone does not grant liveness authority to an ephemeral object.

### H/P — release 3.1.2 quorum mode proposes close-session like other state-changing transactions

`LeaderZooKeeperServer` in 3.1.2 installs the chain:

```text
PrepRequestProcessor
    -> ProposalRequestProcessor
    -> CommitProcessor
    -> ToBeAppliedRequestProcessor
    -> FinalRequestProcessor
```

`ProposalRequestProcessor` sends state-changing requests to the leader proposal path and to a `SyncRequestProcessor`.

Therefore a prepared `closeSession` is not a special non-replicated side effect in this inspected release; it enters the replicated transaction path.

### H/P — follower ACK follows local transaction-log sync

In 3.1.2, a follower receiving a `PROPOSAL` deserializes its transaction header/body and calls `FollowerZooKeeperServer.logRequest(...)`. That method sends the request to the follower's `SyncRequestProcessor`.

The follower's `SyncRequestProcessor` appends and commits the log before calling its next processor. That next processor is `SendAckRequestProcessor`, which emits the `ACK` for ordinary transactions.

The bounded ordering is therefore:

```text
follower receives closeSession proposal
    -> append local log
    -> commit/sync local log
    -> SendAckRequestProcessor
    -> ACK to leader
```

This is source-level evidence that, for the inspected 3.1.2 path, a follower's transaction ACK is downstream of local log sync.

### H/P — leader majority ACK converts the proposal into committed state

`Leader.processAck(...)` increments the proposal's ACK count. Once the count is greater than half of the configured quorum peers, it removes the proposal from outstanding proposals, sends a commit packet, and calls the leader's `CommitProcessor.commit(...)` for the request.

The bounded sequence becomes:

```text
zxid-bearing closeSession proposal
    -> replicas durably log before ACK
    -> leader observes majority ACK
    -> COMMIT
    -> committed request applied
    -> killSession
    -> ephemerals removed from current namespace
```

This is the strongest result of this deepening.

It should still not be simplified to `the exact moment a client timeout elapsed was durably replicated`. The replicated state transition is `closeSession`; timeout observation and the subsequent transaction are distinct stages.

## Engineering reconstruction

### E — liveness authority depends on two retained state classes

A restored ephemeral znode is not live merely because its node record survives a snapshot. Liveness depends on the compatibility of:

```text
restored node.ephemeralOwner
    + restored/replayed live-session membership
```

The server explicitly checks for owner relations lacking a live restored session and removes those ephemerals.

This supports:

> `object bytes survived restart != liveness authority survived restart`.

### E — a derived owner index can be rebuilt while the relation remains durable

The in-memory `session -> ephemeral paths` collection is not the only embodiment of ownership. `DataTree.deserialize(...)` reconstructs it from persisted node `ephemeralOwner` fields.

Therefore:

> `runtime lookup structure lost != ownership relation lost`.

This is functionally similar to other reconstruction cases in the repository, but no genealogy is implied.

### E — session-set persistence and node persistence can disagree transiently in recovery material

A fuzzy snapshot/log architecture can expose recovery inputs in which DataTree node state and the final reconstructed session set are not yet the same as the post-replay current state. ZooKeeper resolves this through transaction replay and the dead-session cleanup check.

The important boundary is:

```text
recovery material internally contains stale relation
    != stale relation remains authoritative after recovery
```

### E — retirement intent, durability, consensus, and namespace effect are separate milestones

For the inspected quorum path:

```text
expiration detected
    != closeSession transaction prepared
    != local log synchronized
    != quorum committed
    != DataTree killSession applied
    != observers have learned deletion
```

Treating all of these as one instant would erase useful failure boundaries.

### E — durable close state is smaller than the set of nodes it retires

`closeSession` does not persist a serialized list of all ephemeral paths in its own transaction body. The durable transaction identifies the session; the nodes to remove are determined from the restored/current ownership relation.

This is a useful retention pattern:

```text
small durable control fact
    + reconstructible relation/index
    -> retirement of many current objects
```

It does not mean the system can recover without the DataTree's ownership metadata.

### E — clean restart can restore a still-live session without rewriting every ephemeral payload

Because snapshots retain live session IDs/timeouts and nodes retain `ephemeralOwner`, the server can reconstruct the relation after restart. The runtime owner->paths index is rebuilt from the nodes.

That is different from saying a client session has unlimited lifetime across arbitrary ensemble outages. Session validity still depends on ZooKeeper's timeout/failover semantics and later revalidation behavior.

## Functional comparisons

### A — Case 144 vs Case 71 ZooKeeper recovery history

Case 71 asks how fuzzy snapshot plus transaction log reconstructs server state. This deepening uses that lower-level mechanism only to answer a Case 144 question:

> which retained recovery facts carry the session/ephemeral liveness relation and its retirement transition across restart?

The relationship is:

```text
Case 71 recovery substrate
    -> snapshot sessions + DataTree
    -> post-snapshot log replay

Case 144 liveness relation
    -> restored session membership
    + restored ephemeralOwner relation
    + replayed closeSession retirement
```

This is reuse of a recovery mechanism, not a second general ZooKeeper persistence history.

### A — ZooKeeper owner relation vs HDFS scan cursor or Flash mapping rebuild

The common functional pattern is that a volatile convenience structure can be reconstructed from more durable evidence. The object and authority being reconstructed are different:

- ZooKeeper: owner session -> ephemeral paths;
- HDFS scanner: traversal progress / iterator state;
- Flash mapping: logical -> physical resolution.

No historical influence is inferred.

### A — close-session transaction vs a tombstone

Both can functionally retire previously live state, but `closeSession` is not documented here as a per-znode tombstone. It names the session-level state transition and causes the implementation to delete all currently associated ephemerals.

Therefore:

> `many objects retired by one durable control transition != one tombstone stored per object`.

## Philosophical interpretation

### I — persistence can preserve a relation rather than only a payload

The bounded philosophical point is modest:

> what survives a restart need not be a second copy of the visible coordination object; it can be the smaller relation and ordered transition history needed to decide whether that object still counts as current.

For ZooKeeper, the relevant retained pieces include session membership/timeouts, node ownership metadata, and close-session transaction history.

This does not make ZooKeeper a theory of social presence, memory, identity, or mortality. It is an engineering example of operational presence depending on retained relation-state plus recovery rules.

## Explicit non-claims

1. This note does not claim ZooKeeper invented ephemeral namespace objects.
2. It does not identify the first pre-3.0.0 commit that introduced ephemerals.
3. It does not claim release 3.0.0 was the first implementation ever built by the project.
4. It does not claim every later ZooKeeper release has byte-for-byte identical code paths.
5. It does not claim a lost TCP connection directly creates a `closeSession` transaction.
6. It does not claim timeout observation and quorum commitment occur at the same instant.
7. It does not claim the creator process is physically dead when the session expires.
8. It does not claim every session heartbeat/touch is individually written as a transaction-log record.
9. It does not claim `ephemeralOwner` alone proves the owner session is still live.
10. It does not claim the runtime owner->paths map is separately authoritative durable state.
11. It does not claim `closeSession` carries a serialized list of ephemeral paths.
12. It does not claim logical deletion erases older snapshots or transaction logs.
13. It does not claim log `commit()` here proves any particular disk-controller capacitor or storage-media behavior below the filesystem/OS contract.
14. It does not claim one follower ACK alone is enough to commit a transaction.
15. It does not claim a prepared transaction is already committed.
16. It does not claim a quorum-committed close means every observer has already processed a watch notification.
17. It does not claim a restored node record is automatically admissible as a live ephemeral.
18. It does not claim the source inspection proves all crash interleavings without fault injection.
19. It does not claim standalone and quorum mode have identical failure semantics.
20. It does not claim historical recovery traces vanish when current namespace state changes.

## Claim ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| ZooKeeper 3.0.0 routed expiration through an ordinary `closeSession` request | H/P | `release-3.0.0` `ZooKeeperServer.java` | supported |
| 3.0.0 `closeSession` receives a zxid in request preparation | H/P | `release-3.0.0` `PrepRequestProcessor.java` | supported |
| `closeSession` is represented by its transaction header without a separate txn body in the inspected releases | H/P | 3.0.0/3.1.2 `SerializeUtils.java` | supported |
| standalone `SyncRequestProcessor` syncs the log before forwarding state-changing requests downstream | H/P | 3.0.0/3.1.2 `SyncRequestProcessor.java` | supported |
| `DataTree.processTxn(closeSession)` calls `killSession`, which deletes session ephemerals | H/P | 3.0.0/3.1.2 `DataTree.java` | supported |
| snapshots retain live session IDs/timeouts and node-level `ephemeralOwner` metadata | H/P | 3.0.0 `SerializeUtils.java`; `DataTree.java` | supported |
| DataTree deserialization rebuilds the owner-session -> ephemeral-path index | H/P | 3.0.0/3.1.2 `DataTree.java` | supported |
| restore replays `createSession` and `closeSession` to reconstruct session membership and namespace state | H/P | 3.0.0/3.1.2 `FileTxnSnapLog.java` | supported |
| startup removes restored ephemerals whose owner lacks a restored live session record | H/P | 3.0.0/3.1.2 `ZooKeeperServer.loadData()` | supported |
| in 3.1.2 quorum mode a follower sends ACK downstream of local log sync | H/P | `Follower*`; `SyncRequestProcessor`; `SendAckRequestProcessor` | supported |
| leader majority ACK causes commit of the proposal | H/P | 3.1.2 `Leader.processAck()` | supported |
| timeout detection itself is the same event as durable quorum commit | X | staged source path | rejected |
| snapshot node survival alone proves ephemeral liveness after restart | X | restored-session reconciliation | rejected |
| logical ephemeral deletion is secure media erase | X | no lower-layer evidence | rejected |

## Source ledger

1. Apache ZooKeeper News: <https://zookeeper.apache.org/news/>
   - 27 October 2008: release 3.0.0 available.
   - 14 December 2009: release 3.1.2 available.
2. Apache historical distribution archive: <https://archive.apache.org/dist/hadoop/zookeeper/>
   - retains the 3.0.0 and 3.1.2 release directories.
3. Apache ZooKeeper `release-3.0.0` source:
   - `ZooKeeperServer.java`: <https://github.com/apache/zookeeper/blob/release-3.0.0/src/java/main/org/apache/zookeeper/server/ZooKeeperServer.java>
   - `PrepRequestProcessor.java`: <https://github.com/apache/zookeeper/blob/release-3.0.0/src/java/main/org/apache/zookeeper/server/PrepRequestProcessor.java>
   - `SyncRequestProcessor.java`: <https://github.com/apache/zookeeper/blob/release-3.0.0/src/java/main/org/apache/zookeeper/server/SyncRequestProcessor.java>
   - `DataTree.java`: <https://github.com/apache/zookeeper/blob/release-3.0.0/src/java/main/org/apache/zookeeper/server/DataTree.java>
   - `SerializeUtils.java`: <https://github.com/apache/zookeeper/blob/release-3.0.0/src/java/main/org/apache/zookeeper/server/util/SerializeUtils.java>
   - `FileTxnSnapLog.java`: <https://github.com/apache/zookeeper/blob/release-3.0.0/src/java/main/org/apache/zookeeper/server/persistence/FileTxnSnapLog.java>
4. Apache ZooKeeper `release-3.1.2` source:
   - `ZooKeeperServer.java`: <https://github.com/apache/zookeeper/blob/release-3.1.2/src/java/main/org/apache/zookeeper/server/ZooKeeperServer.java>
   - `PrepRequestProcessor.java`: <https://github.com/apache/zookeeper/blob/release-3.1.2/src/java/main/org/apache/zookeeper/server/PrepRequestProcessor.java>
   - `SyncRequestProcessor.java`: <https://github.com/apache/zookeeper/blob/release-3.1.2/src/java/main/org/apache/zookeeper/server/SyncRequestProcessor.java>
   - `DataTree.java`: <https://github.com/apache/zookeeper/blob/release-3.1.2/src/java/main/org/apache/zookeeper/server/DataTree.java>
   - `SerializeUtils.java`: <https://github.com/apache/zookeeper/blob/release-3.1.2/src/java/main/org/apache/zookeeper/server/util/SerializeUtils.java>
   - `FileTxnSnapLog.java`: <https://github.com/apache/zookeeper/blob/release-3.1.2/src/java/main/org/apache/zookeeper/server/persistence/FileTxnSnapLog.java>
   - `LeaderZooKeeperServer.java`: <https://github.com/apache/zookeeper/blob/release-3.1.2/src/java/main/org/apache/zookeeper/server/quorum/LeaderZooKeeperServer.java>
   - `ProposalRequestProcessor.java`: <https://github.com/apache/zookeeper/blob/release-3.1.2/src/java/main/org/apache/zookeeper/server/quorum/ProposalRequestProcessor.java>
   - `Leader.java`: <https://github.com/apache/zookeeper/blob/release-3.1.2/src/java/main/org/apache/zookeeper/server/quorum/Leader.java>
   - `Follower.java`: <https://github.com/apache/zookeeper/blob/release-3.1.2/src/java/main/org/apache/zookeeper/server/quorum/Follower.java>
   - `FollowerZooKeeperServer.java`: <https://github.com/apache/zookeeper/blob/release-3.1.2/src/java/main/org/apache/zookeeper/server/quorum/FollowerZooKeeperServer.java>
   - `SendAckRequestProcessor.java`: <https://github.com/apache/zookeeper/blob/release-3.1.2/src/java/main/org/apache/zookeeper/server/quorum/SendAckRequestProcessor.java>

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `ZooKeeper closeSession ephemeral session transaction log` returned no dedicated reusable packet. Broader Zab genealogy, pre-Apache/early-Yahoo commit history, production deployment, filesystem/fsync behavior, and coordination-service history remain better placed there.

## Remaining evidence debt

This slice closes the **early public-release close-session durability/recovery path** for the inspected 3.0.0 and 3.1.2 baselines. It does not close:

- exact pre-release commit archaeology for the first introduction of ephemeral znodes, `ephemeralOwner`, or `closeSession`;
- fault-injection tests at each boundary (`prepared`, `logged`, `ACKed`, `committed`, `applied`);
- exact OS/filesystem/storage-device durability semantics beneath ZooKeeper's transaction-log `commit()` call;
- later Zab implementation changes and modern session/reconfiguration behavior;
- observer/watch timing after quorum commit;
- broad Chubby/ZooKeeper/failure-detector genealogy.

## Bounded result

The early ZooKeeper source gives a much sharper retention statement than the API-level rule alone:

> **An ephemeral znode's restart-time liveness is reconstructed from retained session state plus retained node ownership metadata; session retirement is represented as an ordered `closeSession` transaction that is replayable after restart, and in the inspected 3.1.2 quorum path replica ACKs follow local log synchronization before majority commit.**

This yields five durable distinctions for Case 144:

```text
node record retained
    != owner session remains live

owner->paths runtime index lost
    != ownership relation lost

expiration detected
    != closeSession prepared
    != log synchronized
    != quorum committed
    != current ephemerals deleted

current ephemeral deleted
    != historical recovery material erased

recovery evidence survives
    != stale relation remains authoritative after replay/reconciliation
```
