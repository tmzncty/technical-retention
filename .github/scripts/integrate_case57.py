from pathlib import Path
import zlib

CASE_PATH = "cases/57-google-bigtable-tablet-log-memtable-recovery.md"
EVIDENCE_PATH = "evidence/57-bigtable-2006-log-memtable-sstable-grounding.md"

Path(CASE_PATH).write_text(zlib.decompress(Path(".github/payloads/case57.zlib").read_bytes()).decode("utf-8"))
Path(EVIDENCE_PATH).write_text(zlib.decompress(Path(".github/payloads/evidence57.zlib").read_bytes()).decode("utf-8"))

# README navigation
p = Path("README.md")
s = p.read_text()
case_link = "- [`cases/57-google-bigtable-tablet-log-memtable-recovery.md`](cases/57-google-bigtable-tablet-log-memtable-recovery.md) — grounded Google Bigtable 2006 tablet-recovery bridge: commit-log redo precedes volatile memtable insertion; reads merge memtable with immutable SSTables; METADATA live-file membership and redo points make tablet recovery possible; compaction can reduce future replay while retiring obsolete positive/negative state."
ev_link = "- [`evidence/57-bigtable-2006-log-memtable-sstable-grounding.md`](evidence/57-bigtable-2006-log-memtable-sstable-grounding.md) — Case-57 grounding record: Chang et al. OSDI 2006 primary evidence grounds commit-before-memtable ordering, SSTable/materialization, recovery via live files plus redo points, shared-log recovery sorting/deduplication, compaction/deletion semantics, and an explicit LSM-tree prior-art boundary."
lines = s.splitlines()
if CASE_PATH not in s:
    i = next(i for i,l in enumerate(lines) if "cases/56-apache-kafka-replicated-log-high-watermark.md" in l)
    lines.insert(i + 1, case_link)
s = "\n".join(lines) + "\n"
if EVIDENCE_PATH not in s:
    lines = s.splitlines()
    try:
        j = next(i for i,l in enumerate(lines) if "evidence/56-kafka-082-replication-high-watermark-grounding.md" in l)
        lines.insert(j + 1, ev_link)
    except StopIteration:
        j = next(i for i,l in enumerate(lines) if "cases/57-google-bigtable-tablet-log-memtable-recovery.md" in l)
        lines.insert(j + 1, ev_link)
    s = "\n".join(lines) + "\n"
p.write_text(s)

# ROADMAP
p = Path("ROADMAP.md")
s = p.read_text()
lines = s.splitlines()

idx = next(i for i,l in enumerate(lines) if l.startswith("- [ ] distributed replication and erasure coding beyond RADOS"))
line = lines[idx]
line = line.replace("Cases 19, 23, 24, 25, 26, 27, 28, 29, 41, 46, 48, 49, 50, 51, and 56",
                    "Cases 19, 23, 24, 25, 26, 27, 28, 29, 41, 46, 48, 49, 50, 51, 56, and 57")
if CASE_PATH not in line:
    sentence = " [`cases/57-google-bigtable-tablet-log-memtable-recovery.md`](cases/57-google-bigtable-tablet-log-memtable-recovery.md), grounded by [`evidence/57-bigtable-2006-log-memtable-sstable-grounding.md`](evidence/57-bigtable-2006-log-memtable-sstable-grounding.md), adds a tablet-server recovery/materialization regime: Bigtable commits mutation redo before volatile memtable insertion; persistent `METADATA` names the live SSTables and redo points needed for recovery; minor compaction materializes recent state and reduces future replay; and one shared physical tablet-server log can later be sorted back into logical tablet streams. This separates committed mutation, volatile serving embodiment, current materialized files, replay boundary, and recovery work."
    marker = " The broad item stays unchecked"
    line = line.replace(marker, sentence + marker, 1)
lines[idx] = line

idx2 = next(i for i,l in enumerate(lines) if l.startswith("- [ ] append-log / changelog compaction and current-state reconstruction"))
line2 = lines[idx2]
line2 = line2.replace("partially advanced by grounded Case 42", "partially advanced by grounded Cases 42 and 57")
if CASE_PATH not in line2:
    sentence2 = " [`cases/57-google-bigtable-tablet-log-memtable-recovery.md`](cases/57-google-bigtable-tablet-log-memtable-recovery.md), grounded by [`evidence/57-bigtable-2006-log-memtable-sstable-grounding.md`](evidence/57-bigtable-2006-log-memtable-sstable-grounding.md), adds the complementary redo/materialization path: committed updates first acquire redo evidence, volatile memtable state can be reconstructed, immutable SSTables become replacement materializations, and advancing redo points can make older recovery-history prefixes dispensable. This is not Kafka's stable-offset keyed compaction contract."
    marker = " The broad item stays unchecked"
    line2 = line2.replace(marker, sentence2 + marker, 1)
lines[idx2] = line2
s = "\n".join(lines) + "\n"

q = "- [ ] In log-structured tablet recovery, how should committed redo history, volatile memtable state, immutable materialized files, live-file membership, redo points, replay cost, and deletion-marker retirement be separated?"
if q not in s:
    anchor = "- [ ] In a replicated log, how should physical suffix survival, replica currentness, committed-prefix/high-watermark state, consumer visibility, and failover truncation authority be separated?"
    if anchor in s:
        s = s.replace(anchor, anchor + "\n" + q, 1)

maint = "- commit-log replay, memtable materialization, SSTable compaction, live-file membership, and obsolete-file garbage collection;"
if maint not in s:
    anchor = "- distributed peering/repair/anti-entropy;"
    if anchor in s:
        s = s.replace(anchor, maint + "\n" + anchor, 1)
p.write_text(s)

# CASE_INDEX row + count + comparison + findings
p = Path("CASE_INDEX.md")
s = p.read_text()
row = "| [Google Bigtable 2006 Tablet Recovery: Commit Log, Memtable, SSTable Compaction, and Redo Points](cases/57-google-bigtable-tablet-log-memtable-recovery.md) | **grounded** | GFS-backed commit-log redo + volatile memtable + immutable SSTables + METADATA live-file/redo-point state + compaction/replay | separate committed mutation from volatile serving embodiment; current readable view from one physical file; replay history from replay boundary; compaction from initial durability; deletion currentness from lower-layer erasure | [2006 Bigtable log/memtable/SSTable grounding](evidence/57-bigtable-2006-log-memtable-sstable-grounding.md); source-code crash-window archaeology, later Bigtable/Cloud Bigtable semantics, independent fault injection, and lower-layer GFS/media composition remain separate work |"
if CASE_PATH not in s:
    lines = s.splitlines()
    i = next(i for i,l in enumerate(lines) if l.startswith("| [") and "cases/56-apache-kafka-replicated-log-high-watermark.md" in l)
    lines.insert(i + 1, row)
    s = "\n".join(lines) + "\n"

for old,new in [
    ("57 bounded cases","58 bounded cases"),
    ("all 57 cases","all 58 cases"),
    ("fifty-seven bounded cases","fifty-eight bounded cases"),
    ("fifty-seven cases","fifty-eight cases"),
]:
    s = s.replace(old,new)

matrix_kafka = "| Apache Kafka replicated log / 0.8.2 bounded regime | partition log records + ISR/progress/high-watermark state + disk checkpoint | follower replication, ISR qualification, high-watermark advancement, checkpointing, optional truncation after unclean election | ordinary consumer reads capped at high watermark while follower replication can fetch beyond it | topic/partition + offset + leader/ISR currentness | physical suffix can survive yet be non-authoritative and later truncated | no complete history guarantee beyond retained records; high-watermark checkpoint retains a recovery boundary, not replication event history |"
matrix_bigtable = "| Google Bigtable tablet recovery / 2006 bounded regime | GFS-backed redo log + volatile memtable + immutable SSTables + METADATA live-file/redo-point state | commit-log group commit; memtable flush/minor compaction; merging/major compaction; replay; obsolete-file GC | merged view across memtable + current SSTables | table/tablet row range + current SSTable roots + redo points | volatile memtable can disappear and be reconstructed; SSTable embodiments can be replaced by compaction | bounded redo history + optional cell-version history; old redo/materialized/deletion state becomes dispensable after safe materialization/compaction |"
marker = "\n\n---\n\n## Cross-case findings already supported"
if matrix_bigtable not in s and marker in s:
    insert = ""
    if matrix_kafka not in s:
        insert += "\n" + matrix_kafka
    insert += "\n" + matrix_bigtable
    s = s.replace(marker, insert + marker, 1)

findings = """
## Case 57 — Bigtable redo/materialization findings

590. **Committed mutation ≠ surviving memtable object.** Bigtable records a valid mutation in the commit log and commits it before inserting the same update into the volatile memtable, so RAM-object survival is not the durability condition for a committed mutation.
591. **Current readable tablet state ≠ one current physical file.** Reads merge the memtable with the live SSTables; the current tablet is a compositional view rather than one privileged file embodiment.
592. **Persistent logical state can include reconstructible volatile working state.** The memtable participates in ordinary serving while its committed contents can be recreated after tablet-server loss from retained persistent evidence.
593. **Recovery metadata ≠ payload, while recovery metadata can be retention infrastructure.** The live SSTable list and redo points do not themselves carry the user values, yet they qualify which surviving files/log ranges must be combined to reconstruct the tablet.
594. **Redo point ≠ redo history.** A redo point is a compact boundary into retained mutation history, not a record of every mutation or every recovery event.
595. **Minor compaction ≠ original commit/durability event.** Mutations can already be committed through the log before a frozen memtable is materialized as an SSTable.
596. **Current-state materialization can reduce future history-retention obligation.** Bigtable explicitly uses minor compaction to reduce the amount of commit log that recovery must read; after safe materialization, the same old redo prefix need not remain constitutive of restart.
597. **One physical commit log ≠ one logical tablet history.** A tablet server shares one log among tablets, and recovery sorts co-mingled records back by table/row/sequence rather than treating physical append adjacency as logical-tablet identity.
598. **Duplicate retained redo records ≠ duplicate logical mutation application.** Bigtable's log-switching optimization can leave duplicates, while sequence numbers let recovery elide them.
599. **Immutable SSTable survival ≠ current tablet membership.** SSTable files do not change in place, but tablet `METADATA` names the live set and obsolete files can later be garbage-collected.
600. **Deletion entry ≠ deleted payload physically absent.** A delete marker can make an older value noncurrent while that older value still remains in a live SSTable.
601. **Major-compaction forgetting ≠ raw-media sanitization.** Bigtable major compaction can omit deleted data and deletion entries from the new live representation without proving erasure from GFS replicas, disks, backups, or forensic layers.
602. **Bigtable compaction ≠ Kafka log compaction.** Both rewrite retained representations, but Bigtable's memtable/SSTable compaction has no cited Kafka-style permanent logical-offset contract.
603. **Bigtable commit log ≠ Kafka replicated log/high watermark.** Bigtable uses redo to reconstruct tablet working state; Case 56 uses ISR/high-watermark state to qualify a committed prefix of a replicated append log.
604. **Bigtable 2006 LSM/logging composition ≠ invention of LSM/logging/group commit.** Chang et al. explicitly compare the memtable/SSTable design to the 1996 LSM-tree and cite earlier logging/group-commit literature; the grounded claim is the Bigtable-specific composition and retention relation.
"""
if "## Case 57 — Bigtable redo/materialization findings" not in s:
    s = s.rstrip() + "\n\n" + findings.strip() + "\n"
p.write_text(s)

# Validation
assert Path(CASE_PATH).exists() and Path(EVIDENCE_PATH).exists()
assert CASE_PATH in Path("README.md").read_text()
road = Path("ROADMAP.md").read_text()
assert CASE_PATH in road
ci = Path("CASE_INDEX.md").read_text()
assert ci.count(CASE_PATH) >= 1
assert "After fifty-eight bounded cases" in ci
assert "604." in ci
assert matrix_bigtable in ci
