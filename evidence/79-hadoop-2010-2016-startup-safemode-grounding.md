# Case 79 Grounding Record — HDFS Startup SafeMode and Block-Report Re-observation (2008–2017)

## Evidence goal

Ground the narrow claim used by Case 79:

> HDFS can recover persistent namespace identity without persisting one authoritative checkpoint of current block replica locations; DataNodes re-report their inventories after restart, and NameNode SafeMode delays ordinary mutation/replication until enough minimum-replica evidence has been re-observed.

This record does **not** attempt a full HDFS architecture history or a first-invention genealogy for safe startup modes.

---

## Source 0 — Apache Hadoop 0.18.0 exact implementation (2008)

**Type:** released primary implementation source (`P/H`).

Official release chronology: Apache Hadoop, **release 0.18.0 available**, **22 August 2008**: <https://hadoop.apache.org/release/0.18.0.html>

Exact released source: <https://github.com/apache/hadoop/blob/release-0.18.0/src/hdfs/org/apache/hadoop/dfs/FSNamesystem.java>

### Directly inspected anchors

The source-level bookkeeping comment states that:

- the valid filesystem name → block list is kept on disk/logged;
- `block -> machinelist` is **kept in memory, rebuilt dynamically from reports**.

The `datanodeMap` documentation further says the descriptor list is checkpointed in the namespace image, but only the `DatanodeInfo` portion is persistent and the list of blocks is restored from DataNode block reports.

During `FSNamesystem` initialization the implementation loads `FSImage`, creates `SafeModeInfo(conf)`, and sets the total-block denominator. The startup `SafeModeInfo(Configuration)` has a threshold, extension, minimum safe replication, `blockTotal`, `blockSafe`, and reached-state accounting. Its release-specific defaults are:

- `dfs.safemode.threshold.pct = 0.95f`;
- `dfs.safemode.extension = 0`;
- `dfs.replication.min = 1`.

The same source has a separate no-argument `SafeModeInfo()` for manual entry, uses sentinel/unreachable automatic-exit values, and exposes `isManual()` via `blockTotal == -1`.

### Supported boundaries

- `checkpointed namespace / DataNode descriptor state ≠ checkpointed block-location inventory`;
- `startup SafeMode ≠ manual SafeMode`;
- `2008 0.95 + no extension ≠ later 0.999 + 30 s defaults`;
- `released HDFS implementation floor ≠ invention priority`.

This exact source is stronger than using a later architecture rendering merely to infer what the 2008 release already did.

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

## Source 6 — Hadoop 2.8.0 `FSNamesystem.SafeModeInfo` continuity

**Type:** released primary implementation source (`P/H`).

<https://hadoop.apache.org/docs/r2.8.0/hadoop-project-dist/hadoop-hdfs/api/src-html/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.SafeModeInfo.html>

The class documentation explicitly says startup SafeMode counts safe blocks and uses threshold/extension progress for automatic exit, while manually entered SafeMode does not track safe blocks for that automatic-exit lifecycle because it is not intended to leave automatically on the startup condition.

This is a later continuity witness, not evidence that the distinction originated in 2.8.0; exact 0.18.0 source already contains a separate manual `SafeModeInfo()` state and `isManual()` discriminator.

### Consolidation note

A later repository slice accidentally created `Case 117` for the same HDFS startup-SafeMode mechanism already grounded here. Its genuinely useful additions — the exact 2008 chronology floor, manual/startup lifecycle emphasis, and cross-controls with Cases 80/83/116 — are now absorbed into canonical Case 79. The old Case-117 paths remain only as link-stability stubs.

---

## Source triangulation

The case is `grounded` because the central relation is supported at several levels:

1. **exact released 0.18.0 source (2008)** — explicitly marks block→machine location state as in-memory/report-rebuilt and already distinguishes startup from manual SafeMode;
2. **2010 system architecture paper** — location state is not in the persistent checkpoint and is re-learned from DataNodes;
3. **versioned Apache documentation** — startup SafeMode waits for reported minimum-replica evidence and postpones block replication;
4. **tag-matched 2.7.3 implementation** — the SafeMode counters, threshold/extension checks, mutation gate, and replication-queue gating are inspectable;
5. **tag-matched configuration source** — release defaults show why SafeMode `safe` cannot be normalized into `full configured redundancy`;
6. **2.8.0 source continuity** — explicitly preserves the lifecycle distinction between automatic startup SafeMode and manual entry.

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

No invention claim is made for SafeMode, startup inventory reconstruction, or replication repair. Exact released Hadoop 0.18.0 source already implements the report-rebuilt location relation and distinct startup/manual SafeMode state before the 2010 paper and later 1.x/2.x documentation used for continuity. A proper genealogy would need earlier HDFS releases plus predecessor/distributed-filesystem recovery literature.

That broader technical history belongs in `computing-archaeology` if pursued. The retention-specific contribution here is the decomposition:

`persistent namespace -> re-observed location evidence -> startup admission -> later redundancy repair`.

---

## Related-repository duplication check

Repository search found no dedicated `HDFS` or `SafeMode` treatment in `tmzncty/computing-archaeology` at the time of this slice. Therefore Case 79 does not duplicate an existing companion history. If such a history is later added, this case should link to it rather than expand into a general HDFS architecture account.

---

## Status decision

**`grounded`**.

Reason: the central claim is triangulated by exact released 0.18.0 implementation source, a contemporary 2010 system paper, versioned Apache documentation, and later tag-matched source/configuration through 2.8.0. Historical vocabulary and source boundaries are explicit, analogies are labeled, and the case does not depend on an unverified implementation assumption.
