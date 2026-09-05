from pathlib import Path

CASE_PATH = 'cases/90-apache-kafka-leader-epoch-safe-truncation.md'
EVID_PATH = 'evidence/90-kafka-2016-2017-leader-epoch-truncation-grounding.md'


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
readme_line = "- [`cases/90-apache-kafka-leader-epoch-safe-truncation.md`](cases/90-apache-kafka-leader-epoch-safe-truncation.md) — grounded replicated-log recovery bridge: Kafka 0.11/KIP-101 retains per-replica leader-epoch→start-offset lineage in `leader-epoch-checkpoint`, enters an explicit truncation phase before ordinary follower fetching, and can deliberately discard a longer surviving suffix when the leader-qualified epoch boundary shows it is divergent; this deepens Case 56 by separating committed-prefix high-watermark state from recovery-lineage state; see [`evidence/90-kafka-2016-2017-leader-epoch-truncation-grounding.md`](evidence/90-kafka-2016-2017-leader-epoch-truncation-grounding.md)."
text = insert_after_line(text, 'cases/89-ata-lba-chs-translation-logical-sector-identity.md', readme_line)
p.write_text(text)

# ROADMAP latest bridge
p = Path('ROADMAP.md')
text = p.read_text()
roadmap_line = "- [x] Kafka KIP-101 leader-epoch recovery / lineage-qualified truncation — [`cases/90-apache-kafka-leader-epoch-safe-truncation.md`](cases/90-apache-kafka-leader-epoch-safe-truncation.md), grounded by [`evidence/90-kafka-2016-2017-leader-epoch-truncation-grounding.md`](evidence/90-kafka-2016-2017-leader-epoch-truncation-grounding.md), deepens Case 56 without repeating Kafka replication history: the 0.11 path retains an epoch→start-offset checkpoint, queries the current leader before follower fetching resumes, and uses the returned epoch end to qualify/truncate divergent suffixes. This separates high-watermark committed-prefix state from retained recovery lineage, while preserving compatibility fallback and KIP-101's explicit unclean-election limit. Pre-Kafka epoch genealogy, later KIP refinements, KRaft, and production fault-injection remain separate work."
text = insert_after_line(text, 'cases/89-ata-lba-chs-translation-logical-sector-identity.md', roadmap_line)
p.write_text(text)

# CASE_INDEX ledger, matrix, aggregate and findings
p = Path('CASE_INDEX.md')
text = p.read_text()
ledger_line = "| [Apache Kafka 0.11 Leader-Epoch Recovery: Log Lineage, Safe Truncation, and Retained Recovery Metadata](cases/90-apache-kafka-leader-epoch-safe-truncation.md) | **grounded** | replicated partition log + leader epochs + per-replica epoch→start-offset checkpoint + `OffsetsForLeaderEpoch` exchange + explicit follower truncation phase | separate committed-prefix high watermark from recovery lineage; distinguish physical suffix survival from common-lineage authority; show epoch metadata must itself be pruned/reconciled with the retained log | [2016–2017 Kafka leader-epoch grounding](evidence/90-kafka-2016-2017-leader-epoch-truncation-grounding.md); pre-Kafka epoch genealogy, later KIP refinements, KRaft, production incident/fault tests, and media-forensic truncation remain separate work |"
text = insert_after_line(text, 'cases/89-ata-lba-chs-translation-logical-sector-identity.md', ledger_line)
matrix_row = "| Apache Kafka 0.11 / KIP-101 leader-epoch recovery | replicated log records + per-replica leader-epoch→start-offset lineage + high watermark/LEO + truncation-phase control state | leader/follower transition triggers epoch query and lineage-qualified truncation before ordinary fetching; epoch entries are flushed and pruned/reconciled with log lifetime | ordinary follower replication resumes only after truncation completes; a longer surviving suffix can be rejected when the leader epoch boundary marks divergence | partition identity + leader epoch + start/end offsets identify a common leadership lineage; high watermark remains a distinct commit/visibility boundary | physical log tail can be shortened deliberately while the partition identity/current history persists | no complete operation history; sparse leadership-boundary history is retained only as long as needed to qualify surviving log lineage |"
marker = '## Cross-case findings already supported'
if matrix_row not in text:
    if marker not in text:
        raise RuntimeError('matrix marker missing')
    text = text.replace(marker, matrix_row + '\n\n' + marker, 1)
old = 'After ninety bounded cases, **all ninety cases are now `grounded`.**'
new = 'After ninety-one bounded cases, **all ninety-one cases are now `grounded`.**'
if old not in text and new not in text:
    raise RuntimeError('aggregate sentence missing')
text = text.replace(old, new, 1)
findings = """

### Case 90 — Kafka leader-epoch recovery findings

1117. **high watermark ≠ complete recovery lineage** — KIP-101's motivating failure shows that a follower's retained HW can lag a commitment fact learned by the leader, so HW alone can be unsafe as the sole initialization-truncation witness.
1118. **physical suffix survival ≠ authoritative suffix** — a follower can retain readable records beyond the leader-qualified common epoch boundary and correctly truncate them.
1119. **log-end offset ≠ lineage equivalence** — replica length alone does not show whether suffixes were generated in the same leadership history.
1120. **leader epoch ≠ wall-clock time** — Kafka's epoch orders leadership periods for one partition rather than measuring elapsed time.
1121. **leader-epoch checkpoint ≠ user payload** — `leader-epoch-checkpoint` retains epoch/start-offset boundary metadata used to qualify recovery, while records remain in the partition log.
1122. **epoch boundary history ≠ complete operation history** — the checkpoint stores sparse leadership starts, not every produce, fetch, acknowledgement, ISR transition, or truncation event.
1123. **durable recovery metadata ≠ immutable recovery metadata** — epoch entries must be removed/adjusted as the log is truncated or its retained prefix advances, and KIP-101 requires reconciliation when sequence state extends beyond surviving LEO after unclean shutdown.
1124. **more retained metadata ≠ safer recovery** — retaining epoch entries that no longer correspond to the surviving log can misdescribe lineage; correct forgetting of stale metadata is part of keeping the recovery relation valid.
1125. **recovery query ≠ ordinary replication fetch** — 0.11 follower state separates the truncation/epoch-query phase from the later ready-for-fetch phase.
1126. **recovery ordering is constitutive state** — lineage qualification and truncation occur before ordinary fetching resumes, preventing the follower from composing new replication traffic with an unresolved divergent suffix.
1127. **lineage-qualified truncation ≠ secure erasure** — logical removal of a divergent Kafka suffix establishes protocol convergence, not forensic sanitization of the underlying medium.
1128. **KIP-101 leader epochs ≠ replacement of high watermark** — high watermark remains a separate commit/visibility relation and an explicit fallback when epoch information is unavailable.
1129. **compatibility fallback ≠ semantic identity** — the ability to fall back from epoch-based truncation to HW-based truncation does not mean those retained states contain the same information.
1130. **Kafka Leader Epoch ≠ HDFS QJM epoch by shared name alone** — Case 50 uses epoch to fence journal-writer authority; Case 90 uses epoch boundaries to qualify replicated-log lineage. The comparison is functional/terminological, not genealogical.
1131. **recovery-sufficient history can be sparse** — like Case 88's bounded recovery evidence in a different domain, Kafka can preserve enough historical structure for recovery without preserving a complete duplicate history; no technical descent is implied.
1132. **correct forgetting can preserve historical continuity** — removing a physically surviving but divergent suffix can be the operation that restores one continuing replicated history, provided the authority boundary is established by the sourced protocol rather than inferred from material survival alone.
"""
if '1117. **high watermark ≠ complete recovery lineage**' not in text:
    text = text.rstrip() + findings + '\n'
p.write_text(text)

# Validate cross-navigation before removing one-shot integration machinery.
for path in ['README.md', 'ROADMAP.md', 'CASE_INDEX.md']:
    t = Path(path).read_text()
    if CASE_PATH not in t:
        raise RuntimeError(f'{path} missing Case 90 navigation')
if EVID_PATH not in Path('README.md').read_text() or EVID_PATH not in Path('ROADMAP.md').read_text() or EVID_PATH not in Path('CASE_INDEX.md').read_text():
    raise RuntimeError('grounding navigation incomplete')
if 'After ninety-one bounded cases, **all ninety-one cases are now `grounded`.**' not in Path('CASE_INDEX.md').read_text():
    raise RuntimeError('aggregate status not updated')

Path('.github/scripts/case90_integrate.py').unlink(missing_ok=True)
Path('.github/workflows/case90-integration.yml').unlink(missing_ok=True)
