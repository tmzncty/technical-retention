# Chain Replication: Tail-Qualified Currentness, `Sent` Lists, and Failure Reconfiguration

## Scope

- **Bounded historical/technical regime:** van Renesse and Schneider's OSDI 2004 chain-replication protocol for fail-stop storage servers, with a bounded 2010 Hibari implementation deepening where explicitly marked.
- **Primary question:** what state must remain while an update has entered a replicated chain but has not yet reached the replica whose processing defines the client-visible completed history, and how is that unfinished obligation preserved across reconfiguration?
- **Retention-specific focus:** head/tail role asymmetry, tail-qualified currentness, per-server `Sent_i` lists, acknowledgement-driven retirement of in-process state, internal-server failure repair, new-tail catch-up before role admission, and the distinction between protocol completion and implementation-specific local persistence frontiers.
- **Excluded from this case:** a general history of replication; later CRAQ or unrelated descendants; Byzantine or partition-tolerant variants; exhaustive storage-stack durability below `fsync(2)`; and invention priority for primary/backup, state-machine replication, acknowledgements, write-ahead logging, group commit, or replicated storage.

The case uses the paper's formal `Hist` / `Pending` model as evidence about the protocol specification while preserving the authors' own warning that an implementation need not retain a complete update sequence. The Hibari follow-on is kept separate so that its WAL/`fsync` contract is not projected backward into the abstract 2004 protocol.

---

## Evidence navigation

- [`evidence/81-chain-replication-2004-grounding.md`](../evidence/81-chain-replication-2004-grounding.md) — original protocol, `Hist` / `Pending`, `Sent_i`, failure reconfiguration, chain extension, and prior-art boundary.
- [`evidence/81-hibari-2010-wal-durability-frontier-deepening.md`](../evidence/81-hibari-2010-wal-durability-frontier-deepening.md) — 2010 Hibari WAL/group-commit implementation, per-brick safe-serial durability frontier, downstream propagation gate, write/sync race evidence, and documented weaker durability modes.

---

## Historical vocabulary

The primary 2004 paper uses terms including:

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

The 2010 Hibari implementation report additionally uses concrete implementation vocabulary including:

- write-ahead log / WAL;
- group commit;
- `fsync(2)`;
- write serial number;
- largest serial number safely flushed to disk.

The following are **project engineering terms**, not quotations from the authors:

- `tail-qualified currentness`;
- `forwarding obligation`;
- `role admission`;
- `in-process suffix retention`;
- `configuration authority`;
- `local durability frontier`;
- `composed acknowledgement contract`.

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

### H/P — Hibari 2010 adds a local WAL/flush frontier beneath protocol completion

Scott Lystig Fritchie's 2010 Hibari implementation report gives a concrete stable-storage policy that the abstract 2004 protocol did not specify. Hibari uses a write-ahead log and group commit; the shared WAL process reports to each logical brick the **largest serial number safely flushed to disk**. The brick may then propagate that safe prefix downstream.

The implementation therefore distinguishes:

```text
update known locally
    != WAL I/O requested
    != WAL flush completed
    != safe-serial frontier learned
    != downstream propagation completed
    != tail-qualified completion
```

The same report records early bugs in which WAL writes occurred out of order, `fsync(2)` completion was associated with the wrong serial number, or replay messages went downstream in the wrong order; it says many of these bugs caused data loss. The bookkeeping relation between serial order and local safe-flush progress is therefore historically witnessed as correctness-critical, not merely diagnostic metadata.

### H/P — Hibari's durability is a configurable implementation policy, not a chain-replication theorem

First-party Hibari documentation later exposes weaker modes. `fsync()` may be disabled for asynchronous writes at the cost of possible crash/power-failure data loss, and logging may be disabled for non-durable updates at the cost of data loss if all chain nodes crash.

So retain the boundary:

```text
chain replication
    != mandatory local fsync policy
```

Hibari's durable default composes a local persistence contract with chain ordering; it does not prove that every chain-replicated system has the same lower-layer durability semantics.

---

## Retained state

At least seven state classes should remain distinct.

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

### 7. Implementation-specific local persistence progress

In Hibari's 2010 WAL design, a brick needs to know how far its ordered write stream has crossed the intended local stable-storage boundary. The reported largest safely flushed serial is not payload and is not tail completion; it is a local progress relation that controls downstream eligibility.

---

## Maintenance and transition

### Normal update path — abstract 2004 protocol

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

### Normal update path — Hibari 2010 durable-default deepening

The implementation report adds a lower-layer gate at each brick:

```text
ordered update at brick
    -> local WAL work
    -> group-commit / fsync completion
    -> largest safely flushed serial advances
    -> safe prefix may propagate downstream
    -> eventual tail/client acknowledgement
```

This is a composed implementation path, not a retroactive definition of the abstract protocol.

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

Updates enter through the head and propagate serially to the tail. Upstream processing does not by itself produce the client-view completed state. In the bounded Hibari default, local persistence progress also qualifies which ordered prefix is eligible to proceed downstream.

### Recovery

Recovery from an internal replica failure uses retained `Sent` state plus successor progress evidence to close the missing suffix before the new chain edge handles later work normally. Hibari's implementation report further shows that repair/re-sync must coexist with local write/sync latency and ordered replay; copied bytes alone are not a sufficient description of repair completion.

### Forgetting

An acknowledged request can be removed from `Sent_i` because the protocol has learned that the tail processed it. This is **forgetting a forwarding obligation**, not erasing the object update itself.

Likewise, moving a local safe-serial frontier forward summarizes a prefix that has crossed one implementation-defined persistence boundary; it is not deletion of those WAL records, secure erasure, or proof of client knowledge.

Removing a failed server from the chain changes membership/current role; it is not evidence that bytes formerly stored by that server have been sanitized.

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

### E — local persistence and chain completion are orthogonal frontiers

Hibari's largest safely flushed serial qualifies a prefix at one brick. Tail processing/acknowledgement qualifies service progress through the chain. A single word such as “committed” should not be allowed to hide this distinction.

```text
per-brick safe serial
    != tail-qualified completion
    != client receipt of success
```

### E — stronger acknowledgement meaning arises by composition

The abstract protocol gives tail completion an ordering/currentness role. Hibari's durable default additionally gates progress on local WAL flush. The stronger practical acknowledgement contract comes from composing those layers; it is not intrinsic to chain replication as a protocol family.

### E — group commit makes completion evidence prefix-shaped

One `fsync(2)` can qualify multiple ordered writes. The system therefore retains a frontier such as “largest safe serial” rather than requiring an independent flush event per operation. This compact representation is safe only if serial order, WAL order, and flush-completion attribution remain aligned.

### E — false progress evidence can be worse than missing progress evidence

A missing safe-serial notification can stall useful work. A falsely advanced serial can authorize propagation based on an update that has not crossed the intended local durability boundary. The reported early Hibari wrong-serial/out-of-order bugs and associated data loss provide a concrete historical witness for this control-state hazard.

---

## Functional comparisons — not genealogy

### A — Case 56, Kafka high watermark

Both cases distinguish bytes/updates that exist on replicas from a stronger frontier that ordinary clients may treat as committed/current. Kafka's high watermark is an offset frontier derived from ISR progress; chain replication uses tail processing and role ordering. Hibari additionally exposes a per-brick safe-flush serial. Similar frontier shape does not imply identical authority or protocol descent.

### A — Case 05, RADOS repair

Both systems retain control relations that qualify which replicas count for current service and repair. RADOS uses placement/version/peering relations rather than one fixed head-to-tail order. The EBOFS persistence deepening also shows a distinct application/journal/checkpoint chain; functional similarity to Hibari's WAL frontier is not genealogy.

### A — Case 23, Dynamo divergent versions

Dynamo deliberately allows concurrent causally unrelated versions to remain admissible until reconciliation. The bounded chain-replication protocol instead serializes strong-consistency queries/updates at the tail under fail-stop assumptions. Replication alone therefore does not determine one universal currentness rule.

### A — Cases 79–80, HDFS re-observation and decommission

HDFS startup SafeMode re-observes replica inventory, and DataNode decommission safely withdraws a still-existing embodiment after preservation work. Chain replication's bounded failure path instead repairs an ordered in-flight suffix and reassigns head/tail topology. All three retain control evidence around changing replica populations, but their objects, triggers, and authority rules differ.

### A — Case 152, SQLite WAL

Both SQLite WAL and Hibari separate working updates, retained log evidence, and later completion boundaries. SQLite's transaction/checkpoint authority and Hibari's per-brick flush/chain-propagation authority are different. The comparison is structural only.

---

## Philosophical interpretation — bounded

### I — retention can include keeping an unfinished obligation until its completion becomes knowable

The technically grounded point is narrower than a general philosophy of memory:

> a distributed system may need to retain not only current payload, but also a temporary relation saying that some already-performed work might still be needed to preserve continuity elsewhere.

When `ack(r)` arrives, forgetting that obligation is successful completion rather than failure of memory. This can discipline later discussions of technical forgetting, but `Sent_i` is not thereby a cultural archive, a Stieglerian tertiary retention, or Heideggerian `Bestand`.

### I — “completion” is layer-relative

Hibari sharpens the same discipline: ordering, local log persistence, downstream propagation, tail processing, and client knowledge are separately nameable transitions. Philosophical interpretation should not begin by collapsing them into one undifferentiated event called “the write exists.”

---

## Counterexamples and limits

- The 2004 protocol assumes **fail-stop** server failures; this case does not generalize the result to Byzantine faults.
- The paper's failure treatment relies on a master/configuration service. Its proof idealizes a non-failing master; the prototype discussion notes replication of the master using Paxos. This case does not claim a complete master-durability analysis.
- Chain replication does not gracefully provide the same guarantees through arbitrary network partitioning; partition-tolerant protocols are outside this bounded case.
- `Hist_objID` and `Pending_objID` are specification/proof constructs. The paper explicitly warns that an implementation can store the current object value instead of complete update history.
- `Sent_i` is not a write-ahead log, an application audit trail, or proof of stable-media persistence.
- A tail acknowledgement in the **abstract 2004 protocol** proves the protocol event described by the paper; it is not generalized into an end-to-end fsync/media-durability guarantee below each storage server.
- Hibari's 2010 durable-default policy is implementation-specific. First-party documentation exposes asynchronous/non-durable modes, so local `fsync` cannot be treated as a chain-replication theorem.
- Hibari's use of `fsync(2)` states the software persistence boundary used by the implementation report; it is not independent proof about every disk cache, RAID controller, filesystem, firmware, or power-loss behavior beneath that interface.
- One group-commit `fsync` may qualify multiple writes; one physical/logical flush event is not one-to-one with one chain operation.
- Adding a new tail proves a protocol state-transfer/catch-up relation, not physical secure deletion of any old replica.
- The 2004 simulation/prototype performance results do not establish production deployment or universal performance superiority.
- The 2010 Hibari report documents implementation/production experience but is not evidence that all deployments used identical configuration or hardware.
- No invention-priority claim is made for primary/backup, state-machine replication, acknowledgements, WAL, group commit, `fsync`, or replicated storage.

---

## Prior-art boundary

The 2004 paper itself supplies the key restraint. It explicitly describes chain replication as **a form of primary/backup**, and primary/backup as **an instance of the state-machine approach**. Its references include earlier primary/backup and state-machine work.

The defensible historical statement is therefore narrow:

> **In the 2004 OSDI paper, van Renesse and Schneider specified a fail-stop chain-replication protocol in which the tail defines the client-view completed history, per-server `Sent` lists retain not-yet-tail-confirmed forwarded updates, backward acknowledgements retire that in-process state, and failure/extension protocols preserve the chain invariants before new roles become authoritative. By 2010, Fritchie's Hibari implementation report documented one concrete composition of that protocol with local WAL/group-commit persistence, using ordered serial numbers to represent a per-brick safe-flush frontier before downstream propagation.**

This case does **not** claim that either work invented replicated storage, primary/backup, state-machine replication, acknowledgement-based completion, online state transfer, write-ahead logging, group commit, or stable-storage interfaces.

---

## Evidence status

**Status: `grounded`. No maturity change in this deepening.**

The original mechanism remains grounded in the OSDI 2004 primary paper and USENIX proceedings metadata. The new implementation-specific lower layer is grounded in Scott Lystig Fritchie's 2010 Erlang Workshop implementation report and author slides, plus first-party Hibari operator/contributor documentation.

The follow-on closes the previous evidence-debt item “production implementations such as Hibari and their product-specific stable-storage contracts” **for the bounded 2010 durable-default / safe-serial question only**. It does not close source-revision archaeology, hardware-level persistence validation, Admin-Server durability, or all optional-mode semantics.

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for both `Hibari` and `Chain Replication` found no dedicated packet in this run. Broader replication genealogy, Hibari/Gemini product history, carrier deployments, CRAQ/Hibari influence relations, and storage-stack history below `fsync(2)` belong there rather than being duplicated here.

---

## Remaining evidence debt

Useful future slices, none required for the current `grounded` status:

- exact master/Admin-Server configuration-state durability and network-partition behavior;
- exact 2010 Hibari source revision corresponding to the paper and a source-level brick ↔ shared-WAL message reconstruction;
- crash/fault-injection validation of safe-serial propagation, suffix repair, and tail extension;
- exact semantics of asynchronous/non-durable Hibari modes across releases;
- filesystem/RAID/controller/device persistence beneath the documented `fsync(2)` boundary;
- later CRAQ / chain-replication descendants and read scaling;
- broader production/deployment genealogy, which should be routed through `computing-archaeology`.

---

## References

- Robbert van Renesse and Fred B. Schneider, “Chain Replication for Supporting High Throughput and Availability,” *6th Symposium on Operating Systems Design & Implementation (OSDI 04)*, USENIX Association, December 2004, pp. 91–104. USENIX record: <https://www.usenix.org/conference/osdi-04/chain-replication-supporting-high-throughput-and-availability>.
- Full HTML of the OSDI 2004 paper: <https://www.usenix.org/legacy/events/osdi04/tech/full_papers/renesse/renesse_html/>.
- Scott Lystig Fritchie, “Chain Replication in Theory and in Practice,” *Proceedings of the 9th ACM SIGPLAN Workshop on Erlang*, September 30, 2010, pp. 33–44, DOI `10.1145/1863509.1863515`. Proceedings facsimile: <https://www.erlang-solutions.com/wp-content/uploads/2024/05/Erlang_10-Workshop.pdf>.
- Fritchie, author slides for the Erlang 2010 paper: <https://www.snookles.com/scott/presentations/erlang2010-slf-slides.pdf>.
- Hibari first-party documentation, “Hibari's Main Features in Broad Detail”: <https://hibari.readthedocs.io/en/latest/admin-guide/main-features.html>.
- Hibari documentation repository: <https://github.com/hibari/hibari-doc>.
- Robbert van Renesse, author page, retrospective Chain Replication note: <https://www.cs.cornell.edu/people/rvr/>.