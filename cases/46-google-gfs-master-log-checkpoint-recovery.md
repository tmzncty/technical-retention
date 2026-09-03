# Google File System Master Metadata Recovery: Operation Log, Checkpoints, and Re-Derived Chunk Locations

## Status

**`grounded`** — bounded to the master-metadata recovery design described by Ghemawat, Gobioff, and Leung at SOSP 2003, with earlier IBM database recovery literature used only to prevent a false invention-priority claim for logging/checkpointing.

Grounding record: [`../evidence/46-gfs-2003-master-log-checkpoint-grounding.md`](../evidence/46-gfs-2003-master-log-checkpoint-grounding.md).

## Scope

This case asks a narrow question left open by the repository's earlier GFS integrity case:

> If the Google File System master keeps its working metadata in volatile memory, what must be retained across a master crash, what can instead be reconstructed from surviving participants, and when does a metadata mutation count as durable enough to become visible?

The bounded 2003 mechanism is:

```text
master working metadata in memory
        |
        +-- namespace + file->chunk mapping
        |      -> mutations appended to operation log
        |      -> log flushed locally + remotely before client-visible commitment
        |      -> periodic checkpoint materializes a recoverable state
        |      -> restart = latest complete checkpoint + later log replay
        |
        +-- chunk replica locations
               -> deliberately not retained as a persistent master record
               -> re-derived by asking chunkservers at startup / join
```

The important retention problem is therefore not simply `metadata must be persistent`. GFS deliberately gives **different metadata classes different continuity mechanisms**.

This case is **not**:

- a general history of GFS or Google storage;
- a repetition of Case 26's chunk-version/checksum/inactive-chunk verification argument;
- a claim that GFS invented operation logs, write-ahead logging, checkpoints, replicated logs, or replay recovery;
- a claim that the GFS operation log is semantically identical to a database WAL, Unix filesystem journal, Kafka user log, or consensus log;
- a claim that chunk payload bytes are stored in the master log;
- a reconstruction of later Colossus metadata architecture;
- a claim that every master datum is persisted in the same representation.

The contribution is a bounded **metadata-retention and recovery decomposition**: volatile working state, replicated mutation history, checkpoint materialization, replay suffix, intentionally nonpersistent location state, and re-observation from chunkservers.

## Relation to the earlier GFS case

[`26-google-gfs-inactive-chunk-integrity.md`](26-google-gfs-inactive-chunk-integrity.md) asks whether surviving chunk replicas are current and integrity-valid. It studies chunk version numbers, per-block checksums, demand verification, idle `scan and verify`, alternate reads, and re-replication.

Case 46 asks a different question:

```text
Case 26:
    Which surviving data replica may safely count?

Case 46:
    How can the master recover the metadata relations needed to name,
    order, and locate the surviving data after master-state loss?
```

The two cases therefore separate **payload/replica integrity** from **metadata-state recoverability**. A cluster can have intact chunks and still lose recent namespace/file-to-chunk state if the corresponding master mutation history is not retained. Conversely, the master can reconstruct current chunk locations from the chunkservers rather than retaining an authoritative persistent location table.

## Historical vocabulary

The 2003 paper directly uses:

- `metadata`;
- `file and chunk namespaces`;
- `mapping from files to chunks`;
- `locations of each chunk's replicas`;
- `operation log`;
- `historical record`;
- `logical time line`;
- `checkpoint`;
- `master replicas`;
- `committed`;
- `replay`;
- `shadow masters`;
- `stale` metadata.

The paper itself calls the operation log a **historical record of critical metadata changes** and the **only persistent record of metadata** in the bounded design. It also says the log serves as a logical time line ordering concurrent operations.

`recoverable metadata closure`, `re-derived location state`, `history-to-state materialization`, and `retention-class split` below are **project engineering terms**, not GFS historical vocabulary.

## Historical record

### H/P — all master metadata is in memory, but only selected classes are persistently logged

Section 2.6 divides master metadata into three major types:

1. file and chunk namespaces;
2. file-to-chunk mapping;
3. current replica locations.

All are kept in master memory. The first two are also made persistent by logging mutations to an operation log stored on the master's local disk and replicated on remote machines.

The third class is deliberately different: the master does **not** keep chunk-location information persistently. At startup it asks chunkservers what chunks they actually hold.

This immediately rejects a simple rule:

> **important control state ≠ one universal persistence mechanism**.

**Primary anchor:** Ghemawat, Gobioff, and Leung 2003, §§2.6–2.6.2.

### H/P — the operation log is both retained history and an ordering relation

Section 2.6.3 calls the operation log a historical record of critical metadata changes and says it serves as a logical time line defining the order of concurrent operations. Files, chunks, and versions are identified by the logical times at which they were created.

The log therefore does more than retain bytes describing past mutations. In the bounded design, its order participates in the identity/currentness relation through which later master state is reconstructed.

**Primary anchor:** §2.6.3.

### H/P — metadata mutations are not made visible before their log records are persistent

The same section states that GFS must not make changes visible to clients until the corresponding metadata changes have been made persistent. The authors give the failure consequence explicitly: otherwise the system can effectively lose the whole file system or recent client operations even when the chunks themselves survive.

The operation log is therefore replicated on remote machines, and the master responds to a client operation only after the corresponding log record has been flushed to disk locally and remotely. Several log records may be batched before flush.

Section 5.1.3 restates the rule at the master-replication layer: a mutation is considered committed only after its log record has been flushed locally and on all master replicas.

**Primary anchors:** §§2.6.3, 5.1.3.

### H/P — recovery is checkpoint plus later log replay, not replay of an indefinitely growing history

The master recovers file-system state by replaying the operation log. To bound startup work, it checkpoints state when the log grows beyond a certain size.

The checkpoint is stored in a compact B-tree-like form that can be mapped directly into memory for namespace lookup. The master switches to a new log file and constructs the checkpoint in a separate thread; that checkpoint contains all mutations before the switch.

When complete, the checkpoint is written both locally and remotely. Recovery needs only:

```text
latest complete checkpoint
    +
subsequent log files
```

Older checkpoints and log files can then be deleted, although the paper says several are retained as protection against catastrophe. An incomplete checkpoint is detected and skipped.

**Primary anchor:** §2.6.3.

### H/P — persistent chunk-location metadata was tried and rejected

Section 2.6.2 is unusually explicit about the design history. The authors say they initially tried to keep chunk-location information persistently at the master, then chose instead to request it from chunkservers at startup and periodically thereafter.

Their reason is not that location is unimportant. It is that chunkservers are the final authority about what chunks physically remain on their disks, while servers can join, leave, fail, restart, change names, or lose chunks because of disk failure.

This is a period-primary example of **re-observation replacing persisted authority** for one metadata class.

**Primary anchor:** §2.6.2.

### H/P — master-state replication and shadow reads add a separate availability/currentness relation

Section 5.1.3 says the operation log and checkpoints are replicated on multiple machines. If the primary machine or disk fails, monitoring infrastructure outside GFS starts a new master process elsewhere using the replicated operation log.

`Shadow` masters provide read-only service while the primary is unavailable, but the paper explicitly says they may lag the primary slightly. A shadow reads a replica of the growing operation log and applies the same sequence of changes to its own structures.

Therefore:

> **metadata durability ≠ read-copy freshness**.

A shadow can increase read availability while still being a slightly stale metadata observer.

**Primary anchor:** §5.1.3.

## Retained state

The bounded design contains several different state classes:

1. **namespace state** — paths, names, and namespace mutations;
2. **file-to-chunk mapping** — relation from logical file structure to immutable chunk handles;
3. **logical creation/order state** — operation-log ordering used to identify files/chunks/versions and order metadata mutations;
4. **checkpoint state** — materialized master state sufficient to replace replay of an older history prefix;
5. **post-checkpoint log suffix** — critical mutations that occurred after the checkpoint boundary;
6. **chunk replica locations** — operationally important but intentionally not persisted as an authoritative master record;
7. **chunkserver-reported physical possession** — re-observed state used to reconstruct current locations;
8. **shadow-master applied-log position** — enough derived state to provide read-only metadata service while possibly lagging the primary.

The chunk payload itself remains on chunkservers and is not the object stored in the master operation log.

## Retention mechanism

### 1. Working state is volatile for speed

The master keeps metadata in memory so operations and full-state scans are fast. Volatility at the working layer is deliberate rather than an accidental omission.

### 2. Critical mutation history crosses a persistence boundary before visibility

For namespace/file-to-chunk state, the retained relation is:

```text
metadata mutation
    -> operation-log record
    -> local + remote durable flush
    -> mutation may count as committed / become client-visible
```

This is a **visibility-gated durability relation**, not merely a periodic backup.

### 3. Checkpointing converts a history prefix into a current-state representation

When the log becomes large, the master materializes a checkpoint. Once a complete checkpoint exists, recovery no longer needs the older log prefix.

This is the central retention transition:

```text
history prefix + old materialized state
    -> checkpoint
    -> older recovery history becomes dispensable
```

The system preserves the ability to reconstruct the current metadata state while deliberately reducing how much historical sequence must remain.

### 4. Some state is recovered by replay; other state is recovered by observation

GFS does **not** reconstruct every master datum from the log/checkpoint pair. Chunk locations come from current chunkserver reports.

Thus restart composes two epistemically different operations:

```text
retained historical evidence
    -> replay authoritative namespace/mapping state

surviving distributed participants
    -> re-observe current chunk locations
```

This gives the case one of its strongest distinctions:

> **replay recovery ≠ re-observation recovery**.

### 5. Replication protects the recovery record, while one master retains mutation authority

Copies of the operation log/checkpoints exist on multiple machines, but the 2003 design keeps one master process in charge of mutations. Replica multiplicity of recovery state therefore does not imply multiple concurrent mutation authorities.

## Addressing and recovery geometry

A bounded restart path is:

```text
latest complete checkpoint
    -> map checkpoint into master memory
    -> replay later operation-log records in order
    -> recover namespace + file-to-chunk relations

chunkserver inventory reports
    -> reconstruct chunk-handle -> current-replica-location relations

canonical master name / external monitoring
    -> redirect service to restarted or relocated master process
```

The result is a master state assembled from **retained representations plus renewed observations**.

## Read / write semantics

### Metadata mutation

The bounded persistence rule applies to metadata mutations: visibility/commitment is gated on durable operation-log state. The paper permits batching several records before flushing, so persistence work can be amortized without changing the ordering relation.

### Metadata read through shadow masters

Shadow masters apply the same operation sequence from a replicated growing log but can lag. They therefore extend read availability without becoming mutation authorities or perfectly fresh mirrors.

### Data read/write

This case does not reconstruct the full GFS data-mutation protocol. Case 26 handles a separate retained relation around chunk-version and integrity validity; other parts of the 2003 paper handle leases, mutation ordering, and record append.

## Time

Several timescales coexist:

- immediate in-memory master operation time;
- log-flush/replication delay before metadata commitment and client response;
- batched flush intervals;
- log-growth interval before checkpoint creation;
- checkpoint construction time — the paper reports roughly a minute for a cluster with a few million files;
- restart replay time from checkpoint plus suffix;
- chunk-location re-discovery time after restart;
- shadow-master lag — described as typically fractions of a second;
- long-term retention of a few older checkpoints/log files as catastrophe protection.

These are not one `persistence latency`.

## Maintenance and labor

The apparently stable namespace depends on:

- operation-log append and ordered flush;
- remote replication of recovery state;
- checkpoint construction;
- completion validation and rejection of incomplete checkpoints;
- log/checkpoint reclamation;
- startup replay;
- chunkserver inventory polling;
- HeartBeat/state collection;
- external monitoring capable of starting a new master process elsewhere;
- DNS/canonical-name reassignment when the master moves;
- shadow-master log following.

The paper also leaves visible human/infrastructure assumptions: server renaming and machine/disk failure are real events, while external monitoring and naming infrastructure participate in recovery.

> **master-state persistence ≠ self-sufficient persistence inside one master process**.

## Failure / forgetting modes

Keep distinct:

- **volatile master-memory loss** — ordinary process/machine loss destroys the working representation;
- **unpersisted recent metadata mutation** — if visibility outran log persistence, recent operations could be lost despite surviving chunks; GFS's commit rule is designed to prevent this;
- **loss of recovery-record replicas** — reduces or defeats the ability to reconstruct authoritative master state;
- **incomplete checkpoint** — physically present but not admissible for recovery and therefore skipped;
- **unbounded operation log** — can preserve history but make restart too slow; checkpointing converts part of that history into a compact recovery state;
- **stale persisted chunk-location table** — the design avoids treating this as authoritative by re-deriving locations from chunkservers;
- **shadow-master lag** — read-only availability can exist with slightly stale metadata;
- **surviving chunks without sufficient namespace/mapping history** — payload embodiments can remain while the relations needed to expose them through the file system are lost;
- **participant disappearance** — a chunkserver can no longer report a replica that vanished through disk failure or disablement.

These are different failures of retention, currentness, and availability.

## Engineering reconstruction

### E — payload survival does not imply namespace recoverability

The authors explicitly say that losing critical metadata history can effectively lose the file system or recent operations even if chunks survive.

Therefore:

> **surviving chunks ≠ recoverable file-system namespace**.

The payload and the relations that make it an addressable current file are separate retention targets.

### E — volatile working state can participate in a durable service

The master deliberately keeps all metadata in memory, but selected mutation history/checkpoints exist outside that volatile embodiment.

Therefore:

> **volatile current embodiment ≠ volatile logical service state**.

Durability can belong to a recovery relation rather than to the currently active representation.

### E — persistent control state does not have to include every control datum

Chunk locations are essential for service but intentionally excluded from the persistent master record.

Therefore:

> **important metadata ≠ necessarily persistently recorded metadata**.

A datum can be retained operationally by making it **re-observable** from surviving components rather than by storing one authoritative historical copy.

### E — replay recovery and re-observation recovery are distinct

Namespace/mapping state is reconstructed from retained mutation history and checkpoint state. Location state is reconstructed by interrogating the current distributed substrate.

Therefore:

> **replayable relation ≠ re-discoverable relation**.

The distinction matters because one can survive only if its historical ordering evidence survives, while the other can survive if the underlying participants remain able to report present reality.

### E — a historical log can be constitutive without being an archive

The operation log is historically described as a `historical record`, yet old log files can be discarded after a complete checkpoint plus newer suffix is sufficient for recovery.

Therefore:

> **historical record ≠ indefinite history retention**.

And:

> **current-state reconstructability ≠ retention of the complete mutation sequence**.

This resembles Case 42's distinction between current-state reconstruction and complete history only at a functional level; the mechanisms are different.

### E — checkpoint completion is an admissibility boundary

An incomplete checkpoint may physically exist but recovery detects and skips it.

Therefore:

> **checkpoint presence ≠ recovery-admissible checkpoint**.

Completion status changes whether a retained representation may count as the basis of current state.

### E — replicated recovery state does not eliminate singular mutation authority

Operation logs/checkpoints are copied across machines, while one master remains responsible for mutations.

Therefore:

> **replica multiplicity ≠ authority multiplicity**.

This echoes a broader distributed-retention lesson without claiming protocol identity with RADOS, Dynamo, or consensus systems.

### E — read availability and metadata freshness can diverge

Shadow masters can answer read-only metadata requests while lagging the primary.

Therefore:

> **read availability ≠ metadata freshness**.

That lag is a bounded permitted state of the 2003 architecture, not evidence that all stale metadata is acceptable for mutation authority.

## Functional analogies and limits

### A — Case 39 GeckoFTL metadata recovery

Both cases show that surviving payload media are insufficient if the metadata relation needed to recover logical identity disappears.

The mechanisms differ sharply:

- GeckoFTL reconstructs controller mapping/validity relations after power failure from Flash-resident metadata, checkpoints, and surviving runs;
- GFS reconstructs namespace/mapping state from a replicated operation log/checkpoint and separately re-derives chunk locations from remote chunkservers.

`FTL restart reconstruction ≠ distributed master recovery`.

### A — Case 42 Kafka log compaction

Both cases reject `current state requires complete retained history`.

Kafka 0.8.1 compacts the user-visible keyed changelog while preserving permanent logical offsets and at least the last value per key. GFS uses an internal master operation log as recovery/ordering metadata and can retire an old history prefix after checkpoint materialization.

`compacted user changelog ≠ master metadata recovery log`.

### A — Case 16 BSD FFS soft updates

Soft updates deliberately construct crash-admissible on-disk metadata **without** requiring a persistent recovery log for the bounded mechanism. GFS instead makes its operation log central to reconstructing volatile master metadata.

The comparison therefore sharpens:

> **crash-admissible stable state ≠ replay-recovered volatile working state**.

### A — Case 26 GFS inactive-chunk integrity

Case 26 qualifies which payload replicas are current and integrity-valid; Case 46 qualifies which retained/reconstructed metadata makes those replicas addressable through a recovered master.

Neither mechanism substitutes for the other.

## Prior art and anti-anachronism

This case makes **no claim that GFS invented logging or checkpointing**.

Earlier database systems already used durable logs and checkpoints for crash recovery. IBM's 1981 System R recovery-manager account describes transaction undo/redo based on records in a transaction log and a checkpoint mechanism. Haerder and Reuter's 1983 recovery survey explicitly treats `checkpoint` and logging techniques as established recovery vocabulary and classification dimensions. ARIES later developed a much richer write-ahead-logging recovery method.

Those systems are used here only as a **prior-art boundary**:

```text
logging/checkpoint recovery existed earlier
    !=
GFS operation-log/checkpoint semantics are historically derived from,
identical to, or reducible to one database recovery protocol
```

The bounded historical claim is narrower:

> In the 2003 GFS design, selected master metadata mutations are retained in a replicated operation log before commitment; checkpoints bound replay; incomplete checkpoints are rejected; and chunk-location state is intentionally re-derived from chunkservers instead of persistently authoritative at the master.

The terms `operation log`, `historical record`, `logical time line`, `checkpoint`, `master replicas`, and `shadow masters` remain the paper's vocabulary.

## Philosophical / media-theoretical interpretation

The technical fact creating the conceptual problem is precise: GFS needs a historical mutation sequence to reconstruct current metadata, but it does **not** need to retain the entire sequence forever. Once a complete checkpoint exists, an older log prefix may be discarded without destroying the current namespace.

That pressures a simple equation between technical memory and archive.

A narrow interpretation is:

> A technical system can retain history **instrumentally** as a means of producing a later admissible present, then forget part of that history once another representation preserves the required continuity.

A second pressure comes from chunk locations. GFS can intentionally refuse to remember an authoritative historical location table and instead ask the surviving world again.

> Technical retention can combine **remembered relations** with **renewed observation**.

The interpretation stops there. The GFS authors are not attributed a theory of human memory, archival forgetting, or Heideggerian/Stieglerian temporality. `Historical record` in the paper is an engineering term for the operation log, not automatically an archive-theory category.

## Counterexamples and limits

This case does **not** establish that:

- all GFS metadata is persistently logged in identical form;
- chunk locations are unimportant merely because they are re-derived;
- the operation log contains chunk payload bytes;
- every durable metadata representation is immediately current on every shadow master;
- a physically present incomplete checkpoint is safe to use;
- a checkpoint preserves the complete historical mutation sequence it replaces;
- the GFS operation log has the same transaction semantics as ARIES/WAL;
- GFS invented logs, checkpoints, replay recovery, replication, or logical time;
- later Google distributed filesystems retain identical master architecture;
- preserving a few old checkpoints/logs for catastrophe protection turns the bounded operation log into a complete archival history.

## Cross-case result

Case 46 adds a distributed metadata-recovery decomposition that was previously only implicit:

```text
working-state speed
    -> volatile in-memory master metadata

metadata commitment
    -> replicated persistent operation-log record

recovery history growth
    -> checkpoint materialization

restart
    -> latest complete checkpoint + later log replay

physical replica location
    -> not one persistent master truth
    -> re-observed from chunkservers

read availability
    -> shadow master may serve while slightly stale
```

This forces at least these distinctions:

- `payload survival ≠ namespace recoverability`;
- `volatile working embodiment ≠ volatile logical service state`;
- `important metadata ≠ persist-everything metadata`;
- `replay recovery ≠ re-observation recovery`;
- `historical record ≠ indefinite history retention`;
- `checkpoint presence ≠ checkpoint admissibility`;
- `replica multiplicity ≠ authority multiplicity`;
- `metadata durability ≠ metadata freshness`.

## Claim ledger

| Claim | Label | Evidence / status |
| --- | --- | --- |
| GFS master keeps namespace, file-to-chunk mapping, and chunk-location metadata in memory | H/P | GFS 2003 §2.6 |
| namespace and file-to-chunk mutations are persisted through a local + remotely replicated operation log | H/P | §§2.6, 2.6.3 |
| chunk locations are intentionally not persistently recorded at the master and are queried from chunkservers | H/P | §2.6.2 |
| the operation log is called a historical record and logical time line | H/P | §2.6.3 |
| client-visible metadata commitment waits for local/remote durable log flush | H/P | §§2.6.3, 5.1.3 |
| recovery loads the latest complete checkpoint and replays only later log files | H/P | §2.6.3 |
| checkpoint creation switches to a new log and proceeds without blocking incoming mutations | H/P | §2.6.3 |
| incomplete checkpoints are detected and skipped | H/P | §2.6.3 |
| older checkpoints/log files can be deleted after a sufficient checkpoint+suffix exists | H/P | §2.6.3 |
| operation log/checkpoints are replicated; external monitoring can restart the master elsewhere from the replicated log | H/P | §5.1.3 |
| shadow masters can provide read-only service while slightly lagging primary metadata | H/P | §5.1.3 |
| surviving chunks do not by themselves preserve the namespace/mapping relation | H/P/E | explicit failure warning in §2.6.3 |
| replay recovery and chunk-location re-observation are separate continuity mechanisms | E | reconstruction from §§2.6.2–2.6.3 |
| a historical recovery log can be constitutive without being an indefinite archive | E/A | old log deletion after checkpoint; project comparison |
| GFS invented log/checkpoint recovery | X | contradicted by pre-2003 recovery literature |
| GFS operation log is simply ARIES/WAL under another name | X | unsupported; only a functional prior-art comparison is made |

## Sources

### Primary GFS source

Sanjay Ghemawat, Howard Gobioff, Shun-Tak Leung, **“The Google File System,”** *Proceedings of the 19th ACM Symposium on Operating Systems Principles (SOSP)*, 2003, pp. 29–43 in the ACM publication record, DOI `10.1145/945445.945450`.

- Google Research record: <https://research.google/pubs/the-google-file-system/>
- Google-hosted PDF: <https://storage.googleapis.com/gweb-research2023-media/pubtools/4446.pdf>
- bounded anchors: §§2.6, 2.6.1, 2.6.2, 2.6.3, 2.7.1, and 5.1.3;
- direct visual inspection in this research slice: PDF page containing §2.6.2–2.7.1 and PDF page containing §5.1.3.

### Earlier recovery prior art

Jim Gray, Paul McJones, Mike Blasgen, Bruce Lindsay, Raymond Lorie, Tom Price, Franco Putzolu, Irving Traiger, **“The Recovery Manager of the System R Database Manager,”** *ACM Computing Surveys*, 1981.

- IBM Research record: <https://research.ibm.com/publications/the-recovery-manager-of-the-system-r-database-manager>
- used only to establish that transaction-log + checkpoint recovery predates GFS.

Theo Haerder and Andreas Reuter, **“Principles of Transaction-Oriented Database Recovery,”** *ACM Computing Surveys*, 1983.

- IBM Research record: <https://research.ibm.com/publications/principles-of-transaction-oriented-database-recovery>
- used only as an earlier terminology/recovery-framework boundary for checkpointing and logging.

### Repository controls

- [`26-google-gfs-inactive-chunk-integrity.md`](26-google-gfs-inactive-chunk-integrity.md) — same 2003 system, separate chunk currentness/integrity mechanism.
- [`39-geckoftl-power-failure-metadata-recovery.md`](39-geckoftl-power-failure-metadata-recovery.md) — controller metadata reconstruction after interruption.
- [`42-apache-kafka-log-compaction-delete-marker-retention.md`](42-apache-kafka-log-compaction-delete-marker-retention.md) — current-state reconstructability without complete history, through a different log mechanism.
- [`16-bsd-ffs-soft-updates-crash-admissibility.md`](16-bsd-ffs-soft-updates-crash-admissibility.md) — crash-consistency counterexample that does not depend on replaying a persistent recovery log in the bounded mechanism.

### Related-repository duplication check

`tmzncty/computing-archaeology` was searched in this slice for `Google File System`, `GFS checkpoint`, `operation log`, and master-metadata recovery. No dedicated matching case was found. A broader GFS architecture/history should still be routed there rather than expanded here.

## Status rationale

**`grounded`**

The central claims rest on one system-primary period paper whose relevant pages and sections were directly inspected, including the exact metadata-class split, operation-log visibility rule, checkpoint/replay boundary, incomplete-checkpoint handling, deliberate non-persistence of chunk locations, master-log replication, and shadow-master lag. Earlier IBM recovery literature blocks a false invention-priority claim without being used to rewrite GFS's own vocabulary or mechanism.