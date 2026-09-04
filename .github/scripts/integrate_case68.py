from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
CASE_PATH = "cases/68-amazon-dynamo-membership-failure-boundary.md"
EVIDENCE_PATH = "evidence/68-dynamo-2007-membership-failure-grounding.md"

case = r'''# Amazon Dynamo Ring Membership: Persistent Change History, Local Failure Suspicion, and Placement Authority

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
'''

evidence = r'''# Evidence Record 68 — Dynamo 2007 Membership History, Failure Suspicion, and Placement Authority

## Promotion target

Ground [`cases/68-amazon-dynamo-membership-failure-boundary.md`](../cases/68-amazon-dynamo-membership-failure-boundary.md) as a bounded distributed-control-state retention case.

The question is not `how does distributed membership work?` generally. It is:

> **What does Dynamo 2007 persist to represent durable ring membership/placement, what does it intentionally leave as local transient failure suspicion, and how does that lifetime split prevent temporary outages from becoming permanent topology changes?**

## Evidence status

**Result:** sufficient for `grounded`.

Reasons:

- the central mechanism is directly stated in the 2007 Dynamo paper's §§4.8–4.9 and §6 discussion;
- Amazon Science independently anchors the paper's 2007 publication identity;
- the author-hosted HTML edition exposes exact period wording for persisted membership-change history, token mappings, local failure suspicion, abandoned global failure-state view, and membership-driven key transfer;
- earlier gossip/failure-detection literature is used to block novelty claims rather than to retrofit Dynamo semantics;
- `computing-archaeology` was searched for a dedicated Dynamo membership/failure-detection case and no matching treatment was found;
- historical terms, engineering reconstruction, functional analogy, and philosophical interpretation remain explicitly separated.

This record does not claim a named later DynamoDB implementation, exact hidden production data structures, or a consensus protocol that the paper does not specify.

---

## Source A — DeCandia et al., Dynamo, SOSP 2007

### Bibliographic identity

Giuseppe DeCandia, Deniz Hastorun, Madan Jampani, Gunavardhan Kakulapati, Avinash Lakshman, Alex Pilchin, Swaminathan Sivasubramanian, Peter Vosshall, and Werner Vogels, **“Dynamo: Amazon's Highly Available Key-value Store,”** *Proceedings of the 21st ACM Symposium on Operating Systems Principles (SOSP '07')*, 2007.

Amazon Science:

<https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store>

Author-hosted full online version:

<https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html>

### Inspection level

**Primary / direct full-text inspection through the author-hosted HTML edition.**

The bounded anchors are:

- §4.8.1 Ring Membership — persisted membership changes, timestamps, history, gossip reconciliation, persisted node/token mappings;
- §4.8.2 External Discovery — seeds and temporary logical membership partitions;
- §4.8.3 Failure Detection — purely local suspicion and rejection of a globally consistent failure-state requirement;
- §4.9 Adding/Removing Storage Nodes — membership-driven key movement and confirmation;
- §6.2 / production partition-strategy discussion — metadata-size pressure, recovery/bootstrap effects, and coordination cost of membership change.

---

## Source A claim ledger

### A1 — transient outage is not automatically permanent departure

**Labels:** `H/P`

**Anchor:** §4.8.1.

The authors state that node outages from failures or maintenance are often transient, can last extended intervals, and rarely signify permanent departure. They explicitly say such outages should not cause partition-assignment rebalancing or unreachable-replica repair merely because the node is temporarily absent.

**Established:** transient reachability failure and permanent ring membership are distinct historical design categories.

**Not established:** that all temporary outages are harmless or need no repair path.

### A2 — membership changes are explicit, persisted, and historical

**Labels:** `H/P`

**Anchor:** §4.8.1.

An administrator explicitly joins/removes a node. The node receiving the command writes the membership change and its issue time to persistent store. The paper says membership changes form a history because a node can be removed and added back multiple times.

**Established:** Dynamo retains control-plane history, not merely an instantaneous membership bitset.

**Engineering consequence (`E`):** role/topology state has a persistence obligation distinct from temporary liveness observations.

### A3 — membership histories converge through gossip

**Labels:** `H/P`

**Anchor:** §4.8.1.

Each node periodically contacts a random peer, and the pair reconcile their persisted membership-change histories. The result is described as an eventually consistent membership view.

**Established:** persistence of a local history does not imply instantaneous network-wide agreement about it.

### A4 — node/token mappings are also persisted and reconciled

**Labels:** `H/P`

**Anchor:** §4.8.1.

A node chooses tokens on first start, records node-to-token mappings on disk, and reconciles mappings with peers during the same gossip exchange. The paper ties this state to awareness of token ranges and direct routing of read/write requests.

**Established:** routing/placement intent depends on retained metadata separate from key/value payload.

### A5 — seeds reduce membership partition risk without becoming a central registry

**Labels:** `H/P`

**Anchor:** §4.8.2.

The paper describes a temporary state in which independently joined nodes know themselves but not each other. Some nodes act as externally discoverable seeds known to all nodes; eventual reconciliation with a seed makes logical partitions highly unlikely.

**Established:** common discovery points help membership convergence.

**Not established:** that seeds serialize all membership changes or are a single authoritative central database.

### A6 — failure suspicion is intentionally node-local

**Labels:** `H/P`

**Anchor:** §4.8.3.

For avoiding failed communication attempts, Dynamo says a purely local notion is enough: A can consider B failed if B does not answer A even when B answers C. A uses alternatives and retries B later.

**Established:** `A suspects B` is not a globally agreed membership fact.

### A7 — failure knowledge need not be continuously maintained without traffic

**Labels:** `H/P`

**Anchor:** §4.8.3.

The authors state that if client traffic does not create communication between two nodes, neither particularly needs to know the other's current reachability.

**Established:** some liveness state can be demand-derived rather than continuously retained with a global consistency obligation.

### A8 — early global failure-state view was deliberately abandoned

**Labels:** `H/P`

**Anchor:** §4.8.3.

The paper says early Dynamo designs used a decentralized failure detector to maintain a globally consistent failure-state view. Later, explicit join/leave for permanent changes plus local communication failure for temporary outages made that global view unnecessary.

**Established:** the membership/liveness lifetime split is an explicit reported design evolution, not merely a modern analogy.

### A9 — permanent membership change creates real data movement

**Labels:** `H/P`

**Anchor:** §4.9.

Adding X changes token responsibility. Existing nodes transfer keys for ranges X now owns. Removal reverses the process. The authors describe an offer/confirmation transfer step and a confirmation round that prevents duplicate transfer for a key range.

**Established:** durable role changes can produce downstream payload-placement work.

**Boundary:** the paper does not specify a general transaction/atomic-commit theorem for all membership changes.

### A10 — membership metadata has scaling and operational cost

**Labels:** `H/P`

**Anchor:** §6.2 and conclusion discussion.

The paper reports that a refined partition strategy reduced per-node membership information by three orders of magnitude relative to one earlier strategy, improves bootstrap/recovery, and notes that changing membership under the refined strategy requires coordination to preserve assignment properties. It also describes Dynamo as using a full membership model in which nodes actively gossip routing information.

**Established:** retained control-plane state consumes storage/communication/coordination resources and its representation is an engineering design variable.

---

## Source B — Amazon Science publication record

### Source

Amazon Science, **“Dynamo: Amazon's highly available key-value store”**:

<https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store>

### Use

Institutional metadata independently anchors:

- title and author list;
- 2007 year;
- SOSP conference identity;
- Dynamo as a highly available key-value storage system used for Amazon service state.

Mechanism details remain grounded in Source A.

---

## Source C — van Renesse, Minsky, Hayden, gossip-style failure detection, 1998

### Source

Robbert van Renesse, Yaron Minsky, Mark Hayden, **“A Gossip-Style Failure Detection Service,”** 1998 Middleware / Cornell technical-report lineage:

<https://www.cs.cornell.edu/projects/spinglass/public_pdfs/Gossip%20Style%20Failure.pdf>

### Inspection level

**Primary-paper text / mechanism-level prior-art boundary.**

The paper describes a scalable failure detector based on random gossip and discusses probabilistic false reporting, failure/unreachability detection, and scaling properties.

### Use

This blocks any claim that Dynamo 2007 invented gossip-based failure detection.

**Not used to claim:** that Dynamo's explicit persistent ring-membership history is algorithmically identical to the 1998 service.

---

## Source D — SWIM, 2002

### Source

Abhinandan Das, Indranil Gupta, Ashish Motivala, **“SWIM: Scalable Weakly-consistent Infection-style Process Group Membership Protocol,”** DSN 2002:

<https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/SWIM.pdf>

### Inspection level

**Primary-paper abstract/conclusion-level prior-art boundary.**

SWIM explicitly separates failure-detection functionality from membership-update dissemination and uses infection-style dissemination.

### Use

This blocks a broad priority story that Dynamo introduced the general idea of separating failure detection from membership dissemination.

**Not used to claim:** that SWIM and Dynamo have the same membership semantics. Dynamo's bounded distinction is specifically explicit persistent join/remove history versus node-local temporary reachability suspicion in a storage-placement system.

---

## Prior-art / novelty boundary

Reject:

| Claim | Status | Reason |
| --- | --- | --- |
| `Dynamo invented gossip-based failure detection` | **rejected** | primary gossip failure-detection work predates 2007 |
| `Dynamo invented failure detectors` | **rejected** | much older distributed-systems literature exists; Dynamo itself cites earlier failure-detector work |
| `Dynamo invented separating failure detection from membership dissemination` | **rejected** | SWIM 2002 supplies an explicit earlier separation |
| `Dynamo invented consistent hashing / DHT membership` | **rejected** | Dynamo explicitly describes a synthesis of prior techniques and cites earlier consistent-hashing/DHT work |
| `Dynamo membership = DynamoDB membership` | **rejected** | this case is bounded to the internal 2007 system |

The defensible historical claim is the **Dynamo-specific composition** of:

```text
explicit join/remove
    -> persisted membership-change history + issue time
    -> gossip reconciliation
    + persisted node/token mapping

while

temporary communication failure
    -> local suspicion
    -> alternate request routing / retry
    -> no automatic permanent membership removal
```

---

## In-repository boundaries

### Case 23 — object divergence and hinted handoff

[`../cases/23-amazon-dynamo-divergent-version-anti-entropy.md`](../cases/23-amazon-dynamo-divergent-version-anti-entropy.md) already grounds version clocks, sibling retention, hinted temporary replicas, read repair, and anti-entropy. Case 68 does not duplicate those mechanisms. It isolates the **topology/liveness state split** that determines whether a failure is a temporary routing problem or an explicit membership change.

### Case 05 — RADOS

Both systems retain placement/repair metadata. Comparison is functional only: RADOS peering/currentness rules and Dynamo's local failure suspicion are not one historical or protocol mechanism.

### Case 61 — HDFS Observer

Client freshness state is not membership state. A read lower bound and a node/token placement history can both qualify service but encode different relations.

### Cases 04 / 14 — remapping

Stable designation across changing physical embodiment is a useful analogy. No genealogy is claimed between device-local remapping and Dynamo's distributed membership/placement control.

---

## Historical record / engineering reconstruction / interpretation separation

### Historical record (`H/P`)

Directly established:

- explicit administrator join/remove;
- persisted change + time of issue;
- membership-change history;
- gossip reconciliation of persisted histories;
- persisted node/token maps;
- seeds as discovery/reconciliation aids;
- local failure suspicion sufficient for request-path avoidance;
- early globally consistent failure-state design abandoned;
- membership-driven key transfer and confirmation.

### Engineering reconstruction (`E`)

Project terms:

- `durable role state`;
- `ephemeral reachability view`;
- `topology-retention state`;
- `placement authority`;
- `payload survival ≠ enough information to reconstruct placement intent`;
- `service continuity can change embodiment without changing durable role identity`.

### Functional analogy (`A`)

- RADOS: distributed placement/currentness metadata, different authority semantics;
- mapped Flash / HDD reassignment: logical designation across changed embodiment, different mechanism and scope;
- HDFS Observer: small control state can qualify service, but freshness frontier ≠ membership history.

No genealogy follows.

### Philosophical interpretation (`I`)

The bounded interpretation is only that a system may need to retain a **role relation** while intentionally allowing a transient observation about that role-holder to expire/rederive. This is not a claim about human memory or social identity.

---

## What the evidence does not establish

The sources do not establish:

- exact internal serialization/schema of Dynamo membership records;
- a consensus protocol for membership changes;
- instantaneous agreement on ring membership;
- exact production durability medium for every membership-history deployment;
- that seeds are centralized authorities;
- that local suspicion is always correct;
- all crash/restart edge cases for membership persistence;
- modern DynamoDB membership behavior;
- first-invention priority for gossip, failure detectors, or DHT membership.

These remain separate research questions.

## Related-repository duplication check

A current search of `tmzncty/computing-archaeology` for `Dynamo membership failure detection gossip` returned no dedicated treatment. If a broader process-group/failure-detector/DHT history is developed, it belongs there. This record keeps only the retention-specific lifetime split among payload, placement-role history, and temporary reachability evidence.
'''

readme_case_line = "- [`cases/68-amazon-dynamo-membership-failure-boundary.md`](cases/68-amazon-dynamo-membership-failure-boundary.md) — grounded Dynamo 2007 control-state slice: explicit ring join/remove and node/token maps are persisted and gossip-reconciled, while temporary unreachability is intentionally node-local and need not become a durable membership change; separates placement-role retention from transient reachability evidence."
readme_evidence_line = "- [`evidence/68-dynamo-2007-membership-failure-grounding.md`](evidence/68-dynamo-2007-membership-failure-grounding.md) — Case-68 grounding record: exact Dynamo §§4.8–4.9 membership/failure anchors plus pre-2007 gossip/failure-detector prior art; no DynamoDB or invention-priority claim."

case_index_row = "| [Amazon Dynamo Ring Membership: Persistent Change History, Local Failure Suspicion, and Placement Authority](cases/68-amazon-dynamo-membership-failure-boundary.md) | **grounded** | persisted membership-change history + persisted node/token placement map + gossip reconciliation + node-local temporary failure suspicion + explicit membership-driven transfer | separate permanent role/topology change from temporary reachability; show control-plane history can determine where payload belongs; distinguish local rerouting/handoff from durable membership reconfiguration | [2007 Dynamo membership/failure grounding](evidence/68-dynamo-2007-membership-failure-grounding.md); later Dynamo/DynamoDB membership, exact record format, consensus semantics, and broader failure-detector genealogy remain separate work |"

matrix_row = "| Amazon Dynamo membership / failure boundary, 2007 | membership-change history + issue times + node/token map + local reachability suspicion + application payload | explicit join/remove persists role changes; gossip reconciles membership/token state; temporary failures are detected locally and retried | request path can route around a locally unreachable node without changing durable ring membership; real membership change triggers key transfer | persisted control-plane history and mapping coexist with intentionally transient node-relative liveness evidence | stale/lost membership history or token maps can corrupt placement intent; mistaken permanent removal can create unnecessary migration; local suspicion can be stale without implying payload loss | preserves placement-role identity across temporary outages while allowing short-lived failure evidence to be re-derived |"

findings = r'''## Case 68 — Dynamo membership / failure-boundary findings

765. **temporary unreachability ≠ permanent membership departure** — Dynamo 2007 explicitly treats many outages as transient and does not make them automatic ring removals;
766. **local failure suspicion ≠ global membership fact** — A may consider B failed because B does not answer A even while B remains reachable from C;
767. **membership change ≠ failure-detector event** — permanent join/remove is an explicit administrative operation, while temporary communication failure is detected opportunistically on request paths;
768. **persisted membership-change history ≠ instantaneous ring-wide view** — nodes retain and gossip histories but the resulting membership view is eventually, not immediately, consistent;
769. **membership history ≠ complete operational history** — Dynamo persists join/remove changes and issue times without thereby retaining every transient outage, packet loss, retry, or request failure;
770. **node/token mapping ≠ payload** — routing/placement metadata is persisted separately from key/value contents yet is required to determine responsibility for keys;
771. **payload survival ≠ sufficient knowledge of intended placement** — surviving object copies do not by themselves encode which ring members should own the key under current membership/token state;
772. **logical membership ≠ bilateral reachability now** — a node can remain a member while one peer temporarily cannot communicate with it;
773. **alternate request routing ≠ durable ownership transfer** — routing around an unreachable peer preserves service without itself rewriting ring membership;
774. **hinted handoff ≠ ring reconfiguration** — Case 23's temporary substitute placement depends on an intended recipient that remains meaningful precisely because transient failure has not become permanent membership change;
775. **durable membership change can create a payload-placement obligation** — explicit add/remove changes key-range responsibility and causes data transfer between old and new responsible nodes;
776. **transfer initiation ≠ confirmed placement handoff** — Dynamo's node-add path includes destination confirmation; the source paper does not license treating an offered transfer as completed current placement;
777. **seed discovery aid ≠ centralized membership registry** — seeds reduce logical partition risk while Dynamo remains described as decentralized and membership histories still reconcile by gossip;
778. **globally consistent failure-state view ≠ required liveness infrastructure** — Dynamo reports abandoning an early global failure-state design in favor of explicit permanent membership plus local temporary suspicion;
779. **control-state representation cost is part of retention infrastructure** — Dynamo's production partitioning discussion treats membership-information size, gossip overhead, bootstrap/recovery behavior, and coordination on membership change as engineering costs;
780. **Dynamo 2007 membership/failure composition ≠ invention of gossip or failure detectors** — 1998 gossip-style failure detection and 2002 SWIM predate Dynamo; the grounded claim is Dynamo's storage-specific composition of persisted role history with local transient reachability evidence.
'''

roadmap_line = "- [x] In Dynamo-style membership/placement control, separate `persistent membership-change history`, `node/token placement state`, `eventually reconciled membership view`, `node-local failure suspicion`, `temporary alternate routing/handoff`, and `membership-driven transfer completion` — grounded in [`cases/68-amazon-dynamo-membership-failure-boundary.md`](cases/68-amazon-dynamo-membership-failure-boundary.md), with [`evidence/68-dynamo-2007-membership-failure-grounding.md`](evidence/68-dynamo-2007-membership-failure-grounding.md); broader failure-detector and DHT-membership history remains routed to `computing-archaeology`."


def insert_after_line_with(text, needle, new_line):
    if new_line in text:
        return text
    lines = text.splitlines()
    matches = [i for i, line in enumerate(lines) if needle in line]
    if not matches:
        raise RuntimeError(f"anchor not found: {needle}")
    lines.insert(matches[-1] + 1, new_line)
    return "\n".join(lines).rstrip() + "\n"


def patch_readme(text):
    text = insert_after_line_with(text, "cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md", readme_case_line)
    text = insert_after_line_with(text, "evidence/67-sk-hynix-2009-2019-read-reclaim-grounding.md", readme_evidence_line)
    return text


def patch_roadmap(text):
    if CASE_PATH in text:
        return text
    return insert_after_line_with(text, "In divergent-version replication", roadmap_line)


def patch_case_index(text):
    if CASE_PATH not in text:
        text = insert_after_line_with(text, "cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md", case_index_row)
    if matrix_row not in text:
        lines = text.splitlines()
        h = next((i for i, line in enumerate(lines) if line.strip() == "## Comparison matrix — provisional"), None)
        if h is None:
            raise RuntimeError("comparison matrix heading not found")
        start = next((i for i in range(h + 1, len(lines)) if lines[i].startswith("| Case |")), None)
        if start is None:
            raise RuntimeError("comparison matrix table not found")
        end = start + 2
        while end < len(lines) and lines[end].startswith("|"):
            end += 1
        lines.insert(end, matrix_row)
        text = "\n".join(lines).rstrip() + "\n"
    if "## Case 68 — Dynamo membership / failure-boundary findings" not in text:
        text = text.rstrip() + "\n\n" + findings.rstrip() + "\n"
    return text


def run(*args):
    return subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)


def main():
    subprocess.run(["git", "pull", "--ff-only", "origin", "main"], cwd=ROOT, check=True)

    (ROOT / CASE_PATH).write_text(case.rstrip() + "\n", encoding="utf-8")
    (ROOT / EVIDENCE_PATH).write_text(evidence.rstrip() + "\n", encoding="utf-8")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
    index = (ROOT / "CASE_INDEX.md").read_text(encoding="utf-8")

    (ROOT / "README.md").write_text(patch_readme(readme), encoding="utf-8")
    (ROOT / "ROADMAP.md").write_text(patch_roadmap(roadmap), encoding="utf-8")
    (ROOT / "CASE_INDEX.md").write_text(patch_case_index(index), encoding="utf-8")

    nums = sorted(int(p.name[:2]) for p in (ROOT / "cases").glob("[0-9][0-9]-*.md"))
    if nums != list(range(69)):
        raise RuntimeError(f"case-number ledger mismatch: {nums[:3]} ... {nums[-5:]}")
    for p in [CASE_PATH, EVIDENCE_PATH]:
        if not (ROOT / p).exists():
            raise RuntimeError(f"missing {p}")
    for nav in ["README.md", "ROADMAP.md", "CASE_INDEX.md"]:
        t = (ROOT / nav).read_text(encoding="utf-8")
        if CASE_PATH not in t:
            raise RuntimeError(f"{nav} missing Case 68 path")
    idx_text = (ROOT / "CASE_INDEX.md").read_text(encoding="utf-8")
    if "765. **temporary unreachability" not in idx_text or "780. **Dynamo 2007" not in idx_text:
        raise RuntimeError("Case 68 findings missing")
    if idx_text.count(CASE_PATH) < 1:
        raise RuntimeError("Case 68 index row missing")
    run("git", "diff", "--check")

    subprocess.run(["git", "config", "user.name", "github-actions[bot]"], cwd=ROOT, check=True)
    subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], cwd=ROOT, check=True)
    subprocess.run(["git", "add", "README.md", "ROADMAP.md", "CASE_INDEX.md", CASE_PATH, EVIDENCE_PATH], cwd=ROOT, check=True)
    subprocess.run(["git", "rm", "-f", ".github/scripts/integrate_case68.py", ".github/workflows/integrate-case68.yml"], cwd=ROOT, check=True)
    subprocess.run(["git", "commit", "-m", "case68: ground Dynamo membership and failure boundary"], cwd=ROOT, check=True)
    subprocess.run(["git", "push", "origin", "HEAD:main"], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
