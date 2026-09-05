from pathlib import Path

p = Path('CASE_INDEX.md')
text = p.read_text()
row = "| Apache Kafka 0.11 / KIP-101 leader-epoch recovery | replicated log records + per-replica leader-epoch→start-offset lineage + high watermark/LEO + truncation-phase control state | leader/follower transition triggers epoch query and lineage-qualified truncation before ordinary fetching; epoch entries are flushed and pruned/reconciled with log lifetime | ordinary follower replication resumes only after truncation completes; a longer surviving suffix can be rejected when the leader epoch boundary marks divergence | partition identity + leader epoch + start/end offsets identify a common leadership lineage; high watermark remains a distinct commit/visibility boundary | physical log tail can be shortened deliberately while the partition identity/current history persists | no complete operation history; sparse leadership-boundary history is retained only as long as needed to qualify surviving log lineage |"
bad = "\n\n---\n\n" + row + "\n\n## Cross-case findings already supported"
good = "\n" + row + "\n\n---\n\n## Cross-case findings already supported"
if bad not in text:
    raise RuntimeError('expected misplaced Case 90 comparison row not found')
if text.count(row) != 1:
    raise RuntimeError('Case 90 comparison row is not unique')
text = text.replace(bad, good, 1)
p.write_text(text)
Path('.github/scripts/case90_matrix_fix.py').unlink(missing_ok=True)
Path('.github/workflows/case90-matrix-fix.yml').unlink(missing_ok=True)
