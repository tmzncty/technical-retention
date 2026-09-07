from pathlib import Path

ROADMAP = Path("ROADMAP.md")
INDEX = Path("CASE_INDEX.md")

case_path = "cases/117-apache-hdfs-startup-safemode-reobservation.md"
evidence_path = "evidence/117-hadoop-2008-2017-startup-safemode-grounding.md"

roadmap_entry = f"""- [x] Apache HDFS startup Safemode / re-observation-before-mutation boundary — [`{case_path}`]({case_path}), grounded by [`{evidence_path}`]({evidence_path}): the 2008-era HDFS architecture record, Hadoop 1.0.4 user/configuration documentation, and Hadoop 2.8.0 NameNode source separate `FsImage`/`EditLog` namespace recovery from DataNode `Blockreport` re-observation. Startup Safemode suppresses mutations/replication while minimum-replica evidence accumulates; crossing a configurable safe-block percentage is an admission threshold rather than proof that every block, configured replication factor, rack placement, or checksum-integrity relation is restored, and an extension may delay exit after threshold attainment. Released source also separates automatic startup Safemode from manually entered Safemode. This closes only the bounded `retained namespace + surviving payload != current location knowledge != mutation authority` relation; pre-2008 genealogy, HA/resource-low/force-exit semantics, erasure-coded startup, production incident evidence, and fault injection remain open. Broad HDFS recovery history stays with `computing-archaeology`."""

index_row = f"""| [Apache HDFS Startup Safemode: Namespace Recovery, Block Re-observation, and Withheld Mutation Authority]({case_path}) | **grounded** | persistent `FsImage`/`EditLog` namespace + DataNode block payloads + startup Blockreports + safe-block/minimum-replica counters + threshold/extension + read-only NameNode state | separate namespace replay from replica-location re-observation; payload survival from NameNode knowledge; minimum safe-block admission from full redundancy/integrity/placement; retained/readable state from mutation authority | [2008–2017 Apache grounding]({evidence_path}); pre-2008 genealogy, HA/failover and resource-low semantics, EC-era startup, force-exit incidents, and fault injection remain open |"""

findings = """## Case 117 — HDFS startup Safemode findings

- **1830 — 2008 released HDFS Safemode record != invention priority:** Apache's 22 August 2008 Hadoop 0.18.0 release and early HDFS architecture documentation provide a public HDFS chronology floor, not proof of the first recovery gate, read-only startup mode, or distributed-storage Safemode concept. (`H/P`, `X`)
- **1831 — retained namespace != reconstructed replica-location map:** `FsImage`/`EditLog` recover namespace and block-to-file relations, while DataNode Blockreports re-establish current knowledge of which nodes hold blocks. (`H/P`, `E`)
- **1832 — payload survival != NameNode knowledge of payload location:** a DataNode block can survive on local storage before its post-restart Blockreport has been incorporated by the NameNode. (`H/P`, `E`)
- **1833 — Blockreport re-observation != payload rewrite:** reporting an already-existing block reconstructs controller knowledge; it does not create a new payload embodiment merely by being reported. (`H/P`, `E`)
- **1834 — minimum-replica check-in != configured replication factor restored:** a block can satisfy the Safemode minimum while still being under-replicated relative to its ordinary target; post-Safemode replication remains a separate phase. (`H/P`)
- **1835 — safe-block percentage threshold != every block available:** Hadoop 1.0.4 publishes `0.999f` as a configurable default, demonstrating that the startup admission relation need not mean 100% of blocks have met the minimum; that default is release-bounded, not universal. (`H/P`, `X`)
- **1836 — threshold reached != Safemode exit complete:** the configured extension can keep the NameNode in Safemode after the ratio condition has been reached; Hadoop 2.8.0 retains explicit `reached` / extension state for this interval. (`H/P`)
- **1837 — startup Safemode != manual Safemode:** Hadoop 2.8.0 source tracks safe blocks for automatic startup exit but explicitly does not use that automatic-exit lifecycle for manually entered Safemode. (`H/P`)
- **1838 — retained/readable state != mutation authority:** the Hadoop 1.0.4 guide describes startup Safemode as essentially read-only while file-system/block modifications are withheld. (`H/P`, `E`)
- **1839 — withheld replication != absence of surviving replicas:** HDFS waits because enough replicas may already exist but have not yet reported; temporary non-action prevents premature reconstruction based on incomplete observations. (`H/P`, `E`)
- **1840 — withheld deletion != permanent undeletability or physical WORM:** Safemode's suppression of state-changing work is a service-policy condition, not evidence of irreversible media write protection, secure retention, or sanitization. (`E`, `X`)
- **1841 — safe/reported replica != checksum-integrity-qualified replica:** Case 83 separately grounds periodic checksum verification and corrupt-replica reporting; startup minimum-replica evidence is not a substitute for that integrity relation. (`A`, `X`)
- **1842 — safe-block count != rack/failure-domain placement qualification:** Case 80 separately grounds placement-policy satisfaction as distinct from replica count, so startup safe-block admission cannot silently stand in for decommission/placement admissibility. (`A`, `X`)
- **1843 — namespace recovery != end-to-end file availability:** reconstructing pathname and block-to-file metadata does not manufacture missing/unreported DataNode embodiments; historical metadata continuity and present payload embodiment evidence are separate recovery requirements. (`E`)
- **1844 — service-admission control state != user payload:** threshold, safe-replication minimum, `blockSafe`/`blockTotal`, live-DataNode conditions, `reached`, and extension govern when ordinary authority resumes but are not the application bytes being retained. (`H/P`, `E`)
- **1845 — Case 117 startup Safemode != Case 116 DataNode maintenance mode:** the former is a NameNode-wide startup admission gate while replica-location evidence is rebuilt; the latter is a per-DataNode temporary-withdrawal/expiry regime. The comparison is functional only and establishes no genealogy. (`A`, `X`)
- **1846 — related-repository boundary:** current `tmzncty/computing-archaeology` search found no dedicated HDFS Safemode case; broader HDFS/GFS recovery genealogy and Blockreport history belong there if developed, while Case 117 keeps only the retention-specific replay/re-observation/admission relation. (`H/P` project-state record)
"""

# ROADMAP: insert the newest bounded Phase-2 item at the top of the phase.
roadmap = ROADMAP.read_text(encoding="utf-8")
if case_path not in roadmap:
    marker = "## Phase 2 — Build missing technical bridges\n\n"
    if marker not in roadmap:
        raise SystemExit("ROADMAP Phase 2 marker not found")
    roadmap = roadmap.replace(marker, marker + roadmap_entry + "\n", 1)
    ROADMAP.write_text(roadmap, encoding="utf-8")

# CASE_INDEX table: place Case 117 immediately after Case 116.
index = INDEX.read_text(encoding="utf-8")
if case_path not in index:
    lines = index.splitlines()
    insert_at = None
    for i, line in enumerate(lines):
        if "cases/116-apache-hdfs-datanode-maintenance-state.md" in line and line.startswith("|"):
            insert_at = i + 1
            break
    if insert_at is None:
        raise SystemExit("Case 116 table row not found")
    lines.insert(insert_at, index_row)
    index = "\n".join(lines)

# Findings ledger: append one bounded section after the current Case 116 tail.
if "## Case 117 — HDFS startup Safemode findings" not in index:
    index = index.rstrip() + "\n\n" + findings.rstrip() + "\n"

INDEX.write_text(index, encoding="utf-8")

# Invariants.
roadmap_final = ROADMAP.read_text(encoding="utf-8")
index_final = INDEX.read_text(encoding="utf-8")
if roadmap_final.count(case_path) != 2:
    raise SystemExit(f"unexpected ROADMAP Case 117 path count: {roadmap_final.count(case_path)}")
if index_final.count(case_path) != 1:
    raise SystemExit(f"unexpected CASE_INDEX Case 117 path count: {index_final.count(case_path)}")
if index_final.count("## Case 117 — HDFS startup Safemode findings") != 1:
    raise SystemExit("Case 117 findings heading missing or duplicated")
for n in range(1830, 1847):
    token = f"**{n} —"
    if index_final.count(token) != 1:
        raise SystemExit(f"finding {n} missing or duplicated")
