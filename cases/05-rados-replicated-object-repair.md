# RADOS Replicated Objects: Retention by Replica Agreement and Repair

## Scope

- **Object / system:** Ceph's Reliable Autonomic Distributed Object Store (RADOS), as described in the 2006 OSDI Ceph paper.
- **Date range:** bounded primarily to the 2006 prototype and papers immediately surrounding it.
- **Place / institution:** Storage Systems Research Center, University of California, Santa Cruz.
- **Retention question:** how can one logical object remain current and recoverable when its physical replicas move, fail, become stale, or are replaced?

This is **not** a history of Ceph, cloud object storage, distributed consensus, or every replication protocol. It uses one early RADOS design as a bounded case in which retention becomes a property of **replica placement + versioned currentness + temporary primary authority + failure detection + repair**.

The central question is:

> **What exactly persists when no particular storage device has to remain the permanent home of an object?**

The short answer is not simply `multiple copies`.

A replicated object remains usable only because the system also retains enough information and protocol state to decide:

- which devices currently ought to hold replicas;
- which replica state is current;
- who is temporarily authoritative for ordering updates;
- when an update is merely visible versus safely committed;
- when a failed or stale replica must be replaced or repaired.

That makes RADOS a useful transition from **location-independent identity inside one controller** (Case 04, mapped Flash) to **location-independent identity across many independently failing machines**.

---

## Historical vocabulary

The 2006 Ceph paper uses vocabulary that is already recognizably distributed-storage vocabulary rather than terminology reconstructed by this repository:

- `object`;
- `object store` / `object storage cluster`;
- `OSD` (Object Storage Device);
- `placement group` (`PG`);
- `replica`;
- `primary`;
- `cluster map`;
- `epoch`;
- `version number`;
- `replication`;
- `failure detection`;
- `recovery`;
- `commit`.

The paper describes clients and metadata servers as viewing the OSD cluster as a **single logical object store and namespace**, while responsibility for replication, failure detection, migration, and recovery is delegated to OSDs.[^ceph-osdi-5]

That historical language matters. We do not need to invent a modern analogy to say that the system itself presents one logical store while distributing physical embodiments.

---

## Retained state

For the bounded case, the retained state is **the current logical contents of an object together with enough ordering and placement state for the system to identify which physical replicas count as current**.

The object bytes alone are therefore insufficient.

RADOS also depends on retained control state including:

- the current OSD cluster map and its epoch;
- the mapping from object → placement group → ordered OSD set;
- object / placement-group version numbers;
- recent placement-group change logs or content summaries used during recovery.

This makes the case especially important for the repository's developing claim that **metadata can be constitutive of retention**.

In Case 04, Flash mapping metadata decides which physical block currently embodies a logical address. In RADOS, the relevant relation is distributed across placement rules, cluster membership, replica ordering, and version history.

---

## Physical / logical substrate

At the user-visible level, the substrate is a named logical object.

At the bounded 2006 implementation level, physical embodiments are stored by multiple OSDs, each backed by conventional disks and a local object file system (EBOFS in the prototype).[^ceph-osdi-ebofs]

The system does not require a permanent one-to-one relation:

```text
logical object A
    ↓ hash / PG mapping
placement group P
    ↓ CRUSH + current cluster map
ordered OSD set
    ↓
replica on osd7
replica on osd12
replica on osd31
```

If an OSD fails or the cluster changes, the ordered OSD set can change and the object's physical embodiments can be migrated or reconstructed elsewhere.

So this case strengthens a distinction already visible in mapped Flash:

> **identity persistence does not require location persistence.**

But RADOS adds another layer:

> **identity persistence does not require persistence of one privileged physical copy either.**

That statement needs qualification. The protocol **does** select a primary OSD at a given moment to order writes. What is absent is a permanently privileged physical device that must remain the object's eternal home.

---

## Placement: from `where is it?` to a recalculable relation

### Historical record

Ceph first maps objects into placement groups, then uses CRUSH to map each placement group to an ordered list of OSDs on which replicas should reside.[^ceph-osdi-placement]

The paper emphasizes that this placement does not depend on a conventional per-object location directory. To locate an object, a participant needs the placement group plus the OSD cluster map; clients, OSDs, and metadata servers can independently calculate placement.[^ceph-osdi-placement]

The cluster map includes down/inactive devices and an epoch number that changes with membership state.[^ceph-osdi-placement]

The separate 2006 CRUSH paper describes the same family of mechanism as a deterministic pseudo-random mapping from an object or object-group identifier to a list of devices, using a hierarchical cluster description and placement rules that can separate replicas across failure domains.[^crush-2006]

### Engineering reconstruction

This changes the ontology of `where the object is`.

`Location` is no longer only a stored coordinate. It is a **relation recomputed from identity + placement-group assignment + current cluster state + placement policy**.

The same object identifier can therefore remain stable while its correct physical replica set changes.

That is a stronger form of location independence than Case 04's controller-local remapping because the replacement locations are separate machines with independent failure modes.

---

## Replica identity is not enough: currentness requires ordering

A naive description of replication would say:

```text
object A exists because there are N copies of A
```

The 2006 RADOS design is more demanding.

### Historical record

RADOS uses a variant of **primary-copy replication**. Each placement group maps to an ordered list of `n` OSDs for `n`-way replication. Clients send writes to the first non-failed OSD, the primary. The primary assigns a new version number for the object and placement group, forwards the write to the replicas, and coordinates acknowledgement.[^ceph-osdi-replication]

During recovery, OSDs compare placement-group version numbers. If the primary lacks the most recent state, it retrieves recent change logs or a content summary from current or former replicas to determine the correct placement-group contents. Only after the correct state has been determined and shared is I/O permitted; missing or outdated objects are then recovered from peers.[^ceph-osdi-recovery]

### Engineering reconstruction

Multiple physical copies do not by themselves define one retained object.

If replicas disagree, the system needs a rule for **currentness**.

In this bounded design, currentness is reconstructed through:

- temporary primary authority;
- version numbers;
- recent PG change logs / content summaries;
- membership implied by the current cluster map;
- peering before ordinary I/O resumes.

This means the retained object is partly **relational**:

```text
object identity
+ replica contents
+ ordering/version state
+ current membership/placement state
= recoverable current object
```

A stale physical replica can still contain bytes and yet fail to count as the current object state.

This resembles logical invalidation in mapped Flash, but the failure mode is different. The stale RADOS replica may not have been deliberately invalidated; it can become obsolete simply because another replica accepted later ordered updates while it was absent.

---

## Read semantics

In the bounded 2006 replication path, reads are directed to the current primary.[^ceph-osdi-replication]

A successful read is not physically destructive in the sense of magnetic core or the bounded Dennard 1T1C case.

The more relevant read-side retention issue is **authority and freshness**:

- a physically present replica may be stale;
- a newly recovered OSD may not immediately be trusted as current;
- normal I/O waits until peering has established the correct placement-group state.

So the important comparison axis is no longer `destructive vs nondestructive read` alone.

Distributed retention adds:

> **Is this readable physical copy authoritative and current enough to answer?**

---

## Write semantics: visible, replicated, and safely committed are different thresholds

One of the most useful retention distinctions in the 2006 paper is that a write does not have only one moment of `having happened`.

### Historical record

The primary sends the update to replicas. The paper describes an acknowledgement after the update has been applied to the in-memory buffer caches of all OSDs replicating the object, while a later final `commit` notification is sent only after the data has safely reached disk.[^ceph-osdi-safety]

The authors explicitly distinguish two client concerns:

1. making an update visible quickly for synchronization;
2. knowing that it is safely replicated on disk and can survive failures.[^ceph-osdi-safety]

The prototype's clients by default also retain writes locally until the final commit so that previously acknowledged updates can be replayed after a simultaneous power loss affecting all OSDs in the placement group.[^ceph-osdi-safety]

### Engineering reconstruction

This case therefore forces a new question for the repository:

> **At what service-level threshold does an update count as retained?**

A write may be:

```text
ordered by the primary
    ↓
replicated into volatile caches
    ↓
acknowledged / visible
    ↓
committed to persistent local media
```

These are not equivalent states.

The phrase `stored` can hide protocol-defined stages with different failure guarantees.

This distinction should later be compared with:

- filesystem `fsync`;
- database WAL commit;
- battery-backed caches;
- quorum writes;
- object-store durability acknowledgements.

Do not project the 2006 RADOS acknowledgement semantics onto modern Ceph releases. This case is historically bounded to the design described in the paper.

---

## Failure changes membership before it destroys identity

### Historical record

The paper assumes that failures in very large clusters are normal rather than exceptional.[^ceph-osdi-replication]

When an OSD is unreachable it is initially marked `down`, and primary responsibility can temporarily pass to the next OSD in affected placement groups. If it does not quickly recover, it is marked `out`; another OSD joins each affected placement group so the desired replication level can be restored.[^ceph-osdi-failure]

Clients with operations outstanding against the failed OSD resubmit to the new primary.[^ceph-osdi-failure]

### Engineering reconstruction

The logical object's survival is therefore deliberately separated from survival of one member device.

A device can disappear while the object remains:

```text
before failure
PG P → [osd1, osd2, osd3]

osd1 fails
PG P → primary authority moves

osd1 remains out
PG P → another OSD is selected
       missing replica is reconstructed
```

This is **repair-triggered retention maintenance**.

The maintenance trigger is neither:

- continuous circulation (delay line);
- destructive access (classic core);
- elapsed-time deadline (DRAM);
- capacity/reclamation pressure (mapped Flash).

It is a detected loss or membership change that has reduced or threatened redundancy/currentness.

---

## Recovery: persistence as controlled re-creation

The strongest cross-case bridge is recovery.

### Historical record

When cluster membership changes, OSDs recalculate their placement-group responsibility. Replicated placement groups peer: members exchange version information; the primary determines the correct most-recent PG state using logs or a content summary; then individual OSDs retrieve missing or outdated objects from peers.[^ceph-osdi-recovery]

Recovery occurs across many placement groups in parallel, often toward different replacement OSDs.[^ceph-osdi-recovery]

### Engineering reconstruction

The object can remain logically continuous even though:

- one physical copy disappears permanently;
- another copy becomes temporarily authoritative;
- a new physical replica is later created on a different device.

This is a distributed version of a pattern already present in the delay line, destructive-read core, DRAM refresh, and mapped Flash:

> **logical identity can survive physical re-creation.**

RADOS extends that principle to **membership replacement**.

The object persists not because all original copies survive, but because enough current state survives for the protocol to identify and reconstruct the desired replica set.

---

## Replica placement makes infrastructure part of retention

CRUSH placement rules can encode failure-domain separation. The 2006 Ceph paper gives an example in which three replicas are placed on OSDs in different cabinets to reduce exposure to a shared power circuit or edge-switch failure.[^ceph-osdi-placement]

The CRUSH paper makes this motivation explicit: placement policies can use a hierarchy reflecting devices, shelves, cabinets, rows, and other infrastructure so replicas are separated across chosen failure domains.[^crush-2006]

This means the retained object's durability is partly a property of **physical topology**.

Three copies in one failure domain do not provide the same protection as three copies distributed across independent domains.

So distributed retention connects logical redundancy to:

- power topology;
- network topology;
- racks/cabinets/rooms;
- correlated failure assumptions.

A philosophical account that sees only abstract duplication would miss the infrastructure that makes the copies genuinely independent enough to matter.

---

## Maintenance and labor

The system makes persistence appear like a stable property of an object, but that appearance depends on continuous and event-driven work.

### Automatic system work

- monitor and OSD liveness tracking;
- cluster-map dissemination;
- primary selection;
- version assignment;
- replica forwarding;
- peering;
- change-log exchange;
- missing/stale object recovery;
- re-replication after permanent device loss;
- data migration after topology changes.

### Human / institutional work

The bounded paper abstracts most operator labor away, but the mechanism assumes someone maintains:

- functioning replacement hardware;
- power/network failure domains;
- monitor infrastructure;
- cluster configuration and placement policy;
- enough capacity for repair and migration.

Later infrastructure-scale cases should recover this labor explicitly rather than treating `self-healing` as literal absence of maintenance.

---

## Failure / forgetting modes

This case adds forms of technical forgetting that are not reducible to destruction of a storage cell.

### 1. Replica loss

One physical embodiment is destroyed or becomes inaccessible.

Logical state may survive if other current replicas remain.

### 2. Staleness

A replica physically survives but lacks later ordered updates.

This is especially important: **physical survival is not semantic currentness**.

### 3. Insufficient surviving current state

If too many mutually necessary copies/current logs are lost before repair, the system may no longer be able to establish or reconstruct the intended object state.

The 2006 paper does not justify a universal quantitative durability claim; do not manufacture one.

### 4. Placement / membership state failure

The ability to identify which OSDs should participate depends on a consistent cluster map and epoch progression.

### 5. Recovery-state failure

If version/log information needed to determine current PG contents is unavailable or inconsistent beyond protocol recovery, physical bytes may remain while currentness becomes ambiguous.

### 6. Correlated failure

Replica count is not sufficient if replicas share a failure domain. Placement policy therefore becomes part of retention engineering.

---

## Historical record vs engineering reconstruction

### Historical record (`H/P`)

The 2006 OSDI paper directly establishes that the prototype:

- presented the OSD cluster as a single logical object store;
- mapped objects to placement groups and PGs to ordered OSD lists through CRUSH;
- used a cluster map with epochs and device state;
- used a primary-copy replication variant;
- assigned version numbers to object / PG updates;
- acknowledged replicated cache state separately from final disk commit;
- changed primary responsibility after failure;
- re-replicated data when an OSD remained out;
- used version/log exchange and peering to establish correct PG state before I/O;
- recovered missing/stale objects in the background.

### Engineering reconstruction (`E`)

From those documented mechanisms, this repository infers that:

- logical persistence is separable from persistence of any one physical replica;
- `currentness` is a retained relation, not merely a property of bytes;
- placement metadata / cluster state is part of what makes an object recoverable as the same object;
- repair can be constitutive of long-lived durability even though it is triggered only after degradation;
- a distributed store may have multiple service-level thresholds for when a write counts as retained.

These are mechanistic interpretations, not quotations from the authors.

---

## Philosophical / media-theoretical interpretation

This case should **not** yet be used to claim that distributed object stores directly instantiate Stiegler's `tertiary retention`, Heidegger's `Bestand`, or any other philosophical category.

It does sharpen three technical problems that later philosophical synthesis must respect.

### 1. Identity can become relational

The `same object` is not tied to one material token. It is stabilized by name, placement relation, version/order state, and repair protocol.

### 2. Persistence can be maintenance of replaceability

Long-lived retention may depend less on making one carrier immortal than on ensuring that a failed carrier can be replaced before the system loses enough current state.

### 3. Availability is not mere physical survival

A physically intact but stale or unauthoritative replica does not automatically count as the presently usable object.

These mechanisms place a hard limit on metaphors of digital storage as a static warehouse of identical copies.

---

## Functional analogy

A bounded analogy is useful between mapped Flash (Case 04) and RADOS:

```text
mapped Flash
logical address stays stable
while physical block changes
because mapping metadata identifies current embodiment

RADOS
logical object stays stable
while replica membership changes
because placement/version/membership state identifies current embodiments
```

The analogy stops there.

The 1993 Flash system is a single managed storage architecture with controller-local remapping and erase/reclamation constraints. RADOS is a networked distributed system with independently failing OSDs, temporary primary authority, replicated state, failure detection, and peer recovery.

Do not present one as the historical descendant of the other.

---

## Counterexamples and limits

### A primary still exists

It would be too strong to say RADOS has `no privileged copy` without qualification.

The bounded protocol gives one OSD temporary primary authority for ordering writes and serving reads. The safer statement is:

> **No permanently privileged physical replica is required for the logical object's identity to persist.**

### Replication is not consensus in the general sense

This case should not be used as a generic explanation of Paxos, Raft, Byzantine agreement, or quorum databases. It studies the specific replication/recovery scheme described by the 2006 Ceph paper.

### The 2006 system was a prototype

The paper explicitly describes prototype status and notes incompletely implemented elements, including portions of monitor functionality and future work.[^ceph-osdi-future]

Do not silently treat this paper as documentation of modern Ceph behavior.

### `Self-healing` does not mean maintenance-free

Automatic re-replication still consumes devices, bandwidth, spare capacity, software, monitoring, and operator-maintained infrastructure.

### Multiple replicas do not guarantee arbitrary durability

The paper gives a mechanism and performance/recovery argument, not a timeless probabilistic durability guarantee for all deployments. Replica count, correlated failures, placement rules, media failure, detection time, and repair time all matter.

---

## Cross-case result

Case 05 adds three distinctions to the repository:

> **replica multiplicity ≠ retained currentness**

Several physical copies may exist while only some represent the current ordered state.

> **retention can be repair-triggered**

Redundancy can degrade after failure and be restored by copying current state onto replacement members.

> **logical success ≠ durable commit**

A distributed write can pass through protocol-defined stages with different retention guarantees.

Together with Cases 00–04, the maintenance regimes now include:

```text
human / positional maintenance      — abacus
continuous regenerative maintenance — delay line
access-triggered restore            — classic core
deadline-driven refresh             — DRAM
capacity/reclaim-triggered work     — mapped Flash
failure/repair-triggered work       — RADOS
```

The sequence is comparative, not evolutionary.

---

## Related repositories

A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no existing RADOS / Ceph / CRUSH treatment at the time of this case.

If a broader history of object storage, distributed storage, CRUSH, RAID, erasure coding, or storage networking is later added there, `technical-retention` should link to it rather than expanding this case into a general distributed-storage survey.

---

## Evidence status

**Status: first-pass candidate, suitable for promotion after navigation updates.**

Strong points:

- primary peer-reviewed 2006 system paper with mechanism-level detail;
- historical vocabulary is explicit;
- placement, replication, safety acknowledgements, failure detection, and recovery are all described in the same source;
- the case exposes a new maintenance trigger and a new identity/currentness distinction.

Still needed before `grounded`:

1. inspect the OSDI PDF directly and record printed page / figure anchors for central claims;
2. inspect the 2006 CRUSH paper directly rather than relying on its abstract/searchable rendering;
3. inspect the 2007 RADOS paper to distinguish what changed between the OSDI prototype and the later object-store presentation;
4. add one primary implementation artifact or contemporaneous code/documentation for PG peering / recovery semantics;
5. add an independent scholarly or institutional history if a later historical claim depends on chronology beyond the papers themselves.

---

## Sources

[^ceph-osdi-5]: Sage A. Weil, Scott A. Brandt, Ethan L. Miller, Darrell D. E. Long, and Carlos Maltzahn, “Ceph: A Scalable, High-Performance Distributed File System,” *Proceedings of the 7th Symposium on Operating Systems Design and Implementation (OSDI '06)*, pp. 307–320, especially §5 “Distributed Object Storage.” USENIX HTML: https://static.usenix.org/event/osdi06/tech/full_papers/weil/weil_html/index.html

[^ceph-osdi-placement]: Weil et al., “Ceph,” §5.1 “Data Distribution with CRUSH,” especially the object → placement group → ordered OSD mapping, cluster map, epoch, and replica placement-rule discussion. https://static.usenix.org/event/osdi06/tech/full_papers/weil/weil_html/index.html

[^ceph-osdi-replication]: Weil et al., “Ceph,” §5.2 “Replication,” especially the primary-copy replication description and object / PG version assignment. https://static.usenix.org/event/osdi06/tech/full_papers/weil/weil_html/index.html

[^ceph-osdi-safety]: Weil et al., “Ceph,” §5.3 “Data Safety,” especially the distinction between replicated cache acknowledgement and later on-disk commit. https://static.usenix.org/event/osdi06/tech/full_papers/weil/weil_html/index.html

[^ceph-osdi-failure]: Weil et al., “Ceph,” §5.4 “Failure Detection,” especially `down` versus `out`, primary failover, and re-replication. https://static.usenix.org/event/osdi06/tech/full_papers/weil/weil_html/index.html

[^ceph-osdi-recovery]: Weil et al., “Ceph,” §5.5 “Recovery and Cluster Updates,” especially PG version exchange, recent-change logs/content summaries, peering, and retrieval of missing or outdated objects. https://static.usenix.org/event/osdi06/tech/full_papers/weil/weil_html/index.html

[^ceph-osdi-ebofs]: Weil et al., “Ceph,” §5.6 “Object Storage with EBOFS.” https://static.usenix.org/event/osdi06/tech/full_papers/weil/weil_html/index.html

[^ceph-osdi-future]: Weil et al., “Ceph,” §9 “Future Work,” which explicitly records unfinished prototype elements and planned changes. https://static.usenix.org/event/osdi06/tech/full_papers/weil/weil_html/index.html

[^crush-2006]: Sage A. Weil, Scott A. Brandt, Ethan L. Miller, and Carlos Maltzahn, “CRUSH: Controlled, Scalable, Decentralized Placement of Replicated Data,” *SC '06*, November 2006. Project-hosted paper: https://ceph.io/assets/pdfs/weil-crush-sc06.pdf
