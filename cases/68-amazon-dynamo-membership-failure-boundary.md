# Amazon Dynamo Ring Membership: Persistent Change History, Local Failure Suspicion, and Placement Authority

## Status

**`grounded`** — bounded to the membership, failure-detection, and node-add/remove mechanisms described in DeCandia et al.'s 2007 Dynamo paper, especially §§4.8–4.9 and the production discussion in §6.2. Earlier gossip/failure-detection work is used only to block invention-priority claims.

Grounding record: [`../evidence/68-dynamo-2007-membership-failure-grounding.md`](../evidence/68-dynamo-2007-membership-failure-grounding.md).

## Scope

This case asks a question that Case 23 deliberately left in the background:

> When a distributed store distinguishes a node's **durable membership/placement role** from another node's **temporary belief that it is unreachable**, what state must persist, what state may remain local and short-lived, and how does that difference control where retained payload ought to live?

The bounded object is Amazon Dynamo as reported in 2007:

- explicit administrator-initiated ring join/remove operations;
- persisted membership changes and their issue times;
- a history of membership changes reconciled through gossip;
- persisted node-to-token mappings;
- seeds used to reduce the risk of logically partitioned membership views;
- local request-path failure suspicion rather than a required globally consistent liveness view;
- alternate request routing during temporary failures;
- explicit data transfer when membership actually changes.

This is **not**:

- a generic history of group membership, failure detectors, gossip, DHTs, or consistent hashing;
- a claim that Dynamo invented gossip-based failure detection, membership dissemination, consistent hashing, or failure suspicion;
- a claim that a local failure suspicion permanently removes a node from the ring;
- a claim that every node always holds an identical membership view at every instant;
- a claim that a seed is a centralized membership registry or single source of truth;
- a history of DynamoDB or later Amazon storage services;
- a substitute for Case 23's version clocks, sibling reconciliation, hinted-handoff payload placement, and anti-entropy currentness semantics.

## Historical vocabulary

The 2007 paper directly uses:

- `membership change`;
- `join` / `remove`;
- `persistent store`;
- `history` of membership changes;
- `gossip-based protocol`;
- `eventually consistent view of membership`;
- `token` and node/token mappings;
- `seed`;
- `failure detection`;
- `purely local notion of failure detection`;
- `globally consistent view of failure state` as an earlier design that was later rejected;
- `preference list`;
- `transfer` and confirmation during node addition/removal.

Project phrases such as `durable role state`, `ephemeral reachability view`, `placement authority`, and `topology-retention state` are **engineering reconstructions**, not Amazon's historical vocabulary.

## Historical record

### Explicit membership change is persisted as history

In §4.8.1, Dynamo treats ordinary node outages as often transient, including maintenance outages that can last for extended intervals. The paper says such an outage rarely means permanent departure and therefore should not automatically cause partition reassignment or unreachable-replica repair.

Permanent ring membership is changed through an explicit administrator action. The node receiving a join/remove request writes the membership change **and its time of issue** to persistent store. The paper then states that the membership changes form a history because nodes may be removed and added back multiple times.

This gives the first boundary:

> **temporary unreachability ≠ permanent membership departure**.

and:

> **membership change record ≠ payload record**.

The retained history is control-plane state about who belongs to the ring and when membership changed; it is not an object's key/value bytes.

### Membership history is reconciled, not assumed instantly identical

Dynamo gossips membership changes. Each node periodically contacts a random peer and the pair reconciles their **persisted membership change histories**, yielding an eventually consistent membership view rather than an always-identical instantaneous view.

The paper explicitly describes a temporary logical-partition scenario in which two newly joined nodes can each know itself but not yet know the other. Seeds are introduced so nodes have externally discoverable common contact points and can eventually reconcile membership.

Thus:

> **persisted membership history ≠ instantaneous globally identical ring view**.

A control history can survive locally while propagation/convergence of its interpretation across the ring remains incomplete.

### Token ownership is retained separately from payload

A node starting for the first time chooses tokens and builds a node-to-token mapping. The paper says this mapping is persisted on disk, and different nodes reconcile their mappings during the same gossip exchange used for membership histories.

Because key placement and direct request routing derive from these mappings, the following distinction matters:

> **retained object copies ≠ retained placement authority**.

Payload bytes may still exist, but a node also needs membership/token state to determine which nodes should be responsible for a key under the current ring configuration.

### Temporary failure detection is intentionally local

§4.8.3 makes a stronger statement than a generic `failure detector exists`. To avoid failed communication attempts, Dynamo says a **purely local notion** is sufficient: node A can consider B failed because B does not answer A, even while B still answers C.

A then routes operations through alternatives and periodically retries B. Without traffic between two nodes, the paper says they do not particularly need an up-to-date belief about one another's reachability.

This establishes:

> **local failure suspicion ≠ global membership fact**.

and:

> **logical membership ≠ current bilateral reachability**.

The bounded system deliberately allows those state classes to have different scopes and lifetimes.

### Dynamo abandoned a globally consistent failure-state requirement

The paper reports that early Dynamo designs used a decentralized failure detector to maintain a globally consistent failure-state view. The later design concluded this was unnecessary: explicit join/remove handles permanent node additions/removals, while temporary failures are detected locally when communication fails.

This is historical evidence for a deliberate control-state split:

```text
persistent explicit membership history
        !=
local transient reachability suspicion
```

The distinction is not a later philosophical reconstruction imposed on an unspecified implementation; the paper itself narrates the design change.

### Temporary failure rerouting does not itself transfer ring membership

When A locally treats B as unreachable, A can use alternate nodes for requests mapped to B's partitions. Case 23 separately grounds hinted handoff: a temporary substitute can hold a replica plus a hint naming the intended recipient.

In the membership slice, the important point is that this temporary service action does not by itself rewrite the durable ring membership history.

> **alternate request routing ≠ membership transfer**.

and:

> **hinted handoff ≠ ring reconfiguration**.

The system can preserve service through a temporary placement deviation while keeping the intended topology stable enough for later return.

### Explicit membership changes can require payload movement

§4.9 describes a different regime. When node X is explicitly added and assigned token ranges, existing nodes may no longer be responsible for some keys. They offer and, upon confirmation from X, transfer the affected keys. Removal reverses the process.

The confirmation round also prevents duplicate transfers for a given key range.

This supports:

> **durable membership change can create a payload-placement obligation**.

and a narrower safe-retirement rule:

> **transfer initiation ≠ confirmation that the new placement has been accepted**.

The paper does not define this as a transactional commit protocol, so the project should not import stronger atomicity claims.

## Retained state and lifetime split

At least seven state classes should remain separate:

1. **application payload** — key/value versions stored by Dynamo;
2. **version/context state** — Case 23's vector-clock/currentness information;
3. **membership-change history** — persisted join/remove events plus issue times;
4. **node/token mapping** — persisted routing/placement relation;
5. **seed discovery state** — externally known contact points used to reduce membership partitions;
6. **local failure suspicion** — node-relative evidence that a peer is currently unreachable;
7. **hinted-handoff state** — temporary placement metadata naming an intended recipient when a preferred node is unavailable.

They do not need the same persistence horizon. Membership changes and token mappings are persisted; local reachability suspicion can be derived from communication and retried; hints live only until their temporary repair obligation is discharged or otherwise fails.

## Engineering reconstruction

### Not every operational truth should become durable membership state

A tempting design is to treat every observed failure as a topology change. Dynamo's 2007 design explicitly rejects that move for transient outages.

So:

> **ephemeral reachability evidence can safely be less durable than placement-role state**.

The safety claim is bounded: this works because the system has separate mechanisms for routing around temporary failures, retrying peers, hinted handoff, and explicit permanent membership change. It is not a general rule that failure information is disposable.

### Persistent control history can determine where payload ought to live

The membership history and token map are not user data, yet they participate in calculating preference lists and direct routing. They therefore help determine whether a surviving physical copy is on an intended owner, a temporary substitute, or a node that should relinquish keys after a membership change.

> **payload survival ≠ enough information to reconstruct placement intent**.

This extends the repository's recurring rule that retention infrastructure can be constitutive without being the payload itself.

### Membership currentness and liveness currentness are different relations

Dynamo can have a node that is still a ring member but currently unreachable from one peer. It can also have an eventually converging membership view in which nodes have not yet learned the same explicit change.

Hence at least three questions must be separated:

```text
Is B a ring member?
Is B reachable from A now?
Has A learned the latest membership history?
```

A single Boolean `node is current` hides three different state relations.

### Routing around a failure can preserve topology while changing embodiment

The local failure path allows a requester/coordinator to choose alternates without first changing ring membership. Case 23's hinted handoff then lets actual physical replica location deviate from preferred placement while retaining an intended destination.

This produces a strong retention relation:

> **service continuity can be achieved by changing the current embodiment without changing durable role identity**.

This is analogous only functionally to local remapping in Flash/HDD cases; the mechanism here is distributed and membership-governed.

### Membership history is a history-retention mechanism with a narrow purpose

Dynamo explicitly retains a history of membership changes, but this is not an archive of all operational events. It does not preserve every packet loss, request failure, temporary suspicion, or payload transition.

> **control-plane history retention ≠ complete operational history retention**.

The history is kept because repeated remove/add cycles and delayed dissemination must still be reconciled into a usable ring view.

## Cross-case boundaries

### Versus Case 23 — Dynamo divergent versions / hinted handoff

Case 23 asks which object versions remain admissible and how temporary payload placement/replica divergence is repaired. Case 68 asks what topology/control state distinguishes **permanent role change** from **temporary reachability failure**.

The same system therefore carries at least two independent kinds of `currentness`:

- object/version currentness;
- membership/placement-role currentness.

Neither can substitute for the other.

### Versus Case 05 — RADOS peering and repair

Both RADOS and Dynamo maintain distributed placement/repair control state.

**Functional analogy only:** bounded RADOS peering uses cluster-map/version/PG authority to establish a serviceable current PG state; Dynamo's 2007 design explicitly permits local disagreement about temporary reachability and does not require a globally consistent failure-state view. Shared replication vocabulary does not establish identical authority semantics.

### Versus Case 61 — HDFS Observer freshness

Case 61 carries a client-observed transaction frontier used to reject too-stale read replicas. Case 68 carries membership/token history used to decide node role and placement plus local failure suspicion used to avoid unreachable peers.

A monotonic read frontier and a ring-membership history are different control-state types even though both can determine whether a physical replica is eligible for some operation.

### Versus Cases 04 and 14 — Flash/HDD remapping

All can keep a logical designation while changing physical embodiment.

**Functional analogy only:** Flash/HDD remapping is controller-local mapping/replacement; Dynamo separates a distributed durable membership/placement relation from transient node-relative reachability and temporary handoff placement.

## Failure and forgetting boundaries

Distinct failure modes include:

- persisted membership history is lost or corrupted;
- node/token mapping is lost or inconsistent;
- gossip delay leaves nodes with different membership views for too long;
- seed discovery is misconfigured or unavailable during bootstrap/reconciliation;
- a temporary outage is mistakenly turned into an explicit permanent removal;
- a permanent membership change is not disseminated sufficiently;
- local reachability suspicion is stale and causes avoidable alternate routing;
- key transfer after a real membership change fails or remains incomplete;
- temporary hinted replicas disappear before handoff, leaving Case 23's anti-entropy path to protect durability;
- surviving payload copies remain while the control state needed to decide intended placement is unavailable.

These are not one generic `replica failure` condition.

## Historical record / reconstruction / interpretation ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| explicit join/remove writes a membership change and issue time to persistent store | `H/P` | Dynamo §4.8.1 |
| membership changes form a history and persisted histories are reconciled through gossip | `H/P` | Dynamo §4.8.1 |
| node/token mappings are persisted and reconciled | `H/P` | Dynamo §4.8.1 |
| seeds reduce the risk of logically partitioned membership views | `H/P` | Dynamo §4.8.2 |
| node A may locally consider B failed while C can still reach B | `H/P` | Dynamo §4.8.3 |
| later Dynamo design did not require a globally consistent failure-state view | `H/P` | Dynamo §4.8.3 |
| local failure suspicion permanently removes B from ring membership | `X` | contradicted by explicit join/remove separation |
| alternate request routing is itself durable ownership transfer | `X` | not established; temporary failure path preserves membership distinction |
| seed is a centralized membership registry | `X` | paper presents seeds as discovery/reconciliation aids inside a decentralized system |
| payload survival alone is sufficient to recover intended placement | `E/X` | token/membership state is separately persisted and used for placement |
| control-state lifetime can be shorter when it is cheaply re-derived and does not define durable role | `E` | bounded to local reachability suspicion versus persisted membership |
| Dynamo invented gossip-based failure detection | `X` | earlier primary literature and Dynamo's own references predate 2007 |

## Philosophical interpretation — bounded

Case 68 adds one narrow conceptual pressure:

> **Technical retention may require preserving not only an object but a durable account of its role relations, while deliberately refusing to make every transient observation equally durable.**

The important contrast is not `remembering versus forgetting` in a human sense. It is an engineering division between a persisted history that defines membership/placement and a local, revisable suspicion used only to avoid a currently unreachable path.

That distinction helps make `technical retention` less object-centric: what must outlive a moment can be the **relation that says where an object belongs**, while another operational belief about the same node may be safely regenerated from new communication.

## Cross-case result

```text
payload copy
    !=
version/currentness state
    !=
persisted membership-change history
    !=
persisted node/token placement map
    !=
local reachability suspicion
    !=
temporary hinted placement
    !=
confirmed membership-driven transfer
```

The strongest new result is:

> **A distributed retention system can intentionally give durable topology-role state and transient reachability state different persistence semantics, because confusing temporary failure with permanent membership change would itself create destructive maintenance work.**

## Prior art and anti-anachronism

Dynamo's paper says the system is a synthesis of well-known techniques and cites earlier work on scalable distributed failure detectors. Earlier Cornell work by van Renesse, Minsky, and Hayden in 1998 describes a gossip-style failure-detection service, and SWIM (Das, Gupta, Motivala, 2002) explicitly separates failure detection from membership-update dissemination in a scalable membership protocol.

Therefore do **not** claim:

- Dynamo invented gossip;
- Dynamo invented failure detectors;
- Dynamo invented group membership;
- Dynamo invented the conceptual distinction between failure detection and membership dissemination;
- Dynamo invented consistent hashing or DHT membership.

The defensible 2007-specific claim is narrower:

> **Dynamo documented a production storage composition in which explicit join/remove changes and node/token maps are persisted and gossip-reconciled, while temporary unreachability is handled by node-local suspicion, alternate routing, and repair paths without requiring a globally consistent failure-state view.**

That composition is sufficient for this retention comparison without an invention-priority story.

## Sources

1. Giuseppe DeCandia et al., **“Dynamo: Amazon's Highly Available Key-value Store,”** SOSP '07, 2007. Amazon Science publication record: <https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store>. Author-hosted full online version: <https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html>.
2. Robbert van Renesse, Yaron Minsky, Mark Hayden, **“A Gossip-Style Failure Detection Service,”** Middleware '98 / Cornell technical-report lineage, 1998: <https://www.cs.cornell.edu/projects/spinglass/public_pdfs/Gossip%20Style%20Failure.pdf>.
3. Abhinandan Das, Indranil Gupta, Ashish Motivala, **“SWIM: Scalable Weakly-consistent Infection-style Process Group Membership Protocol,”** DSN 2002: <https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/SWIM.pdf>.

## Related repositories

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for dedicated Dynamo membership/failure-detection treatment returned no matching case. A full history of process-group membership, failure detectors, gossip protocols, DHT routing, and consistent-hashing membership belongs there if pursued later. This case keeps only the retention-specific relation among persisted role history, temporary reachability evidence, and payload placement.
