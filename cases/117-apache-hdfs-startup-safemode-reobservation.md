# Apache HDFS Startup Safemode: Namespace Recovery, Block Re-observation, and Withheld Mutation Authority

## Status

**`grounded`** — bounded to the Apache HDFS startup Safemode relation documented in the 2008-era architecture record, Hadoop 1.0.4 user/configuration documentation, and Hadoop 2.8.0 NameNode source. This case does not claim that HDFS invented startup quiescence, storage-service recovery gates, replica re-observation, or read-only recovery modes.

Grounding record: [`../evidence/117-hadoop-2008-2017-startup-safemode-grounding.md`](../evidence/117-hadoop-2008-2017-startup-safemode-grounding.md).

## Scope

HDFS can retain two very different things across a NameNode restart:

1. namespace and block-to-file metadata persisted through `FsImage` and `EditLog`;
2. HDFS block payloads already present on DataNode storage.

Yet startup does not immediately imply ordinary mutation, deletion, or replication authority. The NameNode enters `Safemode`, rebuilds namespace state, receives DataNode `Heartbeat` / `Blockreport` information, counts blocks that have checked in with a minimum number of replicas, and only later leaves the startup gate.

This case asks:

> **If namespace metadata and DataNode payloads survive a NameNode restart, why does HDFS deliberately withhold mutation and replication authority until it has re-observed enough block embodiments?**

The bounded regime includes:

- `FsImage` + `EditLog` namespace recovery;
- DataNode startup block scanning and `Blockreport` re-observation;
- `safe blocks` and minimum-replication qualification;
- startup Safemode as a read-only / no-replication interval;
- configurable safe-block threshold and extension;
- the distinction between automatic startup Safemode and manually entered Safemode;
- post-Safemode identification of still-under-replicated blocks.

It does **not** attempt a general HDFS startup/recovery history, NameNode HA/failover analysis, erasure-coded recovery study, resource-low Safemode study, or fault-injection campaign.

---

## Historical vocabulary

The inspected Apache sources directly use:

- `Safemode` / `safe mode`;
- `safe blocks` / `safely replicated`;
- `minimal number of replicas` / minimum replication;
- `Heartbeat`;
- `Blockreport`;
- `FsImage` / `fsimage`;
- `EditLog` / `edits`;
- `threshold`;
- `extension`;
- `safeReplication`;
- `blockSafe` / `blockTotal`;
- `reached`;
- manually entered safe mode;
- replication / under-replication.

The following are **project engineering terms**, not Apache historical quotations:

- `re-observation`;
- `service-admission gate`;
- `withheld mutation authority`;
- `reported embodiment evidence`;
- `recovery channel`;
- `retained-but-not-yet-admitted state`.

---

## Historical record

### H/P — an open 2008 HDFS record already documents startup Safemode

Apache records Hadoop 0.18.0 as released on **22 August 2008**. The HDFS architecture documentation from this period describes startup Safemode as a distinct NameNode state in which block replication does not occur while Heartbeats and Blockreports arrive.

That is a defensible public HDFS chronology floor only:

> **2008 released HDFS Safemode evidence ≠ invention priority for recovery gates or read-only startup modes.**

This case makes no broader origin claim.

### H/P — namespace recovery and replica-location recovery use different evidence channels

The architecture guide says the NameNode persists the file-system namespace using `FsImage` and `EditLog`. At startup it reads the image and log, applies logged transactions to the in-memory namespace representation, and writes a new image.

The same documentation gives a different path for DataNode holdings. Each DataNode stores HDFS blocks locally, scans its local filesystem at startup, constructs a list of its blocks, and sends a `Blockreport` to the NameNode.

So the bounded HDFS restart relation already separates:

```text
namespace / block-to-file relation
    <- replay retained FsImage + EditLog

current block-location relation
    <- re-observe DataNode block holdings through Blockreports
```

The first is recovery from retained historical metadata; the second is renewed observation of surviving distributed embodiments.

### H/P — Safemode deliberately suppresses replication while block evidence arrives

The 2008-era architecture guide states that on startup the NameNode enters Safemode, does not replicate blocks, and receives Heartbeats and Blockreports. A block becomes `safely replicated` for this startup calculation after its specified minimum number of replicas has checked in.

Hadoop 1.0.4 states the reason even more explicitly: the NameNode waits for DataNodes to report their blocks so that it does not begin replication prematurely when enough replicas may already exist in the cluster.

Therefore:

> **withheld repair can itself be a retention-protecting action when the controller's current replica knowledge is incomplete.**

The system is not assuming that missing reports mean missing payloads.

### H/P — startup Safemode is essentially read-only in the bounded 1.0.4 guide

The Hadoop 1.0.4 HDFS Users Guide describes Safemode during startup as essentially read-only and says the NameNode does not allow modifications to the file system or blocks during that interval.

This gives a direct split:

```text
retained namespace / readable state
    !=
ordinary mutation authority
```

The payload may be present and the namespace may be reconstructable while the service intentionally withholds state-changing operations.

### H/P — `safe` is a minimum-replica admission relation, not proof of full redundancy restoration

The architecture guide says a block is considered safely replicated after its **minimum** number of replicas has checked in. After the configurable fraction of safe blocks has checked in and the additional delay has passed, the NameNode leaves Safemode and then determines which blocks still have fewer than their specified replication factor and replicates them.

Thus the startup predicate cannot be inflated into:

```text
safe block == fully restored configured replication == integrity verified == placement verified
```

Those are different relations.

### H/P — Hadoop 1.0.4 makes the startup gate quantitatively explicit

Hadoop 1.0.4 `hdfs-default.html` publishes:

- `dfs.replication.min = 1`;
- `dfs.safemode.threshold.pct = 0.999f`;
- `dfs.safemode.extension = 30000` milliseconds.

The threshold description says it is the percentage of blocks that must satisfy the minimal replication requirement. Values above 1 make Safemode permanent in that configuration contract; the extension is time retained after the threshold is reached.

These are **release-bounded defaults**, not universal HDFS constants.

### H/P — threshold attainment and Safemode exit remain distinct states

The Hadoop 2.8.0 `FSNamesystem.SafeModeInfo` source retains explicit state for:

- `threshold`;
- minimum live-DataNode threshold;
- `extension`;
- `safeReplication`;
- `blockTotal`;
- `blockSafe`;
- the time `reached` when the threshold was attained.

Its class documentation says that reaching the safe-block ratio starts a monitor which waits for the extension before Safemode is left.

Therefore:

> **threshold reached ≠ admission transition complete.**

The service can retain evidence that the threshold was reached while still intentionally remaining inside the startup gate.

### H/P — automatic startup Safemode and manual Safemode are not one lifecycle

The Hadoop 2.8.0 source explicitly says that during startup the safe-block count is tracked for automatic exit. If Safemode is entered manually, that count is not tracked for the same purpose because the NameNode is not intended to leave automatically on the startup condition.

So:

> **startup Safemode ≠ manual Safemode.**

They share a service state name but not the same exit authority or retained progress relation.

---

## Retained state

At least seven state classes must remain distinct.

### 1. DataNode block payload

The bytes embodied in the local block files held by DataNodes.

### 2. Namespace and block-to-file metadata

`FsImage` plus `EditLog` preserve the namespace/history needed to reconstruct the NameNode's file-system metadata view.

### 3. Current block-location observations

Blockreports tell the restarted NameNode which DataNodes currently claim each HDFS block. In the bounded architecture these holdings are re-observed rather than recovered solely from the namespace image.

### 4. Safe-block count

`blockSafe` summarizes how much of the namespace's block population has reached the startup minimum-replica check-in condition.

### 5. Total-block denominator

`blockTotal` is retained/derived control state needed to interpret the safe-block ratio.

### 6. Admission policy

The safe replication minimum, block-percentage threshold, minimum live-DataNode condition in later source, and extension define when startup may proceed.

### 7. Threshold/extension progress

The `reached` time and extension distinguish `condition has become true` from `the service has already left Safemode`.

None of these control states is the user payload itself.

---

## Engineering reconstruction

### Recovery can compose replay and re-observation without treating them as the same operation

HDFS restart uses at least two reconstruction logics:

```text
retained historical metadata
    -> replay / merge
    -> reconstructed namespace

surviving distributed embodiments
    -> current reports
    -> reconstructed location knowledge
```

A system can therefore preserve one part of its identity by durable historical inscription and another part by asking the surviving world what is still there.

> **replay recovery ≠ re-observation recovery.**

### Physical payload survival is weaker than controller knowledge of where it is

A DataNode can still contain a valid block before its first post-restart Blockreport has been incorporated by the NameNode. In that interval:

> **payload survival ≠ NameNode knowledge of payload location.**

Conversely, a namespace record saying a block should exist does not manufacture a surviving block embodiment.

### Safemode protects against acting too strongly on incomplete observations

A naïve controller could see few currently reported replicas and immediately create replacements. HDFS instead waits because additional DataNodes may soon report already-existing copies.

This makes temporary non-action meaningful:

> **not repairing yet can preserve placement/capacity efficiency and avoid unnecessary replica creation while evidence is incomplete.**

That is not equivalent to saying replication is unnecessary; after the observation gate closes, ordinary under-replication work resumes.

### Startup `safe` is an admission predicate, not a complete health predicate

The startup relation answers a narrow question:

> Has enough of the block population checked in at the configured minimum-replica level for the NameNode to leave the startup gate?

It does not by itself answer:

- are all blocks available?
- is every file fully replicated at its configured factor?
- are replicas distributed across the desired racks?
- has every replica recently passed checksum verification?
- has every later mutation path reached its own durability boundary?

That distinction is central to the repository's use of the word `qualified`.

### A read-only state can retain service value while withholding future-state authority

Safemode demonstrates that availability is typed. A recovered namespace and surviving block set may support some observation/read behavior while write, deletion, and replication authority remain withheld.

Therefore:

> **retained / readable ≠ mutable.**

This is an engineering distinction. It is not evidence that HDFS actors were formulating a philosophical theory of availability.

---

## Read, write, repair, and forgetting

### Reads

The bounded 1.0.4 guide describes Safemode as essentially read-only. Readability is therefore compatible with temporarily withheld mutation authority.

### Writes / namespace mutation

File-system and block modifications are suppressed during the startup gate in the inspected guide.

### Replication

Replication is deliberately suppressed while block reports accumulate. After exit, the NameNode identifies blocks still below their specified replication requirement and schedules replication.

### Deletion

Later HDFS command documentation describes Safemode as not replicating or deleting blocks. Even when deletion is withheld, this is a temporary service-policy condition:

> **withheld deletion ≠ WORM media ≠ secure retention ≠ permanent undeletability.**

### Forgetting

Loss of `FsImage`/`EditLog`, loss of a DataNode block, failure of a DataNode to report, and temporary Safemode withholding are not one kind of forgetting. A physically surviving but unreported block differs from a destroyed block, just as a retained namespace record differs from a currently observed embodiment.

---

## Cross-case comparison

### Case 80 — decommission / rack placement

Case 80 already shows that live-replica count and placement-policy satisfaction are distinct. Case 117 therefore does not treat the Safemode minimum-replica check-in count as evidence that the rack/failure-domain placement relation is already fully qualified.

> **startup safe-block count ≠ decommission/placement admissibility.**

### Case 83 — DataNode block scanner

Case 83 separates replica presence from checksum/integrity qualification. A replica that has checked in enough to contribute to startup `blockSafe` is not thereby proven recently scrubbed or checksum-qualified.

> **reported/safe replica ≠ integrity-qualified replica.**

### Case 116 — DataNode maintenance state

Both cases contain retained administrative/service-admission state, but their scopes differ:

- Case 117: cluster/NameNode startup gate while replica-location evidence is rebuilt;
- Case 116: per-DataNode temporary-withdrawal regime with a retained expiry and relaxed redundancy condition.

This is a bounded functional comparison only.

> **startup Safemode ≠ DataNode maintenance mode.**

No implementation genealogy is inferred from the comparison.

---

## Philosophical interpretation

The case sharpens one narrow availability problem.

A technical state can be materially present and historically reconstructable yet not be admitted to every current operation. In HDFS startup, availability depends not only on payload survival but also on whether the NameNode has reconstructed enough relations to authorize ordinary mutation and repair.

That can discipline a philosophical discussion of technical availability or orderability, but the limit is strict:

> **Safemode is not a definition of `Bestand`, and HDFS startup control state is not automatically `tertiary retention`.**

The historical/engineering facts stand independently of either philosophical vocabulary.

---

## Counterexamples and limits

This case does **not** establish:

- that 2008 is the invention date of Safemode-like recovery gating;
- that every HDFS release uses the same default threshold or extension;
- that a safe block has its full configured replication factor;
- that a safe block satisfies rack/failure-domain placement policy;
- that a safe block has passed a recent checksum scan;
- that Blockreport is the only modern HDFS source of replica state;
- that manual, resource-low, HA standby, upgrade, or administrator-forced Safemode has the same lifecycle as startup Safemode;
- that withheld deletion means physical erasure can never occur later;
- that startup recovery proves all DataNode media embodiments are physically healthy;
- that the bounded HDFS mechanism descends from any specific earlier distributed filesystem.

---

## Related repositories

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated HDFS Safemode case to reuse.

Broader work on:

- HDFS startup/recovery genealogy;
- GFS/HDFS implementation history;
- NameNode HA and standby reconstruction;
- Blockreport protocol evolution;
- recovery-gate design across distributed filesystems;

belongs primarily in `computing-archaeology` if developed. This case keeps only the retention-specific relation among persisted namespace, surviving block payloads, re-observed locations, and withheld mutation authority.

---

## Sources

Primary / official Apache sources:

- Apache Hadoop, **release 0.18.0 available**, 22 August 2008: <https://hadoop.apache.org/release/0.18.0.html>.
- Apache Hadoop, **HDFS Architecture Guide**, Safemode / file-system metadata persistence / DataNode local-storage sections: <https://hadoop.apache.org/docs/r1.2.1/hdfs_design.html>.
- Apache Hadoop 1.0.4, **HDFS Users Guide**, Safemode and checkpoint/startup sections: <https://hadoop.apache.org/docs/r1.0.4/hdfs_user_guide.html>.
- Apache Hadoop 1.0.4, **HDFS default configuration**, `dfs.replication.min`, `dfs.safemode.threshold.pct`, `dfs.safemode.extension`: <https://hadoop.apache.org/docs/r1.0.4/hdfs-default.html>.
- Apache Hadoop 2.8.0, **`FSNamesystem.SafeModeInfo` source**, startup safe-block counting, threshold, extension, manual-mode distinction: <https://hadoop.apache.org/docs/r2.8.0/hadoop-project-dist/hadoop-hdfs/api/src-html/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.SafeModeInfo.html>.

## Evidence debt

Still open:

- pre-2008 HDFS Safemode proposal/commit genealogy;
- exact transition semantics across 0.18→1.x→2.x→3.x;
- HA active/standby and edit-tail interactions;
- erasure-coded HDFS startup qualification;
- resource-low and force-exit Safemode as separate regimes;
- exact persistence/crash semantics of startup progress counters;
- fault injection showing late Blockreports versus premature replication;
- production incident evidence;
- cross-filesystem prior-art genealogy.
