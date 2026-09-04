from pathlib import Path

README = Path('README.md')
ROADMAP = Path('ROADMAP.md')
INDEX = Path('CASE_INDEX.md')
CASE = Path('cases/64-apache-kafka-transaction-coordinator-state-recovery.md')
EVIDENCE = Path('evidence/64-kafka-0110-transaction-state-recovery-grounding.md')

if not CASE.exists() or not EVIDENCE.exists():
    raise SystemExit('Case 64/evidence 64 missing before navigation integration')

case_line = "- [`cases/64-apache-kafka-transaction-coordinator-state-recovery.md`](cases/64-apache-kafka-transaction-coordinator-state-recovery.md) — grounded Kafka 0.11 coordinator-state recovery bridge: a compacted replicated `TransactionalId` state log survives coordinator RAM/role replacement; durable PREPARE state is reloaded and resumes COMMIT/ABORT marker work, while producer and coordinator epochs protect different authority generations."
evidence_line = "- [`evidence/64-kafka-0110-transaction-state-recovery-grounding.md`](evidence/64-kafka-0110-transaction-state-recovery-grounding.md) — Case-64 grounding record: exact `0.11.0.0` transaction-state manager/log/metadata/coordinator source plus KIP-98 ground durable transition-before-cache-update, cache reconstruction, PREPARE resumption, compaction, fencing boundaries, and expiration tombstones; System R prevents a false transaction-log/recovery invention claim."

text = README.read_text()
lines = text.splitlines()
if case_line not in text:
    for i, line in enumerate(lines):
        if line.startswith("- [`cases/63-apache-kafka-transactional-read-visibility.md`]"):
            lines.insert(i + 1, case_line)
            break
    else:
        raise SystemExit('README Case 63 anchor missing')
text = '\n'.join(lines) + '\n'
lines = text.splitlines()
if evidence_line not in text:
    for i, line in enumerate(lines):
        if line.startswith("- [`evidence/63-kafka-0110-transaction-lso-grounding.md`]"):
            lines.insert(i + 1, evidence_line)
            break
    else:
        raise SystemExit('README evidence 63 anchor missing')
README.write_text('\n'.join(lines).rstrip() + '\n')

text = ROADMAP.read_text()
lines = text.splitlines()
for i, line in enumerate(lines):
    if line.startswith('- [ ] distributed replication and erasure coding beyond RADOS'):
        old_cases = 'Cases 19, 23, 24, 25, 26, 27, 28, 29, 41, 46, 48, 49, 50, 51, 56, 57, 58, 61, and 63'
        new_cases = 'Cases 19, 23, 24, 25, 26, 27, 28, 29, 41, 46, 48, 49, 50, 51, 56, 57, 58, 61, 63, and 64'
        if old_cases in line:
            line = line.replace(old_cases, new_cases, 1)
        elif new_cases not in line:
            raise SystemExit('distributed case-count anchor missing')
        if 'cases/64-apache-kafka-transaction-coordinator-state-recovery.md' not in line:
            insert = " [`cases/64-apache-kafka-transaction-coordinator-state-recovery.md`](cases/64-apache-kafka-transaction-coordinator-state-recovery.md), grounded by [`evidence/64-kafka-0110-transaction-state-recovery-grounding.md`](evidence/64-kafka-0110-transaction-state-recovery-grounding.md), adds the coordinator-side recovery layer left outside Case 63: Kafka 0.11 stores per-`TransactionalId` transaction metadata in a replicated compacted internal topic, reconstructs the active coordinator cache on transaction-state partition leadership, and resumes marker propagation when a recovered state is `PrepareCommit` or `PrepareAbort`. Durable coordinator state, process-local cache, producer fencing, coordinator ownership, and participant completion remain separate relations."
            marker = ' The broad item stays unchecked because'
            pos = line.find(marker)
            if pos < 0:
                raise SystemExit('distributed remaining-work marker missing')
            line = line[:pos] + insert + line[pos:]
        lines[i] = line
        break
else:
    raise SystemExit('distributed roadmap bullet missing')

for i, line in enumerate(lines):
    if line.startswith('- [ ] append-log / changelog compaction and current-state reconstruction'):
        old_cases = 'partially advanced by grounded Cases 42, 57, 58, and 63'
        new_cases = 'partially advanced by grounded Cases 42, 57, 58, 63, and 64'
        if old_cases in line:
            line = line.replace(old_cases, new_cases, 1)
        elif new_cases not in line:
            raise SystemExit('append-log case-count anchor missing')
        if 'cases/64-apache-kafka-transaction-coordinator-state-recovery.md' not in line:
            insert = " [`cases/64-apache-kafka-transaction-coordinator-state-recovery.md`](cases/64-apache-kafka-transaction-coordinator-state-recovery.md), grounded by [`evidence/64-kafka-0110-transaction-state-recovery-grounding.md`](evidence/64-kafka-0110-transaction-state-recovery-grounding.md), adds a distinct compacted state-store/recovery composition inside Kafka itself: coordinator RAM is rebuilt from the keyed transaction-state log, superseded transaction-state transitions need not survive indefinitely, and retained PREPARE state can require a replacement coordinator to resume already-selected completion work. This is distinct from user-topic compaction in Case 42 and transaction read filtering in Case 63."
            marker = ' The broad item stays unchecked because'
            pos = line.find(marker)
            if pos < 0:
                raise SystemExit('append-log remaining-work marker missing')
            line = line[:pos] + insert + line[pos:]
        line = line.replace('post-0.11 transaction evolution, compaction correctness under failure', 'post-0.11 transaction/coordinator evolution, compaction correctness under failure')
        lines[i] = line
        break
else:
    raise SystemExit('append-log roadmap bullet missing')
ROADMAP.write_text('\n'.join(lines).rstrip() + '\n')

text = INDEX.read_text()
row = "| [Apache Kafka 0.11 Transaction Coordinator State Recovery: Compacted Current State, Failover Reload, and Resumed Completion](cases/64-apache-kafka-transaction-coordinator-state-recovery.md) | **grounded** | replicated internal transaction-state topic + `TransactionalId`-keyed compacted metadata + role-local coordinator cache + durable PREPARE/final states + producer/coordinator epochs + expiration tombstones | separate coordinator RAM from durable transaction state; pending intent from durably admitted transition; recovered decision direction from remaining marker work; producer fencing from coordinator ownership; and current-state retention from complete transition history | [0.11.0.0 coordinator-state recovery grounding](evidence/64-kafka-0110-transaction-state-recovery-grounding.md); post-0.11 coordinator evolution, KRaft redesign, independent failover fault injection, Streams state composition, and state-topic corruption/loss remain separate work |"
if row not in text:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith('| [Apache Kafka 0.11 Transactional Read Visibility:'):
            lines.insert(i + 1, row)
            break
    else:
        raise SystemExit('CASE_INDEX Case 63 row anchor missing')
    text = '\n'.join(lines) + '\n'
text = text.replace(
    'transaction-coordinator state-log recovery, post-0.11 correctness/defense evolution, Streams processing/changelog semantics, compaction interaction, independent fault injection, and lower-layer durability composition remain separate work',
    'post-0.11 correctness/defense and coordinator evolution, Streams processing/changelog semantics, compaction interaction, independent fault injection, and lower-layer durability composition remain separate work',
    1,
)

matrix_row = "| Apache Kafka transaction coordinator / 0.11.0.0 bounded regime | `TransactionalId`-keyed internal transaction metadata + producer/status/participant/timing fields + replicated compacted state log + role-local cache + producer/coordinator epochs | proposed state transition is appended/replicated before cache completion; new coordinator ownership reloads current metadata; recovered PREPARE state resumes matching marker work | coordinator reads/reconstructs internal state; user clients do not treat this state store as application payload; participant COMMIT/ABORT markers remain a separate log class | `TransactionalId` hashes to transaction-state partition; current partition leadership and coordinator epoch qualify active cache/mutation authority | final-state compaction and later keyed tombstone can retire superseded/expired coordinator state without implying participant-log or media sanitization | current coordinator state and unfinished completion obligation survive process replacement; complete transition/audit history need not |"
if matrix_row not in text:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith('| Apache Kafka transactional read visibility / 0.11.0.0 bounded regime |'):
            lines.insert(i + 1, matrix_row)
            break
    else:
        raise SystemExit('Kafka transaction comparison-matrix anchor missing')
    text = '\n'.join(lines) + '\n'

old_count = 'After sixty-four bounded cases, **all sixty-four cases are now `grounded`.**'
new_count = 'After sixty-five bounded cases, **all sixty-five cases are now `grounded`.**'
if old_count in text:
    text = text.replace(old_count, new_count, 1)
elif new_count not in text:
    raise SystemExit('CASE_INDEX synthesis-count anchor missing')

heading = '## Case 64 — Kafka transaction-coordinator state-recovery findings'
if heading not in text:
    findings = r'''

## Case 64 — Kafka transaction-coordinator state-recovery findings

701. **coordinator cache ≠ durable transaction state** — Kafka 0.11 reconstructs the transaction coordinator's role-local metadata cache from the internal transaction-state log when a broker takes ownership of the corresponding partition;
702. **coordinator process lifetime ≠ transaction lifetime** — a transaction's current coordination state can survive the broker/process that previously materialized its cache;
703. **pending in-memory transition ≠ durably admitted transaction-state transition** — the bounded implementation completes the cached state transition only after the corresponding transaction-log append succeeds;
704. **replicated transaction-state record ≠ application transaction payload** — coordinator metadata and user-produced records inhabit different log roles even though both use Kafka's storage machinery;
705. **durable PREPARE direction ≠ completed participant work** — `PrepareCommit` or `PrepareAbort` can already survive in coordinator state while marker propagation remains unfinished;
706. **recovered PREPARE state can preserve a future completion obligation** — a new coordinator reloads `PrepareCommit`/`PrepareAbort` and resumes the matching COMMIT/ABORT marker path;
707. **resumed completion ≠ re-deciding transaction outcome** — recovery continues the direction encoded by retained PREPARE state rather than treating coordinator replacement as a new commit/abort choice;
708. **producer epoch ≠ coordinator epoch** — the producer epoch fences stale producer generations for one `TransactionalId`, while the coordinator epoch guards current transaction-state partition ownership/cache mutation in the bounded implementation;
709. **current transaction state ≠ complete transaction transition history** — compacted keyed state can remain sufficient for continuation after superseded coordinator-state records become dispensable;
710. **state-log compaction ≠ user-log transaction abort** — compaction retires superseded internal coordinator-state versions, while ABORT control records in participant logs preserve a negative transaction decision for read isolation;
711. **transaction-state tombstone ≠ participant ABORT marker** — a null-valued internal state-log record expires a `TransactionalId` mapping; a participant ABORT marker rejects user payload from committed history;
712. **transaction-state tombstone ≠ physical sanitization** — logical retirement from the compacted state store neither proves immediate byte removal nor erases participant/user-log traces;
713. **cache reconstruction ≠ state-store dispensability** — making volatile metadata reproducible removes dependence on one RAM embodiment while increasing dependence on the retained authoritative reconstruction source;
714. **completion-state retention obligation can shrink after protocol completion** — KIP-98 explicitly permits most transaction-state records to disappear once final completion is recorded, leaving only the identity/epoch-lifecycle state still needed;
715. **Kafka 0.11 transaction-state recovery ≠ invention of transaction logging/recovery** — System R and older transaction-processing literature already ground commit/abort and transaction-log recovery; the bounded contribution is Kafka's specific replicated compacted-topic composition;
716. **retained state can encode unfinished protocol work rather than only finished payload** — Case 64 adds a regime in which what must survive is partly an obligation for a future coordinator to complete an already-selected action.
'''
    text = text.rstrip() + findings + '\n'

INDEX.write_text(text.rstrip() + '\n')

for p in (README, ROADMAP, INDEX):
    data = p.read_text()
    if '64-apache-kafka-transaction-coordinator-state-recovery.md' not in data:
        raise SystemExit(f'missing Case 64 navigation in {p}')
    if '64-kafka-0110-transaction-state-recovery-grounding.md' not in data:
        raise SystemExit(f'missing evidence 64 navigation in {p}')
idx = INDEX.read_text()
for n in range(701, 717):
    if f'{n}. **' not in idx:
        raise SystemExit(f'missing finding {n}')
if idx.count(heading) != 1:
    raise SystemExit('duplicate Case 64 findings heading')
if 'After sixty-five bounded cases, **all sixty-five cases are now `grounded`.**' not in idx:
    raise SystemExit('65-case synthesis count missing')
print('Case 64 content and integration patch validated')
