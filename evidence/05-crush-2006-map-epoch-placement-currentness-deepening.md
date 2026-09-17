# Evidence 05 — CRUSH 2006 Map/Epoch Placement-Currentness Deepening

## Status

**`bounded deepening complete`**

This record deepens [Case 05 — RADOS Replicated Objects: Retention by Replica Agreement and Repair](../cases/05-rados-replicated-object-repair.md).

It closes one explicitly listed evidence debt in the earlier Case-05 deepening: direct inspection of the 2006 CRUSH paper for placement-specific claims.

The bounded result is:

> **In early Ceph/RADOS, object location is not simply a durable fact attached to an object. CRUSH recomputes an ordered placement relation from an object/PG identifier, placement policy, and the current cluster map. When the map changes, physically surviving replicas can cease to be current placement targets, new targets can acquire a repair/migration obligation, and all parties need a sufficiently current map epoch before they can agree on where the object now belongs.**

This is not a claim that CRUSH by itself establishes replica content currentness. CRUSH computes intended placement; RADOS peering/version history separately establishes which surviving replica state is current enough to serve or repair from.

---

## Bounded question

The canonical Case 05 already says that CRUSH makes location recalculable and that RADOS uses map epochs, peering, versions, and repair.

The narrower unresolved question was:

```text
if there is no per-object placement directory,
what exactly makes one set of devices the current place for an object?

old replica bytes still exist on osdA
    ?= osdA is still a current placement target

new CRUSH result names osdB
    ?= osdB already contains the required payload

placement can be recomputed
    ?= no retained placement/currentness state is needed
```

The 2006 CRUSH paper and the contemporaneous OSDI Ceph paper answer all three equations negatively.

---

## 1. Historical record — CRUSH computes an ordered target list rather than consulting a per-object directory

The November 2006 SC paper defines CRUSH as a pseudo-random, deterministic data-distribution function for object-based storage systems.

Its input is normally an object or object-group identifier. Its output is a list of storage devices on which replicas should be placed.

The paper explicitly contrasts this design with a conventional per-file or per-object directory. CRUSH needs a compact hierarchical description of the storage cluster plus the applicable placement policy rather than one stored location record per object.

The contemporaneous OSDI 2006 Ceph paper states the same architecture at system level:

```text
object
    -> placement group
    -> CRUSH(PG, cluster map, placement rule)
    -> ordered OSD list
```

The OSDI paper says that locating an object requires the placement group and the OSD cluster map, and that clients, OSDs, and metadata servers can independently calculate placement.

### Retention significance

This is not `location without metadata`.

It is:

```text
no per-object location directory
    != no retained placement state
```

The map and rule are shared retained inputs to a deterministic resolver.

The current physical location relation is therefore generated from retained cluster-level state rather than individually recorded beside each object.

**Primary sources:**

- Sage A. Weil, Scott A. Brandt, Ethan L. Miller, Carlos Maltzahn, “CRUSH: Controlled, Scalable, Decentralized Placement of Replicated Data,” SC 2006, abstract and §§1, 3.1–3.2: <https://ceph.com/assets/pdfs/weil-crush-sc06.pdf>.
- Sage A. Weil et al., “Ceph: A Scalable, High-Performance Distributed File System,” OSDI 2006, §5.1: <https://www.usenix.org/legacy/event/osdi06/tech/full_papers/weil/weil_html/index.html>.

---

## 2. Historical record — placement is policy-bearing, not only load distribution

CRUSH does not merely choose `n` statistically balanced devices.

The paper's placement rules can constrain replica targets according to the physical hierarchy of the installation. Its example selects replicas in different cabinets so that one shared power circuit or network failure does not remove all copies.

The input hierarchy can represent devices, shelves, cabinets, rows, and other nested failure domains.

Thus the target list embodies at least two things at once:

```text
resource-distribution choice
+
failure-domain policy
```

This is important for Case 05 because a surviving copy can be physically readable yet no longer satisfy the current placement policy.

For example, after topology or policy change, three surviving copies in one cabinet are not equivalent to three copies distributed across three required cabinets merely because the byte count is still three.

That last sentence is an engineering reconstruction from the policy mechanism; it is not a quoted 2006 statement about that exact scenario.

---

## 3. Historical record — failed and overloaded devices remain represented but cease to be admissible targets for selected placements

CRUSH §3.2.1 gives an especially useful distinction.

Failed or overloaded devices are marked in the cluster map but are **left in the hierarchy**. During selection they are rejected and an alternate target is chosen.

For failed devices, the algorithm restarts the relevant selection recursion and redistributes affected items across available storage.

Therefore the historical mechanism already separates:

```text
device remains represented in placement topology
    != device is currently admissible as a target
```

This matters because `present in the map` is not a one-bit synonym for `owns current replica placement`.

A failed device can remain part of the hierarchy for reorganization reasons while being excluded from the actual selected result.

### Engineering reconstruction

That gives three different relations:

```text
topological membership
    != placement admissibility
    != payload possession
```

An OSD may retain payload bytes while being marked failed/out for current placement purposes.

CRUSH alone does not say whether those bytes are the newest object version. That is a RADOS peering/version question.

---

## 4. Historical record — a simple device failure changes placement for only the affected share

Section 3.3, “Map Changes and Data Movement,” treats device failure as a cluster-map change.

For an individual failed device, the paper leaves the device in the hierarchy but rejects it during selection. The authors state that the resulting map change remaps the minimum fraction of data associated with that failed device: approximately the failed device's weight divided by total system weight.

The important retention point is not the exact formula alone.

It is the shape of the transition:

```text
old map M0
    -> object/PG maps to target set T0

failure recorded in new map M1
    -> same object/PG identifier is re-evaluated
    -> failed target rejected
    -> replacement target selected
    -> target set T1 differs only where required
```

The logical object identifier can stay unchanged while the current embodiment relation changes.

This is a named historical mechanism for **location discontinuity under identity continuity**.

---

## 5. Historical record — expansion/removal changes the resolver itself, not only one object's metadata

CRUSH also addresses cluster expansion and removal.

The paper explains that changes to the hierarchy or item weights can move data beyond the absolute theoretical minimum because the cluster map is a weighted hierarchical decision tree.

The different CRUSH bucket types intentionally trade mapping computation against reorganization efficiency:

- uniform buckets are fast but can cause broad reshuffling when modified;
- list buckets can be close to optimal for particular addition patterns but poor for some removals;
- tree buckets bound movement according to tree depth;
- straw buckets spend more computation to obtain strong reorganization behavior under arbitrary item changes.

This matters for retention analysis because there is no timeless one-to-one statement of:

```text
object X lives on device Y
```

independent of the map version.

Instead:

```text
placement = f(identifier, rule, cluster map)
```

and changing one of those retained inputs can change the currently intended embodiment relation.

### Boundary

`minimal movement` or `efficient reorganization` does **not** mean `no movement`.

CRUSH is explicitly designed to make dynamic placement changes manageable, not to freeze the original location forever.

---

## 6. Historical record — replica-list position can itself carry semantics

CRUSH §3.2.2 distinguishes replication from parity/erasure-coding placement.

For primary-copy replication, the paper notes that after failure it may be desirable for an existing replica target to become the new primary.

For parity/erasure coding, the rank/position of each target in the CRUSH output can be critical because different targets may hold different pieces of the encoded object. The failed position should be replaced in place while other targets preserve their ranks.

Thus even the output list is not always a set whose members can be arbitrarily permuted.

The paper supports this bounded decomposition:

```text
target membership
    != target rank
    != current payload/version state
```

The first two are placement outputs. The third remains a higher-level data-currentness question.

### Retention significance

A retained placement relation may need to preserve not only **which** devices are involved, but also **which role/position** each device occupies in the redundancy geometry.

This is particularly important when later cases compare replication and erasure-coded systems.

---

## 7. Historical record — Ceph gives the placement relation an explicit epoch

The OSDI 2006 Ceph paper supplies a system-level currentness mechanism that the CRUSH algorithm paper by itself does not define.

The OSD cluster map contains an **epoch number** that increments whenever the map changes.

The paper states that OSD requests carry the client's map epoch so that participants can agree on the current distribution of data. OSDs exchange incremental map updates, and replies can carry newer map information to a client that is behind.

This gives a precise historical relation:

```text
same object / same PG
+
different map epoch
    -> potentially different current placement result
```

Therefore:

```text
CRUSH determinism
    != timeless placement
```

CRUSH is deterministic **relative to its inputs**. A stale map can deterministically produce an old placement relation.

### Engineering reconstruction

The map epoch is not itself the object payload, nor is it a per-object version.

It is evidence about the **configuration context under which placement is being resolved**.

That means the system needs both:

```text
object currentness evidence
and
placement-context currentness evidence
```

They solve different problems.

---

## 8. Historical record — receiving a new map triggers responsibility recomputation before payload convergence

OSDI §5.5 makes the transition operational.

When an OSD receives a new cluster map, it scans locally stored placement groups and recalculates the CRUSH mapping to determine whether it is now primary, replica, or no longer responsible.

If membership changed — or if the OSD has just booted — peering follows. The primary gathers PG versions/log state, determines the most recent PG contents, and tells replicas what the PG should contain.

Only after this currentness reconstruction is ordinary I/O admitted. Missing or stale payload objects can then be recovered in the background.

The sequence is therefore:

```text
new map becomes authoritative
    ↓
recompute intended placement
    ↓
placement membership may change
    ↓
peer/reconstruct object-history currentness
    ↓
admit service
    ↓
material recovery/migration may continue
```

This directly blocks a common shortcut:

```text
new target selected
    != payload already present there
```

CRUSH decides **where state ought to be** under the current map. RADOS recovery performs the material work required to make that relation true.

---

## 9. Placement currentness and replica content currentness are orthogonal

The paired 2006 papers now allow Case 05 to state this more sharply.

### Placement currentness

Question:

> Under the current cluster map and placement policy, which OSDs are the intended targets and in what order/role?

Evidence:

- CRUSH map;
- device failure/overload state;
- placement rules;
- map epoch.

### Replica content currentness

Question:

> Among surviving/current/prior participants, which object/PG history is the most recent and which local copies are missing or stale?

Evidence:

- object/PG versions;
- PG logs;
- prior participants;
- peering state;
- missing-object state.

These can diverge.

Example reconstruction:

```text
osdA contains a recent object replica
but
osdA is no longer selected by the current map

osdB is selected by the current map
but
osdB has not yet recovered the object
```

Neither statement alone identifies the object that should be served.

The system needs both the current placement context and the current content history.

---

## 10. Physically surviving old placement can become repair source without remaining destination authority

CRUSH's design goal of minimizing movement means that many old targets stay selected after a small map change, while only affected placements move.

RADOS recovery also consults current and former participants when necessary.

That supports a useful engineering distinction:

```text
surviving old replica
    may remain useful as recovery evidence/source

surviving old replica
    != guaranteed member of new intended target set
```

So physical survival can preserve **repair value** after it loses **placement authority**.

This is analogous to, but not historically descended from, storage systems in which an obsolete physical embodiment remains readable until migration/reclamation completes.

---

## 11. Deterministic recomputation does not abolish retention obligations

It would be easy to misread CRUSH as eliminating placement state because there is no per-object directory.

The mechanism shows the opposite.

What is eliminated is one particular representation:

```text
per-object stored location list
```

What remains necessary is shared/recoverable state sufficient to reproduce the same current relation:

```text
object/PG identity
+ cluster topology/weights
+ device state
+ placement rule
+ sufficiently current map epoch
```

If those inputs are lost, incompatible, or stale, the fact that the mapping function is deterministic does not recover the intended current placement by magic.

Thus:

> **reconstructable relation != relation requiring no retained basis**

This is engineering reconstruction from the documented mechanism.

---

## 12. Failure-domain placement is part of recoverability margin, not just location aesthetics

CRUSH rules can deliberately separate replicas across cabinets, racks, power domains, or other failure-correlated regions.

The current placement relation therefore carries a safety property beyond simple reachability.

After a placement change, the system may need to restore not merely the configured replica count but the configured **failure-domain distribution**.

This yields:

```text
N readable copies
    != N copies satisfying current placement policy
```

and:

```text
replica-count restoration
    != placement-policy restoration
```

The exact modern Ceph state labels used for such conditions are outside this 2006 slice. The claim is bounded to what the 2006 CRUSH policy mechanism logically requires.

---

## 13. Functional analogy — Case 04 mapped Flash

Case 04 and Case 05 now support a more precise comparison than `both remap data`.

### Mapped Flash

A controller retains/reconstructs a relation such as:

```text
logical sector L
    -> current physical embodiment P
```

Old physical pages can remain after `P` changes.

### RADOS / CRUSH

The system retains/reconstructs a relation such as:

```text
placement group G
+ map epoch E
+ rule R
    -> ordered intended OSD targets T
```

Old replicas can remain after `T` changes.

The common functional pattern is:

```text
stable designation
    + retained resolver context
    -> current embodiment relation
```

But the mechanisms differ strongly:

- Flash mapping is normally controller-local and directly records/reconstructs logical-to-physical currentness;
- CRUSH algorithmically derives placement from shared cluster-level state;
- RADOS then needs a separate distributed peering/version layer to establish payload currentness.

No historical lineage is claimed.

---

## 14. Functional analogy — configuration-currentness versus progress-currentness

Case 42 Kafka cleaner and Case 152 SQLite checkpoint work distinguish saved maintenance progress from the current geometry to which that progress refers.

CRUSH provides a different kind of currentness problem:

```text
map/configuration context changes
    -> same deterministic resolver can yield a different target set
```

The family resemblance is only this:

> a retained coordinate or rule is meaningful only relative to the state space that gives it a referent.

CRUSH map epochs are **not** maintenance checkpoints, and no shared genealogy is implied.

---

## 15. Philosophical interpretation — identity can outlive place only through a retained resolver relation

The mechanism permits a cautious downstream philosophical observation.

A RADOS object can remain `the same` logical object while its physical replica set changes.

But this is not immaterial persistence.

The continuity is technically mediated by retained relations:

- object/PG designation;
- a current cluster-map context;
- placement policy;
- replica/content history;
- peering and repair.

Thus the physical location can change without logical identity disappearing, but only because the system preserves or reconstructs the machinery that determines what counts as the object's current embodiment.

This is a philosophical interpretation of the engineering result, not a claim made by the 2006 authors.

---

## 16. Historical record vs engineering reconstruction vs functional analogy vs philosophy

### Historical record (`H/P`)

Directly supported by the 2006 CRUSH and OSDI papers:

- CRUSH maps an identifier to an ordered list of devices without a per-object location directory;
- the map contains a hierarchical description of available devices and placement policy;
- rules can separate replicas across failure domains;
- failed/overloaded devices can remain in the hierarchy while being rejected as selected targets;
- device failures and hierarchy modifications alter data placement and induce bounded reorganization;
- different CRUSH bucket types make explicit computation/reorganization tradeoffs;
- target rank can matter for primary-copy and coded placement;
- Ceph cluster maps carry epochs that change with the map;
- requests carry client map epochs;
- an OSD receiving a changed map recomputes PG responsibility;
- membership changes lead to peering before ordinary I/O;
- missing/stale objects may be recovered after service-admissible PG history is reconstructed.

### Engineering reconstruction (`E`)

This repository infers that:

- placement currentness and content currentness are distinct relations;
- physical replica survival does not prove current placement membership;
- current placement membership does not prove local payload completion;
- a deterministic placement function still depends on retained resolver inputs;
- a previous target may retain repair value after losing destination authority;
- replica-count restoration and failure-domain-placement restoration are distinct obligations.

### Functional analogy (`A`)

- Case 04 mapped Flash: stable designation can outlive changing physical embodiment through a retained resolver relation;
- Cases 42/152: referent/context currentness matters, although those cases concern maintenance progress rather than replica placement.

No shared historical lineage is claimed.

### Philosophical interpretation (`Φ`)

Logical identity can persist through location replacement only because the system retains/reconstructs relations that decide what currently counts as the object's embodiment.

This interpretation is downstream of the technical evidence.

---

## 17. Explicit non-claims

This evidence does **not** claim that:

1. CRUSH by itself establishes which replica contains the newest payload;
2. a CRUSH target is automatically a complete replica;
3. a physically surviving old target remains a current target after every map change;
4. a failed OSD is erased when it is marked failed;
5. leaving a failed device in the hierarchy means continuing to select it normally;
6. `map epoch` is an object version number;
7. `map epoch` is a complete history of all placement decisions;
8. every map change moves every object;
9. minimal expected movement means zero movement;
10. the theoretical movement bound proves exact behavior for every practical hierarchy;
11. every CRUSH bucket type has identical reorganization behavior;
12. the 2006 CRUSH paper describes every later Ceph `up`/`acting` semantic;
13. the 2006 monitor implementation was already complete;
14. map agreement alone makes a PG safe to serve;
15. peering alone restores desired replica count;
16. replica count alone proves failure-domain policy is satisfied;
17. primary-copy replica rank and erasure-code fragment rank are historically or semantically identical;
18. Case 04 Flash mapping and CRUSH share implementation lineage;
19. deterministic computation eliminates the need to retain configuration state;
20. old replicas become useless immediately when placement changes;
21. CRUSH placement policy is equivalent to consensus;
22. a current target list proves durable on-disk commitment;
23. this slice establishes modern Ceph behavior beyond the 2006 evidence boundary;
24. the paper establishes invention priority for algorithmic distributed placement;
25. philosophical claims about identity follow automatically from the implementation.

---

## 18. Claim ledger

| Claim | Evidence class | Strength | Boundary |
|---|---|---:|---|
| CRUSH deterministically maps an identifier to ordered storage targets without a per-object directory | primary 2006 paper | strong | relative to map/rule inputs |
| placement rules can encode failure-domain separation | primary 2006 paper | strong | policy mechanism, not guarantee under arbitrary loss |
| failed/overloaded devices may remain in hierarchy while being rejected during selection | primary 2006 paper | strong | CRUSH 2006 mechanism |
| an individual device failure remaps only the affected weighted share in the described case | primary 2006 paper | strong | model/design result, not every hierarchy modification |
| hierarchy/bucket changes create explicit reorganization tradeoffs | primary 2006 paper | strong | bucket-specific behavior |
| replica-list rank can carry redundancy semantics | primary 2006 paper | strong | replication/coding distinction |
| Ceph cluster maps use epochs and tag requests with the client's epoch | primary OSDI 2006 paper | strong | 2006 Ceph design |
| new maps cause OSDs to recompute PG responsibility and peer on membership change | primary OSDI 2006 paper | strong | 2006 RADOS design |
| placement currentness != content currentness | engineering reconstruction | strong from paired mechanisms | project terminology |
| old replica can remain physically useful after losing current placement membership | engineering reconstruction | bounded | usefulness depends on peering/version validity |
| deterministic placement still depends on retained resolver context | engineering reconstruction | strong | not historical vocabulary |
| mapped Flash and CRUSH share a functional identity/location pattern | functional analogy | bounded | no genealogy |

---

## 19. Source ledger

### Primary / contemporaneous technical sources

1. Sage A. Weil, Scott A. Brandt, Ethan L. Miller, Carlos Maltzahn, **“CRUSH: Controlled, Scalable, Decentralized Placement of Replicated Data,”** Proceedings of SC 2006, November 2006. Direct author/project PDF:  
   <https://ceph.com/assets/pdfs/weil-crush-sc06.pdf>
2. Sage A. Weil, Scott A. Brandt, Ethan L. Miller, Darrell D. E. Long, Carlos Maltzahn, **“Ceph: A Scalable, High-Performance Distributed File System,”** OSDI 2006, pp. 307–320. USENIX HTML full text:  
   <https://www.usenix.org/legacy/event/osdi06/tech/full_papers/weil/weil_html/index.html>
3. UCSC/SSRC publication chronology listing CRUSH on 15 November 2006 and the OSDI Ceph paper on 6 November 2006:  
   <https://www.crss.ucsc.edu/person/sage.html>

### Existing repository evidence

4. [Case 05 — RADOS Replicated Objects](../cases/05-rados-replicated-object-repair.md).
5. [Evidence 05 — 2005–2007 Peering and PG-Metadata Retention](05-rados-2005-2007-peering-pg-metadata-retention-deepening.md).
6. [Case 04 — Flash Virtual Mapping and Logical Identity](../cases/04-flash-virtual-mapping-logical-identity.md).
7. [Case 42 — Kafka cleaner checkpoint/currentness](../cases/42-kafka-log-cleaner-checkpoint-retention.md).
8. [Case 152 — SQLite WAL checkpoint/backfill retention](../cases/152-sqlite-wal-checkpoint-backfill-reader-retention.md).

---

## 20. Related-repository check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `CRUSH`, `Ceph RADOS`, and related combined terms returned no dedicated CRUSH/RADOS technical-history packet to reuse during this slice.

Accordingly, this file keeps only the retention-specific seam:

```text
stable object/PG designation
    + current cluster-map context
    + placement rule
    -> current intended target relation
    -> peering/content-currentness qualification
    -> migration/recovery obligation
```

A broader history of RUSH→CRUSH, algorithmic placement, bucket evolution, monitor-map governance, production deployment, or later `up`/`acting` semantics belongs primarily in `computing-archaeology` if that repository develops the subject.

---

## 21. Remaining debt after this slice

This slice closes the earlier evidence debt to inspect the 2006 CRUSH paper directly for placement-specific claims.

Still open as separable follow-on work:

- trace the implementation transition from the August-2005 RG/RUSH-era source to the 2006 CRUSH/PG implementation without assuming continuity;
- inspect a historically appropriate 2006–2007 source revision for exact cluster-map serialization/persistence and OSD restart behavior;
- reconstruct one old-map/new-map example with the contemporary CRUSH implementation to show which PGs move and which remain stable;
- examine monitor map-consistency / epoch-distribution implementation only if a later claim depends on exact failure behavior;
- keep later `up`/`acting`/backfill semantics separate from the 2006 evidence unless explicitly version-bounded;
- broaden placement-function genealogy (RUSH, consistent hashing, Sorrento, etc.) only in coordination with `computing-archaeology`.

None of those debts blocks the bounded conclusion:

> **The retained identity of a distributed object is not tied to one enduring location. Its current location is a versioned/policy-bearing relation that must be reproducible from sufficiently current cluster state, while a separate peering/history mechanism determines which surviving payload state is admissible as current.**
