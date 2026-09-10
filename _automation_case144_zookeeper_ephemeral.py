from pathlib import Path
import re

CASE_PATH = Path('cases/144-zookeeper-ephemeral-session-liveness.md')
EVIDENCE_PATH = Path('evidence/144-zookeeper-2009-2015-ephemeral-session-liveness-grounding.md')

CASE = r'''# Apache ZooKeeper Ephemeral Znodes: Session-Scoped Liveness, Timeout-Qualified Retirement, and Logical Deletion

## Status

**`grounded`** — bounded to ZooKeeper's documented/session-implementation relation among a live client session, an ephemeral znode, timeout-based session termination, and automatic logical deletion. The historical floor is Apache ZooKeeper 3.1.2 (released 14 December 2009) plus the 2010 USENIX ATC ZooKeeper paper; release-3.4.7 source is used as a later implementation witness.

Grounding record: [`../evidence/144-zookeeper-2009-2015-ephemeral-session-liveness-grounding.md`](../evidence/144-zookeeper-2009-2015-ephemeral-session-liveness-grounding.md).

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

> **ZooKeeper makes object liveness depend on a retained session-to-znode relation rather than on byte age or one TCP connection. That relation can survive reconnection, can be retired by an explicit or timeout-qualified session termination, and can disappear logically while lower-level recovery history may still preserve traces of the old state.**

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
7. **snapshot/transaction-log recovery history** — a separate persistence layer treated in Case 71, not the same thing as namespace liveness.

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

The release-3.4.7 implementation routes detected expiration through `closeSession`, and explicit session closure also uses that operation. This supports a common state-retirement mechanism.

It does **not** erase the distinction between:

- administrator/application-intended close;
- timeout-based service inference;
- transport disconnection before timeout.

### E — retirement completion != observer awareness

A disconnected creator may learn of expiration only after reconnecting. State authority therefore belongs to the ensemble's session decision, not to a synchronous acknowledgement held by the creator.

### E — logical ephemeral deletion != disappearance of historical recovery material

Case 71 grounds ZooKeeper's separate transaction-log/snapshot recovery set. In release-3.4.7, closeSession itself receives a zxid and drives znode deletion. It is therefore unsafe to infer that deleting an ephemeral from the **current namespace** proves the corresponding creation/data bytes have already vanished from every older log, snapshot, backup, filesystem block, or storage medium.

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

These can point in opposite directions:

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
- **Session timeout / explicit close:** retires session-scoped ephemeral liveness.
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

The useful distinction is instead mechanistic: ZooKeeper's public 2009–2010 contract ties each ephemeral znode to the **creating session**, exposes that relation as `ephemeralOwner`, and automatically removes session-owned ephemerals when the session terminates.

## Philosophical interpretation

### I — technical presence can be an actively maintained relation

A bounded philosophical reading is possible only after the mechanism is explicit:

> the continued technical presence of an ephemeral coordination object is not exhausted by the persistence of its bytes; it also depends on a maintained relation that says the creating session still counts as live.

The same bytes can therefore lose current authority because the relation ends, without any claim that all historical traces were physically erased.

This does **not** identify ZooKeeper sessions with human memory, social belonging, Heideggerian presence, or Stieglerian retention. It is a narrow engineering counterexample to `physical survival = operational presence`.

## Source ledger

1. Apache ZooKeeper **3.1.2 Programmer's Guide**, release announced 14 December 2009: <https://zookeeper.apache.org/doc/r3.1.2/zookeeperProgrammers.html>.
   - `Ephemeral Nodes`: session-scoped lifetime and automatic deletion;
   - `ZooKeeper Stat Structure`: `ephemeralOwner` session ID;
   - `ZooKeeper Sessions`: reconnect/server-switch, session ID/password, PING keepalive.
2. Apache ZooKeeper **News**, 14 December 2009: <https://zookeeper.apache.org/news/>.
   - dates 3.1.2 availability.
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

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `ZooKeeper ephemeral session` returned no dedicated study before drafting. Broader ZooKeeper/Chubby/session/failure-detector history belongs there if developed; this case keeps the retention-specific liveness relation.

## Claim ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| ZooKeeper 3.1.2 documented ephemeral znodes as living while their creating session is active | H/P | Apache 3.1.2 Programmer's Guide | supported |
| an ephemeral znode exposes its creating session ID in `ephemeralOwner` | H/P | Apache 3.1.2 Programmer's Guide | supported |
| a session can move/reconnect among ZooKeeper servers without being identical to one TCP connection | H/P | Apache 3.1.2 guide; Hunt et al. 2010 | supported |
| lack of session traffic past timeout is used to decide session failure/expiration | H/P | Hunt et al. 2010; Apache 3.4.7 guide | supported |
| session expiration deletes associated ephemerals | H/P | Apache docs; Hunt et al.; release-3.4.7 source | supported |
| release-3.4.7 routes expiration through a zxid-bearing `closeSession` transaction and `killSession` | H/P | 3.4.7 source | supported |
| one lost TCP connection immediately deletes all ephemerals | X | reconnect/session semantics | rejected |
| session timeout is simply a per-znode creation-time TTL | X | session semantics | rejected |
| ephemeral deletion proves the creator process no longer exists | X | timeout-based failure detection | rejected |
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

## Maturity judgment

Case 144 is **grounded**, not `mature`.

The bounded mechanism is supported by period official documentation, the 2010 implementation paper, and later frozen release source. Remaining work includes:

- exact first ZooKeeper commit/release that introduced ephemeral znodes and `ephemeralOwner`;
- frozen pre-3.1 source archaeology for the original session/ephemeral implementation;
- exact Zab/log durability path for close-session across the earliest releases;
- controlled partition/pause/failover tests measuring expiration and observer timing;
- modern persistent-recursive watches / TTL-node/container-node contrasts;
- broader Chubby → ZooKeeper / failure-detector / coordination-service genealogy, which belongs primarily in `computing-archaeology`.
'''

EVIDENCE = r'''# Evidence 144 — ZooKeeper ephemeral znodes, session-scoped liveness, and timeout-qualified retirement (2009–2015)

## Case

[`cases/144-zookeeper-ephemeral-session-liveness.md`](../cases/144-zookeeper-ephemeral-session-liveness.md)

## Evidence status

**Grounded for the bounded session → ephemeral-znode liveness → automatic-retirement relation.**

This record deliberately separates four things that are easy to collapse:

```text
TCP/server connection
    != ZooKeeper session
    != ephemeral znode's current namespace liveness
    != lower-layer persistence of historical bytes
```

It also distinguishes a timeout-qualified service judgment from proof that a client process has ceased to exist.

Claim labels follow [`docs/METHOD.md`](../docs/METHOD.md):

- **H** — historical record;
- **P** — primary / first-party technical evidence;
- **E** — engineering reconstruction;
- **A** — functional analogy/comparison;
- **I** — bounded philosophical interpretation;
- **X** — explicit exclusion / unsupported stronger claim.

## Sources

### P1 — Apache ZooKeeper 3.1.2 Programmer's Guide (release available 14 December 2009)

Apache Software Foundation, **ZooKeeper Programmer's Guide, release 3.1.2**:

<https://zookeeper.apache.org/doc/r3.1.2/zookeeperProgrammers.html>

Apache project news dates 3.1.2 availability to **14 December 2009**:

<https://zookeeper.apache.org/news/>

Relevant source statements:

- `Ephemeral Nodes`: ephemeral znodes exist as long as the session that created them is active and are deleted when the session ends;
- `ZooKeeper Stat Structure`: `ephemeralOwner` is the session ID of the owner if the znode is ephemeral, otherwise zero;
- `ZooKeeper Sessions`: a client reconnecting to a different server sends its session ID and password; requests/PING traffic keeps the session alive.

Evidence strength: **strong period first-party documentation**.

Chronology limit: the dated 3.1.2 release proves the feature was publicly documented by December 2009, not that 3.1.2 introduced it.

### P2 — Hunt et al., USENIX ATC 2010

Patrick Hunt, Mahadev Konar, Flavio P. Junqueira, Benjamin Reed, **“ZooKeeper: Wait-free Coordination for Internet-scale Systems,”** USENIX Annual Technical Conference, presented 24 June 2010:

<https://www.usenix.org/events/usenix10/tech/full_papers/Hunt.pdf>

Official conference record:

<https://www.usenix.org/conference/usenix-atc-10/zookeeper-wait-free-coordination-internet-scale-systems>

Relevant locations:

- §2.1, pp. 2–3: regular vs ephemeral znodes; ephemeral nodes are removed automatically when the creating session terminates; watches are also session-associated;
- §2.1, p. 2: sessions have timeouts, end on explicit close or detected fault, and allow transparent movement across ZooKeeper servers;
- §2.4, pp. 4–5: ephemeral nodes implement group membership and lock recipes;
- §4.4, p. 9: timeout-based session failure detection, heartbeat traffic, and reconnection to another server before timeout.

Evidence strength: **strong contemporary implementation paper from the ZooKeeper authors, published by USENIX**.

### P3 — Apache ZooKeeper 3.4.7 Programmer's Guide

Apache Software Foundation, **ZooKeeper Programmer's Guide, release 3.4.7**:

<https://zookeeper.apache.org/doc/r3.4.7/zookeeperProgrammers.html>

The guide states that session expiration is managed by the ZooKeeper cluster. The negotiated timeout is used to decide expiration when no heartbeat/session traffic is heard. At expiration the cluster deletes ephemerals owned by the session and notifies connected watchers; the expired/disconnected client may not learn this until it later reconnects.

Evidence strength: **strong later first-party contract witness**.

It is not used as evidence that every timing detail was identical in 2009.

### P4 — Apache ZooKeeper release-3.4.7 frozen source

Annotated release tag `release-3.4.7`, tag date **21 November 2015**, commit `b3119273f9a16274ed9e1f87418a765b130e1063`.

Source locations:

- `src/java/main/org/apache/zookeeper/server/ZooKeeperServer.java`
  <https://github.com/apache/zookeeper/blob/release-3.4.7/src/java/main/org/apache/zookeeper/server/ZooKeeperServer.java>
- `src/java/main/org/apache/zookeeper/server/PrepRequestProcessor.java`
  <https://github.com/apache/zookeeper/blob/release-3.4.7/src/java/main/org/apache/zookeeper/server/PrepRequestProcessor.java>
- `src/java/main/org/apache/zookeeper/server/DataTree.java`
  <https://github.com/apache/zookeeper/blob/release-3.4.7/src/java/main/org/apache/zookeeper/server/DataTree.java>

Observed implementation chain:

```text
ZooKeeperServer.expire(session)
    -> close(sessionId)
    -> submit OpCode.closeSession

PrepRequestProcessor
    -> create/close session go through pRequest2Txn(... getNextZxid ...)
    -> collects session ephemerals / marks closing

DataTree.processTxn(closeSession)
    -> killSession(sessionId, zxid)
    -> remove session's ephemeral-path set
    -> deleteNode(path, zxid) for each surviving ephemeral
```

Evidence strength: **strong frozen first-party implementation witness**.

Version limit: source-level statements apply to release-3.4.7 unless older source is separately verified.

### P5 — Burrows, Chubby OSDI 2006 prior art / counterexample

Mike Burrows, **“The Chubby lock service for loosely-coupled distributed systems,”** OSDI 2006:

<https://static.usenix.org/events/osdi06/tech/full_papers/burrows/burrows_html/>

Relevant sections:

- §2.3: Chubby nodes may be permanent or ephemeral; an ephemeral node is deleted when no client has it open (and a directory must also be empty), and ephemeral files can indicate that a client is alive;
- §2.8: sessions are maintained with KeepAlive handshakes and an associated session lease timeout;
- §2.9: failover can preserve session relations through a grace interval.

Evidence strength: **strong earlier system paper**.

Use limit: this is prior-art/counterexample evidence, not evidence of direct Chubby → ZooKeeper code or design genealogy.

## Historical record

### H/P — public ZooKeeper documentation already tied ephemeral lifetime to creating session in 2009

P1 supplies a dated lower bound. The important relation is explicit:

```text
creating session active
    -> ephemeral znode remains
session ends
    -> znode deleted
```

P1 also exposes `ephemeralOwner`, making the session-to-object relation visible in the znode's stat metadata.

This is not an object-age retention timer.

### H/P — the 2010 authors used ephemerals as a liveness-qualified coordination primitive

P2's group-membership example creates one ephemeral child per group member. The paper explains that when the represented process fails or ends, the znode is automatically removed. The lock recipes likewise use `EPHEMERAL` so abandoned lock requests/locks can be cleaned up.

This grounds a production-oriented use of **continued presence as a session-conditioned statement**.

It does not prove perfect failure detection.

### H/P — session validity is deliberately wider than one connection

P1/P2 document reconnecting a session to a different server. P2 says sessions persist across ZooKeeper servers and explains client heartbeat/reconnect timing.

Therefore a transient server/socket failure is not itself the authoritative deletion event.

### H/P — timeout is the service's failure-admission rule

P2 says ZooKeeper considers a client faulty after it receives nothing from that session beyond the timeout. P3 makes expiration a cluster-managed decision and ties it to automatic ephemeral deletion.

The safe claim is:

> absence of session traffic beyond the negotiated bound authorizes retirement of session-scoped objects.

The unsafe stronger claim is:

> ZooKeeper has proved the client process is physically dead.

### H/P — 3.4.7 source records expiration as a normal state-change path, not mere local socket cleanup

P4 matters because it shows a service-level chain. `expire()` submits `closeSession`; the request is assigned a zxid by the preparation pipeline; processing a close-session transaction removes the session's ephemerals from the data tree.

This supports the engineering distinction:

```text
local transport teardown
    !=
ordered ZooKeeper session-retirement state transition
```

The exact Zab persistence/replication proof for this transition is outside this bounded evidence file.

### H/P — state authority can change before the disconnected creator learns it

P3 explicitly says the expired session's client may still be disconnected when the cluster removes its ephemerals; the client learns expiration only if/when it re-establishes connectivity.

Thus notification latency is not the definition of state currentness.

## Engineering reconstruction

### E1 — ephemeral liveness is a retained relation, not a property of bytes alone

At least four layers must remain distinct:

```text
znode bytes/name/stat
session identifier
session-validity / timeout state
session -> ephemeral ownership relation
```

The object stays current only while the service continues to accept the session relation. Physical bytes alone do not define that currentness.

### E2 — object age != session expiry

No cited source says that an ephemeral is removed N seconds after creation. A session that continues heartbeats can keep the same znode alive beyond many timeout intervals.

Therefore:

```text
session timeout != creation-time TTL
```

### E3 — connection loss != session loss

The client can reconnect to another server before the session expires. The retained session identity bridges transport replacement.

This makes the session itself a continuity relation across changing server/connection embodiments.

### E4 — service-qualified liveness != physical process existence

Timeout failure detection is epistemic/operational: the ensemble has not heard from the session. A partitioned, paused, overloaded, or otherwise unreachable process may still execute locally after its session has been retired.

Applications using an ephemeral node as membership evidence therefore consume **ZooKeeper's current liveness judgment**, not a perfect sensor of process existence.

### E5 — `ephemeralOwner` != complete session history

The session ID is enough to bind object lifetime to a session, but does not preserve all heartbeat times, prior connections, causal history, or application semantics. It is bounded current control metadata.

### E6 — same cleanup path != same initiating event

Release-3.4.7 sends both explicit close and timeout-driven expiration toward `closeSession`. This common retirement mechanism does not make explicit intent and inferred failure the same historical event.

### E7 — deletion currentness != deletion awareness

If the creator is disconnected, the service can already have retired its session and ephemerals while the creator has not yet received the expiration event. Currentness is therefore not defined by symmetric knowledge among participants.

### E8 — logical deletion != secure erasure or immediate history disappearance

Case 71 separately grounds transaction-log and snapshot recovery history. A current ephemeral can be removed from the namespace while old logs/snapshots/backups remain subject to their own retention and purge schedules.

This evidence record makes no claim about whether a particular prior znode payload remains recoverable from any specific device after deletion.

## Prior art and functional boundary

### A/P — Chubby prevents an invention shortcut but supplies a useful counterexample

P5 predates P1/P2 and already has both:

- session/KeepAlive state;
- ephemeral namespace objects used as liveness indicators.

But Chubby's ephemeral deletion predicate is **open-handle/reference based**, not ZooKeeper's `creating session remains active` rule.

So:

```text
Chubby ephemeral file
    ~ functional class: temporary coordination/liveness state
    !=
ZooKeeper ephemeral znode state machine
```

This is exactly why the repository must keep historical vocabulary and mechanism together rather than normalize by modern category labels.

## Cross-case comparison

### A — Case 71 fuzzy snapshots / replay

Case 71 is a recovery-retention case: an imperfect snapshot remains usable when enough ordered log history survives.

Case 144 is an authority-liveness case: the service deliberately removes a currently visible object when its session relation ends.

Together they produce a useful anti-collapse:

```text
logical current-state forgetting
    can happen before
historical recovery-material reclamation
```

No claim is made that every deleted ephemeral remains recoverable in practice.

### A — Case 141 PostgreSQL replication slots

Both systems let a relation outlive one connection:

```text
ZooKeeper: session may outlive server/socket attachment
PostgreSQL: slot/WAL obligation may outlive consumer connection
```

But they preserve different futures. ZooKeeper session state supports current coordination membership until timeout; PostgreSQL slot state preserves replay continuity/history until policy invalidates the claim.

`connection-independent relation` is the analogy; storage/history semantics are not.

## Philosophical interpretation — bounded

### I — presence is conditional on maintained authority

The engineering record supports one restrained interpretive sentence:

> a technical object may remain materially represented yet cease to count as present/current for the system because the relation that authorized its presence has ended.

The opposite is also possible: a session relation can bridge changing network connections and keep the object present without rewriting its payload.

Nothing here establishes a theory of human memory, consciousness, social membership, or metaphysical presence.

## Anti-anachronism and negative claims

This slice does **not** establish:

- that ZooKeeper 3.1.2 introduced ephemeral nodes;
- the exact first ZooKeeper commit containing `ephemeralOwner`;
- that the 3.4.7 internal implementation was byte-for-byte or state-machine identical in 2009;
- that `session timeout` should be renamed `TTL` or `lease` in historical ZooKeeper vocabulary;
- that a disconnected process is physically dead when ZooKeeper expires its session;
- that ZooKeeper watches define the authoritative deletion event;
- that every closeSession detail is independently proved crash-durable by this source set;
- that Chubby's ephemeral-file semantics are the direct ancestor or implementation model of ZooKeeper ephemerals;
- that logical deletion removes all log/snapshot/backup/media traces;
- that session-scoped presence is equivalent to secure deletion, GC, or filesystem unlink semantics.

## Related-repository boundary

A fresh `tmzncty/computing-archaeology` search for `ZooKeeper ephemeral session` returned no dedicated result before drafting.

If developed later, these belong primarily in `computing-archaeology`:

- exact ZooKeeper feature-introduction commits and release genealogy;
- Chubby/ZooKeeper/Boxwood/etcd coordination-service lineage;
- failure-detector theory and implementation history;
- Zab/session replication implementation archaeology;
- evolution of TTL/container nodes and persistent-recursive watches.

`technical-retention` keeps only the bounded relation needed here:

> **a session-scoped object can survive transport replacement, remain current while a separate liveness relation is refreshed, and be retired automatically when that relation is explicitly closed or times out.**

## Readiness

This evidence slice is complete enough to mark Case 144 `grounded` because it has:

- a dated 2009 official ZooKeeper documentation floor;
- the 2010 author/system paper with session and ephemeral-node semantics plus concrete group-membership use;
- a later official programmer guide with explicit cluster-side expiration behavior;
- frozen release-3.4.7 source confirming the closeSession/ephemeral-deletion implementation chain;
- a 2006 Chubby primary-system counterexample/prior-art boundary;
- explicit failure, maintenance, awareness, recovery-history, and sanitization limits;
- a fresh related-repository duplication check.
'''

CASE_PATH.parent.mkdir(parents=True, exist_ok=True)
EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
if CASE_PATH.exists() or EVIDENCE_PATH.exists():
    raise SystemExit('Case 144 path already exists; refusing duplicate work')
CASE_PATH.write_text(CASE, encoding='utf-8')
EVIDENCE_PATH.write_text(EVIDENCE, encoding='utf-8')

# Update CASE_INDEX table immediately after Case 143.
ip = Path('CASE_INDEX.md')
ci = ip.read_text(encoding='utf-8')
if 'cases/144-zookeeper-ephemeral-session-liveness.md' in ci or '## Case 144 — ZooKeeper ephemeral-session findings' in ci:
    raise SystemExit('Case 144 already indexed; refusing duplicate integration')
nums = [int(x) for x in re.findall(r'(?m)^- \*\*(\d+) —', ci)]
if not nums or max(nums) != 3100:
    raise SystemExit(f'unexpected finding max {max(nums) if nums else None}; concurrent research likely landed')
row = '| [Apache ZooKeeper Ephemeral Znodes: Session-Scoped Liveness, Timeout-Qualified Retirement, and Logical Deletion](cases/144-zookeeper-ephemeral-session-liveness.md) | **grounded** | ephemeral znode payload/stat + creating-session identity + negotiated timeout/heartbeat state + `ephemeralOwner` relation + close/expiration transaction | separate transport connection from session continuity; object age from session timeout; service-qualified liveness from physical process existence; logical retirement from observer awareness and lower-layer erasure | [2009–2015 ZooKeeper grounding](evidence/144-zookeeper-2009-2015-ephemeral-session-liveness-grounding.md); exact feature-introduction genealogy, earliest source path, closeSession durability archaeology, partition/failover timing tests, and later TTL/container-node comparison remain open |'
lines = ci.splitlines()
anchor = next((i for i, x in enumerate(lines) if 'cases/143-sqlite3-rollback-journal-hot-recovery-authority.md' in x and x.startswith('| [')), None)
if anchor is None:
    raise SystemExit('Case 143 table anchor missing')
lines.insert(anchor + 1, row)
ci = '\n'.join(lines).rstrip() + '\n'

findings = [
    ('2009 public documentation floor != feature-introduction date', 'Apache dates ZooKeeper 3.1.2 to 14 December 2009 and that guide already documents session-scoped ephemeral deletion; it does not prove 3.1.2 introduced the feature. (`H/P`, `X`)'),
    ('ephemeral znode lifetime != znode age', 'the bounded contract ties continued existence to the creating session remaining active rather than to elapsed time since znode creation. (`H/P`, `E`)'),
    ('session timeout != per-object TTL', 'ongoing session traffic can keep old ephemerals alive across arbitrarily many timeout intervals; timeout qualifies the shared session relation, not each znode age. (`H/P`, `E`, `X`)'),
    ('transport connection lifetime != session lifetime', 'clients can reconnect the same session to another ZooKeeper server before timeout, so one broken socket/server attachment does not itself retire ephemerals. (`H/P`, `E`)'),
    ('session lifetime != process lifetime', 'ZooKeeper can expire a silent/unreachable session after timeout even if the client process still physically exists behind a partition or pause. (`H/P`, `E`, `X`)'),
    ('`ephemeralOwner` relation metadata != payload', 'the stat field retains the creating session ID used to bind liveness but is neither another payload copy nor a complete session/heartbeat history. (`H/P`, `E`)'),
    ('session validity is constitutive currentness state for ephemerals', 'physically represented znode data does not by itself establish current namespace liveness once its creating session has been retired. (`E`)'),
    ('explicit close != timeout inference despite common cleanup path', 'release-3.4.7 routes expiration through `closeSession`, but deliberate termination and service-side timeout remain different initiating conditions. (`H/P`, `E`)'),
    ('closeSession is a state transition != local socket cleanup', 'release-3.4.7 assigns create/close-session processing a zxid and `DataTree.killSession` deletes associated ephemerals under that transition. (`H/P`, `E`)'),
    ('authoritative deletion != creator awareness', 'a disconnected creator can learn that its session expired only after later connectivity, while the cluster may already have removed its ephemerals. (`H/P`, `E`)'),
    ('watch/notification state != liveness authority', 'observer delivery reports a change but does not define whether the session-owned znode is still current. (`H/P`, `E`)'),
    ('group-membership znode != perfect failure detector', 'the 2010 group-membership recipe exposes the service timeout judgment; it does not prove ontological process death. (`H/P`, `E`, `X`)'),
    ('ZooKeeper ephemeral != Chubby ephemeral by shared vocabulary', 'Chubby 2006 deletes ephemerals based on open handles/reference state, while ZooKeeper ties an ephemeral to the creating session; this is prior-art/functional comparison, not one state machine. (`H/P`, `A`, `X`)'),
    ('Chubby prior art != ZooKeeper genealogy', 'the 2006 Chubby record blocks an invention shortcut for temporary coordination/liveness objects without proving direct design or code descent. (`H/P`, `X`)'),
    ('namespace retirement != recovery-history reclamation', 'Case 71 separately grounds transaction-log/snapshot retention, so a deleted current ephemeral need not imply every older recovery representation was already reclaimed. (`A`, `E`)'),
    ('logical ephemeral deletion != media sanitization', 'session expiration/close does not establish block overwrite, Flash erase, cryptographic erase, or forensic disappearance. (`E`, `X`)'),
    ('connection-independent relation has typed semantics', 'ZooKeeper sessions and PostgreSQL replication slots can both outlive one connection, but one qualifies current coordination liveness while the other preserves future replay history. (`A`, `X`)'),
    ('related-repository boundary', 'a fresh `tmzncty/computing-archaeology` search for `ZooKeeper ephemeral session` found no dedicated study; broad coordination-service/failure-detector genealogy belongs there, while this case keeps the session-scoped retention relation. (`H/P` project-state record)'),
]
out = ['', '## Case 144 — ZooKeeper ephemeral-session findings', '', 'Grounding record: [`evidence/144-zookeeper-2009-2015-ephemeral-session-liveness-grounding.md`](evidence/144-zookeeper-2009-2015-ephemeral-session-liveness-grounding.md).', '']
for n, (title, body) in enumerate(findings, start=3101):
    out.append(f'- **{n} — {title}:** {body}')
ip.write_text(ci.rstrip() + '\n' + '\n'.join(out) + '\n', encoding='utf-8')

# Update ROADMAP immediately after the previous new-case slice where possible.
rp = Path('ROADMAP.md')
rm = rp.read_text(encoding='utf-8')
key = 'Case 144 ZooKeeper ephemeral-znode session-liveness / automatic-retirement slice'
if key in rm:
    raise SystemExit('Case 144 already present in ROADMAP')
bullet = "- [x] Case 144 ZooKeeper ephemeral-znode session-liveness / automatic-retirement slice — [`cases/144-zookeeper-ephemeral-session-liveness.md`](cases/144-zookeeper-ephemeral-session-liveness.md) + [`evidence/144-zookeeper-2009-2015-ephemeral-session-liveness-grounding.md`](evidence/144-zookeeper-2009-2015-ephemeral-session-liveness-grounding.md): Apache's 14-Dec-2009 ZooKeeper 3.1.2 documentation and the 2010 USENIX paper ground ephemeral znodes whose current namespace lifetime follows the creating session rather than object age or one transport connection; release-3.4.7 source later confirms timeout expiration feeding a zxid-bearing `closeSession` path that removes session-owned ephemerals. Chubby 2006 supplies earlier temporary/liveness-object prior art while also providing a counterexample because its ephemeral-file predicate is open-handle based rather than ZooKeeper's creating-session rule. This closes only the bounded `connection vs session vs object liveness vs logical deletion` relation; exact introduction commits, early Zab/session source archaeology, partition/failover timing tests, later TTL/container-node comparison, and broader coordination-service genealogy remain open and belong primarily in `computing-archaeology`."
rm_lines = rm.splitlines()
prev = next((i for i, x in enumerate(rm_lines) if 'Case 143 SQLite 3 rollback-journal hot-recovery / commit-invalidation slice' in x), None)
if prev is None:
    h = '## Phase 2 — Build missing technical bridges'
    prev = next((i for i, x in enumerate(rm_lines) if x.strip() == h), None)
    if prev is None:
        raise SystemExit('ROADMAP Phase2 anchor missing')
rm_lines.insert(prev + 1, bullet)
rp.write_text('\n'.join(rm_lines).rstrip() + '\n', encoding='utf-8')

# Clean temporary integration scaffolding from the final tree.
Path('_automation_case144_zookeeper_ephemeral.py').unlink(missing_ok=True)
Path('.github/workflows/tmp-case144-zookeeper-ephemeral.yml').unlink(missing_ok=True)
