# RADOS 2006–2007 grounding record

This companion evidence record deepens [`cases/05-rados-replicated-object-repair.md`](../cases/05-rados-replicated-object-repair.md). It is deliberately narrow: it verifies the case's central retention claims against exact primary-source locations, distinguishes the 2006 OSDI prototype description from the 2007 RADOS presentation, and adds a contemporaneous implementation artifact.

**Canonical maturity status is tracked in [`CASE_INDEX.md`](../CASE_INDEX.md).** This record supersedes the older `first-pass` evidence note at the end of the case document without rewriting the case into a general history of Ceph.

## Grounding question

The case argues that a RADOS object can remain logically current while:

- physical replica membership changes;
- one replica becomes stale or disappears;
- primary authority moves;
- a new replica is reconstructed elsewhere;
- an acknowledged update and a durably committed update occupy different retention thresholds.

The grounding task is therefore not `prove that Ceph replicated data`. It is to establish the exact mechanisms that make **currentness, authority, replacement, and commit state** recoverable.

---

## Source A — Ceph OSDI '06: exact anchors

Sage A. Weil, Scott A. Brandt, Ethan L. Miller, Darrell D. E. Long, and Carlos Maltzahn, “Ceph: A Scalable, High-Performance Distributed File System,” *OSDI '06*, USENIX, pp. 307–320.

Primary PDF:
https://usenix.org/event/osdi06/tech/full_papers/weil/weil.pdf

### A1. Object → PG → ordered OSD placement

**Printed p. 312, §5.1, Figure 3.**

The paper states that Ceph first maps objects into placement groups and then uses CRUSH to map each PG to an **ordered list of OSDs** holding replicas. It also states that object location can be independently calculated from the placement group plus the OSD cluster map, rather than recovered from a per-object allocation list.

This grounds two claims in Case 05:

- object identity is separated from one permanently stored physical-location record;
- the current cluster map is part of the relation needed to recover physical embodiments.

### A2. Failure domains are part of placement semantics

**Printed p. 312, §5.1.**

The same page describes a hierarchical cluster map aligned with physical/logical failure sources and gives the concrete example of placing replicas in separate cabinets to reduce exposure to a shared power circuit or edge-switch failure.

This grounds the case's claim that replica count alone is insufficient: **independence of failure domains is part of retention engineering**.

### A3. Primary-copy replication and version assignment

**Printed p. 312, §5.2.**

RADOS is described as using a variant of primary-copy replication. A PG maps to an ordered list of `n` OSDs; writes go to the first non-failed OSD, the primary; the primary assigns a new version number for the object and PG and forwards the update to replicas.

This grounds the narrow use of `primary`, `replica`, and `version` in the case. It also bounds the phrase `no privileged copy`: the design has temporary protocol authority even though no physical device is the object's permanent home.

### A4. Ack and durable commit are distinct retention thresholds

**Printed p. 313, Figure 4 and §5.3 “Data Safety.”**

Figure 4 and the surrounding text distinguish:

1. an `ack` after the update has reached the in-memory buffer caches of all OSDs replicating the object;
2. a later final `commit` after the update has safely reached disk.

The text explicitly separates rapid visibility/synchronization from knowing that the update is safely replicated on disk and can survive power or other failures. Clients also retain writes until final commit so acknowledged ordered updates can be replayed after simultaneous power loss affecting the PG.

This is primary evidence for the case distinction:

> **logical success / visibility ≠ durable commit.**

It should not be generalized to modern Ceph without version-specific evidence.

### A5. `down` / `out` and repair-triggered membership change

**Printed p. 313, §5.4 “Failure Detection.”**

An unresponsive OSD is first marked `down`, with primary responsibilities temporarily passing to the next OSD in the PG. If it does not recover quickly, it is marked `out`, another OSD joins each affected PG, and contents are re-replicated.

This grounds **failure/repair-triggered maintenance** as a distinct retention regime.

### A6. Peering determines current PG contents before normal I/O

**Printed pp. 313–314, §5.5 “Recovery and Cluster Updates.”**

OSDs maintain an object version and a log of recent changes for each PG. After membership changes, PG members peer; the primary obtains PG versions and, where necessary, recent logs or a complete content summary to determine the correct most-recent PG contents. Only after the primary has determined and shared what the PG should contain is ordinary I/O permitted; missing or outdated objects are then recovered.

The continuation on printed p. 314 gives a concrete failure/recovery example in which a former primary returns, discovers from the new map that it is no longer primary, exchanges PG log/version information with the new primary, and resumes service while outdated objects are recovered in the background.

This is the strongest primary support for:

> **replica multiplicity ≠ retained currentness.**

Physical bytes can survive while protocol currentness has to be reconstructed from version, log, membership, and authority state.

---

## Source B — CRUSH SC '06: exact mechanism boundary

Sage A. Weil, Scott A. Brandt, Ethan L. Miller, and Carlos Maltzahn, “CRUSH: Controlled, Scalable, Decentralized Placement of Replicated Data,” *SC 2006*.

Project-hosted PDF:
https://ceph.io/assets/pdfs/weil-crush-sc06.pdf

### B1. Placement is a deterministic relation, not a per-object directory

**PDF pp. 1–2 of 12, Introduction and §3.**

CRUSH is defined as a deterministic pseudo-random function mapping an object/object-group identifier to an ordered list of storage targets. The required state is a compact hierarchical cluster description plus placement policy, not a per-object location directory.

This supports Case 05's engineering reconstruction that `where the object is` can be a **recalculable relation** rather than a permanently retained location field.

### B2. Physical topology is deliberately encoded into replica placement

**PDF pp. 2–3 of 12, §3 and §3.2 “Replica Placement.”**

The paper models devices inside shelves, cabinets, rows, rooms, power supplies, controllers, networks, and other failure domains. Placement rules may explicitly separate replicas across those domains. A concrete example places three mirrored replicas in different physical cabinets so they do not share an electrical circuit.

This is stronger than a generic claim that `three copies are safer than one`: it grounds the case's claim that **correlated-failure topology changes the meaning of redundancy**.

### B3. Do not merge CRUSH with the replication protocol

CRUSH establishes *where replicas should be placed*. It does not by itself establish which disagreeing replica is current, how writes are ordered, or how peering recovers PG contents. Those semantics belong to RADOS replication/recovery and must remain separate in the repository.

---

## Source C — RADOS PDSW '07: what changed or became explicit

Sage A. Weil, Andrew W. Leung, Scott A. Brandt, and Carlos Maltzahn, “RADOS: A Scalable, Reliable Storage Service for Petabyte-scale Storage Clusters,” *PDSW '07*, pp. 35–44, November 2007.

Archived publication record:
https://www.ssrc.us/pub/weil-pdsw07.html

Accessible paper mirror used for direct inspection:
https://code.garrettmills.dev/Archives/papers-we-love_papers-we-love/raw/commit/8ac9250746600bb98cc202961097c6487cd902ec/datastores/rados-a-scalable-reliable-storage-service-for-petabyte-scale-storage-clusters.pdf

The SSRC publication record establishes title, authors, venue, and November 2007 publication date. The paper itself is primary evidence for the later bounded design.

### C1. RADOS is presented as a storage service in its own right

**Printed pp. 35–36 / PDF pp. 1–2.**

The 2007 paper presents RADOS directly as a reliable object storage service and says clients see a single logical object store. It makes the **versioned cluster map** central to consistent data distribution and read/write access.

This is a scope change from the 2006 OSDI paper, where RADOS is presented inside the broader Ceph file-system architecture. It is not evidence that the underlying retention problem suddenly appeared in 2007.

### C2. Replication strategy is no longer only primary-copy in the presentation

**Printed p. 38 / PDF p. 4, §3.1 and Figure 2.**

The 2007 paper documents three implemented replication schemes:

- primary-copy;
- chain replication;
- `splay` replication.

Primary-copy serves reads/writes at the primary and updates replicas in parallel. Chain writes serially and serves reads from the tail. Splay combines parallel update behavior with tail reads.

Therefore the 2006 case's statement `reads go to the primary` must remain explicitly bounded to the 2006 primary-copy path. It is not a timeless property of RADOS.

### C3. Map-epoch consistency and stale-read exclusion are made much more explicit

**Printed p. 38 / PDF p. 4, §3.2 “Strong Consistency.”**

All RADOS messages are tagged with the sender's map epoch. If membership changes, newly responsible OSDs must contact prior non-failed members to determine correct PG contents before becoming active. The paper also describes a heartbeat-based rule that blocks reads when the read-serving OSD has not heard from peer replicas within the configured interval, preventing an old read authority from serving stale data after another OSD takes over.

This sharpens the case's concept of `currentness`: **readability is protocol-authorized freshness, not mere physical reachability**.

### C4. Peering is generalized across arbitrary distribution changes

**Printed pp. 38–39 / PDF pp. 4–5, §3.4 and §3.4.1.**

The 2007 paper explicitly says device failure is only one instance of a more general problem: establishing a new distribution after failures, recoveries, expansion, contraction, or a new CRUSH policy. RADOS makes no continuity assumption between one map and the next.

Peering examines **all intervening map epochs**, not only the newest map, so an OSD that left and later rejoined a PG cannot silently ignore updates that occurred while it was absent. The primary builds a `prior set`, obtains PG log fragments or full PG content information where necessary, shares missing log fragments with replicas, and only then activates I/O/recovery state.

This significantly strengthens the retention interpretation:

> logical continuity is reconstructed across discontinuous physical membership by retaining enough history of membership and object versions.

### C5. PG metadata is deliberately guarded even while object safety is degraded

**Printed pp. 38–39 / PDF pp. 4–5.**

The 2007 paper says OSDs aggressively replicate the PG log and its record of what the current PG contents *should be*, even when some object replicas are locally missing. It explicitly notes that recovery may be slow and object safety degraded while PG metadata is carefully guarded.

This is direct historical evidence for a claim that was only implicit in the first-pass case:

> **retention of the relation that identifies current state can be prioritized separately from retention of every material replica.**

---

## Source D — Weil 2007 dissertation: do not misread the workshop paper's abbreviated ack figure

Sage A. Weil, *Ceph: Reliable, Scalable, and High-Performance Distributed Storage*, PhD dissertation, University of California, Santa Cruz, 2007.

PDF:
https://www.ceph.com/assets/pdfs/weil-thesis.pdf

Relevant location: Chapter 6, especially §6.3.1–§6.3.5; dissertation pp. 130–142. Figure 6.4 and §6.3.2 are on dissertation pp. 131–132.

### D1. The two-threshold ack/commit model still exists in the 2007 technical account

**Dissertation pp. 131–132, Figure 6.4 and §6.3.2 “Serialization versus Safety.”**

The dissertation keeps the same fundamental distinction as OSDI '06 while applying it to the expanded replication schemes:

- replica OSDs acknowledge after applying an update to the in-memory EBOFS cache;
- the client receives `ack` after the required replicas have applied it;
- EBOFS later reports safe on-disk commit;
- only after all required replicas report safe commit does the client receive the final `commit`.

The dissertation explicitly says RADOS disassociates write acknowledgement from safety and that clients buffer updates until final commit so they can participate in recovery if all OSDs holding uncommitted volatile state fail.

### D2. Documentary caution

The PDSW '07 replication section compresses the message flow into a single acknowledgement after replicas are updated. That shorter workshop presentation must **not** be interpreted as evidence that durable commit semantics disappeared. The contemporaneous dissertation documents the ack/commit distinction in detail.

This is a useful historiographic warning for the repository:

> **absence of a mechanism from a shorter paper is not evidence that the mechanism was absent from the system.**

---

## Source E — contemporaneous implementation artifact

Ceph repository commit:

`a32d6d32c1a92d3bc45399e235a7e80edd551fdd`

Commit date: **2007-02-26**

Commit message:

> `fixed pg log storage (and the stupid recovery problems); fakestore cleanup`

Canonical commit:
https://github.com/ceph/ceph/commit/a32d6d32c1a92d3bc45399e235a7e80edd551fdd

The diff includes concrete `PG::write_log`, `PG::append_log`, and `PG::read_log` paths, persists PG log bounds as collection attributes, writes log entries to the object store, and reconstructs the in-memory PG log from the on-disk log.

This artifact is valuable for a narrow reason: it demonstrates that **PG log retention and recovery were implementation concerns in the contemporaneous codebase**, not vocabulary invented retrospectively from the papers.

It is not sufficient by itself to prove every 2007 paper semantic, and the commit message itself says it fixes recovery problems. The code should therefore be treated as implementation evidence, not as proof that the system was already production-stable.

---

## 2006 → 2007 semantic ledger

| Topic | OSDI '06 bounded description | PDSW/dissertation '07 bounded description | Retention consequence |
| --- | --- | --- | --- |
| Replication strategy | primary-copy variant | primary-copy + chain + splay | read authority and update path are protocol-specific, not timeless RADOS properties |
| Placement/current membership | cluster map + epoch; `down`/`out` | versioned cluster map; explicit `up/down` and `in/out`; generalized map transitions | object identity survives changes in the correct replica set |
| Read currentness | reads at primary in bounded path | role varies by scheme; heartbeat rule excludes stale read authority | physically readable replica ≠ authorized current read source |
| Recovery | PG versions/logs/content summary; peering before I/O | all intervening epochs; prior-set discovery; aggressively replicated PG logs; background recovery | currentness depends on retained relation/history, not bytes alone |
| Safety threshold | in-memory replicated `ack` then on-disk `commit` | dissertation retains ack/commit split across replication schemes | visible/ordered/replicated/durable remain distinct thresholds |
| Failure as trigger | OSD failure drives `down`/`out` and re-replication | failure is one case of generalized redistribution after any map change | repair-triggered retention generalizes to membership/topology migration |
| Monitor state | small monitor cluster, map updates | monitor state machine/Paxos presentation made explicit | retaining the map itself has consistency/durability requirements |

The ledger is a comparison of **documented bounded designs**, not a claim that every change was first implemented in the year of publication.

---

## Claim ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| logical object location is calculable from PG + current map | `H/P` | OSDI '06 p. 312 §5.1; CRUSH §3 | strong |
| replica failure domains affect data safety | `H/P` | OSDI '06 p. 312; CRUSH §3.2 | strong |
| currentness requires version/log/peering state, not copy count alone | `H/P + E` | OSDI '06 pp. 313–314; PDSW '07 pp. 38–39 | strong |
| no permanently privileged physical home is required | `E` | placement + primary transfer + recovery sources above | strong, with temporary-primary qualification |
| ack and durable commit are distinct retention thresholds | `H/P + E` | OSDI '06 p. 313 Fig. 4 §5.3; Weil thesis pp. 131–132 | strong for bounded designs |
| physical survival can coexist with semantic staleness | `E` | peering/version/role-transition evidence | strong |
| PG metadata can remain authoritative while object replicas are missing | `H/P` | PDSW '07 pp. 38–39 §3.4 | strong |
| PG log was implemented as persisted recovery state | `H/P` implementation artifact | Ceph commit `a32d6d3`, 2007-02-26 | strong for existence, not production maturity |
| modern Ceph has the same exact semantics | `X` | not established by these sources | rejected |
| replication alone equals consensus | `X` | outside bounded mechanism | rejected |

---

## Grounding judgment

The RADOS case now satisfies the repository's `grounded` gate:

- **strong primary evidence:** OSDI '06, CRUSH SC '06, PDSW '07, Weil 2007 dissertation, contemporaneous source commit;
- **precise locations:** printed/PDF page and section anchors for central claims;
- **historical vocabulary:** object, PG, primary, replica, epoch, version, peering, ack, commit, recovery are used by the period sources themselves;
- **mechanism/failure modes:** placement, version ordering, stale replicas, `down/out`, peering, re-replication, failure domains, volatile ack vs durable commit;
- **limits/counterexamples:** temporary primary authority remains; replication is not generic consensus; modern Ceph is not inferred from the prototype;
- **related-repository check:** `tmzncty/computing-archaeology` currently has no Ceph/RADOS/CRUSH treatment, so this bounded retention analysis does not duplicate an existing technical-history article.

The next work should therefore **not** be more generic Ceph material merely to make this case longer. Useful future deepening would be narrower: early monitor/Paxos implementation archaeology, recovery-state counterexamples, or a later-version case that explicitly studies how these semantics changed.
