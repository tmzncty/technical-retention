# Evidence 57 — Google Bigtable 2006 Commit-Log / Memtable / SSTable Recovery Grounding

## Purpose

Ground Case 57 without turning `technical-retention` into a generic Bigtable or LSM-tree history.

The bounded question is:

> **How did the 2006 Bigtable implementation retain a tablet across tablet-server failure when the serving state was split among a durable commit log, volatile memtable, immutable SSTables, and recovery metadata—and how did compaction change which history still had to be retained?**

Case file:

- [`cases/57-google-bigtable-tablet-log-memtable-recovery.md`](../cases/57-google-bigtable-tablet-log-memtable-recovery.md)

Status after this record:

- **`grounded`**

---

## Source set

### P1 — Chang et al., Bigtable, OSDI 2006

**Citation**

Fay Chang, Jeffrey Dean, Sanjay Ghemawat, Wilson C. Hsieh, Deborah A. Wallach, Mike Burrows, Tushar Chandra, Andrew Fikes, Robert E. Gruber, “Bigtable: A Distributed Storage System for Structured Data,” OSDI '06, pp. 205–218, 7 November 2006.

**Official access**

- USENIX HTML: <https://static.usenix.org/event/osdi06/tech/chang/chang_html/>
- USENIX conference record: <https://www.usenix.org/conference/osdi-06/presentation/bigtable-distributed-storage-system-structured-data>
- Google Research record: <https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/>

**Evidence class**

- primary / contemporary system paper;
- production-system author report;
- strongest source in this slice.

**Key inspected anchors**

#### §2 `Timestamps`

The paper states that one Bigtable cell can contain multiple timestamp-indexed versions and that column-family policy can keep only the last `n` versions or only versions younger than an age bound.

**Use**

Separates application-visible version history from the internal commit-log history used for recovery.

#### §4 `Building Blocks`

The paper says:

- Bigtable uses GFS for log and data files;
- SSTable is a persistent, ordered, immutable map;
- Bigtable depends on Chubby for bootstrap/location/schema/access-control functions.

**Use**

Grounds the persistent embodiment classes without re-proving the lower-layer GFS mechanism.

#### §5.3 `Tablet Serving`

Inspected statements:

- “The persistent state of a tablet is stored in GFS.”
- updates are committed to a commit log storing redo records;
- recently committed updates are in the in-memory `memtable`;
- older updates are in SSTables;
- recovery reads tablet metadata containing current SSTables and redo points;
- recovery reconstructs the memtable by applying committed updates since the redo points;
- a valid mutation is written to the commit log;
- after the write has committed, it is inserted into the memtable;
- reads use a merged view of SSTables plus memtable.

**Use**

This is the central retention evidence. It directly supports:

```text
commit-log record
    -> committed logical mutation
    -> volatile working memtable embodiment

memtable loss
    -> not necessarily mutation loss

SSTable list + redo points + committed log suffix
    -> reconstruct serving memtable
```

#### §5.4 `Compactions`

Inspected statements:

- full memtable is frozen and converted to a new SSTable in GFS;
- minor compaction reduces memory use and amount of commit-log data needed on recovery;
- merging compaction reads several SSTables plus memtable, writes a new SSTable, then inputs can be discarded;
- major compaction rewrites all SSTables into one;
- non-major outputs can contain deletion entries suppressing deleted data in older live SSTables;
- major-compaction output contains neither deletion information nor deleted data;
- major compaction is regularly used to reclaim deleted resources and make deleted data disappear from the system in a timely fashion.

**Use**

Grounds representation handoff, replay-horizon reduction, and Bigtable-level deletion forgetting.

**Boundary**

“Disappear from the system” is not converted into a claim of lower-layer raw-media sanitization.

#### §6 `Commit-log implementation`

Inspected statements:

- per-tablet logs would create too many concurrently written GFS files and weaken group commit;
- one commit log per tablet server co-mingles mutations for different tablets;
- after server death, recovered tablets can be spread over many servers;
- the failed log is sorted by `<table, row name, log sequence number>` so one tablet's mutations become contiguous;
- two log-writing threads/files can be switched to avoid GFS latency spikes;
- log sequence numbers allow recovery to elide duplicated entries resulting from switching.

**Use**

Grounds:

- physical append stream ≠ one logical tablet history;
- duplicate durable redo embodiment ≠ duplicate logical replay;
- sequence metadata as recovery/currentness infrastructure.

#### §6 `Speeding up tablet recovery`

Inspected statements:

- before planned tablet movement, the source server minor-compacts the tablet;
- after the first compaction it stops serving;
- a second usually-fast minor compaction removes remaining uncompacted log state;
- after that, the tablet can be loaded elsewhere without recovery of log entries.

**Use**

Strong evidence that a materialized current-state representation can intentionally replace the need to retain/replay recent mutation history.

#### §6 `Exploiting immutability`

Inspected statements:

- SSTables are immutable;
- permanently removing deleted data becomes garbage collecting obsolete SSTables;
- live SSTables are registered in `METADATA`;
- the master uses the `METADATA` live set as roots and deletes unreferenced files.

**Use**

Grounds `immutable physical file presence ≠ current tablet membership`.

#### §10 `Related Work`

Inspected statements:

- Bigtable's use of memtables and SSTables is described by the authors as analogous to the Log-Structured Merge Tree;
- both buffer sorted data in memory before writing to disk and merge memory/disk state on reads;
- bibliography cites O'Neil et al. 1996.

**Use**

Blocks an invention claim for LSM organization.

---

### P2 — O'Neil, Cheng, Gawlick, O'Neil, LSM-tree, 1996

**Citation**

Patrick O'Neil, Edward Cheng, Dieter Gawlick, Elizabeth O'Neil, “The Log-Structured Merge-Tree (LSM-Tree),” *Acta Informatica* 33(4), 1996, 351–385. DOI `10.1007/s002360050048`.

**Accessible bibliographic record**

- <https://dblp.org/rec/journals/acta/ONeilCGO96.html>
- DOI landing: <https://doi.org/10.1007/s002360050048>

**Evidence class**

- prior-art bibliographic anchor;
- original full text was not needed for the central Bigtable mechanism because Bigtable itself explicitly identifies the analogy.

**Use**

Only the narrow chronology:

> a named LSM-tree publication predates Bigtable 2006, and Bigtable's authors explicitly cite it as analogous prior work.

**Not used for**

- claiming exact identity between Bigtable compaction and the 1996 LSM algorithm;
- importing later production-LSM vocabulary back into 1996 or 2006;
- reconstructing Bigtable implementation details not stated by Chang et al.

---

### P3 — earlier logging/group-commit references named by Bigtable

Bigtable 2006 cites earlier logging/group-commit literature, including:

- Jim Gray, “Notes on Database Operating Systems,” 1978;
- Robert Hagmann, “Reimplementing the Cedar File System Using Logging and Group Commit,” SOSP 1987.

**Evidence class**

- prior-art references as named in the primary Bigtable bibliography;
- not independently re-inspected in this slice.

**Use**

Novelty guard only:

> Bigtable is not treated as the origin of redo logging or group commit.

Any stronger historical genealogy needs a separate prior-art slice.

---

## Evidence-to-claim map

| Case-57 claim | Source | Strength | Notes |
| --- | --- | --- | --- |
| commit log stores redo records | P1 §5.3 | strong primary | explicit |
| committed update can be resident in volatile memtable | P1 §5.3 | strong primary | commit precedes memtable insertion |
| reads merge memtable + SSTables | P1 §5.3 | strong primary | explicit |
| recovery uses SSTable list + redo points + committed log replay | P1 §5.3 | strong primary | explicit |
| minor compaction reduces future recovery-log read volume | P1 §5.4 | strong primary | author-stated goal |
| merging compaction can replace old input embodiments | P1 §5.4 | strong primary | old inputs discardable after completion |
| major compaction can eliminate deletion markers and deleted data from live Bigtable state | P1 §5.4 | strong primary | lower-layer sanitize excluded |
| one physical tablet-server log contains many tablets | P1 §6 | strong primary | explicit |
| recovery re-separates tablet streams by sorting | P1 §6 | strong primary | explicit sort key |
| log sequence numbers support duplicate suppression | P1 §6 | strong primary | explicit |
| planned move can compact away need for log replay | P1 §6 | strong primary | explicit two-minor-compaction sequence |
| live SSTable identity comes from `METADATA` roots | P1 §6 | strong primary | explicit GC description |
| Bigtable memtable/SSTable organization has LSM-tree prior art | P1 §10 + P2 | strong chronology | Bigtable authors say “analogous” |
| Bigtable invented logging/group commit | rejected | strong boundary | primary paper cites older literature |
| Bigtable major compaction guarantees raw-media sanitization | rejected | strong boundary | not in source |
| Bigtable deletion retention equals Cassandra/Swift tombstone grace semantics | rejected | strong boundary | not in source |

---

## Technical reconstruction

### 1. Committed state has multiple simultaneous embodiments

A mutation can be:

- present as a redo record in a persistent commit log;
- present as a sorted entry in volatile memtable state;
- later materialized into one or more immutable SSTables.

These are not three independent application versions. They are overlapping representations participating in one tablet's recoverable current state.

### 2. The memtable is volatile without making the committed mutation volatile

Because the source explicitly orders commit before memtable insertion and explicitly reconstructs memtable state after failure, loss of the RAM embodiment is an expected recovery event.

Project relation:

> **volatile serving embodiment ≠ volatile logical commitment**

### 3. Redo points are retained boundaries, not history archives

The redo point tells recovery where relevant unmaterialized committed history may begin. It is a compact pointer into retained history, not the history itself.

Project relation:

> **replay boundary ≠ replay history**

### 4. Minor compaction moves the replay horizon

The source's explicit recovery-time motivation makes minor compaction a retention-maintenance operation: the state is re-expressed so the future system needs less old redo history to reconstruct service.

Project relation:

> **current-state materialization can reduce future history-retention obligation**

### 5. A shared physical log can be logically repartitioned after failure

Co-mingling is chosen for normal-operation throughput; sorting after failure recovers tablet-local streams.

Project relation:

> **physical sequentiality ≠ logical object-history boundary**

### 6. Immutable files need retained membership metadata

An SSTable can be perfectly readable yet obsolete. `METADATA` says which files are roots of current tablet state.

Project relation:

> **immutable file survival ≠ current membership**

### 7. Deletion entries are transitional negative state

Until all older live SSTables are incorporated, the deletion entry suppresses an older positive value. Major compaction can then produce a representation needing neither.

Project relation:

> **negative currentness evidence can be temporary once all older positive embodiments are retired from the live representation**

---

## Cross-case controls

### Case 46 — GFS master log/checkpoint recovery

Functional similarity:

- both retain a bounded log suffix plus a materialized recovery representation;
- both can discard older history once a later representation is sufficient.

Difference:

- GFS master log concerns namespace/master metadata and checkpoint replay;
- Bigtable commit log concerns tablet mutations and memtable reconstruction.

No genealogy or protocol identity is claimed.

### Case 42 — Kafka log compaction

Functional similarity:

- both rewrite storage to reduce retained obsolete history.

Difference:

- Kafka retains stable logical offsets and latest-per-key semantics in a replicated append log;
- Bigtable compaction rewrites sorted-table materialization and uses different deletion/version semantics.

### Cases 28/41 — Swift/Cassandra tombstones

Functional similarity:

- a negative state can suppress an older physically surviving positive state.

Difference:

- those cases ground distributed-replica consistency/grace relations;
- Bigtable 2006 only grounds deletion entries relative to older live SSTables and major compaction.

### Case 39 — GeckoFTL metadata recovery

Functional similarity:

- volatile working state can be reconstructed from persistent evidence.

Difference:

- FTL mapping/validity metadata and Bigtable tablet/log/SSTable state belong to different systems and failure domains.

### Case 56 — Kafka high watermark / ISR

Control:

- Bigtable `commit log` must not be normalized into Kafka's replicated partition log;
- Bigtable's source does not ground an ISR/high-watermark commit frontier.

### Case 16 — BSD FFS soft updates

Contrast:

- Case 16 shows crash admissibility without a persistent recovery log;
- Bigtable explicitly uses redo history to reconstruct current volatile state.

---

## Prior-art judgment

### Established

- Bigtable 2006 had the exact bounded commit-log → memtable → SSTable → compaction/replay mechanism described in P1.
- The authors explicitly named LSM-tree as analogous prior art.
- The primary paper itself cites earlier logging/group-commit literature.

### Not established

- who first combined every ingredient in exactly Bigtable's form;
- whether Bigtable's internal implementation was a direct descendant of one specific LSM codebase;
- a complete logging genealogy from databases/filesystems to Bigtable;
- modern `WAL` terminology as the period's preferred Bigtable term.

### Safe wording

Use:

> “Bigtable 2006 composes a commit-log/redo-recovery path with volatile memtables, immutable SSTables, retained redo points, and compaction; its authors explicitly compare the memtable/SSTable organization to the earlier LSM-tree.”

Do not use:

> “Bigtable invented LSM storage.”

Do not use:

> “Bigtable invented write-ahead logging.”

---

## Related-repository duplication check

Searches performed against `tmzncty/computing-archaeology`:

- `Bigtable`
- `memtable`
- `SSTable`
- `commit log`

No dedicated Bigtable recovery/storage-engine case was found.

Result:

- no technical-history text was copied from the companion repository;
- this slice stays bounded to retention/recovery relations;
- future general Bigtable history belongs in `computing-archaeology` if it becomes necessary.

---

## Grounding judgment

### Why `grounded`

The central claims rely on a single unusually information-dense **primary production-system paper** with exact implementation sections that directly describe:

- commit ordering;
- memtable/SSTable composition;
- redo-point recovery;
- three compaction classes;
- deletion-marker consequences;
- shared commit-log recovery sorting;
- duplicate suppression;
- planned-movement recovery optimization;
- immutable-file garbage collection;
- explicit related-work comparison to LSM-tree.

The novelty boundary is controlled by the authors' own related-work discussion plus the 1996 LSM bibliographic anchor.

### What would be required for `mature`

- a second independent or code-level implementation witness;
- exact recovery metadata update/crash-window archaeology;
- a later Bigtable implementation comparison showing which semantics changed or survived;
- independent operational failure evidence;
- deeper direct inspection of logging/group-commit genealogy if an invention-history claim becomes important.

For the present bounded purpose, those are future maturation tasks rather than blockers.
