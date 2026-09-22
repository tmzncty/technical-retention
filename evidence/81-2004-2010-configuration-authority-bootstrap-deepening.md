# Case 81 deepening — configuration authority, retained master state, and bootstrap (2004–2010)

## Status

**`bounded deepening complete`**

**Case 81 remains `grounded`.**

This slice deepens a previously open Case 81 question: the object replicas can retain payload and in-process update obligations, but what retains the **configuration authority** that tells those replicas which chain exists, which server is head or tail, and how a failed edge is rewired?

It is deliberately narrower than a general history of configuration services or consensus. It also does not reopen the already-covered `Sent_i` suffix-repair mechanism or Hibari WAL safe-serial frontier.

The evidence supports a useful separation:

```text
replicated payload
    != retained configuration authority

live configuration process
    != retained configuration state

configuration-state replication
    != data-chain replication
```

---

## Research question

The 2004 Chain Replication protocol assigns reconfiguration work to a `master`. The protocol's storage-server fault tolerance therefore depends on another state-bearing authority outside the chain itself.

By 2010, Hibari exposes this boundary more concretely: an active Admin Server can fail and restart, while its private management state is separately replicated across cluster bricks. Hibari also avoids storing that private state with chain replication because doing so would make Admin Server bootstrap depend on the very configuration service being bootstrapped.

The narrow question is therefore:

> what configuration state must survive so that otherwise surviving object replicas can again be interpreted as a valid chain after management-process failure or cluster reconfiguration?

---

## Source ledger

### P1 — van Renesse & Schneider, OSDI 2004

**Source:** Robbert van Renesse and Fred B. Schneider, “Chain Replication for Supporting High Throughput and Availability,” *6th Symposium on Operating Systems Design & Implementation (OSDI 04)*, USENIX Association, December 2004, pp. 91–104.

- USENIX record: <https://www.usenix.org/conference/osdi-04/chain-replication-supporting-high-throughput-and-availability>
- Full HTML: <https://www.usenix.org/legacy/events/osdi04/tech/full_papers/renesse/renesse_html/index.html>
- PDF: <https://www.usenix.org/event/osdi04/tech/full_papers/renesse/renesse.pdf>

**Directly inspected location:** §3, the failure-reconfiguration discussion describing the `master`, its predecessor/successor and head/tail duties, the simplifying assumption that it never fails, and the prototype note that the master is replicated with Paxos.

**Evidence class:** contemporary primary protocol paper (`H/P`).

### P2 — Fritchie, Erlang Workshop 2010

**Source:** Scott Lystig Fritchie, “Chain Replication in Theory and in Practice,” *Erlang'10*, September 30, 2010, pp. 33–44, DOI `10.1145/1863509.1863515`.

- Author-hosted paper: <https://www.snookles.com/scott/publications/erlang2010-slf.pdf>
- Author slides: <https://www.snookles.com/scott/presentations/erlang2010-slf-slides.pdf>

**Directly inspected locations:** §7 and the scaling discussion later in the paper: active/standby Admin Server behavior, Admin Server private-state replication, bootstrap circularity, network-partition handling, and private-state update bottlenecks.

**Evidence class:** contemporary primary implementation report (`H/P`).

### S1 — van Renesse author retrospective

**Source:** Robbert van Renesse, Cornell University home page, “Chain Replication” section.

- <https://www.cs.cornell.edu/home/rvr/>

The page retrospectively says a downside of the original protocol is that it requires a configuration service and discusses later work on self-reconfiguration.

**Evidence class:** later author retrospective (`H/S`). It is used only as a retrospective boundary, not to rewrite what the 2004 paper itself specified.

---

## Historical record

### H/P — the 2004 `master` is part of the service's currentness machinery

The OSDI paper gives the `master` several duties that cannot be reduced to storing user payload:

- detecting server failures;
- informing surviving servers when their predecessor or successor changes;
- telling clients which server is the current head or tail.

These duties determine where an update may enter, where a query may be served, and which newly connected chain edge is legitimate.

Thus the original protocol already contains two different retained relations:

```text
object state / in-process update state
    !=
configuration and role authority
```

The latter is not merely an operator convenience. The suffix-repair and new-tail procedures described elsewhere in Case 81 require a current answer to “who is my successor?”, “who is the tail?”, and “which configuration should clients use?”.

### H/P — the paper simplifies the proof story by assuming a non-failing master

For exposition, the 2004 paper assumes a single master process that never fails.

That assumption is intentionally stronger than the storage-server failure model. It means the paper's claim that a chain can tolerate storage-server failures must not be silently rephrased as:

```text
all service control state is itself failure-free by theorem
```

The object-chain protocol and the configuration service have different fault-handling responsibilities.

### H/P — the 2004 prototype used Paxos replication for the master

The same paragraph immediately notes that the prototype did not literally rely on one immortal process. It replicated the master on multiple hosts using Paxos so that the replicas behaved collectively like the assumed non-failing master.

This establishes a historical implementation fact:

```text
chain-replicated storage servers
    + separately replicated configuration authority
```

It does **not** by itself establish the exact durable representation of Paxos state, the stable-storage boundary of the master replicas, the configuration-version format, or the ordering between a configuration decision and every server/client observing that decision.

### H/P — Hibari 2010 keeps one active Admin Server authority even with active/standby processes

Fritchie's 2010 implementation report says Hibari runs its Admin Server in an active/standby arrangement under Erlang/OTP application control. If the active machine crashes, the current Admin Server service is lost until restart/failover; the paper reports a restart time on the order of ten seconds in the described environment.

The important retention distinction is not the exact number of seconds. It is:

```text
current active management process
    !=
management state that must survive process loss
```

The paper treats brick crash/restart handling, status administration, and cluster reconfiguration as Admin Server responsibilities. Ordinary data-path activity and configuration-changing activity are therefore not the same availability problem.

### H/P — Hibari retains Admin Server private state separately across cluster bricks

Fritchie states that the Admin Server has private state, including histories concerning logical-brick and chain down/up status, and that this state is distributed across cluster bricks.

This is direct implementation evidence that configuration authority itself has retained state. It is not reconstructed merely from the fact that a control plane exists.

The state is also semantically different from user objects:

```text
user object payload
    !=
brick/chain administrative history
    !=
active Admin Server process memory
```

### H/P — Hibari deliberately does not chain-replicate the Admin Server's private state

The 2010 report explains the bootstrap problem explicitly. If Admin Server private state were itself managed by chain replication, recovering the Admin Server would first require knowing the chain configuration needed to access that private state. But the Admin Server is itself the component responsible for providing/managing that configuration.

Hibari cuts this circular dependency by replicating Admin Server private state with a **quorum-voting style** mechanism rather than with the normal chain-replication path.

This is unusually clean evidence for a control-plane bootstrap boundary:

```text
recover configuration authority
    cannot naively require
already-recovered configuration authority
```

and:

```text
data replication mechanism
    !=
bootstrap replication mechanism
```

### H/P — configuration-state traffic can become a real scaling bottleneck

Later in the same report, Fritchie identifies updates to the Admin Server's private-state storage bricks as a bottleneck. Private-state updates are serialized, and a sufficiently large simultaneous wave of logical-brick startup transitions can exceed the update rate of those state-storage bricks; the paper gives an example involving more than roughly 3000 logical bricks booting at once.

This matters because it rejects another weak framing:

```text
configuration metadata = tiny static decoration
```

No. In the described system, topology/health history is an actively changing write workload whose update capacity can constrain cluster recovery/startup behavior.

### H/P — retained configuration state does not eliminate uncertainty about failure truth

Fritchie also spends substantial effort on the difference between a crashed node, a slow node, and a network partition. Hibari's partition detector can refuse Admin Server initialization when it suspects a partition, raise an alarm, and leave the management process idle pending intervention.

Therefore separate:

```text
configuration state survives
    !=
current failure observation is correct
    !=
new configuration is safe to authorize
```

Persistent control state can preserve previous knowledge without turning an ambiguous network observation into a perfect failure oracle.

---

## Retained-state decomposition

For this slice, keep at least the following state classes distinct.

### 1. User/object payload

The value or object replica stored by the chain's bricks.

### 2. In-process update obligation

The 2004 protocol's `Sent_i` state, covered by the original Case 81 grounding, remembers forwarded work whose tail completion is not yet known.

### 3. Local durability progress

The Hibari WAL safe-serial frontier, covered by the existing 2010 WAL deepening, records how far a brick's ordered local stream has crossed the implementation's intended flush boundary.

### 4. Current chain topology and role assignment

The relation that says which server is head, tail, predecessor, successor, or outside the chain.

### 5. Configuration-service private/history state

Hibari's Admin Server retains management history such as brick/chain up/down transitions separately from user payload.

### 6. Active management-process liveness

Whether a process currently exists that can interpret and act on retained configuration state.

### 7. Failure-observation state

Evidence or suspicion that a brick, host, link, or partition has failed. This evidence can be wrong or ambiguous even if prior configuration state is intact.

### 8. Configuration publication / client-routing knowledge

Clients and servers must eventually learn which head/tail or predecessor/successor relation is current. The sources inspected here do not establish one universal atomic publication event across every participant.

---

## Engineering reconstruction

### E — replication moves some correctness burden into small control state

Three copies of an object do not answer which copy is tail or which chain membership is current.

Therefore:

```text
payload redundancy
    !=
configuration redundancy
```

The latter can be much smaller in bytes while still controlling the interpretation and use of the former.

### E — process failover is not the same as state recovery

A standby process becoming runnable is a liveness event. Recovering enough authoritative state to make correct reconfiguration decisions is a state-continuity event.

The two may be coupled in one implementation, but they should not be collapsed in analysis.

### E — the control plane needs its own recovery root

Hibari's choice to keep Admin private state outside normal chain replication is a concrete instance of a general bootstrap constraint:

```text
if service A decides how service B is configured,
then recovering A solely through B's already-valid configuration
can create a circular dependency.
```

The engineering response in this implementation is not “no retained control state”; it is **a differently replicated retained control state**.

### E — membership change is an authorization event, not just a topology observation

A node being unreachable does not by itself prove that the system may safely forget it, promote another node, or publish a new chain. Hibari's partition discussion shows that reachability evidence and reconfiguration authority remain distinct.

### E — full-service fault tolerance is layered

The 2004 paper's storage-server tolerance argument should be read under its stated master assumption. A data chain may have enough surviving replicas while configuration-changing operations are temporarily unavailable because the configuration authority is down or intentionally refusing to initialize.

Thus:

```text
sufficient surviving data replicas
    !=
all control-plane transitions currently admissible
```

### E — configuration history can become a recovery workload

Hibari's private-state bottleneck during large startup waves shows that control-state recovery/update is not free. The system may retain all required bytes yet still be constrained by the rate at which authoritative configuration transitions can be recorded and processed.

---

## Functional comparisons — not genealogy

### A — Case 50, HDFS QJM epoch fencing

Both cases show that authority over surviving payload depends on retained control state that is smaller than the payload itself.

- HDFS QJM uses epochs/fencing and quorum-journal relations to bound which NameNode may act.
- Chain Replication uses a configuration authority to define head/tail and predecessor/successor roles; Hibari separately retains Admin private state.

The similarity is functional. No descent or common implementation is asserted.

### A — Case 68, Dynamo membership/failure boundary

Both systems distinguish payload replication from membership/failure knowledge. Dynamo's gossip/membership and sloppy-quorum behavior belong to a different consistency/failure regime; it is useful only as a comparison showing that “replica exists” and “replica counts in the current authority relation” are separate questions.

### A — Case 81 `Sent_i` and WAL safe serial

Within the same case, three compact control relations serve different purposes:

```text
Sent_i
    -> unfinished downstream/tail obligation

safe serial
    -> local persistence prefix

configuration authority state
    -> which chain/role relation may act
```

Their small size and administrative appearance do not make them interchangeable.

---

## Philosophical interpretation — bounded

### I — redundancy does not eliminate the need for an interpretation of “current”

The supported lesson is technical: multiple surviving embodiments of an object still require a retained relation that says which topology and role assignment is authoritative.

This is not a claim that every distributed system has one centralized “true copy”, nor a general metaphysical thesis about identity.

### I — a small control record can govern a much larger retained object set

Configuration state may be tiny relative to stored payload, yet losing or corrupting it can prevent the system from safely using otherwise intact replicas. This is a concrete retention relation, not an argument that metadata is universally more important than data.

---

## Explicit non-claims

This slice does **not** claim that:

1. the 2004 Chain Replication paper invented configuration services, failure detectors, Paxos, membership, or master/standby control planes;
2. “prototype replicated the master with Paxos” proves a particular Paxos log format or stable-storage implementation;
3. the 2004 paper proves that every master/configuration decision survives total power loss;
4. the 2004 paper specifies a persisted configuration epoch, generation number, or fencing token unless explicitly shown elsewhere;
5. the storage-chain `t-1` failure tolerance claim is a theorem that every control-plane component simultaneously tolerates the same failures;
6. a surviving copy of object payload is automatically a valid head or tail;
7. a new predecessor/successor relation is safe merely because a network connection can be opened;
8. Hibari's active/standby Admin Server arrangement is itself the mechanism that persists Admin private state;
9. Hibari's quorum-style Admin-state replication is the same protocol as chain replication;
10. distributed Admin private state means every management transition is synchronously durable before any effect is visible;
11. the reported roughly ten-second Admin restart time is a universal Hibari timing guarantee;
12. an Admin Server outage implies all client data operations are unavailable for exactly that interval;
13. retained configuration history makes network partition and crash perfectly distinguishable;
14. a partition detector is a consensus protocol or a perfect failure oracle;
15. the >3000-logical-brick startup example establishes a universal cluster-size ceiling;
16. serialized private-state updates imply user-data writes are serialized globally;
17. the production incidents discussed by Fritchie prove that chain replication as a protocol is inherently unsafe;
18. the later Cornell retrospective is substituted for the 2004 primary paper;
19. similarity to HDFS, Dynamo, ZooKeeper, Raft, or other systems establishes genealogy;
20. this slice closes the exact durable-state semantics of the 2004 prototype master or Hibari Admin-state quorum implementation.

---

## Claim ledger

| Claim | Type | Evidence |
| --- | --- | --- |
| the 2004 master detects server failures and publishes predecessor/successor and head/tail changes | `H/P` | P1 §3 |
| the paper assumes a single non-failing master for exposition | `H/P` | P1 §3 |
| the prototype replicated the master on multiple hosts using Paxos | `H/P` | P1 §3 |
| this does not expose the exact stable-storage contract of the master replicas | `E/X` | absence boundary after direct inspection of P1 |
| Hibari runs an Admin Server in an active/standby arrangement | `H/P` | P2 §7 |
| Hibari separately distributes Admin Server private state across cluster bricks | `H/P` | P2 §7 |
| Hibari avoids chain-replicating that private state because of bootstrap circularity | `H/P` | P2 §7 |
| Hibari instead uses a quorum-voting style replication mechanism for Admin private state | `H/P` | P2 §7 |
| Admin private-state updates can bottleneck large simultaneous startup transitions | `H/P` | P2 scaling discussion |
| partition suspicion can prevent Admin initialization and require intervention | `H/P` | P2 §7 |
| payload redundancy and configuration redundancy are distinct retention obligations | `E` | P1 + P2 |
| a configuration service needs a recovery root that does not circularly depend on its own already-valid output | `E` | P2 bootstrap rationale |
| later author commentary describes external configuration service dependence as a downside of the original design | `H/S` | S1 |

---

## Cross-repository duplication check

A current GitHub search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Chain Replication` returned no dedicated technical-history packet.

**Decision:** retain only the configuration-state/currentness decomposition here. If a broader genealogy of configuration services, Paxos implementations, master failover, or replication-control planes is later developed, put that historical engineering narrative in `computing-archaeology` and link to it rather than duplicating it here.

---

## Remaining evidence debt

This deepening narrows the earlier generic “master/configuration-service durability” gap to a smaller set of concrete questions:

- find the 2004 prototype master implementation or companion description that exposes the actual Paxos state representation and stable-storage boundary;
- identify whether configuration decisions had explicit epochs/generations and how stale master/client views were fenced;
- inspect Hibari source for the exact Admin private-state quorum read/write protocol, persistence boundary, retry behavior, and repair behavior;
- determine what configuration state survives a total cluster restart and how it is reconstituted before normal chain admission;
- fault-inject between Admin private-state update, topology publication, brick reconfiguration, and client routing update;
- distinguish “configuration accepted by control plane” from “configuration observed by every server/client”.

These are implementation/source-code debts, not reasons to weaken the established historical claims above.

---

## Promotion decision

**Case 81 remains `grounded`.**

This slice materially strengthens one previously open control-plane dimension, but it does not justify a maturity promotion. Exact persistent state transitions for the 2004 prototype master and Hibari's Admin private-state quorum mechanism remain unverified, and the case still lacks direct fault-injection evidence for configuration-update crash windows.
