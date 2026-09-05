from pathlib import Path

CASE_PATH = 'cases/91-apache-cassandra-tombstone-grace-zombie-prevention.md'
EVID_PATH = 'evidence/91-cassandra-2006-2014-tombstone-grace-grounding.md'


def insert_after_line(text, needle, newline):
    if newline in text:
        return text
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if needle in line:
            lines.insert(i + 1, newline)
            return '\n'.join(lines) + ('\n' if text.endswith('\n') else '')
    raise RuntimeError(f'anchor not found: {needle}')


# README navigation
p = Path('README.md')
text = p.read_text()
readme_line = "- [`cases/91-apache-cassandra-tombstone-grace-zombie-prevention.md`](cases/91-apache-cassandra-tombstone-grace-zombie-prevention.md) — grounded distributed-forgetting bridge: Cassandra's tombstone is retained negative/currentness evidence rather than immediate absence; the 1.2.19 path gives it deletion/local-time state, a configurable grace interval, and overlap-aware compaction purge constraints, while CASSANDRA-7810 demonstrates that discarding an expired marker before applying its suppressive effect can resurrect data even locally; see [`evidence/91-cassandra-2006-2014-tombstone-grace-grounding.md`](evidence/91-cassandra-2006-2014-tombstone-grace-grounding.md)."
text = insert_after_line(text, 'cases/90-apache-kafka-leader-epoch-safe-truncation.md', readme_line)
p.write_text(text)

# ROADMAP latest bridge + forgetting axis
p = Path('ROADMAP.md')
text = p.read_text()
roadmap_line = "- [x] Cassandra tombstone grace / distributed deletion-evidence retention — [`cases/91-apache-cassandra-tombstone-grace-zombie-prevention.md`](cases/91-apache-cassandra-tombstone-grace-zombie-prevention.md), grounded by [`evidence/91-cassandra-2006-2014-tombstone-grace-grounding.md`](evidence/91-cassandra-2006-2014-tombstone-grace-grounding.md), adds a bounded forgetting regime in which a timestamped negative marker must temporarily outlive the value it disqualifies: 1.2.19 source grounds `DeletedColumn`, the ten-day default grace constant, and overlap-aware purge refusal; ASF CASSANDRA-7810 supplies a concrete premature-purge resurrection failure; Bigtable 2006 blocks any claim that Cassandra invented deletion entries. Exact repair/hinted-handoff genealogy, later repair-aware purge controls, range tombstones, TTL variants, and physical sanitization remain separate work."
text = insert_after_line(text, 'cases/90-apache-kafka-leader-epoch-safe-truncation.md', roadmap_line)
old_forgetting = '- [ ] logical deletion / invalidation;'
new_forgetting = '- [ ] logical deletion / invalidation — **partially advanced by grounded Cases 44, 73, 74, and now 91**: Case 91 adds distributed negative-state retention, showing that a delete can require a tombstone to remain authoritative over older SSTable/replica values until purge is locally admissible and stale replicas cannot legitimately restore the old value; broader database deletion, object lifecycle, key-destruction, and secure-erasure genealogies remain open;'
if old_forgetting in text:
    text = text.replace(old_forgetting, new_forgetting, 1)
elif new_forgetting not in text:
    raise RuntimeError('logical deletion roadmap anchor missing')
p.write_text(text)

# CASE_INDEX ledger, matrix, aggregate and findings
p = Path('CASE_INDEX.md')
text = p.read_text()
ledger_line = "| [Apache Cassandra Tombstone Grace: Retaining Deletion Evidence to Prevent Zombie Resurrection](cases/91-apache-cassandra-tombstone-grace-zombie-prevention.md) | **grounded** | timestamped deletion marker / `DeletedColumn` + older immutable SSTable/replica values + `gc_grace_seconds` + overlap-aware compaction purge + distributed repair assumption | separate logical deletion from physical disappearance; deletion evidence from deleted payload; grace expiry from purge admissibility; local absence from cluster-wide forgetting; show premature forgetting of negative state can resurrect older positive state | [2006–2014 Cassandra tombstone grounding](evidence/91-cassandra-2006-2014-tombstone-grace-grounding.md); exact early repair/hinted-handoff genealogy, later repair-aware purge controls, range/TTL tombstones, production fault injection, and media sanitization remain separate work |"
text = insert_after_line(text, 'cases/90-apache-kafka-leader-epoch-safe-truncation.md', ledger_line)

matrix_row = "| Apache Cassandra tombstone grace / compaction purge | user-value versions + timestamped deletion marker + local deletion time + grace/purge threshold + compaction overlap knowledge + distributed replica/reconciliation state | delete writes a negative marker; marker must continue to suppress older versions through compaction/replica lag; after grace and applicable closure conditions, compaction can retire obsolete marker/data | reads reject versions older than the tombstone; an unreconciled stale value can become visible again if deletion evidence disappears too early | timestamp ordering + marker presence qualify currentness; local overlap checks bound safe compaction purge; distributed correctness also depends on stale-replica reconciliation assumptions | old positive bytes may survive after logical deletion; correct reclamation can later discard both old values and the no-longer-needed negative marker | no complete operation history; a selective deletion/currentness witness is retained only while older state can still matter |"
text = insert_after_line(text, 'Apache Kafka 0.11 / KIP-101 leader-epoch recovery', matrix_row)

old = 'After ninety-one bounded cases, **all ninety-one cases are now `grounded`.**'
new = 'After ninety-two bounded cases, **all ninety-two cases are now `grounded`.**'
if old not in text and new not in text:
    raise RuntimeError('aggregate sentence missing')
text = text.replace(old, new, 1)

findings = """

### Case 91 — Cassandra tombstone-grace findings

1133. **logical deletion ≠ physical disappearance** — a newer tombstone can suppress an older value while the older value still survives in another SSTable or replica.
1134. **tombstone ≠ deleted payload** — `DeletedColumn` retains negative/currentness metadata, not a duplicate of the value it invalidates.
1135. **local deletion ≠ cluster-wide forgetting** — one replica can correctly suppress a value while an unavailable replica still retains the pre-delete version.
1136. **physical survival ≠ currentness** — a stale value can remain fully readable yet be inadmissible because a later deletion timestamp supersedes it.
1137. **grace expiry ≠ immediate purge** — `gc_grace_seconds` determines eligibility; actual tombstone removal occurs through compaction.
1138. **grace expiry ≠ sufficient local purge authority** — the 1.2.19 compaction controller still refuses purge when overlapping SSTables may retain versions at or before the deletion timestamp.
1139. **time policy ≠ proof of distributed convergence** — a grace interval gives lagging replicas an operational reconciliation window but is not itself proof that every stale embodiment has learned the delete.
1140. **forgetting can require retained negative evidence** — the system may need to remember that a value must count as forgotten until older positive representations can no longer legitimately win.
1141. **forgetting the forgetting record too early can restore old state** — Apache's zombie model makes deletion-marker loss, not payload loss, the failure that lets a stale value return.
1142. **safe purge is a closure relation, not just an age test** — local compaction must account for older shadowed versions; distributed deletion adds replica-reconciliation assumptions beyond that local condition.
1143. **purge sequencing is semantic state** — CASSANDRA-7810 shows that even one-node compaction can resurrect a row if an expired tombstone is discarded before its suppressive effect is applied.
1144. **negative-state retention ≠ complete history retention** — Cassandra preserves a selective deletion/currentness witness rather than every mutation that led to the present row state.
1145. **Cassandra tombstone ≠ JBD revoke** — both suppress older surviving state, but Case 91 operates over timestamped database versions/replicas while Case 74 governs transaction-relative journal replay; the comparison is functional only.
1146. **Cassandra deferred deletion ≠ GFS deferred deletion** — both separate user-visible deletion from later reclamation, but their authority, metadata, and cleanup mechanisms differ.
1147. **tombstone purge ≠ secure sanitization** — compaction-level logical retirement does not prove forensic erasure of the underlying disk/SSD, snapshots, or backups.
1148. **deletion evidence has a retirement point** — once older competing representations can no longer reassert themselves under the bounded recovery model, retaining the negative marker forever is no longer required for correctness and becomes reclaimable state.
"""
if '1133. **logical deletion ≠ physical disappearance**' not in text:
    text = text.rstrip() + findings + '\n'
p.write_text(text)

# Validate cross-navigation and aggregate before removing one-shot integration machinery.
for path in ['README.md', 'ROADMAP.md', 'CASE_INDEX.md']:
    t = Path(path).read_text()
    if CASE_PATH not in t:
        raise RuntimeError(f'{path} missing Case 91 navigation')
if EVID_PATH not in Path('README.md').read_text() or EVID_PATH not in Path('ROADMAP.md').read_text() or EVID_PATH not in Path('CASE_INDEX.md').read_text():
    raise RuntimeError('grounding navigation incomplete')
idx = Path('CASE_INDEX.md').read_text()
if 'After ninety-two bounded cases, **all ninety-two cases are now `grounded`.**' not in idx:
    raise RuntimeError('aggregate status not updated')
if '1148. **deletion evidence has a retirement point**' not in idx:
    raise RuntimeError('findings incomplete')
if idx.find('Apache Cassandra tombstone grace / compaction purge') > idx.find('## Cross-case findings already supported'):
    raise RuntimeError('comparison row outside matrix')

Path('.github/scripts/case91_integrate.py').unlink(missing_ok=True)
Path('.github/workflows/case91-integration.yml').unlink(missing_ok=True)
