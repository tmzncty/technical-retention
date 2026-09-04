# Google Bigtable Tablet Recovery: Commit Log, Memtable, SSTable Compaction, and Redo Points

## Scope

- **Bounded system:** Google Bigtable as described by Chang et al. at OSDI 2006, with production use reported from April 2005 and the published implementation description treated as the principal historical artifact.
- **Bounded mechanism:** tablet-server mutation commit to a GFS-backed commit log, volatile memtable working state, immutable SSTables, `METADATA`-retained SSTable lists and redo points, crash recovery by log replay, minor/merging/major compaction, and the bounded deletion-marker consequences described in the same paper.
- **Research question:** when recently committed state is simultaneously represented in a durable redo log, a volatile memtable, and later immutable SSTables, what exactly has to survive for a tablet to remain recoverable, and how can compaction deliberately replace one recovery representation with another without preserving the full sequence of writes forever?

This is **not** a general history of Bigtable, GFS, LSM trees, database logging, distributed transactions, HBase, LevelDB/RocksDB, Spanner, or modern Cloud Bigtable. It also does not claim that Bigtable invented write-ahead/redo logging, group commit, memory-to-disk merge structures, tombstones, or compaction.

The bounded retention claim is:

> **In the 2006 Bigtable design, a committed mutation does not have to survive as the same in-memory object or the same disk record forever. A valid mutation is first committed to a GFS-backed redo log and only then inserted into the volatile memtable; the tablet's current readable state is assembled from memtable plus immutable SSTables; `METADATA` retains the SSTable set and redo points needed for recovery; and minor compaction can convert volatile working state into a new SSTable so that less old log history is required on the next recovery. Retention is therefore a relation among committed redo history, current materialized files, recovery metadata, and replay rules rather than identity of one physical embodiment.**

`recovery representation`, `replay horizon`, `materialized current-state embodiment`, and `recovery-cost retention` below are **project engineering terms**, not historical Bigtable vocabulary.

---

## Historical vocabulary

The inspected 2006 paper uses:

- `tablet`;
- `tablet server`;
- `commit log`;
- `redo records`;
- `memtable`;
- `SSTable`;
- `METADATA` table;
- `redo points`;
- `group commit`;
- `minor compaction`;
- `merging compaction`;
- `major compaction`;
- `deletion entries`;
- `log sequence number`;
- `garbage collection`.

Keep these terms period-specific. Do not retroactively replace the bounded Bigtable language with later generic `WAL`, `LSM level`, `manifest`, `sequence-number snapshot`, `Raft log`, or modern Cloud Bigtable implementation vocabulary unless a later case explicitly establishes those continuities.

---

## Historical record

### H/P — the tablet's persistent state is composite, not one file

Chang et al. state that the persistent state of a tablet is stored in GFS. The representation is split across:

1. a commit log containing redo records for committed updates;
2. a volatile sorted in-memory buffer called a `memtable` for recently committed updates;
3. a sequence of persistent immutable `SSTables` for older updates.

A read does not choose one canonical physical file. It executes against a merged view of the memtable and the SSTables.

This directly establishes that the tablet's current logical contents can be distributed across **different representation classes with different volatility**.

**Primary anchor:** Chang et al., “Bigtable: A Distributed Storage System for Structured Data,” OSDI 2006, §5.3 `Tablet Serving`.

### H/P — commit precedes memtable insertion

For a valid mutation, the tablet server writes the mutation to the commit log and uses group commit for throughput. The paper then says that **after the write has been committed**, its contents are inserted into the memtable.

The bounded ordering is therefore:

```text
valid mutation
    -> commit-log durability/commit step
    -> memtable insertion
    -> later read through merged memtable + SSTables
```

The in-memory memtable is a working embodiment of state whose committed recoverability is already supported elsewhere.

**Primary anchor:** Chang et al. 2006, §5.3.

### H/P — crash recovery reconstructs the volatile memtable from retained relations

To recover a tablet, the recovering tablet server reads tablet metadata from the `METADATA` table. That metadata contains:

- the list of SSTables comprising the tablet; and
- a set of `redo points` pointing into commit logs that may contain tablet data.

The server reads SSTable indexes and reconstructs the memtable by applying updates committed since the redo points.

This means payload bytes in GFS are not enough by themselves. Recovery also depends on retained **composition metadata** saying which immutable files currently belong to the tablet and where replay must begin.

**Primary anchor:** Chang et al. 2006, §5.3.

### H/P — minor compaction changes the recovery embodiment and shortens future replay work

When a memtable reaches a threshold, Bigtable freezes it, creates a new memtable for new writes, and converts the frozen memtable to an SSTable in GFS. The paper gives two explicit goals:

- reduce tablet-server memory use;
- reduce the amount of commit-log data that must be read during recovery after a server failure.

A minor compaction therefore does more than optimize reads or reclaim memory. It moves already-current state from one recovery representation to another and **reduces the retained log suffix that future recovery must consult**.

**Primary anchor:** Chang et al. 2006, §5.4 `Compactions`.

### H/P — merging compaction can retire old materialized embodiments after a new one is complete

Bigtable periodically performs merging compactions so reads do not have to merge an unbounded number of SSTables. A merging compaction reads several SSTables and the memtable and writes a new SSTable; after the compaction finishes, the input SSTables and memtable can be discarded.

The paper's sequencing matters:

```text
read old inputs
    -> produce new SSTable
    -> compaction finishes
    -> old inputs can be discarded
```

This is a representation handoff. The current tablet state can survive while the physical files that previously embodied it cease to be retained.

**Primary anchor:** Chang et al. 2006, §5.4.

### H/P — major compaction changes deletion retention

Non-major compactions may retain special deletion entries that suppress deleted data in older SSTables that remain live. A major compaction rewrites all SSTables into exactly one SSTable and produces an output with neither deletion information nor deleted data. Bigtable regularly applies major compactions, and the authors explicitly connect them with reclaiming deleted resources and making deleted data disappear from the system in a timely manner.

This establishes a bounded forgetting relation:

```text
delete becomes current
    -> deletion entry can coexist with older physical value
    -> reads treat deletion entry as suppressing the older value
    -> major compaction rewrites the full current view
    -> deletion marker and deleted value can both disappear from Bigtable's live SSTable set
```

This is **not** evidence of raw-media sanitization below GFS.

**Primary anchor:** Chang et al. 2006, §5.4.

### H/P — immutable SSTables move permanent deletion toward file garbage collection

The paper describes SSTables as immutable. Because they are not edited in place, permanently removing obsolete data becomes a problem of garbage collecting obsolete SSTable files. Each tablet's live SSTables are registered in `METADATA`; the master treats those references as roots and deletes files not in the live set.

Physical file survival and logical tablet membership are therefore distinct. An immutable file can still exist in GFS while no longer being part of the tablet's current live-file relation, pending garbage collection.

**Primary anchor:** Chang et al. 2006, §6 `Exploiting immutability`.

### H/P — a tablet server deliberately co-mingles logical recovery streams in one physical commit log

To avoid many concurrent GFS log files and improve group commit, Bigtable writes mutations for many tablets into one commit log per tablet server.

After a tablet-server failure, those tablets can be reassigned to many different servers. Bigtable therefore sorts the failed server's commit-log entries by `<table, row name, log sequence number>` so mutations for a recovered tablet are contiguous and can be read efficiently.

One physical append stream is thus **not** identical to one logical tablet history.

**Primary anchor:** Chang et al. 2006, §6 `Commit-log implementation`.

### H/P — sequence numbers also support deduplication across log-writer switching

To reduce stalls from GFS latency spikes, a tablet server uses two log-writing threads and can switch the active log file. Mutations queued during the transition can be written by the new thread; log entries carry sequence numbers so recovery can elide duplicates caused by this switching.

The retained sequence relation is not application payload, but it changes which surviving redo records should be applied once versus ignored as duplicates.

**Primary anchor:** Chang et al. 2006, §6 `Commit-log implementation`.

### H/P — planned tablet movement uses compaction to collapse the replay requirement

Before moving a tablet from one server to another, the source server first performs a minor compaction, then stops serving the tablet; it performs a second usually-fast minor compaction to eliminate uncompacted state that arrived during the first compaction. After the second compaction, the destination can load the tablet without replaying log entries.

This is a particularly clear retention handoff:

> the system can deliberately eliminate the need to preserve/replay one recent-history representation by materializing an equivalent current-state representation first.

**Primary anchor:** Chang et al. 2006, §6 `Speeding up tablet recovery`.

---

## Retained state

The bounded Bigtable mechanism retains several distinct classes of state.

### 1. User cell versions

Bigtable's data model can retain several timestamped versions of a cell, subject to per-column-family version/age garbage-collection policy. This is **application-visible version retention**, not the same thing as the internal recovery log.

### 2. Commit-log redo records

These retain enough recent committed mutation history to reconstruct the volatile part of a tablet after tablet-server loss.

### 3. Memtable

The memtable is a volatile, sorted, current working representation of recently committed updates. It participates directly in reads but is reconstructible.

### 4. SSTables

SSTables are persistent immutable sorted maps containing older/materialized tablet state. A tablet can consist of several SSTables simultaneously.

### 5. `METADATA` live-file relation

The tablet metadata says which SSTables currently comprise a tablet. This relation makes a set of otherwise independent immutable files into the current materialized state of one tablet.

### 6. Redo points

Redo points delimit which commit-log regions may still be needed after the materialized SSTable state. They are recovery pointers, not payload.

### 7. Log sequence numbers

Sequence numbers help order/recover mutations and let recovery suppress duplicates introduced by log-writer switching.

### 8. Deletion entries

Deletion entries are negative currentness state that can temporarily remain necessary because older SSTables still contain the superseded value.

---

## Retention mechanism

A simplified write/recovery path is:

```text
client mutation
    -> commit redo record to GFS-backed commit log
    -> mutation becomes committed
    -> insert same logical update into volatile memtable
    -> reads merge memtable + SSTables

memtable grows
    -> freeze memtable
    -> create replacement active memtable
    -> write frozen state as new SSTable in GFS
    -> update tablet's materialized representation / redo horizon
    -> future crash recovery needs less old log replay
```

Crash recovery is:

```text
tablet server dies
    -> memtable embodiment disappears
    -> recover tablet METADATA
    -> recover current SSTable list + redo points
    -> open SSTables
    -> replay committed mutations after redo points
    -> reconstruct memtable
    -> resume tablet service
```

The logical tablet survives even though a particular memtable does not.

A deletion/major-compaction path is:

```text
old value exists in older SSTable
    -> deletion entry becomes current in newer state
    -> merged read suppresses old value
    -> major compaction computes complete current view
    -> new SSTable excludes deleted value and deletion marker
    -> old SSTables become obsolete
    -> file GC can remove obsolete physical files
```

The delete first changes **admissibility/currentness**; later compaction and garbage collection change the physical live-file set.

---

## Read, write, compaction, and recovery semantics

### Write

A mutation is first recorded in the commit log. Only after commit is it inserted into the memtable. The memtable is therefore not the sole durability witness for a committed write.

### Read

A read forms a merged view over the memtable and all live SSTables. No single file is necessarily the complete current tablet.

### Minor compaction

Minor compaction turns a frozen volatile working representation into a persistent SSTable. It reduces later replay work, but it is not the original commit event for mutations that were already committed.

### Merging compaction

Merging compaction reduces the number of materialized immutable components. Old inputs can be retired only after the replacement SSTable has been produced.

### Major compaction

Major compaction computes the complete current view of the tablet's SSTables and can eliminate both deleted data and the deletion entries that previously suppressed it.

### Recovery

Recovery combines retained file membership, redo points, immutable SSTables, and committed log entries. The recovered memtable is a **new embodiment** of logically current updates rather than resurrection of the lost RAM objects.

---

## Engineering reconstruction

### E — committed mutation ≠ surviving memtable object

A tablet server can lose RAM and still recover a committed mutation because the commit log retains redo evidence and the current SSTable/redo-point relation tells recovery what to replay.

### E — current readable state ≠ one current physical file

A read may require a merged view across a volatile memtable plus several immutable SSTables. “The current tablet” is a compositional relation.

### E — persistent logical state can include reconstructible volatile working state

The phrase “persistent state of a tablet” does not imply that every currently serving embodiment is nonvolatile. The volatile memtable participates in current reads while its committed contents remain reconstructible from retained persistent relations.

### E — recovery metadata ≠ payload, while recovery metadata can be constitutive of retention

The SSTable list and redo points do not contain the user values themselves, but without the correct current file set and replay boundary the surviving payload/log records are not enough to reconstruct the intended tablet efficiently and unambiguously.

### E — compaction can be retention work even when no new user value is created

Minor compaction changes how already-committed state is embodied so future failure requires less replay. It is maintenance of recoverability and recovery cost, not merely a foreground write.

### E — current-state materialization can make an older recovery-history prefix dispensable

Once volatile/log-backed updates are materialized in SSTables and the recovery boundary advances, the system no longer needs the same old commit-log prefix to rebuild the current tablet.

This is related to Case 46's GFS checkpoint/log relation only at the **functional** level. Bigtable's commit log is tablet mutation redo; GFS's master operation log is namespace/master metadata history with different authority and recovery semantics.

### E — one physical log ≠ one logical retained object history

Mutations for many tablets share one physical commit log. Recovery later sorts and partitions those records back into tablet-specific streams. Physical append locality and logical recovery identity are separate.

### E — duplicate durable records ≠ duplicate logical application

The two-log-thread refinement can leave duplicate redo records. Sequence numbers let recovery recognize them as duplicates rather than apply the same logical mutation twice.

### E — deletion currentness can require temporarily retaining negative evidence

A deletion entry may need to remain while older SSTables containing the deleted value are still live. The old positive embodiment can survive physically while the negative entry makes it noncurrent.

### E — full compaction can end both positive and negative retention obligations

After a major compaction has rewritten the complete current state, neither the deleted value nor the deletion entry is needed in the new SSTable. That is different from systems where tombstones must remain for an independent distributed-consistency grace window.

### E — Bigtable disappearance ≠ raw-media sanitization

The authors' statement that major compaction makes deleted data disappear from the system is bounded to Bigtable's live representation. GFS replicas, disk sectors, lower-layer remanence, backups, or forensic access are not analyzed by this paper.

---

## Functional analogies and boundaries

### A — Bigtable minor compaction and GFS checkpointing both replace some replay work with a materialized recovery state

Case 46 shows a complete GFS master checkpoint allowing recovery to start from a later state plus log suffix. Bigtable minor compaction likewise materializes recent state into SSTable form and reduces commit-log replay.

The analogy stops there. A Bigtable SSTable is not a GFS master checkpoint, and the two logs carry different state and authority.

### A — Bigtable compaction and Kafka compaction both deliberately rewrite retained representations, but not with the same identity contract

Case 42 Kafka compaction retains permanent logical offsets even when records are removed and promises latest-key state under its own cleaner semantics. Bigtable merging/major compaction rewrites sorted table state and has no cited permanent-Kafka-offset relation.

`compaction` is shared vocabulary, not proof of identical semantics or genealogy.

### A — Bigtable deletion entries resemble Cassandra and Swift negative-currentness evidence only at a narrow level

Cases 28 and 41 show tombstones that must survive asynchronous replica-delivery/repair risk. Bigtable's 2006 paper shows deletion entries suppressing older data in live SSTables until major compaction.

The Bigtable source does **not** establish Cassandra-style `gc_grace_seconds`, Swift consistency windows, stale-replica resurrection, or an equivalent distributed tombstone-retention rule. Do not import those semantics.

### A — Bigtable commit-log replay and GeckoFTL metadata recovery both reconstruct volatile controller/server state from persistent evidence

Case 39 reconstructs volatile Flash-management state from nonvolatile metadata/checkpoints. Bigtable reconstructs a memtable from SSTables, redo points, and committed log records.

This is only a functional recovery analogy; there is no historical or architectural identity.

### A — Bigtable redo log ≠ Kafka replicated commit log

Case 56 asks which prefix of a replicated Kafka partition is committed/current under ISR/high-watermark rules. Bigtable's commit log is a recovery log for tablet mutations stored on GFS. The 2006 paper does not make Bigtable's log itself a Kafka-like replicated consensus log.

### A — Bigtable redo logging and FFS soft updates are useful opposites

Case 16 shows a crash-consistency regime designed to avoid a persistent recovery log by constraining stable write ordering. Bigtable explicitly retains redo records and reconstructs volatile state after failure.

Both support recoverability, but through different retained evidence.

---

## Prior-art and novelty boundary

The Bigtable paper itself prevents an invention-priority story.

### H/P — Bigtable explicitly compares memtable/SSTable storage to the LSM-tree

In its related-work section, Chang et al. say that Bigtable's use of memtables and SSTables to store tablet updates is **analogous** to the Log-Structured Merge Tree, and summarize the shared pattern: sorted data buffered in memory, written to disk, and reads merging memory and disk.

The cited LSM-tree paper is:

Patrick O'Neil, Edward Cheng, Dieter Gawlick, and Elizabeth O'Neil, “The Log-Structured Merge-Tree (LSM-Tree),” *Acta Informatica* 33(4), 1996, pp. 351–385, DOI `10.1007/s002360050048`.

Therefore:

> **Bigtable 2006 is not evidence that Google invented the LSM-tree idea.**

### H/P — the Bigtable paper also cites earlier logging/group-commit literature

Its implementation section cites earlier group-commit/logging work, and its bibliography includes Gray's 1978 database-operating-system notes and Hagmann's 1987 Cedar filesystem logging/group-commit paper.

This case does not independently re-litigate the invention of redo logging or group commit. It uses Bigtable as a well-bounded distributed-system implementation in which those older techniques are composed with GFS, memtables, SSTables, metadata redo points, and tablet migration.

### Project novelty boundary

The retention-specific contribution here is narrower:

> **Use Bigtable 2006 to separate committed redo evidence, volatile current working state, persistent materialized state, file-membership/replay metadata, recovery cost, and deletion-marker retirement—and compare those relations against GFS checkpoints, Kafka compaction, distributed tombstones, and controller-metadata recovery without collapsing them into one generic “log-structured storage” mechanism.**

---

## Philosophical interpretation

### I — persistence can include the ability to recreate a working present, not preservation of its transient embodiment

A memtable can be part of the serving present and still be disposable as a physical RAM object. What persists is the relation that lets another server reconstruct an admissible present from SSTables, redo points, and committed log suffix.

This supports the repository's relational retention criterion without implying that the reconstructed bytes are metaphysically the same material object.

### I — retained history can be instrumental and intentionally finite

The commit log preserves recent mutation history because recovery may need it. Minor compaction reduces that need by materializing state elsewhere.

The past is retained here **to recover a present**, not because the system is an archive of its own complete history.

### I — forgetting can be a successful maintenance operation

Major compaction makes some negative evidence and the superseded positive data unnecessary in the live Bigtable representation. File garbage collection can then eliminate obsolete immutable embodiments.

That is technical forgetting at a particular system layer, not proof of physical obliteration at every lower layer.

### Boundary

Do not turn Bigtable into an illustration of `tertiary retention`, `Bestand`, archival memory, or cultural memory by mere analogy. The case first establishes a distributed storage-engine recovery mechanism. Any philosophical use must preserve the differences among user-visible versions, internal redo history, volatile working state, current materialized files, and lower-layer physical traces.

---

## Failure and forgetting modes

Within the bounded mechanism, retention can fail or become more expensive through several distinct routes:

- loss/unavailability of GFS-backed commit-log state needed after the redo point;
- incorrect or unavailable `METADATA` describing live SSTables or redo points;
- tablet-server RAM loss before state is reconstructed (expected failure, not necessarily data loss);
- excessive uncompacted log suffix increasing recovery work;
- duplicate redo entries applied incorrectly if sequence-number deduplication failed;
- obsolete SSTables remaining physically present after they cease to be live roots;
- deletion entries retired before their suppressive role is no longer needed (a general mechanism risk; the 2006 paper does not document a specific Bigtable bug of this form);
- lower-layer GFS or media failures outside the Bigtable-specific mechanism described here.

Do **not** infer a documented production failure from a mechanism-level risk unless an incident source is added later.

---

## Claim ledger

| Claim | Label | Evidence strength | Boundary |
| --- | --- | --- | --- |
| committed updates are recorded in a commit log containing redo records | H/P | strong | Chang et al. 2006 §5.3 |
| committed recent updates also exist in a volatile memtable | H/P | strong | memtable is inserted after commit |
| reads merge memtable with SSTables | H/P | strong | bounded 2006 design |
| recovery uses SSTable metadata + redo points + replay | H/P | strong | exact recovery description |
| minor compaction reduces future log-replay volume | H/P | strong | author-stated goal |
| merging compaction can retire old SSTables after replacement completes | H/P | strong | exact sequencing described |
| major compaction can remove deletion entries and deleted data from live Bigtable state | H/P | strong | does not imply lower-layer sanitize |
| one physical commit log contains many tablets' mutations | H/P | strong | 2006 implementation refinement |
| recovery sorts co-mingled records by table/row/sequence | H/P | strong | exact source description |
| sequence numbers let recovery elide duplicates from log switching | H/P | strong | exact source description |
| memtable survival is not required for committed mutation recovery | E | strong | follows directly from commit-before-memtable + replay |
| redo points are constitutive recovery metadata rather than payload | E | strong | direct role, project wording |
| compaction can convert retained history into retained current-state materialization | E/A | strong | project synthesis, bounded to source mechanism |
| Bigtable invented LSM | X | rejected | authors explicitly cite LSM-tree prior art |
| Bigtable invented redo logging/group commit | X | rejected | authors cite earlier literature; not investigated as origin claim |
| Bigtable major compaction is secure media sanitization | X | rejected | source only establishes Bigtable-level disappearance |
| Bigtable deletion-entry semantics equal Cassandra/Swift tombstone grace semantics | X | rejected | no such distributed grace-window evidence in source |

---

## Sources

### Primary / contemporary

1. Fay Chang, Jeffrey Dean, Sanjay Ghemawat, Wilson C. Hsieh, Deborah A. Wallach, Mike Burrows, Tushar Chandra, Andrew Fikes, and Robert E. Gruber, **“Bigtable: A Distributed Storage System for Structured Data,”** *7th USENIX Symposium on Operating Systems Design and Implementation (OSDI '06)*, pp. 205–218, 7 November 2006.
   - Official USENIX HTML: <https://static.usenix.org/event/osdi06/tech/chang/chang_html/>
   - USENIX conference record: <https://www.usenix.org/conference/osdi-06/presentation/bigtable-distributed-storage-system-structured-data>
   - Google Research publication record: <https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/>
   - Principal anchors: §2 `Timestamps`; §4 `Building Blocks`; §5.3 `Tablet Serving`; §5.4 `Compactions`; §6 `Commit-log implementation`, `Speeding up tablet recovery`, `Exploiting immutability`; §10 `Related Work`.

### Prior art / bibliography boundary

2. Patrick O'Neil, Edward Cheng, Dieter Gawlick, and Elizabeth O'Neil, **“The Log-Structured Merge-Tree (LSM-Tree),”** *Acta Informatica* 33(4), 1996, pp. 351–385. DOI: <https://doi.org/10.1007/s002360050048>.
   - Bigtable 2006 explicitly calls its memtable/SSTable update organization analogous to the LSM-tree.
   - Bibliographic record: <https://dblp.org/rec/journals/acta/ONeilCGO96.html>.

3. Jim Gray, **“Notes on Database Operating Systems,”** 1978, and Robert Hagmann, **“Reimplementing the Cedar File System Using Logging and Group Commit,”** SOSP 1987.
   - These are retained here as **prior-art references named by the Bigtable paper**, not as directly re-inspected mechanism sources in this slice.

---

## Evidence gaps / future work

This case is `grounded` for the bounded 2006 mechanism, but several questions remain deliberately open:

- exact GFS append/commit semantics beneath Bigtable's commit-log writes should be reused from or separately grounded against GFS sources rather than inferred here;
- exact `METADATA` update ordering when new SSTables/redo points advance is not fully reconstructed from the OSDI paper alone;
- source-code-level Bigtable implementation was not public, so internal crash windows beyond the paper's stated protocol are not claimed;
- later Bigtable/Cloud Bigtable WAL, compaction, replication, and deletion semantics require new version-specific cases;
- HBase/LevelDB/RocksDB/Cassandra LSM-engine behavior must not be projected back into Bigtable 2006;
- secure deletion, backup retention, lower-layer GFS replicas, and raw-media remanence remain outside this system-level deletion claim;
- independent production fault-injection evidence is not available in this bounded public source set.

---

## Related repositories

A repository search for `Bigtable`, `memtable`, `SSTable`, and the commit-log/recovery mechanism found **no dedicated Bigtable case in `tmzncty/computing-archaeology`** at the time of this slice.

Therefore this file keeps the historical account narrowly retention-specific. If a broader Bigtable engineering history is later added to `computing-archaeology`, this case should link to it and retain only the recovery/representation comparison needed here.
