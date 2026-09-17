# Case 42 Deepening — Kafka 0.8.1 Cleaner Checkpoint, Restart Reconstruction, and Frontier Currentness

**Status:** `bounded deepening complete`  
**Case:** [`cases/42-apache-kafka-log-compaction-delete-marker-retention.md`](../cases/42-apache-kafka-log-compaction-delete-marker-retention.md)  
**Primary baseline:** Apache Kafka `0.8.1` source, released 12 March 2014  
**Later genealogy used only as bounded evidence:** KAFKA-1641 / Kafka 0.9.0.0; KAFKA-3330 / Kafka 0.10.0.0

---

## 1. Bounded question

The existing Case 42 grounds what Kafka 0.8.1 log compaction retains at the **data/log semantics** level:

- the latest known value per key;
- stable logical offsets even when records at those offsets disappear;
- bounded delete-marker visibility;
- background segment recopy rather than in-place record erasure.

This slice asks a different, narrower question:

> **When the cleaner itself is interrupted or the broker process restarts, which pieces of compaction-maintenance state are retained, which are reconstructed, and which are merely runtime state? What makes a retained cleaner frontier still meaningful after the underlying log geometry changes?**

The resulting control-state distinction is:

```text
persistent cleaner frontier
    != in-memory latest-key map
    != in-progress / paused runtime state
    != physical segment-swap state
    != proof of power-loss durability
```

A second distinction emerges from the later bug trail:

```text
checkpoint bytes survive
    != checkpoint still denotes a valid cleaning frontier
```

`maintenance frontier`, `frontier currentness`, `conservative replay`, and `referent geometry` below are **project engineering terms**, not historical Kafka vocabulary.

---

## 2. Claim discipline

### H/P — historical / primary record

Historical and implementation claims are limited to:

- Apache Kafka exact tagged source;
- Apache Kafka project JIRA records;
- Apache Kafka source changes in later tagged releases where they directly answer the bounded checkpoint-currentness question.

### E — engineering reconstruction

Terms such as `maintenance frontier`, `semantic currentness`, and `conservative replay` are analytical descriptions of source-observable relations. They are not attributed to Kafka developers unless the source uses equivalent wording.

### A — functional analogy

Comparisons with HDFS, LevelDB, RAID maintenance, or other repository cases are relational only. They do not establish genealogy or mechanism identity.

### I — philosophical interpretation

Interpretation appears only after the implementation record and is explicitly weaker than it.

---

## 3. Historical / implementation record — Kafka 0.8.1

### H/P 3.1 — cleaner progress is externalized as `cleaner-offset-checkpoint`

In Kafka `0.8.1`, `LogCleanerManager` constructs one `OffsetCheckpoint` per configured log directory:

```scala
private val checkpoints = logDirs.map(dir =>
  (dir, new OffsetCheckpoint(new File(dir, "cleaner-offset-checkpoint"))))
  .toMap
```

The source comment describes these as:

> `the offset checkpoints holding the last cleaned point for each log`

The manager's `allCleanerCheckpoints()` reads the checkpoint files and merges their topic/partition-to-offset mappings.

This is direct implementation evidence that the cleaner's **completed frontier** is not represented only inside a cleaner thread's heap.

**Primary anchor:** Kafka `0.8.1`, `core/src/main/scala/kafka/log/LogCleanerManager.scala`.

### H/P 3.2 — scheduler selection re-reads that frontier and falls back to the log's first segment when no checkpoint exists

`grabFilthiestLog()` begins by reading all cleaner checkpoints. For each compacted log it constructs `LogToClean` with:

```scala
lastClean.getOrElse(topicAndPartition, log.logSegments.head.baseOffset)
```

as the first dirty offset.

Therefore the bounded 0.8.1 relationship is:

```text
checkpoint entry exists
    -> use retained offset as first dirty frontier

checkpoint entry absent
    -> fall back to first segment base offset
```

The checkpoint does not contain a full serialized cleaner execution state. It supplies one coordinate from which the cleaner reconstructs work against the **currently loaded log**.

**Primary anchor:** Kafka `0.8.1`, `LogCleanerManager.scala`.

### H/P 3.3 — a successfully completed cleaning advances the checkpoint; an aborted cleaning does not

`LogCleaner.CleanerThread.cleanOrSleep()` initializes `endOffset` to the first dirty offset, runs `cleaner.clean(cleanable)`, and calls `cleanerManager.doneCleaning(...)` in a `finally` block.

`LogCleanerManager.doneCleaning()` distinguishes runtime states:

- if the partition is `LogCleaningInProgress`, it reads the current checkpoint map, writes the new `(topicAndPartition, endOffset)` entry, and removes the partition from the in-progress set;
- if the cleaner was aborted, it changes runtime state to `LogCleaningPaused` and **does not write a new completed offset**.

The source therefore separates:

```text
work attempted
    != work checkpointed as completed
```

and:

```text
abort / pause transition
    != advance durable-looking cleaner frontier
```

This is not a transactional-commit claim. It is the narrower source fact that the normal completed-cleaning path advances the external checkpoint while the explicit abort path does not.

**Primary anchors:** Kafka `0.8.1`, `LogCleaner.scala`; `LogCleanerManager.scala`.

### H/P 3.4 — the latest-key offset map is rebuilt, not checkpointed

The `Cleaner` object owns an `OffsetMap` used for deduplication. Every `clean()` call invokes `buildOffsetMap(...)`; `buildOffsetMap()` begins with:

```scala
map.clear()
```

and scans the dirty log segments to repopulate key-hash-to-latest-offset relations.

The 0.8.1 cleaner therefore does **not** need to retain its complete latest-key summary across cleaner cycles or broker-process lifetime in order to continue cleaning.

The retained/reconstructed split is:

```text
retained externally:
    first-dirty / last-cleaned offset checkpoint

reconstructed from current log contents:
    key -> latest offset map for the dirty region
```

This is a concrete example of **progress persistence without algorithm-state persistence**.

**Primary anchor:** Kafka `0.8.1`, `LogCleaner.scala`, `Cleaner.buildOffsetMap()`.

### H/P 3.5 — `inProgress`, aborted, and paused cleaner states are ordinary process-memory state

`LogCleanerManager` declares:

```scala
private val inProgress = mutable.HashMap[TopicAndPartition, LogCleaningState]()
```

and uses the three runtime states:

- `LogCleaningInProgress`;
- `LogCleaningAborted`;
- `LogCleaningPaused`.

The inspected 0.8.1 code does not serialize this map into `cleaner-offset-checkpoint` or another cleaner-state file.

On a new `LogCleanerManager` instance, the runtime map begins empty. The process can still recover a cleaning frontier from `cleaner-offset-checkpoint`, but it does not thereby recover the previous process's exact paused/in-progress state machine.

Thus:

```text
cleaner progress checkpoint
    != cleaner runtime control state
```

**Primary anchor:** Kafka `0.8.1`, `LogCleanerManager.scala`.

### H/P 3.6 — broker startup reconstructs logs first and then constructs/starts a new cleaner

Kafka `0.8.1` `LogManager`:

1. validates and locks log directories;
2. reads recovery-point checkpoints;
3. loads logs from the directories;
4. constructs a new `LogCleaner` when enabled;
5. later starts the cleaner threads in `LogManager.startup()`.

The cleaner therefore resumes in a newly constructed process context **against logs that have themselves been reloaded/recovered from disk**.

This matters because `cleaner-offset-checkpoint` is not self-sufficient. Its offset is interpreted relative to the post-startup segment set.

**Primary anchor:** Kafka `0.8.1`, `core/src/main/scala/kafka/log/LogManager.scala`.

### H/P 3.7 — checkpoint writing uses temp-file replacement, but the inspected 0.8.1 implementation does not explicitly fsync the file or parent directory

`OffsetCheckpoint.write()` in Kafka `0.8.1`:

1. creates `<checkpoint>.tmp`;
2. writes version, entry count, and topic/partition/offset tuples with `BufferedWriter` / `FileWriter`;
3. calls `writer.flush()` and then closes the writer;
4. replaces the previous checkpoint with `File.renameTo()`;
5. on Windows-style rename failure, deletes the destination and retries the rename.

The inspected method does **not** contain an explicit `FileDescriptor.sync()`, `FileChannel.force(...)`, or containing-directory fsync.

The safe claim is therefore:

> **Kafka 0.8.1 externalizes cleaner progress to a restart-readable file representation using temp-file replacement. This source inspection does not establish a universal sudden-power-loss durability guarantee for the checkpoint publication itself.**

Do not silently upgrade:

```text
file-backed / restart-readable
```

to:

```text
proven crash-durable under every filesystem + storage stack
```

**Primary anchor:** Kafka `0.8.1`, `core/src/main/scala/kafka/server/OffsetCheckpoint.scala`.

### H/P 3.8 — segment replacement has a separate, explicit interrupted-swap recovery protocol

The cleaner's physical segment replacement is not the same state as its offset checkpoint.

In `Cleaner.cleanSegments()`:

- a new `.cleaned` log/index pair is created;
- retained records are copied into it;
- the cleaned segment is flushed;
- `log.replaceSegments(cleaned, segments)` performs the swap.

`Log.replaceSegments()` explicitly says it swaps the replacement segment and retires old segments **“in a crash-safe manner”** and that an interrupted swap is completed in `loadSegments()`.

Its suffix protocol is approximately:

```text
*.cleaned
    -> rename to *.swap
    -> add replacement to live segment map
    -> rename old segments to *.deleted and schedule deletion
    -> remove *.swap suffix from replacement
```

At startup, `loadSegments()` makes a first pass through files:

- `.deleted` and `.cleaned` files are deleted;
- `.swap` index files are deleted so the index can be rebuilt;
- a `.swap` log file is renamed into the normal `.log` name so the interrupted swap can be completed.

This is an explicit **segment-embodiment recovery protocol**. It is distinct from the cleaner's `topic/partition -> first dirty offset` checkpoint.

**Primary anchors:** Kafka `0.8.1`, `LogCleaner.scala`; `Log.scala`.

### H/P 3.9 — segment-swap recovery and cleaner-frontier persistence are different recovery layers

The code therefore exposes at least two maintenance-recovery relations:

```text
A. physical segment publication / retirement
   .cleaned -> .swap -> normal segment
   with startup repair of interrupted swap

B. cleaner progress frontier
   cleaner-offset-checkpoint
   topic/partition -> offset
```

A new process can need both:

- a coherent set of physical segments;
- a usable coordinate saying where future cleaner work begins.

Neither representation contains the other.

This is a historical/source-level decomposition, not a claim that Kafka developers described it in these analytical terms.

---

## 4. 2014 operational evidence — KAFKA-1641 and a checkpoint that survived but became too old for the current log start

### H/P 4.1 — the bug report is explicitly about a later broker restart

Apache JIRA **KAFKA-1641**, created **18 September 2014**, is titled:

> `Log cleaner exits if last cleaned offset is lower than earliest offset`

It is marked as affecting **0.8.1.1** and fixed for **0.9.0.0**.

The reporter says that after the cleaner had previously exited, **“on a subsequent restart of the broker”** the cleaner failed with:

```text
Last clean offset is 54770438
but segment base offset is 382844024
```

The important evidence is not the exact numeric gap. It is that the cleaner retained a previous frontier and later interpreted it against a segment set whose earliest available base offset had advanced beyond that frontier.

**Primary anchor:** Apache JIRA KAFKA-1641.

### H/P 4.2 — later 0.9 source validates the retained frontier against current log start

Kafka `0.9.0.0` `LogCleanerManager.grabFilthiestLog()` contains an explicit currentness check:

```scala
val logStartOffset = log.logSegments.head.baseOffset
val offset = lastClean.getOrElse(topicAndPartition, logStartOffset)
if (offset < logStartOffset) {
  error("Resetting first dirty offset ... since the checkpointed offset ... is invalid.")
  logStartOffset
} else {
  offset
}
```

This does not mean the checkpoint failed to persist. It means persistence was insufficient: the retained coordinate had to be **validated/rebound against the current log geometry**.

The historical relationship is:

```text
retained offset
    + later segment retention / deletion
    -> possible stale coordinate
    -> validate against current log start
    -> reset if no longer admissible
```

**Primary anchor:** Kafka `0.9.0.0`, `LogCleanerManager.scala`; KAFKA-1641.

---

## 5. 2016 genealogy — KAFKA-3330 and truncation invalidating a different frontier relation

### H/P 5.1 — log truncation could leave the cleaner checkpoint semantically incompatible with the new segment layout

Apache JIRA **KAFKA-3330**, created **3 March 2016** and resolved **17 March 2016**, describes another cleaner failure.

The issue gives a concrete sequence:

```text
segments: [100,200), [200,300), [300,400)
cleaner checkpoint: 300

truncate log to 220
    -> segments: [100,200), [200,220)
    -> checkpoint still 300

append new data
    -> segments include [200,320), [320,420)
    -> checkpoint still 300

cleaner starts from 300
    -> buildOffsetMap requires its starting offset to equal a segment base offset
    -> requirement fails
```

The retained integer `300` is still a perfectly readable integer. The problem is that its role as the clean/dirty boundary is no longer valid after the log was rewritten around it.

**Primary anchor:** Apache JIRA KAFKA-3330.

### H/P 5.2 — Kafka 0.10.0.0 couples truncation with cleaner-checkpoint correction

KAFKA-3330 is marked fixed for **0.10.0.0**.

The `0.10.0.0` source exposes `maybeTruncateCheckpoint(...)`. `LogManager.truncateTo()` and `truncateFullyAndStartAt()`:

1. abort/pause cleaner work when needed;
2. truncate the log;
3. invoke cleaner checkpoint correction against the new active-segment base offset;
4. resume cleaner work.

`LogCleanerManager.maybeTruncateCheckpoint()` reads the existing checkpoint and, when it is above the supplied valid frontier, rewrites that partition's checkpoint to the supplied offset.

This later fix is useful here because it directly demonstrates the required relation:

```text
log geometry mutation
    -> cleaner frontier may need mutation too
```

The checkpoint is not an autonomous truth. Its meaning depends on the structure it indexes.

**Primary anchors:** Apache JIRA KAFKA-3330; Kafka `0.10.0.0` `LogCleaner.scala`, `LogCleanerManager.scala`, and `LogManager.scala`.

---

## 6. Engineering reconstruction

### E 6.1 — progress persistence ≠ algorithm-state persistence

Kafka 0.8.1 externally retains the last-cleaned/first-dirty frontier, but rebuilds the key-to-latest-offset map from the dirty log.

Therefore:

```text
restartable maintenance
    need not mean
serialize the entire maintenance algorithm state
```

A much smaller retained coordinate can be sufficient when the larger working set is reconstructible from authoritative data.

### E 6.2 — persisted coordinate ≠ self-validating coordinate

KAFKA-1641 and KAFKA-3330 show two forms of referent drift:

```text
checkpoint too far behind current log start
```

and:

```text
checkpoint no longer aligned with the post-truncation segment geometry
```

In both cases the bytes can remain intact while the coordinate becomes operationally invalid.

Thus:

```text
bitwise persistence
    != semantic currentness
```

### E 6.3 — semantic persistence can require retaining or reconstructing the interpretation structure

A cleaner checkpoint offset has meaning only relative to at least:

- the same topic/partition identity;
- the current ordered offset space;
- the current set of segment base offsets;
- the log's present truncation/start boundary;
- the cleaner rule that interprets the number as the first dirty position.

This is a concrete distributed-storage example of Synthesis 29's broader point:

```text
stored scalar
    + valid interpretation frame
    = usable retained meaning
```

The interpretation frame here is not a clock coordinate, as in HDFS Case 116. It is a **mutable log geometry**.

### E 6.4 — completed frontier ≠ exact record of all maintenance already embodied on disk

The cleaner swaps cleaned segment groups during `clean()`, while the per-partition cleaner checkpoint is advanced by `doneCleaning()` after the cleaning run returns.

Therefore the physical log can pass through segment-replacement steps before the aggregate cleaner frontier is advanced.

A conservative reading is:

```text
checkpoint may lag some already-produced cleaned embodiments
```

which means a restarted/retried cleaner may have to revisit work rather than assuming exact once-only execution.

This evidence does **not** prove that every interruption causes duplicate recopy, nor does it fully enumerate every crash window. It only blocks the stronger claim:

```text
cleaner checkpoint == exact physical work ledger
```

### E 6.5 — restart continuation ≠ exactly-once maintenance execution

The bounded design is compatible with replay/re-cleaning from a conservative frontier.

That is enough to distinguish:

```text
can continue making progress after restart
    != every cleaning unit is performed exactly once
```

No exactly-once cleaner guarantee is claimed by the inspected 0.8.1 sources.

### E 6.6 — segment-swap crash recovery ≠ checkpoint power-loss durability

`Log.replaceSegments()` and `loadSegments()` explicitly implement an interrupted-swap recovery protocol.

`OffsetCheckpoint.write()` uses temp-file replacement but the inspected implementation does not explicitly issue the stronger storage-barrier sequence that would be required to make a filesystem-independent sudden-power-loss claim.

Therefore:

```text
source labels segment swap crash-safe
    != all cleaner metadata publication has identical durability semantics
```

Different retained relations can have different recovery mechanisms even inside one maintenance subsystem.

### E 6.7 — maintenance progress must co-evolve with destructive log mutation

The 2016 truncation fix makes this especially clear:

```text
change the log's valid history / geometry
    without changing dependent maintenance frontier
    -> retained control state can become false
```

This is stronger than saying “checkpoints can be stale.” It identifies a dependency:

```text
checkpoint currentness
    depends on
current log geometry
```

A state-retention design therefore has to retain not merely a value, but the relation that makes that value valid.

---

## 7. Functional analogies and limits

### A 7.1 — HDFS Case 116: same persistence problem, different interpretation frame

Case 116 shows an externally retained maintenance-expiry scalar whose meaning was unstable when interpreted with a new JVM-local monotonic-clock origin.

Case 42's cleaner frontier has a different failure mode: the offset number survives, but the log segment geometry against which it is interpreted can change.

The bounded analogy is:

```text
persisted scalar
    != persisted meaning
```

The mechanisms are unrelated: clock-coordinate alignment is not log-segment-frontier validation.

### A 7.2 — LevelDB Case 137: maintenance frontier is not a root-pointer publication protocol

LevelDB Case 137 separates durable MANIFEST contents from publication of the `CURRENT` pathname relation.

Kafka Case 42 instead separates:

- physical segment-swap recovery;
- cleaner progress checkpoint;
- reconstructed dedupe map.

Both show that multiple retained relations can participate in restart behavior, but there is no claim that Kafka's cleaner checkpoint is equivalent to LevelDB's `CURRENT` root pointer.

### A 7.3 — MegaRAID Case 136: explicit task continuation vs reconstructible maintenance frontier

Case 136 grounds controller-level restart continuation for rebuild/check-consistency without exposing the exact progress representation.

Case 42 is almost the inverse evidence shape: source exposes a concrete progress coordinate (`cleaner-offset-checkpoint`) but does not retain the full runtime cleaner state.

The comparison is useful because:

```text
maintenance continuation
    and
progress representation
```

are separate questions.

No RAID-to-Kafka genealogy is implied.

---

## 8. Philosophical / media-theoretical interpretation

The narrow interpretive lesson is that **a retained trace does not carry its own future legibility**.

Kafka's cleaner offset looks like an unusually simple retained object: topic, partition, number. Yet its operational meaning depends on a later log still presenting a compatible geometry. Retaining the mark while transforming the field it marks can turn preservation into residue.

The stronger formulation is therefore not:

> persistence keeps a fact.

It is:

> persistence keeps a relation only if enough of the relation's future interpretation conditions survive or can be reconstructed.

This interpretation remains downstream of the implementation record. Kafka developers are not being credited with this philosophical vocabulary.

---

## 9. Explicit non-claims

This slice does **not** claim that:

1. `cleaner-offset-checkpoint` contains the latest value for every Kafka key;
2. the dedupe `OffsetMap` itself is persisted across broker restart in Kafka 0.8.1;
3. paused/in-progress cleaner control state is serialized in the checkpoint file;
4. a cleaner checkpoint is a Kafka consumer offset;
5. a cleaner checkpoint is the partition's replication high watermark;
6. cleaner restart semantics prove Kafka message durability under broker failure;
7. `OffsetCheckpoint.write()` is universally power-loss atomic across filesystems;
8. absence of an explicit fsync in this inspected method proves corruption will occur on a particular filesystem;
9. Java `renameTo()` supplies one universal crash-durability contract across platforms;
10. the `.cleaned/.swap/.deleted` protocol is identical to the cleaner offset checkpoint protocol;
11. a source comment saying `crash-safe` is by itself a hardware/storage-stack fault-injection proof;
12. every broker restart repeats compaction work;
13. cleaner execution is exactly-once;
14. KAFKA-1641 proves the same failure occurs in every Kafka 0.8.1 deployment;
15. KAFKA-3330 affected Kafka 0.8.1 specifically; the issue is later genealogy and is not projected backward as a release-specific 0.8.1 bug claim;
16. Kafka 0.9 and 0.10 fixes are silently attributed to Kafka 0.8.1;
17. cleaner-checkpoint currentness is the same problem as HDFS clock semantics or LevelDB pathname publication;
18. this slice grounds replication, ISR recovery, leader election, transaction semantics, or consumer-offset persistence;
19. current-state log compaction provides arbitrary point-in-time replay;
20. retaining a valid cleaner frontier guarantees delete markers remain observable beyond their separately defined retention window.

---

## 10. Claim ledger

| Claim | Type | Evidence | Boundary |
| --- | --- | --- | --- |
| Kafka 0.8.1 stores per-log-directory `cleaner-offset-checkpoint` files | H/P | `LogCleanerManager.scala` | cleaner maintenance progress only |
| checkpoint maps topic/partition to last-cleaned / first-dirty offset | H/P | `LogCleanerManager.scala` | not per-key state |
| absent checkpoint falls back to first segment base offset | H/P | `grabFilthiestLog()` | 0.8.1 baseline |
| successful normal cleaning advances checkpoint | H/P | `doneCleaning()` | completed path |
| explicit abort path does not advance checkpoint | H/P | `doneCleaning()` | runtime abort semantics |
| dedupe latest-key map is cleared/rebuilt from dirty log | H/P | `Cleaner.buildOffsetMap()` | not persisted algorithm state |
| in-progress/paused cleaner states are held in process-memory map | H/P | `LogCleanerManager.scala` | no serialization found in bounded source |
| broker startup loads logs then constructs/starts cleaner | H/P | `LogManager.scala` | restart reconstruction path |
| 0.8.1 checkpoint write uses temp file + rename | H/P | `OffsetCheckpoint.scala` | no universal power-loss claim |
| 0.8.1 source does not explicitly fsync checkpoint file or parent directory in `OffsetCheckpoint.write()` | H/P/source observation | `OffsetCheckpoint.scala` | absence of explicit call, not proof of failure |
| segment replacement uses `.cleaned/.swap/.deleted` interrupted-swap recovery | H/P | `LogCleaner.scala`, `Log.scala` | physical segment layer |
| KAFKA-1641 records restart failure when checkpoint < earliest segment offset | H/P | Apache JIRA, 2014 | affects 0.8.1.1, not every deployment |
| Kafka 0.9 validates checkpoint against current log start and resets invalid old frontier | H/P | `0.9.0.0` `LogCleanerManager.scala` | later fix/genealogy |
| KAFKA-3330 records checkpoint invalidation after truncation | H/P | Apache JIRA, 2016 | later genealogy |
| Kafka 0.10 couples log truncation with cleaner-checkpoint correction | H/P | `0.10.0.0` source | later fix/genealogy |
| progress persistence ≠ algorithm-state persistence | E | checkpoint + rebuilt offset map | project formulation |
| bitwise persistence ≠ semantic currentness | E | KAFKA-1641 + KAFKA-3330 | project formulation |
| restart continuation ≠ exactly-once maintenance | E | checkpoint/swap ordering | no exactly-once claim |
| checkpoint currentness depends on log geometry | E | later bug/fix trail | bounded cleaner frontier relation |

---

## 11. Sources

### Primary exact-release sources

1. Apache Kafka `0.8.1`, `core/src/main/scala/kafka/log/LogCleanerManager.scala`  
   <https://github.com/apache/kafka/blob/0.8.1/core/src/main/scala/kafka/log/LogCleanerManager.scala>
2. Apache Kafka `0.8.1`, `core/src/main/scala/kafka/log/LogCleaner.scala`  
   <https://github.com/apache/kafka/blob/0.8.1/core/src/main/scala/kafka/log/LogCleaner.scala>
3. Apache Kafka `0.8.1`, `core/src/main/scala/kafka/server/OffsetCheckpoint.scala`  
   <https://github.com/apache/kafka/blob/0.8.1/core/src/main/scala/kafka/server/OffsetCheckpoint.scala>
4. Apache Kafka `0.8.1`, `core/src/main/scala/kafka/log/Log.scala`  
   <https://github.com/apache/kafka/blob/0.8.1/core/src/main/scala/kafka/log/Log.scala>
5. Apache Kafka `0.8.1`, `core/src/main/scala/kafka/log/LogManager.scala`  
   <https://github.com/apache/kafka/blob/0.8.1/core/src/main/scala/kafka/log/LogManager.scala>
6. Apache Kafka downloads / release archive — Kafka 0.8.1 released 12 March 2014  
   <https://kafka.apache.org/community/downloads/>

### Later project genealogy / operational evidence

7. Apache JIRA **KAFKA-1641**, `Log cleaner exits if last cleaned offset is lower than earliest offset`, created 18 September 2014; affects 0.8.1.1; fixed for 0.9.0.0.  
   <https://issues.apache.org/jira/browse/KAFKA-1641>
8. Apache Kafka `0.9.0.0`, `LogCleanerManager.scala` — validation/reset when checkpoint is below current log start.  
   <https://github.com/apache/kafka/blob/0.9.0.0/core/src/main/scala/kafka/log/LogCleanerManager.scala>
9. Apache JIRA **KAFKA-3330**, `Truncate log cleaner offset checkpoint if the log is truncated`, created 3 March 2016; resolved 17 March 2016; fixed for 0.10.0.0.  
   <https://issues.apache.org/jira/browse/KAFKA-3330>
10. Apache Kafka `0.10.0.0`, `LogCleaner.scala`, `LogCleanerManager.scala`, and `LogManager.scala` — checkpoint truncation/correction integration.  
    <https://github.com/apache/kafka/blob/0.10.0.0/core/src/main/scala/kafka/log/LogCleaner.scala>  
    <https://github.com/apache/kafka/blob/0.10.0.0/core/src/main/scala/kafka/log/LogCleanerManager.scala>  
    <https://github.com/apache/kafka/blob/0.10.0.0/core/src/main/scala/kafka/log/LogManager.scala>
11. Apache Kafka PR #1009, KAFKA-3330 patch discussion. The PR is used as development-history context; the tagged 0.10.0.0 source is the stronger landed-code anchor.  
    <https://github.com/apache/kafka/pull/1009>

### Repository controls

12. [`evidence/42-kafka-081-log-compaction-grounding.md`](42-kafka-081-log-compaction-grounding.md) — existing Case 42 semantic/mechanism grounding.
13. [`docs/SYNTHESIS_29_SEMANTIC_PERSISTENCE_AND_RESTART_CONTINUATION.md`](../docs/SYNTHESIS_29_SEMANTIC_PERSISTENCE_AND_RESTART_CONTINUATION.md) — cross-case vocabulary for progress/semantic/restart continuity.
14. [`cases/137-leveldb-v17-manifest-current-recovery.md`](../cases/137-leveldb-v17-manifest-current-recovery.md) — bounded comparison for restart-relevant metadata publication; analogy only.
15. [`cases/116-hadoop-datanode-maintenance-state.md`](../cases/116-hadoop-datanode-maintenance-state.md) — bounded comparison for persisted scalar + interpretation frame; analogy only.

---

## 12. Related-repository duplication check

A fresh search of `tmzncty/computing-archaeology` for:

- `Kafka`;
- `cleaner-offset-checkpoint`;
- log-cleaner restart/checkpoint history

returned no dedicated matching packet.

Accordingly this file keeps only the retention-specific seam:

```text
maintenance progress frontier
    -> process restart
    -> reconstruction from current log
    -> validation against changed log geometry
```

A broad history of Kafka log cleaning, segment formats, LinkedIn/Databus influence, or the evolution of Kafka storage internals belongs in `computing-archaeology` if developed later.

---

## 13. Remaining evidence debt

This slice intentionally leaves the following for later bounded work:

1. exact commit/patch genealogy from KAFKA-1641's 2014 attachments into the final 0.9 source;
2. fault-injection evidence for 0.8.1 `OffsetCheckpoint.write()` across specific filesystems and sudden-power-loss windows;
3. exact crash-window tests for interruption between individual cleaned-segment swaps and `doneCleaning()` checkpoint publication;
4. whether a graceful broker restart was directly covered by a 0.8.1 cleaner-checkpoint integration test;
5. later lifecycle rules that remove/migrate checkpoint entries when partitions are deleted or moved between log directories;
6. interaction between cleaner checkpoint currentness and later transactional-log/first-uncleanable-offset semantics, which postdate the bounded 0.8.1 regime.

None of these debts blocks the bounded conclusion here.

---

## 14. Bounded conclusion

Kafka 0.8.1 log cleaning did not persist one monolithic “cleaner state.” It split maintenance continuity across several representations:

```text
persistent-ish external frontier:
    cleaner-offset-checkpoint

reconstructed working state:
    key -> latest offset map

runtime-only control state:
    in-progress / aborted / paused map

physical replacement recovery:
    .cleaned / .swap / .deleted segment protocol
```

Later Apache bug and fix records show why the frontier itself still requires semantic currentness. A checkpoint can survive a broker restart and yet cease to denote a valid place in the **current** log after retention or truncation changes the segment geometry.

The strongest safe engineering statement is therefore:

> **Maintenance progress is not preserved merely by keeping a checkpoint number. It is preserved only when the later system can still interpret that number against a compatible or repaired referent structure.**

Case 42 remains **`grounded`**. This evidence deepens its maintenance-control/restart boundary without changing the case maturity.