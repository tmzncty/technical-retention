from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ROADMAP = ROOT / "ROADMAP.md"
INDEX = ROOT / "CASE_INDEX.md"
CASE = ROOT / "cases/53-dram-rowhammer-targeted-refresh-policy.md"
EVIDENCE = ROOT / "evidence/53-rowhammer-2012-2020-targeted-refresh-grounding.md"
WORKFLOW = ROOT / ".github/workflows/integrate-case53.yml"
SCRIPT = ROOT / "tools/integrate_case53.py"

CASE_LINK = "cases/53-dram-rowhammer-targeted-refresh-policy.md"
EVID_LINK = "evidence/53-rowhammer-2012-2020-targeted-refresh-grounding.md"


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
        raise RuntimeError(f"expected exactly one replacement anchor, got {count}: {old[:120]!r}")
    return text.replace(old, new, 1)


if not CASE.exists() or not EVIDENCE.exists():
    raise RuntimeError("Case 53 or its grounding record is missing")

# README navigation.
readme = README.read_text()
readme_case = "- [`cases/53-dram-rowhammer-targeted-refresh-policy.md`](cases/53-dram-rowhammer-targeted-refresh-policy.md) — grounded RowHammer/targeted-refresh bridge: repeated activation of one DRAM row can accelerate charge loss in physical neighbors, so access history and adjacency can create extra refresh urgency distinct from the ordinary periodic deadline; Intel 2012-priority targeted-refresh work, ISCA 2014 PARA, Micron DDR4 TRR documentation, and TRRespass 2020 keep proposal, product claim, and empirical guarantee separate."
readme = insert_after_line(readme, "cases/52-nand-flash-read-disturb-access-induced-decay.md", readme_case)
readme_evidence = "- [`evidence/53-rowhammer-2012-2020-targeted-refresh-grounding.md`](evidence/53-rowhammer-2012-2020-targeted-refresh-grounding.md) — Case-53 grounding record: Intel's 2012-priority row-hammer refresh-command architecture and Kim et al. 2014 bound mechanism/prior art; a Micron 2015 DDR4 datasheet supplies manufacturer TRR vocabulary, while TRRespass 2020 independently qualifies implementation-level immunity."
readme = insert_after_line(readme, "evidence/52-cai-2009-2015-nand-read-disturb-grounding.md", readme_evidence)
README.write_text(readme)

# ROADMAP: advance the explicit RowHammer-oriented refresh-policy gap without claiming the broad DRAM item complete.
roadmap = ROADMAP.read_text()
roadmap = replace_once(
    roadmap,
    "partially advanced by nine grounded bounded sub-slices",
    "partially advanced by ten grounded bounded sub-slices",
)
case53_roadmap = "[`cases/53-dram-rowhammer-targeted-refresh-policy.md`](cases/53-dram-rowhammer-targeted-refresh-policy.md), grounded by [`evidence/53-rowhammer-2012-2020-targeted-refresh-grounding.md`](evidence/53-rowhammer-2012-2020-targeted-refresh-grounding.md), adds an access-induced DRAM maintenance regime: repeated aggressor-row activation can accelerate charge loss in physical victim neighbors, so workload history and adjacency can create extra refresh urgency beyond the ordinary periodic deadline. Intel's 2012-priority targeted-refresh work prevents a false 2014 invention claim; Kim et al. distinguish global-refresh, hot-row tracking, and stateless probabilistic PARA; a bounded Micron DDR4 record documents background TRR; and TRRespass 2020 shows that a mitigation label does not itself prove implementation-level immunity. "
roadmap = replace_once(
    roadmap,
    "The broad item stays unchecked because a true JEDEC standards chronology",
    case53_roadmap + "The broad item stays unchecked because a true JEDEC standards chronology",
)
roadmap = replace_once(
    roadmap,
    "and RowHammer-oriented refresh policy remain distinct open regimes;",
    "and post-2020 RowHammer / DDR5 Refresh Management (`RFM`) evolution, exact normative mitigation semantics, and independent named-product fault validation remain distinct open regimes;",
)
ROADMAP.write_text(roadmap)

# CASE_INDEX: case ledger, matrix, total count, mechanism gate, and cross-case findings.
index = INDEX.read_text()
case_row = "| [DRAM RowHammer: Access-Induced Retention Loss, Targeted Refresh, and Mitigation Limits](cases/53-dram-rowhammer-targeted-refresh-policy.md) | **grounded** | periodic DRAM retention + access-induced neighbor disturbance + activation-history/topology-conditioned extra refresh + residual ECC | separate ordinary deadline refresh from disturbance-conditioned urgency; access-history control state from payload; aggressor identification from physical-victim resolution; abstract mitigation from deployed implementation guarantee | [2012–2020 RowHammer/targeted-refresh grounding](evidence/53-rowhammer-2012-2020-targeted-refresh-grounding.md); later DDR5 RFM, exact JEDEC chronology, post-2020 defenses, and independent named-product validation remain separate work |"
index = insert_after_line(index, "cases/52-nand-flash-read-disturb-access-induced-decay.md", case_row)

matrix_row = "| DRAM RowHammer / 2012–2020 bounded regime | victim-row capacitor charge + ordinary refresh schedule + aggressor activation relation + physical-neighbor/topology relation + detector/probability/TRR policy state | ordinary periodic refresh continues; repeated aggressor activation can accelerate neighbor leakage; mitigations add global or targeted restoration, counters/detectors, probabilistic PARA, or in-DRAM TRR | aggressor accesses can succeed while an unaccessed victim loses margin; residual ECC is distinct from preventive refresh | logical row identity does not necessarily reveal physical adjacency; controller can identify a hammered row while DRAM resolves physical victim neighbors | targeted refresh restores logical victim state without preserving one uninterrupted physical charge embodiment; internal remapping can change which physical rows are neighbors | no user history is implied; recent activation counts/detector state may be retained, while PARA demonstrates workload-conditioned maintenance without per-row history tables |"
index = insert_after_line(index, "NAND read disturb / 2009–2015 bounded regime", matrix_row)

index = replace_once(
    index,
    "After fifty-three bounded cases, **all fifty-three cases are now `grounded`.**",
    "After fifty-four bounded cases, **all fifty-four cases are now `grounded`.**",
)
index = replace_once(index, "currently fifty-three;", "currently fifty-four;")

findings = """528. **meeting the ordinary refresh schedule ≠ immunity to access-induced retention loss** — RowHammer adds an access-coupled route by which a neighboring victim can lose charge margin faster than the ordinary periodic schedule assumes;
529. **periodic refresh deadline ≠ disturbance-conditioned refresh urgency** — elapsed-time restoration remains necessary, while repeated aggressor activation can create additional victim-row maintenance before the next ordinary refresh;
530. **recent access history can become constitutive retention-policy state** — threshold/counter-based RowHammer defenses retain evidence about recent row activation because that evidence decides where extra restoration should be spent;
531. **workload-conditioned maintenance ≠ necessarily explicit per-row history retention** — PARA makes adjacent-row maintenance statistically dependent on row closes while intentionally avoiding per-row activation counters/address tables;
532. **aggressor identification ≠ victim-row physical resolution** — a controller may know which logical row was hammered while the DRAM device resolves which physical neighboring row or rows are actually at disturbance risk;
533. **logical row adjacency ≠ physical disturbance adjacency** — manufacturer-specific layout and internal remapping can separate host/controller-visible row numbering from the physical neighborhood that determines coupling;
534. **more frequent global refresh ≠ targeted disturbance mitigation** — globally shortening the interval spends restoration work on all rows, whereas targeted methods require detection/topology/probability policy to choose extra victim refreshes;
535. **retention obligation ≠ maintenance scheduling policy** — the obligation is to keep victim charge inside a recoverable margin; counters, targeted commands, PARA probability, and in-DRAM TRR are different policies for satisfying that obligation;
536. **counter-free/stateless policy ≠ zero retention work** — PARA removes per-row history tables but still performs probabilistic adjacent-row activations and therefore still spends bandwidth/energy on preservation;
537. **stateless mitigation ≠ deterministic guarantee** — the 2014 PARA proposal explicitly retains a nonzero modeled residual failure probability rather than proving absolute prevention;
538. **modeled low failure probability ≠ measured deployed-system immunity** — PARA's evaluation does not establish a named commercial implementation or field guarantee;
539. **TRR presence ≠ universal RowHammer immunity** — TRRespass's bounded 2020 sample found TRR-aware patterns that induced flips in 13 of 42 tested DDR4 modules, so the mitigation class cannot be equated with universal containment;
540. **mitigation-class label ≠ complete implementation contract** — opaque tracker capacity, sampling, topology, thresholds, and policy can materially change which hammering patterns a device actually contains;
541. **refresh localization for service concurrency ≠ refresh targeting for disturbance containment** — DDR5 Same Bank Refresh localizes ordinary maintenance around bank/group availability, while RowHammer mitigation localizes extra restoration around an aggressor/victim disturbance relation;
542. **disturbance prevention/restoration ≠ residual error correction** — targeted victim refresh tries to prevent corruption by renewing charge, whereas ECC acts on raw errors after they exist within a correction envelope;
543. **intrinsic retention weakness ≠ access-induced victimhood** — a row need not be intrinsically short-retention to become unsafe when another physically coupled row is activated pathologically often;
544. **2014 experimental characterization ≠ invention of RowHammer-aware targeted refresh** — Intel's 2012-priority filing already discloses row-hammer thresholds, victim adjacency, and targeted-refresh commands, so the 2014 paper's historical contribution must remain bounded to open characterization, system demonstration, mitigation comparison, and PARA.

"""
if "528. **meeting the ordinary refresh schedule" not in index:
    marker = "These are provisional cross-case findings, not final philosophical conclusions."
    if index.count(marker) != 1:
        raise RuntimeError("cross-case findings insertion marker not unique")
    index = index.replace(marker, findings + marker, 1)
INDEX.write_text(index)

# Structural validation before committing.
for file_path, needle in [
    (README, CASE_LINK),
    (README, EVID_LINK),
    (ROADMAP, CASE_LINK),
    (ROADMAP, EVID_LINK),
    (INDEX, CASE_LINK),
    (INDEX, EVID_LINK),
]:
    if file_path.read_text().count(needle) < 1:
        raise RuntimeError(f"missing integrated link {needle} in {file_path.name}")

idx = INDEX.read_text()
if "After fifty-four bounded cases, **all fifty-four cases are now `grounded`.**" not in idx:
    raise RuntimeError("case-count status not updated")
if "currently fifty-four;" not in idx:
    raise RuntimeError("mechanism-gate count not updated")
if idx.count("528. **meeting the ordinary refresh schedule") != 1 or idx.count("544. **2014 experimental characterization") != 1:
    raise RuntimeError("finding range 528–544 is incomplete or duplicated")
if "post-2020 RowHammer / DDR5 Refresh Management (`RFM`) evolution" not in ROADMAP.read_text():
    raise RuntimeError("RowHammer roadmap gap was not narrowed")

# Remove one-shot integration machinery from the resulting tree.
if WORKFLOW.exists():
    WORKFLOW.unlink()
if SCRIPT.exists():
    SCRIPT.unlink()

subprocess.run(["git", "config", "user.name", "github-actions[bot]"], cwd=ROOT, check=True)
subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], cwd=ROOT, check=True)
subprocess.run([
    "git", "add", "README.md", "ROADMAP.md", "CASE_INDEX.md",
    ".github/workflows/integrate-case53.yml", "tools/integrate_case53.py"
], cwd=ROOT, check=True)
subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, check=True)
if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode == 0:
    print("Case 53 navigation/status already integrated; no commit needed")
else:
    subprocess.run(["git", "commit", "-m", "docs: integrate grounded RowHammer targeted-refresh case"], cwd=ROOT, check=True)
    subprocess.run(["git", "push", "origin", "HEAD:main"], cwd=ROOT, check=True)
