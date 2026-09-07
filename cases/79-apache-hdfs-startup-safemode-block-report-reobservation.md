# Apache HDFS Startup SafeMode: Reconstructed Block Locations, Re-observed Replicas, and Delayed Repair Authority

## Scope

- **Object / system:** Apache Hadoop HDFS NameNode startup and SafeMode, now bounded by exact released source from Hadoop 0.18.0 (2008), the architecture described by Shvachko et al. in 2010, Apache 1.0.4 documentation, and released 2.7.3/2.8.0 source through 2017.
- **Retention question:** after the NameNode has recovered the durable namespace, what additional state must be re-observed before the system is willing to resume ordinary mutation and replication work?
- **Primary evidence:** the 2010 HDFS architecture paper; Apache HDFS 1.0.4 and 2.7.3 documentation; tag-matched Hadoop 2.7.3 `FSNamesystem.java` and `DFSConfigKeys.java`.
- **Status:** `grounded`.

This is **not** a general history of HDFS, NameNode HA, block placement, leases, checksums, replication algorithms, or Hadoop operations. Cases 49–51 and 61 already cover other HDFS control-state boundaries: generation-stamp lease recovery, QJM epoch fencing, DataNode command fencing, and Observer read freshness. This case asks a different startup question:

> **How can a distributed filesystem recover durable namespace identity while deliberately refusing to treat surviving replica locations as already known enough for ordinary mutation/repair?**

The bounded answer is that HDFS does not need one durable NameNode checkpoint of every current block location. DataNodes retain block replicas and report their inventories after registration. The NameNode reconstructs a location view from those reports while SafeMode keeps ordinary namespace/block mutation and replication work restricted until a configured sufficient-replica condition has been re-established.

The project terms `re-observation`, `inventory-confidence state`, and `delayed repair authority` below are **engineering reconstructions**, not Apache historical vocabulary.

---

## Historical vocabulary

The inspected HDFS sources use these terms directly:

- `NameNode`;
- `DataNode`;
- `FsImage`;
- `EditLog` / journal;
- `Blockreport` / `block report`;
- `Heartbeat`;
- `SafeMode` / `safe mode`;
- `safe blocks` in the implementation;
- `safely replicated` in user/architecture documentation;
- `minimum number of replicas` / minimum replication;
- safe-mode `threshold`;
- safe-mode `extension`;
- replication queues;
- under-replicated blocks.

Do not silently replace these with stronger modern abstractions such as `proof`, `quorum`, `consensus`, `integrity certificate`, or `durable inventory ledger`. A block report is positive inventory evidence from a DataNode, not a cryptographic or Byzantine proof.

---

## Retained state

The bounded startup path exposes several different retained-state classes.

### 1. Durable namespace state

The NameNode's persistent namespace is reconstructed from checkpoint/image and journal/edit information. This retains file and directory metadata and the relation from files to block identities.

### 2. DataNode-resident block replicas

The payload blocks and their local replica metadata survive on DataNode storage independently of one NameNode process lifetime.

### 3. Reconstructed block-location knowledge

The 2010 HDFS paper explicitly says block replica locations may change and are **not part of the persistent checkpoint**. DataNodes send a block report after registration, and the NameNode learns current replica locations from this distributed inventory evidence.

### 4. SafeMode progress/control state

In Hadoop 2.7.3 the `SafeModeInfo` object tracks, among other things:

- the configured safe-block threshold;
- a minimum DataNode threshold;
- an extension interval;
- `safeReplication`;
- `blockTotal` and `blockSafe`;
- the threshold for populating replication queues;
- whether the threshold has been reached and whether the extension period has elapsed.

These values are neither user payload nor a complete record of every block-report event. They are bounded control state used to decide when the recovered namespace/location view is sufficient for later operations.

---

## Physical / logical substrate

The logical namespace and the physical replica population cross process and machine boundaries:

```text
persistent NameNode namespace
  file/path -> block identities
             │
             │ restart reconstructs namespace
             ▼
      NameNode working state
             │
             │ DataNode registration + Blockreport
             ▼
reconstructed block -> DataNode location relation
             │
             │ sufficient safe-block condition + extension
             ▼
ordinary mutation / replication management resumes
```

The key methodological point is that the middle relation is not simply another copy of payload. It is a recovered **placement/availability relation** between stable block identities and currently reporting physical replicas.

Therefore:

> **durable namespace identity ≠ durable replica-location inventory.**

And:

> **replica bytes surviving on a DataNode ≠ the restarted NameNode already knowing that replica as currently available.**

---

## Historical record: namespace recovery and location re-observation

### H/P — 2010 HDFS architecture paper

Konstantin Shvachko, Hairong Kuang, Sanjay Radia, and Robert Chansler describe the NameNode's persistent namespace state separately from replica location state. On restart, the NameNode restores its namespace from the checkpoint/image and journal. The paper then makes the critical boundary explicit: **block replica locations are not part of the persistent checkpoint because they may change**. DataNodes register and send block reports containing their stored block inventory, which the NameNode uses to reconstruct the location relation.

This is not evidence that HDFS forgets block identities. The persistent namespace still identifies blocks and their file relation. What is deliberately re-derived is the currently observed mapping from block identities to DataNode replicas.

### H/P — Apache HDFS architecture documentation

The Apache 2.7.3 architecture documentation gives the same division of work at the operational interface:

- the NameNode maintains namespace and block-to-DataNode mapping as working metadata;
- DataNodes send Heartbeats and Blockreports;
- a Blockreport contains the list of blocks on the DataNode;
- NameNode restart loads `FsImage` and applies `EditLog` changes;
- a DataNode scans its local storage and reports its block inventory.

The documentation then places SafeMode between startup reconstruction and ordinary replication management.

### E — engineering reconstruction

The retention consequence is not merely “some metadata is volatile.” More precisely:

1. block identity and file membership can survive in durable NameNode state;
2. block payload can survive in DataNode storage;
3. the relation “replica R is currently present on DataNode D” can nevertheless require **fresh observation after restart**;
4. the system can defer actions that would be unsafe or wasteful if it acted on an incomplete location view.

This is a distinct retention regime from preserving a complete location table across crash.

---

## SafeMode: successful recovery is not one instant

### H/P — startup gate

Apache documentation describes NameNode startup as entering SafeMode. During this period block replication does not proceed. A block becomes “safely replicated” for the SafeMode calculation when a configured minimum number of replicas have checked in. Once a configurable percentage of blocks satisfies that criterion and the extension interval has elapsed, the NameNode leaves SafeMode and then determines which blocks remain under-replicated and starts replication work.

The older Apache HDFS 1.0.4 user guide explains the operational reason particularly clearly: the NameNode waits for DataNodes to report blocks so that it does not begin replicating prematurely even though enough replicas may already exist but have not yet reported.

### H/P — Hadoop 2.7.3 source

Tag-matched `FSNamesystem.java` keeps the distinction concrete:

- `SafeModeInfo` stores `threshold`, `datanodeThreshold`, `extension`, `safeReplication`, block totals, safe-block totals, and replication-queue threshold state;
- `incrementSafeBlockCount()` advances the safe count when observed replication reaches the configured `safeReplication` boundary;
- `canLeave()` refuses automatic exit until the threshold has been reached and the extension period has passed, subject to the remaining SafeMode conditions;
- ordinary file creation calls `checkNameNodeSafeMode(...)`, making SafeMode an actual mutation gate rather than merely a status message;
- replication-queue initialization has its own threshold check.

`DFSConfigKeys.java` in the same 2.7.3 tag gives the bounded release defaults:

- `dfs.namenode.safemode.threshold-pct = 0.999`;
- `dfs.namenode.safemode.extension = 30000` ms;
- `dfs.namenode.replication.min = 1`.

These are release-specific defaults, not timeless definitions of HDFS SafeMode.

---

## “Safe” does not mean “fully replicated”

The word `safe` can tempt a stronger claim than the bounded source supports.

In Hadoop 2.7.3, the default SafeMode minimum replication is **one**, while the ordinary default file replication factor is **three**. Therefore the SafeMode predicate is not “every block has already reached its final configured redundancy.” It is a startup gate based on enough blocks having reached a configured minimum observed-replica condition.

After SafeMode exits, the NameNode can identify blocks that remain under-replicated and schedule additional copies.

So:

> **safely replicated for SafeMode ≠ fully restored configured replication margin.**

Likewise:

> **99.9% safe-block threshold ≠ proof that 100% of blocks are fully redundant.**

The remaining fraction, minimum-replication choice, and later replication queues must be kept visible.

---

## Block report is evidence, not repair

A block report describes a DataNode's block inventory. Sending the report does not itself copy the user block to another DataNode, restore a lost replica, or increase redundancy.

This yields a useful sequence:

```text
replica already survives on DataNode
        │
        ▼
DataNode reports replica identity/state
        │
        ▼
NameNode re-establishes observed location relation
        │
        ▼
SafeMode progress may increase
        │
        ▼
NameNode later decides repair / replication work
        │
        ▼
new replica may actually be created
```

Thus:

> **re-observation ≠ restoration.**

and:

> **repair-need discovery ≠ repair execution.**

The deliberate suppression of ordinary replication during startup uncertainty is therefore not maintenance abandonment. It is a scheduling/authority choice: first recover enough inventory evidence to avoid acting on an obviously incomplete view, then perform the remaining repair work.

---

## Read / write semantics

Apache's older user guide calls NameNode SafeMode “essentially a read-only mode” in which modifications to the filesystem or blocks are not allowed.

That wording must be kept bounded.

It supports:

> **namespace/payload survival can permit some read-only service before ordinary mutation authority resumes.**

It does **not** support:

> every read must succeed while SafeMode is active.

A requested block may still lack a currently known/live serving replica, and this case does not audit every read-path exception. `read-only mode` is therefore a control-policy description, not a universal availability guarantee.

---

## Time and thresholds

Case 79 has at least four different clocks/boundaries:

1. **persistent namespace recovery time** — loading image/checkpoint and replaying durable edits;
2. **inventory re-observation time** — DataNodes register and send block reports;
3. **SafeMode threshold/extension time** — enough blocks satisfy the configured minimum and the extension interval runs;
4. **post-exit repair time** — under-replicated blocks are subsequently copied until desired redundancy is restored.

They are not one “recovery complete” timestamp.

This yields:

> **namespace recovery completion ≠ location-view reconstruction completion ≠ mutation/repair admission ≠ redundancy restoration completion.**

The staged structure is a strong retention example because a stable user-visible object can depend on several independently timed control relations after restart.

---

## Failure / forgetting modes

Keep these distinct:

- **lost NameNode namespace image/journal** — can destroy or invalidate logical namespace reconstruction even when DataNode block files survive;
- **DataNode disk/replica loss** — removes a physical payload embodiment;
- **DataNode not yet reported** — does not prove the local replica is lost; it may be surviving but not yet re-observed;
- **stale/incomplete NameNode location view** — placement knowledge is incomplete even while blocks survive elsewhere;
- **insufficient safe-block progress** — keeps automatic SafeMode active;
- **premature forced exit** — can allow actions to proceed from a less-complete inventory view than the automatic policy would require;
- **under-replication after exit** — system may be serviceable while future failure margin remains below the desired replication factor;
- **checksum/content corruption** — a different integrity problem; ordinary block-report presence is not proof that every reported byte passes independent integrity verification;
- **manual SafeMode** — a separate operator-controlled regime and should not be confused with automatic startup threshold progress.

A particularly useful negative result is:

> **absence from the current reconstructed inventory ≠ historical proof of physical destruction.**

At startup it may instead mean that positive presence evidence has not yet arrived.

---

## Maintenance and labor

The apparently simple property “the file is still there after NameNode restart” depends on work distributed across machines and layers:

- persistent NameNode namespace logging/checkpointing before failure;
- DataNode local storage and startup scanning;
- DataNode registration and block-report generation;
- NameNode inventory reconstruction;
- SafeMode accounting and threshold policy;
- post-exit under-replication scheduling;
- actual replica transfer;
- operator policy and, where used, manual SafeMode actions.

No single one of these is “retention” in the abstract. Together they make the retained namespace usable again without requiring one durable central checkpoint of every replica location.

---

## Cross-case comparison

### Case 46 — GFS master recovery

GFS and bounded HDFS both supply an important functional comparison: durable namespace/control state can coexist with replica-location information that is deliberately re-derived from storage servers after restart. This is a **functional analogy**, not a genealogy claim.

Case 46 emphasizes GFS operation-log/checkpoint recovery and re-derived chunk locations. Case 79 adds a more explicit startup admission policy: HDFS uses block-report progress and SafeMode thresholds to delay ordinary modification/replication while that distributed location view is re-established.

### Case 51 — HDFS DataNode command fencing

Case 51 asks **which NameNode may issue block-changing commands after HA failover**. Case 79 asks **whether a restarting NameNode has re-observed enough replica inventory to resume ordinary mutation/repair work**.

Therefore:

> **command-source authority ≠ startup inventory confidence.**

### Case 61 — HDFS Observer freshness

Case 61 uses state IDs so a client can reject a read from an Observer that is behind a required namespace frontier. Case 79 instead reconstructs DataNode block-location availability during NameNode startup.

Therefore:

> **client-qualified read freshness ≠ startup block-location re-observation.**

### Cases 17/19/24 — redundancy and repair

Those cases show that service can continue before full repair margin is restored. Case 79 adds a different precursor: a system may first need to **relearn which redundancy already survives** before deciding how much new redundancy to create.

---

## Historical deepening — exact 0.18.0 implementation and later lifecycle continuity

### H/P — Hadoop 0.18.0 already implements the report-rebuilt location relation

Apache records Hadoop 0.18.0 as released on **22 August 2008**. More importantly than the release notice alone, the exact `release-0.18.0` `FSNamesystem.java` source states in its bookkeeping summary that the `block -> machinelist` relation is **kept in memory and rebuilt dynamically from reports**. The same source's DataNode-map documentation says that only the `DatanodeInfo` portion is checkpointed while the list of blocks is restored from DataNode block reports.

This supplies an implementation-level floor for the central Case-79 relation two years before the 2010 MSST paper:

> **by released Hadoop 0.18.0, HDFS already distinguished checkpointed namespace/DataNode descriptive state from a block-location relation reconstructed from reports.**

This is a chronology floor for HDFS only. It is not an invention-priority claim for report-rebuilt inventories, read-only startup modes, or distributed recovery gates.

### H/P — 0.18.0 startup SafeMode already retains typed progress state

The same exact source loads `FSImage`, constructs `SafeModeInfo`, sets the total-block denominator, and starts the relevant monitors. Its startup `SafeModeInfo(Configuration)` retains:

- a safe-block ratio threshold;
- an extension;
- `safeReplication`;
- `blockTotal`;
- `blockSafe`;
- threshold-reached state.

For this release the source defaults are `dfs.safemode.threshold.pct = 0.95`, `dfs.safemode.extension = 0`, and `dfs.replication.min = 1`.

This is useful precisely because later releases differ. Hadoop 1.0.4 documents `0.999f` and a 30-second extension, while later 2.x source retains the same general threshold/extension structure. Therefore:

> **same named SafeMode mechanism across releases ≠ one timeless quantitative admission contract.**

The 0.18.0 values are historical release-specific implementation evidence, not reliability constants.

### H/P — manual SafeMode is already a distinct state machine in 0.18.0

The exact 0.18.0 source has a separate no-argument `SafeModeInfo()` constructor for manual entry. It uses deliberately unreachable automatic-exit parameters, sets `blockTotal` and `blockSafe` to `-1`, and `isManual()` identifies the mode from that state. Hadoop 2.8.0 later makes the same lifecycle distinction explicit in class documentation: startup SafeMode tracks safe blocks for automatic exit, whereas manually entered SafeMode is not intended to leave through that automatic startup condition.

This strengthens the existing boundary:

> **startup SafeMode ≠ manual SafeMode, even when both expose the same service-state name.**

The distinction is historical/implementation evidence, not a modern philosophical analogy.

### Cross-case controls added by consolidation

Case 80 separately shows that replica count does not establish rack/failure-domain placement satisfaction. Case 83 separately shows that a present/reported replica is not thereby checksum-qualified. Case 116 separately models temporary DataNode maintenance with an expiry. Consequently:

- **safe-block admission ≠ rack-placement qualification**;
- **safe/reported replica ≠ integrity-qualified replica**;
- **NameNode-wide startup SafeMode ≠ per-DataNode maintenance mode**.

These are bounded functional comparisons within the repository, not implementation genealogy.

---

## Prior-art boundary

This case makes **no invention-priority claim** for:

- safe/restricted startup modes;
- rebuilding volatile inventory from peripheral/storage-device reports;
- filesystem recovery;
- replication repair;
- read-only recovery states.

Exact released Hadoop 0.18.0 source already implements report-rebuilt block-location state and separate startup/manual SafeMode control before the 2010 paper and later 1.x/2.x continuity sources. Earlier distributed filesystems and storage systems also had startup, recovery, and inventory-reconstruction mechanisms; reconstructing that broader genealogy belongs in distributed-filesystem history, preferably in `computing-archaeology` if the work expands beyond this retention-specific slice.

The defensible historical claim is narrower:

> **By released Hadoop 0.18.0, the implementation already kept the block-to-machine relation in memory and rebuilt it from reports while separating startup and manual SafeMode control state; the 2010 architecture paper and later 1.x/2.x documentation/source then independently expose the same namespace/re-observation split and its evolving threshold, extension, mutation-gating, and post-exit repair semantics.**

---

## Engineering reconstruction

The case adds these controlled retention relations:

1. `durable namespace ≠ durable replica-location inventory`;
2. `physical replica survival ≠ NameNode-observed availability`;
3. `block report ≠ payload replication`;
4. `namespace recovery ≠ location-view recovery`;
5. `re-observation ≠ restoration`;
6. `SafeMode admission threshold ≠ full configured redundancy`;
7. `repair-need discovery ≠ repair execution`;
8. `repair suppression under startup uncertainty ≠ maintenance abandonment`;
9. `read-only startup policy ≠ universal read-availability guarantee`;
10. `positive location evidence ≠ content-integrity proof`;
11. `startup SafeMode ≠ HA command fencing ≠ Observer freshness alignment`.

These are project reconstructions used to compare mechanisms. They are not claims that Apache developers used the repository's vocabulary.

---

## Philosophical interpretation — bounded

Case 79 is useful for the repository's addressability/currentness thesis because **physical survival and logical designation still do not exhaust technical availability**. A block can have a stable file/block identity and surviving bytes, while the restarted coordination layer has not yet reconstructed the relation needed to treat that embodiment as presently available for ordinary management.

That does not justify calling SafeMode “memory,” “institutional forgetting,” or a Heideggerian concept. The legitimate philosophical use is narrower: availability is an achieved relation among retained identity, surviving embodiment, re-established knowledge, and operational authority.

---

## Limitations

This bounded case does not establish:

- the first historical SafeMode implementation in HDFS;
- the genealogy of safe startup/read-only recovery modes;
- behavior of every Hadoop release outside the bounded 0.18.0 / 1.0.4 / 2.7.3 / 2.8.0 evidence chain;
- every HA startup/failover interaction;
- checksum validation semantics of block reports;
- exact large-cluster startup performance;
- DataNode-local on-disk recovery internals;
- operator practices or empirical outage distributions;
- that a `safe` block is independently verified correct at the byte level;
- that all HDFS reads succeed in SafeMode.

Those are separate archival, implementation, or experimental projects.

---

## Related repositories

A search of `tmzncty/computing-archaeology` found no dedicated HDFS/SafeMode treatment at the time of this case. The broader history of distributed filesystems, NameNode architecture, and startup/recovery design should be built there if needed. `technical-retention` should retain only the bounded comparison among durable namespace state, reconstructed replica-location evidence, SafeMode admission, and later repair.

---

## Claim ledger

| Claim | Layer | Support / boundary |
| --- | --- | --- |
| released Hadoop 0.18.0 keeps block→machine location state in memory and rebuilds it from reports | `H/P` | exact `release-0.18.0` `FSNamesystem.java`; HDFS implementation chronology floor only |
| startup and manual SafeMode already use distinguishable control state in 0.18.0 | `H/P` | separate `SafeModeInfo` constructors plus `isManual()`; later 2.8.0 source is continuity evidence |
| HDFS NameNode persistent namespace recovery is separated from replica-location reconstruction | `H/P` | Shvachko et al. 2010 plus Apache architecture docs |
| block replica locations are not part of the persistent NameNode checkpoint in the bounded architecture | `H/P` | Shvachko et al. 2010 |
| DataNodes re-advertise local block inventories through block reports | `H/P` | 2010 paper + Apache docs/source |
| startup SafeMode suppresses ordinary block replication until a configured safe-block condition is reached | `H/P` | Apache HDFS docs + Hadoop 2.7.3 source |
| 2.7.3 defaults use 0.999 threshold, 30 s extension, and minimum replication 1 | `H/P` | tag-matched `DFSConfigKeys.java` |
| safe-mode minimum replication is not the same as ordinary desired replication factor | `E` grounded in `P` | 2.7.3 defaults separate `dfs.namenode.replication.min=1` from `dfs.replication=3` |
| surviving replica bytes can exist before the restarted NameNode has re-observed them | `E` | inferred directly from nonpersistent location table + report-driven reconstruction |
| block report is re-observation rather than payload repair | `E` | report semantics versus later replication work |
| HDFS SafeMode is analogous to GFS re-derived location state only at a bounded functional level | `A` | Cases 46/79; no genealogy claimed |
| SafeMode is a proof of byte integrity | `X` | unsupported; inventory presence and independent integrity are separate |
| HDFS 2.7.3 invented safe startup modes | `X` | no priority evidence; older HDFS docs and broader systems history predate bounded source |
| SafeMode guarantees every read succeeds | `X` | documentation supports an essentially read-only policy, not universal read success |

---

## Sources

### Primary / contemporary / institutional

- Apache Hadoop, **release 0.18.0 available**, 22 August 2008: <https://hadoop.apache.org/release/0.18.0.html>.
- Apache Hadoop `release-0.18.0`, **`src/hdfs/org/apache/hadoop/dfs/FSNamesystem.java`**, exact released implementation of report-rebuilt block locations and startup/manual `SafeModeInfo`: <https://github.com/apache/hadoop/blob/release-0.18.0/src/hdfs/org/apache/hadoop/dfs/FSNamesystem.java>.
- Konstantin Shvachko, Hairong Kuang, Sanjay Radia, Robert Chansler, **“The Hadoop Distributed File System,”** *2010 IEEE 26th Symposium on Mass Storage Systems and Technologies (MSST)*, 2010. Original conference paper: <https://storageconference.us/2010/Papers/MSST/Shvachko.pdf>.
- Apache Hadoop, **HDFS Architecture Guide, Release 2.7.3**, especially NameNode/DataNode roles, data replication, SafeMode, filesystem metadata persistence, and DataNode block reporting: <https://hadoop.apache.org/docs/r2.7.3/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html>.
- Apache Hadoop, **HDFS User Guide, Release 1.0.4**, SafeMode section: <https://hadoop.apache.org/docs/r1.0.4/hdfs_user_guide.html>.
- Apache Hadoop `rel/release-2.7.3`, `FSNamesystem.java`: <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.java>.
- Apache Hadoop `rel/release-2.7.3`, `DFSConfigKeys.java`: <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/DFSConfigKeys.java>.
- Apache Hadoop 2.8.0, **`FSNamesystem.SafeModeInfo` source rendering**, startup versus manually entered SafeMode lifecycle: <https://hadoop.apache.org/docs/r2.8.0/hadoop-project-dist/hadoop-hdfs/api/src-html/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.SafeModeInfo.html>.

### Repository comparisons

- Case 46 — GFS master log/checkpoint recovery.
- Case 49 — HDFS generation-stamp lease recovery.
- Case 50 — HDFS QJM epoch fencing.
- Case 51 — HDFS DataNode command fencing.
- Case 61 — HDFS Observer state-ID freshness.

---

## Status

**`grounded`** for the bounded 2008–2017 HDFS startup relation among persistent namespace state, report-rebuilt replica locations, startup/manual SafeMode control state, admission thresholds, and post-exit replication repair. The accidental later Case 117 duplicate has been consolidated into this canonical case without asserting a broader invention genealogy.
