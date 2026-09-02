# Amazon Dynamo: Divergent Version Retention, Hinted Handoff, and Anti-Entropy

## Scope

- **Object / system:** Amazon Dynamo as described in the 2007 SOSP paper by DeCandia et al.
- **Date range:** bounded to the production design and experience reported in 2007.
- **Institution:** Amazon.com.
- **Retention question:** what must remain when a highly available replicated key-value store deliberately permits replicas and versions to diverge, and how does it later decide what may be forgotten, repaired, or converged?

This is **not** a history of DynamoDB, NoSQL, CAP, vector clocks, gossip protocols, or eventual consistency as a whole. It does not claim that Amazon invented anti-entropy, weakly consistent replication, conflict reconciliation, or Merkle trees.

The bounded question is narrower:

> **When one logical key can legitimately have more than one causally unrelated version, what does it mean for the system to retain the key's current state without prematurely discarding an update?**

Dynamo is useful after Case 05 (RADOS) because it breaks a tempting simplification in the repository. In the bounded RADOS case, protocol authority, versions, and peering are used to establish a current placement-group state before ordinary service resumes. In Dynamo, by contrast, the service can deliberately preserve and return several causally unrelated versions of one key until reconciliation collapses them.

That makes `currentness` potentially **set-valued and unresolved**, rather than always one already-selected value.

---

## Historical vocabulary

The 2007 Dynamo paper uses the following period terms directly:

- `object versioning`;
- `vector clock`;
- `context`;
- `causality`;
- `conflicting versions` / `divergent versions`;
- `syntactic reconciliation`;
- `semantic reconciliation`;
- `preference list`;
- `N`, `R`, and `W`;
- `sloppy quorum`;
- `hinted handoff`;
- `hint`;
- `anti-entropy`;
- `replica synchronization`;
- `Merkle tree`;
- `read repair`;
- `foreground` and `background` tasks.

The project terms `set-valued currentness`, `temporary placement obligation`, `convergence debt`, and `retention of disagreement` are **engineering reconstructions**, not Amazon's historical vocabulary.

---

## Retained state

At the service level, Dynamo retains values associated with keys. But the bounded retention target cannot be reduced to one byte string per key.

The design may need to retain:

1. one or more object versions;
2. the vector clock attached to each version;
3. client-visible `context` carrying version information across a read→write sequence;
4. the preference-list / replica-placement relation for the key;
5. temporary `hint` metadata when a replica is stored away from its intended node;
6. enough replica-comparison state to detect and repair divergence through anti-entropy or read repair.

The important complication is item 1: **several versions can simultaneously be intentionally retained because the system cannot yet prove that one supersedes the others.**

The paper is explicit that applications must acknowledge the possibility of multiple versions so that updates are not lost. Vector clocks allow the system to distinguish an ancestor from a causally unrelated branch. An ancestor can be forgotten; parallel branches require reconciliation.

So a key's retained operational state can temporarily be represented as:

```text
logical key K
    ↓
{version A + vector clock A,
 version B + vector clock B,
 ...}
    ↓
causality test
    ├─ ancestor relation → older version may be discarded
    └─ no causal order   → preserve siblings for reconciliation
```

This is not application history preservation in the archival sense. Dynamo does not promise to retain every past version. It retains enough branch state to avoid treating an unresolved concurrent update as obsolete.

---

## Physical / logical substrate

The logical substrate is a key and its object versions.

The physical embodiments are copies stored on Dynamo nodes, each using a local persistence engine. The paper reports that applications could choose among local storage engines and that most production instances used Berkeley DB Transactional Data Store.

Replica placement is computed from consistent hashing and a key's preference list. Under normal conditions, the first `N` appropriate healthy nodes hold the replicas. Under failure, the physical location can temporarily deviate from that intended placement through hinted handoff.

Therefore this case separates at least four relations:

```text
key identity
≠ version identity
≠ current physical replica location
≠ intended replica location
```

That final distinction is what hinted handoff makes unusually explicit.

---

## Versioning: retention can require preserving disagreement

### Historical record

Section 4.4 of the 2007 paper describes version branching under concurrent updates and failures. Dynamo associates a vector clock with every version of every object. The clock is used to decide whether one version is causally descended from another or whether the two lie on parallel branches.

If one clock is dominated by another, the older version is an ancestor and **“can be forgotten.”** If there is no causal ordering, the changes are considered conflicting and require reconciliation.

When a read encounters several branches that cannot be syntactically reconciled, Dynamo returns the causally unrelated leaf versions with version information in the client context. A later update using that context can collapse the branches into a new reconciled version.

The paper's Figure 3 example makes the boundary concrete: versions D1 and D2 can be garbage-collected after a descendant is known, while two causally unrelated descendants such as D3 and D4 must both remain until reconciliation establishes a later successor.

### Engineering reconstruction

This yields a retention rule that differs from ordinary `latest-value` intuition:

> **A physically older-looking or concurrently created value cannot be forgotten merely because another value exists. It becomes safely forgettable only when the retained causal relation establishes supersession or reconciliation creates a successor that subsumes the siblings.**

For this bounded case:

- `replica multiplicity ≠ one current value`;
- `version existence ≠ version authority`;
- `newer arrival ≠ proof of supersession`;
- `causal ancestry can authorize forgetting`;
- `causal incomparability can create a positive retention obligation`.

The repository should therefore not define distributed `currentness` as necessarily singular. In one regime, the admissible current state of a key can be a set of unresolved leaves.

---

## Read semantics

A Dynamo `get()` gathers versions from replicas and waits for the configured `R` responses. If the coordinator obtains multiple causally unrelated versions, it can return all of them.

The read path therefore does more than fetch a physical copy. It can participate in:

- collecting distributed evidence about versions;
- syntactic reconciliation;
- constructing client context that summarizes the surviving vector-clock relation;
- opportunistic repair after the caller has already received a response.

The paper describes the last step as `read repair`: after returning the read result, the coordinator briefly waits for outstanding responses and updates nodes that returned stale versions.

So:

> **read completion ≠ replica convergence.**

A request may finish while repair work continues or remains for later anti-entropy.

This is distinct from Case 02's destructive core read and Case 18's checksum verification. The Dynamo read can alter future replica convergence because it exposes disagreement and triggers opportunistic repair, but ordinary reading is not a physical destructive-read mechanism.

---

## Write semantics: availability can precede intended placement and convergence

### Historical record

For a `put()`, the coordinator creates a new version/vector clock and sends it to the `N` highest-ranked reachable nodes. The operation succeeds after the configured write threshold `W` is met.

Section 4.6 explicitly rejects strict quorum membership during failures in favor of a `sloppy quorum` over the first `N` healthy nodes in the preference walk.

If intended node A is unavailable, a replica that normally belongs on A can be written to node D. D stores a `hint` identifying A as the intended recipient. D keeps hinted replicas in a separate local database that is scanned periodically. When A recovers, D attempts to deliver the replica to A; after successful transfer D may delete its temporary copy without reducing the replica count.

### Engineering reconstruction

A successful write therefore need not imply that the desired steady-state placement already exists.

```text
successful write
    ↓
replica exists on reachable temporary node
    + retained hint naming intended node
    ↓ later recovery
handoff to intended node
    ↓
temporary replica may be deleted
```

The hint is not payload, but it is constitutive retention state: without some retained relation identifying the intended destination, the temporary copy would not by itself express the repair obligation that hinted handoff is designed to discharge.

This gives another separation:

> **write availability ≠ steady-state placement convergence.**

It also gives a new location relation not present in Case 14 HDD reassignment or Case 04 Flash mapping. Those cases can deliberately change the current serving embodiment. Hinted handoff instead permits a **temporary serving/storage embodiment that is explicitly marked as not the intended long-term replica placement**.

---

## Anti-entropy: detecting divergence is separate from repairing it

### Historical record

Section 4.7 says hinted handoff works best for transient failures and does not by itself cover every durability threat. Dynamo therefore implements an `anti-entropy (replica synchronization) protocol`.

It uses Merkle trees to compare key ranges. Two nodes can compare tree roots; equal roots imply no synchronization is required for that range, while unequal roots cause traversal toward differing leaves. The process identifies keys that are `out of sync`, after which the nodes perform the appropriate synchronization action.

The mechanism is economical because the comparison can localize disagreement without sending every key/value or reading the entire data set for every comparison.

### Engineering reconstruction

The paper lets us separate:

1. **divergence exists**;
2. **divergence is detected**;
3. **the affected key/range is localized**;
4. **a synchronization action is performed**;
5. **the intended replica relation has converged enough for the relevant policy**.

Thus:

> **replica-comparison metadata / hashes ≠ repaired payload.**

Merkle trees help establish whether and where copies differ; they are not themselves the repaired object value.

This is useful against a generic use of the word `scrub`. Case 18 ZFS scrub verifies block integrity against checksum relations and may repair media corruption from redundancy. Dynamo anti-entropy compares distributed replica state for synchronization. Both can be proactive/background verification-and-repair regimes, but the failure model and currentness semantics are different.

---

## Read repair and anti-entropy are different repair schedules

Dynamo has at least two replica-repair paths in the bounded paper:

- **read repair** — opportunistic, coupled to an ordinary read that discovers stale replies;
- **anti-entropy** — background replica synchronization intended to cover divergence even when ordinary reads do not happen to expose it.

The distinction matters for technical retention because the same logical redundancy can be maintained by differently triggered work.

Neither should be normalized into DRAM-style refresh:

- there is no fixed physical decay deadline established here;
- the object is not rewritten periodically merely because a time interval elapsed;
- the maintenance target is distributed agreement/currentness, not charge restoration.

---

## Time: foreground service and convergence have different clocks

The 2007 production experience explicitly discusses competition between foreground `put/get` work and background replica synchronization / handoff.

Early production settings experienced resource contention. Dynamo therefore integrated background work with admission control: background tasks reserve runtime slices, while a feedback mechanism monitors foreground performance and changes how much resource is available to background activities.

This makes an important temporal separation visible:

```text
foreground request can complete
        │
        ├───────────────┐
        ▼               ▼
read repair may run   handoff / anti-entropy may remain
opportunistically     background work
        │               │
        └─────── later convergence ───────┘
```

### Engineering reconstruction

`Availability` and `convergence` are therefore not one time threshold.

The system can remain useful while background retention maintenance is incomplete, and it may deliberately slow that maintenance to protect foreground service-level objectives.

This is not evidence that repair delay is costless. It shows instead that retention maintenance consumes resources and is scheduled under another operational priority relation.

---

## Failure / forgetting modes

Keep the following distinct:

- **node/network failure** — may cause temporary placement deviation and hinted handoff;
- **replica staleness** — a copy exists but does not contain the relevant latest/surviving version set;
- **causal conflict** — multiple versions exist and none is established as an ancestor of the others;
- **hint loss before handoff** — a transient-repair path can fail before intended placement is restored;
- **anti-entropy lag** — divergent replicas remain out of sync until comparison/synchronization proceeds;
- **premature version collapse** — would constitute logical loss of an update that causal metadata did not authorize discarding;
- **background-resource starvation/contention** — can delay handoff or synchronization without being identical to physical media loss;
- **application reconciliation error** — semantic reconciliation can choose a resulting value that the storage layer cannot infer from causality alone.

The last item is an interface boundary, not a claim that Dynamo preserves user intent perfectly.

---

## Maintenance and labor

Dynamo's apparent always-on key/value service depends on work below the simple API:

- failure detection and membership state;
- replica placement computation;
- version/vector-clock maintenance;
- hint creation, scanning, retry, and handoff;
- read repair;
- Merkle-tree maintenance/comparison and synchronization;
- admission control for background tasks;
- application-specific reconciliation logic in cases where syntactic causality is insufficient;
- operators choosing production parameters such as `N`, `R`, and `W` for service goals.

This is automated infrastructure, but `automation ≠ absence of maintenance` and `background ≠ costless` remain supported cross-case controls.

---

## Historical record

The central primary source is:

- Giuseppe DeCandia, Deniz Hastorun, Madan Jampani, Gunavardhan Kakulapati, Avinash Lakshman, Alex Pilchin, Swaminathan Sivasubramanian, Peter Vosshall, and Werner Vogels, **“Dynamo: Amazon's Highly Available Key-value Store,”** *Proceedings of the 21st ACM Symposium on Operating Systems Principles (SOSP '07)*, 2007, pp. 205–220. Amazon Science publication page and author-hosted facsimile: <https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store>.

Directly inspected anchors used here include:

- §4.4 / printed p. 210: divergent versions, vector clocks, ancestor forgetting, semantic reconciliation;
- §4.5–4.6 / printed pp. 211–212: `N/R/W`, sloppy quorum, hinted handoff and intended-recipient hint;
- §4.7 / printed p. 212: anti-entropy, Merkle-tree comparison, out-of-sync keys and synchronization;
- §5 / printed p. 213: read-repair state machine;
- §6.5 / printed p. 218: background replica synchronization/handoff, resource contention, admission control.

Amazon's contemporary engineering account by Werner Vogels also states that Dynamo combines techniques from prior operating/distributed-systems research rather than presenting every component as an Amazon invention: <https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html>.

---

## Prior-art boundary

Dynamo's own paper says it synthesizes `well known techniques`; the novelty of this case is therefore **not** an invention-priority claim for its ingredients.

Two earlier lines are especially relevant:

- Alan Demers et al., **“Epidemic Algorithms for Replicated Database Maintenance,”** PODC 1987, pp. 1–12, DOI <https://doi.org/10.1145/41840.41841>. This is direct prior art for randomized propagation / replica convergence well before Dynamo's anti-entropy deployment.
- Douglas B. Terry et al., **“Managing Update Conflicts in Bayou, a Weakly Connected Replicated Storage System,”** SOSP 1995, pp. 172–182, DOI <https://doi.org/10.1145/224057.224070>. This is earlier primary literature for weakly connected replicated storage with application-specific conflict handling.

The present case therefore makes **no** claim that Dynamo invented eventual consistency, divergent-version reconciliation, anti-entropy, vector clocks, or Merkle trees.

A full genealogy of vector clocks, epidemic replication, consistent hashing, quorums, Merkle trees, and weak consistency belongs in distributed-systems history, not in this bounded retention slice.

---

## Engineering reconstruction

The case adds the following retention relations:

### 1. `replicated currentness` can be plural

A logical key can have several causally unrelated leaf versions that are all still admissible inputs to later reconciliation. `Current state` is therefore not universally equivalent to one already-selected value.

### 2. Causality can authorize forgetting

A version can be safely discarded when its vector clock establishes it as an ancestor of a surviving descendant. In contrast, causally unrelated siblings have a positive reason to remain until reconciliation.

### 3. Availability can precede convergence

A successful sloppy-quorum operation can complete while replicas are temporarily stored away from intended nodes or while stale replicas remain to be repaired.

### 4. Placement metadata can encode a future obligation

A hinted replica's payload is not enough to describe its role. The hint that identifies the intended recipient is retained control state directing later handoff.

### 5. Detection and correction are different retention work

Merkle-tree comparison can prove/localize replica disagreement without itself repairing the values. Read repair and anti-entropy then provide separate correction schedules.

### 6. Repair has a resource budget

The paper's production admission controller establishes that replica synchronization and handoff compete with foreground service for real database/runtime resources. Maintenance latency can therefore be a policy outcome rather than only a failure symptom.

---

## Functional analogies — explicitly bounded

### Dynamo ↔ RADOS (Case 05)

Both preserve logical objects across changing replica conditions and require version/currentness metadata.

**But:** the bounded RADOS case peering establishes the correct PG state before normal I/O, whereas Dynamo can deliberately return multiple causally unrelated versions for later semantic reconciliation. Do not normalize both into a single `replication = copies + repair` model.

### Dynamo ↔ ZFS scrub (Case 18)

Both include background work that can detect a problem before ordinary service alone would necessarily repair every embodiment.

**But:** ZFS scrub is checksum-qualified integrity verification against latent media/block corruption; Dynamo anti-entropy compares replicas for synchronization. Their failure models, identity relations, and repair decisions differ.

### Dynamo ↔ mapped Flash / HDD remapping (Cases 04 and 14)

All can preserve a higher-level designation while physical embodiments or serving locations change.

**But:** hinted handoff explicitly retains an intended destination for later return; FTL relocation and grown-defect reassignment are different controller-local location mechanisms with different triggers and authority.

---

## Philosophical / media-theoretical interpretation

The case sharpens one project-level problem without requiring a new philosophical vocabulary:

> **Retention may require preserving unresolved difference, not merely preserving an already-unified identity.**

If the system discarded one concurrent branch simply because another branch was newer in wall-clock arrival or happened to be read first, it could erase an update that the causal relation does not establish as obsolete. In this bounded mechanism, preservation sometimes means keeping a conflict open until another actor or rule can decide how it closes.

That is useful for thinking about technical identity and forgetting: the thing that persists is not always one material token or one currently authoritative scalar value, but a relation among versions together with rules governing which differences may be collapsed.

This does **not** make Dynamo a model of human memory, Stieglerian tertiary retention, or Heideggerian orderability. Those would require separate arguments about the retained object, exteriorization, interpretation, and socio-technical use.

---

## Counterexamples and limits

Do **not** infer any of the following from this case:

- `Dynamo invented anti-entropy / vector clocks / eventual consistency / Merkle trees`;
- every Dynamo deployment always returned multiple versions;
- every application used the same reconciliation policy;
- every successful write was immediately stored on the intended steady-state replica set;
- every divergent copy was a causally valid sibling rather than simply stale;
- anti-entropy and read repair are the same trigger/path;
- eventual convergence means every historical version remains archived;
- a hint is a durable application record rather than transient repair metadata;
- Amazon Dynamo 2007 and present-day DynamoDB have identical semantics;
- distributed consistency can be reduced to a philosophical metaphor about memory.

The paper itself reports deployment variation in reconciliation logic and quorum characteristics. This case therefore stays at the 2007 design/production boundary.

---

## Related repositories

`tmzncty/computing-archaeology` was searched for dedicated `Dynamo`, `Merkle tree anti-entropy replication`, and related entries before writing this slice; no dedicated treatment was found in the indexed repository state inspected for this round.

If a broader history of vector clocks, epidemic replication, DHTs, consistent hashing, quorum systems, or Dynamo descendants is later written, that technical genealogy belongs primarily in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). This case should remain the retention-specific comparison.

The anti-anachronism rule remains inherited from [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history): `set-valued currentness`, `retention of disagreement`, and `temporary placement obligation` are present-day analytical terms unless directly attributed otherwise.

---

## Sources

### Primary / contemporary

- Giuseppe DeCandia et al., **“Dynamo: Amazon's Highly Available Key-value Store,”** SOSP '07, 2007, pp. 205–220. Amazon Science: <https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store>.
- Werner Vogels, **“Amazon's Dynamo,”** *All Things Distributed*, 2 October 2007: <https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html>.
- Alan Demers et al., **“Epidemic Algorithms for Replicated Database Maintenance,”** PODC '87, 1987, pp. 1–12, DOI <https://doi.org/10.1145/41840.41841>.
- Douglas B. Terry et al., **“Managing Update Conflicts in Bayou, a Weakly Connected Replicated Storage System,”** SOSP '95, 1995, pp. 172–182, DOI <https://doi.org/10.1145/224057.224070>.

### Evidence record

See [`evidence/23-amazon-dynamo-2007-version-handoff-antientropy-grounding.md`](../evidence/23-amazon-dynamo-2007-version-handoff-antientropy-grounding.md).