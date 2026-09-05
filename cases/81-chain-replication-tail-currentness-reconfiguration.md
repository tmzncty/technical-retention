# Chain Replication: Tail-Qualified Currentness, `Sent` Lists, and Failure Reconfiguration

## Scope

- **Bounded historical/technical regime:** van Renesse and Schneider's OSDI 2004 chain-replication protocol for fail-stop storage servers.
- **Primary question:** what state must remain while an update has entered a replicated chain but has not yet reached the replica whose processing defines the client-visible completed history, and how is that unfinished obligation preserved across reconfiguration?
- **Retention-specific focus:** head/tail role asymmetry, tail-qualified currentness, per-server `Sent_i` lists, acknowledgement-driven retirement of in-process state, internal-server failure repair, and new-tail catch-up before role admission.
- **Excluded from this case:** a general history of replication; later CRAQ or production descendants; Byzantine or partition-tolerant variants; storage-media durability below each server; and invention priority for primary/backup, state-machine replication, acknowledgements, or replicated storage.

The case uses the paper's formal `Hist` / `Pending` model as evidence about the protocol specification while preserving the authors' own warning that an implementation need not retain a complete update sequence.

---

## Historical vocabulary

The primary paper uses terms including:

- `chain`;
- `head`;
- `tail`;
- `Hist`;
- `Pending`;
- `Sent_i`;
- `ack(r)`;
- `Update Propagation Invariant`;
- `Inprocess Requests Invariant`;
- `master`;
- `primary/backup`;
- `state machine approach`;
- `fail-stop`.

The following are **project engineering terms**, not quotations from the authors:

- `tail-qualified currentness`;
- `forwarding obligation`;
- `role admission`;
- `in-process suffix retention`;
- `configuration authority`.

They are used only to expose retention relations across cases.

---

## Historical record

### H/P — head receipt is not the same event as tail-qualified completion

The protocol linearly orders the servers holding an object. Update requests enter at the **head**, are processed there, and then propagate over reliable FIFO links until the **tail** handles them. Query requests go to the tail, and the tail generates replies.

The paper's client-view specification makes the distinction explicit. `Hist_objID` is defined from the tail's replica history, while `Pending_objID` contains requests that have reached some server in the current chain but have not yet been processed by the tail.

Thus, in this bounded protocol, a request can already have changed one or more upstream replicas while remaining outside the state that the specification treats as completed for the client view.

**Primary source:** Robbert van Renesse and Fred B. Schneider, “Chain Replication for Supporting High Throughput and Availability,” OSDI 2004, §§2–3: <https://www.usenix.org/legacy/events/osdi04/tech/full_papers/renesse/renesse_html/>.

### H/P — strong consistency is tied to tail serialization, not replica symmetry

The paper assigns different operational roles to replicas. The head sequences updates; the tail processes queries and is the point through which update completion enters the client-view history. The authors argue strong consistency from the fact that queries and updates are serialized at the tail.

Replica multiplicity therefore does not make every replica equally authoritative for every operation. A middle replica can hold a newer state than one predecessor and still not be the query-serving endpoint or the place that defines client-view completion.

### H/P — `Sent_i` retains an unfinished forwarding obligation

When a server `i` forwards update request `r` to its successor, it also appends `r` to `Sent_i`. The paper defines the list as containing update requests that have been forwarded but might not yet have been processed by the tail.

When the tail completes `r`, it sends `ack(r)` backward. Each predecessor that receives the acknowledgement removes `r` from its own `Sent_i` and forwards the acknowledgement further toward the head.

This is a bounded form of retained control state: an upstream server keeps enough information about still-unconfirmed work to repair a broken chain edge. Once downstream completion is known through the acknowledgement path, that particular forwarding obligation can be forgotten.

### H/P — an internal failure requires suffix reconciliation before normal forwarding resumes

For failure of an internal server, the master reconnects the failed server's predecessor and successor. But the predecessor may not simply begin sending newly arriving updates across the new edge.

The successor first reports the sequence number of the last update it received. The predecessor uses that evidence to compute the missing suffix of its `Sent` list and sends that suffix before normal operation on the new chain position proceeds.

The historical mechanism therefore distinguishes:

1. membership change;
2. evidence about how far the surviving successor progressed;
3. transfer of the missing in-process suffix;
4. resumption of ordinary forwarding.

Reconfiguration alone is not the preservation mechanism.

### H/P — adding a new tail requires state transfer plus concurrent catch-up before tail authority moves

A failed server shortens the chain and therefore reduces the number of further failures that can be tolerated. The paper restores the desired chain length by adding a server, with the practical discussion placing it at the tail.

The current tail forwards its object replica to the new server. Because that transfer can be lengthy, the old tail may continue processing requests, provided concurrent updates are appended to `Sent_T`. Only after the stated invariant relating the old tail state, the new replica, and `Sent_T` is re-established can the new server begin serving as tail; the master and clients are then informed of the new tail.

A physically present or partially initialized replica therefore does not automatically possess tail authority.

### H/P — lost reply and completed update remain distinct

The service model allows clients to retry after timeout. The paper explicitly warns that an update need not be idempotent: a client that retries must take precautions because an update may already have executed even though the client did not receive the reply.

This bounds the phrase `tail-qualified completion`: tail processing defines the service-side completed history in the model, but successful client knowledge of that completion is another relation.

### H/P — the formal history variable is not an implementation requirement to retain complete history

A note in the paper explicitly says that an actual implementation would probably store the **current object value** rather than the complete sequence of updates represented by `Hist_objID`; the update-sequence representation is used because it simplifies the strong-consistency proof.

This is especially important for `technical-retention`:

> the proof can reason with history without requiring the implementation to preserve that complete history as stored operational state.

`Hist` is therefore not evidence that chain replication is intrinsically an append-only history-retention system.

---

## Retained state

At least six state classes should remain distinct.

### 1. Object payload / current replica state

Each server holds a replica of the object or the state produced by the ordered updates it has processed.

### 2. Tail-qualified completed state

The formal client-view `Hist_objID` is tied to the tail. It represents what the specification currently treats as processed rather than merely received somewhere upstream.

### 3. Pending request relation

`Pending_objID` is a specification-level set of requests received by the current chain but not yet processed by the tail. It is not assumed to be one concrete persistent data structure in every implementation.

### 4. Per-server `Sent_i` in-process state

`Sent_i` retains updates forwarded downstream whose tail completion is not yet known at that server. It supports repair of a newly formed chain edge.

### 5. Chain configuration and role state

Which replicas are head, middle, tail, predecessor, and successor determines where requests enter, where queries are admitted, how updates flow, and which replica defines completion.

### 6. Catch-up / recovery relation

During internal failure repair or chain extension, sequence progress and transferred state determine whether a surviving/new replica can safely take its new place in the chain.

---

## Maintenance and transition

### Normal update path

```text
client update
    -> head receives/processes
    -> head forwards + retains request in Sent_head
    -> middle replicas process/forward + retain corresponding Sent state
    -> tail processes update
    -> update enters tail-qualified completed state
    -> tail sends ack(r) backward
    -> each predecessor removes r from Sent_i after ack
```

The payload and the temporary forwarding obligation have different lifetimes.

### Internal-server failure

```text
master removes failed middle server
    -> successor learns new role and reports last received sequence
    -> predecessor learns new successor + progress point
    -> predecessor sends missing suffix from Sent
    -> ordinary forwarding over new edge resumes
```

The reconfiguration must preserve update propagation rather than treating membership change as sufficient by itself.

### Chain extension

```text
shortened chain
    -> add new server at tail
    -> old tail forwards current object state
    -> concurrent updates continue and accumulate in Sent_T
    -> new server catches up until the invariant is restored
    -> tail role + master/client configuration move to new server
```

A state-transfer operation and a role-transfer operation are related but not identical.

---

## Read, write, recovery, and forgetting

### Read

Queries are directed to the tail in the strong-consistency protocol. The tail is not merely one convenient replica; its place in the chain is part of the read-admission/currentness rule.

### Write

Updates enter through the head and propagate serially to the tail. Upstream processing does not by itself produce the client-view completed state.

### Recovery

Recovery from an internal replica failure uses retained `Sent` state plus successor progress evidence to close the missing suffix before the new chain edge handles later work normally.

### Forgetting

An acknowledged request can be removed from `Sent_i` because the protocol has learned that the tail processed it. This is **forgetting a forwarding obligation**, not erasing the object update itself.

Likewise, removing a failed server from the chain changes membership/current role; it is not evidence that bytes formerly stored by that server have been sanitized.

---

## Engineering reconstruction

### E — replica presence does not imply role equivalence

The chain contains several embodiments of one object, but head, middle, and tail are not interchangeable at a given instant. Retention includes a relation assigning different operational authority to surviving copies.

### E — local application can precede global/client-view currentness

An update can be present in upstream replicas while still remaining pending relative to the tail-qualified service state.

### E — temporary control state can be constitutive precisely because it is temporary

`Sent_i` is useful because it survives long enough to bridge uncertainty about downstream processing. Keeping it forever would not improve the protocol's current-state semantics; acknowledgement allows safe retirement.

### E — completion evidence can authorize forgetting of recovery state

Backward acknowledgements do more than signal latency completion. They give each predecessor a reason to stop retaining one request as potentially needed for suffix repair.

### E — reconfiguration safety depends on continuity evidence, not only topology

A new predecessor/successor relation is admitted only after the possible gap between them is reconstructed from progress evidence and retained updates.

### E — state transfer does not itself confer service authority

A new tail needs enough object state, the concurrent delta closure, and a configuration transition before it may serve the tail role.

---

## Functional comparisons — not genealogy

### A — Case 56, Kafka high watermark

Both cases distinguish bytes/updates that exist on replicas from a stronger frontier that ordinary clients may treat as committed/current. Kafka's high watermark is an offset frontier derived from ISR progress; chain replication uses tail processing and role ordering. Similarity of function is not protocol descent.

### A — Case 05, RADOS repair

Both systems retain control relations that qualify which replicas count for current service and repair. RADOS uses placement/version/peering relations rather than one fixed head-to-tail order. This is a mechanism comparison, not genealogy.

### A — Case 23, Dynamo divergent versions

Dynamo deliberately allows concurrent causally unrelated versions to remain admissible until reconciliation. The bounded chain-replication protocol instead serializes strong-consistency queries/updates at the tail under fail-stop assumptions. Replication alone therefore does not determine one universal currentness rule.

### A — Cases 79–80, HDFS re-observation and decommission

HDFS startup SafeMode re-observes replica inventory, and DataNode decommission safely withdraws a still-existing embodiment after preservation work. Chain replication's bounded failure path instead repairs an ordered in-flight suffix and reassigns head/tail topology. All three retain control evidence around changing replica populations, but their objects, triggers, and authority rules differ.

---

## Philosophical interpretation — bounded

### I — retention can include keeping an unfinished obligation until its completion becomes knowable

The technically grounded point is narrower than a general philosophy of memory:

> a distributed system may need to retain not only current payload, but also a temporary relation saying that some already-performed work might still be needed to preserve continuity elsewhere.

When `ack(r)` arrives, forgetting that obligation is successful completion rather than failure of memory. This can discipline later discussions of technical forgetting, but `Sent_i` is not thereby a cultural archive, a Stieglerian tertiary retention, or Heideggerian `Bestand`.

---

## Counterexamples and limits

- The 2004 protocol assumes **fail-stop** server failures; this case does not generalize the result to Byzantine faults.
- The paper's failure treatment relies on a master/configuration service. Its proof idealizes a non-failing master; the prototype discussion notes replication of the master using Paxos. This case does not claim a complete master-durability analysis.
- Chain replication does not gracefully provide the same guarantees through arbitrary network partitioning; partition-tolerant protocols are outside this bounded case.
- `Hist_objID` and `Pending_objID` are specification/proof constructs. The paper explicitly warns that an implementation can store the current object value instead of complete update history.
- `Sent_i` is not a write-ahead log, an application audit trail, or proof of stable-media persistence.
- A tail acknowledgement proves the protocol event described by the paper; it is not generalized into an end-to-end fsync/media-durability guarantee below each storage server.
- Adding a new tail proves a protocol state-transfer/catch-up relation, not physical secure deletion of any old replica.
- The simulation/prototype performance results do not establish production deployment or universal performance superiority.
- No invention-priority claim is made for primary/backup, state-machine replication, acknowledgements, or replicated storage.

---

## Prior-art boundary

The paper itself supplies the key restraint. It explicitly describes chain replication as **a form of primary/backup**, and primary/backup as **an instance of the state-machine approach**. Its references include earlier primary/backup and state-machine work.

The defensible historical statement is therefore narrow:

> **In the 2004 OSDI paper, van Renesse and Schneider specified a fail-stop chain-replication protocol in which the tail defines the client-view completed history, per-server `Sent` lists retain not-yet-tail-confirmed forwarded updates, backward acknowledgements retire that in-process state, and failure/extension protocols preserve the chain invariants before new roles become authoritative.**

This case does **not** claim that the paper invented replicated storage, primary/backup, state-machine replication, acknowledgement-based completion, or online state transfer.

---

## Evidence status

**Status: `grounded`.**

Grounded in the original OSDI 2004 paper's HTML full text plus the USENIX proceedings metadata. The mechanism claims above are drawn from the paper's storage-service specification, normal protocol, failure handling, chain extension, primary/backup comparison, and implementation note.

A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated Chain Replication / van Renesse–Schneider case at the time of this slice. A broader replication history should be developed there rather than duplicated here.

---

## References

- Robbert van Renesse and Fred B. Schneider, “Chain Replication for Supporting High Throughput and Availability,” *6th Symposium on Operating Systems Design & Implementation (OSDI 04)*, USENIX Association, December 2004, pp. 91–104. USENIX record: <https://www.usenix.org/conference/osdi-04/chain-replication-supporting-high-throughput-and-availability>.
- Full HTML of the OSDI 2004 paper: <https://www.usenix.org/legacy/events/osdi04/tech/full_papers/renesse/renesse_html/>.
- Robbert van Renesse, author page, retrospective Chain Replication note: <https://www.cs.cornell.edu/people/rvr/>.
