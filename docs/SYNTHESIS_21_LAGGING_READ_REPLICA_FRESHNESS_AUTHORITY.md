# Synthesis 21 — Lagging Read-Replica Freshness, Client Frontiers, and Fallback

## Status and scope

**Bounded relation-decomposition synthesis.** This document closes one explicit ROADMAP question:

> In lagging read replicas, how should mutation authority, replica-applied transaction progress, a client's retained seen-state lower bound, `msync`/frontier import, edit-tail maintenance, read-admission waiting/retry, and Active fallback be separated?

The canonical mechanism is [Case 61 — Apache HDFS Observer NameNode state-ID read freshness](../cases/61-apache-hdfs-observer-stateid-read-freshness.md), grounded in Apache HDFS-12943/HDFS-13688/HDFS-14272, released Hadoop documentation, and Hadoop 3.3.0 source. [Case 50](../cases/50-apache-hdfs-qjm-epoch-fencing.md) and [Case 51](../cases/51-apache-hdfs-datanode-command-fencing.md) provide HDFS-internal counterexamples against collapsing writer authority, DataNode command authority, and read freshness. [Synthesis 16](SYNTHESIS_16_REPLICA_CURRENTNESS_RETAINED_RELATION.md) and [Synthesis 17](SYNTHESIS_17_REPLICATED_LOG_SUFFIX_CURRENTNESS_VISIBILITY.md) provide cross-system currentness/visibility boundaries without being treated as HDFS genealogy.

Historical claims remain in the canonical cases/evidence. The decomposition below is an **engineering reconstruction**. Cross-system comparisons are **functional analogies only**. No claim is made that HDFS invented read replicas, read-your-writes, monotonic reads, session guarantees, transaction IDs, follower catch-up, or causal/session frontiers.

The bounded conclusion is:

> **A lagging replica can be readable, internally coherent, and non-authoritative for mutation while still being inadmissible for a particular read. HDFS Observer closes that gap by composing three different progress relations: authoritative namespace progress, replica-applied progress, and a client-retained lower bound on already-observed state. Edit tailing advances the replica; `stateId` carries the client's lower bound; `msync()` imports a newer lower bound from the Active; coordinated reads wait/retry until the Observer has caught up; and Active fallback preserves service when the Observer path cannot satisfy the admission condition.**

---

## 1. The three progress frontiers are not one number

HDFS uses NameNode transaction progress in several places, but the same numerical lineage must not be normalized into one universal `currentness counter`.

For this synthesis, separate:

```text
A = Active / authoritative namespace transaction progress
O = Observer last-applied transaction progress
C = client retained last-seen state-ID lower bound
```

A typical lagging configuration is:

```text
O < C <= A
```

The Observer can be a valid namespace replica and still be too old for that client. A different client with a lower retained frontier can legitimately have a different admission result against the same Observer.

That yields:

```text
replica exists
    != replica is current with Active
    != replica is sufficiently current for this client
```

The last relation is observer-specific. It cannot be inferred from physical replica survival alone.

---

## 2. Mutation authority is upstream of read admissibility, not identical to it

**Historical record inherited from Case 50:** QJM writer epochs and JournalNode `lastPromisedEpoch` decide which NameNode writer may extend the shared edit log after failover. An older NameNode may remain alive and even reachable while losing mutation authority.

**Historical record inherited from Case 51:** DataNodes separately retain which NameNode's block-management commands are admissible, while post-failover block inventories can remain stale even after authority has shifted.

**Historical record inherited from Case 61:** Observer is deliberately a non-Active read-serving role.

Therefore:

```text
journal mutation authority
    != DataNode command authority
    != Observer read authority
    != client-specific read freshness
```

A system can correctly fence mutation while still needing additional retained state to decide whether a lagging read replica may answer a given client.

This is also why “the Active is known” is not the end of the retention problem. Authority selects who may advance the namespace. It does not automatically make every follower's already-retained view admissible.

---

## 3. The client retains a lower bound, not a copy of the state

**Historical record inherited from Case 61:** Hadoop 3.3.0 `ClientGSIContext` accumulates the maximum response `stateId` it has seen and places that value in later request headers.

The retained client state therefore says approximately:

```text
future coordinated reads must not place me before state C
```

It does **not** say:

- which exact operations produced `C`;
- what the namespace contained at `C`;
- which objects the client accessed;
- which NameNode currently has mutation authority;
- whether every Observer has already reached `C`.

This gives a useful controlled distinction:

> **retained seen-state lower bound ≠ retained namespace snapshot ≠ retained client operation history.**

The scalar is lossy but operationally constitutive: it changes which future replica states may be used.

---

## 4. Client process lifetime and causal/frontier lifetime can diverge

HDFS-14272 is decisive negative evidence.

Two shell commands can execute in ordinary wall-clock order:

```text
client/process 1: write X
client/process 2: read X
```

yet the second process does not automatically inherit the first process's response `stateId`. Human/program order across client instances is therefore not sufficient protocol evidence that the second read must reject an older Observer view.

So:

```text
later process start
    != inherited seen-state frontier

wall-clock order
    != transported protocol causality
```

The startup synchronization added to `ObserverReadProxyProvider` repairs that boundary by importing a current frontier through the Active.

This is a retention failure of **relation transport**, not evidence that the written namespace mutation vanished.

---

## 5. `msync()` imports a frontier; it does not replicate the namespace

The Observer guide's `foo` / `bar` example shows the same issue without requiring process restart. A mutation can become known to another application through an out-of-band channel while the second HDFS client still lacks the state ID associated with that mutation.

`msync()` solves that bounded problem by contacting the Active path and updating the caller's alignment state.

The strongest guardrails are:

```text
msync()
    != a user-data write
    != a new namespace commit
    != an Observer flush
    != immediate convergence of all Observers
```

Instead:

```text
Active current progress
        |
        v
     msync()
        |
        v
client lower bound C rises
        |
        v
future coordinated Observer read must satisfy O >= C
```

`msync()` changes what the client is entitled to demand from future reads. Replica advancement remains separate work.

---

## 6. Edit tailing is maintenance; state alignment is admission

Case 61 directly separates two mechanisms that are easy to collapse because both affect observed staleness.

### Replica-maintenance path

Observer/Standby NameNodes tail edits from JournalNodes. Fast in-progress edit tailing reduces the distance:

```text
A - O
```

and therefore reduces expected wait time.

### Read-admission path

For coordinated reads, the server compares the request's client frontier against local applied progress. If `O >= C`, the read can proceed on freshness grounds. If the Observer is behind, processing can wait; if the gap is unsuitable for bounded waiting, the server can return a retriable path.

Therefore:

> **edit-tail speed ≠ read-admission criterion.**

A very fast Observer still needs the criterion because a client can carry a frontier newer than its local state at that instant. Conversely, a perfectly specified admission rule cannot make a permanently stalled Observer advance; it can only wait, reject, retry, or route elsewhere.

---

## 7. Waiting, retry, and fallback are three different closure paths

When `O < C`, “the read failed” is too coarse.

The bounded mechanism exposes several outcomes:

1. **wait** — local replica advancement may soon satisfy `O >= C`;
2. **retry** — the current Observer is too far behind or otherwise unsuitable, so another candidate can be attempted;
3. **fallback to Active** — the Observer path does not produce an admissible service result, so the mutation authority's current namespace view supplies the read.

These transitions preserve another distinction:

```text
read-admission failure
    != namespace loss
    != replica corruption
    != loss of mutation authority
```

Active fallback is also not a convergence mechanism:

> **successful fallback ≠ Observer caught up.**

It closes the caller's service path while the lagging replica may still require edit-tail maintenance afterward.

---

## 8. “Read-only” is not one retention contract

The Hadoop 3.3.0 `ReadOnly` annotation and `ObserverReadProxyProvider` retain separate classifications such as `activeOnly` and `isCoordinated`.

This blocks the shortcut:

```text
method does not mutate user-visible namespace
    -> any Observer may answer immediately
```

The actual bounded distinctions are closer to:

```text
read-like operation
    != Observer-eligible operation
    != coordinated freshness-checked operation
    != operation independent of Active-only state
```

Configuration can move an operation across those boundaries; the Observer guide's access-time example shows a nominal read path becoming Active-requiring when it entails metadata mutation.

So operation class is itself part of read-admission semantics.

---

## 9. Freshness/currentness is observer-relative here

Synthesis 16 established that distributed currentness is a protocol-qualified relation rather than one universal metadata field. Case 61 adds a sharper observer-specific form.

For one fixed Observer state `O`:

```text
client C1 <= O  -> admissible on freshness grounds
client C2 >  O  -> must wait/retry/fallback
```

The physical replica is unchanged. What differs is the retained lower bound carried by the requester.

This gives:

> **one replica state can be fresh enough for one client and stale for another without being internally inconsistent.**

That is not the same relation as Kafka's high watermark. Kafka's bounded high-watermark case qualifies a partition prefix for ordinary consumption based on replica progress/ISR state. HDFS Observer carries a client-specific minimum already-seen frontier. Both are functionally comparable as currentness/admissibility relations, but:

```text
Kafka committed-prefix frontier
    != HDFS client seen-state floor
```

No shared protocol or genealogy follows.

---

## 10. Freshness is not durability, integrity, or convergence

The HDFS Observer case is about namespace-read admissibility. It should not absorb neighboring retention questions.

A successful state-aligned read does not by itself prove:

- end-to-end file-block durability on DataNodes;
- checksum integrity of every payload embodiment;
- that every Standby/Observer has converged;
- that decommission/maintenance placement requirements are satisfied;
- that a future failover will preserve every current read path;
- that storage below HDFS satisfied its own flush/persistence contract.

Conversely, a stale Observer read path can be rejected while authoritative namespace/edit state remains safely retained.

Therefore:

```text
fresh-enough read
    != durable payload
    != integrity-qualified payload
    != full replica convergence
```

This synthesis remains deliberately at the namespace/read-admission layer.

---

## 11. The retained relation can be tiny yet constitutive

The technical-retention significance of Case 61 is not that one more scalar is stored.

The important structure is:

```text
authoritative history exists
        +
replica has applied some prefix
        +
client retains what it has already seen
        +
protocol transports that lower bound
        +
server compares lower bound to local progress
        +
maintenance can advance the replica
        +
routing can escape to Active
        =
bounded monotonic/fresh read service
```

Removing any one relation changes the behavior:

- without authoritative progress, the frontier has no reference;
- without replica-applied progress, the server cannot tell whether it has caught up;
- without client lower-bound retention, the server cannot know what this client must not move behind;
- without transport/frontier import, causality across requests/processes can be lost;
- without edit-tail maintenance, lag does not close;
- without admission/wait/retry, stale local state can escape;
- without fallback, service may stall even though an authoritative current view exists.

This is a case where **retention of a relation about prior observation** is constitutive of future service even though the relation is tiny compared with the namespace.

---

## 12. Historical record, engineering reconstruction, analogy, philosophy

### Historical record

Inherited from grounded HDFS Cases 50, 51, and 61:

- QJM persists writer-epoch promises that fence stale namespace writers;
- DataNodes separately track command-source recency and post-failover inventory freshness;
- Observer NameNodes serve reads while following edit-log progress;
- clients retain a maximum seen `stateId`;
- coordinated Observer reads compare client and server progress;
- `msync()` updates a client's frontier through the Active;
- startup synchronization addresses a demonstrated cross-client/process freshness hole;
- edit tailing and Active fallback are separate mechanisms in the released path.

### Engineering reconstruction

Project terms used here include:

- `authoritative progress frontier`;
- `replica-applied frontier`;
- `retained seen-state lower bound`;
- `frontier import`;
- `read-admission closure`;
- the decomposition `authority → progress → client lower bound → maintenance → admission → routing`.

These are explanatory abstractions, not claims about Apache actors' vocabulary.

### Functional analogy

The comparison to Kafka high-watermark/lineage currentness, causal/session guarantees, cache validity, or other follower-read systems is limited to the function “additional retained relation constrains whether surviving state may be served.” It establishes neither mechanism identity nor historical descent.

### Philosophical interpretation

No philosophical claim is needed to establish the mechanism. A later interpretation may ask what it means for a system to retain “how much of the past this observer is already entitled to presuppose,” but that interpretation must remain downstream of the source-grounded protocol.

---

## 13. Prior-art and related-repository boundary

This synthesis makes no invention-priority claim for:

- read replicas;
- monotonic/session reads;
- read-your-writes;
- client session state;
- transaction-number frontiers;
- follower catch-up;
- leader/follower routing;
- or active fallback.

Case 61 already preserves HDFS-12943's own framing of stale follower reads as a pre-existing replicated-system problem and links earlier HDFS Standby-read work.

A fresh repository search found no dedicated HDFS Observer / `stateId` / `msync` treatment in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). A broad history of follower reads, session guarantees, causal consistency, HDFS HA evolution, and later database read-replica mechanisms belongs there if developed. `technical-retention` keeps only the retention-specific relation decomposition.

---

## 14. Bounded conclusion

The roadmap question can now be answered without reducing “freshness” to one scalar or one server role:

```text
mutation authority
    != authoritative transaction progress
    != replica-applied progress
    != client retained seen-state lower bound
    != frontier import
    != edit-tail maintenance
    != read-admission waiting/retry
    != Active fallback
    != full convergence
```

The strongest reusable guardrail is:

> **A surviving readable replica is not automatically admissible for every observer. Correct lagging-replica service can depend on retaining what the client has already seen, transporting that lower bound, comparing it with replica-applied progress, and preserving separate maintenance and routing paths that either close the gap or escape it.**
