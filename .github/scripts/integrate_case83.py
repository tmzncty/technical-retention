from pathlib import Path

CASE = "cases/83-apache-hdfs-block-scanner-checksum-verification.md"
EVID = "evidence/83-hadoop-2003-2016-block-scanner-grounding.md"


def insert_after_line(text: str, predicate, new_line: str, label: str) -> str:
    if new_line in text:
        return text
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if predicate(line):
            lines.insert(i + 1, new_line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    raise RuntimeError(f"anchor not found: {label}")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected one {label} anchor, got {count}")
    return text.replace(old, new, 1)


# README navigation
p = Path("README.md")
text = p.read_text()
readme_line = (
    "- [`cases/83-apache-hdfs-block-scanner-checksum-verification.md`]"
    "(cases/83-apache-hdfs-block-scanner-checksum-verification.md) — grounded HDFS distributed-integrity bridge: "
    "DataNode-local periodic/suspect-triggered checksum verification separates positive Blockreport presence from content-integrity qualification; "
    "qualifying failures are reported into distributed repair control, while saved scanner cursor/progress state preserves maintenance coverage across restart; "
    "see [`evidence/83-hadoop-2003-2016-block-scanner-grounding.md`](evidence/83-hadoop-2003-2016-block-scanner-grounding.md)."
)
text = insert_after_line(
    text,
    lambda line: line.startswith("- [") and "cases/82-micron-nand-copyback-ecc-requalification.md" in line,
    readme_line,
    "README Case 82 repository-map line",
)
p.write_text(text)

# ROADMAP: add the bounded bridge and make the broad bit-rot item explicitly partial.
p = Path("ROADMAP.md")
text = p.read_text()
roadmap_line = (
    "- [x] HDFS DataNode block-scanner / checksum-integrity qualification — "
    "[`cases/83-apache-hdfs-block-scanner-checksum-verification.md`](cases/83-apache-hdfs-block-scanner-checksum-verification.md), "
    "grounded by [`evidence/83-hadoop-2003-2016-block-scanner-grounding.md`](evidence/83-hadoop-2003-2016-block-scanner-grounding.md), "
    "adds a distributed integrity-maintenance regime in which a reported/present replica is not thereby checksum-qualified; per-volume scanners rate-limit periodic coverage, "
    "suspect blocks can be prioritized, qualifying verification failures are reported for later replica-management action, and block-iterator/cursor state is saved so maintenance progress itself can cross restart. "
    "This remains distinct from startup Blockreport re-observation (Case 79), ZFS scrub/self-heal (Case 18), physical media ECC, and the later act of re-replication or deletion; broad scanner genealogy and production fault validation remain separate work."
)
text = insert_after_line(
    text,
    lambda line: line.startswith("- [x]") and "cases/82-micron-nand-copyback-ecc-requalification.md" in line,
    roadmap_line,
    "ROADMAP Case 82 bridge line",
)
old_bitrot = "- [ ] bit rot;"
new_bitrot = (
    "- [ ] bit rot — **partially advanced by grounded Case 83 at the HDFS replicated-block layer**: "
    "periodic/suspect-triggered checksum verification can discover a corrupt local replica before ordinary demand and report it into distributed repair control, "
    "but device/media error physics, correlated corruption, checksum failure, independent fault validation, and long-term archival bit-rot regimes remain open;"
)
text = replace_once(text, old_bitrot, new_bitrot, "ROADMAP bit-rot")
p.write_text(text)

# CASE_INDEX main ledger row.
p = Path("CASE_INDEX.md")
text = p.read_text()
ledger_row = (
    "| [Apache HDFS DataNode Block Scanner: Periodic Checksum Verification, Retained Scan Progress, and Corrupt-Replica Reporting]"
    "(cases/83-apache-hdfs-block-scanner-checksum-verification.md) | **grounded** | "
    "DataNode-resident replicated block + checksum/replica metadata + periodic per-volume scanner + suspect-block priority + saved iterator/cursor + bad-replica report | "
    "separate positive replica presence from integrity qualification; periodic verification from demand reads; detection/reporting from repair/deletion; and payload retention from retained maintenance-progress state | "
    "[2003–2016 GFS/Apache grounding](evidence/83-hadoop-2003-2016-block-scanner-grounding.md); earliest HDFS scanner genealogy, cursor crash-atomicity, post-2.7 evolution, correlated-corruption analysis, and named-cluster fault validation remain separate work |"
)
text = insert_after_line(
    text,
    lambda line: line.startswith("| [") and "cases/82-micron-nand-copyback-ecc-requalification.md" in line,
    ledger_row,
    "CASE_INDEX Case 82 ledger row",
)

# Comparison matrix row.
matrix_row = (
    "| HDFS DataNode BlockScanner / 2008–2016 bounded regime | "
    "DataNode block replica + checksum/replica metadata + current block iterator/cursor + suspect queue + distributed corrupt-replica relation | "
    "rate-limited periodic per-volume traversal; saved cursor/progress; suspect-block priority; checksum/read verification; qualifying failure report; later NameNode-managed re-replication | "
    "background scanner reads/checks without an application consuming the payload; demand reads can also verify, but the two triggers are distinct | "
    "file/path -> block identity -> DataNode replica location, then local block/genstamp resolution plus checksum relation for integrity qualification | "
    "the replica may remain physically present while losing admissible-replica status; later replacement can preserve logical block identity on another DataNode | "
    "no complete verification history is required: current iterator/cursor/progress state is retained for coverage, while a successful check is a time-bounded observation rather than permanent trust |"
)
text = insert_after_line(
    text,
    lambda line: line.startswith("| Micron NAND IDM/COPYBACK / 2006–2015 bounded regime |"),
    matrix_row,
    "CASE_INDEX Case 82 comparison row",
)

# Findings 1005–1020.
findings = """\n## Case 83 — Apache HDFS DataNode BlockScanner findings

1005. **replica presence ≠ content-integrity qualification** — a DataNode can positively hold/report a block while a later checksum/read verification rejects that embodiment;
1006. **Blockreport ≠ checksum verification** — Case 79's inventory re-observation re-establishes location knowledge, whereas Case 83 separately asks whether a present replica passes the integrity path;
1007. **periodic verification ≠ demand read verification** — background scanning deliberately exercises blocks that no application currently needs, while ordinary reads can also expose checksum failure;
1008. **checksum verification ≠ payload repair** — scanning can establish that a replica is bad without creating a replacement payload;
1009. **corrupt-replica report ≠ physical deletion** — `reportBadBlocks` changes distributed knowledge/qualification before any separately scheduled removal of the local embodiment;
1010. **repair from another replica ≠ scanner-local rewrite** — the bounded scanner reports corruption; restoration of redundancy is a later distributed replication action using another good source;
1011. **scanner exception ≠ unconditional corruption verdict** — the 2.7.3 handler explicitly avoids reporting some missing/racy states as bad blocks, so event interpretation depends on concurrent replica state;
1012. **scan-progress state ≠ user payload** — iterator, cursor, schedule, suspect queue, throughput accounting, and scan statistics are maintenance-control state rather than the object being protected;
1013. **retained scanner cursor ≠ complete verification history** — saving traversal position across restart preserves coverage work without requiring a permanent event log of every successful check;
1014. **machine/process restart ≠ mandatory restart of maintenance from zero** — the bounded implementation saves iterator/cursor state using wall-clock information specifically because monotonic time commonly resets on reboot;
1015. **successful verification now ≠ permanent future integrity** — a passing scan is a bounded observation, and recurring scans remain meaningful because corruption can occur after the last check;
1016. **suspect-block priority ≠ ordinary periodic cadence** — event/suspicion-driven rescanning can pull one block forward while broad iterator coverage remains a separate maintenance schedule;
1017. **scan-period target ≠ continuous integrity visibility** — rate-limited traversal and week-scale rescan policy leave a nonzero interval in which a newly corrupted dormant replica may remain undiscovered;
1018. **inventory re-observation ≠ integrity qualification ≠ redundancy restoration** — Cases 79 and 83 together require three stages: know a replica is present, verify whether it remains acceptable, and later restore the desired replica margin if needed;
1019. **HDFS BlockScanner ≠ ZFS scrub as historical identity** — both proactively expose latent defects, but they differ in implementation locus, repair path, vocabulary, and system architecture; the comparison is functional only;
1020. **HDFS does not establish invention priority for proactive distributed integrity scanning** — GFS 2003 already documents checksum verification plus idle scanning of inactive chunks and replacement of corrupted replicas; direct genealogy remains unproven.\n"""
if "## Case 83 — Apache HDFS DataNode BlockScanner findings" not in text:
    anchor = "1004. **copyback support ≠ safe unrestricted use across devices/generations**"
    lines = text.splitlines()
    idx = next((i for i, line in enumerate(lines) if line.startswith(anchor)), None)
    if idx is None:
        raise RuntimeError("CASE_INDEX finding 1004 anchor not found")
    # Insert after the full finding line.
    lines.insert(idx + 1, findings.rstrip("\n"))
    text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")

p.write_text(text)

# Strong idempotency/integration checks.
readme = Path("README.md").read_text()
roadmap = Path("ROADMAP.md").read_text()
index = Path("CASE_INDEX.md").read_text()
for name, doc in [("README", readme), ("ROADMAP", roadmap), ("CASE_INDEX", index)]:
    if CASE not in doc:
        raise RuntimeError(f"{name} missing Case 83 path")
if EVID not in readme or EVID not in roadmap or EVID not in index:
    raise RuntimeError("grounding path not fully integrated")
if index.count(CASE) != 1:
    raise RuntimeError(f"expected one Case 83 ledger link in CASE_INDEX, got {index.count(CASE)}")
for n in range(1005, 1021):
    if index.count(f"{n}. **") != 1:
        raise RuntimeError(f"finding {n} missing or duplicated")
if index.count("| HDFS DataNode BlockScanner / 2008–2016 bounded regime |") != 1:
    raise RuntimeError("Case 83 comparison-matrix row missing or duplicated")
if "partially advanced by grounded Case 83 at the HDFS replicated-block layer" not in roadmap:
    raise RuntimeError("ROADMAP bit-rot status not updated")
print("case83 integration checks passed")
