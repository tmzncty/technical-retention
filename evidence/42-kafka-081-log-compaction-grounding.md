# Case 42 Grounding — Apache Kafka 0.8.1 Log Compaction, Stable Offsets, and Delete-Marker Retention

## Purpose

This record grounds [`cases/42-apache-kafka-log-compaction-delete-marker-retention.md`](../cases/42-apache-kafka-log-compaction-delete-marker-retention.md).

The bounded question is not whether Kafka has a cleanup policy. It is whether Apache's own versioned documentation and 0.8.1 implementation establish the stronger retention relations used by the case:

```text
key receives successive values
    -> later value makes older same-key records obsolete for compacted state
    -> cleaner recopies segments while omitting superseded records
    -> surviving records retain original logical offsets
    -> removed offsets remain valid traversal positions
    -> null-payload delete marker can remove older positive values
    -> marker itself remains only for a bounded observation interval
    -> consumer progress relative to that interval affects whether deletion is observed during traversal
```

## Source hierarchy

### P1 — Apache Kafka 0.8.1 versioned design documentation

**URL:** <https://kafka.apache.org/081/design/design/>

Directly establishes:

- `Log Compaction` terminology;
- at least the `last known value` for each key is retained within a topic partition;
- the stated recovery use includes rebuilding state after application/system failure and reloading caches;
- compaction is contrasted with time/size retention and with a hypothetical complete infinite log;
- a complete log can preserve every historical state but grows without bound;
- coarse time/size retention may no longer be enough to reconstruct current state from the beginning;
- compaction selectively removes older same-key records while retaining at least the final state per key;
- Apache says the feature was inspired by LinkedIn Databus;
- compacted records retain their original offsets;
- offsets never change and remain permanent identifiers for positions in the log;
- an offset whose message has been compacted away remains a valid position and reads advance to the next surviving offset;
- the documented 36/37/38 example makes sparse occupancy explicit;
- compaction preserves ordering and removes records rather than reordering them;
- keyed null payload is a delete marker;
- delete markers are themselves later removed;
- a consumer traversing from the start sees all delete markers only if it reaches the log head within `delete.retention.ms`;
- the page's 0.8.1 default is 24 hours;
- marker removal occurs concurrently with reads;
- cleaner work is background segment recopy and can be I/O-throttled;
- as of 0.8.1 the log cleaner is disabled by default and enabled through `log.cleaner.enable=true` plus per-topic `log.cleanup.policy=compact`;
- the active segment is excluded from cleaning in the bounded version and compressed topics are listed as unsupported by compaction.

**Evidence strength:** primary Apache project documentation explicitly versioned for the bounded 0.8.1 regime.

**Date boundary:** Apache's current downloads page records Kafka 0.8.1 as released on **12 March 2014**. The preserved versioned design page is used for release semantics, not as evidence that its current web-file modification date equals the historical publication date.

### P2 — Apache Kafka `0.8.1` `LogCleaner.scala`

**URL:** <https://github.com/apache/kafka/blob/0.8.1/core/src/main/scala/kafka/log/LogCleaner.scala>

Directly inspected source comments and code establish:

- cleaner responsibility for obsolete records under the source's `dedupe retention strategy` wording;
- an older record `K@O` is obsolete when a later `K@O'` exists with `O < O'`;
- clean and dirty log regions;
- the active segment is excluded from cleaning;
- background cleaner threads select dirty logs;
- cleaner builds a `key=>last_offset` mapping;
- segments are recopied while records having a later same-key offset are omitted;
- cleaned segments are swapped into the log;
- null payloads are treated as deletes;
- delete records are retained only for a configurable period;
- that period is measured from the time a segment enters the clean portion, at which point prior same-key records have been removed;
- old delete markers in the clean section are omitted during later recopy;
- implementation computes `deleteHorizonMs` using `log.config.deleteRetentionMs`;
- per-segment `retainDeletes` controls whether delete records survive the recopy;
- cleaner I/O is throttled.

**Evidence strength:** exact release-tag implementation evidence for the core compaction/delete-retention mechanism.

### P3 — Apache Kafka `0.8.1` `LogSegment.scala`

**URL:** <https://github.com/apache/kafka/blob/0.8.1/core/src/main/scala/kafka/log/LogSegment.scala>

Directly inspected source establishes:

- each segment contains a message log and an `OffsetIndex`;
- the source explicitly says the index maps **logical offsets to physical file positions**;
- `translateOffset` finds the physical file position for the first message with offset greater than or equal to the requested offset;
- `read` likewise begins with the first offset `>= startOffset`;
- segment files and indexes have physical filesystem embodiments and can be renamed/deleted;
- recovery can rebuild the index from the log file.

**Evidence use:** supports the engineering separation `stable logical offset ≠ stable physical byte position` when combined with P2's segment recopy/swap behavior. P3 by itself does not establish compaction policy.

### P4 — Apache Kafka downloads / release archive

**URL:** <https://kafka.apache.org/community/downloads/>

Directly records:

- Kafka **0.8.1 Release — Released March 12, 2014**;
- Kafka 0.8.1.1 — Released April 29, 2014.

**Evidence use:** historical date anchor for the bounded release.

### P5 — Databus prior-art boundary

Kafka P1 itself states that the functionality was inspired by LinkedIn's Databus, which it calls a database changelog caching service.

A prior scholarly anchor is:

Shirshanka Das et al., **“All Aboard the Databus!: LinkedIn's Scalable Consistent Change Data Capture Platform,”** *SoCC '12*, 2012, DOI `10.1145/2391229.2391247`.

LinkedIn's public Databus repository is <https://github.com/linkedin/databus>.

**Evidence use:** prevents a false novelty/priority claim. This record does not attempt a full Databus compaction-history reconstruction.

---

## Claim ledger

| Claim | Type | Grounding | Boundary |
| --- | --- | --- | --- |
| compaction retains at least latest known value per key | H/P | P1 | one topic partition; keyed compaction regime |
| compaction can support current-state restoration without complete change history | H/P + E | P1 | not arbitrary point-in-time replay |
| compaction differs from coarse time/size retention | H/P | P1 | release documentation comparison |
| records keep original offsets through compaction | H/P | P1 | logical offset, not physical byte position |
| offset stays a valid position after its record is removed | H/P | P1 | read advances to next surviving offset |
| ordering survives while occupancy becomes sparse | H/P + E | P1 | removed records do not imply reorder |
| null payload with key is a delete marker | H/P | P1, P2 | bounded 0.8.1 vocabulary |
| delete marker is itself retained only for configured time | H/P | P1, P2 | not indefinite negative state |
| consumer traversal time relative to `delete.retention.ms` affects guaranteed delete observation | H/P + E | P1 | observer-progress relation; not replica-repair guarantee |
| cleaner recopies segments and omits obsolete records | H/P | P1, P2 | not in-place per-record erase |
| cleaner uses latest-offset-per-key summary | H/P | P1, P2 | implementation mechanism |
| logical offsets map to physical file positions | H/P | P3 | segment/index implementation relation |
| stable logical offset ≠ stable physical byte position | E | P2 + P3 | engineering reconstruction |
| current-state reconstructability ≠ complete history retention | E | P1 | explicit source contrast supports reconstruction |
| compaction-mediated forgetting can require copying survivors | E | P1, P2 | project formulation |
| Kafka 0.8.1 delete marker = Cassandra/Swift tombstone mechanism | X | none | functional analogy only |
| Kafka invented changelog/current-state compaction | X | P1 points to Databus inspiration | no priority claim |
| delete-marker removal = secure physical erasure | X | none | outside source scope |
| Case 42 grounds Kafka replication/ISR durability | X | none | outside bounded mechanism |

---

## Cross-case controls

### Case 41 — Apache Cassandra tombstones

Shared functional relation:

```text
negative state may need to survive temporarily before it can be forgotten
```

Do not collapse the mechanisms:

- Cassandra 3.x: tombstone suppresses stale positive replicas; repair/outage relation and compaction safety determine anti-resurrection behavior;
- Kafka 0.8.1: null-payload delete marker participates in keyed log compaction and a consumer traversal/observation window while older same-key records are removed.

The timer semantics are different. `delete.retention.ms` is not `gc_grace_seconds`.

### Case 28 — OpenStack Swift tombstones

Shared functional relation: a negative record can outlive the user-facing delete and later become reclaimable.

Boundary: Swift `.ts` state participates in timestamp selection and asynchronous replica/reconstruction convergence. Kafka's delete marker participates in ordered changelog compaction and consumer traversal.

### Case 04 — mapped Flash

Shared functional relation: logical continuity can survive changed physical embodiment and reclamation can copy current state before deleting old material.

Boundary: Flash responds to erase-unit geometry and FTL mapping; Kafka cleaner recopy is a log-level keyed-history reduction. There is no historical genealogy claim.

### Finding 1 — state retention ≠ history retention

Kafka 0.8.1 is an unusually direct positive stress test for the existing finding. Apache explicitly contrasts complete-history replay with a compacted current-state representation. The case therefore strengthens the distinction without changing its scope.

---

## Terminology control

Use these as **historical 0.8.1 terms** when possible:

- `log compaction`;
- `last known value`;
- `offset`;
- `delete marker`;
- `delete retention point`;
- `log cleaner`;
- `dedupe retention strategy` (source-comment wording);
- `clean` / `dirty` section.

Use these as **project reconstruction terms only**:

- `current-state reconstructability`;
- `sparse logical position space`;
- `observer-progress retention window`;
- `compaction-mediated forgetting`.

Do not silently attribute later Kafka's convenient word `tombstone` to the inspected 0.8.1 page/source. Later continuity can be mentioned only as later terminology.

---

## Related-repository check

Search of `tmzncty/computing-archaeology` for Kafka log compaction, `delete.retention.ms`, delete-marker/tombstone, and Databus material returned no dedicated matching case during this slice.

Therefore the retention-specific case remains here. If a broader Kafka/Databus engineering history is later developed in `computing-archaeology`, Case 42 should link to it and retain only the current-state/history/offset/reclamation analysis.

---

## Evidence limits

1. The main mechanism is bounded to Kafka 0.8.1; later compaction defaults and controls differ.
2. The versioned Apache design page is a maintained historical-version page; the release date is independently anchored by Apache's downloads archive.
3. The documented 24-hour delete retention is a release/default fact, not a universal recommended value.
4. This evidence does not ground Kafka replication acknowledgements, ISR/leader recovery, broker-failure durability, or consumer-offset persistence.
5. It does not establish transaction-consistent snapshots across arbitrary keys.
6. It does not establish secure media erasure after compaction.
7. It does not equate a stable logical offset with surviving original record bytes.
8. It does not claim Kafka invented changelog caching or compaction; Kafka's own documentation names Databus as inspiration.
9. It does not equate Kafka delete-marker retention with Cassandra/Swift tombstone safety windows.
10. `stable logical offset ≠ stable physical byte position` is an engineering reconstruction jointly supported by cleaner recopy and the source's explicit logical-offset→file-position mapping; it is not a phrase used by Apache.

## Status decision

**Case 42: `grounded`.**

Reason: the central current-state/history distinction, stable-offset semantics, delete-marker observation window, cleaner-recopy mechanism, and logical-offset/physical-position separation are all grounded in version-bounded Apache documentation and exact 0.8.1 implementation source. Prior-art and later-terminology boundaries are explicit, and related-repository duplication was checked.
