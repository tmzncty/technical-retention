# Evidence Record 68 — Dynamo 2007 Membership History, Failure Suspicion, and Placement Authority

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
