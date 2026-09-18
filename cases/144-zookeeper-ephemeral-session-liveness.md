# Apache ZooKeeper Ephemeral Znodes: Session-Scoped Liveness, Timeout-Qualified Retirement, and Logical Deletion

## Status

**`grounded`** — bounded to ZooKeeper's documented/session-implementation relation among a live client session, an ephemeral znode, timeout-based session termination, and automatic logical deletion. The public-documentation floor remains Apache ZooKeeper 3.1.2 (released 14 December 2009) plus the 2010 USENIX ATC ZooKeeper paper; frozen source archaeology now extends the implementation witness back to the archived `release-3.0.0` baseline (released 27 October 2008), while release-3.4.7 remains a later implementation witness.

Grounding record: [`../evidence/144-zookeeper-2009-2015-ephemeral-session-liveness-grounding.md`](../evidence/144-zookeeper-2009-2015-ephemeral-session-liveness-grounding.md).

Early durability/restart deepening: [`../evidence/144-zookeeper-2008-2009-close-session-durability-recovery-deepening.md`](../evidence/144-zookeeper-2008-2009-close-session-durability-recovery-deepening.md).

## Scope

This case asks one narrow distributed-retention question:

> **Can an object remain authoritative only while a separate, time-qualified session relation remains valid, so that a transport interruption need not delete it but session expiration does?**

The bounded relation is:

```text
client establishes ZooKeeper session S
    -> S has a negotiated timeout
    -> client creates ephemeral znode E
    -> E records S as ephemeralOwner

connection/server change
    -> client may reconnect to another ZooKeeper server
    -> same session S can remain valid
    -> E remains live while S remains active

no session traffic beyond timeout / explicit close
    -> service terminates S
    -> closeSession state transition is processed
    -> ephemerals associated with S are deleted
    -> observers may learn of deletion / expiration later
```

This is **not** a general ZooKeeper, Zab, failure-detector, lease, service-discovery, lock, session-persistence, or garbage-collection history. It does not claim that ZooKeeper invented session-scoped temporary namespace entries. Chubby's 2006 paper already documented sessions/KeepAlives and ephemeral files, but with materially different file-liveness semantics.

The retention-specific claim is narrower:

> **ZooKeeper makes object liveness depend on a retained session-to-znode relation rather than on byte age or one TCP connection. That relation can survive reconnection, can be reconstructed from persisted session/ownership evidence after server restart, can be retired by an explicit or timeout-qualified `closeSession` transaction, and can disappear logically while lower-level recovery history may still preserve traces of the old state.**

`session-scoped liveness`, `liveness authority`, and `retirement authority` below are project engineering terms, not ZooKeeper's historical vocabulary.

## Historical vocabulary

The sources directly use `session`, `session timeout`, `ephemeral node` / `ephemeral znode`, `ephemeralOwner`, `heartbeat`, `PING`, `session expiration`, `closeSession`, `zxid`, `group membership`, and `watch`.

Do not silently normalize these into a generic object `TTL`, Chubby `session lease`, Kubernetes lease, Raft leadership lease, database row TTL, or media-retention timer.

## Historical record

### H/P — ephemeral znodes were documented in ZooKeeper 3.1.2 by December 2009

Apache's 3.1.2 Programmer's Guide says ephemeral znodes exist as long as the session that created them is active and are deleted when the session ends. It also says an ephemeral znode cannot have children. The same release's `Stat` description exposes `ephemeralOwner`, the session ID of the owner for an ephemeral node.

Apache's project news dates ZooKeeper 3.1.2 availability to **14 December 2009**.

This establishes the bounded behavior before the June 2010 USENIX paper without claiming that 3.1.2 introduced the feature.

### H/P — session identity is not one transport connection

The 3.1.2 guide says a client can reconnect to another server in the ensemble and presents the same session ID/password when doing so. PING/request traffic keeps the session alive.

The 2010 paper states the same relation more explicitly: sessions allow a client to move transparently from one ZooKeeper server to another and therefore persist across ZooKeeper servers. If the client cannot communicate with one server it connects to another to re-establish the session.

Therefore:

> `TCP/server connection lifetime != ZooKeeper session lifetime`.

### H/P — ephemeral lifetime follows session termination, not znode age

Hunt et al. distinguish regular znodes, which clients create/delete explicitly, from ephemeral znodes, which are deleted explicitly or automatically when the creating session terminates deliberately or due to failure. The paper's group-membership example makes this operational: each member creates an ephemeral child; if the process fails or ends, the representing znode is automatically removed.

The evidence does **not** describe an object-age TTL. A long-lived ephemeral can remain present while its session remains valid.

### H/P — session termination is timeout-qualified service judgment

The 2010 paper says sessions have an associated timeout. ZooKeeper considers a client faulty if it receives nothing from the session for more than that timeout; the leader determines session failure from ensemble receipt of traffic. The client library sends heartbeat messages in idle periods and can change servers before timeout.

The 3.4.7 Programmer's Guide later states the operational rule directly: expiration is managed by the ZooKeeper cluster; when the cluster hears nothing from the client within the negotiated timeout, it expires the session and deletes the session's ephemerals.

This is a failure-detection contract, not proof that the client process has physically ceased to exist.

### H/P — release-3.4.7 source turns expiration into a close-session state transition

In the release-3.4.7 source tree:

- `ZooKeeperServer.expire()` logs the exceeded timeout and calls the same `close(sessionId)` path used by session close;
- `close()` submits an `OpCode.closeSession` request;
- `PrepRequestProcessor` assigns `createSession` and `closeSession` requests a new zxid through `pRequest2Txn(...)` and marks the session closing while accounting for associated ephemerals;
- `DataTree.processTxn()` handles `OpCode.closeSession` by invoking `killSession(...)`;
- `DataTree.killSession()` removes the session's ephemeral-path set and deletes each znode with the close transaction's zxid.

The annotated `release-3.4.7` tag is dated **21 November 2015**. This source is a later implementation witness, not a claim that every internal detail was identical in 2009.

### H/P — the archived 3.0.0 source already has the same core close-session persistence relation

Fresh source archaeology of `release-3.0.0`, which Apache project news dates to **27 October 2008**, moves the implementation floor earlier than the prior Case 144 record.

The frozen source already shows:

- `expire(sessionId)` routing through `closeSession(...)`;
- `PrepRequestProcessor` assigning a zxid-bearing `TxnHeader` to `OpCode.closeSession`;
- `SyncRequestProcessor` committing the transaction log before forwarding the request downstream;
- `DataTree.processTxn(closeSession)` invoking `killSession(...)` to delete the session's ephemeral paths;
- snapshots serializing live session IDs/timeouts as well as DataTree nodes carrying `ephemeralOwner`;
- DataTree deserialization rebuilding the in-memory session-to-ephemeral-path index from persisted node metadata;
- transaction-log restore replaying `createSession` and `closeSession` to reconstruct live session membership and namespace state;
- startup removing restored ephemerals whose owner is absent from the restored live-session set.

This does **not** establish the exact pre-release commit that introduced the mechanism. It establishes that it is present in the earliest archived public release inspected here.

### H/P — release-3.1.2 quorum ACK follows local log synchronization, then majority commit

The 3.1.2 quorum path sharpens the durability boundary. `ProposalRequestProcessor` proposes state-changing requests and also sends them through a local `SyncRequestProcessor`. On followers, `FollowerZooKeeperServer.logRequest(...)` forwards received proposals to a `SyncRequestProcessor`; that processor appends and commits the transaction log before invoking `SendAckRequestProcessor`, which emits the transaction ACK. `Leader.processAck(...)` commits a proposal only after the ACK count exceeds half of the configured quorum peers.

For the inspected baseline:

```text
closeSession proposal
    -> replica local log sync
    -> ACK
    -> majority ACK
    -> COMMIT
    -> committed request application
    -> killSession / current ephemeral deletion
```

This is evidence about the transaction transition, not proof that the earlier **timeout observation itself** is synchronously durable at the instant it is made.

### H/P — creator awareness can lag service-side retirement

The 3.4.7 Programmer's Guide notes that a disconnected client may not learn that its session expired until it later regains connectivity. Other connected clients watching the affected znodes can be notified when the cluster deletes them.

Therefore:

> `authoritative state transition != creator's immediate knowledge of that transition`.

## Retained state and mechanism

The bounded relation contains several different state classes:

1. **ephemeral znode payload/name/stat** — coordination data currently in the ZooKeeper namespace;
2. **session identity and validity state** — the relation to which ephemeral liveness is attached;
3. **negotiated session timeout / heartbeat progress** — evidence used to decide whether the session remains admissible;
4. **`ephemeralOwner` relation** — per-znode metadata tying the object to a session ID;
5. **close/expiration transaction state** — the state transition that retires the session and associated ephemerals;
6. **observer/watch state** — notification machinery, distinct from whether the deletion has already become authoritative;
7. **snapshot/transaction-log recovery history** — a separate persistence layer treated in Case 71, but now directly shown to carry session membership, node ownership, and `closeSession` replay evidence needed by this case.

The central relation is therefore not:

```text
ephemeral znode bytes exist -> znode is live
```

but:

```text
ephemeral object
    + valid creating session
    + timeout/heartbeat relation
    = current namespace liveness
```

and retirement is not:

```text
one socket breaks -> object vanishes
```

but:

```text
session explicitly closes
or
service concludes timeout has expired
    -> session termination
    -> ordered closeSession transition
    -> associated ephemeral deletion
```

## Engineering reconstruction

### E — object lifetime can be relational rather than age-based

The znode does not carry a simple countdown from creation. Its continued namespace existence depends on whether the creating session remains active. Session traffic can therefore maintain an old ephemeral without rewriting its payload.

This supports:

> `object age != retention deadline` and `session timeout != object TTL`.

### E — transport continuity != session continuity != object continuity

A broken connection can cause the client library to reconnect elsewhere while preserving the session. The ephemeral therefore outlives a particular TCP connection/server attachment.

Conversely, once the session is expired, later network recovery does not retroactively restore the old session's ephemeral nodes. The client must treat expiration as unrecoverable for that session and establish new state.

### E — failure-detector judgment != ontological process death

The service's timeout rule is based on absence of session traffic. A partitioned or paused process can therefore still exist while ZooKeeper has already concluded its session is faulty and retired its ephemerals.

For coordination use, the znode represents **service-qualified membership/liveness**, not metaphysical or hardware-level proof that the process no longer exists.

### E — `ephemeralOwner` is relation metadata, not another payload copy

The stat field links a znode to the creating session ID. This small control relation can decide the lifetime of larger coordination data. It is not a complete session history, process identity proof, ACL ownership model, or replica of the znode payload.

### E — explicit close and timeout expiration can converge on one cleanup transition without having the same cause

The early 3.0.0 source already routes expiration through `closeSession`, and the 3.4.7 implementation retains the same broad convergence. This supports a common state-retirement mechanism across the inspected endpoints.

It does **not** erase the distinction between:

- administrator/application-intended close;
- timeout-based service inference;
- transport disconnection before timeout.

### E — restart-time object bytes != restart-time liveness authority

The early source makes the recovery relation explicit:

```text
restored DataNode with ephemeralOwner
    + restored/replayed live session membership
    -> eligible current ephemeral relation

restored DataNode with ephemeralOwner
    + owner absent from restored live session set
    -> dead-session cleanup
    -> node removed from current namespace
```

Therefore:

> `ephemeral bytes survived snapshot/restart != ephemeral remains authoritative`.

### E — volatile owner index can disappear without destroying the durable ownership relation

The in-memory `session -> ephemeral paths` map is rebuilt during DataTree deserialization from each node's persisted `ephemeralOwner` value.

Thus:

> `runtime lookup structure lost != ownership relation lost`.

This is a reconstruction result, not a claim that all runtime state is reconstructible from `ephemeralOwner` alone.

### E — retirement intent, durable log state, consensus, application, and observation are separate milestones

The 3.1.2 quorum source supports a more precise boundary:

```text
expiration detected
    != closeSession prepared
    != transaction log synchronized
    != quorum committed
    != DataTree killSession applied
    != creator/observer has learned the deletion
```

This distinction matters when reasoning about failures between stages.

### E — retirement completion != observer awareness

A disconnected creator may learn of expiration only after reconnecting. State authority therefore belongs to the ensemble's session decision/committed transition, not to a synchronous acknowledgement held by the creator.

### E — logical ephemeral deletion != disappearance of historical recovery material

Case 71 grounds ZooKeeper's separate transaction-log/snapshot recovery set. `closeSession` itself is retained as ordered transaction evidence and drives znode deletion. It is therefore unsafe to infer that deleting an ephemeral from the **current namespace** proves the corresponding creation/data bytes have already vanished from every older log, snapshot, backup, filesystem block, or storage medium.

This is an engineering/cross-case boundary, not a forensic claim about a particular ZooKeeper deployment.

## Functional comparisons and boundaries

### A — ZooKeeper ephemeral znode vs Chubby ephemeral file

Chubby 2006 provides clear prior art for session/KeepAlive coordination and ephemeral namespace objects. But the retention conditions are not interchangeable:

- Chubby's paper says an ephemeral node is deleted when no client has it open (and ephemeral directories also require emptiness);
- ZooKeeper says an ephemeral znode lives while the **creating session** is active and deletes it when that session ends.

Therefore:

> `same "ephemeral" vocabulary != same liveness predicate`.

The comparison blocks an invention shortcut while preserving the different mechanisms.

### A — ZooKeeper Case 144 vs ZooKeeper fuzzy-snapshot Case 71

Case 71 asks what snapshot/log material must remain so a crashed server can reconstruct current ZooKeeper state. Case 144 asks when a coordination object is allowed to remain in that current state.

The new source-level bridge is now explicit:

```text
Case 71 recovery substrate
    -> snapshot sessions + DataTree
    -> post-snapshot transaction replay

Case 144 liveness relation
    -> restored session membership
    + restored ephemeralOwner relation
    + replayed closeSession retirement
```

These can still point in opposite directions:

```text
session expires
    -> current ephemeral logically disappears
while
older recovery material may remain retained for restart/history
```

Thus:

> `namespace liveness != recovery-history retention`.

### A — ZooKeeper session relation vs PostgreSQL replication slot (Case 141)

Both are counterexamples to `connection ended -> dependent relation ended`:

- a ZooKeeper session can survive server reconnection until timeout;
- a PostgreSQL replication slot can retain a consumer's WAL claim while that consumer is disconnected.

But the retained obligations differ. The slot preserves replay history for future continuation; the ZooKeeper session qualifies the current liveness of ephemeral coordination objects and has explicit timeout-based retirement. No genealogy is inferred.

### A — timeout-qualified deletion vs ordinary TTL

Both can involve elapsed time, but the mechanisms differ. ZooKeeper session expiration is refreshed by ongoing session communication and can retire multiple associated ephemerals together. A generic per-object TTL normally attaches an expiry deadline directly to each object.

Do not translate the former into the latter without product-specific evidence.

## Failure and forgetting

- **Transient connection loss:** may interrupt communication without ending the session; deleting ephemerals immediately on socket loss would be too strong for ZooKeeper's documented semantics.
- **Session timeout / explicit close:** retires session-scoped ephemeral liveness through an ordered close-session state transition in the inspected source.
- **Failure between detection and commit:** timeout observation, prepared `closeSession`, log synchronization, quorum commit, DataTree application, and observer awareness are separate milestones.
- **False-positive failure judgment under partition/pause:** the process can remain physically alive while its ZooKeeper session is no longer authoritative.
- **Delayed creator knowledge:** a disconnected creator may temporarily act on a stale belief that its session survives; applications must handle expiration as a separate state.
- **Stale observer knowledge:** watches are notifications, not the authoritative state itself.
- **Recovery-history over-retention:** old transaction/snapshot material can outlive current namespace membership until separate purge/reclamation policy removes it.
- **Lower-layer persistence:** logical deletion is not secure erase, block overwrite, Flash sanitize, cryptographic erase, or forensic disappearance.

## Prior art and novelty boundary

No invention-priority claim is made.

Mike Burrows's 2006 Chubby paper already documents:

- a session relation maintained by KeepAlive exchanges;
- session lease timeouts;
- ephemeral files used as indicators that a client is alive;
- deletion of ephemeral nodes when no client keeps them open.

That is enough to reject a claim that ZooKeeper originated the broad category `time-/session-qualified temporary coordination namespace state`.

The useful distinction is instead mechanistic: ZooKeeper's public early-release implementation and public 2009–2010 documentation tie each ephemeral znode to the **creating session**, preserve/reconstruct that relation across server recovery, and automatically remove session-owned ephemerals when the session terminates.

## Philosophical interpretation

### I — technical presence can be an actively maintained and reconstructible relation

A bounded philosophical reading is possible only after the mechanism is explicit:

> the continued technical presence of an ephemeral coordination object is not exhausted by the persistence of its bytes; it also depends on a maintained relation that says the creating session still counts as live, and that relation itself can be reconstructed from retained recovery evidence.

The same bytes can therefore lose current authority because the relation ends, without any claim that all historical traces were physically erased.

This does **not** identify ZooKeeper sessions with human memory, social belonging, Heideggerian presence, or Stieglerian retention. It is a narrow engineering counterexample to `physical survival = operational presence`.

## Source ledger

1. Apache ZooKeeper **3.1.2 Programmer's Guide**, release announced 14 December 2009: <https://zookeeper.apache.org/doc/r3.1.2/zookeeperProgrammers.html>.
   - `Ephemeral Nodes`: session-scoped lifetime and automatic deletion;
   - `ZooKeeper Stat Structure`: `ephemeralOwner` session ID;
   - `ZooKeeper Sessions`: reconnect/server-switch, session ID/password, PING keepalive.
2. Apache ZooKeeper **News**: <https://zookeeper.apache.org/news/>.
   - 27 October 2008: release 3.0.0 available;
   - 14 December 2009: release 3.1.2 available.
3. Patrick Hunt, Mahadev Konar, Flavio P. Junqueira, Benjamin Reed, **“ZooKeeper: Wait-free Coordination for Internet-scale Systems,”** USENIX ATC 2010, official paper: <https://www.usenix.org/events/usenix10/tech/full_papers/Hunt.pdf>.
   - §2.1: regular vs ephemeral znodes, sessions, session timeout, server migration;
   - §2.4: group membership and locks built with ephemerals;
   - §4.4: heartbeat/session failure detection and reconnect behavior.
4. Apache ZooKeeper **3.4.7 Programmer's Guide**: <https://zookeeper.apache.org/doc/r3.4.7/zookeeperProgrammers.html>.
   - session expiration is cluster-managed; expiration deletes session ephemerals; disconnected creator can learn expiration later.
5. Apache ZooKeeper **release-3.4.7 source**, annotated tag dated 21 November 2015:
   - `ZooKeeperServer.java`: <https://github.com/apache/zookeeper/blob/release-3.4.7/src/java/main/org/apache/zookeeper/server/ZooKeeperServer.java>;
   - `PrepRequestProcessor.java`: <https://github.com/apache/zookeeper/blob/release-3.4.7/src/java/main/org/apache/zookeeper/server/PrepRequestProcessor.java>;
   - `DataTree.java`: <https://github.com/apache/zookeeper/blob/release-3.4.7/src/java/main/org/apache/zookeeper/server/DataTree.java>.
6. Mike Burrows, **“The Chubby lock service for loosely-coupled distributed systems,”** OSDI 2006: <https://static.usenix.org/events/osdi06/tech/full_papers/burrows/burrows_html/>.
   - §§2.3, 2.8–2.9: ephemeral nodes, sessions/KeepAlives, lease/failover behavior; used only as prior-art and functional-boundary evidence.
7. Apache ZooKeeper **release-3.0.0** and **release-3.1.2** frozen source, inspected directly for the durability/restart deepening:
   - `ZooKeeperServer.java`, `PrepRequestProcessor.java`, `SyncRequestProcessor.java`, `DataTree.java`, `SerializeUtils.java`, `FileTxnSnapLog.java` in both baselines;
   - 3.1.2 quorum path additionally: `LeaderZooKeeperServer.java`, `ProposalRequestProcessor.java`, `Leader.java`, `Follower.java`, `FollowerZooKeeperServer.java`, `SendAckRequestProcessor.java`;
   - detailed file links and claim mapping are in [`../evidence/144-zookeeper-2008-2009-close-session-durability-recovery-deepening.md`](../evidence/144-zookeeper-2008-2009-close-session-durability-recovery-deepening.md).
8. Apache historical ZooKeeper distribution archive: <https://archive.apache.org/dist/hadoop/zookeeper/>.
   - custody corroboration for archived 3.0.0 and 3.1.2 source releases.

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `ZooKeeper ephemeral session` and `ZooKeeper closeSession ephemeral session transaction log` returned no dedicated reusable packet. Broader ZooKeeper/Chubby/Zab/session/failure-detector history, pre-Apache commit genealogy, and low-level filesystem durability archaeology belong there if developed; this case keeps the retention-specific liveness/recovery relation.

## Claim ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| ZooKeeper 3.1.2 documented ephemeral znodes as living while their creating session is active | H/P | Apache 3.1.2 Programmer's Guide | supported |
| an ephemeral znode exposes its creating session ID in `ephemeralOwner` | H/P | Apache 3.1.2 Programmer's Guide | supported |
| a session can move/reconnect among ZooKeeper servers without being identical to one TCP connection | H/P | Apache 3.1.2 guide; Hunt et al. 2010 | supported |
| lack of session traffic past timeout is used to decide session failure/expiration | H/P | Hunt et al. 2010; Apache 3.4.7 guide | supported |
| session expiration deletes associated ephemerals | H/P | Apache docs; Hunt et al.; frozen source | supported |
| archived ZooKeeper 3.0.0 already routes expiration through a zxid-bearing `closeSession` transaction | H/P | `release-3.0.0` source | supported |
| early snapshots retain live-session timeout state plus node `ephemeralOwner`, and restart rebuilds the owner index | H/P | 3.0.0/3.1.2 `SerializeUtils`, `DataTree`, `FileTxnSnapLog` | supported |
| restart removes restored ephemerals whose owner is absent from restored live-session state | H/P | 3.0.0/3.1.2 `ZooKeeperServer.loadData()` | supported |
| in the inspected 3.1.2 quorum path follower ACK follows local log sync and leader majority ACK causes commit | H/P | 3.1.2 quorum source | supported |
| one lost TCP connection immediately deletes all ephemerals | X | reconnect/session semantics | rejected |
| session timeout is simply a per-znode creation-time TTL | X | session semantics | rejected |
| ephemeral deletion proves the creator process no longer exists | X | timeout-based failure detection | rejected |
| timeout detection itself is identical to durable quorum commitment | X | staged 3.1.2 source path | rejected |
| persisted ephemeral bytes alone prove restart-time liveness authority | X | restored-session reconciliation | rejected |
| logical znode deletion proves secure media erasure | X | no lower-layer evidence; Case 71 boundary | rejected |
| ZooKeeper invented ephemeral/session-based coordination objects | X | Chubby 2006 prior art | rejected |

## Case findings

1. **Ephemeral payload persistence is conditional on session liveness.**
2. **Connection lifetime ≠ session lifetime.**
3. **Session lifetime ≠ process lifetime.**
4. **Session timeout ≠ per-object TTL.**
5. **`ephemeralOwner` relation metadata ≠ user payload or complete history.**
6. **Explicit close and timeout expiration can share cleanup machinery without sharing cause.**
7. **Authoritative deletion ≠ creator's immediate awareness.**
8. **Logical namespace retirement ≠ physical trace erasure.**
9. **ZooKeeper ephemeral semantics ≠ Chubby ephemeral semantics despite shared vocabulary.**
10. **Current-object liveness ≠ recovery-history retention.**
11. **Runtime owner-index loss ≠ durable ownership-relation loss: early source rebuilds it from persisted node metadata.**
12. **Expiration detected ≠ closeSession logged ≠ quorum committed ≠ DataTree deletion applied ≠ observer awareness.**
13. **Restored node survival ≠ restored liveness authority: owner-session membership is separately reconstructed and checked.**

## Maturity judgment

Case 144 is **grounded**, not `mature`.

The bounded mechanism is now supported by period official documentation, the 2010 implementation paper, later frozen source, and direct frozen-source archaeology back to the archived 3.0.0 public-release baseline. The early public-release `closeSession` persistence/replay path and the inspected 3.1.2 quorum log-sync/ACK/commit path are no longer open evidence debts.

Remaining work includes:

- exact pre-release commit archaeology for the first introduction of ephemeral znodes, `ephemeralOwner`, and `closeSession`;
- controlled crash/partition/pause/failover tests at the distinct boundaries of detection, log sync, quorum commit, DataTree application, and observer notification;
- exact operating-system/filesystem/storage durability semantics beneath the historical transaction-log `commit()` implementation;
- modern persistent-recursive watches / TTL-node/container-node contrasts;
- broader Chubby → ZooKeeper / Zab / failure-detector / coordination-service genealogy, which belongs primarily in `computing-archaeology`.
