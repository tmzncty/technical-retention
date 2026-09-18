# Case 05 evidence deepening — Ceph 2007 OSDMap persistence and restart selection

**Status:** bounded deepening complete

**Case:** [`cases/05-rados-replicated-object-repair.md`](../cases/05-rados-replicated-object-repair.md)

**Bounded question:** In the 2007 Ceph implementation surrounding the RADOS research system, what placement/currentness control state was actually retained on an OSD, and how was that retained state used after restart?

This note closes one narrow evidence debt in Case 05. It does **not** attempt a general history of Ceph OSDMap persistence, monitor consensus, CRUSH evolution, BlueStore, modern peering, or later `up`/`acting` semantics.

---

## 1. Why this slice matters

Case 05 already establishes two different distributed-retention problems:

1. the system must know **where a PG/object ought to be placed under the current cluster state**;
2. it must separately know **which surviving replica history/content is current enough to serve and repair**.

The 2006 CRUSH deepening showed that deterministic placement still depends on a current cluster-map/epoch context. The remaining question was more concrete:

> Was that map context merely transient runtime knowledge, or did an early OSD retain enough map/control state locally to restart with a historically meaningful placement context?

A September 2007 Ceph source snapshot gives a direct answer.

At that snapshot, the OSD stores:

- an `OSDSuperblock` containing `current_epoch`, `oldest_map`, and `newest_map`;
- full OSDMap objects keyed by epoch;
- incremental OSDMap objects keyed by epoch;
- per-PG `info` attributes;
- on-disk PG logs.

On restart, it mounts the local object store, reads the superblock, loads the full OSDMap selected by the persisted `current_epoch`, reloads PG metadata/logs, recomputes each PG's acting set/role under that map, and then boots back into the distributed protocol.

That makes the local OSDMap archive part of the bounded restart apparatus rather than merely a cache incidental to one process lifetime.

---

## 2. Source custody and chronology

### Primary implementation snapshot

Ceph public Git history preserves the earlier SourceForge SVN history. This note uses commit:

- `c93efe01c518c2e90ba62245352baaac5fa675f2`
- date: **2007-09-05**
- mirrored SVN revision: `@1787`
- commit message: **“stupid hack to pull osdmaps out of an osd store”**

Commit:

<https://github.com/ceph/ceph/commit/c93efe01c518c2e90ba62245352baaac5fa675f2>

Relevant files at that exact revision:

- `trunk/ceph/osd/OSD.cc`
  - <https://github.com/ceph/ceph/blob/c93efe01c518c2e90ba62245352baaac5fa675f2/trunk/ceph/osd/OSD.cc>
- `trunk/ceph/osd/OSD.h`
  - <https://github.com/ceph/ceph/blob/c93efe01c518c2e90ba62245352baaac5fa675f2/trunk/ceph/osd/OSD.h>
- `trunk/ceph/osd/osd_types.h`
  - <https://github.com/ceph/ceph/blob/c93efe01c518c2e90ba62245352baaac5fa675f2/trunk/ceph/osd/osd_types.h>
- `trunk/ceph/extractosdmaps.cc`
  - introduced by the same commit and visible in the commit diff above.

### Earlier direct PG-log witness

For a narrower supporting point about on-disk PG logs, this note also uses:

- `a32d6d32c1a92d3bc45399e235a7e80edd551fdd`
- date: **2007-02-26**
- mirrored SVN revision: `@1129`
- commit message: **“fixed pg log storage (and the stupid recovery problems); fakestore cleanup”**

<https://github.com/ceph/ceph/commit/a32d6d32c1a92d3bc45399e235a7e80edd551fdd>

The September snapshot is the main source. The February commit is used only to corroborate that PG-log persistence was already an explicit implementation concern in 2007.

### Chronological caution

The September 2007 tree is later than the November 2006 OSDI paper and sits around the mature 2007 RADOS research period. It is therefore appropriate as an **immediately surrounding implementation record**, but it must not be projected backwards as proof that every detail already existed in the exact OSDI paper implementation.

Likewise, nothing here is a claim about modern Ceph.

---

## 3. Historical record — the superblock retained an epoch selection state

At this revision, `OSDSuperblock` is a small explicit on-store control structure. Its fields include:

```text
magic
fsid
whoami
current_epoch
oldest_map
newest_map
```

The source comments describe:

- `current_epoch` as the most recent epoch;
- `oldest_map` / `newest_map` as the oldest and newest maps the OSD has.

The OSD writes this structure into a dedicated `SUPERBLOCK_OBJECT` and reads it back during startup.

### Historical claim

**The 2007 OSD retained not only payload/PG state but also an epoch-indexed statement about which cluster-map state it had reached and what map range it held locally.**

That is stronger than saying “the OSD had a map in RAM.”

It is also weaker than saying “the superblock was the final authority for cluster membership.” The monitor protocol remains present and newer epochs can supersede the locally selected map.

---

## 4. Historical record — full and incremental maps were local ObjectStore objects

`OSD.h` exposes two epoch-derived object names:

```text
get_osdmap_object_name(epoch)
get_inc_osdmap_object_name(epoch)
```

In the September source, `handle_osd_map()` receives full and/or incremental maps and writes them into the OSD's local `ObjectStore` if that epoch is not already present.

For a full map, the code obtains the epoch-derived full-map object name and writes the supplied bytes. For an incremental map, it does the same with the incremental-map object name.

While accepting those maps, it updates the in-memory `superblock.newest_map` and `superblock.oldest_map` boundaries.

### Independent same-snapshot witness

The commit itself introduces `extractosdmaps.cc`, a small utility that:

1. mounts `dev/osd0` using `Ebofs`;
2. begins at epoch 1;
3. reads the full-map object for each epoch using `OSD::get_osdmap_object_name(e)`;
4. reads the corresponding incremental map object;
5. copies those byte strings into a `MonitorStore` as `osdmap_full` and `osdmap` records.

The utility only works because those epoch-indexed OSDMap byte strings are materially present in the OSD store.

### Historical claim

**By September 2007, full and incremental OSDMaps were explicitly materialized as retrievable objects in the OSD's local store.**

This is direct implementation evidence for retained placement/control history, not only a paper-level architecture statement.

---

## 5. Historical record — restart selected a locally persisted current map

The non-`mkfs` startup path in `OSD::init()` performs this order:

```text
mount local store
    ↓
read_superblock()
    ↓
load_pgs()
    ↓
assert local OSD identity
    ↓
initialize runtime services
    ↓
send MOSDBoot(..., superblock) to a monitor
```

Inside `read_superblock()` the code:

1. reads `SUPERBLOCK_OBJECT` from the local store;
2. copies it into the in-memory `superblock` structure;
3. allocates a fresh `OSDMap`;
4. fetches the locally stored full-map bytes for `superblock.current_epoch`;
5. decodes those bytes into the runtime `osdmap`.

The restart path therefore does **not** begin from an empty placement relation and wait for a monitor before it can even interpret local PG placement state.

### Historical claim

**The persisted `current_epoch` selected a persisted full OSDMap that was decoded as the restart-time runtime map before PGs were reloaded.**

### Important limit

This does **not** mean the locally selected map is guaranteed to be the cluster's newest map after an outage.

The same implementation still boots to a monitor, exchanges map state, and can request missing epochs.

---

## 6. Historical record — PG metadata/logs were reinterpreted under the loaded map

After `read_superblock()`, startup calls `load_pgs()`.

For each stored collection / PG, the code:

- constructs the in-memory PG object;
- reads the collection attribute named `info` into `pg->info`;
- calls `pg->read_log(store)`;
- calls `osdmap->pg_to_acting_osds(...)` to derive the acting set;
- calls `osdmap->calc_pg_role(...)` to derive the local OSD's role.

The February 2007 commit `a32d6d32...` directly modifies `PG::write_log()`, `PG::append_log()`, and `PG::read_log()` and describes itself as fixing “pg log storage”. It records log bounds as collection attributes and reads log records from the PG's object in the local store.

### Historical claim

**Restart brought together at least three retained classes of state:**

```text
cluster-map / epoch state
PG information + history
PG update log
```

The running PG role was then derived from retained PG identity/history plus the selected OSDMap.

This is a useful source-level confirmation of a distinction already present in the 2007 research description:

```text
payload / PG content
    != PG history/log state
    != placement-map state
```

---

## 7. Historical record — locally retained map history could be replayed

`handle_osd_map()` advances from `superblock.current_epoch` toward `superblock.newest_map`.

For each next epoch, it can use either:

- an incremental map included in the incoming message; or
- a locally stored incremental map already present in the ObjectStore.

When applying an incremental, it updates the in-memory OSDMap and then writes an encoded full map for the resulting epoch into the transaction.

If no usable incremental/full map exists for the next epoch, it asks a monitor for that missing epoch with `MOSDGetMap(cur+1)` and stops advancing until the gap is filled.

The source also contains `get_map(epoch, OSDMap&)`, which searches backward for a complete map and then applies later incremental maps to reconstruct the requested historical epoch.

`project_pg_history()` uses these historical maps while walking backward across epochs to determine when a PG acting set, primary, or acker changed.

### Historical claim

**The locally retained map archive was not only a latest-state cache. It was also used to reconstruct prior map states needed for PG-history reasoning.**

This is a history-retention function inside an operational storage protocol.

It is still a bounded history: the source tracks `oldest_map` and `newest_map`; nothing here implies indefinite archival preservation of every epoch.

---

## 8. Historical record — advancement and local admission were separately represented

During map handling, after successfully applying the next epoch, the source increments `cur` and assigns:

```text
superblock.current_epoch = cur
```

Only after advancing through the available maps and updating PG state does it call:

```text
write_superblock(t)
store->apply_transaction(t)
```

The same transaction also writes updated PG `info` attributes.

The source therefore gives the local OSD an explicit persisted marker for the map epoch it has processed, rather than inferring currentness merely from whichever map blob happens to exist in the store.

### Historical claim

**Map-byte presence and processed/current epoch were represented separately.**

The implementation's own structure therefore blocks this shortcut:

```text
OSDMap object exists locally
    == OSD has necessarily admitted that epoch as its current processed state
```

That equality is false at the representation level even before asking detailed crash-consistency questions.

---

## 9. Engineering reconstruction — map retention supports restart without becoming cluster authority

The source supports the following bounded engineering reconstruction:

```text
persisted superblock epoch selector
+ locally persisted full/incremental OSDMaps
+ persisted PG info/logs
    ↓
restart can reconstruct a coherent local placement/history context
    ↓
local PG roles/acting sets can be derived
    ↓
OSD rejoins monitor/map exchange
    ↓
newer/missing epochs can revise that context
    ↓
peering can establish replica-content currentness
```

This gives two different notions of “current map” that should not be collapsed:

1. **restart-selected local currentness** — the map selected by the persisted `superblock.current_epoch`;
2. **cluster-current map state** — the sufficiently new map state learned through the live distributed protocol.

The first is retained locally.

The second can supersede it.

So:

```text
restart-legible placement state
    != globally newest placement state
```

and:

```text
locally selected current map
    != PG peering complete
    != replica content current
    != desired redundancy restored
```

---

## 10. Engineering reconstruction — persisted resolver history is part of object retention

Case 05 asks what must survive if physical replicas are replaceable.

This source adds a concrete answer: some retained state is not object payload at all. It is **resolver/history state that lets the system determine what the payload's placement relation meant across map epochs and restart**.

A useful decomposition is:

```text
object payload bytes
    ↓ not sufficient by themselves
PG identity / local metadata
    ↓
PG log / version history
    ↓
OSDMap epoch history
    ↓
superblock epoch selection state
    ↓
live monitor/map exchange
    ↓
peering / repair
```

The layers are not interchangeable.

Losing one replica's payload can be repaired if enough authoritative distributed state survives.

Conversely, raw local bytes plus stale or uninterpretable placement/currentness state do not automatically define the object's current distributed meaning.

---

## 11. Engineering reconstruction — physical presence, local admission, and distributed admissibility differ

The September code writes incoming map objects before the later transaction that persists the updated superblock and PG state. The source comment explicitly notes that the map is stored “outside” the transaction because `activate_map` reads it.

That ordering is analytically useful, but it must be handled carefully.

What can safely be said from the code structure is:

```text
map blob presence
    != superblock.current_epoch selection
```

What **cannot** be claimed from this slice alone is an exact power-failure outcome for every point between those calls. To do that responsibly would require the contemporaneous ObjectStore/EBOFS durability, writeback, ordering, and transaction semantics.

So this note deliberately does **not** claim:

- that a map write was durable immediately on return;
- that the superblock transaction was atomic with all relevant earlier writes;
- that a crash at a particular source line yields a specific recoverable state;
- that every stored map beyond `current_epoch` necessarily survives or is ignored after every failure.

The narrower source-backed boundary is enough:

> the design represented stored map bytes and processed/current epoch as different retained state.

---

## 12. Engineering reconstruction — restart is not instant service admission

The startup path loads a map and PGs locally, but it does not then declare all PGs immediately active merely because the disk mounted successfully.

The map activation path scans PGs. For an inactive primary it builds prior information and enters `peer(...)`; strays/replicas notify the current primary. The OSD also announces its boot to a monitor.

That supports another bounded distinction:

```text
local restart succeeded
    != distributed currentness reconstructed
    != PG admitted for ordinary service
```

The stored map makes restart **legible**; peering and later map exchange make the restarted OSD **admissible in the distributed system**.

---

## 13. Functional analogy — TrueFFS restart reconstruction, carefully bounded

A useful functional comparison exists with Case 04's TrueFFS mapping-reconstruction evidence.

### TrueFFS bounded function

```text
volatile runtime map disappears
+ Flash-resident mapping/currentness evidence survives
+ reconstruction procedure survives
    ↓
new usable runtime logical→physical resolution relation
```

### 2007 RADOS bounded function

```text
process-local runtime OSDMap/PG objects disappear
+ superblock/map archive/PG metadata survive locally
+ distributed map/peering protocol survives
    ↓
restart-time local placement relation is re-established
    ↓
then revised/admitted against live cluster state
```

The analogy is only functional:

> **both systems retain evidence from which a usable resolver/currentness relation can be re-established after runtime state disappears.**

The mechanisms are historically and technically different.

TrueFFS is a managed Flash mapping system within one storage device/software stack. RADOS is a distributed object store in which live monitor/map exchange and peer histories can supersede one node's retained local view.

No genealogy is claimed.

---

## 14. Functional comparison — deterministic placement still needs retained context

CRUSH can deterministically compute placement from an identifier, cluster description, and rule.

This 2007 implementation shows why `deterministic` must not be misread as `stateless`.

A restarted OSD still retains:

- which epoch it had processed;
- which map epochs it holds;
- the serialized map state itself;
- PG histories/logs that must be interpreted against those epochs.

Therefore:

```text
deterministic placement algorithm
    != no retained placement context
```

The algorithm can eliminate a conventional per-object location table while still depending on retained **cluster-state history**.

---

## 15. Philosophical interpretation — retention can preserve a relation, not only a thing

**Philosophical interpretation, not historical vocabulary.**

The case makes one narrow philosophical point available without turning Ceph into a metaphor.

A retained object can depend on preserving not only embodiments of its bytes but also **relations that make those embodiments addressable, current, and recoverable**.

Here the past that matters operationally includes:

- which map epoch had been processed;
- enough map history to reconstruct placement changes;
- enough PG history to know prior participation and expected state;
- enough live protocol to revise a restarted node's local view.

The physical replicas are replaceable, but the system cannot simply forget every relation that once made them participants in one logical object.

The careful formulation is therefore:

> distributed retention may require retention or reconstruction of **the conditions under which surviving embodiments count**.

This is not a claim that OSDMap epochs are “memory” in a universal philosophical sense, nor that every retained relation is equivalent to cultural or human memory.

---

## 16. Explicit non-claims

This deepening does **not** establish any of the following:

1. that the September 2007 implementation is byte-for-byte the November 2006 OSDI implementation;
2. that the design shown here was the first Ceph implementation to persist OSDMaps;
3. that every OSDMap epoch was retained indefinitely;
4. that `oldest_map` / `newest_map` had every semantic later Ceph versions gave similarly named fields;
5. that a locally stored map was globally authoritative;
6. that restart could proceed correctly forever without monitors;
7. that decoding the local `current_epoch` map made every PG immediately active;
8. that placement currentness and replica-content currentness were the same state;
9. that a map blob's physical presence meant its epoch had been admitted as `current_epoch`;
10. that the out-of-transaction map write had any specific crash-durability guarantee not established here;
11. that superblock and map writes were power-fail atomic as a unit;
12. that PG-log persistence alone guaranteed recoverability;
13. that retained map history alone guaranteed recoverability;
14. that the local map archive was a substitute for peering;
15. that the local map archive was a substitute for payload redundancy;
16. that `extractosdmaps.cc` was production recovery tooling rather than the hack its own commit message calls it;
17. that the 2007 OSD superblock layout is representative of modern Ceph;
18. that later map trimming, map gaps, BlueStore, `up`/`acting`, backfill, or modern peering semantics can be projected backward into this snapshot;
19. that TrueFFS influenced Ceph or Ceph influenced TrueFFS;
20. that all distributed systems need this exact form of persisted placement history.

---

## 17. Claim ledger

| Claim | Type | Evidence strength | Boundary |
|---|---|---:|---|
| September 2007 OSD superblock records `current_epoch`, `oldest_map`, `newest_map` | Historical record | direct source | exact snapshot only |
| Full and incremental OSDMaps are stored as epoch-keyed local ObjectStore objects | Historical record | direct source + extractor utility | exact snapshot only |
| Restart reads superblock then decodes locally stored full map at `current_epoch` | Historical record | direct source | exact snapshot only |
| Restart reloads PG `info` and PG log, then derives acting set/role from loaded map | Historical record | direct source | exact snapshot only |
| Locally stored incremental maps can be replayed to advance map epochs | Historical record | direct source | exact snapshot only |
| Historical map states can be reconstructed for PG-history projection | Historical record | direct source | exact snapshot only |
| Missing next map epoch triggers monitor request | Historical record | direct source | exact snapshot only |
| Map blob presence and processed/current-epoch state are represented separately | Engineering reconstruction from direct source structure | strong | no exact crash outcome implied |
| Local map persistence makes restart placement/history context legible but not globally authoritative | Engineering reconstruction | strong | requires live protocol for cluster currentness |
| Resolver/history state is constitutive of distributed object recoverability | Engineering reconstruction | strong within Case 05 | not payload-equivalent |
| TrueFFS and RADOS both re-establish runtime resolution relations from retained evidence | Functional analogy | bounded | no genealogy/equivalence |
| Retention may preserve conditions under which embodiments count | Philosophical interpretation | bounded | not period vocabulary |

---

## 18. What this closes in Case 05

This closes the narrow evidence debt:

> inspect historically appropriate source for exact cluster-map serialization/persistence and OSD restart behavior.

The closure is deliberately scoped to the **September 2007 implementation snapshot**.

What is now directly established is:

```text
serialized full/incremental maps persisted locally
+ persisted epoch-selection/range state in OSDSuperblock
+ persisted PG metadata/logs
    ↓
restart reconstructs a local map + PG context
    ↓
monitor/map exchange can supply newer or missing epochs
    ↓
peering separately reconstructs replica-content currentness
```

This is enough to reject both of these oversimplifications:

```text
CRUSH is deterministic, therefore placement needs no retained state
```

and:

```text
OSD has a map on disk, therefore its distributed object state is current
```

---

## 19. Remaining evidence debt

The following work remains genuinely open and should not be smuggled into this slice:

1. **Earlier introduction chronology** — identify when epoch-indexed full/incremental OSDMap persistence and the relevant superblock fields first entered the source tree.
2. **2005 → 2007 bridge** — trace the RG/RUSH-era peering prototype into the CRUSH/PG architecture without assuming continuity merely from shared names/authorship.
3. **ObjectStore/EBOFS crash semantics** — inspect contemporaneous write, transaction, sync, journal, and recovery semantics before making source-line-level power-failure claims about map versus superblock ordering.
4. **Monitor-side persistence** — inspect the contemporaneous monitor store, map proposal/update path, and monitor restart/quorum behavior as a separate control-plane retention problem.
5. **Map trimming policy** — establish how/when old map epochs could be discarded in this period and what minimum history had to remain available.
6. **Paper/source alignment** — identify the precise source revision corresponding most closely to the 2006 OSDI paper and 2007 RADOS paper/dissertation descriptions.
7. **Later semantics** — keep later `up`/`acting`, backfill, map-gap, BlueStore, and modern peering archaeology out of this bounded historical claim until separately researched.

---

## 20. Related-repository boundary

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `RADOS` and `CRUSH` found no dedicated packet to reuse.

This repository therefore keeps only the retention-specific seam:

```text
persisted map bytes
    ↓
persisted epoch selection/range
    ↓
restart-time local placement context
    ↓
newer/missing map reconciliation
    ↓
PG peering/content-currentness qualification
    ↓
repair / renewed redundancy
```

The broader work belongs in `computing-archaeology`:

- RUSH → CRUSH algorithm genealogy;
- early Ceph source-tree evolution;
- monitor architecture/history;
- EBOFS/ObjectStore implementation archaeology;
- production deployment history;
- map-trimming evolution;
- later `up`/`acting`, backfill, BlueStore, and modern OSD restart semantics.

---

## 21. One-sentence retention result

> **In the September 2007 Ceph implementation, an OSD restart did not recover placement meaning from payload bytes alone: it reloaded a persisted epoch selector, serialized OSDMap history, and PG metadata/logs to re-establish a local placement/history context, then relied on the live distributed protocol to revise that context and separately establish replica-content currentness.**
