from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def insert_after(text: str, anchor: str, addition: str, label: str) -> str:
    return replace_once(text, anchor, anchor + addition, label)


# README
p = Path("README.md")
text = p.read_text()
case41 = "- [`cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md`](cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md) — grounded distributed-deletion/repair bridge: Cassandra retains tombstones so missed deletes can later defeat stale positive replicas; `gc_grace_seconds`, compaction overlap, repair, and optional repaired-state gating keep deletion convergence, age eligibility, and actual reclamation distinct, while premature loss of deletion evidence can let repair resurrect older data.\n"
case42 = "- [`cases/42-apache-kafka-log-compaction-delete-marker-retention.md`](cases/42-apache-kafka-log-compaction-delete-marker-retention.md) — grounded compacted-changelog bridge: Kafka 0.8.1 keeps at least the last known value per key while background segment recopy removes superseded history; original logical offsets remain permanent traversal positions even when records disappear, and time-bounded delete markers make consumer catch-up progress part of the deletion-observation contract.\n"
text = insert_after(text, case41, case42, "README case anchor")
ev41 = "- [`evidence/41-cassandra-3x-tombstone-repair-grounding.md`](evidence/41-cassandra-3x-tombstone-repair-grounding.md) — Case-41 grounding record: Apache Cassandra 3.11 documentation, 3.x release notes, branch source, and unit tests separate tombstone negative currentness, hint delivery, anti-entropy repair, `gc_grace_seconds`, compaction eligibility, repaired/unrepaired state, and data-resurrection risk without equating reclamation with secure erasure.\n"
ev42 = "- [`evidence/42-kafka-081-log-compaction-grounding.md`](evidence/42-kafka-081-log-compaction-grounding.md) — Case-42 grounding record: versioned Apache Kafka 0.8.1 design documentation and exact release-tag cleaner/segment source separate current-state reconstruction from complete history, stable logical offsets from record/byte-position survival, background recopy from in-place erase, and bounded delete-marker observation from Cassandra/Swift-style replica-repair windows.\n"
text = insert_after(text, ev41, ev42, "README evidence anchor")
p.write_text(text)

# ROADMAP
p = Path("ROADMAP.md")
text = p.read_text()
marker = "\nA bridge belongs here only when it changes the retention comparison. Generic technical history belongs primarily in `computing-archaeology`.\n"
new_item = "\n- [ ] append-log / changelog compaction and current-state reconstruction — **partially advanced by grounded Case 42**: [`cases/42-apache-kafka-log-compaction-delete-marker-retention.md`](cases/42-apache-kafka-log-compaction-delete-marker-retention.md), grounded by [`evidence/42-kafka-081-log-compaction-grounding.md`](evidence/42-kafka-081-log-compaction-grounding.md), uses Apache Kafka 0.8.1 design documentation plus exact release-tag cleaner/segment source to separate latest-per-key current-state reconstruction from complete history, permanent logical offsets from surviving record occupancy and physical byte position, background segment recopy from in-place deletion, and time-bounded delete-marker observation from replica-repair tombstone windows. The broad item stays unchecked because Databus mechanism genealogy, pre/post-0.8.1 Kafka compaction chronology, replication/ISR interaction, later transaction/Streams changelog semantics, compaction correctness under failure, and operational/commercial evolution remain separate regimes.\n"
text = replace_once(text, marker, new_item + marker, "ROADMAP log-compaction insertion")
p.write_text(text)

# CASE_INDEX
p = Path("CASE_INDEX.md")
text = p.read_text()
case41row = "| [Apache Cassandra GC Grace: Tombstone Retention, Repair Windows, and Data Resurrection](cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md) | **grounded** | replicated positive values + timestamped tombstone negative state + hints/repair + SSTable repaired/unrepaired state + compaction/overlap reclamation constraints | show deletion can depend on retained negative evidence; separate tombstone age, replica convergence, repair evidence, and physical reclamation; show forgetting deletion evidence can make older payload current again | [Cassandra 3.x tombstone/repair grounding](evidence/41-cassandra-3x-tombstone-repair-grounding.md); later Cassandra repair/tombstone evolution, secure erasure, cross-version semantics, and broader tombstone genealogy remain separate work |\n"
case42row = "| [Apache Kafka 0.8.1 Log Compaction: Stable Offsets, Last-Value Retention, and Time-Bounded Delete Markers](cases/42-apache-kafka-log-compaction-delete-marker-retention.md) | **grounded** | append-only keyed records + permanent logical offsets + latest-per-key compaction state + background segment recopy + bounded delete-marker retention | separate current-state reconstructability from complete history; stable logical position from surviving record/physical location; and delete-marker observation window from replica-repair tombstone semantics | [Kafka 0.8.1 log-compaction grounding](evidence/42-kafka-081-log-compaction-grounding.md); Databus genealogy, later Kafka compaction/transactions, replication interaction, and failure-correctness evolution remain separate work |\n"
text = insert_after(text, case41row, case42row, "CASE_INDEX case row")

matrix41 = "| Apache Cassandra tombstone/GC-grace / 3.x bounded regime | replicated positive values + timestamped tombstone negative currentness + hint state + repaired/unrepaired SSTable relation + compaction overlap | DELETE retains tombstones; hints can temporarily deliver missed mutations; read/anti-entropy repair converges replicas; compaction later reclaims eligible tombstones, optionally only after repaired status | a stale positive embodiment can remain physically readable yet be suppressed by a newer tombstone; after deletion evidence is lost, repair can make that older value current again | logical partition/row/column designation resolves across replicas and timestamped states; compaction additionally reasons over SSTable overlap and repaired status | positive and negative embodiments can coexist across replicas/SSTables; deletion identity is relational rather than one physical absence | no complete history; bounded negative currentness, repair status, hints, and reclamation-control state are retained long enough to sustain deletion |\n"
matrix42 = "| Apache Kafka log compaction / 0.8.1 bounded regime | keyed append records + permanent logical offsets + latest-offset-per-key cleaner summary + segment/index embodiments + bounded delete-marker state | background cleaner selects dirty logs, builds key→last-offset map, recopies segments omitting superseded records, swaps clean segments, and later omits expired delete markers | consumer reads from a logical offset and receives the first surviving message at or above it; traversal must catch the head within delete retention to be guaranteed to observe all delete markers | topic/partition + logical offset → segment/index → physical file position; removed offsets remain valid traversal positions | surviving records can move to recopied segment/file positions while offsets/order remain; removed positions remain logically meaningful without their original record | deliberately incomplete history: at least final keyed state is retained, while superseded values and eventually delete markers are forgotten |\n"
text = insert_after(text, matrix41, matrix42, "CASE_INDEX matrix row")

text = replace_once(
    text,
    "After forty-two bounded cases, **all forty-two cases are now `grounded`.**",
    "After forty-three bounded cases, **all forty-three cases are now `grounded`.**",
    "CASE_INDEX synthesis count",
)

old80 = "80. **category coherence is provisional and evidence-gated** — forty-two grounded regimes now support the current relational criterion, including the grounded delay-line circulation/temperature-control regime plus powered flip-flop, static-MOS, cache-policy, refresh-address-internalization, autonomous leakage-tracked refresh-scheduling, SDRAM refresh-mode handoff, floating-gate EPROM erase-asymmetry, byte-erasable EEPROM, coarse-erase early Flash, HDD defect-reassignment, SSD power-loss-durability, BSD FFS crash-admissibility, RAID parity-reconstruction, ZFS proactive-scrubbing, f4 distributed-erasure-coding, NVMe 1.0 persistence-interface, IBM paging/backing-copy-currentness, Dynamo divergent-version/anti-entropy, Windows Azure LRC repair-locality/representation-handoff, Swift mutable-EC currentness, GFS distributed-integrity-verification, Ceph EC checksum-authority/deep-scrub, Swift distributed-delete/tombstone-consistency, Ceph Luminous scrub-repair-authority, NVMe 1.4 persistent-memory-region, SNIA persistence-domain, Intel ADR/eADR power-fail-domain, DDR5 same-bank-refresh-localization, temperature-conditioned DRAM-refresh, commercial Mobile-DDR automatic-TCSR/selective-retention, NAND-Flash FCR controller-maintenance, commercial Samsung 840 EVO old-data performance-refresh, Intel DC S3700/S3500 PLI-health/validation, GeckoFTL controller-metadata-recovery, RAIDR retention-profile/row-selective-refresh, and Cassandra tombstone/repair-window bridges; future write-back-cache, filesystem, refresh, virtual-memory, and distributed regimes must still be allowed to break or revise it rather than being forced into it;"
new80 = "80. **category coherence is provisional and evidence-gated** — forty-three grounded regimes now support the current relational criterion, including the grounded delay-line circulation/temperature-control regime plus powered flip-flop, static-MOS, cache-policy, refresh-address-internalization, autonomous leakage-tracked refresh-scheduling, SDRAM refresh-mode handoff, floating-gate EPROM erase-asymmetry, byte-erasable EEPROM, coarse-erase early Flash, HDD defect-reassignment, SSD power-loss-durability, BSD FFS crash-admissibility, RAID parity-reconstruction, ZFS proactive-scrubbing, f4 distributed-erasure-coding, NVMe 1.0 persistence-interface, IBM paging/backing-copy-currentness, Dynamo divergent-version/anti-entropy, Windows Azure LRC repair-locality/representation-handoff, Swift mutable-EC currentness, GFS distributed-integrity-verification, Ceph EC checksum-authority/deep-scrub, Swift distributed-delete/tombstone-consistency, Ceph Luminous scrub-repair-authority, NVMe 1.4 persistent-memory-region, SNIA persistence-domain, Intel ADR/eADR power-fail-domain, DDR5 same-bank-refresh-localization, temperature-conditioned DRAM-refresh, commercial Mobile-DDR automatic-TCSR/selective-retention, NAND-Flash FCR controller-maintenance, commercial Samsung 840 EVO old-data performance-refresh, Intel DC S3700/S3500 PLI-health/validation, GeckoFTL controller-metadata-recovery, RAIDR retention-profile/row-selective-refresh, Cassandra tombstone/repair-window, and Kafka log-compaction/delete-marker-retention bridges; future write-back-cache, filesystem, refresh, virtual-memory, distributed, and log-compaction regimes must still be allowed to break or revise it rather than being forced into it;"
text = replace_once(text, old80, new80, "CASE_INDEX finding 80 count")

finding390 = "390. **tombstone reclamation ≠ secure erasure** — removing Cassandra's negative currentness marker is a distributed-storage reclamation event; it does not establish sanitization of every stale physical copy or lower-layer media trace.\n"
new_findings = """
391. **current-state reconstructability ≠ complete history retention** — Kafka 0.8.1 explicitly uses compaction to retain at least the final value for every key without retaining a complete log of all changes; being able to rebuild `now` does not imply being able to replay every prior state.
392. **stable logical offset ≠ surviving record at that offset** — compacted-away records do not cause offset renumbering; Apache says the offset remains a valid position and a read continues from the next surviving offset.
393. **ordering continuity ≠ dense record occupancy** — compaction never reorders surviving messages but deliberately creates holes where older records were removed; ordered traversal and complete occupancy are separate relations.
394. **stable logical position ≠ stable physical byte position** — the 0.8.1 segment source explicitly maps logical offsets to physical file positions while the cleaner recopies and swaps segment embodiments; logical position can remain fixed while physical placement changes.
395. **compaction-mediated forgetting ≠ in-place record erasure** — Kafka 0.8.1 forgets superseded history by constructing cleaned segments that copy survivors and omit obsolete records, making preservation of the current state and physical reconstruction of its carrier one coupled operation.
396. **delete-marker retention ≠ indefinite negative-state retention** — a null-payload delete marker first defeats older same-key values, but Kafka deliberately removes the marker itself after its configured retention relation so negative state does not accumulate forever.
397. **observer progress can be part of a retention guarantee** — Apache guarantees that a start-to-head consumer sees all delete markers only if it catches up within `delete.retention.ms`; whether the negative state remains observable can depend on reader traversal time while cleanup proceeds concurrently.
398. **Kafka `delete.retention.ms` ≠ Cassandra `gc_grace_seconds` ≠ Swift `reclaim_age`** — all three can bound negative-state lifetime, but Kafka's bounded relation is compacted-log consumer observation, Cassandra's is stale-replica/repair anti-resurrection safety, and Swift's is timestamped replica/reconstruction convergence; vocabulary similarity does not establish mechanism identity.
399. **compaction ≠ time-based retention** — Kafka 0.8.1 explicitly distinguishes per-key compaction from coarse age/size deletion: one retains a latest keyed state even when old, while the other can discard old records regardless of whether they are the only surviving state for a key.
400. **source-of-current-state role ≠ point-in-time archive role** — a compacted Kafka topic can remain a source from which current keyed state is rebuilt while no longer retaining enough superseded records to reproduce arbitrary historical points; `source of truth` for current state does not mean complete historical archive.
"""
text = insert_after(text, finding390, new_findings, "CASE_INDEX new findings")
p.write_text(text)

# Sanity checks
assert Path("cases/42-apache-kafka-log-compaction-delete-marker-retention.md").exists()
assert Path("evidence/42-kafka-081-log-compaction-grounding.md").exists()
for path in [Path("README.md"), Path("ROADMAP.md"), Path("CASE_INDEX.md")]:
    data = path.read_text()
    if "42-apache-kafka-log-compaction-delete-marker-retention" not in data:
        raise SystemExit(f"Case 42 missing from {path}")

if "After forty-three bounded cases" not in Path("CASE_INDEX.md").read_text():
    raise SystemExit("CASE_INDEX count not updated")
if "400. **source-of-current-state role" not in Path("CASE_INDEX.md").read_text():
    raise SystemExit("Case 42 findings not integrated")

print("Case 42 navigation/status integration completed")
