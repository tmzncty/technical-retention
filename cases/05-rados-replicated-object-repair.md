# RADOS Replicated Objects: Retention by Replica Agreement and Repair

## Scope

- **Object / system:** Ceph's Reliable Autonomic Distributed Object Store (RADOS), bounded primarily to the 2006–2007 research system and its immediately surrounding implementation record.
- **Place / institution:** Storage Systems Research Center, University of California, Santa Cruz.
- **Retention question:** how can one logical object remain current and recoverable when its physical replicas move, fail, become stale, or are replaced?

This is **not** a general history of Ceph, cloud object storage, consensus, or every replication protocol. It uses early RADOS as a bounded case in which retention becomes a property of **replica placement + versioned currentness + temporary primary authority + failure detection + peering + repair**.

The central question is:

> **What exactly persists when no particular storage device has to remain the permanent home of an object?**

The short answer is not simply `multiple copies`.

A replicated object remains usable only because the system also retains enough information and protocol state to decide:

- which devices currently ought to hold replicas;
- which replica state is current;
- who is temporarily authoritative for ordering updates;
- when an update is merely visible versus safely committed;
- which prior participants must be consulted after membership changes;
- which object versions should exist even when some copies are currently missing;
- when a failed or stale replica must be replaced or repaired.

That makes RADOS a useful transition from **location-independent identity inside one controller** (Case 04, mapped Flash) to **location-independent identity across independently failing machines**.

### Evidence deepening

- [`evidence/05-rados-2005-2007-peering-pg-metadata-retention-deepening.md`](../evidence/05-rados-2005-2007-peering-pg-metadata-retention-deepening.md) — contemporaneous August 2005 source plus the mature 2007 RADOS presentation, separating payload completeness, peering/currentness knowledge, PG logs, missing-state metadata, and repair completion.
- [`evidence/05-crush-2006-map-epoch-placement-currentness-deepening.md`](../evidence/05-crush-2006-map-epoch-placement-currentness-deepening.md) — direct 2006 CRUSH/OSDI inspection separating current map/epoch placement relation from replica-content currentness, and fixing `physical replica survival != current placement membership` and `deterministic recomputation != no retained resolver state`.

---

## Historical vocabulary

The 2006–2007 RADOS record uses vocabulary that is already recognizably distributed-storage vocabulary rather than terminology reconstructed by this repository:

- `object`;
- `object store` / `object storage cluster`;
- `OSD` (Object Storage Device);
- `placement group` (`PG`);
- `replica`;
- `primary`;
- `cluster map`;
- `epoch`;
- `version` / version number;
- `PG log`;
- `last_update`;
- `last_complete`;
- `missing`;
- `prior set`;
- `peering`;
- `replication`;
- `failure detection`;
- `recovery`;
- `commit`.

The 2006 OSDI paper describes clients and metadata servers as viewing the OSD cluster as a **single logical object store and namespace**, while responsibility for replication, failure detection, migration, and recovery is delegated to OSDs.[^ceph-osdi-5]

The 2007 RADOS paper and Sage Weil's dissertation sharpen the peering/recovery vocabulary by making PG history, completeness, and missing-state relations explicit.[^rados-2007][^weil-thesis]

That historical language matters. We do not need to invent a modern analogy to say that the system itself presents one logical store while distributing physical embodiments.

Project vocabulary used below includes:

- **currentness reconstruction** — establishing which surviving history/replicas define the authoritative PG state after membership or failure changes;
- **admission state** — enough reconciled history to permit a PG to resume ordinary service;
- **repair debt** — expected replica/object state that is known to be missing or stale and still requires material reconstruction.

Those three are engineering reconstructions, not period RADOS terms.

---

## Retained state

For the bounded case, the retained state is **the current logical contents of an object together with enough ordering, placement, membership, and recovery history for the system to identify which physical replicas count as current and which required state is missing**.

The object bytes alone are therefore insufficient.

RADOS depends on retained control/history state including:

- the current OSD cluster map and its epoch;
- the mapping from object → placement group → ordered OSD set;
- object / PG version numbers;
- recent PG logs;
- `last_update` / `last_complete` boundaries in the 2007 design;
- missing-object/version state used during recovery;
- enough prior-participant history to avoid silently ignoring an OSD that may contain a newer update.

This makes the case especially important for the repository's claim that **metadata can be constitutive of retention**.

The deepening now makes the decomposition more explicit:

```text
payload replica bytes
    != placement / membership state
    != version / ordering state
    != expected-content history
    != missing / repair-debt state
    != live peer-session state
    != completed repair
```

In Case 04, Flash mapping metadata decides which physical block currently embodies a logical address. In RADOS, the relevant relation is distributed across placement rules, cluster membership, replica ordering, PG history, and recovery state.

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

> **identity persistence does not require persistence of one permanently privileged physical copy either.**

That statement needs qualification. The protocol **does** select a primary OSD at a given moment to order writes. What is absent is a permanently privileged physical device that must remain the object's eternal home.

---

## Placement: from `where is it?` to a recalculable relation

### Historical record

Ceph first maps objects into placement groups, then uses CRUSH to map each placement group to an ordered list of OSDs on which replicas should reside.[^ceph-osdi-placement]

The paper emphasizes that this placement does not depend on a conventional per-object location directory. To locate an object, a participant needs the placement group plus the OSD cluster map; clients, OSDs, and metadata servers can independently calculate placement.[^ceph-osdi-placement]

The cluster map includes device state and an epoch number that changes with membership state.[^ceph-osdi-placement]

The separate 2006 CRUSH paper describes the same family of mechanism as a deterministic pseudo-random mapping from an object or object-group identifier to a list of devices, using a hierarchical cluster description and placement rules that can separate replicas across failure domains.[^crush-2006]

The direct-paper deepening adds two placement-specific boundaries. Failed or overloaded devices can remain represented in the hierarchy while being rejected as current selection targets, and the rank of a returned target can itself carry primary-copy or coded-fragment semantics. A changed cluster map therefore changes a policy-bearing placement relation; it does not merely update a passive address book. See [`../evidence/05-crush-2006-map-epoch-placement-currentness-deepening.md`](../evidence/05-crush-2006-map-epoch-placement-currentness-deepening.md).

### Engineering reconstruction

`Location` is no longer only a stored coordinate. It is a **relation recomputed from identity + placement-group assignment + current cluster state + placement policy**.

The same object identifier can therefore remain stable while its correct physical replica set changes.

That is a stronger form of location independence than Case 04's controller-local remapping because the replacement locations are separate machines with independent failure modes.

The direct CRUSH inspection sharpens the boundary further:

```text
physical replica survives
    != replica remains a current placement target

current placement target
    != payload is already current/complete there

CRUSH is deterministic
    != placement is timeless
```

Placement currentness is relative to a sufficiently current map/epoch and rule; replica-content currentness remains a separate peering/version-history question.

---

## Replica multiplicity is not currentness

A naive description of replication would say:

```text
object A exists because there are N copies of A
```

The bounded RADOS design is more demanding.

### Historical record

RADOS uses a variant of **primary-copy replication**. Each placement group maps to an ordered list of OSDs. Clients send writes to the primary; the primary assigns a version, forwards the update to replicas, and coordinates acknowledgement.[^ceph-osdi-replication]

During recovery, OSDs compare PG/version history. If the new primary lacks enough history, it obtains logs or content information from current or former participants before establishing the correct PG state.[^ceph-osdi-recovery]

The 2007 description sharpens this further. It separates the most recently applied update (`last_update`) from the point through which required local object state is complete (`last_complete`), and uses a PG log plus missing-state information to describe updates/deletions and absent objects between those boundaries.[^weil-thesis]

### Engineering reconstruction

Multiple physical copies do not by themselves define one retained object.

If replicas disagree, the system needs a rule for **currentness**.

In this bounded design, currentness is reconstructed through:

- temporary primary authority;
- map epochs and membership history;
- object / PG versions;
- recent PG logs / content summaries;
- missing-state information;
- consultation of prior participants;
- peering before normal service resumes.

This means the retained object is partly relational:

```text
object identity
+ surviving replica contents
+ ordering/version history
+ placement/membership state
+ knowledge of missing/stale state
= recoverable current object
```

A stale physical replica can still contain bytes and yet fail to count as the current object state.

---

## Peering is not just copying bytes

### 2005 implementation witness

Ceph's historical source commit `88086b83b7dcb0eb5c092e30fde8570475173f5e` (2005-08-06) is explicitly labelled by its own commit message as peering work that was `still not complete`.[^ceph-2005-peering]

That early code predates the mature 2007 CRUSH/PG design and still uses `RG` / RUSH-era structures. It must not be treated as an implementation snapshot of the final 2007 algorithm.

It nevertheless provides a valuable contemporaneous genealogy witness.

`ceph/osd/OSD.h` distinguishes:

- `RG_STATE_COMPLETE` — full local RG contents;
- `RG_STATE_PEERED` — enough contact/content-list exchange with prior/current participants to know the RG state;
- `RG_STATE_CLEAN` — fully replicated state on the primary.[^ceph-2005-osdh]

The same source labels active `peers` as **soft state**, while `RG::store()` / `RG::fetch()` persist and reload `role`, `primary`, and `state` through collection attributes.[^ceph-2005-osdh]

So even this unfinished prototype already distinguishes:

```text
local data completeness
    != peering/currentness knowledge
    != full replication

persistent group state
    != live peer-session state
```

### Map changes invalidate knowledge before they erase payload

In the same revision, a newer map triggers an RG scan. Role/primary changes clear `RG_STATE_PEERED`, persist the changed group state, and initiate new peering work. Local object bytes need not disappear for prior peering knowledge to become insufficient.[^ceph-2005-osdcc]

Thus:

```text
membership / authority change
    -> old peering knowledge no longer sufficient
    -> repeering required

local bytes may physically survive throughout
```

### Peering exchanges object/version state

The 2005 `handle_rg_peer()` path returns RG state, deleted-object state, an object inventory, and each object's `version`; the primary installs those responses as per-peer state.[^ceph-2005-osdcc]

This is not yet the full later PG-log algorithm, but it proves that peering was already about **replica-state comparison**, not only liveness.

---

## PG metadata can outlive missing payload replicas

The 2007 RADOS presentation makes the retention consequence explicit.

OSDs maintain short-term PG logs recording recent update/delete operations and versions. Sage Weil's dissertation states that those logs are stored on disk and may also be present in RAM/NVRAM.[^weil-thesis]

More importantly, the recovery design deliberately guards the PG log's record of **what the PG should contain even while some object replicas are missing locally**.[^rados-2007][^weil-thesis]

This gives a new bounded distinction:

```text
payload copy present here
    != system remembers that this object/version ought to exist here
```

That second relation can survive while material repair is still outstanding.

### Engineering reconstruction: retained obligation

The PG log / missing-state design lets the system retain not only positive state (`these copies exist`) but also a negative obligation (`this object/version is expected but absent or incomplete here`).

So Case 05 now distinguishes:

```text
payload retention
    != expected-state retention
    != repair-debt retention
```

A missing replica does not become equivalent to a legitimate deletion merely because its bytes are absent from one OSD; the retained PG history can still say that the state ought to exist.

This formulation is a project reconstruction from the mechanism, not period terminology.

---

## Peering reconstructs authoritative history before repair completes

### Historical record

The 2007 design considers map epochs and prior participants when a PG's active set changes. A new primary solicits state from OSDs that may have participated since the last successful peering interval, obtains needed log fragments, and can fall back to a fuller PG-content listing when logs are insufficient.[^rados-2007][^weil-thesis]

The reconciled history tells the active replicas what the PG **should** contain even if some objects are not yet local everywhere. Payload recovery can then continue in the background under the described conditions.[^rados-2007]

### Engineering reconstruction

This sequence is better represented as:

```text
surviving physical replicas / remnants
    ↓
collect relevant prior-participant history
    ↓
reconstruct authoritative PG state
    ↓
identify missing / stale object versions
    ↓
admit the PG for service when protocol conditions are met
    ↓
continue material repair / redundancy restoration
```

Therefore:

> **peering is a currentness-reconstruction and admission procedure, not merely a payload-copy operation.**

And:

```text
serviceable / active
    != every replica locally complete
    != desired redundancy fully restored
```

This is bounded to the historical design described by the sources; do not project it unchanged onto every modern Ceph release.

---

## Read semantics

In the bounded 2006 replication path, reads are directed to the current primary.[^ceph-osdi-replication]

A successful read is not physically destructive in the sense of magnetic core or the bounded Dennard 1T1C case.

The more relevant read-side retention issue is **authority and freshness**:

- a physically present replica may be stale;
- a newly recovered OSD may not immediately be trusted as current;
- a membership change can require peering even though local payload survives;
- normal service depends on protocol-established currentness, not mere readability of one disk copy.

Distributed retention therefore adds:

> **Is this readable physical copy authoritative and current enough to answer?**

---

## Write semantics: visible, replicated, and safely committed are different thresholds

One of the most useful retention distinctions in the 2006 paper is that a write does not have only one moment of `having happened`.

### Historical record

The primary sends the update to replicas. The paper describes an acknowledgement after the update has been applied to the in-memory buffer caches of all OSDs replicating the object, while a later final `commit` notification is sent only after the data has safely reached disk.[^ceph-osdi-safety]

The authors explicitly distinguish two client concerns:

1. making an update visible quickly for synchronization;
2. knowing that it is safely replicated on disk and can survive failures.[^ceph-osdi-safety]

The prototype's clients by default retain writes locally until final commit so previously acknowledged updates can be replayed after a simultaneous power loss affecting all OSDs in the placement group.[^ceph-osdi-safety]

### Engineering reconstruction

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

These are not equivalent retention states.

The phrase `stored` can hide protocol-defined stages with different failure guarantees.

Do not project the 2006 acknowledgement semantics onto modern Ceph releases.

---

## Failure changes membership before it destroys identity

### Historical record

The OSDI paper assumes failures in very large clusters are normal rather than exceptional.[^ceph-osdi-replication]

When an OSD is unreachable it is initially marked `down`, and primary responsibility can temporarily pass to another OSD. If it remains unavailable it can be marked `out`; another OSD joins affected PGs so desired replication can be restored.[^ceph-osdi-failure]

Clients with operations outstanding against the failed OSD resubmit to the new primary.[^ceph-osdi-failure]

### Engineering reconstruction

The logical object's survival is deliberately separated from survival of one member device:

```text
before failure
PG P → [osd1, osd2, osd3]

osd1 fails
PG P → authority changes / repeering

osd1 remains out
PG P → replacement participation
       missing replica reconstructed
```

This is **repair-triggered retention maintenance**.

The maintenance trigger is neither continuous circulation, destructive access, elapsed-time refresh, nor capacity reclamation. It is detected degradation/change in membership, redundancy, or currentness.

---

## Recovery: persistence as controlled re-creation

When cluster membership changes, OSDs recalculate PG responsibility. Peering reconstructs the most recent admissible PG history; missing or outdated objects are then recovered from peers.[^ceph-osdi-recovery][^rados-2007]

The object can remain logically continuous even though:

- one physical copy disappears permanently;
- another copy becomes temporarily authoritative;
- a new physical replica is later created on a different device;
- the system can remember that an object/version is missing before that missing copy has been recreated.

This extends a pattern already present in earlier cases:

> **logical identity can survive physical re-creation.**

RADOS adds both **membership replacement** and **retained negative/repair state**.

The object persists not because all original copies survive, but because enough current payload **and enough currentness/history state** survive for the protocol to identify and reconstruct the intended replica state.

---

## Replica placement makes infrastructure part of retention

CRUSH placement rules can encode failure-domain separation. The 2006 Ceph paper gives an example in which three replicas are placed on OSDs in different cabinets to reduce exposure to a shared power circuit or edge-switch failure.[^ceph-osdi-placement]

The CRUSH paper similarly motivates hierarchy-aware placement across devices, shelves, cabinets, rows, and other failure domains.[^crush-2006]

This means the retained object's durability is partly a property of **physical topology**.

Three copies in one failure domain do not provide the same protection as three copies distributed across independent domains.

So distributed retention connects logical redundancy to power/network/rack topology and correlated-failure assumptions.

---

## Maintenance and labor

The system makes persistence appear like a stable property of an object, but that appearance depends on continuous and event-driven work.

### Automatic system work

- monitor and OSD liveness tracking;
- cluster-map dissemination;
- primary selection;
- version assignment;
- replica forwarding;
- peering and prior-participant discovery;
- PG-log/history exchange;
- missing/stale object identification;
- re-replication after permanent device loss;
- data migration after topology changes.

### Human / institutional work

The bounded papers abstract much operator labor away, but the mechanism assumes someone maintains:

- functioning replacement hardware;
- power/network failure domains;
- monitor infrastructure;
- cluster configuration and placement policy;
- enough spare capacity and bandwidth for repair/migration.

`Self-healing` therefore must not be read as literal absence of maintenance.

---

## Failure / forgetting modes

### 1. Replica loss

One physical embodiment is destroyed or becomes inaccessible. Logical state may survive if enough current state/history remains elsewhere.

### 2. Staleness

A replica physically survives but lacks later ordered updates.

**Physical survival is not semantic currentness.**

### 3. History/currentness loss

Payload fragments may remain while the system lacks enough version/log/membership history to establish which state is authoritative.

### 4. Missing-state forgetting

If the system loses the metadata that a particular object/version ought to exist, physical absence becomes harder to distinguish from legitimate non-membership/deletion. The 2007 design's guarded PG metadata is specifically relevant to avoiding that loss of repair knowledge.

### 5. Insufficient surviving current state

If too much mutually necessary payload/history is lost before repair, the intended object state may no longer be reconstructable.

The historical papers do not justify a timeless universal durability number; do not manufacture one.

### 6. Placement / membership state failure

The ability to identify which OSDs should participate depends on cluster-map/epoch progression.

### 7. Correlated failure

Replica count is not sufficient when replicas share failure domains. Placement policy therefore becomes part of retention engineering.

---

## Cross-case comparisons

### Case 04 — mapped Flash

```text
mapped Flash
logical address remains stable
while physical embodiment changes
because mapping/control state identifies current storage

RADOS
logical object remains stable
while replica membership changes
because placement/version/history state identifies current embodiments
```

The analogy stops there. Flash is controller-local remapping under erase/reclamation constraints; RADOS is a networked system with independently failing participants, temporary primary authority, peering, and distributed recovery.

### Case 100 — ZFS DTL

Case 100 preserves intervals in which replication was deficient so later repair can be bounded. RADOS PG log/missing state instead preserves ordered object history plus knowledge of object versions that should exist but may be missing on participants.

The functional family resemblance is:

```text
repair-control metadata
    != repaired payload itself
```

But DTL and RADOS PG logs are different algorithms, data structures, historical lineages, and failure models.

---

## Historical record vs engineering reconstruction

### Historical record (`H/P`)

The primary sources directly establish that the bounded systems/designs:

- present a logical object store over distributed physical OSDs;
- map objects through PGs to ordered OSD sets;
- use map epochs and temporary primary authority;
- version object/PG updates;
- distinguish visibility/acknowledgement from final disk commit;
- re-peer after relevant membership changes;
- compare replica state/history before accepting a reconstructed PG;
- preserve PG logs/currentness metadata even while some payload replicas are missing;
- recover missing/stale payload after currentness history has been established;
- contain a 2005 implementation predecessor that already separates completeness, peering knowledge, clean replication, persisted group attributes, and soft peer-session state.

### Engineering reconstruction (`E`)

From those mechanisms, this repository infers that:

- logical persistence is separable from persistence of any one physical replica;
- `currentness` is a retained relation, not merely a property of bytes;
- peering is an admission/currentness-reconstruction procedure, not merely copying;
- expected-state metadata can retain repair debt before the corresponding payload is restored;
- negative state (`missing`) can be constitutive of recoverability;
- distributed write success can have multiple protocol-defined retention thresholds.

### Functional analogy (`A`)

- Case 04: logical identity can survive changing physical embodiment because control state identifies current state;
- Case 100: repair-control metadata can persist an outstanding maintenance obligation independently of completed payload repair.

No shared implementation or genealogy is claimed.

### Philosophical interpretation (`Φ`)

This case may later support arguments that identity can be stabilized by relations, histories, and obligations rather than one enduring material token. That interpretation remains downstream of the engineering record and is not needed to establish the case.

---

## Counterexamples and limits

### A primary still exists

It would be too strong to say RADOS has `no privileged copy` without qualification. The bounded protocol gives one OSD temporary primary authority. The safer statement is:

> **No permanently privileged physical replica is required for the logical object's identity to persist.**

### Peering metadata is not payload

A surviving PG log can say what should exist, but it does not magically recreate lost bytes. Metadata retention can preserve the **knowledge of loss/repair obligation** without guaranteeing repair is possible under arbitrary multi-device failure.

### `Active` is not the same as `fully repaired`

The 2007 design can establish enough PG history for service while background recovery remains outstanding. Do not collapse availability/currentness/completeness/full replication into one state.

### The 2005 source is deliberately immature

Commit `88086b83...` says peering is still incomplete, uses RG/RUSH-era structures, and does not prove that every 2007 PG-log/prior-set mechanism already existed unchanged.

### Replication is not generic consensus

This case is not a generic explanation of Paxos, Raft, Byzantine agreement, or quorum databases.

### The 2006 system was a prototype

The OSDI paper explicitly describes prototype status and future work.[^ceph-osdi-future]

### `Self-healing` does not mean maintenance-free

Automatic repair still consumes devices, bandwidth, spare capacity, software, monitoring, and operator-maintained infrastructure.

### Multiple replicas do not guarantee arbitrary durability

Replica count, correlated failures, placement rules, media failures, detection time, repair time, and survival of currentness/history state all matter.

---

## Cross-case result

Case 05 now adds seven distinctions to the repository:

> **replica multiplicity ≠ retained currentness**

Several physical copies may exist while only some represent the current ordered state.

> **physical survival ≠ admission to service**

A replica may retain bytes while membership/history changes force repeering before it can count as current.

> **physical survival ≠ current placement membership**

A replica may retain useful bytes after a map/epoch change while no longer being an intended destination under current placement policy.

> **placement currentness ≠ content currentness**

The cluster map/rule determines where state ought to be; peering/version history determines which surviving state is admissible as current.

> **repair metadata ≠ repaired payload**

The system can retain what should exist and what is missing before material reconstruction is complete.

> **retention can be repair-triggered**

Redundancy can degrade after failure and be restored by copying current state onto replacement members.

> **logical success ≠ durable commit**

A distributed write can pass through protocol-defined stages with different retention guarantees.

Together with Cases 00–04, the maintenance regimes include:

```text
human / positional maintenance       — abacus
continuous regenerative maintenance — delay line
access-triggered restore             — classic core
deadline-driven refresh              — DRAM
capacity/reclaim-triggered work      — mapped Flash
failure/repair-triggered work        — RADOS
```

The sequence is comparative, not evolutionary.

---

## Related repositories

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated RADOS/CRUSH treatment during the 2005–2007 peering and 2006 placement deepening slices.

A broader history of RUSH → CRUSH, EBOFS, peering implementation evolution, monitor/Paxos development, algorithmic distributed placement, bucket evolution, object storage, RAID, erasure coding, or storage networking belongs there if later developed. `technical-retention` should link to that work instead of expanding this case into a general distributed-storage history.

---

## Evidence status

**Status: `grounded`.**

The repository roadmap and case-maturity ledger treat Case 05 as grounded. The canonical text is now aligned with that established repository state rather than retaining its older pre-promotion `first-pass candidate` wording.

Strong points include:

- primary peer-reviewed 2006 system paper with mechanism-level detail;
- direct 2006 CRUSH-paper evidence for deterministic policy-bearing placement, failure-domain rules, map-change reorganization, and target-rank semantics;
- direct 2006 OSDI evidence for cluster-map epochs and map-triggered responsibility recomputation;
- direct 2007 RADOS/dissertation evidence for PG logs, `last_update`, `last_complete`, missing state, prior-set peering, and guarded metadata;
- a dated contemporaneous implementation artifact from August 2005 showing explicit peering/currentness state and persistent-vs-soft control-state separation;
- explicit historical vocabulary;
- a retained-state decomposition separating payload, placement currentness, content currentness, expected state, repair debt, and transient peer sessions.

The two bounded source debts previously named in this file are now materially closed:

- **inspect the 2007 RADOS presentation / add a peering implementation witness** — closed by [`../evidence/05-rados-2005-2007-peering-pg-metadata-retention-deepening.md`](../evidence/05-rados-2005-2007-peering-pg-metadata-retention-deepening.md);
- **inspect the 2006 CRUSH paper directly for placement-specific claims** — closed by [`../evidence/05-crush-2006-map-epoch-placement-currentness-deepening.md`](../evidence/05-crush-2006-map-epoch-placement-currentness-deepening.md).

Remaining work is narrower archival/implementation archaeology rather than a maturity blocker:

1. record printed page / figure anchors from a directly rendered 2006 OSDI PDF if later wording needs page-exact citation beyond the USENIX HTML;
2. bridge the August-2005 RG/RUSH-era code to the 2006–2007 CRUSH/PG implementation without assuming continuity;
3. inspect historically appropriate source for exact cluster-map serialization/persistence and OSD restart behavior;
4. optionally add a bounded historical-revision CRUSH mapping reconstruction or fault-injection experiment if buildability permits;
5. keep later `up`/`acting`/backfill semantics separate unless explicitly version-bounded.

---

## Sources

[^ceph-osdi-5]: Sage A. Weil, Scott A. Brandt, Ethan L. Miller, Darrell D. E. Long, and Carlos Maltzahn, “Ceph: A Scalable, High-Performance Distributed File System,” *Proceedings of the 7th Symposium on Operating Systems Design and Implementation (OSDI '06)*, pp. 307–320, especially §5 “Distributed Object Storage.” USENIX HTML: https://static.usenix.org/event/osdi06/tech/full_papers/weil/weil_html/index.html

[^ceph-osdi-placement]: Weil et al., “Ceph,” §5.1 “Data Distribution with CRUSH,” especially the object → placement group → ordered OSD mapping, cluster map, epoch, and replica placement-rule discussion. https://static.usenix.org/event/osdi06/tech/full_papers/weil/weil_html/index.html

[^ceph-osdi-replication]: Weil et al., “Ceph,” §5.2 “Replication,” especially primary-copy replication and object / PG version assignment. https://static.usenix.org/event/osdi06/tech/full_papers/weil/weil_html/index.html

[^ceph-osdi-safety]: Weil et al., “Ceph,” §5.3 “Data Safety,” especially the distinction between replicated cache acknowledgement and later on-disk commit. https://static.usenix.org/event/osdi06/tech/full_papers/weil/weil_html/index.html

[^ceph-osdi-failure]: Weil et al., “Ceph,” §5.4 “Failure Detection,” especially `down` versus `out`, primary failover, and re-replication. https://static.usenix.org/event/osdi06/tech/full_papers/weil/weil_html/index.html

[^ceph-osdi-recovery]: Weil et al., “Ceph,” §5.5 “Recovery and Cluster Updates,” especially PG version exchange, recent-change logs/content summaries, peering, and retrieval of missing/outdated objects. https://static.usenix.org/event/osdi06/tech/full_papers/weil/weil_html/index.html

[^ceph-osdi-ebofs]: Weil et al., “Ceph,” §5.6 “Object Storage with EBOFS.” https://static.usenix.org/event/osdi06/tech/full_papers/weil/weil_html/index.html

[^ceph-osdi-future]: Weil et al., “Ceph,” §9 “Future Work.” https://static.usenix.org/event/osdi06/tech/full_papers/weil/weil_html/index.html

[^crush-2006]: Sage A. Weil, Scott A. Brandt, Ethan L. Miller, and Carlos Maltzahn, “CRUSH: Controlled, Scalable, Decentralized Placement of Replicated Data,” *SC '06*, November 2006. Project-hosted paper: https://ceph.io/assets/pdfs/weil-crush-sc06.pdf

[^rados-2007]: Sage A. Weil, Andrew W. Leung, Scott A. Brandt, and Carlos Maltzahn, “RADOS: A Scalable, Reliable Storage Service for Petabyte-scale Storage Clusters,” *PDSW '07*, pp. 35–44, DOI 10.1145/1374596.1374606. UCSC SSRC publication record: https://ssrc.us/pub/weil-pdsw07.html

[^weil-thesis]: Sage A. Weil, *Ceph: Reliable, Scalable, and High-Performance Distributed Storage*, PhD dissertation, University of California, Santa Cruz, December 2007, Chapter 6, especially §§6.3.4–6.3.5, printed pp. 134–137. https://www.ceph.io/assets/pdfs/weil-thesis.pdf

[^ceph-2005-peering]: Ceph historical commit `88086b83b7dcb0eb5c092e30fde8570475173f5e`, 2005-08-06, `lots of OSD peering stuff (still not complete)`. https://github.com/ceph/ceph/commit/88086b83b7dcb0eb5c092e30fde8570475173f5e

[^ceph-2005-osdh]: `ceph/osd/OSD.h` at `88086b83...`, including `RGReplicaInfo`, `RGPeer`, `RG_STATE_COMPLETE`, `RG_STATE_PEERED`, `RG_STATE_CLEAN`, and `RG::store/fetch`. https://github.com/ceph/ceph/blob/88086b83b7dcb0eb5c092e30fde8570475173f5e/ceph/osd/OSD.h

[^ceph-2005-osdcc]: `ceph/osd/OSD.cc` at `88086b83...`, especially map handling, `scan_rg`, `handle_rg_peer`, and `handle_rg_peer_ack`. https://github.com/ceph/ceph/blob/88086b83b7dcb0eb5c092e30fde8570475173f5e/ceph/osd/OSD.cc
