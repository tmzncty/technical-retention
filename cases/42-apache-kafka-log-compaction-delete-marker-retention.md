# Apache Kafka 0.8.1 Log Compaction: Stable Offsets, Last-Value Retention, and Time-Bounded Delete Markers

## Scope

- **Bounded system:** Apache Kafka 0.8.1, released 12 March 2014, with the versioned 0.8.1 design documentation and the `0.8.1` source tree as the principal inspected artifacts.
- **Bounded mechanism:** keyed log compaction, permanent logical offsets, background segment recopy, last-offset-per-key selection, null-payload delete records, and `delete.retention.ms` as a bounded delete-marker observation window.
- **Primary source base:** Apache Kafka 0.8.1 design documentation and Apache Kafka `0.8.1` source (`LogCleaner.scala`, `LogSegment.scala`).
- **Research question:** how can a log preserve enough state to reconstruct the current keyed result while deliberately forgetting most of the history that produced it, and what remains stable when the physical records themselves are recopied or removed?

This is **not** a general history of Kafka, event sourcing, log-structured storage, change-data capture, distributed messaging, or Kafka replication. It does not claim Kafka invented log compaction, changelog caching, keyed snapshots, or delete markers. The 0.8.1 design page itself says the functionality was inspired by LinkedIn's Databus.

The bounded retention claim is:

> **Kafka 0.8.1 log compaction retains at least the latest known value for each key while allowing older same-key records to disappear. Logical offsets remain permanent positions even when the record originally at an offset is removed, and a null-payload delete record is itself retained only for a bounded interval so consumers traversing concurrently with compaction can still observe the deletion. The resulting service preserves current-state reconstructability and ordering without preserving a complete event history or one fixed physical record layout.**

`current-state reconstructability`, `sparse logical position space`, `observer-progress retention window`, and `compaction-mediated forgetting` below are **project engineering terms**, not historical Kafka vocabulary.

---

## Historical vocabulary

The inspected Kafka 0.8.1 documentation directly uses:

- `log compaction`;
- `last known value`;
- `primary key` / message `key`;
- `offset`;
- `permanent identifier for a position in the log`;
- `delete marker`;
- `delete retention point`;
- `delete.retention.ms`;
- `log cleaner`;
- `log head` / `log tail`;
- `clean` / `dirty` log sections in source comments;
- `log.cleanup.policy=compact`;
- `log.cleaner.enable=true`.

The 0.8.1 `LogCleaner.scala` source comments also call the relevant policy the `dedupe retention strategy` and call null-payload entries `delete records` / `delete markers`.

Later Kafka documentation commonly calls a null-value keyed record a `tombstone`. The bounded 0.8.1 sources inspected here do not need that later word. This case therefore uses **`delete marker`** when describing the 0.8.1 historical mechanism and reserves `tombstone` for cross-case/later terminology notes.

---

## Historical record

### H/P — compaction preserves at least the last known value per key

Kafka 0.8.1's design documentation states that log compaction ensures the log of one topic partition retains at least the last known value for each message key. It presents this as useful for restoring state after application/system failure and reloading caches after restart.

The same documentation explicitly contrasts compaction with ordinary time/size retention. A complete infinite log could reproduce the state at arbitrary earlier points, but grows without bound. Coarse time/size retention bounds space but may no longer contain enough old updates to rebuild the current state from the beginning. Compaction instead selectively removes records for which a later record with the same key exists, leaving at least the final state for each key.

**Primary anchor:** Apache Kafka 0.8.1 design, `Log Compaction`.

### H/P — compacted records keep their original offsets; missing records do not renumber the log

The 0.8.1 design page says messages in the compacted tail retain the original offset assigned when written and that the offset never changes. It goes further: **all offsets remain valid positions** even when the message at a particular offset has been compacted away. A read from such an offset begins at the next higher offset that still has a record.

Its example says offsets 36, 37, and 38 can become equivalent positions when 36 and 37 no longer contain messages, with a read at any of those positions returning the message set beginning at 38.

**Primary anchor:** Apache Kafka 0.8.1 design, `Log Compaction Basics`.

### H/P — ordering is retained even though record occupancy becomes sparse

The 0.8.1 guarantee list says compaction never reorders messages; it only removes some. It separately says a message's offset never changes and remains the permanent identifier for a position in the log.

The historical guarantee is therefore not `dense append sequence forever`. It is a stable ordered position space in which some formerly occupied positions may no longer have surviving records.

**Primary anchor:** Apache Kafka 0.8.1 design, `What guarantees does log compaction provide?`.

### H/P — delete markers are negative records with a finite retention interval

The 0.8.1 design says a message with a key and a null payload is treated as a delete. This delete marker causes prior messages with the same key to be removed, but the delete marker is itself later cleaned from the log after a period so it does not consume space indefinitely.

The guarantee section says a consumer traversing from the start will see all delete markers only if it reaches the log head within the topic's `delete.retention.ms`; the documented default in this versioned design page is 24 hours. Apache explicitly explains why the timing matters: delete-marker removal happens concurrently with reads, so a marker must not be removed before the relevant traversal has had the opportunity to see it.

**Primary anchor:** Apache Kafka 0.8.1 design, `Log Compaction Basics` and `What guarantees does log compaction provide?`.

### H/P — forgetting is implemented by background segment recopy, not one in-place record erase

The 0.8.1 design describes log compaction as background work that periodically recopies log segments. Cleaner threads build a summary of the last offset for each key, recopy older segments while omitting records that have a later occurrence, and swap newly cleaned segments into the log. Cleaning does not block reads and can be I/O-throttled.

The exact `0.8.1` `LogCleaner.scala` source independently confirms the mechanism. Its comments define an obsolete message with key `K` at offset `O` as one for which a later `K` exists at `O' > O`; the cleaner builds a `key=>last_offset` map; it recopies segments while omitting superseded records; and cleaned segments are swapped into the log.

**Primary anchors:** Apache Kafka 0.8.1 design; `core/src/main/scala/kafka/log/LogCleaner.scala`, tag `0.8.1`.

### H/P — source code ties delete-marker retention to cleaned-segment state

The `0.8.1` cleaner comments say null-payload messages are deletes and that delete records are retained only for a configurable period measured from when the segment enters the clean portion of the log—at which point prior messages for that key have been removed. Delete markers in the clean section older than the interval are not retained during later segment recopy.

The implementation computes a `deleteHorizonMs` from the last modified time of the cleaned region minus `log.config.deleteRetentionMs`, then passes a `retainDeletes` decision into segment cleaning.

This is a stronger implementation anchor than simply observing that a configuration key exists.

**Primary anchor:** `LogCleaner.scala`, tag `0.8.1`.

### H/P — logical offsets are explicitly translated to physical file positions

The `0.8.1` `LogSegment.scala` comments describe each segment as a log file plus an `OffsetIndex` that **maps logical offsets to physical file positions**. `translateOffset` finds the physical file position for the first message whose offset is at least the requested offset, and `read` begins at the first offset greater than or equal to the requested value.

Together with segment recopy, this provides period implementation evidence that logical offset continuity does not require one stable byte position in one immutable file.

**Primary anchor:** `core/src/main/scala/kafka/log/LogSegment.scala`, tag `0.8.1`.

### H/P — compaction was an opt-in/disabled-by-default feature in 0.8.1

The versioned design says that **as of 0.8.1** the cleaner was disabled by default; operators enabled the cleaner with `log.cleaner.enable=true` and selected compaction per topic with `log.cleanup.policy=compact`. It also records release-specific limitations: all segments except the active one were eligible, and compaction was not yet compatible with compressed topics.

This matters because later Kafka documentation should not be projected backward onto 0.8.1 as if the operational defaults and feature boundaries were timeless.

**Primary anchor:** Apache Kafka 0.8.1 design, `Configuring The Log Cleaner` and `Log Compaction Limitations`.

---

## Retained state

The bounded mechanism retains several distinct relations.

### 1. Latest keyed value

For a key that still has a positive current value, at least its latest record must survive compaction.

### 2. Ordered logical offset space

Offsets remain durable logical positions/identifiers even when the records formerly occupying some positions have been removed.

### 3. Delete-marker state

A keyed null-payload record temporarily represents deletion strongly enough that older same-key records can be removed and a traversing consumer can observe the delete.

### 4. Cleaner summary / progress state

The cleaner builds a latest-offset-per-key map over the dirty region and maintains clean/dirty progress/checkpoint relations needed to know what can be recopied.

### 5. Physical segment/index embodiments

Actual surviving records are held in `.log` segments with index structures mapping logical offsets to file positions. Cleaning replaces segment embodiments while preserving the relevant logical ordering/offset relation.

### 6. Consumer progress

Consumer position is not payload inside the compacted log, but the documented delete-marker guarantee depends on the consumer's progress through the log relative to the marker-retention interval.

---

## Retention mechanism

A simplified positive-key sequence is:

```text
K -> V1 at offset 10
K -> V2 at offset 40
    -> cleaner records latest K offset = 40
    -> older segment is recopied
    -> record at offset 10 is omitted
    -> offset 10 remains a valid logical position
    -> read from 10 resolves to the next surviving offset
    -> V2 remains sufficient to reconstruct K's current value
```

A simplified deletion sequence is:

```text
K -> V2
K -> null   (delete marker)
    -> cleaner can omit older K values
    -> delete marker remains for bounded delete-retention interval
    -> traversing consumer can observe deletion if it catches up in time
    -> later cleaning can omit the delete marker too
    -> K has no surviving current record
```

The result deliberately retains less than the full event sequence.

---

## Addressing and access geometry

Kafka's bounded position relation is unusually useful for retention comparison:

```text
topic + partition + logical offset
    -> segment/base-offset selection
    -> offset index
    -> physical file position
    -> first surviving message with offset >= requested offset
```

The 0.8.1 design's `36, 37, 38` example means a logical position can remain meaningful after its original record disappears. This is not ordinary stable-address-to-stable-object identity.

`offset 36 still valid` means approximately **“a valid place from which traversal can resume”**, not **“the original record 36 still exists.”**

---

## Read / write / deletion semantics

### Append/write

New messages receive new offsets in the append sequence. A later same-key record does not modify the earlier record in place at write time.

### Read

Reads traverse surviving records in offset order. A requested offset whose record has been compacted resolves to the next higher surviving record.

### Supersession

An older keyed record becomes eligible for removal because a later same-key record exists.

### Delete

A keyed null payload records a delete. The marker first participates in removing older positive records; later the marker itself becomes reclaimable after its retention relation permits.

### Physical reclamation

The bounded cleaner does not erase one old record in place. It recopies selected surviving records into a clean segment, flushes/switches segment embodiments, and later removes superseded segment files.

---

## Time, maintenance, and labor

Relevant timescales include:

- append/consumer-read latency;
- the delay before a dirty segment is selected by the cleaner;
- cleaner throughput and configured I/O throttle;
- the interval in which duplicate/superseded records remain physically present before recopy;
- `delete.retention.ms`;
- the time a consumer needs to traverse from the beginning to the head;
- segment rolling and the fact that the current active segment is excluded from cleaning in the bounded 0.8.1 regime.

This is not a DRAM-like physical retention deadline. The work is policy-, workload-, segment-, and observer-progress-dependent.

The 0.8.1 feature also has operational labor: the cleaner was disabled by default, operators had to enable it and select compact policy per topic, and the cleaner consumed configurable I/O. Background automation therefore did not eliminate configuration or resource-management work.

---

## Failure / forgetting modes

Keep distinct:

- losing the latest value for a key;
- intentionally losing superseded historical values;
- losing a delete marker after its bounded observation interval;
- a traversing consumer failing to catch the log head before delete-marker reclamation;
- corrupt/missing cleaner progress or index state (not fully analyzed in this slice);
- record loss from replica/storage failure, which belongs to Kafka replication/durability semantics outside this case;
- offset discontinuity versus missing record occupancy;
- physical segment replacement versus logical ordering change;
- compaction being disabled or inapplicable under the 0.8.1 limitations.

---

## Engineering reconstruction

### E — current-state reconstructability ≠ complete history retention

The 0.8.1 design says this almost directly: compaction preserves enough per-key final state to restore current state without retaining every change. The ability to reconstruct **now** is weaker than the ability to replay to every earlier point in time.

### E — stable logical offset ≠ surviving record at that offset

Kafka explicitly keeps offsets as permanent positions even after the record at an offset is removed. A durable logical coordinate can survive the loss of the item that originally occupied it.

### E — ordering continuity ≠ dense occupancy

Compaction preserves ordering of surviving records while producing holes in the record sequence. `ordered` does not imply `every prior position remains occupied`.

### E — stable logical position ≠ stable physical byte position

`LogSegment.scala` explicitly maps logical offsets to physical file positions; `LogCleaner.scala` recopies and swaps segment files. A record's offset can remain unchanged while its physical byte position/file embodiment changes during cleaning.

### E — compaction-mediated forgetting ≠ in-place erasure

Kafka forgets older history by reconstructing a new segment containing the survivors. Retention and forgetting are therefore coupled through copying: continuing the current log state can require producing a new physical embodiment that deliberately excludes older entries.

### E — delete-marker retention ≠ indefinite negative-state retention

The negative record is useful only for a bounded relation. Once older values are removed and the configured observation window passes, Kafka can forget the delete marker itself.

### E — observer progress can be part of a retention guarantee

Apache's guarantee is phrased relative to a consumer reaching the log head before `delete.retention.ms` expires. Whether a deletion remains observable is therefore not only a property of stored bytes; it can depend on how quickly a reader traverses the changing log while cleaner work proceeds concurrently.

### E — source-of-current-state guarantee ≠ point-in-time replay guarantee

Compaction can be a source for rebuilding final keyed state while no longer supporting arbitrary reconstruction of historical states. `source of truth for current keyed result` and `complete historical archive` are separate roles.

---

## Functional analogies and limits

### A — Kafka delete markers and Cassandra tombstones (Case 41)

Both retain negative state for some interval and later reclaim it, but the safety relation differs.

- Cassandra 3.x retains tombstones so a disconnected stale replica cannot later resurrect an older value during repair; `gc_grace_seconds` is tied to replica outage/repair and compaction safety.
- Kafka 0.8.1 retains a delete marker long enough to support compacted-log traversal/consumer observation while older same-key records are being removed; `delete.retention.ms` is not documented here as Cassandra-style anti-entropy protection.

`delete marker` similarity therefore supports a functional comparison, not mechanism identity or genealogy.

### A — Kafka delete markers and Swift tombstones (Case 28)

Swift's `.ts` negative state participates in timestamp currentness and asynchronous replica/reconstructor convergence. Kafka's bounded delete marker participates in a keyed changelog/snapshot and cleaner traversal contract. The same English idea—remember a deletion temporarily—sits inside different protocols.

### A — Kafka compaction and mapped Flash reclamation (Case 04)

Both can preserve a higher-level designation while copying current state into a changed physical embodiment and later deleting obsolete material. But Kafka compaction operates over keyed log records and stable offsets; Flash FTL reclamation responds to erase-unit geometry and logical-to-physical mapping. No historical continuity is implied.

### A — Kafka compaction and log/checkpoint recovery

Compaction is functionally similar to producing a reduced representation sufficient for current recovery, but it is not a database checkpoint or transactional snapshot unless separately established. The 0.8.1 guarantee is about per-key final records and offset/order semantics, not transaction-consistent application state across arbitrary keys.

---

## Prior art and terminology boundary

The 0.8.1 Kafka design explicitly says the functionality was inspired by LinkedIn's **Databus**, described there as a database changelog caching service. A 2012 ACM SoCC paper, *All Aboard the Databus!*, predates Kafka 0.8.1 and documents Databus as LinkedIn change-data-capture infrastructure.

The safe historical claim is therefore:

> **Kafka 0.8.1 provides a directly documented, source-inspectable log-compaction regime with stable offsets and bounded delete-marker retention; Apache itself points to Databus as inspiration, so this case makes no Kafka invention-priority claim for changelog caching or current-state reconstruction.**

This case also avoids projecting later Kafka terminology backward. Later documentation uses `tombstone`; the inspected 0.8.1 material uses `delete marker` / `delete records` for the bounded historical mechanism.

---

## Philosophical / media-theoretical interpretation

The exact technical pressure is that **preserving a present state can require systematic destruction of the history that produced it while preserving the coordinate system through which the remaining state is traversed**.

Kafka 0.8.1 makes three separations unusually explicit:

1. the latest keyed state can remain while superseded changes disappear;
2. logical positions can remain while particular records at those positions disappear;
3. evidence of deletion can itself be retained only long enough to support a specified future recovery/observation relation.

This disciplines any claim that technical retention is simply accumulation. In this regime, retention of current state is materially coupled to selective forgetting.

The interpretation stops there. It does not make Kafka a model of human memory, an archive in the institutional sense, or an instance of Stiegler's tertiary retention without a separate argument about exteriorization/transmission/use.

---

## Counterexamples / limits

- The case is bounded to Kafka 0.8.1 log-compaction semantics and source; later Kafka changes defaults and adds compaction controls.
- The 24-hour delete retention value is a documented 0.8.1 default, not a universal Kafka constant or recommendation.
- `delete.retention.ms` is not Cassandra `gc_grace_seconds` and is not evidence of replica repair completion.
- A stable Kafka offset is a logical position, not proof that the original record survives.
- Compaction preserves at least final keyed state, not every intermediate value or arbitrary point-in-time replay.
- A compacted topic is not automatically a transaction-consistent database snapshot across keys.
- This case does not ground Kafka replication acknowledgements, ISR recovery, leader election, durability under broker failure, or consumer-offset storage.
- This case does not prove secure deletion of historical bytes from lower storage layers.
- Kafka 0.8.1 documentation itself points to Databus inspiration; no invention-priority claim is made.
- Later `tombstone` terminology is not silently attributed to the 0.8.1 source vocabulary.

---

## Claim ledger

| Claim | Label | Evidence / status |
| --- | --- | --- |
| compaction retains at least latest known value for each key | H/P | Kafka 0.8.1 design, `Log Compaction` |
| compaction supports rebuilding current keyed state without full history | H/P + E | Kafka 0.8.1 design |
| messages keep original offsets through compaction | H/P | `Log Compaction Basics` |
| offsets remain valid positions after their records are removed | H/P | 0.8.1 design 36/37/38 example |
| compaction preserves ordering while removing records | H/P | 0.8.1 guarantee list |
| keyed null payload is a delete marker | H/P | 0.8.1 design + `LogCleaner.scala` |
| delete marker is itself time-bounded | H/P | 0.8.1 design + `LogCleaner.scala` |
| caught-up traversal relative to `delete.retention.ms` is part of delete-observation guarantee | H/P + E | 0.8.1 guarantee list |
| cleaner performs background segment recopy and swap | H/P | design + `LogCleaner.scala` |
| logical offsets map to physical file positions | H/P | `LogSegment.scala` |
| stable offset ≠ stable physical byte position | E | cleaner recopy + offset-to-file-position mapping |
| current-state retention ≠ complete history retention | E | explicit design contrast |
| Kafka 0.8.1 delete marker is historically identical to Cassandra/Swift tombstones | X | none; analogy only |
| Kafka invented changelog compaction/current-state caching | X | contradicted by Apache's Databus inspiration note |
| compaction proves secure erasure | X | none; outside scope |

---

## Sources

### Primary / period project sources

1. Apache Kafka **0.8.1 Design — Log Compaction**: <https://kafka.apache.org/081/design/design/>
2. Apache Kafka source, tag **`0.8.1`**, `core/src/main/scala/kafka/log/LogCleaner.scala`: <https://github.com/apache/kafka/blob/0.8.1/core/src/main/scala/kafka/log/LogCleaner.scala>
3. Apache Kafka source, tag **`0.8.1`**, `core/src/main/scala/kafka/log/LogSegment.scala`: <https://github.com/apache/kafka/blob/0.8.1/core/src/main/scala/kafka/log/LogSegment.scala>
4. Apache Kafka downloads / release archive: <https://kafka.apache.org/community/downloads/> — records Kafka 0.8.1 as released **12 March 2014**.

### Prior-art boundary

5. Shirshanka Das et al., **“All Aboard the Databus!: LinkedIn's Scalable Consistent Change Data Capture Platform,”** *Proceedings of the Third ACM Symposium on Cloud Computing (SoCC '12)*, 2012, DOI `10.1145/2391229.2391247`. Kafka's own 0.8.1 design page is the source for the narrower historical statement that log compaction was inspired by Databus.
6. LinkedIn Databus repository: <https://github.com/linkedin/databus>.

### Repository controls

- [`cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md`](41-apache-cassandra-tombstone-gc-grace-resurrection.md) — distributed delete/repair comparison.
- [`cases/28-openstack-swift-tombstone-consistency-window.md`](28-openstack-swift-tombstone-consistency-window.md) — distributed tombstone/replica-convergence comparison.
- [`cases/04-flash-virtual-mapping-logical-identity.md`](04-flash-virtual-mapping-logical-identity.md) — physical relocation/reclamation comparison.

### Related-repository duplication check

`tmzncty/computing-archaeology` was searched for Kafka log compaction, `delete.retention.ms`, tombstone/delete-marker, and Databus overlap. No dedicated matching case was found during this slice. A broad Kafka/Databus architecture history should live there if developed later; this repository keeps the retention-specific current-state/history/offset/deletion comparison.

---

## Status

**`grounded`**

Grounding basis: version-bounded Apache design documentation; exact 0.8.1 source for cleaner recopy/delete-marker behavior and logical-offset-to-physical-position mapping; explicit release-specific defaults/limitations; direct Apache prior-art boundary to Databus; related-repository duplication check; and explicit separation of historical record, engineering reconstruction, functional analogy, and philosophical interpretation.
