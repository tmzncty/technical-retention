#!/usr/bin/env python3
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ROADMAP = ROOT / "ROADMAP.md"
CASE_INDEX = ROOT / "CASE_INDEX.md"
CASE_PATH = ROOT / "cases/51-apache-hdfs-datanode-command-fencing.md"
EVIDENCE_PATH = ROOT / "evidence/51-hadoop-2011-2016-datanode-command-fencing-grounding.md"
WORKFLOW = ROOT / ".github/workflows/integrate-case51.yml"
SELF = Path(__file__)

def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)

def append_after_line(text, line, addition, label):
    needle = line + "\n"
    count = text.count(needle)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one anchor line, found {count}")
    return text.replace(needle, needle + addition + "\n", 1)

if not CASE_PATH.exists() or not EVIDENCE_PATH.exists():
    raise RuntimeError("staged Case 51 / evidence 51 files are missing")

readme = README.read_text(encoding="utf-8")
readme = append_after_line(readme, "- [`cases/50-apache-hdfs-qjm-epoch-fencing.md`](cases/50-apache-hdfs-qjm-epoch-fencing.md) — grounded HDFS HA/QJM writer-authority bridge: JournalNodes persist a higher `lastPromisedEpoch` so quorum overlap can fence stale edit-log writers without requiring the old NameNode process to disappear; journal-write fencing remains distinct from stale-read/process fencing and from ZooKeeper election.", "- [`cases/51-apache-hdfs-datanode-command-fencing.md`](cases/51-apache-hdfs-datanode-command-fencing.md) — grounded HDFS DataNode command-authority/freshness bridge: heartbeat HA state plus namespace transaction-ID recency select which connected NameNode may issue block-mutation commands, while post-failover stale replica-inventory state separately postpones some irreversible invalidations until fresh reports arrive.", "README case 50")
readme = append_after_line(readme, "- [`evidence/50-hadoop-qjm-2012-2016-epoch-fencing-grounding.md`](evidence/50-hadoop-qjm-2012-2016-epoch-fencing-grounding.md) — Case-50 grounding record: HDFS-3077's 2012 QJM design, Hadoop 2.7.3 HA documentation, and release source ground quorum epoch establishment, persistent JournalNode writer promises, lower-epoch rejection, and the boundary between shared-log fencing, process/read fencing, and ZooKeeper/ZKFC election.", "- [`evidence/51-hadoop-2011-2016-datanode-command-fencing-grounding.md`](evidence/51-hadoop-2011-2016-datanode-command-fencing-grounding.md) — Case-51 grounding record: HDFS-1972/HDFS-2627 plus Hadoop 2.7.3 release source ground heartbeat role/txid Active selection, runtime DataNode command fencing, command-class exceptions, and post-failover stale-inventory revalidation before some replica deletions.", "README evidence 50")
README.write_text(readme, encoding="utf-8")

roadmap = ROADMAP.read_text(encoding="utf-8")
roadmap = replace_once(roadmap, "**partially advanced by grounded Cases 19, 23, 24, 25, 26, 27, 28, 29, 41, 46, 48, 49, and 50**", "**partially advanced by grounded Cases 19, 23, 24, 25, 26, 27, 28, 29, 41, 46, 48, 49, 50, and 51**", "ROADMAP distributed count")
roadmap = replace_once(roadmap, "The broad item stays unchecked because later HDFS lease/pipeline recovery evolution, DataNode command fencing, post-2.7 QJM/HA evolution, and Observer/read-freshness semantics", "[`cases/51-apache-hdfs-datanode-command-fencing.md`](cases/51-apache-hdfs-datanode-command-fencing.md), grounded by [`evidence/51-hadoop-2011-2016-datanode-command-fencing-grounding.md`](evidence/51-hadoop-2011-2016-datanode-command-fencing-grounding.md), adds the DataNode-side command-authority and post-failover inventory-freshness slice left open by Case 50: heartbeat HA state plus namespace transaction-ID recency select which connected NameNode may issue block-mutation commands, the DataNode updates that authority view before interpreting same-heartbeat commands, Standby block-mutation classes are ignored while an access-key exception preserves command-specific scope, and a separate stale-inventory state can postpone invalidation until fresh post-failover heartbeat/block-report evidence arrives. This keeps DataNode `lastActiveClaimTxId` distinct from QJM's durable JournalNode `lastPromisedEpoch` and keeps authority currentness distinct from replica-inventory currentness. The broad item stays unchecked because later HDFS lease/pipeline recovery evolution, post-2.7 DataNode command-fencing evolution and restart/split-brain fault validation, post-2.7 QJM/HA evolution, and Observer/read-freshness semantics", "ROADMAP distributed tail")
ROADMAP.write_text(roadmap, encoding="utf-8")

case_index = CASE_INDEX.read_text(encoding="utf-8")
row50 = "| [Apache HDFS QJM Epoch Fencing: Persisted Writer Promises, Quorum Overlap, and Split-Brain Containment](cases/50-apache-hdfs-qjm-epoch-fencing.md) | **grounded** | replicated namespace edit log + persistent JournalNode epoch promises + quorum overlap + separate HA/election/process-fencing state | separate process liveness from mutation authority; show durable refusal/control metadata fencing stale writers across failover; distinguish QJM journal fencing from process/read fencing and ZooKeeper election | [2012–2016 HDFS QJM epoch-fencing grounding](evidence/50-hadoop-qjm-2012-2016-epoch-fencing-grounding.md); DataNode command fencing, later QJM/Observer semantics, independent fault injection, and broader consensus genealogy remain separate work |"
row50_new = "| [Apache HDFS QJM Epoch Fencing: Persisted Writer Promises, Quorum Overlap, and Split-Brain Containment](cases/50-apache-hdfs-qjm-epoch-fencing.md) | **grounded** | replicated namespace edit log + persistent JournalNode epoch promises + quorum overlap + separate HA/election/process-fencing state | separate process liveness from mutation authority; show durable refusal/control metadata fencing stale writers across failover; distinguish QJM journal fencing from process/read fencing and ZooKeeper election | [2012–2016 HDFS QJM epoch-fencing grounding](evidence/50-hadoop-qjm-2012-2016-epoch-fencing-grounding.md); DataNode command fencing is now handled separately in Case 51, while later QJM/Observer semantics, independent fault injection, and broader consensus genealogy remain separate work |"
row51 = "| [Apache HDFS DataNode Command Fencing: Heartbeat Authority, Transaction-ID Recency, and Stale Replica Inventories](cases/51-apache-hdfs-datanode-command-fencing.md) | **grounded** | DataNode runtime selected-Active actor + `lastActiveClaimTxId` + heartbeat HA state/namespace txid + post-failover storage freshness state + fresh block-report evidence | separate connectivity from block-command authority; runtime authority memory from durable fencing promises; command-source currentness from replica-inventory freshness; and stale inventory from payload corruption | [2011–2016 HDFS DataNode command-fencing grounding](evidence/51-hadoop-2011-2016-datanode-command-fencing-grounding.md); post-2.7 command-fencing evolution, DataNode restart/split-brain fault injection, modern EC block commands, and broader fencing genealogy remain separate work |"
case_index = replace_once(case_index, row50, row50_new, "CASE_INDEX row 50")
case_index = append_after_line(case_index, row50_new, row51, "CASE_INDEX row 51 insertion")

matrix50 = "| HDFS QJM epoch fencing / 2012 design + Hadoop 2.7.3 bounded regime | replicated namespace edit records + persistent `lastPromisedEpoch` / `lastWriterEpoch` + current-epoch IPC ordering state + HA/election state | quorum edit replication; higher-epoch establishment and stale-writer rejection during failover; standby tailing; optional external/process fencing is separate work | old Active may still answer stale reads after losing QJM write authority, so read execution and shared-log mutation authority are distinct | logical HDFS nameservice/edit transaction stream resolved through a JournalNode quorum; writer epoch qualifies which mutation source may be admitted | Active role can move between physical NameNodes while the old process survives; retained higher promises remove its successful shared-log mutation authority | bounded edit history is retained for namespace recovery; epoch promises retain authority/future-refusal state rather than application payload history |"
matrix51 = "| HDFS DataNode command fencing / 2011 HA design + Hadoop 2.7.3 bounded regime | DataNode runtime `bpServiceToActive` + `lastActiveClaimTxId` + heartbeat HA state/txid + post-failover `blockContentsStale`/report freshness | heartbeat-driven Active selection; command-class filtering; post-failover inventory revalidation; delayed invalidation of uncertain over-replication | DataNode receives heartbeats from both NameNodes, but only the selected Active's block-mutation commands are admitted; fresh block reports can retire inventory uncertainty | block pool → per-NameNode actor; heartbeat role + namespace txid selects the command source, while block reports requalify storage inventory | block payload can remain physically unchanged while command-source authority and inventory freshness move across failover | no payload history; runtime authority watermark and freshness/control state guide future mutations, and the watermark is not shown as crash-durable in this release |"
case_index = append_after_line(case_index, matrix50, matrix51, "CASE_INDEX matrix row 51")
case_index = replace_once(case_index, "After fifty-one bounded cases, **all fifty cases are now `grounded`.**", "After fifty-two bounded cases, **all fifty-two cases are now `grounded`.**", "CASE_INDEX grounded count")
case_index = replace_once(case_index, "- [x] at least four contrasting cases at `grounded` or better — currently fifty-one;", "- [x] at least four contrasting cases at `grounded` or better — currently fifty-two;", "CASE_INDEX synthesis count")
old = "500. **HDFS QJM epoch design ≠ invention of epoch/quorum fencing** — the 2012 HDFS-3077 design itself cites Paxos and ZAB and describes borrowing epoch-generation ideas from that prior distributed-systems literature.\n\nThese are provisional cross-case findings"
new = "500. **HDFS QJM epoch design ≠ invention of epoch/quorum fencing** — the 2012 HDFS-3077 design itself cites Paxos and ZAB and describes borrowing epoch-generation ideas from that prior distributed-systems literature.\n\n501. **connected NameNode ≠ command-authoritative NameNode** — Hadoop 2.7.3 DataNodes maintain actors for multiple NameNodes, while `bpServiceToActive` separately selects which actor's block-mutation commands are admissible.\n502. **Standby heartbeat participation ≠ destructive block-command authority** — Standby communication remains live, but transfer, invalidation, recovery, finalize, cache, and related mutation classes are ignored when they come from the non-selected actor.\n503. **higher observed namespace txid can supersede a lower Active claim at the DataNode** — HDFS-2627 and `BPOfferService` use heartbeat transaction-ID recency to prevent an earlier Active that still claims the role from taking command authority back with an older claim.\n504. **heartbeat reception ≠ same-response command admissibility** — `BPServiceActor` deliberately updates the DataNode's HA/Active view before processing commands returned by that heartbeat, so current role interpretation gates the command list.\n505. **DataNode `lastActiveClaimTxId` ≠ JournalNode `lastPromisedEpoch`** — Case 51 uses a runtime local observation watermark for command-source selection, while Case 50 uses a persisted acceptor-side promise plus quorum overlap for shared-edit-log writer fencing.\n506. **runtime command-fencing memory ≠ crash-persistent fencing state** — the bounded 2.7.3 `lastActiveClaimTxId` is an ordinary in-memory field initialized to `-1`; this case does not infer that DataNode restart preserves the prior watermark.\n507. **command authority can be command-class-specific** — Standby `DNA_ACCESSKEYUPDATE` is accepted even though destructive/replicative/recovery command classes are ignored, rejecting a universal `Standby = no control authority` simplification.\n508. **NameNode failover completion ≠ fresh replica inventory** — a NameNode can be the new Active while DataNode storage inventories remain marked stale until post-failover heartbeat/block-report evidence arrives.\n509. **`blockContentsStale` ≠ block corruption** — the stale flag records uncertainty that the NameNode has incorporated prior deletion effects, not a checksum or byte-integrity failure in the local replica.\n510. **apparent over-replication under stale inventory ≠ safely reclaimable redundancy** — HDFS-1972 postpones invalidation because a replica still present in the central map may already have been deleted under the previous NameNode.\n511. **post-failover uncertainty can itself be retained to prevent premature forgetting** — `blockContentsStale` preserves a negative safety condition that withholds deletion until the inventory is re-observed.\n512. **command-authority currentness ≠ replica-inventory freshness** — selecting the right NameNode command source answers `who may request a mutation`; fresh block reports answer `do we know enough about current replicas to perform this mutation safely`.\n513. **pre-failover queued maintenance decision ≠ automatically post-failover admissible decision** — the 2011 HDFS-1972 patch clears replication/invalidation/recovery decisions made under an earlier control state rather than carrying every conclusion across role transition.\n514. **one logical Active ≠ one fencing locus** — HDFS composes JournalNode writer fencing, DataNode command-source filtering, replica-inventory revalidation, ZooKeeper/ZKFC election, and external/process fencing as distinct safety surfaces rather than one universal authority bit.\n\nThese are provisional cross-case findings"
case_index = replace_once(case_index, old, new, "CASE_INDEX findings 501-514")
CASE_INDEX.write_text(case_index, encoding="utf-8")

checks = [
    (README, "cases/51-apache-hdfs-datanode-command-fencing.md"),
    (README, "evidence/51-hadoop-2011-2016-datanode-command-fencing-grounding.md"),
    (ROADMAP, "Cases 19, 23, 24, 25, 26, 27, 28, 29, 41, 46, 48, 49, 50, and 51"),
    (CASE_INDEX, "After fifty-two bounded cases, **all fifty-two cases are now `grounded`.**"),
    (CASE_INDEX, "501. **connected NameNode ≠ command-authoritative NameNode**"),
    (CASE_INDEX, "514. **one logical Active ≠ one fencing locus**"),
]
for p, needle in checks:
    if needle not in p.read_text(encoding="utf-8"):
        raise RuntimeError(f"validation failed: {needle!r} missing from {p.name}")

if README.read_text(encoding="utf-8").count("cases/51-apache-hdfs-datanode-command-fencing.md") != 1:
    raise RuntimeError("README Case 51 navigation is not unique")
if README.read_text(encoding="utf-8").count("evidence/51-hadoop-2011-2016-datanode-command-fencing-grounding.md") != 1:
    raise RuntimeError("README evidence 51 navigation is not unique")

if WORKFLOW.exists():
    WORKFLOW.unlink()
if SELF.exists():
    SELF.unlink()

subprocess.run(["git", "config", "user.name", "technical-retention-bot"], cwd=ROOT, check=True)
subprocess.run(["git", "config", "user.email", "technical-retention-bot@users.noreply.github.com"], cwd=ROOT, check=True)
subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)

changed = subprocess.check_output(["git", "diff", "--cached", "--name-only"], cwd=ROOT, text=True).splitlines()
expected = {"README.md", "ROADMAP.md", "CASE_INDEX.md", ".github/workflows/integrate-case51.yml", "tools/integrate_case51.py"}
if set(changed) != expected:
    raise RuntimeError(f"unexpected final staged paths: {changed}")

subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, check=True)
subprocess.run(["git", "commit", "-m", "docs: integrate grounded HDFS DataNode command-fencing case"], cwd=ROOT, check=True)
subprocess.run(["git", "push", "origin", "HEAD:main"], cwd=ROOT, check=True)
