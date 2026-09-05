# Evidence Record 23 — Amazon Dynamo 2007 Version Retention, Hinted Handoff, and Anti-Entropy

## Promotion target

Ground [`cases/23-amazon-dynamo-divergent-version-anti-entropy.md`](../cases/23-amazon-dynamo-divergent-version-anti-entropy.md) as a bounded distributed-retention case.

The research question is not `how does Dynamo work?` in general. It is:

> **How does the 2007 Dynamo design decide which replicated versions must remain, which may be forgotten, how temporary replica placement is repaired, and how disagreement is detected and converged without equating request availability with replica convergence?**

## Evidence status

**Result:** sufficient for `grounded`.

Reasons:

- the central mechanism is anchored in the directly inspected 2007 SOSP primary paper;
- the key pages for version branching, hinted handoff, anti-entropy, read repair, and background-task scheduling were checked in the page-preserving PDF facsimile;
- the Amazon Science publication record independently anchors title/authors/year/conference identity;
- prior-art controls are supplied by Dynamo's own `well known techniques` statement, Lamport 1978, Parker et al. 1983, Mattern 1989, and earlier ACM records for epidemic replica maintenance and Bayou conflict handling;
- the `computing-archaeology` repository was searched for a dedicated Dynamo / anti-entropy treatment and none was found in the indexed state inspected this round;
- reconstruction vocabulary is explicitly separated from period vocabulary.

No claim in this record depends on an uninspected figure geometry or on retroactively assigning later DynamoDB semantics to the 2007 system.

---

## Source A — DeCandia et al., Dynamo, SOSP 2007

### Bibliographic identity

Giuseppe DeCandia, Deniz Hastorun, Madan Jampani, Gunavardhan Kakulapati, Avinash Lakshman, Alex Pilchin, Swaminathan Sivasubramanian, Peter Vosshall, and Werner Vogels, **“Dynamo: Amazon's Highly Available Key-value Store,”** *Proceedings of the 21st ACM Symposium on Operating Systems Principles (SOSP '07)*, 2007, pp. 205–220.

Amazon Science publication record:

<https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store>

Direct Amazon-hosted PDF linked from that record:

<https://cdn.amazon.science/ac/1d/eb50c4064c538c8ac440ce6a1d91/dynamo-amazons-highly-available-key-value-store.pdf>

### Inspection level

**Primary / direct PDF text + direct page-image inspection.**

The PDF was inspected at the following page-image locations during this research slice:

- PDF page index 5 / printed p. 210 — §4.4 versioning and reconciliation;
- PDF page index 7 / printed p. 212 — §4.6 hinted handoff and §4.7 replica synchronization;
- PDF page index 13 / printed p. 218 — §6.5 background/foreground task scheduling.

The extracted text layer was also checked for §5 read repair on printed p. 213.

The page images support ordinary text/section claims only. This record does not rely on measuring or reconstructing Figure 3's graphical geometry beyond the prose explanation supplied by the authors.

---

## Source A claim ledger

### A1 — Dynamo deliberately permits multiple versions so updates are not lost

**Labels:** `H/P`

**Anchor:** §4.4, printed p. 210.

The paper says failure plus concurrent update can branch object versions and explicitly requires applications to acknowledge the possibility of multiple versions in order not to lose updates. When versions cannot be reconciled by the storage layer, clients perform semantic reconciliation.

**Established:** multiple retained versions can be an intended safety condition, not merely corrupted duplicate state.

**Not established:** that multiple versions are always returned, or that every application resolves them the same way.

### A2 — vector clocks distinguish superseded ancestors from concurrent siblings

**Labels:** `H/P`

**Anchor:** §4.4, printed p. 210.

A vector clock is associated with each version. The paper uses clock comparison to determine whether one version is an ancestor or whether two versions occupy parallel branches. The authors explicitly say an ancestor **can be forgotten**; otherwise the changes are in conflict and require reconciliation.

**Established:** the historical source itself makes forgetting conditional on a causal relation.

**Engineering consequence (`E`):** physical/version existence alone does not authorize discard; retained causality metadata participates in deciding whether a version remains admissible.

### A3 — divergent leaf versions can all be returned

**Labels:** `H/P`

**Anchor:** §4.4, printed pp. 210–211.

When a read encounters multiple branches that cannot be syntactically reconciled, Dynamo returns all leaf objects with their version context. An update carrying a context that subsumes the branches is treated as reconciliation and collapses them into a new version.

**Established:** one logical key can have a set of surviving causally unrelated versions until a later operation collapses the set.

**Project reconstruction:** `set-valued currentness` is useful shorthand, but it is not the paper's historical term.

### A4 — stale ancestors may linger physically after supersession

**Labels:** `H/P`

**Anchor:** Figure 3 explanatory prose, printed p. 211.

The paper notes that an older version D1 may still linger at nodes that have not yet seen descendant D2, while nodes that compare a newer descendant can recognize D1/D2 as overwritten and garbage-collect them.

**Established:** physical replica survival and version admissibility can diverge.

**Boundary:** this does not prove anything about forensic recovery after the local storage engine deletes/reuses bytes.

### A5 — sloppy quorum can write to a temporary substitute and retain an intended-recipient hint

**Labels:** `H/P`

**Anchor:** §4.6, printed p. 212.

With `N=3`, if intended node A is unavailable, a replica can be stored on D. The replica includes a metadata hint naming A as its intended recipient. Hinted replicas are kept in a separate local database that is scanned periodically; after A recovers, D attempts transfer and may delete its temporary copy once transfer succeeds without reducing the replica count.

**Established:** successful highly available service can temporarily separate actual replica location from intended replica location.

**Engineering consequence (`E`):** the hint is constitutive repair/control state because it carries a future placement obligation that payload bytes alone do not encode.

### A6 — hinted handoff is not sufficient for every durability threat

**Labels:** `H/P`

**Anchor:** transition from §4.6 to §4.7, printed p. 212.

The paper states that hinted handoff works best for transient failures and notes cases where hinted replicas can become unavailable before they return to the original replica node.

**Established:** hinted handoff is a bounded transient-failure mechanism rather than a proof of final convergence/durability by itself.

### A7 — anti-entropy detects replica divergence using Merkle trees and then synchronizes

**Labels:** `H/P`

**Anchor:** §4.7, printed p. 212.

Dynamo implements `anti-entropy (replica synchronization)` to keep replicas synchronized. Nodes compare Merkle-tree roots for shared key ranges, traverse branches when roots differ, identify keys that are `out of sync`, and then perform synchronization.

**Established:** replica comparison/localization and synchronization are separable stages.

**Engineering consequence (`E`):** `divergence detection ≠ repair completion`.

### A8 — read repair is an opportunistic path distinct from anti-entropy

**Labels:** `H/P`

**Anchor:** §5, printed p. 213.

After returning a read response, the coordinator can wait briefly for outstanding responses. If stale versions appear, it updates those nodes with the latest version. The paper names this `read repair` and says it relieves the anti-entropy protocol from having to perform that repair.

**Established:** Dynamo has at least two repair schedules/triggers: request-coupled opportunistic repair and background anti-entropy.

### A9 — background retention maintenance competes with foreground service

**Labels:** `H/P`

**Anchor:** §6.5, printed p. 218.

Replica synchronization and data handoff are background tasks. The paper reports that in early production they caused resource contention and affected normal `put/get` performance. Dynamo therefore integrated them with admission control and feedback from monitored foreground performance to limit background intrusiveness.

**Established:** repair/convergence work has a real resource budget and can be throttled relative to foreground SLA work.

**Engineering consequence (`E`):** `foreground availability ≠ immediate convergence` and convergence time can be shaped by resource policy.

### A10 — reconciliation policy varies by deployment/application

**Labels:** `H/P`

**Anchor:** §6 introduction and §6.3, printed pp. 213–217.

The paper states that Dynamo instances differ in version reconciliation logic and quorum characteristics; syntactically irreconcilable versions can be passed to business logic for semantic reconciliation.

**Established:** no universal one-policy interpretation should be projected across all Dynamo applications.

---

## Source B — Amazon Science publication record

### Source

Amazon Science, **“Dynamo: Amazon's highly available key-value store,”** publication page:

<https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store>

### Inspection level

**Institutional publication metadata + abstract-level description.**

### Use

This independently anchors:

- the author list;
- 2007 publication year;
- SOSP conference identity;
- Amazon's description of Dynamo as a highly available key-value storage system;
- explicit emphasis on object versioning and application-assisted conflict resolution.

It is not used for mechanism details that are more precisely stated in the paper.

---

## Source C — Werner Vogels, “Amazon's Dynamo,” 2 October 2007

### Source

<https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html>

### Inspection level

**Contemporary author/company engineering publication.**

### Use

The article is useful for a prior-art/novelty boundary because it presents Dynamo as integrating techniques from operating and distributed-systems research rather than claiming the ingredients as unprecedented inventions.

It also reproduces the paper's production discussion, including divergent versions and background maintenance, but the SOSP paper remains the primary mechanism source for this case.

---

## Source D — Demers et al., epidemic replicated-database maintenance, 1987

### Bibliographic record

Alan Demers et al., **“Epidemic Algorithms for Replicated Database Maintenance,”** *Proceedings of the Sixth Annual ACM Symposium on Principles of Distributed Computing (PODC '87)*, pp. 1–12.

DOI:

<https://doi.org/10.1145/41840.41841>

ACM publication record gives publication date 1 December 1987 and pages 1–12. A later Xerox/PARC technical-report version explicitly notes that an earlier version appeared at PODC 1987.

### Inspection level

**Primary-paper bibliographic/abstract-level evidence for this slice.**

### Use

The abstract describes randomized algorithms for distributing updates and driving replicas toward consistency. This is sufficient here to block a novelty claim that Dynamo introduced the general idea of background/epidemic convergence among replicated databases.

**Not used to claim:** exact algorithmic identity between Xerox epidemic algorithms and Dynamo's Merkle-tree anti-entropy.

---

## Source E — Terry et al., Bayou update conflicts, 1995

### Bibliographic record

Douglas B. Terry, Marvin Theimer, Karin Petersen, Alan J. Demers, Mike Spreitzer, and Carl Hauser, **“Managing Update Conflicts in Bayou, a Weakly Connected Replicated Storage System,”** *SOSP '95*, pp. 172–182.

DOI:

<https://doi.org/10.1145/224057.224070>

### Inspection level

**Primary-paper bibliographic/abstract-level evidence for this slice.**

### Use

The ACM abstract and record establish earlier weakly connected replicated storage with application-specific conflict detection/resolution and replicas moving toward consistency.

This is enough to prevent a broad claim that Dynamo was the first replicated store to preserve/resolve conflicting updates under weak connectivity.

**Not used to claim:** that Bayou and Dynamo have identical version/currentness semantics.

---

## Source F — Lamport, logical clocks and event ordering, 1978

### Bibliographic record

Leslie Lamport, **“Time, Clocks, and the Ordering of Events in a Distributed System,”** *Communications of the ACM* 21(7), July 1978, pp. 558–565.

Microsoft Research author/publication record:

<https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/>

DOI:

<https://doi.org/10.1145/359545.359563>

### Inspection level

**Primary-paper institutional publication record + abstract/author context; Dynamo reference list directly inspected.**

### Use

Lamport's paper establishes the `happened before` partial order and a synchronized logical-clock mechanism that can totally order events consistently with that causal relation. Dynamo's 2007 reference [12] points directly to Lamport 1978.

**Established:** Lamport is direct causal-order/logical-clock prior art for the problem Dynamo cites.

**Not established:** that Lamport 1978 used a per-object vector of site counters, the term `version vector`, or the exact Dynamo clock representation. The historical distinction matters because `logical clock` is not one fixed data structure across all later literature.

---

## Source G — Parker et al., replicated-file version vectors, 1983

### Bibliographic record

D. Stott Parker Jr., Gerald J. Popek, Gerard Rudisin, Allen Stoughton, Bruce J. Walker, Evelyn Walton, Johanna M. Chow, David Edwards, Stephen Kiser, and Charles Kline, **“Detection of Mutual Inconsistency in Distributed Systems,”** *IEEE Transactions on Software Engineering* 9(3), May 1983, pp. 240–247.

DOI:

<https://doi.org/10.1109/TSE.1983.236733>

Direct facsimile mirror inspected for text:

<https://pages.cs.wisc.edu/~remzi/Classes/739/Fall2018/Papers/parker83detection.pdf>

### Inspection level

**Primary-paper direct PDF text, especially printed pp. 242–244 (§III.C–D).**

### Use

The paper explicitly uses the term `version vector`. It proposes keeping a vector with each copy of each replicated file; each component counts updates made at one site. The authors define componentwise compatibility/dominance, increment the originating site's component on update, combine predecessor maxima during reconciliation, and state that the vector is committed with the updated file.

The retention-specific motivation is especially important: the paper rejects retaining an entire potentially unbounded partition/history graph and instead proposes a version-numbering scheme encoding only the necessary characteristics of that history graph.

This grounds:

- `version vector` terminology no later than 1983 in a replicated-file partition context;
- `causal/history summary ≠ full history archive`;
- a small retained relation can authorize conflict detection without retaining every historical event.

### Counterexamples / limits

The authors also state two limits that must survive comparison with Dynamo:

1. identical independent updates in separate partitions can still be reported as a version conflict;
2. the bounded scheme applies to single files and can miss a cross-file transaction serialization conflict.

Therefore `vector compatibility` is not a universal test for semantic equality or arbitrary transactional consistency.

**Not used to claim:** code lineage from this paper to Dynamo, or that Parker's exact file-copy semantics are identical to Dynamo's object clocks.

---

## Source H — Mattern, vector time and explicit relation to Fidge/Parker, 1989

### Bibliographic record

Friedemann Mattern, **“Virtual Time and Global States of Distributed Systems,”** in M. Cosnard et al. (eds.), *Proceedings of the Workshop on Parallel and Distributed Algorithms*, North-Holland / Elsevier, 1989, pp. 215–226.

Official ETH publication/facsimile:

<https://vs.inf.ethz.ch/publ/papers/VirtTimeGlobStates.pdf>

Official ETH bibliographic record:

<https://vs.inf.ethz.ch/publ/bibtex.html?file=papers%2FVirtTimeGlobStates>

### Inspection level

**Primary paper, direct text + page-image inspection.** The vector-time construction was checked around reprint printed p. 126, and the Fidge/Parker comparison around printed p. 129.

### Use

Mattern builds `vector time` from one logical-clock component per process, increments the local component, piggybacks the vector, and merges received knowledge with componentwise maximum. In the applications discussion he says that Fidge independently suggested vectors of logical clocks for distributed debugging. He then explicitly describes Parker et al.'s older replicated-file `version vector`, including per-site update counts and conflict detection for independent modifications under partition.

This is a particularly strong terminology bridge because it is a late-1980s primary author explicitly relating:

```text
vectors of logical clocks / vector time
        to
an earlier replicated-file version-vector scheme
```

**Boundary:** Mattern's wording establishes a contemporaneous relationship and an independent-work statement about Fidge; it does not settle a universal priority dispute for every vector-clock/version-vector concept.

---

## Source A addendum — Dynamo clock truncation is deliberate causal-metadata forgetting

### Anchor

DeCandia et al. §4.4 / author-hosted online text corresponding to printed pp. 210–211.

### Inspection level

**Primary paper / author-hosted text.**

### Use

Dynamo states that vector-clock size can grow when many servers coordinate writes. Its bounded scheme stores a timestamp with each `(node, counter)` pair and removes the oldest pair after a threshold (the paper gives 10 as an example). The authors explicitly say this can make descendant relationships impossible to derive accurately and therefore create reconciliation inefficiency; they also report that this had not surfaced in production and was not thoroughly investigated.

This directly grounds:

- `causal metadata is itself retained state`;
- `bounded metadata growth can require deliberate metadata forgetting`;
- `metadata forgetting ≠ payload-version deletion`;
- `smaller retained causal summary can reduce future reconciliation precision`.

It does **not** establish a quantified probability of false conflict/loss, nor a general claim that truncation is unsafe in every workload.

---

## Prior-art controls

The bounded case rejects the following priority stories:

| Claim | Status | Reason |
| --- | --- | --- |
| `Dynamo invented anti-entropy` | **rejected** | epidemic replica-maintenance literature predates Dynamo by two decades; Dynamo itself describes a synthesis of known techniques |
| `Dynamo invented application-specific conflict reconciliation` | **rejected** | Bayou 1995 is earlier direct literature; Dynamo cites a broader prior-art lineage |
| `Dynamo invented Merkle trees` | **rejected** | the paper cites Ralph Merkle's earlier work; no invention-priority argument is made here |
| `Dynamo invented vector clocks` | **rejected** | Lamport 1978 is causal/logical-clock prior art; Parker et al. 1983 directly use `version vector` for replicated files; Mattern 1989 relates vector time, Fidge's independent vectors of logical clocks, and Parker's earlier version vectors |
| `Lamport 1978 already contains the Dynamo/Parker vector data structure` | **rejected / unsupported** | Lamport's bounded inspected result is happened-before + logical clocks/total ordering; do not infer the later per-site vector representation from Dynamo's citation alone |
| `Parker version vector = Dynamo vector clock in every semantic detail` | **rejected** | useful functional/prior-art relation, but different systems, vocabulary, object models, and stated limits |
| `Dynamo = DynamoDB` | **rejected** | this case is bounded to the internal 2007 Dynamo system/paper |

No positive invention-priority claim is required for the retention comparison.

---

## Historical record vs engineering reconstruction

### Historical record (`H/P`)

Directly grounded terms/mechanisms:

- multiple object versions;
- Dynamo's historical term `vector clock` and per-object `(node, counter)` representation;
- clock-component timestamping/truncation as an explicit bounded-metadata mechanism;
- vector-clock causality;
- ancestor version `can be forgotten`;
- client semantic reconciliation of conflicts;
- sloppy quorum;
- hinted handoff with intended-recipient hint;
- periodic scan of hinted replicas and later transfer;
- anti-entropy / replica synchronization;
- Merkle-tree comparison to find out-of-sync keys;
- read repair;
- background handoff/synchronization under admission control.

### Engineering reconstruction (`E`)

Project-level comparison terms introduced from those facts:

- `set-valued currentness`;
- `retention of disagreement`;
- `temporary placement obligation`;
- `availability ≠ convergence`;
- `divergence detection ≠ repair completion`;
- `causal ancestry can authorize forgetting`;
- `causal summary ≠ full history archive`;
- `clock truncation ≠ object-version deletion`;
- `metadata-size control can trade causal precision for bounded retained state`;
- `vector dominance ≠ semantic equality or arbitrary transaction-consistency proof`;
- `background maintenance has a resource budget`.

These expressions should never be attributed to DeCandia et al. as their historical vocabulary unless the phrase itself occurs in the primary text.

### Functional analogy (`A`)

- RADOS Case 05: both need currentness/version/repair machinery, but bounded RADOS peering establishes a correct PG state before I/O whereas Dynamo can return several causally unrelated versions.
- ZFS Case 18: both can perform proactive/background maintenance, but ZFS verifies integrity against checksums/media defects while Dynamo synchronizes divergent replicas.
- Flash/HDD Cases 04/14: all detach higher-level identity from one embodiment, but Dynamo hinted handoff uniquely encodes a temporary placement plus intended destination in this comparison set.

No genealogy follows from these analogies.

### Philosophical interpretation (`I`)

The only bounded interpretive claim proposed is:

> Technical retention can sometimes require preserving unresolved difference until the mechanism supplies a legitimate rule for collapsing it.

This is a project interpretation of the causal-version mechanism. It is not evidence that Dynamo instantiates human memory, tertiary retention, or `Bestand`.

---

## Failure / counterexample controls

The case remains grounded only if the following limits remain explicit:

1. a stale replica is not automatically a causally concurrent sibling;
2. a causally concurrent sibling is not automatically an immutable historical version;
3. read success does not prove all replicas are synchronized;
4. write success under sloppy quorum does not prove intended steady-state placement is restored;
5. successful hinted handoff does not make anti-entropy unnecessary for all failures;
6. Merkle equality/difference detection is not itself the repaired payload;
7. background synchronization is not free and can be throttled;
8. application reconciliation may change logical semantics in ways the storage layer cannot infer;
9. this paper's semantics must not be projected onto all later Amazon services.

---

## Related-repository duplication check

Before writing and again during the vector/version-vector deepening, the indexed `tmzncty/computing-archaeology` repository was checked for a dedicated treatment of:

- `Dynamo`;
- `Merkle tree anti entropy replication`;
- vector clocks / version vectors.

No dedicated matching treatment was returned in the inspected index/search state.

Therefore this bounded retention argument is not duplicating an existing companion-repository technical history in the inspected state. A future broad genealogy of DHTs, consistent hashing, vector clocks, quorums, epidemic replication, weak consistency, and Dynamo descendants should be routed primarily to `computing-archaeology` and linked from here.

---

## Grounding decision

**Promote Case 23 directly to `grounded`.**

The central claims survive the required checks:

- period vocabulary is direct;
- key mechanisms are on directly inspected primary-paper pages;
- physical/logical/control-state layers are separated;
- version retention and forgetting have explicit period evidence;
- repair triggers are distinguished;
- prior-art boundaries reject broad invention claims;
- cross-case analogies are labeled as analogies;
- the companion repository was checked for duplication.

### Remaining work — not promotion blockers

Future slices may separately investigate:

- the **full** priority genealogy beyond the bounded Lamport 1978 → Parker 1983 → Fidge/Mattern late-1980s anchors established here, including terminology drift and later database/filesystem descendants;
- detailed Bayou→Dynamo comparison;
- later Dynamo descendants and DynamoDB semantics;
- anti-entropy protocol evolution beyond this 2007 Merkle-tree design;
- formal consistency models and application-visible guarantees;
- durability consequences of the paper's optional buffered-write optimization;
- modern repair scheduling under large-scale multi-region operation.

Those are independent regimes, not hidden requirements for this bounded case.