# Evidence record — HDFS Observer NameNode state-ID read freshness, 2017–2020

## Purpose

This record grounds [`Case 61`](../cases/61-apache-hdfs-observer-stateid-read-freshness.md) in Apache primary project records, release documentation, and Apache Hadoop 3.3.0 source.

The bounded research question is:

> How does HDFS distinguish a NameNode replica that exists and can serve reads from a replica that is sufficiently current for a particular client's read?

The answer used by this case is **not** reduced to “Observer is eventually consistent.” The evidence establishes a more specific mechanism: NameNode transaction progress is surfaced as a `state ID`; a client retains the maximum state ID it has observed; later RPCs transport that lower bound; an Observer must align to it for coordinated reads or cause retry/fallback; `msync()` lets a client import a fresh frontier from the Active when ordinary same-client response flow is insufficient.

---

## Evidence classes

| ID | Source | Type | Evidence role | Directly establishes | Does **not** establish |
| --- | --- | --- | --- | --- | --- |
| A | Apache JIRA HDFS-12943, 2017–2019 | primary project/design/release record | historical feature boundary | Observer NameNode, state ID in RPC headers, read-after-write goal, Observer catch-up before response, `msync`, `ObserverReadProxyProvider`, release versions | invention priority for read replicas or session consistency; every later implementation detail |
| B | Apache Hadoop 3.2.3 Observer NameNode guide | official release documentation | architecture/deployment semantics | Active/Standby/Observer roles; transaction-ID-backed state ID; client → Observer alignment; `msync`; out-of-band client problem; edit-tail fast path; auto-msync; fallback-related deployment semantics | precise source-level behavior of every method/version; universal HDFS configuration |
| C | Apache Hadoop 3.3.0 `ClientGSIContext.java` | primary source code | client retained-state mechanism | max-accumulated `lastSeenStateId`; response accumulation; request-header propagation | durable persistence across client restart; namespace contents; writer authority |
| D | Apache Hadoop 3.3.0 `GlobalStateIdContext.java` | primary source code | server read-admission mechanism | server state ID from last applied/written txid; missing-state-ID rejection on Observer; too-far-behind retriable path; coordinated-method selection | a general consensus commit index; writer fencing; DataNode block-command authority |
| E | Apache Hadoop 3.3.0 `ObserverReadProxyProvider.java` | primary source code | routing and synchronization mechanism | startup `msync` through Active-side proxy; optional auto-msync; Observer-only eligible read attempts; Active fallback; writes to Active | that every read goes to Observer; that `msync` instantly advances every Observer |
| F | Apache Hadoop 3.3.0 `ReadOnly.java` | primary source code | operation-classification boundary | separate `activeOnly` and `isCoordinated` flags for nominally read-only methods | that all read-only RPCs share one freshness contract |
| G | Apache JIRA HDFS-13688, 2018 | primary development record | `msync` historical development | `msync` created inside HDFS-12943 to wait for/align consistent reads | the final routing semantics of every release without checking released code/docs |
| H | Apache JIRA HDFS-14272, 2019 | primary bug record | negative/counterexample evidence | a new client process did not inherit a previous client's state ID; sequential shell commands could therefore observe stale state; startup synchronization was needed | payload loss; a universal failure of Observer reads after the fix |

---

## Source A — HDFS-12943

**Source:** Apache Hadoop JIRA, [HDFS-12943 — Consistent Reads from Standby Node](https://issues.apache.org/jira/browse/HDFS-12943).

**Dates inspected:** created 19 December 2017; resolved 1 November 2019.

**Fix versions recorded by JIRA:** 2.10.0, 3.3.0, 3.1.4, 3.2.2.

### Direct evidence

The release note states that:

- `Observer` is a new NameNode type alongside Active and Standby;
- an Observer maintains a namespace replica like a Standby and additionally serves client reads;
- a `state ID` is added to RPC headers for read-after-write consistency within one client;
- an Observer responds only after its own state catches up with the client's state ID;
- clients can explicitly invoke `msync()`;
- `ObserverReadProxyProvider` switches writes and reads toward Active and Observer roles respectively.

The issue description also explicitly frames stale reads as a problem inherent in using a replicated Standby as a read-only replica. This matters for the prior-art boundary: the JIRA does not present “replica can be stale” as a newly discovered phenomenon.

### Retention relevance

The state ID is evidence about **how much prior namespace state a client has already observed**. It is not the namespace itself. Once carried into a later request, it constrains whether a candidate Observer is acceptable.

---

## Source B — released Observer NameNode guide

**Source:** Apache Hadoop, [Consistent Reads from HDFS Observer NameNode](https://hadoop.apache.org/docs/r3.2.3/hadoop-project-dist/hadoop-hdfs/ObserverNameNode.html), 3.2.3 documentation.

### Architecture inspected

The guide states that:

- Active serves mutations and normal client traffic;
- Standby/Observer follow namespace edits and block-location information;
- state ID is implemented using NameNode transaction ID;
- after an Active write, the client updates its state ID;
- the next Observer read sends that ID and waits until the Observer has caught up;
- this yields bounded same-client `read your own writes` behavior.

The guide separately describes **Edit Tailing Fast-Path** and configuration of in-progress edit tailing. It says the tail period determines Observer staleness relative to the Active and therefore affects the time a request can spend waiting for catch-up.

This supports a strict separation:

```text
replica advancement mechanism    = edit-log tailing
read-admission lower bound       = client state ID
```

Improving the first reduces lag but does not logically replace the second.

### Multi-client / out-of-band communication

The guide's `foo`/`bar` example is decisive. If `foo` writes and tells `bar` through a non-HDFS channel, `bar` does not automatically possess the state ID associated with `foo`'s mutation. `bar` may therefore obtain a stale Observer result unless it calls `msync()`.

The guide says `msync()` updates the client's state ID against the Active; later Observer reads are then consistent up to the point of that synchronization.

This directly grounds:

> **Observer catch-up capability ≠ client knowledge of the required catch-up frontier.**

### Configuration-sensitive operation class

The guide also warns that enabling access-time updates can make `getBlockLocations` require a write path, causing Observer attempts to fail/fall back to the Active. This is useful negative evidence against treating `read` as one uniform semantic class.

---

## Source C — `ClientGSIContext.java`

**Source:** Apache Hadoop 3.3.0 source, [`ClientGSIContext.java`](https://github.com/apache/hadoop/blob/rel/release-3.3.0/hadoop-hdfs-project/hadoop-hdfs-client/src/main/java/org/apache/hadoop/hdfs/ClientGSIContext.java).

### Direct code facts

The class holds:

```java
private final LongAccumulator lastSeenStateId =
    new LongAccumulator(Math::max, Long.MIN_VALUE);
```

On receiving an RPC response, it performs:

```java
lastSeenStateId.accumulate(header.getStateId());
```

When building a request, it sends:

```java
header.setStateId(lastSeenStateId.longValue());
```

### Retention interpretation

The client therefore retains a **monotonic maximum** of state IDs it has seen. Older responses cannot lower the stored frontier.

This state is compact and lossy relative to history:

- it says nothing about which exact operations produced the frontier;
- it does not preserve the namespace payload;
- it does not preserve a vector of per-object versions;
- it does not itself grant write authority.

It is retained because it changes the admissibility of future reads.

### Negative boundary

The field is ordinary runtime client state in this source. This case does not claim that it is persisted durably across arbitrary client restarts. The startup `msync` path and HDFS-14272 are evidence that a new client cannot simply be assumed to inherit an earlier process's frontier.

---

## Source D — `GlobalStateIdContext.java`

**Source:** Apache Hadoop 3.3.0 source, [`GlobalStateIdContext.java`](https://github.com/apache/hadoop/blob/rel/release-3.3.0/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/GlobalStateIdContext.java).

### Direct code facts

`getLastSeenStateId()` returns the NameNode's last applied or written transaction ID through the FSImage/namesystem path.

For Observer requests:

1. a missing state ID causes `StandbyException`, with a source comment explaining that an unaligned client should fail over to Active rather than potentially receive a stale result;
2. the server compares `clientStateId` and `serverStateId`;
3. if the client is sufficiently far ahead of an Observer, the method throws `RetriableException`, so the client can try another Observer or the Active;
4. only methods marked coordinated through the `ReadOnly` metadata are selected for this alignment behavior.

### Retention interpretation

The code separates three objects that could otherwise be collapsed:

```text
server namespace state       ≠
server transaction frontier  ≠
client required frontier
```

A correct decision depends on their relation.

### Important limit

The server state ID is used here as namespace progress for read alignment. The case does not treat it as interchangeable with:

- JournalNode `lastPromisedEpoch` in Case 50;
- DataNode `lastActiveClaimTxId` in Case 51;
- Kafka high watermark in Case 56;
- or a generic consensus `term` / `commitIndex`.

---

## Source E — `ObserverReadProxyProvider.java`

**Source:** Apache Hadoop 3.3.0 source, [`ObserverReadProxyProvider.java`](https://github.com/apache/hadoop/blob/rel/release-3.3.0/hadoop-hdfs-project/hadoop-hdfs-client/src/main/java/org/apache/hadoop/hdfs/server/namenode/ha/ObserverReadProxyProvider.java).

### Startup synchronization

Before the first Observer read, the provider invokes `initializeMsync()`. The implementation calls `ClientProtocol#msync()` through the Active-side failover proxy and marks the client `msynced`.

The source comment explicitly says this initial sync ensures that a new client reads data consistent with the world as of its instantiation.

### Auto-msync

The provider supports a configurable interval:

- negative: no automatic recurring `msync`;
- zero: `msync` every read;
- positive: synchronize after the configured elapsed period.

This produces an explicit cost/freshness tradeoff. More frequent Active contact can tighten the client's freshness frontier, but it also consumes RPC work and can reduce the scaling benefit of Observer reads.

### Routing and fallback

For eligible read methods the provider tries Observer proxies. It skips Active/Standby proxies in that Observer loop, handles Observer-specific retry signals, and falls back to the Active if Observer attempts cannot service the call.

Write/noneligible paths are forwarded to Active.

This directly supports:

> **read authority can be delegated conditionally without delegating mutation authority.**

---

## Source F — `ReadOnly.java`

**Source:** Apache Hadoop 3.3.0 source, [`ReadOnly.java`](https://github.com/apache/hadoop/blob/rel/release-3.3.0/hadoop-hdfs-project/hadoop-hdfs-client/src/main/java/org/apache/hadoop/hdfs/server/namenode/ha/ReadOnly.java).

The annotation exposes three separate properties:

- `atimeAffected`;
- `activeOnly`;
- `isCoordinated`.

The comment on `isCoordinated` says that, when true, server processing waits if server state ID is behind the client; when false, the method proceeds regardless of server state.

Therefore the project should not use a single Boolean `read-only` label as shorthand for all Observer freshness semantics.

---

## Source G — HDFS-13688

**Source:** Apache JIRA, [HDFS-13688 — Introduce msync API call](https://issues.apache.org/jira/browse/HDFS-13688), HDFS-12943 subtask.

The issue records the explicit creation of an `msync` RPC for consistent reads and describes the transaction-ID alignment objective. Because implementation details evolved while HDFS-12943 was developed, this record is used as **development-history evidence**, while released documentation and 3.3.0 source control final bounded semantics.

This prevents a common source error: treating an intermediate JIRA description as if it necessarily describes every final code path byte-for-byte.

---

## Source H — HDFS-14272

**Source:** Apache JIRA, [HDFS-14272 — ObserverReadProxyProvider should sync with active txnID on startup](https://issues.apache.org/jira/browse/HDFS-14272), created 13 February 2019, resolved 1 March 2019.

The report gives a minimal failure sequence:

```text
hdfs dfs -touchz /tmp/abc
hdfs dfs -ls /tmp/abc
```

The second command could fail to see the file because it was a separate client process and did not know the state ID returned to the first command. The Observer therefore did not wait for the relevant edit propagation.

This is especially valuable because it is **negative evidence from implementation/testing**, not only a design description.

It grounds three findings:

1. process/shell sequence does not itself transport HDFS state-ID causality;
2. a new client needs a way to import a current lower bound;
3. stale read in this case does not imply the committed namespace mutation was lost.

---

## Claims ledger

### Strongly grounded historical/implementation claims

1. Observer is a distinct HDFS NameNode role that can serve reads without being the Active mutation authority.
2. HDFS-12943 uses RPC-carried state IDs backed by NameNode transaction progress to align Observer reads.
3. `ClientGSIContext` retains the maximum state ID observed by the client and propagates it into later requests.
4. `GlobalStateIdContext` compares client and server progress, rejects missing state IDs on Observer, and supports retry when the Observer is too far behind.
5. `ObserverReadProxyProvider` performs startup `msync`, supports optional auto-msync, attempts Observer reads, and can fall back to Active.
6. HDFS-14272 demonstrates that a new client process can lose the causal freshness frontier even when commands execute sequentially from the user's point of view.
7. Fast edit tailing reduces lag; it is separate from the state-alignment criterion.
8. nominally read-only calls can differ in `activeOnly` and `isCoordinated` requirements.

### Engineering reconstructions introduced by this repository

- `client freshness frontier`;
- `read-admissibility lower bound`;
- `retained observation frontier`;
- `replica-maintenance speed ≠ read-admissibility criterion`;
- `writer fencing ≠ command authority ≠ read freshness`.

These terms summarize source-supported relations but are not attributed to Apache actors unless the exact source phrase is separately cited.

### Functional analogies only

The case may be compared to:

- Kafka high-watermark/currentness;
- Dynamo divergent-version qualification;
- Raft follower progress;
- cache valid/current bits;
- scrub-qualified replica use.

The analogy is only that **physical state presence may be insufficient for current use without additional currentness evidence**. No common protocol or direct historical genealogy is claimed.

---

## Prior-art / novelty boundary

No invention claim is made for read replicas, follower reads, transaction sequencing, monotonic reads, read-your-writes, session consistency, causal consistency, or replicated-state-machine catch-up.

The historical claim is intentionally narrower:

> HDFS-12943 and the released Hadoop 3.x implementation provide a specific Apache HDFS composition of Observer NameNode role, transaction-backed state ID, RPC-carried client frontier, catch-up gating, `msync`, Observer-aware routing, and edit-tail acceleration.

HDFS-12943 itself frames stale-read handling as a replicated-system problem and links earlier HDFS work for stale Standby reads. That is sufficient to block a false “Observer invented consistent follower reads” narrative without turning this slice into a general distributed-consistency prior-art survey.

---

## Cross-case boundary ledger

| Comparison | Valid relation | Invalid collapse |
| --- | --- | --- |
| Case 50 QJM | both retain compact control state that constrains future admissibility | client state ID is **not** a persisted JournalNode fencing epoch |
| Case 51 DataNode commands | both use NameNode transaction progress as control evidence in bounded implementations | read freshness is **not** DataNode command authority |
| Case 56 Kafka | both distinguish replica physical state from what a consumer/client may safely observe | HDFS client state ID is **not** Kafka partition high watermark |
| Case 23 Dynamo | both require currentness evidence beyond byte survival | ordered Observer catch-up is **not** concurrent-version reconciliation |
| Case 08 cache | both distinguish surviving copy from current/valid use | Observer state alignment is **not** cache-coherence or validity hardware |

---

## Evidence gaps deliberately left open

- direct page-by-page inspection of the HDFS-12943 design PDF and its proposal revisions;
- HDFS-13150 fast-path design document archaeology;
- exact RPC-queue waiting implementation beneath `AlignmentContext` for every affected release;
- Router-Based Federation propagation of state IDs;
- post-3.3 Observer regressions and fixes;
- independent black-box stale-read/fallback fault injection;
- end-to-end relation between NameNode freshness and DataNode file-data service;
- wider prior-art survey of consistent follower reads outside HDFS.

None of these gaps overturns the bounded source-level mechanism established above.

---

## Promotion decision

**Case 61 is `grounded`.**

Promotion is justified because the core mechanism is supported by multiple mutually constraining Apache primary sources:

- project/release history says what consistency problem the feature was intended to solve;
- official released documentation gives the architecture and configuration semantics;
- client source shows the retained monotonic state frontier;
- server source shows the alignment/retry boundary;
- proxy source shows `msync`, routing, and fallback;
- a 2019 bug report supplies a concrete counterexample where user-visible sequentiality failed to transport the required retained frontier.

The remaining work is refinement, later-version evolution, independent experimentation, and broader prior art rather than a blocker on the bounded case.
