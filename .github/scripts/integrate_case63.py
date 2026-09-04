from pathlib import Path

README = Path("README.md")
ROADMAP = Path("ROADMAP.md")
INDEX = Path("CASE_INDEX.md")

case_line = "- [`cases/63-apache-kafka-transactional-read-visibility.md`](cases/63-apache-kafka-transactional-read-visibility.md) — grounded Kafka 0.11 transactional read-visibility bridge: the replication high watermark and transaction-sensitive last stable offset remain distinct; an earlier open transaction can withhold later offsets, while retained COMMIT/ABORT control state and aborted-range indexing let `READ_COMMITTED` suppress physically surviving aborted records."
evidence_line = "- [`evidence/63-kafka-0110-transaction-lso-grounding.md`](evidence/63-kafka-0110-transaction-lso-grounding.md) — Case-63 grounding record: exact Kafka 0.11.0.0 source plus KIP-98 separate high watermark, first unstable transaction, LSO, hidden control markers, per-segment aborted-transaction indexing, and consumer isolation; System R prior art prevents a false transaction/atomic-commit invention claim."

# README navigation.
text = README.read_text()
if case_line not in text:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("- [`cases/62-ibm-system360-model40-tros-replaceable-control-store.md`]"):
            lines.insert(i + 1, case_line)
            break
    else:
        raise SystemExit("README Case 62 anchor missing")
    text = "\n".join(lines) + "\n"
if evidence_line not in text:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("- [`evidence/62-ibm-bell-1950-1970-tros-grounding.md`]"):
            lines.insert(i + 1, evidence_line)
            break
    else:
        raise SystemExit("README evidence 62 anchor missing")
    text = "\n".join(lines) + "\n"
README.write_text(text)

# ROADMAP: advance both replicated-log and current-state-reconstruction bridges without
# pretending the whole transaction/Streams history is closed.
text = ROADMAP.read_text()
old = "partially advanced by grounded Cases 42, 57, and 58"
new = "partially advanced by grounded Cases 42, 57, 58, and 63"
if old not in text and new not in text:
    raise SystemExit("append-log case-count anchor missing")
text = text.replace(old, new, 1)

lines = text.splitlines()
for i, line in enumerate(lines):
    if line.startswith("- [ ] append-log / changelog compaction and current-state reconstruction"):
        if "cases/63-apache-kafka-transactional-read-visibility.md" not in line:
            insert = " [`cases/63-apache-kafka-transactional-read-visibility.md`](cases/63-apache-kafka-transactional-read-visibility.md), grounded by [`evidence/63-kafka-0110-transaction-lso-grounding.md`](evidence/63-kafka-0110-transaction-lso-grounding.md), adds a transaction-sensitive read-admissibility layer above Case 56's replication frontier: Kafka 0.11 carries high watermark and last stable offset separately; the earliest open transaction can hold `READ_COMMITTED` behind already-replicated bytes; COMMIT/ABORT control records and aborted-transaction index state let the system retain a negative decision so physically surviving aborted payload remains excluded from the application-visible history. This is distinct from Case 42 keyed compaction and Case 56 replication commitment."
            marker = " The broad item stays unchecked because"
            pos = line.find(marker)
            if pos < 0:
                raise SystemExit("append-log remaining-work marker missing")
            line = line[:pos] + insert + line[pos:]
        line = line.replace("later transaction/Streams changelog semantics", "later Streams changelog/processing semantics and post-0.11 transaction evolution")
        lines[i] = line
        break
else:
    raise SystemExit("append-log roadmap bullet missing")

for i, line in enumerate(lines):
    if line.startswith("- [ ] distributed replication and erasure coding beyond RADOS"):
        old_cases = "Cases 19, 23, 24, 25, 26, 27, 28, 29, 41, 46, 48, 49, 50, 51, 56, 57, 58, and 61"
        new_cases = "Cases 19, 23, 24, 25, 26, 27, 28, 29, 41, 46, 48, 49, 50, 51, 56, 57, 58, 61, and 63"
        if old_cases in line:
            line = line.replace(old_cases, new_cases, 1)
        elif new_cases not in line:
            raise SystemExit("distributed case-count anchor missing")
        if "cases/63-apache-kafka-transactional-read-visibility.md" not in line:
            insert = " [`cases/63-apache-kafka-transactional-read-visibility.md`](cases/63-apache-kafka-transactional-read-visibility.md), grounded by [`evidence/63-kafka-0110-transaction-lso-grounding.md`](evidence/63-kafka-0110-transaction-lso-grounding.md), adds a post-replication transactional visibility frontier: replicated/high-watermark currentness and transaction-decision currentness remain separate, so `READ_COMMITTED` may stop at LSO and filter aborted ranges while the same bytes remain in the replicated log."
            marker = " The broad item stays unchecked because"
            pos = line.find(marker)
            if pos < 0:
                raise SystemExit("distributed remaining-work marker missing")
            line = line[:pos] + insert + line[pos:]
        lines[i] = line
        break
else:
    raise SystemExit("distributed roadmap bullet missing")
ROADMAP.write_text("\n".join(lines) + "\n")

# CASE_INDEX case ledger.
text = INDEX.read_text()
row = "| [Apache Kafka 0.11 Transactional Read Visibility: Last Stable Offset, Abort Markers, and Retained Negative Decisions](cases/63-apache-kafka-transactional-read-visibility.md) | **grounded** | transactional record batches + replication high watermark + first-open-transaction/LSO frontier + COMMIT/ABORT control batches + per-segment aborted-transaction index + consumer isolation | separate replication commitment from transaction decision; physical record survival from `READ_COMMITTED` admissibility; application-level abort from physical erase; and hidden negative-decision evidence from user payload | [0.11.0.0 transaction/LSO grounding](evidence/63-kafka-0110-transaction-lso-grounding.md); transaction-coordinator state-log recovery, post-0.11 correctness/defense evolution, Streams processing/changelog semantics, compaction interaction, independent fault injection, and lower-layer durability composition remain separate work |"
if row not in text:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("| [IBM System/360 Model 40 TROS: Runtime Read-Only State in Replaceable Transformer Control Tapes]"):
            lines.insert(i + 1, row)
            break
    else:
        raise SystemExit("CASE_INDEX Case 62 row anchor missing")
    text = "\n".join(lines) + "\n"

# Close the explicit Case-56 LSO gap while keeping later transaction work open.
text = text.replace(
    "0.11+ leader-epoch recovery, KRaft, transactions/last-stable-offset, independent fault injection",
    "0.11+ leader-epoch recovery, KRaft, post-0.11 transaction evolution, independent fault injection",
    1,
)

# Comparison matrix.
matrix_row = "| Apache Kafka transactional read visibility / 0.11.0.0 bounded regime | partition log records + replication HW + first unstable transaction + LSO + COMMIT/ABORT control batches + transaction index | replication and ordinary log retention continue; transaction completion advances decision state; transaction-index/recovery state makes aborted ranges filterable | `READ_UNCOMMITTED` may expose aborted transactional data; `READ_COMMITTED` stops at LSO and suppresses aborted ranges while control records remain non-user payload | topic/partition + offset ordered frontier; earliest open transaction can constrain later offsets independent of their own transaction membership | physical aborted records can survive in live segments while losing `READ_COMMITTED` authority; no immediate erase is implied | bounded transaction-decision/index state is retained, not a full request/coordinator history; negative decision evidence can preserve logical forgetting |"
if matrix_row not in text:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("| Apache Kafka replicated log / 0.8.2 bounded regime |"):
            lines.insert(i + 1, matrix_row)
            break
    else:
        raise SystemExit("Kafka comparison-matrix anchor missing")
    text = "\n".join(lines) + "\n"

# Synthesis count.
old_count = "After sixty-three bounded cases, **all sixty-three cases are now `grounded`.**"
new_count = "After sixty-four bounded cases, **all sixty-four cases are now `grounded`.**"
if old_count in text:
    text = text.replace(old_count, new_count, 1)
elif new_count not in text:
    raise SystemExit("CASE_INDEX synthesis-count anchor missing")

# Append findings only once.
heading = "## Case 63 — Kafka transactional read-visibility findings"
if heading not in text:
    findings = r'''

## Case 63 — Kafka transactional read-visibility findings

685. **high watermark ≠ last stable offset** — Kafka 0.11 keeps the replication committed-prefix frontier distinct from the transaction-sensitive `READ_COMMITTED` stability frontier;
686. **replication commitment ≠ transaction decision** — records can be replicated below HW before their transaction is committed or aborted;
687. **physically retained aborted record ≠ `READ_COMMITTED`-visible record** — aborted batches can remain in live log segments while consumer isolation suppresses them;
688. **transaction abort ≠ physical erasure** — ABORT changes application-level admissibility through decision/control state and filtering rather than synchronously deleting the original bytes;
689. **negative decision evidence can sustain logical forgetting** — retaining ABORT/control/index state prevents physically surviving aborted payload from re-entering the committed application history;
690. **control-record invisibility ≠ control-state irrelevance** — COMMIT/ABORT control batches are hidden from ordinary application consumption while remaining constitutive of transaction interpretation;
691. **first open transaction can constrain visibility of later offsets** — an unresolved earlier transaction can hold LSO behind later records that already exist and may already be replicated;
692. **offset-order preservation can turn one open transaction into a partition-wide read frontier** — later records can wait behind an earlier open transaction without belonging to it;
693. **transaction index ≠ user payload** — per-segment aborted-range metadata is retained protocol/index state used to qualify reads;
694. **transaction index ≠ complete transaction history** — it stores bounded producer/range/LSO evidence rather than every coordinator transition, retry, or request;
695. **rebuildable metadata ≠ dispensable metadata** — a transaction index or producer-state view may be reconstructed from authoritative log/snapshot material while its logical filtering function remains necessary;
696. **`READ_UNCOMMITTED` and `READ_COMMITTED` can expose different admissible histories from the same physical log** — isolation is a read-admission rule over retained bytes plus transaction state, not a second physical archive;
697. **replication-currentness state ≠ transaction-decision state** — ISR/HW answers whether a log prefix is sufficiently replicated, while LSO/control state answers whether that prefix is transactionally stable for committed reads;
698. **transactional commit ≠ atomic consumer delivery as one indivisible read batch** — KIP-98's cross-partition, seek, retention, and subscription limits prevent that stronger interpretation;
699. **Kafka abort marker ≠ Kafka compaction tombstone** — an abort rejects one transaction's produced records from committed history, whereas a compaction tombstone is a keyed negative current-state record with a different retention horizon;
700. **Kafka 0.11 transactional isolation ≠ invention of transactions/atomic commit** — System R and broader database transaction/log-recovery literature long predate Kafka; the bounded historical claim is the Kafka-specific composition of replicated log, hidden decision markers, LSO, aborted-range indexing, and selectable read isolation.
'''
    text = text.rstrip() + findings + "\n"

INDEX.write_text(text)

# Minimal invariants.
for path in (README, ROADMAP, INDEX):
    data = path.read_text()
    if "63-apache-kafka-transactional-read-visibility.md" not in data:
        raise SystemExit(f"missing Case 63 navigation in {path}")
    if "63-kafka-0110-transaction-lso-grounding.md" not in data:
        raise SystemExit(f"missing evidence 63 navigation in {path}")

idx = INDEX.read_text()
for n in range(685, 701):
    if f"{n}. **" not in idx:
        raise SystemExit(f"missing finding {n}")
if idx.count("## Case 63 — Kafka transactional read-visibility findings") != 1:
    raise SystemExit("duplicate Case 63 findings heading")

print("Case 63 integration patch validated")
