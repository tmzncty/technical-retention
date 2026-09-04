# Apache HDFS Observer NameNode: State-ID Read Freshness Beyond Writer Authority

## Scope

- **Object / system:** Apache HDFS Observer NameNode and the client/server state-alignment mechanism developed under HDFS-12943;
- **Bounded implementation witness:** Apache Hadoop 3.3.0 release source for `ObserverReadProxyProvider`, `ClientGSIContext`, `GlobalStateIdContext`, and `ReadOnly`;
- **Historical window:** 2017–2020 for the design, implementation, bug-fix, and release evidence used here;
- **Why this case matters for technical retention:** an HDFS namespace replica may be physically present, internally coherent, and permitted to serve reads while still being too far behind the state a particular client is entitled to observe. HDFS therefore retains and transports a **state-ID lower bound** in addition to retaining the namespace itself.

This is not a general history of HDFS HA, replicated state machines, read replicas, or consistency models. It isolates a narrower retention problem:

> Once mutation authority and replica survival have already been established, what additional retained state is needed to decide whether a lagging replica is *fresh enough for this read*?

It complements rather than repeats three existing HDFS cases:

- [`Case 49`](49-apache-hdfs-generation-stamp-lease-recovery.md) asks which block replicas/recovery attempt are current after writer failure;
- [`Case 50`](50-apache-hdfs-qjm-epoch-fencing.md) asks which NameNode may continue writing the shared edit log;
- [`Case 51`](51-apache-hdfs-datanode-command-fencing.md) asks which connected NameNode may issue block-management commands to DataNodes.

Case 61 instead asks when a NameNode that **does not have mutation authority** may nevertheless answer a read without violating the bounded client-consistency contract.

A repository-tree check of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated HDFS Observer/`stateId` case at the time of this slice. No parallel Hadoop history is reproduced here.

---

## Historical vocabulary

The HDFS-12943 release note and later Apache user guide use the following actor vocabulary directly:

- `Active NameNode`;
- `Standby NameNode`;
- `Observer NameNode`;
- `state ID`;
- NameNode `transaction ID`;
- `read-after-write consistency` / `read your own writes`;
- `msync()` / `metadata sync`;
- `ObserverReadProxyProvider`;
- edit-log `tailing` and `Edit Tailing Fast-Path`.

The 3.3.0 source adds implementation vocabulary including `AlignmentContext`, `ClientGSIContext`, `GlobalStateIdContext`, `lastSeenStateId`, `isCoordinated`, `activeOnly`, and `ObserverRetryOnActiveException`.[^orpp][^client-gsi][^global-gsi][^readonly]

The phrases **client freshness frontier**, **read-admissibility lower bound**, and **retained observation frontier** below are engineering reconstructions. They are not presented as Apache's historical terminology.

---

## Architecture: a readable replica can intentionally lag

Traditional HDFS HA already had an Active NameNode and Standby NameNode(s). The Active handled client operations, while Standby nodes followed namespace edits from JournalNodes and received block-location information. HDFS-12943 introduced `Observer` as an additional HA state so a non-Active NameNode could serve client reads and offload read traffic from the Active.[^hdfs12943][^observer-guide]

This immediately creates a retention/currentness problem that writer fencing alone does not solve.

An Observer obtains namespace mutations by tailing the edit log. Therefore, at a given moment:

```text
Active last transaction ID      = N
Observer last applied txid      = N - d
```

where `d` may be zero or positive.

The Observer can hold a valid replica of the namespace and still lack the newest mutations already observed by a client. Apache's guide therefore treats edit-tail latency as directly related to Observer staleness and recommends fast in-progress edit tailing to reduce the interval between Active application and Observer application.[^observer-guide]

This yields the first boundary:

> **read-capable replica ≠ sufficiently fresh replica for every client.**

Replica existence and read permission are not enough; a read also needs an admissibility relation between what the client has already observed and what this Observer has applied.

---

## The client retains a monotonic lower bound

Apache Hadoop 3.3.0's `ClientGSIContext` stores `lastSeenStateId` in a `LongAccumulator(Math::max, Long.MIN_VALUE)`. Every RPC response carrying a state ID can advance that value, but an older response cannot move it backward. On later requests the client places the accumulated value into the RPC request header.[^client-gsi]

In the bounded implementation, the state ID is therefore not a copy of the whole namespace and not a client operation log. It is a compact monotonic statement:

```text
I have already observed namespace state at least through state ID S.
```

That retained scalar can constrain future reads. A later Observer response must not silently place the same client behind `S` for coordinated calls.

The retention relation is consequently:

```text
past accepted response
    ↓
client retains max state ID
    ↓
future request carries that lower bound
    ↓
server must align before the coordinated read is admitted
```

This supports several distinctions:

- **retained observation frontier ≠ retained operation history**;
- **one monotonic scalar ≠ a complete snapshot of namespace state**;
- **client-side currentness evidence ≠ server-side payload/metadata replica**.

The scalar matters because it changes which future server state is acceptable, not because it contains the namespace itself.

---

## Server-side alignment: local coherence is not enough

`GlobalStateIdContext` is the NameNode-side `AlignmentContext` implementation in the bounded 3.3.0 source. Its state ID comes from the NameNode's last applied or written transaction ID. For Observer requests, it compares the client's state ID with the server's current state ID.[^global-gsi]

Two source-level safeguards make the admission boundary concrete.

First, if an Observer receives a request with **no state ID**, it throws `StandbyException` rather than treating an unset/zero client frontier as permission to return a potentially stale result. The source explicitly describes this as protection for clients that are not configured with `ObserverReadProxyProvider`.[^global-gsi]

Second, if the client's state is so far ahead that the Observer is unlikely to catch up within the client's wait budget, the server throws a `RetriableException`. The request can then be retried against another Observer or the Active rather than waiting without bound.[^global-gsi]

HDFS-12943's release note states the positive rule: an Observer answers only after its own state has caught up with the state ID supplied by the client.[^hdfs12943]

Therefore:

> **internally consistent Observer state ≠ read-admissible Observer state for a client with a newer frontier.**

The missing relation is not “does this replica contain valid HDFS metadata?” but “has this replica reached at least the state already established for this client?”

---

## `stateId` is a freshness lower bound, not writer authority

It is tempting to call every monotonically increasing HDFS control number an `epoch`, `term`, or authority token. The surrounding HDFS cases show why that would be wrong.

Case 50's JournalNode `lastPromisedEpoch` is persisted acceptor-side refusal state. It determines which NameNode writer epochs JournalNodes will reject after failover.

Case 51's DataNode `lastActiveClaimTxId` is runtime command-authority recency state. It helps decide which NameNode may issue block-changing commands.

Case 61's client `lastSeenStateId` is different again. It is a **read-freshness floor** derived from NameNode transaction progress and carried through RPC headers.

These numbers are related only at a high functional level:

```text
lastPromisedEpoch     → who may mutate the shared edit log?
lastActiveClaimTxId   → whose DataNode commands are current?
client stateId        → how far must a read replica have caught up?
```

So:

> **writer fencing ≠ command authority ≠ read freshness.**

A NameNode can lack write authority and still be an admissible read server after its namespace state reaches the client's required frontier.

---

## `msync()`: importing an external freshness frontier

The per-client state ID naturally protects operations whose causal path goes through the same client. A write to the Active returns a newer state ID; that client retains it; a subsequent Observer read carries the newer lower bound.[^observer-guide]

But this does not automatically cover communication that happens outside HDFS.

Apache's user guide gives the explicit example of client `foo` performing a write and separately telling client `bar` about it through an out-of-band channel. `bar` has not received the state ID associated with `foo`'s write, so `bar` can otherwise make a valid but stale Observer read.[^observer-guide]

`msync()` closes that specific gap. In the final 3.3.0 client path, `ObserverReadProxyProvider` invokes `msync()` through the Active-side failover proxy to refresh the client's alignment state; later Observer reads then inherit the newer lower bound.[^orpp]

HDFS-13688 records the development of this API under HDFS-12943, while the released documentation describes its final role as updating the client's state ID against the Active so later Observer reads are consistent up to that point.[^hdfs13688][^observer-guide]

This gives another useful boundary:

> **replica catch-up ≠ client knowledge that catch-up is required.**

An Observer may eventually contain the new mutation, but the protocol cannot force a particular client to wait for that mutation unless the client has first acquired an appropriate freshness frontier.

---

## The 2019 startup bug: process ordering is not a retained causal chain

HDFS-14272 provides an unusually clear counterexample to naive reasoning about “later commands.” A shell script could run:

```text
hdfs dfs -touchz /tmp/abc
hdfs dfs -ls /tmp/abc
```

sequentially yet fail to find the just-created file through Observer reads. The second shell command started a new client that did not know the state ID returned to the first client, so the Observer had no reason to wait for those edits to propagate before answering.[^hdfs14272]

The fix required `ObserverReadProxyProvider` to synchronize with the Active when the client starts. In the 3.3.0 source, the first Observer read calls `initializeMsync()` exactly for this purpose; later reads can also use configurable auto-`msync` behavior.[^orpp]

This establishes:

> **wall-clock/program order across different client instances ≠ retained protocol causality.**

A human sees “command B happened after command A.” HDFS Observer consistency needs a state frontier that actually crosses that client boundary.

The failure was not evidence that the file's metadata had been lost. It was evidence that **the second client had not retained/imported the causal lower bound required to reject a stale-but-otherwise-valid read.**

---

## Freshness maintenance and read admission are separate work

The Observer mechanism has at least two distinct maintenance layers.

### 1. Replica advancement

Observer/Standby NameNodes tail edits from JournalNodes. The `Edit Tailing Fast-Path`, in-progress tailing, JournalNode cache, and tail period reduce the lag between Active state and Observer state.[^observer-guide]

### 2. Request alignment

The client retains a state ID, the request transports it, and coordinated Observer RPCs wait, retry, or fall back until a sufficiently current server can answer.[^hdfs12943][^global-gsi][^orpp]

Fast tailing lowers expected waiting time. It does **not** replace the consistency condition.

Conversely, a perfectly specified state-ID check cannot make a permanently lagging Observer become current; it can only wait, reject, or route elsewhere.

Therefore:

> **replica-maintenance speed ≠ read-admissibility criterion.**

This is analogous only at the functional level to other retention systems where “state exists” and “state is qualified for use” are separate. No claim of shared mechanism is implied.

---

## Read-only is still not one semantic class

The 3.3.0 `ReadOnly` annotation keeps two important flags separate:

- `activeOnly()` — a nominally read-only operation may still require information available only on the Active;
- `isCoordinated()` — only selected read operations require the server to wait for state alignment before processing.[^readonly]

`ObserverReadProxyProvider` likewise checks whether a method is eligible for Observer routing and sends write/noneligible work to the Active. If Observer attempts fail, it falls back to the Active.[^orpp]

This prevents another overgeneralization:

> **read-only operation ≠ Observer-eligible operation ≠ state-aligned read operation.**

The “read/write” distinction by itself is too coarse to describe currentness obligations.

The Apache guide supplies a concrete configuration-sensitive example: access-time updates can turn `getBlockLocations` into a write path, causing Observer attempts to fail back to the Active.[^observer-guide]

---

## Failure semantics: stale service is not the same as lost state

In this bounded case, several failures must remain distinct:

1. the Observer can be reachable but behind the client's state ID;
2. the Observer can be so far behind that the server chooses a retriable failure rather than waiting;
3. an Observer RPC can fail for transport or service reasons and the client can try another Observer;
4. after Observer attempts are exhausted, the proxy can fall back to the Active;
5. the namespace payload itself can still be durable in the journal/NameNode HA machinery even while one read path is temporarily inadmissible.[^global-gsi][^orpp]

Thus:

> **freshness failure ≠ namespace-data loss.**

A system can preserve the authoritative state while temporarily refusing to serve it through a particular replica because the retained currentness evidence is insufficient.

---

## Retention analysis

The case can be summarized as a chain of distinct retained or reconstructed state:

| Relation | What is retained / observed | What it does **not** mean |
| --- | --- | --- |
| namespace/edit state | Active + journal + tail-applied Observer namespace progress | every Observer is currently at the Active frontier |
| Observer server state ID | last applied/written transaction progress | mutation authority |
| client `lastSeenStateId` | monotonic lower bound from prior responses / `msync` | complete client history or complete namespace snapshot |
| RPC state-ID field | transports that lower bound to a candidate server | durable persistence across arbitrary new client processes |
| `msync()` result | refreshes a client's lower bound against the Active | forces all Observers instantly current |
| Observer HA state | allows a distinct read-serving role | permission to accept writes or participate as Active without transition |
| edit-tail fast path | reduces replica lag | replaces the state-alignment check |

The strongest retention-specific conclusion is:

> A distributed system may need to retain **how much of the authoritative past a client is already entitled to assume** in order to decide whether a surviving replica is admissible for future reads.

That retained relation can be tiny compared with the namespace itself, but still constitutive of correct service.

---

## Historical record, engineering reconstruction, functional analogy, philosophy

### Historical record

Supported directly here:

- HDFS-12943 introduced Observer as a read-serving NameNode state and state IDs in RPC headers for consistent reads;
- HDFS 3.3.0 source retains the client's maximum seen state ID and sends it on later requests;
- Observer server code compares client/server state IDs and rejects unsafe/unbounded cases;
- `ObserverReadProxyProvider` performs startup/optional `msync`, routes eligible reads to Observers, and falls back to Active;
- HDFS-14272 documents a real cross-client/startup freshness hole and the need for initial synchronization.

### Engineering reconstruction

The following are this repository's abstractions:

- `client freshness frontier`;
- `read-admissibility lower bound`;
- `retained observation frontier`;
- the separation `writer authority ≠ command authority ≠ read freshness`.

### Functional analogy

It is legitimate to compare this case with Kafka high-watermark/currentness, Dynamo version currentness, Raft follower progress, cache validity, or scrub-qualified replica use **only** at the level that a physically surviving copy may need additional state before it is safe to serve as current. The protocols, histories, guarantees, and failure models are not identical.

### Philosophy

No philosophical claim is required to establish this case. Any later synthesis about retention of “the already-seen past” must remain downstream of the concrete HDFS mechanism rather than being inserted as historical explanation.

---

## Prior-art and novelty boundary

This case does **not** claim that Apache HDFS invented:

- read replicas;
- follower/standby reads;
- transaction IDs;
- read-your-writes consistency;
- causal consistency;
- monotonic reads;
- client session state;
- or replicated-state-machine catch-up.

HDFS-12943 itself frames stale reads as a generic replicated-system problem, and the same JIRA links earlier HDFS work on allowing stale reads from Standby nodes. The bounded historical claim is narrower:

> By the HDFS-12943 / Hadoop 3.3.0 implementation, Apache composed NameNode transaction progress, RPC-carried client state IDs, Observer catch-up gating, `msync()`, Observer-aware proxy routing, and edit-log tailing into a concrete HDFS read-freshness mechanism.

That composition is the object of this case.

---

## Comparison with adjacent cases

### Case 50 — QJM epoch fencing

- retains a durable writer-promise floor in JournalNodes;
- prevents stale NameNodes from successfully extending the shared edit log;
- can remain necessary even if the stale process is alive.

Case 61 assumes that mutation authority is already handled and asks whether a read replica is sufficiently current.

### Case 51 — DataNode command fencing

- chooses which connected NameNode may issue block-management commands;
- separately retains/revalidates replica-inventory freshness after failover.

Case 61 concerns namespace-read admissibility for a client, not DataNode command execution.

### Case 56 — Kafka high watermark

- the broker protocol derives a committed prefix from replica progress and ISR membership;
- ordinary consumer visibility is capped at that global-ish partition frontier in the bounded Kafka case.

HDFS Observer state ID instead records a **client-specific lower bound** that a candidate read replica must have reached. The mechanisms must not be collapsed.

### Case 23 — Dynamo divergent versions

- multiple concurrent versions can remain simultaneously admissible and require reconciliation;
- read repair/anti-entropy address divergent object state.

HDFS Observer is not reconciling concurrent namespace versions in this case; it is waiting for one journal-ordered state machine replica to catch up to a required transaction frontier.

---

## Open work intentionally left outside this slice

- exact HDFS-12943 design-PDF page archaeology and proposal-version evolution;
- Router-Based Federation Observer-read state propagation;
- post-3.3 Observer consistency regressions and fixes;
- WebHDFS and delegation-token-specific behavior;
- end-to-end file-data visibility versus NameNode metadata freshness;
- interaction with snapshots, encryption zones, access-time configuration, and other operation classes;
- independent fault injection measuring stale-read/fallback behavior;
- broader comparison with follower reads in ZooKeeper, Raft-based databases, Spanner-like systems, or object stores.

These are follow-on slices, not blockers for the bounded mechanism established here.

---

## Status

**grounded** — Apache JIRA/release records, Apache user documentation, and release-3.3.0 source directly establish the Observer role, RPC state-ID mechanism, client monotonic state retention, server alignment checks, `msync`, routing/fallback, and the 2019 startup/cross-client freshness failure. No invention-priority claim is made.

[^hdfs12943]: Apache Hadoop JIRA, [HDFS-12943 — Consistent Reads from Standby Node](https://issues.apache.org/jira/browse/HDFS-12943), created 19 December 2017, resolved 1 November 2019; release note and subtasks inspected.
[^observer-guide]: Apache Hadoop, [Consistent Reads from HDFS Observer NameNode](https://hadoop.apache.org/docs/r3.2.3/hadoop-project-dist/hadoop-hdfs/ObserverNameNode.html), Hadoop 3.2.3 documentation; architecture, client consistency, tailing, deployment, and client configuration sections inspected.
[^hdfs13688]: Apache Hadoop JIRA, [HDFS-13688 — Introduce msync API call](https://issues.apache.org/jira/browse/HDFS-13688), HDFS-12943 subtask.
[^hdfs14272]: Apache Hadoop JIRA, [HDFS-14272 — ObserverReadProxyProvider should sync with active txnID on startup](https://issues.apache.org/jira/browse/HDFS-14272), resolved 1 March 2019.
[^orpp]: Apache Hadoop 3.3.0 source, [`ObserverReadProxyProvider.java`](https://github.com/apache/hadoop/blob/rel/release-3.3.0/hadoop-hdfs-project/hadoop-hdfs-client/src/main/java/org/apache/hadoop/hdfs/server/namenode/ha/ObserverReadProxyProvider.java).
[^client-gsi]: Apache Hadoop 3.3.0 source, [`ClientGSIContext.java`](https://github.com/apache/hadoop/blob/rel/release-3.3.0/hadoop-hdfs-project/hadoop-hdfs-client/src/main/java/org/apache/hadoop/hdfs/ClientGSIContext.java).
[^global-gsi]: Apache Hadoop 3.3.0 source, [`GlobalStateIdContext.java`](https://github.com/apache/hadoop/blob/rel/release-3.3.0/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/GlobalStateIdContext.java).
[^readonly]: Apache Hadoop 3.3.0 source, [`ReadOnly.java`](https://github.com/apache/hadoop/blob/rel/release-3.3.0/hadoop-hdfs-project/hadoop-hdfs-client/src/main/java/org/apache/hadoop/hdfs/server/namenode/ha/ReadOnly.java).
