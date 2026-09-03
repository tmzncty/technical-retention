# Case 46 grounding record — GFS master operation log, checkpoints, and restart recovery, 2003

## Status

**Grounding record for Case 46.**

Case: [`../cases/46-google-gfs-master-log-checkpoint-recovery.md`](../cases/46-google-gfs-master-log-checkpoint-recovery.md).

This record grounds a deliberately narrow metadata-retention mechanism in the Google File System as documented by Ghemawat, Gobioff, and Leung at SOSP 2003. It does **not** turn GFS into a generic model of distributed metadata recovery, and it does not claim that GFS invented logging, checkpointing, replay recovery, replicated recovery state, or logical-time ordering.

## Research question

The case tests one relation that the existing GFS integrity case does not answer:

> If the GFS master keeps its operational metadata in volatile memory, which metadata relations must survive a master crash as retained historical state, which can be reconstructed from a checkpoint and replay, and which are intentionally re-observed from chunkservers rather than persisted as master truth?

The bounded evidence shows three distinct continuity paths:

```text
volatile working metadata
    -> replicated operation-log persistence before visibility

historical mutation prefix
    -> complete checkpoint
    -> later recovery needs checkpoint + post-checkpoint suffix

current chunk locations
    -> not persisted authoritatively at master
    -> re-derived from surviving chunkservers
```

## Evidence set and role separation

### E1 — Ghemawat, Gobioff, and Leung, “The Google File System,” SOSP 2003

**Source:** Sanjay Ghemawat, Howard Gobioff, Shun-Tak Leung, “The Google File System,” *Proceedings of the 19th ACM Symposium on Operating Systems Principles*, 2003, DOI `10.1145/945445.945450`.

- Google Research record: <https://research.google/pubs/the-google-file-system/>
- Google-hosted PDF: <https://storage.googleapis.com/gweb-research2023-media/pubtools/4446.pdf>

**Role:** system-primary period evidence for the master metadata classes, operation-log durability rule, checkpoint/replay recovery, nonpersistent chunk-location policy, master-state replication, and shadow-master lag.

**Directly inspected anchors:**

- §2.6 `Metadata`;
- §2.6.1 `In-Memory Data Structures`;
- §2.6.2 `Chunk Locations`;
- §2.6.3 `Operation Log`;
- §5.1.3 `Master and Operation Log Replication`.

**Visual inspection in this research slice:**

- the PDF page containing §2.6.2–§2.6.3 was rendered and inspected directly, confirming the paragraph that GFS initially tried persistent master chunk-location information, the operation-log `historical record` / `logical time line` wording, the visibility-after-persistence rule, and checkpoint/replay behavior;
- the PDF page containing §5.1.3 was rendered and inspected directly, confirming replicated log/checkpoint state, commit-after-local-and-replica-flush, external restart of a master on another machine, and shadow-master lag/read-only semantics.

#### E1-A — metadata-class split

Section 2.6 identifies three major master metadata classes:

1. file and chunk namespaces;
2. file-to-chunk mapping;
3. locations of each chunk's replicas.

All are held in memory. Mutations of the first two are made persistent through the operation log on the local disk and replicated remotely. Chunk-location information is instead obtained from chunkservers at startup and when chunkservers join.

**Claims grounded:**

- volatile in-memory master working state;
- selective persistence rather than a persist-everything policy;
- persistent namespace/file-to-chunk mutation history;
- intentionally re-derived replica-location state.

#### E1-B — chunkserver as present-state authority for location

Section 2.6.2 says the authors initially attempted persistent chunk-location state at the master and then removed that requirement. The paper explains that chunkservers are the final authority on which chunks remain on their disks because servers can join, leave, fail, restart, be renamed, or lose chunks through disk failure.

**Claims grounded:**

- re-observation is a deliberate design choice, not an accidental omission;
- persisted historical metadata and current participant-reported location state have different authority relations;
- `important metadata` does not imply `authoritatively persisted at the master`.

#### E1-C — operation log as historical record and logical time line

Section 2.6.3 calls the operation log the `historical record of critical metadata changes` and the `only persistent record of metadata`. It also says the log defines a logical time line for concurrent operations and that files, chunks, and versions are identified by logical times of creation.

**Claims grounded:**

- the operation log retains more than unordered mutation bytes;
- ordered historical state participates in recovery/currentness/identity relations;
- GFS's own historical vocabulary includes `historical record` and `logical time line`.

**Boundary:** this wording does not make the operation log an archival institution or prove that every historical mutation must be retained indefinitely.

#### E1-D — persistence before visibility / commitment

Section 2.6.3 warns that GFS must not make metadata changes visible until they are persistent; otherwise a crash can effectively lose the whole file system or recent client operations even when chunks themselves survive. The master replicates the operation log remotely and replies to a client only after the corresponding log record is flushed locally and remotely. Several records may be batched before one flush.

Section 5.1.3 restates the rule: a mutation is considered committed only after its log record has been flushed locally and on all master replicas.

**Claims grounded:**

- payload embodiment survival and namespace/mapping recoverability are separable;
- the operation-log flush is a metadata-commit boundary;
- replicated recovery records are constitutive of the bounded commit contract;
- batching changes cost/timing without removing the durability-before-visibility relation.

#### E1-E — checkpoint plus suffix recovery

Section 2.6.3 says the master recovers file-system state by replaying the operation log, but periodically checkpoints when the log grows beyond a size threshold to keep startup time bounded. The checkpoint is stored in a compact B-tree-like form and can be mapped directly into memory for namespace lookup. The master switches to a new log and constructs the checkpoint in another thread; the completed checkpoint includes all mutations before that switch.

Recovery needs only the latest complete checkpoint and later log files. Older checkpoints/logs can then be removed, though several are retained as catastrophe protection. An incomplete checkpoint is detected and skipped.

**Claims grounded:**

- current-state reconstruction does not require indefinite retention of the entire log history;
- checkpointing is a history-prefix-to-state materialization step;
- physical checkpoint presence is weaker than recovery admissibility;
- checkpoint completion and post-checkpoint suffix retention jointly define the bounded recovery set.

#### E1-F — master replication, relocation, and shadow freshness

Section 5.1.3 says operation logs and checkpoints are replicated on multiple machines. One master remains responsible for mutations. If its machine or disk fails, external monitoring starts a new master elsewhere from the replicated log; the canonical name can be redirected.

The paper also describes `shadow` masters that provide read-only service during primary unavailability. Shadows read a replica of the growing operation log and apply the same sequence of changes, but they may lag the primary slightly, typically by fractions of a second.

**Claims grounded:**

- replicated recovery state does not imply replicated mutation authority;
- logical master-service continuity can survive physical master-host replacement;
- read availability and metadata freshness can diverge;
- durable metadata copies and current read-serving state are separate relations.

### E2 — Google Research publication record

**Source:** Google Research, “The Google File System.”

URL: <https://research.google/pubs/the-google-file-system/>

**Role:** stable institutional bibliographic anchor for the 2003 paper and authorship. It is not used as a substitute for the paper's mechanism text.

**Claims grounded:**

- paper identity and Google Research provenance;
- 2003 publication context.

### E3 — System R recovery manager, 1981

**Source:** Jim Gray, Paul McJones, Mike Blasgen, Bruce Lindsay, Raymond Lorie, Tom Price, Franco Putzolu, Irving Traiger, “The Recovery Manager of the System R Database Manager,” *ACM Computing Surveys*, 1981.

IBM Research record: <https://research.ibm.com/publications/the-recovery-manager-of-the-system-r-database-manager>

**Role:** earlier recovery prior art. The IBM abstract explicitly describes undo/redo based on records in a transaction log and a checkpoint mechanism.

**Claim grounded:**

- durable log + checkpoint crash-recovery ideas predate GFS by decades.

**Claims not grounded by E3:**

- direct historical lineage from System R to GFS;
- semantic identity between a transactional database recovery log and the GFS operation log;
- GFS use of ARIES semantics or database isolation/transaction guarantees.

### E4 — Haerder and Reuter recovery survey, 1983

**Source:** Theo Haerder and Andreas Reuter, “Principles of Transaction-Oriented Database Recovery,” *ACM Computing Surveys*, 1983.

IBM Research record: <https://research.ibm.com/publications/principles-of-transaction-oriented-database-recovery>

**Role:** earlier terminology/recovery-framework boundary. The paper treats checkpointing and logging techniques as established parts of transaction recovery analysis.

**Claim grounded:**

- by 1983, `checkpoint` and logging-based recovery were established recovery concepts, preventing a false `GFS invented checkpoint/replay` narrative.

**Scope warning:** E3/E4 are used only to bound novelty and terminology. They do not overwrite GFS's own `operation log`, `historical record`, `logical time line`, and checkpoint semantics.

## Directly grounded mechanism decomposition

### A. Working metadata can be volatile while the logical service state is recoverable

From E1:

```text
master memory
    -> fast active representation

operation log + checkpoints
    -> retained reconstruction basis
```

This supports:

> `volatile working embodiment ≠ volatile logical service state`.

The durability relation belongs to the recovery system, not to the currently executing RAM image by itself.

### B. Payload survival and namespace recoverability are different retention targets

E1 explicitly warns that metadata-history loss can lose the file system or recent operations even if chunks survive.

This supports:

> `surviving chunks ≠ recoverable file-system namespace`.

A chunk's bytes and the retained relations that make those bytes part of a named current file are distinct state classes.

### C. Replay and re-observation are different recovery operations

Namespace/file-to-chunk state is reconstructed from historical evidence. Chunk locations are reconstructed by asking surviving chunkservers what they hold now.

This supports:

> `replay recovery ≠ re-observation recovery`.

One method requires an ordered historical relation to remain; the other requires surviving components capable of reporting present state.

### D. Checkpointing makes part of retained history dispensable

Once a complete checkpoint exists, older log files no longer need to remain for ordinary recovery; the checkpoint plus later suffix is sufficient.

This supports:

> `historical record ≠ indefinite history retention`.

and:

> `current-state reconstructability ≠ complete mutation-history retention`.

The paper's term `historical record` is therefore not evidence that the operation log is intended as a permanent complete archive.

### E. Checkpoint completion is an admissibility relation

An incomplete checkpoint can physically exist but is detected and skipped during recovery.

This supports:

> `checkpoint presence ≠ recovery-admissible checkpoint`.

The bits exist, but a completion condition determines whether they may stand for current metadata state.

### F. Replication, authority, and freshness remain separate

The operation log/checkpoints are replicated. One master remains mutation authority. Shadow masters can serve reads while lagging.

This supports:

> `replica multiplicity ≠ authority multiplicity`

and:

> `metadata durability ≠ metadata freshness`.

## Counterexamples established by the evidence

### Counterexample 1 — “If chunk payload survives, the file system survives.”

Rejected.

E1 explicitly describes loss of critical metadata history as capable of losing the effective file-system state or recent operations even while chunks survive.

### Counterexample 2 — “All important master metadata must be persistently recorded.”

Rejected.

Chunk replica locations are important, yet GFS deliberately reconstructs them from chunkservers rather than maintaining a persistent authoritative master location record.

### Counterexample 3 — “A historical log must be retained forever to remain constitutive.”

Rejected.

The operation log is constitutive of commitment/recovery, but a complete checkpoint can replace the recovery need for an older log prefix.

### Counterexample 4 — “A file on disk is usable recovery state merely because it exists.”

Rejected.

Incomplete checkpoints can exist physically and be rejected as inadmissible.

### Counterexample 5 — “Replicated metadata implies replicated mutation authority.”

Rejected.

The 2003 design replicates recovery state while retaining one mutation-authoritative master.

### Counterexample 6 — “Read availability proves fresh metadata.”

Rejected.

Shadow masters can provide read-only service while slightly lagging the primary.

## Cross-case boundaries

### Case 26 — GFS inactive-chunk integrity

Case 26 asks whether a physical replica is version-current and checksum-valid and whether enough trustworthy repair sources remain. Case 46 asks whether the master can recover namespace/mapping relations and re-discover locations after its volatile working state disappears.

Therefore:

> `replica integrity/currentness ≠ metadata namespace recoverability`.

### Case 39 — GeckoFTL

Both cases show that payload survival can be insufficient without metadata recovery. GeckoFTL reconstructs controller mapping/validity state from Flash-resident metadata/checkpoints after power interruption. GFS combines replay from a replicated historical log/checkpoint with fresh observation of distributed participants.

Therefore:

> `FTL restart reconstruction ≠ distributed master metadata recovery`.

### Case 42 — Kafka log compaction

Both cases show that reconstructing current state need not preserve complete history. Kafka 0.8.1 compacts a user-visible keyed changelog; GFS checkpoints an internal metadata mutation history and can delete an old prefix once recovery closure moves to another representation.

Therefore:

> `compacted keyed changelog ≠ checkpointed metadata recovery log`.

### Case 16 — BSD FFS soft updates

Soft updates constructs dependency-safe stable metadata states without making replay from a persistent recovery log constitutive of the bounded mechanism. GFS does make an operation log central to recovering the master working state.

Therefore:

> `crash-admissible stable state ≠ replay-recovered volatile working state`.

## Terminology and prior-art boundary

Historical GFS vocabulary retained in the case:

- `operation log`;
- `historical record`;
- `logical time line`;
- `checkpoint`;
- `committed`;
- `master replicas`;
- `shadow masters`.

Project vocabulary used only for reconstruction:

- `replay recovery`;
- `re-observation recovery`;
- `re-derived location state`;
- `recovery-admissible checkpoint`;
- `retention-class split`;
- `history-prefix-to-state materialization`.

The case does **not** rename the GFS operation log into `WAL` as historical vocabulary. Earlier database WAL/logging/checkpoint systems establish prior art at the functional/recovery level only.

## Related-repository duplication check

`tmzncty/computing-archaeology` was searched in this slice for:

- `Google File System`;
- `GFS checkpoint`;
- `operation log`;
- `master metadata recovery`.

No dedicated matching case was found. A broader architectural or technical history of GFS should still be routed to `computing-archaeology`; this repository keeps only the retention-specific metadata decomposition.

## Evidence maturity and remaining limits

The case is `grounded` because its central claims rest directly on a system-primary period paper with exact section anchors and direct visual inspection of the relevant pages. The IBM sources supply an earlier prior-art boundary for logging/checkpointing.

Remaining work is deliberately outside the bounded case:

- later Colossus metadata architecture;
- independent failure-injection measurements of GFS master recovery;
- detailed external monitor/DNS implementation archaeology;
- exact ordering behavior of every GFS metadata mutation class;
- comparison with later consensus-replicated metadata services;
- broader database-WAL genealogy;
- operational field evidence beyond the 2003 design report.

None of those gaps blocks the narrower mechanism claim established here.