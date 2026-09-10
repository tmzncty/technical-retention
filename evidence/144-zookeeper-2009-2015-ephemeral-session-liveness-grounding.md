# Evidence 144 — ZooKeeper ephemeral znodes, session-scoped liveness, and timeout-qualified retirement (2009–2015)

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
