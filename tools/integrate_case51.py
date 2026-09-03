#!/usr/bin/env python3
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ROADMAP = ROOT / "ROADMAP.md"
CASE_INDEX = ROOT / "CASE_INDEX.md"
WORKFLOW = ROOT / ".github/workflows/integrate-case51.yml"
SELF = Path(__file__).resolve()


def insert_after_prefixed_line(text, prefix, line, label):
    lines = text.splitlines()
    hits = [i for i, x in enumerate(lines) if x.startswith(prefix)]
    if len(hits) != 1:
        raise RuntimeError(f"{label}: expected one line beginning {prefix!r}, got {len(hits)}")
    i = hits[0]
    if i + 1 < len(lines) and lines[i + 1] == line:
        return text
    lines.insert(i + 1, line)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def replace_unique(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{label}: expected one match, got {n}")
    return text.replace(old, new, 1)

# New permanent files must already be present in the staging commit.
for p in [ROOT / "cases/51-apache-hdfs-datanode-command-fencing.md",
          ROOT / "evidence/51-hadoop-2011-2016-datanode-command-fencing-grounding.md"]:
    if not p.exists():
        raise RuntimeError(f"missing staged permanent file: {p}")

# README navigation.
readme = README.read_text(encoding="utf-8")
case_line = "- [`cases/51-apache-hdfs-datanode-command-fencing.md`](cases/51-apache-hdfs-datanode-command-fencing.md) — grounded HDFS DataNode command-authority/freshness bridge: heartbeat HA state plus namespace transaction-ID recency select which connected NameNode may issue block-mutation commands, while post-failover stale replica-inventory state separately postpones some irreversible invalidations until fresh reports arrive."
evidence_line = "- [`evidence/51-hadoop-2011-2016-datanode-command-fencing-grounding.md`](evidence/51-hadoop-2011-2016-datanode-command-fencing-grounding.md) — Case-51 grounding record: HDFS-1972/HDFS-2627 plus Hadoop 2.7.3 release source ground heartbeat role/txid Active selection, runtime DataNode command fencing, command-class exceptions, and post-failover stale-inventory revalidation before some replica deletions."
readme = insert_after_prefixed_line(readme, "- [`cases/50-apache-hdfs-qjm-epoch-fencing.md`]", case_line, "README case nav")
readme = insert_after_prefixed_line(readme, "- [`evidence/50-hadoop-qjm-2012-2016-epoch-fencing-grounding.md`]", evidence_line, "README evidence nav")
README.write_text(readme, encoding="utf-8")

# ROADMAP distributed-storage slice. Use short unique anchors rather than the full long paragraph.
roadmap = ROADMAP.read_text(encoding="utf-8")
roadmap = replace_unique(
    roadmap,
    "**partially advanced by grounded Cases 19, 23, 24, 25, 26, 27, 28, 29, 41, 46, 48, 49, and 50**",
    "**partially advanced by grounded Cases 19, 23, 24, 25, 26, 27, 28, 29, 41, 46, 48, 49, 50, and 51**",
    "ROADMAP case list")
roadmap = replace_unique(
    roadmap,
    "The broad item stays unchecked because later HDFS lease/pipeline recovery evolution, DataNode command fencing, post-2.7 QJM/HA evolution, and Observer/read-freshness semantics",
    "[`cases/51-apache-hdfs-datanode-command-fencing.md`](cases/51-apache-hdfs-datanode-command-fencing.md), grounded by [`evidence/51-hadoop-2011-2016-datanode-command-fencing-grounding.md`](evidence/51-hadoop-2011-2016-datanode-command-fencing-grounding.md), adds the DataNode-side command-authority and post-failover inventory-freshness slice left open by Case 50: heartbeat HA state plus namespace transaction-ID recency select which connected NameNode may issue block-mutation commands; the DataNode updates that authority view before interpreting same-heartbeat commands; Standby block-mutation classes are ignored while an access-key exception preserves command-specific scope; and a separate stale-inventory state can postpone invalidation until fresh post-failover heartbeat/block-report evidence arrives. This keeps DataNode `lastActiveClaimTxId` distinct from QJM's durable JournalNode `lastPromisedEpoch` and keeps authority currentness distinct from replica-inventory currentness. The broad item stays unchecked because later HDFS lease/pipeline recovery evolution, post-2.7 DataNode command-fencing evolution and restart/split-brain fault validation, post-2.7 QJM/HA evolution, and Observer/read-freshness semantics",
    "ROADMAP open-tail")
ROADMAP.write_text(roadmap, encoding="utf-8")

# CASE_INDEX case table.
ci = CASE_INDEX.read_text(encoding="utf-8")
row51 = "| [Apache HDFS DataNode Command Fencing: Heartbeat Authority, Transaction-ID Recency, and Stale Replica Inventories](cases/51-apache-hdfs-datanode-command-fencing.md) | **grounded** | DataNode runtime selected-Active actor + `lastActiveClaimTxId` + heartbeat HA state/namespace txid + post-failover storage freshness state + fresh block-report evidence | separate connectivity from block-command authority; runtime authority memory from durable fencing promises; command-source currentness from replica-inventory freshness; and stale inventory from payload corruption | [2011–2016 HDFS DataNode command-fencing grounding](evidence/51-hadoop-2011-2016-datanode-command-fencing-grounding.md); post-2.7 command-fencing evolution, DataNode restart/split-brain fault injection, modern EC block commands, and broader fencing genealogy remain separate work |"
ci = insert_after_prefixed_line(ci, "| [Apache HDFS QJM Epoch Fencing:", row51, "CASE_INDEX case row")
# Tighten the Case-50 open-work note only once.
ci = replace_unique(ci, "DataNode command fencing, later QJM/Observer semantics", "DataNode command fencing is now handled separately in Case 51, while later QJM/Observer semantics", "CASE_INDEX Case50 next-work")

# Comparison matrix.
matrix51 = "| HDFS DataNode command fencing / 2011 HA design + Hadoop 2.7.3 bounded regime | DataNode runtime `bpServiceToActive` + `lastActiveClaimTxId` + heartbeat HA state/txid + post-failover `blockContentsStale`/report freshness | heartbeat-driven Active selection; command-class filtering; post-failover inventory revalidation; delayed invalidation of uncertain over-replication | DataNode receives heartbeats from both NameNodes, but only the selected Active's block-mutation commands are admitted; fresh block reports can retire inventory uncertainty | block pool → per-NameNode actor; heartbeat role + namespace txid selects the command source, while block reports requalify storage inventory | block payload can remain physically unchanged while command-source authority and inventory freshness move across failover | no payload history; runtime authority watermark and freshness/control state guide future mutations, and the watermark is not shown as crash-durable in this release |"
ci = insert_after_prefixed_line(ci, "| HDFS QJM epoch fencing /", matrix51, "CASE_INDEX matrix row")

# Correct existing count drift while adding this case.
if "After fifty-one bounded cases, **all fifty cases are now `grounded`.**" in ci:
    ci = ci.replace("After fifty-one bounded cases, **all fifty cases are now `grounded`.**", "After fifty-two bounded cases, **all fifty-two cases are now `grounded`.**", 1)
elif "After fifty-one bounded cases, **all fifty-one cases are now `grounded`.**" in ci:
    ci = ci.replace("After fifty-one bounded cases, **all fifty-one cases are now `grounded`.**", "After fifty-two bounded cases, **all fifty-two cases are now `grounded`.**", 1)
else:
    raise RuntimeError("CASE_INDEX bounded/grounded status anchor not found")
ci = replace_unique(ci, "currently fifty-one;", "currently fifty-two;", "CASE_INDEX synthesis count")

# Findings 501–514: insert immediately after finding 500 line.
findings = [
"501. **connected NameNode ≠ command-authoritative NameNode** — Hadoop 2.7.3 DataNodes maintain actors for multiple NameNodes, while `bpServiceToActive` separately selects which actor's block-mutation commands are admissible.",
"502. **Standby heartbeat participation ≠ destructive block-command authority** — Standby communication remains live, but transfer, invalidation, recovery, finalize, cache, and related mutation classes are ignored when they come from the non-selected actor.",
"503. **higher observed namespace txid can supersede a lower Active claim at the DataNode** — HDFS-2627 and `BPOfferService` use heartbeat transaction-ID recency to prevent an earlier Active that still claims the role from taking command authority back with an older claim.",
"504. **heartbeat reception ≠ same-response command admissibility** — `BPServiceActor` deliberately updates the DataNode's HA/Active view before processing commands returned by that heartbeat, so current role interpretation gates the command list.",
"505. **DataNode `lastActiveClaimTxId` ≠ JournalNode `lastPromisedEpoch`** — Case 51 uses a runtime local observation watermark for command-source selection, while Case 50 uses a persisted acceptor-side promise plus quorum overlap for shared-edit-log writer fencing.",
"506. **runtime command-fencing memory ≠ crash-persistent fencing state** — the bounded 2.7.3 `lastActiveClaimTxId` is an ordinary in-memory field initialized to `-1`; this case does not infer that DataNode restart preserves the prior watermark.",
"507. **command authority can be command-class-specific** — Standby `DNA_ACCESSKEYUPDATE` is accepted even though destructive/replicative/recovery command classes are ignored, rejecting a universal `Standby = no control authority` simplification.",
"508. **NameNode failover completion ≠ fresh replica inventory** — a NameNode can be the new Active while DataNode storage inventories remain marked stale until post-failover heartbeat/block-report evidence arrives.",
"509. **`blockContentsStale` ≠ block corruption** — the stale flag records uncertainty that the NameNode has incorporated prior deletion effects, not a checksum or byte-integrity failure in the local replica.",
"510. **apparent over-replication under stale inventory ≠ safely reclaimable redundancy** — HDFS-1972 postpones invalidation because a replica still present in the central map may already have been deleted under the previous NameNode.",
"511. **post-failover uncertainty can itself be retained to prevent premature forgetting** — `blockContentsStale` preserves a negative safety condition that withholds deletion until the inventory is re-observed.",
"512. **command-authority currentness ≠ replica-inventory freshness** — selecting the right NameNode command source answers `who may request a mutation`; fresh block reports answer `do we know enough about current replicas to perform this mutation safely`.",
"513. **pre-failover queued maintenance decision ≠ automatically post-failover admissible decision** — the 2011 HDFS-1972 patch clears replication/invalidation/recovery decisions made under an earlier control state rather than carrying every conclusion across role transition.",
"514. **one logical Active ≠ one fencing locus** — HDFS composes JournalNode writer fencing, DataNode command-source filtering, replica-inventory revalidation, ZooKeeper/ZKFC election, and external/process fencing as distinct safety surfaces rather than one universal authority bit."
]
lines = ci.splitlines()
hits = [i for i, x in enumerate(lines) if x.startswith("500. **HDFS QJM epoch design")]
if len(hits) != 1:
    raise RuntimeError(f"finding 500 anchor count: {len(hits)}")
i = hits[0]
if not any(x.startswith("501. **connected NameNode") for x in lines):
    lines[i+1:i+1] = [""] + findings
ci = "\n".join(lines) + ("\n" if ci.endswith("\n") else "")
CASE_INDEX.write_text(ci, encoding="utf-8")

# Validate bounded final content.
assert case_line in README.read_text(encoding="utf-8")
assert evidence_line in README.read_text(encoding="utf-8")
assert "Cases 19, 23, 24, 25, 26, 27, 28, 29, 41, 46, 48, 49, 50, and 51" in ROADMAP.read_text(encoding="utf-8")
ci2 = CASE_INDEX.read_text(encoding="utf-8")
assert "After fifty-two bounded cases, **all fifty-two cases are now `grounded`.**" in ci2
assert ci2.count("501. **connected NameNode ≠ command-authoritative NameNode**") == 1
assert ci2.count("514. **one logical Active ≠ one fencing locus**") == 1

# Remove one-shot integration machinery from the final tree.
if WORKFLOW.exists(): WORKFLOW.unlink()
if SELF.exists(): SELF.unlink()

subprocess.run(["git", "config", "user.name", "technical-retention-bot"], cwd=ROOT, check=True)
subprocess.run(["git", "config", "user.email", "technical-retention-bot@users.noreply.github.com"], cwd=ROOT, check=True)
subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, check=True)
changed = set(subprocess.check_output(["git", "diff", "--cached", "--name-only"], cwd=ROOT, text=True).splitlines())
expected = {"README.md", "ROADMAP.md", "CASE_INDEX.md", ".github/workflows/integrate-case51.yml", "tools/integrate_case51.py"}
if changed != expected:
    raise RuntimeError(f"unexpected staged paths: {sorted(changed)}")
subprocess.run(["git", "commit", "-m", "docs: integrate grounded HDFS DataNode command-fencing case"], cwd=ROOT, check=True)
subprocess.run(["git", "push", "origin", "HEAD:main"], cwd=ROOT, check=True)
