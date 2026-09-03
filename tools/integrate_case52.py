from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ROADMAP = ROOT / "ROADMAP.md"
INDEX = ROOT / "CASE_INDEX.md"
CASE = ROOT / "cases/52-nand-flash-read-disturb-access-induced-decay.md"
EVIDENCE = ROOT / "evidence/52-cai-2009-2015-nand-read-disturb-grounding.md"
WORKFLOW = ROOT / ".github/workflows/integrate-case52.yml"
SCRIPT = ROOT / "tools/integrate_case52.py"

CASE_LINK = "cases/52-nand-flash-read-disturb-access-induced-decay.md"
EVID_LINK = "evidence/52-cai-2009-2015-nand-read-disturb-grounding.md"


def insert_after_line(text: str, needle: str, new_line: str) -> str:
    if new_line in text:
        return text
    lines = text.splitlines()
    hits = [i for i, line in enumerate(lines) if needle in line]
    if len(hits) != 1:
        raise RuntimeError(f"expected exactly one anchor for {needle!r}, got {len(hits)}")
    lines.insert(hits[0] + 1, new_line)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count == 0 and new in text:
        return text
    if count != 1:
        raise RuntimeError(f"expected exactly one replacement anchor, got {count}: {old[:100]!r}")
    return text.replace(old, new, 1)


if not CASE.exists() or not EVIDENCE.exists():
    raise RuntimeError("Case 52 or its grounding record is missing")

# README navigation
readme = README.read_text()
readme_case = "- [`cases/52-nand-flash-read-disturb-access-induced-decay.md`](cases/52-nand-flash-read-disturb-access-induced-decay.md) — grounded NAND read-disturb bridge: reading one page can cumulatively shift unread same-block cell thresholds through pass-through voltage stress; read-count history, P/E wear, ECC margin, Vpass tuning, relocation, and probabilistic RDR remain separate retention/recovery relations."
readme = insert_after_line(readme, "cases/51-apache-hdfs-datanode-command-fencing.md", readme_case)
readme_evidence = "- [`evidence/52-cai-2009-2015-nand-read-disturb-grounding.md`](evidence/52-cai-2009-2015-nand-read-disturb-grounding.md) — Case-52 grounding record: a 2009-priority controller patent and 2013 APSys prior art bound read-count/relocation chronology, while Cai et al. DSN 2015 directly characterize commercial 2Y-nm MLC read disturb and keep measured device physics separate from proposed Vpass Tuning/RDR deployment."
readme = insert_after_line(readme, "evidence/51-hadoop-2011-2016-datanode-command-fencing-grounding.md", readme_evidence)
README.write_text(readme)

# ROADMAP: add Case 52 to the SSD/controller bridge and maintenance vocabulary.
roadmap = ROADMAP.read_text()
roadmap = replace_once(
    roadmap,
    "partially advanced by grounded Cases 15, 20, 30, 31, 32, 36, 37, 38, 39, 44, and 47",
    "partially advanced by grounded Cases 15, 20, 30, 31, 32, 36, 37, 38, 39, 44, 47, and 52",
)
case52_roadmap = "[`cases/52-nand-flash-read-disturb-access-induced-decay.md`](cases/52-nand-flash-read-disturb-access-induced-decay.md), grounded by [`evidence/52-cai-2009-2015-nand-read-disturb-grounding.md`](evidence/52-cai-2009-2015-nand-read-disturb-grounding.md), adds an access-induced reliability regime: a successful read to one NAND page can apply `Vpass` stress to unread same-block cells, making cumulative read count a maintenance clock distinct from elapsed retention age. Earlier patent/APSys evidence prevents a false 2015 invention claim, while the DSN 2015 commercial-chip measurements keep read disturb, retention loss, P/E wear, ECC margin, voltage tuning, relocation, and probabilistic recovery distinct. "
roadmap = replace_once(
    roadmap,
    "The broad item stays unchecked because independent named-product PLP fault compliance",
    case52_roadmap + "The broad item stays unchecked because independent named-product PLP fault compliance",
)
roadmap = replace_once(
    roadmap,
    "and filesystem/database composition remain distinct regimes.",
    "modern 3D-NAND read-reclaim/device-specific read-disturb management, and filesystem/database composition remain distinct regimes.",
)
maintenance_anchor = "- SSD firmware, reclamation, wear management, bad-block replacement;"
maintenance_line = "- NAND read-disturb counting, pass-through-voltage mitigation, and access-stress-triggered relocation/recovery;"
roadmap = insert_after_line(roadmap, maintenance_anchor, maintenance_line)
ROADMAP.write_text(roadmap)

# CASE_INDEX case table, comparison matrix, count, and findings.
index = INDEX.read_text()
case_row = "| [NAND Flash Read Disturb: Access-Induced Decay, Vpass Mitigation, and Recovery](cases/52-nand-flash-read-disturb-access-induced-decay.md) | **grounded** | selected-page read + elevated `Vpass` on unselected same-block cells + cumulative read-count stress + threshold-voltage drift + ECC margin + optional relocation/RDR | separate present read success from future neighbor-retention cost; access-count maintenance from retention-age refresh; selected-page nondestructiveness from zero material disturbance elsewhere; measured chip behavior from proposed controller mitigation/recovery | [2009–2015 NAND read-disturb grounding](evidence/52-cai-2009-2015-nand-read-disturb-grounding.md); later 3D-NAND/read-reclaim history, named-controller deployment, and independent product fault validation remain separate work |"
index = insert_after_line(index, "cases/51-apache-hdfs-datanode-command-fencing.md", case_row)
matrix_row = "| NAND read disturb / 2009–2015 bounded regime | threshold-voltage cell states + logical payload + ECC margin + cumulative read-count/wear and optional Vpass/mapping policy | ordinary reads impose pass-through stress on unselected cells; controller policy can count reads, tune Vpass, or relocate/rewrite; RDR experimentally adds controlled disturb for recovery inference | requested read can succeed while neighboring unread cells accumulate stress; ECC can mask raw errors until correction margin is exhausted | logical request resolves through mapping to a physical page/block; physical block membership determines which unselected cells share read-pass stress | logical payload can survive relocation to a new physical block while the old embodiment is retired; RDR can infer logical state without restoring the earlier Vth distribution | no user history is implied; bounded read-count/wear/policy state can retain access-stress evidence that controls future maintenance |"
index = insert_after_line(index, "HDFS DataNode command fencing / 2011 HA design + Hadoop 2.7.3 bounded regime", matrix_row)
index = replace_once(
    index,
    "After fifty-two bounded cases, **all fifty-two cases are now `grounded`.**",
    "After fifty-three bounded cases, **all fifty-three cases are now `grounded`.**",
)
findings = """515. **successful selected-page read ≠ zero material change to neighboring retained state** — NAND read access requires pass-through voltage on unselected same-block cells, and repeated exposure can cumulatively shift their threshold voltages even while the requested page is returned correctly;
516. **logical nondestructiveness of the requested read ≠ zero future-retention cost to the surrounding physical block** — Case 52 does not show the selected page being destroyed on every read; it shows that access can spend future error margin in other cells coupled by NAND read geometry;
517. **access count can become a retention-maintenance clock** — 2009-priority controller evidence explicitly retains a per-block read count and uses threshold crossing to trigger relocation behavior, making cumulative use rather than elapsed wall time a maintenance input;
518. **read hotness ≠ write wear, while read hotness can consume future error margin** — many reads can accumulate disturb without host rewrites, while the 2015 measurements separately show that prior P/E wear increases susceptibility to each disturb;
519. **read-disturb accumulation ≠ retention-age leakage** — Cai et al. treat read disturb and retention as separate error sources that can coexist in one raw-error/ECC budget; a common later rewrite does not make their physical causes or trigger variables identical;
520. **ECC-correctable successful read ≠ undisturbed physical state** — raw disturb errors can remain masked by ECC before interface-visible loss, so present payload availability does not prove unchanged physical or future-correction margin;
521. **access-stress-triggered maintenance ≠ elapsed-retention-time refresh** — Case 36 renews NAND under retention-age/wear pressure, while Case 52 adds cumulative read activity as a distinct stress signal even though both may eventually relocate/rewrite data;
522. **physical block coupling ≠ logical request scope** — one logical page request resolves to a physical NAND block whose unselected cells participate electrically in the read path; the material disturbance domain is wider than the value explicitly requested;
523. **lower Vpass ≠ free reliability improvement** — reducing pass-through voltage lowers read-disturb stress but can create additional read errors when unselected cells no longer conduct with sufficient margin, so mitigation is an error-budget tradeoff rather than stress elimination;
524. **additional controlled disturbance can become recovery evidence** — the proposed RDR mechanism intentionally induces further read disturb after an uncorrectable read and uses differential threshold response to classify susceptible cells before retrying ECC;
525. **inferred logical recovery ≠ restoration of the prior physical threshold distribution** — RDR probabilistically reconstructs likely logical values from measured response to extra disturbance; it does not demonstrate physical reversal of the charge/threshold shifts that produced the failed read;
526. **2015 commercial-chip characterization ≠ invention of read-disturb mitigation** — US7818525B1 has 2009 priority and already documents `Read Disturb`, ECC, block read counting, threshold-triggered movement, and mapping updates; APSys 2013 independently predates the 2015 characterization with FTL-oriented management;
527. **commercial-chip characterization ≠ commercial-controller deployment** — the DSN 2015 experiments directly ground 2Y-nm MLC device behavior and experimental recovery, while Vpass Tuning/RDR remain proposed/evaluated mechanisms rather than named shipped-controller evidence.

"""
if "515. **successful selected-page read" not in index:
    marker = "These are provisional cross-case findings, not final philosophical conclusions."
    if index.count(marker) != 1:
        raise RuntimeError("cross-case findings insertion marker not unique")
    index = index.replace(marker, findings + marker, 1)
INDEX.write_text(index)

# Structural validation before committing.
checks = {
    "README case": README.read_text().count(CASE_LINK),
    "README evidence": README.read_text().count(EVID_LINK),
    "ROADMAP case": ROADMAP.read_text().count(CASE_LINK),
    "ROADMAP evidence": ROADMAP.read_text().count(EVID_LINK),
    "INDEX case": INDEX.read_text().count(CASE_LINK),
    "INDEX evidence": INDEX.read_text().count(EVID_LINK),
}
for name, count in checks.items():
    if count < 1:
        raise RuntimeError(f"missing integrated link: {name}")
if "After fifty-three bounded cases, **all fifty-three cases are now `grounded`.**" not in INDEX.read_text():
    raise RuntimeError("case-count status not updated")
if INDEX.read_text().count("515. **successful selected-page read") != 1 or INDEX.read_text().count("527. **commercial-chip characterization") != 1:
    raise RuntimeError("finding range 515–527 is incomplete or duplicated")

# Remove one-shot integration machinery from the resulting tree.
if WORKFLOW.exists():
    WORKFLOW.unlink()
if SCRIPT.exists():
    SCRIPT.unlink()

subprocess.run(["git", "config", "user.name", "github-actions[bot]"], cwd=ROOT, check=True)
subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], cwd=ROOT, check=True)
subprocess.run(["git", "add", "README.md", "ROADMAP.md", "CASE_INDEX.md", ".github/workflows/integrate-case52.yml", "tools/integrate_case52.py"], cwd=ROOT, check=True)
subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, check=True)
if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode == 0:
    print("Case 52 navigation/status already integrated; no commit needed")
else:
    subprocess.run(["git", "commit", "-m", "docs: integrate grounded NAND read-disturb case"], cwd=ROOT, check=True)
    subprocess.run(["git", "push", "origin", "HEAD:main"], cwd=ROOT, check=True)
