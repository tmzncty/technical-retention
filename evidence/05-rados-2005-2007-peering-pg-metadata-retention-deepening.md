# Evidence 05 — RADOS 2005–2007 Peering and PG-Metadata Retention Deepening

## Status

**`bounded deepening complete`**

This record deepens [Case 05 — RADOS Replicated Objects: Retention by Replica Agreement and Repair](../cases/05-rados-replicated-object-repair.md).

It closes one narrow evidence debt from the first-pass case: add a contemporaneous implementation witness for peering/recovery state and inspect the 2007 RADOS presentation closely enough to separate **payload replicas** from the **metadata that says what the placement group ought to contain**.

The bounded result is:

> **RADOS retention depends not only on preserving enough object bytes, but also on preserving enough PG history to distinguish current, missing, stale, and safely recoverable state. In the 2007 design, PG logs and missing-state metadata can remain authoritative even while some object replicas are absent. Peering is therefore not merely data copying; it is an admission procedure that reconstructs the right to treat a replica set as current.**

This is not a claim that every historical or modern Ceph release used the same peering state machine. The 2005 source witness is explicitly incomplete and predates the mature 2007 PG-log design; it is used as a genealogy/implementation witness, not as proof that the 2007 paper's exact algorithm already existed unchanged in 2005.

---

## Bounded question

The canonical case already established from the 2006 OSDI paper that replicas can disagree, that placement changes, and that peering/recovery uses versions and logs before ordinary I/O resumes.

The remaining retention question was narrower:

```text
object bytes survive somewhere
    ?= enough state survives to know what the PG should contain

replica is physically present
    ?= replica may immediately serve as current

recovery metadata exists
    ?= payload repair has already completed
```

This slice answers all three negatively.

---

## 1. Historical implementation record — August 2005 source already makes `PEERED` an epistemic state

Ceph's imported historical repository contains commit `88086b83b7dcb0eb5c092e30fde8570475173f5e`, dated **2005-08-06**, whose commit message says `lots of OSD peering stuff (still not complete)`.

That parenthetical matters: the source is an early implementation artifact, not a finished specification.

At that revision the code still speaks of **replica groups (`RG`)** and uses a RUSH-era mapping path, not the later mature CRUSH/PG implementation. Nevertheless, it already exposes an important retention distinction.

`ceph/osd/OSD.h` defines:

- `RG_STATE_COMPLETE`: the local OSD has the full RG contents;
- `RG_STATE_PEERED`: the OSD has contacted prior-primary / replica participants and/or fetched their content lists sufficiently to `know what's up`;
- `RG_STATE_CLEAN`: the primary considers the group fully replicated.

Those are separate bits.

The implementation therefore does **not** collapse:

```text
local payload completeness
    == knowledge of replica-group history/currentness
    == full replication
```

Instead it already distinguishes them as separate control states.

### Retention significance

This is a contemporaneous implementation witness for a principle that becomes much clearer in the 2007 RADOS description:

```text
having bytes
    != having enough history to admit those bytes as current
```

The distinction is historical/source-level; the phrase `epistemic admission state` is this repository's engineering reconstruction.

Source:

- Ceph historical commit `88086b83...`, 2005-08-06: https://github.com/ceph/ceph/commit/88086b83b7dcb0eb5c092e30fde8570475173f5e
- `ceph/osd/OSD.h` at that commit: https://github.com/ceph/ceph/blob/88086b83b7dcb0eb5c092e30fde8570475173f5e/ceph/osd/OSD.h

---

## 2. Historical implementation record — some RG state is persisted while peer-session state is explicitly soft

The same 2005 `RG` implementation separates persistent group state from in-memory peer-session state.

`RG` contains:

- `role`;
- `state`;
- `primary`;
- `old_replica_set`;
- `peers`.

But the source comments describe `peers` as **`(soft state) active peers`**.

By contrast, `RG::store()` writes collection attributes for:

- `role`;
- `primary`;
- `state`.

`RG::fetch()` reads those attributes back from the object store.

This early implementation therefore already distinguishes:

```text
persistent group control state
    != live peering-session state
```

The evidence is not enough to claim that all information necessary for crash recovery was durably persisted in this 2005 prototype. In particular, the code fragment does not show every field being stored, and the commit itself says peering work is incomplete.

The safe historical claim is only that **the implementation deliberately separates persisted RG attributes from soft active-peer session objects**.

### Engineering reconstruction

For retention analysis, that means `protocol state` must not be treated as one undifferentiated blob.

A system may retain:

```text
membership / role / group-state facts
```

while reconstructing:

```text
live peer conversations
request/response session state
transient synchronization work
```

after restart or map change.

This is functionally comparable to later cases where a durable maintenance basis is re-expanded into transient runtime state, but no historical lineage is implied.

---

## 3. Historical implementation record — a map change invalidates peering status before it destroys local bytes

In `OSD::update_map()` the 2005 source decodes a newer OSD map and then scans known replica groups.

During `scan_rg()` a role or primary change causes the group to clear `RG_STATE_PEERED`, update its role/primary, persist the changed RG state, and initiate new peer notification/session work.

The source does **not** first erase local object data merely because authority changed.

That gives a precise historical relation:

```text
membership / authority change
    -> prior peering knowledge becomes insufficient
    -> PEERED state cleared
    -> new peering required

local object bytes may still exist throughout
```

This is stronger than the loose statement `the system rebalances after a map change`.

It shows that a topology/control-plane transition can invalidate the **admissibility of prior knowledge** independently of the physical survival of local data.

Source:

- `ceph/osd/OSD.cc`, `update_map()` / `scan_rg()` at `88086b83...`: https://github.com/ceph/ceph/blob/88086b83b7dcb0eb5c092e30fde8570475173f5e/ceph/osd/OSD.cc

---

## 4. Historical implementation record — peering exchanges object/version inventories, not merely liveness

The same early source shows the primary asking peers for replica-group state.

`handle_rg_peer()` constructs an acknowledgement containing:

- RG state;
- a `deleted` map;
- a list of objects in the collection;
- each object's `version` attribute.

The primary-side `handle_rg_peer_ack()` then installs that returned state into the per-peer structure.

This is still an unfinished 2005 mechanism, but it proves that peering was already conceived as more than `is the other OSD alive?`.

It exchanged state needed to compare **what objects exist and which versions they carry**.

Thus:

```text
failure detection / reachability
    != replica-state comparison
    != repair completion
```

The distinction later becomes explicit and richer in the 2007 PG-log design.

---

## 5. Historical record — 2007 RADOS makes `last_update`, `last_complete`, PG log, and missing-list state explicit

Sage Weil's December 2007 UCSC dissertation gives a much more mature statement of the RADOS recovery design. Chapter 6, especially §§6.3.4–6.3.5, separates several kinds of PG state.

The dissertation describes each PG as having:

- `last_update`: the most recently applied modification;
- `last_complete`: the point through which required object state is complete locally;
- a short-term PG log containing recent update/delete history and versions;
- a `missing` list summarizing objects absent between the complete and update frontiers.

It states that the short-term PG log is stored **on disk** as well as in RAM or NVRAM when available.

The retention decomposition is therefore:

```text
latest operation known for the PG
    != latest point locally complete
    != recent operation history
    != set of object versions still missing locally
```

These are control/history relations about payload, not the payload bytes themselves.

Primary source:

- Sage A. Weil, *Ceph: Reliable, Scalable, and High-Performance Distributed Storage*, PhD dissertation, UC Santa Cruz, December 2007, Chapter 6, especially pp. 134–137 (printed pagination): https://www.ceph.io/assets/pdfs/weil-thesis.pdf

Publication record:

- UCSC Storage Systems Research Center, `RADOS: A Fast, Scalable, and Reliable Storage Service for Petabyte-scale Storage Clusters`, November 2007: https://ssrc.us/pub/weil-pdsw07.html

---

## 6. Historical record — PG metadata is deliberately guarded even while object replicas are missing

The strongest retention-specific statement in the 2007 RADOS presentation is that OSDs **aggressively replicate the PG log and its record of what the PG should contain even when some object replicas are missing locally**.

The paper/dissertation explains the reason: preserving that metadata simplifies recovery and lets the system reliably recognize data loss.

This yields a relation that the 2006 first-pass case only implied:

```text
currentness / expected-content metadata can survive
    while
some required payload replicas are still absent
```

The system is therefore allowed to know:

> `object version X should exist here`

before it has completed recreating that object locally.

That is a particularly clear example of **retention of an obligation** rather than retention of the fulfilled physical state.

### Engineering reconstruction

The repository can now distinguish:

```text
payload retention
    != expected-state retention
    != repair-debt retention
```

If an object replica is missing but PG history still records that it ought to exist, the system has not silently forgotten the object. It retains enough negative/obligation state to know that material repair remains outstanding.

Conversely, if both payload and the metadata saying it ought to exist were lost, physical absence could become much harder to distinguish from legitimate non-membership or deletion.

That last sentence is an engineering inference about why the metadata matters; it is not quoted as RADOS terminology.

---

## 7. Historical record — peering reconstructs an authoritative history before ordinary service

The 2007 design does not ask only the OSDs in the newest mapping.

When a PG's active set changes, peering considers map epochs and constructs a **prior set** of OSDs that may have participated since the last successful peering interval. The primary collects state such as recent-update boundaries and PG-log ranges, determines the most recent update present on any relevant replica, and requests necessary log fragments.

If logs are insufficient, the design can fall back to a complete PG-content listing.

Only after this metadata reconciliation can replicas agree on what the PG should contain; missing payload can then be recovered in the background.

The key technical-retention sequence is:

```text
physical replicas / remnants exist
    ↓
collect prior-participant metadata
    ↓
reconstruct authoritative PG history
    ↓
identify missing / stale objects
    ↓
admit PG for service under reconstructed currentness
    ↓
continue payload recovery as needed
```

This is why `peering` should not be reduced to copying bytes between nodes.

It is first a **currentness reconstruction / admission procedure**, and only then a basis for repair.

The label `currentness reconstruction / admission procedure` is this repository's engineering vocabulary.

---

## 8. `active` or serviceable is not the same state as `fully repaired`

A particularly useful 2007 boundary is that active replicas can be brought to agreement about **what the PG should contain** even though some objects are still missing locally, and ordinary processing can resume while recovery continues in the background under the described conditions.

Therefore:

```text
PG history reconciled enough for service
    != every replica locally complete
    != desired redundancy fully restored
```

This matters for retention because `available`, `current`, `complete`, and `fully replicated` are distinct service states.

A system can expose a logically current object while still carrying repair debt.

Do not generalize this sentence into a universal modern Ceph rule; it is bounded to the 2007 design described by the source.

---

## 9. A negative-state ledger can be as constitutive as the positive copies

The 2007 PG log / missing-list design provides an unusually concrete example of retained **negative state**.

The system does not merely preserve:

```text
these objects are present
```

It also preserves enough history to state:

```text
these object versions are expected
these ones are not locally complete yet
these operations/deletions happened in this order
```

That gives a useful repository-wide distinction:

```text
retained embodiment
    != retained expectation about embodiment
```

The second can guide the re-creation of the first.

This is an engineering reconstruction from the documented mechanism, not a philosophical claim about absence in general.

---

## 10. Functional comparison — Case 100 ZFS DTL

Case 100's ZFS DTL preserves intervals in which a vdev had less than required replication so later resilvering can select repair work.

Case 05's PG log / missing metadata preserves a different kind of repair-control state: recent ordered object history and knowledge of objects/versions that should exist but are missing or stale on participants.

The functional family resemblance is:

```text
RADOS PG history / missing state
    -> what object-version state should exist and what is absent

ZFS DTL
    -> when replication was deficient and therefore which block births may require repair
```

Both cases show:

```text
repair-control metadata
    != repaired payload itself
```

But they are not the same algorithm, data structure, historical lineage, or failure model.

---

## 11. Functional comparison — Case 04 mapped Flash

The original Case 05 already compares CRUSH placement with Flash logical-to-physical mapping.

This deepening adds a second comparison axis.

Mapped Flash needs control state that says which physical embodiment is **current** after remapping.

RADOS additionally needs distributed history that says which replica/object versions count as **current**, which participants' histories must be consulted, and which expected replicas are still missing.

Thus:

```text
location indirection
    != distributed currentness reconstruction
```

The analogy is functional only. No historical descent from the Flash case is claimed.

---

## 12. Historical genealogy boundary — 2005 source is not the 2007 algorithm frozen in amber

The 2005 implementation artifact is valuable precisely because it is early.

It also creates a risk of overclaiming.

At `88086b83...`:

- the code speaks of `RG`, not the mature later `PG` model;
- mapping is still RUSH-era;
- the commit says peering is `still not complete`;
- the replica-state exchange shown here inventories objects/versions rather than demonstrating the full later short-term PG-log/prior-set algorithm.

Therefore this evidence supports a bounded chronology:

```text
by Aug 2005:
    explicit peering states + role/map-triggered repeering
    + object/version inventory exchange existed in source

by 2007:
    the published RADOS design explicitly describes
    PG logs, last_update, last_complete, missing state,
    prior-set reconstruction, and guarded PG metadata
```

It does **not** establish that every 2007 mechanism was already implemented in August 2005.

---

## 13. Historical record vs engineering reconstruction vs analogy vs philosophy

### Historical record (`H/P`)

Supported directly by contemporaneous source/papers:

- August 2005 source has distinct `COMPLETE`, `PEERED`, and `CLEAN` replica-group states;
- peer-session objects are labelled soft state while some RG attributes are persisted through the object store;
- map/role changes clear `PEERED` and initiate new peering;
- early peering exchanges object inventories and per-object version attributes;
- 2007 RADOS uses per-PG version/history state including `last_update`, `last_complete`, short-term logs, and missing information;
- those logs are described as stored on disk, with RAM/NVRAM copies where available;
- 2007 RADOS deliberately preserves PG metadata even while some object replicas are missing;
- peering considers prior participants/map history before accepting a reconstructed PG state.

### Engineering reconstruction (`E`)

This repository infers that:

- peering is an admission/currentness-reconstruction step, not merely a byte-copy phase;
- expected-state metadata can preserve a repair obligation before the corresponding payload copy is restored;
- physical replica survival and semantic admissibility are separate;
- distributed retention can depend on a negative-state ledger describing what is missing;
- retained control history can be constitutive of the ability to identify data loss.

### Functional analogy (`A`)

- Case 100 DTL: both retain repair-control evidence rather than only payload;
- Case 04 Flash mapping: both separate logical currentness from one fixed physical embodiment.

No shared implementation or genealogy is claimed.

### Philosophical interpretation (`Φ`)

The mechanism may later support arguments about identity being stabilized by records of obligation, absence, or history rather than by one enduring material token.

That interpretation is **not** needed to establish the engineering claims in this evidence package and should remain downstream of them.

---

## 14. Explicit non-claims

This evidence does **not** claim that:

1. the August 2005 peering code was production-ready;
2. the 2005 `RG` implementation was identical to the 2007 RADOS `PG` algorithm;
3. RUSH and CRUSH are interchangeable names for the same historical stage;
4. a `PEERED` bit alone proves payload durability;
5. a PG log is a replacement for payload replication;
6. metadata survival guarantees that missing payload can always be reconstructed;
7. every missing object implies data loss;
8. every physically surviving replica is safe to serve;
9. all modern Ceph versions expose the same state machine as the 2007 dissertation;
10. the 2007 design is a generic consensus algorithm;
11. peering by itself restores desired replica count;
12. active/serviceable necessarily means clean/fully replicated;
13. the early code proves exact crash-durability semantics for every RG field;
14. Case 100 DTL and RADOS PG logs share lineage or data structures;
15. philosophical conclusions follow automatically from these mechanisms.

---

## 15. Claim ledger

| Claim | Evidence class | Strength | Boundary |
|---|---|---:|---|
| 2005 source distinguishes local completeness, peering knowledge, and clean replication | period implementation | strong | early/incomplete RG code |
| 2005 source labels active peers soft state while persisting role/primary/state RG attributes | period implementation | strong | does not prove every crash-recovery requirement |
| map/role changes clear peering state and force new reconciliation | period implementation | strong | August 2005 code only |
| early peering exchanges object/version inventory | period implementation | strong | not yet the full 2007 PG-log algorithm |
| 2007 RADOS distinguishes `last_update`, `last_complete`, PG log, and missing state | primary dissertation/paper | strong | 2007 design |
| 2007 PG log is retained on disk, with RAM/NVRAM use described | primary dissertation | strong | source-described implementation |
| 2007 design guards PG metadata even while payload replicas are missing | primary dissertation/paper | strong | does not promise eventual repair under arbitrary loss |
| peering is best modeled as currentness/admission reconstruction | engineering reconstruction | strong from mechanism | project terminology |
| expected-state metadata is a retained repair obligation | engineering reconstruction | strong from mechanism | not historical vocabulary |
| RADOS PG history and ZFS DTL belong to a broad repair-control family | functional analogy | bounded | no genealogy |

---

## 16. Source ledger

### Primary / contemporaneous implementation

1. Ceph historical commit `88086b83b7dcb0eb5c092e30fde8570475173f5e`, **2005-08-06**, `lots of OSD peering stuff (still not complete)`:  
   https://github.com/ceph/ceph/commit/88086b83b7dcb0eb5c092e30fde8570475173f5e
2. `ceph/osd/OSD.h` at that commit — `RGReplicaInfo`, `RGPeer`, `RG_STATE_COMPLETE`, `RG_STATE_PEERED`, `RG_STATE_CLEAN`, `RG::store/fetch`:  
   https://github.com/ceph/ceph/blob/88086b83b7dcb0eb5c092e30fde8570475173f5e/ceph/osd/OSD.h
3. `ceph/osd/OSD.cc` at that commit — map-version handling, RG scan, repeering, `handle_rg_peer`, object/version inventory exchange:  
   https://github.com/ceph/ceph/blob/88086b83b7dcb0eb5c092e30fde8570475173f5e/ceph/osd/OSD.cc

### Primary / scholarly

4. Sage A. Weil, *Ceph: Reliable, Scalable, and High-Performance Distributed Storage*, PhD dissertation, University of California, Santa Cruz, December 2007, Chapter 6:  
   https://www.ceph.io/assets/pdfs/weil-thesis.pdf
5. Sage A. Weil, Andrew W. Leung, Scott A. Brandt, Carlos Maltzahn, `RADOS: A Scalable, Reliable Storage Service for Petabyte-scale Storage Clusters`, PDSW 2007, pp. 35–44, DOI `10.1145/1374596.1374606`.
6. UCSC Storage Systems Research Center publication record for the PDSW 2007 paper:  
   https://ssrc.us/pub/weil-pdsw07.html

### Repository comparison

7. [Case 04 — Flash Virtual Mapping and Logical Identity](../cases/04-flash-virtual-mapping-logical-identity.md).
8. [Case 100 — ZFS Dirty Time Log](../cases/100-zfs-dirty-time-log-selective-resilver.md).

---

## 17. Related-repository check

A fresh repository search for `RADOS` in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) returned no dedicated treatment during this slice.

Therefore this file keeps only the **retention-specific** evidence chain. A broader genealogy of RUSH → CRUSH, EBOFS, OSD peering implementations, monitor/Paxos evolution, or the history of distributed object stores still belongs in `computing-archaeology` if that project later develops the topic.

---

## 18. Remaining debt after this slice

This deepening closes the canonical case's need for **one contemporaneous implementation artifact** and materially addresses the request to inspect the 2007 RADOS presentation.

Still open:

- record printed page / figure anchors from the 2006 OSDI paper itself;
- inspect the 2006 CRUSH paper directly for placement-specific claims;
- trace the implementation transition from the August 2005 RG/RUSH-era peering code to the mature 2007 PG-log/prior-set implementation without assuming continuity;
- add a bounded reproduction or fault-injection experiment on a historically appropriate Ceph revision if buildability permits;
- locate an independent institutional/scholarly history only if the case later makes chronology claims beyond the primary papers/source.

Those are separable follow-on slices. None is required to establish the bounded result of this file:

> **distributed retention may require preserving the history that says what should exist, not merely preserving whichever payload copies happen to remain physically present.**
