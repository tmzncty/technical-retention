from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel, text):
    (ROOT / rel).write_text(text.rstrip() + "\n", encoding="utf-8")


roadmap_path = "ROADMAP.md"
index_path = "CASE_INDEX.md"
case80_path = "cases/80-apache-hdfs-datanode-decommission-replica-drain.md"

roadmap = read(roadmap_path)
index = read(index_path)
case80 = read(case80_path)

case_path = "cases/116-apache-hdfs-datanode-maintenance-state.md"
evidence_path = "evidence/116-hadoop-2014-2018-datanode-maintenance-grounding.md"

# ROADMAP: add one bounded completed slice at the start of Phase 2.
if case_path not in roadmap:
    anchor = "## Phase 2 — Build missing technical bridges\n\n"
    assert anchor in roadmap, "Phase 2 anchor missing"
    bullet = (
        "- [x] Apache HDFS DataNode maintenance-state / temporary-withdrawal boundary — "
        "[`cases/116-apache-hdfs-datanode-maintenance-state.md`](cases/116-apache-hdfs-datanode-maintenance-state.md), "
        "grounded by [`evidence/116-hadoop-2014-2018-datanode-maintenance-grounding.md`](evidence/116-hadoop-2014-2018-datanode-maintenance-grounding.md): "
        "ASF HDFS-6729/HDFS-7877 plus released Hadoop 2.9.0/3.0.1 documentation/source separate short-lived maintenance from full decommission. "
        "`ENTERING_MAINTENANCE` gates withdrawal on a maintenance-specific redundancy floor; `IN_MAINTENANCE` can retain the node's replica relation while ordinary service avoids the node; "
        "and retained expiry bounds how long that relaxed dependency may remain authoritative, after which ordinary reconstruction/extra-redundancy convergence resumes according to node state. "
        "The April 2015 design still listed timeout as open, so final released expiry semantics are not projected backward. "
        "This closes only `temporary withdrawal != permanent retirement`, `retained embodiment != ordinary service eligibility`, and `policy expiry != physical retention expiry`; "
        "exact commit genealogy, HA/restart persistence, erasure-coded behavior, fault injection, and broader distributed maintenance-mode history remain open.\n"
    )
    roadmap = roadmap.replace(anchor, anchor + bullet, 1)

# CASE_INDEX table: place Case 116 immediately after Case 115.
if case_path not in index:
    lines = index.splitlines()
    match_idx = next(
        (i for i, line in enumerate(lines)
         if "cases/115-apache-hdfs-snapshot-shared-block-replication.md" in line),
        None,
    )
    assert match_idx is not None, "Case 115 table row missing"
    row = (
        "| [Apache HDFS DataNode Maintenance State: Temporary Withdrawal, Relaxed Redundancy, and Expiry]"
        "(cases/116-apache-hdfs-datanode-maintenance-state.md) | **grounded** | "
        "HDFS block payload + normal replication objective + maintenance-specific redundancy minimum + DataNode liveness/admin state + retained maintenance expiry + transition/reconstruction progress | "
        "separate temporary withdrawal from decommission; replica presence from service eligibility; maintenance minimum from permanent replication factor; policy expiry from payload deletion; expected return from present physical availability | "
        "[2014–2018 HDFS maintenance-state grounding](evidence/116-hadoop-2014-2018-datanode-maintenance-grounding.md); exact subtask/commit genealogy, NameNode failover persistence, EC-specific behavior, fault injection, and broad maintenance-mode history remain separate work |"
    )
    lines.insert(match_idx + 1, row)
    index = "\n".join(lines)

# CASE_INDEX findings: append after current 1812 tail.
if "## Case 116 — HDFS DataNode maintenance-state findings" not in index:
    assert "**1812 — related-repository boundary:**" in index, "expected Case 115 tail finding missing"
    findings = r'''

## Case 116 — HDFS DataNode maintenance-state findings

- **1813 — 2014 HDFS-6729 public floor != HDFS-7877 invention priority:** the earlier ASF issue already states the short-outage maintenance problem before HDFS-7877 was created in March 2015; this is an HDFS project chronology floor, not a broader invention claim. (`H/P`, `X`)
- **1814 — DataNode liveness != administrative maintenance state:** the HDFS maintenance design/released manager permits a node's live/dead condition and its `ENTERING_MAINTENANCE` / `IN_MAINTENANCE` role to vary independently. (`H/P`)
- **1815 — April-2015 maintenance design != final released expiry contract:** the HDFS-7877 design still lists timeout as an open issue, while released 3.0.1 code retains and enforces a maintenance expiration time. (`H/P`, `X` backward projection)
- **1816 — maintenance request != withdrawal admissibility:** `ENTERING_MAINTENANCE` exists because an operator request can precede the reconstruction/revalidation needed before the node may become `IN_MAINTENANCE`. (`H/P`, `E`)
- **1817 — maintenance minimum != normal replication factor:** released HDFS explicitly allows maintenance entry without always restoring the full ordinary replication factor, using a maintenance-specific sufficiency threshold instead. (`H/P`)
- **1818 — temporary redundancy relaxation != permanent replication-factor reduction:** the ordinary redundancy objective remains; maintenance only changes what may be temporarily relied upon while the expiry-bounded relation is valid. (`E`)
- **1819 — retained/known maintenance replica != ordinary service eligibility:** the bounded design keeps maintenance replicas in the NameNode block relation while excluding an `IN_MAINTENANCE` node from ordinary read locations and new write placement. (`H/P`, `E`)
- **1820 — `ENTERING_MAINTENANCE` != `IN_MAINTENANCE`:** requested withdrawal and admitted temporary withdrawal are separate administrative states with different transition evidence. (`H/P`)
- **1821 — retained maintenance expiry != payload-retention lifetime:** `maintenanceExpireTimeInMS` governs the life of an administrative/redundancy policy, not how long disk or Flash media physically retain bits. (`H/P`, `E`)
- **1822 — maintenance expiry != payload deletion:** expiration invokes `stopMaintenance` / ordinary redundancy convergence; it does not establish block erasure or sanitization on the maintenance node. (`H/P`, `E`, `X`)
- **1823 — expiry revokes relaxed-dependency authority:** when the bounded maintenance interval ends, HDFS may no longer continue treating the temporary maintenance relation as sufficient reason to keep ordinary live redundancy relaxed. (`E`)
- **1824 — dead-node maintenance exit != live-node maintenance exit:** released 3.0.1 code removes dead-node replica accounting to trigger needed reconstruction, while a live return can instead create extra-redundancy cleanup. (`H/P`)
- **1825 — return-time over-redundancy cleanup != failed preservation:** extra replicas can be a legitimate consequence of conservative reconstruction or factor changes during the outage; cleanup restores policy after return rather than proving that the maintenance operation was erroneous. (`H/P`, `E`)
- **1826 — Case 80 decommission != Case 116 maintenance:** decommission aims to retire dependence on the departing embodiment after stronger alternative-replica/placement conditions; maintenance can deliberately retain time-bounded dependence on an expected-to-return embodiment. (`H/P`, `A` bounded within HDFS)
- **1827 — Case 68 Dynamo temporary-failure analogy != mechanism identity or genealogy:** Dynamo's local failure suspicion/hinted handoff and HDFS's NameNode-administered maintenance state/expiry solve functionally related continuity problems with different authority and placement mechanisms. (`A`, `X`)
- **1828 — Case 115 historical replication authority != Case 116 administrative/time relaxation:** snapshot metadata can preserve a higher present block-replication obligation, while maintenance metadata can temporarily relax how much redundancy must be live outside one planned-outage node. (`A`)
- **1829 — related-repository boundary:** current `tmzncty/computing-archaeology` search found no dedicated HDFS DataNode maintenance-state case; broad temporary-node-maintenance genealogy belongs there if developed, while Case 116 keeps only the retention-specific temporary-dependence/expiry relation. (`H/P` project-state record)
'''
    index = index.rstrip() + findings

# Case 80: explicit continuation so later readers do not project decommission semantics into maintenance.
if "116-apache-hdfs-datanode-maintenance-state.md" not in case80:
    continuation = r'''

---

## Continuation — Case 116: temporary maintenance is not decommission

Grounded [Case 116](116-apache-hdfs-datanode-maintenance-state.md) handles the later HDFS maintenance-state regime deliberately left outside this case. It keeps `ENTERING_MAINTENANCE` / `IN_MAINTENANCE`, a maintenance-specific redundancy threshold, retained expiry, and post-expiry convergence separate from the bounded 0.18–2.7.3 decommission path documented here.

The comparison is narrow:

> **decommission retirement admissibility != temporary-maintenance admissibility**

Case 80 asks when HDFS may stop depending on a node as an ordinary embodiment. Case 116 asks when HDFS may temporarily keep depending on an expected-to-return embodiment while denying it ordinary service eligibility and relaxing how much redundancy must be live elsewhere. Do not project the later maintenance states, threshold, or expiry backward into the 0.18/2.7.3 record.
'''
    case80 = case80.rstrip() + continuation

write(roadmap_path, roadmap)
write(index_path, index)
write(case80_path, case80)

# Guard the navigation and finding sequence before allowing the integration commit.
roadmap2 = read(roadmap_path)
index2 = read(index_path)
case802 = read(case80_path)
assert case_path in roadmap2
assert evidence_path in roadmap2
assert index2.count("(cases/116-apache-hdfs-datanode-maintenance-state.md)") == 1
assert "## Case 116 — HDFS DataNode maintenance-state findings" in index2
section = index2.split("## Case 116 — HDFS DataNode maintenance-state findings", 1)[1]
ids = [int(x) for x in re.findall(r"\*\*(\d+) —", section)]
assert ids == list(range(1813, 1830)), ids
assert "116-apache-hdfs-datanode-maintenance-state.md" in case802

subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)
print("Case 116 integration validation passed")