from pathlib import Path

CASE_PATH = Path('cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md')
EVIDENCE_PATH = Path('evidence/79-hadoop-2010-2016-startup-safemode-grounding.md')
README = Path('README.md')
ROADMAP = Path('ROADMAP.md')
INDEX = Path('CASE_INDEX.md')

case = r'''# Apache HDFS Startup SafeMode: Reconstructed Block Locations, Re-observed Replicas, and Delayed Repair Authority

## Scope

- **Object / system:** Apache Hadoop HDFS NameNode startup and SafeMode, bounded primarily to the architecture described by Shvachko et al. in 2010 and the Apache Hadoop 2.7.3 documentation/source released in 2016.
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

## Prior-art boundary

This case makes **no invention-priority claim** for:

- safe/restricted startup modes;
- rebuilding volatile inventory from peripheral/storage-device reports;
- filesystem recovery;
- replication repair;
- read-only recovery states.

The Apache 1.0.4 documentation alone shows the SafeMode concept predates the bounded 2.7.3 source used here. Earlier distributed filesystems and storage systems also had startup, recovery, and inventory-reconstruction mechanisms; reconstructing that genealogy belongs in distributed-filesystem history, preferably in `computing-archaeology` if the work expands beyond this retention-specific slice.

The defensible historical claim is narrower:

> **By the 2010 HDFS architecture account, block replica locations were deliberately excluded from the NameNode's persistent checkpoint and reconstructed from DataNode reports; the Hadoop 2.7.3 implementation then provides a directly inspectable SafeMode control regime that counts sufficiently replicated blocks, gates mutation/replication, waits through a threshold/extension boundary, and only afterward proceeds with ordinary under-replication repair.**

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
- behavior of every Hadoop release before/after 2.7.3;
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

- Konstantin Shvachko, Hairong Kuang, Sanjay Radia, Robert Chansler, **“The Hadoop Distributed File System,”** *2010 IEEE 26th Symposium on Mass Storage Systems and Technologies (MSST)*, 2010. Original conference paper: <https://storageconference.us/2010/Papers/MSST/Shvachko.pdf>.
- Apache Hadoop, **HDFS Architecture Guide, Release 2.7.3**, especially NameNode/DataNode roles, data replication, SafeMode, filesystem metadata persistence, and DataNode block reporting: <https://hadoop.apache.org/docs/r2.7.3/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html>.
- Apache Hadoop, **HDFS User Guide, Release 1.0.4**, SafeMode section: <https://hadoop.apache.org/docs/r1.0.4/hdfs_user_guide.html>.
- Apache Hadoop `rel/release-2.7.3`, `FSNamesystem.java`: <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.java>.
- Apache Hadoop `rel/release-2.7.3`, `DFSConfigKeys.java`: <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/DFSConfigKeys.java>.

### Repository comparisons

- Case 46 — GFS master log/checkpoint recovery.
- Case 49 — HDFS generation-stamp lease recovery.
- Case 50 — HDFS QJM epoch fencing.
- Case 51 — HDFS DataNode command fencing.
- Case 61 — HDFS Observer state-ID freshness.

---

## Status

**`grounded`** for the bounded 2010–2016 HDFS startup relation among persistent namespace state, non-checkpointed replica locations, DataNode block-report re-observation, SafeMode admission, and post-exit replication repair.
'''

evidence = r'''# Case 79 Grounding Record — HDFS Startup SafeMode and Block-Report Re-observation (2010–2016)

## Evidence goal

Ground the narrow claim used by Case 79:

> HDFS can recover persistent namespace identity without persisting one authoritative checkpoint of current block replica locations; DataNodes re-report their inventories after restart, and NameNode SafeMode delays ordinary mutation/replication until enough minimum-replica evidence has been re-observed.

This record does **not** attempt a full HDFS architecture history or a first-invention genealogy for safe startup modes.

---

## Source 1 — Shvachko et al., HDFS system paper (2010)

**Type:** primary/contemporary system paper (`P/H`).

Konstantin Shvachko, Hairong Kuang, Sanjay Radia, Robert Chansler, **“The Hadoop Distributed File System,”** *2010 IEEE 26th Symposium on Mass Storage Systems and Technologies (MSST)*.

Original conference paper: <https://storageconference.us/2010/Papers/MSST/Shvachko.pdf>

### Directly used facts

The inspected paper separates:

- persistent namespace metadata/checkpoint and journal recovery at the NameNode;
- DataNode-local block replicas;
- current block replica locations.

Its crucial architectural statement is that replica locations can change and are **not part of the persistent checkpoint**. On startup/reconnection, DataNodes register and provide block reports; the NameNode thereby reconstructs the current block-location relation.

The DataNode handshake also includes namespace identity, while a block report communicates the DataNode's stored block inventory (including block identity/version/length information in the bounded paper).

### Supported boundary

`durable namespace state ≠ durable replica-location inventory`.

The paper supports re-derivation of location state; it does not say payload is reconstructed merely by receiving a block report.

---

## Source 2 — Apache HDFS 2.7.3 architecture documentation

**Type:** primary institutional documentation (`P/H`).

<https://hadoop.apache.org/docs/r2.7.3/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html>

### Directly used facts

The inspected architecture guide states that:

- the NameNode manages namespace and block-to-DataNode mapping as operational metadata;
- DataNodes periodically send Heartbeats and Blockreports;
- a Blockreport contains the list of blocks on a DataNode;
- NameNode restart loads `FsImage` and applies `EditLog` changes;
- DataNode startup scans local storage and sends the resulting block inventory to the NameNode;
- the NameNode enters SafeMode on startup;
- block replication does not occur while it is in the documented startup SafeMode;
- a block counts as safely replicated when a configured minimum number of replicas have checked in;
- after a configured percentage of blocks has met that condition and the extension period has elapsed, the NameNode exits SafeMode and determines which blocks still require replication.

### Supported boundary

`startup evidence accumulation ≠ repair execution`.

The block-report phase can establish that replicas already exist; the later replication phase creates missing redundancy.

---

## Source 3 — Apache HDFS 1.0.4 user guide

**Type:** earlier primary institutional documentation (`P/H`).

<https://hadoop.apache.org/docs/r1.0.4/hdfs_user_guide.html>

### Why it is retained

The older guide establishes that the SafeMode startup rationale predates the bounded 2.7.3 source implementation. It explains that the NameNode waits for DataNodes to report blocks to avoid prematurely replicating blocks that may already have sufficient replicas but whose reports have not yet arrived. It also describes SafeMode as essentially read-only, with filesystem/block modification restricted.

### Boundary

This is **continuity evidence**, not first-use or invention-priority evidence.

---

## Source 4 — Hadoop 2.7.3 `FSNamesystem.java`

**Type:** tag-matched primary implementation source (`P/H`).

<https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.java>

### Directly inspected anchors

`SafeModeInfo` contains configuration/control fields including:

- `threshold`;
- `datanodeThreshold`;
- `extension`;
- `safeReplication`;
- `replQueueThreshold`;
- `blockTotal`;
- `blockSafe`;
- reached/extension progress state.

The implementation's `incrementSafeBlockCount(short replication)` increments the safe count when replication reaches the configured `safeReplication` boundary.

`canLeave()` requires the threshold to have been reached and the extension interval to have elapsed, subject to the remaining SafeMode checks.

File creation calls `checkNameNodeSafeMode(...)`, grounding the claim that SafeMode is an actual mutation gate rather than only a display/status concept.

Replication-queue initialization is separately gated by a replication-queue threshold, which helps keep “enough evidence to begin some repair planning” distinct from “SafeMode fully exited.”

### Boundary

The in-memory counters/threshold state are **control state**, not a persistent history of each report. The source is not used to claim a particular durable representation for SafeMode counters across NameNode restart.

---

## Source 5 — Hadoop 2.7.3 `DFSConfigKeys.java`

**Type:** tag-matched primary implementation source (`P/H`).

<https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/DFSConfigKeys.java>

### Directly inspected bounded defaults

For this release:

- `DFS_NAMENODE_SAFEMODE_THRESHOLD_PCT_DEFAULT = 0.999f`;
- `DFS_NAMENODE_SAFEMODE_EXTENSION_DEFAULT = 30000` ms;
- `DFS_NAMENODE_REPLICATION_MIN_DEFAULT = 1`;
- ordinary `DFS_REPLICATION_DEFAULT = 3`.

### Why this matters

These values directly prevent the false equation:

`safe for startup exit = already at ordinary configured replication factor`.

The defaults are **release-specific**. They are not projected backward or forward to every HDFS release/deployment.

---

## Source triangulation

The case is `grounded` because the central relation is supported at several levels:

1. **2010 system architecture paper** — location state is not in the persistent checkpoint and is re-learned from DataNodes;
2. **versioned Apache documentation** — startup SafeMode waits for reported minimum-replica evidence and postpones block replication;
3. **tag-matched implementation** — the exact SafeMode counters, threshold/extension checks, mutation gate, and replication-queue gating are inspectable;
4. **tag-matched configuration source** — release defaults show why SafeMode `safe` cannot be normalized into `full configured redundancy`;
5. **older Apache user guide** — confirms the operational rationale is older than 2.7.3 without turning the case into a priority claim.

---

## Negative claims / evidence limits

The sources do **not** establish:

- that a reported replica has passed every checksum/integrity verification merely because it contributes to the SafeMode count;
- that every SafeMode read succeeds;
- that SafeMode is a quorum/consensus proof;
- that HDFS invented read-only recovery or safe startup;
- that current replica locations are never persisted anywhere in every later HDFS subsystem;
- that the 2.7.3 defaults are invariant across deployments/releases;
- that a missing report proves a replica has been physically destroyed;
- a full performance model of large-cluster startup.

These boundaries are carried into the case text.

---

## Prior-art boundary

No invention claim is made for SafeMode, startup inventory reconstruction, or replication repair. Apache HDFS 1.0.4 already documents the mechanism before the 2.7.3 implementation used for source-level inspection. A proper genealogy would need earlier HDFS releases plus predecessor/distributed-filesystem recovery literature.

That broader technical history belongs in `computing-archaeology` if pursued. The retention-specific contribution here is the decomposition:

`persistent namespace -> re-observed location evidence -> startup admission -> later redundancy repair`.

---

## Related-repository duplication check

Repository search found no dedicated `HDFS` or `SafeMode` treatment in `tmzncty/computing-archaeology` at the time of this slice. Therefore Case 79 does not duplicate an existing companion history. If such a history is later added, this case should link to it rather than expand into a general HDFS architecture account.

---

## Status decision

**`grounded`**.

Reason: the central claim is triangulated by a contemporary system paper, versioned Apache documentation, and exact tag-matched source/configuration. Historical vocabulary and source boundaries are explicit, analogies are labeled, and the case does not depend on an unverified implementation assumption.
'''

if CASE_PATH.exists() or EVIDENCE_PATH.exists():
    raise SystemExit('case79 target already exists; refusing duplicate integration')
CASE_PATH.write_text(case)
EVIDENCE_PATH.write_text(evidence)

# README: add the new case directly after Case 78.
readme = README.read_text()
case78_marker = '- [`Case 78 — Micron NAND Bad Blocks: Erasable Factory Defect Marks, Retained Bad-Block Tables, and Replacement`](cases/78-micron-nand-bad-block-marker-management.md)'
pos = readme.find(case78_marker)
if pos < 0:
    raise SystemExit('README Case 78 marker missing')
line_end = readme.find('\n', pos)
if line_end < 0:
    raise SystemExit('README Case 78 line terminator missing')
case79_line = '- [`Case 79 — Apache HDFS Startup SafeMode: Reconstructed Block Locations, Re-observed Replicas, and Delayed Repair Authority`](cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md) — `grounded`; the 2010 HDFS paper and Hadoop 2.7.3 documentation/source separate durable namespace recovery from non-checkpointed replica-location re-observation: DataNode Blockreports rebuild the location view while SafeMode gates ordinary mutation/replication until a configured minimum-replica threshold/extension is satisfied, after which under-replication repair proceeds. Grounding: [`evidence/79-hadoop-2010-2016-startup-safemode-grounding.md`](evidence/79-hadoop-2010-2016-startup-safemode-grounding.md).\n'
readme = readme[:line_end+1] + case79_line + readme[line_end+1:]
README.write_text(readme)

# ROADMAP: add one bounded distributed-storage bridge before the broad DRAM continuation.
roadmap = ROADMAP.read_text()
dram_marker = '- [ ] DRAM evolution and refresh machinery beyond the bounded case — **partially advanced by thirteen grounded bounded sub-slices**:'
if roadmap.count(dram_marker) != 1:
    raise SystemExit(f'ROADMAP DRAM marker count={roadmap.count(dram_marker)}')
roadmap_entry = '- [x] HDFS startup SafeMode / block-report re-observation — [`cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md`](cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md), grounded by [`evidence/79-hadoop-2010-2016-startup-safemode-grounding.md`](evidence/79-hadoop-2010-2016-startup-safemode-grounding.md), separates persistent namespace reconstruction from non-checkpointed replica-location re-observation: DataNode Blockreports rebuild the NameNode location view, SafeMode postpones ordinary mutation/replication until a configured safe-block threshold/extension is met, and later under-replication repair remains a distinct stage. This is separate from HDFS HA command fencing (Case 51), Observer freshness (Case 61), and block-integrity verification; broader startup/recovery genealogy belongs in `computing-archaeology`.\n'
roadmap = roadmap.replace(dram_marker, roadmap_entry + dram_marker, 1)
ROADMAP.write_text(roadmap)

idx = INDEX.read_text()

def insert_after_line_containing(text, needle, addition):
    p = text.find(needle)
    if p < 0:
        raise SystemExit(f'INDEX marker missing: {needle}')
    if text.find(needle, p + 1) >= 0:
        raise SystemExit(f'INDEX marker not unique: {needle}')
    e = text.find('\n', p)
    if e < 0:
        raise SystemExit(f'INDEX line end missing: {needle}')
    return text[:e+1] + addition + text[e+1:]

ledger_line = '| [Apache HDFS Startup SafeMode: Reconstructed Block Locations, Re-observed Replicas, and Delayed Repair Authority](cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md) | **grounded** | persistent NameNode namespace + DataNode-resident block replicas + non-checkpointed/re-reported location state + SafeMode safe-block counters/thresholds + post-exit replication queues | separate durable namespace from current replica-location knowledge; physical replica survival from re-observed availability; Blockreport from repair; startup admission from full redundancy restoration | [2010–2016 HDFS startup/SafeMode grounding](evidence/79-hadoop-2010-2016-startup-safemode-grounding.md); full SafeMode genealogy, newer HA/startup semantics, checksum-integrity composition, startup fault injection, and performance traces remain separate work |\n'
idx = insert_after_line_containing(idx, '| [Micron NAND Bad Blocks: Erasable Factory Defect Marks, Retained Bad-Block Tables, and Replacement](cases/78-micron-nand-bad-block-marker-management.md)', ledger_line)

matrix_line = '| HDFS startup SafeMode / 2010–2016 bounded regime | persistent namespace/checkpoint+journal + DataNode block replicas + reconstructed block-location relation + SafeMode safe-block/threshold state | load namespace; DataNodes rescan/report; count minimum-replica observations; defer ordinary replication until SafeMode criteria/extension; then repair under-replication | SafeMode is essentially read-only in bounded docs, but a reported/known serving replica is still required for a given read; writes/mutations are gated | file/path -> block identity from persistent namespace, then Blockreport-derived block -> DataNode location relation | DataNode replicas may physically survive while the restarted NameNode has not yet re-observed them; later repair may add embodiments without changing logical block identity | persistent namespace history is bounded by image/journal; current location knowledge is re-derived, and SafeMode counters do not retain complete report history |\n'
idx = insert_after_line_containing(idx, '| ONFI/Micron NAND bad-block management / 2006–2011 bounded regime |', matrix_line)

old_aggregate = 'After seventy-nine bounded cases, **all seventy-nine cases are now `grounded`.**'
new_aggregate = 'After eighty bounded cases, **all eighty cases are now `grounded`.**'
if idx.count(old_aggregate) != 1:
    raise SystemExit(f'INDEX aggregate marker count={idx.count(old_aggregate)}')
idx = idx.replace(old_aggregate, new_aggregate, 1)

findings = r'''

## Case 79 — HDFS startup SafeMode findings

941. **durable namespace ≠ durable replica-location inventory** — the bounded HDFS architecture persists namespace/checkpoint+journal state while current block replica locations are re-derived from DataNode reports;
942. **DataNode block survival ≠ NameNode-observed availability** — a replica can physically survive restart while the new NameNode working view has not yet received the report that locates it;
943. **Blockreport ≠ payload replication** — reporting an already-present block can increase startup knowledge/safe-block progress without creating another block copy;
944. **namespace recovery ≠ location-view recovery** — loading `FsImage`/journal reconstructs logical namespace state, while DataNode registration/reporting reconstructs a different distributed placement relation;
945. **startup SafeMode ≠ data-restoration mechanism** — SafeMode gates operations while evidence accumulates; it does not itself recreate every missing payload replica;
946. **safely replicated for SafeMode ≠ full configured replication factor** — Hadoop 2.7.3 defaults minimum replication to 1 while ordinary default replication is 3, so startup admissibility can precede restoration of desired redundancy margin;
947. **0.999 safe-block threshold ≠ every block fully accounted for or fully redundant** — the release-specific threshold is a policy boundary over minimum-replica observations, not a proof of universal full replication;
948. **repair suppression under startup uncertainty ≠ maintenance abandonment** — documented SafeMode postpones block replication so the NameNode does not act prematurely on an incomplete report population;
949. **repair-need discovery ≠ repair execution** — after SafeMode exit the NameNode can identify under-replicated blocks, while actual replica creation is subsequent maintenance work;
950. **re-observation can be constitutive availability state without being payload** — Blockreport-derived location knowledge determines which surviving embodiments the NameNode can treat as current serving/management candidates;
951. **SafeMode counters/threshold state ≠ complete block-report history** — bounded progress summaries and current inventory relations need not preserve the sequence of every report event;
952. **SafeMode read-only policy ≠ guarantee that every read succeeds** — the mode restricts modifications, but a requested block can still lack a currently known/live serving replica;
953. **automatic startup SafeMode ≠ manual SafeMode** — the 2.7.3 source gives manual/resource-low mode deliberately unreachable automatic thresholds, so trigger and exit authority must remain distinct;
954. **namespace-ID continuity ≠ replica-location continuity** — a DataNode can remain in the same filesystem namespace while its current replica inventory still has to be re-advertised after registration/restart;
955. **startup inventory confidence ≠ HA command fencing ≠ Observer read-freshness alignment** — Cases 51, 61, and 79 preserve different control relations even though all affect whether surviving distributed state may be acted upon;
956. **HDFS bounded SafeMode evidence ≠ invention-priority proof** — older HDFS documentation already precedes the inspected 2.7.3 source, and the case makes no claim that Apache invented safe startup, read-only recovery, or inventory reconstruction.
'''
idx = insert_after_line_containing(idx, '940. **NAND bad-block replacement ≈ SCSI grown-defect reassignment only at the continuity relation**', findings)
INDEX.write_text(idx)

# Validate repository-facing invariants before removing the one-shot machinery.
assert CASE_PATH.exists() and EVIDENCE_PATH.exists()
readme = README.read_text()
roadmap = ROADMAP.read_text()
idx = INDEX.read_text()
assert readme.count('cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md') == 1
assert readme.count('evidence/79-hadoop-2010-2016-startup-safemode-grounding.md') == 1
assert roadmap.count('cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md') == 1
assert roadmap.count('evidence/79-hadoop-2010-2016-startup-safemode-grounding.md') == 1
assert idx.count('cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md') == 1
assert idx.count('| HDFS startup SafeMode / 2010–2016 bounded regime |') == 1
assert idx.count('## Case 79 — HDFS startup SafeMode findings') == 1
assert idx.count('941. **durable namespace ≠ durable replica-location inventory**') == 1
assert idx.count('956. **HDFS bounded SafeMode evidence ≠ invention-priority proof**') == 1
assert idx.count('After eighty bounded cases, **all eighty cases are now `grounded`.**') == 1

case_nums = sorted(int(p.name.split('-', 1)[0]) for p in Path('cases').glob('[0-9][0-9]-*.md'))
assert case_nums == list(range(80)), case_nums

# One-shot integration machinery must not remain in the final tree.
for temp in [Path('.github/case79_integrate.py'), Path('.github/workflows/case79-integration.yml')]:
    if temp.exists():
        temp.unlink()

print('Case 79 integration prepared and validated: cases 00–79 contiguous, navigation and findings updated.')
