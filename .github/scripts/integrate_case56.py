from pathlib import Path

CASE_PATH = 'cases/56-apache-kafka-replicated-log-high-watermark.md'
EVIDENCE_PATH = 'evidence/56-kafka-082-replication-high-watermark-grounding.md'

case_link = "- [`cases/56-apache-kafka-replicated-log-high-watermark.md`](cases/56-apache-kafka-replicated-log-high-watermark.md) — grounded Kafka 0.8.2 replicated-log bridge: ISR membership and per-replica progress define a high-watermark committed prefix that caps ordinary consumer reads, while periodic checkpointing retains a recovery boundary and unclean-election recovery can deliberately truncate a longer but non-authoritative suffix."
ev_link = "- [`evidence/56-kafka-082-replication-high-watermark-grounding.md`](evidence/56-kafka-082-replication-high-watermark-grounding.md) — Case-56 grounding record: versioned Apache 0.8.2 design/config plus exact `0.8.2.0` Partition/ReplicaManager/ReplicaFetcherThread source ground ISR currentness, high-watermark computation/consumer visibility, disk checkpointing, and bounded unclean-election truncation; PacificA is retained as prior-art boundary rather than an origin claim."

# README
p = Path('README.md')
s = p.read_text()
lines = s.splitlines()
if CASE_PATH not in s:
    i = next(i for i,l in enumerate(lines) if 'cases/55-nvme-smart-health-endurance-telemetry.md' in l)
    lines.insert(i + 1, case_link)
if EVIDENCE_PATH not in '\n'.join(lines):
    try:
        j = next(i for i,l in enumerate(lines) if 'evidence/55-nvme10-13-smart-health-endurance-grounding.md' in l)
        lines.insert(j + 1, ev_link)
    except StopIteration:
        pass
p.write_text('\n'.join(lines) + '\n')

# ROADMAP
p = Path('ROADMAP.md')
s = p.read_text()
if CASE_PATH not in s:
    lines = s.splitlines()
    idx = next(i for i,l in enumerate(lines) if l.startswith('- [ ] distributed replication and erasure coding beyond RADOS'))
    line = lines[idx]
    line = line.replace('Cases 19, 23, 24, 25, 26, 27, 28, 29, 41, 46, 48, 49, 50, and 51',
                        'Cases 19, 23, 24, 25, 26, 27, 28, 29, 41, 46, 48, 49, 50, 51, and 56')
    sentence = " [`cases/56-apache-kafka-replicated-log-high-watermark.md`](cases/56-apache-kafka-replicated-log-high-watermark.md), grounded by [`evidence/56-kafka-082-replication-high-watermark-grounding.md`](evidence/56-kafka-082-replication-high-watermark-grounding.md), adds a replicated-log committed-prefix regime: current ISR progress sets a high watermark that bounds ordinary consumer visibility, the watermark has a separate disk-checkpoint embodiment for recovery, and an uncleanly elected shorter leader can force a returning longer replica to truncate. This keeps assigned replication, replica currentness, physical suffix survival, committed-prefix visibility, and failover authority distinct."
    marker = ' The broad item stays unchecked'
    if marker in line:
        line = line.replace(marker, sentence + marker, 1)
    else:
        line = line.rstrip(';') + sentence + ';'
    lines[idx] = line
    s = '\n'.join(lines) + '\n'
q = '- [ ] In a replicated log, how should physical suffix survival, replica currentness, committed-prefix/high-watermark state, consumer visibility, and failover truncation authority be separated?'
if q not in s:
    anchor = '- [ ] When replicas disagree, is `currentness` itself retained metadata/protocol state?'
    if anchor in s:
        s = s.replace(anchor, anchor + '\n' + q, 1)
p.write_text(s)

# CASE_INDEX case row
p = Path('CASE_INDEX.md')
s = p.read_text()
row = "| [Apache Kafka 0.8.2 Replicated Log: High Watermark, ISR Currentness, and Failover Truncation](cases/56-apache-kafka-replicated-log-high-watermark.md) | **grounded** | partition replicas + leader/ISR currentness + per-replica LEO + high-watermark committed prefix + disk checkpoint + optional unclean-election truncation | separate physical suffix survival from committed visibility; assignment from current redundancy margin; current ISR authority from mere replica presence; and recovery convergence from maximal-byte preservation | [0.8.2 replication/high-watermark grounding](evidence/56-kafka-082-replication-high-watermark-grounding.md); 0.11+ leader-epoch recovery, KRaft, transactions/last-stable-offset, independent fault injection, and lower-layer durability composition remain separate work |"
if CASE_PATH not in s:
    lines = s.splitlines()
    i = next(i for i,l in enumerate(lines) if l.startswith('| [') and 'cases/55-nvme-smart-health-endurance-telemetry.md' in l)
    lines.insert(i + 1, row)
    s = '\n'.join(lines) + '\n'

# Explicit total-count phrases only.
for old,new in [
    ('56 bounded cases','57 bounded cases'),
    ('all 56 cases','all 57 cases'),
    ('fifty-six bounded cases','fifty-seven bounded cases'),
    ('fifty-six cases','fifty-seven cases'),
]:
    s = s.replace(old,new)

findings = r'''

## Case 56 — replicated-log committed-prefix findings

575. **Physical record presence ≠ committed retention.** Kafka 0.8.2 can retain records above the high watermark in a local log while ordinary consumers remain bounded to the committed prefix.
576. **Leader log-end offset ≠ committed frontier.** The leader may possess a longer suffix than the slowest current ISR replica; the high watermark advances from the minimum ISR log-end frontier.
577. **Replication factor ≠ current redundancy margin.** Assigned replicas describe intended multiplicity; ISR membership describes currently qualified replication participants.
578. **Assigned replica membership ≠ replica currentness.** A physically present assigned replica can be removed from ISR when it is too far behind or stuck.
579. **Follower catch-up ≠ immediate currentness until the ISR condition is satisfied.** In the bounded source, a follower can re-enter ISR only after reaching at least the leader high watermark plus the assignment/membership checks.
580. **Follower-replication visibility ≠ ordinary consumer visibility.** Replica fetches may copy the leader tail beyond the high watermark because that copying is how commitment can advance; ordinary consumer reads are capped at the high watermark.
581. **Follower log end ≠ follower committed prefix.** The follower sets its high watermark to the minimum of its own log end and the leader-reported high watermark.
582. **Retained high-watermark checkpoint ≠ retained replication history.** `replication-offset-checkpoint` preserves a recovery boundary without recording every fetch, lag transition, or ISR change that produced it.
583. **Runtime high watermark ≠ necessarily the most recently checkpointed high watermark at every instant.** The 0.8.2 configuration explicitly checkpoints periodically; this distinction does not by itself imply data loss because recovery uses more than one relation.
584. **`request.required.acks=-1` ≠ acknowledgement by every assigned replica.** In the bounded regime it composes with the current ISR/high-watermark path and `min.insync.replicas`.
585. **Longer surviving log ≠ more authoritative log.** The unclean-election recovery path can truncate a returning follower whose local end lies beyond the current leader end.
586. **Failover convergence can require deliberate forgetting.** Truncating an extant divergent suffix is a protocol repair/convergence operation, not evidence that those bytes were physically absent.
587. **Unclean leader election availability ≠ the normal committed-message retention guarantee.** Electing a non-ISR replica can restore service while explicitly accepting possible data loss.
588. **Kafka replication truncation ≠ Kafka log compaction.** Case 42 forgets superseded committed keyed history; Case 56 can forget a non-authoritative/divergent suffix during replica convergence.
589. **Kafka high watermark/ISR ≠ generic quorum or consensus semantics.** Kafka's own design situates the mechanism among earlier replicated-log work and names PacificA as close prior art; the project keeps the 0.8.2 implementation specific rather than turning all commit-frontier mechanisms into one genealogy.
'''
if '## Case 56 — replicated-log committed-prefix findings' not in s:
    s = s.rstrip() + findings + '\n'
p.write_text(s)

# Validation
assert Path(CASE_PATH).exists()
assert Path(EVIDENCE_PATH).exists()
assert CASE_PATH in Path('README.md').read_text()
assert CASE_PATH in Path('ROADMAP.md').read_text()
ci = Path('CASE_INDEX.md').read_text()
assert ci.count(CASE_PATH) >= 1
assert '589.' in ci
