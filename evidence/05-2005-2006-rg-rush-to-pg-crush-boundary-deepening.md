# Evidence 05 — 2005–2006 RG/RUSH → PG/CRUSH Boundary Deepening

## Status

**`bounded deepening complete`**

This record deepens [Case 05 — RADOS Replicated Objects: Retention by Replica Agreement and Repair](../cases/05-rados-replicated-object-repair.md).

It closes one explicitly listed implementation-archaeology debt: bridge the August-2005 `RG` / RUSH-era source witness to the 2006 `PG` / CRUSH architecture **without assuming that the later implementation is merely the earlier code with renamed classes**.

The bounded result is:

> **Between the August-2005 unfinished peering source and the end of 2006, Ceph's visible implementation vocabulary and placement/recovery structures changed materially: `repgroup_t` / `RG` and a RUSH-backed `OSDMap` give way to `pg_t` / `PG`, explicit PG history/log/missing structures, and a CRUSH-backed PG→OSD mapping path. The retention problem is recognizably continuous — membership changes can invalidate prior replica-currentness knowledge even while bytes survive — but the historical record inspected here does not justify treating `RG = PG`, `RUSH = CRUSH`, or the two peering state machines as one unchanged mechanism.**

This is deliberately a **two-endpoint bridge plus contemporaneous published architecture**, not a full genealogy of every intermediate Ceph commit.

---

## Bounded question

The earlier Case-05 deepening used the 2005 source as a contemporaneous predecessor because it already separates:

```text
local completeness
    != peering/currentness knowledge
    != clean/full replication
```

But it also warned that the revision still used `RG` / RUSH-era structures and that the commit itself said peering was `still not complete`.

The unresolved question was therefore:

```text
2005 RG/RUSH predecessor
    ?
    ↓
2006–2007 PG/CRUSH RADOS design
```

What can be shown directly across that boundary, and what must remain unclaimed?

This note asks only four things:

1. what group/placement state the August-2005 code actually names;
2. what changed in the 2006 published architecture;
3. whether late-2006 source actually contains the later PG/CRUSH structures rather than only paper vocabulary;
4. which retention relation can be compared safely across the two endpoints.

---

## 1. Source custody and chronology

### August 2005 implementation endpoint

Primary source:

- Ceph historical Git commit `88086b83b7dcb0eb5c092e30fde8570475173f5e`;
- date: **2005-08-06**;
- imported SVN revision: `@485`;
- commit message begins: **`lots of OSD peering stuff (still not complete)`**.

Relevant files:

- `ceph/osd/OSD.h`
- `ceph/osd/OSD.cc`
- `ceph/osd/OSDMap.h`

Commit:

<https://github.com/ceph/ceph/commit/88086b83b7dcb0eb5c092e30fde8570475173f5e>

### November 2006 published architecture

Primary peer-reviewed source:

- Sage A. Weil, Scott A. Brandt, Ethan L. Miller, Darrell D. E. Long, Carlos Maltzahn, “Ceph: A Scalable, High-Performance Distributed File System,” OSDI 2006, November 2006, especially §§5.1–5.5.

USENIX record / HTML:

<https://www.usenix.org/legacy/events/osdi06/tech/full_papers/weil/weil_html/>

### December 2006 implementation endpoint

Primary source:

- Ceph historical Git commit `283b68e12a9847ca7ea7adb16d9a9b45af138ef3`;
- date: **2006-12-06**;
- imported SVN revision: `@977`;
- commit message: **`improved support for forcing the first element of a crush result`**.

The changed files include:

- `ceph/crush/crush.h`;
- `ceph/osd/OSDMap.h`.

The repository at that same revision also contains:

- `ceph/osd/PG.h`.

Commit:

<https://github.com/ceph/ceph/commit/283b68e12a9847ca7ea7adb16d9a9b45af138ef3>

### Chronological limit

The dates establish **observed endpoints**, not the exact moment of transition.

This note does **not** claim:

```text
2005-08-06
    + one identifiable rename/refactor
    = 2006 PG/CRUSH
```

Finding the precise intermediate change sequence would be broader source genealogy and belongs primarily in `computing-archaeology`.

---

# Historical record

## 2. August 2005 — the unit is a `Replica Group (RG)`

`ceph/osd/OSD.h` at `88086b83...` explicitly defines:

```text
RG - Replica Group
```

The `RG` object carries, among other fields:

- a `repgroup_t rgid`;
- a role;
- state bits;
- a primary identity;
- an old replica set;
- active peer objects;
- deleted-object information for unstable states.

Three state bits matter especially for retention analysis:

```text
RG_STATE_COMPLETE
    local OSD has full RG contents

RG_STATE_PEERED
    enough contact/content-list exchange has occurred
    to know the replica-group situation

RG_STATE_CLEAN
    primary considers the group fully replicated
```

The file labels active `peers` as **soft state** while `RG::store()` / `RG::fetch()` persist `role`, `primary`, and `state` as collection attributes.

These details are already analyzed in the earlier peering deepening; here they matter only as the **pre-boundary endpoint**.

Historical conclusion:

```text
2005 visible group abstraction = RG / repgroup_t
```

not yet the later `PG` implementation vocabulary.

---

## 3. August 2005 — placement is explicitly RUSH-backed

The stronger boundary evidence comes from `ceph/osd/OSDMap.h` at the same revision.

The file includes:

```text
#include "rush.h"
```

and describes `OSDGroup` as a group of identical disks added to the cluster.

The `OSDMap` holds:

```text
vector<OSDGroup> osd_groups;   // RUSH disk groups
Rush *rush;                    // rush implementation
```

Its mapping comments are explicit:

```text
map (repgroup) to a raw list of osds.
this is where we invoke RUSH.
```

`repgroup_to_raw_osds()` calls `rush->GetServersByKey(...)`.

The code then derives nonfailed / acting OSD lists by filtering RUSH results through `failed_osds` and `down_osds`.

Therefore the 2005 endpoint can be stated without inference:

```text
object/file layout
    -> repgroup_t / RG
    -> RUSH-backed OSD mapping
    -> current acting primary / replicas after down/failed filtering
```

This is not CRUSH terminology retroactively applied to 2005 source.

---

## 4. The 2005 source already ties map change to requalification of replica knowledge

The same August source is valuable because the later architectural change did **not** invent the retention problem from nothing.

As recorded in the earlier Evidence 05 packet, map/role changes clear prior `PEERED` state and trigger fresh peering work even though local object bytes may remain present.

The historical relation is therefore already visible in the predecessor:

```text
placement / authority context changes
    ↓
old replica-currentness knowledge no longer sufficient
    ↓
requalification / peering required
```

This is the continuity that can safely be compared later.

It is **not** proof that the later PG-log/prior-set algorithm was already present in 2005.

---

## 5. November 2006 — the published unit is a placement group (`PG`), mapped by CRUSH

The OSDI 2006 paper describes a different visible architecture.

Its data-distribution chain is:

```text
object
    -> placement group (PG)
    -> CRUSH(PG, OSD cluster map, placement rule)
    -> ordered OSD list
```

The paper says objects are first mapped into placement groups with a hash/mask scheme, and PGs are then mapped to OSDs by **CRUSH (Controlled Replication Under Scalable Hashing)**.

Placement requires the PG plus the OSD cluster map. Participants can independently calculate locations from those shared inputs.

The same paper separately describes recovery after map change: OSDs iterate over locally stored PGs, recompute responsibility, and perform peering when membership has changed or an OSD has just booted.

Thus by the published November-2006 architecture, the visible vocabulary is no longer merely the August-2005 RG/RUSH vocabulary.

Historical conclusion:

```text
2006 published group abstraction = placement group (PG)
2006 published placement function = CRUSH
```

---

## 6. December 2006 source — `OSDMap` is actually calling CRUSH for PG placement

The `283b68e...` source change is useful because it prevents a paper/code ambiguity.

Its `ceph/osd/OSDMap.h` patch contains the `PG_LAYOUT_CRUSH` path and invokes:

```text
crush.do_rule(...)
```

on the PG placement seed / rule context to produce an OSD vector.

The same patch defines PG roles such as:

```text
PG_ROLE_HEAD
PG_ROLE_ACKER
PG_ROLE_MIDDLE
PG_ROLE_STRAY
```

and computes a role from the OSD's rank in the mapped result.

The commit also modifies `ceph/crush/crush.h` itself, including hierarchy/parent indexing and forced-result support.

So this is direct implementation evidence that by **2006-12-06**:

```text
PG mapping path
    + CRUSH implementation
    + PG role computation
```

coexist in the source tree.

This does not tell us exactly which earlier revision first introduced each feature.

---

## 7. December 2006 source — `PG` is not merely a spelling change for the old `RG`

`ceph/osd/PG.h` at the same December revision defines:

```text
PG - Replica Placement Group
```

Its internal representation is materially richer than the August-2005 `RG` declaration inspected here.

`PG::Info` contains:

- `pgid`;
- `last_update`;
- `last_complete`;
- log-bottom / backlog state;
- `last_epoch_started` / `last_epoch_finished`;
- history including `same_since`, `same_primary_since`, and `same_acker_since`.

The comments make a specific distinction: `last_complete` means the PG locally has the required object state through that version boundary; it is not just the latest update observed.

`PG::Missing` separately tracks:

```text
object -> missing version
missing version -> object
object -> location where it may be obtained
```

And `PG::Log` records recent update/delete history with `eversion_t` versions and request identities.

The safe conclusion is:

```text
2006 PG implementation
    has explicit history/log/missing structures
that are not present as the same structures
in the inspected 2005 RG declaration
```

That is enough to reject a casual `RG was just renamed PG` shortcut.

It is **not** enough to claim every one of those structures was invented between exactly those two sampled commits, because intermediate source was not exhaustively reconstructed here.

---

## 8. The retention problem survives the architectural change

Across the two endpoints, the machinery changes, but one bounded problem remains recognizable.

### 2005 endpoint

```text
local RG bytes may survive
    + map/role changes
    -> old PEERED knowledge cleared
    -> replica state must be compared again
```

### 2006 endpoint

```text
local PG bytes may survive
    + cluster-map/epoch changes
    -> placement responsibility recomputed
    -> PG history/log state used during peering/recovery
```

The common retention relation is therefore not a class name.

It is:

> **Physical replica survival does not by itself preserve the authority to treat that replica as current after placement/membership context changes.**

This is a controlled functional continuity statement.

It is not a claim of unchanged implementation.

---

# Engineering reconstruction

## 9. Separate three kinds of continuity

The bridge is easiest to state by separating three questions.

### A. Problem continuity

Did the system in both periods need to recover currentness after placement/membership change while bytes might survive?

**Yes, directly supported by the bounded records.**

### B. Conceptual / vocabulary continuity

Did both periods use identical names and abstractions?

**No.** The inspected endpoints visibly differ: `RG` / `repgroup_t` / RUSH versus `PG` / `pg_t` / CRUSH.

### C. implementation genealogy

Can we say exactly how every old RG/RUSH structure transformed into every later PG/CRUSH structure?

**No, not from this bounded slice.**

Therefore:

```text
same retention problem
    != same abstraction name
    != same state machine
    != proven direct line-by-line genealogy
```

---

## 10. `group identity` and `placement resolver` are independently mutable design choices

The endpoints also show that two dimensions change together but should not be collapsed.

2005:

```text
replica-group abstraction
    + RUSH resolver
```

late 2006:

```text
placement-group abstraction
    + CRUSH resolver
```

The historical record here does not prove that changing one logically required changing the other.

For retention analysis, this matters because the system needs both:

```text
a unit whose replica history/currentness can be reasoned about
and
a resolver that says which OSDs should currently embody that unit
```

Those are separable functions even when one implementation revision changes both.

---

## 11. Later metadata richness should not be back-projected into the predecessor

The December-2006 `PG` exposes:

```text
last_update
last_complete
log range/backlog
history epochs
missing-object versions
```

The August-2005 `RG` source exposes a different, earlier arrangement built around local/peer inventories and coarser state bits.

So the following reconstruction is prohibited:

```text
2005 RG_STATE_PEERED
    == 2006 PG log + prior history + Missing
```

They serve a partially overlapping currentness/recovery function, but the data structures and evidenced semantics differ.

The safe comparison is functional only:

```text
both retain/reconstruct evidence needed
before surviving replica bytes count as current
```

---

# Controlled cross-case / cross-version comparison

## 12. Case 05 internal version comparison

This is an unusual comparison because both sides belong to the same project lineage, but project membership alone does not license semantic identity.

| Dimension | August 2005 source | November/December 2006 record |
|---|---|---|
| Group term | `RG`, `Replica Group`, `repgroup_t` | `PG`, `placement group`, `pg_t` |
| Placement | RUSH-backed `OSDMap` | CRUSH-backed PG mapping |
| Currentness evidence | RG state bits + peer object/version inventories | PG `Info` + versioned log + `Missing` + epoch history |
| Map-change effect | clear prior `PEERED`, re-peer | recompute PG responsibility, peer/recover under new map |
| Exact genealogy | not established | not established backwards |

The table is a bounded comparison of inspected sources, not a claim that every unlisted component changed at exactly the same time.

---

## 13. Functional comparison with mapped Flash remains bounded

Case 04 and Case 05 both show that a stable logical identity can survive changes in physical placement.

But this bridge adds a warning:

```text
same high-level retention function
    does not imply
stable implementation vocabulary across versions
```

That warning applies both across different technologies and across revisions of the **same** distributed-storage project.

No Flash→Ceph genealogy is implied.

---

# Philosophical interpretation

## 14. Historical identity is not preserved by forcing vocabulary to stay still

A downstream project-level interpretation is possible:

> A technical system can preserve a recognizable problem — how to decide which surviving embodiments still count as current — while substantially changing the names and machinery through which it answers that problem.

This interpretation is useful for `technical-retention` because it blocks a common historical mistake: treating later terminology as though it had always been present.

But the philosophical point is downstream.

The historical claim remains only that the inspected 2005 and 2006 records differ in the concrete ways listed above.

---

# Explicit non-claims

This packet does **not** claim that:

1. `RG` was simply renamed `PG`;
2. RUSH was simply renamed CRUSH;
3. the 2005 RG state machine is the same as the 2006 PG state machine;
4. `RG_STATE_PEERED` equals later PG peering semantics;
5. the August-2005 source is a finished or production peering implementation;
6. the December-2006 source is identical to the OSDI artifact used for the November paper;
7. every December-2006 PG field first appeared after August 2005;
8. commit `283b68e...` is the first CRUSH implementation;
9. commit `283b68e...` is the first PG implementation;
10. this note identifies the first use of the term `placement group`;
11. this note identifies the first use of CRUSH in Ceph source;
12. every intermediate 2005–2006 revision has been audited;
13. the 2005 RUSH algorithm and 2006 CRUSH algorithm are shown here to share one direct code lineage;
14. the two placement algorithms have identical movement or failure-domain properties;
15. the 2005 `OSDMap::version` is semantically identical to the later published map-epoch mechanism in every respect;
16. physically surviving replicas are automatically current in either design;
17. peering is only liveness detection;
18. later PG `Missing` state is merely a renamed 2005 peer object inventory;
19. the December-2006 source proves later 2007 prior-set semantics in full;
20. this packet proves crash consistency or power-loss durability of the control metadata;
21. RUSH→CRUSH development history belongs wholly in this repository;
22. modern Ceph retains these exact implementation structures;
23. same-project version succession alone proves direct conceptual continuity;
24. the published OSDI architecture and every repository revision were perfectly synchronized;
25. the bridge is an evolutionary narrative in which one mechanism inevitably improves into the next.

---

# Claim ledger

| Claim | Type | Evidence strength | Boundary |
|---|---|---:|---|
| August-2005 Ceph source uses `RG` / `repgroup_t` and explicitly calls the group a Replica Group | H | strong primary source | exact inspected revision only |
| August-2005 `OSDMap` includes `rush.h`, stores RUSH disk groups, and calls `Rush::GetServersByKey` for replica-group placement | H | strong primary source | exact inspected revision only |
| August-2005 map/authority change can invalidate `PEERED` knowledge without first erasing local payload | H | strong primary source, already deepened separately | unfinished implementation |
| OSDI 2006 presents object→PG→CRUSH→ordered OSD placement and map-triggered peering/recovery | H | strong peer-reviewed primary source | published architecture, not every code revision |
| 2006-12-06 source contains a CRUSH-backed PG mapping path in `OSDMap` | H | strong primary source | observed endpoint, not first introduction |
| The same December source contains `PG::Info`, versioned log, history, and `PG::Missing` structures | H | strong primary source | observed endpoint, not first introduction |
| The inspected endpoints materially differ in vocabulary and recovery metadata structure | E/H | strong bounded comparison | does not reconstruct every intermediate revision |
| The retention problem of requalifying replica currentness after membership/placement change is recognizable at both endpoints | E | strong controlled reconstruction | functional continuity, not algorithm identity |
| `same retention problem != same state machine != proven genealogy` | E | project synthesis | depends on bounded evidence above |

---

# Related repositories and reuse boundary

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `RUSH CRUSH Ceph` found no dedicated packet to reuse.

This repository therefore keeps only the retention-specific bridge:

```text
placement/membership context changes
    -> old replica-currentness evidence can become insufficient
    -> currentness must be reconstructed
```

The following belong primarily in `computing-archaeology` if pursued:

- the full RUSH→CRUSH algorithm genealogy;
- exact commit-by-commit transition from `repgroup_t/RG` to `pg_t/PG`;
- first introduction / naming chronology for `placement group`;
- CRUSH bucket/algorithm evolution;
- benchmark/performance motivation for replacing earlier placement machinery;
- developer correspondence / mailing-list design discussion;
- production deployment chronology.

`technical-retention` should link that future work rather than duplicating it.

---

# Remaining evidence debt

This bounded bridge closes the canonical debt **at the level needed for Case 05**: there is now a source-backed predecessor endpoint, a peer-reviewed 2006 architecture, and a late-2006 implementation endpoint, with anti-genealogy boundaries explicit.

Further work is optional and belongs mainly to broader source archaeology:

1. identify the earliest source revision containing `PG` / `pg_t` without treating first surviving Git evidence as invention priority;
2. identify the earliest source revision selecting `PG_LAYOUT_CRUSH`;
3. inspect intermediate design notes or mailing-list discussion if a true RUSH→CRUSH genealogy is needed;
4. test one historically buildable revision only if that would answer a new retention question rather than merely reenact placement.

None of those is a maturity blocker for the grounded Case 05.

---

# Primary sources

- Ceph historical commit `88086b83b7dcb0eb5c092e30fde8570475173f5e`, 2005-08-06, `lots of OSD peering stuff (still not complete)`: <https://github.com/ceph/ceph/commit/88086b83b7dcb0eb5c092e30fde8570475173f5e>
- `ceph/osd/OSD.h` at `88086b83...`: <https://github.com/ceph/ceph/blob/88086b83b7dcb0eb5c092e30fde8570475173f5e/ceph/osd/OSD.h>
- `ceph/osd/OSDMap.h` at `88086b83...`: <https://github.com/ceph/ceph/blob/88086b83b7dcb0eb5c092e30fde8570475173f5e/ceph/osd/OSDMap.h>
- Sage A. Weil et al., “Ceph: A Scalable, High-Performance Distributed File System,” OSDI 2006, §§5.1–5.5: <https://www.usenix.org/legacy/events/osdi06/tech/full_papers/weil/weil_html/>
- Ceph historical commit `283b68e12a9847ca7ea7adb16d9a9b45af138ef3`, 2006-12-06, `improved support for forcing the first element of a crush result`: <https://github.com/ceph/ceph/commit/283b68e12a9847ca7ea7adb16d9a9b45af138ef3>
- `ceph/osd/PG.h` at `283b68e...`: <https://github.com/ceph/ceph/blob/283b68e12a9847ca7ea7adb16d9a9b45af138ef3/ceph/osd/PG.h>
- `ceph/osd/OSDMap.h` at `283b68e...`: <https://github.com/ceph/ceph/blob/283b68e12a9847ca7ea7adb16d9a9b45af138ef3/ceph/osd/OSDMap.h>
