# Case 61 deepening — HDFS RBF federated state-ID propagation, publication ordering, and invalidation (2022–2024)

## Status

**bounded deepening complete**

This evidence slice deepens [`Case 61 — Apache HDFS Observer NameNode`](../cases/61-apache-hdfs-observer-stateid-read-freshness.md) at one intentionally narrow boundary: what happened when the single-name-service Observer freshness mechanism was extended through **Router-Based Federation (RBF)**, where one client-visible Router can proxy several independent HDFS nameservices.

The result is useful for `technical-retention` because it exposes three different obligations that a scalar `stateId` story can hide:

1. **scope** — a freshness frontier has to remain attached to the correct nameservice;
2. **publication ordering** — the currentness metadata from an RPC response has to become visible before the application is allowed to treat the response as completed;
3. **invalidation** — a previously valid monotonic frontier may have to be forgotten when the mechanism that gives that number meaning is disabled.

The bounded engineering relation is:

```text
retaining a larger freshness number
    != sufficient currentness safety

freshness evidence must also retain
    scope + publication order + validity regime
```

`freshness-scope state`, `publication-before-use`, and `validity-regime boundary` are project reconstruction terms. They are not Apache historical vocabulary.

---

## Why this is a separate slice from the original Case 61 grounding

The canonical Case 61 is centered on HDFS-12943 and the Hadoop 3.3.0 single-nameservice mechanism:

```text
client retains max stateId S
    -> request carries S
    -> Observer waits until local txid >= S
    -> read may be admitted
```

That mechanism is already grounded.

RBF adds another mediation layer:

```text
client
  -> Router
       -> nameservice ns1 -> Active / Observer
       -> nameservice ns2 -> Active / Observer
       -> nameservice ns3 -> Active / Observer
```

A single scalar is no longer enough to say how far the client may assume **each independent namespace** has advanced. This slice therefore does not repeat Observer catch-up semantics; it studies the retained control state needed to preserve those semantics across the Router boundary.

---

## Source/evidence classification

### Primary Apache historical / implementation evidence

1. **HADOOP-18345 — “Enhance client protocol to propagate last seen state IDs for multiple nameservices.”**
   - created 18 July 2022;
   - resolved 23 August 2022;
   - target/fix version recorded as Hadoop 3.4.0;
   - directly states that the existing RPC header had one `stateId`, while RBF needs state IDs for multiple nameservices.
   - <https://issues.apache.org/jira/browse/HADOOP-18345>

2. **HDFS-13522 — “Add federated nameservices states to client protocol and propagate it between routers and clients.”**
   - resolved 9 September 2022;
   - fix version 3.4.0;
   - directly says the patch captures the state of all namespaces in Routers and propagates it to clients.
   - <https://issues.apache.org/jira/browse/HDFS-13522>

3. **Apache Hadoop commit `e77d54d1eef071f74a97dfee28f12ee7cfc069de`**, 9 September 2022.
   - implements HDFS-13522;
   - adds `RouterFederatedStateProto` transport and Router-side namespace state tracking;
   - introduces `PoolAlignmentContext` and per-namespace shared/local state-ID handling.
   - <https://github.com/apache/hadoop/commit/e77d54d1eef071f74a97dfee28f12ee7cfc069de>

4. **HDFS-16767 — “RBF: Support observer node from Router-Based Federation.”**
   - resolved 14 September 2022;
   - fix version 3.4.0;
   - directly describes routing read calls from Routers to Observer NameNodes.
   - <https://issues.apache.org/jira/browse/HDFS-16767>

5. **Apache Hadoop commit `6422eaf3017eed43d081406ab0c41426c9b6dc6f`**, 14 September 2022.
   - implements HDFS-16767.
   - <https://github.com/apache/hadoop/commit/6422eaf3017eed43d081406ab0c41426c9b6dc6f>

6. **Hadoop 3.4.0 `RouterStateIdContext.java`.**
   - explicitly describes itself as the Router implementation holding state IDs for all namespaces;
   - uses a `ConcurrentHashMap<String, LongAccumulator>` keyed by namespace ID;
   - says the values are updated only from NameNode responses;
   - serializes the namespace map into `RouterFederatedStateProto` for clients.
   - <https://github.com/apache/hadoop/blob/rel/release-3.4.0/hadoop-hdfs-project/hadoop-hdfs-rbf/src/main/java/org/apache/hadoop/hdfs/server/federation/router/RouterStateIdContext.java>

7. **Hadoop 3.4.0 `ClientGSIContext.java`.**
   - retains a `routerFederatedState` in addition to the original scalar `lastSeenStateId`;
   - merges federated maps by taking the maximum per namespace;
   - forwards the serialized federated state in subsequent RPC requests.
   - <https://github.com/apache/hadoop/blob/rel/release-3.4.0/hadoop-hdfs-project/hadoop-hdfs-client/src/main/java/org/apache/hadoop/hdfs/ClientGSIContext.java>

8. **HDFS-17156 — “Client may receive old state ID which will lead to inconsistent reads.”**
   - resolved 17 August 2023;
   - affects/fixes 3.4.0 and 3.3.9 according to the issue record;
   - documents an observed RBF + Observer-read stale-read failure caused by returning an RPC result to the caller before the latest response state ID had been processed.
   - <https://issues.apache.org/jira/browse/HDFS-17156>

9. **Apache Hadoop commit `42b4525f75b828bf58170187f030b08622e238ab`**, 17 August 2023.
   - moves `call.setRpcResponse(value)` to occur **after** `alignmentContext.receiveResponseState(header)`;
   - adds a test asserting that state reception happens before caller notification.
   - <https://github.com/apache/hadoop/commit/42b4525f75b828bf58170187f030b08622e238ab>

10. **HDFS-17514 — “RBF: Routers keep using cached stateID even when active NN returns unset header.”**
    - resolved in 2024;
    - describes the case where a NameNode is restarted with `dfs.namenode.state.context.enabled=false` while Routers retain a previously cached state ID;
    - says new clients behind RBF may otherwise continue to receive the stale state ID.
    - <https://issues.apache.org/jira/browse/HDFS-17514>

11. **Apache Hadoop commit `6a4f0be854b36b0dd985aba8d3110b0f2928c2fc`**, 14 May 2024.
    - changes `PoolAlignmentContext.receiveResponseState()` so a zero state ID from the NameNode can reset previously positive shared/local state-ID accumulators;
    - adds tests for a restarted Active NameNode with state context disabled.
    - <https://github.com/apache/hadoop/commit/6a4f0be854b36b0dd985aba8d3110b0f2928c2fc>

### Related repository check

A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for HDFS Observer, Router-Based Federation, and `stateId` found no dedicated technical-history case. This slice therefore remains here because its focus is the retention/currentness relation, not a general RBF history.

---

## Historical record 1 — federation turns one scalar frontier into a nameservice-scoped relation

### H/P — HADOOP-18345 states the mismatch directly

The original Observer mechanism carried one field in the RPC header:

```text
optional int64 stateId = 8; // The last seen Global State ID
```

HADOOP-18345 says this is insufficient once a client is communicating through Router-Based Federation with multiple nameservices. The protocol needs state IDs for **each** nameservice.

That is direct actor evidence for the scope problem. It is not a later theoretical reconstruction imposed on RBF.

The safe historical claim is:

> **By the 2022 RBF Observer work, Apache developers explicitly treated one global-looking scalar state ID as insufficient for a Router spanning multiple independent HDFS nameservices.**

This does not establish that HDFS invented scoped causal/session frontiers.

### H/P — HDFS-13522 captures and returns all namespace frontiers

HDFS-13522 says the Router captures the state of all namespaces and propagates that state to clients. Its implementation adds a `RouterFederatedStateProto` containing a map from nameservice ID to state ID.

Hadoop 3.4.0 `RouterStateIdContext` materializes that relation as:

```text
namespace ID
    -> LongAccumulator(max)
    -> serialized RouterFederatedStateProto
    -> RPC response to client
```

The client-side `ClientGSIContext` retains the returned federated blob and merges later values by namespace using a maximum operation.

The important boundary is therefore:

```text
stateId value
    != complete freshness relation

stateId value + nameservice identity
    -> bounded freshness relation
```

A state ID copied from one nameservice into another is not made meaningful merely because the number is large.

---

## Historical record 2 — Router state has two trust domains

### H/P — NameNode responses may advance shared Router state

The HDFS-13522 implementation describes `RouterStateIdContext` as state updated by responses from NameNodes. Its `PoolAlignmentContext` has two distinct accumulators:

- `sharedGlobalStateId` — shared for a namespace and updated from NameNode responses;
- `poolLocalStateId` — local to a connection pool and able to incorporate client-observed state for downstream requests.

The implementation comment explicitly says the shared value is updated only from NameNode responses so clients cannot poison it. Client-provided state can affect the local pool value, with scope limited to the relevant connection-pool context.

This gives a retained-state decomposition:

```text
namespace authoritative-progress evidence from NameNode
    != client-observed lower bound
    != serialized federated state sent to clients
```

They may all contain transaction-derived numbers, but they have different provenance and authority.

### Engineering reconstruction

The Router is therefore not merely a transparent byte-forwarder. For Observer consistency it becomes a **currentness-state mediator** that must preserve:

- nameservice identity;
- provenance of the frontier;
- monotonic relation within the intended domain;
- correct propagation to clients and downstream NameNodes.

`currentness-state mediator` is a project term.

---

## Historical record 3 — response completion raced ahead of currentness-metadata publication

### H/P — HDFS-17156 records a concrete stale-read failure

HDFS-17156 was reported from an RBF environment with Observer reads enabled. The issue describes a workload where a file is written through the Active NameNode and immediately read through an Observer. The observed read could reflect the earlier `OP_ADD` state rather than the later `OP_CLOSE` state.

The issue's diagnosis is specific: during writes, the Router could respond to the client before the latest state ID returned by the Active NameNode had been installed into the alignment context. The following Observer read therefore carried an older frontier and could be admitted too early.

This is a crucial retention boundary because the namespace mutation itself was not necessarily missing. The problem was the **ordering between payload/RPC-result visibility and currentness-metadata visibility**.

### H/P — the 2023 fix establishes publication-before-notification ordering

Commit `42b4525...` changes the IPC client success path from:

```text
make RPC result visible to caller
    -> receive response state into AlignmentContext
```

to:

```text
receive response state into AlignmentContext
    -> make RPC result visible to caller
```

The added test says what is being guaranteed: verify that `stateID` is received into the call before the caller is notified.

This lets the case add a precise statement:

```text
RPC operation completed at application layer
    != all sideband currentness evidence already published
```

unless the implementation enforces that order.

### Engineering reconstruction — completion has a control-state closure

For a client that will use the response's freshness frontier to constrain later reads, a write-like RPC is not safely “complete for the Observer-read protocol” merely because its return value is available.

A bounded closure relation is:

```text
response value decoded
    + response stateId processed
    -> caller may safely proceed under this protocol
```

This is **not** a claim that every RPC system must atomically publish every sideband field. It is specific to a protocol where later read admissibility depends on state learned from the prior response.

---

## Historical record 4 — monotonic retention can itself become stale across a validity-regime change

### H/P — HDFS-17514 exposes over-retention of currentness evidence

The original state-ID accumulators deliberately use `max`: an older response should not make a client's or Router's lower bound move backward during normal operation.

HDFS-17514 demonstrates why that monotonic rule cannot be interpreted as “retain the largest number forever.” The issue considers a NameNode that previously had `dfs.namenode.state.context.enabled=true`, then restarts with that feature disabled.

The Router could continue using the earlier cached state ID even though the Active no longer supplied meaningful state-ID context. Behind RBF this was worse than the direct-client case because **new clients** could receive the Router's stale cached frontier as if it were current protocol state.

The failure is therefore not ordinary numeric regression. It is a change in whether the number still has a valid producing mechanism.

### H/P — the 2024 fix makes zero a reset signal for previously positive Router state

Commit `6a4f0be...` changes `PoolAlignmentContext.receiveResponseState()` so that when the response carries `stateId == 0` while the shared cached value is positive, it resets both:

- the shared namespace state accumulator;
- the pool-local accumulator.

The accompanying test says Routers should reset the cached state ID so they do not send a stale value to the Observer.

This gives the strongest new relation in this slice:

```text
monotonic within one valid state-ID regime
    != monotonic across regime invalidation
```

and:

```text
retaining more currentness evidence
    != always safer
```

Sometimes correctness requires **forgetting** a formerly useful control value because the system no longer has the mechanism required to extend or interpret it safely.

### Boundary — the fix does not prove universal deletion of stale state everywhere

The integration test intentionally distinguishes a newly created filesystem/client from the old one. After the Router resets its cached value, a new client should not gain fresh Observer routing from that stale state, while the old filesystem object can still carry its previously retained state and continue making Observer calls.

So this slice must not say:

```text
NameNode disables state context
    -> every previously distributed state ID disappears globally
```

The evidence supports a narrower claim:

> **The Router must stop re-publishing a stale cached namespace frontier to new clients once the downstream NameNode no longer supplies valid state context. Existing clients may still retain older session state.**

That distinction matters because “invalidating a cache” and “revoking every copy already distributed to clients” are different engineering problems.

---

## Retained-state decomposition after the RBF deepening

The bounded Observer mechanism now contains at least the following distinct state:

1. **namespace payload / edit state** — the actual HDFS metadata state;
2. **NameNode transaction progress** — the source from which state IDs are derived;
3. **single-nameservice client frontier** — original `lastSeenStateId` relation;
4. **Router namespace map** — nameservice ID → latest trusted state ID;
5. **pool-local client frontier** — a lower bound carried into one Router connection-pool context;
6. **serialized federated frontier** — `RouterFederatedStateProto` sent to clients;
7. **client-retained federated map** — merged max-per-namespace state returned by Routers;
8. **publication-order state** — whether a response's frontier has been installed before the application observes RPC completion;
9. **validity-regime state** — whether the NameNode/Router path is currently producing meaningful state-ID context at all.

These are related but not interchangeable.

A useful compact form is:

```text
payload currentness
    != evidence of currentness
    != scope of that evidence
    != publication of that evidence
    != continuing validity of that evidence
```

---

## Failure / forgetting matrix

| Failure or transition | What survives | What goes wrong if treated as sufficient |
| --- | --- | --- |
| Observer lags | namespace replica + older txid | replica exists but is not yet admissible for this client |
| single scalar used across federation | a state-ID number | nameservice scope is missing |
| RPC result released before state processing | operation result + eventually arriving state ID | next read may start from an older frontier |
| Router retains old positive state after producer disables state context | cached frontier | new clients can inherit a stale protocol assumption |
| Router resets cached frontier | namespace data still exists | reset does not erase user data or force all clients to forget old session state |
| existing client retains previously distributed federated state | client session frontier | Router-side invalidation is not universal revocation |

---

## Engineering reconstruction

### E — freshness evidence is relational, not merely numeric

A larger integer is not intrinsically “fresher.” The number has to be bound to:

- the correct nameservice;
- a trusted producer path;
- the protocol configuration in which it is meaningful.

### E — sideband metadata can be part of operation completion

If a subsequent operation's admissibility depends on metadata learned from the prior response, then publishing the response payload before that metadata creates a real causal hole even though both eventually arrive.

### E — monotonicity is scoped by validity

`max` is appropriate while successive values belong to the same meaningful progress relation. HDFS-17514 shows that a change in the availability of the state-context mechanism can invalidate the assumption under which monotonic accumulation was safe.

### E — invalidation is not payload erasure

Resetting a cached state ID does not delete namespace metadata. It removes or weakens an **admission claim** about how fresh a future Observer read must be or may safely be routed.

### E — invalidating one mediator is not revoking every distributed copy

The 2024 test boundary shows that a Router can stop re-exporting stale state to new clients without retroactively deleting state already retained by older clients.

This is another instance of a general retention lesson:

```text
stop producing / stop publishing state
    != recall every embodiment already distributed
```

---

## Functional comparisons

### Case 50 — QJM epoch fencing

**Functional analogy only.** Both cases retain small control values that change whether later operations are admissible. But:

- QJM's epoch promise is writer-authority refusal state;
- Observer/RBF state IDs are read-freshness lower bounds;
- a stale state ID does not authorize writing the edit log.

### Case 56 — Kafka high watermark

**Functional analogy only.** Both use compact progress/currentness metadata rather than copying the whole retained payload to decide what may be served. Kafka's high watermark is partition/broker replication state; HDFS RBF carries client/Router nameservice-scoped lower bounds. Their consistency contracts and update paths differ.

### Case 58 — Raft snapshot publication

**Functional analogy only.** Case 58 shows that a replacement representation existing on disk is not the same as its publication/currentness relation becoming authoritative. HDFS-17156 shows a smaller but structurally related distinction: an RPC result can exist before its currentness metadata is safely published to the next operation. No implementation genealogy is claimed.

---

## Bounded philosophical interpretation

The strongest philosophical point justified by this slice is modest:

> A system may have to forget a retained control state not because the represented past became false, but because the relation that made that past actionable has changed.

The old state ID can be a perfectly real historical value and still be unsafe as a present routing/read-admission frontier after state-context production is disabled.

This is useful for analyses of technical memory only if the engineering distinction remains intact:

```text
historically true value
    != presently valid control state
```

No stronger claim about human memory, archival truth, or philosophical forgetting follows automatically.

---

## Explicit non-claims

This slice does **not** claim that:

1. HDFS invented read-your-writes, monotonic reads, session guarantees, causal consistency, or vector-like scoped progress metadata.
2. `RouterFederatedStateProto` is a general vector clock.
3. nameservice state IDs encode causal relations between independent HDFS namespaces.
4. the Router's state map is user payload.
5. a larger state ID from another nameservice is meaningful for the current nameservice.
6. HDFS-17156 proves namespace data loss; it documents stale read/currentness propagation failure.
7. every RPC framework must process alignment metadata before returning every response.
8. state-ID processing and response delivery are one atomic durable transaction.
9. HDFS-17514 means a state ID of zero is a universal semantic reset in all HDFS versions and contexts; the claim is bounded to the inspected fix path.
10. resetting Router state deletes or rolls back HDFS namespace data.
11. the 2024 Router reset remotely revokes already-retained state from every existing client.
12. Router Based Federation makes Routers consensus authorities over namespace content.
13. the RBF State Store and the Observer `RouterStateIdContext` are the same retained-state mechanism.
14. HDFS 3.4.0 already contains the May 2024 HDFS-17514 fix; the fix is treated as a later commit-level witness unless a release/backport is independently established.
15. HDFS-13522 or HDFS-16767 is the invention date of federated read-freshness tracking in distributed systems.
16. RBF Observer reads and Kafka/Raft follower reads are historically or technically identical.

---

## Claim ledger

| Claim | Class | Evidence strength | Boundary |
| --- | --- | --- | --- |
| One scalar state ID is insufficient for multiple RBF nameservices | historical record | strong primary | HADOOP-18345 actor statement |
| RBF captures namespace-scoped state IDs and propagates them to clients | historical record | strong primary | HDFS-13522 + implementation |
| Router shared namespace state is updated from NameNode responses | historical record | strong primary | 3.4.0 source comments/code |
| Client retains/merges per-namespace Router federated state | historical record | strong primary | 3.4.0 `ClientGSIContext` |
| RPC caller notification could precede state-ID processing | historical record | strong primary | HDFS-17156 + exact fix diff |
| State-ID processing must precede caller notification for this protocol path | historical record / engineering reconstruction | strong primary | bounded to inspected IPC/Observer dependency |
| Router could retain stale state after producer state context was disabled | historical record | strong primary | HDFS-17514 |
| Resetting stale cached state is required for new-client safety in the inspected fix | historical record | strong primary | exact 2024 tests/diff |
| Monotonicity is safe only inside a valid interpretation regime | engineering reconstruction | strong | derived from 2022–2024 failures/fixes |
| Historically true control value can cease to be presently admissible | bounded philosophical interpretation | moderate | downstream of mechanism only |

---

## What this closes and what remains open

### Closed by this slice

The canonical Case 61 open item **“Router-Based Federation Observer-read state propagation”** is now grounded at a bounded implementation level for:

- nameservice-scoped state-ID transport;
- Router/client retained state decomposition;
- response-publication ordering failure/fix;
- stale cached-frontier invalidation when the producing NameNode disables state context.

The broader item **“post-3.3 Observer consistency regressions and fixes”** is only **partially** closed: HDFS-17156 and HDFS-17514 are two strong later regressions, not an exhaustive audit.

### Remaining evidence debt

1. inspect HDFS-16767 routing implementation in a fixed release at the same detail level as the state propagation path;
2. determine the exact release/backport history of HDFS-17156 and HDFS-17514 beyond the Jira/commit records used here;
3. fault-inject response/state publication races to reproduce HDFS-17156 independently;
4. test Router restart, NameNode state-context disable/enable, and mixed old/new clients across several nameservices;
5. inspect size-limit behavior when the Router namespace-state map exceeds `dfs.federation.router.observer.federated-state.propagation.maxsize`;
6. keep WebHDFS/delegation-token semantics outside this slice unless a concrete currentness interaction is found.

---

## Source list

### Primary Apache issues / commits

- HADOOP-18345 — multi-nameservice state IDs: <https://issues.apache.org/jira/browse/HADOOP-18345>
- HDFS-13522 — federated namespace state propagation: <https://issues.apache.org/jira/browse/HDFS-13522>
- HDFS-16767 — Observer reads through RBF: <https://issues.apache.org/jira/browse/HDFS-16767>
- HDFS-17156 — response exposed before latest state ID becomes visible: <https://issues.apache.org/jira/browse/HDFS-17156>
- HDFS-17514 — stale Router cached state ID after state context is disabled: <https://issues.apache.org/jira/browse/HDFS-17514>
- HDFS-13522 implementation commit: <https://github.com/apache/hadoop/commit/e77d54d1eef071f74a97dfee28f12ee7cfc069de>
- HDFS-16767 implementation commit: <https://github.com/apache/hadoop/commit/6422eaf3017eed43d081406ab0c41426c9b6dc6f>
- HDFS-17156 fix commit: <https://github.com/apache/hadoop/commit/42b4525f75b828bf58170187f030b08622e238ab>
- HDFS-17514 fix commit: <https://github.com/apache/hadoop/commit/6a4f0be854b36b0dd985aba8d3110b0f2928c2fc>

### Fixed-release implementation witnesses

- Hadoop 3.4.0 `RouterStateIdContext.java`: <https://github.com/apache/hadoop/blob/rel/release-3.4.0/hadoop-hdfs-project/hadoop-hdfs-rbf/src/main/java/org/apache/hadoop/hdfs/server/federation/router/RouterStateIdContext.java>
- Hadoop 3.4.0 `ClientGSIContext.java`: <https://github.com/apache/hadoop/blob/rel/release-3.4.0/hadoop-hdfs-project/hadoop-hdfs-client/src/main/java/org/apache/hadoop/hdfs/ClientGSIContext.java>

### Canonical earlier Observer grounding

- HDFS-12943 — Consistent Reads from Standby Node / Observer NameNode: <https://issues.apache.org/jira/browse/HDFS-12943>
- Canonical repository case: [`../cases/61-apache-hdfs-observer-stateid-read-freshness.md`](../cases/61-apache-hdfs-observer-stateid-read-freshness.md)
